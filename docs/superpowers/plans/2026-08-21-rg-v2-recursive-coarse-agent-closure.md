# RG-v2 Recursive Coarse-Agent Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. Every production slice follows `superpowers:test-driven-development`; steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build one exact finite Phase 2 witness in which four fine agents are blocked into two recursively usable Release 1 `AgentDatum` objects, with a lossless observation relabeling, explicit information access, all-observation Bayesian update tables, and exact recognition/evidence/posterior roundtrips.

**Architecture:** Phase 2 is additive and repository-local under root `rg_v2/`. A strict primitive fixture constructs the fine population through unchanged Release 1 functions; `coarse_agent.py` applies two declared exact block channels, disintegrates the pushed generative law into two ordinary agent mechanisms plus one dense combined record, and separately constructs information/update and recognition interfaces. `recursive_experiment.py` publishes a distinct eight-artifact, twenty-metric run without modifying Release 1 science or promoting `AggregateDatum` into an agent.

**Tech Stack:** Python 3.14, frozen dataclasses, `fractions.Fraction`, exact `ExactMarkovChannel`, NumPy float64 mirrors, existing `ExperimentConfig`, `RunStore`, `MetricRecord`, provenance, and pytest on CPU.

**Spec:** `docs/superpowers/specs/2026-08-21-rg-v2-recursive-coarse-agent-closure-design.md`

## Global Constraints

- Work only in the existing isolated branch rooted at `d4ce80bc9eda90ec54dc9c97d8405d7d28ca6182`; preserve the live Desktop checkout and unrelated WIP.
- All new laboratory implementation lives at repository root under `rg_v2/`; never create `src/multiagent_elbo/rg_v2` or add a reverse import from `src/multiagent_elbo` to `rg_v2`.
- Release 1 is frozen: do not edit `rg_v2/contracts.py`, `rg_v2/population.py`, `rg_v2/coarse.py`, `rg_v2/fixtures.py`, `rg_v2/experiment.py`, its three LF3 fixtures, `run_renormalization_v2_lab.py`, `pyproject.toml`, `artifacts.py`, or `runtime.py`.
- Shared installed-package edits are additive only in `src/multiagent_elbo/config.py` and `src/multiagent_elbo/experiment_support.py`; every existing canonical config identity, registry record, launcher, artifact inventory, metric inventory, and scientific result remains unchanged.
- The only Phase 2 fixture is `lf4_two_parent_recursive_v1`; it uses exact rational arithmetic, deterministic CPU float64, `0 < numerics.atol <= 1e-12`, diagnostics enabled, and figures disabled.
- The flagship has exactly four fine agents, 256 fine latent states, 16 positive-evidence observations, 4,096 fine joint cells, two coarse agents, 16 coarse latent states, and 256 coarse joint cells. Larger inputs fail before RNG or filesystem effects.
- Generative construction receives only `PopulationJoint` and `RecursiveCoarseStructure`. Access/update construction receives only the completed coarse population and explicit access specifications. Recognition is attached only afterward from a fine `PopulationInference`.
- Keep the exact public type field order and five public function signatures in the approved specification. Do not add agent conversion, meta-agent, evolution, scale-composition, fixed-point, universality, or continuum interfaces.
- The dense combined record is the admitted exact fallback. The declared sparse two-record-family factorization must fail at least one exact identity and retain its exact maximum conditional total-variation magnitude as a diagnostic.
- Publish exactly eight semantic artifacts in this order: `fixture_snapshot`, `fine_population`, `coarse_generative`, `coarse_interfaces`, `coarse_population`, `all_observation_inference`, `metrics`, `arrays`.
- Emit exactly the approved twenty metric names in their approved order. Every record remains `verification_state="CANDIDATE"` with explicit assessment scope, theorem status, and claim origin.

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

- Compute and validate every scientific body, exact metric, finalized JSON envelope, hash dependency, and NPZ array in memory before the first `RunStore.create` call.
- Primitive JSON contains no constructed population, selected population recognition, evidence, posterior, combined channel, coarse mechanism, derived evaluator, combined record, expected metric, status, or pass flag.
- Use reduced `{ "numerator": n, "denominator": d }` rationals with positive denominators; canonical JSON uses sorted keys, compact separators, ASCII escaping, and disallows NaN.
- Every behavior test names a concrete production mutation it catches and derives expected values independently. Each production task records a failing RED test before adding its production implementation, then runs only its task-scoped GREEN tests. The consolidated Phase 2 focused JUnit runs once after all implementation edits, followed by one broader CPU JUnit pass.
- No CUDA result is claimed. Do not push, merge, or synchronize another checkout without a separate user request.

---

## File Map

```text
rg_v2/
    coarse_agent.py                 # Phase 2 types, construction, validation, and sparse diagnostics
    recursive_fixtures.py           # Strict LF4 primitive loader and subrecord hashes
    recursive_experiment.py         # Phase 2 science, metrics, artifacts, and RunStore publication
    data/
        lf4_two_parent_recursive_v1.json
    README.md                       # Add the Phase 2 click-to-run boundary and nonclaims
run_renormalization_v2_recursive_lab.py
src/multiagent_elbo/config.py       # Additive strict theory discriminator only
src/multiagent_elbo/experiment_support.py  # Additive registry record only
tests/rg_v2/
    test_coarse_agent.py
    test_recursive_fixtures.py
    test_recursive_experiment.py
tests/test_config.py
tests/test_experiment_support.py
docs/change-logs/2026-08-21.md
```

