"""Pure statistics for the preregistered Gaussian fixed-ray confirmation."""

from __future__ import annotations

from math import comb, isfinite
from typing import Mapping

import numpy as np


SECONDARY_ENDPOINT_IDS = (
    "construction_residual",
    "retained_beta_trend",
    "basin_exit_rate",
    "scheme_dispersion",
    "conditioning_trend",
    "rejection_rate",
)


def exact_sign_pvalue(values: object, boundary: float) -> float:
    """Return the conservative lower-sided exact sign-test p-value."""
    sample = np.asarray(values, dtype=np.float64)
    if sample.ndim != 1 or sample.size == 0 or not np.all(np.isfinite(sample)):
        raise ValueError("sign-test values must be a nonempty finite vector")
    if not isfinite(float(boundary)):
        raise ValueError("sign-test boundary must be finite")
    favorable = int(np.count_nonzero(sample < float(boundary)))
    trials = int(sample.size)
    return float(sum(comb(trials, count) for count in range(favorable, trials + 1)) / (2**trials))


def exact_binomial_lower_tail(
    events: int, trials: int, boundary_probability: float
) -> float:
    """Return P(X <= events) at the composite-null binomial boundary."""
    if type(events) is not int or type(trials) is not int:
        raise ValueError("binomial counts must be integers")
    if trials <= 0 or events < 0 or events > trials:
        raise ValueError("binomial counts are outside the admitted range")
    probability = float(boundary_probability)
    if not isfinite(probability) or not 0.0 <= probability <= 1.0:
        raise ValueError("binomial boundary probability must lie in [0, 1]")
    return float(
        sum(
            comb(trials, count)
            * probability**count
            * (1.0 - probability) ** (trials - count)
            for count in range(events + 1)
        )
    )


def holm_adjust(
    pvalues: Mapping[str, float], *, alpha: float = 0.05
) -> list[dict[str, object]]:
    """Adjust the frozen six-endpoint family using Holm's step-down method."""
    if set(pvalues) != set(SECONDARY_ENDPOINT_IDS):
        raise ValueError("Holm input must contain exactly six frozen endpoints")
    if not isfinite(float(alpha)) or not 0.0 < float(alpha) < 1.0:
        raise ValueError("Holm alpha must lie strictly between zero and one")
    raw: dict[str, float] = {}
    for endpoint_id in SECONDARY_ENDPOINT_IDS:
        value = float(pvalues[endpoint_id])
        if not isfinite(value) or not 0.0 <= value <= 1.0:
            raise ValueError("Holm p-values must be finite and lie in [0, 1]")
        raw[endpoint_id] = value

    ordered = sorted(raw.items(), key=lambda item: (item[1], item[0]))
    adjusted_by_id: dict[str, float] = {}
    rank_by_id: dict[str, int] = {}
    running = 0.0
    family_size = len(ordered)
    for index, (endpoint_id, value) in enumerate(ordered):
        running = max(running, (family_size - index) * value)
        adjusted_by_id[endpoint_id] = min(1.0, running)
        rank_by_id[endpoint_id] = index + 1

    return [
        {
            "endpoint_id": endpoint_id,
            "unadjusted_p": raw[endpoint_id],
            "adjusted_p": adjusted_by_id[endpoint_id],
            "rank": rank_by_id[endpoint_id],
            "rejected": adjusted_by_id[endpoint_id] <= float(alpha),
        }
        for endpoint_id in SECONDARY_ENDPOINT_IDS
    ]


__all__ = [
    "SECONDARY_ENDPOINT_IDS",
    "exact_binomial_lower_tail",
    "exact_sign_pvalue",
    "holm_adjust",
]
