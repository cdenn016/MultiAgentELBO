"""Artifact-backed non-heavy pilot for the preregistered Gaussian fixed ray."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from types import MappingProxyType
from typing import Literal, Mapping

import numpy as np

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import ExperimentConfig, config_sha256
from multiagent_elbo.cuda_backend import (
    WorkerJobResult,
    _parse_environment_lock,
    _run_cuda_preflight,
    parity_diagnostics,
    run_worker_job,
    validate_worker_provenance,
    validate_worker_result,
)
from multiagent_elbo.experiment_support import (
    MetricRecord,
    target_metric,
    validate_worker_protocol_manifest,
)
from multiagent_elbo.runtime import RngStreams, collect_provenance

from .fixed_ray import (
    blocking_scheme_dispersion,
    build_preregistered_system,
    generate_initial_coefficients,
    iterate_fixed_ray,
    job_seed,
    projective_ray_angle,
    scalarized_ray_construction_residual,
)
from .confirmatory_analysis import analyze_holdout, analyze_primary


MetricStatus = Literal["pass", "fail", "inconclusive"]
_PREREGISTRATION_SHA256 = (
    "57be7aa49af8c9fa56585879fa394ca93517cc1b58269596e53293d350a07dd5"
)


@dataclass(frozen=True)
class GaussianFixedRayExperimentResult:
    run_dir: Path
    config_hash: str
    status: MetricStatus
    metrics: Mapping[str, MetricRecord]
    arrays: Mapping[str, np.ndarray]


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical_text_sha256(path: Path) -> str:
    """Hash text with Git's LF representation as the canonical form."""
    raw = path.read_bytes()
    canonical = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(canonical).hexdigest()


def _readonly(values: object, *, dtype: object = np.float64) -> np.ndarray:
    array = np.array(values, dtype=dtype, copy=True, order="C")
    array.setflags(write=False)
    return array


def _run_nvidia_smi(arguments: list[str]) -> list[str]:
    completed = subprocess.run(
        ["nvidia-smi", *arguments],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"GPU occupancy query failed with exit {completed.returncode}: "
            f"{completed.stderr.strip()}"
        )
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def capture_idle_gpu_gate(
    *,
    operator_opt_in: bool,
    sample_count: int = 5,
    sample_interval_seconds: float = 1.0,
    freshness_ttl_seconds: float = 300.0,
) -> dict[str, object]:
    """Capture an operator-attested idle-residency observation without killing processes."""
    if operator_opt_in is not True:
        raise ValueError("CUDA execution requires explicit operator opt-in")
    if type(sample_count) is not int or sample_count <= 0:
        raise ValueError("sample_count must be a positive integer")
    if not np.isfinite(sample_interval_seconds) or sample_interval_seconds < 0.0:
        raise ValueError("sample interval must be finite and nonnegative")
    if not np.isfinite(freshness_ttl_seconds) or freshness_ttl_seconds <= 0.0:
        raise ValueError("freshness TTL must be finite and positive")

    samples: list[dict[str, object]] = []
    raw_gpu_rows: list[str] = []
    query = [
        "--query-gpu=index,name,uuid,driver_version,pstate,utilization.gpu,"
        "memory.used,memory.total,temperature.gpu",
        "--format=csv,noheader,nounits",
    ]
    for sample_index in range(sample_count):
        rows = _run_nvidia_smi(query)
        if len(rows) != 1:
            raise RuntimeError("idle gate requires exactly one visible GPU")
        raw_gpu_rows.append(rows[0])
        fields = [field.strip() for field in rows[0].split(",")]
        if len(fields) != 9:
            raise RuntimeError("GPU occupancy row does not match the frozen schema")
        samples.append(
            {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "index": int(fields[0]),
                "name": fields[1],
                "uuid": fields[2],
                "driver_version": fields[3],
                "pstate": fields[4],
                "utilization_gpu_percent": int(fields[5]),
                "memory_used_mib": int(fields[6]),
                "memory_total_mib": int(fields[7]),
                "temperature_c": int(fields[8]),
            }
        )
        if sample_index + 1 < sample_count and sample_interval_seconds:
            time.sleep(sample_interval_seconds)

    raw_process_rows = _run_nvidia_smi(
        [
            "--query-compute-apps=gpu_uuid,pid,process_name,used_gpu_memory",
            "--format=csv,noheader,nounits",
        ]
    )
    processes: list[dict[str, object]] = []
    for row in raw_process_rows:
        fields = [field.strip() for field in row.split(",", 3)]
        if len(fields) != 4:
            raise RuntimeError("GPU process row does not match the frozen schema")
        used_memory = None if fields[3].startswith("[") else int(fields[3])
        processes.append(
            {
                "gpu_uuid": fields[0],
                "pid": int(fields[1]),
                "process_name": fields[2],
                "used_gpu_memory_mib": used_memory,
            }
        )

    memory_values = [int(sample["memory_used_mib"]) for sample in samples]
    idle = (
        all(sample["utilization_gpu_percent"] == 0 for sample in samples)
        and all(sample["pstate"] == "P8" for sample in samples)
        and max(memory_values) - min(memory_values) <= 64
    )
    if not idle:
        raise RuntimeError("GPU is not idle across the required occupancy samples")
    captured_at = datetime.now(timezone.utc)
    return {
        "schema_version": "cuda-idle-operator-gate-v1",
        "captured_at_utc": captured_at.isoformat(),
        "expires_at_utc": (
            captured_at + timedelta(seconds=float(freshness_ttl_seconds))
        ).isoformat(),
        "operator_opt_in": True,
        "operator_process_acceptance_pending": True,
        "idle_observation_passed": True,
        "idle_observation_scope": (
            "Observed residency only; listed processes may resume after sampling."
        ),
        "sample_count": sample_count,
        "sample_interval_seconds": float(sample_interval_seconds),
        "sample_window_seconds": float(sample_interval_seconds * (sample_count - 1)),
        "freshness_ttl_seconds": float(freshness_ttl_seconds),
        "memory_stability_tolerance_mib": 64,
        "processes_present": bool(processes),
        "samples": samples,
        "active_compute_processes": processes,
        "raw_gpu_rows": raw_gpu_rows,
        "raw_process_rows": raw_process_rows,
    }


def _capture_idle_gpu_gate_after_cooldown(
    *, operator_opt_in: bool
) -> dict[str, object]:
    """Wait briefly for this sentinel's prior CUDA work to return to P8."""
    maximum_attempts = 31
    poll_seconds = 1.0
    idle_error = "GPU is not idle across the required occupancy samples"
    for attempt in range(1, maximum_attempts + 1):
        try:
            gate = capture_idle_gpu_gate(
                operator_opt_in=operator_opt_in,
                sample_count=1,
                sample_interval_seconds=0.0,
                freshness_ttl_seconds=300.0,
            )
        except RuntimeError as error:
            if str(error) != idle_error or attempt == maximum_attempts:
                raise
            time.sleep(poll_seconds)
            continue
        gate["idle_wait_attempts"] = attempt
        gate["idle_wait_seconds"] = float((attempt - 1) * poll_seconds)
        return gate
    raise AssertionError("unreachable CUDA idle-wait state")


def _live_cuda_common_bindings(config: ExperimentConfig) -> dict[str, object]:
    if config.compute.backend != "cuda" or config.compute.dtype != "float64":
        raise ValueError("CUDA gate requires a CUDA float64 configuration")
    repo_root = Path(__file__).resolve().parents[4]
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    tracked_status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if (
        revision.returncode != 0
        or tracked_status.returncode != 0
        or tracked_status.stdout.strip()
    ):
        raise RuntimeError("CUDA gate requires an exact clean Git revision")
    preregistration = (
        repo_root
        / "docs"
        / "experiments"
        / "2026-08-09-gaussian-fixed-ray-preregistration.md"
    )
    preregistration_sha256 = _validate_preregistration(preregistration)
    environment_lock = repo_root / "environments" / "cuda-rtx5090-cu128.lock.txt"
    worker_script = repo_root / "tools" / "cuda_worker.py"
    worker_python = config.compute.cuda_worker_python.resolve(strict=True)
    environment = dict(os.environ)
    lock_records = _parse_environment_lock(environment_lock)
    environment["CUBLAS_WORKSPACE_CONFIG"] = lock_records[
        "required_CUBLAS_WORKSPACE_CONFIG"
    ]
    preflight = _run_cuda_preflight(
        worker_python=worker_python,
        worker_script=worker_script,
        environment=environment,
        lock_records=lock_records,
        timeout_seconds=120.0,
    )
    return {
        "source_identity": {
            "git_revision": revision.stdout.strip(),
            "tracked_worktree_clean": True,
        },
        "config_sha256": config_sha256(config),
        "preregistration_sha256": preregistration_sha256,
        "environment_lock_identity": {
            "path": str(environment_lock),
            "sha256": _file_sha256(environment_lock),
        },
        "worker_python_identity": {
            "path": str(worker_python),
            "sha256": _file_sha256(worker_python),
        },
        "worker_script_identity": {
            "path": str(worker_script),
            "sha256": _file_sha256(worker_script),
        },
        "preflight": dict(preflight),
    }


def _live_cuda_gate_bindings(config: ExperimentConfig) -> dict[str, object]:
    if config.compute.heavy_sweep_enabled:
        raise ValueError("CUDA gate precedes heavy-sweep enablement")
    return _live_cuda_common_bindings(config)


def _validate_cuda_gate_bindings(
    config: ExperimentConfig, gate: Mapping[str, object]
) -> None:
    live = _live_cuda_gate_bindings(config)
    if any(gate.get(key) != value for key, value in live.items()):
        raise ValueError("accepted CUDA gate identity drifted from the live execution")


def build_cuda_gate_record(
    config: ExperimentConfig, *, operator_opt_in: bool
) -> dict[str, object]:
    """Bind a fresh occupancy gate to the exact clean source and CUDA preflight."""
    bindings = _live_cuda_gate_bindings(config)
    gate = capture_idle_gpu_gate(operator_opt_in=operator_opt_in)
    gate.update(bindings)
    gate["decision"] = "PENDING_OPERATOR_PROCESS_ACCEPTANCE"
    return gate


def build_confirmatory_gate_record(
    config: ExperimentConfig, *, operator_opt_in: bool
) -> dict[str, object]:
    """Bind a fresh idle observation to the heavy confirmatory configuration."""
    if config.compute.heavy_sweep_enabled is not True:
        raise ValueError("confirmatory gate requires heavy_sweep_enabled=True")
    bindings = _live_cuda_common_bindings(config)
    gate = capture_idle_gpu_gate(
        operator_opt_in=operator_opt_in,
        sample_count=5,
        sample_interval_seconds=1.0,
        freshness_ttl_seconds=21_600.0,
    )
    gate.update(bindings)
    gate["schema_version"] = "cuda-confirmatory-operator-gate-v1"
    gate["execution_scope"] = "gaussian_fixed_ray_confirmatory_40_job"
    gate["heavy_sweep_enabled"] = True
    gate["decision"] = "PENDING_OPERATOR_PROCESS_ACCEPTANCE"
    return gate


