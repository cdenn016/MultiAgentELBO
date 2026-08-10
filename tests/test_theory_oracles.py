from __future__ import annotations

from dataclasses import FrozenInstanceError
from fractions import Fraction
import json
import math
from pathlib import Path

import pytest


def test_parse_fraction_literal_accepts_only_canonical_reduced_strings():
    from multiagent_elbo.finite.theory_oracles import parse_fraction_literal

    assert parse_fraction_literal("0") == Fraction(0)
    assert parse_fraction_literal("-7") == Fraction(-7)
    assert parse_fraction_literal("-3/5") == Fraction(-3, 5)


@pytest.mark.parametrize(
    "literal",
    ["2/4", "0/2", "1/0", "1/-2", "+1/2", "01", " 1/2", "1 /2", 1, True],
)
def test_parse_fraction_literal_rejects_noncanonical_or_wrong_type(literal: object):
    from multiagent_elbo.finite.theory_oracles import parse_fraction_literal

    with pytest.raises((TypeError, ValueError), match="rational literal"):
        parse_fraction_literal(literal)


def test_fraction_containers_are_validated_and_immutable():
    from multiagent_elbo.finite.theory_oracles import (
        FractionMatrix,
        FractionTensor,
        FractionVector,
    )

    vector = FractionVector((Fraction(1, 3), Fraction(2, 3)))
    matrix = FractionMatrix(
        ((Fraction(1), Fraction(0)), (Fraction(1, 4), Fraction(3, 4)))
    )
    tensor = FractionTensor((2, 2), (Fraction(1), Fraction(2), Fraction(3), Fraction(4)))

    assert vector.values == (Fraction(1, 3), Fraction(2, 3))
    assert matrix.shape == (2, 2)
    assert tensor.at((1, 0)) == Fraction(3)
    with pytest.raises(FrozenInstanceError):
        vector.values = (Fraction(1),)  # type: ignore[misc]
    with pytest.raises(TypeError, match="tuple"):
        FractionVector([Fraction(1)])  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="Fraction"):
        FractionMatrix(((Fraction(1), 0),))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="rectangular"):
        FractionMatrix(((Fraction(1),), (Fraction(1), Fraction(2))))
    with pytest.raises(ValueError, match="shape"):
        FractionTensor((2, 2), (Fraction(1),))


def test_fixture_evidence_elbo_has_structurally_zero_exact_residual():
    from multiagent_elbo.finite.theory_oracles import (
        FractionVector,
        exact_evidence_elbo,
    )

    evidence = FractionVector(
        tuple(
            Fraction(numerator, 128)
            for numerator in (3, 1, 1, 3, 1, 3, 3, 1, 3, 9, 9, 3, 9, 3, 3, 9)
        )
    )
    posterior = FractionVector(
        tuple(
            Fraction(numerator, 64)
            for numerator in (3, 1, 1, 3, 1, 3, 3, 1, 3, 9, 9, 3, 9, 3, 3, 9)
        )
    )
    recognition = FractionVector((Fraction(1, 16),) * 16)

    result = exact_evidence_elbo(evidence, Fraction(1, 2), posterior, recognition)

    assert result.evidence_log.term_pairs == ((Fraction(2), Fraction(-1)),)
    assert result.elbo is not None
    assert result.elbo.term_pairs == (
        (Fraction(2), Fraction(-3)),
        (Fraction(3), Fraction(1)),
    )
    assert result.kl is not None
    assert result.kl.term_pairs == (
        (Fraction(2), Fraction(2)),
        (Fraction(3), Fraction(-1)),
    )
    assert result.residual is not None and result.residual.is_zero
    assert result.branch == "finite"
    assert result.elbo.evaluate_float() == pytest.approx(math.log(3.0 / 8.0))


def test_evidence_elbo_preserves_support_violation_as_extended_branch():
    from multiagent_elbo.finite.theory_oracles import (
        FractionVector,
        exact_evidence_elbo,
    )

    result = exact_evidence_elbo(
        FractionVector((Fraction(1, 2), Fraction(0), Fraction(0), Fraction(0))),
        Fraction(1, 2),
        FractionVector((Fraction(1), Fraction(0), Fraction(0), Fraction(0))),
        FractionVector(
            (Fraction(1, 4), Fraction(1, 4), Fraction(0), Fraction(1, 2))
        ),
    )

    assert result.branch == "recognition_not_absolutely_continuous"
    assert result.elbo == -math.inf
    assert result.kl == math.inf
    assert result.residual is None
    assert result.offending_support_entries == (1, 3)


