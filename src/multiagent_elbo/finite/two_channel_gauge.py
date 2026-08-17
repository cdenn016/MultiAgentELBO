"""Finite two-channel gauge primitives over a cyclic structure group.

This module supplies the exact combinatorial and group-theoretic layer used by the
finite categorical falsification laboratory: a cyclic structure group carrying two
distinct representations, orbit-closed families of laws, a directed interaction
graph with one group element per edge per channel, root-based holonomy, and the
spanning-tree transports a block needs in order to name a parent frame.

Conventions fixed once, and relied on everywhere below.

An ordered pair ``(receiver, source)`` means the receiver observes the source, so a
row indexed by the receiver is a conditional law over sources, the occupancy
attaches to the receiver, and the edge transport carries the source frame into the
receiver frame. A walk is a sequence of steps, each step traversing one declared
edge either forward (source frame to receiver frame) or backward. Because the
structure group here is abelian, a walk transport is a signed sum of edge elements,
and reversing every direction convention at once negates every holonomy. Trivial
holonomy is therefore convention independent, which is what the belief against
model separation in the falsification design actually tests.

A backward step is where the reciprocity hypothesis would otherwise be smuggled in.
When the graph declares the reverse arc, that arc's own element is the transport of
the backward step, whatever it happens to be; the reciprocal element is used only
where no reverse arc is declared and the inverse is the sole reading available. On a
one-way skeleton the two agree identically, so nothing measured there moves.

All arithmetic is exact: laws are tuples of ``Fraction`` and group elements are
integers modulo the group order. No floating point enters this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Mapping, Sequence

Law = tuple[Fraction, ...]


def _as_law(values: Sequence[object], order: int) -> Law:
    """Coerce a sequence to an exact probability law on the cyclic sample space."""
    if len(values) != order:
        raise ValueError("law length must equal the group order")
    entries: list[Fraction] = []
    for value in values:
        if type(value) is bool:
            raise TypeError("law entries must not be bool")
        if type(value) is Fraction:
            entries.append(value)
        elif type(value) is int:
            entries.append(Fraction(value))
        elif type(value) is str:
            entries.append(Fraction(value))
        else:
            raise TypeError("law entries must be Fraction, int, or str")
    if any(entry < 0 for entry in entries):
        raise ValueError("law entries must be nonnegative")
    if sum(entries) != 1:
        raise ValueError("law entries must sum to exactly one")
    return tuple(entries)


@dataclass(frozen=True)
class CyclicRepresentation:
    """A representation of Z_order acting on Z_order by k -> multiplier * k."""

    order: int
    multiplier: int
    name: str

    def __post_init__(self) -> None:
        if type(self.order) is not int or self.order < 2:
            raise ValueError("order must be an integer at least two")
        if type(self.multiplier) is not int:
            raise TypeError("multiplier must be an integer")
        if type(self.name) is not str or not self.name:
            raise ValueError("name must be a nonempty string")

    def shift(self, element: int) -> int:
        """Return the sample-space shift produced by a group element."""
        return (self.multiplier * element) % self.order

    def is_faithful(self) -> bool:
        """Report whether distinct group elements induce distinct shifts."""
        return len({self.shift(k) for k in range(self.order)}) == self.order

    def permutation(self, element: int) -> tuple[int, ...]:
        """Return the sample-space permutation z -> z + shift(element)."""
        step = self.shift(element)
        return tuple((z + step) % self.order for z in range(self.order))

    def act(self, element: int, law: Law) -> Law:
        """Push a law forward by the group element, so mass at z moves to z + shift."""
        step = self.shift(element)
        return tuple(law[(z - step) % self.order] for z in range(self.order))

    def fixes(self, element: int, law: Law) -> bool:
        """Report whether the group element stabilizes the law exactly."""
        return self.act(element, law) == law


def uniform_law(order: int) -> Law:
    """Return the uniform law on the cyclic sample space."""
    return tuple(Fraction(1, order) for _ in range(order))


def orbit(representation: CyclicRepresentation, law: Sequence[object]) -> tuple[Law, ...]:
    """Return the orbit of one law under the representation, in sorted order."""
    seed = _as_law(law, representation.order)
    members = {representation.act(k, seed) for k in range(representation.order)}
    return tuple(sorted(members))


def orbit_closure(
    representation: CyclicRepresentation,
    seeds: Iterable[Sequence[object]],
) -> tuple[Law, ...]:
    """Return the smallest representation-closed family containing every seed."""
    members: set[Law] = set()
    for seed in seeds:
        members.update(orbit(representation, seed))
    if not members:
        raise ValueError("an admitted family must be nonempty")
    return tuple(sorted(members))


def stabilizer(representation: CyclicRepresentation, law: Law) -> tuple[int, ...]:
    """Return every group element that stabilizes the law exactly."""
    return tuple(k for k in range(representation.order) if representation.fixes(k, law))


def fixed_laws(
    representation: CyclicRepresentation,
    elements: Sequence[int],
    family: Sequence[Law],
) -> tuple[Law, ...]:
    """Return the members of an admitted family fixed by every listed element."""
    return tuple(
        law
        for law in family
        if all(representation.fixes(element, law) for element in elements)
    )


def fixed_simplex_laws(
    representation: CyclicRepresentation,
    elements: Sequence[int],
) -> tuple[Law, ...]:
    """Return generators of the fixed sector inside the whole simplex.

    For a cyclic shift action the fixed sector is the set of laws constant on the
    orbits of the induced permutation group, so it is the simplex spanned by the
    normalized orbit indicators. The returned tuple lists those indicators; the
    fixed sector is their convex hull, and it is a single point exactly when the
    induced group is transitive.
    """
    order = representation.order
    parent = list(range(order))

    def find(node: int) -> int:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for element in elements:
        step = representation.shift(element)
        for z in range(order):
            a, b = find(z), find((z + step) % order)
            if a != b:
                parent[a] = b
    blocks: dict[int, list[int]] = {}
    for z in range(order):
        blocks.setdefault(find(z), []).append(z)
    indicators: list[Law] = []
    for members in blocks.values():
        weight = Fraction(1, len(members))
        indicators.append(
            tuple(weight if z in members else Fraction(0) for z in range(order))
        )
    return tuple(sorted(indicators))


@dataclass(frozen=True)
class DirectedEdge:
    """One declared interaction, read as `receiver observes source`."""

    receiver: int
    source: int

    def __post_init__(self) -> None:
        if type(self.receiver) is not int or type(self.source) is not int:
            raise TypeError("edge endpoints must be integers")


@dataclass(frozen=True)
class TwoChannelGraph:
    """A finite directed graph carrying one group element per edge per channel."""

    order: int
    vertices: tuple[int, ...]
    edges: tuple[DirectedEdge, ...]
    belief_elements: tuple[int, ...]
    model_elements: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.order) is not int or self.order < 2:
            raise ValueError("order must be an integer at least two")
        if len(set(self.vertices)) != len(self.vertices):
            raise ValueError("vertices must be distinct")
        if len(self.edges) != len(self.belief_elements):
            raise ValueError("belief elements must be parallel to edges")
        if len(self.edges) != len(self.model_elements):
            raise ValueError("model elements must be parallel to edges")
        seen: set[tuple[int, int]] = set()
        for edge in self.edges:
            if edge.receiver not in self.vertices or edge.source not in self.vertices:
                raise ValueError("edge endpoints must be declared vertices")
            key = (edge.receiver, edge.source)
            if key in seen:
                raise ValueError("edges must be distinct ordered pairs")
            seen.add(key)
        for element in (*self.belief_elements, *self.model_elements):
            if type(element) is not int or not 0 <= element < self.order:
                raise ValueError("edge elements must lie in the structure group")

    def channel_elements(self, channel: str) -> tuple[int, ...]:
        """Return the per-edge group elements of one declared channel."""
        if channel == "belief":
            return self.belief_elements
        if channel == "model":
            return self.model_elements
        raise ValueError("channel must be 'belief' or 'model'")

    def sources_of(self, receiver: int) -> tuple[int, ...]:
        """Return the declared sources of one receiver, in edge order."""
        return tuple(edge.source for edge in self.edges if edge.receiver == receiver)

    def induced(self, block: Sequence[int]) -> "TwoChannelGraph":
        """Return the subgraph induced on a block of vertices."""
        members = tuple(v for v in self.vertices if v in set(block))
        keep = [
            index
            for index, edge in enumerate(self.edges)
            if edge.receiver in set(members) and edge.source in set(members)
        ]
        return TwoChannelGraph(
            order=self.order,
            vertices=members,
            edges=tuple(self.edges[index] for index in keep),
            belief_elements=tuple(self.belief_elements[index] for index in keep),
            model_elements=tuple(self.model_elements[index] for index in keep),
        )


def _spanning_tree(graph: TwoChannelGraph, root: int) -> dict[int, tuple[int, int]]:
    """Return, per reachable vertex, the (edge index, sign) step toward the root.

    The sign is +1 when the declared edge is traversed from source to receiver and
    -1 when it is traversed backward. The underlying graph is treated as undirected
    for the purpose of choosing the tree, which is the standard cycle-basis
    construction; direction is retained in the sign.
    """
    if root not in graph.vertices:
        raise ValueError("root must be a declared vertex")
    parent_step: dict[int, tuple[int, int]] = {}
    visited = {root}
    frontier = [root]
    while frontier:
        current = frontier.pop(0)
        for index, edge in enumerate(graph.edges):
            if edge.source == current and edge.receiver not in visited:
                parent_step[edge.receiver] = (index, +1)
                visited.add(edge.receiver)
                frontier.append(edge.receiver)
            elif edge.receiver == current and edge.source not in visited:
                parent_step[edge.source] = (index, -1)
                visited.add(edge.source)
                frontier.append(edge.source)
    return parent_step


def _walk_to_root(
    graph: TwoChannelGraph,
    parent_step: Mapping[int, tuple[int, int]],
    vertex: int,
    root: int,
) -> tuple[tuple[int, int], ...]:
    """Return the signed edge walk carrying the vertex frame to the root frame."""
    steps: list[tuple[int, int]] = []
    current = vertex
    while current != root:
        if current not in parent_step:
            raise ValueError("vertex is not connected to the root")
        index, sign = parent_step[current]
        steps.append((index, -sign))
        edge = graph.edges[index]
        current = edge.source if sign == +1 else edge.receiver
    return tuple(steps)


def declared_reverse_arcs(graph: TwoChannelGraph) -> dict[int, int]:
    """Return, per edge index, the index of its declared reverse arc where one exists.

    Self loops are excluded because their reverse is themselves, which would read a
    backward traversal as a forward one rather than as an inverse.
    """
    position = {
        (edge.receiver, edge.source): index for index, edge in enumerate(graph.edges)
    }
    return {
        index: position[(edge.source, edge.receiver)]
        for index, edge in enumerate(graph.edges)
        if edge.source != edge.receiver and (edge.source, edge.receiver) in position
    }


def walk_element(
    graph: TwoChannelGraph,
    channel: str,
    steps: Sequence[tuple[int, int]],
) -> int:
    r"""Return the group element of a signed edge walk in one channel.

    A forward step contributes the traversed arc's own element. A backward step of
    edge e contributes the element declared on the reverse arc when the graph
    declares one, and only otherwise the reciprocal -Theta_e. Reading a backward
    step as -Theta_e unconditionally would write the reciprocity hypothesis into the
    primitive, so a bi-directed instance with independent reverse transports would
    report the holonomy of a connection it does not declare.
    """
    elements = graph.channel_elements(channel)
    reverse = declared_reverse_arcs(graph)
    total = 0
    for index, sign in steps:
        if sign not in (+1, -1):
            raise ValueError("walk signs must be +1 or -1")
        if sign == +1:
            total += elements[index]
        elif index in reverse:
            total += elements[reverse[index]]
        else:
            total -= elements[index]
    return total % graph.order


def tree_transport_elements(
    graph: TwoChannelGraph,
    channel: str,
    root: int,
) -> dict[int, int]:
    """Return, per vertex, the group element carrying its frame to the root frame."""
    parent_step = _spanning_tree(graph, root)
    transports = {root: 0}
    for vertex in graph.vertices:
        if vertex == root:
            continue
        steps = _walk_to_root(graph, parent_step, vertex, root)
        transports[vertex] = walk_element(graph, channel, steps)
    return transports


def based_holonomy_generators(
    graph: TwoChannelGraph,
    channel: str,
    root: int,
) -> tuple[int, ...]:
    """Return the based holonomy generators of the graph at one root.

    One generator is emitted per non-tree edge, and each generator is a genuine
    loop based at the root: the tree walk from the root to the edge's source, the
    edge itself, and the tree walk from the edge's receiver back to the root. The
    two tree legs are what make these elements of a single based fundamental group
    rather than loops based at unrelated vertices.
    """
    parent_step = _spanning_tree(graph, root)
    tree_indices = {index for index, _ in parent_step.values()}
    generators: list[int] = []
    for index, edge in enumerate(graph.edges):
        if index in tree_indices:
            continue
        if edge.source not in parent_step and edge.source != root:
            continue
        if edge.receiver not in parent_step and edge.receiver != root:
            continue
        to_source = _reverse_walk(_walk_to_root(graph, parent_step, edge.source, root))
        from_receiver = _walk_to_root(graph, parent_step, edge.receiver, root)
        steps = (*to_source, (index, +1), *from_receiver)
        generators.append(walk_element(graph, channel, steps))
    return tuple(generators)


def _reverse_walk(steps: Sequence[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    """Return the reverse of a signed edge walk."""
    return tuple((index, -sign) for index, sign in reversed(steps))


def generated_subgroup(order: int, generators: Sequence[int]) -> tuple[int, ...]:
    """Return the cyclic subgroup generated by a set of elements, as a sorted tuple."""
    members = {0}
    frontier = [0]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            candidate = (current + generator) % order
            if candidate not in members:
                members.add(candidate)
                frontier.append(candidate)
    return tuple(sorted(members))


def holonomy_group(
    graph: TwoChannelGraph,
    channel: str,
    root: int,
) -> tuple[int, ...]:
    """Return the based holonomy group of one channel at one root."""
    generators = based_holonomy_generators(graph, channel, root)
    return generated_subgroup(graph.order, generators)


__all__ = [
    "CyclicRepresentation",
    "DirectedEdge",
    "Law",
    "TwoChannelGraph",
    "based_holonomy_generators",
    "declared_reverse_arcs",
    "fixed_laws",
    "fixed_simplex_laws",
    "generated_subgroup",
    "holonomy_group",
    "orbit",
    "orbit_closure",
    "stabilizer",
    "tree_transport_elements",
    "uniform_law",
    "walk_element",
]
