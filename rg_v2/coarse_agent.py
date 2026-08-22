"""Immutable semantic contracts for the recursive coarse-agent fixture."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import hashlib
import json
import math
import re
from typing import Literal

from multiagent_elbo.config import NumericsConfig
from multiagent_elbo.finite.scale_cocycle import ExactMarkovChannel
from rg_v2.contracts import (
    AgentDatum,
    AgentRecognitionDatum,
    CoarseChannelSpec,
    ExactProbabilityLaw,
    ModelEvaluation,
    PopulationInference,
    PopulationJoint,
    RecordDatum,
    SelectorSpec,
)
from rg_v2.population import construct_population_joint, derive_population_inference


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True, allow_nan=False)


def _require_identifier(value: str, *, field: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a nonempty string")


def _require_labels(labels: tuple[str, ...], *, field: str) -> None:
    if not isinstance(labels, tuple) or not labels or any(not isinstance(label, str) or not label for label in labels):
        raise ValueError(f"{field} must be a nonempty tuple of nonempty strings")
    if len(set(labels)) != len(labels):
        raise ValueError(f"{field} must be unique")


def _require_sha256(value: str, *, field: str) -> None:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise ValueError(f"{field} must be 64 lowercase hexadecimal characters")


def canonical_local_state_labels(
    belief_labels: tuple[str, ...],
    model_labels: tuple[str, ...],
) -> tuple[str, ...]:
    """Return the belief-major compact-JSON local-state support."""
    return tuple(_canonical_json([belief, model]) for belief in belief_labels for model in model_labels)


def _parse_local_state(label: str, *, field: str) -> tuple[str, str]:
    try:
        parsed = json.loads(label)
    except json.JSONDecodeError as error:
        raise ValueError(f"{field} labels must be canonical compact JSON") from error
    if (
        _canonical_json(parsed) != label
        or not isinstance(parsed, list)
        or len(parsed) != 2
        or any(not isinstance(part, str) or not part for part in parsed)
    ):
        raise ValueError(f"{field} labels must be canonical compact JSON")
    return parsed[0], parsed[1]


def canonical_agent_assignment_labels(agents: tuple[AgentDatum, ...]) -> tuple[str, ...]:
    """Return canonical assignments in the declared agent and state order."""
    if not isinstance(agents, tuple) or not agents or any(not isinstance(agent, AgentDatum) for agent in agents):
        raise TypeError("agents must be a nonempty tuple of AgentDatum values")
    agent_ids = tuple(agent.agent_id for agent in agents)
    if len(set(agent_ids)) != len(agent_ids):
        raise ValueError("agent IDs must be unique")
    state_coordinates = tuple(tuple(_parse_local_state(label, field="agent state") for label in agent.state_labels) for agent in agents)
    return tuple(
        _canonical_json(
            [[agent.agent_id, belief, model] for agent, (belief, model) in zip(agents, assignment, strict=True)]
        )
        for assignment in __import__("itertools").product(*state_coordinates)
    )


def channel_sha256(channel: ExactMarkovChannel) -> str:
    """Hash only an exact channel's canonical semantic declaration."""
    if not isinstance(channel, ExactMarkovChannel):
        raise TypeError("channel must be an ExactMarkovChannel")
    payload = {
        "matrix": [
            [
                {"denominator": mass.denominator, "numerator": mass.numerator}
                for mass in row
            ]
            for row in channel.matrix
        ],
        "recognition_independent": channel.recognition_independent,
        "source_labels": list(channel.source_labels),
        "target_labels": list(channel.target_labels),
    }
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _require_exact_joint_matrix(
    rows: tuple[tuple[Fraction, ...], ...],
    row_count: int,
    column_count: int,
    *,
    field: str,
) -> None:
    if not isinstance(rows, tuple) or len(rows) != row_count:
        raise ValueError(f"{field} rows must align with labels")
    if any(not isinstance(row, tuple) or len(row) != column_count for row in rows):
        raise ValueError(f"{field} columns must align with labels")
    masses = tuple(mass for row in rows for mass in row)
    if any(not isinstance(mass, Fraction) for mass in masses):
        raise TypeError(f"{field} masses must be exact Fraction values")
    if any(mass < 0 for mass in masses) or sum(masses, Fraction(0)) != 1:
        raise ValueError(f"{field} masses must be nonnegative and sum to one exactly")


def _require_channel_assignments(channel: ExactMarkovChannel, source_agent_ids: tuple[str, ...]) -> None:
    for label in channel.source_labels:
        try:
            parsed = json.loads(label)
        except json.JSONDecodeError as error:
            raise ValueError("block channel source labels must be canonical ordered assignments") from error
        if _canonical_json(parsed) != label or not isinstance(parsed, list) or len(parsed) != len(source_agent_ids):
            raise ValueError("block channel source labels must be canonical ordered assignments")
        for agent_id, item in zip(source_agent_ids, parsed, strict=True):
            if (
                not isinstance(item, list)
                or len(item) != 3
                or item[0] != agent_id
                or any(not isinstance(value, str) or not value for value in item)
            ):
                raise ValueError("block channel source labels must be canonical ordered assignments")


@dataclass(frozen=True)
class CoarseAgentSpec:
    agent_id: str
    source_agent_ids: tuple[str, ...]
    parent_ids: tuple[str, ...]
    source_context_id: str
    belief_labels: tuple[str, ...]
    model_labels: tuple[str, ...]
    state_labels: tuple[str, ...]
    block_channel: ExactMarkovChannel
    null_row_policy: Literal["forbid"]

    def __post_init__(self) -> None:
        _require_identifier(self.agent_id, field="coarse agent ID")
        _require_labels(self.source_agent_ids, field="source agent IDs")
        if not isinstance(self.parent_ids, tuple) or len(set(self.parent_ids)) != len(self.parent_ids):
            raise ValueError("parent IDs must be a unique tuple")
        for parent_id in self.parent_ids:
            _require_identifier(parent_id, field="parent ID")
        if self.agent_id in self.parent_ids:
            raise ValueError("a coarse agent cannot be its own parent")
        _require_identifier(self.source_context_id, field="source context ID")
        _require_labels(self.belief_labels, field="belief labels")
        _require_labels(self.model_labels, field="model labels")
        if self.state_labels != canonical_local_state_labels(self.belief_labels, self.model_labels):
            raise ValueError("state labels must be the belief-major canonical Cartesian product")
        if not isinstance(self.block_channel, ExactMarkovChannel):
            raise TypeError("block channel must be an ExactMarkovChannel")
        if self.block_channel.recognition_independent is not True:
            raise ValueError("block channel must be recognition-independent")
        if self.block_channel.target_labels != self.state_labels:
            raise ValueError("block channel target labels must equal state labels")
        _require_channel_assignments(self.block_channel, self.source_agent_ids)
        if self.null_row_policy != "forbid":
            raise ValueError("null row policy must be 'forbid'")


@dataclass(frozen=True)
class CoarseObservationSpec:
    record_id: str
    fine_observation_labels: tuple[str, ...]
    compound_outcome_labels: tuple[str, ...]
    compound_outcome_by_fine_observation: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_identifier(self.record_id, field="compound record ID")
        _require_labels(self.fine_observation_labels, field="fine observation labels")
        _require_labels(self.compound_outcome_labels, field="compound outcome labels")
        if (
            not isinstance(self.compound_outcome_by_fine_observation, tuple)
            or len(self.compound_outcome_by_fine_observation) != len(self.fine_observation_labels)
            or set(self.compound_outcome_by_fine_observation) != set(self.compound_outcome_labels)
            or len(set(self.compound_outcome_by_fine_observation)) != len(self.compound_outcome_by_fine_observation)
        ):
            raise ValueError("observation map must be an ordered bijection")


