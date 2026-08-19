r"""Phase two of the rescaling map: coupling read-back, the closed step, C3 and C4.

The coarse channel and the coarse connection exist (:mod:`closure_residual`,
:mod:`rescaling`). This module reads the exact coarse action back into the
declared pairwise family so that the composite maps a declared parameter vector
to a declared parameter vector of the same type and therefore iterates.

**The parameter vector.** A pairwise theory on the identified coarse graph: one
anchored site table per parent and one anchored pair table per coarse edge, in
the anchored Moebius gauge in which every component vanishes when any of its
coordinates sits at the declared ground state. The additive constant is carried
but is not part of the coupling vector, because it cancels in every
probability. The state space is the same nine-element space at every level, so
the read-back closes the step.

**Three routes, reported every step.** The primary route is the variational
projection: the family law minimizing
$\mathrm{KL}(\pi_{\mathrm{coarse}} \| \pi_{\mathrm{family}}(\theta))$. For a
discrete exponential family whose sufficient statistics are the admitted
subset indicators this M-projection is exactly the law in the family matching
the coarse marginals on every admitted pair, and iterative proportional
fitting from a seed inside the family converges to it (Csiszar 1975); the
implementation is therefore deterministic rather than a descent with a local
minimum to fear. The seed and control is the Moebius truncation: the pairwise
components of the exact anchored decomposition, the classical decimation and
truncation answer, computed on rationals. The difference between seed and
converged projection is reported every step, and outside the declared band the
step reports unresolved rather than averaged. The diagnostic route compares
the three declared observables, the holonomy of each coarse cycle, the
flow-averaged divergence across each coarse edge, and the per-parent
occupancies of the law, under the exact coarse flow and under both fitted
laws; the holonomy lives in the retained connection, which both routes share,
so it is matched by construction and reported as such.

**Declared checks, thresholds fixed in the 2026-08-17 design before
measurement.** C4, projection agreement: the variational and Moebius coupling
vectors agree to a relative $0.05$ per step over the pairwise block, because
the measured one-step truncation residual is $0.0063$ and a disagreement an
order of magnitude above the truncated quantity indicates the optimizer rather
than the physics. On a two-parent step the pairwise family is the whole
function space, the truncation is lossless, and C4 cannot fail; that
structural fact is reported rather than counted as corroboration. C3,
compatibility: blocking by the full ratio must equal blocking in stages after
the declared identifications, coupling vectors agreeing to $10^{-10}$. On the
declared C(2, 3) tower the stages are the inner blocking followed by the outer
one; the reverse order, pairs first, is **not performed**, because no pair
partition of C(2, 3) is a blocking of the declared tower structure — its
sub-cycles are the inner triangles — and the design records that reporting an
illegitimate ordering as a comparison would test nothing. Failure of C3 is a
result about the theory: the flow is a typed cocycle rather than an autonomous
semigroup, and fixed-point language downstream is unlicensed.

**Iteration.** The step's coarse instance carries the identified graph with
the phase-one Wilson-line connection and the primary-route couplings. Blocking
it again uses the same declared structure at the new level: the same state
space, the same representations and families, the same kappas, and the same
declared parent law, which is what the design's self-similarity declares.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import math
from typing import Mapping, Sequence

import numpy as np

from .categorical_falsification_model import (
    BELIEF_SEED,
    FalsificationModel,
    GROUP_ORDER,
    MODEL_SEED,
)
from .closure_residual import (
    _blocked_action,
    _coarse_child_weights,
    _divergence_table,
)
from .rescaling import CoarseConnection, coarse_connection
from .scale_cocycle import State, anchored_mobius_decompose
from .two_channel_gauge import CyclicRepresentation, TwoChannelGraph, orbit

CHANNELS = ("belief", "model")
COMPATIBILITY_TOLERANCE = 1.0e-10
DECLARED_CONCENTRATION = Fraction(1)
DECLARED_ANCHOR_STATE = 0
PROJECTION_AGREEMENT_TOLERANCE = 0.05
IPF_MARGINAL_TOLERANCE = 1.0e-13
IPF_MAX_SWEEPS = 500
ROUTE_C_STATUS = (
    "not performed: no pair partition of C(2, 3) is a blocking of the declared "
    "tower structure, whose sub-cycles are the inner triangles, so the reverse "
    "ordering would block a genuinely different subgraph"
)


@dataclass(frozen=True)
class PairwiseCouplings:
    """An anchored pairwise parameter vector on a declared set of sites.

    Site tables carry one value per state, zero at the declared ground state;
    pair tables carry one value per state pair, zero whenever either coordinate
    is at the ground state. The constant is the order-zero component and is not
    a coupling: it cancels in every probability and is excluded from every
    declared comparison.
    """

    width: int
    constant: Fraction
    sites: tuple[tuple[Fraction, ...], ...]
    pairs: tuple[tuple[tuple[int, int], tuple[tuple[Fraction, ...], ...]], ...]


def _state_count(couplings: PairwiseCouplings) -> int:
    """Return the per-site state count of one declared coupling vector."""
    return len(couplings.sites[0])


def couplings_action(couplings: PairwiseCouplings) -> np.ndarray:
    """Return the action array of one declared coupling vector."""
    size = _state_count(couplings)
    action = np.full((size,) * couplings.width, float(couplings.constant))
    for position, table in enumerate(couplings.sites):
        shape = [1] * couplings.width
        shape[position] = size
        action = action + np.array([float(v) for v in table]).reshape(shape)
    for (left, right), table in couplings.pairs:
        shape = [1] * couplings.width
        shape[left] = size
        shape[right] = size
        block = np.array([[float(v) for v in row] for row in table])
        action = action + block.reshape(shape)
    return action


def mobius_couplings(
    action: Mapping[State, Fraction],
    admitted_pairs: Sequence[tuple[int, int]],
    anchor: Sequence[int] | None = None,
) -> tuple[PairwiseCouplings, Fraction]:
    """Return the exact Moebius truncation and the sup norm of what it omits.

    This is the classical decimation-and-truncation read-back, computed on
    rationals so that alternating sums cannot cancel approximately. The second
    return value is the largest component magnitude outside the declared
    family, which is the one-step truncation residual in the anchored gauge.

    The anchor is the ground state at which every anchored component vanishes,
    and it is a gauge fixing: the anchored decomposition of one action is a
    different parameter vector at a different anchor, so every sup-norm
    statistic read off it moves with the anchor. It defaults to the declared
    all-``DECLARED_ANCHOR_STATE`` ground state, which is what was pinned
    silently before 2026-08-18; a caller reporting a sup-norm statistic should
    sweep it and report the range beside the pinned value
    (:func:`anchor_swept_pair_sup`). The law the couplings define, and every
    functional of that law such as the mutual-information retention, is exactly
    anchor-invariant, so the sweep is needed only for the sup-norm quantities.
    """
    width = len(next(iter(action)))
    admitted = tuple(sorted({tuple(sorted(pair)) for pair in admitted_pairs}))
    for pair in admitted:
        if len(set(pair)) != 2 or not all(0 <= i < width for i in pair):
            raise ValueError("admitted pairs must name two distinct declared sites")
    if anchor is None:
        ground = (DECLARED_ANCHOR_STATE,) * width
    else:
        ground = tuple(int(value) for value in anchor)
        if len(ground) != width:
            raise ValueError("the anchor must name one ground state per declared site")
    decomposition = anchored_mobius_decompose(action, anchor=ground)
    size = len({state[0] for state in action})
    sites = tuple(
        tuple(
            decomposition.components[(position,)][(value,)] for value in range(size)
        )
        for position in range(width)
    )
    pairs = tuple(
        (
            pair,
            tuple(
                tuple(
                    decomposition.components[pair][(left, right)]
                    for right in range(size)
                )
                for left in range(size)
            ),
        )
        for pair in admitted
    )
    omitted = Fraction(0)
    kept = {(), *((position,) for position in range(width)), *admitted}
    for subset, table in decomposition.components.items():
        if subset in kept:
            continue
        for value in table.values():
            omitted = max(omitted, abs(value))
    return (
        PairwiseCouplings(
            width=width,
            constant=decomposition.components[()][()],
            sites=sites,
            pairs=pairs,
        ),
        omitted,
    )


@dataclass(frozen=True)
class IpfReport:
    """Convergence record of the iterative proportional fitting projection."""

    sweeps: int
    marginal_gap: float
    kl_seed: float
    kl_projected: float
    family_leakage: float
    converged: bool


def _law_from_action(action: np.ndarray) -> np.ndarray:
    """Return the normalized Boltzmann law of one action array."""
    weights = np.exp(-(action - action.min()))
    return weights / weights.sum()


def _kl_arrays(left: np.ndarray, right: np.ndarray) -> float:
    """Return the relative entropy of two strictly positive laws."""
    return float(np.sum(left * (np.log(left) - np.log(right))))


def variational_couplings(
    action: Mapping[State, Fraction],
    admitted_pairs: Sequence[tuple[int, int]],
    seed: PairwiseCouplings,
    tolerance: float = IPF_MARGINAL_TOLERANCE,
    max_sweeps: int = IPF_MAX_SWEEPS,
) -> tuple[PairwiseCouplings, IpfReport]:
    """Return the variational projection of one coarse action onto the family.

    The projection minimizes KL(coarse law || family law). Because the family
    is the discrete exponential family spanned by the admitted subset
    indicators, the minimizer is the member matching the coarse marginals on
    every admitted pair, and iterative proportional fitting from the declared
    seed converges to it deterministically. The report carries the seed and
    projected divergences, the residual marginal gap, and the family leakage,
    the largest component of the projected action outside the admitted family,
    which is floating-point noise when the fit stayed inside the family.
    """
    width = len(next(iter(action)))
    size = len({state[0] for state in action})
    admitted = tuple(sorted(tuple(sorted(pair)) for pair in set(admitted_pairs)))
    target = np.empty((size,) * width)
    for state, value in action.items():
        target[state] = float(value)
    coarse_law = _law_from_action(target)
    fitted = _law_from_action(couplings_action(seed))
    kl_seed = _kl_arrays(coarse_law, fitted)
    gap = math.inf
    sweeps = 0
    while sweeps < max_sweeps:
        gap = 0.0
        for pair in admitted:
            others = tuple(axis for axis in range(width) if axis not in pair)
            coarse_marginal = coarse_law.sum(axis=others)
            fitted_marginal = fitted.sum(axis=others)
            gap = max(gap, float(np.abs(fitted_marginal - coarse_marginal).max()))
            shape = [1] * width
            shape[pair[0]] = size
            shape[pair[1]] = size
            fitted = fitted * (coarse_marginal / fitted_marginal).reshape(shape)
        sweeps += 1
        if gap <= tolerance:
            break
    projected_action = -np.log(fitted)
    projected = {
        state: Fraction(float(projected_action[state]))
        for state in product(range(size), repeat=width)
    }
    couplings, leakage = mobius_couplings(projected, admitted)
    return (
        couplings,
        IpfReport(
            sweeps=sweeps,
            marginal_gap=gap,
            kl_seed=kl_seed,
            kl_projected=_kl_arrays(coarse_law, fitted),
            family_leakage=float(leakage),
            converged=gap <= tolerance,
        ),
    )


def projection_agreement(
    variational: PairwiseCouplings,
    mobius: PairwiseCouplings,
) -> float:
    """Return the declared C4 statistic over the pairwise block.

    The statistic is the sup-norm difference of the pairwise blocks divided by
    the sup norm of the Moebius pairwise block. An empty pairwise block, as on
    a single-parent step, has no truncation to disagree about and returns zero;
    C4 is vacuous there and the step must not count it as corroboration.
    """
    if dict(variational.pairs).keys() != dict(mobius.pairs).keys():
        raise ValueError("the two routes must declare the same pairwise block")
    numerator = 0.0
    denominator = 0.0
    reference = dict(mobius.pairs)
    for pair, table in variational.pairs:
        for row, other in zip(table, reference[pair]):
            for left, right in zip(row, other):
                numerator = max(numerator, abs(float(left) - float(right)))
                denominator = max(denominator, abs(float(right)))
    if denominator == 0.0:
        return 0.0 if numerator == 0.0 else math.inf
    return numerator / denominator


@dataclass(frozen=True)
class PairwiseInstance:
    """A declared coarse instance: the identified graph and its couplings."""

    graph: TwoChannelGraph
    couplings: PairwiseCouplings


@dataclass(frozen=True)
class RescalingStep:
    """One closed renormalization step with all three routes reported."""

    blocks: tuple[tuple[int, ...], ...]
    connection: CoarseConnection | None
    action: Mapping[State, Fraction]
    flow_weights: Mapping[State, Fraction]
    mobius: PairwiseCouplings
    mobius_omitted_sup: Fraction
    variational: PairwiseCouplings
    ipf: IpfReport
    projection_ratio: float
    resolved: bool
    instance: PairwiseInstance | None


def _kernel_model(
    graph: TwoChannelGraph,
    name: str,
    concentration: Fraction = DECLARED_CONCENTRATION,
) -> FalsificationModel:
    """Return the declared level-invariant structure attached to one graph.

    The state space, the representations and families, the kappas, and the
    declared parent law are carried unchanged to every level of the tower;
    only the graph and its connection change. Occupancies and attention rows
    are irrelevant to the downward kernels and are declared uniform.

    What this model does **not** carry is the instance's couplings. The block
    energy of :mod:`partition_dynamics` is assembled from the downward kernels,
    which are level-invariant declared structure, so no coupling vector of any
    magnitude moves it. A coupling scale reaches a partition posterior only
    through the level's Boltzmann flow, which reweights which configurations
    the energy is averaged over; the landscape itself is coupling-independent
    by construction, and a sweep in the coupling scale is a flow reweighting
    rather than a sweep of the formation landscape (2026-08-18 lab-versus-theory
    audit, finding 2).

    ``concentration`` is the Ewens concentration of the partition prior. It was
    pinned at one from 2026-08-17 to 2026-08-18 with no override reachable from
    the published route; it is a declared knob, and callers that report a
    partition posterior should report the value they used.
    """
    belief_representation = CyclicRepresentation(GROUP_ORDER, 1, "belief")
    model_representation = CyclicRepresentation(GROUP_ORDER, 2, "model")
    size = len(graph.vertices)
    return FalsificationModel(
        name=name,
        belief_representation=belief_representation,
        model_representation=model_representation,
        belief_family=orbit(belief_representation, BELIEF_SEED),
        model_family=orbit(model_representation, MODEL_SEED),
        graph=graph,
        alpha_belief=tuple(Fraction(1, size) for _ in range(size)),
        alpha_model=tuple(Fraction(1, size) for _ in range(size)),
        parent_labels=tuple(f"A{index + 1}" for index in range(size)),
        candidate_partitions=(tuple((vertex,) for vertex in graph.vertices),),
        kappa_belief=2.0,
        kappa_model=2.0,
        crp_concentration=Fraction(concentration),
        identity_holonomy_weight=Fraction(1, 4),
        row_configurations=("uniform", "peaked"),
    )


def _checked_step_blocks(
    model: FalsificationModel,
    blocks: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    """Return the validated blocking of one step, which may be a single block."""
    declared = tuple(tuple(block) for block in blocks)
    arranged = sorted(agent for block in declared for agent in block)
    if arranged != sorted(model.agents):
        raise ValueError("the blocking must arrange every declared agent exactly once")
    return declared


def _readback(
    model: FalsificationModel,
    weight_tensor: np.ndarray,
    declared: tuple[tuple[int, ...], ...],
    parent_priors: Mapping[int, Sequence[float]] | None = None,
    anchor: Sequence[int] | None = None,
) -> RescalingStep:
    """Block one child-weight tensor and read the coarse couplings back."""
    action, flow = _blocked_action(model, weight_tensor, declared, parent_priors)
    return _readback_from_action(model, action, flow, declared, anchor)


def _readback_from_action(
    model: FalsificationModel,
    action: Mapping[State, Fraction],
    flow: Mapping[State, Fraction],
    declared: tuple[tuple[int, ...], ...],
    anchor: Sequence[int] | None = None,
) -> RescalingStep:
    """Read one already-computed coarse action back into the declared family."""
    connection = (
        coarse_connection(model, declared) if len(declared) >= 2 else None
    )
    if connection is None:
        admitted: tuple[tuple[int, int], ...] = ()
    else:
        admitted = tuple(
            sorted(
                {
                    tuple(sorted((edge.receiver - 1, edge.source - 1)))
                    for edge in connection.graph.edges
                }
            )
        )
    mobius, omitted = mobius_couplings(action, admitted, anchor)
    variational, ipf = variational_couplings(action, admitted, mobius)
    ratio = projection_agreement(variational, mobius)
    resolved = ipf.converged and ratio <= PROJECTION_AGREEMENT_TOLERANCE
    instance = (
        PairwiseInstance(graph=connection.graph, couplings=variational)
        if connection is not None
        else None
    )
    return RescalingStep(
        blocks=declared,
        connection=connection,
        action=action,
        flow_weights=flow,
        mobius=mobius,
        mobius_omitted_sup=omitted,
        variational=variational,
        ipf=ipf,
        projection_ratio=ratio,
        resolved=resolved,
        instance=instance,
    )


def initial_step(
    model: FalsificationModel,
    observation: Sequence[int],
    blocks: Sequence[Sequence[int]],
    parent_priors: Mapping[int, Sequence[float]] | None = None,
    anchor: Sequence[int] | None = None,
) -> RescalingStep:
    """Run one closed renormalization step on the declared fine model.

    The fine object being blocked is the auxiliary pairwise child theory of
    the declared model at the declared observation, exactly as in the coarse
    closure measurement. The step's instance carries the primary-route
    couplings on the identified graph, ready to be blocked again.

    ``parent_priors`` declares one parent law per block root. The default is
    the declared law at every block, which is *not* gauge-covariant: regauging
    a root re-expresses the law attached to it, so a caller comparing a
    regauged run against a bare one must thread the re-expressed priors here.
    ``anchor`` is the Moebius ground state of the read-back gauge.
    """
    if type(model) is not FalsificationModel:
        raise TypeError("model must be a FalsificationModel")
    record = tuple(observation)
    if len(record) != len(model.agents):
        raise ValueError("the observation must carry one record per declared agent")
    if any(type(value) is not int or value not in (0, 1) for value in record):
        raise ValueError("every observation record must be binary")
    declared = _checked_step_blocks(model, blocks)
    return _readback(
        model, _coarse_child_weights(model, record), declared, parent_priors, anchor
    )


def iterated_step(
    instance: PairwiseInstance,
    blocks: Sequence[Sequence[int]],
    parent_priors: Mapping[int, Sequence[float]] | None = None,
    anchor: Sequence[int] | None = None,
) -> RescalingStep:
    """Run one closed renormalization step on a coarse instance.

    The child weights are the Boltzmann weights of the instance's coupling
    action; the downward kernels are built from the instance's graph and the
    level-invariant declared structure. There is no observation term at coarse
    levels: the record was consumed at the fine level and the coupling action
    is the whole theory.
    """
    if type(instance) is not PairwiseInstance:
        raise TypeError("instance must be a PairwiseInstance")
    model = _kernel_model(instance.graph, "coarse-instance")
    declared = _checked_step_blocks(model, blocks)
    action = couplings_action(instance.couplings)
    weights = np.exp(-(action - action.min()))
    return _readback(model, weights, declared, parent_priors, anchor)


@dataclass(frozen=True)
class AnchorSweep:
    """The pinned value of a sup-norm read-back statistic beside its anchor range.

    The anchored Moebius decomposition is a gauge fixing, so a sup norm read off
    it is an anchor-dependent number. This record carries the value at the
    declared anchor, the extremes over the swept anchors, and the anchors that
    attain them, so a published sup norm can be quoted with the range it moves
    over instead of as if it were anchor-free.
    """

    pinned_anchor: tuple[int, ...]
    pinned_value: float
    minimum_value: float
    minimum_anchor: tuple[int, ...]
    maximum_value: float
    maximum_anchor: tuple[int, ...]
    swept_count: int

    @property
    def relative_range(self) -> float:
        """Return the swept range as a fraction of the pinned value."""
        if self.pinned_value == 0.0:
            return 0.0
        return (self.maximum_value - self.minimum_value) / abs(self.pinned_value)


def _pair_sup(couplings: PairwiseCouplings) -> float:
    """Return the sup norm of one coupling vector's pairwise block."""
    return max(
        (
            abs(float(value))
            for _, table in couplings.pairs
            for row in table
            for value in row
        ),
        default=0.0,
    )


