# Local-First Renormalization v2 Release 1 Implementation Plan

> **For agentic workers:** Execute task-by-task with `superpowers:subagent-driven-development` or `superpowers:executing-plans`. Write the tests before each implementation slice, but execute them together in the single focused pass in Task 8.

**Goal:** Build an exact finite, repository-local laboratory that begins with agent-indexed belief/model spaces, evaluated local generative mechanisms, local recognition laws, and once-owned record kernels; constructs the population law; derives recognition and posterior data; and pushes the complete datum through one recognition-independent channel to `AggregateDatum`.

**Architecture:** Release 1 lives directly under root-level `rg_v2/`. It imports stable public primitives from `src/multiagent_elbo`; installed-package modules never import `rg_v2`. Shared installed-package edits are limited to an additive theory-config discriminator in `config.py` and an additive experiment record in `experiment_support.py`. Package discovery, pytest metadata, coverage metadata, artifact/runtime libraries, and v1 experiment implementations remain unchanged. Release 1 stops at `AggregateDatum` and supplies no coarse-agent semantics.

**Baseline:** `c04a56e80abf3fd956941aa0021a3a93ea53eaae`

**Binding specifications:** `docs/superpowers/specs/2026-08-21-local-first-renormalization-v2-design.md` and its corrections in `docs/superpowers/specs/2026-08-21-local-first-renormalization-v2-design-amendment.md`. Where they differ, the amendment governs.

**Runtime:** `C:\Python314\python.exe`; exact `fractions.Fraction` structure; NumPy float64 only at the existing finite VFE boundary and in `arrays.npz`; no CUDA claim.

## Fixed boundaries

- Create `rg_v2/` at repository root. Never create `src/multiagent_elbo/rg_v2/`.
- Do not edit `pyproject.toml`, including setuptools discovery, pytest paths, and coverage metadata.
- The root launcher inserts only `ROOT / "src"` into `sys.path`. Its script directory already supplies root.
- Do not edit `artifacts.py`, `runtime.py`, `finite/scale_cocycle.py`, v1 experiments, or v1 launchers. Reuse their public APIs.
- Generate `legacy_rescaling_v1.json` mechanically from a detached temporary worktree at the baseline before either shared edit. Do not transcribe remembered hashes or semantic constants.
- Publish exactly six semantic artifacts: `fixture_snapshot.json`, `population_joint.json`, `population_inference.json`, `aggregate_datum.json`, `metrics.json`, and `arrays.npz`.
- Emit exactly the thirteen metric names in Task 7.
- Primitive fixture JSON supplies no population joint, selected population recognition, evidence slice, evidence, posterior, expected result, or verification state.
- `construct_population_joint` accepts generative data and context only. The private recognition selector accepts local recognition data and a selector only.
- `aggregate_population` receives one `CoarseChannelSpec` and one validated `NumericsConfig`. The identical in-process `ExactMarkovChannel` object performs all three pushes. Persist the channel ID and canonical hash, never `id()`.
- `AggregateDatum` stores `observed_record` but no channel object or evidence submeasure. It has no evaluator, observation interface, update rule, section data, or agent conversion.
- The VFE adapter consumes fine `P_V`, the fine evidence submeasure, fine `Q`, the exact channel converted to `MarkovKernel`, and the supplied numerics. Record the conditional KL defect and absolute residual.
- Reject every figure request and any `numerics.atol > 1e-12` before RNG or filesystem effects, including `collect_diagnostics=False, render_figures=True`.
- Do not compare artifact bytes from different output roots. Compare decoded mathematics while treating config/provenance identity as root-specific.
- Execute the focused tests once after implementation, followed by one broader CPU pass required by the base design's Phase 5.

## Release 1 files

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
tests/rg_v2/
    test_contracts.py
    test_population.py
    test_coarse.py
    test_fixtures.py
    test_experiment.py
    test_legacy_regression.py
