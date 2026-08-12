# Scientific Integrity Remediation Wave C Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Every checkbox is a stopping point; do not combine commits or skip a RED run.

**Goal:** Close `AUD-06`, `AUD-07`, `AUD-08`, `AUD-09`, and `AUD-19` by making every fixed-ray execution consume one validated 2x2 system identity, carrying two unambiguous digests through versioned CPU/CUDA records, resolving one publication root, and rejecting inert scale-cocycle options before effects.

**Architecture:** Wave A supplies the sole spectral assessment and bytes-backed immutable-array boundary. Wave B supplies resolved configurations and detached prepare-then-publish bundles. Wave C validates the complete fixed-ray configuration before provenance, RNG, gate, worker, or output effects; constructs one `FixedRaySystem`; derives a root-invariant scientific digest and a publication-bound execution digest from closed preimages; and threads that identity through every active fixed-ray path. CUDA uses new request/response protocol v3. Existing protocol v1/v2 and persisted fixed-ray v1 records remain read-only legacy observations. Fixed-ray publications use `run-manifest-v3`; general Wave B `run-manifest-v2` remains unchanged.

**Tech Stack:** Python 3.14, frozen dataclasses, NumPy float64, SHA-256, Wave A spectral assessment and `immutable_array`, Wave B canonical roots and detached bundles, pytest/JUnit, Ruff, Git, and optional CUDA Python `C:\anaconda\python.exe` only after a fresh accepted gate.

## Global Constraints

- Start from the exact verified merge of Waves 0, A, and B, with design revision `c43a7c50675cf63b60f7b6cbea9664b638cd4c4e` in history. Fetch `origin/main`, verify its log, and create a fresh isolated `codex/` worktree.
- Treat the reviewed Wave 0 plan as immutable authority: `docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md` must have SHA-256 `dbe2263a3b0fe1e9f5db4ff1fca9a19f819cfd32ef38da71d6e5cb5485723ac2`. Bind its terminal tested Git head, final ledger, closure index, and pinned verification snapshot before Wave C evidence preparation.
- Resolve the installed gate only through `tools/remediation_evidence.py resolve-verification-gate --snapshot docs/verification/remediation/verification-contract-v1.json --root "C:\Users\chris and christine\.codex\skills\verification"`. The explicit canonical `.codex` root is mandatory; no alternate home, PATH-local, copied-script, or fallback gate is eligible.
- Preserve every byte in the user's live checkout. Never stash, reset, clean, switch, or rewrite live configuration.
- Use American English in source, tests, documents, and commits.
- CPU tests use `C:\Python314\python.exe`, cache-disabled pytest, worktree-local basetemps, and fresh JUnit where evidence is requested.
- Do not run CUDA while implementing Tasks 1-9. Task 10 contains the only optional CUDA path and requires current operator authorization for the exact evidence-child revision.
- The current fixed-ray contract is exactly dimension `2`, ordered schemes `("adjacent_pairs", "balanced_alternating")`, float64, logical device `0`, deterministic algorithms `True`, TF32 `False`, and the frozen preregistration.
- Reject unsupported values before provenance collection, RNG construction, output-root creation, gate capture/write, GPU inspection, preflight, worker launch, staging, or bundle preparation.
- `scientific_system_digest` and `execution_binding_digest` are the only digest names. Do not add `identity_digest` or another alias.
- Every persisted producer field named `verification_state` is exactly `CANDIDATE`. Numerical decisions use `pass`, `fail`, or `inconclusive`; external verification states exist only in the ledger.
- No Wave C code promotes attraction, universality, confirmatory equivalence, or CUDA currentness. Absent an authorized exact-revision sentinel, the CUDA operational claim remains `INCONCLUSIVE`.
- The scale-cocycle semantic inventory remains exactly nine payloads. Wave A's exact Fisher witness is nested inside versioned `derivative_cocycle.json`; no tenth `fisher_cocycle_witness.json` is emitted.

## File Responsibility Map

- Modify `src/multiagent_elbo/realizations/gaussian/fixed_ray.py`: import Wave A's sole `MatrixDomainPolicy`, define the frozen fixed-ray instance, require it at construction, freeze system arrays, and keep the canonical builder default.
- Modify `src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py`: fixed-ray execution identity, digest preimages, gate/sentinel/confirmatory schemas, and identity-only execution paths.
- Modify `src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostic_experiment.py`: consume the validated system instead of rebuilding it.
- Modify `src/multiagent_elbo/realizations/gaussian/__init__.py`: re-export the exact Wave A `MatrixDomainPolicy` class object only for frozen compatibility, plus `FROZEN_FIXED_RAY_MATRIX_POLICY`, `FixedRayExecutionIdentity`, and `validate_fixed_ray_execution_identity`.
- Modify `src/multiagent_elbo/artifact_schema.py` and `src/multiagent_elbo/artifacts.py`: add bound `run-manifest-v3` preparation/loading without mutating v2.
- Modify `src/multiagent_elbo/config.py`: shared fail-closed fixed-ray and scale-option validation.
- Modify `src/multiagent_elbo/cuda_backend.py` and `tools/cuda_worker.py`: protocol-v3 records, validation, requested/observed settings, and v1/v2 legacy dispatch.
- Modify `run_gaussian_fixed_ray_lab.py`: build identities before every gate/run/discovery branch and use identity roots.
- Modify `run_gaussian_fixed_ray_diagnostic.py`: supply the source-bound identity to diagnostic replay/publication.
- Modify `src/multiagent_elbo/finite/scale_cocycle_experiment.py` and `run_scale_cocycle_lab.py`: reject unsupported options before effects and preserve the exact nine semantic payloads.
- Modify `tests/test_artifact_schema.py`, `tests/test_config.py`, `tests/test_cuda_backend.py`, `tests/test_gaussian_fixed_ray.py`, `tests/test_gaussian_fixed_ray_diagnostics.py`, `tests/test_gaussian_fixed_ray_diagnostic_experiment.py`, `tests/test_gaussian_fixed_ray_experiment.py`, `tests/test_gaussian_confirmatory_experiment.py`, `tests/test_gaussian_results_document.py`, `tests/test_launchers.py`, `tests/test_scale_cocycle.py`, and `tests/test_scale_cocycle_experiment.py`.
- Create `tools/build_wave_c_evidence.py` and `tests/test_wave_c_evidence.py`.
- Create candidate evidence under `docs/verification/evidence/wave-c/<P-short>/`; create exact-child closure evidence under `verification-evidence/wave-c/<E-short>/`; create the external ledger under `.verification/wave-c/`.

---

### Task 1: Require one strict matrix-domain policy (`AUD-19`)

**Files:**

- Modify: `src/multiagent_elbo/realizations/gaussian/fixed_ray.py`
- Modify: `src/multiagent_elbo/realizations/gaussian/__init__.py`
- Modify: `tests/test_gaussian_fixed_ray.py`
- Modify: `tests/test_gaussian_fixed_ray_diagnostics.py`
- Modify: `tests/test_gaussian_fixed_ray_diagnostic_experiment.py`

**Interfaces:**

```text
from multiagent_elbo.conditioning import MatrixDomainPolicy

FROZEN_FIXED_RAY_MATRIX_POLICY = MatrixDomainPolicy(min_spd_rcond=1e-12)

FixedRaySystem.__init__(
    self,
    *,
    matrix_direction: object,
    spatial_maps: Mapping[str, object],
    perron_ray: object,
    node_factor: object,
    edge_labels: Sequence[tuple[int, int]],
    basin_lower: float,
    basin_upper: float,
    log_block_scale: float,
    domain_policy: MatrixDomainPolicy,
) -> None

build_preregistered_system(
    *, domain_policy: MatrixDomainPolicy = FROZEN_FIXED_RAY_MATRIX_POLICY
) -> FixedRaySystem
```

- [ ] **Step 1: Add literal constructor, policy, and immutable-array RED tests**

Add these imports, this helper, and these tests to
`tests/test_gaussian_fixed_ray.py`:

```python
import ast
from pathlib import Path

import multiagent_elbo.conditioning as conditioning
import multiagent_elbo.realizations.gaussian as gaussian
import multiagent_elbo.realizations.gaussian.fixed_ray as fixed_ray


def _system_kwargs() -> dict[str, object]:
    adjacent = np.full((6, 6), 0.1, dtype=np.float64)
    np.fill_diagonal(adjacent, 0.5)
    alternating = 0.1 * np.array(
        [
            [3, 2, 2, 1, 1, 1],
            [1, 3, 2, 2, 1, 1],
            [1, 1, 3, 2, 2, 1],
            [2, 1, 1, 3, 2, 1],
            [1, 2, 1, 1, 3, 2],
            [2, 1, 2, 1, 1, 3],
        ],
        dtype=np.float64,
    )
    return {
        "matrix_direction": np.array([[2.0, 0.5], [0.5, 1.0]]),
        "spatial_maps": {
            "adjacent_pairs": adjacent,
            "balanced_alternating": alternating,
        },
        "perron_ray": np.ones(6),
        "node_factor": np.ones(4),
        "edge_labels": ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)),
        "basin_lower": 0.25,
        "basin_upper": 4.0,
        "log_block_scale": math.log(2.0),
    }


def test_fixed_ray_reuses_the_one_wave_a_matrix_domain_policy():
    assert fixed_ray.MatrixDomainPolicy is conditioning.MatrixDomainPolicy
    assert gaussian.MatrixDomainPolicy is conditioning.MatrixDomainPolicy
    assert fixed_ray.MatrixDomainPolicy.__module__ == "multiagent_elbo.conditioning"
    assert (
        fixed_ray.FROZEN_FIXED_RAY_MATRIX_POLICY
        == conditioning.MatrixDomainPolicy(min_spd_rcond=1e-12)
    )
    tree = ast.parse(
        Path(fixed_ray.__file__).read_text(encoding="utf-8"),
        filename=fixed_ray.__file__,
    )
    assert [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef) and node.name == "MatrixDomainPolicy"
    ] == []


@pytest.mark.parametrize(
    "value", [True, False, 0.0, -1.0, 1.0, 1.0000001, np.nan, np.inf]
)
def test_matrix_domain_policy_rejects_invalid_threshold(value):
    with pytest.raises((TypeError, ValueError)):
        MatrixDomainPolicy(min_spd_rcond=value)


def test_fixed_ray_system_requires_keyword_domain_policy():
    with pytest.raises(TypeError, match="domain_policy"):
        FixedRaySystem(**_system_kwargs())


@pytest.mark.parametrize(
    "matrix, message",
    [
        (np.diag([np.inf, 1.0]), "finite"),
        (np.array([[1.0, 0.2], [0.1, 1.0]]), "symmetric"),
        (np.diag([1.0, -1.0e-5]), "positive definite"),
        (np.diag([1.0e-13, 1.0]), "reciprocal condition"),
    ],
)
def test_fixed_ray_system_rejects_out_of_domain_matrix(matrix, message):
    values = _system_kwargs()
    values["matrix_direction"] = matrix
    with pytest.raises(ValueError, match=message):
        FixedRaySystem(
            **values,
            domain_policy=MatrixDomainPolicy(min_spd_rcond=1.0e-12),
        )


def test_fixed_ray_system_arrays_cannot_reenable_writeability():
    system = build_preregistered_system()
    arrays = [
        system.matrix_direction,
        system.perron_ray,
        system.node_factor,
        *system.spatial_maps.values(),
    ]
    for array in arrays:
        assert array.flags.writeable is False
        with pytest.raises(ValueError, match="WRITEABLE"):
            array.setflags(write=True)
```

Update the two existing direct `FixedRaySystem` calls in this test file to pass `domain_policy=FROZEN_FIXED_RAY_MATRIX_POLICY`.

- [ ] **Step 2: Run the focused RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_gaussian_fixed_ray.py -k "domain_policy or out_of_domain or writeability" -q -p no:cacheprovider --basetemp=.pytest-wave-c-task1-red
$redExit = $LASTEXITCODE
if ($redExit -eq 0) { throw 'Task 1 RED unexpectedly passed' }
```

Expected: FAIL because the fixed-ray module does not yet import/re-export Wave
A's exact class object, the required parameter does not exist,
nonfinite/ill-conditioned directions do not share Wave A's assessment, and
current NumPy arrays can re-enable `WRITEABLE`.

- [ ] **Step 3: Import the sole Wave A policy and use Wave A's assessment**

Add this exact import and frozen instance to `fixed_ray.py`. Do not define a
class named `MatrixDomainPolicy` anywhere in Wave C:

```python
from multiagent_elbo._immutable import immutable_array
from multiagent_elbo.conditioning import MatrixDomainPolicy, assess_spectral_spd


FROZEN_FIXED_RAY_MATRIX_POLICY = MatrixDomainPolicy(min_spd_rcond=1e-12)
```

At the start of `FixedRaySystem.__init__`, after the required type check, replace the existing eigensolver predicate with:

```python
if not isinstance(domain_policy, MatrixDomainPolicy):
    raise TypeError("domain_policy must be a MatrixDomainPolicy")
assessment = assess_spectral_spd(
    matrix_direction,
    min_rcond=domain_policy.min_spd_rcond,
    atol=0.0,
    rtol=0.0,
)
if assessment.decision != "pass":
    raise ValueError(f"matrix direction is outside the strict SPD domain: {assessment.reason}")
matrix = immutable_array(assessment.matrix, dtype=np.float64)
```

After validating each mutable spatial-map copy, assign `immutable_array(spatial, dtype=np.float64)`. Assign `perron_ray` and `node_factor` through the same function. Store `domain_policy` on the frozen system. Delete all `setflags(write=False)` calls in this class.

- [ ] **Step 4: Make the builder explicit and export the public policy**

Use this definition and call shape:

```python
def build_preregistered_system(
    *,
    domain_policy: MatrixDomainPolicy = FROZEN_FIXED_RAY_MATRIX_POLICY,
) -> FixedRaySystem:
    return FixedRaySystem(
        matrix_direction=((2.0, 0.5), (0.5, 1.0)),
        spatial_maps={
            "adjacent_pairs": adjacent,
            "balanced_alternating": alternating,
        },
        perron_ray=np.ones(6),
        node_factor=np.ones(4),
        edge_labels=((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)),
        basin_lower=0.25,
        basin_upper=4.0,
        log_block_scale=math.log(2.0),
        domain_policy=domain_policy,
    )
```

Re-export the imported policy class object, constant, system, and builder from
`realizations/gaussian/__init__.py` and include them in `__all__`. The re-export
is required by Wave 0's frozen compatibility inventory; it must be object
identity with `multiagent_elbo.conditioning.MatrixDomainPolicy` and must not be
a wrapper, subclass, alias assignment to a second class, or duplicate
definition.

- [ ] **Step 5: Run GREEN, static checks, and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_gaussian_fixed_ray.py tests\test_gaussian_fixed_ray_diagnostics.py tests\test_gaussian_fixed_ray_diagnostic_experiment.py -q -p no:cacheprovider --basetemp=.pytest-wave-c-task1-green
if ($LASTEXITCODE -ne 0) { throw 'Task 1 GREEN failed' }
C:\Python314\python.exe -m ruff check --no-cache src/multiagent_elbo/realizations/gaussian/fixed_ray.py src/multiagent_elbo/realizations/gaussian/__init__.py tests/test_gaussian_fixed_ray.py
if ($LASTEXITCODE -ne 0) { throw 'Task 1 lint failed' }
C:\Python314\python.exe -m ruff format --check --no-cache src/multiagent_elbo/realizations/gaussian/fixed_ray.py src/multiagent_elbo/realizations/gaussian/__init__.py tests/test_gaussian_fixed_ray.py
if ($LASTEXITCODE -ne 0) { throw 'Task 1 format check failed' }
git add -- src/multiagent_elbo/realizations/gaussian/fixed_ray.py src/multiagent_elbo/realizations/gaussian/__init__.py tests/test_gaussian_fixed_ray.py tests/test_gaussian_fixed_ray_diagnostics.py tests/test_gaussian_fixed_ray_diagnostic_experiment.py
if ($LASTEXITCODE -ne 0) { throw 'Task 1 staging failed' }
git commit -m "fix: enforce fixed-ray matrix domain"
if ($LASTEXITCODE -ne 0) { throw 'Task 1 commit failed' }
```

---

### Task 2: Build one resolved immutable execution identity (`AUD-06`)

**Files:**

- Modify: `src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py`
- Modify: `src/multiagent_elbo/realizations/gaussian/__init__.py`
- Modify: `tests/test_gaussian_fixed_ray_experiment.py`
- Modify: `tests/test_gaussian_confirmatory_experiment.py`

**Exact public interface:**

```text
@dataclass(frozen=True)
class FixedRayExecutionIdentity:
    system: FixedRaySystem
    resolved_config: ExperimentConfig
    scientific_system_digest: str
    execution_binding_digest: str
    canonical_output_root: Path
    run_namespace: str
    source_identity: Mapping[str, object]
    config_identity: str


def validate_fixed_ray_execution_identity(
    config: ExperimentConfig,
    repo_root: Path,
) -> FixedRayExecutionIdentity
```

The implementation body is frozen below. `repo_root / "Theory"` is the exact Theory root. The validator calls Wave B's `with_resolved_output_root` exactly once and hashes only the returned configuration.

**Closed digest preimages:**

```python
SCIENTIFIC_DIGEST_DOMAIN = b"multiagent-elbo/fixed-ray-scientific-system/v1\0"
EXECUTION_DIGEST_DOMAIN = b"multiagent-elbo/fixed-ray-execution-binding/v1\0"

SCIENTIFIC_ARRAY_NAMES = (
    "matrix_direction",
    "node_factor",
    "perron_ray",
    "spatial_map.adjacent_pairs",
    "spatial_map.balanced_alternating",
)
```

The canonical scientific JSON object has exactly `schema_version`, `experiment`, `fixture`, `preregistration`, `dimension`, `schemes`, `dtype`, `matrix_domain_policy`, `scientific_numerics`, and `system`. `system` has exactly `arrays`, `edge_labels`, `basin_lower_hex`, `basin_upper_hex`, `log_block_scale_hex`, `primitive_powers`, and `noncommuting_gap_hex`. Each array descriptor has exactly `name`, `dtype`, `shape`, and `sha256`, where `sha256` is `canonical_array_sha256(name, array, "float64")`. Every finite scalar is stored with `float(value).hex()`.

The canonical execution JSON object has exactly `schema_version`, `scientific_system_digest`, `config_identity`, `source_identity`, `canonical_output_root`, and `run_namespace`. `config_identity` is the SHA-256 from `config_sha256(resolved_config)`. `canonical_output_root` is `str(resolved_config.output.root)`. The JSON encoder is Wave B's `canonical_json_bytes`. Each digest is `sha256(domain_separator + canonical_json_bytes(payload)).hexdigest()`.

- [ ] **Step 1: Add root ordering, one-system, and unsupported-dimension RED tests**

Add these tests to `tests/test_gaussian_fixed_ray_experiment.py`:

```python
def test_identity_resolves_config_before_hashing(tmp_path, monkeypatch):
    calls: list[tuple[str, object]] = []
    real_resolver = module.with_resolved_output_root

    def recording_resolver(config, *, anchor, repo_root, theory_root):
        resolved = real_resolver(
            config,
            anchor=anchor,
            repo_root=repo_root,
            theory_root=theory_root,
        )
        calls.append(("resolve", resolved.output.root))
        return resolved

    real_hash = module.config_sha256

    def recording_hash(config):
        calls.append(("hash", config.output.root))
        assert config.output.root.is_absolute()
        return real_hash(config)

    monkeypatch.setattr(module, "with_resolved_output_root", recording_resolver)
    monkeypatch.setattr(module, "config_sha256", recording_hash)
    identity = validate_fixed_ray_execution_identity(
        fixed_ray_config(Path("artifacts") / "fixed-ray"), ROOT
    )
    assert [name for name, unused in calls] == ["resolve", "hash"]
    assert identity.canonical_output_root == (ROOT / "artifacts" / "fixed-ray").resolve()


def test_identity_constructs_exactly_one_system(tmp_path, monkeypatch):
    real_builder = module.build_preregistered_system
    calls = 0

    def counted_builder(*, domain_policy):
        nonlocal calls
        calls += 1
        return real_builder(domain_policy=domain_policy)

    monkeypatch.setattr(module, "build_preregistered_system", counted_builder)
    identity = validate_fixed_ray_execution_identity(fixed_ray_config(tmp_path / "out"), ROOT)
    assert calls == 1
    assert identity.system.matrix_direction.shape == (2, 2)


def test_dimension_three_rejects_before_root_provenance_rng_or_system(tmp_path, monkeypatch):
    config = replace(
        fixed_ray_config(tmp_path / "out"),
        theory=replace(fixed_ray_config(tmp_path / "out").theory, matrix_dimension=3),
    )
    monkeypatch.setattr(module, "with_resolved_output_root", lambda *args, **kwargs: pytest.fail("root resolution"))
    monkeypatch.setattr(module, "collect_provenance", lambda *args, **kwargs: pytest.fail("provenance"))
    monkeypatch.setattr(module.RngStreams, "from_seed", lambda seed: pytest.fail("RNG"))
    monkeypatch.setattr(module, "build_preregistered_system", lambda **kwargs: pytest.fail("system"))
    with pytest.raises(ValueError, match="matrix_dimension must be 2"):
        validate_fixed_ray_execution_identity(config, ROOT)
    assert not (tmp_path / "out").exists()
```

- [ ] **Step 2: Add the exact digest mutation truth table**

Add this table and test. `valid` means an identity is produced; `reject` means validation raises before either digest exists.

```python
DIGEST_MUTATION_TRUTH_TABLE = {
    "output_root": ("valid", False, True),
    "run_name": ("valid", False, True),
    "seed": ("valid", False, True),
    "source_identity": ("valid", False, True),
    "max_frame_condition": ("valid", True, True),
    "min_spd_rcond": ("valid", True, True),
    "system_map_bytes": ("valid", True, True),
    "dimension": ("reject", False, False),
    "scheme_order": ("reject", False, False),
    "compute_dtype": ("reject", False, False),
}


def _assert_digest_change(left, right, scientific_changes, execution_changes):
    assert (left.scientific_system_digest != right.scientific_system_digest) is scientific_changes
    assert (left.execution_binding_digest != right.execution_binding_digest) is execution_changes


def test_root_change_only_changes_execution_binding(tmp_path):
    left = validate_fixed_ray_execution_identity(fixed_ray_config(tmp_path / "left"), ROOT)
    right = validate_fixed_ray_execution_identity(fixed_ray_config(tmp_path / "right"), ROOT)
    _assert_digest_change(left, right, False, True)


def test_every_digest_mutation_has_the_frozen_outcome(tmp_path, monkeypatch):
    baseline_config = fixed_ray_config(tmp_path / "base")
    baseline = validate_fixed_ray_execution_identity(baseline_config, ROOT)

    run_changed = replace(baseline_config, run=replace(baseline_config.run, name="changed-run"))
    _assert_digest_change(
        baseline,
        validate_fixed_ray_execution_identity(run_changed, ROOT),
        *DIGEST_MUTATION_TRUTH_TABLE["run_name"][1:],
    )

    seed_changed = replace(baseline_config, run=replace(baseline_config.run, seed=baseline_config.run.seed + 1))
    _assert_digest_change(
        baseline,
        validate_fixed_ray_execution_identity(seed_changed, ROOT),
        *DIGEST_MUTATION_TRUTH_TABLE["seed"][1:],
    )

    condition_changed = replace(
        baseline_config,
        numerics=replace(
            baseline_config.numerics,
            max_frame_condition=baseline_config.numerics.max_frame_condition / 2.0,
        ),
    )
    _assert_digest_change(
        baseline,
        validate_fixed_ray_execution_identity(condition_changed, ROOT),
        *DIGEST_MUTATION_TRUTH_TABLE["max_frame_condition"][1:],
    )

    threshold_changed = replace(
        baseline_config,
        numerics=replace(baseline_config.numerics, min_spd_rcond=1.0e-10),
    )
    _assert_digest_change(
        baseline,
        validate_fixed_ray_execution_identity(threshold_changed, ROOT),
        *DIGEST_MUTATION_TRUTH_TABLE["min_spd_rcond"][1:],
    )

    for field, config in (
        ("dimension", replace(baseline_config, theory=replace(baseline_config.theory, matrix_dimension=3))),
        ("scheme_order", replace(baseline_config, theory=replace(baseline_config.theory, blocking_schemes=("balanced_alternating", "adjacent_pairs")))),
        ("compute_dtype", replace(baseline_config, compute=replace(baseline_config.compute, dtype="float32"))),
    ):
        assert DIGEST_MUTATION_TRUTH_TABLE[field][0] == "reject"
        with pytest.raises(ValueError):
            validate_fixed_ray_execution_identity(config, ROOT)
```

Add these two tests immediately after the table test:

```python
def test_source_identity_change_only_changes_execution_binding(tmp_path, monkeypatch):
    config = fixed_ray_config(tmp_path / "source-change")
    baseline = validate_fixed_ray_execution_identity(config, ROOT)
    real_collect = module.collect_provenance

    def changed_source(*args, **kwargs):
        payload = copy.deepcopy(real_collect(*args, **kwargs))
        payload["source_identity"]["git_commit"] = "f" * 40
        return payload

    monkeypatch.setattr(module, "collect_provenance", changed_source)
    changed = validate_fixed_ray_execution_identity(config, ROOT)
    _assert_digest_change(baseline, changed, False, True)


def test_valid_system_map_byte_change_changes_both_digests(tmp_path, monkeypatch):
    config = fixed_ray_config(tmp_path / "system-change")
    baseline = validate_fixed_ray_execution_identity(config, ROOT)
    original = build_preregistered_system()
    adjacent = np.array(original.spatial_maps["adjacent_pairs"], copy=True)
    adjacent[0, 0] += 0.01
    adjacent[0, 1] -= 0.01
    changed_system = FixedRaySystem(
        matrix_direction=original.matrix_direction,
        spatial_maps={
            "adjacent_pairs": adjacent,
            "balanced_alternating": original.spatial_maps["balanced_alternating"],
        },
        perron_ray=original.perron_ray,
        node_factor=original.node_factor,
        edge_labels=original.edge_labels,
        basin_lower=original.basin_lower,
        basin_upper=original.basin_upper,
        log_block_scale=original.log_block_scale,
        domain_policy=original.domain_policy,
    )
    monkeypatch.setattr(
        module,
        "build_preregistered_system",
        lambda *, domain_policy: changed_system,
    )
    changed = validate_fixed_ray_execution_identity(config, ROOT)
    _assert_digest_change(baseline, changed, True, True)
```

- [ ] **Step 3: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py -k "identity or digest_mutation or root_change or dimension_three" -q -p no:cacheprovider --basetemp=.pytest-wave-c-task2-red
$redExit = $LASTEXITCODE
if ($redExit -eq 0) { throw 'Task 2 RED unexpectedly passed' }
```

Expected: FAIL because there is no resolved identity, no closed preimage, and active functions independently rebuild the preregistered system.

- [ ] **Step 4: Implement exact validation and digest construction**

Implement the following order in `validate_fixed_ray_execution_identity`:

```python
if not isinstance(config, ExperimentConfig):
    raise TypeError("config must be an ExperimentConfig")
repo_root = Path(repo_root).resolve(strict=True)
if config.theory.experiment != "gaussian_fixed_ray":
    raise ValueError("fixed-ray execution requires gaussian_fixed_ray")
if config.theory.matrix_dimension != 2:
    raise ValueError("matrix_dimension must be 2")
if config.theory.blocking_schemes != ("adjacent_pairs", "balanced_alternating"):
    raise ValueError("blocking_schemes must be adjacent_pairs then balanced_alternating")
if config.numerics.dtype != "float64" or config.compute.dtype != "float64":
    raise ValueError("fixed-ray execution requires float64")
if config.compute.device_index != 0:
    raise ValueError("fixed-ray execution requires device_index 0")
if config.compute.deterministic is not True:
    raise ValueError("fixed-ray execution requires deterministic=True")
if config.compute.allow_tf32 is not False:
    raise ValueError("fixed-ray execution requires allow_tf32=False")
if config.compute.cpu_cuda_parity is not True:
    raise ValueError("fixed-ray execution requires cpu_cuda_parity=True")
if config.compute.backend == "cpu" and config.compute.heavy_sweep_enabled:
    raise ValueError("CPU fixed-ray execution cannot enable the heavy sweep")
