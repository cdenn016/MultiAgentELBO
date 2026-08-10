"""Exact finite measure-pair and variational-free-energy calculations."""

from .attention import AttentionDisintegration, StateConditionedAttentionLaw, compose_kernels
from .attention_experiment import AttentionExperimentResult, run_attention_experiment
from .agent_network_experiment import (
    AgentNetworkExperimentResult,
    run_agent_network_experiment,
)
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
from .counterexample_experiment import (
    FiniteCounterexampleExperimentResult,
    run_finite_counterexample_experiment,
)
from .information_history_experiment import (
    InformationHistoryExperimentResult,
    run_information_history_experiment,
)
from .measures import FiniteMeasure, MarkovKernel, MeasurePair, ProbabilityMeasure
from .scale_cocycle_experiment import (
    ScaleCocycleExperimentResult,
    run_scale_cocycle_experiment,
)
from .theory_oracle_experiment import (
    TheoryOracleExperimentResult,
    run_theory_oracle_experiment,
)
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
    "AgentNetworkExperimentResult",
    "BlockUpdateResult",
    "CategoricalDqmAnalysis",
    "CategoricalDqmExperimentResult",
    "CategoricalExponentialFamily",
    "DqmRemainderLadder",
    "FiniteCounterexampleExperimentResult",
    "FiniteMeasure",
    "MarkovKernel",
    "MeasurePair",
    "InformationHistoryExperimentResult",
    "ProbabilityMeasure",
    "ScaleCocycleExperimentResult",
    "StateConditionedAttentionLaw",
    "TheoryOracleExperimentResult",
    "VfeChannelResult",
    "analyze_categorical_dqm",
    "block_update_decomposition",
    "centered_log_probability_finite_difference",
    "centered_pushed_log_probability_finite_difference",
    "compose_kernels",
    "free_energy",
    "kl_divergence",
    "normalized_dqm_remainder_ladder",
    "run_agent_network_experiment",
    "run_attention_experiment",
    "run_categorical_dqm_experiment",
    "run_finite_counterexample_experiment",
    "run_information_history_experiment",
    "run_scale_cocycle_experiment",
    "run_theory_oracle_experiment",
    "vfe_channel_decomposition",
]
