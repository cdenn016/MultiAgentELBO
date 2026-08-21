"""Immutable exact semantic contracts for the local-first v2 laboratory."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import json
import math
import re
from typing import Literal

from multiagent_elbo.finite.scale_cocycle import ExactMarkovChannel


def _require_identifier(value: str, *, field: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a nonempty string")


def _require_unique_labels(labels: tuple[str, ...], *, field: str) -> None:
    if not isinstance(labels, tuple) or not labels or any(not isinstance(label, str) or not label for label in labels):
        raise ValueError(f"{field} must be a nonempty tuple of nonempty strings")
    if len(set(labels)) != len(labels):
        raise ValueError(f"{field} must be unique")


def _require_fraction_masses(labels: tuple[str, ...], masses: tuple[Fraction, ...], *, field: str, unit_mass: bool) -> None:
    _require_unique_labels(labels, field=f"{field} labels")
    if not isinstance(masses, tuple) or len(masses) != len(labels):
        raise ValueError(f"{field} masses must align with labels")
    if any(not isinstance(mass, Fraction) for mass in masses):
        raise TypeError(f"{field} masses must be exact Fraction values")
    if any(mass < 0 for mass in masses):
        raise ValueError(f"{field} masses must be nonnegative")
    if unit_mass and sum(masses, Fraction(0)) != 1:
        raise ValueError(f"{field} masses must sum to one exactly")


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"))


def _require_ordered_assignment(label: str, ids: tuple[str, ...], *, width: int, field: str) -> None:
    """Validate one compact ordered JSON assignment against its declared IDs."""
    if not isinstance(label, str) or not label:
        raise ValueError(f"{field} support labels must be nonempty strings")
    try:
        parsed = json.loads(label)
    except json.JSONDecodeError as error:
        raise ValueError(f"{field} support labels must be canonical JSON assignments") from error
    if _canonical_json(parsed) != label or not isinstance(parsed, list) or len(parsed) != len(ids):
        raise ValueError(f"{field} support labels must use canonical ordered assignments")
    for expected_id, item in zip(ids, parsed, strict=True):
        if (
            not isinstance(item, list)
            or len(item) != width
            or item[0] != expected_id
            or any(not isinstance(part, str) or not part for part in item)
        ):
            raise ValueError(f"{field} support labels must match declared IDs in order")


def _canonical_local_labels(belief_labels: tuple[str, ...], model_labels: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(_canonical_json([belief, model]) for belief in belief_labels for model in model_labels)


def _require_exact_joint_matrix(rows: tuple[tuple[Fraction, ...], ...], *, row_count: int, column_count: int, field: str) -> None:
    if not isinstance(rows, tuple) or len(rows) != row_count:
        raise ValueError(f"{field} rows must align with labels")
    if any(not isinstance(row, tuple) or len(row) != column_count for row in rows):
        raise ValueError(f"{field} columns must align with labels")
    flattened = tuple(mass for row in rows for mass in row)
    if any(not isinstance(mass, Fraction) for mass in flattened):
        raise TypeError(f"{field} masses must be exact Fraction values")
    if any(mass < 0 for mass in flattened) or sum(flattened, Fraction(0)) != 1:
        raise ValueError(f"{field} masses must be nonnegative and sum to one exactly")


@dataclass(frozen=True)
class ExactProbabilityLaw:
    """Exact normalized finite probability law ``p(x)``."""

    labels: tuple[str, ...]
    masses: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        _require_fraction_masses(self.labels, self.masses, field="probability law", unit_mass=True)


@dataclass(frozen=True)
class ExactSubmeasure:
    """Exact nonnegative finite submeasure, with arbitrary total mass."""

    labels: tuple[str, ...]
    masses: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        _require_fraction_masses(self.labels, self.masses, field="submeasure", unit_mass=False)


@dataclass(frozen=True)
class ModelEvaluation:
    """One model-presentation evaluator over an agent's belief support."""

    model_label: str
    kernel: ExactMarkovChannel

    def __post_init__(self) -> None:
        _require_identifier(self.model_label, field="model label")
        if not isinstance(self.kernel, ExactMarkovChannel):
            raise TypeError("evaluator kernel must be an ExactMarkovChannel")


