"""Componentwise finite Borel relabeling metamorphics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence

import numpy as np

from multiagent_elbo.finite.interactions import (
    InteractionDecomposition,
    InteractionProjection,
    hoeffding_decompose,
    retain_interaction_order,
)
from multiagent_elbo.finite.measures import (
    FiniteMeasure,
    MarkovKernel,
    MeasurePair,
    ProbabilityMeasure,
)
from multiagent_elbo.finite.permutations import FinitePermutation
from multiagent_elbo.finite.vfe import kl_divergence, vfe_channel_decomposition


FiniteGaugeScope = Literal["componentwise_finite_borel_relabeling"]


def _readonly(values: object) -> np.ndarray:
    result = np.array(values, dtype=np.float64, copy=True, order="C")
    result.setflags(write=False)
    return result


@dataclass(frozen=True)
class FiniteGaugeResiduals:
    """Signed invariant differences and sup-norm intertwining residuals."""

    evidence: float
    kl: float
    vfe: float
    conditional_kl: float
    interaction_reconstruction: float
    retained_projection_intertwining: float
    channel_intertwining: float


@dataclass(frozen=True)
class FiniteRelabelingResult:
    """All objects after one coherent componentwise finite relabeling."""

    recognition: ProbabilityMeasure
    pair: MeasurePair
    channel: MarkovKernel
    values: np.ndarray
    axis_references: tuple[np.ndarray, ...]
    interaction_decomposition: InteractionDecomposition
    retained_projection: InteractionProjection
    residuals: FiniteGaugeResiduals
    scope: FiniteGaugeScope = "componentwise_finite_borel_relabeling"


def _require_permutation(value: object, name: str) -> FinitePermutation:
    if not isinstance(value, FinitePermutation):
        raise TypeError(f"{name} must be a FinitePermutation")
    return value


def _pull_product_array(
    values: np.ndarray, permutations: tuple[FinitePermutation, ...]
) -> np.ndarray:
    result = np.array(values, dtype=np.float64, copy=True, order="C")
    for axis, permutation in enumerate(permutations):
        result = permutation.pullback_axis(result, axis)
    return result


def apply_site_relabeling(
    *,
    q: ProbabilityMeasure,
    pair: MeasurePair,
    channel: MarkovKernel,
    values: Sequence[object],
    axis_references: Sequence[Sequence[float]],
    source_permutation: FinitePermutation,
    target_permutation: FinitePermutation,
    axis_permutations: Sequence[FinitePermutation],
    retained_interaction_order: int,
) -> FiniteRelabelingResult:
    """Relabel every typed finite object coherently and compute metamorphic residuals.

    This is scoped to componentwise finite Borel relabelings. It is not an API for
    arbitrary gauge fields, connections, or holonomy.
    """
    source = _require_permutation(source_permutation, "source_permutation")
    target = _require_permutation(target_permutation, "target_permutation")
    if not isinstance(q, ProbabilityMeasure):
        raise TypeError("q must be a ProbabilityMeasure")
    if not isinstance(pair, MeasurePair):
        raise TypeError("pair must be a MeasurePair")
    if not isinstance(channel, MarkovKernel):
        raise TypeError("channel must be a MarkovKernel")
    if source.size != len(q.labels):
        raise ValueError("source permutation size must match recognition support")
    if target.size != len(channel.target_labels):
        raise ValueError("target permutation size must match channel target support")

    action = np.array(values, dtype=np.float64, copy=True, order="C")
    axis_permutation_tuple = tuple(axis_permutations)
    if len(axis_permutation_tuple) != action.ndim:
        raise ValueError("one axis permutation is required per value axis")
    for axis, permutation in enumerate(axis_permutation_tuple):
        typed = _require_permutation(permutation, f"axis_permutations[{axis}]")
        if typed.size != action.shape[axis]:
            raise ValueError(f"axis permutation {axis} size must match value axis")

    original_decomposition = hoeffding_decompose(action, axis_references)
    original_projection = retain_interaction_order(
        original_decomposition, retained_interaction_order
    )
    original_vfe = vfe_channel_decomposition(q, pair, channel)
    original_kl = kl_divergence(q, pair.posterior())

    relabeled_q = ProbabilityMeasure(
        q.labels, q.masses @ source.matrix, q.numerics
    )
    relabeled_pair = MeasurePair(
        ProbabilityMeasure(
            pair.reference.labels,
            pair.reference.masses @ source.matrix,
            pair.reference.numerics,
        ),
        FiniteMeasure(
            pair.evidence_measure.labels,
            pair.evidence_measure.masses @ source.matrix,
            pair.evidence_measure.numerics,
        ),
    )
    relabeled_channel = MarkovKernel(
        channel.source_labels,
        channel.target_labels,
        source.matrix.T @ channel.matrix @ target.matrix,
        channel.numerics,
    )
    relabeled_references = tuple(
        _readonly(reference @ permutation.matrix)
        for reference, permutation in zip(
            original_decomposition.axis_references, axis_permutation_tuple
        )
    )
    relabeled_values = _pull_product_array(action, axis_permutation_tuple)
    relabeled_decomposition = hoeffding_decompose(
        relabeled_values, relabeled_references
    )
    relabeled_projection = retain_interaction_order(
        relabeled_decomposition, retained_interaction_order
    )

    relabeled_vfe = vfe_channel_decomposition(
        relabeled_q, relabeled_pair, relabeled_channel
    )
    relabeled_kl = kl_divergence(relabeled_q, relabeled_pair.posterior())
    expected_retained = _pull_product_array(
        original_projection.retained_values, axis_permutation_tuple
    )
    channel_left = relabeled_q.masses @ relabeled_channel.matrix
    channel_right = (q.masses @ channel.matrix) @ target.matrix
    residuals = FiniteGaugeResiduals(
        evidence=relabeled_pair.evidence - pair.evidence,
        kl=relabeled_kl - original_kl,
        vfe=relabeled_vfe.fine_vfe - original_vfe.fine_vfe,
        conditional_kl=(
            relabeled_vfe.conditional_kl - original_vfe.conditional_kl
        ),
        interaction_reconstruction=(
            relabeled_decomposition.reconstruction_residual_sup
            - original_decomposition.reconstruction_residual_sup
        ),
        retained_projection_intertwining=float(
            np.max(np.abs(relabeled_projection.retained_values - expected_retained))
        ),
        channel_intertwining=float(np.max(np.abs(channel_left - channel_right))),
    )
    return FiniteRelabelingResult(
        recognition=relabeled_q,
        pair=relabeled_pair,
        channel=relabeled_channel,
        values=_readonly(relabeled_values),
        axis_references=relabeled_references,
        interaction_decomposition=relabeled_decomposition,
        retained_projection=relabeled_projection,
        residuals=residuals,
    )