docs/change-logs/2026-08-21.md
```

Do not add `gauge.py`, `scale.py`, `legacy.py`, `regeneration.py`, or `rendering.py` in this release.

## Task 1: Freeze v1 and establish the root-local boundary

**Create:** `rg_v2/README.md`, `rg_v2/__init__.py`, `rg_v2/data/legacy_rescaling_v1.json`, `tests/rg_v2/test_legacy_regression.py`

Create a detached temporary Git worktree at the declared baseline with `git worktree add --detach <verified-temporary-path> c04a56e80abf3fd956941aa0021a3a93ea53eaae`. Verify `git rev-parse HEAD` inside it before capture. This allows the implementation branch to contain prior documentation commits while binding v1 evidence to the intended source revision. Do not require implementation `HEAD` itself to equal the baseline. After capture, remove only that exact task-owned worktree through `git worktree remove <verified-temporary-path>`.

Run the baseline capture in a fresh isolated subprocess, never in the implementation interpreter. Launch `C:\Python314\python.exe -I -B -c <capture-bootstrap>` with `cwd` equal to the detached baseline root and an environment copy whose inherited `PYTHONPATH` is the empty string. The bootstrap imports only standard-library modules until it resolves the baseline root, inserts `<baseline-root>/src` at `sys.path[0]` and `<baseline-root>` at `sys.path[1]`, and only then calls `runpy` or imports `multiagent_elbo`. Because this is a fresh interpreter, its project-facing `sys.modules` starts empty; do not preload or pass current-branch modules into it. Create the scale-cocycle output directory under a verified temporary directory outside both the implementation and detached worktrees. Redirect incidental capture output to stderr and emit exactly one canonical machine-readable JSON object on stdout; the implementation-side controller parses that JSON and, only in explicit refresh mode, writes the manifest in the implementation worktree.

The subprocess capture implementation accepts the selected revision root and external temporary output root and:

1. loads each selected-revision launcher with `runpy.run_path` under a non-main name;
2. constructs `ExperimentConfig` from its `RUN`, `THEORY`, `NUMERICS`, `OUTPUT`, and optional `COMPUTE` dictionaries;
3. records both `canonical_config_json(config)` and its SHA-256 after asserting that digest equals `config_sha256(config)`;
4. hashes the protected source fixtures used by those launchers;
5. runs the selected-revision scale-cocycle experiment into the external temporary output root;
6. decodes its seven registered semantic JSON artifacts, removes only run-path/publication metadata, and hashes canonical semantic JSON; and
7. records each complete serialized `MetricRecord`, including value, tolerance, status, interpretation, assessment scope, theorem status, verification state, and claim origin.

Freeze this complete launcher list:

```python
_BASELINE_LAUNCHERS = (
    "run_attention_lab.py",
    "run_categorical_dqm_lab.py",
    "run_categorical_falsification_lab.py",
    "run_finite_counterexample_lab.py",
    "run_finite_lab.py",
    "run_gauge_holonomy_lab.py",
    "run_gaussian_fixed_ray_lab.py",
    "run_gaussian_lab.py",
    "run_information_history_lab.py",
    "run_multiagent_network_lab.py",
    "run_scale_cocycle_lab.py",
    "run_theory_oracle_lab.py",
)
```

The frozen JSON contains `schema_version`, `baseline_commit`, an ordered mapping from all twelve launcher names to their canonical config JSON and SHA-256, ordered source-fixture hashes, canonical hashes of every registered scale-cocycle semantic artifact, and complete serialized scale-cocycle metric records. Create it by explicitly invoking the isolated capture controller against the verified detached worktree under `RG_V2_REFRESH_LEGACY_BASELINE=1`; normal tests must never write repository files. Remove the environment variable and verify the normal regression path compares current protected launcher configs, source-fixture hashes, v1 semantic artifact hashes, and complete metrics with the frozen manifest. The current-revision side of that comparison must run through the same fresh-subprocess protocol: `cwd` at the current revision root, empty inherited `PYTHONPATH`, current `<root>/src` at `sys.path[0]`, current root at `sys.path[1]`, fresh project-facing `sys.modules`, external temporary output, and one JSON result on stdout. For protected files other than the additive `config.py` and `experiment_support.py` seams, also verify the current Git blob equals the baseline worktree blob. This generation is the sole source of values; do not hardcode an unverified existing hash.

Add tests that `pyproject.toml` matches its baseline Git blob, setuptools still discovers only under `src`, `src/multiagent_elbo/rg_v2` is absent, and no installed-package source imports `rg_v2`.

Write `README.md` with the CPU command, repository-local/non-installed status, one-way dependency, fixture IDs, six artifacts, and `AggregateDatum` endpoint. Keep `__init__.py` minimal:

```python
"""Repository-local local-first renormalization laboratory."""

