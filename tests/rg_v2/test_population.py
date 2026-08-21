"""Exact population construction and inference tests for RG-v2."""

from __future__ import annotations

from fractions import Fraction
from inspect import signature
from itertools import product
import json
from typing import Never

import pytest

import rg_v2.population as population
from multiagent_elbo.finite.scale_cocycle import ExactMarkovChannel
from rg_v2.contracts import AgentRecognitionDatum, ExactProbabilityLaw, PopulationJoint, RecordDatum, SelectorSpec
from rg_v2.fixtures import load_fixture
from rg_v2.population import construct_population_joint, enumerate_population_joint_independently


def _compact(value: object) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"))


def _test_only_frozen_oracle() -> tuple[
    tuple[str, ...],
    tuple[str, ...],
    tuple[tuple[Fraction, ...], ...],
]:
    """Enumerate the frozen three-agent witness from hardcoded rational rows."""
    agent_ids = ("a", "b", "c")
    record_ids = ("r_a", "r_b", "r_c")
    local_states = (("b0", "m0"), ("b0", "m1"), ("b1", "m0"), ("b1", "m1"))
    root_row = (Fraction(3, 8), Fraction(1, 8), Fraction(1, 8), Fraction(3, 8))
    child_rows = (
        (Fraction(3, 5), Fraction(3, 20), Fraction(3, 20), Fraction(1, 10)),
        (Fraction(1, 5), Fraction(9, 20), Fraction(1, 20), Fraction(3, 10)),
        (Fraction(3, 10), Fraction(1, 20), Fraction(9, 20), Fraction(1, 5)),
        (Fraction(1, 10), Fraction(3, 20), Fraction(3, 20), Fraction(3, 5)),
    )
    record_rows = (
        (Fraction(4, 5), Fraction(1, 5)),
        (Fraction(4, 5), Fraction(1, 5)),
        (Fraction(1, 5), Fraction(4, 5)),
        (Fraction(1, 5), Fraction(4, 5)),
    )
    latent_labels: list[str] = []
    masses: list[tuple[Fraction, ...]] = []
    observation_labels = tuple(
        _compact([[record_id, str(outcome_index)] for record_id, outcome_index in zip(record_ids, outcome_indices, strict=True)])
        for outcome_indices in product(range(2), repeat=3)
    )

    for a_index, b_index, c_index in product(range(4), repeat=3):
        state_indices = (a_index, b_index, c_index)
        latent_labels.append(
            _compact([[agent_id, *local_states[state_index]] for agent_id, state_index in zip(agent_ids, state_indices, strict=True)])
        )
        generative_mass = root_row[a_index] * child_rows[a_index][b_index] * child_rows[b_index][c_index]
        row: list[Fraction] = []
        for outcome_indices in product(range(2), repeat=3):
            record_mass = (
                record_rows[a_index][outcome_indices[0]]
                * record_rows[b_index][outcome_indices[1]]
                * record_rows[c_index][outcome_indices[2]]
            )
            row.append(generative_mass * record_mass)
        masses.append(tuple(row))
    return tuple(latent_labels), observation_labels, tuple(masses)


def _explode(*_args: object, **_kwargs: object) -> Never:
    raise AssertionError("constructor-private helper was reused")


def _local_joint_marginal(
    law: ExactProbabilityLaw,
    recognition: AgentRecognitionDatum,
    agent_index: int,
) -> tuple[Fraction, ...]:
    totals = {label: Fraction(0) for label in recognition.state_labels}
    for latent_label, mass in zip(law.labels, law.masses, strict=True):
        assignment = json.loads(latent_label)
        entry = assignment[agent_index]
        assert entry[0] == recognition.agent_id
        totals[_compact(entry[1:])] += mass
    return tuple(totals[label] for label in recognition.state_labels)


def _total_variation(left: ExactProbabilityLaw, right: ExactProbabilityLaw) -> Fraction:
    assert left.labels == right.labels
    return sum((abs(a - b) for a, b in zip(left.masses, right.masses, strict=True)), Fraction(0)) / 2


