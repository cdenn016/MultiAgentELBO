# Scientific Integrity Remediation Wave D Implementation Plan

> **Binding 2026-08-13 gate-execution supersession.** Any older path-return
> resolver command preserved below records the historical review context only and
> is not executable guidance. Current gate actions must validate the snapshot and
> explicit `.codex` root and execute retained bytes in one safe invocation:
> `C:\Python314\python.exe -B tools\remediation_evidence.py run-verification-gate --snapshot SNAPSHOT --root ROOT -- start ARGS` or
> `C:\Python314\python.exe -B tools\remediation_evidence.py run-verification-gate --snapshot SNAPSHOT --root ROOT -- validate ARGS`.
> Never assign or execute a resolved `$gate` path. Historical JUnit and evidence
> records remain revision-bound history and are not rewritten by this correction.
> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Attribute the counterexample-suite and fixed-ray CUDA costs with revision-bound component timings, then apply only the optimizations whose preregistered trigger fires without changing scientific outputs or execution guarantees.

**Architecture:** D0 adds one immutable timing schema and observation seams around existing pure phases; it freezes budgets and decision rules before collecting measurements. D0 closes measurement and exact threshold propositions only. D1 is conditional and split by subsystem: an immutable exact-catalog cache may address repeated CPU enumeration, while paired-job CUDA batching is preferred over a persistent worker and is implemented only if bounded authorized GPU measurements attribute material cost to repeated process/hash initialization. Every performance comparison is a same-session interleaved AB/BA experiment with raw repetitions, dispersion, load/thermal metadata, and exact scientific-output identity.

**Tech Stack:** Python 3.14, `time.perf_counter_ns`, dataclasses, JSON, NumPy, pytest/JUnit, Wave C's read-only worker protocol v3, separate timing sidecars, revision-bound evidence indexes, optional CUDA Python `C:\anaconda\python.exe` only after explicit operator authorization.

## Global Constraints

- Start only after Waves 0, A, B, and C are merged and exact-final ledgers validate.
- Preserve all live WIP and work in a fresh isolated `codex/` worktree from fetched `origin/main`.
- Use American English throughout.
- D0 records measurement; it does not claim an optimization or performance SLA.
- Freeze thresholds and sample counts before observing new timing data.
- CPU tests use `C:\Python314\python.exe`, cache-disabled pytest, and worktree-local basetemps.
- Do not use the GPU until the user explicitly confirms availability for the exact D0 revision and accepts the fresh gate record. Operator acceptance is authorization, not evidence of execution.
- CUDA evidence is stale after any instrumentation or execution-path change. D1 requires a fresh exact-revision sentinel only if a current sentinel operational claim is sought.
- Preserve gate expiry, identity digests, device/determinism/TF32 enforcement, immutable request/response records, one outer-job retry, crash-resume, and H holdout boundaries.
- Scientific outputs must be byte-semantically identical under canonical JSON/per-array hashing; performance changes never promote attraction, equivalence, or universality claims.
- Persisted producer verification states remain exactly `CANDIDATE`.
- Execute the installed gate only through `tools/remediation_evidence.py run-verification-gate --snapshot docs/verification/remediation/verification-contract-v1.json --root 'C:\Users\chris and christine\.codex\skills\verification' -- <start|validate> ARGS`. The explicit canonical `.codex` root is mandatory; there is no `.claude`, PATH, home, registry, copied-script, path-return command, or environment fallback.
- Treat the reviewed Wave 0, A, B, C, and D plans, their last-touch commits, the Wave 0 verification snapshot, and the complete terminal Wave 0/A/B/C ledger/index/closure exports as exact inputs. Wave E's reviewed plan is a verifier-pattern reference only: its Research revision is not a MultiAgentELBO upstream dependency or aggregate-ledger member.
- The three CUDA scopes are independent and nontransitive: exact-E0 D0 attribution, exact-E1 D1 v3/v4 comparison, and the optional exact-E1 five-job v4 operational sentinel. Each needs its own fresh idle gate, process record, displayed digest, and explicit user acceptance. Acceptance of one scope never authorizes either other scope.
- No 40-job confirmatory sweep is part of Wave D. No command, projection, authorization, sentinel, or comparator in this plan may be interpreted as permission to start it.
- Before the first test, create the ignored `.verification/` directory. Every
  RED and GREEN command below writes a fresh JUnit XML there; parse counts from
  XML and never use a console progress line as closure evidence.

---

## File Responsibility Map

- Create `src/multiagent_elbo/performance.py`: immutable timing spans, clocks, aggregation, decision rules, and canonical timing records.
- Modify `src/multiagent_elbo/finite/counterexample_experiment.py`: observe catalog enumeration, minimization, serialization, fixture construction, and assertion/publication preparation as separate phases.
- Modify `src/multiagent_elbo/cuda_backend.py`: observe controller validation, preflight/worker process walls, request serialization, response read/parse, output validation, and observer delivery without changing Wave C protocol v3.
- Modify `tools/cuda_worker.py`: emit a separate timing sidecar for module/Torch import, library hashing, CUDA initialization, input loading, kernel/synchronization, response serialization, and response writing; do not add fields to protocol v3.
- Modify `src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py`: aggregate per-exchange timings without changing job/retry/resume semantics.
- Create `tools/run_remediation_performance_profile.py`: click-to-run D0 measurement launcher with editable dictionaries and no CLI requirement for normal use.
- Create `tools/run_wave_d_d0_cuda_attribution.py`: fixed exact-E0 ten-pair attribution launcher.
- Create `tools/run_wave_d_d1_cpu_comparator.py`: exact-E0/exact-E1 paired AB/BA CPU comparator with separate raw, load/thermal, and semantic-hash records.
- Create `tools/run_wave_d_d1_cuda_comparator.py`: fixed exact-E1 ten-outer-pair v3/v4 comparator launcher.
- Create `tools/run_wave_d_d1_cuda_sentinel.py`: fixed exact-E1 five-job v4 operational sentinel launcher.
- Create `tools/build_wave_d_evidence.py`: checked-in Wave-D wrapper around the
  exact Wave 0 evidence-index API for D0 and conditional D1.
- Modify `tests/test_counterexample_experiment.py`, `tests/test_cuda_backend.py`, `tests/test_gaussian_fixed_ray_experiment.py`, and `tests/test_gaussian_confirmatory_experiment.py`.
- Create `tests/test_performance.py` and `tests/test_performance_launcher.py`.
- Create `docs/verification/remediation/performance-budget-v1.json`: preregistered thresholds and decision rules.
- Create D0/D1 evidence under their exact revision-derived evidence directories.

### Task 0: Prove the serial handoff, isolate Wave D, and fingerprint live WIP

**Files:**
- Read only: `C:\Users\chris and christine\Desktop\MultiAgentELBO`.
- Require preserved exact-terminal worktrees: `C:\tmp\MultiAgentELBO-remediation-wave-{0,a,b,c}-terminal`.
- Create worktree: `C:\tmp\MultiAgentELBO-remediation-wave-d-20260811`.
- Create branch: `codex/scientific-integrity-remediation-wave-d-20260811`.
- Create ignored dependency copies under `.verification/dependencies/wave-{0,a,b,c}/` only after every source worktree validates.

**Interfaces:**
- Each preserved upstream root is at its exact terminal SHA and contains `final-ledger.json`, `closure/index.json`, every file named by the generic and domain indexes, and `terminal.json`. `terminal.json` has exactly `schema_version`, `wave`, `tested_git_head`, `implementation_parent_git_head`, `reviewed_plan`, `ledger`, `generic_index`, `domain_indexes`, `closure_inventory`, `closure_inventory_sha256`, and `verification_snapshot_sha256`. `closure_inventory` is the ASCII-path-sorted complete recursive tuple of closed `{path,size_bytes,sha256}` records, including every index and review/adjudicator byte but excluding `terminal.json` and the ignored ledger.
- `Get-WipFingerprint` binds every path reported by Git plus `uv.lock` by repository-relative path, kind, byte size, and SHA-256 without writing to the live checkout.
- Upstream validation is read-only and complete. It resolves the pinned installed gate in each exact-terminal worktree; validates that wave's ledger at its own head; validates the generic index and every wave-specific domain index; recomputes every closure file size/hash and the exact no-extra path set; requires `E^=P` and an evidence-only `P..E`; binds the full 40-hex terminal SHA; and validates the same nine-file Wave 0 snapshot. A ledger file alone is never a handoff.
- Wave D starts only from freshly fetched `origin/main` after proving the exact Wave 0/A/B/C terminal SHAs are ancestors in serial order and that `origin/main` equals the Wave C terminal SHA. A merge commit, missing terminal export, stale plan/snapshot, invalid ledger, closure drift, or live-WIP drift blocks Task 1.

- [ ] **Step 1: Capture the live checkout before fetching**

At execution time, read the complete `superpowers:using-git-worktrees` skill. Then run:

```powershell
$ErrorActionPreference = 'Stop'
$liveRepo = 'C:\Users\chris and christine\Desktop\MultiAgentELBO'
$worktree = 'C:\tmp\MultiAgentELBO-remediation-wave-d-20260811'
$branch = 'codex/scientific-integrity-remediation-wave-d-20260811'
$wipBefore = 'C:\tmp\multiagentelbo-wave-d-live-wip-before.json'
$wipAfter = 'C:\tmp\multiagentelbo-wave-d-live-wip-after.json'
$upstreamRoots = [ordered]@{
  'wave-0' = 'C:\tmp\MultiAgentELBO-remediation-wave-0-terminal'
  'wave-a' = 'C:\tmp\MultiAgentELBO-remediation-wave-a-terminal'
  'wave-b' = 'C:\tmp\MultiAgentELBO-remediation-wave-b-terminal'
  'wave-c' = 'C:\tmp\MultiAgentELBO-remediation-wave-c-terminal'
}

function Get-WipFingerprint([string]$Repo) {
    $raw = (& git -C $Repo status --porcelain=v1 -z --untracked-files=all) -join "`n"
    if ($LASTEXITCODE -ne 0) { throw 'live worktree status failed' }
    $paths = [System.Collections.Generic.HashSet[string]]::new(
        [System.StringComparer]::Ordinal
    )
    foreach ($entry in ($raw -split "`0")) {
        if ([string]::IsNullOrEmpty($entry) -or $entry.Length -lt 4) { continue }
        $candidate = $entry.Substring(3)
        if ($candidate.Contains(' -> ')) {
            $candidate = $candidate.Split(' -> ')[-1]
        }
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
            [ordered]@{
                path=$relative.Replace('\', '/'); kind='directory'
                size_bytes=$null; sha256=$null
            }
        } else {
            [ordered]@{
                path=$relative.Replace('\', '/'); kind='absent'
                size_bytes=$null; sha256=$null
            }
        }
    }
    return @($records)
}

Get-WipFingerprint $liveRepo |
  ConvertTo-Json -Depth 8 |
  Set-Content -LiteralPath $wipBefore -Encoding utf8NoBOM
if (-not (Test-Path -LiteralPath $wipBefore -PathType Leaf)) {
  throw 'live WIP fingerprint was not captured'
}
git -C $liveRepo status --short
if ($LASTEXITCODE -ne 0) { throw 'live checkout status failed' }
```

- [ ] **Step 2: Validate every exact-terminal upstream in its own worktree**

The coordinator creates each fixed terminal export immediately after that wave's gate validates and before its worktree is released. Export creation is a read-only inventory operation; it never edits the terminal commit, closure, or ledger. Run:

```powershell
$verificationRoot = 'C:\Users\chris and christine\.codex\skills\verification'
$expectedPlanSha256 = [ordered]@{
  'wave-0' = 'dbe2263a3b0fe1e9f5db4ff1fca9a19f819cfd32ef38da71d6e5cb5485723ac2'
  'wave-a' = 'e13201bc18bf7045318fb8f641be1b9a1ef937c9c6882f91cfe1412bfc83433b'
  'wave-b' = '1544737bd5be505431c027475e2e839b8dfe771cec2b6ca65e87563e3386691f'
  'wave-c' = 'bebd4e2e04e29c9b07eb4d10211debeb9f47adf79117a793936eefaa4a9af289'
}
$terminalShas = [ordered]@{}

