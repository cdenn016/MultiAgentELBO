r"""Phase three: the cocycle flow, its declared measurements, and linearization.

C3 failed, so what iterates here is a typed cocycle, one map per level pair,
not an autonomous flow on coupling space. This module implements what the
2026-08-17 amendment declares and nothing stronger: homogeneous cycle
instances as declared seeds, iteration by consecutive-block steps, the C6
composition defect between staged and direct routes, the C7 fixed-ray
comparison on the reduced homogeneous coupling space, and the level-local
linearization of the reduced self-map at a declared ratio. Every number this
module produces is level-local cocycle data; no fixed-point, relevance, or
universality claim is licensed by any of it.

A homogeneous cycle instance carries the same site table at every site, the
same pair table along every edge in cycle orientation, and the same group
element on every edge per channel. Consecutive blocking preserves this
symmetry exactly, because rotation by one coarse site is rotation by the
ratio at the fine level, and the residual per-site deviation is reported as
the homogeneity defect rather than assumed away. The reduced coupling space
at cycle length at least three is one anchored site table and one anchored
pair table; the 2-cycle merges both edge directions into a single pair table
and leaves the reduced type, so ray comparisons stop above it, as declared.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import math
from pathlib import Path
from typing import Sequence

import numpy as np

from ..cuda_backend import Backend
from .closure_residual import _blocked_action, _divergence_table
from .contraction_backend import iterated_step_via_worker
from .coupling_readback import (
    PairwiseCouplings,
    PairwiseInstance,
    RescalingStep,
    _kernel_model,
    couplings_action,
    iterated_step,
    mobius_couplings,
)
from .two_channel_gauge import DirectedEdge, TwoChannelGraph

CHANNELS = ("belief", "model")
GROUP_ORDER = 3


def homogeneous_cycle_instance(
    length: int,
    site_table: Sequence[Fraction],
    pair_table: Sequence[Sequence[Fraction]],
    belief_element: int = 1,
    model_element: int = 0,
) -> PairwiseInstance:
    """Return the declared homogeneous cycle instance of one length.

    The pair table is declared in cycle orientation, indexed by the receiver
    site's state and then the next site's state; the wrap edge stores its
    transpose because the anchored parameter vector keys pairs by ascending
    position. Length two is refused: its two arcs form a reciprocal pair and
    its single pair table merges both directions, which is not the declared
    homogeneous type.
    """
    if type(length) is not int or length < 3:
        raise ValueError("a homogeneous cycle needs at least three sites")
    size = len(site_table)
    site = tuple(Fraction(value) for value in site_table)
    pair = tuple(tuple(Fraction(value) for value in row) for row in pair_table)
    if any(len(row) != size for row in pair) or len(pair) != size:
        raise ValueError("the pair table must be square on the site state space")
    edges = tuple(
        DirectedEdge(position + 1, (position + 1) % length + 1)
        for position in range(length)
    )
    graph = TwoChannelGraph(
        order=GROUP_ORDER,
        vertices=tuple(range(1, length + 1)),
        edges=edges,
        belief_elements=(int(belief_element) % GROUP_ORDER,) * length,
        model_elements=(int(model_element) % GROUP_ORDER,) * length,
    )
    transposed = tuple(tuple(pair[right][left] for right in range(size)) for left in range(size))
    pairs = []
    for position in range(length - 1):
        pairs.append(((position, position + 1), pair))
    pairs.append(((0, length - 1), transposed))
    couplings = PairwiseCouplings(
        width=length,
        constant=Fraction(0),
        sites=(site,) * length,
        pairs=tuple(sorted(pairs)),
    )
    return PairwiseInstance(graph=graph, couplings=couplings)


def homogeneous_circulant_instance(
    length: int,
    offsets: Sequence[int],
    site_table: Sequence[Fraction],
    pair_table: Sequence[Sequence[Fraction]],
    belief_element: int = 1,
    model_element: int = 0,
) -> PairwiseInstance:
    """Return the declared homogeneous circulant instance of amendment 3.

    Every site carries the seed site table; every edge of every declared
    offset carries the seed pair table in receiver-to-source orientation,
    stored transposed wherever the ascending position key reverses that
    orientation. The belief element sits on offset-one edges only, so chords
    thicken the coupling boundary without touching the declared holonomy.
    Offsets must stay strictly below half the length, which excludes both
    reciprocal pairs and coincident unordered pairs.
    """
    if type(length) is not int or length < 3:
        raise ValueError("a circulant instance needs at least three sites")
    declared = tuple(sorted(set(int(offset) for offset in offsets)))
    if not declared or declared[0] < 1 or 2 * declared[-1] >= length:
        raise ValueError("offsets must lie strictly between zero and half the length")
    size = len(site_table)
    site = tuple(Fraction(value) for value in site_table)
    pair = tuple(tuple(Fraction(value) for value in row) for row in pair_table)
    if any(len(row) != size for row in pair) or len(pair) != size:
        raise ValueError("the pair table must be square on the site state space")
    transposed = tuple(
        tuple(pair[right][left] for right in range(size)) for left in range(size)
    )
    edges: list[DirectedEdge] = []
    belief_elements: list[int] = []
    pairs: list[tuple[tuple[int, int], tuple[tuple[Fraction, ...], ...]]] = []
    for offset in declared:
        for position in range(length):
            source_position = (position + offset) % length
            edges.append(DirectedEdge(position + 1, source_position + 1))
            belief_elements.append(
                int(belief_element) % GROUP_ORDER if offset == 1 else 0
            )
            if position < source_position:
                pairs.append(((position, source_position), pair))
            else:
                pairs.append(((source_position, position), transposed))
    graph = TwoChannelGraph(
        order=GROUP_ORDER,
        vertices=tuple(range(1, length + 1)),
        edges=tuple(edges),
        belief_elements=tuple(belief_elements),
        model_elements=(int(model_element) % GROUP_ORDER,) * len(edges),
    )
    couplings = PairwiseCouplings(
        width=length,
        constant=Fraction(0),
        sites=(site,) * length,
        pairs=tuple(sorted(pairs)),
    )
    return PairwiseInstance(graph=graph, couplings=couplings)


@dataclass(frozen=True)
class PairRetention:
    """Measurement M-bundle: one-step pair retention at declared multiplicity."""

    length: int
    offsets: tuple[int, ...]
    ratio: int
    cut_per_boundary: int
    fine_pair_sup: float
    coarse_pair_sup: float
    retention: float
    omitted_sup: float


def one_step_pair_retention(
    instance: PairwiseInstance,
    ratio: int,
) -> PairRetention:
    """Measure the one-step pair retention factor of amendment 3.

    The instance is blocked consecutively at the declared ratio through the
    audited contraction, the coarse couplings are read back by the exact
    Moebius route with every coarse pair admitted, and the retention factor is
    the ratio of coarse to fine pairwise sup norms. No threshold is attached:
    the number is the result.
    """
    length = len(instance.graph.vertices)
    blocks = consecutive_blocks(length, int(ratio))
    model = _kernel_model(instance.graph, "pair-retention")
    action_array = couplings_action(instance.couplings)
    weights = np.exp(-(action_array - action_array.min()))
    action, _ = _blocked_action(model, weights, blocks)
    coarse_length = length // int(ratio)
    admitted = tuple(
        (left, right)
        for left in range(coarse_length)
        for right in range(left + 1, coarse_length)
    )
    coarse, omitted = mobius_couplings(action, admitted)
    fine_sup = max(
        abs(float(value))
        for _, table in instance.couplings.pairs
        for row in table
        for value in row
    )
    coarse_sup = max(
        (
            abs(float(value))
            for _, table in coarse.pairs
            for row in table
            for value in row
        ),
        default=0.0,
    )
    offsets = tuple(
        sorted(
            {
                min(
                    (edge.source - edge.receiver) % length,
                    (edge.receiver - edge.source) % length,
                )
                for edge in instance.graph.edges
            }
        )
    )
    return PairRetention(
        length=length,
        offsets=offsets,
        ratio=int(ratio),
        cut_per_boundary=sum(offsets),
        fine_pair_sup=fine_sup,
        coarse_pair_sup=coarse_sup,
        retention=coarse_sup / fine_sup if fine_sup else 0.0,
        omitted_sup=float(omitted),
    )


def consecutive_blocks(length: int, ratio: int) -> tuple[tuple[int, ...], ...]:
    """Return the consecutive blocking of one cycle length at one ratio."""
    if type(ratio) is not int or ratio < 2:
        raise ValueError("a blocking ratio must be an integer at least two")
    if length % ratio != 0:
        raise ValueError("the ratio must divide the cycle length")
    return tuple(
        tuple(range(start + 1, start + ratio + 1))
        for start in range(0, length, ratio)
    )


def cocycle_flow(
    instance: PairwiseInstance,
    ratios: Sequence[int],
    *,
    work_root: Path | None = None,
    worker_backend: Backend | None = None,
    worker_min_sites: int = 8,
) -> tuple[RescalingStep, ...]:
    """Run the declared sequence of typed steps, largest contractions on the worker.

    Each step blocks the current cycle by its declared ratio and reads the
    couplings back; the next step runs on the returned instance. Steps whose
    site count reaches ``worker_min_sites`` are routed through the worker
    protocol when a backend is declared, and run in process otherwise.
    """
    steps: list[RescalingStep] = []
    current = instance
    for position, ratio in enumerate(ratios):
        length = len(current.graph.vertices)
        blocks = consecutive_blocks(length, int(ratio))
        if worker_backend is not None and length >= worker_min_sites:
            if work_root is None:
                raise ValueError("worker routing needs a declared work root")
            step = iterated_step_via_worker(
                current,
                blocks,
                work_root=work_root / f"flow-step-{position}",
                backend=worker_backend,
            )
        else:
            step = iterated_step(current, blocks)
        steps.append(step)
        if step.instance is None:
            if position != len(ratios) - 1:
                raise ValueError("the flow reached one site with ratios left to spend")
            break
        current = step.instance
    return tuple(steps)


def _oriented_pair_tables(couplings: PairwiseCouplings) -> list[np.ndarray]:
    """Return every pair table in cycle orientation, wrap edge untransposed."""
    width = couplings.width
    tables: list[np.ndarray] = []
    for (left, right), table in couplings.pairs:
        array = np.array([[float(value) for value in row] for row in table])
        if (left, right) == (0, width - 1) and width > 2:
            array = array.T
        tables.append(array)
    return tables


def homogeneity_defect(couplings: PairwiseCouplings) -> float:
    """Return the sup deviation of the coupling tables from site-one's copies."""
    sites = [
        np.array([float(value) for value in table]) for table in couplings.sites
    ]
    defect = max(
        (float(np.abs(table - sites[0]).max()) for table in sites[1:]),
        default=0.0,
    )
    pairs = _oriented_pair_tables(couplings)
    if pairs:
        defect = max(
            defect,
            max(
                (float(np.abs(table - pairs[0]).max()) for table in pairs[1:]),
                default=0.0,
            ),
        )
    return defect


