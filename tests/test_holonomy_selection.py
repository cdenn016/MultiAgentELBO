"""Tests for partition selection driven by the holonomy stabilization condition."""

from __future__ import annotations

import numpy as np
import pytest

from multiagent_elbo.finite.categorical_falsification_model import (
    build_null_model,
    build_reference_model,
)
from multiagent_elbo.finite import holonomy_selection as selection
from multiagent_elbo.finite import partition_dynamics as dynamics
from multiagent_elbo.finite.holonomy_retention import block_holonomy_group
from multiagent_elbo.finite.two_channel_gauge import TwoChannelGraph, uniform_law


def _forbidden(model) -> set:
    """Return the candidate partitions carrying a block with no coherent parent."""
    admitted = set(selection.admissible_partitions(model, False))
    return set(model.candidate_partitions) - admitted


def _empty_fixed_sector(model, block) -> bool:
    """Report whether the block holonomy fixes no admitted presentation."""
    belief = block_holonomy_group(model, tuple(block), "belief")
    law = block_holonomy_group(model, tuple(block), "model")
    beliefs = [
        q
        for q in model.belief_family
        if all(model.belief_representation.fixes(e, q) for e in belief)
    ]
    laws = [
        q
        for q in model.model_family
        if all(model.model_representation.fixes(e, q) for e in law)
    ]
    return not beliefs or not laws


def _belief_variant(model, elements: tuple[int, ...]):
    """Return the model with only its belief edge elements replaced."""
    graph = TwoChannelGraph(
        order=model.graph.order,
        vertices=model.graph.vertices,
        edges=model.graph.edges,
        belief_elements=elements,
        model_elements=model.graph.model_elements,
    )
    return type(model)(**{**vars(model), "graph": graph})


def test_a_block_enclosing_nontrivial_belief_holonomy_admits_no_parent() -> None:
    """Mutation caught: a downward kernel that ignores the stabilization condition."""
    model = build_reference_model()
    assert selection.admissible_parent_states(model, (1, 2, 3), False) == ()
    assert selection.admissible_parent_states(model, (1, 2, 3, 4), False) == ()
    assert selection.admissible_parent_states(model, (1, 2, 3, 4, 5, 6), False) == ()
    assert len(selection.admissible_parent_states(model, (4, 5, 6), False)) == 9


def test_exclusion_is_exactly_the_empty_fixed_sector_condition() -> None:
    """Mutation caught: excluding blocks by size or count rather than by holonomy."""
    for model in [build_reference_model()] + [build_null_model(s) for s in range(1, 9)]:
        predicted = {
            partition
            for partition in model.candidate_partitions
            if any(_empty_fixed_sector(model, block) for block in partition)
        }
        assert _forbidden(model) == predicted


def test_the_declared_instance_forbids_exactly_the_cycle_enclosing_partitions() -> None:
    """Mutation caught: an admissible set that does not track the declared design."""
    model = build_reference_model()
    assert _forbidden(model) == {
        ((1, 2, 3), (4, 5, 6)),
        ((1, 2, 3, 4, 5, 6),),
        ((1, 2, 3, 4), (5, 6)),
    }
    assert len(selection.admissible_partitions(model, False)) == 3


def test_a_forbidden_partition_has_infinite_energy_and_free_energy() -> None:
    """Mutation caught: a finite surrogate standing in for an absent parent."""
    model = build_reference_model()
    states = [0, 1, 2, 3, 4, 5]
    forbidden = ((1, 2, 3), (4, 5, 6))
    assert selection.constrained_block_energy(model, forbidden, states) == float("inf")
    assert selection.constrained_free_energy(model, forbidden, states) == float("inf")
    allowed = ((1, 2), (3, 4), (5, 6))
    assert np.isfinite(selection.constrained_block_energy(model, allowed, states))


def test_the_constrained_energy_responds_to_holonomy_where_the_tree_energy_does_not(
) -> None:
    """Mutation caught: the defect this module exists to repair, reintroduced."""
    model = build_reference_model()
    states = [0, 1, 2, 3, 4, 5]
    block = ((1, 2, 3), (4, 5, 6))
    tree_energies = []
    constrained_admissible = []
    for chord in (0, 1, 2):
        elements = list(model.graph.belief_elements)
        elements[1] = chord
        graph = TwoChannelGraph(
            order=model.graph.order,
            vertices=model.graph.vertices,
            edges=model.graph.edges,
            belief_elements=tuple(elements),
            model_elements=model.graph.model_elements,
        )
        variant = type(model)(
            **{**vars(model), "graph": graph}
        )
        tree_energies.append(dynamics.block_energy(variant, block, states))
        constrained_admissible.append(
            bool(selection.admissible_parent_states(variant, (1, 2, 3), False))
        )
    spread = max(tree_energies) - min(tree_energies)
    assert spread < 1.0e-3
    assert constrained_admissible == [False, False, True]


