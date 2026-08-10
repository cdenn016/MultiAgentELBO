"""Typed multivariate-Gaussian adapter for the ambient finite theory."""

from .experiment import GaussianExperimentResult, run_gaussian_experiment
from .fixed_ray_experiment import (
    GaussianFixedRayExperimentResult,
    build_cuda_gate_record,
    capture_idle_gpu_gate,
    publish_cuda_sentinel,
    run_cuda_sentinel,
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
    "build_cuda_gate_record",
    "capture_idle_gpu_gate",
    "galerkin_aggregate_precision",
    "publish_cuda_sentinel",
    "run_cuda_sentinel",
    "run_gaussian_experiment",
    "run_gaussian_fixed_ray_experiment",
    "schur_complement_precision",
]
