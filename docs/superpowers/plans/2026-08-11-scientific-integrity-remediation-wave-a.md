# Scientific Integrity Remediation Wave A Implementation Plan

> **Binding 2026-08-13 gate-execution supersession.** Any older path-return
> resolver command preserved below records the historical review context only and
> is not executable guidance. Current gate actions must validate the snapshot and
> explicit `.codex` root and execute retained bytes in one safe invocation:
> `C:\Python314\python.exe -B tools\remediation_evidence.py run-verification-gate --snapshot SNAPSHOT --root ROOT -- start ARGS` or
> `C:\Python314\python.exe -B tools\remediation_evidence.py run-verification-gate --snapshot SNAPSHOT --root ROOT -- validate ARGS`.
> Never assign or execute a resolved `$gate` path. Historical JUnit and evidence
> records remain revision-bound history and are not rewritten by this correction.
> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close `AUD-03`, `AUD-13`, `AUD-14`, `AUD-15`, `AUD-16`, `AUD-17`, and `AUD-18` by making probability, KL, symmetric-matrix, Fisher-quotient, recovery, and Fisher-provenance invariants explicit and mechanically enforced.

**Architecture:** One bytes-backed array boundary and one float64 probability canonicalizer establish valid finite inputs before one stable KL reducer runs. The existing conditioning module becomes the sole finite symmetric-matrix policy and owns the single eigensystem consumed by a new immutable Fisher quotient. Recovery is a separate Loewner/relative-loss assessment with an optional exact witness, while the scale experiment binds its Fisher-labeled metric to an exact persisted statistical construction and leaves the legacy arbitrary-bilinear helper explicitly non-Fisher.

**Tech Stack:** Python 3.14, NumPy, SciPy symmetric eigensolvers, `fractions.Fraction`, pytest, JUnit XML, Ruff, Git, the Wave 0 `remediation-evidence-v1` tooling, and the installed verification control plane.

## Global Constraints

- Start only after Wave 0 is merged and its compatibility inventory, status/failure contract, evidence schema, and `tools/remediation_evidence.py` tests pass at the branch base. Base the Wave A branch on that exact merged revision; the approved program design is commit `c43a7c50675cf63b60f7b6cbea9664b638cd4c4e`.
- Use an isolated `codex/` branch/worktree. Fetch first, inspect `origin/main`, and preserve the user's live checkout, uncommitted configuration, launchers, untracked review directory, and `uv.lock` byte-for-byte.
- Use American English. Use explicit `C:\Python314\python.exe` for every command in this plan. Do not import Torch, query CUDA, set the CUDA opt-in to true, run a CUDA-marked test, or make a current CUDA claim.
- Before every CPU evidence run, remove `MULTIAGENTELBO_RUN_CUDA_TESTS` from the environment. The one explicitly opted-out CUDA testcase may remain skipped only if its exact testcase ID/reason appears in the Wave 0 allowlist; no new unexplained skip is accepted.
- `NumericsConfig.atol` and `rtol` remain parser-valid comparison tolerances. They never decide probability membership, symmetry membership, PSD membership, or whether a negative KL is material.
- `FiniteMeasure` remains finite, nonnegative, and intentionally unnormalized. No Wave A code may silently turn it into a probability.
- Structurally invalid inputs fail before an authoritative object, assessment-derived object, run directory, or artifact is returned. A matrix assessment with decision `inconclusive` cannot construct a Gaussian interaction, quotient, or recovery result.
- Every public authoritative array created or changed in this wave is C-contiguous and backed by immutable `bytes`; `array.setflags(write=True)` must raise `ValueError`. Scratch arrays that never escape a calculation may remain mutable.
- Existing constructors and `.masses`/`.matrix` NumPy access remain. The `InformationPoint` constructor fields remain exactly, and in this order, `probability`, `score`, `fisher`, `vfe_gradient`, `natural_gradient`, `fisher_projector`, `rank`, `nullity`, `positive_spectrum_condition_number`, `range_residual`, `inverse_rule`, and `used_pseudoinverse`; quotient assessment is private implementation state and never a required constructor field. Existing `RecoveryDiagnostics` attributes remain available through conservative compatibility properties. No property may call threshold-level recovery exact.
- Every persisted producer record remains `verification_state="CANDIDATE"`. `pass`/`fail`/`inconclusive` are typed numerical decisions, never producer verification promotion.
- Preserve the boundary `global_experiment_recovery_claimed=False`: pointwise Fisher equality or quotient recovery does not prove a global Blackwell recovery kernel or a smooth global statistical quotient.
- Record a RED reproducer at the exact pre-fix task revision, implement the smallest GREEN, run cache-disabled targeted and affected tests, and commit only after GREEN. Never commit a knowingly red test.
- Candidate and closure evidence follow the Wave 0 two-commit protocol exactly. Mathematical closure additionally requires the derivations/exact oracles named in Task 8. Agent agreement is not evidence.

---

## File Responsibility Map

- Create `src/multiagent_elbo/_immutable.py`: the only bytes-backed public-array constructor used by Wave A code.
- Create `src/multiagent_elbo/finite/_probability.py`: the only structural float64 probability canonicalizer.
- Create `src/multiagent_elbo/finite/_kl.py`: the only floating KL term reducer; public and legacy wrappers preserve their existing support-failure carriers.
- Modify `src/multiagent_elbo/finite/measures.py`: strict probability/kernel membership, unnormalized finite measures, immutable results.
- Modify `src/multiagent_elbo/finite/vfe.py`, `src/multiagent_elbo/finite/agent_network.py`, and `src/multiagent_elbo/finite/counterexamples.py`: route every floating KL calculation through the one stable reducer while preserving infinity, finite-only error, and `ExtendedRealKL` support semantics.
- Modify `src/multiagent_elbo/experiment_support.py`, `src/multiagent_elbo/finite/categorical_dqm.py`, `src/multiagent_elbo/finite/fisher.py`, `src/multiagent_elbo/finite/information_history.py`, `src/multiagent_elbo/finite/interactions.py`, and `src/multiagent_elbo/realizations/gaussian/interactions.py`: delegate every authoritative array touched by Wave A to the immutable boundary.
- Modify `src/multiagent_elbo/conditioning.py`: one finite-real-symmetric PSD/SPD assessment plus one immutable quotient constructed from the assessment's eigensystem.
- Modify `src/multiagent_elbo/finite/information_history.py`: constructor-preserving information points computed from a private quotient assessment, plus Loewner/relative-loss recovery diagnostics.
- Modify `src/multiagent_elbo/finite/fisher.py`: own the exact finite Fisher witness used by recovery and scale provenance.
- Modify `src/multiagent_elbo/finite/scale_cocycle.py`: add explicit `bilinear_identity_only` compatibility status; this module does not own or manufacture Fisher provenance.
- Modify `src/multiagent_elbo/finite/scale_cocycle_experiment.py`: derive the active defect from the exact witness and persist its closed record inside the existing `derivative_cocycle.json` semantic payload.
- Modify `src/multiagent_elbo/__init__.py` and `src/multiagent_elbo/finite/__init__.py`: export only the new documented public assessments/witnesses; keep internal canonicalizers private.
- Modify `tests/test_measures.py`, `tests/test_vfe.py`, `tests/test_agent_network.py`, `tests/test_experiment_support.py`, `tests/test_conditioning.py`, `tests/test_gaussian_realization.py`, `tests/test_fisher.py`, `tests/test_information_history.py`, `tests/test_information_history_experiment.py`, `tests/test_interactions.py`, `tests/test_scale_cocycle.py`, `tests/test_scale_cocycle_experiment.py`, `tests/test_shared_scientific_contracts.py`, and `tests/test_counterexamples.py`: RED/GREEN guards and compatibility coverage.
- Create `tools/wave_a_evidence.py` and `tests/test_wave_a_evidence.py`: a wave-specific runner/index adapter over the Wave 0 Python builder; it does not introduce a second generic evidence schema.
- Create only during candidate evidence: `docs/verification/evidence/wave-a/$implementationShort`, where the variable is computed from exact `P`.
- Create only during exact-child closure and do not commit: `verification-evidence/wave-a/$evidenceShort`, `.verification/wave-a/final-ledger.json`, and the repository-global gate marker `.verification/active.json`.

### Task 0: Gate the parent, isolate the branch, and fingerprint live WIP

**Files:**
- Read only: `C:\Users\chris and christine\Desktop\MultiAgentELBO`
- Create worktree: `C:\Users\chris and christine\Documents\ChatGPT\MultiAgentELBO\.superpowers\worktrees\MultiAgentELBO-wave-a-20260811`
- Create branch: `codex/scientific-integrity-remediation-wave-a-20260811`

**Interfaces:**
- The implementation parent is the freshly fetched `origin/main` SHA that contains the approved design commit and all four Wave 0 contract/tool files.
- `Get-WipFingerprint` binds every path reported by Git plus `uv.lock` by repository-relative name, type, size, and SHA-256; it never writes to the live checkout.
- The implementation worktree is clean and independent. No command in this task uses stash, reset, clean, force checkout, or a recursive remove.

- [ ] **Step 1: Load the worktree skill and capture the live checkout before fetching**

At execution time, read the complete `superpowers:using-git-worktrees` skill before running these commands. Then run this exact PowerShell from any directory:

```powershell
$liveRepo = 'C:\Users\chris and christine\Desktop\MultiAgentELBO'
$worktree = 'C:\Users\chris and christine\Documents\ChatGPT\MultiAgentELBO\.superpowers\worktrees\MultiAgentELBO-wave-a-20260811'
$branch = 'codex/scientific-integrity-remediation-wave-a-20260811'
$designSha = 'c43a7c50675cf63b60f7b6cbea9664b638cd4c4e'
$wipBefore = 'C:\tmp\multiagentelbo-wave-a-live-wip-before.json'

function Get-WipFingerprint([string]$Repo) {
    $raw = (& git -C $Repo status --porcelain=v1 -z --untracked-files=all) -join "`n"
    if ($LASTEXITCODE -ne 0) { throw 'live worktree status failed' }
    $paths = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
    foreach ($entry in ($raw -split "`0")) {
        if ([string]::IsNullOrEmpty($entry) -or $entry.Length -lt 4) { continue }
        $candidate = $entry.Substring(3)
        if ($candidate.Contains(' -> ')) { $candidate = $candidate.Split(' -> ')[-1] }
        [void]$paths.Add($candidate.Replace('/', '\'))
    }
    [void]$paths.Add('uv.lock')
    $records = foreach ($relative in ($paths | Sort-Object)) {
        $absolute = Join-Path $Repo $relative
        if (Test-Path -LiteralPath $absolute -PathType Leaf) {
            [ordered]@{
                path = $relative.Replace('\', '/')
                kind = 'file'
                size_bytes = (Get-Item -LiteralPath $absolute).Length
                sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $absolute).Hash.ToLowerInvariant()
            }
        } elseif (Test-Path -LiteralPath $absolute -PathType Container) {
            [ordered]@{path=$relative.Replace('\', '/'); kind='directory'; size_bytes=$null; sha256=$null}
        } else {
            [ordered]@{path=$relative.Replace('\', '/'); kind='absent'; size_bytes=$null; sha256=$null}
        }
    }
    return @($records)
}

Get-WipFingerprint $liveRepo | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $wipBefore -Encoding utf8NoBOM
Get-FileHash -Algorithm SHA256 -LiteralPath $wipBefore
git -C $liveRepo status --short
```

- [ ] **Step 2: Fetch, prove the Wave 0/publication parent, and create the isolated worktree**

```powershell
git -C $liveRepo fetch origin
git -C $liveRepo log -1 --oneline origin/main
$parent = (& git -C $liveRepo rev-parse origin/main).Trim()
git -C $liveRepo merge-base --is-ancestor $designSha $parent
if ($LASTEXITCODE -ne 0) { throw "approved design $designSha is not an ancestor of $parent" }
foreach ($required in @(
    'docs/verification/remediation/audit-disposition-v1.json',
    'docs/verification/remediation/compatibility-inventory-v1.json',
    'docs/verification/remediation/status-failure-contract-v1.json',
    'docs/verification/remediation/remediation-evidence-v1.schema.json',
    'docs/verification/remediation/verification-contract-v1.json',
    'docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md',
    'tools/remediation_evidence.py',
    'tests/test_remediation_contracts.py',
    'tests/test_remediation_evidence.py'
)) {
    git -C $liveRepo cat-file -e "$parent`:$required"
    if ($LASTEXITCODE -ne 0) { throw "Wave 0 dependency missing at $parent`: $required" }
}
if (Test-Path -LiteralPath $worktree) { throw "worktree path already exists: $worktree" }
git -C $liveRepo show-ref --verify --quiet "refs/heads/$branch"
if ($LASTEXITCODE -eq 0) { throw "branch already exists: $branch" }
git -C $liveRepo worktree add -b $branch $worktree $parent
git -C $worktree rev-parse HEAD
git -C $worktree status --porcelain=v1
if ((& git -C $worktree rev-parse HEAD).Trim() -ne $parent) { throw 'worktree parent drift' }
if ((& git -C $worktree status --porcelain=v1)) { throw 'new Wave A worktree is not clean' }
$wave0PlanPath = 'docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md'
$expectedWave0PlanSha256 = 'dbe2263a3b0fe1e9f5db4ff1fca9a19f819cfd32ef38da71d6e5cb5485723ac2'
$wave0PlanAbsolute = Join-Path $worktree $wave0PlanPath
if (-not (Test-Path -LiteralPath $wave0PlanAbsolute -PathType Leaf)) { throw 'frozen Wave 0 PASS plan is missing' }
$observedWave0PlanSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $wave0PlanAbsolute).Hash.ToLowerInvariant()
if ($observedWave0PlanSha256 -ne $expectedWave0PlanSha256) { throw "Wave 0 PASS plan hash drift: $observedWave0PlanSha256" }
$trackedWave0Plan = (& git -C $worktree ls-files --error-unmatch -- $wave0PlanPath).Trim()
if ($LASTEXITCODE -ne 0 -or $trackedWave0Plan -ne $wave0PlanPath) { throw 'Wave 0 PASS plan is not the exact tracked path' }
```

- [ ] **Step 3: Prove the parent contracts and preserve the WIP baseline**

```powershell
Push-Location $worktree
try {
    Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
    C:\Python314\python.exe -B -m pytest tests\test_remediation_contracts.py tests\test_remediation_evidence.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task0-wave0 --junitxml=C:\tmp\multiagentelbo-wave-a-task0-wave0.xml
    if ($LASTEXITCODE -ne 0) { throw 'Wave 0 parent gate failed' }
    $snapshot = 'docs/verification/remediation/verification-contract-v1.json'
    $verificationRoot = 'C:\Users\chris and christine\.codex\skills\verification'
} finally {
    Pop-Location
}
[xml]$task0 = Get-Content -Raw -LiteralPath 'C:\tmp\multiagentelbo-wave-a-task0-wave0.xml'
$task0Suites = @($task0.testsuites.testsuite)
$task0Failures = ($task0Suites | Measure-Object -Property failures -Sum).Sum
$task0Errors = ($task0Suites | Measure-Object -Property errors -Sum).Sum
if ([int]$task0Failures -ne 0 -or [int]$task0Errors -ne 0) { throw 'Wave 0 JUnit is not green' }
$wipBeforeSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $wipBefore).Hash
Set-Content -LiteralPath 'C:\tmp\multiagentelbo-wave-a-wip-before.sha256' -Value $wipBeforeSha -Encoding ascii
```

Expected: Wave 0 is present and green at the exact fetched parent, its reviewed
PASS plan is the exact tracked path with SHA-256
`dbe2263a3b0fe1e9f5db4ff1fca9a19f819cfd32ef38da71d6e5cb5485723ac2`,
the isolated worktree is clean, and the live checkout remains untouched.

### Task 1: Establish immutable storage and structural probability membership (`AUD-03`, `AUD-13`)

**Files:**
- Create: `src/multiagent_elbo/_immutable.py`
- Create: `src/multiagent_elbo/finite/_probability.py`
- Modify: `src/multiagent_elbo/finite/measures.py`
- Modify: `src/multiagent_elbo/experiment_support.py`
- Modify: `tests/test_measures.py`
- Modify: `tests/test_experiment_support.py`

**Interfaces:**
- Private `immutable_array(values: object, *, dtype: object | None = np.float64) -> np.ndarray` copies once into C order, rejects object dtype, serializes to immutable bytes, and reconstructs the original dtype/shape over that byte buffer.
- Private `canonical_probability_array(values: object, *, field: str, expected_shape: tuple[int, ...] | None = None) -> np.ndarray` applies the exact `math.fsum`/`8*n*eps` policy to the flattened input.
- `ProbabilityMeasure(...)`, `MarkovKernel(...)`, `FiniteMeasure(...)`, `MeasurePair.evidence_density()`, and `BlockUpdateResult.outside_marginal` retain NumPy-facing access but cannot be made writable again.

- [ ] **Step 1: Add the loose-tolerance, exact-sum, caller-mutation, and immutable-backing RED tests**

Add these concrete tests; use a direct `NumericsConfig` so the reproducer proves that parser-valid comparison tolerances have no structural authority:

```python
LOOSE = NumericsConfig(dtype="float64", atol=0.9, rtol=0.9)


@pytest.mark.parametrize("masses", [(0.0, 0.0), (0.4, 0.4)])
def test_probability_membership_ignores_loose_comparison_tolerances(masses):
    with pytest.raises(ValueError, match="sum to one"):
        ProbabilityMeasure(("x", "y"), masses, LOOSE)


def test_zero_markov_row_is_rejected_under_loose_tolerances():
    with pytest.raises(ValueError, match=r"row 1.*sum to one"):
        MarkovKernel(
            ("x", "y"), ("z",), ((1.0,), (0.0,)), LOOSE
        )


def test_probability_is_exactly_canonical_and_bytes_backed():
    eps = np.finfo(np.float64).eps
    source = np.array([0.1, 0.2, 0.7 + eps])
    law = ProbabilityMeasure(("a", "b", "c"), source, LOOSE)
    source[:] = (1.0, 0.0, 0.0)
    assert math.fsum(float(x) for x in law.masses) == 1.0
    assert law.masses.dtype == np.float64
    assert law.masses.flags.c_contiguous
    with pytest.raises(ValueError, match="WRITEABLE"):
        law.masses.setflags(write=True)


def test_finite_measure_stays_unnormalized_but_bytes_backed():
    measure = FiniteMeasure(("x", "y"), (0.4, 0.4), LOOSE)
    assert measure.total_mass == pytest.approx(0.8)
    with pytest.raises(ValueError, match="WRITEABLE"):
        measure.masses.setflags(write=True)


@pytest.mark.parametrize("bad", [(True, 0.0), (np.nan, 1.0), (-0.1, 1.1)])
def test_probability_rejects_boolean_nonfinite_and_negative_entries(bad):
    with pytest.raises((TypeError, ValueError)):
        ProbabilityMeasure(("x", "y"), bad, LOOSE)
```

Extend `tests/test_experiment_support.py::test_readonly_array_copies_and_freezes_values` with a `setflags(write=True)` failure, not merely `flags.writeable is False`.

- [ ] **Step 2: Run the focused RED at the exact pre-fix revision**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_measures.py tests\test_experiment_support.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task1-red --junitxml=C:\tmp\multiagentelbo-wave-a-task1-red.xml
```

Expected: FAIL because `(0,0)`, total `0.8`, and a zero kernel row are accepted under `LOOSE`, and current public arrays can re-enable `WRITEABLE`.

- [ ] **Step 3: Implement the one immutable boundary and one structural canonicalizer**

Use this implementation shape; do not substitute `np.sum`, `np.isclose`, `np.allclose`, configured tolerances, or `setflags(write=False)`:

```python
# src/multiagent_elbo/_immutable.py
def immutable_array(values: object, *, dtype: object | None = np.float64) -> np.ndarray:
    owned = np.array(values, dtype=dtype, copy=True, order="C")
    if owned.dtype.hasobject:
        raise TypeError("authoritative arrays must not have object dtype")
    backing = owned.tobytes(order="C")
    return np.frombuffer(backing, dtype=owned.dtype).reshape(owned.shape)


# src/multiagent_elbo/finite/_probability.py
def canonical_probability_array(
    values: object,
    *,
    field: str,
    expected_shape: tuple[int, ...] | None = None,
) -> np.ndarray:
    raw = np.asarray(values, dtype=object)
    if any(isinstance(value, (bool, np.bool_)) for value in raw.flat):
        raise TypeError(f"{field} must not contain Boolean values")
    try:
        owned = np.array(values, dtype=np.float64, copy=True, order="C")
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError(f"{field} must contain numeric values") from error
    if expected_shape is not None and owned.shape != expected_shape:
        raise ValueError(f"{field} has the wrong shape")
    if owned.size == 0 or not np.all(np.isfinite(owned)) or np.any(owned < 0.0):
        raise ValueError(f"{field} must be finite and nonnegative")
    flat = owned.reshape(-1)
    total = math.fsum(float(value) for value in flat)
    tolerance = 8.0 * flat.size * np.finfo(np.float64).eps
    if total <= 0.0 or abs(total - 1.0) > tolerance:
        raise ValueError(f"{field} must sum to one")
    normalized = flat / total
    correction_index = int(np.argmax(normalized))
    normalized[correction_index] += 1.0 - math.fsum(
        float(value) for value in normalized
    )
    if (
        not np.all(np.isfinite(normalized))
        or np.any(normalized < 0.0)
        or math.fsum(float(value) for value in normalized) != 1.0
    ):
        raise ArithmeticError(f"{field} canonicalization failed")
    return immutable_array(normalized.reshape(owned.shape), dtype=np.float64)
```

In `ProbabilityMeasure`, canonicalize the vector directly rather than validating an already-created `FiniteMeasure`. In `MarkovKernel`, canonicalize each row independently, include the row index in `field`, stack the canonical rows, and freeze the final matrix over bytes. In `FiniteMeasure`, retain only finite/nonnegative validation and use `immutable_array` without normalizing. Make `total_mass` use `math.fsum`.

Delegate `experiment_support.readonly_array` to `immutable_array`; it stays public with the same positional `values, dtype` signature.

- [ ] **Step 4: Run GREEN, static checks, and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_measures.py tests\test_experiment_support.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task1-green --junitxml=C:\tmp\multiagentelbo-wave-a-task1-green.xml
[xml]$task1 = Get-Content -Raw -LiteralPath 'C:\\tmp\\multiagentelbo-wave-a-task1-green.xml'
$task1Suites = @($task1.testsuites.testsuite)
if ([int](($task1Suites | Measure-Object failures -Sum).Sum) -ne 0 -or [int](($task1Suites | Measure-Object errors -Sum).Sum) -ne 0) { throw 'Task 1 JUnit is not green' }
C:\Python314\python.exe -m ruff check --no-cache src/multiagent_elbo/_immutable.py src/multiagent_elbo/finite/_probability.py src/multiagent_elbo/finite/measures.py src/multiagent_elbo/experiment_support.py tests/test_measures.py tests/test_experiment_support.py
C:\Python314\python.exe -m ruff format --check --no-cache src/multiagent_elbo/_immutable.py src/multiagent_elbo/finite/_probability.py src/multiagent_elbo/finite/measures.py src/multiagent_elbo/experiment_support.py tests/test_measures.py tests/test_experiment_support.py
git add -- src/multiagent_elbo/_immutable.py src/multiagent_elbo/finite/_probability.py src/multiagent_elbo/finite/measures.py src/multiagent_elbo/experiment_support.py tests/test_measures.py tests/test_experiment_support.py
git commit -m "fix: enforce structural probability membership"
```

### Task 2: Route probability tables and information inputs through the same boundary (`AUD-03`, `AUD-13`)

**Files:**
- Modify: `src/multiagent_elbo/finite/vfe.py`
- Modify: `src/multiagent_elbo/finite/categorical_dqm.py`
- Modify: `src/multiagent_elbo/finite/fisher.py`
- Modify: `src/multiagent_elbo/finite/information_history.py`
- Modify: `src/multiagent_elbo/finite/interactions.py`
- Modify: `src/multiagent_elbo/realizations/gaussian/interactions.py`
- Modify: `tests/test_vfe.py`
- Modify: `tests/test_information_history.py`
- Modify: `tests/test_interactions.py`
- Modify: `tests/test_fisher.py`
- Modify: `tests/test_gaussian_realization.py`

**Interfaces:**
- `_probability_table(values, name)` canonicalizes the flattened table, restores the exact input shape, and returns immutable float64 storage.
- `_positive_probability(values, expected_size, numerics)` uses structural canonicalization first and applies strict positivity second; `numerics` remains accepted for source compatibility but has no membership authority.
- Every row of `ProbabilityCoordinateConfigurationMap.probability_matrix` uses the same structural canonicalizer.
- Local `_readonly` helpers in Wave A-touched modules delegate to `immutable_array`; there is no second storage implementation.

- [ ] **Step 1: Add cross-consumer RED tests**

```python
# tests/test_vfe.py already imports NumPy and pytest.
@pytest.mark.parametrize("bad_total", [0.0, 0.8])
def test_block_probability_tables_reject_invalid_totals(bad_total):
    posterior = np.array([[bad_total, 0.0], [0.0, 0.0]])
    valid = np.array([[0.25, 0.25], [0.25, 0.25]])
    with pytest.raises(ValueError, match="posterior must sum to one"):
        block_update_decomposition(posterior, valid, valid, block_axes=(0,))


# tests/test_information_history.py: add this constant and make the existing
# helper accept the explicit numerics fixture without changing existing calls.
LOOSE = NumericsConfig(dtype="float64", atol=0.9, rtol=0.9)


def _three_category_family(
    *, numerics: NumericsConfig = NUMERICS
) -> CategoricalExponentialFamily:
    return CategoricalExponentialFamily(
        ("x0", "x1", "x2"),
        (0.0, 0.0, 0.0),
        ((1.0, 0.0), (0.0, 1.0), (0.0, 0.0)),
        numerics,
    )


def test_information_target_ignores_loose_tolerances_and_positive_chart_rejects_zero():
    module = _sut()
    family = _three_category_family(numerics=LOOSE)
    with pytest.raises(ValueError, match="target_probability must sum to one"):
        module.categorical_information_point(
            family, (0.0, 0.0), (0.4, 0.4, 0.0), rcond=1e-12
        )
    with pytest.raises(ValueError, match="strictly positive"):
        module.categorical_information_point(
            family, (0.0, 0.0), (0.5, 0.5, 0.0), rcond=1e-12
        )


def test_probability_coordinate_rows_reject_zero_and_point_eight_under_loose_tolerances():
    module = _sut()
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    model = module.build_information_history_model(payload, LOOSE)
    invalid = np.array([[0.4, 0.4, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]])
    with pytest.raises(ValueError, match=r"row 0.*sum to one"):
        module.ProbabilityCoordinateConfigurationMap(
            model.fine_family, model.coarse_family, invalid
        )


# Add this local helper to each of tests/test_vfe.py, tests/test_fisher.py,
# tests/test_information_history.py, tests/test_interactions.py, and
# tests/test_gaussian_realization.py; NumPy and pytest are already imported.
def assert_bytes_backed(array: np.ndarray) -> None:
    assert array.flags.c_contiguous
    with pytest.raises(ValueError, match="WRITEABLE"):
        array.setflags(write=True)
```

Make the required calls literal. In
`test_block_update_supports_multiple_noncontiguous_block_axes`, append:

```python
assert_bytes_backed(result.outside_marginal)
```

In `test_result_arrays_are_read_only_defensive_copies`, replace the
`assert not array.flags.writeable` assertion inside its existing result-array
loop with:

```python
assert_bytes_backed(array)
```

In
`test_information_point_matches_independent_score_fisher_and_vfe_oracles`,
append:

```python
for array in (
    point.probability,
    point.score,
    point.fisher,
    point.vfe_gradient,
    point.natural_gradient,
    point.fisher_projector,
):
    assert_bytes_backed(array)
```

In `test_default_history_has_separate_orbit_rg_duration_and_nonzero_defect_records`,
replace its writeability-only generator assertion with:

```python
for array in history.semantic_arrays():
    assert_bytes_backed(array)
```

In `test_interaction_results_are_read_only_defensive_copies`, call the helper
inside the existing loop over decomposition/projection arrays:

```python
assert_bytes_backed(array)
```

In `test_interaction_and_partition_inputs_are_defensively_owned`, replace the
two writeability-only assertions with:

```python
assert_bytes_backed(interaction.precision)
assert_bytes_backed(result.precision)
```

Keep every existing caller-mutation assertion and element-assignment failure.

- [ ] **Step 2: Run focused RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_vfe.py tests\test_information_history.py tests\test_interactions.py tests\test_fisher.py tests\test_gaussian_realization.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task2-red --junitxml=C:\tmp\multiagentelbo-wave-a-task2-red.xml
```

Expected: FAIL because table and information-row membership still uses tolerant sums, and several authoritative arrays can re-enable writing.

- [ ] **Step 3: Replace every Wave A-local read-only helper and migrate probability consumers**

Implement `_probability_table` exactly as shape-preserving flattened canonicalization:

```python
def _probability_table(values: Sequence[object], name: str) -> np.ndarray:
    raw = np.asarray(values, dtype=object)
    if raw.ndim == 0:
        raise ValueError(f"{name} must be a nonempty probability table")
    return canonical_probability_array(
        values, field=name, expected_shape=tuple(raw.shape)
    ).reshape(raw.shape)
```

Implement the positive chart in this order:

```python
def _positive_probability(values, expected_size, numerics):
    del numerics
    probability = canonical_probability_array(
        values,
        field="target_probability",
        expected_shape=(expected_size,),
    )
    if np.any(probability <= 0.0):
        raise ValueError("target_probability must be strictly positive")
    return probability
```

For `ProbabilityCoordinateConfigurationMap`, canonicalize each row with field `probability_matrix row {index}`, stack, and freeze. Replace local `setflags(write=False)` helpers in every file listed for this task with delegation to `immutable_array`; do not change scratch arrays.

- [ ] **Step 4: Run GREEN and the affected finite/Gaussian interaction suite**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_vfe.py tests\test_fisher.py tests\test_information_history.py tests\test_information_history_experiment.py tests\test_interactions.py tests\test_gaussian_realization.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task2-green --junitxml=C:\tmp\multiagentelbo-wave-a-task2-green.xml
[xml]$task2 = Get-Content -Raw -LiteralPath 'C:\\tmp\\multiagentelbo-wave-a-task2-green.xml'
$task2Suites = @($task2.testsuites.testsuite)
if ([int](($task2Suites | Measure-Object failures -Sum).Sum) -ne 0 -or [int](($task2Suites | Measure-Object errors -Sum).Sum) -ne 0) { throw 'Task 2 JUnit is not green' }
git add -- src/multiagent_elbo/finite/vfe.py src/multiagent_elbo/finite/categorical_dqm.py src/multiagent_elbo/finite/fisher.py src/multiagent_elbo/finite/information_history.py src/multiagent_elbo/finite/interactions.py src/multiagent_elbo/realizations/gaussian/interactions.py tests/test_vfe.py tests/test_information_history.py tests/test_interactions.py tests/test_fisher.py tests/test_gaussian_realization.py
git commit -m "fix: share probability and immutable array contracts"
```

### Task 3: Replace every floating KL path with one stable reducer (`AUD-18`)

**Files:**
- Create: `src/multiagent_elbo/finite/_kl.py`
- Modify: `src/multiagent_elbo/finite/vfe.py`
- Modify: `src/multiagent_elbo/finite/agent_network.py`
- Modify: `src/multiagent_elbo/finite/counterexamples.py`
- Modify: `tests/test_vfe.py`
- Modify: `tests/test_agent_network.py`
- Modify: `tests/test_counterexamples.py`

**Interfaces:**
- Private immutable `StableKlReduction(value: float, support_violations: tuple[int, ...])` and `stable_kl_reduce(q: Sequence[object], p: Sequence[object]) -> StableKlReduction` in `finite._kl` are the sole floating term reducer.
- `vfe._kl_arrays(q, p) -> tuple[float, int | None]` remains as a thin compatibility wrapper returning infinity plus the first offending index; `counterexamples.kl_divergence` preserves the full `ExtendedRealKL.support_violations`; the exact-application helpers in `agent_network` preserve their finite-only `ValueError` branches.
- Ordinary, coarse, reverse-conditional, weighted-conditional, block-update, global-VFE, local/collective, overlapping-objective, and exact-counterexample KL paths call the shared reducer. Every outer weighted or repeated sum uses `math.fsum`.
- The nonconfigurable bound is `64*n*eps*max(1, math.fsum(abs(term)))`; no configured tolerance enters it.

- [ ] **Step 1: Add exact support, cancellation, and material-negative RED tests**

```python
# tests/test_vfe.py: add beside the existing imports.
import multiagent_elbo.finite.vfe as vfe_module


def test_stable_kl_clamps_only_machine_scale_negative_cancellation():
    q = ProbabilityMeasure(
        ("x", "y"),
        (0.48748304799535896, 0.5125169520046411),
        NUMERICS,
    )
    p = ProbabilityMeasure(
        ("x", "y"),
        (0.48748304799535885, 0.5125169520046412),
        NUMERICS,
    )
    assert kl_divergence(q, p) == 0.0


def test_stable_kl_preserves_extended_real_support_semantics():
    q = ProbabilityMeasure(("x", "y"), (1.0, 0.0), NUMERICS)
    p = ProbabilityMeasure(("x", "y"), (0.0, 1.0), NUMERICS)
    assert kl_divergence(q, p) == math.inf


def test_stable_kl_rejects_material_negative_internal_input():
    with pytest.raises(ArithmeticError, match="materially negative KL"):
        vfe_module._kl_arrays(
            np.array([0.4, 0.4]), np.array([0.5, 0.5])
        )


def test_block_update_kl_operands_are_nonnegative_before_differencing():
    posterior = np.array([[0.10, 0.20], [0.30, 0.40]])
    q_before = np.array([[0.21, 0.13], [0.14, 0.52]])
    q_after = np.array([[0.14, 0.325], [0.21, 0.325]])
    outside = q_before.sum(axis=0)
    posterior_conditionals = posterior / posterior.sum(axis=0, keepdims=True)
    before_conditionals = q_before / outside[np.newaxis, :]
    after_conditionals = q_after / outside[np.newaxis, :]

    before_collective, _ = vfe_module._kl_arrays(
        q_before.reshape(-1), posterior.reshape(-1)
    )
    after_collective, _ = vfe_module._kl_arrays(
        q_after.reshape(-1), posterior.reshape(-1)
    )
    before_local_terms = [
        vfe_module._kl_arrays(
            before_conditionals[:, index], posterior_conditionals[:, index]
        )[0]
        for index in range(outside.size)
    ]
    after_local_terms = [
        vfe_module._kl_arrays(
            after_conditionals[:, index], posterior_conditionals[:, index]
        )[0]
        for index in range(outside.size)
    ]

    assert before_collective >= 0.0
    assert after_collective >= 0.0
    assert all(value >= 0.0 for value in before_local_terms)
    assert all(value >= 0.0 for value in after_local_terms)
    result = block_update_decomposition(
        posterior, q_before, q_after, block_axes=(0,)
    )
    assert result.collective_difference == pytest.approx(
        after_collective - before_collective
    )
    assert result.local_difference == pytest.approx(
        math.fsum(
            outside[index]
            * (after_local_terms[index] - before_local_terms[index])
            for index in range(outside.size)
        )
    )
```

Retain the existing smallest-positive-subnormal test unchanged.

In each of `tests/test_vfe.py`, `tests/test_agent_network.py`, and
`tests/test_counterexamples.py`, monkeypatch
`multiagent_elbo.finite._kl.stable_kl_reduce` with a recording wrapper, invoke
every named consumer in this task's Interfaces block, and assert the call count
increases after each invocation. Consumers import the `_kl` module and call
`kl_module.stable_kl_reduce` so this is a runtime-reachability test, not a
detached imported binding. Use the existing normalized two-state float and
`Fraction` fixtures; do not synthesize malformed inputs for this routing test.
Also add literal controls named
`test_agent_network_finite_only_support_error_is_preserved` and
`test_counterexample_kl_preserves_all_support_violations`. The first calls
`agent_network_module._kl((Fraction(1), Fraction(0)),
(Fraction(0), Fraction(1)))` and requires the existing finite-only `ValueError`.
The second computes counterexample KL from
`ExactLaw((Fraction(1, 2), Fraction(1, 2), Fraction(0)))` to
`ExactLaw((Fraction(0), Fraction(0), Fraction(1)))` and requires exactly
`ExtendedRealKL(True, None, (0, 1))`.

- [ ] **Step 2: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_vfe.py tests\test_agent_network.py tests\test_counterexamples.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task3-red --junitxml=C:\tmp\multiagentelbo-wave-a-task3-red.xml
```

Expected: FAIL because the cancellation fixture returns a small negative value and the internal malformed fixture returns a material negative instead of raising.

- [ ] **Step 3: Implement the stable reducer and route all accumulations through it**

The following first definition belongs in `src/multiagent_elbo/finite/_kl.py`;
the compatibility wrapper at the end belongs in `finite/vfe.py`.

```python
@dataclass(frozen=True)
class StableKlReduction:
    value: float
    support_violations: tuple[int, ...]


def stable_kl_reduce(
    q: Sequence[object], p: Sequence[object]
) -> StableKlReduction:
    q_values = tuple(q)
    p_values = tuple(p)
    if len(q_values) != len(p_values):
        raise ValueError('KL laws must have matching support')
    violations = tuple(
        index
        for index, (q_value, p_value) in enumerate(
            zip(q_values, p_values, strict=True)
        )
        if q_value > 0 and p_value == 0
    )
    if violations:
        return StableKlReduction(math.inf, violations)
    terms = []
    for q_value, p_value in zip(q_values, p_values, strict=True):
        if q_value == 0:
            continue
        q_float = float(q_value)
        if isinstance(q_value, Fraction) and isinstance(p_value, Fraction):
            log_ratio = math.log(float(q_value / p_value))
        else:
            log_ratio = math.log(q_float) - math.log(float(p_value))
        terms.append(q_float * log_ratio)
    divergence = math.fsum(terms)
    bound = (
        64.0
        * len(q_values)
        * np.finfo(np.float64).eps
        * max(1.0, math.fsum(abs(term) for term in terms))
    )
    if divergence < -bound:
        raise ArithmeticError('materially negative KL divergence')
    return StableKlReduction(max(0.0, divergence), ())


def _kl_arrays(q: np.ndarray, p: np.ndarray) -> tuple[float, int | None]:
    if q.shape != p.shape:
        raise ValueError("KL arrays must have matching shapes")
    reduced = kl_module.stable_kl_reduce(q.flat, p.flat)
    first = reduced.support_violations[0] if reduced.support_violations else None
    return reduced.value, first
```

Import `dataclass`, `Fraction`, `math`, `Sequence`, and NumPy in
`finite._kl` exactly as used above. Replace the loops at the current
`agent_network.py` sites around lines 498--508, 523--536, and 569--594 with
calls to the shared reducer. The direct global-VFE term reduces `q` against the
normalized posterior and then subtracts `log(evidence)`; it does not retain a
second independent log-sum. Conditional calls form their conditional laws and
pass them to the reducer, then use `math.fsum` for outer weights. Replace the
current `sum(...)` at `counterexamples.py:306--312` with the reducer and
construct `ExtendedRealKL(True, None, reduction.support_violations)` on support
failure or `ExtendedRealKL(False, reduction.value, ())` otherwise.

Accumulate `vfe._conditional_kl` and `vfe._weighted_conditional_kl` into lists
of `float(weight) * divergence`, then return `math.fsum`. Do the same for the
outer local-objective sum at `agent_network.py:640`. Do not clamp VFE
differences or chain-rule residuals; only KL values receive this documented
bound. Add a source-level regression that parses all three modules and rejects
any floating KL term loop outside `finite._kl`; the exact `Fraction` probability
normalizers remain exact and are not part of this prohibition.

- [ ] **Step 4: Run GREEN and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_vfe.py tests\test_measures.py tests\test_agent_network.py tests\test_counterexamples.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task3-green --junitxml=C:\tmp\multiagentelbo-wave-a-task3-green.xml
[xml]$task3 = Get-Content -Raw -LiteralPath 'C:\\tmp\\multiagentelbo-wave-a-task3-green.xml'
$task3Suites = @($task3.testsuites.testsuite)
if ([int](($task3Suites | Measure-Object failures -Sum).Sum) -ne 0 -or [int](($task3Suites | Measure-Object errors -Sum).Sum) -ne 0) { throw 'Task 3 JUnit is not green' }
git add -- src/multiagent_elbo/finite/_kl.py src/multiagent_elbo/finite/vfe.py src/multiagent_elbo/finite/agent_network.py src/multiagent_elbo/finite/counterexamples.py tests/test_vfe.py tests/test_agent_network.py tests/test_counterexamples.py
git commit -m "fix: stabilize finite KL accumulation"
```

### Task 4: Make the existing conditioning module the sole PSD/SPD policy (`AUD-14`)

**Files:**
- Modify: `src/multiagent_elbo/conditioning.py`
- Modify: `src/multiagent_elbo/__init__.py`
- Modify: `src/multiagent_elbo/realizations/gaussian/interactions.py`
- Modify: `src/multiagent_elbo/finite/fisher.py`
- Modify: `src/multiagent_elbo/finite/counterexamples.py`
- Modify: `tests/test_conditioning.py`
- Modify: `tests/test_gaussian_realization.py`
- Modify: `tests/test_fisher.py`
- Modify: `tests/test_counterexamples.py`
- Modify: `tests/test_shared_scientific_contracts.py`

**Interfaces:**
- Public frozen `MatrixDomainPolicy(min_spd_rcond: float)` is defined only in
  `multiagent_elbo.conditioning`. It rejects Boolean and non-real inputs, stores
  a finite float, and requires `0 < min_spd_rcond < 1`. Wave C imports and
  re-exports this exact class object; no Gaussian module defines a second type.
- Public `assess_symmetric_matrix(matrix, *, requirement, min_rcond=None, atol=0.0, rtol=0.0) -> SpectralConditioningAssessment` is the one implementation.
- Existing `assess_spectral_spd(matrix, *, min_rcond, atol, rtol)` remains and delegates with `requirement="spd"`.
- Public `assess_spectral_psd(matrix) -> SpectralConditioningAssessment` delegates with `requirement="psd"` and has no user tolerance parameters.
- `SpectralConditioningAssessment` records immutable symmetrized matrix, immutable eigenvalues/eigenvectors, normalized symmetry residual/band, spectral scale, machine uncertainty, extrema, reciprocal condition, optional threshold, boundary tolerance, decision, and reason.

- [ ] **Step 1: Add the tri-state and tolerance-independence RED tests**

```python
def test_psd_policy_has_machine_scale_pass_inconclusive_fail_states():
    passed = conditioning.assess_spectral_psd(np.diag([1.0, 0.0]))
    uncertain = conditioning.assess_spectral_psd(np.diag([1.0, -1.0e-15]))
    failed = conditioning.assess_spectral_psd(np.diag([1.0e6, -1.0e-5]))
    assert passed.decision == "pass"
    assert uncertain.decision == "inconclusive"
    assert failed.decision == "fail"
    assert failed.minimum_eigenvalue < -failed.machine_uncertainty


@pytest.mark.parametrize(
    "value,error",
    [
        (True, TypeError),
        ("1e-12", TypeError),
        (0.0, ValueError),
        (1.0, ValueError),
        (math.inf, ValueError),
    ],
)
def test_matrix_domain_policy_has_one_strict_public_definition(value, error):
    with pytest.raises(error):
        conditioning.MatrixDomainPolicy(min_spd_rcond=value)
    assert (
        conditioning.MatrixDomainPolicy.__module__
        == "multiagent_elbo.conditioning"
    )


def test_matrix_domain_policy_normalizes_a_valid_real():
    policy = conditioning.MatrixDomainPolicy(min_spd_rcond=np.float64(1e-12))
    assert type(policy.min_spd_rcond) is float
    assert policy.min_spd_rcond == 1e-12


def test_user_tolerances_cannot_license_asymmetry_or_negative_curvature():
    matrix = np.array([[1.0e6, 1.0], [0.0, -1.0e-5]])
    assessment = conditioning.assess_symmetric_matrix(
        matrix,
        requirement="psd",
        atol=1.0e9,
        rtol=1.0e9,
    )
    assert assessment.decision == "fail"
    assert assessment.symmetry_residual > assessment.symmetry_uncertainty


def test_in_band_asymmetry_is_recorded_and_symmetrized():
    eps = np.finfo(np.float64).eps
    matrix = np.array([[1.0, eps], [0.0, 1.0]])
    assessment = conditioning.assess_spectral_psd(matrix)
    assert assessment.decision == "pass"
    assert assessment.symmetry_residual > 0.0
    np.testing.assert_array_equal(
        assessment.symmetric_matrix, 0.5 * (matrix + matrix.T)
    )


def test_zero_spectrum_spd_is_a_fail_decision():
    result = conditioning.assess_symmetric_matrix(
        np.diag([1.0, 0.0]),
        requirement="spd",
        min_rcond=1.0e-12,
        atol=0.0,
        rtol=0.0,
    )
    assert result.decision == "fail"
    assert result.minimum_eigenvalue == 0.0


@pytest.mark.parametrize("matrix", [np.array([[np.inf]]), np.ones((2, 3))])
def test_matrix_assessment_rejects_nonfinite_or_nonsquare_before_decision(matrix):
    with pytest.raises(ValueError, match="finite|square"):
        conditioning.assess_spectral_psd(matrix)
```

Add this literal test to `tests/test_gaussian_realization.py`; all names are
already imported there:

```python
def test_gaussian_negative_edge_mode_fails_before_interaction_construction():
    edge = np.diag([1.0e6, -1.0e-5])
    with pytest.raises(GaussianNumericalError, match="positive semidefinite"):
        GaussianInteraction.from_self_and_edges(
            (np.eye(2), np.eye(2)), {(0, 1): edge}, NUMERICS
        )
```

- [ ] **Step 2: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_conditioning.py tests\test_gaussian_realization.py tests\test_fisher.py tests\test_counterexamples.py tests\test_shared_scientific_contracts.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task4-red --junitxml=C:\tmp\multiagentelbo-wave-a-task4-red.xml
```

Expected: FAIL because no PSD assessment exists and Gaussian PSD membership uses configured norm-scaled tolerances.

- [ ] **Step 3: Extend the existing assessment using one `scipy.linalg.eigh` call**

Define the sole public policy before the assessment types:

```python
@dataclass(frozen=True)
class MatrixDomainPolicy:
    min_spd_rcond: float

    def __post_init__(self) -> None:
        value = self.min_spd_rcond
        if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real):
            raise TypeError("min_spd_rcond must be a non-Boolean real")
        normalized = float(value)
        if not math.isfinite(normalized) or not 0.0 < normalized < 1.0:
            raise ValueError("min_spd_rcond must be finite and in (0, 1)")
        object.__setattr__(self, "min_spd_rcond", normalized)
```

Import `Real` from `numbers`. No other module may declare a class named
`MatrixDomainPolicy`. `assess_spectral_spd` accepts the scalar value as before;
Wave C will pass `domain_policy.min_spd_rcond` and re-export this class object.

Use these exact bands:

```python
raw_scale = max(1.0, float(np.max(np.abs(values))))
symmetry_residual = float(np.max(np.abs(values - values.T))) / raw_scale
symmetry_uncertainty = 64.0 * n * np.finfo(np.float64).eps
symmetric = 0.5 * (values + values.T)
eigenvalues, eigenvectors = scipy.linalg.eigh(symmetric, check_finite=True)
spectral_scale = float(np.max(np.abs(eigenvalues)))
machine_uncertainty = (
    64.0 * n * np.finfo(np.float64).eps * max(1.0, spectral_scale)
)
```

Decision precedence is fixed:

1. symmetry residual above `symmetry_uncertainty` is `fail`;
2. minimum eigenvalue below `-machine_uncertainty` is `fail`;
3. minimum in `[-machine_uncertainty, 0)` is `inconclusive`;
4. PSD with nonnegative spectrum is `pass`;
5. SPD with minimum exactly zero is `fail`;
6. SPD with positive spectrum applies the existing configured rcond threshold and only its existing `atol + rtol*abs(threshold)` boundary may be `inconclusive`.

Freeze all returned arrays with `immutable_array`. In Gaussian interactions, remove `_validate_psd`'s configured tolerance and make `_symmetrize_checked`, `_validate_psd`, and `_validate_spd` consume the shared assessment. Both `fail` and `inconclusive` raise `GaussianNumericalError`; Cholesky runs only after an SPD `pass`. In `fisher_channel_decomposition`, attach `defect_assessment: SpectralConditioningAssessment` and preserve the legacy fields with these exact conservative properties:

```python
@property
def minimum_defect_eigenvalue(self) -> float:
    return self.defect_assessment.minimum_eigenvalue

@property
def defect_psd_tolerance(self) -> float:
    return self.defect_assessment.machine_uncertainty

@property
def defect_is_psd(self) -> bool:
    return self.defect_assessment.decision == "pass"
```

An `inconclusive` assessment therefore never maps to legacy `defect_is_psd=True`.
Replace the package root, which currently contains only a docstring, with this
exact public surface:

```python
"""Importable APIs for exact Gauge-VFE experiment laboratories."""

from .conditioning import (
    MatrixDomainPolicy,
    SpectralConditioningAssessment,
    assess_spectral_psd,
    assess_spectral_spd,
    assess_symmetric_matrix,
)

__all__ = [
    "MatrixDomainPolicy",
    "SpectralConditioningAssessment",
    "assess_spectral_psd",
    "assess_spectral_spd",
    "assess_symmetric_matrix",
]
```

- [ ] **Step 4: Run GREEN, compatibility tests, and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_conditioning.py tests\test_gaussian_realization.py tests\test_fisher.py tests\test_counterexamples.py tests\test_shared_scientific_contracts.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task4-green --junitxml=C:\tmp\multiagentelbo-wave-a-task4-green.xml
[xml]$task4 = Get-Content -Raw -LiteralPath 'C:\\tmp\\multiagentelbo-wave-a-task4-green.xml'
$task4Suites = @($task4.testsuites.testsuite)
if ([int](($task4Suites | Measure-Object failures -Sum).Sum) -ne 0 -or [int](($task4Suites | Measure-Object errors -Sum).Sum) -ne 0) { throw 'Task 4 JUnit is not green' }
git add -- src/multiagent_elbo/conditioning.py src/multiagent_elbo/__init__.py src/multiagent_elbo/realizations/gaussian/interactions.py src/multiagent_elbo/finite/fisher.py src/multiagent_elbo/finite/counterexamples.py tests/test_conditioning.py tests/test_gaussian_realization.py tests/test_fisher.py tests/test_counterexamples.py tests/test_shared_scientific_contracts.py
git commit -m "fix: unify finite symmetric matrix assessment"
```

### Task 5: Construct one Fisher quotient from one assessed eigensystem (`AUD-15`)

**Files:**
- Modify: `src/multiagent_elbo/conditioning.py`
- Modify: `src/multiagent_elbo/finite/information_history.py`
- Modify: `src/multiagent_elbo/__init__.py`
- Modify: `tests/test_conditioning.py`
- Modify: `tests/test_information_history.py`
- Modify: `tests/test_information_history_experiment.py`

**Interfaces:**
- Public immutable `SpectralQuotientAssessment` fields: `matrix_assessment`, `rcond`, `spectral_scale`, `cutoff`, `retained_mask`, `rank`, `nullity`, `retained_condition_number`, `pseudoinverse`, and `range_projector`.
- Public `assess_spectral_quotient(matrix: object, *, rcond: float) -> SpectralQuotientAssessment` requires `0 < rcond < 1` and requires A3 PSD decision `pass` before truncation.
- `SpectralQuotientAssessment.natural_gradient_descent(gradient)` returns immutable `-F_plus @ gradient` after exact shape/finite checks.
- `categorical_information_point` constructs one quotient assessment as a local
  variable and copies its outputs into the 12 existing `InformationPoint`
  constructor fields. The dataclass gains no `quotient` field, no `init=False`
  cache, and no new required argument.

- [ ] **Step 1: Add single-mask and negative-curvature RED tests**

```python
def test_quotient_uses_one_scale_relative_mask_for_every_output(monkeypatch):
    monkeypatch.setattr(
        np.linalg,
        "pinv",
        lambda *_args, **_kwargs: pytest.fail("np.linalg.pinv must not run"),
    )
    quotient = conditioning.assess_spectral_quotient(
        np.diag([1.0e-8, 1.0e-20]), rcond=1.0e-6
    )
    assert quotient.cutoff == pytest.approx(1.0e-14)
    assert quotient.retained_mask.tolist() == [False, True]
    assert quotient.rank == 1
    assert quotient.nullity == 1
    assert np.linalg.matrix_rank(quotient.range_projector, tol=1e-12) == 1
    np.testing.assert_allclose(
        quotient.pseudoinverse,
        np.diag([1.0e8, 0.0]),
        rtol=1e-14,
    )


def test_rcond_cannot_license_negative_fisher_curvature():
    with pytest.raises(ValueError, match="PSD assessment failed"):
        conditioning.assess_spectral_quotient(
            np.diag([1.0, -0.05]), rcond=0.1
        )


def test_zero_fisher_has_zero_quotient_operators():
    quotient = conditioning.assess_spectral_quotient(
        np.zeros((2, 2)), rcond=1e-6
    )
    assert quotient.rank == 0
    assert quotient.nullity == 2
    np.testing.assert_array_equal(quotient.pseudoinverse, np.zeros((2, 2)))
    np.testing.assert_array_equal(quotient.range_projector, np.zeros((2, 2)))


# tests/test_information_history.py; add `import inspect` and
# `import multiagent_elbo.conditioning as conditioning`.
def test_information_point_constructor_and_fields_use_the_one_quotient_mask():
    module = _sut()
    assert tuple(inspect.signature(module.InformationPoint).parameters) == (
        "probability",
        "score",
        "fisher",
        "vfe_gradient",
        "natural_gradient",
        "fisher_projector",
        "rank",
        "nullity",
        "positive_spectrum_condition_number",
        "range_residual",
        "inverse_rule",
        "used_pseudoinverse",
    )
    family = CategoricalExponentialFamily(
        ("a", "b", "c"),
        (0.0, 0.0, 0.0),
        ((1.0, 0.0), (0.0, 1.0e-8), (0.0, 0.0)),
        NUMERICS,
    )
    point = module.categorical_information_point(
        family, (0.0, 0.0), (0.2, 0.3, 0.5), rcond=1.0e-6
    )
    quotient = conditioning.assess_spectral_quotient(
        point.fisher, rcond=1.0e-6
    )

    assert not hasattr(point, "quotient")
    assert point.rank == quotient.rank == 1
    assert point.nullity == quotient.nullity == 1
    assert point.used_pseudoinverse is True
    assert point.positive_spectrum_condition_number == (
        quotient.retained_condition_number
    )
    np.testing.assert_array_equal(
        point.fisher_projector, quotient.range_projector
    )
    assert np.linalg.matrix_rank(
        point.fisher_projector, tol=quotient.cutoff
    ) == point.rank
    np.testing.assert_array_equal(
        point.natural_gradient,
        quotient.natural_gradient_descent(point.vfe_gradient),
    )
```

The retained-mask order follows `scipy.linalg.eigh`'s ascending eigenvalue order.

- [ ] **Step 2: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_conditioning.py tests\test_information_history.py tests\test_information_history_experiment.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task5-red --junitxml=C:\tmp\multiagentelbo-wave-a-task5-red.xml
```

Expected: FAIL because `SpectralQuotientAssessment` does not exist and current rank and `np.linalg.pinv` cutoffs disagree.

- [ ] **Step 3: Build quotient operators only from A3's eigenvectors/eigenvalues**

```python
assessment = assess_spectral_psd(matrix)
if assessment.decision != "pass":
    raise ValueError(f"PSD assessment {assessment.decision}: {assessment.reason}")
eigenvalues = assessment.eigenvalues
eigenvectors = assessment.eigenvectors
spectral_scale = float(np.max(np.abs(eigenvalues)))
cutoff = rcond_value * spectral_scale
retained = eigenvalues > cutoff
retained_vectors = eigenvectors[:, retained]
retained_values = eigenvalues[retained]
if retained_values.size:
    pseudoinverse = (retained_vectors / retained_values) @ retained_vectors.T
    projector = retained_vectors @ retained_vectors.T
    condition = float(retained_values[-1] / retained_values[0])
else:
    pseudoinverse = np.zeros_like(assessment.symmetric_matrix)
    projector = np.zeros_like(assessment.symmetric_matrix)
    condition = 0.0
```

Freeze the mask, pseudoinverse, and projector. Validate `rcond` as a
non-Boolean finite real strictly inside `(0,1)`. Remove
`_spectral_diagnostics` and every `np.linalg.pinv` call from
`information_history.py`. Use `assess_spectral_quotient` for fine, coarse, and
pushed Fisher diagnostics, but keep each assessment local to the computation.
Construct the existing public carrier exactly:

```python
quotient = assess_spectral_quotient(fisher, rcond=rcond_value)
natural_gradient = quotient.natural_gradient_descent(gradient)
range_residual = float(
    np.linalg.norm(
        gradient - quotient.range_projector @ gradient,
        ord=np.inf,
    )
)
return InformationPoint(
    probability=immutable_array(probability),
    score=immutable_array(score),
    fisher=immutable_array(fisher),
    vfe_gradient=immutable_array(gradient),
    natural_gradient=natural_gradient,
    fisher_projector=quotient.range_projector,
    rank=quotient.rank,
    nullity=quotient.nullity,
    positive_spectrum_condition_number=quotient.retained_condition_number,
    range_residual=range_residual,
    inverse_rule="moore_penrose_identifiable_tangent_quotient",
    used_pseudoinverse=quotient.nullity > 0,
)
```

Do not add a dataclass field or property named `quotient`. Replace the Task 4 package
root export block with this exact superset:

```python
"""Importable APIs for exact Gauge-VFE experiment laboratories."""

from .conditioning import (
    MatrixDomainPolicy,
    SpectralConditioningAssessment,
    SpectralQuotientAssessment,
    assess_spectral_psd,
    assess_spectral_quotient,
    assess_spectral_spd,
    assess_symmetric_matrix,
)

__all__ = [
    "MatrixDomainPolicy",
    "SpectralConditioningAssessment",
    "SpectralQuotientAssessment",
    "assess_spectral_psd",
    "assess_spectral_quotient",
    "assess_spectral_spd",
    "assess_symmetric_matrix",
]
```

- [ ] **Step 4: Run GREEN, prove the duplicate mask is absent, and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_conditioning.py tests\test_information_history.py tests\test_information_history_experiment.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task5-green --junitxml=C:\tmp\multiagentelbo-wave-a-task5-green.xml
[xml]$task5 = Get-Content -Raw -LiteralPath 'C:\\tmp\\multiagentelbo-wave-a-task5-green.xml'
$task5Suites = @($task5.testsuites.testsuite)
if ([int](($task5Suites | Measure-Object failures -Sum).Sum) -ne 0 -or [int](($task5Suites | Measure-Object errors -Sum).Sum) -ne 0) { throw 'Task 5 JUnit is not green' }
$duplicates = rg -n "np\.linalg\.pinv|def _spectral_diagnostics" src\multiagent_elbo\finite\information_history.py
if ($LASTEXITCODE -eq 0) { throw "duplicate quotient path remains: $duplicates" }
if ($LASTEXITCODE -ne 1) { throw 'duplicate-path scan failed' }
```

Expected: the duplicate-path scan exits through the explicit no-match branch.

```powershell
git add -- src/multiagent_elbo/conditioning.py src/multiagent_elbo/finite/information_history.py src/multiagent_elbo/__init__.py tests/test_conditioning.py tests/test_information_history.py tests/test_information_history_experiment.py
git commit -m "fix: use one Fisher quotient eigensystem"
```

### Task 6: Separate quotient-threshold recovery from exact pointwise equality (`AUD-16`)

**Files:**
- Modify: `src/multiagent_elbo/finite/fisher.py`
- Modify: `src/multiagent_elbo/finite/information_history.py`
- Modify: `src/multiagent_elbo/finite/__init__.py`
- Modify: `tests/test_fisher.py`
- Modify: `tests/test_information_history.py`

**Interfaces:**
- Public immutable `ExactFisherChannelWitness` stores exact rational `probability`, `scores`, `channel`, `fine_fisher`, `coarse_fisher`, `conditional_covariance`, and `decomposition_residual`.
- Public `exact_fisher_channel_witness(probability, scores, channel) -> ExactFisherChannelWitness` validates exact probability/channel normalization and exact score centering before exact arithmetic.
- Public `assess_information_recovery(probability, score, channel, *, rcond, exact_witness=None) -> RecoveryDiagnostics` is the v2 assessment.
- Existing `recovery_diagnostics(probability, score, channel, *, rcond=None, exact_witness=None)` delegates, using `probability.numerics.min_spd_rcond` only when the new keyword is omitted.
- Private `_assess_recovery_matrices(fine_fisher, coarse_fisher, conditional_covariance, *, rcond, exact_pointwise_equality) -> RecoveryDiagnostics` owns the matrix checks so the public statistical entry point and matrix negative controls cannot diverge.
- `RecoveryDiagnostics` fields: `schema_version="fisher-recovery-v2"`, `rcond`, `fisher_defect`, `fine_information_rank`, `fine_nullity`, `structural_nullity`, `relative_loss_spectrum`, `maximum_relative_loss`, `quotient_threshold_recovery`, `exact_pointwise_equality`, `decomposition_residual`, `loewner_lower_residual`, `loewner_upper_residual`, `fine_null_block_residual`, `fine_null_range_cross_residual`, and `global_experiment_recovery_claimed=False`.
- Compatibility property `recoverable_direction_dimension` counts retained `mu <= rcond`; compatibility property `pointwise_full_fisher_equality` is true only when `exact_pointwise_equality is True` and otherwise returns false.

- [ ] **Step 1: Add full-Loewner, cross-block, and exact-versus-threshold RED tests**

```python
# tests/test_information_history.py: add these imports with the existing imports.
from fractions import Fraction

import multiagent_elbo.finite.fisher as fisher_module


def test_recovery_rejects_information_outside_the_fine_range():
    module = _sut()
    with pytest.raises(ValueError, match="PSD|Loewner"):
        module._assess_recovery_matrices(
            np.diag([1.0, 0.0]),
            np.diag([1.0, 1.0]),
            np.diag([0.0, -1.0]),
            rcond=0.1,
            exact_pointwise_equality=None,
        )


def test_recovery_rejects_nonzero_fine_null_range_cross_block():
    module = _sut()
    with pytest.raises(ValueError, match="PSD|Loewner|null/range"):
        module._assess_recovery_matrices(
            np.diag([1.0, 0.0]),
            np.array([[0.9, 1.0e-3], [1.0e-3, 0.0]]),
            np.array([[0.1, -1.0e-3], [-1.0e-3, 0.0]]),
            rcond=0.1,
            exact_pointwise_equality=None,
        )


def test_threshold_recovery_does_not_become_exact_equality():
    module = _sut()
    witness = fisher_module.exact_fisher_channel_witness(
        probability=(Fraction(1, 2), Fraction(1, 2)),
        scores=((Fraction(-1),), (Fraction(1),)),
        channel=((Fraction(19, 20), Fraction(1, 20)),
                 (Fraction(1, 20), Fraction(19, 20))),
    )
    probability = ProbabilityMeasure(("x", "y"), (0.5, 0.5), NUMERICS)
    channel = MarkovKernel(("x", "y"), ("a", "b"), witness.channel, NUMERICS)
    result = module.assess_information_recovery(
        probability,
        witness.scores,
        channel,
        rcond=0.2,
        exact_witness=witness,
    )
    assert result.maximum_relative_loss == pytest.approx(0.19)
    assert result.quotient_threshold_recovery is True
    assert result.exact_pointwise_equality is False
    assert result.pointwise_full_fisher_equality is False


def test_missing_exact_witness_never_infers_exact_equality():
    module = _sut()
    probability = ProbabilityMeasure(("x", "y"), (0.5, 0.5), NUMERICS)
    identity = MarkovKernel(
        ("x", "y"),
        ("x", "y"),
        ((1.0, 0.0), (0.0, 1.0)),
        NUMERICS,
    )
    score = ((-1.0,), (1.0,))
    result = module.assess_information_recovery(
        probability, score, identity, rcond=1e-6
    )
    assert result.exact_pointwise_equality is None
    assert result.pointwise_full_fisher_equality is False
    assert result.global_experiment_recovery_claimed is False
```

Add this exact independent constructor test to `tests/test_fisher.py`; its
module import exists before the new attribute, so the RED suite collects:

```python
import multiagent_elbo.finite.fisher as fisher_module


def test_exact_fisher_witness_uses_fraction_arithmetic_and_exact_residual():
    witness = fisher_module.exact_fisher_channel_witness(
        probability=(Fraction(1, 2), Fraction(1, 2)),
        scores=((Fraction(-1),), (Fraction(1),)),
        channel=((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))),
    )
    assert witness.fine_fisher == ((Fraction(1),),)
    assert witness.coarse_fisher == witness.fine_fisher
    assert witness.conditional_covariance == ((Fraction(0),),)
    assert witness.decomposition_residual == ((Fraction(0),),)
```

Also add `from fractions import Fraction` to `tests/test_fisher.py`.

- [ ] **Step 2: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_fisher.py tests\test_information_history.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task6-red --junitxml=C:\tmp\multiagentelbo-wave-a-task6-red.xml
```

Expected: FAIL because the exact witness and relative recovery assessment do not exist, and the current absolute floor labels sufficiently small total loss as full equality.

- [ ] **Step 3: Implement full matrix membership/Loewner checks before whitening**

For `fine`, `coarse`, and `delta = fine - coarse`, require A3 PSD `pass`. Reject any decomposition residual whose max absolute entry exceeds
`64*n*eps*max(1, maxabs(fine), maxabs(coarse), maxabs(delta))`. This band is internal and cannot use `NumericsConfig` tolerances.

Use the positive-eigenvalue structural null basis (`lambda == 0.0` after A3 membership), not the rcond-discarded small-positive subspace, for the explicit null and cross checks. Full Loewner membership remains authoritative even when that basis is empty. Then compute:

```python
retained = fine_quotient.retained_mask
vectors = fine_quotient.matrix_assessment.eigenvectors[:, retained]
values = fine_quotient.matrix_assessment.eigenvalues[retained]
scaled = vectors / np.sqrt(values)
relative_loss = 0.5 * (scaled.T @ delta @ scaled + (scaled.T @ delta @ scaled).T)
mu = scipy.linalg.eigvalsh(relative_loss, check_finite=True)
if np.any(mu < -rcond_value) or np.any(mu > 1.0 + rcond_value):
    raise ValueError("relative Fisher loss is outside the declared Loewner interval")
threshold_recovery = bool(np.all(mu <= rcond_value))
```

Bind an exact witness by exact equality of its float-rendered probability, scores, and channel to the three runtime inputs; a stale/mismatched witness raises before classification. Set `exact_pointwise_equality` by exact `Fraction` zero/nonzero entries of the witness defect, including its exact residual, null, and cross blocks. Without a witness, store `None` even when numerical defect entries are zero.

Implement the compatibility properties exactly:

```python
@property
def recoverable_direction_dimension(self) -> int:
    return int(np.count_nonzero(self.relative_loss_spectrum <= self.rcond))

@property
def pointwise_full_fisher_equality(self) -> bool:
    return self.exact_pointwise_equality is True
```

Update `src/multiagent_elbo/finite/__init__.py` with these imports and ordered
`__all__` additions, preserving every existing entry:

```python
from .fisher import ExactFisherChannelWitness, exact_fisher_channel_witness
from .information_history import (
    RecoveryDiagnostics,
    assess_information_recovery,
    recovery_diagnostics,
)

# Insert into __all__ in alphabetic position:
"ExactFisherChannelWitness",
"RecoveryDiagnostics",
"assess_information_recovery",
"exact_fisher_channel_witness",
"recovery_diagnostics",
```

The module-level implementations remain defined in `finite.fisher` and
`finite.information_history`; the package initializer only re-exports them and
does not wrap or duplicate them.

- [ ] **Step 4: Run GREEN, export the public v2 surface, and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_fisher.py tests\test_information_history.py tests\test_information_history_experiment.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task6-green --junitxml=C:\tmp\multiagentelbo-wave-a-task6-green.xml
[xml]$task6 = Get-Content -Raw -LiteralPath 'C:\\tmp\\multiagentelbo-wave-a-task6-green.xml'
$task6Suites = @($task6.testsuites.testsuite)
if ([int](($task6Suites | Measure-Object failures -Sum).Sum) -ne 0 -or [int](($task6Suites | Measure-Object errors -Sum).Sum) -ne 0) { throw 'Task 6 JUnit is not green' }
git add -- src/multiagent_elbo/finite/fisher.py src/multiagent_elbo/finite/information_history.py src/multiagent_elbo/finite/__init__.py tests/test_fisher.py tests/test_information_history.py
git commit -m "fix: assess Fisher recovery on the fine quotient"
```

### Task 7: Bind the scale Fisher metric to an exact persisted statistical witness (`AUD-17`)

**Files:**
- Modify: `src/multiagent_elbo/finite/scale_cocycle.py`
- Modify: `src/multiagent_elbo/finite/scale_cocycle_experiment.py`
- Modify: `tests/test_scale_cocycle.py`
- Modify: `tests/test_scale_cocycle_experiment.py`

**Interfaces:**
- `FisherCocycleResidualForms` remains the compatibility carrier but adds `status: Literal["bilinear_identity_only"]` and `has_fisher_provenance: Literal[False]`; `base_fisher_cocycle_residual_forms(...)` never promotes arbitrary input.
- The active experiment calls `exact_fisher_channel_witness` on the approved six-state law/scores/constant channel, feeds `witness.conditional_covariance` into the bilinear identity, and separately records exact Fisher provenance.
- Existing `derivative_cocycle.json` advances to schema
  `scale-cocycle-derivative-v2` and contains a closed
  `fisher_cocycle_witness` record with schema
  `scale-fisher-cocycle-witness-v1` and exact string-valued law, score, channel,
  fine/coarse Fisher, conditional covariance, and residual matrices. No tenth
  semantic payload is added; the approved nine-payload inventory remains exact.

- [ ] **Step 1: Add generic non-Fisher and active exact-witness RED tests**

```python
# tests/test_scale_cocycle.py: add this import beside the existing scale imports.
from multiagent_elbo.finite.fisher import exact_fisher_channel_witness


def test_generic_bilinear_identity_never_claims_fisher_provenance():
    forms = base_fisher_cocycle_residual_forms(
        fisher_defect=((F(0), F(1)), (F(0), F(0))),
        pushed_fine_jet=(F(1), F(2)),
        horizontal_anomaly=(F(2), F(-1)),
    )
    assert forms.status == "bilinear_identity_only"
    assert forms.has_fisher_provenance is False
    assert forms.from_norm_difference == forms.from_coarse_jet_cross_terms


def test_exact_six_state_witness_derives_the_active_fisher_defect():
    witness = exact_fisher_channel_witness(
        probability=(F(1,8), F(1,8), F(1,4), F(1,4), F(1,8), F(1,8)),
        scores=((F(2),F(0)), (F(-2),F(0)), (F(0),F(2)),
                (F(0),F(-2)), (F(2),F(2)), (F(-2),F(-2))),
        channel=((F(1),),) * 6,
    )
    assert witness.coarse_fisher == ((F(0), F(0)), (F(0), F(0)))
    assert witness.fine_fisher == ((F(2), F(1)), (F(1), F(3)))
    assert witness.conditional_covariance == witness.fine_fisher
    assert witness.decomposition_residual == ((F(0), F(0)), (F(0), F(0)))
```

Add this complete experiment test to `tests/test_scale_cocycle_experiment.py`;
`Fraction`, `json`, `np`, `Path`, and `run_scale_cocycle_experiment` are already
imported:

```python
def test_persisted_fisher_witness_recomputes_active_defect_without_tenth_payload(
    tmp_path: Path,
):
    result = run_scale_cocycle_experiment(scale_config(tmp_path))
    derivative = json.loads(
        (result.run_dir / "derivative_cocycle.json").read_text(encoding="utf-8")
    )
    assert derivative["schema_version"] == "scale-cocycle-derivative-v2"
    record = derivative["fisher_cocycle_witness"]
    assert record["schema_version"] == "scale-fisher-cocycle-witness-v1"

    probability = tuple(Fraction(value) for value in record["probability"])
    scores = tuple(
        tuple(Fraction(value) for value in row) for row in record["scores"]
    )
    channel = tuple(
        tuple(Fraction(value) for value in row) for row in record["channel"]
    )
    dimension = len(scores[0])
    zero_matrix = tuple(
        tuple(Fraction(0) for _ in range(dimension))
        for _ in range(dimension)
    )

    assert sum(probability, Fraction(0)) == Fraction(1)
    assert all(sum(row, Fraction(0)) == Fraction(1) for row in channel)
    center = tuple(
        sum((probability[x] * scores[x][i] for x in range(len(probability))), Fraction(0))
        for i in range(dimension)
    )
    assert center == (Fraction(0),) * dimension
    fine = tuple(
        tuple(
            sum(
                (probability[x] * scores[x][i] * scores[x][j] for x in range(len(probability))),
                Fraction(0),
            )
            for j in range(dimension)
        )
        for i in range(dimension)
    )
    coarse_probability = tuple(
        sum((probability[x] * channel[x][z] for x in range(len(probability))), Fraction(0))
        for z in range(len(channel[0]))
    )
    coarse_score = tuple(
        tuple(
            sum(
                (probability[x] * channel[x][z] * scores[x][i] for x in range(len(probability))),
                Fraction(0),
            ) / coarse_probability[z]
            for i in range(dimension)
        )
        for z in range(len(coarse_probability))
    )
    coarse = tuple(
        tuple(
            sum(
                (coarse_probability[z] * coarse_score[z][i] * coarse_score[z][j]
                 for z in range(len(coarse_probability))),
                Fraction(0),
            )
            for j in range(dimension)
        )
        for i in range(dimension)
    )
    conditional = tuple(
        tuple(
            sum(
                (
                    probability[x]
                    * channel[x][z]
                    * (scores[x][i] - coarse_score[z][i])
                    * (scores[x][j] - coarse_score[z][j])
                    for x in range(len(probability))
                    for z in range(len(coarse_probability))
                ),
                Fraction(0),
            )
            for j in range(dimension)
        )
        for i in range(dimension)
    )
    residual = tuple(
        tuple(fine[i][j] - coarse[i][j] - conditional[i][j] for j in range(dimension))
        for i in range(dimension)
    )

    def matrix(values):
        return tuple(tuple(Fraction(value) for value in row) for row in values)

    assert matrix(record["fine_fisher"]) == fine == ((Fraction(2), Fraction(1)), (Fraction(1), Fraction(3)))
    assert matrix(record["coarse_fisher"]) == coarse == zero_matrix
    assert matrix(record["conditional_covariance"]) == conditional == fine
    assert matrix(record["decomposition_residual"]) == residual == zero_matrix
    np.testing.assert_array_equal(
        result.arrays["base_fisher_defect"],
        np.asarray(conditional, dtype=np.float64),
    )
    metric = result.metrics["base_fisher_cocycle_forms_residual"]
    assert metric.value == 0.0
    assert "derivative_cocycle.json#fisher_cocycle_witness" in metric.interpretation

    control = derivative["bilinear_identity_nonsymmetric_control"]
    assert control["status"] == "bilinear_identity_only"
    assert control["has_fisher_provenance"] is False
    control_matrix = matrix(control["matrix"])
    assert control_matrix != tuple(zip(*control_matrix))

    nonsymmetric_literal = [["0", "1"], ["0", "0"]]
    nonsymmetric_paths = []
    def visit(value, path=()):
        if isinstance(value, dict):
            for key, child in value.items():
                visit(child, path + (key,))
        elif value == nonsymmetric_literal:
            nonsymmetric_paths.append("/".join(path))
    visit(derivative)
    assert nonsymmetric_paths
    assert all("bilinear_identity" in path for path in nonsymmetric_paths)
    assert all("fisher" not in path for path in nonsymmetric_paths)

    approved = {
        "three_level_extension.json",
        "composed_channels.json",
        "coarse_actions.json",
        "posterior_bridges.json",
        "comparison_isomorphisms.json",
        "derivative_cocycle.json",
        "retained_projection_residual.json",
        "metrics.json",
        "arrays.npz",
    }
    nonsemantic = {"config.json", "manifest.json"}
    published = {path.name for path in result.run_dir.iterdir() if path.is_file()}
    assert published - nonsemantic == approved
    assert "fisher_cocycle_witness.json" not in published
```

- [ ] **Step 2: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_scale_cocycle.py tests\test_scale_cocycle_experiment.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task7-red --junitxml=C:\tmp\multiagentelbo-wave-a-task7-red.xml
```

Expected: FAIL because the generic carrier has no non-Fisher status and the active experiment passes a parallel hard-coded matrix without a persisted witness.

- [ ] **Step 3: Derive, consume, and persist the exact witness**

Replace the active literal with:

```python
fisher_witness = exact_fisher_channel_witness(
    probability=(F(1, 8), F(1, 8), F(1, 4), F(1, 4), F(1, 8), F(1, 8)),
    scores=((F(2), F(0)), (F(-2), F(0)), (F(0), F(2)),
            (F(0), F(-2)), (F(2), F(2)), (F(-2), F(-2))),
    channel=((F(1),),) * 6,
)
fisher_forms = base_fisher_cocycle_residual_forms(
    fisher_defect=fisher_witness.conditional_covariance,
    pushed_fine_jet=(F(1), F(2)),
    horizontal_anomaly=(F(2), F(-1)),
)
```

Persist this exact closed record:

```json
{
  "schema_version": "scale-fisher-cocycle-witness-v1",
  "provenance": "exact_finite_centered_score_fixed_channel",
  "probability": ["1/8", "1/8", "1/4", "1/4", "1/8", "1/8"],
  "scores": [["2", "0"], ["-2", "0"], ["0", "2"], ["0", "-2"], ["2", "2"], ["-2", "-2"]],
  "channel": [["1"], ["1"], ["1"], ["1"], ["1"], ["1"]],
  "fine_fisher": [["2", "1"], ["1", "3"]],
  "coarse_fisher": [["0", "0"], ["0", "0"]],
  "conditional_covariance": [["2", "1"], ["1", "3"]],
  "decomposition_residual": [["0", "0"], ["0", "0"]]
}
```

Insert the record above under `derivative_cocycle["fisher_cocycle_witness"]`
before the existing nine-payload bundle is prepared; do not add a new artifact
name. Keep `base_fisher_cocycle_forms_residual` as `CANDIDATE`, but make it
consume the derived matrix and name
`derivative_cocycle.json#fisher_cocycle_witness` in its interpretation. Add a
separate `bilinear_identity_nonsymmetric_control` only as an algebraic negative
control with no Fisher provenance.

Advance `derivative_cocycle["schema_version"]` to
`scale-cocycle-derivative-v2`. Add
`arrays["base_fisher_defect"] = _float_array(fisher_witness.conditional_covariance)`;
this is an array inside the existing `arrays.npz`, not a tenth semantic payload.
Persist the nonsymmetric control exactly as:

```python
derivative_cocycle["bilinear_identity_nonsymmetric_control"] = {
    "status": "bilinear_identity_only",
    "has_fisher_provenance": False,
    "matrix": [["0", "1"], ["0", "0"]],
}
```

- [ ] **Step 4: Run GREEN and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_scale_cocycle.py tests\test_scale_cocycle_experiment.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task7-green --junitxml=C:\tmp\multiagentelbo-wave-a-task7-green.xml
[xml]$task7 = Get-Content -Raw -LiteralPath 'C:\\tmp\\multiagentelbo-wave-a-task7-green.xml'
$task7Suites = @($task7.testsuites.testsuite)
if ([int](($task7Suites | Measure-Object failures -Sum).Sum) -ne 0 -or [int](($task7Suites | Measure-Object errors -Sum).Sum) -ne 0) { throw 'Task 7 JUnit is not green' }
git add -- src/multiagent_elbo/finite/scale_cocycle.py src/multiagent_elbo/finite/scale_cocycle_experiment.py tests/test_scale_cocycle.py tests/test_scale_cocycle_experiment.py
git commit -m "fix: derive Fisher cocycle metric from exact witness"
```

### Task 8: Produce revision-bound Wave A evidence and close all seven findings

**Files:**
- Create: `tools/wave_a_evidence.py`
- Create: `tests/test_wave_a_evidence.py`
- Create at runtime and commit: the directory computed as `docs/verification/evidence/wave-a/$implementationShort`.
- Create at runtime and do not commit: the directory computed as `verification-evidence/wave-a/$evidenceShort`.
- Create in ignored control-plane storage: `.verification/wave-a/final-ledger.json`; the installed gate owns the repository-global `.verification/active.json` marker.

**Interfaces:**
- All targeted, subsystem, and full suites use the frozen generic CLI exactly:
  `tools/remediation_evidence.py run-junit --record PATH --junit PATH -- ARGV`.
  Wave A defines no second pytest runner, command-record schema, JUnit parser, or
  environment writer.
- `write-derivations --implementation-head SHA --tested-head SHA --output DIR`
  writes four create-once canonical raw records below the ignored raw staging
  directory. It rejects any output other than the stage/head-derived
  `.verification/raw/wave-a/{tested-short}/{candidate|closure}/domain/derivations`
  path before creating a directory. It labels exact derivation, exact rational
  oracle, numerical policy, and mechanical probe sections separately. Its pure
  helper `prepare_derivation_files(implementation_head, tested_head)` returns the
  four immutable `PreparedEvidenceFile` values without writing.
- `prepare_upstream_wave0_plan_file(repo_root) -> PreparedEvidenceFile` reads
  only `UPSTREAM_WAVE0_PLAN_PATH`, requires a tracked regular non-reparse file
  whose SHA-256 is exactly `UPSTREAM_WAVE0_PLAN_SHA256`, and returns
  `UPSTREAM_WAVE0_PUBLIC_PATH` with exactly
  `UPSTREAM_WAVE0_RECORD_FIELDS` and
  `schema_version="wave-a-upstream-wave0-plan-v1"`. It never accepts a caller
  path, digest, or status override.
- `review-context-sha --tested-head SHA --implementation-parent SHA --raw-dir
  PATH` validates exact `E/P` ancestry, candidate evidence, all three raw
  command/JUnit pairs, derivations, resolved tested/source/dependency inputs,
  the reviewed Wave A plan and its plan commit, the pinned verification
  snapshot, claim/criteria constants, and every candidate/closure path contract.
  It writes only ignored `review-context.json` and prints its canonical SHA-256.
- `review-target --tested-head SHA --implementation-parent SHA --raw-dir PATH`
  validates the context and current external review records and prints only
  `2`, `4`, or `8`. `validate-reviews` takes the same arguments and requires
  the complete selected view tier, both high-severity skeptics, and all 14
  adjudicators before a public closure byte exists.
- `build --stage {candidate,closure} --tested-head SHA --implementation-parent
  SHA --raw-dir PATH --output-dir PATH` prepares the generic Wave 0
  JUnit/environment/index files, prepares the Wave A derivation/review domain
  files, applies the Wave 0 total privacy transform to every raw/public pair,
  validates the exact stage/branch virtual union, and publishes that union once.
  Candidate construction rejects any review input. Closure construction
  consumes only the already validated external review/adjudicator bytes bound
  by `review-context.json`; it never synthesizes a view or decision.
- `validate-domain --bundle-dir PATH` validates the closed Wave A domain
  inventory, its canonical generic-non-index inventory digest, the absence of
  any final-index back-edge, and exact union completeness.
- `populate-ledger --ledger FILE --closure-index FILE --domain-index FILE` may
  replace only the empty closure template created by the installed gate. It
  revalidates both indexes and every indexed public review at live `HEAD`, then
  maps support/refute/abstain to
  `EVIDENCE_VERIFIED`/`REFUTED`/`INCONCLUSIVE`. `CLAIM_SPECS` supplies no
  state, review, score, trigger, or obligation.
- The adapter imports `PreparedEvidenceBundle`, `PreparedEvidenceFile`,
  `canonical_json_bytes`, `prepare_evidence_bundle`,
  `publish_evidence_bundle`, and `validate_evidence_index` from
  `tools.remediation_evidence`. `publish_evidence_bundle` remains the only writer
  to either final evidence directory.

The adapter consumes the Wave 0 generic builder without changing its schema.
The tested-input policy contains the exact reviewed Wave A plan, the frozen Wave
0 PASS plan, and `verification-contract-v1.json` rules. The generic resolver
discovers the Wave A plan's concrete last-touch commit and proves that commit is
an ancestor of both `P` and `E` with the same plan blob; callers never supply a
plan commit. The adapter independently requires
`UPSTREAM_WAVE0_PLAN_PATH` at exact `UPSTREAM_WAVE0_PLAN_SHA256` in tested,
source/config, and dependency inventories and emits the closed
`upstream-wave0-plan.json` record. Dependency inputs three and four are the
frozen Wave 0 plan and pinned snapshot. The adapter adds that upstream record,
derivations, and external review records only to the detached virtual file map
after the generic records have been prepared, then regenerates and validates
the one final `index.json` over every public artifact except itself before the
sole publication call. It never accepts a caller-built tested-input subset or
an unindexed public byte.

Use these exact production constants in `tools/wave_a_evidence.py`:

```python
CPU_PYTHON = Path(r"C:\Python314\python.exe")
UPSTREAM_WAVE0_PLAN_PATH = (
    "docs/superpowers/plans/"
    "2026-08-11-scientific-integrity-remediation-wave-0.md"
)
UPSTREAM_WAVE0_PLAN_SHA256 = (
    "dbe2263a3b0fe1e9f5db4ff1fca9a19f819cfd32ef38da71d6e5cb5485723ac2"
)
UPSTREAM_WAVE0_PUBLIC_PATH = "upstream-wave0-plan.json"
UPSTREAM_WAVE0_RECORD_FIELDS = (
    "schema_version",
    "path",
    "size_bytes",
    "sha256",
)

WAVE_A_TESTED_INPUT_POLICY = {
    "schema_version": "wave-a-source-config-theory-tools-tests-v1",
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
        "exact:docs/superpowers/specs/2026-08-11-scientific-integrity-remediation-program-design.md",
        "exact:docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md",
        "exact:docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-a.md",
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

WAVE_A_DEPENDENCY_INPUTS = (
    "pyproject.toml",
    "environments/cuda-rtx5090-cu128.lock.txt",
    "docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md",
    "docs/verification/remediation/verification-contract-v1.json",
)

EXPECTED_ENVIRONMENT_KEYS = (
    "CUDA_VISIBLE_DEVICES",
    "MULTIAGENTELBO_RUN_CUDA_TESTS",
    "VFE3_TEST_DEVICE",
    "CUBLAS_WORKSPACE_CONFIG",
    "PYTHONHASHSEED",
    "PYTHONPATH",
)

WAVE_A_REQUIRED_SOURCE_CONFIG_BINDINGS = (
    ".gitattributes",
    ".gitignore",
    "docs/audits/2026-08-11-post-fixed-ray-deep-audit.md",
    "docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md",
    "docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-a.md",
    "docs/superpowers/specs/2026-08-11-scientific-integrity-remediation-program-design.md",
    "docs/verification/remediation/verification-contract-v1.json",
    "environments/cuda-rtx5090-cu128.lock.txt",
    "pyproject.toml",
    "src/multiagent_elbo/__init__.py",
    "src/multiagent_elbo/_immutable.py",
    "src/multiagent_elbo/conditioning.py",
    "src/multiagent_elbo/experiment_support.py",
    "src/multiagent_elbo/finite/__init__.py",
    "src/multiagent_elbo/finite/_kl.py",
    "src/multiagent_elbo/finite/_probability.py",
    "src/multiagent_elbo/finite/agent_network.py",
    "src/multiagent_elbo/finite/categorical_dqm.py",
    "src/multiagent_elbo/finite/counterexamples.py",
    "src/multiagent_elbo/finite/fisher.py",
    "src/multiagent_elbo/finite/information_history.py",
    "src/multiagent_elbo/finite/interactions.py",
    "src/multiagent_elbo/finite/measures.py",
    "src/multiagent_elbo/finite/scale_cocycle.py",
    "src/multiagent_elbo/finite/scale_cocycle_experiment.py",
    "src/multiagent_elbo/finite/vfe.py",
    "src/multiagent_elbo/realizations/gaussian/interactions.py",
    "tests/test_agent_network.py",
    "tests/test_conditioning.py",
    "tests/test_counterexamples.py",
    "tests/test_experiment_support.py",
    "tests/test_fisher.py",
    "tests/test_gaussian_realization.py",
    "tests/test_information_history.py",
    "tests/test_information_history_experiment.py",
    "tests/test_interactions.py",
    "tests/test_measures.py",
    "tests/test_remediation_evidence.py",
    "tests/test_scale_cocycle.py",
    "tests/test_scale_cocycle_experiment.py",
    "tests/test_shared_scientific_contracts.py",
    "tests/test_vfe.py",
    "tests/test_wave_a_evidence.py",
    "tools/remediation_evidence.py",
    "tools/wave_a_evidence.py",
)

# The wrapper additionally binds every tracked regular file below
# docs/verification/remediation/ in sorted repository-relative order. Missing,
# extra, case-aliased, untracked-matching, symlink, or reparse inputs reject.

SKIP_ALLOWLIST_BY_SUITE = {
    "targeted": {},
    "subsystem": {},
    "full": {
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
        "tests.test_cuda_backend::test_pinned_cuda_worker_runs_first_job_with_determinism_environment":
            "requires explicit dedicated CUDA-lane opt-in",
    },
}

CLAIM_CRITERIA_BY_DOMAIN = {
    "code": (
        ("execution", "execution"),
        ("input_output_behavior", "input/output behavior"),
        ("boundary_failure_behavior", "boundary/failure behavior"),
        ("regression_coverage", "regression coverage"),
        ("configuration_reachability", "configuration reachability"),
        ("reproducibility", "reproducibility"),
    ),
    "mathematics": (
        ("statement_precision", "statement precision"),
        ("definitions_domains", "definitions and domains"),
        ("assumptions", "assumptions"),
        ("derivation_validity", "derivation validity"),
        ("theorem_lemma_dependencies", "theorem or lemma dependencies"),
        ("limiting_cases", "limiting cases"),
        ("counterexample_search", "counterexample search"),
        (
            "notation_conclusion_agreement",
            "agreement between notation and conclusion",
        ),
    ),
    "evidence": (
        ("source_authority", "source authority"),
        ("primary_source_status", "primary-source status"),
        ("exact_statement_support", "exact support for the statement"),
        ("quotation_data_fidelity", "quotation or data fidelity"),
        ("provenance", "provenance"),
        (
            "artifact_revision_currency",
            "currency for the stated artifact revision",
        ),
        (
            "material_counterevidence_coverage",
            "material counterevidence coverage",
        ),
    ),
}

CLAIM_SPECS = (
    {
        "id": "AUD-03-DEFECT-REPRODUCTION",
        "domain": "code",
        "severity": "high",
        "kind": "mechanical",
        "evidence_ids": ("aud03-defect-targeted-counterevidence",),
        "statement": "The AUD-03 loose-tolerance malformed-probability and negative-KL defect still reproduces at this artifact revision.",
    },
    {
        "id": "AUD-03-CORRECTED-CONTRACT",
        "domain": "mathematics",
        "severity": "high",
        "kind": "derivation",
        "evidence_ids": ("aud03-kl-nonnegativity-derivation",),
        "statement": "For finite normalized probability laws q and p, KL(q||p) is nonnegative on q absolutely continuous with respect to p, is zero exactly when q=p, and is positive infinity on support failure.",
    },
    {
        "id": "AUD-13-DEFECT-REPRODUCTION",
        "domain": "code",
        "severity": "medium",
        "kind": "mechanical",
        "evidence_ids": ("aud13-defect-targeted-counterevidence",),
        "statement": "The AUD-13 authoritative-array WRITEABLE re-enable defect still reproduces at this artifact revision.",
    },
    {
        "id": "AUD-13-CORRECTED-CONTRACT",
        "domain": "code",
        "severity": "medium",
        "kind": "mechanical",
        "evidence_ids": ("aud13-contract-targeted-evidence",),
        "statement": "Every Wave A authoritative public array is C-contiguous and bytes-backed at this artifact revision.",
    },
    {
        "id": "AUD-14-DEFECT-REPRODUCTION",
        "domain": "code",
        "severity": "medium",
        "kind": "mechanical",
        "evidence_ids": ("aud14-defect-targeted-counterevidence",),
        "statement": "The AUD-14 configured-tolerance negative-curvature acceptance defect still reproduces at this artifact revision.",
    },
    {
        "id": "AUD-14-CORRECTED-CONTRACT",
        "domain": "code",
        "severity": "medium",
        "kind": "mechanical",
        "evidence_ids": ("aud14-contract-targeted-evidence",),
        "statement": "The sole MatrixDomainPolicy and shared finite symmetric-matrix assessment enforce pass, fail, and inconclusive membership before every Wave A matrix consumer at this artifact revision.",
    },
    {
        "id": "AUD-15-DEFECT-REPRODUCTION",
        "domain": "code",
        "severity": "medium",
        "kind": "mechanical",
        "evidence_ids": ("aud15-defect-targeted-counterevidence",),
        "statement": "The AUD-15 rank and pseudoinverse mask disagreement still reproduces at this artifact revision.",
    },
    {
        "id": "AUD-15-CORRECTED-CONTRACT",
        "domain": "mathematics",
        "severity": "medium",
        "kind": "derivation",
        "evidence_ids": ("aud15-spectral-quotient-derivation",),
        "statement": "For a real symmetric positive-semidefinite matrix and one declared relative cutoff, the retained eigenspace uniquely determines the stated rank, nullity, Moore-Penrose operator, range projector, retained condition number, and natural-gradient map.",
    },
    {
        "id": "AUD-16-DEFECT-REPRODUCTION",
        "domain": "code",
        "severity": "medium",
        "kind": "mechanical",
        "evidence_ids": ("aud16-defect-targeted-counterevidence",),
        "statement": "The AUD-16 absolute-floor promotion of small nonzero Fisher loss to exact equality still reproduces at this artifact revision.",
    },
    {
        "id": "AUD-16-CORRECTED-CONTRACT",
        "domain": "mathematics",
        "severity": "medium",
        "kind": "derivation",
        "evidence_ids": ("aud16-loewner-recovery-derivation",),
        "statement": "For positive-semidefinite coarse and fine Fisher forms with 0<=coarse<=fine, whitening on the retained fine range yields a relative-loss spectrum in [0,1], while threshold recovery remains logically distinct from exact equality of forms.",
    },
    {
        "id": "AUD-17-DEFECT-REPRODUCTION",
        "domain": "code",
        "severity": "medium",
        "kind": "mechanical",
        "evidence_ids": ("aud17-defect-targeted-counterevidence",),
        "statement": "The AUD-17 arbitrary nonsymmetric bilinear form can still acquire Fisher provenance at this artifact revision.",
    },
    {
        "id": "AUD-17-CORRECTED-CONTRACT",
        "domain": "mathematics",
        "severity": "medium",
        "kind": "derivation",
        "evidence_ids": ("aud17-fixed-channel-fisher-derivation",),
        "statement": "For a finite centered score family and a fixed parameter-independent Markov channel, the fine Fisher form decomposes exactly into the coarse Fisher form plus conditional score covariance.",
    },
    {
        "id": "AUD-18-DEFECT-REPRODUCTION",
        "domain": "code",
        "severity": "low",
        "kind": "mechanical",
        "evidence_ids": ("aud18-defect-targeted-counterevidence",),
        "statement": "The AUD-18 machine-scale negative KL cancellation result still escapes unclamped at this artifact revision.",
    },
    {
        "id": "AUD-18-CORRECTED-CONTRACT",
        "domain": "code",
        "severity": "low",
        "kind": "mechanical",
        "evidence_ids": ("aud18-routing-targeted-evidence",),
        "statement": "Every floating KL path in vfe, agent_network, and counterexamples reaches the one stable reducer and preserves its public support-failure carrier at this artifact revision.",
    },
)

EVIDENCE_SPECS_BY_CLAIM = {
    "AUD-03-DEFECT-REPRODUCTION": (
        "aud03-defect-targeted-counterevidence", "mechanical", False,
        "targeted.xml",
    ),
    "AUD-03-CORRECTED-CONTRACT": (
        "aud03-kl-nonnegativity-derivation", "derivation", True,
        "derivations/stable-kl-bound.json#/analytic_probability_and_kl_derivation",
    ),
    "AUD-13-DEFECT-REPRODUCTION": (
        "aud13-defect-targeted-counterevidence", "mechanical", False,
        "targeted.xml",
    ),
    "AUD-13-CORRECTED-CONTRACT": (
        "aud13-contract-targeted-evidence", "mechanical", True, "targeted.xml",
    ),
    "AUD-14-DEFECT-REPRODUCTION": (
        "aud14-defect-targeted-counterevidence", "mechanical", False,
        "targeted.xml",
    ),
    "AUD-14-CORRECTED-CONTRACT": (
        "aud14-contract-targeted-evidence", "mechanical", True, "targeted.xml",
    ),
    "AUD-15-DEFECT-REPRODUCTION": (
        "aud15-defect-targeted-counterevidence", "mechanical", False,
        "targeted.xml",
    ),
    "AUD-15-CORRECTED-CONTRACT": (
        "aud15-spectral-quotient-derivation", "derivation", True,
        "derivations/spectral-and-quotient.json#/exact_diagonal_quotient_algebra",
    ),
    "AUD-16-DEFECT-REPRODUCTION": (
        "aud16-defect-targeted-counterevidence", "mechanical", False,
        "targeted.xml",
    ),
    "AUD-16-CORRECTED-CONTRACT": (
        "aud16-loewner-recovery-derivation", "derivation", True,
        "derivations/fisher-recovery-and-provenance.json#/exact_loewner_and_recovery_derivation",
    ),
    "AUD-17-DEFECT-REPRODUCTION": (
        "aud17-defect-targeted-counterevidence", "mechanical", False,
        "targeted.xml",
    ),
    "AUD-17-CORRECTED-CONTRACT": (
        "aud17-fixed-channel-fisher-derivation", "derivation", True,
        "derivations/fisher-recovery-and-provenance.json#/exact_six_state_fisher_witness",
    ),
    "AUD-18-DEFECT-REPRODUCTION": (
        "aud18-defect-targeted-counterevidence", "mechanical", False,
        "targeted.xml",
    ),
    "AUD-18-CORRECTED-CONTRACT": (
        "aud18-routing-targeted-evidence", "mechanical", True, "targeted.xml",
    ),
}

INITIAL_VIEW_IDS = ("code-runtime", "exact-oracle")
TARGET4_ADDITIONAL_VIEW_IDS = ("numerical-analysis", "information-geometry")
TARGET8_ADDITIONAL_VIEW_IDS = (
    "boundary-review",
    "adversarial-numerics",
    "api-compatibility",
    "provenance-review",
)
VIEW_IDS_BY_TARGET = {
    2: INITIAL_VIEW_IDS,
    4: INITIAL_VIEW_IDS + TARGET4_ADDITIONAL_VIEW_IDS,
    8: (
        INITIAL_VIEW_IDS
        + TARGET4_ADDITIONAL_VIEW_IDS
        + TARGET8_ADDITIONAL_VIEW_IDS
    ),
}
INITIAL_REVIEW_PATHS = (
    "reviews/code-runtime.json",
    "reviews/exact-oracle.json",
)
TARGET4_ADDITIONAL_REVIEW_PATHS = (
    "reviews/escalation/numerical-analysis.json",
    "reviews/escalation/information-geometry.json",
)
TARGET8_ADDITIONAL_REVIEW_PATHS = (
    "reviews/escalation/boundary-review.json",
    "reviews/escalation/adversarial-numerics.json",
    "reviews/escalation/api-compatibility.json",
    "reviews/escalation/provenance-review.json",
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
SKEPTIC_PATHS = (
    "reviews/skeptics/AUD-03-DEFECT-REPRODUCTION.json",
    "reviews/skeptics/AUD-03-CORRECTED-CONTRACT.json",
)
ADJUDICATOR_PATHS = (
    "reviews/adjudicators/AUD-03-DEFECT-REPRODUCTION.json",
    "reviews/adjudicators/AUD-03-CORRECTED-CONTRACT.json",
    "reviews/adjudicators/AUD-13-DEFECT-REPRODUCTION.json",
    "reviews/adjudicators/AUD-13-CORRECTED-CONTRACT.json",
    "reviews/adjudicators/AUD-14-DEFECT-REPRODUCTION.json",
    "reviews/adjudicators/AUD-14-CORRECTED-CONTRACT.json",
    "reviews/adjudicators/AUD-15-DEFECT-REPRODUCTION.json",
    "reviews/adjudicators/AUD-15-CORRECTED-CONTRACT.json",
    "reviews/adjudicators/AUD-16-DEFECT-REPRODUCTION.json",
    "reviews/adjudicators/AUD-16-CORRECTED-CONTRACT.json",
    "reviews/adjudicators/AUD-17-DEFECT-REPRODUCTION.json",
    "reviews/adjudicators/AUD-17-CORRECTED-CONTRACT.json",
    "reviews/adjudicators/AUD-18-DEFECT-REPRODUCTION.json",
    "reviews/adjudicators/AUD-18-CORRECTED-CONTRACT.json",
)
ALLOWED_ESCALATION_TRIGGERS = (
    "small_margin",
    "high_dispersion",
    "criterion_disagreement",
    "high_severity",
)
REVIEW_RECORD_FIELDS = (
    "schema_version",
    "view_id",
    "calibration_kind",
    "tested_git_head",
    "implementation_parent_git_head",
    "reviewed_input_inventory_sha256",
    "reviewed_paths",
    "claim_scores",
    "verdict",
    "escalation_triggers",
    "unresolved_disagreement",
    "open_obligations",
    "result_location",
    "falsification_conditions",
)
CLAIM_SCORE_FIELDS = (
    "claim_id",
    "domain",
    "severity",
    "evidence_ids",
    "criteria",
    "verdict",
    "escalation_triggers",
    "unresolved_disagreement",
    "open_obligations",
)
INITIAL_CLAIM_SCORE_EXTRA_FIELDS = (
    "candidate_ids",
    "candidate_descriptions",
    "comparison_order",
    "comparison_outcome",
    "comparison_criteria",
)
VERIFIER_RECORD_FIELDS = (
    "schema_version",
    "role",
    "claim_id",
    "tested_git_head",
    "implementation_parent_git_head",
    "reviewed_input_inventory_sha256",
    "escalation_triggers",
    "escalation_target",
    "view_ids",
    "result",
    "evidence_ids",
    "result_location",
    "reason",
    "falsification_condition",
    "open_obligations",
)
VERIFIER_ROLES = ("verifier-skeptic", "verifier-adjudicator")
VERIFIER_RESULTS = ("support", "refute", "abstain")
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
GENERIC_NON_INDEX_PUBLIC_PATHS = (
    "commands/full.json",
    "commands/subsystem.json",
    "commands/targeted.json",
    "dependencies.json",
    "environment.json",
    "full.xml",
    "plan-binding.json",
    "privacy-transform.json",
    "subsystem.xml",
    "targeted.xml",
)
UPSTREAM_PUBLIC_PATHS = ("upstream-wave0-plan.json",)
DERIVATION_PUBLIC_PATHS = (
    "derivations/fisher-recovery-and-provenance.json",
    "derivations/probability-canonicalization.json",
    "derivations/spectral-and-quotient.json",
    "derivations/stable-kl-bound.json",
)
DOMAIN_EVIDENCE_FIELDS = (
    "schema_version",
    "wave",
    "evidence_stage",
    "tested_git_head",
    "implementation_parent_git_head",
    "generic_non_index_inventory_sha256",
    "artifacts",
)
DOMAIN_BASE_PUBLIC_PATHS = DERIVATION_PUBLIC_PATHS + ("domain-evidence.json",)
CANDIDATE_PUBLIC_PATHS = (
    GENERIC_PUBLIC_PATHS + UPSTREAM_PUBLIC_PATHS + DOMAIN_BASE_PUBLIC_PATHS
)
CLOSURE_PUBLIC_PATHS_BY_TARGET = {
    4: (
        GENERIC_PUBLIC_PATHS
        + UPSTREAM_PUBLIC_PATHS
        + DOMAIN_BASE_PUBLIC_PATHS
        + REVIEW_PATHS_BY_TARGET[4]
        + SKEPTIC_PATHS
        + ADJUDICATOR_PATHS
    ),
    8: (
        GENERIC_PUBLIC_PATHS
        + UPSTREAM_PUBLIC_PATHS
        + DOMAIN_BASE_PUBLIC_PATHS
        + REVIEW_PATHS_BY_TARGET[8]
        + SKEPTIC_PATHS
        + ADJUDICATOR_PATHS
    ),
}
```

- [ ] **Step 1: Write literal RED tests for every adapter command and the 14-claim inventory**

Create `tests/test_wave_a_evidence.py` with these imports and fixtures; do not use
undefined helper names:

```python
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

import tools.wave_a_evidence as wave_a_evidence


EXPECTED_CLAIMS = {
    f"AUD-{number:02d}-{suffix}"
    for number in (3, 13, 14, 15, 16, 17, 18)
    for suffix in ("DEFECT-REPRODUCTION", "CORRECTED-CONTRACT")
}


@pytest.fixture
def empty_gate_ledger(tmp_path: Path) -> Path:
    path = tmp_path / "final-ledger.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "mode": "closure",
                "artifact_revision": "git:" + "a" * 40 + ":sha256:" + "b" * 64,
                "claims": [],
            },
            sort_keys=True,
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )
    return path


def test_claim_inventory_is_state_free_and_uses_exact_domain_criteria():
    specs = wave_a_evidence.CLAIM_SPECS
    assert len(specs) == 14
    assert {record["id"] for record in specs} == EXPECTED_CLAIMS
    assert sum(record["severity"] == "high" for record in specs) == 2
    for record in specs:
        assert set(record) == {
            "id", "domain", "severity", "kind", "evidence_ids", "statement"
        }
        assert "state" not in record
        assert record["evidence_ids"] == (
            wave_a_evidence.EVIDENCE_SPECS_BY_CLAIM[record["id"]][0],
        )
        if record["domain"] == "mathematics":
            assert record["kind"] in {"derivation", "formal_proof"}
        if record["domain"] == "code":
            assert record["kind"] in {"mechanical", "reproduced_output"}
    assert tuple(
        key for key, _ in wave_a_evidence.CLAIM_CRITERIA_BY_DOMAIN["code"]
    ) == (
        "execution",
        "input_output_behavior",
        "boundary_failure_behavior",
        "regression_coverage",
        "configuration_reachability",
        "reproducibility",
    )
    assert tuple(
        key for key, _ in wave_a_evidence.CLAIM_CRITERIA_BY_DOMAIN["mathematics"]
    ) == (
        "statement_precision",
        "definitions_domains",
        "assumptions",
        "derivation_validity",
        "theorem_lemma_dependencies",
        "limiting_cases",
        "counterexample_search",
        "notation_conclusion_agreement",
    )
    forbidden = {"coverage", "freshness", "artifact_bound_correctness"}
    assert not forbidden.intersection(
        key
        for records in wave_a_evidence.CLAIM_CRITERIA_BY_DOMAIN.values()
        for key, _ in records
    )


def test_review_tiers_and_public_inventories_are_closed():
    assert wave_a_evidence.VIEW_IDS_BY_TARGET[2] == (
        "code-runtime", "exact-oracle"
    )
    assert len(wave_a_evidence.VIEW_IDS_BY_TARGET[4]) == 4
    assert len(wave_a_evidence.VIEW_IDS_BY_TARGET[8]) == 8
    assert len(wave_a_evidence.CANDIDATE_PUBLIC_PATHS) == 17
    assert len(wave_a_evidence.CLOSURE_PUBLIC_PATHS_BY_TARGET[4]) == 37
    assert len(wave_a_evidence.CLOSURE_PUBLIC_PATHS_BY_TARGET[8]) == 41
    assert len(wave_a_evidence.ADJUDICATOR_PATHS) == 14
    assert set(wave_a_evidence.ADJUDICATOR_PATHS) == {
        f"reviews/adjudicators/{claim_id}.json" for claim_id in EXPECTED_CLAIMS
    }
    assert wave_a_evidence.VERIFIER_ROLES == (
        "verifier-skeptic", "verifier-adjudicator"
    )
    assert wave_a_evidence.VERIFIER_RESULTS == (
        "support", "refute", "abstain"
    )
    for paths in (
        wave_a_evidence.CANDIDATE_PUBLIC_PATHS,
        *wave_a_evidence.CLOSURE_PUBLIC_PATHS_BY_TARGET.values(),
    ):
        assert len(paths) == len(set(paths))


def test_wave0_pass_plan_binding_is_exact_and_public():
    path = (
        "docs/superpowers/plans/"
        "2026-08-11-scientific-integrity-remediation-wave-0.md"
    )
    digest = (
        "dbe2263a3b0fe1e9f5db4ff1fca9a19"
        "f819cfd32ef38da71d6e5cb5485723ac2"
    )
    assert wave_a_evidence.UPSTREAM_WAVE0_PLAN_PATH == path
    assert wave_a_evidence.UPSTREAM_WAVE0_PLAN_SHA256 == digest
    assert wave_a_evidence.UPSTREAM_WAVE0_PUBLIC_PATH == (
        "upstream-wave0-plan.json"
    )
    assert wave_a_evidence.UPSTREAM_PUBLIC_PATHS == (
        "upstream-wave0-plan.json",
    )
    assert path in wave_a_evidence.WAVE_A_DEPENDENCY_INPUTS
    assert path in wave_a_evidence.WAVE_A_REQUIRED_SOURCE_CONFIG_BINDINGS
    assert f"exact:{path}" in (
        wave_a_evidence.WAVE_A_TESTED_INPUT_POLICY["selection_rules"]
    )
    assert wave_a_evidence.UPSTREAM_WAVE0_RECORD_FIELDS == (
        "schema_version", "path", "size_bytes", "sha256"
    )


def test_domain_evidence_contract_has_no_final_index_back_edge():
    assert wave_a_evidence.DOMAIN_EVIDENCE_FIELDS == (
        "schema_version",
        "wave",
        "evidence_stage",
        "tested_git_head",
        "implementation_parent_git_head",
        "generic_non_index_inventory_sha256",
        "artifacts",
    )
    assert "base_index" not in wave_a_evidence.DOMAIN_EVIDENCE_FIELDS
    assert "index.json" not in wave_a_evidence.GENERIC_NON_INDEX_PUBLIC_PATHS
    assert set(wave_a_evidence.GENERIC_NON_INDEX_PUBLIC_PATHS) == (
        set(wave_a_evidence.GENERIC_PUBLIC_PATHS) - {"index.json"}
    )
    sample = [{"path": "environment.json", "size_bytes": 1, "sha256": "0" * 64}]
    digest = hashlib.sha256(
        wave_a_evidence.canonical_json_bytes(sample)
    ).hexdigest()
    assert len(digest) == 64
    for public_paths in (
        wave_a_evidence.CANDIDATE_PUBLIC_PATHS,
        *wave_a_evidence.CLOSURE_PUBLIC_PATHS_BY_TARGET.values(),
    ):
        assert set(public_paths) - {"index.json"} == {
            path for path in public_paths if path != "index.json"
        }


def test_adapter_cli_is_closed_and_has_no_second_pytest_or_environment_writer():
    parser = wave_a_evidence.build_parser()
    assert parser.parse_args([
        "build", "--stage", "candidate", "--tested-head", "a" * 40,
        "--implementation-parent", "a" * 40, "--raw-dir", ".verification/raw",
        "--output-dir", "docs/verification/evidence/wave-a/aaaaaaaaaaaa",
    ]).command == "build"
    for command in ("review-context-sha", "review-target", "validate-reviews"):
        assert parser.parse_args([
            command,
            "--tested-head", "b" * 40,
            "--implementation-parent", "a" * 40,
            "--raw-dir", ".verification/raw",
        ]).command == command
    assert parser.parse_args([
        "validate-domain", "--bundle-dir",
        "verification-evidence/wave-a/bbbbbbbbbbbb",
    ]).command == "validate-domain"
    assert parser.parse_args([
        "populate-ledger", "--ledger", ".verification/wave-a/final-ledger.json",
        "--closure-index", "verification-evidence/wave-a/bbbbbbbbbbbb/index.json",
        "--domain-index",
        "verification-evidence/wave-a/bbbbbbbbbbbb/domain-evidence.json",
    ]).command == "populate-ledger"
    assert not hasattr(wave_a_evidence, "run_pytest")
    assert not hasattr(wave_a_evidence, "write_environment")
    assert not hasattr(wave_a_evidence, "write_index")


def test_skip_allowlist_is_the_exact_frozen_per_suite_mapping():
    assert wave_a_evidence.SKIP_ALLOWLIST_BY_SUITE["targeted"] == {}
    assert wave_a_evidence.SKIP_ALLOWLIST_BY_SUITE["subsystem"] == {}
    full = wave_a_evidence.SKIP_ALLOWLIST_BY_SUITE["full"]
    assert len(full) == 6
    assert full[
        "tests.test_cuda_backend::test_pinned_cuda_worker_runs_first_job_with_determinism_environment"
    ] == "requires explicit dedicated CUDA-lane opt-in"
    assert set(full.values()) == {
        "capability unavailable: symbolic_link",
        "capability unavailable: hard_link",
        "requires explicit dedicated CUDA-lane opt-in",
    }


def test_derivation_records_separate_exact_and_numerical_evidence():
    files = wave_a_evidence.prepare_derivation_files(
        implementation_head="1" * 40,
        tested_head="2" * 40,
    )
    payloads = {str(item.path): json.loads(item.data) for item in files}
    probability = payloads["probability-canonicalization.json"]
    kl = payloads["stable-kl-bound.json"]
    spectral = payloads["spectral-and-quotient.json"]
    fisher = payloads["fisher-recovery-and-provenance.json"]
    assert probability["evidence_classes"] == ["mechanical", "numerical"]
    assert kl["evidence_classes"] == ["derivation", "numerical"]
    assert spectral["evidence_classes"] == ["derivation", "numerical"]
    assert fisher["evidence_classes"] == ["derivation", "numerical"]


def test_populate_ledger_rejects_a_nonempty_gate_template_before_indexes(
    empty_gate_ledger: Path, tmp_path: Path
):
    payload = json.loads(empty_gate_ledger.read_text(encoding="utf-8"))
    payload["claims"] = [{"id": "preexisting"}]
    empty_gate_ledger.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="empty closure template"):
        wave_a_evidence.populate_ledger(
            closure_index=tmp_path / "missing-index.json",
            domain_index=tmp_path / "missing-domain-evidence.json",
            ledger=empty_gate_ledger,
        )
```

In the same temporary two-commit repository fixtures used by Wave 0, add literal
negative tests for: swapped candidate/closure heads; a non-direct evidence child;
an output directory that already exists; a raw path outside `.verification/raw/`;
an omitted required source/config binding; an untracked matching input; a changed
`pyproject.toml`, CUDA-lock, reviewed Wave A plan byte/commit/blob, frozen Wave 0
PASS-plan byte/path/SHA or `upstream-wave0-plan.json` field, or verification
snapshot byte/active-file hash; any non-pinned root or fallback gate resolution; an
unknown/missing/case-aliased domain file; review or derivation path/privacy
tampering; an absolute path hidden in an argv token, interpreter, `PYTHONPATH`,
review/result field, or XML node; a closure build/index attempted before validated
external reviews; an unselected tier or fabricated view; criterion mean drift; a
generic non-index byte changed without a matching canonical inventory digest; a
`domain-evidence.json` containing `base_index`, `index.json`, an upstream/generic
artifact, or any other final-index path/size/SHA back-edge; a final index that
omits any public artifact, includes itself, or fails to detect a mutated upstream
or domain byte; a nonzero command; every unallowlisted skip and reason mutation; a
failure injected before `publish_evidence_bundle`; and a failure injected during publication. Every
preparation failure must leave the destination and its parent byte-identical. The
injected publication failure may remove only its newly created sibling and must
leave no destination.

Run the RED command and preserve its JUnit even though it contains failures:

```powershell
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'
C:\Python314\python.exe -B -m pytest tests\test_wave_a_evidence.py tests\test_remediation_evidence.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task8-red --junitxml=C:\tmp\multiagentelbo-wave-a-task8-red.xml
```

Expected: FAIL because `tools.wave_a_evidence` does not exist.

- [ ] **Step 2: Implement the adapter and ledger writer, then run GREEN**

Implement canonical JSON with `sort_keys=True`, compact separators,
`allow_nan=False`, UTF-8, and a trailing newline. Every output except the gate's
already-created empty ledger is create-once. Implement each subcommand as follows:

1. `build` owns the literal targeted, subsystem, and full argv definitions and
   `SKIP_ALLOWLIST_BY_SUITE`. It requires all raw command/JUnit pairs below the
   exact ignored `.verification/raw/wave-a/{tested-short}/{stage}/` directory,
   rejects an output other than
   `docs/verification/evidence/wave-a/{tested-short}` for `candidate` or
   `verification-evidence/wave-a/{tested-short}` for `closure`, and passes
   `wave="wave-a"`, the two heads, parsed raw records, the literal
   `WAVE_A_TESTED_INPUT_POLICY`, exact source/config paths, exact dependency
   inputs, and raw JUnit bytes to `prepare_evidence_bundle`. No caller supplies a
   tested-input list. The generic preparation creates the exact six-key
   environment record, scrubbed public JUnit, command metadata, discovered
   `reviewed_plan_binding`, validated `verification_contract_binding`, and
   closed `remediation-evidence-v1` index entirely in memory. The wrapper asserts its
   environment-variable key set equals `EXPECTED_ENVIRONMENT_KEYS`, requires
   `CUDA_VISIBLE_DEVICES="-1"` and `PYTHONHASHSEED="0"`, and requires the three
   CUDA opt-in/device variables to be JSON null.
2. Resolve source/config bindings as the sorted literal
   `WAVE_A_REQUIRED_SOURCE_CONFIG_BINDINGS` plus every tracked regular file under
   `docs/verification/remediation/`. Reject a missing/extra/case-aliased binding,
   an untracked match, symlink/reparse input, or a path absent from the exhaustive
   tested-input inventory. It requires the reviewed Wave A plan's current
   size/hash plus its discovered last-touch commit/blob relationship; independently
   rereads `UPSTREAM_WAVE0_PLAN_PATH` and requires exact
   `UPSTREAM_WAVE0_PLAN_SHA256` in the tested, source/config, dependency, and
   upstream-record views; and validates all nine active files in
   `verification-contract-v1.json` against the explicit
   `.codex/skills/verification` root. `dependency_input_paths` is exactly
   `WAVE_A_DEPENDENCY_INPUTS` in its four-item order; `uv.lock` is
   live-checkout WIP only and is never an isolated Wave A evidence dependency.
3. `prepare_wave_a_bundle` reads each raw derivation and, for closure, each
   selected review, skeptic, and adjudicator exactly once after
   `validate-reviews` has bound it to `review-context.json`. It applies the
   imported Wave 0 `privacy_transform_bytes` to every raw or generated public
   preimage: command JSON, JUnit XML, environment/dependency/plan/snapshot
   records, derivations, reviews, skeptics, and adjudicators. It also prepares
   `upstream-wave0-plan.json` from the already validated exact repository-relative
   source record; the caller cannot supply its path or digest. The structural
   walker handles interpreter, `cwd`, every argv token and
   `--option=VALUE`, every environment value and `PYTHONPATH` component,
   dependency/plan/snapshot/review/result/JUnit paths, XML text/attributes,
   Windows drive/UNC/device paths, POSIX absolute paths, hostname, and PID
   fields. Only the Wave 0 placeholder vocabulary is permitted. A second
   transform must be byte-identical, and parsed raw-to-public semantic
   comparison must preserve all nonprivate content.
   The one `privacy-transform.json` contains sorted closed
   `{raw_relative_path,raw_sha256,public_path,public_sha256,transforms}` records
   for every such preimage. `upstream-wave0-plan.json`, `index.json`,
   `privacy-transform.json`, and `domain-evidence.json` have no raw self-preimage
   and are separately scanned for private tokens before hashing. The adapter
   forms `generic_non_index_inventory` as the ASCII-path-sorted closed
   `{path,kind,size_bytes,sha256}` records for exactly
   `GENERIC_NON_INDEX_PUBLIC_PATHS` and computes
   `sha256(canonical_json_bytes(generic_non_index_inventory)).hexdigest()`. It
   then writes in memory a closed `wave-a-domain-evidence-v1` record with exactly
   `DOMAIN_EVIDENCE_FIELDS`. `generic_non_index_inventory_sha256` is that digest.
   `artifacts` is a sorted list of `{path,kind,size_bytes,sha256}` containing
   only sanitized derivation/review/skeptic/adjudicator domain artifacts. It
   excludes `domain-evidence.json`, `upstream-wave0-plan.json`, every generic
   artifact, and `index.json`. No final-index path, size, hash, or record may
   occur in `domain-evidence.json`.
4. Discard the generic builder's provisional index, then merge the generic
   non-index prepared files, exact upstream record, sanitized domain files, and
   `domain-evidence.json` into one immutable `PreparedEvidenceBundle`. Construct
   the one final `index.json` last; its `files` array hashes every path in the
   stage's exact public contract except `index.json` itself. Before any write,
   validate the complete virtual map: both heads/stage, the recomputed canonical
   generic-non-index digest, every generic/upstream/domain byte, exact allowed
   path set, no aliases/traversal, no final-index self-entry or domain back-edge,
   and no private token. Candidate requires exactly
   `CANDIDATE_PUBLIC_PATHS` (17 files) and rejects every review path. Closure
   requires exactly `CLOSURE_PUBLIC_PATHS_BY_TARGET[4]` (37 files) or
   `CLOSURE_PUBLIC_PATHS_BY_TARGET[8]` (41 files), including all selected
   external views, both high-severity skeptics, and all 14 adjudicators. No
   closure directory or index may exist before review validation. Call
   `publish_evidence_bundle` exactly once, then
   `validate_evidence_index` and `validate-domain` from disk. The destination and
   its parent remain byte-identical on every preparation failure; publication
   failure removes only its exact new sibling and leaves no destination.
5. `review-context-sha` creates a closed `wave-a-review-context-v1` payload with
   exact fields `schema_version`, both full heads, `evidence_diff_inventory`,
   `candidate_evidence_inventory`, raw command/JUnit inventories,
   tested/source/dependency/environment inventories, `reviewed_plan_bytes`,
   `upstream_wave0_plan_bytes`, `verification_snapshot_bytes`,
   `derivation_inventory`, `claim_specs`, and `public_path_contracts`. Every
   inventory item is a sorted closed
   `{path,size_bytes,sha256}` record. The command independently proves `E^=P`,
   validates candidate bytes and exact source/config state, writes only
   `$rawDir/review-context.json`, and prints its canonical digest. Mutating any
   nested byte, head, plan commit/blob, frozen Wave 0 path/source
   SHA/public-record hash, snapshot active-file hash, generic-non-index inventory
   digest, claim, criterion, path contract, or environment value changes or
   invalidates the digest. `upstream_wave0_plan_bytes` is the closed source
   `{path,size_bytes,sha256}` record plus the public
   `{path,size_bytes,sha256}` record, and its source SHA must equal
   `UPSTREAM_WAVE0_PLAN_SHA256`.

   Each external review record has exactly `REVIEW_RECORD_FIELDS`. Each claim
   score has exactly `CLAIM_SCORE_FIELDS`, and every `criteria` member has
   exactly the claim domain's stable criterion keys with integer scores in
   `[0,20]`. Initial claim scores additionally have exactly
   `INITIAL_CLAIM_SCORE_EXTRA_FIELDS`. Candidate A is the literal statement and candidate B
   its explicit negation. `code-runtime` records AB and `exact-oracle` BA;
   `comparison_criteria` equals the claim's exact domain criteria. Scores are
   integers in `[0,20]` and
   `calibration_kind="independent_pairwise_source_reading_v1"`.

   Initial records score all 14 claims. Target-4 and target-8 records score only
   the nonempty claim subset whose current target selects that tier; padding an
   untriggered claim is invalid. The two high claims always retain
   `high_severity` and target 4. Any initial `small_margin`,
   `high_dispersion`, or `criterion_disagreement` also selects target 4 for
   that claim. Unresolved `criterion_disagreement` after four selects target 8;
   after eight it remains unresolved and requires `INCONCLUSIVE`. Trigger
   removal, target regression, an unselected review, or majority resolution is
   invalid.

   Both high claims have one closed `verifier-skeptic` record at the literal
   `SKEPTIC_PATHS`. Every claim has one closed `verifier-adjudicator` record at
   its literal `ADJUDICATOR_PATHS` member. Both record types have exactly
   `VERIFIER_RECORD_FIELDS`; `role` selects one value from `VERIFIER_ROLES` and
   no field may be omitted or added. Thus each record explicitly binds both
   heads, the review-context digest, exact trigger set/target/calibrated view
   IDs, stable eligible evidence IDs, public result location, result, reason,
   falsification condition, and open obligations. Results are exactly
   `VERIFIER_RESULTS`. Missing
   eligible evidence or disagreement requires `abstain` and a nonempty
   obligation. `validate-reviews` rejects any missing/extra/unknown field,
   fabricated view, wrong criterion, mean drift, head/context drift, stale
   evidence ID, unselected tier, or private path before closure construction.
6. `populate-ledger` first validates the exact ledger path and reads the gate
   template; it rejects anything except the closed four-field, closure-mode,
   concrete-artifact-revision, empty-claims template before reading an index. It
   then requires the final closure index and `domain-evidence.json`, exact
   `git rev-parse HEAD` equality, the reviewed plan binding, frozen Wave 0
   source/upstream-record binding, pinned snapshot binding, review-context
   digest, and every selected indexed review/skeptic/adjudicator byte. It revalidates the
   complete on-disk union, constructs all claims from the state-free
   `CLAIM_SPECS` plus those external records, and atomically replaces only the
   already-created empty ledger. It refuses a ledger path other than
   `.verification/wave-a/final-ledger.json` and refuses index paths outside the
   exact current closure directory. It never copies a SHA into the evidence
   revision and instead uses the gate template's complete `artifact_revision`
   string.

For each ledger claim, candidate IDs are `claim-statement` and
`explicit-negation` with nonempty literal descriptions. Pairwise method,
`orders=["AB","BA"]`, and the complete two-match grid come byte-for-byte from
the indexed initial reviews. Every match uses its recorded view ID, outcome,
exact domain criterion map, and public result location. Escalation reviews add
scores only. For every criterion, the aggregate is exactly
`sum(view_scores[key]) / escalation_target` across the selected 2, 4, or 8
views, with no weighting or pre-serialization rounding.

The sole eligible record for each claim is the literal
`EVIDENCE_SPECS_BY_CLAIM` member and the identical ID in `CLAIM_SPECS`. Code
claims use current `mechanical` evidence; mathematics claims use only current
`derivation` evidence for closure. JUnit may corroborate a mathematics
implementation but cannot close its theorem. `index.json` and
`domain-evidence.json` are structural prerequisites and are forbidden from
claim evidence and verifier `evidence_ids`.

Population derives state from the indexed adjudicator; it never receives an
expected state. `support` plus current domain-eligible supporting evidence maps
to `EVIDENCE_VERIFIED`. `refute` plus current domain-eligible
`supports=false` counterevidence maps to `REFUTED`. `abstain`, missing eligible
evidence, or unresolved disagreement maps to `INCONCLUSIVE` with the exact
nonempty obligation. Any inconsistent result/evidence polarity fails. Every
terminal claim has exactly one indexed `verifier-adjudicator` linked to all
selected views and its stable eligible ID. The two high claims also have exactly
one indexed `verifier-skeptic`. Closed claims have no obligation and
`evidence_invalidated=false`; no vote or `CLAIM_SPECS` default can change a
state.

The four derivation files have these honest evidence boundaries:

- `probability-canonicalization.json` is a mechanical/numerical record of float64
  `math.fsum`, correction, rejection, and bytes-backing behavior; it is not an
  exact proof merely because JSON is deterministic.
- `stable-kl-bound.json` contains an exact analytic derivation of KL
  nonnegativity for normalized probability laws and a separately labeled
  numerical float64 cancellation/bound/clamp record. Floating `math.log` values
  are numerical evidence.
- `spectral-and-quotient.json` contains exact diagonal/rational mask,
  pseudoinverse, projector, and rank algebra plus a separately labeled SciPy
  eigensolver/uncertainty-policy record.
- `fisher-recovery-and-provenance.json` contains exact `Fraction` Loewner/control
  and six-state Fisher derivations plus a separately labeled numerical whitened
  relative-loss assessment. The exact sections, not numerical agreement, support
  the mathematics claims.

Run GREEN and require zero JUnit failures/errors:

```powershell
$ErrorActionPreference = 'Stop'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'
C:\Python314\python.exe -B -m pytest tests\test_wave_a_evidence.py tests\test_remediation_evidence.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-task8-green --junitxml=C:\tmp\multiagentelbo-wave-a-task8-green.xml
if ($LASTEXITCODE -ne 0) { throw 'Task 8 adapter tests failed' }
[xml]$task8 = Get-Content -Raw -LiteralPath 'C:\tmp\multiagentelbo-wave-a-task8-green.xml'
$task8Suites = @($task8.testsuites.testsuite)
if ([int](($task8Suites | Measure-Object failures -Sum).Sum) -ne 0 -or [int](($task8Suites | Measure-Object errors -Sum).Sum) -ne 0) { throw 'Task 8 adapter JUnit is not green' }
C:\Python314\python.exe -m ruff check --no-cache tools/wave_a_evidence.py tests/test_wave_a_evidence.py
if ($LASTEXITCODE -ne 0) { throw 'Task 8 lint failed' }
C:\Python314\python.exe -m ruff format --check --no-cache tools/wave_a_evidence.py tests/test_wave_a_evidence.py
if ($LASTEXITCODE -ne 0) { throw 'Task 8 format check failed' }
git add -- tools/wave_a_evidence.py tests/test_wave_a_evidence.py
git commit -m "test: add wave A evidence and ledger adapter"
```

- [ ] **Step 3: Establish the clean implementation parent with machine-readable checks**

```powershell
$ErrorActionPreference = 'Stop'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'
if (Test-Path Env:MULTIAGENTELBO_RUN_CUDA_TESTS) { throw 'CUDA opt-in is still set' }
C:\Python314\python.exe -B -m pytest tests\test_measures.py tests\test_vfe.py tests\test_agent_network.py tests\test_conditioning.py tests\test_fisher.py tests\test_information_history.py tests\test_information_history_experiment.py tests\test_interactions.py tests\test_gaussian_realization.py tests\test_scale_cocycle.py tests\test_scale_cocycle_experiment.py tests\test_shared_scientific_contracts.py tests\test_counterexamples.py tests\test_wave_a_evidence.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-final-targeted --junitxml=C:\tmp\multiagentelbo-wave-a-final-targeted.xml
if ($LASTEXITCODE -ne 0) { throw 'implementation-parent targeted suite failed' }
C:\Python314\python.exe -B -m pytest tests\test_measures.py tests\test_vfe.py tests\test_agent_network.py tests\test_finite_experiment.py tests\test_categorical_dqm.py tests\test_categorical_dqm_experiment.py tests\test_fisher.py tests\test_information_history.py tests\test_information_history_experiment.py tests\test_interactions.py tests\test_conditioning.py tests\test_gaussian_realization.py tests\test_scale_cocycle.py tests\test_scale_cocycle_experiment.py tests\test_shared_scientific_contracts.py tests\test_counterexamples.py tests\test_wave_a_evidence.py tests\test_remediation_evidence.py -q -p no:cacheprovider --basetemp=.pytest-wave-a-final-subsystem --junitxml=C:\tmp\multiagentelbo-wave-a-final-subsystem.xml
if ($LASTEXITCODE -ne 0) { throw 'implementation-parent subsystem suite failed' }
foreach ($xmlPath in @('C:\tmp\multiagentelbo-wave-a-final-targeted.xml','C:\tmp\multiagentelbo-wave-a-final-subsystem.xml')) {
    [xml]$xml = Get-Content -Raw -LiteralPath $xmlPath
    $suites = @($xml.testsuites.testsuite)
    if ([int](($suites | Measure-Object failures -Sum).Sum) -ne 0 -or [int](($suites | Measure-Object errors -Sum).Sum) -ne 0) { throw "non-green JUnit: $xmlPath" }
}
C:\Python314\python.exe -m ruff check --no-cache src tests tools
if ($LASTEXITCODE -ne 0) { throw 'implementation-parent lint failed' }
C:\Python314\python.exe -m ruff format --check --no-cache src tests tools
if ($LASTEXITCODE -ne 0) { throw 'implementation-parent format check failed' }
git diff --check
if ($LASTEXITCODE -ne 0) { throw 'implementation-parent diff check failed' }
if ((git status --porcelain=v1)) { throw 'implementation parent worktree is not clean' }
$implementationSha = (git rev-parse HEAD).Trim()
$implementationShort = $implementationSha.Substring(0, 12)
$candidateDir = "docs\verification\evidence\wave-a\$implementationShort"
```

- [ ] **Step 4: Produce and commit the exact candidate evidence child**

```powershell
$ErrorActionPreference = 'Stop'
if (git status --porcelain=v1) { throw 'implementation parent is not clean' }
$rawDir = ".verification/raw/wave-a/$implementationShort/candidate"
if (Test-Path -LiteralPath $rawDir) { throw 'candidate raw directory already exists' }
if (Test-Path -LiteralPath $candidateDir) { throw 'candidate evidence directory already exists' }
New-Item -ItemType Directory -Path $rawDir | Out-Null

Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'

C:\Python314\python.exe -B tools\wave_a_evidence.py write-derivations --implementation-head $implementationSha --tested-head $implementationSha --output "$rawDir/domain/derivations"
if ($LASTEXITCODE -ne 0) { throw 'candidate derivation staging failed' }

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/targeted.command.json" --junit "$rawDir/targeted.raw.xml" -- C:\Python314\python.exe -B -m pytest tests\test_measures.py tests\test_vfe.py tests\test_agent_network.py tests\test_conditioning.py tests\test_fisher.py tests\test_information_history.py tests\test_information_history_experiment.py tests\test_interactions.py tests\test_gaussian_realization.py tests\test_scale_cocycle.py tests\test_scale_cocycle_experiment.py tests\test_shared_scientific_contracts.py tests\test_counterexamples.py tests\test_wave_a_evidence.py -q -p no:cacheprovider --basetemp="$rawDir/tmp-targeted" --junitxml="$rawDir/targeted.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'candidate targeted suite failed' }

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/subsystem.command.json" --junit "$rawDir/subsystem.raw.xml" -- C:\Python314\python.exe -B -m pytest tests\test_measures.py tests\test_vfe.py tests\test_agent_network.py tests\test_finite_experiment.py tests\test_categorical_dqm.py tests\test_categorical_dqm_experiment.py tests\test_fisher.py tests\test_information_history.py tests\test_information_history_experiment.py tests\test_interactions.py tests\test_conditioning.py tests\test_gaussian_realization.py tests\test_scale_cocycle.py tests\test_scale_cocycle_experiment.py tests\test_shared_scientific_contracts.py tests\test_counterexamples.py tests\test_wave_a_evidence.py tests\test_remediation_evidence.py -q -p no:cacheprovider --basetemp="$rawDir/tmp-subsystem" --junitxml="$rawDir/subsystem.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'candidate subsystem suite failed' }

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/full.command.json" --junit "$rawDir/full.raw.xml" -- C:\Python314\python.exe -B -m pytest -q -p no:cacheprovider --basetemp="$rawDir/tmp-full" --junitxml="$rawDir/full.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'candidate full suite failed' }

