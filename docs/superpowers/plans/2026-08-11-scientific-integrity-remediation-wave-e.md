# Wave E Connectedness Claim Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct AUD-20 in the Research manuscript so graph connectedness licenses
only conditional componentwise decoupling, never an unproved unique limiting fixed
point, while preserving every exact ELBO/coarse-graining equation and every
`OPEN`/`INCONCLUSIVE` RG boundary.

**Architecture:** Work in a new Research worktree whose parent is either fetched
`origin/main` containing `c9f237d2` or the explicitly declared unpublished
`c9f237d2` parent. Add two exact symbolic counterexample oracles, one durable
source-language regression, and a Research-local, Wave-0-conforming evidence
adapter with its own failure-injection tests; replace six prose paragraphs in
`08a_coarse_graining.tex`, then prove equation-byte identity, compile the root
manuscript, and close the high finding through a separate Research-revision
verification ledger. Publish the
fixed-ray ingest first when it is still absent from remote `main`, fast-forward
only clean `main`, and leave the dirty live Research review checkout byte-identical.

**Tech Stack:** Git worktrees, PowerShell, Python 3.14 CPU, pytest/JUnit, SymPy,
LuaLaTeX, BibTeX through `latexmk`, the installed verification gate, and LaTeX.
No new dependency is permitted.

## Global Constraints

- Governing design revision:
  `c43a7c50675cf63b60f7b6cbea9664b638cd4c4e`.
- Governing audit: MultiAgentELBO
  `docs/audits/2026-08-11-post-fixed-ray-deep-audit.md`, AUD-20.
- No Research implementation step may start until fetched MultiAgentELBO
  `origin/main` contains the finalized Wave 0 plan and this corrected Wave E plan.
  Task 1 freezes one concrete planning commit and records the Git blob ID, byte
  length, and SHA-256 of both plans, the governing design, and the governing audit.
  Every candidate and closure source-input inventory revalidates those four exact
  records; a moved planning ref does not rewrite the frozen binding.
- Research context revision:
  `c9f237d2ca54c274ba5760012e62823a69d203a3`.
- Pinned pre-fix manuscript SHA-256:
  `E08DEADCE851B890B260787379956C794E3AA8764F124146043164C7F3EABA38`.
- Modify Research implementation source only at
  `manuscripts/magent_elbo_whitepaper/08a_coarse_graining.tex` and
  `manuscripts/magent_elbo_whitepaper/verification/test_elbo_oracles.py`; create
  `manuscripts/magent_elbo_whitepaper/verification/wave_e_evidence.py` and
  `manuscripts/magent_elbo_whitepaper/verification/test_wave_e_evidence.py` in
  the same implementation commit. The evidence builder is necessary because the
  repository has no checked-in producer that can express privacy provenance,
  recorder-derived TeX inputs, or a closed closure-file inventory.
- Change only the status-bearing prose currently at lines 174, 176, 178, 180, 182,
  and 194.
  Every `equation` environment, label, reference, exact ELBO/gap/sufficiency
  statement, and aggregation identity remains byte-identical to `c9f237d2` after
  line-ending normalization.
- Do not edit `wiki/`, `sources/`, `index.md`, `log.md`, bibliography files, any
  other manuscript, or the MultiAgentELBO repository during implementation.
- Preserve the conclusions that no rescaling, attraction theorem, RG flow,
  universality result, unique quotient fixed object, common basin, convergence
  theorem, or effective-law non-observability theorem has been established.
- The two mathematical controls are exact symbolic/algebraic tests. Floating-point
  sampling is not eligible mathematics evidence.
- Use `C:\Python314\python.exe` for every Python/pytest command. The lane is CPU
  only; do not query or run CUDA. Every recorded command requires
  `CUDA_VISIBLE_DEVICES=-1` and `PYTHONHASHSEED=0`; records the exact string
  value or JSON null for `CUDA_VISIBLE_DEVICES`,
  `MULTIAGENTELBO_RUN_CUDA_TESTS`, `VFE3_TEST_DEVICE`,
  `CUBLAS_WORKSPACE_CONFIG`, `PYTHONHASHSEED`, and `PYTHONPATH`; and rejects the
  three CUDA opt-in/device variables when present.
- Every TeX command additionally records exact string or JSON-null values for
  `WINDIR`, `SystemRoot`, `TEXINPUTS`, `BIBINPUTS`, `BSTINPUTS`, `TEXMF`,
  `TEXMFHOME`, `TEXMFLOCAL`, `TEXMFCNF`, `TEXMFVAR`, `TEXMFCONFIG`,
  `TEXMFOUTPUT`, `MIKTEX_USERCONFIG`, `MIKTEX_USERDATA`, `MIKTEX_USERINSTALL`,
  `MIKTEX_COMMONCONFIG`, `MIKTEX_COMMONDATA`, and `MIKTEX_COMMONINSTALL`.
  Baseline, candidate, and closure builds use `latexmk -norc`; no unbound
  `latexmkrc` is consulted. Recorder-discovered TeX configuration remains bound.
- Use `apply_patch` for tracked source/test/prose changes. Generated JUnit and
  machine-readable evidence may be written by their producing commands.
- The existing Research oracle file collects exactly 17 tests at the pinned base.
  The two counterexample oracles plus the source contract bring the expected total
  to 20.
- The implementation commit contains only the four exact implementation paths
  above. A direct evidence-only child contains durable candidate evidence. Exact-child
  closure evidence and the external ledger remain local, nonignored, and bound by
  the verification gate.
- `remediation-evidence-v1` is the authoritative outer/base index and
  `remediation-command-record-v1` is the authoritative JUnit runner record. Wave E
  adds a closed `wave-e-domain-inventory-v1` file for mathematical, TeX, privacy,
  source-diff, and review evidence; the domain inventory references the base index
  and may not replace, rename, or weaken a Wave 0 field or runner check.
- The binding Wave 0 plan byte is exactly SHA-256
  `dbe2263a3b0fe1e9f5db4ff1fca9a19f819cfd32ef38da71d6e5cb5485723ac2`.
  Task 1 rejects any other Wave 0 plan before it writes the planning contract.
- Wave E never embeds its own content hash. An operator/coordinator creates the
  external `wave-e-planning-release-v1` record only after the final Wave E plan
  commit. That record binds fetched planning commit, repository, plan path, Git
  blob, byte size, and SHA-256; Task 1, both evidence stages, and Task 6 revalidate
  it byte-for-byte. Historical plan identity
  `7AD54524FFB3F170FB2848882489DF0F3E94341660F2FFB9A906EECD0C96A5A4`
  describes the superseded pre-correction draft only and is never an acceptance
  literal, because changing this plan necessarily invalidates that old hash and a
  current self-hash inside the file would be circular.
- Gate selection is likewise owned by Wave 0. Wave E consumes the frozen
  `verification-contract-v1` and byte-equivalent
  `resolve-verification-gate` resolver, validates the explicit active
  `C:\Users\chris and christine\.codex\skills\verification` tree, and binds the
  snapshot, resolver, SKILL, contract, five criteria, ledger schema, and gate
  identities as dependency/config inputs. It never defines an independent verifier
  contract or falls back to `.claude`.
- Every JUnit XML, pytest console stream, TeX build product, claim-language scan,
  equation comparison, source-diff record, and raw review first lands under the exact out-of-repository
  `C:\tmp\magent-wave-e-*-raw` staging roots. Before any tracked candidate byte or
  nonignored closure byte is created, the builder computes every raw size/SHA-256,
  applies the deterministic `wave-e-path-redaction-v1` privacy transform in memory,
  and validates the complete would-be public bundle.
- Root-TeX input binding comes from the fresh build's `-recorder` `.fls` file, not
  a hand-maintained list. Every consumed repository include and every external
  class, style, font, map, encoding, configuration, or other regular-file `INPUT`
  outside the build directory is normalized, sized, and SHA-256 bound. Because
  BibTeX does not emit `.fls`, bibliography and BST inputs are additionally
  recovered from the fresh `.aux`/`.blg` pair and resolved with the same TeX path
  resolver used by the build. The Python oracle/test/tool inputs and the Python,
  `latexmk`, LuaLaTeX, BibTeX, and `kpsewhich` executables are separately bound by
  resolved path, complete version output, size, and SHA-256. Generated JUnit,
  scan, equation, build, baseline-warning, privacy, review, and index bytes are
  evidence outputs and are forbidden from `dependency_inputs`.
- AUD-20 remains severity `high`. Closure requires escalation target 4 or 8,
  `escalation_triggers` containing `high_severity`, four independent views at
  minimum, one structured skeptic, and one structured adjudicator. Agent
  agreement is not evidence.
- Missing proof, stale bytes, a changed equation, unresolved review disagreement,
  a TeX failure, an unexplained skip, or an invalid ledger yields `INCONCLUSIVE`
  and blocks publication.
- Do not reuse the fixed-ray ingest worktree or mutate the live checkout at
  `C:\Users\chris and christine\Desktop\Research`.
- Do not push any Wave E ref until the validated ledger passes and, if required,
  remote `main` first reaches `c9f237d2`.
- Wave E uses only the Research revision and
  `.verification/wave-e/final-ledger.json`. It never enters, updates, or supplies
  evidence to the MultiAgentELBO aggregate ledger.

## Planned File Structure

Research implementation files:

- Modify:
  `manuscripts/magent_elbo_whitepaper/verification/test_elbo_oracles.py`
  — two exact counterexamples plus the source-language regression.
- Modify:
  `manuscripts/magent_elbo_whitepaper/08a_coarse_graining.tex`
  — six calibrated prose paragraphs only.

- Create:
  `manuscripts/magent_elbo_whitepaper/verification/wave_e_evidence.py`
  -- privacy-first publication, exhaustive input binding, bundle/index
  validation, review validation, and explicit ledger population.
- Create:
  `manuscripts/magent_elbo_whitepaper/verification/test_wave_e_evidence.py`
  -- fourteen conformance and failure-injection tests for the evidence adapter.

Candidate evidence, named after the implementation commit at execution time:

- Create under `docs/verification/evidence/wave-e/$implShort/` only through the
  builder: `elbo-oracles.xml`, `evidence-tool-tests.xml`,
  `aud20-derivation.md`, `baseline-warning-provenance.json`,
  `claim-language.json`,
  `equation-byte-comparison.json`, `tex-build-summary.json`, `tex-inputs.json`,
  `environment.json`, `command-records.json`, `privacy-manifest.json`,
  `source-diff.json`, the exact Wave 0 base `remediation-index.json`, and the final
  `evidence-index.json` domain inventory. The candidate set is exactly 14 files.

Exact-child closure evidence, named after the evidence-only child at execution
time:

- Create locally under `verification-evidence/wave-e/$evidenceShort/` only
  through the builder: the twelve common public payloads above,
  `pre-review-manifest.json`, the exact Wave 0 base `remediation-index.json`, the
  final `closure-index.json` domain inventory, and exactly four primary views, one
  skeptic, and one adjudicator under `views/`. If and only if a primary-view
  criterion disagrees, add the four frozen escalation views and set escalation
  target 8. The closure set is exactly 21 files or 25 under escalation.
- Create locally at `.verification/wave-e/final-ledger.json` through the installed
  verification control plane.

Temporary read-only safety/build records:

- `C:\tmp\magent-wave-e-live-wip-before.json`
- `C:\tmp\magent-wave-e-live-wip-after.json`
- `C:\tmp\magent-wave-e-planning-contract.json`
- `C:\tmp\magent-wave-e-baseline-c9f237d2\`
- `C:\tmp\magent-wave-e-candidate-$implShort\`
- `C:\tmp\magent-wave-e-closure-$evidenceShort\`
- `C:\tmp\magent-wave-e-candidate-$implShort-raw\`
- `C:\tmp\magent-wave-e-closure-$evidenceShort-raw\`

---

## Literal AUD-20 Derivation Contract

`scan_raw` writes the following UTF-8 text, with LF line endings and one final
newline, byte-for-byte as `aud20-derivation.md`. The evidence-builder test imports
the same literal constant and compares the emitted bytes exactly, while the oracle
tests independently check its load-bearing algebra; a paraphrase is not eligible
derivation evidence.

```text
# AUD-20 connectedness, quotient, and relative-invariant derivation

## 1. Connected support does not imply a unique attractor

On the admitted interval [0,1], let F(x)=3x^2-2x^3. Then

F(x)-x=x(1-x)(2x-1),
F'(x)=6x(1-x).

The fixed-point equation F(x)=x therefore has exactly x=0, x=1/2, and x=1.
Their derivatives are 0, 3/2, and 0. For 0<x<1/2, 0<=F(x)<x, so the iterates
decrease monotonically to a fixed point below 1/2 and hence to 0. For
1/2<x<1, x<F(x)<=1, so the iterates increase monotonically to a fixed point
above 1/2 and hence to 1. Thus 0 and 1 are attracting fixed points with distinct
basins separated by the repelling fixed point 1/2. One connected component can
therefore support multiple fixed objects and basin-dependent limits.

## 2. Component decomposition gives decoupling only under a local normalization

Let the interaction graph have connected components C_alpha and let the admitted
model space decompose as X=direct_sum_alpha X_alpha. If the unnormalized step
respects components, S_l=direct_sum_alpha S_{l,alpha}, and each positive
normalizer zeta_{l,alpha} is either fixed exogenously or depends only on the state
x_alpha of its own component, then

R_l(x)_alpha=zeta_{l,alpha}(x_alpha)^(-1) S_{l,alpha}(x_alpha),
R_l=direct_sum_alpha R_{l,alpha}.

This proves only componentwise evolution. If a normalizer for one block depends
on another block, the normalized map is not a direct sum even when S_l is block
diagonal. Neither block diagonal structure nor graph connectedness supplies
existence, uniqueness, attraction, convergence, or common-basin coverage inside
one component.

## 3. A quotient fixed-object claim requires descent of the map

Let H_alpha be the residual global frame group on component C_alpha. A component
map R_{l,alpha} defines a quotient map by

bar(R)_{l,alpha}([x])=[R_{l,alpha}(x)]

only if the right-hand side is independent of the representative x. Equivariance,
R_{l,alpha}(h action x)=h action R_{l,alpha}(x), is a sufficient condition; the
weaker necessary statement is that points in one H_alpha-orbit map into one
H_alpha-orbit. A fixed exogenous common scalar preserves this property, as do
gauge-invariant block scalars zeta_{l,alpha} whose alpha-th value depends only on
x_alpha, when S_{l,alpha} has it. Without this descent check, existence or
uniqueness on the residual-frame quotient is not a well-defined conclusion.

## 4. Rank of M alone does not classify the pair (A,M)

For K=1 with a>0 and m>0, the residual GL(1) frame h acts simultaneously by

(a,m) -> (h^2 a,h^2 m).

Therefore a/m is invariant. A common positive normalization also preserves it:
(a/zeta)/(m/zeta)=a/m. If two pairs (a,m) and (a',m') were in the same residual
orbit, then a'=h^2 a and m'=h^2 m, which implies a'/m'=a/m. Hence pairs with
different ratios are gauge inequivalent even though every positive scalar M has
rank one and lies in the single positive congruence class. Sylvester inertia or
rank classifies M alone; it does not exhaust the relative invariants of (A,M), the
fixed-object classes, or their possible continuous moduli.

## 5. Exact conclusions and falsifiers

The established conclusion is conditional componentwise decoupling under a
block-preserving step and either a fixed exogenous common scalar or block-indexed
scalars whose alpha-th value depends only on x_alpha. Graph
connectivity does not exhaust fixed-object variety. It proves none of existence,
quotient uniqueness, attraction, convergence, common-basin coverage, or
non-observability of alternative effective laws. A quotient statement additionally
requires a well-defined descended map, and classification of M alone cannot be
substituted for classification of the full model pair.

This derivation is falsified by any of the following: an algebraic error in the
factorization, derivatives, or monotone-basin argument for F; a residual GL(1)
frame that changes a/m; a simultaneous congruence relating two positive scalar
pairs with different a/m; or a proof that the stated normalized map remains a
direct sum while one output block genuinely depends on another block. Proving
equivariance and quotient descent for a specified map would discharge the
well-definedness prerequisite, but would not by itself prove a unique fixed orbit
or global attraction.
```

---

### Task 1: Gate the Research parent and create an isolated worktree

**Files:**

- Read only: `manuscripts/magent_elbo_whitepaper/08a_coarse_graining.tex`
- Read only: `manuscripts/magent_elbo_whitepaper/verification/test_elbo_oracles.py`
- Read only at one frozen MultiAgentELBO planning commit: Wave 0 plan, corrected
  Wave E plan, governing design, governing audit, Wave 0 verification-contract
  snapshot, and Wave 0 resolver implementation.
- Read only outside the repository:
  `C:\tmp\magent-wave-e-planning-release.json`, created and approved by the
  operator/coordinator after the final Wave E plan commit.
- Create outside the repository: `C:\tmp\magent-wave-e-live-wip-before.json`
- Create outside the repository: `C:\tmp\magent-wave-e-planning-contract.json`
- Create outside the repository: `C:\tmp\magent-wave-e-baseline-c9f237d2\`

**Interfaces:**

- Consumes: fetched MultiAgentELBO `origin/main`, fetched Research `origin/main`,
  and context commit `c9f237d2`.
- Produces: clean branch
  `codex/magent-aud20-connectedness-remediation-20260811` in worktree
  `C:\Users\chris and christine\Documents\ChatGPT\MultiAgentELBO\.superpowers\worktrees\Research-magent-aud20-remediation-20260811`.
- Produces: a byte-level fingerprint of the protected live Research WIP and a
  baseline TeX warning inventory with complete provenance.

- [ ] **Step 1: Load the worktree skill and declare exact paths**

The executor first loads `superpowers:using-git-worktrees`, then runs this block
from PowerShell:

```powershell
$researchRepo = 'C:\Users\chris and christine\Desktop\Research'
$liveRepo = 'C:\Users\chris and christine\Desktop\Research'
$planningRepo = 'C:\Users\chris and christine\Documents\ChatGPT\MultiAgentELBO'
$planningContract = 'C:\tmp\magent-wave-e-planning-contract.json'
$planningRelease = 'C:\tmp\magent-wave-e-planning-release.json'
$verificationResolution = 'C:\tmp\magent-wave-e-verification-resolution.json'
$verificationRoot = 'C:\Users\chris and christine\.codex\skills\verification'
$waveWorktree = 'C:\Users\chris and christine\Documents\ChatGPT\MultiAgentELBO\.superpowers\worktrees\Research-magent-aud20-remediation-20260811'
$waveBranch = 'codex/magent-aud20-connectedness-remediation-20260811'
$contextCommit = 'c9f237d2ca54c274ba5760012e62823a69d203a3'
$targetRel = 'manuscripts/magent_elbo_whitepaper/08a_coarse_graining.tex'
$expectedTargetHash = 'E08DEADCE851B890B260787379956C794E3AA8764F124146043164C7F3EABA38'
$wave0PlanPath = 'docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md'
$waveEPlanPath = 'docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-e.md'
$expectedWave0PlanSha256 = 'dbe2263a3b0fe1e9f5db4ff1fca9a19f819cfd32ef38da71d6e5cb5485723ac2'

if (Test-Path -LiteralPath $waveWorktree) {
    throw "Wave E worktree already exists: $waveWorktree"
}
& git -C $researchRepo show-ref --verify --quiet "refs/heads/$waveBranch"
if ($LASTEXITCODE -eq 0) {
    throw "Wave E branch already exists: $waveBranch"
}
if ($LASTEXITCODE -ne 1) { throw 'Wave E branch lookup failed' }
if (-not (Test-Path -LiteralPath $planningRelease -PathType Leaf)) {
    throw 'Approved post-commit Wave E planning-release record is missing'
}
```

Expected: neither path nor branch exists. Do not delete or repurpose an existing
path/ref; stop for ownership review instead.

- [ ] **Step 2: Freeze the committed Wave 0/Wave E planning contract before implementation**

Fetch without touching the live MultiAgentELBO checkout, create one detached
read-only snapshot worktree under `C:\tmp`, and record exact Git and byte identities:

```powershell
$planningPaths = @(
    $wave0PlanPath,
    $waveEPlanPath,
    'docs/superpowers/specs/2026-08-11-scientific-integrity-remediation-program-design.md',
    'docs/audits/2026-08-11-post-fixed-ray-deep-audit.md'
)
$verificationContractPaths = @(
    'docs/verification/remediation/verification-contract-v1.json',
    'tools/remediation_evidence.py'
)
$allPlanningPaths = @($planningPaths + $verificationContractPaths)
& git -C $planningRepo fetch origin
if ($LASTEXITCODE -ne 0) { throw 'MultiAgentELBO planning fetch failed' }
$planningCommit = (& git -C $planningRepo rev-parse origin/main).Trim()
if ($planningCommit -notmatch '^[0-9a-f]{40}$') {
    throw 'Planning commit is not a concrete full SHA'
}
$planningShort = $planningCommit.Substring(0,12)
$planningSnapshot = "C:\tmp\magent-wave-e-planning-snapshot-$planningShort"
if (Test-Path -LiteralPath $planningSnapshot) {
    throw "Planning snapshot already exists: $planningSnapshot"
}
& git -C $planningRepo worktree add --detach $planningSnapshot $planningCommit
if ($LASTEXITCODE -ne 0) { throw 'Planning snapshot worktree creation failed' }

$planningSources = foreach ($path in $allPlanningPaths) {
    $absolute = Join-Path $planningSnapshot $path
    if (-not (Test-Path -LiteralPath $absolute -PathType Leaf)) {
        throw "Frozen planning source is absent: $path"
    }
    $blob = (& git -C $planningRepo rev-parse "$planningCommit`:$path").Trim()
    $snapshotBlob = (& git -C $planningSnapshot hash-object -- $path).Trim()
    if ($blob -cne $snapshotBlob) {
        throw "Frozen planning blob mismatch: $path"
    }
    $item = Get-Item -LiteralPath $absolute
    [ordered]@{
        path = $path
        git_blob = $blob
        size_bytes = [int64]$item.Length
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $absolute).Hash
    }
}

$wave0PlanRecord = $planningSources | Where-Object path -eq $wave0PlanPath
if ($null -eq $wave0PlanRecord -or
    $wave0PlanRecord.sha256.ToLowerInvariant() -cne $expectedWave0PlanSha256) {
    throw 'Binding Wave 0 plan SHA-256 drifted before planning-contract creation'
}

$releasePayload = Get-Content -Raw -LiteralPath $planningRelease | ConvertFrom-Json
$releaseKeys = @($releasePayload.PSObject.Properties.Name | Sort-Object)
if (Compare-Object $releaseKeys @(
    'planning_commit','repository','reviewed_plan','schema_version'
)) {
    throw 'Planning-release root schema drifted'
}
$releasePlanKeys = @(
    $releasePayload.reviewed_plan.PSObject.Properties.Name | Sort-Object
)
if (Compare-Object $releasePlanKeys @(
    'git_blob','path','sha256','size_bytes'
)) {
    throw 'Planning-release reviewed-plan schema drifted'
}
$waveEPlanRecord = $planningSources | Where-Object path -eq $waveEPlanPath
$planningRemote = (& git -C $planningRepo remote get-url origin).Trim()
if ($releasePayload.schema_version -cne 'wave-e-planning-release-v1' -or
    $releasePayload.repository -cne $planningRemote -or
    $releasePayload.planning_commit -cne $planningCommit) {
    throw 'Planning release does not approve this fetched planning revision'
}
foreach ($field in @('path','git_blob','size_bytes','sha256')) {
    if ([string]$releasePayload.reviewed_plan.$field -cne
        [string]$waveEPlanRecord.$field) {
        throw "Planning release reviewed-plan field drifted: $field"
    }
}
$planningReleaseItem = Get-Item -LiteralPath $planningRelease
$planningReleaseBinding = [ordered]@{
    path = '$PLANNING_RELEASE'
    size_bytes = [int64]$planningReleaseItem.Length
    sha256 = (
        Get-FileHash -Algorithm SHA256 -LiteralPath $planningRelease
    ).Hash.ToLowerInvariant()
}

