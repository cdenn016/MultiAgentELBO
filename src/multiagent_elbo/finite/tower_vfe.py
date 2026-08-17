"""Depth-one generative tower free energy for the finite categorical design.

The declared instance of the falsification design is lifted here to a generative
tower of depth one, with variables ordered as parent state, partition, row
configuration, holonomy atom, child state, and finally the record. Every factor is
a normalized Markov kernel conditioning only on strictly earlier variables, so the
joint carries no partition function and the free energy is an ordinary evidence
bound rather than a variational surrogate for one.

Two independent routes to the same number live in this module. The flat route
materializes the entire joint over the tower state space, sums it to obtain the
evidence, normalizes it to obtain the posterior, and takes one flat relative
entropy against the recognition tower. The decomposed route never forms that array
and instead assembles the six conditional groups of the decomposition theorem. The
routes share the declared factors, because there is only one declared model, but
they share no part of the free-energy assembly, which is what makes their agreement
an accounting measurement rather than an algebraic rearrangement.

The recognition tower is disintegrated along the same ordering, factor for factor.
It is a correlated law: each factor is a separate conditional law for every value
of its conditioning variables, and nothing in this module ever reconstructs it from
coordinate marginals.

Every declared constant is a rational, and every array is float64.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import math

import numpy as np

from .categorical_falsification_model import (
    FalsificationModel,
    crp_partition_prior,
    kl_laws,
    transported,
)
from .vfe import _kl_arrays

HOLONOMY_ATOMS: tuple[str, ...] = ("computed", "identity")

PARENT_STATE_WEIGHTS: tuple[Fraction, ...] = (
    Fraction(5, 45),
    Fraction(3, 45),
    Fraction(8, 45),
    Fraction(2, 45),
    Fraction(7, 45),
    Fraction(4, 45),
    Fraction(9, 45),
    Fraction(1, 45),
    Fraction(6, 45),
)


@dataclass(frozen=True)
class TowerRecognition:
    """A recognition tower disintegrated along the declared variable ordering."""

    top: np.ndarray
    partition: np.ndarray
    rows: np.ndarray
    holonomy: np.ndarray
    child: np.ndarray

    def __post_init__(self) -> None:
        names = ("top", "partition", "rows", "holonomy", "child")
        factors = (self.top, self.partition, self.rows, self.holonomy, self.child)
        for place, (name, factor) in enumerate(zip(names, factors), start=1):
            if type(factor) is not np.ndarray:
                raise TypeError(f"{name} must be a numpy array")
            if factor.dtype != np.float64:
                raise TypeError(f"{name} must hold float64 entries")
            if factor.ndim != place:
                raise ValueError(f"{name} must carry {place} axes")
            if not np.all(np.isfinite(factor)) or np.any(factor < 0.0):
                raise ValueError(f"{name} must be finite and nonnegative")
            if not np.allclose(factor.sum(axis=-1), 1.0, rtol=0.0, atol=1e-12):
                raise ValueError(f"{name} must normalize over its last axis")
        shapes = tuple(factor.shape for factor in factors)
        for earlier, later in zip(shapes, shapes[1:]):
            if later[:-1] != earlier:
                raise ValueError("recognition factors must nest along the ordering")


@dataclass(frozen=True)
class TowerDecomposition:
    """The six conditional groups of the depth-one tower free energy and their total."""

    observation_term: float
    top_prior_term: float
    partition_term: float
    row_term: float
    holonomy_term: float
    cross_scale_term: float
    total: float


def _relative_entropy(q: np.ndarray, p: np.ndarray) -> float:
    """Return the relative entropy of two flat probability arrays."""
    value, _ = _kl_arrays(q, p)
    return value


def _frozen(array: np.ndarray) -> np.ndarray:
    """Return the array marked read only, so cached tables cannot be mutated."""
    array.setflags(write=False)
    return array


def _check_model(model: FalsificationModel) -> None:
    """Reject any declared instance the depth-one tower cannot represent."""
    if type(model) is not FalsificationModel:
        raise TypeError("model must be a FalsificationModel")
    if model.state_count != len(PARENT_STATE_WEIGHTS):
        raise ValueError("the declared parent law must match the agent state space")
    if not model.candidate_partitions:
        raise ValueError("the tower needs at least one candidate partition")
    if not model.row_configurations:
        raise ValueError("the tower needs at least one row configuration")
    agents = sorted(model.agents)
    for partition in model.candidate_partitions:
        if len(partition) > len(model.parent_labels):
            raise ValueError("a candidate partition exceeds the declared label pool")
        members = sorted(agent for block in partition for agent in block)
        if members != agents:
            raise ValueError("a candidate partition must partition the declared agents")


def _check_observation(model: FalsificationModel, observation: tuple[int, ...]) -> tuple[int, ...]:
    """Reject any record that is not a binary outcome for every declared agent."""
    if type(observation) is not tuple:
        raise TypeError("observation must be a tuple of binary outcomes")
    if len(observation) != len(model.agents):
        raise ValueError("observation must carry one outcome per declared agent")
    for outcome in observation:
        if type(outcome) is not int:
            raise TypeError("observation outcomes must be integers")
        if outcome not in (0, 1):
            raise ValueError("observation outcomes must be zero or one")
    return observation


def _check_recognition(model: FalsificationModel, recognition: TowerRecognition) -> None:
    """Reject any recognition tower whose factors do not fit the declared tower."""
    if type(recognition) is not TowerRecognition:
        raise TypeError("recognition must be a TowerRecognition")
    if recognition.child.shape != _tower_shape(model):
        raise ValueError("recognition factors must match the declared tower shape")


def _tower_shape(model: FalsificationModel) -> tuple[int, int, int, int, int]:
    """Return the cardinalities of the five tower variables in declared order."""
    return (
        model.state_count ** len(model.parent_labels),
        len(model.candidate_partitions),
        len(model.row_configurations),
        len(HOLONOMY_ATOMS),
        model.state_count ** len(model.agents),
    )


@lru_cache(maxsize=None)
def _state_digits(base: int, places: int) -> np.ndarray:
    """Return the base digits of every flat index, most significant place first."""
    indices = np.arange(base ** places, dtype=np.int64)
    digits = np.empty((indices.size, places), dtype=np.int64)
    for place in range(places):
        digits[:, place] = (indices // base ** (places - 1 - place)) % base
    return _frozen(digits)


@lru_cache(maxsize=None)
def _partition_label_of(model: FalsificationModel) -> tuple[dict[int, int], ...]:
    """Return, per candidate partition, the parent label index carrying each agent."""
    tables: list[dict[int, int]] = []
    for partition in model.candidate_partitions:
        tables.append({agent: index for index, block in enumerate(partition) for agent in block})
    return tuple(tables)


@lru_cache(maxsize=None)
def _top_prior(model: FalsificationModel) -> np.ndarray:
    """Return the declared parent-state prior, a product over the parent label pool."""
    per_label = np.array([float(weight) for weight in PARENT_STATE_WEIGHTS], dtype=np.float64)
    digits = _state_digits(model.state_count, len(model.parent_labels))
    return _frozen(per_label[digits].prod(axis=1))


@lru_cache(maxsize=None)
def _partition_prior(model: FalsificationModel) -> np.ndarray:
    """Return the Chinese-restaurant prior restricted to the candidate partitions."""
    masses = [
        crp_partition_prior(partition, model.crp_concentration)
        for partition in model.candidate_partitions
    ]
    total = sum(masses, Fraction(0))
    if total == 0:
        raise ValueError("the candidate partitions carry no prior mass")
    return _frozen(np.array([float(mass / total) for mass in masses], dtype=np.float64))


@lru_cache(maxsize=None)
def _holonomy_prior(model: FalsificationModel) -> np.ndarray:
    """Return the two-atom holonomy prior, identity weighted by the declared amount."""
    identity = model.identity_holonomy_weight
    if not 0 <= identity <= 1:
        raise ValueError("the identity holonomy weight must be a probability")
    return _frozen(np.array([float(1 - identity), float(identity)], dtype=np.float64))


@lru_cache(maxsize=None)
def _edge_divergence_tables(model: FalsificationModel) -> np.ndarray:
    """Return the transported endpoint divergence of every edge in both channels."""
    count = model.state_count
    tables = np.zeros((len(model.graph.edges), 2, count, count), dtype=np.float64)
    for index in range(len(model.graph.edges)):
        belief_element = model.graph.belief_elements[index]
        model_element = model.graph.model_elements[index]
        for receiver_state in range(count):
            receiver_belief, receiver_model = model.state_pair(receiver_state)
            for source_state in range(count):
                source_belief, source_model = model.state_pair(source_state)
                tables[index, 0, receiver_state, source_state] = kl_laws(
                    receiver_belief,
                    transported(model.belief_representation, belief_element, source_belief),
                )
                tables[index, 1, receiver_state, source_state] = kl_laws(
                    receiver_model,
                    transported(model.model_representation, model_element, source_model),
                )
    return _frozen(tables)


@lru_cache(maxsize=None)
def _row_prior(model: FalsificationModel) -> np.ndarray:
    """Return the row-configuration prior, a Gibbs law over parent-level energies only.

    The energy of one configuration is the edge-event weighted sum, over the declared
    edges and both channels, of the divergence between the two endpoint parent states
    after the edge transport carries the source parent frame into the receiver parent
    frame. It reads the parent state and the partition and nothing else, so it never
    touches the child state generated after it and never touches a recognition law.
    """
    parent_count, partition_count, row_count = _tower_shape(model)[:3]
    divergences = _edge_divergence_tables(model)
    digits = _state_digits(model.state_count, len(model.parent_labels))
    label_tables = _partition_label_of(model)
    position_of = {agent: index for index, agent in enumerate(model.agents)}
    energies = np.zeros((parent_count, partition_count, row_count), dtype=np.float64)
    for partition_index in range(partition_count):
        label_of = label_tables[partition_index]
        for row_index, configuration in enumerate(model.row_configurations):
            belief_events = model.edge_event_law(configuration, "belief")
            model_events = model.edge_event_law(configuration, "model")
            for edge_index, edge in enumerate(model.graph.edges):
                receiver = position_of[edge.receiver]
                source = position_of[edge.source]
                receiver_state = digits[:, label_of[edge.receiver]]
                source_state = digits[:, label_of[edge.source]]
                energies[:, partition_index, row_index] += (
                    float(belief_events[receiver, source])
                    * model.kappa_belief
                    * divergences[edge_index, 0, receiver_state, source_state]
                )
                energies[:, partition_index, row_index] += (
                    float(model_events[receiver, source])
                    * model.kappa_model
                    * divergences[edge_index, 1, receiver_state, source_state]
                )
    weights = np.exp(-(energies - energies.min(axis=-1, keepdims=True)))
    return _frozen(weights / weights.sum(axis=-1, keepdims=True))


@lru_cache(maxsize=None)
def _downward_rows(model: FalsificationModel) -> np.ndarray:
    """Return the per-agent downward kernel rows, indexed by partition and holonomy atom.

    Under the computed atom the block spanning-tree transport carries the parent frame
    into the agent frame, which is the declared cross-scale kernel. Under the identity
    atom every tree transport is replaced by the identity, which is exactly the kernel
    of the singleton block containing that agent, so the flatness assumption appears
    here as a visible modeling choice rather than as a hidden regularizer.
    """
    partition_count = len(model.candidate_partitions)
    agent_count = len(model.agents)
    count = model.state_count
    rows = np.empty(
        (partition_count, len(HOLONOMY_ATOMS), agent_count, count, count),
        dtype=np.float64,
    )
    for partition_index, partition in enumerate(model.candidate_partitions):
        block_of = {agent: block for block in partition for agent in block}
        for atom_index, atom in enumerate(HOLONOMY_ATOMS):
            for position, agent in enumerate(model.agents):
                block = (agent,) if atom == "identity" else block_of[agent]
                for parent_state in range(count):
                    rows[partition_index, atom_index, position, parent_state] = (
                        model.downward_kernel(block, agent, parent_state)
                    )
    return _frozen(rows)


@lru_cache(maxsize=None)
def _cross_scale_table(model: FalsificationModel) -> np.ndarray:
    """Return the downward kernel over the whole child space, per parent, partition, atom."""
    parent_count, partition_count, _, atom_count, child_count = _tower_shape(model)
    rows = _downward_rows(model)
    parent_digits = _state_digits(model.state_count, len(model.parent_labels))
    child_digits = _state_digits(model.state_count, len(model.agents))
    label_tables = _partition_label_of(model)
    table = np.ones((parent_count, partition_count, atom_count, child_count), dtype=np.float64)
    for partition_index in range(partition_count):
        label_of = label_tables[partition_index]
        for atom_index in range(atom_count):
            for position, agent in enumerate(model.agents):
                parent_state = parent_digits[:, label_of[agent]]
                table[:, partition_index, atom_index, :] *= rows[
                    partition_index, atom_index, position
                ][np.ix_(parent_state, child_digits[:, position])]
    return _frozen(table)


@lru_cache(maxsize=None)
def _likelihood_vector(model: FalsificationModel, observation: tuple[int, ...]) -> np.ndarray:
    """Return the record likelihood at every child state of the declared tower."""
    table = model.likelihood_table()
    digits = _state_digits(model.state_count, len(model.agents))
    value = np.ones(digits.shape[0], dtype=np.float64)
    for position, outcome in enumerate(observation):
        value *= table[digits[:, position], outcome]
    return _frozen(value)


@lru_cache(maxsize=None)
def _log_likelihood_vector(
    model: FalsificationModel, observation: tuple[int, ...]
) -> np.ndarray:
    """Return the log record likelihood at every child state of the declared tower."""
    table = model.likelihood_table()
    digits = _state_digits(model.state_count, len(model.agents))
    value = np.zeros(digits.shape[0], dtype=np.float64)
    for position, outcome in enumerate(observation):
        value += np.log(table[digits[:, position], outcome])
    return _frozen(value)


def _flat_recognition(recognition: TowerRecognition) -> np.ndarray:
    """Return the joint recognition array assembled from its declared disintegration."""
    joint = recognition.top
    for factor in (recognition.partition, recognition.rows, recognition.holonomy, recognition.child):
        joint = joint[..., np.newaxis] * factor
    return joint


def tower_observation_records(model: FalsificationModel) -> tuple[tuple[int, ...], ...]:
    """Return every binary record of the declared agent set, in counting order."""
    _check_model(model)
    digits = _state_digits(2, len(model.agents))
    return tuple(tuple(int(entry) for entry in row) for row in digits)


def flat_tower_joint(model: FalsificationModel, observation: tuple[int, ...]) -> np.ndarray:
    """Return the joint mass of one record and every tower state, enumerated state by state.

    The returned array carries one entry per element of the tower state space, in the
    declared ordering of parent state, partition, row configuration, holonomy atom, and
    child state. Every entry is evaluated on its own by looking up the value of each
    declared factor at that state, so nothing is marginalized analytically and no sum
    is replaced by a closed form.
    """
    _check_model(model)
    record = _check_observation(model, observation)
    parent_count, partition_count, row_count, atom_count, child_count = _tower_shape(model)
    cross_scale = _cross_scale_table(model)
    likelihood = _likelihood_vector(model, record)
    joint = np.empty(
        (parent_count, partition_count, row_count, atom_count, child_count),
        dtype=np.float64,
    )
    for partition_index in range(partition_count):
        for atom_index in range(atom_count):
            observed = cross_scale[:, partition_index, atom_index, :] * likelihood
            joint[:, partition_index, :, atom_index, :] = observed[:, np.newaxis, :]
    joint *= _top_prior(model)[:, np.newaxis, np.newaxis, np.newaxis, np.newaxis]
    joint *= _partition_prior(model)[np.newaxis, :, np.newaxis, np.newaxis, np.newaxis]
    joint *= _row_prior(model)[:, :, :, np.newaxis, np.newaxis]
    joint *= _holonomy_prior(model)[np.newaxis, np.newaxis, np.newaxis, :, np.newaxis]
    return joint


def seeded_tower_recognition(
    model: FalsificationModel,
    observation: tuple[int, ...],
    seed: int,
) -> TowerRecognition:
    """Return a deterministic correlated recognition tower for one record.

    Each factor is drawn independently for every value of its conditioning variables
    and then normalized over its own variable, so the resulting law is correlated
    across the tower rather than a product of coordinate marginals. A floor keeps
    every entry strictly positive, so no relative entropy in either route diverges.
    """
    _check_model(model)
    record = _check_observation(model, observation)
    if type(seed) is not int:
        raise TypeError("seed must be an integer")
    parent_count, partition_count, row_count, atom_count, child_count = _tower_shape(model)
    code = sum(outcome << position for position, outcome in enumerate(record))
    generator = np.random.default_rng([seed, code])
    factors: list[np.ndarray] = []
    shapes = (
        (parent_count,),
        (parent_count, partition_count),
        (parent_count, partition_count, row_count),
        (parent_count, partition_count, row_count, atom_count),
        (parent_count, partition_count, row_count, atom_count, child_count),
    )
    for shape in shapes:
        draw = generator.random(shape) + 0.05
        factors.append(draw / draw.sum(axis=-1, keepdims=True))
    return TowerRecognition(
        top=factors[0],
        partition=factors[1],
        rows=factors[2],
        holonomy=factors[3],
        child=factors[4],
    )


def posterior_tower_recognition(
    model: FalsificationModel,
    observation: tuple[int, ...],
) -> TowerRecognition:
    """Return the exact tower posterior, disintegrated along the declared ordering.

    This is a successive conditioning of the flat joint, not a projection onto a
    product family, so reassembling the factors returns the posterior exactly and the
    recognition gap vanishes.
    """
    joint = flat_tower_joint(model, observation)
    posterior = joint / joint.sum()
    child_mass = posterior.sum(axis=-1)
    child = posterior / child_mass[..., np.newaxis]
    holonomy_mass = child_mass.sum(axis=-1)
    holonomy = child_mass / holonomy_mass[..., np.newaxis]
    row_mass = holonomy_mass.sum(axis=-1)
    rows = holonomy_mass / row_mass[..., np.newaxis]
    partition_mass = row_mass.sum(axis=-1)
    partition = row_mass / partition_mass[..., np.newaxis]
    return TowerRecognition(
        top=partition_mass,
        partition=partition,
        rows=rows,
        holonomy=holonomy,
        child=child,
    )


def flat_tower_free_energy(
    model: FalsificationModel,
    observation: tuple[int, ...],
    recognition: TowerRecognition,
) -> float:
    """Return the tower free energy from the materialized joint over the tower state space.

    The evidence is the sum of the flat joint over every tower state, the posterior is
    that joint normalized, and the gap is a single relative entropy taken over the whole
    tower state space at once. No conditional group and no chain rule enters here.
    """
    _check_model(model)
    record = _check_observation(model, observation)
    _check_recognition(model, recognition)
    joint = flat_tower_joint(model, record)
    evidence = float(joint.sum())
    if not evidence > 0.0:
        raise ValueError("the declared tower assigns no mass to this record")
    posterior = joint / evidence
    gap = _relative_entropy(_flat_recognition(recognition).ravel(), posterior.ravel())
    return -math.log(evidence) + gap


def decomposed_tower_free_energy(
    model: FalsificationModel,
    observation: tuple[int, ...],
    recognition: TowerRecognition,
) -> TowerDecomposition:
    """Return the six conditional groups of the tower free energy and their total.

    The groups are the observation term, the top prior divergence, and the recognition
    expected conditional divergences of the partition, row, holonomy, and cross-scale
    factors. The flat joint is never formed, and the recognition tower is used only
    through its declared conditional factors.
    """
    _check_model(model)
    record = _check_observation(model, observation)
    _check_recognition(model, recognition)
    parent_count, partition_count, row_count, atom_count, _ = _tower_shape(model)
    top_prior = _top_prior(model)
    partition_prior = _partition_prior(model)
    row_prior = _row_prior(model)
    holonomy_prior = _holonomy_prior(model)
    cross_scale = _cross_scale_table(model)

    weight_top = recognition.top
    weight_partition = weight_top[:, np.newaxis] * recognition.partition
    weight_rows = weight_partition[..., np.newaxis] * recognition.rows
    weight_holonomy = weight_rows[..., np.newaxis] * recognition.holonomy

    top_prior_term = _relative_entropy(recognition.top, top_prior)

    partition_term = 0.0
    for parent in range(parent_count):
        weight = float(weight_top[parent])
        if weight == 0.0:
            continue
        partition_term += weight * _relative_entropy(recognition.partition[parent], partition_prior)

    row_term = 0.0
    for parent, partition in np.ndindex(parent_count, partition_count):
        weight = float(weight_partition[parent, partition])
        if weight == 0.0:
            continue
        row_term += weight * _relative_entropy(
            recognition.rows[parent, partition], row_prior[parent, partition]
        )

    holonomy_term = 0.0
    for parent, partition, row in np.ndindex(parent_count, partition_count, row_count):
        weight = float(weight_rows[parent, partition, row])
        if weight == 0.0:
            continue
        holonomy_term += weight * _relative_entropy(
            recognition.holonomy[parent, partition, row], holonomy_prior
        )

    cross_scale_term = 0.0
    for index in np.ndindex(parent_count, partition_count, row_count, atom_count):
        parent, partition, _, atom = index
        weight = float(weight_holonomy[index])
        if weight == 0.0:
            continue
        cross_scale_term += weight * _relative_entropy(
            recognition.child[index], cross_scale[parent, partition, atom]
        )

    log_likelihood = _log_likelihood_vector(model, record)
    observation_term = -float(np.sum(weight_holonomy * (recognition.child @ log_likelihood)))

    total = (
        observation_term
        + top_prior_term
        + partition_term
        + row_term
        + holonomy_term
        + cross_scale_term
    )
    return TowerDecomposition(
        observation_term=observation_term,
        top_prior_term=top_prior_term,
        partition_term=partition_term,
        row_term=row_term,
        holonomy_term=holonomy_term,
        cross_scale_term=cross_scale_term,
        total=total,
    )


def tower_accounting_residual(
    model: FalsificationModel,
    observation: tuple[int, ...],
    recognition: TowerRecognition,
) -> float:
    """Return the absolute gap between the flat route and the decomposed route."""
    flat = flat_tower_free_energy(model, observation, recognition)
    decomposed = decomposed_tower_free_energy(model, observation, recognition)
    return abs(flat - decomposed.total)


def naive_local_potential_sum(
    model: FalsificationModel,
    observation: tuple[int, ...],
    recognition: TowerRecognition,
) -> tuple[float, float]:
    """Return the naive sum of local row potentials and its exact edge overcount.

    The naive sum adds, for every agent, the potentials of the interaction factors
    touching it, so each declared edge is counted once by its receiver and once by its
    source. The declared interaction factors are the graph edges and the boundary of an
    edge is its endpoint pair, so every boundary has size two and the exact pointwise
    overcount, the sum over factors of the boundary size less one times the factor
    energy, reduces here to the plain sum of the edge energies.

    This quantity is NOT an evidence bound and is NOT the tower free energy. It omits
    the top prior, partition, row, holonomy, cross-scale, and observation groups
    entirely, and it double counts every interaction. Reporting it as the evidence
    lower bound is a declared falsifier of this design. The record enters only through
    the recognition tower, which is conditioned on it.
    """
    _check_model(model)
    _check_observation(model, observation)
    _check_recognition(model, recognition)
    parent_count, partition_count, row_count, atom_count, _ = _tower_shape(model)
    divergences = _edge_divergence_tables(model)
    position_of = {agent: index for index, agent in enumerate(model.agents)}
    count = model.state_count

    weight_partition = recognition.top[:, np.newaxis] * recognition.partition
    weight_rows = weight_partition[..., np.newaxis] * recognition.rows
    weight_holonomy = weight_rows[..., np.newaxis] * recognition.holonomy
    weighted = weight_holonomy[..., np.newaxis] * recognition.child
    grid = weighted.reshape(
        parent_count, partition_count, row_count, atom_count, *(count,) * len(model.agents)
    )

    row_events = tuple(
        (
            model.edge_event_law(configuration, "belief"),
            model.edge_event_law(configuration, "model"),
        )
        for configuration in model.row_configurations
    )
    energies = np.zeros(len(model.graph.edges), dtype=np.float64)
    for edge_index, edge in enumerate(model.graph.edges):
        receiver = position_of[edge.receiver]
        source = position_of[edge.source]
        moved = np.moveaxis(grid, (2, 4 + receiver, 4 + source), (0, 1, 2))
        pair = moved.sum(axis=tuple(range(3, moved.ndim)))
        for row_index in range(row_count):
            belief_events, model_events = row_events[row_index]
            potential = (
                float(belief_events[receiver, source])
                * model.kappa_belief
                * divergences[edge_index, 0]
            )
            potential = potential + (
                float(model_events[receiver, source])
                * model.kappa_model
                * divergences[edge_index, 1]
            )
            energies[edge_index] += float(np.sum(pair[row_index] * potential))

    boundary_size = 2
    naive_sum = float(boundary_size * energies.sum())
    overcount = float((boundary_size - 1) * energies.sum())
    return naive_sum, overcount


__all__ = [
    "HOLONOMY_ATOMS",
    "PARENT_STATE_WEIGHTS",
    "TowerDecomposition",
    "TowerRecognition",
    "decomposed_tower_free_energy",
    "flat_tower_free_energy",
    "flat_tower_joint",
    "naive_local_potential_sum",
    "posterior_tower_recognition",
    "seeded_tower_recognition",
    "tower_accounting_residual",
    "tower_observation_records",
]
