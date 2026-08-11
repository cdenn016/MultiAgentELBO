# Fixed-Model Attraction Diagnosis Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task by task.

**Goal:** Durably close the completed Gaussian confirmatory result, prove that its
preregistered practical-support boundary was unreachable inside the frozen
coefficient basin, and publish deterministic continuous diagnostics of the
unchanged maps and trajectories.

**Architecture:** A pure module owns canonical Fraction maps, the analytic basin
certificate, normalized-map derivatives, reduced tangent operators, spectral
diagnostics, and trajectory summaries. A separate experiment validates a tracked
scientific extract of the `fcb2c49` bundle, deterministically replays all 80 CPU
trajectories, and publishes hash-bound diagnostic artifacts. Repository evidence
is finalized and verified before a separate Research-wiki ingest.

**Tech stack:** Python 3.14 CPU, `fractions.Fraction`, NumPy, SciPy, pytest/JUnit,
the existing `RunStore` and verification ledger, PowerShell, and Obsidian
Markdown. No new dependency is permitted.

## Global constraints

- Scientific implementation revision:
  `fcb2c49efdca2ad3ee502dc08fbb82fc285e7a05`.
- Keep both maps, `M0`, the Perron ray, 40 job literals, basin, eight steps,
  endpoint window, paired reduction, bootstrap, and thresholds unchanged.
- Run no CUDA job, GPU gate, parameter grid, or heavy sweep.
- Never pool `C` and `H`. Only `C001`-`C030` determine the primary result;
  `H001`-`H010` are a separate descriptive replication.
- Do not retune `-0.02`, select seeds, replace raw-angle OLS by log-angle OLS, or
  promote a finite result to unrestricted attraction or universality.
- Every producer record remains `CANDIDATE`. Only a validated external ledger
  may use `EVIDENCE_VERIFIED` or `REFUTED`.
- Exact claims apply to canonical rational map literals after an explicit
  runtime-float conformance check. Trajectories and angles are numerical.
- Report norms and condition numbers only for reduced tangent operators, never
  the singular ambient normalized-map Jacobian.
- Use click-to-run editable dictionaries, not a CLI.
- Preserve Desktop and Research WIP. Use isolated worktrees, audit overlap, and
  never switch or advance the dirty Research review branch.
- Use `apply_patch` for tracked text/code edits. Do not commit full execution
  logs, generated run directories, JUnit XML, or `.verification/ledger.json`.

## Immutable source inventory

Recovery source:

`C:\Users\chris and christine\Documents\ChatGPT\MultiAgentELBO\.superpowers\worktrees\MultiAgentELBO-shared-scientific-contracts-20260810`

Coordinator evidence SHA-256:
`7fb07f04d709a3d07613fa220529875c7ddd63601940f3bbb2b87d2440b055fa`.

Original confirmatory run:
`artifacts/gaussian-fixed-ray-confirmatory/c6eb894ba5e08bcf64136e0dea5b4692c0e2e1e6c6a289d7d47e50e78739d748-20260809`.

| File | SHA-256 | Bytes | Track in compact extract |
|---|---|---:|---|
| `config.json` | `66e474db7e46ae0589ca5198712c59aa9f28317d219381ddf96b989e5d40d191` | 792 | yes |
| `confirmatory_arrays.npz` | `7040967043619fd52a0386ff0b9623febdd4c97f0c2356f8abb98fd786dc2b6a` | 71,942 | yes |
| `confirmatory_endpoints.json` | `7d6b36b5bde80969d8974d5550c0ed8c125896ee03be7ffd196d3915f8261556` | 214,173 | yes |
| `confirmatory_execution.json` | `04661576c3a4132fca52739a95038a221976abdd2fcd02ea5bbe0d9d3a8fe518` | 9,334,757 | no; hash only |
| `confirmatory_job_table.json` | `a50dd3893ce1ad9c081a8e2f2cbc5adc676e2b217c9c3ec321e8b0d62b453adf` | 9,062 | yes |
| `holdout_analysis.json` | `ff09a656d7638a233d21149132367b95072fae6030187ee997290aa1a0596d1d` | 8,152 | yes |
| `manifest.json` | `7e0a050850b48b446c70bff3a67010c84d2daa1fada6c48742d3ab152d43a1fb` | 2,522 | yes |
| `metrics.json` | `cd45e55dd39236b556dc200a04ad081affcb19a6c52fb584ad63f3f1992f7f59` | 394 | yes |
| `primary_analysis.json` | `f8b58ae7f8777e18800c37d63b55d37c0052cd47b407a40497405ef5f6375155` | 17,093 | yes |
| `primary_execution.json` | `e1a952259227f754bafacf3e0a983cea28996325adee96d1579ae1944024f816` | 7,170,105 | no; hash only |

