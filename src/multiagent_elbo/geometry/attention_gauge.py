"""Gauge-covariant scalar attention contractions."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from multiagent_elbo.config import NumericsConfig


def _readonly(values: object) -> np.ndarray:
    result = np.array(values, dtype=np.float64, copy=True)
    result.setflags(write=False)
    return result


@dataclass(frozen=True, init=False)
class AttentionCovariantInputs:
    """Vectors, covectors, and source-to-receiver links in local frames."""

    receiver_vectors: np.ndarray
    receiver_covectors: np.ndarray
    source_vectors: np.ndarray
    links: np.ndarray
    numerics: NumericsConfig

    def __init__(
        self,
        receiver_vectors: object,
        receiver_covectors: object,
        source_vectors: object,
        links: object,
        numerics: NumericsConfig,
    ) -> None:
        if not isinstance(numerics, NumericsConfig):
            raise TypeError("numerics must be a NumericsConfig")
        receivers = np.asarray(receiver_vectors, dtype=np.float64)
        covectors = np.asarray(receiver_covectors, dtype=np.float64)
        sources = np.asarray(source_vectors, dtype=np.float64)
        transports = np.asarray(links, dtype=np.float64)
        if receivers.ndim != 2 or receivers.shape[0] < 1:
            raise ValueError("receiver_vectors must have shape (I, K)")
        receiver_count, fiber_dimension = receivers.shape
        if fiber_dimension < 1:
            raise ValueError("fiber dimension must be positive")
        if covectors.shape != receivers.shape:
            raise ValueError("receiver_covectors shape must match receiver_vectors")
        if sources.ndim != 2 or sources.shape[0] < 1:
            raise ValueError("source_vectors must have shape (J, K)")
        source_count = sources.shape[0]
        if sources.shape[1] != fiber_dimension:
            raise ValueError("all arrays must share a common fiber dimension")
        if transports.ndim != 4:
            raise ValueError("links must have shape (I, J, K, K)")
        if transports.shape != (
            receiver_count,
            source_count,
            fiber_dimension,
            fiber_dimension,
        ):
            raise ValueError(
                "links shape must match receiver, source, and common fiber dimensions"
            )
        arrays = (receivers, covectors, sources, transports)
        if not all(np.all(np.isfinite(values)) for values in arrays):
            raise ValueError("attention inputs must contain only finite values")
        object.__setattr__(self, "receiver_vectors", _readonly(receivers))
        object.__setattr__(self, "receiver_covectors", _readonly(covectors))
        object.__setattr__(self, "source_vectors", _readonly(sources))
        object.__setattr__(self, "links", _readonly(transports))
        object.__setattr__(self, "numerics", numerics)


@dataclass(frozen=True)
class AttentionGaugeEvaluation:
    """Invariant logits and their scalar marked-event law."""

    occupancy_logits: np.ndarray
    source_logits: np.ndarray
    alpha: np.ndarray
    beta: np.ndarray
    eta: np.ndarray


def _softmax(values: np.ndarray, *, axis: int) -> np.ndarray:
    shifted = values - np.max(values, axis=axis, keepdims=True)
    weights = np.exp(shifted)
    return weights / np.sum(weights, axis=axis, keepdims=True)


def evaluate_attention(inputs: AttentionCovariantInputs) -> AttentionGaugeEvaluation:
    """Contract covariant inputs and form a stable scalar attention law."""
    if not isinstance(inputs, AttentionCovariantInputs):
        raise TypeError("inputs must be an AttentionCovariantInputs")
    occupancy_logits = np.einsum(
        "ik,ik->i", inputs.receiver_covectors, inputs.receiver_vectors
    )
    source_logits = np.einsum(
        "ik,ijkl,jl->ij",
        inputs.receiver_covectors,
        inputs.links,
        inputs.source_vectors,
    )
    if not (
        np.all(np.isfinite(occupancy_logits))
        and np.all(np.isfinite(source_logits))
    ):
        raise ValueError("attention logits must be finite")
    alpha = _softmax(occupancy_logits, axis=0)
    beta = _softmax(source_logits, axis=1)
    eta = alpha[:, None] * beta
    return AttentionGaugeEvaluation(
        occupancy_logits=_readonly(occupancy_logits),
        source_logits=_readonly(source_logits),
        alpha=_readonly(alpha),
        beta=_readonly(beta),
        eta=_readonly(eta),
    )


def transform_attention_inputs(
    inputs: AttentionCovariantInputs, frames: object
) -> AttentionCovariantInputs:
    """Apply one coherent local-frame family to all node-indexed inputs."""
    if not isinstance(inputs, AttentionCovariantInputs):
        raise TypeError("inputs must be an AttentionCovariantInputs")
    receiver_count, fiber_dimension = inputs.receiver_vectors.shape
    source_count = inputs.source_vectors.shape[0]
    if receiver_count != source_count:
        raise ValueError(
            "receiver and source counts must match for one shared node-frame family"
        )
    checked_frames = np.asarray(frames, dtype=np.float64)
    if (
        checked_frames.ndim != 3
        or checked_frames.shape[1] != checked_frames.shape[2]
    ):
        raise ValueError("frames must have shape (N, K, K)")
    if checked_frames.shape[0] != receiver_count:
        raise ValueError("frames must contain one frame per shared node")
    if checked_frames.shape[1] != fiber_dimension:
        raise ValueError("frame fiber dimension must match attention inputs")
    if not np.all(np.isfinite(checked_frames)):
        raise ValueError("frames must contain only finite values")
    for index, frame in enumerate(checked_frames):
        determinant_sign, log_absolute_determinant = np.linalg.slogdet(frame)
        if determinant_sign <= 0.0 or not np.isfinite(log_absolute_determinant):
            raise ValueError(f"frame {index} must have positive determinant")
        condition = float(np.linalg.cond(frame))
        if (
            not np.isfinite(condition)
            or condition > inputs.numerics.max_frame_condition
        ):
            raise ValueError(
                f"frame {index} condition number exceeds max_frame_condition"
            )
    transformed_receiver_vectors = np.einsum(
        "ikl,il->ik", checked_frames, inputs.receiver_vectors
    )
    transformed_receiver_covectors = np.stack(
        [
            np.linalg.solve(frame.T, covector)
            for frame, covector in zip(
                checked_frames, inputs.receiver_covectors, strict=True
            )
        ]
    )
    transformed_source_vectors = np.einsum(
        "jkl,jl->jk", checked_frames, inputs.source_vectors
    )
    transformed_links = np.empty_like(inputs.links)
    for receiver_index, receiver_frame in enumerate(checked_frames):
        for source_index, source_frame in enumerate(checked_frames):
            left_action = receiver_frame @ inputs.links[receiver_index, source_index]
            transformed_links[receiver_index, source_index] = np.linalg.solve(
                source_frame.T, left_action.T
            ).T
    return AttentionCovariantInputs(
        transformed_receiver_vectors,
        transformed_receiver_covectors,
        transformed_source_vectors,
        transformed_links,
        inputs.numerics,
    )