function Get-ClosureInventory([string]$Root, [string]$ClosureRelative) {
    $closure = Join-Path $Root $ClosureRelative
    if (-not (Test-Path -LiteralPath $closure -PathType Container)) {
        throw "closure root missing: $closure"
    }
    return @(
        Get-ChildItem -LiteralPath $closure -Recurse -File |
        ForEach-Object {
            $relative = [IO.Path]::GetRelativePath($closure, $_.FullName)
            [ordered]@{
                path = $relative.Replace('\', '/')
                size_bytes = $_.Length
                sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()
            }
        } |
        Sort-Object { $_.path }
    )
}

foreach ($wave in $upstreamRoots.Keys) {
  $root = $upstreamRoots[$wave]
  if (-not (Test-Path -LiteralPath $root -PathType Container)) {
    throw "missing exact-terminal upstream worktree: $wave"
  }
  $terminalPath = Join-Path $root 'terminal.json'
  $terminal = Get-Content -Raw -LiteralPath $terminalPath | ConvertFrom-Json
  $terminalKeys = @(
    'schema_version','wave','tested_git_head',
    'implementation_parent_git_head','reviewed_plan','ledger','generic_index',
    'domain_indexes','closure_inventory','closure_inventory_sha256',
    'verification_snapshot_sha256'
  )
  if (@($terminal.PSObject.Properties.Name | Sort-Object) -join "`0" -ne
      @($terminalKeys | Sort-Object) -join "`0") {
    throw "closed terminal schema mismatch: $wave"
  }
  $head = (& git -C $root rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0 -or $head -notmatch '^[0-9a-f]{40}$' -or
      $terminal.schema_version -ne 'wave-d-upstream-terminal-v1' -or
      $terminal.wave -ne $wave -or $terminal.tested_git_head -ne $head) {
    throw "terminal record/head mismatch: $wave"
  }
  $parent = (& git -C $root rev-parse HEAD^).Trim()
  if ($LASTEXITCODE -ne 0 -or
      $terminal.implementation_parent_git_head -ne $parent) {
    throw "terminal E/P mismatch: $wave"
  }
  $nonEvidence = @(& git -C $root diff --name-only $parent..$head) |
    Where-Object { $_ -notlike 'docs/verification/evidence/*' }
  if ($LASTEXITCODE -ne 0 -or $nonEvidence) {
    throw "terminal child is not evidence-only: $wave $nonEvidence"
  }
  $planPath = Join-Path $root ([string]$terminal.reviewed_plan.path)
  $planHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $planPath).Hash.ToLowerInvariant()
  if ($planHash -ne [string]$terminal.reviewed_plan.sha256) {
    throw "reviewed plan hash mismatch: $wave"
  }
  if ($expectedPlanSha256.Contains($wave) -and
      $planHash -ne $expectedPlanSha256[$wave]) {
    throw "binding PASS plan hash mismatch: $wave"
  }
  $snapshot = Join-Path $root 'docs\verification\remediation\verification-contract-v1.json'
  $snapshotHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $snapshot).Hash.ToLowerInvariant()
  if ($snapshotHash -ne [string]$terminal.verification_snapshot_sha256) {
    throw "repository verification snapshot drift: $wave"
  }
  $ledger = Join-Path $root ([string]$terminal.ledger)
  & 'C:\Python314\python.exe' -B (Join-Path $root 'tools\remediation_evidence.py') run-verification-gate --snapshot $snapshot --root $verificationRoot -- validate --cwd $root $ledger
  if ($LASTEXITCODE -ne 0) { throw "terminal ledger invalid: $wave" }
  $genericIndex = Join-Path $root ([string]$terminal.generic_index)
  & 'C:\Python314\python.exe' -B (Join-Path $root 'tools\remediation_evidence.py') validate $genericIndex --cwd $root
  if ($LASTEXITCODE -ne 0) { throw "generic closure index invalid: $wave" }

  $closureRelative = Split-Path -Parent ([string]$terminal.generic_index)
  if ($wave -eq 'wave-a') {
    & 'C:\Python314\python.exe' -B (Join-Path $root 'tools\wave_a_evidence.py') validate-domain --bundle-dir (Join-Path $root $closureRelative)
    if ($LASTEXITCODE -ne 0) { throw 'Wave A domain closure invalid' }
  } elseif ($wave -eq 'wave-c') {
    & 'C:\Python314\python.exe' -B (Join-Path $root 'tools\build_wave_c_evidence.py') validate-domain --bundle-dir (Join-Path $root $closureRelative)
    if ($LASTEXITCODE -ne 0) { throw 'Wave C domain closure invalid' }
  }
  foreach ($domainIndexRelative in @($terminal.domain_indexes)) {
    $domainIndexPath = Join-Path $root ([string]$domainIndexRelative)
    if (-not (Test-Path -LiteralPath $domainIndexPath -PathType Leaf)) {
      throw "domain index missing: $wave $domainIndexRelative"
    }
  }

  $observedInventory = @(Get-ClosureInventory $root $closureRelative)
  $recordedInventory = @($terminal.closure_inventory)
  if (($observedInventory | ConvertTo-Json -Depth 8 -Compress) -cne
      ($recordedInventory | ConvertTo-Json -Depth 8 -Compress)) {
    throw "complete closure inventory mismatch: $wave"
  }
  $inventoryBytes = [Text.Encoding]::UTF8.GetBytes(
    ($recordedInventory | ConvertTo-Json -Depth 8 -Compress) + "`n"
  )
  $sha256 = [Security.Cryptography.SHA256]::Create()
  try {
    $inventorySha = [BitConverter]::ToString(
      $sha256.ComputeHash($inventoryBytes)
    ).Replace('-', '').ToLowerInvariant()
  } finally {
    $sha256.Dispose()
  }
  if ($inventorySha -ne [string]$terminal.closure_inventory_sha256) {
    throw "closure inventory digest mismatch: $wave"
  }
  $terminalShas[$wave] = $head
}
```

The Wave B terminal export is additionally required to contain its exact 29-file branch and `wave-b-domain-index.json`; the recursive terminal inventory plus its already validated exact-head ledger makes omission, addition, or byte drift fatal. The Wave 0 export has no domain index. Wave A and C must pass their checked-in domain validators as shown. No current Wave D wrapper is used to manufacture or bless an upstream record.

For Wave B, existence checking is insufficient: before accepting its terminal,
run the exact checked-in Wave-B projection validator (or its same-revision
mechanical equivalent) against the closure/domain index and final ledger. It must
verify the closed `wave-b-domain-evidence-v1` schema, exact 29-file branch,
one-way root/domain bindings, all 15 projected claims, two independently
calibrated views per claim, AB/BA order and both nested matches, all closed
comparison fields, six criterion scores per view, and every unrounded top-level
criterion arithmetic mean. Add a mutation test for each nested comparison,
match, calibration, score, and domain-index member; any mutation must reject
before Task 1. Wave A and Wave C validators remain required unchanged.

- [ ] **Step 3: Fetch, prove serial ancestry, and create the isolated worktree**

```powershell
git -C $liveRepo fetch origin
if ($LASTEXITCODE -ne 0) { throw 'origin fetch failed' }
git -C $liveRepo log -1 --oneline origin/main
if ($LASTEXITCODE -ne 0) { throw 'cannot show authoritative origin/main' }
$parent = (& git -C $liveRepo rev-parse origin/main).Trim()
if ($parent -ne $terminalShas['wave-c']) {
  throw 'origin/main is not the exact validated Wave C terminal SHA'
}
$ordered = @('wave-0','wave-a','wave-b','wave-c')
for ($i = 0; $i -lt $ordered.Count - 1; $i++) {
  git -C $liveRepo merge-base --is-ancestor $terminalShas[$ordered[$i]] $terminalShas[$ordered[$i + 1]]
  if ($LASTEXITCODE -ne 0) {
    throw "nonserial upstream ancestry: $($ordered[$i])"
  }
}
if (Test-Path -LiteralPath $worktree) {
  throw 'Wave D worktree already exists'
}
git -C $liveRepo show-ref --verify --quiet "refs/heads/$branch"
if ($LASTEXITCODE -eq 0) { throw 'Wave D branch already exists' }
git -C $liveRepo worktree add -b $branch $worktree $parent
if ($LASTEXITCODE -ne 0) { throw 'Wave D worktree creation failed' }
if ((& git -C $worktree rev-parse HEAD).Trim() -ne $parent -or
    (& git -C $worktree status --porcelain=v1)) {
  throw 'fresh Wave D worktree is not clean at the validated parent'
}
```

- [ ] **Step 4: Copy and revalidate every dependency, then prove live WIP unchanged**

```powershell
foreach ($wave in $upstreamRoots.Keys) {
  $source = $upstreamRoots[$wave]
  $destination = Join-Path $worktree ".verification\dependencies\$wave"
  if (Test-Path -LiteralPath $destination) {
    throw "upstream copy destination exists: $wave"
  }
  New-Item -ItemType Directory -Path $destination | Out-Null
  Copy-Item -LiteralPath (Join-Path $source 'terminal.json') -Destination $destination
  Copy-Item -LiteralPath (Join-Path $source 'final-ledger.json') -Destination $destination
  Copy-Item -LiteralPath (Join-Path $source 'closure') -Destination $destination -Recurse
  $sourceInventory = @(
    Get-ChildItem -LiteralPath $source -Recurse -File |
    Where-Object {
      $_.FullName -eq (Join-Path $source 'terminal.json') -or
      $_.FullName -eq (Join-Path $source 'final-ledger.json') -or
      $_.FullName.StartsWith((Join-Path $source 'closure') + '\')
    } |
    ForEach-Object {
      [ordered]@{
        path = [IO.Path]::GetRelativePath($source, $_.FullName).Replace('\','/')
        size_bytes = $_.Length
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()
      }
    } | Sort-Object { $_.path }
  )
  $copiedInventory = @(
    Get-ChildItem -LiteralPath $destination -Recurse -File |
    ForEach-Object {
      [ordered]@{
        path = [IO.Path]::GetRelativePath($destination, $_.FullName).Replace('\','/')
        size_bytes = $_.Length
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()
      }
    } | Sort-Object { $_.path }
  )
  if (($sourceInventory | ConvertTo-Json -Depth 8 -Compress) -cne
      ($copiedInventory | ConvertTo-Json -Depth 8 -Compress)) {
    throw "upstream copy drift: $wave"
  }
}

Get-WipFingerprint $liveRepo |
  ConvertTo-Json -Depth 8 |
  Set-Content -LiteralPath $wipAfter -Encoding utf8NoBOM
$beforeSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $wipBefore).Hash
$afterSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $wipAfter).Hash
if ($beforeSha -ne $afterSha) {
  throw 'live WIP changed during Wave D isolation'
}
```

After entering `$worktree`, rerun the installed snapshot resolver there and revalidate the four copied terminal records, ledgers, generic/domain indexes, complete closure inventories, reviewed-plan bindings, and terminal SHAs before Task 1. Save the copied terminal/inventory hashes in ignored `.verification/wave-d-entry.json`; candidate and closure review contexts bind its public privacy-transformed form. The copies remain read-only for all D0/D1 work.

---

### Task 1: Freeze immutable timing records and decision rules

**Files:**
- Create: `src/multiagent_elbo/performance.py`
- Create: `tests/test_performance.py`
- Create: `docs/verification/remediation/performance-budget-v1.json`

**Interfaces:**
- Produces `Clock` protocol with `now_ns() -> int` and production `PerfCounterClock`.
- Produces `TimingSpan(component: str, started_ns: int, ended_ns: int, unit_id: str)` with derived nonnegative `duration_ns`.
- Produces `TimingObservation(schema_version, source_revision, config_digest,
  environment_digest, machine_digest, sample_phase, trial_index,
  component_spans, wall_duration_ns, verification_state="CANDIDATE")`, where
  `sample_phase` is exactly `cold`, `warmup`, or `measured` and `trial_index` is a
  nonnegative non-boolean integer.
- Produces summaries with the accepted raw observation IDs, exact-rational median
  and median absolute deviation (numerator/denominator integer pairs), and
  exact-rational component shares. Decision rules consume only `measured`
  observations; `cold`/`warmup` remain descriptive.
- Produces `evaluate_cpu_catalog_trigger(summary) -> Literal["optimize", "retain", "inconclusive"]`.
- Produces `evaluate_cuda_exchange_trigger(summary) -> Literal["optimize", "retain", "inconclusive"]`.
- Produces `evaluate_cpu_improvement(comparison)` and
  `evaluate_cuda_improvement(comparison)`, each returning
  `Literal["verified", "not_verified", "inconclusive"]` from the frozen
  before/after rules without emitting a verification-ledger state.

- [ ] **Step 1: Write fake-clock and invalid-span RED tests**

```python
class FakeClock:
    def __init__(self, values):
        self._values = iter(values)
    def now_ns(self):
        return next(self._values)


def test_timing_span_uses_injected_monotonic_clock():
    with observe_timing("catalog.enumeration", "trial-001", FakeClock([10, 35])) as result:
        pass
    assert result.span.duration_ns == 25


def test_timing_span_rejects_negative_or_boolean_times():
    with pytest.raises(ValueError, match="monotonic"):
        TimingSpan("x", 20, 19, "u")
    with pytest.raises(TypeError, match="integer"):
        TimingSpan("x", True, 19, "u")
```

- [ ] **Step 2: Write exact budget RED tests**

Freeze these rules in JSON before measurements:

```text
CPU trigger: at least 15 measured trials after 5 warmups; optimize only when
median(catalog_enumeration_ns) >= 1_000_000_000 and its median share of total
catalog pipeline wall time is >= 0.40.

CUDA trigger: at least 10 accepted exchange observations from the exact same
source/config/environment/device; optimize only when the median sum of process
startup, Torch/CUDA initialization, and CUDA-library hashing is >= 0.50 of
exchange wall time and the 640-exchange projection is >= 600 seconds.

CPU D1 success: the same 5 warmups and 15 measured catalog-pipeline trials at the
same machine/config/environment; canonical scientific outputs identical; median
total wall time improves by >= 25% and >= 250,000,000 ns. Both boundaries are
inclusive.

CUDA D1 success: after separate authorization, 2 warmups and 10 matched outer-job
trials. Each before trial runs the same exact 2-scheme x 8-step input through 16
serial protocol-v3 exchanges; each after trial runs it through one protocol-v4
paired job. Canonical subrecord outputs must be identical. Median outer-job wall
time must improve by >= 30% and the 40-job projected saving must be >= 600
seconds. Both boundaries are inclusive.

Boundary equality triggers optimization. Missing authorization, mixed identities,
retries, rejected samples, fewer samples, or instrumentation overhead greater
than 1% of measured wall time or 5,000,000 ns per observation yields
inconclusive.

The overhead condition is a separate paired qualification, not a no-op clock,
calibration, or estimated subtraction. Before a CPU measurement can be accepted,
run exactly 15 same-input paired observations; before a separately authorized
D0 CUDA exchange can be accepted, run exactly 10. Draw and record one unbiased
initial order before the first pair and alternate `AB`, `BA` thereafter. `A` is
the fully untimed production path and `B` is the complete timed path. Record
every raw duration, order, start/end load and thermal sample, binding digest,
semantic hash, and rejected-pair reason. Set conservative observer cost to
`max(0, median(B.wall_duration_ns) - median(A.wall_duration_ns))`, without
rounding, and require it to be at most both `5_000_000 ns` and one percent of
the timed median wall. Strict excess, a retry, unequal semantic hash, mixed
identity, missing load/thermal evidence, nonalternating order, or a deficient
pair count makes the affected decision `inconclusive`; it is never repaired by
subtracting an estimated cost.

CPU `B` includes every clock read, `TimingSpan` construction, completed-span
observer callback, and profile recording. CUDA `B` includes every controller
callback; canonical sidecar JSON serialization; base64 encoding; stderr write,
read, prefix handling, and parse; response/sidecar hash verification; controller
read/parse; and every CUDA synchronization required to observe a duration. CUDA
`A` performs the identical scientific v3 preflight and response validation but
emits none of those timing side effects. The matched overhead record is an
eligibility guard only, never a timing correction or scientific output.
```

```python
def test_cpu_trigger_is_frozen_at_both_boundaries():
    summary = cpu_summary(trials=15, median_enumeration_ns=1_000_000_000, median_share=0.40)
    assert evaluate_cpu_catalog_trigger(summary) == "optimize"


def test_cuda_trigger_rejects_mixed_identity_and_insufficient_samples():
    assert evaluate_cuda_exchange_trigger(cuda_summary(samples=9)) == "inconclusive"
    assert evaluate_cuda_exchange_trigger(cuda_summary(samples=10, mixed_identity=True)) == "inconclusive"


def test_trigger_is_inconclusive_when_instrumentation_overhead_is_material():
    assert evaluate_cpu_catalog_trigger(
        cpu_summary(trials=15, instrumentation_overhead_share=Decimal("0.0101"))
    ) == "inconclusive"


def test_cpu_trigger_is_inconclusive_with_too_few_trials():
    assert evaluate_cpu_catalog_trigger(cpu_summary(trials=14)) == "inconclusive"


def test_d1_success_rules_are_inclusive_and_require_identical_outputs():
    assert evaluate_cpu_improvement(cpu_comparison(relative=0.25, saved_ns=250_000_000)) == "verified"
    assert evaluate_cuda_improvement(cuda_comparison(relative=0.30, projected_saved_s=600)) == "verified"
    assert evaluate_cpu_improvement(cpu_comparison(relative=0.25, saved_ns=250_000_000, outputs_equal=False)) == "inconclusive"


def test_timing_observation_has_candidate_verification_state_only(valid_observation):
    assert valid_observation.verification_state == "CANDIDATE"
    with pytest.raises(ValueError, match="verification_state"):
        dataclasses.replace(valid_observation, verification_state="INCONCLUSIVE")


def test_summary_keeps_raw_ids_and_frozen_dispersion(measured_observations):
    summary = summarize_timing(measured_observations)
    assert summary.accepted_observation_ids == tuple(
        observation.observation_id for observation in measured_observations
    )
    assert summary.median_ns == Fraction(30)
    assert summary.median_absolute_deviation_ns == Fraction(10)
```

- [ ] **Step 3: Run RED**

```powershell
New-Item -ItemType Directory -Path .verification -Force | Out-Null
C:\Python314\python.exe -B -m pytest tests\test_performance.py -q -p no:cacheprovider --basetemp=.pytest-wave-d-task1-red --junitxml=.verification\wave-d-task1-red.xml
```

Expected: FAIL because `multiagent_elbo.performance` and the budget record do not exist.

- [ ] **Step 4: Implement the immutable schema and canonical evaluators**

Reject unknown component names, duplicate `(unit_id, component)` pairs, negative durations, inconsistent wall totals, nonfinite derived ratios, mixed bindings, and any producer state other than `CANDIDATE`. Use integer nanoseconds in raw records; convert to decimal seconds only in derived summaries.

`machine_digest` is the SHA-256 of canonical JSON containing OS/version/
architecture, CPU model and logical count, total physical memory, Python
executable hash, and—only for CUDA records—GPU UUID/name/compute capability,
driver, CUDA runtime, and relevant cuBLAS library hashes. Missing fields make a
comparison `inconclusive`; they are never silently omitted from the preimage.

```python
@dataclass(frozen=True)
class TimingSpan:
    component: str
    started_ns: int
    ended_ns: int
    unit_id: str

    def __post_init__(self) -> None:
        for name, value in (("started_ns", self.started_ns), ("ended_ns", self.ended_ns)):
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{name} must be an integer")
        if self.ended_ns < self.started_ns:
            raise ValueError("timing span must be monotonic")
        if self.component not in ALLOWED_TIMING_COMPONENTS:
            raise ValueError("unknown timing component")

    @property
    def duration_ns(self) -> int:
        return self.ended_ns - self.started_ns


def evaluate_cpu_catalog_trigger(summary: CpuCatalogSummary) -> TriggerDecision:
    if summary.mixed_bindings or summary.accepted_trials < 15:
        return "inconclusive"
    return (
        "optimize"
        if summary.median_enumeration_ns >= 1_000_000_000
        and summary.median_enumeration_share >= Decimal("0.40")
        else "retain"
    )
```

Implement the CUDA evaluator from the equally literal rules above. Both consume
validated summaries and return no evidence/verification state.

- [ ] **Step 5: Run GREEN, Ruff, and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_performance.py -q -p no:cacheprovider --basetemp=.pytest-wave-d-task1-green --junitxml=.verification\wave-d-task1-green.xml
C:\Python314\python.exe -m ruff check --no-cache src/multiagent_elbo/performance.py tests/test_performance.py
C:\Python314\python.exe -m ruff format --check --no-cache src/multiagent_elbo/performance.py tests/test_performance.py
git add -- src/multiagent_elbo/performance.py tests/test_performance.py docs/verification/remediation/performance-budget-v1.json
git commit -m "feat: freeze remediation performance measurements"
```

### Task 2: Partition the CPU exact-catalog pipeline

**Files:**
- Modify: `src/multiagent_elbo/finite/counterexample_experiment.py`
- Modify: `tests/test_counterexample_experiment.py`
- Modify: `tests/test_performance.py`

**Interfaces:**
- Changes `_catalog(config, *, timing_observer=None)` only by adding a keyword-only observation seam.
- Emits exactly `catalog.fixture`, `catalog.enumeration`, `catalog.minimization`, `catalog.serialization`, and `catalog.assertion` spans.
- The observer cannot return or modify scientific values; it receives completed immutable `TimingSpan` objects after each phase.

- [ ] **Step 1: Write phase inventory and observer-isolation RED tests**

```python
def test_catalog_emits_exact_phase_inventory_without_changing_result(config):
    spans = []
    observed = _catalog(config, timing_observer=spans.append)
    baseline = _catalog(config)
    assert catalog_semantic_sha256(observed) == catalog_semantic_sha256(baseline)
    assert [span.component for span in spans] == [
        "catalog.fixture", "catalog.enumeration", "catalog.minimization",
        "catalog.serialization", "catalog.assertion",
    ]


def test_catalog_observer_return_value_cannot_replace_scientific_data(config):
    result = _catalog(config, timing_observer=lambda span: {"replacement": True})
    assert catalog_semantic_sha256(result) == catalog_semantic_sha256(_catalog(config))
```

- [ ] **Step 2: Run RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_counterexample_experiment.py -k timing -q -p no:cacheprovider --basetemp=.pytest-wave-d-task2-red --junitxml=.verification\wave-d-task2-red.xml
```

Expected: FAIL because `_catalog` has no timing observer or phase inventory.

- [ ] **Step 3: Add observation-only boundaries**

Capture each phase's result into a local before notifying the observer. Never call the observer while mutable module state or an authoritative iterator can be replaced. Preserve one production enumeration per producer run.

```python
def _notify_timing(observer: Callable[[TimingSpan], object] | None, span: TimingSpan) -> None:
    if observer is not None:
        observer(span)  # return value is deliberately ignored


with timed_span("catalog.enumeration", unit_id, clock) as completed:
    candidates = tuple(_enumerate_candidates(laws, channels))
_notify_timing(timing_observer, completed.span)
```

Apply the same completed-local pattern to every named phase. Notify only after
the authoritative phase output is detached/frozen.

- [ ] **Step 4: Prove exact output identity and run the affected suite**

Compare canonical candidate JSON, all result dataclasses, every arrays key/dtype/shape/value, and final experiment artifact semantics with and without observation. Then run:

```powershell
C:\Python314\python.exe -B -m pytest tests\test_counterexamples.py tests\test_counterexample_experiment.py tests\test_performance.py -q -p no:cacheprovider --basetemp=.pytest-wave-d-task2-green --junitxml=.verification\wave-d-task2-green.xml
```

- [ ] **Step 5: Commit CPU instrumentation**

```powershell
git add -- src/multiagent_elbo/finite/counterexample_experiment.py tests/test_counterexample_experiment.py tests/test_performance.py
git commit -m "perf: partition exact catalog timing"
```

### Task 3: Partition CUDA controller and worker timing without changing identity

**Files:**
- Modify: `src/multiagent_elbo/cuda_backend.py`
- Modify: `tools/cuda_worker.py`
- Modify: `src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py`
- Modify: `tests/test_cuda_backend.py`
- Modify: `tests/test_gaussian_fixed_ray_experiment.py`
- Modify: `tests/test_gaussian_confirmatory_experiment.py`

**Interfaces:**
- Leaves Wave C request/response protocol v3 byte-for-byte read-only.
- Produces sidecar schema `cuda-worker-timing-v1` with exact fields
  `{schema_version, process_kind, job_id, request_sha256, bound_output_sha256,
  scientific_system_digest, execution_binding_digest,
  process_wall_ns, spans, verification_state}`.
- Produces controller schema `cuda-controller-timing-v1` with exact fields
  `{schema_version, job_id, request_sha256, response_sha256,
  scientific_system_digest, execution_binding_digest, process_wall_ns, spans,
  worker_sidecar_sha256, verification_state}`.
- Controller leaf components are `controller.validation`,
  `controller.request_serialization`, `controller.preflight_process_wall`,
  `controller.worker_process_wall`, `controller.response_read_parse`,
  `controller.output_validation`, and `controller.observer_delivery`.
- Worker leaf components are `worker.module_torch_import`,
  `worker.cuda_library_hash`, `worker.cuda_initialization`,
  `worker.input_load_validation`, `worker.kernel_and_sync`,
  `worker.response_serialization`, and `worker.response_write`.
- Fixed-ray profiling adds `experiment.exchange_record_publication` after the
  accepted result is durably staged. Scientific resume/job records do not gain a
  timing field; the performance profile owns timing observations separately.
- Parent process spans may contain child spans. Aggregation records
  `exclusive_process_overhead_ns = process_wall_ns - sum(nonoverlapping_child_ns)`
  and rejects negative/overlapping child accounting. Trigger ratios use exclusive
  overhead plus leaf import/hash/init spans exactly once.
- Timing is opt-in through the controller-set child environment value
  `MULTIAGENTELBO_WORKER_TIMING_V1=1`. On a successful timed process, the worker
  writes exactly one stderr line
  the prefix `MULTIAGENTELBO_TIMING_V1:` followed by base64 canonical JSON. It never adds fields to
  request/response/preflight/provenance JSON and never creates a timing file.
  `bound_output_sha256` binds the exact preflight stdout bytes for a preflight
  process and the exact response JSON bytes for a compute process. Untimed
  production behavior emits no timing line.

- [ ] **Step 1: Write CPU fault-injection RED tests with a fake clock**

```python
def test_worker_timing_sidecar_binds_unchanged_v3_response(fake_v3_exchange):
    response_bytes, sidecar = fake_v3_exchange
    assert sidecar.schema_version == "cuda-worker-timing-v1"
    assert sidecar.bound_output_sha256 == hashlib.sha256(response_bytes).hexdigest()
    assert sidecar.verification_state == "CANDIDATE"
    assert {span.component for span in sidecar.spans} == EXPECTED_WORKER_COMPONENTS


def test_timing_observer_cannot_change_worker_result(valid_request, fake_runner):
    baseline = run_worker_job(valid_request, process_runner=fake_runner)
    seen = []
    observed = run_worker_job(
        valid_request,
        process_runner=fake_runner,
        timing_observer=lambda record: seen.append(record) or {"replace": True},
    )
    assert worker_result_semantic_sha256(observed) == worker_result_semantic_sha256(baseline)
    assert len(seen) == 1


def test_nested_process_accounting_does_not_double_count():
    summary = aggregate_cuda_timing(
        process_wall_ns=100,
        child_spans=(span("worker.module_torch_import", 10, 30),
                     span("worker.cuda_library_hash", 30, 50)),
    )
    assert summary.exclusive_process_overhead_ns == 60
    assert summary.accounted_total_ns == 100


def test_sidecar_mutation_cannot_make_a_v3_result_eligible(fake_v3_exchange):
    response_bytes, sidecar = fake_v3_exchange
    tampered = dataclasses.replace(sidecar, bound_output_sha256="0" * 64)
    with pytest.raises(WorkerBackendError, match="bound_output_sha256"):
        validate_worker_timing(tampered, response_bytes=response_bytes)


def test_untimed_worker_preserves_stdout_stderr_and_protocol(fake_runner, valid_request):
    result = run_worker_job(valid_request, process_runner=fake_runner, timing_observer=None)
    assert result.response_manifest["schema_version"] == WAVE_C_PROTOCOL_V3
    assert fake_runner.compute_stderr == ""
    assert "timing" not in result.response_manifest
```

- [ ] **Step 2: Write gate/expiry/retry invariance RED tests**

Add literal tests that patch the timing observer to raise before and after v3
response validation. Before validation, the exchange fails under the existing
outer retry rule; after a validated scientific result, observer failure marks the
profile sample rejected but cannot change the scientific result or consume a
second retry. Reuse the existing gate-expiry and C-before-H fixtures and assert
their record hashes are identical with `timing_observer=None` and a collecting
observer.

- [ ] **Step 3: Run RED on CPU only**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_cuda_backend.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py -k timing -q -p no:cacheprovider --basetemp=.pytest-wave-d-task3-red --junitxml=.verification\wave-d-task3-red.xml
```

Expected: FAIL because timing sidecars/observers and exclusive aggregation do not
exist; no CUDA subprocess is started.

- [ ] **Step 4: Implement timing envelopes around existing phases**

Set a stdlib-only process-start timestamp before NumPy/Torch imports, then time the
existing import/hash/init/load/compute/serialize/write calls; never repeat one for
measurement. Serialize protocol-v3 response bytes first, compute their SHA-256,
then serialize the detached timing sidecar to the prefixed stderr line only when
the controller opted in. `run_worker_job` validates v3 response
bytes first, validates the sidecar against those same bytes, constructs the normal
`WorkerJobResult`, and only then calls an observation-only callback. The
controller measures each named phase with the injected clock. Do not combine
preflight and compute processes in D0. Preserve request/response scientific fields
and Wave-C identity digests exactly.

- [ ] **Step 5: Run CPU GREEN and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_cuda_backend.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py tests\test_performance.py -q -p no:cacheprovider --basetemp=.pytest-wave-d-task3-green --junitxml=.verification\wave-d-task3-green.xml
C:\Python314\python.exe -m ruff check --no-cache src/multiagent_elbo/performance.py src/multiagent_elbo/cuda_backend.py src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py tools/cuda_worker.py
git add -- src/multiagent_elbo/cuda_backend.py tools/cuda_worker.py src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py tests/test_cuda_backend.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py tests/test_performance.py
git commit -m "perf: partition fixed-ray worker timing"
```

### Task 4: Publish the D0 CPU profile and bounded optional CUDA profile

**Files:**
- Create: `tools/run_remediation_performance_profile.py`
- Create: `tools/build_wave_d_evidence.py`
- Create: `tests/test_performance_launcher.py`
- Create at runtime: revision-derived D0 timing artifacts.

**Interfaces:**
- Editable dictionaries: `RUN`, `CPU_PROFILE`, `CUDA_PROFILE`, `OUTPUT`, `COMPUTE`.
- Defaults: CPU profile enabled with 1 cold observation, 5 warmups, and 15
  measured trials; CUDA profile disabled with 1 cold, 2 warmup, and 10 measured
  exchanges available only after an accepted gate.
- Produces raw spans, derived summaries, decision records, environment/source/config bindings, and `verification_state=CANDIDATE`.
- `MULTIAGENTELBO_PROFILE_OUTPUT`, when present and nonempty, is the sole
  operational evidence-harness override for `OUTPUT["root"]`; it is normalized
  through Wave B before config hashing or effects and is recorded verbatim plus
  resolved form. Normal click-to-run use edits `OUTPUT` and needs no CLI.
- Before measured trials, calibrates 1,000 no-op timing spans and 1,000 canonical
  sidecar encodings on the same clock/process. It records all calibration raw
  durations and their median; it never subtracts them from phase timings. The
  frozen trigger rule above rejects materially instrumented observations.

#### Normative Wave D evidence and verifier contract

This subsection overrides any older Task 4, 5, or 8 evidence prose that conflicts
with it. It consumes Wave 0's generic builder, total privacy transform, immutable
`PreparedEvidenceBundle`, snapshot resolver, plan binding, review tiers, and
gate template without signature drift. Wave D adds a one-way domain index; it
does not add a twelfth generic base file or implement a second gate resolver.

**Binding closure-lifecycle correction.** For both D0 and conditional D1, the
only admissible lifecycle is the Wave-0 lifecycle: at clean implementation head
`P`, create and validate the exact `P/P` candidate bundle and commit only its
SHA-named tracked child `E`; at clean exact `E` with direct parent `P`, rerun the
three suites and the eligible profile/comparator into ignored raw staging,
compute a detached canonical review-context digest, obtain raw reviews and one
raw adjudicator for every literal claim, validate those raw bytes, privacy
transform the complete selected public set in memory, and publish the absent
closure directory exactly once. No closure index, ledger claim, public review,
adjudicator, or closure directory may exist before `validate-reviews` succeeds.
The wrapper cannot synthesize a review, view score, AB/BA match, escalation,
aggregate, adjudication, verdict, result location, evidence ID, or obligation.

`review-context-sha` and `validate-reviews` are required closed wrapper commands
for both programs, in addition to the listed build/populate/export/validation
commands. The closed Wave-D context has exactly
`{schema_version,tested_git_head,implementation_parent_git_head,evidence_diff_inventory,candidate_evidence_inventory,raw_command_inventory,raw_junit_inventory,raw_profile_inventory,raw_comparison_inventory,tested_input_inventory,source_config_inventory,dependency_inventory,environment_inventory,reviewed_plan_bytes,verification_snapshot_bytes,upstream_terminal_bytes,claim_specs,public_path_contracts,branch_selection}`.
Its schema version is respectively `wave-d0-review-context-v1` or
`wave-d1-review-context-v1`; every inventory is ASCII-path sorted closed
`{path,size_bytes,sha256}`; `E^=P` is independently proved; and `branch_selection`
is derived solely from raw decision/authorization/outcome bytes. D0's
`upstream_terminal_bytes` binds complete revalidated Wave 0/A/B/C exports; D1's
binds the complete revalidated D0 export, including ledger, index, every indexed
closure byte, and export inventory. Its candidate inventory includes `index.json`.
The context is written only to ignored raw staging and has no final public path.
Every leaf mutation changes its digest or makes validation fail.

Raw reviews use the Wave-0 closed review schema and must bind this exact context
digest, E/P heads, literal claim/domain/severity/evidence IDs, the full installed
domain criterion map, selected candidate statement and explicit negation, and
the actual ordered AB and BA matches. The normal tier is exactly two independent
views and target 2; any recorded `small_margin`, `high_dispersion`, or
`criterion_disagreement` requires all target-4 paths, and unresolved criterion
disagreement at four requires every target-8 path. Each claim receives one raw
`verifier-adjudicator` record with the Wave-0 closed fields, exact target view
IDs, literal eligible evidence IDs, result location, falsification condition,
and nonempty obligation when abstaining. A missing or contradictory observation
forces `INCONCLUSIVE`, never a vote. No index, domain index, privacy map,
authorization-only record, or review-context digest is claim evidence.

The privacy transform is total, idempotent, and semantic over every base/domain
JSON or XML byte, raw command, JUnit, profile, comparator, review, adjudicator,
and result field. Its closed mapping records each raw/public relative path and
SHA-256 without retaining absolute paths, hostnames, PIDs, resident-process rows,
gate telemetry, absolute argv/environment components, or raw private token. It
must preserve numerical spans, order, scientific semantic hashes, binding digests,
criteria, trigger decisions, and public result locations. The public directory
must contain exactly the branch/tier inventory below; candidate rejects all
review/adjudicator bytes, closure rejects any raw extra or absent selected byte,
and both validators reject a private token or a case alias before publication.

**CUDA authorization correction.** Wave D has exactly three independent,
nontransitive operator scopes: exact-E0 D0 attribution with ten exchanges,
exact-E1 D1 v3/v4 comparison with ten outer pairs, and optional exact-E1 v4
sentinel with five jobs. A scope starts with a gate-only invocation that writes
one ignored raw gate/process record; it must be displayed to the operator and
its SHA-256 explicitly accepted before the corresponding run invocation. Each
run independently requires the exact scope name, tested head, accepted raw-gate
SHA-256, recheck record, clean head/status, exact identity, five idle samples,
resident-process record, and unexpired gate. A prior scope never authorizes a
later scope. The harness exposes no 40-job option and never launches one.

```powershell
# D0-ATTRIBUTION at exact E0. STOP after printing the digest for acceptance.
$d0Gate = $closureRaw\cuda\d0-attribution-gate.raw.json
Remove-Item Env:CUDA_VISIBLE_DEVICES -ErrorAction Stop
try {
  & 'C:\anaconda\python.exe' -B tools\run_wave_d_d0_cuda_attribution.py --stage gate --scope d0-attribution --tested-head $e0 --raw-gate $d0Gate
  if ($LASTEXITCODE -ne 0) { throw 'D0 attribution gate capture failed' }
} finally { $env:CUDA_VISIBLE_DEVICES = '-1' }
$d0GateSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $d0Gate).Hash.ToLowerInvariant()
Write-Output $d0GateSha
# Obtain explicit user acceptance of this displayed D0-ATTRIBUTION digest only.
Remove-Item Env:CUDA_VISIBLE_DEVICES -ErrorAction Stop
try {
  & 'C:\anaconda\python.exe' -B tools\run_wave_d_d0_cuda_attribution.py --stage run --scope d0-attribution --tested-head $e0 --raw-gate $d0Gate --accepted-gate-sha256 $d0GateSha --exchanges 10
  if ($LASTEXITCODE -ne 0) { throw 'D0 ten-exchange attribution failed' }
} finally { $env:CUDA_VISIBLE_DEVICES = '-1' }
```

```powershell
# D1-COMPARATOR at exact E1. STOP after printing the digest for acceptance.
$d1ComparatorGate = $closureRaw\cuda\d1-comparator-gate.raw.json
Remove-Item Env:CUDA_VISIBLE_DEVICES -ErrorAction Stop
try {
  & 'C:\anaconda\python.exe' -B tools\run_wave_d_d1_cuda_comparator.py --stage gate --scope d1-comparator --tested-head $e1 --raw-gate $d1ComparatorGate
  if ($LASTEXITCODE -ne 0) { throw 'D1 comparator gate capture failed' }
} finally { $env:CUDA_VISIBLE_DEVICES = '-1' }
$d1ComparatorGateSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $d1ComparatorGate).Hash.ToLowerInvariant()
Write-Output $d1ComparatorGateSha
# Obtain explicit user acceptance of this displayed D1-COMPARATOR digest only.
Remove-Item Env:CUDA_VISIBLE_DEVICES -ErrorAction Stop
try {
  & 'C:\anaconda\python.exe' -B tools\run_wave_d_d1_cuda_comparator.py --stage run --scope d1-comparator --tested-head $e1 --raw-gate $d1ComparatorGate --accepted-gate-sha256 $d1ComparatorGateSha --outer-pairs 10
  if ($LASTEXITCODE -ne 0) { throw 'D1 ten-outer-pair comparator failed' }
} finally { $env:CUDA_VISIBLE_DEVICES = '-1' }
```

```powershell
# D1-SENTINEL at exact E1. This optional scope is independent of D1-COMPARATOR.
$d1SentinelGate = $closureRaw\cuda\d1-sentinel-gate.raw.json
Remove-Item Env:CUDA_VISIBLE_DEVICES -ErrorAction Stop
try {
  & 'C:\anaconda\python.exe' -B tools\run_wave_d_d1_cuda_sentinel.py --stage gate --scope d1-sentinel --tested-head $e1 --raw-gate $d1SentinelGate
  if ($LASTEXITCODE -ne 0) { throw 'D1 sentinel gate capture failed' }
} finally { $env:CUDA_VISIBLE_DEVICES = '-1' }
$d1SentinelGateSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $d1SentinelGate).Hash.ToLowerInvariant()
Write-Output $d1SentinelGateSha
# Obtain explicit user acceptance of this displayed D1-SENTINEL digest only.
Remove-Item Env:CUDA_VISIBLE_DEVICES -ErrorAction Stop
try {
  & 'C:\anaconda\python.exe' -B tools\run_wave_d_d1_cuda_sentinel.py --stage run --scope d1-sentinel --tested-head $e1 --raw-gate $d1SentinelGate --accepted-gate-sha256 $d1SentinelGateSha --jobs 5
  if ($LASTEXITCODE -ne 0) { throw 'D1 five-job v4 sentinel failed' }
} finally { $env:CUDA_VISIBLE_DEVICES = '-1' }
```

```python
CLAIM_CRITERIA_BY_DOMAIN = {
    "code": (
        ("execution", "execution"),
        ("input_output_behavior", "input/output behavior"),
        ("boundary_failure_behavior", "boundary/failure behavior"),
        ("regression_coverage", "regression coverage"),
        ("configuration_reachability", "configuration reachability"),
        ("reproducibility", "reproducibility"),
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
    "experiment": (
        (
            "hypothesis_endpoint_definition",
            "hypothesis/endpoint definition",
        ),
        ("protocol_fidelity", "protocol fidelity"),
        ("data_provenance", "data provenance"),
        ("configuration_identity", "configuration identity"),
        ("seed_split_control", "seed/split control"),
        ("statistical_treatment", "statistical treatment"),
        (
            "reproduced_output_agreement",
            "reproduced-output agreement",
        ),
        ("robustness", "robustness"),
        ("alternative_explanations", "alternative explanations"),
    ),
}

D0_CLAIM_SPECS = (
    {
        "id": "WAVE-D0-UPSTREAM-INSTRUMENTATION-CONTRACT",
        "domain": "code",
        "severity": "medium",
        "kind": "mechanical",
        "statement": (
            "At exact E0, Wave D0 consumes the complete validated serial "
            "Wave 0/A/B/C handoff and its timing observers preserve the "
            "declared execution, failure, retry, and publication contracts."
        ),
        "explicit_negation": (
            "At exact E0, at least one serial-handoff or timing-observer "
            "execution contract is absent, stale, or behavior-changing."
        ),
        "evidence_ids": (
            "d0-upstream-terminal-bindings",
            "d0-targeted-junit",
            "d0-subsystem-junit",
            "d0-full-junit",
        ),
    },
    {
        "id": "WAVE-D0-CPU-SCIENTIFIC-IDENTITY",
        "domain": "code",
        "severity": "medium",
        "kind": "mechanical",
        "statement": (
            "At exact E0, timed and untimed CPU catalog executions have "
            "identical canonical scientific outputs for every accepted pair."
        ),
        "explicit_negation": (
            "At exact E0, at least one accepted timed/untimed CPU pair changes "
            "a canonical scientific output."
        ),
        "evidence_ids": (
            "d0-cpu-semantic-hashes",
            "d0-targeted-junit",
        ),
    },
    {
        "id": "WAVE-D0-CPU-ATTRIBUTION-MEASUREMENT",
        "domain": "experiment",
        "severity": "low",
        "kind": "reproduced_output",
        "statement": (
            "The exact-E0 CPU profile is an eligible repeated causal "
            "attribution measurement under the frozen protocol."
        ),
        "explicit_negation": (
            "The exact-E0 CPU profile violates at least one frozen eligibility "
            "condition and is not an eligible causal attribution measurement."
        ),
        "evidence_ids": (
            "d0-cpu-raw-observations",
            "d0-cpu-observer-overhead-pairs",
            "d0-cpu-load-thermal-metadata",
            "d0-cpu-summary",
        ),
    },
    {
        "id": "AUD-22-D0-THRESHOLD-PROPOSITION",
        "domain": "experiment",
        "severity": "low",
        "kind": "reproduced_output",
        "statement": (
            "At exact E0 under the frozen D0 protocol, median exact-catalog "
            "enumeration is at least 1000000000 ns and its median pipeline "
            "share is at least 0.40."
        ),
        "explicit_negation": (
            "At exact E0 under the frozen D0 protocol, at least one of the two "
            "AUD-22 optimization thresholds is not met."
        ),
        "evidence_ids": ("d0-performance-budget", "d0-cpu-decision"),
    },
    {
        "id": "WAVE-D0-CUDA-ATTRIBUTION-MEASUREMENT",
        "domain": "experiment",
        "severity": "medium",
        "kind": "reproduced_output",
        "statement": (
            "The separately authorized exact-E0 ten-pair CUDA profile is an "
            "eligible repeated causal attribution measurement."
        ),
        "explicit_negation": (
            "The exact-E0 CUDA profile violates at least one frozen eligibility "
            "condition and is not an eligible causal attribution measurement."
        ),
        "evidence_ids": (
            "d0-cuda-authorization-binding",
            "d0-cuda-raw-observations",
            "d0-cuda-observer-overhead-pairs",
            "d0-cuda-load-thermal-metadata",
            "d0-cuda-summary",
        ),
    },
    {
        "id": "AUD-21-D0-THRESHOLD-PROPOSITION",
        "domain": "experiment",
        "severity": "medium",
        "kind": "reproduced_output",
        "statement": (
            "At exact E0 under the separately authorized frozen D0 protocol, "
            "median repeated process/import/hash/init overhead is at least "
            "0.50 of exchange wall time and the 640-exchange projection is "
            "at least 600 seconds."
        ),
        "explicit_negation": (
            "At exact E0 under the frozen D0 protocol, at least one of the two "
            "AUD-21 optimization thresholds is not met."
        ),
        "evidence_ids": ("d0-performance-budget", "d0-cuda-decision"),
    },
    {
        "id": "WAVE-D0-EVIDENCE-PROVENANCE",
        "domain": "evidence",
        "severity": "medium",
        "kind": "reproduced_source",
        "statement": (
            "Every exact-E0 profile, decision, JUnit, plan, snapshot, "
            "environment, machine, and upstream byte has current complete "
            "revision-bound provenance."
        ),
        "explicit_negation": (
            "At least one exact-E0 load-bearing evidence byte lacks current "
            "complete revision-bound provenance."
        ),
        "evidence_ids": (
            "d0-upstream-terminal-bindings",
            "d0-profile-provenance",
            "d0-privacy-transform",
        ),
    },
)
```

The two D0 threshold statements are the only optimization-trigger propositions.
They are not restatements of the historical AUD findings. On eligible exact-E0
data, `optimize` maps that literal threshold proposition to
`EVIDENCE_VERIFIED`, `retain` maps it to `REFUTED`, and
`inconclusive` maps it to `INCONCLUSIVE` with the exact failed eligibility
obligation. D0 never marks an AUD remediation claim complete.

```python
D1_CLAIM_SPECS = (
    {
        "id": "WAVE-D1-UPSTREAM-REGRESSION-CONTRACT",
        "domain": "code",
        "severity": "medium",
        "kind": "mechanical",
        "statement": (
            "At exact E1, only exact-E0-authorized D1 paths changed and all "
            "targeted, subsystem, and full CPU regression contracts pass."
        ),
        "explicit_negation": (
            "At exact E1, an unauthorized path changed or a required CPU "
            "regression contract fails."
        ),
        "evidence_ids": (
            "d1-d0-terminal-binding",
            "d1-targeted-junit",
            "d1-subsystem-junit",
            "d1-full-junit",
        ),
    },
    {
        "id": "WAVE-D1-CPU-SCIENTIFIC-IDENTITY",
        "domain": "code",
        "severity": "low",
        "kind": "mechanical",
        "statement": (
            "Every accepted interleaved exact-E0/exact-E1 CPU comparison pair "
            "has identical canonical scientific outputs."
        ),
        "explicit_negation": (
            "At least one accepted interleaved exact-E0/exact-E1 CPU pair "
            "changes a canonical scientific output."
        ),
        "evidence_ids": (
            "d1-cpu-semantic-hashes",
            "d1-cpu-raw-comparison",
        ),
    },
    {
        "id": "AUD-22-D1-PERFORMANCE-SUCCESS",
        "domain": "experiment",
        "severity": "low",
        "kind": "reproduced_output",
        "statement": (
            "Under eligible same-session AB/BA evidence with identical "
            "scientific outputs, exact E1 improves median CPU pipeline wall "
            "time by at least 25 percent and 250000000 ns versus exact E0."
        ),
        "explicit_negation": (
            "Under eligible same-session evidence, at least one AUD-22 D1 "
            "scientific-identity or performance-success conjunct is false."
        ),
        "evidence_ids": (
            "d1-performance-budget",
            "d1-cpu-raw-comparison",
            "d1-cpu-load-thermal-metadata",
            "d1-cpu-semantic-hashes",
            "d1-cpu-comparison-summary",
        ),
    },
    {
        "id": "AUD-22-D1-REMEDIATION",
        "domain": "code",
        "severity": "low",
        "kind": "mechanical",
        "statement": (
            "The exact-E0-authorized immutable catalog cache satisfies the "
            "AUD-22 D1 scientific-identity and preregistered performance "
            "acceptance contract at exact E1."
        ),
        "explicit_negation": (
            "The exact-E0-authorized immutable catalog cache fails at least "
            "one AUD-22 D1 scientific-identity or performance acceptance "
            "condition at exact E1."
        ),
        "evidence_ids": (
            "d1-cpu-semantic-hashes",
            "d1-cpu-comparison-summary",
            "d1-targeted-junit",
        ),
    },
    {
        "id": "WAVE-D1-CUDA-SCIENTIFIC-IDENTITY",
        "domain": "experiment",
        "severity": "medium",
        "kind": "reproduced_output",
        "statement": (
            "Every separately authorized accepted exact-E1 v3/v4 outer-job "
            "comparison pair has identical ordered scientific suboutputs."
        ),
        "explicit_negation": (
            "At least one separately authorized accepted exact-E1 v3/v4 "
            "outer-job pair changes an ordered scientific suboutput."
        ),
        "evidence_ids": (
            "d1-cuda-comparator-authorization-binding",
            "d1-cuda-semantic-hashes",
            "d1-cuda-raw-comparison",
        ),
    },
    {
        "id": "AUD-21-D1-PERFORMANCE-SUCCESS",
        "domain": "experiment",
        "severity": "medium",
        "kind": "reproduced_output",
        "statement": (
            "Under eligible separately authorized AB/BA evidence with "
            "identical scientific outputs, v4 improves median outer-job wall "
            "time by at least 30 percent and projects at least 600 seconds "
            "saved over 40 jobs versus v3."
        ),
        "explicit_negation": (
            "Under eligible separately authorized evidence, at least one "
            "AUD-21 D1 scientific-identity or performance-success conjunct "
            "is false."
        ),
        "evidence_ids": (
            "d1-performance-budget",
            "d1-cuda-comparator-authorization-binding",
            "d1-cuda-raw-comparison",
            "d1-cuda-load-thermal-metadata",
            "d1-cuda-semantic-hashes",
            "d1-cuda-comparison-summary",
        ),
    },
    {
        "id": "AUD-21-D1-REMEDIATION",
        "domain": "code",
        "severity": "medium",
        "kind": "mechanical",
        "statement": (
            "The exact-E0-authorized protocol-v4 paired-job path satisfies "
            "the AUD-21 D1 scientific-identity and preregistered performance "
            "acceptance contract at exact E1."
        ),
        "explicit_negation": (
            "The exact-E0-authorized protocol-v4 paired-job path fails at "
            "least one AUD-21 D1 scientific-identity or performance "
            "acceptance condition at exact E1."
        ),
        "evidence_ids": (
            "d1-cuda-semantic-hashes",
            "d1-cuda-comparison-summary",
            "d1-targeted-junit",
        ),
    },
    {
        "id": "WAVE-D1-CUDA-V4-FIVE-JOB-SENTINEL",
        "domain": "experiment",
        "severity": "medium",
        "kind": "reproduced_output",
        "statement": (
            "The separately authorized exact-E1 five-job sentinel executes "
            "the protocol-v4 paired path with current identity, parity, "
            "failure, and provenance checks."
        ),
        "explicit_negation": (
            "The exact-E1 five-job sentinel fails at least one protocol-v4 "
            "currentness, parity, failure, or provenance check."
        ),
        "evidence_ids": (
            "d1-cuda-sentinel-authorization-binding",
            "d1-cuda-sentinel-record",
        ),
    },
    {
        "id": "WAVE-D1-EVIDENCE-PROVENANCE",
        "domain": "evidence",
        "severity": "medium",
        "kind": "reproduced_source",
        "statement": (
            "Every exact-E1 comparison, outcome, JUnit, plan, snapshot, "
            "environment, machine, and exact-E0 authorization byte has "
            "current complete revision-bound provenance."
        ),
        "explicit_negation": (
            "At least one exact-E1 load-bearing evidence byte lacks current "
            "complete revision-bound provenance."
        ),
        "evidence_ids": (
            "d1-d0-terminal-binding",
            "d1-profile-provenance",
            "d1-privacy-transform",
        ),
    },
)
```

Every claim has a literal eligible evidence-ID tuple and one public result
location. `index.json`, the domain index, review context, privacy map, reviewer
agreement, and an authorization record by itself are structural prerequisites,
not substitutes for measurement or code evidence. The wrapper rejects an
unknown ID, polarity, domain, severity, criterion, or result path and never
synthesizes a claim, view, score, verdict, or adjudication.

**D0 polarity is measurement-only.** No D0 ledger row states or implies that an
historical AUD defect still occurs, is repaired, or is remediated. It projects
only the seven literal `D0_CLAIM_SPECS`: a complete supporting mechanical or
measurement record gives `EVIDENCE_VERIFIED`; a current eligible observed
explicit negation gives `REFUTED`; and an absent authorization, failed paired
qualification, mixed binding, missing eligible byte, or unresolved review
conflict gives `INCONCLUSIVE` with that precise obligation. In particular,
`AUD-22-D0-THRESHOLD-PROPOSITION` is `EVIDENCE_VERIFIED` only for decision
`optimize`, `REFUTED` only for decision `retain`, and `INCONCLUSIVE` only for
decision `inconclusive`. The same mapping applies to
`AUD-21-D0-THRESHOLD-PROPOSITION`, except a missing D0-ATTRIBUTION authorization
is necessarily `INCONCLUSIVE`. These states determine whether a D1 path may be
implemented; they are not a D1 success claim and never close an AUD remediation.

**Exact D1 frozen outcome table.** At exact E1, after all branch-authorized
closure measurements and before review-context construction, the wrapper creates
one immutable `outcomes/frozen-table.json` in raw staging with exactly
`{schema_version,program,d0_tested_git_head,d1_tested_git_head,cpu_branch,cuda_branch,rows}`
and schema version `wave-d1-frozen-outcomes-v1`. `rows` is ASCII-ID-sorted and
contains exactly the nine `D1_CLAIM_SPECS` IDs. Every row has exactly
`{claim_id,required_branch,eligible,observed_polarity,ledger_state,reason,open_obligations}`;
the wrapper derives every field from validated D0 decisions, candidate/closure
JUnits, paired raw comparisons, semantic hashes, authorization bindings, and
the selected review tier. Callers cannot supply a state.

| D1 row | `EVIDENCE_VERIFIED` | `REFUTED` | `INCONCLUSIVE` |
| --- | --- | --- | --- |
| `WAVE-D1-UPSTREAM-REGRESSION-CONTRACT` | only authorized paths changed and all required suites pass | an eligible unauthorized diff or required suite failure | required suite/evidence/review unavailable |
| `WAVE-D1-CPU-SCIENTIFIC-IDENTITY` | CPU branch is comparator and every accepted pair hash agrees | an eligible accepted pair hash disagrees | CPU branch not triggered or pair qualification fails |
| `AUD-22-D1-PERFORMANCE-SUCCESS` | CPU identity holds and both frozen improvement limits hold | an eligible comparison establishes the literal negation of either conjunct | no eligible CPU comparison |
| `AUD-22-D1-REMEDIATION` | the immediately preceding CPU identity and success rows both verify | either predecessor is refuted by eligible current evidence | either predecessor is inconclusive |
| `WAVE-D1-CUDA-SCIENTIFIC-IDENTITY` | CUDA branch includes comparator and every accepted outer pair agrees | an eligible accepted outer pair disagrees | no accepted D1-COMPARATOR scope |
| `AUD-21-D1-PERFORMANCE-SUCCESS` | CUDA identity holds and both frozen v3/v4 limits hold | an eligible comparison establishes the literal negation of either conjunct | no eligible CUDA comparator |
| `AUD-21-D1-REMEDIATION` | the immediately preceding CUDA identity and success rows both verify | either predecessor is refuted by eligible current evidence | either predecessor is inconclusive |
| `WAVE-D1-CUDA-V4-FIVE-JOB-SENTINEL` | exact D1-SENTINEL authorization and all five v4 jobs satisfy its listed checks | an eligible sentinel check fails | sentinel scope is absent, stale, or incomplete |
| `WAVE-D1-EVIDENCE-PROVENANCE` | all listed E1 and imported E0 bindings validate | a current eligible listed binding contradicts the statement | a required binding or review is absent |

This table overrides later prose that labels an untriggered or unmeasured D1
defect as refuted, or mechanically assumes all implemented D1 paths succeed.
No failure of a requested comparator begins a 40-job run; it is terminal for the
applicable Wave-D outcome row.

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
INITIAL_REVIEW_PATHS = (
    "reviews/code-contract-review.json",
    "reviews/performance-evidence-review.json",
)
TARGET4_ADDITIONAL_REVIEW_PATHS = (
    "reviews/escalation/boundary-failure-review.json",
    "reviews/escalation/provenance-counterevidence-review.json",
)
TARGET8_ADDITIONAL_REVIEW_PATHS = (
    "reviews/escalation/configuration-reachability-review.json",
    "reviews/escalation/protocol-adversary-review.json",
    "reviews/escalation/path-privacy-adversary.json",
    "reviews/escalation/reproducibility-review.json",
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
    "small_margin",
)
D0_ADJUDICATOR_PATHS = tuple(
    sorted(
        (
            f"reviews/adjudicators/{spec['id']}.json"
            for spec in D0_CLAIM_SPECS
        ),
        key=lambda value: value.encode("ascii"),
    )
)
D1_ADJUDICATOR_PATHS = tuple(
    sorted(
        (
            f"reviews/adjudicators/{spec['id']}.json"
            for spec in D1_CLAIM_SPECS
        ),
        key=lambda value: value.encode("ascii"),
    )
)

D0_CORE_DOMAIN_PATHS = (
    "claim-contracts.json",
    "domain-evidence.json",
    "domain-privacy-transform.json",
    "performance-budget.json",
    "profile/cpu/decision.json",
    "profile/cpu/load-thermal-metadata.json",
    "profile/cpu/observer-overhead-pairs.json",
    "profile/cpu/raw-observations.json",
    "profile/cpu/semantic-hashes.json",
    "profile/cpu/summary.json",
    "profile/provenance.json",
    "upstream-terminal-bindings.json",
)
D0_CUDA_BRANCH_PATHS = {
    "no-cuda": ("profile/cuda/open-obligation.json",),
    "d0-attribution": (
        "profile/cuda/authorization-binding.json",
        "profile/cuda/decision.json",
        "profile/cuda/load-thermal-metadata.json",
        "profile/cuda/observer-overhead-pairs.json",
        "profile/cuda/raw-observations.json",
        "profile/cuda/semantic-hashes.json",
        "profile/cuda/summary.json",
    ),
}
D1_CORE_DOMAIN_PATHS = (
    "claim-contracts.json",
    "d0-terminal-binding.json",
    "domain-evidence.json",
    "domain-privacy-transform.json",
    "outcomes/frozen-table.json",
    "performance-budget.json",
    "profile/provenance.json",
)
D1_CPU_BRANCH_PATHS = {
    "not-implemented": ("outcomes/cpu.json",),
    "comparator": (
        "outcomes/cpu.json",
        "profile/cpu/comparison-summary.json",
        "profile/cpu/load-thermal-metadata.json",
        "profile/cpu/raw-comparison.json",
        "profile/cpu/semantic-hashes.json",
    ),
}
D1_CUDA_BRANCH_PATHS = {
    "no-cuda": (
        "outcomes/cuda.json",
        "profile/cuda/open-obligation.json",
    ),
    "comparator": (
        "outcomes/cuda.json",
        "profile/cuda/comparator-authorization-binding.json",
        "profile/cuda/comparison-summary.json",
        "profile/cuda/load-thermal-metadata.json",
        "profile/cuda/raw-comparison.json",
        "profile/cuda/semantic-hashes.json",
    ),
    "sentinel": (
        "outcomes/cuda.json",
        "profile/cuda/sentinel-authorization-binding.json",
        "profile/cuda/sentinel-record.json",
    ),
    "comparator-and-sentinel": (
        "outcomes/cuda.json",
        "profile/cuda/comparator-authorization-binding.json",
        "profile/cuda/comparison-summary.json",
        "profile/cuda/load-thermal-metadata.json",
        "profile/cuda/raw-comparison.json",
        "profile/cuda/semantic-hashes.json",
        "profile/cuda/sentinel-authorization-binding.json",
        "profile/cuda/sentinel-record.json",
    ),
}

D0_CANDIDATE_PUBLIC_PATHS = tuple(
    sorted(
        GENERIC_PUBLIC_PATHS
        + D0_CORE_DOMAIN_PATHS
        + D0_CUDA_BRANCH_PATHS["no-cuda"],
        key=lambda value: value.encode("ascii"),
    )
)
D0_CLOSURE_PUBLIC_PATHS_BY_BRANCH_AND_TARGET = {
    (branch, target): tuple(
        sorted(
            GENERIC_PUBLIC_PATHS
            + D0_CORE_DOMAIN_PATHS
            + branch_paths
            + REVIEW_PATHS_BY_TARGET[target]
            + D0_ADJUDICATOR_PATHS,
            key=lambda value: value.encode("ascii"),
        )
    )
    for branch, branch_paths in D0_CUDA_BRANCH_PATHS.items()
    for target in (2, 4, 8)
}
D1_CANDIDATE_PUBLIC_PATHS_BY_BRANCH = {
    (cpu_branch, cuda_branch): tuple(
        sorted(
            GENERIC_PUBLIC_PATHS
            + D1_CORE_DOMAIN_PATHS
            + cpu_paths
            + cuda_paths,
            key=lambda value: value.encode("ascii"),
        )
    )
    for cpu_branch, cpu_paths in D1_CPU_BRANCH_PATHS.items()
    for cuda_branch, cuda_paths in D1_CUDA_BRANCH_PATHS.items()
}
D1_CLOSURE_PUBLIC_PATHS_BY_BRANCH_AND_TARGET = {
    (cpu_branch, cuda_branch, target): tuple(
        sorted(
            D1_CANDIDATE_PUBLIC_PATHS_BY_BRANCH[
                (cpu_branch, cuda_branch)
            ]
            + REVIEW_PATHS_BY_TARGET[target]
            + D1_ADJUDICATOR_PATHS,
            key=lambda value: value.encode("ascii"),
        )
    )
    for cpu_branch in D1_CPU_BRANCH_PATHS
    for cuda_branch in D1_CUDA_BRANCH_PATHS
    for target in (2, 4, 8)
}
```

The domain index is `domain-evidence.json` and one-way binds the already
prepared generic `index.json`. Candidate and closure constructors require
exact set equality with the applicable tuple above, exact cardinality,
case-sensitive uniqueness, ASCII sort order, and no extra recursive file. A
branch name is derived from validated raw authorization/outcome bytes; callers
cannot select one. Candidate construction rejects all review/adjudicator bytes.
Closure construction requires the selected complete 2/4/8 review tier and every
claim-specific adjudicator before preparing either index.

- [ ] **Step 1: Write launcher RED tests**

```python
def test_performance_launcher_defaults_to_cpu_measurement_only():
    module = load_launcher("run_remediation_performance_profile.py")
    assert module.CPU_PROFILE == {
        "enabled": True, "cold_trials": 1, "warmups": 5, "trials": 15,
    }
    assert module.CUDA_PROFILE == {
        "enabled": False,
        "cold_exchanges": 1,
        "warmup_exchanges": 2,
        "measured_exchanges": 10,
    }
    assert module.COMPUTE["heavy_sweep_enabled"] is False
    assert not hasattr(module, "build_parser")


def test_cuda_profile_without_accepted_gate_fails_before_output(tmp_path, monkeypatch):
    module = load_launcher("run_remediation_performance_profile.py")
    module.CUDA_PROFILE = {**module.CUDA_PROFILE, "enabled": True}
    module.OUTPUT = {**module.OUTPUT, "root": str(tmp_path / "out")}
    monkeypatch.setattr(module, "capture_idle_gpu_gate", forbidden("GPU query"))
    with pytest.raises(ValueError, match="accepted exact-revision gate"):
        module.main()
    assert not (tmp_path / "out").exists()
```

Add a foreign-CWD test with an absolute output override. In the same test module,
define `write_valid_wave_d_raw(tmp_path, *, program, stage) -> Path` by invoking
the frozen Wave-0 test record/fixture builders; it writes only a complete ignored
raw fixture and returns its path. Then add these exact wrapper controls:

```python
@pytest.mark.parametrize(
    "missing",
    ("budget", "source", "config", "environment", "decision"),
)
def test_wave_d_prepare_rejects_a_missing_binding_before_parent_exists(
    tmp_path, missing
):
    raw = write_valid_wave_d_raw(tmp_path, program="d0", stage="candidate")
    remove_named_raw_binding(raw, missing)
    destination = tmp_path / "absent" / "bundle"
    with pytest.raises(ValueError, match="binding"):
        prepare_wave_d_bundle(raw_dir=raw, output_dir=destination, **head_args("d0"))
    assert not destination.parent.exists()


def test_prepared_wave_d_bundle_owns_detached_bytes(tmp_path):
    raw = write_valid_wave_d_raw(tmp_path, program="d0", stage="candidate")
    original = raw.joinpath("profile/decision.json")
    prepared = prepare_wave_d_bundle(
        raw_dir=raw, output_dir=tmp_path / "published", **head_args("d0")
    )
    original.write_bytes(b'{"mutated":true}')
    publish_wave_d_bundle(prepared)
    validate_wave_d_bundle(tmp_path / "published")
    assert b"mutated" not in (tmp_path / "published/profile/decision.json").read_bytes()


def test_d1_prepare_revalidates_every_upstream_export_byte(tmp_path):
    upstream = write_valid_d0_export(tmp_path)
    raw = write_valid_wave_d_raw(tmp_path, program="d1", stage="candidate")
    upstream.joinpath("closure/profile/decision.json").write_bytes(b"{}")
    destination = tmp_path / "absent" / "d1"
    with pytest.raises(ValueError, match="upstream"):
        prepare_wave_d_bundle(
            raw_dir=raw,
            output_dir=destination,
            d0_bundle_dir=upstream,
            **head_args("d1"),
        )
    assert not destination.parent.exists()


@pytest.mark.parametrize("boundary", ALL_WAVE_D_WRITE_AND_RENAME_BOUNDARIES)
def test_wave_d_publication_failure_leaves_no_output(tmp_path, boundary, monkeypatch):
    raw = write_valid_wave_d_raw(tmp_path, program="d0", stage="candidate")
    destination = tmp_path / "absent" / "bundle"
    prepared = prepare_wave_d_bundle(
        raw_dir=raw, output_dir=destination, **head_args("d0")
    )
    inject_publication_failure(monkeypatch, boundary)
    with pytest.raises(OSError):
        publish_wave_d_bundle(prepared)
    assert not destination.parent.exists()
```

The helper functions named above are local test helpers implemented in the same
commit; `ALL_WAVE_D_WRITE_AND_RENAME_BOUNDARIES` is imported from the publisher so
the parametrization cannot silently omit a boundary.

- [ ] **Step 2: Run the launcher RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_performance_launcher.py -q -p no:cacheprovider --basetemp=.pytest-wave-d-task4-red --junitxml=.verification\wave-d-task4-red.xml
```

Expected: FAIL because the launcher and Wave-D evidence wrapper do not exist.

- [ ] **Step 3: Implement the click-to-run launcher and evidence wrapper**

```python
def main() -> PerformanceProfileResult:
    config = PerformanceProfileConfig.from_dicts(
        RUN, CPU_PROFILE, CUDA_PROFILE, OUTPUT, COMPUTE
    )
    resolved = with_resolved_output_root(
        config,
        anchor=ROOT,
        repo_root=ROOT,
        theory_root=ROOT / "Theory",
    )
    validated = validate_profile_config_before_effects(resolved, repo_root=ROOT)
    cpu = run_cpu_profile(validated)
    cuda = (
        run_bounded_cuda_profile(validated)
        if validated.cuda_authorized
        else inconclusive_cuda_profile(validated)
    )
    return publish_performance_profile(validated, cpu=cpu, cuda=cuda)
```

The wrapper imports `build_evidence_index`, `validate_evidence_index`,
`prepare_evidence_bundle`, `publish_evidence_bundle`, and
`PreparedEvidenceBundle` from `tools/remediation_evidence.py`. Its CLI is closed:

```text
build --program {d0,d1} --stage {candidate,closure} --tested-head SHA
      --implementation-parent SHA --raw-dir PATH --output-dir PATH
      [--d0-tested-head SHA --d0-bundle-dir PATH]
populate-ledger --program {d0,d1} --ledger PATH --closure-index PATH
export-upstream --ledger PATH --closure-dir PATH --output-dir PATH
validate-upstream --bundle-dir PATH
validate-domain --bundle-dir PATH
```

It adds the performance budget/decision/profile bindings and then calls the Wave
0 validator; its domain inventory supplements rather than replaces the generic
evidence schema. All exact-suite runs
use the generic `tools/remediation_evidence.py run-junit` CLI, while the generic
`validate` CLI validates the resulting index.

Because `remediation-evidence-v1` inventories commands, environment, dependencies,
and tested source/config inputs but has no domain-output field, the wrapper prepares
`performance-evidence-inventory.json` in memory. That closed
`wave-d-performance-evidence-v1` record has exactly `{schema_version, program,
evidence_stage, tested_git_head, implementation_parent_git_head, base_index,
artifacts}`; `base_index` is exactly `{name="index.json", size_bytes, sha256}` and
creates the one-way binding from domain evidence to the already prepared generic
index;
`artifacts` is a sorted list of safe bundle-relative
`{name, kind, size_bytes, sha256}` records for every profile, decision,
calibration, semantic-output comparison, D0 upstream copy, and review file. It
excludes itself and `index.json` to avoid recursion. `validate-domain` rejects an
unknown/missing/extra/case-aliased/hash-drifted domain byte or base-index drift.
The external ledger
references both indexes and the gate artifact digest binds all nonignored closure
bytes.

`prepare_wave_d_bundle(...) -> PreparedEvidenceBundle` is the only construction
path. It first calls generic `prepare_evidence_bundle` without publishing; reads
every performance profile, decision, calibration, semantic comparison, upstream
dependency, and review byte exactly once; applies the deterministic privacy
transform; validates each closed domain schema; builds the domain inventory from
those exact detached bytes; inserts it into the generic bundle's virtual file map;
and calls `validate_wave_d_combined_bundle`, which applies the generic validator to
the exact base subset and the domain validator to the full one-way-bound union.
`publish_wave_d_bundle(...)`
delegates exactly once to generic `publish_evidence_bundle` and may write only those
prepared immutable bytes. It cannot reread raw paths, profiles, callbacks, or
caller-owned objects. Candidate and closure builders reject any preexisting raw,
output, or sibling staging directory. Fault-injection tests cover every write and
rename boundary and prove malformed input or failed publication leaves the
destination and its parent byte-identical.

The builder reads raw timing/review bytes once, records their local SHA-256 in a
domain `privacy-transform.json`, removes absolute user paths, hostnames, PIDs,
resident-process rows, and gate telemetry from public copies, and preserves all
numeric spans, observation IDs, source/config/environment/machine digests, trigger
decisions, and semantic-output hashes. Candidate and closure publication fails if
any private token remains. Raw gate/process records stay ignored and may support
authorization only; they are never tracked evidence.

Freeze two closed tested-input policies in the wrapper. `wave-d0-inputs-v1`
selects the approved design, Wave 0 plan and schemas, this Wave D plan,
`docs/verification/remediation/performance-budget-v1.json`,
`tools/remediation_evidence.py`, `tools/build_wave_d_evidence.py`,
`tools/run_remediation_performance_profile.py`, `src/multiagent_elbo/performance.py`,
the counterexample catalog/experiment modules, `src/multiagent_elbo/cuda_backend.py`,
the Gaussian fixed-ray experiment/analysis modules, every test in the literal D0
targeted and subsystem suites, `pyproject.toml`, and
`environments/cuda-rtx5090-cu128.lock.txt`. `wave-d1-inputs-v1` contains every D0
input plus all conditionally changed CPU/CUDA worker paths, protocol-v3/v4 tests,
the launcher, the validated D0 export inventory, and each declared before/after
input. The wrapper resolves the exhaustive sorted inventories from Git, rejects
missing/extra/untracked matching inputs, and passes the policy plus the exact
source/config subset to the generic builder. Dependency inputs are exactly
`pyproject.toml` and `environments/cuda-rtx5090-cu128.lock.txt`.

The literal Wave-D binding surface is:

```python
D0_SOURCE_CONFIG_PATHS = (
    ".gitattributes", ".gitignore", "pyproject.toml",
    "environments/cuda-rtx5090-cu128.lock.txt",
    "docs/audits/2026-08-11-post-fixed-ray-deep-audit.md",
    "docs/superpowers/specs/2026-08-11-scientific-integrity-remediation-program-design.md",
    "docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md",
    "docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-d.md",
    "docs/verification/remediation/performance-budget-v1.json",
    "docs/verification/remediation/remediation-evidence-v1.schema.json",
    "tools/remediation_evidence.py", "tools/build_wave_d_evidence.py",
    "tools/run_remediation_performance_profile.py",
    "src/multiagent_elbo/performance.py",
    "src/multiagent_elbo/finite/counterexamples.py",
    "src/multiagent_elbo/finite/counterexample_experiment.py",
    "src/multiagent_elbo/cuda_backend.py", "tools/cuda_worker.py",
    "src/multiagent_elbo/realizations/gaussian/fixed_ray.py",
    "src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py",
    "src/multiagent_elbo/realizations/gaussian/confirmatory_analysis.py",
)
D0_TEST_PATHS = (
    "tests/test_performance.py", "tests/test_performance_launcher.py",
    "tests/test_counterexamples.py", "tests/test_counterexample_experiment.py",
    "tests/test_cuda_backend.py", "tests/test_gaussian_fixed_ray.py",
    "tests/test_gaussian_fixed_ray_experiment.py",
    "tests/test_gaussian_confirmatory_experiment.py",
    "tests/test_launchers.py", "tests/test_config.py", "tests/test_runtime.py",
    "tests/test_artifacts.py",
)
D1_SOURCE_CONFIG_PATHS = D0_SOURCE_CONFIG_PATHS
D1_TEST_PATHS = D0_TEST_PATHS
```

The tested-input selection rules are those literal paths plus `prefix:src/`,
`prefix:tests/`, `prefix:tools/`, `prefix:Theory/`, and all top-level Python files;
the exclusions are exactly Wave 0's evidence/cache exclusions. This makes the
policy exhaustive while the source/config binding subset remains auditable.

The CPU evidence environment is Wave 0's six-key policy. Additionally,
`MULTIAGENTELBO_PROFILE_OUTPUT`, `MULTIAGENTELBO_PROFILE_BASELINE`, and
`MULTIAGENTELBO_WORKER_TIMING_V1` must be absent before every generic `run-junit`;
profile records bind their exact temporary values together with machine, device,
determinism, configuration, source, and environment identities in the domain
inventory.

Freeze literal skip maps:

```python
CUDA_SKIP = {
    "tests.test_cuda_backend::test_pinned_cuda_worker_runs_first_job_with_determinism_environment":
        "requires explicit dedicated CUDA-lane opt-in",
}
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
}
SKIP_ALLOWLIST_BY_PROGRAM_AND_SUITE = {
    "d0": {"targeted": CUDA_SKIP, "subsystem": {**CUDA_SKIP, **CAPABILITY_SKIPS},
           "full": {**CUDA_SKIP, **CAPABILITY_SKIPS}},
    "d1": {"targeted": CUDA_SKIP, "subsystem": {**CUDA_SKIP, **CAPABILITY_SKIPS},
           "full": {**CUDA_SKIP, **CAPABILITY_SKIPS}},
}
```

Allowed skips may be absent; no other ID or reason is valid. Any amendment is a
checked-in contract change before P0/P1 and forces complete candidate and closure
reruns. Current XML can never amend the map.

For a closure bundle, `validate-domain` also requires an empty tracked diff and
index, parses both base and domain inventories, and compares the case-sensitive
normalized expected path set with `git ls-files --others --exclude-standard`.
The only permitted nonignored untracked bytes are the exact union inventoried under
that one closure directory; an extra file anywhere, an omitted indexed file, or a
path alias rejects before gate capture.

`populate-ledger --closure-index` resolves the sibling
`performance-evidence-inventory.json`, calls both validators again at live HEAD,
and refuses to populate a claim whose evidence is absent from either inventory.
It records both index hashes and the current gate-generated artifact revision in
every applicable evidence entry.

- [ ] **Step 4: Run CPU GREEN**

```powershell
$ErrorActionPreference = 'Stop'
C:\Python314\python.exe -B -m pytest tests\test_performance.py tests\test_performance_launcher.py tests\test_counterexample_experiment.py tests\test_cuda_backend.py -q -p no:cacheprovider --basetemp=.pytest-wave-d-task4-green --junitxml=.verification\wave-d-task4-green.xml
if ($LASTEXITCODE -ne 0) { throw 'Wave D Task 4 CPU GREEN failed' }
```

- [ ] **Step 5: Commit the D0 implementation parent and run the CPU profile twice**

```powershell
$ErrorActionPreference = 'Stop'
git add -- tools/run_remediation_performance_profile.py tools/build_wave_d_evidence.py tests/test_performance_launcher.py
if ($LASTEXITCODE -ne 0) { throw 'cannot stage D0 profile launcher' }
git commit -m "feat: publish remediation performance profile"
if ($LASTEXITCODE -ne 0) { throw 'D0 profile launcher commit failed' }
Remove-Item Env:MULTIAGENTELBO_PROFILE_BASELINE -ErrorAction SilentlyContinue
Remove-Item Env:MULTIAGENTELBO_WORKER_TIMING_V1 -ErrorAction SilentlyContinue
$env:MULTIAGENTELBO_PROFILE_OUTPUT = (Resolve-Path '.verification').Path + '\wave-d0-run-a'
if (Test-Path -LiteralPath $env:MULTIAGENTELBO_PROFILE_OUTPUT) { throw 'run A output exists' }
C:\Python314\python.exe -B tools\run_remediation_performance_profile.py
if ($LASTEXITCODE -ne 0) { throw 'D0 profile run A failed' }
$launcherPath = (Resolve-Path 'tools\run_remediation_performance_profile.py').Path
$externalCwd = 'C:\tmp\MultiAgentELBO-wave-d0-external-cwd'
if (Test-Path -LiteralPath $externalCwd) { throw 'external profile CWD exists' }
New-Item -ItemType Directory -Path $externalCwd | Out-Null
Push-Location $externalCwd
$env:MULTIAGENTELBO_PROFILE_OUTPUT = (Resolve-Path $externalCwd).Path + '\wave-d0-run-b'
& 'C:\Python314\python.exe' -B $launcherPath
if ($LASTEXITCODE -ne 0) { throw 'D0 profile run B failed' }
Pop-Location
Remove-Item Env:MULTIAGENTELBO_PROFILE_OUTPUT
```

The serialized command record contains the resolved real launcher path. Require
semantic timing-schema equality apart from actual durations and root-dependent
operational fields. Evaluate the CPU rule mechanically.

- [ ] **Step 6: Stop for exact GPU authorization if CUDA attribution is needed**

First verify the CUDA interpreter without starting a model job:

```powershell
$ErrorActionPreference = 'Stop'
& 'C:\anaconda\python.exe' -c 'import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))'
if ($LASTEXITCODE -ne 0) { throw 'CUDA interpreter verification failed' }
```

Capture a fresh Wave-C idle gate at the exact D0 source/config/environment. Present its digest and observed processes to the user and obtain exact acceptance. If authorization is absent, serialize `cuda_measurement_decision="inconclusive"` and do not run the 10 exchanges. If accepted, recheck before every exchange and stop on occupancy/config/process drift; never start the 40-job sweep.

- [ ] **Step 7: Adjudicate D1 triggers before writing optimization code**

Persist the raw observations and exact rule outputs. If a rule returns `retain`, mark that subsystem's D1 `not_triggered` and make no optimization. If it returns `inconclusive`, state the open obligation. Only `optimize` authorizes the corresponding Task 6 or Task 7, and only after Task 5's D0 ledger validates.

### Task 5: Close D0 before authorizing any D1 work

**Files:**
- Create and commit candidate evidence in the SHA-named child of
  `docs/verification/evidence/wave-d0/`.
- Create uncommitted exact-child evidence in the SHA-named child of
  `verification-evidence/wave-d0/`.
- Create ignored `.verification/wave-d0/final-ledger.json`.

**Interfaces:**
- `tools/build_wave_d_evidence.py build --program d0 --stage candidate ...`
  creates a sanitized
  candidate index whose `tested_git_head` and `implementation_parent_git_head`
  both equal `P0`.
- `tools/build_wave_d_evidence.py build --program d0 --stage closure ...` creates a
  closure index only after exact-child profiles, JUnit, and review files exist.
- D0 closes timing-schema integrity and the mechanical trigger decisions only.
  It does not mark either performance defect remediated.

- [ ] **Step 1: Run candidate suites and profile at clean implementation head `P0`**

```powershell
$ErrorActionPreference = 'Stop'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
Remove-Item Env:MULTIAGENTELBO_PROFILE_OUTPUT -ErrorAction SilentlyContinue
Remove-Item Env:MULTIAGENTELBO_PROFILE_BASELINE -ErrorAction SilentlyContinue
Remove-Item Env:MULTIAGENTELBO_WORKER_TIMING_V1 -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'
$p0 = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve P0' }
$p0Short = $p0.Substring(0, 12)
$raw = ".verification\raw\wave-d0\$p0Short\candidate"
$public = "docs\verification\evidence\wave-d0\$p0Short"
if (git status --porcelain=v1) { throw 'P0 worktree is not clean' }
if ($LASTEXITCODE -ne 0) { throw 'cannot inspect P0 worktree' }
if (Test-Path -LiteralPath $raw) { throw 'P0 candidate raw directory exists' }
if (Test-Path -LiteralPath $public) { throw 'P0 candidate output exists' }
$rawParent = Split-Path -Parent $raw
if (-not (Test-Path -LiteralPath $rawParent)) {
  New-Item -ItemType Directory -Path $rawParent | Out-Null
}
New-Item -ItemType Directory -Path $raw | Out-Null
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$raw\targeted.command.json" --junit "$raw\targeted.raw.xml" -- C:\Python314\python.exe -B -m pytest tests\test_performance.py tests\test_performance_launcher.py tests\test_counterexamples.py tests\test_counterexample_experiment.py tests\test_cuda_backend.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py -q -p no:cacheprovider --basetemp=.pytest-wave-d0-p0-targeted --junitxml="$raw\targeted.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 P0 targeted suite failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$raw\subsystem.command.json" --junit "$raw\subsystem.raw.xml" -- C:\Python314\python.exe -B -m pytest tests\test_performance.py tests\test_performance_launcher.py tests\test_counterexamples.py tests\test_counterexample_experiment.py tests\test_cuda_backend.py tests\test_gaussian_fixed_ray.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py tests\test_launchers.py tests\test_config.py tests\test_runtime.py tests\test_artifacts.py -q -p no:cacheprovider --basetemp=.pytest-wave-d0-p0-subsystem --junitxml="$raw\subsystem.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 P0 subsystem suite failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$raw\full.command.json" --junit "$raw\full.raw.xml" -- C:\Python314\python.exe -B -m pytest -q -p no:cacheprovider --basetemp=.pytest-wave-d0-p0-full --junitxml="$raw\full.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 P0 full suite failed' }
$env:MULTIAGENTELBO_PROFILE_OUTPUT = "$raw\profile"
C:\Python314\python.exe -B tools\run_remediation_performance_profile.py
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 P0 profile failed' }
Remove-Item Env:MULTIAGENTELBO_PROFILE_OUTPUT
C:\Python314\python.exe -B tools\build_wave_d_evidence.py build --program d0 --stage candidate --tested-head $p0 --implementation-parent $p0 --raw-dir $raw --output-dir $public
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 P0 evidence build failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py validate "$public\index.json" --cwd .
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 P0 base index validation failed' }
C:\Python314\python.exe -B tools\build_wave_d_evidence.py validate-domain --bundle-dir $public
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 P0 domain validation failed' }
```

The wrapper applies the literal per-suite maps frozen above; current XML can never
authorize an amendment. It records raw XML hashes and deterministic privacy
transforms before writing tracked copies.

- [ ] **Step 2: Commit the candidate evidence-only child `E0`**

```powershell
$ErrorActionPreference = 'Stop'
$p0 = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve P0 before evidence commit' }
$p0Short = $p0.Substring(0, 12)
$public = "docs\verification\evidence\wave-d0\$p0Short"
if (-not (Test-Path -LiteralPath "$public\index.json")) { throw 'P0 candidate index absent' }
git add -- $public
if ($LASTEXITCODE -ne 0) { throw 'cannot stage P0 candidate evidence' }
git diff --cached --name-only
if ($LASTEXITCODE -ne 0) { throw 'cannot inspect staged P0 candidate evidence' }
$staged = @(git diff --cached --name-only)
if ($staged.Count -eq 0 -or @($staged | Where-Object { $_ -notlike "docs/verification/evidence/wave-d0/$p0Short/*" }).Count -ne 0) {
    throw 'P0 candidate staged set is not exactly its SHA directory'
}
git commit -m "test: record wave D0 candidate evidence"
if ($LASTEXITCODE -ne 0) { throw 'P0 candidate evidence commit failed' }
$e0 = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve E0' }
if ((git rev-parse HEAD^).Trim() -ne $p0) { throw 'E0 is not the direct child of P0' }
$bad = git diff --name-only $p0..$e0 | Where-Object { $_ -notlike "docs/verification/evidence/wave-d0/$p0Short/*" }
if ($LASTEXITCODE -ne 0) { throw 'cannot inspect P0..E0' }
if ($bad) { throw "non-evidence path in P0..E0: $bad" }
```

- [ ] **Step 3: Rerun suites and the CPU profile at exact `E0`**

```powershell
$ErrorActionPreference = 'Stop'
$e0 = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve E0 for closure' }
$p0 = (git rev-parse HEAD^).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve P0 parent for closure' }
$e0Short = $e0.Substring(0, 12)
$closure = "verification-evidence\wave-d0\$e0Short"
$closureRaw = ".verification\raw\wave-d0\$e0Short\closure"
if (git status --porcelain=v1) { throw 'E0 is not clean before closure staging' }
if ($LASTEXITCODE -ne 0) { throw 'cannot inspect E0 status' }
if (Test-Path -LiteralPath $closureRaw) { throw 'E0 closure raw directory exists' }
if (Test-Path -LiteralPath $closure) { throw 'E0 closure output exists' }
$closureRawParent = Split-Path -Parent $closureRaw
if (-not (Test-Path -LiteralPath $closureRawParent)) {
  New-Item -ItemType Directory -Path $closureRawParent | Out-Null
}
New-Item -ItemType Directory -Path $closureRaw | Out-Null
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
Remove-Item Env:MULTIAGENTELBO_PROFILE_OUTPUT -ErrorAction SilentlyContinue
Remove-Item Env:MULTIAGENTELBO_PROFILE_BASELINE -ErrorAction SilentlyContinue
Remove-Item Env:MULTIAGENTELBO_WORKER_TIMING_V1 -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$closureRaw\targeted.command.json" --junit "$closureRaw\targeted.raw.xml" -- C:\Python314\python.exe -B -m pytest tests\test_performance.py tests\test_performance_launcher.py tests\test_counterexamples.py tests\test_counterexample_experiment.py tests\test_cuda_backend.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py -q -p no:cacheprovider --basetemp=.pytest-wave-d0-e0-targeted --junitxml="$closureRaw\targeted.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 E0 targeted suite failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$closureRaw\subsystem.command.json" --junit "$closureRaw\subsystem.raw.xml" -- C:\Python314\python.exe -B -m pytest tests\test_performance.py tests\test_performance_launcher.py tests\test_counterexamples.py tests\test_counterexample_experiment.py tests\test_cuda_backend.py tests\test_gaussian_fixed_ray.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py tests\test_launchers.py tests\test_config.py tests\test_runtime.py tests\test_artifacts.py -q -p no:cacheprovider --basetemp=.pytest-wave-d0-e0-subsystem --junitxml="$closureRaw\subsystem.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 E0 subsystem suite failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$closureRaw\full.command.json" --junit "$closureRaw\full.raw.xml" -- C:\Python314\python.exe -B -m pytest -q -p no:cacheprovider --basetemp=.pytest-wave-d0-e0-full --junitxml="$closureRaw\full.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 E0 full suite failed' }
$env:MULTIAGENTELBO_PROFILE_OUTPUT = "$closureRaw\profile"
C:\Python314\python.exe -B tools\run_remediation_performance_profile.py
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 E0 profile failed' }
Remove-Item Env:MULTIAGENTELBO_PROFILE_OUTPUT
```

If exact-revision CUDA measurement is authorized, capture/accept a fresh E0 gate
and run the bounded 10-exchange harness before continuing. Otherwise the profile
must serialize an `inconclusive` CUDA trigger and its open obligation.

- [ ] **Step 4: Create current D0 reviews before freezing the closure index**

Place code, performance-method, and experiment/provenance review JSON records in
`$closureRaw\reviews\`. The builder privacy-validates and copies them into the
indexed closure bundle. Each record contains reviewer role, reviewed E0/head and
profile/JUnit hashes, verdict, findings, and falsification conditions. Review
agreement is not evidence; the raw profile and JUnit remain load-bearing.

The preceding D0 review step is superseded by this exact E0/P0 sequence. Before
any review exists, compute the detached context. Obtain only the selected raw
two-, four-, or eight-view review files and exactly seven raw adjudicators after
that digest has been supplied to independent reviewers. Do not create `$closure`,
an index, a ledger, or any public review before the final command succeeds.

```powershell
$reviewContextSha = (& C:\Python314\python.exe -B tools\build_wave_d_evidence.py review-context-sha --program d0 --tested-head $e0 --implementation-parent $p0 --raw-dir $closureRaw).Trim()
if ($LASTEXITCODE -ne 0 -or $reviewContextSha -notmatch '^[0-9a-f]{64}$') { throw 'D0 review context failed' }
if (Test-Path -LiteralPath $closure) { throw 'D0 context created closure bytes' }
$reviewTarget = [int]((& C:\Python314\python.exe -B tools\build_wave_d_evidence.py review-target --program d0 --tested-head $e0 --implementation-parent $p0 --raw-dir $closureRaw).Trim())
if ($LASTEXITCODE -ne 0 -or $reviewTarget -notin @(2,4,8)) { throw 'D0 review target invalid' }
# Write only selected raw reviews and all seven raw adjudicators under $closureRaw\reviews.
& C:\Python314\python.exe -B tools\build_wave_d_evidence.py validate-reviews --program d0 --tested-head $e0 --implementation-parent $p0 --raw-dir $closureRaw
if ($LASTEXITCODE -ne 0) { throw 'D0 raw reviews/adjudicators invalid' }
if (Test-Path -LiteralPath $closure) { throw 'D0 review validation created closure bytes' }
```

`build --stage closure` is permitted only after that validator. It copies the
validated raw review/adjudicator bytes through the total transform exactly once;
it may not regenerate them or silently add the older experiment/provenance
review name. The E0/P0 direct-child/evidence-only checks in Steps 2 and 3 remain
mandatory and are a precondition to the context command.

- [ ] **Step 5: Build/validate the closure index and populate the D0 ledger**

```powershell
$ErrorActionPreference = 'Stop'
$e0 = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve E0 for final D0 closure' }
$p0 = (git rev-parse HEAD^).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve P0 for final D0 closure' }
$e0Short = $e0.Substring(0, 12)
$closureRaw = ".verification\raw\wave-d0\$e0Short\closure"
$closure = "verification-evidence\wave-d0\$e0Short"
if (-not (Test-Path -LiteralPath "$closureRaw\reviews")) { throw 'D0 current reviews absent' }
if (Test-Path -LiteralPath $closure) { throw 'D0 closure output already exists' }
C:\Python314\python.exe -B tools\build_wave_d_evidence.py build --program d0 --stage closure --tested-head $e0 --implementation-parent $p0 --raw-dir $closureRaw --output-dir $closure
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 closure build failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py validate "$closure\index.json" --cwd .
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 closure base index failed' }
C:\Python314\python.exe -B tools\build_wave_d_evidence.py validate-domain --bundle-dir $closure
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 closure domain/worktree validation failed' }
$ledger = '.verification\wave-d0\final-ledger.json'
$active = '.verification\active.json'
if (Test-Path -LiteralPath $active) { throw 'preexisting verification gate is active' }
if (Test-Path -LiteralPath $ledger) { throw 'preexisting D0 ledger exists' }
& 'C:\Python314\python.exe' -B tools\remediation_evidence.py run-verification-gate --snapshot docs/verification/remediation/verification-contract-v1.json --root 'C:\Users\chris and christine\.codex\skills\verification' -- start --cwd . --mode closure --ledger $ledger
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 gate start failed' }
& 'C:\Python314\python.exe' -B tools\remediation_evidence.py run-verification-gate --snapshot docs/verification/remediation/verification-contract-v1.json --root 'C:\Users\chris and christine\.codex\skills\verification' -- validate --cwd . $ledger
if ($LASTEXITCODE -eq 0) { throw 'empty Wave D0 template unexpectedly validated' }
C:\Python314\python.exe -B tools\build_wave_d_evidence.py populate-ledger --program d0 --ledger $ledger --closure-index "$closure\index.json"
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 ledger population failed' }
```

The populated ledger follows the binding measurement-only polarity projection above. Timing
schema/output identity and every mechanically eligible trigger decision are
`EVIDENCE_VERIFIED`. For CPU AUD-22 and CUDA AUD-21 separately: `retain` supports the
positive proposition "the preregistered material-dominance defect still occurs at
E0" `REFUTED` and verifies the measurement/decision guard; `optimize` makes that
defect proposition `EVIDENCE_VERIFIED` at E0 and leaves its remediation obligation
open for D1; `inconclusive` leaves both the defect and remediation claims
`INCONCLUSIVE` with the exact missing-authorization/profile obligation. Historical
audit findings remain revision-bound history. Then run:

The preceding legacy shorthand is superseded in full by the binding D0
measurement-only polarity section; no defect or remediation claim is projected.

```powershell
$ErrorActionPreference = 'Stop'
$ledger = '.verification\wave-d0\final-ledger.json'
& 'C:\Python314\python.exe' -B tools\remediation_evidence.py run-verification-gate --snapshot docs/verification/remediation/verification-contract-v1.json --root 'C:\Users\chris and christine\.codex\skills\verification' -- validate --cwd . $ledger
if ($LASTEXITCODE -ne 0) { throw 'Wave D0 ledger validation failed' }
```

- [ ] **Step 6: Enforce the D0-to-D1 barrier**

Do not edit D1 production code until the D0 ledger validates at exact E0. A
subsystem may proceed only when its serialized exact-E0 trigger is `optimize`;
`retain` means no code change, and `inconclusive` leaves remediation open.

If D1 is authorized, do not reuse the closure worktree: its nonignored E0 closure
bytes are part of the exact D0 artifact. Preserve it read-only, create a fresh
isolated D1 worktree at E0, and copy the D0 ledger plus its complete indexed
closure bundle into the new worktree's ignored
`.verification/upstream-wave-d0/`. Record and recheck the source ledger/index
SHA-256 and every indexed file hash after copying. This imported record is an
immutable historical dependency that authorized D1; it is not relabeled as a
current P1/E1 closure ledger and is never passed to `verification_gate.py
validate` against the new artifact revision.

```powershell
$ErrorActionPreference = 'Stop'
$e0 = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve verified E0 for export' }
$e0Short = $e0.Substring(0, 12)
$closure = "verification-evidence\wave-d0\$e0Short"
$d0Export = "C:\tmp\MultiAgentELBO-wave-d0-upstream-$e0Short"
$d1Worktree = "C:\tmp\MultiAgentELBO-wave-d1-$e0Short"
if (Test-Path -LiteralPath $d0Export) { throw 'D0 export destination exists' }
if (Test-Path -LiteralPath $d1Worktree) { throw 'D1 worktree destination exists' }
C:\Python314\python.exe -B tools\build_wave_d_evidence.py export-upstream --ledger .verification\wave-d0\final-ledger.json --closure-dir $closure --output-dir $d0Export
if ($LASTEXITCODE -ne 0) { throw 'D0 upstream export failed' }
C:\Python314\python.exe -B tools\build_wave_d_evidence.py validate-upstream --bundle-dir $d0Export
if ($LASTEXITCODE -ne 0) { throw 'D0 upstream export validation failed' }
git worktree add -b codex/scientific-integrity-remediation-wave-d1-20260811 $d1Worktree $e0
if ($LASTEXITCODE -ne 0) { throw 'D1 worktree creation failed' }
if (Test-Path -LiteralPath "$d1Worktree\.verification\upstream-wave-d0") {
    throw 'D1 upstream destination unexpectedly exists'
}
Copy-Item -LiteralPath $d0Export -Destination "$d1Worktree\.verification\upstream-wave-d0" -Recurse
Push-Location $d1Worktree
C:\Python314\python.exe -B tools\build_wave_d_evidence.py validate-upstream --bundle-dir .verification\upstream-wave-d0
if ($LASTEXITCODE -ne 0) { throw 'copied D0 upstream validation failed' }
Pop-Location
```

The export command refuses an existing destination and writes a closed canonical
inventory of the ledger, index, and every indexed closure byte. The validation
command rejects missing/extra/hash-drifted bytes.

### Task 6: Conditionally cache one immutable exact CPU catalog (`AUD-22`)

**Files:**
- Modify only if CPU trigger is `optimize`: `src/multiagent_elbo/finite/counterexample_experiment.py`
- Modify: `tests/test_counterexample_experiment.py`
- Modify: `tests/test_counterexamples.py`

**Interfaces:**
- Produces `ExactCatalogIdentity(schema_version, max_states, max_denominator,
  algorithm_version)` and accepts only the registered identity
  `("finite-counterexample-catalog-v1", 2, 4, 1)`.
- Produces `_frozen_exact_candidates(identity) -> FrozenCandidateCatalog` with
  `functools.lru_cache(maxsize=1)`. The frozen result contains only the expensive
  exact `candidates` and `minimal` tuples; `_catalog(config)` still derives every
  config-dependent bound, metric, stress assessment, and publication payload on
  each call.
- Returns frozen `CandidateRecord` tuples; callers receive the immutable tuple or
  detached serialization, never a shared mutable mapping/array.
- Mutation/monkeypatch tests bypass or clear the cache explicitly so controls remain effective.

- [ ] **Step 1: Write call-count, immutability, and mutation-control RED tests**

```python
def test_registered_catalog_enumerates_once_for_twenty_identical_calls(monkeypatch, config):
    module._frozen_exact_candidates.cache_clear()
    calls = 0
    original = module._enumerate_candidates
    def counted(*args, **kwargs):
        nonlocal calls
        calls += 1
        return original(*args, **kwargs)
    monkeypatch.setattr(module, "_enumerate_candidates", counted)
    results = [module._catalog(config) for _ in range(20)]
    assert calls == 1
    assert len({catalog_semantic_sha256(result) for result in results}) == 1


