# Independent foundation reviews

## Scope

This record summarizes independent, read-only reviews of the fixed Task 4
commits and the subsequent fixed-commit re-reviews. Reviewers inspected source,
tests, and exact-commit archives; reproduced adversarial probes; and separated
software correctness from analytic-theory status. Agreement among reviewers is
supporting judgment only. Current JUnit and reproduced run artifacts provide the
mechanical evidence used by the verification ledger.

## Figure, toggle, and launcher integration

Initial range: `dbbeb10..e4cbf97`

The review confirmed behaviorally independent `collect_diagnostics` and
`render_figures` paths, numerical finalization before rendering, byte-identical
saved-input replays, source-layout bootstrapping without an editable install,
local Matplotlib styling, Okabe-Ito encodings, and explicit `n=1 exact fixture`
semantics.

It found these actionable defects:

1. PNG and PDF were moved separately without rollback, so an injected failure
   on the second final replace left a stray PNG.
2. `output_dir` could equal or sit below `run_dir`, allowing figure replay to
   mutate an immutable numerical bundle.
3. `bbox_inches="tight"` changed the exported width from the declared 3.5
   inches.

Commit `23cb9b2` added tracked rollback of all published image paths, resolved
path-containment guards to both public figure APIs, and exact-size exports. The
independent re-review reproduced an injected second-replace failure and found
no remaining image, a failed manifest, and an unchanged valid preexisting
bundle. Equal/nested paths caused no numerical mutation; a Windows junction
resolving into the run was also rejected. Measured widths were 1050 pixels at
300 DPI and 252 PDF points. Re-review verdict: no Critical or Important issues;
one minor observation was that the mechanically successful junction probe is
not a portable dynamic regression because link creation is environment
dependent. Ready: yes.

## Gaussian realization and numerical boundaries

Initial commit: `52ace1b`

Independent symbolic/exact-arithmetic review recomputed:

- Galerkin precision `[[8,-5],[-5,8]]`;
- scalar Schur precision `[[39/11,-20/11],[-20/11,63/11]]`;
- the exact matrix-valued Schur witness and asymmetric manufactured block;
- precision and Laplacian energies `149/5` and `34/5`;
- determinants `10802/25` and `5401/450`;
- the generalized characteristic polynomial and radical roots;
- both ordinary-spectrum radical oracles;
- the transformed prolongator and both sides of the coarse commuting square.

The initial review found:

1. raw determinant underflow/overflow and an exact condition-ceiling comparison
   rejected valid positive-orientation frames, including many frames emitted by
   the module's own generator;
2. a renderer could return an unbacked `complete` or `failed` status;
3. the commuting square was exercised by a unit test but was not a first-class,
   independently replayable experiment metric;
4. retain-all Schur output ignored the caller's requested vertex order.

Commit `523274e` changed orientation validation to `slogdet`, admitted only the
configured roundoff allowance at the condition boundary, verified on-disk
figure manifests and PNG/PDF SHA-256 identities, pinned and persisted `T_c`,
literal `S'`, and both coarse operators, added
`GAU-01_commuting_square_residual`, and honored requested retain-all order.

The fixed-commit re-review ran 800 generated-frame round trips with zero
rejections, exercised full transforms at uniform scales `1e-100` and `1e100`,
and confirmed that materially over-bound frames still reject. Backed
complete/failed manifests passed; unbacked and corrupt-hash controls became
recorded failures without invalidating numerical results. The independently
computed commuting-square residual was `5.55e-17`, and the retain-all
permutation error was exactly zero. Exact-tree focused JUnit: 74 tests, zero
failures, errors, or skips. Re-review verdict: no Critical, Important, or Minor
issues. Ready: yes.

## Earlier finite-core reviews

The finite foundation had already undergone independent code and mathematical
reviews before Task 4. Those reviews checked runtime category guards, structured
extended-real KL behavior, non-leading and multi-axis block updates, centered
Fisher scores, nonuniform stochastic conditional weights, distinct interaction
norms, and coherent finite permutation directions. All Critical and Important
findings were remediated before commit `903027f`. Later integration review
invalidated that commit's broad launcher closure because its two output toggles
were initially inert and its direct source-layout import was masked by pytest;
commit `e4cbf97` supplied the reachable 2-by-2 toggle matrix and sanitized
fresh-checkout launchers. The final ledger therefore binds current revision
`51480cf`, not the superseded Task 3 ledger.

## Attention and categorical-DQM task reviews

Range reviewed before shared Task 8 integration: `b9d6f04..b5ffae7`.

The task-scoped specification and code-quality passes checked the state-conditioned
marked-event law, nested state/node composition, local-frame metamorphics, the
positive categorical family, centered finite differences, DQM remainder evaluation,
Fisher-loss analysis, experiment artifact publication, and click-to-run launchers.
Three material review findings were resolved before Task 8:

1. A gauge-frame test could have accepted a validation-preserving no-op or an
   alternative transform. Commit `d2153d0` pinned every transformed vector,
   covector, source, and link entry to hand-derived values in addition to the scalar
   invariance assertions.
2. Centered quotients formed an overflowing doubled step for representable extreme
   steps, and an expected subnormal quotient emitted a warning. Commits `09ebd3c`
   and `394083d` hardened the finite-difference boundary and made the expected
   underflow path explicit without changing the mathematical result.
