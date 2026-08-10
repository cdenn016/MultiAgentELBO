# Exact theory-oracle results — 2026-08-09

## Outcome

Session 2 provides a standard-library `Fraction` oracle and a separate
floating-point experiment path for five groups of finite identities. At the
reviewed source revision, all 52 focused tests passed, both new production
modules exceeded the required 80% line-coverage threshold, and the
dictionary-driven no-argument launcher finalized nine artifacts containing
five passing implementation-comparison metrics. Same-seed runs in two output
roots produced byte-identical semantic artifacts.

These results verify the implementation at the stated finite fixtures and
premises. The mathematical evidence is the independent derivation in
`docs/verification/reviews/2026-08-09-theory-oracle-review.md`; the small
floating residuals below corroborate code behavior but do not prove any
identity. Application-family premises that the lane does not check remain
inconclusive.

## Revision and owned scope

| Item | Value |
|---|---|
| Branch | `codex/exact-theory-oracles-20260809` |
| Contract-freeze base | `b80df01f239c2f9a18842f6887cdeca67dff508f` |
| Tested source and review revision | `9f9425fa14485845e0fcb8d618f2a3d3ce4ab3ad` |
| Manifest Git state | `git_dirty=false` |
| Theory tree SHA-256 | `a7fddfcb8c67dbec71c7a35d0e415313a38154719e05d6ccd73672a810939343` |
| Frozen application ID | `30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd` |
| Frozen fixture file SHA-256 | `a207eba1e9f3a36e80d809940405dce178f20c52dffc2482bbc24f4fc26df567` |

The exact Session 2 changed-path set relative to the contract freeze, before
this result file is committed, is:

- `src/multiagent_elbo/finite/theory_oracles.py`
- `src/multiagent_elbo/finite/theory_oracle_experiment.py`
- `run_theory_oracle_lab.py`
- `tests/test_theory_oracles.py`
- `tests/test_theory_oracle_experiment.py`
- `docs/verification/reviews/2026-08-09-theory-oracle-review.md`

This document is the seventh and final lane-owned path. No `Theory/**`, shared
configuration, package export, artifact/runtime, rendering, dependency,
registry, README, existing launcher, or other lane's path is part of the
Session 2 diff.

## Environment and commands

The evidence used the mandated explicit CPU interpreter. No CUDA claim is
made.

| Component | Version or value |
|---|---|
| Interpreter | `C:\Python314\python.exe` |
| Python | 3.14.4, 64-bit MSC v.1944 |
| Platform | Windows 10.0.19045 |
| pytest | 9.0.2 |
| Coverage.py | 7.15.2 |
| NumPy | 2.4.4 |
| SciPy | 1.17.1 |
| Compute policy | CPU, float64, deterministic, TF32 disabled |
| Root seed | 20260809 |

Focused JUnit was generated with:

```powershell
C:\Python314\python.exe -m pytest `
  tests/test_theory_oracles.py `
  tests/test_theory_oracle_experiment.py `
  -q -p no:cacheprovider `
  --basetemp=.verification/session2-results-draft/9f9425f/focused-basetemp `
  --junitxml=.verification/session2-results-draft/9f9425f/pytest.xml
```

Branch-aware coverage and the lane-scoped XML were generated with:

```powershell
C:\Python314\python.exe -m coverage run `
  --data-file=.verification/session2-results-draft/9f9425f/.coverage `
  --branch --source=src -m pytest `
  tests/test_theory_oracles.py `
  tests/test_theory_oracle_experiment.py `
  -q -p no:cacheprovider `
  --basetemp=.verification/session2-results-draft/9f9425f/coverage-basetemp

C:\Python314\python.exe -m coverage xml `
  --data-file=.verification/session2-results-draft/9f9425f/.coverage `
  --include=*/theory_oracles.py,*/theory_oracle_experiment.py `
  -o .verification/session2-results-draft/9f9425f/coverage-lane.xml
```

The following path-safe recipe invokes the no-argument launcher from a fresh
working directory with an empty `PYTHONPATH`:

```powershell
$repo = (Resolve-Path '.').Path
$token = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$launchCwd = Join-Path $repo ".verification/session2-results-draft/9f9425f/launcher-sanitized-$token"
New-Item -ItemType Directory -Path $launchCwd | Out-Null
Push-Location $launchCwd
try {
  $env:PYTHONPATH = ''
  & 'C:\Python314\python.exe' (Join-Path $repo 'run_theory_oracle_lab.py')
  if ($LASTEXITCODE -ne 0) { throw "launcher exit code $LASTEXITCODE" }
} finally {
  Pop-Location
}
```

The editable `RUN`, `THEORY`, `NUMERICS`, `OUTPUT`, and `COMPUTE` dictionaries
in that file are the user interface. The launcher has no `argparse` or CLI
options.

## Machine-readable verification

The JUnit XML was parsed as data rather than read from the console summary.

| Tests | Passed | Failures | Errors | Skipped | XML time |
|---:|---:|---:|---:|---:|---:|
| 52 | 52 | 0 | 0 | 0 | 2.028 s |

Evidence file:
`.verification/session2-results-draft/9f9425f/pytest.xml`, SHA-256
`a8f2adbc235ede913d2bda122cef086d79a3fd9f4a7be233ec5306573ee74073`.

Coverage XML was also parsed mechanically. The threshold applies to line
coverage; branch instrumentation is retained and reported independently.

| Production module | Lines | Branches |
|---|---:|---:|
| `theory_oracle_experiment.py` | 94.07% | 76.67% |
| `theory_oracles.py` | 89.06% | 70.28% |
| Combined lane | 90.97% (846/930) | 72.19% (218/302) |

Both new modules clear the required 80% line threshold. They are new at the
contract-freeze baseline, so there is no preexisting touched-module coverage
to regress. The scoped XML is
`.verification/session2-results-draft/9f9425f/coverage-lane.xml`, SHA-256
`8791a332909586a7aaa6528bde0b26698271d7ab2e141ee8f4e56177fbc92631`.
The branch percentages are not represented as meeting an 80% threshold.

## Launcher reproduction and artifacts

The sanitized launcher completed with exit code zero in 0.525346 seconds and
reported `status=pass`, five metrics, and `figures=not_exposed`. Its finalized
run is:

`.verification/session2-results-draft/9f9425f/launcher-sanitized/artifacts/theory_oracle/a80d4ddb5d6d33b9105fd192650bb5e869a2e9ca98e287dd867db790c98c1d94-20260809`

The manifest binds the clean source revision `9f9425f`, the Theory digest, the
fixture digest and application ID, resolved configuration, platform and
dependency versions, and named RNG streams. It finalizes exactly these nine
files:

- `config.json`
- `manifest.json`
- `metrics.json`
- `arrays.npz`
- `diagnostics.npz`
- `exact_numerators.json`
- `exact_denominators.json`
- `theorem_assumption_matrix.json`
- `literal_commuting_diagrams.json`

The exact files contain 41 rational arrays, four formal-log sums, and a
five-metric reconstruction layout. The theorem-assumption artifact contains
10 typed records. The manifest SHA-256 is
`8d8b9da847d7e09d93d4e845b317d6ba4a74bc86f22ef38122ec2671946fb3bb`;
the metric-file SHA-256 is
`8d8efca46866e5c549a18e541db7956c6b49bbb1c386f73be014e9ae88d59c1e`.

A fresh no-argument profile at commit `cd5740b` used Python's standard-library
`subprocess` and `time.perf_counter`, plus `ctypes` access to Windows
`GetProcessMemoryInfo`. It completed in 0.535613 seconds with a peak working
set of 62,509,056 bytes (59.613 MiB), measured over 190 samples. This is a
process peak-working-set measurement, not a claim about asymptotic memory.