def test_public_population_constructor_signatures_are_narrow() -> None:
    expected = ("agents", "records", "context_id")
    assert tuple(signature(construct_population_joint).parameters) == expected
    assert tuple(signature(enumerate_population_joint_independently).parameters) == expected


def test_constructor_runtime_oracle_and_test_oracle_match_every_exact_entry() -> None:
    fixture = load_fixture("lf3_product_v1")
    constructed = construct_population_joint(fixture.agents, fixture.records, fixture.context_id)
    runtime_oracle = enumerate_population_joint_independently(fixture.agents, fixture.records, fixture.context_id)
    test_latent, test_observations, test_masses = _test_only_frozen_oracle()

    assert constructed.agent_order == runtime_oracle.agent_order == ("a", "b", "c")
    assert constructed.record_order == runtime_oracle.record_order == ("r_a", "r_b", "r_c")
    assert constructed.latent_labels == runtime_oracle.latent_labels == test_latent
    assert constructed.observation_labels == runtime_oracle.observation_labels == test_observations
    assert constructed.joint_masses == runtime_oracle.joint_masses == test_masses
    assert sum((sum(row, Fraction(0)) for row in constructed.joint_masses), Fraction(0)) == 1
    assert constructed.construction_trace == runtime_oracle.construction_trace == (
        "agent:a",
        "agent:b",
        "agent:c",
        "record:r_a",
        "record:r_b",
        "record:r_c",
    )
    observed_111 = _compact([["r_a", "1"], ["r_b", "1"], ["r_c", "1"]])
    assert constructed.joint_masses[0][constructed.observation_labels.index(observed_111)] == Fraction(27, 25000)
    observed_000 = _compact([["r_a", "0"], ["r_b", "0"], ["r_c", "0"]])
    assert constructed.joint_masses[0][constructed.observation_labels.index(observed_000)] == Fraction(216, 3125)


def test_runtime_oracle_reuses_no_constructor_private_helper(monkeypatch: pytest.MonkeyPatch) -> None:
    fixture = load_fixture("lf3_product_v1")
    for name in (
        "_compact_json",
        "_decode_local_label",
        "_expected_assignment_labels",
        "_validate_exact_channel",
        "_validate_evaluator_compatibility",
        "_validate_agent_dag",
        "_validate_record_ownership",
        "_canonical_latent_labels",
        "_canonical_observation_labels",
        "_multiply_each_factor_once",
        "_sum_matrix",
    ):
        monkeypatch.setattr(population, name, _explode)
    oracle = enumerate_population_joint_independently(fixture.agents, fixture.records, fixture.context_id)
    assert len(oracle.latent_labels) == 64
    assert len(oracle.observation_labels) == 8


def test_product_and_correlated_fixtures_construct_identical_population_law() -> None:
    product_fixture = load_fixture("lf3_product_v1")
    correlated_fixture = load_fixture("lf3_correlated_v1")
    product_population = construct_population_joint(product_fixture.agents, product_fixture.records, product_fixture.context_id)
    correlated_population = construct_population_joint(correlated_fixture.agents, correlated_fixture.records, correlated_fixture.context_id)
    assert product_population == correlated_population


def test_duplicate_record_ids_are_rejected_before_factor_multiplication(monkeypatch: pytest.MonkeyPatch) -> None:
    fixture = load_fixture("lf3_product_v1")
    duplicate_records = (fixture.records[0], fixture.records[0], fixture.records[2])
    monkeypatch.setattr(population, "_multiply_each_factor_once", _explode)
    with pytest.raises(ValueError, match="record IDs"):
        construct_population_joint(fixture.agents, duplicate_records, fixture.context_id)


