"""Exact finite measure-pair and variational-free-energy calculations."""

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
    "BlockUpdateResult",
    "FiniteMeasure",
    "MarkovKernel",
    "MeasurePair",
    "ProbabilityMeasure",
    "VfeChannelResult",
    "block_update_decomposition",
    "free_energy",
    "kl_divergence",
    "vfe_channel_decomposition",
]
