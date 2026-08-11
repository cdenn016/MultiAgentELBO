# Fixed-Model Attraction Diagnosis and Results Closeout Design

Date approved: 2026-08-10

Adversarial amendment: 2026-08-10

Scientific implementation revision: `fcb2c49efdca2ad3ee502dc08fbb82fc285e7a05`

Parent protocol: `2026-08-09-gaussian-fixed-ray-v1a`
Execution state: design only; no new CUDA run or parameter search authorized

## Purpose

The Gaussian fixed-ray confirmatory experiment completed all 30 primary and 10
descriptive holdout jobs. The frozen primary analysis returned `inconclusive`:
the median projective-angle slope was `-0.00026786510016806844`, with 95% interval
`[-0.00029802317797700826, -0.00021070275415133334]`. The interval did not meet
the preregistered practical-support boundary `-0.02`, and no counterevidence rule
fired. The descriptive holdout estimate was `-0.00030310407296303384`, with
interval `[-0.00040771248808456155, -0.00019982541962230285]`.

This wave will:

1. durably record the completed CUDA sentinel and confirmatory result;
2. prove whether the practical-support boundary was reachable inside the frozen
   coefficient basin and endpoint definition; and
3. publish continuous fixed-map diagnostics that explain the observed finite
   trajectories without tuning a model, seed population, window, or threshold.

The wave may close finite claims about the two frozen maps, the endpoint's
feasible range, and deterministic replay of the 40 jobs. It cannot prove or
refute unrestricted Gaussian attraction, attraction on the full matrix coupling
cone, an infinite hierarchy, universality, or a continuum limit.

## Why the design was amended

Independent mathematical, numerical, implementation, and adversarial reviews
found that the first approved draft pinned a false adjacent-map spectrum and
used post hoc mechanism thresholds that did not identify causes. The source map
is

$$
A_{\mathrm{adj}}=\frac25 I+\frac1{10}\mathbf 1\mathbf 1^\top,
$$

so its spectrum is `1` together with five copies of `2/5`, not two copies of
`2/5` and three zeros. The amendment replaces the heuristic headline classifier
with an analytic feasibility certificate and continuous diagnostics. No
scientific implementation, execution artifact, preregistered endpoint, or result
is changed.

## Frozen scientific boundary

The following remain fixed:

- both six-dimensional row-stochastic maps returned by
  `build_preregistered_system()`;
- the Perron ray `(1,1,1,1,1,1)`, positive matrix direction `M0`, and scalarized
  construction `W_e=c_e M0`;
- `C001`-`C030` and `H001`-`H010` master-seed job literals;
- eight map applications and scales 4 through 8 for the endpoint;
- projective angle, raw-angle OLS, paired least-favorable reduction, bootstrap,
  and all preregistered thresholds; and
- `H` as hash-bound descriptive replication only.

This wave cannot retune `-0.02`, replace raw-angle OLS by log-angle OLS, select
seeds, alter a map or scale window, pool `C` and `H`, or use `H` to define any
primary conclusion. Any parameter or endpoint study requires a later exploratory
design.

## Decisive analytic certificate

Write an admissible initial coefficient vector as

$$
c_0=m\mathbf 1+d,\qquad d\perp\mathbf 1,
$$

and let `theta_k` be its projective angle to the Perron ray after `k` adjacent-map
applications. The adjacent map preserves the radial component and multiplies
every transverse component by `2/5`, hence

$$
\tan\theta_k=\left(\frac25\right)^k\frac{\lVert d\rVert_2}{\sqrt6\,m}.
$$

For entries in the frozen basin `[1/4,4]`, the Bhatia-Davis variance inequality
gives the coefficient-of-variation bound

$$
\frac{\lVert d\rVert_2}{\sqrt6\,m}\le
\frac{4-1/4}{2\sqrt{4(1/4)}}=\frac{15}{8}.
$$

Therefore

$$
\theta_4\le\arctan\left(\left(\frac25\right)^4\frac{15}{8}\right)
=\arctan\left(\frac6{125}\right).
$$

The frozen OLS slope on scales 4 through 8 is

$$
s=\frac{-2\theta_4-\theta_5+\theta_7+2\theta_8}{10}.
$$

The adjacent angles are nonnegative and decreasing, so