def reduced_couplings(couplings: PairwiseCouplings) -> np.ndarray:
    """Return the reduced homogeneous parameter vector, site block then pair block."""
    if couplings.width < 3:
        raise ValueError("the reduced type needs a cycle of at least three sites")
    site = np.array([float(value) for value in couplings.sites[0]])
    pair = _oriented_pair_tables(couplings)[0]
    return np.concatenate([site, pair.reshape(-1)])


@dataclass(frozen=True)
class RayComparison:
    """Check C7: one level's reduced couplings against the previous, up to scale."""

    scale: float
    relative_residual: float


def ray_comparison(
    fine: PairwiseCouplings,
    coarse: PairwiseCouplings,
) -> RayComparison:
    """Return the least-squares scale and rescaled residual between two levels."""
    fine_vector = reduced_couplings(fine)
    coarse_vector = reduced_couplings(coarse)
    weight = float(fine_vector @ fine_vector)
    if weight == 0.0:
        raise ValueError("the fine level carries no couplings to fit a ray against")
    scale = float(coarse_vector @ fine_vector) / weight
    ceiling = float(np.abs(coarse_vector).max())
    if ceiling == 0.0:
        raise ValueError("the coarse level carries no couplings to compare")
    residual = float(np.abs(coarse_vector - scale * fine_vector).max()) / ceiling
    return RayComparison(scale=scale, relative_residual=residual)


