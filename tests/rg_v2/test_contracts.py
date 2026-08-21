"""Contract tests for the root-local renormalization v2 semantic types."""

from __future__ import annotations

from dataclasses import fields
from fractions import Fraction
import inspect
import json

import pytest

from multiagent_elbo.finite.scale_cocycle import ExactMarkovChannel
from rg_v2.contracts import AgentDatum, AgentRecognitionDatum, AggregateDatum, CoarseChannelSpec, ExactProbabilityLaw, ExactSubmeasure, ModelEvaluation, PopulationInference, PopulationJoint, RecordDatum, SelectorSpec


def _local(belief: str, model: str) -> str:
    return json.dumps([belief, model], ensure_ascii=True, separators=(",", ":"))


def _assignment(*entries: tuple[str, str, str]) -> str:
    return json.dumps([list(entry) for entry in entries], ensure_ascii=True, separators=(",", ":"))


def _channel(source: tuple[str, ...], target: tuple[str, ...], rows: tuple[tuple[Fraction, ...], ...]) -> ExactMarkovChannel:
    return ExactMarkovChannel(source, target, rows)


def _root_agent() -> AgentDatum:
    beliefs = ("b0", "b1")
    models = ("m0", "m1")
    states = tuple(_local(belief, model) for belief in beliefs for model in models)
    kernel = _channel(("()",), states, ((Fraction(1, 3), Fraction(1, 6), Fraction(1, 3), Fraction(1, 6)),))
    return AgentDatum("a", (), beliefs, models, states, (ModelEvaluation("m0", _channel(("()",), beliefs, ((Fraction(1, 2), Fraction(1, 2)),))), ModelEvaluation("m1", _channel(("()",), beliefs, ((Fraction(1, 2), Fraction(1, 2)),))),), kernel)


def test_exact_public_field_orders_and_signatures_are_pinned() -> None:
    expected = {
        ExactProbabilityLaw: ("labels", "masses"), ExactSubmeasure: ("labels", "masses"), ModelEvaluation: ("model_label", "kernel"), AgentDatum: ("agent_id", "parent_ids", "belief_labels", "model_labels", "state_labels", "evaluator", "generative_kernel"), AgentRecognitionDatum: ("agent_id", "belief_labels", "model_labels", "state_labels", "joint", "belief_marginal", "model_marginal"), RecordDatum: ("record_id", "owner_id", "scope_ids", "outcome_labels", "kernel"), SelectorSpec: ("selector_id", "selector_kind", "coupling"), CoarseChannelSpec: ("channel_id", "source_agent_ids", "structural_input_ids", "channel"), PopulationJoint: ("context_id", "agent_order", "record_order", "latent_labels", "observation_labels", "joint_masses", "construction_trace"), PopulationInference: ("population", "observed_record", "recognitions", "selector", "recognition", "evidence_measure", "evidence", "posterior"), AggregateDatum: ("aggregate_id", "source_agent_ids", "observed_record", "channel_id", "channel_sha256", "observation_labels", "target_labels", "generative_joint", "recognition", "posterior", "evidence", "conditional_kl_defect", "kl_chain_residual"),
    }
    for contract, names in expected.items(): assert tuple(field.name for field in fields(contract)) == names
    assert tuple(inspect.signature(AgentRecognitionDatum).parameters) == ("agent", "joint")
    assert tuple(inspect.signature(AgentRecognitionDatum.__init__).parameters) == ("self", "agent", "joint")
    assert tuple(inspect.signature(PopulationInference.selector_id.fget).parameters) == ("self",)


def test_exact_laws_require_fraction_masses_and_correct_normalization() -> None:
    law = ExactProbabilityLaw(("x", "y"), (Fraction(1, 3), Fraction(2, 3)))
    measure = ExactSubmeasure(("x", "y"), (Fraction(0), Fraction(2, 3)))
    assert law.masses == (Fraction(1, 3), Fraction(2, 3)); assert measure.masses == (Fraction(0), Fraction(2, 3))
    for labels, masses in (((), ()), (("x", "x"), (Fraction(1, 2), Fraction(1, 2))), (("x",), (1,)), (("x",), (Fraction(-1),))):
        with pytest.raises((TypeError, ValueError)): ExactProbabilityLaw(labels, masses)
    with pytest.raises(ValueError, match="sum"): ExactProbabilityLaw(("x", "y"), (Fraction(1, 3), Fraction(1, 3)))
    with pytest.raises((TypeError, ValueError)): ExactSubmeasure(("x",), (0,))


def test_agent_validates_root_evaluators_and_positive_model_slices() -> None:
    agent = _root_agent()
    assert agent.generative_kernel.source_labels == ("()",)
    assert agent.state_labels == tuple(_local(belief, model) for belief in agent.belief_labels for model in agent.model_labels)


def test_agent_rejects_bad_state_support_root_source_and_evaluator_slice() -> None:
    agent = _root_agent()
    with pytest.raises(ValueError, match="state"): AgentDatum("a", (), agent.belief_labels, agent.model_labels, tuple(reversed(agent.state_labels)), agent.evaluator, agent.generative_kernel)
    wrong_source = _channel(("bad",), agent.state_labels, agent.generative_kernel.matrix)
    with pytest.raises(ValueError, match="root"): AgentDatum("a", (), agent.belief_labels, agent.model_labels, agent.state_labels, agent.evaluator, wrong_source)
    incompatible = (ModelEvaluation("m0", _channel(("()",), agent.belief_labels, ((Fraction(1), Fraction(0)),))), agent.evaluator[1])
    with pytest.raises(ValueError, match="evaluator"): AgentDatum("a", (), agent.belief_labels, agent.model_labels, agent.state_labels, incompatible, agent.generative_kernel)