def test_fixed_channel_fisher_defect_uses_exact_joint_conditional_weights():
    from multiagent_elbo.finite.theory_oracles import (
        FractionMatrix,
        FractionVector,
        exact_fisher_defect,
    )

    result = exact_fisher_defect(
        FractionVector((Fraction(1, 3), Fraction(2, 3))),
        FractionMatrix(
            ((Fraction(1), Fraction(0)), (Fraction(1, 4), Fraction(3, 4)))
        ),
        FractionMatrix(((Fraction(2),), (Fraction(-1),))),
    )

    assert result.joint_weights.rows == (
        (Fraction(1, 3), Fraction(0)),
        (Fraction(1, 6), Fraction(1, 2)),
    )
    assert result.coarse_mass.values == (Fraction(1, 2), Fraction(1, 2))
    assert result.coarse_scores.rows == ((Fraction(1),), (Fraction(-1),))
    assert result.coarse_scores.rows[0][0] != Fraction(1, 2)  # unweighted mutation
    assert result.fine_fisher.rows == ((Fraction(2),),)
    assert result.coarse_fisher.rows == ((Fraction(1),),)
    assert result.defect.rows == ((Fraction(1),),)
    assert result.conditional_covariance.rows == ((Fraction(1),),)
    assert result.defect == result.conditional_covariance


def test_fixed_channel_fisher_defect_rejects_transposed_channel_orientation():
    from multiagent_elbo.finite.theory_oracles import (
        FractionMatrix,
        FractionVector,
        exact_fisher_defect,
    )

    transposed = FractionMatrix(
        ((Fraction(1), Fraction(1, 4)), (Fraction(0), Fraction(3, 4)))
    )

    with pytest.raises(ValueError, match="source-row orientation"):
        exact_fisher_defect(
            FractionVector((Fraction(1, 3), Fraction(2, 3))),
            transposed,
            FractionMatrix(((Fraction(2),), (Fraction(-1),))),
        )


def test_zero_mass_coarse_score_row_is_a_nonsemantic_excluded_version_sentinel():
    from multiagent_elbo.finite.theory_oracles import (
        FractionMatrix,
        FractionVector,
        exact_fisher_defect,
    )

    probability = FractionVector((Fraction(1, 3), Fraction(2, 3)))
    scores = FractionMatrix(((Fraction(2),), (Fraction(-1),)))
    with_zero_mass_target = exact_fisher_defect(
        probability,
        FractionMatrix(
            (
                (Fraction(1), Fraction(0)),
                (Fraction(1), Fraction(0)),
            )
        ),
        scores,
    )
    positive_mass_only = exact_fisher_defect(
        probability,
        FractionMatrix(((Fraction(1),), (Fraction(1),))),
        scores,
    )

    assert with_zero_mass_target.coarse_mass.values == (Fraction(1), Fraction(0))
    assert with_zero_mass_target.coarse_scores.rows == (
        (Fraction(0),),
        (Fraction(0),),
    )
    assert with_zero_mass_target.zero_mass_coarse_score_rows == (1,)
    assert with_zero_mass_target.fine_fisher.rows == ((Fraction(2),),)
    assert with_zero_mass_target.coarse_fisher.rows == ((Fraction(0),),)
    assert with_zero_mass_target.defect.rows == ((Fraction(2),),)
    assert with_zero_mass_target.conditional_covariance.rows == ((Fraction(2),),)
    assert (
        with_zero_mass_target.fine_fisher,
        with_zero_mass_target.coarse_fisher,
        with_zero_mass_target.defect,
        with_zero_mass_target.conditional_covariance,
    ) == (
        positive_mass_only.fine_fisher,
        positive_mass_only.coarse_fisher,
        positive_mass_only.defect,
        positive_mass_only.conditional_covariance,
    )
    assert with_zero_mass_target.assumption_boundary == (
        "finite algebraic identity only; statistical Fisher interpretation requires "
        "a regular DQM family, a parameter-independent normalized channel, and "
        "square-integrable centered score versions; zero rows at zero coarse mass "
        "are nonsemantic version sentinels excluded by every mass-weighted result"
    )


def test_marked_event_pushforward_includes_source_state_mass_before_disintegration():
    from multiagent_elbo.finite.theory_oracles import (
        FractionMatrix,
        FractionTensor,
        FractionVector,
        push_marked_event_law,
    )

    identity = FractionMatrix(((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))))
    result = push_marked_event_law(
        FractionVector((Fraction(1, 4), Fraction(3, 4))),
        FractionTensor(
            (2, 2, 2),
            (
                Fraction(1), Fraction(0), Fraction(0), Fraction(0),
                Fraction(0), Fraction(0), Fraction(0), Fraction(1),
            ),
        ),
        FractionMatrix(
            ((Fraction(1), Fraction(0)), (Fraction(1, 3), Fraction(2, 3)))
        ),
        identity,
        identity,
    )

    assert result.joint.shape == (2, 2, 2)
    assert result.joint.values == (
        Fraction(1, 4), Fraction(0), Fraction(0), Fraction(1, 4),
        Fraction(0), Fraction(0), Fraction(0), Fraction(1, 2),
    )
    assert result.joint.values != (
        Fraction(1), Fraction(0), Fraction(0), Fraction(1, 3),
        Fraction(0), Fraction(0), Fraction(0), Fraction(2, 3),
    )  # mutation omitting p(y)
    assert result.coarse_state_mass.values == (Fraction(1, 2), Fraction(1, 2))
    assert result.conditional_events[0] is not None
    assert result.conditional_events[0].values == (
        Fraction(1, 2), Fraction(0), Fraction(0), Fraction(1, 2)
    )
    assert sum(result.joint.values, Fraction(0)) == 1