def _site_sup(couplings: PairwiseCouplings) -> float:
    """Return the sup norm of one coupling vector's site block."""
    return max(
        (abs(float(value)) for table in couplings.sites for value in table),
        default=0.0,
    )


def anchor_swept_sup(
    action: Mapping[State, Fraction],
    admitted_pairs: Sequence[tuple[int, int]],
    anchors: Sequence[Sequence[int]],
    block: str = "pair",
) -> AnchorSweep:
    """Return the declared-anchor sup norm of one coarse action beside its range.

    ``block`` selects the pairwise or the site block of the read-back parameter
    vector. The declared anchor is always evaluated, whether or not the swept
    set contains it, so the pinned value in the record is the published one.
    """
    if block not in ("pair", "site"):
        raise ValueError("block must be 'pair' or 'site'")
    measure = _pair_sup if block == "pair" else _site_sup
    width = len(next(iter(action)))
    pinned_anchor = (DECLARED_ANCHOR_STATE,) * width
    pinned_value = measure(mobius_couplings(action, admitted_pairs, pinned_anchor)[0])
    swept: list[tuple[float, tuple[int, ...]]] = [(pinned_value, pinned_anchor)]
    for candidate in anchors:
        ground = tuple(int(value) for value in candidate)
        if ground == pinned_anchor:
            continue
        swept.append(
            (measure(mobius_couplings(action, admitted_pairs, ground)[0]), ground)
        )
    lowest = min(swept)
    highest = max(swept)
    return AnchorSweep(
        pinned_anchor=pinned_anchor,
        pinned_value=pinned_value,
        minimum_value=lowest[0],
        minimum_anchor=lowest[1],
        maximum_value=highest[0],
        maximum_anchor=highest[1],
        swept_count=len(swept),
    )


