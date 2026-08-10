from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

from multiagent_elbo.config import ExperimentConfig
from multiagent_elbo.finite.counterexamples import (
    ExactAction,
    ExactChannel,
    ExactLaw,
    coarsen_marked_event,
    fixed_channel_score_gap,
    hoeffding_decompose_action,
    kl_divergence,
    project_action,
    relabel_law,
)
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


def config(
    root: Path,
    *,
    diagnostics: bool = False,
    render_figures: bool = False,
) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": "finite_counterexample", "seed": 20260809},
        {
            "experiment": "finite_counterexample",
            "fixture": "counterexample_catalog_v1",
            "max_states": 4,
            "max_denominator": 8,
            "arithmetic": "exact_rational",
        },
        {
            "dtype": "float64",
            "atol": 1.0e-12,
            "rtol": 1.0e-10,
            "min_spd_rcond": 1.0e-12,
            "max_frame_condition": 1.0e6,
        },
        {"root": str(root), "collect_diagnostics": diagnostics, "render_figures": render_figures},
    )


def _fractions(numerators: np.ndarray, denominators: np.ndarray) -> tuple[Fraction, ...]:
    return tuple(Fraction(int(num), int(den)) for num, den in zip(numerators.flat, denominators.flat))


def test_counterexample_run_emits_frozen_metrics_complete_candidates_and_provenance(tmp_path: Path):
    result = run_finite_counterexample_experiment(config(tmp_path, diagnostics=True))
    assert isinstance(result, FiniteCounterexampleExperimentResult)
    assert result.status == "pass"
    assert set(result.metrics) == METRICS
    assert result.metrics["support_violation_count"].value == 1.0
    assert result.metrics["parameter_dependent_channel_gap"].value == 0.125
    assert result.metrics["single_law_relabeling_gap"].value == pytest.approx(math.log(3.0) / 2.0)
    assert result.metrics["marked_event_source_mass_gap"].value == 0.5
    assert result.metrics["pairwise_truncation_residual"].value == 1.0
    assert {metric.claim_origin for metric in result.metrics.values()} >= {"STANDARD", "PROJECT_NOVEL"}
    expected = {"config.json", "manifest.json", "metrics.json", "arrays.npz", "enumeration_bounds.json", "candidate_records.json", "minimal_witnesses.json", "stress_matrix.json", "diagnostics.npz"}
    assert {path.name for path in result.run_dir.iterdir()} == expected
    manifest = json.loads((result.run_dir / "manifest.json").read_text("utf-8"))
    assert manifest["complete"] is True
    assert manifest["provenance"]["arithmetic"] == "exact_rational"
    bounds = json.loads((result.run_dir / "enumeration_bounds.json").read_text("utf-8"))
    assert bounds["requested"] == {"max_states": 4, "max_denominator": 8}
    assert bounds["effective"] == {"max_states": 2, "max_denominator": 4}
    assert bounds["enumerated_counts"]["laws"] == 7
    candidates = json.loads((result.run_dir / "candidate_records.json").read_text("utf-8"))
    minimal = json.loads((result.run_dir / "minimal_witnesses.json").read_text("utf-8"))
    assert len(candidates) > len(minimal) == 5
    for record in candidates + minimal:
        assert set(record) == {"claim_id", "inside_declared_domain", "assumptions_satisfied", "smallest_witness", "exact_or_numeric", "observed_residual", "classification", "theorem_status", "verification_state", "claim_origin"}
        assert record["classification"] in {"catalog", "assumption_boundary"}


