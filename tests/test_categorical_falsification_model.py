"""Tests for the declared finite categorical falsification model instance."""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import pytest

from multiagent_elbo.finite.categorical_falsification_model import (
    REDUCED_SINGLETON_PARTITION,
    build_null_model,
    build_reduced_model,
    build_reference_model,
    crp_partition_prior,
    kl_laws,
    transported,
)
from multiagent_elbo.finite.two_channel_gauge import holonomy_group, uniform_law


def test_the_reference_instance_matches_the_declared_design() -> None:
    """Mutation caught: silently altering the frozen system declaration."""
    model = build_reference_model()
    assert model.agents == (1, 2, 3, 4, 5, 6)
    assert len(model.graph.edges) == 8
    assert len(model.belief_family) == 3
    assert len(model.model_family) == 3
    assert model.state_count == 9
    assert len(model.candidate_partitions) == 6
    assert model.parent_labels == ("A1", "A2", "A3")
    assert sum(model.alpha_belief) == 1
    assert sum(model.alpha_model) == 1
    assert model.alpha_belief != model.alpha_model


def test_neither_admitted_orbit_family_contains_the_uniform_law() -> None:
    """Mutation caught: an orbit family that secretly admits a holonomy fixed point."""
    model = build_reference_model()
    assert uniform_law(3) not in model.belief_family
    assert uniform_law(3) not in model.model_family


def test_the_likelihood_is_normalized_and_bounded_away_from_the_endpoints() -> None:
    """Mutation caught: a likelihood that can vanish and break integrability."""
    table = build_reference_model().likelihood_table()
    assert table.shape == (9, 2)
    assert np.allclose(table.sum(axis=1), 1.0, atol=1e-15)
    assert table.min() > 0.0
    assert table.max() < 1.0


def test_edge_event_laws_are_probability_laws_on_ordered_pairs() -> None:
    """Mutation caught: coarse-graining a row instead of the joint event law."""
    model = build_reference_model()
    for configuration in model.row_configurations:
        for channel in ("belief", "model"):
            eta = model.edge_event_law(configuration, channel)
            assert eta.shape == (6, 6)
            assert eta.min() >= 0.0
            assert eta.sum() == pytest.approx(1.0, abs=1e-12)


def test_attention_rows_are_normalized_over_sources_and_supported_on_the_skeleton() -> None:
    """Mutation caught: rows normalized over receivers instead of sources."""
    model = build_reference_model()
    index_of = {agent: position for position, agent in enumerate(model.agents)}
    for configuration in model.row_configurations:
        rows = model.attention_rows(configuration)["belief"]
        assert np.allclose(rows.sum(axis=1), 1.0, atol=1e-12)
        for receiver in model.agents:
            admitted = {receiver, *model.graph.sources_of(receiver)}
            for source in model.agents:
                if source not in admitted:
                    assert rows[index_of[receiver], index_of[source]] == 0.0


def test_the_downward_kernel_is_normalized_for_every_parent_state() -> None:
    """Mutation caught: an unnormalized downward kernel breaking tower normalization."""
    model = build_reference_model()
    for block in ((1, 2, 3), (4, 5, 6)):
        for agent in block:
            for parent_state in range(model.state_count):
                kernel = model.downward_kernel(block, agent, parent_state)
                assert kernel.shape == (9,)
                assert kernel.min() > 0.0
                assert kernel.sum() == pytest.approx(1.0, abs=1e-12)


def test_the_downward_kernel_peaks_on_the_transported_parent_state() -> None:
    """Mutation caught: a downward kernel that ignores the tree transport."""
    model = build_reference_model()
    block = (4, 5, 6)
    for agent in block:
        belief_shift = model.block_transports(block, "belief")[agent]
        model_shift = model.block_transports(block, "model")[agent]
        for parent_state in range(model.state_count):
            parent_belief, parent_model = model.state_pair(parent_state)
            target_belief = transported(
                model.belief_representation, (-belief_shift) % 3, parent_belief
            )
            target_model = transported(
                model.model_representation, (-model_shift) % 3, parent_model
            )
            expected = None
            for index in range(model.state_count):
                belief, model_law = model.state_pair(index)
                if belief == target_belief and model_law == target_model:
                    expected = index
            assert expected is not None
            kernel = model.downward_kernel(block, agent, parent_state)
            assert int(np.argmax(kernel)) == expected


