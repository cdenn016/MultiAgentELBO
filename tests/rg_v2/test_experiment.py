from __future__ import annotations

import ast
from dataclasses import replace
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import zipfile

import numpy as np
import pytest

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import ExperimentConfig, config_sha256
from multiagent_elbo.experiment_support import EXPERIMENT_REGISTRY
from multiagent_elbo.finite.scale_cocycle import ExactMarkovChannel
from rg_v2.coarse import aggregate_population, validate_aggregate_datum
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
import rg_v2.experiment as experiment_module
from rg_v2.experiment import run_renormalization_v2_experiment
from rg_v2.fixtures import LocalFirstFixture
from rg_v2.population import (
    construct_population_joint,
    derive_population_inference,
    enumerate_population_joint_independently,
)


_REPO_ROOT = Path(__file__).resolve().parents[2]
_PYTHON = Path(r"C:\Python314\python.exe")

_FIXTURE_IDS = (
    "lf3_product_v1",
    "lf3_correlated_v1",
    "lf3_dirac_boundary_v1",
)
_JSON_ARTIFACTS = (
    "fixture_snapshot",
    "population_joint",
    "population_inference",
    "aggregate_datum",
    "metrics",
)
_ARTIFACT_FILES = tuple(f"{name}.json" for name in _JSON_ARTIFACTS) + (
    "arrays.npz",
)
_CORE_FILES = ("config.json", "manifest.json")
_NPZ_PROVENANCE = (
    "schema_version",
    "fixture_id",
    "producer_commit",
    "config_hash",
    "direct_input_names",
    "direct_input_sha256",
)


def _config(
    root: Path,
    fixture_id: str,
    *,
    collect_diagnostics: bool = True,
    render_figures: bool = False,
    atol: float = 1.0e-12,
) -> ExperimentConfig:
    return ExperimentConfig.from_dicts(
        {"name": f"renormalization-v2-{fixture_id}", "seed": 20260821},
        {
            "experiment": "renormalization_v2",
            "fixture": fixture_id,
            "arithmetic": "exact_rational",
        },
        {
            "dtype": "float64",
            "atol": atol,
            "rtol": 1.0e-10,
            "min_spd_rcond": 1.0e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": root,
            "collect_diagnostics": collect_diagnostics,
            "render_figures": render_figures,
        },
    )


