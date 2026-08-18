r"""The rescaling map, phase one: coarse connection, identification, and checks.

A complete renormalization step is a coarse channel followed by an
identification that puts the result back on a common footing with its input.
The coarse channel exists: blocking with the Bayes kernel, implemented in
:mod:`closure_residual`. This module supplies the connection half of the
identification and the two exact checks declared in the design, C1 and C2.
Reading the coarse couplings back into the family is phase two and is not here.

**Coarse connection.** The transport between adjacent parents is the Wilson
line along the fine path joining their block roots: the spanning-tree transport
from the receiving block's boundary agent to its root, the cross edge's own
element, and the inverse tree transport into the source block's root. In the
retained data of the mark-carrying parent this is exactly

    Theta_K = V_R(e) + V_S(e) - Theta_e,

where ``V_R(e)`` and ``V_S(e)`` are the dressed boundary generators of the same
cross edge as retained by the receiver-side and source-side blocks, so the
coarse link is composed from marks the parents already carry rather than from a
new construction. Under the declared gauge action the coarse link transforms as
a link under simultaneous frame changes at the two block roots, which is the
covariance a coarse connection requires.

**Graph identification.** The coarse graph of a cycle of blocks is a cycle,
and the identification relabels the parents as agents in the declared block
order, carrying no freedom once the boundary convention is fixed. **State
identification** is the identity: parent states and child states inhabit the
same nine-element space, so no state rescaling is available or needed.

**The gauge group of the coupled system.** Each channel carries its own
connection, and each channel's edge divergences are covariant under that
channel's gauges separately. The observation term is not: the evaluator pairs
the belief and model sample spaces point for point, so a pair of channel gauges
preserves the likelihood exactly when both induce the same sample-space shift.
The gauge group under which the coupled fine theory is covariant is therefore
parameterized by one sample shift per vertex, each channel receiving the group
element whose representation produces that shift; this requires both declared
representations to be faithful. Matter transforms as ``z' = rho(-h_v) z`` and
edges as ``Theta' = Theta + h_source - h_receiver``, the same action
:func:`mark_carrying_parent.regauge` declares.

**The parent law is frame data.** The declared parent law is attached to the
root frame of each block: regauging a root re-expresses the law in the new
frame rather than leaving it fixed while every transport moves. Check C1 feeds
the blocking exactly these re-expressed laws; feeding the fixed declared law
instead breaks covariance by construction, and the tests pin that failure so
the check is demonstrably able to fail.

**Declared checks.** C1, gauge covariance of the step: gauging the fine model
and then blocking must equal blocking and then applying the induced coarse
gauge, to ``1.0e-12`` on the coarse action and exactly on the coarse
connection. Failure refutes the construction, not the theory. C2, holonomy
conservation: the holonomy of the coarse cycle equals the fine holonomy of the
loop it encloses, exactly, as group elements, per channel; the fine loop runs
through each block along its spanning tree between the boundary agents and
across each cross edge, and each block's interior holonomy group is retained
per parent rather than discarded, which closes the cut-loop defect recorded in
the 2026-08-17 audit. Both sides of C2 are computed by independent walks, the
coarse side on the identified graph and the fine side on the full fine graph.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from itertools import product
from typing import Mapping, Sequence

from .categorical_falsification_model import FalsificationModel
from .closure_residual import _coarse_action, _declared_parent_prior
from .holonomy_retention import block_holonomy_group
from .mark_carrying_parent import mark_datum
from .scale_cocycle import State
from .two_channel_gauge import (
    CyclicRepresentation,
    DirectedEdge,
    TwoChannelGraph,
    _reverse_walk,
    _spanning_tree,
    _walk_to_root,
    based_holonomy_generators,
    declared_reverse_arcs,
    walk_element,
)

CHANNELS = ("belief", "model")
GAUGE_COVARIANCE_TOLERANCE = 1.0e-12


@dataclass(frozen=True)
class CoarseConnection:
    """The identified coarse graph, its per-channel links, and the retained marks.

    The graph's vertices are the parents relabeled ``1..m`` in declared block
    order, its edge elements are the Wilson-line coarse links, and the retained
    holonomy records each block's interior holonomy group per channel, keyed in
    block order as (belief group, model group) pairs. ``retained_generators``
    keeps, in the same keying, the based holonomy generators themselves — one
    element per interior fundamental loop of the block at its root — because
    the generated subgroup forgets the charge: in $Z_3$ the full group arises
    from generator one and from generator two alike, and Wilson-charge
    conservation is a statement about elements, not about the groups they
    generate. ``fine_edge_indices`` is parallel to the coarse edges and names
    the fine cross edge each one dresses.
    """

    blocks: tuple[tuple[int, ...], ...]
    roots: tuple[int, ...]
    graph: TwoChannelGraph
    fine_edge_indices: tuple[int, ...]
    retained_holonomy: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]
    retained_generators: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]


def _check_blocks(
    model: FalsificationModel,
    blocks: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    """Return the validated blocking, which must arrange every agent once."""
    declared = tuple(tuple(block) for block in blocks)
    if len(declared) < 2:
        raise ValueError("a coarse connection needs at least two blocks")
    arranged = sorted(agent for block in declared for agent in block)
    if arranged != sorted(model.agents):
        raise ValueError("the blocking must arrange every declared agent exactly once")
    return declared


def coarse_connection(
    model: FalsificationModel,
    blocks: Sequence[Sequence[int]],
) -> CoarseConnection:
    """Return the coarse connection of one blocking of the declared model.

    Each fine edge joining two distinct blocks becomes one coarse edge between
    the corresponding parents, oriented as the fine edge is, and its element is
    composed from the two dressed boundary generators the adjacent parents
    retain, ``Theta_K = V_R(e) + V_S(e) - Theta_e``. Two cross edges inducing
    the same ordered parent pair would need a coarse graph with parallel edges,
    which the declared graph type does not carry, so that case raises rather
    than silently merging.
    """
    if type(model) is not FalsificationModel:
        raise TypeError("model must be a FalsificationModel")
    declared = _check_blocks(model, blocks)
    for block in declared:
        if declared_reverse_arcs(model.graph.induced(block)):
            raise ValueError(
                "a block declares reciprocal arcs; the dressed-generator "
                "composition reads its reverse tree leg reciprocally, so the "
                "declared-reverse Wilson line is not implemented for such blocks"
            )
    block_of = {
        agent: index for index, block in enumerate(declared) for agent in block
    }
    order = model.graph.order
    data = {
        (index, channel): dict(mark_datum(model, block, channel, 0).boundary)
        for index, block in enumerate(declared)
        for channel in CHANNELS
    }
    coarse_edges: list[DirectedEdge] = []
    fine_indices: list[int] = []
    elements: dict[str, list[int]] = {channel: [] for channel in CHANNELS}
    for index, edge in enumerate(model.graph.edges):
        receiver_block = block_of[edge.receiver]
        source_block = block_of[edge.source]
        if receiver_block == source_block:
            continue
        coarse = DirectedEdge(receiver_block + 1, source_block + 1)
        if coarse in coarse_edges:
            raise ValueError(
                "two cross edges join the same ordered block pair; the coarse "
                "graph cannot carry parallel edges"
            )
        coarse_edges.append(coarse)
        fine_indices.append(index)
        for channel in CHANNELS:
            bare = model.graph.channel_elements(channel)[index]
            dressed_receiver = data[(receiver_block, channel)][
                (edge.receiver, edge.source)
            ]
            dressed_source = data[(source_block, channel)][
                (edge.receiver, edge.source)
            ]
            elements[channel].append(
                (dressed_receiver + dressed_source - bare) % order
            )
    if not coarse_edges:
        raise ValueError("the blocking cuts no edge, so no coarse connection exists")
    graph = TwoChannelGraph(
        order=order,
        vertices=tuple(range(1, len(declared) + 1)),
        edges=tuple(coarse_edges),
        belief_elements=tuple(elements["belief"]),
        model_elements=tuple(elements["model"]),
    )
    return CoarseConnection(
        blocks=declared,
        roots=tuple(min(block) for block in declared),
        graph=graph,
        fine_edge_indices=tuple(fine_indices),
        retained_holonomy=tuple(
            (
                block_holonomy_group(model, block, "belief"),
                block_holonomy_group(model, block, "model"),
            )
            for block in declared
        ),
        retained_generators=tuple(
            (
                based_holonomy_generators(
                    model.graph.induced(block), "belief", min(block)
                ),
                based_holonomy_generators(
                    model.graph.induced(block), "model", min(block)
                ),
            )
            for block in declared
        ),
    )


def _compatible_channel_element(
    representation: CyclicRepresentation,
    sample_shift: int,
) -> int:
    """Return the group element whose representation shifts samples by the shift."""
    try:
        inverse = pow(representation.multiplier % representation.order, -1, representation.order)
    except ValueError as error:
        raise ValueError(
            "the gauge group of the coupled system needs a faithful representation"
        ) from error
    return (inverse * sample_shift) % representation.order


def _checked_shifts(
    model: FalsificationModel,
    shifts: Mapping[int, int],
) -> dict[int, int]:
    """Return one sample shift per declared vertex, defaulting to zero."""
    unknown = set(shifts) - set(model.agents)
    if unknown:
        raise ValueError("gauge shifts must be keyed by declared vertices")
    order = model.graph.order
    return {vertex: int(shifts.get(vertex, 0)) % order for vertex in model.agents}


def gauge_transformed_model(
    model: FalsificationModel,
    shifts: Mapping[int, int],
) -> FalsificationModel:
    """Return the model with every connection regauged by the declared shifts.

    ``shifts`` assigns each vertex its sample-space shift; each channel receives
    the group element whose representation produces that shift, and every edge
    transforms by the declared action ``Theta' = Theta + h_source - h_receiver``.
    Occupancies, attention rows, and state families are frame-independent data
    and do not move; matter and the parent law are re-expressed by the caller
    through :func:`state_shift_permutation`.
    """
    if type(model) is not FalsificationModel:
        raise TypeError("model must be a FalsificationModel")
    values = _checked_shifts(model, shifts)
    order = model.graph.order
    new_elements: dict[str, tuple[int, ...]] = {}
    for channel, representation in (
        ("belief", model.belief_representation),
        ("model", model.model_representation),
    ):
        gauges = {
            vertex: _compatible_channel_element(representation, shift)
            for vertex, shift in values.items()
        }
        new_elements[channel] = tuple(
            (element + gauges[edge.source] - gauges[edge.receiver]) % order
            for element, edge in zip(
                model.graph.channel_elements(channel), model.graph.edges
            )
        )
    graph = TwoChannelGraph(
        order=order,
        vertices=model.graph.vertices,
        edges=model.graph.edges,
        belief_elements=new_elements["belief"],
        model_elements=new_elements["model"],
    )
    return replace(model, name=f"{model.name}-gauged", graph=graph)


def state_shift_permutation(
    model: FalsificationModel,
    sample_shift: int,
) -> tuple[int, ...]:
    """Return the state-index permutation of one vertex under one sample shift.

    Matter transforms as ``z' = rho(-h) z`` in each channel, with both channel
    elements chosen to produce the same sample shift, so the evaluator pairing
    and therefore the likelihood table are preserved exactly. The families are
    orbit closed, so the transformed laws are members and the map is a
    permutation of the joint state index.
    """
    order = model.graph.order
    belief_h = _compatible_channel_element(model.belief_representation, sample_shift)
    model_h = _compatible_channel_element(model.model_representation, sample_shift)
    model_size = len(model.model_family)
    permutation: list[int] = []
    for index in range(model.state_count):
        belief, law = model.state_pair(index)
        moved_belief = model.belief_representation.act((-belief_h) % order, belief)
        moved_model = model.model_representation.act((-model_h) % order, law)
        permutation.append(
            model.belief_family.index(moved_belief) * model_size
            + model.model_family.index(moved_model)
        )
    return tuple(permutation)


def coarse_action(
    model: FalsificationModel,
    observation: Sequence[int],
    blocks: Sequence[Sequence[int]],
    parent_priors: Mapping[int, Sequence[float]] | None = None,
) -> tuple[Mapping[State, Fraction], Mapping[State, Fraction]]:
    """Return the exact coarse action and its flow weights for one blocking.

    This is the coarse channel of the renormalization step, delegated to the
    blocking already implemented and audited in :mod:`closure_residual`, with
    the parent law optionally declared per block root so that a regauged root
    can carry its re-expressed law. The contraction runs on the CPU; the
    declared GPU worker protocol carries only the fixed-ray kernel today, and
    no phase-one instance exceeds a six-agent contraction, so extending the
    protocol is deferred to the phase that first needs a larger instance.
    """
    record = tuple(observation)
    if len(record) != len(model.agents):
        raise ValueError("the observation must carry one record per declared agent")
    if any(type(value) is not int or value not in (0, 1) for value in record):
        raise ValueError("every observation record must be binary")
    declared = _check_blocks(model, blocks)
    return _coarse_action(model, record, declared, parent_priors)


@dataclass(frozen=True)
class GaugeCovarianceReport:
    """Check C1: the blocking commutes with the declared gauge action."""

    shifts: tuple[tuple[int, int], ...]
    max_action_deviation: float
    connection_covariant: bool
    passes: bool


def check_gauge_covariance(
    model: FalsificationModel,
    observation: Sequence[int],
    blocks: Sequence[Sequence[int]],
    shifts: Mapping[int, int],
) -> GaugeCovarianceReport:
    """Run check C1 on one blocking under one declared gauge transformation.

    The gauged side blocks the regauged model with the parent law re-expressed
    at each root; the reference side blocks the original model and is then read
    through the induced coarse gauge, the per-root state permutations. The two
    coarse actions must agree to ``GAUGE_COVARIANCE_TOLERANCE``, and the coarse
    connection of the gauged model must equal the link-transformed coarse
    connection of the original exactly. Failure refutes the construction, not
    the theory.
    """
    values = _checked_shifts(model, shifts)
    declared = _check_blocks(model, blocks)
    gauged = gauge_transformed_model(model, values)
    base_prior = _declared_parent_prior(model.state_count)
    permutations: list[tuple[int, ...]] = []
    priors: dict[int, tuple[float, ...]] = {}
    for block in declared:
        root = min(block)
        sigma = state_shift_permutation(model, values[root])
        permutations.append(sigma)
        moved = [0.0] * len(base_prior)
        for state, weight in enumerate(base_prior):
            moved[sigma[state]] = weight
        priors[root] = tuple(moved)
    reference, _ = coarse_action(model, observation, declared)
    transformed, _ = coarse_action(gauged, observation, declared, priors)
    inverses = [
        tuple(sorted(range(len(sigma)), key=sigma.__getitem__))
        for sigma in permutations
    ]
    deviation = 0.0
    for state in product(range(model.state_count), repeat=len(declared)):
        pulled = tuple(
            inverses[position][value] for position, value in enumerate(state)
        )
        deviation = max(
            deviation,
            abs(float(transformed[state]) - float(reference[pulled])),
        )
    connection = coarse_connection(model, declared)
    gauged_connection = coarse_connection(gauged, declared)
    covariant = gauged_connection.graph.edges == connection.graph.edges
    order = model.graph.order
    for channel, representation in (
        ("belief", model.belief_representation),
        ("model", model.model_representation),
    ):
        gauges = {
            vertex + 1: _compatible_channel_element(
                representation, values[connection.roots[vertex]]
            )
            for vertex in range(len(declared))
        }
        expected = tuple(
            (element + gauges[edge.source] - gauges[edge.receiver]) % order
            for element, edge in zip(
                connection.graph.channel_elements(channel), connection.graph.edges
            )
        )
        covariant = covariant and (
            gauged_connection.graph.channel_elements(channel) == expected
        )
    return GaugeCovarianceReport(
        shifts=tuple(sorted(values.items())),
        max_action_deviation=deviation,
        connection_covariant=covariant,
        passes=deviation <= GAUGE_COVARIANCE_TOLERANCE and covariant,
    )


def _tree_path_steps(
    model: FalsificationModel,
    block: Sequence[int],
    start: int,
    goal: int,
) -> tuple[tuple[int, int], ...]:
    """Return the signed fine-edge walk from start to goal along the block tree."""
    induced = model.graph.induced(block)
    root = min(block)
    parent_step = _spanning_tree(induced, root)
    steps = (
        *_walk_to_root(induced, parent_step, start, root),
        *_reverse_walk(_walk_to_root(induced, parent_step, goal, root)),
    )
    position = {
        (edge.receiver, edge.source): index
        for index, edge in enumerate(model.graph.edges)
    }
    return tuple(
        (position[(induced.edges[index].receiver, induced.edges[index].source)], sign)
        for index, sign in steps
    )


@dataclass(frozen=True)
class HolonomyConservationReport:
    """Check C2: the coarse cycle holonomy equals the enclosed fine holonomy."""

    coarse_elements: tuple[tuple[str, int], ...]
    fine_elements: tuple[tuple[str, int], ...]
    retained_holonomy: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]
    passes: bool


def check_holonomy_conservation(
    model: FalsificationModel,
    blocks: Sequence[Sequence[int]],
) -> HolonomyConservationReport:
    """Run check C2 on one blocking whose coarse graph is a single cycle.

    The coarse side traverses the identified cycle once, every coarse edge
    forward, on the coarse graph. The fine side traverses the corresponding
    loop on the full fine graph: within each block along the spanning tree
    between the boundary agents, and across each cross edge. The two group
    elements must be equal exactly, per channel. Interior block holonomy is not
    part of this loop; it is retained per parent in the connection's marks, so
    nothing the blocking cuts is discarded.
    """
    connection = coarse_connection(model, blocks)
    graph = connection.graph
    outgoing: dict[int, int] = {}
    for index, edge in enumerate(graph.edges):
        if edge.source in outgoing:
            raise ValueError("the identified coarse graph is not a single cycle")
        outgoing[edge.source] = index
    if set(outgoing) != set(graph.vertices):
        raise ValueError("the identified coarse graph is not a single cycle")
    coarse_steps: list[tuple[int, int]] = []
    vertex = graph.vertices[0]
    for _ in graph.vertices:
        index = outgoing[vertex]
        coarse_steps.append((index, +1))
        vertex = graph.edges[index].receiver
    if vertex != graph.vertices[0]:
        raise ValueError("the identified coarse graph is not a single cycle")
    block_of = {
        agent: index
        for index, block in enumerate(connection.blocks)
        for agent in block
    }
    start = connection.roots[0]
    current = start
    fine_steps: list[tuple[int, int]] = []
    for index, _ in coarse_steps:
        fine_index = connection.fine_edge_indices[index]
        fine_edge = model.graph.edges[fine_index]
        source_block = connection.blocks[block_of[fine_edge.source]]
        if block_of[current] != block_of[fine_edge.source]:
            raise ValueError("the coarse traversal left the fine loop disconnected")
        fine_steps.extend(_tree_path_steps(model, source_block, current, fine_edge.source))
        fine_steps.append((fine_index, +1))
        current = fine_edge.receiver
    fine_steps.extend(
        _tree_path_steps(model, connection.blocks[block_of[current]], current, start)
    )
    coarse_elements = tuple(
        (channel, walk_element(graph, channel, coarse_steps)) for channel in CHANNELS
    )
    fine_elements = tuple(
        (channel, walk_element(model.graph, channel, fine_steps))
        for channel in CHANNELS
    )
    return HolonomyConservationReport(
        coarse_elements=coarse_elements,
        fine_elements=fine_elements,
        retained_holonomy=connection.retained_holonomy,
        passes=coarse_elements == fine_elements,
    )


@dataclass(frozen=True)
class WilsonChargeReport:
    """Conservation of the Wilson charge basis under one blocking step.

    The fine cycle space of a connected instance has rank $E - V + 1$, one
    independent charge per fundamental loop. Blocking used to discard every
    interior loop's charge; the fix is that the coarse side now carries the
    full basis: one charge per retained interior generator of each parent,
    plus one per coarse cycle. The report records both ranks, which must be
    equal, and the cut-loop element comparison per channel, which must be
    exact; per-parent retained charges are carried for inspection and are
    pinned against independently computed cycle elements in the tests.
    """

    fine_rank: int
    coarse_rank: int
    cut_loop_elements: tuple[tuple[str, int, int], ...]
    retained_charges: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]
    passes: bool


def check_wilson_charge_conservation(
    model: FalsificationModel,
    blocks: Sequence[Sequence[int]],
) -> WilsonChargeReport:
    """Check that no independent loop's Wilson charge is lost by blocking.

    Two exact conditions. First, rank conservation: the number of retained
    interior generators summed over parents, plus the cycle rank of the
    identified coarse graph, must equal the fine graph's cycle rank, so the
    coarse-side data spans the whole fine cycle space rather than the cut
    loops alone. Second, cut-loop charge conservation: the coarse cycle's
    element equals the fine element of the loop it encloses, per channel,
    which is the holonomy-conservation identity reused as a charge statement.
    """
    connection = coarse_connection(model, blocks)
    holonomy = check_holonomy_conservation(model, blocks)
    fine_rank = len(
        based_holonomy_generators(model.graph, "belief", min(model.agents))
    )
    coarse_rank = len(
        based_holonomy_generators(connection.graph, "belief", 1)
    ) + sum(len(belief) for belief, _ in connection.retained_generators)
    cut = tuple(
        (channel, coarse, dict(holonomy.fine_elements)[channel])
        for channel, coarse in holonomy.coarse_elements
    )
    return WilsonChargeReport(
        fine_rank=fine_rank,
        coarse_rank=coarse_rank,
        cut_loop_elements=cut,
        retained_charges=connection.retained_generators,
        passes=fine_rank == coarse_rank
        and all(coarse == fine for _, coarse, fine in cut),
    )


__all__ = [
    "CHANNELS",
    "CoarseConnection",
    "GAUGE_COVARIANCE_TOLERANCE",
    "GaugeCovarianceReport",
    "HolonomyConservationReport",
    "WilsonChargeReport",
    "check_gauge_covariance",
    "check_holonomy_conservation",
    "check_wilson_charge_conservation",
    "coarse_action",
    "coarse_connection",
    "gauge_transformed_model",
    "state_shift_permutation",
]