@dataclass(frozen=True)
class CompatibilityReport:
    """Check C3: blocking by the full ratio against blocking in declared stages."""

    direct_sites: tuple[Fraction, ...]
    staged_sites: tuple[Fraction, ...]
    deviation: float
    compatible: bool
    intermediate: RescalingStep
    route_c_status: str


def check_compatibility(
    model: FalsificationModel,
    observation: Sequence[int],
    blocks: Sequence[Sequence[int]],
) -> CompatibilityReport:
    """Run check C3 on one declared two-stage tower blocking.

    The direct route blocks every declared agent into one parent. The staged
    route blocks the declared inner blocks first, closes the step through the
    read-back, and blocks the resulting coarse instance into one parent. Both
    end at a single-site coupling vector, the anchored site table, and the
    declared criterion is agreement to ``COMPATIBILITY_TOLERANCE`` in sup
    norm. The reverse ordering is not performed, for the pre-registered
    reason carried in ``route_c_status``. Failure is a result, not a bug: the
    flow is then a typed cocycle and fixed-point language is unlicensed.
    """
    declared = _checked_step_blocks(model, blocks)
    everything = (tuple(sorted(model.agents)),)
    direct = initial_step(model, observation, everything)
    intermediate = initial_step(model, observation, declared)
    if intermediate.instance is None:
        raise ValueError("the staged route needs at least two declared blocks")
    staged = iterated_step(
        intermediate.instance,
        (tuple(intermediate.instance.graph.vertices),),
    )
    direct_sites = direct.mobius.sites[0]
    staged_sites = staged.mobius.sites[0]
    deviation = max(
        abs(float(left) - float(right))
        for left, right in zip(direct_sites, staged_sites)
    )
    return CompatibilityReport(
        direct_sites=direct_sites,
        staged_sites=staged_sites,
        deviation=deviation,
        compatible=deviation <= COMPATIBILITY_TOLERANCE,
        intermediate=intermediate,
        route_c_status=ROUTE_C_STATUS,
    )