@dataclass(frozen=True)
class CompositionDefect:
    """Check C6: staged against direct blocking of the same instance."""

    staged_ratios: tuple[int, ...]
    direct_ratios: tuple[int, ...]
    defect: float


def _coupling_vector(couplings: PairwiseCouplings) -> np.ndarray:
    """Return every order-one and order-two component as one flat vector."""
    parts = [
        np.array([float(value) for value in table]) for table in couplings.sites
    ]
    parts.extend(
        np.array([[float(value) for value in row] for row in table]).reshape(-1)
        for _, table in couplings.pairs
    )
    return np.concatenate(parts)


def composition_defect(
    instance: PairwiseInstance,
    staged_ratios: Sequence[int],
    direct_ratios: Sequence[int],
    *,
    work_root: Path | None = None,
    worker_backend: Backend | None = None,
) -> CompositionDefect:
    """Measure C6 on one instance: two declared routes to the same final level.

    Both routes must reach the same cycle length, so the coupling vectors are
    the same type and the comparison is entry for entry on the Moebius
    read-back, which is exact and deterministic. No threshold is declared,
    because none is justifiable in advance; the number is the result.
    """
    staged = tuple(int(ratio) for ratio in staged_ratios)
    direct = tuple(int(ratio) for ratio in direct_ratios)
    if not staged or not direct:
        raise ValueError("both routes must declare at least one ratio")
    if int(np.prod(staged)) != int(np.prod(direct)):
        raise ValueError("the two routes must contract by the same total ratio")
    staged_steps = cocycle_flow(
        instance,
        staged,
        work_root=None if work_root is None else work_root / "staged",
        worker_backend=worker_backend,
    )
    direct_steps = cocycle_flow(
        instance,
        direct,
        work_root=None if work_root is None else work_root / "direct",
        worker_backend=worker_backend,
    )
    left = _coupling_vector(staged_steps[-1].mobius)
    right = _coupling_vector(direct_steps[-1].mobius)
    return CompositionDefect(
        staged_ratios=staged,
        direct_ratios=direct,
        defect=float(np.abs(left - right).max()),
    )


