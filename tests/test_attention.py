from __future__ import annotations

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
import pytest

from multiagent_elbo.config import NumericsConfig
from multiagent_elbo.finite import attention
from multiagent_elbo.finite.attention import StateConditionedAttentionLaw
from multiagent_elbo.finite.measures import MarkovKernel, ProbabilityMeasure


NUMERICS = NumericsConfig(dtype="float64", atol=1e-12, rtol=1e-10)
STATE_LABELS = ("active", "null")
RECEIVER_LABELS = ("receiver-0", "receiver-1")
SOURCE_LABELS = ("source-0", "source-1")


def _valid_state_probability() -> ProbabilityMeasure:
    return ProbabilityMeasure(STATE_LABELS, (1.0, 0.0), NUMERICS)


def _valid_eta() -> np.ndarray:
    return np.array(
        [
            [[0.3, 0.2], [0.1, 0.4]],
            [[0.0, 0.0], [0.0, 0.0]],
        ]
    )


def test_from_alpha_beta_forms_literal_event_law_and_defensively_owns_inputs():
    state_masses = np.array([1.0, 0.0])
    alpha = np.array([[0.5, 0.5], [0.0, 0.0]])
    beta = np.array(
        [
            [[0.6, 0.4], [0.2, 0.8]],
            [[0.0, 0.0], [0.0, 0.0]],
        ]
    )
    state_probability = ProbabilityMeasure(STATE_LABELS, state_masses, NUMERICS)

    law = StateConditionedAttentionLaw.from_alpha_beta(
        state_probability,
        RECEIVER_LABELS,
        SOURCE_LABELS,
        alpha,
        beta,
    )

    assert_allclose(law.eta_given_state[0], [[0.3, 0.2], [0.1, 0.4]])
    assert_array_equal(law.eta_given_state[1], np.zeros((2, 2)))
    assert law.receiver_labels == RECEIVER_LABELS
    assert law.source_labels == SOURCE_LABELS
    assert not law.eta_given_state.flags.writeable

    state_masses[:] = [0.0, 1.0]
    alpha[:] = 0.0
    beta[:] = 0.0

    assert_array_equal(law.state_probability.masses, [1.0, 0.0])
    assert_allclose(law.eta_given_state[0], [[0.3, 0.2], [0.1, 0.4]])


def test_disintegrate_recovers_active_conditionals_and_masks_null_representatives():
    eta = _valid_eta()
    law = StateConditionedAttentionLaw(
        ProbabilityMeasure(STATE_LABELS, (1.0, 0.0), NUMERICS),
        RECEIVER_LABELS,
        SOURCE_LABELS,
        eta,
    )

    result = law.disintegrate()

    assert_allclose(result.alpha_given_state, [[0.5, 0.5], [0.0, 0.0]])
    assert_allclose(
        result.beta_given_state[0],
        [[0.6, 0.4], [0.2, 0.8]],
    )
    assert_array_equal(result.positive_state_mask, [True, False])
    assert_array_equal(
        result.positive_receiver_mask,
        [[True, True], [False, False]],
    )
    assert_array_equal(result.beta_given_state[1], np.zeros((2, 2)))
    for values in (
        result.alpha_given_state,
        result.beta_given_state,
        result.positive_state_mask,
        result.positive_receiver_mask,
    ):
        assert not values.flags.writeable

    eta[:] = 0.0
    assert_allclose(law.eta_given_state[0], [[0.3, 0.2], [0.1, 0.4]])


def test_law_requires_a_probability_measure_at_runtime():
    with pytest.raises(TypeError, match="state_probability must be a ProbabilityMeasure"):
        StateConditionedAttentionLaw(  # type: ignore[arg-type]
            object(), RECEIVER_LABELS, SOURCE_LABELS, _valid_eta()
        )


@pytest.mark.parametrize(
    ("receiver_labels", "source_labels", "message"),
    [
        ((), SOURCE_LABELS, "receiver_labels must be nonempty"),
        (RECEIVER_LABELS, (), "source_labels must be nonempty"),
        (("receiver", "receiver"), SOURCE_LABELS, "receiver_labels must be unique"),
        (RECEIVER_LABELS, ("source", "source"), "source_labels must be unique"),
        (("", "receiver"), SOURCE_LABELS, "receiver_labels entries must be nonempty"),
    ],
)
def test_law_rejects_empty_or_duplicate_labels(
    receiver_labels: tuple[str, ...],
    source_labels: tuple[str, ...],
    message: str,
):
    with pytest.raises(ValueError, match=message):
        StateConditionedAttentionLaw(
            _valid_state_probability(),
            receiver_labels,
            source_labels,
            _valid_eta(),
        )


