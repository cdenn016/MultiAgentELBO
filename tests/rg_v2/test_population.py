"""Exact population-construction tests for the local-first v2 laboratory."""

from __future__ import annotations

from fractions import Fraction
from inspect import signature
from itertools import product
import json
from typing import Never

import pytest

import rg_v2.population as population
from multiagent_elbo.finite.scale_cocycle import ExactMarkovChannel
from rg_v2.contracts import RecordDatum
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
