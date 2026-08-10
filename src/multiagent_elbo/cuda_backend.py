"""Side-effect-free controller for the standalone Python 3.12 worker."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from types import MappingProxyType
from typing import Literal, Mapping

import numpy as np

from .experiment_support import (
    CUDA_WORKER_PROTOCOL_VERSION,
    validate_worker_protocol_manifest,
)


Backend = Literal["cpu", "cuda"]
ScientificDtype = Literal["float64", "float32", "bfloat16"]
_JOB_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_ARRAY_NAME = _JOB_ID
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_NUMPY_DTYPES = {
    "float64": np.dtype("<f8"),
    "float32": np.dtype("<f4"),
    "int64": np.dtype("<i8"),
    "bool": np.dtype(np.bool_),
}


class WorkerBackendError(RuntimeError):
    """Raised when controller-worker validation or execution fails."""


@dataclass(frozen=True)
class WorkerJobResult:
    request_manifest: Mapping[str, object]
    response_manifest: Mapping[str, object]
    arrays: Mapping[str, np.ndarray]
    provenance: Mapping[str, object]
    request_json: Path
    input_npz: Path
    response_json: Path
    output_npz: Path


@dataclass(frozen=True)
class ParityDiagnostics:
    maximum_absolute_residual: float
    maximum_relative_residual: float
    atol: float
    rtol: float
    passed: bool


def _canonical_dtype_array(array: np.ndarray, dtype: str) -> np.ndarray:
    if dtype == "bfloat16":
        if array.dtype != np.uint16:
            raise ValueError("bfloat16 arrays must use canonical uint16 bit patterns")
        return np.ascontiguousarray(array.astype("<u2", copy=False))
    canonical_dtype = _NUMPY_DTYPES.get(dtype)
    if canonical_dtype is None:
        raise ValueError(f"unsupported worker dtype: {dtype}")
    if dtype == "bool":
        return np.ascontiguousarray(array.astype(np.bool_, copy=False))
    return np.ascontiguousarray(array.astype(canonical_dtype, copy=False))


def _dtype_name(array: np.ndarray) -> str:
    dtype = array.dtype
    if dtype == np.dtype(np.float64):
        return "float64"
    if dtype == np.dtype(np.float32):
        return "float32"
    if dtype == np.dtype(np.int64):
        return "int64"
    if dtype == np.dtype(np.bool_):
        return "bool"
    raise ValueError(f"unsupported array dtype: {dtype}")


def canonical_array_sha256(name: str, values: object, dtype: str) -> str:
    """Hash one array with the frozen name/dtype/shape/data framing."""
    if type(name) is not str or _ARRAY_NAME.fullmatch(name) is None:
        raise ValueError("invalid array name")
    array = _canonical_dtype_array(np.asarray(values), dtype)
    shape_json = json.dumps(list(array.shape), separators=(",", ":"))
    prefix = (
        b"cuda-worker-array-v1\0"
        + name.encode("utf-8")
        + b"\0"
        + dtype.encode("ascii")
        + b"\0"
        + shape_json.encode("utf-8")
        + b"\0"
    )
    return hashlib.sha256(prefix + array.tobytes(order="C")).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _parse_environment_lock(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise WorkerBackendError(f"environment lock does not exist: {path}")
    records: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        records[key] = value
    required = {
        "python_executable_sha256",
        "required_CUBLAS_WORKSPACE_CONFIG",
        "required_scientific_confirmation_dtype",
    }
    if not required <= records.keys():
        raise WorkerBackendError("environment lock is missing required records")
    return records


def _validate_job_inputs(
    *,
    job_id: str,
    requested_backend: str,
    requested_dtype: str,
    arrays: Mapping[str, np.ndarray],
) -> dict[str, np.ndarray]:
    if type(job_id) is not str or _JOB_ID.fullmatch(job_id) is None:
        raise WorkerBackendError("invalid immutable job ID")
    if requested_backend not in {"cpu", "cuda"}:
        raise WorkerBackendError("requested backend must be cpu or cuda")
    if requested_dtype not in {"float64", "float32", "bfloat16"}:
        raise WorkerBackendError("requested dtype is invalid")
    if set(arrays) != {
        "coefficients",
        "spatial_map",
        "matrix_direction",
        "batch_size",
    }:
        raise WorkerBackendError("worker input arrays do not match the fixed-ray kernel")
    normalized = {name: np.asarray(value) for name, value in arrays.items()}
    coefficients = normalized["coefficients"]
    spatial_map = normalized["spatial_map"]
    matrix_direction = normalized["matrix_direction"]
    batch_size = normalized["batch_size"]
    expected_dtype = np.dtype(np.float64 if requested_dtype == "float64" else np.float32)
    if requested_dtype == "bfloat16":
        raise WorkerBackendError("bfloat16 requires a separately encoded exploratory payload")
    if coefficients.dtype != expected_dtype or spatial_map.dtype != expected_dtype or matrix_direction.dtype != expected_dtype:
        raise WorkerBackendError("scientific input dtypes must equal requested dtype")
    if coefficients.ndim != 2 or spatial_map.ndim != 2 or spatial_map.shape[0] != spatial_map.shape[1]:
        raise WorkerBackendError("coefficients and spatial_map have invalid shapes")
    if coefficients.shape[1] != spatial_map.shape[0]:
        raise WorkerBackendError("coefficient width must match spatial map")
    if matrix_direction.ndim != 2 or matrix_direction.shape[0] != matrix_direction.shape[1]:
        raise WorkerBackendError("matrix_direction must be square")
    if batch_size.shape != () or batch_size.dtype != np.dtype(np.int64) or int(batch_size) <= 0:
        raise WorkerBackendError("batch_size must be one positive int64 scalar")
    if not all(np.all(np.isfinite(array)) for array in (coefficients, spatial_map, matrix_direction)):
        raise WorkerBackendError("scientific worker inputs must be finite")
    if not np.allclose(matrix_direction, matrix_direction.T, rtol=0.0, atol=0.0):
        raise WorkerBackendError("matrix_direction must be exactly symmetric")
    if np.min(np.linalg.eigvalsh(matrix_direction.astype(np.float64))) <= 0.0:
        raise WorkerBackendError("matrix_direction must be positive definite")
    return {
        "batch_size": np.array(batch_size, dtype=np.int64, copy=True),
        "coefficients": np.ascontiguousarray(coefficients),
        "matrix_direction": np.ascontiguousarray(matrix_direction),
        "spatial_map": np.ascontiguousarray(spatial_map),
    }


def _descriptors(arrays: Mapping[str, np.ndarray]) -> list[dict[str, object]]:
    descriptors: list[dict[str, object]] = []
    for name in sorted(arrays):
        dtype = _dtype_name(arrays[name])
        descriptors.append(
            {
                "name": name,
                "shape": list(arrays[name].shape),
                "dtype": dtype,
                "sha256": canonical_array_sha256(name, arrays[name], dtype),
            }
        )
    return descriptors


def _atomic_json(path: Path, payload: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False),
        encoding="utf-8",
    )
    os.replace(temporary, path)


def validate_worker_result(
    *,
    request_manifest: Mapping[str, object],
    response_manifest: Mapping[str, object],
    output_npz: Path,
) -> Mapping[str, np.ndarray]:
    """Validate response binding plus the exact NPZ and per-array identities."""
    validated = validate_worker_protocol_manifest(
        response_manifest,
        expected_message_type="response",
        request_manifest=request_manifest,
    )
    if not Path(output_npz).is_file():
        raise WorkerBackendError("worker output NPZ is missing")
    if _file_sha256(Path(output_npz)) != validated.npz_sha256:
        raise WorkerBackendError("worker output NPZ SHA-256 does not match response")
    with np.load(output_npz, allow_pickle=False) as archive:
        if set(archive.files) != {descriptor.name for descriptor in validated.arrays}:
            raise WorkerBackendError("worker output array inventory does not match response")
        arrays = {name: np.array(archive[name], copy=True) for name in archive.files}
    for descriptor in validated.arrays:
        array = arrays[descriptor.name]
        if tuple(array.shape) != descriptor.shape:
            raise WorkerBackendError(f"worker output shape mismatch: {descriptor.name}")
        try:
            dtype = _dtype_name(array)
        except ValueError as error:
            raise WorkerBackendError(str(error)) from error
        if dtype != descriptor.dtype:
            raise WorkerBackendError(f"worker output dtype mismatch: {descriptor.name}")
        if canonical_array_sha256(descriptor.name, array, dtype) != descriptor.sha256:
            raise WorkerBackendError(f"worker output array SHA-256 mismatch: {descriptor.name}")
        array.setflags(write=False)
    return MappingProxyType(arrays)


def run_worker_job(
    *,
    worker_python: Path,
    worker_script: Path,
    work_root: Path,
    job_id: str,
    requested_backend: Backend,
    requested_dtype: ScientificDtype,
    arrays: Mapping[str, np.ndarray],
    environment_lock: Path,
    timeout_seconds: float = 120.0,
) -> WorkerJobResult:
    """Run one validated immutable worker job without importing Torch."""
    worker_python = Path(worker_python).resolve(strict=True)
    worker_script = Path(worker_script).resolve(strict=True)
    environment_lock = Path(environment_lock).resolve(strict=True)
    normalized = _validate_job_inputs(
        job_id=job_id,
        requested_backend=requested_backend,
        requested_dtype=requested_dtype,
        arrays=arrays,
    )
    lock_records = _parse_environment_lock(environment_lock)
    executable_sha256 = _file_sha256(worker_python)
    if requested_backend == "cuda" and executable_sha256 != lock_records["python_executable_sha256"]:
        raise WorkerBackendError(
            "requested CUDA requires the pinned CUDA worker executable"
        )
    environment_sha256 = _file_sha256(environment_lock)

    work_root = Path(work_root)
    if work_root.exists():
        raise WorkerBackendError(f"worker job path already exists: {work_root}")
    work_root.mkdir(parents=True, exist_ok=False)
    input_npz = work_root / "input.npz"
    request_json = work_root / "request.json"
    response_json = work_root / "response.json"
    output_npz = work_root / "output.npz"
    np.savez(input_npz, **normalized)
    request_manifest: dict[str, object] = {
        "schema_version": CUDA_WORKER_PROTOCOL_VERSION,
        "message_type": "request",
        "job_id": job_id,
        "requested_backend": requested_backend,
        "requested_dtype": requested_dtype,
        "effective_backend": None,
        "effective_dtype": None,
        "environment_sha256": environment_sha256,
        "npz_sha256": _file_sha256(input_npz),
        "arrays": _descriptors(normalized),
        "output_identity": None,
    }
    validate_worker_protocol_manifest(request_manifest, expected_message_type="request")
    _atomic_json(request_json, request_manifest)

    environment = os.environ.copy()
    environment["CUBLAS_WORKSPACE_CONFIG"] = lock_records[
        "required_CUBLAS_WORKSPACE_CONFIG"
    ]
    completed = subprocess.run(
        [
            str(worker_python),
            str(worker_script),
            str(request_json),
            str(input_npz),
            str(response_json),
            str(output_npz),
        ],
        cwd=worker_script.parent,
        env=environment,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )
    if completed.returncode != 0:
        raise WorkerBackendError(
            f"worker failed with exit {completed.returncode}: {completed.stderr.strip()}"
        )
    try:
        response_manifest = json.loads(response_json.read_text(encoding="utf-8"))
        worker_provenance = json.loads(completed.stdout.strip())
    except (OSError, json.JSONDecodeError) as error:
        raise WorkerBackendError("worker emitted invalid response or provenance JSON") from error
    arrays_out = validate_worker_result(
        request_manifest=request_manifest,
        response_manifest=response_manifest,
        output_npz=output_npz,
    )
    if not isinstance(worker_provenance, dict):
        raise WorkerBackendError("worker provenance must be a JSON object")
    provenance = dict(worker_provenance)
    provenance.update(
        {
            "environment_sha256": environment_sha256,
            "worker_executable": str(worker_python),
            "worker_executable_sha256": executable_sha256,
            "worker_script_sha256": _file_sha256(worker_script),
            "requested_backend": requested_backend,
            "effective_backend": response_manifest["effective_backend"],
            "requested_dtype": requested_dtype,
            "effective_dtype": response_manifest["effective_dtype"],
            "kernel_strategy": "batched_spatial_map_matmul",
            "batch_size": int(normalized["batch_size"]),
            "cublas_workspace_config": environment[
                "CUBLAS_WORKSPACE_CONFIG"
            ],
        }
    )
    return WorkerJobResult(
        request_manifest=MappingProxyType(request_manifest),
        response_manifest=MappingProxyType(response_manifest),
        arrays=arrays_out,
        provenance=MappingProxyType(provenance),
        request_json=request_json,
        input_npz=input_npz,
        response_json=response_json,
        output_npz=output_npz,
    )


def parity_diagnostics(
    reference: object,
    candidate: object,
    *,
    dtype: ScientificDtype,
    condition_number: float,
) -> ParityDiagnostics:
    """Apply a declared dtype- and condition-scaled CPU/worker parity rule."""
    left = np.asarray(reference, dtype=np.float64)
    right = np.asarray(candidate, dtype=np.float64)
    if left.shape != right.shape:
        raise ValueError("parity arrays must have equal shapes")
    if not np.all(np.isfinite(left)) or not np.all(np.isfinite(right)):
        raise ValueError("parity arrays must be finite")
    if not np.isfinite(condition_number) or condition_number < 1.0:
        raise ValueError("condition_number must be finite and at least one")
    base = {
        "float64": (1.0e-12, 1.0e-10),
        "float32": (2.0e-6, 2.0e-5),
        "bfloat16": (2.0e-2, 5.0e-2),
    }[dtype]
    condition_scale = min(max(condition_number**0.5, 1.0), 1.0e4)
    atol = base[0] * condition_scale
    rtol = base[1] * condition_scale
    absolute = np.abs(left - right)
    scale = np.maximum(np.abs(left), np.abs(right))
    relative = np.divide(
        absolute,
        scale,
        out=np.zeros_like(absolute),
        where=scale > 0.0,
    )
    maximum_absolute = float(np.max(absolute)) if absolute.size else 0.0
    maximum_relative = float(np.max(relative)) if relative.size else 0.0
    return ParityDiagnostics(
        maximum_absolute_residual=maximum_absolute,
        maximum_relative_residual=maximum_relative,
        atol=atol,
        rtol=rtol,
        passed=bool(np.all(absolute <= atol + rtol * scale)),
    )


__all__ = [
    "ParityDiagnostics",
    "WorkerBackendError",
    "WorkerJobResult",
    "canonical_array_sha256",
    "parity_diagnostics",
    "run_worker_job",
    "validate_worker_result",
]
