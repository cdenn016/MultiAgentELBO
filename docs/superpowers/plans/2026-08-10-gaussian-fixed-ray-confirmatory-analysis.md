# Gaussian Fixed-Ray Confirmatory Analysis Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement, verify, and artifact-bind the preregistered 30-job primary plus 10-job holdout CUDA float64 Gaussian fixed-ray confirmatory experiment without promoting finite evidence into a theorem or universality claim.

**Architecture:** Add a pure NumPy/statistics module that reduces paired jobs and computes immutable bootstrap, exact sign/binomial, and Holm results. Extend the existing Gaussian fixed-ray experiment controller with a resumable, one-job-at-a-time CUDA execution path and two-stage primary/holdout publication. Extend the click-to-run launcher with separate confirmatory gate and execution modes while preserving pilot and sentinel behavior.

**Tech Stack:** Python 3.14 CPU controller, Python 3.12 CUDA worker at `C:\anaconda\python.exe`, NumPy, standard-library `math.comb`, pytest, JUnit XML, existing `RunStore`, existing immutable CUDA worker protocol.

## Global Constraints

- Work from a clean branch based on current `origin/main`; preserve the user's live Desktop WIP.
- Use strict red-green-refactor TDD. No production change precedes its failing test.
- The scientific unit is one master-seed job; schemes and scales are repeated measurements.
- Primary inference uses only `C001`-`C030`; `H001`-`H010` remain locked until the primary record is hash-bound.
- Sentinel trajectories remain analysis-ineligible and are never reused as confirmatory observations.
- Exactly 10,000 immutable whole-job bootstrap resamples are used.
- Exactly six secondary p-values form one Holm family at familywise alpha `0.05`.
- `heavy_sweep_enabled=False` through implementation, unit/integration tests, review, CUDA worker verification, and a fresh current-revision sentinel.
- The real 40-job sweep requires a separate explicit operator opt-in and a fresh accepted confirmatory gate.
- Every CUDA claim uses `C:\anaconda\python.exe`; ordinary CPU tests use bare `python`.
- The controller never kills processes and fails closed if the accepted process set, utilization, or memory changes.
- Producer claims remain `NUMERICAL/CANDIDATE/APPLICATION_SPECIFIC`; universality and unrestricted attraction remain `OPEN/INCONCLUSIVE`.

---

### Task 1: Freeze the preregistration amendment and identity

**Files:**
- Modify: `docs/experiments/2026-08-09-gaussian-fixed-ray-preregistration.md`
- Modify: `src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py`
- Test: `tests/test_gaussian_fixed_ray_experiment.py`

**Interfaces:**
- Consumes: approved design `docs/superpowers/specs/2026-08-10-gaussian-fixed-ray-confirmatory-analysis-design.md`
- Produces: canonical preregistration SHA-256 and required literal validation for protocol amendment `2026-08-09-gaussian-fixed-ray-v1a`

- [ ] **Step 1: Write the failing amendment-identity test**

Add a test that reads the canonical LF bytes, asserts the protocol contains `2026-08-09-gaussian-fixed-ray-v1a`, `construction_residual`, `retained_beta_trend`, `basin_exit_rate`, `scheme_dispersion`, `conditioning_trend`, `rejection_rate`, and calls `_validate_preregistration()` successfully. Also mutate `exact one-sided sign test` and assert validation fails.