if config.output.render_figures:
    raise ValueError("fixed-ray execution has no direct figure renderer")

resolved_config = with_resolved_output_root(
    config,
    anchor=repo_root,
    repo_root=repo_root,
    theory_root=repo_root / "Theory",
)
config_identity = config_sha256(resolved_config)
policy = MatrixDomainPolicy(resolved_config.numerics.min_spd_rcond)
system = build_preregistered_system(domain_policy=policy)
streams = RngStreams.from_seed(resolved_config.run.seed)
provenance = collect_provenance(
    repo_root,
    repo_root / "Theory",
    config_identity,
    streams,
    excluded_output_roots=(resolved_config.output.root,),
)
source_identity = provenance["source_identity"]
if not isinstance(source_identity, Mapping):
    raise ValueError("provenance source_identity must be a mapping")
scientific_payload = _fixed_ray_scientific_payload(resolved_config, system)
scientific_system_digest = _domain_digest(SCIENTIFIC_DIGEST_DOMAIN, scientific_payload)
execution_payload = {
    "schema_version": "fixed-ray-execution-binding-v1",
    "scientific_system_digest": scientific_system_digest,
    "config_identity": config_identity,
    "source_identity": dict(source_identity),
    "canonical_output_root": str(resolved_config.output.root),
    "run_namespace": resolved_config.run.name,
}
execution_binding_digest = _domain_digest(EXECUTION_DIGEST_DOMAIN, execution_payload)
return FixedRayExecutionIdentity(
    system=system,
    resolved_config=resolved_config,
    scientific_system_digest=scientific_system_digest,
    execution_binding_digest=execution_binding_digest,
    canonical_output_root=resolved_config.output.root,
    run_namespace=resolved_config.run.name,
    source_identity=_freeze_json_mapping(source_identity),
    config_identity=config_identity,
)
```

Implement `_fixed_ray_scientific_payload`, `_domain_digest`, and recursive `_freeze_json_mapping` exactly from the field sets and encodings above. Reject Boolean integers, nonfinite scalars, wrong array names/order, non-float64 arrays, malformed SHA-256, and unknown source-identity fields before returning the identity.

- [ ] **Step 5: Run GREEN, static checks, and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py tests\test_gaussian_fixed_ray.py -k "identity or digest or matrix_dimension or root" -q -p no:cacheprovider --basetemp=.pytest-wave-c-task2-green
if ($LASTEXITCODE -ne 0) { throw 'Task 2 GREEN failed' }
C:\Python314\python.exe -m ruff check --no-cache src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py src/multiagent_elbo/realizations/gaussian/__init__.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py
if ($LASTEXITCODE -ne 0) { throw 'Task 2 lint failed' }
C:\Python314\python.exe -m ruff format --check --no-cache src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py src/multiagent_elbo/realizations/gaussian/__init__.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py
if ($LASTEXITCODE -ne 0) { throw 'Task 2 format check failed' }
git add -- src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py src/multiagent_elbo/realizations/gaussian/__init__.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py
if ($LASTEXITCODE -ne 0) { throw 'Task 2 staging failed' }
git commit -m "feat: bind fixed-ray execution identity"
if ($LASTEXITCODE -ne 0) { throw 'Task 2 commit failed' }
```

---

### Task 3: Make every mode fail before effects (`AUD-06`, `AUD-07`)

**Files:**

- Modify: `src/multiagent_elbo/config.py`
- Modify: `src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py`
- Modify: `run_gaussian_fixed_ray_lab.py`
- Modify: `tests/test_config.py`
- Modify: `tests/test_launchers.py`
- Modify: `tests/test_gaussian_fixed_ray_experiment.py`
- Modify: `tests/test_gaussian_confirmatory_experiment.py`

**Changed entry-point signatures:**

```text
def build_cuda_gate_record(
    execution_identity: FixedRayExecutionIdentity,
    *,
    operator_opt_in: bool,
) -> dict[str, object]


def build_confirmatory_gate_record(
    execution_identity: FixedRayExecutionIdentity,
    *,
    operator_opt_in: bool,
) -> dict[str, object]


def run_gaussian_fixed_ray_experiment(
    execution_identity: FixedRayExecutionIdentity,
    *,
    preregistration_path: Path | None = None,
) -> GaussianFixedRayExperimentResult


def run_cuda_sentinel(
    execution_identity: FixedRayExecutionIdentity,
    *,
    operator_opt_in: bool,
    operator_gate: Mapping[str, object],
    accepted_gate_sha256: str,
    work_root: Path,
    sample_count: int = 5,
) -> dict[str, object]


def publish_cuda_sentinel(
    execution_identity: FixedRayExecutionIdentity,
    *,
    operator_opt_in: bool,
    operator_gate: Mapping[str, object],
    accepted_gate_sha256: str,
    staging_root: Path,
) -> GaussianFixedRayExperimentResult


def publish_confirmatory_experiment(
    execution_identity: FixedRayExecutionIdentity,
    *,
    operator_opt_in: bool,
    operator_gate: Mapping[str, object],
    accepted_gate_sha256: str,
    sentinel_run_dir: Path,
    accepted_sentinel_manifest_sha256: str,
    staging_root: Path,
) -> GaussianFixedRayExperimentResult
```

- [ ] **Step 1: Add the complete unsupported-setting RED matrix**

Add this literal test to `tests/test_gaussian_fixed_ray_experiment.py`:

```python
@pytest.mark.parametrize(
    "field, mutate, message",
    [
        ("dimension", lambda c: replace(c, theory=replace(c.theory, matrix_dimension=3)), "matrix_dimension"),
        ("schemes", lambda c: replace(c, theory=replace(c.theory, blocking_schemes=("balanced_alternating", "adjacent_pairs"))), "blocking_schemes"),
        ("dtype", lambda c: replace(c, compute=replace(c.compute, dtype="float32")), "float64"),
        ("device", lambda c: replace(c, compute=replace(c.compute, device_index=1)), "device_index"),
        ("deterministic", lambda c: replace(c, compute=replace(c.compute, deterministic=False)), "deterministic"),
        ("tf32", lambda c: replace(c, compute=replace(c.compute, allow_tf32=True)), "allow_tf32"),
        ("parity", lambda c: replace(c, compute=replace(c.compute, cpu_cuda_parity=False)), "cpu_cuda_parity"),
        ("cpu_heavy", lambda c: replace(c, compute=replace(c.compute, backend="cpu", heavy_sweep_enabled=True)), "heavy sweep"),
    ],
)
def test_unsupported_fixed_ray_setting_has_zero_effects(tmp_path, monkeypatch, field, mutate, message):
    config = mutate(fixed_ray_config(tmp_path / field))
    watched = {
        "gate": lambda *args, **kwargs: pytest.fail("GPU gate"),
        "worker": lambda *args, **kwargs: pytest.fail("worker"),
        "prepare": lambda *args, **kwargs: pytest.fail("bundle preparation"),
        "publish": lambda *args, **kwargs: pytest.fail("publication"),
        "rng": lambda seed: pytest.fail("RNG"),
    }
    monkeypatch.setattr(module, "capture_idle_gpu_gate", watched["gate"])
    monkeypatch.setattr(module, "run_worker_job", watched["worker"])
    monkeypatch.setattr(module, "prepare_fixed_ray_run_bundle", watched["prepare"])
    monkeypatch.setattr(module, "publish_run_bundle", watched["publish"])
    monkeypatch.setattr(module.RngStreams, "from_seed", watched["rng"])
    with pytest.raises(ValueError, match=message):
        validate_fixed_ray_execution_identity(config, ROOT)
    assert not (tmp_path / field).exists()
```

Add this test to `tests/test_launchers.py`:

```python
@pytest.mark.parametrize(
    "mode",
    ["pilot", "cuda_gate", "cuda_sentinel", "confirmatory_gate", "confirmatory_run"],
)
def test_fixed_ray_launcher_validates_identity_before_mode_effects(tmp_path, monkeypatch, mode):
    launcher = load_launcher(
        f"fixed_ray_identity_first_{mode}",
        GAUSSIAN_FIXED_RAY_LAUNCHER,
    )
    launcher.THEORY = {**launcher.THEORY, "matrix_dimension": 3}
    launcher.OUTPUT = {**launcher.OUTPUT, "root": str(tmp_path / "out")}
    operator_mode = mode if mode in {"cuda_gate", "cuda_sentinel"} else "pilot"
    confirmatory_mode = mode if mode.startswith("confirmatory_") else "pilot"
    monkeypatch.setattr(
        launcher,
        "_operator_control",
        lambda: {
            "mode": operator_mode,
            "operator_opt_in": True,
            "accepted_gate_sha256": "a" * 64,
        },
    )
    monkeypatch.setattr(
        launcher,
        "_confirmatory_control",
        lambda: {
            "mode": confirmatory_mode,
            "operator_opt_in": True,
            "accepted_gate_sha256": "b" * 64,
            "accepted_sentinel_manifest_sha256": "c" * 64,
        },
    )
    monkeypatch.setattr(launcher, "_current_git_revision", lambda: "d" * 40)

    def forbidden(*args, **kwargs):
        pytest.fail("mode effect occurred before identity validation")

    monkeypatch.setattr(launcher, "build_cuda_gate_record", forbidden)
    monkeypatch.setattr(launcher, "build_confirmatory_gate_record", forbidden)
    monkeypatch.setattr(launcher, "publish_cuda_sentinel", forbidden)
    monkeypatch.setattr(launcher, "publish_confirmatory_experiment", forbidden)
    monkeypatch.setattr(launcher, "run_gaussian_fixed_ray_experiment", forbidden)
    with pytest.raises(ValueError, match="matrix_dimension"):
        launcher.main()
    assert not (tmp_path / "out").exists()
```

- [ ] **Step 2: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_config.py tests\test_launchers.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py -k "unsupported_fixed_ray or zero_effect or identity_before_effect" -q -p no:cacheprovider --basetemp=.pytest-wave-c-task3-red
$redExit = $LASTEXITCODE
if ($redExit -eq 0) { throw 'Task 3 RED unexpectedly passed' }
```

Expected: FAIL because public entry points still accept raw config and several launcher branches inspect gate/output state before constructing the shared identity.

- [ ] **Step 3: Route the launcher and entry points through identity-only bodies**

Implement one launcher helper:

```python
def _validated_identity(
    run: Mapping[str, object],
    theory: Mapping[str, object],
    numerics: Mapping[str, object],
    output: Mapping[str, object],
    compute: Mapping[str, object],
) -> FixedRayExecutionIdentity:
    config = ExperimentConfig.from_dicts(run, theory, numerics, output, compute)
    return validate_fixed_ray_execution_identity(config, ROOT)
```

For `pilot`, `cuda_gate`, and `cuda_sentinel`, create the one mode identity before reading or capturing a gate. For `confirmatory_gate` and `confirmatory_run`, first create the confirmatory identity and then create the sentinel identity from `_sentinel_run(source_revision)` using the same root and sentinel compute settings; validate both before discovery or GPU inspection. Pass identity objects, never raw config, to all six public functions above. `build_cuda_gate_record` and `build_confirmatory_gate_record` build their v2 records only from the supplied identity and live observations. `publish_cuda_sentinel`, `run_cuda_sentinel`, and `publish_confirmatory_experiment` pass that same identity through every nested producer; none may reconstruct an identity or either digest from raw configuration. Every function begins:

```python
if not isinstance(execution_identity, FixedRayExecutionIdentity):
    raise TypeError("execution_identity must be a FixedRayExecutionIdentity")
config = execution_identity.resolved_config
```

Bodies that need the fixed system use `execution_identity.system` directly. Delete every public-path call that constructs `FixedRaySystem`, hashes an unresolved config, or copies named digest fields from a caller-supplied mapping.

- [ ] **Step 4: Run GREEN and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_config.py tests\test_launchers.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py -q -p no:cacheprovider --basetemp=.pytest-wave-c-task3-green
if ($LASTEXITCODE -ne 0) { throw 'Task 3 GREEN failed' }
C:\Python314\python.exe -m ruff check --no-cache src/multiagent_elbo/config.py src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py run_gaussian_fixed_ray_lab.py tests/test_config.py tests/test_launchers.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py
if ($LASTEXITCODE -ne 0) { throw 'Task 3 lint failed' }
C:\Python314\python.exe -m ruff format --check --no-cache src/multiagent_elbo/config.py src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py run_gaussian_fixed_ray_lab.py tests/test_config.py tests/test_launchers.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py
if ($LASTEXITCODE -ne 0) { throw 'Task 3 format check failed' }
git add -- src/multiagent_elbo/config.py src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py run_gaussian_fixed_ray_lab.py tests/test_config.py tests/test_launchers.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py
if ($LASTEXITCODE -ne 0) { throw 'Task 3 staging failed' }
git commit -m "fix: validate fixed-ray modes before effects"
if ($LASTEXITCODE -ne 0) { throw 'Task 3 commit failed' }
```

---

### Task 4: Introduce closed CUDA worker protocol v3 (`AUD-07`)

**Files:**

- Modify: `src/multiagent_elbo/cuda_backend.py`
- Modify: `tools/cuda_worker.py`
- Modify: `tests/test_cuda_backend.py`
- Modify: `tests/test_experiment_support.py`

**Protocol types and exact signatures:**

```text
@dataclass(frozen=True)
class WorkerRuntimeBindingV3:
    backend: Literal["cpu", "cuda"]
    dtype: Literal["float64"]
    device_index: int
    deterministic: bool
    allow_tf32: bool
    environment_sha256: str
    worker_executable_sha256: str
    worker_script_sha256: str
    cuda_library_manifest_sha256: str | None


@dataclass(frozen=True)
class WorkerRequestV3:
    schema_version: Literal["cuda-worker-request-v3"]
    message_type: Literal["request"]
    job_id: str
    requested: WorkerRuntimeBindingV3
    scientific_system_digest: str
    execution_binding_digest: str
    npz_sha256: str
    arrays: Sequence[WorkerArrayDescriptor]
    output_identity: None


@dataclass(frozen=True)
class WorkerResponseV3:
    schema_version: Literal["cuda-worker-response-v3"]
    message_type: Literal["response"]
    job_id: str
    requested: WorkerRuntimeBindingV3
    observed: WorkerRuntimeBindingV3
    scientific_system_digest: str
    execution_binding_digest: str
    npz_sha256: str
    arrays: Sequence[WorkerArrayDescriptor]
    output_identity: str


@dataclass(frozen=True)
class WorkerJobResult:
    request_manifest: WorkerRequestV3
    response_manifest: WorkerResponseV3
    arrays: Mapping[str, np.ndarray]
    provenance: Mapping[str, object]
    request_json: Path
    input_npz: Path
    response_json: Path
    output_npz: Path


def run_worker_job(
    *,
    worker_python: Path,
    worker_script: Path,
    work_root: Path,
    job_id: str,
    requested_backend: Literal["cpu", "cuda"],
    requested_dtype: Literal["float64"],
    arrays: Mapping[str, np.ndarray],
    environment_lock: Path,
    execution_identity: FixedRayExecutionIdentity,
    device_index: int,
    deterministic: bool,
    allow_tf32: bool,
    timeout_seconds: float = 120.0,
) -> WorkerJobResult


def worker_response_identity(payload: Mapping[str, object]) -> str
```

Use `TYPE_CHECKING` plus postponed annotations for `FixedRayExecutionIdentity`; `cuda_backend.py` must not import `fixed_ray_experiment.py` at runtime.

`worker_response_identity` requires the exact response-v3 key set, requires
`output_identity is None` in its input, and returns lowercase SHA-256 of:

```python
b"multiagent-elbo/cuda-worker-response/v3\0" + canonical_json_bytes(payload)
```

The worker sets `output_identity=None`, calls this helper once, and then inserts
the returned digest. Controller validation copies the response, replaces
`output_identity` with `None`, recomputes through this helper, and compares using
`hmac.compare_digest`. No field in the exact response-v3 schema may be excluded
from the response preimage except the digest's own value. Subprocess timing and
controller-local provenance are not response-v3 fields, are not authenticated by
`output_identity`, and must not be described as authenticated by this protocol.

The request has exactly `schema_version`, `message_type`, `job_id`, `requested`, `scientific_system_digest`, `execution_binding_digest`, `npz_sha256`, `arrays`, and `output_identity`. The response replaces `requested` with the pair `requested`, `observed` and otherwise has the same key set. A runtime binding has exactly the nine fields in `WorkerRuntimeBindingV3`.

Protocol v1 and v2 readers return `LegacyWorkerObservation(schema_version, payload, eligible_for_current_run=False)` and never construct `WorkerRequestV3`, `WorkerResponseV3`, or `WorkerJobResult`.

- [ ] **Step 1: Add closed-schema and requested/observed RED tests**

Add these tests to `tests/test_cuda_backend.py`:

```python
REQUEST_V3_KEYS = {
    "schema_version", "message_type", "job_id", "requested",
    "scientific_system_digest", "execution_binding_digest",
    "npz_sha256", "arrays", "output_identity",
}
RESPONSE_V3_KEYS = REQUEST_V3_KEYS | {"observed"}
RUNTIME_V3_KEYS = {
    "backend", "dtype", "device_index", "deterministic", "allow_tf32",
    "environment_sha256", "worker_executable_sha256", "worker_script_sha256",
    "cuda_library_manifest_sha256",
}


@pytest.fixture
def identity():
    value = object.__new__(FixedRayExecutionIdentity)
    object.__setattr__(value, "scientific_system_digest", "a" * 64)
    object.__setattr__(value, "execution_binding_digest", "b" * 64)
    return value


@pytest.fixture
def valid_request_v3():
    requested = {
        "backend": "cpu",
        "dtype": "float64",
        "device_index": 0,
        "deterministic": True,
        "allow_tf32": False,
        "environment_sha256": "c" * 64,
        "worker_executable_sha256": "d" * 64,
        "worker_script_sha256": "e" * 64,
        "cuda_library_manifest_sha256": None,
    }
    return {
        "schema_version": "cuda-worker-request-v3",
        "message_type": "request",
        "job_id": "fixed-ray.cpu.fixture",
        "requested": requested,
        "scientific_system_digest": "a" * 64,
        "execution_binding_digest": "b" * 64,
        "npz_sha256": "f" * 64,
        "arrays": [],
        "output_identity": None,
    }


@pytest.fixture
def valid_response_v3(valid_request_v3):
    response = copy.deepcopy(valid_request_v3)
    response["schema_version"] = "cuda-worker-response-v3"
    response["message_type"] = "response"
    response["observed"] = copy.deepcopy(response["requested"])
    response["output_identity"] = None
    response["output_identity"] = worker_response_identity(response)
    return response


@pytest.fixture
def legacy_payload():
    return {
        "schema_version": "cuda-worker-protocol-v1",
        "message_type": "response",
        "job_id": "legacy.fixture",
    }


def test_worker_v3_closed_key_sets(valid_request_v3, valid_response_v3):
    assert set(valid_request_v3) == REQUEST_V3_KEYS
    assert set(valid_response_v3) == RESPONSE_V3_KEYS
    assert set(valid_request_v3["requested"]) == RUNTIME_V3_KEYS
    assert set(valid_response_v3["requested"]) == RUNTIME_V3_KEYS
    assert set(valid_response_v3["observed"]) == RUNTIME_V3_KEYS


@pytest.mark.parametrize(
    "field, invalid",
    [
        ("backend", "cuda"),
        ("dtype", "float32"),
        ("device_index", 1),
        ("deterministic", False),
        ("allow_tf32", True),
        ("environment_sha256", "0" * 64),
        ("worker_executable_sha256", "1" * 64),
        ("worker_script_sha256", "2" * 64),
        ("cuda_library_manifest_sha256", "3" * 64),
    ],
)
def test_worker_v3_rejects_each_observed_mismatch(valid_response_v3, identity, field, invalid):
    response = copy.deepcopy(valid_response_v3)
    response["observed"][field] = invalid
    with pytest.raises(WorkerBackendError, match=field):
        validate_worker_response_v3(response, expected_identity=identity)


@pytest.mark.parametrize("field", ["scientific_system_digest", "execution_binding_digest"])
def test_worker_v3_rejects_each_digest_mismatch(valid_response_v3, identity, field):
    response = copy.deepcopy(valid_response_v3)
    response[field] = "f" * 64
    with pytest.raises(WorkerBackendError, match=field):
        validate_worker_response_v3(response, expected_identity=identity)


def test_worker_v3_actual_lock_mutation_cannot_self_echo_requested(
    tmp_path,
    valid_request_v3,
    valid_response_v3,
    identity,
):
    environment_lock = tmp_path / "environment.lock"
    environment_lock.write_bytes(b"requested-lock\n")
    requested_sha256 = file_sha256(environment_lock)
    request = copy.deepcopy(valid_request_v3)
    request["requested"]["environment_sha256"] = requested_sha256

    environment_lock.write_bytes(b"mutated-actual-lock\n")
    actual_sha256 = file_sha256(environment_lock)
    assert actual_sha256 != requested_sha256
    response = copy.deepcopy(valid_response_v3)
    response["requested"] = copy.deepcopy(request["requested"])
    response["observed"]["environment_sha256"] = actual_sha256
    response["output_identity"] = None
    response["output_identity"] = worker_response_identity(response)
    with pytest.raises(WorkerBackendError, match="environment_sha256"):
        validate_worker_response_v3(
            response,
            expected_request=request,
            expected_identity=identity,
        )

    worker_source = Path("tools/cuda_worker.py").read_text(encoding="utf-8")
    assert '"environment_sha256": request["requested"]["environment_sha256"]' not in worker_source
    assert '"environment_sha256": file_sha256(environment_lock)' in worker_source


@pytest.mark.parametrize("schema", ["cuda-worker-protocol-v1", "cuda-worker-request-v2", "cuda-worker-response-v2"])
def test_legacy_worker_records_cannot_become_current(schema, legacy_payload):
    payload = dict(legacy_payload)
    payload["schema_version"] = schema
    observation = load_worker_protocol_record(payload)
    assert observation.schema_version == schema
    assert observation.eligible_for_current_run is False
    assert not isinstance(observation, (WorkerRequestV3, WorkerResponseV3))
```

Add this closed-schema mutation test:

```python
@pytest.mark.parametrize(
    "mutation, message",
    [
        ("unknown_top", "unknown"),
        ("missing_top", "missing"),
        ("unknown_nested", "unknown"),
        ("missing_nested", "missing"),
        ("boolean_device", "device_index"),
        ("invalid_digest", "scientific_system_digest"),
        ("job_mismatch", "job_id"),
        ("downgrade", "schema_version"),
        ("cuda_library_missing", "cuda_library_manifest_sha256"),
        ("cpu_library_present", "cuda_library_manifest_sha256"),
    ],
)
def test_worker_v3_rejects_every_closed_schema_mutation(
    valid_request_v3,
    valid_response_v3,
    identity,
    mutation,
    message,
):
    request = copy.deepcopy(valid_request_v3)
    response = copy.deepcopy(valid_response_v3)
    if mutation == "unknown_top":
        response["surprise"] = True
    elif mutation == "missing_top":
        del response["npz_sha256"]
    elif mutation == "unknown_nested":
        response["observed"]["surprise"] = True
    elif mutation == "missing_nested":
        del response["observed"]["dtype"]
    elif mutation == "boolean_device":
        response["observed"]["device_index"] = True
    elif mutation == "invalid_digest":
        response["scientific_system_digest"] = "not-a-digest"
    elif mutation == "job_mismatch":
        response["job_id"] = "fixed-ray.cpu.other"
    elif mutation == "downgrade":
        response["schema_version"] = "cuda-worker-response-v2"
    elif mutation == "cuda_library_missing":
        response["requested"]["backend"] = "cuda"
        response["observed"]["backend"] = "cuda"
        response["requested"]["cuda_library_manifest_sha256"] = None
        response["observed"]["cuda_library_manifest_sha256"] = None
    elif mutation == "cpu_library_present":
        response["requested"]["cuda_library_manifest_sha256"] = "2" * 64
        response["observed"]["cuda_library_manifest_sha256"] = "2" * 64
    with pytest.raises((TypeError, ValueError, WorkerBackendError), match=message):
        validate_worker_response_v3(
            response,
            expected_request=request,
            expected_identity=identity,
        )
```

- [ ] **Step 2: Run CPU-only RED**

```powershell
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
C:\Python314\python.exe -B -m pytest tests\test_cuda_backend.py tests\test_experiment_support.py -k "worker_v3 or legacy_worker" -q -p no:cacheprovider --basetemp=.pytest-wave-c-task4-red
$redExit = $LASTEXITCODE
if ($redExit -eq 0) { throw 'Task 4 RED unexpectedly passed' }
```

Expected: FAIL because v3 types and validators do not exist. The CUDA-skipped test remains the only permitted skip and no worker subprocess starts in the selected tests.

- [ ] **Step 3: Implement request construction, worker observation, and controller validation**

Implement exact v3 key-set rejection before reading values. In the controller, validate identity and requested fixed-ray settings before `work_root.mkdir` or `subprocess.run`. Resolve `environment_lock` strictly and compute its SHA-256, the worker executable SHA-256, and the worker script SHA-256 before constructing the request. Pass the resolved lock path to the worker as a dedicated `--environment-lock` process argument; do not serialize that private absolute path into either manifest. For CUDA, use the existing preflight's canonical library record and hash it with `canonical_json_bytes`; for CPU, require `cuda_library_manifest_sha256 is None`.

In `tools/cuda_worker.py`, parse only v3 for current execution. Resolve the separately supplied environment-lock path with `strict=True`, select `cuda:{device_index}` or `cpu`, select the actual Torch dtype object, apply the requested deterministic/TF32 values, and construct `observed` from independently observed process state. No `observed` member may be copied from `request["requested"]`:

```python
selected_device = torch.device(
    "cpu" if requested_backend == "cpu" else f"cuda:{requested_device_index}"
)
selected_dtype = getattr(torch, requested_dtype)
environment_lock = Path(parsed_args.environment_lock).resolve(strict=True)
observed = {
    "backend": selected_device.type,
    "dtype": str(selected_dtype).removeprefix("torch."),
    "device_index": 0 if selected_device.type == "cpu" else int(torch.cuda.current_device()),
    "deterministic": bool(torch.are_deterministic_algorithms_enabled()),
    "allow_tf32": False if requested_backend == "cpu" else bool(
        torch.backends.cuda.matmul.allow_tf32 or torch.backends.cudnn.allow_tf32
    ),
    "environment_sha256": file_sha256(environment_lock),
    "worker_executable_sha256": file_sha256(Path(sys.executable).resolve()),
    "worker_script_sha256": file_sha256(Path(__file__).resolve()),
    "cuda_library_manifest_sha256": None if requested_backend == "cpu" else canonical_library_manifest_sha256(torch),
}
```

Reject requested/observed divergence in the worker before computing arrays and again in the controller before returning `WorkerJobResult`. The test suite mutates the environment-lock bytes after request construction and proves the worker's independently hashed `observed.environment_sha256` exposes the divergence. Compute `output_identity` over the exact v3 response payload with `output_identity=None`; the digest field is excluded from its own preimage. Do not relabel v1/v2 payloads, and make no timing/provenance authentication claim outside that closed response.

- [ ] **Step 4: Run GREEN, static checks, and commit**

```powershell
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
C:\Python314\python.exe -B -m pytest tests\test_cuda_backend.py tests\test_experiment_support.py -q -p no:cacheprovider --basetemp=.pytest-wave-c-task4-green
if ($LASTEXITCODE -ne 0) { throw 'Task 4 GREEN failed' }
C:\Python314\python.exe -m ruff check --no-cache src/multiagent_elbo/cuda_backend.py tools/cuda_worker.py tests/test_cuda_backend.py tests/test_experiment_support.py
if ($LASTEXITCODE -ne 0) { throw 'Task 4 lint failed' }
C:\Python314\python.exe -m ruff format --check --no-cache src/multiagent_elbo/cuda_backend.py tools/cuda_worker.py tests/test_cuda_backend.py tests/test_experiment_support.py
if ($LASTEXITCODE -ne 0) { throw 'Task 4 format check failed' }
git add -- src/multiagent_elbo/cuda_backend.py tools/cuda_worker.py tests/test_cuda_backend.py tests/test_experiment_support.py
if ($LASTEXITCODE -ne 0) { throw 'Task 4 staging failed' }
git commit -m "feat: bind CUDA worker protocol v3"
if ($LASTEXITCODE -ne 0) { throw 'Task 4 commit failed' }
```

