# Six-Session Theory/Simulation Integration Results

Date: 2026-08-10

Branch: `codex/theory-simulation-integration-20260809`

Contract freeze: `b80df01f239c2f9a18842f6887cdeca67dff508f`

Authoritative final artifact identity: the post-closeout validated live
`.verification/ledger.json`

## Current scientific-contract supersession

The integration results below remain the historical record for their stated
revisions. For current behavior at scientific code revision
`f4966db1127ad952e3f3f1ce118b518ca58b5811`, see
[Shared Scientific Contract Remediation Results](2026-08-10-shared-scientific-contract-remediation-results.md).
That revision-bound record supersedes only the current interpretation of the
shared relabeling, SPD-conditioning, Session-3 producer-state, and aggregate
status contracts. It does not rewrite this document's historical bytes, test
totals, review findings, or ledger disposition.

## Outcome

All six session branches were clean, committed, confined to their frozen
allowlists, and independently green before serial integration. They were merged
in the plan's exact order in an isolated worktree. The live `main` checkout and
its uncommitted files were not modified.

The final-revision CPU record contains 700 collected tests: 698 passed, zero
failed, zero errored, and two expected Windows privilege-dependent symlink
tests skipped. The separately pinned worker-CPU check passed 1 of 1. Aggregate
coverage is 91.20% line and 74.48% branch; every production module remains at
or above 80% line coverage, with `cuda_backend.py` the minimum at 80.56%.

This is not full program closure. The Gaussian fixed-ray CUDA parity claim and
confirmatory sweep remain `INCONCLUSIVE`: operator opt-in, a current idle-GPU
gate, and the frozen float64 sentinel prerequisites were absent. No heavy CUDA
job was run.

## Serial integration evidence

| Step | Integrated source | Merge/checkpoint | Fresh CPU result |
|---|---|---|---:|
| Baseline | Contract freeze | `b80df01` | 438 passed, 2 skipped |
| 1 | Session 2 exact theory oracles (`9f4922f`) | `2e1a1c8` | 490 passed, 2 skipped |
| 2 | Session 1 multi-agent application (`31a20e7`) | `4c58f7d` | 513 passed, 2 skipped |
| 3 | Session 3 finite counterexamples (`3d6e28d`) | `b2e14d4` | 539 passed, 2 skipped |
| 4 | Session 4 information histories (`4cb8375`) | `a70a2d6` | 562 passed, 2 skipped |
| 5 | Session 5 gauge holonomy (`75c32c5`) | `f963597` | 599 passed, 2 skipped |
| 6-7 | Session 6 scale/CUDA infrastructure and CPU Gaussian pilot (`198febf`) | `977688b`, then `0255c1c` | 661 passed, 2 skipped |
| 8 | Shared exports and launcher matrix | `f483a33` | 682 passed, 2 skipped |
| 9 | Saved-artifact renderers | `d5a0514` | 683 passed, 2 skipped |
| 10 | Final review remediation | `e4a7244` | 686 passed, 2 skipped |
| Reconcile | Current `origin/main` plus complete refreshed Session 2 tip (`aa3fa6b`) | `8491ad9` | 696 passed, 2 skipped |
| Pre-remediation evidence checkpoint | Documentation/evidence reconciliation through `ddf2a41` | `ddf2a41` | 696 passed, 2 skipped |

The reconciliation absorbed Session 5's immutable two-cell boundary repair and
the complete reviewed Session 2 canonical-rational contract repair. Both
changes stayed within their frozen lane allowlists. The only merge conflict was
between two independently implemented preregistration line-ending helpers; the
resolution retained Git-LF canonicalization, the stricter lone-CR handling, and
both regression tests. Focused Gaussian/holonomy verification passed 27 tests
before the broad checkpoint.

## Final-review remediation

Independent final review found that the first split-archive renderer accepted
tampered manifest keys naming an absolute or parent-relative NPZ path. The
renderer now applies the numerical artifact store's portable-name, resolved
ownership, regular-file, reparse-point, and single-hard-link checks to the
manifest, metrics, and every numeric archive before reading. New traversal,
absolute-path, and hard-link regressions pass; the existing shared ownership
tests retain the symlink/reparse coverage.

The mathematical review also found that the initial registry supplement used
`EVIDENCE_VERIFIED` as if it were an integration-wide state. The registry now
reports lane outcomes descriptively and reserves integration-wide state for the
validated live final-SHA ledger. The focused code and mathematical re-reviews
both pass after these corrections.

The Session 6 merge initially exposed three integration-only failures because
Git's Windows checkout conversion changed the byte representation of a frozen
text preregistration from LF to CRLF. The scientific content and Git tree were
unchanged. Checkpoint `0255c1c` added a regression and canonicalizes text line
endings only for that preregistration digest; executable and environment-lock
hashes remain raw-byte hashes.

## Final-revision evidence and audit disposition

The post-fix evidence refresh completed every scoped CPU, worker-CPU,
reproduction, replay, and independent-review check. All 11/11 laboratory
bundles reproduced from clean roots. Two independent replay roots each contain
33 files, and corresponding files are byte-identical. The post-fix code and
mathematical re-reviews each reported zero Critical, Important, or Minor
findings. The experiment audit reported zero Critical or Important findings and
explicitly retained the two expected Windows privilege skips as limitations.

Because this closeout text changes the Git revision, it does not hardcode a
purported final commit or ledger digest. After the controller performs the
final evidence refresh validation, the validated live
`.verification/ledger.json` is the authoritative source for the exact artifact
identity. That ledger will bind the CPU, replay, and claim-boundary checks as
`EVIDENCE_VERIFIED` and CUDA closure as `INCONCLUSIVE`. This document neither
edits the ledger nor claims that the post-closeout binding has already occurred.

## Laboratory records

- [Multi-agent network](2026-08-09-multiagent-network-results.md)
- [Independent theory oracles](2026-08-09-theory-oracle-results.md)
- [Finite counterexamples](2026-08-09-finite-counterexample-results.md)
- [Information histories](2026-08-09-information-history-results.md)
- [Gauge holonomy](2026-08-09-gauge-holonomy-results.md)
- [Exact scale cocycle](2026-08-09-scale-cocycle-results.md)
- [Gaussian fixed-ray CPU pilot](2026-08-09-gaussian-fixed-ray-results.md)

The exact finite, attention, categorical-DQM, and Gaussian foundation results
remain recorded separately and also pass in the merged suite.

## Saved-artifact replay

The shared renderer now accepts every complete numeric NPZ artifact listed by a
finalized manifest. A conventional `arrays.npz` keeps unqualified array names;
named archives are loaded under archive-qualified names to avoid collisions.
This permits pure replay of experiments that intentionally split arrays by
semantic role.

Actual finalized CPU bundles were replayed successfully for:

- `multiagent_network`
- `theory_oracles`
- `finite_counterexamples`
- `information_history`
- `gauge_holonomy`
- `scale_cocycle`
- `gaussian_fixed_ray`

Each replay produced a PDF and 300-DPI PNG plus a complete figure manifest. The
Gaussian caption explicitly records that CUDA parity is inconclusive and the
heavy sweep was not run.

## Remaining gates

1. Obtain explicit operator opt-in and a current validated idle-GPU gate, then
   run the pinned Python 3.12 float64 CUDA sentinel. The confirmatory sweep
   remains separately gated.

Publication disposition after the final evidence refresh and controller ledger
validation: the declared CPU and saved-artifact replay scope is publishable.
CUDA parity and the confirmatory sweep remain `INCONCLUSIVE`, so unqualified
full-program closure is not supported.
