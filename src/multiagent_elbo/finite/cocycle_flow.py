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
from typing import Mapping, Sequence

import numpy as np

from ..cuda_backend import Backend
from .categorical_falsification_model import FalsificationModel
from .closure_residual import (
    _CONTRACTION_LETTERS,
    _block_bayes_kernel,
    _block_prior_vector,
    _blocked_action,
    _divergence_table,
)
from .holonomy_retention import block_transport_elements
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
SECTOR_READOUTS = ("charge", "first_member")
MI_CEILING_FLOOR = 1.0e-12


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
    parent_priors: Mapping[int, Sequence[float]] | None = None,
    anchor: Sequence[int] | None = None,
) -> PairRetention:
    """Measure the one-step pair retention factor of amendment 3.

    The instance is blocked consecutively at the declared ratio through the
    audited contraction, the coarse couplings are read back by the exact
    Moebius route with every coarse pair admitted, and the retention factor is
    the ratio of coarse to fine pairwise sup norms. No threshold is attached:
    the number is the result.

    ``parent_priors`` declares one parent law per block root; the default
    leaves the declared law fixed at every root, which is not what a regauging
    does to it. ``anchor`` is the Moebius ground state, a gauge fixing that the
    sup norm moves with; sweep it with
    :func:`~multiagent_elbo.finite.coupling_readback.anchor_swept_sup` before
    publishing a sup-norm number.
    """
    length = len(instance.graph.vertices)
    blocks = consecutive_blocks(length, int(ratio))
    model = _kernel_model(instance.graph, "pair-retention")
    action_array = couplings_action(instance.couplings)
    weights = np.exp(-(action_array - action_array.min()))
    action, _ = _blocked_action(model, weights, blocks, parent_priors)
    coarse_length = length // int(ratio)
    admitted = tuple(
        (left, right)
        for left in range(coarse_length)
        for right in range(left + 1, coarse_length)
    )
    coarse, omitted = mobius_couplings(action, admitted, anchor)
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


@dataclass(frozen=True)
class CapacityRetention:
    """Measurement M-capacity: one-step retention with sector-carrying parents."""

    length: int
    offsets: tuple[int, ...]
    ratio: int
    sector_count: int
    fine_pair_sup: float
    coarse_pair_sup: float
    retention: float


