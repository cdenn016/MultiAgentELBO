"""Measurement M5, partition persistence on the finite categorical instance.

The partition posterior is the exact coordinate update of Proposition 4,

    Q_R(R) proportional to P_R(R) exp(-U(R)),   minimum value -log Z_R,

with the Ewens prior of the declared instance supplying P_R and the temperature
pinned at one. Nothing here introduces a free temperature: a tempered sector is a
different objective and mixing it into a reported free-energy number is an
accounting error, so the only number this module reports is the untempered one.

The block energy U(R) is **derived, not proposed**. Proposition 4 defines it as
exactly the sum of the conditional divergences that the choice of R controls,
which at depth one are the graph group, the holonomy group, and the cross-scale
group conditioned on R,

    U(R) = KL(Q_G || P_G(. | Z_1, R))
         + E_{Q_G}[ KL(Q_H || P_H) + E_{Q_H} KL(Q_0 || K_down) ].

A hand-written trade-off between internal mismatch and boundary retention is a
*proposal for* U, and it is an exact free-energy sector only if it happens to
equal the displayed sum for the declared P_G, P_H and K_down. This module never
writes such a trade-off; every term below is one of the three conditional
divergences, evaluated on the declared kernels of the instance.

Frozen recognition coordinates, declared once and used everywhere. U(R) is defined
at frozen values of every coordinate other than R, so those values are part of the
declaration rather than of the derivation. Q_0 is the point mass at the supplied
agent states, which is what makes the cross-scale group the negative log downward
kernel. Q_H is frozen at the declared generative weights, so the holonomy group
contributes exactly zero and the holonomy atoms enter only through the mixture
inside the cross-scale group. Q_G is frozen at the uniform law on the two declared
row configurations, which is the maximum-entropy choice and is independent of R,
so no partition preference is smuggled in through the recognition side. The parent
coordinate is a point mass at its own exact conditional optimum, which is the
minimization over the parent state named in the cross-scale term.

Every dynamical quantity here is measured, not bounded. The relaxation time is the
observed decay of the state-change rate, the residence time is an observed mean
sojourn, and the exit-time scaling is an observed least-squares fit. The two
pre-registered falsifiers are evaluated and reported as computed.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from typing import Optional, Sequence

import numpy as np

from .categorical_falsification_model import (
    FalsificationModel,
    Partition,
    build_null_model,
    build_reference_model,
    crp_partition_prior,
    kl_laws,
    transported,
)
from .two_channel_gauge import Law, tree_transport_elements

CALIBRATION_INITIALIZATIONS = 24
DESCENT_STEPS = 300
EXIT_STEP_BUDGET = 2000
INITIALIZATION_COUNT = 200
LINEARITY_R_SQUARED_THRESHOLD = 0.9
NULL_DESCENT_STEPS = 150
NULL_INITIALIZATION_COUNT = 60
PARTITION_MOVE_PROBABILITY = 0.5
REFERENCE_NOISE = 1.0
REFERENCE_NOISE_VALUES = (0.3, 0.4, 0.5, 0.7, 1.0, 1.5, 2.0)
RELAXATION_REPLICAS = 256
RELAXATION_SMOOTHING = 5
RELAXATION_WINDOW = 200
RESIDENCE_RATIO_THRESHOLD = 10.0


@dataclass(frozen=True)
class EnergyTerms:
    """Hold the three conditional-divergence groups that make up the derived U(R)."""

    graph_divergence: float
    holonomy_divergence: float
    cross_scale_divergence: float
    total: float
    parent_states: tuple[int, ...]


@dataclass(frozen=True)
class DescentTrace:
    """Hold one recorded coupled Metropolis run over partitions and agent states."""

    model_name: str
    seed: int
    noise: float
    steps: int
    partitions: tuple[Partition, ...]
    energies: tuple[float, ...]
    final_states: tuple[int, ...]
    acceptance_rate: float


@dataclass(frozen=True)
class ExitTimeFit:
    """Hold the mean exit times per noise value and the log-against-inverse-noise fit."""

    partition: Partition
    noise_values: tuple[float, ...]
    mean_exit_times: tuple[float, ...]
    censored_fraction: tuple[float, ...]
    step_budget: int
    slope: float
    intercept: float
    r_squared: float
    linearity_falsifier_fired: bool


@dataclass(frozen=True)
class PersistenceReport:
    """Hold every block-formation statistic measured on one model instance."""

    model_name: str
    seed: int
    noise: float
    steps: int
    initializations: int
    modal_partition: Partition
    modal_occupancy: float
    residence_times: tuple[tuple[Partition, float], ...]
    maximum_residence_time: float
    relaxation_time: float
    residence_ratio: float
    co_membership: tuple[tuple[float, ...], ...]
    largest_off_diagonal_co_membership: float
    timescale_falsifier_fired: bool
    exit_fit: Optional[ExitTimeFit]


@dataclass(frozen=True)
class NullControlReport:
    """Hold the reference statistics beside the null distribution of each of them."""

    seeds: tuple[int, ...]
    noise: float
    steps: int
    initializations: int
    reference: PersistenceReport
    nulls: tuple[PersistenceReport, ...]
    null_modal_occupancy: tuple[float, ...]
    null_maximum_residence_time: tuple[float, ...]
    null_relaxation_time: tuple[float, ...]
    null_residence_ratio: tuple[float, ...]
    null_largest_off_diagonal_co_membership: tuple[float, ...]
    null_timescale_falsifier_fired: tuple[bool, ...]


@dataclass(frozen=True)
class _PairTable:
    """Hold the ordered-pair arrays of one row configuration at the parent scale."""

    block_left: np.ndarray
    block_right: np.ndarray
    belief_element: np.ndarray
    model_element: np.ndarray
    belief_weight: np.ndarray
    model_weight: np.ndarray


@dataclass(frozen=True)
class _PartitionTables:
    """Hold the precomputed exact tables that evaluate U(R) for one partition."""

    blocks: tuple[tuple[int, ...], ...]
    positions: tuple[np.ndarray, ...]
    mixed_cost: np.ndarray
    pairs: tuple[_PairTable, ...]
    belief_kl: np.ndarray
    model_kl: np.ndarray
    kappa_belief: float
    kappa_model: float
    model_family_size: int


def _log_sum_exp(values: np.ndarray) -> np.ndarray:
    """Return the log of a sum of exponentials along the last axis, shifted for stability."""
    peak = values.max(axis=-1, keepdims=True)
    return (peak + np.log(np.exp(values - peak).sum(axis=-1, keepdims=True)))[..., 0]


def _component_transports(
    model: FalsificationModel,
    block: Sequence[int],
    channel: str,
) -> dict[int, int]:
    """Return the group element carrying each member frame to the block root frame.

    A block whose induced subgraph is disconnected carries no declared transport
    between its components, so each component is rooted at its own smallest member
    and the component roots are identified by the identity. On a connected block
    this agrees with the model's own spanning-tree transports exactly.
    """
    induced = model.graph.induced(block)
    members = tuple(sorted(block))
    adjacency: dict[int, set[int]] = {member: set() for member in members}
    for edge in induced.edges:
        adjacency[edge.receiver].add(edge.source)
        adjacency[edge.source].add(edge.receiver)
    transports: dict[int, int] = {}
    unassigned = set(members)
    while unassigned:
        root = min(unassigned)
        component = {root}
        frontier = [root]
        while frontier:
            current = frontier.pop()
            for neighbor in adjacency[current]:
                if neighbor not in component:
                    component.add(neighbor)
                    frontier.append(neighbor)
        subgraph = model.graph.induced(tuple(sorted(component)))
        transports.update(tree_transport_elements(subgraph, channel, root))
        unassigned -= component
    return transports


@lru_cache(maxsize=None)
def _downward_law(
    model: FalsificationModel,
    belief_shift: int,
    model_shift: int,
    parent_state: int,
) -> tuple[float, ...]:
    """Return the declared downward kernel at explicit per-channel transport elements.

    This is the kernel of the instance written with the transport elements exposed,
    so the identity atom of the holonomy variable can be evaluated on the same code
    path as the computed atom. At the computed elements of a connected block it
    reproduces the model's own downward kernel entry for entry.
    """
    order = model.graph.order
    parent_belief, parent_model = model.state_pair(parent_state)
    target_belief = transported(model.belief_representation, (-belief_shift) % order, parent_belief)
    target_model = transported(model.model_representation, (-model_shift) % order, parent_model)
    energies = np.empty(model.state_count, dtype=np.float64)
    for index in range(model.state_count):
        belief, presentation = model.state_pair(index)
        energies[index] = model.kappa_belief * kl_laws(belief, target_belief)
        energies[index] += model.kappa_model * kl_laws(presentation, target_model)
    energies -= energies.min()
    weights = np.exp(-energies)
    return tuple(float(value) for value in weights / weights.sum())


def downward_law(
    model: FalsificationModel,
    block: Sequence[int],
    agent: int,
    parent_state: int,
    flat: bool = False,
) -> np.ndarray:
    """Return the downward kernel of one agent under a declared holonomy atom.

    The computed atom uses the spanning-tree transports of the block and the
    identity atom replaces them by the identity, which is exactly the flatness
    assumption carried by the two-atom holonomy variable of the instance.
    """
    if type(flat) is not bool:
        raise TypeError("flat must be a bool")
    if flat:
        return np.array(_downward_law(model, 0, 0, parent_state), dtype=np.float64)
    belief_shift = _component_transports(model, block, "belief")[agent]
    model_shift = _component_transports(model, block, "model")[agent]
    return np.array(
        _downward_law(model, belief_shift, model_shift, parent_state),
        dtype=np.float64,
    )


@lru_cache(maxsize=None)
def _transport_kl_table(
    model: FalsificationModel,
    channel: str,
) -> np.ndarray:
    """Return table[k, a, b], the divergence of law a from the k-transport of law b."""
    if channel == "belief":
        representation, family = model.belief_representation, model.belief_family
    elif channel == "model":
        representation, family = model.model_representation, model.model_family
    else:
        raise ValueError("channel must be 'belief' or 'model'")
    order = model.graph.order
    size = len(family)
    table = np.zeros((order, size, size), dtype=np.float64)
    for element in range(order):
        for right in range(size):
            pushed: Law = representation.act(element, family[right])
            for left in range(size):
                table[element, left, right] = kl_laws(family[left], pushed)
    return table


@lru_cache(maxsize=None)
def _partition_tables(model: FalsificationModel, partition: Partition) -> _PartitionTables:
    """Return the precomputed exact tables that evaluate the derived U(R)."""
    agents = model.agents
    position_of = {agent: index for index, agent in enumerate(agents)}
    if tuple(sorted(agent for block in partition for agent in block)) != tuple(sorted(agents)):
        raise ValueError("partition must be a set partition of the declared agents")
    states = model.state_count
    identity_weight = float(model.identity_holonomy_weight)
    mixed_cost = np.zeros((len(agents), states, states), dtype=np.float64)
    block_of: dict[int, int] = {}
    belief_transport: dict[int, int] = {}
    model_transport: dict[int, int] = {}
    for block_index, block in enumerate(partition):
        belief_elements = _component_transports(model, block, "belief")
        model_elements = _component_transports(model, block, "model")
        for agent in block:
            block_of[agent] = block_index
            belief_transport[agent] = belief_elements[agent]
            model_transport[agent] = model_elements[agent]
            for parent in range(states):
                computed = np.array(
                    _downward_law(model, belief_elements[agent], model_elements[agent], parent),
                    dtype=np.float64,
                )
                flat = np.array(_downward_law(model, 0, 0, parent), dtype=np.float64)
                cost = -(1.0 - identity_weight) * np.log(computed)
                cost -= identity_weight * np.log(flat)
                mixed_cost[position_of[agent], :, parent] = cost
    edge_element = {
        (edge.receiver, edge.source): index for index, edge in enumerate(model.graph.edges)
    }
    order = model.graph.order
    pairs: list[_PairTable] = []
    for configuration in model.row_configurations:
        belief_eta = model.edge_event_law(configuration, "belief")
        model_eta = model.edge_event_law(configuration, "model")
        left: list[int] = []
        right: list[int] = []
        belief_group: list[int] = []
        model_group: list[int] = []
        belief_weight: list[float] = []
        model_weight: list[float] = []
        for receiver_index, receiver in enumerate(agents):
            for source_index, source in enumerate(agents):
                weight_b = float(belief_eta[receiver_index, source_index])
                weight_m = float(model_eta[receiver_index, source_index])
                if weight_b == 0.0 and weight_m == 0.0:
                    continue
                if receiver == source:
                    edge_belief, edge_model = 0, 0
                else:
                    index = edge_element[(receiver, source)]
                    edge_belief = model.graph.belief_elements[index]
                    edge_model = model.graph.model_elements[index]
                left.append(block_of[receiver])
                right.append(block_of[source])
                belief_group.append(
                    (belief_transport[receiver] + edge_belief - belief_transport[source]) % order
                )
                model_group.append(
                    (model_transport[receiver] + edge_model - model_transport[source]) % order
                )
                belief_weight.append(weight_b)
                model_weight.append(weight_m)
        pairs.append(
            _PairTable(
                block_left=np.array(left, dtype=np.int64),
                block_right=np.array(right, dtype=np.int64),
                belief_element=np.array(belief_group, dtype=np.int64),
                model_element=np.array(model_group, dtype=np.int64),
                belief_weight=np.array(belief_weight, dtype=np.float64),
                model_weight=np.array(model_weight, dtype=np.float64),
            )
        )
    return _PartitionTables(
        blocks=tuple(tuple(block) for block in partition),
        positions=tuple(
            np.array([position_of[agent] for agent in block], dtype=np.int64)
            for block in partition
        ),
        mixed_cost=mixed_cost,
        pairs=tuple(pairs),
        belief_kl=_transport_kl_table(model, "belief"),
        model_kl=_transport_kl_table(model, "model"),
        kappa_belief=model.kappa_belief,
        kappa_model=model.kappa_model,
        model_family_size=len(model.model_family),
    )


def _as_state_batch(model: FalsificationModel, states: Sequence[int]) -> np.ndarray:
    """Coerce one agent-state configuration to a validated batch of shape (1, agents)."""
    array = np.asarray(states, dtype=np.int64)
    if array.ndim != 1 or array.shape[0] != len(model.agents):
        raise ValueError("states must carry one index per declared agent")
    if array.min(initial=0) < 0 or array.max(initial=0) >= model.state_count:
        raise ValueError("states must index the declared presentation space")
    return array.reshape(1, -1)


def _evaluate_batch(
    tables: _PartitionTables,
    states: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the cross-scale group, the graph group, and the optimal parent states."""
    batch = states.shape[0]
    parents = np.empty((batch, len(tables.blocks)), dtype=np.int64)
    cross = np.zeros(batch, dtype=np.float64)
    for index, positions in enumerate(tables.positions):
        selected = tables.mixed_cost[positions[None, :], states[:, positions], :]
        costs = selected.sum(axis=1)
        parents[:, index] = np.argmin(costs, axis=1)
        cross += costs.min(axis=1)
    belief_parent = parents // tables.model_family_size
    model_parent = parents % tables.model_family_size
    energies = np.empty((batch, len(tables.pairs)), dtype=np.float64)
    for index, pair in enumerate(tables.pairs):
        belief_values = tables.belief_kl[
            pair.belief_element[None, :],
            belief_parent[:, pair.block_left],
            belief_parent[:, pair.block_right],
        ]
        model_values = tables.model_kl[
            pair.model_element[None, :],
            model_parent[:, pair.block_left],
            model_parent[:, pair.block_right],
        ]
        energies[:, index] = (pair.belief_weight * belief_values).sum(axis=1) * tables.kappa_belief
        energies[:, index] += (pair.model_weight * model_values).sum(axis=1) * tables.kappa_model
    log_graph = -energies - _log_sum_exp(-energies)[:, None]
    graph = -math.log(len(tables.pairs)) - log_graph.mean(axis=1)
    return cross, graph, parents