```python
def test_preregistration_freezes_confirmatory_analysis_amendment(tmp_path: Path):
    source = PREREGISTRATION.read_text(encoding="utf-8")
    assert "2026-08-09-gaussian-fixed-ray-v1a" in source
    for endpoint_id in SECONDARY_ENDPOINT_IDS:
        assert f"`{endpoint_id}`" in source
    assert fixed_ray_experiment._validate_preregistration(PREREGISTRATION)
    mutated = tmp_path / "mutated.md"
    mutated.write_text(source.replace("exact one-sided sign test", "unspecified test", 1), encoding="utf-8")
    with pytest.raises(ValueError, match="frozen"):
        fixed_ray_experiment._validate_preregistration(mutated)
```

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python -m pytest tests/test_gaussian_fixed_ray_experiment.py::test_preregistration_freezes_confirmatory_analysis_amendment -q`

Expected: FAIL because the amendment ID and required literals are absent.

- [ ] **Step 3: Append the approved amendment and update the canonical digest**

Add a dated amendment section reproducing the approved independent unit, paired least-favorable reductions, six nulls, exact p-values, Holm rule, bootstrap substream, rejection handling, and holdout release. Change `_PREREGISTRATION_SHA256` to the canonical LF SHA-256 of the amended file and extend `required_literals` with the amendment ID and all six endpoint IDs.

- [ ] **Step 4: Run amendment and legacy preregistration tests**

Run: `python -m pytest tests/test_gaussian_fixed_ray_experiment.py -k "preregistration" -q`

Expected: all selected tests PASS.

- [ ] **Step 5: Commit the frozen amendment**

```powershell
git add docs/experiments/2026-08-09-gaussian-fixed-ray-preregistration.md src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py tests/test_gaussian_fixed_ray_experiment.py
git commit -m "docs: freeze Gaussian confirmatory statistics"
```

### Task 2: Implement exact secondary statistics and Holm adjustment

**Files:**
- Create: `src/multiagent_elbo/realizations/gaussian/confirmatory_analysis.py`
- Create: `tests/test_gaussian_confirmatory_analysis.py`
- Modify: `src/multiagent_elbo/realizations/gaussian/__init__.py`

**Interfaces:**
- Produces: `SECONDARY_ENDPOINT_IDS`, `exact_sign_pvalue(values, boundary)`, `exact_binomial_lower_tail(events, trials, boundary_probability)`, `holm_adjust(pvalues, alpha=0.05)`
- `holm_adjust` returns JSON-safe records with endpoint ID, raw p-value, adjusted p-value, rank, and rejected flag.

- [ ] **Step 1: Write failing exact-tail tests**

Pin cases computable by hand:

```python
def test_exact_sign_pvalue_is_conservative_at_ties():
    assert exact_sign_pvalue(np.array([-1.0, -0.5, 0.0, 0.0]), 0.0) == pytest.approx(11 / 16)

def test_exact_binomial_lower_tail_uses_composite_null_boundary():
    assert exact_binomial_lower_tail(0, 30, 0.05) == pytest.approx(0.95**30)
```

- [ ] **Step 2: Run the exact-tail tests and verify RED**

Run: `python -m pytest tests/test_gaussian_confirmatory_analysis.py -k "exact_sign or exact_binomial" -q`

Expected: collection FAIL because the module does not exist.

- [ ] **Step 3: Implement exact tails with validation**

Use `math.comb`; reject Boolean/non-integer counts, nonfinite observations, empty samples, invalid boundaries, and probabilities outside `[0,1]`. Count only values strictly below the sign-test boundary.

- [ ] **Step 4: Run exact-tail tests and verify GREEN**

Run: `python -m pytest tests/test_gaussian_confirmatory_analysis.py -k "exact_sign or exact_binomial" -q`

Expected: PASS.

- [ ] **Step 5: Write failing Holm tests**

Pin order, monotonicity, cap, stable endpoint-ID tie breaking, and preservation of the declared endpoint order:

```python
def test_holm_adjusts_one_frozen_six_endpoint_family():
    raw = dict(zip(SECONDARY_ENDPOINT_IDS, [0.01, 0.04, 0.03, 0.002, 0.5, 0.04]))
    result = holm_adjust(raw)
    assert [row["endpoint_id"] for row in result] == list(SECONDARY_ENDPOINT_IDS)
    by_id = {row["endpoint_id"]: row for row in result}
    assert by_id["scheme_dispersion"]["adjusted_p"] == pytest.approx(0.012)
    assert all(0.0 <= row["adjusted_p"] <= 1.0 for row in result)