def test_catalog_cache_rejects_unregistered_identity_before_enumeration(monkeypatch):
    module._frozen_exact_candidates.cache_clear()
    monkeypatch.setattr(module, "_enumerate_candidates", forbidden("enumeration"))
    changed = dataclasses.replace(REGISTERED_CATALOG_IDENTITY, max_denominator=5)
    with pytest.raises(ValueError, match="registered catalog identity"):
        module._frozen_exact_candidates(changed)


def test_catalog_controls_clear_cache_before_injection(monkeypatch, config):
    module._frozen_exact_candidates.cache_clear()
    with monkeypatch.context() as patch:
        original = module._enumerate_candidates
        patch.setattr(
            module,
            "_enumerate_candidates",
            lambda laws, channels: (*original(laws, channels), injected_counterexample()),
        )
        assert injected_counterexample() in module._catalog(config)[2]
```

Also assert the tuple records are frozen and every nested public array/mapping is
immutable or detached.

- [ ] **Step 2: Run the cache RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_counterexamples.py tests\test_counterexample_experiment.py -k "catalog_cache or enumerates_once" -q -p no:cacheprovider --basetemp=.pytest-wave-d1-task6-red --junitxml=.verification\wave-d1-task6-red.xml
```

Expected: FAIL because no identity-bound cache exists and 20 calls enumerate 20
times.