@dataclass(frozen=True)
class ReducedLinearization:
    """Level-local linearization of the reduced homogeneous self-map."""

    length: int
    ratio: int
    epsilon: float
    jacobian: np.ndarray
    eigenvalues: tuple[complex, ...]


def _reduced_step_map(
    instance: PairwiseInstance,
    ratio: int,
    reduced: np.ndarray,
) -> np.ndarray:
    """Apply one Moebius-read-back step to one reduced parameter vector.

    The reduced vector is tiled back onto the instance's graph, blocked by
    consecutive blocks at the declared ratio, and the coarse Moebius couplings
    are reduced again. The Moebius route is used because it is deterministic
    and exact; the variational route agrees with it within the instrument
    resolution wherever the step is resolved.
    """
    length = len(instance.graph.vertices)
    size = len(instance.couplings.sites[0])
    site = tuple(Fraction(float(value)) for value in reduced[:size])
    pair = tuple(
        tuple(Fraction(float(value)) for value in row)
        for row in reduced[size:].reshape(size, size)
    )
    tiled = homogeneous_cycle_instance(
        length,
        site,
        pair,
        belief_element=instance.graph.belief_elements[0],
        model_element=instance.graph.model_elements[0],
    )
    blocks = consecutive_blocks(length, ratio)
    model = _kernel_model(tiled.graph, "reduced-step")
    action_array = couplings_action(tiled.couplings)
    weights = np.exp(-(action_array - action_array.min()))
    action, _ = _blocked_action(model, weights, blocks)
    coarse_length = length // ratio
    admitted = tuple(
        sorted(
            {
                tuple(sorted((position, (position + 1) % coarse_length)))
                for position in range(coarse_length)
            }
        )
    )
    coarse, _ = mobius_couplings(action, admitted)
    return reduced_couplings(coarse)


