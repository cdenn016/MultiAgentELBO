# Gaussian Fixed-Ray Results

Date: 2026-08-09

Preregistration: `2026-08-09-gaussian-fixed-ray-v1`

Execution: four paired pilot jobs only; Python 3.14 CPU controller plus isolated Python 3.12 worker CPU

CUDA: not requested by this ordinary CPU pilot; no gate-state assertion is emitted

## Current state

The final frozen confirmatory extract is bound to scientific revision
`fcb2c49efdca2ad3ee502dc08fbb82fc285e7a05`. Its machine-readable current state
is [current result](../verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/current_result.json),
and all ten original source hashes and sizes are in its
[source binding](../verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/source_binding.json).
The coordinator evidence SHA-256 is
`7fb07f04d709a3d07613fa220529875c7ddd63601940f3bbb2b87d2440b055fa`.
The copied confirmatory manifest, primary analysis, and holdout analysis hashes
are respectively `7e0a050850b48b446c70bff3a67010c84d2daa1fada6c48742d3ab152d43a1fb`,
`f8b58ae7f8777e18800c37d63b55d37c0052cd47b407a40497405ef5f6375155`,
and `ff09a656d7638a233d21149132367b95072fae6030187ee997290aa1a0596d1d`.
The raw SHA-256 of the copied published job-table file is
`a50dd3893ce1ad9c081a8e2f2cbc5adc676e2b217c9c3ec321e8b0d62b453adf`.
It is intentionally distinct from the frozen planned-table canonical JSON hash
`c3d019beb7c7cc1e6c1d383c3069745c528859aba4b1ded0de1c3a97449075cd`
embedded by the primary analysis, holdout analysis, and manifest. The binding
records the exact producer serialization and the reconstruction from the
published execution wrapper; the former is a scientific payload hash, not a
second raw-file SHA-256.

The successful final float64 CUDA sentinel completed its five parity-only jobs:
all 240 controller/worker exchanges and all scientific-decision parity checks
passed. Its manifest SHA-256 is
`beb0c5bcf0217aabf06cacc974bf44db29e6bbab8e0c16b64fc2e331b99617c7` and
its parity SHA-256 is
`50f7e9889db083c17d6d55649aaa9b3577b64fbbf54b512a6c0217a1d6cc135c`.
The sentinel is not scientific analysis evidence, but it clears the required
execution parity check for the completed confirmatory run.

The planned 40-job confirmatory run completed all 40 jobs: the 30
`C001`--`C030` primary jobs and the separate 10 `H001`--`H010` holdout jobs.
The terminal counts are zero missing jobs, zero rejected jobs, zero retried
jobs, and zero basin-exit events.
The 30-job primary estimate is `-0.00026786510016806844`, with the bootstrap
interval `[-0.00029802317797700826, -0.00021070275415133334]`; its frozen
classification remains `inconclusive`.

The primary practical-support boundary result is `p <= 2/10001`, the bootstrap
resolution floor, in the unfavorable direction relative to the frozen `-0.02`
boundary. This result is distinct from the six Holm-adjusted secondary tests:
conditioning trend, construction residual, retained beta trend, scheme
dispersion, basin-exit rate, and rejection rate. Those secondary tests do not
replace, retune, or reverse the primary boundary classification.

The holdout is a separate descriptive replication only, not pooled with `C`.
Its estimate is `-0.00030310407296303384` with bootstrap interval
`[-0.00040771248808456155, -0.00019982541962230285]`. All producer records
represented by this extract, including the primary, holdout, and sentinel
records, remain
`CANDIDATE`; the finite result remains `NUMERICAL`, and mathematical attraction
remains `INCONCLUSIVE`.

### Fixed-model endpoint-feasibility diagnostic

The deterministic CPU diagnostic is bound to diagnostic source revision
`039df35daa30a49e90f178edde7bfc999a7ee629`, the unchanged scientific revision
`fcb2c49efdca2ad3ee502dc08fbb82fc285e7a05`, and source-binding SHA-256
`c9b6a73764f51b6269f7ba4296985128ede106fa4853d9a02d83d4bbe24d95c0`.
The nine-file public extract is recorded by its
[source-to-output binding](../verification/evidence/2026-08-10-fixed-model-attraction-diagnostic/source_to_output_binding.json),
whose SHA-256 is
`df3130e56bfd1bdd91801a13b6f6ffabe16931813a264ff3e2e2805891b7a355`.
The public manifest, exact support certificate, spectral diagnostics,
continuous trajectory diagnostics, and per-array NPZ have respective SHA-256
values `1829624d76fe723606b5e20fbd7ad85961610b2513c59271c641f560ac38d907`,
`a65bd15e36d85cf810cdb5f7bb5a7bf0dcfcf56672d6601e3d7237be06b07c8b`,
`8f1fbf50ca691c0245c0e59eaaced25af6c02aa5b4f46ac0d7908961e8e8669b`,
`e6169a6fad904bf92082f6d1c12203a8d843e01e473804e1dae3161037111f4f`,
and `1597a92acf50811687183f0062f104acb3c5e4649bb6270e0b153841f9e08bff`.
The raw Run-A manifest is not tracked; the binding records only its SHA-256 and
size and enumerates the public manifest's sole redaction at
`/provenance/theory_root`, replaced by `Theory`.

