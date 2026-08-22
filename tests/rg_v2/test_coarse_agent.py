"""Contract tests for the recursive coarse-agent semantic boundary."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, fields
from fractions import Fraction
import hashlib
import itertools
import json

import pytest

from multiagent_elbo.finite.scale_cocycle import ExactMarkovChannel
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
    PushedCoarseJoint,
    RecursiveCoarseStructure,
    RecursiveObservationDatum,
    SparseRecordFactorizationSpec,
    canonical_agent_assignment_labels,
    channel_sha256,
    validate_coarse_structure_source_supports,
)
from rg_v2.contracts import AgentDatum, AgentRecognitionDatum, ExactProbabilityLaw, ModelEvaluation


def _local_states() -> tuple[str, ...]:
    return ('["b0","m0"]', '["b0","m1"]', '["b1","m0"]', '["b1","m1"]')


def _source_support(source_agent_ids: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        json.dumps(
            [[agent_id, belief, model] for agent_id, (belief, model) in zip(source_agent_ids, state, strict=True)],
            ensure_ascii=True,
            separators=(",", ":"),
        )
        for state in itertools.product((("b0", "m0"), ("b0", "m1"), ("b1", "m0"), ("b1", "m1")), repeat=len(source_agent_ids))
    )


def _block_channel(source_agent_ids: tuple[str, ...], target_labels: tuple[str, ...] | None = None) -> ExactMarkovChannel:
    targets = _local_states() if target_labels is None else target_labels
    return ExactMarkovChannel(
        _source_support(source_agent_ids), targets,
        tuple((Fraction(1),) + (Fraction(0),) * (len(targets) - 1) for _ in _source_support(source_agent_ids)),
        recognition_independent=True,
    )


def _agent(
    agent_id: str,
    belief_labels: tuple[str, ...] = ("b0", "b1"),
    model_labels: tuple[str, ...] = ("m0", "m1"),
) -> AgentDatum:
    state_labels = tuple(json.dumps([belief, model], separators=(",", ":")) for belief in belief_labels for model in model_labels)
    evaluator = tuple(
        ModelEvaluation(
            model_label,
            ExactMarkovChannel(("()",), belief_labels, (tuple(Fraction(1, len(belief_labels)) for _ in belief_labels),), recognition_independent=True),
        )
        for model_label in model_labels
    )
    return AgentDatum(
        agent_id, (), belief_labels, model_labels, state_labels, evaluator,
        ExactMarkovChannel(("()",), state_labels, (tuple(Fraction(1, len(state_labels)) for _ in state_labels),), recognition_independent=True),
    )


def _valid_structure(mutation: str | None = None) -> RecursiveCoarseStructure:
    state_labels = _local_states()
    reversed_order = mutation == "reversed_parent"
    source_a = ("a2", "a3") if reversed_order else ("a0", "a1")
    source_b = ("a0", "a1") if reversed_order else ("a2", "a3")
    spec_a = CoarseAgentSpec(
        "A", source_a, (), "fine-context", ("b0", "b1"), ("m0", "m1"),
        state_labels if mutation != "noncanonical_state" else tuple(reversed(state_labels)),
        _block_channel(source_a, ("wrong",) if mutation == "wrong_channel_target" else state_labels), "forbid",
    )
    spec_b = CoarseAgentSpec("B", source_b, ("A",), "fine-context", ("b0", "b1"), ("m0", "m1"), state_labels, _block_channel(source_b), "forbid")
    observation = CoarseObservationSpec(
        "r_AB", ("fine-0", "fine-1"), ("coarse-0", "coarse-1"),
        ("coarse-0", "coarse-0") if mutation == "nonbijective_observation" else ("coarse-0", "coarse-1"),
    )
    sparse = SparseRecordFactorizationSpec(
        ("r0", "r1"), ("r2", "r3"), ("left-0", "left-1"), ("right-0", "right-1"),
        ("left-0",) if mutation == "incomplete_sparse_projection" else ("left-0", "left-1"),
        ("right-0", "right-1"),
    )
    if mutation == "duplicate_source":
        spec_b = CoarseAgentSpec("B", ("a1", "a2"), spec_b.parent_ids, spec_b.source_context_id, spec_b.belief_labels, spec_b.model_labels, spec_b.state_labels, _block_channel(("a1", "a2")), spec_b.null_row_policy)
    return RecursiveCoarseStructure(
        "two-parent", ("a0", "a1", "a2", "a3"), ("B", "A") if reversed_order else ("A", "B"),
        (spec_b, spec_a) if reversed_order else (spec_a, spec_b), observation, sparse,
    )


def test_recursive_contract_field_order_is_stable() -> None:
    expected = {
        CoarseAgentSpec: ("agent_id", "source_agent_ids", "parent_ids", "source_context_id", "belief_labels", "model_labels", "state_labels", "block_channel", "null_row_policy"),
        CoarseObservationSpec: ("record_id", "fine_observation_labels", "compound_outcome_labels", "compound_outcome_by_fine_observation"),
        SparseRecordFactorizationSpec: ("left_record_ids", "right_record_ids", "left_outcome_labels", "right_outcome_labels", "left_outcome_by_fine_observation", "right_outcome_by_fine_observation"),
        RecursiveCoarseStructure: ("structure_id", "source_agent_order", "coarse_agent_order", "agent_specs", "observation", "sparse_record_candidate"),
        PushedCoarseJoint: ("context_id", "latent_labels", "fine_observation_labels", "joint_masses", "combined_channel_sha256"),
        CoarseGenerativeDatum: ("spec", "agent", "source_population_sha256", "block_channel_sha256", "combined_channel_sha256"),
        CoarseAccessSpec: ("agent_id", "observation_labels", "information_labels", "information_by_observation", "access_kind"),
        CoarseRecognitionDatum: ("agent", "initial_recognition", "recognition_kernel", "source_recognition_sha256"),
        CoarseUpdateDatum: ("agent_id", "update_kind", "kernel", "source_population_sha256", "access_sha256"),
        CoarseInformationDatum: ("access", "update"),
        CoarseAgentDatum: ("generative", "information", "recognition"),
        CoarsePopulationDatum: ("structure", "combined_channel", "generative_agents", "records", "pushed_joint", "reconstructed_population"),
        RecursiveObservationDatum: ("fine_observed_record", "coarse_observed_record", "fine_inference", "coarse_inference", "pushed_recognition", "pushed_posterior", "coarse_agents"),
    }
    assert {contract: tuple(field.name for field in fields(contract)) for contract in expected} == expected
    assert all(contract.__dataclass_params__.frozen for contract in expected)


def test_recursive_structure_rejects_frozen_mutation() -> None:
    structure = _valid_structure()
    with pytest.raises(FrozenInstanceError):
        structure.structure_id = "changed"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("mutation", "message"),
    (
        ("duplicate_source", "source blocks must be disjoint and exhaustive"),
        ("reversed_parent", "coarse agents must be topologically ordered"),
        ("noncanonical_state", "state labels must be the belief-major canonical Cartesian product"),
        ("wrong_channel_target", "block channel target labels must equal state labels"),
        ("nonbijective_observation", "observation map must be an ordered bijection"),
        ("incomplete_sparse_projection", "sparse projections must cover every fine observation"),
    ),
)
def test_recursive_contracts_reject_structural_mutations(mutation: str, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        _valid_structure(mutation)


def test_identity_access_declares_total_lossless_observation_access() -> None:
    access = CoarseAccessSpec("A", ("coarse-0", "coarse-1"), ("coarse-0", "coarse-1"), ("coarse-0", "coarse-1"), "identity_observation")
    assert access.information_by_observation == access.observation_labels
    with pytest.raises(ValueError, match="identity access must preserve every observation label"):
        CoarseAccessSpec("A", ("coarse-0", "coarse-1"), ("coarse-0",), ("coarse-0", "coarse-0"), "identity_observation")


def test_channel_hash_is_canonical_for_equal_exact_channel_values() -> None:
    channel = _block_channel(("a0", "a1"))
    copied_channel = ExactMarkovChannel(channel.source_labels, channel.target_labels, channel.matrix, recognition_independent=True)
    payload = {
        "target_labels": list(channel.target_labels),
        "matrix": [[{"numerator": value.numerator, "denominator": value.denominator} for value in row] for row in channel.matrix],
        "source_labels": list(channel.source_labels),
        "recognition_independent": channel.recognition_independent,
    }
    expected = hashlib.sha256(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True, allow_nan=False).encode("utf-8")).hexdigest()
    assert channel is not copied_channel
    assert channel_sha256(channel) == channel_sha256(copied_channel) == expected


@pytest.mark.parametrize("mutation", ("belief", "model", "state"))
def test_coarse_recognition_rejects_same_agent_id_with_mismatched_support(mutation: str) -> None:
    agent = _agent("A")
    if mutation == "belief":
        recognition_agent = _agent("A", ("x0", "x1"))
        recognition = AgentRecognitionDatum(recognition_agent, ExactProbabilityLaw(recognition_agent.state_labels, (Fraction(1, 4),) * 4))
    elif mutation == "model":
        recognition_agent = _agent("A", model_labels=("n0", "n1"))
        recognition = AgentRecognitionDatum(recognition_agent, ExactProbabilityLaw(recognition_agent.state_labels, (Fraction(1, 4),) * 4))
    else:
        recognition = AgentRecognitionDatum(agent, ExactProbabilityLaw(agent.state_labels, (Fraction(1, 4),) * 4))
        object.__setattr__(recognition, "state_labels", tuple(reversed(agent.state_labels)))
    kernel = ExactMarkovChannel(("information",), agent.state_labels, ((Fraction(1, 4),) * 4,), recognition_independent=True)
    with pytest.raises(ValueError, match="initial recognition supports must equal coarse agent supports"):
        CoarseRecognitionDatum(agent, recognition, kernel, "0" * 64)


def test_source_support_validator_rejects_missing_or_substituted_fine_state() -> None:
    structure = _valid_structure()
    source_agents = tuple(_agent(agent_id) for agent_id in structure.source_agent_order)
    validate_coarse_structure_source_supports(structure, source_agents)
    assert canonical_agent_assignment_labels(source_agents[:2]) == structure.agent_specs[0].block_channel.source_labels
    spec = structure.agent_specs[0]
    missing_channel = ExactMarkovChannel(spec.block_channel.source_labels[:-1], spec.block_channel.target_labels, spec.block_channel.matrix[:-1], recognition_independent=True)
    missing_spec = CoarseAgentSpec(spec.agent_id, spec.source_agent_ids, spec.parent_ids, spec.source_context_id, spec.belief_labels, spec.model_labels, spec.state_labels, missing_channel, spec.null_row_policy)
    missing_structure = RecursiveCoarseStructure(structure.structure_id, structure.source_agent_order, structure.coarse_agent_order, (missing_spec, structure.agent_specs[1]), structure.observation, structure.sparse_record_candidate)
    substituted_labels = list(spec.block_channel.source_labels)
    substituted_labels[0] = substituted_labels[0].replace('"b0"', '"other"', 1)
    substituted_channel = ExactMarkovChannel(tuple(substituted_labels), spec.block_channel.target_labels, spec.block_channel.matrix, recognition_independent=True)
    substituted_spec = CoarseAgentSpec(spec.agent_id, spec.source_agent_ids, spec.parent_ids, spec.source_context_id, spec.belief_labels, spec.model_labels, spec.state_labels, substituted_channel, spec.null_row_policy)
    substituted_structure = RecursiveCoarseStructure(structure.structure_id, structure.source_agent_order, structure.coarse_agent_order, (substituted_spec, structure.agent_specs[1]), structure.observation, structure.sparse_record_candidate)
    with pytest.raises(ValueError, match="block channel source labels must equal declared source-agent support"):
        validate_coarse_structure_source_supports(missing_structure, source_agents)
    with pytest.raises(ValueError, match="block channel source labels must equal declared source-agent support"):
        validate_coarse_structure_source_supports(substituted_structure, source_agents)
