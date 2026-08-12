# Scientific Integrity Remediation Wave B Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close `AUD-01`, `AUD-02`, `AUD-04`, `AUD-05`, `AUD-10`, `AUD-11`, and `AUD-12` with byte-bound run bundles, factory-derived metric decisions, candidate-only producer states, immutable RNG provenance, canonical output roots, transactional figure generations, legacy observation without promotion, and exact-revision machine-readable evidence.

**Architecture:** A pure preparation layer serializes and validates an entire run into detached immutable bytes before any path is created. A publication layer installs those bytes through a sibling staging directory and writes `run-manifest-v2` last. Readers read each owned file once, verify and parse the same buffer, and return frozen payloads. Legacy v1 data goes through a separate observed-bundle adapter. One output-root resolver feeds launchers, experiments, publication, discovery, and figure replay. Figure output uses immutable content-addressed generations plus an atomically replaced active pointer under a process lock and recoverable journal. Numerical assessment and external verification remain separate namespaces: producers emit only `CANDIDATE`; the external ledger alone promotes or refutes claims.

**Tech Stack:** Python 3.14 standard library, NumPy, SciPy, matplotlib, pathlib, dataclasses, immutable `bytes`/`MappingProxyType`, SHA-256, strict JSON, NPZ with `allow_pickle=False`, pytest, JUnit XML, Git, and the installed verification control plane.

## Global Constraints

- Start only after Wave 0 and Wave A are merged serially and their exact-revision ledgers validate. Record the actual starting revision with `git rev-parse HEAD`; do not substitute design commit `c43a7c50675cf63b60f7b6cbea9664b638cd4c4e` for the future implementation base.
- Use a dedicated `codex/` branch and isolated worktree. Fetch before any remote-state claim. Preserve the user's live checkout and all unrelated dirty or untracked work byte-for-byte.
- Use American English in code, tests, comments, commits, evidence, and documentation.
- Use `C:\Python314\python.exe` for every Wave B test. For every evidence-producing command set `CUDA_VISIBLE_DEVICES='-1'` and `PYTHONHASHSEED='0'`; remove `MULTIAGENTELBO_RUN_CUDA_TESTS`, `VFE3_TEST_DEVICE`, and `CUBLAS_WORKSPACE_CONFIG`; and record the current `PYTHONPATH` value or JSON `null`. These are the exact six Wave 0 environment keys. Do not invoke `C:\anaconda\python.exe`, query the GPU, start a CUDA worker, run a sentinel, or run a confirmatory sweep.
- Wave B consumes Wave A's immutable-array behavior. Any authoritative array returned by a new loader must be backed by immutable `bytes`; `array.setflags(write=True)` must fail.
- Historical fixed-ray artifacts under `docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/` and `docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic/` are revision-bound inputs. Never rewrite, normalize, relabel, or upgrade them.
- `run-manifest-v2` is the only self-integrity schema. Legacy observations support compatibility/reproduction only and are ineligible for current v2 or source/config scientific promotion.
- Every returned or persisted producer field named `verification_state` or ending in `_verification_state` is exactly `CANDIDATE`. `pass`, `fail`, and `inconclusive` are assessment decisions, never verification states.
- Preparation, root resolution, source verification, and figure-input validation must finish before any output/staging/lock/journal path is created. Every negative test snapshots destination and relevant source roots and asserts an identical recursive `{relative_path: (size_bytes, sha256)}` map afterward.
- Completed manifests are written last. No manifest self-hashes. No v2 reader verifies one path and later reopens it for parsing.
- Do not garbage-collect figure generations in Wave B. Readers need no lease and may retain an old pointer while another publisher advances the active generation.
- Candidate and closure evidence must use Wave 0's generic `remediation_evidence.py run-junit` command, immutable `PreparedEvidenceBundle`, `build_evidence_index`, `publish_evidence_bundle`, and `validate` command without signature drift. The Wave B wrapper exposes exactly `build --stage {candidate,closure}`, `review-context-sha`, `validate-reviews`, and `populate-ledger`. Candidate evidence records `P/P`; exact-child closure records `E/P`.
- Wave-B-specific reviews and domain controls live in a separate closed `wave-b-domain-evidence-v1` inventory. The wrapper prepares the closed Wave 0 root-index bytes first and then prepares the domain inventory with the root index's path/size/SHA. The root index never points to the domain inventory. Both are published in one validated `PreparedEvidenceBundle`, so the graph is one-way and acyclic without changing Wave 0's root schema.
- Every implementation step below is literal. If a named helper, carrier, test fixture, schema, command, or file is not defined in its owning task, implementation stops and the plan is amended before code is written; workers may not substitute a prose-only approximation.
- Every Wave B source/config/Theory/dependency/environment change invalidates prior code evidence and current CUDA binding. Wave B performs no CUDA rerun; current CUDA sentinel, confirmatory, full-sweep, and general parity claims remain `INCONCLUSIVE`, while historical CUDA records remain unchanged and stale for the new revision.

## Start Gate

- [ ] **Blocking Wave 0 verifier dependency:** require the merged Wave 0
  snapshot `docs/verification/remediation/verification-contract-v1.json` and
  generic resolver CLI `tools/remediation_evidence.py
  resolve-verification-gate --snapshot PATH --root DIR`. Wave B passes the
  active root `C:\Users\chris and christine\.codex\skills\verification`; the
  resolver validates the snapshot-pinned `SKILL.md`, contract, all five
  criteria documents, ledger schema, and gate bytes before returning the gate
  path. There is no `.claude` fallback and Wave B defines no second resolver.
  If the snapshot or CLI is absent at the merged Wave 0 revision, or any byte
  differs, this plan is blocked before Task 1 rather than guessing an
  invocation.

- [ ] Fetch and inspect the real integration base without modifying WIP:

```powershell
git fetch origin
git log -1 --oneline origin/main
git status --short
$waveBBase = (git rev-parse HEAD).Trim()
```

- [ ] Validate the prior Wave A ledger and confirm the current tree contains the Wave 0 remediation contracts and Wave A immutable-array implementation:

```powershell
$verificationSnapshot = 'docs/verification/remediation/verification-contract-v1.json'
$verificationRoot = 'C:\Users\chris and christine\.codex\skills\verification'
$gate = (& 'C:\Python314\python.exe' -B tools\remediation_evidence.py resolve-verification-gate --snapshot $verificationSnapshot --root $verificationRoot).Trim()
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $gate -PathType Leaf)) {
  throw 'Wave 0 verifier snapshot resolution/precheck failed'
}
& 'C:\Python314\python.exe' $gate validate --cwd . .verification\wave-a\final-ledger.json
C:\Python314\python.exe -B -m pytest tests\test_remediation_contracts.py tests\test_remediation_evidence.py -q -p no:cacheprovider --basetemp=.pytest-wave-b-start-contracts
git diff --check
```

- [ ] Require zero failures, a valid ledger bound to the actual current Wave A revision, and no overlap with unrelated WIP before proceeding.

---

## File Responsibility Map

**Create:**

- `src/multiagent_elbo/output_paths.py`: canonical output-root resolution and frozen-config replacement.
- `src/multiagent_elbo/artifact_schema.py`: closed v2 run/metric-supporting artifact records, canonical name and NPZ validation, detached serialization, and frozen parsed payload helpers.
- `src/multiagent_elbo/figure_store.py`: figure-cache identity, lock/journal recovery, immutable generation publication, active-pointer validation, and fault boundaries.
- `tests/test_output_paths.py`: root anchoring, overlap, Git exception, reparse, and zero-effect controls.
- `tests/test_artifact_schema.py`: manifest-v2, preparation, loader, tamper, JSON/NPZ, single-read, and legacy observation controls.
- `tests/test_figure_store.py`: cache binding, generation/pointer transactions, concurrency, termination, and recovery controls.
- `tests/figure_fault_worker.py`: subprocess-only figure crash injector used by the hard-termination tests.
- `tools/build_wave_b_evidence.py`: a Wave-B-specific checked-in wrapper around Wave 0's `build_evidence_index` API.
- `docs/verification/remediation/wave-b-domain-evidence-v1.schema.json`: closed one-way inventory for Wave B control IDs and independent reviews.
- `tests/test_wave_b_evidence.py`: exact suite inventory, source/config bindings, head semantics, and CUDA-absence policy for the wrapper.

**Modify:**

- `src/multiagent_elbo/artifacts.py`, `src/multiagent_elbo/config.py`, `src/multiagent_elbo/runtime.py`, `src/multiagent_elbo/experiment_support.py`, `src/multiagent_elbo/figures.py`, `src/multiagent_elbo/rendering.py`, and `src/multiagent_elbo/__init__.py`.
- Producer/state carriers: `src/multiagent_elbo/finite/agent_network.py`, `src/multiagent_elbo/finite/counterexamples.py`, `src/multiagent_elbo/finite/theory_oracles.py`, and `src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostics.py`.
- Every run producer: `src/multiagent_elbo/finite/experiment.py`, `agent_network_experiment.py`, `attention_experiment.py`, `categorical_dqm_experiment.py`, `counterexample_experiment.py`, `information_history_experiment.py`, `scale_cocycle_experiment.py`, `theory_oracle_experiment.py`, `src/multiagent_elbo/geometry/holonomy_experiment.py`, `src/multiagent_elbo/realizations/gaussian/experiment.py`, `confirmatory_analysis.py`, `fixed_ray_diagnostic_experiment.py`, and `fixed_ray_experiment.py`.
- Every launcher/discovery surface: `run_finite_lab.py`, `run_multiagent_network_lab.py`, `run_attention_lab.py`, `run_categorical_dqm_lab.py`, `run_finite_counterexample_lab.py`, `run_information_history_lab.py`, `run_scale_cocycle_lab.py`, `run_theory_oracle_lab.py`, `run_gauge_holonomy_lab.py`, `run_gaussian_lab.py`, `run_gaussian_fixed_ray_diagnostic.py`, `run_gaussian_fixed_ray_lab.py`, and `make_figures.py`.
- Existing affected tests: `tests/test_artifacts.py`, `test_experiment_support.py`, `test_runtime.py`, `test_config.py`, `test_figures.py`, `test_launchers.py`, every `test_*_experiment.py` that exercises a writer/reader, `test_gaussian_realization.py`, `test_gaussian_confirmatory_analysis.py`, `test_gaussian_results_document.py`, and `test_shared_scientific_contracts.py`.

## Frozen Public Schemas and Interfaces

### Run manifest v2

The schema and union key sets are literal constants, not documentation-only
examples:

```python
RUN_MANIFEST_V2_KEYS = {
    "schema_version",
    "status",
    "artifact_kind",
    "config_identity",
    "source_identity",
    "artifacts",
}
CONFIG_IDENTITY_KEYS = {"schema_version", "sha256"}
AVAILABLE_SOURCE_IDENTITY_KEYS = {
    "status",
    "git_commit",
    "git_dirty",
    "git_status_sha256",
    "dirty_tree_sha256",
    "theory_sha256",
}
UNAVAILABLE_SOURCE_IDENTITY_KEYS = {"status", "reason"}
ARTIFACT_INVENTORY_ENTRY_KEYS = {"name", "kind", "size_bytes", "sha256"}
```

`schema_version` is exactly `run-manifest-v2`, `status` is exactly `complete`,
and `config_identity` is exactly
`{"schema_version":"canonical-experiment-config-v1","sha256":"..."}`,
where the `sha256` value is exactly 64 lowercase hexadecimal characters.
The available source member contains a 40-character lowercase Git SHA-1, a real
Boolean `git_dirty`, and three lowercase SHA-256 values. The unavailable member
has exactly keys `status` and `reason`, value `status="unavailable"`, and a
nonempty string `reason`. It may be
emitted only when provenance explicitly carries that typed member; missing or
malformed provenance never silently becomes unavailable.

The manifest excludes itself. Its ASCII-name-sorted `artifacts` tuple includes
`config.json`, `provenance.json`, every JSON payload, and every NPZ payload.
Each entry has exactly `name`, `kind`, `size_bytes`, and `sha256`; `kind` is one
of `config`, `provenance`, `json`, or `npz`. Names are one portable ASCII
segment, unique after case-folding, and may not alias `manifest.json` or the
optional crash marker.

`config.json` has exactly:

```python
RUN_CONFIG_V2_KEYS = {"schema_version", "config_hash", "resolved_config"}
```

with schema `run-config-v2`. `provenance.json` has exactly
has exactly keys `schema_version` and `record`, value
`schema_version="run-provenance-v2"`, and a mapping-valued `record`. Its record must
contain `config_hash` equal to the config identity, the exact typed
`source_identity`, and `source_digest_exclusions` equal to the sorted resolved
output roots. Loader validation requires the config payload, provenance record,
manifest config identity, and manifest source identity to agree.

### Prepared and verified run interfaces

```python
ArtifactEntryKind = Literal['config', 'provenance', 'json', 'npz']
NpzFinitePolicy = Literal["finite"]


JsonScalar = None | bool | int | float | str


@dataclass(frozen=True, slots=True)
class ArtifactInventoryEntry:
    name: str
    kind: ArtifactEntryKind | Literal['png', 'pdf', 'bytes']
    size_bytes: int
    sha256: str


@dataclass(frozen=True, slots=True)
class AvailableSourceIdentity:
    git_commit: str
    git_dirty: bool
    git_status_sha256: str
    dirty_tree_sha256: str
    theory_sha256: str
    status: Literal["available"] = field(default="available", init=False)


@dataclass(frozen=True, slots=True)
class UnavailableSourceIdentity:
    reason: str
    status: Literal["unavailable"] = field(default="unavailable", init=False)


@dataclass(frozen=True, slots=True)
class NpzArrayInput:
    values: np.ndarray
    finite_policy: NpzFinitePolicy = "finite"


@dataclass(frozen=True, slots=True)
class RunPayloads:
    artifact_kind: str
    json_payloads: Mapping[str, object]
    npz_payloads: Mapping[str, Mapping[str, NpzArrayInput]]


@dataclass(frozen=True, slots=True)
class PreparedArtifact:
    name: str
    kind: ArtifactEntryKind
    content: bytes
    size_bytes: int
    sha256: str


@dataclass(frozen=True, slots=True)
class PreparedRunBundle:
    run_dir: Path
    output_root_admission: ResolvedOutputRoot
    config_hash: str
    artifact_kind: str
    source_identity: AvailableSourceIdentity | UnavailableSourceIdentity
    artifacts: tuple[PreparedArtifact, ...]
    manifest_bytes: bytes
    schema_version: Literal["prepared-run-bundle-v2"] = field(
        default="prepared-run-bundle-v2", init=False
    )


@dataclass(frozen=True, slots=True)
class RunStore:
    run_dir: Path
    config_hash: str
    schema_version: Literal["legacy-run-manifest-v1", "run-manifest-v2"]


@dataclass(frozen=True, slots=True, init=False)
class VerifiedRunBundle:
    run_dir: Path
    manifest_sha256: str
    manifest: Mapping[str, object]
    inventory: tuple[ArtifactInventoryEntry, ...]
    json_payloads: Mapping[str, object]
    npz_payloads: Mapping[str, Mapping[str, np.ndarray]]
    source_claim_eligible: bool


@dataclass(frozen=True, slots=True)
class LegacyObservation:
    observed_at_revision: str
    files: tuple[ArtifactInventoryEntry, ...]
    legacy_schema: Literal['legacy-run-manifest-v1']
    limitations: tuple[str, str]
    schema_version: Literal['legacy-run-observation-v1'] = field(
        default='legacy-run-observation-v1', init=False
    )


@dataclass(frozen=True, slots=True, init=False)
class LegacyObservedBundle:
    run_dir: Path
    observation: LegacyObservation
    file_bytes: Mapping[str, bytes]
    json_payloads: Mapping[str, object]
    npz_payloads: Mapping[str, Mapping[str, np.ndarray]]
    source_claim_eligible: Literal[False] = False


def prepare_run_bundle(
    config: ExperimentConfig,
    provenance: Mapping[str, object],
    payloads: RunPayloads,
) -> PreparedRunBundle: ...


def parse_source_identity(
    value: object,
) -> AvailableSourceIdentity | UnavailableSourceIdentity: ...


def source_identity_payload(
    value: AvailableSourceIdentity | UnavailableSourceIdentity,
) -> dict[str, object]: ...


def publish_run_bundle(prepared: PreparedRunBundle) -> RunStore: ...


def load_verified_run_bundle(run_dir: Path | str) -> VerifiedRunBundle: ...


def verify_legacy_v1_observed(
    run_dir: Path | str,
    *,
    observed_at_revision: str,
) -> LegacyObservedBundle: ...


def load_run_bundle(
    run_dir: Path | str,
    *,
    legacy_observed_at_revision: str | None = None,
) -> VerifiedRunBundle | LegacyObservedBundle: ...
```

`NpzArrayInput` and `RunPayloads` are caller-input carriers only. Preparation
must detach them before constructing `PreparedRunBundle`; neither input carrier
is retained by that bundle. Every source-identity and inventory dataclass
validates its closed enums, exact Boolean-vs-integer types, safe names, positive
sizes where required, and lowercase full-length digests in `__post_init__`.
`PreparedRunBundle.__post_init__` validates tuple order, case-fold uniqueness,
per-artifact byte size/hash, manifest reconstruction, destination identity, and
the exact source/config agreement. `publish_run_bundle` repeats that validation
because callers may directly construct a forged public dataclass.

`VerifiedRunBundle` and `LegacyObservedBundle` have no public initializer. Their
module-private constructors recursively convert JSON mappings to fresh
`MappingProxyType` objects, JSON lists to tuples, file bytes to owned `bytes`,
and numeric arrays to Wave A immutable-byte-backed arrays. Thus no returned
mapping or nested sequence aliases parser state, and `setflags(write=True)`
fails for every authoritative array. The parsed manifest is an exact-key,
deeply frozen mapping; it is never a loose caller-supplied `Mapping`.

`prepare_run_bundle` computes the run directory exactly as:

```python
run_dir = (
    resolved_config.output.root
    / sanitize_run_name(resolved_config.run.name)
    / f"{config_hash}-{resolved_config.run.seed}"
)
```

`sanitize_run_name` retains the existing compatibility rule
`re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip(".-_") or "run"`.
Preparation accepts only an absolute root previously admitted by
`with_resolved_output_root`; it never resolves an ambient path itself.

Every tuple and mapping returned from preparation/loading is deeply frozen.
`PreparedRunBundle` retains only destination identity, scalar metadata, tuples,
the immutable `ResolvedOutputRoot` admission record, and immutable bytes. It
retains no caller collection, array, callback, file
handle, source path, lazy serializer, or closure. Publication rehashes every
owned buffer, reconstructs the complete manifest from parsed owned
`config.json`/`provenance.json` plus artifact records, and requires that
reconstruction to equal `manifest_bytes` byte-for-byte before creating the
destination parent. It writes only those buffers. A v2 `RunStore` rejects every
incremental method; `RunStore.create` returns only a legacy-v1 handle.

### Legacy observation

`LegacyObservedBundle.observation_payload()` returns exactly:

```json
{
  "schema_version": "legacy-run-observation-v1",
  "observed_at_revision": "full-git-object-id",
  "files": [
    {
      "name": "config.json",
      "kind": "json",
      "size_bytes": 1,
      "sha256": "64-lowercase-hex"
    }
  ],
  "legacy_schema": "legacy-run-manifest-v1",
  "limitations": [
    "Observed bytes support compatibility and reproduction only.",
    "The observation does not provide manifest-v2 self-integrity or current scientific promotion."
  ]
}
```

The observation inventories every regular file actually present, even when a
tracked public extract intentionally differs from the original raw v1 manifest
inventory. That difference is a limitation, not grounds for silently inventing
v2 integrity. Absence of `schema_version` is not itself a legacy schema.
`load_run_bundle` dispatches a schemaless mapping only through this closed
recognizer:

```python
LEGACY_MANIFEST_V1_KEYS = {"artifacts", "complete", "config_hash", "provenance"}


def recognize_legacy_v1_manifest(
    payload: object,
    *,
    observed_at_revision: str,
) -> None:
    if type(payload) is not dict or set(payload) != LEGACY_MANIFEST_V1_KEYS:
        raise ValueError("unrecognized schemaless manifest")
    if type(observed_at_revision) is not str or re.fullmatch(
        r"[0-9a-f]{40}", observed_at_revision
    ) is None:
        raise ValueError("legacy observation revision must be a full Git SHA")
    if payload["complete"] is not True:
        raise ValueError("legacy manifest is not complete")
    config_hash = payload["config_hash"]
    if type(config_hash) is not str or re.fullmatch(
        r"[0-9a-f]{64}", config_hash
    ) is None:
        raise ValueError("legacy config identity is invalid")
    artifacts = payload["artifacts"]
    if type(artifacts) is not dict:
        raise ValueError("legacy artifacts must be a mapping")
    if not artifacts or artifacts.get("manifest.json") != "complete":
        raise ValueError("legacy manifest inventory is not recognizable")
    for name, state in artifacts.items():
        if type(name) is not str or re.fullmatch(
            r"[A-Za-z0-9][A-Za-z0-9._-]*", name
        ) is None:
            raise ValueError("legacy artifact name is not portable")
        stem = name.split(".", 1)[0].casefold()
        if stem in {"con", "prn", "aux", "nul"} or re.fullmatch(
            r"(?:com|lpt)[1-9]", stem
        ):
            raise ValueError("legacy artifact name is reserved")
        if type(state) is not str or state != "complete":
            raise ValueError("legacy artifact state is not complete")
    provenance = payload["provenance"]
    if type(provenance) is not dict:
        raise ValueError("legacy provenance must be a mapping")
    if not {"config_hash", "git_commit"} <= set(provenance):
        raise ValueError("legacy provenance identity is incomplete")
    if provenance.get("config_hash") != config_hash:
        raise ValueError("legacy config identity mismatch")
    git_commit = provenance.get("git_commit")
    if type(git_commit) is not str or re.fullmatch(
        r"[0-9a-f]{40}", git_commit
    ) is None or git_commit != observed_at_revision:
        raise ValueError("legacy observation revision mismatch")
```

The implementation uses the already-defined strict key/digest/name helpers;
the code above introduces no second permissive parser. The two pinned historical
manifests satisfy the recognizer. A schemaless mapping with any other root shape,
an incomplete artifact, config/provenance drift, or revision drift rejects.
`load_verified_run_bundle` always rejects legacy. Unknown nonempty schema strings
reject rather than falling through to legacy.

---

### Task 1: Replace caller-selected metric states with `metric-record-v2`

**Closes:** `AUD-04` core contract; establishes the producer-state half of `AUD-05`.

**Files:**

- Modify: `src/multiagent_elbo/experiment_support.py`
- Modify: `tests/test_experiment_support.py`

**Interfaces and exact serialized keys:**

```python
MetricComparatorKind = Literal[
    "within_absolute_tolerance",
    "at_most",
    "at_least",
    "expected_positive_infinity",
]
MetricDirection = Literal["two_sided", "upper", "lower", "positive_infinity"]
MetricStrictness = Literal["inclusive", "strict"]
AssessmentDecision = Literal["pass", "fail", "inconclusive"]

METRIC_RECORD_V2_KEYS = {
    "schema_version",
    "value",
    "comparator",
    "applicability_reason",
    "interpretation",
    "assessment_scope",
    "theorem_status",
    "claim_origin",
    "assessment_decision",
    "verification_state",
}
METRIC_COMPARATOR_V2_KEYS = {
    "kind", "target", "bound", "direction", "strictness", "tolerance"
}


@dataclass(frozen=True)
class MetricComparator:
    kind: MetricComparatorKind
    target: float | None
    bound: float | None
    direction: MetricDirection
    strictness: MetricStrictness
    tolerance: float


@dataclass(frozen=True)
class MetricRecord:
    value: float
    comparator: MetricComparator | None
    applicability_reason: str
    interpretation: str
    assessment_scope: Literal["implementation_check"]
    theorem_status: TheoremStatus
    claim_origin: ClaimOrigin
    schema_version: Literal["metric-record-v2"] = field(
        default="metric-record-v2", init=False
    )
    assessment_decision: AssessmentDecision = field(init=False)
    verification_state: Literal["CANDIDATE"] = field(
        default="CANDIDATE", init=False
    )

    @property
    def status(self) -> AssessmentDecision:
        return self.assessment_decision

    @property
    def decision(self) -> AssessmentDecision:
        return self.assessment_decision
```

The `decision` and `status` properties preserve read compatibility only; neither
is serialized. `metric_record_payload` tags a finite value as
`{"kind":"finite","number":value}` and positive infinity as
`{"kind":"positive_infinity"}`. Comparator target, bound, and tolerance are
ordinary finite JSON numbers. `load_metric_record` rejects unknown/missing keys,
reconstructs the record, recomputes `assessment_decision`, and rejects drift.
Wave 0's public alias identities remain a required end state, but Task 1 does
not import, migrate, or test either producer module. Task 7 first replaces the
private records in `multiagent_elbo.finite.experiment` and
`multiagent_elbo.realizations.gaussian.experiment`, and only then adds the
identity test for `FiniteExperimentMetricRecord`, `GaussianMetricRecord`, and
this exact shared class. This keeps Task 1's local GREEN independent of future
producer changes.

- [ ] **Step 1: Add the literal boundary and closed-schema RED tests**

Add these imports and tests to `tests/test_experiment_support.py`:

```python
import copy
import json
import math
from fractions import Fraction

import numpy as np


def _comparator(
    kind,
    *,
    target=None,
    bound=None,
    direction,
    strictness="inclusive",
    tolerance=0.125,
):
    return MetricComparator(
        kind=kind,
        target=target,
        bound=bound,
        direction=direction,
        strictness=strictness,
        tolerance=tolerance,
    )


ONE = float.fromhex("0x1.0000000000000p+0")
EIGHTH = float.fromhex("0x1.0000000000000p-3")
LOWER = float.fromhex("0x1.c000000000000p-1")
UPPER = float.fromhex("0x1.2000000000000p+0")
assert ONE - EIGHTH == LOWER
assert ONE + EIGHTH == UPPER

TRUTH_CASES = (
    (_comparator("within_absolute_tolerance", target=ONE, direction="two_sided", tolerance=EIGHTH), LOWER, "pass"),
    (_comparator("within_absolute_tolerance", target=ONE, direction="two_sided", tolerance=EIGHTH), math.nextafter(LOWER, -math.inf), "fail"),
    (_comparator("within_absolute_tolerance", target=ONE, direction="two_sided", tolerance=EIGHTH), ONE, "pass"),
    (_comparator("within_absolute_tolerance", target=ONE, direction="two_sided", tolerance=EIGHTH), UPPER, "pass"),
    (_comparator("within_absolute_tolerance", target=ONE, direction="two_sided", tolerance=EIGHTH), math.nextafter(UPPER, math.inf), "fail"),
    (_comparator("at_most", bound=ONE, direction="upper", tolerance=EIGHTH), math.nextafter(LOWER, -math.inf), "pass"),
    (_comparator("at_most", bound=ONE, direction="upper", tolerance=EIGHTH), UPPER, "pass"),
    (_comparator("at_most", bound=ONE, direction="upper", tolerance=EIGHTH), math.nextafter(UPPER, math.inf), "fail"),
    (_comparator("at_most", bound=ONE, direction="upper", strictness="strict", tolerance=EIGHTH), math.nextafter(LOWER, -math.inf), "pass"),
    (_comparator("at_most", bound=ONE, direction="upper", strictness="strict", tolerance=EIGHTH), LOWER, "fail"),
    (_comparator("at_most", bound=ONE, direction="upper", strictness="strict", tolerance=EIGHTH), UPPER, "fail"),
    (_comparator("at_least", bound=ONE, direction="lower", tolerance=EIGHTH), math.nextafter(UPPER, math.inf), "pass"),
    (_comparator("at_least", bound=ONE, direction="lower", tolerance=EIGHTH), LOWER, "pass"),
    (_comparator("at_least", bound=ONE, direction="lower", tolerance=EIGHTH), math.nextafter(LOWER, -math.inf), "fail"),
    (_comparator("at_least", bound=ONE, direction="lower", strictness="strict", tolerance=EIGHTH), math.nextafter(UPPER, math.inf), "pass"),
    (_comparator("at_least", bound=ONE, direction="lower", strictness="strict", tolerance=EIGHTH), UPPER, "fail"),
    (_comparator("at_least", bound=ONE, direction="lower", strictness="strict", tolerance=EIGHTH), LOWER, "fail"),
    (_comparator("expected_positive_infinity", direction="positive_infinity", tolerance=0.0), math.inf, "pass"),
    (_comparator("expected_positive_infinity", direction="positive_infinity", tolerance=0.0), ONE, "fail"),
    (_comparator("expected_positive_infinity", direction="positive_infinity", tolerance=0.0), float.fromhex("0x1.fffffffffffffp+1023"), "fail"),
)
TRUTH_CASE_IDS = (
    "within-lower-pass", "within-below-lower-fail", "within-target-pass",
    "within-upper-pass", "within-above-upper-fail", "at-most-below-pass",
    "at-most-inclusive-upper-pass", "at-most-inclusive-above-fail",
    "at-most-strict-below-pass", "at-most-strict-boundary-fail",
    "at-most-strict-upper-fail", "at-least-above-pass",
    "at-least-inclusive-lower-pass", "at-least-inclusive-below-fail",
    "at-least-strict-above-pass", "at-least-strict-boundary-fail",
    "at-least-strict-lower-fail", "expected-infinity-pass",
    "expected-infinity-one-fail", "expected-infinity-max-finite-fail",
)
assert len(TRUTH_CASES) == len(TRUTH_CASE_IDS)


@pytest.mark.parametrize(
    "comparator,value,expected", TRUTH_CASES, ids=TRUTH_CASE_IDS
)
def test_metric_v2_truth_table(comparator, value, expected):
    record = MetricRecord(
        value=value,
        comparator=comparator,
        applicability_reason="the preregistered comparator applies",
        interpretation="boundary fixture",
        assessment_scope="implementation_check",
        theorem_status="NUMERICAL",
        claim_origin="APPLICATION_SPECIFIC",
    )
    assert record.assessment_decision == expected
    assert record.status == expected
    assert record.verification_state == "CANDIDATE"


def test_inapplicable_metric_is_never_passing():
    record = inapplicable_metric(
        1.0,
        applicability_reason="CUDA was not requested",
        interpretation="CPU-only parity is inapplicable",
        theorem_status="NUMERICAL",
        claim_origin="APPLICATION_SPECIFIC",
    )
    assert record.comparator is None
    assert record.assessment_decision == "inconclusive"
    assert record.verification_state == "CANDIDATE"


@pytest.mark.parametrize(
    "changes,message",
    [
        ({"target": None}, "target"),
        ({"bound": 1.0}, "bound"),
        ({"direction": "upper"}, "direction"),
        ({"strictness": "strict"}, "strictness"),
        ({"tolerance": -1.0}, "tolerance"),
        ({"tolerance": math.inf}, "tolerance"),
        ({"tolerance": True}, "tolerance"),
    ],
)
def test_metric_comparator_rejects_invalid_within_contract(changes, message):
    values = {
        "kind": "within_absolute_tolerance",
        "target": 1.0,
        "bound": None,
        "direction": "two_sided",
        "strictness": "inclusive",
        "tolerance": 0.125,
    }
    values.update(changes)
    with pytest.raises((TypeError, ValueError), match=message):
        MetricComparator(**values)


@pytest.mark.parametrize(
    "values,message",
    [
        ({"kind": "unknown", "target": None, "bound": None, "direction": "upper", "strictness": "inclusive", "tolerance": 0.0}, "kind"),
        ({"kind": "within_absolute_tolerance", "target": None, "bound": None, "direction": "two_sided", "strictness": "inclusive", "tolerance": 0.0}, "target"),
        ({"kind": "within_absolute_tolerance", "target": 1.0, "bound": 1.0, "direction": "two_sided", "strictness": "inclusive", "tolerance": 0.0}, "bound"),
        ({"kind": "within_absolute_tolerance", "target": 1.0, "bound": None, "direction": "upper", "strictness": "inclusive", "tolerance": 0.0}, "direction"),
        ({"kind": "within_absolute_tolerance", "target": 1.0, "bound": None, "direction": "two_sided", "strictness": "strict", "tolerance": 0.0}, "strictness"),
        ({"kind": "at_most", "target": 1.0, "bound": 1.0, "direction": "upper", "strictness": "inclusive", "tolerance": 0.0}, "target"),
        ({"kind": "at_most", "target": None, "bound": None, "direction": "upper", "strictness": "inclusive", "tolerance": 0.0}, "bound"),
        ({"kind": "at_most", "target": None, "bound": 1.0, "direction": "lower", "strictness": "inclusive", "tolerance": 0.0}, "direction"),
        ({"kind": "at_least", "target": 1.0, "bound": 1.0, "direction": "lower", "strictness": "inclusive", "tolerance": 0.0}, "target"),
        ({"kind": "at_least", "target": None, "bound": None, "direction": "lower", "strictness": "inclusive", "tolerance": 0.0}, "bound"),
        ({"kind": "at_least", "target": None, "bound": 1.0, "direction": "upper", "strictness": "inclusive", "tolerance": 0.0}, "direction"),
        ({"kind": "expected_positive_infinity", "target": 1.0, "bound": None, "direction": "positive_infinity", "strictness": "inclusive", "tolerance": 0.0}, "target"),
        ({"kind": "expected_positive_infinity", "target": None, "bound": 1.0, "direction": "positive_infinity", "strictness": "inclusive", "tolerance": 0.0}, "bound"),
        ({"kind": "expected_positive_infinity", "target": None, "bound": None, "direction": "upper", "strictness": "inclusive", "tolerance": 0.0}, "direction"),
        ({"kind": "expected_positive_infinity", "target": None, "bound": None, "direction": "positive_infinity", "strictness": "strict", "tolerance": 0.0}, "strictness"),
        ({"kind": "expected_positive_infinity", "target": None, "bound": None, "direction": "positive_infinity", "strictness": "inclusive", "tolerance": 0.125}, "tolerance"),
    ],
)
def test_metric_comparator_invalid_matrix(values, message):
    with pytest.raises((TypeError, ValueError), match=message):
        MetricComparator(**values)


@pytest.mark.parametrize(
    "field,value",
    [
        ("target", True), ("target", math.nan), ("target", math.inf),
        ("bound", np.bool_(False)), ("bound", -math.inf),
        ("tolerance", np.bool_(True)), ("tolerance", math.nan),
        ("tolerance", -math.inf), ("tolerance", math.inf),
    ],
)
def test_metric_comparator_rejects_non_json_numeric_operands(field, value):
    values = {
        "kind": "within_absolute_tolerance" if field == "target" else "at_most",
        "target": 1.0 if field == "target" else None,
        "bound": None if field == "target" else 1.0,
        "direction": "two_sided" if field == "target" else "upper",
        "strictness": "inclusive",
        "tolerance": 0.0,
    }
    values[field] = value
    with pytest.raises((TypeError, ValueError), match=field):
        MetricComparator(**values)


@pytest.mark.parametrize(
    "value",
    [True, False, np.bool_(True), "1", 1 + 0j, math.nan, -math.inf, math.inf],
)
def test_ordinary_metric_rejects_nonfinite_or_boolean_value(value):
    with pytest.raises((TypeError, ValueError), match="value"):
        MetricRecord(
            value=value,
            comparator=_comparator("at_most", bound=1.0, direction="upper"),
            applicability_reason="comparator applies",
            interpretation="invalid value control",
            assessment_scope="implementation_check",
            theorem_status="NUMERICAL",
            claim_origin="APPLICATION_SPECIFIC",
        )


@pytest.mark.parametrize("value", [math.nan, -math.inf])
def test_expected_infinity_metric_rejects_nan_and_negative_infinity(value):
    with pytest.raises(ValueError, match="value"):
        expected_positive_infinity_metric(
            value,
            applicability_reason="extended endpoint applies",
            interpretation="invalid extended value",
            theorem_status="NUMERICAL",
            claim_origin="APPLICATION_SPECIFIC",
        )


@pytest.mark.parametrize("value", [Fraction(9, 8), np.float64(1.125), np.int64(1)])
def test_metric_real_inputs_normalize_to_json_safe_builtins(value):
    payload = metric_record_payload(target_metric(
        value,
        Fraction(1, 8),
        target=np.float64(1.0),
        applicability_reason="normalization fixture",
        interpretation="all serialized numerics are built in",
        theorem_status="NUMERICAL",
        claim_origin="APPLICATION_SPECIFIC",
    ))
    assert type(payload["value"]["number"]) is float
    assert type(payload["comparator"]["target"]) is float
    assert type(payload["comparator"]["tolerance"]) is float
    json.dumps(payload, allow_nan=False)


def test_metric_v2_payload_is_closed_and_loader_recomputes_decision():
    record = target_metric(
        1.125,
        0.125,
        target=1.0,
        applicability_reason="target comparison applies",
        interpretation="closed payload fixture",
        theorem_status="NUMERICAL",
        claim_origin="APPLICATION_SPECIFIC",
    )
    payload = metric_record_payload(record)
    assert set(payload) == METRIC_RECORD_V2_KEYS
    assert set(payload["comparator"]) == METRIC_COMPARATOR_V2_KEYS
    assert load_metric_record(payload) == record
    changed = copy.deepcopy(payload)
    changed["assessment_decision"] = "fail"
    with pytest.raises(ValueError, match="assessment_decision"):
        load_metric_record(changed)


@pytest.mark.parametrize(
    "mutate,message",
    [
        (lambda p: p.update({"extra": 1}), "keys"),
        (lambda p: p.pop("interpretation"), "keys"),
        (lambda p: p.__setitem__("schema_version", "metric-record-v1"), "schema"),
        (lambda p: p.__setitem__("verification_state", "EVIDENCE_VERIFIED"), "verification_state"),
        (lambda p: p.__setitem__("assessment_scope", "theorem"), "assessment_scope"),
        (lambda p: p.__setitem__("value", {"kind": "finite", "number": math.nan}), "value"),
        (lambda p: p.__setitem__("value", {"kind": "finite", "number": math.inf}), "value"),
        (lambda p: p.__setitem__("value", {"kind": "positive_infinity", "number": 1.0}), "value"),
        (lambda p: p.__setitem__("value", {"kind": "negative_infinity"}), "value"),
        (lambda p: p["comparator"].update({"extra": 1}), "comparator"),
        (lambda p: p["comparator"].__setitem__("tolerance", math.inf), "tolerance"),
    ],
)
def test_metric_v2_loader_invalid_serialization_matrix(mutate, message):
    payload = metric_record_payload(target_metric(
        1.0,
        0.0,
        target=1.0,
        applicability_reason="serialization fixture",
        interpretation="closed reader",
        theorem_status="NUMERICAL",
        claim_origin="APPLICATION_SPECIFIC",
    ))
    mutate(payload)
    with pytest.raises((TypeError, ValueError), match=message):
        load_metric_record(payload)


@pytest.mark.parametrize(
    "comparator,value,expected", TRUTH_CASES, ids=TRUTH_CASE_IDS
)
def test_metric_v2_every_truth_case_round_trips(comparator, value, expected):
    record = MetricRecord(
        value=value,
        comparator=comparator,
        applicability_reason="round-trip fixture",
        interpretation="binary-exact truth table",
        assessment_scope="implementation_check",
        theorem_status="NUMERICAL",
        claim_origin="APPLICATION_SPECIFIC",
    )
    payload = metric_record_payload(record)
    json.dumps(payload, allow_nan=False)
    assert load_metric_record(copy.deepcopy(payload)) == record
    assert record.assessment_decision == expected


def test_metric_state_and_decision_are_not_constructor_inputs():
    kwargs = {
        "value": 1.0,
        "comparator": None,
        "applicability_reason": "not applicable",
        "interpretation": "constructor control",
        "assessment_scope": "implementation_check",
        "theorem_status": "NUMERICAL",
        "claim_origin": "APPLICATION_SPECIFIC",
    }
    with pytest.raises(TypeError, match="verification_state"):
        MetricRecord(**kwargs, verification_state="EVIDENCE_VERIFIED")
    with pytest.raises(TypeError, match="assessment_decision"):
        MetricRecord(**kwargs, assessment_decision="pass")
```

