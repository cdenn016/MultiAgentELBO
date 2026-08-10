from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

from multiagent_elbo.config import NumericsConfig
from multiagent_elbo.finite.categorical import CategoricalExponentialFamily
from multiagent_elbo.finite.measures import MarkovKernel, ProbabilityMeasure


NUMERICS = NumericsConfig(dtype="float64", atol=1.0e-12, rtol=1.0e-10)
FIXTURE_PATH = Path(__file__).parent / "fixtures" / "two_scale_application_v1.json"
APPLICATION_ID = "30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd"


def _sut():
    try:
        import multiagent_elbo.finite.information_history as module
    except ModuleNotFoundError:
        pytest.fail("information-history implementation is missing", pytrace=False)
    return module


def _three_category_family() -> CategoricalExponentialFamily:
    return CategoricalExponentialFamily(
        ("x0", "x1", "x2"),
        (0.0, 0.0, 0.0),
        ((1.0, 0.0), (0.0, 1.0), (0.0, 0.0)),
        NUMERICS,
    )


def test_information_point_matches_independent_score_fisher_and_vfe_oracles():
    module = _sut()
    theta = (math.log(2.0), math.log(3.0))
    target = (1.0 / 2.0, 1.0 / 3.0, 1.0 / 6.0)

    point = module.categorical_information_point(
        _three_category_family(), theta, target, rcond=1.0e-12
    )

    expected_score = np.array(
        [
            [2.0 / 3.0, -1.0 / 2.0],
            [-1.0 / 3.0, 1.0 / 2.0],
            [-1.0 / 3.0, -1.0 / 2.0],
        ]
    )
    expected_fisher = np.array(
        [[2.0 / 9.0, -1.0 / 6.0], [-1.0 / 6.0, 1.0 / 4.0]]
    )
    log_ratio = np.array([math.log(2.0 / 3.0), math.log(3.0 / 2.0), 0.0])
    expected_gradient = np.array(
        [
            sum(q * score[0] * ratio for q, score, ratio in zip((1 / 3, 1 / 2, 1 / 6), expected_score, log_ratio, strict=True)),
            sum(q * score[1] * ratio for q, score, ratio in zip((1 / 3, 1 / 2, 1 / 6), expected_score, log_ratio, strict=True)),
        ]
    )
    expected_vector = -np.linalg.solve(expected_fisher, expected_gradient)

    np.testing.assert_allclose(point.probability, [1 / 3, 1 / 2, 1 / 6], atol=1e-15)
    np.testing.assert_allclose(point.score, expected_score, atol=1e-15)
    np.testing.assert_allclose(point.fisher, expected_fisher, atol=1e-15)
    np.testing.assert_allclose(point.vfe_gradient, expected_gradient, atol=1e-15)
    np.testing.assert_allclose(point.natural_gradient, expected_vector, atol=1e-14)
    assert point.rank == 2
    assert point.range_residual < 1.0e-14
    assert point.inverse_rule == "moore_penrose_identifiable_tangent_quotient"


def test_rank_deficient_fisher_uses_moore_penrose_quotient_without_hidden_inverse():
    module = _sut()
    family = CategoricalExponentialFamily(
        ("a", "b", "c"),
        (0.0, 0.0, 0.0),
        ((1.0, 2.0), (0.0, 0.0), (-1.0, -2.0)),
        NUMERICS,
    )

    point = module.categorical_information_point(
        family, (0.2, 0.1), (0.2, 0.3, 0.5), rcond=1.0e-12
    )

    assert point.rank == 1
    assert point.nullity == 1
    assert point.used_pseudoinverse is True
    assert point.range_residual < 1.0e-12
    np.testing.assert_allclose(
        point.fisher @ point.natural_gradient,
        -point.vfe_gradient,
        atol=1.0e-12,
    )


def test_finite_difference_score_matches_the_analytic_open_family_score():
    module = _sut()
    family = _three_category_family()
    theta = (math.log(2.0), math.log(3.0))

    finite_difference = module.finite_difference_score(family, theta, 1.0e-5)

    np.testing.assert_allclose(finite_difference, family.score(theta), atol=1.0e-8)


def test_fixed_channel_diagnostics_match_literal_fisher_loss_and_fd_score():
    module = _sut()
    family = _three_category_family()
    channel = MarkovKernel(
        family.labels,
        ("z0", "z1"),
        ((1.0, 0.0), (0.0, 1.0), (0.5, 0.5)),
        NUMERICS,
    )

    result = module.fixed_channel_diagnostics(
        family,
        (math.log(2.0), math.log(3.0)),
        channel,
        finite_difference_step=1.0e-5,
    )

    np.testing.assert_allclose(
        result.fisher_result.coarse_score,
        [[7.0 / 15.0, -1.0 / 2.0], [-1.0 / 3.0, 5.0 / 14.0]],
        atol=1.0e-15,
    )
    np.testing.assert_allclose(
        result.fisher_result.conditional_covariance,
        [[1.0 / 15.0, 0.0], [0.0, 1.0 / 14.0]],
        atol=1.0e-15,
    )
    assert result.score_finite_difference_residual < 1.0e-8
    assert result.fisher_defect_residual < 1.0e-14
    assert result.channel_scope == "declared_fixed_parameter_independent"
    assert result.establishes_dqm is False


