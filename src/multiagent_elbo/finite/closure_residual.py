"""Generated many-body terms and the closure residual of a declared parent family.

Exactly eliminating an internal variable from a finite model generates the whole
hyperedge family on the variables that survive, and that hierarchy is recovered by
Moebius inversion of the surviving action against a declared ground configuration.
This module measures two consequences on the declared categorical system. The
primary measurement runs in the coarse-graining direction: children are
eliminated, the surviving parent theory is read off, and its generated
three-body coupling is reported as a ratio against its own pairwise coupling,
because real-space blocking always generates couplings outside the starting
family and a nonzero coefficient is therefore never by itself a defect. The
second is the residual left by projecting that action onto a declared parent
family, reported as a ratio against the retained flow rather than as a bare sup
norm. The elimination that runs against the coarse-graining direction, deleting
a block parent and keeping its children, is retained separately as the generic
common-cause mechanism and is not a renormalization step.

The projection admits a declared set of subsets rather than an order cutoff. On
the declared blocks of the reference design the graph's edge pairs exhaust the
pairs, so there the declared family and the order-two cutoff coincide; the
distinction is real for any block whose induced edge set is a proper subset of the
pairs, and it is exercised directly in the tests.

The flow weighting is the normalized Boltzmann measure of the same action being
decomposed, formed under the declared parent law. The reported ratio divides the
flow-averaged deviation of the omitted part from its own flow average by the
same quantity for the retained part. A constant carries no physical content in
either part because it cancels in every probability, so both are centered and
the ratio is a statement about varying content rather than about an arbitrary
offset. The ratio is invariant under rescaling the weights.

On arithmetic. The Moebius inversion is exact: every action value is carried into a
Fraction before any subset sum is formed, and the alternating sums are performed on
rationals, so nothing cancels approximately. The action values themselves come from
logarithms and from the declared floating-point divergences of the model, so they
are the exactly representable binary rationals nearest the intended transcendental
numbers, and no further rounding occurs downstream. The Ising star of the reference
calculation is on the same footing.

That reference calculation is the three-leaf Ising star. A center spin carrying a
field is eliminated exactly, and the resulting leaf action has a generated
three-body coefficient whose leading behavior in the couplings is known in closed
form. Exact equality at finite coupling is not expected, because the closed form is
the leading term only; what is checked is that the ratio of the exact coefficient
to the closed form approaches one as the couplings are scaled to zero. The star
coefficient is reported in the multilinear spin basis, so the anchored component at
the fully flipped configuration is divided by two cubed, one factor of two for each
coordinate that differs from the anchor.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import math
from types import MappingProxyType
from typing import Iterable, Mapping, Sequence

import numpy as np

from .categorical_falsification_model import FalsificationModel, kl_laws, transported
from .tower_vfe import PARENT_STATE_WEIGHTS
from .scale_cocycle import (
    AnchoredMobiusDecomposition,
    State,
    Subset,
    anchored_mobius_decompose,
)

DECLARED_GROUND_STATE_INDEX = 0
ISING_STAR_ANCHOR: State = (-1, -1, -1)
ISING_STAR_LEAVES = 3
_CONTRACTION_LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _real(value: object, field: str) -> float:
    """Coerce a declared real parameter, rejecting bool and nonfinite values."""
    if type(value) not in (int, float):
        raise TypeError(f"{field} must be an int or a float")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{field} must be finite")
    return result


def _exact(value: object, field: str) -> Fraction:
    """Coerce a declared weight to an exact rational, rejecting bool."""
    if type(value) is bool:
        raise TypeError(f"{field} must be rational, not bool")
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        raise TypeError(f"{field} must be rational") from error


@dataclass(frozen=True)
class DeclaredFamilyProjection:
    """Projection of an anchored decomposition onto a declared family of subsets."""

    admitted_subsets: tuple[Subset, ...]
    omitted_subsets: tuple[Subset, ...]
    retained_value: Mapping[State, Fraction]
    omitted_value: Mapping[State, Fraction]
    residual_sup_norm: Fraction


@dataclass(frozen=True)
class BlockClosureResidual:
    """Closure diagnostics of one declared block of the finite categorical model."""

    block: tuple[int, ...]
    largest_three_body_subset: frozenset[int]
    largest_three_body_coefficient: float
    admitted_pairs: tuple[tuple[int, int], ...]
    projection: DeclaredFamilyProjection
    residual_sup_norm: float
    flow_weighted_residual: float


@dataclass(frozen=True)
class ClosureResidualReport:
    """Closure diagnostics of every declared block that can carry a triple term."""

    observation: tuple[int, ...]
    partition: tuple[tuple[int, ...], ...]
    blocks: tuple[BlockClosureResidual, ...]
    largest_three_body_block: tuple[int, ...]
    largest_three_body_subset: frozenset[int]
    largest_three_body_coefficient: float
    flow_weighted_residual: float
    pairwise_closure_holds: bool


def largest_k_body_coefficient(
    decomposition: AnchoredMobiusDecomposition,
    order: int,
) -> tuple[frozenset[int], Fraction]:
    """Return the subset and signed component of greatest magnitude at one order."""
    if type(decomposition) is not AnchoredMobiusDecomposition:
        raise TypeError("decomposition must be an AnchoredMobiusDecomposition")
    if type(order) is not int or not 0 <= order <= len(decomposition.anchor):
        raise ValueError("order is outside the interaction hierarchy")
    best_subset: Subset = ()
    best_value = Fraction(0)
    best_magnitude = Fraction(-1)
    for subset in sorted(decomposition.components):
        if len(subset) != order:
            continue
        table = decomposition.components[subset]
        for subset_state in sorted(table):
            value = table[subset_state]
            if abs(value) > best_magnitude:
                best_subset = subset
                best_value = value
                best_magnitude = abs(value)
    return frozenset(best_subset), best_value


def declared_family_projection(
    decomposition: AnchoredMobiusDecomposition,
    admitted_subsets: Iterable[Iterable[int]],
) -> DeclaredFamilyProjection:
    """Project an anchored decomposition onto a declared set of subsets."""
    if type(decomposition) is not AnchoredMobiusDecomposition:
        raise TypeError("decomposition must be an AnchoredMobiusDecomposition")
    width = len(decomposition.anchor)
    admitted: list[Subset] = []
    for subset in admitted_subsets:
        declared = tuple(subset)
        if any(type(index) is not int for index in declared):
            raise TypeError("admitted coordinates must be integers")
        indices = tuple(sorted(set(declared)))
        if len(indices) != len(declared):
            raise ValueError("an admitted subset must not repeat a coordinate")
        if any(not 0 <= index < width for index in indices):
            raise ValueError("admitted coordinates must index the declared product")
        if indices in admitted:
            raise ValueError("each admitted subset must be declared once")
        admitted.append(indices)
    admitted_family = set(admitted)
    omitted_subsets = tuple(
        subset for subset in sorted(decomposition.components) if subset not in admitted_family
    )
    retained: dict[State, Fraction] = {}
    omitted: dict[State, Fraction] = {}
    for state, value in decomposition.action.items():
        kept = sum(
            (decomposition.component_value(subset, state) for subset in admitted),
            Fraction(0),
        )
        retained[state] = kept
        omitted[state] = value - kept
    residual = max((abs(value) for value in omitted.values()), default=Fraction(0))
    return DeclaredFamilyProjection(
        admitted_subsets=tuple(sorted(admitted)),
        omitted_subsets=omitted_subsets,
        retained_value=MappingProxyType(retained),
        omitted_value=MappingProxyType(omitted),
        residual_sup_norm=residual,
    )


def flow_weighted_residual(
    projection: DeclaredFamilyProjection,
    flow_weights: Mapping[State, object],
) -> float:
    """Return the flow-averaged omitted spread over the flow-averaged retained spread.

    Both parts are centered on their own flow average, because an additive
    constant cancels in every probability on either side of the ratio.
    """
    if type(projection) is not DeclaredFamilyProjection:
        raise TypeError("projection must be a DeclaredFamilyProjection")
    if set(flow_weights) != set(projection.omitted_value):
        raise ValueError("flow weights must cover the declared configurations exactly")
    weights = {
        state: _exact(value, "flow weight") for state, value in flow_weights.items()
    }
    if any(value < 0 for value in weights.values()):
        raise ValueError("flow weights must be nonnegative")
    mass = sum(weights.values(), Fraction(0))
    if mass == 0:
        raise ValueError("the declared flow must carry positive mass")
    omitted_average = sum(
        (weights[state] * value for state, value in projection.omitted_value.items()),
        Fraction(0),
    ) / mass
    numerator = sum(
        (
            weights[state] * abs(value - omitted_average)
            for state, value in projection.omitted_value.items()
        ),
        Fraction(0),
    )
    average = sum(
        (weights[state] * value for state, value in projection.retained_value.items()),
        Fraction(0),
    ) / mass
    denominator = sum(
        (
            weights[state] * abs(value - average)
            for state, value in projection.retained_value.items()
        ),
        Fraction(0),
    )
    if denominator == 0:
        raise ValueError("the retained flow must vary under the declared weights")
    return float(numerator / denominator)


def ising_star_action(field: float, couplings: Sequence[float]) -> Mapping[State, Fraction]:
    """Return the leaf action of the three-leaf star after eliminating the center spin."""
    strength = _real(field, "field")
    weights = tuple(
        _real(value, f"couplings[{index}]") for index, value in enumerate(couplings)
    )
    if len(weights) != ISING_STAR_LEAVES:
        raise ValueError("the declared star carries exactly three leaves")
    action: dict[State, Fraction] = {}
    for spins in product((-1, 1), repeat=ISING_STAR_LEAVES):
        argument = strength
        for weight, spin in zip(weights, spins):
            argument += weight * spin
        action[spins] = Fraction(-math.log(2.0 * math.cosh(argument)))
    return MappingProxyType(action)


def ising_star_three_body_coefficient(field: float, couplings: Sequence[float]) -> float:
    """Return the exact generated three-body coefficient of the eliminated star."""
    decomposition = anchored_mobius_decompose(
        ising_star_action(field, couplings), anchor=ISING_STAR_ANCHOR
    )
    subset = tuple(range(ISING_STAR_LEAVES))
    flipped = tuple(-value for value in ISING_STAR_ANCHOR)
    component = decomposition.component_value(subset, flipped)
    return float(component) / float(2**ISING_STAR_LEAVES)


def ising_star_leading_order(field: float, couplings: Sequence[float]) -> float:
    """Return the leading-order closed form of the star three-body coefficient."""
    strength = _real(field, "field")
    weights = tuple(
        _real(value, f"couplings[{index}]") for index, value in enumerate(couplings)
    )
    if len(weights) != ISING_STAR_LEAVES:
        raise ValueError("the declared star carries exactly three leaves")
    secant = 1.0 / math.cosh(strength)
    product_of_couplings = weights[0] * weights[1] * weights[2]
    return 2.0 * secant * secant * math.tanh(strength) * product_of_couplings


def ising_star_convergence_ratios(
    field: float,
    couplings: Sequence[float],
    scales: Sequence[float],
) -> tuple[tuple[float, float], ...]:
    """Return the exact to leading-order ratio of the star coefficient at each scale."""
    rows: list[tuple[float, float]] = []
    for index, value in enumerate(scales):
        scale = _real(value, f"scales[{index}]")
        if scale <= 0.0:
            raise ValueError("coupling scales must be positive")
        scaled = tuple(scale * _real(entry, "couplings") for entry in couplings)
        leading = ising_star_leading_order(field, scaled)
        if leading == 0.0:
            raise ValueError("the leading-order form vanishes, so no ratio exists")
        rows.append((scale, ising_star_three_body_coefficient(field, scaled) / leading))
    return tuple(rows)


def _divergence_table(model: FalsificationModel, channel: str, element: int) -> np.ndarray:
    """Return the receiver by source divergence table of one transported channel."""
    if channel == "belief":
        representation = model.belief_representation
        slot = 0
    elif channel == "model":
        representation = model.model_representation
        slot = 1
    else:
        raise ValueError("channel must be 'belief' or 'model'")
    size = model.state_count
    table = np.empty((size, size), dtype=np.float64)
    for receiver in range(size):
        left = model.state_pair(receiver)[slot]
        for source in range(size):
            right = model.state_pair(source)[slot]
            table[receiver, source] = kl_laws(left, transported(representation, element, right))
    return table


def _block_action(
    model: FalsificationModel,
    observation: Sequence[int],
    block: Sequence[int],
) -> tuple[Mapping[State, Fraction], Mapping[State, Fraction]]:
    """Return the exact eliminated block action and its Boltzmann flow weights."""
    size = model.state_count
    width = len(block)
    index_of = {agent: position for position, agent in enumerate(model.agents)}
    position_of = {agent: position for position, agent in enumerate(block)}
    likelihood = model.likelihood_table()
    observed = tuple(observation[index_of[agent]] for agent in block)
    kernels = tuple(
        np.stack([model.downward_kernel(block, agent, parent) for parent in range(size)])
        for agent in block
    )
    induced = model.graph.induced(block)
    configuration = model.row_configurations[0]
    event_law = {
        channel: model.edge_event_law(configuration, channel)
        for channel in ("belief", "model")
    }
    kappa = {"belief": model.kappa_belief, "model": model.kappa_model}
    edge_terms: list[tuple[int, int, float, np.ndarray]] = []
    for edge_index, edge in enumerate(induced.edges):
        for channel in ("belief", "model"):
            weight = kappa[channel] * float(
                event_law[channel][index_of[edge.receiver], index_of[edge.source]]
            )
            element = induced.channel_elements(channel)[edge_index]
            edge_terms.append(
                (
                    position_of[edge.receiver],
                    position_of[edge.source],
                    weight,
                    _divergence_table(model, channel, element),
                )
            )
    parent_prior = _declared_parent_prior(size)
    energies: dict[State, float] = {}
    action: dict[State, Fraction] = {}
    for state in product(range(size), repeat=width):
        energy = 0.0
        for position in range(width):
            energy -= math.log(likelihood[state[position], observed[position]])
        for receiver, source, weight, table in edge_terms:
            energy += weight * table[state[receiver], state[source]]
        marginal = 0.0
        for parent in range(size):
            term = parent_prior[parent]
            for position in range(width):
                term *= kernels[position][parent, state[position]]
            marginal += term
        energy -= math.log(marginal)
        energies[state] = energy
        action[state] = Fraction(energy)
    floor = min(energies.values())
    unnormalized = {state: math.exp(floor - value) for state, value in energies.items()}
    mass = sum(unnormalized.values())
    weights = {state: Fraction(value / mass) for state, value in unnormalized.items()}
    return MappingProxyType(action), MappingProxyType(weights)


@dataclass(frozen=True)
class CoarseClosureReport:
    """Closure diagnostics of the coarse theory obtained by blocking.

    This is the renormalization direction: the children are eliminated exactly and
    the interaction content of the surviving parents is read off. A coarse theory
    is pairwise exactly when every component above pair order vanishes.
    """

    partition: tuple[tuple[int, ...], ...]
    order_magnitudes: tuple[tuple[int, float], ...]
    largest_three_body_blocks: tuple[tuple[int, ...], ...]
    largest_three_body_coefficient: float
    largest_two_body_coefficient: float
    three_to_two_ratio: float
    flow_weighted_residual: float
    pairwise_closure_holds: bool


def _declared_parent_prior(size: int) -> tuple[float, ...]:
    """Return the declared per-parent law, matching the tower's parent measure."""
    if size != len(PARENT_STATE_WEIGHTS):
        raise ValueError("the declared parent law does not cover this state count")
    return tuple(float(weight) for weight in PARENT_STATE_WEIGHTS)


