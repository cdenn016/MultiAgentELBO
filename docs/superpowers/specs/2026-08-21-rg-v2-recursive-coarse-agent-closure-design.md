# RG-v2 Recursive Coarse-Agent Closure Design

**Date:** 2026-08-21

**Status:** Approved in-chat architecture; committed specification awaiting final review

**Repository baseline:** `d4ce80bc9eda90ec54dc9c97d8405d7d28ca6182`

**Implementation location:** repository-root `rg_v2/`

**Release boundary:** static two-parent coarse-agent reconstruction with an all-observation Bayesian update table; no autonomous RG flow

## Purpose and decision

Release 1 ends at `AggregateDatum`. It proves that one declared, recognition-independent Markov channel pushes the complete generative joint, the selected recognition law, and the posterior while preserving evidence and satisfying the finite KL chain rule. That terminal aggregate is not recursively usable as an agent because it has no declared belief/model interpretation, parent mechanism, evaluated model family, observation-access interface, recognition mechanism, or update rule.

Phase 2 fills that type and construction gap. It constructs two coarse parents from four fine agents, reconstructs the pushed generative joint from ordinary next-level `AgentDatum` and `RecordDatum` objects, supplies lossless observation access and a normalized all-observation Bayesian update table, and then sends the constructed parents through the unchanged Release 1 population and inference functions. The phase answers one bounded question:

> Does one declared finite two-block fixture admit an exact, recursively usable representation by two agents of the laboratory's existing probabilistic family?

The answer is an implementation result about closure in the Release 1 combined-state `AgentDatum` family for a declared finite construction. It is not the stronger Chapter 4 separated belief/model factorization, a claim that blocking is canonical, a claim that arbitrary agent families close, a claim that the parents evolve autonomously, or a claim that repeated blocking defines an RG semigroup.

## Governing theory boundary

The manuscript theorem `thm:rg-pointwise-parent-datum` already establishes the common-channel pushforward

\[
P^c=(\operatorname{Id}_{\mathsf O}\times C)_\#P,
\qquad
Q^c=QC,
\qquad
\Pi_o^c=\Pi_oC,
\]

the preserved observation marginal, the induced evaluator tier, and the finite KL/VFE chain identity. Phase 2 does not re-prove those results. It begins with the additional obligation to factor the pushed generative joint into next-level local mechanisms and records, and it supplies a finite observation interface and update table sufficient for one exact recursive use of the existing constructors.

The philosophy chapter supplies the naming fence. A population law is not an agent, and evaluating a block conditional does not create a meta-agent. This phase uses the narrower term **coarse agent datum** only after the coarse state, evaluated generative mechanism, observation access, recognition law, and update rule have all been constructed and validated. It makes no claim about consciousness, agency as ontology, or a universal observer.

## Selected architecture

The flagship fixture has four fine agents in two declared blocks,

\[
I_A=(a_0,a_1),
\qquad
I_B=(a_2,a_3).
\]

Each fine agent has binary belief and binary model-presentation coordinates, so its combined state space has four labels. The fine latent support therefore has $4^4=256$ states. Four binary records give $2^4=16$ complete observation labels. All primitive generative and record rows are strictly positive, so every latent state and every observation has positive mass.

Release 1 encodes a complete fine observation as the ordered tuple of four record assignments. A reconstructed population with one combined record necessarily encodes a different outer record identifier. The structural declaration therefore supplies an explicit bijection

\[
\lambda:\mathsf O_{\mathrm{fine}}\longrightarrow\mathsf O_{AB}
\]

from the sixteen fine observation labels to sixteen compound-record outcome labels. Directly pushed tables retain the fine labels; reconstructed `PopulationJoint` objects retain the compound-record labels. Every cellwise comparison, access lookup, evidence comparison, and posterior comparison applies $\lambda$ explicitly. Phase 2 claims lossless observation relabeling, not literal equality of the two serialized observation supports.

Each block has an independently declared normalized structural channel,

\[
C_A:\mathsf Y_{I_A}\rightsquigarrow
\mathsf Z_A=\mathsf B_A\times\mathsf M_A,
\qquad
C_B:\mathsf Y_{I_B}\rightsquigarrow
\mathsf Z_B=\mathsf B_B\times\mathsf M_B,
\]