---

### Task 5: Version and propagate both digests through every persisted fixed-ray record (`AUD-06`, `AUD-07`)

**Files:**

- Modify: `src/multiagent_elbo/artifact_schema.py`
- Modify: `src/multiagent_elbo/artifacts.py`
- Modify: `src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py`
- Modify: `src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostic_experiment.py`
- Modify: `src/multiagent_elbo/realizations/gaussian/__init__.py`
- Modify: `run_gaussian_fixed_ray_diagnostic.py`
- Modify: `tests/test_artifact_schema.py`
- Modify: `tests/test_gaussian_fixed_ray_experiment.py`
- Modify: `tests/test_gaussian_confirmatory_experiment.py`
- Modify: `tests/test_gaussian_fixed_ray_diagnostic_experiment.py`
- Modify: `tests/test_gaussian_results_document.py`
- Modify: `tests/test_launchers.py`

**Manifest-v3 interfaces:**

```text
def prepare_fixed_ray_run_bundle(
    config: ExperimentConfig,
    provenance: Mapping[str, object],
    payloads: RunPayloads,
    *,
    scientific_system_digest: str,
    execution_binding_digest: str,
) -> PreparedRunBundle


def load_verified_fixed_ray_bundle(
    run_dir: Path | str,
    *,
    expected_scientific_system_digest: str,
    expected_execution_binding_digest: str,
) -> VerifiedFixedRayRunBundle


def run_fixed_model_diagnostic(
    execution_identity: FixedRayExecutionIdentity,
    source_binding: ConfirmatorySourceBinding,
    source_dir: Path,
) -> GaussianFixedRayDiagnosticResult
```

`run-manifest-v3` has exactly these top-level keys:

```python
RUN_MANIFEST_V3_KEYS = {
    "schema_version",
    "status",
    "artifact_kind",
    "config_identity",
    "source_identity",
    "scientific_system_digest",
    "execution_binding_digest",
    "artifacts",
}
```

Its `schema_version` is `run-manifest-v3`; all other Wave B v2 key meanings, artifact ordering, detached-buffer ownership, manifest-last publication, verification-before-parse, and zero-effect failure rules are unchanged. `prepare_run_bundle` continues to emit v2 for non-fixed-ray producers. `load_verified_run_bundle` continues to read v2. A v2 bundle cannot be returned by `load_verified_fixed_ray_bundle` and cannot satisfy a current fixed-ray execution claim. The fixed-ray loader's two expected-digest keywords are mandatory: a manifest cannot authenticate a binding merely by agreeing with its own digest fields.

**Exact current and legacy record versions:**

```python
CURRENT_FIXED_RAY_SCHEMAS = {
    "idle_gate": "cuda-idle-operator-gate-v2",
    "confirmatory_gate": "cuda-confirmatory-operator-gate-v2",
    "sentinel": "gaussian-fixed-ray-cuda-sentinel-v2",
    "worker_exchange_index": "gaussian-fixed-ray-worker-exchange-index-v2",
    "confirmatory_job": "gaussian-fixed-ray-confirmatory-job-v2",
    "primary_execution": "gaussian-fixed-ray-confirmatory-primary-execution-v2",
    "holdout_execution": "gaussian-fixed-ray-confirmatory-holdout-execution-v2",
    "confirmatory_execution": "gaussian-fixed-ray-confirmatory-execution-v2",
    "confirmatory_endpoints": "gaussian-fixed-ray-confirmatory-endpoints-v2",
    "job_table": "gaussian-fixed-ray-job-table-v2",
    "pilot_endpoints": "gaussian-fixed-ray-endpoints-v2",
}

LEGACY_FIXED_RAY_SCHEMAS = {
    "idle_gate": "cuda-idle-operator-gate-v1",
    "confirmatory_gate": "cuda-confirmatory-operator-gate-v1",
    "sentinel": "gaussian-fixed-ray-cuda-sentinel-v1",
    "worker_exchange_index": "gaussian-fixed-ray-worker-exchange-index-v1",
    "confirmatory_job": "gaussian-fixed-ray-confirmatory-job-v1",
    "primary_execution": "gaussian-fixed-ray-confirmatory-primary-execution-v1",
    "holdout_execution": "gaussian-fixed-ray-confirmatory-holdout-execution-v1",
    "confirmatory_execution": "gaussian-fixed-ray-confirmatory-execution-v1",
    "confirmatory_endpoints": "gaussian-fixed-ray-confirmatory-endpoints-v1",
    "job_table": "gaussian-fixed-ray-job-table-v1",
    "pilot_endpoints": "gaussian-fixed-ray-endpoints-v1",
}
```

Every current record above has top-level `scientific_system_digest` and `execution_binding_digest`. Every nested step, endpoint, worker exchange, terminal job, primary result, and holdout result also carries those two fields. In particular, `build_cuda_gate_record(execution_identity, *, operator_opt_in)` emits `cuda-idle-operator-gate-v2`, `build_confirmatory_gate_record(execution_identity, *, operator_opt_in)` emits `cuda-confirmatory-operator-gate-v2`, and both closed gate records carry the two named digests from that exact identity. `publish_cuda_sentinel(execution_identity, ...)` passes the same object to `run_cuda_sentinel` and `prepare_fixed_ray_run_bundle`, so the sentinel-v2 record, every nested record, and manifest-v3 carry the identical pair. These functions reject a raw `ExperimentConfig`; no gate or sentinel publisher reconstructs either digest from config or gate bytes. A legacy loader returns `LegacyFixedRayObservation(kind, schema_version, payload, observed_at_revision, eligible_for_current_run=False)`.

- [ ] **Step 1: Add manifest-v3 closed-schema and legacy-separation RED tests**

Add these imports, fixtures, and tests to `tests/test_artifact_schema.py`:

```python
from multiagent_elbo.config import ExperimentConfig, config_sha256
from multiagent_elbo.output_paths import with_resolved_output_root
from multiagent_elbo.runtime import RngStreams, collect_provenance


def _fixed_ray_artifact_config(tmp_path: Path, *, name: str) -> ExperimentConfig:
    repo_root = Path(__file__).resolve().parents[1]
    unresolved = ExperimentConfig.from_dicts(
        {"name": name, "seed": 20260809},
        {
            "experiment": "gaussian_fixed_ray",
            "fixture": "gaussian_fixed_ray_v1",
            "preregistration": "2026-08-09-gaussian-fixed-ray-v1",
            "blocking_schemes": ["adjacent_pairs", "balanced_alternating"],
            "matrix_dimension": 2,
        },
        {
            "dtype": "float64",
            "atol": 1.0e-12,
            "rtol": 1.0e-10,
            "min_spd_rcond": 1.0e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(tmp_path / "artifacts"),
            "collect_diagnostics": True,
            "render_figures": False,
        },
        {
            "backend": "cpu",
            "dtype": "float64",
            "device_index": 0,
            "batch_size": 4096,
            "deterministic": True,
            "allow_tf32": False,
            "cpu_cuda_parity": True,
            "cuda_worker_python": r"C:\anaconda\python.exe",
            "heavy_sweep_enabled": False,
        },
    )
    return with_resolved_output_root(
        unresolved,
        anchor=repo_root,
        repo_root=repo_root,
        theory_root=repo_root / "Theory",
    )


def _general_preparation_inputs(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    config = _fixed_ray_artifact_config(tmp_path, name="manifest-v2-control")
    provenance = collect_provenance(
        repo_root,
        repo_root / "Theory",
        config_sha256(config),
        RngStreams.from_seed(config.run.seed),
        excluded_output_roots=(config.output.root,),
    )
    payloads = RunPayloads(
        artifact_kind="test_general_bundle",
        json_payloads={
            "record.json": {
                "schema_version": "test-record-v1",
                "verification_state": "CANDIDATE",
            }
        },
        npz_payloads={
            "arrays.npz": {
                "values": NpzArrayInput(np.ones((1, 1), dtype=np.float64), "finite")
            }
        },
    )
    return config, provenance, payloads


@pytest.fixture
def general_preparation_inputs(tmp_path):
    return _general_preparation_inputs(tmp_path)


@pytest.fixture
def fixed_ray_preparation_inputs(tmp_path):
    config, provenance, payloads = _general_preparation_inputs(tmp_path)
    return config, provenance, payloads, "a" * 64, "b" * 64


def test_fixed_ray_bundle_uses_closed_manifest_v3(fixed_ray_preparation_inputs):
    config, provenance, payloads, scientific_digest, execution_digest = fixed_ray_preparation_inputs
    prepared = prepare_fixed_ray_run_bundle(
        config,
        provenance,
        payloads,
        scientific_system_digest=scientific_digest,
        execution_binding_digest=execution_digest,
    )
    manifest = json.loads(prepared.manifest_bytes)
    assert set(manifest) == RUN_MANIFEST_V3_KEYS
    assert manifest["schema_version"] == "run-manifest-v3"
    assert manifest["scientific_system_digest"] == scientific_digest
    assert manifest["execution_binding_digest"] == execution_digest


def test_general_bundle_remains_manifest_v2(general_preparation_inputs):
    config, provenance, payloads = general_preparation_inputs
    prepared = prepare_run_bundle(config, provenance, payloads)
    assert json.loads(prepared.manifest_bytes)["schema_version"] == "run-manifest-v2"


def test_fixed_ray_loader_rejects_v2_without_promotion(tmp_path, general_preparation_inputs):
    config, provenance, payloads = general_preparation_inputs
    store = publish_run_bundle(prepare_run_bundle(config, provenance, payloads))
    with pytest.raises(ValueError, match="run-manifest-v3"):
        load_verified_fixed_ray_bundle(
            store.run_dir,
            expected_scientific_system_digest="a" * 64,
            expected_execution_binding_digest="b" * 64,
        )
```

- [ ] **Step 2: Add exact schema-map, propagation, count, and mutation RED tests**

Add this literal assertion to `tests/test_gaussian_fixed_ray_experiment.py`:

```python
EXPECTED_CURRENT_FIXED_RAY_SCHEMAS = {
    "idle_gate": "cuda-idle-operator-gate-v2",
    "confirmatory_gate": "cuda-confirmatory-operator-gate-v2",
    "sentinel": "gaussian-fixed-ray-cuda-sentinel-v2",
    "worker_exchange_index": "gaussian-fixed-ray-worker-exchange-index-v2",
    "confirmatory_job": "gaussian-fixed-ray-confirmatory-job-v2",
    "primary_execution": "gaussian-fixed-ray-confirmatory-primary-execution-v2",
    "holdout_execution": "gaussian-fixed-ray-confirmatory-holdout-execution-v2",
    "confirmatory_execution": "gaussian-fixed-ray-confirmatory-execution-v2",
    "confirmatory_endpoints": "gaussian-fixed-ray-confirmatory-endpoints-v2",
    "job_table": "gaussian-fixed-ray-job-table-v2",
    "pilot_endpoints": "gaussian-fixed-ray-endpoints-v2",
}


def _assert_binding(record, identity):
    assert record["scientific_system_digest"] == identity.scientific_system_digest
    assert record["execution_binding_digest"] == identity.execution_binding_digest


def test_current_fixed_ray_schema_map_is_exact():
    assert CURRENT_FIXED_RAY_SCHEMAS == EXPECTED_CURRENT_FIXED_RAY_SCHEMAS
    assert set(CURRENT_FIXED_RAY_SCHEMAS) == set(LEGACY_FIXED_RAY_SCHEMAS)
    assert all(value.endswith("-v2") for value in CURRENT_FIXED_RAY_SCHEMAS.values())
    assert all(value.endswith("-v1") for value in LEGACY_FIXED_RAY_SCHEMAS.values())


@pytest.mark.parametrize("field", ["scientific_system_digest", "execution_binding_digest"])
def test_digest_mutation_blocks_resume_before_publication(field, monkeypatch):
    identity = object.__new__(FixedRayExecutionIdentity)
    object.__setattr__(identity, "scientific_system_digest", "a" * 64)
    object.__setattr__(identity, "execution_binding_digest", "b" * 64)
    record = _published_job("C001", "confirmatory_primary", identity=identity)
    record[field] = "f" * 64
    monkeypatch.setattr(module, "prepare_fixed_ray_run_bundle", lambda *args, **kwargs: pytest.fail("publication"))
    with pytest.raises(ValueError, match=field):
        validate_terminal_job_for_resume(record, expected_identity=identity)
```

Add this exhaustive common-layer mutation loop:

```python
@pytest.mark.parametrize("kind", tuple(EXPECTED_CURRENT_FIXED_RAY_SCHEMAS))
@pytest.mark.parametrize("field", ["scientific_system_digest", "execution_binding_digest"])
def test_every_current_record_schema_rejects_each_binding_mutation(kind, field, identity):
    record = {
        "schema_version": EXPECTED_CURRENT_FIXED_RAY_SCHEMAS[kind],
        "scientific_system_digest": identity.scientific_system_digest,
        "execution_binding_digest": identity.execution_binding_digest,
    }
    record[field] = "f" * 64
    with pytest.raises(ValueError, match=field):
        validate_execution_binding_fields(record, expected_identity=identity)


@pytest.mark.parametrize("field", ["scientific_system_digest", "execution_binding_digest"])
def test_run_manifest_v3_rejects_each_binding_mutation(
    fixed_ray_preparation_inputs,
    field,
):
    config, provenance, payloads, scientific_digest, execution_digest = fixed_ray_preparation_inputs
    store = publish_run_bundle(
        prepare_fixed_ray_run_bundle(
            config,
            provenance,
            payloads,
            scientific_system_digest=scientific_digest,
            execution_binding_digest=execution_digest,
        )
    )
    manifest_path = store.run_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="ascii"))
    manifest[field] = "f" * 64
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")),
        encoding="ascii",
    )
    with pytest.raises(ValueError, match=field):
        load_verified_fixed_ray_bundle(
            manifest_path.parent,
            expected_scientific_system_digest=scientific_digest,
            expected_execution_binding_digest=execution_digest,
        )
```

In `tests/test_gaussian_fixed_ray_experiment.py`, migrate the existing
`test_cuda_sentinel_runs_five_frozen_jobs_through_three_float64_lanes` to create
`identity = validate_fixed_ray_execution_identity(config, ROOT)` before the
call, pass `identity` instead of `config`, and add these literal assertions
after the existing count assertions:

```python
_assert_binding(sentinel, identity)
assert len(sentinel["step_records"]) == 80
assert len(sentinel["endpoint_records"]) == 10
assert len(sentinel["worker_jobs"]) == 240
for collection in ("step_records", "endpoint_records", "worker_jobs"):
    for record in sentinel[collection]:
        _assert_binding(record, identity)
```

In `tests/test_gaussian_confirmatory_experiment.py`, add this helper immediately
before `_published_job`:

```python
def _published_exchange(job_id: str, index: int, identity: FixedRayExecutionIdentity):
    runtime = {
        "backend": "cuda",
        "dtype": "float64",
        "device_index": 0,
        "deterministic": True,
        "allow_tf32": False,
        "environment_sha256": "c" * 64,
        "worker_executable_sha256": "d" * 64,
        "worker_script_sha256": "e" * 64,
        "cuda_library_manifest_sha256": "f" * 64,
    }
    response = {
        "schema_version": "cuda-worker-response-v3",
        "message_type": "response",
        "job_id": f"{job_id}.exchange.{index:02d}",
        "requested": dict(runtime),
        "observed": dict(runtime),
        "scientific_system_digest": identity.scientific_system_digest,
        "execution_binding_digest": identity.execution_binding_digest,
        "npz_sha256": "0" * 64,
        "arrays": [],
        "output_identity": None,
    }
    response["output_identity"] = worker_response_identity(response)
    return response
```

Change `_published_job` to accept the required keyword
`identity: FixedRayExecutionIdentity`, insert these literal members in its return
mapping, and pass the same identity at all forty call sites:

```text
"scientific_system_digest": identity.scientific_system_digest,
"execution_binding_digest": identity.execution_binding_digest,
"worker_exchanges": [
    _published_exchange(job_id, index, identity) for index in range(16)
],
"worker_exchange_count": 16,
```

In the existing publication-contract test, immediately after `config` is
created, add:

```python
identity = validate_fixed_ray_execution_identity(
    config,
    Path(__file__).resolve().parents[1],
)
```

Load the result through the fixed-ray loader and add:

```python
bundle = load_verified_fixed_ray_bundle(
    result.run_dir,
    expected_scientific_system_digest=identity.scientific_system_digest,
    expected_execution_binding_digest=identity.execution_binding_digest,
)
execution = bundle.json_payloads["confirmatory_execution.json"]
jobs = execution["jobs"]
assert len(jobs) == 40
assert sum(len(job["worker_exchanges"]) for job in jobs) == 640
_assert_binding(execution, identity)
for job in jobs:
    _assert_binding(job, identity)
    for exchange in job["worker_exchanges"]:
        _assert_binding(exchange, identity)
```

Add this source-first, one-identity launcher test to `tests/test_launchers.py`:

```python
def test_diagnostic_launcher_builds_source_bound_identity_exactly_once(
    tmp_path,
    monkeypatch,
):
    launcher = load_launcher(
        "fixed_ray_diagnostic_source_bound_identity",
        GAUSSIAN_FIXED_RAY_DIAGNOSTIC_LAUNCHER,
    )
    source_root = tmp_path / "source"
    shutil.copytree(GAUSSIAN_CONFIRMATORY_SOURCE, source_root)
    launcher.SOURCE = {"root": str(source_root)}
    launcher.OUTPUT = {**launcher.OUTPUT, "root": str(tmp_path / "output")}
    launcher.COMPUTE = {
        **launcher.COMPUTE,
        "backend": "cpu",
        "dtype": "float64",
        "device_index": 0,
        "deterministic": True,
        "allow_tf32": False,
        "cpu_cuda_parity": True,
        "heavy_sweep_enabled": False,
    }
    revision = "d" * 40
    source_binding = launcher.ConfirmatorySourceBinding.from_path(
        source_root / "source_binding.json",
        diagnostic_revision=revision,
    )
    source_digest = source_binding.canonical_source_binding_sha256
    expected_namespace = f"{launcher.RUN['name']}-{source_digest}"
    identity = object()
    calls: list[str] = []
    monkeypatch.setattr(launcher, "_current_git_revision", lambda: revision)

    def validate_once(config, repo_root):
        calls.append("identity")
        assert repo_root == launcher.ROOT
        assert config.run.name == expected_namespace
        assert config.compute.backend == "cpu"
        assert config.compute.dtype == "float64"
        assert config.compute.device_index == 0
        assert config.compute.deterministic is True
        assert config.compute.allow_tf32 is False
        assert config.compute.cpu_cuda_parity is True
        assert config.compute.heavy_sweep_enabled is False
        return identity

    def consume_same_identity(received, binding, source_dir):
        calls.append("run")
        assert received is identity
        assert binding.canonical_source_binding_sha256 == source_digest
        assert source_dir == source_root.resolve()
        return SimpleNamespace(
            run_dir=tmp_path / "published",
            status="complete",
            source_binding_sha256=source_digest,
        )

    monkeypatch.setattr(
        launcher,
        "validate_fixed_ray_execution_identity",
        validate_once,
    )
    monkeypatch.setattr(
        launcher,
        "run_fixed_model_diagnostic",
        consume_same_identity,
    )
    result = launcher.main()
    assert result.source_binding_sha256 == source_digest
    assert calls == ["identity", "run"]
```

- [ ] **Step 3: Run RED**

```powershell
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
C:\Python314\python.exe -B -m pytest tests\test_artifact_schema.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py tests\test_gaussian_fixed_ray_diagnostic_experiment.py tests\test_gaussian_results_document.py tests\test_launchers.py -k "manifest_v3 or schema_map or both_digests or digest_mutation or one_system or source_bound_identity" -q -p no:cacheprovider --basetemp=.pytest-wave-c-task5-red
$redExit = $LASTEXITCODE
if ($redExit -eq 0) { throw 'Task 5 RED unexpectedly passed' }
```

Expected: FAIL because current records use v1 shapes, run-manifest-v2 has no fixed-ray bindings, and active helpers rebuild the system.

- [ ] **Step 4: Implement bound preparation and version dispatch**

Factor Wave B's pure preparation internals so both public preparation functions validate all caller objects and create detached `PreparedArtifact` bytes before manifest construction. `prepare_fixed_ray_run_bundle` validates both lowercase SHA-256 values and creates v3 bytes from the exact key set above. `publish_run_bundle` accepts prepared v2 or v3 bytes without reserializing. `load_verified_fixed_ray_bundle` verifies manifest size/hash inventory and parses each same buffer once before returning immutable payloads.

Implement legacy fixed-ray dispatch as:

```python
def load_fixed_ray_record(
    kind: str,
    payload: Mapping[str, object],
    *,
    observed_at_revision: str | None = None,
) -> Mapping[str, object] | LegacyFixedRayObservation:
    schema = payload.get("schema_version")
    if schema == CURRENT_FIXED_RAY_SCHEMAS[kind]:
        return validate_current_fixed_ray_record(kind, payload)
    if schema == LEGACY_FIXED_RAY_SCHEMAS[kind]:
        if observed_at_revision is None:
            raise ValueError("legacy fixed-ray record requires observed_at_revision")
        return LegacyFixedRayObservation(
            kind=kind,
            schema_version=str(schema),
            payload=_freeze_json_mapping(payload),
            observed_at_revision=observed_at_revision,
            eligible_for_current_run=False,
        )
    raise ValueError(f"unsupported {kind} schema_version")
```

- [ ] **Step 5: Thread the one identity through all fixed-ray producers**

Change `_job_table`, `run_confirmatory_job`, primary/holdout helpers, resume validators, sentinel analysis, and diagnostic replay helpers to accept `execution_identity: FixedRayExecutionIdentity`. Replace each internal `build_preregistered_system()` with `execution_identity.system`. Change `run_fixed_model_diagnostic` to the exact identity-bearing signature above and begin it by setting `config = execution_identity.resolved_config`; remove `_diagnostic_config` entirely. Every v2 record is built through:

```python
def _with_execution_binding(
    schema_version: str,
    identity: FixedRayExecutionIdentity,
    fields: Mapping[str, object],
) -> dict[str, object]:
    payload = {
        "schema_version": schema_version,
        "scientific_system_digest": identity.scientific_system_digest,
        "execution_binding_digest": identity.execution_binding_digest,
        **fields,
    }
    if len(payload) != len(fields) + 3:
        raise ValueError("fixed-ray record attempted to overwrite a binding field")
    return payload
```

Use `prepare_fixed_ray_run_bundle` for CPU pilot, sentinel, confirmatory, and fixed-model diagnostic publication. Put both digests in each run manifest and provenance record. Before resume or downstream analysis, validate the complete persisted identity against the supplied identity; never reconstruct a digest from a subset.

In `run_gaussian_fixed_ray_diagnostic.py`, set the editable `COMPUTE["cpu_cuda_parity"]` default to `True`. `_require_cpu_only` rejects any final compute mapping that is not CPU, float64, device 0, deterministic, TF32-disabled, parity-enabled, and heavy-sweep-disabled. Then use this exact source-first order; there is no later config replacement:

```python
source_dir = _source_directory()
revision = _current_git_revision()
source_binding = ConfirmatorySourceBinding.from_path(
    source_dir / "source_binding.json",
    diagnostic_revision=revision,
)
source_digest = source_binding.canonical_source_binding_sha256
diagnostic_run = {
    **RUN,
    "name": f"{RUN['name']}-{source_digest}",
}
config = ExperimentConfig.from_dicts(
    diagnostic_run,
    THEORY,
    NUMERICS,
    OUTPUT,
    COMPUTE,
)
execution_identity = validate_fixed_ray_execution_identity(config, ROOT)
result = run_fixed_model_diagnostic(
    execution_identity,
    source_binding,
    source_dir,
)
```

The validator resolves the output root and configuration exactly once. `execution_identity.run_namespace` is the source-digest-bearing name above. The diagnostic body consumes `execution_identity.resolved_config` and the same `execution_identity.system`; it must not call `replace(config, ...)`, `_diagnostic_config`, `config_sha256`, or `build_preregistered_system`.

- [ ] **Step 6: Prove no production fixed-ray path rebuilds the system, run GREEN, and commit**

```powershell
rg -n "build_preregistered_system\(|_diagnostic_config\(" src/multiagent_elbo/realizations/gaussian run_gaussian_fixed_ray_diagnostic.py
if ($LASTEXITCODE -ne 0) { throw 'Task 5 static scan failed' }
C:\Python314\python.exe -B -m pytest tests\test_artifact_schema.py tests\test_gaussian_fixed_ray.py tests\test_gaussian_fixed_ray_diagnostics.py tests\test_gaussian_fixed_ray_diagnostic_experiment.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py tests\test_gaussian_confirmatory_analysis.py tests\test_gaussian_results_document.py tests\test_launchers.py -q -p no:cacheprovider --basetemp=.pytest-wave-c-task5-green
if ($LASTEXITCODE -ne 0) { throw 'Task 5 GREEN failed' }
C:\Python314\python.exe -m ruff check --no-cache src/multiagent_elbo/artifact_schema.py src/multiagent_elbo/artifacts.py src/multiagent_elbo/realizations/gaussian run_gaussian_fixed_ray_diagnostic.py tests/test_artifact_schema.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py tests/test_gaussian_fixed_ray_diagnostic_experiment.py tests/test_gaussian_results_document.py tests/test_launchers.py
if ($LASTEXITCODE -ne 0) { throw 'Task 5 lint failed' }
C:\Python314\python.exe -m ruff format --check --no-cache src/multiagent_elbo/artifact_schema.py src/multiagent_elbo/artifacts.py src/multiagent_elbo/realizations/gaussian run_gaussian_fixed_ray_diagnostic.py tests/test_artifact_schema.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py tests/test_gaussian_fixed_ray_diagnostic_experiment.py tests/test_gaussian_results_document.py tests/test_launchers.py
if ($LASTEXITCODE -ne 0) { throw 'Task 5 format check failed' }
git add -- src/multiagent_elbo/artifact_schema.py src/multiagent_elbo/artifacts.py src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostic_experiment.py src/multiagent_elbo/realizations/gaussian/__init__.py run_gaussian_fixed_ray_diagnostic.py tests/test_artifact_schema.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py tests/test_gaussian_fixed_ray_diagnostic_experiment.py tests/test_gaussian_results_document.py tests/test_launchers.py
if ($LASTEXITCODE -ne 0) { throw 'Task 5 staging failed' }
git commit -m "fix: version fixed-ray execution bindings"
if ($LASTEXITCODE -ne 0) { throw 'Task 5 commit failed' }
```

The `rg` result may contain the builder definition and the single call inside `validate_fixed_ray_execution_identity`; it must contain no `_diagnostic_config` match and no other production builder match.

---

### Task 6: Unify sentinel publication and discovery roots (`AUD-08`)

**Files:**

- Modify: `run_gaussian_fixed_ray_lab.py`
- Modify: `tests/test_launchers.py`
- Modify: `tests/test_gaussian_confirmatory_experiment.py`

**Exact discovery interface:**

```python
def _find_accepted_sentinel_run(
    manifest_sha256: str,
    *,
    sentinel_identity: FixedRayExecutionIdentity,
) -> Path:
    """Find one verified v3 sentinel only in its canonical namespace."""
```

The function searches only `sentinel_identity.canonical_output_root / sentinel_identity.run_namespace`, loads candidates through `load_verified_fixed_ray_bundle`, and requires manifest hash plus both identity digests. It never uses process CWD, launcher `ROOT / OUTPUT["root"]`, or a raw output string. A confirmatory identity may have a different run namespace and execution binding; acceptance requires equal scientific digest and a separately validated sentinel execution binding.

- [ ] **Step 1: Add an unmocked arbitrary-CWD and decoy RED test**

Add this test to `tests/test_launchers.py`:

