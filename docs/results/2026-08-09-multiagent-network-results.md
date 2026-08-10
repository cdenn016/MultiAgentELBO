# Session 1 Multi-Agent Network Results

Date: 2026-08-09

Branch: `codex/multiagent-application-20260809`

Contract base: `b80df01f239c2f9a18842f6887cdeca67dff508f`

## Scope

This lane instantiates the frozen application ID
`30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd` as an
explicit four-binary-agent, two-block, one-arrow finite application. It checks
application premises and implementations of conditional finite identities. It
does not claim physical time, learned-agent behavior, universality, a continuum
limit, or a fixed-point theorem.

The frozen tuple supplies the correlated baseline, base observation record,
fine and coarse references, product-recognition family, local blocks,
configuration map, comparison records, and the strictly positive normalized
fine-to-coarse channel. Each scenario adds normalized interaction-success
records without replacing or rehashing the frozen fixture:

- `aligned`: all four cycle records prefer equal endpoint states;
- `frustrated`: three records prefer equality and `e30` prefers inequality, so
  no binary assignment satisfies every record simultaneously;
- `asymmetric_evidence`: aligned records use log2 penalties 1, 2, 3, and 4;
- `higher_order`: aligned cycle records plus the declared `h012` even-parity
  record with a two-bit log2 penalty.

All state laws, record kernels, channel entries, configuration maps, and
Hoeffding components are evaluated with `fractions.Fraction`. Logarithms, KL,
VFE, and displayed effective coarse actions are explicitly floating-point
evaluations of those exact rational inputs.

## Exact and numerical results

The exact scenario evidence masses are:

| Scenario | Evidence mass | Pairwise retained residual in log2 units |
|---|---:|---:|
| `aligned` | `91/512` | `0` |
| `frustrated` | `5/32` | `0` |
| `asymmetric_evidence` | `3515/32768` | `0` |
| `higher_order` | `775/8192` | `1` |

The `higher_order` residual is the pinned negative control: the complete
Hoeffding family reconstructs exactly, while pairwise retention omits the pure
`(0,1,2)` parity component with sup norm one. The other three declared actions
are pairwise and therefore have zero omitted residual.

The finalized aligned artifact reports:

| Metric | Value | Tolerance | `theorem_status` | `verification_state` | `claim_origin` |
|---|---:|---:|---|---|---|
| `evidence_residual` | `0` | `1.01e-10` | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` |
| `elbo_gap_residual` | `0` | `1.01e-10` | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` |
| `local_collective_residual` | `2.220446049250313e-16` | `1.01e-10` | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `PROJECT_NOVEL` |
| `hoeffding_reconstruction_residual` | `0` | `0` | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` |
| `recognition_lift_residual` | `0` | `0` | `HYPOTHESIS` | `EVIDENCE_VERIFIED` | `APPLICATION_SPECIFIC` |
| `pairwise_retained_residual` | `0` | `0` | `HYPOTHESIS` | `EVIDENCE_VERIFIED` | `APPLICATION_SPECIFIC` |

The aligned block-`B01` literal oracle is independently pinned at
`0.4496337464793081` for both the local and collective KL changes. The
overlapping-local-objective control differs from the joint objective by
`0.18747552763150188`; this prevents replacing one normalized collective VFE
with a sum of overlapping local objectives.

## Negative controls and premise boundaries

- A rehashed but nonnormalized channel is rejected before RNG construction or
  run-directory creation.
- A deliberately wrong uniform recognition lift has a nonzero right-inverse
  residual (`1/10` for the pinned coordinate control).
- The overlapping-local-objective sum disagrees with the correct joint
  functional on the frozen application.
- The higher-order scenario reconstructs exactly only in the complete
  interaction family; its pairwise omitted residual is exactly one.
- A parameter-dependent channel is recorded as
  `HYPOTHESIS/INCONCLUSIVE/APPLICATION_SPECIFIC` and described as outside the
  fixed-channel theorem. It is not labeled a refutation.
- `render_figures=True` fails before RNG or artifact creation because shared
  figure integration is outside this lane's ownership.

## Artifact and environment record

Representative aligned development artifact:

`.verification/session1/final-artifacts/multiagent-network-aligned/839d151244b0cad5ad42f44c2f2e3dac4cc9e1d40cf2a6f1d681b9bff6bdd670-20260809`

The bundle contains `metrics.json`, `claims.json`, `arrays.npz`,
`diagnostics.npz`, and the completed manifest. The six frozen semantic arrays
are present together with exact numerator/denominator arrays sufficient to
reconstruct their rational values. The manifest binds the fixture-file digest,
application ID, theory-tree digest, Git revision, dirty-tree digest, Python,
NumPy, SciPy, named RNG streams, and exact-versus-floating computation roles.

For that aligned run on `C:\Python314\python.exe`:

- validated scientific evaluation runtime: `0.026030200000604964 s`;
- tracemalloc peak: `157587 bytes`;
- Python: `3.14.4`;
- NumPy: `2.4.4`;
- SciPy: `1.17.1`.

Artifact SHA-256 values:

| File | SHA-256 |
|---|---|
| `metrics.json` | `fd8c4636afabbd7c485506b740fa09221f010d445afb114262b73314ee64b9a0` |
| `claims.json` | `5f32b6ba0da48ce3b2141a3b1049a5b1e1493b88b77418e584fc18e84a23bdc7` |
| `arrays.npz` | `246cdace6b6d75414a1044dc5384776648f8b966f25974046f37d6c795a4e098` |
| `diagnostics.npz` | `93d23d2e3017c7d24f81d6eb9fc67ffb9f07a76b94fe2492c5331172701db23c` |
| `manifest.json` | `9b5a88ce563f344256491d059631a8b394dae009c2b53c930724b8178c7016c8` |

## Verification commands

The lane uses the CPU-only Python 3.14 controller because it makes no CUDA
claim. Machine-readable evidence is written under ignored
`.verification/session1/` state.

```powershell
C:\Python314\python.exe -m pytest tests/test_agent_network.py tests/test_agent_network_experiment.py `
  --basetemp=.verification/session1/focused-final-tmp `
  --junitxml=.verification/session1/pytest-focused.xml

$env:COVERAGE_FILE='.verification/session1/.coverage-final'
C:\Python314\python.exe -m coverage run --branch --source=src/multiagent_elbo/finite `
  -m pytest tests/test_agent_network.py tests/test_agent_network_experiment.py `
  --basetemp=.verification/session1/coverage-final-tmp
C:\Python314\python.exe -m coverage xml `
  --include='*agent_network.py,*agent_network_experiment.py' `
  -o .verification/session1/coverage.xml
C:\Python314\python.exe -m coverage report `
  --include='*agent_network.py,*agent_network_experiment.py' --fail-under=80

C:\Python314\python.exe -m pytest `
  --basetemp=.verification/session1/full-final-tmp `
  --junitxml=.verification/session1/pytest-full.xml
```

The focused pre-commit JUnit report records 23 passed tests with no failures,
errors, or skips. The full pre-commit JUnit report records 463 collected, 461
passed, and two skipped. Branch-aware coverage is 82% for `agent_network.py`,
93% for `agent_network_experiment.py`, and 85% combined. Closure evidence is
rerun and parsed mechanically at the final lane commit rather than inferred
from this document or a console progress line.

## Remaining obligations

Independent cross-session mathematical and implementation review remains an
integration-stage obligation. Shared package exports, launcher registry,
figures, README, hypotheses, and final cross-laboratory metamorphics are frozen
shared paths and were not edited here. Continuum, universality, canonical
geometry, graph-to-base holonomy, physical-time, and learned-agent claims remain
`OPEN/INCONCLUSIVE` unless a separate proof or experiment closes them.