with binary coarse belief and binary coarse model-presentation coordinates. The flagship uses deterministic belief-parity and model-parity channels, but the public contract is an exact finite normalized channel contract rather than a parity-specific API. The ordered product channel

\[
C_{AB}(y,dz_A,dz_B)=C_A(y_{I_A},dz_A)C_B(y_{I_B},dz_B)
\]

acts on the complete fine latent support and leaves the observation coordinate unchanged. Its target support is exactly the canonical Cartesian support of the two next-level agents.

The pushed joint is

\[
P^c(o,z_A,z_B)
=
\sum_y P(o,y)C_{AB}(y,z_A,z_B).
\]

The next-level agent order is declared as $(A,B)$. The exact parent mechanisms are the chain disintegration

\[
G_A(z_A)=P^c_Z(z_A),
\qquad
G_B(z_B\mid z_A)=
\frac{P^c_Z(z_A,z_B)}{P^c_Z(z_A)}.
\]

The fixture requires every denominator and every positive model slice used by the evaluator to be strictly positive. Phase 2 therefore uses `null_row_policy="forbid"`; it does not introduce arbitrary null representatives.

The exact record fallback is one combined hyper-record owned once by $B$, scoped to $(A,B)$, with outcome support $\mathsf O_{AB}$ and kernel

\[
K^c(\lambda(o)\mid z_A,z_B)=
\frac{P^c(o,z_A,z_B)}{P^c_Z(z_A,z_B)}.
\]

The product of $G_A$, $G_B$, and $K^c$ reconstructs $P^c$ exactly. A separately evaluated sparse-record candidate is allowed to fail. The implementation must report its exact obstruction instead of replacing the dense fallback with an unsupported local factorization.

## Generative and recognition separation

The coarse generative path accepts only the constructed fine `PopulationJoint` and declared structural data. Its public seam is:

```python
def construct_coarse_population_joint(
    population: PopulationJoint,
    structure: RecursiveCoarseStructure,
) -> CoarsePopulationDatum:
    ...
```

`RecursiveCoarseStructure` contains the block partition, parent order, parent-state interpretations, exact block channels, full-context provenance, observation bijection, declared sparse candidate, and fixed null-row policy. It contains no local recognition law, selector, realized observation, evidence, posterior, `PopulationInference`, or `AggregateDatum`. The function must not accept or inspect those objects through positional arguments, keyword arguments, closures, globals, or fixture rereads.

The returned `CoarsePopulationDatum` contains the exact combined channel declaration, a neutral pushed joint table retaining fine observation labels, the constructed next-level agent mechanisms and evaluator families, the once-owned combined record, the observation bijection, and the population reconstructed by the unchanged `construct_population_joint`. Its exact validation compares the two tables after relabeling and requires byte-stable canonical serialization of the generative result under mutations of fine recognition laws, selector coupling, realized observation, and posterior.

Information access and the Bayesian update table form a second, generative-derived path. They receive the completed coarse population and explicit `CoarseAccessSpec` inputs, but no fine inference. Recognition is a third path. It may use a fine `PopulationInference` only after the generative and information objects are complete. It pushes the selected fine recognition law through the already declared combined channel, derives the two local coarse recognition marginals, retains the exact pushed joint as a declared correlated coarse selector, and calls the unchanged `derive_population_inference` on the reconstructed next-level population.

The flagship access specifications preserve the complete reconstructed observation support:

\[
\operatorname{Acc}_A(o)=o,
\qquad
\operatorname{Acc}_B(o)=o.
\]

The fixture supplies one observation-independent fine recognition tuple and selector. Each parent therefore has a normalized constant-row initial recognition kernel whose sixteen rows equal its pushed local recognition law. Observation-dependent recognition-family descent is not proved in this phase. Each parent also has a separately typed Bayesian update kernel whose row for information value $o$ is the corresponding marginal of $P^c(z_A,z_B\mid o)$. The full joint coarse posterior remains a population inference output; local posterior marginals do not determine it.

The update table is derived once from the complete reconstructed generative joint for every admitted information value before any inference object is supplied to the recognition constructor. It is not fitted from one realized observation and does not depend on the selected recognition law. It is a finite law-valued Bayesian update interface, not a physical-time transition, action policy, learning rule, or proof of autonomous dynamics.

## Exact semantic types

Phase 2 adds immutable types without changing the field order or behavior of any Release 1 type.