@dataclass(frozen=True)
class SparseRecordFactorizationSpec:
    left_record_ids: tuple[str, ...]
    right_record_ids: tuple[str, ...]
    left_outcome_labels: tuple[str, ...]
    right_outcome_labels: tuple[str, ...]
    left_outcome_by_fine_observation: tuple[str, ...]
    right_outcome_by_fine_observation: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_labels(self.left_record_ids, field="left record IDs")
        _require_labels(self.right_record_ids, field="right record IDs")
        if set(self.left_record_ids) & set(self.right_record_ids):
            raise ValueError("sparse record groups must be disjoint")
        _require_labels(self.left_outcome_labels, field="left outcome labels")
        _require_labels(self.right_outcome_labels, field="right outcome labels")
        for projection, labels, field in (
            (self.left_outcome_by_fine_observation, self.left_outcome_labels, "left sparse projection"),
            (self.right_outcome_by_fine_observation, self.right_outcome_labels, "right sparse projection"),
        ):
            if not isinstance(projection, tuple) or any(value not in labels for value in projection):
                raise ValueError(f"{field} must use declared outcome labels")


@dataclass(frozen=True)
class RecursiveCoarseStructure:
    structure_id: str
    source_agent_order: tuple[str, ...]
    coarse_agent_order: tuple[str, ...]
    agent_specs: tuple[CoarseAgentSpec, ...]
    observation: CoarseObservationSpec
    sparse_record_candidate: SparseRecordFactorizationSpec

    def __post_init__(self) -> None:
        _require_identifier(self.structure_id, field="structure ID")
        _require_labels(self.source_agent_order, field="source agent order")
        _require_labels(self.coarse_agent_order, field="coarse agent order")
        if not isinstance(self.agent_specs, tuple) or any(not isinstance(spec, CoarseAgentSpec) for spec in self.agent_specs):
            raise TypeError("agent specs must be CoarseAgentSpec values")
        if tuple(spec.agent_id for spec in self.agent_specs) != self.coarse_agent_order:
            raise ValueError("coarse agent order must equal declared agent specs")
        declared_sources = tuple(agent_id for spec in self.agent_specs for agent_id in spec.source_agent_ids)
        if declared_sources != self.source_agent_order:
            raise ValueError("source blocks must be disjoint and exhaustive")
        seen: set[str] = set()
        for spec in self.agent_specs:
            if any(parent_id not in seen for parent_id in spec.parent_ids):
                raise ValueError("coarse agents must be topologically ordered")
            seen.add(spec.agent_id)
        if len({spec.source_context_id for spec in self.agent_specs}) != 1:
            raise ValueError("coarse agent source contexts must agree")
        if not isinstance(self.observation, CoarseObservationSpec):
            raise TypeError("observation must be a CoarseObservationSpec")
        if not isinstance(self.sparse_record_candidate, SparseRecordFactorizationSpec):
            raise TypeError("sparse record candidate must be a SparseRecordFactorizationSpec")
        sparse = self.sparse_record_candidate
        fine_count = len(self.observation.fine_observation_labels)
        if (
            len(sparse.left_outcome_by_fine_observation) != fine_count
            or len(sparse.right_outcome_by_fine_observation) != fine_count
        ):
            raise ValueError("sparse projections must cover every fine observation")


def validate_coarse_structure_source_supports(
    structure: RecursiveCoarseStructure,
    source_agents: tuple[AgentDatum, ...],
) -> None:
    """Require each declared block channel to use its exact fine-agent support."""
    if not isinstance(structure, RecursiveCoarseStructure):
        raise TypeError("structure must be a RecursiveCoarseStructure")
    if tuple(agent.agent_id for agent in source_agents) != structure.source_agent_order:
        raise ValueError("source agents must equal the declared source agent order")
    agents_by_id = {agent.agent_id: agent for agent in source_agents}
    for spec in structure.agent_specs:
        expected = canonical_agent_assignment_labels(tuple(agents_by_id[agent_id] for agent_id in spec.source_agent_ids))
        if spec.block_channel.source_labels != expected:
            raise ValueError("block channel source labels must equal declared source-agent support")


@dataclass(frozen=True)
class PushedCoarseJoint:
    context_id: str
    latent_labels: tuple[str, ...]
    fine_observation_labels: tuple[str, ...]
    joint_masses: tuple[tuple[Fraction, ...], ...]
    combined_channel_sha256: str

    def __post_init__(self) -> None:
        _require_identifier(self.context_id, field="context ID")
        _require_labels(self.latent_labels, field="coarse latent labels")
        _require_labels(self.fine_observation_labels, field="fine observation labels")
        _require_exact_joint_matrix(self.joint_masses, len(self.latent_labels), len(self.fine_observation_labels), field="pushed coarse joint")
        _require_sha256(self.combined_channel_sha256, field="combined channel SHA-256")


@dataclass(frozen=True)
class CoarseGenerativeDatum:
    spec: CoarseAgentSpec
    agent: AgentDatum
    source_population_sha256: str
    block_channel_sha256: str
    combined_channel_sha256: str

    def __post_init__(self) -> None:
        if not isinstance(self.spec, CoarseAgentSpec) or not isinstance(self.agent, AgentDatum):
            raise TypeError("coarse generative datum requires a spec and AgentDatum")
        if self.agent.agent_id != self.spec.agent_id or self.agent.state_labels != self.spec.state_labels:
            raise ValueError("coarse generative agent must equal its declared spec")
        for value, field in (
            (self.source_population_sha256, "source population SHA-256"),
            (self.block_channel_sha256, "block channel SHA-256"),
            (self.combined_channel_sha256, "combined channel SHA-256"),
        ):
            _require_sha256(value, field=field)


@dataclass(frozen=True)
class CoarseAccessSpec:
    agent_id: str
    observation_labels: tuple[str, ...]
    information_labels: tuple[str, ...]
    information_by_observation: tuple[str, ...]
    access_kind: Literal["identity_observation"]

    def __post_init__(self) -> None:
        _require_identifier(self.agent_id, field="coarse access agent ID")
        _require_labels(self.observation_labels, field="access observation labels")
        _require_labels(self.information_labels, field="access information labels")
        if self.access_kind != "identity_observation":
            raise ValueError("access kind must be 'identity_observation'")
        if (
            self.information_labels != self.observation_labels
            or self.information_by_observation != self.observation_labels
        ):
            raise ValueError("identity access must preserve every observation label")


@dataclass(frozen=True)
class CoarseRecognitionDatum:
    agent: AgentDatum
    initial_recognition: AgentRecognitionDatum
    recognition_kernel: ExactMarkovChannel
    source_recognition_sha256: str

    def __post_init__(self) -> None:
        if not isinstance(self.agent, AgentDatum) or not isinstance(self.initial_recognition, AgentRecognitionDatum):
            raise TypeError("coarse recognition requires an AgentDatum and AgentRecognitionDatum")
        if self.initial_recognition.agent_id != self.agent.agent_id:
            raise ValueError("initial recognition must belong to the coarse agent")
        if (
            self.initial_recognition.belief_labels != self.agent.belief_labels
            or self.initial_recognition.model_labels != self.agent.model_labels
            or self.initial_recognition.state_labels != self.agent.state_labels
        ):
            raise ValueError("initial recognition supports must equal coarse agent supports")
        if not isinstance(self.recognition_kernel, ExactMarkovChannel):
            raise TypeError("recognition kernel must be an ExactMarkovChannel")
        if self.recognition_kernel.target_labels != self.agent.state_labels:
            raise ValueError("recognition kernel target labels must equal agent state labels")
        _require_sha256(self.source_recognition_sha256, field="source recognition SHA-256")


@dataclass(frozen=True)
class CoarseUpdateDatum:
    agent_id: str
    update_kind: Literal["exact_bayes_marginal"]
    kernel: ExactMarkovChannel
    source_population_sha256: str
    access_sha256: str

    def __post_init__(self) -> None:
        _require_identifier(self.agent_id, field="coarse update agent ID")
        if self.update_kind != "exact_bayes_marginal":
            raise ValueError("update kind must be 'exact_bayes_marginal'")
        if not isinstance(self.kernel, ExactMarkovChannel):
            raise TypeError("update kernel must be an ExactMarkovChannel")
        _require_sha256(self.source_population_sha256, field="source population SHA-256")
        _require_sha256(self.access_sha256, field="access SHA-256")