RELEASE_ID = "renormalization-v2-release-1"

__all__ = ["RELEASE_ID"]
```

Do not run tests yet.

## Task 2: Implement exact semantic contracts

**Create:** `rg_v2/contracts.py`, `tests/rg_v2/test_contracts.py`

Write tests that pin `dataclasses.fields` and signatures before production code. Implement these exact semantic fields:

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
    belief_labels: tuple[str, ...]
    model_labels: tuple[str, ...]
    state_labels: tuple[str, ...]
    joint: ExactProbabilityLaw
    belief_marginal: ExactProbabilityLaw
    model_marginal: ExactProbabilityLaw

    def __init__(self, agent: AgentDatum, joint: ExactProbabilityLaw) -> None:
        belief = _marginalize_local_law(agent, joint, axis="belief")
        model = _marginalize_local_law(agent, joint, axis="model")
        object.__setattr__(self, "agent_id", agent.agent_id)
        object.__setattr__(self, "belief_labels", agent.belief_labels)
        object.__setattr__(self, "model_labels", agent.model_labels)
        object.__setattr__(self, "state_labels", agent.state_labels)
        object.__setattr__(self, "joint", joint)
        object.__setattr__(self, "belief_marginal", belief)
        object.__setattr__(self, "model_marginal", model)


@dataclass(frozen=True)
class RecordDatum:
    record_id: str
    owner_id: str
    scope_ids: tuple[str, ...]
    outcome_labels: tuple[str, ...]
    kernel: ExactMarkovChannel


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
    recognitions: tuple[AgentRecognitionDatum, ...]
    selector: SelectorSpec
    recognition: ExactProbabilityLaw
    evidence_measure: ExactSubmeasure
    evidence: Fraction
    posterior: ExactProbabilityLaw

    @property
    def selector_id(self) -> str:
        return self.selector.selector_id


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

`CoarseChannelSpec` has no aggregate ID. `AggregateDatum` has no channel or evidence-submeasure field. Recognition retains local support metadata; inference retains the local recognitions and full selector for replay; aggregate retains the canonical observed assignment for evidence replay.

Use compact canonical JSON strings for local `[belief, model]` labels and ordered parent/scope/latent/observation assignments. Validation requires unique nonempty labels, exact nonnegative `Fraction` masses, exact probability normalization, belief-major state-label enumeration, root source `("()",)`, canonical parent source support, evaluator completeness, exact positive-slice compatibility between `G_i` and evaluator rows, derived recognition marginals, owner-in-scope, selector coupling rules, and recognition-independent coarse channels.

Tests reject caller-supplied marginals, incompatible evaluator slices, malformed supports, a coarse channel with `aggregate_id`, and any `CoarseAgentDatum`, agent conversion, evaluator, observation interface, or update rule on `AggregateDatum`. Do not run tests yet.

## Task 3: Add strict primitive fixtures

**Create:** `rg_v2/fixtures.py`, three `rg_v2/data/lf3_*.json` fixtures, `tests/rg_v2/test_fixtures.py`

Expose the approved loader:

```python
FixtureName = Literal[
    "lf3_product_v1",
    "lf3_correlated_v1",
    "lf3_dirac_boundary_v1",
]


def load_fixture(fixture: FixtureName) -> LocalFirstFixture:
    path = Path(__file__).with_name("data") / f"{fixture}.json"
    raw = path.read_bytes()
    payload = _require_object(json.loads(raw.decode("utf-8")), "fixture")
    _require_exact_keys(payload, _TOP_LEVEL_KEYS, "fixture")
    return _build_fixture(fixture, path, hashlib.sha256(raw).hexdigest(), payload)
