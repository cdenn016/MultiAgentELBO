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
        FractionVector((Fraction(1, 2), Fraction(0))),
        Fraction(1, 2),
        FractionVector((Fraction(1), Fraction(0))),
        FractionVector((Fraction(1, 2), Fraction(1, 2))),
    )

    assert result.branch == "recognition_not_absolutely_continuous"
    assert result.elbo is None
    assert result.kl is None
    assert result.residual is None


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

    identity = FractionMatrix(((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))))
    first_state = FractionMatrix(
        ((Fraction(1), Fraction(0)), (Fraction(1, 3), Fraction(2, 3)))
    )
    second_state = FractionMatrix(
        ((Fraction(1, 2), Fraction(1, 2)), (Fraction(0), Fraction(1)))
    )
    collapse = FractionMatrix(((Fraction(1),), (Fraction(1),)))
    state_mass = FractionVector((Fraction(1, 4), Fraction(3, 4)))
    events = FractionTensor(
        (2, 2, 2),
        (
            Fraction(1), Fraction(0), Fraction(0), Fraction(0),
            Fraction(0), Fraction(0), Fraction(0), Fraction(1),
        ),
    )
    first = push_marked_event_law(
        state_mass, events, first_state, identity, identity
    )
    assert all(event is not None for event in first.conditional_events)
    staged_events = FractionTensor(
        (2, 2, 2),
        tuple(
            value
            for event in first.conditional_events
            if event is not None
            for value in event.values
        ),
    )
    staged = push_marked_event_law(
        first.coarse_state_mass,
        staged_events,
        second_state,
        collapse,
        collapse,
    )
    composed_state = compose_markov_kernels(first_state, second_state)
    assert composed_state.rows == (
        (Fraction(1, 2), Fraction(1, 2)),
        (Fraction(1, 6), Fraction(5, 6)),
    )
    direct = push_marked_event_law(
        state_mass,
        events,
        composed_state,
        compose_markov_kernels(identity, collapse),
        compose_markov_kernels(identity, collapse),
    )

    assert direct.joint.values == (Fraction(1, 4), Fraction(3, 4))
    assert staged == direct


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


def test_theorem_assumption_matrix_is_immutable_complete_and_boundary_preserving():
    from multiagent_elbo.finite.theory_oracles import (
        LANE_PRIVATE_AUXILIARY_PACKETS,
        THEOREM_ASSUMPTION_MATRIX,
    )

    expected_identities = {
        "evidence_elbo",
        "fixed_channel_fisher_defect",
        "marked_event_associativity",
        "full_hoeffding_mobius",
        "gaussian_inverse_congruence",
        "gaussian_galerkin_restriction",
        "gaussian_schur_complement",
        "two_scale_literal_commuting_square",
    }
    assert {record.identity_id for record in THEOREM_ASSUMPTION_MATRIX} == expected_identities
    for record in THEOREM_ASSUMPTION_MATRIX:
        assert record.premises
        assert record.theory_source.startswith("Theory/")
        assert record.theorem_status in {"ESTABLISHED", "HYPOTHESIS"}
        assert record.verification_state == "CANDIDATE"
        assert record.claim_origin in {"PROJECT_NOVEL", "APPLICATION_SPECIFIC"}
        assert record.evidence_kind == "exact_fraction_derivation_witness"
        assert record.falsification_condition
        with pytest.raises(FrozenInstanceError):
            record.verification_state = "EVIDENCE_VERIFIED"  # type: ignore[misc]

    assert {packet.packet_id for packet in LANE_PRIVATE_AUXILIARY_PACKETS} == {
        "oracle_aux_fisher_v1",
        "oracle_aux_marked_event_v1",
        "oracle_aux_hoeffding_v1",
        "oracle_aux_gaussian_v1",
    }
    assert all(packet.lane_private for packet in LANE_PRIVATE_AUXILIARY_PACKETS)
    assert all(
        not packet.replacement_application_fixture
        for packet in LANE_PRIVATE_AUXILIARY_PACKETS
    )