- [ ] **Step 3: Implement the minimal one-entry cache and run affected tests**

```python
@dataclass(frozen=True)
class FrozenCandidateCatalog:
    candidates: tuple[CandidateRecord, ...]
    minimal: tuple[CandidateRecord, ...]


@functools.lru_cache(maxsize=1)
def _frozen_exact_candidates(identity: ExactCatalogIdentity) -> FrozenCandidateCatalog:
    if identity != REGISTERED_CATALOG_IDENTITY:
        raise ValueError("only the registered catalog identity is supported")
    laws = tuple(enumerate_rational_laws(identity.max_states, identity.max_denominator))
    channels = tuple(enumerate_rational_channels(2, 2, identity.max_denominator))
    candidates = tuple(_enumerate_candidates(laws, channels))
    return FrozenCandidateCatalog(candidates, tuple(minimize_candidates(candidates)))
```

`_catalog(config)` obtains this frozen exact result, then reconstructs all other
return fields afresh. It never caches output-root, run-seed, diagnostics-toggle,
metric, or publication objects.

```powershell
C:\Python314\python.exe -B -m pytest tests\test_counterexamples.py tests\test_counterexample_experiment.py -q -p no:cacheprovider --basetemp=.pytest-wave-d1-task6-green --junitxml=.verification\wave-d1-task6-green.xml
```