The machine-readable record is
`.verification/session2-results-draft/9f9425f/launcher-profile-latest.json`,
SHA-256
`c8953e884d827eeff0964fa07d575d312ae9fe2cf543a57a5d6e0b0288c24a5f`.
It records the exact two-element command, absolute working directory,
`PYTHONPATH` override, interpreter, exit code, elapsed seconds, peak bytes,
sample count, launcher stdout and stderr, parsed launcher and figure statuses,
metric count, manifest completeness, measurement method, and manifest Git
commit. PowerShell reparsing confirmed exit code zero, empty stderr,
`status=pass`, `figures=not_exposed`, five metrics, a complete manifest, and
manifest revision `cd5740b774fb8f5f61611900dbc6d55be204fa53`.

The retained ignored probe makes the profile command exact and path safe:

```powershell
$repo = (Resolve-Path '.').Path
& 'C:\Python314\python.exe' `
  (Join-Path $repo '.verification/session2-results-draft/9f9425f/profile_launcher_probe.py')
if ($LASTEXITCODE -ne 0) { throw "profile probe exit code $LASTEXITCODE" }
```

## Metric results

Every metric compares a vector reconstructed from the independent exact
representation with a separate existing NumPy production path. The tolerance
is `1.01e-10` throughout.

| Metric | Value | Status |
|---|---:|---|
| `elbo_oracle_residual` | `3.3306690738754696e-16` | pass |
| `fisher_defect_oracle_residual` | `0` | pass |
| `marked_event_associativity_residual` | `1.1102230246251565e-16` | pass |
| `hoeffding_oracle_residual` | `0` | pass |
| `gaussian_linear_algebra_oracle_residual` | `2.220446049250313e-16` | pass |

The saved metric records state
`assessment_scope="implementation_check"`,
`theorem_status="ESTABLISHED"`,
`verification_state="EVIDENCE_VERIFIED"`, and
`claim_origin="PROJECT_NOVEL"`. Here `PROJECT_NOVEL` describes the oracle
packet and comparison protocol, not the origin of the standard identities.

## Independent oracles and mutation controls

The oracle is not a float re-expression of the production computation. It
uses immutable `Fraction` containers and canonical formal-log sums; the
experiment serializes numerator and denominator data independently and tests
reconstruction from those files. Corrupting one saved Schur numerator changes
the reconstructed residual beyond tolerance, so an arrays-only tautology
cannot satisfy the check.

Pinned exact witnesses include:

- evidence mass `1/2`, a structurally zero formal-log ELBO gap, and a separate
  extended-real branch for `q>0, p=0` that never evaluates `inf-inf`;
- Fisher coarse mass `(1/2, 1/2)` with exact Fisher defect equal to the
  joint-weighted conditional covariance; transposed orientation and
  unweighted conditional-score mutations are rejected or distinguished;
- marked-event direct and staged coarse masses `(101/315, 214/315)` with
  exact joint equality; reversed kernel composition, omitted source mass, and
  beta-only averaging produce different results;
- exact full Hoeffding/Mobius reconstruction including the empty component,
  with a nonzero three-way residual under pairwise truncation and a separate
  nonuniform product-reference control;
- exact inverse congruence and transformed-prolongator commutation, Galerkin
  restriction distinct from Schur marginalization, and Schur result
  `[[11/3,-1/3],[-1/3,5/3]]`;
- the frozen two-scale literal square and a lane-private nonidentity commuting
  positive control, paired with a noncommuting negative control.

Malformed discriminator, backend, compute dtype, numerical dtype, figure
request, and Schur index packets are rejected before RNG construction,
provenance collection, or artifact creation. Schur checks cover nonintegral,
duplicate, overlapping, out-of-range, and incomplete partitions. Returned
metric and diagnostic mappings are immutable, their arrays are read-only, and
a complete run cannot be overwritten.

Figures are intentionally not exposed in this lane. `render_figures=True`
fails during validation, so there is no renderer-failure isolation obligation
or figure artifact to claim.

## Deterministic replay

Two runs used seed 20260809 and identical semantic configuration but distinct
output roots. Metric values matched exactly. These seven semantic artifacts
were byte-identical:

| Artifact | SHA-256 in both roots |
|---|---|
| `metrics.json` | `8d8efca46866e5c549a18e541db7956c6b49bbb1c386f73be014e9ae88d59c1e` |
| `arrays.npz` | `3a7f5ce386983138710b404fa49db5896075f4f2efc55f94f0964639f0e0e971` |
| `diagnostics.npz` | `38b6e3c3dd58e54cdf084f332eaac3ef4cf6710909267d1c5c2ea9eea39d9505` |
| `exact_numerators.json` | `e470de17a57d0770f5d67a32027385841129bb8771f28255df7b99e9515de1cd` |
| `exact_denominators.json` | `1be11f1f55b15e42ceb8c9c56985dae731d51e946c2c870541a536a288af690c` |
| `theorem_assumption_matrix.json` | `2e55ffbe4aacfc39c063382a19111cb3e81b609d173a2d6b25751669a26b2595` |
| `literal_commuting_diagrams.json` | `8cc8502cfb8eb5fd9c086b613de6be24f603b75d38863708b814cffd3a1f11d5` |

`config.json` and `manifest.json` are correctly excluded from byte equality
because each records its distinct output root and resulting configuration
hash.

The replay is recorded as machine-readable JSON at
`.verification/session2-results-draft/9f9425f/deterministic-replay-latest.json`,
SHA-256
`68ca11295805804c0cbe05f4e353a8b3ae98434379e63494fb0fa35cf2b3f5c0`.
The record contains both absolute run directories, both complete hash maps,
all five metric-equality booleans, the seed, interpreter, semantic inventory,
and probe command. It was generated with:

```powershell
$repo = (Resolve-Path '.').Path
& 'C:\Python314\python.exe' `
  (Join-Path $repo '.verification/session2-results-draft/9f9425f/deterministic_replay_probe.py')
if ($LASTEXITCODE -ne 0) { throw "replay probe exit code $LASTEXITCODE" }
```