def test_marked_event_receiver_aggregation_is_not_beta_only_averaging():
    from multiagent_elbo.finite.theory_oracles import (
        FractionMatrix,
        FractionTensor,
        FractionVector,
        push_marked_event_law,
    )

    result = push_marked_event_law(
        FractionVector((Fraction(1),)),
        FractionTensor(
            (1, 2, 2),
            (Fraction(1, 4), Fraction(0), Fraction(0), Fraction(3, 4)),
        ),
        FractionMatrix(((Fraction(1),),)),
        FractionMatrix(((Fraction(1),), (Fraction(1),))),
        FractionMatrix(((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))),
    )

    assert result.joint.values == (Fraction(1, 4), Fraction(3, 4))
    assert result.conditional_source[0] is not None
    assert result.conditional_source[0][0] is not None
    assert result.conditional_source[0][0].values == (Fraction(1, 4), Fraction(3, 4))
    assert result.conditional_source[0][0].values != (Fraction(1, 2), Fraction(1, 2))


def test_marked_event_direct_and_staged_pushforwards_agree_exactly():
    from multiagent_elbo.finite.theory_oracles import (
        FractionMatrix,
        FractionTensor,
        FractionVector,
        compose_markov_kernels,
        push_marked_event_law,
    )

    first_state = FractionMatrix(
        ((Fraction(3, 4), Fraction(1, 4)), (Fraction(1, 3), Fraction(2, 3)))
    )
    second_state = FractionMatrix(
        ((Fraction(1, 5), Fraction(4, 5)), (Fraction(3, 7), Fraction(4, 7)))
    )
    first_receiver = FractionMatrix(
        ((Fraction(2, 3), Fraction(1, 3)), (Fraction(1, 4), Fraction(3, 4)))
    )
    second_receiver = FractionMatrix(
        ((Fraction(3, 4), Fraction(1, 4)), (Fraction(2, 5), Fraction(3, 5)))
    )
    first_source = FractionMatrix(
        ((Fraction(3, 5), Fraction(2, 5)), (Fraction(1, 6), Fraction(5, 6)))
    )
    second_source = FractionMatrix(
        ((Fraction(1, 3), Fraction(2, 3)), (Fraction(4, 7), Fraction(3, 7)))
    )
    state_mass = FractionVector((Fraction(1, 3), Fraction(2, 3)))
    events = FractionTensor(
        (2, 2, 2),
        (
            Fraction(1), Fraction(0), Fraction(0), Fraction(0),
            Fraction(0), Fraction(0), Fraction(0), Fraction(1),
        ),
    )
    first = push_marked_event_law(
        state_mass, events, first_state, first_receiver, first_source
    )
    intermediate_state_mass = FractionVector((Fraction(17, 36), Fraction(19, 36)))
    staged_events = FractionTensor(
        (2, 2, 2),
        (
            Fraction(59, 255), Fraction(61, 255),
            Fraction(14, 85), Fraction(31, 85),
            Fraction(28, 285), Fraction(62, 285),
            Fraction(13, 95), Fraction(52, 95),
        ),
    )
    assert first.coarse_state_mass == intermediate_state_mass
    assert first.conditional_events == (
        FractionTensor((2, 2), staged_events.values[:4]),
        FractionTensor((2, 2), staged_events.values[4:]),
    )
    staged = push_marked_event_law(
        intermediate_state_mass,
        staged_events,
        second_state,
        second_receiver,
        second_source,
    )
    composed_state = compose_markov_kernels(first_state, second_state)
    assert composed_state.rows == (
        (Fraction(9, 35), Fraction(26, 35)),
        (Fraction(37, 105), Fraction(68, 105)),
    )
    composed_receiver = compose_markov_kernels(first_receiver, second_receiver)
    assert composed_receiver.rows == (
        (Fraction(19, 30), Fraction(11, 30)),
        (Fraction(39, 80), Fraction(41, 80)),
    )
    composed_source = compose_markov_kernels(first_source, second_source)
    assert composed_source.rows == (
        (Fraction(3, 7), Fraction(4, 7)),
        (Fraction(67, 126), Fraction(59, 126)),
    )
    direct = push_marked_event_law(
        state_mass,
        events,
        composed_state,
        composed_receiver,
        composed_source,
    )

    expected_joint = (
        Fraction(44539, 529200), Fraction(8959, 105840),
        Fraction(123023, 1587600), Fraction(23603, 317520),
        Fraction(23699, 132300), Fraction(4979, 26460),
        Fraction(62143, 396900), Fraction(12343, 79380),
    )
    assert direct.coarse_state_mass.values == (Fraction(101, 315), Fraction(214, 315))
    assert direct.joint.values == expected_joint
    assert staged.joint.values == expected_joint
    assert staged == direct

    wrong_order = push_marked_event_law(
        state_mass,
        events,
        compose_markov_kernels(second_state, first_state),
        compose_markov_kernels(second_receiver, first_receiver),
        compose_markov_kernels(second_source, first_source),
    )
    assert wrong_order.coarse_state_mass.values == (
        Fraction(121, 252), Fraction(131, 252)
    )
    assert wrong_order.joint.values != expected_joint


