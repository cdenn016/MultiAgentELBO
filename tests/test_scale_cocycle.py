from __future__ import annotations

from fractions import Fraction
import math

import pytest

from multiagent_elbo.finite.scale_cocycle import (
    ExactLinearIsomorphism,
    ExactMarkovChannel,
    ExactTypedMorphism,
    anchored_mobius_decompose,
    base_fisher_cocycle_residual_forms,
    conditional_log_laplace_action,
    identified_linear_step,
    ordered_derivative_cocycle,
    posterior_bridge,
    projection_intertwining_residual,
    retained_beta_diagnostics,
)


F = Fraction


def test_exact_channels_compose_right_acting_and_push_laws_by_a_literal_oracle():
    first = ExactMarkovChannel(
        ("x0", "x1"),
        ("z0", "z1"),
        ((F(3, 4), F(1, 4)), (F(1, 3), F(2, 3))),
    )
    second = ExactMarkovChannel(
        ("z0", "z1"),
        ("w0", "w1"),
        ((F(2, 3), F(1, 3)), (F(1, 5), F(4, 5))),
    )

    direct = first.compose(second)
    law = (F(2, 5), F(3, 5))

    assert direct.matrix == (
        (F(11, 20), F(9, 20)),
        (F(16, 45), F(29, 45)),
    )
    assert direct.pushforward(law) == (F(13, 30), F(17, 30))
    assert second.pushforward(first.pushforward(law)) == direct.pushforward(law)
    assert first.recognition_independent is True


def test_channels_reject_non_normalization_and_type_mismatch():
    with pytest.raises(ValueError, match="sum to one"):
        ExactMarkovChannel(("x",), ("z0", "z1"), ((F(1, 2), F(1, 3)),))

    first = ExactMarkovChannel(("x",), ("z",), ((F(1),),))
    second = ExactMarkovChannel(("other",), ("w",), ((F(1),),))
    with pytest.raises(ValueError, match="labels"):
        first.compose(second)


def test_conditional_log_laplace_action_and_posterior_bridge_match_literal_mass_oracles():
    channel = ExactMarkovChannel(
        ("x0", "x1"),
        ("z0", "z1"),
        ((F(3, 4), F(1, 4)), (F(1, 3), F(2, 3))),
    )
    reference = (F(2, 5), F(3, 5))
    evidence = (F(1, 10), F(3, 10))

    action = conditional_log_laplace_action(reference, evidence, channel)
    bridge = posterior_bridge((F(1, 4), F(3, 4)), channel)

    assert action.coarse_reference == (F(1, 2), F(1, 2))
    assert action.coarse_evidence == (F(7, 40), F(9, 40))
    assert action.likelihood == (F(7, 20), F(9, 20))
    assert action.action == pytest.approx((-math.log(7 / 20), -math.log(9 / 20)))
    assert bridge.coarse_posterior == (F(7, 16), F(9, 16))
    assert bridge.reverse == (
        (F(3, 7), F(4, 7)),
        (F(1, 9), F(8, 9)),
    )
    for source_index in range(2):
        for target_index in range(2):
            assert bridge.joint[source_index][target_index] == (
                bridge.coarse_posterior[target_index]
                * bridge.reverse[target_index][source_index]
            )


def test_comparison_orientation_and_ordered_derivative_cocycle_are_typed_and_noncommutative():
    source_identification = ExactLinearIsomorphism(
        "native-0", "reference", ((F(2), F(0)), (F(0), F(3)))
    )
    target_identification = ExactLinearIsomorphism(
        "native-1", "reference", ((F(5), F(0)), (F(0), F(7)))
    )
    native_step = ((F(1), F(2)), (F(3), F(4)))

    identified = identified_linear_step(
        source_identification, native_step, target_identification
    )
    first_derivative = ExactTypedMorphism(
        "level-0",
        "level-1",
        "tangent-0",
        "tangent-1",
        ((F(1), F(1)), (F(0), F(1))),
    )
    second_derivative = ExactTypedMorphism(
        "level-1",
        "level-2",
        "tangent-1",
        "tangent-2",
        ((F(1), F(0)), (F(1), F(1))),
    )

    assert identified == ((F(5, 2), F(10, 3)), (F(21, 2), F(28, 3)))
    composite = ordered_derivative_cocycle((first_derivative, second_derivative))
    assert composite.matrix == (
        (F(1), F(1)),
        (F(1), F(2)),
    )
    assert composite.source_level == "level-0"
    assert composite.target_level == "level-2"
    assert composite.source_type == "tangent-0"
    assert composite.target_type == "tangent-2"

    with pytest.raises(ValueError, match="adjacent levels and types"):
        ordered_derivative_cocycle((second_derivative, first_derivative))


def test_retained_beta_has_the_exact_signed_residual_in_three_equivalent_forms():
    identity = ExactLinearIsomorphism(
        "native", "reference", ((F(1), F(0)), (F(0), F(1)))
    )
    exact_step = ((F(1), F(0)), (F(1), F(0)))
    retained = ((F(1), F(0)), (F(0), F(0)))

    result = retained_beta_diagnostics(
        exact_step=exact_step,
        reference_input=(F(2), F(0)),
        source_identification=identity,
        target_identification=identity,
        source_projection=retained,
        target_projection=retained,
        delta_log_scale=F(1),
    )

    assert result.exact_beta == (F(0), F(2))
    assert result.retained_beta == (F(0), F(0))
    assert result.residual_from_difference == (F(0), F(2))
    assert result.residual_from_identified_projection == (F(0), F(2))
    assert result.residual_from_native_transport == (F(0), F(2))


def test_projection_intertwining_and_fisher_residual_controls_preserve_signs():
    identification = ExactLinearIsomorphism(
        "native", "reference", ((F(1), F(1)), (F(0), F(1)))
    )
    native_projection = ((F(1), F(0)), (F(0), F(0)))
    wrongly_held_reference_projection = native_projection

    gap = projection_intertwining_residual(
        identification, native_projection, wrongly_held_reference_projection
    )
    forms = base_fisher_cocycle_residual_forms(
        fisher_defect=((F(2), F(1)), (F(1), F(3))),
        pushed_fine_jet=(F(1), F(2)),
        horizontal_anomaly=(F(2), F(-1)),
    )

    assert gap == F(1)
    assert forms.from_norm_difference == forms.from_coarse_jet_cross_terms
    assert forms.from_pushed_jet_cross_terms == forms.from_norm_difference
    assert forms.from_norm_difference == F(-9)


def test_full_subset_mobius_closure_reconstructs_and_pairwise_truncation_fails():
    action = {
        state: F(state[0] + 2 * state[1] + 3 * state[2] + 5 * math.prod(state))
        for state in (
            (0, 0, 0),
            (0, 0, 1),
            (0, 1, 0),
            (0, 1, 1),
            (1, 0, 0),
            (1, 0, 1),
            (1, 1, 0),
            (1, 1, 1),
        )
    }

    decomposition = anchored_mobius_decompose(action, anchor=(0, 0, 0))

    assert all(decomposition.reconstruct(state) == value for state, value in action.items())
    assert decomposition.component_value((0, 1, 2), (1, 1, 1)) == F(5)
    assert decomposition.maximum_residual(maximum_order=2) == F(5)
