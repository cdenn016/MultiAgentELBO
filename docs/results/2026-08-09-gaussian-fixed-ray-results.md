# Gaussian Fixed-Ray Pilot Results

Date: 2026-08-09

Preregistration: `2026-08-09-gaussian-fixed-ray-v1`

Execution: four paired pilot jobs only; Python 3.14 CPU controller plus isolated Python 3.12 worker CPU

CUDA: not requested by this ordinary CPU pilot; no gate-state assertion is emitted

## Outcome

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

## 2026-08-10 CUDA sentinel attempt and numerical correction

A later float64 parity sentinel at source revision `f3d26921424d012aee472b08cff998b6c0cc1b5e` used operator-gate digest `210bbbbd9226121061600d402e504c212f9887c6921f7d77665ffe2a1a692158`. It completed all 240 controller/worker exchanges for `C001`, `C015`, `C030`, `H001`, and `H010`, while preserving the `H` jobs as parity-only and ineligible for scientific analysis. Every stepwise controller-CPU, worker-CPU, worker-CUDA, and repeated-worker-CUDA comparison passed, CUDA repeatability was exact, and every basin/rejection/threshold decision agreed.

The sentinel nevertheless failed closed before publication because the `H010` `balanced_alternating` angle slope differed from the controller by approximately `3.5e-12`, above the endpoint parity tolerance. The controller value was `-0.00014309631977561107`, the worker-CPU value was `-0.0001430963162191419`, and both CUDA repetitions returned `-0.0001430963162673183`. The same failure in the independent worker-CPU lane, together with passing trajectory parity and exact CUDA repeatability, localized the discrepancy to the derived endpoint rather than the CUDA kernel.

Revision `dae4a4f` replaces the ill-conditioned near-parallel evaluation `acos(dot(u, v))` with the algebraically equivalent chord formula `2*asin(norm(u-v)/2)` for normalized rays. A pinned `1e-6`-radian positive-ray regression fails under the former formula and passes under the correction. Recomputing the preserved trajectories with the corrected formula reduces the `H010` slope differences to approximately `1e-17` without changing the estimand, thresholds, job IDs, seeds, or categorical decisions. The failed digest namespace remains immutable negative evidence. It is not a successful sentinel artifact, does not close CUDA parity, and does not authorize confirmatory execution; a complete fresh-gate rerun at the new final source revision is required.

## Evidence artifact

The non-publication evidence run was written under the ignored repository-local path:

`.pytest-tmp/session6-round3-pilot-evidence/session6-round3-pilot-evidence/5380a859c02eee1581bd764dba42ef8412d2e64348cff012c95cb36749e48f4c-20260809`

It contains the full 44-job planned table, four CPU-generated pilot literals, every pilot trajectory and diagnostic array, per-seed endpoints, backend provenance, request/response manifests, parity matrix, performance record, and typed metrics.
