# V1 Information-Retention Numerical Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair the v1 information-retention denominator contract and publication-precision regression, then re-pin the frozen v1 baseline without weakening its protected-blob gate.

**Architecture:** A first test-driven commit changes only the numerical guard and its audit assertions. A second commit points the existing frozen-baseline controller at that exact fix commit and regenerates the canonical legacy capture through its explicit refresh route. The original recursive Phase 2 Task 7 owns the final consolidated gates and its pending replay/log changes.

**Tech Stack:** Python 3.14, NumPy float64, `fractions.Fraction`, pytest, canonical JSON, Git detached-worktree capture.

**Spec:** `docs/superpowers/specs/2026-08-22-v1-information-retention-numerical-remediation-design.md`

## Global Constraints

- Work only in `C:\tmp\MultiAgentELBO-rg-v2-recursive-20260821` on `codex/rg-v2-recursive-closure-20260821`.
- Preserve unstaged `tests/rg_v2/test_recursive_experiment.py`, `docs/change-logs/2026-08-21.md`, and every retained JUnit XML.
- Do not add `cocycle_flow.py` to `_SEAMS`; re-pin the baseline instead.
- Do not change launcher configurations, semantic artifact hashes, metric values, or the source-fixture hash without an executed, documented scientific justification.
- CPU tests use `C:\Python314\python.exe` with `CUDA_VISIBLE_DEVICES=-1`, `PYTHONHASHSEED=0`, and `-p no:cacheprovider`.
- Run each focused command once after batched edits. The original Phase 2 Task 7 runs the final focused and broad JUnit commands.

---

### Task 1: Correct the v1 information-retention contract

**Files:**
- Modify: `src/multiagent_elbo/finite/cocycle_flow.py:558-586`
- Modify: `tests/test_lab_vs_theory_audit_remediation.py:351-375`

**Interfaces:**
- Consumes: `MI_CEILING_FLOOR`, `_mutual_information`, `capacity_information_retention`, and `one_step_pair_retention`.
- Produces: fail-closed finite-denominator validation and a six-decimal publication-resolution retention regression.

- [ ] **Step 1: Add deterministic failing denominator tests**

Add a parameterized audit test that exercises the real public
`capacity_information_retention` path while controlling only the
cancellation-prone `_mutual_information` result. Its literal cases are
`0.0`, `-1e-16`, and `1e-16`, and each must raise `ValueError`. Retain an
above-floor public-path case proving an admitted denominator is not rejected.
The production mutation caught is restoring the strict-positive lower bound.

- [ ] **Step 2: Record RED**

Run the exact new denominator selection with:

```powershell
$env:CUDA_VISIBLE_DEVICES = "-1"
$env:PYTHONHASHSEED = "0"
C:\Python314\python.exe -B -m pytest tests\test_lab_vs_theory_audit_remediation.py -k "zero_information or negative_information or subfloor_information" -q -p no:cacheprovider --basetemp=.pytest-v1-retention-red
```

Expected: exact-zero and negative cases fail because the current guard accepts
them; the positive sub-floor case already raises.

- [ ] **Step 3: Implement the minimum production correction**

Reject nonfinite `fine_information` explicitly. Reject every finite
`fine_information <= MI_CEILING_FLOOR` before forming the retention ratio.
Do not change the contraction, IPF fixture, returned dataclass, or any admitted
above-floor value.

- [ ] **Step 4: Align the published-precision assertion**

Change only the one-step pair-retention expectation to:

```python
pytest.approx(0.155747, rel=0.0, abs=5.0e-7)
```

Retain the independent capacity-retention assertion unchanged.

- [ ] **Step 5: Run GREEN once**

```powershell
$env:CUDA_VISIBLE_DEVICES = "-1"
$env:PYTHONHASHSEED = "0"
C:\Python314\python.exe -B -m pytest tests\test_lab_vs_theory_audit_remediation.py tests\test_cocycle_flow.py -q -p no:cacheprovider --basetemp=.pytest-v1-retention-green
```

Expected: zero failures and zero errors.

- [ ] **Step 6: Commit only Task 1 files**