## Task 1: Add exact recursive semantic contracts and structural validation

**Files:**
- Create: `rg_v2/coarse_agent.py`
- Create: `tests/rg_v2/test_coarse_agent.py`

**Interfaces:**
- Consumes: unchanged `AgentDatum`, `AgentRecognitionDatum`, `CoarseChannelSpec`, `ExactProbabilityLaw`, `PopulationInference`, `PopulationJoint`, `RecordDatum`, `SelectorSpec`, `ExactMarkovChannel`, and `NumericsConfig`.
- Produces: the thirteen frozen Phase 2 dataclasses from the spec, canonical structural validators, exact channel hashing, and canonical support helpers used by Tasks 2–4.

- [ ] **Step 1: Write contract tests that name the break**

Add field-order assertions for every approved dataclass, frozen-mutation rejection, and behavior tests for canonical state labels, nonempty/disjoint/exhaustive blocks, topological coarse order, block-channel source/target supports, the fine-to-compound observation bijection, sparse record projections, and identity access declarations. Use literal expected field tuples, for example:

```python
def test_recursive_structure_field_order_is_stable() -> None:
    assert tuple(field.name for field in fields(RecursiveCoarseStructure)) == (
        "structure_id",
        "source_agent_order",
        "coarse_agent_order",
        "agent_specs",
        "observation",
        "sparse_record_candidate",
    )


@pytest.mark.parametrize(
    "mutation, message",
    (
        ("duplicate_source", "source blocks must be disjoint and exhaustive"),
        ("reversed_parent", "coarse agents must be topologically ordered"),
        ("noncanonical_state", "state labels must be the belief-major canonical Cartesian product"),
        ("wrong_channel_target", "block channel target labels must equal state labels"),
        ("nonbijective_observation", "observation map must be an ordered bijection"),
        ("incomplete_sparse_projection", "sparse projections must cover every fine observation"),
    ),
)
def test_recursive_contracts_reject_structural_mutations(
    mutation: str,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        build_mutated_contract(mutation)
```

The helper `build_mutated_contract` is test-only and constructs each complete malformed object with real `ExactMarkovChannel` values; it must not mock constructors or assert on source text.

- [ ] **Step 2: Run RED and verify the failure is the missing module**

Run:

```powershell
$env:CUDA_VISIBLE_DEVICES = "-1"
$env:PYTHONHASHSEED = "0"
C:\Python314\python.exe -B -m pytest tests\rg_v2\test_coarse_agent.py -k "field_order or structural_mutations" -q -p no:cacheprovider
```

Expected: collection fails because `rg_v2.coarse_agent` does not exist. A syntax or fixture error is not an accepted RED.

- [ ] **Step 3: Implement the frozen dataclasses exactly**

Define the fields in this order and with these types:

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

Implement `__post_init__` checks on owned fields and reusable private validation functions. Canonical local state labels are compact ASCII JSON in belief-major order. Canonical agent assignments preserve declared tuple order. SHA-256 helpers hash only canonical semantic declarations, never Python identity or filesystem paths.

- [ ] **Step 4: Run GREEN and the mutation check**

Run the same task-scoped command without `-k`. Confirm every test passes, then mentally mutate each validator: duplicate one block member, swap one state label, duplicate one compound outcome, omit one sparse projection, and replace one target support. At least one named test must fail for each mutation.

- [ ] **Step 5: Inspect and commit Task 1**

Run `git diff --check`, stage only the two Task 1 files, inspect the cached diff, and commit:

```powershell
git commit -m "feat: add recursive coarse-agent contracts"
```

## Task 2: Add the strict LF4 primitive fixture and loader

**Files:**
- Create: `rg_v2/recursive_fixtures.py`
- Create: `rg_v2/data/lf4_two_parent_recursive_v1.json`
- Create: `tests/rg_v2/test_recursive_fixtures.py`

**Interfaces:**
- Consumes: Task 1 contracts and unchanged Release 1 primitive types.
- Produces: `RecursiveFixture`, `RecursiveFixtureName`, `load_recursive_fixture`, raw SHA-256, and ordered canonical subrecord hashes for generative, recognition, structure, and access inputs.

- [ ] **Step 1: Write loader tests before the loader**

Pin a closed top-level schema containing exactly `schema_version`, `fixture_id`, `context_id`, `agents`, `recognitions`, `records`, `selector`, `observation`, `recursive_structure`, and `access_specs`. Tests must assert:

```python
def test_flagship_fixture_is_primitive_positive_and_exact() -> None:
    fixture = load_recursive_fixture("lf4_two_parent_recursive_v1")
    assert tuple(agent.agent_id for agent in fixture.agents) == (
        "a0", "a1", "a2", "a3"
    )
    assert tuple(record.record_id for record in fixture.records) == (
        "r0", "r1", "r2", "r3"
    )
    assert fixture.structure.source_agent_order == (
        "a0", "a1", "a2", "a3"
    )
    assert fixture.structure.coarse_agent_order == ("A", "B")
    assert len(fixture.structure.observation.fine_observation_labels) == 16
    assert fixture.observation == (
        ("r0", "1"), ("r1", "1"), ("r2", "1"), ("r3", "1")
    )
    assert tuple(name for name, _ in fixture.subrecord_sha256) == (
        "generative", "recognition", "structure", "access"
    )


def test_declared_fine_coupling_is_correlated_with_uniform_local_marginals() -> None:
    fixture = load_recursive_fixture("lf4_two_parent_recursive_v1")
    coupling = fixture.selector.coupling
    assert coupling is not None
    assert coupling.masses.count(Fraction(1, 128)) == 128
    assert coupling.masses.count(Fraction(0)) == 128
    assert all(
        recognition.joint.masses == (Fraction(1, 4),) * 4
        for recognition in fixture.recognitions
    )
```

Add recursive rejection tests that insert one forbidden derived key at each nesting level, mutate a rational denominator to zero, change one agent/evaluator row, remove one record source row, break the block partition, reorder the observation bijection, change an access label, or replace the exact fixture name. Assert the real loader error, not a mock call.

- [ ] **Step 2: Run RED and verify the missing loader**

Run:

```powershell
C:\Python314\python.exe -B -m pytest tests\rg_v2\test_recursive_fixtures.py -q -p no:cacheprovider
```

Expected: collection fails because `rg_v2.recursive_fixtures` is missing.

- [ ] **Step 3: Author the self-contained primitive JSON**

Use the existing LF3 root row for `a0` and the existing LF3 positive child rows and evaluator rows for `a1`, `a2`, and `a3`, with the declared chain `a0 -> a1 -> a2 -> a3`. Rename IDs only; preserve the exact rational tables. All agents use `("b0", "b1")`, `("m0", "m1")`, and the canonical four-state support.

Define four positive binary records:

```text
r0: owner a0, scope (a0); reuse LF3 belief-conditioned 4/5 versus 1/5 rows.
r1: owner a1, scope (a1,a2); P(0)=4/5 when the two belief labels agree, else 1/5.
r2: owner a2, scope (a1,a2); use the same equality-sensitive rows as r1.
r3: owner a3, scope (a3); reuse LF3 belief-conditioned 4/5 versus 1/5 rows.
```

Materialize four uniform local recognition laws. Materialize the declared-correlated fine selector in canonical 256-state order: assign `1/128` exactly when the XOR of the four belief bits is zero and `0` otherwise. This gives uniform local marginals while retaining genuine coarse belief correlation.

Declare blocks `A=(a0,a1)` and `B=(a2,a3)`. Each `16 x 4` deterministic block channel maps its two fine states to canonical coarse `(belief parity, model parity)` labels `("B0","B1") x ("M0","M1")`. Do not serialize the derived `256 x 16` product channel.

Declare `r_AB` compound outcomes `o0000` through `o1111` in canonical fine-observation order. Map each fine observation label to the corresponding outcome exactly once. Declare sparse left records `(r0,r1)`, right records `(r2,r3)`, four two-bit outcome supports, and the complete left/right projections for all sixteen fine observations. Declare identity access for both parents over the sixteen reconstructed one-record observation labels.

- [ ] **Step 4: Implement strict decoding and subrecord hashing**

Define:

```python
RecursiveFixtureName = Literal["lf4_two_parent_recursive_v1"]


@dataclass(frozen=True)
class RecursiveFixture:
    fixture_id: str
    fixture_path: Path
    fixture_sha256: str
    subrecord_sha256: tuple[tuple[str, str], ...]
    context_id: str
    agents: tuple[AgentDatum, ...]
    recognitions: tuple[AgentRecognitionDatum, ...]
    records: tuple[RecordDatum, ...]
    observation: tuple[tuple[str, str], ...]
    selector: SelectorSpec
    structure: RecursiveCoarseStructure
    access_specs: tuple[CoarseAccessSpec, ...]


def load_recursive_fixture(
    fixture: RecursiveFixtureName,
) -> RecursiveFixture:
    fixture_path = Path(__file__).resolve().parent / "data" / f"{fixture}.json"
    raw = fixture_path.read_bytes()
    payload = json.loads(raw)
    return _decode_recursive_fixture(payload, fixture_path, sha256(raw).hexdigest())
```

Validate the fixture name before any file read. Reject derived keys recursively. Hash the raw file separately, then hash the four canonical JSON subrecords in the fixed order. Do not reread the file after typed construction.

- [ ] **Step 5: Run GREEN, inspect, and commit Task 2**

Run the full Task 2 test file. Confirm the malformed and byte-mutation cases fail through the public loader. Run `git diff --check`, stage only the loader, fixture, and test, and commit:

```powershell
git commit -m "feat: add recursive LF4 primitive fixture"
```

## Task 3: Construct the coarse generative population and independent oracles

**Files:**
- Modify: `rg_v2/coarse_agent.py`
- Modify: `tests/rg_v2/test_coarse_agent.py`

