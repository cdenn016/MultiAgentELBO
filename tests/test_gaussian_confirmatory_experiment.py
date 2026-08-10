from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
from types import MappingProxyType, SimpleNamespace

import numpy as np
import pytest

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.realizations.gaussian import fixed_ray_experiment
from multiagent_elbo.realizations.gaussian.fixed_ray_experiment import (
    build_confirmatory_gate_record,
    run_confirmatory_job,
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
