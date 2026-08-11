# Fixed-Model Attraction Diagnosis and Results Closeout Design

Date approved: 2026-08-10
Scientific implementation revision: `fcb2c49efdca2ad3ee502dc08fbb82fc285e7a05`
Parent protocol: `2026-08-09-gaussian-fixed-ray-v1a`
Execution state: design only; no new CUDA run or parameter search authorized

## Purpose

The Gaussian fixed-ray confirmatory experiment completed all 30 primary and 10
holdout jobs at the scientific implementation revision above. The frozen primary
analysis returned `inconclusive`: the median projective-angle slope was
`-0.00026786510016806844`, with 95% interval
`[-0.00029802317797700826, -0.00021070275415133334]`. The upper endpoint did not
meet the preregistered practical-support boundary `-0.02`, while none of the
counterevidence rules fired. The descriptive holdout estimate was
`-0.00030310407296303384`, with interval
`[-0.00040771248808456155, -0.00019982541962230285]`, and failed the same practical
threshold without becoming a second confirmatory test.

This design has two goals:

1. close the durable documentation gap by recording the successful CUDA sentinel,
   complete confirmatory execution, and bounded scientific result; and
2. explain the weak observed absolute slopes inside the exact frozen model before
   introducing any new parameter, map, population, endpoint, or threshold.

The diagnostic may close claims about the finite linear maps, their normalized
projective dynamics, and the reproduced 40-job trajectories. It cannot prove
unrestricted Gaussian attraction, attraction on the full matrix coupling cone,
an infinite hierarchy, universality, or a continuum/thermodynamic limit.

## Considered approaches

Three approaches were considered.

1. **Fixed-model analytic diagnosis, then artifact comparison.** Derive the exact
   spectral and projective behavior of the two frozen spatial maps, predict the
   finite-window diagnostics, and compare those predictions with every primary
   and holdout trajectory. This is selected because it can distinguish structural
   scale effects from seed variation without post hoc model changes.
2. **Immediate exploratory parameter sweep.** Vary coupling strength, temperature,
   scale window, or map family to locate regimes with larger negative slopes. This
   is deferred because it would answer a different question and could turn the
   failed practical threshold into a tuning target.
3. **Documentation-only closeout.** Record the completed run and stop. This is
   necessary but insufficient because it leaves the reproducible factor-of-about-75
   mismatch between the observed point estimate and the practical threshold
   unexplained.

## Frozen scientific boundary

The first diagnostic wave holds the following objects fixed:

- the two six-dimensional row-stochastic maps `adjacent_pairs` and
  `balanced_alternating` returned by `build_preregistered_system()`;
- the Perron ray `(1,1,1,1,1,1)`;
- the fixed positive matrix direction `M0` and the scalarized construction
  `W_e = c_e M0`;
- the deterministic `C001`-`C030` and `H001`-`H010` master-seed job literals;
- eight map applications and the recorded scale labels;
- the projective-angle definition, paired least-favorable reduction, bootstrap
  procedure, and all preregistered thresholds; and
- the interpretation of `H` as hash-bound descriptive replication only.

No implementation step may retune a threshold, replace the raw-angle OLS endpoint
with a logarithmic endpoint, select favorable seeds, change a spatial map, alter
the scale window, or use holdout observations to define a new primary statistic.
Any later parameter study requires a separate exploratory design after this wave.

## Mathematical diagnostic

For either frozen spatial map `A`, the coefficient dynamics are exactly

$$
c_{k+1}=A c_k.
$$

Let

$$
u_k=\frac{c_k}{\lVert c_k\rVert_2},
\qquad
\mathcal N_A(u)=\frac{Au}{\lVert Au\rVert_2}.
$$

If `v = N_A(u)`, the derivative acting on a perturbation `h` is

$$
D\mathcal N_A(u)[h]
=\frac{(I-vv^\top)Ah}{\lVert Au\rVert_2}.
$$