```

- [ ] **Step 6: Run Holm tests and verify RED**

Run: `python -m pytest tests/test_gaussian_confirmatory_analysis.py -k holm -q`

Expected: FAIL because `holm_adjust` is absent.

- [ ] **Step 7: Implement Holm adjustment and export the public constants/functions**

Sort by `(raw_p, endpoint_id)`, compute `(m-rank+1)*raw_p`, take the ordered cumulative maximum, cap at one, then restore `SECONDARY_ENDPOINT_IDS` order.

- [ ] **Step 8: Run the statistics module tests and commit**

Run: `python -m pytest tests/test_gaussian_confirmatory_analysis.py -q`

Expected: PASS.

```powershell
git add src/multiagent_elbo/realizations/gaussian/confirmatory_analysis.py src/multiagent_elbo/realizations/gaussian/__init__.py tests/test_gaussian_confirmatory_analysis.py
git commit -m "feat: add exact confirmatory statistics"
```

### Task 3: Implement paired summaries and immutable bootstrap analysis

**Files:**
- Modify: `src/multiagent_elbo/realizations/gaussian/confirmatory_analysis.py`
- Modify: `tests/test_gaussian_confirmatory_analysis.py`

**Interfaces:**
- Produces: `summarize_paired_job(job_record)`, `bootstrap_seed(protocol_id, job_table_sha256, endpoint_id)`, `percentile_interval(values, seed, resamples=10000)`, `analyze_primary(job_records, protocol_id, job_table_sha256)`
- `analyze_primary` returns a canonical JSON-safe dictionary and never consumes pilot, sentinel, or holdout records.

- [ ] **Step 1: Write failing paired-reduction tests**

Construct one job whose adjacent scheme is favorable and alternating scheme is unfavorable. Assert primary slope, normalized distance, beta trend, construction residual, and conditioning trend use the larger value; assert either-scheme basin/rejection uses logical OR.

- [ ] **Step 2: Run the paired-reduction test and verify RED**

Run: `python -m pytest tests/test_gaussian_confirmatory_analysis.py::test_paired_summary_uses_least_favorable_scheme_without_pseudoreplication -q`

Expected: FAIL because `summarize_paired_job` is absent.

- [ ] **Step 3: Implement scale-aware slopes and paired summaries**

Use angle values labeled `4,...,8`, beta residual transition values labeled `4,...,8`, and `log(coefficient_conditioning)` at scales `4,...,8`. Validate exact scale coverage, two frozen scheme IDs, finite numeric values, matching job identity, and Boolean event types.

- [ ] **Step 4: Run the paired-reduction test and verify GREEN**

Run the same focused test; expected PASS.

- [ ] **Step 5: Write failing bootstrap and primary-analysis tests**

Assert 10,000 whole-job resamples are deterministic across process/order changes, change when the endpoint label or job-table hash changes, preserve job pairing, and produce a primary record with exactly 30 unique `C` IDs and exactly six Holm rows. Assert any `P`, `H`, or sentinel-eligibility-false record is rejected as primary input.

- [ ] **Step 6: Run bootstrap tests and verify RED**

Run: `python -m pytest tests/test_gaussian_confirmatory_analysis.py -k "bootstrap or primary" -q`

Expected: FAIL because bootstrap/analysis functions are absent.

- [ ] **Step 7: Implement deterministic whole-job bootstrap and primary analysis**

Derive the unsigned 64-bit seed from SHA-256 of the protocol ID, job-table hash, literal `confirmatory-analysis-bootstrap-v1`, and endpoint ID. Use `np.random.Generator(np.random.PCG64(seed))`; sample job indices with shape `(10000, 30)`. Record input, index-array, and result hashes. Compute the primary null-centered two-sided p-value with `+1` correction, the supporting-distance interval, six exact secondary tests, Holm results, all frozen decision-rule inputs, and the finite `support`/`counterevidence`/`inconclusive` classification.

- [ ] **Step 8: Add conservative rejected-record tests and implementation**

Assert a rejected job remains in the 30-job denominator, counts as a rejection, never counts as favorable in sign tests, records `continuous_endpoint_censored_worst_case=true`, and cannot be silently omitted. Assert a missing job forces `inconclusive`.

- [ ] **Step 9: Run the pure analysis tests and commit**

Run: `python -m pytest tests/test_gaussian_confirmatory_analysis.py -q`

Expected: PASS.

```powershell
git add src/multiagent_elbo/realizations/gaussian/confirmatory_analysis.py tests/test_gaussian_confirmatory_analysis.py
git commit -m "feat: add paired confirmatory analysis"
```

### Task 4: Implement resumable one-job-at-a-time CUDA execution

**Files:**
- Modify: `src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py`
- Create: `tests/test_gaussian_confirmatory_experiment.py`

**Interfaces:**
- Produces: `build_confirmatory_gate_record(config, operator_opt_in)`, `run_confirmatory_job(...)`, `run_confirmatory_primary(...)`
- Reuses: `_run_or_resume_worker_job`, `_capture_idle_gpu_gate_after_cooldown`, `_validate_gate_recheck`, `generate_initial_coefficients`, `_sentinel_endpoint`

- [ ] **Step 1: Write failing confirmatory-gate tests**

Assert a gate can bind a CUDA float64 config with `heavy_sweep_enabled=True`, records `execution_scope=gaussian_fixed_ray_confirmatory_40_job`, requires operator opt-in, binds the current source/config/preregistration/lock/worker identities, and cannot be accepted by the sentinel path.

- [ ] **Step 2: Run gate tests and verify RED**

Run: `python -m pytest tests/test_gaussian_confirmatory_experiment.py -k gate -q`

Expected: FAIL because the confirmatory gate API is absent.

- [ ] **Step 3: Implement the separate confirmatory gate schema**

Do not weaken `build_cuda_gate_record` or sentinel validation. Add a distinct schema and validator whose config binding includes `heavy_sweep_enabled=True` and the amended preregistration digest.

- [ ] **Step 4: Run gate tests and verify GREEN**

Run the same focused tests; expected PASS.

- [ ] **Step 5: Write failing single-job execution tests**

Inject the existing worker-call seam and gate-recheck seam. Assert one `C` job executes exactly two schemes by eight sequential CUDA steps, uses the immutable CPU-generated initial literal, performs one fresh recheck before the outer job, respects a five-minute deadline, captures peak memory/provenance, and emits per-scheme trajectory/endpoints. Assert process-set drift, nonzero utilization, changed memory, expiry, identity drift, or exhausted retry fails closed without starting the next job.

- [ ] **Step 6: Run the single-job tests and verify RED**

Run: `python -m pytest tests/test_gaussian_confirmatory_experiment.py -k "single_job or recheck or deadline" -q`

Expected: FAIL because `run_confirmatory_job` is absent.

- [ ] **Step 7: Implement single-job execution**

Use one CUDA worker exchange per scheme/step and immutable IDs `confirmatory.<job_id>.<scheme>.stepNN.cuda`. Disable exchange-local retries in this path; the one authorized infrastructure retry applies to the entire paired outer job. Bind every attempt context to the accepted confirmatory gate, the immediate outer-job recheck, source/config/job-table/preregistration identities, and the original job literal hash.

- [ ] **Step 8: Write failing primary-sequence and resume tests**

Assert only `C001`-`C030` are eligible, order is deterministic, terminal valid staging records resume without rerun, incomplete attempts consume the one retry, no favorable-result early stopping occurs, and every planned/completed/rejected/retried/missing job remains represented.

- [ ] **Step 9: Implement primary sequencing and run integration tests**

Run: `python -m pytest tests/test_gaussian_confirmatory_experiment.py -k "primary or resume or retry" -q`

Expected: PASS after minimal implementation.

- [ ] **Step 10: Commit CUDA execution support**

```powershell
git add src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py
git commit -m "feat: add gated Gaussian confirmatory execution"
```

### Task 5: Implement two-stage publication and holdout release

**Files:**
- Modify: `src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py`
- Modify: `src/multiagent_elbo/realizations/gaussian/confirmatory_analysis.py`
- Modify: `tests/test_gaussian_confirmatory_experiment.py`
- Modify: `tests/test_gaussian_confirmatory_analysis.py`

**Interfaces:**
- Produces: `publish_confirmatory_experiment(...)`
- Publishes: `confirmatory_job_table.json`, `confirmatory_endpoints.json`, `primary_analysis.json`, `holdout_analysis.json`, `confirmatory_execution.json`, `confirmatory_arrays.npz`, `metrics.json`

- [ ] **Step 1: Write failing primary-before-holdout tests**

Assert holdout execution is rejected until `primary_analysis.json` is canonicalized and its SHA-256 is stored in the staging state. Assert sentinel records are rejected even when their IDs match `H001`/`H010`. Assert holdout output contains no p-values or Holm decisions and binds the exact primary digest.

- [ ] **Step 2: Run holdout-release tests and verify RED**

Run: `python -m pytest tests/test_gaussian_confirmatory_experiment.py -k holdout -q`

Expected: FAIL because two-stage publication is absent.

- [ ] **Step 3: Implement primary finalization and holdout release**

Canonicalize both primary execution and primary analysis JSON with sorted keys, compact separators, ASCII, and `allow_nan=False`. Atomically write and hash the exact bytes, validate the primary analysis by recomputation from the execution record, require all 30 primary IDs terminal-complete with no missing IDs, and only then enable the ten `H` jobs. Analyze holdout descriptively with identical frozen summaries and 10,000-job bootstrap intervals but no p-values, no Holm family, and no classification rewrite.

- [ ] **Step 4: Write failing final artifact-contract tests**

Using injected tiny deterministic worker fixtures, assert all seven declared artifacts are present, no undeclared files enter `RunStore`, all hashes recompute, `confirmatory_executed=true` appears only after 40 terminal job records and both analysis stages validate, and metrics retain `NUMERICAL/CANDIDATE/APPLICATION_SPECIFIC`.

- [ ] **Step 5: Implement publication and verify tests**

Run: `python -m pytest tests/test_gaussian_confirmatory_experiment.py tests/test_gaussian_confirmatory_analysis.py -q`

Expected: PASS.

- [ ] **Step 6: Commit two-stage publication**

```powershell
git add src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py src/multiagent_elbo/realizations/gaussian/confirmatory_analysis.py tests/test_gaussian_confirmatory_experiment.py tests/test_gaussian_confirmatory_analysis.py
git commit -m "feat: publish two-stage Gaussian confirmation"
```

### Task 6: Add click-to-run confirmatory modes without weakening pilot/sentinel controls

**Files:**
- Modify: `run_gaussian_fixed_ray_lab.py`
- Modify: `tests/test_gaussian_fixed_ray_experiment.py`
- Modify: `tests/test_gaussian_confirmatory_experiment.py`

**Interfaces:**
- Consumes: `build_confirmatory_gate_record`, `publish_confirmatory_experiment`
- Produces: launcher modes `confirmatory_gate` and `confirmatory_run` using `.verification/gaussian-fixed-ray-confirmatory-control.json`

- [ ] **Step 1: Write failing launcher-mode tests**

Pin the separate control schema:

```json
{"mode":"confirmatory_gate","operator_opt_in":true,"accepted_gate_sha256":"","accepted_sentinel_manifest_sha256":"<64 hex>"}
```

Assert `confirmatory_gate` keeps execution disabled while publishing a digest; `confirmatory_run` requires the exact accepted gate and successful current-revision sentinel manifest, sets `heavy_sweep_enabled=True`, and rejects pilot/sentinel controls as heavy authorization.

- [ ] **Step 2: Run launcher tests and verify RED**

Run: `python -m pytest tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py -k launcher -q`

Expected: FAIL because confirmatory modes are absent.

- [ ] **Step 3: Implement separate launcher paths**

Add separate confirmatory control, gate, and staging paths. Preserve the existing three-key sentinel sidecar and all `pilot`, `cuda_gate`, and `cuda_sentinel` behavior byte-for-byte. Print the confirmatory gate digest and required acceptance instruction; never infer acceptance from GPU idleness alone.

- [ ] **Step 4: Run launcher and Gaussian focused suites**

Run: `python -m pytest tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py tests/test_gaussian_confirmatory_analysis.py -q`

Expected: PASS.

- [ ] **Step 5: Commit launcher support**

```powershell
git add run_gaussian_fixed_ray_lab.py tests/test_gaussian_fixed_ray_experiment.py tests/test_gaussian_confirmatory_experiment.py
git commit -m "feat: add confirmatory launcher modes"
```

### Task 7: Verify implementation, review, and prepare—but do not start—the real sweep

**Files:**
- Create: `.verification/gaussian-confirmatory-implementation.xml` (ignored)
- Create: `.verification/gaussian-confirmatory-cuda-worker.xml` (ignored)
- Update: `.verification/ledger.json` (ignored)
- Modify only if evidence requires correction: `docs/results/2026-08-09-gaussian-fixed-ray-results.md`

**Interfaces:**
- Produces: current-revision machine-readable CPU/CUDA evidence, independent review decisions, validated ledger, and a neutral confirmatory operator sidecar.

- [ ] **Step 1: Run the full CPU suite with JUnit**

Run: `python -m pytest -q --junitxml=.verification/gaussian-confirmatory-implementation.xml`

Expected: zero failures/errors; totals parsed from JUnit.

- [ ] **Step 2: Verify the real CUDA interpreter and focused worker test**

Run: `C:\anaconda\python.exe -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"`