def test_law_rejects_nonstring_labels():
    with pytest.raises(TypeError, match="source_labels entries must be strings"):
        StateConditionedAttentionLaw(
            _valid_state_probability(),
            RECEIVER_LABELS,
            ("source", 1),  # type: ignore[arg-type]
            _valid_eta(),
        )


@pytest.mark.parametrize(
    "eta",
    [
        np.zeros((2, 2)),
        np.zeros((2, 2, 2, 1)),
        np.zeros((1, 2, 2)),
        np.zeros((2, 1, 2)),
        np.zeros((2, 2, 1)),
    ],
)
def test_law_rejects_wrong_eta_dimensions_or_axis_lengths(eta: np.ndarray):
    with pytest.raises(ValueError, match="eta_given_state shape"):
        StateConditionedAttentionLaw(
            _valid_state_probability(), RECEIVER_LABELS, SOURCE_LABELS, eta
        )


@pytest.mark.parametrize("entry", [np.nan, np.inf, -0.1])
def test_law_rejects_nonfinite_or_negative_eta_entries(entry: float):
    eta = _valid_eta()
    eta[0, 0, 0] = entry

    with pytest.raises(ValueError, match="eta_given_state must be finite nonnegative"):
        StateConditionedAttentionLaw(
            _valid_state_probability(), RECEIVER_LABELS, SOURCE_LABELS, eta
        )


def test_law_rejects_nonunit_active_state_event_mass():
    eta = _valid_eta()
    eta[0] *= 0.9

    with pytest.raises(ValueError, match="positive-state eta mass must equal one"):
        StateConditionedAttentionLaw(
            _valid_state_probability(), RECEIVER_LABELS, SOURCE_LABELS, eta
        )


def test_law_rejects_nonzero_null_state_representative():
    eta = _valid_eta()
    eta[1, 0, 0] = 0.1

    with pytest.raises(ValueError, match="zero-probability-state eta must be zero"):
        StateConditionedAttentionLaw(
            _valid_state_probability(), RECEIVER_LABELS, SOURCE_LABELS, eta
        )


@pytest.mark.parametrize(
    ("alpha", "beta", "message"),
    [
        (
            np.zeros((2, 2, 1)),
            np.zeros((2, 2, 2)),
            "alpha_given_state shape",
        ),
        (
            np.zeros((2, 2)),
            np.zeros((2, 2)),
            "beta_given_state shape",
        ),
        (
            np.zeros((1, 2)),
            np.zeros((2, 2, 2)),
            "alpha_given_state shape",
        ),
        (
            np.zeros((2, 2)),
            np.zeros((1, 2, 2)),
            "beta_given_state shape",
        ),
    ],
)
def test_from_alpha_beta_rejects_wrong_dimensions_or_state_count(
    alpha: np.ndarray,
    beta: np.ndarray,
    message: str,
):
    with pytest.raises(ValueError, match=message):
        StateConditionedAttentionLaw.from_alpha_beta(
            _valid_state_probability(),
            RECEIVER_LABELS,
            SOURCE_LABELS,
            alpha,
            beta,
        )


@pytest.mark.parametrize("entry", [np.nan, np.inf, -0.1])
def test_from_alpha_beta_rejects_nonfinite_or_negative_entries(entry: float):
    alpha = np.array([[0.5, 0.5], [0.0, 0.0]])
    beta = np.array(
        [
            [[0.6, 0.4], [0.2, 0.8]],
            [[0.0, 0.0], [0.0, 0.0]],
        ]
    )
    alpha[0, 0] = entry

    with pytest.raises(ValueError, match="alpha_given_state must be finite nonnegative"):
        StateConditionedAttentionLaw.from_alpha_beta(
            _valid_state_probability(),
            RECEIVER_LABELS,
            SOURCE_LABELS,
            alpha,
            beta,
        )

    alpha = np.array([[0.5, 0.5], [0.0, 0.0]])
    beta[0, 0, 0] = entry
    with pytest.raises(ValueError, match="beta_given_state must be finite nonnegative"):
        StateConditionedAttentionLaw.from_alpha_beta(
            _valid_state_probability(),
            RECEIVER_LABELS,
            SOURCE_LABELS,
            alpha,
            beta,
        )


