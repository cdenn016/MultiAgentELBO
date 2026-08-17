"""The declared finite categorical model for the two-channel falsification design.

Six agents sit at one contextual point on two directed three-cycles joined by two
cross edges. The structure group is Z_3 carrying two distinct representations, one
per channel, and every agent state is a pair of laws drawn from finite
orbit-closed families. Nothing here is Gaussian, and every declared number is a
rational, so the downstream measurements are exact up to the final logarithms.

The transports are chosen so that the belief channel carries nontrivial holonomy
on one cycle while the model channel is flat on every cycle. That asymmetry is the
prediction the holonomy measurement tests, and it survives a global flip of the
direction convention because an abelian holonomy only changes sign under such a
flip while triviality is preserved.

This module declares the system and its kernels. It computes no measurement.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence

import numpy as np

from .two_channel_gauge import (
    CyclicRepresentation,
    DirectedEdge,
    Law,
    TwoChannelGraph,
    orbit,
    tree_transport_elements,
)

Partition = tuple[tuple[int, ...], ...]

GROUP_ORDER = 3
BELIEF_SEED = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))
MODEL_SEED = (Fraction(2, 3), Fraction(1, 6), Fraction(1, 6))

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
REFERENCE_BELIEF_ELEMENTS = (1, 1, 0, 1, 1, 1, 0, 0)
REFERENCE_MODEL_ELEMENTS = (1, 1, 1, 2, 2, 2, 0, 0)

REFERENCE_ALPHA_BELIEF = (
    Fraction(30, 100),
    Fraction(25, 100),
    Fraction(20, 100),
    Fraction(12, 100),
    Fraction(8, 100),
    Fraction(5, 100),
)
REFERENCE_ALPHA_MODEL = (
    Fraction(5, 100),
    Fraction(8, 100),
    Fraction(12, 100),
    Fraction(20, 100),
    Fraction(25, 100),
    Fraction(30, 100),
)

REFERENCE_PARTITIONS: tuple[Partition, ...] = (
    ((1, 2, 3), (4, 5, 6)),
    ((1, 2), (3, 4), (5, 6)),
    ((1, 2, 3, 4, 5, 6),),
    ((1, 2, 3, 4), (5, 6)),
    ((1, 4), (2, 5), (3, 6)),
    ((1,), (2, 3, 4, 5, 6)),
)

REDUCED_PARTITIONS: tuple[Partition, ...] = (
    ((1, 2, 3),),
    ((1, 2), (3,)),
    ((1, 3), (2,)),
    ((1,), (2, 3)),
)

REDUCED_SINGLETON_PARTITION: Partition = ((1,), (2,), (3,))


def kl_laws(left: Law, right: Law) -> float:
    """Return the relative entropy of two exact laws, infinite on support failure."""
    total = 0.0
    for p, q in zip(left, right):
        if p == 0:
            continue
        if q == 0:
            return float("inf")
        total += float(p) * (np.log(float(p)) - np.log(float(q)))
    return total


def transported(
    representation: CyclicRepresentation,
    element: int,
    law: Law,
) -> Law:
    """Push a law forward by the representation of a group element."""
    return representation.act(element, law)


@dataclass(frozen=True)
class FalsificationModel:
    """One fully declared instance of the finite two-channel categorical system."""

    name: str
    belief_representation: CyclicRepresentation
    model_representation: CyclicRepresentation
    belief_family: tuple[Law, ...]
    model_family: tuple[Law, ...]
    graph: TwoChannelGraph
    alpha_belief: tuple[Fraction, ...]
    alpha_model: tuple[Fraction, ...]
    parent_labels: tuple[str, ...]
    candidate_partitions: tuple[Partition, ...]
    kappa_belief: float
    kappa_model: float
    crp_concentration: Fraction
    identity_holonomy_weight: Fraction
    row_configurations: tuple[str, ...]
    declared_rows: tuple[tuple[str, str, tuple[tuple[float, ...], ...]], ...] | None = (
        None
    )

    @property
    def agents(self) -> tuple[int, ...]:
        """Return the declared agent labels."""
        return self.graph.vertices

    @property
    def state_count(self) -> int:
        """Return the cardinality of one agent's joint presentation space."""
        return len(self.belief_family) * len(self.model_family)

    def state_pair(self, index: int) -> tuple[Law, Law]:
        """Return the belief and model laws of one agent state index."""
        model_size = len(self.model_family)
        return self.belief_family[index // model_size], self.model_family[index % model_size]

    def likelihood_table(self) -> np.ndarray:
        """Return L[state, outcome], the per-agent evaluator-averaged likelihood.

        The evaluator sends a model presentation m to the Bernoulli kernel with
        success probability m_z at belief sample point z, and the agent likelihood
        averages it against the belief law. Every entry is strictly inside (0, 1),
        so the observation term is finite and the integrability hypothesis of the
        decomposition theorem holds by construction rather than by assumption.
        """
        table = np.zeros((self.state_count, 2), dtype=np.float64)
        for index in range(self.state_count):
            belief, model = self.state_pair(index)
            success = sum(b * m for b, m in zip(belief, model))
            table[index, 1] = float(success)
            table[index, 0] = float(1 - success)
        return table

    def block_transports(self, block: Sequence[int], channel: str) -> dict[int, int]:
        """Return the group element carrying each member frame to the block root."""
        induced = self.graph.induced(block)
        root = min(block)
        return tree_transport_elements(induced, channel, root)

    def downward_kernel(
        self,
        block: Sequence[int],
        agent: int,
        parent_state: int,
    ) -> np.ndarray:
        """Return K(child state | parent state) for one agent inside one block.

        The parent state is expressed in the block root frame. It is carried into
        the agent frame by the inverse of the spanning-tree transport, and the
        child law is drawn from a Gibbs law whose energy is the transported
        mismatch in both channels. On a block with nontrivial holonomy the tree
        transport is path dependent, so no parent state reconciles every child and
        the block acquires a strictly positive energy floor. That is the channel
        through which holonomy reaches the free energy, and it is not smoothed.
        """
        belief_shift = self.block_transports(block, "belief")[agent]
        model_shift = self.block_transports(block, "model")[agent]
        parent_belief, parent_model = self.state_pair(parent_state)
        target_belief = transported(
            self.belief_representation,
            (-belief_shift) % self.graph.order,
            parent_belief,
        )
        target_model = transported(
            self.model_representation,
            (-model_shift) % self.graph.order,
            parent_model,
        )
        energies = np.empty(self.state_count, dtype=np.float64)
        for index in range(self.state_count):
            belief, model = self.state_pair(index)
            energies[index] = self.kappa_belief * kl_laws(belief, target_belief)
            energies[index] += self.kappa_model * kl_laws(model, target_model)
        energies -= energies.min()
        weights = np.exp(-energies)
        return weights / weights.sum()

    def attention_rows(self, configuration: str) -> dict[str, np.ndarray]:
        """Return the declared per-channel row matrices of one graph configuration.

        A model may declare its rows outright, which is what a genuinely
        bi-directed instance needs: with both arcs of a pair present the two
        directions carry independent weights, and no symmetric rule generates
        them. When no rows are declared the two built-in configurations are used.

        Rows are indexed by receiver and normalized over sources, with the self
        loop always admitted so that no row is forced to be a point mass. The two
        configurations are the declared finite support of the graph variable.
        """
        if self.declared_rows is not None:
            declared: dict[str, np.ndarray] = {}
            for name, channel, matrix in self.declared_rows:
                if name == configuration:
                    declared[channel] = np.array(matrix, dtype=np.float64)
            if set(declared) != {"belief", "model"}:
                raise ValueError("declared rows must cover both channels")
            for matrix in declared.values():
                if not np.allclose(matrix.sum(axis=1), 1.0, atol=1e-12):
                    raise ValueError("declared rows must be normalized over sources")
            return declared
        size = len(self.agents)
        index_of = {agent: position for position, agent in enumerate(self.agents)}
        rows: dict[str, np.ndarray] = {}
        for channel in ("belief", "model"):
            matrix = np.zeros((size, size), dtype=np.float64)
            for receiver in self.agents:
                sources = [receiver, *self.graph.sources_of(receiver)]
                sources = list(dict.fromkeys(sources))
                position = index_of[receiver]
                if configuration == "uniform":
                    for source in sources:
                        matrix[position, index_of[source]] = 1.0 / len(sources)
                elif configuration == "peaked":
                    external = [s for s in sources if s != receiver]
                    if not external:
                        matrix[position, position] = 1.0
                    else:
                        matrix[position, position] = 0.3
                        for source in external:
                            matrix[position, index_of[source]] = 0.7 / len(external)
                else:
                    raise ValueError("row configuration must be 'uniform' or 'peaked'")
            rows[channel] = matrix
        return rows

    def edge_event_law(self, configuration: str, channel: str) -> np.ndarray:
        """Return the directed edge-event law eta[receiver, source] of one channel.

        This is the transportable graph object: a probability law on ordered pairs
        and a family of gauge-invariant scalars. It is the receiver occupancy times
        the receiver row, and it sums to one over ordered pairs.
        """
        rows = self.attention_rows(configuration)[channel]
        occupancy = self.alpha_belief if channel == "belief" else self.alpha_model
        weights = np.array([float(value) for value in occupancy], dtype=np.float64)
        return weights[:, None] * rows


def crp_partition_prior(partition: Partition, concentration: Fraction) -> Fraction:
    """Return the exact Ewens or Chinese-restaurant prior mass of a set partition."""
    if concentration <= 0:
        raise ValueError("concentration must be positive")
    size = sum(len(block) for block in partition)
    numerator = concentration ** len(partition)
    for block in partition:
        for step in range(1, len(block)):
            numerator *= step
    denominator = Fraction(1)
    for step in range(size):
        denominator *= concentration + step
    return Fraction(numerator) / denominator


def build_reference_model() -> FalsificationModel:
    """Return the declared six-agent two-cycle instance of the design."""
    belief_representation = CyclicRepresentation(GROUP_ORDER, 1, "belief")
    model_representation = CyclicRepresentation(GROUP_ORDER, 2, "model")
    graph = TwoChannelGraph(
        order=GROUP_ORDER,
        vertices=(1, 2, 3, 4, 5, 6),
        edges=REFERENCE_EDGES,
        belief_elements=REFERENCE_BELIEF_ELEMENTS,
        model_elements=REFERENCE_MODEL_ELEMENTS,
    )
    return FalsificationModel(
        name="reference",
        belief_representation=belief_representation,
        model_representation=model_representation,
        belief_family=orbit(belief_representation, BELIEF_SEED),
        model_family=orbit(model_representation, MODEL_SEED),
        graph=graph,
        alpha_belief=REFERENCE_ALPHA_BELIEF,
        alpha_model=REFERENCE_ALPHA_MODEL,
        parent_labels=("A1", "A2", "A3"),
        candidate_partitions=REFERENCE_PARTITIONS,
        kappa_belief=2.0,
        kappa_model=2.0,
        crp_concentration=Fraction(1),
        identity_holonomy_weight=Fraction(1, 4),
        row_configurations=("uniform", "peaked"),
    )


def build_reduced_model() -> FalsificationModel:
    """Return the three-agent cut-down used for the independent flat enumeration.

    Cycle A is retained in full, so the belief channel keeps its nontrivial
    holonomy and the model channel stays flat. Both channels remain live, and the
    joint is small enough to enumerate without exploiting any factorization, which
    is what makes the direct route a genuinely independent computation rather than
    a rearrangement of the decomposition.
    """
    reference = build_reference_model()
    graph = reference.graph.induced((1, 2, 3))
    total_belief = sum(REFERENCE_ALPHA_BELIEF[:3])
    total_model = sum(REFERENCE_ALPHA_MODEL[:3])
    return FalsificationModel(
        name="reduced",
        belief_representation=reference.belief_representation,
        model_representation=reference.model_representation,
        belief_family=reference.belief_family,
        model_family=reference.model_family,
        graph=graph,
        alpha_belief=tuple(value / total_belief for value in REFERENCE_ALPHA_BELIEF[:3]),
        alpha_model=tuple(value / total_model for value in REFERENCE_ALPHA_MODEL[:3]),
        parent_labels=("A1", "A2"),
        candidate_partitions=REDUCED_PARTITIONS,
        kappa_belief=2.0,
        kappa_model=2.0,
        crp_concentration=Fraction(1),
        identity_holonomy_weight=Fraction(1, 4),
        row_configurations=("uniform", "peaked"),
    )


def build_null_model(seed: int) -> FalsificationModel:
    """Return a null-control instance with randomized transports and beliefs.

    The graph skeleton, the occupancies, the candidate partitions, and every
    kernel family are held fixed; only the edge group elements are randomized and
    the belief family is replaced by a random orbit. A pipeline that still reports
    block formation here is detecting its own blocking algorithm rather than the
    system, which is why this control is mandatory rather than optional.
    """
    reference = build_reference_model()
    generator = np.random.default_rng(seed)
    edge_count = len(reference.graph.edges)
    belief_elements = tuple(int(k) for k in generator.integers(0, GROUP_ORDER, edge_count))
    model_elements = tuple(int(k) for k in generator.integers(0, GROUP_ORDER, edge_count))
    weights = generator.integers(1, 7, GROUP_ORDER)
    seed_law = tuple(Fraction(int(w), int(weights.sum())) for w in weights)
    graph = TwoChannelGraph(
        order=GROUP_ORDER,
        vertices=reference.graph.vertices,
        edges=reference.graph.edges,
        belief_elements=belief_elements,
        model_elements=model_elements,
    )
    return FalsificationModel(
        name=f"null-{seed}",
        belief_representation=reference.belief_representation,
        model_representation=reference.model_representation,
        belief_family=orbit(reference.belief_representation, seed_law),
        model_family=reference.model_family,
        graph=graph,
        alpha_belief=reference.alpha_belief,
        alpha_model=reference.alpha_model,
        parent_labels=reference.parent_labels,
        candidate_partitions=reference.candidate_partitions,
        kappa_belief=reference.kappa_belief,
        kappa_model=reference.kappa_model,
        crp_concentration=reference.crp_concentration,
        identity_holonomy_weight=reference.identity_holonomy_weight,
        row_configurations=reference.row_configurations,
    )


__all__ = [
    "REDUCED_SINGLETON_PARTITION",
    "FalsificationModel",
    "Partition",
    "build_null_model",
    "build_reduced_model",
    "build_reference_model",
    "crp_partition_prior",
    "kl_laws",
    "transported",
]
