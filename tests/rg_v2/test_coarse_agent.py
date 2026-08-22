"""Contract tests for the recursive coarse-agent semantic boundary.

Each structural mutation below names the validation it must break.  The
fixtures use real exact channels; no constructor is mocked.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, fields
from fractions import Fraction
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
    channel_sha256,
)


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
        _source_support(source_agent_ids),
        targets,
        tuple((Fraction(1),) + (Fraction(0),) * (len(targets) - 1) for _ in _source_support(source_agent_ids)),
        recognition_independent=True,
    )


def _valid_structure(mutation: str | None = None) -> RecursiveCoarseStructure:
    state_labels = _local_states()
    reversed_order = mutation == "reversed_parent"
    source_a = ("a2", "a3") if reversed_order else ("a0", "a1")
    source_b = ("a0", "a1") if reversed_order else ("a2", "a3")
    spec_a = CoarseAgentSpec(
        agent_id="A", source_agent_ids=source_a, parent_ids=(), source_context_id="fine-context",
        belief_labels=("b0", "b1"), model_labels=("m0", "m1"),
        state_labels=state_labels if mutation != "noncanonical_state" else tuple(reversed(state_labels)),
        block_channel=_block_channel(source_a, ("wrong",) if mutation == "wrong_channel_target" else state_labels),
        null_row_policy="forbid",
    )
    spec_b = CoarseAgentSpec(
        agent_id="B", source_agent_ids=source_b, parent_ids=("A",), source_context_id="fine-context",
        belief_labels=("b0", "b1"), model_labels=("m0", "m1"), state_labels=state_labels,
        block_channel=_block_channel(source_b), null_row_policy="forbid",
    )
    observation = CoarseObservationSpec(
        record_id="r_AB", fine_observation_labels=("fine-0", "fine-1"),
        compound_outcome_labels=("coarse-0", "coarse-1"),
        compound_outcome_by_fine_observation=("coarse-0", "coarse-0") if mutation == "nonbijective_observation" else ("coarse-0", "coarse-1"),
    )
    sparse = SparseRecordFactorizationSpec(
        left_record_ids=("r0", "r1"), right_record_ids=("r2", "r3"),
        left_outcome_labels=("left-0", "left-1"), right_outcome_labels=("right-0", "right-1"),
        left_outcome_by_fine_observation=("left-0",) if mutation == "incomplete_sparse_projection" else ("left-0", "left-1"),
        right_outcome_by_fine_observation=("right-0", "right-1"),
    )
    if mutation == "duplicate_source":
        spec_b = CoarseAgentSpec(
            agent_id=spec_b.agent_id, source_agent_ids=("a1", "a2"), parent_ids=spec_b.parent_ids,
            source_context_id=spec_b.source_context_id, belief_labels=spec_b.belief_labels,
            model_labels=spec_b.model_labels, state_labels=spec_b.state_labels,
            block_channel=_block_channel(("a1", "a2")), null_row_policy=spec_b.null_row_policy,
        )
    return RecursiveCoarseStructure(
        structure_id="two-parent", source_agent_order=("a0", "a1", "a2", "a3"),
        coarse_agent_order=("B", "A") if reversed_order else ("A", "B"),
        agent_specs=(spec_b, spec_a) if reversed_order else (spec_a, spec_b),
        observation=observation, sparse_record_candidate=sparse,
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
    access = CoarseAccessSpec(
        agent_id="A", observation_labels=("coarse-0", "coarse-1"), information_labels=("coarse-0", "coarse-1"),
        information_by_observation=("coarse-0", "coarse-1"), access_kind="identity_observation",
    )
    assert access.information_by_observation == access.observation_labels
    with pytest.raises(ValueError, match="identity access must preserve every observation label"):
        CoarseAccessSpec(
            agent_id="A", observation_labels=("coarse-0", "coarse-1"), information_labels=("coarse-0",),
            information_by_observation=("coarse-0", "coarse-0"), access_kind="identity_observation",
        )


def test_channel_hash_is_canonical_for_equal_exact_channel_values() -> None:
    channel = _block_channel(("a0", "a1"))
    copied_channel = ExactMarkovChannel(channel.source_labels, channel.target_labels, channel.matrix, recognition_independent=True)
    assert channel is not copied_channel
    assert channel_sha256(channel) == channel_sha256(copied_channel)
    assert len(channel_sha256(channel)) == 64
