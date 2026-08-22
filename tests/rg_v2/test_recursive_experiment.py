from __future__ import annotations

import ast
from dataclasses import replace
from fractions import Fraction
import hashlib
import inspect
from itertools import combinations, product
import json
import os
from pathlib import Path
import shutil
import subprocess
import zipfile

import numpy as np
import pytest

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import (
    ExperimentConfig,
    RenormalizationV2TheoryConfig,
    config_sha256,
)
from multiagent_elbo.experiment_support import EXPERIMENT_REGISTRY
from multiagent_elbo.finite.scale_cocycle import ExactMarkovChannel
from rg_v2.coarse_agent import (
    CoarseAccessSpec,
    CoarseAgentSpec,
    CoarseObservationSpec,
    RecursiveCoarseStructure,
    SparseRecordFactorizationSpec,
    _enumerate_coarse_population_independently,
    construct_coarse_information_interfaces,
    construct_coarse_population_joint,
    construct_coarse_recognition,
    derive_recursive_observation,
    validate_recursive_observation,
)
from rg_v2.coarse import aggregate_population
from rg_v2.contracts import (
    AgentDatum,
    AgentRecognitionDatum,
    AggregateDatum,
    CoarseChannelSpec,
    ExactProbabilityLaw,
    ExactSubmeasure,
    ModelEvaluation,
    PopulationInference,
    PopulationJoint,
    RecordDatum,
    SelectorSpec,
)
import rg_v2.recursive_experiment as experiment_module
from rg_v2.recursive_experiment import (
    run_renormalization_v2_recursive_experiment,
)
from rg_v2.recursive_fixtures import RecursiveFixture, load_recursive_fixture
from rg_v2.population import (
    construct_population_joint,
    derive_population_inference,
    enumerate_population_joint_independently,
)


_JSON_STEMS = (
    "fixture_snapshot",
    "fine_population",
    "coarse_generative",
    "coarse_interfaces",
    "coarse_population",
    "all_observation_inference",
    "metrics",
)
_ARTIFACT_STEMS = (*_JSON_STEMS, "arrays")
_CORE_FILES = ("config.json", "manifest.json")
_ARTIFACT_FILES = tuple(f"{name}.json" for name in _JSON_STEMS) + (
    "arrays.npz",
)
_PROVENANCE_ARRAYS = (
    "schema_version",
    "fixture_id",
    "producer_commit",
    "config_hash",
    "direct_input_names",
    "direct_input_sha256",
)
_FLOAT_ARRAYS = (
    "fine_population",
    "fine_population_oracle",
    "coarse_pushed_population",
    "coarse_reconstructed_population",
    "fine_recognition",
    "coarse_recognition",
    "fine_evidences",
    "coarse_evidences",
    "pushed_posteriors",
    "coarse_posteriors",
    "coarse_update_A",
    "coarse_update_B",
    "sparse_conditional_tv",
    "metric_values",
    "metric_tolerances",
)
_REPO_ROOT = Path(__file__).resolve().parents[2]
_PYTHON = Path(r"C:\\Python314\\python.exe")


def _config(
    root: Path,
    *,
    collect_diagnostics: bool = True,
    render_figures: bool = False,
    atol: float = 1.0e-12,
) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": "renormalization-v2-recursive", "seed": 20260821},
        {
            "experiment": "renormalization_v2_recursive",
            "fixture": "lf4_two_parent_recursive_v1",
            "arithmetic": "exact_rational",
        },
        {
            "dtype": "float64",
            "atol": atol,
            "rtol": 1.0e-12,
            "min_spd_rcond": 1.0e-12,
            "max_frame_condition": 1.0e12,
        },
        {
            "root": root,
            "collect_diagnostics": collect_diagnostics,
            "render_figures": render_figures,
        },
    )


def _read_json(run_dir: Path, stem: str) -> dict[str, object]:
    payload = json.loads((run_dir / f"{stem}.json").read_text(encoding="utf-8"))
    assert type(payload) is dict
    return payload


def _canonical_bytes(payload: object) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def _canonical_sha256(payload: object) -> str:
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _direct_inputs(envelope: dict[str, object]) -> tuple[tuple[str, str], ...]:
    records = envelope["direct_inputs"]
    assert type(records) is list
    return tuple((record["name"], record["sha256"]) for record in records)


def _fraction(payload: object) -> Fraction:
    assert type(payload) is dict
    assert set(payload) == {"numerator", "denominator"}
    numerator = payload["numerator"]
    denominator = payload["denominator"]
    assert type(numerator) is int, "fraction numerator must be a built-in int"
    assert type(denominator) is int, (
        "fraction denominator must be a built-in int"
    )
    assert denominator > 0, "fraction denominator must be positive"
    value = Fraction(numerator, denominator)
    assert (value.numerator, value.denominator) == (numerator, denominator), (
        "fraction must be reduced and canonical"
    )
    return value


def _vector(payload: object) -> tuple[Fraction, ...]:
    assert type(payload) is list
    return tuple(_fraction(value) for value in payload)


def _matrix(payload: object) -> tuple[tuple[Fraction, ...], ...]:
    assert type(payload) is list
    return tuple(_vector(row) for row in payload)


def _law(payload: object) -> tuple[tuple[str, ...], tuple[Fraction, ...]]:
    assert type(payload) is dict
    assert set(payload) == {"labels", "masses"}
    labels = payload["labels"]
    assert type(labels) is list and all(type(label) is str for label in labels)
    return tuple(labels), _vector(payload["masses"])


def _observation(label: str) -> tuple[tuple[str, str], ...]:
    decoded = json.loads(label)
    return tuple((str(record_id), str(outcome)) for record_id, outcome in decoded)


def _semantic_subhashes(fixture: RecursiveFixture) -> dict[str, str]:
    result = dict(fixture.subrecord_sha256)
    assert tuple(result) == ("generative", "recognition", "structure", "access")
    return result


def _require_object(value: object, label: str) -> dict[str, object]:
    assert type(value) is dict, f"{label} must be an object"
    return value


def _require_list(value: object, label: str) -> list[object]:
    assert type(value) is list, f"{label} must be a list"
    return value


def _strings(value: object, label: str) -> tuple[str, ...]:
    items = _require_list(value, label)
    assert all(type(item) is str for item in items), (
        f"{label} must contain built-in strings"
    )
    return tuple(items)


def _exact_channel(value: object) -> ExactMarkovChannel:
    payload = _require_object(value, "exact channel")
    assert set(payload) == {
        "source_labels",
        "target_labels",
        "matrix",
        "recognition_independent",
    }
    assert payload["recognition_independent"] is True
    return ExactMarkovChannel(
        _strings(payload["source_labels"], "channel sources"),
        _strings(payload["target_labels"], "channel targets"),
        _matrix(payload["matrix"]),
        recognition_independent=True,
    )


def _probability_law(value: object) -> ExactProbabilityLaw:
    labels, masses = _law(value)
    return ExactProbabilityLaw(labels, masses)


def _submeasure(value: object) -> ExactSubmeasure:
    labels, masses = _law(value)
    return ExactSubmeasure(labels, masses)


def _agent_from_artifact(value: object) -> AgentDatum:
    payload = _require_object(value, "agent")
    generative_payload = _require_object(
        payload["generative_kernel"], "agent generative kernel"
    )
    generative_kernel = _exact_channel(generative_payload)
    assert payload["generative_kernel_sha256"] == _canonical_sha256(
        generative_payload
    )
    evaluations: list[ModelEvaluation] = []
    for raw in _require_list(payload["evaluator"], "agent evaluator"):
        item = _require_object(raw, "model evaluation")
        kernel_payload = _require_object(item["kernel"], "evaluator kernel")
        evaluator_kernel = _exact_channel(kernel_payload)
        assert item["kernel_sha256"] == _canonical_sha256(kernel_payload)
        assert type(item["model_label"]) is str
        evaluations.append(
            ModelEvaluation(item["model_label"], evaluator_kernel)
        )
    return AgentDatum(
        agent_id=str(payload["agent_id"]),
        parent_ids=_strings(payload["parent_ids"], "agent parent IDs"),
        belief_labels=_strings(payload["belief_labels"], "agent belief labels"),
        model_labels=_strings(payload["model_labels"], "agent model labels"),
        state_labels=_strings(payload["state_labels"], "agent state labels"),
        evaluator=tuple(evaluations),
        generative_kernel=generative_kernel,
    )


def _recognition_from_artifact(
    value: object,
    agent: AgentDatum,
) -> AgentRecognitionDatum:
    payload = _require_object(value, "recognition")
    assert payload["agent_id"] == agent.agent_id
    assert _strings(payload["belief_labels"], "recognition beliefs") == (
        agent.belief_labels
    )
    assert _strings(payload["model_labels"], "recognition models") == (
        agent.model_labels
    )
    assert _strings(payload["state_labels"], "recognition states") == (
        agent.state_labels
    )
    datum = AgentRecognitionDatum(agent, _probability_law(payload["joint"]))
    assert datum.belief_marginal == _probability_law(
        payload["belief_marginal"]
    )
    assert datum.model_marginal == _probability_law(payload["model_marginal"])
    body = {key: item for key, item in payload.items() if key != "sha256"}
    assert payload["sha256"] == _canonical_sha256(body)
    return datum


def _record_from_artifact(value: object) -> RecordDatum:
    payload = _require_object(value, "record")
    kernel_payload = _require_object(payload["kernel"], "record kernel")
    assert payload["kernel_sha256"] == _canonical_sha256(kernel_payload)
    body = {key: item for key, item in payload.items() if key != "sha256"}
    assert payload["sha256"] == _canonical_sha256(body)
    return RecordDatum(
        record_id=str(payload["record_id"]),
        owner_id=str(payload["owner_id"]),
        scope_ids=_strings(payload["scope_ids"], "record scope IDs"),
        outcome_labels=_strings(payload["outcome_labels"], "record outcomes"),
        kernel=_exact_channel(kernel_payload),
    )


def _selector_from_artifact(value: object) -> SelectorSpec:
    payload = _require_object(value, "selector")
    coupling = payload["coupling"]
    return SelectorSpec(
        str(payload["selector_id"]),
        str(payload["selector_kind"]),
        None if coupling is None else _probability_law(coupling),
    )


def _population_from_artifact(value: object) -> PopulationJoint:
    payload = _require_object(value, "population")
    return PopulationJoint(
        context_id=str(payload["context_id"]),
        agent_order=_strings(payload["agent_order"], "population agent order"),
        record_order=_strings(payload["record_order"], "population record order"),
        latent_labels=_strings(payload["latent_labels"], "population latent labels"),
        observation_labels=_strings(
            payload["observation_labels"], "population observation labels"
        ),
        joint_masses=_matrix(payload["joint_masses"]),
        construction_trace=_strings(
            payload["construction_trace"], "population construction trace"
        ),
    )


def _inference_from_artifact(
    value: object,
    population: PopulationJoint,
    agents_by_id: dict[str, AgentDatum],
) -> PopulationInference:
    payload = _require_object(value, "population inference")
    recognitions = tuple(
        _recognition_from_artifact(
            raw,
            agents_by_id[
                str(_require_object(raw, "inference recognition")["agent_id"])
            ],
        )
        for raw in _require_list(
            payload["recognitions"], "inference recognitions"
        )
    )
    return PopulationInference(
        population=population,
        observed_record=str(payload["observed_record"]),
        recognitions=recognitions,
        selector=_selector_from_artifact(payload["selector"]),
        recognition=_probability_law(payload["recognition"]),
        evidence_measure=_submeasure(payload["evidence_measure"]),
        evidence=_fraction(payload["evidence"]),
        posterior=_probability_law(payload["posterior"]),
    )


def _aggregate_from_artifact(value: object) -> AggregateDatum:
    payload = _require_object(value, "aggregate")
    return AggregateDatum(
        aggregate_id=str(payload["aggregate_id"]),
        source_agent_ids=_strings(
            payload["source_agent_ids"], "aggregate source agents"
        ),
        observed_record=str(payload["observed_record"]),
        channel_id=str(payload["channel_id"]),
        channel_sha256=str(payload["channel_sha256"]),
        observation_labels=_strings(
            payload["observation_labels"], "aggregate observations"
        ),
        target_labels=_strings(payload["target_labels"], "aggregate targets"),
        generative_joint=_matrix(payload["generative_joint"]),
        recognition=_probability_law(payload["recognition"]),
        posterior=_probability_law(payload["posterior"]),
        evidence=_fraction(payload["evidence"]),
        conditional_kl_defect=float(payload["conditional_kl_defect"]),
        kl_chain_residual=float(payload["kl_chain_residual"]),
    )