Stop if the coordinator evidence or any owned source file differs. The compact
extract preserves the eight replay-relevant files byte for byte and records all
ten hashes, so a fresh clone can reproduce the scientific diagnosis without the
two large worker-control logs.

## Planned repository files

- Create `docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/`
  with the eight-file compact extract plus `source_binding.json` and
  `current_result.json`.
- Create `docs/verification/reviews/2026-08-10-fixed-model-attraction-derivation.md`.
- Create `src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostics.py`.
- Create
  `src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostic_experiment.py`.
- Create `run_gaussian_fixed_ray_diagnostic.py`.
- Create `tests/test_gaussian_results_document.py`.
- Create `tests/test_gaussian_fixed_ray_diagnostics.py`.
- Create `tests/test_gaussian_fixed_ray_diagnostic_experiment.py`.
- Modify `tests/test_launchers.py` only for import safety; use dedicated launcher
  tests for source-required execution.
- Modify `src/multiagent_elbo/realizations/gaussian/__init__.py`.
- Modify `docs/results/2026-08-09-gaussian-fixed-ray-results.md`.
- Create a tracked final diagnostic extract under
  `docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic/`.

---

### Task 0: Publish the amended governing documents

**Files:**
- Modify: `docs/superpowers/specs/2026-08-10-fixed-model-attraction-diagnosis-design.md`
- Create: `docs/superpowers/plans/2026-08-10-fixed-model-attraction-diagnosis.md`

- [x] **Step 1: Commit the adversarially amended design and this plan**

The planning coordinator stages exactly these two governing documents and commits
them as the planning handoff. This completed checkbox is carried by that commit;
no implementation task begins from the earlier design-only revision.

- [x] **Step 2: Require a clean implementation starting point**

Immediately after the planning commit, require `git status --porcelain` to be
empty. Generated worktree-local dependency locks are removed only after proving
they are not the user's protected live-checkout files.

---

### Task 1: Track the final scientific extract and close the stale result record

**Files:**
- Create: `docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/*`
- Create: `tests/test_gaussian_results_document.py`
- Modify: `docs/results/2026-08-09-gaussian-fixed-ray-results.md`

**Interfaces:** The tracked `source_binding.json` is the durable source of all ten
original hashes. `current_result.json` is the single machine-readable current
state; prose may retain clearly labeled history.

- [ ] **Step 1: Verify recovery evidence before copying anything**

Recompute the coordinator-evidence hash, all ten file hashes, and sizes at the
absolute recovery path. Stop on any difference. Copy only the eight files marked
`yes` into the tracked evidence directory, preserving their original names and
bytes. Create `source_binding.json` with:

```json
{
  "schema_version": "gaussian-confirmatory-source-binding-v1",
  "scientific_revision": "fcb2c49efdca2ad3ee502dc08fbb82fc285e7a05",
  "coordinator_evidence_sha256": "7fb07f04d709a3d07613fa220529875c7ddd63601940f3bbb2b87d2440b055fa",
  "complete_original_inventory": {"...": {"sha256": "...", "size_bytes": 0}},
  "tracked_scientific_subset": ["config.json", "confirmatory_arrays.npz", "confirmatory_endpoints.json", "confirmatory_job_table.json", "holdout_analysis.json", "manifest.json", "metrics.json", "primary_analysis.json"]
}
```

- [ ] **Step 2: Write a failing current-state document contract**

The test parses `current_result.json`, verifies its values against the copied
primary/holdout JSON, and requires the result document to link the binding file.
It must assert:

```python
assert current["completed_jobs"] == 40
assert current["missing_jobs"] == 0
assert current["rejected_jobs"] == 0
assert current["retried_jobs"] == 0
assert current["primary"]["classification"] == "inconclusive"
assert current["primary"]["estimate"] == -0.00026786510016806844
assert current["primary"]["interval"][1] == -0.00021070275415133334
assert current["holdout"]["scope"] == "descriptive_replication_only"
assert current["producer_verification_state"] == "CANDIDATE"
```

The test scopes historical wording checks to a delimited `Current state` section;
it must not reject dated pilot history or pass contradictory current prose by
substring coincidence.

- [ ] **Step 3: Run RED**

Run: `python -m pytest tests/test_gaussian_results_document.py -q`

Expected: fail because the machine-readable current record and current section do
not yet exist.

- [ ] **Step 4: Write the current record and update prose**

Retain pilot and failed-sentinel sections as history. Add the successful sentinel,
40-job completion, primary and descriptive holdout results, zero terminal failure
counts, hashes, and scope. Separate the primary boundary result
`p <= 2/10001` (bootstrap resolution floor, unfavorable direction) from the six
Holm-adjusted secondary tests. Mark historical ledger states as revision-bound;
all original producer records remain `CANDIDATE`.

- [ ] **Step 5: Run GREEN and commit**

```powershell
python -m pytest tests/test_gaussian_results_document.py -q
git diff --check
git add docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49 docs/results/2026-08-09-gaussian-fixed-ray-results.md tests/test_gaussian_results_document.py
git commit -m "docs: close Gaussian confirmatory evidence"
```

---

### Task 2: Implement exact map identities and the basin feasibility certificate

**Files:**
- Create: `src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostics.py`
- Create: `tests/test_gaussian_fixed_ray_diagnostics.py`
- Create: `docs/verification/reviews/2026-08-10-fixed-model-attraction-derivation.md`
- Modify: `src/multiagent_elbo/realizations/gaussian/__init__.py`

**Interfaces:**

```python
canonical_fraction_maps() -> Mapping[str, tuple[tuple[Fraction, ...], ...]]
fraction_characteristic_polynomial(matrix) -> tuple[Fraction, ...]
runtime_map_conformance(runtime_maps, exact_maps, *, atol) -> Mapping[str, float]
adjacent_support_certificate(*, basin_lower, basin_upper, threshold) -> Mapping[str, object]
```

- [ ] **Step 1: Write failing exact polynomial tests**

Pin the correct source-derived values:

```python
assert fraction_characteristic_polynomial(exact["adjacent_pairs"]) == (
    Fraction(1), Fraction(-3), Fraction(18, 5), Fraction(-56, 25),
    Fraction(96, 125), Fraction(-432, 3125), Fraction(32, 3125),
)
assert fraction_characteristic_polynomial(exact["balanced_alternating"]) == (
    Fraction(1), Fraction(-9, 5), Fraction(27, 25),
    Fraction(-333, 1000), Fraction(73, 1250),
    Fraction(-141, 25000), Fraction(3, 12500),
)
```

Assert adjacent factorization `(lambda-1)(lambda-2/5)^5` and fivefold
multiplicity. Reject Boolean, non-square, nonfinite, or noncanonical inputs.

- [ ] **Step 2: Write failing certificate tests**

Pin the derivation outputs:

```python
cert = adjacent_support_certificate(
    basin_lower=Fraction(1, 4), basin_upper=Fraction(4),
    threshold=Fraction(-1, 50),
)
assert cert["coefficient_of_variation_bound"] == Fraction(15, 8)
assert cert["tan_theta4_bound"] == Fraction(6, 125)
assert cert["ols_weights"] == tuple(Fraction(x, 10) for x in (-2, -1, 0, 1, 2))
assert cert["slope_lower_bound"] == pytest.approx(
    -0.3 * math.atan(6 / 125), abs=1e-15
)
assert cert["rational_slope_lower_bound"] == Fraction(-9, 625)
assert cert["rational_margin_above_threshold"] == Fraction(7, 1250)
assert cert["slope_lower_bound"] > -0.02
assert cert["paired_support_boundary_reachable"] is False
```