def test_bad_record_ownership_and_malformed_or_undeclared_scopes_are_rejected() -> None:
    fixture = load_fixture("lf3_product_v1")
    bad_owner = load_fixture("lf3_product_v1").records[0]
    object.__setattr__(bad_owner, "owner_id", "b")
    with pytest.raises(ValueError, match="owner"):
        construct_population_joint(fixture.agents, (bad_owner,) + fixture.records[1:], fixture.context_id)

    duplicate_scope = load_fixture("lf3_product_v1").records[0]
    object.__setattr__(duplicate_scope, "scope_ids", ("a", "a"))
    with pytest.raises(ValueError, match="scope"):
        construct_population_joint(fixture.agents, (duplicate_scope,) + fixture.records[1:], fixture.context_id)

    source = (_compact([["ghost", "b0", "m0"]]),)
    ghost_record = RecordDatum(
        "r_ghost",
        "ghost",
        ("ghost",),
        ("0", "1"),
        ExactMarkovChannel(source, ("0", "1"), ((Fraction(1, 2), Fraction(1, 2)),)),
    )
    with pytest.raises(ValueError, match="scope"):
        construct_population_joint(fixture.agents, fixture.records + (ghost_record,), fixture.context_id)


def test_reversed_dag_order_is_rejected_before_factor_multiplication(monkeypatch: pytest.MonkeyPatch) -> None:
    fixture = load_fixture("lf3_product_v1")
    monkeypatch.setattr(population, "_multiply_each_factor_once", _explode)
    with pytest.raises(ValueError, match="topological"):
        construct_population_joint(tuple(reversed(fixture.agents)), fixture.records, fixture.context_id)


def test_incomplete_agent_and_record_supports_are_rejected() -> None:
    fixture = load_fixture("lf3_product_v1")
    child = load_fixture("lf3_product_v1").agents[1]
    object.__setattr__(
        child,
        "generative_kernel",
        ExactMarkovChannel(
            child.generative_kernel.source_labels[:1],
            child.state_labels,
            child.generative_kernel.matrix[:1],
        ),
    )
    with pytest.raises(ValueError, match="generative.*support"):
        construct_population_joint((fixture.agents[0], child, fixture.agents[2]), fixture.records, fixture.context_id)

    record = load_fixture("lf3_product_v1").records[0]
    object.__setattr__(
        record,
        "kernel",
        ExactMarkovChannel(record.kernel.source_labels[:1], record.outcome_labels, record.kernel.matrix[:1]),
    )
    with pytest.raises(ValueError, match="record.*support"):
        construct_population_joint(fixture.agents, (record,) + fixture.records[1:], fixture.context_id)


def test_post_construction_generative_and_evaluator_mutations_are_rejected_before_multiplication(monkeypatch: pytest.MonkeyPatch) -> None:
    fixture = load_fixture("lf3_product_v1")
    root = fixture.agents[0]
    object.__setattr__(
        root,
        "generative_kernel",
        ExactMarkovChannel(
            root.generative_kernel.source_labels,
            root.state_labels,
            ((Fraction(1, 8), Fraction(3, 8), Fraction(1, 8), Fraction(3, 8)),),
        ),
    )
    monkeypatch.setattr(population, "_multiply_each_factor_once", _explode)
    with pytest.raises(ValueError, match="evaluator"):
        construct_population_joint(fixture.agents, fixture.records, fixture.context_id)

    evaluator_fixture = load_fixture("lf3_product_v1")
    evaluator = evaluator_fixture.agents[0].evaluator[0]
    object.__setattr__(
        evaluator,
        "kernel",
        ExactMarkovChannel(
            evaluator.kernel.source_labels,
            evaluator.kernel.target_labels,
            ((Fraction(1, 2), Fraction(1, 2)),),
        ),
    )
    with pytest.raises(ValueError, match="evaluator"):
        construct_population_joint(evaluator_fixture.agents, evaluator_fixture.records, evaluator_fixture.context_id)


def test_omitting_one_record_constructs_a_smaller_valid_law_but_not_the_complete_oracles() -> None:
    fixture = load_fixture("lf3_product_v1")
    omitted = construct_population_joint(fixture.agents, fixture.records[:-1], fixture.context_id)
    omitted_runtime = enumerate_population_joint_independently(fixture.agents, fixture.records[:-1], fixture.context_id)
    complete = construct_population_joint(fixture.agents, fixture.records, fixture.context_id)
    test_latent, test_observations, test_masses = _test_only_frozen_oracle()

    assert omitted == omitted_runtime
    assert len(omitted.latent_labels) == 64
    assert len(omitted.observation_labels) == 4
    assert all(len(row) == 4 for row in omitted.joint_masses)
    assert sum((sum(row, Fraction(0)) for row in omitted.joint_masses), Fraction(0)) == 1
    assert len(omitted.construction_trace) == 5
    assert omitted.construction_trace == complete.construction_trace[:-1]
    assert omitted != complete
    assert omitted.latent_labels == test_latent
    assert omitted.observation_labels != test_observations
    assert omitted.joint_masses != test_masses


