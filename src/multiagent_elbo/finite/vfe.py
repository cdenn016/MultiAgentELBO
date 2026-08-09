"""Exact finite variational free energy and chain-rule decompositions."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np

from .measures import MarkovKernel, MeasurePair, ProbabilityMeasure


@dataclass(frozen=True)
class VfeChannelResult:
    """Fine/coarse VFE terms, with an explicit undefined residual branch."""

    fine_vfe: float
    coarse_vfe: float
    conditional_kl: float
    residual: float | None
    offending_state: str | None


@dataclass(frozen=True)
class BlockUpdateResult:
    """Independent local and collective VFE differences for one exact block update."""

    local_difference: float
    collective_difference: float
    residual: float | None
    outside_marginal: np.ndarray


def _kl_arrays(q: np.ndarray, p: np.ndarray) -> tuple[float, int | None]:
    support_violation = (q > 0.0) & (p == 0.0)
    locations = np.flatnonzero(support_violation)
    if locations.size:
        return math.inf, int(locations[0])
    positive_q = q > 0.0
    return float(np.sum(q[positive_q] * np.log(q[positive_q] / p[positive_q]))), None


def kl_divergence(q: ProbabilityMeasure, p: ProbabilityMeasure) -> float:
    """Return KL(q || p), as infinity when q is outside p's support."""
    if q.labels != p.labels:
        raise ValueError("KL measures must have matching labels")
    value, _ = _kl_arrays(q.masses, p.masses)
    return value


def free_energy(q: ProbabilityMeasure, pair: MeasurePair) -> float:
    """Return KL(q || posterior) - log evidence for a positive-evidence pair."""
    posterior = pair.posterior()
    if q.labels != posterior.labels:
        raise ValueError("recognition and measure-pair labels must match")
    divergence = kl_divergence(q, posterior)
    return math.inf if math.isinf(divergence) else divergence - math.log(pair.evidence)


def _reverse_conditional(
    measure: ProbabilityMeasure, channel: MarkovKernel
) -> tuple[np.ndarray, np.ndarray]:
    joint = measure.masses[:, np.newaxis] * channel.matrix
    coarse = joint.sum(axis=0)
    reverse = np.zeros_like(joint)
    np.divide(joint, coarse[np.newaxis, :], out=reverse, where=coarse[np.newaxis, :] > 0.0)
    return reverse, coarse


def _conditional_kl(
    q: ProbabilityMeasure, p: ProbabilityMeasure, channel: MarkovKernel
) -> float:
    q_reverse, q_coarse = _reverse_conditional(q, channel)
    p_reverse, _ = _reverse_conditional(p, channel)
    total = 0.0
    for target_index, weight in enumerate(q_coarse):
        if weight == 0.0:
            continue
        divergence, _ = _kl_arrays(q_reverse[:, target_index], p_reverse[:, target_index])
        if math.isinf(divergence):
            return math.inf
        total += float(weight) * divergence
    return total


def vfe_channel_decomposition(
    q: ProbabilityMeasure, pair: MeasurePair, channel: MarkovKernel
) -> VfeChannelResult:
    """Compute the finite KL chain rule for recognition and posterior laws."""
    posterior = pair.posterior()
    if q.labels != posterior.labels or q.labels != channel.source_labels:
        raise ValueError("recognition, posterior, and channel source labels must match")

    fine_kl, offending_index = _kl_arrays(q.masses, posterior.masses)
    q_coarse = q.pushforward(channel)
    posterior_coarse = posterior.pushforward(channel)
    coarse_kl, _ = _kl_arrays(q_coarse.masses, posterior_coarse.masses)
    conditional = _conditional_kl(q, posterior, channel)
    log_evidence = math.log(pair.evidence)
    fine_vfe = math.inf if math.isinf(fine_kl) else fine_kl - log_evidence
    coarse_vfe = math.inf if math.isinf(coarse_kl) else coarse_kl - log_evidence
    residual = (
        fine_vfe - coarse_vfe - conditional
        if all(math.isfinite(value) for value in (fine_vfe, coarse_vfe, conditional))
        else None
    )
    return VfeChannelResult(
        fine_vfe=fine_vfe,
        coarse_vfe=coarse_vfe,
        conditional_kl=conditional,
        residual=residual,
        offending_state=None if offending_index is None else q.labels[offending_index],
    )


