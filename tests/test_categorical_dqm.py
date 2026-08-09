from __future__ import annotations

import math
import warnings

import numpy as np
import pytest

from multiagent_elbo.config import NumericsConfig
from multiagent_elbo.finite.categorical import CategoricalExponentialFamily
from multiagent_elbo.finite.categorical_dqm import (
    analyze_categorical_dqm,
    centered_log_probability_finite_difference,
    centered_pushed_log_probability_finite_difference,
    normalized_dqm_remainder_ladder,
)
from multiagent_elbo.finite.measures import MarkovKernel


LABELS = ("x0", "x1", "x2")
BASE_LOGITS = (0.0, 0.0, 0.0)
STATISTICS = ((1.0, 0.0), (0.0, 1.0), (0.0, 0.0))
NUMERICS = NumericsConfig(dtype="float64", atol=1e-12, rtol=1e-10)
THETA = (math.log(2.0), math.log(3.0))


def _family() -> CategoricalExponentialFamily:
    return CategoricalExponentialFamily(
        LABELS, BASE_LOGITS, STATISTICS, NUMERICS
    )


def _channel() -> MarkovKernel:
    return MarkovKernel(
        LABELS,
        ("z0", "z1"),
        ((1.0, 0.0), (0.0, 1.0), (0.5, 0.5)),
        NUMERICS,
    )


def test_family_matches_hand_derived_probability_score_and_fisher():
    family = _family()

    np.testing.assert_allclose(
        family.probabilities(THETA), [1.0 / 3.0, 1.0 / 2.0, 1.0 / 6.0]
    )
    np.testing.assert_allclose(
        family.score(THETA),
        [
            [2.0 / 3.0, -1.0 / 2.0],
            [-1.0 / 3.0, 1.0 / 2.0],
            [-1.0 / 3.0, -1.0 / 2.0],
        ],
    )
    np.testing.assert_allclose(
        family.fisher_information(THETA),
        [[2.0 / 9.0, -1.0 / 6.0], [-1.0 / 6.0, 1.0 / 4.0]],
    )
    np.testing.assert_allclose(
        family.log_probabilities(THETA),
        [math.log(1.0 / 3.0), math.log(1.0 / 2.0), math.log(1.0 / 6.0)],
    )
    measure = family.probability_measure(THETA)
    assert measure.labels == LABELS
    np.testing.assert_allclose(
        measure.masses, [1.0 / 3.0, 1.0 / 2.0, 1.0 / 6.0]
    )


@pytest.mark.parametrize(
    "theta",
    [(0.0, 0.0), (math.log(2.0), math.log(3.0)), (-0.75, 1.25)],
)
def test_analytic_score_is_centered_at_three_literal_parameters(theta):
    family = _family()

    weighted_score = family.probabilities(theta) @ family.score(theta)

    np.testing.assert_allclose(weighted_score, [0.0, 0.0], atol=1e-15)


def test_family_defensively_owns_inputs_and_returns_read_only_float64_arrays():
    base_logits = np.zeros(3, dtype=np.float32)
    statistics = np.array(STATISTICS, dtype=np.float32)
    theta = np.array(THETA, dtype=np.float32)
    family = CategoricalExponentialFamily(
        LABELS, base_logits, statistics, NUMERICS
    )
    base_logits[:] = 100.0
    statistics[:] = 100.0

    outputs = (
        family.base_logits,
        family.sufficient_statistics,
        family.log_probabilities(theta),
        family.probabilities(theta),
        family.score(theta),
        family.fisher_information(theta),
    )

    np.testing.assert_allclose(family.base_logits, BASE_LOGITS)
    np.testing.assert_allclose(family.sufficient_statistics, STATISTICS)
    for array in outputs:
        assert array.dtype == np.dtype(np.float64)
        assert not array.flags.writeable
        with pytest.raises(ValueError):
            array.flat[0] = 0.0