def energy_terms(
    model: FalsificationModel,
    partition: Partition,
    states: Sequence[int],
) -> EnergyTerms:
    """Return the derived U(R) split into its three conditional-divergence groups.

    The graph group is the divergence of the frozen uniform recognition law over
    row configurations from the declared parent-scale Gibbs law, whose weights read
    parent-scale divergences of dressed transports and nothing else. The holonomy
    group is the divergence of the frozen recognition law over the two holonomy
    atoms from the declared generative weights, which is exactly zero because the
    two are frozen equal. The cross-scale group is the divergence of the point-mass
    child recognition law from the downward kernel, averaged over the holonomy
    atoms and minimized over the parent state of each block.
    """
    tables = _partition_tables(model, partition)
    batch = _as_state_batch(model, states)
    cross, graph, parents = _evaluate_batch(tables, batch)
    total = float(cross[0]) + float(graph[0])
    return EnergyTerms(
        graph_divergence=float(graph[0]),
        holonomy_divergence=0.0,
        cross_scale_divergence=float(cross[0]),
        total=total,
        parent_states=tuple(int(value) for value in parents[0]),
    )


def block_energy(
    model: FalsificationModel,
    partition: Partition,
    states: Sequence[int],
) -> float:
    """Return the derived block energy U(R) of Proposition 4 at frozen coordinates.

    The collected divergences are exactly the three conditional groups that the
    choice of R controls at depth one: the graph group KL(Q_G || P_G(. | Z_1, R)),
    the holonomy group KL(Q_H || P_H) averaged under Q_G, and the cross-scale group
    E_{Q_H} KL(Q_0 || K_down) averaged under both. The cross-scale group dominates
    and is, for the point-mass child recognition law of this measurement, the sum
    over blocks and members of the negative log downward kernel, whose leading part
    is the divergence of each child law from the transported parent law, minimized
    over the parent state of the block. No hand-written mismatch or retention term
    appears, because such a term would be a proposal for U rather than U.
    """
    return energy_terms(model, partition, states).total