- [ ] **Step 2: Run the focused RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_experiment_support.py -k "metric or producer" -q -p no:cacheprovider --basetemp=.pytest-wave-b-task1-red
```

Expected: FAIL because the old record accepts caller states/nonfinite values and lacks the closed comparator schema.

- [ ] **Step 3: Implement exact validation, decision derivation, and factories**

Use these predicates without algebraic rearrangement:

```python
def _metric_decision(
    value: float,
    comparator: MetricComparator | None,
) -> AssessmentDecision:
    if comparator is None:
        return "inconclusive"
    if comparator.kind == "within_absolute_tolerance":
        assert comparator.target is not None
        return "pass" if abs(value - comparator.target) <= comparator.tolerance else "fail"
    if comparator.kind == "at_most":
        assert comparator.bound is not None
        if comparator.strictness == "inclusive":
            passed = value <= comparator.bound + comparator.tolerance
        else:
            passed = value < comparator.bound - comparator.tolerance
        return "pass" if passed else "fail"
    if comparator.kind == "at_least":
        assert comparator.bound is not None
        if comparator.strictness == "inclusive":
            passed = value >= comparator.bound - comparator.tolerance
        else:
            passed = value > comparator.bound + comparator.tolerance
        return "pass" if passed else "fail"
    if comparator.kind == "expected_positive_infinity":
        return "pass" if value == float("inf") else "fail"
    raise AssertionError("validated comparator kind became unreachable")
```

Implement `MetricComparator.__post_init__` so each kind admits only its exact
target/bound/direction/strictness combination. Validate every ordinary operand
with `isinstance(value, Real) and not isinstance(value, (bool, np.bool_))` plus
`math.isfinite`; tolerance is nonnegative. Expected positive infinity requires
no target/bound, direction `positive_infinity`, inclusive strictness, and zero
tolerance. `MetricRecord.__post_init__` validates nonempty strings and closed
theorem/origin fields, admits positive infinity only for that explicit
comparator, and installs the derived decision with `object.__setattr__`.
Normalize every admitted `numbers.Real` operand immediately with built-in
`float(value)`, then repeat the finite/extended-infinity check after conversion;
the stored record and comparator therefore contain no NumPy scalar, `Fraction`,
Boolean, or other non-JSON numeric subtype. Serialization never emits a raw
nonfinite JSON number: positive infinity is represented only by its closed tag.

Keep `target_metric(value, tolerance, *, target, applicability_reason,
interpretation, theorem_status, claim_origin)` and
`lower_bounded_metric(value, tolerance, *, lower_bound, applicability_reason,
interpretation, theorem_status, claim_origin)` as compatibility factories, but
remove `verification_state`. Add analogous `upper_bounded_metric` with
`upper_bound`, `strict_lower_bounded_metric` with `lower_bound`,
`expected_positive_infinity_metric`, and `inapplicable_metric`. Factories only
construct the validated public types; none computes or accepts a state.

- [ ] **Step 4: Run local contract GREEN and static checks**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_experiment_support.py -k "metric or producer" -q -p no:cacheprovider --basetemp=.pytest-wave-b-task1-green
C:\Python314\python.exe -m ruff check --no-cache src/multiagent_elbo/experiment_support.py tests/test_experiment_support.py
C:\Python314\python.exe -m ruff format --check --no-cache src/multiagent_elbo/experiment_support.py tests/test_experiment_support.py
```

This is deliberately a local API-contract GREEN only. Do not run a repository-
wide metric/producer GREEN or global source scan until Task 7 has migrated every
producer and call site. In particular, the Task 7 alias identity test is not
present or collected in Task 1; no Task 1 assertion depends on a future module
migration.

- [ ] **Step 5: Commit the metric core**

```powershell
git add -- src/multiagent_elbo/experiment_support.py tests/test_experiment_support.py
git commit -m "feat: derive metric v2 decisions"
```

### Task 2: Enforce candidate-only producer carriers

**Closes:** `AUD-05`; completes the producer-state boundary needed by `AUD-04`.

**Files:**

- Modify: `src/multiagent_elbo/finite/agent_network.py`
- Modify: `src/multiagent_elbo/finite/counterexamples.py`
- Modify: `src/multiagent_elbo/finite/theory_oracles.py`
- Modify: `src/multiagent_elbo/geometry/holonomy_experiment.py`
- Modify: `src/multiagent_elbo/realizations/gaussian/confirmatory_analysis.py`
- Modify: `src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostics.py`
- Modify: `src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostic_experiment.py`
- Modify: `tests/test_agent_network.py`
- Modify: `tests/test_counterexamples.py`
- Modify: `tests/test_theory_oracles.py`
- Modify: `tests/test_holonomy_experiment.py`
- Modify: `tests/test_gaussian_confirmatory_analysis.py`
- Modify: `tests/test_gaussian_fixed_ray_diagnostics.py`
- Modify: `tests/test_gaussian_fixed_ray_diagnostic_experiment.py`
- Modify: `tests/test_shared_scientific_contracts.py`

**Closed carrier inventory and interfaces:**

```python
@dataclass(frozen=True)
class PremiseAssessment:
    claim_id: str
    satisfied: bool
    applicability_decision: Literal["pass", "inconclusive"]
    theorem_status: Literal["HYPOTHESIS"]
    claim_origin: Literal["APPLICATION_SPECIFIC"]
    reason: str
    verification_state: Literal["CANDIDATE"] = field(
        default="CANDIDATE", init=False
    )
```

Apply the same non-init field to every public producer carrier in this closed
inventory:

```python
PRODUCER_STATE_FIELDS = (
    (MetricRecord, "verification_state"),
    (PremiseAssessment, "verification_state"),
    (CandidateRecord, "verification_state"),
    (TwoScaleApplicationOracle, "application_verification_state"),
    (TheoremAssumptionRecord, "verification_state"),
    (HolonomyExperimentResult, "verification_state"),
)
```

This dataclass inventory is only one half of the closed carrier surface. The
dict-returning producers are frozen separately so `confirmatory_analysis.py`
and the fixed-model diagnostics cannot escape through dynamically built JSON:

```python
PRODUCER_PAYLOAD_FACTORIES = (
    ("src/multiagent_elbo/realizations/gaussian/confirmatory_analysis.py", "analyze_primary"),
    ("src/multiagent_elbo/realizations/gaussian/confirmatory_analysis.py", "analyze_holdout"),
    ("src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostics.py", "adjacent_support_certificate"),
    ("src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostics.py", "spectral_diagnostics"),
    ("src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostics.py", "diagnose_trajectory"),
    ("src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostics.py", "summarize_population"),
    ("src/multiagent_elbo/geometry/holonomy_experiment.py", "run_holonomy_experiment"),
)

PRODUCER_STATE_SOURCE_PATHS = (
    "src/multiagent_elbo/experiment_support.py",
    "src/multiagent_elbo/finite/agent_network.py",
    "src/multiagent_elbo/finite/agent_network_experiment.py",
    "src/multiagent_elbo/finite/counterexamples.py",
    "src/multiagent_elbo/finite/counterexample_experiment.py",
    "src/multiagent_elbo/finite/information_history_experiment.py",
    "src/multiagent_elbo/finite/scale_cocycle_experiment.py",
    "src/multiagent_elbo/finite/theory_oracles.py",
    "src/multiagent_elbo/finite/theory_oracle_experiment.py",
    "src/multiagent_elbo/geometry/holonomy_experiment.py",
    "src/multiagent_elbo/realizations/gaussian/confirmatory_analysis.py",
    "src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostics.py",
    "src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostic_experiment.py",
    "src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py",
)
```

Task 2 owns the seven payload factories and carrier definitions. Task 7 owns
the metric call sites and every persisted run payload. The shared AST test scans
all tracked `src/multiagent_elbo/**/*.py`, discovers dataclass fields, literal
mapping keys, and call keywords equal to `verification_state` or ending in
`_verification_state`, and requires every discovered path to be in
`PRODUCER_STATE_SOURCE_PATHS`. A newly discovered path fails until explicitly
classified; the inventory may not be weakened to a substring scan.

`TwoScaleApplicationOracle.application_verification_state` is therefore
`Literal["CANDIDATE"] = field(default="CANDIDATE", init=False)` despite its
prefixed name. Rename the calculation key
`mathematical_verification_state` to
`mathematical_assessment_decision` in `fixed_ray_diagnostics.py`,
`confirmatory_analysis.py`, and the diagnostic experiment's read/write schema.
Its closed values are `pass`, `fail`, and `inconclusive`; every surrounding
producer `verification_state` remains `CANDIDATE`. No compatibility alias for
the old key is emitted because it would violate the suffix invariant.

- [ ] **Step 1: Add this literal carrier-inventory RED test**

Add to `tests/test_shared_scientific_contracts.py`:

```python
import ast
import subprocess
from collections.abc import Mapping
from dataclasses import asdict, fields
from pathlib import Path
from types import MappingProxyType

from multiagent_elbo.experiment_support import MetricRecord
from multiagent_elbo.finite.agent_network import PremiseAssessment
from multiagent_elbo.finite.counterexamples import CandidateRecord
from multiagent_elbo.finite.theory_oracles import (
    TheoremAssumptionRecord,
    TwoScaleApplicationOracle,
)
from multiagent_elbo.geometry.holonomy_experiment import HolonomyExperimentResult


PRODUCER_STATE_FIELDS = (
    (MetricRecord, "verification_state"),
    (PremiseAssessment, "verification_state"),
    (CandidateRecord, "verification_state"),
    (TwoScaleApplicationOracle, "application_verification_state"),
    (TheoremAssumptionRecord, "verification_state"),
    (HolonomyExperimentResult, "verification_state"),
)
STATE_PRODUCER_MODULES = (
    "src/multiagent_elbo/finite/agent_network.py",
    "src/multiagent_elbo/finite/counterexamples.py",
    "src/multiagent_elbo/finite/theory_oracles.py",
    "src/multiagent_elbo/geometry/holonomy_experiment.py",
    "src/multiagent_elbo/realizations/gaussian/confirmatory_analysis.py",
    "src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostics.py",
    "src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostic_experiment.py",
)


def _walk_named_fields(value, path=()):
    if isinstance(value, Mapping):
        for key, nested in value.items():
            yield from _walk_named_fields(nested, (*path, str(key)))
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            yield from _walk_named_fields(nested, (*path, str(index)))
    elif path:
        yield path, value


def test_all_public_producer_state_fields_are_non_init_candidate_literals():
    for carrier, name in PRODUCER_STATE_FIELDS:
        member = next(item for item in fields(carrier) if item.name == name)
        assert member.init is False
        assert member.default == "CANDIDATE"


def test_no_production_source_emits_promoted_or_legacy_calculation_state():
    forbidden = (
        'verification_state="LLM_SUPPORTED"',
        'verification_state="EVIDENCE_VERIFIED"',
        'verification_state="REFUTED"',
        'verification_state="INCONCLUSIVE"',
        '"mathematical_verification_state"',
    )
    for relative in STATE_PRODUCER_MODULES:
        source = Path(relative).read_text(encoding="utf-8")
        assert all(token not in source for token in forbidden), relative


def _is_verification_state_name(name):
    return name == "verification_state" or name.endswith("_verification_state")


def test_producer_state_source_inventory_is_complete():
    raw = subprocess.check_output([
        "git", "ls-files", "-z", "--", "src/multiagent_elbo"
    ])
    tracked = tuple(
        Path(item.decode("utf-8"))
        for item in raw.split(b"\0") if item.endswith(b".py")
    )
    discovered = set()
    for path in tracked:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                names.append(node.target.id)
            elif isinstance(node, ast.keyword) and node.arg is not None:
                names.append(node.arg)
            elif isinstance(node, ast.Dict):
                names.extend(
                    key.value for key in node.keys
                    if isinstance(key, ast.Constant) and isinstance(key.value, str)
                )
            if any(_is_verification_state_name(name) for name in names):
                discovered.add(path.as_posix())
    assert discovered == set(PRODUCER_STATE_SOURCE_PATHS)


def assert_candidate_payload(payload):
    for path, value in _walk_named_fields(payload):
        if path[-1] == "verification_state" or path[-1].endswith(
            "_verification_state"
        ):
            assert value == "CANDIDATE", ".".join(path)


@pytest.mark.parametrize(
    "carrier_name",
    (
        "MetricRecord",
        "PremiseAssessment",
        "CandidateRecord",
        "TwoScaleApplicationOracle",
        "TheoremAssumptionRecord",
        "HolonomyExperimentResult",
    ),
)
def test_recursive_candidate_validation_covers_every_closed_carrier(
    carrier_name, producer_carrier_examples
):
    assert set(producer_carrier_examples) == {
        carrier.__name__ for carrier, _ in PRODUCER_STATE_FIELDS
    }
    carrier = producer_carrier_examples[carrier_name]
    frozen_payload = MappingProxyType(asdict(carrier))
    assert_candidate_payload(frozen_payload)
    assert tuple(_walk_named_fields(frozen_payload))


@pytest.mark.parametrize(
    "factory_name",
    (
        "analyze_primary",
        "analyze_holdout",
        "adjacent_support_certificate",
        "spectral_diagnostics",
        "diagnose_trajectory",
        "summarize_population",
        "run_holonomy_experiment",
    ),
)
def test_recursive_candidate_validation_covers_every_payload_factory(
    factory_name, producer_payload_examples
):
    assert set(producer_payload_examples) == {
        name for _, name in PRODUCER_PAYLOAD_FACTORIES
    }
    frozen_payload = MappingProxyType(dict(producer_payload_examples[factory_name]))
    assert_candidate_payload(frozen_payload)
    assert tuple(_walk_named_fields(frozen_payload))
```

Define the two fixtures in this test module from the already-valid, minimal
factory inputs used by the owning tests. They are test-only mappings with
exactly the six carrier names and seven payload-factory names above; no
production fixture API is introduced. The `Mapping` branch is mandatory so
`dict`, `MappingProxyType`, and any other read-only mapping implementation
receive identical recursive validation. Each owning behavioral test also wraps
its result in `MappingProxyType(asdict(result))` (or
`MappingProxyType(dict(payload))`) before calling `assert_candidate_payload`.

- [ ] **Step 2: Add literal behavioral RED controls to the owning tests**

Add to `tests/test_agent_network.py`:

```python
@pytest.mark.parametrize(
    "independent,satisfied,decision",
    [(True, True, "pass"), (False, False, "inconclusive")],
)
def test_fixed_channel_assessment_separates_calculation_from_verification(
    independent, satisfied, decision
):
    result = assess_fixed_channel_premise(recognition_independent=independent)
    assert result.satisfied is satisfied
    assert result.applicability_decision == decision
    assert result.verification_state == "CANDIDATE"
    with pytest.raises(TypeError, match="verification_state"):
        PremiseAssessment(
            claim_id=result.claim_id,
            satisfied=result.satisfied,
            applicability_decision=result.applicability_decision,
            theorem_status="HYPOTHESIS",
            claim_origin="APPLICATION_SPECIFIC",
            reason=result.reason,
            verification_state="EVIDENCE_VERIFIED",
        )
```

In `tests/test_counterexamples.py`, assert
`parameter_dependent_channel_witness(Fraction(1, 3)).verification_state ==
"CANDIDATE"` and that passing a tenth positional state argument now raises
`TypeError`. In `tests/test_theory_oracles.py`, iterate
`THEOREM_ASSUMPTION_MATRIX`, load
`tests/fixtures/two_scale_application_v1.json`
through `load_two_scale_application`, and pass both values through
`assert_candidate_payload(asdict(...))`. In `tests/test_holonomy_experiment.py`,
inspect the dataclass field and assert `HolonomyExperimentResult(...,
verification_state="EVIDENCE_VERIFIED", ...)` raises `TypeError` before any
run path is made.

For each payload returned by `adjacent_support_certificate`,
`spectral_diagnostics`, `diagnose_trajectory`, `summarize_population`,
`analyze_primary`, and `analyze_holdout`, add:

```python
assert_candidate_payload(payload)
assert "mathematical_verification_state" not in repr(payload)
for path, value in _walk_named_fields(payload):
    if path[-1] == "mathematical_assessment_decision":
        assert value in {"pass", "fail", "inconclusive"}
```

The diagnostic-experiment round-trip test must also assert the new key survives
serialization/loading and the removed key is rejected as an unknown field.

- [ ] **Step 3: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_agent_network.py tests\test_counterexamples.py tests\test_theory_oracles.py tests\test_holonomy_experiment.py tests\test_gaussian_confirmatory_analysis.py tests\test_gaussian_fixed_ray_diagnostics.py tests\test_gaussian_fixed_ray_diagnostic_experiment.py tests\test_shared_scientific_contracts.py -k "premise or candidate or verification_state or assessment_decision or producer_state" -q -p no:cacheprovider --basetemp=.pytest-wave-b-task2-red
```

Expected: FAIL on the current `EVIDENCE_VERIFIED`/`INCONCLUSIVE` producer values.

- [ ] **Step 4: Implement immutable candidate fields and separate decisions**

Delete producer-side verification-state enums containing promoted or terminal
states. Keep those values only in external verification tooling. Preserve
theorem status and claim origin. Update positional carrier construction to named
arguments so removing the state input cannot silently shift later fields. Make
the diagnostic loaders closed-schema and reject rather than alias the old key.

- [ ] **Step 5: Run GREEN and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_agent_network.py tests\test_counterexamples.py tests\test_theory_oracles.py tests\test_holonomy_experiment.py tests\test_gaussian_confirmatory_analysis.py tests\test_gaussian_fixed_ray_diagnostics.py tests\test_gaussian_fixed_ray_diagnostic_experiment.py tests\test_shared_scientific_contracts.py -k "premise or candidate or verification_state or assessment_decision or producer_state" -q -p no:cacheprovider --basetemp=.pytest-wave-b-task2-green
rg -n 'verification_state\s*=\s*"(LLM_SUPPORTED|EVIDENCE_VERIFIED|REFUTED|INCONCLUSIVE)"|"mathematical_verification_state"' src/multiagent_elbo/finite/agent_network.py src/multiagent_elbo/finite/counterexamples.py src/multiagent_elbo/finite/theory_oracles.py src/multiagent_elbo/geometry/holonomy_experiment.py src/multiagent_elbo/realizations/gaussian/confirmatory_analysis.py src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostics.py src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostic_experiment.py
git add -- src/multiagent_elbo/finite/agent_network.py src/multiagent_elbo/finite/counterexamples.py src/multiagent_elbo/finite/theory_oracles.py src/multiagent_elbo/geometry/holonomy_experiment.py src/multiagent_elbo/realizations/gaussian/confirmatory_analysis.py src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostics.py src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostic_experiment.py tests/test_agent_network.py tests/test_counterexamples.py tests/test_theory_oracles.py tests/test_holonomy_experiment.py tests/test_gaussian_confirmatory_analysis.py tests/test_gaussian_fixed_ray_diagnostics.py tests/test_gaussian_fixed_ray_diagnostic_experiment.py tests/test_shared_scientific_contracts.py
git commit -m "fix: reserve claim promotion for ledgers"
```

The scoped `rg` command must return exit code 1 with no matches. Any match is
a failed GREEN, not an allowlisted exception. The repository-wide source scan
is intentionally deferred until Task 7 has migrated every metric producer,
serializer, and call site; Task 2 must not declare a global GREEN over Task 7's
still-live legacy call sites.

### Task 3: Make RNG provenance immutable

**Closes:** `AUD-12`.

**Files:**

- Modify: `src/multiagent_elbo/runtime.py`
- Modify: `tests/test_runtime.py`

**Exact interface:**

```python
@dataclass(frozen=True, init=False)
class RngStreams:
    seed: int
    problem: np.random.Generator
    recognition: np.random.Generator
    controls: np.random.Generator
    figures: np.random.Generator
    _spawn_key_items: tuple[tuple[str, tuple[int, ...]], ...]

    @classmethod
    def from_seed(cls, seed: int) -> "RngStreams": ...

    @property
    def spawn_keys(self) -> Mapping[str, tuple[int, ...]]:
        return MappingProxyType({name: key for name, key in self._spawn_key_items})

    def provenance(self) -> dict[str, object]:
        return {
            "seed": self.seed,
            "named_streams": {
                name: list(key) for name, key in self._spawn_key_items
            },
        }
```

- [ ] **Step 1: Add these mutation and draw-parity RED tests**

Add to `tests/test_runtime.py`:

```python
def test_rng_spawn_provenance_mutation_changes_neither_seed_material_nor_draws():
    seed = 314159
    stream_names = ("problem", "recognition", "controls", "figures")
    baseline_children = np.random.SeedSequence(seed).spawn(len(stream_names))
    expected_keys = {
        name: tuple(int(part) for part in child.spawn_key)
        for name, child in zip(stream_names, baseline_children, strict=True)
    }
    expected_draws = {
        name: np.random.default_rng(child).integers(0, 2**31, size=16)
        for name, child in zip(stream_names, baseline_children, strict=True)
    }

    streams = RngStreams.from_seed(seed)
    expected_provenance = {
        "seed": seed,
        "named_streams": {
            name: list(expected_keys[name]) for name in stream_names
        },
    }
    state_before = {
        name: copy.deepcopy(getattr(streams, name).bit_generator.state)
        for name in stream_names
    }
    exposed = streams.spawn_keys
    with pytest.raises(TypeError):
        exposed["problem"] = (99,)
    with pytest.raises(TypeError):
        del exposed["problem"]
    detached = dict(exposed)
    detached["problem"] = (99,)
    detached["added"] = (100,)
    exported = streams.provenance()
    exported["named_streams"]["problem"][0] = 99
    exported["named_streams"]["added"] = [100]

    assert streams.provenance() == expected_provenance
    assert dict(streams.spawn_keys) == expected_keys
    assert tuple(name for name, _ in streams._spawn_key_items) == stream_names
    assert all(isinstance(key, tuple) for _, key in streams._spawn_key_items)
    for name in stream_names:
        assert getattr(streams, name).bit_generator.state == state_before[name]
        np.testing.assert_array_equal(
            getattr(streams, name).integers(0, 2**31, size=16),
            expected_draws[name],
        )


@pytest.mark.parametrize("seed", [0, 1, 271828, 2**63 - 1])
def test_rng_refactor_matches_independent_seedsequence_oracle(seed):
    names = ("problem", "recognition", "controls", "figures")
    children = np.random.SeedSequence(seed).spawn(len(names))
    expected_keys = tuple(
        (name, tuple(int(part) for part in child.spawn_key))
        for name, child in zip(names, children, strict=True)
    )
    expected_draws = tuple(
        np.random.default_rng(child).random(8)
        for child in children
    )
    actual = RngStreams.from_seed(seed)
    assert actual._spawn_key_items == expected_keys
    for name, expected in zip(names, expected_draws, strict=True):
        np.testing.assert_array_equal(getattr(actual, name).random(8), expected)


@pytest.mark.parametrize("seed", [True, False, 1.0, "1", np.int64(1)])
def test_rng_seed_remains_exact_builtin_int(seed):
    with pytest.raises(TypeError, match="seed"):
        RngStreams.from_seed(seed)


def test_rng_direct_construction_is_not_a_spawn_key_injection_seam():
    with pytest.raises(TypeError):
        RngStreams()
```

Import `copy` in the test module. The oracle is deliberately constructed
directly from NumPy's public `SeedSequence.spawn` and `default_rng`, never
from a second `RngStreams` instance. Equality of bit-generator states before
and after every mapping/provenance mutation attempt proves the inspection path
does not consume a draw; the subsequent independent draw comparison proves the
seed material and stream assignment also remain unchanged.

- [ ] **Step 2: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_runtime.py -k "spawn or provenance" -q -p no:cacheprovider --basetemp=.pytest-wave-b-task3-red
```

Expected: FAIL because `spawn_keys` is currently a shared mutable dictionary.

- [ ] **Step 3: Store tuple items and expose only a read-only reconstruction**

`from_seed` validates with `type(seed) is int`, spawns in `_STREAM_NAMES`
order, allocates the `init=False` instance with `object.__new__(cls)`, and sets
all seven fields with `object.__setattr__`. Copy every
`SeedSequence.spawn_key` through `tuple(int(part) for part in child.spawn_key)`;
never retain a mapping or caller sequence. `provenance()` reconstructs fresh
lists from the tuple each time. Preserve current stream names and draws.

- [ ] **Step 4: Run GREEN and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_runtime.py -q -p no:cacheprovider --basetemp=.pytest-wave-b-task3-green
git add -- src/multiagent_elbo/runtime.py tests/test_runtime.py
git commit -m "fix: freeze RNG spawn provenance"
```

### Task 4: Resolve one canonical output root before identity or effects

**Closes:** `AUD-10`; supplies Wave C's `AUD-08` prerequisite.

**Files:**

- Create: `src/multiagent_elbo/output_paths.py`
- Create: `tests/test_output_paths.py`
- Modify: `src/multiagent_elbo/config.py`
- Modify: `src/multiagent_elbo/runtime.py`
- Modify: `tests/test_config.py`
- Modify: `tests/test_runtime.py`

**Interfaces:**

```python
@dataclass(frozen=True, slots=True)
class ResolvedOutputRoot:
    path: Path
    anchor: Path
    repo_root: Path
    theory_root: Path
    admission: Literal["external", "ignored_untracked_repo_descendant"]


@dataclass(frozen=True, slots=True)
class AuthorizedSourceDigestBinding:
    source_identity: AvailableSourceIdentity | UnavailableSourceIdentity
    excluded_output_roots: tuple[Path, ...]
    repo_root: Path
    theory_root: Path


def authorize_source_digest_binding(
    *,
    repo_root: Path,
    theory_root: Path,
    excluded_output_roots: Sequence[Path],
) -> AuthorizedSourceDigestBinding: ...


def resolve_output_root(
    root: Path | str,
    *,
    anchor: Path,
    repo_root: Path,
    theory_root: Path,
) -> ResolvedOutputRoot:
    """Return one normalized, policy-checked root plus its admission proof."""


def with_resolved_output_root(
    config: ExperimentConfig,
    *,
    anchor: Path,
    repo_root: Path,
    theory_root: Path,
) -> ExperimentConfig:
    if config._resolved_output_root is not None:
        existing = require_resolved_output_root(config)
        expected_anchor = anchor.resolve(strict=True)
        expected_repo = repo_root.resolve(strict=True)
        expected_theory = theory_root.resolve(strict=True)
        if (
            existing.anchor != expected_anchor
            or existing.repo_root != expected_repo
            or existing.theory_root != expected_theory
        ):
            raise ValueError("resolved output-root context mismatch")
        return config
    resolution = resolve_output_root(
        config.output.root,
        anchor=anchor,
        repo_root=repo_root,
        theory_root=theory_root,
    )
    return replace(
        config,
        output=replace(config.output, root=resolution.path),
        _resolved_output_root=resolution,
    )


def require_resolved_output_root(config: ExperimentConfig) -> ResolvedOutputRoot:
    """Reject unresolved/forged config-root disagreement at every consumer."""
    ...


def revalidate_resolved_output_root(
    config: ExperimentConfig,
) -> ResolvedOutputRoot:
    cached = require_resolved_output_root(config)
    return revalidate_output_root(cached)


def revalidate_output_root(
    cached: ResolvedOutputRoot,
) -> ResolvedOutputRoot:
    refreshed = resolve_output_root(
        cached.path,
        anchor=cached.anchor,
        repo_root=cached.repo_root,
        theory_root=cached.theory_root,
    )
    if refreshed != cached:
        raise ValueError("cached output-root admission is stale")
    return refreshed
```

The function is intentionally idempotent. A launcher and its public producer
may both call it with the same context and receive the same immutable config;
calling it with a different anchor/repository/Theory context rejects rather
than silently rebinding an already hashed configuration.

`ExperimentConfig` gains private field
`_resolved_output_root: ResolvedOutputRoot | None = field(default=None,
compare=False, repr=False)`. `from_dicts()` always sets it to `None` and
`canonical_config_json()` removes it before hashing. `require_resolved_output_root`
requires a non-`None` record, exact equality with `config.output.root`, absolute
normalized members, and the same repo/Theory nonoverlap invariant; it returns the
record without consulting CWD. `prepare_run_bundle`, legacy `RunStore.create`,
discovery, and figure publication all call this guard.

`require_resolved_output_root` validates the frozen record but is not a
time-of-check/time-of-use admission. Every effectful entry point calls
`revalidate_resolved_output_root` immediately before its first mkdir, lock,
journal, gate, worker, staging, or publication effect. The revalidation reruns
the full lexical/reparse/overlap/Git-ignore/tracked-descendant policy against
the cached absolute context and requires exact equality with the cached record.
It never accepts a cached admission merely because its dataclass fields agree.

`collect_provenance()` gains required keywords
`excluded_output_roots: Sequence[Path]` and
`authorized_source_binding: AuthorizedSourceDigestBinding`. It canonicalizes those values, requires
them to equal the resolved config root passed by the producer, records them as
sorted absolute strings in `source_digest_exclusions`, and excludes them from
status/untracked-content hashing. The source binding recomputes and authorizes
its Git-status, dirty-tree, Theory, and exclusion digests first. Only after that
authorization succeeds may the caller compute `config_sha256`; only after both
steps may it construct `RngStreams` or any execution identity.

- [ ] **Step 1: Write this real-Git fixture and literal root-policy RED matrix**

Add to `tests/test_output_paths.py`:

```python
def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


@pytest.fixture
def root_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.name", "Wave B Tests")
    _git(repo, "config", "user.email", "wave-b@example.invalid")
    (repo / ".gitignore").write_text("artifacts/\n", encoding="utf-8")
    (repo / "Theory").mkdir()
    (repo / "Theory/source.tex").write_text("theory\n", encoding="utf-8")
    (repo / "tracked.txt").write_text("tracked\n", encoding="utf-8")
    _git(repo, "add", ".gitignore", "Theory/source.tex", "tracked.txt")
    _git(repo, "commit", "-m", "fixture")
    return repo


def _snapshot(root: Path) -> dict[str, tuple[int, str]]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): (
            path.stat().st_size,
            hashlib.sha256(path.read_bytes()).hexdigest(),
        )
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_relative_root_uses_declared_anchor_not_cwd(root_repo, tmp_path, monkeypatch):
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    result = resolve_output_root(
        "artifacts", anchor=root_repo, repo_root=root_repo,
        theory_root=root_repo / "Theory"
    )
    assert result.path == (root_repo / "artifacts").resolve(strict=False)
    assert result.admission == "ignored_untracked_repo_descendant"
    assert not result.path.exists()


@pytest.mark.parametrize("spelling", ["outside", "./outside", "nested/../outside"])
def test_equivalent_safe_spellings_have_one_identity(root_repo, tmp_path, spelling):
    anchor = tmp_path / "anchor"
    anchor.mkdir(exist_ok=True)
    result = resolve_output_root(
        spelling, anchor=anchor, repo_root=root_repo,
        theory_root=root_repo / "Theory"
    )
    assert result.path == (anchor / "outside").resolve(strict=False)
    assert result.admission == "external"


@pytest.mark.parametrize("kind", ["equal", "contains", "contained"])
@pytest.mark.parametrize("protected", ["repo", "theory"])
def test_protected_root_overlap_rejects_without_effect(
    root_repo, tmp_path, kind, protected
):
    protected_root = root_repo if protected == "repo" else root_repo / "Theory"
    candidate = {
        "equal": protected_root,
        "contains": protected_root.parent,
        "contained": protected_root / "nested-output",
    }[kind]
    before = _snapshot(root_repo)
    with pytest.raises(ValueError, match="overlap|ignored"):
        resolve_output_root(
            candidate, anchor=tmp_path, repo_root=root_repo,
            theory_root=root_repo / "Theory"
        )
    assert _snapshot(root_repo) == before
    assert not (protected_root / "nested-output").exists()


def test_ignored_root_with_tracked_descendant_rejects(root_repo):
    tracked = root_repo / "artifacts/tracked.txt"
    tracked.parent.mkdir()
    tracked.write_text("tracked\n", encoding="utf-8")
    _git(root_repo, "add", "-f", "artifacts/tracked.txt")
    before = _snapshot(root_repo)
    with pytest.raises(ValueError, match="tracked"):
        resolve_output_root(
            tracked.parent, anchor=root_repo, repo_root=root_repo,
            theory_root=root_repo / "Theory"
        )
    assert _snapshot(root_repo) == before
```

Add separate symlink and Windows-junction tests which create the link only in
the test fixture before the snapshot, target `Theory`, and then execute the same
rejection/body assertion. If capability creation fails, skip with exactly
`capability unavailable: symbolic_link` or
`capability unavailable: windows_junction`. Add a nonexistent external-parent
case and assert neither candidate nor parent is created. These tests cover:

1. `Path("artifacts")` resolves under `anchor` after `monkeypatch.chdir()` moves elsewhere.
2. Absolute and equivalent dotted spellings return one identical normalized path.
3. Root equal to, containing, or contained by `theory_root` rejects.
4. Root equal to or containing `repo_root` rejects.
5. An in-repository descendant rejects unless `git check-ignore --no-index` succeeds and `git ls-files` returns zero tracked paths below it.
6. A tracked file beneath an otherwise ignored root rejects.
7. A symlink or Windows junction/reparse component that redirects into repo/Theory rejects.
8. A nonexistent safe external root validates without creating itself or its parent.
9. Every rejection leaves repo, Theory, and destination snapshots byte-identical.

- [ ] **Step 2: Add resolved-config/provenance RED controls**

Add to `tests/test_config.py` and `tests/test_runtime.py`:

```python
def test_hash_uses_resolved_root_but_not_private_resolution_metadata(config, roots):
    resolved = with_resolved_output_root(config, **roots)
    assert require_resolved_output_root(resolved).path == resolved.output.root
    assert "_resolved_output_root" not in canonical_config_json(resolved)
    assert config_sha256(resolved) == hashlib.sha256(
        canonical_config_json(resolved).encode("utf-8")
    ).hexdigest()
    with pytest.raises(ValueError, match="not resolved"):
        require_resolved_output_root(config)


def test_provenance_rejects_output_exclusion_mismatch(resolved_config, repo_root):
    binding = authorize_source_digest_binding(
        repo_root=repo_root,
        theory_root=repo_root / "Theory",
        excluded_output_roots=(resolved_config.output.root,),
    )
    config_hash = config_sha256(resolved_config)
    streams = RngStreams.from_seed(resolved_config.run.seed)
    with pytest.raises(ValueError, match="output root exclusion"):
        collect_provenance(
            repo_root,
            repo_root / "Theory",
            config_hash,
            streams,
            excluded_output_roots=(repo_root.parent / "different-output",),
            resolved_config=resolved_config,
            authorized_source_binding=binding,
        )


def test_cached_ignored_root_is_revalidated_before_effect(root_repo, config):
    resolved = with_resolved_output_root(
        config,
        anchor=root_repo,
        repo_root=root_repo,
        theory_root=root_repo / "Theory",
    )
    tracked = resolved.output.root / "late-tracked.txt"
    tracked.parent.mkdir(parents=True)
    tracked.write_text("late\n", encoding="utf-8")
    _git(root_repo, "add", "-f", tracked.relative_to(root_repo).as_posix())
    before = _snapshot(root_repo)
    with pytest.raises(ValueError, match="tracked|stale"):
        revalidate_resolved_output_root(resolved)
    assert _snapshot(root_repo) == before


def test_cached_external_root_rejects_late_reparse_without_effect(
    root_repo, tmp_path, config, reparse_factory
):
    external = tmp_path / "external"
    resolved = with_resolved_output_root(
        replace(config, output=replace(config.output, root=external / "out")),
        anchor=tmp_path,
        repo_root=root_repo,
        theory_root=root_repo / "Theory",
    )
    reparse_factory(external, root_repo / "Theory")
    before = _snapshot(root_repo)
    with pytest.raises(ValueError, match="reparse|stale"):
        revalidate_resolved_output_root(resolved)
    assert _snapshot(root_repo) == before
```

The reparse fixture uses the exact capability skip reasons from Step 1. Task 4
stops at resolver, frozen-config, provenance-binding, and revalidation GREEN;
it does not import or spy on future producers, renderers, or launchers. Task 7
owns the producer order spies after all producers migrate, Task 8 owns the
renderer order spies after `render_run` exists, Task 9 owns the launcher order
spies after all launchers migrate, and Task 10 checks their final closed
inventories. Each owning task uses the same domain order and zero-effect
negative semantics defined below.

Freeze the resulting signature as:

```python
def collect_provenance(
    repo_root: Path,
    theory_root: Path,
    config_hash: str,
    streams: RngStreams,
    *,
    excluded_output_roots: Sequence[Path],
    resolved_config: ExperimentConfig,
    authorized_source_binding: AuthorizedSourceDigestBinding,
) -> dict[str, object]:
    ...
```

- [ ] **Step 3: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_output_paths.py tests\test_config.py tests\test_runtime.py -k "output_root or exclusion or arbitrary_cwd or reparse" -q -p no:cacheprovider --basetemp=.pytest-wave-b-task4-red
```

Expected: FAIL because relative roots still depend on ambient CWD and overlap is accepted.

- [ ] **Step 4: Implement path and Git admission in this exact order**

1. Require `Path | str`; reject empty strings and NUL.
2. Resolve `anchor`, `repo_root`, and `theory_root` strictly and reject symlink/reparse components in them.
3. Anchor a relative `root` to `anchor`, then normalize with `resolve(strict=False)`.
4. Walk every existing lexical component with `lstat`; reject symlink tags and Windows `FILE_ATTRIBUTE_REPARSE_POINT`.
5. Reject equality/ancestor/descendant overlap with Theory.
6. Reject equality or ancestor overlap with repo.
7. For a descendant of repo only, run `git -C $repoRoot check-ignore -q --no-index -- $relativeRoot` and `git -C $repoRoot ls-files -z -- $relativeRoot`. Require ignore exit zero and empty tracked output.
8. Return the resolved path without creating anything.

Do not fall back to CWD, textual prefix checks, or `Path.is_symlink()` alone.

- [ ] **Step 5: Bind provenance exclusions**

Update `_dirty_tree_sha256()` and provenance tests so the admitted ignored root is explicitly recorded and remains absent from source/config digests. Reject a provenance/config mismatch where the recorded output root differs from `config.output.root`.
Treat `revalidate_resolved_output_root` as the only just-in-time admission
function: no producer, renderer, launcher, worker/gate wrapper, or publisher may
perform an effect after calling only `require_resolved_output_root`.

- [ ] **Step 6: Run GREEN, static checks, and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_output_paths.py tests\test_config.py tests\test_runtime.py -q -p no:cacheprovider --basetemp=.pytest-wave-b-task4-green
C:\Python314\python.exe -m ruff check --no-cache src/multiagent_elbo/output_paths.py src/multiagent_elbo/config.py src/multiagent_elbo/runtime.py tests/test_output_paths.py tests/test_config.py tests/test_runtime.py
C:\Python314\python.exe -m ruff format --check --no-cache src/multiagent_elbo/output_paths.py src/multiagent_elbo/config.py src/multiagent_elbo/runtime.py tests/test_output_paths.py tests/test_config.py tests/test_runtime.py
git add -- src/multiagent_elbo/output_paths.py src/multiagent_elbo/config.py src/multiagent_elbo/runtime.py tests/test_output_paths.py tests/test_config.py tests/test_runtime.py
git commit -m "feat: canonicalize output roots"
```

### Task 5: Prepare complete detached run bundles with zero effects

**Closes:** `AUD-04` fail-closed serialization and `AUD-11`; establishes the byte inventory required by `AUD-01`.

**Files:**

- Create: `src/multiagent_elbo/artifact_schema.py`
- Create: `tests/test_artifact_schema.py`
- Modify: `src/multiagent_elbo/artifacts.py`
- Modify: `tests/test_artifacts.py`

Use the exact public types and signatures frozen above; do not introduce a
second `PreparedRunBundle` shape. In particular, `artifacts` is a tuple, the
bundle has schema `prepared-run-bundle-v2`, and preparation accepts no path,
callback, serializer, or lazy value other than the already-resolved destination
inside `config`.

Import Wave A's sole storage boundary as `from ._immutable import immutable_array`. Preparation uses it for each detached canonical NPZ member before serialization, and loading uses it after parsing the verified in-memory NPZ buffer. Do not add a second read-only-array implementation.

Canonical NPZ dtype admission is exactly `bool` (`|b1`), little-endian signed `int64` (`<i8`), little-endian `float64` (`<f8`), and little-endian `complex128` (`<c16`). Every array name is one portable ASCII segment using `[A-Za-z0-9][A-Za-z0-9._-]*`, is unique after case-folding, and is not a Windows reserved basename. Arrays must be nonempty, C-contiguous, and own a detached canonical copy before serialization. The sole closed policy is `finite`; real and imaginary components must both be finite. NaN and either infinity are forbidden in NPZ, so no unpersisted per-member exception policy exists. Tagged positive infinity remains available only in strict `metric-record-v2` JSON. Object, structured, datetime, timedelta, Unicode, byte-string, void, and pickle-dependent dtypes reject.

- [ ] **Step 1: Add exact fixtures and closed-name/value RED tests**

Add these helpers to `tests/test_artifact_schema.py`:

```python
def _prepared_inputs(tmp_path):
    root = tmp_path / "outside" / "runs"
    config = make_config(root)
    config = with_resolved_output_root(
        config,
        anchor=Path.cwd(),
        repo_root=Path.cwd(),
        theory_root=Path.cwd() / "Theory",
    )
    source_identity = source_identity_payload(parse_source_identity({
        "status": "available",
        "git_commit": "a" * 40,
        "git_dirty": False,
        "git_status_sha256": "b" * 64,
        "dirty_tree_sha256": "c" * 64,
        "theory_sha256": "d" * 64,
    }))
    config_hash = config_sha256(config)
    provenance = {
        "config_hash": config_hash,
        "source_identity": source_identity,
        "source_digest_exclusions": [str(config.output.root)],
    }
    payloads = RunPayloads(
        artifact_kind="test_bundle",
        json_payloads={
            "metrics.json": {
                "verification_state": "CANDIDATE",
                "values": [1, 2],
            }
        },
        npz_payloads={
            "arrays.npz": {
                "values": NpzArrayInput(
                    np.array([[1.0, 2.0]], dtype="<f8"), "finite"
                )
            }
        },
    )
    return config, provenance, payloads


INVALID_ARTIFACT_NAMES = (
    "", ".", "..", "../x.json", "x/y.json", "x\\y.json",
    "/x.json", "C:/x.json", "C:\\x.json", "x.json:stream",
    "x.json.", "x.json ", "CON.json", "nul.npz", "manifest.json",
    "incomplete-run-v1.json", "é.json",
)


@pytest.mark.parametrize("name", INVALID_ARTIFACT_NAMES)
def test_prepare_rejects_nonportable_artifact_name_before_parent(tmp_path, name):
    config, provenance, payloads = _prepared_inputs(tmp_path)
    payloads = RunPayloads("test_bundle", {name: {}}, {})
    with pytest.raises((TypeError, ValueError), match="artifact name"):
        prepare_run_bundle(config, provenance, payloads)
    assert not config.output.root.exists()


@pytest.mark.parametrize(
    "left,right", [("Metrics.json", "metrics.JSON"), ("A.npz", "a.NPZ")]
)
def test_prepare_rejects_case_aliases(tmp_path, left, right):
    config, provenance, _ = _prepared_inputs(tmp_path)
    payloads = RunPayloads("test_bundle", {left: {}, right: {}}, {})
    with pytest.raises(ValueError, match="case-fold"):
        prepare_run_bundle(config, provenance, payloads)
    assert not config.output.root.exists()


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_prepare_rejects_extended_json_numbers(tmp_path, value):
    config, provenance, _ = _prepared_inputs(tmp_path)
    with pytest.raises(ValueError, match="JSON|finite"):
        prepare_run_bundle(
            config, provenance,
            RunPayloads("test_bundle", {"bad.json": {"value": value}}, {}),
        )
    assert not config.output.root.exists()


INVALID_ARRAYS = (
    np.array([object()], dtype=object),
    np.array([(1, 2.0)], dtype=[("a", "<i8"), ("b", "<f8")]),
    np.array(["2026-08-11"], dtype="datetime64[D]"),
    np.array([1], dtype="timedelta64[D]"),
    np.array(["x"], dtype="U1"),
    np.array([b"x"], dtype="S1"),
    np.array([1], dtype="<i4"),
    np.array([1.0], dtype="<f4"),
    np.array([1.0], dtype=">f8"),
    np.array([], dtype="<f8"),
    np.arange(8, dtype="<f8")[::2],
)


INVALID_ARRAY_IDS = (
    "object", "structured", "datetime", "timedelta", "unicode", "bytes",
    "int32", "float32", "big-endian-float64", "empty", "noncontiguous",
)


@pytest.mark.parametrize("array", INVALID_ARRAYS, ids=INVALID_ARRAY_IDS)
def test_prepare_rejects_noncanonical_npz_array(tmp_path, array):
    config, provenance, _ = _prepared_inputs(tmp_path)
    payloads = RunPayloads(
        "test_bundle", {}, {"bad.npz": {"x": NpzArrayInput(array)}}
    )
    with pytest.raises((TypeError, ValueError), match="array|dtype|contiguous|empty"):
        prepare_run_bundle(config, provenance, payloads)
    assert not config.output.root.exists()


@pytest.mark.parametrize(
    "value,policy",
    [
        (math.nan, "finite"),
        (math.inf, "finite"),
        (-math.inf, "finite"),
        (math.inf, "finite_or_positive_infinity"),
        (1.0, "finite_or_positive_infinity"),
        (1.0, "unknown"),
    ],
    ids=(
        "nan-rejected", "positive-infinity-rejected",
        "negative-infinity-rejected", "old-exception-policy-rejected",
        "finite-value-with-old-policy-rejected", "unknown-policy-rejected",
    ),
)
def test_npz_finiteness_policy_is_closed(tmp_path, value, policy):
    config, provenance, _ = _prepared_inputs(tmp_path)
    payloads = RunPayloads(
        "test_bundle", {},
        {"values.npz": {"x": NpzArrayInput(np.array([value], dtype="<f8"), policy)}},
    )
    with pytest.raises((TypeError, ValueError), match="finite|policy"):
        prepare_run_bundle(config, provenance, payloads)
    assert not config.output.root.exists()
```

Also parameterize malformed available/unavailable source unions (Boolean digest,
abbreviated revision, extra/missing key, empty unavailable reason), mismatched
config/provenance hash, mismatched exclusion, unknown producer verification
state, and an invalid embedded `metric-record-v2`. Add an explicit typed
source-identity matrix that round-trips both
`AvailableSourceIdentity -> source_identity_payload -> parse_source_identity`
and `UnavailableSourceIdentity -> source_identity_payload ->
parse_source_identity`, then rejects a raw mapping passed where a typed
identity is required, Boolean digest/revision values, abbreviated/mixed-case
digests, extra/missing keys, empty reasons, wrong status tags, and an
unavailable identity carrying available-only fields. Each case uses
`_prepared_inputs`, calls `prepare_run_bundle`, and asserts the root remains
absent.

- [ ] **Step 2: Add the exact detach, deterministic-order, and zero-I/O RED controls**

The required detach control is:

```python
json_payload = {"nested": {"values": [1, 2], "verification_state": "CANDIDATE"}}
array = np.array([[1.0, 2.0]], dtype=np.float64)
payloads = RunPayloads(
    artifact_kind="test_bundle",
    json_payloads={"metrics.json": json_payload},
    npz_payloads={
        "arrays.npz": {"values": NpzArrayInput(array, "finite")}
    },
)
prepared = prepare_run_bundle(config, provenance, payloads)
prepared_snapshot = tuple((item.name, item.content, item.sha256) for item in prepared.artifacts)
json_payload["nested"]["values"][0] = 99
json_payload["nested"]["added"] = True
array[0, 0] = 99.0
assert tuple((item.name, item.content, item.sha256) for item in prepared.artifacts) == prepared_snapshot
```

Task 5 stops at the immutable prepared-byte assertion. Do not call
`publish_run_bundle` or either v2 loader before Task 6 implements those APIs.
Task 6 repeats this fixture through publication and loading after the APIs
exist.

Parameterize the mutation over the outer JSON mapping, nested mapping/list,
outer NPZ mapping, member mapping, and original array. Preparation must retain
none. Construct the same logical payload with reversed insertion order and
assert equality of the complete prepared artifact tuple and manifest bytes.
Then inspect each `.npz` buffer with `zipfile.ZipFile`: member names are sorted
ASCII, each timestamp is `(1980, 1, 1, 0, 0, 0)`, compression is
`ZIP_STORED`, external attributes are zero, and each member is an NPY v2.0
buffer. Also require an empty ZIP comment, empty member comments/extras, no
directory/encrypted/data-descriptor members, portable case-fold-unique base
names, exact canonical dtype strings, `fortran_order is False`, nonempty
integer shapes, and byte-for-byte equality after canonical reserialization of
every NPY member and the complete ZIP in observed central-directory order.

For the representative malformed JSON and NPZ cases add:

```python
@pytest.mark.parametrize("kind", ["json", "npz"])
def test_prepare_failure_calls_no_filesystem_writer(tmp_path, monkeypatch, kind):
    config, provenance, _ = _prepared_inputs(tmp_path)
    payloads = (
        RunPayloads("test_bundle", {"bad.json": {"x": math.nan}}, {})
        if kind == "json"
        else RunPayloads(
            "test_bundle", {},
            {"bad.npz": {"x": NpzArrayInput(np.array([object()], dtype=object))}},
        )
    )
    monkeypatch.setattr(Path, "mkdir", lambda *a, **k: pytest.fail("mkdir called"))
    monkeypatch.setattr(tempfile, "NamedTemporaryFile", lambda *a, **k: pytest.fail("tempfile called"))
    monkeypatch.setattr(builtins, "open", lambda *a, **k: pytest.fail("open called"))
    with pytest.raises((TypeError, ValueError)):
        prepare_run_bundle(config, provenance, payloads)
```

- [ ] **Step 3: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_artifact_schema.py tests\test_artifacts.py -k "prepare or manifest_v2 or npz or json or candidate_state" -q -p no:cacheprovider --basetemp=.pytest-wave-b-task5-red
```

Expected: FAIL because no pure preparation layer exists and legacy `write_npz` accepts unreadable object arrays.

- [ ] **Step 4: Implement canonical serialization from detached values**

Use one JSON encoder everywhere:

```python
def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def strict_json_from_bytes(content: bytes) -> object:
    def reject_constant(token: str) -> NoReturn:
        raise ValueError(f"nonfinite JSON token: {token}")

    def closed_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    parsed = json.loads(
        content.decode("ascii"),
        parse_constant=reject_constant,
        object_pairs_hook=closed_object,
    )

    def reject_nonfinite(value: object) -> None:
        if type(value) is float and not math.isfinite(value):
            raise ValueError("nonfinite JSON number")
        if type(value) is dict:
            for nested in value.values():
                reject_nonfinite(nested)
        elif type(value) is list:
            for nested in value:
                reject_nonfinite(nested)

    reject_nonfinite(parsed)
    return parsed
