"""Typed multivariate-Gaussian adapter for the ambient finite theory."""

from .experiment import GaussianExperimentResult, run_gaussian_experiment
from .fixed_ray_experiment import (
    GaussianFixedRayExperimentResult,
    run_gaussian_fixed_ray_experiment,
)
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
    "GaussianFixedRayExperimentResult",
    "GaussianGaugeResult",
    "GaussianInteraction",
    "GaussianNumericalError",
    "apply_frame_change",
    "galerkin_aggregate_precision",
    "run_gaussian_experiment",
    "run_gaussian_fixed_ray_experiment",
    "schur_complement_precision",
]