```

`LocalFirstFixture` is immutable and carries fixture ID/path/hash, context ID, agents, local recognitions, records, observation tuple, selector, and coarse-channel declaration. It carries no derived population or inference law.

Represent rationals as reduced `{numerator, denominator}` objects with positive denominator. Reject strings, floats, booleans, unknown/missing keys, and supplied recognition marginals. Construct `AgentRecognitionDatum(agent, joint)` in the loader.

The product and correlated fixtures share these local data:

- agents `a,b,c`, with parents `(),(a,),(b,)`;
- binary belief/model labels and four belief-major combined states per agent;
- root `G_a=(3/8,1/8,1/8,3/8)`;
- each child has canonical rows `(3/5,3/20,3/20,1/10)`, `(1/5,9/20,1/20,3/10)`, `(3/10,1/20,9/20,1/5)`, `(1/10,3/20,3/20,3/5)`;
- root evaluator rows `(3/4,1/4)` for `m0` and `(1/4,3/4)` for `m1`;
- child evaluator rows `(4/5,1/5)` and `(3/5,2/5)` for parent belief `b0`, then `(2/5,3/5)` and `(1/5,4/5)` for parent belief `b1`, ordered by model label;
- uniform local recognition on four states, giving non-Dirac model marginals `(1/2,1/2)`;
- records `r_a,r_b,r_c`, each owned by and scoped to its matching agent, outcomes `(0,1)`, row `(4/5,1/5)` on `b0` and `(1/5,4/5)` on `b1`, independent of model;
- observation `((r_a,1),(r_b,1),(r_c,1))`;
- belief-parity coarse declaration over `(a,b,c)` with targets `(even,odd)` and a nonempty structural input ID.

The product selector has no coupling. The declared-correlated selector contains the full 64-label table: mass `1/32` on every even-belief-parity latent assignment and zero on odd parity. Its local combined-state marginals equal the uniform locals and its exact TV distance from product is `1/2`.

The boundary fixture has the same ordering but singleton belief/model/state/evaluator/mechanism/record/recognition/observation/coarse supports and a product selector. Tests recursively reject prohibited derived keys, verify all exact rows and supports, compare decoded shared local data rather than raw bytes, and check the correlated marginals and non-Dirac counts. Do not run tests yet.

## Task 4: Construct the complete population joint and independent oracles

**Create:** `rg_v2/population.py`, `tests/rg_v2/test_population.py`

Implement the exact public signature:

```python
def construct_population_joint(
    agents: tuple[AgentDatum, ...],
    records: tuple[RecordDatum, ...],
    context_id: str,
) -> PopulationJoint:
    agent_order = _validate_agent_dag(agents)
    _validate_record_ownership(records, agents)
    latent_labels = _canonical_latent_labels(agents)
    observation_labels = _canonical_observation_labels(records)
    masses = _multiply_each_factor_once(
        agents, records, latent_labels, observation_labels
    )
    if _sum_matrix(masses) != Fraction(1):
        raise ArithmeticError("constructed population joint is not normalized")
    trace = tuple(f"agent:{item}" for item in agent_order) + tuple(
        f"record:{item.record_id}" for item in records
    )
    return PopulationJoint(
        context_id=context_id,
        agent_order=agent_order,
        record_order=tuple(item.record_id for item in records),
        latent_labels=latent_labels,
        observation_labels=observation_labels,
        joint_masses=masses,
        construction_trace=trace,
    )