@dataclass(frozen=True)
class AgentDatum:
    """Local generative datum with exact evaluator compatibility.

    For positive model mass, ``G_i(b,m | pa) / G_i^M(m | pa)`` equals the
    corresponding evaluator row.
    """

    agent_id: str
    parent_ids: tuple[str, ...]
    belief_labels: tuple[str, ...]
    model_labels: tuple[str, ...]
    state_labels: tuple[str, ...]
    evaluator: tuple[ModelEvaluation, ...]
    generative_kernel: ExactMarkovChannel

    def __post_init__(self) -> None:
        _require_identifier(self.agent_id, field="agent ID")
        if not isinstance(self.parent_ids, tuple) or len(set(self.parent_ids)) != len(self.parent_ids):
            raise ValueError("parent IDs must be a unique tuple")
        for parent_id in self.parent_ids:
            _require_identifier(parent_id, field="parent ID")
        if self.agent_id in self.parent_ids:
            raise ValueError("an agent cannot be its own parent")
        _require_unique_labels(self.belief_labels, field="belief labels")
        _require_unique_labels(self.model_labels, field="model labels")
        if self.state_labels != _canonical_local_labels(self.belief_labels, self.model_labels):
            raise ValueError("state labels must be the belief-major canonical Cartesian product")
        if not isinstance(self.generative_kernel, ExactMarkovChannel):
            raise TypeError("generative kernel must be an ExactMarkovChannel")
        if self.generative_kernel.target_labels != self.state_labels:
            raise ValueError("generative kernel target labels must equal state labels")
        source_labels = self.generative_kernel.source_labels
        if not self.parent_ids:
            if source_labels != ("()",):
                raise ValueError("root generative kernel source labels must equal ('()',)")
        else:
            for source_label in source_labels:
                _require_ordered_assignment(source_label, self.parent_ids, width=3, field="parent")
        if not isinstance(self.evaluator, tuple) or len(self.evaluator) != len(self.model_labels):
            raise ValueError("evaluator must contain one entry for every model label")
        if any(not isinstance(entry, ModelEvaluation) for entry in self.evaluator):
            raise TypeError("evaluator entries must be ModelEvaluation values")
        if tuple(entry.model_label for entry in self.evaluator) != self.model_labels:
            raise ValueError("evaluator labels must equal model labels in declared order")
        for entry in self.evaluator:
            if entry.kernel.source_labels != source_labels or entry.kernel.target_labels != self.belief_labels:
                raise ValueError("evaluator support must match generative parent and belief supports")
        for source_index, row in enumerate(self.generative_kernel.matrix):
            for model_index, model_label in enumerate(self.model_labels):
                state_indices = tuple(index * len(self.model_labels) + model_index for index in range(len(self.belief_labels)))
                model_mass = sum((row[index] for index in state_indices), Fraction(0))
                if model_mass != 0:
                    conditional = tuple(row[index] / model_mass for index in state_indices)
                    if conditional != self.evaluator[model_index].kernel.matrix[source_index]:
                        raise ValueError(f"evaluator is incompatible with positive model slice {model_label!r}")


def _marginalize_local_law(agent: AgentDatum, joint: ExactProbabilityLaw, *, axis: Literal["belief", "model"]) -> ExactProbabilityLaw:
    """Return the exact belief or model marginal of a local recognition law."""
    if joint.labels != agent.state_labels:
        raise ValueError("joint recognition labels must equal the agent state labels")
    width = len(agent.model_labels)
    if axis == "belief":
        return ExactProbabilityLaw(agent.belief_labels, tuple(sum(joint.masses[index * width : (index + 1) * width], Fraction(0)) for index in range(len(agent.belief_labels))))
    return ExactProbabilityLaw(agent.model_labels, tuple(sum(joint.masses[index::width], Fraction(0)) for index in range(width)))


