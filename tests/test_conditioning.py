from __future__ import annotations

import numpy as np
import pytest

import multiagent_elbo.conditioning as conditioning
from multiagent_elbo.conditioning import assess_spectral_spd


def test_spectral_policy_rejects_correlated_matrix_old_proxy_false_accepted():
    """A near-collinear SPD matrix is rejected by its spectral rcond."""
    matrix = np.array([[1.0, 1.0 - 1.0e-12], [1.0 - 1.0e-12, 1.0]])

    result = assess_spectral_spd(
        matrix, min_rcond=1.0e-12, atol=0.0, rtol=0.0
    )

    assert result.decision == "fail"
    assert result.reciprocal_condition < 1.0e-12


def test_spectral_policy_accepts_repeated_small_diagonal_old_proxy_false_rejected():
    """Repeated small eigenvalues do not multiply the conditioning penalty."""
    result = assess_spectral_spd(
        np.diag([1.0, 1.0e-7, 1.0e-7]),
        min_rcond=1.0e-12,
        atol=0.0,
        rtol=0.0,
    )

    assert result.decision == "pass"
    assert result.reciprocal_condition == pytest.approx(1.0e-7)


def test_threshold_band_is_inconclusive_and_tolerances_are_reachable():
    """The declared absolute and relative bands defer close threshold calls."""
    matrix = np.diag([1.0, 1.05e-6])

    assert assess_spectral_spd(
        matrix, min_rcond=1.0e-6, atol=0.0, rtol=0.0
    ).decision == "pass"
    assert assess_spectral_spd(
        matrix, min_rcond=1.0e-6, atol=1.0e-7, rtol=0.0
    ).decision == "inconclusive"
    assert assess_spectral_spd(
        matrix, min_rcond=1.0e-6, atol=0.0, rtol=0.1
    ).decision == "inconclusive"


@pytest.mark.parametrize(
    "matrix",
    [
        np.array([[1.0, 0.0], [0.0, 0.0]]),
        np.array([[np.inf]]),
    ],
)
def test_spectral_policy_requires_finite_strictly_positive_spectrum(
    matrix: np.ndarray,
):
    """Shared policy does not assign conditioning to invalid SPD inputs."""
    with pytest.raises(ValueError, match="positive|finite"):
        assess_spectral_spd(matrix, min_rcond=1.0e-12, atol=0.0, rtol=0.0)


def test_spectral_policy_rejects_nonfinite_eigensolver_output(
    monkeypatch: pytest.MonkeyPatch,
):
    """An invalid eigensolver result cannot silently become a pass decision."""
    monkeypatch.setattr(
        conditioning.scipy.linalg,
        "eigvalsh",
        lambda *_args, **_kwargs: np.array([np.nan, np.nan]),
    )

    with pytest.raises(ValueError, match="eigensolver returned nonfinite eigenvalues"):
        assess_spectral_spd(
            np.eye(2), min_rcond=1.0e-12, atol=0.0, rtol=0.0
        )