Add a falsification control using a synthetic wider basin or larger transverse
factor for which the sufficient bound no longer excludes `-0.02`; the function
must return `not_certified`, not a false proof.

- [ ] **Step 3: Run RED**

Run: `python -m pytest tests/test_gaussian_fixed_ray_diagnostics.py -k "characteristic or certificate" -q`

- [ ] **Step 4: Implement exact arithmetic and derivation**

Use canonical Fraction literals and Faddeev-LeVerrier or fraction-safe determinant
recurrence. Runtime conformance checks compare float encodings to those literals;
they do not manufacture exact trajectory claims by snapping arbitrary floats.

Write the tracked derivation with:

1. `A_adj = 2/5 I + 1/10 11^T` and its spectrum;
2. the Bhatia-Davis coefficient-of-variation bound;
3. `tan(theta_k)=(2/5)^k tan(theta_0)`;
4. the five-point OLS weights and monotonic-angle inequality;
5. the paired maximum implication; and
6. the explicit boundary between endpoint-feasibility and attraction claims.

- [ ] **Step 5: Obtain independent symbolic and hand checks**

Use locally installed SymPy only as a developer oracle and a separate hand/Fraction
script that does not import the production diagnostic module. Save both outputs
under `.verification/`; cite the tracked derivation as mathematics evidence.

- [ ] **Step 6: Run GREEN and commit**

```powershell
python -m pytest tests/test_gaussian_fixed_ray_diagnostics.py -k "characteristic or certificate" -q
git diff --check
git add src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostics.py src/multiagent_elbo/realizations/gaussian/__init__.py tests/test_gaussian_fixed_ray_diagnostics.py docs/verification/reviews/2026-08-10-fixed-model-attraction-derivation.md
git commit -m "feat: certify fixed-ray support boundary"
```

---

### Task 3: Implement reduced tangent and continuous trajectory diagnostics

**Files:**
- Modify: `fixed_ray_diagnostics.py`
- Modify: `tests/test_gaussian_fixed_ray_diagnostics.py`

**Interfaces:**

```python
normalized_projective_map(A, u) -> NDArray[np.float64]
normalized_projective_jacobian(A, u) -> NDArray[np.float64]
orthonormal_tangent_basis(u) -> NDArray[np.float64]
reduced_tangent_step(A, u, next_u) -> NDArray[np.float64]
spectral_diagnostics(A, perron_ray) -> Mapping[str, object]
diagnose_trajectory(A, coefficients, perron_ray, scale_labels) -> Mapping[str, object]
summarize_population(records, *, population) -> Mapping[str, object]
```

- [ ] **Step 1: Write failing derivative and tangent tests**

Accept every finite nonzero projective representative and reject zero/nonfinite
inputs. Compare the analytic derivative on tangent directions with a sphere
geodesic finite-difference ladder near `eps_machine**(1/3)`; require convergent,
scale-aware residuals rather than a single noise-floor step.

Assert `J @ u == 0` and do not compute `cond(J)`. For tangent bases `B_k`, assert
orthonormality, tangency, and the reduced formula
`K_k = B_{k+1}.T @ J_k @ B_k`.

- [ ] **Step 2: Write failing spectral tests**

For adjacent, pin tangent spectrum `{2/5 x 5}`, singular values `{2/5 x 5}`, and
spectral-excess ratio exactly one. For alternating, compare eigenvalues by
multiplicity against exact factors, use scale-normalized Schur residuals, and
compare invariant-subspace projectors rather than eigenvector order or phase.

Freeze the Perron reduced tangent `T_* = B_*^T P_* A B_*`. The alternating slow
cluster is exactly `lambda=1/5` plus `(3 +/- i sqrt(7))/20`, so
`rho(T_*)=1/5` and its ordered real-Schur cluster has dimension three. Let `Q_s`
be that orthonormal Schur basis and compare the ambient projector
`B_* Q_s Q_s^T B_*^T`, which is invariant to the choice of orthonormal `B_*`.

Report for horizons 1 through 8:

```text
absolute_gain[m] = ||T^m||_2
spectral_excess[m] = ||T^m||_2 / rho(T)^m
```