def test_nonroot_parent_support_requires_canonical_ordered_assignment_syntax() -> None:
    states = (_local("b", "m"),); source = (_assignment(("parent", "b", "m")),)
    evaluator = (ModelEvaluation("m", _channel(source, ("b",), ((Fraction(1),),))),)
    AgentDatum("child", ("parent",), ("b",), ("m",), states, evaluator, _channel(source, states, ((Fraction(1),),)))
    malformed = _channel((json.dumps([["other", "b", "m"]]),), states, ((Fraction(1),),))
    with pytest.raises(ValueError, match="parent"): AgentDatum("child", ("parent",), ("b",), ("m",), states, (ModelEvaluation("m", _channel(malformed.source_labels, ("b",), ((Fraction(1),),))),), malformed)


def test_recognition_derives_only_marginals_from_canonical_joint() -> None:
    agent = _root_agent(); recognition = AgentRecognitionDatum(agent, ExactProbabilityLaw(agent.state_labels, (Fraction(1, 4), Fraction(1, 4), Fraction(1, 3), Fraction(1, 6))))
    assert recognition.belief_marginal == ExactProbabilityLaw(agent.belief_labels, (Fraction(1, 2), Fraction(1, 2)))
    assert recognition.model_marginal == ExactProbabilityLaw(agent.model_labels, (Fraction(7, 12), Fraction(5, 12)))
    with pytest.raises(TypeError): AgentRecognitionDatum(agent, recognition.joint, recognition.belief_marginal)  # type: ignore[call-arg]
    with pytest.raises(ValueError, match="joint"): AgentRecognitionDatum(agent, ExactProbabilityLaw(tuple(reversed(agent.state_labels)), recognition.joint.masses))


def test_record_requires_owner_scope_and_canonical_scope_support() -> None:
    outcome = ("no", "yes"); source = (_assignment(("a", "b0", "m0")),)
    record = RecordDatum("r", "a", ("a",), outcome, _channel(source, outcome, ((Fraction(1, 2), Fraction(1, 2)),)))
    assert record.owner_id == "a"
    with pytest.raises(ValueError, match="owner"): RecordDatum("r", "b", ("a",), outcome, record.kernel)
    with pytest.raises(ValueError, match="scope"): RecordDatum("r", "a", ("a",), outcome, _channel(("bad",), outcome, ((Fraction(1, 2), Fraction(1, 2)),)))


def test_selector_coupling_presence_rules_and_coarse_channel_contract() -> None:
    product = SelectorSpec("product-v1", "product", None); coupling = ExactProbabilityLaw(("x",), (Fraction(1),)); correlated = SelectorSpec("corr-v1", "declared_correlated", coupling)
    assert product.coupling is None; assert correlated.coupling is coupling
    with pytest.raises(ValueError, match="product"): SelectorSpec("bad", "product", coupling)
    with pytest.raises(ValueError, match="correlated"): SelectorSpec("bad", "declared_correlated", None)
    channel = _channel(("x",), ("y",), ((Fraction(1),),)); spec = CoarseChannelSpec("c", ("a",), ("boundary",), channel)
    assert spec.channel is channel
    with pytest.raises(TypeError): CoarseChannelSpec("c", ("a",), (), channel, aggregate_id="forbidden")  # type: ignore[call-arg]
    object.__setattr__(channel, "recognition_independent", False)
    with pytest.raises(ValueError, match="recognition"): CoarseChannelSpec("c", ("a",), ("boundary",), channel)


def test_population_inference_exposes_full_selector_and_aggregate_remains_nonagent() -> None:
    agent = _root_agent(); local = AgentRecognitionDatum(agent, ExactProbabilityLaw(agent.state_labels, (Fraction(1, 4), Fraction(1, 4), Fraction(1, 4), Fraction(1, 4))))
    population = PopulationJoint("ctx", ("a",), ("r",), agent.state_labels, ("no", "yes"), ((Fraction(1, 2), Fraction(1, 2)), (Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)), (Fraction(0), Fraction(0))), ("a", "r"))
    recognition = ExactProbabilityLaw(agent.state_labels, local.joint.masses); posterior = ExactProbabilityLaw(agent.state_labels, local.joint.masses); selector = SelectorSpec("product-v1", "product", None)
    inference = PopulationInference(population, _assignment(("r", "yes", "")), (local,), selector, recognition, ExactSubmeasure(agent.state_labels, local.joint.masses), Fraction(1), posterior)
    assert inference.selector_id == "product-v1"
    aggregate = AggregateDatum("A", ("a",), inference.observed_record, "c", "hash", ("no", "yes"), ("z",), ((Fraction(1, 2), Fraction(1, 2)),), recognition, posterior, Fraction(1), 0.0, 0.0)
    forbidden = {"CoarseAgentDatum", "as_agent", "evaluator", "observation_interface", "update_rule", "channel", "evidence_measure"}
    assert not any(hasattr(AggregateDatum, name) or hasattr(aggregate, name) for name in forbidden)