def test_marked_event_disintegration_is_absent_on_zero_coarse_state_mass():
    from multiagent_elbo.finite.theory_oracles import (
        FractionMatrix,
        FractionTensor,
        FractionVector,
        push_marked_event_law,
    )

    result = push_marked_event_law(
        FractionVector((Fraction(1),)),
        FractionTensor((1, 1, 1), (Fraction(1),)),
        FractionMatrix(((Fraction(1), Fraction(0)),)),
        FractionMatrix(((Fraction(1),),)),
        FractionMatrix(((Fraction(1),),)),
    )

    assert result.coarse_state_mass.values == (Fraction(1), Fraction(0))
    assert result.conditional_events[0] is not None
    assert result.conditional_events[1] is None
    assert result.conditional_source[1] is None


def test_full_hoeffding_reconstruction_includes_empty_and_detects_triple_residual():
    from multiagent_elbo.finite.theory_oracles import (
        FractionTensor,
        FractionVector,
        exact_hoeffding_decomposition,
    )

    values = FractionTensor(
        (2, 2, 2),
        tuple(Fraction(value) for value in (-1, 1, 1, -1, 1, -1, -1, 1)),
    )
    uniform = FractionVector((Fraction(1, 2), Fraction(1, 2)))

    result = exact_hoeffding_decomposition(values, (uniform, uniform, uniform), 2)

    assert result.component(()).values == (Fraction(0),) * 8
    for subset in ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2)):
        assert result.component(subset).values == (Fraction(0),) * 8
    assert result.component((0, 1, 2)) == values
    assert result.reconstruction == values
    assert result.reconstruction_residual.values == (Fraction(0),) * 8
    assert result.retained_values.values == (Fraction(0),) * 8
    assert result.retained_residual == values
    assert any(value != 0 for value in result.retained_residual.values)


def test_hoeffding_uses_declared_nonuniform_product_reference_weights():
    from multiagent_elbo.finite.theory_oracles import (
        FractionTensor,
        FractionVector,
        exact_hoeffding_decomposition,
    )

    result = exact_hoeffding_decomposition(
        FractionTensor(
            (2, 2),
            (Fraction(1), Fraction(-1), Fraction(-1), Fraction(1)),
        ),
        (
            FractionVector((Fraction(3, 4), Fraction(1, 4))),
            FractionVector((Fraction(1, 5), Fraction(4, 5))),
        ),
        2,
    )

    assert result.component(()).values == (Fraction(-3, 10),) * 4
    assert result.component((0,)).values == (
        Fraction(-3, 10), Fraction(-3, 10), Fraction(9, 10), Fraction(9, 10)
    )
    assert result.component((1,)).values == (
        Fraction(4, 5), Fraction(-1, 5), Fraction(4, 5), Fraction(-1, 5)
    )
    assert result.component((0, 1)).values == (
        Fraction(4, 5), Fraction(-1, 5), Fraction(-12, 5), Fraction(3, 5)
    )
    assert result.reconstruction.values == (
        Fraction(1), Fraction(-1), Fraction(-1), Fraction(1)
    )


def test_hoeffding_rejects_reference_shape_or_normalization_mismatch():
    from multiagent_elbo.finite.theory_oracles import (
        FractionTensor,
        FractionVector,
        exact_hoeffding_decomposition,
    )

    values = FractionTensor((2, 2), (Fraction(0),) * 4)
    uniform = FractionVector((Fraction(1, 2), Fraction(1, 2)))

    with pytest.raises(ValueError, match="one product reference"):
        exact_hoeffding_decomposition(values, (uniform,), 1)
    with pytest.raises(ValueError, match="sum to one"):
        exact_hoeffding_decomposition(
            values,
            (uniform, FractionVector((Fraction(1, 3), Fraction(1, 3)))),
            1,
        )