@lru_cache(maxsize=None)
def _log_partition_prior(model: FalsificationModel, partition: Partition) -> float:
    """Return the log of the exact Ewens prior mass of one candidate partition."""
    prior: Fraction = crp_partition_prior(partition, model.crp_concentration)
    return math.log(float(prior))


def free_energy(
    model: FalsificationModel,
    partition: Partition,
    states: Sequence[int],
) -> float:
    """Return the exact finite free energy of one joint partition and state configuration."""
    return block_energy(model, partition, states) - _log_partition_prior(model, partition)


def partition_posterior(
    model: FalsificationModel,
    states: Sequence[int],
) -> dict[Partition, float]:
    """Return the exact Gibbs partition law of Proposition 4 at temperature one."""
    weights = np.array(
        [
            _log_partition_prior(model, partition) - block_energy(model, partition, states)
            for partition in model.candidate_partitions
        ],
        dtype=np.float64,
    )
    normalizer = float(_log_sum_exp(weights[None, :])[0])
    law = np.exp(weights - normalizer)
    return {
        partition: float(value)
        for partition, value in zip(model.candidate_partitions, law)
    }


def partition_log_normalizer(model: FalsificationModel, states: Sequence[int]) -> float:
    """Return the minimum value -log Z_R attained by the Proposition 4 update."""
    weights = np.array(
        [
            _log_partition_prior(model, partition) - block_energy(model, partition, states)
            for partition in model.candidate_partitions
        ],
        dtype=np.float64,
    )
    return -float(_log_sum_exp(weights[None, :])[0])