**Interfaces:**
- Consumes: `PopulationJoint` and `RecursiveCoarseStructure` only at the public generative seam.
- Produces: `construct_coarse_population_joint`, a separately coded private runtime enumerator used by the experiment, exact sparse-factorization diagnostics, two ordinary `AgentDatum` parents, one combined `RecordDatum`, `PushedCoarseJoint`, and reconstructed `PopulationJoint`.

- [ ] **Step 1: Add RED tests for the complete generative arrow**

Construct the fine population through unchanged `construct_population_joint`. Compare all cells against unchanged `enumerate_population_joint_independently` and a third test-only literal-loop oracle that uses hardcoded LF3 rational tables, record predicates, parity maps, and no fixture or production helper.

Add tests that call the not-yet-implemented public function and assert:

```python
coarse = construct_coarse_population_joint(fine_population, fixture.structure)
assert coarse.reconstructed_population.agent_order == ("A", "B")
assert coarse.reconstructed_population.record_order == ("r_AB",)
assert len(coarse.pushed_joint.joint_masses) == 16
assert all(len(row) == 16 for row in coarse.pushed_joint.joint_masses)
assert relabel_reconstructed_rows(coarse) == coarse.pushed_joint.joint_masses
assert tuple(item.agent.agent_id for item in coarse.generative_agents) == ("A", "B")
assert coarse.records[0].owner_id == "B"
assert coarse.records[0].scope_ids == ("A", "B")
```

Monkeypatch every constructor helper to raise and prove the separately coded runtime enumerator still reproduces all 256 coarse cells. Add mutations for block partition, channel source/target, factor order, positive evaluator row, compound bijection, and combined record. Pass an `AggregateDatum` to the generative seam and require an error naming the missing structural, generative, observation, recognition, and update obligations. Inspect the public signature and require that no inference, recognition, selector, observation, posterior, numerics, or aggregate parameter exists.

- [ ] **Step 2: Run RED and verify the missing function**

Run only the new generative tests. Expected: import or attribute failure for `construct_coarse_population_joint`, not an oracle/setup failure.

- [ ] **Step 3: Implement the exact combined channel and push**

Build each block-source label by restricting a canonical fine latent assignment to the block's declared source IDs. The combined channel source labels equal `population.latent_labels`; its target labels are the canonical two-parent assignment labels in `(A,B)` order. Each row is the exact product

```python
combined_mass = (
    spec_a.block_channel.matrix[source_a][target_a]
    * spec_b.block_channel.matrix[source_b][target_b]
)
```

Push the complete joint observation-column by observation-column with exact `Fraction` accumulation. Retain fine observation labels in `PushedCoarseJoint`, hash the canonical combined channel declaration, and reject any normalization or support mismatch before disintegration.

- [ ] **Step 4: Disintegrate into two Release 1 agents and one record**

Compute `G_A(z_A)=P^c_Z(z_A)` and `G_B(z_B|z_A)=P^c_Z(z_A,z_B)/P^c_Z(z_A)`. Under `null_row_policy="forbid"`, reject every zero denominator. Derive each evaluator by conditioning every positive model slice of the corresponding generative row; do not copy a fine evaluator.

Build the combined record with source support equal to canonical `(A,B)` assignments and outcome support from `CoarseObservationSpec`. Its row is

```python
record_mass = pushed_joint.joint_masses[latent_index][fine_observation_index]
record_row[outcome_index] = record_mass / pushed_latent_mass
```

Create the ordinary parent `AgentDatum` objects and combined `RecordDatum`, then call unchanged `construct_population_joint`. Relabel the reconstructed one-record observations through the explicit bijection and require exact cellwise equality with `PushedCoarseJoint`.

- [ ] **Step 5: Implement the independent runtime oracle and sparse diagnostics**

The private runtime oracle must duplicate support parsing, block-channel row lookup, channel products, exact push, disintegration, evaluator derivation, record construction, normalization, and relabeling using only public fields. It must not call the production constructor or any of its private helpers.

For the declared sparse candidate, compute the exact conditional joint over `(o_L,o_R)` for every `(z_A,z_B)`, its left and right marginals, every marginal-invariance identity, and the product residual. Count every failed unordered pairwise left-marginal invariance comparison, every failed unordered pairwise right-marginal invariance comparison, and every failed product cell. Return `(violation_count, maximum_conditional_tv)` from a private helper. The flagship literal oracle fixes `violation_count == 448` and `maximum_conditional_tv == Fraction(47889, 245000)`: 96 left comparisons, 96 right comparisons, and all 256 product cells fail. The dense reconstruction remains exact.

- [ ] **Step 6: Run GREEN, inspect, and commit Task 3**

Run the complete `test_coarse_agent.py` file. Confirm the constructor, runtime oracle, and test-only oracle compare all 4,096 fine and 256 coarse cells. Run `git diff --check`, stage the two Task 3 files, and commit:

```powershell
git commit -m "feat: construct recursive coarse generative data"
```

## Task 4: Add information access, recognition, all-observation inference, and validation