Emit `transient_amplification=false` unless an absolute gain exceeds one. The
adjacent slow subspace is the full tangent and its seed-alignment field is
`not_applicable_degenerate_spectrum`.

- [ ] **Step 3: Write failing trajectory tests**

Use production `projective_ray_angle` and the frozen OLS routine, promoted to a
shared public helper if necessary. Require exact same-path endpoint equality;
use `np.polyfit` only as an independent loose cross-check. Recurrence tolerance is
`8 * eps_float64 * max(1, max_abs_coefficient)` unless the same code path yields
bit identity.

For every record report scales 4 through 8, raw and log angles, one-step ratios,
reduced propagator norms/condition numbers, actual-direction gains, and continuous
mode-projector energy. Do not emit a heuristic mechanism label.

For seed `c_0`, freeze
`delta_0=P_*(c_0/||c_0||_2)`,
`actual_gain_m=||T_*^m B_*^T delta_0||_2/||B_*^T delta_0||_2`, and
`slow_energy=||Pi_s delta_0||_2^2/||delta_0||_2^2`. A zero transverse deviation is
not applicable. Pin the independent-oracle `C001` alternating values
`slow_energy=0.24294168484640577`, `actual_gain_1=0.19447462201557028`, and
`actual_gain_8=3.422752480391632e-06` with `abs=1e-12`, and require invariance
under an independently rotated tangent basis.

- [ ] **Step 4: Freeze population separation tests**

`summarize_population(..., population="C")` uses 30 master-seed jobs and the same
per-job least-favorable map reduction as the frozen primary. `population="H"`
uses 10 jobs and is always `descriptive_replication_only`. A mutation to any H
record must not change any C summary byte. Reject pooled `C+H` input.

- [ ] **Step 5: Implement, run, and commit**

```powershell
python -m pytest tests/test_gaussian_fixed_ray_diagnostics.py -q
git add src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostics.py src/multiagent_elbo/realizations/gaussian/fixed_ray.py src/multiagent_elbo/realizations/gaussian/confirmatory_analysis.py tests/test_gaussian_fixed_ray_diagnostics.py
git commit -m "feat: add reduced fixed-ray diagnostics"
```

Only stage `fixed_ray.py` or `confirmatory_analysis.py` if a pure endpoint helper
must be promoted without changing behavior; otherwise omit them.

---

### Task 4: Validate the tracked evidence and deterministically replay 80 trajectories

**Files:**
- Create: `fixed_ray_diagnostic_experiment.py`
- Create: `tests/test_gaussian_fixed_ray_diagnostic_experiment.py`
- Modify: Gaussian `__init__.py`

**Interfaces:**

```python
ConfirmatorySourceBinding
validate_scientific_extract(path, binding) -> ValidatedConfirmatorySource
replay_confirmatory_diagnostics(source, *, iterate_fn=iterate_fixed_ray) -> ReplayResult
```

- [ ] **Step 1: Write synthetic fail-closed unit tests**

Use a fixture factory committed as test code, not copied live artifacts. Mutate
every owned hash, source revision, job order, duplicate ID, scheme inventory,
trajectory shape, NPZ object dtype, endpoint, and primary/holdout binding. Each
mutation must fail before output-directory creation.

- [ ] **Step 2: Write the tracked-extract integration test**

Require all eight owned hashes, all ten inventory entries, 40 ordered unique job
IDs, 30 C plus 10 H, two schemes, and nine states per trajectory. Preserve the
recorded 640-exchange/zero-retry facts as source metadata but do not pretend to
revalidate omitted execution logs.

- [ ] **Step 3: Write replay tests**

Regenerate every initial literal from master seed and job ID, then call the frozen
`iterate_fixed_ray` for each job/scheme. Require 80 injected calls and equality or
the explicitly frozen CPU-replay tolerance against the tracked arrays/endpoints.
A loader that simply returns stored outputs must fail the call-count control.

- [ ] **Step 4: Implement validation and replay**

Load NPZ with `allow_pickle=False`, return immutable defensive copies, bind the
historical scientific revision separately from the live diagnostic revision, and
name this operation deterministic replay. The independent derivation/oracle from
Tasks 2 and 6 supplies independent evidence.

- [ ] **Step 5: Run and commit**

