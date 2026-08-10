"""Exact finite application tuple for the four-agent, two-scale laboratory."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
import json
import math
from pathlib import Path
from types import MappingProxyType
from typing import Iterable, Literal, Mapping, Sequence

from multiagent_elbo.experiment_support import validate_two_scale_application_fixture


ExactVector = tuple[Fraction, ...]
ExactMatrix = tuple[ExactVector, ...]
ScenarioName = Literal[
    "aligned", "frustrated", "asymmetric_evidence", "higher_order"
]


def _fraction_vector(values: Sequence[object]) -> ExactVector:
    return tuple(Fraction(value) for value in values)


def _fraction_matrix(values: Sequence[Sequence[object]]) -> ExactMatrix:
    return tuple(_fraction_vector(row) for row in values)


@dataclass(frozen=True)
class ApplicationFixture:
    """Validated exact data shared by the scientific implementation lanes."""

    application_id: str
    agent_ids: tuple[str, ...]
    fine_labels: tuple[str, ...]
    coarse_labels: tuple[str, ...]
    baseline: ExactVector
    observation_likelihood: ExactVector
    evidence_measure: ExactVector
    evidence: Fraction
    posterior: ExactVector
    fine_reference: ExactVector
    fine_axis_references: ExactMatrix
    coarse_reference: ExactVector
    coarse_axis_references: ExactMatrix
    recognition_law: ExactVector
    coarse_recognition_law: ExactVector
    channel: ExactMatrix
    configuration_scale_map: ExactMatrix
    local_blocks: Mapping[str, tuple[tuple[int, ...], tuple[int, ...]]]
    oriented_edges: tuple[tuple[str, str, str], ...]
    hyperedges: Mapping[str, tuple[str, ...]]


@dataclass(frozen=True)
class ScenarioApplication:
    """One explicit normalized interaction-record extension of the frozen tuple."""

    fixture: ApplicationFixture
    scenario: ScenarioName
    interaction_record_kernels: Mapping[str, ExactMatrix]
    interaction_action_log2: ExactVector
    total_likelihood: ExactVector
    evidence_measure: ExactVector
    evidence: Fraction
    posterior: ExactVector
    coarse_baseline: ExactVector
    coarse_evidence_measure: ExactVector
    coarse_posterior: ExactVector
    coarse_effective_likelihood: ExactVector


@dataclass(frozen=True)
class ExactInteractionDecomposition:
    """Full product-reference Hoeffding components in broadcast state order."""

    components: Mapping[tuple[int, ...], ExactVector]
    reconstruction: ExactVector
    reconstruction_residual: Fraction


@dataclass(frozen=True)
class VfeGap:
    """Direct unnormalized VFE and its posterior-KL representation."""

    direct_vfe: float
    posterior_kl: float
    negative_log_evidence: float
    residual: float


@dataclass(frozen=True)
class LocalCollectiveDifference:
    """A fixed-outside conditional update compared with the joint KL change."""

    local_difference: float
    collective_difference: float
    residual: float
    outside_marginal: ExactVector


@dataclass(frozen=True)
class PremiseAssessment:
    """Application-premise result without changing the conditional theorem status."""

    claim_id: str
    satisfied: bool
    theorem_status: Literal["HYPOTHESIS"]
    verification_state: Literal["EVIDENCE_VERIFIED", "INCONCLUSIVE"]
    claim_origin: Literal["APPLICATION_SPECIFIC"]
    reason: str


def load_application_fixture(path: Path | str) -> ApplicationFixture:
    """Load and validate the frozen fixture before constructing runtime state."""
    fixture_path = Path(path)
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("application fixture must be a JSON object")
    application_id = validate_two_scale_application_fixture(payload)

    state_spaces = payload["state_spaces"]
    generative = payload["generative_structure"]
    references = payload["reference_laws"]
    recognition = payload["recognition"]
    configuration = payload["configuration"]
    interaction_complex = payload["interaction_complex"]
    arrows = payload["channel"]["arrows"]
    if len(arrows) != 1:
        raise ValueError("two-scale application requires exactly one channel arrow")
    arrow = arrows[0]

    fine_axis_order = tuple(state_spaces["fine"]["axis_order"])
    axis_index = {name: index for index, name in enumerate(fine_axis_order)}
    local_blocks = {
        block["block_id"]: (
            tuple(axis_index[name] for name in block["updated_axes"]),
            tuple(axis_index[name] for name in block["outside_axes"]),
        )
        for block in payload["local_blocks"]
    }
    observed_index = tuple(generative["observation_labels"]).index(
        generative["observed_record"]
    )
    observation_likelihood = tuple(
        Fraction(row[observed_index]) for row in generative["observation_record_kernel"]
    )

    return ApplicationFixture(
        application_id=application_id,
        agent_ids=tuple(agent["agent_id"] for agent in payload["agents"]),
        fine_labels=tuple(state_spaces["fine"]["labels"]),
        coarse_labels=tuple(state_spaces["coarse"]["labels"]),
        baseline=_fraction_vector(generative["correlated_baseline"]),
        observation_likelihood=observation_likelihood,
        evidence_measure=_fraction_vector(generative["evidence_submeasure"]),
        evidence=Fraction(generative["evidence_mass"]),
        posterior=_fraction_vector(generative["posterior"]),
        fine_reference=_fraction_vector(references["fine"]["values"]),
        fine_axis_references=_fraction_matrix(references["fine"]["factor_values"]),
        coarse_reference=_fraction_vector(references["coarse"]["values"]),
        coarse_axis_references=_fraction_matrix(
            references["coarse"]["factor_values"]
        ),
        recognition_law=_fraction_vector(recognition["fine_law"]),
        coarse_recognition_law=_fraction_vector(recognition["coarse_law"]),
        channel=_fraction_matrix(arrow["rows"]),
        configuration_scale_map=_fraction_matrix(
            configuration["coarse_map_matrix"]
        ),
        local_blocks=MappingProxyType(local_blocks),
        oriented_edges=tuple(
            (edge["edge_id"], edge["source"], edge["target"])
            for edge in interaction_complex["oriented_edges"]
        ),
        hyperedges=MappingProxyType(
            {
                hyperedge["hyperedge_id"]: tuple(hyperedge["members"])
                for hyperedge in interaction_complex["hyperedges"]
            }
        ),
    )


def _pushforward(law: ExactVector, channel: ExactMatrix) -> ExactVector:
    if len(law) != len(channel):
        raise ValueError("law length must match channel source size")
    target_size = len(channel[0])
    if any(len(row) != target_size or sum(row) != 1 for row in channel):
        raise ValueError("channel must be rectangular and row normalized")
    return tuple(
        sum((mass * channel[source][target] for source, mass in enumerate(law)), Fraction())
        for target in range(target_size)
    )


def _binary_states(labels: Sequence[str]) -> tuple[tuple[int, ...], ...]:
    states: list[tuple[int, ...]] = []
    for label in labels:
        if not label or any(bit not in "01" for bit in label):
            raise ValueError("fine labels must be binary strings")
        states.append(tuple(int(bit) for bit in label))
    return tuple(states)


def _record_kernel(success: Sequence[Fraction]) -> ExactMatrix:
    rows = tuple((value, Fraction(1) - value) for value in success)
    if any(value <= 0 or value > 1 for value in success):
        raise ValueError("record success probabilities must lie in (0, 1]")
    if any(sum(row) != 1 for row in rows):
        raise ValueError("interaction record kernels must be normalized")
    return rows


def _penalty_success(
    states: Sequence[tuple[int, ...]],
    source: int,
    target: int,
    *,
    weight: int,
    prefer_equal: bool,
) -> ExactVector:
    return tuple(
        Fraction(1)
        if ((state[source] == state[target]) is prefer_equal)
        else Fraction(1, 2**weight)
        for state in states
    )


def _scenario_records(
    fixture: ApplicationFixture, scenario: ScenarioName
) -> Mapping[str, ExactMatrix]:
    states = _binary_states(fixture.fine_labels)
    agent_index = {agent_id: index for index, agent_id in enumerate(fixture.agent_ids)}
    edge_weights = (1, 1, 1, 1)
    if scenario == "asymmetric_evidence":
        edge_weights = (1, 2, 3, 4)

    records: dict[str, ExactMatrix] = {}
    for edge_position, (edge_id, source_id, target_id) in enumerate(
        fixture.oriented_edges
    ):
        prefer_equal = not (scenario == "frustrated" and edge_id == "e30")
        success = _penalty_success(
            states,
            agent_index[source_id],
            agent_index[target_id],
            weight=edge_weights[edge_position],
            prefer_equal=prefer_equal,
        )
        records[edge_id] = _record_kernel(success)

    if scenario == "higher_order":
        members = fixture.hyperedges.get("h012")
        if members is None:
            raise ValueError("higher_order scenario requires hyperedge h012")
        axes = tuple(agent_index[member] for member in members)
        success = tuple(
            Fraction(1)
            if sum(state[axis] for axis in axes) % 2 == 0
            else Fraction(1, 4)
            for state in states
        )
        records["h012"] = _record_kernel(success)
    return MappingProxyType(records)


def _log2_penalty(probability: Fraction) -> Fraction:
    if probability.numerator != 1:
        raise ValueError("scenario success probabilities must be powers of two")
    denominator = probability.denominator
    if denominator & (denominator - 1):
        raise ValueError("scenario success probabilities must be powers of two")
    return Fraction(denominator.bit_length() - 1)


def build_scenario_application(
    fixture: ApplicationFixture, scenario: str
) -> ScenarioApplication:
    """Attach one declared record family and compute its exact one-arrow laws."""
    if not isinstance(fixture, ApplicationFixture):
        raise TypeError("fixture must be an ApplicationFixture")
    if scenario not in {
        "aligned",
        "frustrated",
        "asymmetric_evidence",
        "higher_order",
    }:
        raise ValueError("invalid multi-agent scenario")
    scenario_name: ScenarioName = scenario  # type: ignore[assignment]
    records = _scenario_records(fixture, scenario_name)
    interaction_likelihood = tuple(
        _product(record[state_index][0] for record in records.values())
        for state_index in range(len(fixture.fine_labels))
    )
    interaction_action = tuple(
        sum(
            (_log2_penalty(record[state_index][0]) for record in records.values()),
            Fraction(),
        )
        for state_index in range(len(fixture.fine_labels))
    )
    total_likelihood = tuple(
        observed * interaction
        for observed, interaction in zip(
            fixture.observation_likelihood, interaction_likelihood
        )
    )
    evidence_measure = tuple(
        baseline * likelihood
        for baseline, likelihood in zip(fixture.baseline, total_likelihood)
    )
    evidence = sum(evidence_measure, Fraction())
    if evidence <= 0:
        raise ValueError("scenario must have positive finite evidence")
    posterior = tuple(mass / evidence for mass in evidence_measure)
    coarse_baseline = _pushforward(fixture.baseline, fixture.channel)
    coarse_evidence_measure = _pushforward(evidence_measure, fixture.channel)
    coarse_posterior = tuple(mass / evidence for mass in coarse_evidence_measure)
    coarse_effective_likelihood = tuple(
        mass / reference
        for mass, reference in zip(coarse_evidence_measure, coarse_baseline)
    )
    return ScenarioApplication(
        fixture=fixture,
        scenario=scenario_name,
        interaction_record_kernels=records,
        interaction_action_log2=interaction_action,
        total_likelihood=total_likelihood,
        evidence_measure=evidence_measure,
        evidence=evidence,
        posterior=posterior,
        coarse_baseline=coarse_baseline,
        coarse_evidence_measure=coarse_evidence_measure,
        coarse_posterior=coarse_posterior,
        coarse_effective_likelihood=coarse_effective_likelihood,
    )


def product_bernoulli_law(parameters: Sequence[Fraction]) -> ExactVector:
    """Lift four open-unit Bernoulli coordinates to the ordered product law."""
    probabilities = tuple(Fraction(value) for value in parameters)
    if len(probabilities) != 4:
        raise ValueError("recognition parameters must contain four coordinates")
    if any(value <= 0 or value >= 1 for value in probabilities):
        raise ValueError("recognition parameters must lie in the open unit cube")
    return tuple(
        _product(
            probability if bit == "1" else Fraction(1) - probability
            for bit, probability in zip(f"{state:04b}", probabilities)
        )
        for state in range(16)
    )


def extract_bernoulli_coordinates(law: Sequence[Fraction]) -> ExactVector:
    """Extract the four one-site success marginals from an ordered fine law."""
    masses = tuple(Fraction(value) for value in law)
    if len(masses) != 16 or any(value < 0 for value in masses):
        raise ValueError("recognition law must have sixteen nonnegative masses")
    if sum(masses, Fraction()) != 1:
        raise ValueError("recognition law must sum exactly to one")
    return tuple(
        sum(
            (mass for state, mass in enumerate(masses) if f"{state:04b}"[axis] == "1"),
            Fraction(),
        )
        for axis in range(4)
    )


def recognition_lift_residual(
    parameters: Sequence[Fraction], lifted_law: Sequence[Fraction] | None = None
) -> Fraction:
    """Return the exact sup residual of extraction after the declared lift."""
    expected = tuple(Fraction(value) for value in parameters)
    active_law = (
        product_bernoulli_law(expected) if lifted_law is None else tuple(lifted_law)
    )
    extracted = extract_bernoulli_coordinates(active_law)
    if len(extracted) != len(expected):
        raise ValueError("lifted coordinate dimension does not match parameters")
    return max(
        (abs(actual - target) for actual, target in zip(extracted, expected)),
        default=Fraction(),
    )


def _axis_states(axis_references: Sequence[Sequence[Fraction]]) -> tuple[tuple[int, ...], ...]:
    lengths = tuple(len(reference) for reference in axis_references)
    if not lengths or any(length <= 0 for length in lengths):
        raise ValueError("axis references must be nonempty")
    return tuple(product(*(range(length) for length in lengths)))


def _all_subsets(axis_count: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        subset
        for size in range(axis_count + 1)
        for subset in combinations(range(axis_count), size)
    )


def exact_hoeffding_decompose(
    values: Sequence[Fraction], axis_references: Sequence[Sequence[Fraction]]
) -> ExactInteractionDecomposition:
    """Compute exact finite Hoeffding/Mobius components with ``Fraction`` arithmetic."""
    references = tuple(tuple(Fraction(value) for value in row) for row in axis_references)
    if any(any(value < 0 for value in row) or sum(row, Fraction()) != 1 for row in references):
        raise ValueError("each axis reference must be an exact probability law")
    states = _axis_states(references)
    action = tuple(Fraction(value) for value in values)
    if len(action) != len(states):
        raise ValueError("action length must match the product state space")
    state_index = {state: index for index, state in enumerate(states)}
    subsets = _all_subsets(len(references))

    conditional: dict[tuple[int, ...], ExactVector] = {}
    for subset in subsets:
        active = set(subset)
        averaged: list[Fraction] = []
        for target_state in states:
            total = Fraction()
            for source_state in states:
                if any(source_state[axis] != target_state[axis] for axis in active):
                    continue
                weight = _product(
                    references[axis][source_state[axis]]
                    for axis in range(len(references))
                    if axis not in active
                )
                total += action[state_index[source_state]] * weight
            averaged.append(total)
        conditional[subset] = tuple(averaged)

    components: dict[tuple[int, ...], ExactVector] = {}
    for subset in subsets:
        component = []
        for state_position in range(len(states)):
            value = Fraction()
            for proper_size in range(len(subset) + 1):
                for proper in combinations(subset, proper_size):
                    sign = -1 if (len(subset) - len(proper)) % 2 else 1
                    value += sign * conditional[proper][state_position]
            component.append(value)
        components[subset] = tuple(component)

    reconstruction = tuple(
        sum((components[subset][position] for subset in subsets), Fraction())
        for position in range(len(states))
    )
    residual = max(
        (abs(actual - expected) for actual, expected in zip(reconstruction, action)),
        default=Fraction(),
    )
    return ExactInteractionDecomposition(
        components=MappingProxyType(components),
        reconstruction=reconstruction,
        reconstruction_residual=residual,
    )


def retained_interaction_residual(
    decomposition: ExactInteractionDecomposition, *, maximum_order: int
) -> Fraction:
    """Return the exact sup norm of interactions omitted above the retained order."""
    if type(maximum_order) is not int or maximum_order < 0:
        raise ValueError("maximum_order must be a nonnegative int")
    if not isinstance(decomposition, ExactInteractionDecomposition):
        raise TypeError("decomposition must be an ExactInteractionDecomposition")
    omitted = tuple(
        sum(
            (
                component[position]
                for subset, component in decomposition.components.items()
                if len(subset) > maximum_order
            ),
            Fraction(),
        )
        for position in range(len(decomposition.reconstruction))
    )
    return max((abs(value) for value in omitted), default=Fraction())


def _exact_probability(law: Sequence[Fraction], name: str) -> ExactVector:
    masses = tuple(Fraction(value) for value in law)
    if not masses or any(value < 0 for value in masses):
        raise ValueError(f"{name} must be a nonnegative probability law")
    if sum(masses, Fraction()) != 1:
        raise ValueError(f"{name} must sum exactly to one")
    return masses


def _kl(q: ExactVector, p: ExactVector) -> float:
    if len(q) != len(p):
        raise ValueError("KL laws must have matching support")
    total = 0.0
    for q_mass, p_mass in zip(q, p):
        if q_mass == 0:
            continue
        if p_mass == 0:
            raise ValueError("finite application checks require finite posterior KL")
        total += float(q_mass) * math.log(float(q_mass / p_mass))
    return total


def global_vfe_gap(
    recognition: Sequence[Fraction], evidence_measure: Sequence[Fraction]
) -> VfeGap:
    """Evaluate the joint VFE and independent posterior-KL gap formula."""
    q = _exact_probability(recognition, "recognition")
    measure = tuple(Fraction(value) for value in evidence_measure)
    if len(measure) != len(q) or any(value < 0 for value in measure):
        raise ValueError("evidence measure must match the recognition support")
    evidence = sum(measure, Fraction())
    if evidence <= 0:
        raise ValueError("VFE requires positive evidence")
    posterior = tuple(value / evidence for value in measure)
    direct = 0.0
    for q_mass, evidence_mass in zip(q, measure):
        if q_mass == 0:
            continue
        if evidence_mass == 0:
            raise ValueError("finite application checks require finite posterior KL")
        direct += float(q_mass) * math.log(float(q_mass / evidence_mass))
    posterior_kl = _kl(q, posterior)
    negative_log_evidence = -math.log(float(evidence))
    return VfeGap(
        direct_vfe=direct,
        posterior_kl=posterior_kl,
        negative_log_evidence=negative_log_evidence,
        residual=direct - (posterior_kl + negative_log_evidence),
    )


def _binary_support(length: int) -> tuple[tuple[int, ...], ...]:
    if length <= 0 or length & (length - 1):
        raise ValueError("law support must be a nonempty binary product")
    axis_count = length.bit_length() - 1
    return tuple(product((0, 1), repeat=axis_count))


def _outside_marginal(law: ExactVector, block_axes: tuple[int, ...]) -> ExactVector:
    states = _binary_support(len(law))
    axis_count = len(states[0])
    if not block_axes or len(set(block_axes)) != len(block_axes):
        raise ValueError("block_axes must be unique and nonempty")
    if any(type(axis) is not int or axis < 0 or axis >= axis_count for axis in block_axes):
        raise ValueError("block_axes must index the binary product")
    outside_axes = tuple(axis for axis in range(axis_count) if axis not in block_axes)
    outside_states = tuple(product((0, 1), repeat=len(outside_axes)))
    return tuple(
        sum(
            (
                mass
                for state, mass in zip(states, law)
                if tuple(state[axis] for axis in outside_axes) == outside_state
            ),
            Fraction(),
        )
        for outside_state in outside_states
    )


def _weighted_conditional_kl(
    recognition: ExactVector, posterior: ExactVector, block_axes: tuple[int, ...]
) -> float:
    states = _binary_support(len(recognition))
    axis_count = len(states[0])
    outside_axes = tuple(axis for axis in range(axis_count) if axis not in block_axes)
    q_outside = _outside_marginal(recognition, block_axes)
    p_outside = _outside_marginal(posterior, block_axes)
    outside_states = tuple(product((0, 1), repeat=len(outside_axes)))
    total = 0.0
    for outside_index, outside_state in enumerate(outside_states):
        q_weight = q_outside[outside_index]
        if q_weight == 0:
            continue
        p_weight = p_outside[outside_index]
        if p_weight == 0:
            raise ValueError("finite application checks require finite conditional KL")
        for state, q_mass, p_mass in zip(states, recognition, posterior):
            if tuple(state[axis] for axis in outside_axes) != outside_state or q_mass == 0:
                continue
            if p_mass == 0:
                raise ValueError("finite application checks require finite conditional KL")
            q_conditional = q_mass / q_weight
            p_conditional = p_mass / p_weight
            total += float(q_mass) * math.log(float(q_conditional / p_conditional))
    return total


def local_collective_difference(
    posterior: Sequence[Fraction],
    q_before: Sequence[Fraction],
    q_after: Sequence[Fraction],
    *,
    block_axes: tuple[int, ...],
) -> LocalCollectiveDifference:
    """Evaluate the exact fixed-outside local-to-collective difference identity."""
    target = _exact_probability(posterior, "posterior")
    before = _exact_probability(q_before, "q_before")
    after = _exact_probability(q_after, "q_after")
    if not (len(target) == len(before) == len(after)):
        raise ValueError("posterior and recognition laws must have matching support")
    before_outside = _outside_marginal(before, block_axes)
    after_outside = _outside_marginal(after, block_axes)
    if before_outside != after_outside:
        raise ValueError("q_before and q_after must have exactly equal outside marginals")
    local_difference = _weighted_conditional_kl(
        after, target, block_axes
    ) - _weighted_conditional_kl(
        before,
        target,
        block_axes,
    )
    collective_difference = _kl(after, target) - _kl(before, target)
    return LocalCollectiveDifference(
        local_difference=local_difference,
        collective_difference=collective_difference,
        residual=local_difference - collective_difference,
        outside_marginal=before_outside,
    )


def overlapping_local_objective_gap(
    posterior: Sequence[Fraction],
    recognition: Sequence[Fraction],
    blocks: Sequence[tuple[int, ...]],
) -> float:
    """Return the mismatch between overlapping conditional KL sums and joint KL."""
    target = _exact_probability(posterior, "posterior")
    q = _exact_probability(recognition, "recognition")
    if len(target) != len(q):
        raise ValueError("posterior and recognition laws must have matching support")
    local_sum = sum(_weighted_conditional_kl(q, target, block) for block in blocks)
    return local_sum - _kl(q, target)


_SCENARIO_RECOGNITION_TARGETS: Mapping[ScenarioName, ExactVector] = MappingProxyType(
    {
        "aligned": (Fraction(1, 4), Fraction(1, 4), Fraction(3, 4), Fraction(3, 4)),
        "frustrated": (Fraction(1, 4), Fraction(3, 4), Fraction(3, 4), Fraction(1, 4)),
        "asymmetric_evidence": (
            Fraction(3, 4),
            Fraction(1, 4),
            Fraction(2, 3),
            Fraction(1, 3),
        ),
        "higher_order": (
            Fraction(2, 5),
            Fraction(3, 5),
            Fraction(3, 5),
            Fraction(2, 5),
        ),
    }
)


def scenario_recognition_target(scenario: str) -> ExactVector:
    """Return the declared exact target coordinates for one scenario."""
    try:
        return _SCENARIO_RECOGNITION_TARGETS[scenario]  # type: ignore[index]
    except KeyError as error:
        raise ValueError("invalid multi-agent scenario") from error


def assess_fixed_channel_premise(*, recognition_independent: bool) -> PremiseAssessment:
    """Classify the concrete channel premise without claiming theorem refutation."""
    if type(recognition_independent) is not bool:
        raise TypeError("recognition_independent must be a bool")
    if recognition_independent:
        return PremiseAssessment(
            claim_id="APP-HYP-FIXED-CHANNEL",
            satisfied=True,
            theorem_status="HYPOTHESIS",
            verification_state="EVIDENCE_VERIFIED",
            claim_origin="APPLICATION_SPECIFIC",
            reason="the declared channel is fixed and recognition-independent",
        )
    return PremiseAssessment(
        claim_id="APP-HYP-FIXED-CHANNEL",
        satisfied=False,
        theorem_status="HYPOTHESIS",
        verification_state="INCONCLUSIVE",
        claim_origin="APPLICATION_SPECIFIC",
        reason="a parameter-dependent channel is outside the fixed-channel theorem",
    )


def _product(values: Iterable[Fraction]) -> Fraction:
    result = Fraction(1)
    for value in values:
        result *= value
    return result


__all__ = [
    "ApplicationFixture",
    "ExactInteractionDecomposition",
    "LocalCollectiveDifference",
    "PremiseAssessment",
    "ScenarioApplication",
    "VfeGap",
    "build_scenario_application",
    "assess_fixed_channel_premise",
    "exact_hoeffding_decompose",
    "extract_bernoulli_coordinates",
    "global_vfe_gap",
    "load_application_fixture",
    "local_collective_difference",
    "overlapping_local_objective_gap",
    "product_bernoulli_law",
    "recognition_lift_residual",
    "retained_interaction_residual",
    "scenario_recognition_target",
]