```python
def fixed_ray_launcher_config(*, output_root: Path, run_name: str, backend: str, heavy_sweep_enabled: bool):
    return ExperimentConfig.from_dicts(
        {"name": run_name, "seed": 20260809},
        {
            "experiment": "gaussian_fixed_ray",
            "fixture": "gaussian_fixed_ray_v1",
            "preregistration": "2026-08-09-gaussian-fixed-ray-v1",
            "blocking_schemes": ["adjacent_pairs", "balanced_alternating"],
            "matrix_dimension": 2,
        },
        {
            "dtype": "float64",
            "atol": 1.0e-12,
            "rtol": 1.0e-10,
            "min_spd_rcond": 1.0e-12,
            "max_frame_condition": 1.0e6,
        },
        {
            "root": str(output_root),
            "collect_diagnostics": True,
            "render_figures": False,
        },
        {
            "backend": backend,
            "dtype": "float64",
            "device_index": 0,
            "batch_size": 4096,
            "deterministic": True,
            "allow_tf32": False,
            "cpu_cuda_parity": True,
            "cuda_worker_python": r"C:\anaconda\python.exe",
            "heavy_sweep_enabled": heavy_sweep_enabled,
        },
    )


def publish_schema_valid_fake_sentinel(identity):
    streams = RngStreams.from_seed(identity.resolved_config.run.seed)
    provenance = collect_provenance(
        ROOT,
        ROOT / "Theory",
        identity.config_identity,
        streams,
        excluded_output_roots=(identity.canonical_output_root,),
    )
    payloads = RunPayloads(
        artifact_kind="gaussian_fixed_ray_cuda_sentinel",
        json_payloads={
            "sentinel_parity.json": {
                "schema_version": "gaussian-fixed-ray-cuda-sentinel-v2",
                "scientific_system_digest": identity.scientific_system_digest,
                "execution_binding_digest": identity.execution_binding_digest,
                "verification_state": "CANDIDATE",
                "sentinel_job_ids": [],
                "step_records": [],
                "endpoint_records": [],
                "worker_jobs": [],
            }
        },
        npz_payloads={
            "sentinel_arrays.npz": {
                "fixture": NpzArrayInput(np.ones((1, 1), dtype=np.float64), "finite")
            }
        },
    )
    prepared = prepare_fixed_ray_run_bundle(
        identity.resolved_config,
        provenance,
        payloads,
        scientific_system_digest=identity.scientific_system_digest,
        execution_binding_digest=identity.execution_binding_digest,
    )
    return publish_run_bundle(prepared).run_dir


def test_sentinel_publication_and_discovery_share_identity_root(tmp_path, monkeypatch):
    external_root = tmp_path / "external-output"
    unrelated_cwd = tmp_path / "unrelated-cwd"
    unrelated_cwd.mkdir()
    sentinel_config = fixed_ray_launcher_config(
        output_root=external_root,
        run_name="sentinel-bound-run",
        backend="cuda",
        heavy_sweep_enabled=False,
    )
    sentinel_identity = validate_fixed_ray_execution_identity(sentinel_config, ROOT)
    run_dir = publish_schema_valid_fake_sentinel(sentinel_identity)
    manifest_sha256 = hashlib.sha256((run_dir / "manifest.json").read_bytes()).hexdigest()

    fake_repo_root = tmp_path / "fake-repository"
    fake_repo_root.mkdir()
    launcher.ROOT = fake_repo_root
    launcher.OUTPUT = {**launcher.OUTPUT, "root": "artifacts"}
    decoy = fake_repo_root / "artifacts" / sentinel_identity.run_namespace
    decoy.mkdir(parents=True)
    (decoy / "manifest.json").write_bytes((run_dir / "manifest.json").read_bytes())

    monkeypatch.chdir(unrelated_cwd)
    found = launcher._find_accepted_sentinel_run(
        manifest_sha256,
        sentinel_identity=sentinel_identity,
    )
    assert found == run_dir
    assert decoy not in found.parents
```

Do not mock the resolver, preparer, publisher, loader, or finder.

- [ ] **Step 2: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_launchers.py tests\test_gaussian_confirmatory_experiment.py -k "sentinel_publication_and_discovery or arbitrary_cwd or decoy" -q -p no:cacheprovider --basetemp=.pytest-wave-c-task6-red
$redExit = $LASTEXITCODE
if ($redExit -eq 0) { throw 'Task 6 RED unexpectedly passed' }
```

Expected: FAIL because the finder reconstructs `ROOT / OUTPUT["root"]` and cannot discover an externally rooted v3 sentinel from an unrelated CWD.

- [ ] **Step 3: Implement identity-rooted discovery and launcher wiring**

Use:

```python
namespace = sentinel_identity.canonical_output_root / sentinel_identity.run_namespace
matches: list[Path] = []
if namespace.is_dir():
    for manifest_path in sorted(namespace.glob("*/manifest.json")):
        manifest_bytes = manifest_path.read_bytes()
        if hashlib.sha256(manifest_bytes).hexdigest() != manifest_sha256:
            continue
        bundle = load_verified_fixed_ray_bundle(
            manifest_path.parent,
            expected_scientific_system_digest=sentinel_identity.scientific_system_digest,
            expected_execution_binding_digest=sentinel_identity.execution_binding_digest,
        )
        if bundle.scientific_system_digest != sentinel_identity.scientific_system_digest:
            continue
        if bundle.execution_binding_digest != sentinel_identity.execution_binding_digest:
            continue
        matches.append(manifest_path.parent)
if len(matches) != 1:
    raise ValueError("accepted sentinel manifest must resolve to exactly one bound run")
return matches[0]
```

In confirmatory mode, validate `sentinel_identity.scientific_system_digest == confirmatory_identity.scientific_system_digest`; require inequality of execution bindings when the namespaces differ; pass the sentinel identity to discovery and the confirmatory identity to confirmatory execution.

- [ ] **Step 4: Run GREEN and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_launchers.py tests\test_gaussian_confirmatory_experiment.py tests\test_artifact_schema.py -q -p no:cacheprovider --basetemp=.pytest-wave-c-task6-green
if ($LASTEXITCODE -ne 0) { throw 'Task 6 GREEN failed' }
git add -- run_gaussian_fixed_ray_lab.py tests/test_launchers.py tests/test_gaussian_confirmatory_experiment.py
if ($LASTEXITCODE -ne 0) { throw 'Task 6 staging failed' }
git commit -m "fix: unify sentinel publication discovery root"
if ($LASTEXITCODE -ne 0) { throw 'Task 6 commit failed' }
```

---

### Task 7: Reject inert scale-cocycle options and preserve nine payloads (`AUD-09`)

**Files:**

- Modify: `src/multiagent_elbo/config.py`
- Modify: `src/multiagent_elbo/finite/scale_cocycle_experiment.py`
- Modify: `run_scale_cocycle_lab.py`
- Modify: `tests/test_config.py`
- Modify: `tests/test_scale_cocycle.py`
- Modify: `tests/test_scale_cocycle_experiment.py`
- Modify: `tests/test_launchers.py`

**Exact interface and inventory:**

```python
SCALE_COCYCLE_SEMANTIC_PAYLOADS = (
    "arrays.npz",
    "coarse_actions.json",
    "comparison_isomorphisms.json",
    "composed_channels.json",
    "derivative_cocycle.json",
    "metrics.json",
    "posterior_bridges.json",
    "retained_projection_residual.json",
    "three_level_extension.json",
)


def validate_scale_cocycle_options(config: ExperimentConfig) -> None:
    if config.theory.experiment != "scale_cocycle":
        raise ValueError("scale-cocycle options require theory.experiment='scale_cocycle'")
    if config.theory.retained_interaction_order != 2:
        raise ValueError("retained_interaction_order must be 2")
    if config.output.collect_diagnostics is not True:
        raise ValueError("collect_diagnostics must be True")
```

Wave A's Fisher witness is nested at `derivative_cocycle["fisher_cocycle_witness"]` under schema `scale-cocycle-derivative-v2`. The nested record has schema `scale-fisher-cocycle-witness-v1`, and the `base_fisher_cocycle_forms_residual` metric interpretation names the exact anchor `derivative_cocycle.json#fisher_cocycle_witness`. Neither the producer nor manifest contains `fisher_cocycle_witness.json`.

- [ ] **Step 1: Add zero-effect option RED tests**

Add this test to `tests/test_scale_cocycle_experiment.py`:

```python
@pytest.mark.parametrize(
    "mutate, message",
    [
        (
            lambda c: replace(c, theory=replace(c.theory, retained_interaction_order=1)),
            "retained_interaction_order must be 2",
        ),
        (
            lambda c: replace(c, theory=replace(c.theory, retained_interaction_order=3)),
            "retained_interaction_order must be 2",
        ),
        (
            lambda c: replace(c, output=replace(c.output, collect_diagnostics=False)),
            "collect_diagnostics must be True",
        ),
    ],
)
def test_unsupported_scale_options_fail_before_effects(tmp_path, monkeypatch, mutate, message):
    config = mutate(scale_config(tmp_path / "out"))
    monkeypatch.setattr(module.RngStreams, "from_seed", lambda seed: pytest.fail("RNG"))
    monkeypatch.setattr(module, "_exact_fixtures", lambda *args: pytest.fail("fixture construction"))
    monkeypatch.setattr(module, "prepare_run_bundle", lambda *args: pytest.fail("bundle preparation"))
    monkeypatch.setattr(module, "publish_run_bundle", lambda *args: pytest.fail("publication"))
    with pytest.raises(ValueError, match=message):
        run_scale_cocycle_experiment(config)
    assert not (tmp_path / "out").exists()
```

- [ ] **Step 2: Add the accepted inventory and nested-witness RED test**

```python
def test_supported_scale_run_has_exact_nine_semantic_payloads_and_nested_witness(tmp_path):
    result = run_scale_cocycle_experiment(scale_config(tmp_path / "out"))
    bundle = load_verified_run_bundle(result.run_dir)
    semantic_names = tuple(
        item.name
        for item in bundle.inventory
        if item.name not in {"config.json", "provenance.json"}
    )
    assert len(semantic_names) == 9
    assert semantic_names == tuple(
        sorted(semantic_names, key=lambda name: name.encode("ascii"))
    )
    assert semantic_names == SCALE_COCYCLE_SEMANTIC_PAYLOADS
    assert len(set(semantic_names)) == 9
    assert "fisher_cocycle_witness.json" not in {
        item.name for item in bundle.inventory
    }
    derivative = bundle.json_payloads["derivative_cocycle.json"]
    assert derivative["schema_version"] == "scale-cocycle-derivative-v2"
    assert set(derivative["fisher_cocycle_witness"]) == {
        "schema_version", "provenance", "probability", "scores", "channel",
        "fine_fisher", "coarse_fisher", "conditional_covariance",
        "decomposition_residual",
    }
    assert derivative["fisher_cocycle_witness"]["schema_version"] == "scale-fisher-cocycle-witness-v1"
    metric = result.metrics["base_fisher_cocycle_forms_residual"]
    assert "derivative_cocycle.json#fisher_cocycle_witness" in metric.interpretation
```

- [ ] **Step 3: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_config.py tests\test_scale_cocycle.py tests\test_scale_cocycle_experiment.py tests\test_launchers.py -k "unsupported_scale or exact_nine or nested_witness" -q -p no:cacheprovider --basetemp=.pytest-wave-c-task7-red
$redExit = $LASTEXITCODE
if ($redExit -eq 0) { throw 'Task 7 RED unexpectedly passed' }
```

Expected: FAIL because unsupported values are accepted into execution identity and the Wave A witness/inventory boundary is not yet enforced at publication.

- [ ] **Step 4: Call the shared validator before every effect**

The first executable line after type validation in `run_scale_cocycle_experiment` is `validate_scale_cocycle_options(config)`. The launcher calls it immediately after `ExperimentConfig.from_dicts` and before resolving an output root. Preserve Wave A's exact derivative record: `semantic_artifacts["derivative_cocycle"]["schema_version"] == "scale-cocycle-derivative-v2"`, its nested key is exactly `fisher_cocycle_witness`, and `metrics["base_fisher_cocycle_forms_residual"].interpretation` names `derivative_cocycle.json#fisher_cocycle_witness`. Do not accept an alias or silently version either name. Construct `RunPayloads` with exactly these mappings:

```python
payloads = RunPayloads(
    artifact_kind="scale_cocycle",
    json_payloads={
        "coarse_actions.json": semantic_artifacts["coarse_actions"],
        "comparison_isomorphisms.json": semantic_artifacts["comparison_isomorphisms"],
        "composed_channels.json": semantic_artifacts["composed_channels"],
        "derivative_cocycle.json": semantic_artifacts["derivative_cocycle"],
        "metrics.json": {name: asdict(metrics[name]) for name in sorted(metrics)},
        "posterior_bridges.json": semantic_artifacts["posterior_bridges"],
        "retained_projection_residual.json": semantic_artifacts["retained_projection_residual"],
        "three_level_extension.json": extension,
    },
    npz_payloads={
        "arrays.npz": {
            name: NpzArrayInput(arrays[name], "finite") for name in sorted(arrays)
        }
    },
)

semantic_names = tuple(
    sorted(
        (*payloads.json_payloads, *payloads.npz_payloads),
        key=lambda name: name.encode("ascii"),
    )
)
if semantic_names != SCALE_COCYCLE_SEMANTIC_PAYLOADS or len(semantic_names) != 9:
    raise ValueError("scale-cocycle semantic payload inventory must be exactly nine")
```

`SCALE_COCYCLE_SEMANTIC_PAYLOADS` is the canonical ASCII-sorted inventory used by both producer and test. The producer rejects any missing, duplicate, reordered, or tenth semantic payload before bundle preparation; manifest/config/provenance bytes are not semantic payloads.

- [ ] **Step 5: Run GREEN, static checks, and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_config.py tests\test_scale_cocycle.py tests\test_scale_cocycle_experiment.py tests\test_launchers.py -q -p no:cacheprovider --basetemp=.pytest-wave-c-task7-green
if ($LASTEXITCODE -ne 0) { throw 'Task 7 GREEN failed' }
C:\Python314\python.exe -m ruff check --no-cache src/multiagent_elbo/config.py src/multiagent_elbo/finite/scale_cocycle_experiment.py run_scale_cocycle_lab.py tests/test_config.py tests/test_scale_cocycle.py tests/test_scale_cocycle_experiment.py tests/test_launchers.py
if ($LASTEXITCODE -ne 0) { throw 'Task 7 lint failed' }
C:\Python314\python.exe -m ruff format --check --no-cache src/multiagent_elbo/config.py src/multiagent_elbo/finite/scale_cocycle_experiment.py run_scale_cocycle_lab.py tests/test_config.py tests/test_scale_cocycle.py tests/test_scale_cocycle_experiment.py tests/test_launchers.py
if ($LASTEXITCODE -ne 0) { throw 'Task 7 format check failed' }
git add -- src/multiagent_elbo/config.py src/multiagent_elbo/finite/scale_cocycle_experiment.py run_scale_cocycle_lab.py tests/test_config.py tests/test_scale_cocycle.py tests/test_scale_cocycle_experiment.py tests/test_launchers.py
if ($LASTEXITCODE -ne 0) { throw 'Task 7 staging failed' }
git commit -m "fix: reject inert scale-cocycle options"
if ($LASTEXITCODE -ne 0) { throw 'Task 7 commit failed' }
```

---

### Task 8: Build the Wave C adapter on the frozen Wave 0 evidence lifecycle

**Files:**

- Create: `tools/build_wave_c_evidence.py`
- Create: `tests/test_wave_c_evidence.py`

**Frozen lifecycle boundary:**

- The Wave 0 generic runner is the only process/JUnit/environment collector. Every evidence suite is invoked through `tools/remediation_evidence.py run-junit --record $recordPath --junit $junitPath -- $pythonAndPytestArgv`.
- Candidate raw bytes exist only below `.verification/raw/wave-c/$implementationShort/candidate/`; closure raw bytes exist only below `.verification/raw/wave-c/$evidenceShort/closure/`. Both locations are ignored. Raw JUnit, basetemps, command records, private host values, reviews, CUDA gates, and sentinel source artifacts are never committed.
- `build --stage {candidate,closure}` calls the generic immutable `prepare_evidence_bundle`, prepares the Wave C domain files in memory, validates the complete virtual union, and calls `publish_evidence_bundle` exactly once into an absent final directory. No final-directory candidate or closure byte is written before that sole publish call.
- `wave-c-domain-evidence-v1` points one way to the already-prepared generic `index.json` by path, size, and SHA-256. It inventories every public Wave C domain byte except itself. The generic index does not point back to the domain index, so there is no hash cycle.
- Candidate polarity is exactly `tested_git_head=P`, `implementation_parent_git_head=P`. Closure polarity is exactly `tested_git_head=E`, `implementation_parent_git_head=P`, where `E^ == P` and `P..E` contains only the committed candidate bundle.
- `validate-domain` revalidates the generic index, the domain index, exact allowed path set, privacy transform, current `HEAD`, heads/stage, and every byte. `populate-ledger` accepts only the installed gate's empty closure template, then live-revalidates both indexes and the complete union before replacing that template.
- CUDA is not an implementation prerequisite. The default exact-`E` branch records a current `INCONCLUSIVE` obligation without importing Torch or inspecting the GPU. A sentinel branch exists only after a separately presented and accepted fresh gate. It runs the five-job sentinel and never the confirmatory or heavy sweep. A passing sentinel can close only the sentinel-protocol currentness claim.

Use these exact production constants:

```python
from pathlib import Path

CPU_PYTHON = Path(r"C:\Python314\python.exe")
WAVE = "wave-c"
VERIFICATION_ROOT = Path(
    r"C:\Users\chris and christine\.codex\skills\verification"
)
VERIFICATION_SNAPSHOT = Path(
    "docs/verification/remediation/verification-contract-v1.json"
)
WAVE0_REVIEWED_PLAN = Path(
    "docs/superpowers/plans/"
    "2026-08-11-scientific-integrity-remediation-wave-0.md"
)
WAVE0_REVIEWED_PLAN_SHA256 = (
    "dbe2263a3b0fe1e9f5db4ff1fca9a19"
    "f819cfd32ef38da71d6e5cb5485723ac2"
)
WAVE_A_OWNERSHIP_PLAN = Path(
    "docs/superpowers/plans/"
    "2026-08-11-scientific-integrity-remediation-wave-a.md"
)
WAVE_C_REVIEWED_PLAN = Path(
    "docs/superpowers/plans/"
    "2026-08-11-scientific-integrity-remediation-wave-c.md"
)
WAVE0_TERMINAL_INPUT_ROOT = Path(".verification/dependencies/wave-0")
WAVE0_TERMINAL_LEDGER = WAVE0_TERMINAL_INPUT_ROOT / "final-ledger.json"
WAVE0_TERMINAL_CLOSURE = WAVE0_TERMINAL_INPUT_ROOT / "closure"
WAVE0_TERMINAL_INDEX = WAVE0_TERMINAL_CLOSURE / "index.json"

TARGETED_TESTS = (
    "tests/test_artifact_schema.py",
    "tests/test_config.py",
    "tests/test_cuda_backend.py",
    "tests/test_experiment_support.py",
    "tests/test_gaussian_fixed_ray.py",
    "tests/test_gaussian_fixed_ray_diagnostics.py",
    "tests/test_gaussian_fixed_ray_diagnostic_experiment.py",
    "tests/test_gaussian_fixed_ray_experiment.py",
    "tests/test_gaussian_confirmatory_experiment.py",
    "tests/test_gaussian_results_document.py",
    "tests/test_launchers.py",
    "tests/test_scale_cocycle.py",
    "tests/test_scale_cocycle_experiment.py",
)

SUBSYSTEM_TESTS = TARGETED_TESTS + (
    "tests/test_artifacts.py",
    "tests/test_runtime.py",
    "tests/test_output_paths.py",
    "tests/test_gaussian_confirmatory_analysis.py",
    "tests/test_shared_scientific_contracts.py",
)

EXPECTED_CPU_ENVIRONMENT = {
    "CUDA_VISIBLE_DEVICES": "-1",
    "MULTIAGENTELBO_RUN_CUDA_TESTS": None,
    "VFE3_TEST_DEVICE": None,
    "CUBLAS_WORKSPACE_CONFIG": None,
    "PYTHONHASHSEED": "0",
    "PYTHONPATH": None,
}

SYMLINK_SKIP = (
    "tests.test_experiment_support::"
    "test_validated_renderer_status_rejects_a_publication_symlink_escape"
)
CUDA_SKIP = (
    "tests.test_cuda_backend::"
    "test_pinned_cuda_worker_runs_first_job_with_determinism_environment"
)
ARTIFACT_CAPABILITY_SKIPS = {
    "tests.test_artifacts::test_finalize_rejects_a_declared_symlink":
        "capability unavailable: symbolic_link",
    "tests.test_artifacts::test_finalize_rejects_a_declared_file_with_an_external_hard_link":
        "capability unavailable: hard_link",
    "tests.test_artifacts::test_finalize_rejects_an_external_hard_link_to_core_config":
        "capability unavailable: hard_link",
    "tests.test_artifacts::test_finalize_rejects_duplicate_file_identity_within_inventory":
        "capability unavailable: hard_link",
}
SKIP_ALLOWLIST_BY_SUITE = {
    "targeted": {
        SYMLINK_SKIP: "capability unavailable: symbolic_link",
        CUDA_SKIP: "requires explicit dedicated CUDA-lane opt-in",
    },
    "subsystem": {
        **ARTIFACT_CAPABILITY_SKIPS,
        SYMLINK_SKIP: "capability unavailable: symbolic_link",
        CUDA_SKIP: "requires explicit dedicated CUDA-lane opt-in",
    },
    "full": {
        **ARTIFACT_CAPABILITY_SKIPS,
        SYMLINK_SKIP: "capability unavailable: symbolic_link",
        CUDA_SKIP: "requires explicit dedicated CUDA-lane opt-in",
    },
}

WAVE_C_TESTED_INPUT_POLICY = {
    "schema_version": "wave-c-source-config-theory-tools-tests-v1",
    "selection_rules": (
        "prefix:src/",
        "prefix:tests/",
        "prefix:Theory/",
        "prefix:tools/",
        "prefix:configs/",
        "top_level_suffix:.py",
        "exact:pyproject.toml",
        "exact:.gitignore",
        "exact:.gitattributes",
        "exact:environments/cuda-rtx5090-cu128.lock.txt",
        "exact:docs/audits/2026-08-11-post-fixed-ray-deep-audit.md",
        "exact:docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md",
        "exact:docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-a.md",
        "exact:docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-c.md",
        "exact:docs/superpowers/specs/2026-08-11-scientific-integrity-remediation-program-design.md",
        "exact:docs/verification/remediation/verification-contract-v1.json",
        "prefix:docs/verification/remediation/",
    ),
    "exclusion_rules": (
        "prefix:docs/verification/evidence/",
        "prefix:verification-evidence/",
        "prefix:.verification/",
        "prefix:.pytest_cache/",
        "prefix:.pytest-",
    ),
}

WAVE_C_DEPENDENCY_INPUTS = (
    "pyproject.toml",
    "environments/cuda-rtx5090-cu128.lock.txt",
    "docs/verification/remediation/verification-contract-v1.json",
)

WAVE_C_REQUIRED_SOURCE_CONFIG_BINDINGS = (
    ".gitattributes",
    ".gitignore",
    "docs/audits/2026-08-11-post-fixed-ray-deep-audit.md",
    "docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md",
    "docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-a.md",
    "docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-c.md",
    "docs/superpowers/specs/2026-08-11-scientific-integrity-remediation-program-design.md",
    "docs/verification/remediation/verification-contract-v1.json",
    "environments/cuda-rtx5090-cu128.lock.txt",
    "pyproject.toml",
    "run_gaussian_fixed_ray_diagnostic.py",
    "run_gaussian_fixed_ray_lab.py",
    "run_scale_cocycle_lab.py",
    "src/multiagent_elbo/artifact_schema.py",
    "src/multiagent_elbo/artifacts.py",
    "src/multiagent_elbo/conditioning.py",
    "src/multiagent_elbo/config.py",
    "src/multiagent_elbo/cuda_backend.py",
    "src/multiagent_elbo/experiment_support.py",
    "src/multiagent_elbo/finite/scale_cocycle_experiment.py",
    "src/multiagent_elbo/output_paths.py",
    "src/multiagent_elbo/realizations/gaussian/__init__.py",
    "src/multiagent_elbo/realizations/gaussian/fixed_ray.py",
    "src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostic_experiment.py",
    "src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py",
    "src/multiagent_elbo/runtime.py",
    "tests/test_artifact_schema.py",
    "tests/test_artifacts.py",
    "tests/test_config.py",
    "tests/test_cuda_backend.py",
    "tests/test_experiment_support.py",
    "tests/test_gaussian_confirmatory_analysis.py",
    "tests/test_gaussian_confirmatory_experiment.py",
    "tests/test_gaussian_fixed_ray.py",
    "tests/test_gaussian_fixed_ray_diagnostic_experiment.py",
    "tests/test_gaussian_fixed_ray_diagnostics.py",
    "tests/test_gaussian_fixed_ray_experiment.py",
    "tests/test_gaussian_results_document.py",
    "tests/test_launchers.py",
    "tests/test_output_paths.py",
    "tests/test_remediation_evidence.py",
    "tests/test_runtime.py",
    "tests/test_scale_cocycle.py",
    "tests/test_scale_cocycle_experiment.py",
    "tests/test_shared_scientific_contracts.py",
    "tests/test_wave_c_evidence.py",
    "tools/build_wave_c_evidence.py",
    "tools/cuda_worker.py",
    "tools/remediation_evidence.py",
)

# Add every tracked regular file below docs/verification/remediation/ in sorted
# repository-relative order. Reject missing, extra, case-aliased, untracked,
# symlink, or reparse matches before bundle preparation.

INITIAL_REVIEW_PATHS = (
    "views/artifact-protocol.json",
    "views/code-runtime.json",
)
TARGET4_ADDITIONAL_REVIEW_PATHS = (
    "views/failure-ordering.json",
    "views/identity-boundary.json",
)
AUD_06_SKEPTIC_PATHS = (
    "views/skeptics/AUD-06-CORRECTED-GUARD.json",
    "views/skeptics/AUD-06-DEFECT-REPRODUCTION.json",
)
TARGET8_ADDITIONAL_REVIEW_PATHS = (
    "views/escalation/configuration-boundary.json",
    "views/escalation/digest-preimage.json",
    "views/escalation/protocol-adversary.json",
    "views/escalation/publication-root.json",
)
REVIEW_PATHS_BY_TARGET = {
    2: INITIAL_REVIEW_PATHS,
    4: INITIAL_REVIEW_PATHS + TARGET4_ADDITIONAL_REVIEW_PATHS,
    8: (
        INITIAL_REVIEW_PATHS
        + TARGET4_ADDITIONAL_REVIEW_PATHS
        + TARGET8_ADDITIONAL_REVIEW_PATHS
    ),
}
VIEW_IDS_BY_TARGET = {
    target: tuple(Path(path).stem for path in paths)
    for target, paths in REVIEW_PATHS_BY_TARGET.items()
}
ALLOWED_ESCALATION_TRIGGERS = (
    "criterion_disagreement",
    "high_dispersion",
    "high_severity",
    "small_margin",
)
AUD_06_INITIAL_ESCALATION_TRIGGERS = ("high_severity",)
AUD_06_DISAGREEMENT_ESCALATION_TRIGGERS = (
    "criterion_disagreement",
    "high_severity",
)
CONDITIONAL_VIEW_IDS = VIEW_IDS_BY_TARGET[2]

CLAIM_CRITERIA_BY_DOMAIN = {
    "code": (
        ("execution", "execution"),
        ("input_output_behavior", "input/output behavior"),
        ("boundary_failure_behavior", "boundary/failure behavior"),
        ("regression_coverage", "regression coverage"),
        ("configuration_reachability", "configuration reachability"),
        ("reproducibility", "reproducibility"),
    ),
    "experiment": (
        ("hypothesis_endpoint_definition", "hypothesis/endpoint definition"),
        ("protocol_fidelity", "protocol fidelity"),
        ("data_provenance", "data provenance"),
        ("configuration_identity", "configuration identity"),
        ("seed_split_control", "seed/split control"),
        ("statistical_treatment", "statistical treatment"),
        ("reproduced_output_agreement", "reproduced-output agreement"),
        ("robustness", "robustness"),
        ("alternative_explanations", "alternative explanations"),
    ),
}

