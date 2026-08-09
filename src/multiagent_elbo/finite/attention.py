"""Pure finite state-conditioned marked-event attention laws."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from numpy.typing import ArrayLike

from multiagent_elbo.config import NumericsConfig
from multiagent_elbo.finite.measures import MarkovKernel, ProbabilityMeasure


def _labels(labels: Sequence[str], name: str) -> tuple[str, ...]:
    try:
        result = tuple(labels)
    except TypeError as exc:
        raise TypeError(f"{name} must be a sequence of labels") from exc
    if not result:
        raise ValueError(f"{name} must be nonempty")
    if not all(isinstance(label, str) for label in result):
        raise TypeError(f"{name} entries must be strings")
    if any(not label for label in result):
        raise ValueError(f"{name} entries must be nonempty")
    if len(set(result)) != len(result):
        raise ValueError(f"{name} must be unique")
    return result


def _finite_nonnegative(values: ArrayLike, name: str) -> np.ndarray:
    try:
        result = np.array(values, dtype=np.float64, copy=True, order="C")
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{name} must be numeric") from exc
    if not np.all(np.isfinite(result)) or np.any(result < 0.0):
        raise ValueError(f"{name} must be finite nonnegative")
    return result


def _readonly(values: ArrayLike, *, dtype: object | None = np.float64) -> np.ndarray:
    result = np.array(values, dtype=dtype, copy=True, order="C")
    result.setflags(write=False)
    return result


@dataclass(frozen=True)
class AttentionDisintegration:
    """Receiver occupancies and conditional source rows of an attention law."""

    alpha_given_state: np.ndarray
    beta_given_state: np.ndarray
    positive_state_mask: np.ndarray
    positive_receiver_mask: np.ndarray


@dataclass(frozen=True, init=False)
class StateConditionedAttentionLaw:
    """A conditional probability law on receiver/source marked events."""

    state_probability: ProbabilityMeasure
    receiver_labels: tuple[str, ...]
    source_labels: tuple[str, ...]
    eta_given_state: np.ndarray
    numerics: NumericsConfig

    def __init__(
        self,
        state_probability: ProbabilityMeasure,
        receiver_labels: Sequence[str],
        source_labels: Sequence[str],
        eta_given_state: ArrayLike,
    ) -> None:
        if not isinstance(state_probability, ProbabilityMeasure):
            raise TypeError("state_probability must be a ProbabilityMeasure")
        receivers = _labels(receiver_labels, "receiver_labels")
        sources = _labels(source_labels, "source_labels")
        eta = _finite_nonnegative(eta_given_state, "eta_given_state")
        expected_shape = (
            len(state_probability.labels),
            len(receivers),
            len(sources),
        )
        if eta.shape != expected_shape:
            raise ValueError(
                "eta_given_state shape must match states, receivers, and sources"
            )
        positive_state = state_probability.masses > 0.0
        if not np.allclose(
            eta[positive_state].sum(axis=(1, 2)),
            1.0,
            rtol=state_probability.numerics.rtol,
            atol=state_probability.numerics.atol,
        ):
            raise ValueError("positive-state eta mass must equal one")
        if np.any(eta[~positive_state] != 0.0):
            raise ValueError("zero-probability-state eta must be zero")
        object.__setattr__(self, "state_probability", state_probability)
        object.__setattr__(self, "receiver_labels", receivers)
        object.__setattr__(self, "source_labels", sources)
        object.__setattr__(self, "eta_given_state", _readonly(eta))
        object.__setattr__(self, "numerics", state_probability.numerics)

    @classmethod
    def from_alpha_beta(
        cls,
        state_probability: ProbabilityMeasure,
        receiver_labels: Sequence[str],
        source_labels: Sequence[str],
        alpha_given_state: ArrayLike,
        beta_given_state: ArrayLike,
    ) -> "StateConditionedAttentionLaw":
        if not isinstance(state_probability, ProbabilityMeasure):
            raise TypeError("state_probability must be a ProbabilityMeasure")
        receivers = _labels(receiver_labels, "receiver_labels")
        sources = _labels(source_labels, "source_labels")
        alpha = _finite_nonnegative(alpha_given_state, "alpha_given_state")
        beta = _finite_nonnegative(beta_given_state, "beta_given_state")
        state_count = len(state_probability.labels)
        if alpha.shape != (state_count, len(receivers)):
            raise ValueError(
                "alpha_given_state shape must match states and receivers"
            )
        if beta.shape != (state_count, len(receivers), len(sources)):
            raise ValueError(
                "beta_given_state shape must match states, receivers, and sources"
            )
        positive_state = state_probability.masses > 0.0
        if not np.allclose(
            alpha[positive_state].sum(axis=1),
            1.0,
            rtol=state_probability.numerics.rtol,
            atol=state_probability.numerics.atol,
        ):
            raise ValueError("positive-state alpha mass must equal one")
        if np.any(alpha[~positive_state] != 0.0):
            raise ValueError("zero-probability-state alpha must be zero")
        positive_receiver = positive_state[:, None] & (alpha > 0.0)
        if not np.allclose(
            beta[positive_receiver].sum(axis=1),
            1.0,
            rtol=state_probability.numerics.rtol,
            atol=state_probability.numerics.atol,
        ):
            raise ValueError("active beta rows must sum to one")
        if np.any(beta[~positive_receiver] != 0.0):
            raise ValueError("inactive beta rows must be zero")
        return cls(
            state_probability,
            receivers,
            sources,
            alpha[..., None] * beta,
        )

    def disintegrate(self) -> AttentionDisintegration:
        positive_state = self.state_probability.masses > 0.0
        alpha = self.eta_given_state.sum(axis=2)
        positive_receiver = positive_state[:, None] & (alpha > 0.0)
        beta = np.zeros_like(self.eta_given_state)
        np.divide(
            self.eta_given_state,
            alpha[..., None],
            out=beta,
            where=positive_receiver[..., None],
        )
        return AttentionDisintegration(
            alpha_given_state=_readonly(alpha),
            beta_given_state=_readonly(beta),
            positive_state_mask=_readonly(positive_state, dtype=np.bool_),
            positive_receiver_mask=_readonly(positive_receiver, dtype=np.bool_),
        )

    def pushforward(
        self,
        state_channel: MarkovKernel,
        receiver_partition: MarkovKernel,
        source_partition: MarkovKernel,
    ) -> "StateConditionedAttentionLaw":
        for kernel, name in (
            (state_channel, "state_channel"),
            (receiver_partition, "receiver_partition"),
            (source_partition, "source_partition"),
        ):
            if not isinstance(kernel, MarkovKernel):
                raise TypeError(f"{name} must be a MarkovKernel")
            if kernel.numerics != self.numerics:
                raise ValueError(f"{name} numerics must match law numerics")
        if state_channel.source_labels != self.state_probability.labels:
            raise ValueError(
                "state_channel source labels must equal law state labels"
            )
        if receiver_partition.source_labels != self.receiver_labels:
            raise ValueError(
                "receiver_partition source labels must equal law receiver labels"
            )
        if source_partition.source_labels != self.source_labels:
            raise ValueError(
                "source_partition source labels must equal law source labels"
            )

        joint = (
            self.state_probability.masses[:, None, None] * self.eta_given_state
        )
        coarse_joint = np.einsum(
            "yz,iI,jJ,yij->zIJ",
            state_channel.matrix,
            receiver_partition.matrix,
            source_partition.matrix,
            joint,
        )
        coarse_masses = self.state_probability.masses @ state_channel.matrix
        coarse_eta = np.zeros_like(coarse_joint)
        positive_coarse_state = coarse_masses > 0.0
        np.divide(
            coarse_joint,
            coarse_masses[:, None, None],
            out=coarse_eta,
            where=positive_coarse_state[:, None, None],
        )
        coarse_probability = ProbabilityMeasure(
            state_channel.target_labels,
            coarse_masses,
            self.numerics,
        )
        return StateConditionedAttentionLaw(
            coarse_probability,
            receiver_partition.target_labels,
            source_partition.target_labels,
            coarse_eta,
        )


def compose_kernels(first: MarkovKernel, second: MarkovKernel) -> MarkovKernel:
    """Compose two ordered finite Markov kernels."""
    if not isinstance(first, MarkovKernel):
        raise TypeError("first must be a MarkovKernel")
    if not isinstance(second, MarkovKernel):
        raise TypeError("second must be a MarkovKernel")
    if first.target_labels != second.source_labels:
        raise ValueError("first target labels must equal second source labels")
    if first.numerics != second.numerics:
        raise ValueError("kernel numerics must match")
    return MarkovKernel(
        first.source_labels,
        second.target_labels,
        first.matrix @ second.matrix,
        first.numerics,
    )