def _coarse_child_weights(
    model: FalsificationModel,
    observation: Sequence[int],
) -> np.ndarray:
    r"""Return $\exp(-E)$ of the auxiliary pairwise child theory at every child state.

    The energy is the per-agent record likelihood together with the declared edge
    divergences, $E(x) = -\sum_a \log L(x_a, o_a) + \sum_{(i \leftarrow j)}
    \kappa^c \eta^c_{ij} D^c_{ij}(x_i, x_j)$, where $D$ is indexed by the receiver
    state first. A divergence table is transposed before it is broadcast whenever
    the receiver occupies the later axis, because the reshape fills axes in
    ascending order and would otherwise place the receiver row axis on the source.
    """
    size = model.state_count
    agents = model.agents
    index_of = {agent: position for position, agent in enumerate(agents)}
    likelihood = model.likelihood_table()
    configuration = model.row_configurations[0]
    event_law = {
        channel: model.edge_event_law(configuration, channel)
        for channel in ("belief", "model")
    }
    kappa = {"belief": model.kappa_belief, "model": model.kappa_model}
    weight_tensor = np.ones((size,) * len(agents), dtype=np.float64)
    for position, agent in enumerate(agents):
        shape = [1] * len(agents)
        shape[position] = size
        column = likelihood[:, observation[index_of[agent]]]
        weight_tensor = weight_tensor * column.reshape(shape)
    for edge_index, edge in enumerate(model.graph.edges):
        if edge.receiver == edge.source:
            continue
        receiver = index_of[edge.receiver]
        source = index_of[edge.source]
        table = np.zeros((size, size), dtype=np.float64)
        for channel in ("belief", "model"):
            strength = kappa[channel] * float(event_law[channel][receiver, source])
            element = model.graph.channel_elements(channel)[edge_index]
            table = table + strength * _divergence_table(model, channel, element)
        factor = np.exp(-table)
        if receiver > source:
            factor = factor.T
        shape = [1] * len(agents)
        shape[receiver] = size
        shape[source] = size
        weight_tensor = weight_tensor * factor.reshape(shape)
    return weight_tensor