def test_fraction_matrix_transpose_multiply_and_elimination_inverse_are_exact():
    from multiagent_elbo.finite.theory_oracles import (
        FractionMatrix,
        exact_matrix_inverse,
        matrix_multiply,
        matrix_transpose,
    )

    matrix = FractionMatrix(
        ((Fraction(2), Fraction(1)), (Fraction(1), Fraction(1)))
    )
    inverse = exact_matrix_inverse(matrix)

    assert matrix_transpose(matrix) == matrix
    assert inverse.rows == (
        (Fraction(1), Fraction(-1)),
        (Fraction(-1), Fraction(2)),
    )
    assert matrix_multiply(matrix, inverse).rows == (
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
    )
    with pytest.raises(ValueError, match="singular"):
        exact_matrix_inverse(
            FractionMatrix(((Fraction(1), Fraction(2)), (Fraction(2), Fraction(4))))
        )


def test_inverse_congruence_and_transformed_prolongator_commute_exactly():
    from multiagent_elbo.finite.theory_oracles import (
        FractionMatrix,
        galerkin_restriction,
        inverse_congruence,
        transform_prolongator,
    )

    precision = FractionMatrix(
        (
            (Fraction(2), Fraction(0), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(3), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(4), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(0), Fraction(5)),
        )
    )
    prolongator = FractionMatrix(
        (
            (Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(1)),
            (Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(1)),
        )
    )
    fine_frame = FractionMatrix(
        (
            (Fraction(2), Fraction(0), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(0), Fraction(3)),
        )
    )
    coarse_frame = FractionMatrix(
        ((Fraction(5), Fraction(0)), (Fraction(0), Fraction(2)))
    )

    transformed_precision = inverse_congruence(precision, fine_frame)
    transformed_prolongator = transform_prolongator(
        prolongator, fine_frame, coarse_frame
    )

    assert transformed_prolongator.rows == (
        (Fraction(2, 5), Fraction(0)),
        (Fraction(0), Fraction(1, 2)),
        (Fraction(1, 5), Fraction(0)),
        (Fraction(0), Fraction(3, 2)),
    )
    coarse = galerkin_restriction(precision, prolongator)
    transformed_coarse = galerkin_restriction(
        transformed_precision, transformed_prolongator
    )
    assert coarse.rows == (
        (Fraction(6), Fraction(0)),
        (Fraction(0), Fraction(8)),
    )
    assert transformed_coarse.rows == (
        (Fraction(6, 25), Fraction(0)),
        (Fraction(0), Fraction(2)),
    )
    assert transformed_coarse == inverse_congruence(coarse, coarse_frame)


def test_fixed_prolongator_is_rejected_without_the_required_intertwiner():
    from multiagent_elbo.finite.theory_oracles import (
        FractionMatrix,
        transform_prolongator,
    )

    prolongator = FractionMatrix(
        (
            (Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(1)),
            (Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(1)),
        )
    )
    fine_frame = FractionMatrix(
        (
            (Fraction(2), Fraction(0), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(0), Fraction(3)),
        )
    )
    coarse_frame = FractionMatrix(
        ((Fraction(5), Fraction(0)), (Fraction(0), Fraction(2)))
    )

    with pytest.raises(ValueError, match="intertwine"):
        transform_prolongator(
            prolongator, fine_frame, coarse_frame, hold_fixed=True
        )


def test_galerkin_restriction_is_not_schur_marginalization():
    from multiagent_elbo.finite.theory_oracles import (
        FractionMatrix,
        galerkin_restriction,
        schur_complement,
    )

    precision = FractionMatrix(
        (
            (Fraction(4), Fraction(1), Fraction(0)),
            (Fraction(1), Fraction(3), Fraction(1)),
            (Fraction(0), Fraction(1), Fraction(2)),
        )
    )
    prolongator = FractionMatrix(
        (
            (Fraction(1), Fraction(0)),
            (Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(1)),
        )
    )

    galerkin = galerkin_restriction(precision, prolongator)
    schur = schur_complement(precision, retained=(0, 2), eliminated=(1,))

    assert galerkin.rows == (
        (Fraction(9), Fraction(1)),
        (Fraction(1), Fraction(2)),
    )
    assert schur.rows == (
        (Fraction(11, 3), Fraction(-1, 3)),
        (Fraction(-1, 3), Fraction(5, 3)),
    )
    assert galerkin != schur


def test_frozen_two_scale_fixture_has_literal_jacobian_and_commuting_square():
    from multiagent_elbo.finite.theory_oracles import load_two_scale_application

    fixture = Path(__file__).parent / "fixtures" / "two_scale_application_v1.json"
    result = load_two_scale_application(fixture)

    assert result.application_id == (
        "30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd"
    )
    assert result.coarse_jacobian.rows == (
        (Fraction(1, 2), Fraction(1, 2), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1, 2), Fraction(1, 2)),
    )
    assert result.left_square == result.coarse_jacobian
    assert result.right_square == result.coarse_jacobian
    assert result.commutes
    assert result.fine_comparison_inverse == result.fine_comparison
    assert result.coarse_comparison_inverse == result.coarse_comparison
    assert result.recognition_right_inverse_state == "NOT_CHECKED"
    assert result.application_theorem_status == "HYPOTHESIS"
    assert result.application_verification_state == "CANDIDATE"
    assert result.application_claim_origin == "APPLICATION_SPECIFIC"