def _validate_confirmatory_gate_bindings(
    config: ExperimentConfig, gate: Mapping[str, object]
) -> None:
    if (
        config.compute.heavy_sweep_enabled is not True
        or gate.get("schema_version") != "cuda-confirmatory-operator-gate-v1"
        or gate.get("execution_scope") != "gaussian_fixed_ray_confirmatory_40_job"
        or gate.get("heavy_sweep_enabled") is not True
    ):
        raise ValueError("accepted confirmatory gate scope is invalid")
    live = _live_cuda_common_bindings(config)
    if any(gate.get(key) != value for key, value in live.items()):
        raise ValueError("accepted confirmatory gate identity drifted from live execution")


def _validate_gate_recheck(
    initial_gate: Mapping[str, object], current_gate: Mapping[str, object]
) -> None:
    initial_samples = initial_gate["samples"]
    current_samples = current_gate["samples"]
    initial_last = initial_samples[-1]  # type: ignore[index]
    current_first = current_samples[0]  # type: ignore[index]
    if initial_last["uuid"] != current_first["uuid"]:  # type: ignore[index]
        raise RuntimeError("GPU identity changed after operator attestation")
    memory_drift = abs(
        int(current_first["memory_used_mib"])  # type: ignore[index]
        - int(initial_last["memory_used_mib"])  # type: ignore[index]
    )
    if memory_drift > 256:
        raise RuntimeError("GPU residency changed materially after operator attestation")

    def process_signature(gate: Mapping[str, object]) -> set[tuple[object, ...]]:
        return {
            (
                process["gpu_uuid"],
                process["pid"],
                process["process_name"],
                process["used_gpu_memory_mib"],
            )
            for process in gate["active_compute_processes"]  # type: ignore[union-attr]
        }

    if process_signature(initial_gate) != process_signature(current_gate):
        raise RuntimeError("GPU compute-process set changed after operator attestation")


def _atomic_json(path: Path, payload: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False),
        encoding="utf-8",
    )
    temporary.replace(path)


def _record_sha256(payload: object) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _validate_execution_context(
    context: Mapping[str, object], *, persisted: bool
) -> None:
    required = {
        "accepted_gate_sha256",
        "accepted_gate_record",
        "operator_gate_recheck_sha256",
        "operator_gate_recheck_record",
        "sentinel_job_id",
        "scheme",
        "step",
        "lane",
        "config_sha256",
        "source_revision",
    }
    if persisted:
        required |= {"outer_attempt", "parent_attempt"}
    if set(context) != required:
        raise RuntimeError("worker execution context schema drifted")
    if (
        _record_sha256(context["accepted_gate_record"])
        != context["accepted_gate_sha256"]
        or _record_sha256(context["operator_gate_recheck_record"])
        != context["operator_gate_recheck_sha256"]
    ):
        raise RuntimeError("worker execution context gate digest drifted")
    accepted_gate = context["accepted_gate_record"]
    if not isinstance(accepted_gate, Mapping) or (
        accepted_gate.get("config_sha256") != context["config_sha256"]
        or not isinstance(accepted_gate.get("source_identity"), Mapping)
        or accepted_gate["source_identity"].get("git_revision")
        != context["source_revision"]
    ):
        raise RuntimeError("worker execution context identity binding drifted")
    if persisted and (
        context["outer_attempt"] not in {1, 2}
        or context["parent_attempt"]
        != (None if context["outer_attempt"] == 1 else 1)
    ):
        raise RuntimeError("worker execution context retry lineage drifted")


def _validate_execution_context_compatibility(
    stored: Mapping[str, object], current: Mapping[str, object]
) -> None:
    scientific_fields = {
        "sentinel_job_id",
        "scheme",
        "step",
        "lane",
        "config_sha256",
        "source_revision",
    }
    if any(stored[field] != current[field] for field in scientific_fields):
        raise RuntimeError("worker execution context scientific identity drifted")
    binding_fields = {
        "source_identity",
        "config_sha256",
        "preregistration_sha256",
        "environment_lock_identity",
        "worker_python_identity",
        "worker_script_identity",
        "preflight",
    }
    stored_gate = stored["accepted_gate_record"]
    current_gate = current["accepted_gate_record"]
    if not isinstance(stored_gate, Mapping) or not isinstance(current_gate, Mapping):
        raise RuntimeError("worker execution context accepted gate is invalid")
    if any(stored_gate.get(field) != current_gate.get(field) for field in binding_fields):
        raise RuntimeError("worker execution context accepted gate binding drifted")


def _run_or_resume_worker_job(
    *,
    worker_python: Path,
    worker_script: Path,
    work_root: Path,
    job_id: str,
    requested_backend: Literal["cpu", "cuda"],
    requested_dtype: Literal["float64"],
    arrays: Mapping[str, np.ndarray],
    environment_lock: Path,
    execution_context: Mapping[str, object],
) -> tuple[WorkerJobResult, Mapping[str, object]]:
    """Resume a valid attempt or make one infrastructure retry with bound context."""
    exchange_root = Path(work_root)
    exchange_root.mkdir(parents=True, exist_ok=True)
    expected_names = {
        "input.npz",
        "request.json",
        "response.json",
        "output.npz",
        "provenance.json",
    }
    _validate_execution_context(execution_context, persisted=False)

    def load_attempt(
        attempt_root: Path, context_path: Path
    ) -> tuple[WorkerJobResult, Mapping[str, object]]:
        if {path.name for path in attempt_root.iterdir()} != expected_names:
            raise RuntimeError(f"incomplete immutable worker exchange: {job_id}")
        request_path = attempt_root / "request.json"
        response_path = attempt_root / "response.json"
        input_path = attempt_root / "input.npz"
        output_path = attempt_root / "output.npz"
        request = json.loads(request_path.read_text(encoding="utf-8"))
        response = json.loads(response_path.read_text(encoding="utf-8"))
        provenance = json.loads(
            (attempt_root / "provenance.json").read_text(encoding="utf-8")
        )
        stored_context = json.loads(context_path.read_text(encoding="utf-8"))
        _validate_execution_context(stored_context, persisted=True)
        _validate_execution_context_compatibility(stored_context, execution_context)
        validate_worker_protocol_manifest(request, expected_message_type="request")
        if (
            request["job_id"] != job_id
            or request["requested_backend"] != requested_backend
            or request["requested_dtype"] != requested_dtype
            or request["npz_sha256"] != _file_sha256(input_path)
            or request["environment_sha256"] != _file_sha256(environment_lock)
        ):
            raise RuntimeError(f"immutable worker request drifted: {job_id}")
        with np.load(input_path, allow_pickle=False) as archive:
            if set(archive.files) != set(arrays) or any(
                not np.array_equal(archive[name], np.asarray(arrays[name]))
                for name in archive.files
            ):
                raise RuntimeError(f"immutable worker inputs drifted: {job_id}")
        arrays_out = validate_worker_result(
            request_manifest=request,
            response_manifest=response,
            output_npz=output_path,
        )
        validate_worker_provenance(
            provenance,
            requested_backend=requested_backend,
            requested_dtype=requested_dtype,
            environment_sha256=_file_sha256(environment_lock),
            batch_size=int(np.asarray(arrays["batch_size"])),
        )
        resolved_python = Path(worker_python).resolve(strict=True)
        resolved_script = Path(worker_script).resolve(strict=True)
        if (
            Path(str(provenance["python_executable"])).resolve() != resolved_python
            or Path(str(provenance["worker_executable"])).resolve() != resolved_python
            or provenance["worker_executable_sha256"] != _file_sha256(resolved_python)
            or provenance["worker_script_sha256"] != _file_sha256(resolved_script)
        ):
            raise RuntimeError(f"immutable worker provenance drifted: {job_id}")
        return (
            WorkerJobResult(
                request_manifest=MappingProxyType(request),
                response_manifest=MappingProxyType(response),
                arrays=arrays_out,
                provenance=MappingProxyType(provenance),
                request_json=request_path,
                input_npz=input_path,
                response_json=response_path,
                output_npz=output_path,
            ),
            MappingProxyType(stored_context),
        )

    for attempt in (2, 1):
        attempt_root = exchange_root / f"attempt-{attempt}"
        context_path = exchange_root / f"attempt-{attempt}-context.json"
        if attempt_root.is_dir() and context_path.is_file():
            if {path.name for path in attempt_root.iterdir()} == expected_names:
                return load_attempt(attempt_root, context_path)

    attempt_1_started = (exchange_root / "attempt-1").exists() or (
        exchange_root / "attempt-1-context.json"
    ).exists()
    attempt = 2 if attempt_1_started else 1
    attempt_root = exchange_root / f"attempt-{attempt}"
    context_path = exchange_root / f"attempt-{attempt}-context.json"
    if attempt_root.exists() or context_path.exists():
        raise RuntimeError(f"worker exchange exhausted one infrastructure retry: {job_id}")
    context = dict(execution_context)
    context["outer_attempt"] = attempt
    context["parent_attempt"] = None if attempt == 1 else 1
    _validate_execution_context(context, persisted=True)
    _atomic_json(context_path, context)
    result = run_worker_job(
        worker_python=worker_python,
        worker_script=worker_script,
        work_root=attempt_root,
        job_id=job_id,
        requested_backend=requested_backend,
        requested_dtype=requested_dtype,
        arrays=arrays,
        environment_lock=environment_lock,
    )
    _atomic_json(attempt_root / "provenance.json", dict(result.provenance))
    return result, MappingProxyType(context)


def _confirmatory_scheme_record(
    coefficients: np.ndarray, *, system: object
) -> dict[str, object]:
    ray = system.perron_ray
    normalized_ray = ray / np.linalg.norm(ray)
    angles = np.array(
        [projective_ray_angle(row, ray) for row in coefficients], dtype=np.float64
    )
    distances = np.array(
        [
            np.linalg.norm(row / np.linalg.norm(row) - normalized_ray)
            for row in coefficients
        ],
        dtype=np.float64,
    )
    projection = np.outer(ray, ray) / float(np.dot(ray, ray))
    beta_vectors = np.array(
        [
            (np.eye(ray.size) - projection) @ difference / system.log_block_scale
            for difference in np.diff(coefficients, axis=0)
        ],
        dtype=np.float64,
    )
    beta_residuals = np.linalg.norm(beta_vectors, axis=1)
    construction = np.array(
        [
            scalarized_ray_construction_residual(
                row[:, None, None] * system.matrix_direction,
                system.matrix_direction,
            )
            for row in coefficients
        ],
        dtype=np.float64,
    )
    basin_exits = np.any(
        (coefficients < system.basin_lower) | (coefficients > system.basin_upper),
        axis=1,
    )
    conditioning = np.max(coefficients, axis=1) / np.min(coefficients, axis=1)
    return {
        "projective_ray_angles": angles.tolist(),
        "normalized_coupling_distances": distances.tolist(),
        "retained_beta_residuals": beta_residuals.tolist(),
        "scalarized_ray_construction_residuals": construction.tolist(),
        "coefficient_conditioning": conditioning.tolist(),
        "matrix_condition": float(np.linalg.cond(system.matrix_direction)),
        "basin_exit": bool(np.any(basin_exits)),
        "rejected": False,
        "rejection_reason": None,
    }