def test_centered_fine_log_probability_difference_matches_analytic_score():
    family = _family()

    finite_difference = centered_log_probability_finite_difference(
        family, THETA, 1.0e-5
    )

    assert np.max(np.abs(finite_difference - family.score(THETA))) < 1.0e-8


def test_centered_pushed_difference_matches_hand_derived_conditional_score():
    finite_difference = centered_pushed_log_probability_finite_difference(
        _family(), THETA, _channel(), 1.0e-5
    )

    expected = np.array(
        [[7.0 / 15.0, -1.0 / 2.0], [-1.0 / 3.0, 5.0 / 14.0]]
    )
    assert np.max(np.abs(finite_difference - expected)) < 1.0e-8


def test_centered_fine_difference_avoids_overflowing_doubled_step():
    family = CategoricalExponentialFamily(
        ("x0", "x1"),
        (0.0, 0.0),
        ((1.0e-308,), (-1.0e-308,)),
        NUMERICS,
    )

    with warnings.catch_warnings(), np.errstate(under="warn"):
        warnings.simplefilter("error", RuntimeWarning)
        finite_difference = centered_log_probability_finite_difference(
            family, (0.0,), 1.0e308
        )

    np.testing.assert_allclose(
        finite_difference,
        [[1.0e-308], [-1.0e-308]],
        rtol=2.0e-15,
        atol=0.0,
    )


def test_centered_pushed_difference_avoids_overflowing_doubled_step():
    family = CategoricalExponentialFamily(
        ("x0", "x1"),
        (0.0, 0.0),
        ((1.0e-308,), (-1.0e-308,)),
        NUMERICS,
    )
    swap = MarkovKernel(
        ("x0", "x1"),
        ("z0", "z1"),
        ((0.0, 1.0), (1.0, 0.0)),
        NUMERICS,
    )

    with warnings.catch_warnings(), np.errstate(under="warn"):
        warnings.simplefilter("error", RuntimeWarning)
        finite_difference = centered_pushed_log_probability_finite_difference(
            family, (0.0,), swap, 1.0e308
        )

    np.testing.assert_allclose(
        finite_difference,
        [[-1.0e-308], [1.0e-308]],
        rtol=2.0e-15,
        atol=0.0,
    )


def test_analysis_matches_hand_derived_fisher_channel_identity():
    analysis = analyze_categorical_dqm(
        _family(),
        THETA,
        _channel(),
        1.0e-5,
        (3.0 / 5.0, -4.0 / 5.0),
        (0.1, 0.05, 0.025, 0.0125),
    )

    np.testing.assert_allclose(
        analysis.base_probability, [1.0 / 3.0, 1.0 / 2.0, 1.0 / 6.0]
    )
    np.testing.assert_allclose(
        analysis.fisher_channel_result.coarse_probability,
        [5.0 / 12.0, 7.0 / 12.0],
    )
    np.testing.assert_allclose(
        analysis.fisher_channel_result.coarse_fisher,
        [[7.0 / 45.0, -1.0 / 6.0], [-1.0 / 6.0, 5.0 / 28.0]],
    )
    np.testing.assert_allclose(
        analysis.fisher_channel_result.conditional_covariance,
        [[1.0 / 15.0, 0.0], [0.0, 1.0 / 14.0]],
        atol=1.0e-15,
    )
    assert np.max(np.abs(analysis.fisher_channel_result.residual)) < 1.0e-12
    assert analysis.family_scope == "finite_positive_smooth_exponential_family"
    assert analysis.channel_scope == "declared_fixed_parameter_independent"


def test_two_sided_dqm_remainder_matches_pinned_ladders_and_decreases():
    ladder = normalized_dqm_remainder_ladder(
        _family(),
        THETA,
        (3.0 / 5.0, -4.0 / 5.0),
        (0.1, 0.05, 0.025, 0.0125),
    )

    np.testing.assert_allclose(
        ladder.positive,
        [0.00559638, 0.00280237, 0.00140217, 0.000701326],
        rtol=0.0,
        atol=5.0e-9,
    )
    np.testing.assert_allclose(
        ladder.negative,
        [0.00562600, 0.00280979, 0.00140403, 0.000701790],
        rtol=0.0,
        atol=5.0e-9,
    )
    assert np.all(np.diff(ladder.positive) < 0.0)
    assert np.all(np.diff(ladder.negative) < 0.0)
    for array in (ladder.step_sizes, ladder.positive, ladder.negative):
        assert array.dtype == np.dtype(np.float64)
        assert not array.flags.writeable
        with pytest.raises(ValueError):
            array.flat[0] = 0.0