@dataclass(frozen=True)
class MomentDiagnostic:
    """The three declared observables under the exact flow and both fitted laws.

    The holonomy of each coarse cycle lives in the retained connection, which
    both routes share by construction, so it is matched identically and is
    reported as the connection's per-channel coarse elements. The divergence
    rows carry, per coarse edge and channel, the flow-averaged divergence under
    the exact coarse law and its deviation under each fitted law; the occupancy
    rows carry the per-parent marginal sup-norm deviations.
    """

    holonomy_matched: bool
    coarse_elements: tuple[tuple[str, tuple[int, ...]], ...]
    divergence_rows: tuple[tuple[int, str, float, float, float], ...]
    occupancy_rows: tuple[tuple[int, float, float], ...]


def moment_matching_diagnostic(step: RescalingStep) -> MomentDiagnostic:
    """Compare the three declared observables across the exact and fitted laws.

    The design computes this route only when the first two routes disagree
    beyond C4, to adjudicate which has moved; the function itself is callable
    on any step with a connection.
    """
    if step.connection is None:
        raise ValueError("the diagnostic needs a step with a coarse connection")
    graph = step.connection.graph
    model = _kernel_model(graph, "moment-diagnostic")
    width = len(step.blocks)
    size = model.state_count
    exact = np.empty((size,) * width)
    for state, weight in step.flow_weights.items():
        exact[state] = float(weight)
    laws = {
        "variational": _law_from_action(couplings_action(step.variational)),
        "mobius": _law_from_action(couplings_action(step.mobius)),
    }
    divergence_rows: list[tuple[int, str, float, float, float]] = []
    for position, edge in enumerate(graph.edges):
        axes = (edge.receiver - 1, edge.source - 1)
        others = tuple(axis for axis in range(width) if axis not in axes)
        marginals = {
            name: law.sum(axis=others)
            for name, law in {"exact": exact, **laws}.items()
        }
        if axes[0] > axes[1]:
            marginals = {name: table.T for name, table in marginals.items()}
        for channel in CHANNELS:
            element = graph.channel_elements(channel)[position]
            table = _divergence_table(model, channel, element)
            averages = {
                name: float(np.sum(marginal * table))
                for name, marginal in marginals.items()
            }
            divergence_rows.append(
                (
                    position,
                    channel,
                    averages["exact"],
                    abs(averages["variational"] - averages["exact"]),
                    abs(averages["mobius"] - averages["exact"]),
                )
            )
    occupancy_rows: list[tuple[int, float, float]] = []
    for position in range(width):
        others = tuple(axis for axis in range(width) if axis != position)
        exact_marginal = exact.sum(axis=others)
        occupancy_rows.append(
            (
                position,
                float(np.abs(laws["variational"].sum(axis=others) - exact_marginal).max()),
                float(np.abs(laws["mobius"].sum(axis=others) - exact_marginal).max()),
            )
        )
    return MomentDiagnostic(
        holonomy_matched=True,
        coarse_elements=tuple(
            (channel, graph.channel_elements(channel)) for channel in CHANNELS
        ),
        divergence_rows=tuple(divergence_rows),
        occupancy_rows=tuple(occupancy_rows),
    )


__all__ = [
    "AnchorSweep",
    "CHANNELS",
    "COMPATIBILITY_TOLERANCE",
    "CompatibilityReport",
    "DECLARED_ANCHOR_STATE",
    "DECLARED_CONCENTRATION",
    "IPF_MARGINAL_TOLERANCE",
    "IPF_MAX_SWEEPS",
    "IpfReport",
    "MomentDiagnostic",
    "PairwiseCouplings",
    "PairwiseInstance",
    "PROJECTION_AGREEMENT_TOLERANCE",
    "RescalingStep",
    "ROUTE_C_STATUS",
    "anchor_swept_sup",
    "check_compatibility",
    "couplings_action",
    "initial_step",
    "iterated_step",
    "mobius_couplings",
    "moment_matching_diagnostic",
    "projection_agreement",
    "variational_couplings",
]