def test_the_crp_prior_normalizes_exactly_over_all_set_partitions() -> None:
    """Mutation caught: an unnormalized partition prior smuggling in a free constant."""
    partitions = (
        ((1,), (2,), (3,)),
        ((1, 2), (3,)),
        ((1, 3), (2,)),
        ((2, 3), (1,)),
        ((1, 2, 3),),
    )
    total = sum(crp_partition_prior(p, Fraction(1)) for p in partitions)
    assert total == Fraction(1)
    with pytest.raises(ValueError):
        crp_partition_prior(((1,),), Fraction(0))


def test_the_crp_prior_charges_for_block_count_at_small_concentration() -> None:
    """Mutation caught: a prior that cannot penalize the all-singleton degeneracy."""
    singletons = ((1,), (2,), (3,))
    one_block = ((1, 2, 3),)
    small = Fraction(1, 10)
    assert crp_partition_prior(singletons, small) < crp_partition_prior(one_block, small)


def test_the_reduced_instance_keeps_both_channels_and_the_holonomy_asymmetry() -> None:
    """Mutation caught: a cut-down that quietly discards the tested asymmetry."""
    reduced = build_reduced_model()
    assert reduced.agents == (1, 2, 3)
    assert len(reduced.belief_family) == 3
    assert len(reduced.model_family) == 3
    assert sum(reduced.alpha_belief) == 1
    assert holonomy_group(reduced.graph, "belief", 1) == (0, 1, 2)
    assert holonomy_group(reduced.graph, "model", 1) == (0,)


def test_every_reduced_partition_fits_the_reduced_label_pool() -> None:
    """Mutation caught: a flat enumeration that outgrows its declared label pool."""
    reduced = build_reduced_model()
    for partition in reduced.candidate_partitions:
        assert len(partition) <= len(reduced.parent_labels)
        assert sorted(agent for block in partition for agent in block) == [1, 2, 3]
    assert len(REDUCED_SINGLETON_PARTITION) > len(reduced.parent_labels)


def test_every_reference_partition_fits_the_reference_label_pool() -> None:
    """Mutation caught: indexing a scale by occupied sets instead of a fixed pool."""
    model = build_reference_model()
    for partition in model.candidate_partitions:
        assert len(partition) <= len(model.parent_labels)
        assert sorted(agent for block in partition for agent in block) == [1, 2, 3, 4, 5, 6]


def test_the_null_control_randomizes_transports_while_holding_the_skeleton() -> None:
    """Mutation caught: a null control that also perturbs the graph being tested."""
    reference = build_reference_model()
    null = build_null_model(7)
    assert null.graph.edges == reference.graph.edges
    assert null.graph.vertices == reference.graph.vertices
    assert null.alpha_belief == reference.alpha_belief
    assert null.candidate_partitions == reference.candidate_partitions
    assert len(null.belief_family) == 3
    distinct = {
        build_null_model(seed).graph.belief_elements for seed in range(6)
    }
    assert len(distinct) > 1


def test_relative_entropy_of_laws_is_exact_zero_and_infinite_where_it_should_be() -> None:
    """Mutation caught: clamping an infinite divergence to a finite surrogate."""
    law = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))
    assert kl_laws(law, law) == pytest.approx(0.0, abs=1e-15)
    supported = (Fraction(1, 2), Fraction(1, 2), Fraction(0))
    assert kl_laws(law, supported) == float("inf")
    assert kl_laws(supported, law) > 0.0