def coupled_descent(
    model: FalsificationModel,
    seed: int,
    noise: float,
    steps: int = DESCENT_STEPS,
) -> DescentTrace:
    """Run the coupled Metropolis dynamics on the joint partition and state configuration.

    Proposals are symmetric: with the declared probability the partition moves to a
    uniformly drawn different candidate, otherwise one uniformly drawn agent moves
    to a uniformly drawn different state. The acceptance rule is Metropolis on the
    exact finite free energy at inverse temperature one over the noise amplitude,
    so the chain is reversible with respect to that law and reduces at unit noise
    and frozen states to the Proposition 4 posterior over partitions.
    """
    if type(steps) is not int or steps < 1:
        raise ValueError("steps must be a positive integer")
    if not noise > 0.0:
        raise ValueError("noise must be positive")
    generator = np.random.default_rng(seed)
    candidates = model.candidate_partitions
    count = len(candidates)
    index = int(generator.integers(count))
    states = generator.integers(0, model.state_count, len(model.agents)).astype(np.int64)
    current = free_energy(model, candidates[index], states)
    recorded: list[Partition] = []
    energies: list[float] = []
    accepted = 0
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
        candidate = free_energy(model, candidates[proposed_index], proposed_states)
        gap = candidate - current
        if gap <= 0.0 or generator.random() < math.exp(-gap / noise):
            index, states, current = proposed_index, proposed_states, candidate
            accepted += 1
        recorded.append(candidates[index])
        energies.append(current)
    return DescentTrace(
        model_name=model.name,
        seed=int(seed),
        noise=float(noise),
        steps=steps,
        partitions=tuple(recorded),
        energies=tuple(energies),
        final_states=tuple(int(value) for value in states),
        acceptance_rate=accepted / steps,
    )