$snapshotPath = Join-Path $planningSnapshot $verificationContractPaths[0]
$resolverPath = Join-Path $planningSnapshot $verificationContractPaths[1]
$resolverOutput = @(
    & 'C:\Python314\python.exe' -B $resolverPath `
        resolve-verification-gate --snapshot $snapshotPath --root $verificationRoot
)
if ($LASTEXITCODE -ne 0 -or $resolverOutput.Count -ne 1) {
    throw 'Frozen Wave 0 verification-gate resolution failed'
}
$resolvedGate = $resolverOutput[0].Trim()
$expectedGate = Join-Path $verificationRoot 'scripts\verification_gate.py'
if ((Resolve-Path -LiteralPath $resolvedGate).Path -cne
    (Resolve-Path -LiteralPath $expectedGate).Path) {
    throw 'Wave 0 resolver did not select the bound active Codex gate'
}
$snapshotPayload = Get-Content -Raw -LiteralPath $snapshotPath | ConvertFrom-Json
$snapshotFiles = @($snapshotPayload.files)
$requiredContractPaths = @(
    'SKILL.md',
    'references/contract.md',
    'references/criteria-code.md',
    'references/criteria-evidence.md',
    'references/criteria-experiment.md',
    'references/criteria-general.md',
    'references/criteria-math.md',
    'schemas/claim-ledger.schema.json',
    'scripts/verification_gate.py'
)
if ($snapshotPayload.schema_version -cne 'verification-contract-v1' -or
    @($requiredContractPaths | Where-Object { $_ -notin @($snapshotFiles.path) }).Count -ne 0 -or
    $snapshotFiles.Count -ne 9) {
    throw 'Wave 0 verification-contract snapshot inventory drifted'
}
if ((Get-Content -Raw -LiteralPath $snapshotPath) -match
    '(?i)(?:[A-Z]:\\|/Users/|/home/|\\\\)') {
    throw 'Wave 0 verification snapshot contains an absolute source root'
}
$resolvedContractFiles = foreach ($record in $snapshotFiles) {
    $absolute = Join-Path $verificationRoot $record.path
    if (-not (Test-Path -LiteralPath $absolute -PathType Leaf)) {
        throw "Resolved verification-contract file is missing: $($record.path)"
    }
    $item = Get-Item -LiteralPath $absolute
    $sha = (Get-FileHash -Algorithm SHA256 -LiteralPath $absolute).Hash.ToLowerInvariant()
    if ([int64]$record.size_bytes -ne [int64]$item.Length -or
        $record.sha256.ToLowerInvariant() -cne $sha) {
        throw "Resolved verification-contract identity drifted: $($record.path)"
    }
    [ordered]@{
        path = ('$VERIFICATION_ROOT/' + $record.path.Replace('\','/'))
        size_bytes = [int64]$item.Length
        sha256 = $sha
    }
}
$verificationBinding = [ordered]@{
    schema_version = 'wave-e-verification-binding-v1'
    root_alias = '$VERIFICATION_ROOT'
    snapshot = [ordered]@{
        path = $verificationContractPaths[0]
        git_blob = ($planningSources | Where-Object path -eq $verificationContractPaths[0]).git_blob
        size_bytes = (Get-Item -LiteralPath $snapshotPath).Length
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $snapshotPath).Hash.ToLowerInvariant()
    }
    resolver = [ordered]@{
        path = $verificationContractPaths[1]
        git_blob = ($planningSources | Where-Object path -eq $verificationContractPaths[1]).git_blob
        size_bytes = (Get-Item -LiteralPath $resolverPath).Length
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $resolverPath).Hash.ToLowerInvariant()
    }
    resolved_gate = '$VERIFICATION_ROOT/scripts/verification_gate.py'
    contract_files = @($resolvedContractFiles)
}
$verificationBinding | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath `
    $verificationResolution -Encoding utf8NoBOM

[ordered]@{
    schema_version = 'wave-e-planning-contract-v1'
    repository = $planningRemote
    planning_commit = $planningCommit
    wave0_plan_sha256 = $expectedWave0PlanSha256
    planning_release_binding = $planningReleaseBinding
    planning_release_record = $releasePayload
    sources = @($planningSources | Where-Object { $_.path -in $planningPaths })
    verification_contract_inputs = @(
        $planningSources | Where-Object { $_.path -in $verificationContractPaths }
    )
    verification_contract = $verificationBinding
} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath `
    $planningContract -Encoding utf8NoBOM

$planningPayload = Get-Content -Raw -LiteralPath $planningContract | ConvertFrom-Json
if ($planningPayload.planning_commit -cne $planningCommit -or
    $planningPayload.wave0_plan_sha256 -cne $expectedWave0PlanSha256 -or
    @($planningPayload.sources).Count -ne 4 -or
    @($planningPayload.verification_contract_inputs).Count -ne 2 -or
    @($planningPayload.verification_contract.contract_files).Count -ne 9) {
    throw 'Frozen planning contract validation failed'
}
"planning_commit=$planningCommit"
"planning_contract_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $planningContract).Hash)"
```

This is the contract-freeze gate. If either corrected plan is absent from fetched
`origin/main`, the Wave 0 plan is not the exact `dbe2263...723ac2` byte, the
post-commit planning-release record does not match the fetched Wave E commit/path/
blob/size/SHA byte-for-byte, any other file/blob/hash differs, or the Wave 0
snapshot/resolver rejects the
active Codex installation, or any SKILL/contract/five-criteria/schema/gate identity
drifts, stop before creating the Research feature worktree. There is no `.claude`
fallback. The snapshots are retained read-only for later candidate and closure
source/dependency revalidation; Wave E does not define an independent verification
contract.

- [ ] **Step 3: Fetch and enforce the unpublished-parent gate**

```powershell
& git -C $researchRepo fetch origin
if ($LASTEXITCODE -ne 0) { throw 'Research fetch failed' }

& git -C $researchRepo cat-file -e "$contextCommit^{commit}"
if ($LASTEXITCODE -ne 0) { throw 'Pinned c9f237d2 commit is unavailable' }

& git -C $researchRepo merge-base --is-ancestor $contextCommit origin/main
if ($LASTEXITCODE -eq 0) {
    $waveParent = (& git -C $researchRepo rev-parse origin/main).Trim()
    $ingestPublicationRequired = $false
} else {
    $waveParent = $contextCommit
    $ingestPublicationRequired = $true
}

"wave_parent=$waveParent"
"ingest_publication_required=$ingestPublicationRequired"
& git -C $researchRepo log -3 --oneline --decorate origin/main
& git -C $researchRepo show --stat --oneline $contextCommit
```

Expected: `$waveParent` is a concrete 40-character commit. If
`$ingestPublicationRequired` is true, Wave E may be implemented locally but its
ref cannot publish until Task 5 first advances remote `main` to `c9f237d2`.

- [ ] **Step 4: Fingerprint every protected live WIP byte**

Run this exact function without switching the live branch:

```powershell
function Write-ResearchWipFingerprint {
    param(
        [Parameter(Mandatory=$true)][string]$RepoPath,
        [Parameter(Mandatory=$true)][string]$OutputPath
    )

    $paths = @(
        & git -C $RepoPath ls-files --modified --deleted
        & git -C $RepoPath diff --cached --name-only
        & git -C $RepoPath ls-files --others --exclude-standard
    ) | Sort-Object -Unique

    $entries = foreach ($relativePath in $paths) {
        $absolutePath = Join-Path $RepoPath $relativePath
        if (Test-Path -LiteralPath $absolutePath -PathType Leaf) {
            $item = Get-Item -LiteralPath $absolutePath -Force
            [ordered]@{
                path = $relativePath.Replace('\', '/')
                exists = $true
                length = [int64]$item.Length
                sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $absolutePath).Hash
            }
        } else {
            [ordered]@{
                path = $relativePath.Replace('\', '/')
                exists = $false
                length = $null
                sha256 = $null
            }
        }
    }

    $indexScript = @'
import hashlib
import json
import subprocess
import sys

repo = sys.argv[1]


def git_bytes(*args: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", repo, *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


raw_stage = git_bytes("-c", "core.quotePath=false", "ls-files", "--stage", "-z")
records = []
for entry in raw_stage.split(b"\0"):
    if not entry:
        continue
    metadata, path_bytes = entry.split(b"\t", 1)
    mode, object_id, stage = metadata.decode("ascii").split(" ")
    blob_bytes = git_bytes("cat-file", "blob", object_id)
    records.append(
        {
            "path": path_bytes.decode("utf-8", "strict").replace(chr(92), "/"),
            "mode": mode,
            "stage": int(stage),
            "object_id": object_id,
            "blob_size_bytes": len(blob_bytes),
            "blob_sha256": hashlib.sha256(blob_bytes).hexdigest(),
        }
    )

records_bytes = json.dumps(
    records,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
).encode("utf-8")
payload = {
    "schema_version": "research-live-index-fingerprint-v1",
    "ls_files_stage_size_bytes": len(raw_stage),
    "ls_files_stage_sha256": hashlib.sha256(raw_stage).hexdigest(),
    "records_sha256": hashlib.sha256(records_bytes).hexdigest(),
    "records": records,
}
sys.stdout.write(
    json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    + "\n"
)
'@
    $indexJson = @(
        & 'C:\Python314\python.exe' -B -c $indexScript $RepoPath
    )
    if ($LASTEXITCODE -ne 0) {
        throw 'Complete staged-index fingerprint failed'
    }
    $indexStage = ($indexJson -join "`n") | ConvertFrom-Json
    if ($indexStage.schema_version -cne 'research-live-index-fingerprint-v1' -or
        @($indexStage.records).Count -eq 0) {
        throw 'Complete staged-index fingerprint is empty or malformed'
    }


    [ordered]@{
        head = (& git -C $RepoPath rev-parse HEAD).Trim()
        branch = (& git -C $RepoPath branch --show-current).Trim()
        status = @(& git -C $RepoPath status --porcelain=v2 --untracked-files=all)
        entries = @($entries)
        index_stage = $indexStage
    } | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
}

$beforeWip = 'C:\tmp\magent-wave-e-live-wip-before.json'
Write-ResearchWipFingerprint -RepoPath $liveRepo -OutputPath $beforeWip
$beforeWipHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $beforeWip).Hash
"live_wip_before_sha256=$beforeWipHash"
```

Expected: the command only writes `C:\tmp\magent-wave-e-live-wip-before.json`.
The fingerprint contains the raw size/SHA-256 of complete NUL-delimited
`git ls-files --stage` output and every stage record's path, mode, stage, Git
object ID, blob size, and independently computed blob-byte SHA-256. The live
branch, HEAD, index, tracked bytes, and untracked bytes are unchanged.

- [ ] **Step 5: Create the feature worktree and verify the pinned manuscript**

```powershell
& git -C $researchRepo worktree add -b $waveBranch $waveWorktree $waveParent
if ($LASTEXITCODE -ne 0) { throw 'Wave E worktree creation failed' }

if ((& git -C $waveWorktree status --porcelain).Count -ne 0) {
    throw 'New Wave E worktree is not clean'
}
$observedTargetHash = (
    Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $waveWorktree $targetRel)
).Hash
if ($observedTargetHash -cne $expectedTargetHash) {
    throw "08a source drift: expected $expectedTargetHash, observed $observedTargetHash"
}
& git -C $waveWorktree rev-parse HEAD
& git -C $waveWorktree status --short --branch
Set-Location -LiteralPath $waveWorktree
if ((Resolve-Path '.').Path -cne (Resolve-Path $waveWorktree).Path) {
    throw 'Failed to enter the dedicated Wave E Research worktree'
}
```

Expected: a clean worktree whose `08a_coarse_graining.tex` hash is exactly
`E08DEAD...EABA38`. Any different hash invalidates this plan and requires a new
AUD-20 source review.

- [ ] **Step 6: Prove the 17-test baseline without writing repository cache files**

```powershell
$env:CUDA_VISIBLE_DEVICES = '-1'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
$env:PYTHONHASHSEED = '0'
& 'C:\Python314\python.exe' -B -m pytest `
    manuscripts\magent_elbo_whitepaper\verification\test_elbo_oracles.py `
    --collect-only -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { throw 'Baseline oracle collection failed' }
```

Expected: `17 tests collected`.

- [ ] **Step 7: Build the pinned TeX baseline outside the repository and bind warning provenance**

```powershell
$baselineBuild = 'C:\tmp\magent-wave-e-baseline-c9f237d2'
if (Test-Path -LiteralPath $baselineBuild) {
    throw "Baseline build directory already exists: $baselineBuild"
}
New-Item -ItemType Directory -Path $baselineBuild | Out-Null
$env:WINDIR = $env:SystemRoot
$texEnvironmentNames = @(
    'WINDIR','SystemRoot','TEXINPUTS','BIBINPUTS','BSTINPUTS','TEXMF',
    'TEXMFHOME','TEXMFLOCAL','TEXMFCNF','TEXMFVAR','TEXMFCONFIG','TEXMFOUTPUT',
    'MIKTEX_USERCONFIG','MIKTEX_USERDATA','MIKTEX_USERINSTALL',
    'MIKTEX_COMMONCONFIG','MIKTEX_COMMONDATA','MIKTEX_COMMONINSTALL'
)
$baselineTexEnvironment = [ordered]@{}
foreach ($name in $texEnvironmentNames) {
    $baselineTexEnvironment[$name] = if (Test-Path "Env:$name") {
        (Get-Item "Env:$name").Value
    } else {
        $null
    }
}
$latexmkExe = (Get-Command latexmk -CommandType Application -ErrorAction Stop).Source
$lualatexExe = (Get-Command lualatex -CommandType Application -ErrorAction Stop).Source
$bibtexExe = (Get-Command bibtex -CommandType Application -ErrorAction Stop).Source
$kpsewhichExe = (Get-Command kpsewhich -CommandType Application -ErrorAction Stop).Source

Push-Location (Join-Path $waveWorktree 'manuscripts')
try {
    & $latexmkExe -norc -gg -lualatex -bibtex -recorder -interaction=nonstopmode `
        -halt-on-error -file-line-error "-outdir=$baselineBuild" `
        MAgent_exact_elbo_whitepaper.tex `
        *> 'C:\tmp\magent-wave-e-baseline-c9f237d2.stdout.log'
    if ($LASTEXITCODE -ne 0) { throw 'Pinned baseline TeX build failed' }
} finally {
    Pop-Location
}

$baselineLog = Join-Path $baselineBuild 'MAgent_exact_elbo_whitepaper.log'
$baselineHardErrors = Select-String -LiteralPath $baselineLog -Pattern @(
    'Undefined control sequence',
    'Citation .* undefined',
    'Reference .* undefined',
    'There were undefined references',
    'multiply defined',
    'Rerun to get cross-references right'
)
if ($baselineHardErrors) { throw 'Pinned baseline contains unresolved TeX errors' }

$baselineWarnings = @(
    Select-String -LiteralPath $baselineLog -Pattern 'Warning|Overfull|Underfull' |
        ForEach-Object {
            $_.Line -replace 'on input line \d+', 'on input line N' `
                    -replace 'page \d+', 'page N'
        } |
        Sort-Object
)
$baselineWarnings | Set-Content -LiteralPath `
    'C:\tmp\magent-wave-e-baseline-warnings.txt' -Encoding UTF8
$baselineWarningHash = (
    Get-FileHash -Algorithm SHA256 -LiteralPath `
        'C:\tmp\magent-wave-e-baseline-warnings.txt'
).Hash
$baselineArtifacts = foreach ($name in @(
    'MAgent_exact_elbo_whitepaper.pdf',
    'MAgent_exact_elbo_whitepaper.log',
    'MAgent_exact_elbo_whitepaper.fls',
    'MAgent_exact_elbo_whitepaper.aux',
    'MAgent_exact_elbo_whitepaper.blg'
)) {
    $path = Join-Path $baselineBuild $name
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Pinned baseline output is missing: $name"
    }
    $item = Get-Item -LiteralPath $path
    [ordered]@{path=$name;size_bytes=[int64]$item.Length;sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash}
}
$baselineExecutables = foreach ($path in @(
    $latexmkExe,$lualatexExe,$bibtexExe,$kpsewhichExe
)) {
    $item = Get-Item -LiteralPath $path
    [ordered]@{path=$path;size_bytes=[int64]$item.Length;sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash}
}
$baselineProvenance = 'C:\tmp\magent-wave-e-baseline-warning-provenance.json'
[ordered]@{
    schema_version = 'wave-e-baseline-warning-provenance-v1'
    context_commit = $contextCommit
    planning_commit = $planningCommit
    planning_contract_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $planningContract).Hash
    root_tex = 'manuscripts/MAgent_exact_elbo_whitepaper.tex'
    cwd_rel = 'manuscripts'
    argv = @($latexmkExe,'-norc','-gg','-lualatex','-bibtex','-recorder','-interaction=nonstopmode','-halt-on-error','-file-line-error',"-outdir=$baselineBuild",'MAgent_exact_elbo_whitepaper.tex')
    tex_environment = $baselineTexEnvironment
    executables = @($baselineExecutables)
    artifacts = @($baselineArtifacts)
    normalized_warnings = @($baselineWarnings)
    normalized_warning_sha256 = $baselineWarningHash
} | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath `
    $baselineProvenance -Encoding utf8NoBOM
```

Expected: exit zero, a root PDF in the temporary directory, no unresolved
references/citations, a recorder file, and a fixed normalized warning inventory
whose build artifacts, exact TeX environment, executables, planning contract, and
command are bound by `wave-e-baseline-warning-provenance-v1`. The later builder
reparses the baseline `.fls`/`.aux`/`.blg`, adds the exhaustive baseline input
inventory, and rejects any provenance/hash drift.

---

### Task 2: Add RED guards, apply the six prose corrections, and reach GREEN

**Files:**

- Modify:
  `manuscripts/magent_elbo_whitepaper/verification/test_elbo_oracles.py:1-5`
- Modify:
  `manuscripts/magent_elbo_whitepaper/verification/test_elbo_oracles.py:424`
- Modify:
  `manuscripts/magent_elbo_whitepaper/08a_coarse_graining.tex:174-194`

**Interfaces:**

- Consumes: the clean Task 1 worktree and pinned source hash.
- Produces: exactly two symbolic counterexample tests and one manuscript-language
  contract.
- Produces: corrected prose with unchanged equations and theorem status.

Before Step 1, retain the Task 1 location and fail closed on any CWD drift:

```powershell
$waveWorktree = 'C:\Users\chris and christine\Documents\ChatGPT\MultiAgentELBO\.superpowers\worktrees\Research-magent-aud20-remediation-20260811'
if ((Resolve-Path '.').Path -cne (Resolve-Path $waveWorktree).Path) {
    throw 'Task 2 must run from the dedicated Wave E Research worktree'
}
```

- [ ] **Step 1: Add the Path import and three regression tests**

Use `apply_patch` to add `from pathlib import Path` after the future import and
append these exact tests to `test_elbo_oracles.py`:

```python
def test_connected_block_map_has_two_attracting_fixed_points() -> None:
    """One state block does not imply one attracting fixed point."""
    x = sp.symbols("x", real=True)
    mapping = 3 * x**2 - 2 * x**3
    derivative = sp.diff(mapping, x)
    fixed_points = sp.solve(sp.Eq(mapping, x), x)

    assert fixed_points == [sp.Integer(0), sp.Rational(1, 2), sp.Integer(1)]
    assert [
        sp.simplify(derivative.subs(x, point)) for point in fixed_points
    ] == [sp.Integer(0), sp.Rational(3, 2), sp.Integer(0)]
    assert sp.simplify(
        mapping - x - x * (1 - x) * (2 * x - 1)
    ) == 0
    assert sp.simplify(derivative - 6 * x * (1 - x)) == 0
    t = sp.symbols("t", positive=True)
    left_half = t / (2 * (1 + t))
    right_half = (1 + 2 * t) / (2 * (1 + t))
    assert sp.factor((mapping - x).subs(x, left_half)) == (
        -t * (t + 2) / (4 * (t + 1) ** 3)
    )
    assert sp.factor((mapping - x).subs(x, right_half)) == (
        t * (2 * t + 1) / (4 * (t + 1) ** 3)
    )


def test_connected_scalar_family_has_gauge_inequivalent_invariant_rays() -> None:
    """Aggregation, scalar rescaling, and GL(1) preserve a/m."""
    x1, x2, x3, x4, m, a, h, zeta = sp.symbols(
        "x1 x2 x3 x4 m a h zeta",
        positive=True,
    )
    x_i = x1 + x2
    x_j = x3 + x4
    coarse_cut_weight = sum(
        left * right * m
        for left in (x1, x2)
        for right in (x3, x4)
    )
    coarse_self_term = x1 * a + x2 * a

    assert sp.simplify(coarse_cut_weight - x_i * x_j * m) == 0
    assert sp.simplify(coarse_self_term - x_i * a) == 0
    assert (x1 * x3 * m).is_positive is True
    assert sp.simplify((h**2 * a) / (h**2 * m) - a / m) == 0
    assert sp.simplify((a / zeta) / (m / zeta) - a / m) == 0
    assert sp.solve(
        [sp.Eq(h**2, 1), sp.Eq(h**2, 2)],
        [h],
        dict=True,
    ) == []


def test_coarse_graining_connectedness_claim_is_conditioned() -> None:
    source_path = (
        Path(__file__).resolve().parents[1] / "08a_coarse_graining.tex"
    )
    source = source_path.read_text(encoding="utf-8")
    forbidden = (
        "Distinct fixed points require distinct components of the interaction graph.",
        "reach the same fixed point",
        "A different effective law is not a different region of one world but a different component",
        "predicts no observable variation in the effective law",
        "What would be testable is the approach to a fixed point rather than the identity of one.",
        "The internal sector supplies no continuous moduli",
        "any variety among fixed points must come from the spectral exponent",
        "a property of how the population is connected rather than of what its agents are made of",
    )
    required = (
        "Connectivity fixes only the component decomposition",
        "rank classifies \\(M\\) alone",
        "relative invariants of the pair \\((A,M)\\)",
        "ratio \\(a/m\\)",
        "common scalar \\(\\zeta_\\ell\\) fixed exogenously",
        "block scalars \\(\\zeta_{\\ell,\\alpha}\\)",
        "depends only on its own block",
        "well defined on the residual-frame quotient",
        "Connectedness gives no converse",
        "uniqueness modulo the residual global frame action",
        "Multiple fixed objects or basins, cycles, and nonconvergent trajectories",
        "does not establish that coupled agents reach one effective law",
        "non-observability of alternative effective laws",
        "no renormalization-group flow",
    )

    for phrase in forbidden:
        assert phrase not in source
    for phrase in required:
        assert phrase in source
```

- [ ] **Step 2: Run the targeted RED command**

```powershell
& 'C:\Python314\python.exe' -B -m pytest `
    manuscripts\magent_elbo_whitepaper\verification\test_elbo_oracles.py `
    -k 'connected_block_map or connected_scalar_family or connectedness_claim' `
    -q -p no:cacheprovider
```

Expected: `2 passed, 1 failed`. Both exact mathematical controls pass, including
the exact basin-sign parameterizations and the GL(1) relative-invariant control. The source
contract fails because the pinned manuscript still contains the first forbidden
conclusion and lacks the required calibrated language. Any failure in either
exact oracle blocks the prose edit and triggers mathematical re-review.

- [ ] **Step 3: Replace line 174 with the weighted-spectrum boundary**

Use `apply_patch` to replace the full current paragraph at line 174 with exactly:

```tex
Two kinds of invariant may label a declared fixed object, but neither is determined by connectivity alone. The first is spectral. Because the interaction operator and its Laplacian part transform by the same congruence under a change of frame, the generalized spectrum of the pair is unchanged by local reframing, so those eigenvalue data are frame-independent without gauge fixing. They remain data of the full weighted operator pair, not of the unweighted support graph. If a spectral density exists and has a power law near zero, its exponent may supply a continuous label for a specified flow; existence of that density and preservation of the power law are additional hypotheses. Connectivity fixes only the component decomposition and the absence of cross-component observations. It neither fixes the within-component spectrum nor exhausts fixed-object variety.
```

- [ ] **Step 4: Replace line 176 with the full-pair and quotient boundary**

Use `apply_patch` to replace the full current paragraph at line 176 with exactly:

```tex
The second proposed invariant concerns the internal matrices, where the object being classified must be kept explicit. Under the residual global frame action \(M\mapsto h^{\top}Mh\), Sylvester's law classifies \(M\) alone by inertia, and rank classifies \(M\) alone within the positive-semidefinite cone. It does not classify the full pair \((A,M)\) under simultaneous congruence. The pair may carry relative invariants of the pair \((A,M)\): for \(K=1\), \((a,m)\mapsto(h^2a,h^2m)\) leaves the continuous ratio \(a/m\) unchanged, even though every \(m>0\) has rank one. The rank class of \(M\) therefore does not imply one internal fixed-object class or exclude continuous moduli. A claim about a fixed object modulo the residual frame action also requires the specified normalized map to be well defined on the residual-frame quotient. A sufficient condition is residual-frame equivariance of each block map together with either a gauge-invariant common scalar \(\zeta_\ell\) fixed exogenously or gauge-invariant block scalars \(\zeta_{\ell,\alpha}\) whose \(\alpha\)th value depends only on its own block; no such descent or quotient-uniqueness theorem is established here.
```

- [ ] **Step 5: Replace line 178 with the convergence-qualified participatory reading**

Use `apply_patch` to replace the full current paragraph at line 178 with exactly:

```tex
This bears on the participatory reading, and it is worth stating what that reading costs. If an agent's observations are the states of other agents, then the world an agent models is the remainder of the population, and a fixed point of a specified normalized map based on Equation~\eqref{eq:rescaled-aggregation-flow} would be a candidate effective law for that world. Saying that the population has arrived at that candidate adds a convergence premise not established here. Calling the candidate a physical law adds the further premise that there is nothing else for the agents to be modeling. Both are identifications rather than theorems. The latter premise is available in this framework because observations are gauge-inert coordinates exchanged along declared edges, but the chapter marks it as a declaration.
```

- [ ] **Step 6: Replace line 180 with the exact componentwise conclusion**

Use `apply_patch` to replace the full current paragraph at line 180 with exactly:

```tex
Granting that identification, the component decomposition supplies only a conditional decoupling statement. If every \(S_\ell\) respects the connected-component decomposition and either the common positive scalar \(\zeta_\ell\) is fixed exogenously or the block-local generalization uses positive scalars \(\zeta_{\ell,\alpha}\) with each \(\zeta_{\ell,\alpha}\) depending only on block \(\alpha\), then the interaction operator remains block diagonal, the conditional maps act componentwise, and no observations cross components. If quotient language is used, the common exogenous scalar or the block-local scalars must also be gauge-invariant so that each normalized block map descends under the residual global frame action. Connectedness gives no converse: it implies neither existence nor uniqueness of a fixed object, nor convergence of all admitted initial models to one basin. Multiple fixed objects or basins, cycles, and nonconvergent trajectories on the model space of one connected component are not excluded. The construction therefore does not establish that coupled agents reach one effective law, that distinct effective laws require disconnected components, or that effective-law variation is unobservable. Those conclusions would require a specified rescaled map on a common comparison space, a well-defined descended map, and a proof of existence, uniqueness modulo the residual global frame action, convergence of all admitted initial models, and common basin coverage on the relevant quotient.
```

- [ ] **Step 7: Replace line 182 with the testable running-coupling statement**

Use `apply_patch` to replace the full current paragraph at line 182 with exactly:

```tex
Once a normalization, comparison space, and trajectory are declared, the scale dependence of effective couplings is testable. Away from a fixed object the parameters of Equation~\eqref{eq:rescaled-aggregation-flow} run with the resolution at which the population is described, and the form of that running is a property of the specified map. Interpreting the running as approach to a fixed object additionally requires a declared fixed object and a convergence criterion. The running itself, not a unique endpoint or the exclusion of alternative effective-law classes, is the falsifiable residue of this section.
```

- [ ] **Step 8: Replace line 194 with the complete OPEN boundary**

Use `apply_patch` to replace the full current paragraph at line 194 with exactly:

```tex
It adopts no rescaling, and therefore establishes no renormalization-group flow. Section~\ref{sec:coarse-universality} is conditional throughout: it records what a declared rescaling would imply and does not supply one. Within that conditional development, the invariance of the scale-free form is proved, but the existence of a fixed exogenous common scalar or gauge-invariant block scalars \(\zeta_{\ell,\alpha}\) depending only on their own blocks, descent of a specified normalized map to the residual-frame quotient, existence or uniqueness of a fixed orbit, convergence, common basin coverage, and non-observability of alternative effective laws are not established. Rank classification of \(M\) alone does not classify the relative invariants of \((A,M)\), and connectivity does not exhaust fixed-object variety, so no universality statement is established here. The identification of a fixed point with a physical law is marked there as a declaration rather than derived; and no specific law follows from any of it, since the construction fixes no dynamics, no signature, and no structure group beyond the one declared in Chapter~\ref{ch:bundle-geometry}. What the section supplies is the place such a derivation would occupy.
```

- [ ] **Step 9: Run targeted and full GREEN tests**

```powershell
& 'C:\Python314\python.exe' -B -m pytest `
    manuscripts\magent_elbo_whitepaper\verification\test_elbo_oracles.py `
    -k 'connected_block_map or connected_scalar_family or connectedness_claim' `
    -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { throw 'Wave E targeted GREEN failed' }

& 'C:\Python314\python.exe' -B -m pytest `
    manuscripts\magent_elbo_whitepaper\verification\test_elbo_oracles.py `
    -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { throw 'Wave E full oracle GREEN failed' }
```

