# Gaussian Fixed-Ray Attack Preregistration

Date frozen: 2026-08-09  
Protocol ID: `2026-08-09-gaussian-fixed-ray-v1`  
Execution gate: `heavy_sweep_enabled=False` until a fresh idle-GPU check and explicit operator opt-in  
Theory boundary: the scoped fixed-ray statement is `CONJECTURE`; every finite floating-point result is `NUMERICAL`, and its mathematical `verification_state` remains `INCONCLUSIVE`.

## Scoped claim and finite domain

This experiment attacks only the fixed-`B` scalarized restriction in `Theory/10_renormalization.tex`. It does not test attraction on the full positive-semidefinite coupling cone, select a matrix direction, establish an infinite hierarchy, establish universality, or turn a nonautonomous cocycle into an autonomous map.

The finite domain is fixed as follows.

- Four spatial vertices give the six ordered edge-coordinate labels `(01, 02, 03, 12, 13, 23)`.
- The matrix dimension is exactly two and the declared, frozen matrix direction is

  \[
  M_0=\begin{pmatrix}2&1/2\\1/2&1\end{pmatrix}\succ0.
  \]

- Every admitted coupling has the scalarized form `W_e = c_e M0`, with all `c_e > 0`.
- Each initial coefficient is generated once on CPU as `exp(U(log(1/4), log(4)))` from the immutable job-derived substream. Hence every generated start lies in the declared basin `c_e in [1/4, 4]`, with coefficient condition ratio at most 16.
- The hierarchy has scale indices `0,...,8`, giving exactly eight applications of one fixed spatial map per blocking scheme. The primary scale window is the five endpoints at scales `4,...,8`.
- The Perron candidate is the positive vector `c*=(1,1,1,1,1,1)`, which factorizes as `c_ij=x_i x_j` with `x=(1,1,1,1)`.
- Both declared spatial maps are strictly positive in one step, so the finite primitivity premise is satisfied with `q=1`. Each is row stochastic and therefore has the displayed right Perron ray. This is a finite premise check, not an attraction theorem.

The paired fixed maps are

\[
B_{\rm adjacent}=\frac1{10}
\begin{pmatrix}
5&1&1&1&1&1\\
1&5&1&1&1&1\\
1&1&5&1&1&1\\
1&1&1&5&1&1\\
1&1&1&1&5&1\\
1&1&1&1&1&5
\end{pmatrix},
\]

and

\[
B_{\rm alternating}=\frac1{10}
\begin{pmatrix}
3&2&2&1&1&1\\
1&3&2&2&1&1\\
1&1&3&2&2&1\\
2&1&1&3&2&1\\
1&2&1&1&3&2\\
2&1&2&1&1&3
\end{pmatrix}.
\]

They share the declared right Perron ray but do not commute: the exact maximum entry magnitude of their commutator is `1/100`. This noncommuting pair is the blocking-scheme negative control; it prevents an accidental claim that paired agreement follows from commuting updates.

## Exact job table and CPU-generated population

Each job contains both blocking schemes applied to the identical initial coefficient literal. The substream seed is the displayed integer and the actual generator seed is the first unsigned 64-bit word of `SHA-256("gaussian-fixed-ray-v1\0" || decimal(master_seed) || "\0" || job_id)`, interpreted big-endian. Jobs may be executed in any order; scientific inputs are generated once on CPU and transferred as identical literals to every worker lane.

| Job IDs | Master seeds | Role | Threshold use |
|---|---|---|---|
| `P001`-`P004` | `202608090001`-`202608090004` | pilot | runtime/range/failure-mode estimation only |
| `C001`-`C030` | `202608090101`-`202608090130` | confirmatory primary population | primary and secondary inference |
| `H001`-`H010` | `202608090201`-`202608090210` | confirmatory holdout | untouched until the primary analysis is finalized |

The ranges expand by zero-padded consecutive IDs and consecutive integer seeds with no omissions. The planned table therefore contains exactly 44 paired initial conditions, 88 scheme trajectories, and 704 map applications. The pilot does not enter confirmatory estimates. The confirmatory primary population contains 30 independent initial conditions per scheme; the 10 paired holdouts are reported separately and never used to tune the basin, window, endpoint, tolerance, or effect threshold.

## Endpoints and decision rules

For every scale, initial condition, and scheme, record:

- projective ray angle `acos(<c,c*>/(||c|| ||c*||))`;
- normalized coupling distance `||c/||c|| - c*/||c*||||_2`;
- scalarized-ray construction residual, computed by Frobenius projection of every constructed `W_e=c_e M0` onto the frozen `M0` ray as a roundoff consistency diagnostic, not as a test of unrestricted matrix dynamics;
- exact comparison-typed retained beta residual divided by `log(2)`;
- basin exit indicator;
- paired blocking-scheme dispersion between normalized coefficient rays;
- coefficient and matrix-direction conditioning;
- rejection reason and rejected-run count.

The primary endpoint is the paired median ordinary-least-squares slope of projective ray angle over scales `4,...,8`, estimated across the 30 `C` initial conditions. The practical attraction threshold is a slope of at most `-0.02` radians per scale. The prespecified supporting endpoint is the median normalized coupling distance at scale 8. Secondary endpoints are the scalarized-ray construction residual, retained beta residual, basin-exit rate, scheme dispersion, conditioning, and rejection rate.

The finite numerical result is classified as support only if all of the following hold on the `C` population: the upper endpoint of the two-sided 95% paired bootstrap confidence interval for the median angle slope is at most `-0.02`; the median scale-8 normalized distance is at most `0.05`; the upper 95% confidence bound for median scheme dispersion is at most `0.02`; basin-exit and rejection rates are each at most `0.05`; and no primary endpoint changes status under the required float64 CPU/CUDA sentinel recomputation. A positive result is still only `theorem_status=NUMERICAL`.

Finite counterevidence is recorded if any one of these prespecified events occurs in-domain: the lower 95% confidence endpoint for the median angle slope is nonnegative; the lower 95% confidence endpoint for median scheme dispersion exceeds `0.05`; either basin-exit or rejection rate exceeds `0.20`; or the two schemes approach distinct projective rays under the paired endpoint rule. Floating-point counterevidence has mathematical `verification_state=INCONCLUSIVE`. Mathematical `REFUTED` requires a separate exact rational/analytic witness or a rigorously interval-certified in-domain witness satisfying every premise above.

The result is inconclusive if neither support nor counterevidence thresholds are met, the primary 95% interval half-width exceeds `0.02` radians per scale, any planned `C` job is missing after authorized retries, float64 decision stability fails, the preregistered premises fail, or the GPU/worker evidence gate is incomplete.

## Precision, uncertainty, multiplicity, and exclusions

Scientific confirmation uses float64. Float32 is a screening/throughput lane only and bfloat16 is exploratory only; neither may support a near-singular or confirmatory conclusion. The paired bootstrap uses 10,000 immutable resamples derived from a separate preregistered analysis substream and reports percentile 95% intervals. The primary endpoint is tested once at two-sided familywise alpha `0.05`. The six secondary endpoint families use Holm correction in the order induced by their unadjusted p-values; all unadjusted and adjusted values are retained. The holdout is descriptive replication under the already frozen thresholds, not a second opportunity to redefine success.

A run is rejected only for a nonfinite input/output, failure of exact job/manifest/hash identity, loss of symmetry or positive definiteness of `M0`, matrix-direction condition number above `1e12`, a coefficient leaving the strictly positive domain, or a worker protocol/backend/dtype mismatch. Threshold misses, basin exits, and nonattraction are outcomes, not exclusions. Every planned, completed, rejected, retried, and missing job remains in the manifest.

## Compute budget, sentinel parity, and stopping rule

The pilot budget is four paired CPU initial conditions, eight steps, float64, and at most 2 GB resident memory. It may run with `heavy_sweep_enabled=False`. The confirmatory budget is the 40 paired `C`/`H` initial conditions, eight steps, float64, one heavy job at a time, at most 5 minutes and 8 GB allocated GPU memory per paired job, with one retry only for infrastructure failure under the identical immutable job ID and explicit retry lineage. OOM is a failed job and never triggers silent batch adaptation.

Before confirmatory execution, the controller must record a fresh idle-GPU check, explicit operator opt-in, the frozen environment-lock digest, executable and worker hashes, requested/effective backend and dtype, Torch/CUDA/device/capability and library records, deterministic controls, peak allocated/reserved memory, and a full Python 3.14 CPU / Python 3.12 worker CPU / Python 3.12 worker CUDA float64 parity matrix. The sentinel subset is exactly `C001`, `C015`, `C030`, `H001`, and `H010`, including threshold-near and worst-conditioned realized strata. A fixed parity mutation must fail.

No job may stop early because the conjecture looks supported or unsupported. Execution stops only after the planned table is complete, after the single authorized infrastructure retry is exhausted, on protocol/provenance invalidity, on non-idle GPU detection, on operator withdrawal, or when the fixed compute budget is exhausted. None of those safety stops authorizes selective reporting or replacement jobs.