def test_from_alpha_beta_rejects_nonunit_active_alpha():
    alpha = np.array([[0.4, 0.5], [0.0, 0.0]])
    beta = np.array(
        [
            [[0.6, 0.4], [0.2, 0.8]],
            [[0.0, 0.0], [0.0, 0.0]],
        ]
    )

    with pytest.raises(ValueError, match="positive-state alpha mass must equal one"):
        StateConditionedAttentionLaw.from_alpha_beta(
            _valid_state_probability(),
            RECEIVER_LABELS,
            SOURCE_LABELS,
            alpha,
            beta,
        )


def test_from_alpha_beta_rejects_nonunit_active_beta_row():
    alpha = np.array([[0.5, 0.5], [0.0, 0.0]])
    beta = np.array(
        [
            [[0.6, 0.3], [0.2, 0.8]],
            [[0.0, 0.0], [0.0, 0.0]],
        ]
    )

    with pytest.raises(ValueError, match="active beta rows must sum to one"):
        StateConditionedAttentionLaw.from_alpha_beta(
            _valid_state_probability(),
            RECEIVER_LABELS,
            SOURCE_LABELS,
            alpha,
            beta,
        )


def test_from_alpha_beta_rejects_nonzero_null_state_alpha_representative():
    alpha = np.array([[0.5, 0.5], [1.0, 0.0]])
    beta = np.array(
        [
            [[0.6, 0.4], [0.2, 0.8]],
            [[1.0, 0.0], [0.0, 0.0]],
        ]
    )

    with pytest.raises(ValueError, match="zero-probability-state alpha must be zero"):
        StateConditionedAttentionLaw.from_alpha_beta(
            _valid_state_probability(),
            RECEIVER_LABELS,
            SOURCE_LABELS,
            alpha,
            beta,
        )


def test_from_alpha_beta_rejects_nonzero_inactive_representatives():
    alpha = np.array([[1.0, 0.0], [0.0, 0.0]])
    beta = np.array(
        [
            [[0.6, 0.4], [1.0, 0.0]],
            [[1.0, 0.0], [0.0, 1.0]],
        ]
    )

    with pytest.raises(ValueError, match="inactive beta rows must be zero"):
        StateConditionedAttentionLaw.from_alpha_beta(
            _valid_state_probability(),
            RECEIVER_LABELS,
            SOURCE_LABELS,
            alpha,
            beta,
        )


@pytest.mark.parametrize(
    ("mismatched_kernel", "message"),
    [
        ("state", "state_channel numerics must match law numerics"),
        ("receiver", "receiver_partition numerics must match law numerics"),
        ("source", "source_partition numerics must match law numerics"),
    ],
)
def test_pushforward_rejects_kernel_numerical_policy_mismatch(
    mismatched_kernel: str, message: str
):
    law = StateConditionedAttentionLaw(
        _valid_state_probability(), RECEIVER_LABELS, SOURCE_LABELS, _valid_eta()
    )
    other_numerics = NumericsConfig(dtype="float64", atol=1e-9, rtol=1e-10)
    state_channel = MarkovKernel(
        STATE_LABELS,
        ("coarse",),
        ((1.0,), (1.0,)),
        other_numerics if mismatched_kernel == "state" else NUMERICS,
    )
    receiver_partition = MarkovKernel(
        RECEIVER_LABELS,
        ("receiver",),
        ((1.0,), (1.0,)),
        other_numerics if mismatched_kernel == "receiver" else NUMERICS,
    )
    source_partition = MarkovKernel(
        SOURCE_LABELS,
        ("source",),
        ((1.0,), (1.0,)),
        other_numerics if mismatched_kernel == "source" else NUMERICS,
    )

    with pytest.raises(ValueError, match=message):
        law.pushforward(state_channel, receiver_partition, source_partition)