$$
s\ge-\frac3{10}\theta_4
\ge-\frac3{10}\arctan\left(\frac6{125}\right)
>-\frac9{625}=-0.0144>-\frac1{50}=-0.02.
$$

The last strict inequality uses `arctan(x) < x` for positive `x`. It leaves the
exact rational margin `7/1250` above the support boundary.

The preregistered paired endpoint is the least-favorable maximum of the adjacent
and alternating slopes. It is therefore at least the adjacent slope. For the
actual complete, in-basin run, every paired job endpoint, every resampled median,
and the upper percentile endpoint must remain above `-0.02`. Thus practical
`support` was structurally unreachable under the frozen basin and endpoint.

This is an application-specific endpoint-feasibility theorem. It does not show
that projective attraction is false; it shows that this preregistered practical
support rule could not certify it in the admitted finite model.

## Continuous map and trajectory diagnostics

The analytic certificate is the headline result. The remaining diagnostics are
continuous explanatory quantities, not a post hoc causal classifier.

For nonzero `u`, define

$$
\mathcal N_A(u)=\frac{Au}{\lVert Au\rVert_2},\qquad
D\mathcal N_A(u)[h]=\frac{(I-vv^\top)Ah}{\lVert Au\rVert_2},
\quad v=\mathcal N_A(u).
$$

The ambient Jacobian has a radial null direction and is therefore singular.
Condition numbers and propagator norms must be computed only after restriction to
orthonormal tangent bases. If `B_k` spans `T_{u_k}S^5`, define

$$
K_k=B_{k+1}^\top D\mathcal N_A(u_k)B_k.
$$

All trajectory propagators are products of these reduced `5 x 5` matrices. For
`balanced_alternating`, the Euclidean tangent is not invariant under `A`; Schur
and mode diagnostics therefore operate on the reduced normalized-map tangent
operator, not raw eigenvectors of `A`.

For seed/mode diagnostics, freeze the normalized Perron ray `u_*`,
`P_*=I-u_*u_*^T`, any orthonormal tangent basis `B_*`, and

$$
T_*=B_*^\top P_*AB_*.
$$

For `balanced_alternating`, the slow cluster is exactly the spectral-radius
cluster: the real eigenvalue `1/5` and the conjugate pair
`(3 +/- i sqrt(7))/20`, of total real dimension three. Use an ordered real-Schur
basis `Q_s` for that cluster and the orthogonal ambient projector
`Pi_s=B_*Q_sQ_s^TB_*^T`; do not use an oblique Riesz projector while calling the
result energy. For an initial literal, set
`delta_0=P_*(c_0/||c_0||_2)` and define

$$
g_m(\delta_0)=\frac{\lVert T_*^m B_*^\top\delta_0\rVert_2}
{\lVert B_*^\top\delta_0\rVert_2},\qquad
e_s(\delta_0)=\frac{\lVert\Pi_s\delta_0\rVert_2^2}
{\lVert\delta_0\rVert_2^2}.
$$

These are continuous reported quantities. The adjacent spectral-radius cluster is
the entire five-dimensional tangent, so a narrower adjacent slow-mode energy is
not identifiable and remains not applicable.

The diagnostic reports, separately for each map:

- exact characteristic polynomials for canonical rational map literals and a
  conformance check against the runtime float64 matrices;
- multiplicity-aware eigenvalue and Schur residuals;
- reduced Perron-tangent eigenvalues, singular values, and invariant-subspace
  projector residuals;
- absolute gains `||T^m||_2`, spectral-excess ratios
  `||T^m||_2/rho(T)^m`, and the frozen actual-direction gains above for
  `m=1,...,8`;
- reduced tangent propagators along every trajectory;
- exact use of the frozen projective-angle and OLS endpoint routines;
- map-specific and paired least-favorable `C` summaries; and
- an identically defined, separate `H` descriptive replication.

`Nonnormal amplification` is used only if an absolute gain exceeds one. Excess
over asymptotic spectral decay with all absolute gains below one is reported as
`nonnormal spectral excess`, not transient amplification. The adjacent tangent
spectrum is fivefold degenerate, so a narrower adjacent slow-mode alignment is
not identifiable and is marked not applicable. Alternating slow-subspace energy
is reported continuously through basis-independent spectral projectors.