def _read_json(run_dir: Path, stem: str) -> dict[str, object]:
    payload = json.loads((run_dir / f"{stem}.json").read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _canonical_sha256(payload: object) -> str:
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _direct_inputs(envelope: dict[str, object]) -> tuple[tuple[str, str], ...]:
    records = envelope["direct_inputs"]
    assert isinstance(records, list)
    return tuple((record["name"], record["sha256"]) for record in records)


def _metric_records(envelope: dict[str, object]) -> dict[str, dict[str, object]]:
    payload = _require_object(envelope["payload"], "metrics payload")
    raw_records = _require_list(payload["records"], "metric records")
    inventory = EXPERIMENT_REGISTRY["renormalization_v2"].metric_inventory
    assert len(raw_records) == len(inventory), (
        "metrics artifact must contain exactly thirteen records"
    )
    records = tuple(
        _require_object(record, "metric record") for record in raw_records
    )
    assert all(type(record.get("name")) is str for record in records)
    names = tuple(record["name"] for record in records)
    assert len(set(names)) == len(names), "metric record names must be unique"
    assert names == inventory, (
        "metric record names must match the exact ordered inventory"
    )
    return {
        name: _require_object(record["record"], "serialized MetricRecord")
        for name, record in zip(names, records, strict=True)
    }



def _require_object(value: object, label: str) -> dict[str, object]:
    assert type(value) is dict, f"{label} must be an object"
    return value


def _require_list(value: object, label: str) -> list[object]:
    assert type(value) is list, f"{label} must be a list"
    return value


def _exact_fraction(value: object) -> Fraction:
    payload = _require_object(value, "fraction")
    assert set(payload) == {"numerator", "denominator"}
    numerator = payload["numerator"]
    denominator = payload["denominator"]
    assert type(numerator) is int
    assert type(denominator) is int and denominator > 0
    result = Fraction(numerator, denominator)
    assert result.numerator == numerator
    assert result.denominator == denominator
    return result


def _exact_vector(value: object) -> tuple[Fraction, ...]:
    return tuple(_exact_fraction(item) for item in _require_list(value, "fraction vector"))


def _exact_matrix(value: object) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(_exact_vector(row) for row in _require_list(value, "fraction matrix"))


def _probability_law(value: object) -> ExactProbabilityLaw:
    payload = _require_object(value, "probability law")
    assert set(payload) == {"labels", "masses"}
    return ExactProbabilityLaw(
        tuple(str(label) for label in _require_list(payload["labels"], "law labels")),
        _exact_vector(payload["masses"]),
    )


def _submeasure(value: object) -> ExactSubmeasure:
    payload = _require_object(value, "submeasure")
    assert set(payload) == {"labels", "masses"}
    return ExactSubmeasure(
        tuple(str(label) for label in _require_list(payload["labels"], "measure labels")),
        _exact_vector(payload["masses"]),
    )


def _exact_channel(value: object) -> ExactMarkovChannel:
    payload = _require_object(value, "channel")
    assert set(payload) == {
        "source_labels",
        "target_labels",
        "matrix",
        "recognition_independent",
    }
    assert payload["recognition_independent"] is True
    return ExactMarkovChannel(
        tuple(str(label) for label in _require_list(payload["source_labels"], "channel sources")),
        tuple(str(label) for label in _require_list(payload["target_labels"], "channel targets")),
        _exact_matrix(payload["matrix"]),
        recognition_independent=True,
    )


def _agent_from_artifact(value: object) -> AgentDatum:
    payload = _require_object(value, "agent")
    evaluator_records = _require_list(payload["evaluator"], "agent evaluator")
    evaluations: list[ModelEvaluation] = []
    for raw_evaluation in evaluator_records:
        evaluation = _require_object(raw_evaluation, "model evaluation")
        kernel_payload = _require_object(evaluation["kernel"], "evaluator kernel")
        assert evaluation["kernel_sha256"] == _canonical_sha256(kernel_payload)
        evaluations.append(
            ModelEvaluation(
                model_label=str(evaluation["model_label"]),
                kernel=_exact_channel(kernel_payload),
            )
        )
    generative_payload = _require_object(
        payload["generative_kernel"], "generative kernel"
    )
    assert payload["generative_kernel_sha256"] == _canonical_sha256(
        generative_payload
    )
    return AgentDatum(
        agent_id=str(payload["agent_id"]),
        parent_ids=tuple(
            str(item) for item in _require_list(payload["parent_ids"], "parent IDs")
        ),
        belief_labels=tuple(
            str(item)
            for item in _require_list(payload["belief_labels"], "belief labels")
        ),
        model_labels=tuple(
            str(item)
            for item in _require_list(payload["model_labels"], "model labels")
        ),
        state_labels=tuple(
            str(item)
            for item in _require_list(payload["state_labels"], "state labels")
        ),
        evaluator=tuple(evaluations),
        generative_kernel=_exact_channel(generative_payload),
    )


def _recognition_from_artifact(
    value: object,
    agent: AgentDatum,
) -> AgentRecognitionDatum:
    payload = _require_object(value, "recognition")
    assert payload["agent_id"] == agent.agent_id
    assert tuple(payload["belief_labels"]) == agent.belief_labels
    assert tuple(payload["model_labels"]) == agent.model_labels
    assert tuple(payload["state_labels"]) == agent.state_labels
    recognition = AgentRecognitionDatum(agent, _probability_law(payload["joint"]))
    assert recognition.belief_marginal == _probability_law(
        payload["belief_marginal"]
    )
    assert recognition.model_marginal == _probability_law(payload["model_marginal"])
    body = {key: item for key, item in payload.items() if key != "sha256"}
    assert payload["sha256"] == _canonical_sha256(body)
    return recognition


def _record_from_artifact(value: object) -> RecordDatum:
    payload = _require_object(value, "record")
    kernel_payload = _require_object(payload["kernel"], "record kernel")
    assert payload["kernel_sha256"] == _canonical_sha256(kernel_payload)
    body = {key: item for key, item in payload.items() if key != "sha256"}
    assert payload["sha256"] == _canonical_sha256(body)
    return RecordDatum(
        record_id=str(payload["record_id"]),
        owner_id=str(payload["owner_id"]),
        scope_ids=tuple(
            str(item) for item in _require_list(payload["scope_ids"], "record scope")
        ),
        outcome_labels=tuple(
            str(item)
            for item in _require_list(payload["outcome_labels"], "record outcomes")
        ),
        kernel=_exact_channel(kernel_payload),
    )


def _selector_from_artifact(value: object) -> SelectorSpec:
    payload = _require_object(value, "selector")
    coupling_payload = payload["coupling"]
    return SelectorSpec(
        selector_id=str(payload["selector_id"]),
        selector_kind=str(payload["selector_kind"]),
        coupling=(
            None if coupling_payload is None else _probability_law(coupling_payload)
        ),
    )


def _coarse_channel_from_artifact(value: object) -> CoarseChannelSpec:
    payload = _require_object(value, "coarse channel")
    channel_payload = _require_object(payload["channel"], "coarse exact channel")
    assert payload["channel_sha256"] == _canonical_sha256(channel_payload)
    return CoarseChannelSpec(
        channel_id=str(payload["channel_id"]),
        source_agent_ids=tuple(
            str(item)
            for item in _require_list(
                payload["source_agent_ids"], "coarse source agents"
            )
        ),
        structural_input_ids=tuple(
            str(item)
            for item in _require_list(
                payload["structural_input_ids"], "coarse structural inputs"
            )
        ),
        channel=_exact_channel(channel_payload),
    )


def _population_from_artifact(value: object) -> PopulationJoint:
    payload = _require_object(value, "population")
    return PopulationJoint(
        context_id=str(payload["context_id"]),
        agent_order=tuple(
            str(item) for item in _require_list(payload["agent_order"], "agent order")
        ),
        record_order=tuple(
            str(item)
            for item in _require_list(payload["record_order"], "record order")
        ),
        latent_labels=tuple(
            str(item)
            for item in _require_list(payload["latent_labels"], "latent labels")
        ),
        observation_labels=tuple(
            str(item)
            for item in _require_list(
                payload["observation_labels"], "observation labels"
            )
        ),
        joint_masses=_exact_matrix(payload["joint_masses"]),
        construction_trace=tuple(
            str(item)
            for item in _require_list(
                payload["construction_trace"], "construction trace"
            )
        ),
    )


def _aggregate_from_artifact(value: object) -> AggregateDatum:
    payload = _require_object(value, "aggregate")
    return AggregateDatum(
        aggregate_id=str(payload["aggregate_id"]),
        source_agent_ids=tuple(
            str(item)
            for item in _require_list(
                payload["source_agent_ids"], "aggregate source agents"
            )
        ),
        observed_record=str(payload["observed_record"]),
        channel_id=str(payload["channel_id"]),
        channel_sha256=str(payload["channel_sha256"]),
        observation_labels=tuple(
            str(item)
            for item in _require_list(
                payload["observation_labels"], "aggregate observation labels"
            )
        ),
        target_labels=tuple(
            str(item)
            for item in _require_list(
                payload["target_labels"], "aggregate target labels"
            )
        ),
        generative_joint=_exact_matrix(payload["generative_joint"]),
        recognition=_probability_law(payload["recognition"]),
        posterior=_probability_law(payload["posterior"]),
        evidence=_exact_fraction(payload["evidence"]),
        conditional_kl_defect=float(payload["conditional_kl_defect"]),
        kl_chain_residual=float(payload["kl_chain_residual"]),
    )


def _maximum_fraction(values: list[Fraction]) -> Fraction:
    return max(values, default=Fraction(0))


def _matrix_residual(
    left: tuple[tuple[Fraction, ...], ...],
    right: tuple[tuple[Fraction, ...], ...],
) -> Fraction:
    assert len(left) == len(right)
    residuals: list[Fraction] = []
    for left_row, right_row in zip(left, right, strict=True):
        assert len(left_row) == len(right_row)
        residuals.extend(
            abs(left_item - right_item)
            for left_item, right_item in zip(left_row, right_row, strict=True)
        )
    return _maximum_fraction(residuals)


def _replayed_recognition_marginal_residual(
    inference: PopulationInference,
) -> Fraction:
    residuals: list[Fraction] = []
    for agent_index, local in enumerate(inference.recognitions):
        marginal = {label: Fraction(0) for label in local.state_labels}
        for latent_label, mass in zip(
            inference.recognition.labels,
            inference.recognition.masses,
            strict=True,
        ):
            assignment = json.loads(latent_label)
            local_state = assignment[agent_index]
            label = json.dumps(
                local_state[1:],
                ensure_ascii=True,
                separators=(",", ":"),
            )
            marginal[label] += mass
        residuals.extend(
            abs(marginal[label] - expected)
            for label, expected in zip(
                local.state_labels,
                local.joint.masses,
                strict=True,
            )
        )
    return _maximum_fraction(residuals)


def _replayed_posterior_residual(inference: PopulationInference) -> Fraction:
    column = inference.population.observation_labels.index(
        inference.observed_record
    )
    expected_measure = tuple(
        row[column] for row in inference.population.joint_masses
    )
    expected_evidence = sum(expected_measure, Fraction(0))
    expected_posterior = tuple(
        value / expected_evidence for value in expected_measure
    )
    return _maximum_fraction(
        [
            *(
                abs(actual - expected)
                for actual, expected in zip(
                    inference.evidence_measure.masses,
                    expected_measure,
                    strict=True,
                )
            ),
            abs(inference.evidence - expected_evidence),
            *(
                abs(actual - expected)
                for actual, expected in zip(
                    inference.posterior.masses,
                    expected_posterior,
                    strict=True,
                )
            ),
        ]
    )


def _complete_metric_record(
    value: Fraction | int | float,
    tolerance: float,
    *,
    status: str,
    interpretation: str,
    theorem_status: str,
    claim_origin: str,
) -> dict[str, object]:
    return {
        "value": float(value),
        "tolerance": float(tolerance),
        "status": status,
        "interpretation": interpretation,
        "assessment_scope": "implementation_check",
        "theorem_status": theorem_status,
        "verification_state": "CANDIDATE",
        "claim_origin": claim_origin,
    }


def _replayed_metric_records(
    fixture_id: str,
    agents: tuple[AgentDatum, ...],
    records: tuple[RecordDatum, ...],
    population: PopulationJoint,
    independent_population: PopulationJoint,
    inference: PopulationInference,
    aggregate: AggregateDatum,
    tolerance: float,
) -> dict[str, dict[str, object]]:
    agent_residual = _maximum_fraction(
        [
            abs(sum(row, Fraction(0)) - 1)
            for agent in agents
            for row in agent.generative_kernel.matrix
        ]
    )
    evaluator_residuals: list[Fraction] = []
    for agent in agents:
        model_count = len(agent.model_labels)
        for source_index, row in enumerate(agent.generative_kernel.matrix):
            for model_index, evaluation in enumerate(agent.evaluator):
                indices = tuple(
                    belief_index * model_count + model_index
                    for belief_index in range(len(agent.belief_labels))
                )
                model_mass = sum((row[index] for index in indices), Fraction(0))
                if model_mass == 0:
                    continue
                conditional = tuple(row[index] / model_mass for index in indices)
                evaluator_residuals.extend(
                    abs(actual - expected)
                    for actual, expected in zip(
                        conditional,
                        evaluation.kernel.matrix[source_index],
                        strict=True,
                    )
                )
    record_residual = _maximum_fraction(
        [
            abs(sum(row, Fraction(0)) - 1)
            for record in records
            for row in record.kernel.matrix
        ]
    )
    agent_ids = {agent.agent_id for agent in agents}
    seen_records: set[str] = set()
    ownership_violations = 0
    for record in records:
        if record.record_id in seen_records:
            ownership_violations += 1
        seen_records.add(record.record_id)
        if record.owner_id not in agent_ids or record.owner_id not in record.scope_ids:
            ownership_violations += 1
        ownership_violations += sum(
            agent_id not in agent_ids for agent_id in record.scope_ids
        )
    population_residual = abs(
        sum(
            (sum(row, Fraction(0)) for row in population.joint_masses),
            Fraction(0),
        )
        - 1
    )
    independent_residual = _matrix_residual(
        population.joint_masses,
        independent_population.joint_masses,
    )
    recognition_residual = _replayed_recognition_marginal_residual(inference)
    non_dirac_models = sum(
        sum(mass > 0 for mass in recognition.model_marginal.masses) > 1
        for recognition in inference.recognitions
    )
    posterior_residual = _replayed_posterior_residual(inference)
    coarse_residual = abs(aggregate.evidence - inference.evidence)

    zero_specs = {
        "agent_kernel_normalization_residual": (
            agent_residual,
            "Every local generative kernel row is normalized exactly.",
            "ESTABLISHED",
            "STANDARD",
        ),
        "evaluator_compatibility_residual": (
            _maximum_fraction(evaluator_residuals),
            "Every positive model slice agrees with its declared evaluator.",
            "ESTABLISHED",
            "STANDARD",
        ),
        "record_kernel_normalization_residual": (
            record_residual,
            "Every record-kernel row is normalized exactly.",
            "ESTABLISHED",
            "STANDARD",
        ),
        "record_ownership_violation_count": (
            ownership_violations,
            "Every record has one declared owner in its declared scope.",
            "ESTABLISHED",
            "APPLICATION_SPECIFIC",
        ),
        "population_normalization_residual": (
            population_residual,
            "The constructed complete population law is normalized exactly.",
            "ESTABLISHED",
            "STANDARD",
        ),
        "independent_population_residual": (
            independent_residual,
            "The constructor and independent runtime enumeration agree entrywise.",
            "ESTABLISHED",
            "PROJECT_NOVEL",
        ),
        "recognition_marginal_residual": (
            recognition_residual,
            "The selected population recognition preserves every declared local law.",
            "ESTABLISHED",
            "STANDARD",
        ),
        "posterior_derivation_residual": (
            posterior_residual,
            "Evidence and posterior equal the exact observed population slice.",
            "ESTABLISHED",
            "STANDARD",
        ),
        "coarse_evidence_residual": (
            coarse_residual,
            "The common channel preserves the selected observation evidence exactly.",
            "ESTABLISHED",
            "STANDARD",
        ),
    }
    expected: dict[str, dict[str, object]] = {}
    for name, (value, interpretation, theorem_status, claim_origin) in zero_specs.items():
        expected[name] = _complete_metric_record(
            value,
            0.0,
            status="pass" if value == 0 else "fail",
            interpretation=interpretation,
            theorem_status=theorem_status,
            claim_origin=claim_origin,
        )
    if fixture_id == "lf3_dirac_boundary_v1":
        expected["model_marginal_non_dirac_count"] = _complete_metric_record(
            non_dirac_models,
            0.0,
            status="pass" if non_dirac_models == 0 else "fail",
            interpretation="The Dirac boundary has no non-Dirac local model marginal.",
            theorem_status="HYPOTHESIS",
            claim_origin="APPLICATION_SPECIFIC",
        )
    else:
        expected["model_marginal_non_dirac_count"] = _complete_metric_record(
            non_dirac_models,
            0.0,
            status="pass" if non_dirac_models >= 1 else "fail",
            interpretation="The admitted non-boundary fixture retains local model uncertainty.",
            theorem_status="HYPOTHESIS",
            claim_origin="APPLICATION_SPECIFIC",
        )
    expected["conditional_kl_defect"] = _complete_metric_record(
        aggregate.conditional_kl_defect,
        tolerance,
        status=(
            "pass"
            if aggregate.conditional_kl_defect >= -tolerance
            else "fail"
        ),
        interpretation=(
            "The finite conditional KL defect is nonnegative within "
            "the declared float64 tolerance."
        ),
        theorem_status="ESTABLISHED",
        claim_origin="STANDARD",
    )
    expected["kl_chain_residual"] = _complete_metric_record(
        aggregate.kl_chain_residual,
        tolerance,
        status=(
            "pass" if aggregate.kl_chain_residual <= tolerance else "fail"
        ),
        interpretation=(
            "The finite VFE channel chain residual stays within the "
            "declared float64 tolerance."
        ),
        theorem_status="ESTABLISHED",
        claim_origin="STANDARD",
    )
    assert len(expected) == 12
    return expected


_IDENTITY_METRIC_RECORD = {
    "value": 0.0,
    "tolerance": 0.0,
    "status": "pass",
    "interpretation": "One in-process channel object performed all three aggregate pushes.",
    "assessment_scope": "implementation_check",
    "theorem_status": "ESTABLISHED",
    "verification_state": "CANDIDATE",
    "claim_origin": "PROJECT_NOVEL",
}


def _independent_aggregate_id(
    inference: PopulationInference,
    channel: CoarseChannelSpec,
    channel_sha256: str,
) -> str:
    route = {
        "context_id": inference.population.context_id,
        "source_agent_ids": list(channel.source_agent_ids),
        "observed_record": inference.observed_record,
        "channel_id": channel.channel_id,
        "channel_sha256": channel_sha256,
    }
    return "aggregate-" + _canonical_sha256(route)


def _replay_finalized_run(run_dir: Path) -> None:
    expected_files = set(_CORE_FILES + _ARTIFACT_FILES)
    assert {path.name for path in run_dir.iterdir()} == expected_files
    manifest = _read_json(run_dir, "manifest")
    config_document = _read_json(run_dir, "config")
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
            else _require_object(resolved["compute"], "compute configuration")
        ),
    )
    assert config_sha256(config) == config_document["config_hash"]
    assert manifest["config_hash"] == config_document["config_hash"]

    envelopes = {
        name: _read_json(run_dir, name) for name in _JSON_ARTIFACTS
    }
    fixture_id = str(envelopes["fixture_snapshot"]["fixture_id"])
    producer_commit = str(envelopes["fixture_snapshot"]["producer_commit"])
    config_hash = str(envelopes["fixture_snapshot"]["config_hash"])
    for envelope in envelopes.values():
        assert envelope["schema_version"] == "rg-v2-release-1-artifact-v1"
        assert envelope["fixture_id"] == fixture_id
        assert envelope["producer_commit"] == producer_commit
        assert envelope["config_hash"] == config_hash
    assert config_hash == config_document["config_hash"]
    assert producer_commit == manifest["provenance"]["git_commit"]

    hashes = {
        name: _canonical_sha256(envelope)
        for name, envelope in envelopes.items()
    }
    fixture_payload = _require_object(
        envelopes["fixture_snapshot"]["payload"], "fixture payload"
    )
    fixture_sources = tuple(
        (str(record["name"]), str(record["sha256"]))
        for record in (
            _require_object(item, "fixture source")
            for item in _require_list(
                fixture_payload["source_inputs"], "fixture sources"
            )
        )
    )
    assert _direct_inputs(envelopes["fixture_snapshot"]) == fixture_sources
    assert _direct_inputs(envelopes["population_joint"]) == (
        ("fixture_snapshot", hashes["fixture_snapshot"]),
    )
    assert _direct_inputs(envelopes["population_inference"]) == (
        ("fixture_snapshot", hashes["fixture_snapshot"]),
        ("population_joint", hashes["population_joint"]),
    )

    agents = tuple(
        _agent_from_artifact(item)
        for item in _require_list(fixture_payload["agents"], "fixture agents")
    )
    agents_by_id = {agent.agent_id: agent for agent in agents}
    assert len(agents_by_id) == len(agents)
    fixture_recognition_payloads = _require_list(
        fixture_payload["recognitions"], "fixture recognitions"
    )
    recognitions = tuple(
        _recognition_from_artifact(
            item,
            agents_by_id[str(_require_object(item, "recognition")["agent_id"])],
        )
        for item in fixture_recognition_payloads
    )
    records = tuple(
        _record_from_artifact(item)
        for item in _require_list(fixture_payload["records"], "fixture records")
    )
    selector_payload = _require_object(
        fixture_payload["selector"], "fixture selector"
    )
    selector = _selector_from_artifact(selector_payload)
    coarse_payload = _require_object(
        fixture_payload["coarse_channel"], "fixture coarse channel"
    )
    channel = _coarse_channel_from_artifact(coarse_payload)
    channel_declaration = _require_object(
        coarse_payload["channel"], "coarse channel declaration"
    )
    channel_sha256 = _canonical_sha256(channel_declaration)
    assert channel_sha256 == coarse_payload["channel_sha256"]

    population_envelope_payload = _require_object(
        envelopes["population_joint"]["payload"], "population envelope payload"
    )
    stored_population = _population_from_artifact(
        population_envelope_payload["population"]
    )
    stored_independent = _population_from_artifact(
        population_envelope_payload["independent_population"]
    )
    constructor_population = construct_population_joint(
        agents,
        records,
        str(fixture_payload["context_id"]),
    )
    runtime_population = enumerate_population_joint_independently(
        agents,
        records,
        str(fixture_payload["context_id"]),
    )
    assert constructor_population == stored_population
    assert runtime_population == stored_independent
    assert constructor_population == runtime_population
    independent_residual = _matrix_residual(
        constructor_population.joint_masses,
        runtime_population.joint_masses,
    )
    assert independent_residual == _exact_fraction(
        population_envelope_payload["independent_population_residual"]
    )
    assert _exact_fraction(
        population_envelope_payload["normalization_residual"]
    ) == 0

    inference_envelope_payload = _require_object(
        envelopes["population_inference"]["payload"], "inference envelope payload"
    )
    assert inference_envelope_payload["recognitions"] == fixture_recognition_payloads
    assert inference_envelope_payload["selector"] == selector_payload
    observation = tuple(
        (str(record["record_id"]), str(record["outcome"]))
        for record in (
            _require_object(item, "observation item")
            for item in _require_list(
                fixture_payload["observation"], "fixture observation"
            )
        )
    )
    assert inference_envelope_payload["observation"] == fixture_payload["observation"]
    stored_inference = PopulationInference(
        population=stored_population,
        observed_record=str(inference_envelope_payload["observed_record"]),
        recognitions=recognitions,
        selector=selector,
        recognition=_probability_law(inference_envelope_payload["recognition"]),
        evidence_measure=_submeasure(
            inference_envelope_payload["evidence_measure"]
        ),
        evidence=_exact_fraction(inference_envelope_payload["evidence"]),
        posterior=_probability_law(inference_envelope_payload["posterior"]),
    )
    derived_inference = derive_population_inference(
        stored_population,
        observation,
        recognitions,
        selector,
    )
    assert derived_inference == stored_inference
    assert inference_envelope_payload["context_id"] == stored_population.context_id
    assert _exact_fraction(
        inference_envelope_payload["recognition_marginal_residual"]
    ) == _replayed_recognition_marginal_residual(stored_inference)
    assert _exact_fraction(
        inference_envelope_payload["posterior_derivation_residual"]
    ) == _replayed_posterior_residual(stored_inference)
    assert inference_envelope_payload["model_marginal_non_dirac_count"] == sum(
        sum(mass > 0 for mass in recognition.model_marginal.masses) > 1
        for recognition in recognitions
    )

    aggregate_envelope_payload = _require_object(
        envelopes["aggregate_datum"]["payload"], "aggregate envelope payload"
    )
    assert aggregate_envelope_payload["coarse_channel"] == coarse_payload
    stored_aggregate = _aggregate_from_artifact(
        aggregate_envelope_payload["aggregate"]
    )
    replayed_aggregate = aggregate_population(
        stored_inference,
        channel,
        config.numerics,
    )
    assert replayed_aggregate == stored_aggregate
    validate_aggregate_datum(
        stored_aggregate,
        stored_inference,
        channel,
        config.numerics,
    )
    assert aggregate_envelope_payload["fine_context_id"] == stored_population.context_id
    assert _exact_fraction(
        aggregate_envelope_payload["fine_evidence"]
    ) == stored_inference.evidence
    assert _exact_fraction(
        aggregate_envelope_payload["coarse_evidence_residual"]
    ) == abs(stored_aggregate.evidence - stored_inference.evidence)
    assert stored_aggregate.channel_sha256 == channel_sha256
    assert stored_aggregate.aggregate_id == _independent_aggregate_id(
        stored_inference,
        channel,
        channel_sha256,
    )
    assert _direct_inputs(envelopes["aggregate_datum"]) == (
        ("fixture_snapshot", hashes["fixture_snapshot"]),
        ("population_inference", hashes["population_inference"]),
        ("coarse_channel", channel_sha256),
    )

    metrics_envelope = envelopes["metrics"]
    assert _direct_inputs(metrics_envelope) == tuple(
        (name, hashes[name])
        for name in (
            "fixture_snapshot",
            "population_joint",
            "population_inference",
            "aggregate_datum",
        )
    )
    stored_metric_records = _metric_records(metrics_envelope)
    replayed_metric_records = _replayed_metric_records(
        fixture_id,
        agents,
        records,
        stored_population,
        runtime_population,
        stored_inference,
        stored_aggregate,
        min(config.numerics.atol, 1.0e-12),
    )
    assert set(replayed_metric_records) == (
        set(EXPERIMENT_REGISTRY["renormalization_v2"].metric_inventory)
        - {"common_channel_identity_violation_count"}
    )
    for name, expected_record in replayed_metric_records.items():
        assert stored_metric_records[name] == expected_record

    assert aggregate_envelope_payload[
        "common_channel_identity_violation_count"
    ] == 0
    assert stored_metric_records[
        "common_channel_identity_violation_count"
    ] == _IDENTITY_METRIC_RECORD
    assert aggregate_envelope_payload["coarse_channel"] == coarse_payload
    assert aggregate_envelope_payload["aggregate"]["channel_sha256"] == channel_sha256
    assert _direct_inputs(envelopes["aggregate_datum"])[2] == (
        "coarse_channel",
        channel_sha256,
    )

    inventory = EXPERIMENT_REGISTRY["renormalization_v2"].metric_inventory
    complete_expected_metrics = {
        name: (
            _IDENTITY_METRIC_RECORD
            if name == "common_channel_identity_violation_count"
            else replayed_metric_records[name]
        )
        for name in inventory
    }
    array_inputs = tuple(
        (name, hashes[name])
        for name in (
            "fixture_snapshot",
            "population_joint",
            "population_inference",
            "aggregate_datum",
            "metrics",
        )
    )
    expected_array_names = (
        "schema_version",
        "fixture_id",
        "producer_commit",
        "config_hash",
        "direct_input_names",
        "direct_input_sha256",
        "population_joint",
        "independent_population_joint",
        "recognition",
        "evidence_measure",
        "posterior",
        "aggregate_generative_joint",
        "aggregate_recognition",
        "aggregate_posterior",
        "evidence",
        "aggregate_evidence",
        "conditional_kl_defect",
        "kl_chain_residual",
        "metric_values",
        "metric_tolerances",
    )
    expected_float_arrays = {
        "population_joint": np.asarray(
            [
                [float(value) for value in row]
                for row in stored_population.joint_masses
            ],
            dtype=np.float64,
        ),
        "independent_population_joint": np.asarray(
            [
                [float(value) for value in row]
                for row in runtime_population.joint_masses
            ],
            dtype=np.float64,
        ),
        "recognition": np.asarray(
            [float(value) for value in stored_inference.recognition.masses],
            dtype=np.float64,
        ),
        "evidence_measure": np.asarray(
            [float(value) for value in stored_inference.evidence_measure.masses],
            dtype=np.float64,
        ),
        "posterior": np.asarray(
            [float(value) for value in stored_inference.posterior.masses],
            dtype=np.float64,
        ),
        "aggregate_generative_joint": np.asarray(
            [
                [float(value) for value in row]
                for row in stored_aggregate.generative_joint
            ],
            dtype=np.float64,
        ),
        "aggregate_recognition": np.asarray(
            [float(value) for value in stored_aggregate.recognition.masses],
            dtype=np.float64,
        ),
        "aggregate_posterior": np.asarray(
            [float(value) for value in stored_aggregate.posterior.masses],
            dtype=np.float64,
        ),
        "evidence": np.asarray(stored_inference.evidence, dtype=np.float64),
        "aggregate_evidence": np.asarray(
            stored_aggregate.evidence, dtype=np.float64
        ),
        "conditional_kl_defect": np.asarray(
            stored_aggregate.conditional_kl_defect, dtype=np.float64
        ),
        "kl_chain_residual": np.asarray(
            stored_aggregate.kl_chain_residual, dtype=np.float64
        ),
        "metric_values": np.asarray(
            [complete_expected_metrics[name]["value"] for name in inventory],
            dtype=np.float64,
        ),
        "metric_tolerances": np.asarray(
            [
                complete_expected_metrics[name]["tolerance"]
                for name in inventory
            ],
            dtype=np.float64,
        ),
    }
    with np.load(run_dir / "arrays.npz", allow_pickle=False) as archive:
        assert tuple(archive.files) == expected_array_names
        assert len(archive.files) == 20
        for name in (
            "schema_version",
            "fixture_id",
            "producer_commit",
            "config_hash",
        ):
            assert archive[name].dtype.kind == "U"
            assert archive[name].shape == ()
        assert archive["direct_input_names"].dtype.kind == "U"
        assert archive["direct_input_sha256"].dtype.kind == "U"
        assert archive["direct_input_names"].shape == (5,)
        assert archive["direct_input_sha256"].shape == (5,)
        assert str(archive["schema_version"].item()) == "rg-v2-release-1-artifact-v1"
        assert str(archive["fixture_id"].item()) == fixture_id
        assert str(archive["producer_commit"].item()) == producer_commit
        assert str(archive["config_hash"].item()) == config_hash
        assert tuple(archive["direct_input_names"].tolist()) == tuple(
            name for name, _ in array_inputs
        )
        assert tuple(archive["direct_input_sha256"].tolist()) == tuple(
            sha256 for _, sha256 in array_inputs
        )
        for name, expected_array in expected_float_arrays.items():
            assert archive[name].dtype == np.float64
            assert archive[name].shape == expected_array.shape
            np.testing.assert_array_equal(archive[name], expected_array)
        logical_arrays = {
            "arrays": [
                {
                    "name": name,
                    "dtype": archive[name].dtype.str,
                    "shape": list(archive[name].shape),
                    "values": archive[name].tolist(),
                }
                for name in sorted(archive.files)
            ]
        }
    semantic_hashes = manifest["provenance"]["semantic_artifact_sha256"]
    assert {
        name: semantic_hashes[name] for name in _JSON_ARTIFACTS
    } == hashes
    assert semantic_hashes["arrays"] == _canonical_sha256(logical_arrays)


