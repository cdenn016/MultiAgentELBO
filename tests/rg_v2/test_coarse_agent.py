"""Contract tests for the recursive coarse-agent semantic boundary."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, replace
from fractions import Fraction
import hashlib
from inspect import signature
import itertools
import json
from typing import Never

import pytest

import rg_v2.coarse_agent as coarse_agent
from multiagent_elbo.config import NumericsConfig
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
from rg_v2.contracts import (
    AgentDatum,
    AgentRecognitionDatum,
    AggregateDatum,
    ExactProbabilityLaw,
    ModelEvaluation,
    PopulationInference,
    SelectorSpec,
)
from rg_v2.population import construct_population_joint, derive_population_inference, enumerate_population_joint_independently
from rg_v2.recursive_fixtures import load_recursive_fixture


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


def _explode(*_args: object, **_kwargs: object) -> Never:
    raise AssertionError("coarse constructor helper was reused")


def _literal_lf4_oracle() -> tuple[
    tuple[str, ...],
    tuple[str, ...],
    tuple[tuple[Fraction, ...], ...],
    tuple[tuple[Fraction, ...], ...],
]:
    """Enumerate LF4 and its parity push from literal rational tables."""
    agent_ids = ("a0", "a1", "a2", "a3")
    record_ids = ("r0", "r1", "r2", "r3")
    local_states = (("b0", "m0"), ("b0", "m1"), ("b1", "m0"), ("b1", "m1"))
    root_row = (Fraction(3, 8), Fraction(1, 8), Fraction(1, 8), Fraction(3, 8))
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
            [[record_id, str(outcome)] for record_id, outcome in zip(record_ids, outcomes, strict=True)],
            ensure_ascii=True,
            separators=(",", ":"),
        )
        for outcomes in itertools.product(range(2), repeat=4)
    )
    latent_labels: list[str] = []
    fine_rows: list[tuple[Fraction, ...]] = []
    coarse_rows = [[Fraction(0) for _ in range(16)] for _ in range(16)]
    for states in itertools.product(range(4), repeat=4):
        a0, a1, a2, a3 = states
        latent_labels.append(
            json.dumps(
                [[agent_id, *local_states[state]] for agent_id, state in zip(agent_ids, states, strict=True)],
                ensure_ascii=True,
                separators=(",", ":"),
            )
        )
        generative = root_row[a0] * child_rows[a0][a1] * child_rows[a1][a2] * child_rows[a2][a3]
        belief_agrees = local_states[a1][0] == local_states[a2][0]
        record_rows = (
            high if local_states[a0][0] == "b0" else low,
            high if belief_agrees else low,
            high if belief_agrees else low,
            high if local_states[a3][0] == "b0" else low,
        )
        row: list[Fraction] = []
        for observation_index, outcomes in enumerate(itertools.product(range(2), repeat=4)):
            mass = generative
            for record_row, outcome in zip(record_rows, outcomes, strict=True):
                mass *= record_row[outcome]
            row.append(mass)
            a_target = ((a0 // 2) ^ (a1 // 2)) * 2 + ((a0 % 2) ^ (a1 % 2))
            b_target = ((a2 // 2) ^ (a3 // 2)) * 2 + ((a2 % 2) ^ (a3 % 2))
            coarse_rows[a_target * 4 + b_target][observation_index] += mass
        fine_rows.append(tuple(row))
    return tuple(latent_labels), observation_labels, tuple(fine_rows), tuple(tuple(row) for row in coarse_rows)


def _relabel_reconstructed_rows(coarse: CoarsePopulationDatum) -> tuple[tuple[Fraction, ...], ...]:
    observation = coarse.structure.observation
    reconstructed = coarse.reconstructed_population
    columns = tuple(
        reconstructed.observation_labels.index(
            json.dumps([[observation.record_id, outcome]], ensure_ascii=True, separators=(",", ":"))
        )
        for outcome in observation.compound_outcome_by_fine_observation
    )
    return tuple(tuple(row[column] for column in columns) for row in reconstructed.joint_masses)


def _fine_population() -> tuple[object, object]:
    fixture = load_recursive_fixture("lf4_two_parent_recursive_v1")
    population = construct_population_joint(fixture.agents, fixture.records, fixture.context_id)
    return fixture, population


def test_generative_public_signature_has_only_population_and_structure() -> None:
    function = coarse_agent.construct_coarse_population_joint
    assert tuple(signature(function).parameters) == ("population", "structure")
    forbidden = {"inference", "recognition", "selector", "observation", "posterior", "numerics", "aggregate"}
    assert forbidden.isdisjoint(signature(function).parameters)


def test_generative_constructor_runtime_oracle_and_literal_oracle_match_all_cells() -> None:
    fixture, fine = _fine_population()
    runtime_fine = enumerate_population_joint_independently(fixture.agents, fixture.records, fixture.context_id)
    literal_latent, literal_observations, literal_fine, literal_coarse = _literal_lf4_oracle()
    assert fine.latent_labels == runtime_fine.latent_labels == literal_latent
    assert fine.observation_labels == runtime_fine.observation_labels == literal_observations
    assert fine.joint_masses == runtime_fine.joint_masses == literal_fine
    assert sum(len(row) for row in fine.joint_masses) == 4096

    constructed = coarse_agent.construct_coarse_population_joint(fine, fixture.structure)
    runtime = coarse_agent._enumerate_coarse_population_independently(fine, fixture.structure)
    assert constructed.pushed_joint.joint_masses == runtime.pushed_joint.joint_masses == literal_coarse
    assert constructed.reconstructed_population == runtime.reconstructed_population
    assert _relabel_reconstructed_rows(constructed) == constructed.pushed_joint.joint_masses
    assert sum(len(row) for row in constructed.pushed_joint.joint_masses) == 256


def test_generative_constructor_builds_two_agents_one_record_and_exact_roundtrip() -> None:
    fixture, fine = _fine_population()
    coarse = coarse_agent.construct_coarse_population_joint(fine, fixture.structure)
    assert coarse.reconstructed_population.agent_order == ("A", "B")
    assert coarse.reconstructed_population.record_order == ("r_AB",)
    assert len(coarse.pushed_joint.joint_masses) == 16
    assert all(len(row) == 16 for row in coarse.pushed_joint.joint_masses)
    assert _relabel_reconstructed_rows(coarse) == coarse.pushed_joint.joint_masses
    assert tuple(item.agent.agent_id for item in coarse.generative_agents) == ("A", "B")
    assert coarse.records[0].owner_id == "B"
    assert coarse.records[0].scope_ids == ("A", "B")
    assert coarse.combined_channel.channel.source_labels == fine.latent_labels
    assert coarse.combined_channel.channel.target_labels == coarse.pushed_joint.latent_labels
    assert all(sum(row, Fraction(0)) == 1 for row in coarse.combined_channel.channel.matrix)


def test_generative_runtime_oracle_reuses_no_constructor_helper(monkeypatch: pytest.MonkeyPatch) -> None:
    fixture, fine = _fine_population()
    expected = coarse_agent.construct_coarse_population_joint(fine, fixture.structure)
    for name in (
        "_population_sha256",
        "_build_combined_channel",
        "_push_population_joint",
        "_derive_coarse_agents",
        "_derive_evaluator",
        "_build_combined_record",
        "_relabel_reconstructed_joint",
        "_validate_coarse_population_datum",
    ):
        monkeypatch.setattr(coarse_agent, name, _explode)
    actual = coarse_agent._enumerate_coarse_population_independently(fine, fixture.structure)
    assert actual.pushed_joint.joint_masses == expected.pushed_joint.joint_masses
    assert actual.reconstructed_population.joint_masses == expected.reconstructed_population.joint_masses


@pytest.mark.parametrize(
    ("mutation", "message"),
    (
        ("block_partition", "source blocks must be disjoint and exhaustive"),
        ("channel_source", "block channel source labels"),
        ("channel_target", "block channel target labels"),
        ("factor_order", "generative agents must equal the coarse agent order"),
        ("positive_evaluator", "evaluator"),
        ("compound_bijection", "observation map|roundtrip"),
        ("combined_record", "roundtrip"),
    ),
)
def test_generative_validation_rejects_named_mutations(mutation: str, message: str) -> None:
    fixture, fine = _fine_population()
    coarse = coarse_agent.construct_coarse_population_joint(fine, fixture.structure)
    if mutation == "block_partition":
        object.__setattr__(coarse.structure.agent_specs[1], "source_agent_ids", ("a1", "a2"))
    elif mutation == "channel_source":
        channel = coarse.structure.agent_specs[0].block_channel
        object.__setattr__(channel, "source_labels", tuple(reversed(channel.source_labels)))
    elif mutation == "channel_target":
        channel = coarse.structure.agent_specs[0].block_channel
        object.__setattr__(channel, "target_labels", tuple(reversed(channel.target_labels)))
    elif mutation == "factor_order":
        object.__setattr__(coarse, "generative_agents", tuple(reversed(coarse.generative_agents)))
    elif mutation == "positive_evaluator":
        evaluator = coarse.generative_agents[0].agent.evaluator[0]
        kernel = evaluator.kernel
        altered = tuple(tuple(reversed(row)) for row in kernel.matrix)
        object.__setattr__(evaluator, "kernel", ExactMarkovChannel(kernel.source_labels, kernel.target_labels, altered))
    elif mutation == "compound_bijection":
        observation = coarse.structure.observation
        object.__setattr__(observation, "compound_outcome_by_fine_observation", tuple(reversed(observation.compound_outcome_by_fine_observation)))
    else:
        record = coarse.records[0]
        kernel = record.kernel
        altered = (tuple(reversed(kernel.matrix[0])),) + kernel.matrix[1:]
        object.__setattr__(record, "kernel", ExactMarkovChannel(kernel.source_labels, kernel.target_labels, altered))
    with pytest.raises(ValueError, match=message):
        coarse_agent._validate_coarse_population_datum(coarse)


def test_generative_sparse_record_diagnostics_match_literal_control() -> None:
    fixture, fine = _fine_population()
    coarse = coarse_agent.construct_coarse_population_joint(fine, fixture.structure)
    violations, maximum_tv = coarse_agent._sparse_record_factorization_diagnostics(coarse)
    assert violations == 448
    assert maximum_tv == Fraction(47889, 245000)


def test_generative_seam_rejects_aggregate_only_promotion_with_all_obligations() -> None:
    fixture, fine = _fine_population()
    singleton = ExactProbabilityLaw(("z",), (Fraction(1),))
    aggregate = AggregateDatum(
        "aggregate-only",
        fine.agent_order,
        fine.observation_labels[0],
        "terminal-channel",
        "0" * 64,
        fine.observation_labels,
        ("z",),
        ((Fraction(1),) + (Fraction(0),) * (len(fine.observation_labels) - 1),),
        singleton,
        singleton,
        Fraction(1),
        0.0,
        0.0,
    )
    with pytest.raises(
        ValueError,
        match="structural.*generative.*observation.*recognition.*update",
    ):
        coarse_agent.construct_coarse_population_joint(aggregate, fixture.structure)  # type: ignore[arg-type]


def _observations(label: str) -> tuple[tuple[str, str], ...]:
    return tuple((record_id, outcome) for record_id, outcome in json.loads(label))


def _local_marginal(
    law: ExactProbabilityLaw,
    agent_id: str,
    state_labels: tuple[str, ...],
) -> ExactProbabilityLaw:
    masses = [Fraction(0) for _ in state_labels]
    for latent_label, mass in zip(law.labels, law.masses, strict=True):
        assignment = json.loads(latent_label)
        entry = next(item for item in assignment if item[0] == agent_id)
        state_label = json.dumps(entry[1:], ensure_ascii=True, separators=(",", ":"))
        masses[state_labels.index(state_label)] += mass
    return ExactProbabilityLaw(state_labels, tuple(masses))


def _fine_inference_for_label(fixture: object, population: object, label: str) -> PopulationInference:
    return derive_population_inference(
        population,
        _observations(label),
        fixture.recognitions,
        fixture.selector,
    )


class _ExplodingInferenceSentinel:
    def __init__(self, touches: list[str]) -> None:
        object.__setattr__(self, "_touches", touches)

    def __getattribute__(self, name: str) -> Never:
        touches = object.__getattribute__(self, "_touches")
        touches.append(name)
        raise AssertionError(f"information construction touched inference attribute {name!r}")


def test_task4_public_signatures_are_exact_and_separated() -> None:
    expected = {
        "construct_coarse_information_interfaces": (
            (("coarse_population", "CoarsePopulationDatum"), ("access_specs", "tuple[CoarseAccessSpec, ...]")),
            "tuple[CoarseInformationDatum, ...]",
        ),
        "construct_coarse_recognition": (
            (
                ("coarse_population", "CoarsePopulationDatum"),
                ("information", "tuple[CoarseInformationDatum, ...]"),
                ("fine_inference", "PopulationInference"),
            ),
            "tuple[CoarseAgentDatum, ...]",
        ),
        "derive_recursive_observation": (
            (
                ("coarse_population", "CoarsePopulationDatum"),
                ("coarse_agents", "tuple[CoarseAgentDatum, ...]"),
                ("fine_inference", "PopulationInference"),
            ),
            "RecursiveObservationDatum",
        ),
        "validate_recursive_observation": (
            (
                ("datum", "RecursiveObservationDatum"),
                ("coarse_population", "CoarsePopulationDatum"),
                ("numerics", "NumericsConfig"),
            ),
            "None",
        ),
    }
    for function_name, (parameters, return_annotation) in expected.items():
        function_signature = signature(getattr(coarse_agent, function_name))
        assert tuple(
            (name, parameter.annotation)
            for name, parameter in function_signature.parameters.items()
        ) == parameters
        assert function_signature.return_annotation == return_annotation


def test_task4_information_is_inference_free_and_rejects_live_collapsed_access() -> None:
    fixture, fine = _fine_population()
    coarse = coarse_agent.construct_coarse_population_joint(fine, fixture.structure)
    information = coarse_agent.construct_coarse_information_interfaces(coarse, fixture.access_specs)
    assert tuple(item.access.agent_id for item in information) == ("A", "B")
    assert all(len(item.update.kernel.matrix) == 16 for item in information)
    assert all(sum(row, Fraction(0)) == 1 for item in information for row in item.update.kernel.matrix)
    assert all(len(set(item.update.kernel.matrix)) >= 2 for item in information)

    touches: list[str] = []
    sentinel = _ExplodingInferenceSentinel(touches)
    with pytest.raises(TypeError):
        coarse_agent.construct_coarse_information_interfaces(coarse, fixture.access_specs, sentinel)  # type: ignore[call-arg]
    assert touches == []

    access = replace(fixture.access_specs[0])
    rows = information[0].update.kernel.matrix
    left, right = next(
        (left, right)
        for left, right in itertools.combinations(range(len(rows)), 2)
        if rows[left] != rows[right]
    )
    collapsed = list(access.information_by_observation)
    collapsed[right] = collapsed[left]
    object.__setattr__(access, "information_by_observation", tuple(collapsed))
    with pytest.raises(ValueError, match="access descent"):
        coarse_agent.construct_coarse_information_interfaces(coarse, (access, fixture.access_specs[1]))


def test_task4_all_sixteen_observations_reconstruct_exact_inference_and_updates() -> None:
    fixture, fine = _fine_population()
    coarse = coarse_agent.construct_coarse_population_joint(fine, fixture.structure)
    information = coarse_agent.construct_coarse_information_interfaces(coarse, fixture.access_specs)
    numerics = NumericsConfig("float64", 1.0e-12, 1.0e-12)
    seen: list[str] = []
    first_recursive: RecursiveObservationDatum | None = None

    for fine_label in fine.observation_labels:
        fine_inference = _fine_inference_for_label(fixture, fine, fine_label)
        coarse_agents = coarse_agent.construct_coarse_recognition(coarse, information, fine_inference)
        recursive = coarse_agent.derive_recursive_observation(coarse, coarse_agents, fine_inference)
        coarse_agent.validate_recursive_observation(recursive, coarse, numerics)
        seen.append(recursive.fine_observed_record)
        if first_recursive is None:
            first_recursive = recursive

        direct_recognition = ExactProbabilityLaw(
            coarse.combined_channel.channel.target_labels,
            coarse.combined_channel.channel.pushforward(fine_inference.recognition.masses),
        )
        direct_posterior = ExactProbabilityLaw(
            coarse.combined_channel.channel.target_labels,
            coarse.combined_channel.channel.pushforward(fine_inference.posterior.masses),
        )
        fine_index = fine.observation_labels.index(fine_label)
        outcome = coarse.structure.observation.compound_outcome_by_fine_observation[fine_index]
        paired_record = json.dumps(
            [[coarse.structure.observation.record_id, outcome]],
            ensure_ascii=True,
            separators=(",", ":"),
        )
        assert recursive.coarse_observed_record == paired_record
        assert recursive.coarse_inference.observed_record == paired_record
        assert recursive.coarse_inference.evidence == fine_inference.evidence
        assert recursive.pushed_recognition == direct_recognition
        assert recursive.coarse_inference.recognition == direct_recognition
        assert recursive.pushed_posterior == direct_posterior
        assert recursive.coarse_inference.posterior == direct_posterior

        for agent, interface in zip(coarse_agents, information, strict=True):
            recognition = agent.recognition
            assert recognition.initial_recognition.joint == _local_marginal(
                direct_recognition,
                recognition.agent.agent_id,
                recognition.agent.state_labels,
            )
            assert len(recognition.recognition_kernel.matrix) == 16
            assert all(row == recognition.initial_recognition.joint.masses for row in recognition.recognition_kernel.matrix)
            assert all(sum(row, Fraction(0)) == 1 for row in recognition.recognition_kernel.matrix)
            information_index = interface.access.information_labels.index(paired_record)
            assert interface.update.kernel.matrix[information_index] == _local_marginal(
                direct_posterior,
                recognition.agent.agent_id,
                recognition.agent.state_labels,
            ).masses

    assert seen == list(fine.observation_labels)
    assert first_recursive is not None
    for agent in first_recursive.coarse_agents:
        assert agent.recognition.initial_recognition.model_marginal.masses == (Fraction(1, 2), Fraction(1, 2))
        assert len(set(agent.information.update.kernel.matrix)) >= 2
    local_a, local_b = (
        agent.recognition.initial_recognition.joint.masses
        for agent in first_recursive.coarse_agents
    )
    product_masses = tuple(mass_a * mass_b for mass_a in local_a for mass_b in local_b)
    assert first_recursive.pushed_recognition.masses != product_masses


def test_task4_generation_and_information_are_stable_under_all_inference_mutations() -> None:
    fixture, fine = _fine_population()
    base_coarse = coarse_agent.construct_coarse_population_joint(fine, fixture.structure)
    base_information = coarse_agent.construct_coarse_information_interfaces(base_coarse, fixture.access_specs)
    base = _fine_inference_for_label(fixture, fine, fine.observation_labels[0])
    product_selector = SelectorSpec("task4-product-selector", "product", None)
    selector_mutation = derive_population_inference(
        fine,
        _observations(fine.observation_labels[0]),
        fixture.recognitions,
        product_selector,
    )
    altered_first = AgentRecognitionDatum(
        fixture.agents[0],
        ExactProbabilityLaw(fixture.agents[0].state_labels, (Fraction(1, 2), Fraction(1, 6), Fraction(1, 6), Fraction(1, 6))),
    )
    recognition_mutation = derive_population_inference(
        fine,
        _observations(fine.observation_labels[0]),
        (altered_first,) + fixture.recognitions[1:],
        SelectorSpec("task4-recognition-product-selector", "product", None),
    )
    observation_mutation = _fine_inference_for_label(fixture, fine, fine.observation_labels[1])
    posterior_mutation = replace(
        base,
        posterior=ExactProbabilityLaw(base.posterior.labels, tuple(reversed(base.posterior.masses))),
    )

    for inference in (recognition_mutation, selector_mutation, observation_mutation, posterior_mutation):
        rebuilt = coarse_agent.construct_coarse_population_joint(fine, fixture.structure)
        rebuilt_information = coarse_agent.construct_coarse_information_interfaces(rebuilt, fixture.access_specs)
        assert rebuilt == base_coarse
        assert rebuilt_information == base_information

    base_recognition = coarse_agent.construct_coarse_recognition(base_coarse, base_information, base)
    assert coarse_agent.construct_coarse_recognition(base_coarse, base_information, recognition_mutation) != base_recognition
    assert coarse_agent.construct_coarse_recognition(base_coarse, base_information, selector_mutation) != base_recognition


def test_task4_recognition_rejects_mismatched_information_order() -> None:
    fixture, fine = _fine_population()
    coarse = coarse_agent.construct_coarse_population_joint(fine, fixture.structure)
    information = coarse_agent.construct_coarse_information_interfaces(coarse, fixture.access_specs)
    fine_inference = _fine_inference_for_label(fixture, fine, fine.observation_labels[0])
    with pytest.raises(ValueError, match="information order"):
        coarse_agent.construct_coarse_recognition(coarse, tuple(reversed(information)), fine_inference)


@pytest.mark.parametrize(
    ("mutation", "message"),
    (
        ("split_channel", "combined channel"),
        ("observation_relabel", "observation relabel|roundtrip"),
        ("selector_marginal", "selector marginal"),
        ("update_row", "update row"),
        ("record", "roundtrip"),
        ("evaluator", "evaluator"),
    ),
)
def test_task4_validation_rejects_named_live_mutations(mutation: str, message: str) -> None:
    fixture, fine = _fine_population()
    coarse = coarse_agent.construct_coarse_population_joint(fine, fixture.structure)
    information = coarse_agent.construct_coarse_information_interfaces(coarse, fixture.access_specs)
    fine_inference = _fine_inference_for_label(fixture, fine, fine.observation_labels[0])
    coarse_agents = coarse_agent.construct_coarse_recognition(coarse, information, fine_inference)
    recursive = coarse_agent.derive_recursive_observation(coarse, coarse_agents, fine_inference)

    if mutation == "split_channel":
        channel = coarse.combined_channel.channel
        altered = ExactMarkovChannel(
            channel.source_labels,
            channel.target_labels,
            tuple(tuple(reversed(row)) for row in channel.matrix),
            recognition_independent=True,
        )
        object.__setattr__(coarse.combined_channel, "channel", altered)
    elif mutation == "observation_relabel":
        observation = coarse.structure.observation
        object.__setattr__(
            observation,
            "compound_outcome_by_fine_observation",
            tuple(reversed(observation.compound_outcome_by_fine_observation)),
        )
    elif mutation == "selector_marginal":
        coupling = recursive.coarse_inference.selector.coupling
        assert coupling is not None
        bad_coupling = ExactProbabilityLaw(
            coupling.labels,
            (Fraction(1),) + (Fraction(0),) * (len(coupling.labels) - 1),
        )
        object.__setattr__(
            recursive.coarse_inference,
            "selector",
            SelectorSpec("task4-bad-selector", "declared_correlated", bad_coupling),
        )
    elif mutation == "update_row":
        update = recursive.coarse_agents[0].information.update
        kernel = update.kernel
        row_index = next(index for index, row in enumerate(kernel.matrix) if tuple(reversed(row)) != row)
        rows = list(kernel.matrix)
        rows[row_index] = tuple(reversed(rows[row_index]))
        object.__setattr__(
            update,
            "kernel",
            ExactMarkovChannel(kernel.source_labels, kernel.target_labels, tuple(rows), recognition_independent=True),
        )
    elif mutation == "record":
        record = coarse.records[0]
        kernel = record.kernel
        object.__setattr__(
            record,
            "kernel",
            ExactMarkovChannel(
                kernel.source_labels,
                kernel.target_labels,
                (tuple(reversed(kernel.matrix[0])),) + kernel.matrix[1:],
                recognition_independent=True,
            ),
        )
    else:
        evaluator = coarse.generative_agents[0].agent.evaluator[0]
        kernel = evaluator.kernel
        object.__setattr__(
            evaluator,
            "kernel",
            ExactMarkovChannel(
                kernel.source_labels,
                kernel.target_labels,
                tuple(tuple(reversed(row)) for row in kernel.matrix),
                recognition_independent=True,
            ),
        )

    with pytest.raises(ValueError, match=message):
        coarse_agent.validate_recursive_observation(
            recursive,
            coarse,
            NumericsConfig("float64", 1.0e-12, 1.0e-12),
        )