def _coarse_action(
    model: FalsificationModel,
    observation: Sequence[int],
    partition: Sequence[Sequence[int]],
    parent_priors: Mapping[int, Sequence[float]] | None = None,
) -> tuple[Mapping[State, Fraction], Mapping[State, Fraction]]:
    """Return the exact coarse action on parents and its Boltzmann flow weights.

    The fine object being blocked is the auxiliary pairwise child theory: the
    per-agent record likelihood together with the declared edge divergences
    $\\kappa\\,\\eta_{ij} D_{ij}(x_i, x_j)$ evaluated at child states. It is not
    the declared tower joint, whose scale-0 conditional factorizes over agents
    given the parent and therefore blocks to an exactly pairwise parent theory;
    the question asked here is whether blocking a genuinely pairwise child
    theory stays pairwise. The blocking kernel per block is the Bayes posterior
    $T(p \\mid x_B) = P(p) \\prod_{a \\in B} K(x_a \\mid p) / \\sum_{p'} P(p')
    \\prod_{a \\in B} K(x_a \\mid p')$ under the declared parent law, so
    $\\sum_p T(p \\mid x_B) = 1$ and the blocking preserves the partition
    function exactly, which is the standard real-space condition. Children in
    different blocks are coupled by the declared cross edges, which is what can
    induce interactions among parents beyond pair order, so the whole edge set
    enters rather than the induced one.

    The parent measure defaults to the declared parent law at every block. A
    caller may instead declare one law per block root, keyed by the root label,
    which is what gauge covariance requires: the parent law is data attached to
    the root frame, and regauging a root re-expresses its law rather than
    leaving it fixed while everything else moves.
    """
    return _blocked_action(
        model, _coarse_child_weights(model, observation), partition, parent_priors
    )


