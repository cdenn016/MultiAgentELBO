# Shared Scientific Contract Remediation Results

**Date:** 2026-08-10

**Scientific code revision:** `f4966db1127ad952e3f3f1ce118b518ca58b5811`

**Documentation revision:** committed separately from the scientific code
revision; the scoped Task-7 report records the resulting documentation commit.

**Interpreter:** `C:\Python314\python.exe` (CPython 3.14.4, CPU)

## Scope and revision binding

This record binds the remediated shared permutation, spectral-conditioning, and
Session-3 producer contracts to code revision `f4966db`. It reports two fresh
clean-root reproductions of the click-to-run Session-3 laboratory, together
with current Task-6 JUnit and coverage artifacts produced at that same committed
code revision. No source or test file changed between that evidence and the two
reproductions.

This is finite CPU implementation and experiment evidence. It makes no
continuum, CUDA, security, provenance-hardening, registry, or general-theory
claim. Verification-state promotion remains external to the producer and is
not performed in this document.

## Reproduction method and roots

Each run loaded `run_finite_counterexample_lab.py`, changed only the in-memory
`OUTPUT["root"]` value, and called the launcher's zero-argument `main()`.
Neither launcher source nor any editable launcher dictionary on disk was
changed. The clean ignored output roots and resulting bundle identities were:

| Replay | Output root | Configuration hash | Aggregate status |
|---|---|---|---:|
| A | `.pytest-tmp/task7-replay-a` | `4754376d738b8fc45a369100ca1bce9d2cb461b66832a0ab5bb99821456a2e95` | `inconclusive` |
| B | `.pytest-tmp/task7-replay-b` | `103bde2433eddb53d7cec0de58d980acf824d939c88daf4d970a37424cfac623` | `inconclusive` |

The full run directories are the corresponding
`finite_counterexample/<configuration-hash>-20260809` children of those roots.
The configuration hashes differ because the absolute output-root string is a
resolved configuration input. Both manifests bind the scientific code revision
to `f4966db`, record a clean Git status, and otherwise carry the same requested
scientific and numerical configuration.

## Deterministic semantic comparison

The five JSON artifacts were parsed and compared as structured values. Every
comparison was equal, and the serialized bytes were also identical. The NPZ
archives were loaded with `allow_pickle=False`: all 41 array names and values
were exactly equal under `numpy.array_equal`, including all 36 rational
numerator/denominator arrays (18 pairs). The complete NPZ archives were also
byte-identical.

| Semantic artifact | Replay A SHA-256 | Replay B SHA-256 | Result |
|---|---|---|---|
| `metrics.json` | `b4fd3d6514ca1ed14dabe8df5691eb0683ba5205da42f40b07ca95950ab1e71b` | `b4fd3d6514ca1ed14dabe8df5691eb0683ba5205da42f40b07ca95950ab1e71b` | semantic and byte equality |
| `enumeration_bounds.json` | `6919d7f9ea4bc17698fe806c9947157debbfbae03f71e041b2db26a77d64656e` | `6919d7f9ea4bc17698fe806c9947157debbfbae03f71e041b2db26a77d64656e` | semantic and byte equality |
| `candidate_records.json` | `ee3b876d6ca889bcc81be31c19f385c03f21a6b488fd0808cfb33b0f22ea4801` | `ee3b876d6ca889bcc81be31c19f385c03f21a6b488fd0808cfb33b0f22ea4801` | semantic and byte equality |
| `minimal_witnesses.json` | `281c4d1e3d1f49d9fea87a0762656a78d1f7507808220ae1e3f773d9a04eec06` | `281c4d1e3d1f49d9fea87a0762656a78d1f7507808220ae1e3f773d9a04eec06` | semantic and byte equality |
| `stress_matrix.json` | `072be1d4c9f6bc18f9e50ba9563da5ee210ec663a9fb84a91c59c4cf67caf200` | `072be1d4c9f6bc18f9e50ba9563da5ee210ec663a9fb84a91c59c4cf67caf200` | semantic and byte equality |
| `arrays.npz` | `aafa135e901d5425eaaf996c535903a5c0dc59a52ff5cb82ec87667d82f678de` | `aafa135e901d5425eaaf996c535903a5c0dc59a52ff5cb82ec87667d82f678de` | all arrays and bytes equal |

## Catalog and minimal witnesses

The requested catalog bounds remain `max_states=4` and
`max_denominator=8`. The explicitly saved effective exhaustive domain remains
two-state laws and 2-by-2 channels through denominator 4, together with a
three-axis binary action catalog over values in `{-1, 0, 1}`. The reproduced
counts are 7 laws, 49 channels, 6,561 actions, 19,587 candidate records, and 5
globally minimal witnesses.

| Minimal claim | Boundary | Reproduced minimal residual | Witness summary |
|---|---|---:|---|
| `fixed_channel_score_fisher` | assumption boundary | `4/3` | two states, `theta=1/2`, parameter-dependent channel |
| `marked_event_source_mass` | inside catalog | `1/2` | two-state source `(0,1)` with the saved beta and channel |
| `pairwise_truncation` | inside catalog | `1/8` | three binary axes, retained order 2, values `(-1,-1,-1,-1,-1,-1,-1,0)` |
| `single_law_relabeling` | assumption boundary | `0.23104906018664842` | law `(1/3,2/3)` under the two-state swap |
| `support_boundary` | assumption boundary | `1` | `q=(1,0)`, `p=(0,1)` outside absolute-continuity applicability |

