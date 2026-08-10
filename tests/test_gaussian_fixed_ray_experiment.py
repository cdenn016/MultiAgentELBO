from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import numpy as np
import pytest

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.realizations.gaussian.fixed_ray_experiment import (
    GaussianFixedRayExperimentResult,
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
            "cuda_worker_python": r"C:\anaconda\python.exe",
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
        "off_family_nonlinear_remainder",
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
        metric.verification_state in {"EVIDENCE_VERIFIED", "INCONCLUSIVE"}
        for metric in result.metrics.values()
    )
    assert result.metrics["cpu_cuda_parity_residual"].status == "inconclusive"
    assert result.metrics["cpu_cuda_parity_residual"].theorem_status == "OPEN"
    assert result.metrics["cpu_cuda_parity_residual"].verification_state == "INCONCLUSIVE"
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
    assert backend["worker_cuda"]["status"] == "not_run_busy_gpu"

    parity = json.loads(
        (result.run_dir / "parity_matrix.json").read_text(encoding="utf-8")
    )
    assert parity["controller_cpu_vs_worker_cpu"]["passed"] is True
    assert parity["controller_cpu_vs_worker_cuda"]["status"] == "inconclusive"
    assert parity["mutation_negative_control"]["passed"] is False

    arrays = np.load(result.run_dir / "initial_conditions.npz", allow_pickle=False)
    assert arrays["initial_coefficients"].shape == (4, 6)
    assert arrays["adjacent_pairs_coefficients"].shape == (4, 9, 6)
    assert arrays["balanced_alternating_coefficients"].shape == (4, 9, 6)
    assert arrays["adjacent_pairs_projective_angles"].shape == (4, 9)
    assert arrays["balanced_alternating_retained_beta_residuals"].shape == (4, 8)
    assert arrays["blocking_scheme_dispersion"].shape == (4, 9)
    np.testing.assert_allclose(
        arrays["off_family_nonlinear_remainders"], 0.0, rtol=0.0, atol=1.0e-12
    )


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