def run_confirmatory_job(
    config: ExperimentConfig,
    *,
    job: Mapping[str, object],
    operator_opt_in: bool,
    operator_gate: Mapping[str, object],
    accepted_gate_sha256: str,
    work_root: Path,
    deadline_seconds: float = 300.0,
) -> dict[str, object]:
    """Run one preregistered paired job through 16 serial CUDA exchanges."""
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    if (
        config.theory.experiment != "gaussian_fixed_ray"
        or config.compute.backend != "cuda"
        or config.compute.dtype != "float64"
        or config.compute.heavy_sweep_enabled is not True
    ):
        raise ValueError("confirmatory job requires heavy CUDA float64 configuration")
    if operator_opt_in is not True:
        raise ValueError("confirmatory job requires explicit operator opt-in")
    if not np.isfinite(deadline_seconds) or not 0.0 < deadline_seconds <= 300.0:
        raise ValueError("confirmatory paired-job deadline must lie in (0, 300]")
    gate = dict(operator_gate)
    if (
        gate.get("schema_version") != "cuda-confirmatory-operator-gate-v1"
        or gate.get("operator_opt_in") is not True
        or gate.get("idle_observation_passed") is not True
        or _record_sha256(gate) != accepted_gate_sha256
    ):
        raise ValueError("operator acceptance does not match the confirmatory gate")
    _validate_confirmatory_gate_bindings(config, gate)
    try:
        expires_at = datetime.fromisoformat(str(gate["expires_at_utc"]))
    except (KeyError, ValueError) as error:
        raise ValueError("confirmatory gate expiry is invalid") from error
    if datetime.now(timezone.utc) >= expires_at:
        raise ValueError("confirmatory gate expired before job execution")

    job_id = job.get("job_id")
    master_seed = job.get("master_seed")
    role = job.get("role")
    if (
        not isinstance(job_id, str)
        or not (job_id.startswith("C") or job_id.startswith("H"))
        or type(master_seed) is not int
        or role not in {"confirmatory_primary", "confirmatory_holdout"}
        or job.get("schemes") != list(config.theory.blocking_schemes)
        or job.get("steps") != 8
    ):
        raise ValueError("confirmatory job record drifted from the frozen table")

    recheck = _capture_idle_gpu_gate_after_cooldown(operator_opt_in=operator_opt_in)
    _validate_gate_recheck(gate, recheck)
    recheck_sha256 = _record_sha256(recheck)
    system = build_preregistered_system()
    initial = generate_initial_coefficients(master_seed, job_id)
    initial_sha256 = hashlib.sha256(initial.tobytes(order="C")).hexdigest()
    trajectories = {
        scheme: np.empty((9, initial.size), dtype=np.float64)
        for scheme in config.theory.blocking_schemes
    }
    for trajectory in trajectories.values():
        trajectory[0, :] = initial

    repo_root = Path(__file__).resolve().parents[4]
    worker_script = repo_root / "tools" / "cuda_worker.py"
    environment_lock = repo_root / "environments" / "cuda-rtx5090-cu128.lock.txt"
    worker_records: list[dict[str, object]] = []
    peak_allocated = 0
    peak_reserved = 0
    started = time.perf_counter()
    for scheme in config.theory.blocking_schemes:
        spatial_map = system.spatial_maps[scheme]
        for step in range(1, 9):
            if time.perf_counter() - started > deadline_seconds:
                raise TimeoutError(f"confirmatory paired job exceeded five minutes: {job_id}")
            if datetime.now(timezone.utc) >= datetime.fromisoformat(
                str(recheck["expires_at_utc"])
            ):
                raise RuntimeError(f"GPU gate expired during confirmatory job {job_id}")
            immutable_id = f"confirmatory.{job_id}.{scheme}.step{step:02d}.cuda"
            execution_context = {
                "accepted_gate_sha256": accepted_gate_sha256,
                "accepted_gate_record": gate,
                "operator_gate_recheck_sha256": recheck_sha256,
                "operator_gate_recheck_record": recheck,
                "sentinel_job_id": job_id,
                "scheme": scheme,
                "step": step,
                "lane": "worker_cuda_confirmatory",
                "config_sha256": config_sha256(config),
                "source_revision": gate["source_identity"]["git_revision"],  # type: ignore[index]
            }
            result, stored_context = _run_or_resume_worker_job(
                worker_python=config.compute.cuda_worker_python,
                worker_script=worker_script,
                work_root=Path(work_root) / immutable_id,
                job_id=immutable_id,
                requested_backend="cuda",
                requested_dtype="float64",
                arrays={
                    "coefficients": trajectories[scheme][step - 1 : step, :],
                    "spatial_map": spatial_map,
                    "matrix_direction": system.matrix_direction,
                    "batch_size": np.array(config.compute.batch_size, dtype=np.int64),
                },
                environment_lock=environment_lock,
                execution_context=execution_context,
            )
            updated = np.asarray(result.arrays["updated_coefficients"], dtype=np.float64)
            if updated.shape != (1, initial.size) or not np.all(np.isfinite(updated)):
                raise RuntimeError(f"confirmatory worker output is invalid: {immutable_id}")
            trajectories[scheme][step, :] = updated[0]
            provenance = dict(result.provenance)
            peak_allocated = max(peak_allocated, int(provenance["peak_allocated_bytes"]))
            peak_reserved = max(peak_reserved, int(provenance["peak_reserved_bytes"]))
            worker_records.append(
                {
                    "job_id": immutable_id,
                    "scheme": scheme,
                    "step": step,
                    "execution_context": dict(stored_context),
                    "request_manifest": dict(result.request_manifest),
                    "response_manifest": dict(result.response_manifest),
                    "provenance": provenance,
                }
            )

    elapsed = time.perf_counter() - started
    if elapsed > deadline_seconds:
        raise TimeoutError(f"confirmatory paired job exceeded five minutes: {job_id}")
    first_scheme, second_scheme = config.theory.blocking_schemes
    dispersion = blocking_scheme_dispersion(
        trajectories[first_scheme], trajectories[second_scheme]
    )
    return {
        "schema_version": "gaussian-fixed-ray-confirmatory-job-v1",
        "job_id": job_id,
        "master_seed": master_seed,
        "role": role,
        "terminal_status": "completed",
        "scientific_analysis_eligibility": True,
        "accepted_gate_sha256": accepted_gate_sha256,
        "config_sha256": config_sha256(config),
        "source_revision": gate["source_identity"]["git_revision"],  # type: ignore[index]
        "initial_coefficients": initial.tolist(),
        "initial_coefficients_sha256": initial_sha256,
        "operator_gate_recheck": recheck,
        "operator_gate_recheck_sha256": recheck_sha256,
        "schemes": {
            scheme: _confirmatory_scheme_record(trajectories[scheme], system=system)
            for scheme in config.theory.blocking_schemes
        },
        "blocking_scheme_dispersion": dispersion.tolist(),
        "distinct_projective_rays": False,
        "worker_exchange_count": len(worker_records),
        "worker_exchanges": worker_records,
        "elapsed_seconds": elapsed,
        "peak_allocated_bytes": peak_allocated,
        "peak_reserved_bytes": peak_reserved,
        "trajectory_coefficients": {
            scheme: trajectories[scheme].tolist()
            for scheme in config.theory.blocking_schemes
        },
    }


def run_confirmatory_primary(
    config: ExperimentConfig,
    *,
    operator_opt_in: bool,
    operator_gate: Mapping[str, object],
    accepted_gate_sha256: str,
    work_root: Path,
) -> dict[str, object]:
    """Run or resume the 30 frozen primary jobs in deterministic order."""
    gate = dict(operator_gate)
    if (
        operator_opt_in is not True
        or _record_sha256(gate) != accepted_gate_sha256
        or gate.get("operator_opt_in") is not True
    ):
        raise ValueError("primary execution requires the accepted confirmatory gate")
    _validate_confirmatory_gate_bindings(config, gate)
    table = _job_table(config)
    jobs = [
        job
        for job in table["jobs"]  # type: ignore[union-attr]
        if job["role"] == "confirmatory_primary"
    ]
    expected_ids = [f"C{index:03d}" for index in range(1, 31)]
    if [job["job_id"] for job in jobs] != expected_ids:
        raise RuntimeError("primary job table drifted from the frozen sequence")
    staging = Path(work_root) / "primary-jobs"
    staging.mkdir(parents=True, exist_ok=True)
    config_hash = config_sha256(config)
    source_revision = gate["source_identity"]["git_revision"]  # type: ignore[index]
    records: list[dict[str, object]] = []
    for job in jobs:
        job_id = str(job["job_id"])
        path = staging / f"{job_id}.json"
        if path.is_file():
            record = json.loads(path.read_text(encoding="utf-8"))
            if (
                not isinstance(record, dict)
                or record.get("schema_version")
                != "gaussian-fixed-ray-confirmatory-job-v1"
                or record.get("job_id") != job_id
                or record.get("master_seed") != job["master_seed"]
                or record.get("role") != "confirmatory_primary"
                or record.get("terminal_status") != "completed"
                or record.get("scientific_analysis_eligibility") is not True
                or record.get("accepted_gate_sha256") != accepted_gate_sha256
                or record.get("config_sha256") != config_hash
                or record.get("source_revision") != source_revision
            ):
                raise RuntimeError(f"staged primary job identity drifted: {job_id}")
        else:
            record = run_confirmatory_job(
                config,
                job=job,
                operator_opt_in=operator_opt_in,
                operator_gate=gate,
                accepted_gate_sha256=accepted_gate_sha256,
                work_root=Path(work_root) / "worker-exchanges",
            )
            _atomic_json(path, record)
        records.append(record)
    return {
        "schema_version": "gaussian-fixed-ray-confirmatory-primary-execution-v1",
        "planned_job_ids": expected_ids,
        "completed_job_ids": [str(record["job_id"]) for record in records],
        "missing_job_ids": [],
        "job_records": records,
        "accepted_gate_sha256": accepted_gate_sha256,
        "config_sha256": config_hash,
        "source_revision": source_revision,
    }


