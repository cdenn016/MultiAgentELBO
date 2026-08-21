# Local-First Renormalization v2 Design

**Date:** 2026-08-21

**Status:** Approved architecture, with root-level package location incorporated

**Repository baseline:** `c04a56e80abf3fd956941aa0021a3a93ea53eaae`

**Implementation location:** repository-root `rg_v2/`

**Release boundary:** the strongest constructed coarse object is `AggregateDatum`; Release 1 does not define `CoarseAgentDatum` or a meta-agent

## Purpose and decision

The renormalization laboratory will be rebuilt as an additive, local-first v2 rather than as a semantic extension of the existing coupling-readback laboratory. The new laboratory begins with finite agent-indexed belief and model-presentation spaces, exact local recognition laws over their product, evaluated model kernels, normalized agent generative mechanisms, and uniquely owned interaction-record kernels. It constructs a normalized population generative law, selects a population recognition coupling from the local recognition marginals, derives the posterior from the constructed generative law and the observed record, and pushes the generative, recognition, and posterior laws through one recognition-independent coarse channel.

The implementation will live directly at repository root:

```text
MultiAgentELBO/
    rg_v2/
    run_renormalization_v2_lab.py
    src/multiagent_elbo/
```

`rg_v2` is a repository-local research-laboratory package. It imports stable numerical and runtime primitives from `src/multiagent_elbo`; no module under `src/multiagent_elbo` imports `rg_v2`. The package finder in `pyproject.toml` searches only `src`, so `rg_v2` is intentionally absent from installed wheel and editable-package discovery in Release 1. The root launcher and repository tests import it because the repository root is available during those workflows. This placement marks v2 as an explicit laboratory surface, not yet part of the installed library API.

The implemented dependency is

\[
\left(
\{G_{\theta,i,D},\operatorname{ev}_i\}_{i\in V},
\{Q_{i,o,X}\}_{i\in V},
\{K_a\}_{a\in\mathfrak A}
\right)
\longrightarrow
\left(P_{\theta,V},Q_{V,o,X},\Pi_{V,o,X}\right)
\xrightarrow{C_A}
\operatorname{AggregateDatum}_A.
\]

The arrows denote implemented dependency, not an ontological hierarchy. The aggregate contains coarse probability laws and a record of how they were obtained. It does not contain a coarse observation interface, model evaluator, autonomous update rule, or section and gluing data. It is therefore not an agent under the manuscript's sufficiency conditions.

## Governing theory contract

The design implements five manuscript boundaries.

First, an agent's law-valued model state and its model evaluator are different objects. Each finite agent has belief labels \(\mathsf B_i\), model-presentation labels \(\mathsf M_i\), a combined local state space \(\mathsf Y_i=\mathsf B_i\times\mathsf M_i\), a recognition law \(Q_i\) on \(\mathsf Y_i\), and a normalized evaluator map

\[
\operatorname{ev}_i:m_i\longmapsto K^X_{i,m_i}.
\]

The model marginal \(q_i^m\) and belief marginal \(q_i^b\) are derived from \(Q_i\). A fixture may carry non-Dirac uncertainty over model presentations. A string naming a model or evaluator is not a substitute for this structure.

Second, local agent data precede complete population laws. Normalized parent-conditioned mechanisms \(G_i\) and normalized record kernels construct the generative law, while local recognition laws determine only a coupling class. A correlated population recognition law requires a declared selector. The selector is not allowed to infer a coupling from the generative law.

Third, generative construction is recognition-independent. No generative factor may receive a recognition law, a recognition parameter, or a posterior derived from the law being constructed. The implementation enforces this by giving population construction a generative-only signature.

Fourth, one normalized Markov channel acts on the fine latent variables while leaving the observation coordinate unchanged. The same immutable channel instance pushes the full generative joint, the selected recognition law, and the derived posterior. Different channels for these paths are a contract failure, not a configurable alternative.

Fifth, selecting a block does not construct a meta-agent. A coarse agent would additionally require a coarse state interpretation, observation interface, evaluator, recognition mechanism, and update rule. Release 1 neither supplies those objects nor provides a conversion from an aggregate to an agent.

The exact finite laboratory realizes these conditional statements. It does not establish an autonomous RG semigroup, a universality class, scaling exponents, a continuum limit, or an all-things-are-agents ontology.

## Alternatives considered

### Retrofit the existing coupling-readback laboratory

This option would add local-looking wrappers around `FalsificationModel`, `PairwiseInstance`, and `RescalingStep`. It is rejected. Those types begin from an already assembled graph, population-scale orbit families, occupancies, partitions, and couplings. At later levels the existing path consumes the record and treats the coupling action as the whole theory. Wrapping that path would preserve the dependency inversion that v2 is intended to test.

