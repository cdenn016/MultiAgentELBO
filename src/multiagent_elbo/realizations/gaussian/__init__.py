"""Typed multivariate-Gaussian adapter for the ambient finite theory."""

from .experiment import GaussianExperimentResult, run_gaussian_experiment
from .gauge import GaussianGaugeResult, apply_frame_change
from .interactions import (
    GaussianAggregationResult,
    GaussianInteraction,
    GaussianNumericalError,
    galerkin_aggregate_precision,
    schur_complement_precision,
)

__all__ = [
    "GaussianAggregationResult",
    "GaussianExperimentResult",
    "GaussianGaugeResult",
    "GaussianInteraction",
    "GaussianNumericalError",
    "apply_frame_change",
    "galerkin_aggregate_precision",
    "run_gaussian_experiment",
    "schur_complement_precision",
]
