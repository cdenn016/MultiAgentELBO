from __future__ import annotations

from fractions import Fraction
from itertools import product
import math

import numpy as np
import pytest

from multiagent_elbo.finite.categorical_falsification_model import (
    build_reference_model,
    kl_laws,
)
from multiagent_elbo.finite.holonomy_retention import (
    aligned_state_configuration,
    barycenter_is_group_element,
    block_components,
    block_holonomy_group,
    block_transport_elements,
    convolution_converse_witness,
    declared_endpoint_kernel,
    dressed_barycenter,
    dressed_transport_law,
    exact_dressed_transport_law,
    fixed_sector,
    holonomy_distortion,
    logical_chain_report,
    positive_atoms,
    prediction_report,
    reference_states,
    restricted_dressed_mass,
    retention_report,
    stabilizer_mass,
    theory_falsifier_verdict,
    transported_laws,
    zero_distortion_is_attainable,
)
from multiagent_elbo.finite.two_channel_gauge import (
    based_holonomy_generators,
    uniform_law,
)


def test_the_first_cycle_block_carries_the_whole_group_in_belief_and_nothing_in_the_model() -> None:
    model = build_reference_model()

    assert based_holonomy_generators(model.graph.induced((1, 2, 3)), "belief", 1) == (2,)
    assert block_holonomy_group(model, (1, 2, 3), "belief") == (0, 1, 2)
    assert block_holonomy_group(model, (1, 2, 3), "model") == (0,)


def test_the_second_cycle_block_carries_trivial_holonomy_in_both_channels() -> None:
    model = build_reference_model()

    assert block_holonomy_group(model, (4, 5, 6), "belief") == (0,)
    assert block_holonomy_group(model, (4, 5, 6), "model") == (0,)
    assert model.graph.induced((4, 5, 6)).belief_elements == (1, 1, 1)


def test_the_whole_graph_has_belief_generators_two_two_one_and_a_flat_model_channel() -> None:
    model = build_reference_model()

    assert based_holonomy_generators(model.graph, "belief", 1) == (2, 2, 1)
    assert based_holonomy_generators(model.graph, "model", 1) == (0, 0, 0)
    assert block_holonomy_group(model, model.agents, "belief") == (0, 1, 2)
    assert block_holonomy_group(model, model.agents, "model") == (0,)


def test_component_transports_reproduce_the_declared_block_transports_when_connected() -> None:
    model = build_reference_model()

    for block in ((1, 2, 3), (4, 5, 6), (3, 4), (2, 3, 4, 5, 6)):
        for channel in ("belief", "model"):
            assert block_components(model, block) == (tuple(block),)
            assert block_transport_elements(model, block, channel) == model.block_transports(
                block, channel
            )


def test_the_orbit_family_leaves_an_empty_fixed_sector_and_an_infinite_belief_score() -> None:
    model = build_reference_model()
    states = reference_states(model)

    assert fixed_sector(model, (1, 2, 3), "belief", "orbit") == ()
    assert holonomy_distortion(model, (1, 2, 3), "belief", "orbit", states) == math.inf
    assert not zero_distortion_is_attainable(model, (1, 2, 3), "belief", "orbit")


def test_the_simplex_family_leaves_the_uniform_law_and_a_finite_positive_belief_score() -> None:
    model = build_reference_model()
    states = reference_states(model)

    sector = fixed_sector(model, (1, 2, 3), "belief", "simplex")
    score = holonomy_distortion(model, (1, 2, 3), "belief", "simplex", states)
    entropy = -sum(
        float(value) * math.log(float(value)) for value in model.belief_family[0]
    )

    assert sector == (uniform_law(3),)
    assert math.isfinite(score)
    assert score > 0.0
    assert score == pytest.approx(math.log(3.0) - entropy, abs=1e-12)


def test_the_score_vanishes_exactly_when_every_transported_law_sits_in_the_fixed_sector() -> None:
    model = build_reference_model()
    target = model.belief_family[0]
    aligned = aligned_state_configuration(model, (4, 5, 6), "belief", target)
    carried = transported_laws(model, (4, 5, 6), "belief", aligned, (0,))
    disturbed = dict(aligned)
    disturbed[6] = (disturbed[6] + len(model.model_family)) % model.state_count

    assert set(carried.values()) == {target}
    assert holonomy_distortion(model, (4, 5, 6), "belief", "orbit", aligned) == 0.0
    assert holonomy_distortion(model, (4, 5, 6), "belief", "simplex", aligned) == 0.0
    assert holonomy_distortion(model, (4, 5, 6), "belief", "orbit", disturbed) > 0.0

    cyclic = aligned_state_configuration(model, (1, 2, 3), "belief", target)
    agreeing = transported_laws(model, (1, 2, 3), "belief", cyclic, (0,))

    assert set(agreeing.values()) == {target}
    assert target not in fixed_sector(model, (1, 2, 3), "belief", "simplex")
    assert holonomy_distortion(model, (1, 2, 3), "belief", "simplex", cyclic) > 0.0