def test_parameter_dependent_channel_control_is_outside_the_fixed_channel_theorem():
    module = _sut()

    control = module.parameter_dependent_channel_counterexample(
        NUMERICS, finite_difference_step=1.0e-5
    )

    np.testing.assert_allclose(control.conditional_expected_score, [[0.0], [0.0]], atol=1e-15)
    np.testing.assert_allclose(control.actual_coarse_score, [[0.5], [-0.5]], atol=1e-8)
    assert control.gap == pytest.approx(0.5, abs=1.0e-8)
    assert control.inside_fixed_channel_theorem is False
    assert control.classification == "assumption_boundary_witness_not_theorem_refutation"


def test_recovery_diagnostics_separate_directional_pointwise_and_global_claims():
    module = _sut()
    labels = ("00", "01", "10", "11")
    probability = ProbabilityMeasure(labels, (0.25,) * 4, NUMERICS)
    channel = MarkovKernel(
        labels,
        ("left", "right"),
        ((1.0, 0.0), (1.0, 0.0), (0.0, 1.0), (0.0, 1.0)),
        NUMERICS,
    )
    score = np.array(
        [[-1.0, -1.0], [-1.0, 1.0], [1.0, -1.0], [1.0, 1.0]]
    )

    result = module.recovery_diagnostics(probability, score, channel)

    np.testing.assert_allclose(result.fisher_defect, [[0.0, 0.0], [0.0, 1.0]])
    assert result.recoverable_direction_dimension == 1
    assert result.pointwise_full_fisher_equality is False
    assert result.global_experiment_recovery_claimed is False


def test_two_histories_with_identical_endpoints_have_different_fisher_durations():
    module = _sut()
    family = _three_category_family()
    straight = np.array([[-0.6, -0.4], [0.0, 0.0], [0.6, 0.4]])
    detour = np.array([[-0.6, -0.4], [-0.5, 0.9], [0.6, 0.4]])

    straight_duration = module.fisher_path_duration(family, straight)
    detour_duration = module.fisher_path_duration(family, detour)

    np.testing.assert_array_equal(straight[0], detour[0])
    np.testing.assert_array_equal(straight[-1], detour[-1])
    assert detour_duration[-1] > straight_duration[-1] + 0.05


def test_chart_reparameterization_changes_raw_speed_but_not_information_duration():
    module = _sut()
    family = _three_category_family()
    history = np.array([[-0.4, 0.1], [-0.1, 0.2], [0.3, 0.25]])

    diagnostic = module.linear_chart_reparameterization_diagnostic(
        family, history, chart_scale=2.0
    )

    assert diagnostic.raw_coordinate_length_ratio == pytest.approx(2.0)
    assert diagnostic.information_duration_residual < 1.0e-14


def test_semiconjugacy_defect_uses_the_typed_minus_sign_and_rejects_plus_mutation():
    module = _sut()
    coarse_map = np.array([[0.5, 0.5, 0.0], [0.0, 0.5, 0.5]])
    fine_vector = np.array([2.0, -1.0, 3.0])
    coarse_vector = np.array([0.25, -0.75])
    literal_oracle = np.array([0.25, 1.75])

    defect = module.semiconjugacy_defect(coarse_map, fine_vector, coarse_vector)
    plus_sign_mutation = coarse_map @ fine_vector + coarse_vector

    np.testing.assert_allclose(defect, literal_oracle, atol=0.0)
    assert not np.allclose(plus_sign_mutation, literal_oracle)


def test_frozen_fixture_builds_the_declared_fine_and_coarse_statistical_charts():
    module = _sut()
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    model = module.build_information_history_model(payload, NUMERICS)

    assert model.application_id == APPLICATION_ID
    assert model.fine_family.labels == tuple(f"{value:04b}" for value in range(16))
    assert model.fine_family.parameter_count == 4
    assert model.coarse_family.labels == ("00", "01", "10", "11")
    assert model.coarse_family.parameter_count == 2
    np.testing.assert_allclose(
        model.coarse_map,
        [[0.5, 0.5, 0.0, 0.0], [0.0, 0.0, 0.5, 0.5]],
    )
    assert model.family_scope == "finite_positive_categorical_softmax_open_chart"


def test_default_history_has_separate_orbit_rg_duration_and_nonzero_defect_records():
    module = _sut()
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    model = module.build_information_history_model(payload, NUMERICS)

    history = module.simulate_information_history(
        model, history_steps=16, step_size=0.05
    )

    assert history.fine_parameters.shape == (16, 4)
    assert history.coarse_parameters.shape == (16, 2)
    assert history.inference_orbit_parameter.shape == (16,)
    np.testing.assert_array_equal(history.rg_depth, [0.0, 1.0])
    assert history.information_duration.shape == (16,)
    assert history.wall_time_seconds >= 0.0
    assert history.semiconjugacy_defects.shape == (16, 2)
    assert np.max(history.semiconjugacy_defect_norms) > 1.0e-3
    assert np.all(np.diff(history.information_duration) >= 0.0)
    assert all(not array.flags.writeable for array in history.semantic_arrays())