AUDIT_CLAIM_IDS = tuple(
    f"AUD-{number:02d}-{suffix}"
    for number in (6, 7, 8, 9, 19)
    for suffix in ("DEFECT-REPRODUCTION", "CORRECTED-GUARD")
)
CONDITIONAL_CLAIM_IDS = (
    "WAVE-C-CUDA-SENTINEL-PROTOCOL-CURRENTNESS",
    "WAVE-C-CONFIRMATORY-EQUIVALENCE",
    "WAVE-C-ATTRACTION",
    "WAVE-C-UNIVERSALITY",
)
ALL_CLAIM_IDS = AUDIT_CLAIM_IDS + CONDITIONAL_CLAIM_IDS
ADJUDICATOR_PATHS = tuple(
    sorted(
        (f"views/adjudicators/{claim_id}.json" for claim_id in ALL_CLAIM_IDS),
        key=lambda path: path.encode("ascii"),
    )
)

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
CANDIDATE_DOMAIN_PATHS = (
    "claim-contracts.json",
    "domain-evidence.json",
    "domain-privacy-transform.json",
    "wave0-terminal-binding.json",
)
NO_CUDA_DOMAIN_PATHS = ("cuda-open-obligation.json",)
SENTINEL_DOMAIN_PATHS = (
    "cuda-sentinel/command-record.json",
    "cuda-sentinel/gate.json",
    "cuda-sentinel/manifest.json",
    "cuda-sentinel/metrics.json",
    "cuda-sentinel/semantic-array-hashes.json",
    "cuda-sentinel/worker-exchange-index.json",
)
CANDIDATE_PUBLIC_PATHS = tuple(
    sorted(
        GENERIC_PUBLIC_PATHS + CANDIDATE_DOMAIN_PATHS,
        key=lambda path: path.encode("ascii"),
    )
)
CLOSURE_PUBLIC_PATHS_BY_BRANCH_AND_TARGET = {
    (branch, target): tuple(
        sorted(
            (
                GENERIC_PUBLIC_PATHS
                + CANDIDATE_DOMAIN_PATHS
                + REVIEW_PATHS_BY_TARGET[target]
                + AUD_06_SKEPTIC_PATHS
                + ADJUDICATOR_PATHS
                + (
                    NO_CUDA_DOMAIN_PATHS
                    if branch == "no-cuda"
                    else SENTINEL_DOMAIN_PATHS
                )
            ),
            key=lambda path: path.encode("ascii"),
        )
    )
    for branch in ("no-cuda", "sentinel")
    for target in (4, 8)
}
```

`uv.lock` is protected live-checkout WIP only. It is neither a tested-input policy member nor a dependency input for isolated Wave C evidence.

`GENERIC_PUBLIC_PATHS` is byte-for-byte the final Wave 0 eleven-file base
contract. Wave C never removes, renames, regenerates, or adds a twelfth generic
file. The domain privacy map uses the distinct
`domain-privacy-transform.json` path, so it cannot collide with Wave 0's base
`privacy-transform.json`. The exact union cardinalities are 15 for candidate;
36/40 for no-CUDA target 4/8; and 41/45 for sentinel target 4/8.

Define exactly 14 claim specifications. The ten audit propositions have the same state in both CUDA branches; the sentinel claim is conditional; the last three claims are always open:

```python
CLAIM_SPECS = (
    {"id":"AUD-06-DEFECT-REPRODUCTION","domain":"code","severity":"high","no_cuda_state":"REFUTED","sentinel_state":"REFUTED","kind":"mechanical","statement":"The unsupported-setting, multiple-system, or digest-domain AUD-06 defect still reproduces at this artifact revision."},
    {"id":"AUD-06-CORRECTED-GUARD","domain":"code","severity":"high","no_cuda_state":"EVIDENCE_VERIFIED","sentinel_state":"EVIDENCE_VERIFIED","kind":"mechanical","statement":"One validated 2x2 system identity fails before effects and carries the frozen scientific and execution digests at this artifact revision."},
    {"id":"AUD-07-DEFECT-REPRODUCTION","domain":"code","severity":"medium","no_cuda_state":"REFUTED","sentinel_state":"REFUTED","kind":"mechanical","statement":"The open or requested-only CUDA worker protocol defect still reproduces at this artifact revision."},
    {"id":"AUD-07-CORRECTED-GUARD","domain":"code","severity":"medium","no_cuda_state":"EVIDENCE_VERIFIED","sentinel_state":"EVIDENCE_VERIFIED","kind":"mechanical","statement":"Protocol v3 rejects unknown fields, requested-observed divergence, and legacy promotion before eligibility at this artifact revision."},
    {"id":"AUD-08-DEFECT-REPRODUCTION","domain":"code","severity":"medium","no_cuda_state":"REFUTED","sentinel_state":"REFUTED","kind":"mechanical","statement":"The split publication-discovery-root AUD-08 defect still reproduces at this artifact revision."},
    {"id":"AUD-08-CORRECTED-GUARD","domain":"code","severity":"medium","no_cuda_state":"EVIDENCE_VERIFIED","sentinel_state":"EVIDENCE_VERIFIED","kind":"mechanical","statement":"Fixed-ray publication and discovery use the one resolved identity root and reject old-root decoys at this artifact revision."},
    {"id":"AUD-09-DEFECT-REPRODUCTION","domain":"code","severity":"medium","no_cuda_state":"REFUTED","sentinel_state":"REFUTED","kind":"mechanical","statement":"An inert scale-cocycle option or a tenth semantic payload still escapes at this artifact revision."},
    {"id":"AUD-09-CORRECTED-GUARD","domain":"code","severity":"medium","no_cuda_state":"EVIDENCE_VERIFIED","sentinel_state":"EVIDENCE_VERIFIED","kind":"mechanical","statement":"Unsupported scale-cocycle options fail before effects and the semantic inventory remains exactly nine payloads at this artifact revision."},
    {"id":"AUD-19-DEFECT-REPRODUCTION","domain":"code","severity":"medium","no_cuda_state":"REFUTED","sentinel_state":"REFUTED","kind":"mechanical","statement":"The permissive matrix-domain AUD-19 defect still reproduces at this artifact revision."},
    {"id":"AUD-19-CORRECTED-GUARD","domain":"code","severity":"medium","no_cuda_state":"EVIDENCE_VERIFIED","sentinel_state":"EVIDENCE_VERIFIED","kind":"mechanical","statement":"The required matrix policy rejects invalid inputs and returns bytes-backed system arrays at this artifact revision."},
    {"id":"WAVE-C-CUDA-SENTINEL-PROTOCOL-CURRENTNESS","domain":"experiment","severity":"medium","no_cuda_state":"INCONCLUSIVE","sentinel_state":"EVIDENCE_VERIFIED","kind":"reproduced_output","statement":"The accepted exact-revision five-job CUDA sentinel satisfies only its frozen protocol, identity, parity, and decision controls."},
    {"id":"WAVE-C-CONFIRMATORY-EQUIVALENCE","domain":"experiment","severity":"medium","no_cuda_state":"INCONCLUSIVE","sentinel_state":"INCONCLUSIVE","kind":"reproduced_output","statement":"CPU and CUDA confirmatory executions are equivalent at this artifact revision."},
    {"id":"WAVE-C-ATTRACTION","domain":"experiment","severity":"medium","no_cuda_state":"INCONCLUSIVE","sentinel_state":"INCONCLUSIVE","kind":"reproduced_output","statement":"The fixed-ray system establishes the preregistered attraction claim at this artifact revision."},
    {"id":"WAVE-C-UNIVERSALITY","domain":"experiment","severity":"medium","no_cuda_state":"INCONCLUSIVE","sentinel_state":"INCONCLUSIVE","kind":"reproduced_output","statement":"The observed fixed-ray behavior establishes a universality claim at this artifact revision."},
)

STATE_TO_ADJUDICATOR_RESULT = {
    "EVIDENCE_VERIFIED": "support",
    "REFUTED": "refute",
    "INCONCLUSIVE": "abstain",
}

AUDIT_EVIDENCE_SPECS = {
    "AUD-06-DEFECT-REPRODUCTION": (
        {"id":"aud-06-defect-current-counterevidence","kind":"mechanical",
         "relative_location":"targeted.xml","supports":False},
    ),
    "AUD-06-CORRECTED-GUARD": (
        {"id":"aud-06-guard-current-evidence","kind":"mechanical",
         "relative_location":"targeted.xml","supports":True},
    ),
    "AUD-07-DEFECT-REPRODUCTION": (
        {"id":"aud-07-defect-current-counterevidence","kind":"mechanical",
         "relative_location":"targeted.xml","supports":False},
    ),
    "AUD-07-CORRECTED-GUARD": (
        {"id":"aud-07-guard-current-evidence","kind":"mechanical",
         "relative_location":"targeted.xml","supports":True},
    ),
    "AUD-08-DEFECT-REPRODUCTION": (
        {"id":"aud-08-defect-current-counterevidence","kind":"mechanical",
         "relative_location":"targeted.xml","supports":False},
    ),
    "AUD-08-CORRECTED-GUARD": (
        {"id":"aud-08-guard-current-evidence","kind":"mechanical",
         "relative_location":"targeted.xml","supports":True},
    ),
    "AUD-09-DEFECT-REPRODUCTION": (
        {"id":"aud-09-defect-current-counterevidence","kind":"mechanical",
         "relative_location":"targeted.xml","supports":False},
    ),
    "AUD-09-CORRECTED-GUARD": (
        {"id":"aud-09-guard-current-evidence","kind":"mechanical",
         "relative_location":"targeted.xml","supports":True},
    ),
    "AUD-19-DEFECT-REPRODUCTION": (
        {"id":"aud-19-defect-current-counterevidence","kind":"mechanical",
         "relative_location":"targeted.xml","supports":False},
    ),
    "AUD-19-CORRECTED-GUARD": (
        {"id":"aud-19-guard-current-evidence","kind":"mechanical",
         "relative_location":"targeted.xml","supports":True},
    ),
}

EVIDENCE_SPECS_BY_CLAIM_AND_BRANCH = {
    **{
        (claim_id, branch): records
        for claim_id, records in AUDIT_EVIDENCE_SPECS.items()
        for branch in ("no-cuda", "sentinel")
    },
    ("WAVE-C-CUDA-SENTINEL-PROTOCOL-CURRENTNESS", "no-cuda"): (),
    ("WAVE-C-CUDA-SENTINEL-PROTOCOL-CURRENTNESS", "sentinel"): (
        {"id":"wave-c-sentinel-current-reproduced-output",
         "kind":"reproduced_output",
         "relative_location":"cuda-sentinel/manifest.json","supports":True},
    ),
    ("WAVE-C-CONFIRMATORY-EQUIVALENCE", "no-cuda"): (),
    ("WAVE-C-CONFIRMATORY-EQUIVALENCE", "sentinel"): (),
    ("WAVE-C-ATTRACTION", "no-cuda"): (),
    ("WAVE-C-ATTRACTION", "sentinel"): (),
    ("WAVE-C-UNIVERSALITY", "no-cuda"): (),
    ("WAVE-C-UNIVERSALITY", "sentinel"): (),
}

WAVE_C_REVIEW_CONTEXT_FIELDS = (
    "schema_version",
    "tested_git_head",
    "implementation_parent_git_head",
    "evidence_diff_inventory",
    "candidate_evidence_inventory",
    "raw_command_inventory",
    "raw_junit_inventory",
    "tested_input_inventory",
    "source_config_inventory",
    "dependency_inventory",
    "environment_inventory",
    "reviewed_wave_c_plan_bytes",
    "verification_snapshot_bytes",
    "wave0_terminal_binding",
    "cuda_branch_inventory",
    "claim_specs",
    "evidence_specs",
    "criteria_contracts",
    "review_path_contracts",
    "public_path_contracts",
)

WAVE0_TERMINAL_BINDING_FIELDS = (
    "schema_version",
    "wave0_reviewed_plan",
    "wave0_tested_git_head",
    "wave0_implementation_parent_git_head",
    "wave0_artifact_revision",
    "wave0_ledger",
    "wave0_closure_index",
    "wave0_closure_inventory_sha256",
    "verification_snapshot",
)
```

Every evidence ID is claim-unique. At population, prepend
`verification-evidence/wave-c/{evidence_short}/` to each
`relative_location` and copy the gate template's complete artifact revision.
Records with `supports=True` go only to `evidence`; records with
`supports=False` go only to `counterevidence`. A `REFUTED` adjudicator has
`result="refute"` and links its current `supports=False` counterevidence; an
`EVIDENCE_VERIFIED` adjudicator has `result="support"` and links current
supporting evidence. An `INCONCLUSIVE` adjudicator has `result="abstain"` and
may link no evidence, but it must retain its precise open obligation. No claim
or verifier may cite `index.json`, `domain-evidence.json`, a review-context
digest, or an opposite-polarity evidence ID as closure evidence.

**Executable adapter commands:**

```text
C:\Python314\python.exe -B tools\build_wave_c_evidence.py build --stage candidate --tested-head $testedSha --implementation-parent $implementationSha --raw-dir $rawDir --output-dir $outputDir
C:\Python314\python.exe -B tools\build_wave_c_evidence.py write-cuda-obligation --tested-head $testedSha --implementation-parent $implementationSha --raw-dir $rawDir
C:\Python314\python.exe -B tools\build_wave_c_evidence.py stage-sentinel --tested-head $testedSha --implementation-parent $implementationSha --raw-dir $rawDir --sentinel-run-dir $sentinelRunDir --accepted-gate-sha256 $acceptedGateSha256
C:\Python314\python.exe -B tools\build_wave_c_evidence.py review-context-sha --tested-head $testedSha --implementation-parent $implementationSha --raw-dir $rawDir
C:\Python314\python.exe -B tools\build_wave_c_evidence.py review-target --tested-head $testedSha --implementation-parent $implementationSha --raw-dir $rawDir
C:\Python314\python.exe -B tools\build_wave_c_evidence.py validate-reviews --tested-head $testedSha --implementation-parent $implementationSha --raw-dir $rawDir
C:\Python314\python.exe -B tools\build_wave_c_evidence.py validate-domain --bundle-dir $bundleDir
C:\Python314\python.exe -B tools\build_wave_c_evidence.py populate-ledger --ledger $ledgerPath --closure-index $closureIndex --domain-index $domainIndex
```

The adapter imports, rather than reimplements, these exact generic Wave 0 seams:

```python
from tools.remediation_evidence import (
    PreparedEvidenceBundle,
    PreparedEvidenceFile,
    canonical_json_bytes,
    prepare_evidence_bundle,
    privacy_transform_bytes,
    publish_evidence_bundle,
    resolve_verification_gate,
    validate_evidence_index,
)
```

`build` validates full lowercase 40-character heads and the exact stage relation before reading raw inputs. The raw directory must resolve to `.verification/raw/wave-c/{tested_head[:12]}/{stage}`. The candidate output must resolve to `docs/verification/evidence/wave-c/{tested_head[:12]}`; the closure output must resolve to `verification-evidence/wave-c/{tested_head[:12]}`. The output directory must be absent before preparation. A preparation failure leaves its parent directory byte-identical; an injected publication failure removes only its newly created sibling/destination and leaves every preexisting sibling byte-identical.

Before either stage, resolve the installed validator only through `resolve_verification_gate(VERIFICATION_SNAPSHOT, root=VERIFICATION_ROOT)`, equivalently the frozen CLI `tools/remediation_evidence.py resolve-verification-gate --snapshot docs/verification/remediation/verification-contract-v1.json --root "C:\Users\chris and christine\.codex\skills\verification"`. Validate the snapshot's exact nine active files and reject every PATH/local-copy/environment/home lookup or alternate-root fallback. The reviewed Wave C plan binding is discovered from its current bytes and last-touch commit, which must be an ancestor of both `P` and `E` and whose committed blob must equal the tested plan bytes.

`wave0-terminal-binding.json` is a closed public-form dependency record with exactly `WAVE0_TERMINAL_BINDING_FIELDS`. It rereads the fixed ignored inputs `WAVE0_TERMINAL_LEDGER` and the complete `WAVE0_TERMINAL_CLOSURE`, validates `WAVE0_TERMINAL_INDEX` and every indexed byte, requires the finalized Wave 0 plan bytes to have SHA-256 `WAVE0_REVIEWED_PLAN_SHA256`, requires the same pinned verification snapshot, and validates the Wave 0 ledger as schema `1.0`/mode `closure` with exactly its two terminal claims and one common complete artifact revision. It recomputes the ASCII-sorted closure inventory digest, binds the full Wave 0 tested head and implementation parent, verifies their ancestry and the index heads, and rejects any terminal-ledger/index/closure/snapshot/plan mismatch. This is a read-only prerequisite; Wave C never promotes, rewrites, or fabricates Wave 0 evidence.

The adapter validates three raw command/JUnit pairs against the literal suite argv, `EXPECTED_CPU_ENVIRONMENT`, and `SKIP_ALLOWLIST_BY_SUITE`. The CUDA opt-out skip must appear in all three CPU suites. A listed capability skip may be absent when the host supplies that capability, but every actual skip must match an allowed testcase ID and normalized reason byte-for-byte; no unlisted skip is accepted. The adapter supplies the generic builder with exactly the parsed command records, the closed tested-input policy, resolved required source/config bindings, exact dependency inputs, and raw JUnit bytes. It never supplies a caller-built tested-input inventory, an environment path, review paths, CUDA paths, or `uv.lock`. Generic preparation produces exactly the eleven paths in `GENERIC_PUBLIC_PATHS`: three sanitized command records, dependency/environment/plan bindings, three scrubbed JUnit files, the base privacy map, and the closed base index.

Resolve source/config bindings as the sorted literal `WAVE_C_REQUIRED_SOURCE_CONFIG_BINDINGS` plus every tracked regular file below `docs/verification/remediation/`. Reject missing, extra, case-aliased, untracked-matching, symlink, or reparse inputs and any binding absent from the generic exhaustive tested-input inventory. `dependency_input_paths` is exactly `WAVE_C_DEPENDENCY_INPUTS`, including the verification snapshot and excluding `uv.lock`. The Wave 0 plan, Wave A ownership plan, reviewed Wave C plan, snapshot, `multiagent_elbo.conditioning` source, and both evidence tools are tested/source bindings.

`prepare_claim_contract_file(implementation_parent, tested_head, evidence_stage, cuda_branch)` returns one immutable canonical `PreparedEvidenceFile` at `claim-contracts.json`. Candidate preparation requires `cuda_branch=None`, records `verification_state="CANDIDATE"` for all 14 propositions, and preserves the declared closure-state map without asserting closure. Closure preparation requires exactly `cuda_branch="no-cuda"` or `cuda_branch="sentinel"` and selects the corresponding states, claim-unique eligible evidence, polarity, and precise open obligations. The no-CUDA sentinel obligation is `A fresh exact-revision gate was not separately accepted and the five-job sentinel was not run.` The three broader empirical obligations state respectively that the 40-job confirmatory sweep was not run, attraction was not established by current eligible evidence, and universality was not established by current eligible evidence.

Candidate domain preparation contains exactly the four paths in `CANDIDATE_DOMAIN_PATHS`. Closure reads the raw review tree and exactly one CUDA branch tree before preparing any public byte. The no-CUDA tree contains only `cuda-open-obligation.json`. The sentinel tree contains exactly the six files in `SENTINEL_DOMAIN_PATHS`. Reject a mixed branch, an absent branch, any extra file, head/digest mismatch, non-v3/v2 current schema, legacy promotion, confirmatory artifact, `heavy_sweep_enabled=true`, or a count other than 5 sentinel IDs, 80 step records, 10 endpoint records, and 240 unique worker exchanges. Require requested/observed backend, dtype, device, deterministic-algorithm, TF32, independently observed environment/lock identity, scientific digest, execution digest, parity, and decision controls to agree.

Reuse Wave 0's single structural `privacy_transform_bytes` implementation for every generic and domain JSON/XML preimage. It first validates the exact CPU interpreter and maps it to `<CPU_PYTHON>`; then it structurally replaces repository/user prefixes, every absolute component in argv (including `--option=VALUE`), every environment/path-list component including `PYTHONPATH`, dependency/plan/snapshot/review/result/JUnit paths, Windows drive/UNC/device paths, POSIX paths, hostname, and PID fields. Public bytes contain only the Wave 0 placeholder grammar, retain semantic token/cardinality/order, contain no literal absolute path, and are byte-identical on a second pass.

The base `privacy-transform.json` remains exactly the Wave 0 generic map. Distinct `domain-privacy-transform.json` contains one ASCII-sorted closed `{raw_relative_path,raw_sha256,public_path,public_sha256,transforms}` record for every external, generated, or raw Wave C domain preimage, including Wave 0 terminal binding, claim contracts, CUDA branch inputs, every selected review, both skeptics, and all adjudicators. Every raw input has a raw-to-public hash mapping; every public domain byte is privacy-scanned. The two maps' path sets are disjoint and complete. `index.json`, `privacy-transform.json`, `domain-evidence.json`, and `domain-privacy-transform.json` are generated only from already transformed bytes and separately scanned, avoiding a self-referential hash cycle.

Build `domain-evidence.json` with exactly `{schema_version,wave,evidence_stage,tested_git_head,implementation_parent_git_head,base_index,artifacts}`. `schema_version` is `wave-c-domain-evidence-v1`; `base_index` is exactly `{path,size_bytes,sha256}` for `index.json`; `artifacts` is the ASCII-sorted `{path,kind,size_bytes,sha256}` inventory of every public domain file except `domain-evidence.json`. Merge the unchanged eleven-file generic prepared set, public domain files, and domain index into one immutable `PreparedEvidenceBundle`. Validate the complete detached virtual path/byte union against `CANDIDATE_PUBLIC_PATHS` or exactly one `CLOSURE_PUBLIC_PATHS_BY_BRANCH_AND_TARGET` branch, then call `publish_evidence_bundle` once. After publication call both `validate_evidence_index` and `validate-domain` from disk.

`write-cuda-obligation` writes create-once canonical raw JSON only to the exact closure raw path. It records `schema_version="wave-c-cuda-open-obligation-v1"`, both heads, `state="INCONCLUSIVE"`, the exact obligation above, `sentinel_executed=false`, `confirmatory_executed=false`, and `heavy_confirmatory_executed=false`.

`stage-sentinel` accepts only an already completed sentinel directory from the frozen launcher. It validates the accepted gate SHA-256, exact `E`, protocol-v3 worker exchanges, current v2 fixed-ray schemas, the two identity digests, all counts/settings/controls, and absence of confirmatory/heavy outputs before writing the six create-once raw records. It does not launch a process or inspect the GPU.

`review-context-sha` independently revalidates exact `E/P` and writes canonical `$rawDir/review-context.json` only after constructing the closed `WAVE_C_REVIEW_CONTEXT_FIELDS` payload. Its ASCII-sorted path/size/hash inventories bind the complete `P..E` diff, every candidate byte including its index, the three raw command/JUnit pairs, independently resolved tested/source/dependency/environment inventories, reviewed Wave C plan bytes/last-touch commit, verification snapshot bytes/active-file inventory, validated Wave 0 terminal binding, selected raw CUDA branch, literal claim/evidence/criteria/review/public-path contracts, and both heads. It prints the canonical payload SHA-256 and never creates a public directory or index. Tests mutate every scalar leaf and every array/subobject member; any mutation must change the digest or fail validation, while two unchanged constructions are byte-identical.

Initial review is exactly `INITIAL_REVIEW_PATHS`. Each initial view scores all 14 claims and supplies one of the complete claim-statement-versus-explicit-negation AB/BA comparisons. `review-target` retains the union of declared triggers. With two records it returns 4 when any allowed trigger is present and otherwise 2; AUD-06's `high_severity` makes Wave C's global target at least 4. Target 4 requires both `TARGET4_ADDITIONAL_REVIEW_PATHS`, each scoring exactly the nonempty subset of claims whose per-claim target includes that view. Unresolved `criterion_disagreement` after four requires all `TARGET8_ADDITIONAL_REVIEW_PATHS` and target 8. No partial tier or target 3/5/6/7 is valid; unresolved disagreement after eight is `INCONCLUSIVE`. The four conditional claims normally retain exact two-view/no-trigger target 2, but an actually recorded `small_margin`, `high_dispersion`, or `criterion_disagreement` must follow the same 2-to-4-to-8 transition and cannot be discarded to force the default branch.

Every primary review is canonical `wave-c-review-v1` JSON with exactly `schema_version`, `view_id`, `calibration_kind`, `tested_git_head`, `implementation_parent_git_head`, `reviewed_input_inventory_sha256`, `reviewed_paths`, `claim_scores`, `verdict`, `escalation_triggers`, `unresolved_disagreement`, `open_obligations`, `result_location`, and `falsification_conditions`. `calibration_kind="independent_pairwise_source_reading_v1"`. Scores are integers in `[0,20]`; paths are sorted repository-relative paths; `result_location` is the intended public path below `views/`. Initial-view claim records add the exact Wave 0 comparison fields with candidate IDs `claim-statement` and `explicit-negation` and orders AB/BA; escalation records do not fabricate comparison matches. For every criterion, the aggregate is the exact unrounded arithmetic mean across the required 2, 4, or 8 views. Aggregate, view, and match scores use exactly `CLAIM_CRITERIA_BY_DOMAIN[claim.domain]` and pinned labels. Missing, extra, duplicated, renamed, or generic `coverage`, `freshness`, or `artifact_bound_correctness` criteria are rejected.

AUD-06 has exactly four views with `escalation_triggers=["high_severity"]` or exactly eight views with `escalation_triggers=["criterion_disagreement","high_severity"]`. An extra AUD-06 trigger is contract drift and requires plan re-review. Both claim-specific skeptic records use role `verifier-skeptic` and bind the exact context, evidence IDs, public result location, reason, and falsification condition. After the final target is known, author exactly one closed `verifier-adjudicator` record per claim with the exact target-required view IDs, result from `STATE_TO_ADJUDICATOR_RESULT`, eligible evidence IDs and polarity, public result location, reason, falsification condition, and open obligation. A conflict or missing eligible evidence yields `result="abstain"` and `INCONCLUSIVE`; no majority resolution or wrapper-authored review exists.

`validate-reviews` rereads the context and requires exactly the selected review tier, both AUD-06 skeptics, and all 14 adjudicators before any closure byte exists. It rejects unselected/extra files, trigger removal, an escalation view padded with an untriggered claim, evidence-polarity drift, an index-derived evidence ID, private tokens, arithmetic-mean drift, or result-location drift. The closure branch target is the maximum validated per-claim target and therefore exactly 4 or 8.

`populate-ledger` first checks that the ledger path is exactly `.verification/wave-c/final-ledger.json`, then requires the gate-generated closed four-field closure template with a concrete artifact revision and `claims=[]`. It performs this rejection before opening either index. It then requires exact live `HEAD=E`, `E^=P`, evidence-only `P..E`, exact closure paths, live base/domain/snapshot/plan/Wave0-terminal validation, the selected CUDA branch, and byte-identical indexed reviews/adjudicators. `index.json` is a structural prerequisite and never claim evidence. Population consumes the indexed claim specifications, criterion scores, arithmetic aggregates, AB/BA matches, triggers, targets, verdicts, evidence IDs/polarity, result locations, adjudications, and obligations byte-for-byte; it may not synthesize or alter them. It copies the gate template's complete artifact revision into every claim and evidence entry and never substitutes a Git SHA.

The five defect propositions close `REFUTED` only with their current claim-unique `supports=False` counterevidence and `result="refute"`. The five corrected guards close `EVIDENCE_VERIFIED` only with claim-unique `supports=True` evidence and `result="support"`. The sentinel-specific claim closes only for a validated sentinel branch; otherwise its adjudicator abstains with no fabricated evidence. Confirmatory equivalence, attraction, and universality remain `INCONCLUSIVE` with exact obligations in both branches. Each claim has exactly one adjudicator and the exact complete domain criteria in aggregate, every view, and every comparison.

- [ ] **Step 1: Add literal RED tests for the frozen policies, immutable union, and ledger**

Create `tests/test_wave_c_evidence.py` with these imports and assertions:

```python
from __future__ import annotations

import copy
from hashlib import sha256
import json
from pathlib import Path

import pytest

import tools.build_wave_c_evidence as wave_c


