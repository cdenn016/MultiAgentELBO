from __future__ import annotations

from pathlib import Path
import importlib.util
import json
import os
import subprocess
import sys

import numpy as np
import pytest

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.finite.counterexample_experiment import (
    FiniteCounterexampleExperimentResult,
    run_finite_counterexample_experiment,
)


METRICS = {
    "support_violation_count",
    "parameter_dependent_channel_gap",
    "single_law_relabeling_gap",
    "marked_event_source_mass_gap",
    "pairwise_truncation_residual",
}


def config(root: Path, *, diagnostics: bool = False) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": "finite_counterexample", "seed": 20260809},
        {"experiment": "finite_counterexample", "fixture": "counterexample_catalog_v1", "max_states": 4, "max_denominator": 8, "arithmetic": "exact_rational"},
        {"dtype": "float64", "atol": 1.0e-12, "rtol": 1.0e-10, "min_spd_rcond": 1.0e-12, "max_frame_condition": 1.0e6},
        {"root": str(root), "collect_diagnostics": diagnostics, "render_figures": False},
    )


def test_counterexample_run_emits_frozen_metrics_and_exact_artifacts(tmp_path: Path):
    result = run_finite_counterexample_experiment(config(tmp_path, diagnostics=True))
    assert isinstance(result, FiniteCounterexampleExperimentResult)
    assert result.status == "pass"
    assert set(result.metrics) == METRICS
    assert result.metrics["support_violation_count"].value == 1.0
    assert result.metrics["parameter_dependent_channel_gap"].value == 0.5
    assert result.metrics["single_law_relabeling_gap"].value == 0.0
    assert result.metrics["marked_event_source_mass_gap"].value == 0.5
    assert result.metrics["pairwise_truncation_residual"].value == 1.0
    for metric in result.metrics.values():
        assert metric.theorem_status.isupper()
        assert metric.verification_state.isupper()
        assert metric.claim_origin.isupper()
    expected = {"config.json", "manifest.json", "metrics.json", "arrays.npz", "enumeration_bounds.json", "candidate_records.json", "minimal_witnesses.json", "stress_matrix.json", "diagnostics.npz"}
    assert {path.name for path in result.run_dir.iterdir()} == expected
    assert json.loads((result.run_dir / "manifest.json").read_text("utf-8"))["complete"] is True


def test_arrays_recompute_each_scalar_and_results_are_immutable(tmp_path: Path):
    result = run_finite_counterexample_experiment(config(tmp_path))
    arrays = result.arrays
    assert float(arrays["support_violation_indices"].size) == result.metrics["support_violation_count"].value
    assert float(arrays["parameter_theta"][0] * arrays["parameter_theta"][0] * 2.0) == result.metrics["parameter_dependent_channel_gap"].value
    assert float(np.max(np.abs(arrays["relabeling_difference"]))) == result.metrics["single_law_relabeling_gap"].value
    assert float(np.max(np.abs(arrays["marked_joint"] - arrays["marked_beta_only"]))) == result.metrics["marked_event_source_mass_gap"].value
    assert float(arrays["pairwise_omitted_max"][0]) == result.metrics["pairwise_truncation_residual"].value
    with pytest.raises(TypeError): result.metrics["x"] = result.metrics["support_violation_count"]  # type: ignore[index]
    with pytest.raises(ValueError): arrays["parameter_theta"][0] = 0.0


def test_same_seed_semantic_artifacts_are_root_independent(tmp_path: Path):
    first = run_finite_counterexample_experiment(config(tmp_path / "one"))
    second = run_finite_counterexample_experiment(config(tmp_path / "two"))
    assert first.config_hash != second.config_hash
    for name in ("metrics.json", "enumeration_bounds.json", "candidate_records.json", "minimal_witnesses.json", "stress_matrix.json", "arrays.npz"):
        assert (first.run_dir / name).read_bytes() == (second.run_dir / name).read_bytes()


def test_wrong_experiment_fails_before_runtime_seams(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    import multiagent_elbo.finite.counterexample_experiment as experiment
    bad = ExperimentConfig.from_dicts({"name": "bad", "seed": 1}, {"experiment": "finite_exact", "retained_interaction_order": 2}, {"dtype": "float64", "atol": 1e-12, "rtol": 1e-10, "min_spd_rcond": 1e-12, "max_frame_condition": 1e6}, {"root": str(tmp_path), "collect_diagnostics": False, "render_figures": False})
    monkeypatch.setattr(experiment.RngStreams, "from_seed", lambda *_: (_ for _ in ()).throw(AssertionError("rng")))
    with pytest.raises(ValueError, match="finite_counterexample"):
        run_finite_counterexample_experiment(bad)
    assert not tmp_path.exists() or not list(tmp_path.iterdir())


def test_launcher_is_import_safe_and_has_editable_no_parser_dictionaries(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    path = Path(__file__).parents[1] / "run_finite_counterexample_lab.py"
    monkeypatch.chdir(tmp_path); monkeypatch.setattr("sys.argv", ["lab.py", "--ignored"])
    spec = importlib.util.spec_from_file_location("finite_counterexample_lab", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    assert not hasattr(module, "parser") and module.THEORY["experiment"] == "finite_counterexample"
    module.OUTPUT["root"] = str(tmp_path / "artifacts")
    assert module.main().status == "pass"


def test_launcher_runs_from_clean_directory_without_inherited_pythonpath(tmp_path: Path):
    launcher = Path(__file__).parents[1] / "run_finite_counterexample_lab.py"
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)
    completed = subprocess.run(
        [sys.executable, str(launcher)], cwd=tmp_path, env=environment,
        capture_output=True, text=True, check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "status=pass; metrics=5; figures=not_requested" in completed.stdout
    assert (tmp_path / "artifacts").is_dir()
