from __future__ import annotations

import numpy as np
import pytest

from multiagent_elbo.config import NumericsConfig
from multiagent_elbo.finite.fisher import fisher_channel_decomposition
from multiagent_elbo.finite.measures import MarkovKernel, ProbabilityMeasure


NUMERICS = NumericsConfig(dtype="float64", atol=1e-12, rtol=1e-10)


def test_deterministic_channel_matches_literal_conditional_covariance_identity():
    labels = ("0", "1", "2", "3")
    probability = ProbabilityMeasure(labels, (0.25, 0.25, 0.25, 0.25), NUMERICS)
    channel = MarkovKernel(
        labels,
        ("A", "B"),
        ((1.0, 0.0), (1.0, 0.0), (0.0, 1.0), (0.0, 1.0)),
        NUMERICS,
    )

    result = fisher_channel_decomposition(
        probability, (-1.5, -0.5, 0.5, 1.5), channel
    )

    assert result.joint_mass.shape == (4, 2)
    assert result.coarse_probability.shape == (2,)
    assert result.coarse_score.shape == (2, 1)
    assert result.fine_fisher.shape == (1, 1)
    assert result.coarse_fisher.shape == (1, 1)
    assert result.conditional_covariance.shape == (1, 1)
    assert result.residual.shape == (1, 1)
    np.testing.assert_allclose(result.fine_fisher, [[1.25]])
    np.testing.assert_allclose(result.coarse_score, [[-1.0], [1.0]])
    np.testing.assert_allclose(result.coarse_fisher, [[1.0]])
    np.testing.assert_allclose(result.conditional_covariance, [[0.25]])
    np.testing.assert_allclose(result.residual, [[0.0]], atol=1e-12)


def test_stochastic_channel_uses_joint_mass_weights_not_uniform_averages():
    labels = ("x0", "x1", "x2")
    probability = ProbabilityMeasure(labels, (0.5, 1.0 / 3.0, 1.0 / 6.0), NUMERICS)
    channel = MarkovKernel(
        labels,
        ("z0", "z1"),
        ((1.0, 0.0), (0.5, 0.5), (0.0, 1.0)),
        NUMERICS,
    )

    result = fisher_channel_decomposition(probability, (-1.0, 1.0, 1.0), channel)

    assert result.coarse_probability == pytest.approx([2.0 / 3.0, 1.0 / 3.0])
    np.testing.assert_allclose(result.coarse_score, [[-0.5], [1.0]])
    np.testing.assert_allclose(result.fine_fisher, [[1.0]])
    np.testing.assert_allclose(result.coarse_fisher, [[0.5]])
    np.testing.assert_allclose(result.conditional_covariance, [[0.5]])
    np.testing.assert_allclose(result.residual, [[0.0]], atol=1e-12)


def test_identity_channel_has_zero_information_loss():
    labels = ("0", "1", "2", "3")
    probability = ProbabilityMeasure(labels, (0.25,) * 4, NUMERICS)
    identity = MarkovKernel(labels, labels, np.eye(4), NUMERICS)

    result = fisher_channel_decomposition(
        probability, (-1.5, -0.5, 0.5, 1.5), identity
    )

    np.testing.assert_allclose(result.conditional_covariance, [[0.0]], atol=1e-12)
    np.testing.assert_allclose(result.coarse_fisher, result.fine_fisher)


def test_lossy_channel_can_recover_a_fiber_constant_score():
    labels = ("0", "1", "2", "3")
    probability = ProbabilityMeasure(labels, (0.25,) * 4, NUMERICS)
    lossy = MarkovKernel(
        labels,
        ("A", "B"),
        ((1.0, 0.0), (1.0, 0.0), (0.0, 1.0), (0.0, 1.0)),
        NUMERICS,
    )

    result = fisher_channel_decomposition(
        probability, (-1.0, -1.0, 1.0, 1.0), lossy
    )

    np.testing.assert_allclose(result.conditional_covariance, [[0.0]], atol=1e-12)
    assert result.minimum_defect_eigenvalue == pytest.approx(0.0, abs=1e-12)


def test_zero_score_is_a_valid_zero_tangent_and_unreachable_targets_use_zero_representative():
    labels = ("x", "y")
    probability = ProbabilityMeasure(labels, (0.5, 0.5), NUMERICS)
    channel = MarkovKernel(
        labels,
        ("seen", "unreachable"),
        ((1.0, 0.0), (1.0, 0.0)),
        NUMERICS,
    )

    result = fisher_channel_decomposition(probability, (0.0, 0.0), channel)

    assert result.coarse_probability == pytest.approx([1.0, 0.0])
    np.testing.assert_allclose(result.coarse_score, [[0.0], [0.0]])
    np.testing.assert_allclose(result.fine_fisher, [[0.0]])
    np.testing.assert_allclose(result.conditional_covariance, [[0.0]])