C:\Python314\python.exe -B tools\wave_a_evidence.py build --stage candidate --tested-head $implementationSha --implementation-parent $implementationSha --raw-dir $rawDir --output-dir $candidateDir
if ($LASTEXITCODE -ne 0) { throw 'candidate evidence preparation/publication failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py validate "$candidateDir\index.json" --cwd .
if ($LASTEXITCODE -ne 0) { throw 'candidate generic index validation failed' }
C:\Python314\python.exe -B tools\wave_a_evidence.py validate-domain --bundle-dir $candidateDir
if ($LASTEXITCODE -ne 0) { throw 'candidate domain validation failed' }

$repoRoot = (Resolve-Path '.').Path
$expectedStaged = @(Get-ChildItem -LiteralPath $candidateDir -Recurse -File | ForEach-Object {
    [System.IO.Path]::GetRelativePath($repoRoot, $_.FullName).Replace('\','/')
} | Sort-Object)
git add -- $candidateDir
$candidatePrefix = $candidateDir.Replace('\','/') + '/'
$staged = @(git diff --cached --name-only | Sort-Object)
if (-not $staged) { throw 'candidate evidence staged no files' }
if (@($staged | Where-Object { -not $_.StartsWith($candidatePrefix, [System.StringComparison]::Ordinal) }).Count -ne 0) { throw 'candidate staging escaped its exact directory' }
if (Compare-Object $expectedStaged $staged) { throw 'candidate staged set differs from validated bundle' }
git commit -m "test: record wave A candidate evidence"
if ($LASTEXITCODE -ne 0) { throw 'candidate evidence commit failed' }
$evidenceSha = (git rev-parse HEAD).Trim()
$actualParent = (git rev-parse HEAD^).Trim()
if ($actualParent -ne $implementationSha) { throw 'evidence child is not a direct child of P' }
$candidateDiff = @(git diff --name-only "$implementationSha..$evidenceSha")
if (@($candidateDiff | Where-Object { -not $_.StartsWith($candidatePrefix, [System.StringComparison]::Ordinal) }).Count -ne 0) { throw 'P..E contains a noncandidate path' }
if ((git status --porcelain=v1)) { throw 'candidate child is not clean' }
```

The durable candidate record is historical evidence for `P`; it is not the
exact-child closure record and does not populate the external ledger. Its public
union is exactly the 17 `CANDIDATE_PUBLIC_PATHS`: three sanitized command
records, three scrubbed JUnits, `dependencies.json`, `environment.json`,
`plan-binding.json`, `upstream-wave0-plan.json`, `privacy-transform.json`,
`domain-evidence.json`, the four sanitized derivations, and `index.json`. The
final index hashes all other 16 public artifacts and also binds the complete
tested/source inventory, frozen Wave 0 PASS-plan identity, and pinned
verification snapshot. Raw JUnit, raw command
records, basetemps, review files, host paths, process identifiers, and gate
telemetry remain ignored and are never committed.

- [ ] **Step 5: Run all exact-child closure commands at `E`**

```powershell
$ErrorActionPreference = 'Stop'
$evidenceSha = (git rev-parse HEAD).Trim()
$implementationSha = (git rev-parse HEAD^).Trim()
$evidenceShort = $evidenceSha.Substring(0, 12)
$rawDir = ".verification/raw/wave-a/$evidenceShort/closure"
$closureDir = "verification-evidence\wave-a\$evidenceShort"
if ((git status --porcelain=v1)) { throw 'E is not clean' }
if (Test-Path -LiteralPath $rawDir) { throw 'closure raw directory already exists' }
if (Test-Path -LiteralPath $closureDir) { throw 'closure evidence directory already exists' }
New-Item -ItemType Directory -Path $rawDir | Out-Null

Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/targeted.command.json" --junit "$rawDir/targeted.raw.xml" -- C:\Python314\python.exe -B -m pytest tests\test_measures.py tests\test_vfe.py tests\test_agent_network.py tests\test_conditioning.py tests\test_fisher.py tests\test_information_history.py tests\test_information_history_experiment.py tests\test_interactions.py tests\test_gaussian_realization.py tests\test_scale_cocycle.py tests\test_scale_cocycle_experiment.py tests\test_shared_scientific_contracts.py tests\test_counterexamples.py tests\test_wave_a_evidence.py -q -p no:cacheprovider --basetemp="$rawDir/tmp-targeted" --junitxml="$rawDir/targeted.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'closure targeted suite failed' }

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/subsystem.command.json" --junit "$rawDir/subsystem.raw.xml" -- C:\Python314\python.exe -B -m pytest tests\test_measures.py tests\test_vfe.py tests\test_agent_network.py tests\test_finite_experiment.py tests\test_categorical_dqm.py tests\test_categorical_dqm_experiment.py tests\test_fisher.py tests\test_information_history.py tests\test_information_history_experiment.py tests\test_interactions.py tests\test_conditioning.py tests\test_gaussian_realization.py tests\test_scale_cocycle.py tests\test_scale_cocycle_experiment.py tests\test_shared_scientific_contracts.py tests\test_counterexamples.py tests\test_wave_a_evidence.py tests\test_remediation_evidence.py -q -p no:cacheprovider --basetemp="$rawDir/tmp-subsystem" --junitxml="$rawDir/subsystem.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'closure subsystem suite failed' }

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/full.command.json" --junit "$rawDir/full.raw.xml" -- C:\Python314\python.exe -B -m pytest -q -p no:cacheprovider --basetemp="$rawDir/tmp-full" --junitxml="$rawDir/full.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'closure full suite failed' }