```

Every JSON reader uses `strict_json_from_bytes`; plain `json.loads` is
forbidden on authoritative bytes. RED tests inject duplicate keys at the root
and nested levels plus literal `NaN`, `Infinity`, `-Infinity`, `1e999`,
and `-1e999` into `manifest.json`, `config.json`, `provenance.json`, and an ordinary JSON
payload. Each must reject before parsing any dependent payload and without
changing the source or destination inventory.

Serialize NPZ to `io.BytesIO` only after validation and detached canonical copying. Build `PreparedArtifact` records from those exact bytes. Serialize `config.json` as `{"schema_version":"run-config-v2","config_hash":config_hash,"resolved_config":resolved_config}` and `provenance.json` as `{"schema_version":"run-provenance-v2","record":provenance}`. Build the manifest from the finished artifact records; do not include `manifest.json` in its inventory.

Use this deterministic member writer; do not call `np.savez`:

```python
def canonical_npz_bytes(arrays: Mapping[str, np.ndarray]) -> bytes:
    target = io.BytesIO()
    with zipfile.ZipFile(target, mode="w", compression=zipfile.ZIP_STORED) as archive:
        for name in sorted(arrays, key=lambda value: value.encode("ascii")):
            npy = io.BytesIO()
            np.lib.format.write_array(
                npy, arrays[name], version=(2, 0), allow_pickle=False
            )
            info = zipfile.ZipInfo(f"{name}.npy", (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 0
            info.external_attr = 0
            archive.writestr(info, npy.getvalue())
    return target.getvalue()
```

Recursively require `CANDIDATE` for any JSON key equal to `verification_state` or ending `_verification_state`. Validate every embedded `metric-record-v2` with `load_metric_record()` before preparation returns.

`parse_source_identity` is the sole nested-union constructor. It accepts an
exact built-in `dict` only at the serialized boundary, checks the literal key
set and scalar types before constructing one of the two typed dataclasses, and
never converts malformed data to unavailable. `source_identity_payload`
accepts only those exact dataclass types and emits a fresh built-in dictionary.
`PreparedRunBundle.source_identity`, the parsed provenance member, and the
manifest member must all be the same typed value; their serialized payloads
must compare equal byte-for-byte after canonical encoding.

- [ ] **Step 5: Label the incremental API as legacy**

Retain `RunStore.create/write_json/write_npz/finalize` only for explicit v1 compatibility tests. Set `schema_version="legacy-run-manifest-v1"` on those handles, emit `DeprecationWarning` from `create`, and reject calling incremental methods on a v2 handle. No production module may call the legacy methods after Task 7.

- [ ] **Step 6: Run GREEN and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_artifact_schema.py tests\test_artifacts.py -k "prepare or manifest_v2 or npz or json or candidate_state or legacy" -q -p no:cacheprovider --basetemp=.pytest-wave-b-task5-green
C:\Python314\python.exe -m ruff check --no-cache src/multiagent_elbo/artifact_schema.py src/multiagent_elbo/artifacts.py tests/test_artifact_schema.py tests/test_artifacts.py
C:\Python314\python.exe -m ruff format --check --no-cache src/multiagent_elbo/artifact_schema.py src/multiagent_elbo/artifacts.py tests/test_artifact_schema.py tests/test_artifacts.py
git add -- src/multiagent_elbo/artifact_schema.py src/multiagent_elbo/artifacts.py tests/test_artifact_schema.py tests/test_artifacts.py
git commit -m "feat: prepare detached run bundles"
```

### Task 6: Publish, verify, and version-dispatch run bundles

**Closes:** `AUD-01` run-bundle integrity; completes `AUD-11` reader/writer parity.

**Files:**

- Modify: `src/multiagent_elbo/artifacts.py`
- Modify: `src/multiagent_elbo/artifact_schema.py`
- Modify: `src/multiagent_elbo/__init__.py`
- Modify: `tests/test_artifact_schema.py`
- Modify: `tests/test_artifacts.py`

**Additional exact result schemas:** the `ArtifactInventoryEntry`,
`LegacyObservation`, `VerifiedRunBundle`, and `LegacyObservedBundle` definitions
in **Frozen Public Schemas and Interfaces** are the only definitions. Task 6
implements those declarations verbatim and must not redeclare, widen, or shadow
them.

All mappings are `MappingProxyType`; all sequences are tuples; parsed authoritative arrays pass through Wave A's `immutable_array`. `source_claim_eligible` is true only for the `available` v2 source-identity member.

Run publication also has this closed private, parent-side ownership record. It
is not a public carrier and never appears inside the final run:

```python
RUN_PUBLICATION_JOURNAL_KEYS = {
    "schema_version", "owner_token", "phase", "stage_name", "final_name",
    "prepared_manifest_sha256",
}
RUN_INCOMPLETE_MARKER_KEYS = {
    "schema_version", "owner_token", "journal_name", "stage_name",
    "final_name", "prepared_manifest_sha256",
}
RUN_PUBLICATION_JOURNAL_PHASES = (
    "staging", "ready_to_install", "installed",
)
RUN_PUBLICATION_RECOVERY_TABLE = {
    "staging": ("journal_only", "owned_stage_with_marker"),
    "ready_to_install": (
        "owned_complete_stage_with_marker",
        "owned_complete_stage_without_marker",
        "installed_final",
    ),
    "installed": ("installed_final",),
}
```

For final name `$runName` and a fresh 32-byte lowercase-hex `$ownerToken`, the
stage is `.$runName.$ownerToken.staging` and the journal is
`.$runName.$ownerToken.publication-journal.json`, both direct children of the
same resolved parent. The incomplete marker and journal repeat those exact
names, token, and SHA-256 of `prepared.manifest_bytes`. Journal schema is
`run-publication-journal-v1`; marker schema is `incomplete-run-v1`. Every
journal create/rewrite uses an owned sibling temp, atomic replace, file fsync,
and parent-directory fsync. The journal is durable before stage creation and is
retained across marker removal and stage rename.

Freeze `ArtifactInventoryEntry` as a frozen slots dataclass with fields
`name`, `kind`, `size_bytes`, and `sha256`. Freeze legacy observation root keys
as exactly `schema_version`, `observed_at_revision`, `files`, `legacy_schema`,
and `limitations`; each file has exactly `name`, `kind`, `size_bytes`, and
`sha256`, where kind is `json`, `npz`, or `bytes`. The v2 loader never returns
`LegacyObservedBundle`; the dispatch loader never infers legacy from an unknown
nonempty schema.

- [ ] **Step 1: Add literal publication-boundary RED tests**

Freeze the private test seam, not the public signature:

```python
PublishRunBoundary = Literal[
    "after_stage_mkdir",
    "after_marker_fsync",
    "after_each_artifact_fsync",
    "after_stage_readback",
    "before_manifest_write",
    "after_manifest_fsync",
    "after_stage_manifest_dir_fsync",
    "before_marker_remove",
    "after_marker_remove",
    "after_marker_remove_dir_fsync",
    "before_stage_rename",
    "after_stage_rename",
    "after_parent_fsync",
]


def _publish_run_bundle(
    prepared: PreparedRunBundle,
    *,
    fault_injector: Callable[[PublishRunBoundary, str | None], None] | None,
) -> RunStore: ...
```

Add this parameterized control to `tests/test_artifact_schema.py`:

```python
PRE_RENAME_BOUNDARIES = (
    "after_stage_mkdir", "after_marker_fsync",
    "after_each_artifact_fsync", "after_stage_readback",
    "before_manifest_write", "after_manifest_fsync",
    "after_stage_manifest_dir_fsync", "before_marker_remove",
    "after_marker_remove", "after_marker_remove_dir_fsync",
    "before_stage_rename",
)


@pytest.mark.parametrize("boundary", PRE_RENAME_BOUNDARIES)
def test_publication_exception_before_rename_leaves_no_run_or_stage(
    tmp_path, boundary
):
    prepared = _prepare_valid_bundle(tmp_path)
    def fail(actual, name):
        if actual == boundary:
            raise InjectedFailure(f"{actual}:{name}")
    with pytest.raises(InjectedFailure):
        artifact_schema._publish_run_bundle(prepared, fault_injector=fail)
    assert not prepared.run_dir.exists()
    assert not list(prepared.run_dir.parent.glob(f".{prepared.run_dir.name}.*.staging"))
    assert not list(prepared.run_dir.parent.glob(
        f".{prepared.run_dir.name}.*.publication-journal.json"
    ))


@pytest.mark.parametrize("boundary", ["after_stage_rename", "after_parent_fsync"])
def test_exception_after_atomic_install_leaves_complete_consumable_run(
    tmp_path, boundary
):
    prepared = _prepare_valid_bundle(tmp_path)
    def fail(actual, name):
        if actual == boundary:
            raise InjectedFailure(actual)
    with pytest.raises(InjectedFailure):
        artifact_schema._publish_run_bundle(prepared, fault_injector=fail)
    assert load_verified_run_bundle(prepared.run_dir).manifest["status"] == "complete"
    assert not list(prepared.run_dir.parent.glob(
        f".{prepared.run_dir.name}.*.publication-journal.json"
    ))


@pytest.mark.parametrize(
    "boundary",
    PRE_RENAME_BOUNDARIES + ("after_stage_rename", "after_parent_fsync"),
)
def test_process_crash_recovery_at_every_publication_boundary(
    tmp_path, boundary
):
    prepared_fixture = write_subprocess_prepared_fixture(tmp_path)
    foreign_stage = prepared_fixture.run_parent / ".foreign-owner.staging"
    foreign_stage.mkdir()
    (foreign_stage / "foreign.txt").write_bytes(b"foreign\n")
    foreign_before = recursive_file_inventory(foreign_stage)
    result = run_crashing_publisher(prepared_fixture, boundary)
    assert result.returncode == CRASH_EXIT_CODE
    assert prepared_fixture.expected_journal.is_file()
    journal = strict_json_from_bytes(prepared_fixture.expected_journal.read_bytes())
    assert set(journal) == RUN_PUBLICATION_JOURNAL_KEYS
    assert journal["phase"] == (
        "staging" if boundary in {
            "after_stage_mkdir", "after_marker_fsync",
            "after_each_artifact_fsync", "after_stage_readback",
            "before_manifest_write", "after_manifest_fsync",
            "after_stage_manifest_dir_fsync",
        } else "ready_to_install"
    )
    if boundary == "before_marker_remove":
        assert prepared_fixture.expected_marker.is_file()
    if boundary in {
        "after_marker_remove", "after_marker_remove_dir_fsync",
        "before_stage_rename", "after_stage_rename", "after_parent_fsync",
    }:
        assert not prepared_fixture.expected_marker.exists()
    recovered = recover_owned_run_publication(prepared_fixture.run_parent)
    if boundary in {"after_stage_rename", "after_parent_fsync"}:
        assert load_verified_run_bundle(prepared_fixture.run_dir)
        assert recovered == ()
    else:
        assert not prepared_fixture.run_dir.exists()
        assert recovered == (prepared_fixture.expected_stage,)
        assert not prepared_fixture.expected_stage.exists()
    assert not prepared_fixture.expected_journal.exists()
    assert recursive_file_inventory(foreign_stage) == foreign_before


def test_prepared_snapshot_is_detached_through_publish_and_load(tmp_path):
    prepared, json_payload, array = _prepare_mutable_source_bundle(tmp_path)
    snapshot = tuple(
        (item.name, item.content, item.size_bytes, item.sha256)
        for item in prepared.artifacts
    )
    json_payload["nested"]["values"][0] = 99
    array[0, 0] = 99.0
    published = publish_run_bundle(prepared)
    verified = load_verified_run_bundle(published.run_dir)
    assert tuple(
        (item.name, item.content, item.size_bytes, item.sha256)
        for item in prepared.artifacts
    ) == snapshot
    assert verified.json_payloads["metrics.json"]["nested"]["values"] == (1, 2)
    np.testing.assert_array_equal(
        verified.npz_payloads["arrays.npz"]["values"],
        np.array([[1.0, 2.0]], dtype="<f8"),
    )
```

Count `after_each_artifact_fsync` calls and inject once at every artifact index.
Spy on `fsync` and require the staging directory descriptor immediately after
marker unlink, the final-parent directory descriptor immediately after rename,
and the parent descriptor after every journal create/rewrite/removal. Spy on
journal phase writes and require exactly `staging`, `ready_to_install`, and
`installed` on ordinary success, followed by journal unlink and parent fsync.
The subprocess helper exits with `os._exit(CRASH_EXIT_CODE)` from the same
literal boundary seam, so exception cleanup cannot mask crash behavior. The
fixture exposes `expected_journal` and `expected_marker` derived from its
recorded owner token; it does not discover either path by globbing after the
crash.

`recover_owned_run_publication` enumerates only canonical parent journals, not
staging directories. It validates `RUN_PUBLICATION_JOURNAL_KEYS`, canonical
bytes, token/name relations, manifest digest, phase, and exactly one row of
`RUN_PUBLICATION_RECOVERY_TABLE` before touching anything. In `staging`, it may
remove only the named stage with the matching marker. In `ready_to_install`, it
may remove only the named, byte-verified complete stage whether the marker is
still present or already durably absent; if rename already installed the exact
final, it validates that final and leaves it. In `installed`, it requires the
exact final and no stage. It then removes only the validated journal and fsyncs
the parent. A missing/malformed journal, two journals targeting one final,
phase/filesystem mismatch, foreign stage, or unjournaled stage is untouched and
fails closed; recovery never guesses ownership from a stage name or marker
alone. The three crash boundaries `after_marker_remove`,
`after_marker_remove_dir_fsync`, and `before_stage_rename` therefore remain
recoverable because their `ready_to_install` journal is already durable.
Record calls to `_write_owned_bytes` and assert `manifest.json` is last. Prepare,
then monkeypatch `canonical_json_bytes`, `canonical_npz_bytes`, and
`canonical_config_json` to raise; `publish_run_bundle(prepared)` must still
succeed because it writes only prepared buffers. Existing complete and
incomplete finals both reject before a sibling exists. A staging crash marker
must be rejected by discovery/load as incomplete.

- [ ] **Step 2: Add literal v2 tamper and read-once RED tests**

Add this closed mutation table and apply each mutation to a copied valid run:

```python
TAMPER_CASES = (
    ("missing_artifact", "run inventory is missing"),
    ("extra_artifact", "unexpected filesystem entry"),
    ("unknown_manifest_key", "unknown manifest field"),
    ("missing_manifest_key", "missing manifest field"),
    ("duplicate_inventory_name", "duplicate artifact name"),
    ("case_alias", "case-fold"),
    ("size", "size"),
    ("sha256", "sha256"),
    ("config_identity", "config identity"),
    ("source_identity", "source identity"),
    ("metric_decision", "assessment_decision"),
    ("pickle_npz", "pickle|dtype"),
)


@pytest.mark.parametrize(
    "mutation,message", TAMPER_CASES, ids=tuple(case[0] for case in TAMPER_CASES)
)
def test_v2_loader_rejects_closed_tamper_matrix(valid_run_copy, mutation, message):
    apply_manifest_v2_tamper(valid_run_copy, mutation)
    with pytest.raises((TypeError, ValueError), match=message):
        load_verified_run_bundle(valid_run_copy)
```

`apply_manifest_v2_tamper` is a literal test helper with one `match` case per
table row; it never recomputes an unrelated hash. Add symlink, junction/reparse,
and hard-link cases separately because they need capability probes and exact
skip reasons. A source identity of typed `unavailable` is valid but must return
`source_claim_eligible is False`; malformed unavailable state rejects.

Use this literal single-read control. It proves verification and parsing consume
the same owned buffer, rather than merely counting `open()` calls:

```python
def test_verified_loader_reads_each_owned_file_once_and_parses_same_buffer(
    valid_run_copy, monkeypatch
):
    baseline = load_verified_run_bundle(valid_run_copy)
    original_manifest = json.loads(
        (valid_run_copy / "manifest.json").read_text(encoding="utf-8")
    )
    names = ("manifest.json",) + tuple(
        entry["name"] for entry in original_manifest["artifacts"]
    )
    reads = Counter()
    original_reader = artifact_schema._read_owned_regular_file_once

    def read_then_replace(path):
        data = original_reader(path)
        name = path.relative_to(valid_run_copy).as_posix()
        reads[name] += 1
        path.write_bytes(b"x" * max(1, len(data)))
        return data

    monkeypatch.setattr(
        artifact_schema, "_read_owned_regular_file_once", read_then_replace
    )
    loaded = load_verified_run_bundle(valid_run_copy)
    assert reads == Counter({name: 1 for name in names})
    assert loaded.manifest == baseline.manifest
    assert loaded.json_payloads == baseline.json_payloads
    for artifact_name, archive in loaded.npz_payloads.items():
        for array_name, array in archive.items():
            assert np.array_equal(
                array, baseline.npz_payloads[artifact_name][array_name]
            )
    for payload in loaded.json_payloads.values():
        with pytest.raises(TypeError):
            payload["mutation"] = True
    for archive in loaded.npz_payloads.values():
        for array in archive.values():
            with pytest.raises(ValueError):
                array.setflags(write=True)
    with pytest.raises((TypeError, ValueError), match="manifest|size|sha256"):
        load_verified_run_bundle(valid_run_copy)
```

- [ ] **Step 3: Add explicit legacy RED tests**

Require `load_verified_run_bundle()` to reject v1. Require `load_run_bundle(v1)` to reject unless `legacy_observed_at_revision` is supplied. Require `verify_legacy_v1_observed()` to inventory the actual files once, emit the exact closed observation, reject unknown observation fields, retain the two limitations, and never write the source directory.

Add this literal recognizer matrix; it prevents an arbitrary schemaless JSON
object from becoming a legacy observation merely because the caller supplied a
revision:

```python
LEGACY_RECOGNIZER_MUTATIONS = (
    "unknown_root_key",
    "missing_root_key",
    "incomplete_manifest",
    "noncomplete_artifact",
    "config_provenance_drift",
    "wrong_observation_revision",
)


@pytest.mark.parametrize(
    "mutation", LEGACY_RECOGNIZER_MUTATIONS, ids=LEGACY_RECOGNIZER_MUTATIONS
)
def test_schemaless_dispatch_requires_the_exact_legacy_contract(
    tmp_path, mutation
):
    source, valid_revision = HISTORICAL_RUNS[0]
    copied = tmp_path / mutation
    shutil.copytree(source, copied)
    manifest_path = copied / "manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    revision = valid_revision
    match mutation:
        case "unknown_root_key":
            payload["extra"] = True
        case "missing_root_key":
            del payload["complete"]
        case "incomplete_manifest":
            payload["complete"] = False
        case "noncomplete_artifact":
            payload["artifacts"]["config.json"] = "incomplete"
        case "config_provenance_drift":
            payload["provenance"]["config_hash"] = "0" * 64
        case "wrong_observation_revision":
            revision = "b" * 40
        case _:
            raise AssertionError(mutation)
    manifest_path.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")),
        encoding="utf-8",
    )
    with pytest.raises((TypeError, ValueError), match="legacy|schemaless"):
        load_run_bundle(copied, legacy_observed_at_revision=revision)


def test_arbitrary_schemaless_mapping_is_not_legacy(tmp_path):
    run = tmp_path / "not-legacy"
    run.mkdir()
    (run / "manifest.json").write_text('{"complete":true}', encoding="utf-8")
    with pytest.raises(ValueError, match="schemaless"):
        load_run_bundle(run, legacy_observed_at_revision="a" * 40)
```

Run the adapter against copies of both tracked historical fixed-ray directories. Their public-extract inventory drift must be recorded as a limitation and must not be misreported as v2 integrity.

Use the exact two paths and pin file bytes before and after:

```python
HISTORICAL_RUNS = (
    (
        Path("docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49"),
        "fcb2c49efdca2ad3ee502dc08fbb82fc285e7a05",
    ),
    (
        Path("docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic"),
        "039df35daa30a49e90f178edde7bfc999a7ee629",
    ),
)


@pytest.mark.parametrize(
    "source,revision", HISTORICAL_RUNS,
    ids=("confirmatory", "fixed-model-diagnostic"),
)
def test_tracked_v1_is_observed_without_rewrite(source, revision, tmp_path):
    before = recursive_file_inventory(source)
    copied = tmp_path / source.name
    shutil.copytree(source, copied)
    with pytest.raises(ValueError, match="legacy_observed_at_revision"):
        load_run_bundle(copied)
    observed = load_run_bundle(copied, legacy_observed_at_revision=revision)
    assert isinstance(observed, LegacyObservedBundle)
    assert observed.source_claim_eligible is False
    assert observed.observation_payload()["limitations"] == [
        "Observed bytes support compatibility and reproduction only.",
        "The observation does not provide manifest-v2 self-integrity or current scientific promotion.",
    ]
    assert recursive_file_inventory(source) == before
```

- [ ] **Step 4: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_artifact_schema.py tests\test_artifacts.py tests\test_gaussian_results_document.py -k "publish or verified or tamper or legacy or historical or single_read" -q -p no:cacheprovider --basetemp=.pytest-wave-b-task6-red
```

- [ ] **Step 5: Implement publication in this exact order**

1. Revalidate the frozen prepared record, including
   `output_root_admission`, in memory.
2. Reject an existing target without creating a sibling.
3. Immediately rerun `revalidate_output_root(prepared.output_root_admission)`;
   reject admission drift before any effect.
4. Create only the target parent. Canonically write/fsync the parent journal in
   phase `staging`, then fsync the parent before creating any stage.
5. Create the exact same-volume sibling `.$runName.$ownerToken.staging`.
6. Write `incomplete-run-v1.json` with the exact journal/owner/name/manifest
   binding, flush/fsync it, then fsync the staging directory.
7. Write each prepared artifact byte buffer with exclusive creation, flush, and fsync.
8. Read each staged artifact once, compare size/hash with the prepared inventory, then discard the verification buffer.
9. Write `manifest.json` last from `prepared.manifest_bytes`, flush/fsync it,
   then fsync the staging directory.
10. Verify the complete staged inventory, atomically rewrite/fsync the parent
    journal to `ready_to_install`, and fsync the parent before marker removal.
11. Remove the incomplete marker and fsync its parent staging directory before
    proceeding.
12. Atomically rename staging to the final run directory and fsync the final
    parent directory.
13. Verify the installed final against the prepared inventory; atomically
    rewrite/fsync the journal to `installed` and fsync its parent.
14. Remove the journal and fsync the final parent directory.
15. Return a v2 `RunStore`; never reopen caller objects.

On ordinary exceptions before rename, validate and remove only this task's exact
stage and journal, then fsync the parent. After rename, retain the exact complete
final, validate and remove only this task's journal, and fsync the parent. Never
remove or overwrite a preexisting final run. A hard process termination may
leave a stage plus parent journal; discovery ignores both because neither is a
final run, and recovery acts only through the durable journal contract above.

- [ ] **Step 6: Implement read-once parsing and version dispatch**

Read `manifest.json` once, decode it only with `strict_json_from_bytes`,
dispatch on exact schema, and pass its byte buffer into the internal v2/legacy
loader. Recursively enumerate actual files before parsing; reject aliases and
entries not exactly accounted for by the selected schema. For v2, hash an
inventory file's single buffer before parsing that same buffer with
`strict_json_from_bytes` or
`np.load(io.BytesIO(buffer), allow_pickle=False)`. Do not call
`Path.read_text`, `Path.read_bytes`, or `np.load(path)` after verification.

Before exposing an NPZ mapping, validate the ZIP central directory and every
NPY header against Task 5's closed writer contract: exact sorted member order,
portable case-fold-unique `name.npy` members only, no extras/comments,
`ZIP_STORED`, fixed timestamp/system/attributes, NPY version 2.0,
`fortran_order=False`, admitted canonical dtype, nonempty shape and value
count, and finite real/imaginary components. Re-encode each array and the full
archive with `canonical_npz_bytes` and require byte-for-byte equality with the
verified input. Tests mutate each member/order/name/dtype/shape/version/header
and ZIP metadata field independently, recompute only the outer run hash, and
require the strict reader to reject.

- [ ] **Step 7: Run GREEN and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_artifact_schema.py tests\test_artifacts.py tests\test_gaussian_results_document.py -q -p no:cacheprovider --basetemp=.pytest-wave-b-task6-green
git add -- src/multiagent_elbo/artifacts.py src/multiagent_elbo/artifact_schema.py src/multiagent_elbo/__init__.py tests/test_artifact_schema.py tests/test_artifacts.py tests/test_gaussian_results_document.py
git commit -m "feat: publish and verify run manifest v2"
```

### Task 7: Migrate every metric and run producer to prepare-then-publish

**Closes:** `AUD-04`, `AUD-05`, and `AUD-11` across active paths; makes `AUD-01` v2 reachable from every writer.

**Files:** all thirteen producer/state modules and every owning test listed in
the File Responsibility Map. The publication inventory below is binding; the
analysis-only `confirmatory_analysis.py` is separately covered by Task 2.

```python
ACTIVE_PUBLICATION_CALLABLES = (
    ("src/multiagent_elbo/finite/experiment.py", "run_finite_experiment", "tests/test_finite_experiment.py"),
    ("src/multiagent_elbo/finite/agent_network_experiment.py", "run_agent_network_experiment", "tests/test_agent_network_experiment.py"),
    ("src/multiagent_elbo/finite/attention_experiment.py", "run_attention_experiment", "tests/test_attention_experiment.py"),
    ("src/multiagent_elbo/finite/categorical_dqm_experiment.py", "run_categorical_dqm_experiment", "tests/test_categorical_dqm_experiment.py"),
    ("src/multiagent_elbo/finite/counterexample_experiment.py", "run_finite_counterexample_experiment", "tests/test_counterexample_experiment.py"),
    ("src/multiagent_elbo/finite/information_history_experiment.py", "run_information_history_experiment", "tests/test_information_history_experiment.py"),
    ("src/multiagent_elbo/finite/scale_cocycle_experiment.py", "run_scale_cocycle_experiment", "tests/test_scale_cocycle_experiment.py"),
    ("src/multiagent_elbo/finite/theory_oracle_experiment.py", "run_theory_oracle_experiment", "tests/test_theory_oracle_experiment.py"),
    ("src/multiagent_elbo/geometry/holonomy_experiment.py", "run_holonomy_experiment", "tests/test_holonomy_experiment.py"),
    ("src/multiagent_elbo/realizations/gaussian/experiment.py", "run_gaussian_experiment", "tests/test_gaussian_realization.py"),
    ("src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostic_experiment.py", "run_fixed_model_diagnostic", "tests/test_gaussian_fixed_ray_diagnostic_experiment.py"),
    ("src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py", "publish_cuda_sentinel", "tests/test_gaussian_fixed_ray_experiment.py"),
    ("src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py", "publish_confirmatory_experiment", "tests/test_gaussian_confirmatory_experiment.py"),
    ("src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py", "run_gaussian_fixed_ray_experiment", "tests/test_gaussian_fixed_ray_experiment.py"),
)
```

**Required producer root map and effect order:**

```python
PUBLICATION_MODULE_ROOT_DEPTHS = (
    ("src/multiagent_elbo/finite/experiment.py", 3),
    ("src/multiagent_elbo/finite/agent_network_experiment.py", 3),
    ("src/multiagent_elbo/finite/attention_experiment.py", 3),
    ("src/multiagent_elbo/finite/categorical_dqm_experiment.py", 3),
    ("src/multiagent_elbo/finite/counterexample_experiment.py", 3),
    ("src/multiagent_elbo/finite/information_history_experiment.py", 3),
    ("src/multiagent_elbo/finite/scale_cocycle_experiment.py", 3),
    ("src/multiagent_elbo/finite/theory_oracle_experiment.py", 3),
    ("src/multiagent_elbo/geometry/holonomy_experiment.py", 3),
    ("src/multiagent_elbo/realizations/gaussian/experiment.py", 4),
    ("src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostic_experiment.py", 4),
    ("src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py", 4),
)
```

Each module defines exactly one `_REPO_ROOT =
Path(__file__).resolve().parents[depth]` from this table. Every public producer,
including `publish_cuda_sentinel`, `publish_confirmatory_experiment`, and
`run_gaussian_fixed_ray_experiment`, executes this literal sequence before any
RNG draw, temporary path, gate capture, GPU query, worker launch, or write:

```python
if not isinstance(config, ExperimentConfig):
    raise TypeError("config must be an ExperimentConfig")
repo_root = _REPO_ROOT
resolved_config = with_resolved_output_root(
    config,
    anchor=repo_root,
    repo_root=repo_root,
    theory_root=repo_root / "Theory",
)
# Run all owning input/schema/experiment/option validation here. Recompute and
# compare every declared input/source inventory size and digest from the same
# owned read buffer; retain only immutable authorized records.
source_binding = authorize_source_digest_binding(
    repo_root=repo_root,
    theory_root=repo_root / "Theory",
    excluded_output_roots=(resolved_config.output.root,),
)
config_hash = config_sha256(resolved_config)
streams = RngStreams.from_seed(resolved_config.run.seed)
provenance = collect_provenance(
    repo_root,
    repo_root / "Theory",
    config_hash,
    streams,
    excluded_output_roots=(resolved_config.output.root,),
    resolved_config=resolved_config,
    authorized_source_binding=source_binding,
)
# This is the last operation before any gate, worker, lock, mkdir, or write.
revalidate_resolved_output_root(resolved_config)
# Capture an authorized gate here only for callables that require one.
# Launch an authorized worker here only for callables that require one.
payloads = RunPayloads(
    artifact_kind=resolved_config.theory.experiment,
    json_payloads=json_payloads,
    npz_payloads=npz_payloads,
)
prepared = prepare_run_bundle(resolved_config, provenance, payloads)
store = publish_run_bundle(prepared)
```

`authorize_source_digest_binding` is a closed immutable internal record of the
Git status, dirty-tree, Theory, and exclusion digests. It performs the only
source filesystem/Git reads used by `collect_provenance`;
`collect_provenance` validates and consumes that record without re-reading or
accepting caller digest strings. Every owning file/inventory digest is likewise
recomputed and compared during the preceding validator call. The source/input
authorizations therefore precede `config_sha256`, and the config hash precedes
RNG or execution-identity construction. The literal domain order is:

```text
root_admission
  < input_schema_digest_authorization
  < config_identity_rng
  < root_admission_revalidated
  < gate
  < worker
  < publication
```

Nodes absent from a callable are omitted, never reordered. No caller may hash a
config while an input/source inventory digest is merely declared but not
recomputed and authorized. The cached root is
fully revalidated as the final operation before the first gate/worker/output
effect. `publish_run_bundle` independently repeats admission immediately
before its mkdir. No config hashing, identity/RNG construction, gate capture,
worker launch, or publication may occur before all input/source digest
authorization succeeds.

The launchers call the same idempotent resolver before dispatch, but that is not
the producer's safety proof: a direct public call must still execute the sequence
above. `tests/test_shared_scientific_contracts.py` parses each callable in
`ACTIVE_PUBLICATION_CALLABLES` and requires the lexical order
`with_resolved_output_root < input/schema validators and inventory-digest
authorization < authorize_source_digest_binding < config_sha256 <
RngStreams.from_seed < collect_provenance < revalidate_resolved_output_root <
gate < worker < prepare_run_bundle < publish_run_bundle`, omitting only
inapplicable gate/worker nodes. Runtime negative
controls monkeypatch the owning module's RNG factory, gate capture, worker
launcher, and filesystem writer to fail if called; an invalid/overlapping root
must raise first with all counters still zero.

Task 7 owns and adds
`test_every_publication_callable_has_literal_domain_order` and
`test_invalid_root_precedes_all_producer_effects` only after every callable in
`ACTIVE_PUBLICATION_CALLABLES` has migrated. The lexical helper also injects a
wrong declared input/source digest and requires failure before
`config_sha256`, `RngStreams.from_seed`, any gate/worker, or any filesystem
effect. Task 4 does not collect either cross-module test.

No production source may retain `RunStore.create`, `write_json`, `write_npz`, or `finalize` after this task.

- [ ] **Step 1: Add one literal shared result assertion and invoke it in every owning test**

Add to `tests/test_shared_scientific_contracts.py`:

```python
def assert_v2_published_result(result):
    bundle = load_verified_run_bundle(result.run_dir)
    assert bundle.manifest["schema_version"] == "run-manifest-v2"
    assert bundle.manifest["status"] == "complete"
    assert tuple(item.name for item in bundle.inventory) == tuple(
        sorted(item.name for item in bundle.inventory)
    )
    assert {"config.json", "provenance.json"} <= {
        item.name for item in bundle.inventory
    }
    config_payload = bundle.json_payloads["config.json"]
    assert Path(config_payload["resolved_config"]["output"]["root"]).is_absolute()
    assert result.run_dir.is_relative_to(
        Path(config_payload["resolved_config"]["output"]["root"])
    )
    for payload in bundle.json_payloads.values():
        assert_candidate_payload(payload)
        if isinstance(payload, Mapping):
            for value in payload.values():
                if isinstance(value, Mapping) and value.get("schema_version") == "metric-record-v2":
                    assert load_metric_record(value).verification_state == "CANDIDATE"
    for members in bundle.npz_payloads.values():
        for array in members.values():
            with pytest.raises(ValueError):
                array.setflags(write=True)
```

Import and call `assert_v2_published_result(result)` in the primary successful
publication test in each exact test path in `ACTIVE_PUBLICATION_CALLABLES`.
For callables returning a run path rather than a result, wrap it in
`SimpleNamespace(run_dir=returned_path)`. The test must also compare the
manifest's artifact names with the callable's existing expected artifact set;
do not weaken or replace those producer-specific expectations.

Update the writer-specific failure tests to inject malformed JSON/NPZ before preparation and require the staging parent absent. Add one shared monkeypatch test that makes every legacy `RunStore` incremental method raise; every producer must still pass.

Add this AST reachability test so the inventory cannot silently omit a new or
legacy publication path:

```python
def test_active_publication_inventory_is_complete_and_uses_v2_only():
    inventoried = {(path, name) for path, name, _ in ACTIVE_PUBLICATION_CALLABLES}
    discovered = set()
    for path in sorted({Path(item[0]) for item in ACTIVE_PUBLICATION_CALLABLES}):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                calls = {ast.unparse(call.func) for call in ast.walk(node) if isinstance(call, ast.Call)}
                if {"publish_run_bundle", "RunStore.create"} & calls:
                    discovered.add((path.as_posix(), node.name))
                assert "RunStore.create" not in calls
                assert not {"store.write_json", "store.write_npz", "store.finalize"} & calls
    assert discovered == inventoried
```

- [ ] **Step 2: Run all writer RED tests**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_finite_experiment.py tests\test_agent_network_experiment.py tests\test_attention_experiment.py tests\test_categorical_dqm_experiment.py tests\test_counterexample_experiment.py tests\test_information_history_experiment.py tests\test_scale_cocycle_experiment.py tests\test_theory_oracle_experiment.py tests\test_holonomy_experiment.py tests\test_gaussian_realization.py tests\test_gaussian_fixed_ray_diagnostic_experiment.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py -k "manifest or publication or metric or candidate or output_root or malformed" -q -p no:cacheprovider --basetemp=.pytest-wave-b-task7-red
```

- [ ] **Step 3: Migrate all metric call sites with this exact mapping**

Replace the private `MetricRecord` in `finite/experiment.py` and `GaussianMetricRecord` in `realizations/gaussian/experiment.py` with aliases/imports of the shared v2 record. Replace every direct status constructor with a matching factory. Descriptive values without a preregistered predicate use `inapplicable_metric()` and decision `inconclusive`; they must not be labeled passing. Detection controls currently expressed as `value > tolerance` use `strict_lower_bounded_metric(value, lower_bound=0.0, tolerance=tolerance)`. CPU-only parity when CUDA was not requested is inapplicable and candidate, not verification-inconclusive.

Only after both alias modules have migrated, add this identity control to
`tests/test_experiment_support.py`:

```python
def test_wave_zero_metric_aliases_are_exact_shared_type():
    assert FiniteExperimentMetricRecord is MetricRecord
    assert GaussianMetricRecord is MetricRecord
```

The test is absent from Task 1 RED/GREEN and is first collected by Task 7
GREEN. A subclass, wrapper, duplicate dataclass, or delayed compatibility shim
fails the identity assertions.

The factory keyword for strict lower bounds is `lower_bound`, not `bound`:

```python
strict_lower_bounded_metric(
    value,
    tolerance,
    lower_bound=0.0,
    applicability_reason="the preregistered detection control applies",
    interpretation=interpretation,
    theorem_status="NUMERICAL",
    claim_origin="APPLICATION_SPECIFIC",
)
```

Use `target_metric` for two-sided equality controls, `lower_bounded_metric` for
inclusive lower controls, `upper_bounded_metric` for inclusive upper controls,
`expected_positive_infinity_metric` only for a declared extended-KL endpoint,
and `inapplicable_metric` for descriptive/no-predicate and unrequested CUDA
parity. No producer constructs `MetricRecord` directly.

Serialize metrics only through `metric_record_payload()`, never `asdict(metric)`, so expected positive infinity remains strict JSON.

- [ ] **Step 4: Migrate every writer and direct reader**

Build complete JSON/NPZ mappings before preparation. Include diagnostic and optional payloads conditionally in that in-memory mapping, not through later writes. In `fixed_ray_experiment.py`, delete the post-finalize manifest reopen/mutation used to append hashes; the v2 inventory is authoritative. Route sentinel validation and every resume/discovery reader through `load_run_bundle()` with explicit version dispatch. Route the fixed-model diagnostic's historical source through `verify_legacy_v1_observed()` before applying its existing source-binding checks.

Every callable follows the shown ordering: admit the root; validate
inputs/schema/options and recompute/authorize every input/source inventory
digest; authorize the source binding; compute `config_sha256`; construct
identity and RNG state; revalidate admission; capture any gate; launch any worker;
compute complete payloads; prepare; then publish. No gate, worker, temporary
directory, or output path exists before just-in-time admission revalidation.
Preserve every existing JSON and NPZ scientific payload and optional-diagnostics
condition; only `config.json`, `provenance.json`, and `manifest.json` change to
their v2 schemas.

- [ ] **Step 5: Run GREEN, source scans, and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_experiment_support.py tests\test_finite_experiment.py tests\test_agent_network_experiment.py tests\test_attention_experiment.py tests\test_categorical_dqm_experiment.py tests\test_counterexample_experiment.py tests\test_information_history_experiment.py tests\test_scale_cocycle_experiment.py tests\test_theory_oracle_experiment.py tests\test_holonomy_experiment.py tests\test_gaussian_realization.py tests\test_gaussian_fixed_ray_diagnostic_experiment.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py tests\test_shared_scientific_contracts.py -q -p no:cacheprovider --basetemp=.pytest-wave-b-task7-green
rg -n "RunStore\.create|\.write_json\(|\.write_npz\(|\.finalize\(" src/multiagent_elbo --glob "!artifacts.py"
if ($LASTEXITCODE -ne 1) { throw "legacy incremental publication remains reachable" }
rg -n 'verification_state\s*=\s*"(LLM_SUPPORTED|EVIDENCE_VERIFIED|REFUTED|INCONCLUSIVE)"|"mathematical_verification_state"' src/multiagent_elbo
if ($LASTEXITCODE -ne 1) { throw "producer promotion state remains" }
```

Both scans must return exit code 1 with no matches. Then commit:

```powershell
git add -- src/multiagent_elbo/finite/experiment.py src/multiagent_elbo/finite/agent_network_experiment.py src/multiagent_elbo/finite/attention_experiment.py src/multiagent_elbo/finite/categorical_dqm_experiment.py src/multiagent_elbo/finite/counterexample_experiment.py src/multiagent_elbo/finite/information_history_experiment.py src/multiagent_elbo/finite/scale_cocycle_experiment.py src/multiagent_elbo/finite/theory_oracle_experiment.py src/multiagent_elbo/geometry/holonomy_experiment.py src/multiagent_elbo/realizations/gaussian/experiment.py src/multiagent_elbo/realizations/gaussian/confirmatory_analysis.py src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostic_experiment.py src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py tests/test_experiment_support.py tests/test_finite_experiment.py tests/test_agent_network_experiment.py tests/test_attention_experiment.py tests/test_categorical_dqm_experiment.py tests/test_counterexample_experiment.py tests/test_information_history_experiment.py tests/test_scale_cocycle_experiment.py tests/test_theory_oracle_experiment.py tests/test_holonomy_experiment.py tests/test_gaussian_realization.py tests/test_gaussian_confirmatory_analysis.py tests/test_gaussian_fixed_ray_diagnostic_experiment.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py tests/test_shared_scientific_contracts.py
git commit -m "feat: publish all experiments through run v2"
```

### Task 8: Publish figures as immutable generations behind an atomic pointer

**Closes:** `AUD-02`; completes figure-cache closure for `AUD-01`.

**Files:**

- Create: `src/multiagent_elbo/figure_store.py`
- Create: `tests/test_figure_store.py`
- Modify: `src/multiagent_elbo/figures.py`
- Modify: `src/multiagent_elbo/rendering.py`
- Modify: `tests/test_figures.py`
- Modify: `tests/test_experiment_support.py`

**On-disk layout:**

```text
$outputDir/active-generation.json
$outputDir/generations/{generation_id}/figure-generation.json
$outputDir/generations/{generation_id}/{figure}.png
$outputDir/generations/{generation_id}/{figure}.pdf
$outputDir/last-failure.json
$outputDirParent/.$outputName.publisher.lock
$outputDirParent/.$outputName.publication-journal.json
$outputDirParent/.$outputName.$ownerToken.staging/
```

No file directly below `$outputDir` other than the active pointer and optional
failure record is a figure payload. No generation is deleted in Wave B.

**Closed schemas and public interfaces:**

```python
FIGURE_CACHE_IDENTITY_V2_KEYS = {
    "schema_version", "source_manifest_sha256", "source_inventory_sha256",
    "requested", "renderer_options", "renderer_schema",
    "renderer_source_identity", "expected_outputs", "reuse_eligible",
    "unavailable_nonce",
}
FIGURE_OUTPUT_V2_KEYS = {"name", "kind", "size_bytes", "sha256"}
FIGURE_SOURCE_BINDING_V2_KEYS = {
    "run_dir", "run_schema", "observed_at_revision",
    "manifest_sha256", "inventory_sha256", "source_claim_eligible",
}
FIGURE_GENERATION_V2_KEYS = {
    "schema_version", "status", "generation_id", "cache_identity",
    "cache_identity_sha256", "source_binding", "outputs",
}
ACTIVE_GENERATION_V2_KEYS = {
    "schema_version", "generation_id", "generation_manifest_sha256"
}
FIGURE_JOURNAL_V2_KEYS = {
    "schema_version", "owner_token", "phase", "cache_identity_sha256",
    "staging_name", "generation_id", "pointer_temp_name"
}
FIGURE_FAILURE_V2_KEYS = {
    "schema_version", "cache_identity_sha256", "failure_kind", "message"
}
FIGURE_LOCK_V2_KEYS = {
    "schema_version", "owner_token", "process_id", "started_utc"
}
FIGURE_JOURNAL_PHASES = (
    "rendering", "generation_prepared", "generation_installed",
    "pointer_preparing", "pointer_prepared", "pointer_replaced",
)


@dataclass(frozen=True, slots=True)
class AvailableRendererSourceIdentity:
    git_commit: str
    dirty_tree_sha256: str
    files: tuple[ArtifactInventoryEntry, ...]
    status: Literal["available"] = field(default="available", init=False)


@dataclass(frozen=True, slots=True)
class UnavailableRendererSourceIdentity:
    reason: str
    status: Literal["unavailable"] = field(default="unavailable", init=False)


@dataclass(frozen=True, slots=True)
class FigureSourceBinding:
    run_dir: Path
    run_schema: Literal["run-manifest-v2", "legacy-run-manifest-v1"]
    observed_at_revision: str | None
    manifest_sha256: str
    inventory_sha256: str
    source_claim_eligible: bool


@dataclass(frozen=True)
class FigureCacheIdentity:
    source_manifest_sha256: str
    source_inventory_sha256: str
    requested: tuple[str, ...]
    renderer_options: tuple[tuple[str, JsonScalar], ...]
    renderer_source_identity: (
        AvailableRendererSourceIdentity | UnavailableRendererSourceIdentity
    )
    expected_outputs: tuple[str, ...]
    reuse_eligible: bool
    unavailable_nonce: str | None
    schema_version: Literal["figure-cache-identity-v2"] = field(
        default="figure-cache-identity-v2", init=False
    )
    renderer_schema: Literal["multiagent-elbo-figure-renderer-v2"] = field(
        default="multiagent-elbo-figure-renderer-v2", init=False
    )


@dataclass(frozen=True, slots=True)
class FigureOutputRecord:
    name: str
    kind: Literal["png", "pdf"]
    path: Path
    size_bytes: int
    sha256: str


@dataclass(frozen=True, slots=True, init=False)
class FigureManifest:
    run_dir: Path
    output_dir: Path
    generation_dir: Path
    requested: tuple[str, ...]
    generation_id: str
    cache_identity_sha256: str
    cache_identity: FigureCacheIdentity
    source_binding: FigureSourceBinding
    outputs: tuple[FigureOutputRecord, ...]
    manifest_sha256: str
    manifest_path: Path
    pointer_path: Path
    source_claim_eligible: bool
    status: Literal["complete"] = field(default="complete", init=False)

    @property
    def figure_paths(self) -> tuple[Path, ...]:
        return tuple(item.path for item in self.outputs)

    def complete_inventory(self) -> tuple[tuple[str, int, str], ...]:
        return tuple(
            (item.name, item.size_bytes, item.sha256) for item in self.outputs
        )

    def has_exact_complete_inventory(self) -> bool:
        return verify_loaded_figure_manifest(self)


def render_run(
    run_dir: Path | str,
    output_dir: Path | str,
    requested: Sequence[str] | None = None,
    *,
    legacy_observed_at_revision: str | None = None,
    renderer_options: Mapping[str, JsonScalar] | None = None,
    anchor: Path | None = None,
    repo_root: Path | None = None,
    theory_root: Path | None = None,
) -> FigureManifest: ...


def load_active_figure_generation(
    output_dir: Path | str,
    *,
    anchor: Path | None = None,
    repo_root: Path | None = None,
    theory_root: Path | None = None,
) -> FigureManifest: ...


def _load_verified_figure_generation(
    output_dir: Path | str,
    generation_id: str,
) -> FigureManifest:
    """Load one inactive or active generation through the strict verifier."""
    ...


def verify_loaded_figure_manifest(manifest: FigureManifest) -> bool: ...
```

The first three `render_run` positional parameters are the Wave 0 compatibility
signature and remain callable unchanged. Optional root-context keywords are an
additive strictness seam. When omitted, all three are derived from the module's
fixed `_REPO_ROOT = Path(__file__).resolve().parents[2]`; neither function
consults ambient CWD. The AST inventory in Task 9 enumerates and calls every
tracked `render_run` call site in both compatibility and explicit-context
forms, so no caller is silently stranded.
`verify_loaded_figure_manifest` rereads each declared output once as an owned
regular file, rejects aliases/reparse/hard-link substitutions, and returns
`True` only when the complete name/size/SHA inventory and generation manifest
still agree; any mismatch raises rather than returning `False`.
`_load_verified_figure_generation` accepts only a 64-character lowercase-hex
generation ID, derives the direct child below `output_dir/generations`, parses
the closed generation manifest, reconstructs `FigureManifest`, and calls
`verify_loaded_figure_manifest` before returning. `load_active_figure_generation`
validates the pointer and then delegates to this same private verifier; recovery
and tests do not implement a second generation reader.

The available renderer source identity binds a full lowercase Git SHA, dirty-tree
digest, and exact sorted records for `figures.py`, `figure_store.py`, and
`rendering.py`. The unavailable union requires a nonempty reason, sets
`reuse_eligible=False`, and requires a fresh 32-byte lowercase-hex
`unavailable_nonce`; available requires `reuse_eligible=True` and nonce `None`.
Renderer options have exact keys `png_dpi`, `pdf_metadata_creator`, and
`matplotlib_backend`. `png_dpi` is the sole configurable member and must be
an exact built-in integer in `[72, 1200]` (Boolean rejected);
`pdf_metadata_creator` is exactly `MultiAgentELBO` and
`matplotlib_backend` is exactly `Agg`. `None` selects the closed default
`{"png_dpi":300,"pdf_metadata_creator":"MultiAgentELBO",
"matplotlib_backend":"Agg"}`; partial, extra, or mutable-after-call mappings
are detached then validated. Options are serialized as the ASCII-name-sorted
tuple. Expected outputs are derived only from the ordered request as
`name.png`, `name.pdf` pairs and are never independently configurable.

Compute identities with these domain-separated preimages:

```python
source_inventory_sha256 = hashlib.sha256(
    b"multiagent-elbo:verified-run-inventory:v1\0"
    + canonical_json_bytes([asdict(item) for item in verified.inventory])
).hexdigest()
cache_identity_sha256 = hashlib.sha256(
    b"multiagent-elbo:figure-cache:v2\0"
    + canonical_json_bytes(figure_cache_identity_payload(identity))
).hexdigest()
generation_id = hashlib.sha256(
    b"multiagent-elbo:figure-generation:v2\0"
    + canonical_json_bytes(
        {
            "cache_identity": figure_cache_identity_payload(identity),
            "output_inventory": output_inventory,
        }
    )
).hexdigest()
```

The output inventory excludes `figure-generation.json`, is ordered by ASCII
name, and has exact output-entry keys. The generation manifest uses schema
`figure-generation-v2`, status `complete`, and embeds the cache identity plus
its digest plus the closed `FigureSourceBinding`. The binding stores a
normalized absolute source run directory, exact run schema, the full legacy
observation revision only for legacy, exact source manifest/inventory digests,
and an exact Boolean eligibility bit. On load, the active-generation reader
strictly parses that binding, calls `load_run_bundle` with the persisted
revision when required, and recomputes all three binding values before it
constructs `FigureManifest` through a module-private constructor. Thus
`run_dir`, cache identity, source eligibility, and output paths are
reconstructible from persisted bytes; no undefined or caller-supplied field is
invented. The pointer uses schema `active-figure-generation-v2`. The journal
uses schema `figure-publication-journal-v2` and phase `rendering`,
`generation_prepared`, `generation_installed`, `pointer_preparing`,
`pointer_prepared`, or `pointer_replaced`. The failure
record uses schema `figure-publication-failure-v2`; it is diagnostic and never a
cache hit or active generation.

`FigurePublishBoundary` is the closed tuple
`after_journal_rendering`, `after_each_render`,
`after_generation_manifest_fsync`, `after_journal_generation_prepared`,
`after_generation_rename`, `after_generation_parent_fsync`,
`after_journal_generation_installed`, `after_journal_pointer_preparing`,
`after_pointer_temp_fsync`, `after_pointer_temp_parent_fsync`,
`after_journal_pointer_prepared`, `after_pointer_replace`,
`after_pointer_parent_fsync`, `after_journal_pointer_replaced`,
`before_journal_remove`, `after_journal_remove`, and
`after_journal_parent_fsync`.

Every figure record rejects unknown or missing fields before use. The exact value
contracts are:

- `figure-generation-v2` has `status="complete"`; `generation_id`,
  `cache_identity_sha256`, every output SHA, and the pointer's manifest SHA are
  lowercase 64-hex strings. `outputs` is a nonempty ASCII-name-sorted tuple with
  no case-fold alias, and each name equals the ordered request expansion.
- `active-figure-generation-v2` contains only one generation ID and the SHA-256
  of the exact `figure-generation.json` bytes. The reader derives
  `generations/{generation_id}/`; no persisted absolute path is accepted.
- `figure-publisher-lock-v2` has a fresh 64-hex owner token, a positive exact
  integer process ID (Boolean rejected), and an RFC 3339 UTC timestamp. The OS
  lock, not these diagnostic fields, establishes liveness.
- `figure-publication-journal-v2` has the same owner token and one of the six
  frozen phases. `staging_name` is always one safe sibling filename.
  `generation_id` is JSON `null` only during `rendering` and otherwise a
  lowercase 64-hex value. `pointer_temp_name` is JSON `null` during
  `rendering`, `generation_prepared`, and `generation_installed`, then one
  safe sibling filename during `pointer_preparing`, `pointer_prepared`, and
  `pointer_replaced`. The referenced filesystem state is
  closed by this table:

  | phase | staging path | generation | pointer-temp path | active pointer |
  |---|---|---|---|---|
  | `rendering` | exists and is task-owned | absent | name is `null` | unchanged |
  | `generation_prepared` | exists, task-owned, and contains the exact complete generation | absent | name is `null` | unchanged |
  | `generation_installed` | absent | exact complete generation exists | name is `null` | unchanged |
  | `pointer_preparing` | absent | exact complete generation exists | exact name persisted; temp may be absent or exact | unchanged |
  | `pointer_prepared` | absent | exact complete generation exists | either exact temp exists, or it is absent only when active already selects this exact generation | old or exact intended generation |
  | `pointer_replaced` | absent | exact complete generation exists | absent | selects exact intended generation |

- `figure-publication-failure-v2` has a cache digest, closed `failure_kind` in
  `render_exception`, `validation_exception`, or `recovery_exception`, and a
  nonempty single-line message. It contains no traceback, absolute path,
  hostname, or process identifier and never participates in cache identity.

Startup recovery is also closed. `rendering` removes only the validated
task-owned sibling. `generation_prepared` verifies the complete staged
generation, installs it with one atomic rename, fsyncs the generations parent,
then journals/fsyncs `generation_installed`. `generation_installed` computes
the exact pointer bytes/name and journals/fsyncs `pointer_preparing` *before*
creating the pointer temp. `pointer_preparing` accepts either no temp or the
exact verified temp, writes/fsyncs it if absent, fsyncs its parent, then
journals/fsyncs `pointer_prepared`. `pointer_prepared` verifies the
generation and either (a) verifies the exact temp before `os.replace`, or (b),
for the crash window immediately after replacement, requires the temp absent
and the active pointer bytes already equal to the intended pointer. It fsyncs
the pointer parent, then journals/fsyncs `pointer_replaced`.
`pointer_replaced` verifies the active pointer, removes only the matching
journal, and fsyncs the journal parent. Every journal rewrite is atomic and both
file- and parent-directory-fsynced. Thus `generation_prepared(id)` is durable
before rename and `pointer_preparing(temp)` is durable before temp creation or
replacement. Any schema, owner, name, digest, or phase/filesystem mismatch
raises without deleting or replacing anything. No recovery branch deletes a
generation.

- [ ] **Step 1: Add literal cache-identity and tamper RED matrices**

Add to `tests/test_figure_store.py`:

```python
CACHE_MUTATIONS = (
    "new_valid_source_manifest", "new_valid_source_payload",
    "renderer_git_commit", "renderer_dirty_tree", "renderer_file_byte",
    "png_dpi", "request_order",
)


@pytest.mark.parametrize("mutation", CACHE_MUTATIONS, ids=CACHE_MUTATIONS)
def test_each_cache_input_change_forces_a_distinct_generation(
    figure_fixture, mutation
):
    first = figure_fixture.render()
    figure_fixture.mutate_cache_input(mutation)
    second = figure_fixture.render()
    assert second.generation_id != first.generation_id
    assert first.manifest_path.read_bytes() == figure_fixture.first_manifest_bytes
    assert all(path.exists() for path in first.figure_paths)


INVALID_CACHE_MUTATIONS = (
    "tampered_source_manifest", "tampered_source_payload",
    "source_inventory_order", "expected_output_name",
    "missing_renderer_option", "extra_renderer_option",
    "pdf_metadata_creator", "matplotlib_backend",
    "png_dpi_bool", "png_dpi_low", "png_dpi_high",
)


@pytest.mark.parametrize(
    "mutation", INVALID_CACHE_MUTATIONS, ids=INVALID_CACHE_MUTATIONS
)
def test_invalid_cache_input_mutation_rejects_without_activation(
    figure_fixture, mutation
):
    old = figure_fixture.render()
    before = figure_fixture.snapshot_publication_tree()
    figure_fixture.mutate_invalid_cache_input(mutation)
    with pytest.raises((TypeError, ValueError)):
        figure_fixture.render()
    assert figure_fixture.snapshot_publication_tree() == before
    assert load_active_figure_generation(
        figure_fixture.output_dir
    ).generation_id == old.generation_id


FIGURE_TAMPERS = (
    ("pointer_unknown_key", "pointer"),
    ("pointer_manifest_digest", "manifest"),
    ("generation_unknown_key", "generation"),
    ("generation_identity_digest", "cache identity"),
    ("generation_source_binding", "source binding"),
    ("generation_source_revision", "source binding"),
    ("missing_image", "missing"),
    ("extra_image", "unexpected"),
    ("image_size", "size"),
    ("image_sha256", "sha256"),
    ("output_order", "order"),
)


@pytest.mark.parametrize(
    "mutation,message", FIGURE_TAMPERS, ids=tuple(case[0] for case in FIGURE_TAMPERS)
)
def test_active_reader_rejects_closed_tamper_matrix(
    published_figures, mutation, message
):
    apply_figure_tamper(published_figures.output_dir, mutation)
    with pytest.raises((TypeError, ValueError), match=message):
        load_active_figure_generation(published_figures.output_dir)


@pytest.mark.parametrize("failure", ["source_manifest", "source_payload", "missing_array"])
def test_source_validation_failure_precedes_every_figure_path(
    figure_fixture, failure
):
    figure_fixture.break_source(failure)
    parent = figure_fixture.output_dir.parent
    before = recursive_file_inventory(parent)
    with pytest.raises((TypeError, ValueError)):
        figure_fixture.render()
    assert recursive_file_inventory(parent) == before
    assert not figure_fixture.output_dir.exists()
```

`figure_fixture`, `mutate_cache_input`, `mutate_invalid_cache_input`,
`apply_figure_tamper`, and `break_source` are implemented in the same test
module as closed `match` statements over these exact tuples; an unknown
mutation raises `AssertionError`. Each valid source mutation creates a new
fully consistent v2 source bundle and repoints the fixture; immutable old source
bytes are never edited. Invalid source mutations deliberately leave size/hash
or canonical order inconsistent, so verified loading fails without creating a
generation. Expected output names remain derived state, not a cache-input knob.

- [ ] **Step 2: Add exception-boundary and hard-termination RED tests**

Start with a valid active generation. Inject an exception at every `FigurePublishBoundary`, including the second image. Assert the old pointer and every old-generation byte remain unchanged. After success, assert the pointer selects a complete new generation and the old generation still exists unchanged.

Use these exact parameterized tests:

```python
FIGURE_BOUNDARIES = (
    "after_journal_rendering", "after_each_render",
    "after_generation_manifest_fsync", "after_journal_generation_prepared",
    "after_generation_rename", "after_generation_parent_fsync",
    "after_journal_generation_installed", "after_journal_pointer_preparing",
    "after_pointer_temp_fsync", "after_pointer_temp_parent_fsync",
    "after_journal_pointer_prepared", "after_pointer_replace",
    "after_pointer_parent_fsync", "after_journal_pointer_replaced",
    "before_journal_remove", "after_journal_remove",
    "after_journal_parent_fsync",
)


@pytest.mark.parametrize("boundary", FIGURE_BOUNDARIES, ids=FIGURE_BOUNDARIES)
def test_exception_boundary_preserves_one_complete_active_generation(
    active_old_generation, boundary
):
    old = active_old_generation.snapshot()
    with pytest.raises(InjectedFailure):
        active_old_generation.render_with_exception(boundary)
    active = load_active_figure_generation(active_old_generation.output_dir)
    assert active.generation_id in {
        old.generation_id, active_old_generation.expected_new_generation_id
    }
    assert active.complete_inventory() in {
        old.complete_inventory, active_old_generation.expected_new_inventory
    }
    assert active_old_generation.snapshot_generation(old.generation_id) == old.complete_inventory


@pytest.mark.parametrize("boundary", FIGURE_BOUNDARIES, ids=FIGURE_BOUNDARIES)
def test_process_termination_recovers_all_old_or_all_new(
    active_old_generation, boundary
):
    command = [
        sys.executable, "-B", "tests/figure_fault_worker.py",
        "--case", str(active_old_generation.case_path),
        "--boundary", boundary,
    ]
    result = subprocess.run(command, cwd=Path.cwd(), check=False)
    assert result.returncode == 73
    recovered = active_old_generation.recover_in_fresh_process()
    assert recovered.generation_id in {
        active_old_generation.old_generation_id,
        active_old_generation.expected_new_generation_id,
    }
    assert recovered.has_exact_complete_inventory()
```

`tests/figure_fault_worker.py` has a closed argparse choice over
`FIGURE_BOUNDARIES`, loads only the JSON case description, and injects
`os._exit(73)` at the selected boundary. `recover_in_fresh_process` invokes a
second worker action with `subprocess.run(..., check=True)`; it does not call
recovery again in the parent process. The second-render failure is injected by
counting `after_each_render` and exiting/raising on count two.
The `active_old_generation` test harness defines the otherwise fixture-local
members used above: `snapshot()`, `snapshot_generation(id)`,
`render_with_exception(boundary)`, `recover_in_fresh_process()`,
`expected_new_generation_id`, `expected_new_inventory`, and
`old_generation_id`. `snapshot()` returns a frozen test dataclass with
`generation_id` and `complete_inventory`; none of these names is implied to
be a production `FigureManifest` field.

Add this literal method to that test-only harness class:

```python
def verify_all_figure_generations(self) -> tuple[FigureManifest, ...]:
    generations_root = self.output_dir / "generations"
    entries = tuple(sorted(
        generations_root.iterdir(), key=lambda path: path.name.encode("ascii")
    ))
    if not entries or any(not path.is_dir() for path in entries):
        raise AssertionError("generation root is empty or contains a non-directory")
    manifests = tuple(
        figure_store._load_verified_figure_generation(
            self.output_dir, generation_dir.name
        )
        for generation_dir in entries
    )
    if not all(verify_loaded_figure_manifest(item) for item in manifests):
        raise AssertionError("generation verification returned false")
    return manifests
```

This is the sole definition of the fixture method; all concurrency assertions
call it rather than an unbound `verify_all_figure_generations` function.

- [ ] **Step 3: Add literal process-concurrency and stale-metadata RED tests**

Add these exact tests and helper to `tests/test_figure_store.py`:

```python
def _wait_for_files(paths, timeout_seconds=10.0):
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if all(path.is_file() for path in paths):
            return
        time.sleep(0.01)
    raise AssertionError(f"timed out waiting for {paths!r}")


def test_two_publishers_and_reader_never_observe_mixed_generation(
    active_old_generation,
):
    case = active_old_generation.case_path
    release = case.parent / "publish.release"
    ready = [case.parent / f"publish-{name}.ready" for name in ("a", "b")]
    processes = [
        subprocess.Popen([
            sys.executable, "-B", "tests/figure_fault_worker.py",
            "--action", "publish", "--case", str(case),
            "--request", name, "--ready", str(flag),
            "--release", str(release),
        ])
        for name, flag in zip(("a", "b"), ready, strict=True)
    ]
    _wait_for_files(ready)
    release.write_bytes(b"release\n")
    observed = []
    while any(process.poll() is None for process in processes):
        observed.append(
            load_active_figure_generation(active_old_generation.output_dir)
            .complete_inventory()
        )
    assert [process.wait() for process in processes] == [0, 0]
    assert all(
        inventory in active_old_generation.allowed_complete_inventories()
        for inventory in observed
    )
    generations = active_old_generation.verify_all_figure_generations()
    assert {generation.requested for generation in generations} >= {
        ("a",), ("b",)
    }
    active = load_active_figure_generation(active_old_generation.output_dir)
    assert active.requested in {("a",), ("b",)}


def test_live_lock_wins_and_stale_metadata_is_replaced_after_termination(
    active_old_generation,
):
    case = active_old_generation.case_path
    ready = case.parent / "holder.ready"
    release = case.parent / "holder.release"
    holder = subprocess.Popen([
        sys.executable, "-B", "tests/figure_fault_worker.py",
        "--action", "hold-lock", "--case", str(case),
        "--ready", str(ready), "--release", str(release),
    ])
    _wait_for_files([ready])
    old_metadata = active_old_generation.lock_metadata_path.read_bytes()
    busy = subprocess.run([
        sys.executable, "-B", "tests/figure_fault_worker.py",
        "--action", "try-lock", "--case", str(case),
    ], check=False, capture_output=True, text=True)
    assert busy.returncode == 75
    assert busy.stdout.strip() == "busy"
    holder.terminate()
    assert holder.wait() != 0
    acquired = subprocess.run([
        sys.executable, "-B", "tests/figure_fault_worker.py",
        "--action", "publish", "--case", str(case), "--request", "recovery",
    ], check=False)
    assert acquired.returncode == 0
    new_metadata = active_old_generation.lock_metadata_path.read_bytes()
    assert new_metadata != old_metadata
    old_owner = json.loads(old_metadata)
    new_owner = json.loads(new_metadata)
    assert (new_owner["process_id"], new_owner["owner_token"]) != (
        old_owner["process_id"], old_owner["owner_token"]
    )
```

The fixture methods `allowed_complete_inventories()` and
`verify_all_figure_generations()` validate exact manifest-declared bytes; they
do not accept a mixed inventory. The worker parser has closed choices for
`--action {publish,hold-lock,try-lock}`, request IDs `{a,b,recovery}`, and the
optional ready/release paths shown above. Capability skips are forbidden for
the ordinary Windows/POSIX lock implementation.

Also replace the existing broad platform decorator on
`test_replay_rejects_a_lexical_junction_run_root_before_resolving_it` with this
closed capability fixture in `tests/test_figures.py`:

```python
@pytest.fixture
def windows_junction_factory():
    def create(link: Path, target: Path) -> Path:
        if os.name != "nt" or not hasattr(Path, "is_junction"):
            pytest.skip("capability unavailable: windows_junction")
        result = subprocess.run(
            ["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0 or not link.is_junction():
            pytest.skip("capability unavailable: windows_junction")
        return link
    return create


def test_replay_rejects_a_lexical_junction_run_root_before_resolving_it(
    tmp_path: Path,
    windows_junction_factory,
):
    physical_run = tmp_path / "physical-run"
    _write_buildout_metric_run(physical_run)
    junction_run = windows_junction_factory(
        tmp_path / "junction-run", physical_run
    )
    assert junction_run.is_junction()
    # Retain the existing render rejection and finally-block junction cleanup.
```

Delete `@pytest.mark.skipif(os.name != "nt", reason="Windows junction
regression")` and the test's inline `mklink` block. The fixture is the only
skip site and emits the exact Task 10 allowlisted reason.

- [ ] **Step 4: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_figure_store.py tests\test_figures.py tests\test_experiment_support.py -k "cache or generation or pointer or render or renderer or lock or journal or termination or concurrent" -q -p no:cacheprovider --basetemp=.pytest-wave-b-task8-red
```

- [ ] **Step 5: Implement validation and publication in this exact order**

`render_run()` first resolves `run_dir` and `output_dir` with the explicit
anchor/repo/Theory arguments; loads the run through `load_run_bundle`; rejects a
legacy run without the exact observation revision; validates ordered requests,
options, all metric/array inputs, source inventory, renderer source identity,
and only then the complete cache identity. It recomputes each persisted source
manifest/inventory digest from the verified buffers before constructing the
cache/config identity; no declared digest is trusted. These steps perform no write and create no
parent. The resolved output admission is retained as a
`ResolvedOutputRoot`, and `revalidate_output_root(output_admission)` is the
last call immediately before the first lock/mkdir/journal effect. Only then may
it create/acquire the sibling lock and recover a journal.

Render all outputs into the new sibling staging directory and validate
signatures/byte inventories. Write/fsync `figure-generation.json` and fsync
the staging directory. Atomically write/fsync the
`generation_prepared(generation_id)` journal and its parent *before* renaming
staging to `generations/{generation_id}/`; then rename and fsync the
generations parent. Atomically write/fsync `generation_installed`. Compute the
closed pointer bytes/temp name, atomically write/fsync
`pointer_preparing(pointer_temp_name)` and its parent *before* creating the
temp, then write/fsync the temp and its parent, advance/fsync
`pointer_prepared`, `os.replace` only the pointer, fsync its parent, and
advance/fsync `pointer_replaced`. Finally unlink the journal and fsync its
parent. If an identical generation already exists, verify it byte-for-byte and
reuse it; never overwrite it. `last-failure.json` may record a post-validation
failure but may not alter the active pointer or a generation.

Use `msvcrt.locking` on Windows and `fcntl.flock` on POSIX through one context manager. The OS lock determines live ownership; JSON owner metadata is diagnostic and replaced after successful acquisition. Recovery may delete only this invocation's validated sibling staging directory, may complete a pointer update only for a fully verified installed generation matching the journal, and may remove only a journal whose owner/cache identity it validated.

Task 8 owns `test_render_run_has_literal_domain_order` and
`test_invalid_root_or_source_digest_precedes_renderer_effects`. Their AST/event
spies require `root admission < verified run/source inventory authorization <
renderer source authorization < cache identity < root revalidation < lock or
mkdir < render < generation publication`. The negative test corrupts each
source manifest/inventory digest in turn and requires zero cache-hit lookup,
lock, journal, render, or filesystem calls. These tests are first collected in
Task 8, not Task 4.

Render to the exact expected filenames and validate PNG signature
`b"\x89PNG\r\n\x1a\n"`, PDF signature `b"%PDF-"`, nonzero size, and SHA before
the generation manifest. Write all JSON via `canonical_json_bytes`; flush and
`os.fsync` every payload, manifest, pointer temp, and affected directory.
Generation collision is accepted only after a byte-for-byte verification of
the complete existing generation. Unavailable renderer identity never takes
the active-cache fast path because its per-invocation nonce changes the key.

- [ ] **Step 6: Update renderer result validation**

`validated_renderer_status()` must validate `active-generation.json`, its manifest digest, the generation inventory, request order, run/cache binding, and returned figure paths under the selected immutable generation. Remove the requirement that image files and `figure-manifest.json` live directly under `output_dir`.

`load_active_figure_generation` applies the same fixed-root defaulting and
strict output-root admission, parses every JSON object with
`strict_json_from_bytes`, reconstructs the exact `FigureSourceBinding`, and
revalidates its source run before returning. Unknown/duplicate/nonfinite JSON,
a missing source, revision drift, eligibility drift, or cache/source mismatch
rejects. It performs no publication or recovery effect.

It accepts only the immutable `FigureManifest` returned by
`load_active_figure_generation`, compares its generation ID/cache digest/request
tuple with the expected verified run and options, and never reopens an
unverified caller path. `record_figure_failure_safely` may write only the closed
failure record after validation has admitted the output root; it never changes
the active pointer.

- [ ] **Step 7: Run GREEN and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_figure_store.py tests\test_figures.py tests\test_experiment_support.py -q -p no:cacheprovider --basetemp=.pytest-wave-b-task8-green
C:\Python314\python.exe -m ruff check --no-cache src/multiagent_elbo/figure_store.py src/multiagent_elbo/figures.py src/multiagent_elbo/rendering.py tests/test_figure_store.py tests/test_figures.py tests/test_experiment_support.py
C:\Python314\python.exe -m ruff format --check --no-cache src/multiagent_elbo/figure_store.py src/multiagent_elbo/figures.py src/multiagent_elbo/rendering.py tests/test_figure_store.py tests/test_figures.py tests/test_experiment_support.py
git add -- src/multiagent_elbo/figure_store.py src/multiagent_elbo/figures.py src/multiagent_elbo/rendering.py tests/test_figure_store.py tests/test_figures.py tests/test_experiment_support.py
git commit -m "feat: publish atomic figure generations"
```

### Task 9: Wire launchers, discovery, legacy replay, and exact historical pins

**Closes:** active-path reachability for `AUD-01`, `AUD-02`, and `AUD-10`; preserves historical compatibility.

**Files:** all thirteen top-level launcher/replay files in the File Responsibility Map, `tests/test_launchers.py`, `tests/test_gaussian_results_document.py`, `tests/test_gaussian_fixed_ray_diagnostic_experiment.py`, and `tests/test_gaussian_fixed_ray_experiment.py`.

**Closed launcher and historical inventories:**

```python
LAUNCHER_PATHS = (
    "run_finite_lab.py",
    "run_multiagent_network_lab.py",
    "run_attention_lab.py",
    "run_categorical_dqm_lab.py",
    "run_finite_counterexample_lab.py",
    "run_information_history_lab.py",
    "run_scale_cocycle_lab.py",
    "run_theory_oracle_lab.py",
    "run_gauge_holonomy_lab.py",
    "run_gaussian_lab.py",
    "run_gaussian_fixed_ray_diagnostic.py",
    "run_gaussian_fixed_ray_lab.py",
    "make_figures.py",
)
HISTORICAL_OBSERVATION_REVISIONS = {
    "2026-08-10-gaussian-confirmatory-fcb2c49":
        "fcb2c49efdca2ad3ee502dc08fbb82fc285e7a05",
    "2026-08-10-fixed-model-attraction-diagnostic":
        "039df35daa30a49e90f178edde7bfc999a7ee629",
}
PRODUCTION_RENDER_RUN_CALLERS = (
    ("make_figures.py", "_render_from_config"),
)
```

- [ ] **Step 1: Add literal arbitrary-CWD and resolved-config API RED tests**

Add to `tests/test_launchers.py`:

```python
@pytest.mark.parametrize("relative", LAUNCHER_PATHS)
def test_launcher_uses_declared_root_and_never_ambient_cwd(relative):
    source = Path(relative).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=relative)
    calls = {
        ast.unparse(node.func)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
    }
    assert "Path.cwd" not in calls
    assert "with_resolved_output_root" in calls
    assert re.search(
        r"ROOT\s*=\s*Path\(__file__\)\.resolve\(\)\.parent", source
    )


@pytest.mark.parametrize("module_name", [Path(path).stem for path in LAUNCHER_PATHS])
def test_launcher_absolute_override_is_cwd_independent(
    module_name, tmp_path, monkeypatch
):
    module = importlib.import_module(module_name)
    output = (tmp_path / "absolute-output").resolve()
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    monkeypatch.setitem(module.OUTPUT, "root", str(output))
    observed = []
    monkeypatch.setattr(
        module,
        module.RUNNER_NAME,
        lambda config, *args, **kwargs: observed.append(
            require_resolved_output_root(config).path
        ),
    )
    module.main()
    assert observed == [output]


def test_legacy_run_store_rejects_unresolved_config_before_effect(tmp_path):
    config = make_config(tmp_path / "runs")
    with pytest.raises(ValueError, match="not resolved"):
        RunStore.create(config, {"source": "legacy-test"})
    assert not (tmp_path / "runs").exists()


def test_render_run_signature_and_production_caller_inventory_are_compatible(
    valid_v2_run, tmp_path
):
    # Frozen Wave 0 positional call remains valid without root keywords.
    compatibility = render_run(
        valid_v2_run, tmp_path / "compatibility", ("overview",)
    )
    explicit = render_run(
        valid_v2_run,
        tmp_path / "explicit",
        ("overview",),
        anchor=ROOT,
        repo_root=ROOT,
        theory_root=ROOT / "Theory",
    )
    assert compatibility.requested == explicit.requested == ("overview",)
    discovered = discover_production_calls(
        symbol="render_run",
        tracked_python=git_tracked_python_paths(),
        exclude=("tests/", "src/multiagent_elbo/figures.py"),
    )
    assert discovered == set(PRODUCTION_RENDER_RUN_CALLERS)
```

Add the small public constants `RUNNER_NAME` and editable `OUTPUT` where a
launcher lacks them; they are test/discovery metadata, not a CLI. For
`make_figures.py`, the runner is a local `_render_from_config` adapter with the
same first `ExperimentConfig` argument. Each launcher defines `ROOT` from its
own file, resolves before hashing/dispatch, and passes the resolved config.
The test-only AST helpers above use `git ls-files -z -- '*.py'`, parse direct
and module-qualified calls, and return exact `(path, enclosing_callable)`
pairs. A newly added production caller fails until it is either migrated to the
explicit context or added to the frozen inventory; the compatibility call
continues to derive context from `figures.py`'s fixed module root.

Add a direct default-root integration test using a copied minimal repository
whose `.gitignore` contains `artifacts/`: execute the launcher module after
changing CWD elsewhere and assert the observed root equals
`copied_repo/artifacts`. Patch `Path.cwd()` to raise after module import; launcher,
discovery, `RunStore.create` with resolved config, and `render_run` must still
work. Downstream components call `require_resolved_output_root`; they do not
reconstruct or silently resolve raw spellings.

Task 9, not Task 4, adds
`test_every_launcher_admits_root_before_dispatch` and
`test_invalid_launcher_root_precedes_dispatch`. The first parses each exact
`LAUNCHER_PATHS` `main()` and requires the lexical call to
`with_resolved_output_root` before the callable named by `RUNNER_NAME`; a
runtime spy requires events exactly `("root_admission", "dispatch")`. The
second monkeypatches `with_resolved_output_root` to reject and every runner to
raise if called, then requires only `("root_admission",)` and byte-identical
source/output inventories. `make_figures.py` additionally must authorize the
loaded run/source manifest and inventory digests before its renderer/cache
identity or dispatch. These launcher controls are first collected after every
launcher in the frozen inventory has migrated.

- [ ] **Step 2: Add legacy replay and byte-pin RED tests**

Add to `tests/test_gaussian_results_document.py`:

```python
@pytest.mark.parametrize(
    "source,revision",
    [
        (CONFIRMATORY_EVIDENCE, HISTORICAL_OBSERVATION_REVISIONS[CONFIRMATORY_EVIDENCE.name]),
        (DIAGNOSTIC_EVIDENCE, HISTORICAL_OBSERVATION_REVISIONS[DIAGNOSTIC_EVIDENCE.name]),
    ],
)
def test_legacy_figure_replay_requires_exact_observation_revision(
    source, revision, tmp_path
):
    copied = tmp_path / "legacy" / source.name
    shutil.copytree(source, copied)
    destination = tmp_path / "figures" / source.name
    with pytest.raises(ValueError, match="legacy_observed_at_revision"):
        render_run(
            copied, destination, anchor=Path.cwd(), repo_root=Path.cwd(),
            theory_root=Path.cwd() / "Theory"
        )
    assert not destination.exists()
    result = render_run(
        copied, destination,
        anchor=Path.cwd(), repo_root=Path.cwd(), theory_root=Path.cwd() / "Theory",
        legacy_observed_at_revision=revision,
    )
    assert result.source_claim_eligible is False
```

Keep `CONFIRMATORY_TRACKED_INVENTORY` and `DIAGNOSTIC_TRACKED_INVENTORY` as
the literal Wave 0 size/SHA dictionaries already owned by this test. Add one
session-scoped autouse fixture that computes both recursive inventories before
tests and asserts exact equality afterward. Never regenerate these constants
from current bytes.

- [ ] **Step 3: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_launchers.py tests\test_gaussian_results_document.py tests\test_gaussian_fixed_ray_diagnostic_experiment.py tests\test_gaussian_fixed_ray_experiment.py -k "cwd or root or discovery or legacy or historical or manifest" -q -p no:cacheprovider --basetemp=.pytest-wave-b-task9-red
```

- [ ] **Step 4: Wire resolved values, not user spellings**

Every `main()` calls `with_resolved_output_root(config, anchor=ROOT,
repo_root=ROOT, theory_root=ROOT / "Theory")` before hashing or dispatch.
`make_figures.py` adds editable
`LEGACY_OBSERVED_AT_REVISION: str | None = None`, resolves source/output with the
shared resolver, and passes the revision explicitly. Freeze sentinel discovery
as:

```python
def _find_accepted_sentinel_run(
    config: ExperimentConfig,
    *,
    accepted_manifest_sha256: str,
    accepted_source_revision: str,
) -> VerifiedRunBundle:
    if re.fullmatch(r"[0-9a-f]{64}", accepted_manifest_sha256) is None:
        raise ValueError("accepted sentinel manifest SHA-256 is invalid")
    if re.fullmatch(r"[0-9a-f]{40}", accepted_source_revision) is None:
        raise ValueError("accepted sentinel source revision is invalid")
    output_root = revalidate_resolved_output_root(config).path
    namespace = sanitize_run_name(
        f"gaussian-fixed-ray-sentinel-{accepted_source_revision[:12]}"
    )
    accepted: list[VerifiedRunBundle] = []
    for manifest_path in sorted(
        output_root.rglob("manifest.json"),
        key=lambda path: path.relative_to(output_root).as_posix().encode("ascii"),
    ):
        relative = manifest_path.relative_to(output_root)
        # Actual run-v2 layout is namespace/config-hash-seed/manifest.json.
        if (
            len(relative.parts) != 3
            or relative.parts[0] != namespace
            or relative.parts[2] != "manifest.json"
        ):
            continue
        bundle = load_verified_run_bundle(manifest_path.parent)
        source = bundle.manifest["source_identity"]
        sentinel = bundle.json_payloads.get("sentinel_parity.json")
        if (
            bundle.manifest_sha256 == accepted_manifest_sha256
            and source.get("status") == "available"
            and source.get("git_commit") == accepted_source_revision
            and isinstance(sentinel, Mapping)
            and sentinel.get("schema_version")
            == "gaussian-fixed-ray-cuda-sentinel-v1"
        ):
            accepted.append(bundle)
    if len(accepted) != 1:
        raise ValueError("accepted sentinel must resolve uniquely")
    return accepted[0]
```

Discovery is genuinely recursive from the admitted output root so it reaches
the actual `run-name/config-hash-seed/manifest.json` layout; the exact
three-component filter prevents figure generations, sibling experiments,
staging directories, and nested decoys from becoming candidates. It never
reads a manifest directly. It may return only one strict v2 bundle whose exact
manifest SHA, available manifest source identity, full source revision,
namespace prefix, and sentinel payload schema all agree. Zero, multiple,
legacy, unavailable-source, wrong-revision, wrong-namespace, or same-SHA decoy
candidates reject. The caller passes `accepted.run_dir` to the confirmatory
publisher and binds both accepted SHA and source revision into its provenance.
It never evaluates `ROOT / str(OUTPUT["root"])` or consults CWD. Wave C later
strengthens execution identity; Wave B supplies canonical root, recursive
layout discovery, strict schema dispatch, and SHA/revision binding.

Add RED controls that construct two complete v2 sentinel bundles at the actual
recursive layout plus decoys at one-level, deeper, staging, figure-generation,
wrong namespace, wrong source revision, and unavailable-source paths. Require
only the unique exact SHA/revision candidate to resolve. A second exact
candidate must fail closed. Patch `Path.glob`, direct `read_bytes`, and
`json.loads` in the launcher to raise, proving discovery uses `rglob` plus
`load_verified_run_bundle`. Assert the returned bundle's
`manifest_sha256`, source `git_commit`, and sentinel schema before any
confirmatory gate or worker mock is called.

- [ ] **Step 5: Normalize deterministic skip reasons**

Replace environment-dependent exception text with these exact lowercase reasons:

```python
pytest.skip("capability unavailable: hard_link")
pytest.skip("capability unavailable: symbolic_link")
pytest.skip("capability unavailable: windows_junction")
```

The only CUDA skip allowed in the full CPU suite is
`tests.test_cuda_backend::test_pinned_cuda_worker_runs_first_job_with_determinism_environment`
with exact reason `requires explicit dedicated CUDA-lane opt-in`. The wrapper in
Task 10 binds actual skip IDs/reasons; substring or prefix matching is forbidden.

- [ ] **Step 6: Run GREEN and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_launchers.py tests\test_gaussian_results_document.py tests\test_gaussian_fixed_ray_diagnostic_experiment.py tests\test_gaussian_fixed_ray_experiment.py -q -p no:cacheprovider --basetemp=.pytest-wave-b-task9-green
git diff --exit-code -- docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49 docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic
git add -- run_finite_lab.py run_multiagent_network_lab.py run_attention_lab.py run_categorical_dqm_lab.py run_finite_counterexample_lab.py run_information_history_lab.py run_scale_cocycle_lab.py run_theory_oracle_lab.py run_gauge_holonomy_lab.py run_gaussian_lab.py run_gaussian_fixed_ray_diagnostic.py run_gaussian_fixed_ray_lab.py make_figures.py tests/test_launchers.py tests/test_gaussian_results_document.py tests/test_gaussian_fixed_ray_diagnostic_experiment.py tests/test_gaussian_fixed_ray_experiment.py tests/test_artifacts.py tests/test_experiment_support.py
git commit -m "fix: unify publication and discovery roots"
```

### Task 10: Freeze the Wave B evidence and ledger wrapper

**Files:**

- Create: `tools/build_wave_b_evidence.py`
- Create: `tests/test_wave_b_evidence.py`
- Create: `docs/verification/remediation/wave-b-domain-evidence-v1.schema.json`

**Interfaces:**

- Import Wave 0's `PreparedEvidenceFile`, `PreparedEvidenceBundle`,
  `prepare_evidence_bundle`, `publish_evidence_bundle`,
  `build_evidence_index`, and `validate_evidence_index` without wrappers that
  change their signatures.
- Import Wave 0's frozen `CLAIM_CRITERIA_BY_DOMAIN` from
  `tools/build_wave0_evidence.py` as the criterion-key authority. Wave B may
  bind controls and fixed scores to those keys but may not rename or relabel
  them.
- Consume Wave 0's generic `resolve-verification-gate --snapshot PATH --root
  DIR` CLI unchanged with snapshot
  `docs/verification/remediation/verification-contract-v1.json` and active
  root `C:\Users\chris and christine\.codex\skills\verification`; Task 10
  tests require byte drift or a different root to fail and the snapshot-bound
  active Codex gate to be returned. Do not add a local resolver or fallback.
- Expose exactly `build --stage {candidate,closure} --tested-head SHA
  --implementation-parent SHA --raw-dir PATH --output-dir PATH`,
  `review-context-sha --tested-head SHA --implementation-parent SHA --raw-dir
  PATH`, `validate-reviews --tested-head SHA --implementation-parent SHA
  --raw-dir PATH`, and `populate-ledger --ledger PATH --closure-index PATH`.
- Build root `remediation-evidence-v1` bytes first in memory. Build the separate
  domain index second so it points to the root index and never vice versa. Do
  not mutate a frozen carrier in place. Construct one `PreparedEvidenceBundle`
  whose file tuple contains the root files plus domain/review files, then call
  the generic atomic publisher exactly once.
- Preserve Wave 0's production carrier exactly as
  `PreparedEvidenceBundle(output_dir: PurePosixPath,
  files: tuple[PreparedEvidenceFile, ...])`. Do not add mapping methods,
  `raw_reviews`, or any other field. `PreparedClosureHarness` below exists only
  in `tests/test_wave_b_evidence.py`; its read-only path/role maps are derived
  from immutable `PreparedEvidenceFile` tuples and never enter production.

The exact suites remain:

```python
TARGETED_TESTS = (
    "tests/test_remediation_contracts.py", "tests/test_remediation_evidence.py",
    "tests/test_artifact_schema.py", "tests/test_artifacts.py",
    "tests/test_output_paths.py", "tests/test_experiment_support.py",
    "tests/test_runtime.py", "tests/test_figure_store.py",
    "tests/test_figures.py", "tests/test_launchers.py",
    "tests/test_finite_experiment.py", "tests/test_agent_network_experiment.py",
    "tests/test_attention_experiment.py", "tests/test_categorical_dqm_experiment.py",
    "tests/test_counterexample_experiment.py", "tests/test_information_history_experiment.py",
    "tests/test_scale_cocycle_experiment.py", "tests/test_theory_oracle_experiment.py",
    "tests/test_holonomy_experiment.py", "tests/test_gaussian_realization.py",
    "tests/test_gaussian_fixed_ray_diagnostic_experiment.py",
    "tests/test_gaussian_fixed_ray_experiment.py",
    "tests/test_gaussian_confirmatory_experiment.py",
    "tests/test_gaussian_results_document.py", "tests/test_wave_b_evidence.py",
)
SUBSYSTEM_TESTS = TARGETED_TESTS + (
    "tests/test_config.py", "tests/test_agent_network.py",
    "tests/test_counterexamples.py", "tests/test_theory_oracles.py",
    "tests/test_gaussian_fixed_ray_diagnostics.py",
    "tests/test_shared_scientific_contracts.py", "tests/test_cuda_backend.py",
)
```

Freeze exact skip maps; an allowed capability skip may be absent, but every
actual skip must match both ID and reason byte-for-byte:

```python
CAPABILITY_SKIPS = {
    "tests.test_artifacts::test_finalize_rejects_a_declared_symlink":
        "capability unavailable: symbolic_link",
    "tests.test_artifacts::test_finalize_rejects_a_declared_file_with_an_external_hard_link":
        "capability unavailable: hard_link",
    "tests.test_artifacts::test_finalize_rejects_an_external_hard_link_to_core_config":
        "capability unavailable: hard_link",
    "tests.test_artifacts::test_finalize_rejects_duplicate_file_identity_within_inventory":
        "capability unavailable: hard_link",
    "tests.test_experiment_support::test_validated_renderer_status_rejects_a_publication_symlink_escape":
        "capability unavailable: symbolic_link",
    "tests.test_figures::test_replay_rejects_a_lexical_junction_run_root_before_resolving_it":
        "capability unavailable: windows_junction",
    "tests.test_artifact_schema::test_v2_loader_rejects_symlink_entry":
        "capability unavailable: symbolic_link",
    "tests.test_artifact_schema::test_v2_loader_rejects_windows_junction_entry":
        "capability unavailable: windows_junction",
    "tests.test_artifact_schema::test_v2_loader_rejects_external_hard_link_entry":
        "capability unavailable: hard_link",
    "tests.test_output_paths::test_symlink_component_into_theory_rejects_without_effect":
        "capability unavailable: symbolic_link",
    "tests.test_output_paths::test_windows_junction_component_into_theory_rejects_without_effect":
        "capability unavailable: windows_junction",
    "tests.test_output_paths::test_cached_external_root_rejects_late_reparse_without_effect[symbolic_link]":
        "capability unavailable: symbolic_link",
    "tests.test_output_paths::test_cached_external_root_rejects_late_reparse_without_effect[windows_junction]":
        "capability unavailable: windows_junction",
}
CUDA_SKIP = {
    "tests.test_cuda_backend::test_pinned_cuda_worker_runs_first_job_with_determinism_environment":
        "requires explicit dedicated CUDA-lane opt-in",
}
SKIP_ALLOWLIST_BY_SUITE = {
    "targeted": CAPABILITY_SKIPS,
    "subsystem": CAPABILITY_SKIPS | CUDA_SKIP,
    "full": CAPABILITY_SKIPS | CUDA_SKIP,
}
```

The named link/reparse tests are mandatory names, not examples. The late
reparse test is parameterized with exactly the two IDs shown. Before evidence,
`tests/test_wave_b_evidence.py` AST-discovers every `pytest.skip`,
`pytest.mark.skip`, and `pytest.mark.skipif` in the three frozen suite
closures and requires its fully expanded node ID/reason pair to occur in
`SKIP_ALLOWLIST_BY_SUITE`; it also requires every allowlisted node ID to
collect in at least one owning suite (it may pass rather than skip when the
capability exists). Dynamic exception text and uncollected stale allowlist
entries fail. This is the complete skip surface: capability rows above plus the
single CUDA row, with no prefix, regex, or substring matching.

Freeze Wave B's tested-input and source-binding policy as these literal rules:

```python
WAVE_B_SELECTION_RULES = (
    "prefix:src/", "prefix:tests/", "prefix:Theory/", "prefix:tools/",
    "top_level_suffix:.py", "exact:pyproject.toml", "exact:.gitignore",
    "exact:.gitattributes", "exact:environments/cuda-rtx5090-cu128.lock.txt",
    "exact:docs/audits/2026-08-11-post-fixed-ray-deep-audit.md",
    "exact:docs/superpowers/specs/2026-08-11-scientific-integrity-remediation-program-design.md",
    "exact:docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-b.md",
    "prefix:docs/verification/remediation/",
)
WAVE_B_EXCLUSION_RULES = (
    "prefix:docs/verification/evidence/", "prefix:verification-evidence/",
    "prefix:.verification/", "prefix:.pytest_cache/", "prefix:.pytest-",
)
WAVE_B_REQUIRED_SOURCE_CONFIG_PATHS = (
    ".gitattributes", ".gitignore", "pyproject.toml",
    "docs/audits/2026-08-11-post-fixed-ray-deep-audit.md",
    "docs/superpowers/specs/2026-08-11-scientific-integrity-remediation-program-design.md",
    "docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-b.md",
    "tools/remediation_evidence.py", "tools/build_wave_b_evidence.py",
    "tests/test_remediation_contracts.py", "tests/test_remediation_evidence.py",
    "tests/test_wave_b_evidence.py",
)
WAVE_B_REVIEWED_PLAN_PATH = (
    "docs/superpowers/plans/"
    "2026-08-11-scientific-integrity-remediation-wave-b.md"
)
WAVE_B_DEPENDENCY_INPUTS = (
    "pyproject.toml",
    "environments/cuda-rtx5090-cu128.lock.txt",
    "docs/verification/remediation/verification-contract-v1.json",
)
```

The policy resolver discovers its own sorted `inputs` from Git, adds every
tracked regular file below `docs/verification/remediation/` to the exact
required source/config paths above, and rejects a matching untracked path,
caller-supplied omission, case-fold alias, symlink/reparse input, missing file,
or ordering drift. It never binds untracked `uv.lock`. The third dependency is
the Wave 0 verifier snapshot, in the literal order above. `plan-binding.json`
binds the exact reviewed Wave B plan path
`docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-b.md`,
its current size/SHA-256, and the concrete commit returned by
`git log -n 1 --format=%H -- <plan-path>`. That commit must be an ancestor of
both `P` and `E`, and its plan blob must equal the tested plan bytes; callers
cannot supply or override the plan commit.

The domain schema has exactly these shapes:

```python
GENERIC_PUBLIC_PATHS = (
    "commands/full.json",
    "commands/subsystem.json",
    "commands/targeted.json",
    "dependencies.json",
    "environment.json",
    "full.xml",
    "index.json",
    "plan-binding.json",
    "privacy-transform.json",
    "subsystem.xml",
    "targeted.xml",
)
DOMAIN_INDEX_PATH = "wave-b-domain-index.json"
CANDIDATE_PUBLIC_PATHS = GENERIC_PUBLIC_PATHS + (DOMAIN_INDEX_PATH,)
VIEW_IDS = ("code-runtime", "artifact-concurrency")
REVIEW_PATHS = (
    "reviews/code-runtime.json",
    "reviews/artifact-concurrency.json",
)
DOMAIN_INDEX_KEYS = {
    "schema_version", "wave", "evidence_stage", "tested_git_head",
    "implementation_parent_git_head", "root_index", "required_controls",
    "claim_specs", "review_policy", "reviews", "adjudicators",
}
FILE_BINDING_KEYS = {"path", "size_bytes", "sha256"}
RAW_REVIEW_KEYS = {
    "schema_version", "view_id", "calibration_kind", "tested_git_head",
    "implementation_parent_git_head", "reviewed_input_inventory_sha256",
    "reviewed_paths", "claim_scores", "verdict", "escalation_triggers",
    "unresolved_disagreement", "open_obligations", "result_location",
    "falsification_conditions",
}
RAW_CLAIM_SCORE_KEYS = {
    "claim_id", "domain", "severity", "evidence_ids", "criteria",
    "candidate_ids", "candidate_descriptions", "comparison_order",
    "comparison_outcome", "comparison_criteria", "verdict",
    "escalation_triggers", "unresolved_disagreement", "open_obligations",
}
RAW_ADJUDICATOR_KEYS = {
    "schema_version", "role", "claim_id", "tested_git_head",
    "implementation_parent_git_head", "reviewed_input_inventory_sha256",
    "escalation_triggers", "escalation_target", "view_ids", "result",
    "evidence_ids", "result_location", "reason", "falsification_condition",
    "open_obligations",
}
REVIEW_SCHEMA_VERSION = "wave-b-review-v1"
ADJUDICATOR_SCHEMA_VERSION = "wave-b-adjudicator-v1"
CALIBRATION_KIND = "independent_pairwise_source_reading_v1"
CANDIDATE_IDS = ("claim-statement", "explicit-negation")
FROZEN_REVIEW_ESCALATION_TARGET = 2
ADJUDICATOR_RESULTS = ("support", "refute", "abstain")
ADJUDICATOR_RESULT_TO_LEDGER_STATE = {
    "support": "EVIDENCE_VERIFIED",
    "refute": "REFUTED",
    "abstain": "INCONCLUSIVE",
}
METRIC_TRUTH_CONTROL_IDS = tuple(
    "tests.test_experiment_support::test_metric_v2_truth_table[" + case + "]"
    for case in (
        "within-lower-pass", "within-below-lower-fail", "within-target-pass",
        "within-upper-pass", "within-above-upper-fail", "at-most-below-pass",
        "at-most-inclusive-upper-pass", "at-most-inclusive-above-fail",
        "at-most-strict-below-pass", "at-most-strict-boundary-fail",
        "at-most-strict-upper-fail", "at-least-above-pass",
        "at-least-inclusive-lower-pass", "at-least-inclusive-below-fail",
        "at-least-strict-above-pass", "at-least-strict-boundary-fail",
        "at-least-strict-lower-fail", "expected-infinity-pass",
        "expected-infinity-one-fail", "expected-infinity-max-finite-fail",
    )
)
CARRIER_CONTROL_IDS = tuple(
    "tests.test_shared_scientific_contracts::"
    "test_recursive_candidate_validation_covers_every_closed_carrier[" + name + "]"
    for name in (
        "MetricRecord", "PremiseAssessment", "CandidateRecord",
        "TwoScaleApplicationOracle", "TheoremAssumptionRecord",
        "HolonomyExperimentResult",
    )
)
PAYLOAD_FACTORY_CONTROL_IDS = tuple(
    "tests.test_shared_scientific_contracts::"
    "test_recursive_candidate_validation_covers_every_payload_factory[" + name + "]"
    for name in (
        "analyze_primary", "analyze_holdout", "adjacent_support_certificate",
        "spectral_diagnostics", "diagnose_trajectory",
        "summarize_population", "run_holonomy_experiment",
    )
)
RUN_CRASH_CONTROL_IDS = tuple(
    "tests.test_artifact_schema::"
    "test_process_crash_recovery_at_every_publication_boundary[" + boundary + "]"
    for boundary in (
        "after_stage_mkdir", "after_marker_fsync",
        "after_each_artifact_fsync", "after_stage_readback",
        "before_manifest_write", "after_manifest_fsync",
        "after_stage_manifest_dir_fsync", "before_marker_remove",
        "after_marker_remove", "after_marker_remove_dir_fsync",
        "before_stage_rename", "after_stage_rename", "after_parent_fsync",
    )
)
FIGURE_BOUNDARY_IDS = (
    "after_journal_rendering", "after_each_render",
    "after_generation_manifest_fsync", "after_journal_generation_prepared",
    "after_generation_rename", "after_generation_parent_fsync",
    "after_journal_generation_installed", "after_journal_pointer_preparing",
    "after_pointer_temp_fsync", "after_pointer_temp_parent_fsync",
    "after_journal_pointer_prepared", "after_pointer_replace",
    "after_pointer_parent_fsync", "after_journal_pointer_replaced",
    "before_journal_remove", "after_journal_remove",
    "after_journal_parent_fsync",
)
FIGURE_EXCEPTION_CONTROL_IDS = tuple(
    "tests.test_figure_store::"
    "test_exception_boundary_preserves_one_complete_active_generation[" + boundary + "]"
    for boundary in FIGURE_BOUNDARY_IDS
)
FIGURE_CRASH_CONTROL_IDS = tuple(
    "tests.test_figure_store::"
    "test_process_termination_recovers_all_old_or_all_new[" + boundary + "]"
    for boundary in FIGURE_BOUNDARY_IDS
)

REQUIRED_CONTROLS = {
    "AUD-01": (
        "tests.test_artifact_schema::test_v2_loader_rejects_closed_tamper_matrix[size]",
        "tests.test_artifact_schema::test_v2_loader_rejects_closed_tamper_matrix[sha256]",
        "tests.test_artifact_schema::test_verified_loader_reads_each_owned_file_once_and_parses_same_buffer",
        "tests.test_artifact_schema::test_strict_json_reader_rejects_duplicate_and_nonfinite_tokens",
        "tests.test_artifact_schema::test_verified_npz_reader_rejects_noncanonical_zip_npy_matrix",
        "tests.test_artifact_schema::test_source_identity_typed_round_trip_and_failure_matrix",
        "tests.test_artifact_schema::test_prepared_snapshot_is_detached_through_publish_and_load",
        "tests.test_gaussian_results_document::test_source_binding_pins_the_complete_original_inventory",
        "tests.test_gaussian_results_document::test_fixed_model_diagnostic_extract_has_exact_bound_inventory",
    ) + RUN_CRASH_CONTROL_IDS,
    "AUD-02": FIGURE_EXCEPTION_CONTROL_IDS + FIGURE_CRASH_CONTROL_IDS + (
        "tests.test_figure_store::test_figure_recovery_table_covers_every_phase_and_boundary",
        "tests.test_figure_store::test_valid_cache_mutation_matrix_is_complete",
        "tests.test_figure_store::test_source_validation_failure_precedes_every_figure_path[source_manifest]",
        "tests.test_figure_store::test_two_publishers_and_reader_never_observe_mixed_generation",
        "tests.test_figure_store::test_live_lock_wins_and_stale_metadata_is_replaced_after_termination",
        "tests.test_figure_store::test_success_never_deletes_old_generation",
    ),
    "AUD-04": METRIC_TRUTH_CONTROL_IDS + (
        "tests.test_experiment_support::test_metric_v2_complete_invalid_matrix",
        "tests.test_experiment_support::test_metric_v2_complete_serialization_invalid_matrix",
        "tests.test_experiment_support::test_inapplicable_metric_is_never_passing",
        "tests.test_experiment_support::test_metric_v2_payload_is_closed_and_loader_recomputes_decision",
        "tests.test_experiment_support::test_metric_state_and_decision_are_not_constructor_inputs",
        "tests.test_experiment_support::test_wave_zero_metric_aliases_are_exact_shared_type",
    ),
    "AUD-05": CARRIER_CONTROL_IDS + PAYLOAD_FACTORY_CONTROL_IDS + (
        "tests.test_shared_scientific_contracts::test_all_public_producer_state_fields_are_non_init_candidate_literals",
        "tests.test_shared_scientific_contracts::test_no_production_source_emits_promoted_or_legacy_calculation_state",
        "tests.test_shared_scientific_contracts::test_producer_state_source_inventory_is_complete",
        "tests.test_shared_scientific_contracts::test_active_publication_inventory_is_complete_and_uses_v2_only",
    ),
    "AUD-10": (
        "tests.test_output_paths::test_relative_root_uses_declared_anchor_not_cwd",
        "tests.test_output_paths::test_ignored_root_with_tracked_descendant_rejects",
        "tests.test_runtime::test_provenance_rejects_output_exclusion_mismatch",
        "tests.test_output_paths::test_root_policy_matrix_is_complete",
        "tests.test_output_paths::test_cached_ignored_root_is_revalidated_before_effect",
        "tests.test_shared_scientific_contracts::test_every_publication_callable_has_literal_domain_order",
        "tests.test_shared_scientific_contracts::test_invalid_root_precedes_all_producer_effects",
    ),
    "AUD-11": (
        "tests.test_artifact_schema::test_prepare_rejects_noncanonical_npz_array[object]",
        "tests.test_artifact_schema::test_prepare_rejects_noncanonical_npz_array[big-endian-float64]",
        "tests.test_artifact_schema::test_npz_finiteness_policy_is_closed[positive-infinity-rejected]",
        "tests.test_artifact_schema::test_npz_finiteness_policy_is_closed[negative-infinity-rejected]",
        "tests.test_artifact_schema::test_npz_finiteness_policy_is_closed[old-exception-policy-rejected]",
        "tests.test_artifact_schema::test_v2_loader_rejects_closed_tamper_matrix[pickle_npz]",
        "tests.test_artifact_schema::test_verified_npz_reader_rejects_noncanonical_zip_npy_matrix",
        "tests.test_artifact_schema::test_strict_json_reader_rejects_duplicate_and_nonfinite_tokens",
    ),
    "AUD-12": (
        "tests.test_runtime::test_rng_spawn_provenance_mutation_changes_neither_seed_material_nor_draws",
        "tests.test_runtime::test_rng_refactor_matches_independent_seedsequence_oracle[0]",
        "tests.test_runtime::test_rng_refactor_matches_independent_seedsequence_oracle[1]",
        "tests.test_runtime::test_rng_refactor_matches_independent_seedsequence_oracle[271828]",
        "tests.test_runtime::test_rng_refactor_matches_independent_seedsequence_oracle[9223372036854775807]",
        "tests.test_runtime::test_rng_direct_construction_is_not_a_spawn_key_injection_seam",
    ),
}
CROSS_AUDIT_REUSED_CONTROLS = {
    "tests.test_artifact_schema::test_strict_json_reader_rejects_duplicate_and_nonfinite_tokens":
        ("AUD-01", "AUD-11"),
    "tests.test_artifact_schema::test_verified_npz_reader_rejects_noncanonical_zip_npy_matrix":
        ("AUD-01", "AUD-11"),
}
```

The named nonparameterized matrix/meta controls above are required
implementations: each loops the corresponding frozen case tuple and asserts it
is nonempty, unique, and exactly equal to the parameter-ID inventory used by
the owning tests. `test_figure_recovery_table_covers_every_phase_and_boundary`
requires all six phases and every `FIGURE_BOUNDARIES` member;
`test_success_never_deletes_old_generation` snapshots every prior generation.
`test_every_publication_callable_has_literal_domain_order` and
`test_invalid_root_precedes_all_producer_effects` cover every callable in
`ACTIVE_PUBLICATION_CALLABLES`, not one representative. The evidence wrapper
expands these constants, rejects a duplicate within any one audit tuple, and
requires every exact node to pass in the JUnit union. Across audits there are
exactly 126 bindings and 124 unique node IDs. The only permitted cross-audit
reuse is `CROSS_AUDIT_REUSED_CONTROLS`: the strict JSON and canonical NPZ reader
controls each bind both `AUD-01` and `AUD-11`. Any third duplicate, changed
owner tuple, changed count, or uncollected node fails.

The owning tasks also implement these literal nonparameterized controls in
their already-listed test files. Rename the inline Task 1 invalid tables to
`COMPARATOR_INVALID_CASES` and `SERIALIZATION_INVALID_CASES`; define
`SOURCE_IDENTITY_INVALID_CASES`, `STRICT_JSON_INVALID_BYTES`,
`NPZ_READER_MUTATIONS`, and the figure/root table constants from the exact
matrices above. The test-only `make_valid_run_copy`,
`apply_noncanonical_npz_mutation`, `assert_publication_callable_order`, and
`invoke_callable_with_invalid_root` helpers are closed match/AST helpers in
the named owning test modules and reject an unknown case:

```python
def test_required_control_binding_counts_and_duplicate_policy():
    owners_by_node: dict[str, list[str]] = {}
    for audit_id, controls in REQUIRED_CONTROLS.items():
        assert len(controls) == len(set(controls))
        for node_id in controls:
            owners_by_node.setdefault(node_id, []).append(audit_id)
    assert sum(len(controls) for controls in REQUIRED_CONTROLS.values()) == 126
    assert len(owners_by_node) == 124
    reused = {
        node_id: tuple(owners)
        for node_id, owners in owners_by_node.items()
        if len(owners) > 1
    }
    assert reused == CROSS_AUDIT_REUSED_CONTROLS


def test_metric_v2_complete_invalid_matrix():
    assert len(COMPARATOR_INVALID_CASES) == 16
    for values, message in COMPARATOR_INVALID_CASES:
        with pytest.raises((TypeError, ValueError), match=message):
            MetricComparator(**values)


def test_metric_v2_complete_serialization_invalid_matrix():
    assert len(SERIALIZATION_INVALID_CASES) == 11
    for mutate, message in SERIALIZATION_INVALID_CASES:
        payload = _valid_metric_payload()
        mutate(payload)
        with pytest.raises((TypeError, ValueError), match=message):
            load_metric_record(payload)


VALID_AVAILABLE_SOURCE_PAYLOAD = {
    "status": "available",
    "git_commit": "a" * 40,
    "git_dirty": False,
    "git_status_sha256": "b" * 64,
    "dirty_tree_sha256": "c" * 64,
    "theory_sha256": "d" * 64,
}
SOURCE_IDENTITY_INVALID_CASES = (
    VALID_AVAILABLE_SOURCE_PAYLOAD | {"git_commit": True},
    VALID_AVAILABLE_SOURCE_PAYLOAD | {"git_commit": "a" * 12},
    VALID_AVAILABLE_SOURCE_PAYLOAD | {"git_status_sha256": True},
    VALID_AVAILABLE_SOURCE_PAYLOAD | {"dirty_tree_sha256": "C" * 64},
    VALID_AVAILABLE_SOURCE_PAYLOAD | {"extra": 1},
    {
        key: value for key, value in VALID_AVAILABLE_SOURCE_PAYLOAD.items()
        if key != "theory_sha256"
    },
    {"status": "unavailable", "reason": ""},
    {"status": "missing", "reason": "not available"},
    {"status": "unavailable", "reason": "not available", "git_commit": "a" * 40},
)


def test_source_identity_typed_round_trip_and_failure_matrix():
    identities = (
        AvailableSourceIdentity(
            git_commit="a" * 40,
            git_dirty=False,
            git_status_sha256="b" * 64,
            dirty_tree_sha256="c" * 64,
            theory_sha256="d" * 64,
        ),
        UnavailableSourceIdentity(reason="source metadata unavailable"),
    )
    assert len(SOURCE_IDENTITY_INVALID_CASES) == 9
    for identity in identities:
        payload = source_identity_payload(identity)
        assert type(payload) is dict
        assert parse_source_identity(payload) == identity
    for payload in SOURCE_IDENTITY_INVALID_CASES:
        with pytest.raises((TypeError, ValueError)):
            parse_source_identity(copy.deepcopy(payload))
    with pytest.raises(TypeError):
        source_identity_payload(source_identity_payload(identities[0]))


STRICT_JSON_INVALID_BYTES = (
    b'{"x":1,"x":2}', b'{"x":{"y":1,"y":2}}',
    b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}',
    b'{"x":1e999}', b'{"x":-1e999}',
)


def test_strict_json_reader_rejects_duplicate_and_nonfinite_tokens():
    for content in STRICT_JSON_INVALID_BYTES:
        with pytest.raises(ValueError):
            strict_json_from_bytes(content)


def test_verified_npz_reader_rejects_noncanonical_zip_npy_matrix(
    tmp_path,
):
    assert NPZ_READER_MUTATIONS == (
        "member_order", "member_name", "case_alias", "zip_comment",
        "member_extra", "compression", "timestamp", "create_system",
        "external_attr", "npy_version", "fortran_order", "dtype",
        "shape", "nonfinite",
    )
    for mutation in NPZ_READER_MUTATIONS:
        copied = make_valid_run_copy(tmp_path / mutation)
        apply_noncanonical_npz_mutation(copied, mutation)
        with pytest.raises((TypeError, ValueError)):
            load_verified_run_bundle(copied)


def test_root_policy_matrix_is_complete():
    assert ROOT_POLICY_CASE_IDS == (
        "relative-anchor", "equivalent-spellings", "theory-equal",
        "theory-ancestor", "theory-descendant", "repo-equal",
        "repo-ancestor", "ignored-untracked-descendant",
        "tracked-descendant", "symbolic-link", "windows-junction",
        "nonexistent-external-no-effect",
    )


def test_every_publication_callable_has_literal_domain_order():
    for path, callable_name, _ in ACTIVE_PUBLICATION_CALLABLES:
        assert_publication_callable_order(
            Path(path), callable_name,
            (
                "root_admission", "input_source_digest_authorization",
                "config_identity_rng", "root_admission_revalidated",
                "gate", "worker", "publication",
            ),
        )


def test_invalid_root_precedes_all_producer_effects(tmp_path):
    for path, callable_name, _ in ACTIVE_PUBLICATION_CALLABLES:
        counters = invoke_callable_with_invalid_root(
            Path(path), callable_name, tmp_path
        )
        assert counters == {
            "source_digest": 0, "config_hash": 0, "rng": 0,
            "gate": 0, "worker": 0, "filesystem": 0,
        }


def test_figure_recovery_table_covers_every_phase_and_boundary():
    assert FIGURE_JOURNAL_PHASES == (
        "rendering", "generation_prepared", "generation_installed",
        "pointer_preparing", "pointer_prepared", "pointer_replaced",
    )
    assert FIGURE_BOUNDARIES == (
        "after_journal_rendering", "after_each_render",
        "after_generation_manifest_fsync",
        "after_journal_generation_prepared", "after_generation_rename",
        "after_generation_parent_fsync",
        "after_journal_generation_installed",
        "after_journal_pointer_preparing", "after_pointer_temp_fsync",
        "after_pointer_temp_parent_fsync",
        "after_journal_pointer_prepared", "after_pointer_replace",
        "after_pointer_parent_fsync", "after_journal_pointer_replaced",
        "before_journal_remove", "after_journal_remove",
        "after_journal_parent_fsync",
    )


def test_success_never_deletes_old_generation(active_old_generation):
    before = active_old_generation.snapshot_all_generations()
    active_old_generation.render_successfully()
    after = active_old_generation.snapshot_all_generations()
    assert set(before) < set(after)
    assert all(after[name] == content for name, content in before.items())


def test_valid_cache_mutation_matrix_is_complete():
    assert CACHE_MUTATIONS == (
        "new_valid_source_manifest", "new_valid_source_payload",
        "renderer_git_commit", "renderer_dirty_tree", "renderer_file_byte",
        "png_dpi", "request_order",
    )
```

The two historical source-binding controls are preexisting Wave 0 byte-pin
tests retained under their exact names; Task 9's before/after inventory fixture
keeps their literal constants authoritative. No REQUIRED_CONTROL name is
prose-only.

The claim criteria are not generic quality labels. Freeze this exact
criterion-to-control map; every tuple is nonempty and every named control must
belong to that audit's `REQUIRED_CONTROLS` tuple:

```python
CODE_CRITERION_KEYS = (
    "execution",
    "input_output_behavior",
    "boundary_failure_behavior",
    "regression_coverage",
    "configuration_reachability",
    "reproducibility",
)
CLAIM_CRITERION_CONTROLS = {
    "AUD-01": {
        "execution": (
            "tests.test_artifact_schema::test_verified_loader_reads_each_owned_file_once_and_parses_same_buffer",
        ),
        "input_output_behavior": (
            "tests.test_artifact_schema::test_strict_json_reader_rejects_duplicate_and_nonfinite_tokens",
            "tests.test_artifact_schema::test_verified_npz_reader_rejects_noncanonical_zip_npy_matrix",
        ),
        "boundary_failure_behavior": RUN_CRASH_CONTROL_IDS,
        "regression_coverage": (
            "tests.test_artifact_schema::test_v2_loader_rejects_closed_tamper_matrix[size]",
            "tests.test_artifact_schema::test_v2_loader_rejects_closed_tamper_matrix[sha256]",
        ),
        "configuration_reachability": (
            "tests.test_artifact_schema::test_source_identity_typed_round_trip_and_failure_matrix",
        ),
        "reproducibility": (
            "tests.test_artifact_schema::test_prepared_snapshot_is_detached_through_publish_and_load",
            "tests.test_gaussian_results_document::test_source_binding_pins_the_complete_original_inventory",
        ),
    },
    "AUD-02": {
        "execution": FIGURE_EXCEPTION_CONTROL_IDS,
        "input_output_behavior": (
            "tests.test_figure_store::test_two_publishers_and_reader_never_observe_mixed_generation",
        ),
        "boundary_failure_behavior": FIGURE_CRASH_CONTROL_IDS,
        "regression_coverage": (
            "tests.test_figure_store::test_success_never_deletes_old_generation",
            "tests.test_figure_store::test_figure_recovery_table_covers_every_phase_and_boundary",
        ),
        "configuration_reachability": (
            "tests.test_figure_store::test_source_validation_failure_precedes_every_figure_path[source_manifest]",
        ),
        "reproducibility": (
            "tests.test_figure_store::test_valid_cache_mutation_matrix_is_complete",
        ),
    },
    "AUD-04": {
        "execution": METRIC_TRUTH_CONTROL_IDS,
        "input_output_behavior": (
            "tests.test_experiment_support::test_metric_v2_payload_is_closed_and_loader_recomputes_decision",
        ),
        "boundary_failure_behavior": (
            "tests.test_experiment_support::test_metric_v2_complete_invalid_matrix",
            "tests.test_experiment_support::test_metric_v2_complete_serialization_invalid_matrix",
        ),
        "regression_coverage": (
            "tests.test_experiment_support::test_metric_state_and_decision_are_not_constructor_inputs",
        ),
        "configuration_reachability": (
            "tests.test_experiment_support::test_wave_zero_metric_aliases_are_exact_shared_type",
        ),
        "reproducibility": METRIC_TRUTH_CONTROL_IDS,
    },
    "AUD-05": {
        "execution": CARRIER_CONTROL_IDS,
        "input_output_behavior": PAYLOAD_FACTORY_CONTROL_IDS,
        "boundary_failure_behavior": (
            "tests.test_shared_scientific_contracts::test_no_production_source_emits_promoted_or_legacy_calculation_state",
        ),
        "regression_coverage": (
            "tests.test_shared_scientific_contracts::test_all_public_producer_state_fields_are_non_init_candidate_literals",
        ),
        "configuration_reachability": (
            "tests.test_shared_scientific_contracts::test_producer_state_source_inventory_is_complete",
            "tests.test_shared_scientific_contracts::test_active_publication_inventory_is_complete_and_uses_v2_only",
        ),
        "reproducibility": (
            "tests.test_shared_scientific_contracts::test_active_publication_inventory_is_complete_and_uses_v2_only",
        ),
    },
    "AUD-10": {
        "execution": (
            "tests.test_output_paths::test_relative_root_uses_declared_anchor_not_cwd",
        ),
        "input_output_behavior": (
            "tests.test_runtime::test_provenance_rejects_output_exclusion_mismatch",
        ),
        "boundary_failure_behavior": (
            "tests.test_output_paths::test_root_policy_matrix_is_complete",
            "tests.test_output_paths::test_cached_ignored_root_is_revalidated_before_effect",
        ),
        "regression_coverage": (
            "tests.test_output_paths::test_ignored_root_with_tracked_descendant_rejects",
        ),
        "configuration_reachability": (
            "tests.test_shared_scientific_contracts::test_every_publication_callable_has_literal_domain_order",
            "tests.test_shared_scientific_contracts::test_invalid_root_precedes_all_producer_effects",
        ),
        "reproducibility": (
            "tests.test_output_paths::test_relative_root_uses_declared_anchor_not_cwd",
        ),
    },
    "AUD-11": {
        "execution": (
            "tests.test_artifact_schema::test_verified_npz_reader_rejects_noncanonical_zip_npy_matrix",
        ),
        "input_output_behavior": (
            "tests.test_artifact_schema::test_prepare_rejects_noncanonical_npz_array[object]",
            "tests.test_artifact_schema::test_prepare_rejects_noncanonical_npz_array[big-endian-float64]",
        ),
        "boundary_failure_behavior": (
            "tests.test_artifact_schema::test_npz_finiteness_policy_is_closed[positive-infinity-rejected]",
            "tests.test_artifact_schema::test_npz_finiteness_policy_is_closed[old-exception-policy-rejected]",
        ),
        "regression_coverage": (
            "tests.test_artifact_schema::test_v2_loader_rejects_closed_tamper_matrix[pickle_npz]",
        ),
        "configuration_reachability": (
            "tests.test_artifact_schema::test_strict_json_reader_rejects_duplicate_and_nonfinite_tokens",
        ),
        "reproducibility": (
            "tests.test_artifact_schema::test_verified_npz_reader_rejects_noncanonical_zip_npy_matrix",
        ),
    },
    "AUD-12": {
        "execution": (
            "tests.test_runtime::test_rng_refactor_matches_independent_seedsequence_oracle[271828]",
        ),
        "input_output_behavior": (
            "tests.test_runtime::test_rng_spawn_provenance_mutation_changes_neither_seed_material_nor_draws",
        ),
        "boundary_failure_behavior": (
            "tests.test_runtime::test_rng_direct_construction_is_not_a_spawn_key_injection_seam",
        ),
        "regression_coverage": (
            "tests.test_runtime::test_rng_spawn_provenance_mutation_changes_neither_seed_material_nor_draws",
        ),
        "configuration_reachability": (
            "tests.test_runtime::test_rng_direct_construction_is_not_a_spawn_key_injection_seam",
        ),
        "reproducibility": (
            "tests.test_runtime::test_rng_refactor_matches_independent_seedsequence_oracle[0]",
            "tests.test_runtime::test_rng_refactor_matches_independent_seedsequence_oracle[1]",
            "tests.test_runtime::test_rng_refactor_matches_independent_seedsequence_oracle[271828]",
            "tests.test_runtime::test_rng_refactor_matches_independent_seedsequence_oracle[9223372036854775807]",
        ),
    },
}
FIXED_REVIEW_CRITERION_SCORES = {
    "closed": {key: 20 for key in CODE_CRITERION_KEYS},
    "cuda-currentness": {
        "execution": 0,
        "input_output_behavior": 0,
        "boundary_failure_behavior": 0,
        "regression_coverage": 0,
        "configuration_reachability": 20,
        "reproducibility": 0,
    },
}
CLAIM_SPECS = (
    {
        "id": "WAVE-B-AUD-01-DEFECT-REPRODUCES", "domain": "code",
        "kind": "mechanical", "severity": "medium",
        "evidence_ids": ("wave-b-aud-01-defect-counterevidence",),
        "statement": "At this artifact revision, a v2 run path can accept unbound or changed bytes, or verify bytes other than those it parses.",
    },
    {
        "id": "WAVE-B-AUD-01-REGRESSION-CONTRACT", "domain": "code",
        "kind": "mechanical", "severity": "medium",
        "evidence_ids": ("wave-b-aud-01-regression-evidence",),
        "statement": "At this artifact revision, v2 run preparation, publication, and loading enforce the closed byte-bound single-read contract.",
    },
    {
        "id": "WAVE-B-AUD-02-DEFECT-REPRODUCES", "domain": "code",
        "kind": "mechanical", "severity": "medium",
        "evidence_ids": ("wave-b-aud-02-defect-counterevidence",),
        "statement": "At this artifact revision, figure readers or publishers can expose a mixed, partial, or unowned generation.",
    },
    {
        "id": "WAVE-B-AUD-02-REGRESSION-CONTRACT", "domain": "code",
        "kind": "mechanical", "severity": "medium",
        "evidence_ids": ("wave-b-aud-02-regression-evidence",),
        "statement": "At this artifact revision, figure generation, journal, pointer, crash recovery, and concurrent access are one closed transaction contract.",
    },
    {
        "id": "WAVE-B-AUD-04-DEFECT-REPRODUCES", "domain": "code",
        "kind": "mechanical", "severity": "medium",
        "evidence_ids": ("wave-b-aud-04-defect-counterevidence",),
        "statement": "At this artifact revision, a metric caller can inject a decision/state or serialize a value outside the closed MetricRecord-v2 truth table.",
    },
    {
        "id": "WAVE-B-AUD-04-REGRESSION-CONTRACT", "domain": "code",
        "kind": "mechanical", "severity": "medium",
        "evidence_ids": ("wave-b-aud-04-regression-evidence",),
        "statement": "At this artifact revision, MetricRecord-v2 normalizes inputs and derives every decision from its closed comparator contract.",
    },
    {
        "id": "WAVE-B-AUD-05-DEFECT-REPRODUCES", "domain": "code",
        "kind": "mechanical", "severity": "low",
        "evidence_ids": ("wave-b-aud-05-defect-counterevidence",),
        "statement": "At this artifact revision, a producer carrier or payload can emit a promoted or legacy calculation verification state.",
    },
    {
        "id": "WAVE-B-AUD-05-REGRESSION-CONTRACT", "domain": "code",
        "kind": "mechanical", "severity": "low",
        "evidence_ids": ("wave-b-aud-05-regression-evidence",),
        "statement": "At this artifact revision, every inventoried producer carrier and payload factory emits only CANDIDATE verification state.",
    },
    {
        "id": "WAVE-B-AUD-10-DEFECT-REPRODUCES", "domain": "code",
        "kind": "mechanical", "severity": "medium",
        "evidence_ids": ("wave-b-aud-10-defect-counterevidence",),
        "statement": "At this artifact revision, a cached, ambiguous, tracked, or reparse output root can reach an effect before renewed admission.",
    },
    {
        "id": "WAVE-B-AUD-10-REGRESSION-CONTRACT", "domain": "code",
        "kind": "mechanical", "severity": "medium",
        "evidence_ids": ("wave-b-aud-10-regression-evidence",),
        "statement": "At this artifact revision, every publication entrypoint revalidates the canonical output root before authorization, identity, RNG, worker, or publication effects.",
    },
    {
        "id": "WAVE-B-AUD-11-DEFECT-REPRODUCES", "domain": "code",
        "kind": "mechanical", "severity": "medium",
        "evidence_ids": ("wave-b-aud-11-defect-counterevidence",),
        "statement": "At this artifact revision, a noncanonical, pickled, nonfinite, or structurally ambiguous NPZ member can enter or leave a v2 run.",
    },
    {
        "id": "WAVE-B-AUD-11-REGRESSION-CONTRACT", "domain": "code",
        "kind": "mechanical", "severity": "medium",
        "evidence_ids": ("wave-b-aud-11-regression-evidence",),
        "statement": "At this artifact revision, v2 NPZ writing and verified-buffer reading enforce one deterministic closed archive and array policy.",
    },
    {
        "id": "WAVE-B-AUD-12-DEFECT-REPRODUCES", "domain": "code",
        "kind": "mechanical", "severity": "low",
        "evidence_ids": ("wave-b-aud-12-defect-counterevidence",),
        "statement": "At this artifact revision, caller mutation can alter RNG seed material, provenance, or subsequent draws after construction.",
    },
    {
        "id": "WAVE-B-AUD-12-REGRESSION-CONTRACT", "domain": "code",
        "kind": "mechanical", "severity": "low",
        "evidence_ids": ("wave-b-aud-12-regression-evidence",),
        "statement": "At this artifact revision, RNG provenance is detached, immutable, and reproducible against an independent SeedSequence oracle.",
    },
    {
        "id": "WAVE-B-CUDA-CURRENTNESS", "domain": "code",
        "kind": "mechanical", "severity": "low",
        "evidence_ids": ("wave-b-cpu-environment", "wave-b-cuda-skip-record"),
        "statement": "At this artifact revision, dedicated CUDA path execution and command-harness reproducibility have current eligible evidence.",
    },
)
EVIDENCE_BINDING_KEYS = {"path", "supports"}
LEDGER_CLAIM_KEYS = {
    "id", "domain", "statement", "severity", "state", "artifact_revision",
    "criteria", "escalation_triggers", "escalation_target", "views",
    "evidence", "counterevidence", "verifiers", "open_obligations",
    "evidence_invalidated",
}
LEDGER_CRITERION_KEYS = {"name", "score"}
LEDGER_VIEWS_KEYS = {
    "calibration_kind", "unresolved_disagreement", "comparison", "scores",
}
LEDGER_VIEW_SCORE_KEYS = {"view_id", "criteria"}
LEDGER_COMPARISON_KEYS = {
    "method", "candidate_count", "candidate_ids", "candidate_descriptions",
    "pivot_ids", "orders", "matches",
}
LEDGER_CANDIDATE_DESCRIPTION_KEYS = {"id", "description"}
LEDGER_MATCH_KEYS = {
    "left", "right", "view_id", "outcome", "criteria", "result_location",
}
LEDGER_VERIFIER_KEYS = {
    "role", "view_ids", "result", "evidence_ids", "result_location",
}
LEDGER_EVIDENCE_KEYS = {"id", "kind", "location", "artifact_revision"}
LEDGER_COUNTEREVIDENCE_KEYS = {
    "id", "kind", "location", "artifact_revision", "supports",
}
EVIDENCE_LOCATIONS_BY_ID = {
    "wave-b-aud-01-defect-counterevidence": {
        "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
        "supports": False,
    },
    "wave-b-aud-01-regression-evidence": {
        "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
        "supports": True,
    },
    "wave-b-aud-02-defect-counterevidence": {
        "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
        "supports": False,
    },
    "wave-b-aud-02-regression-evidence": {
        "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
        "supports": True,
    },
    "wave-b-aud-04-defect-counterevidence": {
        "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
        "supports": False,
    },
    "wave-b-aud-04-regression-evidence": {
        "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
        "supports": True,
    },
    "wave-b-aud-05-defect-counterevidence": {
        "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
        "supports": False,
    },
    "wave-b-aud-05-regression-evidence": {
        "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
        "supports": True,
    },
    "wave-b-aud-10-defect-counterevidence": {
        "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
        "supports": False,
    },
    "wave-b-aud-10-regression-evidence": {
        "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
        "supports": True,
    },
    "wave-b-aud-11-defect-counterevidence": {
        "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
        "supports": False,
    },
    "wave-b-aud-11-regression-evidence": {
        "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
        "supports": True,
    },
    "wave-b-aud-12-defect-counterevidence": {
        "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
        "supports": False,
    },
    "wave-b-aud-12-regression-evidence": {
        "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
        "supports": True,
    },
    "wave-b-cpu-environment": {
        "path": "verification-evidence/wave-b/{evidence_short}/environment.json",
        "supports": False,
    },
    "wave-b-cuda-skip-record": {
        "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
        "supports": False,
    },
}
ADJUDICATOR_PATHS = (
    "reviews/adjudicators/WAVE-B-AUD-01-DEFECT-REPRODUCES.json",
    "reviews/adjudicators/WAVE-B-AUD-01-REGRESSION-CONTRACT.json",
    "reviews/adjudicators/WAVE-B-AUD-02-DEFECT-REPRODUCES.json",
    "reviews/adjudicators/WAVE-B-AUD-02-REGRESSION-CONTRACT.json",
    "reviews/adjudicators/WAVE-B-AUD-04-DEFECT-REPRODUCES.json",
    "reviews/adjudicators/WAVE-B-AUD-04-REGRESSION-CONTRACT.json",
    "reviews/adjudicators/WAVE-B-AUD-05-DEFECT-REPRODUCES.json",
    "reviews/adjudicators/WAVE-B-AUD-05-REGRESSION-CONTRACT.json",
    "reviews/adjudicators/WAVE-B-AUD-10-DEFECT-REPRODUCES.json",
    "reviews/adjudicators/WAVE-B-AUD-10-REGRESSION-CONTRACT.json",
    "reviews/adjudicators/WAVE-B-AUD-11-DEFECT-REPRODUCES.json",
    "reviews/adjudicators/WAVE-B-AUD-11-REGRESSION-CONTRACT.json",
    "reviews/adjudicators/WAVE-B-AUD-12-DEFECT-REPRODUCES.json",
    "reviews/adjudicators/WAVE-B-AUD-12-REGRESSION-CONTRACT.json",
    "reviews/adjudicators/WAVE-B-CUDA-CURRENTNESS.json",
)
CLOSURE_PUBLIC_PATHS = (
    GENERIC_PUBLIC_PATHS + (DOMAIN_INDEX_PATH,) + REVIEW_PATHS + ADJUDICATOR_PATHS
)
```

Each of the 14 AUD claim records in both raw reviews contains exactly
`CODE_CRITERION_KEYS`, in order, with the literal score 20 for every key. The
CUDA-currentness record also contains all six keys, with the exact
`0,0,0,0,20,0` mapping in `FIXED_REVIEW_CRITERION_SCORES`. Reviewers write
these scores and the literal claim-specific `CLAIM_SPECS` evidence IDs; neither `build` nor
`populate-ledger` may generate, rename, fill, average away, or otherwise
synthesize a criterion, view, evidence ID, verdict, or obligation. Generic
`coverage`/`freshness`, Wave 0's superseded display labels, and a missing or
extra criterion are hard failures. The union of all claim-spec evidence IDs
must equal the key set of `EVIDENCE_LOCATIONS_BY_ID`. Every value has exactly
`EVIDENCE_BINDING_KEYS`; seven defect entries point to current `full.xml`
mechanical counterevidence with `supports=False`, seven regression entries
point to current `full.xml` mechanical evidence with `supports=True`, and the
CUDA entries bind exactly `environment.json` and the CUDA skip in `full.xml`
with `supports=False`.

`schema_version` is `wave-b-domain-evidence-v1`, `wave` is `wave-b`, and
`root_index` is the exact path/size/SHA of the sibling `index.json`.
`required_controls` is the literal `REQUIRED_CONTROLS` mapping above; every
listed testcase ID must occur as a passing testcase in the parsed
targeted/subsystem/full XML union. `claim_specs` equals the literal 15-entry
`CLAIM_SPECS` tuple. Candidate `review_policy` is `not-required-candidate` with
`reviews=[]` and `adjudicators=[]`. Closure policy is exactly
`two-independent-pairwise-reviews-plus-verifier-adjudicators`; `reviews` contains
the two strict public file bindings in `REVIEW_PATHS` order and
`adjudicators` contains the 15 strict public file bindings in
`ADJUDICATOR_PATHS`/`CLAIM_SPECS` order.

After the closure JUnits exist and before a review is dispatched,
`review-context-sha` validates exact `E/P`, the candidate selected-input digest,
the three raw command/JUnit pairs, the plan/snapshot/source bindings, and the
current six-key CPU environment. It writes canonical ignored
`raw-dir/review-context.json` and prints only its lowercase SHA-256. Both raw
reviews bind that digest in `reviewed_input_inventory_sha256`, list the exact
sorted reviewed paths, and contain all 15 claim records in `CLAIM_SPECS` order.
The `code-runtime` view performs `AB`; `artifact-concurrency` independently
performs `BA`. Each record has exactly `RAW_CLAIM_SCORE_KEYS`, candidate IDs
`claim-statement`/`explicit-negation` with the same exact two
`{id,description}` objects in both views,
`comparison_criteria` equal to its six-key `criteria`, and the intended public
`result_location`. Both outer reviews and every claim score have
`escalation_triggers=[]` and `unresolved_disagreement=False`. Defect
propositions select the explicit negation and record reviewer verdict
`refute`; regression contracts select the claim statement and record
`support`; CUDA records `abstain` with a nonempty current-execution and
reproducibility obligation. CUDA abstention is an evidence gap, not reviewer
disagreement. Comparison outcomes are literal: defect AB/BA are `right`/`left`,
regression AB/BA are `left`/`right`, and CUDA is `inconclusive` in both orders.

The reviewers, not the wrapper, also write exactly one raw strict
`RAW_ADJUDICATOR_KEYS` object per `CLAIM_SPECS` entry under
`raw-dir/reviews/adjudicators/{claim_id}.json`. It binds the same exact `E/P`
and review-context digest, has `role="verifier-adjudicator"`,
`escalation_triggers=[]`, `escalation_target=2`, `view_ids` exactly `VIEW_IDS`,
`evidence_ids` byte-for-byte equal to the claim spec, and the intended public
adjudicator path. Its `result` is exactly one of `ADJUDICATOR_RESULTS`: `refute`
for the seven defect propositions, `support` for the seven regression
contracts, and `abstain` for CUDA. Ledger states are forbidden in `result`.
`ADJUDICATOR_RESULT_TO_LEDGER_STATE` is the only mapping to
`REFUTED`/`EVIDENCE_VERIFIED`/`INCONCLUSIVE`.

`validate-reviews` reads the two raw reviews and 15 raw adjudicators exactly
once, rejects duplicate/nonfinite JSON and every missing/extra/renamed field,
recomputes the review context, enforces the AB/BA and score contracts above,
and exits successfully before `build --stage closure` may run. The frozen
29-file branch accepts only escalation target 2, empty trigger arrays, and zero
reviewer disagreement. Any trigger, disagreement, missing comparison, or
non-CUDA reviewer obligation stops before publication; this plan defines no
4/8-view Wave B branch. A missing or
extra raw review/adjudicator, duplicate view/claim identity, absolute,
backslash, traversal, or mismatched result location, invalid lowercase digest,
or changed raw byte fails while the public closure parent remains absent.

Only after successful `validate-reviews`, closure preparation applies Wave 0's
ordered privacy transform to all 17 raw records, re-parses each scrubbed byte
sequence to prove semantic equality, and publishes the same 17 records at
`REVIEW_PATHS + ADJUDICATOR_PATHS`. The generic
`privacy-transform.json`—not a synthesized review envelope or domain-index
copy—contains every raw-to-public path/size/SHA and scrubbed-hash binding.
`populate-ledger` consumes the validated public review and adjudicator objects
byte-for-byte. It may translate the frozen records into the gate schema but may
not invent or change any claim statement, criterion, score, comparison,
verdict/result, evidence ID, evidence polarity, result location, escalation
field, or obligation. Translation maps only the exact public adjudicator result
through `ADJUDICATOR_RESULT_TO_LEDGER_STATE`.

The generic root bundle remains exactly `GENERIC_PUBLIC_PATHS`; the domain
index is the twelfth candidate file and binds the root one-way. Closure is
exactly `CLOSURE_PUBLIC_PATHS` (29 recursive relative paths): the 11 generic
files, domain index, two public reviews, and 15 public adjudicators. Validation
enumerates regular files recursively, normalizes each relative path to POSIX,
and requires exact set equality. The root index never refers to the domain
index, review paths, or adjudicator paths; the domain schema remains eligible
in the generic source/config inventory.

- [ ] **Step 1: Write literal RED tests for the parser, atomic bundle, domain
  schema, skip maps, and ledger population**

```python
def _prepared_bytes_by_path(
    files: tuple[PreparedEvidenceFile, ...],
) -> Mapping[str, bytes]:
    assert type(files) is tuple
    pairs = tuple((item.path.as_posix(), item.data) for item in files)
    assert all(type(data) is bytes for _, data in pairs)
    assert len(pairs) == len({path for path, _ in pairs})
    return MappingProxyType(dict(pairs))


@dataclass(frozen=True, slots=True)
class PreparedClosureHarness:
    bundle: PreparedEvidenceBundle
    raw_review_files: tuple[PreparedEvidenceFile, ...]
    raw_adjudicator_files: tuple[PreparedEvidenceFile, ...]

    def public_files_by_path(self) -> Mapping[str, bytes]:
        return _prepared_bytes_by_path(self.bundle.files)

    def raw_reviews_by_role(self) -> Mapping[str, bytes]:
        assert len(self.raw_review_files) == len(VIEW_IDS)
        paths = tuple(item.path.as_posix() for item in self.raw_review_files)
        assert paths == REVIEW_PATHS
        by_path = _prepared_bytes_by_path(self.raw_review_files)
        return MappingProxyType({
            view_id: by_path[path]
            for view_id, path in zip(VIEW_IDS, paths, strict=True)
        })

    def raw_adjudicators_by_claim(self) -> Mapping[str, bytes]:
        assert len(self.raw_adjudicator_files) == len(CLAIM_SPECS)
        paths = tuple(item.path.as_posix() for item in self.raw_adjudicator_files)
        assert paths == ADJUDICATOR_PATHS
        by_path = _prepared_bytes_by_path(self.raw_adjudicator_files)
        return MappingProxyType({
            spec["id"]: by_path[path]
            for spec, path in zip(CLAIM_SPECS, paths, strict=True)
        })


def _string_leaves(value: object) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Mapping):
        return tuple(
            leaf for item in value.values() for leaf in _string_leaves(item)
        )
    if isinstance(value, (list, tuple)):
        return tuple(leaf for item in value for leaf in _string_leaves(item))
    return ()


