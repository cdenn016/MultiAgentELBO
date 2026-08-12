# Audit 04 — Adversarial code audit, `MultiAgentELBO`

Auditor role: senior scientific-software auditor / numerical analyst
Date: 2026-08-11
Repo HEAD audited: `c101b8a0e6ba534c72c22047985670a3dbcd8885`
Prior audit baseline: `aedc6621a4e4f1c725a54f8b287aac425ef833d8`

**`git diff --stat aedc662 HEAD -- src tests tools Theory` is empty.** The three commits since the
prior audit are documentation only (`f078e66`, `c43a7c5`, `c101b8a`). Therefore **every one of
AUD-01..AUD-22 is still present in source**; nothing has been remediated. I spot-verified nine of
them with runnable probes (Section 1) and then spent the remaining effort on new defects
(Section 2), test-suite adequacy (Section 3), and the theory-vs-self question (Sections 5–6).

Environment: Linux sandbox, Python 3.10, numpy 2.2.6, scipy 1.15.3. Repo targets Python 3.14 on
Windows; 764 of ~890 collectible tests pass here, the 125 failures are all environmental
(`tomllib` absent; `cuda_worker_python = C:\anaconda\python.exe` is not an absolute POSIX path;
launcher subprocess tests). No CUDA was available or used.

---

## 0. Executive assessment

This is a genuinely disciplined codebase. The core mathematics — KL chain rule, law of total
covariance, Hoeffding/Möbius decomposition, Schur complement, Gaussian gauge congruence, softmax
stability, DQM remainder normalization — is **correct**; I re-derived and re-implemented each one
independently and found no disagreement with the docstrings. The unit tests have real teeth:
all ten deliberate math mutations I injected were caught (Section 3.1). The exact-rational oracle
lane is a real independent reimplementation, not a mirror of the float code.

The defects are not in the formulas. They are in three places:

1. **The seed does not reach the science.** `run.seed` is hashed into config identity, written into
   the run-directory name, and serialized as RNG provenance in every manifest — and in 11 of 12
   experiment modules it has **zero** effect on any output. The 40-job Gaussian fixed-ray study,
   the only "stochastic replication" in the project, draws its initial conditions from three
   hard-coded integer literals that ignore `run.seed` entirely (N-01, HIGH).
2. **Two of the eight conjuncts that decide the confirmatory classification are the literal
   `True`.** `premises_passed=True, gpu_gate_complete=True` are passed at the only production call
   site, are serialized into the published analysis JSON as if they were checked facts, and no test
   anywhere passes `False` for either (N-02, HIGH). The project's own diagnostic module records the
   contradicting `"actual_run_premises_validated": False`.
3. **The provenance apparatus is disproportionate to the science it protects.** 17,857 lines of
   `Theory/verification` build-audit/lifecycle-gate machinery guard a 24-file LaTeX manuscript and a
   16,484-line source tree, and the flagship 40-job / 640-process / 3,644-second GPU experiment
   computes `A^n c` for a fixed 6×6 row-stochastic matrix, whose convergence is Perron–Frobenius and
   is not in doubt (N-09, N-10, Section 6).

New findings: **3 HIGH, 6 MEDIUM, 5 LOW**.

---

## 1. Status of the 22 known findings

All still present (source unchanged). Verified by probe:

| ID | Status | Evidence |
|---|---|---|
| AUD-03 | **PRESENT** | `NumericsConfig(atol=1.0, rtol=1.0)` is parser-legal (`config.py:240-241`). Probe: `ProbabilityMeasure(("a","b"),(0.4,0.4))` → `total_mass = 0.8`; `ProbabilityMeasure(("a","b"),(0.0,0.0))` accepted, `total_mass = 0.0`; `MarkovKernel` with all-zero rows accepted, `rowsums=[0. 0.]`. With `q=(0.3,0.5)`: `free_energy = 0.0699`, so `ELBO = -0.0699 > log evidence = -0.2231` — the ELBO bound is violated. |
| AUD-04 | **PRESENT** | `target_metric(1e300, tolerance=inf, target=0.0)` → `status="pass"`. `MetricRecord(value=nan, tolerance=-1.0, status="banana", ...)` constructs without error (`experiment_support.py:74-81` validates only `theorem_status`/`verification_state`/`claim_origin`). |
| AUD-05 | **PRESENT** | `agent_network.py:672-691` returns `EVIDENCE_VERIFIED` from a caller-supplied bool; experiment overrides to `CANDIDATE` at `agent_network_experiment.py:325`. |
| AUD-06 | **PRESENT** | `matrix_dimension != 2` is rejected only in `run_gaussian_fixed_ray_experiment` (`fixed_ray_experiment.py:3162-3163`). `run_cuda_sentinel` (`:1583`) and `publish_confirmatory_experiment` (`:2448`) have no such guard and call `build_preregistered_system()` unconditionally (`:1642`, and via `run_confirmatory_job` `:732`/`:1105`). |
| AUD-07 | **PRESENT** | `tools/cuda_worker.py:385` `device = torch.device("cuda:0")`; `:378` `torch.use_deterministic_algorithms(True, warn_only=False)`. `device_index` / `deterministic` never enter the request manifest (`cuda_backend.py:394-404`). |
| AUD-12 | **PRESENT** | `RngStreams.from_seed(7)`; `s.spawn_keys["problem"] = (999,)` changes `s.provenance()` from `[0]` to `[999]` without changing the generators. |
| AUD-13 | **PRESENT** | `p.masses.flags.owndata == True`; `p.masses.setflags(write=True); p.masses[0] = -5.0` → `total_mass = -4.5` on a live `ProbabilityMeasure`. |
| AUD-14 | **PRESENT** | Edge block `diag(-1e-5, 1e6)` accepted; assembled Laplacian minimum eigenvalue `-1.99999798e-05` (`interactions.py:45-52`). |
| AUD-15 | **PRESENT** | See runnable demo below. |
| AUD-16 | **PRESENT** | `information_history.py:274-278` still uses `atol + rtol*max(1, ‖defect‖)`. |
| AUD-17 | **PRESENT** | `base_fisher_cocycle_residual_forms(fisher_defect=[[0,7],[-3,2]], pushed_fine_jet=[1,2], horizontal_anomaly=[3,-5])` returns all three forms `= 46` for a **nonsymmetric indefinite** matrix. Algebraically `form_a = form_b = form_c = -vᵀMa - aᵀMv - aᵀMa` for any `M`; the check is an identity, not a Fisher fact. |
| AUD-18 | **PRESENT** | 200,000 random near-identical normalized pairs; most negative KL observed `-4.489e-16`. |
| AUD-19 | **PRESENT** | `FixedRaySystem(matrix_direction=diag(inf, 1.0), ...)` is **accepted** (`np.array_equal(M, M.T)` is True for `inf`, `eigvalsh` gives `[1, inf]`, min > 0); resulting `coupling_matrices` are non-finite and `scalarized_ray_construction_residuals = [nan nan nan]`. `diag(1e13, 1.0)` (condition 1e13) also accepted. |
| AUD-01/02/08/09/10/11/20/21/22 | **PRESENT** | Confirmed by source read: `artifacts.py:128` writes `{name: "complete"}` with no digest; `figures.py:253-257` `for path in published: path.unlink(missing_ok=True)`; `config.py:240-241` unbounded tolerances; `scale_cocycle_experiment.py` toggles unimplemented. |

### AUD-15 runnable demonstration

```python
from multiagent_elbo.finite.information_history import _spectral_diagnostics
import numpy as np
F, rc = np.diag([1e-2, 1e-4]), 1e-3
rank, *_ = _spectral_diagnostics(F, rc)                   # cutoff = rc * max(1, lmax) = 1e-3
proj = F @ np.linalg.pinv(F, rcond=rc, hermitian=True)    # cutoff = rc * lmax      = 1e-5
```
```
reported rank = 1   nullity = 1   reported cutoff = 0.001
pinv cutoff = 1e-05  projector = [[1. 0.] [0. 1.]]  -> retained rank = 2
DISAGREEMENT: True
```
The `max(1.0, ...)` floor at `information_history.py:80` also makes the reported rank **not
scale-invariant** — the same Fisher direction is rank 0 at scale `1e-3` and rank 1 at scale `1`:
```
Fisher = diag(1.0, 1e-4), rcond = 1e-3
  scaled by 0.001 -> reported rank = 0
  scaled by 1     -> reported rank = 1
  scaled by 1000  -> reported rank = 1
```

---

## 2. New findings

### N-01 — HIGH — PROVENANCE GAP — `run.seed` is hashed and published but does not reach the science

`src/multiagent_elbo/runtime.py:41-55`, 12 call sites, `realizations/gaussian/fixed_ray_experiment.py:2758-2762`

`RngStreams.from_seed(config.run.seed)` is called in twelve experiment modules. Its four generators
are consumed in **exactly one**:

```
agent_network_experiment.py           generators_consumed=0
attention_experiment.py               generators_consumed=0
categorical_dqm_experiment.py         generators_consumed=0
counterexample_experiment.py          generators_consumed=0
finite/experiment.py                  generators_consumed=0
information_history_experiment.py     generators_consumed=0
scale_cocycle_experiment.py           generators_consumed=0
theory_oracle_experiment.py           generators_consumed=0
holonomy_experiment.py                generators_consumed=0
realizations/gaussian/experiment.py   generators_consumed=1   <-- streams.problem, line 415
fixed_ray_diagnostic_experiment.py    generators_consumed=0
fixed_ray_experiment.py               generators_consumed=0
```

In every other module the generators are constructed and immediately discarded; only
`streams.provenance()` — `{"seed": N, "named_streams": {"problem": [0], ...}}` — is written into the
manifest, beside results that do not depend on it. `run.seed` still enters `config_sha256` and the
run directory name `f"{config_hash}-{config.run.seed}"` (`artifacts.py:48-52`), so changing the seed
produces a *different run identity with byte-identical science*.

Worse, in the flagship experiment the seed is bypassed by a second, hard-coded RNG path:

```python
# fixed_ray_experiment.py:2758-2762
groups = (
    ("P",  4, 202608090001, "pilot"),
    ("C", 30, 202608090101, "confirmatory_primary"),
    ("H", 10, 202608090201, "confirmatory_holdout"),
)
```
`master_seed = first_seed + offset` — a literal, independent of `config.run.seed`. The 30 "primary"
initial coefficient vectors come from `generate_initial_coefficients(master_seed, job_id)`
(`fixed_ray.py:182-192`), which opens a *fresh* `np.random.default_rng(job_seed(...))`. So the only
random quantity in the entire 40-job confirmatory study is a frozen literal, while the manifest
records `rng.seed = 20260809` and per-stream spawn keys as if the results were a draw from that
stream.