Expected: CUDA available on the RTX 5090.

Run: `C:\anaconda\python.exe -m pytest tests/test_cuda_backend.py -k cuda -q --junitxml=.verification/gaussian-confirmatory-cuda-worker.xml`

Expected: selected CUDA worker test PASS, not skip.

- [ ] **Step 3: Run independent code, mathematics, and experiment reviews**

Review the exact clean source revision. Code review must check fail-closed execution/resume semantics and artifact validation. Mathematics review must confirm no theorem-boundary promotion. Experiment review must independently recompute the exact p-values, Holm adjustments, bootstrap identities, and two-stage eligibility rules.

- [ ] **Step 4: Validate the current-revision ledger**

Record separate claims for statistical implementation correctness, execution-controller correctness, and scientific closure. The first two may close only with current evidence. The scientific claim remains `INCONCLUSIVE` until the 40-job run is complete and independently adjudicated.

- [ ] **Step 5: Run a fresh current-revision CUDA sentinel**

Capture and explicitly accept a new sentinel gate, run the five frozen parity-only jobs, and verify its manifest/artifact hashes. Do not reuse the prior `8988637` sentinel after source changes.

- [ ] **Step 6: Reset the confirmatory operator sidecar to neutral**

The committed/default state must be:

```json
{"mode":"pilot","operator_opt_in":false,"accepted_gate_sha256":"","accepted_sentinel_manifest_sha256":""}
```

