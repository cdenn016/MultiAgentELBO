"""Strict primitive-fixture loader for the local-first v2 laboratory."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
from typing import Literal

from multiagent_elbo.finite.scale_cocycle import ExactMarkovChannel
from rg_v2.contracts import AgentDatum, AgentRecognitionDatum, CoarseChannelSpec, ExactProbabilityLaw, ModelEvaluation, RecordDatum, SelectorSpec


FixtureName = Literal["lf3_product_v1", "lf3_correlated_v1", "lf3_dirac_boundary_v1"]
_TOP = frozenset({"schema_version", "fixture_id", "context_id", "agents", "recognitions", "records", "observation", "selector", "coarse_channel"})
_REF_TOP = frozenset({"schema_version", "fixture_id", "context_id", "shared_local_data", "selector"})
_KEYS = {
    "agent": frozenset({"agent_id", "parent_ids", "belief_labels", "model_labels", "generative_rows", "evaluator"}),
    "evaluator": frozenset({"model_label", "rows"}), "recognition": frozenset({"agent_id", "masses"}),
    "record": frozenset({"record_id", "owner_id", "scope_ids", "outcome_labels", "rows"}),
    "selector": frozenset({"selector_id", "selector_kind", "coupling"}), "coupling": frozenset({"masses"}),
    "coarse": frozenset({"channel_id", "source_agent_ids", "structural_input_ids", "target_labels", "rows"}),
    "rational": frozenset({"numerator", "denominator"}),
}
_DERIVED = frozenset({"population", "population_joint", "inference", "population_inference", "evidence", "evidence_measure", "posterior", "coarse_result", "coarse_law", "aggregate", "vfe", "status", "pass"})


@dataclass(frozen=True)
class LocalFirstFixture:
    """Primitive inputs only; population and inference data are derived later."""

    fixture_id: str
    fixture_path: Path
    fixture_sha256: str
    context_id: str
    agents: tuple[AgentDatum, ...]
    recognitions: tuple[AgentRecognitionDatum, ...]
    records: tuple[RecordDatum, ...]
    observation: tuple[tuple[str, str], ...]
    selector: SelectorSpec
    coarse_channel: CoarseChannelSpec


def _require_object(value: object, field: str) -> dict[str, object]:
    if type(value) is not dict:
        raise TypeError(f"{field} must be an object")
    return value


def _list(value: object, field: str) -> list[object]:
    if type(value) is not list:
        raise TypeError(f"{field} must be an array")
    return value


def _string(value: object, field: str) -> str:
    if type(value) is not str or not value:
        raise TypeError(f"{field} must be a nonempty string")
    return value


def _exact(payload: dict[str, object], keys: frozenset[str], field: str) -> None:
    if set(payload) != keys:
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
    payload = _require_object(value, field)
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
    return tuple(tuple(_fraction(item, f"{field}[{i}][{j}]") for j, item in enumerate(_list(row, f"{field}[{i}]"))) for i, row in enumerate(_list(value, field)))


def _strings(value: object, field: str) -> tuple[str, ...]:
    return tuple(_string(item, f"{field}[{i}]") for i, item in enumerate(_list(value, field)))


def _local(beliefs: tuple[str, ...], models: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(json.dumps([belief, model], ensure_ascii=True, separators=(",", ":")) for belief in beliefs for model in models)


def _decode(label: str) -> tuple[str, str]:
    value = json.loads(label)
    if type(value) is not list or len(value) != 2 or any(type(item) is not str for item in value):
        raise ValueError("local support labels must be canonical")
    return value[0], value[1]


def _assignments(ids: tuple[str, ...], agents: dict[str, AgentDatum]) -> tuple[str, ...]:
    supports = tuple(tuple(_decode(label) for label in agents[agent_id].state_labels) for agent_id in ids)
    return tuple(json.dumps([list((agent_id, belief, model)) for agent_id, (belief, model) in zip(ids, state, strict=True)], ensure_ascii=True, separators=(",", ":")) for state in product(*supports))


def _agents(value: object) -> tuple[AgentDatum, ...]:
    result: list[AgentDatum] = []
    prior: dict[str, AgentDatum] = {}
    for index, raw in enumerate(_list(value, "agents")):
        item = _require_object(raw, f"agents[{index}]")
        _exact(item, _KEYS["agent"], f"agents[{index}]")
        agent_id = _string(item["agent_id"], "agent ID")
        parents = _strings(item["parent_ids"], "parent IDs")
        if agent_id in prior or len(set(parents)) != len(parents) or any(parent not in prior for parent in parents):
            raise ValueError("agents must be unique and topologically ordered")
        beliefs, models = _strings(item["belief_labels"], "belief labels"), _strings(item["model_labels"], "model labels")
        source = ("()",) if not parents else _assignments(parents, prior)
        evaluator: list[ModelEvaluation] = []
        for evaluator_index, raw_evaluator in enumerate(_list(item["evaluator"], "evaluators")):
            entry = _require_object(raw_evaluator, f"evaluator[{evaluator_index}]")
            _exact(entry, _KEYS["evaluator"], "evaluator")
            evaluator.append(ModelEvaluation(_string(entry["model_label"], "model label"), ExactMarkovChannel(source, beliefs, _rows(entry["rows"], "evaluator rows"))))
        agent = AgentDatum(agent_id, parents, beliefs, models, _local(beliefs, models), tuple(evaluator), ExactMarkovChannel(source, _local(beliefs, models), _rows(item["generative_rows"], "generative rows")))
        result.append(agent)
        prior[agent_id] = agent
    if not result:
        raise ValueError("fixture requires agents")
    return tuple(result)


def _recognitions(value: object, agents: tuple[AgentDatum, ...]) -> tuple[AgentRecognitionDatum, ...]:
    raw = _list(value, "recognitions")
    if len(raw) != len(agents):
        raise ValueError("recognitions must align with agents")
    result: list[AgentRecognitionDatum] = []
    for item, agent in zip(raw, agents, strict=True):
        payload = _require_object(item, "recognition")
        _exact(payload, _KEYS["recognition"], "recognition")
        if _string(payload["agent_id"], "recognition agent ID") != agent.agent_id:
            raise ValueError("recognitions must use agent order")
        result.append(AgentRecognitionDatum(agent, ExactProbabilityLaw(agent.state_labels, tuple(_fraction(mass, "recognition mass") for mass in _list(payload["masses"], "recognition masses")))))
    return tuple(result)


def _records(value: object, agents: tuple[AgentDatum, ...]) -> tuple[RecordDatum, ...]:
    agent_map = {agent.agent_id: agent for agent in agents}
    result: list[RecordDatum] = []
    for raw in _list(value, "records"):
        item = _require_object(raw, "record")
        _exact(item, _KEYS["record"], "record")
        scope, outcomes = _strings(item["scope_ids"], "record scope IDs"), _strings(item["outcome_labels"], "record outcomes")
        if any(agent_id not in agent_map for agent_id in scope):
            raise ValueError("record scope must be declared")
        result.append(RecordDatum(_string(item["record_id"], "record ID"), _string(item["owner_id"], "record owner ID"), scope, outcomes, ExactMarkovChannel(_assignments(scope, agent_map), outcomes, _rows(item["rows"], "record rows"))))
    if not result or len({record.record_id for record in result}) != len(result):
        raise ValueError("record IDs must be nonempty and unique")
    return tuple(result)


def _observation(value: object, records: tuple[RecordDatum, ...]) -> tuple[tuple[str, str], ...]:
    pairs = tuple(_strings(item, "observation entry") for item in _list(value, "observation"))
    if any(len(pair) != 2 for pair in pairs) or tuple(pair[0] for pair in pairs) != tuple(record.record_id for record in records):
        raise ValueError("observation must align with record order")
    if any(outcome not in record.outcome_labels for (_, outcome), record in zip(pairs, records, strict=True)):
        raise ValueError("observation outcome must be declared")
    return tuple((pair[0], pair[1]) for pair in pairs)


def _selector(value: object, latent: tuple[str, ...]) -> SelectorSpec:
    item = _require_object(value, "selector")
    _exact(item, _KEYS["selector"], "selector")
    selector_id, kind = _string(item["selector_id"], "selector ID"), _string(item["selector_kind"], "selector kind")
    if kind == "product":
        if item["coupling"] is not None:
            raise ValueError("product selector cannot supply coupling")
        return SelectorSpec(selector_id, "product", None)
    if kind != "declared_correlated":
        raise ValueError("selector kind is unsupported")
    coupling = _require_object(item["coupling"], "declared coupling")
    _exact(coupling, _KEYS["coupling"], "declared coupling")
    masses = _list(coupling["masses"], "declared coupling masses")
    if len(masses) != len(latent):
        raise ValueError("declared coupling must explicitly list the full canonical latent table")
    return SelectorSpec(selector_id, "declared_correlated", ExactProbabilityLaw(latent, tuple(_fraction(mass, "declared coupling mass") for mass in masses)))


def _coarse(value: object, agents: tuple[AgentDatum, ...], latent: tuple[str, ...]) -> CoarseChannelSpec:
    item = _require_object(value, "coarse channel")
    _exact(item, _KEYS["coarse"], "coarse channel")
    source_ids, structural = _strings(item["source_agent_ids"], "coarse source IDs"), _strings(item["structural_input_ids"], "coarse structural IDs")
    if source_ids != tuple(agent.agent_id for agent in agents) or not structural:
        raise ValueError("coarse declaration must retain full source order and structural provenance")
    return CoarseChannelSpec(_string(item["channel_id"], "coarse channel ID"), source_ids, structural, ExactMarkovChannel(latent, _strings(item["target_labels"], "coarse target labels"), _rows(item["rows"], "coarse rows")))


def _build_fixture(fixture: FixtureName, path: Path, raw_sha256: str, payload: dict[str, object]) -> LocalFirstFixture:
    """Build one schema-validated primitive fixture."""
    _reject_derived(payload)
    _exact(payload, _REF_TOP if fixture == "lf3_correlated_v1" else _TOP, "fixture")
    if _string(payload["fixture_id"], "fixture ID") != fixture or _string(payload["schema_version"], "schema version") != "lf3-primitive-v1":
        raise ValueError("fixture identity or schema version is invalid")
    if type(raw_sha256) is not str or len(raw_sha256) != 64:
        raise ValueError("fixture SHA-256 is invalid")
    if fixture == "lf3_correlated_v1":
        if _string(payload["shared_local_data"], "shared local data") != "lf3_product_v1":
            raise ValueError("correlated fixture must reference frozen product local data")
        shared = load_fixture("lf3_product_v1")
        if _string(payload["context_id"], "context ID") != shared.context_id:
            raise ValueError("referenced local data must retain context")
        latent = _assignments(tuple(agent.agent_id for agent in shared.agents), {agent.agent_id: agent for agent in shared.agents})
        return LocalFirstFixture(fixture, path, raw_sha256, shared.context_id, shared.agents, shared.recognitions, shared.records, shared.observation, _selector(payload["selector"], latent), shared.coarse_channel)
    agents = _agents(payload["agents"])
    latent = _assignments(tuple(agent.agent_id for agent in agents), {agent.agent_id: agent for agent in agents})
    if len(latent) > 4096:
        raise ValueError("fixture exceeds the 4096-state exact limit")
    records = _records(payload["records"], agents)
    return LocalFirstFixture(fixture, path, raw_sha256, _string(payload["context_id"], "context ID"), agents, _recognitions(payload["recognitions"], agents), records, _observation(payload["observation"], records), _selector(payload["selector"], latent), _coarse(payload["coarse_channel"], agents, latent))


def load_fixture(fixture: FixtureName) -> LocalFirstFixture:
    """Load a closed Release 1 primitive fixture by its identifier."""
    path = Path(__file__).with_name("data") / f"{fixture}.json"
    raw = path.read_bytes()
    payload = _require_object(json.loads(raw.decode("utf-8")), "fixture")
    _exact(payload, _REF_TOP if fixture == "lf3_correlated_v1" else _TOP, "fixture")
    return _build_fixture(fixture, path, hashlib.sha256(raw).hexdigest(), payload)


__all__ = ["FixtureName", "LocalFirstFixture", "load_fixture"]