REGENERATION_TEMPERATURE = 1.0


@dataclass(frozen=True)
class RegeneratedInstance:
    """One coarse instance with its attention regenerated per amendment 4."""

    instance: PairwiseInstance
    rows: tuple[tuple[str, tuple[tuple[float, ...], ...]], ...]
    injected_pair_sup: float


def regenerated_instance(
    step: RescalingStep,
    tau: float = REGENERATION_TEMPERATURE,
) -> RegeneratedInstance:
    r"""Regenerate the coarse level's attention and fold it into the couplings.

    Per channel and per coarse edge, the flow-averaged transported divergence
    $\overline D^c_{IJ}$ is computed under the step's own coarse flow law with
    the coarse connection's element; rows over each receiver's sources plus the
    self loop are $\beta \propto \exp(-\overline D/\tau)$; occupancies are the
    declared uniform $1/m$; and the regenerated alignment energy
    $\sum_c \kappa_c\, \alpha \beta\, D^c(p_I, p_J)$ is added to the coarse
    action before the read-back. The temperature and the uniform occupancies
    are declared, not derived. Factorized theories are not invariant under the
    regenerated map, by construction: the added term is a pair-sector source
    built from the conserved connection.
    """
    if step.connection is None or step.instance is None:
        raise ValueError("regeneration needs a step with a coarse connection")
    if not tau > 0.0:
        raise ValueError("the declared temperature must be positive")
    graph = step.connection.graph
    model = _kernel_model(graph, "regenerated-attention")
    width = len(graph.vertices)
    size = model.state_count
    flow = np.empty((size,) * width)
    for state, weight in step.flow_weights.items():
        flow[state] = float(weight)
    kappa = {"belief": model.kappa_belief, "model": model.kappa_model}
    injected = np.zeros((size,) * width)
    rows_report: list[tuple[str, tuple[tuple[float, ...], ...]]] = []
    for channel in CHANNELS:
        averages = np.zeros((width, width))
        tables: dict[int, np.ndarray] = {}
        for position, edge in enumerate(graph.edges):
            element = graph.channel_elements(channel)[position]
            table = _divergence_table(model, channel, element)
            tables[position] = table
            axes = (edge.receiver - 1, edge.source - 1)
            others = tuple(axis for axis in range(width) if axis not in axes)
            marginal = flow.sum(axis=others)
            if axes[0] > axes[1]:
                marginal = marginal.T
            averages[axes[0], axes[1]] = float(np.sum(marginal * table))
        weights = np.zeros((width, width))
        for receiver in graph.vertices:
            weights[receiver - 1, receiver - 1] = 1.0
            for source in graph.sources_of(receiver):
                weights[receiver - 1, source - 1] = math.exp(
                    -averages[receiver - 1, source - 1] / tau
                )
        rows = weights / weights.sum(axis=1, keepdims=True)
        rows_report.append(
            (channel, tuple(tuple(float(v) for v in row) for row in rows))
        )
        for position, edge in enumerate(graph.edges):
            receiver = edge.receiver - 1
            source = edge.source - 1
            strength = kappa[channel] * (1.0 / width) * rows[receiver, source]
            factor = tables[position]
            if receiver > source:
                factor = factor.T
            shape = [1] * width
            shape[min(receiver, source)] = size
            shape[max(receiver, source)] = size
            injected = injected + strength * factor.reshape(shape)
    total = couplings_action(step.variational) + injected
    action = {
        state: Fraction(float(total[state]))
        for state in product(range(size), repeat=width)
    }
    admitted = tuple(
        sorted(
            {
                tuple(sorted((edge.receiver - 1, edge.source - 1)))
                for edge in graph.edges
            }
        )
    )
    couplings, _ = mobius_couplings(action, admitted)
    injected_action = {
        state: Fraction(float(injected[state]))
        for state in product(range(size), repeat=width)
    }
    injected_couplings, _ = mobius_couplings(injected_action, admitted)
    injected_sup = max(
        (
            abs(float(value))
            for _, table in injected_couplings.pairs
            for row in table
            for value in row
        ),
        default=0.0,
    )
    return RegeneratedInstance(
        instance=PairwiseInstance(graph=graph, couplings=couplings),
        rows=tuple(rows_report),
        injected_pair_sup=injected_sup,
    )