- [ ] **Step 7: Commit any evidence-backed documentation correction**

If no tracked correction is needed, leave the source tree unchanged. Do not commit ignored run evidence.

### Task 8: Execute and adjudicate the real 40-job sweep after explicit opt-in

**Files:**
- Create: ignored confirmatory staging and final artifact bundle
- Update: `.verification/ledger.json` (ignored)
- Modify: `docs/results/2026-08-09-gaussian-fixed-ray-results.md`

**Interfaces:**
- Consumes: clean reviewed revision, accepted current sentinel manifest, explicit heavy-sweep operator opt-in, fresh confirmatory gate
- Produces: complete immutable confirmatory artifact bundle and bounded scientific result

- [ ] **Step 1: Obtain explicit heavy-sweep authorization**

Ask the operator to accept the exact confirmatory gate digest and any observed stable resident PIDs. Do not treat earlier sentinel acceptance or general GPU availability as this authorization.

- [ ] **Step 2: Run all 30 primary jobs serially**

Recheck the GPU immediately before each outer job. Preserve staging and resume only validated immutable exchanges. Do not stop for scientific results.

- [ ] **Step 3: Finalize and hash-bind primary analysis**

Recompute all job summaries, bootstrap records, exact tests, Holm family, and decision rules independently before releasing holdout.