def _closed_objects_with_keys(
    value: object, keys: frozenset[str]
) -> tuple[Mapping[str, object], ...]:
    if isinstance(value, Mapping) and frozenset(value) == keys:
        return (value,)
    if isinstance(value, Mapping):
        return tuple(
            item
            for child in value.values()
            for item in _closed_objects_with_keys(child, keys)
        )
    if isinstance(value, (list, tuple)):
        return tuple(
            item
            for child in value
            for item in _closed_objects_with_keys(child, keys)
        )
    return ()


def test_wrapper_exposes_only_frozen_commands():
    assert parser().parse_args([
        "build", "--stage", "candidate", "--tested-head", "a" * 40,
        "--implementation-parent", "a" * 40, "--raw-dir", ".verification/raw",
        "--output-dir", "docs/verification/evidence/wave-b/aaaaaaaaaaaa",
    ]).command == "build"
    assert parser().parse_args([
        "review-context-sha", "--tested-head", "b" * 40,
        "--implementation-parent", "a" * 40,
        "--raw-dir", ".verification/raw",
    ]).command == "review-context-sha"
    assert parser().parse_args([
        "validate-reviews", "--tested-head", "b" * 40,
        "--implementation-parent", "a" * 40,
        "--raw-dir", ".verification/raw",
    ]).command == "validate-reviews"
    assert parser().parse_args([
        "populate-ledger", "--ledger", ".verification/wave-b/final-ledger.json",
        "--closure-index", "verification-evidence/wave-b/bbbbbbbbbbbb/index.json",
    ]).command == "populate-ledger"