## Claim, evidence, and falsifier table

Verification and falsification run in opposite, explicitly separated
directions. A derivation or proof verifies the precisely stated conditional
mathematical claim. A failing test or residual refutes only implementation
conformance unless it also supplies a premise-satisfying, in-domain
counterexample to that exact mathematical claim. Missing premises yield
`INCONCLUSIVE`, not a refutation.

| Claim | `theorem_status` | `verification_state` | `claim_origin` | Evidence type | Failure or refutation condition |
|---|---|---|---|---|---|
| Finite evidence/ELBO decomposition, including its extended-support qualification | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Exact derivation plus Fraction/formal-log witness | Implementation failure: a nonzero canonical finite residual, a finite singular-branch result, or construction of `-inf+inf`. Mathematical refutation: a finite premise-satisfying `(p,q)` for which the stated extended identity is false. |
| Fixed-channel finite Fisher-defect algebra | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Exact derivation and joint-weighted rational witness | Implementation failure: the defect differs from conditional covariance or accepts a transposed/nonnormalized channel. Mathematical refutation: a normalized fixed-channel finite witness satisfying the score premises but violating the matrix identity. |
| Marked-event direct/staged pushforward | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Finite-sum derivation and exact asymmetric witness | Implementation failure: direct/staged joints differ or agreement requires dropped source mass/reversed composition. Mathematical refutation: normalized finite kernels and a marked joint law satisfying the orientation premises but violating associativity. |
| Full product-reference Hoeffding/Mobius reconstruction | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Mobius derivation and exact three-way witness | Implementation failure: a nonzero full residual, missing empty component, or missing triple residual under order-two truncation. Mathematical refutation: a finite normalized product-reference witness satisfying the projector definition but violating reconstruction. |
| Inverse congruence, Galerkin restriction, and algebraic Schur complement as distinct operations | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Exact matrix derivations and rational literals | Implementation failure: disagreement with the respective exact matrix formula or collapse of the two reductions. Mathematical refutation: matrices satisfying each operation's invertibility and typing premises but violating its stated identity. |
| The project comparison lab reproduces all five exact-oracle vectors at revision `9f9425f` | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `PROJECT_NOVEL` | JUnit, branch-aware coverage, exact serialized reconstruction, and reproduced output | This is an implementation claim: a residual above tolerance, undetected exact-JSON corruption, changed semantic replay hash, or incomplete manifest refutes conformance at the bound revision. |
| The frozen two-scale application satisfies all premises needed for the application theorem | `HYPOTHESIS` | `INCONCLUSIVE` | `APPLICATION_SPECIFIC` | Exact literal Jacobian/square plus review of missing witnesses | Verification requires proofs of every named premise. A supplied exact witness that violates one precise premise refutes only that application-premise claim; absent witnesses remain inconclusive. |
| Continuum, infinite-volume, universality, nonlinear-attraction, or physical-time conclusions | `OPEN` | `INCONCLUSIVE` | `PROJECT_NOVEL` | No eligible evidence in this finite lane | These labels are not one claim. Each must first be scoped precisely; proof may verify it, while an in-domain premise-satisfying certified counterexample may refute it. Finite residuals do neither. |