- [ ] **Step 4: Reprofile with the exact D0 harness and commit only on trigger**

Require identical canonical candidate/minimal JSON, metric records, stress
records, and per-array results, then commit:

```powershell
git add -- src/multiagent_elbo/finite/counterexample_experiment.py tests/test_counterexample_experiment.py tests/test_counterexamples.py
git commit -m "perf: reuse immutable exact catalog"
```

If the trigger did not fire, record `not_triggered` and omit this commit entirely.

### Task 7: Conditionally batch one paired fixed-ray job per worker (`AUD-21`)

**Files:**
- Modify only if CUDA trigger is `optimize`: `src/multiagent_elbo/cuda_backend.py`
- Modify: `tools/cuda_worker.py`
- Modify: `src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py`
- Modify: `tests/test_cuda_backend.py`
- Modify: `tests/test_gaussian_fixed_ray_experiment.py`
- Modify: `tests/test_gaussian_confirmatory_experiment.py`

**Interfaces:**
- Adds paired-job protocol v4 for one outer paired job containing exactly 2 schemes x 8 ordered steps; Wave C protocol v3 remains read-only and is the before-path comparator.
- One request/response retains 16 immutable exchange subrecords and scientific array hashes.
- Gate expiry and per-job recheck occur before launch; one process failure consumes the outer job's sole retry; crash-resume either validates a complete paired response or terminalizes the job.
- `PairedWorkerRequestV4` has the closed field inventory
  `{schema_version, message_type, job_id, requested, gate_binding,
  scientific_system_digest, execution_binding_digest, ordered_exchanges,
  npz_sha256, arrays, output_identity}`. `requested` is exactly Wave C's
  nine-field `WorkerRuntimeBindingV3`. `gate_binding` has exactly
  `{gate_digest, gate_record_sha256, recheck_digest, recheck_record_sha256}`.
  `ordered_exchanges` is an exact 16-tuple whose closed record fields are
  `{exchange_id, scheme, step, input_array_names}`; all scientific inputs live in
  the single described NPZ. `output_identity` is `None` in a request.
