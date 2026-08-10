# Independent Review: Finite Counterexample Laboratory

**Date:** 2026-08-09

**Branch:** `codex/finite-counterexamples-20260809`

**Contract freeze:** `b80df01f239c2f9a18842f6887cdeca67dff508f`

**Reviewed implementation revision:** `3df4b92db525c612716ecc67fdd3efdf7e6e876d`

**Reviewed result-record revision:** `812725074d3c671dd33c46632e1dd1c7346de67b`

**Verdict:** **APPROVED**

## Scope and ownership

The base-to-result-record diff contains exactly these seven Session-3 allowlisted
paths:

- `docs/results/2026-08-09-finite-counterexample-results.md`
- `docs/verification/reviews/2026-08-09-finite-counterexample-review.md`
- `run_finite_counterexample_lab.py`
- `src/multiagent_elbo/finite/counterexample_experiment.py`
- `src/multiagent_elbo/finite/counterexamples.py`
- `tests/test_counterexample_experiment.py`
- `tests/test_counterexamples.py`

This rereview updates only the lane-unique review path. No frozen shared interface,
package export, `Theory/**` source, CUDA path, or dependency file changed.

## Review history

The initial core commit `f8defb9770a171fa50af6f87abb7bd8d29de2bc4`
was rejected because it lacked action and relabeling enumeration, derived
Hoeffding projection, near-singular rejection, safe outside-domain
classification, structural witness minimization, deep immutable rational
serialization, a target-resolved marked-event joint, and retained-projection
metamorphics. Commit `b48bd840e325570eb993edcef5a2899a94679031`
addressed those findings. Its scoped rereview found one API regression:
`fixed_channel_score_gap` no longer returned a scalar `Fraction`. Commit
`5618d94c93065770d5e8d31634cc5bc1711ff6ee` restored that contract, and the
second scoped rereview approved the core.

The initial experiment commit
`1dc3961` was rejected because its alleged minimal witnesses were hand-picked
rather than obtained from the declared exhaustive catalog and `arrays.npz`
did not contain primitives sufficient for independent recomputation. Commit
`a5f63b3` introduced the exhaustive effective-domain catalog and rational
primitive arrays, but its first rereview found overstated action bounds, an
incorrectly typed/in-domain one-sided relabeling record, a tautological deep
composition case, and missing contract assertions. Commit `2105b12` corrected
those issues. Its rereview found that most numeric-log candidate records still
stored the type label rather than an observed residual. Commit `4b61565`
serialized the actual deterministic residuals, and the final narrow rereview
approved that correction.

The durable result record was committed as `71a6de0`. This independent review
reparsed its named evidence and inspected the current base-to-head code and
tests. It found the artifact-integrity defect described below, which was not
identified in the earlier scoped rereviews.

The original rejection was committed as `db604e6`. Commit `ab74700` then
replaced the singular stress input with exact positive-definite
`diag(1,10^-100)`, serialized its threshold comparison and rejection reason,
and added a literal reconstruction test. The experiment reviewer approved that
scoped fix. Commit `86b4551` refreshed the durable result record and all cited
mechanical evidence at the corrected implementation revision. This rereview
independently parsed that refreshed evidence and resolves the original blocker.

A final whole-lane code review at `b2fa7ee` subsequently found two Important
defects and one Minor defect: accepted low enumeration bounds did not constrain
the executed pinned catalog; the parameter-dependent-channel gap was a bare
formula without saved finite primitives or an independent derivation; and
witness denominator minimization was inert for produced nested rational
values. Commit `3df4b92` addressed all three. Its scoped rereview confirmed the
implementation corrections but withheld merge approval because the durable
result and review documents still described the superseded implementation.
Commit `8127250` refreshed the result record and all evidence. This final
rereview verifies that remediation and updates the remaining stale review
record without erasing any earlier finding trail.

## Current mechanical evidence

The cited focused JUnit XML at
`.verification/session3/task3-final-focused.xml` parses to 26 tests, 0
failures, 0 errors, 0 skips, and 35.591 seconds. The cited full-suite JUnit XML
at `.verification/session3/task3-final-full.xml` parses to 466 tests, 0
failures, 0 errors, 2 skips, and 54.098 seconds. The two skips are the existing
Windows-privilege-dependent link tests.

The cited coverage XML at
`.verification/session3/task3-final-coverage.xml` reports 91.40% line and
78.26% branch coverage for `counterexamples.py`, and 97.77% line and 93.48%
branch coverage for `counterexample_experiment.py`. Both new production modules
exceed the required 80% line threshold.

The final clean launcher manifest binds implementation revision `3df4b92`,
records `git_dirty=false`, CPU/float64 execution, exact-rational arithmetic,
and the canonical configuration hash
`ecb50ab6806a296629778ecbd9965859c4de5b99df406a7a1b408acf3efc9af0`.
The six semantic artifact hashes match the final result record:

- `arrays.npz`: `aafa135e901d5425eaaf996c535903a5c0dc59a52ff5cb82ec87667d82f678de`;
- `candidate_records.json`: `187c7ac65269f0c166c26fa19feb53640230368486135e07a08df7d1861475b8`;
- `enumeration_bounds.json`: `6919d7f9ea4bc17698fe806c9947157debbfbae03f71e041b2db26a77d64656e`;
- `metrics.json`: `4bcc4826e43f8bddbd44dd170ec455c50ac7bd59cff9f852ef08b9504fb4a6d0`;
- `minimal_witnesses.json`: `8cdab56605783b9912071a0830f46657957f0e2c55f8c78e65a46c73c8e85bd4`;
- `stress_matrix.json`: `04ad19a198e3130118dc657acc053e4f6a3be250ed484e333c1d9de194c9c576`.

Fresh independent replay under two output roots produced byte-identical
semantic artifacts after excluding the deliberately root-sensitive
configuration identity.

These files are eligible implementation and finite-experiment evidence for the
corrected tested code revision. They are not mathematical proof. Any subsequent
tracked source or artifact change requires fresh evidence at the new revision.

## Technical assessment

The enumeration record truthfully distinguishes the requested bound (four
states, denominator eight) from the effective exhaustive domains: two-state
laws and 2-by-2 channels through denominator four, plus three binary axes with
ternary integer action values. The saved counts are 7 laws, 49 channels, 6,561
actions, 19,587 candidates, and 5 claim-wise minimal witnesses. No claim over
the larger requested domain is supported.

Candidate minimization uses an explicit structural key before canonical JSON
tie-breaking. Witness mappings and sequences are recursively frozen, exact
fractions serialize as reduced rational strings, and outside-domain or
failed-assumption records are forced to `assumption_boundary`. The primitive
NPZ bundle stores numerator/denominator arrays, permutations, shapes, axis
sizes, and retained order. The focused test reconstructs `Fraction` objects
and independently recomputes all five published metrics through core
primitives rather than reading each metric back as its own oracle.

The launcher has editable dictionaries, no argument parser, and an import-safe
main guard. Incorrect experiment, CUDA, and figure requests are tested to fail
before RNG creation, provenance collection, or `RunStore.create`. The
sanitized subprocess removes inherited `PYTHONPATH`, runs from a temporary
directory without an editable install, and asserts that Torch is absent from
`sys.modules`. The production lane imports neither Torch nor a CUDA backend
and performs no silent fallback. The algorithm is intentionally finite and
bounded but expensive; the action and marked-event catalog loops are the main
CPU/memory scaling risks if effective bounds are increased.

The required controls are otherwise present and correctly scoped:

- a structured extended-real support violation without `inf - inf`;
- an explicit parameter-dependent-channel boundary fixture with saved exact
  `p,p',K,K',r,r'` and score primitives, literal gap `16/15` at `theta=1/4`,
  globally minimal `theta=1/2` gap `4/3`, and endpoint `theta=1` exclusion;
- coherent relabeling invariance and one-sided relabeling with `ln(3)/2`;
- source-mass versus beta-only marked-event pushforward;
- an order-three action with an order-two retained projection residual;
- incompatible channel orientation/order rejection;
- associative three-channel deep composition with exact zero residual;
- coherent retained-space relabeling and an incoherent negative control;
- exact tolerance scaling; and
- singular and near-singular SPD rejection in the core test suite.

## Original blocking finding and resolution

**Original Medium finding -- the published conditioning stress datum was
semantically false.**
The original `stress_matrix.json` published
`"conditioning":{"rejected_near_singular":true,...}`. However,
the original `_rejected_near_singular()` called `validate_full_rank_spd` with
`diag(1,0)`, which is singular, not near-singular. The experiment test merely
asserts the resulting mislabeled Boolean. A separate core test does correctly
reject `diag(1,10^-100)` at the declared exact conditioning boundary, so this
did not show that the validator was broken. It showed that the original durable
stress artifact did not measure what its field said it measured.

At the original reviewed revision, this scientific-artifact integrity failure
blocked approval. The required repair was narrow: make the stress producer
exercise an actually positive-definite near-singular input, add a test that
distinguishes that input from the singular control, reproduce the launcher
bundle/JUnit/coverage at the new revision, and update the result record and
hashes.

**Resolution -- addressed by `ab74700` and rebound by `86b4551`.** The producer
now uses exact `diag(1,10^-100)`. Independent parsing confirms both diagonal
entries and the determinant are strictly positive, the serialized minimum
diagonal matches `10^-100`, the condition score is exactly `10^100`, and
`10^100 > 10^12`. The record preserves `positive_definite=true`,
`rejected=true`, and reason
`near-singular SPD input exceeds the exact conditioning boundary`. The test
reconstructs the serialized matrix as `Fraction` values and reaches that exact
near-singular rejection. The singular control remains separate. Fresh focused
and full JUnit, coverage, launcher provenance, semantic hashes, and two-root
replay all bind the corrected implementation. The original blocker is closed.