```python
@dataclass(frozen=True)
class CoarseAgentSpec:
    agent_id: str
    source_agent_ids: tuple[str, ...]
    parent_ids: tuple[str, ...]
    source_context_id: str
    belief_labels: tuple[str, ...]
    model_labels: tuple[str, ...]
    state_labels: tuple[str, ...]
    block_channel: ExactMarkovChannel
    null_row_policy: Literal["forbid"]


@dataclass(frozen=True)
class CoarseObservationSpec:
    record_id: str
    fine_observation_labels: tuple[str, ...]
    compound_outcome_labels: tuple[str, ...]
    compound_outcome_by_fine_observation: tuple[str, ...]


@dataclass(frozen=True)
class SparseRecordFactorizationSpec:
    left_record_ids: tuple[str, ...]
    right_record_ids: tuple[str, ...]
    left_outcome_labels: tuple[str, ...]
    right_outcome_labels: tuple[str, ...]
    left_outcome_by_fine_observation: tuple[str, ...]
    right_outcome_by_fine_observation: tuple[str, ...]


@dataclass(frozen=True)
class RecursiveCoarseStructure:
    structure_id: str
    source_agent_order: tuple[str, ...]
    coarse_agent_order: tuple[str, ...]
    agent_specs: tuple[CoarseAgentSpec, ...]
    observation: CoarseObservationSpec
    sparse_record_candidate: SparseRecordFactorizationSpec


@dataclass(frozen=True)
class PushedCoarseJoint:
    context_id: str
    latent_labels: tuple[str, ...]
    fine_observation_labels: tuple[str, ...]
    joint_masses: tuple[tuple[Fraction, ...], ...]
    combined_channel_sha256: str


@dataclass(frozen=True)
class CoarseGenerativeDatum:
    spec: CoarseAgentSpec
    agent: AgentDatum
    source_population_sha256: str
    block_channel_sha256: str
    combined_channel_sha256: str


@dataclass(frozen=True)
class CoarseAccessSpec:
    agent_id: str
    observation_labels: tuple[str, ...]
    information_labels: tuple[str, ...]
    information_by_observation: tuple[str, ...]
    access_kind: Literal["identity_observation"]


@dataclass(frozen=True)
class CoarseRecognitionDatum:
    agent: AgentDatum
    initial_recognition: AgentRecognitionDatum
    recognition_kernel: ExactMarkovChannel
    source_recognition_sha256: str


@dataclass(frozen=True)
class CoarseUpdateDatum:
    agent_id: str
    update_kind: Literal["exact_bayes_marginal"]
    kernel: ExactMarkovChannel
    source_population_sha256: str
    access_sha256: str


@dataclass(frozen=True)
class CoarseInformationDatum:
    access: CoarseAccessSpec
    update: CoarseUpdateDatum


@dataclass(frozen=True)
class CoarseAgentDatum:
    generative: CoarseGenerativeDatum
    information: CoarseInformationDatum
    recognition: CoarseRecognitionDatum


@dataclass(frozen=True)
class CoarsePopulationDatum:
    structure: RecursiveCoarseStructure
    combined_channel: CoarseChannelSpec
    generative_agents: tuple[CoarseGenerativeDatum, ...]
    records: tuple[RecordDatum, ...]
    pushed_joint: PushedCoarseJoint
    reconstructed_population: PopulationJoint


@dataclass(frozen=True)
class RecursiveObservationDatum:
    fine_observed_record: str
    coarse_observed_record: str
    fine_inference: PopulationInference
    coarse_inference: PopulationInference
    pushed_recognition: ExactProbabilityLaw
    pushed_posterior: ExactProbabilityLaw
    coarse_agents: tuple[CoarseAgentDatum, ...]
```

`CoarseAgentSpec.state_labels` is the canonical belief-major Cartesian product of its belief and model labels. Its block-channel target support equals those labels. The block source supports are the canonical supports of exactly the declared source agents. The source blocks are disjoint, nonempty, cover the fine agent order exactly once, and appear in the declared coarse order.

`CoarseGenerativeDatum.agent` is an ordinary Release 1 `AgentDatum`. Every positive model slice of its generative kernel disintegrates to the corresponding evaluator row exactly. `CoarsePopulationDatum.records` contains one combined record in the flagship construction. Only the tuple of `CoarseGenerativeDatum.agent` objects and `records` enters `construct_population_joint`.

