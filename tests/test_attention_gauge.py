from __future__ import annotations

import numpy as np
from numpy.testing import assert_allclose
import pytest

from multiagent_elbo.config import NumericsConfig
from multiagent_elbo.geometry.attention_gauge import (
    AttentionCovariantInputs,
    evaluate_attention,
    transform_attention_inputs,
)


NUMERICS = NumericsConfig(dtype="float64", atol=1e-12, rtol=1e-10)


def _literal_inputs() -> tuple[AttentionCovariantInputs, tuple[np.ndarray, ...]]:
    receiver_vectors = np.array([[1.0, 2.0], [-1.0, 1.0]])
    receiver_covectors = np.array([[2.0, -0.5], [1.0 / 3.0, 2.0]])
    source_vectors = np.array([[1.0, -1.0], [2.0, 0.5]])
    links = np.array(
        [
            [[[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.5], [0.0, 1.0]]],
            [[[2.0, 0.0], [1.0 / 3.0, 1.0]], [[1.0, 0.0], [-0.25, 1.5]]],
        ]
    )
    inputs = AttentionCovariantInputs(
        receiver_vectors,
        receiver_covectors,
        source_vectors,
        links,
        NUMERICS,
    )
    return inputs, (
        receiver_vectors,
        receiver_covectors,
        source_vectors,
        links,
    )


def _literal_frames() -> np.ndarray:
    return np.array(
        [
            [[2.0, 0.5], [0.0, 1.0]],
            [[1.0, 0.0], [1.0 / 3.0, 1.5]],
        ]
    )


def test_literal_attention_logits_and_scalar_law_are_independently_pinned():
    inputs, _ = _literal_inputs()

    evaluation = evaluate_attention(inputs)

    assert_allclose(evaluation.occupancy_logits, [1.0, 5.0 / 3.0])
    assert_allclose(
        evaluation.source_logits,
        [[5.0 / 2.0, 17.0 / 4.0], [-2.0 / 3.0, 7.0 / 6.0]],
    )
    assert_allclose(evaluation.eta, evaluation.alpha[:, None] * evaluation.beta)
    assert evaluation.eta.sum() == pytest.approx(1.0)


def test_inputs_and_evaluation_are_defensive_read_only_values():
    inputs, originals = _literal_inputs()
    evaluation = evaluate_attention(inputs)

    for original in originals:
        original[...] = 99.0

    assert_allclose(inputs.receiver_vectors, [[1.0, 2.0], [-1.0, 1.0]])
    assert_allclose(inputs.receiver_covectors, [[2.0, -0.5], [1.0 / 3.0, 2.0]])
    assert_allclose(inputs.source_vectors, [[1.0, -1.0], [2.0, 0.5]])
    assert_allclose(inputs.links[0, 1], [[1.0, 0.5], [0.0, 1.0]])
    for values in (
        inputs.receiver_vectors,
        inputs.receiver_covectors,
        inputs.source_vectors,
        inputs.links,
        evaluation.occupancy_logits,
        evaluation.source_logits,
        evaluation.alpha,
        evaluation.beta,
        evaluation.eta,
    ):
        assert not values.flags.writeable


@pytest.mark.parametrize(
    ("receiver_vectors", "receiver_covectors", "source_vectors", "links", "message"),
    [
        (
            np.ones(2),
            np.ones((2, 2)),
            np.ones((2, 2)),
            np.ones((2, 2, 2, 2)),
            r"receiver_vectors must have shape \(I, K\)",
        ),
        (
            np.ones((2, 2)),
            np.ones((3, 2)),
            np.ones((2, 2)),
            np.ones((2, 2, 2, 2)),
            "receiver_covectors shape",
        ),
        (
            np.ones((2, 2)),
            np.ones((2, 2)),
            np.ones((2, 3)),
            np.ones((2, 2, 2, 2)),
            "common fiber dimension",
        ),
        (
            np.ones((2, 2)),
            np.ones((2, 2)),
            np.ones((2, 2)),
            np.ones((2, 2, 2)),
            r"links must have shape \(I, J, K, K\)",
        ),
        (
            np.ones((2, 0)),
            np.ones((2, 0)),
            np.ones((2, 0)),
            np.ones((2, 2, 0, 0)),
            "fiber dimension must be positive",
        ),
        (
            np.array([[np.nan, 0.0], [0.0, 0.0]]),
            np.ones((2, 2)),
            np.ones((2, 2)),
            np.ones((2, 2, 2, 2)),
            "must contain only finite values",
        ),
    ],
)
def test_covariant_inputs_reject_malformed_shapes_and_nonfinite_entries(
    receiver_vectors: np.ndarray,
    receiver_covectors: np.ndarray,
    source_vectors: np.ndarray,
    links: np.ndarray,
    message: str,
):
    with pytest.raises(ValueError, match=message):
        AttentionCovariantInputs(
            receiver_vectors,
            receiver_covectors,
            source_vectors,
            links,
            NUMERICS,
        )