C:\Python314\python.exe -B tools\wave_a_evidence.py write-derivations --implementation-head $implementationSha --tested-head $evidenceSha --output "$rawDir/domain/derivations"
if ($LASTEXITCODE -ne 0) { throw 'closure derivation staging failed' }
```

The targeted and subsystem allowlists are empty. The full allowlist is the literal
six-entry map above. An allowed capability skip may be absent when the host
supports it; every actual skip must match both testcase ID and normalized reason
byte-for-byte. XML observed after a run can never amend this checked-in policy.

- [ ] **Step 6: Bind exact-E inputs, obtain external reviews, then publish once**

First run `review-context-sha`. It must validate every exact-E input, write only
`$rawDir/review-context.json`, print a 64-hex digest, and leave
`$closureDir` absent. Dispatch two independent source-reading agents against
that digest and exact `E/P` bytes. Save their canonical records at
`$rawDir/reviews/code-runtime.json` and
`$rawDir/reviews/exact-oracle.json`. These are external source records: the
adapter may validate and privacy-transform them but may not generate, complete,
or alter any score, trigger, verdict, comparison, or obligation.

Run `review-target`. Because both `AUD-03` claims are high, the initial result
must be 4. Obtain
`reviews/escalation/numerical-analysis.json` and
`reviews/escalation/information-geometry.json` for the high claims and every
other claim selected by an initial trigger. Run `review-target` again. It
returns 8 only if `criterion_disagreement` remains unresolved after four; if
so, obtain exactly the four `TARGET8_ADDITIONAL_REVIEW_PATHS` for the still
disputed claims and require a stable final result of 8.

After the selected view tier exists, obtain the two independent high-severity
skeptic records at `SKEPTIC_PATHS` and one adjudicator source record for each
literal claim at `ADJUDICATOR_PATHS`. Each agent receives the exact review
context, reviewed paths, eligible evidence IDs, and its intended public result
location. It must state a falsification condition; abstention includes a
specific obligation. No majority vote closes a claim. Only after
`validate-reviews` succeeds may the adapter build an index or closure directory.

```powershell
if (Test-Path -LiteralPath $closureDir) { throw 'closure exists before review context' }
$reviewContextSha = (& 'C:\Python314\python.exe' -B tools\wave_a_evidence.py review-context-sha --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir).Trim()
if ($LASTEXITCODE -ne 0 -or $reviewContextSha -notmatch '^[0-9a-f]{64}$') { throw 'review context digest failed' }
if (-not (Test-Path -LiteralPath "$rawDir/review-context.json")) { throw 'review context bytes missing' }
if (Test-Path -LiteralPath $closureDir) { throw 'review context wrote closure bytes' }