def residence_times(trace: DescentTrace) -> dict[Partition, float]:
    """Return the mean contiguous sojourn length of each partition visited by a trace.

    A sojourn is a maximal run of consecutive recorded steps at one partition, and
    the final run is retained although it is right censored by the end of the run.
    Partitions never visited carry no entry.
    """
    totals: dict[Partition, float] = {}
    counts: dict[Partition, int] = {}
    if not trace.partitions:
        return {}
    current = trace.partitions[0]
    length = 0
    for partition in trace.partitions:
        if partition == current:
            length += 1
            continue
        totals[current] = totals.get(current, 0.0) + length
        counts[current] = counts.get(current, 0) + 1
        current, length = partition, 1
    totals[current] = totals.get(current, 0.0) + length
    counts[current] = counts.get(current, 0) + 1
    return {partition: totals[partition] / counts[partition] for partition in totals}


def ensemble_residence_times(traces: Sequence[DescentTrace]) -> dict[Partition, float]:
    """Return the mean sojourn length of each partition pooled over several traces."""
    totals: dict[Partition, float] = {}
    counts: dict[Partition, float] = {}
    for trace in traces:
        if not trace.partitions:
            continue
        current = trace.partitions[0]
        length = 0
        for partition in trace.partitions:
            if partition == current:
                length += 1
                continue
            totals[current] = totals.get(current, 0.0) + length
            counts[current] = counts.get(current, 0.0) + 1.0
            current, length = partition, 1
        totals[current] = totals.get(current, 0.0) + length
        counts[current] = counts.get(current, 0.0) + 1.0
    return {partition: totals[partition] / counts[partition] for partition in totals}