def _exact_three_state_law() -> StateConditionedAttentionLaw:
    eta0 = np.array(
        [
            [1 / 40, 1 / 80, 1 / 100, 1 / 400],
            [1 / 16, 1 / 20, 1 / 40, 9 / 80],
            [1 / 200, 1 / 200, 1 / 200, 17 / 200],
            [3 / 25, 9 / 50, 3 / 50, 6 / 25],
        ]
    )
    eta1 = np.array(
        [
            [6 / 25, 3 / 25, 9 / 50, 3 / 50],
            [1 / 400, 1 / 40, 1 / 80, 1 / 100],
            [9 / 80, 1 / 16, 1 / 20, 1 / 40],
            [17 / 200, 1 / 200, 1 / 200, 1 / 200],
        ]
    )
    eta2 = np.array(
        [
            [1 / 40, 1 / 16, 1 / 200, 3 / 25],
            [1 / 80, 1 / 20, 1 / 200, 9 / 50],
            [1 / 100, 1 / 40, 1 / 200, 3 / 50],
            [1 / 400, 9 / 80, 17 / 200, 6 / 25],
        ]
    )
    return StateConditionedAttentionLaw(
        ProbabilityMeasure(("y0", "y1", "y2"), (1 / 2, 1 / 3, 1 / 6), NUMERICS),
        ("n0", "n1", "n2", "n3"),
        ("n0", "n1", "n2", "n3"),
        np.array([eta0, eta1, eta2]),
    )