@pytest.mark.parametrize("fixture_name", ["lf3_product_v1", "lf3_dirac_boundary_v1"])
def test_population_constructors_normalize_exactly_on_admitted_boundaries(fixture_name: str) -> None:
    fixture = load_fixture(fixture_name)  # type: ignore[arg-type]
    constructed = construct_population_joint(fixture.agents, fixture.records, fixture.context_id)
    oracle = enumerate_population_joint_independently(fixture.agents, fixture.records, fixture.context_id)
    assert constructed == oracle
    assert sum((sum(row, Fraction(0)) for row in constructed.joint_masses), Fraction(0)) == 1
    if fixture_name == "lf3_dirac_boundary_v1":
        assert constructed.joint_masses == ((Fraction(1),),)


def test_inference_and_selector_signatures_are_exact_and_narrow() -> None:
    assert tuple(signature(population._select_recognition).parameters) == ("recognitions", "selector")
    assert tuple(signature(population.derive_population_inference).parameters) == (
        "population",
        "observations",
        "recognitions",
        "selector",
    )


def test_product_selector_forms_the_exact_canonical_tensor_product() -> None:
    fixture = load_fixture("lf3_product_v1")
    selected = population._select_recognition(fixture.recognitions, fixture.selector)
    constructed = construct_population_joint(fixture.agents, fixture.records, fixture.context_id)

    assert selected.labels == constructed.latent_labels
    assert selected.masses == (Fraction(1, 64),) * 64
    assert tuple(recognition.joint.masses for recognition in fixture.recognitions) == ((Fraction(1, 4),) * 4,) * 3
    for index, recognition in enumerate(fixture.recognitions):
        assert _local_joint_marginal(selected, recognition, index) == recognition.joint.masses
    assert sum(sum(mass > 0 for mass in recognition.model_marginal.masses) > 1 for recognition in fixture.recognitions) == 3


def test_declared_correlated_selector_has_exact_marginals_and_tv_half() -> None:
    product_fixture = load_fixture("lf3_product_v1")
    correlated_fixture = load_fixture("lf3_correlated_v1")
    product_law = population._select_recognition(product_fixture.recognitions, product_fixture.selector)
    correlated_law = population._select_recognition(correlated_fixture.recognitions, correlated_fixture.selector)

    assert correlated_law.labels == product_law.labels
    expected = []
    for label in correlated_law.labels:
        beliefs = tuple(entry[1] for entry in json.loads(label))
        expected.append(Fraction(1, 32) if sum(belief == "b1" for belief in beliefs) % 2 == 0 else Fraction(0))
    assert correlated_law.masses == tuple(expected)
    assert _total_variation(product_law, correlated_law) == Fraction(1, 2)
    for index, recognition in enumerate(correlated_fixture.recognitions):
        assert _local_joint_marginal(correlated_law, recognition, index) == recognition.joint.masses == (Fraction(1, 4),) * 4


def test_dirac_boundary_has_one_coupling_and_zero_tv() -> None:
    fixture = load_fixture("lf3_dirac_boundary_v1")
    product_law = population._select_recognition(fixture.recognitions, fixture.selector)
    declared = SelectorSpec(
        "declared-singleton",
        "declared_correlated",
        ExactProbabilityLaw(product_law.labels, product_law.masses),
    )
    declared_law = population._select_recognition(fixture.recognitions, declared)

    assert product_law.masses == declared_law.masses == (Fraction(1),)
    assert _total_variation(product_law, declared_law) == 0
    assert sum(sum(mass > 0 for mass in recognition.model_marginal.masses) > 1 for recognition in fixture.recognitions) == 0