def test_domain_inventory_is_one_way(valid_domain, public_files):
    assert set(valid_domain) == DOMAIN_INDEX_KEYS
    assert set(valid_domain["root_index"]) == FILE_BINDING_KEYS
    root = strict_json_from_bytes(public_files["index.json"])
    assert DOMAIN_INDEX_PATH not in set(_string_leaves(root))
    assert any(
        binding["path"]
        == "docs/verification/remediation/wave-b-domain-evidence-v1.schema.json"
        for binding in root["source_config_bindings"]
    )
    validate_wave_b_domain_index(valid_domain, public_files=public_files)


def test_public_path_sets_are_recursive_and_exact():
    from tools.build_wave0_evidence import (
        GENERIC_PUBLIC_PATHS as WAVE0_GENERIC_PUBLIC_PATHS,
    )

    assert GENERIC_PUBLIC_PATHS == WAVE0_GENERIC_PUBLIC_PATHS
    assert len(GENERIC_PUBLIC_PATHS) == 11
    assert len(CANDIDATE_PUBLIC_PATHS) == 12
    assert len(CLOSURE_PUBLIC_PATHS) == 29
    assert len(set(CLOSURE_PUBLIC_PATHS)) == 29
    assert CANDIDATE_PUBLIC_PATHS == GENERIC_PUBLIC_PATHS + (DOMAIN_INDEX_PATH,)
    assert CLOSURE_PUBLIC_PATHS == (
        GENERIC_PUBLIC_PATHS + (DOMAIN_INDEX_PATH,) + REVIEW_PATHS
        + ADJUDICATOR_PATHS
    )
    assert WAVE_B_REVIEWED_PLAN_PATH in WAVE_B_REQUIRED_SOURCE_CONFIG_PATHS
    assert WAVE_B_DEPENDENCY_INPUTS == (
        "pyproject.toml",
        "environments/cuda-rtx5090-cu128.lock.txt",
        "docs/verification/remediation/verification-contract-v1.json",
    )