Consequence: the study is a single deterministic point. It cannot be re-drawn under a different
seed to check sampling variability, and the published RNG provenance is misleading about what
determined the numbers.

**Fix.** Either (a) delete `RngStreams` from every module that does not consume a generator and stop
recording RNG provenance there, or (b) make it load-bearing. For the fixed-ray path, derive
`master_seed` from `config.run.seed` (e.g. `job_seed(config.run.seed, job_id)`) so the
preregistered draw is actually bound to the hashed configuration, and record the derivation rule.
Add a regression test asserting that two different seeds produce different `initial_coefficients`.

---

### N-02 — HIGH — VACUOUS TEST / DEAD MACHINERY — two scientific gate flags are hard-coded `True`

`realizations/gaussian/fixed_ray_experiment.py:2503-2504`; `confirmatory_analysis.py:306-322, 488-510, 540-542`

```python
# fixed_ray_experiment.py:2496-2506 — the ONLY production call site
primary_analysis = analyze_primary(
    primary_records,
    protocol_id="2026-08-09-gaussian-fixed-ray-v1a",
    job_table_sha256=job_table_sha256,
    decision_stability=bool(
        sentinel_identity.get("scientific_decision_parity_passed", True)
    ),
    premises_passed=True,
    gpu_gate_complete=True,
    ...
```

Both flags are load-bearing in the classifier:

```python
# confirmatory_analysis.py:488-510
support = (... and decision_stability and premises_passed and gpu_gate_complete)
forced_inconclusive = (interval_half_width > 0.02 or bool(missing_job_ids)
                       or not decision_stability or not premises_passed
                       or not gpu_gate_complete)
```

and both are serialized into the published artifact (`:541-542`) as `"premises_passed": true`,
`"gpu_gate_complete": true` — presented as findings. `grep -rn "premises_passed=False|gpu_gate_complete=False" tests src`
returns **nothing**: no test in the 20,705-line suite ever exercises the `False` branch. If I
deleted lines 495-496 and 508-509 entirely, no test would go red and no output would change.

This is directly contradicted by the project's own diagnostic module, which is honest about the
same question:

```python
# realizations/gaussian/fixed_ray_diagnostics.py:265
"actual_run_premises_validated": False,
```

`decision_stability` is at least reachable in principle, but `_validate_confirmatory_sentinel_bundle`
raises on `scientific_decision_parity_passed is not True` (`:2356`) and then returns the literal
`"scientific_decision_parity_passed": True` (`:2443`), so it too is `True` on every path that
survives to the call.

**Fix.** Compute `premises_passed` from an explicit, enumerated premise checklist evaluated against
the executed system (basin membership, positivity, primitivity, scale window, uncensoring), and
`gpu_gate_complete` from the gate record fields actually observed. Add regression tests that force
each to `False` and assert `classification == "inconclusive"`. Until then, remove both from the
published record rather than shipping asserted literals as scientific status.

---

### N-03 — HIGH — NUMERICAL HAZARD — the CUDA repeatability lane cannot fail

`realizations/gaussian/fixed_ray_experiment.py:1775-1780`; `cuda_backend.py:648-687`

The sentinel runs the same CUDA kernel twice and compares:

```python
"worker_cuda_repeatability": parity_diagnostics(
    lanes["worker_cuda"][job_index, step, :],
    lanes["worker_cuda_repeat"][job_index, step, :],
    dtype="float64",
    condition_number=condition,
),
```

The worker sets `torch.use_deterministic_algorithms(True, warn_only=False)` and pins
`CUBLAS_WORKSPACE_CONFIG=:4096:8`. Under that contract the two lanes must be **bit-identical**. But
`parity_diagnostics` grades them with `atol = 1e-12·√cond`, `rtol = 1e-10·√cond`:

```
injected relative drift 1e-11 -> passed = True   (atol=1.67e-12, rtol=1.67e-10)
injected relative drift 1e-10 -> passed = True
```

A genuine loss of GPU determinism — a changed reduction order, a nondeterministic kernel selection,
a TF32 leak — produces relative drift of order `1e-14`–`1e-11` and **passes**. The repeatability
lane, the one comparison in the whole sentinel that has an exact expected answer, is tested with a
tolerance five orders of magnitude too loose to detect the failure it exists to detect.

**Fix.** Compare `worker_cuda` and `worker_cuda_repeat` with `np.array_equal` (or SHA-256 of the
canonical byte encoding — the machinery already exists in `canonical_array_sha256`). Keep the
tolerance-based rule only for genuinely cross-implementation lanes.

---

### N-04 — MEDIUM — NUMERICAL HAZARD — parity tolerance is condition-scaled by the wrong operator

`fixed_ray_experiment.py:1643`; `cuda_backend.py:665-671`; `tools/cuda_worker.py:396`

