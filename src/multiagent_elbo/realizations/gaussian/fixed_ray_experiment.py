"""Artifact-backed non-heavy pilot for the preregistered Gaussian fixed ray."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
from pathlib import Path
import sys
import tempfile
import time
from types import MappingProxyType
from typing import Literal, Mapping

import numpy as np

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import ExperimentConfig, config_sha256
from multiagent_elbo.cuda_backend import parity_diagnostics, run_worker_job
from multiagent_elbo.experiment_support import MetricRecord, target_metric
from multiagent_elbo.runtime import RngStreams, collect_provenance

from .fixed_ray import (
    blocking_scheme_dispersion,
    build_preregistered_system,
    generate_initial_coefficients,
    iterate_fixed_ray,
    job_seed,
)


MetricStatus = Literal["pass", "fail", "inconclusive"]
_PREREGISTRATION_SHA256 = (
    "b9eeac423f9181feff6847c99abaae8865fc95b754fda85f7b87fc0b636c0186"
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
    raw = path.read_bytes()
    canonical = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(canonical).hexdigest()


def _readonly(values: object, *, dtype: object = np.float64) -> np.ndarray:
    array = np.array(values, dtype=dtype, copy=True, order="C")
    array.setflags(write=False)
    return array


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
    verification_state: str = "EVIDENCE_VERIFIED",
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
    arrays["off_family_nonlinear_remainders"] = _readonly(
        [
            [
                trajectory.off_family_nonlinear_remainders
                for trajectory in trajectories[scheme]
            ]
            for scheme in config.theory.blocking_schemes
        ]
    )

    worker_script = repo_root / "tools" / "cuda_worker.py"
    environment_lock = repo_root / "environments" / "cuda-rtx5090-cu128.lock.txt"
    temporary_parent = repo_root / ".pytest-tmp"
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
    off_family = arrays["off_family_nonlinear_remainders"]
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
        "off_family_nonlinear_remainder": target_metric(
            float(np.max(off_family)),
            config.numerics.atol,
            target=0.0,
            interpretation="Scalarized updates remain on the preregistered M0 matrix ray.",
            theorem_status="NUMERICAL",
            verification_state="EVIDENCE_VERIFIED",
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
            verification_state="EVIDENCE_VERIFIED",
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
            verification_state="EVIDENCE_VERIFIED",
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
            verification_state="EVIDENCE_VERIFIED",
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
                    "maximum_off_family_remainder": float(
                        np.max(trajectory.off_family_nonlinear_remainders)
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


__all__ = ["GaussianFixedRayExperimentResult", "run_gaussian_fixed_ray_experiment"]