def _attention_partitions() -> tuple[
    MarkovKernel,
    MarkovKernel,
    MarkovKernel,
    MarkovKernel,
    MarkovKernel,
    MarkovKernel,
]:
    fine = ("n0", "n1", "n2", "n3")
    middle = ("A", "B", "C")
    coarse = ("U", "V")
    fine_to_middle = (
        (1.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
    )
    middle_to_coarse = (
        (1.0, 0.0),
        (1.0, 0.0),
        (0.0, 1.0),
    )
    fine_to_coarse = (
        (1.0, 0.0),
        (1.0, 0.0),
        (1.0, 0.0),
        (0.0, 1.0),
    )
    return (
        MarkovKernel(fine, middle, fine_to_middle, NUMERICS),
        MarkovKernel(fine, middle, fine_to_middle, NUMERICS),
        MarkovKernel(middle, coarse, middle_to_coarse, NUMERICS),
        MarkovKernel(middle, coarse, middle_to_coarse, NUMERICS),
        MarkovKernel(fine, coarse, fine_to_coarse, NUMERICS),
        MarkovKernel(fine, coarse, fine_to_coarse, NUMERICS),
    )


def test_node_pushforward_matches_every_literal_middle_and_coarse_base_state_value():
    law = _exact_three_state_law()
    receiver_01, source_01, receiver_12, source_12, receiver_02, source_02 = (
        _attention_partitions()
    )
    identity_state = MarkovKernel(
        ("y0", "y1", "y2"),
        ("y0", "y1", "y2"),
        np.eye(3),
        NUMERICS,
    )
    expected_middle_eta_y0 = np.array(
        [
            [3 / 20, 7 / 200, 23 / 200],
            [1 / 100, 1 / 200, 17 / 200],
            [3 / 10, 3 / 50, 6 / 25],
        ]
    )
    expected_middle_alpha_y0 = np.array([3 / 10, 1 / 10, 3 / 5])
    expected_middle_beta_y0 = np.array(
        [
            [1 / 2, 7 / 60, 23 / 60],
            [1 / 10, 1 / 20, 17 / 20],
            [1 / 2, 1 / 10, 2 / 5],
        ]
    )
    expected_coarse_eta_y0 = np.array([[1 / 5, 1 / 5], [9 / 25, 6 / 25]])
    expected_coarse_alpha_y0 = np.array([2 / 5, 3 / 5])
    expected_coarse_beta_y0 = np.array([[1 / 2, 1 / 2], [3 / 5, 2 / 5]])

    middle_law = law.pushforward(identity_state, receiver_01, source_01)
    staged_law = middle_law.pushforward(identity_state, receiver_12, source_12)
    direct_law = law.pushforward(identity_state, receiver_02, source_02)
    middle_disintegration = middle_law.disintegrate()
    direct_disintegration = direct_law.disintegrate()

    assert_allclose(middle_law.eta_given_state[0], expected_middle_eta_y0)
    assert_allclose(
        middle_disintegration.alpha_given_state[0], expected_middle_alpha_y0
    )
    assert_allclose(
        middle_disintegration.beta_given_state[0], expected_middle_beta_y0
    )
    assert_allclose(staged_law.eta_given_state[0], expected_coarse_eta_y0)
    assert_allclose(direct_law.eta_given_state[0], expected_coarse_eta_y0)
    assert_allclose(
        direct_disintegration.alpha_given_state[0], expected_coarse_alpha_y0
    )
    assert_allclose(
        direct_disintegration.beta_given_state[0], expected_coarse_beta_y0
    )


def test_state_and_node_pushforward_matches_literal_bridges_and_final_laws():
    law = _exact_three_state_law()
    receiver_01, source_01, receiver_12, source_12, receiver_02, source_02 = (
        _attention_partitions()
    )
    state_01 = MarkovKernel(
        ("y0", "y1", "y2"),
        ("z0", "z1"),
        ((1.0, 0.0), (1.0, 0.0), (0.0, 1.0)),
        NUMERICS,
    )
    state_12 = MarkovKernel(
        ("z0", "z1"),
        ("w0", "w1"),
        ((3 / 4, 1 / 4), (1 / 4, 3 / 4)),
        NUMERICS,
    )
    state_02 = MarkovKernel(
        ("y0", "y1", "y2"),
        ("w0", "w1"),
        ((3 / 4, 1 / 4), (3 / 4, 1 / 4), (1 / 4, 3 / 4)),
        NUMERICS,
    )
    expected_middle_probability = np.array([5 / 6, 1 / 6])
    expected_final_probability = np.array([2 / 3, 1 / 3])
    expected_direct_bridge = np.array(
        [[9 / 16, 3 / 8, 1 / 16], [3 / 8, 1 / 4, 3 / 8]]
    )
    direct_bridge = np.array(
        [
            [(1 / 2) * (3 / 4) / (2 / 3), (1 / 3) * (3 / 4) / (2 / 3), (1 / 6) * (1 / 4) / (2 / 3)],
            [(1 / 2) * (1 / 4) / (1 / 3), (1 / 3) * (1 / 4) / (1 / 3), (1 / 6) * (3 / 4) / (1 / 3)],
        ]
    )
    fine_given_middle = np.array([[3 / 5, 2 / 5, 0.0], [0.0, 0.0, 1.0]])
    middle_given_final = np.array([[15 / 16, 1 / 16], [5 / 8, 3 / 8]])
    staged_bridge = middle_given_final @ fine_given_middle
    expected_w0 = np.array(
        [[683 / 1600, 273 / 1600], [401 / 1600, 243 / 1600]]
    )
    expected_w1 = np.array(
        [[281 / 800, 187 / 800], [187 / 800, 145 / 800]]
    )
    expected_final_alpha = np.array(
        [[239 / 400, 161 / 400], [117 / 200, 83 / 200]]
    )
    expected_final_beta = np.array(
        [
            [[683 / 956, 273 / 956], [401 / 644, 243 / 644]],
            [[281 / 468, 187 / 468], [187 / 332, 145 / 332]],
        ]
    )

    middle_law = law.pushforward(state_01, receiver_01, source_01)
    staged_law = middle_law.pushforward(state_12, receiver_12, source_12)
    direct_law = law.pushforward(state_02, receiver_02, source_02)
    direct_disintegration = direct_law.disintegrate()

    assert_allclose(middle_law.state_probability.masses, expected_middle_probability)
    assert_allclose(direct_bridge, expected_direct_bridge)
    assert_allclose(staged_bridge, expected_direct_bridge)
    assert_allclose(staged_law.state_probability.masses, expected_final_probability)
    assert_allclose(direct_law.state_probability.masses, expected_final_probability)
    assert_allclose(staged_law.eta_given_state[0], expected_w0)
    assert_allclose(staged_law.eta_given_state[1], expected_w1)
    assert_allclose(direct_law.eta_given_state[0], expected_w0)
    assert_allclose(direct_law.eta_given_state[1], expected_w1)
    assert_allclose(direct_disintegration.alpha_given_state, expected_final_alpha)
    assert_allclose(direct_disintegration.beta_given_state, expected_final_beta)


def test_pushforward_preserves_zero_representatives_at_null_coarse_states():
    law = StateConditionedAttentionLaw(
        _valid_state_probability(), RECEIVER_LABELS, SOURCE_LABELS, _valid_eta()
    )
    identity_state = MarkovKernel(STATE_LABELS, STATE_LABELS, np.eye(2), NUMERICS)
    identity_receiver = MarkovKernel(
        RECEIVER_LABELS, RECEIVER_LABELS, np.eye(2), NUMERICS
    )
    identity_source = MarkovKernel(
        SOURCE_LABELS, SOURCE_LABELS, np.eye(2), NUMERICS
    )

    pushed = law.pushforward(identity_state, identity_receiver, identity_source)
    result = pushed.disintegrate()

    assert_array_equal(pushed.state_probability.masses, [1.0, 0.0])
    assert_array_equal(pushed.eta_given_state[1], np.zeros((2, 2)))
    assert_array_equal(result.positive_state_mask, [True, False])
    assert_array_equal(result.positive_receiver_mask[1], [False, False])
    assert_array_equal(result.beta_given_state[1], np.zeros((2, 2)))


@pytest.mark.parametrize("mismatched_partition", ["state", "receiver", "source"])
def test_pushforward_rejects_partition_source_label_mismatch(
    mismatched_partition: str,
):
    law = StateConditionedAttentionLaw(
        _valid_state_probability(), RECEIVER_LABELS, SOURCE_LABELS, _valid_eta()
    )
    state_labels = (
        tuple(reversed(STATE_LABELS))
        if mismatched_partition == "state"
        else STATE_LABELS
    )
    receiver_labels = (
        tuple(reversed(RECEIVER_LABELS))
        if mismatched_partition == "receiver"
        else RECEIVER_LABELS
    )
    source_labels = (
        tuple(reversed(SOURCE_LABELS))
        if mismatched_partition == "source"
        else SOURCE_LABELS
    )
    state_channel = MarkovKernel(state_labels, ("coarse",), ((1.0,), (1.0,)), NUMERICS)
    receiver_partition = MarkovKernel(
        receiver_labels, ("receiver",), ((1.0,), (1.0,)), NUMERICS
    )
    source_partition = MarkovKernel(
        source_labels, ("source",), ((1.0,), (1.0,)), NUMERICS
    )

    with pytest.raises(ValueError, match=f"{mismatched_partition}.*source labels"):
        law.pushforward(state_channel, receiver_partition, source_partition)


def test_compose_kernels_matches_literal_products_and_labels():
    state_01 = MarkovKernel(
        ("y0", "y1", "y2"),
        ("z0", "z1"),
        ((1.0, 0.0), (1.0, 0.0), (0.0, 1.0)),
        NUMERICS,
    )
    state_12 = MarkovKernel(
        ("z0", "z1"),
        ("w0", "w1"),
        ((3 / 4, 1 / 4), (1 / 4, 3 / 4)),
        NUMERICS,
    )
    receiver_01, _, receiver_12, _, _, _ = _attention_partitions()

    composed_state = attention.compose_kernels(state_01, state_12)
    composed_receiver = attention.compose_kernels(receiver_01, receiver_12)

    assert composed_state.source_labels == ("y0", "y1", "y2")
    assert composed_state.target_labels == ("w0", "w1")
    assert_allclose(
        composed_state.matrix,
        [[3 / 4, 1 / 4], [3 / 4, 1 / 4], [1 / 4, 3 / 4]],
    )
    assert composed_receiver.source_labels == ("n0", "n1", "n2", "n3")
    assert composed_receiver.target_labels == ("U", "V")
    assert_array_equal(
        composed_receiver.matrix,
        [[1.0, 0.0], [1.0, 0.0], [1.0, 0.0], [0.0, 1.0]],
    )


def test_compose_kernels_rejects_label_and_numerical_policy_mismatches():
    first = MarkovKernel(("a", "b"), ("x", "y"), np.eye(2), NUMERICS)
    wrong_labels = MarkovKernel(("y", "x"), ("u", "v"), np.eye(2), NUMERICS)
    other_numerics = NumericsConfig(dtype="float64", atol=1e-9, rtol=1e-10)
    wrong_numerics = MarkovKernel(
        ("x", "y"), ("u", "v"), np.eye(2), other_numerics
    )

    with pytest.raises(ValueError, match="first target labels must equal second source labels"):
        attention.compose_kernels(first, wrong_labels)
    with pytest.raises(ValueError, match="kernel numerics must match"):
        attention.compose_kernels(first, wrong_numerics)