def test_brute_force_state_search_agrees_with_the_zero_score_criterion_on_a_small_block() -> None:
    model = build_reference_model()
    block = (3, 4)

    for channel in ("belief", "model"):
        for admitted in ("orbit", "simplex"):
            family = model.belief_family if channel == "belief" else model.model_family
            found = False
            for first, second in product(range(len(family)), repeat=2):
                states = {
                    3: aligned_state_configuration(model, (3,), channel, family[first])[3],
                    4: aligned_state_configuration(model, (4,), channel, family[second])[4],
                }
                if holonomy_distortion(model, block, channel, admitted, states) == 0.0:
                    found = True
            assert found is zero_distortion_is_attainable(model, block, channel, admitted)


def test_the_dressed_transport_law_sums_to_one_while_the_restricted_numerator_does_not() -> None:
    model = build_reference_model()
    kernel = declared_endpoint_kernel(model)

    for channel in ("belief", "model"):
        for pair in (("A1", "A1"), ("A1", "A2"), ("A2", "A2")):
            exact = exact_dressed_transport_law(model, channel, kernel, pair)
            law = dressed_transport_law(model, channel, kernel, pair)
            restricted = restricted_dressed_mass(model, channel, kernel, pair)

            assert sum(exact.values(), Fraction(0)) == 1
            assert all(mass >= 0 for mass in exact.values())
            assert math.fsum(law.values()) == 1.0
            assert type(restricted) is Fraction
            assert restricted != 1
            assert restricted > 1


def test_the_split_child_is_what_breaks_the_restricted_numerator() -> None:
    model = build_reference_model()
    kernel = declared_endpoint_kernel(model)
    hard = type(kernel)(
        labels=kernel.labels,
        agents=kernel.agents,
        weights=(
            (Fraction(1), Fraction(0), Fraction(0)),
            (Fraction(1), Fraction(0), Fraction(0)),
            (Fraction(1), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(1), Fraction(0)),
        ),
    )

    assert kernel.membership("A1", 3) == Fraction(1, 2)
    assert restricted_dressed_mass(model, "belief", kernel, ("A1", "A1")) != 1
    assert restricted_dressed_mass(model, "belief", hard, ("A1", "A1")) == 1


def test_the_belief_loop_barycenter_is_doubly_stochastic_but_not_a_permutation_matrix() -> None:
    model = build_reference_model()
    kernel = declared_endpoint_kernel(model)
    law = dressed_transport_law(model, "belief", kernel, ("A1", "A1"))
    barycenter = dressed_barycenter(law, model.belief_representation)

    assert positive_atoms(law) == (0, 2)
    np.testing.assert_allclose(barycenter.sum(axis=0), np.ones(3), atol=1e-14, rtol=0.0)
    np.testing.assert_allclose(barycenter.sum(axis=1), np.ones(3), atol=1e-14, rtol=0.0)
    assert not barycenter_is_group_element(barycenter, model.belief_representation)

    flat = dressed_transport_law(model, "model", kernel, ("A1", "A1"))
    flat_barycenter = dressed_barycenter(flat, model.model_representation)

    assert barycenter_is_group_element(flat_barycenter, model.model_representation)


def test_a_flat_channel_puts_all_the_loop_mass_on_the_stabilizer_of_every_admitted_law() -> None:
    model = build_reference_model()
    report = logical_chain_report(model)

    assert report.flat_holonomy == (0,)
    assert report.flat_loop_law[0] == 1.0
    assert report.minimum_flat_stabilizer_mass == 1.0
    assert report.flatness_implies_stabilization

    kernel = declared_endpoint_kernel(model)
    law = dressed_transport_law(model, "model", kernel, ("A1", "A1"))
    for admitted in model.model_family:
        assert stabilizer_mass(law, model.model_representation, admitted) == 1.0