def test_nonzero_constant_score_is_rejected_as_not_centered():
    labels = ("x", "y")
    probability = ProbabilityMeasure(labels, (0.5, 0.5), NUMERICS)
    identity = MarkovKernel(labels, labels, np.eye(2), NUMERICS)

    with pytest.raises(ValueError, match="centered"):
        fisher_channel_decomposition(probability, (1.0, 1.0), identity)


def test_centering_check_scales_each_parameter_coordinate_independently():
    labels = ("x", "y")
    probability = ProbabilityMeasure(labels, (0.5, 0.5), NUMERICS)
    identity = MarkovKernel(labels, labels, np.eye(2), NUMERICS)
    score = np.array([[1.0e12, 1.0], [-1.0e12 + 100.0, -1.0]])

    result = fisher_channel_decomposition(probability, score, identity)

    assert result.fine_fisher.shape == (2, 2)


def test_two_parameter_defect_may_be_singular_positive_semidefinite():
    labels = ("0", "1", "2", "3")
    probability = ProbabilityMeasure(labels, (0.25,) * 4, NUMERICS)
    lossy = MarkovKernel(
        labels,
        ("A", "B"),
        ((1.0, 0.0), (1.0, 0.0), (0.0, 1.0), (0.0, 1.0)),
        NUMERICS,
    )
    score = np.array(
        [[-1.5, -1.0], [-0.5, 1.0], [0.5, -1.0], [1.5, 1.0]]
    )

    result = fisher_channel_decomposition(probability, score, lossy)

    np.testing.assert_allclose(
        result.conditional_covariance, [[0.25, 0.5], [0.5, 1.0]]
    )
    assert np.linalg.eigvalsh(result.conditional_covariance) == pytest.approx(
        [0.0, 1.25], abs=1e-12
    )
    assert result.minimum_defect_eigenvalue == pytest.approx(0.0, abs=1e-12)
    assert result.defect_is_psd


def test_result_arrays_are_read_only_defensive_copies():
    labels = ("x", "y")
    masses = np.array([0.5, 0.5])
    score = np.array([-1.0, 1.0])
    kernel_matrix = np.eye(2)
    probability = ProbabilityMeasure(labels, masses, NUMERICS)
    identity = MarkovKernel(labels, labels, kernel_matrix, NUMERICS)

    result = fisher_channel_decomposition(probability, score, identity)
    score[:] = 9.0
    masses[:] = (1.0, 0.0)
    kernel_matrix[:] = 0.5

    np.testing.assert_allclose(result.coarse_score, [[-1.0], [1.0]])
    for array in (
        result.joint_mass,
        result.coarse_probability,
        result.coarse_score,
        result.fine_fisher,
        result.coarse_fisher,
        result.conditional_covariance,
        result.residual,
    ):
        assert not array.flags.writeable
        with pytest.raises(ValueError):
            array.flat[0] = 0.0


@pytest.mark.parametrize(
    ("score", "message"),
    [
        ([[1.0, -1.0]], "one row per source state"),
        ([[-1.0], [1.0], [0.0]], "one row per source state"),
        ([[0.0, np.inf], [0.0, -np.inf]], "finite"),
        (np.zeros((2, 1, 1)), "one- or two-dimensional"),
    ],
)
def test_score_validation_rejects_wrong_shapes_and_nonfinite_values(score, message):
    labels = ("x", "y")
    probability = ProbabilityMeasure(labels, (0.5, 0.5), NUMERICS)
    identity = MarkovKernel(labels, labels, np.eye(2), NUMERICS)

    with pytest.raises(ValueError, match=message):
        fisher_channel_decomposition(probability, score, identity)


def test_probability_and_channel_must_share_source_labels_and_numerics():
    probability = ProbabilityMeasure(("x", "y"), (0.5, 0.5), NUMERICS)
    wrong_labels = MarkovKernel(("y", "x"), ("a",), ((1.0,), (1.0,)), NUMERICS)
    loose = NumericsConfig(dtype="float64", atol=1e-8, rtol=1e-7)
    wrong_numerics = MarkovKernel(("x", "y"), ("a",), ((1.0,), (1.0,)), loose)

    with pytest.raises(ValueError, match="source labels"):
        fisher_channel_decomposition(probability, (-1.0, 1.0), wrong_labels)
    with pytest.raises(ValueError, match="numerics"):
        fisher_channel_decomposition(probability, (-1.0, 1.0), wrong_numerics)


def test_finite_scores_that_overflow_fisher_products_are_rejected_not_called_psd():
    labels = ("x", "y")
    probability = ProbabilityMeasure(labels, (0.5, 0.5), NUMERICS)
    lossy = MarkovKernel(labels, ("z",), ((1.0,), (1.0,)), NUMERICS)

    with pytest.raises(ValueError, match="nonfinite Fisher"):
        fisher_channel_decomposition(probability, (-1.0e308, 1.0e308), lossy)