@pytest.mark.parametrize(
    ("labels", "base_logits", "statistics", "message"),
    [
        ((), (), np.empty((0, 2)), "at least two"),
        (("x",), (0.0,), ((1.0,),), "at least two"),
        (("x", "x"), (0.0, 0.0), ((1.0,), (0.0,)), "unique"),
        (LABELS, (0.0, 0.0), STATISTICS, "one entry per label"),
        (LABELS, BASE_LOGITS, ((1.0, 0.0),), "one row per label"),
        (LABELS, BASE_LOGITS, np.empty((3, 0)), "at least one parameter"),
        (LABELS, (0.0, np.nan, 0.0), STATISTICS, "finite"),
        (
            LABELS,
            BASE_LOGITS,
            ((1.0, 0.0), (0.0, np.inf), (0.0, 0.0)),
            "finite",
        ),
    ],
)
def test_family_rejects_malformed_shapes_labels_and_nonfinite_data(
    labels, base_logits, statistics, message
):
    with pytest.raises(ValueError, match=message):
        CategoricalExponentialFamily(labels, base_logits, statistics, NUMERICS)


@pytest.mark.parametrize(
    ("theta", "message"),
    [
        ((True, False), "Boolean"),
        ((0.0,), "one entry per parameter"),
        ((0.0, 0.0, 0.0), "one entry per parameter"),
        ((np.nan, 0.0), "finite"),
        ((np.inf, 0.0), "finite"),
    ],
)
def test_family_rejects_boolean_wrong_shape_and_nonfinite_theta(theta, message):
    with pytest.raises((TypeError, ValueError), match=message):
        _family().probabilities(theta)


def test_family_rejects_nonfinite_matrix_products_before_returning_a_result():
    family = CategoricalExponentialFamily(
        ("x", "y"), (0.0, 0.0), ((1.0e308,), (0.0,)), NUMERICS
    )

    with pytest.raises(ValueError, match="nonfinite categorical matrix product"):
        family.log_probabilities((2.0,))


def test_family_rejects_float64_underflow_that_erases_source_support():
    family = CategoricalExponentialFamily(
        ("x", "y"), (0.0, -1000.0), ((0.0,), (0.0,)), NUMERICS
    )

    with pytest.raises(ValueError, match="strictly positive"):
        family.probabilities((0.0,))


@pytest.mark.parametrize("step", [0.0, -1.0e-5, np.nan, np.inf, True])
def test_finite_differences_reject_nonpositive_nonfinite_and_boolean_steps(step):
    with pytest.raises((TypeError, ValueError), match="step"):
        centered_log_probability_finite_difference(_family(), THETA, step)
    with pytest.raises((TypeError, ValueError), match="step"):
        centered_pushed_log_probability_finite_difference(
            _family(), THETA, _channel(), step
        )


@pytest.mark.parametrize(
    ("direction", "message"),
    [
        ((1.0, 1.0), "unit"),
        ((0.0, 0.0), "unit"),
        ((1.0,), "one entry per parameter"),
        ((np.inf, 0.0), "finite"),
    ],
)
def test_dqm_ladder_rejects_nonunit_wrong_shape_and_nonfinite_directions(
    direction, message
):
    with pytest.raises(ValueError, match=message):
        normalized_dqm_remainder_ladder(
            _family(), THETA, direction, (0.1, 0.05)
        )