The existing laboratory remains useful as a historical rescaling witness. Its direct-versus-staged defects, gauge and holonomy checks, passive and regenerated flows, mutual-information diagnostics, and coupling readback are frozen as `legacy-rescaling-v1` evidence. They are not silently reinterpreted as local-first construction.

### Add a root-level local-first laboratory

This is the selected option. New semantics live under `rg_v2/`; stable exact channels, finite-measure calculations, VFE decomposition, artifact publication, metric records, and provenance capture are imported from `multiagent_elbo`. The dependency direction is one-way, so the installed package remains independent of the research laboratory.

This option permits a complete vertical slice without renaming or destabilizing existing finite modules. It also makes the experimental status visible in the filesystem: the laboratory must mature before it can be proposed for installed-package discovery.

### Build a generic local-to-global compiler in `src/multiagent_elbo`

This option would introduce abstract graph, kernel, selector, gauge, and multiscale interfaces before the first local-first witness exists. It is deferred. The proposed abstraction surface is larger than the current evidence and would make it harder to distinguish scientific requirements from speculative reuse. A later promotion may extract stable objects from `rg_v2` after at least two genuinely different local-first fixture families use the same interface.

## Dependency direction and stable reuse

The permitted import graph is:

```text
run_renormalization_v2_lab.py
              |
              v
           rg_v2
              |
              v
      multiagent_elbo public modules
```

The reverse edge is forbidden. `rg_v2` may import the following existing primitives when their current contracts suffice:

* `multiagent_elbo.finite.scale_cocycle.ExactMarkovChannel` for exact normalized finite channels and exact composition;
* `multiagent_elbo.finite.measures` and `multiagent_elbo.finite.vfe` through explicit exact-to-float adapters for finite KL and VFE diagnostics;
* `multiagent_elbo.artifacts.RunStore` for immutable, non-clobbering publication;
* `multiagent_elbo.runtime.RngStreams` and `collect_provenance` for deterministic streams and revision-bound provenance;
* `multiagent_elbo.experiment_support.MetricRecord` and its constructors for typed implementation checks.

Private functions, fixture constants, and experiment-specific constructors under `src/multiagent_elbo/finite` are not stable reuse seams. If a v2 operation cannot be expressed through the public objects above, it remains in `rg_v2` until a separate extraction is justified.

Shared installed-package edits are additive and restricted to configuration and experiment registration. `config.py` gains one discriminated theory-config type and parser branch. `experiment_support.py` gains one registry entry. `artifacts.py` is unchanged unless the generic `RunStore` is shown to be insufficient; the Release 1 design requires no new RunStore behavior. Existing experiment dataclasses, parser branches, registry records, launchers, serialization, and hashes are frozen.

## Release 1 file map

The complete Release 1 surface is deliberately small:

```text
rg_v2/
    README.md
    __init__.py
    contracts.py
    population.py
    coarse.py
    fixtures.py
    experiment.py
    data/
        lf3_product_v1.json
        lf3_correlated_v1.json
        lf3_dirac_boundary_v1.json
        legacy_rescaling_v1.json
run_renormalization_v2_lab.py
tests/
    rg_v2/
        test_contracts.py
        test_population.py
        test_coarse.py
        test_fixtures.py
        test_experiment.py
        test_legacy_regression.py
```

`README.md` states the laboratory boundary, click-to-run command, fixture choices, artifact contract, and non-installed status. `contracts.py` owns immutable semantic types and exact validation. `population.py` owns generative construction, recognition selection, and posterior derivation. `coarse.py` owns the common-channel pushforward and conditional-KL decomposition. `fixtures.py` parses versioned primitive data and the v1 regression manifest. `experiment.py` executes one selected Release 1 fixture and publishes the minimal artifact inventory.

`rg_v2/__init__.py` exports only the release identity and the semantic result types needed by the launcher. It does not re-export implementation helpers. Gauge, multiscale composition, regeneration, legacy adapters, generalization, and artifact-only rendering remain a later roadmap. No `gauge.py`, `scale.py`, `regeneration.py`, `legacy.py`, or `rendering.py` file is created in Release 1.

## Exact semantic types

All probability inputs are finite and rational. `Fraction` values remain exact through normalization, population construction, marginalization, conditioning, channel pushforward, total variation, and evidence comparison. Logarithms enter only in KL and VFE diagnostics, which use float64 after exact structural checks pass.

### Laws and evaluated model maps

`contracts.py` defines a small exact layer rather than treating bare tuples as interchangeable laws:

```python
@dataclass(frozen=True)
class ExactProbabilityLaw:
    labels: tuple[str, ...]
    masses: tuple[Fraction, ...]

@dataclass(frozen=True)
class ExactSubmeasure:
    labels: tuple[str, ...]
    masses: tuple[Fraction, ...]

@dataclass(frozen=True)
class ModelEvaluation:
    model_label: str
    kernel: ExactMarkovChannel

@dataclass(frozen=True)
class AgentDatum:
    agent_id: str
    parent_ids: tuple[str, ...]
    belief_labels: tuple[str, ...]
    model_labels: tuple[str, ...]
    state_labels: tuple[str, ...]
    evaluator: tuple[ModelEvaluation, ...]
    generative_kernel: ExactMarkovChannel

@dataclass(frozen=True, init=False)
class AgentRecognitionDatum:
    agent_id: str
    joint: ExactProbabilityLaw
    belief_marginal: ExactProbabilityLaw
    model_marginal: ExactProbabilityLaw

@dataclass(frozen=True)
class RecordDatum:
    record_id: str
    owner_id: str
    scope_ids: tuple[str, ...]
    outcome_labels: tuple[str, ...]
    kernel: ExactMarkovChannel
```

`ExactProbabilityLaw` requires nonempty unique labels, nonnegative masses, and exact unit mass. `ExactSubmeasure` requires nonnegative masses but not unit mass.

`AgentDatum.state_labels` is the canonical Cartesian enumeration of `belief_labels` and `model_labels`. Its `generative_kernel` is \(G_i\), a normalized channel from the canonical parent-state configurations to that combined local state. A root uses the one-element source support `("()",)`.

`AgentDatum.evaluator` contains exactly one entry for every model label. Each evaluator kernel has the same source support as \(G_i\) and target support `belief_labels`. For every parent context and every model label having positive \(G_i\)-marginal mass, disintegrating \(G_i\) over belief conditional on that model must reproduce the corresponding evaluator row exactly:

\[
G_i(b_i,m_i\mid y_{\operatorname{pa}(i)},X)
=
G_i^M(m_i\mid y_{\operatorname{pa}(i)},X)
K^X_{i,m_i}(b_i\mid y_{\operatorname{pa}(i)}).
\]

Compatibility is vacuous only on a zero-mass model row and is recorded as such. This makes the evaluator operational rather than decorative while keeping \(G_i\) as the normalized parent-conditioned mechanism over the combined local state.

`AgentRecognitionDatum` is constructed from one exact \(Q_i\) on the combined state support. Its initializer derives `belief_marginal` and `model_marginal`; fixtures cannot supply those fields independently. At least the product and correlated fixtures contain a non-Dirac `model_marginal`, so model uncertainty is exercised rather than represented only by a type.

A record kernel's source labels are the canonical Cartesian enumeration of its scope's combined agent states, and its target labels equal its outcome labels. Its owner is a bookkeeping owner, not a second probabilistic factor.

### Selector, population, inference, and aggregate types

The remaining public types are:

```python
@dataclass(frozen=True)
class SelectorSpec:
    selector_id: str
    selector_kind: Literal["product", "declared_correlated"]
    coupling: ExactProbabilityLaw | None

@dataclass(frozen=True)
class CoarseChannelSpec:
    channel_id: str
    source_agent_ids: tuple[str, ...]
    structural_input_ids: tuple[str, ...]
    channel: ExactMarkovChannel

@dataclass(frozen=True)
class PopulationJoint:
    context_id: str
    agent_order: tuple[str, ...]
    record_order: tuple[str, ...]
    latent_labels: tuple[str, ...]
    observation_labels: tuple[str, ...]
    joint_masses: tuple[tuple[Fraction, ...], ...]
    construction_trace: tuple[str, ...]

@dataclass(frozen=True)
class PopulationInference:
    population: PopulationJoint
    observed_record: str
    selector_id: str
    recognition: ExactProbabilityLaw
    evidence_measure: ExactSubmeasure
    evidence: Fraction
    posterior: ExactProbabilityLaw

@dataclass(frozen=True)
class AggregateDatum:
    aggregate_id: str
    source_agent_ids: tuple[str, ...]
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

`SelectorSpec.coupling` is absent for the product selector. For a declared-correlated selector it carries a versioned exact joint table whose marginals must equal the supplied local recognition laws exactly. The table is additional epistemic data, not something estimated from `PopulationJoint`.

`PopulationJoint.joint_masses[y][o]` stores the complete normalized law over latent and record coordinates. Its construction trace identifies every agent kernel and every record kernel exactly once. `PopulationInference` stores an observed record, selected population recognition law, evidence slice, evidence, and posterior. The evidence and posterior are derived from `PopulationJoint`; neither can enter through a fixture.

`CoarseChannelSpec` may depend on declared structural data and a blocking map. It cannot depend on recognition values, recognition parameters, posterior values, or the realized observation. Its wrapped `ExactMarkovChannel` has `recognition_independent is True`.

`AggregateDatum` deliberately has none of the fields required for an agent. There is no `as_agent`, `promote`, implicit protocol conformance, or adapter that synthesizes an evaluator, information interface, update rule, or autonomous state.

## Public function contracts

Release 1 exposes these functions:

```python
def construct_population_joint(
    agents: tuple[AgentDatum, ...],
    records: tuple[RecordDatum, ...],
    context_id: str,
) -> PopulationJoint:
    ...

