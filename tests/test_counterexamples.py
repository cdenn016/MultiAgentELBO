from __future__ import annotations

from fractions import Fraction
import math

import pytest

from multiagent_elbo.finite.counterexamples import (
    CandidateRecord,
    ExactAction,
    ExactChannel,
    ExactLaw,
    ExtendedRealKL,
    canonical_candidates_json,
    coarsen_marked_event,
    compose_channels,
    enumerate_partitions,
    enumerate_rational_actions,
    enumerate_rational_channels,
    enumerate_rational_laws,
    enumerate_relabelings,
    fixed_channel_score_gap,
    hoeffding_decompose_action,
    kl_divergence,
    minimize_candidates,
    pairwise_interaction_residual,
    parameter_dependent_channel_fixture,
    parameter_dependent_channel_witness,
    project_action,
    relabel_channel,
    relabel_law,
    scale_tolerance,
    diagonal_spd_conditioning,
    retained_projection_invariant,
    validate_full_rank_spd,
)


def test_bounded_exact_enumeration_and_validation_have_literal_oracles():
    laws = tuple(enumerate_rational_laws(max_states=2, max_denominator=2))
    assert laws == (
        ExactLaw((Fraction(0), Fraction(1))),
        ExactLaw((Fraction(1, 2), Fraction(1, 2))),
        ExactLaw((Fraction(1), Fraction(0))),
    )
    assert tuple(enumerate_partitions(3)) == (
        ((0, 1, 2),), ((0, 1), (2,)), ((0, 2), (1,)), ((0,), (1, 2)), ((0,), (1,), (2,))
    )
    channels = tuple(enumerate_rational_channels(2, 2, max_denominator=1))
    assert len(channels) == 4
    with pytest.raises(ValueError, match="sum to one"):
        ExactLaw((Fraction(1, 3), Fraction(1, 3)))
    with pytest.raises(ValueError, match="row"):
        ExactChannel(((Fraction(1), Fraction(0)), (Fraction(1, 2), Fraction(1, 2))), target_states=3)


def test_composition_orientation_and_deep_composition_are_exact():
    first = ExactChannel(((Fraction(1), Fraction(0)), (Fraction(1, 2), Fraction(1, 2))))
    second = ExactChannel(((Fraction(1, 3), Fraction(2, 3)), (Fraction(1), Fraction(0))))
    composed = compose_channels(first, second)
    assert composed.rows == ((Fraction(1, 3), Fraction(2, 3)), (Fraction(2, 3), Fraction(1, 3)))
    assert compose_channels(compose_channels(first, second), first).rows == ((Fraction(2, 3), Fraction(1, 3)), (Fraction(5, 6), Fraction(1, 6)))
    with pytest.raises(ValueError, match="compatible"):
        compose_channels(second, ExactChannel(((Fraction(1),),)))


def test_support_violation_is_structured_extended_real_not_numeric_residual():
    result = kl_divergence(ExactLaw((Fraction(1), Fraction(0))), ExactLaw((Fraction(0), Fraction(1))))
    assert result == ExtendedRealKL(is_infinite=True, value=None, support_violations=(0,))


def test_coherent_relabeling_preserves_kl_but_one_sided_control_is_nonzero():
    q = ExactLaw((Fraction(3, 4), Fraction(1, 4)))
    p = ExactLaw((Fraction(3, 4), Fraction(1, 4)))
    assert kl_divergence(relabel_law(q, (1, 0)), relabel_law(p, (1, 0))).value == kl_divergence(q, p).value
    assert kl_divergence(relabel_law(q, (1, 0)), p).value == pytest.approx(math.log(3) / 2)
    channel = ExactChannel(((Fraction(1), Fraction(0)), (Fraction(1, 2), Fraction(1, 2))))
    assert relabel_channel(channel, (1, 0), (1, 0)).rows == ((Fraction(1, 2), Fraction(1, 2)), (Fraction(0), Fraction(1)))


def test_joint_marked_event_coarsening_differs_from_beta_alone_control():
    source = ExactLaw((Fraction(3, 4), Fraction(1, 4)))
    beta = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    channel = ExactChannel(((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))))
    correct, beta_only = coarsen_marked_event(source, beta, channel)
    assert correct == ((Fraction(3, 4), Fraction(0)), (Fraction(0), Fraction(1, 4)))
    assert beta_only == ((Fraction(1, 2), Fraction(0)), (Fraction(0), Fraction(1, 2)))


