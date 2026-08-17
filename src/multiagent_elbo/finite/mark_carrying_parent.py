"""The retention alternative: a curved block forms a parent that carries its marks.

The stabilized route excludes a block whose holonomy fixes no admitted
presentation. That exclusion is stronger than the theory requires. Proposition 8
yields an infinite mark-free score and a strictly positive block-formation floor,
not an infinite block energy, and the block-formation hypothesis is a disjunction:
either the fixed sector is nonempty, or the parent retains the connection data and
forms anyway. This module implements the second branch.

The retained datum is the simultaneous root-framed equivariant state, a root
presentation, the based holonomy representation, and the dressed boundary
generators,

    (zbar_I, H_I, {V_e}),   V_e = tau_{I<-i} Theta_e (tau_{J<-j})^{-1},

taken as one root-gauge orbit rather than as three separately quotiented pieces.
Quotienting the holonomy by conjugacy on its own would lose its orientation
relative to the root frame and the boundary legs, so the orbit is formed under the
simultaneous action of a root gauge on every component at once.

For the abelian structure group used here the conjugation action on the holonomy is
trivial, so the holonomy is a gauge invariant and the orbit content lives in the
root presentation and the boundary generators, which shift together under a root
regauging. That degeneracy is a property of this group, not of the construction,
and the simultaneous quotient is implemented rather than assumed away.

What the marks buy is coherence without stabilization. A tree path from the root
reaches each member exactly once, so the transported prediction is well defined for
any root presentation; what fails on a curved block is loop closure, and the
holonomy mark records that failure instead of treating it as an error. The parent
therefore exists for every block. What it costs is capacity: the parent state space
must be large enough to carry the marks, and under a capacity bound that is charged
against the presentation it could otherwise have spent those states on. The charge
is declared here, not derived, and the price is an explicit parameter so that the
competition between the two routes can be read off rather than asserted.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import math
from typing import Sequence

import numpy as np

from .categorical_falsification_model import (
    FalsificationModel,
    Partition,
    kl_laws,
    transported,
)
from .holonomy_retention import block_holonomy_group, block_transport_elements
from .holonomy_selection import admissible_parent_states, _parent_laws
from .partition_dynamics import _log_partition_prior

CHANNELS = ("belief", "model")


@dataclass(frozen=True)
class MarkDatum:
    """The retained connection data of one block in one channel.

    The root presentation is an index into the declared parent family, the
    holonomy is the based holonomy group of the block at its root, and the
    boundary generators are the dressed transports of the edges leaving the block,
    keyed by the ordered endpoint pair. All three are carried together because only
    the simultaneous root-gauge orbit is a legitimate quotient.
    """

    block: tuple[int, ...]
    channel: str
    root: int
    presentation: int
    holonomy: tuple[int, ...]
    boundary: tuple[tuple[tuple[int, int], int], ...]


def _boundary_edges(model: FalsificationModel, block: Sequence[int]) -> tuple:
    """Return the declared edges with exactly one endpoint inside the block."""
    members = set(block)
    return tuple(
        (index, edge)
        for index, edge in enumerate(model.graph.edges)
        if (edge.receiver in members) != (edge.source in members)
    )


def mark_datum(
    model: FalsificationModel,
    block: Sequence[int],
    channel: str,
    presentation: int,
) -> MarkDatum:
    """Return the retained root-framed datum of one block in one channel.

    The dressed boundary generator of an edge leaving the block is the microscopic
    transport conjugated by the tree transports of its endpoints, which is the
    boundary leg expressed in the root frame. An endpoint outside the block is
    framed by itself, so its tree contribution is the identity.
    """
    members = tuple(block)
    root = min(members)
    transports = block_transport_elements(model, members, channel)
    elements = model.graph.channel_elements(channel)
    order = model.graph.order
    boundary: list[tuple[tuple[int, int], int]] = []
    for index, edge in _boundary_edges(model, members):
        inside_receiver = transports.get(edge.receiver, 0)
        inside_source = transports.get(edge.source, 0)
        dressed = (inside_receiver + elements[index] - inside_source) % order
        boundary.append(((edge.receiver, edge.source), dressed))
    return MarkDatum(
        block=members,
        channel=channel,
        root=root,
        presentation=int(presentation),
        holonomy=block_holonomy_group(model, members, channel),
        boundary=tuple(sorted(boundary)),
    )


def regauge(model: FalsificationModel, datum: MarkDatum, shift: int) -> MarkDatum:
    """Apply one root gauge simultaneously to every component of the datum.

    The root presentation is pushed forward by the gauge, the boundary generators
    absorb it on their inside leg, and the holonomy is unchanged because the group
    is abelian and conjugation is trivial. Applying the gauge to the presentation
    alone, or to the boundary alone, would not be a legitimate quotient.
    """
    order = model.graph.order
    representation = (
        model.belief_representation
        if datum.channel == "belief"
        else model.model_representation
    )
    pairs = _parent_laws(model, False)
    law = pairs[datum.presentation][0 if datum.channel == "belief" else 1]
    moved = representation.act(shift % order, law)
    family = model.belief_family if datum.channel == "belief" else model.model_family
    position = family.index(moved)
    size = len(model.model_family)
    if datum.channel == "belief":
        presentation = position * size + (datum.presentation % size)
    else:
        presentation = (datum.presentation // size) * size + position
    boundary = tuple(
        sorted(
            (endpoints, (dressed - shift) % order)
            for endpoints, dressed in datum.boundary
        )
    )
    return MarkDatum(
        block=datum.block,
        channel=datum.channel,
        root=datum.root,
        presentation=presentation,
        holonomy=datum.holonomy,
        boundary=boundary,
    )


def root_gauge_orbit(
    model: FalsificationModel,
    datum: MarkDatum,
) -> tuple[MarkDatum, ...]:
    """Return the simultaneous root-gauge orbit of one retained datum."""
    return tuple(
        sorted(
            {regauge(model, datum, shift) for shift in range(model.graph.order)},
            key=lambda item: (item.presentation, item.boundary),
        )
    )


def orbit_representative(model: FalsificationModel, datum: MarkDatum) -> MarkDatum:
    """Return the canonical member of the simultaneous root-gauge orbit."""
    return root_gauge_orbit(model, datum)[0]


@lru_cache(maxsize=None)
def mark_space_size(
    model: FalsificationModel,
    block: tuple[int, ...],
    channel: str,
) -> int:
    """Return how many distinct loop transports the parent must resolve.

    A flat block has a single loop transport and needs no resolution, so its mark
    space is one and it is charged nothing. A block whose holonomy group is the
    whole structure group must distinguish every element to reproduce transport
    around its loops.
    """
    return len(block_holonomy_group(model, block, channel))


def mark_retention_cost(
    model: FalsificationModel,
    block: Sequence[int],
) -> float:
    """Return the declared capacity charged for retaining a block's marks.

    The charge is the log of the number of holonomy elements the parent must
    resolve, summed over channels, so a flat block is free and a fully curved block
    in one channel pays the log of the structure group's order. This is a declared
    modeling price, not a quantity derived from the free energy, and it exists so
    the competition between the stabilized and mark-carrying routes is explicit
    rather than hidden in a choice of parent space.
    """
    members = tuple(block)
    return sum(
        math.log(mark_space_size(model, members, channel)) for channel in CHANNELS
    )


@lru_cache(maxsize=None)
def _unrestricted_cost_table(
    model: FalsificationModel,
    block: tuple[int, ...],
) -> np.ndarray:
    """Return the transported mismatch over the whole declared parent family.

    The mark-carrying route does not restrict the parent to the stabilized sector,
    because the holonomy is retained rather than required to act trivially. Only
    the tree frames enter the prediction, which is exactly why a parent exists for
    every block.
    """
    pairs = _parent_laws(model, False)
    belief_shift = block_transport_elements(model, block, "belief")
    model_shift = block_transport_elements(model, block, "model")
    order = model.graph.order
    table = np.zeros((len(pairs), len(block), model.state_count), dtype=np.float64)
    for row, (parent_belief, parent_model) in enumerate(pairs):
        for column, agent in enumerate(block):
            target_belief = transported(
                model.belief_representation,
                (-belief_shift[agent]) % order,
                parent_belief,
            )
            target_model = transported(
                model.model_representation,
                (-model_shift[agent]) % order,
                parent_model,
            )
            for child in range(model.state_count):
                belief, law = model.state_pair(child)
                cost = model.kappa_belief * kl_laws(belief, target_belief)
                cost += model.kappa_model * kl_laws(law, target_model)
                table[row, column, child] = cost
    return table


def mark_carrying_block_energy(
    model: FalsificationModel,
    block: Sequence[int],
    states: Sequence[int],
    mark_price: float,
) -> float:
    """Return the block energy of the retention route, including its capacity charge.

    The transported mismatch is minimized over the whole declared parent family
    rather than over the stabilized sector, and the declared retention charge is
    added. The result is finite for every block, which is the point of the route.
    """
    members = tuple(block)
    index_of = {agent: position for position, agent in enumerate(model.agents)}
    table = _unrestricted_cost_table(model, members)
    picks = [states[index_of[agent]] for agent in members]
    costs = table[:, np.arange(len(members)), picks].sum(axis=1)
    return float(costs.min()) + mark_price * mark_retention_cost(model, members)


def stabilized_block_energy(
    model: FalsificationModel,
    block: Sequence[int],
    states: Sequence[int],
) -> float:
    """Return the block energy of the stabilized route, infinite where it fails."""
    members = tuple(block)
    parents = admissible_parent_states(model, members, False)
    if not parents:
        return float("inf")
    index_of = {agent: position for position, agent in enumerate(model.agents)}
    table = _unrestricted_cost_table(model, members)
    picks = [states[index_of[agent]] for agent in members]
    costs = table[list(parents)][:, np.arange(len(members)), picks].sum(axis=1)
    return float(costs.min())


@dataclass(frozen=True)
class RouteChoice:
    """Which of the two parent routes a block takes, and at what cost."""

    block: tuple[int, ...]
    stabilized_energy: float
    mark_carrying_energy: float
    retention_cost: float
    route: str


def block_route(
    model: FalsificationModel,
    block: Sequence[int],
    states: Sequence[int],
    mark_price: float,
) -> RouteChoice:
    """Return the cheaper of the two parent routes for one block."""
    stabilized = stabilized_block_energy(model, block, states)
    marked = mark_carrying_block_energy(model, block, states, mark_price)
    route = "stabilized" if stabilized <= marked else "mark_carrying"
    return RouteChoice(
        block=tuple(block),
        stabilized_energy=stabilized,
        mark_carrying_energy=marked,
        retention_cost=mark_retention_cost(model, block),
        route=route,
    )


def retained_block_energy(
    model: FalsificationModel,
    partition: Partition,
    states: Sequence[int],
    mark_price: float,
) -> float:
    """Return the partition energy when each block takes its cheaper route.

    Because the retention route is always available, this energy is finite for
    every partition, so no partition is excluded outright. The obstruction now acts
    as a price rather than as a prohibition, which is the disjunction the theory
    states rather than the harder condition the stabilized selector imposes.
    """
    return sum(
        min(
            stabilized_block_energy(model, block, states),
            mark_carrying_block_energy(model, block, states, mark_price),
        )
        for block in partition
    )


def retained_free_energy(
    model: FalsificationModel,
    partition: Partition,
    states: Sequence[int],
    mark_price: float,
) -> float:
    """Return the retained block energy plus the declared partition prior term."""
    energy = retained_block_energy(model, partition, states, mark_price)
    return energy - _log_partition_prior(model, partition)


def selected_partition(
    model: FalsificationModel,
    states: Sequence[int],
    mark_price: float,
) -> Partition:
    """Return the partition minimizing the retained free energy at one configuration."""
    return min(
        model.candidate_partitions,
        key=lambda partition: retained_free_energy(
            model, partition, states, mark_price
        ),
    )


def marginal_partition_posterior(
    model: FalsificationModel,
    mark_price: float,
    states: Sequence[Sequence[int]],
) -> dict[Partition, float]:
    """Return the partition posterior marginalized over a declared state sample."""
    logs: dict[Partition, float] = {}
    for partition in model.candidate_partitions:
        energies = np.array(
            [
                retained_free_energy(model, partition, configuration, mark_price)
                for configuration in states
            ]
        )
        shift = energies.min()
        logs[partition] = float(np.log(np.exp(-(energies - shift)).sum()) - shift)
    values = np.array([logs[p] for p in model.candidate_partitions])
    weights = np.exp(values - values.max())
    weights /= weights.sum()
    return {p: float(w) for p, w in zip(model.candidate_partitions, weights)}


__all__ = [
    "CHANNELS",
    "MarkDatum",
    "RouteChoice",
    "block_route",
    "mark_carrying_block_energy",
    "mark_datum",
    "mark_retention_cost",
    "mark_space_size",
    "marginal_partition_posterior",
    "orbit_representative",
    "regauge",
    "retained_block_energy",
    "retained_free_energy",
    "root_gauge_orbit",
    "selected_partition",
    "stabilized_block_energy",
]
