"""Exact finite measure-pair and variational-free-energy calculations."""

from .attention import AttentionDisintegration, StateConditionedAttentionLaw, compose_kernels
from .attention_experiment import AttentionExperimentResult, run_attention_experiment
from .categorical import CategoricalExponentialFamily
from .categorical_dqm import (
    CategoricalDqmAnalysis,
    DqmRemainderLadder,
    analyze_categorical_dqm,
    centered_log_probability_finite_difference,
    centered_pushed_log_probability_finite_difference,
    normalized_dqm_remainder_ladder,
)
from .categorical_dqm_experiment import (
    CategoricalDqmExperimentResult,
    run_categorical_dqm_experiment,
)
from .measures import FiniteMeasure, MarkovKernel, MeasurePair, ProbabilityMeasure
from .vfe import (
    BlockUpdateResult,
    VfeChannelResult,
    block_update_decomposition,
    free_energy,
    kl_divergence,
    vfe_channel_decomposition,
)

__all__ = [
    "AttentionDisintegration",
    "AttentionExperimentResult",
    "BlockUpdateResult",
    "CategoricalDqmAnalysis",
    "CategoricalDqmExperimentResult",
    "CategoricalExponentialFamily",
    "DqmRemainderLadder",
    "FiniteMeasure",
    "MarkovKernel",
    "MeasurePair",
    "ProbabilityMeasure",
    "StateConditionedAttentionLaw",
    "VfeChannelResult",
    "analyze_categorical_dqm",
    "block_update_decomposition",
    "centered_log_probability_finite_difference",
    "centered_pushed_log_probability_finite_difference",
    "compose_kernels",
    "free_energy",
    "kl_divergence",
    "normalized_dqm_remainder_ladder",
    "run_attention_experiment",
    "run_categorical_dqm_experiment",
    "vfe_channel_decomposition",
]