def _belief_orbit_coordinates(model: FalsificationModel) -> np.ndarray:
    """Return, per joint state, the orbit coordinate of its belief component.

    The coordinate is the unique group element carrying the first family member
    onto the state's belief law; it exists and is unique because the family is
    a free orbit of an asymmetric seed.
    """
    order = model.graph.order
    base = model.belief_family[0]
    coordinate_of_law = {}
    for k in range(order):
        coordinate_of_law[model.belief_representation.act(k, base)] = k
    model_size = len(model.model_family)
    return np.array(
        [
            coordinate_of_law[model.belief_family[index // model_size]]
            for index in range(model.state_count)
        ],
        dtype=np.int64,
    )


def _capacity_marginal(
    instance: PairwiseInstance,
    ratio: int,
    sector_count: int,
    constant_sector: bool,
    readout: str = "charge",
    parent_priors: Mapping[int, Sequence[float]] | None = None,
) -> tuple[np.ndarray, int, tuple[tuple[int, ...], ...], np.ndarray]:
    r"""Contract one instance through the sector-carrying blocking kernel.

    Returns the unnormalized coarse marginal over the parent alphabet, the
    alphabet size, the blocking, and the fine child-weight tensor. The parent
    label is $(p, s)$ with $s(x_B)$ a deterministic $n_s$-valued readout of the
    block's children, and the kernel is the audited Bayes kernel times that
    readout, $T((p,s) \mid x_B) = T(p \mid x_B)\, \mathbf 1[s = s(x_B)]$. This
    is the single contraction both M-capacity and M-info read from.

    Two things about the sector axis, both established by the 2026-08-18
    lab-versus-theory audit and both load-bearing for how a gain is read.

    ``constant_sector`` collapses the axis, reproducing the plain nine-state
    blocking. That is an identity, not an independent check: the collapsed law
    is the nine-state law by construction, so the control cannot fail and
    cannot testify to anything about the charge.

    ``readout`` selects which same-cardinality label the axis carries.
    ``"charge"`` is the declared root-framed belief-channel $Z_3$ charge
    $s(x_B) = \sum_{a \in B}(k_a + t_a) mod n_s$. ``"first_member"`` is the
    declared control: the first member's own orbit coordinate, the same
    ingredient read at one site instead of summed over the block, carrying the
    same number of labels and no gauge charge. Because the enlarged label is a
    deterministic refinement of the nine-state one on both blocks, any readout
    at all satisfies $R_{\mathrm{MI}}(9 n_s) \ge R_{\mathrm{MI}}(9)$ by data
    processing; the sign of a sector gain is therefore a theorem and carries no
    information about the charge. Only the comparison against a same-cardinality
    non-charge readout does.
    """
    length = len(instance.graph.vertices)
    blocks = consecutive_blocks(length, int(ratio))
    model = _kernel_model(instance.graph, "capacity-retention")
    size = model.state_count
    order = model.graph.order
    action_array = couplings_action(instance.couplings)
    weights = np.exp(-(action_array - action_array.min()))
    coordinates = _belief_orbit_coordinates(model)
    if type(sector_count) is not int or sector_count < 1:
        raise ValueError("sector_count must be a positive integer")
    if readout not in SECTOR_READOUTS:
        raise ValueError(f"readout must be one of {SECTOR_READOUTS}")
    sectors = sector_count
    letters = _CONTRACTION_LETTERS
    if length + len(blocks) > len(letters):
        raise ValueError("the contraction exceeds the declared subscript pool")
    operands: list[np.ndarray] = [weights]
    subscripts: list[str] = [letters[: length]]
    output = ""
    for block_index, block in enumerate(blocks):
        label = letters[length + block_index]
        output += label
        base_kernel = _block_bayes_kernel(
            model, block, _block_prior_vector(model, block, parent_priors)
        )
        width = len(block)
        extended = np.zeros((size * sectors,) + (size,) * width)
        transports = block_transport_elements(model, block, "belief")
        grids = np.meshgrid(
            *[(coordinates + transports[agent]) % order for agent in block],
            indexing="ij",
        )
        if readout == "charge":
            charge = np.zeros((size,) * width, dtype=np.int64)
            for grid in grids:
                charge = charge + grid
        else:
            charge = np.array(grids[0], dtype=np.int64)
        charge = np.zeros((size,) * width, dtype=np.int64) if constant_sector else charge % sectors
        if not constant_sector and len(np.unique(charge)) < sectors:
            raise ValueError(
                "sector_count exceeds the reachable belief-channel charges of "
                "this block; unreachable sectors would carry zero mass"
            )
        for presentation in range(size):
            for sector in range(sectors):
                extended[presentation * sectors + sector] = base_kernel[
                    presentation
                ] * (charge == sector)
        operands.append(extended)
        subscripts.append(
            label
            + "".join(letters[agent - 1] for agent in block)
        )
    marginal = np.einsum(
        ",".join(subscripts) + "->" + output, *operands, optimize=True
    )
    coarse_width = len(blocks)
    if constant_sector:
        marginal = marginal.reshape(
            *[dim for _ in range(coarse_width) for dim in (size, sectors)]
        ).sum(axis=tuple(2 * position + 1 for position in range(coarse_width)))
        alphabet = size
    else:
        alphabet = size * sectors
    return marginal, alphabet, blocks, weights


def capacity_pair_retention(
    instance: PairwiseInstance,
    ratio: int,
    sector_count: int = GROUP_ORDER,
    constant_sector: bool = False,
    readout: str = "charge",
    parent_priors: Mapping[int, Sequence[float]] | None = None,
) -> CapacityRetention:
    r"""Measure M-capacity: one-step pair retention with sector-carrying parents.

    The parent label is $(p, s)$ with $s(x_B)$ the block's belief-channel $Z_3$
    charge, and the blocking kernel is the audited Bayes kernel times the
    deterministic sector readout, $T((p,s) \mid x_B) = T(p \mid x_B)\,
    \mathbf 1[s = s(x_B)]$, normalized over the enlarged label set by
    construction. The charge is root-framed: each member's orbit coordinate is
    carried into the block root frame by the spanning-tree transport before
    summing, $s(x_B) = \sum_{a \in B} (k_a + t_a) \bmod n_s$, matching the
    frame convention of the downward kernels; the family-referenced charge
    without the transports shifts under a sample-shift gauge (2026-08-18
    audit, F8). With ``constant_sector`` the readout is replaced by the
    constant label, which reproduces the nine-state retention exactly — an
    identity rather than an independent check, since the collapsed law *is*
    the nine-state law. The operative control is ``readout="first_member"``,
    a same-cardinality label carrying no gauge charge; the sector gain is only
    informative about the charge when quoted against it.
    """
    length = len(instance.graph.vertices)
    marginal, alphabet, blocks, _ = _capacity_marginal(
        instance, ratio, sector_count, constant_sector, readout, parent_priors
    )
    sectors = sector_count
    coarse_width = len(blocks)
    positive = marginal[marginal > 0.0]
    floor = float(positive.min())
    guarded = np.where(marginal > 0.0, marginal, floor * 1.0e-300)
    action = {
        state: Fraction(float(-np.log(guarded[state])))
        for state in product(range(alphabet), repeat=coarse_width)
    }
    admitted = tuple(
        (left, right)
        for left in range(coarse_width)
        for right in range(left + 1, coarse_width)
    )
    coarse, _ = mobius_couplings(action, admitted)
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
    return CapacityRetention(
        length=length,
        offsets=offsets,
        ratio=int(ratio),
        sector_count=1 if constant_sector else sectors,
        fine_pair_sup=fine_sup,
        coarse_pair_sup=coarse_sup,
        retention=coarse_sup / fine_sup if fine_sup else 0.0,
    )


@dataclass(frozen=True)
class InformationRetention:
    """Measurement M-info: one-step boundary mutual-information retention."""

    length: int
    offsets: tuple[int, ...]
    ratio: int
    sector_count: int
    fine_information: float
    coarse_information: float
    retention: float


def _mutual_information(joint: np.ndarray) -> float:
    r"""Return $I(X;Y)$ in nats of one unnormalized nonnegative joint table."""
    law = joint / joint.sum()
    product = law.sum(axis=1, keepdims=True) * law.sum(axis=0, keepdims=True)
    support = law > 0.0
    return float(np.sum(law[support] * np.log(law[support] / product[support])))


def capacity_information_retention(
    instance: PairwiseInstance,
    ratio: int,
    sector_count: int = GROUP_ORDER,
    constant_sector: bool = False,
    readout: str = "charge",
    parent_priors: Mapping[int, Sequence[float]] | None = None,
) -> InformationRetention:
    r"""Measure M-info: the boundary information a parent alphabet carries.

    The statistic is $R_{\mathrm{MI}} = I(P_1; P_2) / I(X_{B_1}; X_{B_2})$,
    the mutual information between the first two coarse parents under the
    coarse law against the same quantity between their child blocks under the
    fine law, both in nats and both by exact marginalization. The coarse law
    is the pushforward of the fine law through the per-block kernels and each
    parent depends only on its own block's children, so the data processing
    inequality gives $R_{\mathrm{MI}} \le 1$ as a theorem; what is measured
    is the fraction of that ceiling. Unlike the anchored sup norm, the
    statistic is a functional of the law alone: invariant under per-block
    parent relabelings and per-site state permutations, hence
    alphabet-comparable (amendment 9). The first adjacent pair is
    representative by homogeneity on the declared instances.

    Two limits on what a sector gain in this statistic means, both established
    by the 2026-08-18 lab-versus-theory audit.

    *The sign is a theorem, not evidence.* The enlarged label is a
    deterministic refinement of the nine-state one, applied identically on both
    blocks with the denominator unchanged, so $R_{\mathrm{MI}}$ can only rise
    by data processing — for every instance, ratio, coupling and readout. The
    ``constant_sector`` control collapses the axis and reproduces the
    nine-state value by construction, so it is an identity and not an
    independent check. Only a comparison against a same-cardinality non-charge
    readout (``readout="first_member"``) separates the gauge charge from the
    label count, and on the declared instances arbitrary same-cardinality
    readouts beat the charge by a wide margin.

    *It is not gauge-invariant by construction.* The parent law is data
    attached to the block root frame, and the production paths that do not
    thread ``parent_priors`` leave it fixed while everything else regauges, so
    the statistic drifts under the shift group (measured 3.5% at $k = 1$ and
    1.3% at $k = 3$, below the sector gain but not zero). Threading the
    re-expressed prior restores invariance to roundoff.
    """
    length = len(instance.graph.vertices)
    marginal, _, blocks, weights = _capacity_marginal(
        instance, ratio, sector_count, constant_sector, readout, parent_priors
    )
    coarse_width = len(blocks)
    if coarse_width < 2:
        raise ValueError("boundary information needs at least two blocks")
    size = weights.shape[0]
    width = len(blocks[0])
    fine_pair = weights.reshape((size**width,) * coarse_width).sum(
        axis=tuple(range(2, coarse_width))
    )
    coarse_pair = marginal.sum(axis=tuple(range(2, coarse_width)))
    fine_information = _mutual_information(fine_pair)
    coarse_information = _mutual_information(coarse_pair)
    if 0.0 < fine_information < MI_CEILING_FLOOR:
        raise ValueError(
            "the boundary mutual-information ceiling "
            f"{fine_information:.6e} nats is at roundoff scale; the retention "
            "ratio would divide one roundoff residue by another and is not a "
            "measurement. Declare a coupling that correlates the boundary, or "
            "report the ceiling alone."
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
    return InformationRetention(
        length=length,
        offsets=offsets,
        ratio=int(ratio),
        sector_count=1 if constant_sector else sector_count,
        fine_information=fine_information,
        coarse_information=coarse_information,
        retention=coarse_information / fine_information if fine_information else 0.0,
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


def regenerated_composition_defect(
    instance: PairwiseInstance,
    staged_ratios: Sequence[int],
    direct_ratios: Sequence[int],
    tau: float = REGENERATION_TEMPERATURE,
) -> CompositionDefect:
    """Measure RC6: the composition defect of regenerated flows.

    Each route regenerates at every intermediate level with edges; the direct
    route has no intermediate level, so under regeneration the two routes
    differ by construction and the number measures how much level activity
    adds to the typing. Report-only, as declared in amendment 5.
    """
    staged = tuple(int(ratio) for ratio in staged_ratios)
    direct = tuple(int(ratio) for ratio in direct_ratios)
    if not staged or not direct:
        raise ValueError("both routes must declare at least one ratio")
    if int(np.prod(staged)) != int(np.prod(direct)):
        raise ValueError("the two routes must contract by the same total ratio")
    left = _coupling_vector(_regenerated_final_couplings(instance, staged, tau))
    right = _coupling_vector(_regenerated_final_couplings(instance, direct, tau))
    return CompositionDefect(
        staged_ratios=staged,
        direct_ratios=direct,
        defect=float(np.abs(left - right).max()),
    )


def _regenerated_final_couplings(
    instance: PairwiseInstance,
    ratios: Sequence[int],
    tau: float,
) -> PairwiseCouplings:
    """Run one regenerated flow to a single site and return its couplings."""
    current = instance
    for ratio in ratios:
        length = len(current.graph.vertices)
        step = iterated_step(current, consecutive_blocks(length, int(ratio)))
        if step.instance is None:
            return step.mobius
        current = regenerated_instance(step, tau).instance
    raise ValueError("the declared ratios did not reach a single site")


def regenerated_fixed_point(
    instance: PairwiseInstance,
    ratio: int,
    tau: float = REGENERATION_TEMPERATURE,
    tolerance: float = 1.0e-9,
    max_iterations: int = 200,
    *,
    work_root: Path | None = None,
    worker_backend: Backend | None = None,
    worker_min_sites: int = 8,
) -> ReducedFixedPoint:
    """Iterate the regenerated composite: block, regenerate, re-tile, repeat.

    Identical to the passive fixed-point iteration except that each level's
    attention is regenerated before the re-tiling, so the pair sector has a
    source and the factorized subspace is no longer invariant. Convergence is
    reported, not assumed. Instances at or above the worker threshold route
    each blocking through the worker protocol when a backend is declared.
    """
    length = len(instance.graph.vertices)
    reduced = reduced_couplings(instance.couplings)
    size = len(instance.couplings.sites[0])
    change = float("inf")
    iterations = 0
    current = instance
    while iterations < int(max_iterations):
        blocks = consecutive_blocks(length, int(ratio))
        if worker_backend is not None and length >= worker_min_sites:
            if work_root is None:
                raise ValueError("worker routing needs a declared work root")
            step = iterated_step_via_worker(
                current,
                blocks,
                work_root=work_root / f"regen-fp-{iterations}",
                backend=worker_backend,
            )
        else:
            step = iterated_step(current, blocks)
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
    "CapacityRetention",
    "InformationRetention",
    "PairRetention",
    "REGENERATION_TEMPERATURE",
    "capacity_information_retention",
    "capacity_pair_retention",
    "RegeneratedInstance",
    "cocycle_flow",
    "reduced_fixed_point",
    "regenerated_composition_defect",
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