def _blocked_action(
    model: FalsificationModel,
    weight_tensor: np.ndarray,
    partition: Sequence[Sequence[int]],
    parent_priors: Mapping[int, Sequence[float]] | None = None,
) -> tuple[Mapping[State, Fraction], Mapping[State, Fraction]]:
    """Block one explicit child-weight tensor and return the coarse action.

    The tensor carries one axis per declared agent, in agent order, holding
    exp(-E) of whatever fine theory is being blocked; the blocking kernel per
    block is the Bayes posterior under the declared parent law, exactly as in
    the coarse closure measurement. Factoring the contraction away from the
    construction of the weights is what lets a coarse instance, whose theory
    is a coupling action rather than a likelihood with edge divergences, be
    blocked again by the same audited kernel.
    """
    size = model.state_count
    agents = model.agents
    index_of = {agent: position for position, agent in enumerate(agents)}
    letters = _CONTRACTION_LETTERS
    if len(agents) + len(partition) > len(letters):
        raise ValueError("the contraction exceeds the declared subscript pool")
    operands: list[np.ndarray] = [weight_tensor]
    subscripts: list[str] = [letters[: len(agents)]]
    output = ""
    for block_index, block in enumerate(partition):
        label = letters[len(agents) + block_index]
        output += label
        operands.append(
            _block_bayes_kernel(
                model, block, _block_prior_vector(model, block, parent_priors)
            )
        )
        subscripts.append(
            label + "".join(letters[index_of[agent]] for agent in block)
        )
    marginal = np.einsum(
        ",".join(subscripts) + "->" + output, *operands, optimize=True
    )
    return _action_and_flow_from_marginal(marginal)