@dataclass(frozen=True)
class CoarseInformationDatum:
    access: CoarseAccessSpec
    update: CoarseUpdateDatum

    def __post_init__(self) -> None:
        if not isinstance(self.access, CoarseAccessSpec) or not isinstance(self.update, CoarseUpdateDatum):
            raise TypeError("coarse information requires access and update contracts")
        if self.access.agent_id != self.update.agent_id:
            raise ValueError("access and update agent IDs must agree")
        if self.update.kernel.source_labels != self.access.information_labels:
            raise ValueError("update kernel source labels must equal access information labels")


@dataclass(frozen=True)
class CoarseAgentDatum:
    generative: CoarseGenerativeDatum
    information: CoarseInformationDatum
    recognition: CoarseRecognitionDatum

    def __post_init__(self) -> None:
        if not isinstance(self.generative, CoarseGenerativeDatum) or not isinstance(self.information, CoarseInformationDatum) or not isinstance(self.recognition, CoarseRecognitionDatum):
            raise TypeError("coarse agent datum requires generative, information, and recognition contracts")
        agent_id = self.generative.agent.agent_id
        if self.information.access.agent_id != agent_id or self.recognition.agent.agent_id != agent_id:
            raise ValueError("coarse agent datum components must use one agent ID")


@dataclass(frozen=True)
class CoarsePopulationDatum:
    structure: RecursiveCoarseStructure
    combined_channel: CoarseChannelSpec
    generative_agents: tuple[CoarseGenerativeDatum, ...]
    records: tuple[RecordDatum, ...]
    pushed_joint: PushedCoarseJoint
    reconstructed_population: PopulationJoint

    def __post_init__(self) -> None:
        if not isinstance(self.structure, RecursiveCoarseStructure) or not isinstance(self.combined_channel, CoarseChannelSpec):
            raise TypeError("coarse population requires structure and combined channel contracts")
        if not isinstance(self.generative_agents, tuple) or any(not isinstance(item, CoarseGenerativeDatum) for item in self.generative_agents):
            raise TypeError("generative agents must be CoarseGenerativeDatum values")
        if tuple(item.agent.agent_id for item in self.generative_agents) != self.structure.coarse_agent_order:
            raise ValueError("generative agents must equal the coarse agent order")
        if not isinstance(self.records, tuple) or any(not isinstance(record, RecordDatum) for record in self.records):
            raise TypeError("records must be RecordDatum values")
        if not isinstance(self.pushed_joint, PushedCoarseJoint) or not isinstance(self.reconstructed_population, PopulationJoint):
            raise TypeError("coarse population requires pushed and reconstructed population contracts")


@dataclass(frozen=True)
class RecursiveObservationDatum:
    fine_observed_record: str
    coarse_observed_record: str
    fine_inference: PopulationInference
    coarse_inference: PopulationInference
    pushed_recognition: ExactProbabilityLaw
    pushed_posterior: ExactProbabilityLaw
    coarse_agents: tuple[CoarseAgentDatum, ...]

    def __post_init__(self) -> None:
        _require_identifier(self.fine_observed_record, field="fine observed record")
        _require_identifier(self.coarse_observed_record, field="coarse observed record")
        if not isinstance(self.fine_inference, PopulationInference) or not isinstance(self.coarse_inference, PopulationInference):
            raise TypeError("recursive observation requires fine and coarse inference contracts")
        if not isinstance(self.pushed_recognition, ExactProbabilityLaw) or not isinstance(self.pushed_posterior, ExactProbabilityLaw):
            raise TypeError("pushed recognition and posterior must be exact probability laws")
        if not isinstance(self.coarse_agents, tuple) or any(not isinstance(agent, CoarseAgentDatum) for agent in self.coarse_agents):
            raise TypeError("coarse agents must be CoarseAgentDatum values")


def _population_sha256(population: PopulationJoint) -> str:
    payload = {
        "agent_order": list(population.agent_order),
        "construction_trace": list(population.construction_trace),
        "context_id": population.context_id,
        "joint_masses": [
            [
                {"denominator": mass.denominator, "numerator": mass.numerator}
                for mass in row
            ]
            for row in population.joint_masses
        ],
        "latent_labels": list(population.latent_labels),
        "observation_labels": list(population.observation_labels),
        "record_order": list(population.record_order),
    }
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _build_combined_channel(
    population: PopulationJoint,
    structure: RecursiveCoarseStructure,
) -> CoarseChannelSpec:
    if len(structure.agent_specs) != 2:
        raise ValueError("recursive construction requires exactly two coarse agents")
    if population.agent_order != structure.source_agent_order:
        raise ValueError("population agent order must equal the declared source agent order")
    if any(spec.source_context_id != population.context_id for spec in structure.agent_specs):
        raise ValueError("coarse source context must equal the population context")

    local_supports: dict[str, list[str]] = {agent_id: [] for agent_id in population.agent_order}
    for latent_label in population.latent_labels:
        try:
            assignment = json.loads(latent_label)
        except json.JSONDecodeError as error:
            raise ValueError("population latent labels must be canonical ordered assignments") from error
        if _canonical_json(assignment) != latent_label or [entry[0] for entry in assignment] != list(population.agent_order):
            raise ValueError("population latent labels must be canonical ordered assignments")
        for entry in assignment:
            local_label = _canonical_json(entry[1:])
            if local_label not in local_supports[entry[0]]:
                local_supports[entry[0]].append(local_label)

    support_agents: list[AgentDatum] = []
    for agent_id in population.agent_order:
        state_labels = tuple(local_supports[agent_id])
        decoded = tuple(_parse_local_state(label, field="population local state") for label in state_labels)
        belief_labels = tuple(dict.fromkeys(belief for belief, _ in decoded))
        model_labels = tuple(dict.fromkeys(model for _, model in decoded))
        if state_labels != canonical_local_state_labels(belief_labels, model_labels):
            raise ValueError("population local states must form a canonical Cartesian support")
        generative_row = tuple(Fraction(1, len(state_labels)) for _ in state_labels)
        evaluator = tuple(
            ModelEvaluation(
                model_label,
                ExactMarkovChannel(
                    ("()",),
                    belief_labels,
                    (tuple(Fraction(1, len(belief_labels)) for _ in belief_labels),),
                    recognition_independent=True,
                ),
            )
            for model_label in model_labels
        )
        support_agents.append(
            AgentDatum(
                agent_id,
                (),
                belief_labels,
                model_labels,
                state_labels,
                evaluator,
                ExactMarkovChannel(("()",), state_labels, (generative_row,), recognition_independent=True),
            )
        )
    validate_coarse_structure_source_supports(structure, tuple(support_agents))

    target_labels = tuple(
        _canonical_json(
            [
                [spec.agent_id, *_parse_local_state(state_label, field="coarse state")]
                for spec, state_label in zip(structure.agent_specs, states, strict=True)
            ]
        )
        for states in product(*(spec.state_labels for spec in structure.agent_specs))
    )
    rows: list[tuple[Fraction, ...]] = []
    for fine_label in population.latent_labels:
        fine_assignment = {entry[0]: entry[1:] for entry in json.loads(fine_label)}
        source_indices = []
        for spec in structure.agent_specs:
            source_label = _canonical_json([[agent_id, *fine_assignment[agent_id]] for agent_id in spec.source_agent_ids])
            source_indices.append(spec.block_channel.source_labels.index(source_label))
        row: list[Fraction] = []
        for coarse_label in target_labels:
            coarse_assignment = {entry[0]: _canonical_json(entry[1:]) for entry in json.loads(coarse_label)}
            mass = Fraction(1)
            for spec, source_index in zip(structure.agent_specs, source_indices, strict=True):
                target_index = spec.block_channel.target_labels.index(coarse_assignment[spec.agent_id])
                mass *= spec.block_channel.matrix[source_index][target_index]
            row.append(mass)
        rows.append(tuple(row))
    channel = ExactMarkovChannel(
        population.latent_labels,
        target_labels,
        tuple(rows),
        recognition_independent=True,
    )
    return CoarseChannelSpec(
        f"{structure.structure_id}:combined",
        structure.source_agent_order,
        (structure.structure_id,) + tuple(f"block:{spec.agent_id}" for spec in structure.agent_specs),
        channel,
    )