Run `git diff --check`, stage exactly the two Task 1 files, and commit with
`fix: make information retention fail closed`. Record the full commit SHA;
Task 2 binds the refreshed baseline to it.

### Task 2: Re-pin and verify the frozen v1 baseline

**Files:**
- Modify: `tests/rg_v2/test_legacy_regression.py:18-27`
- Modify: `rg_v2/data/legacy_rescaling_v1.json`
- Create: `docs/change-logs/2026-08-22.md`

**Interfaces:**
- Consumes: the exact Task 1 commit, `_capture_legacy_snapshot`, the explicit refresh environment gate, and the existing canonical legacy manifest schema.
- Produces: a refreshed protected baseline that includes the Task 1 numerical blobs while preserving all v1 scientific identities.

- [ ] **Step 1: Point the controller at the Task 1 commit**

Set `_BASELINE` to the complete Task 1 SHA. Do not alter `_SEAMS`, protected
path discovery, output guards, or capture semantics.

- [ ] **Step 2: Record the pre-refresh failure without writing**

With the refresh environment variable absent, run the normal manifest-match
selection before changing the manifest. Expected: failure because the manifest
still binds the prior baseline revision. This command must not call `_refresh`
or write the repository manifest.

```powershell
$env:CUDA_VISIBLE_DEVICES = "-1"
$env:PYTHONHASHSEED = "0"
Remove-Item Env:RG_V2_REFRESH_LEGACY_BASELINE -ErrorAction SilentlyContinue
C:\Python314\python.exe -B -m pytest tests\rg_v2\test_legacy_regression.py -k "legacy_manifest_matches" -q -p no:cacheprovider --basetemp=.pytest-v1-rebaseline-red
```

- [ ] **Step 3: Regenerate the manifest through the explicit route**

Use the controller's task-owned external temporary output, copy the generated
canonical `legacy_rescaling_v1.json` into the repository, and remove only the
validated task-owned temporary path. Do not hand-edit captured hashes or
metric records.

```powershell
$env:CUDA_VISIBLE_DEVICES = "-1"
$env:PYTHONHASHSEED = "0"
$env:RG_V2_REFRESH_LEGACY_BASELINE = "1"
C:\Python314\python.exe -B -m pytest tests\rg_v2\test_legacy_regression.py -k "^test_refresh$" -q -p no:cacheprovider --basetemp=.pytest-v1-rebaseline-refresh
```

- [ ] **Step 4: Compare old and new scientific payloads**

Mechanically compare all launcher canonical JSON/SHA pairs, the source-fixture
hash, semantic artifact hashes, and complete serialized metric records. The
only admitted differences are baseline/revision-binding fields and the
protected source-blob map entries for the authorized Task 1 files.

- [ ] **Step 5: Run the normal legacy gate once**

```powershell
Remove-Item Env:RG_V2_REFRESH_LEGACY_BASELINE -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = "-1"
$env:PYTHONHASHSEED = "0"
C:\Python314\python.exe -B -m pytest tests\rg_v2\test_legacy_regression.py -q -p no:cacheprovider --basetemp=.pytest-v1-rebaseline-green
```

Expected: zero failures and zero errors, including fresh detached-baseline and
current captures plus the protected-blob boundary.

- [ ] **Step 6: Record the remediation**

Create `docs/change-logs/2026-08-22.md` with the authorization, Task 1 SHA,
baseline SHA, exact RED/GREEN commands and results, scientific-payload
comparison, CPU-only boundary, and the retained Phase 2 JUnit failures that
motivated the amendment.

- [ ] **Step 7: Commit only Task 2 files**

Run `git diff --check`, stage exactly the controller, manifest, and dated log,
then commit with `test: re-pin frozen v1 after retention remediation`.

## Completion handoff

After both task reviews approve, resume Task 7 of
`docs/superpowers/plans/2026-08-21-rg-v2-recursive-coarse-agent-closure.md`.
It must rerun the consolidated focused JUnit and one broad CPU JUnit at the
final revision, update its owned replay test and 2026-08-21 log, and obtain a
fresh whole-branch review. No push, merge, or live-checkout synchronization is
authorized by this plan.
