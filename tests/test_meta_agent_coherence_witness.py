from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
WITNESS_PATH = ROOT / "docs/verification/meta_agent_coherence_witness.py"


def _load_witness():
    spec = importlib.util.spec_from_file_location("meta_agent_coherence_witness", WITNESS_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _finite_difference_hessian(function, point: np.ndarray, step: float = 1e-4) -> np.ndarray:
    hessian = np.zeros((point.size, point.size))
    for row in range(point.size):
        for column in range(point.size):
            e_row = np.zeros_like(point)
            e_column = np.zeros_like(point)
            e_row[row] = step
            e_column[column] = step
            hessian[row, column] = (
                function(point + e_row + e_column)
                - function(point + e_row - e_column)
                - function(point - e_row + e_column)
                + function(point - e_row - e_column)
            ) / (4.0 * step * step)
    return hessian


def test_forward_kl_edge_precision_uses_transported_sender_covariance() -> None:
    witness = _load_witness()
    theta_ij = np.diag([2.0, 3.0])
    sigma_j = np.diag([5.0, 7.0])

    precision = witness.forward_kl_edge_precision(theta_ij, sigma_j, beta_ij=11.0)

    np.testing.assert_allclose(
        precision,
        np.diag([11.0 / 20.0, 11.0 / 63.0]),
        atol=1e-14,
        rtol=0.0,
    )


def test_frozen_beta_mean_hessian_matches_forward_kl_finite_difference() -> None:
    witness = _load_witness()
    theta_01 = np.array([[1.2, 0.3], [-0.2, 0.9]])
    sigma_1 = np.array([[1.8, 0.2], [0.2, 0.7]])
    beta_01 = 0.6

    def forward_kl_mean_term(stacked_means: np.ndarray) -> float:
        residual = stacked_means[:2] - theta_01 @ stacked_means[2:]
        transported_sender = theta_01 @ sigma_1 @ theta_01.T
        return 0.5 * beta_01 * float(
            residual @ np.linalg.inv(transported_sender) @ residual
        )

    covariance = {0: np.diag([0.9, 1.4]), 1: sigma_1}
    assembled = witness.assemble_frozen_beta_mean_hessian(
        n=2,
        K=2,
        directed_edges=[(0, 1)],
        theta={(0, 1): theta_01},
        covariance=covariance,
        beta={(0, 1): beta_01},
    )
    finite_difference = _finite_difference_hessian(
        forward_kl_mean_term,
        np.array([0.4, -0.3, 0.2, 0.7]),
    )

    np.testing.assert_allclose(assembled, finite_difference, atol=2e-7, rtol=0.0)


def test_forward_kl_hessian_and_local_fisher_metric_transform_by_gl_congruence() -> None:
    witness = _load_witness()
    theta_01 = np.array([[1.1, 0.2], [-0.3, 0.8]])
    covariance = {
        0: np.array([[1.4, 0.1], [0.1, 0.9]]),
        1: np.array([[0.8, -0.1], [-0.1, 1.7]]),
    }
    gauges = {
        0: np.array([[1.3, 0.2], [0.1, 0.9]]),
        1: np.array([[0.8, -0.1], [0.3, 1.2]]),
    }
    transformed_theta = {
        (0, 1): gauges[0] @ theta_01 @ np.linalg.inv(gauges[1])
    }
    transformed_covariance = {
        index: gauges[index] @ covariance[index] @ gauges[index].T
        for index in range(2)
    }
    kwargs = dict(n=2, K=2, directed_edges=[(0, 1)], beta={(0, 1): 0.7})
    hessian = witness.assemble_frozen_beta_mean_hessian(
        theta={(0, 1): theta_01}, covariance=covariance, **kwargs
    )
    transformed_hessian = witness.assemble_frozen_beta_mean_hessian(
        theta=transformed_theta, covariance=transformed_covariance, **kwargs
    )
    local_metric = witness.local_product_fisher_metric(covariance, n=2, K=2)
    transformed_local_metric = witness.local_product_fisher_metric(
        transformed_covariance, n=2, K=2
    )
    block_gauge = np.block(
        [[gauges[0], np.zeros((2, 2))], [np.zeros((2, 2)), gauges[1]]]
    )
    inverse_block_gauge = np.linalg.inv(block_gauge)

    np.testing.assert_allclose(
        transformed_hessian,
        inverse_block_gauge.T @ hessian @ inverse_block_gauge,
        atol=2e-12,
        rtol=0.0,
    )
    np.testing.assert_allclose(
        transformed_local_metric,
        inverse_block_gauge.T @ local_metric @ inverse_block_gauge,
        atol=2e-12,
        rtol=0.0,
    )
    assert not np.allclose(hessian, local_metric)


def test_reverse_kl_is_a_separate_directed_edge_with_the_reverse_sender_slot() -> None:
    witness = _load_witness()
    theta_01 = np.array([[1.2, 0.1], [0.2, 0.7]])
    theta_10 = np.linalg.inv(theta_01)
    covariance = {0: np.diag([1.0, 4.0]), 1: np.diag([9.0, 2.0])}
    beta = {(0, 1): 0.4, (1, 0): 0.9}
    forward = witness.assemble_frozen_beta_mean_hessian(
        2, 2, [(0, 1)], {(0, 1): theta_01}, covariance, beta
    )
    reverse = witness.assemble_frozen_beta_mean_hessian(
        2, 2, [(1, 0)], {(1, 0): theta_10}, covariance, beta
    )
    both = witness.assemble_frozen_beta_mean_hessian(
        2,
        2,
        [(0, 1), (1, 0)],
        {(0, 1): theta_01, (1, 0): theta_10},
        covariance,
        beta,
    )
    expected_reverse_precision = 0.9 * np.linalg.inv(
        theta_10 @ covariance[0] @ theta_10.T
    )

    np.testing.assert_allclose(both, forward + reverse, atol=1e-13, rtol=0.0)
    np.testing.assert_allclose(
        reverse[2:, 2:], expected_reverse_precision, atol=1e-13, rtol=0.0
    )
    assert not np.allclose(forward[:2, :2], reverse[2:, 2:])


def test_sender_and_receiver_precision_slots_agree_only_under_covariance_transport() -> None:
    witness = _load_witness()
    theta_01 = np.array([[1.2, 0.2], [-0.1, 0.9]])
    sigma_1 = np.array([[1.5, 0.3], [0.3, 0.8]])
    sigma_0 = theta_01 @ sigma_1 @ theta_01.T

    sender_slot = witness.forward_kl_edge_precision(theta_01, sigma_1, beta_ij=0.75)

    np.testing.assert_allclose(
        sender_slot, 0.75 * np.linalg.inv(sigma_0), atol=1e-13, rtol=0.0
    )


def test_local_prior_blocks_are_scaled_by_presence_precision_and_alpha() -> None:
    witness = _load_witness()
    prior_precision = {0: np.diag([2.0, 5.0]), 1: np.diag([7.0, 11.0])}
    hessian = witness.assemble_frozen_beta_mean_hessian(
        n=2,
        K=2,
        directed_edges=[],
        theta={},
        covariance={0: np.eye(2), 1: np.eye(2)},
        beta={},
        chi={0: 1.0, 1: 0.25},
        alpha={0: 3.0, 1: 4.0},
        prior_precision=prior_precision,
    )

    np.testing.assert_allclose(hessian[:2, :2], np.diag([6.0, 15.0]))
    np.testing.assert_allclose(hessian[2:, 2:], np.diag([7.0, 11.0]))


def _support_fixture():
    directed_edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    theta = {edge: np.eye(2) for edge in directed_edges}
    covariance = {index: np.eye(2) for index in range(3)}
    effective_beta = {
        (0, 1): 0.75,
        (1, 0): 0.5,
        (1, 2): 0.0,
        (2, 1): 0.0,
    }
    prior_precision = {index: np.eye(2) for index in range(3)}
    alpha = {index: 1.0 for index in range(3)}
    return directed_edges, theta, covariance, effective_beta, prior_precision, alpha


def test_prescribed_fixed_ambient_decoupling_adds_exactly_k_null_modes() -> None:
    witness = _load_witness()
    edges, theta, covariance, beta, prior_precision, alpha = _support_fixture()
    hessian = witness.assemble_frozen_beta_mean_hessian(
        3,
        2,
        edges,
        theta,
        covariance,
        beta,
        chi={0: 1.0, 1: 1.0, 2: 0.0},
        alpha=alpha,
        prior_precision=prior_precision,
    )

    eigenvalues = np.linalg.eigvalsh(hessian)
    assert int(np.sum(np.abs(eigenvalues) < 1e-12)) == 2
    np.testing.assert_allclose(hessian[4:, :], 0.0, atol=1e-14, rtol=0.0)
    np.testing.assert_allclose(hessian[:, 4:], 0.0, atol=1e-14, rtol=0.0)


def test_edge_dropout_with_present_agent_retains_the_local_prior_floor() -> None:
    witness = _load_witness()
    edges, theta, covariance, beta, prior_precision, alpha = _support_fixture()
    hessian = witness.assemble_frozen_beta_mean_hessian(
        3,
        2,
        edges,
        theta,
        covariance,
        beta,
        chi={0: 1.0, 1: 1.0, 2: 1.0},
        alpha=alpha,
        prior_precision=prior_precision,
    )

    assert np.linalg.eigvalsh(hessian)[0] >= 1.0 - 1e-12
    np.testing.assert_allclose(hessian[4:, 4:], np.eye(2), atol=1e-14, rtol=0.0)


def test_fixed_nonzero_edge_hessian_does_not_decouple_as_positive_receiver_chi_tends_to_zero() -> None:
    witness = _load_witness()
    theta_01 = np.diag([2.0, 3.0])
    covariance = {0: np.diag([1.0, 4.0]), 1: np.diag([5.0, 7.0])}
    effective_beta = {(0, 1): 0.7}
    common = dict(
        n=2,
        K=2,
        directed_edges=[(0, 1)],
        theta={(0, 1): theta_01},
        covariance=covariance,
        beta=effective_beta,
        prior_precision=None,
    )

    receiver_present = witness.assemble_frozen_beta_mean_hessian(
        chi={0: 1.0, 1: 1.0},
        **common,
    )
    receiver_almost_absent = witness.assemble_frozen_beta_mean_hessian(
        chi={0: 1e-12, 1: 1.0},
        **common,
    )
    expected_fixed_edge = np.array(
        [
            [7.0 / 200.0, 0.0, -7.0 / 100.0, 0.0],
            [0.0, 1.0 / 90.0, 0.0, -1.0 / 30.0],
            [-7.0 / 100.0, 0.0, 7.0 / 50.0, 0.0],
            [0.0, -1.0 / 30.0, 0.0, 1.0 / 10.0],
        ]
    )

    np.testing.assert_allclose(
        receiver_present, expected_fixed_edge, atol=1e-14, rtol=0.0
    )
    np.testing.assert_allclose(
        receiver_almost_absent, expected_fixed_edge, atol=1e-14, rtol=0.0
    )
    np.testing.assert_allclose(
        receiver_almost_absent, receiver_present, atol=1e-14, rtol=0.0
    )


def test_active_set_deletion_equals_the_retained_principal_submatrix() -> None:
    witness = _load_witness()
    edges, theta, covariance, beta, prior_precision, alpha = _support_fixture()
    fixed_ambient = witness.assemble_frozen_beta_mean_hessian(
        3,
        2,
        edges,
        theta,
        covariance,
        beta,
        chi={0: 1.0, 1: 1.0, 2: 0.0},
        alpha=alpha,
        prior_precision=prior_precision,
    )
    retained_edges = [(0, 1), (1, 0)]
    deleted = witness.assemble_frozen_beta_mean_hessian(
        2,
        2,
        retained_edges,
        {edge: theta[edge] for edge in retained_edges},
        {0: covariance[0], 1: covariance[1]},
        {edge: beta[edge] for edge in retained_edges},
        chi={0: 1.0, 1: 1.0},
        alpha={0: alpha[0], 1: alpha[1]},
        prior_precision={0: prior_precision[0], 1: prior_precision[1]},
    )

    np.testing.assert_allclose(deleted, fixed_ambient[:4, :4], atol=1e-14, rtol=0.0)


def test_canonical_row_has_no_positive_chi_decoupling_path_and_exact_zero_needs_extension() -> None:
    witness = _load_witness()
    energies = np.array([0.2, 0.8])
    prior = np.array([2.0, 1.0])
    sender_presence = np.array([1.0, 0.5])

    positive_chi = witness.canonical_normalized_attention_row(
        energies, prior, receiver_presence=1.0, sender_presence=sender_presence
    )
    positive_chi_near_zero = witness.canonical_normalized_attention_row(
        energies, prior, receiver_presence=1e-12, sender_presence=sender_presence
    )
    literal_mass = np.array([2.0 * np.exp(-0.2), 0.5 * np.exp(-0.8)])

    np.testing.assert_allclose(
        positive_chi, literal_mass / literal_mass.sum(), atol=1e-14
    )
    np.testing.assert_allclose(positive_chi_near_zero, positive_chi, atol=1e-14, rtol=0.0)
    with pytest.raises(ValueError, match="0/0"):
        witness.canonical_normalized_attention_row(
            energies, prior, receiver_presence=0.0, sender_presence=sender_presence
        )


def test_retracted_laplacian_uses_stored_reverse_map_not_forward_transpose() -> None:
    witness = _load_witness()
    forward = np.diag([2.0, 0.5])
    reverse = np.linalg.inv(forward)
    operator = witness._retracted_laplacian(
        {(0, 1): forward, (1, 0): reverse},
        [(0, 1)],
        np.array([0.25]),
        np.array([0.75]),
        n=2,
        K=2,
    )

    np.testing.assert_allclose(operator[2:4, 0:2], -0.75 * reverse, atol=0.0, rtol=0.0)
    assert not np.allclose(operator[2:4, 0:2], -0.75 * forward.T)


def test_receiver_normalized_directed_weights_sum_to_one_on_every_active_row() -> None:
    witness = _load_witness()
    edges = [(0, 1), (1, 2), (2, 0), (0, 3)]
    raw_bij = np.array([1.0, 2.0, 3.0, 4.0])
    raw_bji = np.array([5.0, 6.0, 7.0, 8.0])

    bij, bji, row_sums = witness.receiver_normalized_directed_weights(
        edges, raw_bij, raw_bji, n=4
    )

    np.testing.assert_allclose(
        bij, np.array([1.0 / 12.0, 2.0 / 7.0, 3.0 / 9.0, 4.0 / 12.0])
    )
    np.testing.assert_allclose(
        bji, np.array([5.0 / 7.0, 6.0 / 9.0, 7.0 / 12.0, 1.0])
    )
    np.testing.assert_allclose(row_sums, np.ones(4), atol=1e-14, rtol=0.0)


def test_exact_identity_cell_matches_the_energy_form() -> None:
    witness = _load_witness()
    edges = [(0, 1), (1, 2), (2, 0)]
    weights = np.array([0.4, 0.7, 1.1])
    links = {}
    for edge, angle in zip(edges, [0.2, -0.5, 0.9]):
        cosine, sine = np.cos(angle), np.sin(angle)
        link = np.array([[cosine, -sine], [sine, cosine]])
        links[edge] = link
        links[(edge[1], edge[0])] = link.T

    retired = witness._retracted_laplacian(
        links, edges, weights, weights.copy(), n=3, K=2
    )
    energy = witness.connection_laplacian(links, edges, weights, n=3, K=2)

    np.testing.assert_allclose(retired, energy, atol=1e-14, rtol=0.0)


def test_nonorthogonal_reciprocal_link_can_retain_nonnegative_real_spectrum() -> None:
    witness = _load_witness()
    forward = np.diag([2.0, 0.5])
    reverse = np.linalg.inv(forward)
    retired = witness._retracted_laplacian(
        {(0, 1): forward, (1, 0): reverse},
        [(0, 1)],
        np.ones(1),
        np.ones(1),
        n=2,
        K=2,
    )

    assert np.linalg.norm(forward.T @ forward - np.eye(2)) > 1.0
    assert np.linalg.eigvals(retired).real.min() >= -1e-12


def test_symmetric_row_stochastic_control_can_remain_symmetric() -> None:
    witness = _load_witness()
    edges = [(0, 1), (1, 2), (2, 0)]
    bij, bji, row_sums = witness.receiver_normalized_directed_weights(
        edges, np.ones(3), np.ones(3), n=3
    )
    identity = np.eye(2)
    links = {}
    for edge in edges:
        links[edge] = identity
        links[(edge[1], edge[0])] = identity
    retired = witness._retracted_laplacian(
        links, edges, bij, bji, n=3, K=2
    )

    np.testing.assert_allclose(bij, np.full(3, 0.5), atol=1e-14, rtol=0.0)
    np.testing.assert_allclose(bji, np.full(3, 0.5), atol=1e-14, rtol=0.0)
    np.testing.assert_allclose(row_sums, np.ones(3), atol=1e-14, rtol=0.0)
    np.testing.assert_allclose(retired, retired.T, atol=1e-14, rtol=0.0)


def test_regime_table_labels_nonidentity_cells_as_diagnostics_not_universal_claims(
    capsys: pytest.CaptureFixture[str],
) -> None:
    witness = _load_witness()

    witness.regime_table()

    output = capsys.readouterr().out
    assert "seeded diagnostics outside the identity cell are not universal implications" in output
    assert "nonorthogonal reciprocal countercontrol" in output
    assert "symmetric row-stochastic countercontrol" in output
    assert "asymmetric as soon as" not in output
    assert "indefinite as soon as" not in output