**Files:**
- Modify: `rg_v2/coarse_agent.py`
- Modify: `tests/rg_v2/test_coarse_agent.py`

**Interfaces:**
- Consumes: completed `CoarsePopulationDatum`, explicit `CoarseAccessSpec` values, one fine `PopulationInference`, and supplied `NumericsConfig` only at validation.
- Produces: the remaining four public functions: `construct_coarse_information_interfaces`, `construct_coarse_recognition`, `derive_recursive_observation`, and `validate_recursive_observation`.

- [ ] **Step 1: Add RED tests for separated information and recognition paths**

Pin these signatures exactly:

```python
def construct_coarse_information_interfaces(
    coarse_population: CoarsePopulationDatum,
    access_specs: tuple[CoarseAccessSpec, ...],
) -> tuple[CoarseInformationDatum, ...]:


def construct_coarse_recognition(
    coarse_population: CoarsePopulationDatum,
    information: tuple[CoarseInformationDatum, ...],
    fine_inference: PopulationInference,
) -> tuple[CoarseAgentDatum, ...]:


def derive_recursive_observation(
    coarse_population: CoarsePopulationDatum,
    coarse_agents: tuple[CoarseAgentDatum, ...],
    fine_inference: PopulationInference,
) -> RecursiveObservationDatum:


def validate_recursive_observation(
    datum: RecursiveObservationDatum,
    coarse_population: CoarsePopulationDatum,
    numerics: NumericsConfig,
) -> None:
```

For all sixteen fine observations, build real fine inference through unchanged `derive_population_inference`, then assert exact paired evidence, pushed recognition, pushed posterior, reconstructed recognition, reconstructed posterior, and local update marginals. Require sixteen normalized rows in each initial recognition and update kernel, at least two distinct update rows per parent, uniform non-Dirac coarse model marginals, and a non-product pushed coarse recognition law.

Add a sentinel object that raises on every attribute access and prove the information constructor never accepts or touches inference. Mutate fine recognitions, selector, realized observation, and posterior while holding fine population and structure fixed; require the generative datum and information/update data to remain exactly equal. Recognition data may change under recognition/selector mutation.

- [ ] **Step 2: Run RED and verify the missing public seams**

Run the new information/recognition test selection. Expected: missing function failures, while Task 3 generative tests remain green.

- [ ] **Step 3: Implement inference-free access and Bayes-update tables**

Validate that access specs are ordered by coarse agent, total over `reconstructed_population.observation_labels`, and identity-valued in Phase 2. For every reconstructed observation column, normalize the exact coarse posterior and marginalize it to each parent state support. Use information labels as update-channel sources and parent state labels as targets.

Compute access descent as

```python
max_tv = max(
    total_variation(update_rows[i], update_rows[j])
    for i, j in equal_access_pairs
)
```

The identity fixture gives exact zero. A test-only collapsed map that identifies two observations with unequal update rows must raise. The function receives no recognition or inference object and hashes only the completed population and access declaration.

- [ ] **Step 4: Implement recognition attachment and recursive observation derivation**

Push `fine_inference.recognition` through the stored combined channel. Marginalize the exact pushed joint to each parent's canonical local state support; build `AgentRecognitionDatum` values and constant-row recognition kernels over the information labels. Create a `declared_correlated` coarse selector whose coupling is the full pushed joint, not a product of the local marginals.

Map `fine_inference.observed_record` through `CoarseObservationSpec` to the one-record compound observation, call unchanged `derive_population_inference`, and push the fine posterior through the same combined channel. Return all values in `RecursiveObservationDatum` and validate exact support, evidence, recognition, posterior, selector-marginal, update-row, and channel consistency.

- [ ] **Step 5: Add live negative controls**

Add tests for a collapsed access map, split block channel, observation-changing relabeling, mismatched information order, mismatched selector marginal, altered update row, and one record/evaluator mutation. Each mutation must fail at its named semantic seam. Keep dynamic lumpability and scale composition absent from both code and tests.

- [ ] **Step 6: Run GREEN, inspect, and commit Task 4**

Run `test_coarse_agent.py` once for this task. Confirm all sixteen observations are exercised. Run `git diff --check`, stage only Task 4 files, and commit:

```powershell
git commit -m "feat: add recursive coarse inference interfaces"
```

## Task 5: Add the strict config discriminator and experiment registry record

**Files:**
- Modify: `src/multiagent_elbo/config.py`
- Modify: `src/multiagent_elbo/experiment_support.py`
- Modify: `tests/test_config.py`
- Modify: `tests/test_experiment_support.py`

**Interfaces:**
- Consumes: existing config resolver and experiment registry ordering.
- Produces: `RenormalizationV2RecursiveTheoryConfig` and the exact Phase 2 experiment contract. No root `rg_v2` module is imported by installed-package code.

- [ ] **Step 1: Write additive config and registry tests first**

Add tests that resolve exactly:

```python
THEORY = {
    "experiment": "renormalization_v2_recursive",
    "fixture": "lf4_two_parent_recursive_v1",
    "arithmetic": "exact_rational",
}
```