```python
condition = float(np.linalg.cond(system.matrix_direction))   # fixed_ray_experiment.py:1643
```
is threaded into every `parity_diagnostics(...)` call. But `matrix_direction` is the frozen 2×2 ray
`[[2, 0.5], [0.5, 1]]`, and **it never enters the arithmetic being compared**. The worker computes

```python
pieces.append(coefficients[start:stop] @ spatial_map.T)   # cuda_worker.py:396
```

`matrix_direction` is passed to the worker only so its condition number can be returned. The
operator whose conditioning actually governs the achievable agreement is `spatial_map`:

```
cond(matrix_direction 2x2)             = 2.784   -> parity atol=1.67e-12, rtol=1.67e-10
cond(spatial_map adjacent_pairs)       = 2.500
cond(spatial_map balanced_alternating) = 8.190
achievable float64 relative agreement for a 6-term dot product ~ 1.33e-15
parity rtol is looser than achievable by a factor of ~1.25e5
```

The scaling is therefore both bound to an irrelevant matrix and ~5 orders of magnitude too generous
for the operation performed. "CPU/CUDA parity established" means much less than a reader would
assume.

**Fix.** Scale by `cond(spatial_map)` for the lane being compared, and declare the tolerance as a
multiple of the forward error bound for a length-6 dot product (`n·eps·cond`), not as a round
literal.

---

### N-05 — MEDIUM — PROVENANCE GAP — the config hash silently omits the entire COMPUTE section

`config.py:615-625`, `config.py:168-179`

```python
payload.pop("_compute_explicit")
if not config.compute_explicit:
    payload.pop("compute")
```

When `COMPUTE` is not supplied, `_default_compute_config()` is used for execution but is **excluded
from the hashed canonical JSON**. Probe:

```
implicit-compute canonical JSON contains 'compute': False
executed backend/dtype/batch_size: cpu float64 4096
```

Seven of twelve launchers omit `COMPUTE` (`run_attention_lab.py`, `run_categorical_dqm_lab.py`,
`run_finite_counterexample_lab.py`, `run_finite_lab.py`, `run_gauge_holonomy_lab.py`,
`run_gaussian_lab.py`, `run_information_history_lab.py`). For those runs, `backend`, `dtype`,
`batch_size`, `deterministic` and `cuda_worker_python` all affect execution and none are covered by
`config_sha256`. If `_default_compute_config()` changes in a future revision, previously published
manifests keep the same config hash while the executed compute changes. Symmetrically, an implicit
config and an explicit config with byte-identical defaults hash differently despite identical
semantics.

**Fix.** Always serialize the resolved `compute` section; record `compute_explicit` as a separate,
also-hashed boolean if the distinction matters.

---

### N-06 — MEDIUM — DEAD MACHINERY — hashed compute surface with no executing path

`config.py:558-600`; `cuda_backend.py:206-207`; `tools/cuda_worker.py:284-285, 379-380, 385`

`dtype ∈ {float32, bfloat16}`, `allow_tf32`, and `device_index > 0` are all parser-legal, validated
against a cross-field policy, and folded into the config hash. None of them can execute:

- every entry point demands float64 (`run_gaussian_fixed_ray_experiment:3164`,
  `run_cuda_sentinel:1598`, `publish_confirmatory_experiment:2461`);
- `cuda_backend.py:206-207` and `cuda_worker.py:284-285` reject `bfloat16` outright;
- `cuda_worker.py:379-380` forces `matmul.allow_tf32 = False` / `cudnn.allow_tf32 = False`
  regardless of the configured `allow_tf32`, and `cuda_backend.py:357-358` then *asserts* they are
  `False`;
- `cuda_worker.py:385` hard-codes `cuda:0` regardless of `device_index`.

This is AUD-07 plus two more ignored fields (`allow_tf32`, and `dtype` beyond float64). The
`allow_tf32` cross-field rule at `config.py:594-600` is elaborate policy guarding an unreachable
state.

**Fix.** Reject `dtype != "float64"`, `allow_tf32 = True`, and `device_index != 0` in
`_resolve_compute_config` until a path implements them, or carry them into the worker request and
verify them in `validate_worker_provenance`.

---

### N-07 — MEDIUM — VACUOUS TEST — `defect_is_psd` is PSD by construction

`finite/fisher.py:104-112, 126-144`; asserted at `tests/test_fisher.py:153`

```python
conditional_covariance = np.zeros_like(fine_fisher)
for target_index in range(len(channel.target_labels)):
    deviations = values - coarse_score[target_index]
    conditional_covariance += np.einsum("x,xi,xj->ij", joint[:, target_index], deviations, deviations)
```

`joint[:, z] = p(x)·K(z|x) ≥ 0` entrywise, so each term is a nonnegative-weighted Gram matrix and
the sum is PSD identically. `minimum_defect_eigenvalue` and `defect_is_psd` therefore measure
floating-point roundoff, not any property of the model, channel, or score. 3,000 random
`(p, K, centered s)` draws:

```
min over 3000 draws of minimum_defect_eigenvalue: 5.538e-04
any defect_is_psd False? False
```

Mutating `defect_is_psd=minimum_defect_eigenvalue >= -tol` to `defect_is_psd=True` breaks exactly
one assertion across `test_fisher.py + test_categorical_dqm*.py` (78 tests still pass). The
`FisherChannelResult` fields read like a verified information-loss inequality; they are a
tautology plus a roundoff monitor.