def _coarse_agent_spec_from_artifact(value: object) -> CoarseAgentSpec:
    payload = _require_object(value, "coarse agent specification")
    block_payload = _require_object(payload["block_channel"], "block channel")
    assert payload["block_channel_sha256"] == _canonical_sha256(block_payload)
    return CoarseAgentSpec(
        agent_id=str(payload["agent_id"]),
        source_agent_ids=_strings(
            payload["source_agent_ids"], "coarse source agents"
        ),
        parent_ids=_strings(payload["parent_ids"], "coarse parents"),
        source_context_id=str(payload["source_context_id"]),
        belief_labels=_strings(payload["belief_labels"], "coarse beliefs"),
        model_labels=_strings(payload["model_labels"], "coarse models"),
        state_labels=_strings(payload["state_labels"], "coarse states"),
        block_channel=_exact_channel(block_payload),
        null_row_policy=str(payload["null_row_policy"]),
    )


def _structure_from_artifact(value: object) -> RecursiveCoarseStructure:
    payload = _require_object(value, "recursive structure")
    observation_payload = _require_object(
        payload["observation_bijection"], "observation bijection"
    )
    fine_labels = _strings(
        observation_payload["fine_observation_labels"],
        "fine observation labels",
    )
    compound_labels = _strings(
        observation_payload["compound_outcome_labels"],
        "compound outcome labels",
    )
    pairs = tuple(
        _require_object(raw, "observation bijection pair")
        for raw in _require_list(
            observation_payload["fine_to_compound"],
            "observation bijection pairs",
        )
    )
    assert len(pairs) == len(fine_labels), (
        "observation bijection pairs must cover every fine observation"
    )
    assert tuple(pair.get("fine_observation") for pair in pairs) == fine_labels, (
        "observation bijection pairs must preserve fine observation order"
    )
    compounds = tuple(pair.get("compound_outcome") for pair in pairs)
    assert all(type(item) is str for item in compounds), (
        "observation bijection pairs must contain built-in strings"
    )
    assert compounds == compound_labels and len(set(compounds)) == len(compounds), (
        "observation bijection pairs must form the ordered bijection"
    )
    observation = CoarseObservationSpec(
        str(observation_payload["record_id"]),
        fine_labels,
        compound_labels,
        compounds,
    )
    sparse_payload = _require_object(
        payload["sparse_record_candidate"], "sparse record candidate"
    )
    projections = tuple(
        _require_object(raw, "sparse projection")
        for raw in _require_list(
            sparse_payload["projections"], "sparse projections"
        )
    )
    assert tuple(item.get("fine_observation") for item in projections) == (
        fine_labels
    ), "sparse projections must preserve fine observation order"
    sparse = SparseRecordFactorizationSpec(
        left_record_ids=_strings(
            sparse_payload["left_record_ids"], "sparse left records"
        ),
        right_record_ids=_strings(
            sparse_payload["right_record_ids"], "sparse right records"
        ),
        left_outcome_labels=_strings(
            sparse_payload["left_outcome_labels"], "sparse left outcomes"
        ),
        right_outcome_labels=_strings(
            sparse_payload["right_outcome_labels"], "sparse right outcomes"
        ),
        left_outcome_by_fine_observation=tuple(
            str(item["left_outcome"]) for item in projections
        ),
        right_outcome_by_fine_observation=tuple(
            str(item["right_outcome"]) for item in projections
        ),
    )
    return RecursiveCoarseStructure(
        structure_id=str(payload["structure_id"]),
        source_agent_order=_strings(
            payload["source_agent_order"], "source agent order"
        ),
        coarse_agent_order=_strings(
            payload["coarse_agent_order"], "coarse agent order"
        ),
        agent_specs=tuple(
            _coarse_agent_spec_from_artifact(raw)
            for raw in _require_list(
                payload["agent_specs"], "coarse agent specifications"
            )
        ),
        observation=observation,
        sparse_record_candidate=sparse,
    )


def _access_from_artifact(value: object) -> CoarseAccessSpec:
    payload = _require_object(value, "coarse access")
    observations = _strings(
        payload["observation_labels"], "access observation labels"
    )
    mappings = tuple(
        _require_object(raw, "access mapping")
        for raw in _require_list(
            payload["observation_to_information"], "access mappings"
        )
    )
    assert tuple(item.get("observation") for item in mappings) == observations
    information = tuple(item.get("information") for item in mappings)
    assert all(type(item) is str for item in information)
    return CoarseAccessSpec(
        agent_id=str(payload["agent_id"]),
        observation_labels=observations,
        information_labels=_strings(
            payload["information_labels"], "access information labels"
        ),
        information_by_observation=information,
        access_kind=str(payload["access_kind"]),
    )


def _coarse_channel_from_artifact(value: object) -> CoarseChannelSpec:
    payload = _require_object(value, "coarse channel")
    declaration = _require_object(payload["channel"], "coarse exact channel")
    assert payload["channel_sha256"] == _canonical_sha256(declaration)
    return CoarseChannelSpec(
        channel_id=str(payload["channel_id"]),
        source_agent_ids=_strings(
            payload["source_agent_ids"], "combined source agents"
        ),
        structural_input_ids=_strings(
            payload["structural_input_ids"], "combined structural inputs"
        ),
        channel=_exact_channel(declaration),
    )


def _raw_semantic_subhashes(
    fixture_payload: dict[str, object],
) -> dict[str, str]:
    typed_agents = tuple(
        _agent_from_artifact(raw)
        for raw in _require_list(fixture_payload["agents"], "fixture agents")
    )
    typed_agents_by_id = {agent.agent_id: agent for agent in typed_agents}
    tuple(
        _recognition_from_artifact(
            raw,
            typed_agents_by_id[
                str(_require_object(raw, "fixture recognition")["agent_id"])
            ],
        )
        for raw in _require_list(
            fixture_payload["recognitions"], "fixture recognitions"
        )
    )
    tuple(_record_from_artifact(raw) for raw in _require_list(fixture_payload["records"], "fixture records"))
    _selector_from_artifact(fixture_payload["selector"])
    _structure_from_artifact(fixture_payload["recursive_structure"])
    tuple(_access_from_artifact(raw) for raw in _require_list(fixture_payload["access_specs"], "fixture access specs"))
    raw_agents: list[dict[str, object]] = []
    for raw in _require_list(fixture_payload["agents"], "fixture agents"):
        agent = _require_object(raw, "fixture agent")
        raw_agents.append(
            {
                "agent_id": agent["agent_id"],
                "parent_ids": agent["parent_ids"],
                "belief_labels": agent["belief_labels"],
                "model_labels": agent["model_labels"],
                "generative_rows": _require_object(
                    agent["generative_kernel"], "generative kernel"
                )["matrix"],
                "evaluator": [
                    {
                        "model_label": evaluation["model_label"],
                        "rows": _require_object(
                            evaluation["kernel"], "evaluator kernel"
                        )["matrix"],
                    }
                    for evaluation in (
                        _require_object(item, "model evaluation")
                        for item in _require_list(
                            agent["evaluator"], "agent evaluator"
                        )
                    )
                ],
            }
        )
    raw_records = []
    for raw in _require_list(fixture_payload["records"], "fixture records"):
        record = _require_object(raw, "fixture record")
        raw_records.append(
            {
                "record_id": record["record_id"],
                "owner_id": record["owner_id"],
                "scope_ids": record["scope_ids"],
                "outcome_labels": record["outcome_labels"],
                "rows": _require_object(record["kernel"], "record kernel")[
                    "matrix"
                ],
            }
        )
    raw_recognitions = [
        {
            "agent_id": recognition["agent_id"],
            "masses": _require_object(
                recognition["joint"], "recognition joint"
            )["masses"],
        }
        for recognition in (
            _require_object(item, "fixture recognition")
            for item in _require_list(
                fixture_payload["recognitions"], "fixture recognitions"
            )
        )
    ]
    selector = _require_object(fixture_payload["selector"], "fixture selector")
    coupling = selector["coupling"]
    raw_selector = {
        "selector_id": selector["selector_id"],
        "selector_kind": selector["selector_kind"],
        "coupling": (
            None
            if coupling is None
            else {
                "masses": _require_object(coupling, "selector coupling")[
                    "masses"
                ]
            }
        ),
    }
    structure = _require_object(
        fixture_payload["recursive_structure"], "recursive structure"
    )
    observation = _require_object(
        structure["observation_bijection"], "observation bijection"
    )
    pairs = tuple(
        _require_object(item, "observation pair")
        for item in _require_list(
            observation["fine_to_compound"], "observation pairs"
        )
    )
    sparse = _require_object(
        structure["sparse_record_candidate"], "sparse candidate"
    )
    projections = tuple(
        _require_object(item, "sparse projection")
        for item in _require_list(sparse["projections"], "sparse projections")
    )
    raw_structure = {
        "structure_id": structure["structure_id"],
        "source_agent_order": structure["source_agent_order"],
        "coarse_agent_order": structure["coarse_agent_order"],
        "agents": [
            {
                "agent_id": spec["agent_id"],
                "source_agent_ids": spec["source_agent_ids"],
                "parent_ids": spec["parent_ids"],
                "source_context_id": spec["source_context_id"],
                "belief_labels": spec["belief_labels"],
                "model_labels": spec["model_labels"],
                "block_rows": _require_object(
                    spec["block_channel"], "block channel"
                )["matrix"],
                "null_row_policy": spec["null_row_policy"],
            }
            for spec in (
                _require_object(item, "coarse agent specification")
                for item in _require_list(
                    structure["agent_specs"], "coarse agent specifications"
                )
            )
        ],
        "observation": {
            "record_id": observation["record_id"],
            "fine_observation_labels": observation[
                "fine_observation_labels"
            ],
            "compound_outcome_labels": observation[
                "compound_outcome_labels"
            ],
            "compound_outcome_by_fine_observation": [
                pair["compound_outcome"] for pair in pairs
            ],
        },
        "sparse_record_candidate": {
            "left_record_ids": sparse["left_record_ids"],
            "right_record_ids": sparse["right_record_ids"],
            "left_outcome_labels": sparse["left_outcome_labels"],
            "right_outcome_labels": sparse["right_outcome_labels"],
            "left_outcome_by_fine_observation": [
                item["left_outcome"] for item in projections
            ],
            "right_outcome_by_fine_observation": [
                item["right_outcome"] for item in projections
            ],
        },
    }
    raw_access = []
    for raw in _require_list(
        fixture_payload["access_specs"], "fixture access specs"
    ):
        access = _require_object(raw, "fixture access")
        mappings = tuple(
            _require_object(item, "access mapping")
            for item in _require_list(
                access["observation_to_information"], "access mappings"
            )
        )
        raw_access.append(
            {
                "agent_id": access["agent_id"],
                "observation_labels": access["observation_labels"],
                "information_labels": access["information_labels"],
                "information_by_observation": [
                    item["information"] for item in mappings
                ],
                "access_kind": access["access_kind"],
            }
        )
    raw_subrecords = {
        "generative": {"agents": raw_agents, "records": raw_records},
        "recognition": {
            "recognitions": raw_recognitions,
            "selector": raw_selector,
        },
        "structure": raw_structure,
        "access": raw_access,
    }
    return {
        name: _canonical_sha256(raw_subrecords[name])
        for name in ("generative", "recognition", "structure", "access")
    }