def test_suite_environment_and_skip_policies_are_exact():
    assert len(wave_c.TARGETED_TESTS) == 13
    assert len(wave_c.SUBSYSTEM_TESTS) == 18
    assert wave_c.EXPECTED_CPU_ENVIRONMENT == {
        "CUDA_VISIBLE_DEVICES": "-1",
        "MULTIAGENTELBO_RUN_CUDA_TESTS": None,
        "VFE3_TEST_DEVICE": None,
        "CUBLAS_WORKSPACE_CONFIG": None,
        "PYTHONHASHSEED": "0",
        "PYTHONPATH": None,
    }
    assert set(wave_c.SKIP_ALLOWLIST_BY_SUITE) == {
        "targeted", "subsystem", "full"
    }
    assert len(wave_c.SKIP_ALLOWLIST_BY_SUITE["targeted"]) == 2
    assert len(wave_c.SKIP_ALLOWLIST_BY_SUITE["subsystem"]) == 6
    assert len(wave_c.SKIP_ALLOWLIST_BY_SUITE["full"]) == 6
    assert wave_c.SKIP_ALLOWLIST_BY_SUITE["targeted"][wave_c.CUDA_SKIP] == (
        "requires explicit dedicated CUDA-lane opt-in"
    )


def test_input_and_dependency_policies_are_closed():
    assert wave_c.WAVE_C_TESTED_INPUT_POLICY["schema_version"] == (
        "wave-c-source-config-theory-tools-tests-v1"
    )
    assert wave_c.WAVE_C_DEPENDENCY_INPUTS == (
        "pyproject.toml",
        "environments/cuda-rtx5090-cu128.lock.txt",
        "docs/verification/remediation/verification-contract-v1.json",
    )
    assert "uv.lock" not in wave_c.WAVE_C_DEPENDENCY_INPUTS
    required = set(wave_c.WAVE_C_REQUIRED_SOURCE_CONFIG_BINDINGS)
    for path in (
        "docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md",
        "docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-a.md",
        "docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-c.md",
        "docs/verification/remediation/verification-contract-v1.json",
        "src/multiagent_elbo/conditioning.py",
        "tools/build_wave_c_evidence.py",
        "tools/remediation_evidence.py",
    ):
        assert path in required
    assert wave_c.WAVE0_REVIEWED_PLAN_SHA256 == (
        "dbe2263a3b0fe1e9f5db4ff1fca9a19"
        "f819cfd32ef38da71d6e5cb5485723ac2"
    )
    assert wave_c.VERIFICATION_ROOT.parts[-3:] == (
        ".codex", "skills", "verification"
    )
    assert str(wave_c.VERIFICATION_ROOT).endswith(
        r"\.codex\skills\verification"
    )


def test_generic_domain_and_branch_path_sets_are_exact():
    assert wave_c.GENERIC_PUBLIC_PATHS == (
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
    assert wave_c.CANDIDATE_DOMAIN_PATHS == (
        "claim-contracts.json",
        "domain-evidence.json",
        "domain-privacy-transform.json",
        "wave0-terminal-binding.json",
    )
    assert len(wave_c.CANDIDATE_PUBLIC_PATHS) == 15
    expected_counts = {
        ("no-cuda", 4): 36,
        ("no-cuda", 8): 40,
        ("sentinel", 4): 41,
        ("sentinel", 8): 45,
    }
    assert set(wave_c.CLOSURE_PUBLIC_PATHS_BY_BRANCH_AND_TARGET) == set(
        expected_counts
    )
    for key, count in expected_counts.items():
        paths = wave_c.CLOSURE_PUBLIC_PATHS_BY_BRANCH_AND_TARGET[key]
        assert len(paths) == count
        assert len(paths) == len(set(paths))
        assert paths == tuple(sorted(paths, key=lambda path: path.encode("ascii")))
        assert "privacy-transform.json" in paths
        assert "domain-privacy-transform.json" in paths


def test_claim_inventory_and_cuda_polarity_are_exact():
    assert len(wave_c.CLAIM_SPECS) == 14
    assert {record["id"] for record in wave_c.CLAIM_SPECS} == set(
        wave_c.ALL_CLAIM_IDS
    )
    audits = [record for record in wave_c.CLAIM_SPECS if record["id"].startswith("AUD-")]
    assert len(audits) == 10
    assert sum(record["no_cuda_state"] == "REFUTED" for record in audits) == 5
    assert sum(
        record["no_cuda_state"] == "EVIDENCE_VERIFIED" for record in audits
    ) == 5
    sentinel = next(
        record for record in wave_c.CLAIM_SPECS
        if record["id"] == "WAVE-C-CUDA-SENTINEL-PROTOCOL-CURRENTNESS"
    )
    assert sentinel["no_cuda_state"] == "INCONCLUSIVE"
    assert sentinel["sentinel_state"] == "EVIDENCE_VERIFIED"
    for claim_id in (
        "WAVE-C-CONFIRMATORY-EQUIVALENCE",
        "WAVE-C-ATTRACTION",
        "WAVE-C-UNIVERSALITY",
    ):
        record = next(item for item in wave_c.CLAIM_SPECS if item["id"] == claim_id)
        assert record["no_cuda_state"] == "INCONCLUSIVE"
        assert record["sentinel_state"] == "INCONCLUSIVE"

    for claim_id, records in wave_c.AUDIT_EVIDENCE_SPECS.items():
        assert len(records) == 1
        assert records[0]["relative_location"] == "targeted.xml"
        if claim_id.endswith("-DEFECT-REPRODUCTION"):
            assert records[0]["supports"] is False
            assert records[0]["id"].endswith("-current-counterevidence")
        else:
            assert records[0]["supports"] is True
            assert records[0]["id"].endswith("-current-evidence")
    assert wave_c.STATE_TO_ADJUDICATOR_RESULT == {
        "EVIDENCE_VERIFIED": "support",
        "REFUTED": "refute",
        "INCONCLUSIVE": "abstain",
    }


def test_review_criteria_escalation_and_conditional_view_policies_are_exact():
    assert wave_c.CLAIM_CRITERIA_BY_DOMAIN == {
        "code": (
            ("execution", "execution"),
            ("input_output_behavior", "input/output behavior"),
            ("boundary_failure_behavior", "boundary/failure behavior"),
            ("regression_coverage", "regression coverage"),
            ("configuration_reachability", "configuration reachability"),
            ("reproducibility", "reproducibility"),
        ),
        "experiment": (
            ("hypothesis_endpoint_definition", "hypothesis/endpoint definition"),
            ("protocol_fidelity", "protocol fidelity"),
            ("data_provenance", "data provenance"),
            ("configuration_identity", "configuration identity"),
            ("seed_split_control", "seed/split control"),
            ("statistical_treatment", "statistical treatment"),
            ("reproduced_output_agreement", "reproduced-output agreement"),
            ("robustness", "robustness"),
            ("alternative_explanations", "alternative explanations"),
        ),
    }
    assert wave_c.AUD_06_INITIAL_ESCALATION_TRIGGERS == ("high_severity",)
    assert wave_c.AUD_06_DISAGREEMENT_ESCALATION_TRIGGERS == (
        "criterion_disagreement",
        "high_severity",
    )
    assert wave_c.ALLOWED_ESCALATION_TRIGGERS == (
        "criterion_disagreement",
        "high_dispersion",
        "high_severity",
        "small_margin",
    )
    assert {
        target: len(paths)
        for target, paths in wave_c.REVIEW_PATHS_BY_TARGET.items()
    } == {2: 2, 4: 4, 8: 8}
    assert {
        target: len(view_ids)
        for target, view_ids in wave_c.VIEW_IDS_BY_TARGET.items()
    } == {2: 2, 4: 4, 8: 8}
    assert wave_c.CONDITIONAL_VIEW_IDS == ("artifact-protocol", "code-runtime")
    forbidden = {"coverage", "freshness", "artifact_bound_correctness"}
    for criteria in wave_c.CLAIM_CRITERIA_BY_DOMAIN.values():
        keys = tuple(key for key, unused_label in criteria)
        labels = tuple(label for unused_key, label in criteria)
        assert len(keys) == len(set(keys))
        assert len(labels) == len(set(labels))
        assert forbidden.isdisjoint(keys)


@pytest.mark.parametrize(
    ("completed", "triggers", "unresolved_after_four", "expected"),
    [
        (2, (), False, 2),
        (2, ("small_margin",), False, 4),
        (2, ("high_dispersion",), False, 4),
        (2, ("high_severity",), False, 4),
        (2, ("criterion_disagreement",), False, 4),
        (4, ("high_severity",), False, 4),
        (4, ("criterion_disagreement",), True, 8),
        (8, ("criterion_disagreement",), True, 8),
    ],
)
def test_review_target_transition_is_exact(
    completed, triggers, unresolved_after_four, expected
):
    assert wave_c.required_review_target(
        completed_view_count=completed,
        retained_triggers=triggers,
        unresolved_criterion_disagreement=unresolved_after_four,
    ) == expected


@pytest.mark.parametrize("target", [2, 4, 8])
def test_criterion_aggregates_are_unrounded_arithmetic_means(target):
    keys = tuple(
        key for key, unused_label in wave_c.CLAIM_CRITERIA_BY_DOMAIN["code"]
    )
    scores = tuple(
        {
            key: (view_index + criterion_index) % 21
            for criterion_index, key in enumerate(keys)
        }
        for view_index in range(target)
    )
    assert wave_c.compute_criterion_aggregates(
        scores, criterion_keys=keys
    ) == {
        key: sum(view[key] for view in scores) / target for key in keys
    }


def _review_context_leaf_paths(value, prefix=()):
    if isinstance(value, dict):
        for key in sorted(value):
            yield from _review_context_leaf_paths(value[key], prefix + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _review_context_leaf_paths(item, prefix + (index,))
    else:
        yield prefix


def _mutate_review_context_leaf(value):
    if value is None:
        return "mutated"
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, float):
        return value + 1.0
    if isinstance(value, str):
        return value + "!"
    raise TypeError(type(value))


def test_review_context_digest_binds_every_member(valid_wave_c_review_context):
    assert set(valid_wave_c_review_context) == set(
        wave_c.WAVE_C_REVIEW_CONTEXT_FIELDS
    )
    assert len(valid_wave_c_review_context) == len(
        wave_c.WAVE_C_REVIEW_CONTEXT_FIELDS
    )
    baseline = wave_c.canonical_json_bytes(valid_wave_c_review_context)
    baseline_sha = sha256(baseline).hexdigest()
    assert wave_c.canonical_json_bytes(valid_wave_c_review_context) == baseline
    paths = tuple(_review_context_leaf_paths(valid_wave_c_review_context))
    assert {path[0] for path in paths} == set(wave_c.WAVE_C_REVIEW_CONTEXT_FIELDS)
    for path in paths:
        mutated = copy.deepcopy(valid_wave_c_review_context)
        cursor = mutated
        for component in path[:-1]:
            cursor = cursor[component]
        cursor[path[-1]] = _mutate_review_context_leaf(cursor[path[-1]])
        mutated_bytes = wave_c.canonical_json_bytes(mutated)
        assert mutated_bytes != baseline, path
        assert sha256(mutated_bytes).hexdigest() != baseline_sha, path


@pytest.mark.parametrize(
    "kind", ["command", "dependency", "environment", "plan",
             "review", "adjudicator", "junit"]
)
def test_wave_c_reuses_total_wave0_privacy_transform(
    kind, raw_public, privacy_context
):
    first, mapping = wave_c.privacy_transform_bytes(
        raw_public[kind], kind=kind, privacy_context=privacy_context
    )
    second, _ = wave_c.privacy_transform_bytes(
        first, kind=kind, privacy_context=privacy_context
    )
    assert first == second
    assert mapping["raw_sha256"] == sha256(raw_public[kind]).hexdigest()
    assert mapping["public_sha256"] == sha256(first).hexdigest()
    wave_c.assert_no_literal_absolute_path(first)


def test_cli_is_closed_and_does_not_reimplement_generic_collection():
    parser = wave_c.build_parser()
    assert parser.parse_args([
        "validate-domain", "--bundle-dir",
        "verification-evidence/wave-c/" + "b" * 12,
    ]).command == "validate-domain"
    assert parser.parse_args([
        "populate-ledger", "--ledger", ".verification/wave-c/final-ledger.json",
        "--closure-index", "verification-evidence/wave-c/" + "b" * 12 + "/index.json",
        "--domain-index", "verification-evidence/wave-c/" + "b" * 12 + "/domain-evidence.json",
    ]).command == "populate-ledger"
    assert parser.parse_args([
        "review-context-sha", "--tested-head", "b" * 40,
        "--implementation-parent", "a" * 40,
        "--raw-dir", ".verification/raw/wave-c/bbbbbbbbbbbb/closure",
    ]).command == "review-context-sha"
    assert parser.parse_args([
        "review-target", "--tested-head", "b" * 40,
        "--implementation-parent", "a" * 40,
        "--raw-dir", ".verification/raw/wave-c/bbbbbbbbbbbb/closure",
    ]).command == "review-target"
    assert not hasattr(wave_c, "run_pytest")
    assert not hasattr(wave_c, "write_environment")
    assert not hasattr(wave_c, "write_index")


def test_nonempty_gate_template_rejects_before_missing_indexes(tmp_path: Path):
    ledger = tmp_path / "final-ledger.json"
    ledger.write_text(json.dumps({
        "schema_version": "1.0",
        "mode": "closure",
        "artifact_revision": "git:" + "a" * 40 + ":sha256:" + "b" * 64,
        "claims": [{"id": "preexisting"}],
    }), encoding="utf-8")
    with pytest.raises(ValueError, match="empty closure template"):
        wave_c.populate_ledger(
            ledger=ledger,
            closure_index=tmp_path / "missing-index.json",
            domain_index=tmp_path / "missing-domain.json",
        )
```

In the same temporary two-commit repository fixtures used by Wave 0, add literal negative tests for abbreviated/swapped heads; a source-changing `P..E`; wrong raw/output directory; existing destination; generic or domain extra/missing/case-aliased path; untracked matching input; changed `pyproject.toml`, CUDA lock, verification snapshot, reviewed Wave C plan/last-touch blob, or sole Wave A conditioning source; `uv.lock` dependency injection; any of the nine active installed verification files changed/extra/missing or a noncanonical alternate-root substitution; environment key/value drift; each per-suite skip mutation; duplicate testcase ID; nonzero command; a mutated Wave 0 terminal plan/ledger/index/closure byte or head/revision inconsistency; mixed/missing CUDA branch; sentinel count, digest, protocol, observed environment/lock identity, setting, gate, confirmatory, or heavy-sweep drift; and an absolute interpreter/argv/`PYTHONPATH`/review/result/dependency/JUnit path that survives either privacy map.

Also test every review-context leaf; review head, inventory, path, score, calibration kind, role, skeptic, adjudicator, or disagreement drift; a missing, extra, renamed, duplicated, generic, or incorrectly averaged domain criterion in aggregate, view, or comparison scores; claim/evidence ID or support-polarity drift; any reference to `index.json` as claim evidence; an AUD-06 four-view record without exact `["high_severity"]` or an eight-view record without exact `["criterion_disagreement","high_severity"]`; the normal conditional two-view/no-trigger branch with an incomplete claim-statement/explicit-negation AB/BA grid; and a conditional record with an actual trigger that does not receive the complete 4/8 escalation tier. Reject a missing/misbound adjudicator, base/domain tampering, a synthesized ledger view, and a nonempty gate template before either index is opened. Inject failure immediately before and during the sole `publish_evidence_bundle` call and prove no partial destination remains; instrument every writer and prove no closure byte/index exists before review validation.

- [ ] **Step 2: Run RED and retain machine-readable failure evidence**

```powershell
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'
C:\Python314\python.exe -B -m pytest tests\test_wave_c_evidence.py tests\test_remediation_evidence.py -q -p no:cacheprovider --basetemp=.pytest-wave-c-task8-red --junitxml=C:\tmp\multiagentelbo-wave-c-task8-red.xml
$redExit = $LASTEXITCODE
if ($redExit -eq 0) { throw 'Wave C evidence RED unexpectedly passed' }
if (-not (Test-Path -LiteralPath 'C:\tmp\multiagentelbo-wave-c-task8-red.xml' -PathType Leaf)) { throw 'Wave C evidence RED JUnit is missing' }
```

Expected: nonzero because `tools.build_wave_c_evidence` does not yet exist.

- [ ] **Step 3: Implement the adapter without a second runner or writer**

Implement canonical JSON with sorted keys, compact separators, `ensure_ascii=True`, `allow_nan=False`, UTF-8, and one trailing newline. Use `Path.resolve(strict=True)`, reject reparse/symlink aliases, hash in 1 MiB blocks, and reject Boolean integers/nonfinite numbers where typed data is expected. Every raw writer and final publisher is create-once. All preparation and validation occurs before directory creation. The only replacement write is the installed gate's already-created empty ledger.

- [ ] **Step 4: Run GREEN, static checks, and commit the adapter**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_wave_c_evidence.py tests\test_remediation_evidence.py -q -p no:cacheprovider --basetemp=.pytest-wave-c-task8-green --junitxml=C:\tmp\multiagentelbo-wave-c-task8-green.xml
if ($LASTEXITCODE -ne 0) { throw 'Wave C evidence GREEN failed' }
C:\Python314\python.exe -m ruff check --no-cache tools\build_wave_c_evidence.py tests\test_wave_c_evidence.py
if ($LASTEXITCODE -ne 0) { throw 'Wave C evidence lint failed' }
C:\Python314\python.exe -m ruff format --check --no-cache tools\build_wave_c_evidence.py tests\test_wave_c_evidence.py
if ($LASTEXITCODE -ne 0) { throw 'Wave C evidence format check failed' }
git diff --check
if ($LASTEXITCODE -ne 0) { throw 'Wave C evidence diff check failed' }
git add -- tools/build_wave_c_evidence.py tests/test_wave_c_evidence.py
if ($LASTEXITCODE -ne 0) { throw 'Wave C evidence staging failed' }
git commit -m "test: define wave C evidence lifecycle"
if ($LASTEXITCODE -ne 0) { throw 'Wave C evidence commit failed' }
```


---

### Task 9: Freeze implementation parent `P` and commit the `P/P` candidate bundle

**Files:**

- Create at runtime and commit only: `docs/verification/evidence/wave-c/$implementationShort/`.
- Create at runtime and keep ignored: `.verification/raw/wave-c/$implementationShort/candidate/`.
- Require read-only ignored inputs: `.verification/dependencies/wave-0/final-ledger.json` and the complete validated `.verification/dependencies/wave-0/closure/`.
- Do not create a closure directory or ledger in this task.

- [ ] **Step 1: Prove the implementation parent is clean before naming `P`**

```powershell
$ErrorActionPreference = 'Stop'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'
if (Test-Path Env:MULTIAGENTELBO_RUN_CUDA_TESTS) { throw 'candidate CUDA opt-in is still set' }
if (Test-Path Env:VFE3_TEST_DEVICE) { throw 'candidate CUDA device selector is still set' }
if (Test-Path Env:CUBLAS_WORKSPACE_CONFIG) { throw 'candidate CUDA workspace configuration is still set' }
if (Test-Path Env:PYTHONPATH) { throw 'candidate PYTHONPATH is still set' }

$verificationRoot = 'C:\Users\chris and christine\.codex\skills\verification'
$snapshot = 'docs/verification/remediation/verification-contract-v1.json'
$gate = (& 'C:\Python314\python.exe' -B tools\remediation_evidence.py resolve-verification-gate --snapshot $snapshot --root $verificationRoot).Trim()
if ($LASTEXITCODE -ne 0 -or -not [System.IO.Path]::IsPathFullyQualified($gate)) { throw 'candidate verification gate resolution failed' }
$resolvedVerificationRoot = (Resolve-Path -LiteralPath $verificationRoot).Path
if (-not $gate.StartsWith($resolvedVerificationRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) { throw 'resolved gate escaped the explicit .codex verification root' }
$wave0Ledger = '.verification/dependencies/wave-0/final-ledger.json'
$wave0Closure = '.verification/dependencies/wave-0/closure'
$wave0Index = "$wave0Closure/index.json"
if (-not (Test-Path -LiteralPath $wave0Ledger -PathType Leaf)) { throw 'Wave 0 terminal ledger input is absent' }
if (-not (Test-Path -LiteralPath $wave0Index -PathType Leaf)) { throw 'Wave 0 terminal closure index input is absent' }

C:\Python314\python.exe -m ruff check --no-cache src tests tools run_gaussian_fixed_ray_lab.py run_gaussian_fixed_ray_diagnostic.py run_scale_cocycle_lab.py
if ($LASTEXITCODE -ne 0) { throw 'implementation-parent lint failed' }
C:\Python314\python.exe -m ruff format --check --no-cache src tests tools run_gaussian_fixed_ray_lab.py run_gaussian_fixed_ray_diagnostic.py run_scale_cocycle_lab.py
if ($LASTEXITCODE -ne 0) { throw 'implementation-parent format check failed' }
git diff --check
if ($LASTEXITCODE -ne 0) { throw 'implementation-parent diff check failed' }
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) { throw 'implementation-parent index is dirty' }
git diff --quiet
if ($LASTEXITCODE -ne 0) { throw 'implementation-parent tracked worktree is dirty' }
$trackedStatus = @(git status --porcelain=v1 --untracked-files=no)
if ($LASTEXITCODE -ne 0 -or $trackedStatus.Count -ne 0) { throw "implementation-parent tracked status is not clean: $trackedStatus" }

$implementationSha = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $implementationSha -notmatch '^[0-9a-f]{40}$') { throw 'implementation parent is not a full lowercase SHA' }
$implementationShort = $implementationSha.Substring(0, 12)
$rawDir = ".verification/raw/wave-c/$implementationShort/candidate"
$candidateDir = "docs/verification/evidence/wave-c/$implementationShort"
if (Test-Path -LiteralPath $rawDir) { throw 'candidate raw directory already exists' }
if (Test-Path -LiteralPath $candidateDir) { throw 'candidate public directory already exists' }
New-Item -ItemType Directory -Path $rawDir | Out-Null
```

- [ ] **Step 2: Run the three candidate suites through the generic Wave 0 runner**

```powershell
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/targeted.command.json" --junit "$rawDir/targeted.raw.xml" -- C:\Python314\python.exe -B -m pytest tests/test_artifact_schema.py tests/test_config.py tests/test_cuda_backend.py tests/test_experiment_support.py tests/test_gaussian_fixed_ray.py tests/test_gaussian_fixed_ray_diagnostics.py tests/test_gaussian_fixed_ray_diagnostic_experiment.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py tests/test_gaussian_results_document.py tests/test_launchers.py tests/test_scale_cocycle.py tests/test_scale_cocycle_experiment.py -q -p no:cacheprovider --basetemp="$rawDir/tmp-targeted" --junitxml="$rawDir/targeted.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'candidate targeted suite failed' }

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/subsystem.command.json" --junit "$rawDir/subsystem.raw.xml" -- C:\Python314\python.exe -B -m pytest tests/test_artifact_schema.py tests/test_config.py tests/test_cuda_backend.py tests/test_experiment_support.py tests/test_gaussian_fixed_ray.py tests/test_gaussian_fixed_ray_diagnostics.py tests/test_gaussian_fixed_ray_diagnostic_experiment.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py tests/test_gaussian_results_document.py tests/test_launchers.py tests/test_scale_cocycle.py tests/test_scale_cocycle_experiment.py tests/test_artifacts.py tests/test_runtime.py tests/test_output_paths.py tests/test_gaussian_confirmatory_analysis.py tests/test_shared_scientific_contracts.py -q -p no:cacheprovider --basetemp="$rawDir/tmp-subsystem" --junitxml="$rawDir/subsystem.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'candidate subsystem suite failed' }

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/full.command.json" --junit "$rawDir/full.raw.xml" -- C:\Python314\python.exe -B -m pytest -q -p no:cacheprovider --basetemp="$rawDir/tmp-full" --junitxml="$rawDir/full.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'candidate full suite failed' }
```

No CUDA interpreter, gate, sentinel, confirmatory mode, or GPU query is used for candidate evidence.

- [ ] **Step 3: Prepare, publish once, and validate the absent candidate directory**

```powershell
C:\Python314\python.exe -B tools\build_wave_c_evidence.py build --stage candidate --tested-head $implementationSha --implementation-parent $implementationSha --raw-dir $rawDir --output-dir $candidateDir
if ($LASTEXITCODE -ne 0) { throw 'candidate immutable bundle build failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py validate "$candidateDir/index.json" --cwd .
if ($LASTEXITCODE -ne 0) { throw 'candidate generic index validation failed' }
C:\Python314\python.exe -B tools\build_wave_c_evidence.py validate-domain --bundle-dir $candidateDir
if ($LASTEXITCODE -ne 0) { throw 'candidate domain validation failed' }

$expectedCandidate = @(
    'commands/full.json',
    'commands/subsystem.json',
    'commands/targeted.json',
    'claim-contracts.json',
    'dependencies.json',
    'domain-evidence.json',
    'domain-privacy-transform.json',
    'environment.json',
    'full.xml',
    'index.json',
    'plan-binding.json',
    'privacy-transform.json',
    'subsystem.xml',
    'targeted.xml',
    'wave0-terminal-binding.json'
) | Sort-Object
if ($expectedCandidate.Count -ne 15 -or @($expectedCandidate | Sort-Object -Unique).Count -ne 15) { throw 'candidate contract is not exactly 15 unique paths' }
$actualCandidate = @(Get-ChildItem -LiteralPath $candidateDir -Recurse -File | ForEach-Object {
    [System.IO.Path]::GetRelativePath((Resolve-Path $candidateDir), $_.FullName).Replace('\','/')
} | Sort-Object)
if (Compare-Object $expectedCandidate $actualCandidate) { throw 'candidate public path set drifted' }
```

The candidate generic index records `evidence_stage="candidate"` and both heads equal full `P`. Its generic path set is exactly `GENERIC_PUBLIC_PATHS`. The domain index binds that generic index and exactly `claim-contracts.json`, `domain-privacy-transform.json`, and `wave0-terminal-binding.json`; `domain-evidence.json` inventories that closed domain set without inventing a fifth domain payload. All 15 public paths pass both validators and both privacy scans. Raw staging and the read-only Wave 0 terminal inputs remain ignored.

- [ ] **Step 4: Commit exactly one candidate-evidence child `E`**

```powershell
$repoRoot = (Resolve-Path '.').Path
$expectedStaged = @(Get-ChildItem -LiteralPath $candidateDir -Recurse -File | ForEach-Object {
    [System.IO.Path]::GetRelativePath($repoRoot, $_.FullName).Replace('\','/')
} | Sort-Object)
git add -- $candidateDir
if ($LASTEXITCODE -ne 0) { throw 'candidate staging failed' }
$staged = @(git diff --cached --name-only | ForEach-Object { $_.Replace('\','/') } | Sort-Object)
if ($LASTEXITCODE -ne 0) { throw 'candidate staged inventory failed' }
if (-not $staged) { throw 'candidate staging selected no files' }
if (Compare-Object $expectedStaged $staged) { throw 'candidate staged set differs from validated bundle' }
$candidatePrefix = $candidateDir.Replace('\','/') + '/'
if (@($staged | Where-Object { -not $_.StartsWith($candidatePrefix, [System.StringComparison]::Ordinal) }).Count -ne 0) { throw 'candidate staging escaped its exact directory' }

git commit -m "test: record wave C candidate evidence"
if ($LASTEXITCODE -ne 0) { throw 'candidate evidence commit failed' }
$evidenceSha = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $evidenceSha -notmatch '^[0-9a-f]{40}$') { throw 'evidence child is not a full lowercase SHA' }
$recordedParent = (git rev-parse HEAD^).Trim()
if ($LASTEXITCODE -ne 0 -or $recordedParent -notmatch '^[0-9a-f]{40}$') { throw 'recorded parent is not a full lowercase SHA' }
if ($recordedParent -ne $implementationSha) { throw 'E is not a direct child of P' }
$candidateDiff = @(git diff --name-only "$implementationSha..$evidenceSha" | ForEach-Object { $_.Replace('\','/') })
if ($LASTEXITCODE -ne 0) { throw 'P..E diff failed' }
if (-not $candidateDiff -or @($candidateDiff | Where-Object { -not $_.StartsWith($candidatePrefix, [System.StringComparison]::Ordinal) }).Count -ne 0) { throw 'P..E is not evidence-only' }
$evidenceStatus = @(git status --porcelain=v1)
if ($LASTEXITCODE -ne 0 -or $evidenceStatus.Count -ne 0) { throw "evidence child has nonignored worktree changes: $evidenceStatus" }
```


---

### Task 10: Rerun exact-`E` closure, review raw inputs, and close without a heavy sweep

**Files:**

- Create and keep ignored: `.verification/raw/wave-c/$evidenceShort/closure/`.
- Create once and do not commit: `verification-evidence/wave-c/$evidenceShort/`.
- Create through the installed gate and keep ignored: `.verification/wave-c/final-ledger.json` and `.verification/active.json`.
- Do not change source, configuration, tests, tools, candidate evidence, frozen v3 schemas, root resolution, either digest domain, or the nine-payload scale inventory.

- [ ] **Step 1: Re-establish exact `E/P`, create ignored raw staging, and rerun all CPU suites**

```powershell
$ErrorActionPreference = 'Stop'
$evidenceSha = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $evidenceSha -notmatch '^[0-9a-f]{40}$') { throw 'closure E is not a full lowercase SHA' }
$implementationSha = (git rev-parse HEAD^).Trim()
if ($LASTEXITCODE -ne 0 -or $implementationSha -notmatch '^[0-9a-f]{40}$') { throw 'closure P is not a full lowercase SHA' }
$parentOfE = (git rev-parse "$evidenceSha^").Trim()
if ($LASTEXITCODE -ne 0 -or $parentOfE -ne $implementationSha) { throw 'E^ is not P' }
$implementationShort = $implementationSha.Substring(0, 12)
$evidenceShort = $evidenceSha.Substring(0, 12)
$candidateDir = "docs/verification/evidence/wave-c/$implementationShort"
$candidatePrefix = "$candidateDir/"
if (-not (Test-Path -LiteralPath "$candidateDir/index.json" -PathType Leaf)) { throw 'candidate base index for P is absent' }
if (-not (Test-Path -LiteralPath "$candidateDir/domain-evidence.json" -PathType Leaf)) { throw 'candidate domain index for P is absent' }
$evidenceDiff = @(git diff --name-only "$implementationSha..$evidenceSha" | ForEach-Object { $_.Replace('\','/') })
if ($LASTEXITCODE -ne 0) { throw 'closure P..E diff failed' }
if (-not $evidenceDiff -or @($evidenceDiff | Where-Object { -not $_.StartsWith($candidatePrefix, [System.StringComparison]::Ordinal) }).Count -ne 0) { throw 'closure P..E is not candidate-evidence-only' }
$closureStartStatus = @(git status --porcelain=v1)
if ($LASTEXITCODE -ne 0 -or $closureStartStatus.Count -ne 0) { throw "E is not clean before closure: $closureStartStatus" }

$rawDir = ".verification/raw/wave-c/$evidenceShort/closure"
$closureDir = "verification-evidence/wave-c/$evidenceShort"
if (Test-Path -LiteralPath $rawDir) { throw 'closure raw directory already exists' }
if (Test-Path -LiteralPath $closureDir) { throw 'closure public directory already exists' }
New-Item -ItemType Directory -Path $rawDir | Out-Null

Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'
if (Test-Path Env:MULTIAGENTELBO_RUN_CUDA_TESTS) { throw 'closure CUDA opt-in is still set' }
if (Test-Path Env:VFE3_TEST_DEVICE) { throw 'closure CUDA device selector is still set' }
if (Test-Path Env:CUBLAS_WORKSPACE_CONFIG) { throw 'closure CUDA workspace configuration is still set' }
if (Test-Path Env:PYTHONPATH) { throw 'closure PYTHONPATH is still set' }

$verificationRoot = 'C:\Users\chris and christine\.codex\skills\verification'
$snapshot = 'docs/verification/remediation/verification-contract-v1.json'
$gate = (& 'C:\Python314\python.exe' -B tools\remediation_evidence.py resolve-verification-gate --snapshot $snapshot --root $verificationRoot).Trim()
if ($LASTEXITCODE -ne 0 -or -not [System.IO.Path]::IsPathFullyQualified($gate)) { throw 'closure verification gate resolution failed' }
$resolvedVerificationRoot = (Resolve-Path -LiteralPath $verificationRoot).Path
if (-not $gate.StartsWith($resolvedVerificationRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) { throw 'resolved closure gate escaped the explicit .codex verification root' }
$wave0Ledger = '.verification/dependencies/wave-0/final-ledger.json'
$wave0Closure = '.verification/dependencies/wave-0/closure'
$wave0Index = "$wave0Closure/index.json"
if (-not (Test-Path -LiteralPath $wave0Ledger -PathType Leaf)) { throw 'Wave 0 terminal ledger input is absent at E' }
if (-not (Test-Path -LiteralPath $wave0Index -PathType Leaf)) { throw 'Wave 0 terminal closure index input is absent at E' }

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/targeted.command.json" --junit "$rawDir/targeted.raw.xml" -- C:\Python314\python.exe -B -m pytest tests/test_artifact_schema.py tests/test_config.py tests/test_cuda_backend.py tests/test_experiment_support.py tests/test_gaussian_fixed_ray.py tests/test_gaussian_fixed_ray_diagnostics.py tests/test_gaussian_fixed_ray_diagnostic_experiment.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py tests/test_gaussian_results_document.py tests/test_launchers.py tests/test_scale_cocycle.py tests/test_scale_cocycle_experiment.py -q -p no:cacheprovider --basetemp="$rawDir/tmp-targeted" --junitxml="$rawDir/targeted.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'closure targeted suite failed' }

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/subsystem.command.json" --junit "$rawDir/subsystem.raw.xml" -- C:\Python314\python.exe -B -m pytest tests/test_artifact_schema.py tests/test_config.py tests/test_cuda_backend.py tests/test_experiment_support.py tests/test_gaussian_fixed_ray.py tests/test_gaussian_fixed_ray_diagnostics.py tests/test_gaussian_fixed_ray_diagnostic_experiment.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py tests/test_gaussian_results_document.py tests/test_launchers.py tests/test_scale_cocycle.py tests/test_scale_cocycle_experiment.py tests/test_artifacts.py tests/test_runtime.py tests/test_output_paths.py tests/test_gaussian_confirmatory_analysis.py tests/test_shared_scientific_contracts.py -q -p no:cacheprovider --basetemp="$rawDir/tmp-subsystem" --junitxml="$rawDir/subsystem.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'closure subsystem suite failed' }

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/full.command.json" --junit "$rawDir/full.raw.xml" -- C:\Python314\python.exe -B -m pytest -q -p no:cacheprovider --basetemp="$rawDir/tmp-full" --junitxml="$rawDir/full.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'closure full suite failed' }
```

The raw directory is still ignored and `$closureDir` is still absent. A source, test, tool, dependency, configuration, or candidate-evidence change now invalidates this attempt and requires a new `P`, new evidence-only `E`, and a restart from Task 9.

- [ ] **Step 2: Select exactly one CUDA branch before review, defaulting to no CUDA**

The default branch performs no Torch import, GPU query, gate capture, or CUDA launch:

```powershell
$cudaBranch = 'no-cuda'
C:\Python314\python.exe -B tools\build_wave_c_evidence.py write-cuda-obligation --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir
if ($LASTEXITCODE -ne 0) { throw 'no-CUDA obligation staging failed' }
```

This default remains valid even when a GPU is physically available. Availability is not exact-revision authorization or current sentinel evidence.

Use the sentinel branch only when the operator separately authorizes a fresh gate for exact `E`. Do not reuse any prior accepted digest. Before the first CUDA command, recheck `HEAD=E`, the clean worktree, and explicit authorization. Then execute only this sequence:

```powershell
$preGateHead = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $preGateHead -ne $evidenceSha) { throw 'HEAD changed before CUDA gate' }
$preGateStatus = @(git status --porcelain=v1)
if ($LASTEXITCODE -ne 0 -or $preGateStatus.Count -ne 0) { throw "worktree changed before CUDA gate: $preGateStatus" }
if ($env:CUDA_VISIBLE_DEVICES -ne '-1') { throw 'CPU evidence environment was not pinned before CUDA gate transition' }

$operatorControl = '.verification/gaussian-fixed-ray-operator-control.json'
$confirmatoryControl = '.verification/gaussian-fixed-ray-confirmatory-control.json'
if (Test-Path -LiteralPath $confirmatoryControl) { throw 'confirmatory control must be absent for sentinel-only closure' }
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$gateControl = [ordered]@{
    mode = 'cuda_gate'
    operator_opt_in = $true
    accepted_gate_sha256 = ''
} | ConvertTo-Json -Compress
[System.IO.File]::WriteAllText($operatorControl, $gateControl + "`n", $utf8NoBom)

Remove-Item Env:CUDA_VISIBLE_DEVICES -ErrorAction Stop
try {
    & 'C:\anaconda\python.exe' -c 'import pathlib,sys,torch; expected=pathlib.Path(r"C:\anaconda\python.exe").resolve(); actual=pathlib.Path(sys.executable).resolve(); assert actual == expected, (actual, expected); assert torch.cuda.is_available(); assert torch.cuda.device_count() > 0; print(torch.__version__, actual, torch.cuda.get_device_name(0))'
    if ($LASTEXITCODE -ne 0) { throw 'CUDA interpreter/visibility verification failed before gate' }

    $gateOutput = @(& 'C:\anaconda\python.exe' run_gaussian_fixed_ray_lab.py 2>&1)
    $gateExit = $LASTEXITCODE
    $gateOutput | ForEach-Object { Write-Host $_ }
    if ($gateExit -ne 0) { throw 'fresh CUDA gate command failed' }
    $gateDigestLine = @($gateOutput | Where-Object { $_ -match '^cuda_gate_sha256=[0-9a-f]{64}$' })
    $gatePathLine = @($gateOutput | Where-Object { $_ -match '^cuda_gate_path=' })
    if ($gateDigestLine.Count -ne 1 -or $gatePathLine.Count -ne 1) { throw 'fresh CUDA gate output is not singular' }
    $gateSha256 = ($gateDigestLine[0] -split '=',2)[1]
    $gatePath = ($gatePathLine[0] -split '=',2)[1]
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $gatePath).Hash.ToLowerInvariant() -ne $gateSha256) { throw 'fresh CUDA gate file hash mismatch' }
} finally {
    $env:CUDA_VISIBLE_DEVICES = '-1'
}
if ($env:CUDA_VISIBLE_DEVICES -ne '-1') { throw 'CPU evidence environment was not restored after CUDA gate' }
```

Stop here and present the complete gate record, exact digest, five utilization samples, resident process rows, source/config/system/execution identities, and expiry to the operator. Continue only after the operator explicitly accepts this exact `$gateSha256`. After that acceptance, and not before it, run:

```powershell
$acceptedGateSha256 = $gateSha256
if ($acceptedGateSha256 -ne $gateSha256) { throw 'accepted gate digest differs from the fresh presented digest' }
$postGateHead = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $postGateHead -ne $evidenceSha) { throw 'HEAD changed after gate acceptance' }
$postGateStatus = @(git status --porcelain=v1)
if ($LASTEXITCODE -ne 0 -or $postGateStatus.Count -ne 0) { throw "worktree changed after gate acceptance: $postGateStatus" }
$sentinelControl = [ordered]@{
    mode = 'cuda_sentinel'
    operator_opt_in = $true
    accepted_gate_sha256 = $acceptedGateSha256
} | ConvertTo-Json -Compress
[System.IO.File]::WriteAllText($operatorControl, $sentinelControl + "`n", $utf8NoBom)

