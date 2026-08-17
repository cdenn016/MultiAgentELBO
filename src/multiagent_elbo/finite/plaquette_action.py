"""Attention-weighted plaquettes and the Wilson action they carry.

Lattice gauge theory puts the action on faces: a sum over plaquettes of a class
function of the holonomy around each one, with a fixed coupling per face on a fixed
lattice. This module builds the same object on the attention network, where no
lattice is given and the faces have to come from somewhere.

They come from the attention. A face is a simple directed cycle of the interaction
skeleton, and its coupling is the probability that the attention walk traverses it,
the product of the directed row weights around the loop. A face whose loop contains
an unattended edge has zero weight and does not exist, and a long loop is suppressed
geometrically in its length because each step costs another factor below one. That
is the sense in which the attention weights say which plaquettes are present and how
much each one counts.

Two properties make this legitimate rather than decorative. The weights are built
from the directed attention rows alone, and in this laboratory those rows are
declared constants that no gauge transformation reads, so the action is gauge
invariant even though the holonomy is not gauge invariant edgewise. That is an
argument from the declaration and not from a property of attention: in the wider
program the rows are built from divergences between transported beliefs, and there
the invariance of the coupling is a theorem to prove rather than one to inherit. And
the defect is a class function of the holonomy, so it vanishes exactly on a flat face
and does not depend on where the loop is based.

One difference from the lattice case is structural and should not be glossed. There
the plaquette coupling is a declared constant; here it is the attention, which is a
variable of the model. The action can therefore be lowered in two ways, by
flattening the connection or by withdrawing attention from a curved loop, and those
are physically different resolutions. This module computes the action and its
decomposition by face; it does not decide which resolution the dynamics should take.

The face set is the set of simple directed cycles, which on a general graph can be
larger than the cycle rank. When it is, the faces are not independent and the
holonomies satisfy relations inherited from the cycle space; the count is reported
so that redundancy is visible rather than assumed away.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Sequence

import numpy as np

from .categorical_falsification_model import FalsificationModel

CHANNELS = ("belief", "model")


@dataclass(frozen=True)
class Plaquette:
    """One face of the attention network, with its holonomy and its couplings."""

    cycle: tuple[int, ...]
    edges: tuple[int, ...]
    belief_holonomy: int
    model_holonomy: int
    belief_weight: float
    model_weight: float

    @property
    def length(self) -> int:
        """Return the number of arcs bounding the face."""
        return len(self.cycle)

    def holonomy(self, channel: str) -> int:
        """Return the holonomy of one channel around this face."""
        if channel == "belief":
            return self.belief_holonomy
        if channel == "model":
            return self.model_holonomy
        raise ValueError("channel must be 'belief' or 'model'")

    def weight(self, channel: str) -> float:
        """Return the attention coupling of one channel on this face."""
        if channel == "belief":
            return self.belief_weight
        if channel == "model":
            return self.model_weight
        raise ValueError("channel must be 'belief' or 'model'")


def _arc_index(model: FalsificationModel) -> dict[tuple[int, int], int]:
    """Return the edge index of every declared arc, keyed source then receiver."""
    return {
        (edge.source, edge.receiver): index
        for index, edge in enumerate(model.graph.edges)
    }


@lru_cache(maxsize=None)
def simple_directed_cycles(model: FalsificationModel) -> tuple[tuple[int, ...], ...]:
    """Return every simple directed cycle of the skeleton, each listed once.

    A cycle is reported starting from its smallest vertex, which makes the listing
    canonical and prevents the same face appearing once per rotation. Self loops
    are excluded because a face needs at least two distinct arcs.
    """
    arcs = _arc_index(model)
    successors: dict[int, list[int]] = {}
    for source, receiver in arcs:
        if source != receiver:
            successors.setdefault(source, []).append(receiver)
    for values in successors.values():
        values.sort()
    found: list[tuple[int, ...]] = []

    def walk(start: int, node: int, path: list[int], seen: frozenset[int]) -> None:
        for following in successors.get(node, ()):
            if following == start and len(path) >= 2:
                found.append(tuple(path))
            elif following not in seen and following > start:
                walk(start, following, path + [following], seen | {following})

    for vertex in sorted(model.graph.vertices):
        walk(vertex, vertex, [vertex], frozenset({vertex}))
    return tuple(sorted(found))


def cycle_edges(
    model: FalsificationModel,
    cycle: Sequence[int],
) -> tuple[int, ...]:
    """Return the edge indices bounding one directed cycle, in traversal order."""
    arcs = _arc_index(model)
    size = len(cycle)
    return tuple(
        arcs[(cycle[position], cycle[(position + 1) % size])] for position in range(size)
    )


def cycle_holonomy(
    model: FalsificationModel,
    cycle: Sequence[int],
    channel: str,
) -> int:
    """Return the holonomy group element accumulated around one directed cycle."""
    elements = model.graph.channel_elements(channel)
    total = sum(elements[index] for index in cycle_edges(model, cycle))
    return total % model.graph.order


def cycle_attention_weight(
    model: FalsificationModel,
    cycle: Sequence[int],
    channel: str,
    configuration: str,
) -> float:
    """Return the probability that the attention walk traverses one directed cycle.

    The weight is the product of the directed row entries around the loop, so an
    unattended arc removes the face entirely and a long loop is suppressed
    geometrically in its length. The rows are gauge-invariant scalars, which is what
    makes the resulting action gauge invariant.
    """
    rows = model.attention_rows(configuration)[channel]
    position_of = {agent: index for index, agent in enumerate(model.agents)}
    size = len(cycle)
    weight = 1.0
    for step in range(size):
        source = cycle[step]
        receiver = cycle[(step + 1) % size]
        weight *= float(rows[position_of[receiver], position_of[source]])
    return weight


def wilson_defect(model: FalsificationModel, element: int, channel: str) -> float:
    r"""Return the Z_n flatness indicator of a holonomy element, a class function.

    The representation permutes the finite sample space, so one minus its normalized
    permutation character counts the fixed points that a shift destroys. On a
    faithful cyclic action every nontrivial element moves the whole sample space, so
    the value is the indicator [U_p != identity], the delta-function action of the
    finite gauge theory rather than the Wilson plaquette term 1 - Re chi(U_p). The two
    agree up to a scale only at n = 3, where the indicator reads 0, 1, 1 and the
    character defect reads 0, 3/2, 3/2; at larger n the indicator is blind to how far
    from the identity a holonomy sits, which is a declared choice of action and not an
    approximation to the character one.

    Faithfulness is required rather than assumed. An unfaithful representation sends
    some nontrivial group element to the identity permutation, and the defect would
    then report a curved face as flat, so any reading of this quantity as a curvature
    magnitude would be measuring the kernel of the representation instead.
    """
    representation = (
        model.belief_representation if channel == "belief" else model.model_representation
    )
    if not representation.is_faithful():
        raise ValueError("the flatness indicator needs a faithful representation")
    order = model.graph.order
    permutation = representation.permutation(element % order)
    fixed = sum(1 for position, image in enumerate(permutation) if position == image)
    return 1.0 - fixed / float(order)


@lru_cache(maxsize=None)
def plaquettes(
    model: FalsificationModel,
    configuration: str,
) -> tuple[Plaquette, ...]:
    """Return every face of the attention network with its holonomies and couplings."""
    faces: list[Plaquette] = []
    for cycle in simple_directed_cycles(model):
        faces.append(
            Plaquette(
                cycle=cycle,
                edges=cycle_edges(model, cycle),
                belief_holonomy=cycle_holonomy(model, cycle, "belief"),
                model_holonomy=cycle_holonomy(model, cycle, "model"),
                belief_weight=cycle_attention_weight(
                    model, cycle, "belief", configuration
                ),
                model_weight=cycle_attention_weight(
                    model, cycle, "model", configuration
                ),
            )
        )
    return tuple(faces)


def wilson_action(
    model: FalsificationModel,
    configuration: str,
    channel: str,
) -> float:
    """Return the attention-weighted Wilson action of one channel.

    The action is the sum over faces of the attention coupling times the holonomy
    defect. It is nonnegative, vanishes exactly when every attended face is flat,
    and is invariant under regauging because both factors are.
    """
    return float(
        sum(
            face.weight(channel) * wilson_defect(model, face.holonomy(channel), channel)
            for face in plaquettes(model, configuration)
        )
    )


def action_by_face(
    model: FalsificationModel,
    configuration: str,
    channel: str,
) -> tuple[tuple[tuple[int, ...], float], ...]:
    """Return the per-face contribution to the Wilson action, largest first."""
    contributions = [
        (
            face.cycle,
            face.weight(channel) * wilson_defect(model, face.holonomy(channel), channel),
        )
        for face in plaquettes(model, configuration)
    ]
    return tuple(sorted(contributions, key=lambda item: (-item[1], item[0])))


def attended_faces(
    model: FalsificationModel,
    configuration: str,
    channel: str,
    threshold: float = 0.0,
) -> tuple[tuple[int, ...], ...]:
    """Return the faces carrying attention above a declared threshold.

    A face below the threshold contributes nothing the dynamics can feel, so this
    is the operational face set: which plaquettes the attention says exist.
    """
    return tuple(
        face.cycle
        for face in plaquettes(model, configuration)
        if face.weight(channel) > threshold
    )


def faces_inside(
    model: FalsificationModel,
    block: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    """Return the faces lying entirely within one block.

    A face straddling a block boundary is not a face of that block's parent, so it
    is not charged to it. Which faces survive a partition is therefore a property
    of the partition, and cutting a curved face removes its cost entirely.
    """
    members = set(block)
    return tuple(
        cycle for cycle in simple_directed_cycles(model) if set(cycle) <= members
    )


def block_wilson_action(
    model: FalsificationModel,
    block: Sequence[int],
    configuration: str,
) -> float:
    """Return the Wilson action carried by the faces internal to one block.

    Both channels are summed, since a parent must reconcile the loops of each. The
    quantity depends only on the connection and the attention, not on the agent
    states, so it enters a block energy as a constant offset.
    """
    internal = set(faces_inside(model, block))
    return float(
        sum(
            face.weight(channel) * wilson_defect(model, face.holonomy(channel), channel)
            for face in plaquettes(model, configuration)
            for channel in CHANNELS
            if face.cycle in internal
        )
    )


def partition_wilson_action(
    model: FalsificationModel,
    partition: Sequence[Sequence[int]],
    configuration: str,
) -> float:
    """Return the Wilson action retained by a partition, summed over its blocks."""
    return float(
        sum(block_wilson_action(model, block, configuration) for block in partition)
    )


def cut_faces(
    model: FalsificationModel,
    partition: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    """Return the faces no block of the partition contains.

    These are the loops the partition severs. Their curvature is not carried by any
    parent, which is the sense in which a partition can dispose of curvature rather
    than pay for it.
    """
    kept = {cycle for block in partition for cycle in faces_inside(model, block)}
    return tuple(
        cycle for cycle in simple_directed_cycles(model) if cycle not in kept
    )


def face_count_versus_cycle_rank(model: FalsificationModel) -> tuple[int, int]:
    """Return the number of faces and the cycle rank, so redundancy stays visible.

    Equality means the faces form a basis of the cycle space. A larger face count
    means the holonomies satisfy relations and the faces are not independent, which
    is a property of the skeleton rather than a defect.
    """
    vertices = len(model.graph.vertices)
    edges = len(model.graph.edges)
    return len(simple_directed_cycles(model)), edges - vertices + 1


__all__ = [
    "CHANNELS",
    "Plaquette",
    "action_by_face",
    "attended_faces",
    "block_wilson_action",
    "cut_faces",
    "faces_inside",
    "partition_wilson_action",
    "cycle_attention_weight",
    "cycle_edges",
    "cycle_holonomy",
    "face_count_versus_cycle_rank",
    "plaquettes",
    "simple_directed_cycles",
    "wilson_action",
    "wilson_defect",
]