def derive_population_inference(
    population: PopulationJoint,
    observations: tuple[tuple[str, str], ...],
    recognitions: tuple[AgentRecognitionDatum, ...],
    selector: SelectorSpec,
) -> PopulationInference:
    ...

def aggregate_population(
    inference: PopulationInference,
    channel: CoarseChannelSpec,
) -> AggregateDatum:
    ...

def validate_aggregate_datum(
    datum: AggregateDatum,
) -> None:
    ...

def load_fixture(
    fixture: Literal[
        "lf3_product_v1",
        "lf3_correlated_v1",
        "lf3_dirac_boundary_v1",
    ],
) -> LocalFirstFixture:
    ...

def run_renormalization_v2_experiment(
    config: ExperimentConfig,
) -> RenormalizationV2ExperimentResult:
    ...
```

`construct_population_joint` has no recognition, observation, selector, or posterior argument. This is the executable fixed-joint prohibition. `derive_population_inference` internally passes only the tuple of local recognitions and `SelectorSpec` to a private selector function; selector implementations never receive `PopulationJoint`, evidence, likelihood, or posterior. Only after selection does the function slice the already constructed population joint at the observed record and derive the posterior.

`aggregate_population` extends the latent channel by the identity on the observation coordinate to construct the coarse complete generative joint. It pushes recognition and posterior through the same wrapped channel object. It records one channel object identity during execution and one canonical channel hash for replay. A split-channel mutation that supplies separate copies to different routes is rejected in the strict Release 1 path; numerical equality is weaker than common provenance.

The aggregate records exact preservation of total mass and evidence and the float64 KL chain identity

\[
\operatorname{KL}(Q\Vert\Pi)
=
\operatorname{KL}(QC_A\Vert\Pi C_A)
+\Delta_A,
\qquad \Delta_A\geq 0.
\]

## Construction and selection invariants

The loader and constructors validate their domain before multiplying any factor.

1. Agent identifiers are unique and appear exactly once in topological order.
2. Every parent identifier is declared and precedes its child.
3. Belief labels and model labels are nonempty and unique. Combined state labels equal their canonical Cartesian product.
4. Every model label has one normalized evaluator kernel. Every positive-mass model slice of \(G_i\) agrees with its evaluator exactly.
5. Every \(G_i\) is a normalized exact channel whose source and target supports match the declared parent and combined local spaces.
6. Every local recognition law is normalized on the combined local space. Its stored belief and model marginals are derived and exact.
7. Record identifiers are unique. Every record has a nonempty unique scope, its owner belongs to that scope, and every scoped agent exists.
8. Each record appears once in the input and once in the construction trace. Two orientations of one undirected record are not accepted as two descriptions of one record.
9. Every record kernel normalizes over record outcomes for every boundary assignment.
10. The latent population law is constructed in topological order and normalizes exactly.
11. The complete population law attaches every record kernel once and normalizes exactly after summing latent and record coordinates.
12. Population construction cannot inspect an observation value. Observation is used only to derive the evidence slice and posterior from the completed joint.
13. The selected recognition support is the canonical Cartesian product in agent order. Every selected law is normalized and reproduces every local joint recognition law as a marginal.
14. The product and correlated fixtures share the same local recognition marginals while supplying different admitted population joints.
15. The Dirac-boundary fixture has at most one non-Dirac local recognition law and therefore admits only one coupling.
16. An invalid correlated table is rejected rather than projected into the coupling class.

An undirected potential is outside the Release 1 constructor. Supporting it would require a separate global normalizer with a positive-finite proof. Reciprocal same-step latent conditionals are excluded unless replaced by an explicit schedule, common cause, or normalized joint.

## Fixture and oracle policy

The three fixture files are primitive inputs:

* `lf3_product_v1.json` contains three `AgentDatum` records, including belief and model-presentation spaces, complete evaluator maps, normalized \(G_i\) kernels, uniquely owned record kernels, local combined-state recognition laws, a product-selector declaration, one fixed observation, and one structural coarse channel.
* `lf3_correlated_v1.json` has the same generative data and local recognition laws as the product fixture but supplies an additional exact correlated coupling. The two runtime files may share a referenced canonical local-data payload only if each provenance record hashes the resolved bytes.
* `lf3_dirac_boundary_v1.json` realizes the coupling-uniqueness boundary with at most one non-Dirac local recognition law.

The product and correlated fixtures each declare at least one non-Dirac \(q_i^m\). Tests derive \(q_i^b\) and \(q_i^m\) from \(Q_i\) and compare them with independently enumerated oracles. This confirms that the model fiber is represented as a probability law over model presentations and that evaluator choice remains distinct from model uncertainty.

No primitive fixture contains derived \(P\), \(Q_V\), \(\Pi\), evidence, coarse laws, VFE values, metric statuses, or expected pass flags. Unit-test oracles calculate small expected tables through an independent enumeration route. Where an expected table is too large to state directly in test code, a separately labeled test-only oracle records its producer and hash and is never read by experiment runtime.

The first three-agent witness has at most 64 latent states. Exact unit fixtures may not exceed 4,096 latent states.

`legacy_rescaling_v1.json` is not a v2 scientific fixture. It is a regression manifest captured from baseline `c04a56e80abf3fd956941aa0021a3a93ea53eaae` before shared config or registry edits. It records each protected launcher, canonical configuration JSON and SHA-256, source fixture hashes, semantic artifact hashes or exact values, metric records, and any normalization rule for volatile provenance fields. The test suite reads it only to establish that additive v2 registration did not change v1 behavior.

## Configuration and launcher

The root launcher follows the repository's click-to-run convention. It prepends only `ROOT / "src"` to `sys.path`; the root package is importable from the launcher's directory. Its editable dictionaries resolve through the shared strict configuration loader.

Release 1 adds this closed config type:

```python
@dataclass(frozen=True)
class RenormalizationV2TheoryConfig:
    experiment: Literal["renormalization_v2"]
    fixture: Literal[
        "lf3_product_v1",
        "lf3_correlated_v1",
        "lf3_dirac_boundary_v1",
    ]
    arithmetic: Literal["exact_rational"]