Reject the LF3 fixture names, unknown fixture, float arithmetic, missing key, and extra key. Append the discriminator after `renormalization_v2` without changing earlier order. Replace brittle tests that use the final tuple index with lookup by `experiment` name; do not change any pinned existing canonical JSON or SHA expectation.

Assert the registry record has launcher `run_renormalization_v2_recursive_lab.py`, config keys `("experiment","fixture","arithmetic")`, the exact eight artifact stems, and the exact twenty metric names from the spec. Retain the existing v1 six-artifact/thirteen-metric record byte-for-byte.

- [ ] **Step 2: Run RED and verify the missing type/record**

Run:

```powershell
C:\Python314\python.exe -B -m pytest tests\test_config.py tests\test_experiment_support.py -q -p no:cacheprovider
```

Expected: import or resolution failure for `RenormalizationV2RecursiveTheoryConfig`, not an altered v1 hash.

- [ ] **Step 3: Implement the additive config seam**

Add:

```python
@dataclass(frozen=True)
class RenormalizationV2RecursiveTheoryConfig:
    experiment: Literal["renormalization_v2_recursive"]
    fixture: Literal["lf4_two_parent_recursive_v1"]
    arithmetic: Literal["exact_rational"]
```

Append it to `ExperimentTheoryConfig`, append the discriminator to `NEW_EXPERIMENT_NAMES`, and add a separate `_resolve_theory_config` branch with exact keys and literals. Do not widen the Release 1 dataclass or its fixture literal.

- [ ] **Step 4: Implement the additive registry record**

Append one `ExperimentContract` in the same order as `NEW_EXPERIMENT_NAMES`. Use lane owner `rg_v2_recursive_phase2`, exact config keys, eight artifact stems, and twenty metrics. Do not weaken the import-time registry-order assertion or any existing lane-owner test.

- [ ] **Step 5: Run GREEN, inspect, and commit Task 5**

Run the same two test files. Confirm every preexisting pinned config hash still passes. Run `git diff --check`, stage only the four Task 5 files, and commit:

```powershell
git commit -m "feat: register recursive renormalization phase"
```

## Task 6: Publish the recursive experiment and click-to-run launcher

**Files:**
- Create: `rg_v2/recursive_experiment.py`
- Create: `run_renormalization_v2_recursive_lab.py`
- Create: `tests/rg_v2/test_recursive_experiment.py`
- Modify: `rg_v2/README.md`

**Interfaces:**
- Consumes: Tasks 2–5, `RunStore`, `collect_provenance`, `RngStreams`, `MetricRecord` helpers, and unchanged Release 1 population/coarse functions.
- Produces: `RenormalizationV2RecursiveExperimentResult`, `run_renormalization_v2_recursive_experiment`, the exact eight-artifact hash DAG, twenty candidate metrics, numerical mirrors, and a no-CLI root launcher.

- [ ] **Step 1: Write publication RED tests**

Add tests for strict pre-effect config validation, one fixture load, exact science-before-provenance/store ordering, exact ten-file finalized manifest, exact artifact order, direct-input DAG hashes, canonical rational records, all twenty `CANDIDATE` metrics, `allow_pickle=False` arrays, and mathematical equality across two output roots without byte/provenance equality.

Require `coarse_generative.json` canonical bytes and SHA to remain identical under recognition, selector, default observation, and posterior mutations. Require `coarse_interfaces.json` to change under a recognition mutation. Assert all sixteen observations occur in fixed order and each evidence/posterior roundtrip is exact.

Use spies only at the filesystem/RNG/provenance boundary to prove no effects; compute scientific expectations from real exact objects. Do not mock population, channel, inference, or metric arithmetic.

- [ ] **Step 2: Run RED and verify the missing runner**

Run:

```powershell
C:\Python314\python.exe -B -m pytest tests\rg_v2\test_recursive_experiment.py -q -p no:cacheprovider
```

Expected: collection fails because `rg_v2.recursive_experiment` is absent.

- [ ] **Step 3: Implement strict runtime validation and science assembly**

Add a Phase 2 result type with `run_dir`, `config_hash`, `status`, `metrics`, and read-only arrays. Reject wrong theory type/discriminator, wrong arithmetic, non-CPU or nondeterministic compute, non-float64 compute/numerics, invalid or loose `atol`, diagnostics disabled, and figures enabled before `load_recursive_fixture`, RNG, provenance, or store creation.

Build in order: fine constructor population, independent Release 1 population oracle, Phase 2 runtime oracle, coarse generative datum, sparse diagnostics, information/update interfaces, sixteen fine inferences, sixteen coarse recognition/observation results, and sixteen terminal common-channel aggregates for the finite KL diagnostics. Compare all exact laws before converting any value to float.

- [ ] **Step 4: Emit the exact twenty metrics**

Use the registry order and these directions:

```text
Exact target zero: metrics 1 through 15 and forbidden_dependency_violation_count.
Lower bound two: coarse_model_marginal_non_dirac_count.
Lower bound one: sparse_record_factorization_violation_count.
Lower bound -1e-12: minimum_conditional_kl_defect.
Upper bound 1e-12: maximum_kl_chain_residual, using absolute residuals.
```

