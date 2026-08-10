from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
from types import MappingProxyType, SimpleNamespace

import numpy as np
import pytest

import run_gaussian_fixed_ray_lab as launcher

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.realizations.gaussian import fixed_ray_experiment
from multiagent_elbo.realizations.gaussian.fixed_ray_experiment import (
    build_confirmatory_gate_record,
    publish_confirmatory_experiment,
    run_confirmatory_job,
    run_confirmatory_holdout,
    run_confirmatory_primary,
)


def confirmatory_config(output_root: Path) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": "gaussian-fixed-ray-confirmatory", "seed": 20260809},
        {
            "experiment": "gaussian_fixed_ray",
            "fixture": "gaussian_fixed_ray_v1",
            "preregistration": "2026-08-09-gaussian-fixed-ray-v1",
            "blocking_schemes": ["adjacent_pairs", "balanced_alternating"],
            "matrix_dimension": 2,
        },
        {
            "dtype": "float64",
            "atol": 1.0e-12,
            "rtol": 1.0e-10,
            "min_spd_rcond": 1.0e-12,
            "max_frame_condition": 1.0e6,
        },
        {"root": str(output_root), "collect_diagnostics": True, "render_figures": False},
        {
            "backend": "cuda",
            "dtype": "float64",
            "device_index": 0,
            "batch_size": 4096,
            "deterministic": True,
            "allow_tf32": False,
            "cpu_cuda_parity": True,
            "cuda_worker_python": str(Path(__file__).resolve()),
            "heavy_sweep_enabled": True,
        },
    )


def _idle_record(schema_version: str) -> dict[str, object]:
    now = datetime.now(timezone.utc)
    sample = {
        "timestamp_utc": now.isoformat(),
        "index": 0,
        "name": "fixture-gpu",
        "uuid": "GPU-fixture",
        "driver_version": "fixture",
        "pstate": "P8",
        "utilization_gpu_percent": 0,
        "memory_used_mib": 100,
        "memory_total_mib": 32_000,
        "temperature_c": 30,
    }
    return {
        "schema_version": schema_version,
        "captured_at_utc": now.isoformat(),
        "expires_at_utc": (now + timedelta(minutes=5)).isoformat(),
        "operator_opt_in": True,
        "operator_process_acceptance_pending": True,
        "idle_observation_passed": True,
        "samples": [sample],
        "active_compute_processes": [],
    }


