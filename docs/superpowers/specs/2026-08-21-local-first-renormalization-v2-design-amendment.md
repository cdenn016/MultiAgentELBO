# Local-First Renormalization v2 Design Amendment

**Date:** 2026-08-21

**Base design:** `2026-08-21-local-first-renormalization-v2-design.md`

**Status:** Binding amendment

This amendment supersedes only the exact-type, signature, artifact, replay, and acceptance clauses below. Every other base-design requirement, invariant, boundary, inventory, hypothesis, phase, and gate remains binding.

## Corrected exact types

```python
@dataclass(frozen=True, init=False)
class AgentRecognitionDatum:
    agent_id: str
    belief_labels: tuple[str, ...]
    model_labels: tuple[str, ...]
    state_labels: tuple[str, ...]
    joint: ExactProbabilityLaw
    belief_marginal: ExactProbabilityLaw
    model_marginal: ExactProbabilityLaw


@dataclass(frozen=True)
class PopulationInference:
    population: PopulationJoint
    observed_record: str
    recognitions: tuple[AgentRecognitionDatum, ...]
    selector: SelectorSpec
    recognition: ExactProbabilityLaw
    evidence_measure: ExactSubmeasure
    evidence: Fraction
    posterior: ExactProbabilityLaw


@dataclass(frozen=True)
class AggregateDatum:
    aggregate_id: str
    source_agent_ids: tuple[str, ...]
    observed_record: str
    channel_id: str
    channel_sha256: str
    observation_labels: tuple[str, ...]
    target_labels: tuple[str, ...]
    generative_joint: tuple[tuple[Fraction, ...], ...]
    recognition: ExactProbabilityLaw
    posterior: ExactProbabilityLaw
    evidence: Fraction
    conditional_kl_defect: float
    kl_chain_residual: float
```

The exact initializer signature is `AgentRecognitionDatum.__init__(self, agent: AgentDatum, joint: ExactProbabilityLaw) -> None`. It copies `agent_id`, `belief_labels`, `model_labels`, and `state_labels` from `agent`, validates unique nonempty belief and model supports, the canonical Cartesian `state_labels`, and `joint.labels == state_labels`, and derives both marginals from `joint`. Its signature rejects independently supplied supports or marginals. `PopulationInference` retains the exact supported local recognitions and complete `SelectorSpec`, including any declared coupling. Its derived read-only property has signature `PopulationInference.selector_id(self) -> str` and returns `self.selector.selector_id`; it is convenience access only. `AggregateDatum.observed_record` binds the result to the observation used for inference.

## Corrected public signatures

`NumericsConfig` is imported explicitly with `from multiagent_elbo.config import NumericsConfig`.

The exact public signatures are `aggregate_population(inference: PopulationInference, channel: CoarseChannelSpec, numerics: NumericsConfig) -> AggregateDatum` and `validate_aggregate_datum(datum: AggregateDatum, inference: PopulationInference, channel: CoarseChannelSpec, numerics: NumericsConfig) -> None`.

Both functions receive `NumericsConfig` explicitly because the reused measure and kernel constructors require it; tolerances are not hardcoded or ambient. The validator receives the source inference and channel so it can recompute every fine-to-coarse arrow, observation binding, evidence identity, and KL decomposition.

## Identity, artifacts, and replay

Within one `aggregate_population` call, execution asserts that the same supplied channel object performs the generative, recognition, and posterior pushes. Artifacts instead store the canonical channel declaration and `channel_sha256`. Replay verifies that hash and recomputes all three pushes; it never stores or compares `id(channel)` or another process-local identity.

The base design's six-artifact inventory is unchanged. `fixture_snapshot.json` serializes each local recognition's belief, model, and canonical combined-state supports with its exact joint, plus the full `SelectorSpec` and any exact declared coupling. `population_inference.json` retains those direct recognition and selector inputs, `observed_record`, and all derived inference outputs. `aggregate_datum.json` retains `observed_record`, the canonical channel and hash, coarse laws, evidence, and KL diagnostics. The run configuration or a directly hashed input record retains the exact `NumericsConfig`.

Replay deserializes the recognitions, selector, inference, channel, observation, and numerical configuration; reconstructs the aggregate; calls `validate_aggregate_datum(datum, inference, channel, numerics)`; and reproduces all exact laws and diagnostics without primitive fixtures. Acceptance requires the same supplied channel object across all three execution pushes, but only one canonical channel declaration and hash across replay pushes. Replay must also rederive belief and model marginals from supported local joints, rerun selection from the retained `SelectorSpec`, and verify that inference and aggregate carry the same `observed_record`.
