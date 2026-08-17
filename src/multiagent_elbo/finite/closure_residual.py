"""Generated many-body terms and the closure residual of a declared parent family.

Exactly eliminating an internal variable from a finite model generates the whole
hyperedge family on the variables that survive, and that hierarchy is recovered by
Moebius inversion of the surviving action against a declared ground configuration.
This module measures two consequences on the declared categorical system. The
first is the largest generated three-body coefficient, which decides whether a
pairwise coarse theory can be exact at all. The second is the residual left by
projecting the action onto a declared parent family, reported as a ratio against
the retained flow rather than as a bare sup norm.

The projection admits a declared set of subsets rather than an order cutoff. On
the declared blocks of the reference design the graph's edge pairs exhaust the
pairs, so there the declared family and the order-two cutoff coincide; the
distinction is real for any block whose induced edge set is a proper subset of the
pairs, and it is exercised directly in the tests.

The flow weighting is the exact block configuration law of the declared model,
which is the normalized Boltzmann measure of the same action being decomposed. The
reported ratio divides the flow-averaged magnitude of the omitted part by the
flow-averaged deviation of the retained part from its own flow average. The
constant component of the retained part carries no physical content because it
cancels in every probability, so removing it is what turns the ratio into a
statement about the retained flow rather than about an arbitrary offset. The ratio
is invariant under rescaling the weights.

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
from .scale_cocycle import (
    AnchoredMobiusDecomposition,
    State,
    Subset,
    anchored_mobius_decompose,
)

DECLARED_GROUND_STATE_INDEX = 0
ISING_STAR_ANCHOR: State = (-1, -1, -1)
ISING_STAR_LEAVES = 3


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
    """Return the flow-averaged omitted magnitude over the flow-averaged retained spread."""
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
    numerator = sum(
        (weights[state] * abs(value) for state, value in projection.omitted_value.items()),
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
    edge_terms: list[tuple[int, int, float, np.ndarray]] = []
    for edge_index, edge in enumerate(induced.edges):
        for channel in ("belief", "model"):
            weight = float(
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
    parent_prior = 1.0 / size
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
            term = parent_prior
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


def model_closure_residual(
    model: FalsificationModel,
    observation: Sequence[int],
) -> ClosureResidualReport:
    """Measure the generated three-body coefficient and the pairwise closure residual."""
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
