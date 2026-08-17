"""Exact tests for the finite two-channel gauge primitives."""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import pytest

from multiagent_elbo.finite.categorical_falsification_model import build_reference_model
from multiagent_elbo.finite.two_channel_gauge import (
    CyclicRepresentation,
    DirectedEdge,
    TwoChannelGraph,
    based_holonomy_generators,
    declared_reverse_arcs,
    fixed_laws,
    fixed_simplex_laws,
    generated_subgroup,
    holonomy_group,
    orbit,
    orbit_closure,
    stabilizer,
    tree_transport_elements,
    uniform_law,
    walk_element,
)

BELIEF = CyclicRepresentation(3, 1, "belief")
MODEL = CyclicRepresentation(3, 2, "model")
SEED = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))

REFERENCE_EDGES = (
    DirectedEdge(1, 2),
    DirectedEdge(2, 3),
    DirectedEdge(3, 1),
    DirectedEdge(4, 5),
    DirectedEdge(5, 6),
    DirectedEdge(6, 4),
    DirectedEdge(3, 4),
    DirectedEdge(6, 1),
)


def _reference_graph() -> TwoChannelGraph:
    """Build the declared six-agent two-cycle graph of the falsification design."""
    return TwoChannelGraph(
        order=3,
        vertices=(1, 2, 3, 4, 5, 6),
        edges=REFERENCE_EDGES,
        belief_elements=(1, 1, 0, 1, 1, 1, 0, 0),
        model_elements=(1, 1, 1, 2, 2, 2, 0, 0),
    )


def test_the_two_declared_representations_are_faithful_and_distinct() -> None:
    """Mutation caught: collapsing the two channels onto a single group action."""
    assert BELIEF.is_faithful()
    assert MODEL.is_faithful()
    assert [BELIEF.shift(k) for k in range(3)] == [0, 1, 2]
    assert [MODEL.shift(k) for k in range(3)] == [0, 2, 1]
    assert BELIEF.shift(1) != MODEL.shift(1)


def test_pushforward_moves_mass_forward_and_composes_additively() -> None:
    """Mutation caught: pushing a law by the inverse of the declared element."""
    law = SEED
    assert BELIEF.act(1, law) == (Fraction(1, 6), Fraction(1, 2), Fraction(1, 3))
    assert BELIEF.act(1, BELIEF.act(1, law)) == BELIEF.act(2, law)
    assert BELIEF.act(0, law) == law
    assert MODEL.act(1, law) == BELIEF.act(2, law)


def test_orbits_are_closed_deduplicated_and_sorted() -> None:
    """Mutation caught: an admitted family that is not representation closed."""
    family = orbit(BELIEF, SEED)
    assert len(family) == 3
    assert tuple(sorted(family)) == family
    for law in family:
        for element in range(3):
            assert BELIEF.act(element, law) in family
    assert orbit_closure(BELIEF, [SEED, SEED]) == family


def test_the_uniform_law_is_the_only_stabilized_law_of_a_nontrivial_shift() -> None:
    """Mutation caught: an admitted family that secretly contains a fixed point."""
    assert stabilizer(BELIEF, uniform_law(3)) == (0, 1, 2)
    for law in orbit(BELIEF, SEED):
        assert stabilizer(BELIEF, law) == (0,)
    assert fixed_laws(BELIEF, (2,), orbit(BELIEF, SEED)) == ()
    assert fixed_laws(BELIEF, (0,), orbit(BELIEF, SEED)) == orbit(BELIEF, SEED)


def test_the_fixed_sector_of_the_whole_simplex_is_the_uniform_law_alone() -> None:
    """Mutation caught: reporting a nonempty fixed sector as a single point wrongly."""
    assert fixed_simplex_laws(BELIEF, (2,)) == (uniform_law(3),)
    assert len(fixed_simplex_laws(BELIEF, (0,))) == 3


