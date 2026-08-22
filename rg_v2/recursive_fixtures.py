"""Strict loader for the self-contained LF4 recursive primitive fixture."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import re
from typing import Literal

from multiagent_elbo.finite.scale_cocycle import ExactMarkovChannel
from rg_v2.coarse_agent import (
    CoarseAccessSpec,
    CoarseAgentSpec,
    CoarseObservationSpec,
    RecursiveCoarseStructure,
    SparseRecordFactorizationSpec,
    canonical_agent_assignment_labels,
    canonical_local_state_labels,
    validate_coarse_structure_source_supports,
)
from rg_v2.contracts import AgentDatum, AgentRecognitionDatum, ExactProbabilityLaw, ModelEvaluation, RecordDatum, SelectorSpec


RecursiveFixtureName = Literal["lf4_two_parent_recursive_v1"]
_NAME = "lf4_two_parent_recursive_v1"
_TOP = frozenset({"schema_version", "fixture_id", "context_id", "agents", "recognitions", "records", "selector", "observation", "recursive_structure", "access_specs"})
_KEYS = {
    "agent": frozenset({"agent_id", "parent_ids", "belief_labels", "model_labels", "generative_rows", "evaluator"}),
    "evaluator": frozenset({"model_label", "rows"}),
    "recognition": frozenset({"agent_id", "masses"}),
    "record": frozenset({"record_id", "owner_id", "scope_ids", "outcome_labels", "rows"}),
    "selector": frozenset({"selector_id", "selector_kind", "coupling"}),
    "coupling": frozenset({"masses"}),
    "rational": frozenset({"numerator", "denominator"}),
    "structure": frozenset({"structure_id", "source_agent_order", "coarse_agent_order", "agents", "observation", "sparse_record_candidate"}),
    "coarse_agent": frozenset({"agent_id", "source_agent_ids", "parent_ids", "source_context_id", "belief_labels", "model_labels", "block_rows", "null_row_policy"}),
    "observation_spec": frozenset({"record_id", "fine_observation_labels", "compound_outcome_labels", "compound_outcome_by_fine_observation"}),
    "sparse": frozenset({"left_record_ids", "right_record_ids", "left_outcome_labels", "right_outcome_labels", "left_outcome_by_fine_observation", "right_outcome_by_fine_observation"}),
    "access": frozenset({"agent_id", "observation_labels", "information_labels", "information_by_observation", "access_kind"}),
}
_DERIVED = frozenset({"population", "population_joint", "inference", "population_inference", "evidence", "evidence_measure", "posterior", "coarse_result", "coarse_law", "aggregate", "vfe", "status", "pass"})


@dataclass(frozen=True)
class RecursiveFixture:
    """Primitive inputs; all population and inference quantities are derived later."""

    fixture_id: str
    fixture_path: Path
    fixture_sha256: str
    subrecord_sha256: tuple[tuple[str, str], ...]
    context_id: str
    agents: tuple[AgentDatum, ...]
    recognitions: tuple[AgentRecognitionDatum, ...]
    records: tuple[RecordDatum, ...]
    observation: tuple[tuple[str, str], ...]
    selector: SelectorSpec
    structure: RecursiveCoarseStructure
    access_specs: tuple[CoarseAccessSpec, ...]


def _object(value: object, field: str) -> dict[str, object]:
    if type(value) is not dict:
        raise TypeError(f"{field} must be an object")
    return value


def _array(value: object, field: str) -> list[object]:
    if type(value) is not list:
        raise TypeError(f"{field} must be an array")
    return value


def _string(value: object, field: str) -> str:
    if type(value) is not str or not value:
        raise TypeError(f"{field} must be a nonempty string")
    return value


def _strings(value: object, field: str) -> tuple[str, ...]:
    return tuple(_string(item, f"{field}[{index}]") for index, item in enumerate(_array(value, field)))


def _exact(value: dict[str, object], keys: frozenset[str], field: str) -> None:
    if set(value) != keys:
        raise ValueError(f"{field} keys must equal the declared schema")


def _reject_derived(value: object) -> None:
    if type(value) is dict:
        for key, nested in value.items():
            if key in _DERIVED:
                raise ValueError(f"prohibited derived fixture key {key!r}")
            _reject_derived(nested)
    elif type(value) is list:
        for nested in value:
            _reject_derived(nested)


def _fraction(value: object, field: str) -> Fraction:
    payload = _object(value, field)
    _exact(payload, _KEYS["rational"], field)
    numerator, denominator = payload["numerator"], payload["denominator"]
    if type(numerator) is not int or type(denominator) is not int:
        raise TypeError(f"{field} numerator and denominator must be integers")
    if denominator <= 0:
        raise ValueError(f"{field} denominator must be positive")
    result = Fraction(numerator, denominator)
    if (result.numerator, result.denominator) != (numerator, denominator):
        raise ValueError(f"{field} must be reduced")
    return result


def _rows(value: object, field: str) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(_fraction(entry, f"{field}[{row_index}][{column_index}]") for column_index, entry in enumerate(_array(row, f"{field}[{row_index}]"))) for row_index, row in enumerate(_array(value, field)))


def _local_labels(beliefs: tuple[str, ...], models: tuple[str, ...]) -> tuple[str, ...]:
    return canonical_local_state_labels(beliefs, models)


def _assignment_labels(agent_ids: tuple[str, ...], known: dict[str, AgentDatum]) -> tuple[str, ...]:
    return canonical_agent_assignment_labels(tuple(known[agent_id] for agent_id in agent_ids))


def _agents(value: object) -> tuple[AgentDatum, ...]:
    result: list[AgentDatum] = []
    known: dict[str, AgentDatum] = {}
    for index, raw in enumerate(_array(value, "agents")):
        item = _object(raw, f"agents[{index}]")
        _exact(item, _KEYS["agent"], f"agents[{index}]")
        agent_id = _string(item["agent_id"], "agent ID")
        parents = _strings(item["parent_ids"], "parent IDs")
        if agent_id in known or len(set(parents)) != len(parents) or any(parent not in known for parent in parents):
            raise ValueError("agents must be unique and topologically ordered")
        beliefs, models = _strings(item["belief_labels"], "belief labels"), _strings(item["model_labels"], "model labels")
        source = ("()",) if not parents else _assignment_labels(parents, known)
        evaluators: list[ModelEvaluation] = []
        for evaluator_index, raw_evaluator in enumerate(_array(item["evaluator"], "evaluator")):
            evaluator = _object(raw_evaluator, f"evaluator[{evaluator_index}]")
            _exact(evaluator, _KEYS["evaluator"], "evaluator")
            try:
                evaluators.append(ModelEvaluation(_string(evaluator["model_label"], "model label"), ExactMarkovChannel(source, beliefs, _rows(evaluator["rows"], "evaluator rows"))))
            except (TypeError, ValueError) as error:
                raise ValueError(f"agent generative/evaluator declaration is invalid: {error}") from error
        try:
            agent = AgentDatum(agent_id, parents, beliefs, models, _local_labels(beliefs, models), tuple(evaluators), ExactMarkovChannel(source, _local_labels(beliefs, models), _rows(item["generative_rows"], "generative rows")))
        except (TypeError, ValueError) as error:
            raise ValueError(f"agent generative/evaluator declaration is invalid: {error}") from error
        result.append(agent)
        known[agent_id] = agent
    expected_chain = (
        ("a0", ()),
        ("a1", ("a0",)),
        ("a2", ("a1",)),
        ("a3", ("a2",)),
    )
    if tuple((agent.agent_id, agent.parent_ids) for agent in result) != expected_chain:
        raise ValueError("fixture agents must use the canonical a0 -> a1 -> a2 -> a3 chain")
    if any(agent.belief_labels != ("b0", "b1") or agent.model_labels != ("m0", "m1") for agent in result):
        raise ValueError("fixture agents must use the canonical binary belief and model labels")
    return tuple(result)


def _recognitions(value: object, agents: tuple[AgentDatum, ...]) -> tuple[AgentRecognitionDatum, ...]:
    rows = _array(value, "recognitions")
    if len(rows) != len(agents):
        raise ValueError("recognitions must align with agents")
    result: list[AgentRecognitionDatum] = []
    for raw, agent in zip(rows, agents, strict=True):
        item = _object(raw, "recognition")
        _exact(item, _KEYS["recognition"], "recognition")
        if _string(item["agent_id"], "recognition agent ID") != agent.agent_id:
            raise ValueError("recognitions must use agent order")
        result.append(AgentRecognitionDatum(agent, ExactProbabilityLaw(agent.state_labels, tuple(_fraction(mass, "recognition mass") for mass in _array(item["masses"], "recognition masses")))))
    return tuple(result)


def _records(value: object, agents: tuple[AgentDatum, ...]) -> tuple[RecordDatum, ...]:
    known = {agent.agent_id: agent for agent in agents}
    result: list[RecordDatum] = []
    for raw in _array(value, "records"):
        item = _object(raw, "record")
        _exact(item, _KEYS["record"], "record")
        scope, outcomes = _strings(item["scope_ids"], "record scope IDs"), _strings(item["outcome_labels"], "record outcomes")
        if not scope or any(agent_id not in known for agent_id in scope):
            raise ValueError("record scope must be declared")
        rows = _rows(item["rows"], "record rows")
        if len(rows) != len(_assignment_labels(scope, known)):
            raise ValueError("record rows must align with the declared scope support")
        result.append(RecordDatum(_string(item["record_id"], "record ID"), _string(item["owner_id"], "record owner ID"), scope, outcomes, ExactMarkovChannel(_assignment_labels(scope, known), outcomes, rows)))
    expected = (
        ("r0", "a0", ("a0",)),
        ("r1", "a1", ("a1", "a2")),
        ("r2", "a2", ("a1", "a2")),
        ("r3", "a3", ("a3",)),
    )
    if tuple((record.record_id, record.owner_id, record.scope_ids) for record in result) != expected:
        raise ValueError("fixture records must use the canonical IDs, owners, scopes, and order")
    if any(record.outcome_labels != ("0", "1") for record in result):
        raise ValueError("fixture records must use canonical binary outcomes")
    return tuple(result)


def _observation(value: object, records: tuple[RecordDatum, ...]) -> tuple[tuple[str, str], ...]:
    result = tuple(_strings(item, "observation entry") for item in _array(value, "observation"))
    if any(len(item) != 2 for item in result) or tuple(item[0] for item in result) != tuple(record.record_id for record in records):
        raise ValueError("observation must align with record order")
    if any(outcome not in record.outcome_labels for (_, outcome), record in zip(result, records, strict=True)):
        raise ValueError("observation outcome must be declared")
    return tuple((record_id, outcome) for record_id, outcome in result)


def _selector(value: object, agents: tuple[AgentDatum, ...], recognitions: tuple[AgentRecognitionDatum, ...]) -> SelectorSpec:
    item = _object(value, "selector")
    _exact(item, _KEYS["selector"], "selector")
    if _string(item["selector_kind"], "selector kind") != "declared_correlated":
        raise ValueError("selector kind must be declared_correlated")
    coupling_payload = _object(item["coupling"], "declared coupling")
    _exact(coupling_payload, _KEYS["coupling"], "declared coupling")
    labels = _assignment_labels(tuple(agent.agent_id for agent in agents), {agent.agent_id: agent for agent in agents})
    masses = tuple(_fraction(mass, "declared coupling mass") for mass in _array(coupling_payload["masses"], "declared coupling masses"))
    if len(masses) != len(labels):
        raise ValueError("declared coupling must explicitly list the full canonical latent table")
    coupling = ExactProbabilityLaw(labels, masses)
    for label, mass in zip(coupling.labels, coupling.masses, strict=True):
        belief_bits = tuple(int(entry[1][-1]) for entry in json.loads(label))
        expected_mass = Fraction(1, 128) if sum(belief_bits) % 2 == 0 else Fraction(0)
        if mass != expected_mass:
            raise ValueError("declared coupling must use the canonical even-belief-parity table")
    for index, recognition in enumerate(recognitions):
        actual = {label: Fraction(0) for label in recognition.state_labels}
        for label, mass in zip(coupling.labels, coupling.masses, strict=True):
            belief, model = json.loads(label)[index][1:]
            actual[json.dumps([belief, model], ensure_ascii=True, separators=(",", ":"))] += mass
        if tuple(actual[label] for label in recognition.state_labels) != recognition.joint.masses:
            raise ValueError("declared coupling local marginal disagrees with recognition")
    if _string(item["selector_id"], "selector ID") != "lf4-parity-correlated-selector-v1":
        raise ValueError("selector ID must equal the canonical LF4 selector ID")
    return SelectorSpec("lf4-parity-correlated-selector-v1", "declared_correlated", coupling)


def _fine_observation_labels(records: tuple[RecordDatum, ...]) -> tuple[str, ...]:
    return tuple(json.dumps([[record.record_id, outcome] for record, outcome in zip(records, outcomes, strict=True)], ensure_ascii=True, separators=(",", ":")) for outcomes in product(*(record.outcome_labels for record in records)))


def _structure(value: object, agents: tuple[AgentDatum, ...], records: tuple[RecordDatum, ...], context_id: str) -> RecursiveCoarseStructure:
    item = _object(value, "recursive structure")
    _exact(item, _KEYS["structure"], "recursive structure")
    specs: list[CoarseAgentSpec] = []
    known = {agent.agent_id: agent for agent in agents}
    for raw in _array(item["agents"], "coarse agents"):
        spec = _object(raw, "coarse agent")
        _exact(spec, _KEYS["coarse_agent"], "coarse agent")
        source = _strings(spec["source_agent_ids"], "coarse source agent IDs")
        beliefs, models = _strings(spec["belief_labels"], "coarse belief labels"), _strings(spec["model_labels"], "coarse model labels")
        state_labels = _local_labels(beliefs, models)
        specs.append(CoarseAgentSpec(_string(spec["agent_id"], "coarse agent ID"), source, _strings(spec["parent_ids"], "coarse parent IDs"), _string(spec["source_context_id"], "coarse source context ID"), beliefs, models, state_labels, ExactMarkovChannel(_assignment_labels(source, known), state_labels, _rows(spec["block_rows"], "block channel rows"), recognition_independent=True), _string(spec["null_row_policy"], "null row policy")))
    observation_payload = _object(item["observation"], "coarse observation")
    _exact(observation_payload, _KEYS["observation_spec"], "coarse observation")
    observation = CoarseObservationSpec(_string(observation_payload["record_id"], "compound record ID"), _strings(observation_payload["fine_observation_labels"], "fine observation labels"), _strings(observation_payload["compound_outcome_labels"], "compound outcome labels"), _strings(observation_payload["compound_outcome_by_fine_observation"], "compound observation map"))
    sparse_payload = _object(item["sparse_record_candidate"], "sparse record candidate")
    _exact(sparse_payload, _KEYS["sparse"], "sparse record candidate")
    sparse = SparseRecordFactorizationSpec(_strings(sparse_payload["left_record_ids"], "left record IDs"), _strings(sparse_payload["right_record_ids"], "right record IDs"), _strings(sparse_payload["left_outcome_labels"], "left outcomes"), _strings(sparse_payload["right_outcome_labels"], "right outcomes"), _strings(sparse_payload["left_outcome_by_fine_observation"], "left sparse projection"), _strings(sparse_payload["right_outcome_by_fine_observation"], "right sparse projection"))
    structure = RecursiveCoarseStructure(_string(item["structure_id"], "structure ID"), _strings(item["source_agent_order"], "source agent order"), _strings(item["coarse_agent_order"], "coarse agent order"), tuple(specs), observation, sparse)
    if structure.structure_id != "lf4-two-parent-structure-v1":
        raise ValueError("structure ID must equal the canonical LF4 structure ID")
    if any(spec.source_context_id != context_id for spec in structure.agent_specs):
        raise ValueError("coarse source context must equal fixture context")
    validate_coarse_structure_source_supports(structure, agents)
    expected_fine = _fine_observation_labels(records)
    expected_outcomes = tuple(f"o{bits[0]}{bits[1]}{bits[2]}{bits[3]}" for bits in product("01", repeat=4))
    if structure.observation.fine_observation_labels != expected_fine or structure.observation.compound_outcome_labels != expected_outcomes or structure.observation.compound_outcome_by_fine_observation != expected_outcomes:
        raise ValueError("observation declaration must use canonical fine-observation order")
    expected_left = tuple(f"l{bits[0]}{bits[1]}" for bits in product("01", repeat=4))
    expected_right = tuple(f"r{bits[2]}{bits[3]}" for bits in product("01", repeat=4))
    if (
        sparse.left_record_ids != ("r0", "r1")
        or sparse.right_record_ids != ("r2", "r3")
        or sparse.left_outcome_labels != ("l00", "l01", "l10", "l11")
        or sparse.right_outcome_labels != ("r00", "r01", "r10", "r11")
        or sparse.left_outcome_by_fine_observation != expected_left
        or sparse.right_outcome_by_fine_observation != expected_right
    ):
        raise ValueError("sparse record declaration must use canonical record groups and projections")
    return structure


def _validate_canonical_lf4_semantics(
    agents: tuple[AgentDatum, ...],
    records: tuple[RecordDatum, ...],
    structure: RecursiveCoarseStructure,
) -> None:
    """Validate the fixed LF4 primitive laws without constructing missing tables."""
    root_generation = (
        (Fraction(3, 8), Fraction(1, 8), Fraction(1, 8), Fraction(3, 8)),
    )
    root_evaluator = (
        ((Fraction(3, 4), Fraction(1, 4)),),
        ((Fraction(1, 4), Fraction(3, 4)),),
    )
    child_generation = (
        (Fraction(3, 5), Fraction(3, 20), Fraction(3, 20), Fraction(1, 10)),
        (Fraction(1, 5), Fraction(9, 20), Fraction(1, 20), Fraction(3, 10)),
        (Fraction(3, 10), Fraction(1, 20), Fraction(9, 20), Fraction(1, 5)),
        (Fraction(1, 10), Fraction(3, 20), Fraction(3, 20), Fraction(3, 5)),
    )
    child_evaluator = (
        (
            (Fraction(4, 5), Fraction(1, 5)),
            (Fraction(4, 5), Fraction(1, 5)),
            (Fraction(2, 5), Fraction(3, 5)),
            (Fraction(2, 5), Fraction(3, 5)),
        ),
        (
            (Fraction(3, 5), Fraction(2, 5)),
            (Fraction(3, 5), Fraction(2, 5)),
            (Fraction(1, 5), Fraction(4, 5)),
            (Fraction(1, 5), Fraction(4, 5)),
        ),
    )
    for index, agent in enumerate(agents):
        expected_generation = root_generation if index == 0 else child_generation
        expected_evaluator = root_evaluator if index == 0 else child_evaluator
        actual_evaluator = tuple(entry.kernel.matrix for entry in agent.evaluator)
        if agent.generative_kernel.matrix != expected_generation or actual_evaluator != expected_evaluator:
            raise ValueError("canonical LF4 agent and evaluator semantics are invalid")
        if any(mass <= 0 for row in agent.generative_kernel.matrix for mass in row):
            raise ValueError("canonical LF4 agent mechanisms must be strictly positive")
        if any(mass <= 0 for entry in agent.evaluator for row in entry.kernel.matrix for mass in row):
            raise ValueError("canonical LF4 evaluator mechanisms must be strictly positive")

    for record in records:
        expected_rows: list[tuple[Fraction, Fraction]] = []
        for source_label in record.kernel.source_labels:
            assignment = json.loads(source_label)
            if record.record_id in ("r0", "r3"):
                high_probability = assignment[0][1] == "b0"
            else:
                high_probability = assignment[0][1] == assignment[1][1]
            expected_rows.append(
                (Fraction(4, 5), Fraction(1, 5))
                if high_probability
                else (Fraction(1, 5), Fraction(4, 5))
            )
        if record.kernel.matrix != tuple(expected_rows):
            raise ValueError("canonical LF4 record semantics are invalid")
        if any(mass <= 0 for row in record.kernel.matrix for mass in row):
            raise ValueError("canonical LF4 record mechanisms must be strictly positive")

    for spec in structure.agent_specs:
        if len(spec.block_channel.source_labels) != 16 or len(spec.block_channel.target_labels) != 4:
            raise ValueError("canonical LF4 block channels must be explicit 16 x 4 tables")
        expected_rows = []
        for source_label in spec.block_channel.source_labels:
            assignment = json.loads(source_label)
            belief_parity = sum(int(entry[1][-1]) for entry in assignment) % 2
            model_parity = sum(int(entry[2][-1]) for entry in assignment) % 2
            target = json.dumps([f"B{belief_parity}", f"M{model_parity}"], ensure_ascii=True, separators=(",", ":"))
            target_index = spec.block_channel.target_labels.index(target)
            expected_rows.append(tuple(Fraction(int(index == target_index)) for index in range(4)))
        if spec.block_channel.matrix != tuple(expected_rows):
            raise ValueError("canonical LF4 block channels must implement belief/model parity")


def _access(value: object, structure: RecursiveCoarseStructure) -> tuple[CoarseAccessSpec, ...]:
    result: list[CoarseAccessSpec] = []
    expected_observations = tuple(json.dumps([[structure.observation.record_id, outcome]], ensure_ascii=True, separators=(",", ":")) for outcome in structure.observation.compound_outcome_labels)
    for raw in _array(value, "access specs"):
        item = _object(raw, "access spec")
        _exact(item, _KEYS["access"], "access spec")
        result.append(CoarseAccessSpec(_string(item["agent_id"], "access agent ID"), _strings(item["observation_labels"], "access observation labels"), _strings(item["information_labels"], "access information labels"), _strings(item["information_by_observation"], "access map"), _string(item["access_kind"], "access kind")))
    if tuple(spec.agent_id for spec in result) != structure.coarse_agent_order:
        raise ValueError("access specs must use coarse agent order")
    if any(spec.observation_labels != expected_observations for spec in result):
        raise ValueError("access specs must cover reconstructed observation support")
    return tuple(result)


def _canonical_sha256(value: object) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True, allow_nan=False).encode("utf-8")).hexdigest()


def _decode_recursive_fixture(payload: dict[str, object], path: Path, raw_sha256: str) -> RecursiveFixture:
    _reject_derived(payload)
    _exact(payload, _TOP, "fixture")
    if _string(payload["fixture_id"], "fixture ID") != _NAME or _string(payload["schema_version"], "schema version") != "lf4-recursive-primitive-v1":
        raise ValueError("fixture identity or schema version is invalid")
    if not isinstance(path, Path) or not isinstance(raw_sha256, str) or re.fullmatch(r"[0-9a-f]{64}", raw_sha256) is None:
        raise ValueError("fixture path and raw SHA-256 are invalid")
    context_id = _string(payload["context_id"], "context ID")
    if context_id != "lf4-context-v1":
        raise ValueError("context ID must equal the canonical LF4 context ID")
    agents = _agents(payload["agents"])
    recognitions = _recognitions(payload["recognitions"], agents)
    records = _records(payload["records"], agents)
    observation = _observation(payload["observation"], records)
    selector = _selector(payload["selector"], agents, recognitions)
    structure = _structure(payload["recursive_structure"], agents, records, context_id)
    _validate_canonical_lf4_semantics(agents, records, structure)
    access_specs = _access(payload["access_specs"], structure)
    subrecords = (("generative", {"agents": payload["agents"], "records": payload["records"]}), ("recognition", {"recognitions": payload["recognitions"], "selector": payload["selector"]}), ("structure", payload["recursive_structure"]), ("access", payload["access_specs"]))
    return RecursiveFixture(_NAME, path, raw_sha256, tuple((name, _canonical_sha256(value)) for name, value in subrecords), context_id, agents, recognitions, records, observation, selector, structure, access_specs)


def _fixture_path(fixture: RecursiveFixtureName) -> Path:
    if type(fixture) is not str or fixture != _NAME:
        raise ValueError("fixture must be the admitted LF4 recursive fixture ID")
    directory = Path(__file__).with_name("data").resolve()
    path = (directory / f"{fixture}.json").resolve()
    if path.parent != directory:
        raise ValueError("fixture path escapes the fixed data directory")
    return path


def load_recursive_fixture(fixture: RecursiveFixtureName) -> RecursiveFixture:
    """Load the closed LF4 primitive fixture after name-before-read validation."""
    path = _fixture_path(fixture)
    raw = path.read_bytes()
    payload = _object(json.loads(raw.decode("utf-8")), "fixture")
    return _decode_recursive_fixture(payload, path, hashlib.sha256(raw).hexdigest())


__all__ = ["RecursiveFixture", "RecursiveFixtureName", "load_recursive_fixture"]
