# Gaussian Fixed-Ray Confirmatory Analysis Design

Date approved: 2026-08-10  
Parent protocol: `2026-08-09-gaussian-fixed-ray-v1`  
Execution state: design only; `heavy_sweep_enabled=False`

## Purpose and boundary

This design closes the statistical-definition gap that remained after the CUDA
float64 parity sentinel. It freezes the independent analysis unit, the paired
reductions, the six secondary null hypotheses, exact p-value construction, the
Holm family, holdout release, rejection handling, and output artifacts before
any confirmatory `C` or `H` job is executed.

The experiment remains a finite, application-specific numerical attack on the
fixed-`B`, fixed-`M0`, scalarized Gaussian restriction. A successful result may
support the frozen finite claim. It cannot prove attraction on the unrestricted
coupling cone, select `M0`, establish an infinite hierarchy, or establish
universality.

## Considered approaches

Three approaches were considered.

1. Exact job-level threshold tests. Reduce each paired job once, test the
   preregistered threshold or a structural zero boundary, and apply Holm to the
   six resulting p-values. This is the selected approach because it preserves
   independence, matches the frozen decision rules, and minimizes distributional
   assumptions.
2. Null-centered bootstrap p-values for all secondary endpoints. This was
   rejected because it adds Monte Carlo dependence and extra implementation
   choices where exact sign or binomial tests are available.
3. Paired blocking-scheme contrast tests. This was rejected because it answers
   whether the schemes differ, rather than whether the finite trajectories meet
   the attraction, stability, and validity thresholds.

## Independent unit and paired reductions

The independent unit is one master-seed job. The two blocking schemes and the
eight map applications within a job are repeated measurements, not independent
replicates. Primary inference uses exactly `C001`-`C030`. Pilot jobs never enter
confirmatory estimates. Holdout jobs remain analysis-ineligible until the
complete primary analysis is finalized and hash-bound.

For a quantity where smaller is better, the paired job statistic is the larger,
least favorable value across the two schemes. For a Boolean failure event, the
paired job statistic is true if either scheme has the event. These reductions
make support require acceptable behavior under both frozen noncommuting schemes
without pseudo-replication.

## Primary and supporting endpoints

For each scheme, fit the ordinary-least-squares slope of projective ray angle at
scales `4,5,6,7,8`. For job `i`, define the primary statistic

`S_i = max(slope_adjacent_i, slope_alternating_i)`.

The primary estimand is `median_i(S_i)` over the 30 `C` jobs. Its two-sided 95%
percentile interval is computed from 10,000 immutable whole-job bootstrap
resamples. The existing support, counterevidence, interval-width, and
inconclusive thresholds remain unchanged. The primary two-sided p-value at the
practical boundary `-0.02` is computed from the null-centered bootstrap
distribution with the finite-resample `+1` correction and capped at one.

The supporting scale-8 normalized-distance statistic is the worse paired value
for each job. Its median and two-sided 95% whole-job percentile interval are
reported. Its frozen `0.05` threshold remains a decision-rule component, not a
seventh member of the secondary Holm family.

## Six secondary hypotheses

All alternatives point in the favorable, lower-is-better direction. Exact tests
use the 30 independent paired `C` job summaries.

| ID | Endpoint and per-job statistic | Null hypothesis | Unadjusted p-value |
|---|---|---|---|
| `construction_residual` | Maximum scalarized-ray construction residual over both schemes and all recorded scales | population median is at least `1e-12` | exact one-sided sign test |
| `retained_beta_trend` | Larger OLS slope of retained beta residual over labeled scales `4,...,8` | population median slope is at least `0` | exact one-sided sign test |
| `basin_exit_rate` | Either scheme exits the basin at any recorded scale | event probability is at least `0.05` | exact lower-tail binomial test at `p=0.05` |
| `scheme_dispersion` | Paired normalized-ray dispersion at scale 8 | population median is at least `0.02` | exact one-sided sign test |
| `conditioning_trend` | Larger OLS slope of log coefficient conditioning over scales `4,...,8` | population median slope is at least `0` | exact one-sided sign test |
| `rejection_rate` | Either scheme is rejected | event probability is at least `0.05` | exact lower-tail binomial test at `p=0.05` |

For a sign test, observations exactly equal to the null boundary do not count as
favorable. If `k` of `n` valid job summaries are strictly below the boundary,
the p-value is `P(Binomial(n, 1/2) >= k)`. For an event-rate test with `x` events,
the p-value is `P(Binomial(n, 0.05) <= x)`. These definitions are conservative
at ties and at the composite-null boundary.

