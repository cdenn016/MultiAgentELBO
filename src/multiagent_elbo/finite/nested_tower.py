"""The declared self-similar family: a nested-cycle tower of two-channel blocks.

A level-one graph is a directed cycle of ``inner`` agents; a level-two graph is a
directed cycle of ``outer`` such blocks, adjacent blocks joined through designated
boundary agents. Write C(outer, inner) for the tower. Cycle sizes are free
parameters rather than fixed at three, which is load bearing for the
compatibility check: with a single ratio the semigroup law can only ever be
probed as b composed with itself, whereas free sizes allow blocking six agents by
six directly and comparing against two followed by three.

Structure carried at every level, unchanged from the reference instance of the
falsification design: two channels, belief and model, each a Z_3 representation
with its own transports; per-agent occupancies; the built-in attention row
configurations; and the declared parent law, which lives in the same nine-state
space at every level so that the state identification of the rescaling map is
the identity.

The boundary-agent convention is a genuine modeling choice and is declared
explicitly rather than hard coded. Under ``last_observes_first`` the last agent
of each block observes the first agent of the next block in cyclic order, which
is exactly the reference instance's convention: at C(2, 3) with the reference
transports and occupancies this module reproduces the reference skeleton edge
for edge. Under ``first_observes_last`` every cross arc is reversed. Both
conventions are exercised by the declared checks of the rescaling module.

This module declares instances. It computes no measurement.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Sequence

from .categorical_falsification_model import (
    BELIEF_SEED,
    FalsificationModel,
    GROUP_ORDER,
    MODEL_SEED,
    Partition,
    REFERENCE_ALPHA_BELIEF,
    REFERENCE_ALPHA_MODEL,
    REFERENCE_BELIEF_ELEMENTS,
    REFERENCE_MODEL_ELEMENTS,
)
from .two_channel_gauge import (
    CyclicRepresentation,
    DirectedEdge,
    TwoChannelGraph,
    orbit,
)

BOUNDARY_CONVENTIONS = ("last_observes_first", "first_observes_last")


def tower_agent(outer: int, inner: int, block: int, position: int) -> int:
    """Return the declared label of one agent of the tower, counted from one."""
    if not 0 <= block < outer or not 0 <= position < inner:
        raise ValueError("the agent coordinates must lie inside the tower")
    return block * inner + position + 1


def tower_blocks(outer: int, inner: int) -> Partition:
    """Return the declared blocking partition of the tower, one block per cycle."""
    _check_sizes(outer, inner)
    return tuple(
        tuple(tower_agent(outer, inner, block, position) for position in range(inner))
        for block in range(outer)
    )


def tower_edges(outer: int, inner: int, boundary: str) -> tuple[DirectedEdge, ...]:
    """Return the declared edges of the tower under one boundary convention.

    Inner edges run around each block in cyclic order, receiver observing the
    next agent, exactly as in the reference instance. Cross edge k joins block k
    to block k + 1 through the designated boundary agents: the last agent of
    block k and the first agent of block k + 1, with the orientation selected by
    the declared convention. Edges are ordered block by block, cross edges last,
    so at C(2, 3) under ``last_observes_first`` the tuple equals the reference
    edge tuple exactly.
    """
    _check_sizes(outer, inner)
    if boundary not in BOUNDARY_CONVENTIONS:
        raise ValueError("boundary must be a declared convention")
    edges: list[DirectedEdge] = []
    for block in range(outer):
        for position in range(inner):
            edges.append(
                DirectedEdge(
                    tower_agent(outer, inner, block, position),
                    tower_agent(outer, inner, block, (position + 1) % inner),
                )
            )
    for block in range(outer):
        exit_port = tower_agent(outer, inner, block, inner - 1)
        entry_port = tower_agent(outer, inner, (block + 1) % outer, 0)
        if boundary == "last_observes_first":
            edges.append(DirectedEdge(exit_port, entry_port))
        else:
            edges.append(DirectedEdge(entry_port, exit_port))
    return tuple(edges)


def _check_sizes(outer: int, inner: int) -> None:
    """Reject tower sizes the two-level construction cannot carry."""
    if type(outer) is not int or outer < 2:
        raise ValueError("the outer cycle must carry at least two blocks")
    if type(inner) is not int or inner < 3:
        raise ValueError(
            "an inner cycle must carry at least three agents; a 2-cycle's arcs "
            "form a reciprocal pair, which the declared cycle type refuses"
        )


def build_tower_model(
    outer: int,
    inner: int,
    belief_elements: Sequence[int],
    model_elements: Sequence[int],
    alpha_belief: Sequence[Fraction] | None = None,
    alpha_model: Sequence[Fraction] | None = None,
    boundary: str = "last_observes_first",
    name: str | None = None,
) -> FalsificationModel:
    """Return one declared instance of the nested-cycle tower C(outer, inner).

    The edge elements are declared data, parallel to :func:`tower_edges`: the
    inner elements of every block first, block by block, then one element per
    cross edge. Occupancies default to uniform and must sum to one exactly when
    declared. The candidate partitions are the declared blocking partition and
    the single-block coarsening, which is what the compatibility check of the
    design blocks by the full ratio.
    """
    _check_sizes(outer, inner)
    size = outer * inner
    edges = tower_edges(outer, inner, boundary)
    for field, elements in (("belief", belief_elements), ("model", model_elements)):
        if len(elements) != len(edges):
            raise ValueError(f"{field} elements must be parallel to the tower edges")
    alpha_belief = _occupancies(alpha_belief, size, "alpha_belief")
    alpha_model = _occupancies(alpha_model, size, "alpha_model")
    belief_representation = CyclicRepresentation(GROUP_ORDER, 1, "belief")
    model_representation = CyclicRepresentation(GROUP_ORDER, 2, "model")
    graph = TwoChannelGraph(
        order=GROUP_ORDER,
        vertices=tuple(range(1, size + 1)),
        edges=edges,
        belief_elements=tuple(int(element) for element in belief_elements),
        model_elements=tuple(int(element) for element in model_elements),
    )
    blocks = tower_blocks(outer, inner)
    return FalsificationModel(
        name=name if name is not None else f"tower-{outer}x{inner}-{boundary}",
        belief_representation=belief_representation,
        model_representation=model_representation,
        belief_family=orbit(belief_representation, BELIEF_SEED),
        model_family=orbit(model_representation, MODEL_SEED),
        graph=graph,
        alpha_belief=alpha_belief,
        alpha_model=alpha_model,
        parent_labels=tuple(f"A{index + 1}" for index in range(outer)),
        candidate_partitions=(blocks, (tuple(range(1, size + 1)),)),
        kappa_belief=2.0,
        kappa_model=2.0,
        crp_concentration=Fraction(1),
        identity_holonomy_weight=Fraction(1, 4),
        row_configurations=("uniform", "peaked"),
    )


def _occupancies(
    values: Sequence[Fraction] | None,
    size: int,
    field: str,
) -> tuple[Fraction, ...]:
    """Return declared per-agent occupancies, defaulting to the uniform law."""
    if values is None:
        return tuple(Fraction(1, size) for _ in range(size))
    declared = tuple(Fraction(value) for value in values)
    if len(declared) != size:
        raise ValueError(f"{field} must carry one occupancy per agent")
    if any(value < 0 for value in declared):
        raise ValueError(f"{field} occupancies must be nonnegative")
    if sum(declared) != 1:
        raise ValueError(f"{field} occupancies must sum to exactly one")
    return declared


def reference_tower() -> FalsificationModel:
    """Return C(2, 3) with the reference transports and occupancies.

    This instance carries the reference skeleton edge for edge, which is the
    declared consistency anchor of the family: the tower at its smallest sizes
    is the instance every published measurement already ran on.
    """
    return build_tower_model(
        2,
        3,
        REFERENCE_BELIEF_ELEMENTS,
        REFERENCE_MODEL_ELEMENTS,
        alpha_belief=REFERENCE_ALPHA_BELIEF,
        alpha_model=REFERENCE_ALPHA_MODEL,
        name="tower-reference",
    )


__all__ = [
    "BOUNDARY_CONVENTIONS",
    "build_tower_model",
    "reference_tower",
    "tower_agent",
    "tower_blocks",
    "tower_edges",
]