@pytest.mark.parametrize(
    ("step_sizes", "message"),
    [
        ((), "nonempty"),
        ((0.05, 0.1), "strictly decreasing"),
        ((0.1, 0.1), "strictly decreasing"),
        ((0.1, 0.0), "positive"),
        ((0.1, np.nan), "finite"),
    ],
)
def test_dqm_ladder_rejects_empty_unordered_duplicate_and_invalid_steps(
    step_sizes, message
):
    with pytest.raises(ValueError, match=message):
        normalized_dqm_remainder_ladder(
            _family(), THETA, (3.0 / 5.0, -4.0 / 5.0), step_sizes
        )


def test_finite_difference_rejects_a_coordinate_perturbation_that_rounds_back():
    with pytest.raises(ValueError, match="rounds back"):
        centered_log_probability_finite_difference(
            _family(), (1.0e20, 1.0e20), 1.0e-5
        )


def test_dqm_ladder_rejects_a_directional_perturbation_that_rounds_back():
    flat_family = CategoricalExponentialFamily(
        LABELS,
        BASE_LOGITS,
        ((1.0, 0.0), (1.0, 0.0), (1.0, 0.0)),
        NUMERICS,
    )

    with pytest.raises(ValueError, match="rounds back"):
        normalized_dqm_remainder_ladder(
            flat_family, (1.0e20, 0.0), (1.0, 0.0), (1.0e-5,)
        )


def test_dqm_ladder_rejects_partial_round_back_in_a_nonzero_direction_coordinate():
    flat_family = CategoricalExponentialFamily(
        LABELS,
        BASE_LOGITS,
        ((1.0, 1.0), (1.0, 1.0), (1.0, 1.0)),
        NUMERICS,
    )

    with pytest.raises(ValueError, match="rounds back"):
        normalized_dqm_remainder_ladder(
            flat_family,
            (1.0e20, 0.0),
            (3.0 / 5.0, 4.0 / 5.0),
            (1.0e-5,),
        )


def test_pushed_finite_difference_rejects_zero_target_probability():
    channel = MarkovKernel(
        LABELS,
        ("reachable", "unreachable"),
        ((1.0, 0.0), (1.0, 0.0), (1.0, 0.0)),
        NUMERICS,
    )

    with pytest.raises(ValueError, match="strictly positive"):
        centered_pushed_log_probability_finite_difference(
            _family(), THETA, channel, 1.0e-5
        )


def test_pushed_finite_difference_rejects_mismatched_labels_and_numerics():
    wrong_labels = MarkovKernel(
        ("x1", "x0", "x2"),
        ("z",),
        ((1.0,), (1.0,), (1.0,)),
        NUMERICS,
    )
    loose = NumericsConfig(dtype="float64", atol=1e-8, rtol=1e-7)
    wrong_numerics = MarkovKernel(
        LABELS, ("z",), ((1.0,), (1.0,), (1.0,)), loose
    )

    with pytest.raises(ValueError, match="source labels"):
        centered_pushed_log_probability_finite_difference(
            _family(), THETA, wrong_labels, 1.0e-5
        )
    with pytest.raises(ValueError, match="numerics"):
        centered_pushed_log_probability_finite_difference(
            _family(), THETA, wrong_numerics, 1.0e-5
        )


def test_finite_difference_and_analysis_arrays_are_defensive_read_only_float64():
    analysis = analyze_categorical_dqm(
        _family(),
        THETA,
        _channel(),
        1.0e-5,
        (3.0 / 5.0, -4.0 / 5.0),
        (0.1, 0.05),
    )
    arrays = (
        centered_log_probability_finite_difference(_family(), THETA, 1.0e-5),
        centered_pushed_log_probability_finite_difference(
            _family(), THETA, _channel(), 1.0e-5
        ),
        analysis.base_probability,
        analysis.analytic_fine_score,
        analysis.finite_difference_fine_score,
        analysis.finite_difference_pushed_score,
    )

    assert analysis.fisher_channel_result.establishes_dqm is False
    for array in arrays:
        assert array.dtype == np.dtype(np.float64)
        assert not array.flags.writeable
        with pytest.raises(ValueError):
            array.flat[0] = 0.0
