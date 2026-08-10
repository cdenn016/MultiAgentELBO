# Gaussian Fixed-Ray Pilot Results

Date: 2026-08-09

Preregistration: `2026-08-09-gaussian-fixed-ray-v1`

Execution: four paired pilot jobs only; Python 3.14 CPU controller plus isolated Python 3.12 worker CPU

CUDA: not run because the fresh preflight reported a busy RTX 5090 and no operator opt-in was given

## Outcome

The pilot completed all `P001`-`P004` jobs, both noncommuting blocking schemes, and all eight finite scale steps without rejection or basin exit. The overall status remains `inconclusive`: the pilot is excluded from confirmatory inference, the preregistered `C` and `H` jobs were not run, and the required float64 CUDA sentinel parity evidence is absent.

Positive finite trends are typed `NUMERICAL`. They do not select a unique matrix direction `M0`, prove infinite attraction, establish universality, or extend outside the frozen scalarized cone.

| Pilot diagnostic | Recorded value | Metric status | Claim typing |
|---|---:|---|---|
| Median scale-8 projective ray angle | `1.8964891266716035e-4` rad | pass | `NUMERICAL / EVIDENCE_VERIFIED / APPLICATION_SPECIFIC` |
| Median scale-8 normalized coupling distance | `1.8964894228803603e-4` | pass | `NUMERICAL / EVIDENCE_VERIFIED / APPLICATION_SPECIFIC` |
| Maximum off-family nonlinear remainder | `1.7771674674387606e-16` | pass | `NUMERICAL / EVIDENCE_VERIFIED / APPLICATION_SPECIFIC` |
| Median final retained beta residual | `8.660655934822545e-4` | pass | `NUMERICAL / EVIDENCE_VERIFIED / APPLICATION_SPECIFIC` |
| Basin-exit rate | `0` | pass | `NUMERICAL / EVIDENCE_VERIFIED / APPLICATION_SPECIFIC` |
| Median scale-8 scheme dispersion | `4.647541415137177e-4` | pass | `NUMERICAL / EVIDENCE_VERIFIED / APPLICATION_SPECIFIC` |
| Controller CPU versus worker CPU maximum residual | `2.220446049250313e-16` | CPU subcheck passed | CUDA metric remains `OPEN / INCONCLUSIVE / APPLICATION_SPECIFIC` |

The eight preregistered-window pilot slopes ranged from approximately `-4.97e-3` to `-2.77e-4` radians per scale. None reaches the preregistered practical confirmatory threshold of `-0.02`; this is descriptive pilot output only and cannot be used to retune the frozen threshold or population.

## Oracles and negative controls

- The independent noncommuting-map oracle was `0.010000000000000009`, matching the exact `1/100` target within `1e-15`.
- Replacing the second map by the first made the commutator gap exactly zero, demonstrating that the control detects the pinned mutation.
- Adding `1e-3` to one parity output produced a failed parity comparison; the negative-control metric therefore passed.
- The scalarized coupling arrays retained every `W_e=c_e M0`, with only float64 roundoff in the Frobenius projection residual.

## Backend and protocol evidence

The worker request and response were bound by immutable job ID `PILOT-CPU-ONE-STEP`, per-array hashes, NPZ hashes, and output identity `3e5c563e5a43cd5ac393408fda5d6a16acabd2f922de028a3812165febf040c1`. The frozen lock digest was `b1309f089eda1914df7e87704628e367706e50203441aba775517fefa02838a2`; the worker executable hash was `6965927a96b81d1717c1d2186de7feb9b29ebf8775464020ebc2f25de6ef8ee0`. Requested and effective worker values were both `cpu/float64`.

The CUDA lanes are explicitly recorded as `not_run_busy_gpu`, with null effective backend/dtype and null CUDA runtime/memory. No CPU fallback is presented as CUDA evidence. `heavy_sweep_enabled` remained false and `confirmatory_executed` remained false.

## Evidence artifact

The non-publication evidence run was written under the ignored repository-local path:

`.pytest-tmp/session6-pilot-evidence/session6-pilot-evidence/7cb33d88a88013a5e11b06dcd8df87ec2f6c6971fe53b9bba47a3063312c0b1f-20260809`

It contains the full 44-job planned table, four CPU-generated pilot literals, every pilot trajectory and diagnostic array, per-seed endpoints, backend provenance, request/response manifests, parity matrix, performance record, and typed metrics.