def _push_population_joint(
    population: PopulationJoint,
    combined_channel: CoarseChannelSpec,
) -> PushedCoarseJoint:
    channel = combined_channel.channel
    if channel.source_labels != population.latent_labels:
        raise ValueError("combined channel source support must equal the population latent support")
    rows = tuple(
        tuple(
            sum(
                (
                    population.joint_masses[source_index][observation_index]
                    * channel.matrix[source_index][target_index]
                    for source_index in range(len(channel.source_labels))
                ),
                Fraction(0),
            )
            for observation_index in range(len(population.observation_labels))
        )
        for target_index in range(len(channel.target_labels))
    )
    return PushedCoarseJoint(
        population.context_id,
        channel.target_labels,
        population.observation_labels,
        rows,
        channel_sha256(channel),
    )


def _derive_evaluator(
    spec: CoarseAgentSpec,
    source_labels: tuple[str, ...],
    generative_rows: tuple[tuple[Fraction, ...], ...],
) -> tuple[ModelEvaluation, ...]:
    model_count = len(spec.model_labels)
    evaluators: list[ModelEvaluation] = []
    for model_index, model_label in enumerate(spec.model_labels):
        rows: list[tuple[Fraction, ...]] = []
        for generative_row in generative_rows:
            indices = tuple(belief_index * model_count + model_index for belief_index in range(len(spec.belief_labels)))
            denominator = sum((generative_row[index] for index in indices), Fraction(0))
            if denominator == 0:
                raise ValueError("null row policy forbids zero positive-model-slice denominator")
            rows.append(tuple(generative_row[index] / denominator for index in indices))
        evaluators.append(
            ModelEvaluation(
                model_label,
                ExactMarkovChannel(source_labels, spec.belief_labels, tuple(rows), recognition_independent=True),
            )
        )
    return tuple(evaluators)


def _derive_coarse_agents(
    pushed: PushedCoarseJoint,
    structure: RecursiveCoarseStructure,
    source_population_sha256: str,
    combined_channel_sha256: str,
) -> tuple[CoarseGenerativeDatum, ...]:
    spec_a, spec_b = structure.agent_specs
    latent_masses = tuple(sum(row, Fraction(0)) for row in pushed.joint_masses)
    joint_indices: list[tuple[int, int]] = []
    for label in pushed.latent_labels:
        assignment = json.loads(label)
        if tuple(entry[0] for entry in assignment) != structure.coarse_agent_order:
            raise ValueError("pushed coarse latent support must use coarse agent order")
        joint_indices.append(
            (
                spec_a.state_labels.index(_canonical_json(assignment[0][1:])),
                spec_b.state_labels.index(_canonical_json(assignment[1][1:])),
            )
        )
    marginal_a = [Fraction(0) for _ in spec_a.state_labels]
    for mass, (a_index, _) in zip(latent_masses, joint_indices, strict=True):
        marginal_a[a_index] += mass
    if any(mass == 0 for mass in marginal_a):
        raise ValueError("null row policy forbids zero parent denominator")
    rows_a = (tuple(marginal_a),)
    agent_a = AgentDatum(
        spec_a.agent_id,
        spec_a.parent_ids,
        spec_a.belief_labels,
        spec_a.model_labels,
        spec_a.state_labels,
        _derive_evaluator(spec_a, ("()",), rows_a),
        ExactMarkovChannel(("()",), spec_a.state_labels, rows_a, recognition_independent=True),
    )
    source_b = canonical_agent_assignment_labels((agent_a,))
    rows_b: list[tuple[Fraction, ...]] = []
    for a_index, denominator in enumerate(marginal_a):
        row = [Fraction(0) for _ in spec_b.state_labels]
        for mass, (candidate_a, b_index) in zip(latent_masses, joint_indices, strict=True):
            if candidate_a == a_index:
                row[b_index] += mass / denominator
        rows_b.append(tuple(row))
    exact_rows_b = tuple(rows_b)
    agent_b = AgentDatum(
        spec_b.agent_id,
        spec_b.parent_ids,
        spec_b.belief_labels,
        spec_b.model_labels,
        spec_b.state_labels,
        _derive_evaluator(spec_b, source_b, exact_rows_b),
        ExactMarkovChannel(source_b, spec_b.state_labels, exact_rows_b, recognition_independent=True),
    )
    return (
        CoarseGenerativeDatum(spec_a, agent_a, source_population_sha256, channel_sha256(spec_a.block_channel), combined_channel_sha256),
        CoarseGenerativeDatum(spec_b, agent_b, source_population_sha256, channel_sha256(spec_b.block_channel), combined_channel_sha256),
    )


def _build_combined_record(
    pushed: PushedCoarseJoint,
    structure: RecursiveCoarseStructure,
) -> RecordDatum:
    observation = structure.observation
    if observation.fine_observation_labels != pushed.fine_observation_labels:
        raise ValueError("fine observation support must equal the declared observation support")
    outcome_indices = tuple(
        observation.compound_outcome_labels.index(outcome)
        for outcome in observation.compound_outcome_by_fine_observation
    )
    rows: list[tuple[Fraction, ...]] = []
    for pushed_row in pushed.joint_masses:
        denominator = sum(pushed_row, Fraction(0))
        if denominator == 0:
            raise ValueError("null row policy forbids zero pushed latent denominator")
        row = [Fraction(0) for _ in observation.compound_outcome_labels]
        for fine_index, outcome_index in enumerate(outcome_indices):
            row[outcome_index] += pushed_row[fine_index] / denominator
        rows.append(tuple(row))
    return RecordDatum(
        observation.record_id,
        structure.coarse_agent_order[-1],
        structure.coarse_agent_order,
        observation.compound_outcome_labels,
        ExactMarkovChannel(pushed.latent_labels, observation.compound_outcome_labels, tuple(rows), recognition_independent=True),
    )


def _relabel_reconstructed_joint(
    reconstructed: PopulationJoint,
    observation: CoarseObservationSpec,
) -> tuple[tuple[Fraction, ...], ...]:
    columns = tuple(
        reconstructed.observation_labels.index(_canonical_json([[observation.record_id, outcome]]))
        for outcome in observation.compound_outcome_by_fine_observation
    )
    return tuple(tuple(row[column] for column in columns) for row in reconstructed.joint_masses)


