from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
WITNESS_PATH = ROOT / "docs/verification/shared_latent_coupling_witness.py"


def _load_witness():
    spec = importlib.util.spec_from_file_location("shared_latent_coupling_witness", WITNESS_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_rank_two_split_has_positive_edges_and_proper_prior() -> None:
    witness = _load_witness()
    example = witness.rank_two_positive_split_example()

    expected_precision = np.array(
        [
            [87 / 110, -1 / 5, -21 / 110, -2 / 11],
            [-1 / 5, 4 / 5, -1 / 5, -1 / 5],
            [-21 / 110, -1 / 5, 87 / 110, -12 / 55],
            [-2 / 11, -1 / 5, -12 / 55, 42 / 55],
        ]
    )
    expected_beta = np.array(
        [
            [0.0, 1 / 5, 21 / 110, 2 / 11],
            [1 / 5, 0.0, 1 / 5, 1 / 5],
            [21 / 110, 1 / 5, 0.0, 12 / 55],
            [2 / 11, 1 / 5, 12 / 55, 0.0],
        ]
    )
    expected_prior = np.array([12 / 55, 1 / 5, 2 / 11, 9 / 55])

    np.testing.assert_allclose(example["precision"], expected_precision, atol=1e-14, rtol=0.0)
    np.testing.assert_allclose(example["beta"], expected_beta, atol=1e-14, rtol=0.0)
    np.testing.assert_allclose(example["prior"], expected_prior, atol=1e-14, rtol=0.0)
    assert example["correction_rank"] == 2
    assert float(example["split_residual"]) < 1e-14
    assert np.isclose(
        float(example["beta"][np.triu_indices(4, 1)].min()),
        2 / 11,
        atol=1e-14,
        rtol=0.0,
    )
    assert np.isclose(float(example["prior"].min()), 9 / 55, atol=1e-14, rtol=0.0)


def test_exact_rank_one_split_can_require_an_improper_residual_prior() -> None:
    witness = _load_witness()
    example = witness.rank_one_improper_prior_example()

    expected_precision = np.array(
        [
            [1 / 26, -5 / 52, -5 / 52, -5 / 52],
            [-5 / 52, 103 / 104, -1 / 104, -1 / 104],
            [-5 / 52, -1 / 104, 103 / 104, -1 / 104],
            [-5 / 52, -1 / 104, -1 / 104, 103 / 104],
        ]
    )
    expected_beta = np.array(
        [
            [0.0, 5 / 52, 5 / 52, 5 / 52],
            [5 / 52, 0.0, 1 / 104, 1 / 104],
            [5 / 52, 1 / 104, 0.0, 1 / 104],
            [5 / 52, 1 / 104, 1 / 104, 0.0],
        ]
    )
    expected_prior = np.array([-1 / 4, 7 / 8, 7 / 8, 7 / 8])

    np.testing.assert_allclose(
        example["loading"], np.array([10.0, 1.0, 1.0, 1.0]), atol=0.0, rtol=0.0
    )
    np.testing.assert_allclose(
        example["precision"], expected_precision, atol=1e-14, rtol=0.0
    )
    np.testing.assert_allclose(
        example["beta"], expected_beta, atol=1e-14, rtol=0.0
    )
    np.testing.assert_allclose(
        example["prior"], expected_prior, atol=1e-14, rtol=0.0
    )
    assert example["correction_rank"] == 1
    assert float(example["split_residual"]) < 1e-14
    assert np.all(example["beta"][np.triu_indices(4, 1)] > 0)
    assert float(example["prior"].min()) < 0
    assert np.isclose(float(example["prior"].min()), -1 / 4, atol=1e-14, rtol=0.0)


def test_claim_4_rejects_a_positive_residual_prior_without_printing_pass(
    capsys,
) -> None:
    witness = _load_witness()
    positive_prior = np.full(4, 1 / 5)

    with pytest.raises(AssertionError, match="negative residual prior"):
        witness.claim_4(positive_prior)

    output = capsys.readouterr().out
    assert "PASS" not in output


def test_correction_rank_tracks_loading_rank_not_latent_width() -> None:
    witness = _load_witness()
    private_covariance = np.diag([1.0, 2.0, 3.0, 4.0])
    loading = np.array(
        [
            [1.0, 2.0],
            [2.0, 4.0],
            [3.0, 6.0],
            [4.0, 8.0],
        ]
    )
    latent_covariance = np.diag([1.0, 3.0])

    correction = witness.woodbury_correction(
        private_covariance, loading, latent_covariance
    )
    direct = np.linalg.inv(private_covariance) - np.linalg.inv(
        private_covariance + loading @ latent_covariance @ loading.T
    )

    np.testing.assert_allclose(correction, direct, atol=1e-14, rtol=0.0)
    assert np.linalg.matrix_rank(loading, tol=1e-12) == 1
    assert witness.correction_rank(private_covariance, loading, latent_covariance) == 1
    assert witness.correction_rank(private_covariance, loading, latent_covariance) < loading.shape[1]


def test_beta_is_removed_before_testing_the_exact_rotation_cocycle() -> None:
    witness = _load_witness()
    example = witness.weighted_rotation_cocycle_example()
    beta = example["beta"]
    precision = example["precision"]
    transports = example["transports"]

    assert beta == 1 / 4
    np.testing.assert_allclose(
        example["reconstructed_precision"], precision, atol=1e-14, rtol=0.0
    )
    for a in range(3):
        np.testing.assert_allclose(
            example["residual_priors"][a], np.eye(2) / 4, atol=1e-14, rtol=0.0
        )
        np.testing.assert_allclose(transports[(a, a)], np.eye(2), atol=1e-14, rtol=0.0)
        for b in range(3):
            omega_ab = transports[(a, b)]
            np.testing.assert_allclose(np.linalg.det(omega_ab), 1.0, atol=1e-14, rtol=0.0)
            if a != b:
                block = precision[2 * a : 2 * a + 2, 2 * b : 2 * b + 2]
                np.testing.assert_allclose(block, -beta * omega_ab, atol=1e-14, rtol=0.0)
                recovered = witness.recover_transport(block, beta, np.eye(2))
                np.testing.assert_allclose(recovered, omega_ab, atol=1e-14, rtol=0.0)
            for c in range(3):
                np.testing.assert_allclose(
                    omega_ab @ transports[(b, c)],
                    transports[(a, c)],
                    atol=1e-14,
                    rtol=0.0,
                )


def test_recover_transport_removes_noncommuting_weight_and_nonunit_beta() -> None:
    witness = _load_witness()
    beta = 1 / 2
    weight = np.array([[2.0, 1.0], [1.0, 2.0]])
    omega = np.array([[0.0, -1.0], [1.0, 0.0]])
    cross_precision_block = np.array([[-0.5, 1.0], [-1.0, 0.5]])

    np.testing.assert_allclose(np.linalg.eigvalsh(weight), [1.0, 3.0], atol=0.0, rtol=0.0)
    assert np.linalg.norm(weight @ omega - omega @ weight) > 1.0
    np.testing.assert_allclose(
        -beta * weight @ omega, cross_precision_block, atol=0.0, rtol=0.0
    )

    recovered = witness.recover_transport(cross_precision_block, beta, weight)
    reconstructed = -beta * weight @ recovered

    np.testing.assert_allclose(recovered, omega, atol=1e-14, rtol=0.0)
    np.testing.assert_allclose(
        reconstructed, cross_precision_block, atol=1e-14, rtol=0.0
    )


def test_d_ge_k_is_only_necessary_for_induced_block_invertibility() -> None:
    witness = _load_witness()
    loading_a = np.array([[1.0, 0.0], [0.0, 0.0]])
    loading_b = np.array([[1.0, 0.0], [0.0, 0.0]])
    middle = np.eye(2)
    private_covariance_b = np.eye(2)

    induced = witness.induced_transport_coefficient(
        loading_a, middle, loading_b, private_covariance_b
    )

    assert loading_a.shape == (2, 2)
    np.testing.assert_allclose(induced, np.diag([1.0, 0.0]), atol=0.0, rtol=0.0)
    assert witness.induced_block_rank(
        loading_a, middle, loading_b, private_covariance_b
    ) == 1
    assert np.linalg.det(induced) == 0.0


def test_induced_block_rank_reports_exact_full_rank_coefficient() -> None:
    witness = _load_witness()
    loading_a = np.array([[1.0, 1.0], [0.0, 1.0]])
    middle = np.diag([2.0, 3.0])
    loading_b = np.array([[1.0, 0.0], [1.0, 1.0]])
    private_covariance_b = np.diag([2.0, 1.0])

    induced = witness.induced_transport_coefficient(
        loading_a, middle, loading_b, private_covariance_b
    )

    np.testing.assert_allclose(
        induced, np.array([[1.0, 5.0], [0.0, 3.0]]), atol=0.0, rtol=0.0
    )
    assert np.isclose(np.linalg.det(induced), 3.0, atol=1e-14, rtol=0.0)
    assert witness.induced_block_rank(
        loading_a, middle, loading_b, private_covariance_b
    ) == 2


def test_main_reports_the_narrow_skeleton_and_open_boundaries(capsys) -> None:
    witness = _load_witness()

    witness.main()
    output = capsys.readouterr().out.lower()

    assert "exact flat scalar mean-alignment skeleton" in output
    assert "never a cocycle" not in output
    assert "kl form or high-rank, not both" not in output
    for open_boundary in (
        "directed row-simplex attention",
        "categorical entropy",
        "two transported law channels",
        "full-law representability",
    ):
        assert f"open -- {open_boundary}" in output