3. The categorical experiment's aggregate status did not initially make a zero
   Fisher-loss trace or flat remainder ladders fail the registered controls. Commit
   `b5ffae7` made the positive-loss predicate and both strict default monotonicity
   checks status-bearing.

The retrospective tracked Task 5 TDD record, including the original staged
RED/GREEN commands and the later `09ebd3c`/`394083d` fix rounds, is
`docs/verification/task-5-categorical-dqm-tdd-evidence.md`. It is explicitly a
tracked copy of an ignored coordination report, not a claim that the intermediate
working trees are Git-reconstructible.

The shared Task 8 integration adds saved-artifact-only attention/DQM figures,
package exports, and sanitized launcher coverage. Its implementation self-review and
machine evidence are recorded in the attention/DQM results document. Any later source
fix requires refreshed JUnit/run evidence and final-revision ledger rebinding.

## Final whole-branch review before the consolidated fix wave

The broad reviewer found no Critical or Important source, mathematics, or test
defect. The only findings were two Minors: incorrect attention final-state labels
plus colliding DQM log-axis labels in the new figures, and the absence of a tracked
Task 5 TDD process-evidence copy. The consolidated fix wave corrected the state
labels and log ticks, made the Task 5 evidence durable, and then moved panel label
`C` clear of every visible y-axis tick after the first scoped visual check exposed
one residual collision. The final scoped re-review at `cc863e4` reported no
Critical, Important, or Minor finding and approved the source for final machine
evidence. The subsequent post-fix audit and evidence refresh are recorded in
the final-revision disposition below.

## Residual limitations

- The current Windows account cannot create symbolic links for the two dynamic
  regressions: artifact symlink rejection and figure-publication symlink escape.
  Both JUnit cases remain skipped, so neither dynamic branch executed. Hard-link
  tests execute, and reparse/junction ownership logic retains static and
  adversarial evidence where applicable.
- Crash recovery and concurrent/distributed writers are outside the current
  single-owner `RunStore` contract.
- The categorical DQM remainder ladder is numerical corroboration of this exact
  implementation; the finite-support Taylor derivation, not the decreasing plot,
  supplies the analytic DQM argument for the declared positive family.
- The concrete categorical kernel records a declared-fixed,
  parameter-independent scope. A single kernel object does not mechanically prove
  independence across an arbitrary parameter family.
- These reviews establish readiness of the declared implementation scope. They
  do not establish universal mathematical claims, Gaussian family membership
  for external data, or RG universality.

## Six-session buildout review index and integration disposition

The six implementation lanes carry durable review records written before serial
integration:

- [Session 1 multi-agent network](reviews/2026-08-09-multiagent-network-review.md)
- [Session 2 exact theory oracles](reviews/2026-08-09-theory-oracle-review.md)
- [Session 3 finite counterexamples](reviews/2026-08-09-finite-counterexample-review.md)
- [Session 4 information histories](reviews/2026-08-09-information-history-review.md)
- [Session 5 gauge holonomy](reviews/2026-08-09-gauge-holonomy-review.md)
- [Session 6 scale, RG, and CUDA](reviews/2026-08-09-scale-rg-cuda-review.md)

The integration coordinator independently reproduced each lane's full CPU suite
at its committed head, verified clean allowlisted diffs, and then ran a fresh
full suite after every merge in the prescribed order. Cross-lane launcher tests
exposed and fixed two Session 6 launcher integration defects. The Session 6
merge also exposed a Windows LF/CRLF preregistration-digest defect; its focused
regression and full merged suite are green. Saved-artifact replay was exercised
against actual finalized outputs from all seven new laboratories.

Final-revision disposition: **CPU and saved-artifact replay scope publishable;
CUDA closure inconclusive.** The final CPU audit records 700 collected tests,
698 passed, zero failures, zero errors, and two expected Windows
privilege-dependent skips. The pinned worker-CPU check passed 1 of 1. Aggregate
coverage is 91.20% line and 74.48% branch; every production module remains at
or above 80% line coverage, with `cuda_backend.py` the minimum at 80.56%.

All 11/11 laboratories reproduced from clean bundle roots. Two
independent replay roots each contain 33 files, and corresponding files are
byte-identical. The actual post-fix code and mathematical re-reviews each
reported zero Critical, Important, or Minor findings. The experiment audit
reported zero Critical or Important findings and explicitly noted the two
expected Windows privilege skips.

This documentation commit necessarily changes the Git revision. The exact
final artifact identity is therefore supplied authoritatively by the validated
live `.verification/ledger.json` after the controller's final evidence refresh
validation, rather than hardcoded here. That ledger will bind the CPU, replay,
and claim-boundary checks as `EVIDENCE_VERIFIED` and CUDA closure as
`INCONCLUSIVE`; this review does not claim that the post-closeout ledger binding
has already occurred.

The only remaining scientific execution gates are explicit operator opt-in, a
current validated idle-GPU gate, the pinned Python 3.12 float64 CUDA sentinel,
and the separately gated confirmatory sweep. Until those CUDA obligations are
satisfied, unqualified full-program closure is not supported.