- `PairedWorkerResponseV4` has the closed field inventory
  `{schema_version, message_type, job_id, requested, observed, gate_binding,
  scientific_system_digest, execution_binding_digest, ordered_subrecords,
  npz_sha256, arrays, output_identity}`. `requested` and
  `observed` are exact Wave-C runtime bindings and must match. Every closed
  subrecord retains `{exchange_id, input_sha256, output_array_names,
  semantic_sha256, decisions}`. The full response identity is SHA-256 over
  `b"multiagent-elbo/cuda-worker-paired-response/v4\0"` plus canonical response
  JSON with `output_identity=None`; no other field is excluded.

- [ ] **Step 1: Write 16-subrecord parity and ordering RED tests**

```python
def test_paired_job_v4_matches_sixteen_v3_fake_worker_calls(identity, paired_inputs):
    v3 = tuple(run_one_v3_exchange(item, identity=identity) for item in paired_inputs)
    v4 = run_paired_v4_job(paired_inputs, identity=identity)
    assert [record.exchange_id for record in v4.subrecords] == EXPECTED_16_EXCHANGE_IDS
    assert tuple(record.semantic_sha256 for record in v4.subrecords) == tuple(
        worker_result_semantic_sha256(record) for record in v3
    )
    assert all(record.scientific_system_digest == identity.scientific_system_digest for record in v4.subrecords)
    assert all(record.execution_binding_digest == identity.execution_binding_digest for record in v4.subrecords)
```

