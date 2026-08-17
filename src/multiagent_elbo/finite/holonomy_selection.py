"""Partition selection driven by the holonomy stabilization condition.

The measured defect this module repairs is specific. The downward kernel of the
first laboratory carries a parent to each child along a spanning tree, and a
spanning tree contains no cycles, so the chord edges never enter the block energy.
Varying a chord while holding the tree transports fixed moves the holonomy group
from the whole structure group to the trivial group, moves the holonomy
obstruction from positive infinity to about one tenth, and moves that block energy
by about two parts in ten thousand, the exact figure depending on which state
configuration the comparison is made at. The energy is therefore blind to holonomy and
sensitive only to the tree transports, which a rechoice of parent state can
largely absorb. That is backwards: the tree transports are the gauge-like part and
the holonomy is the gauge-invariant part.

The repair makes the stabilization condition select, rather than merely score. A
parent presentation is admissible for a block only if every based loop transport
of that block fixes it, which is the condition H_# Q = Q read as a restriction on
the parent space. A block whose holonomy group has no fixed point among the
admitted presentations then has no coherent parent at all, its energy is positive
infinity, and every partition containing it is excluded before any energy
comparison happens.

Describing that as a restriction on the support of the downward kernel would be
ill-typed, and the earlier phrasing of this module said exactly that. A Markov
kernel must be a probability measure for every value of its conditioning
variables, whereas stabilization constrains the parent, which is a conditioning
variable and not an outcome; and in the declared generative order the parent is
sampled before the partition, so no later factor could restrict it in any case.
The object actually implemented is a reordered depth-one tower: the partition is
drawn first from an admissibility-conditioned prior, each occupied parent label
then draws its presentation uniformly on the stabilized sector, which is nonempty
by that conditioning, and the children follow the declared Gibbs kernel. Every
factor is a normalized kernel on finite spaces and conditions only on strictly
earlier variables, so the tower normalizes and an infinite energy is exactly zero
prior mass on that partition. The reordering is a redeclared model, not a
rearrangement of the frozen one.

Three consequences follow, and none of them is cosmetic. The selection is a
declared capacity restriction wearing a support condition's clothes, which is what
Corollary 6 says any nondegenerate selection must be; it does not escape the
partition-degeneracy result and does not derive from the gauge structure alone.
The hard exclusion is also stronger than Proposition 8, which yields an infinite
mark-free score and a strictly positive energy floor, not an infinite block
energy; excluding the block outright forecloses the retention alternative in which
a curved block still forms a parent that carries its holonomy marks. And because
the partition prior is not renormalized over the admissible set, the returned
numbers are free energies only up to a partition-independent constant: differences
and the induced posterior are meaningful, the raw values are not evidence bounds
and must not be quoted beside the unconstrained laboratory's.

Two parent spaces are offered because they separate a hard mechanism from a soft
one. The declared presentation family excludes the uniform law, so a nontrivial
holonomy empties the fixed sector and the exclusion is absolute. Augmenting the
parent space with the uniform law makes the fixed sector nonempty for every block,
so the obstruction becomes a finite energy difference instead; that variant also
enlarges parent capacity, which is a declared modeling change and not a free one.

Two consequences of that choice must be read with the mechanism rather than after
it. First, the augmented space is the orbit family together with the uniform law,
which is a third family and not the frozen specification's declared pair of the
orbit family and the whole simplex. It agrees with the simplex fixed sector on a
block carrying nontrivial holonomy, where that sector is the uniform law alone,
and disagrees on a flat block, where the simplex fixed sector is the whole
simplex. Second, admitting the uniform law does not merely soften the exclusion,
it inverts the outcome: by exact enumeration over all state configurations the
modal partition moves from the five-plus-one split at posterior mass 0.861 to the
single six-agent block at 0.605, because the declared partition prior favors large
blocks and a uniform parent's finite energy floor is cheaper than that prior gap.
The selection reported here is therefore conditional on the declared family, and
the condition is load bearing rather than incidental. Third, the augmented path is
a composite potential and not an exact free energy of any declared normalized law:
once the uniform law is admitted the child kernel normalizer takes several
distinct values across parents and the stabilized sector changes size across
blocks, so the omitted normalizer and sector-size terms no longer cancel between
partitions. Only the unaugmented path carries the free-energy reading, and even
there only up to a partition-independent constant.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Mapping, Sequence

import numpy as np

from .categorical_falsification_model import (
    FalsificationModel,
    Partition,
    kl_laws,
    transported,
)
from .holonomy_retention import block_holonomy_group, block_transport_elements
from .partition_dynamics import (
    PARTITION_MOVE_PROBABILITY,
    _log_partition_prior,
)
from .two_channel_gauge import uniform_law

RESIDENCE_RATIO_THRESHOLD = 10.0


@dataclass(frozen=True)
class SelectionTrace:
    """One coupled descent run under the holonomy-constrained energy."""

    model_name: str
    seed: int
    noise: float
    steps: int
    partitions: tuple[Partition, ...]
    admissible: tuple[Partition, ...]


@dataclass(frozen=True)
class SelectionReport:
    """Block-formation statistics under the holonomy-constrained energy."""

    model_name: str
    augmented: bool
    admissible_partitions: tuple[Partition, ...]
    forbidden_partitions: tuple[Partition, ...]
    modal_partition: Partition
    modal_occupancy: float
    residence_times: tuple[tuple[Partition, float], ...]
    maximum_residence_time: float
    co_membership: tuple[tuple[float, ...], ...]
    largest_off_diagonal_co_membership: float


def _parent_laws(model: FalsificationModel, augmented: bool) -> tuple[tuple, ...]:
    """Return the declared parent presentation pairs, optionally with the uniform law.

    The augmented space is the orbit family together with the uniform law. It is
    not the frozen specification's simplex family: it agrees with the simplex fixed
    sector on a block with nontrivial holonomy, where that sector is the uniform law
    alone, and disagrees on a flat block, where that sector is the whole simplex.
    """
    beliefs = list(model.belief_family)
    models = list(model.model_family)
    if augmented:
        order = model.graph.order
        beliefs.append(uniform_law(order))
        models.append(uniform_law(order))
    return tuple((belief, law) for belief in beliefs for law in models)


@lru_cache(maxsize=None)
def admissible_parent_states(
    model: FalsificationModel,
    block: tuple[int, ...],
    augmented: bool = False,
) -> tuple[int, ...]:
    """Return the parent presentations stabilized by the whole block holonomy.

    A presentation is admissible when every based loop transport of the block
    fixes it in its own channel, which is the stabilization condition read as a
    restriction on the parent space rather than as a penalty. An empty result means
    the block admits no coherent parent and is therefore not a candidate block.
    """
    belief_group = block_holonomy_group(model, block, "belief")
    model_group = block_holonomy_group(model, block, "model")
    pairs = _parent_laws(model, augmented)
    admissible: list[int] = []
    for index, (belief, law) in enumerate(pairs):
        if not all(
            model.belief_representation.fixes(element, belief)
            for element in belief_group
        ):
            continue
        if not all(
            model.model_representation.fixes(element, law) for element in model_group
        ):
            continue
        admissible.append(index)
    return tuple(admissible)


@lru_cache(maxsize=None)
def _block_cost_table(
    model: FalsificationModel,
    block: tuple[int, ...],
    augmented: bool,
) -> np.ndarray:
    """Return the per-agent transported mismatch, indexed by parent then child state.

    The entry is the divergence of a child presentation from the parent
    presentation carried into that child's frame along the block spanning tree.
    Only admissible parents are tabulated, so the tree transports still set the
    frames while the holonomy sets which parents exist at all.

    On a disconnected block each component is framed by its own spanning tree and
    the components are aligned by the identity. The holonomy retention module
    instead infimizes over the relative alignments of the component roots, so the
    two modules compute different finite scores on disconnected blocks while
    agreeing on the exclusion set, which is all that selection uses. Collapsing the
    component roots this way is the further declared coarse channel the theory
    requires for a disconnected parent, and it is declared here rather than derived.
    """
    parents = admissible_parent_states(model, block, augmented)
    pairs = _parent_laws(model, augmented)
    belief_shift = block_transport_elements(model, block, "belief")
    model_shift = block_transport_elements(model, block, "model")
    order = model.graph.order
    table = np.zeros((len(parents), len(block), model.state_count), dtype=np.float64)
    for row, parent in enumerate(parents):
        parent_belief, parent_model = pairs[parent]
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


def constrained_block_energy(
    model: FalsificationModel,
    partition: Partition,
    states: Sequence[int],
    augmented: bool = False,
) -> float:
    """Return the block energy with the parent restricted to the stabilized sector.

    The energy of a block is the transported mismatch minimized over its admissible
    parents. A block with no admissible parent contributes positive infinity, so
    every partition containing it is excluded rather than merely disfavored.
    """
    index_of = {agent: position for position, agent in enumerate(model.agents)}
    total = 0.0
    for block in partition:
        parents = admissible_parent_states(model, tuple(block), augmented)
        if not parents:
            return float("inf")
        table = _block_cost_table(model, tuple(block), augmented)
        picks = [states[index_of[agent]] for agent in block]
        costs = table[:, np.arange(len(block)), picks].sum(axis=1)
        total += float(costs.min())
    return total


def constrained_free_energy(
    model: FalsificationModel,
    partition: Partition,
    states: Sequence[int],
    augmented: bool = False,
) -> float:
    """Return the constrained block energy plus the declared partition prior term.

    The partition prior is the raw declared mass and is not renormalized over the
    admissible set, so the returned number is a free energy only up to a constant
    that does not depend on the partition. Differences between partitions and the
    posterior induced by them are meaningful; the raw values are not evidence
    bounds and must not be quoted beside the unconstrained laboratory's.
    """
    energy = constrained_block_energy(model, partition, states, augmented)
    if energy == float("inf"):
        return float("inf")
    return energy - _log_partition_prior(model, partition)


def admissible_partitions(
    model: FalsificationModel,
    augmented: bool = False,
) -> tuple[Partition, ...]:
    """Return the candidate partitions whose every block admits a coherent parent."""
    return tuple(
        partition
        for partition in model.candidate_partitions
        if all(
            admissible_parent_states(model, tuple(block), augmented)
            for block in partition
        )
    )


def constrained_descent(
    model: FalsificationModel,
    seed: int,
    noise: float,
    steps: int = 300,
    augmented: bool = False,
) -> SelectionTrace:
    """Run the coupled Metropolis dynamics on the holonomy-constrained free energy.

    The chain is the one used by the unconstrained laboratory, with proposals into
    a partition carrying an inadmissible block rejected outright because their
    energy is infinite. The chain is started on an admissible partition so that the
    initial energy is finite.
    """
    if type(steps) is not int or steps < 1:
        raise ValueError("steps must be a positive integer")
    if not noise > 0.0:
        raise ValueError("noise must be positive")
    candidates = admissible_partitions(model, augmented)
    if not candidates:
        raise ValueError("no candidate partition admits a coherent parent")
    generator = np.random.default_rng(seed)
    count = len(candidates)
    index = int(generator.integers(count))
    states = generator.integers(0, model.state_count, len(model.agents)).astype(np.int64)
    current = constrained_free_energy(model, candidates[index], states, augmented)
    recorded: list[Partition] = []
    for _ in range(steps):
        if count > 1 and generator.random() < PARTITION_MOVE_PROBABILITY:
            proposed_index = (index + 1 + int(generator.integers(count - 1))) % count
            proposed_states = states
        else:
            proposed_index = index
            proposed_states = states.copy()
            agent = int(generator.integers(len(model.agents)))
            shift = 1 + int(generator.integers(model.state_count - 1))
            proposed_states[agent] = (states[agent] + shift) % model.state_count
        candidate = constrained_free_energy(
            model, candidates[proposed_index], proposed_states, augmented
        )
        gap = candidate - current
        if gap <= 0.0 or generator.random() < np.exp(-min(gap, 700.0) / noise):
            index, states, current = proposed_index, proposed_states, candidate
        recorded.append(candidates[index])
    return SelectionTrace(
        model_name=model.name,
        seed=int(seed),
        noise=float(noise),
        steps=steps,
        partitions=tuple(recorded),
        admissible=candidates,
    )


def selection_report(
    model: FalsificationModel,
    seed: int,
    noise: float = 1.0,
    steps: int = 300,
    initializations: int = 200,
    augmented: bool = False,
) -> SelectionReport:
    """Measure the block-formation statistics under the constrained energy."""
    traces = [
        constrained_descent(model, seed + offset, noise, steps, augmented)
        for offset in range(initializations)
    ]
    counts: dict[Partition, int] = {}
    sojourns: dict[Partition, list[int]] = {}
    for trace in traces:
        run = 1
        for position, partition in enumerate(trace.partitions):
            counts[partition] = counts.get(partition, 0) + 1
            if position + 1 < len(trace.partitions) and (
                trace.partitions[position + 1] == partition
            ):
                run += 1
            else:
                sojourns.setdefault(partition, []).append(run)
                run = 1
    total = sum(counts.values())
    residence = {
        partition: float(np.mean(values)) for partition, values in sojourns.items()
    }
    modal = max(sorted(counts), key=lambda key: counts[key])
    size = len(model.agents)
    index_of = {agent: position for position, agent in enumerate(model.agents)}
    matrix = np.zeros((size, size), dtype=np.float64)
    for trace in traces:
        for partition in trace.partitions:
            for block in partition:
                for left in block:
                    for right in block:
                        matrix[index_of[left], index_of[right]] += 1.0
    matrix /= float(total)
    off_diagonal = matrix - np.diag(np.diag(matrix))
    admitted = admissible_partitions(model, augmented)
    forbidden = tuple(
        partition
        for partition in model.candidate_partitions
        if partition not in set(admitted)
    )
    return SelectionReport(
        model_name=model.name,
        augmented=bool(augmented),
        admissible_partitions=admitted,
        forbidden_partitions=forbidden,
        modal_partition=modal,
        modal_occupancy=float(counts[modal]) / float(total),
        residence_times=tuple(sorted(residence.items())),
        maximum_residence_time=float(max(residence.values())) if residence else 0.0,
        co_membership=tuple(tuple(float(value) for value in row) for row in matrix),
        largest_off_diagonal_co_membership=float(off_diagonal.max()),
    )


__all__ = [
    "SelectionReport",
    "SelectionTrace",
    "admissible_parent_states",
    "admissible_partitions",
    "constrained_block_energy",
    "constrained_descent",
    "constrained_free_energy",
    "selection_report",
]