```powershell
python -m pytest tests/test_gaussian_fixed_ray_diagnostic_experiment.py -q
python -m pytest tests/test_gaussian_fixed_ray_diagnostics.py -q
git add src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostic_experiment.py src/multiagent_elbo/realizations/gaussian/__init__.py tests/test_gaussian_fixed_ray_diagnostic_experiment.py
git commit -m "feat: replay fixed-ray scientific extract"
```

---

### Task 5: Publish deterministic diagnostics and add the click-to-run launcher

**Files:**
- Modify: `fixed_ray_diagnostic_experiment.py`
- Create: `run_gaussian_fixed_ray_diagnostic.py`
- Modify: diagnostic experiment tests
- Modify: `tests/test_launchers.py`

**Interfaces:**

```python
run_fixed_model_diagnostic(
    config: ExperimentConfig,
    source_binding: ConfirmatorySourceBinding,
    source_dir: Path,
) -> GaussianFixedRayDiagnosticResult
```

- [ ] **Step 1: Write failing publication tests**

Require these artifacts:

```python
{
    "config.json", "manifest.json", "fixed_model_support_certificate.json",
    "fixed_model_spectral_diagnostics.json",
    "fixed_model_trajectory_diagnostics.json",
    "fixed_model_explanation.json", "fixed_model_diagnostic_arrays.npz",
    "metrics.json",
}
```

The manifest must contain `artifact_kind="fixed_model_attraction_diagnostic"`,
diagnostic revision and dirty-tree flag, scientific revision, canonical source
binding digest, source hashes, config/theory hashes, and recomputed SHA-256 for
every non-manifest artifact. `source_binding` must affect the content-addressed
run name so two different sources cannot collide under one config.

- [ ] **Step 2: Freeze producer statuses**

Every emitted metric, including source validation and replay, has
`verification_state=CANDIDATE`. The support certificate uses
`theorem_status=ESTABLISHED`, `claim_origin=APPLICATION_SPECIFIC`, and producer
mathematical state `CANDIDATE`. Continuous trajectory results use
`theorem_status=NUMERICAL`; unrestricted attraction/universality remain
`INCONCLUSIVE`/`OPEN` in the explanation.

- [ ] **Step 3: Implement deterministic publication**

Validate all inputs and require a clean tracked source tree before creating the
run. Canonicalize JSON, prohibit object arrays, include per-array canonical hashes,
and finalize only after recomputing artifact hashes. Across two output roots,
compare semantic JSON and per-array hashes; do not require NPZ ZIP-container byte
identity.

- [ ] **Step 4: Write launcher tests**

Expose `RUN`, `THEORY`, `NUMERICS`, `OUTPUT`, `COMPUTE`, and `SOURCE`. Test:

1. import safety with no filesystem writes;
2. `main()` success with both source and output overridden to temporary fixtures;
3. explicit fail-closed behavior and zero writes when default source is absent;
4. CPU backend and `heavy_sweep_enabled=False`.

Do not add this source-required launcher to a generic clean-CWD success matrix.
Resolve the default source relative to repository root; preserve the ordinary
editable output-root semantics used by existing launchers.

- [ ] **Step 5: Implement, run, and commit**

```powershell
python -m pytest tests/test_gaussian_fixed_ray_diagnostics.py tests/test_gaussian_fixed_ray_diagnostic_experiment.py tests/test_launchers.py -q
git add src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostic_experiment.py run_gaussian_fixed_ray_diagnostic.py tests/test_gaussian_fixed_ray_diagnostic_experiment.py tests/test_launchers.py
git commit -m "feat: publish fixed-model attraction diagnosis"
```

---

### Task 6: Execute, adjudicate, and commit the final diagnostic record

**Files:**
- Create ignored: two diagnostic run roots, oracle output, focused JUnit, ledger
- Create tracked: `docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic/*`
- Modify: result document, current-result JSON, and document contract test

- [ ] **Step 1: Execute twice from clean output roots**

Run the same clean revision and source binding from the worktree root and a
sanitized CWD with explicit output overrides. Require identical semantic JSON and
per-array hashes. Stop on any dirty-tree marker, source drift, or differing
diagnostic value.