Expected: targeted `3 passed`; full file `20 passed`, zero skipped, zero failures,
and zero errors.

- [ ] **Step 10: Run the standalone forbidden/required language scan**

```powershell
$targetRel = 'manuscripts/magent_elbo_whitepaper/08a_coarse_graining.tex'
$source = Get-Content -Raw -LiteralPath $targetRel
$forbidden = @(
    'Distinct fixed points require distinct components of the interaction graph.',
    'reach the same fixed point',
    'A different effective law is not a different region of one world but a different component',
    'predicts no observable variation in the effective law',
    'What would be testable is the approach to a fixed point rather than the identity of one.',
    'The internal sector supplies no continuous moduli',
    'any variety among fixed points must come from the spectral exponent',
    'a property of how the population is connected rather than of what its agents are made of'
)
$required = @(
    'Connectivity fixes only the component decomposition',
    'rank classifies \(M\) alone',
    'relative invariants of the pair \((A,M)\)',
    'ratio \(a/m\)',
    'common scalar \(\zeta_\ell\) fixed exogenously',
    'block scalars \(\zeta_{\ell,\alpha}\)',
    'depends only on its own block',
    'well defined on the residual-frame quotient',
    'Connectedness gives no converse',
    'uniqueness modulo the residual global frame action',
    'Multiple fixed objects or basins, cycles, and nonconvergent trajectories',
    'does not establish that coupled agents reach one effective law',
    'non-observability of alternative effective laws',
    'no renormalization-group flow'
)
$forbiddenFound = @($forbidden | Where-Object { $source.Contains($_) })
$requiredMissing = @($required | Where-Object { -not $source.Contains($_) })
if ($forbiddenFound.Count -ne 0) {
    throw "Forbidden claims remain: $($forbiddenFound -join ' | ')"
}
if ($requiredMissing.Count -ne 0) {
    throw "Required boundaries are missing: $($requiredMissing -join ' | ')"
}
```

Expected: no exception.

- [ ] **Step 11: Prove every equation environment is byte-identical**

```powershell
$baselineText = (
    & git show 'c9f237d2ca54c274ba5760012e62823a69d203a3:manuscripts/magent_elbo_whitepaper/08a_coarse_graining.tex'
) -join "`n"
$currentText = (Get-Content -Raw -LiteralPath $targetRel).Replace("`r`n", "`n")
$equationPattern = [regex]'(?s)\\begin\{equation\}.*?\\end\{equation\}'
$baselineEquations = @($equationPattern.Matches($baselineText) | ForEach-Object Value)
$currentEquations = @($equationPattern.Matches($currentText) | ForEach-Object Value)

if ($baselineEquations.Count -ne $currentEquations.Count) {
    throw 'Equation environment count changed'
}
for ($index = 0; $index -lt $baselineEquations.Count; $index++) {
    if ($baselineEquations[$index] -cne $currentEquations[$index]) {
        throw "Equation environment $index changed"
    }
}
```

Expected: all nine `equation` environments compare identically after CRLF/LF
normalization.

- [ ] **Step 12: Inspect the exact manuscript/test diff and freeze allowed source hunks**

```powershell
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'Whitespace validation failed' }

& git diff --unified=3 -- `
    manuscripts/magent_elbo_whitepaper/08a_coarse_graining.tex `
    manuscripts/magent_elbo_whitepaper/verification/test_elbo_oracles.py

$changed = @(& git diff --name-only) | Sort-Object
$expectedChanged = @(
    'manuscripts/magent_elbo_whitepaper/08a_coarse_graining.tex',
    'manuscripts/magent_elbo_whitepaper/verification/test_elbo_oracles.py'
) | Sort-Object
if (Compare-Object $changed $expectedChanged) {
    throw 'The manuscript phase must own exactly its two paths'
}
```

Expected: exactly the manuscript and oracle-test paths are modified. Do not commit
until the checked-in evidence builder and its tests pass in Task 3.

The later `source-diff.json` validator freezes the baseline-to-`P` and
baseline-to-`E` full change sets. Its source projection has exactly two
`modified` records, in order `TARGET_REL`, `ORACLE_REL`, each with non-null old
and new blob/mode/size/SHA-256 identity, and exactly two `added` records, in
order `TOOL_TEST_REL`, `TOOL_REL`, each with null old identity and exact non-null
new blob/mode/size/SHA-256 identity. The target-manuscript allowlist is exactly six
one-line replacement hunks whose old starts are `174`, `176`, `178`, `180`, `182`,
and `194`. The oracle-test allowlist is exactly one `Path` import after the future
import and an EOF append containing the three named tests above. The two evidence
adapter files are allowed only as whole-file additions. Baseline-to-`P` has no
other change. Baseline-to-`E` additionally contains exactly the already validated
14 whole-file candidate-evidence additions in `P..E`; the record classifies and
hashes them as `evidence_only_changes`, never as source/dependency/tested inputs.
Any other path, hunk, rename, mode change, equation-byte change, or deletion rejects
before publication.

---

### Task 3: Add the Research-local privacy and evidence builder

**Files:**

- Create:
  `manuscripts/magent_elbo_whitepaper/verification/wave_e_evidence.py`
- Create:
  `manuscripts/magent_elbo_whitepaper/verification/test_wave_e_evidence.py`
- Test outside the repository:
  `C:\tmp\magent-wave-e-tool-green.xml`

**Interfaces:**

- Consumes: the two modified Task 2 paths, a raw out-of-repository staging root,
  a fresh `latexmk -recorder` build, and structured raw review JSON.
- Produces: `scan_raw(...)`, `plan_publication(...)`,
  `commit_publication(...)`, `collect_tex_inputs(...)`,
  `collect_bibtex_inputs(...)`, `validate_wave0_plan_bytes(...)`,
  `validate_planning_release(...)`, `validate_verification_binding(...)`,
  `validate_bundle(...)`, `populate_ledger(...)`,
  and CLI subcommands `run-junit`, `scan`, `freeze-review-inputs`,
  `publish-bundle`, `validate-bundle`, `populate-ledger`, and
  `validate-ledger-links`.
- Produces: a clean four-path implementation commit `P`. The exact oracle file
  still collects 20 tests; the evidence-tool file separately collects fourteen
  tests.

Before Step 1, retain and verify the same worktree CWD:

```powershell
$waveWorktree = 'C:\Users\chris and christine\Documents\ChatGPT\MultiAgentELBO\.superpowers\worktrees\Research-magent-aud20-remediation-20260811'
if ((Resolve-Path '.').Path -cne (Resolve-Path $waveWorktree).Path) {
    throw 'Task 3 must run from the dedicated Wave E Research worktree'
}
```

- [ ] **Step 1: Write the fourteen builder RED tests**

Create `test_wave_e_evidence.py` with these imports, helpers, and fourteen tests.
Every name below is part of the required builder interface:

```python
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from manuscripts.magent_elbo_whitepaper.verification import wave_e_evidence


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _record(path: str, payload: bytes) -> dict[str, object]:
    return {
        "path": path,
        "size_bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def test_publication_is_fully_planned_before_the_public_root_exists(
    tmp_path: Path,
) -> None:
    raw_root = tmp_path / "raw"
    public_root = tmp_path / "public"
    raw = _write(raw_root / "elbo-oracles.xml", r"C:\Users\Alice\repo\x")
    plan = wave_e_evidence.plan_publication(
        raw_files={"elbo-oracles.xml": raw},
        replacements=((r"C:\Users\Alice", "$USERPROFILE"),),
        public_root=public_root,
    )
    repeated = wave_e_evidence.plan_publication(
        raw_files={"elbo-oracles.xml": raw},
        replacements=((r"C:\Users\Alice", "$USERPROFILE"),),
        public_root=public_root,
    )
    assert not public_root.exists()
    assert plan["elbo-oracles.xml"].raw_sha256 == hashlib.sha256(
        raw.read_bytes()
    ).hexdigest()
    assert b"$USERPROFILE" in plan["elbo-oracles.xml"].public_bytes
    assert repeated == plan
    wave_e_evidence.commit_publication(plan, public_root)
    assert (public_root / "elbo-oracles.xml").read_bytes() == plan[
        "elbo-oracles.xml"
    ].public_bytes