# Save the two INITIAL_REVIEW_PATHS as external records described above.
$initialTarget = [int]((& 'C:\Python314\python.exe' -B tools\wave_a_evidence.py review-target --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir).Trim())
if ($LASTEXITCODE -ne 0 -or $initialTarget -ne 4) { throw 'high-severity initial review target must be 4' }

# Save both TARGET4_ADDITIONAL_REVIEW_PATHS for every selected claim.
$reviewTarget = [int]((& 'C:\Python314\python.exe' -B tools\wave_a_evidence.py review-target --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir).Trim())
if ($LASTEXITCODE -ne 0 -or $reviewTarget -notin @(4,8)) { throw 'invalid four-view review result' }

# If reviewTarget is 8, save all four TARGET8_ADDITIONAL_REVIEW_PATHS for
# every still-disputed claim, rerun review-target, and require a stable 8.
if ($reviewTarget -eq 8) {
    $stableTarget = [int]((& 'C:\Python314\python.exe' -B tools\wave_a_evidence.py review-target --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir).Trim())
    if ($LASTEXITCODE -ne 0 -or $stableTarget -ne 8) { throw 'eight-view target is not stable' }
}

# Save both SKEPTIC_PATHS and all 14 ADJUDICATOR_PATHS as external records.
$validatedTarget = [int]((& 'C:\Python314\python.exe' -B tools\wave_a_evidence.py validate-reviews --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir).Trim())
if ($LASTEXITCODE -ne 0 -or $validatedTarget -ne $reviewTarget) { throw 'raw closure review validation failed' }
if (Test-Path -LiteralPath $closureDir) { throw 'review validation wrote closure bytes' }

