"""Immutable semantic contracts for the recursive coarse-agent fixture."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import re
from typing import Literal

from multiagent_elbo.finite.scale_cocycle import ExactMarkovChannel
from rg_v2.contracts import (
    AgentDatum,
    AgentRecognitionDatum,
    CoarseChannelSpec,
    ExactProbabilityLaw,
    PopulationInference,
    PopulationJoint,
    RecordDatum,
)


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), allow_nan=False)


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