All 19,587 candidate records and all five metric records carry producer state
`CANDIDATE`. The 12 `support_boundary` candidates are outside the declared
domain, have unsatisfied assumptions, use classification
`assumption_boundary`, retain state `CANDIDATE`, and explicitly name the
absolute-continuity applicability premise.

## Scientific closure

| Contract | Current result | Evidence boundary |
|---|---:|---|
| Three-cycle relabeling | exact residual `0` | finite typed permutation only; old-to-new cycle `(1,2,0)` maps `(1/5,3/10,1/2)` to the exact expected `(1/2,1/5,3/10)` |
| Correlated SPD control | `fail` | finite SPD membership plus shared spectral reciprocal condition |
| Repeated-small-diagonal SPD control | `pass` | finite SPD membership plus shared spectral reciprocal condition |
| Producer verification state | `CANDIDATE` | ledger promotion is external |

The freshly serialized Session-3 relabeling stress uses the typed two-state
swap on all three action axes; it reports `coherent=true`, measured exact
residual `0`, and stress status `pass`. The separately pinned shared
three-cycle oracle above also has exact residual `0`. These are distinct finite
fixtures and are not conflated.

### Corrected spectral decisions and old-proxy reversals

The correlated control is
`[[1, 1-10^-12], [1-10^-12, 1]]`. With `min_spd_rcond=10^-12`
and zero control tolerance, the shared eigenspectrum assessment records minimum
eigenvalue `9.999778782798785e-13`, maximum eigenvalue
`1.999999999999`, reciprocal condition `4.999889391401893e-13`,
method `symmetric_eigenvalue_ratio`, and decision `fail`. The retired
determinant-volume proxy is approximately `5.0001106110475214e11`, below its
`10^12` cutoff, so it incorrectly returned `pass`: a false acceptance.

The repeated-small-diagonal control is `diag(1, 10^-7, 10^-7)`. With the same
threshold and zero control tolerance, the assessment records minimum
eigenvalue `10^-7`, maximum eigenvalue `1`, reciprocal condition `10^-7`, the
same spectral method, and decision `pass`. The retired determinant-volume
proxy is approximately `1.0000000000000012e14`, above its `10^12` cutoff, so
it incorrectly returned `fail`: a false rejection.

### Requested and effective Session-3 policy

The requested and effective Session-3 policy agree exactly:
`min_spd_rcond=1e-12`, `atol=1e-12`, and `rtol=1e-10`.
`max_frame_condition=1e6` is serialized as not applicable to this stress
assessment.

The published near-singular SPD stress fixture is `diag(1, 10^-100)`. Its
serialized spectral fields are: minimum eigenvalue `1e-100`, maximum
eigenvalue `1`, reciprocal condition `1e-100`, threshold `1e-12`, boundary
tolerance `1.0000000001e-12`, method
`symmetric_eigenvalue_ratio`, positive-definite membership `true`, and decision
`inconclusive` because the reciprocal condition lies within the declared
tolerance band. Consequently the conditioning stress is `inconclusive` and
the aggregate Session-3 status is honestly `inconclusive` under the default
absolute tolerance. Failure still has precedence over inconclusive in the
aggregate contract, but no required default stress fails in these reproduced
bundles.

## Current mechanical evidence

The current ignored Task-6 machine-readable evidence was reused because it was
produced at committed code revision `f4966db`; immediately before the Task-7
documentation edits, `HEAD` was exactly that revision and tracked status was
clean. No focused rerun was needed to bind a changed source or test tree.

| Evidence | Mechanical result | SHA-256 |
|---|---|---|
| `.pytest-tmp/task6-contracts.xml` | 11 tests, 11 passed, 0 failed, 0 errors, 0 skipped | `b764b53f2dcecb205c90bacc4fa07ab1d604ac0140eba72d0c066eab4b802c30` |
| `.pytest-tmp/task6-full.xml` | 756 tests, 754 passed, 0 failed, 0 errors, 2 skipped | `0ada528427bdd5b410f6aa62dbe97349dd052ad804658bc8492342fe6d662995` |
| `.pytest-tmp/task6-coverage.xml` | aggregate 94.24% line and 94.23% branch; `conditioning.py` 86.67% line and 85% branch; `permutations.py` 100% line and branch | `9984bf4abcf63b21296231309be5f5299c3246e56751e20cc2d477e658f3fbcf` |

The two skipped complete-suite tests are the existing Windows
privilege-dependent link cases. No CUDA result is included.

## Supersession boundary

The prior Session-3 artifact bundle and the six-session integration document
remain historical revision-bound records. This document supersedes only their
current scientific-contract interpretation: typed relabel direction is shared,
SPD admission uses the reciprocal eigenspectrum policy, the two retired-proxy
decisions reverse as recorded above, producer states remain `CANDIDATE`, and
the default Session-3 aggregate is `inconclusive` rather than `pass`.

This supersession does not rewrite historical bytes, test totals, review
verdicts, or ledger states and does not claim a continuum, CUDA, security,
provenance-hardening, registry, or general-theory result.