def _digest(record: object) -> str:
    return hashlib.sha256(
        json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def test_confirmatory_gate_has_separate_heavy_execution_scope(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    config = confirmatory_config(tmp_path)
    bindings = {
        "source_identity": {"git_revision": "a" * 40, "tracked_worktree_clean": True},
        "config_sha256": "b" * 64,
        "preregistration_sha256": "c" * 64,
        "environment_lock_identity": {"path": "lock", "sha256": "d" * 64},
        "worker_python_identity": {"path": "python", "sha256": "e" * 64},
        "worker_script_identity": {"path": "worker", "sha256": "f" * 64},
        "preflight": {"effective_backend": "cuda", "effective_dtype": "float64"},
    }
    monkeypatch.setattr(fixed_ray_experiment, "_live_cuda_common_bindings", lambda _: bindings)
    monkeypatch.setattr(
        fixed_ray_experiment,
        "capture_idle_gpu_gate",
        lambda **_: _idle_record("cuda-idle-operator-gate-v1"),
    )

    gate = build_confirmatory_gate_record(config, operator_opt_in=True)

    assert gate["schema_version"] == "cuda-confirmatory-operator-gate-v1"
    assert gate["execution_scope"] == "gaussian_fixed_ray_confirmatory_40_job"
    assert gate["heavy_sweep_enabled"] is True
    assert gate["config_sha256"] == "b" * 64


def test_confirmatory_job_runs_two_schemes_eight_steps_after_one_idle_recheck(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    config = confirmatory_config(tmp_path)
    gate = _idle_record("cuda-confirmatory-operator-gate-v1")
    gate.update(
        {
            "execution_scope": "gaussian_fixed_ray_confirmatory_40_job",
            "heavy_sweep_enabled": True,
            "config_sha256": "b" * 64,
            "source_identity": {"git_revision": "a" * 40, "tracked_worktree_clean": True},
        }
    )
    accepted_gate_sha256 = _digest(gate)
    recheck = _idle_record("cuda-idle-operator-gate-v1")
    calls: list[dict[str, object]] = []

    monkeypatch.setattr(
        fixed_ray_experiment, "_validate_confirmatory_gate_bindings", lambda *_: None
    )
    monkeypatch.setattr(
        fixed_ray_experiment,
        "_capture_idle_gpu_gate_after_cooldown",
        lambda **_: recheck,
    )

    def fake_worker(**kwargs: object):
        arrays = kwargs["arrays"]
        assert isinstance(arrays, dict)
        updated = np.asarray(arrays["coefficients"]) @ np.asarray(
            arrays["spatial_map"]
        ).T
        calls.append(dict(kwargs))
        result = SimpleNamespace(
            arrays=MappingProxyType({"updated_coefficients": updated}),
            request_manifest=MappingProxyType({"job_id": kwargs["job_id"]}),
            response_manifest=MappingProxyType({"job_id": kwargs["job_id"]}),
            provenance=MappingProxyType(
                {"peak_allocated_bytes": 1024, "peak_reserved_bytes": 2048}
            ),
        )
        return result, MappingProxyType(dict(kwargs["execution_context"]))

    monkeypatch.setattr(fixed_ray_experiment, "_run_or_resume_worker_job", fake_worker)

    result = run_confirmatory_job(
        config,
        job={
            "job_id": "C001",
            "master_seed": 202608090101,
            "role": "confirmatory_primary",
            "schemes": ["adjacent_pairs", "balanced_alternating"],
            "steps": 8,
        },
        operator_opt_in=True,
        operator_gate=gate,
        accepted_gate_sha256=accepted_gate_sha256,
        work_root=tmp_path / "staging",
    )

    assert len(calls) == 16
    assert {call["requested_backend"] for call in calls} == {"cuda"}
    assert result["job_id"] == "C001"
    assert result["terminal_status"] == "completed"
    assert result["scientific_analysis_eligibility"] is True
    assert set(result["schemes"]) == {"adjacent_pairs", "balanced_alternating"}
    assert result["worker_exchange_count"] == 16
    assert result["peak_allocated_bytes"] == 1024
    assert result["peak_reserved_bytes"] == 2048


def test_confirmatory_primary_runs_only_c_jobs_in_order_and_resumes_terminal_records(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    config = confirmatory_config(tmp_path)
    gate = _idle_record("cuda-confirmatory-operator-gate-v1")
    gate.update(
        {
            "execution_scope": "gaussian_fixed_ray_confirmatory_40_job",
            "heavy_sweep_enabled": True,
            "config_sha256": "b" * 64,
            "source_identity": {"git_revision": "a" * 40, "tracked_worktree_clean": True},
        }
    )
    accepted_gate_sha256 = _digest(gate)
    calls: list[str] = []

    monkeypatch.setattr(
        fixed_ray_experiment, "_validate_confirmatory_gate_bindings", lambda *_: None
    )

    def fake_job(_: ExperimentConfig, **kwargs: object) -> dict[str, object]:
        job = kwargs["job"]
        assert isinstance(job, dict)
        job_id = str(job["job_id"])
        calls.append(job_id)
        return {
            "schema_version": "gaussian-fixed-ray-confirmatory-job-v1",
            "job_id": job_id,
            "master_seed": job["master_seed"],
            "role": "confirmatory_primary",
            "terminal_status": "completed",
            "scientific_analysis_eligibility": True,
            "accepted_gate_sha256": accepted_gate_sha256,
            "config_sha256": fixed_ray_experiment.config_sha256(config),
            "source_revision": "a" * 40,
        }

    monkeypatch.setattr(fixed_ray_experiment, "run_confirmatory_job", fake_job)
    staging = tmp_path / "primary-staging"

    first = run_confirmatory_primary(
        config,
        operator_opt_in=True,
        operator_gate=gate,
        accepted_gate_sha256=accepted_gate_sha256,
        work_root=staging,
    )
    second = run_confirmatory_primary(
        config,
        operator_opt_in=True,
        operator_gate=gate,
        accepted_gate_sha256=accepted_gate_sha256,
        work_root=staging,
    )

    expected = [f"C{index:03d}" for index in range(1, 31)]
    assert calls == expected
    assert first["completed_job_ids"] == expected
    assert second == first
    assert not any(job_id.startswith("H") for job_id in calls)


def test_holdout_requires_hash_bound_primary_analysis_before_any_h_job(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    config = confirmatory_config(tmp_path)
    gate = _idle_record("cuda-confirmatory-operator-gate-v1")
    gate.update(
        {
            "execution_scope": "gaussian_fixed_ray_confirmatory_40_job",
            "heavy_sweep_enabled": True,
            "config_sha256": "b" * 64,
            "source_identity": {"git_revision": "a" * 40, "tracked_worktree_clean": True},
        }
    )
    accepted_gate_sha256 = _digest(gate)
    monkeypatch.setattr(
        fixed_ray_experiment, "_validate_confirmatory_gate_bindings", lambda *_: None
    )
    calls: list[str] = []

    def fake_job(_: ExperimentConfig, **kwargs: object) -> dict[str, object]:
        job = kwargs["job"]
        assert isinstance(job, dict)
        job_id = str(job["job_id"])
        calls.append(job_id)
        return {
            "schema_version": "gaussian-fixed-ray-confirmatory-job-v1",
            "job_id": job_id,
            "master_seed": job["master_seed"],
            "role": "confirmatory_holdout",
            "terminal_status": "completed",
            "scientific_analysis_eligibility": True,
            "accepted_gate_sha256": accepted_gate_sha256,
            "config_sha256": fixed_ray_experiment.config_sha256(config),
            "source_revision": "a" * 40,
        }

    monkeypatch.setattr(fixed_ray_experiment, "run_confirmatory_job", fake_job)
    primary_path = tmp_path / "primary_analysis.json"

    with pytest.raises(ValueError, match="primary analysis"):
        run_confirmatory_holdout(
            config,
            operator_opt_in=True,
            operator_gate=gate,
            accepted_gate_sha256=accepted_gate_sha256,
            primary_analysis_path=primary_path,
            primary_analysis_sha256="0" * 64,
            work_root=tmp_path / "holdout-staging",
        )
    assert calls == []

    primary_path.write_text(
        json.dumps(
            {
                "schema_version": "gaussian-fixed-ray-primary-analysis-v1",
                "classification": "inconclusive",
                "primary_job_ids": [f"C{index:03d}" for index in range(1, 31)],
            },
            sort_keys=True,
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )
    primary_sha256 = hashlib.sha256(primary_path.read_bytes()).hexdigest()

    result = run_confirmatory_holdout(
        config,
        operator_opt_in=True,
        operator_gate=gate,
        accepted_gate_sha256=accepted_gate_sha256,
        primary_analysis_path=primary_path,
        primary_analysis_sha256=primary_sha256,
        work_root=tmp_path / "holdout-staging",
    )

    expected = [f"H{index:03d}" for index in range(1, 11)]
    assert calls == expected
    assert result["completed_job_ids"] == expected
    assert result["primary_analysis_sha256"] == primary_sha256


def _published_job(job_id: str, role: str) -> dict[str, object]:
    trajectory = np.ones((9, 6), dtype=np.float64)
    scheme = {
        "projective_ray_angles": np.linspace(0.2, 0.01, 9).tolist(),
        "normalized_coupling_distances": np.linspace(0.2, 0.01, 9).tolist(),
        "retained_beta_residuals": np.linspace(0.2, 0.01, 8).tolist(),
        "scalarized_ray_construction_residuals": [1.0e-14] * 9,
        "coefficient_conditioning": np.linspace(2.0, 1.1, 9).tolist(),
        "matrix_condition": 2.0,
        "basin_exit": False,
        "rejected": False,
        "rejection_reason": None,
    }
    return {
        "schema_version": "gaussian-fixed-ray-confirmatory-job-v1",
        "job_id": job_id,
        "master_seed": 1,
        "role": role,
        "terminal_status": "completed",
        "scientific_analysis_eligibility": True,
        "accepted_gate_sha256": "g" * 64,
        "config_sha256": "h" * 64,
        "source_revision": "a" * 40,
        "schemes": {
            "adjacent_pairs": dict(scheme),
            "balanced_alternating": dict(scheme),
        },
        "blocking_scheme_dispersion": [0.0] * 9,
        "distinct_projective_rays": False,
        "trajectory_coefficients": {
            "adjacent_pairs": trajectory.tolist(),
            "balanced_alternating": trajectory.tolist(),
        },
        "initial_coefficients": trajectory[0].tolist(),
        "worker_exchanges": [],
        "worker_exchange_count": 16,
        "operator_gate_recheck": _idle_record("cuda-idle-operator-gate-v1"),
        "elapsed_seconds": 1.0,
        "peak_allocated_bytes": 1024,
        "peak_reserved_bytes": 2048,
    }


def test_confirmatory_publication_writes_complete_two_stage_artifact_contract(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    config = confirmatory_config(tmp_path / "artifacts")
    gate = _idle_record("cuda-confirmatory-operator-gate-v1")
    gate.update(
        {
            "execution_scope": "gaussian_fixed_ray_confirmatory_40_job",
            "heavy_sweep_enabled": True,
            "config_sha256": "b" * 64,
            "source_identity": {"git_revision": "a" * 40, "tracked_worktree_clean": True},
        }
    )
    gate_sha256 = _digest(gate)
    primary_records = [
        _published_job(f"C{index:03d}", "confirmatory_primary")
        for index in range(1, 31)
    ]
    holdout_records = [
        _published_job(f"H{index:03d}", "confirmatory_holdout")
        for index in range(1, 11)
    ]
    primary_analysis = {
        "schema_version": "gaussian-fixed-ray-primary-analysis-v1",
        "classification": "inconclusive",
        "primary_job_ids": [f"C{index:03d}" for index in range(1, 31)],
        "theorem_status": "NUMERICAL",
        "verification_state": "CANDIDATE",
        "claim_origin": "APPLICATION_SPECIFIC",
    }

    monkeypatch.setattr(
        fixed_ray_experiment,
        "_validate_confirmatory_sentinel_bundle",
        lambda *_: {"manifest_sha256": "s" * 64, "git_commit": "a" * 40},
    )
    monkeypatch.setattr(
        fixed_ray_experiment, "_validate_confirmatory_gate_bindings", lambda *_: None
    )
    monkeypatch.setattr(
        fixed_ray_experiment,
        "run_confirmatory_primary",
        lambda *_, **__: {"job_records": primary_records, "completed_job_ids": [r["job_id"] for r in primary_records], "missing_job_ids": []},
    )
    monkeypatch.setattr(
        fixed_ray_experiment, "analyze_primary", lambda *_, **__: primary_analysis
    )

    def fake_holdout(*_: object, **kwargs: object) -> dict[str, object]:
        primary_path = Path(kwargs["primary_analysis_path"])
        assert primary_path.is_file()
        assert hashlib.sha256(primary_path.read_bytes()).hexdigest() == kwargs[
            "primary_analysis_sha256"
        ]
        return {
            "job_records": holdout_records,
            "completed_job_ids": [record["job_id"] for record in holdout_records],
            "missing_job_ids": [],
        }

    monkeypatch.setattr(fixed_ray_experiment, "run_confirmatory_holdout", fake_holdout)
    monkeypatch.setattr(
        fixed_ray_experiment,
        "analyze_holdout",
        lambda *_, **kwargs: {
            "schema_version": "gaussian-fixed-ray-holdout-analysis-v1",
            "analysis_scope": "descriptive_replication_only",
            "primary_analysis_sha256": kwargs["primary_analysis_sha256"],
        },
    )
    monkeypatch.setattr(
        fixed_ray_experiment,
        "collect_provenance",
        lambda *_: {"git_commit": "a" * 40, "git_dirty": False, "input_hashes": {}},
    )

    result = publish_confirmatory_experiment(
        config,
        operator_opt_in=True,
        operator_gate=gate,
        accepted_gate_sha256=gate_sha256,
        sentinel_run_dir=tmp_path / "sentinel",
        accepted_sentinel_manifest_sha256="s" * 64,
        staging_root=tmp_path / "staging",
    )

    manifest = json.loads((result.run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["complete"] is True
    assert set(manifest["artifacts"]) == {
        "config.json",
        "manifest.json",
        "confirmatory_job_table.json",
        "confirmatory_endpoints.json",
        "primary_analysis.json",
        "holdout_analysis.json",
        "confirmatory_execution.json",
        "confirmatory_arrays.npz",
        "metrics.json",
    }
    assert manifest["provenance"]["confirmatory_executed"] is True
    metrics = json.loads((result.run_dir / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["confirmatory_primary_classification"]["theorem_status"] == "NUMERICAL"
    assert metrics["confirmatory_primary_classification"]["verification_state"] == "CANDIDATE"


def test_launcher_confirmatory_gate_uses_separate_control_and_heavy_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    control_path = tmp_path / "confirmatory-control.json"
    gate_path = tmp_path / "confirmatory-gate.json"
    control_path.write_text(
        json.dumps(
            {
                "mode": "confirmatory_gate",
                "operator_opt_in": True,
                "accepted_gate_sha256": "",
                "accepted_sentinel_manifest_sha256": "s" * 64,
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(launcher, "CONFIRMATORY_CONTROL_PATH", control_path)
    monkeypatch.setattr(launcher, "CONFIRMATORY_GATE_PATH", gate_path)
    monkeypatch.setattr(
        launcher,
        "build_confirmatory_gate_record",
        lambda config, **_: {
            "schema_version": "cuda-confirmatory-operator-gate-v1",
            "heavy_sweep_enabled": config.compute.heavy_sweep_enabled,
            "processes_present": False,
        },
    )

    result = launcher.main()

    assert result["heavy_sweep_enabled"] is True
    assert gate_path.is_file()


def test_launcher_confirmatory_run_requires_gate_and_current_sentinel_digest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    gate = {"schema_version": "cuda-confirmatory-operator-gate-v1"}
    gate_payload = json.dumps(gate, sort_keys=True, separators=(",", ":"))
    gate_sha256 = hashlib.sha256(gate_payload.encode("utf-8")).hexdigest()
    control_path = tmp_path / "confirmatory-control.json"
    gate_path = tmp_path / "confirmatory-gate.json"
    gate_path.write_text(gate_payload, encoding="utf-8")
    control_path.write_text(
        json.dumps(
            {
                "mode": "confirmatory_run",
                "operator_opt_in": True,
                "accepted_gate_sha256": gate_sha256,
                "accepted_sentinel_manifest_sha256": "s" * 64,
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(launcher, "CONFIRMATORY_CONTROL_PATH", control_path)
    monkeypatch.setattr(launcher, "CONFIRMATORY_GATE_PATH", gate_path)
    monkeypatch.setattr(launcher, "CONFIRMATORY_STAGING_ROOT", tmp_path / "staging")
    monkeypatch.setattr(
        launcher,
        "_find_accepted_sentinel_run",
        lambda _: tmp_path / "sentinel-run",
    )
    captured: dict[str, object] = {}

    def fake_publish(config: ExperimentConfig, **kwargs: object):
        captured["heavy_sweep_enabled"] = config.compute.heavy_sweep_enabled
        captured.update(kwargs)
        return SimpleNamespace(run_dir=tmp_path, status="inconclusive", metrics={})

    monkeypatch.setattr(launcher, "publish_confirmatory_experiment", fake_publish)
    monkeypatch.setattr(launcher, "_print_result", lambda _: None)

    launcher.main()

    assert captured["heavy_sweep_enabled"] is True
    assert captured["accepted_gate_sha256"] == gate_sha256
    assert captured["accepted_sentinel_manifest_sha256"] == "s" * 64