`CoarseAccessSpec` is deliberately restricted to identity access on the reconstructed observation support in Phase 2. `CoarseRecognitionDatum.recognition_kernel` maps every information label to a normalized local recognition law. `CoarseUpdateDatum.kernel` maps every information label to a normalized local posterior law. The two kernels are separate semantic objects, even when a boundary fixture makes some rows equal.

`CoarseAgentDatum` is not accepted by the generative constructor and is not added to Release 1 protocols. It is a Phase 2 result bundle proving that each constructed parent has the finite data required for the next recursive invocation. `AggregateDatum` gains no method, adapter, field, or protocol conformance.

## Public construction and validation seams

The new public functions are:

```python
def construct_coarse_population_joint(
    population: PopulationJoint,
    structure: RecursiveCoarseStructure,
) -> CoarsePopulationDatum:
    ...


def construct_coarse_information_interfaces(
    coarse_population: CoarsePopulationDatum,
    access_specs: tuple[CoarseAccessSpec, ...],
) -> tuple[CoarseInformationDatum, ...]:
    ...


def construct_coarse_recognition(
    coarse_population: CoarsePopulationDatum,
    information: tuple[CoarseInformationDatum, ...],
    fine_inference: PopulationInference,
) -> tuple[CoarseAgentDatum, ...]:
    ...


def derive_recursive_observation(
    coarse_population: CoarsePopulationDatum,
    coarse_agents: tuple[CoarseAgentDatum, ...],
    fine_inference: PopulationInference,
) -> RecursiveObservationDatum:
    ...


def validate_recursive_observation(
    datum: RecursiveObservationDatum,
    coarse_population: CoarsePopulationDatum,
    numerics: NumericsConfig,
) -> None:
    ...
```

`construct_coarse_information_interfaces` receives explicit access specifications and derives every Bayesian update row from the already completed coarse generative joint. It cannot receive or traverse an inference object. The access-descent residual is
$\max_{\operatorname{Acc}(o)=\operatorname{Acc}(o')}\operatorname{TV}(U(o),U(o'))$. The identity fixture makes this zero; a test-only collapsed-access mutation identifies two observations with unequal update rows and must fail. Each parent must have at least two distinct update rows so that control is live.

`construct_coarse_recognition` uses `fine_inference.recognition` only to create the initial recognition law and correlated coarse selector. A mutation of `fine_inference.recognition` may change `CoarseRecognitionDatum.initial_recognition`, its recognition kernel, and the selector, but it must not change `CoarseGenerativeDatum`, the combined record, the reconstructed population, the access map, or the Bayesian update kernel.

`derive_recursive_observation` calls the unchanged Release 1 population inference path and compares its selected coarse recognition and derived posterior with the direct common-channel push. It does not implement a second selector or conditioning formula. `validate_recursive_observation` replays those arrows from explicit inputs and supplied `NumericsConfig`; it uses no ambient tolerance.

## Conditional finite Release 1 combined-state construction theorem

Let $P(o,y\mid X)$ be a strictly positive finite joint, let the declared source blocks partition the fine agent order, and let the normalized block channels define a normalized combined channel $C_{AB}$ with target support

\[
\mathsf Z_A\times\mathsf Z_B
=
(\mathsf B_A\times\mathsf M_A)
\times
(\mathsf B_B\times\mathsf M_B).
\]

Assume the pushed latent marginal is strictly positive and every model slice needed by the declared evaluators has positive mass. Then the chain factors $(G_A,G_B)$, their induced Release 1 evaluators, and the combined record $K^c$ above are normalized exact finite kernels. Supplying those objects to `construct_population_joint` reconstructs the neutral pushforward table after applying the declared observation bijection exactly.

For every observation $o$ with positive evidence, conditioning the reconstructed population at the compound record $\lambda(o)$ equals pushing the fine posterior through $C_{AB}$. For any selected fine recognition law, pushing it through $C_{AB}$, taking its two local marginals, and retaining the full pushed joint as the declared correlated selector causes `derive_population_inference` to reproduce that pushed recognition law exactly. The local Bayesian update rows equal the marginals of the reconstructed population posterior.

