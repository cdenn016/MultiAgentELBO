from __future__ import annotations

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
import pytest

from multiagent_elbo.finite.categorical_falsification_model import build_reference_model
from multiagent_elbo.finite.coarse_composition import (
    PairEndpointKernel,
    REFERENCE_HARD_MEMBERSHIP,
    REFERENCE_PARENT_LABELS,
    WITNESS_AGENT_LABELS,
    WITNESS_ALPHA,
    WITNESS_BETA,
    WITNESS_BLOCK_LABELS,
    WITNESS_MEMBERSHIP,
    compose_endpoint_kernels,
    disintegrate,
    endpoint_marginal_product,
    is_product_form,
    naive_row_average,
    product_endpoint_kernel,
    push_event_law,
    reference_endpoint_kernels,
    run_coarse_composition_measurement,
)

ONE_ULP = 2.220446049250313e-16
CHANNELS = ("belief", "model")
CONFIGURATIONS = ("uniform", "peaked")


def test_the_declared_three_node_witness_reproduces_the_literal_row_average_discrepancy():
    alpha = np.array(WITNESS_ALPHA, dtype=np.float64)
    beta = np.array(WITNESS_BETA, dtype=np.float64)
    membership = np.array(WITNESS_MEMBERSHIP, dtype=np.float64)
    kernel = product_endpoint_kernel(
        membership, WITNESS_AGENT_LABELS, WITNESS_BLOCK_LABELS
    )

    eta = alpha[:, None] * beta
    eta_coarse = push_event_law(eta, kernel)
    alpha_coarse, beta_coarse = disintegrate(eta_coarse)
    beta_naive = naive_row_average(alpha, beta, membership)

    assert eta[0, 2] == 0.9
    assert eta[1, 0] == 0.1
    assert eta_coarse[0, 0] == 0.1
    assert eta_coarse[0, 1] == 0.9
    assert alpha_coarse[0] == 1.0
    assert alpha_coarse[1] == 0.0
    assert beta_coarse[0, 1] == 0.9
    assert beta_naive[0, 1] == 0.5
    assert beta_coarse[0, 1] - beta_naive[0, 1] == 0.4


def test_pushing_through_the_composed_kernel_matches_the_two_step_push_in_every_case():
    model = build_reference_model()
    first, second = reference_endpoint_kernels()
    composed = compose_endpoint_kernels(first, second)

    for channel in CHANNELS:
        for configuration in CONFIGURATIONS:
            eta = model.edge_event_law(configuration, channel)
            staged = push_event_law(push_event_law(eta, first), second)
            direct = push_event_law(eta, composed)

            assert_allclose(staged, direct, rtol=0.0, atol=4.0 * ONE_ULP)


def test_the_composed_endpoint_kernel_equals_the_matrix_product_of_its_two_factors():
    first, second = reference_endpoint_kernels()

    composed = compose_endpoint_kernels(first, second)

    assert composed.fine_labels == first.fine_labels
    assert composed.coarse_labels == second.coarse_labels
    assert composed.matrix.shape == (36, 4)
    assert_array_equal(composed.matrix, first.matrix @ second.matrix)


def test_the_correlated_endpoint_kernels_carry_the_declared_scales_and_are_normalized():
    first, second = reference_endpoint_kernels()

    assert first.fine_labels == ("1", "2", "3", "4", "5", "6")
    assert first.coarse_labels == REFERENCE_PARENT_LABELS
    assert first.matrix.shape == (36, 9)
    assert second.matrix.shape == (9, 4)
    assert_allclose(first.matrix.sum(axis=1), 1.0, rtol=0.0, atol=ONE_ULP)
    assert_allclose(second.matrix.sum(axis=1), 1.0, rtol=0.0, atol=ONE_ULP)


def test_every_push_preserves_total_edge_mass_to_one_unit_in_the_last_place():
    model = build_reference_model()
    first, second = reference_endpoint_kernels()
    composed = compose_endpoint_kernels(first, second)

    for channel in CHANNELS:
        for configuration in CONFIGURATIONS:
            eta = model.edge_event_law(configuration, channel)
            parent = push_event_law(eta, first)
            staged = push_event_law(parent, second)
            direct = push_event_law(eta, composed)

            for law in (eta, parent, staged, direct):
                assert abs(float(law.sum()) - 1.0) <= ONE_ULP


def test_the_declared_correlated_endpoint_kernel_is_not_of_product_form():
    first, second = reference_endpoint_kernels()

    assert not is_product_form(first)
    assert not is_product_form(second)
    assert is_product_form(endpoint_marginal_product(first))
    assert is_product_form(endpoint_marginal_product(second))