Note the *contrast*: `residual = fine_fisher - coarse_fisher - conditional_covariance` **is** a real
check (the law of total covariance can fail if the coarse score is computed wrongly), and my
mutation `deviations = values - center` was caught by 5 tests. Keep the residual, rename the PSD
field to something like `defect_roundoff_minimum_eigenvalue`, and document that PSD is structural.

---

### N-08 — MEDIUM — DEAD MACHINERY — duplicated gate condition presented as two checks

`fixed_ray_experiment.py:1947-1948`, `2355-2356`, `1792-1798`

```python
"all_parity_passed": scientific_decision_parity_passed,
"scientific_decision_parity_passed": scientific_decision_parity_passed,
```
Two keys, one variable. `_validate_confirmatory_sentinel_bundle` then checks them as if independent:
```python
or parity.get("all_parity_passed") is not True
or parity.get("scientific_decision_parity_passed") is not True
```
Separately, step-level parity failure raises at `:1794-1798` *before* the record is emitted, so the
80-record `parity_records_valid` loop at `:2222-2255` can only be false for a tampered file. That is
a legitimate tamper check, but it is presented in the manifest as an independent scientific
verification of parity, which it is not.

**Fix.** Emit one flag, or compute `all_parity_passed` from the step records and
`scientific_decision_parity_passed` from the endpoint/stratum records separately.

---

### N-09 — MEDIUM — MATH/METHOD — the primary endpoint regresses a geometric decay on a linear scale

`confirmatory_analysis.py:190, 440, 488-489`; `fixed_ray.py:245-312`

The project has already certified that the `-0.02` endpoint is unreachable. The *cause* should be
stated plainly: `summarize_paired_job` takes `_ols_slope(angles[4:9])` — an ordinary least-squares
slope of the **raw** projective angle — while the angle decays geometrically (`θ_{n+1} ≈ |λ₂| θ_n`).
By scale 4 the angle is already `O(10⁻²)`, so the absolute per-step decrement is bounded by the
angle itself. Reproduced across all 30 primary jobs × 2 schemes:

```
angles at scales 0..8 (job C001, adjacent_pairs):
  5.43e-01 2.37e-01 9.64e-02 3.86e-02 1.55e-02 6.19e-03 2.47e-03 9.90e-04 3.96e-04
OLS slope of ANGLE over scales 4..8, min/max over 60 (job,scheme): -0.005734 .. -0.0000857
frozen criterion needs the bootstrap UPPER bound of the median slope <= -0.02
max observed |slope| = 0.005734  -> criterion structurally unreachable
```

The scale-natural statistic makes the same data decisive and near-degenerate:

```
OLS slope of log(angle) over scales 4..8, min/max over 30 jobs: -0.916284 .. -0.916245
```
i.e. `log|λ₂| = log 0.4 = -0.91629`, reproduced to 4×10⁻⁵ across every job.

**Fix.** Any successor preregistration should use `log θ` (or `θ_{n+1}/θ_n`) as the endpoint. Record
in the diagnostic that the failure mode was a unit/scale mismatch in the endpoint definition, not a
property of the dynamics.

---

### N-10 — MEDIUM — DEAD MACHINERY (process theater) — the flagship experiment tests Perron–Frobenius

`fixed_ray.py:137-164, 245-312`

`build_preregistered_system()` freezes two 6×6 maps. Both are **row-stochastic**:

```
adjacent_pairs:        rowsums = [1 1 1 1 1 1]   lambda1 = 1.000000   |lambda2| = 0.400000
balanced_alternating:  rowsums = [1 1 1 1 1 1]   lambda1 = 1.000000   |lambda2| = 0.200000
```

`iterate_fixed_ray` (`:265-266`) is `c ← A c` with no normalization. For a primitive stochastic `A`,
`Aⁿ → 1πᵀ`, so every strictly positive initial vector converges to a multiple of `perron_ray = 1`
at rate `|λ₂|`. This is the Perron–Frobenius theorem for a fixed 6×6 matrix. It is independent of
the variational free energy, of the gauge structure, of coarse-graining, and of any RG hypothesis.

Around that computation the repository builds: an operator idle-GPU gate with expiry and rechecks, a
five-job three-lane float64 parity sentinel with 240 worker exchanges, a 40-job primary/holdout
split with Holm correction over six frozen secondary endpoints, deterministic bootstrap seeds bound
to a job-table SHA-256, worst-case censoring imputation, an atomic staging/publication protocol, and
a hash-bound source extract. The prior audit measured 3,644 seconds and ~1.009e12 logical bytes of
hashing (AUD-21) for this.

I want to be precise about what is and is not wrong here. The *engineering* is real and the *scope
disclaimers are honest* (`theorem_status: "NUMERICAL"`, `verification_state: "CANDIDATE"`,
`mathematical_verification_state: "INCONCLUSIVE"`, `claim_origin: "APPLICATION_SPECIFIC"`). What is
disproportionate is the ratio: the apparatus is sized for a claim about renormalization-group
attraction, and the computation underneath it is a linear power iteration whose answer is known in
closed form. Combined with N-01 (the seed does not vary) and N-09 (the endpoint is unreachable), the
40 jobs carry approximately one bit of information.