- [ ] **Step 2: Run the independent oracle**

Use a one-off script that imports NumPy/SciPy and frozen production code but not
`fixed_ray_diagnostics.py`. Recompute exact polynomials, the basin certificate,
finite-difference ladder, reduced tangent spectra, C/H slopes, and all published
continuous summaries. Save its output under `.verification/`.

- [ ] **Step 3: Obtain four exact-revision reviews**

Use independent code, mathematics, numerical-analysis, and experiment reviewers.
Designate one final verifier-adjudicator. Run Claude Opus 5 read-only when
available:

```powershell
claude -p --model opus --effort max --permission-mode plan --tools "Read,Glob,Grep" --no-session-persistence "Adversarially review the exact fixed-model attraction diagnostic revision against its design and plan. Check the basin certificate, reduced tangent operators, C/H separation, source binding, artifact hashes, status discipline, and claim boundaries. Return file:line findings; do not edit or run CUDA."
```

LLM agreement is review input, never closure evidence.

- [ ] **Step 4: Create the tracked diagnostic extract**

Copy the canonical certificate, spectral diagnostics, C and H trajectory
summaries, explanation, per-array hash inventory, config, and manifest into the
tracked diagnostic evidence directory. Exclude transient process/control data.
Add a source-to-output binding JSON with every original and diagnostic hash.

- [ ] **Step 5: Update the authoritative result record**

Record the exact diagnostic revision, correct spectra, analytic lower bound,
paired-threshold implication, continuous C diagnostics, separate H replication,
negative controls, and artifact hashes. State:

- endpoint-feasibility theorem: `ESTABLISHED`, producer `CANDIDATE`;
- frozen practical-support criterion: structurally unreachable in this basin;
- confirmatory classification: unchanged `inconclusive`;
- mathematical attraction: `INCONCLUSIVE`;
- unrestricted universality: `OPEN`/`INCONCLUSIVE`.

- [ ] **Step 6: Run focused tests and commit all final tracked bytes**

```powershell
python -m pytest tests/test_gaussian_results_document.py tests/test_gaussian_fixed_ray_diagnostics.py tests/test_gaussian_fixed_ray_diagnostic_experiment.py tests/test_launchers.py -q --junitxml=.verification/fixed-model-attraction-focused.xml
git diff --check
git add docs/results/2026-08-09-gaussian-fixed-ray-results.md docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/current_result.json tests/test_gaussian_results_document.py
git commit -m "docs: certify fixed-ray endpoint feasibility"
```

Any source change after this commit invalidates the diagnostic artifacts and
requires replay.

---

### Task 7: Verify and publish MultiAgentELBO at the exact final revision

- [ ] **Step 1: Run the full CPU suite with JUnit**

```powershell
python -m pytest -q --junitxml=.verification/fixed-model-attraction-full.xml
```

Parse counts from JUnit. Require zero failures/errors. This wave creates no new
CUDA claim.

- [ ] **Step 2: Obtain final exact-revision adjudication**

After the Task-6 documentation/evidence commit, rerun the designated
verifier-adjudicator on the exact clean `HEAD`. The adjudicator must explicitly
review the tracked derivation, final diagnostic extract, result record, JUnit
evidence, and all earlier reviewer findings. Any substantive source correction
requires diagnostic replay and a new final commit; a stale pre-documentation
review cannot close the final revision.

- [ ] **Step 3: Populate and validate the exact-HEAD ledger**

Record separate claims for:

1. exact map polynomials — mathematics `EVIDENCE_VERIFIED` using the tracked
   derivation plus independent exact oracle;
2. the basin support certificate — mathematics `EVIDENCE_VERIFIED`;
3. tracked-source validation and 80-trajectory replay — code/experiment
   `EVIDENCE_VERIFIED`;
4. deterministic publication — `EVIDENCE_VERIFIED`;
5. frozen analyzer's `inconclusive` classification — `EVIDENCE_VERIFIED`;
6. finite practical support under the frozen rule — `REFUTED` and superseded by
   the stronger structural certificate;
7. fixed-B mathematical attraction — `INCONCLUSIVE`; and
8. unrestricted attraction/universality — `INCONCLUSIVE`/`OPEN`.