The proof is finite disintegration. Normalization follows from exact row sums. Multiplying the latent chain factors gives the pushed latent marginal, and multiplying by $K^c$ gives the complete pushed joint cell by cell. The posterior statement follows by dividing the same cells by the preserved positive observation evidence. Recognition reconstruction follows because the declared selector carries the full pushed joint and its verified marginals are the supplied local laws.

This theorem establishes static recursive representability in the Release 1 combined-state `AgentDatum` family under declared structure and positivity. It does not establish the narrower Chapter 4 separation $P_B^m(dm_B\mid m_A)P_B^b(db_B\mid b_A,m_B)$, uniqueness of the factorization, a sparse interaction graph, autonomy, dynamic semiconjugacy, Markov lumpability, or closure under another independently chosen blocking map.

## Flagship primitive fixture

The sole launchable Phase 2 fixture is `lf4_two_parent_recursive_v1`. Its primitive JSON is self-contained and contains only:

* four ordered fine `AgentDatum` declarations with exact positive generative rows and evaluator data;
* four once-owned positive binary `RecordDatum` declarations, including cross-block scopes that make the sparse-record obstruction live;
* four exact local recognition laws and one exact declared fine selector coupling;
* the two-block structural partition, two exact block channels, the two belief/model target interpretations, parent order, source context, observation bijection, and `SparseRecordFactorizationSpec`;
* two explicit identity `CoarseAccessSpec` declarations; and
* one declared observation only for the click-to-run default, while the experiment still evaluates all sixteen observations.

The primitive file must not contain a constructed fine population joint, selected population recognition law, evidence, posterior, combined channel, coarse mechanisms, evaluator rows derived from the coarse joint, combined record, pushed or reconstructed population, expected metric values, status, or pass flags.

The fine mechanisms and all record rows are strictly positive. The declared fine selector coupling is absolutely continuous with respect to every posterior and yields a pushed coarse recognition law with non-Dirac model marginals for both parents. Every one of the sixteen observation labels has positive evidence. The complete joint has 4,096 exact cells, which is the fixed Phase 2 ceiling.

Production construction is checked against a separately coded exact enumerator that does not call the constructor's factor, support, channel-product, disintegration, or record helpers. Tests add a third oracle using frozen rational tables or independently expanded literal loops. Agreement on normalization or selected cells is insufficient; all 4,096 fine cells and all 256 coarse cells are compared exactly.

## Sparse-record obstruction control

Exact recursion is always permitted to retain the combined record $K^c$. The hashed `SparseRecordFactorizationSpec` declares two ordered, disjoint, exhaustive groups of the four fine records and explicit projections

\[
\pi_L:\mathsf O_{\mathrm{fine}}\to\mathsf O_L,
\qquad
\pi_R:\mathsf O_{\mathrm{fine}}\to\mathsf O_R.
\]

Cross-block record ownership does not select either projection implicitly. Phase 2 asks whether the induced conditional kernel has the narrower factorization

\[
K^c(o_L,o_R\mid z_A,z_B)
\stackrel{?}{=}
K_L(o_L\mid z_A)K_R(o_R\mid z_B).
\]

If this equality holds, the left marginal is independent of $z_B$, the right marginal is independent of $z_A$, and the factors are uniquely those marginals. The runtime checks those marginal-invariance identities and the resulting product equality exactly for every coarse state. `sparse_record_factorization_violation_count` counts the failed exact identities and must be at least one. The maximum exact conditional total-variation violation is retained in `coarse_population.json`; it is not represented by a floating strict-inequality metric.

Cross-block fine records are chosen so the declared sparse factorization fails. The failure is an expected countercontrol, not a failed recursive construction. The runtime preserves both facts: the dense combined record reconstructs the pushed joint exactly, and the declared sparse family does not contain it. It must not describe the dense fallback as evidence for local, pairwise, or graph-sparse closure.

## Exact invariants and countercontrols

The implementation validates the following before publication.