C:\Python314\python.exe -B tools\wave_a_evidence.py build --stage closure --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir --output-dir $closureDir
if ($LASTEXITCODE -ne 0) { throw 'closure evidence preparation/publication failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py validate "$closureDir\index.json" --cwd .
if ($LASTEXITCODE -ne 0) { throw 'closure generic index validation failed' }
C:\Python314\python.exe -B tools\wave_a_evidence.py validate-domain --bundle-dir $closureDir
if ($LASTEXITCODE -ne 0) { throw 'closure domain validation failed' }

git diff --check
if ($LASTEXITCODE -ne 0) { throw 'closure diff check failed' }
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) { throw 'Git index changed during closure' }
git diff --quiet
if ($LASTEXITCODE -ne 0) { throw 'tracked worktree changed during closure' }

$repoRoot = (Resolve-Path '.').Path
$expectedUntracked = @(Get-ChildItem -LiteralPath $closureDir -Recurse -File | ForEach-Object {
    [System.IO.Path]::GetRelativePath($repoRoot, $_.FullName).Replace('\','/')
} | Sort-Object)
$actualUntracked = @(git ls-files --others --exclude-standard | ForEach-Object { $_.Replace('\','/') } | Sort-Object)
if (Compare-Object $expectedUntracked $actualUntracked) {
    throw 'nonignored untracked set differs from the validated closure union'
}

$freezePath = "C:\tmp\multiagentelbo-wave-a-closure-$evidenceShort.json"
$freeze = Get-ChildItem -LiteralPath $closureDir -Recurse -File | Sort-Object FullName | ForEach-Object {
    [ordered]@{path=[System.IO.Path]::GetRelativePath((Resolve-Path $closureDir),$_.FullName).Replace('\','/');size_bytes=$_.Length;sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()}
}
$freeze | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $freezePath -Encoding utf8NoBOM
$freezeSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $freezePath).Hash
```

The final index inventories the three scrubbed JUnits, normalized environment,
commands, dependencies, exhaustive tested source/config inputs, exact upstream
Wave 0 record, `domain-evidence.json`, four derivations, and exactly 20 sanitized
review records at target 4 or 24 at target 8. `domain-evidence.json` inventories
only those derivation/review domain artifacts and binds the canonical digest of
the ten generic non-index artifacts; it contains no final-index path, size, or
SHA. The one generic `privacy-transform.json` maps every raw
generic/domain/review preimage to its public hash. The validated union is exactly
37 files at target 4 or 41 at target 8 and equals the exact nonignored untracked
set. The final index hashes every public artifact except itself, the sole atomic
publisher writes the union once, and no closure byte changes afterward.

- [ ] **Step 7: Start, populate, and validate the exact 14-claim ledger**

```powershell
$snapshot = 'docs/verification/remediation/verification-contract-v1.json'
$verificationRoot = 'C:\Users\chris and christine\.codex\skills\verification'
$ledgerPath = '.verification\wave-a\final-ledger.json'
if (Test-Path -LiteralPath '.verification\active.json') { throw 'verification gate is already active' }
if (Test-Path -LiteralPath $ledgerPath) { throw 'Wave A ledger already exists' }

& 'C:\Python314\python.exe' -B tools\remediation_evidence.py run-verification-gate --snapshot $snapshot --root $verificationRoot -- start --cwd . --mode closure --ledger $ledgerPath
if ($LASTEXITCODE -ne 0) { throw 'verification gate start failed' }

& 'C:\Python314\python.exe' -B tools\remediation_evidence.py run-verification-gate --snapshot $snapshot --root $verificationRoot -- validate --cwd . $ledgerPath
if ($LASTEXITCODE -eq 0) { throw 'empty gate template unexpectedly validated' }

C:\Python314\python.exe -B tools\wave_a_evidence.py populate-ledger --ledger $ledgerPath --closure-index "$closureDir\index.json" --domain-index "$closureDir\domain-evidence.json"
if ($LASTEXITCODE -ne 0) { throw 'Wave A ledger population failed' }
& 'C:\Python314\python.exe' -B tools\remediation_evidence.py run-verification-gate --snapshot $snapshot --root $verificationRoot -- validate --cwd . $ledgerPath
if ($LASTEXITCODE -ne 0) { throw 'verification gate validation failed' }
$ledger = Get-Content -Raw -LiteralPath $ledgerPath | ConvertFrom-Json
if (@($ledger.claims).Count -ne 14) { throw 'ledger does not contain exactly 14 claims' }
foreach ($claim in $ledger.claims) {
    # This is a post-population publication goal. populate-ledger never receives it.
    $closureGoal = if ($claim.id.EndsWith('DEFECT-REPRODUCTION')) { 'REFUTED' } else { 'EVIDENCE_VERIFIED' }
    if ($claim.state -ne $closureGoal) { throw "publication goal not met: $($claim.id)=$($claim.state)" }
    if (@($claim.verifiers | Where-Object role -eq 'verifier-adjudicator').Count -ne 1) { throw "adjudicator count drift: $($claim.id)" }
    if ($claim.escalation_target -notin @(2,4,8) -or @($claim.views.scores).Count -ne $claim.escalation_target) { throw "view target drift: $($claim.id)" }
    if ($claim.id.StartsWith('AUD-03-')) {
        if ($claim.escalation_target -notin @(4,8) -or @($claim.escalation_triggers) -notcontains 'high_severity') { throw "AUD-03 escalation drift: $($claim.id)" }
        if (@($claim.verifiers | Where-Object role -eq 'verifier-skeptic').Count -ne 1) { throw "AUD-03 skeptic drift: $($claim.id)" }
    } elseif ($claim.escalation_target -gt 2 -and @($claim.escalation_triggers).Count -eq 0) {
        throw "untriggered escalation: $($claim.id)"
    }
    if ($claim.escalation_target -eq 8 -and @($claim.escalation_triggers) -notcontains 'criterion_disagreement') {
        throw "target 8 lacks criterion disagreement: $($claim.id)"
    }
    $pairs = @($claim.views.comparison.matches | ForEach-Object { "$($_.left)>$($_.right)" })
    if ($pairs -notcontains 'claim-statement>explicit-negation' -or $pairs -notcontains 'explicit-negation>claim-statement' -or $pairs.Count -ne 2) { throw "ordered pair grid drift: $($claim.id)" }
}
$freezeAfterPath = "C:\tmp\multiagentelbo-wave-a-closure-$evidenceShort-after-ledger.json"
$freezeAfter = Get-ChildItem -LiteralPath $closureDir -Recurse -File | Sort-Object FullName | ForEach-Object {
    [ordered]@{path=[System.IO.Path]::GetRelativePath((Resolve-Path $closureDir),$_.FullName).Replace('\','/');size_bytes=$_.Length;sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()}
}
$freezeAfter | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $freezeAfterPath -Encoding utf8NoBOM
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $freezeAfterPath).Hash -ne $freezeSha) { throw 'closure bytes changed after freeze' }
```

For each `AUD-03`, `AUD-13`, `AUD-14`, `AUD-15`, `AUD-16`, `AUD-17`, and
`AUD-18`, the independently derived final ledger publishes both the audited
defect proposition as `REFUTED` and the corrected code or pure-mathematics
contract as `EVIDENCE_VERIFIED`. A pure-mathematics claim closes only from its
eligible derivation; current JUnit evidence closes runtime routing and contract
reachability but may only corroborate, never prove, a theorem. Wave A makes no
current CUDA claim.

- [ ] **Step 8: Publish exact `E` and perform a WIP-safe fast-forward**

```powershell
$branch = 'codex/scientific-integrity-remediation-wave-a-20260811'
$liveRepo = 'C:\Users\chris and christine\Desktop\MultiAgentELBO'
$evidenceSha = (git rev-parse HEAD).Trim()
& 'C:\Python314\python.exe' -B tools\remediation_evidence.py run-verification-gate --snapshot $snapshot --root $verificationRoot -- validate --cwd . $ledgerPath
if ($LASTEXITCODE -ne 0) { throw 'pre-publication gate failed' }
git fetch origin
$remoteBefore = (git rev-parse origin/main).Trim()
git merge-base --is-ancestor $remoteBefore $evidenceSha
if ($LASTEXITCODE -ne 0) { throw 'origin/main advanced outside E; rebuild and reclose from the new parent' }
git push -u origin "HEAD:refs/heads/$branch"
$remoteBranch = ((git ls-remote --heads origin "refs/heads/$branch") -split "`t")[0]
if ($remoteBranch -ne $evidenceSha) { throw 'remote feature SHA mismatch' }
git push origin "$evidenceSha`:refs/heads/main"
git fetch origin
if ((git rev-parse origin/main).Trim() -ne $evidenceSha) { throw 'origin/main is not exact E' }
```

If branch protection rejects the main push, stop with the verified feature branch
published; never force, amend, rebase, or create a merge commit. Otherwise run the
local WIP-safe fast-forward with these exact commands:

```powershell
if ((git -C $liveRepo symbolic-ref --short HEAD).Trim() -ne 'main') { throw 'live checkout is not on main' }
git -C $liveRepo fetch origin
if ($LASTEXITCODE -ne 0) { throw 'cannot refresh live checkout remote state' }
if ((git -C $liveRepo rev-parse origin/main).Trim() -ne $evidenceSha) { throw 'live origin/main is not exact E' }
$liveHead = (git -C $liveRepo rev-parse HEAD).Trim()
git -C $liveRepo merge-base --is-ancestor $liveHead $evidenceSha
if ($LASTEXITCODE -ne 0) { throw 'live main is not an ancestor of E' }
$incoming = @(git -C $liveRepo diff --name-only "$liveHead..$evidenceSha" | ForEach-Object { $_.Replace('\','/') })
if ($incoming -contains 'uv.lock') { throw 'Wave A unexpectedly changes uv.lock' }
$status = @(git -C $liveRepo status --porcelain=v1 --untracked-files=all)
$dirty = @($status | ForEach-Object {
    $candidate = $_.Substring(3)
    if ($candidate.Contains(' -> ')) { $candidate = $candidate.Split(' -> ')[-1] }
    $candidate.Replace('\','/')
})
$overlap = @($incoming | Where-Object { $dirty -contains $_ })
if ($overlap.Count -ne 0) { throw "incoming/WIP overlap: $($overlap -join ', ')" }
$wipPaths = @($dirty + 'uv.lock' | Sort-Object -Unique)
$before = @($wipPaths | ForEach-Object {
    $absolute = Join-Path $liveRepo $_
    if (Test-Path -LiteralPath $absolute -PathType Leaf) {
        [ordered]@{path=$_;size_bytes=(Get-Item -LiteralPath $absolute).Length;sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $absolute).Hash.ToLowerInvariant()}
    } else { [ordered]@{path=$_;size_bytes=$null;sha256=$null} }
}) | ConvertTo-Json -Depth 4 -Compress
git -C $liveRepo merge --ff-only origin/main
if ((git -C $liveRepo rev-parse HEAD).Trim() -ne $evidenceSha) { throw 'live main did not reach E' }
$after = @($wipPaths | ForEach-Object {
    $absolute = Join-Path $liveRepo $_
    if (Test-Path -LiteralPath $absolute -PathType Leaf) {
        [ordered]@{path=$_;size_bytes=(Get-Item -LiteralPath $absolute).Length;sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $absolute).Hash.ToLowerInvariant()}
    } else { [ordered]@{path=$_;size_bytes=$null;sha256=$null} }
}) | ConvertTo-Json -Depth 4 -Compress
if ($after -cne $before) { throw 'live WIP bytes changed during fast-forward' }
& 'C:\Python314\python.exe' -B tools\remediation_evidence.py run-verification-gate --snapshot $snapshot --root $verificationRoot -- validate --cwd . $ledgerPath
if ($LASTEXITCODE -ne 0) { throw 'post-publication gate validation failed' }
```

Closure is falsified by a changed source/config/Theory/dependency or closure byte,
a different `P`/`E`, a non-direct evidence child, an unallowlisted skip, nonzero
JUnit failure/error, a mathematics claim without current derivation/formal-proof
evidence, unresolved review disagreement, missing skeptic/adjudicator linkage, or
a gate revision mismatch. Preserve failed records as history and use
`INCONCLUSIVE`; do not publish them as closure.
