"""Standalone NumPy/Torch worker for the frozen JSON/NPZ protocol.

This file intentionally does not import ``multiagent_elbo``. It is an internal
worker process behind click-to-run controllers, not a user-facing CLI.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time
from typing import Mapping

import numpy as np


PROTOCOL = "cuda-worker-protocol-v1"
KEYS = {
    "schema_version",
    "message_type",
    "job_id",
    "requested_backend",
    "requested_dtype",
    "effective_backend",
    "effective_dtype",
    "environment_sha256",
    "npz_sha256",
    "arrays",
    "output_identity",
}
ARRAY_KEYS = {"name", "shape", "dtype", "sha256"}
JOB_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
NUMPY_DTYPES = {
    "float64": np.dtype("<f8"),
    "float32": np.dtype("<f4"),
    "int64": np.dtype("<i8"),
    "bool": np.dtype(np.bool_),
}
PROVENANCE_SCHEMA = "cuda-worker-provenance-v1"
PREFLIGHT_SCHEMA = "cuda-worker-preflight-v1"


class ProtocolError(ValueError):
    pass


def _driver_version() -> str:
    completed = subprocess.run(
        [
            "nvidia-smi",
            "--query-gpu=driver_version",
            "--format=csv,noheader,nounits",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0 or not completed.stdout.strip():
        raise ProtocolError("CUDA driver version query failed")
    return completed.stdout.splitlines()[0].strip()


def _windows_file_version(path: Path) -> str:
    completed = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-Command",
            "(Get-Item -LiteralPath $args[0]).VersionInfo.FileVersion",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0 or not completed.stdout.strip():
        raise ProtocolError(f"library version query failed: {path.name}")
    return completed.stdout.strip().replace(", ", ".")


def _cuda_library_records(torch: object) -> dict[str, object]:
    library_root = Path(torch.__file__).resolve().parent / "lib"
    cublas = library_root / "cublas64_12.dll"
    cublas_lt = library_root / "cublasLt64_12.dll"
    if not cublas.is_file() or not cublas_lt.is_file():
        raise ProtocolError("pinned cuBLAS libraries are missing")
    return {
        "cublas_path": str(cublas),
        "cublas_sha256": file_sha256(cublas),
        "cublas_version": _windows_file_version(cublas),
        "cublas_lt_path": str(cublas_lt),
        "cublas_lt_sha256": file_sha256(cublas_lt),
        "cublas_lt_version": _windows_file_version(cublas_lt),
        "torch_config": torch.__config__.show(),
    }


def cuda_preflight() -> dict[str, object]:
    """Return live CUDA identity without creating scientific job artifacts."""
    import torch

    if not torch.cuda.is_available() or torch.cuda.device_count() < 1:
        raise ProtocolError("requested CUDA device is unavailable")
    capability = torch.cuda.get_device_capability(0)
    runtime_result = torch.cuda.cudart().cudaRuntimeGetVersion()
    if isinstance(runtime_result, tuple):
        runtime_error, runtime_version = runtime_result
        if runtime_error != 0:
            raise ProtocolError("CUDA runtime version query failed")
    else:
        runtime_version = runtime_result
    libraries = _cuda_library_records(torch)
    return {
        "schema_version": PREFLIGHT_SCHEMA,
        "torch_version": torch.__version__,
        "torch_cuda_build_runtime": torch.version.cuda,
        "cuda_available": True,
        "device_count": torch.cuda.device_count(),
        "device_name": torch.cuda.get_device_name(0),
        "compute_capability": list(capability),
        "driver_version": _driver_version(),
        "cuda_runtime_version": int(runtime_version),
        "cudnn_version": torch.backends.cudnn.version(),
        "cublas_library_version": libraries["cublas_version"],
        "cublas_lt_library_version": libraries["cublas_lt_version"],
        "library_records": libraries,
    }


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def dtype_name(array: np.ndarray) -> str:
    if array.dtype == np.dtype(np.float64):
        return "float64"
    if array.dtype == np.dtype(np.float32):
        return "float32"
    if array.dtype == np.dtype(np.int64):
        return "int64"
    if array.dtype == np.dtype(np.bool_):
        return "bool"
    raise ProtocolError(f"unsupported array dtype: {array.dtype}")


def canonical_array_sha256(name: str, array: np.ndarray, dtype: str) -> str:
    if JOB_ID.fullmatch(name) is None:
        raise ProtocolError("invalid array name")
    canonical_dtype = NUMPY_DTYPES.get(dtype)
    if canonical_dtype is None:
        raise ProtocolError(f"unsupported worker dtype: {dtype}")
    canonical = np.ascontiguousarray(array.astype(canonical_dtype, copy=False))
    shape_json = json.dumps(list(canonical.shape), separators=(",", ":"))
    preimage = (
        b"cuda-worker-array-v1\0"
        + name.encode("utf-8")
        + b"\0"
        + dtype.encode("ascii")
        + b"\0"
        + shape_json.encode("utf-8")
        + b"\0"
        + canonical.tobytes(order="C")
    )
    return hashlib.sha256(preimage).hexdigest()


def validate_request(manifest: object) -> dict[str, object]:
    if not isinstance(manifest, dict) or set(manifest) != KEYS:
        raise ProtocolError("request manifest keys do not match protocol")
    if manifest["schema_version"] != PROTOCOL or manifest["message_type"] != "request":
        raise ProtocolError("invalid request schema or message type")
    if type(manifest["job_id"]) is not str or JOB_ID.fullmatch(manifest["job_id"]) is None:
        raise ProtocolError("invalid job ID")
    if manifest["requested_backend"] not in {"cpu", "cuda"}:
        raise ProtocolError("invalid requested backend")
    if manifest["requested_dtype"] not in {"float64", "float32", "bfloat16"}:
        raise ProtocolError("invalid requested dtype")
    if manifest["effective_backend"] is not None or manifest["effective_dtype"] is not None:
        raise ProtocolError("request effective fields must be null")
    if manifest["output_identity"] is not None:
        raise ProtocolError("request output identity must be null")
    if type(manifest["environment_sha256"]) is not str or SHA256.fullmatch(manifest["environment_sha256"]) is None:
        raise ProtocolError("invalid environment digest")
    if type(manifest["npz_sha256"]) is not str or SHA256.fullmatch(manifest["npz_sha256"]) is None:
        raise ProtocolError("invalid NPZ digest")
    descriptors = manifest["arrays"]
    if not isinstance(descriptors, list) or not descriptors:
        raise ProtocolError("request array descriptors must be a nonempty list")
    names: set[str] = set()
    for descriptor in descriptors:
        if not isinstance(descriptor, dict) or set(descriptor) != ARRAY_KEYS:
            raise ProtocolError("array descriptor keys do not match protocol")
        name = descriptor["name"]
        if type(name) is not str or JOB_ID.fullmatch(name) is None or name in names:
            raise ProtocolError("invalid or duplicate array name")
        names.add(name)
        shape = descriptor["shape"]
        if type(shape) is not list or any(type(size) is not int or size < 0 for size in shape):
            raise ProtocolError("invalid array shape")
        if descriptor["dtype"] not in {"float64", "float32", "int64", "bool"}:
            raise ProtocolError("invalid array dtype")
        if type(descriptor["sha256"]) is not str or SHA256.fullmatch(descriptor["sha256"]) is None:
            raise ProtocolError("invalid array digest")
    return manifest


def load_and_validate_inputs(
    request: Mapping[str, object], input_npz: Path
) -> dict[str, np.ndarray]:
    if file_sha256(input_npz) != request["npz_sha256"]:
        raise ProtocolError("input NPZ digest mismatch")
    descriptors = {descriptor["name"]: descriptor for descriptor in request["arrays"]}  # type: ignore[index]
    with np.load(input_npz, allow_pickle=False) as archive:
        if set(archive.files) != set(descriptors):
            raise ProtocolError("input NPZ array inventory mismatch")
        arrays = {name: np.array(archive[name], copy=True) for name in archive.files}
    for name, descriptor in descriptors.items():
        array = arrays[name]
        if list(array.shape) != descriptor["shape"]:
            raise ProtocolError(f"input shape mismatch: {name}")
        actual_dtype = dtype_name(array)
        if actual_dtype != descriptor["dtype"]:
            raise ProtocolError(f"input dtype mismatch: {name}")
        if canonical_array_sha256(name, array, actual_dtype) != descriptor["sha256"]:
            raise ProtocolError(f"input array digest mismatch: {name}")
    if set(arrays) != {"coefficients", "spatial_map", "matrix_direction", "batch_size"}:
        raise ProtocolError("fixed-ray input inventory mismatch")
    coefficients = arrays["coefficients"]
    spatial_map = arrays["spatial_map"]
    matrix_direction = arrays["matrix_direction"]
    batch_size = arrays["batch_size"]
    if coefficients.ndim != 2 or spatial_map.ndim != 2 or spatial_map.shape[0] != spatial_map.shape[1]:
        raise ProtocolError("invalid coefficient or spatial-map shape")
    if coefficients.shape[1] != spatial_map.shape[0]:
        raise ProtocolError("coefficient width does not match spatial map")
    if matrix_direction.ndim != 2 or matrix_direction.shape[0] != matrix_direction.shape[1]:
        raise ProtocolError("matrix direction must be square")
    if batch_size.shape != () or batch_size.dtype != np.dtype(np.int64) or int(batch_size) <= 0:
        raise ProtocolError("batch size must be one positive int64 scalar")
    if not all(np.all(np.isfinite(array)) for array in (coefficients, spatial_map, matrix_direction)):
        raise ProtocolError("worker scientific arrays must be finite")
    if np.any(coefficients < 0.0) or np.any(spatial_map < 0.0):
        raise ProtocolError(
            "coefficients and spatial_map must have nonnegative support"
        )
    normalization_atol = (
        1.0e-12 if request["requested_dtype"] == "float64" else 1.0e-6
    )
    if not np.allclose(
        np.sum(spatial_map, axis=1),
        1.0,
        rtol=0.0,
        atol=normalization_atol,
    ):
        raise ProtocolError("spatial_map must be row-stochastic")
    if not np.array_equal(matrix_direction, matrix_direction.T):
        raise ProtocolError("matrix direction must be symmetric")
    if np.min(np.linalg.eigvalsh(matrix_direction.astype(np.float64))) <= 0.0:
        raise ProtocolError("matrix direction must be positive definite")
    requested_numpy_dtype = np.dtype(
        np.float64 if request["requested_dtype"] == "float64" else np.float32
    )
    if request["requested_dtype"] == "bfloat16":
        raise ProtocolError("bfloat16 exploratory payload encoding is not available")
    if any(array.dtype != requested_numpy_dtype for array in (coefficients, spatial_map, matrix_direction)):
        raise ProtocolError("scientific array dtype differs from requested dtype")
    return arrays


def _validate_on_device_probability_payload(
    coefficients: object, spatial_map: object
) -> None:
    """Validate Torch probability tensors without moving them off their device."""
    if not bool(coefficients.isfinite().all().item()) or not bool(
        spatial_map.isfinite().all().item()
    ):
        raise ProtocolError("on-device scientific arrays must be finite")
    if bool((coefficients < 0.0).any().item()) or bool(
        (spatial_map < 0.0).any().item()
    ):
        raise ProtocolError(
            "on-device coefficients and spatial_map must have nonnegative support"
        )
    normalization_atol = 1.0e-12 if coefficients.element_size() == 8 else 1.0e-6
    row_error = (spatial_map.sum(dim=1) - 1.0).abs()
    if bool((row_error > normalization_atol).any().item()):
        raise ProtocolError("on-device spatial_map must be row-stochastic")


def _validate_on_device_probability_output(updated: object) -> None:
    """Reject nonfinite or support-invalid Torch output before host transfer."""
    if not bool(updated.isfinite().all().item()) or bool(
        (updated < 0.0).any().item()
    ):
        raise ProtocolError("on-device updated coefficients must be finite nonnegative")


def _validate_probability_output(outputs: Mapping[str, np.ndarray]) -> None:
    updated = outputs["updated_coefficients"]
    condition = outputs["matrix_condition"]
    if not np.all(np.isfinite(updated)) or np.any(updated < 0.0):
        raise ProtocolError("updated coefficients must be finite nonnegative")
    if not np.all(np.isfinite(condition)) or float(condition) < 1.0:
        raise ProtocolError("matrix condition must be finite and at least one")


def compute_cpu(arrays: Mapping[str, np.ndarray]) -> tuple[dict[str, np.ndarray], dict[str, object]]:
    coefficients = arrays["coefficients"]
    spatial_map = arrays["spatial_map"]
    batch_size = int(arrays["batch_size"])
    output = np.empty((coefficients.shape[0], spatial_map.shape[0]), dtype=coefficients.dtype)
    for start in range(0, coefficients.shape[0], batch_size):
        stop = min(start + batch_size, coefficients.shape[0])
        for row in range(start, stop):
            output[row] = coefficients[row] @ spatial_map.T
    condition = np.array(
        np.linalg.cond(arrays["matrix_direction"].astype(np.float64)),
        dtype=np.float64,
    )
    return (
        {"matrix_condition": condition, "updated_coefficients": output},
        {
            "torch_version": None,
            "torch_cuda_build_runtime": None,
            "cuda_available": False,
            "driver_version": None,
            "cuda_runtime_version": None,
            "cublas_library_version": None,
            "device_name": None,
            "compute_capability": None,
            "deterministic_algorithms": None,
            "deterministic_warn_only": None,
            "matmul_allow_tf32": None,
            "cudnn_allow_tf32": None,
            "cudnn_version": None,
            "library_records": {
                "cublas_path": None,
                "cublas_sha256": None,
                "cublas_version": None,
                "cublas_lt_path": None,
                "cublas_lt_sha256": None,
                "cublas_lt_version": None,
                "torch_config": None,
            },
            "kernel_strategy": "rowwise_spatial_map_matvec",
            "peak_allocated_bytes": 0,
            "peak_reserved_bytes": 0,
        },
    )


def compute_cuda(
    arrays: Mapping[str, np.ndarray], requested_dtype: str
) -> tuple[dict[str, np.ndarray], dict[str, object]]:
    import torch

    torch.use_deterministic_algorithms(True, warn_only=False)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    if os.environ.get("CUBLAS_WORKSPACE_CONFIG") != ":4096:8":
        raise ProtocolError("CUBLAS_WORKSPACE_CONFIG must be :4096:8")
    if not torch.cuda.is_available() or torch.cuda.device_count() < 1:
        raise ProtocolError("requested CUDA device is unavailable")
    device = torch.device("cuda:0")
    torch_dtype = {"float64": torch.float64, "float32": torch.float32}[requested_dtype]
    torch.cuda.reset_peak_memory_stats(device)
    coefficients = torch.as_tensor(arrays["coefficients"], dtype=torch_dtype, device=device)
    spatial_map = torch.as_tensor(arrays["spatial_map"], dtype=torch_dtype, device=device)
    _validate_on_device_probability_payload(coefficients, spatial_map)
    batch_size = int(arrays["batch_size"])
    pieces = []
    for start in range(0, coefficients.shape[0], batch_size):
        stop = min(start + batch_size, coefficients.shape[0])
        pieces.append(coefficients[start:stop] @ spatial_map.T)
    if pieces:
        updated = torch.cat(pieces, dim=0)
    else:
        updated = torch.empty(
            (0, spatial_map.shape[0]), dtype=torch_dtype, device=device
        )
    _validate_on_device_probability_output(updated)
    torch.cuda.synchronize(device)
    output = updated.cpu().numpy()
    condition = np.array(
        np.linalg.cond(arrays["matrix_direction"].astype(np.float64)),
        dtype=np.float64,
    )
    capability = torch.cuda.get_device_capability(0)
    runtime_result = torch.cuda.cudart().cudaRuntimeGetVersion()
    if isinstance(runtime_result, tuple):
        runtime_error, runtime_version = runtime_result
        if runtime_error != 0:
            raise ProtocolError("CUDA runtime version query failed")
    else:
        runtime_version = runtime_result
    libraries = _cuda_library_records(torch)
    provenance = {
        "torch_version": torch.__version__,
        "torch_cuda_build_runtime": torch.version.cuda,
        "cuda_available": True,
        "driver_version": _driver_version(),
        "cuda_runtime_version": int(runtime_version),
        "cublas_library_version": libraries["cublas_version"],
        "device_name": torch.cuda.get_device_name(0),
        "compute_capability": list(capability),
        "deterministic_algorithms": torch.are_deterministic_algorithms_enabled(),
        "deterministic_warn_only": torch.is_deterministic_algorithms_warn_only_enabled(),
        "matmul_allow_tf32": torch.backends.cuda.matmul.allow_tf32,
        "cudnn_allow_tf32": torch.backends.cudnn.allow_tf32,
        "cudnn_version": torch.backends.cudnn.version(),
        "library_records": libraries,
        "kernel_strategy": "batched_spatial_map_matmul",
        "peak_allocated_bytes": int(torch.cuda.max_memory_allocated(device)),
        "peak_reserved_bytes": int(torch.cuda.max_memory_reserved(device)),
    }
    outputs = {"matrix_condition": condition, "updated_coefficients": output}
    _validate_probability_output(outputs)
    return outputs, provenance


def descriptors(arrays: Mapping[str, np.ndarray]) -> list[dict[str, object]]:
    return [
        {
            "name": name,
            "shape": list(arrays[name].shape),
            "dtype": dtype_name(arrays[name]),
            "sha256": canonical_array_sha256(name, arrays[name], dtype_name(arrays[name])),
        }
        for name in sorted(arrays)
    ]


def output_identity(request: Mapping[str, object], response: Mapping[str, object]) -> str:
    request_payload = dict(request)
    request_payload["output_identity"] = None
    response_payload = dict(response)
    response_payload["output_identity"] = None
    canonical = json.dumps(
        {"request": request_payload, "response": response_payload},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def atomic_npz(path: Path, arrays: Mapping[str, np.ndarray]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("wb") as handle:
        np.savez(handle, **arrays)
    os.replace(temporary, path)


def atomic_json(path: Path, payload: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False),
        encoding="utf-8",
    )
    os.replace(temporary, path)


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--preflight-cuda":
        sys.stdout.write(
            json.dumps(
                cuda_preflight(),
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            )
        )
        return 0
    if len(sys.argv) != 5:
        raise ProtocolError("worker requires request JSON, input NPZ, response JSON, and output NPZ")
    request_path, input_path, response_path, output_path = map(Path, sys.argv[1:])
    if response_path.exists() or output_path.exists():
        raise ProtocolError("worker output paths must not exist")
    request = validate_request(json.loads(request_path.read_text(encoding="utf-8")))
    arrays = load_and_validate_inputs(request, input_path)
    started = time.perf_counter()
    if request["requested_backend"] == "cpu":
        outputs, backend_provenance = compute_cpu(arrays)
    else:
        outputs, backend_provenance = compute_cuda(
            arrays, str(request["requested_dtype"])
        )
    _validate_probability_output(outputs)
    atomic_npz(output_path, outputs)
    response: dict[str, object] = {
        "schema_version": PROTOCOL,
        "message_type": "response",
        "job_id": request["job_id"],
        "requested_backend": request["requested_backend"],
        "requested_dtype": request["requested_dtype"],
        "effective_backend": request["requested_backend"],
        "effective_dtype": request["requested_dtype"],
        "environment_sha256": request["environment_sha256"],
        "npz_sha256": file_sha256(output_path),
        "arrays": descriptors(outputs),
        "output_identity": None,
    }
    response["output_identity"] = output_identity(request, response)
    atomic_json(response_path, response)
    provenance = {
        "schema_version": PROVENANCE_SCHEMA,
        "python_executable": str(Path(sys.executable).resolve()),
        "worker_executable": str(Path(sys.executable).resolve()),
        "worker_executable_sha256": file_sha256(Path(sys.executable).resolve()),
        "worker_script_sha256": file_sha256(Path(__file__).resolve()),
        "python_version": sys.version,
        "numpy_version": np.__version__,
        "platform": platform.platform(),
        "requested_backend": request["requested_backend"],
        "effective_backend": request["requested_backend"],
        "requested_dtype": request["requested_dtype"],
        "effective_dtype": request["requested_dtype"],
        "environment_sha256": request["environment_sha256"],
        "environment_lock_consistent": os.environ.get("CUBLAS_WORKSPACE_CONFIG")
        == ":4096:8",
        "cublas_workspace_config": os.environ.get("CUBLAS_WORKSPACE_CONFIG"),
        "batch_size": int(arrays["batch_size"]),
        "runtime_seconds": time.perf_counter() - started,
        "retry_lineage": {"attempt": 1, "parent_job_id": None},
        **backend_provenance,
    }
    sys.stdout.write(
        json.dumps(provenance, sort_keys=True, separators=(",", ":"), allow_nan=False)
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        sys.stderr.write(f"{type(error).__name__}: {error}\n")
        raise SystemExit(2) from error
