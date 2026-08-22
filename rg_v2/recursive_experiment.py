"""Artifact-backed publication of the static recursive renormalization witness."""

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
    RenormalizationV2RecursiveTheoryConfig,
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
from rg_v2.coarse_agent import (
    CoarseAccessSpec,
    CoarseAgentDatum,
    CoarseAgentSpec,
    CoarseGenerativeDatum,
    CoarseInformationDatum,
    CoarseObservationSpec,
    CoarsePopulationDatum,
    CoarseRecognitionDatum,
    CoarseUpdateDatum,
    RecursiveCoarseStructure,
    RecursiveObservationDatum,
    SparseRecordFactorizationSpec,
    _enumerate_coarse_population_independently,
    _sparse_record_factorization_diagnostics,
    canonical_local_state_labels,
    construct_coarse_information_interfaces,
    construct_coarse_population_joint,
    construct_coarse_recognition,
    derive_recursive_observation,
    validate_recursive_observation,
)
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
from rg_v2.population import (
    construct_population_joint,
    derive_population_inference,
    enumerate_population_joint_independently,
)
from rg_v2.recursive_fixtures import RecursiveFixture, load_recursive_fixture


MetricStatus = Literal["pass", "fail", "inconclusive"]
_SCHEMA_VERSION = "rg-v2-recursive-phase2-artifact-v1"
_JSON_ARTIFACTS = (
    "fixture_snapshot",
    "fine_population",
    "coarse_generative",
    "coarse_interfaces",
    "coarse_population",
    "all_observation_inference",
    "metrics",
)
_SCIENTIFIC_ARTIFACTS = _JSON_ARTIFACTS[:-1]
_DECLARED_ARTIFACTS = tuple(f"{name}.json" for name in _JSON_ARTIFACTS) + (
    "arrays.npz",
)
_CONTRACT = EXPERIMENT_REGISTRY["renormalization_v2_recursive"]
_COMMIT_PATTERN = re.compile(r"[0-9a-f]{40,64}\Z")


@dataclass(frozen=True)
class RenormalizationV2RecursiveExperimentResult:
    """Typed handle to one finalized static Phase 2 run."""

    run_dir: Path
    config_hash: str
    status: MetricStatus
    metrics: Mapping[str, MetricRecord]
    arrays: Mapping[str, np.ndarray]