def test_pairwise_retention_and_parameter_dependent_channel_controls_are_nonzero():
    action = ExactAction((2, 2, 2), (Fraction(-1), Fraction(1), Fraction(1), Fraction(-1), Fraction(1), Fraction(-1), Fraction(-1), Fraction(1)))
    decomposition = hoeffding_decompose_action(action)
    projection = project_action(decomposition, retained_order=2)
    assert decomposition.components[(0, 1, 2)][(1, 1, 1)] == Fraction(1)
    assert projection.reconstruction.values == action.values
    assert projection.residual == Fraction(1)
    assert pairwise_interaction_residual(decomposition.components, retained_order=2) == Fraction(1)
    fixture = parameter_dependent_channel_fixture(Fraction(1, 4))
    assert fixture.fine_law == (Fraction(1, 2), Fraction(1, 2))
    assert fixture.fine_derivative == (Fraction(0), Fraction(0))
    assert fixture.channel.rows == (
        (Fraction(5, 8), Fraction(3, 8)),
        (Fraction(5, 8), Fraction(3, 8)),
    )
    assert fixture.channel_derivative == (
        (Fraction(1, 2), Fraction(-1, 2)),
        (Fraction(1, 2), Fraction(-1, 2)),
    )
    assert fixture.pushed_law == (Fraction(5, 8), Fraction(3, 8))
    assert fixture.pushed_derivative == (Fraction(1, 2), Fraction(-1, 2))
    assert fixture.fine_score == (Fraction(0), Fraction(0))
    assert fixture.fixed_predicted_coarse_score == (Fraction(0), Fraction(0))
    assert fixture.actual_coarse_score == (Fraction(4, 5), Fraction(-4, 3))
    assert fixture.fisher_weighted_score_gap == Fraction(16, 15)
    assert fixed_channel_score_gap(Fraction(1, 4)) == Fraction(16, 15)
    witness = parameter_dependent_channel_witness(Fraction(1, 4))
    assert witness.observed_residual == "16/15"
    assert witness.inside_declared_domain is False
    assert witness.assumptions_satisfied is False
    assert witness.classification == "assumption_boundary"
    assert witness.smallest_witness["channel_derivative"] == fixture.channel_derivative
    with pytest.raises(ValueError, match="-1 < theta < 1"):
        parameter_dependent_channel_fixture(Fraction(1))


def test_bounded_action_and_relabeling_enumerators_have_literal_outputs():
    assert tuple(enumerate_relabelings(3)) == ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0))
    actions = tuple(enumerate_rational_actions((2,), max_denominator=1, value_bound=1))
    assert [action.values for action in actions] == [
        (Fraction(-1), Fraction(-1)), (Fraction(-1), Fraction(0)), (Fraction(-1), Fraction(1)),
        (Fraction(0), Fraction(-1)), (Fraction(0), Fraction(0)), (Fraction(0), Fraction(1)),
        (Fraction(1), Fraction(-1)), (Fraction(1), Fraction(0)), (Fraction(1), Fraction(1)),
    ]


def test_retained_projection_metamorphic_invariance_has_pass_and_fail_controls():
    action = ExactAction((2, 2, 2), (Fraction(-1), Fraction(1), Fraction(1), Fraction(-1), Fraction(1), Fraction(-1), Fraction(-1), Fraction(1)))
    transformed = action.relabel(((1, 0), (0, 1), (0, 1)))
    assert retained_projection_invariant(action, transformed, ((1, 0), (0, 1), (0, 1)), 2)
    assert not retained_projection_invariant(action, action, ((1, 0), (0, 1), (0, 1)), 2)