**Fix.** State in the experiment docstring that the frozen maps are row-stochastic and that
convergence follows from Perron–Frobenius, so a reader knows what the run does and does not test.
If the intent is to probe *non-linear* or *recognition-dependent* blocking, the spatial maps must
stop being fixed stochastic matrices.

---

### N-11 — LOW — SILENT FALLBACK — `.get(..., True)` on a scientific decision flag

`fixed_ray_experiment.py:2500-2502`

```python
decision_stability=bool(
    sentinel_identity.get("scientific_decision_parity_passed", True)
),
```
A missing key defaults to "parity passed". The key is in fact always produced at `:2443`, so this is
currently unreachable — but the default is the wrong way round for a fail-closed system.
**Fix:** `sentinel_identity["scientific_decision_parity_passed"]`.

### N-12 — LOW — SILENT FALLBACK — `max_condition` is ignored for scalar blocks

`realizations/gaussian/gauge.py:279`

```python
singular_values = np.geomspace(1.0, max_condition, block_size)
```
For `block_size == 1`, `np.geomspace(1.0, 1e6, 1) == [1.0]`. Probe: three frames generated with
`max_condition=1e6` all have condition exactly `1.0`. A caller requesting ill-conditioned scalar
frames silently gets perfectly conditioned ones. **Fix:** raise, or document, when `block_size == 1`
and `max_condition != 1.0`.

### N-13 — LOW — DEAD MACHINERY — a "premise assessment" that is a constant

`finite/agent_network_experiment.py:324`

```python
**asdict(assess_fixed_channel_premise(recognition_independent=True)),
```
The premise is asserted by literal, never derived from the channel object that is right there. Same
pattern as N-02. The experiment does at least downgrade `verification_state` to `"CANDIDATE"` on the
next line, and it *does* keep an honest negative control (`recognition_independent=False` at `:295`).
**Fix:** derive `recognition_independent` from the constructed `ExactMarkovChannel` /
`interaction_record_kernels`.

### N-14 — LOW — durability — `_atomic_write` does not fsync the containing directory

`artifacts.py:314-330`. The file is `fsync`ed and `os.replace`d, but the parent directory is never
synced, so on a crash the rename may not be durable even though the manifest claims completion.

### N-15 — LOW — PROVENANCE — `matrix_dimension` means two different things

`config.py:122` / `fixed_ray_experiment.py:3162` use it for the 2×2 matrix ray;
`fixed_ray_diagnostics.py:256` emits `"matrix_dimension": 6` (the edge-coordinate dimension) into a
different provenance record. A reader diffing provenance across artifacts sees `2` and `6` for the
same key name.

---

## 3. Test-suite adequacy

### 3.1 Mutation testing — the core math tests have real teeth

I mutated ten functions in a scratch copy and ran the relevant test files. **All ten were caught**:

| Mutation | File:line | Result |
|---|---|---|
| Flip KL direction (`log p − log q`) | `finite/vfe.py:41` | 4 failed / 8 passed |
| `free_energy` sign of `log Z` | `finite/vfe.py:63` | 1 failed / 11 passed |
| Conditional covariance centred on `E[s]` not `E[s\|z]` | `finite/fisher.py:106` | 5 failed / 10 passed |
| `defect_is_psd → True` | `finite/fisher.py:144` | 1 failed / 78 passed |
| Drop max-shift from softmax | `geometry/attention_gauge.py:87` | 1 failed / 35 passed |
| Wrong covector gauge law (`G w` not `G⁻ᵀ w`) | `geometry/attention_gauge.py:163` | 1 failed / 18 passed |
| Quotient sup-norm → plain sup-norm | `finite/interactions.py:180` | 1 failed / 46 passed |
| Drop factor 2 in `2·asin(chord/2)` | `gaussian/fixed_ray.py:210` | 18 failed / 78 passed |
| Drop the `(I − P)` projection from β | `gaussian/fixed_ray.py:287` | 17 failed / 79 passed |
| Schur complement sign flip | `gaussian/interactions.py:322` | 13 failed / 76 passed |

Several are caught by only one test — thin, but not vacuous. This is much better than typical for a
research codebase and should be said plainly.

### 3.2 Where the tests cannot fail

- **N-02:** `premises_passed` / `gpu_gate_complete` are never `False` in any of the 20,705 test
  lines. Deleting both conjuncts from `analyze_primary` changes no test outcome.
- **N-07:** `assert result.defect_is_psd` (`tests/test_fisher.py:153`) asserts a structural identity.
- **N-03:** the repeatability parity assertion would pass under a real determinism failure.
- **AUD-17:** `tests/test_scale_cocycle.py` exercises `base_fisher_cocycle_residual_forms` with a
  literal SPD matrix; the three forms agree for *any* matrix, so the test would pass unchanged if
  the "Fisher defect" were replaced by an arbitrary nonsymmetric indefinite bilinear form.
- Tolerance sweep: `grep -rnE "(abs=|rel=|atol=|rtol=|tol=)\s*(1e-[0-3]|0\.0*[1-9])" tests` returns
  a **single** hit (`tests/test_conditioning.py:46`, an intentional boundary-band test). Tolerances
  in the suite are otherwise `1e-12`/`1e-10` or exact. No evidence of post-hoc tolerance tuning in
  the tests.