def test_wave_b_code_criteria_equal_authoritative_wave_zero_keys():
    from tools.build_wave0_evidence import CLAIM_CRITERIA_BY_DOMAIN

    wave_zero_keys = tuple(
        key for key, _label in CLAIM_CRITERIA_BY_DOMAIN["code"]
    )
    assert CODE_CRITERION_KEYS == wave_zero_keys == (
        "execution",
        "input_output_behavior",
        "boundary_failure_behavior",
        "regression_coverage",
        "configuration_reachability",
        "reproducibility",
    )
    assert all(
        tuple(criterion_map) == wave_zero_keys
        for criterion_map in CLAIM_CRITERION_CONTROLS.values()
    )
    assert tuple(FIXED_REVIEW_CRITERION_SCORES["cuda-currentness"]) \
        == wave_zero_keys


def test_evidence_locations_are_total_exact_and_polarized():
    claim_evidence_ids = tuple(
        evidence_id
        for spec in CLAIM_SPECS
        for evidence_id in spec["evidence_ids"]
    )
    assert len(CLAIM_SPECS) == 15
    assert len(claim_evidence_ids) == 16
    assert len(set(claim_evidence_ids)) == 16
    assert set(claim_evidence_ids) == set(EVIDENCE_LOCATIONS_BY_ID)
    assert all(
        set(binding) == EVIDENCE_BINDING_KEYS
        for binding in EVIDENCE_LOCATIONS_BY_ID.values()
    )
    for spec in CLAIM_SPECS:
        bindings = tuple(
            EVIDENCE_LOCATIONS_BY_ID[evidence_id]
            for evidence_id in spec["evidence_ids"]
        )
        if "-DEFECT-" in spec["id"]:
            assert len(bindings) == 1
            assert bindings[0] == {
                "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
                "supports": False,
            }
        elif "-REGRESSION-" in spec["id"]:
            assert len(bindings) == 1
            assert bindings[0] == {
                "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
                "supports": True,
            }
    assert tuple(
        EVIDENCE_LOCATIONS_BY_ID[evidence_id]
        for evidence_id in CLAIM_SPECS[-1]["evidence_ids"]
    ) == (
        {
            "path": "verification-evidence/wave-b/{evidence_short}/environment.json",
            "supports": False,
        },
        {
            "path": "verification-evidence/wave-b/{evidence_short}/full.xml",
            "supports": False,
        },
    )


def test_adjudicator_result_mapping_is_byte_exact():
    assert ADJUDICATOR_RESULTS == ("support", "refute", "abstain")
    assert canonical_json_bytes(ADJUDICATOR_RESULT_TO_LEDGER_STATE) == (
        b'{"abstain":"INCONCLUSIVE","refute":"REFUTED",'
        b'"support":"EVIDENCE_VERIFIED"}'
    )


@pytest.mark.parametrize("missing", (
    "reviews/artifact-concurrency.json",
    "reviews/adjudicators/WAVE-B-AUD-12-REGRESSION-CONTRACT.json",
))
def test_closure_requires_validated_reviews_before_publication(
    valid_raw, missing, tmp_path
):
    del valid_raw["raw_records"][missing]
    output = tmp_path / "verification-evidence/wave-b/bbbbbbbbbbbb"
    with pytest.raises(ValueError, match="review set is not exact"):
        prepare_wave_b_evidence_bundle(**valid_raw, output_dir=output)
    assert not output.exists()
    assert not output.parent.exists()


@pytest.mark.parametrize("mutation", (
    "outer-trigger", "outer-disagreement", "claim-disagreement", "target-four",
))
def test_frozen_29_file_branch_rejects_escalation_before_publication(
    valid_raw, mutation, tmp_path
):
    path = "reviews/code-runtime.json"
    if mutation == "target-four":
        path = "reviews/adjudicators/WAVE-B-AUD-01-DEFECT-REPRODUCES.json"
    record = strict_json_from_bytes(valid_raw["raw_records"][path])
    if mutation == "outer-trigger":
        record["escalation_triggers"] = ["boundary_failure_disagreement"]
    elif mutation == "outer-disagreement":
        record["unresolved_disagreement"] = True
    elif mutation == "claim-disagreement":
        record["claim_scores"][0]["unresolved_disagreement"] = True
    else:
        record["escalation_target"] = 4
    valid_raw["raw_records"][path] = canonical_json_bytes(record)
    output = tmp_path / "verification-evidence/wave-b/bbbbbbbbbbbb"
    with pytest.raises(ValueError, match="frozen review target 2"):
        prepare_wave_b_evidence_bundle(**valid_raw, output_dir=output)
    assert not output.exists()
    assert not output.parent.exists()


def test_all_17_reviews_close_the_generic_privacy_hash_chain(prepared_closure):
    public_files = prepared_closure.public_files_by_path()
    raw_reviews = prepared_closure.raw_reviews_by_role()
    raw_adjudicators = prepared_closure.raw_adjudicators_by_claim()
    raw_by_public_path = {
        **{
            path: raw_reviews[view_id]
            for view_id, path in zip(VIEW_IDS, REVIEW_PATHS, strict=True)
        },
        **{
            path: raw_adjudicators[spec["id"]]
            for spec, path in zip(CLAIM_SPECS, ADJUDICATOR_PATHS, strict=True)
        },
    }
    privacy = strict_json_from_bytes(public_files["privacy-transform.json"])
    mapping_keys = frozenset({
        "raw_relative_path", "raw_sha256", "public_path",
        "public_sha256", "transforms",
    })
    mappings = {
        item["public_path"]: item
        for item in _closed_objects_with_keys(privacy, mapping_keys)
    }
    assert set(raw_by_public_path) == set(REVIEW_PATHS + ADJUDICATOR_PATHS)
    for public_path, raw in raw_by_public_path.items():
        mapping = mappings[public_path]
        assert frozenset(mapping) == mapping_keys
        assert mapping["raw_sha256"] == sha256(raw).hexdigest()
        assert mapping["public_sha256"] == sha256(
            public_files[public_path]
        ).hexdigest()
    domain = strict_json_from_bytes(
        public_files[DOMAIN_INDEX_PATH]
    )
    assert tuple(item["path"] for item in domain["reviews"]) == REVIEW_PATHS
    assert tuple(item["path"] for item in domain["adjudicators"]) == ADJUDICATOR_PATHS
    validate_wave_b_domain_index(
        domain,
        public_files=public_files,
    )


def test_populated_ledger_is_exact_projection_of_public_records(
    populated_ledger, prepared_closure
):
    public = prepared_closure.public_files_by_path()
    reviews = {
        view_id: strict_json_from_bytes(public[path])
        for view_id, path in zip(VIEW_IDS, REVIEW_PATHS, strict=True)
    }
    adjudicators = {
        spec["id"]: strict_json_from_bytes(public[path])
        for spec, path in zip(CLAIM_SPECS, ADJUDICATOR_PATHS, strict=True)
    }
    closure_index = strict_json_from_bytes(public["index.json"])
    evidence_short = closure_index["tested_git_head"][:12]
    claims = {claim["id"]: claim for claim in populated_ledger["claims"]}
    assert tuple(claims) == tuple(spec["id"] for spec in CLAIM_SPECS)
    for spec in CLAIM_SPECS:
        claim = claims[spec["id"]]
        assert set(claim) == LEDGER_CLAIM_KEYS
        assert claim["statement"] == spec["statement"]
        assert claim["domain"] == spec["domain"]
        assert claim["severity"] == spec["severity"]
        assert claim["escalation_triggers"] == []
        assert claim["escalation_target"] == FROZEN_REVIEW_ESCALATION_TARGET
        assert set(claim["views"]) == LEDGER_VIEWS_KEYS
        assert claim["views"]["calibration_kind"] == CALIBRATION_KIND
        assert claim["views"]["unresolved_disagreement"] is False
        public_scores = {
            view_id: next(
                item for item in reviews[view_id]["claim_scores"]
                if item["claim_id"] == spec["id"]
            )
            for view_id in VIEW_IDS
        }
        expected_claim_criteria = [
            {
                "name": name,
                "score": sum(
                    public_scores[view_id]["criteria"][name]
                    for view_id in VIEW_IDS
                ) / len(VIEW_IDS),
            }
            for name in CODE_CRITERION_KEYS
        ]
        assert claim["criteria"] == expected_claim_criteria
        assert all(
            set(criterion) == LEDGER_CRITERION_KEYS
            for criterion in claim["criteria"]
        )
        comparison = claim["views"]["comparison"]
        assert set(comparison) == LEDGER_COMPARISON_KEYS
        assert comparison["method"] == "pairwise"
        assert comparison["candidate_count"] == 2
        assert comparison["candidate_ids"] == list(CANDIDATE_IDS)
        expected_descriptions = public_scores[VIEW_IDS[0]][
            "candidate_descriptions"
        ]
        assert all(
            public_scores[view_id]["candidate_descriptions"]
            == expected_descriptions
            for view_id in VIEW_IDS
        )
        assert comparison["candidate_descriptions"] == expected_descriptions
        assert all(
            set(item) == LEDGER_CANDIDATE_DESCRIPTION_KEYS
            for item in comparison["candidate_descriptions"]
        )
        assert tuple(
            item["id"] for item in comparison["candidate_descriptions"]
        ) == CANDIDATE_IDS
        assert comparison["pivot_ids"] == []
        assert comparison["orders"] == ["AB", "BA"]
        assert len(comparison["matches"]) == 2
        order_pairs = {
            "AB": CANDIDATE_IDS,
            "BA": tuple(reversed(CANDIDATE_IDS)),
        }
        if "-DEFECT-" in spec["id"]:
            expected_outcomes = {"AB": "right", "BA": "left"}
        elif "-REGRESSION-" in spec["id"]:
            expected_outcomes = {"AB": "left", "BA": "right"}
        else:
            expected_outcomes = {"AB": "inconclusive", "BA": "inconclusive"}
        for view_id, order, match in zip(
            VIEW_IDS, ("AB", "BA"), comparison["matches"], strict=True
        ):
            public_score = public_scores[view_id]
            assert set(match) == LEDGER_MATCH_KEYS
            assert public_score["comparison_order"] == order
            assert public_score["comparison_outcome"] == expected_outcomes[order]
            assert (match["left"], match["right"]) == order_pairs[order]
            assert match["view_id"] == view_id
            assert match["outcome"] == public_score["comparison_outcome"]
            assert match["criteria"] == [
                {"name": name, "score": score}
                for name, score in public_score["comparison_criteria"].items()
            ]
            assert all(
                set(criterion) == LEDGER_CRITERION_KEYS
                for criterion in match["criteria"]
            )
            assert match["result_location"] \
                == reviews[view_id]["result_location"]
        for view_id, ledger_view in zip(
            VIEW_IDS, claim["views"]["scores"], strict=True
        ):
            assert set(ledger_view) == LEDGER_VIEW_SCORE_KEYS
            assert ledger_view["view_id"] == view_id
            assert all(
                set(criterion) == LEDGER_CRITERION_KEYS
                for criterion in ledger_view["criteria"]
            )
            assert reviews[view_id]["escalation_triggers"] == []
            assert reviews[view_id]["unresolved_disagreement"] is False
            public_score = public_scores[view_id]
            assert tuple(score["name"] for score in ledger_view["criteria"]) \
                == tuple(public_score["criteria"])
            assert tuple(score["score"] for score in ledger_view["criteria"]) \
                == tuple(public_score["criteria"].values())
            assert public_score["escalation_triggers"] == []
            assert public_score["unresolved_disagreement"] is False
        public_adjudicator = adjudicators[spec["id"]]
        assert public_adjudicator["role"] == "verifier-adjudicator"
        assert public_adjudicator["escalation_triggers"] == []
        assert public_adjudicator["escalation_target"] == 2
        assert public_adjudicator["result"] in ADJUDICATOR_RESULTS
        assert claim["state"] == ADJUDICATOR_RESULT_TO_LEDGER_STATE[
            public_adjudicator["result"]
        ]
        assert claim["open_obligations"] \
            == public_adjudicator["open_obligations"]
        assert claim["escalation_triggers"] \
            == public_adjudicator["escalation_triggers"]
        assert claim["escalation_target"] \
            == public_adjudicator["escalation_target"]
        verifier = next(
            item for item in claim["verifiers"]
            if item["role"] == "verifier-adjudicator"
        )
        assert set(verifier) == LEDGER_VERIFIER_KEYS
        assert verifier["view_ids"] == public_adjudicator["view_ids"]
        assert verifier["result"] == public_adjudicator["result"]
        assert verifier["evidence_ids"] == public_adjudicator["evidence_ids"]
        assert verifier["result_location"] \
            == public_adjudicator["result_location"]
        evidence = {item["id"]: item for item in claim["evidence"]}
        counterevidence = {
            item["id"]: item for item in claim["counterevidence"]
        }
        expected_evidence = {
            evidence_id for evidence_id in spec["evidence_ids"]
            if EVIDENCE_LOCATIONS_BY_ID[evidence_id]["supports"] is True
        }
        expected_counterevidence = {
            evidence_id for evidence_id in spec["evidence_ids"]
            if EVIDENCE_LOCATIONS_BY_ID[evidence_id]["supports"] is False
        }
        assert set(evidence) == expected_evidence
        assert set(counterevidence) == expected_counterevidence
        for evidence_id in spec["evidence_ids"]:
            binding = EVIDENCE_LOCATIONS_BY_ID[evidence_id]
            if binding["supports"] is True:
                record = evidence[evidence_id]
                assert set(record) == LEDGER_EVIDENCE_KEYS
                assert "supports" not in record
            else:
                record = counterevidence[evidence_id]
                assert set(record) == LEDGER_COUNTEREVIDENCE_KEYS
                assert record["supports"] is False
            assert record["kind"] == spec["kind"]
            assert record["artifact_revision"] == claim["artifact_revision"]
            assert record["location"] == binding["path"].format(
                evidence_short=evidence_short
            )


LEDGER_NESTED_MUTATIONS = (
    ("criteria", []),
    ("criteria.0.name", ""),
    ("criteria.0.score", 21),
    ("views.calibration_kind", "mutated"),
    ("views.unresolved_disagreement", True),
    ("views.comparison.method", "pivot_tournament"),
    ("views.comparison.candidate_count", 3),
    ("views.comparison.candidate_ids", ["x", "y"]),
    ("views.comparison.candidate_descriptions", []),
    ("views.comparison.candidate_descriptions.0.id", "x"),
    ("views.comparison.candidate_descriptions.0.description", ""),
    ("views.comparison.pivot_ids", ["claim-statement"]),
    ("views.comparison.orders", ["BA", "AB"]),
    ("views.comparison.matches", []),
    ("views.comparison.matches.0.left", "x"),
    ("views.comparison.matches.0.right", "x"),
    ("views.comparison.matches.0.view_id", "x"),
    ("views.comparison.matches.0.outcome", "tie"),
    ("views.comparison.matches.0.criteria", []),
    ("views.comparison.matches.0.criteria.0.name", ""),
    ("views.comparison.matches.0.criteria.0.score", 21),
    ("views.comparison.matches.0.result_location", "mutated.json"),
    ("views.scores", []),
    ("views.scores.0.view_id", "x"),
    ("views.scores.0.criteria", []),
    ("views.scores.0.criteria.0.name", ""),
    ("views.scores.0.criteria.0.score", 19),
)


def _replace_dotted(value: object, dotted: str, replacement: object) -> None:
    parts = dotted.split(".")
    cursor = value
    for part in parts[:-1]:
        cursor = cursor[int(part)] if isinstance(cursor, list) else cursor[part]
    final = parts[-1]
    if isinstance(cursor, list):
        cursor[int(final)] = replacement
    else:
        cursor[final] = replacement


@pytest.mark.parametrize(("dotted", "replacement"), LEDGER_NESTED_MUTATIONS)
def test_every_nested_projection_field_is_validated_before_ledger_replacement(
    valid_projected_ledger, validated_closure_index, gate_template_path,
    dotted, replacement,
):
    before = gate_template_path.read_bytes()
    mutated = copy.deepcopy(valid_projected_ledger)
    _replace_dotted(mutated["claims"][0], dotted, replacement)
    with pytest.raises(ValueError, match="closed ledger projection"):
        _validate_and_replace_ledger(
            ledger_path=gate_template_path,
            projected_ledger=mutated,
            closure_index=validated_closure_index,
        )
    assert gate_template_path.read_bytes() == before
