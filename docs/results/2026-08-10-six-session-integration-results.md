# Six-Session Theory/Simulation Integration Results

Date: 2026-08-10

Branch: `codex/theory-simulation-integration-20260809`

Contract freeze: `b80df01f239c2f9a18842f6887cdeca67dff508f`

Final verified pre-remediation source checkpoint: `ddf2a41`

## Outcome

All six session branches were clean, committed, confined to their frozen
allowlists, and independently green before serial integration. They were merged
in the plan's exact order in an isolated worktree. The live `main` checkout and
its uncommitted files were not modified.

The final pre-remediation source checkpoint passes 696 tests with two Windows
symlink-privilege skips. All seven new launchers import without side effects,
run from a sanitized working directory without an editable install, and publish
complete manifests. All seven new figures replay from finalized saved artifacts
without recomputing an experiment.

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
| Final SHA | Documentation/evidence reconciliation through `ddf2a41` | `ddf2a41` | 696 passed, 2 skipped |

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

## Completed final-SHA verification at `ddf2a41`

Final CPU, worker-CPU, experiment reproduction, saved-artifact replay, and
independent final-SHA review were completed at `ddf2a41`; they are not pending
work at that revision. The validated ledger was bound to
`git:ddf2a41d663ee92b01c8ff5190836ade0945d264:sha256:6a5a05003944b86f34a2dc55174c6f44b8043709481c8f75a55341cac909949b`
and contains these actual claim identities:

- `FINAL-CODE-CPU`: `EVIDENCE_VERIFIED` from `coordinator-mechanical` and
  `independent-code-review`, with the 698-test JUnit record (696 passed, zero
  failed, zero errors, two skipped), worker-CPU JUnit, and coverage evidence.
- `FINAL-EXPERIMENT-REPLAY`: `EVIDENCE_VERIFIED` from
  `coordinator-reproducer` and `independent-experiment-review`, with reproduced
  bundles and two saved-artifact replay records.
- `FINAL-CLAIM-BOUNDARIES`: `EVIDENCE_VERIFIED` from
  `coordinator-source-audit` and `independent-mathematical-review`.
- `FINAL-CUDA-CLOSURE`: `INCONCLUSIVE` from `coordinator-gate-audit` and
  `independent-experiment-review`; the ledger retains explicit operator opt-in,
  idle-GPU gate, float64 sentinel, and confirmatory-job obligations.

The tracked remediation documented below changes the artifact revision, so the
`ddf2a41` evidence remains historical and cannot close the remediation commit.
Its final-SHA CPU/replay evidence, independent review, and ledger binding must
be refreshed after the remediation is committed. No new ledger claim is
asserted by this document update.

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

1. Refresh the final-revision CPU JUnit, coverage, worker-CPU, experiment
   reproduction, and saved-artifact replay records after this remediation.
2. Refresh the independent final-SHA reviews and rebind the verification ledger
   to the remediation commit; the completed `ddf2a41` review and ledger binding
   are revision-specific evidence, not missing historical work.
3. Only after explicit operator opt-in and a current validated idle-GPU record,
   run the pinned Python 3.12 float64 CUDA sentinel. The heavy confirmatory sweep
   remains separately gated.

Until those gates close, `ddf2a41` remains the last fully bound CPU-green
checkpoint; the remediation revision has focused test evidence only and is not
eligible for an unqualified final-closure claim.