@dataclass(frozen=True, init=False)
class AgentRecognitionDatum:
    """A local recognition law with exact, derived belief and model marginals."""

    agent_id: str
    belief_labels: tuple[str, ...]
    model_labels: tuple[str, ...]
    state_labels: tuple[str, ...]
    joint: ExactProbabilityLaw
    belief_marginal: ExactProbabilityLaw
    model_marginal: ExactProbabilityLaw

    def __init__(self, agent: AgentDatum, joint: ExactProbabilityLaw) -> None:
        if not isinstance(agent, AgentDatum) or not isinstance(joint, ExactProbabilityLaw):
            raise TypeError("agent recognition requires an AgentDatum and exact joint law")
        _require_unique_labels(agent.belief_labels, field="belief labels")
        _require_unique_labels(agent.model_labels, field="model labels")
        if agent.state_labels != _canonical_local_labels(agent.belief_labels, agent.model_labels):
            raise ValueError("agent state labels must be canonical")
        belief = _marginalize_local_law(agent, joint, axis="belief")
        model = _marginalize_local_law(agent, joint, axis="model")
        object.__setattr__(self, "agent_id", agent.agent_id)
        object.__setattr__(self, "belief_labels", agent.belief_labels)
        object.__setattr__(self, "model_labels", agent.model_labels)
        object.__setattr__(self, "state_labels", agent.state_labels)
        object.__setattr__(self, "joint", joint)
        object.__setattr__(self, "belief_marginal", belief)
        object.__setattr__(self, "model_marginal", model)


@dataclass(frozen=True)
class RecordDatum:
    """A once-owned exact record kernel over a declared ordered scope."""

    record_id: str
    owner_id: str
    scope_ids: tuple[str, ...]
    outcome_labels: tuple[str, ...]
    kernel: ExactMarkovChannel

    def __post_init__(self) -> None:
        _require_identifier(self.record_id, field="record ID")
        _require_identifier(self.owner_id, field="record owner ID")
        _require_unique_labels(self.scope_ids, field="record scope IDs")
        if self.owner_id not in self.scope_ids:
            raise ValueError("record owner must belong to its scope")
        _require_unique_labels(self.outcome_labels, field="record outcome labels")
        if not isinstance(self.kernel, ExactMarkovChannel):
            raise TypeError("record kernel must be an ExactMarkovChannel")
        if self.kernel.target_labels != self.outcome_labels:
            raise ValueError("record kernel target labels must equal outcome labels")
        for source_label in self.kernel.source_labels:
            _require_ordered_assignment(source_label, self.scope_ids, width=3, field="scope")


@dataclass(frozen=True)
class SelectorSpec:
    """A product selector or an explicitly supplied correlated coupling."""

    selector_id: str
    selector_kind: Literal["product", "declared_correlated"]
    coupling: ExactProbabilityLaw | None

    def __post_init__(self) -> None:
        _require_identifier(self.selector_id, field="selector ID")
        if self.selector_kind not in ("product", "declared_correlated"):
            raise ValueError("selector kind is unsupported")
        if self.selector_kind == "product" and self.coupling is not None:
            raise ValueError("product selectors cannot supply a coupling")
        if self.selector_kind == "declared_correlated" and not isinstance(self.coupling, ExactProbabilityLaw):
            raise ValueError("declared-correlated selectors require an exact coupling")


@dataclass(frozen=True)
class CoarseChannelSpec:
    """Recognition-independent channel declaration and structural provenance."""

    channel_id: str
    source_agent_ids: tuple[str, ...]
    structural_input_ids: tuple[str, ...]
    channel: ExactMarkovChannel

    def __post_init__(self) -> None:
        _require_identifier(self.channel_id, field="channel ID")
        _require_unique_labels(self.source_agent_ids, field="source agent IDs")
        _require_unique_labels(self.structural_input_ids, field="structural input IDs")
        if not isinstance(self.channel, ExactMarkovChannel):
            raise TypeError("coarse channel must be an ExactMarkovChannel")
        if self.channel.recognition_independent is not True:
            raise ValueError("coarse channel must be recognition-independent")


@dataclass(frozen=True)
class PopulationJoint:
    """Exact complete population law over canonical latent and record assignments."""

    context_id: str
    agent_order: tuple[str, ...]
    record_order: tuple[str, ...]
    latent_labels: tuple[str, ...]
    observation_labels: tuple[str, ...]
    joint_masses: tuple[tuple[Fraction, ...], ...]
    construction_trace: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_identifier(self.context_id, field="context ID")
        _require_unique_labels(self.agent_order, field="agent order")
        _require_unique_labels(self.record_order, field="record order")
        _require_unique_labels(self.latent_labels, field="latent labels")
        _require_unique_labels(self.observation_labels, field="observation labels")
        for label in self.latent_labels:
            _require_ordered_assignment(label, self.agent_order, width=3, field="latent")
        for label in self.observation_labels:
            _require_ordered_assignment(label, self.record_order, width=2, field="observation")
        _require_exact_joint_matrix(self.joint_masses, row_count=len(self.latent_labels), column_count=len(self.observation_labels), field="population joint")
        expected_trace = tuple(f"agent:{agent_id}" for agent_id in self.agent_order) + tuple(f"record:{record_id}" for record_id in self.record_order)
        if self.construction_trace != expected_trace:
            raise ValueError("construction trace must use typed agent and record IDs exactly once in order")


