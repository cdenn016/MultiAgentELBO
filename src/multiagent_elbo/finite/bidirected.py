"""A genuinely bi-directed instance, and the two reverse-transport conventions.

The declared six-agent skeleton is one-way: every ordered pair carries an arc in
one direction only, so the row weight in the other direction is structurally zero
and the asymmetry of the attention is vacuous rather than a degree of freedom.
This module supplies the bi-directed instance in which both directions exist and
carry independent weights, so that a statement like beta from one to two being
three tenths while the reverse is one tenth is a fact about the model rather than
about which arcs were declared.

Adding the reverse arc forces a choice about its transport, and the two options are
physically different rather than notational.

Under the reciprocal convention the reverse transport is the inverse of the
forward one. This is the standard gauge reading, in which the reverse link is the
inverse link, and it is the hypothesis the zero-distortion and holonomy results of
this program already assume. Every two-cycle is then flat by construction, so
bi-directedness enriches the attention without adding curvature at the shortest
scale, and reversing a loop negates its holonomy.

Under the independent convention the reverse transport is a free group element.
One agent's transport of another need not invert the reverse, which is a
substantive claim about asymmetric epistemic access rather than a bookkeeping
choice. Two-cycles can then be curved, curvature appears at the shortest possible
scale, and the object is no longer a gauge connection in the usual sense, so the
results resting on reciprocity have to be restated rather than inherited.

Both are built here so the reciprocity hypothesis is measured rather than assumed,
which is how this laboratory treats every other declared choice.

Faces are taken as the two orientations of a cycle basis of the directed skeleton.
The full set of simple directed cycles of a bi-directed graph is far larger than the
cycle rank, twenty against eleven on this skeleton, and summing an action over all
of them would count curvature a number of times fixed by graph topology rather than
by anything physical. The basis has one two-cell per reciprocal pair together with a
spanning-tree fundamental loop per chord, which is exactly the directed cycle rank,
edges minus vertices plus one. Excluding the two-cycles would put the face set at
the undirected rank and blind the complex to curvature at the shortest scale, which
is the only scale at which the two conventions differ by construction. Each basis
loop is doubled by orientation because the two traversals carry different attention
weights even when their holonomies are related, and the action averages the two so
that a two-cell is charged once. The longer part of the basis depends on the
spanning tree, so the face set is a declared choice and is reported as one.

The two conventions are built as matched controls. The reverse-arc elements are
drawn from their own stream, so the attention rows and the forward elements are
identical across conventions and a numerical difference between the two instances is
attributable to the reverse-transport hypothesis alone.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from functools import lru_cache
from typing import Sequence

import numpy as np

from .categorical_falsification_model import FalsificationModel, build_reference_model
from .plaquette_action import wilson_defect
from .two_channel_gauge import DirectedEdge, TwoChannelGraph, declared_reverse_arcs

CONVENTIONS = ("reciprocal", "independent")


@dataclass(frozen=True)
class OrientedFace:
    """One orientation of a basis loop, with its holonomy and attention weight."""

    cycle: tuple[int, ...]
    edges: tuple[int, ...]
    orientation: str
    belief_holonomy: int
    model_holonomy: int
    belief_weight: float
    model_weight: float

    def holonomy(self, channel: str) -> int:
        """Return the holonomy of one channel around this oriented face."""
        return self.belief_holonomy if channel == "belief" else self.model_holonomy

    def weight(self, channel: str) -> float:
        """Return the attention coupling of one channel on this oriented face."""
        return self.belief_weight if channel == "belief" else self.model_weight


def _reverse_elements(
    elements: Sequence[int],
    order: int,
    convention: str,
    generator: np.random.Generator,
) -> tuple[int, ...]:
    """Return the reverse-arc group elements under the declared convention."""
    if convention == "reciprocal":
        return tuple((-value) % order for value in elements)
    if convention == "independent":
        return tuple(int(value) for value in generator.integers(0, order, len(elements)))
    raise ValueError("convention must be 'reciprocal' or 'independent'")


def _asymmetric_rows(
    agents: Sequence[int],
    arcs: Sequence[tuple[int, int]],
    generator: np.random.Generator,
) -> tuple[tuple[tuple[float, ...], ...], ...]:
    """Return independent, strictly positive rows for each channel.

    Every admitted source of a receiver draws its own weight, so the two
    directions of a pair are unrelated and no symmetry is imposed between them.
    The self loop is always admitted so no row collapses to a point mass.
    """
    size = len(agents)
    position = {agent: index for index, agent in enumerate(agents)}
    matrices: list[tuple[tuple[float, ...], ...]] = []
    for _ in range(2):
        matrix = np.zeros((size, size), dtype=np.float64)
        for receiver in agents:
            sources = {receiver} | {s for (s, r) in arcs if r == receiver}
            draws = generator.integers(1, 10, len(sources)).astype(np.float64)
            for weight, source in zip(draws, sorted(sources)):
                matrix[position[receiver], position[source]] = weight
            row = matrix[position[receiver]]
            row /= row.sum()
        matrices.append(tuple(tuple(float(v) for v in row) for row in matrix))
    return tuple(matrices)


def build_bidirected_model(
    convention: str = "reciprocal",
    seed: int = 20260817,
) -> FalsificationModel:
    """Return the six-agent instance with both arc directions and asymmetric rows.

    The skeleton, the representations, the presentation families and the candidate
    partitions are inherited unchanged from the declared instance, so the only
    differences are the added reverse arcs, their transports under the chosen
    convention, and genuinely two-sided attention.

    The reverse elements draw from a stream of their own so that the two conventions
    are matched controls: the forward elements and every attention row are identical
    across conventions, and the reciprocal branch consumes no draws it would then
    have to pay for elsewhere. Sharing one stream would confound the reverse-transport
    hypothesis with a different attention configuration.
    """
    if convention not in CONVENTIONS:
        raise ValueError("convention must be 'reciprocal' or 'independent'")
    reference = build_reference_model()
    order = reference.graph.order
    generator = np.random.default_rng(seed)
    element_generator = np.random.default_rng((seed, 1))
    forward = reference.graph.edges
    reverse = tuple(DirectedEdge(edge.source, edge.receiver) for edge in forward)
    belief = reference.graph.belief_elements + _reverse_elements(
        reference.graph.belief_elements, order, convention, element_generator
    )
    model_elements = reference.graph.model_elements + _reverse_elements(
        reference.graph.model_elements, order, convention, element_generator
    )
    graph = TwoChannelGraph(
        order=order,
        vertices=reference.graph.vertices,
        edges=forward + reverse,
        belief_elements=belief,
        model_elements=model_elements,
    )
    arcs = [(edge.source, edge.receiver) for edge in graph.edges]
    belief_rows, model_rows = _asymmetric_rows(reference.agents, arcs, generator)
    declared = tuple(
        (name, channel, matrix)
        for name in ("peaked",)
        for channel, matrix in (("belief", belief_rows), ("model", model_rows))
    )
    return replace(
        reference,
        name=f"bidirected-{convention}",
        graph=graph,
        row_configurations=("peaked",),
        declared_rows=declared,
    )


@lru_cache(maxsize=None)
def basis_loops(model: FalsificationModel) -> tuple[tuple[int, ...], ...]:
    """Return one cycle basis of the directed skeleton, two-cycles included.

    The longer loops are the fundamental loops of a spanning tree of the underlying
    undirected graph, one per chord, so a bi-directed pair contributes at most one of
    them. To those is added one two-cycle per reciprocal pair, the shortest two-cell
    the complex admits and the only place where the independent convention can put
    curvature that the reciprocal convention cannot. Their count together is the
    cycle rank of the directed graph, edges minus vertices plus one, which is three
    on the one-way skeleton and eleven on the bi-directed one. The longer part
    depends on the spanning tree, which makes the face set a declared choice rather
    than an invariant.
    """
    neighbors: dict[int, set[int]] = {v: set() for v in model.graph.vertices}
    for edge in model.graph.edges:
        if edge.source != edge.receiver:
            neighbors[edge.source].add(edge.receiver)
            neighbors[edge.receiver].add(edge.source)
    root = min(model.graph.vertices)
    parent: dict[int, int] = {root: root}
    order_seen = [root]
    frontier = [root]
    while frontier:
        current = frontier.pop(0)
        for following in sorted(neighbors[current]):
            if following not in parent:
                parent[following] = current
                order_seen.append(following)
                frontier.append(following)
    tree = {frozenset((child, mother)) for child, mother in parent.items() if child != mother}
    arcs = {(edge.source, edge.receiver) for edge in model.graph.edges}
    loops: list[tuple[int, ...]] = []
    two_cycles: list[tuple[int, ...]] = []
    for left in sorted(model.graph.vertices):
        for right in sorted(neighbors[left]):
            if right <= left:
                continue
            if (left, right) in arcs and (right, left) in arcs:
                two_cycles.append((left, right))
            if frozenset((left, right)) in tree:
                continue
            loops.append(tuple(_fundamental_loop(parent, left, right)))
    return tuple(two_cycles) + tuple(loops)


def _fundamental_loop(parent: dict[int, int], left: int, right: int) -> list[int]:
    """Return the tree path from one chord endpoint to the other, closing the loop."""

    def ancestry(node: int) -> list[int]:
        chain = [node]
        while parent[chain[-1]] != chain[-1]:
            chain.append(parent[chain[-1]])
        return chain

    first, second = ancestry(left), ancestry(right)
    common = next(node for node in first if node in second)
    head = first[: first.index(common) + 1]
    tail = second[: second.index(common)]
    return head + tail[::-1]


def _arc_elements(model: FalsificationModel) -> dict[tuple[int, int], int]:
    """Return the edge index of every arc, keyed source then receiver."""
    return {
        (edge.source, edge.receiver): index
        for index, edge in enumerate(model.graph.edges)
    }


def oriented_faces(
    model: FalsificationModel,
    configuration: str = "peaked",
) -> tuple[OrientedFace, ...]:
    """Return both orientations of every basis loop, with holonomy and weight.

    A face is a closed walk, so its weight is the product of the row entries along
    the direction actually traversed. Because the rows are two-sided and
    independent, the two orientations of the same loop generally carry different
    weights even when their holonomies are related.
    """
    arcs = _arc_elements(model)
    rows = model.attention_rows(configuration)
    position = {agent: index for index, agent in enumerate(model.agents)}
    order = model.graph.order
    faces: list[OrientedFace] = []
    for loop in basis_loops(model):
        for orientation, walk in (("forward", loop), ("reverse", loop[::-1])):
            holonomy: dict[str, int] = {}
            weight: dict[str, float] = {}
            traversed: list[int] = []
            usable = True
            for channel in ("belief", "model"):
                elements = model.graph.channel_elements(channel)
                total = 0
                product = 1.0
                traversed = []
                for step in range(len(walk)):
                    source = walk[step]
                    receiver = walk[(step + 1) % len(walk)]
                    if (source, receiver) not in arcs:
                        usable = False
                        break
                    traversed.append(arcs[(source, receiver)])
                    total += elements[arcs[(source, receiver)]]
                    product *= float(
                        rows[channel][position[receiver], position[source]]
                    )
                if not usable:
                    break
                holonomy[channel] = total % order
                weight[channel] = product
            if not usable:
                continue
            faces.append(
                OrientedFace(
                    cycle=tuple(walk),
                    edges=tuple(traversed),
                    orientation=orientation,
                    belief_holonomy=holonomy["belief"],
                    model_holonomy=holonomy["model"],
                    belief_weight=weight["belief"],
                    model_weight=weight["model"],
                )
            )
    return tuple(faces)


def _two_cell_key(model: FalsificationModel, face: OrientedFace) -> tuple[int, ...]:
    """Return the orientation-blind edge-index multiset naming one basis two-cell.

    Each traversed arc is named by the smaller of its own index and its declared
    reverse arc's, so the two orientations of a loop share a key while two distinct
    loops over the same vertices do not. Keying by the vertex set instead would merge
    loops that happen to visit the same vertices in a different order.
    """
    reverse = declared_reverse_arcs(model.graph)
    return tuple(sorted(min(index, reverse.get(index, index)) for index in face.edges))


def _faces_by_two_cell(
    model: FalsificationModel,
    configuration: str,
) -> dict[tuple[int, ...], dict[str, OrientedFace]]:
    """Return the oriented faces grouped by the two-cell they orient."""
    grouped: dict[tuple[int, ...], dict[str, OrientedFace]] = {}
    for face in oriented_faces(model, configuration):
        grouped.setdefault(_two_cell_key(model, face), {})[face.orientation] = face
    return grouped


def wilson_action(
    model: FalsificationModel,
    channel: str,
    configuration: str = "peaked",
) -> float:
    """Return the Wilson action of the basis two-cells, averaged over orientation.

    A geometric two-cell is charged once. Both traversals carry the same defect,
    because the defect is a class function and the two holonomies are inverse under
    either convention, but they carry different attention weights, so the coupling of
    the cell is the mean of the two directed traversal probabilities. Summing the
    orientations instead would charge every cell twice and put this quantity at a
    different normalization from the same-named function in `plaquette_action`, which
    sums simple directed cycles once each.
    """
    total = 0.0
    for entry in _faces_by_two_cell(model, configuration).values():
        faces = tuple(entry.values())
        total += sum(
            face.weight(channel) * wilson_defect(model, face.holonomy(channel), channel)
            for face in faces
        ) / len(faces)
    return float(total)


def reversal_is_inverse(
    model: FalsificationModel,
    configuration: str = "peaked",
) -> bool:
    """Report whether reversing every basis two-cell negates its holonomy.

    This is the operational signature of the reciprocal convention. It holds by
    construction there and fails generically under independent reverse transports,
    which makes the two conventions distinguishable from the faces alone rather
    than from the declaration.

    A two-cell that carries only one orientation is a different fact about the model
    and is raised rather than reported as a failure of reciprocity: a one-way
    skeleton has no reverse arc whose transport could disagree with the inverse, and
    reporting False there would read as a refuted hypothesis instead of an untestable
    one.
    """
    order = model.graph.order
    for entry in _faces_by_two_cell(model, configuration).values():
        if set(entry) != {"forward", "reverse"}:
            raise ValueError("a basis two-cell carries only one orientation")
        for channel in ("belief", "model"):
            forward = entry["forward"].holonomy(channel)
            reverse = entry["reverse"].holonomy(channel)
            if (forward + reverse) % order != 0:
                return False
    return True


__all__ = [
    "CONVENTIONS",
    "OrientedFace",
    "basis_loops",
    "build_bidirected_model",
    "oriented_faces",
    "reversal_is_inverse",
    "wilson_action",
]