@pytest.mark.parametrize("fixture_id", _FIXTURE_IDS)
def test_every_fixture_publishes_the_complete_release_contract(
    fixture_id: str,
    tmp_path: Path,
) -> None:
    result = run_renormalization_v2_experiment(_config(tmp_path, fixture_id))

    contract = EXPERIMENT_REGISTRY["renormalization_v2"]
    assert contract.artifact_inventory == (
        "fixture_snapshot",
        "population_joint",
        "population_inference",
        "aggregate_datum",
        "metrics",
        "arrays",
    )
    assert tuple(result.metrics) == contract.metric_inventory
    assert result.status == "pass"
    assert tuple(sorted(path.name for path in result.run_dir.iterdir())) == tuple(
        sorted(_CORE_FILES + _ARTIFACT_FILES)
    )

    manifest = _read_json(result.run_dir, "manifest")
    assert manifest["complete"] is True
    assert manifest["config_hash"] == result.config_hash
    assert manifest["artifacts"] == {
        filename: "complete" for filename in sorted(_CORE_FILES + _ARTIFACT_FILES)
    }

    envelopes = {name: _read_json(result.run_dir, name) for name in _JSON_ARTIFACTS}
    for envelope in envelopes.values():
        assert envelope["schema_version"] == "rg-v2-release-1-artifact-v1"
        assert envelope["fixture_id"] == fixture_id
        assert envelope["producer_commit"] == manifest["provenance"]["git_commit"]
        assert envelope["config_hash"] == result.config_hash
        assert isinstance(envelope["direct_inputs"], list)
        assert isinstance(envelope["payload"], dict)

    hashes = {name: _canonical_sha256(envelope) for name, envelope in envelopes.items()}
    fixture_payload = envelopes["fixture_snapshot"]["payload"]
    assert fixture_payload["fixture_sha256"]
    assert fixture_payload["agents"]
    assert fixture_payload["recognitions"]
    assert fixture_payload["records"]
    assert fixture_payload["selector"]
    assert fixture_payload["coarse_channel"]
    assert "fixture_path" not in json.dumps(fixture_payload)

    fixture_sources = tuple(
        (record["name"], record["sha256"])
        for record in fixture_payload["source_inputs"]
    )
    assert _direct_inputs(envelopes["fixture_snapshot"]) == fixture_sources
    assert _direct_inputs(envelopes["population_joint"]) == (
        ("fixture_snapshot", hashes["fixture_snapshot"]),
    )
    assert _direct_inputs(envelopes["population_inference"]) == (
        ("fixture_snapshot", hashes["fixture_snapshot"]),
        ("population_joint", hashes["population_joint"]),
    )
    channel_hash = fixture_payload["coarse_channel"]["channel_sha256"]
    assert _direct_inputs(envelopes["aggregate_datum"]) == (
        ("fixture_snapshot", hashes["fixture_snapshot"]),
        ("population_inference", hashes["population_inference"]),
        ("coarse_channel", channel_hash),
    )
    assert _direct_inputs(envelopes["metrics"]) == tuple(
        (name, hashes[name])
        for name in (
            "fixture_snapshot",
            "population_joint",
            "population_inference",
            "aggregate_datum",
        )
    )

    population_payload = envelopes["population_joint"]["payload"]
    assert population_payload["population"] == population_payload["independent_population"]
    assert population_payload["independent_population_residual"] == {
        "numerator": 0,
        "denominator": 1,
    }
    metric_records = _metric_records(envelopes["metrics"])
    assert tuple(metric_records) == contract.metric_inventory
    assert metric_records["independent_population_residual"]["value"] == 0.0
    assert all(
        record["assessment_scope"] == "implementation_check"
        for record in metric_records.values()
    )
    assert all(record["verification_state"] == "CANDIDATE" for record in metric_records.values())
    assert all(record["theorem_status"] for record in metric_records.values())
    assert all(record["claim_origin"] for record in metric_records.values())

    with np.load(result.run_dir / "arrays.npz", allow_pickle=False) as archive:
        assert set(_NPZ_PROVENANCE) <= set(archive.files)
        assert all(archive[name].dtype.kind == "U" for name in _NPZ_PROVENANCE)
        assert all(archive[name].dtype != object for name in archive.files)
        assert str(archive["schema_version"].item()) == "rg-v2-release-1-artifact-v1"
        assert str(archive["fixture_id"].item()) == fixture_id
        assert str(archive["producer_commit"].item()) == envelopes["metrics"]["producer_commit"]
        assert str(archive["config_hash"].item()) == result.config_hash
        expected_array_inputs = tuple(
            (name, hashes[name])
            for name in (
                "fixture_snapshot",
                "population_joint",
                "population_inference",
                "aggregate_datum",
                "metrics",
            )
        )
        assert tuple(archive["direct_input_names"].tolist()) == tuple(
            name for name, _ in expected_array_inputs
        )
        assert tuple(archive["direct_input_sha256"].tolist()) == tuple(
            sha256 for _, sha256 in expected_array_inputs
        )
        assert archive["population_joint"].dtype == np.float64
        assert archive["independent_population_joint"].dtype == np.float64
        np.testing.assert_array_equal(
            archive["population_joint"], archive["independent_population_joint"]
        )