def regenerated_fixed_point(
    instance: PairwiseInstance,
    ratio: int,
    tau: float = REGENERATION_TEMPERATURE,
    tolerance: float = 1.0e-9,
    max_iterations: int = 200,
) -> ReducedFixedPoint:
    """Iterate the regenerated composite: block, regenerate, re-tile, repeat.

    Identical to the passive fixed-point iteration except that each level's
    attention is regenerated before the re-tiling, so the pair sector has a
    source and the factorized subspace is no longer invariant. Convergence is
    reported, not assumed.
    """
    length = len(instance.graph.vertices)
    reduced = reduced_couplings(instance.couplings)
    size = len(instance.couplings.sites[0])
    change = float("inf")
    iterations = 0
    current = instance
    while iterations < int(max_iterations):
        step = iterated_step(current, consecutive_blocks(length, int(ratio)))
        regenerated = regenerated_instance(step, tau)
        image = reduced_couplings(regenerated.instance.couplings)
        change = float(np.abs(image - reduced).max())
        reduced = image
        iterations += 1
        if change <= tolerance:
            break
        current = homogeneous_cycle_instance(
            length,
            tuple(Fraction(float(value)) for value in reduced[:size]),
            tuple(
                tuple(Fraction(float(value)) for value in row)
                for row in reduced[size:].reshape(size, size)
            ),
            belief_element=instance.graph.belief_elements[0],
            model_element=instance.graph.model_elements[0],
        )
    return ReducedFixedPoint(
        length=length,
        ratio=int(ratio),
        iterations=iterations,
        final_change=change,
        converged=change <= tolerance,
        vector=reduced,
    )


@dataclass(frozen=True)
class ReducedFixedPoint:
    """Measurement M-fix: the fixed structure of one reduced self-map.

    What is fixed is a point of the declared composite, blocking followed by
    the self-similar re-tiling identification, at one declared ratio. It is
    not a fixed point of an autonomous flow, and the ratio dependence of the
    fixed vector is measured rather than assumed away.
    """

    length: int
    ratio: int
    iterations: int
    final_change: float
    converged: bool
    vector: np.ndarray