def test_tex_inventory_is_exhaustive_and_excludes_build_products(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    build = tmp_path / "build"
    texmf = tmp_path / "texmf"
    root = _write(repo / "manuscripts" / "root.tex", "root")
    include = _write(repo / "manuscripts" / "chapter.tex", "chapter")
    style = _write(repo / "manuscripts" / "scientific_report.sty", "style")
    cls = _write(texmf / "report.cls", "class")
    bib = _write(repo / "manuscripts" / "references.bib", "bib")
    bst = _write(texmf / "plainnat.bst", "bst")
    generated = _write(build / "root.aux", "aux")
    fls = _write(
        build / "root.fls",
        "PWD " + str(repo / "manuscripts") + "\n"
        + "\n".join(f"INPUT {path}" for path in (root, include, style, cls, generated))
        + "\n",
    )
    aux = _write(
        build / "root.aux",
        "\\bibstyle{plainnat}\n\\bibdata{references}\n",
    )
    blg = _write(
        build / "root.blg",
        "The style file: plainnat.bst\nDatabase file #1: references.bib\n",
    )
    records = wave_e_evidence.collect_tex_inputs(
        fls_path=fls,
        repo_root=repo,
        build_root=build,
        replacements=((str(repo), "$REPO"), (str(texmf), "$TEXMF")),
    )
    assert {record["path"] for record in records} == {
        "$REPO/manuscripts/root.tex",
        "$REPO/manuscripts/chapter.tex",
        "$REPO/manuscripts/scientific_report.sty",
        "$TEXMF/report.cls",
    }
    bib_records = wave_e_evidence.collect_bibtex_inputs(
        aux_path=aux,
        blg_path=blg,
        manuscript_root=repo / "manuscripts",
        build_root=build,
        replacements=((str(repo), "$REPO"), (str(texmf), "$TEXMF")),
        resolve_tex_name=lambda name: {
            "references.bib": bib,
            "plainnat.bst": bst,
        }[name],
    )
    assert {(record["path"], record["role"]) for record in bib_records} == {
        ("$REPO/manuscripts/references.bib", "bibliography_input"),
        ("$TEXMF/plainnat.bst", "bibliography_style_input"),
    }


def test_tex_inventory_rejects_a_missing_consumed_input(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    build = tmp_path / "build"
    fls = _write(
        build / "root.fls",
        f"PWD {repo}\nINPUT {repo / 'missing.tex'}\n",
    )
    with pytest.raises(ValueError, match="missing TeX INPUT"):
        wave_e_evidence.collect_tex_inputs(
            fls_path=fls,
            repo_root=repo,
            build_root=build,
            replacements=((str(repo), "$REPO"),),
        )
    aux = _write(build / "root.aux", "\\bibdata{missing}\n\\bibstyle{plainnat}\n")
    blg = _write(
        build / "root.blg",
        "Database file #1: missing.bib\nThe style file: plainnat.bst\n",
    )
    with pytest.raises(ValueError, match="missing BibTeX input"):
        wave_e_evidence.collect_bibtex_inputs(
            aux_path=aux,
            blg_path=blg,
            manuscript_root=repo,
            build_root=build,
            replacements=((str(repo), "$REPO"),),
            resolve_tex_name=lambda name: repo / name,
        )


def test_generated_evidence_cannot_be_a_dependency_input(tmp_path: Path) -> None:
    raw_root = tmp_path / "raw"
    public_root = tmp_path / "public"
    generated = _write(raw_root / "claim-language.json", "{}")
    with pytest.raises(ValueError, match="evidence output used as dependency"):
        wave_e_evidence.validate_dependency_separation(
            dependency_paths=(generated,),
            raw_root=raw_root,
            public_root=public_root,
        )


def test_closed_inventory_rejects_extra_missing_and_modified_files(
    tmp_path: Path,
) -> None:
    bundle = tmp_path / "bundle"
    first = _write(bundle / "first.json", "one")
    second = _write(bundle / "second.json", "two")
    inventory = (_record("first.json", first.read_bytes()), _record("second.json", second.read_bytes()))
    wave_e_evidence.validate_closed_inventory(
        bundle_dir=bundle,
        inventory=inventory,
        self_name="closure-index.json",
        actual_names={"first.json", "second.json", "closure-index.json"},
    )
    _write(bundle / "extra.json", "extra")
    with pytest.raises(ValueError, match="closure allowlist mismatch"):
        wave_e_evidence.validate_closed_inventory(
            bundle_dir=bundle,
            inventory=inventory,
            self_name="closure-index.json",
            actual_names={"first.json", "second.json", "extra.json", "closure-index.json"},
        )
    (bundle / "extra.json").unlink()
    first.write_text("changed", encoding="utf-8")
    with pytest.raises(ValueError, match="closure hash mismatch"):
        wave_e_evidence.validate_closed_inventory(
            bundle_dir=bundle,
            inventory=inventory,
            self_name="closure-index.json",
            actual_names={"first.json", "second.json", "closure-index.json"},
        )
    first.write_text("one", encoding="utf-8")
    second.unlink()
    with pytest.raises(ValueError, match="closure file is missing"):
        wave_e_evidence.validate_closed_inventory(
            bundle_dir=bundle,
            inventory=inventory,
            self_name="closure-index.json",
            actual_names={"first.json", "closure-index.json"},
        )


def test_populate_ledger_requires_empty_template_and_writes_two_high_claims(
    tmp_path: Path,
) -> None:
    fixture = wave_e_evidence.write_test_closure_fixture(tmp_path)
    ledger = fixture["ledger_path"]
    index = fixture["closure_index_path"]
    views = fixture["views_dir"]
    wave_e_evidence.populate_ledger(
        repo_root=fixture["repo_root"],
        ledger_path=ledger,
        closure_index_path=index,
        views_dir=views,
    )
    payload = json.loads(ledger.read_text(encoding="utf-8"))
    assert [claim["id"] for claim in payload["claims"]] == [
        "AUD20-DEFECT-REPRODUCTION",
        "AUD20-CORRECTED-CONTRACT",
    ]
    assert [claim["state"] for claim in payload["claims"]] == [
        "REFUTED",
        "EVIDENCE_VERIFIED",
    ]
    assert all(claim["severity"] == "high" for claim in payload["claims"])
    assert all(
        claim["escalation_triggers"] == ["high_severity"]
        for claim in payload["claims"]
    )
    assert all(claim["escalation_target"] == 4 for claim in payload["claims"])
    assert all(
        [criterion["name"] for criterion in claim["criteria"]]
        == list(wave_e_evidence.MATH_CRITERION_NAMES)
        for claim in payload["claims"]
    )
    assert all(
        all(criterion["score"] == 20 for criterion in claim["criteria"])
        for claim in payload["claims"]
    )
    assert all(
        claim["views"]["calibration_kind"]
        == "artifact-bound-pairwise-v1"
        for claim in payload["claims"]
    )
    assert all(claim["views"]["unresolved_disagreement"] is False for claim in payload["claims"])
    assert all(len(claim["views"]["scores"]) == 4 for claim in payload["claims"])
    assert all(
        all(
            [criterion["name"] for criterion in view["criteria"]]
            == list(wave_e_evidence.MATH_CRITERION_NAMES)
            for view in claim["views"]["scores"]
        )
        for claim in payload["claims"]
    )
    assert all(
        all(
            [criterion["name"] for criterion in match["criteria"]]
            == list(wave_e_evidence.MATH_CRITERION_NAMES)
            for match in claim["views"]["comparison"]["matches"]
        )
        for claim in payload["claims"]
    )
    with pytest.raises(ValueError, match="ledger template is not empty"):
        wave_e_evidence.populate_ledger(
            repo_root=fixture["repo_root"],
            ledger_path=ledger,
            closure_index_path=index,
            views_dir=views,
        )


def test_run_junit_is_wave0_byte_equivalent_and_create_once(tmp_path: Path) -> None:
    fixture = wave_e_evidence.write_test_runner_fixture(tmp_path, sys.executable)
    wave_e_evidence.run_junit(**fixture["arguments"])
    record = fixture["record_path"]
    assert record.read_bytes() == fixture["expected_wave0_record_bytes"]
    payload = json.loads(record.read_text(encoding="utf-8"))
    assert set(payload) == {
        "schema_version", "id", "argv", "cwd_rel", "interpreter",
        "env_allowlist", "started_utc", "ended_utc", "exit_code", "junit",
    }
    assert payload["schema_version"] == "remediation-command-record-v1"
    with pytest.raises(FileExistsError, match="command record already exists"):
        wave_e_evidence.run_junit(**fixture["arguments"])


def test_base_index_conforms_and_domain_inventory_is_named_extension(
    tmp_path: Path,
) -> None:
    fixture = wave_e_evidence.write_test_bundle_fixture(tmp_path)
    base = wave_e_evidence.build_base_index(**fixture["base_arguments"])
    assert set(base) == {
        "schema_version", "wave", "evidence_stage", "tested_git_head",
        "implementation_parent_git_head", "platform", "environment_record",
        "dependency_versions", "dependency_inputs", "tested_input_policy",
        "tested_input_inventory_sha256", "commands", "source_config_bindings",
        "reviewed_plan_binding", "verification_contract_binding", "files",
    }
    assert base["schema_version"] == "remediation-evidence-v1"
    assert set(base["tested_input_policy"]) == {
        "schema_version", "selection_rules", "exclusion_rules", "inputs",
    }
    assert base["tested_input_policy"]["schema_version"] == (
        "wave-e-research-manuscripts-tested-inputs-v1"
    )
    assert base["tested_input_policy"]["selection_rules"] == [
        "prefix:manuscripts/",
    ]
    assert base["tested_input_policy"]["exclusion_rules"] == [
        "prefix:docs/verification/evidence/",
        "prefix:verification-evidence/",
        "prefix:.verification/",
        "prefix:.pytest_cache/",
        "prefix:.pytest-",
    ]
    assert [record["path"] for record in base["source_config_bindings"]] == list(
        wave_e_evidence.SOURCE_CONFIG_BINDING_PATHS
    )
    assert set(base["environment_record"]) == {
        "platform", "interpreter", "dependency_versions",
        "dependency_inputs", "environment_variables",
    }
    assert "privacy_transform" not in base["environment_record"]
    assert base["reviewed_plan_binding"] == fixture["reviewed_plan_binding"]
    assert base["verification_contract_binding"] == (
        fixture["wave0_verification_binding"]
    )
    assert [record["path"] for record in base["files"]] == list(
        wave_e_evidence.BASE_COMMON_FILE_PATHS
    )
    assert all(
        set(record) == {"path", "kind", "size_bytes", "sha256"}
        for record in base["files"]
    )
    assert all(
        record["kind"] == wave_e_evidence.BASE_COMMON_FILE_KINDS[record["path"]]
        and record["size_bytes"] == len(fixture["common_public_bytes"][record["path"]])
        and record["sha256"] == hashlib.sha256(
            fixture["common_public_bytes"][record["path"]]
        ).hexdigest()
        for record in base["files"]
    )
    assert {
        "remediation-index.json", "evidence-index.json", "closure-index.json",
    }.isdisjoint(record["path"] for record in base["files"])
    wave_e_evidence.validate_wave0_plan_bytes(fixture["wave0_plan_bytes"])
    with pytest.raises(ValueError, match="binding Wave 0 plan SHA-256"):
        wave_e_evidence.validate_wave0_plan_bytes(
            fixture["wave0_plan_bytes"] + b"\n"
        )
    wave_e_evidence.validate_planning_release(
        release_bytes=fixture["planning_release_bytes"],
        reviewed_plan_binding=base["reviewed_plan_binding"],
        expected_planning_commit=fixture["planning_commit"],
    )
    mutated_release = json.loads(fixture["planning_release_bytes"])
    mutated_release["reviewed_plan"]["sha256"] = "0" * 64
    with pytest.raises(ValueError, match="planning-release reviewed plan"):
        wave_e_evidence.validate_planning_release(
            release_bytes=wave_e_evidence.canonical_json(mutated_release),
            reviewed_plan_binding=base["reviewed_plan_binding"],
            expected_planning_commit=fixture["planning_commit"],
        )
    base_path = fixture["raw_root"] / "remediation-index.json"
    base_bytes = wave_e_evidence.canonical_json(base)
    base_path.write_bytes(base_bytes)
    planning = json.loads(
        Path(r"C:\tmp\magent-wave-e-planning-contract.json").read_text(
            encoding="utf-8"
        )
    )
    planning_snapshot = Path(
        rf"C:\tmp\magent-wave-e-planning-snapshot-{planning['planning_commit'][:12]}"
    )
    wave0_validator = planning_snapshot / "tools" / "remediation_evidence.py"
    completed = subprocess.run(
        [
            sys.executable, "-B", str(wave0_validator), "validate",
            str(base_path), "--cwd", str(fixture["repo_root"]),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert base_path.read_bytes() == base_bytes
    for name, invalid_bytes in fixture["wave0_invalid_base_bytes"].items():
        invalid_path = fixture["raw_root"] / f"invalid-{name}.json"
        invalid_path.write_bytes(invalid_bytes)
        rejected = subprocess.run(
            [
                sys.executable, "-B", str(wave0_validator), "validate",
                str(invalid_path), "--cwd", str(fixture["repo_root"]),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        assert rejected.returncode != 0, name
    domain = wave_e_evidence.build_domain_inventory(
        base_index=base,
        **fixture["domain_arguments"],
    )
    assert domain["schema_version"] == "wave-e-domain-inventory-v1"
    assert domain["base_schema_version"] == "remediation-evidence-v1"
    assert domain["privacy_provenance"] == fixture["privacy_provenance"]
    assert domain["base_index"]["sha256"] == hashlib.sha256(
        wave_e_evidence.canonical_json(base)
    ).hexdigest()
    wave_e_evidence.validate_verification_binding(
        binding=fixture["wave0_verification_binding"],
        dependency_inputs=base["dependency_inputs"],
    )


def test_candidate_pp_and_closure_ep_reject_swaps_nonchild_and_extra_diff(
    tmp_path: Path,
) -> None:
    fixture = wave_e_evidence.write_test_head_polarity_fixture(tmp_path)
    wave_e_evidence.validate_bundle(**fixture["candidate_pp"])
    wave_e_evidence.validate_bundle(**fixture["closure_ep"])
    for mutation, message in (
        ("candidate_ep", "candidate head polarity"),
        ("closure_pp", "closure head polarity"),
        ("closure_pe", "closure head polarity"),
        ("closure_nonchild", "not a direct child"),
        ("closure_extra_diff", "P..E path outside candidate evidence"),
    ):
        with pytest.raises(ValueError, match=message):
            wave_e_evidence.validate_bundle(**fixture[mutation])


def test_environment_junit_and_schema_drift_fail_closed(tmp_path: Path) -> None:
    fixture = wave_e_evidence.write_test_bundle_fixture(tmp_path)
    for mutation, message in (
        ("missing_environment_key", "six-key CPU environment"),
        ("cuda_opt_in", "CUDA opt-in"),
        ("wrong_junit_total", "JUnit totals"),
        ("duplicate_testcase", "unique testcase IDs"),
        ("unknown_base_key", "base schema keys"),
        ("missing_reviewed_plan_binding", "reviewed plan binding"),
        ("mutated_planning_release", "planning-release reviewed plan"),
        ("missing_verification_contract_binding", "verification contract binding"),
        ("base_environment_privacy_transform", "environment schema"),
        ("base_files_missing", "base files inventory"),
        ("base_files_extra", "base files inventory"),
        ("base_files_index_back_edge", "base index self-reference"),
        ("base_files_byte_mutation", "base files hash"),
        ("unknown_domain_key", "domain schema keys"),
        ("wrong_command_schema", "command schema"),
        ("verification_snapshot_hash_drift", "verification-contract identity"),
        ("verification_snapshot_missing_criterion", "five criteria files"),
        ("verification_claude_root", "active Codex verification root"),
    ):
        with pytest.raises(ValueError, match=message):
            wave_e_evidence.validate_test_mutation(fixture, mutation)


def test_tested_input_policy_rejects_omission_hash_drift_and_matching_untracked(
    tmp_path: Path,
) -> None:
    fixture = wave_e_evidence.write_test_input_policy_fixture(tmp_path)
    wave_e_evidence.validate_tested_inputs(**fixture["valid"])
    for mutation, message in (
        ("omitted_tracked_input", "tested input omitted"),
        ("hash_drift", "tested input hash mismatch"),
        ("digest_drift", "tested input inventory digest"),
        ("matching_untracked_path", "matching untracked input"),
        ("case_alias", "canonical tested input path"),
        ("reparse_input", "reparse tested input"),
    ):
        with pytest.raises(ValueError, match=message):
            wave_e_evidence.validate_tested_inputs(**fixture[mutation])


def test_scan_raw_emits_literal_derivation(tmp_path: Path) -> None:
    fixture = wave_e_evidence.write_test_scan_fixture(tmp_path)
    wave_e_evidence.scan_raw(**fixture)
    actual = (fixture["raw_root"] / "aud20-derivation.md").read_bytes()
    expected = wave_e_evidence.AUD20_DERIVATION_TEXT.encode("utf-8")
    assert actual == expected
    assert actual.endswith(b"\n")
    assert hashlib.sha256(actual).hexdigest() == fixture["derivation_sha256"]
    assert wave_e_evidence.FORBIDDEN_CLAIMS == (
        "Distinct fixed points require distinct components of the interaction graph.",
        "reach the same fixed point",
        "A different effective law is not a different region of one world but a different component",
        "predicts no observable variation in the effective law",
        "What would be testable is the approach to a fixed point rather than the identity of one.",
        "The internal sector supplies no continuous moduli",
        "any variety among fixed points must come from the spectral exponent",
        "a property of how the population is connected rather than of what its agents are made of",
    )
    claim_scan = json.loads(
        (fixture["raw_root"] / "claim-language.json").read_text(encoding="utf-8")
    )
    assert claim_scan["forbidden"] == list(wave_e_evidence.FORBIDDEN_CLAIMS)
    assert claim_scan["required"] == list(wave_e_evidence.REQUIRED_CLAIMS)


def test_source_diff_records_blobs_hashes_paths_and_exact_hunks(
    tmp_path: Path,
) -> None:
    fixture = wave_e_evidence.write_test_source_diff_fixture(tmp_path)
    record = wave_e_evidence.collect_source_diff(**fixture["arguments"])
    assert record == fixture["expected_record"]
    assert [hunk["old_start"] for hunk in record["source_changes"]["manuscript_hunks"]] == [
        174, 176, 178, 180, 182, 194,
    ]
    modified = record["source_changes"]["modified"]
    added = record["source_changes"]["added"]
    assert [change["path"] for change in modified] == [
        wave_e_evidence.TARGET_REL,
        wave_e_evidence.ORACLE_REL,
    ]
    assert [change["path"] for change in added] == [
        wave_e_evidence.TOOL_TEST_REL,
        wave_e_evidence.TOOL_REL,
    ]
    assert all(change["status"] == "modified" for change in modified)
    assert all(
        change["old_blob"] and change["old_size_bytes"] is not None
        and change["old_sha256"] and change["old_mode"]
        and change["new_blob"] and change["new_size_bytes"] is not None
        and change["new_sha256"] and change["new_mode"]
        for change in modified
    )
    assert all(change["status"] == "added" for change in added)
    assert all(
        change["old_blob"] is None and change["old_size_bytes"] is None
        and change["old_sha256"] is None and change["old_mode"] is None
        and change["new_blob"] and change["new_size_bytes"] is not None
        and change["new_sha256"] and change["new_mode"]
        for change in added
    )
    assert len(record["comparisons"]["baseline_to_p"]["evidence_only_changes"]) == 0
    evidence_added = record["comparisons"]["baseline_to_e"]["evidence_only_changes"]
    assert len(evidence_added) == 14
    assert [change["path"].rsplit("/", 1)[-1] for change in evidence_added] == list(
        wave_e_evidence.CANDIDATE_EVIDENCE_FILES
    )
    assert all(change["new_blob"] and change["new_sha256"] for change in record["all_changes"])
    assert all(
        change["status"] == "added"
        and change["role"] == "generated_evidence_output"
        and change["old_blob"] is None and change["old_size_bytes"] is None
        and change["old_sha256"] is None and change["old_mode"] is None
        and change["new_blob"] and change["new_size_bytes"] is not None
        and change["new_sha256"] and change["new_mode"]
        for change in evidence_added
    )
    with pytest.raises(ValueError, match="source diff allowlist"):
        wave_e_evidence.collect_source_diff(**fixture["extra_hunk_arguments"])


def test_pre_review_manifest_and_review_hash_chain_reject_mutation(
    tmp_path: Path,
) -> None:
    fixture = wave_e_evidence.write_test_review_freeze_fixture(tmp_path)
    manifest = wave_e_evidence.freeze_review_inputs(**fixture["freeze_arguments"])
    reviews = wave_e_evidence.write_test_reviews(
        fixture,
        pre_review_manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),
    )
    wave_e_evidence.validate_reviews(**reviews["valid_arguments"])
    fixture["frozen_raw_path"].write_bytes(b"mutated\n")
    with pytest.raises(ValueError, match="pre-review frozen byte changed"):
        wave_e_evidence.validate_reviews(**reviews["valid_arguments"])
    fixture["restore_frozen_raw"]()
    for mutation, message in (
        ("skeptic_missing_primary_hash", "skeptic prior-review hash chain"),
        ("adjudicator_missing_skeptic_hash", "adjudicator prior-review hash chain"),
        ("review_manifest_hash_drift", "pre-review manifest hash"),
    ):
        with pytest.raises(ValueError, match=message):
            wave_e_evidence.validate_reviews(**reviews[mutation])
```

All `write_test_*` functions and `restore_frozen_raw` are test-only helpers in the
builder module; production CLI paths never call them. The fixtures create real
temporary Git repositories and subprocess-produced JUnit, exercise the same
canonical serializers, Wave 0 adapter, ancestry checks, input digests, manifests,
and review validators as production, and never mock those semantics. The closure
fixture creates an exact 14-file candidate child, fresh raw records, an exact
21-file validator-clean closure, and the gate's four-field empty ledger template.

- [ ] **Step 2: Run the builder RED test**

```powershell
& 'C:\Python314\python.exe' -B -m pytest `
    manuscripts\magent_elbo_whitepaper\verification\test_wave_e_evidence.py `
    -q -p no:cacheprovider `
    --junitxml=C:\tmp\magent-wave-e-tool-red.xml
```

Expected: collection fails because `wave_e_evidence.py` does not exist.

- [ ] **Step 3: Implement the builder's closed interfaces**

Create `wave_e_evidence.py` with these literal constants and dataclass:

```python
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

BASE_SCHEMA_VERSION = "remediation-evidence-v1"
DOMAIN_SCHEMA_VERSION = "wave-e-domain-inventory-v1"
COMMAND_SCHEMA_VERSION = "remediation-command-record-v1"
DERIVATION_SCHEMA_VERSION = "aud20-derivation-v1"
TESTED_INPUT_POLICY_SCHEMA = "wave-e-research-manuscripts-tested-inputs-v1"
TESTED_INPUT_SELECTION_RULES = ("prefix:manuscripts/",)
TESTED_INPUT_EXCLUSION_RULES = (
    "prefix:docs/verification/evidence/",
    "prefix:verification-evidence/",
    "prefix:.verification/",
    "prefix:.pytest_cache/",
    "prefix:.pytest-",
)
PRIVACY_POLICY = "wave-e-path-redaction-v1"
WAVE0_PLAN_SHA256 = (
    "dbe2263a3b0fe1e9f5db4ff1fca9a19f819cfd32ef38da71d6e5cb5485723ac2"
)
CONTEXT_COMMIT = "c9f237d2ca54c274ba5760012e62823a69d203a3"
ORACLE_REL = "manuscripts/magent_elbo_whitepaper/verification/test_elbo_oracles.py"
ORACLE_IMPL_REL = "manuscripts/magent_elbo_whitepaper/verification/elbo_oracles.py"
TOOL_REL = "manuscripts/magent_elbo_whitepaper/verification/wave_e_evidence.py"
TOOL_TEST_REL = "manuscripts/magent_elbo_whitepaper/verification/test_wave_e_evidence.py"
TARGET_REL = "manuscripts/magent_elbo_whitepaper/08a_coarse_graining.tex"
ROOT_TEX_REL = "manuscripts/MAgent_exact_elbo_whitepaper.tex"
SOURCE_CONFIG_BINDING_PATHS = (
    ROOT_TEX_REL,
    TARGET_REL,
    ORACLE_IMPL_REL,
    ORACLE_REL,
    TOOL_TEST_REL,
    TOOL_REL,
)
FORBIDDEN_CLAIMS = (
    "Distinct fixed points require distinct components of the interaction graph.",
    "reach the same fixed point",
    "A different effective law is not a different region of one world but a different component",
    "predicts no observable variation in the effective law",
    "What would be testable is the approach to a fixed point rather than the identity of one.",
    "The internal sector supplies no continuous moduli",
    "any variety among fixed points must come from the spectral exponent",
    "a property of how the population is connected rather than of what its agents are made of",
)
REQUIRED_CLAIMS = (
    "Connectivity fixes only the component decomposition",
    "rank classifies \\(M\\) alone",
    "relative invariants of the pair \\((A,M)\\)",
    "ratio \\(a/m\\)",
    "common scalar \\(\\zeta_\\ell\\) fixed exogenously",
    "block scalars \\(\\zeta_{\\ell,\\alpha}\\)",
    "depends only on its own block",
    "well defined on the residual-frame quotient",
    "Connectedness gives no converse",
    "uniqueness modulo the residual global frame action",
    "Multiple fixed objects or basins, cycles, and nonconvergent trajectories",
    "does not establish that coupled agents reach one effective law",
    "non-observability of alternative effective laws",
    "no renormalization-group flow",
)
CLAIM_IDS = (
    "AUD20-DEFECT-REPRODUCTION",
    "AUD20-CORRECTED-CONTRACT",
)
MATH_CRITERIA = (
    ("statement_precision", "statement precision"),
    ("definitions_and_domains", "definitions and domains"),
    ("assumptions", "assumptions"),
    ("derivation_validity", "derivation validity"),
    ("theorem_lemma_dependencies", "theorem or lemma dependencies"),
    ("limiting_cases", "limiting cases"),
    ("counterexample_search", "counterexample search"),
    ("notation_conclusion_agreement", "agreement between notation and conclusion"),
)
MATH_CRITERION_NAMES = tuple(label for _, label in MATH_CRITERIA)
PRIMARY_VIEW_FILES = (
    "views/01-dynamical-systems.json",
    "views/02-gauge-quotient.json",
    "views/03-evidence-code-integrity.json",
    "views/04-manuscript-source-and-status.json",
)
ESCALATION_VIEW_FILES = (
    "views/05-countermodel-boundary.json",
    "views/06-independent-symbolic-check.json",
    "views/07-publication-scope.json",
    "views/08-evidence-provenance.json",
)
REQUIRED_REVIEW_FILES = (
    *PRIMARY_VIEW_FILES,
    "views/skeptic.json",
    "views/adjudicator.json",
)
COMMON_PUBLIC_FILES = (
    "aud20-derivation.md",
    "baseline-warning-provenance.json",
    "claim-language.json",
    "command-records.json",
    "elbo-oracles.xml",
    "environment.json",
    "equation-byte-comparison.json",
    "evidence-tool-tests.xml",
    "privacy-manifest.json",
    "source-diff.json",
    "tex-build-summary.json",
    "tex-inputs.json",
)
BASE_COMMON_FILE_PATHS = tuple(
    sorted(COMMON_PUBLIC_FILES, key=lambda path: path.encode("ascii"))
)
BASE_COMMON_FILE_KINDS = {
    "aud20-derivation.md": "derivation",
    "baseline-warning-provenance.json": "mechanical",
    "claim-language.json": "mechanical",
    "command-records.json": "mechanical",
    "elbo-oracles.xml": "mechanical",
    "environment.json": "mechanical",
    "equation-byte-comparison.json": "derivation",
    "evidence-tool-tests.xml": "mechanical",
    "privacy-manifest.json": "mechanical",
    "source-diff.json": "mechanical",
    "tex-build-summary.json": "mechanical",
    "tex-inputs.json": "mechanical",
}
BASE_INDEX_FILE = "remediation-index.json"
CANDIDATE_DOMAIN_INDEX_FILE = "evidence-index.json"
CLOSURE_DOMAIN_INDEX_FILE = "closure-index.json"
PRE_REVIEW_FILE = "pre-review-manifest.json"
CANDIDATE_EVIDENCE_FILES = tuple(sorted(
    COMMON_PUBLIC_FILES + (BASE_INDEX_FILE, CANDIDATE_DOMAIN_INDEX_FILE)
))

AUD20_DERIVATION_TEXT = """# AUD-20 connectedness, quotient, and relative-invariant derivation

## 1. Connected support does not imply a unique attractor

On the admitted interval [0,1], let F(x)=3x^2-2x^3. Then

F(x)-x=x(1-x)(2x-1),
F'(x)=6x(1-x).

The fixed-point equation F(x)=x therefore has exactly x=0, x=1/2, and x=1.
Their derivatives are 0, 3/2, and 0. For 0<x<1/2, 0<=F(x)<x, so the iterates
decrease monotonically to a fixed point below 1/2 and hence to 0. For
1/2<x<1, x<F(x)<=1, so the iterates increase monotonically to a fixed point
above 1/2 and hence to 1. Thus 0 and 1 are attracting fixed points with distinct
basins separated by the repelling fixed point 1/2. One connected component can
therefore support multiple fixed objects and basin-dependent limits.

## 2. Component decomposition gives decoupling only under a local normalization

Let the interaction graph have connected components C_alpha and let the admitted
model space decompose as X=direct_sum_alpha X_alpha. If the unnormalized step
respects components, S_l=direct_sum_alpha S_{l,alpha}, and each positive
normalizer zeta_{l,alpha} is either fixed exogenously or depends only on the state
x_alpha of its own component, then

R_l(x)_alpha=zeta_{l,alpha}(x_alpha)^(-1) S_{l,alpha}(x_alpha),
R_l=direct_sum_alpha R_{l,alpha}.

This proves only componentwise evolution. If a normalizer for one block depends
on another block, the normalized map is not a direct sum even when S_l is block
diagonal. Neither block diagonal structure nor graph connectedness supplies
existence, uniqueness, attraction, convergence, or common-basin coverage inside
one component.

## 3. A quotient fixed-object claim requires descent of the map

Let H_alpha be the residual global frame group on component C_alpha. A component
map R_{l,alpha} defines a quotient map by

bar(R)_{l,alpha}([x])=[R_{l,alpha}(x)]

only if the right-hand side is independent of the representative x. Equivariance,
R_{l,alpha}(h action x)=h action R_{l,alpha}(x), is a sufficient condition; the
weaker necessary statement is that points in one H_alpha-orbit map into one
H_alpha-orbit. A fixed exogenous common scalar preserves this property, as do
gauge-invariant block scalars zeta_{l,alpha} whose alpha-th value depends only on
x_alpha, when S_{l,alpha} has it. Without this descent check, existence or
uniqueness on the residual-frame quotient is not a well-defined conclusion.

## 4. Rank of M alone does not classify the pair (A,M)

For K=1 with a>0 and m>0, the residual GL(1) frame h acts simultaneously by

(a,m) -> (h^2 a,h^2 m).

Therefore a/m is invariant. A common positive normalization also preserves it:
(a/zeta)/(m/zeta)=a/m. If two pairs (a,m) and (a',m') were in the same residual
orbit, then a'=h^2 a and m'=h^2 m, which implies a'/m'=a/m. Hence pairs with
different ratios are gauge inequivalent even though every positive scalar M has
rank one and lies in the single positive congruence class. Sylvester inertia or
rank classifies M alone; it does not exhaust the relative invariants of (A,M), the
fixed-object classes, or their possible continuous moduli.

## 5. Exact conclusions and falsifiers

The established conclusion is conditional componentwise decoupling under a
block-preserving step and either a fixed exogenous common scalar or block-indexed
scalars whose alpha-th value depends only on x_alpha. Graph
connectivity does not exhaust fixed-object variety. It proves none of existence,
quotient uniqueness, attraction, convergence, common-basin coverage, or
non-observability of alternative effective laws. A quotient statement additionally
requires a well-defined descended map, and classification of M alone cannot be
substituted for classification of the full model pair.

This derivation is falsified by any of the following: an algebraic error in the
factorization, derivatives, or monotone-basin argument for F; a residual GL(1)
frame that changes a/m; a simultaneous congruence relating two positive scalar
pairs with different a/m; or a proof that the stated normalized map remains a
direct sum while one output block genuinely depends on another block. Proving
equivariance and quotient descent for a specified map would discharge the
well-definedness prerequisite, but would not by itself prove a unique fixed orbit
or global attraction.
"""


@dataclass(frozen=True)
class PlannedArtifact:
    raw_sha256: str
    raw_size_bytes: int
    public_bytes: bytes
    public_sha256: str
    public_size_bytes: int
```

Implement the module in this exact order:

1. Canonical JSON uses sorted keys, compact separators, `allow_nan=False`, UTF-8,
   and one trailing newline. Every output is create-once except the gate-created
   empty ledger, which `populate_ledger` replaces exactly once after proving that
   it is the gate's unpopulated template.
2. `run_junit` is a Research-local, byte-equivalent adapter for frozen Wave 0
   `run-junit`. It requires interpreter `C:\Python314\python.exe`, a literal `--`
   before the remainder argv, that argv's exact `--junitxml=<declared raw path>`,
   absent output-record and JUnit paths, repository-relative CWD, and the exact
   six-key CPU environment. It invokes `subprocess.run(argv, shell=False,
   cwd=repo_root, env=validated_env)` and never parses console text. After exit it
   parses the created JUnit, records UTC bounds, and atomically creates the command
   record with exactly the frozen `remediation-command-record-v1` keys
   `schema_version`, `id`, `argv`, `cwd_rel`, `interpreter`, `env_allowlist`,
   `started_utc`, `ended_utc`, `exit_code`, and `junit`. The JUnit record contains
   path, size, SHA-256, exact totals, sorted unique testcase IDs, and their digest.
   Nonzero exit, preexisting output, env drift, schema drift, duplicate testcase,
   or JUnit mismatch fails closed. Conformance tests compare canonical output bytes
   to the frozen Wave 0 fixture, not merely a compatible-looking Python object.
   Wave E does not implement `resolve-verification-gate`. Task 1 and every gate use
   invoke frozen Wave 0 `tools/remediation_evidence.py resolve-verification-gate`
   directly with the frozen snapshot and explicit Codex root. The Research-local
   `validate_verification_binding` only rehashes the already resolved, privacy-safe
   Task 1 binding and requires exact records for `SKILL.md`,
   `references/contract.md`, `references/criteria-code.md`,
   `references/criteria-evidence.md`, `references/criteria-experiment.md`,
   `references/criteria-general.md`, `references/criteria-math.md`,
   `schemas/claim-ledger.schema.json`, and `scripts/verification_gate.py`. It
   cannot choose a root, discover a fallback, or create another verifier contract.
3. `plan_publication(raw_files, replacements, public_root)` reads every raw byte,
   computes all raw hashes/sizes, applies case-insensitive longest-root-first
   replacements for both slash forms entirely in memory, computes all planned
   public hashes/sizes, rejects username, computer name, raw-root text, absolute
   user-profile text, `process_id`, and `gate telemetry`, and returns
   `dict[str, PlannedArtifact]` without creating `public_root`.
   `commit_publication` requires relative planned paths and absent public/staging
   roots; writes only a unique sibling in sorted order; rereads and rehashes every
   byte; writes the base index, then the domain index last; and atomically renames
   the sibling. Failure removes only that newly created sibling.
4. `scan_raw(repo_root, raw_root, stage, tested_head,
   implementation_parent)` first enforces candidate `P/P` or closure `E/P`
   polarity, then creates exactly `claim-language.json`,
   `equation-byte-comparison.json`, `source-diff.json`, and
   `aud20-derivation.md`. The derivation bytes are exactly
   `AUD20_DERIVATION_TEXT.encode("utf-8")`, including its final LF. The language
   scan consumes only the durable ordered `FORBIDDEN_CLAIMS` and `REQUIRED_CLAIMS`
   constants, emits those exact arrays in `claim-language.json`, requires all eight
   forbidden items absent and every required item present, and rejects any list
   drift against the Task 2 oracle contract. Equation comparison hashes
   the nine ordered equation environments at `CONTEXT_COMMIT` and the tested head
   after CRLF-to-LF normalization. `source-diff.json` persists both
   `CONTEXT_COMMIT..P` and `CONTEXT_COMMIT..E` records with old/new commit, Git
   blob ID, byte size, SHA-256, mode, path, status, role, and exact allowed hunk
   coordinates. Every change record has exactly `path`, `status`, `role`,
   `old_blob`, `old_size_bytes`, `old_sha256`, `old_mode`, `new_blob`,
   `new_size_bytes`, `new_sha256`, and `new_mode`. At
   candidate `P/P`, the implementation and tested comparisons are intentionally
   byte-identical; at closure `E/P`, they bind distinct `P` and `E` heads. It
   requires `source_changes.modified` to contain exactly `TARGET_REL` then
   `ORACLE_REL`, both with complete old and new identities, and
   `source_changes.added` to contain exactly `TOOL_TEST_REL` then `TOOL_REL`, both
   with all four old identity fields null and complete new identities. The modified
   records carry the six manuscript one-line starts and exact oracle-test
   import/EOF append; the added records are whole-file additions. Baseline-to-`P`
   has exactly those four source changes and no evidence-only change.
   Baseline-to-`E` has the same source projection plus exactly the 14 ordered
   whole-file additions in `CANDIDATE_EVIDENCE_FILES`, each with null old identity,
   exact new identity, status `added`, and role
   `generated_evidence_output` and excluded from dependency/tested inputs. Any
   extra path/hunk, missing candidate addition, rename, mode change, equation
   change, or deletion rejects.
5. `collect_tex_inputs` parses every `PWD` and `INPUT` from the fresh root `.fls`,
   resolves relative inputs against their recorded PWD, rejects missing,
   nonregular, symlink/reparse, or ambiguous-case inputs, excludes only generated
   files strictly beneath the declared raw build root, and deduplicates by resolved
   case-folded path. There is no suffix allowlist: root/includes, classes, styles,
   TeX engine/configuration files, fonts, maps, and all other consumed inputs are
   hashed. `collect_bibtex_inputs` parses every `\\bibdata`/`\\bibstyle` name in
   `.aux`, requires matching `.blg` records, and runs the bound hashed `kpsewhich`
   as `[kpsewhich,"--progname=bibtex",filename]` for each exact `.bib`/`.bst`.
   It records resolver argv/CWD/exit/result and rejects missing or ambiguous
   resolution. Repository records enter source inputs; external distribution
   records enter dependency inputs; generated PDF/log/FLS/AUX/BLG/stdout bytes are
   evidence outputs only.
6. `write_environment` resolves and hashes exactly `sys.executable`, `latexmk`,
   `lualatex`, `bibtex`, and `kpsewhich`; records their complete version output;
   binds OS/release/architecture and Python implementation/version; and records
   NumPy, pytest, SymPy, all `pytest11` plugin distributions, and their METADATA/
   RECORD hashes when present. It records two closed environment maps: the exact
   six CPU keys from Global Constraints, and the TeX map containing `WINDIR`,
   `SystemRoot`, every listed `TEX*`, `BIB*`, `BST*`, and MiKTeX variable, with
   explicit nulls. Every TeX command is `latexmk -norc`; any rc discovery or argv,
   environment, executable, or version/hash drift rejects. The base index receives
   only the closed Wave 0 `remediation-environment-v1` projection with exact fields
   `platform`, `interpreter`, `dependency_versions`, `dependency_inputs`,
   and `environment_variables`. It has exactly those five fields; a
   `privacy_transform` field in the base environment rejects. TeX executables,
   TeX-variable maps, plugin metadata, recorder identities, privacy policy,
   privacy-manifest identity, and all other Research-specific detail remain solely
   in domain payloads referenced by `wave-e-domain-inventory-v1`.
7. `dependency_inputs` contains only external TeX/BibTeX inputs, Python
   distribution metadata, tracked ancestor dependency declarations, the frozen
   external Wave 0 verification snapshot/resolver identities, and every resolved
   active Codex SKILL/contract/five-criteria/schema/gate file. Verifier records use
   privacy-safe `$VERIFICATION_ROOT/...` aliases plus exact size/SHA-256 and bind
   the resolver output; none is copied into Research. It never
   contains raw/public evidence, reviews, JUnit, scans, equations, build outputs,
   baseline warning controls, privacy manifests, pre-review manifests, or indexes.
   Baseline-warning provenance is an evidence payload recording the planning
   contract, context commit, baseline command/environment, baseline FLS/AUX/BLG
   input identities, warning-normalization algorithm, warning bytes/hash, and the
   raw build artifact hashes. The builder rereads and validates that provenance;
   a naked warning text file is insufficient.
8. `collect_tested_inputs` emits the exact closed Wave 0 nested shape
   `{schema_version,selection_rules,exclusion_rules,inputs}`. The schema/version and
   ordered rule tuples are the three constants above. The canonical resolver calls
   `git ls-files -z` itself and selects every tracked `manuscripts/` path; `inputs`
   is the sorted exact `{path,size_bytes,sha256}` inventory. The SHA-256 of canonical
   compact JSON for `inputs` alone is `tested_input_inventory_sha256`.
   `source_config_bindings` is exactly six records, in
   `SOURCE_CONFIG_BINDING_PATHS` order, and every record must be the byte-identical
   member of `inputs` for that path. Omission, extra/reordered record, policy-key or
   rule drift, hash/digest drift, duplicate/case alias, symlink/reparse input,
   unsorted inventory, or matching untracked path rejects. Planning-contract,
   verifier, TeX-role, source-diff, and review provenance is richer Wave E domain
   data only; it must not add a field or record to the base policy/bindings.
9. The two JUnit parsers require unique sorted testcase IDs and exact totals:
   `elbo-oracles.xml` is `20/0/0/0`; `evidence-tool-tests.xml` is `14/0/0/0`.
   Both commands must be current records from `run_junit`. The environment is
   exactly `CUDA_VISIBLE_DEVICES="-1"`, the three CUDA opt-in keys null,
   `PYTHONHASHSEED="0"`, and explicit `PYTHONPATH`; no skip allowlist exists.
10. `validate_wave0_plan_bytes` requires SHA-256
    `dbe2263a3b0fe1e9f5db4ff1fca9a19f819cfd32ef38da71d6e5cb5485723ac2`.
    `validate_planning_release` parses the exact external
    `wave-e-planning-release-v1` bytes, rejects unknown/missing keys, requires the
    approved fetched planning commit/repository and exact Wave E
    path/Git-blob/size/SHA record, and requires its raw size/SHA to equal the Task 1
    binding. Neither function accepts a caller-supplied replacement digest.
11. `build_base_index` emits the frozen Wave 0 outer schema
    `remediation-evidence-v1` with exactly the 16 roots `schema_version`, `wave`,
    `evidence_stage`, `tested_git_head`, `implementation_parent_git_head`,
    `platform`, `environment_record`, `dependency_versions`, `dependency_inputs`,
    `tested_input_policy`, `tested_input_inventory_sha256`, `commands`,
    `source_config_bindings`, `reviewed_plan_binding`,
    `verification_contract_binding`, and `files`.
    `reviewed_plan_binding` is the exact Wave 0-compatible reviewed-plan record
    `{path,planning_commit,git_blob,size_bytes,sha256}` derived only after the
    approved release bytes validate. `verification_contract_binding` is the exact
    Task 1 snapshot/active-contract binding already revalidated by
    `validate_verification_binding`. `commands` contains the two exact Wave 0
    runner records. Candidate polarity is `P/P`; closure polarity is `E/P`.
    Unknown/missing root or nested keys reject.
12. The base `files` field is the canonical ASCII-path-sorted exact
    `{path,kind,size_bytes,sha256}` inventory of the twelve already planned
    `BASE_COMMON_FILE_PATHS` bytes. The builder constructs every common public byte
    first in a detached in-memory map, freezes those records, then constructs
    `remediation-index.json`; therefore the graph is acyclic. `files` must exclude
    `remediation-index.json`, `evidence-index.json`, `closure-index.json`,
    `pre-review-manifest.json`, and every review. The Wave E domain inventory owns
    the latter domain-only bytes. Any omitted/extra/duplicate/reordered record,
    index back-edge, wrong kind, or byte mutation rejects.
    The canonical base bytes are written as `remediation-index.json`.
    Validation invokes the frozen Wave 0 `tools/remediation_evidence.py validate`
    on those exact bytes and CWD, hashes the file before/after to prove no rewrite,
    and requires the Research validator to accept the identical bytes. Conformance
    tests run the frozen external validator against the positive file and every
    schema/policy/binding/environment/JUnit/files/planning-release negative; no
    same-module expected-byte fixture is eligible as the Wave 0 oracle.
13. `build_domain_inventory` emits the named extension
    `wave-e-domain-inventory-v1`, never a replacement base schema. Its exact keys
    are `schema_version`, `base_schema_version`, `wave`, `evidence_stage`,
    `tested_git_head`, `implementation_parent_git_head`, `privacy_policy`,
    `privacy_provenance`,
    `base_index`, `planning_sources`, `source_diff`, `tex_inputs`,
    `evidence_inventory`, `pre_review_manifest`, and `self_exclusion`. It binds
    `remediation-index.json`, planning commit/blob identities, exhaustive TeX and
    source-diff payloads, and every public artifact except itself. Candidate writes
    `evidence-index.json`; closure writes `closure-index.json`.
    `planning_sources` is the closed object
    `wave-e-planning-sources-v1` with exactly `schema_version`,
    `planning_commit`, `wave0_plan_sha256`, `planning_contract`,
    `planning_release_binding`, `planning_release_record`, `sources`,
    `verification_contract_inputs`, and `verification_contract`.
    `planning_contract` is exactly
    `{path_alias:"$PLANNING_CONTRACT",size_bytes,sha256}`; the remaining records
    are exact closure-bound copies of the Task 1 contract's four planning-source
    identities, exact Wave 0 plan pin, approved release bytes/content, two frozen
    snapshot/resolver identities, and nested nine-file active-verifier binding.
    It is domain provenance, not a replacement for either Wave 0 base binding.
    `privacy_provenance` is the exact
    `{path,size_bytes,sha256}` binding of the validated public
    `privacy-manifest.json`; raw replacement values never enter the base.
14. `freeze_review_inputs` runs only after closure JUnit, scans, source diff,
    derivation, environment, baseline provenance, TeX build/input collection,
    deterministic public planning, and `remediation-index.json` are complete, but
    before any reviewer is dispatched. Within one fail-closed planning operation it
    first create-once writes the canonical raw `remediation-index.json`, then
    create-once writes raw
    `pre-review-manifest.json` with exact raw and planned-public path/size/SHA-256
    inventories for every pre-review input, the base-index identity, head polarity,
    planning sources, and explicit self/review/final-index exclusions. It then
    rehashes every byte. Review production may add only review files. The final
    planner must recompute the same planned-public bytes and reject any frozen-byte
    mutation before it writes privacy or final domain-index bytes.
15. Review records have the closed keys `schema_version`, `role`, `view_id`,
    `tested_git_head`, `pre_review_manifest_sha256`, `prior_review_inputs`,
    `reviewed_paths`, `claim_scores`, `summary`, and `falsification_conditions`.
    Every primary/escalation view cites the exact pre-review manifest and has an
    empty `prior_review_inputs`. The skeptic cites it plus hashes of every required
    independent view. The adjudicator cites it plus hashes of all independent views
    and the skeptic. Each claim score contains the exact ordered `MATH_CRITERIA`
    catalog, with stable keys and the exact installed labels `statement precision`,
    `definitions and domains`, `assumptions`, `derivation validity`,
    `theorem or lemma dependencies`, `limiting cases`, `counterexample search`, and
    `agreement between notation and conclusion`. Every applicable criterion is scored and
    justified; no generic aggregate substitute is allowed. Each `claim_scores`
    entry has exactly `claim_id`, `decision`, `unresolved_disagreement`, and
    `criteria`; each criterion has exactly `key`, `label`, `score`, `evidence_ids`,
    and `rationale`, and its key/label pair must equal the catalog. Missing/stale hashes,
    mutation after citation,
    duplicate views, unknown evidence, or incomplete chain rejects. Disagreement
    after four requires all four escalation views; disagreement after eight is
    `INCONCLUSIVE`, never a vote-based pass.
16. `publish-bundle` validates raw scans, both JUnits/runner records, exact source
    diff, tested-input digest, planning bindings, TeX hard errors and baseline-
    warning provenance, PDF/log/FLS/AUX/BLG/stdout presence, exhaustive TeX/Bib
    identity, and stage-required reviews. Privacy planning occurs fully in memory.
    `privacy-manifest.json` records every raw and transformed artifact except
    itself, `remediation-index.json`, and the not-yet-written domain index, naming
    those exact exclusions. Candidate atomically publishes the exact 14-file set
    `COMMON_PUBLIC_FILES + (BASE_INDEX_FILE, CANDIDATE_DOMAIN_INDEX_FILE)`.
    Closure publishes the exact 21-file set `COMMON_PUBLIC_FILES +
    (BASE_INDEX_FILE, PRE_REVIEW_FILE) + REQUIRED_REVIEW_FILES +
    (CLOSURE_DOMAIN_INDEX_FILE,)`, or 25 files with all escalation views.
17. `validate_bundle` rejects unknown schema keys, wrong P/P or E/P polarity,
    non-direct `P..E`, any `P..E` path outside the exact candidate directory,
    extra/missing/modified public files, privacy leaks, input/tool/config drift,
    dependency/evidence overlap, review-chain drift, and baseline/TeX drift. It
    recomputes the base index, domain inventory, privacy transform, tested-input
    inventory digest, source diff, pre-review manifest, and exact allowlist.
    `closure-index.json` alone is self-excluded; the gate ledger later hashes it.
18. `populate_ledger` requires the gate's exact empty closure template, current
    HEAD equal to the closure index head, a validator-clean bundle, and the complete
    review hash chain. It writes exactly the Task 5 claims, preserves severity
    `high` and the gate artifact revision, uses target 4 or 8 with the specified
    deterministic escalation triggers, hashes the domain/base indexes and all
    eligible evidence, and validates the resulting ledger links. For each claim,
    it records the exact arithmetic mean of independent scores, the complete A/B
    and B/A pairwise comparison grid, and exactly one structured skeptic and one
    adjudicator; those two are never counted as independent views. Each ledger
    claim's aggregate `criteria`, each independent `views.scores[*].criteria`, and
    each ordered comparison `matches[*].criteria` covers exactly the eight installed
    mathematics labels above in the frozen order. Aggregate scores are the exact
    arithmetic means of corresponding independent-view scores. Gate records retain
    the installed `{name, score}` shape; the stable key-to-label catalog is frozen
    in the indexed Research evidence.
17. Both claims have domain `mathematics`. `AUD20-DEFECT-REPRODUCTION=REFUTED`
    requires current `supports:false` derivation counterevidence;
    `AUD20-CORRECTED-CONTRACT=EVIDENCE_VERIFIED` requires the current supporting
    derivation. Tests, source bytes, scans, equation records, and agent agreement
    are corroboration, not substitutes. Missing eligible evidence or any residual
    disagreement yields `INCONCLUSIVE` with a precise obligation.

Expose only these CLI forms; `argparse` rejects every unknown argument:

```text
wave_e_evidence.py run-junit --repo-root DIR --record FILE --junit FILE --id ID -- INTERPRETER -B -m pytest ... --junitxml=FILE
wave_e_evidence.py scan --stage candidate|closure --repo-root DIR --raw-root DIR --tested-head SHA --implementation-parent SHA
wave_e_evidence.py freeze-review-inputs --repo-root DIR --raw-root DIR --tested-head SHA --implementation-parent SHA --planning-contract FILE --planning-release FILE --baseline-provenance FILE
wave_e_evidence.py publish-bundle --stage candidate|closure --repo-root DIR --raw-root DIR --public-root DIR --tested-head SHA --implementation-parent SHA --planning-contract FILE --planning-release FILE --baseline-provenance FILE
wave_e_evidence.py validate-bundle --stage candidate|closure --repo-root DIR --raw-root DIR --bundle-root DIR --tested-head SHA --implementation-parent SHA
wave_e_evidence.py populate-ledger --repo-root DIR --ledger FILE --closure-index FILE --views-dir DIR
wave_e_evidence.py validate-ledger-links --repo-root DIR --ledger FILE --closure-index FILE
```

- [ ] **Step 4: Run builder GREEN, exact oracle GREEN, and cache-free in-memory compilation**

```powershell
$env:CUDA_VISIBLE_DEVICES = '-1'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
$env:PYTHONHASHSEED = '0'
& 'C:\Python314\python.exe' -B -m pytest `
    manuscripts\magent_elbo_whitepaper\verification\test_wave_e_evidence.py `
    -q -p no:cacheprovider `
    --junitxml=C:\tmp\magent-wave-e-tool-green.xml
if ($LASTEXITCODE -ne 0) { throw 'Wave E evidence-tool tests failed' }
[xml]$toolJUnit = Get-Content -Raw -LiteralPath 'C:\tmp\magent-wave-e-tool-green.xml'
$toolSuites = @($toolJUnit.testsuites.testsuite)
if ([int](($toolSuites | Measure-Object tests -Sum).Sum) -ne 14 -or
    [int](($toolSuites | Measure-Object failures -Sum).Sum) -ne 0 -or
    [int](($toolSuites | Measure-Object errors -Sum).Sum) -ne 0 -or
    [int](($toolSuites | Measure-Object skipped -Sum).Sum) -ne 0) {
    throw 'Wave E evidence-tool JUnit is not exactly 14/0/0/0'
}
& 'C:\Python314\python.exe' -B -m pytest `
    manuscripts\magent_elbo_whitepaper\verification\test_elbo_oracles.py `
    -q -p no:cacheprovider `
    --junitxml=C:\tmp\magent-wave-e-oracles-green.xml
if ($LASTEXITCODE -ne 0) { throw 'Wave E exact oracle tests failed' }
[xml]$oracleJUnit = Get-Content -Raw -LiteralPath 'C:\tmp\magent-wave-e-oracles-green.xml'
$oracleSuites = @($oracleJUnit.testsuites.testsuite)
if ([int](($oracleSuites | Measure-Object tests -Sum).Sum) -ne 20 -or
    [int](($oracleSuites | Measure-Object failures -Sum).Sum) -ne 0 -or
    [int](($oracleSuites | Measure-Object errors -Sum).Sum) -ne 0 -or
    [int](($oracleSuites | Measure-Object skipped -Sum).Sum) -ne 0) {
    throw 'Wave E oracle JUnit is not exactly 20/0/0/0'
}
$beforeCompile = @(& git status --porcelain=v2 --untracked-files=all)
$compileSource = @'
from pathlib import Path

for raw_path in (
    "manuscripts/magent_elbo_whitepaper/verification/wave_e_evidence.py",
    "manuscripts/magent_elbo_whitepaper/verification/test_wave_e_evidence.py",
):
    path = Path(raw_path)
    compile(path.read_text(encoding="utf-8"), str(path), "exec")
'@
& 'C:\Python314\python.exe' -B -c $compileSource
if ($LASTEXITCODE -ne 0) { throw 'Wave E evidence Python does not compile' }
$afterCompile = @(& git status --porcelain=v2 --untracked-files=all)
if (($beforeCompile -join "`n") -cne ($afterCompile -join "`n")) {
    throw 'In-memory compile created or changed repository bytes'
}
```

- [ ] **Step 5: Commit the exact four-path implementation parent**

```powershell
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'Wave E implementation whitespace check failed' }
$changed = @(& git status --porcelain=v1 | ForEach-Object { $_.Substring(3).Replace('\','/') }) | Sort-Object
$expectedChanged = @(
    'manuscripts/magent_elbo_whitepaper/08a_coarse_graining.tex',
    'manuscripts/magent_elbo_whitepaper/verification/test_elbo_oracles.py',
    'manuscripts/magent_elbo_whitepaper/verification/test_wave_e_evidence.py',
    'manuscripts/magent_elbo_whitepaper/verification/wave_e_evidence.py'
) | Sort-Object
if (Compare-Object $changed $expectedChanged) {
    throw 'Wave E implementation path ownership drift'
}
& git add -- $expectedChanged
& git commit -m 'docs: condition coarse fixed-point claim'
if ($LASTEXITCODE -ne 0) { throw 'Wave E implementation commit failed' }
$implHead = (& git rev-parse HEAD).Trim()
$implShort = (& git rev-parse --short=12 HEAD).Trim()
if ((& git status --porcelain).Count -ne 0) {
    throw 'Implementation parent is not clean'
}
"implementation_head=$implHead"
"implementation_short=$implShort"
```

---

### Task 4: Produce and commit durable candidate evidence

**Files:**

- Create outside Git first:
  `C:\tmp\magent-wave-e-candidate-$implShort-raw\` and its raw JUnit, scan,
  equation, TeX, stdout, command, and derivation records.
- Create only after the raw bundle is complete:
  `docs/verification/evidence/wave-e/$implShort/` with the exact 14-file
  candidate allowlist from Task 3.

**Interfaces:**

- Consumes: clean four-path implementation commit `P` from Task 3.
- Produces: a builder-validated candidate index before commit and a direct
  evidence-only child `E`; `P..E` contains only the candidate evidence directory.

- [ ] **Step 1: Create only the raw staging root and resolve all five executables**

```powershell
$waveWorktree = 'C:\Users\chris and christine\Documents\ChatGPT\MultiAgentELBO\.superpowers\worktrees\Research-magent-aud20-remediation-20260811'
if ((Resolve-Path '.').Path -cne (Resolve-Path $waveWorktree).Path) {
    throw 'Task 4 must run from the dedicated Wave E Research worktree'
}
$implHead = (& git rev-parse HEAD).Trim()
$implShort = (& git rev-parse --short=12 HEAD).Trim()
$candidateRaw = "C:\tmp\magent-wave-e-candidate-$implShort-raw"
$candidateBuild = Join-Path $candidateRaw 'tex-build'
$candidateDir = "docs\verification\evidence\wave-e\$implShort"
$evidenceTool = 'manuscripts\magent_elbo_whitepaper\verification\wave_e_evidence.py'
$planningContract = 'C:\tmp\magent-wave-e-planning-contract.json'
$planningRelease = 'C:\tmp\magent-wave-e-planning-release.json'
$baselineProvenance = 'C:\tmp\magent-wave-e-baseline-warning-provenance.json'
foreach ($path in @($candidateRaw, $candidateDir)) {
    if (Test-Path -LiteralPath $path) { throw "Preexisting candidate path: $path" }
}
foreach ($path in @($planningContract, $planningRelease, $baselineProvenance)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Required frozen Task 1 input is missing: $path"
    }
}
$planningPayload = Get-Content -Raw -LiteralPath $planningContract | ConvertFrom-Json
$planningSnapshot = "C:\tmp\magent-wave-e-planning-snapshot-$($planningPayload.planning_commit.Substring(0,12))"
$wave0Validator = Join-Path $planningSnapshot 'tools\remediation_evidence.py'
if (-not (Test-Path -LiteralPath $wave0Validator -PathType Leaf)) {
    throw 'Frozen Wave 0 validator is missing from the bound planning snapshot'
}
New-Item -ItemType Directory -Path $candidateBuild -Force | Out-Null
$pythonExe = (Resolve-Path 'C:\Python314\python.exe').Path
$latexmkExe = (Get-Command latexmk -CommandType Application -ErrorAction Stop).Source
$lualatexExe = (Get-Command lualatex -CommandType Application -ErrorAction Stop).Source
$bibtexExe = (Get-Command bibtex -CommandType Application -ErrorAction Stop).Source
$kpsewhichExe = (Get-Command kpsewhich -CommandType Application -ErrorAction Stop).Source
foreach ($path in @($pythonExe,$latexmkExe,$lualatexExe,$bibtexExe,$kpsewhichExe)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Resolved executable is not a file: $path"
    }
}
$env:CUDA_VISIBLE_DEVICES = '-1'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
$env:PYTHONHASHSEED = '0'
```

At this point `git status --porcelain` remains empty and `$candidateDir` does not
exist. The raw root is outside the Research repository.

- [ ] **Step 2: Run both cache-free JUnit commands into raw staging**

```powershell
$candidateCpuEnvironment = [ordered]@{
    CUDA_VISIBLE_DEVICES = $env:CUDA_VISIBLE_DEVICES
    MULTIAGENTELBO_RUN_CUDA_TESTS = $null
    VFE3_TEST_DEVICE = $null
    CUBLAS_WORKSPACE_CONFIG = $null
    PYTHONHASHSEED = $env:PYTHONHASHSEED
    PYTHONPATH = if (Test-Path Env:PYTHONPATH) { $env:PYTHONPATH } else { $null }
}
& $pythonExe -B $evidenceTool run-junit --repo-root . `
    --record "$candidateRaw\elbo-oracles.command.json" `
    --junit "$candidateRaw\elbo-oracles.xml" --id elbo-oracles -- `
    $pythonExe -B -m pytest `
    manuscripts\magent_elbo_whitepaper\verification\test_elbo_oracles.py `
    -q -p no:cacheprovider `
    "--junitxml=$candidateRaw\elbo-oracles.xml"
if ($LASTEXITCODE -ne 0) { throw 'Candidate oracle JUnit/record failed' }

& $pythonExe -B $evidenceTool run-junit --repo-root . `
    --record "$candidateRaw\evidence-tool-tests.command.json" `
    --junit "$candidateRaw\evidence-tool-tests.xml" --id evidence-tool-tests -- `
    $pythonExe -B -m pytest `
    manuscripts\magent_elbo_whitepaper\verification\test_wave_e_evidence.py `
    -q -p no:cacheprovider `
    "--junitxml=$candidateRaw\evidence-tool-tests.xml"
if ($LASTEXITCODE -ne 0) { throw 'Candidate evidence-tool JUnit/record failed' }
```

The first raw XML must later parse as exactly `20/0/0/0`; the second as exactly
`14/0/0/0`. There is no permitted skip. Both adjacent command records must be
create-once canonical `remediation-command-record-v1` bytes from the adapter; no
manually reconstructed command JSON or console-derived total is accepted.

- [ ] **Step 3: Write the raw claim scan, equation comparison, and derivation**

```powershell
& $pythonExe -B $evidenceTool scan --stage candidate `
    --repo-root . --raw-root $candidateRaw `
    --tested-head $implHead --implementation-parent $implHead
if ($LASTEXITCODE -ne 0) { throw 'Candidate raw scan/equation gate failed' }
if (Test-Path -LiteralPath $candidateDir) {
    throw 'Scan created public candidate evidence before privacy planning'
}
```

- [ ] **Step 4: Build the root TeX entry point with recorder output in raw staging**

```powershell
$env:WINDIR = $env:SystemRoot
$candidateTexEnvironment = [ordered]@{
    WINDIR = $env:WINDIR
    SystemRoot = $env:SystemRoot
    TEXINPUTS = if (Test-Path Env:TEXINPUTS) { $env:TEXINPUTS } else { $null }
    BIBINPUTS = if (Test-Path Env:BIBINPUTS) { $env:BIBINPUTS } else { $null }
    BSTINPUTS = if (Test-Path Env:BSTINPUTS) { $env:BSTINPUTS } else { $null }
    TEXMF = if (Test-Path Env:TEXMF) { $env:TEXMF } else { $null }
    TEXMFHOME = if (Test-Path Env:TEXMFHOME) { $env:TEXMFHOME } else { $null }
    TEXMFLOCAL = if (Test-Path Env:TEXMFLOCAL) { $env:TEXMFLOCAL } else { $null }
    TEXMFCNF = if (Test-Path Env:TEXMFCNF) { $env:TEXMFCNF } else { $null }
    TEXMFVAR = if (Test-Path Env:TEXMFVAR) { $env:TEXMFVAR } else { $null }
    TEXMFCONFIG = if (Test-Path Env:TEXMFCONFIG) { $env:TEXMFCONFIG } else { $null }
    TEXMFOUTPUT = if (Test-Path Env:TEXMFOUTPUT) { $env:TEXMFOUTPUT } else { $null }
    MIKTEX_USERCONFIG = if (Test-Path Env:MIKTEX_USERCONFIG) { $env:MIKTEX_USERCONFIG } else { $null }
    MIKTEX_USERDATA = if (Test-Path Env:MIKTEX_USERDATA) { $env:MIKTEX_USERDATA } else { $null }
    MIKTEX_USERINSTALL = if (Test-Path Env:MIKTEX_USERINSTALL) { $env:MIKTEX_USERINSTALL } else { $null }
    MIKTEX_COMMONCONFIG = if (Test-Path Env:MIKTEX_COMMONCONFIG) { $env:MIKTEX_COMMONCONFIG } else { $null }
    MIKTEX_COMMONDATA = if (Test-Path Env:MIKTEX_COMMONDATA) { $env:MIKTEX_COMMONDATA } else { $null }
    MIKTEX_COMMONINSTALL = if (Test-Path Env:MIKTEX_COMMONINSTALL) { $env:MIKTEX_COMMONINSTALL } else { $null }
}
$texStarted = [DateTime]::UtcNow.ToString('o')
Push-Location 'manuscripts'
try {
    & $latexmkExe -norc -gg -lualatex -bibtex -recorder `
        -interaction=nonstopmode -halt-on-error -file-line-error `
        "-outdir=$candidateBuild" MAgent_exact_elbo_whitepaper.tex `
        *> "$candidateRaw\tex.stdout.log"
    $texExit = $LASTEXITCODE
} finally {
    Pop-Location
}
$texEnded = [DateTime]::UtcNow.ToString('o')
if ($texExit -ne 0) { throw 'Candidate root TeX build failed' }
foreach ($name in @(
    'MAgent_exact_elbo_whitepaper.pdf',
    'MAgent_exact_elbo_whitepaper.log',
    'MAgent_exact_elbo_whitepaper.fls',
    'MAgent_exact_elbo_whitepaper.aux',
    'MAgent_exact_elbo_whitepaper.blg'
)) {
    if (-not (Test-Path -LiteralPath (Join-Path $candidateBuild $name) -PathType Leaf)) {
        throw "Candidate root build did not create $name"
    }
}
[ordered]@{schema_version='wave-e-tex-command-raw-v1';id='root-tex';cwd_rel='manuscripts';cpu_environment_variables=$candidateCpuEnvironment;tex_environment_variables=$candidateTexEnvironment;started_utc=$texStarted;ended_utc=$texEnded;exit_code=$texExit;argv=@($latexmkExe,'-norc','-gg','-lualatex','-bibtex','-recorder','-interaction=nonstopmode','-halt-on-error','-file-line-error',"-outdir=$candidateBuild",'MAgent_exact_elbo_whitepaper.tex')} |
    ConvertTo-Json -Depth 6 | Set-Content -LiteralPath `
        "$candidateRaw\tex-command-record.json" -Encoding utf8NoBOM
```

- [ ] **Step 5: Compute all raw hashes/transforms, then publish and index once**

```powershell
if (Test-Path -LiteralPath $candidateDir) {
    throw 'Candidate public directory exists before publish-bundle'
}
& $pythonExe -B $evidenceTool publish-bundle `
    --stage candidate --repo-root . --raw-root $candidateRaw `
    --public-root $candidateDir --tested-head $implHead `
    --implementation-parent $implHead `
    --planning-contract $planningContract `
    --planning-release $planningRelease `
    --baseline-provenance $baselineProvenance
if ($LASTEXITCODE -ne 0) { throw 'Candidate privacy publication/index failed' }
```

The builder computes every raw hash and every transformed byte before creating
`$candidateDir`; writes the twelve common public payloads, then the Wave 0 base
`remediation-index.json`, and writes `evidence-index.json` last. The PDF and raw
log/FLS/AUX/BLG/stdout bytes remain
only in staging; their exact raw hashes enter the privacy and build summaries.

- [ ] **Step 6: Validate the candidate index, exact allowlist, and privacy before commit**

```powershell
& $pythonExe -B $evidenceTool validate-bundle `
    --stage candidate --repo-root . --raw-root $candidateRaw `
    --bundle-root $candidateDir --tested-head $implHead `
    --implementation-parent $implHead
if ($LASTEXITCODE -ne 0) { throw 'Candidate bundle validation failed' }
$candidateBaseIndex = Join-Path $candidateDir 'remediation-index.json'
$candidateBaseBefore = (
    Get-FileHash -Algorithm SHA256 -LiteralPath $candidateBaseIndex
).Hash
& $pythonExe -B $wave0Validator validate $candidateBaseIndex --cwd .
if ($LASTEXITCODE -ne 0) {
    throw 'Frozen Wave 0 validator rejected the candidate base index'
}
$candidateBaseAfter = (
    Get-FileHash -Algorithm SHA256 -LiteralPath $candidateBaseIndex
).Hash
if ($candidateBaseBefore -cne $candidateBaseAfter) {
    throw 'Frozen Wave 0 candidate validation rewrote the base index'
}
foreach ($secret in @($env:USERNAME,$env:COMPUTERNAME,$waveWorktree,$candidateRaw)) {
    if ([string]::IsNullOrWhiteSpace($secret)) { continue }
    & rg -n --fixed-strings -- $secret $candidateDir
    if ($LASTEXITCODE -eq 0) { throw "Candidate privacy leak: $secret" }
    if ($LASTEXITCODE -ne 1) { throw 'Candidate privacy scan execution failed' }
}
& rg -n -i -- 'C:\\Users\\|process.?id|gate telemetry' $candidateDir
if ($LASTEXITCODE -eq 0) { throw 'Candidate generic privacy scan failed' }
if ($LASTEXITCODE -ne 1) { throw 'Candidate generic privacy scan did not execute' }
```

This validation is mandatory before `git add`. The index must bind every root-TeX
`.fls` input, every `.aux`/`.blg`-resolved bibliography and BST input, the four
Python source/test/tool inputs, all five executable records, dependency metadata,
both JUnits, scans, equation comparison, derivation, build summary, privacy
provenance, and exact candidate file inventory. Generated evidence appears only
in the evidence inventory, never in dependency inputs.

- [ ] **Step 7: Commit the direct evidence-only child**

```powershell
& git add -- $candidateDir
$candidatePrefix = ($candidateDir -replace '\\','/') + '/'
$candidateChanges = @(& git diff --cached --name-only)
if ($candidateChanges.Count -ne 14) {
    throw "Candidate evidence must contain exactly 14 files, found $($candidateChanges.Count)"
}
if (@($candidateChanges | Where-Object { -not $_.StartsWith($candidatePrefix, [StringComparison]::Ordinal) }).Count -ne 0) {
    throw 'Evidence child contains a noncandidate path'
}
$expectedCandidateRelative = @(
    'aud20-derivation.md',
    'baseline-warning-provenance.json',
    'claim-language.json',
    'command-records.json',
    'elbo-oracles.xml',
    'environment.json',
    'equation-byte-comparison.json',
    'evidence-index.json',
    'evidence-tool-tests.xml',
    'privacy-manifest.json',
    'remediation-index.json',
    'source-diff.json',
    'tex-build-summary.json',
    'tex-inputs.json'
) | Sort-Object
$candidateRelative = @(
    $candidateChanges | ForEach-Object { $_.Substring($candidatePrefix.Length) } |
        Sort-Object
)
if (Compare-Object $expectedCandidateRelative $candidateRelative) {
    throw 'Staged candidate evidence is not the exact 14-file allowlist'
}
& git commit -m 'docs: record Wave E candidate evidence'
if ($LASTEXITCODE -ne 0) { throw 'Evidence-only child commit failed' }
$evidenceHead = (& git rev-parse HEAD).Trim()
$evidenceShort = (& git rev-parse --short=12 HEAD).Trim()
$parentOfEvidence = (& git rev-parse HEAD^).Trim()
if ($parentOfEvidence -cne $implHead) {
    throw 'Evidence commit is not the direct child of the implementation commit'
}
$candidateDiff = @(& git diff --name-only "$implHead..$evidenceHead")
if (@($candidateDiff | Where-Object { -not $_.StartsWith($candidatePrefix, [StringComparison]::Ordinal) }).Count -ne 0) {
    throw 'P..E contains a noncandidate path'
}
if ((& git status --porcelain).Count -ne 0) {
    throw 'Evidence child is not clean'
}
```

Expected: clean direct child `E` whose only delta from `P` is the already
validated 14-file candidate bundle.

---

### Task 5: Close AUD-20 at the exact evidence child `E`

**Files:**

- Create outside the repository first:
  `C:\tmp\magent-wave-e-closure-$evidenceShort-raw\` with fresh JUnit,
  stdout, scan, equation, derivation, TeX, recorder, command, and raw review files.
- Create only after all raw evidence and reviews pass:
  `verification-evidence/wave-e/$evidenceShort/` with exactly 21 files, or 25
  when the frozen four-view escalation is triggered.
- Create gate-owned local control-plane state only after closure indexing:
  `.verification/wave-e/final-ledger.json` and gate-owned
  `.verification/active.json`.

**Interfaces:**

- Consumes: clean direct evidence child `E`, implementation parent `P`, and the
  already validated durable candidate bundle named for `P`.
- Produces: fresh exact-child Research oracle/tool JUnit, language/equation/
  derivation records, root TeX build and exhaustive input identity, four or eight
  independent views, one skeptic, one adjudicator, a closed closure index, and a
  validated Research-only ledger.
- Closes: `AUD20-DEFECT-REPRODUCTION=REFUTED` and
  `AUD20-CORRECTED-CONTRACT=EVIDENCE_VERIFIED` only when current eligible evidence
  at `E` supports those states. Both are `mathematics` claims: the former closes
  only with current derivation/formal-proof counterevidence, and the latter closes
  only with a current supporting derivation/formal proof. Any gap is `INCONCLUSIVE`
  and blocks Task 6.

- [ ] **Step 1: Resolve `E/P`, require a clean child, and create only raw staging**

```powershell
$ErrorActionPreference = 'Stop'
$waveWorktree = 'C:\Users\chris and christine\Documents\ChatGPT\MultiAgentELBO\.superpowers\worktrees\Research-magent-aud20-remediation-20260811'
if ((Resolve-Path '.').Path -cne (Resolve-Path $waveWorktree).Path) {
    throw 'Task 5 must run from the dedicated Wave E Research worktree'
}
$evidenceHead = (& git rev-parse HEAD).Trim()
$implHead = (& git rev-parse HEAD^).Trim()
$evidenceShort = $evidenceHead.Substring(0,12)
$implShort = $implHead.Substring(0,12)
$candidateDir = "docs\verification\evidence\wave-e\$implShort"
$candidateIndex = Join-Path $candidateDir 'evidence-index.json'
$candidateBaseIndex = Join-Path $candidateDir 'remediation-index.json'
$closureRaw = "C:\tmp\magent-wave-e-closure-$evidenceShort-raw"
$closureBuild = Join-Path $closureRaw 'tex-build'
$closureDir = "verification-evidence\wave-e\$evidenceShort"
$evidenceTool = 'manuscripts\magent_elbo_whitepaper\verification\wave_e_evidence.py'
$planningContract = 'C:\tmp\magent-wave-e-planning-contract.json'
$planningRelease = 'C:\tmp\magent-wave-e-planning-release.json'
$baselineProvenance = 'C:\tmp\magent-wave-e-baseline-warning-provenance.json'

if ((& git status --porcelain).Count -ne 0) {
    throw 'Evidence child E is not clean before closure'
}
foreach ($path in @(
    $candidateIndex,$candidateBaseIndex,$planningContract,$planningRelease,
    $baselineProvenance
)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Required candidate/Task 1 contract input is missing: $path"
    }
}
$planningPayload = Get-Content -Raw -LiteralPath $planningContract | ConvertFrom-Json
$planningSnapshot = "C:\tmp\magent-wave-e-planning-snapshot-$($planningPayload.planning_commit.Substring(0,12))"
$wave0Validator = Join-Path $planningSnapshot 'tools\remediation_evidence.py'
if (-not (Test-Path -LiteralPath $wave0Validator -PathType Leaf)) {
    throw 'Frozen Wave 0 validator is missing from the bound planning snapshot'
}
if ((& git rev-parse "$evidenceHead^").Trim() -cne $implHead) {
    throw 'E is not the direct child of P'
}
& git merge-base --is-ancestor `
    c9f237d2ca54c274ba5760012e62823a69d203a3 $evidenceHead
if ($LASTEXITCODE -ne 0) { throw 'E does not descend from the pinned Research context' }

$candidatePrefix = ($candidateDir -replace '\\','/') + '/'
$candidateDiff = @(& git diff --name-only "$implHead..$evidenceHead")
if ($candidateDiff.Count -ne 14) {
    throw 'P..E is not the exact 14-file candidate child'
}
if (@($candidateDiff | Where-Object {
    -not $_.StartsWith($candidatePrefix,[StringComparison]::Ordinal)
}).Count -ne 0) {
    throw 'P..E contains a noncandidate path'
}
$expectedCandidateRelative = @(
    'aud20-derivation.md',
    'baseline-warning-provenance.json',
    'claim-language.json',
    'command-records.json',
    'elbo-oracles.xml',
    'environment.json',
    'equation-byte-comparison.json',
    'evidence-index.json',
    'evidence-tool-tests.xml',
    'privacy-manifest.json',
    'remediation-index.json',
    'source-diff.json',
    'tex-build-summary.json',
    'tex-inputs.json'
) | Sort-Object
$candidateRelative = @(
    $candidateDiff | ForEach-Object { $_.Substring($candidatePrefix.Length) } |
        Sort-Object
)
if (Compare-Object $expectedCandidateRelative $candidateRelative) {
    throw 'P..E candidate paths do not equal the indexed 14-file allowlist'
}
$candidatePayload = Get-Content -Raw -LiteralPath $candidateIndex | ConvertFrom-Json
$candidateBasePayload = Get-Content -Raw -LiteralPath $candidateBaseIndex | ConvertFrom-Json
if ($candidatePayload.evidence_stage -ne 'candidate' -or
    $candidatePayload.tested_git_head -cne $implHead -or
    $candidatePayload.implementation_parent_git_head -cne $implHead -or
    $candidateBasePayload.schema_version -cne 'remediation-evidence-v1' -or
    $candidateBasePayload.evidence_stage -cne 'candidate' -or
    $candidateBasePayload.tested_git_head -cne $implHead -or
    $candidateBasePayload.implementation_parent_git_head -cne $implHead) {
    throw 'Candidate P/P head polarity is invalid'
}
foreach ($path in @($closureRaw,$closureDir)) {
    if (Test-Path -LiteralPath $path) { throw "Preexisting closure path: $path" }
}

$pythonExe = (Resolve-Path 'C:\Python314\python.exe').Path
$latexmkExe = (Get-Command latexmk -CommandType Application -ErrorAction Stop).Source
$lualatexExe = (Get-Command lualatex -CommandType Application -ErrorAction Stop).Source
$bibtexExe = (Get-Command bibtex -CommandType Application -ErrorAction Stop).Source
$kpsewhichExe = (Get-Command kpsewhich -CommandType Application -ErrorAction Stop).Source
foreach ($path in @($pythonExe,$latexmkExe,$lualatexExe,$bibtexExe,$kpsewhichExe)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Resolved executable is not a regular file: $path"
    }
}
$candidateBaseBefore = (
    Get-FileHash -Algorithm SHA256 -LiteralPath $candidateBaseIndex
).Hash
& $pythonExe -B $wave0Validator validate $candidateBaseIndex --cwd .
if ($LASTEXITCODE -ne 0) {
    throw 'Frozen Wave 0 validator rejected the consumed candidate base index'
}
$candidateBaseAfter = (
    Get-FileHash -Algorithm SHA256 -LiteralPath $candidateBaseIndex
).Hash
if ($candidateBaseBefore -cne $candidateBaseAfter) {
    throw 'Frozen Wave 0 validation rewrote the consumed candidate base index'
}
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'
New-Item -ItemType Directory -Path $closureBuild | Out-Null
if (Test-Path -LiteralPath $closureDir) {
    throw 'Creating raw staging unexpectedly created public closure bytes'
}
```

- [ ] **Step 2: Rerun both exact cache-free JUnit commands at `E`**

```powershell
$cpuEnvironment = [ordered]@{
    CUDA_VISIBLE_DEVICES = $env:CUDA_VISIBLE_DEVICES
    MULTIAGENTELBO_RUN_CUDA_TESTS = $null
    VFE3_TEST_DEVICE = $null
    CUBLAS_WORKSPACE_CONFIG = $null
    PYTHONHASHSEED = $env:PYTHONHASHSEED
    PYTHONPATH = if (Test-Path Env:PYTHONPATH) { $env:PYTHONPATH } else { $null }
}

& $pythonExe -B $evidenceTool run-junit --repo-root . `
    --record "$closureRaw\elbo-oracles.command.json" `
    --junit "$closureRaw\elbo-oracles.xml" --id elbo-oracles -- `
    $pythonExe -B -m pytest `
    manuscripts\magent_elbo_whitepaper\verification\test_elbo_oracles.py `
    -q -p no:cacheprovider `
    "--junitxml=$closureRaw\elbo-oracles.xml"
if ($LASTEXITCODE -ne 0) { throw 'Closure oracle JUnit/record failed' }

& $pythonExe -B $evidenceTool run-junit --repo-root . `
    --record "$closureRaw\evidence-tool-tests.command.json" `
    --junit "$closureRaw\evidence-tool-tests.xml" --id evidence-tool-tests -- `
    $pythonExe -B -m pytest `
    manuscripts\magent_elbo_whitepaper\verification\test_wave_e_evidence.py `
    -q -p no:cacheprovider `
    "--junitxml=$closureRaw\evidence-tool-tests.xml"
if ($LASTEXITCODE -ne 0) { throw 'Closure evidence-tool JUnit/record failed' }
```

These are new `E` runs, not copied candidate XML. The first command is the design's
exact cache-free `test_elbo_oracles.py` command and must parse as `20/0/0/0`; the
second must parse as `14/0/0/0`. Both require unique testcase IDs, exit zero, and no
skip. The builder records raw/public SHA-256, sizes, testcase-ID digests, UTC bounds,
exact ordered argv, interpreter identity, relative CWD, and the six-key environment.

- [ ] **Step 3: Recompute the language, equation, and derivation records at `E`**

```powershell
& $pythonExe -B $evidenceTool scan --stage closure `
    --repo-root . --raw-root $closureRaw `
    --tested-head $evidenceHead --implementation-parent $implHead
if ($LASTEXITCODE -ne 0) { throw 'Closure raw scan/equation gate failed' }
if (Test-Path -LiteralPath $closureDir) {
    throw 'Closure scan created public bytes before review-complete planning'
}
```

The scan must freshly derive all three raw records at `E`; it cannot copy the
candidate files. It requires every forbidden phrase absent, every required status
phrase present, all nine ordered equation environments byte-identical to
`c9f237d2` after only CRLF/LF normalization, and both exact countermodels recorded
with their algebraic consequences.

- [ ] **Step 4: Build the root manuscript afresh with recorder output at `E`**

```powershell
if (-not (Test-Path -LiteralPath $baselineProvenance -PathType Leaf)) {
    throw 'Pinned c9f237d2 baseline-warning provenance is missing'
}
$baselineProvenanceHash = (
    Get-FileHash -Algorithm SHA256 -LiteralPath $baselineProvenance
).Hash
$env:WINDIR = $env:SystemRoot
$texEnvironment = [ordered]@{
    WINDIR = $env:WINDIR
    SystemRoot = $env:SystemRoot
    TEXINPUTS = if (Test-Path Env:TEXINPUTS) { $env:TEXINPUTS } else { $null }
    BIBINPUTS = if (Test-Path Env:BIBINPUTS) { $env:BIBINPUTS } else { $null }
    BSTINPUTS = if (Test-Path Env:BSTINPUTS) { $env:BSTINPUTS } else { $null }
    TEXMF = if (Test-Path Env:TEXMF) { $env:TEXMF } else { $null }
    TEXMFHOME = if (Test-Path Env:TEXMFHOME) { $env:TEXMFHOME } else { $null }
    TEXMFLOCAL = if (Test-Path Env:TEXMFLOCAL) { $env:TEXMFLOCAL } else { $null }
    TEXMFCNF = if (Test-Path Env:TEXMFCNF) { $env:TEXMFCNF } else { $null }
    TEXMFVAR = if (Test-Path Env:TEXMFVAR) { $env:TEXMFVAR } else { $null }
    TEXMFCONFIG = if (Test-Path Env:TEXMFCONFIG) { $env:TEXMFCONFIG } else { $null }
    TEXMFOUTPUT = if (Test-Path Env:TEXMFOUTPUT) { $env:TEXMFOUTPUT } else { $null }
    MIKTEX_USERCONFIG = if (Test-Path Env:MIKTEX_USERCONFIG) { $env:MIKTEX_USERCONFIG } else { $null }
    MIKTEX_USERDATA = if (Test-Path Env:MIKTEX_USERDATA) { $env:MIKTEX_USERDATA } else { $null }
    MIKTEX_USERINSTALL = if (Test-Path Env:MIKTEX_USERINSTALL) { $env:MIKTEX_USERINSTALL } else { $null }
    MIKTEX_COMMONCONFIG = if (Test-Path Env:MIKTEX_COMMONCONFIG) { $env:MIKTEX_COMMONCONFIG } else { $null }
    MIKTEX_COMMONDATA = if (Test-Path Env:MIKTEX_COMMONDATA) { $env:MIKTEX_COMMONDATA } else { $null }
    MIKTEX_COMMONINSTALL = if (Test-Path Env:MIKTEX_COMMONINSTALL) { $env:MIKTEX_COMMONINSTALL } else { $null }
}
$texStarted = [DateTime]::UtcNow.ToString('o')
Push-Location 'manuscripts'
try {
    & $latexmkExe -norc -gg -lualatex -bibtex -recorder `
        -interaction=nonstopmode -halt-on-error -file-line-error `
        "-outdir=$closureBuild" MAgent_exact_elbo_whitepaper.tex `
        *> "$closureRaw\tex.stdout.log"
    $texExit = $LASTEXITCODE
} finally {
    Pop-Location
}
$texEnded = [DateTime]::UtcNow.ToString('o')
if ($texExit -ne 0) { throw 'Closure root TeX build failed' }
foreach ($name in @(
    'MAgent_exact_elbo_whitepaper.pdf',
    'MAgent_exact_elbo_whitepaper.log',
    'MAgent_exact_elbo_whitepaper.fls',
    'MAgent_exact_elbo_whitepaper.aux',
    'MAgent_exact_elbo_whitepaper.blg'
)) {
    if (-not (Test-Path -LiteralPath (Join-Path $closureBuild $name) -PathType Leaf)) {
        throw "Closure root build did not create $name"
    }
}
[ordered]@{
    schema_version = 'wave-e-tex-command-raw-v1'
    id = 'root-tex'
    cwd_rel = 'manuscripts'
    cpu_environment_variables = $cpuEnvironment
    tex_environment_variables = $texEnvironment
    started_utc = $texStarted
    ended_utc = $texEnded
    exit_code = $texExit
    baseline_warning_provenance_sha256 = $baselineProvenanceHash
    argv = @($latexmkExe,'-norc','-gg','-lualatex','-bibtex','-recorder','-interaction=nonstopmode','-halt-on-error','-file-line-error',"-outdir=$closureBuild",'MAgent_exact_elbo_whitepaper.tex')
} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath `
    "$closureRaw\tex-command-record.json" -Encoding utf8NoBOM
```

The later builder requires zero hard TeX errors, undefined citations/references,
multiply defined labels, and rerun requests; an exact normalized warning inventory
equal to the warning bytes bound by the validated `c9f237d2` provenance; and a
nonempty PDF. It hashes the PDF, log, FLS, AUX, BLG, stdout, and full baseline-
warning provenance as evidence outputs. It parses
the `.fls` plus `.aux`/`.blg`, resolves the bibliography and BST through the bound
`kpsewhich`, and binds every repository and TeX-distribution input. It never treats
the PDF, logs, control, summaries, or other generated evidence as dependencies.

- [ ] **Step 5: Freeze immutable pre-review raw and planned-public bytes**

No reviewer may be dispatched until the exact mechanical, mathematical, source,
environment, and TeX inputs they will assess are frozen:

```powershell
$preReviewManifest = Join-Path $closureRaw 'pre-review-manifest.json'
& $pythonExe -B $evidenceTool freeze-review-inputs `
    --repo-root . --raw-root $closureRaw `
    --tested-head $evidenceHead --implementation-parent $implHead `
    --planning-contract $planningContract `
    --planning-release $planningRelease `
    --baseline-provenance $baselineProvenance
if ($LASTEXITCODE -ne 0) { throw 'Pre-review evidence freeze failed' }
if (-not (Test-Path -LiteralPath $preReviewManifest -PathType Leaf)) {
    throw 'Pre-review manifest was not created'
}
$preReviewBaseIndex = Join-Path $closureRaw 'remediation-index.json'
if (-not (Test-Path -LiteralPath $preReviewBaseIndex -PathType Leaf)) {
    throw 'Pre-review freeze did not create the Wave 0 base index'
}
$preReviewBaseBefore = (
    Get-FileHash -Algorithm SHA256 -LiteralPath $preReviewBaseIndex
).Hash
& $pythonExe -B $wave0Validator validate $preReviewBaseIndex --cwd .
if ($LASTEXITCODE -ne 0) {
    throw 'Frozen Wave 0 validator rejected the pre-review base index'
}
$preReviewBaseAfter = (
    Get-FileHash -Algorithm SHA256 -LiteralPath $preReviewBaseIndex
).Hash
if ($preReviewBaseBefore -cne $preReviewBaseAfter) {
    throw 'Frozen Wave 0 pre-review validation rewrote the base index'
}
$preReviewPayload = Get-Content -Raw -LiteralPath $preReviewManifest | ConvertFrom-Json
if ($preReviewPayload.schema_version -cne 'wave-e-pre-review-manifest-v1' -or
    $preReviewPayload.tested_git_head -cne $evidenceHead -or
    $preReviewPayload.implementation_parent_git_head -cne $implHead) {
    throw 'Pre-review manifest head/schema binding drifted'
}
$preReviewManifestHash = (
    Get-FileHash -Algorithm SHA256 -LiteralPath $preReviewManifest
).Hash.ToLowerInvariant()
if (Test-Path -LiteralPath $closureDir) {
    throw 'Pre-review freeze created public closure bytes'
}
```

The manifest is create-once and contains sorted exact raw and planned-public
path/size/SHA-256 records, the Wave 0 base-index digest, tested-input digest,
planning-source identities, source diff, and explicit exclusions for itself,
future reviews, privacy manifest, and final domain index. The builder immediately
rereads all bytes after creation. From this point until final publication, any
change to a frozen raw byte or its deterministic planned-public byte invalidates
the run and requires Task 5 from Step 1.

- [ ] **Step 6: Obtain four independent views, a skeptic, and an adjudicator in raw staging**

Create `C:\tmp\...\reviews`, not a repository directory, and keep the public
closure root absent while reviews are produced:

```powershell
$rawReviews = Join-Path $closureRaw 'reviews'
if (Test-Path -LiteralPath $rawReviews) { throw 'Raw review directory already exists' }
if (Test-Path -LiteralPath $closureDir) { throw 'Closure root exists before reviews' }
New-Item -ItemType Directory -Path $rawReviews | Out-Null
```

Dispatch four different reviewers against exact `E`, the direct `P..E` diff, the
tracked source/test/tool bytes, the candidate index, and the fresh raw closure
records. The mathematical reviewers treat the manuscript and project documents as
objects under review, not as mathematical authority; derivations are primary
closure evidence, and any literature citation is source-level unless its finer
location was actually checked. They own these exact files and questions:

| Raw file | Independent review question |
|---|---|
| `01-dynamical-systems.json` | Recompute both exact counterexamples and decide whether connected support entails existence, uniqueness, a common basin, or convergence. |
| `02-gauge-quotient.json` | Check componentwise decoupling, exogenous/component-local normalization, residual global-frame action, well-defined quotient descent, the distinction between rank classes of `M` and relative invariants of `(A,M)`, and the GL(1) invariant `a/m`. |
| `03-evidence-code-integrity.json` | Review Wave 0 runner/base-schema and verification-resolver conformance; exact snapshot/resolver/SKILL/contract/five-criteria/schema/gate identities; tested-input policy/digest/source bindings; raw/planned-public hashes; source-diff allowlist; JUnit parsing; executable and `.fls`/BibTeX identity; pre-review immutability; dependency/evidence separation; and create-once publication. |
| `04-manuscript-source-and-status.json` | Check the exact six-paragraph diff at old starts 174/176/178/180/182/194, all nine equation environments, rank-versus-relative-invariant and connectivity limitations, normalization/quotient conditions, forbidden/required language, root TeX record, and retained `OPEN`/`INCONCLUSIVE` boundaries. |

Each raw JSON uses exactly this shape, substituting the concrete full `E`, exact
reviewed paths, both claims, and nonempty evidence-grounded prose:

```json
{
  "schema_version": "wave-e-review-v1",
  "role": "independent_view",
  "view_id": "01-dynamical-systems",
  "tested_git_head": "$evidenceHead",
  "pre_review_manifest_sha256": "$preReviewManifestHash",
  "prior_review_inputs": [],
  "reviewed_paths": ["manuscripts/magent_elbo_whitepaper/08a_coarse_graining.tex"],
  "claim_scores": [
    {
      "claim_id": "AUD20-DEFECT-REPRODUCTION",
      "decision": "refute",
      "unresolved_disagreement": false,
      "criteria": [
        {"key": "statement_precision", "label": "statement precision", "score": 20, "evidence_ids": ["aud20-derivation"], "rationale": "The reproduced proposition is stated with explicit quantifiers."},
        {"key": "definitions_and_domains", "label": "definitions and domains", "score": 20, "evidence_ids": ["aud20-derivation"], "rationale": "The map, domain, components, quotient, and pair action are defined."},
        {"key": "assumptions", "label": "assumptions", "score": 20, "evidence_ids": ["aud20-derivation"], "rationale": "Exogenous normalization and component locality are explicit."},
        {"key": "derivation_validity", "label": "derivation validity", "score": 20, "evidence_ids": ["aud20-derivation", "elbo-oracles"], "rationale": "The factorization, derivative signs, and quotient calculation are exact."},
        {"key": "theorem_lemma_dependencies", "label": "theorem or lemma dependencies", "score": 20, "evidence_ids": ["aud20-derivation"], "rationale": "All used elementary continuity and monotonicity steps are named."},
        {"key": "limiting_cases", "label": "limiting cases", "score": 20, "evidence_ids": ["elbo-oracles"], "rationale": "Endpoints, disconnected components, and the GL(1) reduction are checked."},
        {"key": "counterexample_search", "label": "counterexample search", "score": 20, "evidence_ids": ["aud20-derivation", "elbo-oracles"], "rationale": "Exact basin and relative-invariant counterexamples refute the old inference."},
        {"key": "notation_conclusion_agreement", "label": "agreement between notation and conclusion", "score": 20, "evidence_ids": ["claim-language", "equation-byte-comparison"], "rationale": "The refutation matches the tested symbols and does not overstate its scope."}
      ]
    },
    {
      "claim_id": "AUD20-CORRECTED-CONTRACT",
      "decision": "support",
      "unresolved_disagreement": false,
      "criteria": [
        {"key": "statement_precision", "label": "statement precision", "score": 20, "evidence_ids": ["claim-language"], "rationale": "The corrected conclusions and nonconclusions are explicit."},
        {"key": "definitions_and_domains", "label": "definitions and domains", "score": 20, "evidence_ids": ["claim-language", "aud20-derivation"], "rationale": "Rank, relative invariant, component, normalization, and quotient domains are distinguished."},
        {"key": "assumptions", "label": "assumptions", "score": 20, "evidence_ids": ["claim-language"], "rationale": "The corrected text states normalization and descent assumptions."},
        {"key": "derivation_validity", "label": "derivation validity", "score": 20, "evidence_ids": ["aud20-derivation", "elbo-oracles"], "rationale": "The full derivation supports exactly the corrected boundaries."},
        {"key": "theorem_lemma_dependencies", "label": "theorem or lemma dependencies", "score": 20, "evidence_ids": ["aud20-derivation"], "rationale": "No unstated connectivity or quotient theorem is invoked."},
        {"key": "limiting_cases", "label": "limiting cases", "score": 20, "evidence_ids": ["elbo-oracles"], "rationale": "Boundary fixed points and GL(1) scaling are retained."},
        {"key": "counterexample_search", "label": "counterexample search", "score": 20, "evidence_ids": ["elbo-oracles"], "rationale": "The corrected text survives the exact registered counterexamples."},
        {"key": "notation_conclusion_agreement", "label": "agreement between notation and conclusion", "score": 20, "evidence_ids": ["claim-language", "equation-byte-comparison"], "rationale": "All nine equations are unchanged and the prose conclusion matches them."}
      ]
    }
  ],
  "summary": "Concrete evidence-bound assessment.",
  "falsification_conditions": ["A specific current byte or derivation that contradicts this decision."]
}
```

The dispatcher resolves `$evidenceHead` to the concrete 40-hex value and
`$preReviewManifestHash` to the concrete lowercase 64-hex digest before the
reviewer writes JSON; literal dollar-tokens are not permitted in a saved review.

The sample enumerates the mandatory shape, not predetermined scores. Reviewers must
score every one of the eight criteria, lower any score, oppose, or mark
inconclusive when evidence warrants it. `score=20` is eligible only when the cited
current derivation and corroborating evidence fully cover that criterion. The exact
ordered key/label set must equal `MATH_CRITERIA`; missing, duplicate, reordered, or
generic criteria reject. The expected evidence-bound decisions
are `refute` for `AUD20-DEFECT-REPRODUCTION` and `support` for
`AUD20-CORRECTED-CONTRACT`. Do not invent a numeric score threshold. If primary
decisions conflict for either claim or any primary reviewer marks an unresolved
criterion disagreement, record `criterion_disagreement` and dispatch four new
independent escalation reviewers to the exact frozen files
`05-countermodel-boundary.json`,
`06-independent-symbolic-check.json`, `07-publication-scope.json`, and
`08-evidence-provenance.json`; set target 8. A partial escalation set rejects.

After the four or eight independent views, dispatch a separate structured skeptic
to `skeptic.json`. It must steelman and attack each claim, attempt to find surviving
uniqueness/non-observability language, challenge the counterexamples and equation
comparison, challenge the TeX/input/privacy chain, cite current evidence IDs, and
state what would falsify its conclusion. Its `pre_review_manifest_sha256` equals
the frozen digest and its sorted `prior_review_inputs` contains the path, size, and
SHA-256 of every required primary/escalation raw review. Finally dispatch a
different adjudicator to `adjudicator.json`; it must read all independent views,
the skeptic, and every fresh mechanical/mathematical record, decide each claim
without majority voting, name decisive evidence, and retain a precise obligation
for any gap. Its `prior_review_inputs` contains every independent review plus
`skeptic.json`, each bound by exact raw size/SHA-256, and cites the same pre-review
manifest. No reviewer may rewrite a cited predecessor.

Every review has `tested_git_head=$evidenceHead`; all required review files exist
before `publish-bundle`; all `evidence_ids` resolve to the fresh raw artifact map;
and all `reviewed_paths` are current source paths or the exact candidate index.
The builder rejects a duplicate reviewer/view ID, a stale head, missing claim,
unknown evidence ID, empty rationale/falsification condition, unresolved final
disagreement, or an adjudicator that does not consider the skeptic. Review JSON is
then deterministically scrubbed and published under `views/`; agent agreement
itself is never evidence.

- [ ] **Step 7: Build the final closure index only after every review exists**

```powershell
$requiredRawReviews = @(
    '01-dynamical-systems.json',
    '02-gauge-quotient.json',
    '03-evidence-code-integrity.json',
    '04-manuscript-source-and-status.json',
    'skeptic.json',
    'adjudicator.json'
)
foreach ($name in $requiredRawReviews) {
    if (-not (Test-Path -LiteralPath (Join-Path $closureRaw "reviews\$name") -PathType Leaf)) {
        throw "Required raw review is missing: $name"
    }
}
if (Test-Path -LiteralPath $closureDir) {
    throw 'Closure directory exists before review-complete publication'
}

& $pythonExe -B $evidenceTool publish-bundle `
    --stage closure --repo-root . --raw-root $closureRaw `
    --public-root $closureDir --tested-head $evidenceHead `
    --implementation-parent $implHead `
    --planning-contract $planningContract `
    --planning-release $planningRelease `
    --baseline-provenance $baselineProvenance
if ($LASTEXITCODE -ne 0) { throw 'Wave E closure privacy publication/index failed' }
```

For closure, `publish-bundle` first rehashes every frozen pre-review raw byte and
recomputes every planned-public byte, then validates all raw tests, source diff,
scans, equation bytes,
TeX outputs, input inventories, command records, environment records, primary
views, skeptic, adjudicator, and any required escalation views entirely in memory.
It computes every raw size/SHA-256 and deterministic privacy transform before the
public root exists. It then publishes the sanitized bundle atomically and writes
`closure-index.json` last inside the staging sibling before the atomic rename. No
review or evidence output is a dependency input. A missing review, incomplete
four-view escalation, stale reviewed head, unresolved final disagreement, or
privacy leak leaves `$closureDir` absent.

- [ ] **Step 8: Validate the exact closure allowlist, privacy, and worktree state**

```powershell
& $pythonExe -B $evidenceTool validate-bundle `
    --stage closure --repo-root . --raw-root $closureRaw `
    --bundle-root $closureDir --tested-head $evidenceHead `
    --implementation-parent $implHead
if ($LASTEXITCODE -ne 0) { throw 'Wave E closure bundle validation failed' }
$closureBaseIndex = Join-Path $closureDir 'remediation-index.json'
$closureBaseBefore = (
    Get-FileHash -Algorithm SHA256 -LiteralPath $closureBaseIndex
).Hash
& $pythonExe -B $wave0Validator validate $closureBaseIndex --cwd .
if ($LASTEXITCODE -ne 0) {
    throw 'Frozen Wave 0 validator rejected the closure base index'
}
$closureBaseAfter = (
    Get-FileHash -Algorithm SHA256 -LiteralPath $closureBaseIndex
).Hash
if ($closureBaseBefore -cne $closureBaseAfter) {
    throw 'Frozen Wave 0 closure validation rewrote the base index'
}

$commonFiles = @(
    'aud20-derivation.md',
    'baseline-warning-provenance.json',
    'claim-language.json',
    'command-records.json',
    'elbo-oracles.xml',
    'environment.json',
    'equation-byte-comparison.json',
    'evidence-tool-tests.xml',
    'privacy-manifest.json',
    'source-diff.json',
    'tex-build-summary.json',
    'tex-inputs.json'
)
$coreReviews = @(
    'views/01-dynamical-systems.json',
    'views/02-gauge-quotient.json',
    'views/03-evidence-code-integrity.json',
    'views/04-manuscript-source-and-status.json',
    'views/skeptic.json',
    'views/adjudicator.json'
)
$escalationReviews = @(
    'views/05-countermodel-boundary.json',
    'views/06-independent-symbolic-check.json',
    'views/07-publication-scope.json',
    'views/08-evidence-provenance.json'
)
$rawEscalationCount = @(
    $escalationReviews | Where-Object {
        Test-Path -LiteralPath (Join-Path $closureRaw ("reviews/" + $_.Substring(6)))
    }
).Count
if ($rawEscalationCount -notin @(0,4)) {
    throw 'Wave E escalation review set is partial'
}
$reviewFiles = @($coreReviews)
if ($rawEscalationCount -eq 4) { $reviewFiles += $escalationReviews }
$expectedBundleFiles = @(
    $commonFiles +
    @('remediation-index.json','pre-review-manifest.json') +
    $reviewFiles +
    'closure-index.json' |
        Sort-Object
)
$resolvedClosure = (Resolve-Path -LiteralPath $closureDir).Path
$actualBundleFiles = @(
    Get-ChildItem -LiteralPath $closureDir -File -Recurse |
        ForEach-Object {
            $_.FullName.Substring($resolvedClosure.Length + 1).Replace('\','/')
        } |
        Sort-Object
)
if (Compare-Object $expectedBundleFiles $actualBundleFiles) {
    throw 'Wave E closure allowlist mismatch'
}
if ($actualBundleFiles.Count -ne (21 + $rawEscalationCount)) {
    throw 'Wave E closure file count is not exactly 21 or 25'
}

$closurePrefix = ($closureDir -replace '\\','/') + '/'
$expectedUntracked = @(
    $expectedBundleFiles | ForEach-Object { $closurePrefix + $_ } | Sort-Object
)
$actualUntracked = @(& git ls-files --others --exclude-standard | Sort-Object)
if (Compare-Object $expectedUntracked $actualUntracked) {
    throw 'Nonignored untracked paths are not exactly the indexed closure bytes'
}
if ((& git status --porcelain=v1 --untracked-files=no).Count -ne 0) {
    throw 'Tracked worktree is dirty at Wave E closure'
}
if ((& git rev-parse HEAD).Trim() -cne $evidenceHead) {
    throw 'HEAD moved after closure runs'
}
if ((& git rev-parse HEAD^).Trim() -cne $implHead) {
    throw 'E is no longer the direct child of P'
}

foreach ($secret in @($env:USERNAME,$env:COMPUTERNAME,$waveWorktree,$closureRaw)) {
    if ([string]::IsNullOrWhiteSpace($secret)) { continue }
    & rg -n --fixed-strings -- $secret $closureDir
    if ($LASTEXITCODE -eq 0) { throw "Closure privacy leak: $secret" }
    if ($LASTEXITCODE -ne 1) { throw 'Closure privacy scan execution failed' }
}
& rg -n -i -- 'C:\\Users\\|process.?id|gate telemetry' $closureDir
if ($LASTEXITCODE -eq 0) { throw 'Closure generic privacy scan failed' }
if ($LASTEXITCODE -ne 1) { throw 'Closure generic privacy scan did not execute' }
```

The validator rereads and rehashes every public byte, reparses both JUnits, checks
all five executable and dependency/source/TeX identities, proves `E^ == P`, proves
`P..E` contains only the candidate directory, validates every review against `E`,
and requires `evidence_inventory` to match the exact 21- or 25-file allowlist
except for the index's declared self-exclusion. Raw files outside the repository
are not counted as public closure and cannot be the sole support for a claim.

- [ ] **Step 9: Prove the empty gate cannot close, populate it explicitly, and validate**

The installed gate owns only template creation and validation. Start it only after
the closure directory, every public review, and `closure-index.json` have passed
Step 8. The direct validation immediately after `start` is a required negative
control; an empty ledger is never closure.

```powershell
$planningPayload = Get-Content -Raw -LiteralPath $planningContract | ConvertFrom-Json
$planningSnapshot = "C:\tmp\magent-wave-e-planning-snapshot-$($planningPayload.planning_commit.Substring(0,12))"
$verificationSnapshot = Join-Path $planningSnapshot `
    'docs\verification\remediation\verification-contract-v1.json'
$wave0Resolver = Join-Path $planningSnapshot 'tools\remediation_evidence.py'
$verificationRoot = 'C:\Users\chris and christine\.codex\skills\verification'
$gateOutput = @(
    & $pythonExe -B $wave0Resolver resolve-verification-gate `
        --snapshot $verificationSnapshot --root $verificationRoot
)
if ($LASTEXITCODE -ne 0 -or $gateOutput.Count -ne 1) {
    throw 'Closure gate resolution from the frozen Wave 0 contract failed'
}
$gate = $gateOutput[0].Trim()
$expectedGate = Join-Path $verificationRoot 'scripts\verification_gate.py'
if ((Resolve-Path -LiteralPath $gate).Path -cne
    (Resolve-Path -LiteralPath $expectedGate).Path) {
    throw 'Closure resolver did not return the bound Codex gate'
}
$ledger = '.verification\wave-e\final-ledger.json'
if (Test-Path -LiteralPath '.verification\active.json') {
    throw 'A verification gate is already active'
}
if (Test-Path -LiteralPath $ledger) {
    throw 'Wave E ledger already exists'
}

& $pythonExe $gate start --cwd . --mode closure --ledger $ledger
if ($LASTEXITCODE -ne 0) { throw 'Wave E gate start failed' }

& $pythonExe $gate validate --cwd . $ledger
if ($LASTEXITCODE -eq 0) {
    throw 'Empty Wave E ledger unexpectedly validated'
}

& $pythonExe -B $evidenceTool populate-ledger `
    --repo-root . --ledger $ledger `
    --closure-index "$closureDir\closure-index.json" `
    --views-dir "$closureDir\views"
if ($LASTEXITCODE -ne 0) { throw 'Wave E ledger population failed' }

& $pythonExe $gate validate --cwd . $ledger
if ($LASTEXITCODE -ne 0) { throw 'Populated Wave E ledger failed validation' }
& $pythonExe -B $evidenceTool validate-ledger-links `
    --repo-root . --ledger $ledger `
    --closure-index "$closureDir\closure-index.json"
if ($LASTEXITCODE -ne 0) { throw 'Wave E ledger/index link validation failed' }

$ledgerPayload = Get-Content -Raw -LiteralPath $ledger | ConvertFrom-Json
$claims = @($ledgerPayload.claims)
$expectedClaims = @(
    'AUD20-DEFECT-REPRODUCTION',
    'AUD20-CORRECTED-CONTRACT'
)
if (Compare-Object $expectedClaims @($claims.id)) {
    throw 'Wave E ledger claim IDs drifted'
}
if (($claims | Where-Object id -eq 'AUD20-DEFECT-REPRODUCTION').state -ne 'REFUTED') {
    throw 'The current-revision defect proposition was not refuted'
}
if (($claims | Where-Object id -eq 'AUD20-CORRECTED-CONTRACT').state -ne 'EVIDENCE_VERIFIED') {
    throw 'The corrected manuscript contract did not close'
}
if (@($claims | Where-Object { $_.severity -ne 'high' }).Count -ne 0) {
    throw 'AUD-20 severity was downgraded'
}
if (@($claims | Where-Object { $_.escalation_target -notin @(4,8) }).Count -ne 0) {
    throw 'AUD-20 escalation target is invalid'
}
foreach ($claim in $claims) {
    $expectedTriggers = if ($claim.escalation_target -eq 8) {
        @('high_severity', 'criterion_disagreement')
    } else {
        @('high_severity')
    }
    if ((@($claim.escalation_triggers) -join "`n") -cne
        ($expectedTriggers -join "`n")) {
        throw "AUD-20 escalation trigger set/order drifted: $($claim.id)"
    }
    $expectedMathCriteria = @(
        'statement precision',
        'definitions and domains',
        'assumptions',
        'derivation validity',
        'theorem or lemma dependencies',
        'limiting cases',
        'counterexample search',
        'agreement between notation and conclusion'
    )
    if (@($claim.criteria).Count -ne $expectedMathCriteria.Count -or
        (@($claim.criteria.name) -join "`n") -cne
            ($expectedMathCriteria -join "`n")) {
        throw "AUD-20 aggregate mathematics criteria drifted: $($claim.id)"
    }
    if ($claim.views.calibration_kind -cne 'artifact-bound-pairwise-v1' -or
        $claim.views.unresolved_disagreement -ne $false -or
        @($claim.views.scores).Count -ne [int]$claim.escalation_target) {
        throw "AUD-20 calibrated view record drifted: $($claim.id)"
    }
    if ($claim.views.comparison.method -cne 'pairwise' -or
        (@($claim.views.comparison.candidate_ids) -join "`n") -cne
            (@('claim-supported','claim-refuted') -join "`n") -or
        (@($claim.views.comparison.orders) -join "`n") -cne
            (@('AB','BA') -join "`n") -or
        @($claim.views.comparison.pivot_ids).Count -ne 0 -or
        @($claim.views.comparison.matches).Count -ne 2) {
        throw "AUD-20 ordered pairwise comparison drifted: $($claim.id)"
    }
    foreach ($viewScore in @($claim.views.scores)) {
        if ((@($viewScore.criteria.name) -join "`n") -cne
            ($expectedMathCriteria -join "`n")) {
            throw "AUD-20 independent-view mathematics criteria drifted: $($claim.id)"
        }
    }
    foreach ($match in @($claim.views.comparison.matches)) {
        if ((@($match.criteria.name) -join "`n") -cne
            ($expectedMathCriteria -join "`n")) {
            throw "AUD-20 comparison mathematics criteria drifted: $($claim.id)"
        }
    }
    if (@($claim.verifiers | Where-Object role -eq 'verifier-skeptic').Count -ne 1 -or
        @($claim.verifiers | Where-Object role -eq 'verifier-adjudicator').Count -ne 1) {
        throw "AUD-20 structured verifier count drifted: $($claim.id)"
    }
}
$defectClaim = $claims | Where-Object id -eq 'AUD20-DEFECT-REPRODUCTION'
$contractClaim = $claims | Where-Object id -eq 'AUD20-CORRECTED-CONTRACT'
if ($defectClaim.domain -cne 'mathematics' -or
    $contractClaim.domain -cne 'mathematics') {
    throw 'AUD-20 claim-domain mapping drifted'
}
$expectedGateUntracked = @(
    $expectedUntracked +
    '.verification/active.json' +
    '.verification/wave-e/final-ledger.json' |
        Sort-Object
)
$actualGateUntracked = @(& git ls-files --others --exclude-standard | Sort-Object)
if (Compare-Object $expectedGateUntracked $actualGateUntracked) {
    throw 'Post-start status contains paths beyond closure bytes and exact gate state'
}
```

`populate-ledger` accepts only the gate-created empty closure template. It copies
the gate's complete `artifact_revision`; hashes the actual closure index; links
all current closure base/domain indexes, planning contract, source diff, JUnit,
derivation, scan, equation, TeX, baseline provenance, input, environment, privacy,
pre-review manifest, Wave 0 verifier snapshot/resolver, resolved Codex verifier
contract files, and review bytes; emits a complete ordered A/B and B/A
pairwise grid covering every installed mathematics criterion; and
links exactly one skeptic and one adjudicator per claim. The first claim is the
proposition that the original AUD-20 inference still reproduces at `E`; current
counterevidence makes it `REFUTED`. The second is the positive corrected contract
and is `EVIDENCE_VERIFIED`. Missing evidence, unresolved disagreement, or a stale
head produces `INCONCLUSIVE`, never a vote-based pass.
Research does not Git-ignore these two gate files. Their presence is nevertheless
safe for artifact binding because the installed gate's `_safe_git_path` excludes
the entire `.verification` top-level directory before hashing worktree files. The
explicit status comparison above allows only the exact marker and ledger; no Git
exclude file, `.gitignore`, `.git/config`, or shared worktree metadata is changed.

- [ ] **Step 10: Freeze the verified bytes and hand only refs to Task 6**

```powershell
& git diff --check
if ($LASTEXITCODE -ne 0) { throw 'Wave E final whitespace check failed' }
if ((& git status --porcelain=v1 --untracked-files=no).Count -ne 0) {
    throw 'Tracked Wave E worktree changed after evidence child E'
}
& $pythonExe -B $evidenceTool validate-bundle `
    --stage closure --repo-root . --raw-root $closureRaw `
    --bundle-root $closureDir --tested-head $evidenceHead `
    --implementation-parent $implHead
if ($LASTEXITCODE -ne 0) { throw 'Frozen Wave E closure no longer validates' }
& $pythonExe $gate validate --cwd . $ledger
if ($LASTEXITCODE -ne 0) { throw 'Frozen Wave E ledger no longer validates' }
```

After this point no source, candidate, closure, review, or ledger byte may change.
Task 6 may move refs only. Wave E's ledger belongs solely to the Research revision;
it is never copied into or cited as evidence by the MultiAgentELBO aggregate
ledger. Any byte mutation or non-fast-forward integration invalidates this closure
and requires Task 5 from Step 1 with new evidence and reviews.

---

### Task 6: Publish in dependency order and preserve every live WIP byte

**Files:**

- Read only: live Research checkout and before/after WIP fingerprints.
- Update refs only: fixed-ray ingest branch, Wave E feature branch, remote `main`,
  and a clean local `main` worktree.

**Interfaces:**

- Consumes: validated evidence child `E` and local closure ledger.
- Produces: remote feature/main refs at `E`, local clean `main` at `E`, and an
  unchanged live Research review checkout.

- [ ] **Step 1: Revalidate closure-bound contracts, then publish `c9f237d2` when required**

```powershell
$waveWorktree = 'C:\Users\chris and christine\Documents\ChatGPT\MultiAgentELBO\.superpowers\worktrees\Research-magent-aud20-remediation-20260811'
if ((Resolve-Path '.').Path -cne (Resolve-Path $waveWorktree).Path) {
    throw 'Task 6 must run from the dedicated Wave E Research worktree'
}
$researchRepo = 'C:\Users\chris and christine\Desktop\Research'
$contextCommit = 'c9f237d2ca54c274ba5760012e62823a69d203a3'
$ingestBranch = 'codex/multiagentelbo-fixed-ray-ingest-20260810'
$waveBranch = 'codex/magent-aud20-connectedness-remediation-20260811'
$evidenceHead = (& git rev-parse HEAD).Trim()
$evidenceShort = $evidenceHead.Substring(0,12)
$closureIndex = "verification-evidence\wave-e\$evidenceShort\closure-index.json"
$closureBaseIndex = "verification-evidence\wave-e\$evidenceShort\remediation-index.json"
$ledger = '.verification\wave-e\final-ledger.json'
$pythonExe = (Resolve-Path 'C:\Python314\python.exe').Path
$evidenceTool = 'manuscripts\magent_elbo_whitepaper\verification\wave_e_evidence.py'
$planningContract = 'C:\tmp\magent-wave-e-planning-contract.json'
$planningRelease = 'C:\tmp\magent-wave-e-planning-release.json'
$verificationRoot = 'C:\Users\chris and christine\.codex\skills\verification'
if (-not (Test-Path -LiteralPath $closureIndex -PathType Leaf) -or
    -not (Test-Path -LiteralPath $closureBaseIndex -PathType Leaf) -or
    -not (Test-Path -LiteralPath $ledger -PathType Leaf) -or
    -not (Test-Path -LiteralPath $planningRelease -PathType Leaf)) {
    throw 'Task 5 index/ledger or approved planning release is missing'
}

function Assert-ExactKeys {
    param(
        [Parameter(Mandatory=$true)][object]$Record,
        [Parameter(Mandatory=$true)][string[]]$Expected,
        [Parameter(Mandatory=$true)][string]$Label
    )
    $actual = @($Record.PSObject.Properties.Name | Sort-Object)
    $expectedSorted = @($Expected | Sort-Object)
    if (Compare-Object $actual $expectedSorted) {
        throw "$Label keys drifted"
    }
}

function Assert-RecordSequence {
    param(
        [Parameter(Mandatory=$true)][object[]]$Actual,
        [Parameter(Mandatory=$true)][object[]]$Bound,
        [Parameter(Mandatory=$true)][string[]]$Fields,
        [Parameter(Mandatory=$true)][string]$Label
    )
    if ($Actual.Count -ne $Bound.Count) {
        throw "$Label count drifted"
    }
    for ($i = 0; $i -lt $Bound.Count; $i++) {
        foreach ($field in $Fields) {
            if ([string]$Actual[$i].$field -cne [string]$Bound[$i].$field) {
                throw "$Label record $i field $field drifted"
            }
        }
    }
}

function Assert-FileIdentity {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][object]$Bound,
        [Parameter(Mandatory=$true)][string]$Label
    )
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "$Label file is missing"
    }
    $item = Get-Item -LiteralPath $Path
    $sha = (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
    if ([int64]$Bound.size_bytes -ne [int64]$item.Length -or
        $Bound.sha256.ToLowerInvariant() -cne $sha) {
        throw "$Label byte identity drifted"
    }
}

function Assert-PlanningGitFileIdentity {
    param(
        [Parameter(Mandatory=$true)][string]$SnapshotRoot,
        [Parameter(Mandatory=$true)][object]$Bound,
        [Parameter(Mandatory=$true)][string]$Label
    )
    $absolute = Join-Path $SnapshotRoot $Bound.path
    Assert-FileIdentity -Path $absolute -Bound $Bound -Label $Label
    $blob = (& git -C $SnapshotRoot hash-object -- $Bound.path).Trim()
    if ($LASTEXITCODE -ne 0 -or $blob -cne $Bound.git_blob) {
        throw "$Label Git blob identity drifted"
    }
}

# The closure index is the authority for this preflight. Hash the mutable Task 1
# temporary files against its records before reading or executing either one.
$closurePayload = Get-Content -Raw -LiteralPath $closureIndex | ConvertFrom-Json
$basePayload = Get-Content -Raw -LiteralPath $closureBaseIndex | ConvertFrom-Json
if ($closurePayload.schema_version -cne 'wave-e-domain-inventory-v1' -or
    $closurePayload.evidence_stage -cne 'closure' -or
    $closurePayload.tested_git_head -cne $evidenceHead) {
    throw 'Closure index schema/stage/head drifted before publication'
}
Assert-ExactKeys -Record $basePayload -Expected @(
    'schema_version','wave','evidence_stage','tested_git_head',
    'implementation_parent_git_head','platform','environment_record',
    'dependency_versions','dependency_inputs','tested_input_policy',
    'tested_input_inventory_sha256','commands','source_config_bindings',
    'reviewed_plan_binding','verification_contract_binding','files'
) -Label 'Closure Wave 0 base index'
if ($basePayload.schema_version -cne 'remediation-evidence-v1' -or
    $basePayload.evidence_stage -cne 'closure' -or
    $basePayload.tested_git_head -cne $evidenceHead) {
    throw 'Closure Wave 0 base schema/stage/head drifted before publication'
}
$boundPlanning = $closurePayload.planning_sources
Assert-ExactKeys -Record $boundPlanning -Expected @(
    'schema_version','planning_commit','wave0_plan_sha256','planning_contract',
    'planning_release_binding','planning_release_record','sources',
    'verification_contract_inputs','verification_contract'
) -Label 'Closure planning_sources'
if ($boundPlanning.schema_version -cne 'wave-e-planning-sources-v1' -or
    $boundPlanning.planning_commit -notmatch '^[0-9a-f]{40}$' -or
    $boundPlanning.wave0_plan_sha256 -cne
        'dbe2263a3b0fe1e9f5db4ff1fca9a19f819cfd32ef38da71d6e5cb5485723ac2') {
    throw 'Closure-bound planning source schema/commit drifted'
}
Assert-ExactKeys -Record $boundPlanning.planning_contract -Expected @(
    'path_alias','size_bytes','sha256'
) -Label 'Closure planning contract identity'
if ($boundPlanning.planning_contract.path_alias -cne '$PLANNING_CONTRACT') {
    throw 'Closure planning contract alias drifted'
}
Assert-FileIdentity -Path $planningContract `
    -Bound $boundPlanning.planning_contract -Label 'Task 1 planning contract'
Assert-ExactKeys -Record $boundPlanning.planning_release_binding -Expected @(
    'path','size_bytes','sha256'
) -Label 'Closure planning-release identity'
if ($boundPlanning.planning_release_binding.path -cne '$PLANNING_RELEASE') {
    throw 'Closure planning-release alias drifted'
}
Assert-FileIdentity -Path $planningRelease `
    -Bound $boundPlanning.planning_release_binding `
    -Label 'Approved planning-release record'
$releasePayload = Get-Content -Raw -LiteralPath $planningRelease | ConvertFrom-Json
Assert-ExactKeys -Record $releasePayload -Expected @(
    'schema_version','repository','planning_commit','reviewed_plan'
) -Label 'Approved planning-release record'
Assert-ExactKeys -Record $releasePayload.reviewed_plan -Expected @(
    'path','git_blob','size_bytes','sha256'
) -Label 'Approved planning-release reviewed plan'
foreach ($field in @('schema_version','repository','planning_commit')) {
    if ([string]$releasePayload.$field -cne
        [string]$boundPlanning.planning_release_record.$field) {
        throw "Closure-bound planning-release scalar drifted: $field"
    }
}
Assert-RecordSequence -Actual @($releasePayload.reviewed_plan) `
    -Bound @($boundPlanning.planning_release_record.reviewed_plan) `
    -Fields @('path','git_blob','size_bytes','sha256') `
    -Label 'Closure-bound planning-release reviewed plan'

$planningPayload = Get-Content -Raw -LiteralPath $planningContract | ConvertFrom-Json
if ($planningPayload.schema_version -cne 'wave-e-planning-contract-v1' -or
    $planningPayload.planning_commit -cne $boundPlanning.planning_commit -or
    $planningPayload.wave0_plan_sha256 -cne $boundPlanning.wave0_plan_sha256) {
    throw 'Task 1 planning contract content is not the closure-bound contract'
}
Assert-RecordSequence -Actual @($planningPayload.planning_release_binding) `
    -Bound @($boundPlanning.planning_release_binding) `
    -Fields @('path','size_bytes','sha256') `
    -Label 'Planning-contract release identity'
Assert-RecordSequence -Actual @($planningPayload.planning_release_record.reviewed_plan) `
    -Bound @($releasePayload.reviewed_plan) `
    -Fields @('path','git_blob','size_bytes','sha256') `
    -Label 'Planning-contract approved reviewed plan'
Assert-RecordSequence -Actual @($planningPayload.sources) `
    -Bound @($boundPlanning.sources) `
    -Fields @('path','git_blob','size_bytes','sha256') `
    -Label 'Planning sources'
Assert-RecordSequence -Actual @($planningPayload.verification_contract_inputs) `
    -Bound @($boundPlanning.verification_contract_inputs) `
    -Fields @('path','git_blob','size_bytes','sha256') `
    -Label 'Verification snapshot/resolver inputs'

$planningVerification = $planningPayload.verification_contract
$boundVerification = $boundPlanning.verification_contract
Assert-ExactKeys -Record $boundVerification -Expected @(
    'schema_version','root_alias','snapshot','resolver','resolved_gate',
    'contract_files'
) -Label 'Closure verification contract'
foreach ($field in @('schema_version','root_alias','resolved_gate')) {
    if ([string]$planningVerification.$field -cne [string]$boundVerification.$field) {
        throw "Verification contract scalar $field drifted"
    }
}
Assert-RecordSequence -Actual @($planningVerification.snapshot) `
    -Bound @($boundVerification.snapshot) `
    -Fields @('path','git_blob','size_bytes','sha256') `
    -Label 'Frozen verification snapshot'
Assert-RecordSequence -Actual @($planningVerification.resolver) `
    -Bound @($boundVerification.resolver) `
    -Fields @('path','git_blob','size_bytes','sha256') `
    -Label 'Frozen Wave 0 resolver'
Assert-RecordSequence -Actual @($planningVerification.contract_files) `
    -Bound @($boundVerification.contract_files) `
    -Fields @('path','size_bytes','sha256') `
    -Label 'Active Codex verification contract files'

$expectedReviewedPlanBinding = [ordered]@{
    path = $releasePayload.reviewed_plan.path
    planning_commit = $releasePayload.planning_commit
    git_blob = $releasePayload.reviewed_plan.git_blob
    size_bytes = $releasePayload.reviewed_plan.size_bytes
    sha256 = $releasePayload.reviewed_plan.sha256
}
Assert-ExactKeys -Record $basePayload.reviewed_plan_binding -Expected @(
    'path','planning_commit','git_blob','size_bytes','sha256'
) -Label 'Wave 0 reviewed_plan_binding'
Assert-RecordSequence -Actual @($basePayload.reviewed_plan_binding) `
    -Bound @($expectedReviewedPlanBinding) `
    -Fields @('path','planning_commit','git_blob','size_bytes','sha256') `
    -Label 'Wave 0 reviewed_plan_binding'
Assert-ExactKeys -Record $basePayload.verification_contract_binding -Expected @(
    'schema_version','root_alias','snapshot','resolver','resolved_gate',
    'contract_files'
) -Label 'Wave 0 verification_contract_binding'
foreach ($field in @('schema_version','root_alias','resolved_gate')) {
    if ([string]$basePayload.verification_contract_binding.$field -cne
        [string]$boundVerification.$field) {
        throw "Wave 0 verification_contract_binding scalar drifted: $field"
    }
}
Assert-RecordSequence `
    -Actual @($basePayload.verification_contract_binding.snapshot) `
    -Bound @($boundVerification.snapshot) `
    -Fields @('path','git_blob','size_bytes','sha256') `
    -Label 'Wave 0 verification_contract_binding snapshot'
Assert-RecordSequence `
    -Actual @($basePayload.verification_contract_binding.resolver) `
    -Bound @($boundVerification.resolver) `
    -Fields @('path','git_blob','size_bytes','sha256') `
    -Label 'Wave 0 verification_contract_binding resolver'
Assert-RecordSequence `
    -Actual @($basePayload.verification_contract_binding.contract_files) `
    -Bound @($boundVerification.contract_files) `
    -Fields @('path','size_bytes','sha256') `
    -Label 'Wave 0 verification_contract_binding files'

$boundInputRecords = @(
    $boundVerification.snapshot,
    $boundVerification.resolver
)
Assert-RecordSequence -Actual @($boundPlanning.verification_contract_inputs) `
    -Bound $boundInputRecords `
    -Fields @('path','git_blob','size_bytes','sha256') `
    -Label 'Nested verification input identities'

$planningSnapshot = "C:\tmp\magent-wave-e-planning-snapshot-$($boundPlanning.planning_commit.Substring(0,12))"
$planningSnapshotHead = (& git -C $planningSnapshot rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or
    $planningSnapshotHead -cne $boundPlanning.planning_commit) {
    throw 'Frozen planning snapshot HEAD is not the closure-bound planning commit'
}
foreach ($record in @($boundPlanning.sources)) {
    Assert-PlanningGitFileIdentity -SnapshotRoot $planningSnapshot `
        -Bound $record -Label "Frozen planning source $($record.path)"
}
$boundWave0Plan = @(
    $boundPlanning.sources | Where-Object {
        $_.path -ceq 'docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md'
    }
)
if ($boundWave0Plan.Count -ne 1 -or
    $boundWave0Plan[0].sha256.ToLowerInvariant() -cne
        $boundPlanning.wave0_plan_sha256) {
    throw 'Closure-bound Wave 0 plan SHA-256 record drifted'
}
Assert-PlanningGitFileIdentity -SnapshotRoot $planningSnapshot `
    -Bound $boundVerification.snapshot -Label 'Frozen Wave 0 snapshot'
Assert-PlanningGitFileIdentity -SnapshotRoot $planningSnapshot `
    -Bound $boundVerification.resolver -Label 'Frozen Wave 0 resolver'
$verificationSnapshot = Join-Path $planningSnapshot $boundVerification.snapshot.path
$wave0Resolver = Join-Path $planningSnapshot $boundVerification.resolver.path

$expectedContractPaths = @(
    'SKILL.md',
    'references/contract.md',
    'references/criteria-code.md',
    'references/criteria-evidence.md',
    'references/criteria-experiment.md',
    'references/criteria-general.md',
    'references/criteria-math.md',
    'schemas/claim-ledger.schema.json',
    'scripts/verification_gate.py'
)
$boundContractFiles = @($boundVerification.contract_files)
if ($boundContractFiles.Count -ne 9) {
    throw 'Closure-bound active verifier inventory is not exactly nine files'
}
for ($i = 0; $i -lt $expectedContractPaths.Count; $i++) {
    $expectedAlias = '$VERIFICATION_ROOT/' + $expectedContractPaths[$i]
    if ($boundContractFiles[$i].path -cne $expectedAlias) {
        throw "Closure-bound verifier path/order drifted at $i"
    }
    $activePath = Join-Path $verificationRoot $expectedContractPaths[$i]
    Assert-FileIdentity -Path $activePath -Bound $boundContractFiles[$i] `
        -Label "Active Codex verifier $($expectedContractPaths[$i])"
}

$expectedGateAlias = '$VERIFICATION_ROOT/scripts/verification_gate.py'
if ($boundVerification.root_alias -cne '$VERIFICATION_ROOT' -or
    $boundVerification.resolved_gate -cne $expectedGateAlias) {
    throw 'Closure-bound Codex verification root/gate alias drifted'
}
$gateOutput = @(
    & $pythonExe -B $wave0Resolver resolve-verification-gate `
        --snapshot $verificationSnapshot --root $verificationRoot
)
if ($LASTEXITCODE -ne 0 -or $gateOutput.Count -ne 1) {
    throw 'Publication gate resolution from the closure-bound Wave 0 contract failed'
}
$gate = $gateOutput[0].Trim()
$expectedGate = Join-Path $verificationRoot 'scripts\verification_gate.py'
if ((Resolve-Path -LiteralPath $gate).Path -cne
    (Resolve-Path -LiteralPath $expectedGate).Path) {
    throw 'Publication resolver did not return the exact closure-bound Codex gate'
}
& $pythonExe -B $wave0Resolver validate $closureBaseIndex --cwd .
if ($LASTEXITCODE -ne 0) {
    throw 'Frozen Wave 0 validator rejected the prepublication base index'
}

& $pythonExe $gate validate --cwd . $ledger
if ($LASTEXITCODE -ne 0) { throw 'Pre-publication Wave E ledger is invalid' }
& $pythonExe -B $evidenceTool validate-ledger-links `
    --repo-root . --ledger $ledger --closure-index $closureIndex
if ($LASTEXITCODE -ne 0) { throw 'Pre-publication Wave E closure link is invalid' }

& git -C $researchRepo fetch origin
if ($LASTEXITCODE -ne 0) { throw 'Pre-publication fetch failed' }
& git -C $researchRepo merge-base --is-ancestor $contextCommit origin/main
if ($LASTEXITCODE -ne 0) {
    & git -C $researchRepo merge-base --is-ancestor origin/main $contextCommit
    if ($LASTEXITCODE -ne 0) {
        throw 'c9f237d2 cannot fast-forward current origin/main'
    }
    & git -C $researchRepo push origin `
        "${contextCommit}:refs/heads/$ingestBranch"
    if ($LASTEXITCODE -ne 0) { throw 'Fixed-ray ingest branch push failed' }
    & git -C $researchRepo push origin `
        "${contextCommit}:refs/heads/main"
    if ($LASTEXITCODE -ne 0) { throw 'Fixed-ray ingest main publication failed' }
    & git -C $researchRepo fetch origin
    $remoteAfterIngest = (& git -C $researchRepo rev-parse origin/main).Trim()
    if ($remoteAfterIngest -cne $contextCommit) {
        throw 'Remote main does not equal c9f237d2 after ingest publication'
    }
}
```

This entire revalidation block precedes the first gate invocation and the first
fetch, push, merge, or other ref/publication mutation. The temporary Task 1 files
are inputs to be rehashed, never authorities: the closure index supplies the
planning-contract identity, exact planning commit, snapshot/resolver blob and
byte identities, exact Wave 0 plan pin, approved planning-release bytes/content,
the Wave 0-compatible base reviewed-plan/verifier bindings, and all nine ordered
active Codex contract-file identities. The frozen external Wave 0 validator must
also accept the exact base bytes. Any missing record, extra/reordered path,
byte/blob/hash/head mismatch, release mutation, base-binding/files drift, resolver
failure, external-validator failure, or gate-path mismatch blocks publication.

Expected: remote `main` contains `c9f237d2` before any Wave E push. A protected-
branch rejection blocks Wave E publication; do not bypass it or push the child
first.

- [ ] **Step 2: Prove fast-forward ancestry and push the verified feature**

```powershell
& git fetch origin
if ($LASTEXITCODE -ne 0) { throw 'Wave E refetch failed' }
& git merge-base --is-ancestor origin/main $evidenceHead
if ($LASTEXITCODE -ne 0) {
    throw 'Verified evidence child is not a fast-forward of remote main'
}

& git push -u origin $waveBranch
if ($LASTEXITCODE -ne 0) { throw 'Wave E feature push failed' }
$remoteFeature = (
    & git ls-remote origin "refs/heads/$waveBranch"
).Split("`t")[0]
if ($remoteFeature -cne $evidenceHead) {
    throw 'Remote Wave E feature SHA mismatch'
}
```

- [ ] **Step 3: Fast-forward remote `main` to the verified evidence child**

```powershell
& git push origin "${evidenceHead}:refs/heads/main"
if ($LASTEXITCODE -ne 0) { throw 'Wave E main fast-forward failed' }
& git fetch origin
$remoteMain = (& git rev-parse origin/main).Trim()
if ($remoteMain -cne $evidenceHead) {
    throw 'Remote main does not equal the verified evidence child'
}
$remoteRefs = & git ls-remote origin `
    refs/heads/main "refs/heads/$waveBranch"
$remoteRefs
```

Expected: both remote refs resolve to `E`.

- [ ] **Step 4: Fast-forward only the clean local `main` worktree**

```powershell
$worktreeRecords = (
    (& git -C $researchRepo worktree list --porcelain) -join "`n"
) -split "(?:`r?`n){2,}"
$mainRecord = @(
    $worktreeRecords | Where-Object { $_ -match '(?m)^branch refs/heads/main$' }
)
if ($mainRecord.Count -ne 1) {
    throw 'Expected exactly one local Research main worktree'
}
$mainWorktreeLine = @(
    $mainRecord[0] -split "`r?`n" |
        Where-Object { $_ -like 'worktree *' }
)
$mainWorktree = $mainWorktreeLine[0].Substring('worktree '.Length)
if ((& git -C $mainWorktree status --porcelain).Count -ne 0) {
    throw "Local main worktree is dirty: $mainWorktree"
}
& git -C $mainWorktree fetch origin
& git -C $mainWorktree merge --ff-only origin/main
if ($LASTEXITCODE -ne 0) { throw 'Local main fast-forward failed' }

$localMain = (& git -C $mainWorktree rev-parse HEAD).Trim()
$parity = (& git -C $mainWorktree rev-list --left-right --count `
    HEAD...origin/main).Trim()
if ($localMain -cne $evidenceHead -or $parity -ne "0`t0") {
    throw "Local/remote main parity failed: head=$localMain parity=$parity"
}
```

The dirty live review checkout is not this clean `main` worktree and is not
advanced, switched, reset, or written.

- [ ] **Step 5: Re-fingerprint the live checkout and prove exact WIP identity**

```powershell
$liveRepo = 'C:\Users\chris and christine\Desktop\Research'
function Write-ResearchWipFingerprint {
    param(
        [Parameter(Mandatory=$true)][string]$RepoPath,
        [Parameter(Mandatory=$true)][string]$OutputPath
    )

    $paths = @(
        & git -C $RepoPath ls-files --modified --deleted
        & git -C $RepoPath diff --cached --name-only
        & git -C $RepoPath ls-files --others --exclude-standard
    ) | Sort-Object -Unique

    $entries = foreach ($relativePath in $paths) {
        $absolutePath = Join-Path $RepoPath $relativePath
        if (Test-Path -LiteralPath $absolutePath -PathType Leaf) {
            $item = Get-Item -LiteralPath $absolutePath -Force
            [ordered]@{
                path = $relativePath.Replace('\', '/')
                exists = $true
                length = [int64]$item.Length
                sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath `
                    $absolutePath).Hash
            }
        } else {
            [ordered]@{
                path = $relativePath.Replace('\', '/')
                exists = $false
                length = $null
                sha256 = $null
            }
        }
    }

    $indexScript = @'
import hashlib
import json
import subprocess
import sys

repo = sys.argv[1]


def git_bytes(*args: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", repo, *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


raw_stage = git_bytes("-c", "core.quotePath=false", "ls-files", "--stage", "-z")
records = []
for entry in raw_stage.split(b"\0"):
    if not entry:
        continue
    metadata, path_bytes = entry.split(b"\t", 1)
    mode, object_id, stage = metadata.decode("ascii").split(" ")
    blob_bytes = git_bytes("cat-file", "blob", object_id)
    records.append(
        {
            "path": path_bytes.decode("utf-8", "strict").replace(chr(92), "/"),
            "mode": mode,
            "stage": int(stage),
            "object_id": object_id,
            "blob_size_bytes": len(blob_bytes),
            "blob_sha256": hashlib.sha256(blob_bytes).hexdigest(),
        }
    )

records_bytes = json.dumps(
    records,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
).encode("utf-8")
payload = {
    "schema_version": "research-live-index-fingerprint-v1",
    "ls_files_stage_size_bytes": len(raw_stage),
    "ls_files_stage_sha256": hashlib.sha256(raw_stage).hexdigest(),
    "records_sha256": hashlib.sha256(records_bytes).hexdigest(),
    "records": records,
}
sys.stdout.write(
    json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    + "\n"
)
'@
    $indexJson = @(
        & 'C:\Python314\python.exe' -B -c $indexScript $RepoPath
    )
    if ($LASTEXITCODE -ne 0) {
        throw 'Complete staged-index fingerprint failed'
    }
    $indexStage = ($indexJson -join "`n") | ConvertFrom-Json
    if ($indexStage.schema_version -cne 'research-live-index-fingerprint-v1' -or
        @($indexStage.records).Count -eq 0) {
        throw 'Complete staged-index fingerprint is empty or malformed'
    }


    [ordered]@{
        head = (& git -C $RepoPath rev-parse HEAD).Trim()
        branch = (& git -C $RepoPath branch --show-current).Trim()
        status = @(
            & git -C $RepoPath status --porcelain=v2 --untracked-files=all
        )
        entries = @($entries)
        index_stage = $indexStage
    } | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath `
        $OutputPath -Encoding UTF8
}

$afterWip = 'C:\tmp\magent-wave-e-live-wip-after.json'
Write-ResearchWipFingerprint -RepoPath $liveRepo -OutputPath $afterWip
$beforeWipHash = (
    Get-FileHash -Algorithm SHA256 -LiteralPath `
        'C:\tmp\magent-wave-e-live-wip-before.json'
).Hash
$afterWipHash = (
    Get-FileHash -Algorithm SHA256 -LiteralPath $afterWip
).Hash
if ($beforeWipHash -cne $afterWipHash) {
    throw "Live Research WIP changed: before=$beforeWipHash after=$afterWipHash"
}
"live_wip_preserved_sha256=$afterWipHash"
```

Expected: byte-identical WIP fingerprints, including the complete staged-index
record inventory, its raw and canonical digests, and every indexed blob-byte
digest. Any independently changed live worktree or index byte blocks the
preservation claim; do not overwrite it to force equality.

- [ ] **Step 6: Record the final handoff without changing Research again**

Report all of the following from current commands, not memory:

- implementation parent SHA `P`;
- evidence child/published SHA `E`;
- `origin/main` and remote feature SHA equality;
- local clean `main` parity `0 0`;
- exact oracle `20/0/0/0` and evidence-tool `14/0/0/0` closure JUnit counts and
  both JUnit SHA-256 digests;
- root PDF size/SHA-256 and zero TeX hard errors/warning delta;
- claim-language pass and nine-equation byte identity;
- validated ledger path `.verification/wave-e/final-ledger.json` and both terminal
  claim states;
- before/after live WIP fingerprint SHA-256 equality; and
- retained `OPEN`/`INCONCLUSIVE` attraction, RG, universality, convergence, and
  physical-law-identification boundaries.

Do not ingest the correction into the wiki in this wave. Leave both worktrees in
place until the user confirms recovery is no longer needed.

---

## Self-Review Checklist

- [ ] Every requirement in design revision `c43a7c5` maps to a task above.
- [ ] Only the assigned MultiAgentELBO plan file was authored during planning.
- [ ] The implementation parent owns exactly four paths: the manuscript, oracle
  tests, evidence builder, and evidence-builder tests; no wiki or unrelated path.
- [ ] The fixed-ray ingest publication gate precedes every Wave E push when
  `c9f237d2` is absent from remote `main`.
- [ ] The six manuscript replacements at old starts 174/176/178/180/182/194 are
  literal and preserve all equations.
- [ ] RED is `2 passed, 1 failed`; GREEN is targeted `3 passed` and full
  `20 passed` with zero skips/failures/errors.
- [ ] Both exact counterexamples are symbolic/pure algebra, not numerical samples.
- [ ] Candidate and closure evidence use the exact Wave 0-conforming, create-once,
  cache-free `run-junit` adapter command; oracle/tool totals are 20 and 14.
- [ ] The base index has exactly all 16 Wave 0 roots, its environment record has
  exactly five fields with no privacy transform, and its acyclic sorted
  `{path,kind,size_bytes,sha256}` files inventory covers the twelve common public
  bytes while excluding both base/domain indexes.
- [ ] The exact dbe2263 Wave 0 plan byte and the operator-approved post-commit Wave E
  planning-release record are validated before Task 1 writes its contract, at both
  evidence stages, and again before Task 6's first gate/ref mutation; no current
  Wave E self-hash is embedded.
- [ ] Candidate and closure raw files first land outside the repository; every raw
  size/hash and deterministic privacy transform is computed before public bytes.
- [ ] Generated JUnit, scans, equation records, builds, warning controls, privacy
  records, reviews, and indexes are evidence outputs, never dependency inputs.
- [ ] `.fls` plus `.aux`/`.blg` bind every TeX include, class/style/configuration,
  bibliography, and BST input; five executable identities and Python inputs bind.
- [ ] Wave 0's frozen verification snapshot/resolver selects only the active Codex
  root; SKILL/contract/five-criteria/schema/gate size/SHA records are dependency
  inputs with privacy-safe aliases, and no independent or `.claude` fallback exists.
- [ ] Root LuaLaTeX/BibTeX, warning comparison, language scans, and equation-byte
  comparison run at the evidence child.
- [ ] AUD-20 uses high-severity escalation, independent views, skeptic,
  adjudicator, and deterministic ledger validation.
- [ ] The immutable pre-review raw/planned-public manifest exists before every
  review; every view cites it, skeptic/adjudicator prior hashes form a complete
  chain, and the final builder revalidates unchanged bytes.
- [ ] Every independent view, aggregate, and ordered comparison covers exactly all
  eight installed mathematics criteria, with derivation evidence primary.
- [ ] All reviews exist before the final closure index; the public allowlist is
  exactly 21 files or 25 under complete four-view escalation.
- [ ] Gate `start` followed directly by `validate` fails; explicit population then
  validates both terminal claims and their closure-index link.
- [ ] Only the evidence child can publish, and it fast-forwards both remote and
  clean local `main`.
- [ ] The dirty live Research review checkout remains byte-identical and is never
  advanced.
- [ ] No wiki/source-note/index/log/CUDA work is included.
- [ ] Wave E's Research ledger never enters the MultiAgentELBO aggregate ledger.
