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
    MAX_NEAR_SINGULAR_SCORE,
    ExactAction,
    ExactChannel,
    ExactLaw,
    coarsen_marked_event,
    hoeffding_decompose_action,
    kl_divergence,
    project_action,
    relabel_law,
    validate_full_rank_spd,
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
    max_states: int = 4,
    max_denominator: int = 8,
) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": "finite_counterexample", "seed": 20260809},
        {
            "experiment": "finite_counterexample",
            "fixture": "counterexample_catalog_v1",
            "max_states": max_states,
            "max_denominator": max_denominator,
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


@pytest.mark.parametrize(
    ("max_states", "max_denominator", "message"),
    ((1, 4, "max_states must be at least 2"), (2, 3, "max_denominator must be at least 4")),
)
def test_catalog_bound_minima_reject_before_every_effect(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    max_states: int,
    max_denominator: int,
    message: str,
):
    import multiagent_elbo.finite.counterexample_experiment as experiment

    def forbidden(*_args, **_kwargs):
        raise AssertionError("effect reached before bound rejection")

    monkeypatch.setattr(experiment, "_catalog", forbidden)
    monkeypatch.setattr(experiment, "config_sha256", forbidden)
    monkeypatch.setattr(experiment.RngStreams, "from_seed", forbidden)
    monkeypatch.setattr(experiment, "collect_provenance", forbidden)
    monkeypatch.setattr(experiment.RunStore, "create", forbidden)
    invalid = config(
        tmp_path,
        max_states=max_states,
        max_denominator=max_denominator,
    )

    with pytest.raises(ValueError, match=message):
        run_finite_counterexample_experiment(invalid)

    assert not tmp_path.exists() or not list(tmp_path.iterdir())


@pytest.mark.parametrize(
    ("max_states", "max_denominator"),
    ((2, 4), (5, 9)),
)
def test_equal_and_greater_catalog_bounds_never_allow_effective_overreach(
    tmp_path: Path,
    max_states: int,
    max_denominator: int,
):
    result = run_finite_counterexample_experiment(
        config(
            tmp_path,
            max_states=max_states,
            max_denominator=max_denominator,
        )
    )
    bounds = json.loads(
        (result.run_dir / "enumeration_bounds.json").read_text("utf-8")
    )
    assert bounds["requested"] == {
        "max_states": max_states,
        "max_denominator": max_denominator,
    }
    assert bounds["effective"]["laws_channels"] == {
        "max_states": 2,
        "max_denominator": 4,
    }
    assert all(
        bounds["effective"]["laws_channels"][key] <= bounds["requested"][key]
        for key in ("max_states", "max_denominator")
    )


def _fractions(numerators: np.ndarray, denominators: np.ndarray) -> tuple[Fraction, ...]:
    return tuple(Fraction(int(num), int(den)) for num, den in zip(numerators.flat, denominators.flat))


def test_counterexample_run_emits_frozen_metrics_complete_candidates_and_provenance(tmp_path: Path):
    result = run_finite_counterexample_experiment(config(tmp_path, diagnostics=True))
    assert isinstance(result, FiniteCounterexampleExperimentResult)
    assert result.status == "pass"
    assert set(result.metrics) == METRICS
    assert result.metrics["support_violation_count"].value == 1.0
    assert result.metrics["parameter_dependent_channel_gap"].value == pytest.approx(
        16.0 / 15.0
    )
    assert result.metrics["single_law_relabeling_gap"].value == pytest.approx(math.log(3.0) / 2.0)
    assert result.metrics["marked_event_source_mass_gap"].value == 0.5
    assert result.metrics["pairwise_truncation_residual"].value == 1.0
    assert result.metrics["parameter_dependent_channel_gap"].claim_origin == (
        "APPLICATION_SPECIFIC"
    )
    assert result.metrics["single_law_relabeling_gap"].claim_origin == (
        "APPLICATION_SPECIFIC"
    )
    assert {metric.claim_origin for metric in result.metrics.values()} == {
        "APPLICATION_SPECIFIC",
        "PROJECT_NOVEL",
    }
    expected = {"config.json", "manifest.json", "metrics.json", "arrays.npz", "enumeration_bounds.json", "candidate_records.json", "minimal_witnesses.json", "stress_matrix.json", "diagnostics.npz"}
    assert {path.name for path in result.run_dir.iterdir()} == expected
    manifest = json.loads((result.run_dir / "manifest.json").read_text("utf-8"))
    assert manifest["complete"] is True
    assert manifest["provenance"]["arithmetic"] == "exact_rational"
    candidates = json.loads(
        (result.run_dir / "candidate_records.json").read_text("utf-8")
    )
    minimal = json.loads(
        (result.run_dir / "minimal_witnesses.json").read_text("utf-8")
    )
    bounds = json.loads((result.run_dir / "enumeration_bounds.json").read_text("utf-8"))
    assert bounds["requested"] == {"max_states": 4, "max_denominator": 8}
    assert bounds["effective"] == {
        "laws_channels": {"max_states": 2, "max_denominator": 4},
        "actions": {
            "axis_cardinalities": [2, 2, 2],
            "max_denominator": 1,
            "value_bound": 1,
        },
    }
    assert bounds["enumerated_counts"] == {
        "laws": 7,
        "channels": 49,
        "actions": 6561,
        "candidates": 19587,
        "minimal_candidates": 5,
    }
    assert len(candidates) == 19587
    assert len(minimal) == 5
    minimal_parameter = next(
        record
        for record in minimal
        if record["claim_id"] == "fixed_channel_score_fisher"
    )
    assert minimal_parameter["smallest_witness"]["theta"] == "1/2"
    assert minimal_parameter["observed_residual"] == "4/3"
    fields = {"claim_id", "inside_declared_domain", "assumptions_satisfied", "smallest_witness", "exact_or_numeric", "observed_residual", "classification", "theorem_status", "verification_state", "claim_origin"}
    for record in candidates + minimal:
        assert set(record) == fields
        assert record["theorem_status"] == "ESTABLISHED"
        assert record["verification_state"] == "EVIDENCE_VERIFIED"
        assert record["claim_origin"] in {"STANDARD", "PROJECT_NOVEL"}
        assert record["exact_or_numeric"] in {"exact", "numeric_log"}
        assert record["classification"] in {"catalog", "assumption_boundary"}
        if record["classification"] == "catalog":
            assert record["inside_declared_domain"] is True
            assert record["assumptions_satisfied"] is True
            assert record["exact_or_numeric"] == "exact"
        else:
            assert record["inside_declared_domain"] is False
            assert record["assumptions_satisfied"] is False
    relabel = next(record for record in candidates if record["claim_id"] == "single_law_relabeling" and record["smallest_witness"]["p"] == ["3/4", "1/4"])
    assert relabel["observed_residual"] == "ln(3)/2"
    assert relabel["exact_or_numeric"] == "numeric_log"
    assert relabel["inside_declared_domain"] is False
    assert relabel["assumptions_satisfied"] is False
    assert relabel["classification"] == "assumption_boundary"
    assert relabel["claim_origin"] == "STANDARD"
    parameter = next(
        record
        for record in candidates
        if record["claim_id"] == "fixed_channel_score_fisher"
        and record["smallest_witness"]["theta"] == "1/4"
    )
    assert parameter["inside_declared_domain"] is False
    assert parameter["assumptions_satisfied"] is False
    assert parameter["classification"] == "assumption_boundary"
    assert parameter["claim_origin"] == "STANDARD"
    assert parameter["observed_residual"] == "16/15"
    assert parameter["smallest_witness"]["fine_law"] == ["1/2", "1/2"]
    assert parameter["smallest_witness"]["fine_derivative"] == ["0", "0"]
    assert parameter["smallest_witness"]["channel"] == [
        ["5/8", "3/8"],
        ["5/8", "3/8"],
    ]
    assert parameter["smallest_witness"]["channel_derivative"] == [
        ["1/2", "-1/2"],
        ["1/2", "-1/2"],
    ]
    for record in candidates:
        if record["exact_or_numeric"] != "numeric_log":
            continue
        residual = record["observed_residual"]
        assert residual != "numeric_log"
        if residual != "ln(3)/2":
            assert math.isfinite(float(residual))
            assert float(residual) > 0.0
    stress = json.loads((result.run_dir / "stress_matrix.json").read_text("utf-8"))
    assert stress["deep_composition"] == {
        "channels": {
            "a": [["1", "0"], ["1/2", "1/2"]],
            "b": [["1/2", "1/2"], ["0", "1"]],
            "c": [["3/4", "1/4"], ["1/4", "3/4"]],
        },
        "direct_rows": [["1/2", "1/2"], ["3/8", "5/8"]],
        "staged_rows": [["1/2", "1/2"], ["3/8", "5/8"]],
        "residual": "0",
        "direct_equals_staged": True,
    }
    assert stress["relabeling"] == {"coherent": True, "residual": "0"}
    assert stress["retained_space"] == {"pass_residual": "1", "fails_full_reconstruction": True}
    assert stress["tolerance_scaling"] == {"base": "1/100", "states": 2, "scaled": "1/50"}
    near_singular = stress["conditioning"]["rejected_near_singular"]
    assert stress["conditioning"]["accepted_dimension"] == 2
    assert stress["conditioning"]["accepted_condition"] == "4"
    assert near_singular == {
        "matrix": [["1", "0"], ["0", "1/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"]],
        "minimum_diagonal": "1/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "condition_score": "10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "threshold": "1000000000000",
        "positive_definite": True,
        "rejected": True,
        "reason": "near-singular SPD input exceeds the exact conditioning boundary",
    }
    assert Fraction(near_singular["minimum_diagonal"]) > 0
    assert Fraction(near_singular["condition_score"]) > MAX_NEAR_SINGULAR_SCORE
    matrix = tuple(
        tuple(Fraction(value) for value in row)
        for row in near_singular["matrix"]
    )
    with pytest.raises(ValueError, match="near-singular SPD input"):
        validate_full_rank_spd(matrix)


def test_primitive_rational_arrays_independently_recompute_all_metrics(tmp_path: Path):
    result = run_finite_counterexample_experiment(config(tmp_path))
    arrays = result.arrays
    support_q = ExactLaw(_fractions(arrays["support_q_num"], arrays["support_q_den"]))
    support_p = ExactLaw(_fractions(arrays["support_p_num"], arrays["support_p_den"]))
    assert len(kl_divergence(support_q, support_p).support_violations) == 1
    theta = _fractions(arrays["theta_num"], arrays["theta_den"])[0]
    assert theta == Fraction(1, 4)
    fine_law = _fractions(
        arrays["parameter_fine_law_num"], arrays["parameter_fine_law_den"]
    )
    fine_derivative = _fractions(
        arrays["parameter_fine_derivative_num"],
        arrays["parameter_fine_derivative_den"],
    )
    channel_entries = _fractions(
        arrays["parameter_channel_num"], arrays["parameter_channel_den"]
    )
    channel = (channel_entries[:2], channel_entries[2:])
    derivative_entries = _fractions(
        arrays["parameter_channel_derivative_num"],
        arrays["parameter_channel_derivative_den"],
    )
    channel_derivative = (derivative_entries[:2], derivative_entries[2:])
    pushed_law = _fractions(
        arrays["parameter_pushed_law_num"],
        arrays["parameter_pushed_law_den"],
    )
    pushed_derivative = _fractions(
        arrays["parameter_pushed_derivative_num"],
        arrays["parameter_pushed_derivative_den"],
    )
    fine_score = tuple(
        derivative / mass
        for derivative, mass in zip(fine_derivative, fine_law)
    )
    reconstructed_pushed = tuple(
        sum(fine_law[index] * channel[index][target] for index in range(2))
        for target in range(2)
    )
    reconstructed_derivative = tuple(
        sum(
            fine_derivative[index] * channel[index][target]
            + fine_law[index] * channel_derivative[index][target]
            for index in range(2)
        )
        for target in range(2)
    )
    fixed_prediction = tuple(
        sum(
            fine_law[index] * channel[index][target] * fine_score[index]
            for index in range(2)
        )
        / pushed_law[target]
        for target in range(2)
    )
    actual_score = tuple(
        derivative / mass
        for derivative, mass in zip(pushed_derivative, pushed_law)
    )
    score_gap = sum(
        mass * (actual - predicted) ** 2
        for mass, actual, predicted in zip(
            pushed_law, actual_score, fixed_prediction
        )
    )
    assert channel_derivative != ((Fraction(0), Fraction(0)),) * 2
    assert reconstructed_pushed == pushed_law == (Fraction(5, 8), Fraction(3, 8))
    assert reconstructed_derivative == pushed_derivative == (
        Fraction(1, 2),
        Fraction(-1, 2),
    )
    assert fixed_prediction == (Fraction(0), Fraction(0))
    assert actual_score == (Fraction(4, 5), Fraction(-4, 3))
    assert score_gap == Fraction(16, 15)
    assert _fractions(
        arrays["parameter_fine_score_num"],
        arrays["parameter_fine_score_den"],
    ) == fine_score
    assert _fractions(
        arrays["parameter_fixed_predicted_coarse_score_num"],
        arrays["parameter_fixed_predicted_coarse_score_den"],
    ) == fixed_prediction
    assert _fractions(
        arrays["parameter_actual_coarse_score_num"],
        arrays["parameter_actual_coarse_score_den"],
    ) == actual_score
    assert _fractions(
        arrays["parameter_fisher_weighted_score_gap_num"],
        arrays["parameter_fisher_weighted_score_gap_den"],
    ) == (score_gap,)
    assert result.metrics["parameter_dependent_channel_gap"].value == pytest.approx(
        float(Fraction(16, 15))
    )
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