if ($env:CUDA_VISIBLE_DEVICES -ne '-1') { throw 'CPU evidence environment was not pinned before sentinel transition' }
Remove-Item Env:CUDA_VISIBLE_DEVICES -ErrorAction Stop
try {
    & 'C:\anaconda\python.exe' -c 'import pathlib,sys,torch; expected=pathlib.Path(r"C:\anaconda\python.exe").resolve(); actual=pathlib.Path(sys.executable).resolve(); assert actual == expected, (actual, expected); assert torch.cuda.is_available(); assert torch.cuda.device_count() > 0; print(torch.__version__, actual, torch.cuda.get_device_name(0))'
    if ($LASTEXITCODE -ne 0) { throw 'CUDA interpreter/visibility verification failed before sentinel' }

    $sentinelOutput = @(& 'C:\anaconda\python.exe' run_gaussian_fixed_ray_lab.py 2>&1)
    $sentinelExit = $LASTEXITCODE
    $sentinelOutput | ForEach-Object { Write-Host $_ }
    if ($sentinelExit -ne 0) { throw 'five-job CUDA sentinel failed' }
    $runDirLine = @($sentinelOutput | Where-Object { $_ -match '^run_dir=' })
    if ($runDirLine.Count -ne 1) { throw 'sentinel run directory output is not singular' }
    $sentinelRunDir = ($runDirLine[0] -split '=',2)[1]
    if (-not (Test-Path -LiteralPath $sentinelRunDir -PathType Container)) { throw 'sentinel run directory is absent' }
} finally {
    $env:CUDA_VISIBLE_DEVICES = '-1'
}
if ($env:CUDA_VISIBLE_DEVICES -ne '-1') { throw 'CPU evidence environment was not restored after sentinel' }