The explanation record has two layers:

1. `support_boundary_unreachable_in_frozen_basin`, supported by the derivation;
2. continuous evidence about endpoint scale, reduced contraction, nonnormal
   spectral excess, and realized mode content.

It does not choose among heuristic labels using post hoc cutoffs.

## Software architecture

### Pure mathematics and diagnostics

Create `fixed_ray_diagnostics.py` with no filesystem or Git access. It owns
canonical Fraction map literals, exact characteristic polynomials, the basin
certificate, normalized-map derivatives, tangent bases, reduced propagators,
Schur/projector diagnostics, and continuous trajectory summaries.

### Durable source evidence and replay

Track a compact scientific extract of the completed confirmatory run under
`docs/verification/evidence/`. It contains the eight small scientific artifacts
needed for replay plus a source-binding JSON that records all ten original file
hashes and the coordinator-evidence hash. The two large execution logs remain
omitted but hash-bound. Unit tests use synthetic fixture factories; a dedicated
integration test checks the full tracked extract.

The diagnostic experiment accepts a typed source binding, validates every owned
file before publication, regenerates all 80 trajectories through the frozen
production functions, and records scientific and diagnostic revisions
separately. Calling the production path is deterministic replay, not independent
reconstruction. A separate tracked derivation and independent oracle provide the
independent checks.

### Publication and launcher

The click-to-run launcher exposes editable dictionaries and runs on CPU only. Its
source defaults to the tracked extract relative to repository root. Its output
root remains explicitly overrideable. The manifest records `artifact_kind`, the
typed source-binding digest, both revisions, and recomputed hashes for every
non-manifest artifact. NPZ replay compares canonical per-array hashes rather than
ZIP-container bytes.

Every producer-emitted record remains `CANDIDATE`. Only an external validated
ledger may promote a claim to `EVIDENCE_VERIFIED` or `REFUTED`.

## Repository and Research closeout

The tracked result document retains pilot and failed-sentinel history but adds a
single authoritative current-state section backed by machine-readable JSON. It
separates the primary boundary p-value, reported as the bootstrap resolution
floor `p <= 2/10001`, from the six Holm-adjusted secondary tests.

After the final MultiAgentELBO result, evidence extract, derivation, tests, and
ledger validate at one exact clean revision, the Research wiki receives one
immutable run note and calibrated project/RG updates. `C` is the only primary
population; `H` remains descriptive. The dirty Research checkout is not switched
or advanced because it is on a non-main review branch. Research publication uses
an isolated clean `main` worktree.

## Validation and failure behavior

Validation requires:

- exact Fraction derivations and a tracked mathematics derivation;
- a sphere-geodesic or scale-aware finite-difference ladder near
  `eps_machine^(1/3)`;
- reduced-tangent, not ambient-Jacobian, conditioning;
- scale-normalized Schur and subspace residual tolerances;
- all source-binding hashes and deterministic per-array hashes;
- separate `C` primary and `H` descriptive outputs;
- synthetic negative controls and a full tracked-extract integration test;
- two clean-root semantic reproductions;
- current machine-readable JUnit output; and
- independent code, mathematics, numerical, and experiment adjudication plus a
  validating revision-bound ledger.

The diagnostic fails closed on any source drift, nonfinite output, recurrence or
endpoint mismatch, derivative-control failure, or artifact hash mismatch. It may
publish a failure record but cannot promote a producer claim. Unresolved causal
interpretation remains `INCONCLUSIVE` even though the endpoint-feasibility theorem
is `ESTABLISHED`.

## Definition of done

This wave is complete only when:

- the result document accurately records the sentinel, 40-job run, and analytic
  endpoint-feasibility conclusion;
- the exact adjacent spectrum and basin certificate have derivation evidence;
- the 80 trajectories replay and continuous diagnostics are deterministic;
- all runtime records remain `CANDIDATE` and the external ledger validates at the
  exact final revision;
- the compact source and diagnostic evidence extracts are durable in Git;
- the full CPU suite and independent reviews pass;
- MultiAgentELBO is pushed, merged, and safely fast-forwarded without touching
  Desktop WIP; and
- the Research ingest is lint-clean, published through an isolated main worktree,
  and leaves the dirty live Research review branch untouched.