def run_confirmatory_holdout(
    config: ExperimentConfig,
    *,
    operator_opt_in: bool,
    operator_gate: Mapping[str, object],
    accepted_gate_sha256: str,
    primary_analysis_path: Path,
    primary_analysis_sha256: str,
    work_root: Path,
) -> dict[str, object]:
    """Release and run the ten holdouts only after primary analysis is bound."""
    primary_path = Path(primary_analysis_path)
    if (
        not primary_path.is_file()
        or _file_sha256(primary_path) != primary_analysis_sha256
    ):
        raise ValueError("holdout release requires the exact primary analysis digest")
    try:
        primary = json.loads(primary_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("primary analysis record is invalid") from error
    if (
        not isinstance(primary, dict)
        or primary.get("schema_version")
        != "gaussian-fixed-ray-primary-analysis-v1"
        or primary.get("primary_job_ids")
        != [f"C{index:03d}" for index in range(1, 31)]
        or primary.get("classification")
        not in {"support", "counterevidence", "inconclusive"}
    ):
        raise ValueError("primary analysis record does not authorize holdout release")

    gate = dict(operator_gate)
    if (
        operator_opt_in is not True
        or _record_sha256(gate) != accepted_gate_sha256
        or gate.get("operator_opt_in") is not True
    ):
        raise ValueError("holdout execution requires the accepted confirmatory gate")
    _validate_confirmatory_gate_bindings(config, gate)
    table = _job_table(config)
    jobs = [
        job
        for job in table["jobs"]  # type: ignore[union-attr]
        if job["role"] == "confirmatory_holdout"
    ]
    expected_ids = [f"H{index:03d}" for index in range(1, 11)]
    if [job["job_id"] for job in jobs] != expected_ids:
        raise RuntimeError("holdout job table drifted from the frozen sequence")
    staging = Path(work_root) / "holdout-jobs"
    staging.mkdir(parents=True, exist_ok=True)
    config_hash = config_sha256(config)
    source_revision = gate["source_identity"]["git_revision"]  # type: ignore[index]
    records: list[dict[str, object]] = []
    for job in jobs:
        job_id = str(job["job_id"])
        path = staging / f"{job_id}.json"
        if path.is_file():
            record = json.loads(path.read_text(encoding="utf-8"))
            if (
                not isinstance(record, dict)
                or record.get("schema_version")
                != "gaussian-fixed-ray-confirmatory-job-v1"
                or record.get("job_id") != job_id
                or record.get("master_seed") != job["master_seed"]
                or record.get("role") != "confirmatory_holdout"
                or record.get("terminal_status") != "completed"
                or record.get("scientific_analysis_eligibility") is not True
                or record.get("accepted_gate_sha256") != accepted_gate_sha256
                or record.get("config_sha256") != config_hash
                or record.get("source_revision") != source_revision
            ):
                raise RuntimeError(f"staged holdout job identity drifted: {job_id}")
        else:
            record = run_confirmatory_job(
                config,
                job=job,
                operator_opt_in=operator_opt_in,
                operator_gate=gate,
                accepted_gate_sha256=accepted_gate_sha256,
                work_root=Path(work_root) / "worker-exchanges",
            )
            _atomic_json(path, record)
        records.append(record)
    return {
        "schema_version": "gaussian-fixed-ray-confirmatory-holdout-execution-v1",
        "planned_job_ids": expected_ids,
        "completed_job_ids": [str(record["job_id"]) for record in records],
        "missing_job_ids": [],
        "job_records": records,
        "primary_analysis_sha256": primary_analysis_sha256,
        "accepted_gate_sha256": accepted_gate_sha256,
        "config_sha256": config_hash,
        "source_revision": source_revision,
    }


def _sentinel_endpoint(
    coefficients: np.ndarray,
    *,
    system: object,
    scheme_dispersion: float,
) -> dict[str, object]:
    ray = system.perron_ray
    angles = np.array([projective_ray_angle(row, ray) for row in coefficients])
    normalized_ray = ray / np.linalg.norm(ray)
    distances = np.array(
        [np.linalg.norm(row / np.linalg.norm(row) - normalized_ray) for row in coefficients]
    )
    projection = np.outer(ray, ray) / float(np.dot(ray, ray))
    beta_vectors = np.array(
        [
            (np.eye(ray.size) - projection) @ difference / system.log_block_scale
            for difference in np.diff(coefficients, axis=0)
        ]
    )
    construction = max(
        scalarized_ray_construction_residual(
            row[:, None, None] * system.matrix_direction,
            system.matrix_direction,
        )
        for row in coefficients
    )
    basin_exit = bool(
        np.any(
            (coefficients < system.basin_lower)
            | (coefficients > system.basin_upper)
        )
    )
    maximum_condition = float(
        np.max(np.max(coefficients, axis=1) / np.min(coefficients, axis=1))
    )
    slope = _ols_slope(angles)
    scale_8_distance = float(distances[-1])
    return {
        "angle_slope_scales_4_8": slope,
        "scale_8_projective_ray_angle": float(angles[-1]),
        "scale_8_normalized_coupling_distance": scale_8_distance,
        "scale_8_retained_beta_residual": float(np.linalg.norm(beta_vectors[-1])),
        "maximum_scalarized_ray_construction_residual": float(construction),
        "scale_8_scheme_dispersion": float(scheme_dispersion),
        "maximum_coefficient_condition": maximum_condition,
        "basin_exit": basin_exit,
        "rejected": False,
        "angle_slope_threshold_pass": slope <= -0.02,
        "distance_threshold_pass": scale_8_distance <= 0.05,
        "dispersion_threshold_pass": scheme_dispersion <= 0.02,
    }


_SENTINEL_NUMERIC_FIELDS = (
    "angle_slope_scales_4_8",
    "scale_8_projective_ray_angle",
    "scale_8_normalized_coupling_distance",
    "scale_8_retained_beta_residual",
    "maximum_scalarized_ray_construction_residual",
    "scale_8_scheme_dispersion",
    "maximum_coefficient_condition",
)
_SENTINEL_DECISION_FIELDS = (
    "basin_exit",
    "rejected",
    "angle_slope_threshold_pass",
    "distance_threshold_pass",
    "dispersion_threshold_pass",
)


def _compare_sentinel_endpoint(
    reference: Mapping[str, object],
    candidate: Mapping[str, object],
    *,
    condition_number: float,
) -> dict[str, object]:
    numeric = parity_diagnostics(
        [reference[field] for field in _SENTINEL_NUMERIC_FIELDS],
        [candidate[field] for field in _SENTINEL_NUMERIC_FIELDS],
        dtype="float64",
        condition_number=condition_number,
    )
    decisions_match = all(
        reference[field] == candidate[field] for field in _SENTINEL_DECISION_FIELDS
    )
    return {
        "numeric": asdict(numeric),
        "exact_decisions_match": decisions_match,
        "passed": numeric.passed and decisions_match,
    }


def run_cuda_sentinel(
    config: ExperimentConfig,
    *,
    operator_opt_in: bool,
    operator_gate: Mapping[str, object],
    accepted_gate_sha256: str,
    work_root: Path,
    sample_count: int = 5,
) -> dict[str, object]:
    """Run the frozen five-job, three-lane float64 parity sentinel."""
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    if config.theory.experiment != "gaussian_fixed_ray":
        raise ValueError("CUDA sentinel requires gaussian_fixed_ray")
    if config.compute.backend != "cuda" or config.compute.dtype != "float64":
        raise ValueError("CUDA sentinel requires requested CUDA float64")
    if config.compute.heavy_sweep_enabled:
        raise ValueError("CUDA sentinel must pass before enabling the heavy sweep")
    if sample_count != 5:
        raise ValueError("CUDA sentinel requires exactly five initial idle samples")
    work_root = Path(work_root)

    gate = dict(operator_gate)
    gate_bytes = json.dumps(gate, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    gate_sha256 = hashlib.sha256(gate_bytes).hexdigest()
    if (
        gate.get("schema_version") != "cuda-idle-operator-gate-v1"
        or gate.get("operator_opt_in") is not True
        or gate.get("operator_process_acceptance_pending") is not True
        or gate.get("idle_observation_passed") is not True
        or accepted_gate_sha256 != gate_sha256
    ):
        raise ValueError("operator acceptance does not match the captured gate digest")
    _validate_cuda_gate_bindings(config, gate)
    try:
        expires_at = datetime.fromisoformat(str(gate["expires_at_utc"]))
    except (KeyError, ValueError) as error:
        raise ValueError("operator gate expiry is invalid") from error
    if datetime.now(timezone.utc) >= expires_at:
        raise ValueError("operator gate expired before sentinel execution")
    repo_root = Path(__file__).resolve().parents[4]
    worker_script = repo_root / "tools" / "cuda_worker.py"
    environment_lock = repo_root / "environments" / "cuda-rtx5090-cu128.lock.txt"
    if not worker_script.is_file() or not environment_lock.is_file():
        raise ValueError("CUDA sentinel prerequisites are missing")

    table = _job_table(config)
    jobs = {str(job["job_id"]): job for job in table["jobs"]}  # type: ignore[index]
    sentinel_ids = list(table["sentinel_job_ids"])  # type: ignore[arg-type]
    initial = _readonly(
        [
            generate_initial_coefficients(
                int(jobs[job_id]["master_seed"]), job_id
            )
            for job_id in sentinel_ids
        ]
    )
    system = build_preregistered_system()
    condition = float(np.linalg.cond(system.matrix_direction))
    lane_names = (
        "controller_cpu",
        "worker_cpu",
        "worker_cuda",
        "worker_cuda_repeat",
    )
    trajectories = {
        scheme: {
            lane: np.empty((len(initial), 9, initial.shape[1]), dtype=np.float64)
            for lane in lane_names
        }
        for scheme in config.theory.blocking_schemes
    }
    for scheme_lanes in trajectories.values():
        for values in scheme_lanes.values():
            values[:, 0, :] = initial
    parity_records: list[dict[str, object]] = []
    worker_jobs: list[dict[str, object]] = []
    gate_rechecks: list[dict[str, object]] = []

    for job_index, sentinel_id in enumerate(sentinel_ids):
        recheck = _capture_idle_gpu_gate_after_cooldown(
            operator_opt_in=operator_opt_in
        )
        _validate_gate_recheck(gate, recheck)
        recheck_bytes = json.dumps(
            recheck, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        recheck_sha256 = hashlib.sha256(recheck_bytes).hexdigest()
        gate_rechecks.append(
            {
                "sentinel_job_id": sentinel_id,
                "gate_sha256": recheck_sha256,
                "gate": recheck,
            }
        )
        for scheme in config.theory.blocking_schemes:
            spatial_map = system.spatial_maps[scheme]
            lanes = trajectories[scheme]
            for step in range(1, 9):
                lanes["controller_cpu"][job_index, step, :] = (
                    lanes["controller_cpu"][job_index, step - 1, :] @ spatial_map.T
                )
                executions = (
                    ("worker_cpu", "cpu"),
                    ("worker_cuda", "cuda"),
                    ("worker_cuda_repeat", "cuda"),
                )
                for lane, backend in executions:
                    if datetime.now(timezone.utc) >= datetime.fromisoformat(
                        str(recheck["expires_at_utc"])
                    ):
                        raise RuntimeError(
                            f"GPU gate expired during sentinel job {sentinel_id}"
                        )
                    immutable_id = (
                        f"sentinel.{sentinel_id}.{scheme}.step{step:02d}.{lane}"
                    )
                    result, stored_execution_context = _run_or_resume_worker_job(
                        worker_python=config.compute.cuda_worker_python,
                        worker_script=worker_script,
                        work_root=work_root / immutable_id,
                        job_id=immutable_id,
                        requested_backend=backend,  # type: ignore[arg-type]
                        requested_dtype="float64",
                        arrays={
                            "coefficients": lanes[lane][
                                job_index : job_index + 1, step - 1, :
                            ],
                            "spatial_map": spatial_map,
                            "matrix_direction": system.matrix_direction,
                            "batch_size": np.array(
                                config.compute.batch_size, dtype=np.int64
                            ),
                        },
                        environment_lock=environment_lock,
                        execution_context={
                            "accepted_gate_sha256": accepted_gate_sha256,
                            "accepted_gate_record": gate,
                            "operator_gate_recheck_sha256": recheck_sha256,
                            "operator_gate_recheck_record": recheck,
                            "sentinel_job_id": sentinel_id,
                            "scheme": scheme,
                            "step": step,
                            "lane": lane,
                            "config_sha256": config_sha256(config),
                            "source_revision": gate["source_identity"]["git_revision"],  # type: ignore[index]
                        },
                    )
                    lanes[lane][job_index, step, :] = result.arrays[
                        "updated_coefficients"
                    ][0]
                    worker_jobs.append(
                        {
                            "job_id": immutable_id,
                            "sentinel_job_id": sentinel_id,
                            "scheme": scheme,
                            "step": step,
                            "lane": lane,
                            "execution_context": dict(stored_execution_context),
                            "request_manifest": dict(result.request_manifest),
                            "response_manifest": dict(result.response_manifest),
                            "provenance": dict(result.provenance),
                        }
                    )

                comparisons = {
                    "controller_cpu_vs_worker_cpu": parity_diagnostics(
                        lanes["controller_cpu"][job_index, step, :],
                        lanes["worker_cpu"][job_index, step, :],
                        dtype="float64",
                        condition_number=condition,
                    ),
                    "controller_cpu_vs_worker_cuda": parity_diagnostics(
                        lanes["controller_cpu"][job_index, step, :],
                        lanes["worker_cuda"][job_index, step, :],
                        dtype="float64",
                        condition_number=condition,
                    ),
                    "controller_cpu_vs_worker_cuda_repeat": parity_diagnostics(
                        lanes["controller_cpu"][job_index, step, :],
                        lanes["worker_cuda_repeat"][job_index, step, :],
                        dtype="float64",
                        condition_number=condition,
                    ),
                    "worker_cpu_vs_worker_cuda": parity_diagnostics(
                        lanes["worker_cpu"][job_index, step, :],
                        lanes["worker_cuda"][job_index, step, :],
                        dtype="float64",
                        condition_number=condition,
                    ),
                    "worker_cuda_repeatability": parity_diagnostics(
                        lanes["worker_cuda"][job_index, step, :],
                        lanes["worker_cuda_repeat"][job_index, step, :],
                        dtype="float64",
                        condition_number=condition,
                    ),
                }
                parity_records.append(
                    {
                        "sentinel_job_id": sentinel_id,
                        "scheme": scheme,
                        "step": step,
                        "comparisons": {
                            name: asdict(diagnostics)
                            for name, diagnostics in comparisons.items()
                        },
                    }
                )
                if not all(
                    diagnostics.passed for diagnostics in comparisons.values()
                ):
                    raise RuntimeError(
                        f"CUDA sentinel parity failed for {sentinel_id}, "
                        f"{scheme}, step {step}"
                    )

    trajectories = {
        scheme: {
            lane: _readonly(values) for lane, values in scheme_lanes.items()
        }
        for scheme, scheme_lanes in trajectories.items()
    }

    endpoints: dict[str, dict[str, dict[str, object]]] = {
        lane: {} for lane in lane_names
    }
    first_scheme, second_scheme = config.theory.blocking_schemes
    for lane in lane_names:
        for job_index, sentinel_id in enumerate(sentinel_ids):
            dispersion = float(
                blocking_scheme_dispersion(
                    trajectories[first_scheme][lane][job_index],
                    trajectories[second_scheme][lane][job_index],
                )[-1]
            )
            endpoints[lane][sentinel_id] = {
                scheme: _sentinel_endpoint(
                    trajectories[scheme][lane][job_index],
                    system=system,
                    scheme_dispersion=dispersion,
                )
                for scheme in config.theory.blocking_schemes
            }

    endpoint_parity_records: list[dict[str, object]] = []
    scientific_decision_parity_passed = True
    for sentinel_id in sentinel_ids:
        for scheme in config.theory.blocking_schemes:
            reference = endpoints["controller_cpu"][sentinel_id][scheme]
            comparisons: dict[str, object] = {}
            for lane in lane_names[1:]:
                candidate = endpoints[lane][sentinel_id][scheme]
                comparison = _compare_sentinel_endpoint(
                    reference,
                    candidate,
                    condition_number=condition,
                )
                scientific_decision_parity_passed &= bool(comparison["passed"])
                comparisons[lane] = comparison
            endpoint_parity_records.append(
                {
                    "sentinel_job_id": sentinel_id,
                    "scheme": scheme,
                    "comparisons": comparisons,
                }
            )

    stratum_records: dict[str, dict[str, dict[str, str]]] = {}
    stratum_passed = True
    for scheme in config.theory.blocking_schemes:
        by_lane: dict[str, dict[str, str]] = {}
        for lane in lane_names:
            worst = max(
                sentinel_ids,
                key=lambda job_id: endpoints[lane][job_id][scheme][
                    "maximum_coefficient_condition"
                ],
            )
            threshold_near = min(
                sentinel_ids,
                key=lambda job_id: abs(
                    float(
                        endpoints[lane][job_id][scheme][
                            "angle_slope_scales_4_8"
                        ]
                    )
                    + 0.02
                ),
            )
            by_lane[lane] = {
                "worst_conditioned_job_id": worst,
                "threshold_near_job_id": threshold_near,
            }
        stratum_passed &= len(
            {record["worst_conditioned_job_id"] for record in by_lane.values()}
        ) == 1 and len(
            {record["threshold_near_job_id"] for record in by_lane.values()}
        ) == 1
        stratum_records[scheme] = by_lane
    scientific_decision_parity_passed &= stratum_passed

    reference_endpoint = endpoints["controller_cpu"][sentinel_ids[0]][first_scheme]
    mutated_endpoint = dict(reference_endpoint)
    reference_decision = bool(reference_endpoint["angle_slope_threshold_pass"])
    mutated_value = -0.0199999 if reference_decision else -0.0200001
    mutated_endpoint["angle_slope_scales_4_8"] = mutated_value
    mutated_endpoint["angle_slope_threshold_pass"] = not reference_decision
    mutation_comparison = _compare_sentinel_endpoint(
        reference_endpoint,
        mutated_endpoint,
        condition_number=condition,
    )
    threshold_mutation = {
        "threshold": -0.02,
        "sentinel_job_id": sentinel_ids[0],
        "scheme": first_scheme,
        "reference_value": reference_endpoint["angle_slope_scales_4_8"],
        "mutated_value": mutated_value,
        "reference_decision": reference_decision,
        "mutated_decision": not reference_decision,
        "comparison": mutation_comparison,
        "negative_control_passed": not bool(mutation_comparison["passed"]),
    }
    if not threshold_mutation["negative_control_passed"]:
        raise RuntimeError("threshold mutation was not rejected by endpoint parity")
    if not scientific_decision_parity_passed:
        raise RuntimeError("CUDA sentinel scientific endpoint or decision parity failed")

    final_controller = trajectories[config.theory.blocking_schemes[0]][
        "controller_cpu"
    ][:, -1, :]
    mutated = np.array(final_controller, copy=True)
    mutated[0, 0] += 1.0e-3
    mutation = parity_diagnostics(
        final_controller,
        mutated,
        dtype="float64",
        condition_number=condition,
    )
    if mutation.passed:
        raise RuntimeError("fixed parity mutation was not rejected")

    return {
        "schema_version": "gaussian-fixed-ray-cuda-sentinel-v1",
        "sentinel_job_ids": sentinel_ids,
        "scientific_analysis_eligibility": {
            job_id: False for job_id in sentinel_ids
        },
        "scientific_analysis_scope": (
            "Parity-only execution; no sentinel values enter primary, holdout, "
            "threshold, or tuning analyses."
        ),
        "operator_gate": gate,
        "operator_gate_sha256": gate_sha256,
        "accepted_gate_sha256": accepted_gate_sha256,
        "operator_gate_rechecks": gate_rechecks,
        "environment_lock_sha256": _file_sha256(environment_lock),
        "worker_script_sha256": _file_sha256(worker_script),
        "controller_python_executable": sys.executable,
        "controller_python_executable_sha256": _file_sha256(Path(sys.executable)),
        "requested_dtype": "float64",
        "requested_worker_backends": ["cpu", "cuda"],
        "all_parity_passed": scientific_decision_parity_passed,
        "scientific_decision_parity_passed": scientific_decision_parity_passed,
        "endpoint_parity_records": endpoint_parity_records,
        "sentinel_endpoints": endpoints,
        "stratum_decision_parity": {
            "passed": stratum_passed,
            "records": stratum_records,
        },
        "threshold_mutation_negative_control": threshold_mutation,
        "mutation_negative_control": asdict(mutation),
        "parity_records": parity_records,
        "worker_jobs": worker_jobs,
        "trajectories": trajectories,
        "initial_coefficients_sha256": hashlib.sha256(
            initial.tobytes(order="C")
        ).hexdigest(),
    }


def publish_cuda_sentinel(
    config: ExperimentConfig,
    *,
    operator_opt_in: bool,
    operator_gate: Mapping[str, object],
    accepted_gate_sha256: str,
    staging_root: Path,
) -> GaussianFixedRayExperimentResult:
    """Resume the sentinel staging tree and publish one immutable RunStore bundle."""
    repo_root = Path(__file__).resolve().parents[4]
    preregistration = (
        repo_root
        / "docs"
        / "experiments"
        / "2026-08-09-gaussian-fixed-ray-preregistration.md"
    )
    preregistration_sha256 = _validate_preregistration(preregistration)
    environment_lock = repo_root / "environments" / "cuda-rtx5090-cu128.lock.txt"
    worker_script = repo_root / "tools" / "cuda_worker.py"
    sentinel = run_cuda_sentinel(
        config,
        operator_opt_in=operator_opt_in,
        operator_gate=operator_gate,
        accepted_gate_sha256=accepted_gate_sha256,
        work_root=Path(staging_root),
    )
    if (
        sentinel["all_parity_passed"] is not True
        or sentinel["scientific_decision_parity_passed"] is not True
    ):
        raise RuntimeError("CUDA sentinel cannot publish failed parity")

    trajectory_payload = sentinel["trajectories"]
    arrays = {
        f"{scheme}_{lane}_coefficients": _readonly(values)
        for scheme, lanes in trajectory_payload.items()  # type: ignore[union-attr]
        for lane, values in lanes.items()
    }
    worker_jobs = sentinel["worker_jobs"]
    sentinel_json = {
        key: value
        for key, value in sentinel.items()
        if key not in {"trajectories", "worker_jobs"}
    }
    job_table = _job_table(config)
    job_table_bytes = json.dumps(
        job_table, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    config_hash = config_sha256(config)
    streams = RngStreams.from_seed(config.run.seed)
    provenance = collect_provenance(repo_root, repo_root / "Theory", config_hash, streams)
    provenance["experiment_scope"] = "cuda_float64_parity_sentinel_only"
    provenance["confirmatory_executed"] = False
    provenance["effective_backend"] = "cpu_controller_cpu_worker_cuda_worker"
    provenance["effective_dtype"] = "float64"
    input_hashes = provenance["input_hashes"]
    input_hashes["operator_gate_sha256"] = accepted_gate_sha256  # type: ignore[index]
    input_hashes["preregistration_sha256"] = preregistration_sha256  # type: ignore[index]
    input_hashes["environment_lock_sha256"] = _file_sha256(environment_lock)  # type: ignore[index]
    input_hashes["worker_script_sha256"] = _file_sha256(worker_script)  # type: ignore[index]
    input_hashes["job_table_sha256"] = hashlib.sha256(job_table_bytes).hexdigest()  # type: ignore[index]
    metrics = {
        "cuda_sentinel_parity": _metric(
            0.0,
            status="pass",
            tolerance=config.numerics.atol,
            interpretation=(
                "Five preregistered parity-only sentinel IDs passed controller CPU, "
                "worker CPU, CUDA, repeated-CUDA endpoint and decision parity."
            ),
        )
    }
    store = RunStore.create(config, provenance)
    store.write_json("cuda_gate", operator_gate)
    store.write_json("preregistered_job_table", job_table)
    store.write_json("sentinel_parity", sentinel_json)
    store.write_npz("sentinel_arrays", arrays)
    store.write_json(
        "worker_exchange_index",
        {
            "schema_version": "gaussian-fixed-ray-worker-exchange-index-v1",
            "staging_root": str(Path(staging_root).resolve()),
            "records": worker_jobs,
        },
    )
    store.write_json("metrics", {name: asdict(value) for name, value in metrics.items()})
    store.finalize(
        (
            "cuda_gate.json",
            "preregistered_job_table.json",
            "sentinel_parity.json",
            "sentinel_arrays.npz",
            "worker_exchange_index.json",
            "metrics.json",
        )
    )
    return GaussianFixedRayExperimentResult(
        run_dir=store.run_dir,
        config_hash=store.config_hash,
        status="pass",
        metrics=MappingProxyType(metrics),
        arrays=MappingProxyType(arrays),
    )


def _validate_confirmatory_sentinel_bundle(
    sentinel_run_dir: Path,
    accepted_manifest_sha256: str,
    operator_gate: Mapping[str, object],
) -> dict[str, object]:
    run_dir = Path(sentinel_run_dir)
    manifest_path = run_dir / "manifest.json"
    parity_path = run_dir / "sentinel_parity.json"
    if (
        not manifest_path.is_file()
        or _file_sha256(manifest_path) != accepted_manifest_sha256
        or not parity_path.is_file()
    ):
        raise ValueError("accepted current-revision sentinel bundle is missing or drifted")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        parity = json.loads(parity_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("accepted sentinel bundle is invalid") from error
    provenance = manifest.get("provenance") if isinstance(manifest, dict) else None
    source = operator_gate.get("source_identity")
    if (
        manifest.get("complete") is not True
        or not isinstance(provenance, Mapping)
        or not isinstance(source, Mapping)
        or provenance.get("git_commit") != source.get("git_revision")
        or provenance.get("git_dirty") is not False
        or provenance.get("experiment_scope") != "cuda_float64_parity_sentinel_only"
        or provenance.get("confirmatory_executed") is not False
        or parity.get("all_parity_passed") is not True
        or parity.get("scientific_decision_parity_passed") is not True
        or set(parity.get("scientific_analysis_eligibility", {}).values()) != {False}
    ):
        raise ValueError("accepted sentinel bundle is not eligible for confirmation")
    return {
        "manifest_sha256": accepted_manifest_sha256,
        "git_commit": provenance["git_commit"],
        "scientific_decision_parity_passed": True,
        "sentinel_job_ids": list(parity["sentinel_job_ids"]),
    }


def publish_confirmatory_experiment(
    config: ExperimentConfig,
    *,
    operator_opt_in: bool,
    operator_gate: Mapping[str, object],
    accepted_gate_sha256: str,
    sentinel_run_dir: Path,
    accepted_sentinel_manifest_sha256: str,
    staging_root: Path,
) -> GaussianFixedRayExperimentResult:
    """Execute, analyze, and atomically publish the two-stage 40-job bundle."""
    if (
        config.compute.backend != "cuda"
        or config.compute.dtype != "float64"
        or config.compute.heavy_sweep_enabled is not True
    ):
        raise ValueError("confirmatory publication requires heavy CUDA float64")
    gate = dict(operator_gate)
    if operator_opt_in is not True or _record_sha256(gate) != accepted_gate_sha256:
        raise ValueError("confirmatory publication requires exact operator acceptance")
    _validate_confirmatory_gate_bindings(config, gate)
    sentinel_identity = _validate_confirmatory_sentinel_bundle(
        Path(sentinel_run_dir), accepted_sentinel_manifest_sha256, gate
    )

    staging = Path(staging_root)
    staging.mkdir(parents=True, exist_ok=True)
    table = _job_table(config)
    planned_table_bytes = json.dumps(
        table, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    job_table_sha256 = hashlib.sha256(planned_table_bytes).hexdigest()
    primary_execution = run_confirmatory_primary(
        config,
        operator_opt_in=operator_opt_in,
        operator_gate=gate,
        accepted_gate_sha256=accepted_gate_sha256,
        work_root=staging,
    )
    primary_records = primary_execution["job_records"]
    primary_analysis = analyze_primary(
        primary_records,
        protocol_id="2026-08-09-gaussian-fixed-ray-v1a",
        job_table_sha256=job_table_sha256,
        decision_stability=bool(
            sentinel_identity.get("scientific_decision_parity_passed", True)
        ),
        premises_passed=True,
        gpu_gate_complete=True,
    )
    primary_path = staging / "primary_analysis.json"
    if primary_path.is_file():
        stored_primary = json.loads(primary_path.read_text(encoding="utf-8"))
        if stored_primary != primary_analysis:
            raise RuntimeError("staged primary analysis drifted from recomputation")
    else:
        _atomic_json(primary_path, primary_analysis)
    primary_sha256 = _file_sha256(primary_path)

    holdout_execution = run_confirmatory_holdout(
        config,
        operator_opt_in=operator_opt_in,
        operator_gate=gate,
        accepted_gate_sha256=accepted_gate_sha256,
        primary_analysis_path=primary_path,
        primary_analysis_sha256=primary_sha256,
        work_root=staging,
    )
    holdout_records = holdout_execution["job_records"]
    holdout_analysis = analyze_holdout(
        holdout_records,
        protocol_id="2026-08-09-gaussian-fixed-ray-v1a",
        job_table_sha256=job_table_sha256,
        primary_analysis_sha256=primary_sha256,
    )
    all_records = [*primary_records, *holdout_records]
    if (
        len(all_records) != 40
        or primary_execution.get("missing_job_ids")
        or holdout_execution.get("missing_job_ids")
    ):
        raise RuntimeError("confirmatory publication requires 40 terminal job records")

    arrays: dict[str, np.ndarray] = {}
    for record in all_records:
        job_id = str(record["job_id"])
        arrays[f"{job_id}_initial_coefficients"] = _readonly(
            record["initial_coefficients"]
        )
        trajectory_payload = record["trajectory_coefficients"]
        for scheme in config.theory.blocking_schemes:
            arrays[f"{job_id}_{scheme}_coefficients"] = _readonly(
                trajectory_payload[scheme]  # type: ignore[index]
            )

    endpoint_records = []
    worker_exchanges: list[object] = []
    gate_rechecks: list[dict[str, object]] = []
    for record in all_records:
        endpoint_records.append(
            {
                key: value
                for key, value in record.items()
                if key not in {"trajectory_coefficients", "worker_exchanges"}
            }
        )
        worker_exchanges.extend(record.get("worker_exchanges", []))
        gate_rechecks.append(
            {
                "job_id": record["job_id"],
                "gate_sha256": record.get("operator_gate_recheck_sha256"),
                "gate": record.get("operator_gate_recheck"),
            }
        )
    execution = {
        "schema_version": "gaussian-fixed-ray-confirmatory-execution-v1",
        "accepted_gate_sha256": accepted_gate_sha256,
        "accepted_sentinel_manifest_sha256": accepted_sentinel_manifest_sha256,
        "primary_analysis_sha256": primary_sha256,
        "planned_job_count": 40,
        "completed_job_count": 40,
        "rejected_job_count": int(
            sum(
                any(bool(scheme["rejected"]) for scheme in record["schemes"].values())
                for record in all_records
            )
        ),
        "missing_job_count": 0,
        "worker_exchange_count": len(worker_exchanges),
        "worker_exchanges": worker_exchanges,
        "operator_gate_rechecks": gate_rechecks,
        "total_elapsed_seconds": float(
            sum(float(record.get("elapsed_seconds", 0.0)) for record in all_records)
        ),
        "peak_allocated_bytes": max(
            int(record.get("peak_allocated_bytes", 0)) for record in all_records
        ),
        "peak_reserved_bytes": max(
            int(record.get("peak_reserved_bytes", 0)) for record in all_records
        ),
        "stopping_reason": "planned_table_complete",
    }
    published_table = dict(table)
    published_table["confirmatory_executed"] = True
    published_table["executed_primary_job_ids"] = [
        f"C{index:03d}" for index in range(1, 31)
    ]
    published_table["executed_holdout_job_ids"] = [
        f"H{index:03d}" for index in range(1, 11)
    ]

    classification = str(primary_analysis["classification"])
    metric = _metric(
        {"counterevidence": -1.0, "inconclusive": 0.0, "support": 1.0}[
            classification
        ],
        status={
            "counterevidence": "fail",
            "inconclusive": "inconclusive",
            "support": "pass",
        }[classification],  # type: ignore[arg-type]
        interpretation=(
            "Finite preregistered 30-job primary classification; the 10-job "
            "holdout is descriptive and unrestricted attraction/universality remain open."
        ),
    )
    metrics = {"confirmatory_primary_classification": metric}
    repo_root = Path(__file__).resolve().parents[4]
    config_hash = config_sha256(config)
    streams = RngStreams.from_seed(config.run.seed)
    provenance = collect_provenance(repo_root, repo_root / "Theory", config_hash, streams)
    provenance["experiment_scope"] = "gaussian_fixed_ray_confirmatory_40_job"
    provenance["confirmatory_executed"] = True
    provenance["effective_backend"] = "cuda_worker"
    provenance["effective_dtype"] = "float64"
    input_hashes = provenance["input_hashes"]
    input_hashes["operator_gate_sha256"] = accepted_gate_sha256  # type: ignore[index]
    input_hashes["sentinel_manifest_sha256"] = accepted_sentinel_manifest_sha256  # type: ignore[index]
    input_hashes["preregistration_sha256"] = _PREREGISTRATION_SHA256  # type: ignore[index]
    input_hashes["job_table_sha256"] = job_table_sha256  # type: ignore[index]
    input_hashes["primary_analysis_sha256"] = primary_sha256  # type: ignore[index]

    store = RunStore.create(config, provenance)
    store.write_json("confirmatory_job_table", published_table)
    store.write_json(
        "confirmatory_endpoints",
        {
            "schema_version": "gaussian-fixed-ray-confirmatory-endpoints-v1",
            "records": endpoint_records,
        },
    )
    store.write_json("primary_analysis", primary_analysis)
    store.write_json("holdout_analysis", holdout_analysis)
    store.write_json("confirmatory_execution", execution)
    store.write_npz("confirmatory_arrays", arrays)
    store.write_json("metrics", {name: asdict(value) for name, value in metrics.items()})
    store.finalize(
        (
            "confirmatory_job_table.json",
            "confirmatory_endpoints.json",
            "primary_analysis.json",
            "holdout_analysis.json",
            "confirmatory_execution.json",
            "confirmatory_arrays.npz",
            "metrics.json",
        )
    )
    return GaussianFixedRayExperimentResult(
        run_dir=store.run_dir,
        config_hash=store.config_hash,
        status=metric.status,
        metrics=MappingProxyType(metrics),
        arrays=MappingProxyType(arrays),
    )


def _validate_preregistration(path: Path) -> str:
    if not path.is_file():
        raise ValueError(f"preregistration does not exist: {path}")
    digest = _canonical_text_sha256(path)
    if digest != _PREREGISTRATION_SHA256:
        raise ValueError("preregistration does not match the frozen file SHA-256")
    text = path.read_text(encoding="utf-8")
    required_literals = (
        "2026-08-09-gaussian-fixed-ray-v1",
        "heavy_sweep_enabled=False",
        "`P001`-`P004`",
        "`C001`-`C030`",
        "`H001`-`H010`",
        "Mathematical `REFUTED` requires",
        "2026-08-09-gaussian-fixed-ray-v1a",
        "`construction_residual`",
        "`retained_beta_trend`",
        "`basin_exit_rate`",
        "`scheme_dispersion`",
        "`conditioning_trend`",
        "`rejection_rate`",
        "exact one-sided sign test",
        "confirmatory-analysis-bootstrap-v1",
        "21,600-second authorization TTL",
    )
    if any(literal not in text for literal in required_literals):
        raise ValueError("preregistration is missing a frozen decision literal")
    return digest


def _job_table(config: ExperimentConfig) -> dict[str, object]:
    jobs: list[dict[str, object]] = []
    groups = (
        ("P", 4, 202608090001, "pilot"),
        ("C", 30, 202608090101, "confirmatory_primary"),
        ("H", 10, 202608090201, "confirmatory_holdout"),
    )
    for prefix, count, first_seed, role in groups:
        for offset in range(count):
            job_id = f"{prefix}{offset + 1:03d}"
            master_seed = first_seed + offset
            jobs.append(
                {
                    "job_id": job_id,
                    "master_seed": master_seed,
                    "substream_seed_u64": job_seed(master_seed, job_id),
                    "role": role,
                    "schemes": list(config.theory.blocking_schemes),
                    "steps": 8,
                }
            )
    return {
        "schema_version": "gaussian-fixed-ray-job-table-v1",
        "preregistration": config.theory.preregistration,
        "jobs": jobs,
        "executed_pilot_jobs": [dict(job) for job in jobs[:4]],
        "confirmatory_executed": False,
        "heavy_sweep_enabled": config.compute.heavy_sweep_enabled,
        "primary_scale_window": [4, 5, 6, 7, 8],
        "sentinel_job_ids": ["C001", "C015", "C030", "H001", "H010"],
    }


def _metric(
    value: float,
    *,
    status: MetricStatus,
    interpretation: str,
    theorem_status: str = "NUMERICAL",
    verification_state: str = "CANDIDATE",
    tolerance: float = 0.0,
) -> MetricRecord:
    return MetricRecord(
        value=float(value),
        tolerance=float(tolerance),
        status=status,
        interpretation=interpretation,
        assessment_scope="implementation_check",
        theorem_status=theorem_status,  # type: ignore[arg-type]
        verification_state=verification_state,  # type: ignore[arg-type]
        claim_origin="APPLICATION_SPECIFIC",
    )


def _ols_slope(values: np.ndarray) -> float:
    scales = np.arange(4.0, 9.0)
    centered = scales - np.mean(scales)
    return float(np.dot(centered, values[4:9]) / np.dot(centered, centered))


def _run_pilot(
    config: ExperimentConfig,
    *,
    repo_root: Path,
) -> tuple[
    dict[str, MetricRecord],
    dict[str, np.ndarray],
    list[dict[str, object]],
    dict[str, object],
    dict[str, object],
    dict[str, object],
]:
    system = build_preregistered_system()
    pilot_jobs = _job_table(config)["executed_pilot_jobs"]
    assert isinstance(pilot_jobs, list)
    initial = _readonly(
        [
            generate_initial_coefficients(
                int(job["master_seed"]), str(job["job_id"])
            )
            for job in pilot_jobs
        ]
    )
    trajectories = {
        scheme: [
            iterate_fixed_ray(system, row, scheme=scheme, steps=8) for row in initial
        ]
        for scheme in config.theory.blocking_schemes
    }
    first_scheme, second_scheme = config.theory.blocking_schemes
    dispersion = _readonly(
        [
            blocking_scheme_dispersion(first.coefficients, second.coefficients)
            for first, second in zip(
                trajectories[first_scheme], trajectories[second_scheme]
            )
        ]
    )

    arrays: dict[str, np.ndarray] = {
        "initial_coefficients": initial,
        "matrix_direction": _readonly(system.matrix_direction),
        "perron_ray": _readonly(system.perron_ray),
        "blocking_scheme_dispersion": dispersion,
    }
    for scheme in config.theory.blocking_schemes:
        scheme_trajectories = trajectories[scheme]
        arrays[f"{scheme}_spatial_map"] = _readonly(system.spatial_maps[scheme])
        arrays[f"{scheme}_coefficients"] = _readonly(
            [trajectory.coefficients for trajectory in scheme_trajectories]
        )
        arrays[f"{scheme}_coupling_matrices"] = _readonly(
            [trajectory.coupling_matrices for trajectory in scheme_trajectories]
        )
        arrays[f"{scheme}_projective_angles"] = _readonly(
            [trajectory.projective_ray_angles for trajectory in scheme_trajectories]
        )
        arrays[f"{scheme}_normalized_distances"] = _readonly(
            [trajectory.normalized_coupling_distances for trajectory in scheme_trajectories]
        )
        arrays[f"{scheme}_retained_beta_residuals"] = _readonly(
            [trajectory.retained_beta_residuals for trajectory in scheme_trajectories]
        )
        arrays[f"{scheme}_retained_beta_residual_vectors"] = _readonly(
            [
                trajectory.retained_beta_residual_vectors
                for trajectory in scheme_trajectories
            ]
        )
        arrays[f"{scheme}_basin_exits"] = _readonly(
            [trajectory.basin_exits for trajectory in scheme_trajectories],
            dtype=np.bool_,
        )
        arrays[f"{scheme}_coefficient_conditioning"] = _readonly(
            [trajectory.coefficient_conditioning for trajectory in scheme_trajectories]
        )
    arrays["scalarized_ray_construction_residuals"] = _readonly(
        [
            [
                trajectory.scalarized_ray_construction_residuals
                for trajectory in trajectories[scheme]
            ]
            for scheme in config.theory.blocking_schemes
        ]
    )

    worker_script = repo_root / "tools" / "cuda_worker.py"
    environment_lock = repo_root / "environments" / "cuda-rtx5090-cu128.lock.txt"
    temporary_parent = Path(config.output.root).resolve()
    temporary_parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix="session6-fixed-ray-worker-", dir=temporary_parent
    ) as temporary:
        worker_result = run_worker_job(
            worker_python=config.compute.cuda_worker_python,
            worker_script=worker_script,
            work_root=Path(temporary) / "pilot-one-step",
            job_id="PILOT-CPU-ONE-STEP",
            requested_backend="cpu",
            requested_dtype="float64",
            arrays={
                "coefficients": initial,
                "spatial_map": system.spatial_maps[first_scheme],
                "matrix_direction": system.matrix_direction,
                "batch_size": np.array(config.compute.batch_size, dtype=np.int64),
            },
            environment_lock=environment_lock,
        )
        worker_provenance = dict(worker_result.provenance)
        worker_request = dict(worker_result.request_manifest)
        worker_response = dict(worker_result.response_manifest)
        worker_updated = _readonly(worker_result.arrays["updated_coefficients"])

    controller_updated = _readonly(initial @ system.spatial_maps[first_scheme].T)
    parity = parity_diagnostics(
        controller_updated,
        worker_updated,
        dtype="float64",
        condition_number=float(np.linalg.cond(system.matrix_direction)),
    )
    mutated = np.array(worker_updated, copy=True)
    mutated[0, 0] += 1.0e-3
    mutation_parity = parity_diagnostics(
        controller_updated,
        mutated,
        dtype="float64",
        condition_number=float(np.linalg.cond(system.matrix_direction)),
    )
    arrays["controller_cpu_one_step"] = controller_updated
    arrays["worker_cpu_one_step"] = worker_updated

    angles = np.concatenate(
        [arrays[f"{scheme}_projective_angles"][:, -1] for scheme in config.theory.blocking_schemes]
    )
    distances = np.concatenate(
        [arrays[f"{scheme}_normalized_distances"][:, -1] for scheme in config.theory.blocking_schemes]
    )
    beta = np.concatenate(
        [arrays[f"{scheme}_retained_beta_residuals"][:, -1] for scheme in config.theory.blocking_schemes]
    )
    signed_beta = np.concatenate(
        [
            arrays[f"{scheme}_retained_beta_residual_vectors"][:, -1, :].ravel()
            for scheme in config.theory.blocking_schemes
        ]
    )
    basin = np.concatenate(
        [arrays[f"{scheme}_basin_exits"] for scheme in config.theory.blocking_schemes]
    )
    construction_residuals = arrays["scalarized_ray_construction_residuals"]
    metrics = {
        "projective_ray_angle": _metric(
            float(np.median(angles)),
            status="pass",
            interpretation="Pilot median scale-8 angle; finite trend only and not confirmatory evidence.",
        ),
        "normalized_coupling_distance": _metric(
            float(np.median(distances)),
            status="pass",
            interpretation="Pilot median scale-8 normalized distance within the frozen finite domain.",
        ),
        "scalarized_ray_construction_residual": target_metric(
            float(np.max(construction_residuals)),
            config.numerics.atol,
            target=0.0,
            interpretation="Roundoff consistency of the constructed W_e=c_e M0 ray; unrestricted matrix dynamics are not implemented.",
            theorem_status="NUMERICAL",
            verification_state="CANDIDATE",
            claim_origin="APPLICATION_SPECIFIC",
        ),
        "retained_beta_residual": _metric(
            float(np.median(beta)),
            status="pass",
            interpretation="Pilot norm of the signed comparison-typed scale-8 finite-difference residual.",
        ),
        "retained_beta_residual_signed_max": _metric(
            float(np.max(signed_beta)),
            status="pass",
            interpretation="Largest signed component of the pilot scale-8 retained beta residual vector.",
        ),
        "retained_beta_residual_signed_min": _metric(
            float(np.min(signed_beta)),
            status="pass",
            interpretation="Smallest signed component of the pilot scale-8 retained beta residual vector.",
        ),
        "basin_exit_rate": target_metric(
            float(np.mean(basin)),
            0.0,
            target=0.0,
            interpretation="No pilot coefficient left the frozen positive coefficient basin.",
            theorem_status="NUMERICAL",
            verification_state="CANDIDATE",
            claim_origin="APPLICATION_SPECIFIC",
        ),
        "blocking_scheme_dispersion": _metric(
            float(np.median(dispersion[:, -1])),
            status="pass",
            interpretation="Pilot paired scale-8 dispersion for the two noncommuting blocking schemes.",
        ),
        "cpu_cuda_parity_residual": _metric(
            parity.maximum_absolute_residual,
            status="inconclusive",
            tolerance=parity.atol,
            interpretation="Controller/worker CPU parity passed; CUDA float64 parity was not requested by this ordinary CPU pilot.",
            theorem_status="OPEN",
            verification_state="INCONCLUSIVE",
        ),
        "noncommuting_scheme_control": target_metric(
            system.noncommuting_gap,
            1.0e-15,
            target=0.01,
            interpretation="Independent literal oracle detects the frozen noncommuting map pair.",
            theorem_status="NUMERICAL",
            verification_state="CANDIDATE",
            claim_origin="APPLICATION_SPECIFIC",
        ),
        "commuting_mutation_control": target_metric(
            float(
                np.max(
                    np.abs(
                        system.spatial_maps[first_scheme]
                        @ system.spatial_maps[first_scheme]
                        - system.spatial_maps[first_scheme]
                        @ system.spatial_maps[first_scheme]
                    )
                )
            ),
            0.0,
            target=0.0,
            interpretation="Replacing the second scheme by the first destroys the noncommuting control as pinned.",
            theorem_status="NUMERICAL",
            verification_state="CANDIDATE",
            claim_origin="APPLICATION_SPECIFIC",
        ),
        "parity_mutation_negative_control": _metric(
            mutation_parity.maximum_absolute_residual,
            status="pass" if not mutation_parity.passed else "fail",
            tolerance=mutation_parity.atol,
            interpretation="A fixed output mutation is rejected by the parity rule.",
        ),
    }

    endpoints: list[dict[str, object]] = []
    for job_index, job in enumerate(pilot_jobs):
        for scheme in config.theory.blocking_schemes:
            trajectory = trajectories[scheme][job_index]
            endpoints.append(
                {
                    "job_id": job["job_id"],
                    "master_seed": job["master_seed"],
                    "scheme": scheme,
                    "angle_slope_scales_4_8": _ols_slope(
                        trajectory.projective_ray_angles
                    ),
                    "scale_8_projective_ray_angle": float(
                        trajectory.projective_ray_angles[-1]
                    ),
                    "scale_8_normalized_coupling_distance": float(
                        trajectory.normalized_coupling_distances[-1]
                    ),
                    "scale_8_retained_beta_residual": float(
                        trajectory.retained_beta_residuals[-1]
                    ),
                    "maximum_scalarized_ray_construction_residual": float(
                        np.max(trajectory.scalarized_ray_construction_residuals)
                    ),
                    "basin_exit": bool(np.any(trajectory.basin_exits)),
                    "maximum_coefficient_condition": float(
                        np.max(trajectory.coefficient_conditioning)
                    ),
                    "matrix_condition": trajectory.matrix_condition,
                    "rejected": False,
                    "rejection_reason": None,
                }
            )

    backend_provenance = {
        "controller_cpu": {
            "python_executable": sys.executable,
            "python_executable_sha256": _file_sha256(Path(sys.executable)),
            "python_version": sys.version,
            "requested_backend": "cpu",
            "effective_backend": "cpu",
            "requested_dtype": "float64",
            "effective_dtype": "float64",
            "peak_allocated_bytes": 0,
            "peak_reserved_bytes": 0,
        },
        "worker_cpu": {
            **worker_provenance,
            "request_manifest": worker_request,
            "response_manifest": worker_response,
            "output_identity": worker_response["output_identity"],
        },
        "worker_cuda": {
            "status": "not_requested_cpu_pilot",
            "evidence_state": "INCONCLUSIVE_NOT_REQUESTED_CPU_PILOT",
            "requested_backend": None,
            "requested_dtype": None,
            "effective_backend": None,
            "effective_dtype": None,
            "heavy_sweep_enabled": False,
            "gate_record": None,
        },
    }
    parity_matrix = {
        "controller_cpu_vs_worker_cpu": {**asdict(parity), "status": "pass"},
        "controller_cpu_vs_worker_cuda": {
            "status": "inconclusive",
            "passed": None,
            "reason": "CUDA was not requested by the ordinary CPU pilot.",
        },
        "worker_cpu_vs_worker_cuda": {
            "status": "inconclusive",
            "passed": None,
            "reason": "CUDA was not requested by the ordinary CPU pilot.",
        },
        "mutation_negative_control": {
            **asdict(mutation_parity),
            "status": "pass" if not mutation_parity.passed else "fail",
        },
    }
    performance = {
        "scope": "functional_runtime_record_not_a_benchmark",
        "pilot_jobs": 4,
        "paired_trajectories": 8,
        "map_applications": 64,
        "worker_cpu_peak_allocated_bytes": worker_provenance["peak_allocated_bytes"],
        "worker_cpu_peak_reserved_bytes": worker_provenance["peak_reserved_bytes"],
        "cuda_runtime_seconds": None,
        "cuda_peak_allocated_bytes": None,
        "cuda_peak_reserved_bytes": None,
    }
    return metrics, arrays, endpoints, backend_provenance, parity_matrix, performance


def run_gaussian_fixed_ray_experiment(
    config: ExperimentConfig,
    *,
    preregistration_path: Path | None = None,
) -> GaussianFixedRayExperimentResult:
    """Validate, execute the CPU-only pilot, and atomically publish artifacts."""
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    if config.theory.experiment != "gaussian_fixed_ray":
        raise ValueError("Gaussian fixed ray requires theory.experiment='gaussian_fixed_ray'")
    if config.theory.matrix_dimension != 2:
        raise ValueError("Gaussian fixed ray requires matrix_dimension=2")
    if config.compute.backend != "cpu" or config.compute.dtype != "float64":
        raise ValueError("non-heavy pilot requires CPU float64")
    if config.compute.heavy_sweep_enabled:
        raise ValueError("heavy sweep requires a separate idle-GPU and operator-opt-in gate")
    if config.output.render_figures:
        raise ValueError("Gaussian fixed-ray pilot exposes no figure renderer")

    repo_root = Path(__file__).resolve().parents[4]
    resolved_preregistration = (
        repo_root
        / "docs"
        / "experiments"
        / "2026-08-09-gaussian-fixed-ray-preregistration.md"
        if preregistration_path is None
        else Path(preregistration_path)
    )
    preregistration_sha256 = _validate_preregistration(resolved_preregistration)
    environment_lock = repo_root / "environments" / "cuda-rtx5090-cu128.lock.txt"
    if not environment_lock.is_file():
        raise ValueError("frozen CUDA environment lock is missing")
    if not (repo_root / "tools" / "cuda_worker.py").is_file():
        raise ValueError("standalone worker script is missing")

    start = time.perf_counter()
    metrics, arrays, endpoints, backend, parity, performance = _run_pilot(
        config, repo_root=repo_root
    )
    performance["controller_wall_seconds"] = time.perf_counter() - start
    job_table = _job_table(config)

    config_hash = config_sha256(config)
    streams = RngStreams.from_seed(config.run.seed)
    provenance = collect_provenance(repo_root, repo_root / "Theory", config_hash, streams)
    provenance["experiment_scope"] = "preregistered_four-job_cpu_pilot_only"
    provenance["preregistration_sha256"] = preregistration_sha256
    provenance["heavy_sweep_enabled"] = False
    provenance["confirmatory_executed"] = False
    provenance["input_hashes"]["preregistration_sha256"] = preregistration_sha256  # type: ignore[index]
    provenance["input_hashes"]["environment_lock_sha256"] = _file_sha256(environment_lock)  # type: ignore[index]
    provenance["input_hashes"]["initial_coefficients_sha256"] = hashlib.sha256(  # type: ignore[index]
        arrays["initial_coefficients"].tobytes(order="C")
    ).hexdigest()
    provenance["effective_backend"] = "cpu_controller_and_cpu_worker"
    provenance["effective_dtype"] = "float64"
    provenance["cuda_evidence_state"] = "INCONCLUSIVE_NOT_REQUESTED_CPU_PILOT"

    store = RunStore.create(config, provenance)
    store.write_json("preregistered_job_table", job_table)
    store.write_npz("initial_conditions", arrays)
    store.write_json(
        "per_seed_endpoints",
        {
            "schema_version": "gaussian-fixed-ray-endpoints-v1",
            "pilot_only": True,
            "records": endpoints,
            "rejected_run_count": 0,
        },
    )
    store.write_json("backend_provenance", backend)
    store.write_json("parity_matrix", parity)
    store.write_json("performance_records", performance)
    store.write_json("metrics", {name: asdict(metrics[name]) for name in sorted(metrics)})
    store.finalize(
        (
            "preregistered_job_table.json",
            "initial_conditions.npz",
            "per_seed_endpoints.json",
            "backend_provenance.json",
            "parity_matrix.json",
            "performance_records.json",
            "metrics.json",
        )
    )
    return GaussianFixedRayExperimentResult(
        run_dir=store.run_dir,
        config_hash=store.config_hash,
        status="inconclusive",
        metrics=MappingProxyType(dict(metrics)),
        arrays=MappingProxyType(dict(arrays)),
    )


__all__ = [
    "GaussianFixedRayExperimentResult",
    "build_confirmatory_gate_record",
    "build_cuda_gate_record",
    "capture_idle_gpu_gate",
    "publish_confirmatory_experiment",
    "publish_cuda_sentinel",
    "run_confirmatory_job",
    "run_confirmatory_holdout",
    "run_confirmatory_primary",
    "run_cuda_sentinel",
    "run_gaussian_fixed_ray_experiment",
]
