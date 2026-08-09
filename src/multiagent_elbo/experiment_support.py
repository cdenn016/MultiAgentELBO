"""Shared immutable metric records for experiment laboratories."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np


MetricStatus = Literal["pass", "fail", "inconclusive"]
TheoremStatus = Literal[
    "established_conditional_identity",
    "finite_metamorphic_identity",
    "negative_control",
]


@dataclass(frozen=True)
class MetricRecord:
    """One implementation check, separate from its theorem status."""

    value: float
    tolerance: float
    status: MetricStatus
    interpretation: str
    assessment_scope: Literal["implementation_check"]
    theorem_status: TheoremStatus


def target_metric(
    value: float,
    tolerance: float,
    *,
    target: float,
    interpretation: str,
    theorem_status: TheoremStatus,
) -> MetricRecord:
    """Create a metric which passes within tolerance of its target."""
    return MetricRecord(
        value=float(value),
        tolerance=float(tolerance),
        status="pass" if abs(value - target) <= tolerance else "fail",
        interpretation=interpretation,
        assessment_scope="implementation_check",
        theorem_status=theorem_status,
    )


def lower_bounded_metric(
    value: float,
    tolerance: float,
    *,
    lower_bound: float,
    interpretation: str,
    theorem_status: TheoremStatus,
) -> MetricRecord:
    """Create a metric which passes when it reaches its lower bound."""
    return MetricRecord(
        value=float(value),
        tolerance=float(tolerance),
        status="pass" if value >= lower_bound - tolerance else "fail",
        interpretation=interpretation,
        assessment_scope="implementation_check",
        theorem_status=theorem_status,
    )


def readonly_array(values: object, dtype: object = np.float64) -> np.ndarray:
    """Copy values into an immutable C-contiguous numerical array."""
    array = np.array(values, dtype=dtype, copy=True, order="C")
    array.setflags(write=False)
    return array


__all__ = [
    "MetricRecord",
    "MetricStatus",
    "TheoremStatus",
    "lower_bounded_metric",
    "readonly_array",
    "target_metric",
]