@pytest.mark.parametrize(
    ("collect_diagnostics", "render_figures", "message"),
    [
        (False, False, "collect_diagnostics=True"),
        (True, True, "render_figures=False"),
    ],
)
def test_output_modes_are_rejected_before_fixture_rng_or_publication(
    collect_diagnostics: bool,
    render_figures: bool,
    message: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = _config(
        tmp_path,
        "lf3_product_v1",
        collect_diagnostics=collect_diagnostics,
        render_figures=render_figures,
    )
    monkeypatch.setattr(
        experiment_module,
        "load_fixture",
        lambda _: pytest.fail("fixture loaded before output validation"),
    )
    monkeypatch.setattr(
        experiment_module.RngStreams,
        "from_seed",
        lambda _: pytest.fail("RNG created before output validation"),
    )
    monkeypatch.setattr(
        experiment_module.RunStore,
        "create",
        lambda *_: pytest.fail("RunStore created before output validation"),
    )

    with pytest.raises(ValueError, match=message):
        run_renormalization_v2_experiment(config)

    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_loose_atol_is_rejected_before_fixture_rng_or_publication(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = _config(tmp_path, "lf3_product_v1", atol=1.0e-11)
    monkeypatch.setattr(
        experiment_module,
        "load_fixture",
        lambda _: pytest.fail("fixture loaded before tolerance validation"),
    )
    monkeypatch.setattr(
        experiment_module.RngStreams,
        "from_seed",
        lambda _: pytest.fail("RNG created before tolerance validation"),
    )
    monkeypatch.setattr(
        experiment_module.RunStore,
        "create",
        lambda *_: pytest.fail("RunStore created before tolerance validation"),
    )

    with pytest.raises(ValueError, match="at most 1e-12"):
        run_renormalization_v2_experiment(config)

    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_cpu_float64_deterministic_contract_is_enforced_before_fixture_load(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = _config(tmp_path, "lf3_product_v1")
    invalid_compute = replace(config.compute, deterministic=False)
    invalid_config = replace(config, compute=invalid_compute)
    monkeypatch.setattr(
        experiment_module,
        "load_fixture",
        lambda _: pytest.fail("fixture loaded before compute validation"),
    )

    with pytest.raises(ValueError, match="deterministic CPU float64"):
        run_renormalization_v2_experiment(invalid_config)


def test_scientific_failure_precedes_rng_provenance_and_filesystem_effects(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = _config(tmp_path, "lf3_product_v1")
    monkeypatch.setattr(
        experiment_module,
        "enumerate_population_joint_independently",
        lambda *_: (_ for _ in ()).throw(ArithmeticError("independent failure")),
    )
    monkeypatch.setattr(
        experiment_module.RngStreams,
        "from_seed",
        lambda _: pytest.fail("RNG created after failed science"),
    )
    monkeypatch.setattr(
        experiment_module,
        "collect_provenance",
        lambda *_: pytest.fail("provenance collected after failed science"),
    )
    monkeypatch.setattr(
        experiment_module.RunStore,
        "create",
        lambda *_: pytest.fail("RunStore created after failed science"),
    )

    with pytest.raises(ArithmeticError, match="independent failure"):
        run_renormalization_v2_experiment(config)

    assert not tmp_path.exists() or list(tmp_path.iterdir()) == []


def test_fixture_is_loaded_once_and_complete_hash_plan_precedes_runstore_create(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    load_calls: list[str] = []
    real_load = experiment_module.load_fixture
    real_create = RunStore.create.__func__

    def load_once(fixture_id: str) -> LocalFirstFixture:
        load_calls.append(fixture_id)
        return real_load(fixture_id)

    def checked_create(
        cls: type[RunStore],
        config: ExperimentConfig,
        provenance: dict[str, object],
    ) -> RunStore:
        artifact_hashes = provenance["semantic_artifact_sha256"]
        assert tuple(artifact_hashes) == (
            "fixture_snapshot",
            "population_joint",
            "population_inference",
            "aggregate_datum",
            "metrics",
            "arrays",
        )
        assert all(len(value) == 64 for value in artifact_hashes.values())
        assert tuple(provenance["arrays_direct_inputs"]) == (
            "fixture_snapshot",
            "population_joint",
            "population_inference",
            "aggregate_datum",
            "metrics",
        )
        return real_create(cls, config, provenance)

    monkeypatch.setattr(experiment_module, "load_fixture", load_once)
    monkeypatch.setattr(
        experiment_module.RunStore,
        "create",
        classmethod(checked_create),
    )

    run_renormalization_v2_experiment(_config(tmp_path, "lf3_product_v1"))

    assert load_calls == ["lf3_product_v1"]


def test_mathematical_results_are_equal_across_output_roots(
    tmp_path: Path,
) -> None:
    first = run_renormalization_v2_experiment(
        _config(tmp_path / "first", "lf3_correlated_v1")
    )
    second = run_renormalization_v2_experiment(
        _config(tmp_path / "second", "lf3_correlated_v1")
    )

    assert first.config_hash != second.config_hash
    assert first.metrics == second.metrics
    for name in _JSON_ARTIFACTS:
        assert _read_json(first.run_dir, name)["payload"] == _read_json(
            second.run_dir, name
        )["payload"]
    with (
        np.load(first.run_dir / "arrays.npz", allow_pickle=False) as first_arrays,
        np.load(second.run_dir / "arrays.npz", allow_pickle=False) as second_arrays,
    ):
        science_names = tuple(
            name for name in first_arrays.files if name not in _NPZ_PROVENANCE
        )
        assert science_names == tuple(
            name for name in second_arrays.files if name not in _NPZ_PROVENANCE
        )
        for name in science_names:
            np.testing.assert_array_equal(first_arrays[name], second_arrays[name])


@pytest.mark.parametrize("fixture_id", _FIXTURE_IDS)
def test_finalized_artifacts_replay_without_fixture_access(
    fixture_id: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    result = run_renormalization_v2_experiment(_config(tmp_path, fixture_id))
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
        "load_fixture",
        lambda _: pytest.fail("replay called the primitive fixture loader"),
    )
    monkeypatch.setattr(Path, "read_bytes", guarded_read_bytes)
    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    _replay_finalized_run(result.run_dir)



@pytest.mark.parametrize(
    ("mutation", "message"),
    (
        ("duplicate", "metric record names must be unique"),
        ("extra", "metrics artifact must contain exactly thirteen records"),
    ),
)
def test_artifact_replay_rejects_duplicate_or_extra_raw_metric_records(
    mutation: str,
    message: str,
    tmp_path: Path,
) -> None:
    result = run_renormalization_v2_experiment(
        _config(tmp_path, "lf3_product_v1")
    )
    metrics_path = result.run_dir / "metrics.json"
    envelope = _read_json(result.run_dir, "metrics")
    payload = _require_object(envelope["payload"], "metrics payload")
    records = _require_list(payload["records"], "metric records")
    assert len(records) == 13
    if mutation == "duplicate":
        first = _require_object(records[0], "first metric record")
        last = _require_object(records[-1], "last metric record")
        records[-1] = {**last, "name": first["name"]}
    else:
        records.append(
            {
                "name": "unexpected_metric",
                "record": _require_object(records[0], "metric record")["record"],
            }
        )
    metrics_path.write_text(
        json.dumps(
            envelope,
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(AssertionError, match=message):
        _replay_finalized_run(result.run_dir)


def test_absolute_launcher_runs_from_arbitrary_cwd_with_empty_pythonpath(
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
            str(_REPO_ROOT / "run_renormalization_v2_lab.py"),
        ],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "status=pass" in completed.stdout


def test_launcher_has_one_source_only_sys_path_insertion() -> None:
    launcher = _REPO_ROOT / "run_renormalization_v2_lab.py"
    tree = ast.parse(launcher.read_text(encoding="utf-8"), filename=str(launcher))
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


def test_installed_package_sources_do_not_reverse_import_rg_v2() -> None:
    for source in (_REPO_ROOT / "src" / "multiagent_elbo").rglob("*.py"):
        tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
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


def test_offline_wheel_excludes_root_local_rg_v2_and_imports_in_isolation(
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
        assert any(name.startswith("multiagent_elbo/") for name in members)
        assert not any(name == "rg_v2" or name.startswith("rg_v2/") for name in members)
        extracted = tmp_path / "unpacked-wheel"
        archive.extractall(extracted)

    isolated = subprocess.run(
        [
            str(_PYTHON),
            "-I",
            "-B",
            "-c",
            (
                "import importlib.util, pathlib, sys; "
                "wheel_root=pathlib.Path(sys.argv[1]).resolve(); "
                "repo_root=pathlib.Path(sys.argv[2]).resolve(); "
                "assert all(not item or pathlib.Path(item).resolve()!=repo_root "
                "for item in sys.path); "
                "sys.path.insert(0,str(wheel_root)); "
                "import multiagent_elbo; "
                "installed=pathlib.Path(multiagent_elbo.__file__).resolve(); "
                "assert wheel_root in installed.parents; "
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