def test_observation_111_derives_exact_evidence_slice_and_posterior() -> None:
    fixture = load_fixture("lf3_product_v1")
    joint = construct_population_joint(fixture.agents, fixture.records, fixture.context_id)
    inference = population.derive_population_inference(joint, fixture.observation, fixture.recognitions, fixture.selector)
    expected_observed = _compact([["r_a", "1"], ["r_b", "1"], ["r_c", "1"]])
    column = joint.observation_labels.index(expected_observed)
    independent_slice = tuple(row[column] for row in joint.joint_masses)
    independent_evidence = sum(independent_slice, Fraction(0))

    assert inference.population is joint
    assert inference.observed_record == expected_observed
    assert inference.recognitions is fixture.recognitions
    assert inference.selector is fixture.selector
    assert inference.selector_id == fixture.selector.selector_id
    assert inference.recognition.masses == (Fraction(1, 64),) * 64
    assert inference.evidence_measure.labels == joint.latent_labels
    assert inference.evidence_measure.masses == independent_slice
    assert inference.evidence == independent_evidence == Fraction(6953, 40000)
    assert inference.evidence_measure.masses[0] == Fraction(27, 25000)
    assert inference.posterior.labels == joint.latent_labels
    assert inference.posterior.masses == tuple(value / independent_evidence for value in independent_slice)
    assert inference.posterior.masses[0] == Fraction(216, 34765)
    assert sum(inference.posterior.masses, Fraction(0)) == 1


def test_product_and_correlated_selection_leave_p_evidence_and_posterior_fixed() -> None:
    product_fixture = load_fixture("lf3_product_v1")
    correlated_fixture = load_fixture("lf3_correlated_v1")
    product_joint = construct_population_joint(product_fixture.agents, product_fixture.records, product_fixture.context_id)
    correlated_joint = construct_population_joint(correlated_fixture.agents, correlated_fixture.records, correlated_fixture.context_id)
    product_inference = population.derive_population_inference(
        product_joint,
        product_fixture.observation,
        product_fixture.recognitions,
        product_fixture.selector,
    )
    correlated_inference = population.derive_population_inference(
        correlated_joint,
        correlated_fixture.observation,
        correlated_fixture.recognitions,
        correlated_fixture.selector,
    )

    assert product_joint == correlated_joint
    assert _total_variation(product_inference.recognition, correlated_inference.recognition) == Fraction(1, 2)
    assert product_inference.evidence_measure == correlated_inference.evidence_measure
    assert product_inference.evidence == correlated_inference.evidence == Fraction(6953, 40000)
    assert product_inference.posterior == correlated_inference.posterior


def test_observation_001_control_and_reordering_are_canonical() -> None:
    fixture = load_fixture("lf3_product_v1")
    joint = construct_population_joint(fixture.agents, fixture.records, fixture.context_id)
    observation_001 = (("r_a", "0"), ("r_b", "0"), ("r_c", "1"))
    direct = population.derive_population_inference(joint, observation_001, fixture.recognitions, fixture.selector)
    reordered = population.derive_population_inference(joint, tuple(reversed(observation_001)), fixture.recognitions, fixture.selector)
    baseline = population.derive_population_inference(joint, fixture.observation, fixture.recognitions, fixture.selector)

    assert direct == reordered
    assert direct.population is joint
    assert direct.observed_record == _compact([["r_a", "0"], ["r_b", "0"], ["r_c", "1"]])
    assert direct.evidence == Fraction(4667, 40000)
    assert direct.evidence_measure.masses[0] == Fraction(54, 3125)
    assert direct.posterior.masses[0] == Fraction(3456, 23335)
    assert direct.recognition == baseline.recognition
    assert direct.evidence != baseline.evidence
    assert direct.posterior != baseline.posterior