def test_lane_private_nonidentity_comparison_square_and_mismatch_control():
    from multiagent_elbo.finite.theory_oracles import (
        FractionMatrix,
        LANE_PRIVATE_NONIDENTITY_COMMUTING_SQUARE,
        evaluate_commuting_square,
    )

    witness = LANE_PRIVATE_NONIDENTITY_COMMUTING_SQUARE
    assert witness.packet_id == "oracle_aux_nonidentity_commuting_square_v1"
    assert witness.lane_private
    assert not witness.replacement_application_fixture
    assert witness.coarse_map.rows == (
        (Fraction(1, 2), Fraction(1, 2), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1, 2), Fraction(1, 2)),
    )
    assert witness.fine_comparison.rows == (
        (Fraction(2), Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(2), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(3), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0), Fraction(3)),
    )
    assert witness.coarse_comparison.rows == (
        (Fraction(2), Fraction(0)),
        (Fraction(0), Fraction(3)),
    )

    result = evaluate_commuting_square(
        witness.coarse_map,
        witness.fine_comparison,
        witness.coarse_comparison,
    )
    expected = FractionMatrix(
        (
            (Fraction(1), Fraction(1), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(3, 2), Fraction(3, 2)),
        )
    )
    assert result.left == expected
    assert result.right == expected
    assert result.commutes

    mismatch = evaluate_commuting_square(
        witness.coarse_map,
        witness.fine_comparison,
        FractionMatrix(((Fraction(2), Fraction(0)), (Fraction(0), Fraction(4)))),
    )
    assert mismatch.left.rows == (
        (Fraction(1), Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(2), Fraction(2)),
    )
    assert mismatch.right == expected
    assert not mismatch.commutes


def test_fixture_loader_rejects_transposed_channel_orientation_before_hash_check(
    tmp_path: Path,
):
    from multiagent_elbo.finite.theory_oracles import load_two_scale_application

    fixture = Path(__file__).parent / "fixtures" / "two_scale_application_v1.json"
    payload = json.loads(fixture.read_text(encoding="utf-8"))
    rows = payload["channel"]["arrows"][0]["rows"]
    payload["channel"]["arrows"][0]["rows"] = [list(column) for column in zip(*rows)]
    mutated = tmp_path / "transposed.json"
    mutated.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="source-row orientation"):
        load_two_scale_application(mutated)


def test_fixture_loader_rejects_nonreduced_literal_before_hash_check(tmp_path: Path):
    from multiagent_elbo.finite.theory_oracles import load_two_scale_application

    fixture = Path(__file__).parent / "fixtures" / "two_scale_application_v1.json"
    payload = json.loads(fixture.read_text(encoding="utf-8"))
    payload["configuration"]["coarse_map_matrix"][0][0] = "2/4"
    mutated = tmp_path / "nonreduced.json"
    mutated.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="reduced"):
        load_two_scale_application(mutated)


def test_assumption_matrix_splits_algebraic_and_interpretive_premises():
    from multiagent_elbo.finite.theory_oracles import THEOREM_ASSUMPTION_MATRIX

    records = {record.identity_id: record for record in THEOREM_ASSUMPTION_MATRIX}

    assert records["fixed_channel_fisher_defect_algebraic"].premises == (
        "finite normalized source probability law",
        "normalized nonnegative source-row channel",
        "finite centered score array",
        "coarse scores are joint-weighted conditional averages on positive-mass targets",
        "zero-mass coarse-score rows are arbitrary nonsemantic versions excluded by coarse mass",
    )
    assert records["fixed_channel_fisher_statistical_interpretation"].premises == (
        "regular differentiable-in-quadratic-mean statistical family",
        "normalized Markov channel independent of the statistical parameter",
        "square-integrable centered score version",
        "positive-mass conditional disintegration with arbitrary zero-mass versions excluded almost surely",
    )
    assert records["gaussian_schur_complement_algebraic"].premises == (
        "square rational block matrix",
        "retained/eliminated coordinate partition",
        "invertible eliminated block",
    )
    assert records["gaussian_schur_gaussian_marginal_interpretation"].premises == (
        "symmetric positive-definite joint precision",
        "proper nondegenerate Gaussian law",
        "retained/eliminated coordinate partition",
    )


