"""Typed multivariate-Gaussian adapter for the ambient finite theory."""

from .experiment import GaussianExperimentResult, run_gaussian_experiment
from .confirmatory_analysis import (
    SECONDARY_ENDPOINT_IDS,
    analyze_primary,
    analyze_holdout,
    bootstrap_seed,
    exact_binomial_lower_tail,
    exact_sign_pvalue,
    holm_adjust,
    percentile_interval,
    summarize_paired_job,
)
from .fixed_ray_experiment import (
    GaussianFixedRayExperimentResult,
    build_confirmatory_gate_record,
    build_cuda_gate_record,
    capture_idle_gpu_gate,
    publish_cuda_sentinel,
    publish_confirmatory_experiment,
    run_confirmatory_holdout,
    run_confirmatory_job,
    run_confirmatory_primary,
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
    "SECONDARY_ENDPOINT_IDS",
    "analyze_primary",
    "analyze_holdout",
    "apply_frame_change",
    "build_cuda_gate_record",
    "build_confirmatory_gate_record",
    "bootstrap_seed",
    "capture_idle_gpu_gate",
    "exact_binomial_lower_tail",
    "exact_sign_pvalue",
    "galerkin_aggregate_precision",
    "holm_adjust",
    "percentile_interval",
    "publish_cuda_sentinel",
    "publish_confirmatory_experiment",
    "run_confirmatory_job",
    "run_confirmatory_holdout",
    "run_confirmatory_primary",
    "run_cuda_sentinel",
    "run_gaussian_experiment",
    "run_gaussian_fixed_ray_experiment",
    "schur_complement_precision",
    "summarize_paired_job",
]