def _validate_coarse_population_datum(datum: CoarsePopulationDatum) -> None:
    structure = datum.structure
    declared_sources = tuple(agent_id for spec in structure.agent_specs for agent_id in spec.source_agent_ids)
    if declared_sources != structure.source_agent_order:
        raise ValueError("source blocks must be disjoint and exhaustive")
    validated_specs = tuple(
        CoarseAgentSpec(
            spec.agent_id,
            spec.source_agent_ids,
            spec.parent_ids,
            spec.source_context_id,
            spec.belief_labels,
            spec.model_labels,
            spec.state_labels,
            spec.block_channel,
            spec.null_row_policy,
        )
        for spec in structure.agent_specs
    )
    validated_observation = CoarseObservationSpec(
        structure.observation.record_id,
        structure.observation.fine_observation_labels,
        structure.observation.compound_outcome_labels,
        structure.observation.compound_outcome_by_fine_observation,
    )
    validated_sparse = SparseRecordFactorizationSpec(
        structure.sparse_record_candidate.left_record_ids,
        structure.sparse_record_candidate.right_record_ids,
        structure.sparse_record_candidate.left_outcome_labels,
        structure.sparse_record_candidate.right_outcome_labels,
        structure.sparse_record_candidate.left_outcome_by_fine_observation,
        structure.sparse_record_candidate.right_outcome_by_fine_observation,
    )
    RecursiveCoarseStructure(
        structure.structure_id,
        structure.source_agent_order,
        structure.coarse_agent_order,
        validated_specs,
        validated_observation,
        validated_sparse,
    )
    if datum.combined_channel.source_agent_ids != structure.source_agent_order:
        raise ValueError("combined channel source agents must equal the declared source order")
    if datum.combined_channel.channel.target_labels != datum.pushed_joint.latent_labels:
        raise ValueError("combined channel target labels must equal the pushed latent labels")
    for spec in validated_specs:
        expected_sources: list[str] = []
        for fine_label in datum.combined_channel.channel.source_labels:
            assignment = {entry[0]: entry[1:] for entry in json.loads(fine_label)}
            label = _canonical_json([[agent_id, *assignment[agent_id]] for agent_id in spec.source_agent_ids])
            if label not in expected_sources:
                expected_sources.append(label)
        if spec.block_channel.source_labels != tuple(expected_sources):
            raise ValueError("block channel source labels must equal declared source-agent support")
    if tuple(item.agent.agent_id for item in datum.generative_agents) != structure.coarse_agent_order:
        raise ValueError("generative agents must equal the coarse agent order")
    if len(datum.records) != 1 or datum.records[0].owner_id != structure.coarse_agent_order[-1] or datum.records[0].scope_ids != structure.coarse_agent_order:
        raise ValueError("combined record must be owned once by the final coarse agent over both parents")
    reconstructed = construct_population_joint(
        tuple(item.agent for item in datum.generative_agents),
        datum.records,
        datum.pushed_joint.context_id,
    )
    if reconstructed != datum.reconstructed_population:
        raise ValueError("coarse generative roundtrip does not equal its declared factors")
    if reconstructed.latent_labels != datum.pushed_joint.latent_labels:
        raise ValueError("reconstructed and pushed latent supports must agree")
    if _relabel_reconstructed_joint(reconstructed, validated_observation) != datum.pushed_joint.joint_masses:
        raise ValueError("coarse generative roundtrip does not match the pushed joint")


def construct_coarse_population_joint(
    population: PopulationJoint,
    structure: RecursiveCoarseStructure,
) -> CoarsePopulationDatum:
    """Construct the exact two-parent coarse generative population."""
    if not isinstance(population, PopulationJoint):
        raise ValueError(
            "generative construction requires PopulationJoint; aggregate-only input lacks structural, generative, observation, recognition, and update obligations"
        )
    if not isinstance(structure, RecursiveCoarseStructure):
        raise TypeError("structure must be a RecursiveCoarseStructure")
    combined = _build_combined_channel(population, structure)
    pushed = _push_population_joint(population, combined)
    population_hash = _population_sha256(population)
    agents = _derive_coarse_agents(pushed, structure, population_hash, pushed.combined_channel_sha256)
    record = _build_combined_record(pushed, structure)
    reconstructed = construct_population_joint(
        tuple(item.agent for item in agents),
        (record,),
        population.context_id,
    )
    datum = CoarsePopulationDatum(structure, combined, agents, (record,), pushed, reconstructed)
    _validate_coarse_population_datum(datum)
    return datum


def _enumerate_coarse_population_independently(
    population: PopulationJoint,
    structure: RecursiveCoarseStructure,
) -> CoarsePopulationDatum:
    """Independently reconstruct the complete coarse generative arrow."""
    if not isinstance(population, PopulationJoint) or not isinstance(structure, RecursiveCoarseStructure):
        raise TypeError("independent coarse oracle requires PopulationJoint and RecursiveCoarseStructure")
    if len(structure.agent_specs) != 2 or population.agent_order != structure.source_agent_order:
        raise ValueError("independent coarse oracle requires the declared two-block source order")
    spec_a, spec_b = structure.agent_specs
    decoded_fine: list[list[list[str]]] = []
    for label in population.latent_labels:
        assignment = json.loads(label)
        if json.dumps(assignment, ensure_ascii=True, separators=(",", ":")) != label:
            raise ValueError("independent coarse oracle requires canonical fine labels")
        decoded_fine.append(assignment)
    for spec in structure.agent_specs:
        seen: list[str] = []
        for assignment in decoded_fine:
            by_id = {entry[0]: entry[1:] for entry in assignment}
            label = json.dumps([[agent_id, *by_id[agent_id]] for agent_id in spec.source_agent_ids], ensure_ascii=True, separators=(",", ":"))
            if label not in seen:
                seen.append(label)
        if tuple(seen) != spec.block_channel.source_labels or spec.block_channel.target_labels != spec.state_labels:
            raise ValueError("independent coarse oracle found incompatible block-channel support")
    coarse_labels = tuple(
        json.dumps(
            [[spec_a.agent_id, *json.loads(state_a)], [spec_b.agent_id, *json.loads(state_b)]],
            ensure_ascii=True,
            separators=(",", ":"),
        )
        for state_a, state_b in product(spec_a.state_labels, spec_b.state_labels)
    )
    combined_rows: list[tuple[Fraction, ...]] = []
    for assignment in decoded_fine:
        by_id = {entry[0]: entry[1:] for entry in assignment}
        source_a = json.dumps([[agent_id, *by_id[agent_id]] for agent_id in spec_a.source_agent_ids], ensure_ascii=True, separators=(",", ":"))
        source_b = json.dumps([[agent_id, *by_id[agent_id]] for agent_id in spec_b.source_agent_ids], ensure_ascii=True, separators=(",", ":"))
        row_a = spec_a.block_channel.matrix[spec_a.block_channel.source_labels.index(source_a)]
        row_b = spec_b.block_channel.matrix[spec_b.block_channel.source_labels.index(source_b)]
        combined_rows.append(tuple(row_a[a_index] * row_b[b_index] for a_index, b_index in product(range(4), repeat=2)))
    combined_exact_rows = tuple(combined_rows)
    combined_exact = ExactMarkovChannel(population.latent_labels, coarse_labels, combined_exact_rows, recognition_independent=True)
    channel_payload = {
        "matrix": [[{"denominator": mass.denominator, "numerator": mass.numerator} for mass in row] for row in combined_exact.matrix],
        "recognition_independent": True,
        "source_labels": list(combined_exact.source_labels),
        "target_labels": list(combined_exact.target_labels),
    }
    combined_hash = hashlib.sha256(json.dumps(channel_payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True, allow_nan=False).encode("utf-8")).hexdigest()
    pushed_rows = tuple(
        tuple(
            sum((population.joint_masses[source][observation] * combined_exact_rows[source][target] for source in range(len(population.latent_labels))), Fraction(0))
            for observation in range(len(population.observation_labels))
        )
        for target in range(len(coarse_labels))
    )
    pushed = PushedCoarseJoint(population.context_id, coarse_labels, population.observation_labels, pushed_rows, combined_hash)
    latent_masses = tuple(sum(row, Fraction(0)) for row in pushed_rows)
    marginal_a = tuple(sum((latent_masses[a_index * 4 + b_index] for b_index in range(4)), Fraction(0)) for a_index in range(4))
    if any(value == 0 for value in marginal_a):
        raise ValueError("independent coarse oracle forbids null parent rows")
    rows_a = (marginal_a,)

    def oracle_evaluator(spec: CoarseAgentSpec, sources: tuple[str, ...], rows: tuple[tuple[Fraction, ...], ...]) -> tuple[ModelEvaluation, ...]:
        result: list[ModelEvaluation] = []
        for model_index, model_label in enumerate(spec.model_labels):
            evaluator_rows = []
            for row in rows:
                indices = tuple(belief_index * len(spec.model_labels) + model_index for belief_index in range(len(spec.belief_labels)))
                denominator = sum((row[index] for index in indices), Fraction(0))
                if denominator == 0:
                    raise ValueError("independent coarse oracle forbids null evaluator rows")
                evaluator_rows.append(tuple(row[index] / denominator for index in indices))
            result.append(ModelEvaluation(model_label, ExactMarkovChannel(sources, spec.belief_labels, tuple(evaluator_rows), recognition_independent=True)))
        return tuple(result)

    agent_a = AgentDatum(spec_a.agent_id, spec_a.parent_ids, spec_a.belief_labels, spec_a.model_labels, spec_a.state_labels, oracle_evaluator(spec_a, ("()",), rows_a), ExactMarkovChannel(("()",), spec_a.state_labels, rows_a, recognition_independent=True))
    sources_b = tuple(json.dumps([[spec_a.agent_id, *json.loads(label)]], ensure_ascii=True, separators=(",", ":")) for label in spec_a.state_labels)
    rows_b = tuple(tuple(latent_masses[a_index * 4 + b_index] / marginal_a[a_index] for b_index in range(4)) for a_index in range(4))
    agent_b = AgentDatum(spec_b.agent_id, spec_b.parent_ids, spec_b.belief_labels, spec_b.model_labels, spec_b.state_labels, oracle_evaluator(spec_b, sources_b, rows_b), ExactMarkovChannel(sources_b, spec_b.state_labels, rows_b, recognition_independent=True))
    observation = structure.observation
    if observation.fine_observation_labels != population.observation_labels:
        raise ValueError("independent coarse oracle found incompatible observation support")
    outcome_indices = tuple(observation.compound_outcome_labels.index(value) for value in observation.compound_outcome_by_fine_observation)
    record_rows: list[tuple[Fraction, ...]] = []
    for row, denominator in zip(pushed_rows, latent_masses, strict=True):
        if denominator == 0:
            raise ValueError("independent coarse oracle forbids null record rows")
        record_row = [Fraction(0) for _ in observation.compound_outcome_labels]
        for fine_index, outcome_index in enumerate(outcome_indices):
            record_row[outcome_index] += row[fine_index] / denominator
        record_rows.append(tuple(record_row))
    record = RecordDatum(observation.record_id, spec_b.agent_id, (spec_a.agent_id, spec_b.agent_id), observation.compound_outcome_labels, ExactMarkovChannel(coarse_labels, observation.compound_outcome_labels, tuple(record_rows), recognition_independent=True))
    reconstructed_observations = tuple(json.dumps([[observation.record_id, outcome]], ensure_ascii=True, separators=(",", ":")) for outcome in observation.compound_outcome_labels)
    reconstructed_rows: list[tuple[Fraction, ...]] = []
    for latent_index, (a_index, b_index) in enumerate(product(range(4), repeat=2)):
        generative_mass = rows_a[0][a_index] * rows_b[a_index][b_index]
        reconstructed_rows.append(tuple(generative_mass * record_rows[latent_index][outcome_index] for outcome_index in range(16)))
    exact_reconstructed_rows = tuple(reconstructed_rows)
    if sum((sum(row, Fraction(0)) for row in exact_reconstructed_rows), Fraction(0)) != 1:
        raise ArithmeticError("independent coarse reconstruction is not normalized")
    reconstructed = PopulationJoint(population.context_id, (spec_a.agent_id, spec_b.agent_id), (observation.record_id,), coarse_labels, reconstructed_observations, exact_reconstructed_rows, (f"agent:{spec_a.agent_id}", f"agent:{spec_b.agent_id}", f"record:{observation.record_id}"))
    relabeled = tuple(tuple(row[outcome_indices[fine_index]] for fine_index in range(16)) for row in exact_reconstructed_rows)
    if relabeled != pushed_rows:
        raise ValueError("independent coarse reconstruction does not roundtrip")
    population_payload = {
        "agent_order": list(population.agent_order), "construction_trace": list(population.construction_trace), "context_id": population.context_id,
        "joint_masses": [[{"denominator": mass.denominator, "numerator": mass.numerator} for mass in row] for row in population.joint_masses],
        "latent_labels": list(population.latent_labels), "observation_labels": list(population.observation_labels), "record_order": list(population.record_order),
    }
    population_hash = hashlib.sha256(json.dumps(population_payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True, allow_nan=False).encode("utf-8")).hexdigest()
    agents = (
        CoarseGenerativeDatum(spec_a, agent_a, population_hash, channel_sha256(spec_a.block_channel), combined_hash),
        CoarseGenerativeDatum(spec_b, agent_b, population_hash, channel_sha256(spec_b.block_channel), combined_hash),
    )
    combined = CoarseChannelSpec(f"{structure.structure_id}:combined", structure.source_agent_order, (structure.structure_id, f"block:{spec_a.agent_id}", f"block:{spec_b.agent_id}"), combined_exact)
    return CoarsePopulationDatum(structure, combined, agents, (record,), pushed, reconstructed)