For `adjacent_pairs`, the exact characteristic polynomial is
`(lambda - 1)(lambda - 2/5)^5`, so the spectrum is `1` once and `2/5` five
times. For `balanced_alternating`, it is
`(lambda - 1)(5 lambda - 1)(50 lambda^2 - 15 lambda + 2)(100 lambda^2 - 30 lambda + 3)/25000`,
with spectrum `1`, `1/5`, `(3 +/- i sqrt(7))/20`, and
`(3 +/- i sqrt(3))/20`. The adjacent-map certificate gives the exact rational
OLS lower bound `-9/625`, leaving margin `7/1250` above the frozen threshold
`-1/50`.

Under initial coefficients in `[1/4,4]^6`, the two frozen maps, complete
uncensored endpoints, scales 4 through 8 raw-angle OLS, and the per-job
least-favorable maximum, the `-0.02` practical-support boundary is structurally
unreachable. This endpoint-feasibility theorem is
`ESTABLISHED / CANDIDATE / APPLICATION_SPECIFIC`. It does not refute attraction
and does not prove a mechanism.

The continuous primary-C paired median is `-0.0002678651001680694` across 30
jobs. The separate descriptive-H paired median is `-0.0003031040729630512`
across 10 jobs; no C/H pool is present. Both summaries are
`NUMERICAL / CANDIDATE / APPLICATION_SPECIFIC`. The confirmatory classification
remains unchanged at `inconclusive`, fixed-model mathematical attraction remains
`INCONCLUSIVE`, and unrestricted universality remains `OPEN / INCONCLUSIVE`.

## Historical pilot record

The pilot and failed-sentinel material below is retained as dated history. Any
ledger or verification labels in those sections are revision-bound to the
artifacts named there; they are not the current producer state above.

## Pilot outcome

The pilot completed all `P001`-`P004` jobs, both noncommuting blocking schemes, and all eight finite scale steps without rejection or basin exit. The overall status remains `inconclusive`: the pilot is excluded from confirmatory inference, the preregistered `C` and `H` jobs were not run, and the required float64 CUDA sentinel parity evidence is absent.

Positive finite trends are typed `NUMERICAL`. They do not select a unique matrix direction `M0`, prove infinite attraction, establish universality, or extend outside the frozen scalarized cone.

| Pilot diagnostic | Recorded value | Metric status | Claim typing |
|---|---:|---|---|
| Median scale-8 projective ray angle | `1.8964891266716035e-4` rad | pass | `NUMERICAL / EVIDENCE_VERIFIED / APPLICATION_SPECIFIC` |
| Median scale-8 normalized coupling distance | `1.8964894228803603e-4` | pass | `NUMERICAL / EVIDENCE_VERIFIED / APPLICATION_SPECIFIC` |
| Maximum scalarized-ray construction residual | `1.7771674674387606e-16` | pass | `NUMERICAL / EVIDENCE_VERIFIED / APPLICATION_SPECIFIC` |
| Median final retained beta residual norm | `1.3155508488955265e-3` | pass | `NUMERICAL / EVIDENCE_VERIFIED / APPLICATION_SPECIFIC` |
| Final signed retained beta component range | `[-2.409409114073506e-3, 1.5281165231984949e-3]` | pass | `NUMERICAL / EVIDENCE_VERIFIED / APPLICATION_SPECIFIC` |
| Basin-exit rate | `0` | pass | `NUMERICAL / EVIDENCE_VERIFIED / APPLICATION_SPECIFIC` |
| Median scale-8 scheme dispersion | `4.647541415137177e-4` | pass | `NUMERICAL / EVIDENCE_VERIFIED / APPLICATION_SPECIFIC` |
| Controller CPU versus worker CPU maximum residual | `2.220446049250313e-16` | CPU subcheck passed | CUDA metric remains `OPEN / INCONCLUSIVE_NOT_REQUESTED_CPU_PILOT / APPLICATION_SPECIFIC` |