def test_candidate_minimization_and_canonical_serialization_are_order_independent():
    records = (
        CandidateRecord("b", False, False, {"states": 3}, "exact", "1/2", "assumption_boundary", "ESTABLISHED", "EVIDENCE_VERIFIED", "STANDARD"),
        CandidateRecord("a", True, True, {"states": 2}, "exact", "0", "no_counterexample", "HYPOTHESIS", "INCONCLUSIVE", "PROJECT_NOVEL"),
        CandidateRecord("b", False, False, {"states": 2}, "exact", "1/3", "assumption_boundary", "ESTABLISHED", "EVIDENCE_VERIFIED", "STANDARD"),
    )
    minimized = minimize_candidates(reversed(records))
    assert [record.claim_id for record in minimized] == ["a", "b"]
    assert minimized[1].smallest_witness == {"states": 2}
    assert canonical_candidates_json(records) == canonical_candidates_json(tuple(reversed(records)))


def test_candidate_witnesses_are_deeply_immutable_and_fraction_serializable():
    record = CandidateRecord("a", True, True, {"states": 2, "nested": [Fraction(1, 3)]}, "exact", "0", "no_counterexample", "HYPOTHESIS", "INCONCLUSIVE", "PROJECT_NOVEL")
    with pytest.raises(TypeError):
        record.smallest_witness["states"] = 3
    assert record.smallest_witness["nested"] == (Fraction(1, 3),)
    assert '"1/3"' in canonical_candidates_json((record,))
    choices = (
        CandidateRecord("size", True, True, {"states": 10}, "exact", "0", "no_counterexample", "HYPOTHESIS", "INCONCLUSIVE", "PROJECT_NOVEL"),
        CandidateRecord("size", True, True, {"states": 2}, "exact", "0", "no_counterexample", "HYPOTHESIS", "INCONCLUSIVE", "PROJECT_NOVEL"),
    )
    assert minimize_candidates(choices)[0].smallest_witness["states"] == 2


def test_candidate_minimizer_uses_nested_fraction_denominator_complexity():
    lexical_first = CandidateRecord(
        "denominator",
        True,
        True,
        {"states": 2, "nested": {"sequence": [Fraction(1, 10)]}},
        "exact",
        "0",
        "catalog",
        "ESTABLISHED",
        "EVIDENCE_VERIFIED",
        "STANDARD",
    )
    structurally_simpler = CandidateRecord(
        "denominator",
        True,
        True,
        {
            "states": 2,
            "nested": {"sequence": [Fraction(1, 2)]},
        },
        "exact",
        "0",
        "catalog",
        "ESTABLISHED",
        "EVIDENCE_VERIFIED",
        "STANDARD",
    )

    minimized = minimize_candidates((lexical_first, structurally_simpler))

    assert minimized == (structurally_simpler,)
    valid_metadata = CandidateRecord(
        "metadata",
        True,
        True,
        {"states": 2, "denominator": 2, "nested": [Fraction(1, 2)]},
        "exact",
        "0",
        "catalog",
        "ESTABLISHED",
        "EVIDENCE_VERIFIED",
        "STANDARD",
    )
    assert minimize_candidates((valid_metadata,)) == (valid_metadata,)
    invalid_metadata = CandidateRecord(
        "denominator",
        True,
        True,
        {"states": 2, "denominator": 3, "nested": [Fraction(1, 2)]},
        "exact",
        "0",
        "catalog",
        "ESTABLISHED",
        "EVIDENCE_VERIFIED",
        "STANDARD",
    )
    with pytest.raises(ValueError, match="denominator metadata"):
        minimize_candidates((invalid_metadata,))


def test_outside_domain_candidate_cannot_be_a_theorem_refutation():
    with pytest.raises(ValueError, match="assumption_boundary"):
        CandidateRecord("bad", False, False, {}, "exact", "1", "theorem_refutation", "ESTABLISHED", "REFUTED", "STANDARD")


def test_near_singular_spd_is_rejected_before_computation():
    assert validate_full_rank_spd(((Fraction(2), Fraction(0)), (Fraction(0), Fraction(3)))) == 2
    with pytest.raises(ValueError, match="positive definite"):
        validate_full_rank_spd(((Fraction(1), Fraction(1)), (Fraction(1), Fraction(1))))
    with pytest.raises(ValueError, match="near-singular"):
        validate_full_rank_spd(((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1, 10**100))))


def test_tolerance_scaling_and_diagonal_conditioning_stress_are_exact():
    assert scale_tolerance(Fraction(1, 1000), 8) == Fraction(1, 125)
    assert diagonal_spd_conditioning((Fraction(1, 16), Fraction(4))) == Fraction(64)
