from __future__ import annotations

import numpy as np
import pytest

from multiagent_elbo.realizations.gaussian.confirmatory_analysis import (
    SECONDARY_ENDPOINT_IDS,
    exact_binomial_lower_tail,
    exact_sign_pvalue,
    holm_adjust,
)


def test_exact_sign_pvalue_is_conservative_at_ties():
    values = np.array([-1.0, -0.5, 0.0, 0.0], dtype=np.float64)

    assert exact_sign_pvalue(values, 0.0) == pytest.approx(11.0 / 16.0)


def test_exact_binomial_lower_tail_uses_composite_null_boundary():
    assert exact_binomial_lower_tail(0, 30, 0.05) == pytest.approx(0.95**30)


@pytest.mark.parametrize(
    ("values", "boundary"),
    [
        (np.array([], dtype=np.float64), 0.0),
        (np.array([np.nan], dtype=np.float64), 0.0),
        (np.array([0.0], dtype=np.float64), np.inf),
    ],
)
def test_exact_sign_pvalue_rejects_invalid_samples(values: np.ndarray, boundary: float):
    with pytest.raises(ValueError):
        exact_sign_pvalue(values, boundary)


@pytest.mark.parametrize(
    ("events", "trials", "probability"),
    [(-1, 30, 0.05), (31, 30, 0.05), (0, 0, 0.05), (0, 30, -0.1), (0, 30, 1.1)],
)
def test_exact_binomial_lower_tail_rejects_invalid_inputs(
    events: int, trials: int, probability: float
):
    with pytest.raises(ValueError):
        exact_binomial_lower_tail(events, trials, probability)


def test_holm_adjusts_one_frozen_six_endpoint_family():
    raw = dict(
        zip(
            SECONDARY_ENDPOINT_IDS,
            [0.01, 0.04, 0.03, 0.002, 0.5, 0.04],
            strict=True,
        )
    )

    result = holm_adjust(raw)

    assert [row["endpoint_id"] for row in result] == list(SECONDARY_ENDPOINT_IDS)
    by_id = {row["endpoint_id"]: row for row in result}
    assert by_id["scheme_dispersion"]["adjusted_p"] == pytest.approx(0.012)
    assert all(0.0 <= row["adjusted_p"] <= 1.0 for row in result)


def test_holm_breaks_raw_pvalue_ties_by_endpoint_id():
    raw = {endpoint_id: 0.04 for endpoint_id in reversed(SECONDARY_ENDPOINT_IDS)}

    result = holm_adjust(raw)

    ranked = sorted(result, key=lambda row: row["rank"])
    assert [row["endpoint_id"] for row in ranked] == sorted(SECONDARY_ENDPOINT_IDS)


def test_holm_rejects_a_partial_or_extra_family():
    with pytest.raises(ValueError, match="exactly six"):
        holm_adjust({SECONDARY_ENDPOINT_IDS[0]: 0.01})
    with pytest.raises(ValueError, match="exactly six"):
        holm_adjust({**{name: 0.01 for name in SECONDARY_ENDPOINT_IDS}, "extra": 0.2})