def test_primitive_rational_arrays_independently_recompute_all_metrics(tmp_path: Path):
    result = run_finite_counterexample_experiment(config(tmp_path))
    arrays = result.arrays
    support_q = ExactLaw(_fractions(arrays["support_q_num"], arrays["support_q_den"]))
    support_p = ExactLaw(_fractions(arrays["support_p_num"], arrays["support_p_den"]))
    assert len(kl_divergence(support_q, support_p).support_violations) == 1
    theta = _fractions(arrays["theta_num"], arrays["theta_den"])[0]
    assert float(fixed_channel_score_gap(theta)) == result.metrics["parameter_dependent_channel_gap"].value
    relabel_p = ExactLaw(_fractions(arrays["relabel_p_num"], arrays["relabel_p_den"]))
    permutation = tuple(int(value) for value in arrays["relabel_permutation"])
    relabel_kl = kl_divergence(relabel_law(relabel_p, permutation), relabel_p)
    assert relabel_kl.value == pytest.approx(result.metrics["single_law_relabeling_gap"].value)
    source = ExactLaw(_fractions(arrays["marked_source_num"], arrays["marked_source_den"]))
    channel_values = _fractions(arrays["marked_channel_num"], arrays["marked_channel_den"])
    channel = ExactChannel((channel_values[:2], channel_values[2:]), 2)
    beta_values = _fractions(arrays["marked_beta_num"], arrays["marked_beta_den"])
    joint, beta_only = coarsen_marked_event(source, (beta_values[:2], beta_values[2:]), channel)
    assert max(abs(x - y) for a, b in zip(joint, beta_only) for x, y in zip(a, b)) == Fraction(1, 2)
    action_values = _fractions(arrays["action_num"], arrays["action_den"])
    action = ExactAction(tuple(int(x) for x in arrays["action_axis_sizes"]), action_values)
    projection = project_action(hoeffding_decompose_action(action), int(arrays["retained_order"][0]))
    assert float(projection.residual) == result.metrics["pairwise_truncation_residual"].value
    assert action.cardinalities == (2, 2, 2)
    with pytest.raises(TypeError): result.metrics["x"] = result.metrics["support_violation_count"]  # type: ignore[index]
    with pytest.raises(ValueError): arrays["theta_num"][0] = 1


def test_output_toggles_and_deterministic_semantic_artifacts(tmp_path: Path):
    no_diagnostics = run_finite_counterexample_experiment(config(tmp_path / "no"))
    with_diagnostics = run_finite_counterexample_experiment(config(tmp_path / "yes", diagnostics=True))
    assert not (no_diagnostics.run_dir / "diagnostics.npz").exists()
    assert (with_diagnostics.run_dir / "diagnostics.npz").is_file()
    for name in ("metrics.json", "enumeration_bounds.json", "candidate_records.json", "minimal_witnesses.json", "stress_matrix.json", "arrays.npz"):
        assert (no_diagnostics.run_dir / name).read_bytes() == (with_diagnostics.run_dir / name).read_bytes()


@pytest.mark.parametrize("kind", ["wrong_experiment", "cuda", "figures"])
def test_invalid_requests_fail_before_all_runtime_seams(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, kind: str):
    import multiagent_elbo.finite.counterexample_experiment as experiment
    candidate = config(tmp_path)
    if kind == "wrong_experiment":
        candidate = ExperimentConfig.from_dicts({"name": "bad", "seed": 1}, {"experiment": "finite_exact", "retained_interaction_order": 2}, {"dtype": "float64", "atol": 1e-12, "rtol": 1e-10, "min_spd_rcond": 1e-12, "max_frame_condition": 1e6}, {"root": str(tmp_path), "collect_diagnostics": False, "render_figures": False})
    elif kind == "cuda":
        candidate = replace(candidate, compute=replace(candidate.compute, backend="cuda"))
    else:
        candidate = config(tmp_path, render_figures=True)
    forbidden = lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("runtime seam"))
    monkeypatch.setattr(experiment.RngStreams, "from_seed", forbidden)
    monkeypatch.setattr(experiment, "collect_provenance", forbidden)
    monkeypatch.setattr(experiment.RunStore, "create", forbidden)
    with pytest.raises(ValueError): run_finite_counterexample_experiment(candidate)
    assert not tmp_path.exists() or not list(tmp_path.iterdir())


def test_launcher_is_import_safe_and_has_editable_no_parser_dictionaries(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    path = Path(__file__).parents[1] / "run_finite_counterexample_lab.py"
    monkeypatch.chdir(tmp_path); monkeypatch.setattr("sys.argv", ["lab.py", "--ignored"])
    spec = importlib.util.spec_from_file_location("finite_counterexample_lab", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    assert not hasattr(module, "parser") and module.THEORY["experiment"] == "finite_counterexample"


def test_launcher_runs_without_pythonpath_or_torch_import(tmp_path: Path):
    launcher = Path(__file__).parents[1] / "run_finite_counterexample_lab.py"
    environment = dict(os.environ); environment.pop("PYTHONPATH", None)
    audit = "import runpy, sys; runpy.run_path(sys.argv[1], run_name='__main__'); assert 'torch' not in sys.modules"
    completed = subprocess.run([sys.executable, "-c", audit, str(launcher)], cwd=tmp_path, env=environment, capture_output=True, text=True, check=False)
    assert completed.returncode == 0, completed.stderr
    assert "status=pass; metrics=5; figures=not_requested" in completed.stdout