def test_derive_passes_only_recognitions_and_selector_to_private_selector(monkeypatch: pytest.MonkeyPatch) -> None:
    fixture = load_fixture("lf3_product_v1")
    joint = construct_population_joint(fixture.agents, fixture.records, fixture.context_id)
    original = population._select_recognition
    calls: list[tuple[tuple[AgentRecognitionDatum, ...], SelectorSpec]] = []

    def spy(recognitions: tuple[AgentRecognitionDatum, ...], selector: SelectorSpec) -> ExactProbabilityLaw:
        calls.append((recognitions, selector))
        return original(recognitions, selector)

    monkeypatch.setattr(population, "_select_recognition", spy)
    inference = population.derive_population_inference(joint, fixture.observation, fixture.recognitions, fixture.selector)

    assert calls == [(fixture.recognitions, fixture.selector)]
    assert inference.population is joint


def test_selector_rejects_malformed_and_mutated_recognition_metadata() -> None:
    fixture = load_fixture("lf3_product_v1")
    with pytest.raises(TypeError, match="AgentRecognitionDatum"):
        population._select_recognition((object(),), fixture.selector)  # type: ignore[arg-type]

    fixture = load_fixture("lf3_product_v1")
    state_mutation = fixture.recognitions[0]
    object.__setattr__(state_mutation, "state_labels", tuple(reversed(state_mutation.state_labels)))
    with pytest.raises(ValueError, match="canonical.*state"):
        population._select_recognition((state_mutation,) + fixture.recognitions[1:], fixture.selector)

    fixture = load_fixture("lf3_product_v1")
    joint_mutation = fixture.recognitions[0]
    object.__setattr__(
        joint_mutation,
        "joint",
        ExactProbabilityLaw(tuple(reversed(joint_mutation.joint.labels)), tuple(reversed(joint_mutation.joint.masses))),
    )
    with pytest.raises(ValueError, match="joint.*support"):
        population._select_recognition((joint_mutation,) + fixture.recognitions[1:], fixture.selector)

    fixture = load_fixture("lf3_product_v1")
    belief_mutation = fixture.recognitions[0]
    object.__setattr__(belief_mutation, "belief_marginal", ExactProbabilityLaw(belief_mutation.belief_labels, (Fraction(3, 4), Fraction(1, 4))))
    with pytest.raises(ValueError, match="belief marginal"):
        population._select_recognition((belief_mutation,) + fixture.recognitions[1:], fixture.selector)

    fixture = load_fixture("lf3_product_v1")
    model_mutation = fixture.recognitions[0]
    object.__setattr__(model_mutation, "model_marginal", ExactProbabilityLaw(model_mutation.model_labels, (Fraction(1, 4), Fraction(3, 4))))
    with pytest.raises(ValueError, match="model marginal"):
        population._select_recognition((model_mutation,) + fixture.recognitions[1:], fixture.selector)

    fixture = load_fixture("lf3_product_v1")
    mass_mutation = fixture.recognitions[0]
    object.__setattr__(mass_mutation.joint, "masses", (Fraction(1),))
    with pytest.raises(ValueError, match="joint.*masses"):
        population._select_recognition((mass_mutation,) + fixture.recognitions[1:], fixture.selector)


def test_selector_rejects_duplicate_and_population_reordered_recognition_ids() -> None:
    fixture = load_fixture("lf3_product_v1")
    duplicate = (fixture.recognitions[0], fixture.recognitions[0], fixture.recognitions[2])
    with pytest.raises(ValueError, match="recognition agent IDs.*unique"):
        population._select_recognition(duplicate, fixture.selector)

    joint = construct_population_joint(fixture.agents, fixture.records, fixture.context_id)
    with pytest.raises(ValueError, match="recognition agent IDs.*population agent order"):
        population.derive_population_inference(joint, fixture.observation, tuple(reversed(fixture.recognitions)), fixture.selector)