### 3.3 Genuinely good negative controls

`tests/test_shared_scientific_contracts.py:204-244` monkeypatches
`retained_projection_invariant → False` and `retained_projection_residual → Fraction(1)` and asserts
the failure *propagates all the way to* `result.status == "fail"`. That is the right shape for a
negative control. `fixed_ray_experiment.py:1890-1925` mutates an endpoint value and a coefficient
and requires the comparator to *reject* — also correct (it tests the comparator, not the science,
and is labelled as such).

---

## 4. Silent fallbacks and swallowed errors — assessment

`grep` for `except Exception` / `except BaseException` returns 16 hits in `src` + `tools` and ~40 in
`Theory/verification`. I reviewed all of the `src` ones. **None of them downgrade a numerical result
to a pass.** The pattern is consistent and correct:

- `finite/experiment.py:374`, `attention_experiment.py:515`, `categorical_dqm_experiment.py:376`,
  `gaussian/experiment.py:458` catch renderer failures and set `figure_status = "failed"` while
  leaving the numerical `status` untouched.
- `rendering.py` is genuinely **fail-closed**: `validated_renderer_status` re-resolves the manifest
  path, re-reads the JSON, re-hashes every published PNG/PDF, and raises on any mismatch. A renderer
  cannot self-report `"complete"`.
- `artifacts.py:327` / `figures.py:1087` are `except BaseException:` cleanup-and-re-raise, correct.
- `runtime.py:110-112, 134-136, 173-174` return `None` when `git` is absent — recorded honestly as
  `git_commit: null`, not as a pass.

There are **no** `warnings.warn` calls in the entire source tree, and no bare `except: pass`. This
is a real strength.

---

## 5. What each experiment claims, and whether it can deliver

| Module | Intended evidence | Can it deliver? |
|---|---|---|
| `finite/experiment.py` | Exact finite VFE chain rule `F_fine − F_coarse = E_q[KL(q(·\|z)‖p(·\|z))]` | **Yes** — verified correct; a real check of the implementation, though the identity itself is a theorem, so it tests the code not the theory. |
| `finite/fisher.py` + `categorical_dqm` | Law of total covariance for a fixed channel; DQM of `√p_θ` for a finite family | **Partly** — the residual check is real; `defect_is_psd` is tautological (N-07); the DQM ladder correctly normalizes by `‖h‖` and would detect a non-DQM family. |
| `finite/interactions.py` | Hoeffding/ANOVA truncation error bounds | **Yes** — reconstruction residual and quotient sup-norm are correct and mutation-sensitive. |
| `finite/scale_cocycle.py` | Fisher cocycle / retained-β residual identities | **No for the "Fisher" part** (AUD-17: the three forms agree for any bilinear form). Yes for the exact-rational transport/projection algebra. |
| `geometry/attention_gauge.py` | Gauge invariance of attention logits under `GL(K)` frames | **Yes but trivially** — invariance is exact by construction (`wᵀG⁻¹ · GLG'⁻¹ · G'u = wᵀLu`); it verifies the implementation, not a physical symmetry. Docstring is honest. |
| `geometry/discrete_holonomy.py` | Graph-link holonomy, trivializability, operational records | **Yes**, and the module explicitly refuses to promote link holonomy to an operational claim (`LinkOnlyHolonomyDiagnostic.supports_operational_claim = False`). Exemplary scoping. |
| `finite/agent_network.py` | Local vs collective VFE difference under fixed outside marginals | **Yes** — exact rational, correct; the "premise" is the one soft spot (N-13). |
| `finite/theory_oracles.py` | Independent exact-rational witnesses for the float lane | **Yes** — a genuinely separate implementation, not a mirror. Real value. |
| `information_history.py` | Fisher rank / natural gradient / recovery along a history | **Compromised** by AUD-15 (two cutoffs) and AUD-16 (scale-dependent floor). |
| `gaussian/fixed_ray*` | Attraction to a fixed matrix ray under repeated blocking (RG-flavoured) | **No** — see N-01, N-09, N-10. The dynamics is a fixed row-stochastic linear map; the endpoint is unreachable by construction; the seed does not vary. It measures `log 0.4` thirty times. |

---

## 6. Is the provenance apparatus proportionate?

Plainly: no.

- `src/multiagent_elbo`: 16,484 lines of science.
- `tests/`: 20,705 lines.
- `Theory/verification/`: **17,857 lines** (`run_checks.py` 10,443, `build_audit.py` 5,473,
  `lifecycle_gate.py` 1,941) guarding a 24-file LaTeX manuscript.

Within `run_checks.py`, roughly 3,600 lines (lines 2115–5694) are the ~30 actual numerical checks;
the remaining ~6,800 are build-record parsing, revision binding, isolated-CWD enforcement, ctypes
Windows file-attribute probing, and JUnit/ledger emission. `build_audit.py` audits a TeX build
without executing TeX. `lifecycle_gate.py` validates a four-class (S/E/C/W) commit taxonomy.

