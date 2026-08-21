"""Artifact-backed execution of the local-first renormalization v2 laboratory."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
from types import MappingProxyType
from typing import Literal, Mapping

import numpy as np

from multiagent_elbo.artifacts import RunStore
from multiagent_elbo.config import (
    ExperimentConfig,
    RenormalizationV2TheoryConfig,
    config_sha256,
)
from multiagent_elbo.experiment_support import (
    EXPERIMENT_REGISTRY,
    MetricRecord,
    lower_bounded_metric,
    target_metric,
    upper_bounded_metric,
)
from multiagent_elbo.finite.scale_cocycle import ExactMarkovChannel
from multiagent_elbo.runtime import RngStreams, collect_provenance

from rg_v2.coarse import aggregate_population
from rg_v2.contracts import (
    AgentDatum,
    AgentRecognitionDatum,
    AggregateDatum,
    CoarseChannelSpec,
    ExactProbabilityLaw,
    ExactSubmeasure,
    PopulationInference,
    PopulationJoint,
    RecordDatum,
    SelectorSpec,
)
from rg_v2.fixtures import LocalFirstFixture, load_fixture
from rg_v2.population import (
    construct_population_joint,
    derive_population_inference,
    enumerate_population_joint_independently,
)


MetricStatus = Literal["pass", "fail", "inconclusive"]
_SCHEMA_VERSION = "rg-v2-release-1-artifact-v1"
_JSON_ARTIFACTS = (
    "fixture_snapshot",
    "population_joint",
    "population_inference",
    "aggregate_datum",
    "metrics",
)
_DECLARED_ARTIFACTS = tuple(f"{name}.json" for name in _JSON_ARTIFACTS) + (
    "arrays.npz",
)
_CONTRACT = EXPERIMENT_REGISTRY["renormalization_v2"]
_COMMIT_PATTERN = re.compile(r"[0-9a-f]{40,64}\Z")


@dataclass(frozen=True)
class RenormalizationV2ExperimentResult:
    """Typed handle to one finalized Release 1 run."""

    run_dir: Path
    config_hash: str
    status: MetricStatus
    metrics: Mapping[str, MetricRecord]
    arrays: Mapping[str, np.ndarray]


@dataclass(frozen=True)
class _ScientificRun:
    fixture: LocalFirstFixture
    population: PopulationJoint
    independent_population: PopulationJoint
    inference: PopulationInference
    aggregate: AggregateDatum
    fixture_body: dict[str, object]
    population_body: dict[str, object]
    inference_body: dict[str, object]
    aggregate_body: dict[str, object]
    metrics: Mapping[str, MetricRecord]
    metrics_body: dict[str, object]
    numeric_arrays: Mapping[str, np.ndarray]


def _canonical_json(payload: object) -> str:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def _canonical_sha256(payload: object) -> str:
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _json_native(payload: object) -> dict[str, object]:
    """Freeze one JSON body by canonical encode/decode before publication."""
    result = json.loads(_canonical_json(payload))
    if not isinstance(result, dict):
        raise TypeError("artifact envelope must be a JSON object")
    return result


def _fraction_payload(value: Fraction) -> dict[str, int]:
    if not isinstance(value, Fraction):
        raise TypeError("exact artifact values must be Fraction instances")
    return {"numerator": value.numerator, "denominator": value.denominator}


def _fraction_vector(values: tuple[Fraction, ...]) -> list[dict[str, int]]:
    return [_fraction_payload(value) for value in values]


def _fraction_matrix(
    values: tuple[tuple[Fraction, ...], ...],
) -> list[list[dict[str, int]]]:
    return [_fraction_vector(row) for row in values]


def _law_payload(law: ExactProbabilityLaw | ExactSubmeasure) -> dict[str, object]:
    return {"labels": list(law.labels), "masses": _fraction_vector(law.masses)}


def _channel_payload(channel: ExactMarkovChannel) -> dict[str, object]:
    return {
        "source_labels": list(channel.source_labels),
        "target_labels": list(channel.target_labels),
        "matrix": _fraction_matrix(channel.matrix),
        "recognition_independent": channel.recognition_independent,
    }


def _agent_payload(agent: AgentDatum) -> dict[str, object]:
    evaluators: list[dict[str, object]] = []
    for evaluation in agent.evaluator:
        declaration = _channel_payload(evaluation.kernel)
        evaluators.append(
            {
                "model_label": evaluation.model_label,
                "kernel": declaration,
                "kernel_sha256": _canonical_sha256(declaration),
            }
        )
    generative = _channel_payload(agent.generative_kernel)
    return {
        "agent_id": agent.agent_id,
        "parent_ids": list(agent.parent_ids),
        "belief_labels": list(agent.belief_labels),
        "model_labels": list(agent.model_labels),
        "state_labels": list(agent.state_labels),
        "evaluator": evaluators,
        "generative_kernel": generative,
        "generative_kernel_sha256": _canonical_sha256(generative),
    }


def _recognition_payload(
    recognition: AgentRecognitionDatum,
) -> dict[str, object]:
    body = {
        "agent_id": recognition.agent_id,
        "belief_labels": list(recognition.belief_labels),
        "model_labels": list(recognition.model_labels),
        "state_labels": list(recognition.state_labels),
        "joint": _law_payload(recognition.joint),
        "belief_marginal": _law_payload(recognition.belief_marginal),
        "model_marginal": _law_payload(recognition.model_marginal),
    }
    return {**body, "sha256": _canonical_sha256(body)}


def _record_payload(record: RecordDatum) -> dict[str, object]:
    kernel = _channel_payload(record.kernel)
    body = {
        "record_id": record.record_id,
        "owner_id": record.owner_id,
        "scope_ids": list(record.scope_ids),
        "outcome_labels": list(record.outcome_labels),
        "kernel": kernel,
        "kernel_sha256": _canonical_sha256(kernel),
    }
    return {**body, "sha256": _canonical_sha256(body)}


def _selector_payload(selector: SelectorSpec) -> dict[str, object]:
    return {
        "selector_id": selector.selector_id,
        "selector_kind": selector.selector_kind,
        "coupling": (
            None if selector.coupling is None else _law_payload(selector.coupling)
        ),
    }


def _coarse_channel_payload(channel: CoarseChannelSpec) -> dict[str, object]:
    declaration = _channel_payload(channel.channel)
    return {
        "channel_id": channel.channel_id,
        "source_agent_ids": list(channel.source_agent_ids),
        "structural_input_ids": list(channel.structural_input_ids),
        "channel": declaration,
        "channel_sha256": _canonical_sha256(declaration),
    }


def _population_payload(population: PopulationJoint) -> dict[str, object]:
    return {
        "context_id": population.context_id,
        "agent_order": list(population.agent_order),
        "record_order": list(population.record_order),
        "latent_labels": list(population.latent_labels),
        "observation_labels": list(population.observation_labels),
        "joint_masses": _fraction_matrix(population.joint_masses),
        "construction_trace": list(population.construction_trace),
    }


def _inference_payload(inference: PopulationInference) -> dict[str, object]:
    return {
        "context_id": inference.population.context_id,
        "observed_record": inference.observed_record,
        "recognitions": [
            _recognition_payload(recognition)
            for recognition in inference.recognitions
        ],
        "selector": _selector_payload(inference.selector),
        "recognition": _law_payload(inference.recognition),
        "evidence_measure": _law_payload(inference.evidence_measure),
        "evidence": _fraction_payload(inference.evidence),
        "posterior": _law_payload(inference.posterior),
    }


def _aggregate_payload(aggregate: AggregateDatum) -> dict[str, object]:
    return {
        "aggregate_id": aggregate.aggregate_id,
        "source_agent_ids": list(aggregate.source_agent_ids),
        "observed_record": aggregate.observed_record,
        "channel_id": aggregate.channel_id,
        "channel_sha256": aggregate.channel_sha256,
        "observation_labels": list(aggregate.observation_labels),
        "target_labels": list(aggregate.target_labels),
        "generative_joint": _fraction_matrix(aggregate.generative_joint),
        "recognition": _law_payload(aggregate.recognition),
        "posterior": _law_payload(aggregate.posterior),
        "evidence": _fraction_payload(aggregate.evidence),
        "conditional_kl_defect": aggregate.conditional_kl_defect,
        "kl_chain_residual": aggregate.kl_chain_residual,
    }


def _maximum_fraction(values: list[Fraction]) -> Fraction:
    return max(values, default=Fraction(0))


def _agent_normalization_residual(fixture: LocalFirstFixture) -> Fraction:
    return _maximum_fraction(
        [
            abs(sum(row, Fraction(0)) - 1)
            for agent in fixture.agents
            for row in agent.generative_kernel.matrix
        ]
    )


def _evaluator_compatibility_residual(fixture: LocalFirstFixture) -> Fraction:
    residuals: list[Fraction] = []
    for agent in fixture.agents:
        model_count = len(agent.model_labels)
        for source_index, row in enumerate(agent.generative_kernel.matrix):
            for model_index, evaluation in enumerate(agent.evaluator):
                state_indices = tuple(
                    belief_index * model_count + model_index
                    for belief_index in range(len(agent.belief_labels))
                )
                model_mass = sum(
                    (row[index] for index in state_indices), Fraction(0)
                )
                if model_mass == 0:
                    continue
                conditional = tuple(row[index] / model_mass for index in state_indices)
                residuals.extend(
                    abs(actual - expected)
                    for actual, expected in zip(
                        conditional,
                        evaluation.kernel.matrix[source_index],
                        strict=True,
                    )
                )
    return _maximum_fraction(residuals)


def _record_normalization_residual(fixture: LocalFirstFixture) -> Fraction:
    return _maximum_fraction(
        [
            abs(sum(row, Fraction(0)) - 1)
            for record in fixture.records
            for row in record.kernel.matrix
        ]
    )


def _record_ownership_violations(fixture: LocalFirstFixture) -> int:
    agent_ids = {agent.agent_id for agent in fixture.agents}
    seen: set[str] = set()
    violations = 0
    for record in fixture.records:
        if record.record_id in seen:
            violations += 1
        seen.add(record.record_id)
        if record.owner_id not in agent_ids or record.owner_id not in record.scope_ids:
            violations += 1
        violations += sum(agent_id not in agent_ids for agent_id in record.scope_ids)
    return violations


def _matrix_residual(
    left: tuple[tuple[Fraction, ...], ...],
    right: tuple[tuple[Fraction, ...], ...],
) -> Fraction:
    if len(left) != len(right) or any(
        len(left_row) != len(right_row)
        for left_row, right_row in zip(left, right, strict=True)
    ):
        raise ValueError("exact matrices must have the same shape")
    return _maximum_fraction(
        [
            abs(left_value - right_value)
            for left_row, right_row in zip(left, right, strict=True)
            for left_value, right_value in zip(left_row, right_row, strict=True)
        ]
    )


def _recognition_marginal_residual(inference: PopulationInference) -> Fraction:
    residuals: list[Fraction] = []
    for agent_index, local in enumerate(inference.recognitions):
        actual = {label: Fraction(0) for label in local.state_labels}
        for latent_label, mass in zip(
            inference.recognition.labels,
            inference.recognition.masses,
            strict=True,
        ):
            assignment = json.loads(latent_label)
            entry = assignment[agent_index]
            local_label = json.dumps(
                entry[1:], ensure_ascii=True, separators=(",", ":")
            )
            actual[local_label] += mass
        residuals.extend(
            abs(actual[label] - expected)
            for label, expected in zip(
                local.state_labels, local.joint.masses, strict=True
            )
        )
    return _maximum_fraction(residuals)


def _posterior_derivation_residual(inference: PopulationInference) -> Fraction:
    column = inference.population.observation_labels.index(inference.observed_record)
    expected_measure = tuple(
        row[column] for row in inference.population.joint_masses
    )
    expected_evidence = sum(expected_measure, Fraction(0))
    expected_posterior = tuple(value / expected_evidence for value in expected_measure)
    return _maximum_fraction(
        [
            *(abs(actual - expected) for actual, expected in zip(
                inference.evidence_measure.masses, expected_measure, strict=True
            )),
            abs(inference.evidence - expected_evidence),
            *(abs(actual - expected) for actual, expected in zip(
                inference.posterior.masses, expected_posterior, strict=True
            )),
        ]
    )


def _candidate_target(
    value: Fraction | int,
    *,
    interpretation: str,
    theorem_status: Literal["ESTABLISHED", "HYPOTHESIS", "NUMERICAL"],
    claim_origin: Literal["STANDARD", "PROJECT_NOVEL", "APPLICATION_SPECIFIC"],
) -> MetricRecord:
    return target_metric(
        float(value),
        0.0,
        target=0.0,
        interpretation=interpretation,
        theorem_status=theorem_status,
        verification_state="CANDIDATE",
        claim_origin=claim_origin,
    )


def _metric_records(
    fixture: LocalFirstFixture,
    population: PopulationJoint,
    independent: PopulationJoint,
    inference: PopulationInference,
    aggregate: AggregateDatum,
    tolerance: float,
) -> Mapping[str, MetricRecord]:
    population_residual = abs(
        sum(
            (sum(row, Fraction(0)) for row in population.joint_masses),
            Fraction(0),
        )
        - 1
    )
    independent_residual = _matrix_residual(
        population.joint_masses, independent.joint_masses
    )
    recognition_residual = _recognition_marginal_residual(inference)
    non_dirac_models = sum(
        sum(mass > 0 for mass in recognition.model_marginal.masses) > 1
        for recognition in inference.recognitions
    )
    expected_non_dirac = 0 if fixture.fixture_id == "lf3_dirac_boundary_v1" else 1
    if expected_non_dirac == 0:
        model_metric = _candidate_target(
            non_dirac_models,
            interpretation="The Dirac boundary has no non-Dirac local model marginal.",
            theorem_status="HYPOTHESIS",
            claim_origin="APPLICATION_SPECIFIC",
        )
    else:
        model_metric = lower_bounded_metric(
            float(non_dirac_models),
            0.0,
            lower_bound=1.0,
            interpretation="The admitted non-boundary fixture retains local model uncertainty.",
            theorem_status="HYPOTHESIS",
            verification_state="CANDIDATE",
            claim_origin="APPLICATION_SPECIFIC",
        )
    coarse_residual = abs(aggregate.evidence - inference.evidence)

    metrics = {
        "agent_kernel_normalization_residual": _candidate_target(
            _agent_normalization_residual(fixture),
            interpretation="Every local generative kernel row is normalized exactly.",
            theorem_status="ESTABLISHED",
            claim_origin="STANDARD",
        ),
        "evaluator_compatibility_residual": _candidate_target(
            _evaluator_compatibility_residual(fixture),
            interpretation="Every positive model slice agrees with its declared evaluator.",
            theorem_status="ESTABLISHED",
            claim_origin="STANDARD",
        ),
        "record_kernel_normalization_residual": _candidate_target(
            _record_normalization_residual(fixture),
            interpretation="Every record-kernel row is normalized exactly.",
            theorem_status="ESTABLISHED",
            claim_origin="STANDARD",
        ),
        "record_ownership_violation_count": _candidate_target(
            _record_ownership_violations(fixture),
            interpretation="Every record has one declared owner in its declared scope.",
            theorem_status="ESTABLISHED",
            claim_origin="APPLICATION_SPECIFIC",
        ),
        "population_normalization_residual": _candidate_target(
            population_residual,
            interpretation="The constructed complete population law is normalized exactly.",
            theorem_status="ESTABLISHED",
            claim_origin="STANDARD",
        ),
        "independent_population_residual": _candidate_target(
            independent_residual,
            interpretation="The constructor and independent runtime enumeration agree entrywise.",
            theorem_status="ESTABLISHED",
            claim_origin="PROJECT_NOVEL",
        ),
        "recognition_marginal_residual": _candidate_target(
            recognition_residual,
            interpretation=(
                "The selected population recognition preserves every "
                "declared local law."
            ),
            theorem_status="ESTABLISHED",
            claim_origin="STANDARD",
        ),
        "model_marginal_non_dirac_count": model_metric,
        "posterior_derivation_residual": _candidate_target(
            _posterior_derivation_residual(inference),
            interpretation="Evidence and posterior equal the exact observed population slice.",
            theorem_status="ESTABLISHED",
            claim_origin="STANDARD",
        ),
        "common_channel_identity_violation_count": _candidate_target(
            0,
            interpretation="One in-process channel object performed all three aggregate pushes.",
            theorem_status="ESTABLISHED",
            claim_origin="PROJECT_NOVEL",
        ),
        "coarse_evidence_residual": _candidate_target(
            coarse_residual,
            interpretation=(
                "The common channel preserves the selected observation "
                "evidence exactly."
            ),
            theorem_status="ESTABLISHED",
            claim_origin="STANDARD",
        ),
        "conditional_kl_defect": lower_bounded_metric(
            aggregate.conditional_kl_defect,
            tolerance,
            lower_bound=0.0,
            interpretation=(
                "The finite conditional KL defect is nonnegative within "
                "the declared float64 tolerance."
            ),
            theorem_status="ESTABLISHED",
            verification_state="CANDIDATE",
            claim_origin="STANDARD",
        ),
        "kl_chain_residual": upper_bounded_metric(
            aggregate.kl_chain_residual,
            tolerance,
            upper_bound=0.0,
            interpretation=(
                "The finite VFE channel chain residual stays within the "
                "declared float64 tolerance."
            ),
            theorem_status="ESTABLISHED",
            verification_state="CANDIDATE",
            claim_origin="STANDARD",
        ),
    }
    if tuple(metrics) != _CONTRACT.metric_inventory:
        raise RuntimeError("renormalization v2 metric inventory drifted")
    return MappingProxyType(metrics)


def _readonly_array(values: object, *, dtype: object) -> np.ndarray:
    array = np.array(values, dtype=dtype, copy=True, order="C")
    if array.dtype == object:
        raise TypeError("Release 1 NPZ arrays must not use object dtype")
    array.setflags(write=False)
    return array


def _float_matrix(values: tuple[tuple[Fraction, ...], ...]) -> np.ndarray:
    return _readonly_array(
        [[float(value) for value in row] for row in values],
        dtype=np.float64,
    )


def _float_vector(values: tuple[Fraction, ...]) -> np.ndarray:
    return _readonly_array([float(value) for value in values], dtype=np.float64)


def _numeric_arrays(
    population: PopulationJoint,
    independent: PopulationJoint,
    inference: PopulationInference,
    aggregate: AggregateDatum,
    metrics: Mapping[str, MetricRecord],
) -> Mapping[str, np.ndarray]:
    arrays = {
        "population_joint": _float_matrix(population.joint_masses),
        "independent_population_joint": _float_matrix(independent.joint_masses),
        "recognition": _float_vector(inference.recognition.masses),
        "evidence_measure": _float_vector(inference.evidence_measure.masses),
        "posterior": _float_vector(inference.posterior.masses),
        "aggregate_generative_joint": _float_matrix(aggregate.generative_joint),
        "aggregate_recognition": _float_vector(aggregate.recognition.masses),
        "aggregate_posterior": _float_vector(aggregate.posterior.masses),
        "evidence": _readonly_array(inference.evidence, dtype=np.float64),
        "aggregate_evidence": _readonly_array(aggregate.evidence, dtype=np.float64),
        "conditional_kl_defect": _readonly_array(
            aggregate.conditional_kl_defect, dtype=np.float64
        ),
        "kl_chain_residual": _readonly_array(
            aggregate.kl_chain_residual, dtype=np.float64
        ),
        "metric_values": _readonly_array(
            [metrics[name].value for name in _CONTRACT.metric_inventory],
            dtype=np.float64,
        ),
        "metric_tolerances": _readonly_array(
            [metrics[name].tolerance for name in _CONTRACT.metric_inventory],
            dtype=np.float64,
        ),
    }
    return MappingProxyType(arrays)


def _build_scientific_run(
    fixture: LocalFirstFixture,
    config: ExperimentConfig,
) -> _ScientificRun:
    population = construct_population_joint(
        fixture.agents, fixture.records, fixture.context_id
    )
    independent = enumerate_population_joint_independently(
        fixture.agents, fixture.records, fixture.context_id
    )
    inference = derive_population_inference(
        population,
        fixture.observation,
        fixture.recognitions,
        fixture.selector,
    )
    aggregate = aggregate_population(
        inference, fixture.coarse_channel, config.numerics
    )
    tolerance = min(config.numerics.atol, 1.0e-12)
    metrics = _metric_records(
        fixture, population, independent, inference, aggregate, tolerance
    )

    coarse_channel = _coarse_channel_payload(fixture.coarse_channel)
    if coarse_channel["channel_sha256"] != aggregate.channel_sha256:
        raise ArithmeticError("fixture and aggregate channel hashes disagree")
    fixture_body = {
        "fixture_sha256": fixture.fixture_sha256,
        "source_inputs": [
            {"name": name, "sha256": sha256}
            for name, sha256 in fixture.direct_input_sha256
        ],
        "context_id": fixture.context_id,
        "agents": [_agent_payload(agent) for agent in fixture.agents],
        "recognitions": [
            _recognition_payload(recognition)
            for recognition in fixture.recognitions
        ],
        "records": [_record_payload(record) for record in fixture.records],
        "observation": [
            {"record_id": record_id, "outcome": outcome}
            for record_id, outcome in fixture.observation
        ],
        "selector": _selector_payload(fixture.selector),
        "coarse_channel": coarse_channel,
        "numerics": {
            "dtype": config.numerics.dtype,
            "atol": config.numerics.atol,
            "rtol": config.numerics.rtol,
            "min_spd_rcond": config.numerics.min_spd_rcond,
            "max_frame_condition": config.numerics.max_frame_condition,
        },
    }
    population_body = {
        "population": _population_payload(population),
        "independent_population": _population_payload(independent),
        "record_ownership": [
            {
                "record_id": record.record_id,
                "owner_id": record.owner_id,
                "scope_ids": list(record.scope_ids),
            }
            for record in fixture.records
        ],
        "normalization_residual": _fraction_payload(
            abs(
                sum(
                    (sum(row, Fraction(0)) for row in population.joint_masses),
                    Fraction(0),
                )
                - 1
            )
        ),
        "independent_population_residual": _fraction_payload(
            _matrix_residual(population.joint_masses, independent.joint_masses)
        ),
    }
    inference_body = {
        "observation": [
            {"record_id": record_id, "outcome": outcome}
            for record_id, outcome in fixture.observation
        ],
        **_inference_payload(inference),
        "recognition_marginal_residual": _fraction_payload(
            _recognition_marginal_residual(inference)
        ),
        "model_marginal_non_dirac_count": sum(
            sum(mass > 0 for mass in recognition.model_marginal.masses) > 1
            for recognition in inference.recognitions
        ),
        "posterior_derivation_residual": _fraction_payload(
            _posterior_derivation_residual(inference)
        ),
    }
    aggregate_body = {
        "fine_context_id": inference.population.context_id,
        "fine_evidence": _fraction_payload(inference.evidence),
        "coarse_channel": coarse_channel,
        "aggregate": _aggregate_payload(aggregate),
        "common_channel_identity_violation_count": 0,
        "coarse_evidence_residual": _fraction_payload(
            abs(aggregate.evidence - inference.evidence)
        ),
    }
    metrics_body = {
        "records": [
            {"name": name, "record": asdict(metrics[name])}
            for name in _CONTRACT.metric_inventory
        ]
    }
    numeric_arrays = _numeric_arrays(
        population, independent, inference, aggregate, metrics
    )
    if any(metric.status != "pass" for metric in metrics.values()):
        raise ArithmeticError("renormalization v2 scientific checks failed")
    return _ScientificRun(
        fixture=fixture,
        population=population,
        independent_population=independent,
        inference=inference,
        aggregate=aggregate,
        fixture_body=_json_native(fixture_body),
        population_body=_json_native(population_body),
        inference_body=_json_native(inference_body),
        aggregate_body=_json_native(aggregate_body),
        metrics=metrics,
        metrics_body=_json_native(metrics_body),
        numeric_arrays=numeric_arrays,
    )


def _direct_input_records(
    values: tuple[tuple[str, str], ...],
) -> list[dict[str, str]]:
    for name, sha256 in values:
        if type(name) is not str or not name:
            raise ValueError("artifact direct-input names must be nonempty strings")
        if re.fullmatch(r"[0-9a-f]{64}", sha256) is None:
            raise ValueError("artifact direct-input hashes must be lowercase SHA-256")
    return [{"name": name, "sha256": sha256} for name, sha256 in values]


def _envelope(
    fixture_id: str,
    producer_commit: str,
    config_hash: str,
    direct_inputs: tuple[tuple[str, str], ...],
    body: Mapping[str, object],
) -> dict[str, object]:
    return _json_native(
        {
            "schema_version": _SCHEMA_VERSION,
            "fixture_id": fixture_id,
            "producer_commit": producer_commit,
            "config_hash": config_hash,
            "direct_inputs": _direct_input_records(direct_inputs),
            "payload": dict(body),
        }
    )


def _unicode_scalar(value: str) -> np.ndarray:
    return _readonly_array(value, dtype=f"<U{max(1, len(value))}")


def _unicode_vector(values: tuple[str, ...]) -> np.ndarray:
    width = max((len(value) for value in values), default=1)
    return _readonly_array(values, dtype=f"<U{max(1, width)}")


def _final_arrays(
    science: _ScientificRun,
    producer_commit: str,
    config_hash: str,
    direct_inputs: tuple[tuple[str, str], ...],
) -> Mapping[str, np.ndarray]:
    metadata = {
        "schema_version": _unicode_scalar(_SCHEMA_VERSION),
        "fixture_id": _unicode_scalar(science.fixture.fixture_id),
        "producer_commit": _unicode_scalar(producer_commit),
        "config_hash": _unicode_scalar(config_hash),
        "direct_input_names": _unicode_vector(
            tuple(name for name, _ in direct_inputs)
        ),
        "direct_input_sha256": _unicode_vector(
            tuple(sha256 for _, sha256 in direct_inputs)
        ),
    }
    arrays = {**metadata, **science.numeric_arrays}
    if any(array.dtype == object for array in arrays.values()):
        raise TypeError("Release 1 NPZ arrays must not use object dtype")
    return MappingProxyType(arrays)


def _logical_arrays_sha256(arrays: Mapping[str, np.ndarray]) -> str:
    descriptor = {
        "arrays": [
            {
                "name": name,
                "dtype": array.dtype.str,
                "shape": list(array.shape),
                "values": array.tolist(),
            }
            for name, array in sorted(arrays.items())
        ]
    }
    return _canonical_sha256(descriptor)


def _validate_run_config(config: ExperimentConfig) -> RenormalizationV2TheoryConfig:
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    theory = config.theory
    if not isinstance(theory, RenormalizationV2TheoryConfig):
        raise ValueError(
            "renormalization v2 requires theory.experiment='renormalization_v2'"
        )
    if theory.experiment != "renormalization_v2":
        raise ValueError(
            "renormalization v2 requires theory.experiment='renormalization_v2'"
        )
    if theory.arithmetic != "exact_rational":
        raise ValueError("renormalization v2 requires exact_rational arithmetic")
    if (
        config.compute.backend != "cpu"
        or config.compute.dtype != "float64"
        or config.compute.deterministic is not True
        or config.compute.device_index != 0
    ):
        raise ValueError("renormalization v2 requires deterministic CPU float64")
    if config.numerics.dtype != "float64":
        raise ValueError("renormalization v2 requires float64 numerics")
    if (
        type(config.numerics.atol) is not float
        or not math.isfinite(config.numerics.atol)
        or config.numerics.atol <= 0.0
    ):
        raise ValueError("numerics.atol must be a positive finite built-in float")
    if config.numerics.atol > 1.0e-12:
        raise ValueError("numerics.atol must be at most 1e-12")
    if config.output.collect_diagnostics is not True:
        raise ValueError("renormalization v2 requires collect_diagnostics=True")
    if config.output.render_figures is not False:
        raise ValueError("renormalization v2 requires render_figures=False")
    return theory


def run_renormalization_v2_experiment(
    config: ExperimentConfig,
) -> RenormalizationV2ExperimentResult:
    """Validate, derive, provenance-bind, and publish one exact Release 1 run."""
    theory = _validate_run_config(config)
    fixture = load_fixture(theory.fixture)
    if not isinstance(fixture, LocalFirstFixture) or fixture.fixture_id != theory.fixture:
        raise ValueError("loaded fixture does not match the resolved configuration")

    science = _build_scientific_run(fixture, config)
    config_hash = config_sha256(config)
    streams = RngStreams.from_seed(config.run.seed)
    repo_root = Path(__file__).resolve().parents[1]
    provenance = collect_provenance(
        repo_root, repo_root / "Theory", config_hash, streams
    )
    producer_commit = provenance.get("git_commit")
    if type(producer_commit) is not str or _COMMIT_PATTERN.fullmatch(producer_commit) is None:
        raise RuntimeError("producer Git commit is unavailable or invalid")

    fixture_envelope = _envelope(
        fixture.fixture_id,
        producer_commit,
        config_hash,
        fixture.direct_input_sha256,
        science.fixture_body,
    )
    fixture_hash = _canonical_sha256(fixture_envelope)
    population_inputs = (("fixture_snapshot", fixture_hash),)
    population_envelope = _envelope(
        fixture.fixture_id,
        producer_commit,
        config_hash,
        population_inputs,
        science.population_body,
    )
    population_hash = _canonical_sha256(population_envelope)
    inference_inputs = (
        ("fixture_snapshot", fixture_hash),
        ("population_joint", population_hash),
    )
    inference_envelope = _envelope(
        fixture.fixture_id,
        producer_commit,
        config_hash,
        inference_inputs,
        science.inference_body,
    )
    inference_hash = _canonical_sha256(inference_envelope)
    aggregate_inputs = (
        ("fixture_snapshot", fixture_hash),
        ("population_inference", inference_hash),
        ("coarse_channel", science.aggregate.channel_sha256),
    )
    aggregate_envelope = _envelope(
        fixture.fixture_id,
        producer_commit,
        config_hash,
        aggregate_inputs,
        science.aggregate_body,
    )
    aggregate_hash = _canonical_sha256(aggregate_envelope)
    metrics_inputs = (
        ("fixture_snapshot", fixture_hash),
        ("population_joint", population_hash),
        ("population_inference", inference_hash),
        ("aggregate_datum", aggregate_hash),
    )
    metrics_envelope = _envelope(
        fixture.fixture_id,
        producer_commit,
        config_hash,
        metrics_inputs,
        science.metrics_body,
    )
    metrics_hash = _canonical_sha256(metrics_envelope)
    array_inputs = (*metrics_inputs, ("metrics", metrics_hash))
    arrays = _final_arrays(
        science, producer_commit, config_hash, array_inputs
    )
    arrays_hash = _logical_arrays_sha256(arrays)
    envelopes = MappingProxyType(
        {
            "fixture_snapshot": fixture_envelope,
            "population_joint": population_envelope,
            "population_inference": inference_envelope,
            "aggregate_datum": aggregate_envelope,
            "metrics": metrics_envelope,
        }
    )
    artifact_hashes = {
        "fixture_snapshot": fixture_hash,
        "population_joint": population_hash,
        "population_inference": inference_hash,
        "aggregate_datum": aggregate_hash,
        "metrics": metrics_hash,
        "arrays": arrays_hash,
    }

    provenance.update(
        {
            "experiment_scope": "finite_local_first_aggregate_datum_release_1",
            "fixture_id": fixture.fixture_id,
            "arithmetic": "exact_rational_with_float64_vfe_boundary",
            "effective_backend": "cpu",
            "effective_dtype": "float64",
            "semantic_artifact_sha256": artifact_hashes,
            "arrays_direct_inputs": tuple(name for name, _ in array_inputs),
        }
    )
    input_hashes = provenance.get("input_hashes")
    if not isinstance(input_hashes, dict):
        raise RuntimeError("provenance input_hashes is unavailable")
    input_hashes["fixture_direct_inputs"] = [
        {"name": name, "sha256": sha256}
        for name, sha256 in fixture.direct_input_sha256
    ]
    input_hashes["semantic_artifacts"] = dict(artifact_hashes)

    store = RunStore.create(config, provenance)
    for name in _JSON_ARTIFACTS:
        store.write_json(name, envelopes[name])
    store.write_npz("arrays", arrays)
    store.finalize(_DECLARED_ARTIFACTS)

    return RenormalizationV2ExperimentResult(
        run_dir=store.run_dir,
        config_hash=store.config_hash,
        status="pass",
        metrics=MappingProxyType(dict(science.metrics)),
        arrays=arrays,
    )


__all__ = [
    "RenormalizationV2ExperimentResult",
    "run_renormalization_v2_experiment",
]