def test_the_declared_transports_give_nontrivial_belief_and_flat_model_holonomy() -> None:
    """Mutation caught: transports that do not separate the two channels."""
    graph = _reference_graph()
    cycle_a = graph.induced((1, 2, 3))
    cycle_b = graph.induced((4, 5, 6))
    assert based_holonomy_generators(cycle_a, "belief", 1) == (2,)
    assert based_holonomy_generators(cycle_a, "model", 1) == (0,)
    assert holonomy_group(cycle_a, "belief", 1) == (0, 1, 2)
    assert holonomy_group(cycle_a, "model", 1) == (0,)
    assert holonomy_group(cycle_b, "belief", 4) == (0,)
    assert holonomy_group(cycle_b, "model", 4) == (0,)
    assert holonomy_group(graph, "model", 1) == (0,)
    assert holonomy_group(graph, "belief", 1) == (0, 1, 2)


def test_cycle_b_carries_nonzero_edge_elements_with_trivial_holonomy() -> None:
    """Mutation caught: a test that detects identity transports, not holonomy."""
    graph = _reference_graph()
    cycle_b = graph.induced((4, 5, 6))
    assert cycle_b.channel_elements("belief") == (1, 1, 1)
    assert cycle_b.channel_elements("model") == (2, 2, 2)
    assert holonomy_group(cycle_b, "belief", 4) == (0,)


def test_holonomy_triviality_survives_a_global_direction_flip() -> None:
    """Mutation caught: a result that depends on the receiver-source convention."""
    graph = _reference_graph()
    flipped = TwoChannelGraph(
        order=3,
        vertices=graph.vertices,
        edges=tuple(DirectedEdge(e.source, e.receiver) for e in graph.edges),
        belief_elements=tuple((-g) % 3 for g in graph.belief_elements),
        model_elements=tuple((-g) % 3 for g in graph.model_elements),
    )
    for block, root in (((1, 2, 3), 1), ((4, 5, 6), 4)):
        for channel in ("belief", "model"):
            original = holonomy_group(graph.induced(block), channel, root)
            mirrored = holonomy_group(flipped.induced(block), channel, root)
            assert (original == (0,)) == (mirrored == (0,))


def test_based_holonomy_is_root_independent_up_to_the_generated_subgroup() -> None:
    """Mutation caught: generators based at a chord instead of at the declared root."""
    graph = _reference_graph()
    cycle_a = graph.induced((1, 2, 3))
    groups = {holonomy_group(cycle_a, "belief", root) for root in (1, 2, 3)}
    assert groups == {(0, 1, 2)}


def test_tree_transports_are_trivial_at_the_root_and_consistent_along_the_tree() -> None:
    """Mutation caught: a tree transport that does not fix the root frame."""
    graph = _reference_graph()
    cycle_a = graph.induced((1, 2, 3))
    transports = tree_transport_elements(cycle_a, "belief", 1)
    assert transports[1] == 0
    assert set(transports) == {1, 2, 3}
    for value in transports.values():
        assert 0 <= value < 3


def test_generated_subgroup_closes_under_addition() -> None:
    """Mutation caught: reporting the generator list in place of the group."""
    assert generated_subgroup(3, (0,)) == (0,)
    assert generated_subgroup(3, (1,)) == (0, 1, 2)
    assert generated_subgroup(3, (2,)) == (0, 1, 2)
    assert generated_subgroup(3, ()) == (0,)


def test_walk_elements_are_signed_and_reverse_to_the_inverse() -> None:
    """Mutation caught: dropping the sign on a backward traversal."""
    graph = _reference_graph()
    forward = walk_element(graph, "belief", ((0, +1), (1, +1)))
    backward = walk_element(graph, "belief", ((1, -1), (0, -1)))
    assert (forward + backward) % 3 == 0