```

The default dictionaries are:

```python
RUN = {"name": "renormalization-v2", "seed": 20260821}
THEORY = {
    "experiment": "renormalization_v2",
    "fixture": "lf3_product_v1",
    "arithmetic": "exact_rational",
}
```

`NUMERICS`, `OUTPUT`, and `COMPUTE` retain the existing shared schema. Exact-rational v2 runs are CPU-only, deterministic, and float64 at the logarithmic diagnostic boundary. The user may select one of the three frozen fixtures. Release acceptance executes all three rather than reporting only the default.

Adding the parser branch must not alter `canonical_config_json` output for any preexisting config. Existing v1 config hashes are tested before and after the shared edit. The experiment registry receives one additive `renormalization_v2` record with the exact launcher, config keys, artifact inventory, and metric inventory defined here.

## Minimal Release 1 artifact contract

The experiment publishes through `RunStore`. A complete run has the core `config.json` and `manifest.json` plus exactly these six semantic artifacts:

| Artifact | Required content |
|---|---|
| `fixture_snapshot.json` | schema version, fixture identity and hash, exact agent belief/model spaces, evaluator and \(G_i\) hashes, recognition and record hashes, observation, selector and coarse-channel declarations |
| `population_joint.json` | topological order, record ownership, construction trace, exact joint masses, normalization and independent-enumeration checks |
| `population_inference.json` | derived belief/model marginals, selector identity, selected population recognition law, observed evidence slice, evidence, posterior, marginal checks |
| `aggregate_datum.json` | common channel identity and hash, exact coarse generative, recognition and posterior laws, evidence preservation, conditional KL defect and chain residual |
| `metrics.json` | immutable `MetricRecord` serialization for the fixed metric inventory |
| `arrays.npz` | float64 mirrors of finalized exact laws and KL/VFE diagnostics for later replay, with no additional scientific result |

The registry artifact inventory is therefore

```python
(
    "fixture_snapshot",
    "population_joint",
    "population_inference",
    "aggregate_datum",
    "metrics",
    "arrays",
)
```

Exact rational values in JSON use canonical `{ "numerator": n, "denominator": d }` records with a positive denominator. Maps whose order affects a mathematical support are serialized as ordered records, not JSON objects whose ordering might be ignored. Every semantic artifact carries `schema_version`, `fixture_id`, `producer_commit`, `config_hash`, and the hashes of its direct inputs. Canonical hashes use UTF-8 JSON with sorted structural keys and compact separators; mathematical arrays retain declared order.

`metrics.json` contains this fixed inventory:

```python
(
    "agent_kernel_normalization_residual",
    "evaluator_compatibility_residual",
    "record_kernel_normalization_residual",
    "record_ownership_violation_count",
    "population_normalization_residual",
    "independent_population_residual",
    "recognition_marginal_residual",
    "model_marginal_non_dirac_count",
    "posterior_derivation_residual",
    "common_channel_identity_violation_count",
    "coarse_evidence_residual",
    "conditional_kl_defect",
    "kl_chain_residual",
)
```

These are implementation checks. Formula-level checks use theorem status `ESTABLISHED` where they instantiate a proved identity. Fixture-dependent separation and non-Dirac checks use `HYPOTHESIS` or `NUMERICAL`. Every new result begins with verification state `CANDIDATE`. Passing tests or agreement among agents does not change it to `EVIDENCE_VERIFIED`; that state requires a separate evidence-gated verification action bound to the released revision.

## Release 1 hypotheses and evidence stages

Release 1 freezes five hypotheses before measurement.

| ID | Statement under test | Status before execution | Primary falsifier |
|---|---|---|---|
| H-MODEL | Each declared evaluator is normalized, agrees with the positive-mass model slices of \(G_i\), and at least one admitted fixture realizes non-Dirac \(q_i^m\) | conditional identity plus fixture hypothesis | normalization, compatibility, or non-Dirac failure |
| H-LG | Local normalized mechanisms and once-owned record kernels construct the declared normalized population law | `ESTABLISHED` identity, implementation `CANDIDATE` | normalization, ordering, ownership, or independent-enumeration mismatch |
| H-SEL | Product and declared-correlated selectors preserve supplied local laws; the non-Dirac fixtures admit distinct joints and the Dirac boundary does not | conditional theorem plus fixture hypothesis | marginal residual, equal supposedly distinct joints, or nonunique Dirac control |
| H-AGG | One recognition-independent channel constructs normalized coarse \(P,Q,\Pi\) and preserves observation evidence | `ESTABLISHED` identity, implementation `CANDIDATE` | split channel, normalization failure, or changed evidence |
| H-KL | Fine KL equals coarse KL plus the nonnegative conditional defect | `ESTABLISHED` identity, implementation `CANDIDATE` | negative defect beyond tolerance or chain residual |

Evidence proceeds in ordered stages.

1. **Legacy freeze.** Capture v1 config identities and semantic outputs before shared edits. An unexplained mismatch blocks shared edits.
2. **Type and evaluator checks.** Validate exact laws, belief/model products, evaluator completeness and compatibility, non-Dirac model recognition, DAG ordering, record ownership, and forbidden-input signatures.
3. **Population construction.** Construct the complete joint from local generative data and compare it exactly with an independent enumeration.
4. **Recognition and posterior derivation.** Select product or correlated \(Q_V\), verify every local marginal, slice the constructed joint at the observation, and derive evidence and posterior.
5. **One-arrow aggregate.** Construct `AggregateDatum`, verify common channel provenance, exact evidence preservation, positive and negative channel controls, and the KL decomposition.
6. **Artifact and replay checks.** Publish the six semantic artifacts, finalize through `RunStore`, reload them, and reproduce all reported values without consulting primitive fixtures.
7. **Revision-bound verification.** If separately requested, bind the finished revision and submit durable theory, code, and experiment claims to the repository's evidence-gated verifier. Until then results remain candidate evidence.

## Release 1 implementation phases

### Phase 0: freeze v1 and package exclusion

Capture `legacy_rescaling_v1.json` from the baseline before changing `config.py` or `experiment_support.py`. Record canonical config hashes for protected v1 launchers and the semantic outputs used by their regression tests. Add a packaging assertion that a built wheel contains `multiagent_elbo` and excludes `rg_v2` without changing setuptools discovery.

### Phase 1: exact contracts and primitive fixtures

Implement `ExactProbabilityLaw`, `ExactSubmeasure`, `ModelEvaluation`, `AgentDatum`, `AgentRecognitionDatum`, `RecordDatum`, `SelectorSpec`, `CoarseChannelSpec`, `PopulationJoint`, `PopulationInference`, and `AggregateDatum`. Parse the three primitive fixture files, derive recognition marginals, and reject derived population or posterior fields in runtime JSON.

### Phase 2: local population construction

Implement `construct_population_joint` with topological normalization, evaluator compatibility, and once-only record attachment. Establish a separately coded three-agent enumeration oracle.

### Phase 3: recognition and posterior

Implement product and declared-correlated selectors behind a narrowed private input seam. Implement `derive_population_inference`, exact local-marginal checks, the nonuniqueness pair, the Dirac-boundary control, and posterior derivation from positive evidence.

### Phase 4: one-step aggregate

Implement `aggregate_population` and `validate_aggregate_datum`. Reuse `ExactMarkovChannel`, extend it by the observation identity, and adapt exact laws to the existing finite VFE decomposition after structural checks. Add split-channel, observation-dependent-channel, selector-reading-generative, posterior-in-fixture, and record-double-count mutations.

### Phase 5: experiment shell and regression

Add the shared discriminator and registry record, the root launcher, `RunStore` publication, deterministic provenance, all-fixture regression, v1 hash regression, root-package import checks, and wheel exclusion. Run focused tests once after the phase's edits, followed by one broader CPU verification pass for the finished release.

No Release 1 phase adds gauge, multiscale, regeneration, adapter, generalization, or rendering modules. Those are independent follow-on decisions.

## Release 1 acceptance gates

Release 1 is accepted only when all of the following are mechanically demonstrated on the implementation revision.

### Location and dependency

* Every v2 implementation module is under repository-root `rg_v2/`; no `src/multiagent_elbo/rg_v2` directory exists.
* A built wheel excludes `rg_v2` and includes the preexisting `multiagent_elbo` package.
* No `multiagent_elbo` module imports `rg_v2`.
* The root launcher runs from the repository root without installing `rg_v2`.

### Agent, model, and local construction

* Every agent declares nonempty belief and model-presentation spaces and their exact combined support.
* Every model presentation has a normalized evaluator kernel, and positive-mass model slices of \(G_i\) reproduce it exactly.
* Every \(G_i\) and record kernel normalizes row by row.
* The product and correlated fixtures exercise at least one non-Dirac \(q_i^m\), derived from \(Q_i\).
* Every record has one owner, appears once in the input, and appears once in the construction trace.
* `construct_population_joint` accepts no recognition, observation, selector, or posterior object.
* Population normalization and an independent enumeration agree exactly.
* Runtime fixtures contain no derived population joint, evidence measure, selected population law, posterior, or expected status.

### Recognition and posterior

* Every selected population recognition law reproduces all local combined-state recognition laws exactly.
* Product and correlated fixtures with identical local laws produce distinct admitted joints.
* The Dirac-boundary control admits no second joint.
* Evidence and posterior are derived only from the constructed population joint and observed record, with positive evidence.
* Selector implementations cannot receive generative or posterior objects through their call seam.

### Coarse-graining

* One immutable channel instance pushes the complete generative joint, selected recognition law, and posterior.
* The observation coordinate is unchanged, all coarse laws normalize, and coarse evidence equals fine evidence exactly.
* The conditional KL defect is nonnegative within float64 tolerance and the KL chain residual is at most `1e-12` on the tiny fixtures.
* Split-channel and observation-dependent-channel mutations are rejected.
* `AggregateDatum` has no evaluator, observation interface, update rule, section data, `as_agent` method, or agent protocol compatibility.

### Artifacts, regression, and language

* Every finalized run contains exactly the six semantic artifacts plus `config.json` and `manifest.json`, with source revision, theory-tree hash, config hash, direct-input hashes, and named RNG streams.
* Artifact replay reproduces exact laws and diagnostics without rereading primitive fixtures.
* Every protected v1 canonical config hash and semantic result matches `legacy_rescaling_v1.json` after additive shared edits.
* No protected v1 experiment source changes except the allowed additive config and registry seams.
* Every metric has `assessment_scope="implementation_check"`, explicit theorem status, verification state, and claim origin.
* New findings remain `CANDIDATE` until separately verified against the implementation revision.
* No output claims meta-agency, autonomy, universality, an RG semigroup, a fixed point, a critical exponent, or a continuum limit.

## Later roadmap requiring separate approval

The following stages retain the design constraints discovered during planning, but they are not Release 1 implementation, artifacts, hypotheses, or acceptance gates.

### Gauge covariance

A later `rg_v2/gauge.py` may implement finite per-agent permutations and compatible record and target relabelings. It must report three diagrams separately: reconstruction of the population law from transformed local inputs, transformation of an already selected whole recognition law, and rerunning a selector on transformed local marginals. The third diagram is selector equivariance, a separate hypothesis. Parent priors, record labels, and retained marks must transform through their declared representations. A broken-transformation control must show that the wiring is live.

### Typed multiscale composition

A later `rg_v2/scale.py` may compare independently declared direct and staged routes. The direct channel cannot be constructed by composing the staged channels. Comparison must include complete generative, recognition, and posterior laws, evidence, VFE, exact total variation, finite KL where support permits, retained marks, and optional coupling readback with an omitted-interaction residual. Equality establishes only the tested commuting diagram. Failure produces a typed cocycle report, not an autonomous-semigroup label.

### Legacy semantic adapters

A later `rg_v2/legacy.py` may expose v1 objects as a read-only `LegacyAggregateWitness` with a nonempty `missing_local_first_obligations` set. It cannot return any v2 semantic type or manufacture missing local mechanisms, recognition marginals, selector provenance, full population joints, posterior derivation, or common-channel identity. Release 1 freezes v1 but does not implement this adapter.

### Regeneration and environmental controls

A later `rg_v2/regeneration.py` may compare passive, zero-source, matched one-shot, repeated, frozen-row, and environmental protocols. One-shot and repeated conditions must use byte-identical first injections. Every injection constructs a new next-level generative mechanism without reading next-level recognition or posterior and is labeled model replacement. A nonzero pair block under an injected pair source is expected and is not by itself emergence evidence.

### Bounded generalization and rendering

A later approved protocol may preregister thin-cycle and multiple-boundary or hierarchical graph families, ratios two and three, product and correlated selectors, and five instances per topology. Generated failures must remain in the case table. A later `rg_v2/rendering.py` must read finalized artifacts only and cannot import scientific computation modules. Figures may not contain hardcoded measured constants.

These roadmap stages introduce new fixture versions, artifact contracts, hypotheses, and verification obligations. They do not reuse the Release 1 config literal as though the evidence scope were unchanged.

## Risks and controls

### Root-package ambiguity

A root package can accidentally become installable through a future discovery change or import differently outside the repository. The wheel-exclusion test, one-way import check, root-launcher test, and explicit Release 1 status control this risk. Promotion to the installed package requires a later design decision.

### Decorative model structure

Belief and model labels could exist without affecting any executed path. Evaluator completeness, exact compatibility with positive-mass \(G_i\) slices, derived \(q_i^b\) and \(q_i^m\), and a non-Dirac model-law fixture ensure the distinction is operational.

### Hidden recognition dependence

Python cannot prevent a function from reading globals, so narrowed signatures are necessary but not sufficient. Constructors are pure, fixtures are passed explicitly, provenance records input hashes, and tests vary recognition and observation inputs while requiring population-construction bytes to remain identical.

### Factor order and record duplication

Canonical agent, parent, scope, and observation orders are stored in semantic objects rather than inferred from mapping order. Construction traces and independent enumeration expose missing or duplicated factors.

### Selector leakage

A correlated selector could accidentally read the population law and become a posterior fit. The selector helper receives only `AgentRecognitionDatum` objects and `SelectorSpec`; negative tests use sentinels that fail on any generative access.

### Split channel provenance

Numerically equal channel copies do not demonstrate that one declared channel was used. `aggregate_population` owns all three pushes in one call and records one object identity and canonical hash. A mutation using separate instances fails.

### Exponential state growth

Exact joint enumeration grows exponentially. Release 1 uses a three-agent witness of at most 64 latent states and a hard 4,096-state unit bound. Sparse, sampled, and GPU execution are deferred rather than introduced silently.

### v1 drift through shared seams

Adding a config discriminator and registry record can change serialization or registry order even without editing v1 experiments. Capturing v1 identities before those edits and rerunning the exact regression manifest afterward makes such drift visible.

### Evidence inflation

Finite agreement is evidence about declared fixtures, not a proof of universality or autonomy. Typed theorem status, candidate verification state, complete artifacts, and forbidden-claim checks preserve that boundary.

## Runtime and numerical bounds

Release 1 is an exact finite CPU laboratory. Exact structure uses `Fraction`; float64 is used only for logarithms, KL, VFE, and array mirrors. Unit fixtures use at most 4,096 latent states and are sized to finish in seconds on CPU. The three-agent vertical slice uses at most 64 latent states. No test builds a production-scale model, and no GPU claim is in scope.

If a later case crosses its approved state bound, the experiment records `inconclusive`. It does not change arithmetic, truncate a law, sample a subset, or route to CUDA without a new protocol.

## Deferred boundaries

Release 1 explicitly defers:

* `CoarseAgentDatum`, `MetaAgent`, or any automatic promotion from `AggregateDatum`;
* a coarse information interface, parent evaluator, recognition mechanism, update rule, action policy, or autonomous dynamics;
* section and gluing data across contextual overlaps, geometric bundle reconstruction, and global coarse-agent compatibility;
* gauge, multiscale-composition, regeneration, adapter, generalization, and rendering modules;
* learning a selector, generative mechanism, channel, or evaluator from data;
* stochastic, sparse, GPU, or large-state execution;
* arbitrary standard-Borel spaces, continuous laws, and undirected-potential normalization;
* autonomous-semigroup, universality-class, fixed-point, scaling-exponent, or continuum-limit claims;
* interpreting a population law or aggregate as consciousness, a universal observer, or an ontological super-agent;
* installation of `rg_v2` as part of the public `multiagent_elbo` package;
* manuscript changes implied only by numerical output.

A future coarse-agent design must begin from the missing fields rather than rename `AggregateDatum`. It must specify a coarse state, information-access map, evaluated generative mechanism, recognition law, update rule, and compatibility with the coarse population joint. Passing Release 1 supplies only probabilistic input to that future construction.

## Completion criterion

Release 1 is complete when the root-local laboratory reconstructs all three primitive fixtures, represents belief and model-presentation uncertainty with executable evaluators, derives population and coarse probability data through the declared dependency graph, freezes and replays v1 without drift, publishes the minimal six-artifact inventory, and passes the location, type, theory, provenance, and evidence-language gates above. The terminal public type remains `AggregateDatum`, and all empirical conclusions remain bounded to the finite declared fixtures and their recorded verification state.