def _block_prior_vector(
    model: FalsificationModel,
    block: Sequence[int],
    parent_priors: Mapping[int, Sequence[float]] | None,
) -> np.ndarray:
    """Return the parent law of one block, declared or per-root as data."""
    size = model.state_count
    if parent_priors is None:
        return np.asarray(_declared_parent_prior(size), dtype=np.float64)
    if min(block) not in parent_priors:
        raise ValueError("declared parent priors must cover every block root")
    block_prior = np.asarray(
        [float(value) for value in parent_priors[min(block)]],
        dtype=np.float64,
    )
    if block_prior.shape != (size,) or np.any(block_prior < 0.0):
        raise ValueError("a declared parent prior must be a law on parents")
    return block_prior


def _block_bayes_kernel(
    model: FalsificationModel,
    block: Sequence[int],
    block_prior: np.ndarray,
) -> np.ndarray:
    r"""Return the Bayes blocking kernel $T(p \mid x_B)$ of one block.

    The kernel is the parent law times the product of downward kernels over
    the block's members, normalized over parents, so it sums to one at every
    child configuration and the blocking preserves the partition function.
    """
    size = model.state_count
    kernel = np.asarray(block_prior, dtype=np.float64).reshape(
        (size,) + (1,) * len(block)
    ).copy()
    for offset, agent in enumerate(block):
        rows = np.stack(
            [model.downward_kernel(block, agent, parent) for parent in range(size)]
        )
        shape = [1] * (1 + len(block))
        shape[0] = size
        shape[1 + offset] = size
        kernel = kernel * rows.reshape(shape)
    return kernel / kernel.sum(axis=0, keepdims=True)