Assert exact scheme-major/step-minor order, every subrequest/subresponse hash, one
gate/recheck binding, and a closed v4 field inventory.

- [ ] **Step 2: Write crash/retry/expiry/resume RED tests**

```python
@pytest.mark.parametrize("boundary", [
    "before_substep_1", "after_substep_8", "during_response_write",
    "after_response_before_outer_record",
])
def test_paired_job_failure_consumes_only_outer_retry(boundary, harness):
    harness.fail_at(boundary)
    terminal = harness.run_with_one_outer_retry()
    assert terminal.outer_attempts <= 2
    assert terminal.partial_response_eligible is False


def test_expired_gate_stops_before_v4_process_launch(expired_gate, monkeypatch):
    monkeypatch.setattr(subprocess, "run", forbidden("process launch"))
    with pytest.raises(ValueError, match="expired"):
        run_paired_v4_job(VALID_INPUTS, gate=expired_gate, identity=IDENTITY)
```

Restart tests validate a complete response or terminalize; they never reuse a
partial sidecar/response.

- [ ] **Step 3: Run the paired-job RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_cuda_backend.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py -k "paired_v4 or sixteen_v3 or outer_retry" -q -p no:cacheprovider --basetemp=.pytest-wave-d1-task7-red --junitxml=.verification\wave-d1-task7-red.xml
```

Expected: FAIL because protocol v4 and paired-job orchestration do not exist.

- [ ] **Step 4: Implement the paired-job protocol and run CPU fault tests**

```python
@dataclass(frozen=True)
class PairedWorkerRequestV4:
    schema_version: Literal["cuda-worker-paired-request-v4"]
    message_type: Literal["paired_request"]
    job_id: str
    requested: WorkerRuntimeBindingV3
    gate_binding: PairedGateBindingV4
    scientific_system_digest: str
    execution_binding_digest: str
    ordered_exchanges: tuple[PairedExchangeInput, ...]
    npz_sha256: str
    arrays: tuple[WorkerArrayDescriptor, ...]
    output_identity: None = None

    def __post_init__(self) -> None:
        if tuple(item.exchange_id for item in self.ordered_exchanges) != EXPECTED_16_EXCHANGE_IDS:
            raise ValueError("paired request must contain the exact ordered 16 exchanges")


@dataclass(frozen=True)
class PairedWorkerResponseV4:
    schema_version: Literal["cuda-worker-paired-response-v4"]
    message_type: Literal["paired_response"]
    job_id: str
    requested: WorkerRuntimeBindingV3
    observed: WorkerRuntimeBindingV3
    gate_binding: PairedGateBindingV4
    scientific_system_digest: str
    execution_binding_digest: str
    ordered_subrecords: tuple[PairedExchangeResult, ...]
    npz_sha256: str
    arrays: tuple[WorkerArrayDescriptor, ...]
    output_identity: str
