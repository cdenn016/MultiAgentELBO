# Six-Session Theory/Simulation Integration Results

Date: 2026-08-10

Branch: `codex/theory-simulation-integration-20260809`

Contract freeze: `b80df01f239c2f9a18842f6887cdeca67dff508f`

Scientific and integration source checkpoint: `d5a0514`

## Outcome

All six session branches were clean, committed, confined to their frozen
allowlists, and independently green before serial integration. They were merged
in the plan's exact order in an isolated worktree. The live `main` checkout and
its uncommitted files were not modified.

The merged CPU source checkpoint passes 683 tests with two Windows
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

The Session 6 merge initially exposed three integration-only failures because
Git's Windows checkout conversion changed the byte representation of a frozen
text preregistration from LF to CRLF. The scientific content and Git tree were
unchanged. Checkpoint `0255c1c` added a regression and canonicalizes text line
endings only for that preregistration digest; executable and environment-lock
hashes remain raw-byte hashes.

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

1. Run and validate the final-revision CPU JUnit and coverage records after the
   documentation checkpoint.
2. Obtain a final-SHA independent review or record any unresolved disagreement
   as `INCONCLUSIVE`.
3. Only after explicit operator opt-in and a current validated idle-GPU record,
   run the pinned Python 3.12 float64 CUDA sentinel. The heavy confirmatory sweep
   remains separately gated.
4. Rebind the final verification ledger to the resulting artifact revision.

Until those gates close, the integration branch is CPU-green and ready for
review, but it is not eligible for an unqualified final-closure claim.