I checked the numerical checks that this apparatus protects and they are correct
(`check_restriction_schur` reconstructs the block-inversion identity and the KKT constrained-mean
cost independently; `gaussian_kl` at `run_checks.py:2405-2422` is the standard formula with the
right argument order). But two of them are genericity arguments dressed as controls:
`check_gauss_projection` asserts `generic_passes == 0` over 4,000 random matrices, and
`check_gauss_trivialization` asserts `raw_asym > 1e-6` for a single random draw — both are true with
probability 1 for reasons that have nothing to do with the claim. To the project's credit, both
`interpretation` strings say so explicitly ("does not prove generic measure zero"; "the manuscript's
historical magnitudes used different omitted matrices").

The honest summary: the verification layer is well engineered and honestly scoped, and it is
protecting a body of numerical evidence whose strongest members are exact-rational identity checks
of theorems, not tests of open conjectures. The apparatus would be equally justified — and much
cheaper — if it protected an experiment that could actually come out either way.

---

## 7. What is genuinely well done

1. **Core mathematics is correct.** I independently re-derived and re-implemented: the KL chain rule
   and its conditional term (`vfe.py:66-121`), the block-update local/collective identity
   (`vfe.py:164-206`), the law of total covariance (`fisher.py:99-114`), the exponential-family
   score `T − E_p[T]` and Fisher `Cov(T)` (`categorical.py:128-144`), the VFE gradient
   `Σ p·s·log(p/t)` (`information_history.py:134`), the Hoeffding conditional-average + Möbius
   inversion (`interactions.py:99-140`), the anchored Möbius decomposition
   (`scale_cocycle.py:493-528`), the quotient sup-norm `(max−min)/2` (`interactions.py:179-183`),
   the DQM remainder `‖√p_{θ+h} − √p_θ − ½h·s√p_θ‖/‖h‖` (`categorical_dqm.py:290-299`), the passive
   inverse congruence `F⁻ᵀΛF⁻¹` and its generalized-eigenvalue invariance (`gauge.py:57-89`), the
   attention gauge transformation laws (`attention_gauge.py:158-178`), the projective angle
   `2·asin(chord/2)` (`fixed_ray.py:202-210`), and the Schur complement (`interactions.py:281-325`).
   **No disagreement with any docstring or theory statement.**
2. **Numerical hygiene in the Gaussian lane.** `cho_factor`/`cho_solve` for the Schur complement,
   `scipy.linalg.solve` for congruences, `eigvalsh` only on explicitly symmetrized matrices,
   `slogdet` for determinant signs, `_logdet` from the Cholesky diagonal, max-shifted softmax in both
   attention modules, `expm1` for the DQM ratio, `errstate` guards followed by explicit finiteness
   raises rather than silent NaN propagation.
3. **Exact-rational lanes.** `scale_cocycle.py`, `theory_oracles.py`, `agent_network.py` and
   `counterexamples.py` use `fractions.Fraction` throughout, with canonical literal parsing
   (`parse_fraction_literal` rejects non-reduced and non-canonical spellings). This removes an entire
   class of tolerance-tuning temptation.
4. **Fail-closed publication.** `rendering.py` re-hashes every published figure and refuses to accept
   a self-reported status. `artifacts.py` rejects symlinks/junctions/reparse points, hard-linked
   artifacts (`st_nlink != 1`), duplicate inodes, non-portable and Windows-reserved filenames, and
   undeclared directory entries at finalize time. `_atomic_write` uses tempfile+fsync+`os.replace`.
5. **Honest scope language in the code itself.** `discrete_holonomy.py:1-9` ("these graph links are
   declared interaction-complex data … not base-connection parallel transports"),
   `FisherChannelResult` ("does not establish differentiability in quadratic mean"),
   `finite_gauge.apply_site_relabeling` ("not an API for arbitrary gauge fields, connections, or
   holonomy"), `LinkOnlyHolonomyDiagnostic.limitation`. Producer records consistently carry
   `verification_state: "CANDIDATE"` and `mathematical_verification_state: "INCONCLUSIVE"`.
6. **A mutation-resistant test suite** (Section 3.1) with monkeypatch-based end-to-end negative
   controls (Section 3.3) and no loose tolerances.
7. **No swallowed scientific errors.** Zero `warnings.warn`, zero bare `except: pass`, and every
   broad `except` in `src` isolates figure rendering from numerical status (Section 4).

---

## 8. Recommended order

1. **N-01** — bind `run.seed` to the fixed-ray job table (or stop publishing RNG provenance for
   experiments that consume no randomness). This is the single change with the largest effect on
   what the published artifacts actually mean.
2. **N-02** — derive `premises_passed` and `gpu_gate_complete`, add `False` regression tests.
3. **N-03** — exact comparison for the CUDA repeatability lane.
4. **AUD-03 / AUD-18** — separate structural normalization policy from comparison tolerance; bound
   `atol`/`rtol`; use a stable KL summation with a documented machine-scale clamp applied only after
   structural validity.
5. **AUD-15 / AUD-16 / N-07** — one eigendecomposition, one cutoff mask, one scale-relative
   criterion; rename the tautological PSD field.
6. **N-04 / N-05 / N-06** — bind the parity condition scale to `spatial_map`; always hash `compute`;
   reject unimplemented compute values.
7. **AUD-06 / AUD-19 / AUD-14** — one shared fixed-ray identity+conditioning validator called from
   all four publication entry points.
8. **N-09 / N-10** — document the Perron–Frobenius structure and the linear-vs-log endpoint error in
   the diagnostic record so the next preregistration does not repeat it.