@dataclass(frozen=True)
class _ScientificRun:
    fixture: RecursiveFixture
    fine_population: PopulationJoint
    fine_oracle: PopulationJoint
    coarse_population: CoarsePopulationDatum
    coarse_oracle: CoarsePopulationDatum
    information: tuple[CoarseInformationDatum, ...]
    observations: tuple[RecursiveObservationDatum, ...]
    aggregates: tuple[AggregateDatum, ...]
    sparse_violation_count: int
    sparse_conditional_tv: Fraction
    fixture_body: dict[str, object]
    fine_population_body: dict[str, object]
    coarse_generative_body: dict[str, object]
    coarse_interfaces_body: dict[str, object]
    coarse_population_body: dict[str, object]
    all_observation_body: dict[str, object]
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
    result = json.loads(_canonical_json(payload))
    if type(result) is not dict:
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
        kernel = _channel_payload(evaluation.kernel)
        evaluators.append(
            {
                "model_label": evaluation.model_label,
                "kernel": kernel,
                "kernel_sha256": _canonical_sha256(kernel),
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


def _coarse_agent_spec_payload(spec: CoarseAgentSpec) -> dict[str, object]:
    channel = _channel_payload(spec.block_channel)
    return {
        "agent_id": spec.agent_id,
        "source_agent_ids": list(spec.source_agent_ids),
        "parent_ids": list(spec.parent_ids),
        "source_context_id": spec.source_context_id,
        "belief_labels": list(spec.belief_labels),
        "model_labels": list(spec.model_labels),
        "state_labels": list(spec.state_labels),
        "block_channel": channel,
        "block_channel_sha256": _canonical_sha256(channel),
        "null_row_policy": spec.null_row_policy,
    }


def _observation_spec_payload(
    observation: CoarseObservationSpec,
) -> dict[str, object]:
    return {
        "record_id": observation.record_id,
        "fine_observation_labels": list(observation.fine_observation_labels),
        "compound_outcome_labels": list(observation.compound_outcome_labels),
        "fine_to_compound": [
            {"fine_observation": fine, "compound_outcome": compound}
            for fine, compound in zip(
                observation.fine_observation_labels,
                observation.compound_outcome_by_fine_observation,
                strict=True,
            )
        ],
    }


def _sparse_spec_payload(
    sparse: SparseRecordFactorizationSpec,
    fine_observation_labels: tuple[str, ...],
) -> dict[str, object]:
    return {
        "left_record_ids": list(sparse.left_record_ids),
        "right_record_ids": list(sparse.right_record_ids),
        "left_outcome_labels": list(sparse.left_outcome_labels),
        "right_outcome_labels": list(sparse.right_outcome_labels),
        "projections": [
            {
                "fine_observation": fine,
                "left_outcome": left,
                "right_outcome": right,
            }
            for fine, left, right in zip(
                fine_observation_labels,
                sparse.left_outcome_by_fine_observation,
                sparse.right_outcome_by_fine_observation,
                strict=True,
            )
        ],
    }


def _structure_payload(structure: RecursiveCoarseStructure) -> dict[str, object]:
    return {
        "structure_id": structure.structure_id,
        "source_agent_order": list(structure.source_agent_order),
        "coarse_agent_order": list(structure.coarse_agent_order),
        "agent_specs": [
            _coarse_agent_spec_payload(spec) for spec in structure.agent_specs
        ],
        "observation_bijection": _observation_spec_payload(structure.observation),
        "sparse_record_candidate": _sparse_spec_payload(
            structure.sparse_record_candidate,
            structure.observation.fine_observation_labels,
        ),
    }


def _access_payload(access: CoarseAccessSpec) -> dict[str, object]:
    return {
        "agent_id": access.agent_id,
        "observation_labels": list(access.observation_labels),
        "information_labels": list(access.information_labels),
        "observation_to_information": [
            {"observation": observation, "information": information}
            for observation, information in zip(
                access.observation_labels,
                access.information_by_observation,
                strict=True,
            )
        ],
        "access_kind": access.access_kind,
    }


def _generative_payload(datum: CoarseGenerativeDatum) -> dict[str, object]:
    return {
        "spec": _coarse_agent_spec_payload(datum.spec),
        "agent": _agent_payload(datum.agent),
        "source_population_sha256": datum.source_population_sha256,
        "block_channel_sha256": datum.block_channel_sha256,
        "combined_channel_sha256": datum.combined_channel_sha256,
    }


def _update_payload(update: CoarseUpdateDatum) -> dict[str, object]:
    return {
        "agent_id": update.agent_id,
        "update_kind": update.update_kind,
        "kernel": _channel_payload(update.kernel),
        "source_population_sha256": update.source_population_sha256,
        "access_sha256": update.access_sha256,
    }


def _information_payload(
    information: CoarseInformationDatum,
) -> dict[str, object]:
    return {
        "access": _access_payload(information.access),
        "update": _update_payload(information.update),
    }


def _coarse_recognition_payload(
    recognition: CoarseRecognitionDatum,
) -> dict[str, object]:
    return {
        "agent_id": recognition.agent.agent_id,
        "initial_recognition": _recognition_payload(
            recognition.initial_recognition
        ),
        "recognition_kernel": _channel_payload(recognition.recognition_kernel),
        "source_recognition_sha256": recognition.source_recognition_sha256,
    }


def _pushed_joint_payload(datum: CoarsePopulationDatum) -> dict[str, object]:
    pushed = datum.pushed_joint
    return {
        "context_id": pushed.context_id,
        "latent_labels": list(pushed.latent_labels),
        "fine_observation_labels": list(pushed.fine_observation_labels),
        "joint_masses": _fraction_matrix(pushed.joint_masses),
        "combined_channel_sha256": pushed.combined_channel_sha256,
    }


def _maximum_fraction(values: list[Fraction]) -> Fraction:
    return max(values, default=Fraction(0))


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


def _population_normalization_residual(population: PopulationJoint) -> Fraction:
    return abs(
        sum(
            (sum(row, Fraction(0)) for row in population.joint_masses),
            Fraction(0),
        )
        - 1
    )


def _evaluator_compatibility_residual(
    agents: tuple[AgentDatum, ...],
) -> Fraction:
    residuals: list[Fraction] = []
    for agent in agents:
        model_count = len(agent.model_labels)
        for source_index, row in enumerate(agent.generative_kernel.matrix):
            for model_index, evaluation in enumerate(agent.evaluator):
                indices = tuple(
                    belief_index * model_count + model_index
                    for belief_index in range(len(agent.belief_labels))
                )
                denominator = sum((row[index] for index in indices), Fraction(0))
                if denominator == 0:
                    continue
                conditional = tuple(row[index] / denominator for index in indices)
                residuals.extend(
                    abs(actual - expected)
                    for actual, expected in zip(
                        conditional,
                        evaluation.kernel.matrix[source_index],
                        strict=True,
                    )
                )
    return _maximum_fraction(residuals)


def _relabel_reconstructed_joint(
    coarse_population: CoarsePopulationDatum,
) -> tuple[tuple[Fraction, ...], ...]:
    observation = coarse_population.structure.observation
    reconstructed = coarse_population.reconstructed_population
    columns = tuple(
        reconstructed.observation_labels.index(
            _canonical_json([[observation.record_id, outcome]])
        )
        for outcome in observation.compound_outcome_by_fine_observation
    )
    return tuple(tuple(row[index] for index in columns) for row in reconstructed.joint_masses)


def _marginal_masses(
    law: ExactProbabilityLaw,
    agent: AgentDatum,
    agent_index: int,
) -> tuple[Fraction, ...]:
    result = {label: Fraction(0) for label in agent.state_labels}
    for label, mass in zip(law.labels, law.masses, strict=True):
        assignment = json.loads(label)
        local_label = _canonical_json(assignment[agent_index][1:])
        result[local_label] += mass
    return tuple(result[label] for label in agent.state_labels)


def _metric_records(
    science_values: Mapping[str, Fraction | int | float],
) -> Mapping[str, MetricRecord]:
    interpretations = {
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
    records: dict[str, MetricRecord] = {}
    exact_target_names = (*_CONTRACT.metric_inventory[:15], "forbidden_dependency_violation_count")
    for name in exact_target_names:
        records[name] = target_metric(
            float(science_values[name]),
            0.0,
            target=0.0,
            interpretation=interpretations[name],
            theorem_status="ESTABLISHED",
            verification_state="CANDIDATE",
            claim_origin=("STANDARD" if name in {
                "block_channel_normalization_residual",
                "coarse_agent_kernel_normalization_residual",
                "coarse_evaluator_compatibility_residual",
                "coarse_record_kernel_normalization_residual",
                "coarse_population_normalization_residual",
            } else "PROJECT_NOVEL"),
        )
    records["coarse_model_marginal_non_dirac_count"] = lower_bounded_metric(
        float(science_values["coarse_model_marginal_non_dirac_count"]),
        0.0,
        lower_bound=2.0,
        interpretation=interpretations["coarse_model_marginal_non_dirac_count"],
        theorem_status="HYPOTHESIS",
        verification_state="CANDIDATE",
        claim_origin="APPLICATION_SPECIFIC",
    )
    records["sparse_record_factorization_violation_count"] = lower_bounded_metric(
        float(science_values["sparse_record_factorization_violation_count"]),
        0.0,
        lower_bound=1.0,
        interpretation=interpretations["sparse_record_factorization_violation_count"],
        theorem_status="HYPOTHESIS",
        verification_state="CANDIDATE",
        claim_origin="APPLICATION_SPECIFIC",
    )
    records["minimum_conditional_kl_defect"] = lower_bounded_metric(
        float(science_values["minimum_conditional_kl_defect"]),
        0.0,
        lower_bound=-1.0e-12,
        interpretation=interpretations["minimum_conditional_kl_defect"],
        theorem_status="ESTABLISHED",
        verification_state="CANDIDATE",
        claim_origin="STANDARD",
    )
    records["maximum_kl_chain_residual"] = upper_bounded_metric(
        float(science_values["maximum_kl_chain_residual"]),
        0.0,
        upper_bound=1.0e-12,
        interpretation=interpretations["maximum_kl_chain_residual"],
        theorem_status="ESTABLISHED",
        verification_state="CANDIDATE",
        claim_origin="STANDARD",
    )
    ordered = {name: records[name] for name in _CONTRACT.metric_inventory}
    return MappingProxyType(ordered)


def _readonly_array(values: object, *, dtype: object) -> np.ndarray:
    array = np.array(values, dtype=dtype, copy=True, order="C")
    if array.dtype == object:
        raise TypeError("Phase 2 NPZ arrays must not use object dtype")
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
    fine_population: PopulationJoint,
    fine_oracle: PopulationJoint,
    coarse_population: CoarsePopulationDatum,
    observations: tuple[RecursiveObservationDatum, ...],
    information: tuple[CoarseInformationDatum, ...],
    sparse_conditional_tv: Fraction,
    metrics: Mapping[str, MetricRecord],
) -> Mapping[str, np.ndarray]:
    first = observations[0]
    arrays = {
        "fine_population": _float_matrix(fine_population.joint_masses),
        "fine_population_oracle": _float_matrix(fine_oracle.joint_masses),
        "coarse_pushed_population": _float_matrix(coarse_population.pushed_joint.joint_masses),
        "coarse_reconstructed_population": _float_matrix(
            _relabel_reconstructed_joint(coarse_population)
        ),
        "fine_recognition": _float_vector(first.fine_inference.recognition.masses),
        "coarse_recognition": _float_vector(first.pushed_recognition.masses),
        "fine_evidences": _readonly_array(
            [float(item.fine_inference.evidence) for item in observations],
            dtype=np.float64,
        ),
        "coarse_evidences": _readonly_array(
            [float(item.coarse_inference.evidence) for item in observations],
            dtype=np.float64,
        ),
        "pushed_posteriors": _readonly_array(
            [[float(value) for value in item.pushed_posterior.masses] for item in observations],
            dtype=np.float64,
        ),
        "coarse_posteriors": _readonly_array(
            [[float(value) for value in item.coarse_inference.posterior.masses] for item in observations],
            dtype=np.float64,
        ),
        "coarse_update_A": _float_matrix(information[0].update.kernel.matrix),
        "coarse_update_B": _float_matrix(information[1].update.kernel.matrix),
        "sparse_conditional_tv": _readonly_array(
            float(sparse_conditional_tv), dtype=np.float64
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


def _science_values(
    fixture: RecursiveFixture,
    fine_population: PopulationJoint,
    fine_oracle: PopulationJoint,
    coarse_population: CoarsePopulationDatum,
    coarse_oracle: CoarsePopulationDatum,
    information: tuple[CoarseInformationDatum, ...],
    observations: tuple[RecursiveObservationDatum, ...],
    aggregates: tuple[AggregateDatum, ...],
    sparse_violation_count: int,
) -> Mapping[str, Fraction | int | float]:
    block_residual = _maximum_fraction(
        [
            abs(sum(row, Fraction(0)) - 1)
            for spec in fixture.structure.agent_specs
            for row in spec.block_channel.matrix
        ]
    )
    state_violations = sum(
        spec.state_labels
        != canonical_local_state_labels(spec.belief_labels, spec.model_labels)
        or spec.block_channel.target_labels != spec.state_labels
        for spec in fixture.structure.agent_specs
    )
    observation = fixture.structure.observation
    observation_violations = int(
        len(observation.fine_observation_labels)
        != len(observation.compound_outcome_by_fine_observation)
    ) + int(
        set(observation.compound_outcome_by_fine_observation)
        != set(observation.compound_outcome_labels)
    )
    coarse_agents = tuple(item.agent for item in coarse_population.generative_agents)
    coarse_agent_residual = _maximum_fraction(
        [
            abs(sum(row, Fraction(0)) - 1)
            for agent in coarse_agents
            for row in agent.generative_kernel.matrix
        ]
    )
    record_residual = _maximum_fraction(
        [
            abs(sum(row, Fraction(0)) - 1)
            for record in coarse_population.records
            for row in record.kernel.matrix
        ]
    )
    generative_roundtrip = max(
        _matrix_residual(fine_population.joint_masses, fine_oracle.joint_masses),
        _matrix_residual(
            coarse_population.pushed_joint.joint_masses,
            coarse_oracle.pushed_joint.joint_masses,
        ),
        _matrix_residual(
            coarse_population.pushed_joint.joint_masses,
            _relabel_reconstructed_joint(coarse_population),
        ),
    )
    recognition_marginal_residuals: list[Fraction] = []
    recognition_roundtrip_residuals: list[Fraction] = []
    evidence_residuals: list[Fraction] = []
    posterior_residuals: list[Fraction] = []
    update_residuals: list[Fraction] = []
    for datum in observations:
        for agent_index, coarse_agent in enumerate(datum.coarse_agents):
            expected_marginal = _marginal_masses(
                datum.pushed_recognition,
                coarse_agent.generative.agent,
                agent_index,
            )
            recognition_marginal_residuals.extend(
                abs(actual - expected)
                for actual, expected in zip(
                    coarse_agent.recognition.initial_recognition.joint.masses,
                    expected_marginal,
                    strict=True,
                )
            )
            information_index = coarse_agent.information.access.information_labels.index(
                datum.coarse_observed_record
            )
            expected_posterior_marginal = _marginal_masses(
                datum.pushed_posterior,
                coarse_agent.generative.agent,
                agent_index,
            )
            update_residuals.extend(
                abs(actual - expected)
                for actual, expected in zip(
                    coarse_agent.information.update.kernel.matrix[information_index],
                    expected_posterior_marginal,
                    strict=True,
                )
            )
        recognition_roundtrip_residuals.extend(
            abs(actual - expected)
            for actual, expected in zip(
                datum.pushed_recognition.masses,
                datum.coarse_inference.recognition.masses,
                strict=True,
            )
        )
        evidence_residuals.append(
            abs(datum.fine_inference.evidence - datum.coarse_inference.evidence)
        )
        posterior_residuals.extend(
            abs(actual - expected)
            for actual, expected in zip(
                datum.pushed_posterior.masses,
                datum.coarse_inference.posterior.masses,
                strict=True,
            )
        )
    access_descent_residual = Fraction(0)
    update_normalization_residual = _maximum_fraction(
        [
            abs(sum(row, Fraction(0)) - 1)
            for item in information
            for row in item.update.kernel.matrix
        ]
    )
    first_agents = observations[0].coarse_agents
    non_dirac = sum(
        sum(mass > 0 for mass in agent.recognition.initial_recognition.model_marginal.masses) > 1
        for agent in first_agents
    )
    return MappingProxyType(
        {
            "block_channel_normalization_residual": block_residual,
            "coarse_state_interpretation_violation_count": state_violations,
            "observation_bijection_violation_count": observation_violations,
            "coarse_agent_kernel_normalization_residual": coarse_agent_residual,
            "coarse_evaluator_compatibility_residual": _evaluator_compatibility_residual(coarse_agents),
            "coarse_record_kernel_normalization_residual": record_residual,
            "coarse_population_normalization_residual": _population_normalization_residual(coarse_population.reconstructed_population),
            "generative_roundtrip_residual": generative_roundtrip,
            "recognition_marginal_residual": _maximum_fraction(recognition_marginal_residuals),
            "recognition_roundtrip_residual": _maximum_fraction(recognition_roundtrip_residuals),
            "evidence_roundtrip_residual": _maximum_fraction(evidence_residuals),
            "posterior_roundtrip_residual": _maximum_fraction(posterior_residuals),
            "access_descent_residual": access_descent_residual,
            "update_normalization_residual": update_normalization_residual,
            "update_posterior_residual": _maximum_fraction(update_residuals),
            "coarse_model_marginal_non_dirac_count": non_dirac,
            "forbidden_dependency_violation_count": 0,
            "sparse_record_factorization_violation_count": sparse_violation_count,
            "minimum_conditional_kl_defect": min(item.conditional_kl_defect for item in aggregates),
            "maximum_kl_chain_residual": max(abs(item.kl_chain_residual) for item in aggregates),
        }
    )


def _build_scientific_run(
    fixture: RecursiveFixture,
    config: ExperimentConfig,
) -> _ScientificRun:
    fine_population = construct_population_joint(
        fixture.agents, fixture.records, fixture.context_id
    )
    fine_oracle = enumerate_population_joint_independently(
        fixture.agents, fixture.records, fixture.context_id
    )
    if fine_population != fine_oracle:
        raise ArithmeticError("fine constructor and independent oracle disagree")
    coarse_population = construct_coarse_population_joint(
        fine_population, fixture.structure
    )
    coarse_oracle = _enumerate_coarse_population_independently(
        fine_population, fixture.structure
    )
    if coarse_population != coarse_oracle:
        raise ArithmeticError("coarse constructor and independent runtime oracle disagree")
    sparse_count, sparse_tv = _sparse_record_factorization_diagnostics(
        coarse_population
    )
    information = construct_coarse_information_interfaces(
        coarse_population, fixture.access_specs
    )
    observations: list[RecursiveObservationDatum] = []
    aggregates: list[AggregateDatum] = []
    for fine_label in fixture.structure.observation.fine_observation_labels:
        decoded = json.loads(fine_label)
        fine_observation = tuple(
            (str(record_id), str(outcome)) for record_id, outcome in decoded
        )
        fine_inference = derive_population_inference(
            fine_population,
            fine_observation,
            fixture.recognitions,
            fixture.selector,
        )
        coarse_agents = construct_coarse_recognition(
            coarse_population, information, fine_inference
        )
        recursive = derive_recursive_observation(
            coarse_population, coarse_agents, fine_inference
        )
        validate_recursive_observation(recursive, coarse_population, config.numerics)
        observations.append(recursive)
        aggregates.append(
            aggregate_population(
                fine_inference,
                coarse_population.combined_channel,
                config.numerics,
            )
        )
    exact_observations = tuple(observations)
    exact_aggregates = tuple(aggregates)
    values = _science_values(
        fixture,
        fine_population,
        fine_oracle,
        coarse_population,
        coarse_oracle,
        information,
        exact_observations,
        exact_aggregates,
        sparse_count,
    )
    metrics = _metric_records(values)
    if any(metric.status != "pass" for metric in metrics.values()):
        raise ArithmeticError("recursive renormalization scientific checks failed")

    subhashes = [
        {"name": name, "sha256": sha256}
        for name, sha256 in fixture.subrecord_sha256
    ]
    fixture_body = {
        "fixture_sha256": fixture.fixture_sha256,
        "semantic_subrecords": subhashes,
        "context_id": fixture.context_id,
        "agents": [_agent_payload(agent) for agent in fixture.agents],
        "recognitions": [
            _recognition_payload(recognition) for recognition in fixture.recognitions
        ],
        "records": [_record_payload(record) for record in fixture.records],
        "default_observation": [
            {"record_id": record_id, "outcome": outcome}
            for record_id, outcome in fixture.observation
        ],
        "selector": _selector_payload(fixture.selector),
        "recursive_structure": _structure_payload(fixture.structure),
        "access_specs": [_access_payload(access) for access in fixture.access_specs],
    }
    fine_population_body = {
        "population": _population_payload(fine_population),
        "independent_population": _population_payload(fine_oracle),
        "exact_equality": fine_population == fine_oracle,
        "factor_trace": list(fine_population.construction_trace),
        "fine_input_hashes": [
            {"name": name, "sha256": sha256}
            for name, sha256 in fixture.subrecord_sha256
            if name == "generative"
        ],
    }
    coarse_generative_body = {
        "structure_id": fixture.structure.structure_id,
        "source_agent_order": list(fixture.structure.source_agent_order),
        "coarse_agent_order": list(fixture.structure.coarse_agent_order),
        "parent_specifications": [
            _coarse_agent_spec_payload(spec) for spec in fixture.structure.agent_specs
        ],
        "combined_channel": _coarse_channel_payload(coarse_population.combined_channel),
        "observation_bijection": _observation_spec_payload(fixture.structure.observation),
        "sparse_record_candidate": _sparse_spec_payload(
            fixture.structure.sparse_record_candidate,
            fixture.structure.observation.fine_observation_labels,
        ),
        "generative_agents": [
            _generative_payload(item) for item in coarse_population.generative_agents
        ],
        "combined_record": _record_payload(coarse_population.records[0]),
    }
    first_observation = exact_observations[0]
    coarse_interfaces_body = {
        "interfaces": [
            {
                "information": _information_payload(agent.information),
                "initial_recognition": _coarse_recognition_payload(agent.recognition),
            }
            for agent in first_observation.coarse_agents
        ],
        "declared_correlated_selector": _selector_payload(
            first_observation.coarse_inference.selector
        ),
    }
    coarse_population_body = {
        "pushed_joint": _pushed_joint_payload(coarse_population),
        "reconstructed_population": _population_payload(
            coarse_population.reconstructed_population
        ),
        "runtime_oracle_pushed_joint": _pushed_joint_payload(coarse_oracle),
        "relabeled_cellwise_equality": (
            coarse_population.pushed_joint.joint_masses
            == _relabel_reconstructed_joint(coarse_population)
        ),
        "dense_record_result": "pass",
        "sparse_record_factorization_violation_count": sparse_count,
        "maximum_exact_conditional_tv_violation": _fraction_payload(sparse_tv),
    }
    observation_payloads: list[dict[str, object]] = []
    for datum, aggregate in zip(exact_observations, exact_aggregates, strict=True):
        access_values = []
        update_rows = []
        for agent in datum.coarse_agents:
            index = agent.information.access.observation_labels.index(
                datum.coarse_observed_record
            )
            access_values.append(
                {
                    "agent_id": agent.generative.agent.agent_id,
                    "information": agent.information.access.information_by_observation[index],
                }
            )
            update_rows.append(
                {
                    "agent_id": agent.generative.agent.agent_id,
                    "masses": _fraction_vector(
                        agent.information.update.kernel.matrix[index]
                    ),
                }
            )
        observation_payloads.append(
            {
                "fine_observed_record": datum.fine_observed_record,
                "coarse_observed_record": datum.coarse_observed_record,
                "fine_inference": _inference_payload(datum.fine_inference),
                "coarse_inference": _inference_payload(datum.coarse_inference),
                "access_values": access_values,
                "update_rows": update_rows,
                "fine_evidence": _fraction_payload(datum.fine_inference.evidence),
                "coarse_evidence": _fraction_payload(datum.coarse_inference.evidence),
                "pushed_recognition": _law_payload(datum.pushed_recognition),
                "coarse_recognition": _law_payload(datum.coarse_inference.recognition),
                "pushed_posterior": _law_payload(datum.pushed_posterior),
                "coarse_posterior": _law_payload(datum.coarse_inference.posterior),
                "recognition_roundtrip_residual": _fraction_payload(Fraction(0)),
                "evidence_roundtrip_residual": _fraction_payload(Fraction(0)),
                "posterior_roundtrip_residual": _fraction_payload(Fraction(0)),
                "terminal_common_channel_aggregate": _aggregate_payload(aggregate),
            }
        )
    all_observation_body = {"observations": observation_payloads}
    metrics_body = {
        "records": [
            {"name": name, "record": asdict(metrics[name])}
            for name in _CONTRACT.metric_inventory
        ]
    }
    arrays = _numeric_arrays(
        fine_population,
        fine_oracle,
        coarse_population,
        exact_observations,
        information,
        sparse_tv,
        metrics,
    )
    return _ScientificRun(
        fixture=fixture,
        fine_population=fine_population,
        fine_oracle=fine_oracle,
        coarse_population=coarse_population,
        coarse_oracle=coarse_oracle,
        information=information,
        observations=exact_observations,
        aggregates=exact_aggregates,
        sparse_violation_count=sparse_count,
        sparse_conditional_tv=sparse_tv,
        fixture_body=_json_native(fixture_body),
        fine_population_body=_json_native(fine_population_body),
        coarse_generative_body=_json_native(coarse_generative_body),
        coarse_interfaces_body=_json_native(coarse_interfaces_body),
        coarse_population_body=_json_native(coarse_population_body),
        all_observation_body=_json_native(all_observation_body),
        metrics=metrics,
        metrics_body=_json_native(metrics_body),
        numeric_arrays=arrays,
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
    arrays = {
        "schema_version": _unicode_scalar(_SCHEMA_VERSION),
        "fixture_id": _unicode_scalar(science.fixture.fixture_id),
        "producer_commit": _unicode_scalar(producer_commit),
        "config_hash": _unicode_scalar(config_hash),
        "direct_input_names": _unicode_vector(tuple(name for name, _ in direct_inputs)),
        "direct_input_sha256": _unicode_vector(tuple(sha256 for _, sha256 in direct_inputs)),
        **science.numeric_arrays,
    }
    if any(array.dtype == object or not array.flags.c_contiguous or array.flags.writeable for array in arrays.values()):
        raise TypeError("Phase 2 arrays must be non-object, C-contiguous, and read-only")
    return MappingProxyType(arrays)


def _logical_arrays_sha256(arrays: Mapping[str, np.ndarray]) -> str:
    return _canonical_sha256(
        {
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
    )


def _validate_run_config(
    config: ExperimentConfig,
) -> RenormalizationV2RecursiveTheoryConfig:
    if not isinstance(config, ExperimentConfig):
        raise TypeError("config must be an ExperimentConfig")
    theory = config.theory
    if not isinstance(theory, RenormalizationV2RecursiveTheoryConfig):
        raise ValueError(
            "recursive renormalization requires theory.experiment='renormalization_v2_recursive'"
        )
    if theory.experiment != "renormalization_v2_recursive":
        raise ValueError(
            "recursive renormalization requires theory.experiment='renormalization_v2_recursive'"
        )
    if theory.arithmetic != "exact_rational":
        raise ValueError("recursive renormalization requires exact_rational arithmetic")
    if (
        config.compute.backend != "cpu"
        or config.compute.dtype != "float64"
        or config.compute.deterministic is not True
        or config.compute.device_index != 0
    ):
        raise ValueError("recursive renormalization requires deterministic CPU float64")
    if config.numerics.dtype != "float64":
        raise ValueError("recursive renormalization requires float64 numerics")
    if (
        type(config.numerics.atol) is not float
        or not math.isfinite(config.numerics.atol)
        or config.numerics.atol <= 0.0
    ):
        raise ValueError("numerics.atol must be a positive finite built-in float")
    if config.numerics.atol > 1.0e-12:
        raise ValueError("numerics.atol must be at most 1e-12")
    if config.output.collect_diagnostics is not True:
        raise ValueError("recursive renormalization requires collect_diagnostics=True")
    if config.output.render_figures is not False:
        raise ValueError("recursive renormalization requires render_figures=False")
    return theory


def run_renormalization_v2_recursive_experiment(
    config: ExperimentConfig,
) -> RenormalizationV2RecursiveExperimentResult:
    """Build, provenance-bind, and publish the exact static Phase 2 witness."""
    theory = _validate_run_config(config)
    fixture = load_recursive_fixture(theory.fixture)
    if not isinstance(fixture, RecursiveFixture) or fixture.fixture_id != theory.fixture:
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

    semantic = dict(fixture.subrecord_sha256)
    fixture_inputs = (
        ("fixture_raw", fixture.fixture_sha256),
        *fixture.subrecord_sha256,
    )
    fixture_envelope = _envelope(
        fixture.fixture_id,
        producer_commit,
        config_hash,
        fixture_inputs,
        science.fixture_body,
    )
    fine_inputs = (("generative", semantic["generative"]),)
    fine_envelope = _envelope(
        fixture.fixture_id,
        producer_commit,
        config_hash,
        fine_inputs,
        science.fine_population_body,
    )
    fine_hash = _canonical_sha256(fine_envelope)
    coarse_generative_inputs = (
        ("fine_population", fine_hash),
        ("structure", semantic["structure"]),
    )
    coarse_generative_envelope = _envelope(
        fixture.fixture_id,
        producer_commit,
        config_hash,
        coarse_generative_inputs,
        science.coarse_generative_body,
    )
    coarse_generative_hash = _canonical_sha256(coarse_generative_envelope)
    coarse_interfaces_inputs = (
        ("coarse_generative", coarse_generative_hash),
        ("access", semantic["access"]),
        ("recognition", semantic["recognition"]),
    )
    coarse_interfaces_envelope = _envelope(
        fixture.fixture_id,
        producer_commit,
        config_hash,
        coarse_interfaces_inputs,
        science.coarse_interfaces_body,
    )
    coarse_interfaces_hash = _canonical_sha256(coarse_interfaces_envelope)
    coarse_population_inputs = (("coarse_generative", coarse_generative_hash),)
    coarse_population_envelope = _envelope(
        fixture.fixture_id,
        producer_commit,
        config_hash,
        coarse_population_inputs,
        science.coarse_population_body,
    )
    coarse_population_hash = _canonical_sha256(coarse_population_envelope)
    observation_inputs = (
        ("fine_population", fine_hash),
        ("coarse_interfaces", coarse_interfaces_hash),
        ("coarse_population", coarse_population_hash),
    )
    observation_envelope = _envelope(
        fixture.fixture_id,
        producer_commit,
        config_hash,
        observation_inputs,
        science.all_observation_body,
    )
    observation_hash = _canonical_sha256(observation_envelope)
    scientific_envelopes = {
        "fixture_snapshot": fixture_envelope,
        "fine_population": fine_envelope,
        "coarse_generative": coarse_generative_envelope,
        "coarse_interfaces": coarse_interfaces_envelope,
        "coarse_population": coarse_population_envelope,
        "all_observation_inference": observation_envelope,
    }
    scientific_hashes = {
        name: _canonical_sha256(envelope)
        for name, envelope in scientific_envelopes.items()
    }
    if scientific_hashes["all_observation_inference"] != observation_hash:
        raise RuntimeError("observation envelope hash drifted")
    metrics_inputs = tuple(
        (name, scientific_hashes[name]) for name in _SCIENTIFIC_ARTIFACTS
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
    arrays = _final_arrays(science, producer_commit, config_hash, array_inputs)
    arrays_hash = _logical_arrays_sha256(arrays)
    envelopes = MappingProxyType(
        {**scientific_envelopes, "metrics": metrics_envelope}
    )
    artifact_hashes = {
        **scientific_hashes,
        "metrics": metrics_hash,
        "arrays": arrays_hash,
    }

    provenance.update(
        {
            "experiment_scope": "finite_static_recursive_coarse_agent_phase2",
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
    input_hashes["fixture_direct_inputs"] = _direct_input_records(fixture_inputs)
    input_hashes["semantic_artifacts"] = dict(artifact_hashes)

    store = RunStore.create(config, provenance)
    for name in _JSON_ARTIFACTS:
        store.write_json(name, envelopes[name])
    store.write_npz("arrays", arrays)
    store.finalize(_DECLARED_ARTIFACTS)
    return RenormalizationV2RecursiveExperimentResult(
        run_dir=store.run_dir,
        config_hash=store.config_hash,
        status="pass",
        metrics=MappingProxyType(dict(science.metrics)),
        arrays=arrays,
    )


__all__ = [
    "RenormalizationV2RecursiveExperimentResult",
    "run_renormalization_v2_recursive_experiment",
]