Run:

```powershell
python "C:\Users\chris and christine\.claude\skills\verification\scripts\verification_gate.py" validate --cwd . .verification/ledger.json
```

Require ledger revision exactly equal to clean `HEAD`, one structured
verifier-adjudicator, current JUnit hashes, and no untracked files:
`git status --porcelain` must be empty.

- [ ] **Step 4: Fetch authoritative remote and integrate in isolation**

Fetch, inspect `git log origin/main`, and compute
`git rev-list --left-right --count HEAD...origin/main`. Push the feature branch.
Fast-forward `origin/main` only from an isolated clean integration worktree and
verify `git ls-remote` at the exact merge SHA.

- [ ] **Step 5: Safely fast-forward the dirty Desktop main checkout**

Before advancing it, record path/type/SHA-256 for every modified and untracked WIP
file, prove no incoming-path overlap, and rehearse when needed. Fast-forward only
because the live checkout is on `main`; never stash, reset, or delete WIP. Recompute
the WIP manifest afterward and require byte identity.

---

### Task 8: Ingest the validated result into the Research wiki

**Files in an isolated Research worktree:**
- Create: `sources/runs/2026-08-10-multiagentelbo-gaussian-fixed-ray-confirmatory.md`
- Modify: `wiki/projects/Gauge-Theoretic Multi-Agent VFE Model.md`
- Modify: `wiki/concepts/Renormalization-group flow of beliefs.md`
- Modify: `index.md`
- Modify: `log.md`

- [ ] **Step 1: Create a clean Research main worktree**

Fetch and inspect authoritative `origin/main`. Inventory the dirty live Research
checkout and confirm it is on `review/gauge-vfe-rg-deep-2026-08-02`. Do not switch,
advance, or edit that checkout. Create a fresh
`codex/multiagentelbo-fixed-ray-ingest-20260810` worktree from `origin/main`.

- [ ] **Step 2: Write the immutable run note**

Include the source and diagnostic revisions/hashes, 40-job protocol, primary and
holdout estimates, analytic feasibility theorem, continuous diagnostics, negative
controls, exact claim states, and a `Relevance to this research` section. Omit
resident PIDs, absolute user paths, raw process telemetry, and private sidecars.

- [ ] **Step 3: Update project and RG synthesis**

State that the frozen finite endpoint could not meet its support threshold
anywhere in the admitted basin. Distinguish that endpoint-design fact from
projective attraction, an RG fixed point, beta function, semigroup, universality,
or the legacy runtime.

- [ ] **Step 4: Update navigation, log, and lint**

Add the source note to `index.md`, append one `INGEST` line to `log.md`, and run
`python docs/_lint.py`. Require zero broken links, grey nodes, empty files,
basename collisions, and identity collisions.

- [ ] **Step 5: Commit and publish Research in isolation**

Commit exactly the five planned paths, push the feature branch, fast-forward
Research `origin/main` in an isolated integration worktree, and verify the remote
SHA. Leave the dirty live Research review branch untouched; report that it was not
fast-forwarded.

## Final evidence contract

Report exact MultiAgentELBO and Research commits, remote parity, JUnit totals,
source/diagnostic hashes, ledger states, wiki lint totals, and preserved WIP paths.
The bounded scientific conclusion is:

> Under the frozen coefficient basin and paired raw-angle endpoint, the
> preregistered `-0.02` practical-support boundary was analytically unreachable.
> The completed finite experiment remains `inconclusive` about mathematical
> attraction, and unrestricted universality remains open.

## Plan self-review

- No task changes a scientific parameter, threshold, population, or endpoint.
- The correct adjacent polynomial and fivefold transverse multiplicity are pinned.
- The basin certificate is independent of the observed job sample.
- C and H are never pooled.
- Full Jacobian conditioning and arbitrary degenerate eigenvectors are excluded.
- Nonnormal absolute gain and spectral excess are distinct.
- All producer states remain `CANDIDATE`.
- Unit tests use synthetic fixtures; the real integration test uses a tracked
  scientific extract available to fresh clones.
- The ledger is created only after the final tracked commit and before wiki ingest.
- The dirty Research non-main checkout is never advanced.