The eight preregistered-window pilot slopes ranged from approximately `-4.97e-3` to `-2.77e-4` radians per scale. None reaches the preregistered practical confirmatory threshold of `-0.02`; this is descriptive pilot output only and cannot be used to retune the frozen threshold or population.

## Oracles and negative controls

- The independent noncommuting-map oracle was `0.010000000000000009`, matching the exact `1/100` target within `1e-15`.
- Replacing the second map by the first made the commutator gap exactly zero, demonstrating that the control detects the pinned mutation.
- Adding `1e-3` to one parity output produced a failed parity comparison; the negative-control metric therefore passed.
- The constructor forms every coupling as `W_e=c_e M0`; the scalarized-ray construction residual therefore measures only float64 roundoff consistency and is not evidence about unrestricted matrix dynamics.
- The signed retained beta array is `(I-P)(c_(k+1)-c_k)/log(2)`. The literal adjacent-map oracle starts with `[1.5, 0.9, 0.3, -0.3, -0.9, -1.5]/log(2)`; the former next-state mutation has different signs and fails the oracle.

## Backend and protocol evidence

The worker request and response were bound by immutable job ID `PILOT-CPU-ONE-STEP`, exact output inventory, request-derived shapes/dtypes, per-array hashes, NPZ hashes, and output identity `3e5c563e5a43cd5ac393408fda5d6a16acabd2f922de028a3812165febf040c1`. The frozen lock digest was `b1309f089eda1914df7e87704628e367706e50203441aba775517fefa02838a2`; the worker executable hash was `6965927a96b81d1717c1d2186de7feb9b29ebf8775464020ebc2f25de6ef8ee0`. Requested and effective worker values were both `cpu/float64`. The validated CPU provenance records `rowwise_spatial_map_matvec`, runtime, retry lineage, lock consistency, and explicit null CUDA driver/cuBLAS/library fields.

The CUDA lanes are explicitly recorded as `not_requested_cpu_pilot` / `INCONCLUSIVE_NOT_REQUESTED_CPU_PILOT`, with null requested/effective backend and dtype, a null gate record, and null CUDA runtime/memory. The CPU pilot makes no busy/idle or operator-decision assertion; such a state would require a separately validated, timestamped, hash-bound gate record. No CPU fallback is presented as CUDA evidence. `heavy_sweep_enabled` remained false and `confirmatory_executed` remained false.

## 2026-08-10 CUDA sentinel attempt and numerical correction (historical failed attempt)

A later float64 parity sentinel at source revision `f3d26921424d012aee472b08cff998b6c0cc1b5e` used operator-gate digest `210bbbbd9226121061600d402e504c212f9887c6921f7d77665ffe2a1a692158`. It completed all 240 controller/worker exchanges for `C001`, `C015`, `C030`, `H001`, and `H010`, while preserving the `H` jobs as parity-only and ineligible for scientific analysis. Every stepwise controller-CPU, worker-CPU, worker-CUDA, and repeated-worker-CUDA comparison passed, CUDA repeatability was exact, and every basin/rejection/threshold decision agreed.

The sentinel nevertheless failed closed before publication because the `H010` `balanced_alternating` angle slope differed from the controller by approximately `3.5e-12`, above the endpoint parity tolerance. The controller value was `-0.00014309631977561107`, the worker-CPU value was `-0.0001430963162191419`, and both CUDA repetitions returned `-0.0001430963162673183`. The same failure in the independent worker-CPU lane, together with passing trajectory parity and exact CUDA repeatability, localized the discrepancy to the derived endpoint rather than the CUDA kernel.

Revision `dae4a4f` replaces the ill-conditioned near-parallel evaluation `acos(dot(u, v))` with the algebraically equivalent chord formula `2*asin(norm(u-v)/2)` for normalized rays. A pinned `1e-6`-radian positive-ray regression fails under the former formula and passes under the correction. Recomputing the preserved trajectories with the corrected formula reduces the `H010` slope differences to approximately `1e-17` without changing the estimand, thresholds, job IDs, seeds, or categorical decisions. The failed digest namespace remains immutable negative evidence. It is not a successful sentinel artifact, does not close CUDA parity, and does not authorize confirmatory execution; a complete fresh-gate rerun at the new final source revision is required.

## Evidence artifact

The non-publication evidence run was written under the ignored repository-local path:

`.pytest-tmp/session6-round3-pilot-evidence/session6-round3-pilot-evidence/5380a859c02eee1581bd764dba42ef8412d2e64348cff012c95cb36749e48f4c-20260809`

It contains the full 44-job planned table, four CPU-generated pilot literals, every pilot trajectory and diagnostic array, per-seed endpoints, backend provenance, request/response manifests, parity matrix, performance record, and typed metrics.
