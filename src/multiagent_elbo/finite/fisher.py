"""Finite conditional-score and Fisher-information decompositions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence

import numpy as np

from .measures import MarkovKernel, ProbabilityMeasure


FisherIdentityScope = Literal["finite_centered_score_fixed_kernel"]


def _readonly(values: np.ndarray) -> np.ndarray:
    result = np.array(values, dtype=np.float64, copy=True, order="C")
    result.setflags(write=False)
    return result


@dataclass(frozen=True)
class FisherChannelResult:
    """Conditional covariance identity for a supplied centered finite score.

    The channel is declared fixed and parameter-independent. This finite vector
    calculation does not establish differentiability in quadratic mean or verify
    parameter independence across a family of kernels.
    """

    joint_mass: np.ndarray
    coarse_probability: np.ndarray
    coarse_score: np.ndarray
    fine_fisher: np.ndarray
    coarse_fisher: np.ndarray
    conditional_covariance: np.ndarray
    residual: np.ndarray
    minimum_defect_eigenvalue: float
    defect_psd_tolerance: float
    defect_is_psd: bool
    identity_scope: FisherIdentityScope = "finite_centered_score_fixed_kernel"
    establishes_dqm: bool = False


def _score_matrix(score: Sequence[object], state_count: int) -> np.ndarray:
    values = np.array(score, dtype=np.float64, copy=True, order="C")
    if values.ndim == 1:
        values = values[:, np.newaxis]
    elif values.ndim != 2:
        raise ValueError("score must be one- or two-dimensional")
    if values.shape[0] != state_count:
        raise ValueError("score must have one row per source state")
    if values.shape[1] == 0:
        raise ValueError("score must contain at least one parameter coordinate")
    if not np.all(np.isfinite(values)):
        raise ValueError("score must be finite")
    return values


def fisher_channel_decomposition(
    probability: ProbabilityMeasure,
    score: Sequence[object],
    channel: MarkovKernel,
) -> FisherChannelResult:
    """Compute the finite conditional-expectation/covariance Fisher identity."""
    if not isinstance(probability, ProbabilityMeasure):
        raise TypeError("probability must be a ProbabilityMeasure")
    if not isinstance(channel, MarkovKernel):
        raise TypeError("channel must be a MarkovKernel")
    if probability.labels != channel.source_labels:
        raise ValueError("probability labels must equal channel source labels")
    if probability.numerics != channel.numerics:
        raise ValueError("probability and channel numerics must match")

    values = _score_matrix(score, len(probability.labels))
    p = probability.masses
    numerics = probability.numerics
    center = p @ values
    center_scale = p @ np.abs(values)
    center_tolerance = numerics.atol + numerics.rtol * np.maximum(1.0, center_scale)
    if np.any(np.abs(center) > center_tolerance):
        coordinates = np.flatnonzero(np.abs(center) > center_tolerance).tolist()
        raise ValueError(f"score must be centered in every coordinate; failed {coordinates}")

    joint = p[:, np.newaxis] * channel.matrix
    coarse_probability = joint.sum(axis=0)
    with np.errstate(over="ignore", invalid="ignore"):
        weighted_scores = joint.T @ values
        coarse_score = np.zeros(
            (len(channel.target_labels), values.shape[1]), dtype=np.float64
        )
        np.divide(
            weighted_scores,
            coarse_probability[:, np.newaxis],
            out=coarse_score,
            where=coarse_probability[:, np.newaxis] > 0.0,
        )

        fine_fisher = np.einsum("x,xi,xj->ij", p, values, values)
        coarse_fisher = np.einsum(
            "z,zi,zj->ij", coarse_probability, coarse_score, coarse_score
        )

        conditional_covariance = np.zeros_like(fine_fisher)
        for target_index in range(len(channel.target_labels)):
            deviations = values - coarse_score[target_index]
            conditional_covariance += np.einsum(
                "x,xi,xj->ij",
                joint[:, target_index],
                deviations,
                deviations,
            )

        residual = fine_fisher - coarse_fisher - conditional_covariance
    if not all(
        np.all(np.isfinite(array))
        for array in (
            coarse_score,
            fine_fisher,
            coarse_fisher,
            conditional_covariance,
            residual,
        )
    ):
        raise ValueError("nonfinite Fisher intermediate or result")
    symmetric_defect = 0.5 * (
        conditional_covariance + conditional_covariance.T
    )
    defect_eigenvalues = np.linalg.eigvalsh(symmetric_defect)
    minimum_defect_eigenvalue = float(defect_eigenvalues[0])
    defect_scale = max(1.0, float(np.linalg.norm(symmetric_defect, ord=2)))
    defect_psd_tolerance = numerics.atol + numerics.rtol * defect_scale

    return FisherChannelResult(
        joint_mass=_readonly(joint),
        coarse_probability=_readonly(coarse_probability),
        coarse_score=_readonly(coarse_score),
        fine_fisher=_readonly(fine_fisher),
        coarse_fisher=_readonly(coarse_fisher),
        conditional_covariance=_readonly(conditional_covariance),
        residual=_readonly(residual),
        minimum_defect_eigenvalue=minimum_defect_eigenvalue,
        defect_psd_tolerance=defect_psd_tolerance,
        defect_is_psd=minimum_defect_eigenvalue >= -defect_psd_tolerance,
    )