1. The four source agents and two source blocks are nonempty, ordered, disjoint, and exhaustive. The two parent specifications are topologically ordered.
2. Every block channel is normalized, recognition-independent, and supported exactly on its declared block and canonical parent state labels. The combined channel is the exact ordered product of those declarations and leaves the fine observation coordinate unchanged.
3. Both parent state interpretations are bijections onto binary belief by binary model support. Malformed, duplicated, missing, or reordered interpretations are rejected.
4. The fine-to-compound observation declaration is an ordered bijection. Missing, duplicated, reordered, or nonexhaustive outcome maps are rejected.
5. All pushed latent, parent-context, and model-slice denominators are positive under the flagship's `forbid` policy.
6. Parent mechanisms, evaluator rows, the combined record, initial recognition kernels, and update kernels normalize exactly.
7. The reconstructed and pushed generative tables agree in every cell after the declared observation relabeling. Mutating a positive evaluator row, parent factor, factor order, bijection, or combined record is detected.
8. Changing fine local recognition, selector coupling, realized observation, evidence, or posterior leaves canonical coarse generative bytes unchanged. Sentinel inference and aggregate objects fail if the generative constructor touches them.
9. `AggregateDatum`-only promotion is rejected with an explicit list of missing structural, generative, observation, recognition, and update obligations.
10. Each access map is total and identity-valued. A collapsed-access mutation that maps observations with unequal update rows to one information value is rejected by the descent check.
11. For all sixteen observations, direct channel push and reconstruction agree exactly on recognition, evidence, and posterior after relabeling. A split-channel or observation-changing channel fails this commutation check.
12. Both coarse model recognition marginals are non-Dirac.
13. The exact dense record fallback passes while the declared sparse family produces at least one exact factorization violation.

## Configuration and repository boundary

Phase 2 is an additive root-local experiment. It adds the strict experiment discriminator `renormalization_v2_recursive` with exactly these theory keys:

```python
THEORY = {
    "experiment": "renormalization_v2_recursive",
    "fixture": "lf4_two_parent_recursive_v1",
    "arithmetic": "exact_rational",
}
```

The existing exact-rational CPU and float64 gates remain binding. The launcher supplies `RUN`, `THEORY`, `NUMERICS`, and `OUTPUT`, inserts only the adjacent `src` path, performs no work on import, and accepts no command-line flags. It must execute by absolute path from an arbitrary working directory with an empty inherited `PYTHONPATH`.

The new implementation surface is:

```text
rg_v2/
    coarse_agent.py
    recursive_fixtures.py
    recursive_experiment.py
    data/
        lf4_two_parent_recursive_v1.json
run_renormalization_v2_recursive_lab.py
tests/rg_v2/
    test_coarse_agent.py
    test_recursive_fixtures.py
    test_recursive_experiment.py
```

Additive edits to `src/multiagent_elbo/config.py` and `src/multiagent_elbo/experiment_support.py` are limited to the new strict config variant and registry record. The existing `renormalization_v2` entry, its six artifacts, thirteen metrics, fixture loader, launcher, canonical config hashes, and scientific results remain unchanged. No `multiagent_elbo` module imports `rg_v2`; setuptools discovery remains `where=["src"]`; built wheels include `multiagent_elbo` and exclude root `rg_v2`.

## Artifact and provenance contract

Each finalized run contains `config.json`, `manifest.json`, and exactly eight Phase 2 semantic artifacts:

```python
(
    "fixture_snapshot",
    "fine_population",
    "coarse_generative",
    "coarse_interfaces",
    "coarse_population",
    "all_observation_inference",
    "metrics",
    "arrays",
)
```

Their contents are:

| Artifact | Required content |
|---|---|
| `fixture_snapshot.json` | Complete primitive fixture, raw source hash, and independent canonical hashes for generative, recognition, structural-channel, and access subrecords |
| `fine_population.json` | Constructed and independently enumerated fine generative joint, exact equality result, factor trace, and fine input hashes |
| `coarse_generative.json` | Parent specifications, block and combined channel declarations and hashes, observation bijection, sparse candidate, parent mechanisms, evaluator rows, combined record, and only generative/structural direct-input hashes |
| `coarse_interfaces.json` | Access specifications, Bayes-update tables, initial parent recognition laws and constant-row kernels, their local marginals, the declared correlated coarse selector, and ordered generative/access/recognition direct-input hashes |
| `coarse_population.json` | Exact neutral pushed table and reconstructed `PopulationJoint`, relabeled cellwise equality result, dense-record result, sparse-factorization violation count, and maximum exact conditional-TV violation |
| `all_observation_inference.json` | Ordered fine/compound record pairs for all sixteen observations, including fine inference, direct coarse push, reconstructed coarse inference, access values, update rows, evidence, posterior, and exact residuals |
| `metrics.json` | Fixed ordered `MetricRecord` inventory with explicit status fields |
| `arrays.npz` | Float64 mirrors of finalized laws and diagnostics plus fixed-width Unicode provenance; no additional scientific result |