This formula separates three effects that the confirmatory endpoint currently
combines: linear mixing by `A`, removal of the radial component by projective
normalization, and conversion of the remaining transverse error into a raw angle.
At the normalized Perron ray, the tangent restriction
`(I-uu^T)A` controls local projective contraction. Because the maps need not be
normal, the analysis reports both eigenvalue moduli and tangent singular values;
it does not infer transient contraction from eigenvalues alone.

The diagnostic computes, for each map:

- exact rational entries, characteristic polynomial, eigenvalues when exactly
  representable, Perron eigenspace, and invariant tangent subspace;
- floating Schur/eigen and singular-value decompositions with residuals;
- the tangent Jacobian at the Perron ray and along each recorded trajectory;
- one-step transverse norm ratios, cumulative tangent propagators, and their
  condition numbers;
- exact and numerical predictions for normalized distance and projective angle;
- OLS slopes on the unchanged raw-angle scale labels used by the confirmatory
  analysis; and
- a decomposition of the gap between relative contraction and the small absolute
  raw-angle slope after the trajectory is already close to the Perron ray.

The preferred explanatory hypotheses are assessed in this order:

1. **Endpoint-scale effect:** relative contraction remains appreciable, but raw
   angles are already so small at scales 4 through 8 that their absolute OLS slope
   is necessarily much smaller than `0.02` radians per scale.
2. **Weak transverse contraction:** the tangent operator has a subdominant mode
   close to one or a large tangent singular value.
3. **Nonnormal transient behavior:** eigenvalues predict asymptotic contraction but
   finite-window singular behavior delays it.
4. **Seed/mode alignment:** the initial literals place little mass in the slowest
   transverse mode or create cancellations that vary across jobs.
5. **Metric/estimator mismatch:** the frozen raw-angle slope is a valid finite
   endpoint but is not a scale-free estimate of the asymptotic contraction factor.

These are diagnostic alternatives, not outcomes assumed in advance.

## Software architecture

The implementation will keep exact theory, numerical reproduction, and reporting
separate.

### Pure diagnostic module

Create `src/multiagent_elbo/realizations/gaussian/fixed_ray_diagnostics.py`.
It will expose pure functions for normalized-map Jacobians, tangent bases,
spectral diagnostics, trajectory-mode decompositions, and frozen-window endpoint
predictions. It will accept arrays explicitly and will not read artifacts, inspect
Git, or select configuration values.

### Artifact-backed diagnostic experiment

Create an artifact publisher adjacent to the existing fixed-ray experiment. It
will consume an explicitly configured final confirmatory run directory, validate
the recorded source/config/job-table/primary/holdout identities, reconstruct the
two frozen maps and all job literals independently, and require equality or frozen
tolerance agreement with the published trajectories and endpoints before issuing
an interpretation.

The diagnostic revision and the earlier scientific implementation revision will
be recorded separately. New diagnostic code must not relabel regenerated data as
if they were executed at `fcb2c49`.

### Click-to-run launcher

Add a small click-to-run Python launcher with editable dictionaries rather than a
CLI. Its default mode performs CPU-only exact/numerical analysis. It has no CUDA
gate, no heavy-sweep option, and no parameter-grid mode. The source confirmatory
run path is explicit and fails closed when absent or mismatched.

### Published diagnostic artifacts

The new run publishes canonical JSON plus compact NPZ arrays:

- `fixed_model_spectral_diagnostics.json`;
- `fixed_model_trajectory_diagnostics.json`;
- `fixed_model_explanation.json`;
- `fixed_model_diagnostic_arrays.npz`;
- `metrics.json`; and
- a manifest containing hashes, both source revisions, the source confirmatory
  manifest hash, and the primary/holdout analysis hashes.

The explanation record uses a finite classification such as
`endpoint_scale_explains_gap`, `weak_transverse_contraction`,
`nonnormal_transient`, `seed_mode_alignment`, `multiple_mechanisms`, or
`inconclusive`. A classification is emitted only from frozen quantitative rules
defined in the implementation plan; prose intuition alone cannot select it.

## Repository results closeout

Revise `docs/results/2026-08-09-gaussian-fixed-ray-results.md` without deleting its
pilot or failed-sentinel history. Add clearly dated sections for:

- the successful revision-bound CUDA sentinel;
- the complete 40-job confirmatory execution;
- the primary estimate, interval, practical threshold comparison, and exact
  `inconclusive` classification;
- the descriptive holdout estimate and its primary-analysis binding;
- secondary Holm results with an explicit warning that the small p-value at the
  `-0.02` primary boundary points in the unfavorable direction;
- zero missing, rejected, censored, basin-exit, and retry counts;
- source, manifest, artifact, JUnit, and ledger hashes; and
- claim typing: implementation/parity/classification integrity may be
  `EVIDENCE_VERIFIED`, the practical-support criterion is not met, and the
  mathematical attraction/universality claims remain `INCONCLUSIVE`/open.

The document title will be broadened from pilot-only wording while retaining the
pilot as the historical first phase.

## Research-wiki ingest

After the repository result record is validated, ingest the result into
`C:\Users\chris and christine\Desktop\Research` under the wiki's schema:

1. create one immutable `sources/runs/` note containing the frozen configuration,
   source/artifact hashes, primary and holdout estimates, classification, and
   exact scope limitations;
2. update `wiki/projects/Gauge-Theoretic Multi-Agent VFE Model.md` with the completed
   finite instantiation and the next fixed-model diagnostic obligation;
3. update `wiki/concepts/Renormalization-group flow of beliefs.md` to distinguish
   the new finite numerical result from an RG fixed-point or universality result;
4. update `index.md` for the new source note and append the required `INGEST` entry
   to `log.md`; and
5. run the vault link/identity lint and preserve any unrelated Research WIP.

The wiki ingest occurs only after the repository result text and hashes are final,
so the immutable run note does not need correction afterward.

## Validation strategy

Validation is layered by claim type.

### Exact and mathematical checks

- Reconstruct both maps as exact rational matrices and verify row stochasticity,
  Perron-ray membership, characteristic polynomials, and any claimed invariant
  subspaces.
- Derive the normalized-map Jacobian independently and compare it with centered
  finite differences over multiple positive directions and tangent vectors.
- Require analytic/numerical agreement before assigning any mechanism label.

### Numerical and artifact checks

- Recompute all 40 CPU trajectories from the immutable job table and compare them
  with the final confirmatory bundle.
- Recompute all primary and holdout diagnostic inputs without changing the frozen
  classifier.
- Verify every output is finite, deterministic, hash-bound, and identical across
  two clean output roots.
- Include negative controls for a perturbed map, incorrect normalization, omitted
  tangent projection, and shuffled job identity.

### Regression and review gates

- Add focused tests for exact spectra, Jacobian finite differences, nonnormal-map
  handling, mode decomposition, artifact rejection, and deterministic publication.
- Run the complete CPU suite with machine-readable JUnit evidence. No CUDA claim is
  created by this CPU-only wave.
- Obtain independent mathematics, numerical-analysis, experiment, and code review
  of the exact clean revision.
- Record one claim per check in the revision-bound verification ledger and validate
  it before publication.

## Failure behavior

The diagnostic fails closed when the source artifact is missing, its hashes or
revision bindings drift, a map is not the frozen map, regenerated trajectories do
not match, exact and floating spectral calculations disagree beyond their declared
tolerances, a Jacobian finite-difference control fails, or an explanation rule is
not uniquely satisfied. Such a run may publish an immutable failure record but may
not publish a positive mechanism classification.

If no frozen mechanism quantitatively explains the observed finite-window slopes,
the correct result is `inconclusive` with a named mathematical or numerical
obligation. The implementation must not respond by changing parameters within the
same wave.

## Definition of done

This wave is complete only when:

- the repository result document accurately records the successful sentinel and
  complete confirmatory result;
- the Research wiki contains a lint-clean immutable run record and calibrated
  synthesis updates;
- exact and numerical fixed-model diagnostics reproduce the frozen trajectories
  and quantify the observed primary and holdout slopes;
- the selected explanation, or the residual inconclusive obligation, follows from
  frozen machine-readable rules;
- full regression and independent review gates pass at one exact clean revision;
  and
- the branch is committed, pushed, merged, and fast-forwarded without modifying
  unrelated Desktop or Research-vault WIP.