def _probability_table(values: Sequence[object], name: str) -> np.ndarray:
    table = np.asarray(values, dtype=np.float64)
    if table.ndim == 0 or not np.all(np.isfinite(table)) or np.any(table < 0.0):
        raise ValueError(f"{name} must be a finite nonnegative probability table")
    if not math.isclose(float(table.sum()), 1.0, rel_tol=1e-10, abs_tol=1e-12):
        raise ValueError(f"{name} must sum to one")
    return table


def _block_conditionals(
    table: np.ndarray, block_axes: tuple[int, ...]
) -> tuple[np.ndarray, np.ndarray]:
    outside_axes = tuple(axis for axis in range(table.ndim) if axis not in block_axes)
    permutation = block_axes + outside_axes
    transposed = np.transpose(table, permutation)
    block_size = math.prod(table.shape[axis] for axis in block_axes)
    outside_size = math.prod(table.shape[axis] for axis in outside_axes)
    joint = transposed.reshape(block_size, outside_size)
    outside = joint.sum(axis=0)
    conditionals = np.zeros_like(joint)
    np.divide(joint, outside[np.newaxis, :], out=conditionals, where=outside[np.newaxis, :] > 0.0)
    return conditionals, outside


def _weighted_conditional_kl(
    q_conditionals: np.ndarray, q_outside: np.ndarray, p_conditionals: np.ndarray, p_outside: np.ndarray
) -> float:
    total = 0.0
    for index, weight in enumerate(q_outside):
        if weight == 0.0:
            continue
        if p_outside[index] == 0.0:
            return math.inf
        divergence, _ = _kl_arrays(q_conditionals[:, index], p_conditionals[:, index])
        if math.isinf(divergence):
            return math.inf
        total += float(weight) * divergence
    return total


def block_update_decomposition(
    posterior: Sequence[object],
    q_before: Sequence[object],
    q_after: Sequence[object],
    block_axes: tuple[int, ...],
) -> BlockUpdateResult:
    """Verify the exact fixed-outside local-to-collective VFE difference identity."""
    posterior_table = _probability_table(posterior, "posterior")
    before_table = _probability_table(q_before, "q_before")
    after_table = _probability_table(q_after, "q_after")
    if posterior_table.shape != before_table.shape or posterior_table.shape != after_table.shape:
        raise ValueError("posterior and recognition tables must have matching shapes")
    if not block_axes or len(set(block_axes)) != len(block_axes):
        raise ValueError("block_axes must be unique and nonempty")
    if any(type(axis) is not int or axis < 0 or axis >= posterior_table.ndim for axis in block_axes):
        raise ValueError("block_axes must index posterior axes")

    posterior_conditionals, posterior_outside = _block_conditionals(posterior_table, block_axes)
    before_conditionals, before_outside = _block_conditionals(before_table, block_axes)
    after_conditionals, after_outside = _block_conditionals(after_table, block_axes)
    if not np.array_equal(before_outside, after_outside):
        raise ValueError("q_before and q_after must have exactly equal outside marginals")

    local_before = _weighted_conditional_kl(
        before_conditionals, before_outside, posterior_conditionals, posterior_outside
    )
    local_after = _weighted_conditional_kl(
        after_conditionals, after_outside, posterior_conditionals, posterior_outside
    )
    collective_before, _ = _kl_arrays(before_table.ravel(), posterior_table.ravel())
    collective_after, _ = _kl_arrays(after_table.ravel(), posterior_table.ravel())
    if not all(math.isfinite(value) for value in (local_before, local_after, collective_before, collective_after)):
        raise ValueError("block identity requires finite posterior-KL values")
    local_difference = local_after - local_before
    collective_difference = collective_after - collective_before
    outside = before_outside.copy()
    outside.setflags(write=False)
    return BlockUpdateResult(
        local_difference=local_difference,
        collective_difference=collective_difference,
        residual=local_difference - collective_difference,
        outside_marginal=outside,
    )
