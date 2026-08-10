from __future__ import annotations

from fractions import Fraction
import math

import pytest

from multiagent_elbo.finite.counterexamples import (
    CandidateRecord,
    ExactChannel,
    ExactLaw,
    ExtendedRealKL,
    canonical_candidates_json,
    coarsen_marked_event,
    compose_channels,
    enumerate_partitions,
    enumerate_rational_channels,
    enumerate_rational_laws,
    fixed_channel_score_gap,
    kl_divergence,
    minimize_candidates,
    pairwise_interaction_residual,
    relabel_channel,
    relabel_law,
    scale_tolerance,
    diagonal_spd_conditioning,
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
    channel = ExactChannel(((Fraction(1),), (Fraction(1),)))
    correct, beta_only = coarsen_marked_event(source, beta, channel)
    assert correct == (Fraction(3, 4), Fraction(1, 4))
    assert beta_only == (Fraction(1, 2), Fraction(1, 2))


def test_pairwise_retention_and_parameter_dependent_channel_controls_are_nonzero():
    action = {(0, 1, 2): Fraction(1)}
    assert pairwise_interaction_residual(action, retained_order=2) == Fraction(1)
    assert fixed_channel_score_gap(Fraction(1, 3)) == Fraction(2, 9)


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


def test_near_singular_spd_is_rejected_before_computation():
    assert validate_full_rank_spd(((Fraction(2), Fraction(0)), (Fraction(0), Fraction(3)))) == 2
    with pytest.raises(ValueError, match="positive definite"):
        validate_full_rank_spd(((Fraction(1), Fraction(1)), (Fraction(1), Fraction(1))))


def test_tolerance_scaling_and_diagonal_conditioning_stress_are_exact():
    assert scale_tolerance(Fraction(1, 1000), 8) == Fraction(1, 125)
    assert diagonal_spd_conditioning((Fraction(1, 16), Fraction(4))) == Fraction(64)