def test_flatness_does_not_imply_agreement_between_two_identically_transported_agents() -> None:
    model = build_reference_model()
    report = logical_chain_report(model)
    transports = block_transport_elements(model, (3, 4), "belief")

    assert block_holonomy_group(model, (3, 4), "belief") == (0,)
    assert transports == {3: 0, 4: 0}
    assert report.disagreement_distortion > 0.0
    assert not report.flatness_implies_agreement


def test_stabilization_without_flatness_has_no_orbit_witness_but_holds_on_the_uniform_law() -> None:
    model = build_reference_model()
    report = logical_chain_report(model)

    for representation, family in (
        (model.belief_representation, model.belief_family),
        (model.model_representation, model.model_family),
    ):
        for law in family:
            for element in (1, 2):
                assert not representation.fixes(element, law)
    assert not report.stabilization_without_flatness_in_orbit_family
    assert report.curved_holonomy == (0, 1, 2)
    assert report.uniform_stabilizer_mass == 1.0
    assert report.stabilization_without_flatness_on_uniform


def test_convolution_equality_does_not_imply_conditional_independence() -> None:
    witness = convolution_converse_witness()

    assert witness.composite_matches_convolution
    assert not witness.joint_is_a_product
    assert witness.joint[(1, 1)] == pytest.approx(1.0 / 3.0)
    assert witness.joint.get((0, 1), 0.0) == 0.0
    for element in range(3):
        assert witness.composite[element] == pytest.approx(1.0 / 3.0)
        assert witness.convolution[element] == pytest.approx(1.0 / 3.0)


def test_the_predictions_and_the_theory_falsifier_are_reported_as_measured() -> None:
    model = build_reference_model()
    predictions = prediction_report(model)
    verdict = theory_falsifier_verdict(model)

    assert predictions.belief_cyclic_orbit == math.inf
    assert predictions.belief_cyclic_simplex > 0.0
    assert predictions.belief_positive_on_cyclic_block
    assert predictions.model_cyclic_zero_distortion == 0.0
    assert predictions.model_can_vanish_on_cyclic_block
    assert predictions.both_can_vanish_on_flat_block
    assert not verdict.fired
    assert ((4, 5, 6), "orbit") in verdict.zero_distortion_blocks


def test_every_candidate_block_channel_and_admitted_family_is_measured() -> None:
    model = build_reference_model()
    rows = retention_report(model)
    blocks = sum(len(partition) for partition in model.candidate_partitions)

    assert len(rows) == 4 * blocks
    assert {row.admitted for row in rows} == {"orbit", "simplex"}
    assert {row.channel for row in rows} == {"belief", "model"}
    for row in rows:
        assert row.fixed_sector_size == len(
            fixed_sector(model, row.block, row.channel, row.admitted)
        )
        if row.admitted == "orbit" and row.fixed_sector_size == 0:
            assert row.distortion == math.inf
        else:
            assert math.isfinite(row.distortion)


def test_the_maximally_cross_cutting_partition_is_measured_component_wise() -> None:
    model = build_reference_model()
    states = reference_states(model)

    assert block_components(model, (1, 4)) == ((1,), (4,))
    assert block_holonomy_group(model, (1, 4), "belief") == (0,)
    assert holonomy_distortion(model, (1, 4), "belief", "orbit", states) == 0.0


def test_the_weighted_mixture_is_the_unconstrained_forward_divergence_minimizer() -> None:
    model = build_reference_model()
    states = reference_states(model)
    block = (4, 5, 6)
    carried = transported_laws(model, block, "belief", states, (0,))
    weights = {4: Fraction(12, 25), 5: Fraction(8, 25), 6: Fraction(5, 25)}
    mixture = tuple(
        sum((weights[agent] * carried[agent][index] for agent in block), Fraction(0))
        for index in range(3)
    )
    score = sum(float(weights[agent]) * kl_laws(carried[agent], mixture) for agent in block)

    assert holonomy_distortion(model, block, "belief", "simplex", states) == pytest.approx(
        score, abs=1e-14
    )
    for candidate in model.belief_family:
        assert sum(
            float(weights[agent]) * kl_laws(carried[agent], candidate) for agent in block
        ) >= score - 1e-14


def test_the_declared_channel_and_family_names_are_enforced() -> None:
    model = build_reference_model()
    states = reference_states(model)

    with pytest.raises(ValueError):
        fixed_sector(model, (1, 2, 3), "posterior", "orbit")
    with pytest.raises(ValueError):
        fixed_sector(model, (1, 2, 3), "belief", "gaussian")
    with pytest.raises(ValueError):
        holonomy_distortion(model, (1, 2, 3), "belief", "gaussian", states)