```

Also create a real temporary `P -> E` repository. Candidate build must accept
only `P/P`; closure only `E/P`; swapped heads, non-direct ancestry, a `P..E`
path outside `docs/verification/evidence/wave-b/{P[:12]}/`, a missing/extra
review or adjudicator, changed review/adjudicator byte, invalid AB/BA order,
criterion-score drift, any nonempty escalation trigger, escalation target other
than 2, any reviewer disagreement, untracked tested input, unknown domain field,
unexplained skip, or nonzero command must fail before output-parent creation.
Start the installed verification gate in that fixture: direct validation of the
empty template must fail, `populate-ledger` must create exactly 15 terminal
claims, and installed validation must then return zero errors.

- [ ] **Step 2: Implement the literal wrapper and run RED/GREEN**

The `build` branch calls generic preparation with `wave="wave-b"`, the exact
suite definitions, policy schema
`wave-b-source-config-theory-tools-tests-v1`, the literal selection/exclusion
and source/config constants above, and `WAVE_B_DEPENDENCY_INPUTS`. It
constructs candidate domain bytes without reviews. For closure it first
requires the successful context-bound `validate-reviews` result, reads and
privacy-scrubs all 17 already-authored review/adjudicator records without
synthesizing fields, validates the combined exact recursive file set, publishes
atomically, then validates both indexes from disk. The `review-context-sha`
and `validate-reviews` branches perform only the frozen pre-index operations
above and never create either public output directory. The
`populate-ledger` branch derives `wave-b-domain-index.json` as the closure
index's sibling, validates both against live `HEAD`, requires the untouched
gate template, projects the validated public records byte-for-byte, and
atomically replaces only that ledger. Define internal
`_validate_and_replace_ledger(*, ledger_path, projected_ledger,
closure_index)` literally: it validates the installed closed schema plus every
deterministic nested projection invariant before opening a replacement temp or
changing `ledger_path`. It has no mutation hook; the test passes a mutated pure
projection directly to this validator and proves the original gate template
bytes remain unchanged.

```powershell
$ErrorActionPreference = 'Stop'
C:\Python314\python.exe -B -m pytest tests\test_wave_b_evidence.py -q -p no:cacheprovider --basetemp=.pytest-wave-b-task10-red
if ($LASTEXITCODE -eq 0) { throw 'Wave B evidence RED unexpectedly passed' }
```

Implement the schema, parser, preparation, publication, validation, and ledger
population paths described above. Then run GREEN and commit:

```powershell
C:\Python314\python.exe -B -m pytest tests\test_wave_b_evidence.py -q -p no:cacheprovider --basetemp=.pytest-wave-b-task10-green
if ($LASTEXITCODE -ne 0) { throw 'Wave B evidence wrapper tests failed' }
git add -- tools/build_wave_b_evidence.py tests/test_wave_b_evidence.py docs/verification/remediation/wave-b-domain-evidence-v1.schema.json
git commit -m "test: define wave B evidence inventory"
```

- [ ] **Step 3: Run final pre-evidence CPU and static checks and freeze `P`**

```powershell
$ErrorActionPreference = 'Stop'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'
$targetedTests = @(
  'tests/test_remediation_contracts.py','tests/test_remediation_evidence.py',
  'tests/test_artifact_schema.py','tests/test_artifacts.py','tests/test_output_paths.py',
  'tests/test_experiment_support.py','tests/test_runtime.py','tests/test_figure_store.py',
  'tests/test_figures.py','tests/test_launchers.py','tests/test_finite_experiment.py',
  'tests/test_agent_network_experiment.py','tests/test_attention_experiment.py',
  'tests/test_categorical_dqm_experiment.py','tests/test_counterexample_experiment.py',
  'tests/test_information_history_experiment.py','tests/test_scale_cocycle_experiment.py',
  'tests/test_theory_oracle_experiment.py','tests/test_holonomy_experiment.py',
  'tests/test_gaussian_realization.py','tests/test_gaussian_fixed_ray_diagnostic_experiment.py',
  'tests/test_gaussian_fixed_ray_experiment.py','tests/test_gaussian_confirmatory_experiment.py',
  'tests/test_gaussian_results_document.py','tests/test_wave_b_evidence.py'
)
$subsystemTests = $targetedTests + @(
  'tests/test_config.py','tests/test_agent_network.py','tests/test_counterexamples.py',
  'tests/test_theory_oracles.py','tests/test_gaussian_fixed_ray_diagnostics.py',
  'tests/test_shared_scientific_contracts.py','tests/test_cuda_backend.py'
)
C:\Python314\python.exe -B -m pytest $targetedTests -q -p no:cacheprovider --basetemp=.pytest-wave-b-final-targeted
if ($LASTEXITCODE -ne 0) { throw 'Wave B pre-evidence targeted suite failed' }
C:\Python314\python.exe -B -m pytest $subsystemTests -q -p no:cacheprovider --basetemp=.pytest-wave-b-final-subsystem
if ($LASTEXITCODE -ne 0) { throw 'Wave B pre-evidence subsystem suite failed' }
C:\Python314\python.exe -B -m pytest -q -p no:cacheprovider --basetemp=.pytest-wave-b-final-full
if ($LASTEXITCODE -ne 0) { throw 'Wave B pre-evidence full suite failed' }
C:\Python314\python.exe -m ruff check --no-cache src tests tools
if ($LASTEXITCODE -ne 0) { throw 'Wave B Ruff check failed' }
C:\Python314\python.exe -m ruff format --check --no-cache src tests tools
if ($LASTEXITCODE -ne 0) { throw 'Wave B Ruff format check failed' }
git diff --check
if ($LASTEXITCODE -ne 0) { throw 'Wave B diff check failed' }
if (git status --porcelain=v1) { throw 'implementation parent is not clean' }
$implementationSha = (git rev-parse HEAD).Trim()
```

The clean resulting source commit is `P`.

### Task 11: Commit candidate evidence as the direct evidence-only child

**Files:** create only `docs/verification/evidence/wave-b/{P[:12]}/` during this task.

- [ ] **Step 1: Run candidate suites at clean `P` into ignored raw staging**

```powershell
$ErrorActionPreference = 'Stop'
$implementationSha = (git rev-parse HEAD).Trim()
$implementationShort = $implementationSha.Substring(0, 12)
$rawDir = ".verification/raw/wave-b/$implementationShort/candidate"
$candidateDir = "docs/verification/evidence/wave-b/$implementationShort"
if (Test-Path -LiteralPath $rawDir) { throw 'candidate raw directory already exists' }
if (Test-Path -LiteralPath $candidateDir) { throw 'candidate directory already exists' }
New-Item -ItemType Directory -Path $rawDir | Out-Null
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'
$targetedTests = @(
  'tests/test_remediation_contracts.py','tests/test_remediation_evidence.py',
  'tests/test_artifact_schema.py','tests/test_artifacts.py','tests/test_output_paths.py',
  'tests/test_experiment_support.py','tests/test_runtime.py','tests/test_figure_store.py',
  'tests/test_figures.py','tests/test_launchers.py','tests/test_finite_experiment.py',
  'tests/test_agent_network_experiment.py','tests/test_attention_experiment.py',
  'tests/test_categorical_dqm_experiment.py','tests/test_counterexample_experiment.py',
  'tests/test_information_history_experiment.py','tests/test_scale_cocycle_experiment.py',
  'tests/test_theory_oracle_experiment.py','tests/test_holonomy_experiment.py',
  'tests/test_gaussian_realization.py','tests/test_gaussian_fixed_ray_diagnostic_experiment.py',
  'tests/test_gaussian_fixed_ray_experiment.py','tests/test_gaussian_confirmatory_experiment.py',
  'tests/test_gaussian_results_document.py','tests/test_wave_b_evidence.py'
)
$subsystemTests = $targetedTests + @(
  'tests/test_config.py','tests/test_agent_network.py','tests/test_counterexamples.py',
  'tests/test_theory_oracles.py','tests/test_gaussian_fixed_ray_diagnostics.py',
  'tests/test_shared_scientific_contracts.py','tests/test_cuda_backend.py'
)

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/targeted.command.json" --junit "$rawDir/targeted.raw.xml" -- C:\Python314\python.exe -B -m pytest $targetedTests -q -p no:cacheprovider --basetemp="$rawDir/tmp-targeted" --junitxml="$rawDir/targeted.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave B candidate targeted suite failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/subsystem.command.json" --junit "$rawDir/subsystem.raw.xml" -- C:\Python314\python.exe -B -m pytest $subsystemTests -q -p no:cacheprovider --basetemp="$rawDir/tmp-subsystem" --junitxml="$rawDir/subsystem.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave B candidate subsystem suite failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/full.command.json" --junit "$rawDir/full.raw.xml" -- C:\Python314\python.exe -B -m pytest -q -p no:cacheprovider --basetemp="$rawDir/tmp-full" --junitxml="$rawDir/full.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave B candidate full suite failed' }
```

- [ ] **Step 2: Build and validate durable candidate evidence**

The wrapper reads raw records/XML once, validates the exact skip maps, scrubs in
memory, re-parses to prove semantic equality, prepares the root and candidate
domain indexes, and publishes one atomic 12-file bundle. It does not require or
accept candidate reviews/adjudicators. The generic root portion is exactly all
11 `GENERIC_PUBLIC_PATHS`, including three sanitized command records,
dependencies, the exact Wave B plan binding, verifier-snapshot binding, and
privacy transform; `wave-b-domain-index.json` is the twelfth file.

```powershell
C:\Python314\python.exe -B tools\build_wave_b_evidence.py build --stage candidate --tested-head $implementationSha --implementation-parent $implementationSha --raw-dir $rawDir --output-dir $candidateDir
if ($LASTEXITCODE -ne 0) { throw 'Wave B candidate build failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py validate "$candidateDir/index.json" --cwd .
if ($LASTEXITCODE -ne 0) { throw 'Wave B candidate root index failed validation' }
$expectedCandidateRelative = @(
  'commands/full.json','commands/subsystem.json','commands/targeted.json',
  'dependencies.json','environment.json','full.xml','index.json',
  'plan-binding.json','privacy-transform.json','subsystem.xml','targeted.xml',
  'wave-b-domain-index.json'
)
$actualCandidateRelative = @(
  Get-ChildItem -LiteralPath $candidateDir -Recurse -File | ForEach-Object {
    [IO.Path]::GetRelativePath($candidateDir, $_.FullName).Replace('\','/')
  } | Sort-Object
)
if ($actualCandidateRelative.Count -ne 12 -or
    (Compare-Object ($expectedCandidateRelative | Sort-Object) $actualCandidateRelative)) {
  throw 'Wave B candidate file set is not exact'
}
```

The root and domain indexes both contain `evidence_stage="candidate"` and
`tested_git_head=implementation_parent_git_head=P`. The domain index points to
the root index; the root index contains no domain reference.

- [ ] **Step 3: Commit exactly one evidence-only child `E`**

```powershell
git add -- "$candidateDir"
git diff --cached --name-only
git commit -m "test: record wave B candidate evidence"
if ($LASTEXITCODE -ne 0) { throw 'Wave B candidate evidence commit failed' }
$evidenceSha = (git rev-parse HEAD).Trim()
$recordedParent = (git rev-parse HEAD^).Trim()
$changed = @(git diff --name-only "$recordedParent..$evidenceSha")
if ($recordedParent -ne $implementationSha) { throw 'candidate child is not direct' }
$unexpected = @($changed | Where-Object { $_ -notlike "$candidateDir/*" })
if ($unexpected.Count -ne 0) { throw "candidate child has non-evidence paths: $unexpected" }
```

The resulting direct evidence-only child is `E`. No source, config, test, tool,
or remediation-contract path may differ in `P..E`.

### Task 12: Close Wave B at exact evidence child `E`

**Files:** create but do not commit the child directory computed as
`verification-evidence/wave-b/{E[:12]}/`; create ignored raw review/JUnit staging
below `.verification/raw/wave-b/{E[:12]}/closure/`; and let the installed gate
create `.verification/active.json` plus `.verification/wave-b/final-ledger.json`.

- [ ] **Step 1: Establish exact `E/P`, create only ignored staging, and rerun all
  three suites**

```powershell
$ErrorActionPreference = 'Stop'
$evidenceSha = (git rev-parse HEAD).Trim()
$implementationSha = (git rev-parse HEAD^).Trim()
$evidenceShort = $evidenceSha.Substring(0, 12)
$implementationShort = $implementationSha.Substring(0, 12)
$rawDir = ".verification/raw/wave-b/$evidenceShort/closure"
$closureDir = "verification-evidence/wave-b/$evidenceShort"
$candidateDir = "docs/verification/evidence/wave-b/$implementationShort"
if ((git rev-parse HEAD^).Trim() -ne $implementationSha) { throw 'invalid E/P relationship' }
if (-not (Test-Path -LiteralPath "$candidateDir/index.json")) { throw 'candidate index for P is missing' }
if (Test-Path -LiteralPath $rawDir) { throw 'closure raw directory already exists' }
if (Test-Path -LiteralPath $closureDir) { throw 'closure evidence directory already exists' }
New-Item -ItemType Directory -Path $rawDir | Out-Null
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'
$pythonPathAtStart = [Environment]::GetEnvironmentVariable('PYTHONPATH', 'Process')

$targetedTests = @(
  'tests/test_remediation_contracts.py','tests/test_remediation_evidence.py',
  'tests/test_artifact_schema.py','tests/test_artifacts.py','tests/test_output_paths.py',
  'tests/test_experiment_support.py','tests/test_runtime.py','tests/test_figure_store.py',
  'tests/test_figures.py','tests/test_launchers.py','tests/test_finite_experiment.py',
  'tests/test_agent_network_experiment.py','tests/test_attention_experiment.py',
  'tests/test_categorical_dqm_experiment.py','tests/test_counterexample_experiment.py',
  'tests/test_information_history_experiment.py','tests/test_scale_cocycle_experiment.py',
  'tests/test_theory_oracle_experiment.py','tests/test_holonomy_experiment.py',
  'tests/test_gaussian_realization.py','tests/test_gaussian_fixed_ray_diagnostic_experiment.py',
  'tests/test_gaussian_fixed_ray_experiment.py','tests/test_gaussian_confirmatory_experiment.py',
  'tests/test_gaussian_results_document.py','tests/test_wave_b_evidence.py'
)
$subsystemTests = $targetedTests + @(
  'tests/test_config.py','tests/test_agent_network.py','tests/test_counterexamples.py',
  'tests/test_theory_oracles.py','tests/test_gaussian_fixed_ray_diagnostics.py',
  'tests/test_shared_scientific_contracts.py','tests/test_cuda_backend.py'
)

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/targeted.command.json" --junit "$rawDir/targeted.raw.xml" -- C:\Python314\python.exe -B -m pytest $targetedTests -q -p no:cacheprovider --basetemp="$rawDir/tmp-targeted" --junitxml="$rawDir/targeted.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave B closure targeted suite failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/subsystem.command.json" --junit "$rawDir/subsystem.raw.xml" -- C:\Python314\python.exe -B -m pytest $subsystemTests -q -p no:cacheprovider --basetemp="$rawDir/tmp-subsystem" --junitxml="$rawDir/subsystem.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave B closure subsystem suite failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/full.command.json" --junit "$rawDir/full.raw.xml" -- C:\Python314\python.exe -B -m pytest -q -p no:cacheprovider --basetemp="$rawDir/tmp-full" --junitxml="$rawDir/full.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave B closure full suite failed' }
```

The runner records the exact six Wave 0 environment keys. `PYTHONPATH` remains
unchanged and is recorded as its current string or JSON `null`; the other five
keys have the exact values established above. The wrapper rejects a command
record with a different key set/value, a nonzero exit, an unexplained skip, or
an ID/reason mismatch against `SKIP_ALLOWLIST_BY_SUITE`.

- [ ] **Step 2: Freeze the review context, obtain two independent reviews and
  15 claim adjudicators, then validate all 17 before either public index**

Read `$candidateDir/index.json`, require `tested_git_head` and
`implementation_parent_git_head` both equal `P`, and take its
`tested_input_inventory_sha256` as the review source/config digest. The closure
wrapper recomputes the same exhaustive selected-input digest at `E`; because
`P..E` is evidence-only, any inequality is a hard failure before publication.

```powershell
if (Test-Path -LiteralPath $closureDir) { throw 'closure exists before review context' }
$reviewContextSha = (& 'C:\Python314\python.exe' -B tools\build_wave_b_evidence.py review-context-sha --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir).Trim()
if ($LASTEXITCODE -ne 0 -or $reviewContextSha -notmatch '^[0-9a-f]{64}$') {
  throw 'Wave B review context digest failed'
}
if (-not (Test-Path -LiteralPath "$rawDir/review-context.json" -PathType Leaf)) {
  throw 'Wave B review context bytes are missing'
}
if (Test-Path -LiteralPath $closureDir) { throw 'review context created public output' }
```

Dispatch exactly two independent reviewers. The `code-runtime` reviewer checks
root reachability/effect order, closed schema dispatch, source eligibility,
legacy nonpromotion, metric/state construction, and every producer carrier.
The `artifact-concurrency` reviewer checks detached prepared bytes, verified
single-read parsing, NPZ policy, figure generation/pointer/journal/crash
transactions, old-generation preservation, and concurrent readers/publishers.
Both review exact `E/P`, the context digest, all three raw command
records/JUnits, the candidate source/config digest, all 126 audit-control
bindings, and every literal `CLAIM_SPECS` entry. Each writes one canonical
UTF-8 JSON object before either public index exists:

```text
.verification/raw/wave-b/{E[:12]}/closure/reviews/code-runtime.json
.verification/raw/wave-b/{E[:12]}/closure/reviews/artifact-concurrency.json
.verification/raw/wave-b/{E[:12]}/closure/reviews/adjudicators/{claim_id}.json
```

Each review has exactly `RAW_REVIEW_KEYS`, schema
`REVIEW_SCHEMA_VERSION`, its exact `VIEW_IDS` member, all 15 claim records, and
the fixed six-key criterion scores. `code-runtime` records AB and
`artifact-concurrency` records BA. Each raw adjudicator has exactly
`RAW_ADJUDICATOR_KEYS`, schema `ADJUDICATOR_SCHEMA_VERSION`, one unique
`CLAIM_SPECS` ID, both view IDs, and the matching spec evidence IDs. Reviewers
author these records; the wrapper never creates them. Both reviews and all 15
claim scores require `escalation_triggers=[]` and
`unresolved_disagreement=false`. Every adjudicator requires
`role="verifier-adjudicator"`, `escalation_triggers=[]`, and
`escalation_target=2`. Exact reviewer agreement yields public result `refute`
for the seven defect propositions and `support` for the seven regression
contracts. CUDA alone uses public result `abstain` with current
dedicated-execution/reproducibility obligations. A trigger or disagreement
invalidates this 29-file branch before publication; it is not published as an
additional `INCONCLUSIVE` claim.

```powershell
$reviewDir = "$rawDir/reviews"
$expectedRawReviewRelative = @(
  'reviews/code-runtime.json','reviews/artifact-concurrency.json',
  'reviews/adjudicators/WAVE-B-AUD-01-DEFECT-REPRODUCES.json',
  'reviews/adjudicators/WAVE-B-AUD-01-REGRESSION-CONTRACT.json',
  'reviews/adjudicators/WAVE-B-AUD-02-DEFECT-REPRODUCES.json',
  'reviews/adjudicators/WAVE-B-AUD-02-REGRESSION-CONTRACT.json',
  'reviews/adjudicators/WAVE-B-AUD-04-DEFECT-REPRODUCES.json',
  'reviews/adjudicators/WAVE-B-AUD-04-REGRESSION-CONTRACT.json',
  'reviews/adjudicators/WAVE-B-AUD-05-DEFECT-REPRODUCES.json',
  'reviews/adjudicators/WAVE-B-AUD-05-REGRESSION-CONTRACT.json',
  'reviews/adjudicators/WAVE-B-AUD-10-DEFECT-REPRODUCES.json',
  'reviews/adjudicators/WAVE-B-AUD-10-REGRESSION-CONTRACT.json',
  'reviews/adjudicators/WAVE-B-AUD-11-DEFECT-REPRODUCES.json',
  'reviews/adjudicators/WAVE-B-AUD-11-REGRESSION-CONTRACT.json',
  'reviews/adjudicators/WAVE-B-AUD-12-DEFECT-REPRODUCES.json',
  'reviews/adjudicators/WAVE-B-AUD-12-REGRESSION-CONTRACT.json',
  'reviews/adjudicators/WAVE-B-CUDA-CURRENTNESS.json'
)
$actualRawReviewRelative = @(
  Get-ChildItem -LiteralPath $reviewDir -Recurse -File | ForEach-Object {
    [IO.Path]::GetRelativePath($rawDir, $_.FullName).Replace('\','/')
  } | Sort-Object
)
if ($actualRawReviewRelative.Count -ne 17 -or
    (Compare-Object ($expectedRawReviewRelative | Sort-Object) $actualRawReviewRelative)) {
  throw 'Wave B raw review/adjudicator set is not exact'
}
C:\Python314\python.exe -B tools\build_wave_b_evidence.py validate-reviews --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir
if ($LASTEXITCODE -ne 0) {
  throw 'Wave B raw review/adjudicator validation failed'
}
foreach ($relative in $expectedRawReviewRelative) {
  if (-not (Test-Path -LiteralPath "$rawDir/$relative" -PathType Leaf)) {
    throw "validated raw review disappeared: $relative"
  }
}
if (Test-Path -LiteralPath $closureDir) { throw 'review validation created closure output' }
```

- [ ] **Step 3: Prepare, atomically publish, and validate the immutable
  29-file closure bundle**

```powershell
C:\Python314\python.exe -B tools\build_wave_b_evidence.py build --stage closure --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir --output-dir $closureDir
if ($LASTEXITCODE -ne 0) { throw 'Wave B closure evidence build failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py validate "$closureDir/index.json" --cwd .
if ($LASTEXITCODE -ne 0) { throw 'Wave B closure root index failed validation' }
$expectedClosureRelative = @(
  'commands/full.json','commands/subsystem.json','commands/targeted.json',
  'dependencies.json','environment.json','full.xml','index.json',
  'plan-binding.json','privacy-transform.json','subsystem.xml','targeted.xml',
  'wave-b-domain-index.json','reviews/code-runtime.json',
  'reviews/artifact-concurrency.json',
  'reviews/adjudicators/WAVE-B-AUD-01-DEFECT-REPRODUCES.json',
  'reviews/adjudicators/WAVE-B-AUD-01-REGRESSION-CONTRACT.json',
  'reviews/adjudicators/WAVE-B-AUD-02-DEFECT-REPRODUCES.json',
  'reviews/adjudicators/WAVE-B-AUD-02-REGRESSION-CONTRACT.json',
  'reviews/adjudicators/WAVE-B-AUD-04-DEFECT-REPRODUCES.json',
  'reviews/adjudicators/WAVE-B-AUD-04-REGRESSION-CONTRACT.json',
  'reviews/adjudicators/WAVE-B-AUD-05-DEFECT-REPRODUCES.json',
  'reviews/adjudicators/WAVE-B-AUD-05-REGRESSION-CONTRACT.json',
  'reviews/adjudicators/WAVE-B-AUD-10-DEFECT-REPRODUCES.json',
  'reviews/adjudicators/WAVE-B-AUD-10-REGRESSION-CONTRACT.json',
  'reviews/adjudicators/WAVE-B-AUD-11-DEFECT-REPRODUCES.json',
  'reviews/adjudicators/WAVE-B-AUD-11-REGRESSION-CONTRACT.json',
  'reviews/adjudicators/WAVE-B-AUD-12-DEFECT-REPRODUCES.json',
  'reviews/adjudicators/WAVE-B-AUD-12-REGRESSION-CONTRACT.json',
  'reviews/adjudicators/WAVE-B-CUDA-CURRENTNESS.json'
)
$actualClosureRelative = @(
  Get-ChildItem -LiteralPath $closureDir -Recurse -File | ForEach-Object {
    [IO.Path]::GetRelativePath($closureDir, $_.FullName).Replace('\','/')
  } | Sort-Object
)
if ($actualClosureRelative.Count -ne 29 -or
    (Compare-Object ($expectedClosureRelative | Sort-Object) $actualClosureRelative)) {
  throw 'Wave B closure file set is not exact'
}
```

Preparation reads each raw command/JUnit/review/adjudicator once, applies Wave
0's ordered privacy transform in memory, and re-parses every scrubbed byte
sequence to prove semantic equality. The generic root portion contains exactly
the 11 `GENERIC_PUBLIC_PATHS`; its `privacy-transform.json` closes every raw
preimage, including all 17 review/adjudicator records. The one-way domain index
binds the root, literal claim specs, both public reviews, and all 15 public
adjudicators. One combined `PreparedEvidenceBundle` is validated before the
generic publisher creates the destination parent. Publication is one atomic
operation. The root index never points to the domain index or any domain review.
The domain index has `evidence_stage="closure"`, `tested_git_head=E`,
`implementation_parent_git_head=P`, and validates every exact
`REQUIRED_CONTROLS` testcase against the targeted/subsystem/full JUnit union.
It reopens no raw input and synthesizes no review field. No closure byte may
change after this step.

- [ ] **Step 4: Enforce exact closure and worktree state**

```powershell
git diff --check
if ($LASTEXITCODE -ne 0) { throw 'Wave B closure diff check failed' }
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) { throw 'Wave B closure index is dirty' }
git diff --quiet
if ($LASTEXITCODE -ne 0) { throw 'Wave B closure worktree is dirty' }
$trackedDirty = @(git status --porcelain=v1 --untracked-files=no)
if ($trackedDirty.Count -ne 0) { throw "tracked worktree is dirty: $trackedDirty" }
$expectedUntracked = @($expectedClosureRelative | ForEach-Object { "$closureDir/$_" } | Sort-Object)
$actualUntracked = @(git ls-files --others --exclude-standard | Sort-Object)
if ($actualUntracked.Count -ne 29 -or
    (Compare-Object $expectedUntracked $actualUntracked)) {
  throw 'unexpected nonignored untracked paths'
}
```

These exact 29 recursive relative paths are the only nonignored untracked
paths: 11 generic files, one domain index, two reviews, and 15 adjudicators.
Both indexes, all JUnits, the normalized environment/dependency/plan/privacy
records, and all public review records are current mechanical evidence. Ignored
`.verification/**` bytes are control-plane/raw inputs only and never substitute
for the public closure set.

- [ ] **Step 5: Start the real gate, prove the empty template fails, populate
  exactly 15 claims, and validate**

```powershell
$verificationSnapshot = 'docs/verification/remediation/verification-contract-v1.json'
$verificationRoot = 'C:\Users\chris and christine\.codex\skills\verification'
$gate = (& 'C:\Python314\python.exe' -B tools\remediation_evidence.py resolve-verification-gate --snapshot $verificationSnapshot --root $verificationRoot).Trim()
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $gate -PathType Leaf)) {
  throw 'Wave 0 verifier snapshot resolution/precheck failed'
}
$ledger = '.verification/wave-b/final-ledger.json'
if (Test-Path -LiteralPath '.verification/active.json') { throw 'verification gate is already active' }
if (Test-Path -LiteralPath $ledger) { throw 'Wave B ledger already exists' }

& 'C:\Python314\python.exe' $gate start --cwd . --mode closure --ledger $ledger
if ($LASTEXITCODE -ne 0) { throw 'verification gate start failed' }
& 'C:\Python314\python.exe' $gate validate --cwd . $ledger
if ($LASTEXITCODE -eq 0) { throw 'empty start template unexpectedly validated' }

C:\Python314\python.exe -B tools\build_wave_b_evidence.py populate-ledger --ledger $ledger --closure-index "$closureDir/index.json"
if ($LASTEXITCODE -ne 0) { throw 'explicit Wave B ledger population failed' }
& 'C:\Python314\python.exe' $gate validate --cwd . $ledger
if ($LASTEXITCODE -ne 0) { throw 'populated Wave B ledger failed validation' }

$defectClaims = @(
  'WAVE-B-AUD-01-DEFECT-REPRODUCES','WAVE-B-AUD-02-DEFECT-REPRODUCES',
  'WAVE-B-AUD-04-DEFECT-REPRODUCES','WAVE-B-AUD-05-DEFECT-REPRODUCES',
  'WAVE-B-AUD-10-DEFECT-REPRODUCES','WAVE-B-AUD-11-DEFECT-REPRODUCES',
  'WAVE-B-AUD-12-DEFECT-REPRODUCES'
)
$contractClaims = @(
  'WAVE-B-AUD-01-REGRESSION-CONTRACT','WAVE-B-AUD-02-REGRESSION-CONTRACT',
  'WAVE-B-AUD-04-REGRESSION-CONTRACT','WAVE-B-AUD-05-REGRESSION-CONTRACT',
  'WAVE-B-AUD-10-REGRESSION-CONTRACT','WAVE-B-AUD-11-REGRESSION-CONTRACT',
  'WAVE-B-AUD-12-REGRESSION-CONTRACT'
)
$cudaClaim = 'WAVE-B-CUDA-CURRENTNESS'
$ledgerJson = Get-Content -LiteralPath $ledger -Raw | ConvertFrom-Json
$claims = @($ledgerJson.claims)
$expectedClaimIds = @(($defectClaims + $contractClaims + $cudaClaim) | Sort-Object)
$actualClaimIds = @($claims.id | Sort-Object)
if ($claims.Count -ne 15 -or (Compare-Object $expectedClaimIds $actualClaimIds)) {
  throw 'Wave B ledger claim set is not exact'
}
$publicReviewPaths = @(
  "$closureDir/reviews/code-runtime.json",
  "$closureDir/reviews/artifact-concurrency.json"
)
foreach ($publicReviewPath in $publicReviewPaths) {
  $publicReview = Get-Content -LiteralPath $publicReviewPath -Raw | ConvertFrom-Json
  if (@($publicReview.escalation_triggers).Count -ne 0 -or
      $publicReview.unresolved_disagreement -ne $false -or
      @($publicReview.claim_scores | Where-Object {
        @($_.escalation_triggers).Count -ne 0 -or
        $_.unresolved_disagreement -ne $false
      }).Count -ne 0) {
    throw "published review violates frozen target-2 branch: $publicReviewPath"
  }
}
$resultToState = @{
  support = 'EVIDENCE_VERIFIED'
  refute = 'REFUTED'
  abstain = 'INCONCLUSIVE'
}
foreach ($claim in $claims) {
  $adjudicatorPath = "$closureDir/reviews/adjudicators/$($claim.id).json"
  $publicAdjudicator = Get-Content -LiteralPath $adjudicatorPath -Raw | ConvertFrom-Json
  if ($publicAdjudicator.role -ne 'verifier-adjudicator' -or
      @($publicAdjudicator.escalation_triggers).Count -ne 0 -or
      $publicAdjudicator.escalation_target -ne 2 -or
      -not $resultToState.ContainsKey([string]$publicAdjudicator.result)) {
    throw "invalid public adjudicator contract: $($claim.id)"
  }
  $expectedState = $resultToState[[string]$publicAdjudicator.result]
  if ($claim.state -ne $expectedState) {
    throw "ledger state differs from mapped public adjudicator result: $($claim.id)"
  }
  if (Compare-Object @($claim.open_obligations) @($publicAdjudicator.open_obligations)) {
    throw "ledger obligations differ from public adjudicator: $($claim.id)"
  }
  if ($claim.id -in $defectClaims -and
      ($publicAdjudicator.result -ne 'refute' -or $claim.state -ne 'REFUTED')) {
    throw "defect proposition did not use refute -> REFUTED: $($claim.id)"
  }
  if ($claim.id -in $contractClaims -and
      ($publicAdjudicator.result -ne 'support' -or $claim.state -ne 'EVIDENCE_VERIFIED')) {
    throw "regression contract did not use support -> EVIDENCE_VERIFIED: $($claim.id)"
  }
}
$cuda = @($claims | Where-Object { $_.id -eq $cudaClaim })
if ($cuda.Count -ne 1 -or $cuda[0].state -ne 'INCONCLUSIVE' -or
    @($cuda[0].open_obligations).Count -eq 0) {
  throw 'Wave B CUDA currentness must map abstain to INCONCLUSIVE with an obligation'
}
```

`populate-ledger` accepts only the untouched gate-created closure template with
root keys exactly `schema_version`, `mode`, `artifact_revision`, and `claims`,
values `schema_version="1.0"`, `mode="closure"`, a validator-accepted concrete
artifact revision, and `claims=[]`. It revalidates both indexes at live `HEAD=E`
and the exact recursive 29-file closure, then atomically replaces only the
existing ledger. It reads statement/domain/severity/evidence IDs from the
literal public `claim_specs`; spec `kind` is copied only into evidence or
counterevidence entries and is never a claim field. Severity is `medium` for
both AUD-01, AUD-02, AUD-04, AUD-10, and AUD-11 members and `low` for AUD-05
and AUD-12. The CUDA-currentness claim is `low` and names the fresh dedicated
CUDA sentinel plus any authorized confirmatory rerun as open obligations; no
CUDA command runs in Wave B.

Every claim copies the gate-generated `artifact_revision` to the claim and its
evidence entries, sets `evidence_invalidated=false`, and uses the exact six
`CODE_CRITERION_KEYS`, statement, evidence IDs, scores, comparisons, verdict,
and open obligations already present in the public review/adjudicator records.
Every claim has exactly `LEDGER_CLAIM_KEYS`; escalation triggers and target live
on the claim, never the verifier. Each `views.scores` member has exactly
`LEDGER_VIEW_SCORE_KEYS` (`view_id`, `criteria`), and each verifier has exactly
`LEDGER_VERIFIER_KEYS`. `views.calibration_kind` equals `CALIBRATION_KIND`.
Top-level claim criteria are the exact ordered arithmetic means of the two
public view scores for each `CODE_CRITERION_KEYS` member; population may not
copy one view or insert a rounded/model-generated aggregate.

The comparison has exactly `LEDGER_COMPARISON_KEYS`, method `pairwise`,
candidate count 2, exact `CANDIDATE_IDS`, the identical two closed
`{id,description}` objects from both public records, `pivot_ids=[]`, and orders
`["AB","BA"]`. It has exactly two matches, one per `VIEW_IDS` member, each
with exactly `LEDGER_MATCH_KEYS`. Left/right follow the named order; outcome,
ordered criterion objects, and result location are copied from that view's
validated public claim-score/review record. No comparison, match, score, or
description is synthesized. Every nested comparison/match/score/calibration
field is mutation-tested through `_validate_and_replace_ledger` before the
gate template can be replaced.
Before ledger replacement, population parses the public JUnits, proves every
criterion's bound node IDs passed, and resolves each evidence location to the
immutable public JUnit/environment record named by
`EVIDENCE_LOCATIONS_BY_ID`. The `{evidence_short}` path component is derived
only from the revalidated closure index's `tested_git_head[:12]`; the gate
`artifact_revision` prefix is never used as a path identity. The seven defect
propositions receive only current mechanical counterevidence with exact
`LEDGER_COUNTEREVIDENCE_KEYS` and `supports=false`. The seven regression
contracts receive current mechanical supporting entries with exact
`LEDGER_EVIDENCE_KEYS` and no `supports` member. CUDA receives its exact
environment/skip counterevidence with `supports=false`.
Each claim has exactly the two public views `code-runtime` and
`artifact-concurrency`; the former preserves AB, the latter BA. The sole
`verifier-adjudicator` projection is byte-faithful to the matching public
adjudicator. The population code never manufactures a view or adjudicator and
maps public result only through the byte-tested
`ADJUDICATOR_RESULT_TO_LEDGER_STATE`. Any review trigger or disagreement has
already failed before public preparation, so it cannot create an additional
closure-state claim. Generic `coverage` or `freshness` criteria are forbidden
and tested to reject. The CUDA claim uses all six code criteria with the exact
`0,0,0,0,20,0` mapping, has public result `abstain`, no current CUDA execution
or harness evidence, and maps to terminal `INCONCLUSIVE`.

The gate artifact digest binds `HEAD=E` and all 29 nonignored closure files.
Neither evidence index embeds that later gate revision. The ignored ledger is
never sole evidence. After successful validation, no file outside the excluded
ledger may change; the final handoff names the ledger so the gate hook can
validate it and remove `.verification/active.json`. Preserve every historical
ledger/artifact unchanged.

- [ ] **Step 6: Publish exact verified `E` only**

Push the dedicated Wave B branch and integrate serially only after the populated
ledger validates. Fast-forward the clean integration branch to exact `E`,
refetch, verify remote/local SHA parity, and preserve all live-checkout WIP. A
merge commit, conflict resolution, source/config/test/tool/candidate/closure
mutation, dependency/environment change, or different final revision
invalidates both reviews and closure and requires Task 12 from Step 1.

## Acceptance Matrix

| Audit | Must-pass mechanical evidence | Closure state |
|---|---|---|
| `AUD-01` | v2 closed inventory; size/hash tamper; single-read verify/parse; source eligibility; figure cache binds source inventory and renderer revision | defect `REFUTED`; contract `EVIDENCE_VERIFIED` |
| `AUD-02` | second-output failure; every generation/pointer boundary; process termination; two publishers; reader all-old/all-new; no generation deletion | defect `REFUTED`; contract `EVIDENCE_VERIFIED` |
| `AUD-04` | complete comparator truth table; finite/enums/tolerance validation; tagged positive infinity; loader recomputation; no caller decision | defect `REFUTED`; contract `EVIDENCE_VERIFIED` |
| `AUD-05` | both premise branches candidate; every returned/persisted verification field candidate; external ledger is sole promoter | defect `REFUTED`; contract `EVIDENCE_VERIFIED` |
| `AUD-10` | arbitrary CWD; normalized root; source/Theory overlap; ignored-untracked exception; tracked/reparse rejection; provenance exclusion | defect `REFUTED`; contract `EVIDENCE_VERIFIED` |
| `AUD-11` | prohibited dtype matrix; read-compatible canonical NPZ; validation before parent; `allow_pickle=False` from verified buffer | defect `REFUTED`; contract `EVIDENCE_VERIFIED` |
| `AUD-12` | read-only/detached spawn mapping; unchanged provenance and generator stream after mutation attempt | defect `REFUTED`; contract `EVIDENCE_VERIFIED` |

## Final Self-Review Checklist

- [ ] Every Wave B audit ID appears in the Goal, task ownership, acceptance matrix, and two-claim ledger instructions; no Wave C/D/E item is claimed closed.
- [ ] Every current writer and reader found by `rg "RunStore|manifest.json|np.load" src` is assigned either v2 migration or explicit legacy dispatch.
- [ ] `PreparedRunBundle` owns exact bytes and publication has no caller-object or lazy-serialization route.
- [ ] Strict JSON and tagged positive infinity are compatible; NPZ writer and reader admit the same canonical dtype/finiteness policy.
- [ ] Source-unavailable bundles cannot close source/config claims; legacy observations cannot become v2; tracked historical bytes are unchanged.
- [ ] Root resolution happens before config hash, provenance, RNG-dependent execution, worker temp creation, gate/GPU activity, or publication.
- [ ] Figure validation happens before destination creation; pointer replacement is the sole activation step; old generations are never reclaimed.
- [ ] Candidate index names `P/P`; closure index names `E/P`; `P..E` is evidence-only; raw exact-child closure is nonignored/uncommitted and gate-bound.
- [ ] Targeted, subsystem, and full totals come only from fresh JUnit XML. CUDA opt-in is absent and current CUDA claims remain `INCONCLUSIVE`.
- [ ] No placeholder, omitted file family, ambiguous command token, UK spelling, or unapproved historical rewrite remains.

## Execution Handoff

Use `superpowers:subagent-driven-development` in this session when independent tasks can be assigned without overlapping files, or `superpowers:executing-plans` in a separate implementation session. Keep Tasks 5-9 serialized where artifact, producer, and figure contracts share files. Do not begin Wave C until Wave B's exact `E` ledger validates and its integration revision is fixed.
