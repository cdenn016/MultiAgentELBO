"""Shared spectral conditioning policy for symmetric positive-definite matrices."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import scipy.linalg


ConditioningDecision = Literal["pass", "fail", "inconclusive"]


@dataclass(frozen=True)
class SpectralConditioningAssessment:
    """The spectral conditioning decision for an already-established SPD matrix."""

    minimum_eigenvalue: float
    maximum_eigenvalue: float
    reciprocal_condition: float
    threshold: float
    boundary_tolerance: float
    method: Literal["symmetric_eigenvalue_ratio"]
    decision: ConditioningDecision
    reason: str


def _finite_float(value: object, label: str, *, positive: bool) -> float:
    try:
        normalized = float(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError(f"{label} must be a finite float") from error
    if not np.isfinite(normalized) or (normalized <= 0.0 if positive else normalized < 0.0):
        qualifier = "positive" if positive else "nonnegative"
        raise ValueError(f"{label} must be a finite {qualifier} float")
    return normalized


def _conditioning_reason(decision: ConditioningDecision) -> str:
    if decision == "pass":
        return "reciprocal condition exceeds the declared threshold"
    if decision == "fail":
        return "reciprocal condition is below the declared threshold"
    return "reciprocal condition lies within the declared threshold tolerance band"


def assess_spectral_spd(
    matrix: object, *, min_rcond: float, atol: float, rtol: float
) -> SpectralConditioningAssessment:
    """Assess the spectral reciprocal condition of a finite symmetric SPD matrix."""
    threshold = _finite_float(min_rcond, "min_rcond", positive=True)
    absolute_tolerance = _finite_float(atol, "atol", positive=False)
    relative_tolerance = _finite_float(rtol, "rtol", positive=False)
    try:
        values = np.asarray(matrix, dtype=np.float64)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError("matrix must contain numeric values") from error
    if values.ndim != 2 or values.shape[0] != values.shape[1] or values.shape[0] < 1:
        raise ValueError("matrix must be a nonempty square matrix")
    if not np.all(np.isfinite(values)):
        raise ValueError("matrix must contain only finite values")
    if not np.array_equal(values, values.T):
        raise ValueError("matrix must be symmetric")

    eigenvalues = scipy.linalg.eigvalsh(values, check_finite=True)
    minimum = float(eigenvalues[0])
    maximum = float(eigenvalues[-1])
    if minimum <= 0.0 or maximum <= 0.0:
        raise ValueError("matrix must have a strictly positive spectrum")
    reciprocal_condition = minimum / maximum
    boundary_tolerance = absolute_tolerance + relative_tolerance * abs(threshold)
    if abs(reciprocal_condition - threshold) <= boundary_tolerance:
        decision: ConditioningDecision = "inconclusive"
    elif reciprocal_condition < threshold:
        decision = "fail"
    else:
        decision = "pass"
    return SpectralConditioningAssessment(
        minimum_eigenvalue=minimum,
        maximum_eigenvalue=maximum,
        reciprocal_condition=reciprocal_condition,
        threshold=threshold,
        boundary_tolerance=boundary_tolerance,
        method="symmetric_eigenvalue_ratio",
        decision=decision,
        reason=_conditioning_reason(decision),
    )