```

Validate all DAG/support/evaluator/record invariants before multiplying. Attach each normalized agent mechanism in topological order and each supplied owned record kernel exactly once. The function never sees recognition, selector, observation value, evidence, or posterior.

Also implement `enumerate_population_joint_independently(agents, records, context_id) -> PopulationJoint` in `rg_v2/population.py`. This runtime oracle is separately coded: it builds supports from the dataclass fields, decodes assignments, indexes channel rows, and multiplies factors through its own loops. It must not call `construct_population_joint` or reuse constructor-private validation, support-enumeration, row-indexing, multiplication, trace, or normalization helpers. The experiment calls both implementations, computes an exact entrywise maximum residual, and writes the independently enumerated masses, trace comparison, and residual into `population_joint.json`; this supplies `independent_population_residual` at runtime rather than only in tests.

Write a third, separately coded test-only oracle that enumerates all 64 latent and 8 observation assignments, indexes frozen rows directly, and imports no production enumeration helper. Compare the full exact table from the constructor, the runtime oracle, and the test-only oracle pairwise. Also assert the first canonical latent state at observation `("1","1","1")` has mass `27/25000`; this value does not belong to `000`. Assert exact normalization, exact six-item trace, identical `P` for product/correlated fixtures, and signature parameters `agents, records, context_id`. Mutation tests cover duplicate record IDs, bad ownership/scope, reversed DAG order, and evaluator-incompatible `G_i`. A valid call that omits one record constructs a smaller normalized observation space and a shorter trace; it is not rejected as intrinsically invalid, but it must fail comparison with the fixture's complete runtime and test-only oracles and expected construction trace. Do not run tests yet.

## Task 5: Select recognition and derive posterior data

**Modify:** `rg_v2/population.py`, `tests/rg_v2/test_population.py`

Implement the approved public seam:

```python
def derive_population_inference(
    population: PopulationJoint,
    observations: tuple[tuple[str, str], ...],
    recognitions: tuple[AgentRecognitionDatum, ...],
    selector: SelectorSpec,
) -> PopulationInference:
    recognition = _select_recognition(recognitions, selector)
    observed_record = _canonical_observed_record(population, observations)
    column = population.observation_labels.index(observed_record)
    evidence_measure = ExactSubmeasure(
        population.latent_labels,
        tuple(row[column] for row in population.joint_masses),
    )
    evidence = sum(evidence_measure.masses, Fraction(0))
    if evidence <= 0:
        raise ValueError("posterior requires positive evidence")
    posterior = ExactProbabilityLaw(
        population.latent_labels,
        tuple(value / evidence for value in evidence_measure.masses),
    )
    return PopulationInference(
        population=population,
        observed_record=observed_record,
        recognitions=recognitions,
        selector=selector,
        recognition=recognition,
        evidence_measure=evidence_measure,
        evidence=evidence,
        posterior=posterior,
    )
```

Keep the selector narrowed:

```python
def _select_recognition(
    recognitions: tuple[AgentRecognitionDatum, ...],
    selector: SelectorSpec,
) -> ExactProbabilityLaw:
```

Product selection forms the canonical tensor product. Correlated selection validates exact support order and every local combined-state marginal against stored recognition metadata. It never receives or reads `PopulationJoint`. Observation input must name every record exactly once and is reordered by `record_order` into the canonical string stored as `observed_record`.

Tests prove local marginal equality, exact product/correlated TV `1/2`, unique singleton coupling, independent evidence/posterior derivation, fixed-joint independence under recognition/observation changes, complete inference-field retention for replay, and the exact selector/public signatures. Instrument `_select_recognition` to prove it receives only two allowed arguments. Do not run tests yet.

## Task 6: Push through one common channel and compute VFE

**Create:** `rg_v2/coarse.py`, `tests/rg_v2/test_coarse.py`

Use the amended signatures:

```python
def aggregate_population(
    inference: PopulationInference,
    channel: CoarseChannelSpec,
    numerics: NumericsConfig,
) -> AggregateDatum:


def validate_aggregate_datum(
    datum: AggregateDatum,
    inference: PopulationInference,
    channel: CoarseChannelSpec,
    numerics: NumericsConfig,
) -> None:
```

Validate types, source labels, source-agent ordering, recognition independence, structural input IDs, float64 numerics, and `numerics.atol <= 1e-12`. Bind `exact_channel = channel.channel` once and pass that same reference to: complete-joint push with identity on observation; recognition push; and posterior push. Record the three object IDs internally and require one unique identity before returning. This check is execution-only.

Persist a canonical SHA-256 over channel ID-independent structural content: ordered source/target labels, exact numerator/denominator matrix, and recognition-independence flag. Persist channel ID/hash and `observed_record`; never persist Python identity or the channel object. Coarse evidence is the sum of the coarse complete joint at the stored observation and must equal fine evidence exactly.

Define the aggregate identity with no ambient inputs:

```python
def _aggregate_id(
    inference: PopulationInference,
    channel: CoarseChannelSpec,
    channel_sha256: str,
) -> str:
    identity = {
        "context_id": inference.population.context_id,
        "source_agent_ids": list(channel.source_agent_ids),
        "observed_record": inference.observed_record,
        "channel_id": channel.channel_id,
        "channel_sha256": channel_sha256,
    }
    canonical = json.dumps(
        identity,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return "aggregate-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
```

The VFE adapter must be exactly:

```python
def _vfe_diagnostics(
    inference: PopulationInference,
    channel: ExactMarkovChannel,
    numerics: NumericsConfig,
) -> tuple[float, float]:
    fine_p_v = ProbabilityMeasure(
        inference.population.latent_labels,
        [float(sum(row, Fraction(0))) for row in inference.population.joint_masses],
        numerics,
    )
    fine_evidence = FiniteMeasure(
        inference.evidence_measure.labels,
        [float(value) for value in inference.evidence_measure.masses],
        numerics,
    )
    fine_q = ProbabilityMeasure(
        inference.recognition.labels,
        [float(value) for value in inference.recognition.masses],
        numerics,
    )
    float_channel = MarkovKernel(
        channel.source_labels,
        channel.target_labels,
        [[float(value) for value in row] for row in channel.matrix],
        numerics,
    )
    result = vfe_channel_decomposition(
        fine_q,
        MeasurePair(reference=fine_p_v, evidence_measure=fine_evidence),
        float_channel,
    )
    if result.residual is None or result.offending_state is not None:
        raise ValueError("finite VFE decomposition is undefined on this fixture")
    return result.conditional_kl, abs(result.residual)
```

No hidden numerics constant is permitted. Call `validate_aggregate_datum(datum, inference, channel, numerics)` before return. Validation recomputes the canonical hash and aggregate ID, observation identity, exact pushes/evidence, normalizations, conditional defect lower bound `-min(numerics.atol, 1e-12)`, chain-residual upper bound `min(numerics.atol, 1e-12)`, and finite floats. Replay validates channel ID/hash and mathematics; it cannot reproduce Python object identity.

Tests instrument three push seams to assert identical object ID, then test source mismatch, observation-dependent declaration, recognition-dependent channel, split-channel mutation, hash mismatch, nondeterministic aggregate-ID inputs, and `numerics.atol > 1e-12`. Assert exact evidence, observed-record retention, normalized laws, defect/residual bounds at `min(numerics.atol, 1e-12)`, canonical aggregate/hash stability, and exact aggregate field order. Do not run tests yet.

## Task 7: Add config, registry, experiment publication, and launcher

**Create:** `rg_v2/experiment.py`, `run_renormalization_v2_lab.py`, `tests/rg_v2/test_experiment.py`

**Modify:** `src/multiagent_elbo/config.py`, `src/multiagent_elbo/experiment_support.py`, `tests/test_config.py`, `tests/test_experiment_support.py`

After the v1 freeze exists, add:

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

Append it to `ExperimentTheoryConfig`, append `renormalization_v2` to `NEW_EXPERIMENT_NAMES` without reordering old names, and add a strict three-key resolver. Existing canonical launcher configs must remain byte-identical.

Add exactly this registry entry:

```python
"renormalization_v2": ExperimentContract(
    experiment="renormalization_v2",
    lane_owner="rg_v2_release_1",
    launcher="run_renormalization_v2_lab.py",
    config_keys=("experiment", "fixture", "arithmetic"),
    artifact_inventory=(
        "fixture_snapshot",
        "population_joint",
        "population_inference",
        "aggregate_datum",
        "metrics",
        "arrays",
    ),
    metric_inventory=(
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
    ),
),
```

Implement:

```python
def run_renormalization_v2_experiment(
    config: ExperimentConfig,
) -> RenormalizationV2ExperimentResult:
```

Validate experiment/arithmetic, CPU float64, `config.numerics.atol <= 1e-12`, output flags, and primitive fixture before RNG or filesystem effects. Construct the scientific bodies, including both population implementations, all inference/aggregate laws, the thirteen metrics, and the six artifact-specific bodies. Then create `RngStreams` and collect provenance entirely in memory. Use the resulting producer commit and config hash to finalize each artifact envelope and compute canonical hashes in dependency order: `fixture_snapshot` first; `population_joint` from the finalized fixture hash; `population_inference` from finalized fixture/population hashes; `aggregate_datum` from finalized fixture/inference hashes and channel hash; `metrics` from the four finalized semantic hashes; and `arrays` from those hashes plus the finalized metrics hash. Freeze every envelope and NPZ metadata mapping after its direct-input hashes are final. Only then call `RunStore.create`, write exactly five JSON artifacts and one NPZ, and finalize exactly those six filenames. No filesystem write may occur before the complete artifact DAG and all direct-input hashes are final. No RunStore/library edit is allowed.

Every JSON carries schema version, fixture ID, producer commit, config hash, and ordered direct-input hashes. `fixture_snapshot` includes full exact primitives as well as hashes so replay needs no fixture file. `arrays.npz` contains float64 mirrors; scalar fixed-width Unicode arrays named `schema_version`, `fixture_id`, `producer_commit`, and `config_hash`; and ordered fixed-width Unicode arrays `direct_input_names` and `direct_input_sha256`. Load it only with `allow_pickle=False`; no object arrays are permitted. All `MetricRecord`s use `assessment_scope="implementation_check"`, explicit theorem status, `verification_state="CANDIDATE"`, and explicit claim origin. The Dirac fixture targets zero non-Dirac model marginals; the other fixtures target at least one. Exact residuals target zero, conditional KL permits `-min(config.numerics.atol, 1e-12)`, and chain residual uses `min(config.numerics.atol, 1e-12)`.

The root launcher is click-to-run and inserts only source:

```python
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from multiagent_elbo.config import ExperimentConfig  # noqa: E402
from rg_v2.experiment import run_renormalization_v2_experiment  # noqa: E402


RUN = {"name": "renormalization-v2", "seed": 20260821}
THEORY = {
    "experiment": "renormalization_v2",
    "fixture": "lf3_product_v1",
    "arithmetic": "exact_rational",
}
NUMERICS = {
    "dtype": "float64",
    "atol": 1e-12,
    "rtol": 1e-10,
    "min_spd_rcond": 1e-12,
    "max_frame_condition": 1.0e6,
}
OUTPUT = {
    "root": "artifacts",
    "collect_diagnostics": True,
    "render_figures": False,
}


def main() -> object:
    config = ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT)
    result = run_renormalization_v2_experiment(config)
    print(f"run_dir={result.run_dir}")
    print(f"status={result.status}")
    return result


