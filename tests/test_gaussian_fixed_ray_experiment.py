from __future__ import annotations

from dataclasses import replace
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from types import SimpleNamespace

import numpy as np
import pytest

from multiagent_elbo.config import ExperimentConfig, config_sha256
from multiagent_elbo.realizations.gaussian.fixed_ray_experiment import (
    GaussianFixedRayExperimentResult,
    _run_or_resume_worker_job,
    _validate_cuda_gate_bindings,
    capture_idle_gpu_gate,
    publish_cuda_sentinel,
    run_cuda_sentinel,
    run_gaussian_fixed_ray_experiment,
)


def fixed_ray_config(
    root: Path, *, name: str = "Gaussian fixed ray pilot"
) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": name, "seed": 20260809},
        {
            "experiment": "gaussian_fixed_ray",
            "fixture": "gaussian_fixed_ray_v1",
            "preregistration": "2026-08-09-gaussian-fixed-ray-v1",
            "blocking_schemes": ["adjacent_pairs", "balanced_alternating"],
            "matrix_dimension": 2,
        },
        {
            "dtype": "float64",
            "atol": 1e-12,
            "rtol": 1e-10,
            "min_spd_rcond": 1e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(root),
            "collect_diagnostics": True,
            "render_figures": False,
        },
        {
            "backend": "cpu",
            "dtype": "float64",
            "device_index": 0,
            "batch_size": 3,
            "deterministic": True,
            "allow_tf32": False,
            "cpu_cuda_parity": True,
            "cuda_worker_python": str(Path(sys.executable).resolve()),
            "heavy_sweep_enabled": False,
        },
    )