`coarse_generative.json` is finalized before any function receives a fine inference object. It contains no access, update, recognition, selector, realized observation, evidence, or posterior object. `coarse_interfaces.json` depends on that finalized generative hash plus separately hashed access and recognition inputs. It may change under a recognition mutation; `coarse_generative.json` must not.

Every JSON artifact and the NPZ archive carry `schema_version`, `fixture_id`, `producer_commit`, `config_hash`, and ordered direct-input names and SHA-256 values. Exact fractions serialize as reduced numerator/positive-denominator records. Support-sensitive maps serialize as ordered records. The primitive snapshot exposes subrecord hashes so a generative artifact can name only the generative and structural inputs even though the primitive declarations share one physical file.

All scientific bodies, exact metrics, finalized envelopes, direct-input hashes, and the complete NPZ mapping are computed in memory before `RunStore.create`. Artifact hashing proceeds in dependency order and no payload is mutated after hashing. Replay loads finalized artifacts with `allow_pickle=False`, disables primitive fixture access, reconstructs the semantic types, and recomputes all mathematical and structural metrics. It does not compare Python object identity across processes.

## Fixed metric inventory

`metrics.json` contains exactly this ordered inventory:

```python
(
    "block_channel_normalization_residual",
    "coarse_state_interpretation_violation_count",
    "observation_bijection_violation_count",
    "coarse_agent_kernel_normalization_residual",
    "coarse_evaluator_compatibility_residual",
    "coarse_record_kernel_normalization_residual",
    "coarse_population_normalization_residual",
    "generative_roundtrip_residual",
    "recognition_marginal_residual",
    "recognition_roundtrip_residual",
    "evidence_roundtrip_residual",
    "posterior_roundtrip_residual",
    "access_descent_residual",
    "update_normalization_residual",
    "update_posterior_residual",
    "coarse_model_marginal_non_dirac_count",
    "forbidden_dependency_violation_count",
    "sparse_record_factorization_violation_count",
    "minimum_conditional_kl_defect",
    "maximum_kl_chain_residual",
)
```

The first fifteen residual or violation metrics target exact zero. `coarse_model_marginal_non_dirac_count` has a lower bound of two. `forbidden_dependency_violation_count` targets zero. `sparse_record_factorization_violation_count` has a lower bound of one on the declared control. `minimum_conditional_kl_defect` may be no smaller than `-1e-12`, and `maximum_kl_chain_residual` is the maximum absolute chain residual and may be no larger than `1e-12` over the sixteen observations.

Every metric has `assessment_scope="implementation_check"`, an explicit theorem status, `verification_state="CANDIDATE"`, and an explicit claim origin. Exact construction identities may cite `ESTABLISHED` manuscript results as theorem status, but the executable result remains candidate evidence until a separate revision-bound verification action is requested and completed.

## Acceptance gates

Phase 2 is accepted only when the implementation revision mechanically demonstrates all of the following.

### Static recursive construction

* The flagship contains four fine agents, two disjoint exhaustive blocks, two coarse parents, 256 fine latent states, sixteen positive-evidence observations, and two non-Dirac coarse model marginals.
* The generative constructor has no inference, recognition, selector, observed-record, posterior, or aggregate input seam.
* The fine-to-compound observation map is an exact ordered bijection, and exact parent mechanisms plus the once-owned combined record reconstruct the complete pushed joint cell by cell after applying it.
* The resulting ordinary `AgentDatum` and `RecordDatum` objects pass through the unchanged Release 1 `construct_population_joint` function.
* `AggregateDatum` remains terminal and unmodified.

### Observation, recognition, and update

* Identity access is total for both parents and all sixteen reconstructed observation labels; each parent has at least two distinct update rows.
* Initial recognition kernels and Bayesian update kernels normalize row by row.
* The coarse selector reconstructs the full pushed recognition law from verified local parent marginals.
* For every paired fine and compound observation, direct and reconstructed evidence and posterior agree exactly, and each update row equals the corresponding parent posterior marginal.
* Generative artifacts and hashes remain identical under recognition, selector, observed-record, and posterior mutations.

### Live negative controls