def test_augmenting_the_parent_space_with_the_uniform_law_admits_every_block() -> None:
    """Mutation caught: conflating the hard obstruction with the soft one."""
    model = build_reference_model()
    assert selection.admissible_parent_states(model, (1, 2, 3), True) != ()
    assert uniform_law(model.graph.order) not in model.belief_family
    assert len(selection.admissible_partitions(model, True)) == len(
        model.candidate_partitions
    )


def test_the_constrained_descent_never_visits_a_forbidden_partition() -> None:
    """Mutation caught: a chain that leaks into a partition with no coherent parent."""
    model = build_reference_model()
    trace = selection.constrained_descent(model, seed=5, noise=1.0, steps=80)
    forbidden = _forbidden(model)
    assert set(trace.partitions).isdisjoint(forbidden)
    assert set(trace.admissible) == set(selection.admissible_partitions(model, False))


def test_the_selection_report_is_normalized_and_names_its_exclusions() -> None:
    """Mutation caught: statistics reported without their admissibility context."""
    model = build_reference_model()
    report = selection.selection_report(
        model, seed=3, noise=1.0, steps=60, initializations=6
    )
    assert 0.0 < report.modal_occupancy <= 1.0
    assert report.maximum_residence_time > 0.0
    assert len(report.admissible_partitions) + len(report.forbidden_partitions) == len(
        model.candidate_partitions
    )
    assert report.modal_partition in set(report.admissible_partitions)


def test_a_model_whose_belief_family_degenerates_to_uniform_admits_every_block(
) -> None:
    """Mutation caught: treating the obstruction as a property of holonomy alone."""
    model = build_null_model(5)
    assert model.belief_family == (uniform_law(3),)
    assert block_holonomy_group(model, (4, 5, 6), "belief") != (0,)
    assert selection.admissible_parent_states(model, (4, 5, 6), False) != ()


def test_randomizing_transports_alone_changes_the_admissible_set() -> None:
    """Mutation caught: attributing to transports a sensitivity the family supplies.

    The declared null control randomizes the belief family alongside the
    transports, so variation under it does not isolate the gauge structure. Here
    the family, the skeleton, the occupancies and every kernel are held at their
    declared values and only the edge group elements move.
    """
    model = build_reference_model()
    generator = np.random.default_rng(20260817)
    counts: set[int] = set()
    for _ in range(24):
        elements = tuple(int(value) for value in generator.integers(0, 3, 8))
        variant = _belief_variant(model, elements)
        assert variant.belief_family == model.belief_family
        assert variant.graph.edges == model.graph.edges
        counts.add(len(selection.admissible_partitions(variant, False)))
    assert len(counts) > 1


def test_a_cycle_with_nonzero_transports_but_trivial_holonomy_is_admissible() -> None:
    """Mutation caught: forbidding cycles rather than forbidding nontrivial holonomy."""
    model = build_reference_model()
    assert model.graph.induced((4, 5, 6)).channel_elements("belief") == (1, 1, 1)
    assert block_holonomy_group(model, (4, 5, 6), "belief") == (0,)
    assert len(selection.admissible_parent_states(model, (4, 5, 6), False)) == 9


def test_selection_tracks_holonomy_and_not_block_size() -> None:
    """Mutation caught: a selector that is a block-size penalty in disguise."""
    model = build_reference_model()
    assert selection.admissible_parent_states(model, (1, 2, 3, 4), False) == ()
    swapped = _belief_variant(model, (1, 1, 1, 1, 1, 0, 0, 0))
    assert block_holonomy_group(swapped, (1, 2, 3), "belief") == (0,)
    assert block_holonomy_group(swapped, (4, 5, 6), "belief") != (0,)
    assert len(selection.admissible_parent_states(swapped, (1, 2, 3, 4), False)) == 9
    assert selection.admissible_parent_states(swapped, (4, 5, 6), False) == ()


def test_a_fully_flat_connection_forbids_no_partition_at_any_block_size() -> None:
    """Mutation caught: a residual size or cardinality penalty in the selector."""
    model = build_reference_model()
    flat = _belief_variant(model, (0,) * 8)
    flat = type(flat)(
        **{
            **vars(flat),
            "graph": TwoChannelGraph(
                order=flat.graph.order,
                vertices=flat.graph.vertices,
                edges=flat.graph.edges,
                belief_elements=(0,) * 8,
                model_elements=(0,) * 8,
            ),
        }
    )
    assert len(selection.admissible_partitions(flat, False)) == len(
        flat.candidate_partitions
    )
    assert len(selection.admissible_parent_states(flat, (1, 2, 3, 4, 5, 6), False)) == 9


@pytest.mark.parametrize("steps", [0, -1])
def test_the_constrained_descent_rejects_a_nonpositive_step_count(steps: int) -> None:
    """Mutation caught: silently substituting a default for an invalid budget."""
    with pytest.raises(ValueError):
        selection.constrained_descent(build_reference_model(), seed=1, noise=1.0, steps=steps)