def _sparse_record_factorization_diagnostics(
    coarse_population: CoarsePopulationDatum,
) -> tuple[int, Fraction]:
    """Return exact failed sparse identities and maximum conditional TV."""
    if not isinstance(coarse_population, CoarsePopulationDatum):
        raise TypeError("coarse_population must be a CoarsePopulationDatum")
    sparse = coarse_population.structure.sparse_record_candidate
    pushed = coarse_population.pushed_joint
    left_indices = tuple(sparse.left_outcome_labels.index(value) for value in sparse.left_outcome_by_fine_observation)
    right_indices = tuple(sparse.right_outcome_labels.index(value) for value in sparse.right_outcome_by_fine_observation)
    conditional: list[tuple[tuple[Fraction, ...], ...]] = []
    left_marginals: list[tuple[Fraction, ...]] = []
    right_marginals: list[tuple[Fraction, ...]] = []
    for pushed_row in pushed.joint_masses:
        denominator = sum(pushed_row, Fraction(0))
        if denominator == 0:
            raise ValueError("sparse diagnostics require positive coarse latent mass")
        joint = [[Fraction(0) for _ in sparse.right_outcome_labels] for _ in sparse.left_outcome_labels]
        for fine_index, mass in enumerate(pushed_row):
            joint[left_indices[fine_index]][right_indices[fine_index]] += mass / denominator
        exact_joint = tuple(tuple(row) for row in joint)
        conditional.append(exact_joint)
        left_marginals.append(tuple(sum(row, Fraction(0)) for row in exact_joint))
        right_marginals.append(tuple(sum((exact_joint[left][right] for left in range(len(exact_joint))), Fraction(0)) for right in range(len(exact_joint[0]))))
    violations = 0
    for a_index in range(4):
        for left_b, right_b in __import__("itertools").combinations(range(4), 2):
            for outcome in range(4):
                violations += int(left_marginals[a_index * 4 + left_b][outcome] != left_marginals[a_index * 4 + right_b][outcome])
    for b_index in range(4):
        for left_a, right_a in __import__("itertools").combinations(range(4), 2):
            for outcome in range(4):
                violations += int(right_marginals[left_a * 4 + b_index][outcome] != right_marginals[right_a * 4 + b_index][outcome])
    maximum_tv = Fraction(0)
    for latent_index, joint in enumerate(conditional):
        tv = Fraction(0)
        for left in range(4):
            for right in range(4):
                product_mass = left_marginals[latent_index][left] * right_marginals[latent_index][right]
                difference = joint[left][right] - product_mass
                violations += int(difference != 0)
                tv += abs(difference)
        maximum_tv = max(maximum_tv, tv / 2)
    return violations, maximum_tv


def _probability_sha256(law: ExactProbabilityLaw) -> str:
    payload = {
        "labels": list(law.labels),
        "masses": [
            {"denominator": mass.denominator, "numerator": mass.numerator}
            for mass in law.masses
        ],
    }
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _access_sha256(access: CoarseAccessSpec) -> str:
    payload = {
        "access_kind": access.access_kind,
        "agent_id": access.agent_id,
        "information_by_observation": list(access.information_by_observation),
        "information_labels": list(access.information_labels),
        "observation_labels": list(access.observation_labels),
    }
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _marginalize_coarse_law(
    law: ExactProbabilityLaw,
    agent: AgentDatum,
) -> ExactProbabilityLaw:
    masses = [Fraction(0) for _ in agent.state_labels]
    for latent_label, mass in zip(law.labels, law.masses, strict=True):
        assignment = json.loads(latent_label)
        entries = tuple(entry for entry in assignment if entry[0] == agent.agent_id)
        if len(entries) != 1:
            raise ValueError("coarse law must contain each coarse agent exactly once")
        state_label = _canonical_json(entries[0][1:])
        if state_label not in agent.state_labels:
            raise ValueError("coarse law local support must equal the coarse agent support")
        masses[agent.state_labels.index(state_label)] += mass
    return ExactProbabilityLaw(agent.state_labels, tuple(masses))