def test_a_backward_step_reads_the_declared_reverse_arc_where_one_exists() -> None:
    """Mutation caught: writing reciprocity into the walk primitive.

    On a graph carrying both orientations of a pair, traversing the pair backward is
    traversing the declared reverse arc, so the transport is that arc's own element.
    Reading it as the negated forward element would report the holonomy of a
    connection the graph does not declare, and would make the independent convention
    unobservable downstream.
    """
    graph = TwoChannelGraph(
        order=3,
        vertices=(1, 2),
        edges=(DirectedEdge(1, 2), DirectedEdge(2, 1)),
        belief_elements=(1, 1),
        model_elements=(1, 2),
    )
    assert declared_reverse_arcs(graph) == {0: 1, 1: 0}
    assert walk_element(graph, "belief", ((0, -1),)) == 1
    assert walk_element(graph, "model", ((0, -1),)) == 2
    assert walk_element(graph, "belief", ((0, +1), (1, +1))) == 2
    one_way = TwoChannelGraph(
        order=3,
        vertices=(1, 2),
        edges=(DirectedEdge(1, 2),),
        belief_elements=(1,),
        model_elements=(1,),
    )
    assert declared_reverse_arcs(one_way) == {}
    assert walk_element(one_way, "belief", ((0, -1),)) == 2


def test_the_declared_one_way_skeleton_is_untouched_by_the_reverse_arc_rule() -> None:
    """Mutation caught: a reverse-arc branch that moves the reference measurements.

    The declared instance carries no reciprocal pair, so no backward step has a
    reverse arc to read and the walk primitive is exactly the signed sum it always
    was. These are the pinned pre-change values of the two quantities the closure and
    holonomy measurements consume, and they must not move when the reverse-arc rule
    is added.
    """
    graph = _reference_graph()
    assert declared_reverse_arcs(graph) == {}
    assert holonomy_group(graph, "belief", 1) == (0, 1, 2)
    assert holonomy_group(graph, "model", 1) == (0,)
    for root in graph.vertices:
        assert holonomy_group(graph, "belief", root) == (0, 1, 2)
        assert holonomy_group(graph, "model", root) == (0,)
    assert tree_transport_elements(graph, "belief", 1) == {
        1: 0,
        2: 1,
        3: 0,
        4: 0,
        5: 2,
        6: 0,
    }
    assert tree_transport_elements(graph, "model", 1) == {
        1: 0,
        2: 1,
        3: 2,
        4: 2,
        5: 1,
        6: 0,
    }
    model = build_reference_model()
    assert np.allclose(
        model.downward_kernel((1, 2, 3), 2, 0),
        [
            0.04682274101033171,
            0.04682274101033171,
            0.18729096404132684,
            0.04254128345135986,
            0.04254128345135986,
            0.17016513380543943,
            0.0773026422049751,
            0.0773026422049751,
            0.3092105688199004,
        ],
        atol=0.0,
        rtol=1e-15,
    )
    assert np.allclose(
        model.downward_kernel((4, 5, 6), 6, 4),
        [
            0.18729096404132684,
            0.04682274101033171,
            0.04682274101033171,
            0.17016513380543943,
            0.04254128345135986,
            0.04254128345135986,
            0.3092105688199004,
            0.0773026422049751,
            0.0773026422049751,
        ],
        atol=0.0,
        rtol=1e-15,
    )


@pytest.mark.parametrize(
    "values",
    [
        (Fraction(1, 2), Fraction(1, 2)),
        (Fraction(1, 2), Fraction(1, 3), Fraction(1, 3)),
        (Fraction(-1, 2), Fraction(1, 2), Fraction(1)),
    ],
    ids=["wrong_length", "does_not_sum_to_one", "negative_entry"],
)
def test_malformed_laws_are_rejected(values: tuple[Fraction, ...]) -> None:
    """Mutation caught: silently renormalizing or truncating a malformed law."""
    with pytest.raises(ValueError):
        orbit(BELIEF, values)


def test_graph_construction_rejects_duplicate_edges_and_foreign_endpoints() -> None:
    """Mutation caught: accepting a skeleton that is not the declared one."""
    with pytest.raises(ValueError):
        TwoChannelGraph(
            order=3,
            vertices=(1, 2),
            edges=(DirectedEdge(1, 2), DirectedEdge(1, 2)),
            belief_elements=(0, 0),
            model_elements=(0, 0),
        )
    with pytest.raises(ValueError):
        TwoChannelGraph(
            order=3,
            vertices=(1, 2),
            edges=(DirectedEdge(1, 3),),
            belief_elements=(0,),
            model_elements=(0,),
        )