Every record uses `assessment_scope="implementation_check"`, explicit theorem status, `verification_state="CANDIDATE"`, and explicit claim origin. Fail publication if any status is not `pass`.

- [ ] **Step 5: Build artifact bodies and dependency hashes in memory**

Use schema `rg-v2-recursive-phase2-artifact-v1`. Finalize the DAG in this order:

```text
fixture_snapshot -> fine_population -> coarse_generative
coarse_generative + access/recognition subhashes -> coarse_interfaces
coarse_generative -> coarse_population
fine_population + coarse_interfaces + coarse_population -> all_observation_inference
all six scientific JSON hashes -> metrics
all six scientific JSON hashes + metrics -> arrays
```

The fixture snapshot carries raw and ordered generative/recognition/structure/access subhashes. The generative artifact contains no access, update, recognition, selector, realized observation, evidence, or posterior field. Serialize every support-sensitive map as ordered records.

Build exactly six provenance arrays (`schema_version`, `fixture_id`, `producer_commit`, `config_hash`, `direct_input_names`, `direct_input_sha256`) plus float64 mirrors for fine constructor/oracle tables, pushed/reconstructed coarse tables, fine/coarse recognition, sixteen evidences, sixteen pushed/reconstructed posteriors, two update tables, sparse-TV magnitude, metric values, and metric tolerances. Use fixed-width Unicode and float64 only; make every array C-contiguous and read-only in memory.

Only after every envelope and array is final: create streams, collect provenance, call `RunStore.create`, write eight semantic stems, and finalize the exact suffixed filenames. No fixture read or payload mutation occurs after `RunStore.create`.

- [ ] **Step 6: Add the root launcher and README boundary**

Create a 40-line-style launcher matching Release 1:

```python
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

RUN = {"seed": 20260821}
THEORY = {
    "experiment": "renormalization_v2_recursive",
    "fixture": "lf4_two_parent_recursive_v1",
    "arithmetic": "exact_rational",
}
NUMERICS = {
    "dtype": "float64",
    "atol": 1.0e-12,
    "rtol": 1.0e-12,
    "min_spd_rcond": 1.0e-12,
    "max_frame_condition": 1.0e12,
}
OUTPUT = {
    "root": "artifacts/renormalization-v2-recursive",
    "collect_diagnostics": True,
    "render_figures": False,
}
```

The launcher performs no work on import, accepts no flags, and prints the run path and status from `main`. Add the exact click command and the static-closure/non-RG-flow boundary to `rg_v2/README.md` without changing Release 1 instructions.

- [ ] **Step 7: Run GREEN, inspect, and commit Task 6**

Run `test_recursive_experiment.py` plus Task 5 config/registry tests. Run `git diff --check`, stage only Task 6 files, inspect the cached diff, and commit:

```powershell
git commit -m "feat: publish recursive renormalization phase"
```

## Task 7: Add artifact-only replay, regression gates, documentation, and final verification

**Files:**
- Modify: `tests/rg_v2/test_recursive_experiment.py`
- Verify unchanged: `tests/rg_v2/test_legacy_regression.py`
- Modify: `docs/change-logs/2026-08-21.md`

**Interfaces:**
- Consumes: finalized Phase 2 artifacts only, the frozen v1 regression controller, launcher, and wheel metadata.
- Produces: fixture-free replay evidence, launcher/import/package gates, preserved Release 1 identities, final JUnit files, and the dated implementation record.

- [ ] **Step 1: Add the artifact-only replay gate**

Write a test-only replay function that accepts only the finalized run directory. Guard `load_recursive_fixture`, all `rg_v2/data` reads, and primitive paths so any access fails. Reconstruct agents, records, recognitions, selectors, structural channels, access/update data, fine and coarse populations, and all sixteen observation results from artifact bodies.

Before mapping metrics by name, require exactly twenty raw records, built-in string names, uniqueness, and exact ordered equality with the registry inventory. Recompute the 4,096 fine cells through an independent literal loop, all 256 coarse cells, the combined channel hash, observation bijection, sparse violations/TV, all recognition/evidence/posterior roundtrips, all twenty metric values/statuses, the complete DAG, and every NPZ mirror under `allow_pickle=False`.

Add duplicate, extra, reordered, and malformed metric mutations; altered direct-input hash; altered rational denominator; altered observation pair; and NPZ object-dtype mutation. Each must fail at its named raw boundary.

- [ ] **Step 2: Add launcher, import, wheel, and v1 regression gates**

Run the launcher by absolute path from an arbitrary temporary working directory with inherited `PYTHONPATH=""`; assert return code zero and one complete run. Parse the launcher AST and require one `sys.path.insert(0, str(SRC))`. Scan installed-package sources for reverse imports.

Build a wheel from a temporary source copy through `setuptools.build_meta.build_wheel`, inspect the ZIP for `multiagent_elbo/` and absence of top-level `rg_v2/`, extract it, import `multiagent_elbo` from the extracted wheel in a clean subprocess, and require `find_spec("rg_v2") is None`.

Do not edit the existing legacy regression or refresh its frozen semantic values. Its existing allowance already permits only the additive `config.py` and `experiment_support.py` seams. Run the fresh detached-baseline/current capture and require all protected v1 launcher configs, fixture hashes, semantic hashes, complete `MetricRecord` values, and protected blobs to match.