- [ ] **Step 4: Run all 10 holdout jobs serially and publish descriptive replication**

Use the same fresh recheck and retry rules. Do not compute holdout p-values or change the primary classification.

- [ ] **Step 5: Independently adjudicate the final bundle**

Verify all 40 terminal job records, trajectory/endpoints, bootstrap seeds/hashes, raw and adjusted p-values, classification, missing/rejected counts, manifest identities, runtime, and memory. Keep unrestricted attraction and universality `OPEN/INCONCLUSIVE` regardless of finite outcome.

- [ ] **Step 6: Update results and ledger, then run final regression suite**

Run the full CPU suite and focused CUDA worker test again at the exact documentation revision. Record current JUnit and artifact hashes in the ignored ledger.

- [ ] **Step 7: Commit, push, serially merge, and fast-forward safe clean checkouts**

Fetch and verify `origin/main`, merge only after all evidence gates pass, push, verify remote parity, and fast-forward only clean/nonoverlapping checkouts. Preserve the live Desktop WIP exactly.

## Plan self-review

- Spec coverage: all approved statistical, execution, holdout, provenance, artifact, and claim-boundary requirements map to Tasks 1-8.
- Placeholder scan: every task contains concrete tests, implementation behavior, commands, and expected outcomes.
- Type consistency: launcher, controller, analysis, and publication interfaces use the same names throughout the plan.
- Execution boundary: Task 8 cannot begin from Task 7 without a new explicit heavy-sweep authorization.