* Malformed state interpretations, observation bijections, factor order, evaluator rows, record rows, access descent, split channels, and observation-changing channels are rejected or yield their prescribed nonzero residual.
* The dense record fallback passes exactly while the declared sparse family has at least one exact factorization violation and a recorded positive conditional-TV magnitude.
* An aggregate-only promotion attempt fails with the missing-obligation set.

### Artifacts and regressions

* A run finalizes exactly the eight semantic artifacts plus `config.json` and `manifest.json`.
* Artifact-only replay reproduces all exact laws, all-observation results, the twenty-metric inventory, and NPZ mirrors without reading primitive fixture files.
* Release 1's three fixtures, exact six-artifact inventory, thirteen metrics, launcher, replay, canonical config identities, and v1 regression manifest remain unchanged.
* The new launcher passes arbitrary-working-directory and empty-`PYTHONPATH` checks; reverse imports remain absent; a built wheel still excludes `rg_v2`.
* Focused CPU tests run once after batched implementation edits, followed by one broader CPU verification pass. No CUDA result is claimed.

## Explicit nonclaims and deferred work

Phase 2 does not select the blocks, channels, belief/model factorizations, parent order, access map, or null versions canonically. It does not prove the Chapter 4 separated factorization $P_B^m(dm_B\mid m_A)P_B^b(db_B\mid b_A,m_B)$ or that the evaluator depends only on a reduced structural context $X_A$; the full fine context and its hash remain explicit provenance. It preserves observations only through one declared bijection and does not prove a coarsened observation interface or observation-dependent recognition-family descent. It does not prove sparse or pairwise record closure.

It also does not establish autonomous parent dynamics, dynamic semiconjugacy, Markov lumpability, moving membership, retained-memory sufficiency, nonequilibrium persistence, physical time, an RG semigroup, direct-versus-staged scale composition, a fixed point, an attractive manifold, scaling exponents, universality, or a continuum limit. Gauge marks, section/gluing data, nontrivial \(\boldsymbol\Xi_A\) and \(\mathsf H_A\), learned selectors or channels, stochastic approximations, GPU execution, and large-state paths remain outside this phase.

The next approved experiment should be direct-versus-staged composition on independently declared channels after this agent contract is stable. Only a later integration phase should combine recursive agent construction with multiscale composition. Neither later phase may reinterpret a passing static witness as autonomous RG flow.

## Risks and controls

### Tautological reconstruction

Disintegration can always encode a positive finite joint in a dense chain and hyper-record. That existence result is useful only if its scope is explicit. The design therefore requires an independently coded full-table oracle, a live sparse-factorization obstruction, forbidden-dependency mutations, and no claim of uniqueness or locality.

### Recognition leakage into generation

Keeping all primitives in one fixture file could conceal a recognition read. Narrow public signatures, subrecord hashes, sentinel objects, mutation-stable canonical generative bytes, and fixture-read guards make that path observable.

### Local marginals mistaken for a joint

The two parent recognition marginals do not determine their correlated joint. The exact pushed coarse recognition law is retained as the declared selector coupling and is checked against both marginals before the existing inference constructor is called.

### Update mistaken for dynamics

The exact Bayes table maps each admitted information label to a posterior law. It has no time coordinate, action, environment transition, or next-parameter state. Names, types, metrics, and documentation must call it an update table, not autonomous evolution.

### Artifact inflation

The eight semantic artifacts separate generative, interface, population, and all-observation evidence without adding figures or duplicated scientific outputs. Arrays are numerical mirrors only. Rendering requires a later approved design.

### State growth

The flagship has 4,096 exact joint cells and is the hard Phase 2 ceiling. A larger case fails pre-effect rather than sampling, truncating, changing arithmetic, or routing to CUDA.

## Completion criterion

Phase 2 is complete when the root-local laboratory constructs the four-agent fine population from primitives, applies two declared block channels, reconstructs the exact pushed joint from two ordinary next-level agents and one combined record through the declared observation bijection, supplies both parents with identity access, normalized constant-row initial recognition, and an all-observation exact Bayesian update table, and reproduces pushed recognition, evidence, and posterior for all sixteen observations through unchanged Release 1 constructors. The dense exact construction and sparse factorization failure must both remain visible, every metric must remain `CANDIDATE`, and all autonomy, multiscale-composition, universality, continuum, and ontological claims must remain open.