@dataclass(frozen=True)
class PopulationInference:
    """Selected recognition and evidence-derived posterior for one observation."""

    population: PopulationJoint
    observed_record: str
    recognitions: tuple[AgentRecognitionDatum, ...]
    selector: SelectorSpec
    recognition: ExactProbabilityLaw
    evidence_measure: ExactSubmeasure
    evidence: Fraction
    posterior: ExactProbabilityLaw

    def __post_init__(self) -> None:
        if not isinstance(self.population, PopulationJoint) or not isinstance(self.selector, SelectorSpec):
            raise TypeError("population inference requires population and selector contracts")
        if self.observed_record not in self.population.observation_labels:
            raise ValueError("observed record must be a population observation label")
        if not isinstance(self.recognitions, tuple) or any(not isinstance(item, AgentRecognitionDatum) for item in self.recognitions):
            raise TypeError("recognitions must be AgentRecognitionDatum values")
        if tuple(item.agent_id for item in self.recognitions) != self.population.agent_order:
            raise ValueError("recognition agent IDs must align exactly with population agent order")
        if not isinstance(self.recognition, ExactProbabilityLaw) or not isinstance(self.evidence_measure, ExactSubmeasure) or not isinstance(self.posterior, ExactProbabilityLaw):
            raise TypeError("inference laws must use exact law contracts")
        for name, law in (("recognition", self.recognition), ("evidence measure", self.evidence_measure), ("posterior", self.posterior)):
            if law.labels != self.population.latent_labels:
                raise ValueError(f"{name} labels must equal population latent labels")
        if not isinstance(self.evidence, Fraction) or self.evidence < 0:
            raise ValueError("evidence must be a nonnegative exact Fraction")
        if self.evidence != sum(self.evidence_measure.masses, Fraction(0)):
            raise ValueError("evidence must equal the exact evidence-measure total")

    @property
    def selector_id(self) -> str:
        return self.selector.selector_id


@dataclass(frozen=True)
class AggregateDatum:
    """Terminal coarse probability datum; deliberately not an agent interface."""

    aggregate_id: str
    source_agent_ids: tuple[str, ...]
    observed_record: str
    channel_id: str
    channel_sha256: str
    observation_labels: tuple[str, ...]
    target_labels: tuple[str, ...]
    generative_joint: tuple[tuple[Fraction, ...], ...]
    recognition: ExactProbabilityLaw
    posterior: ExactProbabilityLaw
    evidence: Fraction
    conditional_kl_defect: float
    kl_chain_residual: float

    def __post_init__(self) -> None:
        _require_identifier(self.aggregate_id, field="aggregate ID")
        _require_unique_labels(self.source_agent_ids, field="source agent IDs")
        _require_identifier(self.channel_id, field="channel ID")
        if not isinstance(self.channel_sha256, str) or re.fullmatch(r"[0-9a-f]{64}", self.channel_sha256) is None:
            raise ValueError("channel SHA-256 must be 64 lowercase hexadecimal characters")
        _require_unique_labels(self.observation_labels, field="observation labels")
        _require_unique_labels(self.target_labels, field="target labels")
        if self.observed_record not in self.observation_labels:
            raise ValueError("observed record must be an aggregate observation label")
        _require_exact_joint_matrix(self.generative_joint, row_count=len(self.target_labels), column_count=len(self.observation_labels), field="aggregate generative")
        if not isinstance(self.recognition, ExactProbabilityLaw) or not isinstance(self.posterior, ExactProbabilityLaw):
            raise TypeError("aggregate recognition and posterior must be exact probability laws")
        if self.recognition.labels != self.target_labels:
            raise ValueError("aggregate recognition labels must equal target labels")
        if self.posterior.labels != self.target_labels:
            raise ValueError("aggregate posterior labels must equal target labels")
        if not isinstance(self.evidence, Fraction) or self.evidence < 0:
            raise ValueError("aggregate evidence must be a nonnegative exact Fraction")
        for name, value in (("conditional KL defect", self.conditional_kl_defect), ("KL chain residual", self.kl_chain_residual)):
            if not isinstance(value, float) or not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