def test_standard_identity_origins_exclude_project_novel_packaging_label():
    from multiagent_elbo.finite.theory_oracles import THEOREM_ASSUMPTION_MATRIX

    records = {record.identity_id: record for record in THEOREM_ASSUMPTION_MATRIX}
    standard_identity_ids = (
        "evidence_elbo",
        "fixed_channel_fisher_defect_algebraic",
        "fixed_channel_fisher_statistical_interpretation",
        "marked_event_associativity",
        "full_hoeffding_mobius",
        "gaussian_inverse_congruence",
        "gaussian_galerkin_restriction",
        "gaussian_schur_complement_algebraic",
        "gaussian_schur_gaussian_marginal_interpretation",
    )

    assert tuple(records[identity_id].claim_origin for identity_id in standard_identity_ids) == (
        "STANDARD",
        "STANDARD",
        "STANDARD",
        "STANDARD",
        "STANDARD",
        "STANDARD",
        "STANDARD",
        "STANDARD",
        "STANDARD",
    )
    assert records["two_scale_literal_commuting_square"].claim_origin == "APPLICATION_SPECIFIC"


def test_theorem_assumption_matrix_is_immutable_complete_and_boundary_preserving():
    from multiagent_elbo.finite.theory_oracles import (
        LANE_PRIVATE_AUXILIARY_PACKETS,
        THEOREM_ASSUMPTION_MATRIX,
    )

    expected_records = (
        (
            "evidence_elbo",
            (
                "positive finite evidence mass",
                "posterior is normalized evidence slice",
                "recognition is a probability law",
            ),
            "Theory/05_elbo.tex:180-190,212-274",
            "ESTABLISHED",
            "CANDIDATE",
            "STANDARD",
            "exact_fraction_derivation_witness",
            "A nonzero canonical formal-log residual or mishandled support violation falsifies the encoding.",
        ),
        (
            "fixed_channel_fisher_defect_algebraic",
            (
                "finite normalized source probability law",
                "normalized nonnegative source-row channel",
                "finite centered score array",
                "coarse scores are joint-weighted conditional averages on positive-mass targets",
                "zero-mass coarse-score rows are arbitrary nonsemantic versions excluded by coarse mass",
            ),
            "Theory/05c_pullback_geometry.tex:1078-1152",
            "ESTABLISHED",
            "CANDIDATE",
            "STANDARD",
            "exact_fraction_derivation_witness",
            "A mismatch between the finite Fisher difference and mass-weighted conditional covariance falsifies the algebraic identity.",
        ),
        (
            "fixed_channel_fisher_statistical_interpretation",
            (
                "regular differentiable-in-quadratic-mean statistical family",
                "normalized Markov channel independent of the statistical parameter",
                "square-integrable centered score version",
                "positive-mass conditional disintegration with arbitrary zero-mass versions excluded almost surely",
            ),
            "Theory/05c_pullback_geometry.tex:1078-1152",
            "ESTABLISHED",
            "CANDIDATE",
            "STANDARD",
            "theory_derivation_boundary",
            "A parameter-dependent channel, non-DQM family, non-L2 score, or semantic use of a zero-mass version invalidates the Fisher interpretation.",
        ),
        (
            "marked_event_associativity",
            (
                "normalized state law",
                "normalized joint marked-event conditional",
                "normalized state, receiver, and source kernels",
            ),
            "Theory/07b_agent_network_rg.tex:1748+",
            "ESTABLISHED",
            "CANDIDATE",
            "STANDARD",
            "exact_fraction_derivation_witness",
            "A direct/staged joint-law mismatch or a conditional formed on zero mass falsifies the encoding.",
        ),
        (
            "full_hoeffding_mobius",
            (
                "finite tensor product state space",
                "declared normalized product reference",
                "complete subset family including empty set",
            ),
            "Theory/07b_agent_network_rg.tex:1182-1250,1468-1507",
            "ESTABLISHED",
            "CANDIDATE",
            "STANDARD",
            "exact_fraction_derivation_witness",
            "A nonzero full reconstruction residual or missing higher-order retained residual falsifies the encoding.",
        ),
        (
            "gaussian_inverse_congruence",
            ("invertible rational frame", "square rational precision"),
            "Theory/09_coarsegraining.tex:50-166",
            "ESTABLISHED",
            "CANDIDATE",
            "STANDARD",
            "exact_fraction_derivation_witness",
            "Failure of G^-T A G^-1 or its transformed coarse square falsifies the encoding.",
        ),
        (
            "gaussian_galerkin_restriction",
            ("declared prolongator", "compatible square precision"),
            "Theory/09_coarsegraining.tex:50-88",
            "ESTABLISHED",
            "CANDIDATE",
            "STANDARD",
            "exact_fraction_derivation_witness",
            "A result different from S^T A S falsifies the encoding.",
        ),
        (
            "gaussian_schur_complement_algebraic",
            (
                "square rational block matrix",
                "retained/eliminated coordinate partition",
                "invertible eliminated block",
            ),
            "Theory/09_coarsegraining.tex:90-166",
            "ESTABLISHED",
            "CANDIDATE",
            "STANDARD",
            "exact_fraction_derivation_witness",
            "A result different from A_RR-A_RE A_EE^-1 A_ER falsifies the encoding.",
        ),
        (
            "gaussian_schur_gaussian_marginal_interpretation",
            (
                "symmetric positive-definite joint precision",
                "proper nondegenerate Gaussian law",
                "retained/eliminated coordinate partition",
            ),
            "Theory/09_coarsegraining.tex:90-166",
            "ESTABLISHED",
            "CANDIDATE",
            "STANDARD",
            "theory_derivation_boundary",
            "A non-SPD precision, improper Gaussian law, or marginal precision different from the Schur complement invalidates the probabilistic interpretation.",
        ),
        (
            "two_scale_literal_commuting_square",
            (
                "frozen application fixture",
                "declared block-average Jacobian",
                "declared comparison isomorphisms",
            ),
            "Theory/SPEC.md:207+",
            "HYPOTHESIS",
            "CANDIDATE",
            "APPLICATION_SPECIFIC",
            "exact_fraction_derivation_witness",
            "A digest mismatch, noninvertible comparison, or I_c C != C I_f falsifies this application check.",
        ),
    )
    actual_records = tuple(
        (
            record.identity_id,
            record.premises,
            record.theory_source,
            record.theorem_status,
            record.verification_state,
            record.claim_origin,
            record.evidence_kind,
            record.falsification_condition,
        )
        for record in THEOREM_ASSUMPTION_MATRIX
    )
    assert actual_records == expected_records
    for record in THEOREM_ASSUMPTION_MATRIX:
        with pytest.raises(FrozenInstanceError):
            record.verification_state = "EVIDENCE_VERIFIED"  # type: ignore[misc]

    expected_packets = (
        (
            "oracle_aux_fisher_v1",
            "unequal conditional-weight Fisher witness",
            (
                ("probability", ("1/3", "2/3")),
                ("channel", ("1", "0", "1/4", "3/4")),
                ("score", ("2", "-1")),
            ),
            True,
            False,
        ),
        (
            "oracle_aux_marked_event_v1",
            "asymmetric two-stage state/receiver/source marked-event witness",
            (
                ("state_mass", ("1/3", "2/3")),
                ("conditional_events", ("1", "0", "0", "0", "0", "0", "0", "1")),
                ("state_kernel_stage_1", ("3/4", "1/4", "1/3", "2/3")),
                ("state_kernel_stage_2", ("1/5", "4/5", "3/7", "4/7")),
                ("receiver_kernel_stage_1", ("2/3", "1/3", "1/4", "3/4")),
                ("receiver_kernel_stage_2", ("3/4", "1/4", "2/5", "3/5")),
                ("source_kernel_stage_1", ("3/5", "2/5", "1/6", "5/6")),
                ("source_kernel_stage_2", ("1/3", "2/3", "4/7", "3/7")),
                ("intermediate_state_mass", ("17/36", "19/36")),
                (
                    "intermediate_events",
                    ("59/255", "61/255", "14/85", "31/85", "28/285", "62/285", "13/95", "52/95"),
                ),
            ),
            True,
            False,
        ),
        (
            "oracle_aux_hoeffding_v1",
            "pure three-spin interaction witness",
            (
                ("action", ("-1", "1", "1", "-1", "1", "-1", "-1", "1")),
                ("axis_0_reference", ("1/2", "1/2")),
                ("axis_1_reference", ("1/2", "1/2")),
                ("axis_2_reference", ("1/2", "1/2")),
                ("retained_order", ("2",)),
            ),
            True,
            False,
        ),
        (
            "oracle_aux_gaussian_v1",
            "exact frame, Galerkin, and Schur witness",
            (
                (
                    "fine_precision",
                    ("2", "0", "0", "0", "0", "3", "0", "0", "0", "0", "4", "0", "0", "0", "0", "5"),
                ),
                ("prolongator", ("1", "0", "0", "1", "1", "0", "0", "1")),
                (
                    "fine_frame",
                    ("2", "0", "0", "0", "0", "1", "0", "0", "0", "0", "1", "0", "0", "0", "0", "3"),
                ),
                ("coarse_frame", ("5", "0", "0", "2")),
                ("schur_precision", ("4", "1", "0", "1", "3", "1", "0", "1", "2")),
                ("schur_retained", ("0", "2")),
                ("schur_eliminated", ("1",)),
            ),
            True,
            False,
        ),
    )
    actual_packets = tuple(
        (
            packet.packet_id,
            packet.purpose,
            packet.literals,
            packet.lane_private,
            packet.replacement_application_fixture,
        )
        for packet in LANE_PRIVATE_AUXILIARY_PACKETS
    )
    assert actual_packets == expected_packets