if __name__ == "__main__":
    main()
```

This inserts only `ROOT / "src"`; do not insert `ROOT` and do not edit `PYTHONPATH` in the launcher.

Parameterize the publication gate over exactly:

```python
_FIXTURE_IDS = (
    "lf3_product_v1",
    "lf3_correlated_v1",
    "lf3_dirac_boundary_v1",
)


@pytest.mark.parametrize("fixture_id", _FIXTURE_IDS)
def test_every_fixture_publishes_the_complete_release_contract(
    fixture_id: str,
    tmp_path: Path,
) -> None:
```

For each of those three and no implicit default-only shortcut, assert exact registry inventory, exactly eight finalized files including core artifacts, complete hash graph, all six NPZ provenance arrays under `allow_pickle=False`, runtime independent-enumeration residual zero and payload presence, pre-publication failure, explicit rejection of `collect_diagnostics=False/render_figures=True`, pre-effect rejection of looser `atol`, and mathematical result equality across output roots without byte comparison. Do not run tests yet.

## Task 8: Replay, packaging/import checks, focused and broader passes, and commit

**Modify:** `tests/rg_v2/test_experiment.py`, `tests/rg_v2/test_legacy_regression.py`

**Create or update:** `docs/change-logs/2026-08-21.md`

Add a test-only replay that reads only finalized artifacts, never `load_fixture`. Rebuild exact laws from numerator/denominator records; reconstruct local recognitions/selectors from `fixture_snapshot`; validate aggregate with stored inference, reconstructed channel, and resolved config numerics; recompute the canonical channel hash, aggregate ID, independent-population residual, and the other eleven reproducible mathematical/structural metrics; and compare them to `metrics.json`. For `common_channel_identity_violation_count`, replay validates that the stored metric schema/value is exactly the declared zero record and that one channel declaration/hash governs all persisted pushes. It explicitly does not claim to replay Python object identity, which remains covered by the in-process Task 6 test. Load NPZ with `allow_pickle=False`, verify the four scalar identity arrays and two ordered direct-input hash arrays, and compare every float mirror.

Parameterize this fixture-free replay gate with `@pytest.mark.parametrize("fixture_id", _FIXTURE_IDS)` over exactly `lf3_product_v1`, `lf3_correlated_v1`, and `lf3_dirac_boundary_v1`. Each case first publishes its own finalized run, then replay receives only that run directory. The replay function must not import or call `load_fixture`, read `rg_v2/data`, or assume the product selector. The arbitrary-CWD launcher test remains intentionally scoped to the default product fixture.

Add that arbitrary-CWD launcher test:

```python
def test_absolute_launcher_runs_from_arbitrary_cwd_with_empty_pythonpath(
    tmp_path: Path,
) -> None:
    environment = dict(os.environ)
    environment["PYTHONPATH"] = ""
    completed = subprocess.run(
        [
            r"C:\Python314\python.exe",
            str(_REPO_ROOT / "run_renormalization_v2_lab.py"),
        ],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "status=pass" in completed.stdout
```

Inspect launcher AST/source and require its sole `sys.path.insert` value to be `SRC`. Scan `src/multiagent_elbo/**/*.py` for reverse imports. Build a wheel in a temporary output directory and inspect the ZIP: it contains `multiagent_elbo` and no top-level `rg_v2`. In an isolated subprocess, import from the unpacked wheel with repository root absent and assert `find_spec("rg_v2") is None`.

Against a fresh detached worktree at the baseline, rerun the Task 1 isolated capture controller and require exact equality with `legacy_rescaling_v1.json`. Run the current side through its own fresh subprocess rooted at the current revision, with empty inherited `PYTHONPATH` and current source/root path order, before comparing protected launcher canonical JSON/SHA values, source fixtures, semantic artifacts, and complete MetricRecords with the manifest. This is the post-shared-edit v1 gate.

After all edits, run the focused set:

```powershell
C:\Python314\python.exe -B -m pytest tests\rg_v2 tests\test_config.py tests\test_experiment_support.py -q -p no:cacheprovider --basetemp=.pytest-rg-v2-release1 --junitxml=.pytest-rg-v2-release1.xml
```

Repair any demonstrated defect and rerun the focused command until it passes. Then always run the broader CPU pass required by base Phase 5:

```powershell
C:\Python314\python.exe -B -m pytest tests -q -p no:cacheprovider --basetemp=.pytest-rg-v2-broad --junitxml=.pytest-rg-v2-broad.xml
```

Repair any demonstrated defect and rerun the affected focused tests plus the broader command until both final JUnit files report success. Do not make a CUDA claim.

Run static gates:

```powershell
git diff --check
rg -n "src[/\\]multiagent_elbo[/\\]rg_v2|from rg_v2|import rg_v2" src
rg -n "CoarseAgentDatum|MetaAgent|as_agent|universality|semigroup|continuum limit" rg_v2 run_renormalization_v2_lab.py
git status --short
```

The reverse-import scan returns no match. Forbidden-language matches may occur only in explicit README exclusions, never runtime claims or types.

Update the dated log with baseline, root-local boundary, changed files, three fixtures, six artifacts, thirteen metrics, focused and broader commands/JUnit results, wheel/import checks, v1 regression, and the `AggregateDatum` endpoint. State that new results remain `CANDIDATE`.

Stage only named files, inspect the staged diff, and commit once after both gates:

```powershell
git add -- rg_v2 run_renormalization_v2_lab.py src/multiagent_elbo/config.py src/multiagent_elbo/experiment_support.py tests/rg_v2 tests/test_config.py tests/test_experiment_support.py docs/change-logs/2026-08-21.md
git diff --cached --check
git commit -m "feat: add local-first renormalization v2 lab"
```

Do not push, merge, or synchronize another checkout without separate authorization. Preserve unrelated untracked files.

## Completion gate

Release 1 is complete only when the implementation revision demonstrates root-level non-installed placement; unchanged package/test/coverage metadata; subprocess-isolated baseline-worktree-frozen v1 config JSON/SHA values, source fixtures, semantics, and complete metrics; evaluator-compatible local mechanisms; non-Dirac model uncertainty; once-owned population construction equal across the constructor, separately coded runtime oracle, and third test-only oracle; product and declared-correlated recognition with exact local marginals; posterior derived from the constructed observation slice; one in-process common channel with replayable ID/hash; explicit bounded numerics in fine-law VFE; deterministic content-derived aggregate identity; exact evidence preservation; six replayable artifacts with finalized DAG hashes and NPZ provenance; twelve replayed mathematical/structural metrics plus the scoped identity record; publication and fixture-free replay gates for all three fixtures; thirteen candidate metrics; arbitrary-CWD default launcher execution with empty `PYTHONPATH`; wheel exclusion; successful focused and broader CPU JUnit passes; and no semantic type stronger than `AggregateDatum`.