def _posterior_for_observation(
    population: PopulationJoint,
    observation_label: str,
) -> ExactProbabilityLaw:
    if observation_label not in population.observation_labels:
        raise ValueError("posterior observation must belong to the reconstructed population")
    column = population.observation_labels.index(observation_label)
    evidence = sum((row[column] for row in population.joint_masses), Fraction(0))
    if evidence <= 0:
        raise ValueError("coarse update table requires positive evidence for every observation")
    return ExactProbabilityLaw(
        population.latent_labels,
        tuple(row[column] / evidence for row in population.joint_masses),
    )


def _total_variation(
    left: tuple[Fraction, ...],
    right: tuple[Fraction, ...],
) -> Fraction:
    if len(left) != len(right):
        raise ValueError("total variation requires equal finite supports")
    return sum((abs(left_mass - right_mass) for left_mass, right_mass in zip(left, right, strict=True)), Fraction(0)) / 2


def construct_coarse_information_interfaces(
    coarse_population: CoarsePopulationDatum,
    access_specs: tuple[CoarseAccessSpec, ...],
) -> tuple[CoarseInformationDatum, ...]:
    """Derive inference-free identity access and exact Bayes-update tables."""
    if not isinstance(coarse_population, CoarsePopulationDatum):
        raise TypeError("coarse_population must be a CoarsePopulationDatum")
    _validate_coarse_population_datum(coarse_population)
    if not isinstance(access_specs, tuple) or any(not isinstance(access, CoarseAccessSpec) for access in access_specs):
        raise TypeError("access_specs must contain only CoarseAccessSpec values")
    expected_order = coarse_population.structure.coarse_agent_order
    if tuple(access.agent_id for access in access_specs) != expected_order:
        raise ValueError("access specs must use the coarse agent order")

    population = coarse_population.reconstructed_population
    posteriors = tuple(
        _posterior_for_observation(population, observation_label)
        for observation_label in population.observation_labels
    )
    population_hash = _population_sha256(population)
    result: list[CoarseInformationDatum] = []
    for generative, access in zip(coarse_population.generative_agents, access_specs, strict=True):
        if access.observation_labels != population.observation_labels:
            raise ValueError("access observations must cover the reconstructed observation support in order")
        _require_labels(access.information_labels, field="access information labels")
        if (
            not isinstance(access.information_by_observation, tuple)
            or len(access.information_by_observation) != len(access.observation_labels)
            or any(label not in access.information_labels for label in access.information_by_observation)
        ):
            raise ValueError("access map must be total over reconstructed observations")
        observation_rows = tuple(
            _marginalize_coarse_law(posterior, generative.agent).masses
            for posterior in posteriors
        )
        equal_access_pairs = tuple(
            (left, right)
            for left, right in __import__("itertools").combinations(range(len(access.observation_labels)), 2)
            if access.information_by_observation[left] == access.information_by_observation[right]
        )
        max_tv = max(
            (_total_variation(observation_rows[left], observation_rows[right]) for left, right in equal_access_pairs),
            default=Fraction(0),
        )
        if max_tv != 0:
            raise ValueError(f"access descent residual must be zero exactly, got {max_tv}")
        if (
            access.access_kind != "identity_observation"
            or access.information_labels != access.observation_labels
            or access.information_by_observation != access.observation_labels
        ):
            raise ValueError("identity access must preserve every reconstructed observation label")
        rows_by_information = {
            information_label: observation_rows[access.observation_labels.index(information_label)]
            for information_label in access.information_labels
        }
        update_rows = tuple(rows_by_information[label] for label in access.information_labels)
        if len(set(update_rows)) < 2:
            raise ValueError("each coarse update table must contain at least two distinct rows")
        update = CoarseUpdateDatum(
            generative.agent.agent_id,
            "exact_bayes_marginal",
            ExactMarkovChannel(
                access.information_labels,
                generative.agent.state_labels,
                update_rows,
                recognition_independent=True,
            ),
            population_hash,
            _access_sha256(access),
        )
        result.append(CoarseInformationDatum(access, update))
    return tuple(result)


def _validate_information_order(
    coarse_population: CoarsePopulationDatum,
    information: tuple[CoarseInformationDatum, ...],
) -> None:
    if not isinstance(information, tuple) or any(not isinstance(item, CoarseInformationDatum) for item in information):
        raise TypeError("information must contain only CoarseInformationDatum values")
    expected_order = coarse_population.structure.coarse_agent_order
    if tuple(item.access.agent_id for item in information) != expected_order:
        raise ValueError("information order must equal the coarse agent order")
    for generative, item in zip(coarse_population.generative_agents, information, strict=True):
        if item.update.kernel.target_labels != generative.agent.state_labels:
            raise ValueError("information update target support must equal the coarse agent support")


def _validate_fine_inference_route(
    coarse_population: CoarsePopulationDatum,
    fine_inference: PopulationInference,
) -> ExactMarkovChannel:
    if not isinstance(fine_inference, PopulationInference):
        raise TypeError("fine_inference must be a PopulationInference")
    channel = coarse_population.combined_channel.channel
    if channel.source_labels != fine_inference.population.latent_labels:
        raise ValueError("combined channel source support must equal the fine inference support")
    if channel.target_labels != coarse_population.reconstructed_population.latent_labels:
        raise ValueError("combined channel target support must equal the coarse population support")
    fine_population_hash = _population_sha256(fine_inference.population)
    if any(item.source_population_sha256 != fine_population_hash for item in coarse_population.generative_agents):
        raise ValueError("fine inference population must equal the coarse generative source population")
    return channel


def construct_coarse_recognition(
    coarse_population: CoarsePopulationDatum,
    information: tuple[CoarseInformationDatum, ...],
    fine_inference: PopulationInference,
) -> tuple[CoarseAgentDatum, ...]:
    """Attach pushed local recognition laws after generative construction."""
    if not isinstance(coarse_population, CoarsePopulationDatum):
        raise TypeError("coarse_population must be a CoarsePopulationDatum")
    _validate_coarse_population_datum(coarse_population)
    _validate_information_order(coarse_population, information)
    channel = _validate_fine_inference_route(coarse_population, fine_inference)
    pushed = ExactProbabilityLaw(channel.target_labels, channel.pushforward(fine_inference.recognition.masses))
    recognition_hash = _probability_sha256(fine_inference.recognition)
    result: list[CoarseAgentDatum] = []
    for generative, interface in zip(coarse_population.generative_agents, information, strict=True):
        local_law = _marginalize_coarse_law(pushed, generative.agent)
        initial = AgentRecognitionDatum(generative.agent, local_law)
        recognition = CoarseRecognitionDatum(
            generative.agent,
            initial,
            ExactMarkovChannel(
                interface.access.information_labels,
                generative.agent.state_labels,
                tuple(local_law.masses for _ in interface.access.information_labels),
                recognition_independent=True,
            ),
            recognition_hash,
        )
        result.append(CoarseAgentDatum(generative, interface, recognition))
    return tuple(result)