def reduced_fixed_point(
    instance: PairwiseInstance,
    ratio: int,
    tolerance: float = 1.0e-9,
    max_iterations: int = 200,
    *,
    work_root: Path | None = None,
    worker_backend: Backend | None = None,
    worker_min_sites: int = 8,
) -> ReducedFixedPoint:
    """Iterate the reduced self-map from the instance's couplings to its rest.

    Iteration is licensed by measurement, not assumption: the declared seed's
    Jacobian spectrum sits inside the unit circle, so the map is a local
    contraction there, and the loop reports its own convergence rather than
    asserting it. Instances at or above the worker threshold route each
    application through the worker protocol when a backend is declared.
    """
    length = len(instance.graph.vertices)
    reduced = reduced_couplings(instance.couplings)
    change = float("inf")
    iterations = 0
    while iterations < int(max_iterations):
        if worker_backend is not None and length >= worker_min_sites:
            if work_root is None:
                raise ValueError("worker routing needs a declared work root")
            image = _reduced_worker_step(
                instance,
                int(ratio),
                reduced,
                work_root=work_root / f"fixed-point-{iterations}",
                worker_backend=worker_backend,
            )
        else:
            image = _reduced_step_map(instance, int(ratio), reduced)
        change = float(np.abs(image - reduced).max())
        reduced = image
        iterations += 1
        if change <= tolerance:
            break
    return ReducedFixedPoint(
        length=length,
        ratio=int(ratio),
        iterations=iterations,
        final_change=change,
        converged=change <= tolerance,
        vector=reduced,
    )


def _reduced_worker_step(
    instance: PairwiseInstance,
    ratio: int,
    reduced: np.ndarray,
    *,
    work_root: Path,
    worker_backend: Backend,
) -> np.ndarray:
    """Apply one reduced step with the contraction routed through the worker."""
    length = len(instance.graph.vertices)
    size = len(instance.couplings.sites[0])
    tiled = homogeneous_cycle_instance(
        length,
        tuple(Fraction(float(value)) for value in reduced[:size]),
        tuple(
            tuple(Fraction(float(value)) for value in row)
            for row in reduced[size:].reshape(size, size)
        ),
        belief_element=instance.graph.belief_elements[0],
        model_element=instance.graph.model_elements[0],
    )
    step = iterated_step_via_worker(
        tiled,
        consecutive_blocks(length, ratio),
        work_root=work_root,
        backend=worker_backend,
    )
    return reduced_couplings(step.mobius)


def reduced_linearization(
    instance: PairwiseInstance,
    ratio: int,
    epsilon: float = 1.0e-5,
    at: np.ndarray | None = None,
) -> ReducedLinearization:
    """Return the central-difference Jacobian of the reduced self-map at one point.

    The self-map exists only while both levels are cycles of length at least
    three, and its spectrum is level-local contraction data of the cocycle at
    the declared point; per the amendment it is not a set of relevance
    exponents and must not be reported as one.
    """
    length = len(instance.graph.vertices)
    if length // int(ratio) < 3:
        raise ValueError("the linearization needs the coarse level to stay a cycle")
    base = (
        reduced_couplings(instance.couplings)
        if at is None
        else np.asarray(at, dtype=np.float64).copy()
    )
    dimension = base.size
    jacobian = np.empty((dimension, dimension))
    for index in range(dimension):
        forward = base.copy()
        backward = base.copy()
        forward[index] += epsilon
        backward[index] -= epsilon
        jacobian[:, index] = (
            _reduced_step_map(instance, int(ratio), forward)
            - _reduced_step_map(instance, int(ratio), backward)
        ) / (2.0 * epsilon)
    eigenvalues = np.linalg.eigvals(jacobian)
    ordering = np.argsort(-np.abs(eigenvalues))
    return ReducedLinearization(
        length=length,
        ratio=int(ratio),
        epsilon=float(epsilon),
        jacobian=jacobian,
        eigenvalues=tuple(complex(value) for value in eigenvalues[ordering]),
    )


__all__ = [
    "CompositionDefect",
    "RayComparison",
    "ReducedFixedPoint",
    "ReducedLinearization",
    "PairRetention",
    "REGENERATION_TEMPERATURE",
    "RegeneratedInstance",
    "cocycle_flow",
    "reduced_fixed_point",
    "regenerated_fixed_point",
    "regenerated_instance",
    "composition_defect",
    "consecutive_blocks",
    "homogeneity_defect",
    "homogeneous_circulant_instance",
    "homogeneous_cycle_instance",
    "one_step_pair_retention",
    "ray_comparison",
    "reduced_couplings",
    "reduced_linearization",
]