- [ ] **Step 3: Run the Task 7 targeted tests**

Run the replay/launcher/wheel selections and `test_legacy_regression.py`. Repair only demonstrated Phase 2 defects; do not loosen frozen v1 assertions or unrelated numerical tolerances.

- [ ] **Step 4: Run the consolidated focused CPU JUnit once**

Remove only stale task-owned Phase 2 JUnit/basetemp paths after resolving and confirming they are inside this worktree. Then run:

```powershell
$env:CUDA_VISIBLE_DEVICES = "-1"
$env:PYTHONHASHSEED = "0"
C:\Python314\python.exe -B -m pytest tests\rg_v2 tests\test_config.py tests\test_experiment_support.py -q -p no:cacheprovider --basetemp=.pytest-rg-v2-phase2 --junitxml=.pytest-rg-v2-phase2.xml
```

Parse the JUnit XML mechanically and record total, passed, skipped, failures, errors, time, and modification time. A progress line is not evidence.

- [ ] **Step 5: Run one broader CPU JUnit pass**

After the focused gate passes and without parallel edits, run:

```powershell
C:\Python314\python.exe -B -m pytest tests -q -p no:cacheprovider --basetemp=.pytest-rg-v2-phase2-broad --junitxml=.pytest-rg-v2-phase2-broad.xml
```

Let the command finish. If it exposes a defect caused by Phase 2, add a failing focused regression first, fix it, rerun the affected focused test, and rerun any invalidated final gate. If it exposes unrelated process-state sensitivity, preserve the failed XML and diagnose before deciding whether one unchanged rerun is warranted; do not edit unrelated source or tolerance.

- [ ] **Step 6: Run static and scope gates**

Run:

```powershell
git diff --check
rg -n "src[/\\]multiagent_elbo[/\\]rg_v2|from rg_v2|import rg_v2" src
rg -n "MetaAgent|as_agent|autonomous evolution|universality|semigroup|continuum limit" rg_v2 run_renormalization_v2_recursive_lab.py
git status --short
```

The reverse-import scan has no matches. Semantic-language matches are allowed only in explicit README nonclaims. Confirm no frozen Release 1 file changed and no task-owned replacement, patch, backup, fixture-generation, wheel, or temporary file remains.

- [ ] **Step 7: Update the dated log and commit Task 7**

Record the exact branch baseline, files, fixture dimensions, observation bijection, dense-pass/sparse-fail result, eight artifacts, twenty candidate metrics, replay gate, launcher/wheel/import checks, v1 regression, exact focused and broad JUnit totals, and no-CUDA boundary in `docs/change-logs/2026-08-21.md`.

Stage only the named Task 7 files and any Phase 2 JUnit files only if repository policy tracks them; otherwise retain them untracked for review and exclude them from the commit. Run `git diff --cached --check`, inspect the cached diff, and commit:

```powershell
git commit -m "test: close recursive renormalization release gates"
```

## Completion Gate

The branch is ready for final review only when it demonstrates all of the following at the same revision:

- four positive fine agents and four once-owned records construct exactly the same 4,096-cell fine joint through the unchanged constructor, independent runtime oracle, and test-only oracle;
- two declared block channels construct one normalized `256 x 16` combined channel without recognition inputs;
- two ordinary Release 1 agents and one dense combined record reconstruct every one of the 256 pushed coarse cells after the explicit observation bijection;
- every positive coarse model slice agrees with its derived evaluator, both coarse model recognition marginals are non-Dirac, and the coarse recognition joint is genuinely correlated rather than inferred from marginals;
- both information/update tables cover all sixteen observations, have at least two distinct rows, and reject a collapsed access map with unequal rows;
- all sixteen direct/reconstructed recognition, evidence, posterior, and update marginal arrows agree exactly;
- the dense record passes while the declared sparse record family has at least one exact violation and positive exact conditional-TV magnitude;
- generative bytes/hashes are stable under recognition, selector, realized-observation, evidence, and posterior mutations;
- `AggregateDatum` remains unchanged and terminal; the code exposes no dynamics, scale composition, fixed point, universality, continuum, meta-agent, or ontology claim;
- the strict recursive config and registry are additive, while all Release 1 configs, six artifacts, thirteen metrics, fixtures, launcher, results, and regression identities remain unchanged;
- one run finalizes exactly ten files: `config.json`, `manifest.json`, and the eight semantic artifacts with valid ordered dependency hashes;
- artifact-only replay reconstructs the complete mathematics and twenty ordered `CANDIDATE` metrics without primitive reads and validates non-object NPZ mirrors;
- the root launcher works from an arbitrary working directory with empty `PYTHONPATH`; the built wheel imports `multiagent_elbo` and excludes `rg_v2`; installed-package sources have no reverse import;
- final focused and broader CPU JUnit XML files report zero failures and zero errors, and no CUDA claim is made.

After all task reviews are clean, request one whole-branch review against the approved spec and this plan. Do not push, merge, or synchronize the Desktop checkout until the user separately requests publication.