def test_a_product_endpoint_kernel_is_recognized_as_product_form():
    membership = np.array(REFERENCE_HARD_MEMBERSHIP, dtype=np.float64)
    labels = ("1", "2", "3", "4", "5", "6")

    kernel = product_endpoint_kernel(membership, labels, REFERENCE_PARENT_LABELS)

    assert is_product_form(kernel)


def test_substituting_the_product_form_of_its_own_marginals_changes_the_coarse_law():
    model = build_reference_model()
    first, _ = reference_endpoint_kernels()
    substituted = endpoint_marginal_product(first)

    for channel in CHANNELS:
        for configuration in CONFIGURATIONS:
            eta = model.edge_event_law(configuration, channel)
            correlated_push = push_event_law(eta, first)
            factored_push = push_event_law(eta, substituted)

            discrepancy = float(np.max(np.abs(correlated_push - factored_push)))
            assert discrepancy > 0.05


def test_guarded_division_leaves_zero_occupancy_rows_exactly_zero_and_not_undefined():
    eta_coarse = np.array([[0.1, 0.9], [0.0, 0.0]], dtype=np.float64)

    alpha_coarse, beta_coarse = disintegrate(eta_coarse)

    assert alpha_coarse[1] == 0.0
    assert not np.any(np.isnan(beta_coarse))
    assert_array_equal(beta_coarse[1], np.zeros(2))
    assert_array_equal(beta_coarse[0], np.array([0.1, 0.9]))


def test_the_six_agent_row_average_discrepancy_is_strictly_positive_under_skewed_alpha():
    model = build_reference_model()
    membership = np.array(REFERENCE_HARD_MEMBERSHIP, dtype=np.float64)
    labels = ("1", "2", "3", "4", "5", "6")
    kernel = product_endpoint_kernel(membership, labels, REFERENCE_PARENT_LABELS)

    for channel in CHANNELS:
        for configuration in CONFIGURATIONS:
            eta = model.edge_event_law(configuration, channel)
            alpha, beta = disintegrate(eta)
            _, beta_coarse = disintegrate(push_event_law(eta, kernel))
            beta_naive = naive_row_average(alpha, beta, membership)

            assert float(np.max(np.abs(beta_coarse - beta_naive))) > 0.06


def test_the_assembled_measurement_reports_every_declared_number():
    measurement = run_coarse_composition_measurement()

    assert measurement.three_node_witness.beta_coarse == 0.9
    assert measurement.three_node_witness.beta_naive == 0.5
    assert measurement.three_node_witness.discrepancy == 0.4
    assert len(measurement.cases) == 4
    assert not measurement.correlated_is_product_form
    assert measurement.substituted_is_product_form
    assert measurement.max_composition_residual <= 4.0 * ONE_ULP
    assert measurement.max_kernel_matrix_residual == 0.0
    assert measurement.max_mass_residual <= ONE_ULP
    assert measurement.min_product_form_discrepancy > 0.05
    assert measurement.max_row_average_discrepancy > 0.08


def test_pushed_laws_and_disintegrations_are_returned_read_only():
    model = build_reference_model()
    first, _ = reference_endpoint_kernels()
    eta = model.edge_event_law("uniform", "belief")

    pushed = push_event_law(eta, first)
    alpha_coarse, beta_coarse = disintegrate(pushed)

    assert not first.matrix.flags.writeable
    assert not pushed.flags.writeable
    assert not alpha_coarse.flags.writeable
    assert not beta_coarse.flags.writeable


def test_the_kernel_rejects_rows_that_do_not_sum_to_one():
    with pytest.raises(ValueError, match="every fine pair row must sum to one"):
        PairEndpointKernel(("1", "2"), ("A",), np.full((4, 1), 0.5))


def test_composition_rejects_a_scale_mismatch_between_its_factors():
    first, second = reference_endpoint_kernels()

    with pytest.raises(ValueError, match="first coarse labels must equal second fine"):
        compose_endpoint_kernels(second, first)


def test_the_row_average_control_refuses_a_soft_membership():
    alpha = np.array(WITNESS_ALPHA, dtype=np.float64)
    beta = np.array(WITNESS_BETA, dtype=np.float64)
    soft = np.array([[0.5, 0.5], [1.0, 0.0], [0.0, 1.0]], dtype=np.float64)

    with pytest.raises(ValueError, match="requires a hard membership"):
        naive_row_average(alpha, beta, soft)