Holm adjustment is applied once across the six unadjusted p-values. Sort by
`(unadjusted_p, endpoint_id)`, multiply the ordered p-values by the remaining
family size, enforce the cumulative-maximum monotonicity rule, and cap at one.
Retain the original endpoint order, raw p-values, adjusted p-values, ranks, and
rejection decisions at familywise alpha `0.05`.

Holm significance is reported but does not add, remove, or retune any existing
support or counterevidence criterion. The scientific classification is computed
only from the frozen preregistered decision rules.

## Bootstrap substream

Every bootstrap resample draws complete job indices with replacement, thereby
preserving the two-scheme pairing and all within-job repeated measurements. The
resample seed is derived from the protocol ID, the exact confirmatory job-table
hash, the literal label `confirmatory-analysis-bootstrap-v1`, and the endpoint
ID. Exactly 10,000 resamples are used. The implementation records the derived
unsigned 64-bit seed, sample count, endpoint label, input hash, and output hash.

## Rejections, missing jobs, and retries

No rejected or failed job is silently dropped. A job with a scientifically
defined rejection contributes true to `rejection_rate`. When its continuous
endpoint is unavailable, it is ordered as least favorable for threshold and
sign-test decisions. Numeric summaries explicitly report the number of such
right-censored worst-case observations rather than serializing infinity.

Infrastructure failures receive only the single preregistered retry under the
same immutable job ID and exact input identity. An exhausted infrastructure
failure is missing. Any missing `C` job forces the overall classification to
`inconclusive`, while completed data and the full failure manifest remain
published.

## Two-stage primary and holdout release

The controller first executes and publishes all `C` jobs. It then computes the
primary analysis and writes a canonical primary-analysis record whose digest is
bound into the manifest. Only after that record exists may `H001`-`H010` become
analysis-eligible.

The holdout is analyzed once with the same reductions, estimators, intervals,
and frozen thresholds. Holdout results are descriptive replication: no p-values,
no Holm adjustment, no threshold changes, no tuning, and no second opportunity
to change the primary classification. The holdout record stores the exact
primary-analysis digest that authorized release.

The five previously executed sentinel jobs remain parity-only. Their sentinel
values never enter either primary or holdout scientific analysis; confirmatory
execution must rerun those immutable job IDs under the heavy-sweep protocol.

## Execution and provenance gate

Confirmatory execution requires all of the following at the current clean source
revision:

- the committed preregistration amendment and its canonical SHA-256;
- a passing current-revision CPU suite and CUDA worker check;
- a successful current-revision float64 CUDA parity sentinel;
- a fresh idle-GPU record immediately before execution and before every outer
  `C` or `H` job;
- explicit operator opt-in for the heavy sweep, separate from sentinel opt-in;
- exact executable, worker, environment-lock, config, job-table, and analysis
  contract hashes;
- `C` completion and hash-bound primary analysis before holdout release.

Observed resident processes may remain only when their exact PID set was
explicitly accepted by the operator and stays stable with zero utilization and
stable memory across the frozen samples. The controller never kills processes.
Any change in process set, utilization, memory, identity binding, operator
authorization, or protocol state fails closed without replacing jobs.

## Artifact contract

The confirmatory bundle adds these immutable records to the ordinary run-store
inventory:

- `confirmatory_job_table.json`: all planned jobs and execution/retry state;
- `confirmatory_endpoints.json`: per-job, per-scheme endpoints and rejection data;
- `primary_analysis.json`: estimands, bootstrap records, six raw and Holm-adjusted
  secondary tests, classification inputs, and primary classification;
- `holdout_analysis.json`: descriptive replication bound to the primary digest;
- `confirmatory_execution.json`: gate rechecks, worker identities, runtime,
  memory, stopping reason, and complete/missing/rejected counts;
- `confirmatory_arrays.npz`: immutable trajectories and diagnostic arrays needed
  for independent recomputation.

The manifest records `confirmatory_executed=true` only when all 40 planned jobs
have terminal records and the two-stage analysis artifacts validate. Producer
metrics remain `NUMERICAL/CANDIDATE/APPLICATION_SPECIFIC`; only an external,
revision-bound verification ledger may promote eligible finite implementation
or experiment claims to `EVIDENCE_VERIFIED`.

## Verification strategy

Implementation follows strict test-driven development. Unit tests pin exact sign
and binomial tails, Holm ordering and ties, bootstrap determinism, paired
least-favorable reductions, rejection censoring, primary-before-holdout release,
sentinel exclusion, gate rechecks, retry lineage, and artifact hashes. Integration
tests use small injected worker fixtures and may not execute the 40-job GPU sweep.
The real sweep runs only after the implementation suite, CUDA worker test,
current-revision sentinel, ledger validation, and explicit heavy-sweep opt-in all
pass.