def derive_recursive_observation(
    coarse_population: CoarsePopulationDatum,
    coarse_agents: tuple[CoarseAgentDatum, ...],
    fine_inference: PopulationInference,
) -> RecursiveObservationDatum:
    """Derive one paired observation through unchanged population inference."""
    if not isinstance(coarse_population, CoarsePopulationDatum):
        raise TypeError("coarse_population must be a CoarsePopulationDatum")
    if not isinstance(coarse_agents, tuple) or any(not isinstance(agent, CoarseAgentDatum) for agent in coarse_agents):
        raise TypeError("coarse_agents must contain only CoarseAgentDatum values")
    if tuple(agent.generative for agent in coarse_agents) != coarse_population.generative_agents:
        raise ValueError("coarse agents must use the completed coarse generative data in order")
    _validate_information_order(coarse_population, tuple(agent.information for agent in coarse_agents))
    channel = _validate_fine_inference_route(coarse_population, fine_inference)
    pushed_recognition = ExactProbabilityLaw(
        channel.target_labels,
        channel.pushforward(fine_inference.recognition.masses),
    )
    for agent in coarse_agents:
        expected_local = _marginalize_coarse_law(pushed_recognition, agent.generative.agent)
        if agent.recognition.initial_recognition.joint != expected_local:
            raise ValueError("coarse recognition marginal must equal the common-channel push")
    observation = coarse_population.structure.observation
    if fine_inference.observed_record not in observation.fine_observation_labels:
        raise ValueError("fine observed record must belong to the declared observation relabeling")
    fine_index = observation.fine_observation_labels.index(fine_inference.observed_record)
    outcome = observation.compound_outcome_by_fine_observation[fine_index]
    coarse_observed_record = _canonical_json([[observation.record_id, outcome]])
    selector = SelectorSpec(
        f"{coarse_population.structure.structure_id}:declared-correlated",
        "declared_correlated",
        pushed_recognition,
    )
    coarse_inference = derive_population_inference(
        coarse_population.reconstructed_population,
        ((observation.record_id, outcome),),
        tuple(agent.recognition.initial_recognition for agent in coarse_agents),
        selector,
    )
    pushed_posterior = ExactProbabilityLaw(
        channel.target_labels,
        channel.pushforward(fine_inference.posterior.masses),
    )
    return RecursiveObservationDatum(
        fine_inference.observed_record,
        coarse_observed_record,
        fine_inference,
        coarse_inference,
        pushed_recognition,
        pushed_posterior,
        coarse_agents,
    )


def validate_recursive_observation(
    datum: RecursiveObservationDatum,
    coarse_population: CoarsePopulationDatum,
    numerics: NumericsConfig,
) -> None:
    """Validate the exact common-channel recursive observation diagram."""
    if not isinstance(datum, RecursiveObservationDatum):
        raise TypeError("datum must be a RecursiveObservationDatum")
    if not isinstance(coarse_population, CoarsePopulationDatum):
        raise TypeError("coarse_population must be a CoarsePopulationDatum")
    if not isinstance(numerics, NumericsConfig):
        raise TypeError("numerics must be a NumericsConfig")
    if (
        numerics.dtype != "float64"
        or not math.isfinite(numerics.atol)
        or not math.isfinite(numerics.rtol)
        or numerics.atol < 0
        or numerics.rtol < 0
    ):
        raise ValueError("recursive validation requires finite nonnegative float64 numerics")
    _validate_coarse_population_datum(coarse_population)
    channel = _validate_fine_inference_route(coarse_population, datum.fine_inference)
    actual_channel_hash = channel_sha256(channel)
    expected_channel_hashes = (
        coarse_population.pushed_joint.combined_channel_sha256,
        *(item.combined_channel_sha256 for item in coarse_population.generative_agents),
    )
    if any(value != actual_channel_hash for value in expected_channel_hashes):
        raise ValueError("combined channel hash must agree at every recursive route")
    if datum.fine_observed_record != datum.fine_inference.observed_record:
        raise ValueError("fine observed record must equal the supplied fine inference")
    if datum.coarse_inference.population != coarse_population.reconstructed_population:
        raise ValueError("coarse inference population must equal the reconstructed population")
    if datum.coarse_inference.recognitions != tuple(agent.recognition.initial_recognition for agent in datum.coarse_agents):
        raise ValueError("coarse inference recognitions must equal the attached coarse recognition data")
    if tuple(agent.generative for agent in datum.coarse_agents) != coarse_population.generative_agents:
        raise ValueError("coarse agent generative data must equal the completed coarse population")
    _validate_information_order(coarse_population, tuple(agent.information for agent in datum.coarse_agents))

    observation = coarse_population.structure.observation
    if datum.fine_observed_record not in observation.fine_observation_labels:
        raise ValueError("fine observed record must belong to the observation relabeling")
    fine_index = observation.fine_observation_labels.index(datum.fine_observed_record)
    expected_outcome = observation.compound_outcome_by_fine_observation[fine_index]
    expected_coarse_record = _canonical_json([[observation.record_id, expected_outcome]])
    if datum.coarse_observed_record != expected_coarse_record or datum.coarse_inference.observed_record != expected_coarse_record:
        raise ValueError("observation relabeling must preserve the paired realized observation")

    try:
        fine_observations = tuple(
            (record_id, outcome)
            for record_id, outcome in json.loads(datum.fine_observed_record)
        )
        replayed_fine_inference = derive_population_inference(
            datum.fine_inference.population,
            fine_observations,
            datum.fine_inference.recognitions,
            datum.fine_inference.selector,
        )
    except (TypeError, ValueError) as error:
        raise ValueError("fine inference replay failed its retained semantic inputs") from error
    if replayed_fine_inference != datum.fine_inference:
        raise ValueError("fine inference replay must equal every stored inference field")

    selector = datum.coarse_inference.selector
    try:
        replayed_coarse_inference = derive_population_inference(
            coarse_population.reconstructed_population,
            ((observation.record_id, expected_outcome),),
            tuple(agent.recognition.initial_recognition for agent in datum.coarse_agents),
            selector,
        )
    except (TypeError, ValueError) as error:
        raise ValueError("coarse inference replay failed selector marginal validation") from error
    if replayed_coarse_inference != datum.coarse_inference:
        raise ValueError("coarse inference replay must equal every stored inference field")

    expected_recognition_hash = _probability_sha256(replayed_fine_inference.recognition)
    if any(
        agent.recognition.source_recognition_sha256 != expected_recognition_hash
        for agent in datum.coarse_agents
    ):
        raise ValueError("source recognition SHA-256 must equal the exact fine recognition law hash")

    expected_recognition = ExactProbabilityLaw(
        channel.target_labels,
        channel.pushforward(datum.fine_inference.recognition.masses),
    )
    expected_posterior = ExactProbabilityLaw(
        channel.target_labels,
        channel.pushforward(datum.fine_inference.posterior.masses),
    )
    if selector.selector_kind != "declared_correlated" or selector.coupling is None:
        raise ValueError("coarse selector must retain the declared correlated coupling")
    for agent in datum.coarse_agents:
        expected_local_recognition = _marginalize_coarse_law(selector.coupling, agent.generative.agent)
        if expected_local_recognition != agent.recognition.initial_recognition.joint:
            raise ValueError("selector marginal must equal each coarse local recognition law")
    if selector.coupling != expected_recognition:
        raise ValueError("coarse selector coupling must equal the pushed recognition law")
    if datum.pushed_recognition != expected_recognition or datum.coarse_inference.recognition != expected_recognition:
        raise ValueError("pushed and reconstructed recognition laws must agree exactly")
    if datum.coarse_inference.evidence != datum.fine_inference.evidence:
        raise ValueError("fine and coarse evidence must agree exactly")
    if datum.pushed_posterior != expected_posterior or datum.coarse_inference.posterior != expected_posterior:
        raise ValueError("pushed and reconstructed posterior laws must agree exactly")

    declared_information = tuple(agent.information for agent in datum.coarse_agents)
    expected_information = construct_coarse_information_interfaces(
        coarse_population,
        tuple(item.access for item in declared_information),
    )
    for agent, declared, expected in zip(datum.coarse_agents, declared_information, expected_information, strict=True):
        recognition_kernel = agent.recognition.recognition_kernel
        initial_masses = agent.recognition.initial_recognition.joint.masses
        if (
            recognition_kernel.source_labels != declared.access.information_labels
            or recognition_kernel.target_labels != agent.generative.agent.state_labels
            or any(row != initial_masses or sum(row, Fraction(0)) != 1 for row in recognition_kernel.matrix)
        ):
            raise ValueError("initial recognition rows must be normalized constant local laws")
        if declared.update != expected.update:
            raise ValueError("update row must equal the exact all-observation Bayes marginal")
        information_index = declared.access.information_labels.index(expected_coarse_record)
        posterior_marginal = _marginalize_coarse_law(expected_posterior, agent.generative.agent)
        if declared.update.kernel.matrix[information_index] != posterior_marginal.masses:
            raise ValueError("realized update row must equal the coarse posterior marginal")