```

Construct and canonicalize the entire request before process launch. The worker
validates all common fields once, executes each frozen subrequest serially in the
declared order, synchronizes before each result snapshot, and writes one response
atomically. The controller validates the response and every subrecord before any
outer job record is eligible. As in v3, the validated worker provenance remains a
separate immutable member of `PairedWorkerJobResultV4`; it is not smuggled into
the response-identity schema.

```powershell
C:\Python314\python.exe -B -m pytest tests\test_cuda_backend.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py -q -p no:cacheprovider --basetemp=.pytest-wave-d1-task7-green --junitxml=.verification\wave-d1-task7-green.xml
```

- [ ] **Step 5: Commit only after exact CPU semantic parity**

```powershell
git add -- src/multiagent_elbo/cuda_backend.py tools/cuda_worker.py src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py tests/test_cuda_backend.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py
git commit -m "perf: batch fixed-ray paired jobs"
```

- [ ] **Step 6: Require a new exact-revision GPU gate before any operational claim**

The D0 gate is stale because D1 changed the worker/request-response path. Obtain
fresh exact-E1 acceptance only for the separately scoped five-job v4 sentinel,
run only that sentinel, and close only its literal sentinel claim. The 40-job
confirmatory sweep is excluded from Wave D and remains forbidden even if later
requested in a different context. Without the fresh sentinel authorization and
rerun, CUDA operational and performance states remain `INCONCLUSIVE`.

### Task 8: Close conditional D1 at a separate exact revision and serially integrate

**Files:**
- Create only when at least one exact-E0 trigger is `optimize`: candidate evidence
  in `docs/verification/evidence/wave-d1/{P1-short}/`.
- Create only when D1 runs: uncommitted closure evidence in
  `verification-evidence/wave-d1/{E1-short}/`.
- Create only when D1 runs: ignored `.verification/wave-d1/final-ledger.json`.

**Interfaces:**
- If both exact-E0 triggers are `retain` or `inconclusive`, skip Steps 2-9 and
  perform Step 10 with E0 as the terminal Wave-D revision: measurement/trigger
  claims retain their D0 ledger states. Each eligible `retain` closes its positive
  current-revision material-dominance proposition as `REFUTED` and verifies the
  guard; only each `inconclusive` subsystem remains `INCONCLUSIVE`.
- If either trigger is `optimize`, `P1` is the final D1 implementation head and
  `E1` is its direct evidence-only child. D1 does not reuse the D0 closure index
  or ledger.
- `tools/build_wave_d_evidence.py build --program d1 --stage
  {candidate,closure}` uses the exact Wave-0 evidence schema and additionally
  accepts `--d0-bundle-dir`, reruns `validate-upstream` during every prepare, and
  binds the upstream export-inventory hash plus every declared D0 ledger/index/
  closure byte, the frozen trigger record, before/after profiles, and canonical
  scientific-output hashes. A standalone ledger/index path is never sufficient.
- A fresh sentinel can close only its exact sentinel protocol/parity claim. It
  cannot close the CUDA performance-improvement, confirmatory, 40-job
  equivalence, or full-sweep claims.
- Historical 60.7-minute evidence remains context, not a causal profile or SLA.

- [ ] **Step 1: Stop without a D1 commit when no trigger authorizes optimization**

Parse the validated E0 decision record, never a console summary:

```powershell
$ErrorActionPreference = 'Stop'
$e0 = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve terminal E0' }
$e0Short = $e0.Substring(0, 12)
$d0Decision = Get-Content -Raw "verification-evidence\wave-d0\$e0Short\profile\decision.json" | ConvertFrom-Json
$triggered = @($d0Decision.cpu_catalog, $d0Decision.cuda_exchange) | Where-Object { $_ -eq 'optimize' }
if ($triggered.Count -eq 0) {
    Write-Output 'D1 not authorized by the frozen D0 decision; E0 is terminal.'
}
```

When this branch is taken, do not edit Tasks 6 or 7 production paths and do not
manufacture a D1 evidence child. Record the open obligation for every
`inconclusive` decision in the D0 ledger. `retain` means the preregistered current
material-dominance proposition was mechanically refuted under the bounded D0 rule;
the historical aggregate observation remains true only for its recorded revision
and is not relabeled.

- [ ] **Step 2: Freeze final D1 implementation head `P1` after authorized tasks**

Run only Tasks 6 and/or 7 whose exact-E0 trigger is `optimize`. After their
commits, require a clean tree and bind ancestry:

```powershell
$ErrorActionPreference = 'Stop'
$d0Bundle = ".verification\upstream-wave-d0"
$d0Ledger = ".verification\upstream-wave-d0\final-ledger.json"
$d0Index = ".verification\upstream-wave-d0\closure\index.json"
C:\Python314\python.exe -B tools\build_wave_d_evidence.py validate-upstream --bundle-dir $d0Bundle
if ($LASTEXITCODE -ne 0) { throw 'D0 upstream dependency failed before P1 evidence' }
$d0IndexPayload = Get-Content -Raw -LiteralPath $d0Index | ConvertFrom-Json
$e0 = [string]$d0IndexPayload.tested_git_head
$e0Short = $e0.Substring(0, 12)
$p1 = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve P1' }
$p1Short = $p1.Substring(0, 12)
git merge-base --is-ancestor $e0 $p1
if ($LASTEXITCODE -ne 0) { throw 'P1 does not descend from verified E0' }
if (git status --porcelain=v1) { throw 'P1 worktree is not clean' }
if ($LASTEXITCODE -ne 0) { throw 'cannot inspect P1 worktree' }
if (-not (Test-Path -LiteralPath $d0Ledger) -or -not (Test-Path -LiteralPath $d0Index)) { throw 'verified D0 dependency is absent' }
$raw = ".verification\raw\wave-d1\$p1Short\candidate"
$public = "docs\verification\evidence\wave-d1\$p1Short"
if (Test-Path -LiteralPath $raw) { throw 'P1 candidate raw directory exists' }
if (Test-Path -LiteralPath $public) { throw 'P1 candidate output exists' }
$rawParent = Split-Path -Parent $raw
if (-not (Test-Path -LiteralPath $rawParent)) {
  New-Item -ItemType Directory -Path $rawParent | Out-Null
}
New-Item -ItemType Directory -Path $raw | Out-Null
```

- [ ] **Step 3: Run candidate targeted, subsystem, and full CPU suites at `P1`**

```powershell
$ErrorActionPreference = 'Stop'
$p1 = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve P1 for suites' }
$p1Short = $p1.Substring(0, 12)
$raw = ".verification\raw\wave-d1\$p1Short\candidate"
if (-not (Test-Path -LiteralPath $raw)) { throw 'P1 raw staging absent' }
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
Remove-Item Env:MULTIAGENTELBO_PROFILE_OUTPUT -ErrorAction SilentlyContinue
Remove-Item Env:MULTIAGENTELBO_PROFILE_BASELINE -ErrorAction SilentlyContinue
Remove-Item Env:MULTIAGENTELBO_WORKER_TIMING_V1 -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$raw\targeted.command.json" --junit "$raw\targeted.raw.xml" -- C:\Python314\python.exe -B -m pytest tests\test_performance.py tests\test_performance_launcher.py tests\test_counterexamples.py tests\test_counterexample_experiment.py tests\test_cuda_backend.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py -q -p no:cacheprovider --basetemp=.pytest-wave-d1-p1-targeted --junitxml="$raw\targeted.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 P1 targeted suite failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$raw\subsystem.command.json" --junit "$raw\subsystem.raw.xml" -- C:\Python314\python.exe -B -m pytest tests\test_performance.py tests\test_performance_launcher.py tests\test_counterexamples.py tests\test_counterexample_experiment.py tests\test_cuda_backend.py tests\test_gaussian_fixed_ray.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py tests\test_launchers.py tests\test_config.py tests\test_runtime.py tests\test_artifacts.py -q -p no:cacheprovider --basetemp=.pytest-wave-d1-p1-subsystem --junitxml="$raw\subsystem.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 P1 subsystem suite failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$raw\full.command.json" --junit "$raw\full.raw.xml" -- C:\Python314\python.exe -B -m pytest -q -p no:cacheprovider --basetemp=.pytest-wave-d1-p1-full --junitxml="$raw\full.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 P1 full suite failed' }
```

The Wave-0 deterministic scrubber records each raw XML hash, exact transform,
testcase-ID digest, and skip allowlist in the public evidence. No CUDA-marked test
result from the CPU interpreter is eligible CUDA evidence.

- [ ] **Step 4: Reproduce the exact CPU before/after profile at `P1`**

Use the same frozen D0 budget, input catalog, repetitions, interpreter,
environment record, and launcher configuration. The before record is the
validated exact-E0 D0 profile; the after record is produced at P1:

```powershell
$ErrorActionPreference = 'Stop'
$d0Bundle = ".verification\upstream-wave-d0"
C:\Python314\python.exe -B tools\build_wave_d_evidence.py validate-upstream --bundle-dir $d0Bundle
if ($LASTEXITCODE -ne 0) { throw 'D0 upstream dependency drifted before P1 profile' }
$d0Index = "$d0Bundle\closure\index.json"
$d0IndexPayload = Get-Content -Raw -LiteralPath $d0Index | ConvertFrom-Json
$e0 = [string]$d0IndexPayload.tested_git_head
$p1 = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve P1 for profile' }
$p1Short = $p1.Substring(0, 12)
$raw = ".verification\raw\wave-d1\$p1Short\candidate"
$public = "docs\verification\evidence\wave-d1\$p1Short"
if (Test-Path -LiteralPath $public) { throw 'P1 candidate output already exists' }
$env:MULTIAGENTELBO_PROFILE_OUTPUT = "$raw\profile-after"
$env:MULTIAGENTELBO_PROFILE_BASELINE = (Resolve-Path "$d0Bundle\closure\profile").Path
C:\Python314\python.exe -B tools\run_remediation_performance_profile.py
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 P1 profile failed' }
Remove-Item Env:MULTIAGENTELBO_PROFILE_OUTPUT
Remove-Item Env:MULTIAGENTELBO_PROFILE_BASELINE
C:\Python314\python.exe -B tools\build_wave_d_evidence.py build --program d1 --stage candidate --tested-head $p1 --implementation-parent $p1 --d0-tested-head $e0 --d0-bundle-dir $d0Bundle --raw-dir $raw --output-dir $public
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 P1 evidence build failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py validate "$public\index.json" --cwd .
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 P1 base index validation failed' }
C:\Python314\python.exe -B tools\build_wave_d_evidence.py validate-domain --bundle-dir $public
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 P1 domain validation failed' }
```

Require identical canonical scientific JSON and per-array hashes. Do not compare
NPZ ZIP container bytes. The CPU improvement claim is eligible only when the
frozen D0 rule fired and the same-machine after record meets the preregistered
improvement rule.

The two independently produced profile directories are provenance controls, not
the CPU performance comparator. Run the closed paired comparator at both P1 and
E1 with the validated E0 before profile as immutable input. It first records an
unbiased initial order, then exactly 15 same-session interleaved CPU pipeline
pairs in alternating AB/BA order; A runs exact E0 and B runs the authorized P1
or E1 cache path. It records every raw wall duration, complete phase spans,
semantic JSON/per-array hashes, load/thermal sample, binding digest, and rejected
pair. It emits `profile/cpu/raw-comparison.json`,
`profile/cpu/load-thermal-metadata.json`, `profile/cpu/semantic-hashes.json`, and
`profile/cpu/comparison-summary.json`. Any identity/hash mismatch, retry,
rejection, missing metadata, nonalternating order, or fewer than fifteen pairs
makes the D1 CPU outcome `INCONCLUSIVE`; no median comparison of serial profiles
may replace the paired AB/BA record.

```powershell
& C:\Python314\python.exe -B tools\run_wave_d_d1_cpu_comparator.py --before-profile $d0Bundle\closure\profile --after-root $raw\cpu-comparator --tested-head $p1 --pairs 15
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 P1 CPU paired comparator failed' }
```

- [ ] **Step 5: If CUDA D1 ran, obtain separate authorization for its bounded before/after harness**

P1 CPU rehearsal is ineligible for CUDA comparison evidence. Task 7 changes the
execution path, so the E0 gate and any earlier sentinel are stale. The sole
Wave-D v3/v4 comparator is the exact-E1 D1-COMPARATOR gate/run command in the
normative authorization block: it follows the E1 evidence-only child, binds the
fresh E1 gate, and has 2 warmups plus exactly 10 outer pairs. No P1 CUDA gate,
authorization, comparator run, or comparator artifact may be created.
Preserve old-v3 and new-v4 environment/config/system identities and canonical
scientific suboutputs. This is a performance harness, not a primary/H analysis;
all harness job IDs are analysis-ineligible. The 40-job confirmatory sweep is
excluded from and forbidden throughout Wave D; separate authorization does not
broaden this plan.

If the user authorizes only a fresh sentinel, record only sentinel protocol/parity
evidence; the CUDA performance-improvement claim remains `INCONCLUSIVE`. If the
user authorizes neither the bounded comparator nor the sentinel, CPU fault and
semantic tests may close only CPU/controller contracts and all CUDA operational
and performance claims remain `INCONCLUSIVE`.

- [ ] **Step 6: Commit the sanitized candidate evidence as direct child `E1`**

```powershell
$ErrorActionPreference = 'Stop'
$p1 = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve P1 before evidence commit' }
$p1Short = $p1.Substring(0, 12)
$public = "docs\verification\evidence\wave-d1\$p1Short"
if (-not (Test-Path -LiteralPath "$public\index.json")) { throw 'P1 candidate index absent' }
git add -- $public
if ($LASTEXITCODE -ne 0) { throw 'cannot stage P1 candidate evidence' }
git diff --cached --name-only
if ($LASTEXITCODE -ne 0) { throw 'cannot inspect staged P1 candidate evidence' }
$staged = @(git diff --cached --name-only)
if ($staged.Count -eq 0 -or @($staged | Where-Object { $_ -notlike "docs/verification/evidence/wave-d1/$p1Short/*" }).Count -ne 0) {
    throw 'P1 candidate staged set is not exactly its SHA directory'
}
git commit -m "test: record wave D1 candidate evidence"
if ($LASTEXITCODE -ne 0) { throw 'P1 candidate evidence commit failed' }
$e1 = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve E1' }
$e1Short = $e1.Substring(0, 12)
if ((git rev-parse HEAD^).Trim() -ne $p1) { throw 'E1 is not the direct child of P1' }
$bad = git diff --name-only $p1..$e1 | Where-Object { $_ -notlike "docs/verification/evidence/wave-d1/$p1Short/*" }
if ($LASTEXITCODE -ne 0) { throw 'cannot inspect P1..E1' }
if ($bad) { throw "non-evidence path in P1..E1: $bad" }
```

- [ ] **Step 7: Rerun all eligible checks at exact `E1`**

```powershell
$ErrorActionPreference = 'Stop'
$e1 = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve E1 for closure' }
$p1 = (git rev-parse HEAD^).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve P1 parent for closure' }
$e1Short = $e1.Substring(0, 12)
$closure = "verification-evidence\wave-d1\$e1Short"
$closureRaw = ".verification\raw\wave-d1\$e1Short\closure"
$d0Bundle = ".verification\upstream-wave-d0"
if (git status --porcelain=v1) { throw 'E1 is not clean before closure staging' }
if ($LASTEXITCODE -ne 0) { throw 'cannot inspect E1 status' }
C:\Python314\python.exe -B tools\build_wave_d_evidence.py validate-upstream --bundle-dir $d0Bundle
if ($LASTEXITCODE -ne 0) { throw 'D0 upstream dependency drifted before E1 closure' }
if (Test-Path -LiteralPath $closureRaw) { throw 'E1 closure raw directory exists' }
if (Test-Path -LiteralPath $closure) { throw 'E1 closure output exists' }
$closureRawParent = Split-Path -Parent $closureRaw
if (-not (Test-Path -LiteralPath $closureRawParent)) {
  New-Item -ItemType Directory -Path $closureRawParent | Out-Null
}
New-Item -ItemType Directory -Path $closureRaw | Out-Null
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
Remove-Item Env:MULTIAGENTELBO_PROFILE_OUTPUT -ErrorAction SilentlyContinue
Remove-Item Env:MULTIAGENTELBO_PROFILE_BASELINE -ErrorAction SilentlyContinue
Remove-Item Env:MULTIAGENTELBO_WORKER_TIMING_V1 -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$closureRaw\targeted.command.json" --junit "$closureRaw\targeted.raw.xml" -- C:\Python314\python.exe -B -m pytest tests\test_performance.py tests\test_performance_launcher.py tests\test_counterexamples.py tests\test_counterexample_experiment.py tests\test_cuda_backend.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py -q -p no:cacheprovider --basetemp=.pytest-wave-d1-e1-targeted --junitxml="$closureRaw\targeted.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 E1 targeted suite failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$closureRaw\subsystem.command.json" --junit "$closureRaw\subsystem.raw.xml" -- C:\Python314\python.exe -B -m pytest tests\test_performance.py tests\test_performance_launcher.py tests\test_counterexamples.py tests\test_counterexample_experiment.py tests\test_cuda_backend.py tests\test_gaussian_fixed_ray.py tests\test_gaussian_fixed_ray_experiment.py tests\test_gaussian_confirmatory_experiment.py tests\test_launchers.py tests\test_config.py tests\test_runtime.py tests\test_artifacts.py -q -p no:cacheprovider --basetemp=.pytest-wave-d1-e1-subsystem --junitxml="$closureRaw\subsystem.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 E1 subsystem suite failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$closureRaw\full.command.json" --junit "$closureRaw\full.raw.xml" -- C:\Python314\python.exe -B -m pytest -q -p no:cacheprovider --basetemp=.pytest-wave-d1-e1-full --junitxml="$closureRaw\full.raw.xml"
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 E1 full suite failed' }
$env:MULTIAGENTELBO_PROFILE_OUTPUT = "$closureRaw\profile-after"
$env:MULTIAGENTELBO_PROFILE_BASELINE = (Resolve-Path "$d0Bundle\closure\profile").Path
C:\Python314\python.exe -B tools\run_remediation_performance_profile.py
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 E1 profile failed' }
Remove-Item Env:MULTIAGENTELBO_PROFILE_OUTPUT
Remove-Item Env:MULTIAGENTELBO_PROFILE_BASELINE
```

Any GPU evidence used for a current E1 claim must be produced only under its
fresh exact-E1 scope gate and exact acceptance; no P1 CUDA authorization or
evidence exists to become stale after the evidence commit.

- [ ] **Step 8: Create all current reviews before freezing the closure index**

Create code, performance-method, experiment/provenance, skeptic, and adjudicator
records under `$closureRaw\reviews\`; the builder privacy-validates and copies
them into the indexed closure. Each names E1, P1, the validated D0 decision,
all current JUnit/profile hashes, verdict, finding dispositions, and falsification
conditions. Review agreement is never substituted for JUnit or timing evidence.

The preceding D1 review step is superseded by this exact E1/P1 sequence. First
emit the E1 `outcomes/frozen-table.json` only from validated raw measurements and
authorizations. Then compute the detached review context; after the digest,
obtain only the complete selected tier of raw reviews and all nine raw
adjudicators. No closure index, public review/adjudicator, ledger, or `$closure`
directory may exist before validation.

```powershell
& C:\Python314\python.exe -B tools\build_wave_d_evidence.py freeze-outcomes --program d1 --tested-head $e1 --implementation-parent $p1 --d0-bundle-dir $d0Bundle --raw-dir $closureRaw
if ($LASTEXITCODE -ne 0) { throw 'D1 frozen outcomes failed' }
$reviewContextSha = (& C:\Python314\python.exe -B tools\build_wave_d_evidence.py review-context-sha --program d1 --tested-head $e1 --implementation-parent $p1 --d0-bundle-dir $d0Bundle --raw-dir $closureRaw).Trim()
if ($LASTEXITCODE -ne 0 -or $reviewContextSha -notmatch '^[0-9a-f]{64}$') { throw 'D1 review context failed' }
if (Test-Path -LiteralPath $closure) { throw 'D1 context created closure bytes' }
$reviewTarget = [int]((& C:\Python314\python.exe -B tools\build_wave_d_evidence.py review-target --program d1 --tested-head $e1 --implementation-parent $p1 --d0-bundle-dir $d0Bundle --raw-dir $closureRaw).Trim())
if ($LASTEXITCODE -ne 0 -or $reviewTarget -notin @(2,4,8)) { throw 'D1 review target invalid' }
# Write only selected raw review files and all nine raw adjudicators under $closureRaw\reviews.
& C:\Python314\python.exe -B tools\build_wave_d_evidence.py validate-reviews --program d1 --tested-head $e1 --implementation-parent $p1 --d0-bundle-dir $d0Bundle --raw-dir $closureRaw
if ($LASTEXITCODE -ne 0) { throw 'D1 raw reviews/adjudicators invalid' }
if (Test-Path -LiteralPath $closure) { throw 'D1 review validation created closure bytes' }
```

The build in Step 9 copies only these validated raw bytes through the total
privacy transform. It cannot invent, regenerate, rename, or upgrade a review or
adjudicator; it rejects an omitted/extra tier member, outcome byte, or private
token before publishing the one absent closure directory.

- [ ] **Step 9: Build the closure index, populate the D1 ledger, and validate**

```powershell
$ErrorActionPreference = 'Stop'
$e1 = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve E1 for final closure' }
$p1 = (git rev-parse HEAD^).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve P1 for final closure' }
$e1Short = $e1.Substring(0, 12)
$closureRaw = ".verification\raw\wave-d1\$e1Short\closure"
$closure = "verification-evidence\wave-d1\$e1Short"
$d0Bundle = ".verification\upstream-wave-d0"
C:\Python314\python.exe -B tools\build_wave_d_evidence.py validate-upstream --bundle-dir $d0Bundle
if ($LASTEXITCODE -ne 0) { throw 'D0 upstream dependency drifted before D1 build' }
$d0IndexPayload = Get-Content -Raw -LiteralPath "$d0Bundle\closure\index.json" | ConvertFrom-Json
$e0 = [string]$d0IndexPayload.tested_git_head
if (-not (Test-Path -LiteralPath "$closureRaw\reviews")) { throw 'D1 current reviews absent' }
if (Test-Path -LiteralPath $closure) { throw 'D1 closure output already exists' }
C:\Python314\python.exe -B tools\build_wave_d_evidence.py build --program d1 --stage closure --tested-head $e1 --implementation-parent $p1 --d0-tested-head $e0 --d0-bundle-dir $d0Bundle --raw-dir $closureRaw --output-dir $closure
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 closure build failed' }
C:\Python314\python.exe -B tools\remediation_evidence.py validate "$closure\index.json" --cwd .
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 closure base index failed' }
C:\Python314\python.exe -B tools\build_wave_d_evidence.py validate-domain --bundle-dir $closure
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 closure domain/worktree validation failed' }
$ledger = '.verification\wave-d1\final-ledger.json'
$active = '.verification\active.json'
if (Test-Path -LiteralPath $active) { throw 'preexisting verification gate is active' }
if (Test-Path -LiteralPath $ledger) { throw 'preexisting D1 ledger exists' }
& 'C:\Python314\python.exe' -B tools\remediation_evidence.py run-verification-gate --snapshot docs/verification/remediation/verification-contract-v1.json --root 'C:\Users\chris and christine\.codex\skills\verification' -- start --cwd . --mode closure --ledger $ledger
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 gate start failed' }
& 'C:\Python314\python.exe' -B tools\remediation_evidence.py run-verification-gate --snapshot docs/verification/remediation/verification-contract-v1.json --root 'C:\Users\chris and christine\.codex\skills\verification' -- validate --cwd . $ledger
if ($LASTEXITCODE -eq 0) { throw 'empty Wave D1 template unexpectedly validated' }
C:\Python314\python.exe -B tools\build_wave_d_evidence.py populate-ledger --program d1 --ledger $ledger --closure-index "$closure\index.json"
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 ledger population failed' }
```

The populated ledger states, for each implemented and currently reproduced
subsystem, that the proposition “the AUD defect still occurs at
E1” is `REFUTED`, while its positive regression contract is
`EVIDENCE_VERIFIED`. Untriggered, unauthorized, or inadequately measured claims
remain `INCONCLUSIVE` with one explicit obligation. A current sentinel closes
only its sentinel-specific claim. Then run:

The preceding legacy shorthand is superseded in full by the binding frozen D1
outcome table; the ledger is its byte-for-byte projection and may not infer a
defect state or success state from implementation presence alone.

```powershell
$ErrorActionPreference = 'Stop'
$ledger = '.verification\wave-d1\final-ledger.json'
& 'C:\Python314\python.exe' -B tools\remediation_evidence.py run-verification-gate --snapshot docs/verification/remediation/verification-contract-v1.json --root 'C:\Users\chris and christine\.codex\skills\verification' -- validate --cwd . $ledger
if ($LASTEXITCODE -ne 0) { throw 'Wave D1 ledger validation failed' }
```

- [ ] **Step 10: Push and fast-forward only the exact verified terminal SHA**

If D1 did not run, the terminal SHA is E0; otherwise it is E1. Fetch the remote,
show `origin/main`, require the terminal SHA to be a descendant of it, rehearse
integration in a clean isolated worktree, and push a fast-forward without a merge
commit. Before advancing the user's live checkout, inventory the protected WIP,
prove incoming paths do not overlap it, then fast-forward the ref/index while
preserving those bytes. Any merge commit, rebased evidence child, or tracked byte
change requires new exact-terminal closure evidence and ledger validation.
