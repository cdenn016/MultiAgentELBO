from __future__ import annotations

import math

import numpy as np
import pytest

from multiagent_elbo.finite.interactions import (
    hoeffding_decompose,
    retain_interaction_order,
)


UNIFORM_BINARY = (np.array([0.5, 0.5]),) * 4
SPINS = np.array([-1.0, 1.0])


def test_pure_three_spin_interaction_has_only_the_triple_component():
    x1, x2, x3 = np.meshgrid(SPINS, SPINS, SPINS, indexing="ij")
    values = 0.7 * x1 * x2 * x3

    result = hoeffding_decompose(values, UNIFORM_BINARY[:3])

    assert float(result.components[()]) == pytest.approx(0.0, abs=1e-12)
    for subset in ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2)):
        np.testing.assert_allclose(result.components[subset], 0.0, atol=1e-12)
    np.testing.assert_allclose(result.components[(0, 1, 2)], values, atol=1e-12)
    np.testing.assert_allclose(result.reconstruction, values, atol=1e-12)
    assert result.reconstruction_residual_sup < 1e-12


def test_pairwise_retention_reports_three_distinct_residual_norms():
    x1, x2, x3, x4 = np.meshgrid(SPINS, SPINS, SPINS, SPINS, indexing="ij")
    values = 0.3 * x1 * x2 * x3 + 0.4 * x1 * x2 * x4

    decomposition = hoeffding_decompose(values, UNIFORM_BINARY)
    projection = retain_interaction_order(decomposition, 2)

    assert set(projection.omitted_components) == {
        (0, 1, 2),
        (0, 1, 3),
        (0, 2, 3),
        (1, 2, 3),
        (0, 1, 2, 3),
    }
    assert np.max(np.abs(projection.omitted_components[(0, 1, 2)])) == pytest.approx(0.3)
    assert np.max(np.abs(projection.omitted_components[(0, 1, 3)])) == pytest.approx(0.4)
    np.testing.assert_allclose(projection.omitted_components[(0, 2, 3)], 0.0, atol=1e-12)
    np.testing.assert_allclose(projection.omitted_components[(1, 2, 3)], 0.0, atol=1e-12)
    np.testing.assert_allclose(projection.omitted_components[(0, 1, 2, 3)], 0.0, atol=1e-12)
    assert projection.theorem_coordinate_g_norm == pytest.approx(0.7)
    assert projection.quotient_sup_norm == pytest.approx(0.7)
    assert projection.weighted_l2_diagnostic == pytest.approx(0.5)
    np.testing.assert_allclose(projection.retained_values, 0.0, atol=1e-12)
    np.testing.assert_allclose(projection.omitted_values, values, atol=1e-12)


def test_nonuniform_product_reference_uses_declared_axis_weights():
    x1, x2 = np.meshgrid(SPINS, SPINS, indexing="ij")
    values = x1 * x2
    references = (np.array([0.75, 0.25]), np.array([0.2, 0.8]))

    result = hoeffding_decompose(values, references)

    assert float(result.components[()]) == pytest.approx(-0.3)
    np.testing.assert_allclose(result.components[(0,)], [-0.3, 0.9])
    np.testing.assert_allclose(result.components[(1,)], [0.8, -0.2])
    np.testing.assert_allclose(
        result.components[(0, 1)], [[0.8, -0.2], [-2.4, 0.6]]
    )
    np.testing.assert_allclose(result.reconstruction, values, atol=1e-12)
    assert result.reconstruction_residual_sup < 1e-12


def test_retaining_all_orders_has_zero_omitted_residual():
    values = np.arange(8.0).reshape(2, 2, 2)
    decomposition = hoeffding_decompose(values, UNIFORM_BINARY[:3])

    projection = retain_interaction_order(decomposition, 3)

    assert projection.omitted_components == {}
    assert projection.theorem_coordinate_g_norm == 0.0
    assert projection.quotient_sup_norm == 0.0
    assert projection.weighted_l2_diagnostic == 0.0
    np.testing.assert_allclose(projection.retained_values, values, atol=1e-12)


def test_interaction_results_are_read_only_defensive_copies():
    values = np.array([[-1.0, 1.0], [2.0, -2.0]])
    first_reference = np.array([0.5, 0.5])
    second_reference = np.array([0.5, 0.5])

    decomposition = hoeffding_decompose(
        values, (first_reference, second_reference)
    )
    projection = retain_interaction_order(decomposition, 1)
    values[:] = 99.0
    first_reference[:] = (1.0, 0.0)

    np.testing.assert_allclose(decomposition.values, [[-1.0, 1.0], [2.0, -2.0]])
    with pytest.raises(TypeError):
        decomposition.components[(0,)] = np.array([0.0, 0.0])
    for array in (
        decomposition.values,
        decomposition.reconstruction,
        *decomposition.axis_references,
        *decomposition.components.values(),
        projection.retained_values,
        projection.omitted_values,
        *projection.omitted_components.values(),
    ):
        assert not array.flags.writeable
        with pytest.raises(ValueError):
            array.flat[0] = 0.0


@pytest.mark.parametrize(
    ("values", "references", "message"),
    [
        (np.ones((2, 2)), ([0.5, 0.5],), "one reference per value axis"),
        (np.ones((2, 2)), ([0.5, 0.5], [1.0]), "length"),
        (np.ones((2, 2)), ([0.5, 0.5], [0.6, 0.6]), "sum to one"),
        (np.ones((2, 2)), ([0.5, 0.5], [-0.1, 1.1]), "nonnegative"),
        (np.array([[0.0, math.inf], [0.0, 0.0]]), ([0.5, 0.5],) * 2, "finite"),
    ],
)
def test_interaction_input_validation(values, references, message):
    with pytest.raises(ValueError, match=message):
        hoeffding_decompose(values, references)


@pytest.mark.parametrize("order", [True, 0, -1, 1.5, 4])
def test_retained_order_must_be_an_available_positive_integer(order):
    decomposition = hoeffding_decompose(
        np.ones((2, 2, 2)), UNIFORM_BINARY[:3]
    )

    with pytest.raises((TypeError, ValueError), match="order"):
        retain_interaction_order(decomposition, order)


def test_representable_large_residual_norms_do_not_overflow():
    values = np.array([[1.0e308, -1.0e308], [-1.0e308, 1.0e308]])
    decomposition = hoeffding_decompose(values, UNIFORM_BINARY[:2])

    projection = retain_interaction_order(decomposition, 1)

    assert projection.theorem_coordinate_g_norm == pytest.approx(1.0e308)
    assert projection.quotient_sup_norm == pytest.approx(1.0e308)
    assert projection.weighted_l2_diagnostic == pytest.approx(1.0e308)
    assert math.isfinite(projection.quotient_sup_norm)
    assert math.isfinite(projection.weighted_l2_diagnostic)


def test_tolerantly_accepted_references_are_normalized_before_projection():
    decomposition = hoeffding_decompose(
        np.ones(2), (np.array([0.5, 0.50000000005]),)
    )

    assert float(decomposition.components[()]) == pytest.approx(1.0)
    np.testing.assert_allclose(decomposition.components[(0,)], 0.0, atol=1e-15)
    assert float(decomposition.axis_references[0].sum()) == pytest.approx(1.0)
