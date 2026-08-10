"""Integration contracts shared by independent scientific producers."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path

import numpy as np
import pytest

from multiagent_elbo.conditioning import assess_spectral_spd
from multiagent_elbo.config import ExperimentConfig, NumericsConfig
from multiagent_elbo.finite import counterexample_experiment as session3
from multiagent_elbo.finite.counterexamples import (
    ExactLaw,
    relabel_law,
    validate_full_rank_spd,
)
from multiagent_elbo.finite.permutations import FinitePermutation
from multiagent_elbo.realizations.gaussian.interactions import (
    GaussianInteraction,
    GaussianNumericalError,
)


def _session3_config(root: Path) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": "shared_scientific_contracts", "seed": 20260810},
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
        {
            "root": str(root),
            "collect_diagnostics": False,
            "render_figures": False,
        },
    )


def test_same_three_cycle_agrees_across_exact_and_geometry_producers():
    cycle = FinitePermutation.from_old_to_new((1, 2, 0))
    masses = (Fraction(1, 5), Fraction(3, 10), Fraction(1, 2))
    expected = (Fraction(1, 2), Fraction(1, 5), Fraction(3, 10))

    assert relabel_law(ExactLaw(masses), cycle).masses == expected
    np.testing.assert_allclose(
        cycle.pullback_axis(np.asarray(masses, dtype=np.float64)),
        (0.5, 0.2, 0.3),
        rtol=0.0,
        atol=0.0,
    )


def test_inverse_and_composition_obey_the_literal_group_law():
    cycle = FinitePermutation.from_old_to_new((1, 2, 0))
    swap = FinitePermutation.from_old_to_new((1, 0, 2))

    assert cycle.inverse().old_to_new == (2, 0, 1)
    assert cycle.then(cycle.inverse()).old_to_new == (0, 1, 2)
    assert cycle.inverse().then(cycle).old_to_new == (0, 1, 2)
    assert cycle.then(swap).old_to_new == (0, 2, 1)
    np.testing.assert_array_equal(
        swap.pullback_axis(cycle.pullback_axis(np.array([10, 20, 30]))),
        (10, 30, 20),
    )
    np.testing.assert_array_equal(
        cycle.then(swap).pullback_axis(np.array([10, 20, 30])),
        (10, 30, 20),
    )


def test_inverse_convention_mutation_is_detected():
    cycle = FinitePermutation.from_old_to_new((1, 2, 0))
    values = np.array([0.2, 0.3, 0.5])

    correct = cycle.pullback_axis(values)
    mutated = np.take(values, cycle.old_to_new)

    np.testing.assert_allclose(correct, (0.5, 0.2, 0.3), rtol=0.0, atol=0.0)
    np.testing.assert_allclose(mutated, (0.3, 0.5, 0.2), rtol=0.0, atol=0.0)
    assert np.max(np.abs(correct - mutated)) == pytest.approx(0.3)


def test_determinant_proxy_mutations_reverse_both_required_spd_cases():
    def determinant_volume_proxy(matrix: np.ndarray) -> float:
        return 1.0 / abs(float(np.linalg.det(matrix)))

    correlated = np.array(
        [[1.0, 1.0 - 1.0e-12], [1.0 - 1.0e-12, 1.0]]
    )
    repeated = np.diag([1.0, 1.0e-7, 1.0e-7])

    correlated_mutation = (
        "pass" if determinant_volume_proxy(correlated) < 1.0e12 else "fail"
    )
    repeated_mutation = (
        "pass" if determinant_volume_proxy(repeated) < 1.0e12 else "fail"
    )
    assert determinant_volume_proxy(correlated) < 1.0e12
    assert correlated_mutation == "pass"
    assert assess_spectral_spd(
        correlated, min_rcond=1.0e-12, atol=0.0, rtol=0.0
    ).decision == "fail"
    assert determinant_volume_proxy(repeated) > 1.0e12
    assert repeated_mutation == "fail"
    assert assess_spectral_spd(
        repeated, min_rcond=1.0e-12, atol=0.0, rtol=0.0
    ).decision == "pass"


@pytest.mark.parametrize(
    ("finite_matrix", "gaussian_matrix", "expected"),
    [
        pytest.param(
            (
                (Fraction(1), Fraction(10**12 - 1, 10**12)),
                (Fraction(10**12 - 1, 10**12), Fraction(1)),
            ),
            np.array(
                [[1.0, 1.0 - 1.0e-12], [1.0 - 1.0e-12, 1.0]]
            ),
            "fail",
            id="correlated-false-accept",
        ),
        pytest.param(
            (
                (Fraction(1), Fraction(0), Fraction(0)),
                (Fraction(0), Fraction(1, 10**7), Fraction(0)),
                (Fraction(0), Fraction(0), Fraction(1, 10**7)),
            ),
            np.diag([1.0, 1.0e-7, 1.0e-7]),
            "pass",
            id="repeated-small-false-reject",
        ),
    ],
)
def test_exact_finite_and_gaussian_adapters_share_named_spd_decisions(
    finite_matrix: tuple[tuple[Fraction, ...], ...],
    gaussian_matrix: np.ndarray,
    expected: str,
):
    numerics = NumericsConfig(
        dtype="float64",
        atol=0.0,
        rtol=0.0,
        min_spd_rcond=1.0e-12,
        max_frame_condition=1.0e6,
    )

    finite_decision = validate_full_rank_spd(
        finite_matrix, min_rcond=1.0e-12, atol=0.0, rtol=0.0
    ).decision
    try:
        GaussianInteraction.from_self_and_edges((gaussian_matrix,), {}, numerics)
    except GaussianNumericalError as error:
        assert "reciprocal condition" in str(error)
        gaussian_decision = "fail"
    else:
        gaussian_decision = "pass"

    assert finite_decision == expected
    assert gaussian_decision == expected


def test_tolerance_band_is_inconclusive_with_literal_boundary_metadata():
    assessment = assess_spectral_spd(
        np.diag([1.0, 1.05e-6]),
        min_rcond=1.0e-6,
        atol=1.0e-7,
        rtol=0.0,
    )

    assert assessment.reciprocal_condition == pytest.approx(1.05e-6)
    assert assessment.threshold == 1.0e-6
    assert assessment.boundary_tolerance == 1.0e-7
    assert assessment.decision == "inconclusive"


def test_stress_failure_precedes_an_inconclusive_status():
    stress = {
        "uncertain": session3.StressAssessment(
            "uncertain", "1", "0.1", "inconclusive", "0", "literal fixture"
        ),
        "broken": session3.StressAssessment(
            "broken", "1", "0", "fail", "0", "literal fixture"
        ),
    }

    assert session3._aggregate_status({}, stress) == "fail"


def test_false_coherence_alone_forces_session3_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    monkeypatch.setattr(
        session3, "retained_projection_invariant", lambda *_args, **_kwargs: False
    )

    result = session3.run_finite_counterexample_experiment(
        _session3_config(tmp_path)
    )
    stress = json.loads(
        (result.run_dir / "stress_matrix.json").read_text("utf-8")
    )["relabeling"]

    assert stress["coherent"] is False
    assert stress["residual"] == "0"
    assert stress["status"] == "fail"
    assert result.status == "fail"


def test_nonzero_relabel_residual_alone_forces_session3_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    monkeypatch.setattr(
        session3, "retained_projection_invariant", lambda *_args, **_kwargs: True
    )
    monkeypatch.setattr(
        session3, "retained_projection_residual", lambda *_args, **_kwargs: Fraction(1)
    )

    result = session3.run_finite_counterexample_experiment(
        _session3_config(tmp_path)
    )
    stress = json.loads(
        (result.run_dir / "stress_matrix.json").read_text("utf-8")
    )["relabeling"]

    assert stress["coherent"] is True
    assert stress["residual"] == "1"
    assert stress["status"] == "fail"
    assert result.status == "fail"


def test_default_session3_is_inconclusive_with_candidate_boundary_outputs(
    tmp_path: Path,
):
    result = session3.run_finite_counterexample_experiment(
        _session3_config(tmp_path)
    )
    stress = json.loads(
        (result.run_dir / "stress_matrix.json").read_text("utf-8")
    )
    candidates = json.loads(
        (result.run_dir / "candidate_records.json").read_text("utf-8")
    )
    support_boundaries = [
        record for record in candidates if record["claim_id"] == "support_boundary"
    ]

    assert result.status == "inconclusive"
    assert stress["conditioning"]["status"] == "inconclusive"
    assert stress["conditioning"]["rejected_near_singular"]["decision"] == (
        "inconclusive"
    )
    assert {
        metric.verification_state for metric in result.metrics.values()
    } == {"CANDIDATE"}
    assert {record["verification_state"] for record in candidates} == {"CANDIDATE"}
    assert all(
        state in {"CANDIDATE", "INCONCLUSIVE"}
        for state in (
            *(metric.verification_state for metric in result.metrics.values()),
            *(record["verification_state"] for record in candidates),
        )
    )
    assert support_boundaries
    assert all(
        record["inside_declared_domain"] is False
        and record["assumptions_satisfied"] is False
        and record["classification"] == "assumption_boundary"
        and "absolute continuity"
        in record["smallest_witness"]["applicability"].lower()
        for record in support_boundaries
    )