def test_selector_rejects_mutated_product_and_correlated_couplings() -> None:
    correlated_fixture = load_fixture("lf3_correlated_v1")
    assert correlated_fixture.selector.coupling is not None

    product_fixture = load_fixture("lf3_product_v1")
    product_selector = product_fixture.selector
    object.__setattr__(product_selector, "coupling", correlated_fixture.selector.coupling)
    with pytest.raises(ValueError, match="product selector.*coupling"):
        population._select_recognition(product_fixture.recognitions, product_selector)

    missing_coupling = load_fixture("lf3_correlated_v1").selector
    object.__setattr__(missing_coupling, "coupling", None)
    with pytest.raises(ValueError, match="declared-correlated.*coupling"):
        population._select_recognition(correlated_fixture.recognitions, missing_coupling)

    coupling = correlated_fixture.selector.coupling
    permuted = ExactProbabilityLaw(tuple(reversed(coupling.labels)), tuple(reversed(coupling.masses)))
    wrong_order = SelectorSpec("wrong-order", "declared_correlated", permuted)
    with pytest.raises(ValueError, match="canonical latent support"):
        population._select_recognition(correlated_fixture.recognitions, wrong_order)

    wrong_masses = list(coupling.masses)
    wrong_masses[0] -= Fraction(1, 64)
    wrong_masses[1] += Fraction(1, 64)
    wrong_marginal = SelectorSpec(
        "wrong-marginal",
        "declared_correlated",
        ExactProbabilityLaw(coupling.labels, tuple(wrong_masses)),
    )
    with pytest.raises(ValueError, match="local marginal"):
        population._select_recognition(correlated_fixture.recognitions, wrong_marginal)


def test_observation_validation_rejects_incomplete_duplicate_extra_and_undeclared_inputs() -> None:
    fixture = load_fixture("lf3_product_v1")
    joint = construct_population_joint(fixture.agents, fixture.records, fixture.context_id)

    with pytest.raises(ValueError, match="missing"):
        population.derive_population_inference(joint, fixture.observation[:-1], fixture.recognitions, fixture.selector)
    duplicate = (fixture.observation[0], fixture.observation[0], fixture.observation[2])
    with pytest.raises(ValueError, match="duplicate"):
        population.derive_population_inference(joint, duplicate, fixture.recognitions, fixture.selector)
    with pytest.raises(ValueError, match="extra|undeclared"):
        population.derive_population_inference(
            joint,
            fixture.observation + (("ghost", "0"),),
            fixture.recognitions,
            fixture.selector,
        )
    undeclared = (fixture.observation[0], fixture.observation[1], (fixture.observation[2][0], "2"))
    with pytest.raises(ValueError, match="outcome|observation"):
        population.derive_population_inference(joint, undeclared, fixture.recognitions, fixture.selector)


def test_zero_evidence_column_in_valid_normalized_population_is_rejected() -> None:
    fixture = load_fixture("lf3_product_v1")
    joint = construct_population_joint(fixture.agents, fixture.records, fixture.context_id)
    observed = _compact([["r_a", "1"], ["r_b", "1"], ["r_c", "1"]])
    zero_column = joint.observation_labels.index(observed)
    destination = 0 if zero_column != 0 else 1
    moved_rows: list[tuple[Fraction, ...]] = []
    for row in joint.joint_masses:
        moved = list(row)
        moved[destination] += moved[zero_column]
        moved[zero_column] = Fraction(0)
        moved_rows.append(tuple(moved))
    zero_evidence_population = PopulationJoint(
        context_id=joint.context_id,
        agent_order=joint.agent_order,
        record_order=joint.record_order,
        latent_labels=joint.latent_labels,
        observation_labels=joint.observation_labels,
        joint_masses=tuple(moved_rows),
        construction_trace=joint.construction_trace,
    )

    assert sum((sum(row, Fraction(0)) for row in zero_evidence_population.joint_masses), Fraction(0)) == 1
    with pytest.raises(ValueError, match="positive evidence"):
        population.derive_population_inference(
            zero_evidence_population,
            fixture.observation,
            fixture.recognitions,
            fixture.selector,
        )


def test_dirac_inference_is_exactly_normalized() -> None:
    fixture = load_fixture("lf3_dirac_boundary_v1")
    joint = construct_population_joint(fixture.agents, fixture.records, fixture.context_id)
    inference = population.derive_population_inference(joint, fixture.observation, fixture.recognitions, fixture.selector)

    assert inference.recognition.masses == (Fraction(1),)
    assert inference.evidence_measure.masses == (Fraction(1),)
    assert inference.evidence == 1
    assert inference.posterior.masses == (Fraction(1),)