def _action_and_flow_from_marginal(
    marginal: np.ndarray,
) -> tuple[Mapping[State, Fraction], Mapping[State, Fraction]]:
    """Return the coarse action and its Boltzmann flow weights of one marginal."""
    if not np.all(np.isfinite(marginal)) or np.any(marginal <= 0.0):
        raise ValueError(
            "the coarse marginal must be strictly positive and finite; an "
            "exact-zero entry carries no finite coarse action"
        )
    energies = -np.log(marginal)
    size = marginal.shape[0] if marginal.ndim else 1
    action: dict[State, Fraction] = {}
    for state in product(range(size), repeat=marginal.ndim):
        action[state] = Fraction(float(energies[state]))
    floor = float(energies.min())
    unnormalized = {
        state: math.exp(floor - float(energies[state])) for state in action
    }
    mass = sum(unnormalized.values())
    weights = {state: Fraction(value / mass) for state, value in unnormalized.items()}
    return MappingProxyType(action), MappingProxyType(weights)


def coarse_closure_residual(
    model: FalsificationModel,
    observation: Sequence[int],
    partition: Sequence[Sequence[int]] | None = None,
) -> CoarseClosureReport:
    """Measure the interaction content of the coarse theory after blocking.

    This is the direction a renormalization step actually runs, for one blocking
    step. A partition with at least three blocks is required for a three-body
    coarse coupling to be expressible at all; with two blocks the coarse theory
    cannot carry one and reporting its absence would say nothing. Whether a small
    generated coupling is also irrelevant under iterated blocking is a separate
    claim that this measurement does not address, since it needs a fixed point to
    linearize about.
    """
    if type(model) is not FalsificationModel:
        raise TypeError("model must be a FalsificationModel")
    record = tuple(observation)
    if len(record) != len(model.agents):
        raise ValueError("the observation must carry one record per declared agent")
    if any(type(value) is not int or value not in (0, 1) for value in record):
        raise ValueError("every observation record must be binary")
    if partition is None:
        eligible = [
            candidate
            for candidate in model.candidate_partitions
            if len(candidate) >= 3
        ]
        if not eligible:
            raise ValueError(
                "no declared candidate partition carries at least three blocks"
            )
        chosen = tuple(tuple(block) for block in eligible[0])
    else:
        chosen = tuple(tuple(block) for block in partition)
    if len(chosen) < 3:
        raise ValueError("a three-body coarse coupling needs at least three blocks")
    arranged = sorted(agent for block in chosen for agent in block)
    if arranged != sorted(model.agents):
        raise ValueError("the partition must arrange every declared agent exactly once")
    action, weights = _coarse_action(model, record, chosen)
    decomposition = anchored_mobius_decompose(
        action, anchor=tuple(DECLARED_GROUND_STATE_INDEX for _ in chosen)
    )
    magnitudes: dict[int, float] = {}
    for subset, table in decomposition.components.items():
        order = len(subset)
        if not order:
            continue
        magnitudes[order] = max(
            magnitudes.get(order, 0.0),
            max(abs(float(value)) for value in table.values()),
        )
    triple_subset, triple = largest_k_body_coefficient(decomposition, 3)
    _, pair = largest_k_body_coefficient(decomposition, 2)
    admitted = [
        (),
        *((position,) for position in range(len(chosen))),
        *(
            (left, right)
            for left in range(len(chosen))
            for right in range(left + 1, len(chosen))
        ),
    ]
    projection = declared_family_projection(decomposition, admitted)
    ratio = abs(float(triple)) / abs(float(pair)) if float(pair) else math.inf
    return CoarseClosureReport(
        partition=chosen,
        order_magnitudes=tuple(sorted(magnitudes.items())),
        largest_three_body_blocks=tuple(chosen[position] for position in sorted(triple_subset)),
        largest_three_body_coefficient=float(triple),
        largest_two_body_coefficient=float(pair),
        three_to_two_ratio=float(ratio),
        flow_weighted_residual=flow_weighted_residual(projection, weights),
        pairwise_closure_holds=abs(float(triple)) <= 1.0e-12,
    )