def test_pilot_publishes_recomputable_artifacts_with_incomplete_cuda_gate(
    tmp_path: Path,
):
    result = run_gaussian_fixed_ray_experiment(fixed_ray_config(tmp_path))

    assert isinstance(result, GaussianFixedRayExperimentResult)
    assert result.status == "inconclusive"
    expected_artifacts = {
        "preregistered_job_table.json",
        "initial_conditions.npz",
        "per_seed_endpoints.json",
        "backend_provenance.json",
        "parity_matrix.json",
        "performance_records.json",
        "metrics.json",
    }
    assert expected_artifacts <= {path.name for path in result.run_dir.iterdir()}

    required_metrics = {
        "projective_ray_angle",
        "normalized_coupling_distance",
        "scalarized_ray_construction_residual",
        "retained_beta_residual",
        "basin_exit_rate",
        "blocking_scheme_dispersion",
        "cpu_cuda_parity_residual",
    }
    assert required_metrics <= set(result.metrics)
    assert all(metric.theorem_status.isupper() for metric in result.metrics.values())
    assert all(
        metric.claim_origin in {"PROJECT_NOVEL", "APPLICATION_SPECIFIC"}
        for metric in result.metrics.values()
    )
    assert all(
        metric.verification_state in {"CANDIDATE", "INCONCLUSIVE"}
        for metric in result.metrics.values()
    )
    assert result.metrics["cpu_cuda_parity_residual"].status == "inconclusive"
    assert result.metrics["cpu_cuda_parity_residual"].theorem_status == "OPEN"
    assert result.metrics["cpu_cuda_parity_residual"].verification_state == "INCONCLUSIVE"
    assert result.metrics["retained_beta_residual"].interpretation.startswith(
        "Pilot norm"
    )
    assert result.metrics["retained_beta_residual_signed_max"].value > 0.0
    assert result.metrics["retained_beta_residual_signed_min"].value < 0.0
    assert result.metrics["noncommuting_scheme_control"].value == pytest.approx(0.01)
    assert result.metrics["noncommuting_scheme_control"].status == "pass"
    assert result.metrics["commuting_mutation_control"].value == pytest.approx(0.0)
    assert result.metrics["commuting_mutation_control"].status == "pass"

    job_table = json.loads(
        (result.run_dir / "preregistered_job_table.json").read_text(encoding="utf-8")
    )
    assert len(job_table["jobs"]) == 44
    assert [job["job_id"] for job in job_table["executed_pilot_jobs"]] == [
        "P001",
        "P002",
        "P003",
        "P004",
    ]
    assert job_table["heavy_sweep_enabled"] is False
    assert job_table["confirmatory_executed"] is False

    backend = json.loads(
        (result.run_dir / "backend_provenance.json").read_text(encoding="utf-8")
    )
    assert backend["controller_cpu"]["effective_backend"] == "cpu"
    assert backend["controller_cpu"]["effective_dtype"] == "float64"
    assert backend["worker_cpu"]["effective_backend"] == "cpu"
    assert backend["worker_cpu"]["effective_dtype"] == "float64"
    assert backend["worker_cpu"]["environment_sha256"]
    assert backend["worker_cpu"]["output_identity"]
    assert backend["worker_cuda"]["status"] == "not_requested_cpu_pilot"
    assert backend["worker_cuda"]["evidence_state"] == (
        "INCONCLUSIVE_NOT_REQUESTED_CPU_PILOT"
    )
    assert "operator_opt_in" not in backend["worker_cuda"]

    parity = json.loads(
        (result.run_dir / "parity_matrix.json").read_text(encoding="utf-8")
    )
    assert parity["controller_cpu_vs_worker_cpu"]["passed"] is True
    assert parity["controller_cpu_vs_worker_cuda"]["status"] == "inconclusive"
    assert parity["controller_cpu_vs_worker_cuda"]["reason"] == (
        "CUDA was not requested by the ordinary CPU pilot."
    )
    assert parity["mutation_negative_control"]["passed"] is False
    manifest = json.loads(
        (result.run_dir / "manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["provenance"]["cuda_evidence_state"] == (
        "INCONCLUSIVE_NOT_REQUESTED_CPU_PILOT"
    )
    serialized_cuda_state = json.dumps(
        {
            "backend": backend["worker_cuda"],
            "controller_cuda_parity": parity["controller_cpu_vs_worker_cuda"],
            "worker_cuda_parity": parity["worker_cpu_vs_worker_cuda"],
            "provenance": manifest["provenance"]["cuda_evidence_state"],
        },
        sort_keys=True,
    ).lower()
    assert "busy" not in serialized_cuda_state
    assert "idle" not in serialized_cuda_state

    arrays = np.load(result.run_dir / "initial_conditions.npz", allow_pickle=False)
    assert arrays["initial_coefficients"].shape == (4, 6)
    assert arrays["adjacent_pairs_coefficients"].shape == (4, 9, 6)
    assert arrays["balanced_alternating_coefficients"].shape == (4, 9, 6)
    assert arrays["adjacent_pairs_projective_angles"].shape == (4, 9)
    assert arrays["balanced_alternating_retained_beta_residuals"].shape == (4, 8)
    assert arrays["balanced_alternating_retained_beta_residual_vectors"].shape == (
        4,
        8,
        6,
    )
    assert arrays["blocking_scheme_dispersion"].shape == (4, 9)
    np.testing.assert_allclose(
        arrays["scalarized_ray_construction_residuals"],
        0.0,
        rtol=0.0,
        atol=1.0e-12,
    )


def test_cpu_worker_temporary_files_stay_under_configured_output_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import multiagent_elbo.realizations.gaussian.fixed_ray_experiment as experiment

    output_root = tmp_path / "configured-output"
    checkout_worker_root = Path(__file__).resolve().parents[1] / ".pytest-tmp"
    observed_work_roots: list[Path] = []
    real_run_worker_job = experiment.run_worker_job

    def recording_run_worker_job(**kwargs):
        observed_work_roots.append(Path(kwargs["work_root"]).resolve())
        return real_run_worker_job(**kwargs)

    monkeypatch.setattr(experiment, "run_worker_job", recording_run_worker_job)

    result = experiment.run_gaussian_fixed_ray_experiment(
        fixed_ray_config(output_root)
    )

    assert len(observed_work_roots) == 1
    worker_root = observed_work_roots[0]
    assert worker_root.parent.parent == output_root.resolve()
    assert worker_root.parent.parent != checkout_worker_root.resolve()
    backend = json.loads(
        (result.run_dir / "backend_provenance.json").read_text(encoding="utf-8")
    )
    assert Path(backend["worker_cpu"]["python_executable"]).resolve() == Path(
        sys.executable
    ).resolve()
def worker_execution_context() -> dict[str, object]:
    accepted_gate_record = {
        "schema_version": "accepted-test-gate-v1",
        "source_identity": {"git_revision": "d" * 40},
        "config_sha256": "c" * 64,
        "preregistration_sha256": "e" * 64,
        "environment_lock_identity": {"sha256": "f" * 64},
        "worker_python_identity": {"sha256": "1" * 64},
        "worker_script_identity": {"sha256": "2" * 64},
        "preflight": {"torch_version": "test"},
    }
    recheck_record = {"schema_version": "recheck-test-gate-v1"}

    def digest(record: object) -> str:
        return hashlib.sha256(
            json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

    return {
        "accepted_gate_sha256": digest(accepted_gate_record),
        "accepted_gate_record": accepted_gate_record,
        "operator_gate_recheck_sha256": digest(recheck_record),
        "operator_gate_recheck_record": recheck_record,
        "sentinel_job_id": "sentinel.C001.adjacent_pairs.step01.worker_cpu",
        "scheme": "adjacent_pairs",
        "step": 1,
        "lane": "worker_cpu",
        "config_sha256": "c" * 64,
        "source_revision": "d" * 40,
    }


def test_idle_gpu_gate_requires_operator_opt_in_before_inspection(
    monkeypatch: pytest.MonkeyPatch,
):
    def forbidden_run(*_: object, **__: object) -> object:
        raise AssertionError("GPU inspection ran before operator opt-in")

    monkeypatch.setattr(subprocess, "run", forbidden_run)
    with pytest.raises(ValueError, match="operator opt-in"):
        capture_idle_gpu_gate(operator_opt_in=False, sample_count=1)


def test_idle_gpu_gate_rejects_observed_utilization(monkeypatch: pytest.MonkeyPatch):
    responses = iter(
        (
            subprocess.CompletedProcess(
                args=[],
                returncode=0,
                stdout=(
                    "0, NVIDIA GeForce RTX 5090, GPU-test, 576.88, P2, "
                    "7, 1500, 32607, 40\n"
                ),
                stderr="",
            ),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        )
    )
    monkeypatch.setattr(subprocess, "run", lambda *_args, **_kwargs: next(responses))

    with pytest.raises(RuntimeError, match="not idle"):
        capture_idle_gpu_gate(operator_opt_in=True, sample_count=1)


def test_idle_gpu_gate_records_zero_utilization_and_active_processes(
    monkeypatch: pytest.MonkeyPatch,
):
    responses = iter(
        (
            subprocess.CompletedProcess(
                args=[],
                returncode=0,
                stdout=(
                    "0, NVIDIA GeForce RTX 5090, GPU-test, 576.88, P8, "
                    "0, 1129, 32607, 31\n"
                ),
                stderr="",
            ),
            subprocess.CompletedProcess(
                args=[],
                returncode=0,
                stdout="GPU-test, 12956, C:\\anaconda\\python.exe, [N/A]\n",
                stderr="",
            ),
        )
    )
    monkeypatch.setattr(subprocess, "run", lambda *_args, **_kwargs: next(responses))

    gate = capture_idle_gpu_gate(operator_opt_in=True, sample_count=1)

    assert gate["schema_version"] == "cuda-idle-operator-gate-v1"
    assert gate["expires_at_utc"] > gate["captured_at_utc"]
    assert gate["operator_opt_in"] is True
    assert gate["idle_observation_passed"] is True
    assert gate["samples"][0]["utilization_gpu_percent"] == 0
    assert gate["active_compute_processes"][0]["pid"] == 12956


def test_cuda_sentinel_runs_five_frozen_jobs_through_three_float64_lanes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    config = fixed_ray_config(tmp_path / "artifacts")
    config = replace(
        config,
        compute=replace(config.compute, backend="cuda", heavy_sweep_enabled=False),
    )
    gate = {
        "schema_version": "cuda-idle-operator-gate-v1",
        "captured_at_utc": "2099-01-01T00:00:00+00:00",
        "expires_at_utc": "2099-01-01T00:05:00+00:00",
        "operator_opt_in": True,
        "operator_process_acceptance_pending": True,
        "idle_observation_passed": True,
        "source_identity": {"git_revision": "f" * 40},
        "config_sha256": config_sha256(config),
        "samples": [
            {
                "uuid": "GPU-test",
                "utilization_gpu_percent": 0,
                "memory_used_mib": 1129,
            }
        ],
        "active_compute_processes": [
            {
                "gpu_uuid": "GPU-test",
                "pid": 12956,
                "process_name": r"C:\anaconda\python.exe",
                "used_gpu_memory_mib": None,
            }
        ],
    }
    gate_captures = []

    def capture_after_cuda_cooldown(**kwargs: object) -> dict[str, object]:
        gate_captures.append(kwargs)
        if len(gate_captures) == 1:
            raise RuntimeError("GPU is not idle across the required occupancy samples")
        return dict(gate)

    monkeypatch.setattr(
        "multiagent_elbo.realizations.gaussian.fixed_ray_experiment.capture_idle_gpu_gate",
        capture_after_cuda_cooldown,
    )
    monkeypatch.setattr(
        "multiagent_elbo.realizations.gaussian.fixed_ray_experiment.time.sleep",
        lambda _seconds: None,
    )
    monkeypatch.setattr(
        "multiagent_elbo.realizations.gaussian.fixed_ray_experiment._validate_cuda_gate_bindings",
        lambda *_args, **_kwargs: None,
    )
    calls = []

    def fake_worker_job(**kwargs: object) -> object:
        calls.append(kwargs)
        Path(kwargs["work_root"]).mkdir(parents=True)
        arrays = kwargs["arrays"]
        updated = arrays["coefficients"] @ arrays["spatial_map"].T
        backend = kwargs["requested_backend"]
        job_id = kwargs["job_id"]
        return SimpleNamespace(
            arrays={"updated_coefficients": updated},
            provenance={
                "effective_backend": backend,
                "effective_dtype": "float64",
                "peak_allocated_bytes": 0,
                "peak_reserved_bytes": 0,
            },
            request_manifest={"job_id": job_id, "requested_backend": backend},
            response_manifest={
                "job_id": job_id,
                "effective_backend": backend,
                "output_identity": f"identity-{job_id}",
            },
        )

    monkeypatch.setattr(
        "multiagent_elbo.realizations.gaussian.fixed_ray_experiment.run_worker_job",
        fake_worker_job,
    )

    sentinel = run_cuda_sentinel(
        config,
        operator_opt_in=True,
        operator_gate=gate,
        accepted_gate_sha256=hashlib.sha256(
            json.dumps(gate, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        work_root=tmp_path / "sentinel-worker-jobs",
        sample_count=5,
    )

    assert sentinel["schema_version"] == "gaussian-fixed-ray-cuda-sentinel-v1"
    assert sentinel["sentinel_job_ids"] == ["C001", "C015", "C030", "H001", "H010"]
    assert set(sentinel["scientific_analysis_eligibility"].values()) == {False}
    assert sentinel["all_parity_passed"] is True
    assert sentinel["scientific_decision_parity_passed"] is True
    assert len(sentinel["endpoint_parity_records"]) == 10
    assert sentinel["stratum_decision_parity"]["passed"] is True
    assert sentinel["threshold_mutation_negative_control"][
        "negative_control_passed"
    ] is True
    assert sentinel["mutation_negative_control"]["passed"] is False
    assert len(gate_captures) == 6
    assert len(sentinel["operator_gate_rechecks"]) == 5
    assert sentinel["operator_gate_rechecks"][0]["gate"]["idle_wait_attempts"] == 2
    assert sentinel["operator_gate_rechecks"][0]["gate"]["idle_wait_seconds"] == 1.0
    assert len(sentinel["worker_jobs"]) == 240
    assert len(calls) == 240
    assert all(call["arrays"]["coefficients"].shape == (1, 6) for call in calls)
    assert sum(call["requested_backend"] == "cpu" for call in calls) == 80
    assert sum(call["requested_backend"] == "cuda" for call in calls) == 160
    assert {call["requested_backend"] for call in calls} == {"cpu", "cuda"}
    for scheme in config.theory.blocking_schemes:
        for lane in (
            "controller_cpu",
            "worker_cpu",
            "worker_cuda",
            "worker_cuda_repeat",
        ):
            assert sentinel["trajectories"][scheme][lane].shape == (5, 9, 6)


def test_worker_trajectory_job_resumes_only_from_validated_immutable_artifacts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    from multiagent_elbo.realizations.gaussian.fixed_ray import (
        build_preregistered_system,
        generate_initial_coefficients,
    )

    repository = Path(__file__).resolve().parents[1]
    system = build_preregistered_system()
    kwargs = {
        "worker_python": Path(r"C:\anaconda\python.exe"),
        "worker_script": repository / "tools" / "cuda_worker.py",
        "work_root": tmp_path / "resume-job",
        "job_id": "sentinel.C001.adjacent_pairs.step01.worker_cpu",
        "requested_backend": "cpu",
        "requested_dtype": "float64",
        "arrays": {
            "coefficients": generate_initial_coefficients(
                202608090101, "C001"
            )[None, :],
            "spatial_map": system.spatial_maps["adjacent_pairs"],
            "matrix_direction": system.matrix_direction,
            "batch_size": np.array(1, dtype=np.int64),
        },
        "environment_lock": repository
        / "environments"
        / "cuda-rtx5090-cu128.lock.txt",
        "execution_context": worker_execution_context(),
    }
    first, first_context = _run_or_resume_worker_job(**kwargs)
    monkeypatch.setattr(
        "multiagent_elbo.realizations.gaussian.fixed_ray_experiment.run_worker_job",
        lambda **_: (_ for _ in ()).throw(AssertionError("resume reran worker")),
    )

    resumed, resumed_context = _run_or_resume_worker_job(**kwargs)

    np.testing.assert_array_equal(
        first.arrays["updated_coefficients"],
        resumed.arrays["updated_coefficients"],
    )
    assert first.provenance == resumed.provenance
    assert first_context == resumed_context
    assert first_context["operator_gate_recheck_sha256"] == kwargs[
        "execution_context"
    ]["operator_gate_recheck_sha256"]
    assert first_context["outer_attempt"] == 1
    assert (kwargs["work_root"] / "attempt-1" / "provenance.json").is_file()


def test_interrupted_worker_exchange_uses_one_context_bound_outer_retry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import multiagent_elbo.realizations.gaussian.fixed_ray_experiment as module
    from multiagent_elbo.realizations.gaussian.fixed_ray import build_preregistered_system

    repository = Path(__file__).resolve().parents[1]
    system = build_preregistered_system()
    original_worker = module.run_worker_job
    kwargs = {
        "worker_python": Path(r"C:\anaconda\python.exe"),
        "worker_script": repository / "tools" / "cuda_worker.py",
        "work_root": tmp_path / "retry-job",
        "job_id": "sentinel.C001.adjacent_pairs.step01.worker_cpu",
        "requested_backend": "cpu",
        "requested_dtype": "float64",
        "arrays": {
            "coefficients": np.ones((1, 6), dtype=np.float64),
            "spatial_map": system.spatial_maps["adjacent_pairs"],
            "matrix_direction": system.matrix_direction,
            "batch_size": np.array(1, dtype=np.int64),
        },
        "environment_lock": repository
        / "environments"
        / "cuda-rtx5090-cu128.lock.txt",
        "execution_context": worker_execution_context(),
    }

    def interrupted(**call: object) -> object:
        attempt_root = Path(call["work_root"])
        attempt_root.mkdir(parents=True)
        (attempt_root / "partial.txt").write_text("interrupted", encoding="utf-8")
        raise RuntimeError("simulated infrastructure interruption")

    monkeypatch.setattr(module, "run_worker_job", interrupted)
    with pytest.raises(RuntimeError, match="simulated"):
        _run_or_resume_worker_job(**kwargs)
    monkeypatch.setattr(module, "run_worker_job", original_worker)

    _result, context = _run_or_resume_worker_job(**kwargs)

    assert context["outer_attempt"] == 2
    assert context["parent_attempt"] == 1
    assert (kwargs["work_root"] / "attempt-1" / "partial.txt").is_file()
    assert (kwargs["work_root"] / "attempt-2" / "provenance.json").is_file()


def test_context_only_interruption_consumes_first_outer_attempt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import multiagent_elbo.realizations.gaussian.fixed_ray_experiment as module
    from multiagent_elbo.realizations.gaussian.fixed_ray import build_preregistered_system

    repository = Path(__file__).resolve().parents[1]
    system = build_preregistered_system()
    original_worker = module.run_worker_job
    work_root = tmp_path / "context-only-retry"
    kwargs = {
        "worker_python": Path(r"C:\anaconda\python.exe"),
        "worker_script": repository / "tools" / "cuda_worker.py",
        "work_root": work_root,
        "job_id": "sentinel.C001.adjacent_pairs.step01.worker_cpu",
        "requested_backend": "cpu",
        "requested_dtype": "float64",
        "arrays": {
            "coefficients": np.ones((1, 6), dtype=np.float64),
            "spatial_map": system.spatial_maps["adjacent_pairs"],
            "matrix_direction": system.matrix_direction,
            "batch_size": np.array(1, dtype=np.int64),
        },
        "environment_lock": repository
        / "environments"
        / "cuda-rtx5090-cu128.lock.txt",
        "execution_context": worker_execution_context(),
    }

    monkeypatch.setattr(
        module,
        "run_worker_job",
        lambda **_: (_ for _ in ()).throw(RuntimeError("pre-worker interruption")),
    )
    with pytest.raises(RuntimeError, match="pre-worker interruption"):
        _run_or_resume_worker_job(**kwargs)
    assert (work_root / "attempt-1-context.json").is_file()
    assert not (work_root / "attempt-1").exists()

    monkeypatch.setattr(module, "run_worker_job", original_worker)
    _result, context = _run_or_resume_worker_job(**kwargs)

    assert context["outer_attempt"] == 2
    assert context["parent_attempt"] == 1
    assert (work_root / "attempt-2" / "provenance.json").is_file()


def test_resumed_worker_exchange_rejects_tampered_execution_context(tmp_path: Path):
    from multiagent_elbo.realizations.gaussian.fixed_ray import build_preregistered_system

    repository = Path(__file__).resolve().parents[1]
    system = build_preregistered_system()
    work_root = tmp_path / "tampered-context"
    kwargs = {
        "worker_python": Path(r"C:\anaconda\python.exe"),
        "worker_script": repository / "tools" / "cuda_worker.py",
        "work_root": work_root,
        "job_id": "sentinel.C001.adjacent_pairs.step01.worker_cpu",
        "requested_backend": "cpu",
        "requested_dtype": "float64",
        "arrays": {
            "coefficients": np.ones((1, 6), dtype=np.float64),
            "spatial_map": system.spatial_maps["adjacent_pairs"],
            "matrix_direction": system.matrix_direction,
            "batch_size": np.array(1, dtype=np.int64),
        },
        "environment_lock": repository
        / "environments"
        / "cuda-rtx5090-cu128.lock.txt",
        "execution_context": worker_execution_context(),
    }
    _run_or_resume_worker_job(**kwargs)
    context_path = work_root / "attempt-1-context.json"
    context = json.loads(context_path.read_text(encoding="utf-8"))
    context["accepted_gate_sha256"] = "0" * 64
    context_path.write_text(json.dumps(context), encoding="utf-8")

    with pytest.raises(RuntimeError, match="gate digest drifted"):
        _run_or_resume_worker_job(**kwargs)


@pytest.mark.parametrize("field", ["config_sha256", "source_revision"])
def test_resumed_worker_exchange_rejects_current_scientific_identity_drift(
    tmp_path: Path, field: str
):
    from multiagent_elbo.realizations.gaussian.fixed_ray import build_preregistered_system

    repository = Path(__file__).resolve().parents[1]
    system = build_preregistered_system()
    work_root = tmp_path / f"current-{field}-drift"
    arrays = {
        "coefficients": np.ones((1, 6), dtype=np.float64),
        "spatial_map": system.spatial_maps["adjacent_pairs"],
        "matrix_direction": system.matrix_direction,
        "batch_size": np.array(1, dtype=np.int64),
    }
    context = worker_execution_context()
    kwargs = {
        "worker_python": Path(r"C:\anaconda\python.exe"),
        "worker_script": repository / "tools" / "cuda_worker.py",
        "work_root": work_root,
        "job_id": "sentinel.C001.adjacent_pairs.step01.worker_cpu",
        "requested_backend": "cpu",
        "requested_dtype": "float64",
        "arrays": arrays,
        "environment_lock": repository
        / "environments"
        / "cuda-rtx5090-cu128.lock.txt",
        "execution_context": context,
    }
    _run_or_resume_worker_job(**kwargs)
    changed = worker_execution_context()
    if field == "config_sha256":
        changed[field] = "9" * 64
        changed_gate = dict(changed["accepted_gate_record"])
        changed_gate["config_sha256"] = changed[field]
    else:
        changed[field] = "8" * 40
        changed_gate = dict(changed["accepted_gate_record"])
        changed_gate["source_identity"] = {"git_revision": changed[field]}
    changed["accepted_gate_record"] = changed_gate
    changed["accepted_gate_sha256"] = hashlib.sha256(
        json.dumps(changed_gate, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    with pytest.raises(RuntimeError, match="scientific identity drifted"):
        _run_or_resume_worker_job(**{**kwargs, "execution_context": changed})


def test_cuda_sentinel_publishes_manifest_bound_runstore_bundle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    config = fixed_ray_config(tmp_path / "artifacts", name="cuda-sentinel-bundle")
    config = replace(
        config,
        compute=replace(config.compute, backend="cuda", heavy_sweep_enabled=False),
    )
    gate = {
        "schema_version": "cuda-idle-operator-gate-v1",
        "captured_at_utc": "2099-01-01T00:00:00+00:00",
        "expires_at_utc": "2099-01-01T00:05:00+00:00",
        "operator_opt_in": True,
        "operator_process_acceptance_pending": True,
        "idle_observation_passed": True,
    }
    gate_digest = hashlib.sha256(
        json.dumps(gate, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    fake = {
        "schema_version": "gaussian-fixed-ray-cuda-sentinel-v1",
        "operator_gate": gate,
        "operator_gate_sha256": gate_digest,
        "accepted_gate_sha256": gate_digest,
        "all_parity_passed": True,
        "scientific_decision_parity_passed": True,
        "worker_jobs": [{"job_id": "sentinel.fake"}],
        "trajectories": {
            "adjacent_pairs": {
                "controller_cpu": np.ones((5, 9, 6)),
                "worker_cpu": np.ones((5, 9, 6)),
                "worker_cuda": np.ones((5, 9, 6)),
                "worker_cuda_repeat": np.ones((5, 9, 6)),
            }
        },
    }
    monkeypatch.setattr(
        "multiagent_elbo.realizations.gaussian.fixed_ray_experiment.run_cuda_sentinel",
        lambda *_args, **_kwargs: fake,
    )

    result = publish_cuda_sentinel(
        config,
        operator_opt_in=True,
        operator_gate=gate,
        accepted_gate_sha256=gate_digest,
        staging_root=tmp_path / "staging",
    )

    assert result.status == "pass"
    expected = {
        "cuda_gate.json",
        "preregistered_job_table.json",
        "sentinel_parity.json",
        "sentinel_arrays.npz",
        "worker_exchange_index.json",
        "metrics.json",
        "manifest.json",
    }
    assert expected <= {path.name for path in result.run_dir.iterdir()}
    manifest = json.loads((result.run_dir / "manifest.json").read_text("utf-8"))
    assert manifest["provenance"]["input_hashes"]["operator_gate_sha256"] == gate_digest
    artifact_hashes = manifest["provenance"]["artifact_sha256"]
    assert set(artifact_hashes) == (expected | {"config.json"}) - {"manifest.json"}
    assert all(
        hashlib.sha256((result.run_dir / name).read_bytes()).hexdigest() == digest
        for name, digest in artifact_hashes.items()
    )


def test_published_sentinel_schema_is_admitted_by_confirmatory_validator(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import multiagent_elbo.realizations.gaussian.fixed_ray_experiment as experiment

    sentinel_config = fixed_ray_config(tmp_path / "artifacts", name="sentinel-admission")
    sentinel_config = replace(
        sentinel_config,
        compute=replace(
            sentinel_config.compute, backend="cuda", heavy_sweep_enabled=False
        ),
    )
    confirmatory_config = replace(
        sentinel_config,
        compute=replace(sentinel_config.compute, heavy_sweep_enabled=True),
    )
    repository = Path(__file__).resolve().parents[1]
    environment_lock = repository / "environments" / "cuda-rtx5090-cu128.lock.txt"
    worker_script = repository / "tools" / "cuda_worker.py"
    common = {
        "source_identity": {
            "git_revision": "a" * 40,
            "tracked_worktree_clean": True,
        },
        "preregistration_sha256": experiment._PREREGISTRATION_SHA256,
        "environment_lock_identity": {
            "path": str(environment_lock),
            "sha256": experiment._file_sha256(environment_lock),
        },
        "worker_python_identity": {"path": "python", "sha256": "c" * 64},
        "worker_script_identity": {
            "path": str(worker_script),
            "sha256": experiment._file_sha256(worker_script),
        },
        "preflight": {"effective_backend": "cuda", "effective_dtype": "float64"},
    }
    sentinel_gate = {
        "schema_version": "cuda-idle-operator-gate-v1",
        "operator_opt_in": True,
        "idle_observation_passed": True,
        "config_sha256": config_sha256(sentinel_config),
        **common,
    }
    sentinel_gate_sha256 = experiment._record_sha256(sentinel_gate)
    confirmatory_gate = {
        "schema_version": "cuda-confirmatory-operator-gate-v1",
        "operator_opt_in": True,
        "idle_observation_passed": True,
        "config_sha256": config_sha256(confirmatory_config),
        **common,
    }
    sentinel_ids = ["C001", "C015", "C030", "H001", "H010"]
    rechecks = []
    recheck_digests = []
    for sentinel_id in sentinel_ids:
        gate = {"schema_version": "cuda-idle-operator-gate-v1", "job": sentinel_id}
        digest = experiment._record_sha256(gate)
        rechecks.append({"sentinel_job_id": sentinel_id, "gate_sha256": digest, "gate": gate})
        recheck_digests.append(digest)
    comparison_ids = (
        "controller_cpu_vs_worker_cpu",
        "controller_cpu_vs_worker_cuda",
        "controller_cpu_vs_worker_cuda_repeat",
        "worker_cpu_vs_worker_cuda",
        "worker_cuda_repeatability",
    )
    parity_records = [
        {
            "sentinel_job_id": sentinel_id,
            "scheme": scheme,
            "step": step,
            "comparisons": {name: {"passed": True} for name in comparison_ids},
        }
        for sentinel_id in sentinel_ids
        for scheme in ("adjacent_pairs", "balanced_alternating")
        for step in range(1, 9)
    ]
    worker_jobs = [
        {
            "job_id": f"sentinel.{sentinel_id}.{scheme}.step{step:02d}.{lane}",
            "sentinel_job_id": sentinel_id,
            "scheme": scheme,
            "step": step,
            "lane": lane,
            "execution_context": {
                "accepted_gate_sha256": sentinel_gate_sha256,
                "accepted_gate_record": sentinel_gate,
                "operator_gate_recheck_sha256": recheck_digests[job_index],
                "operator_gate_recheck_record": rechecks[job_index]["gate"],
                "sentinel_job_id": sentinel_id,
                "scheme": scheme,
                "step": step,
                "lane": lane,
                "config_sha256": config_sha256(sentinel_config),
                "source_revision": "a" * 40,
            },
            "request_manifest": {
                "job_id": f"sentinel.{sentinel_id}.{scheme}.step{step:02d}.{lane}",
                "requested_backend": "cpu" if lane == "worker_cpu" else "cuda",
            },
            "response_manifest": {},
            "provenance": {},
        }
        for job_index, sentinel_id in enumerate(sentinel_ids)
        for scheme in ("adjacent_pairs", "balanced_alternating")
        for step in range(1, 9)
        for lane in ("worker_cpu", "worker_cuda", "worker_cuda_repeat")
    ]
    trajectories = {
        scheme: {
            lane: np.ones((5, 9, 6), dtype=np.float64)
            for lane in (
                "controller_cpu",
                "worker_cpu",
                "worker_cuda",
                "worker_cuda_repeat",
            )
        }
        for scheme in ("adjacent_pairs", "balanced_alternating")
    }
    fake = {
        "schema_version": "gaussian-fixed-ray-cuda-sentinel-v1",
        "sentinel_job_ids": sentinel_ids,
        "scientific_analysis_eligibility": {job_id: False for job_id in sentinel_ids},
        "operator_gate": sentinel_gate,
        "operator_gate_sha256": sentinel_gate_sha256,
        "accepted_gate_sha256": sentinel_gate_sha256,
        "operator_gate_rechecks": rechecks,
        "all_parity_passed": True,
        "scientific_decision_parity_passed": True,
        "stratum_decision_parity": {"passed": True, "records": {}},
        "parity_records": parity_records,
        "endpoint_parity_records": [
            {
                "sentinel_job_id": sentinel_id,
                "scheme": scheme,
                "comparisons": {
                    lane: {"passed": True}
                    for lane in ("worker_cpu", "worker_cuda", "worker_cuda_repeat")
                },
            }
            for sentinel_id in sentinel_ids
            for scheme in ("adjacent_pairs", "balanced_alternating")
        ],
        "threshold_mutation_negative_control": {"negative_control_passed": True},
        "mutation_negative_control": {"passed": False},
        "worker_jobs": worker_jobs,
        "trajectories": trajectories,
    }
    monkeypatch.setattr(experiment, "run_cuda_sentinel", lambda *_args, **_kwargs: fake)
    monkeypatch.setattr(experiment, "_validate_gate_recheck", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(
        experiment, "validate_worker_protocol_manifest", lambda *_args, **_kwargs: None
    )
    monkeypatch.setattr(
        experiment, "validate_worker_provenance", lambda *_args, **_kwargs: None
    )
    monkeypatch.setattr(
        experiment,
        "collect_provenance",
        lambda *_args, **_kwargs: {
            "git_commit": "a" * 40,
            "git_dirty": False,
            "input_hashes": {},
        },
    )

    published = publish_cuda_sentinel(
        sentinel_config,
        operator_opt_in=True,
        operator_gate=sentinel_gate,
        accepted_gate_sha256=sentinel_gate_sha256,
        staging_root=tmp_path / "staging",
    )
    manifest_sha256 = hashlib.sha256(
        (published.run_dir / "manifest.json").read_bytes()
    ).hexdigest()

    identity = experiment._validate_confirmatory_sentinel_bundle(
        confirmatory_config,
        published.run_dir,
        manifest_sha256,
        confirmatory_gate,
    )

    assert identity["manifest_sha256"] == manifest_sha256
    assert identity["sentinel_job_ids"] == sentinel_ids


def test_click_launcher_gate_mode_publishes_digest_for_two_phase_acceptance(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repository = Path(__file__).resolve().parents[1]
    launcher_path = repository / "run_gaussian_fixed_ray_lab.py"
    spec = importlib.util.spec_from_file_location("fixed_ray_launcher", launcher_path)
    assert spec is not None and spec.loader is not None
    launcher = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(launcher)
    gate = {
        "schema_version": "cuda-idle-operator-gate-v1",
        "operator_opt_in": True,
        "operator_process_acceptance_pending": True,
        "processes_present": True,
    }
    gate_path = tmp_path / "cuda-gate.json"
    control_path = tmp_path / "operator-control.json"
    control_path.write_text(
        json.dumps(
            {
                "mode": "cuda_gate",
                "operator_opt_in": True,
                "accepted_gate_sha256": "",
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(launcher, "OPERATOR_CONTROL_PATH", control_path)
    monkeypatch.setattr(launcher, "CUDA_GATE_PATH", gate_path)
    monkeypatch.setattr(launcher, "build_cuda_gate_record", lambda *_args, **_kwargs: gate)

    published = launcher.main()

    assert published == gate
    assert json.loads(gate_path.read_text("utf-8")) == gate


def test_click_launcher_namespaces_sentinel_staging_by_accepted_gate_digest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repository = Path(__file__).resolve().parents[1]
    launcher_path = repository / "run_gaussian_fixed_ray_lab.py"
    spec = importlib.util.spec_from_file_location("fixed_ray_launcher", launcher_path)
    assert spec is not None and spec.loader is not None
    launcher = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(launcher)
    accepted_digest = "a" * 64
    gate = {"schema_version": "cuda-idle-operator-gate-v1"}
    gate_path = tmp_path / "cuda-gate.json"
    gate_path.write_text(json.dumps(gate), encoding="utf-8")
    control_path = tmp_path / "operator-control.json"
    control_path.write_text(
        json.dumps(
            {
                "mode": "cuda_sentinel",
                "operator_opt_in": True,
                "accepted_gate_sha256": accepted_digest,
            }
        ),
        encoding="utf-8",
    )
    staging_base = tmp_path / "sentinel-staging"
    captured = {}

    def publish(*_args: object, **kwargs: object) -> object:
        captured.update(kwargs)
        return SimpleNamespace(run_dir=tmp_path / "run", status="pass", metrics={})

    monkeypatch.setattr(launcher, "OPERATOR_CONTROL_PATH", control_path)
    monkeypatch.setattr(launcher, "CUDA_GATE_PATH", gate_path)
    monkeypatch.setattr(launcher, "SENTINEL_STAGING_ROOT", staging_base)
    monkeypatch.setattr(launcher, "publish_cuda_sentinel", publish)

    launcher.main()

    assert captured["staging_root"] == staging_base / accepted_digest


@pytest.mark.parametrize(
    "mutated_key",
    (
        "source_identity",
        "config_sha256",
        "preregistration_sha256",
        "environment_lock_identity",
        "worker_python_identity",
        "worker_script_identity",
        "preflight",
    ),
)
def test_cuda_gate_rejects_every_live_identity_mutation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mutated_key: str
):
    config = fixed_ray_config(tmp_path)
    config = replace(config, compute=replace(config.compute, backend="cuda"))
    live = {
        "source_identity": {"git_revision": "a" * 40, "tracked_worktree_clean": True},
        "config_sha256": "b" * 64,
        "preregistration_sha256": "c" * 64,
        "environment_lock_identity": {"path": "lock", "sha256": "d" * 64},
        "worker_python_identity": {"path": "python", "sha256": "e" * 64},
        "worker_script_identity": {"path": "worker", "sha256": "f" * 64},
        "preflight": {"device_name": "NVIDIA GeForce RTX 5090"},
    }
    monkeypatch.setattr(
        "multiagent_elbo.realizations.gaussian.fixed_ray_experiment._live_cuda_gate_bindings",
        lambda _config: live,
    )
    gate = dict(live)
    gate[mutated_key] = {"mutated": True}

    with pytest.raises(ValueError, match="identity drifted"):
        _validate_cuda_gate_bindings(config, gate)


def test_pilot_is_same_seed_deterministic_across_output_roots(tmp_path: Path):
    first = run_gaussian_fixed_ray_experiment(
        fixed_ray_config(tmp_path / "a", name="same")
    )
    second = run_gaussian_fixed_ray_experiment(
        fixed_ray_config(tmp_path / "b", name="same")
    )

    assert first.metrics == second.metrics
    assert first.arrays.keys() == second.arrays.keys()
    for name in first.arrays:
        np.testing.assert_array_equal(first.arrays[name], second.arrays[name])


def test_preregistration_identity_is_stable_across_git_text_line_endings(
    tmp_path: Path,
):
    repository = Path(__file__).resolve().parents[1]
    frozen_text = (
        repository
        / "docs"
        / "experiments"
        / "2026-08-09-gaussian-fixed-ray-preregistration.md"
    ).read_text(encoding="utf-8")
    crlf_preregistration = tmp_path / "frozen-crlf.md"
    crlf_preregistration.write_bytes(
        frozen_text.replace("\n", "\r\n").encode("utf-8")
    )

    result = run_gaussian_fixed_ray_experiment(
        fixed_ray_config(tmp_path / "output"),
        preregistration_path=crlf_preregistration,
    )

    assert result.status == "inconclusive"


def test_preregistration_validation_precedes_rng_worker_and_artifact_creation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    invalid_preregistration = tmp_path / "invalid.md"
    invalid_preregistration.write_text("not the frozen protocol", encoding="utf-8")
    output_root = tmp_path / "output"

    def forbidden_generation(*_: object, **__: object) -> object:
        raise AssertionError("scientific input generated before preregistration validation")

    def forbidden_worker(*_: object, **__: object) -> object:
        raise AssertionError("worker created before preregistration validation")

    monkeypatch.setattr(
        "multiagent_elbo.realizations.gaussian.fixed_ray_experiment.generate_initial_coefficients",
        forbidden_generation,
    )
    monkeypatch.setattr(
        "multiagent_elbo.realizations.gaussian.fixed_ray_experiment.run_worker_job",
        forbidden_worker,
    )
    with pytest.raises(ValueError, match="preregistration"):
        run_gaussian_fixed_ray_experiment(
            fixed_ray_config(output_root),
            preregistration_path=invalid_preregistration,
        )
    assert not output_root.exists()


def test_preregistration_digest_is_stable_across_windows_line_endings(tmp_path: Path):
    from multiagent_elbo.realizations.gaussian.fixed_ray_experiment import (
        _validate_preregistration,
    )

    repository = Path(__file__).resolve().parents[1]
    source = (
        repository
        / "docs"
        / "experiments"
        / "2026-08-09-gaussian-fixed-ray-preregistration.md"
    )
    canonical = source.read_bytes().replace(b"\r\n", b"\n")
    windows_copy = tmp_path / "preregistration-crlf.md"
    windows_copy.write_bytes(canonical.replace(b"\n", b"\r\n"))

    assert (
        _validate_preregistration(windows_copy)
        == "9e22f239be93ad574c46b5ce36846df2b6e61353b6a0852146df2f155600bde0"
    )


def test_preregistration_freezes_confirmatory_analysis_amendment(tmp_path: Path):
    from multiagent_elbo.realizations.gaussian.fixed_ray_experiment import (
        _validate_preregistration,
    )

    repository = Path(__file__).resolve().parents[1]
    preregistration = (
        repository
        / "docs"
        / "experiments"
        / "2026-08-09-gaussian-fixed-ray-preregistration.md"
    )
    source = preregistration.read_text(encoding="utf-8")
    assert "2026-08-09-gaussian-fixed-ray-v1a" in source
    for endpoint_id in (
        "construction_residual",
        "retained_beta_trend",
        "basin_exit_rate",
        "scheme_dispersion",
        "conditioning_trend",
        "rejection_rate",
    ):
        assert f"`{endpoint_id}`" in source
    assert _validate_preregistration(preregistration)

    mutated = tmp_path / "mutated.md"
    mutated.write_text(
        source.replace("exact one-sided sign test", "unspecified test", 1),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="frozen"):
        _validate_preregistration(mutated)


def test_gaussian_launcher_is_click_to_run_from_fresh_uninstalled_checkout(
    tmp_path: Path,
):
    repository = Path(__file__).resolve().parents[1]
    checkout = tmp_path / "fresh-checkout"
    checkout.mkdir()
    shutil.copy2(
        repository / "run_gaussian_fixed_ray_lab.py",
        checkout / "run_gaussian_fixed_ray_lab.py",
    )
    shutil.copytree(repository / "src", checkout / "src")
    shutil.copytree(repository / "Theory", checkout / "Theory")
    shutil.copytree(repository / "tools", checkout / "tools")
    (checkout / "docs" / "experiments").mkdir(parents=True)
    shutil.copy2(
        repository
        / "docs"
        / "experiments"
        / "2026-08-09-gaussian-fixed-ray-preregistration.md",
        checkout
        / "docs"
        / "experiments"
        / "2026-08-09-gaussian-fixed-ray-preregistration.md",
    )
    (checkout / "environments").mkdir()
    shutil.copy2(
        repository / "environments" / "cuda-rtx5090-cu128.lock.txt",
        checkout / "environments" / "cuda-rtx5090-cu128.lock.txt",
    )
    environment = {
        key: value
        for key, value in os.environ.items()
        if key not in {"PYTHONPATH", "PYTHONHOME"} and not key.startswith("PYTEST_")
    }

    completed = subprocess.run(
        [sys.executable, "run_gaussian_fixed_ray_lab.py"],
        cwd=checkout,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "run_dir=" in completed.stdout
    assert "status=inconclusive" in completed.stdout
    source = (checkout / "run_gaussian_fixed_ray_lab.py").read_text(encoding="utf-8")
    assert "import argparse" not in source
    assert "from click" not in source.lower()
    assert "import typer" not in source.lower()