def test_covariant_inputs_require_a_numerics_config():
    with pytest.raises(TypeError, match="numerics must be a NumericsConfig"):
        AttentionCovariantInputs(
            np.ones((1, 1)),
            np.ones((1, 1)),
            np.ones((1, 1)),
            np.ones((1, 1, 1, 1)),
            object(),  # type: ignore[arg-type]
        )


def test_matched_single_node_frames_apply_pinned_action_and_preserve_scalars():
    inputs, _ = _literal_inputs()
    baseline = evaluate_attention(inputs)

    transformed_inputs = transform_attention_inputs(inputs, _literal_frames())
    transformed = evaluate_attention(transformed_inputs)

    assert_allclose(
        transformed_inputs.receiver_vectors,
        [[3.0, 2.0], [-1.0, 7.0 / 6.0]],
        atol=NUMERICS.atol,
        rtol=NUMERICS.rtol,
    )
    assert_allclose(
        transformed_inputs.receiver_covectors,
        [[1.0, -1.0], [-1.0 / 9.0, 4.0 / 3.0]],
        atol=NUMERICS.atol,
        rtol=NUMERICS.rtol,
    )
    assert_allclose(
        transformed_inputs.source_vectors,
        [[3.0 / 2.0, -1.0], [2.0, 17.0 / 12.0]],
        atol=NUMERICS.atol,
        rtol=NUMERICS.rtol,
    )
    assert_allclose(
        transformed_inputs.links,
        [
            [
                [[1.0, 0.0], [0.0, 1.0]],
                [[5.0 / 3.0, 1.0], [-2.0 / 9.0, 2.0 / 3.0]],
            ],
            [
                [[1.0, -1.0 / 2.0], [7.0 / 12.0, 29.0 / 24.0]],
                [[1.0, 0.0], [-13.0 / 24.0, 3.0 / 2.0]],
            ],
        ],
        atol=NUMERICS.atol,
        rtol=NUMERICS.rtol,
    )
    for actual, expected in (
        (transformed.occupancy_logits, baseline.occupancy_logits),
        (transformed.source_logits, baseline.source_logits),
        (transformed.alpha, baseline.alpha),
        (transformed.beta, baseline.beta),
        (transformed.eta, baseline.eta),
    ):
        assert_allclose(
            actual,
            expected,
            atol=NUMERICS.atol,
            rtol=NUMERICS.rtol,
        )
    for values in (
        transformed_inputs.receiver_vectors,
        transformed_inputs.receiver_covectors,
        transformed_inputs.source_vectors,
        transformed_inputs.links,
    ):
        assert not values.flags.writeable


def test_broken_link_control_changes_the_scalar_event_law_by_pinned_gap():
    inputs, _ = _literal_inputs()
    frames = _literal_frames()
    baseline = evaluate_attention(inputs)
    transformed_receiver_vectors = np.einsum(
        "ikl,il->ik", frames, inputs.receiver_vectors
    )
    transformed_source_vectors = np.einsum(
        "jkl,jl->jk", frames, inputs.source_vectors
    )
    transformed_receiver_covectors = np.stack(
        [
            np.linalg.solve(frame.T, covector)
            for frame, covector in zip(frames, inputs.receiver_covectors)
        ]
    )
    broken_inputs = AttentionCovariantInputs(
        transformed_receiver_vectors,
        transformed_receiver_covectors,
        transformed_source_vectors,
        inputs.links,
        NUMERICS,
    )

    broken = evaluate_attention(broken_inputs)
    eta_sup_gap = float(np.max(np.abs(baseline.eta - broken.eta)))

    assert eta_sup_gap == pytest.approx(0.2109948564038245, abs=1e-12)
    assert eta_sup_gap > 0.1


@pytest.mark.parametrize(
    ("frames", "message"),
    [
        (np.ones((2, 2)), r"frames must have shape \(N, K, K\)"),
        (np.array([np.eye(2)]), "one frame per shared node"),
        (np.array([np.eye(3), np.eye(3)]), "frame fiber dimension"),
        (
            np.array([np.diag([1.0, 0.0]), np.eye(2)]),
            "positive determinant",
        ),
        (
            np.array([np.diag([-1.0, 1.0]), np.eye(2)]),
            "positive determinant",
        ),
        (
            np.array([[[np.nan, 0.0], [0.0, 1.0]], np.eye(2)]),
            "finite",
        ),
        (
            np.array([np.diag([1.0e7, 1.0]), np.eye(2)]),
            "condition number exceeds max_frame_condition",
        ),
    ],
)
def test_transform_rejects_invalid_frame_families(
    frames: np.ndarray, message: str
):
    inputs, _ = _literal_inputs()

    with pytest.raises(ValueError, match=message):
        transform_attention_inputs(inputs, frames)


def test_transform_requires_receiver_and_source_axes_to_share_node_labels():
    inputs = AttentionCovariantInputs(
        np.ones((2, 2)),
        np.ones((2, 2)),
        np.ones((3, 2)),
        np.ones((2, 3, 2, 2)),
        NUMERICS,
    )

    with pytest.raises(ValueError, match="receiver and source counts must match"):
        transform_attention_inputs(inputs, np.array([np.eye(2), np.eye(2)]))