def model_closure_residual(
    model: FalsificationModel,
    observation: Sequence[int],
) -> ClosureResidualReport:
    """Measure the marginal-child closure, which runs against the coarse direction.

    This eliminates a block's parent and reports the interaction content induced
    among its children. It is the generic mechanism by which a hidden common cause
    creates higher-order structure, and it is not a renormalization step: it
    describes children in variables that omit their parent. For the coarse theory a
    blocking step actually produces, use `coarse_closure_residual`.
    """
    if type(model) is not FalsificationModel:
        raise TypeError("model must be a FalsificationModel")
    record = tuple(observation)
    if len(record) != len(model.agents):
        raise ValueError("the observation must carry one record per declared agent")
    if any(type(value) is not int or value not in (0, 1) for value in record):
        raise ValueError("every observation record must be binary")
    partition = model.candidate_partitions[0]
    blocks: list[BlockClosureResidual] = []
    for block in partition:
        if len(block) < 3:
            continue
        action, weights = _block_action(model, record, block)
        decomposition = anchored_mobius_decompose(
            action, anchor=tuple(DECLARED_GROUND_STATE_INDEX for _ in block)
        )
        subset, coefficient = largest_k_body_coefficient(decomposition, 3)
        position_of = {agent: position for position, agent in enumerate(block)}
        induced = model.graph.induced(block)
        pairs = sorted(
            {
                (
                    min(position_of[edge.receiver], position_of[edge.source]),
                    max(position_of[edge.receiver], position_of[edge.source]),
                )
                for edge in induced.edges
                if edge.receiver != edge.source
            }
        )
        admitted = [(), *((position,) for position in range(len(block))), *pairs]
        projection = declared_family_projection(decomposition, admitted)
        blocks.append(
            BlockClosureResidual(
                block=tuple(block),
                largest_three_body_subset=frozenset(
                    block[position] for position in sorted(subset)
                ),
                largest_three_body_coefficient=float(coefficient),
                admitted_pairs=tuple(
                    (block[left], block[right]) for left, right in pairs
                ),
                projection=projection,
                residual_sup_norm=float(projection.residual_sup_norm),
                flow_weighted_residual=flow_weighted_residual(projection, weights),
            )
        )
    if not blocks:
        raise ValueError("no declared block is large enough to carry a triple term")
    worst = max(blocks, key=lambda entry: abs(entry.largest_three_body_coefficient))
    return ClosureResidualReport(
        observation=record,
        partition=tuple(tuple(block) for block in partition),
        blocks=tuple(blocks),
        largest_three_body_block=worst.block,
        largest_three_body_subset=worst.largest_three_body_subset,
        largest_three_body_coefficient=worst.largest_three_body_coefficient,
        flow_weighted_residual=max(entry.flow_weighted_residual for entry in blocks),
        pairwise_closure_holds=all(
            entry.largest_three_body_coefficient == 0.0 for entry in blocks
        ),
    )


__all__ = [
    "BlockClosureResidual",
    "ClosureResidualReport",
    "CoarseClosureReport",
    "coarse_closure_residual",
    "DECLARED_GROUND_STATE_INDEX",
    "DeclaredFamilyProjection",
    "ISING_STAR_ANCHOR",
    "ISING_STAR_LEAVES",
    "declared_family_projection",
    "flow_weighted_residual",
    "ising_star_action",
    "ising_star_convergence_ratios",
    "ising_star_leading_order",
    "ising_star_three_body_coefficient",
    "largest_k_body_coefficient",
    "model_closure_residual",
]