def co_membership_matrix(traces: Sequence[DescentTrace]) -> np.ndarray:
    """Return the fraction of recorded steps in which each agent pair shares a block."""
    if not traces:
        raise ValueError("at least one trace is required")
    labels = tuple(sorted(agent for block in traces[0].partitions[0] for agent in block))
    position_of = {agent: index for index, agent in enumerate(labels)}
    size = len(labels)
    matrix = np.zeros((size, size), dtype=np.float64)
    total = 0
    indicators: dict[Partition, np.ndarray] = {}
    for trace in traces:
        for partition in trace.partitions:
            indicator = indicators.get(partition)
            if indicator is None:
                indicator = np.zeros((size, size), dtype=np.float64)
                for block in partition:
                    members = [position_of[agent] for agent in block]
                    for left in members:
                        for right in members:
                            indicator[left, right] = 1.0
                indicators[partition] = indicator
            matrix += indicator
            total += 1
    return matrix / total


def modal_partition(traces: Sequence[DescentTrace]) -> Partition:
    """Return the partition occupying the largest share of the pooled recorded steps."""
    if not traces:
        raise ValueError("at least one trace is required")
    occupancy: dict[Partition, int] = {}
    for trace in traces:
        for partition in trace.partitions:
            occupancy[partition] = occupancy.get(partition, 0) + 1
    return max(sorted(occupancy), key=lambda partition: occupancy[partition])


def modal_occupancy(traces: Sequence[DescentTrace]) -> float:
    """Return the pooled step fraction spent at the modal partition."""
    target = modal_partition(traces)
    hits = sum(sum(1 for step in trace.partitions if step == target) for trace in traces)
    total = sum(len(trace.partitions) for trace in traces)
    return hits / total