## Unresolved assumptions and scope

The external application assessment is `INCONCLUSIVE` because the following
obligations are not closed here:

- prove the declared recognition extraction-after-lift right inverse on its
  stated open domain;
- check exact outside-marginal preservation for each local block update;
- establish recognition absolute continuity and finite KL against the relevant
  posterior before applying a local/global VFE split;
- prove the local-to-collective identity on the same joint law;
- establish equivalence of every product or block-product reference used for
  the application Hoeffding coordinates;
- supply DQM transfer, smooth-family closure, parameter independence,
  square-integrability, and almost-sure score-version conditions before using
  the statistical Fisher interpretation;
- supply symmetry, positive definiteness, and a proper nondegenerate Gaussian
  law before interpreting the algebraic Schur complement as a marginal
  precision.

The serialized frozen fixture therefore retains
`recognition_right_inverse_state="NOT_CHECKED"` and its internal queued
`verification_state="CANDIDATE"`. That artifact state is not presented as a
closure result; this completed review records application applicability as
`INCONCLUSIVE`.

No finite result here establishes a continuum or nondominated theory,
infinite-volume or two-index limit, universality, a fixed point or attracting
ray, canonical pullback geometry, operational base holonomy, intrinsic scale,
learned-agent behavior, or physical time.

## Integration requests and final closure

No blocking shared-interface change is requested. Serial integration may add
package exports, a launcher registry entry, consolidated README/results links,
and any saved-artifact figure integration. Those shared paths were deliberately
not edited by Session 2. The oracle remains CPU-only and figures remain
unexposed unless the integration owner approves a later contract change.

The exact lane allowlist audit is:

```powershell
$base = 'b80df01f239c2f9a18842f6887cdeca67dff508f'
$allowed = @(
  'src/multiagent_elbo/finite/theory_oracles.py',
  'src/multiagent_elbo/finite/theory_oracle_experiment.py',
  'run_theory_oracle_lab.py',
  'tests/test_theory_oracles.py',
  'tests/test_theory_oracle_experiment.py',
  'docs/results/2026-08-09-theory-oracle-results.md',
  'docs/verification/reviews/2026-08-09-theory-oracle-review.md'
)
$changed = @(git diff --name-only "$base...HEAD")
$unexpected = @($changed | Where-Object { $_ -notin $allowed })
$missing = @($allowed | Where-Object { $_ -notin $changed })
if ($unexpected.Count -ne 0 -or $missing.Count -ne 0) {
  throw "allowlist mismatch: unexpected=$unexpected missing=$missing"
}
$changed | Sort-Object
```

This document is written after the evidence run, so the evidence above is
revision-bound to clean source/review SHA `9f9425f`, not to the subsequent
results-document commit. Before lane publication, the coordinator must start a
fresh ignored verification ledger at the final tracked SHA, rerun the required
focused JUnit, scoped coverage, launcher reproduction, determinism, and
allowlist checks, record one claim per check with eligible evidence, validate
the ledger, and keep `.verification/**` uncommitted. Any post-`9f9425f` source,
configuration, dependency, fixture, or mathematical-convention change also
requires affected evidence to be reproduced.