def _literal_lf4_oracle() -> tuple[
    tuple[str, ...],
    tuple[str, ...],
    tuple[tuple[Fraction, ...], ...],
    tuple[tuple[Fraction, ...], ...],
]:
    agent_ids = ("a0", "a1", "a2", "a3")
    record_ids = ("r0", "r1", "r2", "r3")
    local_states = (
        ("b0", "m0"),
        ("b0", "m1"),
        ("b1", "m0"),
        ("b1", "m1"),
    )
    root_row = (
        Fraction(3, 8),
        Fraction(1, 8),
        Fraction(1, 8),
        Fraction(3, 8),
    )
    child_rows = (
        (Fraction(3, 5), Fraction(3, 20), Fraction(3, 20), Fraction(1, 10)),
        (Fraction(1, 5), Fraction(9, 20), Fraction(1, 20), Fraction(3, 10)),
        (Fraction(3, 10), Fraction(1, 20), Fraction(9, 20), Fraction(1, 5)),
        (Fraction(1, 10), Fraction(3, 20), Fraction(3, 20), Fraction(3, 5)),
    )
    high = (Fraction(4, 5), Fraction(1, 5))
    low = (Fraction(1, 5), Fraction(4, 5))
    observation_labels = tuple(
        json.dumps(
            [
                [record_id, str(outcome)]
                for record_id, outcome in zip(
                    record_ids, outcomes, strict=True
                )
            ],
            ensure_ascii=True,
            separators=(",", ":"),
        )
        for outcomes in product(range(2), repeat=4)
    )
    latent_labels: list[str] = []
    fine_rows: list[tuple[Fraction, ...]] = []
    coarse_rows = [
        [Fraction(0) for _ in range(16)] for _ in range(16)
    ]
    for states in product(range(4), repeat=4):
        a0, a1, a2, a3 = states
        latent_labels.append(
            json.dumps(
                [
                    [agent_id, *local_states[state]]
                    for agent_id, state in zip(
                        agent_ids, states, strict=True
                    )
                ],
                ensure_ascii=True,
                separators=(",", ":"),
            )
        )
        generative = (
            root_row[a0]
            * child_rows[a0][a1]
            * child_rows[a1][a2]
            * child_rows[a2][a3]
        )
        belief_agrees = local_states[a1][0] == local_states[a2][0]
        record_rows = (
            high if local_states[a0][0] == "b0" else low,
            high if belief_agrees else low,
            high if belief_agrees else low,
            high if local_states[a3][0] == "b0" else low,
        )
        row: list[Fraction] = []
        for observation_index, outcomes in enumerate(
            product(range(2), repeat=4)
        ):
            mass = generative
            for record_row, outcome in zip(
                record_rows, outcomes, strict=True
            ):
                mass *= record_row[outcome]
            row.append(mass)
            a_target = (
                ((a0 // 2) ^ (a1 // 2)) * 2
                + ((a0 % 2) ^ (a1 % 2))
            )
            b_target = (
                ((a2 // 2) ^ (a3 // 2)) * 2
                + ((a2 % 2) ^ (a3 % 2))
            )
            coarse_rows[a_target * 4 + b_target][
                observation_index
            ] += mass
        fine_rows.append(tuple(row))
    return (
        tuple(latent_labels),
        observation_labels,
        tuple(fine_rows),
        tuple(tuple(row) for row in coarse_rows),
    )


def _relabel_coarse_rows(
    coarse_population: object,
) -> tuple[tuple[Fraction, ...], ...]:
    structure = coarse_population.structure
    reconstructed = coarse_population.reconstructed_population
    columns = tuple(
        reconstructed.observation_labels.index(
            json.dumps(
                [[structure.observation.record_id, outcome]],
                ensure_ascii=True,
                separators=(",", ":"),
            )
        )
        for outcome in (
            structure.observation.compound_outcome_by_fine_observation
        )
    )
    return tuple(
        tuple(row[column] for column in columns)
        for row in reconstructed.joint_masses
    )


def _sparse_replay_diagnostics(
    coarse_population: object,
) -> tuple[int, Fraction]:
    sparse = coarse_population.structure.sparse_record_candidate
    pushed = coarse_population.pushed_joint
    left_indices = tuple(
        sparse.left_outcome_labels.index(value)
        for value in sparse.left_outcome_by_fine_observation
    )
    right_indices = tuple(
        sparse.right_outcome_labels.index(value)
        for value in sparse.right_outcome_by_fine_observation
    )
    conditionals = []
    left_marginals = []
    right_marginals = []
    for pushed_row in pushed.joint_masses:
        denominator = sum(pushed_row, Fraction(0))
        assert denominator > 0
        joint = [
            [Fraction(0) for _ in sparse.right_outcome_labels]
            for _ in sparse.left_outcome_labels
        ]
        for index, mass in enumerate(pushed_row):
            joint[left_indices[index]][right_indices[index]] += (
                mass / denominator
            )
        exact = tuple(tuple(row) for row in joint)
        conditionals.append(exact)
        left_marginals.append(
            tuple(sum(row, Fraction(0)) for row in exact)
        )
        right_marginals.append(
            tuple(
                sum(
                    (exact[left][right] for left in range(4)),
                    Fraction(0),
                )
                for right in range(4)
            )
        )
    violations = 0
    for a_index in range(4):
        for left_b, right_b in combinations(range(4), 2):
            for outcome in range(4):
                violations += int(
                    left_marginals[a_index * 4 + left_b][outcome]
                    != left_marginals[a_index * 4 + right_b][outcome]
                )
    for b_index in range(4):
        for left_a, right_a in combinations(range(4), 2):
            for outcome in range(4):
                violations += int(
                    right_marginals[left_a * 4 + b_index][outcome]
                    != right_marginals[right_a * 4 + b_index][outcome]
                )
    maximum_tv = Fraction(0)
    for latent_index, joint in enumerate(conditionals):
        tv = Fraction(0)
        for left in range(4):
            for right in range(4):
                product_mass = (
                    left_marginals[latent_index][left]
                    * right_marginals[latent_index][right]
                )
                difference = joint[left][right] - product_mass
                violations += int(difference != 0)
                tv += abs(difference)
        maximum_tv = max(maximum_tv, tv / 2)
    return violations, maximum_tv


_METRIC_INTERPRETATIONS = {
    "block_channel_normalization_residual": "Every declared block-channel row is normalized exactly.",
    "coarse_state_interpretation_violation_count": "Each coarse state support is the declared belief-major Cartesian interpretation.",
    "observation_bijection_violation_count": "The fine-to-compound observation declaration is an ordered bijection.",
    "coarse_agent_kernel_normalization_residual": "Every constructed coarse-agent generative row is normalized exactly.",
    "coarse_evaluator_compatibility_residual": "Every positive coarse model slice agrees with its evaluator.",
    "coarse_record_kernel_normalization_residual": "The dense combined record is normalized row by row.",
    "coarse_population_normalization_residual": "The reconstructed coarse population is normalized exactly.",
    "generative_roundtrip_residual": "Constructor, runtime oracle, pushforward, and reconstructed generative tables agree entrywise.",
    "recognition_marginal_residual": "Each attached local recognition law is the exact marginal of the pushed joint.",
    "recognition_roundtrip_residual": "Directly pushed and reconstructed coarse recognition laws agree for all observations.",
    "evidence_roundtrip_residual": "Fine and relabeled coarse evidence agree for all observations.",
    "posterior_roundtrip_residual": "Directly pushed and reconstructed coarse posteriors agree for all observations.",
    "access_descent_residual": "Identity access descends the all-observation update table exactly.",
    "update_normalization_residual": "Every exact Bayesian update row is normalized.",
    "update_posterior_residual": "Every realized update row equals its coarse posterior marginal.",
    "coarse_model_marginal_non_dirac_count": "Both constructed parents retain non-Dirac model-recognition marginals.",
    "forbidden_dependency_violation_count": "The generative publication path has no recognition, selector, realized-observation, evidence, or posterior dependency.",
    "sparse_record_factorization_violation_count": "The declared sparse record family fails at least one exact factorization identity.",
    "minimum_conditional_kl_defect": "Every terminal common-channel conditional KL defect respects data processing within the declared float boundary.",
    "maximum_kl_chain_residual": "Every terminal common-channel KL chain residual stays within the declared float boundary.",
}
_STANDARD_EXACT_METRICS = {
    "block_channel_normalization_residual",
    "coarse_agent_kernel_normalization_residual",
    "coarse_evaluator_compatibility_residual",
    "coarse_record_kernel_normalization_residual",
    "coarse_population_normalization_residual",
}
_LOWER_BOUNDED_METRICS = {
    "coarse_model_marginal_non_dirac_count",
    "sparse_record_factorization_violation_count",
}
_FLOAT_BOUNDARY_METRICS = {
    "minimum_conditional_kl_defect",
    "maximum_kl_chain_residual",
}
_METRIC_RECORD_KEYS = {
    "value",
    "tolerance",
    "status",
    "interpretation",
    "assessment_scope",
    "theorem_status",
    "verification_state",
    "claim_origin",
}


def _expected_metric_records(
    values: dict[str, float],
) -> dict[str, dict[str, object]]:
    inventory = EXPERIMENT_REGISTRY[
        "renormalization_v2_recursive"
    ].metric_inventory
    expected: dict[str, dict[str, object]] = {}
    for name in inventory:
        lower_bounded = name in _LOWER_BOUNDED_METRICS
        standard = (
            name in _STANDARD_EXACT_METRICS
            or name in _FLOAT_BOUNDARY_METRICS
        )
        expected[name] = {
            "value": float(values[name]),
            "tolerance": 0.0,
            "status": "pass",
            "interpretation": _METRIC_INTERPRETATIONS[name],
            "assessment_scope": "implementation_check",
            "theorem_status": "HYPOTHESIS" if lower_bounded else "ESTABLISHED",
            "verification_state": "CANDIDATE",
            "claim_origin": (
                "APPLICATION_SPECIFIC"
                if lower_bounded
                else ("STANDARD" if standard else "PROJECT_NOVEL")
            ),
        }
    return expected


def _recursive_metric_records(
    envelope: dict[str, object],
) -> dict[str, dict[str, object]]:
    payload = _require_object(envelope["payload"], "metrics payload")
    raw_records = _require_list(payload["records"], "metric records")
    inventory = EXPERIMENT_REGISTRY[
        "renormalization_v2_recursive"
    ].metric_inventory
    assert len(raw_records) == 20, (
        "metrics artifact must contain exactly twenty raw records"
    )
    records = tuple(
        _require_object(record, "metric record") for record in raw_records
    )
    assert all(set(record) == {"name", "record"} for record in records), (
        "metric record envelope keys must be exact"
    )
    assert all(type(record.get("name")) is str for record in records), (
        "metric record names must be built-in strings"
    )
    names = tuple(record["name"] for record in records)
    assert len(set(names)) == len(names), (
        "metric record names must be unique"
    )
    assert names == inventory, (
        "metric record names must match the exact ordered inventory"
    )
    return {
        name: _require_object(record["record"], "serialized MetricRecord")
        for name, record in zip(names, records, strict=True)
    }


def _manifest_direct_inputs(
    value: object,
    label: str,
) -> tuple[tuple[str, str], ...]:
    records = tuple(
        _require_object(item, label)
        for item in _require_list(value, label)
    )
    assert all(set(record) == {"name", "sha256"} for record in records), (
        f"{label} keys mismatch"
    )
    assert all(
        type(record["name"]) is str
        and type(record["sha256"]) is str
        and len(record["sha256"]) == 64
        and all(
            character in "0123456789abcdef"
            for character in record["sha256"]
        )
        for record in records
    ), f"{label} must contain named lowercase SHA-256 records"
    return tuple(
        (record["name"], record["sha256"]) for record in records
    )


def _replay_finalized_recursive_run(run_dir: Path) -> None:
    run_dir = run_dir.resolve()
    assert run_dir.is_dir(), "replay accepts only a finalized run directory"
    expected_files = set(_CORE_FILES + _ARTIFACT_FILES)
    assert {path.name for path in run_dir.iterdir()} == expected_files
    manifest = _read_json(run_dir, "manifest")
    config_document = _read_json(run_dir, "config")
    assert set(manifest) == {
        "config_hash",
        "provenance",
        "artifacts",
        "complete",
    }, "manifest keys mismatch"
    provenance = _require_object(
        manifest["provenance"], "manifest provenance"
    )
    assert set(provenance) == {
        "config_hash",
        "git_commit",
        "git_dirty",
        "git_status_format",
        "git_status_sha256",
        "dirty_tree_format",
        "dirty_tree_sha256",
        "theory_root",
        "theory_exists",
        "theory_digest_format",
        "theory_sha256",
        "input_hashes",
        "python_version",
        "numpy_version",
        "scipy_version",
        "platform",
        "rng",
        "experiment_scope",
        "fixture_id",
        "arithmetic",
        "effective_backend",
        "effective_dtype",
        "semantic_artifact_sha256",
        "arrays_direct_inputs",
    }, "manifest provenance keys mismatch"
    input_hashes = _require_object(
        provenance["input_hashes"], "manifest input hashes"
    )
    assert set(input_hashes) == {
        "resolved_config_sha256",
        "theory_tree_sha256",
        "fixture_direct_inputs",
        "semantic_artifacts",
    }, "manifest input_hashes keys mismatch"
    assert manifest["complete"] is True
    assert manifest["artifacts"] == {
        filename: "complete" for filename in sorted(expected_files)
    }

    resolved = _require_object(
        config_document["resolved_config"], "resolved configuration"
    )
    config = ExperimentConfig.from_dicts(
        _require_object(resolved["run"], "run configuration"),
        _require_object(resolved["theory"], "theory configuration"),
        _require_object(resolved["numerics"], "numerics configuration"),
        _require_object(resolved["output"], "output configuration"),
        (
            None
            if "compute" not in resolved
            else _require_object(
                resolved["compute"], "compute configuration"
            )
        ),
    )
    assert config_sha256(config) == config_document["config_hash"]
    assert manifest["config_hash"] == config_document["config_hash"]

    envelopes = {
        name: _read_json(run_dir, name) for name in _JSON_STEMS
    }
    stored_metric_records = _recursive_metric_records(envelopes["metrics"])
    fixture_payload = _require_object(
        envelopes["fixture_snapshot"]["payload"], "fixture payload"
    )
    boundary_structure = _structure_from_artifact(
        fixture_payload["recursive_structure"]
    )
    raw_observation_payload = _require_object(
        envelopes["all_observation_inference"]["payload"],
        "all-observation payload",
    )
    raw_observations = tuple(
        _require_object(raw, "observation result")
        for raw in _require_list(
            raw_observation_payload["observations"], "observation results"
        )
    )
    assert len(raw_observations) == 16
    boundary_mapping = dict(
        zip(
            boundary_structure.observation.fine_observation_labels,
            boundary_structure.observation.compound_outcome_by_fine_observation,
            strict=True,
        )
    )
    for fine_label, stored in zip(
        boundary_structure.observation.fine_observation_labels,
        raw_observations,
        strict=True,
    ):
        expected_coarse = json.dumps(
            [[boundary_structure.observation.record_id, boundary_mapping[fine_label]]],
            ensure_ascii=True,
            separators=(",", ":"),
        )
        assert (
            stored.get("fine_observed_record"),
            stored.get("coarse_observed_record"),
        ) == (fine_label, expected_coarse), (
            "observation result pairs must preserve the declared ordered bijection"
        )
    fixture_id = str(envelopes["fixture_snapshot"]["fixture_id"])
    producer_commit = str(
        envelopes["fixture_snapshot"]["producer_commit"]
    )
    config_hash = str(envelopes["fixture_snapshot"]["config_hash"])
    for envelope in envelopes.values():
        assert (
            envelope["schema_version"]
            == "rg-v2-recursive-phase2-artifact-v1"
        )
        assert envelope["fixture_id"] == fixture_id
        assert envelope["producer_commit"] == producer_commit
        assert envelope["config_hash"] == config_hash
    assert fixture_id == "lf4_two_parent_recursive_v1"
    assert config_hash == config_document["config_hash"]
    assert producer_commit == provenance["git_commit"]

    hashes = {
        name: _canonical_sha256(envelope)
        for name, envelope in envelopes.items()
    }
    semantic_subrecords = tuple(
        (
            str(_require_object(raw, "semantic subrecord")["name"]),
            str(_require_object(raw, "semantic subrecord")["sha256"]),
        )
        for raw in _require_list(
            fixture_payload["semantic_subrecords"],
            "semantic subrecords",
        )
    )
    recomputed_subhashes = _raw_semantic_subhashes(fixture_payload)
    assert semantic_subrecords == tuple(recomputed_subhashes.items()), (
        "semantic subrecord hashes must replay from embedded semantics"
    )
    raw_fixture_sha256 = str(fixture_payload["fixture_sha256"])
    assert len(raw_fixture_sha256) == 64 and all(
        character in "0123456789abcdef"
        for character in raw_fixture_sha256
    ), "raw fixture SHA-256 must be a lowercase provenance digest"
    fixture_inputs = (
        ("fixture_raw", raw_fixture_sha256),
        *semantic_subrecords,
    )
    assert _direct_inputs(envelopes["fixture_snapshot"]) == fixture_inputs, (
        "fixture_snapshot direct-input DAG mismatch"
    )
    assert _manifest_direct_inputs(
        input_hashes["fixture_direct_inputs"], "manifest fixture_direct_inputs"
    ) == fixture_inputs, "manifest fixture_direct_inputs mismatch"
    assert _direct_inputs(envelopes["fine_population"]) == (
        ("generative", recomputed_subhashes["generative"]),
    ), "fine_population direct-input DAG mismatch"
    assert _direct_inputs(envelopes["coarse_generative"]) == (
        ("fine_population", hashes["fine_population"]),
        ("structure", recomputed_subhashes["structure"]),
    ), "coarse_generative direct-input DAG mismatch"
    assert _direct_inputs(envelopes["coarse_interfaces"]) == (
        ("coarse_generative", hashes["coarse_generative"]),
        ("access", recomputed_subhashes["access"]),
        ("recognition", recomputed_subhashes["recognition"]),
    ), "coarse_interfaces direct-input DAG mismatch"
    assert _direct_inputs(envelopes["coarse_population"]) == (
        ("coarse_generative", hashes["coarse_generative"]),
    ), "coarse_population direct-input DAG mismatch"
    assert _direct_inputs(envelopes["all_observation_inference"]) == (
        ("fine_population", hashes["fine_population"]),
        ("coarse_interfaces", hashes["coarse_interfaces"]),
        ("coarse_population", hashes["coarse_population"]),
    ), "all-observation direct-input DAG mismatch"
    scientific_names = _JSON_STEMS[:-1]
    assert _direct_inputs(envelopes["metrics"]) == tuple(
        (name, hashes[name]) for name in scientific_names
    ), "metrics direct-input DAG mismatch"

    agents = tuple(
        _agent_from_artifact(raw)
        for raw in _require_list(fixture_payload["agents"], "fixture agents")
    )
    agents_by_id = {agent.agent_id: agent for agent in agents}
    assert len(agents_by_id) == len(agents) == 4
    records = tuple(
        _record_from_artifact(raw)
        for raw in _require_list(
            fixture_payload["records"], "fixture records"
        )
    )
    assert len(records) == 4
    recognitions = tuple(
        _recognition_from_artifact(
            raw,
            agents_by_id[
                str(_require_object(raw, "fixture recognition")["agent_id"])
            ],
        )
        for raw in _require_list(
            fixture_payload["recognitions"], "fixture recognitions"
        )
    )
    selector = _selector_from_artifact(fixture_payload["selector"])
    structure = _structure_from_artifact(
        fixture_payload["recursive_structure"]
    )
    access_specs = tuple(
        _access_from_artifact(raw)
        for raw in _require_list(
            fixture_payload["access_specs"], "fixture access specs"
        )
    )
    assert tuple(access.agent_id for access in access_specs) == (
        structure.coarse_agent_order
    )

    fine_population = construct_population_joint(
        agents, records, str(fixture_payload["context_id"])
    )
    runtime_fine = enumerate_population_joint_independently(
        agents, records, str(fixture_payload["context_id"])
    )
    (
        literal_latent,
        literal_observations,
        literal_fine,
        literal_coarse,
    ) = _literal_lf4_oracle()
    assert (
        fine_population.latent_labels
        == runtime_fine.latent_labels
        == literal_latent
    )
    assert (
        fine_population.observation_labels
        == runtime_fine.observation_labels
        == literal_observations
    )
    assert (
        fine_population.joint_masses
        == runtime_fine.joint_masses
        == literal_fine
    )
    assert sum(len(row) for row in literal_fine) == 4096
    fine_payload = _require_object(
        envelopes["fine_population"]["payload"], "fine population payload"
    )
    assert _population_from_artifact(
        fine_payload["population"]
    ) == fine_population
    assert _population_from_artifact(
        fine_payload["independent_population"]
    ) == runtime_fine
    assert fine_payload["exact_equality"] is True
    assert _strings(
        fine_payload["factor_trace"], "fine factor trace"
    ) == fine_population.construction_trace

    coarse_population = construct_coarse_population_joint(
        fine_population, structure
    )
    runtime_coarse = _enumerate_coarse_population_independently(
        fine_population, structure
    )
    assert coarse_population == runtime_coarse
    assert (
        coarse_population.pushed_joint.joint_masses
        == runtime_coarse.pushed_joint.joint_masses
        == literal_coarse
    )
    assert _relabel_coarse_rows(coarse_population) == literal_coarse
    assert sum(len(row) for row in literal_coarse) == 256

    coarse_generative = _require_object(
        envelopes["coarse_generative"]["payload"],
        "coarse generative payload",
    )
    _assert_no_forbidden_generative_fields(coarse_generative)
    assert coarse_generative["structure_id"] == structure.structure_id
    assert _strings(
        coarse_generative["source_agent_order"], "source agent order"
    ) == structure.source_agent_order
    assert _strings(
        coarse_generative["coarse_agent_order"], "coarse agent order"
    ) == structure.coarse_agent_order
    assert tuple(
        _coarse_agent_spec_from_artifact(raw)
        for raw in _require_list(
            coarse_generative["parent_specifications"],
            "parent specifications",
        )
    ) == structure.agent_specs
    assert _coarse_channel_from_artifact(
        coarse_generative["combined_channel"]
    ) == coarse_population.combined_channel
    generative_payloads = tuple(
        _require_object(raw, "coarse generative datum")
        for raw in _require_list(
            coarse_generative["generative_agents"],
            "coarse generative agents",
        )
    )
    for raw, expected in zip(
        generative_payloads,
        coarse_population.generative_agents,
        strict=True,
    ):
        assert _coarse_agent_spec_from_artifact(raw["spec"]) == expected.spec
        assert _agent_from_artifact(raw["agent"]) == expected.agent
        assert raw["source_population_sha256"] == (
            expected.source_population_sha256
        )
        assert raw["block_channel_sha256"] == expected.block_channel_sha256
        assert raw["combined_channel_sha256"] == (
            expected.combined_channel_sha256
        )
    assert _record_from_artifact(
        coarse_generative["combined_record"]
    ) == coarse_population.records[0]

    coarse_population_payload = _require_object(
        envelopes["coarse_population"]["payload"],
        "coarse population payload",
    )
    pushed = _require_object(
        coarse_population_payload["pushed_joint"], "pushed joint"
    )
    assert str(pushed["context_id"]) == coarse_population.pushed_joint.context_id
    assert _strings(
        pushed["latent_labels"], "pushed latent labels"
    ) == coarse_population.pushed_joint.latent_labels
    assert _strings(
        pushed["fine_observation_labels"], "pushed observation labels"
    ) == coarse_population.pushed_joint.fine_observation_labels
    assert _matrix(
        pushed["joint_masses"]
    ) == coarse_population.pushed_joint.joint_masses
    assert pushed["combined_channel_sha256"] == (
        coarse_population.pushed_joint.combined_channel_sha256
    )
    assert _population_from_artifact(
        coarse_population_payload["reconstructed_population"]
    ) == coarse_population.reconstructed_population
    runtime_pushed = _require_object(
        coarse_population_payload["runtime_oracle_pushed_joint"],
        "runtime oracle pushed joint",
    )
    assert _matrix(runtime_pushed["joint_masses"]) == (
        runtime_coarse.pushed_joint.joint_masses
    )
    assert coarse_population_payload["relabeled_cellwise_equality"] is True
    assert coarse_population_payload["dense_record_result"] == "pass"
    sparse_count, sparse_tv = _sparse_replay_diagnostics(
        coarse_population
    )
    assert sparse_count > 0 and sparse_tv > 0
    assert coarse_population_payload[
        "sparse_record_factorization_violation_count"
    ] == sparse_count
    assert _fraction(
        coarse_population_payload[
            "maximum_exact_conditional_tv_violation"
        ]
    ) == sparse_tv

    information = construct_coarse_information_interfaces(
        coarse_population, access_specs
    )
    interface_payload = _require_object(
        envelopes["coarse_interfaces"]["payload"],
        "coarse interfaces payload",
    )
    stored_interfaces = tuple(
        _require_object(raw, "coarse interface")
        for raw in _require_list(
            interface_payload["interfaces"], "coarse interfaces"
        )
    )
    assert len(stored_interfaces) == len(information) == 2
    for raw, expected in zip(
        stored_interfaces, information, strict=True
    ):
        raw_information = _require_object(
            raw["information"], "stored information"
        )
        assert _access_from_artifact(
            raw_information["access"]
        ) == expected.access
        update = _require_object(
            raw_information["update"], "stored update"
        )
        assert update["agent_id"] == expected.update.agent_id
        assert update["update_kind"] == expected.update.update_kind
        assert _exact_channel(update["kernel"]) == expected.update.kernel
        assert update["source_population_sha256"] == (
            expected.update.source_population_sha256
        )
        assert update["access_sha256"] == expected.update.access_sha256

    all_observation_payload = _require_object(
        envelopes["all_observation_inference"]["payload"],
        "all-observation payload",
    )
    stored_observations = tuple(
        _require_object(raw, "observation result")
        for raw in _require_list(
            all_observation_payload["observations"],
            "observation results",
        )
    )
    assert len(stored_observations) == 16
    aggregates: list[AggregateDatum] = []
    first_coarse_agents = None
    first_coarse_selector = None
    mapping = dict(
        zip(
            structure.observation.fine_observation_labels,
            structure.observation.compound_outcome_by_fine_observation,
            strict=True,
        )
    )
    for fine_label, stored in zip(
        structure.observation.fine_observation_labels,
        stored_observations,
        strict=True,
    ):
        assert stored["fine_observed_record"] == fine_label, (
            "observation result pairs must preserve fine observation order"
        )
        expected_coarse_label = json.dumps(
            [
                [
                    structure.observation.record_id,
                    mapping[fine_label],
                ]
            ],
            ensure_ascii=True,
            separators=(",", ":"),
        )
        assert stored["coarse_observed_record"] == expected_coarse_label, (
            "observation result pairs must preserve the declared bijection"
        )
        fine_inference = derive_population_inference(
            fine_population,
            _observation(fine_label),
            recognitions,
            selector,
        )
        assert _inference_from_artifact(
            stored["fine_inference"],
            fine_population,
            agents_by_id,
        ) == fine_inference
        coarse_agents = construct_coarse_recognition(
            coarse_population, information, fine_inference
        )
        recursive = derive_recursive_observation(
            coarse_population, coarse_agents, fine_inference
        )
        validate_recursive_observation(
            recursive, coarse_population, config.numerics
        )
        coarse_agent_map = {
            datum.generative.agent.agent_id: datum.generative.agent
            for datum in coarse_agents
        }
        assert _inference_from_artifact(
            stored["coarse_inference"],
            coarse_population.reconstructed_population,
            coarse_agent_map,
        ) == recursive.coarse_inference
        assert _fraction(stored["fine_evidence"]) == fine_inference.evidence
        assert _fraction(stored["coarse_evidence"]) == (
            recursive.coarse_inference.evidence
        )
        assert _probability_law(
            stored["pushed_recognition"]
        ) == recursive.pushed_recognition
        assert _probability_law(
            stored["coarse_recognition"]
        ) == recursive.coarse_inference.recognition
        assert _probability_law(
            stored["pushed_posterior"]
        ) == recursive.pushed_posterior
        assert _probability_law(
            stored["coarse_posterior"]
        ) == recursive.coarse_inference.posterior
        assert _fraction(stored["recognition_roundtrip_residual"]) == 0
        assert _fraction(stored["evidence_roundtrip_residual"]) == 0
        assert _fraction(stored["posterior_roundtrip_residual"]) == 0
        for raw_access, datum in zip(
            _require_list(stored["access_values"], "access values"),
            coarse_agents,
            strict=True,
        ):
            access_value = _require_object(raw_access, "access value")
            assert access_value["agent_id"] == datum.generative.agent.agent_id
            index = datum.information.access.observation_labels.index(
                expected_coarse_label
            )
            assert access_value["information"] == (
                datum.information.access.information_by_observation[index]
            )
        for raw_update, datum in zip(
            _require_list(stored["update_rows"], "update rows"),
            coarse_agents,
            strict=True,
        ):
            update = _require_object(raw_update, "update row")
            assert update["agent_id"] == datum.generative.agent.agent_id
            index = datum.information.access.information_labels.index(
                expected_coarse_label
            )
            assert _vector(update["masses"]) == (
                datum.information.update.kernel.matrix[index]
            )
        aggregate = aggregate_population(
            fine_inference, coarse_population.combined_channel, config.numerics
        )
        assert _aggregate_from_artifact(
            stored["terminal_common_channel_aggregate"]
        ) == aggregate
        aggregates.append(aggregate)
        if first_coarse_agents is None:
            first_coarse_agents = coarse_agents
            first_coarse_selector = recursive.coarse_inference.selector

    assert first_coarse_agents is not None
    assert first_coarse_selector is not None
    for raw, datum in zip(
        stored_interfaces, first_coarse_agents, strict=True
    ):
        recognition = _require_object(
            raw["initial_recognition"], "stored coarse recognition"
        )
        assert recognition["agent_id"] == datum.generative.agent.agent_id
        assert _recognition_from_artifact(
            recognition["initial_recognition"],
            datum.generative.agent,
        ) == datum.recognition.initial_recognition
        assert _exact_channel(
            recognition["recognition_kernel"]
        ) == datum.recognition.recognition_kernel
        assert recognition["source_recognition_sha256"] == (
            datum.recognition.source_recognition_sha256
        )
    assert _selector_from_artifact(
        interface_payload["declared_correlated_selector"]
    ) == first_coarse_selector

    inventory = EXPERIMENT_REGISTRY[
        "renormalization_v2_recursive"
    ].metric_inventory
    expected_values = {name: 0.0 for name in inventory[:15]}
    expected_values.update(
        {
            "coarse_model_marginal_non_dirac_count": 2.0,
            "forbidden_dependency_violation_count": 0.0,
            "sparse_record_factorization_violation_count": float(
                sparse_count
            ),
            "minimum_conditional_kl_defect": min(
                item.conditional_kl_defect for item in aggregates
            ),
            "maximum_kl_chain_residual": max(
                abs(item.kl_chain_residual) for item in aggregates
            ),
        }
    )
    expected_metric_records = _expected_metric_records(expected_values)
    for name in inventory:
        record = stored_metric_records[name]
        assert set(record) == _METRIC_RECORD_KEYS, (
            "serialized MetricRecord mismatch: exact keys"
        )
        assert type(record["value"]) is float, (
            "serialized MetricRecord mismatch: value type"
        )
        assert type(record["tolerance"]) is float, (
            "serialized MetricRecord mismatch: tolerance type"
        )
        assert all(
            type(record[key]) is str
            for key in _METRIC_RECORD_KEYS - {"value", "tolerance"}
        ), "serialized MetricRecord mismatch: string field type"
        assert record == expected_metric_records[name], (
            f"serialized MetricRecord mismatch: {name}"
        )

    array_inputs = tuple(
        (name, hashes[name]) for name in (*scientific_names, "metrics")
    )
    assert _strings(
        provenance["arrays_direct_inputs"], "manifest arrays_direct_inputs"
    ) == tuple(name for name, _ in array_inputs), (
        "manifest arrays_direct_inputs mismatch"
    )
    expected_float_arrays = {
        "fine_population": np.asarray(literal_fine, dtype=np.float64),
        "fine_population_oracle": np.asarray(
            runtime_fine.joint_masses, dtype=np.float64
        ),
        "coarse_pushed_population": np.asarray(
            literal_coarse, dtype=np.float64
        ),
        "coarse_reconstructed_population": np.asarray(
            _relabel_coarse_rows(coarse_population), dtype=np.float64
        ),
    }
    expected_float_arrays["fine_recognition"] = np.asarray(
        [
            float(value)
            for value in _probability_law(
                _require_object(
                    stored_observations[0]["fine_inference"],
                    "first fine inference",
                )["recognition"]
            ).masses
        ],
        dtype=np.float64,
    )
    expected_float_arrays.update(
        {
            "coarse_recognition": np.asarray(
                [
                    float(value)
                    for value in _probability_law(
                        stored_observations[0]["pushed_recognition"]
                    ).masses
                ],
                dtype=np.float64,
            ),
            "fine_evidences": np.asarray(
                [
                    float(_fraction(item["fine_evidence"]))
                    for item in stored_observations
                ],
                dtype=np.float64,
            ),
            "coarse_evidences": np.asarray(
                [
                    float(_fraction(item["coarse_evidence"]))
                    for item in stored_observations
                ],
                dtype=np.float64,
            ),
            "pushed_posteriors": np.asarray(
                [
                    [
                        float(value)
                        for value in _probability_law(
                            item["pushed_posterior"]
                        ).masses
                    ]
                    for item in stored_observations
                ],
                dtype=np.float64,
            ),
            "coarse_posteriors": np.asarray(
                [
                    [
                        float(value)
                        for value in _probability_law(
                            item["coarse_posterior"]
                        ).masses
                    ]
                    for item in stored_observations
                ],
                dtype=np.float64,
            ),
            "coarse_update_A": np.asarray(
                information[0].update.kernel.matrix, dtype=np.float64
            ),
            "coarse_update_B": np.asarray(
                information[1].update.kernel.matrix, dtype=np.float64
            ),
            "sparse_conditional_tv": np.asarray(
                sparse_tv, dtype=np.float64
            ),
            "metric_values": np.asarray(
                [expected_values[name] for name in inventory],
                dtype=np.float64,
            ),
            "metric_tolerances": np.zeros(20, dtype=np.float64),
        }
    )
    expected_array_names = (*_PROVENANCE_ARRAYS, *_FLOAT_ARRAYS)
    with np.load(run_dir / "arrays.npz", allow_pickle=False) as archive:
        assert tuple(archive.files) == expected_array_names
        loaded = {name: archive[name] for name in archive.files}
        assert all(array.dtype != object for array in loaded.values()), (
            "NPZ mirrors must not use object dtype"
        )
        for name in _PROVENANCE_ARRAYS:
            assert loaded[name].dtype.kind == "U"
        assert str(loaded["schema_version"].item()) == (
            "rg-v2-recursive-phase2-artifact-v1"
        )
        assert str(loaded["fixture_id"].item()) == fixture_id
        assert str(loaded["producer_commit"].item()) == producer_commit
        assert str(loaded["config_hash"].item()) == config_hash
        assert tuple(loaded["direct_input_names"].tolist()) == tuple(
            name for name, _ in array_inputs
        )
        assert tuple(loaded["direct_input_sha256"].tolist()) == tuple(
            sha256 for _, sha256 in array_inputs
        )
        for name, expected in expected_float_arrays.items():
            assert loaded[name].dtype == np.float64
            np.testing.assert_array_equal(loaded[name], expected)
        logical_arrays = {
            "arrays": [
                {
                    "name": name,
                    "dtype": loaded[name].dtype.str,
                    "shape": list(loaded[name].shape),
                    "values": loaded[name].tolist(),
                }
                for name in sorted(loaded)
            ]
        }
    semantic_hash_values = {
        **hashes,
        "arrays": _canonical_sha256(logical_arrays),
    }
    expected_semantic_hashes = {
        name: semantic_hash_values[name]
        for name in sorted(semantic_hash_values)
    }
    semantic_hashes = _require_object(
        provenance["semantic_artifact_sha256"], "manifest semantic hashes"
    )
    assert tuple(semantic_hashes) == tuple(expected_semantic_hashes) and (
        semantic_hashes == expected_semantic_hashes
    ), "manifest semantic_artifact_sha256 mismatch"
    input_semantic_hashes = _require_object(
        input_hashes["semantic_artifacts"],
        "manifest input semantic hashes",
    )
    assert tuple(input_semantic_hashes) == tuple(expected_semantic_hashes) and (
        input_semantic_hashes == expected_semantic_hashes
    ), "manifest input semantic_artifacts mismatch"


def _assert_no_forbidden_generative_fields(value: object) -> None:
    forbidden = {
        "access",
        "access_specs",
        "update",
        "updates",
        "recognition",
        "recognitions",
        "selector",
        "realized_observation",
        "observed_record",
        "evidence",
        "evidence_measure",
        "posterior",
    }
    if type(value) is dict:
        assert forbidden.isdisjoint(value)
        for child in value.values():
            _assert_no_forbidden_generative_fields(child)
    elif type(value) is list:
        for child in value:
            _assert_no_forbidden_generative_fields(child)


def _passing_science_values() -> dict[str, Fraction | int | float]:
    inventory = EXPERIMENT_REGISTRY["renormalization_v2_recursive"].metric_inventory
    values: dict[str, Fraction | int | float] = {
        name: Fraction(0) for name in inventory[:15]
    }
    values.update(
        {
            "coarse_model_marginal_non_dirac_count": 2,
            "forbidden_dependency_violation_count": 0,
            "sparse_record_factorization_violation_count": 1,
            "minimum_conditional_kl_defect": 0.0,
            "maximum_kl_chain_residual": 0.0,
        }
    )
    return values


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("block_channel_normalization_residual", Fraction(1, 10**400)),
        ("forbidden_dependency_violation_count", 1),
        ("coarse_model_marginal_non_dirac_count", 1),
        ("sparse_record_factorization_violation_count", 0),
    ],
)
def test_exact_metric_classes_fail_closed_before_float_conversion(
    name: str,
    value: Fraction | int,
) -> None:
    values = _passing_science_values()
    values[name] = value

    records = experiment_module._metric_records(values)

    assert tuple(records) == EXPERIMENT_REGISTRY[
        "renormalization_v2_recursive"
    ].metric_inventory
    assert records[name].status == "fail"
    assert records["minimum_conditional_kl_defect"].status == "pass"
    assert records["maximum_kl_chain_residual"].status == "pass"
    if isinstance(value, Fraction):
        assert records[name].value == 0.0


def test_generative_bodies_freeze_before_information_or_inference(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events: list[str] = []
    real_json_native = experiment_module._json_native
    real_information = experiment_module.construct_coarse_information_interfaces
    real_inference = experiment_module.derive_population_inference

    def traced_json_native(payload: object) -> dict[str, object]:
        frozen = real_json_native(payload)
        if set(frozen) >= {"population", "independent_population", "exact_equality"}:
            events.append("fine_population_frozen")
        if set(frozen) >= {"generative_agents", "combined_record", "combined_channel"}:
            events.append("coarse_generative_frozen")
        return frozen

    def traced_information(*args: object) -> object:
        assert events[:2] == [
            "fine_population_frozen",
            "coarse_generative_frozen",
        ]
        events.append("information")
        return real_information(*args)

    def traced_inference(*args: object) -> object:
        assert events[:2] == [
            "fine_population_frozen",
            "coarse_generative_frozen",
        ]
        events.append("inference")
        return real_inference(*args)

    monkeypatch.setattr(experiment_module, "_json_native", traced_json_native)
    monkeypatch.setattr(
        experiment_module,
        "construct_coarse_information_interfaces",
        traced_information,
    )
    monkeypatch.setattr(
        experiment_module,
        "derive_population_inference",
        traced_inference,
    )

    run_renormalization_v2_recursive_experiment(_config(tmp_path))

    assert events[:3] == [
        "fine_population_frozen",
        "coarse_generative_frozen",
        "information",
    ]
    assert "inference" in events[3:]


def test_narrow_generative_builder_and_dependency_audit_ignore_inference_mutations() -> None:
    fixture = load_recursive_fixture("lf4_two_parent_recursive_v1")
    fine_population = construct_population_joint(
        fixture.agents, fixture.records, fixture.context_id
    )
    coarse_population = construct_coarse_population_joint(
        fine_population, fixture.structure
    )
    assert tuple(
        inspect.signature(experiment_module._build_coarse_generative_body).parameters
    ) == ("structure", "coarse_population")
    body = experiment_module._build_coarse_generative_body(
        fixture.structure, coarse_population
    )
    canonical = _canonical_bytes(body)
    sha256 = _canonical_sha256(body)

    first = derive_population_inference(
        fine_population,
        _observation(fixture.structure.observation.fine_observation_labels[0]),
        fixture.recognitions,
        fixture.selector,
    )
    second = derive_population_inference(
        fine_population,
        _observation(fixture.structure.observation.fine_observation_labels[-1]),
        fixture.recognitions,
        fixture.selector,
    )
    assert first.evidence != second.evidence or first.posterior != second.posterior
    rebuilt = experiment_module._build_coarse_generative_body(
        fixture.structure, coarse_population
    )
    assert _canonical_bytes(rebuilt) == canonical
    assert _canonical_sha256(rebuilt) == sha256

    direct_inputs = ("fine_population", "structure")
    assert experiment_module._forbidden_dependency_violation_count(
        body, direct_inputs
    ) == 0
    contaminated = {**body, "posterior": _law({"labels": [], "masses": []})}
    body_violations = experiment_module._forbidden_dependency_violation_count(
        contaminated, direct_inputs
    )
    input_violations = experiment_module._forbidden_dependency_violation_count(
        body, ("fine_population", "recognition")
    )
    assert body_violations > 0
    assert input_violations > 0
    values = _passing_science_values()
    values["forbidden_dependency_violation_count"] = body_violations + input_violations
    assert experiment_module._metric_records(values)[
        "forbidden_dependency_violation_count"
    ].status == "fail"


def test_recursive_publication_has_exact_dag_metrics_arrays_and_science(
    tmp_path: Path,
) -> None:
    fixture = load_recursive_fixture("lf4_two_parent_recursive_v1")
    result = run_renormalization_v2_recursive_experiment(_config(tmp_path))
    contract = EXPERIMENT_REGISTRY["renormalization_v2_recursive"]

    assert contract.artifact_inventory == _ARTIFACT_STEMS
    assert tuple(result.metrics) == contract.metric_inventory
    assert result.status == "pass"
    assert tuple(sorted(path.name for path in result.run_dir.iterdir())) == tuple(
        sorted(_CORE_FILES + _ARTIFACT_FILES)
    )
    manifest = _read_json(result.run_dir, "manifest")
    assert manifest["complete"] is True
    assert manifest["artifacts"] == {
        name: "complete" for name in sorted(_CORE_FILES + _ARTIFACT_FILES)
    }

    envelopes = {name: _read_json(result.run_dir, name) for name in _JSON_STEMS}
    assert all(
        envelope["schema_version"] == "rg-v2-recursive-phase2-artifact-v1"
        for envelope in envelopes.values()
    )
    hashes = {name: _canonical_sha256(envelope) for name, envelope in envelopes.items()}
    subhashes = _semantic_subhashes(fixture)
    assert _direct_inputs(envelopes["fixture_snapshot"]) == (
        ("fixture_raw", fixture.fixture_sha256),
        *(fixture.subrecord_sha256),
    )
    assert _direct_inputs(envelopes["fine_population"]) == (
        ("generative", subhashes["generative"]),
    )
    assert _direct_inputs(envelopes["coarse_generative"]) == (
        ("fine_population", hashes["fine_population"]),
        ("structure", subhashes["structure"]),
    )
    assert _direct_inputs(envelopes["coarse_interfaces"]) == (
        ("coarse_generative", hashes["coarse_generative"]),
        ("access", subhashes["access"]),
        ("recognition", subhashes["recognition"]),
    )
    assert _direct_inputs(envelopes["coarse_population"]) == (
        ("coarse_generative", hashes["coarse_generative"]),
    )
    scientific_names = _JSON_STEMS[:-1]
    assert _direct_inputs(envelopes["all_observation_inference"]) == (
        ("fine_population", hashes["fine_population"]),
        ("coarse_interfaces", hashes["coarse_interfaces"]),
        ("coarse_population", hashes["coarse_population"]),
    )
    assert _direct_inputs(envelopes["metrics"]) == tuple(
        (name, hashes[name]) for name in scientific_names
    )

    generative_payload = envelopes["coarse_generative"]["payload"]
    _assert_no_forbidden_generative_fields(generative_payload)
    assert _canonical_bytes(generative_payload) == _canonical_bytes(
        json.loads(_canonical_bytes(generative_payload))
    )

    fine_population = construct_population_joint(
        fixture.agents, fixture.records, fixture.context_id
    )
    fine_oracle = enumerate_population_joint_independently(
        fixture.agents, fixture.records, fixture.context_id
    )
    assert fine_population == fine_oracle
    coarse_population = construct_coarse_population_joint(
        fine_population, fixture.structure
    )
    coarse_oracle = _enumerate_coarse_population_independently(
        fine_population, fixture.structure
    )
    assert coarse_population == coarse_oracle
    information = construct_coarse_information_interfaces(
        coarse_population, fixture.access_specs
    )
    observation_records = envelopes["all_observation_inference"]["payload"][
        "observations"
    ]
    assert type(observation_records) is list and len(observation_records) == 16
    assert tuple(record["fine_observed_record"] for record in observation_records) == (
        fixture.structure.observation.fine_observation_labels
    )
    for fine_label, stored in zip(
        fixture.structure.observation.fine_observation_labels,
        observation_records,
        strict=True,
    ):
        fine_inference = derive_population_inference(
            fine_population,
            _observation(fine_label),
            fixture.recognitions,
            fixture.selector,
        )
        coarse_agents = construct_coarse_recognition(
            coarse_population, information, fine_inference
        )
        recursive = derive_recursive_observation(
            coarse_population, coarse_agents, fine_inference
        )
        validate_recursive_observation(recursive, coarse_population, _config(tmp_path / "unused").numerics)
        assert stored["coarse_observed_record"] == recursive.coarse_observed_record
        assert _fraction(stored["fine_evidence"]) == fine_inference.evidence
        assert _fraction(stored["coarse_evidence"]) == recursive.coarse_inference.evidence
        assert _law(stored["pushed_recognition"]) == (
            recursive.pushed_recognition.labels,
            recursive.pushed_recognition.masses,
        )
        assert _law(stored["coarse_recognition"]) == (
            recursive.coarse_inference.recognition.labels,
            recursive.coarse_inference.recognition.masses,
        )
        assert _law(stored["pushed_posterior"]) == (
            recursive.pushed_posterior.labels,
            recursive.pushed_posterior.masses,
        )
        assert _law(stored["coarse_posterior"]) == (
            recursive.coarse_inference.posterior.labels,
            recursive.coarse_inference.posterior.masses,
        )

    records = envelopes["metrics"]["payload"]["records"]
    assert type(records) is list and len(records) == 20
    names = tuple(record["name"] for record in records)
    assert names == contract.metric_inventory and len(set(names)) == 20
    serialized = tuple(record["record"] for record in records)
    assert all(record["status"] == "pass" for record in serialized)
    assert all(record["assessment_scope"] == "implementation_check" for record in serialized)
    assert all(record["verification_state"] == "CANDIDATE" for record in serialized)
    assert all(record["theorem_status"] for record in serialized)
    assert all(record["claim_origin"] for record in serialized)
    assert serialized[15]["value"] >= 2.0
    assert serialized[16]["value"] == 0.0
    assert serialized[17]["value"] >= 1.0
    assert serialized[18]["value"] >= -1.0e-12
    assert serialized[19]["value"] <= 1.0e-12

    assert tuple(result.arrays) == (*_PROVENANCE_ARRAYS, *_FLOAT_ARRAYS)
    assert all(array.flags.c_contiguous for array in result.arrays.values())
    assert all(not array.flags.writeable for array in result.arrays.values())
    with np.load(result.run_dir / "arrays.npz", allow_pickle=False) as archive:
        assert tuple(archive.files) == (*_PROVENANCE_ARRAYS, *_FLOAT_ARRAYS)
        assert all(archive[name].dtype.kind == "U" for name in _PROVENANCE_ARRAYS)
        assert all(archive[name].dtype == np.float64 for name in _FLOAT_ARRAYS)
        assert all(archive[name].dtype != object for name in archive.files)
        array_inputs = tuple(
            (name, hashes[name]) for name in (*scientific_names, "metrics")
        )
        assert tuple(archive["direct_input_names"].tolist()) == tuple(
            name for name, _ in array_inputs
        )
        assert tuple(archive["direct_input_sha256"].tolist()) == tuple(
            sha256 for _, sha256 in array_inputs
        )


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("wrong_theory", "theory.experiment='renormalization_v2_recursive'"),
        ("wrong_arithmetic", "exact_rational"),
        ("nondeterministic", "deterministic CPU float64"),
        ("cuda", "deterministic CPU float64"),
        ("compute_float32", "deterministic CPU float64"),
        ("numerics_float32", "float64 numerics"),
        ("zero_atol", "positive finite"),
        ("loose_atol", "at most 1e-12"),
        ("no_diagnostics", "collect_diagnostics=True"),
        ("figures", "render_figures=False"),
    ],
)
def test_invalid_config_is_rejected_before_all_effect_boundaries(
    mutation: str,
    message: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = _config(tmp_path)
    if mutation == "wrong_theory":
        config = replace(
            config,
            theory=RenormalizationV2TheoryConfig(
                "renormalization_v2", "lf3_product_v1", "exact_rational"
            ),
        )
    elif mutation == "wrong_arithmetic":
        config = replace(config, theory=replace(config.theory, arithmetic="float"))
    elif mutation == "nondeterministic":
        config = replace(config, compute=replace(config.compute, deterministic=False))
    elif mutation == "cuda":
        config = replace(config, compute=replace(config.compute, backend="cuda"))
    elif mutation == "compute_float32":
        config = replace(config, compute=replace(config.compute, dtype="float32"))
    elif mutation == "numerics_float32":
        config = replace(config, numerics=replace(config.numerics, dtype="float32"))
    elif mutation == "zero_atol":
        config = replace(config, numerics=replace(config.numerics, atol=0.0))
    elif mutation == "loose_atol":
        config = replace(config, numerics=replace(config.numerics, atol=1.0e-11))
    elif mutation == "no_diagnostics":
        config = replace(config, output=replace(config.output, collect_diagnostics=False))
    else:
        config = replace(config, output=replace(config.output, render_figures=True))

    monkeypatch.setattr(experiment_module, "load_recursive_fixture", lambda *_: pytest.fail("fixture read"))
    monkeypatch.setattr(experiment_module.RngStreams, "from_seed", lambda *_: pytest.fail("RNG created"))
    monkeypatch.setattr(experiment_module, "collect_provenance", lambda *_: pytest.fail("provenance collected"))
    monkeypatch.setattr(experiment_module.RunStore, "create", lambda *_: pytest.fail("store created"))
    with pytest.raises((TypeError, ValueError), match=message):
        run_renormalization_v2_recursive_experiment(config)
    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_science_completes_before_rng_provenance_store_and_fixture_loads_once(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events: list[str] = []
    real_load = experiment_module.load_recursive_fixture
    real_rng = experiment_module.RngStreams.from_seed.__func__
    real_provenance = experiment_module.collect_provenance
    real_create = RunStore.create.__func__

    def load_once(name: str) -> RecursiveFixture:
        events.append("load")
        return real_load(name)

    def rng(cls: type[object], seed: int) -> object:
        events.append("rng")
        return real_rng(cls, seed)

    def provenance(*args: object) -> dict[str, object]:
        events.append("provenance")
        return real_provenance(*args)

    def create(
        cls: type[RunStore],
        config: ExperimentConfig,
        provenance_data: dict[str, object],
    ) -> RunStore:
        events.append("store")
        hashes = provenance_data["semantic_artifact_sha256"]
        assert tuple(hashes) == _ARTIFACT_STEMS
        assert all(type(value) is str and len(value) == 64 for value in hashes.values())
        return real_create(cls, config, provenance_data)

    monkeypatch.setattr(experiment_module, "load_recursive_fixture", load_once)
    monkeypatch.setattr(experiment_module.RngStreams, "from_seed", classmethod(rng))
    monkeypatch.setattr(experiment_module, "collect_provenance", provenance)
    monkeypatch.setattr(experiment_module.RunStore, "create", classmethod(create))
    run_renormalization_v2_recursive_experiment(_config(tmp_path))
    assert events == ["load", "rng", "provenance", "store"]


def test_scientific_failure_has_no_rng_provenance_or_filesystem_effect(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        experiment_module,
        "_enumerate_coarse_population_independently",
        lambda *_: (_ for _ in ()).throw(ArithmeticError("coarse oracle failure")),
    )
    monkeypatch.setattr(experiment_module.RngStreams, "from_seed", lambda *_: pytest.fail("RNG created"))
    monkeypatch.setattr(experiment_module, "collect_provenance", lambda *_: pytest.fail("provenance collected"))
    monkeypatch.setattr(experiment_module.RunStore, "create", lambda *_: pytest.fail("store created"))
    with pytest.raises(ArithmeticError, match="coarse oracle failure"):
        run_renormalization_v2_recursive_experiment(_config(tmp_path))
    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def _product_selector(
    fixture: RecursiveFixture,
    recognitions: tuple[AgentRecognitionDatum, ...],
) -> SelectorSpec:
    population = construct_population_joint(
        fixture.agents, fixture.records, fixture.context_id
    )
    masses = tuple(
        np.prod([recognitions[index].joint.masses[state] for index, state in enumerate(indices)])
        for indices in product(range(4), repeat=4)
    )
    return SelectorSpec(
        "task6-product-selector",
        "declared_correlated",
        ExactProbabilityLaw(population.latent_labels, tuple(Fraction(value) for value in masses)),
    )


def test_coarse_generative_bytes_ignore_recognition_selector_and_default_observation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = load_recursive_fixture("lf4_two_parent_recursive_v1")
    config = _config(tmp_path / "runs")
    variants: list[RecursiveFixture] = [fixture]
    altered_recognitions = tuple(
        AgentRecognitionDatum(
            agent,
            ExactProbabilityLaw(
                agent.state_labels,
                (Fraction(1, 10), Fraction(2, 10), Fraction(3, 10), Fraction(4, 10)),
            ),
        )
        for agent in fixture.agents
    )
    variants.append(
        replace(
            fixture,
            recognitions=altered_recognitions,
            selector=_product_selector(fixture, altered_recognitions),
        )
    )
    variants.append(
        replace(fixture, selector=_product_selector(fixture, fixture.recognitions))
    )
    variants.append(
        replace(
            fixture,
            observation=_observation(
                fixture.structure.observation.fine_observation_labels[1]
            ),
        )
    )
    generative_bytes: list[bytes] = []
    generative_hashes: list[str] = []
    interface_payloads: list[object] = []
    for index, variant in enumerate(variants):
        monkeypatch.setattr(experiment_module, "load_recursive_fixture", lambda _name, value=variant: value)
        result = run_renormalization_v2_recursive_experiment(config)
        envelope = _read_json(result.run_dir, "coarse_generative")
        generative_bytes.append((result.run_dir / "coarse_generative.json").read_bytes())
        generative_hashes.append(_canonical_sha256(envelope))
        interface_payloads.append(_read_json(result.run_dir, "coarse_interfaces")["payload"])
        shutil.move(str(result.run_dir), str(tmp_path / f"saved-{index}"))
    assert len(set(generative_bytes)) == 1
    assert len(set(generative_hashes)) == 1
    assert interface_payloads[0] != interface_payloads[1]
    assert interface_payloads[0] != interface_payloads[2]


def test_mathematics_is_equal_across_output_roots_without_provenance_equality(
    tmp_path: Path,
) -> None:
    first = run_renormalization_v2_recursive_experiment(_config(tmp_path / "first"))
    second = run_renormalization_v2_recursive_experiment(_config(tmp_path / "second"))
    assert first.config_hash != second.config_hash
    assert first.metrics == second.metrics
    for name in _JSON_STEMS:
        assert _read_json(first.run_dir, name)["payload"] == _read_json(second.run_dir, name)["payload"]
    for name in _FLOAT_ARRAYS:
        np.testing.assert_array_equal(first.arrays[name], second.arrays[name])


def test_recursive_artifact_only_replay_reconstructs_without_primitive_access(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Removing finalized semantics or reading primitives must break replay."""
    result = run_renormalization_v2_recursive_experiment(_config(tmp_path))
    fixture_data_root = (_REPO_ROOT / "rg_v2" / "data").resolve()
    real_read_bytes = Path.read_bytes
    real_read_text = Path.read_text

    def guarded_read_bytes(path: Path) -> bytes:
        resolved = path.resolve()
        if resolved == fixture_data_root or fixture_data_root in resolved.parents:
            pytest.fail(f"replay read primitive fixture bytes: {resolved}")
        return real_read_bytes(path)

    def guarded_read_text(path: Path, *args: object, **kwargs: object) -> str:
        resolved = path.resolve()
        if resolved == fixture_data_root or fixture_data_root in resolved.parents:
            pytest.fail(f"replay read primitive fixture text: {resolved}")
        return real_read_text(path, *args, **kwargs)

    monkeypatch.setattr(
        experiment_module,
        "load_recursive_fixture",
        lambda _: pytest.fail("replay called the primitive fixture loader"),
    )
    monkeypatch.setattr(Path, "read_bytes", guarded_read_bytes)
    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    _replay_finalized_recursive_run(result.run_dir)


@pytest.mark.parametrize(
    ("mutation", "message"),
    (
        ("duplicate", "metric record names must be unique"),
        ("extra", "exactly twenty raw records"),
        ("reordered", "exact ordered inventory"),
        ("malformed", "built-in strings"),
    ),
)
def test_recursive_artifact_replay_rejects_raw_metric_inventory_mutations(
    mutation: str,
    message: str,
    tmp_path: Path,
) -> None:
    """Duplicate, extra, reordered, or malformed raw metrics must fail closed."""
    result = run_renormalization_v2_recursive_experiment(_config(tmp_path))
    path = result.run_dir / "metrics.json"
    envelope = _read_json(result.run_dir, "metrics")
    payload = _require_object(envelope["payload"], "metrics payload")
    records = _require_list(payload["records"], "metric records")
    if mutation == "duplicate":
        first = _require_object(records[0], "first metric")
        last = _require_object(records[-1], "last metric")
        records[-1] = {**last, "name": first["name"]}
    elif mutation == "extra":
        records.append(
            {
                "name": "unexpected_metric",
                "record": _require_object(records[0], "metric")["record"],
            }
        )
    elif mutation == "reordered":
        records[0], records[1] = records[1], records[0]
    else:
        first = _require_object(records[0], "first metric")
        records[0] = {**first, "name": True}
    path.write_text(
        json.dumps(envelope, ensure_ascii=True, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match=message):
        _replay_finalized_recursive_run(result.run_dir)


def test_recursive_artifact_replay_rejects_direct_input_hash_mutation(
    tmp_path: Path,
) -> None:
    """Changing one direct-input digest must break the named DAG edge."""
    result = run_renormalization_v2_recursive_experiment(_config(tmp_path))
    path = result.run_dir / "coarse_generative.json"
    envelope = _read_json(result.run_dir, "coarse_generative")
    direct_inputs = _require_list(envelope["direct_inputs"], "direct inputs")
    first = _require_object(direct_inputs[0], "first direct input")
    direct_inputs[0] = {**first, "sha256": "0" * 64}
    path.write_text(
        json.dumps(envelope, ensure_ascii=True, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    with pytest.raises(
        AssertionError, match="coarse_generative direct-input DAG mismatch"
    ):
        _replay_finalized_recursive_run(result.run_dir)


def test_recursive_artifact_replay_rejects_noncanonical_rational(
    tmp_path: Path,
) -> None:
    """A zero exact denominator must fail at the rational decoder."""
    result = run_renormalization_v2_recursive_experiment(_config(tmp_path))
    path = result.run_dir / "fixture_snapshot.json"
    envelope = _read_json(result.run_dir, "fixture_snapshot")
    payload = _require_object(envelope["payload"], "fixture payload")
    agents = _require_list(payload["agents"], "fixture agents")
    first_agent = _require_object(agents[0], "first agent")
    kernel = _require_object(
        first_agent["generative_kernel"], "generative kernel"
    )
    matrix = _require_list(kernel["matrix"], "generative matrix")
    row = _require_list(matrix[0], "generative row")
    rational = _require_object(row[0], "generative rational")
    row[0] = {**rational, "denominator": 0}
    path.write_text(
        json.dumps(envelope, ensure_ascii=True, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match="denominator must be positive"):
        _replay_finalized_recursive_run(result.run_dir)


def test_recursive_artifact_replay_rejects_observation_pair_mutation(
    tmp_path: Path,
) -> None:
    """Changing a fine/coarse pair must fail at the ordered bijection seam."""
    result = run_renormalization_v2_recursive_experiment(_config(tmp_path))
    path = result.run_dir / "all_observation_inference.json"
    envelope = _read_json(result.run_dir, "all_observation_inference")
    payload = _require_object(envelope["payload"], "all-observation payload")
    observations = _require_list(payload["observations"], "observations")
    first = _require_object(observations[0], "first observation")
    observations[0] = {
        **first,
        "coarse_observed_record": observations[1]["coarse_observed_record"],
    }
    path.write_text(
        json.dumps(envelope, ensure_ascii=True, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    with pytest.raises(AssertionError, match="ordered bijection"):
        _replay_finalized_recursive_run(result.run_dir)


def test_recursive_artifact_replay_rejects_npz_object_dtype(
    tmp_path: Path,
) -> None:
    """An object-dtype mirror must fail under allow_pickle=False."""
    result = run_renormalization_v2_recursive_experiment(_config(tmp_path))
    path = result.run_dir / "arrays.npz"
    with np.load(path, allow_pickle=False) as archive:
        arrays = {name: archive[name] for name in archive.files}
    arrays["metric_values"] = arrays["metric_values"].astype(object)
    np.savez(path, **arrays)
    with pytest.raises(
        ValueError, match="Object arrays cannot be loaded when allow_pickle=False"
    ):
        _replay_finalized_recursive_run(result.run_dir)


def test_recursive_launcher_runs_once_from_arbitrary_cwd_with_empty_pythonpath(
    tmp_path: Path,
) -> None:
    environment = dict(os.environ)
    environment.update(
        CUDA_VISIBLE_DEVICES="-1",
        PYTHONHASHSEED="0",
        PYTHONPATH="",
    )
    completed = subprocess.run(
        [
            str(_PYTHON),
            str(_REPO_ROOT / "run_renormalization_v2_recursive_lab.py"),
        ],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.count("run_dir=") == 1
    assert completed.stdout.count("status=pass") == 1
    run_root = tmp_path / "artifacts" / "renormalization-v2-recursive"
    config_roots = tuple(path for path in run_root.iterdir() if path.is_dir())
    assert len(config_roots) == 1
    runs = tuple(
        path for path in config_roots[0].iterdir() if path.is_dir()
    )
    assert len(runs) == 1
    assert {path.name for path in runs[0].iterdir()} == set(
        _CORE_FILES + _ARTIFACT_FILES
    )


def test_recursive_launcher_has_one_source_only_sys_path_insertion() -> None:
    launcher = _REPO_ROOT / "run_renormalization_v2_recursive_lab.py"
    tree = ast.parse(
        launcher.read_text(encoding="utf-8"), filename=str(launcher)
    )
    insertions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "insert"
        and isinstance(node.func.value, ast.Attribute)
        and node.func.value.attr == "path"
        and isinstance(node.func.value.value, ast.Name)
        and node.func.value.value.id == "sys"
    ]
    assert len(insertions) == 1
    insertion = insertions[0]
    assert len(insertion.args) == 2
    assert isinstance(insertion.args[0], ast.Constant)
    assert insertion.args[0].value == 0
    assert isinstance(insertion.args[1], ast.Call)
    assert isinstance(insertion.args[1].func, ast.Name)
    assert insertion.args[1].func.id == "str"
    assert len(insertion.args[1].args) == 1
    assert isinstance(insertion.args[1].args[0], ast.Name)
    assert insertion.args[1].args[0].id == "SRC"


def test_recursive_installed_sources_do_not_reverse_import_rg_v2() -> None:
    for source in (_REPO_ROOT / "src" / "multiagent_elbo").rglob("*.py"):
        tree = ast.parse(
            source.read_text(encoding="utf-8"), filename=str(source)
        )
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert all(
                    alias.name != "rg_v2"
                    and not alias.name.startswith("rg_v2.")
                    for alias in node.names
                )
            elif isinstance(node, ast.ImportFrom):
                assert node.module is None or (
                    node.module != "rg_v2"
                    and not node.module.startswith("rg_v2.")
                )


def test_recursive_offline_wheel_excludes_rg_v2_and_imports_real_package(
    tmp_path: Path,
) -> None:
    project = tmp_path / "wheel-project"
    project.mkdir()
    shutil.copy2(_REPO_ROOT / "pyproject.toml", project / "pyproject.toml")
    shutil.copytree(_REPO_ROOT / "src", project / "src")
    shutil.copytree(_REPO_ROOT / "rg_v2", project / "rg_v2")
    wheel_output = tmp_path / "wheel-output"
    wheel_output.mkdir()
    environment = dict(os.environ)
    environment.update(
        CUDA_VISIBLE_DEVICES="-1",
        PYTHONHASHSEED="0",
        PYTHONPATH="",
        PIP_NO_INDEX="1",
    )
    build = subprocess.run(
        [
            str(_PYTHON),
            "-B",
            "-c",
            (
                "from setuptools.build_meta import build_wheel; "
                "import sys; print(build_wheel(sys.argv[1]))"
            ),
            str(wheel_output),
        ],
        cwd=project,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert build.returncode == 0, build.stderr
    wheels = tuple(wheel_output.glob("*.whl"))
    assert len(wheels) == 1
    with zipfile.ZipFile(wheels[0]) as archive:
        members = tuple(archive.namelist())
        assert any(
            name.startswith("multiagent_elbo/") for name in members
        )
        assert not any(
            name == "rg_v2" or name.startswith("rg_v2/")
            for name in members
        )
        extracted = tmp_path / "unpacked-wheel"
        archive.extractall(extracted)
    isolated = subprocess.run(
        [
            str(_PYTHON),
            "-I",
            "-B",
            "-c",
            (
                "import importlib.util,pathlib,sys;"
                "wheel_root=pathlib.Path(sys.argv[1]).resolve();"
                "repo_root=pathlib.Path(sys.argv[2]).resolve();"
                "assert all(not item or pathlib.Path(item).resolve()!=repo_root "
                "for item in sys.path);"
                "sys.path.insert(0,str(wheel_root));"
                "import multiagent_elbo;"
                "installed=pathlib.Path(multiagent_elbo.__file__).resolve();"
                "assert wheel_root in installed.parents;"
                "assert importlib.util.find_spec('rg_v2') is None"
            ),
            str(extracted),
            str(_REPO_ROOT),
        ],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert isolated.returncode == 0, isolated.stderr


def _write_artifact_json(
    path: Path, payload: object, *, sort_keys: bool = True
) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=sort_keys)
        + "\n",
        encoding="utf-8",
    )


def _logical_npz_sha256(arrays: dict[str, np.ndarray]) -> str:
    return _canonical_sha256(
        {
            "arrays": [
                {
                    "name": name,
                    "dtype": arrays[name].dtype.str,
                    "shape": list(arrays[name].shape),
                    "values": arrays[name].tolist(),
                }
                for name in sorted(arrays)
            ]
        }
    )


def _coherently_rehash_metric_mutation(
    run_dir: Path,
    mutation: str,
) -> None:
    metrics_path = run_dir / "metrics.json"
    metrics = _read_json(run_dir, "metrics")
    payload = _require_object(metrics["payload"], "metrics payload")
    records = _require_list(payload["records"], "metric records")
    first = _require_object(records[0], "first metric")
    serialized = _require_object(first["record"], "first MetricRecord")
    if mutation == "theorem_status":
        serialized["theorem_status"] = "OPEN"
    elif mutation == "claim_origin":
        serialized["claim_origin"] = "APPLICATION_SPECIFIC"
    elif mutation == "interpretation":
        serialized["interpretation"] = "Mutated but internally rehashed."
    elif mutation == "boolean_value":
        serialized["value"] = False
    else:
        serialized["tolerance"] = False
    _write_artifact_json(metrics_path, metrics)
    metrics_sha256 = _canonical_sha256(metrics)

    arrays_path = run_dir / "arrays.npz"
    with np.load(arrays_path, allow_pickle=False) as archive:
        arrays = {name: archive[name].copy() for name in archive.files}
    names = arrays["direct_input_names"].tolist()
    metrics_index = names.index("metrics")
    arrays["direct_input_sha256"][metrics_index] = metrics_sha256
    np.savez(arrays_path, **arrays)
    arrays_sha256 = _logical_npz_sha256(arrays)

    manifest_path = run_dir / "manifest.json"
    manifest = _read_json(run_dir, "manifest")
    provenance = _require_object(manifest["provenance"], "provenance")
    semantic = _require_object(
        provenance["semantic_artifact_sha256"], "semantic hashes"
    )
    semantic["metrics"] = metrics_sha256
    semantic["arrays"] = arrays_sha256
    input_hashes = _require_object(
        provenance["input_hashes"], "input hashes"
    )
    input_semantic = _require_object(
        input_hashes["semantic_artifacts"], "input semantic hashes"
    )
    input_semantic["metrics"] = metrics_sha256
    input_semantic["arrays"] = arrays_sha256
    _write_artifact_json(manifest_path, manifest)


@pytest.mark.parametrize(
    "mutation",
    (
        "theorem_status",
        "claim_origin",
        "interpretation",
        "boolean_value",
        "boolean_tolerance",
    ),
)
def test_recursive_replay_rejects_coherently_rehashed_metric_mutations(
    mutation: str,
    tmp_path: Path,
) -> None:
    result = run_renormalization_v2_recursive_experiment(_config(tmp_path))
    _coherently_rehash_metric_mutation(result.run_dir, mutation)
    with pytest.raises(
        AssertionError, match="serialized MetricRecord mismatch"
    ):
        _replay_finalized_recursive_run(result.run_dir)


@pytest.mark.parametrize(
    ("mutation", "message"),
    (
        ("semantic_corruption", "semantic_artifact_sha256 mismatch"),
        ("semantic_reorder", "semantic_artifact_sha256 mismatch"),
        ("arrays_corruption", "arrays_direct_inputs mismatch"),
        ("arrays_reorder", "arrays_direct_inputs mismatch"),
        ("fixture_corruption", "fixture_direct_inputs mismatch"),
        ("fixture_reorder", "fixture_direct_inputs mismatch"),
        ("input_semantic_corruption", "input semantic_artifacts mismatch"),
        ("input_semantic_reorder", "input semantic_artifacts mismatch"),
        ("provenance_extra", "manifest provenance keys mismatch"),
        ("input_hashes_extra", "manifest input_hashes keys mismatch"),
    ),
)
def test_recursive_replay_rejects_isolated_manifest_mutations(
    mutation: str,
    message: str,
    tmp_path: Path,
) -> None:
    result = run_renormalization_v2_recursive_experiment(_config(tmp_path))
    path = result.run_dir / "manifest.json"
    manifest = _read_json(result.run_dir, "manifest")
    provenance = _require_object(manifest["provenance"], "provenance")
    semantic = _require_object(
        provenance["semantic_artifact_sha256"], "semantic hashes"
    )
    arrays_inputs = _require_list(
        provenance["arrays_direct_inputs"], "arrays direct inputs"
    )
    input_hashes = _require_object(
        provenance["input_hashes"], "input hashes"
    )
    fixture_inputs = _require_list(
        input_hashes["fixture_direct_inputs"], "fixture direct inputs"
    )
    input_semantic = _require_object(
        input_hashes["semantic_artifacts"], "input semantic hashes"
    )
    if mutation == "semantic_corruption":
        semantic["metrics"] = "0" * 64
    elif mutation == "semantic_reorder":
        provenance["semantic_artifact_sha256"] = dict(
            reversed(tuple(semantic.items()))
        )
    elif mutation == "arrays_corruption":
        arrays_inputs[-1] = "unexpected"
    elif mutation == "arrays_reorder":
        arrays_inputs[0], arrays_inputs[1] = (
            arrays_inputs[1],
            arrays_inputs[0],
        )
    elif mutation == "fixture_corruption":
        first = _require_object(fixture_inputs[0], "fixture input")
        fixture_inputs[0] = {**first, "sha256": "0" * 64}
    elif mutation == "fixture_reorder":
        fixture_inputs[0], fixture_inputs[1] = (
            fixture_inputs[1],
            fixture_inputs[0],
        )
    elif mutation == "input_semantic_corruption":
        input_semantic["arrays"] = "0" * 64
    elif mutation == "input_semantic_reorder":
        input_hashes["semantic_artifacts"] = dict(
            reversed(tuple(input_semantic.items()))
        )
    elif mutation == "provenance_extra":
        provenance["unexpected"] = "value"
    else:
        input_hashes["unexpected"] = "value"
    _write_artifact_json(path, manifest, sort_keys=False)
    with pytest.raises(AssertionError, match=message):
        _replay_finalized_recursive_run(result.run_dir)