No critical security issue or high-priority vulnerability was found in this
offline, CPU-only lane. No residual critical or important implementation issue
was found in the correction or the complete reviewed scope.

## Final code-review findings and resolution

The final whole-lane review initially withheld merge approval at `b2fa7ee`.
The following trail is retained because each item materially changed the final
evidence contract.

**Important -- accepted low bounds did not constrain execution. Resolved.**
The prior experiment always ran the pinned 2-state/denominator-4 catalog, even
when an accepted configuration requested smaller maxima. At `3df4b92`,
`max_states < 2` and `max_denominator < 4` are rejected before `_catalog`,
configuration hashing, RNG, provenance, `RunStore.create`, or artifact effects.
The focused JUnit contains both low-bound parameterizations with every effect
seam replaced by a forbidden callable. Separate exact `(2,4)` and larger
`(5,9)` cases publish the requested/effective distinction and prove that the
effective domain does not exceed the accepted maxima.

**Important -- the parameter-channel gap was a circular bare formula.
Resolved.** The corrected exact fixture defines `p=(1/2,1/2)`, `p'=(0,0)`,
identical rows `K=((1+theta)/2,(1-theta)/2)`, derivative rows
`K'=(1/2,-1/2)`, and derives `r=pK` and `r'=p'K+pK'`. At `theta=1/4`, direct
reconstruction from saved numerator/denominator arrays gives
`r=(5/8,3/8)`, `r'=(1/2,-1/2)`, zero fine score and fixed-channel prediction,
actual coarse score `(4/5,-4/3)`, and literal Fisher-weighted gap `16/15`.
This independent calculation does not call the production gap helper. The
candidate catalog contains all primitives, has no `theta=1` record, and the
fixture rejects that endpoint under `-1 < theta < 1`. Denominator-aware global
minimization selects `theta=1/2` with residual `4/3`. Every parameter witness
remains outside the fixed-channel premises and is classified
`assumption_boundary`, not theorem refutation.

**Minor -- rational denominator minimization was inert. Resolved.** The final
minimizer recursively extracts denominators from nested `Fraction` values,
validates optional denominator metadata, and ranks denominator complexity
before canonical JSON. The focused adversary proves nested `1/2` beats
lexically earlier `1/10` and rejects inconsistent declared denominator 3 for a
`1/2` witness.

**Important evidence-integrity follow-up -- durable records were stale after
the code fix. Resolved.** The scoped remediation rereview correctly withheld
approval at `3df4b92` because the result and independent-review documents still
described `ab74700`. Result commit `8127250` now records the final tested code,
26 focused tests, 466 full-suite tests with 2 skips, updated coverage, 19,587
candidates, the exact parameter primitives and values, endpoint exclusion,
low-bound controls, denominator adversary, current hashes, and final two-root
replay. This review supplies the remaining current revision-bound independent
assessment.

## Claim boundaries and unresolved obligations

The parameter-dependent-channel and one-sided-relabeling witnesses violate
the premises of the corresponding conditional identities. They are assumption
boundaries, **not theorem refutations**. Likewise, exact enumeration and
floating-point or rational replay verify implementation behavior on the saved
finite domain; numerical or computational agreement is **not mathematical
proof**.

The following obligations remain explicitly unresolved:

- `OPEN`: continuum and nondominated-law extensions, infinite-volume and
  two-index limits;
- `OPEN`: universality, nonlinear attraction, and any identification with
  physical time or physical law;
- `OPEN` / `INCONCLUSIVE`: general Gaussian-law scope beyond the declared
  small SPD controls;
- `INCONCLUSIVE`: applicability to any external multi-agent system until its
  laws, channels, actions, and premises are supplied and checked;
- `INCONCLUSIVE`: Wave-3 cross-producer metamorphics and stress checks against
  Sessions 1, 2, 4, 5, and 6; and
- `OPEN`: exhaustive coverage beyond the saved effective bounds.

Residual risks are bounded-domain scaling, the use
of floating logarithms for generally irrational KL values, and deferred
cross-laboratory integration checks. None supports a continuum, universality,
Gaussian-generality, external-application, or physical-time conclusion.

## Verdict

**APPROVED.** All core, experiment, conditioning, bound-validation,
parameter-fixture, structural-minimization, artifact-integrity, and stale-record
findings are resolved. The final exact fixture and all five metrics are
independently recomputable from saved primitives; the exhaustive finite catalog
contains 19,587 candidates within its truthful effective bounds; invalid lower
bounds fail before effects; endpoint `theta=1` is excluded; and final semantic
artifacts replay byte-identically across roots. Focused and full JUnit are
green, both new production modules exceed 80% line coverage, the seven-path
allowlist is exact, and no residual Critical or Important issue was found.

This approval is revision-bound implementation and finite-experiment closure,
not mathematical proof. The stated `OPEN` and `INCONCLUSIVE` obligations remain
unchanged and are not promoted by this approval.