C:\Python314\python.exe -B tools\build_wave_c_evidence.py stage-sentinel --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir --sentinel-run-dir $sentinelRunDir --accepted-gate-sha256 $acceptedGateSha256
if ($LASTEXITCODE -ne 0) { throw 'sentinel domain staging failed' }
$cudaBranch = 'sentinel'
```

The optional branch removes `CUDA_VISIBLE_DEVICES=-1` only inside the two guarded GPU scopes above, verifies the exact CUDA interpreter and visible device before either GPU action, and restores the CPU pin in `finally` before staging or review. Do not set `mode="confirmatory_gate"` or `mode="confirmatory_run"`; do not create the confirmatory-control sidecar; do not enable `heavy_sweep_enabled`; do not run the 40-job sweep. The stage command rejects any evidence that those actions occurred.


- [ ] **Step 3: Obtain and validate raw exact-`E` reviews before any closure index exists**

```powershell
if (Test-Path -LiteralPath $closureDir) { throw 'closure directory exists before reviews' }
if ($env:CUDA_VISIBLE_DEVICES -ne '-1') { throw 'CPU evidence environment was not restored before closure review' }
$reviewContextSha = (& 'C:\Python314\python.exe' -B tools\build_wave_c_evidence.py review-context-sha --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir).Trim()
if ($LASTEXITCODE -ne 0 -or $reviewContextSha -notmatch '^[0-9a-f]{64}$') { throw 'review context digest failed' }
if (-not (Test-Path -LiteralPath "$rawDir/review-context.json" -PathType Leaf)) { throw 'review context bytes are absent' }
if (Test-Path -LiteralPath $closureDir) { throw 'review context wrote closure bytes' }
```

Using the plan execution skill, dispatch exactly the two independent initial source-reading reviews at exact `E` and save canonical raw records at:

```text
.verification/raw/wave-c/$evidenceShort/closure/domain/views/artifact-protocol.json
.verification/raw/wave-c/$evidenceShort/closure/domain/views/code-runtime.json
```

Each initial record has the exact closed `wave-c-review-v1` fields frozen in Task 8, including `calibration_kind="independent_pairwise_source_reading_v1"`. It binds full `$evidenceSha`, full `$implementationSha`, `$reviewContextSha`, sorted path/hash-reviewed inputs, all 14 literal claim/domain/severity/evidence specifications, exact criterion scores, concrete falsification conditions, and its intended public result location. Candidate `A` is `claim-statement` with the literal claim text and candidate `B` is `explicit-negation` with its explicit negation. `artifact-protocol` records order `AB` and `code-runtime` records `BA`; both include the complete ordered comparison criteria and no view ID is used as a candidate ID. `code-runtime` traces fail-before-effects and active call paths. `artifact-protocol` checks protocol v3, legacy nonpromotion, schemas, roots, digests, manifests, exact nine-payload inventory, Wave 0 terminal binding, and both privacy maps.

Run the nonwriting target selector over the two initial records:

```powershell
$reviewTarget = [int]((& 'C:\Python314\python.exe' -B tools\build_wave_c_evidence.py review-target --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir).Trim())
if ($LASTEXITCODE -ne 0 -or $reviewTarget -ne 4) { throw 'AUD-06 high severity did not select the exact initial target 4' }
if (Test-Path -LiteralPath $closureDir) { throw 'review target selection wrote closure bytes' }
```

Now obtain exactly `domain/views/failure-ordering.json` and `domain/views/identity-boundary.json`. Each target-4 record scores exactly the nonempty subset of claims whose retained triggers select target 4; both AUD-06 claims are mandatory and retain exactly `["high_severity"]` unless current criterion disagreement is also recorded. `identity-boundary` independently recomputes both digest preimages, root dependence, installed snapshot, and Wave 0 terminal identity. `failure-ordering` verifies that invalid values fail before provenance, RNG, gate, GPU, worker, or publication effects. A conditional claim with an actual allowed trigger is included; an untriggered claim is not padding.

```powershell
$reviewTarget = [int]((& 'C:\Python314\python.exe' -B tools\build_wave_c_evidence.py review-target --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir).Trim())
if ($LASTEXITCODE -ne 0 -or $reviewTarget -notin @(4,8)) { throw 'target-4 review transition is invalid' }
```

If and only if `$reviewTarget -eq 8`, obtain exactly the four paths in `TARGET8_ADDITIONAL_REVIEW_PATHS`. Each scores only claims with unresolved `criterion_disagreement` after four views. Rerun `review-target` and require a stable 8. The two AUD-06 claims then retain exactly `["criterion_disagreement","high_severity"]`; any extra AUD-06 trigger, trigger removal, partial target-8 tier, or fifth-through-seventh view count is plan drift and stops closure. Any conditional claim that actually reaches target 8 receives all four target-8 views; an untriggered conditional claim remains at its complete target-2 record.

```powershell
if ($reviewTarget -eq 8) {
    $stableTarget = [int]((& 'C:\Python314\python.exe' -B tools\build_wave_c_evidence.py review-target --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir).Trim())
    if ($LASTEXITCODE -ne 0 -or $stableTarget -ne 8) { throw 'target-8 review selection is not stable' }
}
```

Only after the final target is known, save two claim-specific high-severity skeptic records under `domain/views/skeptics/`, one for each AUD-06 proposition, and one claim-specific adjudicator record under `domain/views/adjudicators/` for every one of these literal IDs:

```text
AUD-06-DEFECT-REPRODUCTION
AUD-06-CORRECTED-GUARD
AUD-07-DEFECT-REPRODUCTION
AUD-07-CORRECTED-GUARD
AUD-08-DEFECT-REPRODUCTION
AUD-08-CORRECTED-GUARD
AUD-09-DEFECT-REPRODUCTION
AUD-09-CORRECTED-GUARD
AUD-19-DEFECT-REPRODUCTION
AUD-19-CORRECTED-GUARD
WAVE-C-CUDA-SENTINEL-PROTOCOL-CURRENTNESS
WAVE-C-CONFIRMATORY-EQUIVALENCE
WAVE-C-ATTRACTION
WAVE-C-UNIVERSALITY
```

Each skeptic is a closed `wave-c-skeptic-v1` record with role `verifier-skeptic`, its one literal high-severity AUD-06 claim ID, both heads, `$reviewContextSha`, the exact claim-unique eligible evidence IDs, public result location, reason, and falsification condition. Each adjudicator is a closed `wave-c-adjudicator-v1` record with exactly `schema_version`, `role`, `claim_id`, `tested_git_head`, `implementation_parent_git_head`, `reviewed_input_inventory_sha256`, `escalation_triggers`, `escalation_target`, `view_ids`, `result`, `evidence_ids`, `result_location`, `reason`, `falsification_condition`, and `open_obligations`. It binds the exact per-claim 2/4/8 view IDs, exact public repository-relative path, and exact evidence IDs from `EVIDENCE_SPECS_BY_CLAIM_AND_BRANCH`. It never cites either index, domain index, privacy map, or review-context digest as claim evidence.

Defect adjudicators use `result="refute"` and only the claim's `supports=False` counterevidence. Guard adjudicators use `result="support"` and only the claim's `supports=True` evidence. The sentinel adjudicator supports only on the validated sentinel branch; on no-CUDA it abstains with an empty evidence-ID set and the precise missing-gate/sentinel obligation. Confirmatory-equivalence, attraction, and universality adjudicators abstain with empty evidence-ID sets and their precise obligations in both branches. Any conflict or missing eligible evidence also abstains and forces `INCONCLUSIVE`. A reviewer cannot promote a producer's `verification_state="CANDIDATE"`, and no majority vote closes a claim.

The normal four conditional-claim records have exact two-view/no-trigger target 2, candidate IDs `claim-statement`/`explicit-negation`, complete AB/BA matches, and one adjudicator bound to both views. If an actual allowed trigger exists, its exact complete 4/8 view branch and adjudicator binding replace that default. For every claim, each aggregate criterion equals the exact unrounded arithmetic mean across its selected views, and aggregate, view, and comparison keys/labels equal the complete pinned domain map.

```powershell
$validatedTarget = [int]((& 'C:\Python314\python.exe' -B tools\build_wave_c_evidence.py validate-reviews --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir).Trim())
if ($LASTEXITCODE -ne 0 -or $validatedTarget -ne $reviewTarget) { throw 'raw exact-E review validation failed' }
if (Test-Path -LiteralPath $closureDir) { throw 'review validation wrote closure bytes' }
```

Any requested source/test/tool/configuration fix invalidates this closure attempt. Make the fix with RED/GREEN, form a new `P`, commit a new evidence-only `E`, and restart at Task 9. Do not edit the raw record into a passing verdict.

- [ ] **Step 4: Prepare the base and domain union in memory, publish once, and validate**

```powershell
if (Test-Path -LiteralPath $closureDir) { throw 'closure destination exists before immutable preparation' }
C:\Python314\python.exe -B tools\build_wave_c_evidence.py build --stage closure --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir --output-dir $closureDir
if ($LASTEXITCODE -ne 0) { throw 'closure immutable base-plus-domain publication failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py validate "$closureDir/index.json" --cwd .
if ($LASTEXITCODE -ne 0) { throw 'closure generic index validation failed' }
C:\Python314\python.exe -B tools\build_wave_c_evidence.py validate-domain --bundle-dir $closureDir
if ($LASTEXITCODE -ne 0) { throw 'closure domain validation failed' }
```

The build command is the first command in Task 10 allowed to create `$closureDir`. It reads already validated raw reviews and CUDA branch inputs, prepares all base and domain bytes in memory, validates the detached union, and publishes the complete union atomically once. Before freezing, reopen every selected public review, both skeptics, all 14 adjudicators, `wave0-terminal-binding.json`, and both privacy maps; require the index/domain hashes and semantic records to equal the validated raw records after the declared Wave 0 structural privacy transform. No regeneration or wrapper-authored verdict is accepted.

Verify the exact public set and exact nonignored untracked set:

```powershell
$claimIds = @(
    'AUD-06-DEFECT-REPRODUCTION', 'AUD-06-CORRECTED-GUARD',
    'AUD-07-DEFECT-REPRODUCTION', 'AUD-07-CORRECTED-GUARD',
    'AUD-08-DEFECT-REPRODUCTION', 'AUD-08-CORRECTED-GUARD',
    'AUD-09-DEFECT-REPRODUCTION', 'AUD-09-CORRECTED-GUARD',
    'AUD-19-DEFECT-REPRODUCTION', 'AUD-19-CORRECTED-GUARD',
    'WAVE-C-CUDA-SENTINEL-PROTOCOL-CURRENTNESS',
    'WAVE-C-CONFIRMATORY-EQUIVALENCE', 'WAVE-C-ATTRACTION',
    'WAVE-C-UNIVERSALITY'
)
$expectedClosure = @(
    'claim-contracts.json',
    'commands/full.json', 'commands/subsystem.json', 'commands/targeted.json',
    'dependencies.json', 'domain-evidence.json', 'domain-privacy-transform.json',
    'environment.json', 'full.xml', 'index.json', 'plan-binding.json',
    'privacy-transform.json', 'subsystem.xml', 'targeted.xml',
    'views/artifact-protocol.json',
    'views/code-runtime.json', 'views/failure-ordering.json',
    'views/identity-boundary.json',
    'views/skeptics/AUD-06-DEFECT-REPRODUCTION.json',
    'views/skeptics/AUD-06-CORRECTED-GUARD.json',
    'wave0-terminal-binding.json'
)
$expectedClosure += @($claimIds | ForEach-Object { "views/adjudicators/$_.json" })
if ($cudaBranch -eq 'no-cuda') {
    $expectedClosure += 'cuda-open-obligation.json'
} elseif ($cudaBranch -eq 'sentinel') {
    $expectedClosure += @(
        'cuda-sentinel/command-record.json', 'cuda-sentinel/gate.json',
        'cuda-sentinel/manifest.json', 'cuda-sentinel/metrics.json',
        'cuda-sentinel/semantic-array-hashes.json',
        'cuda-sentinel/worker-exchange-index.json'
    )
} else {
    throw "unknown CUDA branch: $cudaBranch"
}
if ($validatedTarget -eq 8) {
    $expectedClosure += @(
        'views/escalation/configuration-boundary.json',
        'views/escalation/digest-preimage.json',
        'views/escalation/protocol-adversary.json',
        'views/escalation/publication-root.json'
    )
} elseif ($validatedTarget -ne 4) {
    throw "closure review target is not 4 or 8: $validatedTarget"
}
$expectedClosure = @($expectedClosure | Sort-Object)
$expectedClosureCount = @{
    'no-cuda/4' = 36
    'no-cuda/8' = 40
    'sentinel/4' = 41
    'sentinel/8' = 45
}["$cudaBranch/$validatedTarget"]
if ($null -eq $expectedClosureCount) { throw 'closure branch/target count is undefined' }
if ($expectedClosure.Count -ne $expectedClosureCount -or @($expectedClosure | Sort-Object -Unique).Count -ne $expectedClosureCount) { throw 'closure contract count/uniqueness drifted' }
$actualClosure = @(Get-ChildItem -LiteralPath $closureDir -Recurse -File | ForEach-Object {
    [System.IO.Path]::GetRelativePath((Resolve-Path $closureDir), $_.FullName).Replace('\','/')
} | Sort-Object)
if (Compare-Object $expectedClosure $actualClosure) { throw 'closure public path set drifted' }

$repoRoot = (Resolve-Path '.').Path
$expectedUntracked = @($actualClosure | ForEach-Object {
    [System.IO.Path]::GetRelativePath($repoRoot, (Join-Path (Resolve-Path $closureDir) $_)).Replace('\','/')
} | Sort-Object)
$actualUntracked = @(git ls-files --others --exclude-standard | ForEach-Object { $_.Replace('\','/') } | Sort-Object)
if ($LASTEXITCODE -ne 0) { throw 'untracked inventory failed' }
if (Compare-Object $expectedUntracked $actualUntracked) { throw 'nonignored untracked set differs from exact closure union' }

git diff --check
if ($LASTEXITCODE -ne 0) { throw 'closure diff check failed' }
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) { throw 'Git index changed during closure' }
git diff --quiet
if ($LASTEXITCODE -ne 0) { throw 'tracked worktree changed during closure' }

$freezePath = "C:\tmp\multiagentelbo-wave-c-closure-$evidenceShort.json"
$freeze = Get-ChildItem -LiteralPath $closureDir -Recurse -File | Sort-Object FullName | ForEach-Object {
    [ordered]@{
        path = [System.IO.Path]::GetRelativePath((Resolve-Path $closureDir), $_.FullName).Replace('\','/')
        size_bytes = $_.Length
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()
    }
}
$freeze | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $freezePath -Encoding utf8NoBOM
$freezeSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $freezePath).Hash
```

- [ ] **Step 5: Prove the empty gate fails, populate explicitly, and validate all 14 claims**

```powershell
$verificationRoot = 'C:\Users\chris and christine\.codex\skills\verification'
$snapshot = 'docs/verification/remediation/verification-contract-v1.json'
$gate = (& 'C:\Python314\python.exe' -B tools\remediation_evidence.py resolve-verification-gate --snapshot $snapshot --root $verificationRoot).Trim()
if ($LASTEXITCODE -ne 0 -or -not [System.IO.Path]::IsPathFullyQualified($gate)) { throw 'final verification gate resolution failed' }
$resolvedVerificationRoot = (Resolve-Path -LiteralPath $verificationRoot).Path
if (-not $gate.StartsWith($resolvedVerificationRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) { throw 'final gate escaped the explicit .codex verification root' }
$ledgerPath = '.verification/wave-c/final-ledger.json'
if (Test-Path -LiteralPath '.verification/active.json') { throw 'verification gate is already active' }
if (Test-Path -LiteralPath $ledgerPath) { throw 'Wave C ledger already exists' }

& 'C:\Python314\python.exe' $gate start --cwd . --mode closure --ledger $ledgerPath
if ($LASTEXITCODE -ne 0) { throw 'verification gate start failed' }
& 'C:\Python314\python.exe' $gate validate --cwd . $ledgerPath
if ($LASTEXITCODE -eq 0) { throw 'empty Wave C gate template unexpectedly validated' }

C:\Python314\python.exe -B tools\build_wave_c_evidence.py populate-ledger --ledger $ledgerPath --closure-index "$closureDir/index.json" --domain-index "$closureDir/domain-evidence.json"
if ($LASTEXITCODE -ne 0) { throw 'Wave C ledger population failed' }
& 'C:\Python314\python.exe' $gate validate --cwd . $ledgerPath
if ($LASTEXITCODE -ne 0) { throw 'populated Wave C ledger validation failed' }

$ledger = Get-Content -Raw -LiteralPath $ledgerPath | ConvertFrom-Json
if (@($ledger.claims).Count -ne 14) { throw 'Wave C ledger does not contain exactly 14 claims' }
$expectedRootFields = @('artifact_revision','claims','mode','schema_version')
$actualRootFields = @($ledger.PSObject.Properties.Name | Sort-Object)
if (Compare-Object $expectedRootFields $actualRootFields) { throw 'Wave C ledger root projection drifted from schema 1.0' }
$expectedClaimFields = @(
    'artifact_revision','counterevidence','criteria','domain','escalation_target',
    'escalation_triggers','evidence','evidence_invalidated','id','open_obligations',
    'severity','state','statement','verifiers','views'
) | Sort-Object
$expectedEvidenceFields = @('artifact_revision','id','kind','location')
$expectedCounterevidenceFields = @('artifact_revision','id','kind','location','supports')
$expectedVerifierFields = @('evidence_ids','result','result_location','role','view_ids')
$claimsById = @{}
foreach ($claim in $ledger.claims) {
    $actualClaimFields = @($claim.PSObject.Properties.Name | Sort-Object)
    if (Compare-Object $expectedClaimFields $actualClaimFields) { throw "claim projection drifted from schema 1.0: $($claim.id)" }
    if ($claim.artifact_revision -ne $ledger.artifact_revision) { throw "claim artifact revision drifted: $($claim.id)" }
    foreach ($record in @($claim.evidence)) {
        if (Compare-Object $expectedEvidenceFields @($record.PSObject.Properties.Name | Sort-Object)) { throw "evidence projection drifted: $($claim.id)/$($record.id)" }
        if ($record.artifact_revision -ne $ledger.artifact_revision) { throw "evidence artifact revision drifted: $($claim.id)/$($record.id)" }
    }
    foreach ($record in @($claim.counterevidence)) {
        if (Compare-Object $expectedCounterevidenceFields @($record.PSObject.Properties.Name | Sort-Object)) { throw "counterevidence projection drifted: $($claim.id)/$($record.id)" }
        if ($record.artifact_revision -ne $ledger.artifact_revision) { throw "counterevidence artifact revision drifted: $($claim.id)/$($record.id)" }
    }
    foreach ($verifier in @($claim.verifiers)) {
        if (Compare-Object $expectedVerifierFields @($verifier.PSObject.Properties.Name | Sort-Object)) { throw "verifier projection drifted: $($claim.id)/$($verifier.role)" }
    }
    $claimsById[$claim.id] = $claim
}
foreach ($audit in @(6,7,8,9,19)) {
    $auditText = $audit.ToString('00')
    $defectId = "AUD-$auditText-DEFECT-REPRODUCTION"
    $guardId = "AUD-$auditText-CORRECTED-GUARD"
    $defect = $claimsById[$defectId]
    $guard = $claimsById[$guardId]
    if ($defect.state -ne 'REFUTED') { throw "AUD-$audit defect proposition is not REFUTED" }
    if ($guard.state -ne 'EVIDENCE_VERIFIED') { throw "AUD-$audit guard is not EVIDENCE_VERIFIED" }
    $defectEvidenceId = "aud-$auditText-defect-current-counterevidence"
    $guardEvidenceId = "aud-$auditText-guard-current-evidence"
    if (@($defect.evidence).Count -ne 0 -or @($defect.counterevidence).Count -ne 1) { throw "defect evidence polarity drifted: $defectId" }
    if ($defect.counterevidence[0].id -ne $defectEvidenceId -or $defect.counterevidence[0].supports -ne $false) { throw "defect counterevidence identity/support drifted: $defectId" }
    if (@($guard.evidence).Count -ne 1 -or @($guard.counterevidence).Count -ne 0) { throw "guard evidence polarity drifted: $guardId" }
    if ($guard.evidence[0].id -ne $guardEvidenceId) { throw "guard evidence identity drifted: $guardId" }
    foreach ($claim in @($defect,$guard)) {
        if ($claim.evidence_invalidated -ne $false) { throw "terminal audit evidence is invalidated: $($claim.id)" }
        $adjudicators = @($claim.verifiers | Where-Object role -eq 'verifier-adjudicator')
        if ($adjudicators.Count -ne 1) { throw "missing adjudicator: $($claim.id)" }
        $expectedResult = if ($claim.id -eq $defectId) { 'refute' } else { 'support' }
        $expectedEvidenceId = if ($claim.id -eq $defectId) { $defectEvidenceId } else { $guardEvidenceId }
        if ($adjudicators[0].result -ne $expectedResult) { throw "audit adjudicator result drifted: $($claim.id)" }
        if (Compare-Object @($expectedEvidenceId) @($adjudicators[0].evidence_ids)) { throw "audit adjudicator evidence binding drifted: $($claim.id)" }
        $expectedLocation = "$closureDir/views/adjudicators/$($claim.id).json".Replace('\','/')
        if ($adjudicators[0].result_location.Replace('\','/') -ne $expectedLocation) { throw "audit adjudicator location drifted: $($claim.id)" }
    }
}
foreach ($claimId in @('AUD-06-DEFECT-REPRODUCTION','AUD-06-CORRECTED-GUARD')) {
    $claim = $claimsById[$claimId]
    $skeptics = @($claim.verifiers | Where-Object role -eq 'verifier-skeptic')
    if ($skeptics.Count -ne 1) { throw "missing AUD-06 skeptic: $claimId" }
    $viewCount = @($claim.views.scores).Count
    if ($viewCount -notin @(4,8)) { throw "AUD-06 view count is neither 4 nor 8: $claimId=$viewCount" }
    $expectedTriggers = if ($viewCount -eq 4) {
        @('high_severity')
    } else {
        @('criterion_disagreement','high_severity')
    }
    $actualTriggers = @($claim.escalation_triggers | Sort-Object)
    if (Compare-Object $expectedTriggers $actualTriggers) { throw "AUD-06 escalation trigger set drifted: $claimId" }
    $expectedTarget = if ($viewCount -eq 4) { 4 } else { 8 }
    if ($claim.escalation_target -ne $expectedTarget) { throw "AUD-06 escalation target drifted: $claimId" }
    $expectedSkepticResult = if ($claimId.EndsWith('DEFECT-REPRODUCTION')) { 'refute' } else { 'support' }
    $expectedSkepticEvidence = if ($claimId.EndsWith('DEFECT-REPRODUCTION')) {
        'aud-06-defect-current-counterevidence'
    } else {
        'aud-06-guard-current-evidence'
    }
    if ($skeptics[0].result -ne $expectedSkepticResult) { throw "AUD-06 skeptic result drifted: $claimId" }
    if (Compare-Object @($expectedSkepticEvidence) @($skeptics[0].evidence_ids)) { throw "AUD-06 skeptic evidence binding drifted: $claimId" }
    $expectedViewIds = @($claim.views.scores | ForEach-Object view_id | Sort-Object)
    if (Compare-Object $expectedViewIds @($skeptics[0].view_ids | Sort-Object)) { throw "AUD-06 skeptic view binding drifted: $claimId" }
    $expectedSkepticLocation = "$closureDir/views/skeptics/$claimId.json".Replace('\','/')
    if ($skeptics[0].result_location.Replace('\','/') -ne $expectedSkepticLocation) { throw "AUD-06 skeptic location drifted: $claimId" }
}
$sentinelClaim = $claimsById['WAVE-C-CUDA-SENTINEL-PROTOCOL-CURRENTNESS']
$expectedSentinelState = if ($cudaBranch -eq 'sentinel') { 'EVIDENCE_VERIFIED' } else { 'INCONCLUSIVE' }
if ($sentinelClaim.state -ne $expectedSentinelState) { throw 'sentinel-specific claim state drifted' }
$sentinelAdjudicator = @($sentinelClaim.verifiers | Where-Object role -eq 'verifier-adjudicator')
if ($sentinelAdjudicator.Count -ne 1) { throw 'sentinel claim adjudicator count drifted' }
if ($cudaBranch -eq 'sentinel') {
    if (@($sentinelClaim.evidence).Count -ne 1 -or @($sentinelClaim.counterevidence).Count -ne 0) { throw 'sentinel evidence polarity drifted' }
    if ($sentinelClaim.evidence[0].id -ne 'wave-c-sentinel-current-reproduced-output') { throw 'sentinel evidence ID drifted' }
    if ($sentinelAdjudicator[0].result -ne 'support') { throw 'sentinel adjudicator did not support validated sentinel evidence' }
    if (Compare-Object @('wave-c-sentinel-current-reproduced-output') @($sentinelAdjudicator[0].evidence_ids)) { throw 'sentinel adjudicator evidence binding drifted' }
    if (@($sentinelClaim.open_obligations).Count -ne 0) { throw 'validated sentinel claim retained an open obligation' }
} else {
    if (@($sentinelClaim.evidence).Count -ne 0 -or @($sentinelClaim.counterevidence).Count -ne 0) { throw 'no-CUDA sentinel claim fabricated evidence' }
    if ($sentinelAdjudicator[0].result -ne 'abstain' -or @($sentinelAdjudicator[0].evidence_ids).Count -ne 0) { throw 'no-CUDA sentinel adjudicator did not abstain cleanly' }
    if (@($sentinelClaim.open_obligations).Count -eq 0) { throw 'no-CUDA sentinel claim lacks its precise obligation' }
}
foreach ($claimId in @('WAVE-C-CONFIRMATORY-EQUIVALENCE','WAVE-C-ATTRACTION','WAVE-C-UNIVERSALITY')) {
    $claim = $claimsById[$claimId]
    if ($claim.state -ne 'INCONCLUSIVE') { throw "broader empirical claim was overpromoted: $claimId" }
    if (@($claim.open_obligations).Count -eq 0) { throw "broader empirical claim lacks an obligation: $claimId" }
    if (@($claim.evidence).Count -ne 0 -or @($claim.counterevidence).Count -ne 0) { throw "broader empirical claim fabricated evidence: $claimId" }
    $adjudicator = @($claim.verifiers | Where-Object role -eq 'verifier-adjudicator')
    if ($adjudicator.Count -ne 1 -or $adjudicator[0].result -ne 'abstain' -or @($adjudicator[0].evidence_ids).Count -ne 0) { throw "broader empirical adjudicator did not abstain cleanly: $claimId" }
}

$codeCriteria = @(
    'boundary_failure_behavior', 'configuration_reachability', 'execution',
    'input_output_behavior', 'regression_coverage', 'reproducibility'
)
$experimentCriteria = @(
    'alternative_explanations', 'configuration_identity', 'data_provenance',
    'hypothesis_endpoint_definition', 'protocol_fidelity', 'reproduced_output_agreement',
    'robustness', 'seed_split_control', 'statistical_treatment'
)
foreach ($claim in @($ledger.claims)) {
    $expectedCriteria = if ($claim.domain -eq 'code') {
        $codeCriteria
    } elseif ($claim.domain -eq 'experiment') {
        $experimentCriteria
    } else {
        throw "unexpected Wave C claim domain: $($claim.domain)"
    }
    $aggregateNames = @($claim.criteria | ForEach-Object name | Sort-Object)
    if (Compare-Object $expectedCriteria $aggregateNames) { throw "aggregate criterion set drifted: $($claim.id)" }
    if ($claim.views.calibration_kind -ne 'independent_pairwise_source_reading_v1') { throw "calibration kind drifted: $($claim.id)" }
    if (@($claim.views.scores).Count -ne $claim.escalation_target) { throw "view count/target drifted: $($claim.id)" }
    if (@($claim.views.scores | ForEach-Object view_id | Sort-Object -Unique).Count -ne $claim.escalation_target) { throw "view IDs are not unique: $($claim.id)" }
    foreach ($score in @($claim.views.scores)) {
        $scoreNames = @($score.criteria | ForEach-Object name | Sort-Object)
        if (Compare-Object $expectedCriteria $scoreNames) { throw "view criterion set drifted: $($claim.id)/$($score.view_id)" }
    }
    foreach ($match in @($claim.views.comparison.matches)) {
        $matchNames = @($match.criteria | ForEach-Object name | Sort-Object)
        if (Compare-Object $expectedCriteria $matchNames) { throw "comparison criterion set drifted: $($claim.id)" }
    }
    foreach ($criterionName in $expectedCriteria) {
        $values = @($claim.views.scores | ForEach-Object {
            @($_.criteria | Where-Object name -eq $criterionName)[0].score
        })
        $expectedMean = ($values | Measure-Object -Sum).Sum / $values.Count
        $aggregate = @($claim.criteria | Where-Object name -eq $criterionName)[0].score
        if ($aggregate -ne $expectedMean) { throw "unrounded arithmetic mean drifted: $($claim.id)/$criterionName" }
    }
}

$conditionalIds = @(
    'WAVE-C-CUDA-SENTINEL-PROTOCOL-CURRENTNESS',
    'WAVE-C-CONFIRMATORY-EQUIVALENCE',
    'WAVE-C-ATTRACTION',
    'WAVE-C-UNIVERSALITY'
)
$conditionalViewsByTarget = @{
    2 = @('artifact-protocol','code-runtime')
    4 = @('artifact-protocol','code-runtime','failure-ordering','identity-boundary')
    8 = @(
        'artifact-protocol','code-runtime','failure-ordering','identity-boundary',
        'configuration-boundary','digest-preimage','protocol-adversary','publication-root'
    )
}
$expectedCandidateIds = @('claim-statement','explicit-negation')
$expectedPairs = @(
    'claim-statement>explicit-negation@artifact-protocol',
    'explicit-negation>claim-statement@code-runtime'
)
foreach ($claimId in $conditionalIds) {
    $claim = $claimsById[$claimId]
    if ($claim.escalation_target -notin @(2,4,8)) { throw "conditional escalation target drifted: $claimId" }
    $actualTriggers = @($claim.escalation_triggers | Sort-Object)
    if ($claim.escalation_target -eq 2 -and $actualTriggers.Count -ne 0) { throw "conditional target-2 branch retained a trigger: $claimId" }
    if ($claim.escalation_target -eq 4 -and $actualTriggers.Count -eq 0) { throw "conditional target-4 branch lacks its actual trigger: $claimId" }
    if ($claim.escalation_target -eq 8 -and $actualTriggers -notcontains 'criterion_disagreement') { throw "conditional target-8 branch lacks criterion disagreement: $claimId" }
    if ($actualTriggers -contains 'high_severity') { throw "medium-severity conditional claim fabricated high-severity escalation: $claimId" }
    $expectedConditionalViews = @($conditionalViewsByTarget[$claim.escalation_target] | Sort-Object)
    $viewIds = @($claim.views.scores | ForEach-Object view_id | Sort-Object)
    if (Compare-Object $expectedConditionalViews $viewIds) { throw "conditional selected view set drifted: $claimId" }
    $comparison = $claim.views.comparison
    if ($comparison.method -ne 'pairwise' -or $comparison.candidate_count -ne 2 -or @($comparison.pivot_ids).Count -ne 0) { throw "conditional pairwise header drifted: $claimId" }
    $candidateIds = @($comparison.candidate_ids | Sort-Object)
    if (Compare-Object @($expectedCandidateIds | Sort-Object) $candidateIds) { throw "conditional comparison candidates drifted: $claimId" }
    $descriptionIds = @($comparison.candidate_descriptions | ForEach-Object id | Sort-Object)
    if (Compare-Object @($expectedCandidateIds | Sort-Object) $descriptionIds) { throw "conditional comparison descriptions drifted: $claimId" }
    if (@($comparison.candidate_descriptions | Where-Object { -not $_.description }).Count -ne 0) { throw "conditional comparison description is empty: $claimId" }
    $orders = @($comparison.orders | Sort-Object)
    if (Compare-Object @('AB','BA') $orders) { throw "conditional AB/BA orders drifted: $claimId" }
    $pairs = @($comparison.matches | ForEach-Object { "$($_.left)>$($_.right)@$($_.view_id)" } | Sort-Object)
    if (Compare-Object $expectedPairs $pairs) { throw "conditional ordered pair grid drifted: $claimId" }
    $adjudicators = @($claim.verifiers | Where-Object role -eq 'verifier-adjudicator')
    if ($adjudicators.Count -ne 1) { throw "conditional adjudicator count drifted: $claimId" }
    $adjudicatorViews = @($adjudicators[0].view_ids | Sort-Object)
    if (Compare-Object $expectedConditionalViews $adjudicatorViews) { throw "conditional adjudicator view binding drifted: $claimId" }
    $expectedResult = if ($claim.state -eq 'EVIDENCE_VERIFIED') { 'support' } else { 'abstain' }
    $expectedEvidenceIds = if ($claim.state -eq 'EVIDENCE_VERIFIED') {
        @('wave-c-sentinel-current-reproduced-output')
    } else {
        @()
    }
    if ($adjudicators[0].result -ne $expectedResult) { throw "conditional adjudicator result drifted: $claimId" }
    $actualEvidenceIds = @($adjudicators[0].evidence_ids)
    if ($actualEvidenceIds.Count -ne $expectedEvidenceIds.Count) { throw "conditional adjudicator evidence count drifted: $claimId" }
    if ($expectedEvidenceIds.Count -gt 0 -and (Compare-Object $expectedEvidenceIds $actualEvidenceIds)) { throw "conditional adjudicator evidence binding drifted: $claimId" }
    $expectedLocation = "$closureDir/views/adjudicators/$claimId.json".Replace('\','/')
    if ($adjudicators[0].result_location.Replace('\','/') -ne $expectedLocation) { throw "conditional adjudicator location drifted: $claimId" }
}
```

The sentinel branch does not close confirmatory equivalence, attraction, universality, or general CUDA operational currentness. It closes only the literal five-job sentinel protocol claim at exact `E`.

- [ ] **Step 6: Prove closure bytes and the untracked set stayed frozen after ledger work**

```powershell
C:\Python314\python.exe -B tools\remediation_evidence.py validate "$closureDir/index.json" --cwd .
if ($LASTEXITCODE -ne 0) { throw 'post-ledger generic index validation failed' }
C:\Python314\python.exe -B tools\build_wave_c_evidence.py validate-domain --bundle-dir $closureDir
if ($LASTEXITCODE -ne 0) { throw 'post-ledger domain validation failed' }
$freezeAfterPath = "C:\tmp\multiagentelbo-wave-c-closure-$evidenceShort-after-ledger.json"
$freezeAfter = Get-ChildItem -LiteralPath $closureDir -Recurse -File | Sort-Object FullName | ForEach-Object {
    [ordered]@{
        path = [System.IO.Path]::GetRelativePath((Resolve-Path $closureDir), $_.FullName).Replace('\','/')
        size_bytes = $_.Length
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()
    }
}
$freezeAfter | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $freezeAfterPath -Encoding utf8NoBOM
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $freezeAfterPath).Hash -ne $freezeSha) { throw 'closure bytes changed after freeze' }
$actualUntrackedAfter = @(git ls-files --others --exclude-standard | ForEach-Object { $_.Replace('\','/') } | Sort-Object)
if ($LASTEXITCODE -ne 0) { throw 'post-ledger untracked inventory failed' }
if (Compare-Object $expectedUntracked $actualUntrackedAfter) { throw 'nonignored untracked set changed after ledger work' }
$postClosureHead = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $postClosureHead -ne $evidenceSha) { throw 'HEAD changed after closure' }
```

- [ ] **Step 7: Publish and integrate only exact verified `E`**

```powershell
$branch = 'codex/scientific-integrity-remediation-wave-c-20260811'
& 'C:\Python314\python.exe' $gate validate --cwd . $ledgerPath
if ($LASTEXITCODE -ne 0) { throw 'pre-publication Wave C gate failed' }
git fetch origin
if ($LASTEXITCODE -ne 0) { throw 'pre-publication fetch failed' }
$remoteBefore = (git rev-parse origin/main).Trim()
if ($LASTEXITCODE -ne 0 -or $remoteBefore -notmatch '^[0-9a-f]{40}$') { throw 'origin/main did not resolve to a full SHA' }
git merge-base --is-ancestor $remoteBefore $evidenceSha
if ($LASTEXITCODE -ne 0) { throw 'origin/main advanced outside exact E; rebuild from the new parent' }
git push -u origin "HEAD:refs/heads/$branch"
if ($LASTEXITCODE -ne 0) { throw 'Wave C feature-branch push failed' }
$remoteBranch = ((git ls-remote --heads origin "refs/heads/$branch") -split "`t")[0]
if ($LASTEXITCODE -ne 0 -or $remoteBranch -ne $evidenceSha) { throw 'remote Wave C branch SHA mismatch' }
```

Integrate serially by fast-forward only after the integration coordinator confirms no other lane is active. The integrated tree must remain exact `E`; a merge commit, rebase, conflict edit, source/config/test/candidate/closure change, dependency change, or different final revision invalidates closure. Refetch, verify `origin/main`, local integration, and feature-branch SHA equality, then fast-forward the live checkout only after an incoming/WIP overlap and byte-fingerprint rehearsal. Preserve every live WIP byte, including `uv.lock`.

---

## Acceptance Matrix

| Audit or claim | Required exact-final evidence | Closure state |
|---|---|---|
| `AUD-06` | unsupported settings fail before effects; one system construction; frozen digest truth table and preimages; identity-only gate/run/publish/diagnostic entry points; both digests at every current layer; four views with `high_severity` or exact eight views with both triggers; skeptic and adjudicator | defect `REFUTED`; guard `EVIDENCE_VERIFIED` |
| `AUD-07` | protocol-v3 closed keys; independently observed worker device/dtype/environment-lock/executable/script/library identity; actual-lock mutation control; v1/v2 nonpromotion; controller and worker validation before eligibility | defect `REFUTED`; guard `EVIDENCE_VERIFIED` |
| `AUD-08` | one resolved publication/discovery root; unrelated-CWD load; same-hash old-root decoy rejection; sentinel and confirmatory identities remain distinct | defect `REFUTED`; guard `EVIDENCE_VERIFIED` |
| `AUD-09` | unsupported order/diagnostic options fail before effects; canonical ASCII-sorted nine-entry `VerifiedRunBundle.inventory`; nested Fisher witness; no extra/tenth semantic payload | defect `REFUTED`; guard `EVIDENCE_VERIFIED` |
| `AUD-19` | nonfinite/asymmetric/non-SPD/ill-conditioned controls; required sole Wave A matrix-policy object; no Wave C class definition; bytes-backed arrays | defect `REFUTED`; guard `EVIDENCE_VERIFIED` |
| five-job sentinel protocol | separately accepted fresh exact-`E` gate; explicit CPU-pin removal, exact CUDA visibility check, and CPU-pin restoration; validated v3/v2 identities, counts, settings, parity, and decisions | `EVIDENCE_VERIFIED` only on sentinel branch; otherwise `INCONCLUSIVE` |
| confirmatory equivalence, attraction, universality | claim-specific current eligible experiment evidence beyond the sentinel | `INCONCLUSIVE` in both branches |
| review/ledger structure | exact installed code/experiment domain criteria in aggregate, every view, and every comparison; no generic collapse; every conditional claim has a complete claim-statement/explicit-negation AB/BA grid and one bound adjudicator; its normal branch is exact two-view/no-trigger target 2, while any actual trigger requires the complete 4/8 tier | structural prerequisite for every terminal state |

## Final Self-Review Checklist

- [ ] Tasks 1-7 preserve their scientific semantics and frozen v3/root/digest/nine-payload contracts, with only the binding-review corrections enumerated in those tasks.
- [ ] `MatrixDomainPolicy` is defined only in `multiagent_elbo.conditioning` by Wave A; Wave C imports that class, re-exports only the identical object required by compatibility, and defines `FROZEN_FIXED_RAY_MATRIX_POLICY = MatrixDomainPolicy(min_spd_rcond=1e-12)`.
- [ ] All six gate/run/publish entry points and the diagnostic path consume one `FixedRayExecutionIdentity`; both v2 gates, sentinel publication, and diagnostic publication carry both named digests without raw-config reconstruction or post-validation config mutation.
- [ ] Task 3 and Task 5 file lists, static checks, and staging commands include every modified fixed-ray and diagnostic launcher/test file.
- [ ] Worker `observed` state independently hashes the actual environment lock and process/runtime identities; timing and controller-local provenance are explicitly outside the response-identity claim.
- [ ] The scale-cocycle test reads `VerifiedRunBundle.inventory`, uses canonical ASCII order, requires exactly nine semantic names, and rejects a tenth payload.
- [ ] The generic Wave 0 `run-junit`, immutable preparation, sole publisher, and validators are reused; Wave C has no second runner, environment writer, index writer, or partial publisher.
- [ ] The exact Wave 0 eleven-file generic contract is unchanged; candidate has exactly 15 files; no-CUDA target 4/8 has exactly 36/40 files; sentinel target 4/8 has exactly 41/45 files.
- [ ] The reviewed Wave C plan/last-touch blob, sole Wave A ownership plan/type, exact nine-file verification snapshot at the explicit canonical skill root, and validated Wave 0 terminal plan SHA/ledger/index/closure are bound and live-revalidated without any alternate gate discovery.
- [ ] Candidate raw evidence is ignored and publishes an exact `P/P` bundle; `E` is its direct evidence-only child; closure reruns at exact `E/P`.
- [ ] The environment has exactly six keys and deterministic CPU values; targeted has exactly two allowed skips; subsystem and full each have exactly six.
- [ ] Tested-input, source/config, dependency, and domain inventories are exhaustive; `uv.lock` is not an evidence dependency.
- [ ] The closed review-context payload binds every `E/P`, candidate, raw suite, input, environment, plan/snapshot/Wave0-terminal, CUDA-branch, claim/evidence/criteria/review/path member; every-leaf mutation changes its digest or fails validation.
- [ ] Raw exact-`E` CUDA-branch inputs, authored reviews, skeptics, and adjudicators validate before any closure index or public byte exists; the wrapper never fabricates or synthesizes a view or verdict.
- [ ] Wave 0's total structural privacy transform covers every base/domain JSON/XML path-bearing field, absolute argv/environment component, interpreter, review/result, dependency, and JUnit value; disjoint base/domain maps bind all raw-to-public hashes.
- [ ] The absent closure directory receives one immutable base-plus-domain publication and equals the exact branch-specific untracked set.
- [ ] The default branch performs no CUDA action and records a precise obligation. The optional branch requires a separately accepted fresh gate, temporarily removes the CPU CUDA-visibility pin, verifies the CUDA interpreter/device, restores the pin in `finally`, runs only the five-job sentinel, and never enables or runs the heavy confirmatory sweep.
- [ ] The empty gate template fails validation before explicit population; population consumes indexed reviews/adjudicators byte-for-byte, live-revalidates both indexes and all 14 claims, and never treats either index as claim evidence.
- [ ] Every code/experiment claim uses its complete installed domain criterion map in aggregate, view, and comparison scores; generic `coverage`, `freshness`, or `artifact_bound_correctness` criteria are rejected.
- [ ] Five defect propositions are `REFUTED` with claim-unique counterevidence and `refute` adjudicators; five guards are `EVIDENCE_VERIFIED` with claim-unique evidence and `support` adjudicators; AUD-06 has four views with exact `high_severity` or eight views with both exact triggers plus skeptic/adjudicator.
- [ ] All four conditional claims have complete two-candidate AB/BA/adjudicator contracts; the normal branch is exact two-view/no-trigger target 2, any actual trigger receives the full 4/8 tier, the sentinel claim is conditional, and confirmatory equivalence/attraction/universality remain `INCONCLUSIVE` with abstaining adjudicators and empty fabricated-evidence sets.
- [ ] Every native command has an explicit exit/status guard; no source, test, configuration, tool, candidate, or closure byte changes after its evidence boundary.