def belief_relaxation_time(
    model: FalsificationModel,
    seed: int,
    noise: float,
    replicas: int = RELAXATION_REPLICAS,
    window: int = RELAXATION_WINDOW,
) -> float:
    """Return the measured time for the state-change rate to fall by one factor of e.

    The partition is held fixed at the maximizer of the exact Proposition 4
    posterior evaluated at the first drawn start configuration, and an ensemble of
    replicas starts from independent uniformly drawn agent states. Each replica
    then runs the same kernel as the coupled dynamics with the partition move
    replaced by a null move, so the clock is the coupled-chain clock rather than a
    faster state-only clock. The change rate r(t) is the fraction of replicas whose
    state actually moved at step t, smoothed by a centered moving average of the
    declared width. Writing r_inf for the mean rate over the final quarter of the
    window, the relaxation time is the first step at which the smoothed rate falls
    to r_inf + (r(1) - r_inf) / e. If the rate never reaches that level within the
    window the measurement returns the window length, which is the honest statement
    that no decay was resolved rather than an extrapolated bound.
    """
    if not noise > 0.0:
        raise ValueError("noise must be positive")
    if type(replicas) is not int or replicas < 2:
        raise ValueError("replicas must be an integer at least two")
    if type(window) is not int or window < RELAXATION_SMOOTHING:
        raise ValueError("window must be at least the smoothing width")
    generator = np.random.default_rng(seed)
    agents = len(model.agents)
    states = generator.integers(0, model.state_count, (replicas, agents)).astype(np.int64)
    posterior = partition_posterior(model, states[0])
    partition = max(sorted(posterior), key=lambda key: posterior[key])
    tables = _partition_tables(model, partition)
    cross, graph, _ = _evaluate_batch(tables, states)
    current = cross + graph
    rates = np.zeros(window, dtype=np.float64)
    for step in range(window):
        proposed = states.copy()
        move = generator.random(replicas) >= PARTITION_MOVE_PROBABILITY
        agent = generator.integers(0, agents, replicas)
        shift = 1 + generator.integers(0, model.state_count - 1, replicas)
        rows = np.arange(replicas)
        updated = (states[rows, agent] + shift) % model.state_count
        proposed[rows[move], agent[move]] = updated[move]
        cross, graph, _ = _evaluate_batch(tables, proposed)
        candidate = cross + graph
        gap = candidate - current
        accept = (gap <= 0.0) | (
            generator.random(replicas) < np.exp(-np.clip(gap, 0.0, 700.0) / noise)
        )
        changed = accept & move
        states[changed] = proposed[changed]
        current[accept] = candidate[accept]
        rates[step] = float(changed.mean())
    kernel = np.ones(RELAXATION_SMOOTHING, dtype=np.float64)
    support = np.convolve(np.ones(window, dtype=np.float64), kernel, mode="same")
    smoothed = np.convolve(rates, kernel, mode="same") / support
    plateau = float(smoothed[-(window // 4):].mean())
    target = plateau + (float(smoothed[0]) - plateau) / math.e
    for step in range(window):
        if smoothed[step] <= target:
            return float(step + 1)
    return float(window)


def exit_time_scaling(
    model: FalsificationModel,
    seeds: Sequence[int],
    noise_values: Sequence[float],
    steps: int = EXIT_STEP_BUDGET,
    partition: Optional[Partition] = None,
) -> ExitTimeFit:
    """Fit the log mean exit time from one partition against inverse noise amplitude.

    Each run starts at the named partition with uniformly drawn agent states and
    the exit time is the first step at which the coupled chain occupies a different
    partition. A run that never leaves within the step budget is right censored at
    the budget, and the censored fraction is reported per noise value so that a
    saturated point is visible rather than hidden. The fit is ordinary least
    squares of the log mean exit time against one over the noise amplitude, and the
    pre-registered secondary falsifier fires when the coefficient of determination
    falls below the declared threshold.
    """
    if partition is None:
        traces = [
            coupled_descent(model, int(seed), float(noise_values[0]), DESCENT_STEPS)
            for seed in list(seeds)[:CALIBRATION_INITIALIZATIONS]
        ]
        partition = modal_partition(traces)
    candidates = model.candidate_partitions
    if partition not in candidates:
        raise ValueError("partition must be a declared candidate")
    start = candidates.index(partition)
    means: list[float] = []
    censored: list[float] = []
    for noise_index, noise in enumerate(noise_values):
        exits: list[int] = []
        cuts = 0
        for seed in seeds:
            generator = np.random.default_rng((int(seed), noise_index))
            index = start
            states = generator.integers(0, model.state_count, len(model.agents)).astype(np.int64)
            current = free_energy(model, candidates[index], states)
            exit_step = steps
            for step in range(steps):
                if len(candidates) > 1 and generator.random() < PARTITION_MOVE_PROBABILITY:
                    proposed_index = (
                        index + 1 + int(generator.integers(len(candidates) - 1))
                    ) % len(candidates)
                    proposed_states = states
                else:
                    proposed_index = index
                    proposed_states = states.copy()
                    agent = int(generator.integers(len(model.agents)))
                    shift = 1 + int(generator.integers(model.state_count - 1))
                    proposed_states[agent] = (states[agent] + shift) % model.state_count
                candidate = free_energy(model, candidates[proposed_index], proposed_states)
                gap = candidate - current
                if gap <= 0.0 or generator.random() < math.exp(-gap / float(noise)):
                    index, states, current = proposed_index, proposed_states, candidate
                if index != start:
                    exit_step = step + 1
                    break
            else:
                cuts += 1
            exits.append(exit_step)
        means.append(float(np.mean(exits)))
        censored.append(cuts / len(list(seeds)))
    inverse = np.array([1.0 / float(noise) for noise in noise_values], dtype=np.float64)
    response = np.log(np.array(means, dtype=np.float64))
    design = np.vstack([inverse, np.ones_like(inverse)]).T
    solution, *_ = np.linalg.lstsq(design, response, rcond=None)
    slope, intercept = float(solution[0]), float(solution[1])
    residual = response - design @ solution
    total = response - response.mean()
    r_squared = 0.0 if float(total @ total) == 0.0 else 1.0 - float(residual @ residual) / float(total @ total)
    return ExitTimeFit(
        partition=partition,
        noise_values=tuple(float(noise) for noise in noise_values),
        mean_exit_times=tuple(means),
        censored_fraction=tuple(censored),
        step_budget=steps,
        slope=slope,
        intercept=intercept,
        r_squared=r_squared,
        linearity_falsifier_fired=r_squared < LINEARITY_R_SQUARED_THRESHOLD,
    )


def persistence_statistics(
    model: FalsificationModel,
    seed: int,
    noise: float,
    steps: int = DESCENT_STEPS,
    initializations: int = INITIALIZATION_COUNT,
    exit_seeds: Optional[Sequence[int]] = None,
    exit_noise_values: Optional[Sequence[float]] = None,
) -> PersistenceReport:
    """Measure every block-formation statistic of one model instance in one pipeline."""
    traces = [
        coupled_descent(model, seed + offset, noise, steps) for offset in range(initializations)
    ]
    residences = ensemble_residence_times(traces)
    relaxation = belief_relaxation_time(model, seed, noise)
    maximum = max(residences.values()) if residences else 0.0
    ratio = maximum / relaxation
    matrix = co_membership_matrix(traces)
    off_diagonal = matrix - np.diag(np.diag(matrix))
    fit: Optional[ExitTimeFit] = None
    if exit_noise_values is not None:
        fit = exit_time_scaling(
            model,
            list(exit_seeds) if exit_seeds is not None else [seed + offset for offset in range(8)],
            exit_noise_values,
            EXIT_STEP_BUDGET,
            modal_partition(traces),
        )
    return PersistenceReport(
        model_name=model.name,
        seed=int(seed),
        noise=float(noise),
        steps=steps,
        initializations=initializations,
        modal_partition=modal_partition(traces),
        modal_occupancy=modal_occupancy(traces),
        residence_times=tuple(sorted(residences.items())),
        maximum_residence_time=float(maximum),
        relaxation_time=float(relaxation),
        residence_ratio=float(ratio),
        co_membership=tuple(tuple(float(value) for value in row) for row in matrix),
        largest_off_diagonal_co_membership=float(off_diagonal.max()),
        timescale_falsifier_fired=bool(ratio <= RESIDENCE_RATIO_THRESHOLD),
        exit_fit=fit,
    )


def null_control_comparison(
    seeds: Sequence[int],
    noise: float = REFERENCE_NOISE,
    steps: int = NULL_DESCENT_STEPS,
    initializations: int = NULL_INITIALIZATION_COUNT,
    exit_noise_values: Optional[Sequence[float]] = None,
) -> NullControlReport:
    """Run the persistence pipeline on the reference and on several null instances.

    The null instances randomize the edge group elements and the belief family while
    holding the graph skeleton, the occupancies, the candidate partitions and every
    kernel family fixed. The reference is rerun at exactly the settings used for the
    nulls, so each reported block-formation statistic carries the null distribution
    of that same statistic beside it rather than a point comparison.
    """
    if not list(seeds):
        raise ValueError("at least one null seed is required")
    reference = persistence_statistics(
        build_reference_model(),
        int(list(seeds)[0]),
        noise,
        steps,
        initializations,
        None,
        exit_noise_values,
    )
    nulls = tuple(
        persistence_statistics(
            build_null_model(int(seed)),
            int(seed),
            noise,
            steps,
            initializations,
            None,
            exit_noise_values,
        )
        for seed in seeds
    )
    return NullControlReport(
        seeds=tuple(int(seed) for seed in seeds),
        noise=float(noise),
        steps=steps,
        initializations=initializations,
        reference=reference,
        nulls=nulls,
        null_modal_occupancy=tuple(report.modal_occupancy for report in nulls),
        null_maximum_residence_time=tuple(report.maximum_residence_time for report in nulls),
        null_relaxation_time=tuple(report.relaxation_time for report in nulls),
        null_residence_ratio=tuple(report.residence_ratio for report in nulls),
        null_largest_off_diagonal_co_membership=tuple(
            report.largest_off_diagonal_co_membership for report in nulls
        ),
        null_timescale_falsifier_fired=tuple(report.timescale_falsifier_fired for report in nulls),
    )


__all__ = [
    "CALIBRATION_INITIALIZATIONS",
    "DESCENT_STEPS",
    "DescentTrace",
    "EXIT_STEP_BUDGET",
    "EnergyTerms",
    "ExitTimeFit",
    "INITIALIZATION_COUNT",
    "LINEARITY_R_SQUARED_THRESHOLD",
    "NULL_DESCENT_STEPS",
    "NULL_INITIALIZATION_COUNT",
    "NullControlReport",
    "PARTITION_MOVE_PROBABILITY",
    "PersistenceReport",
    "REFERENCE_NOISE",
    "REFERENCE_NOISE_VALUES",
    "RELAXATION_REPLICAS",
    "RELAXATION_SMOOTHING",
    "RELAXATION_WINDOW",
    "RESIDENCE_RATIO_THRESHOLD",
    "belief_relaxation_time",
    "block_energy",
    "co_membership_matrix",
    "coupled_descent",
    "downward_law",
    "energy_terms",
    "ensemble_residence_times",
    "exit_time_scaling",
    "free_energy",
    "modal_occupancy",
    "modal_partition",
    "null_control_comparison",
    "partition_log_normalizer",
    "partition_posterior",
    "persistence_statistics",
    "residence_times",
]
