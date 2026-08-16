# Deep review of the 2026-08-15 codex work — RESUME / STATE FILE

**Purpose of this file.** This review is expected to be interrupted by a rate limit that resets at
01:00 on 2026-08-16. This file is the durable handoff. A resumed session should read this file
first, then read every file under `findings/`, then continue from the first task whose status is
not `COMPLETE`.

## Binding

| Field | Value |
|---|---|
| Review target revision | `8ce635807a6ca2a388255fc996c98f7c535e5843` (merge of PR #4, `main` at 2026-08-15) |
| Diff base for "the 8/15 work" | `060f80e5556e41e0f31aeafcd9ef8564c1544c16^` |
| Review branch | `review/2026-08-15-deep-review` |
| Review started | 2026-08-15 ~21:40 CDT |
| Scale of target | 67 files, 17,560 insertions, 171 deletions |
| Wave 1 workflow run ID | `wf_f6996164-a6c` (task `wktd2gjii`) |
| Wave 1 script | `docs/reviews/2026-08-15-deep-review/workflows/wave1.js` (durable copy) — resumable with `Workflow({scriptPath, resumeFromRunId})` |
| Wave 2 script | `docs/reviews/2026-08-15-deep-review/workflows/wave2.js` (durable copy) — takes `args.contested`, or runs standalone in self-triage mode |
| Scheduled continuation | 2026-08-16 01:05 local (session-scoped cron; see "Resume instructions") |

Reproduce the target diff with:

```
git diff 060f80e5556e41e0f31aeafcd9ef8564c1544c16^ 8ce635807a6ca2a388255fc996c98f7c535e5843
```

## What landed on 2026-08-15

Two rigorous-theory-search packages plus their manuscript integration.

1. **Operational intervention extensions** —
   `docs/derivations/2026-08-14-operational-intervention-extensions/`. Contextual/syntactic protocol
   quotient terminality; minimality of protocol-class cardinality for finite monoids; a
   compact-metrizable quotient under compact-Feller hypotheses; BSC nonidentifiability extended to
   normalized marked-soft mediator replacement and to independently randomized affine experiments;
   an ordered circle heat-chain pair with equal passive retained law but strict Blackwell separation.
2. **Full pointwise meta-agent** —
   `docs/derivations/2026-08-15-full-pointwise-meta-agent/`. A static pointwise standard-Borel parent
   construction at fixed `r_*`, fixed structural `X`, one admitted observation, through one
   normalized recognition-independent Markov channel `C_A`; additive extended-real KL chain with
   defect `Delta_A`; zero-defect and pairwise-recovery characterizations; a holonomy-blindness /
   raw-retention branch; and five finite categorical negative witnesses.
3. **Notation program** — `evidence/notation-standard.md`, `notation-registry.json`,
   `notation_scan.py`, and the `P -> \mathscr P_G` root-gauge vs scale-local bundle separation
   propagated through `Theory/` and `overview.md`.
4. **Manuscript integration** — `Theory/01,02,03,04,05c,05d,06,06a,07b`, `Theory/SPEC.md`,
   `Theory/appendix_claim_ledger.tex`, `Theory/appendix_notation.tex`, `overview.md`,
   `solid_RG_theory.md`, `docs/STATUS.md`.

The packages self-certify: `target` is recorded `EVIDENCE_VERIFIED`, terminal status
`COMPLETE_AFFIRMATIVE`, "no unresolved obligations", 16 adversarial attacks rejected, four domain
views `APPROVE` at Critical/High/Medium `0/0/0`. **The review exists to test that certification, not
to accept it.**

## Review protocol

Wave 1 deploys independent expert investigators. Wave 2 runs adversarial skeptics against the
highest-severity wave-1 findings and then adjudicates. Wave 3 synthesizes. No finding is promoted to
the final report on agent agreement alone; each surviving finding must cite a specific file, line or
section, and either a reconstructed derivation, an executed command with its output, or a primary
source.

Severity scale: **Critical** (a stated theorem is false or the certification is invalid),
**High** (a claim is materially stronger than its proof, or a proof has a repairable gap),
**Medium** (imprecision, missing hypothesis, notation collision, or a citation/novelty problem),
**Low** (wording, presentation, hedging).

## Task table

Status values: `PENDING`, `IN_PROGRESS`, `COMPLETE`, `BLOCKED`.

### Wave 1 — expert investigators

| ID | Findings file | Scope | Status |
|---|---|---|---|
| P1 | `findings/P1-measure-probability.md` | Standard-Borel construction, channel pushforward, disintegration, posterior version selection, absolute continuity, a.s. qualifiers | COMPLETE |
| P2 | `findings/P2-information-vfe.md` | Extended-real KL chain additivity, defect `Delta_A`, extended-real VFE identity, finite tier, recovery equivalence | COMPLETE |
| P3 | `findings/P3-counterexamples-pointwise.md` | The five finite negative constructions; execute `finite_nongaussian_witness.py` | COMPLETE |
| P4 | `findings/P4-gauge-holonomy.md` | Holonomy blindness branch, typed actions, equivariance/covariance/isotropy hypotheses, `\mathscr P_G` vs scale-bundle split | COMPLETE |
| P5 | `findings/P5-category-operational.md` | Protocol-quotient terminality, finite minimality, compact-metrizable quotient; novelty vs Myhill-Nerode / syntactic monoid / topological algebra literature | COMPLETE |
| P6 | `findings/P6-blackwell-comparison.md` | Marked-soft face diameters, 15-coordinate affine determinant, circle heat-chain Blackwell dominance and soft response nesting; execute `recompute.py` | COMPLETE |
| P7 | `findings/P7-rg-coarsegraining.md` | `solid_RG_theory.md`, `Theory/06_general_coarsegraining.tex`, `Theory/07b_agent_network_rg.tex` 8/15 additions and their coherence with the pointwise datum | COMPLETE |
| P8 | `findings/P8-integration-overclaim.md` | Every 8/15 claim in `overview.md`, `Theory/SPEC.md`, `appendix_claim_ledger.tex`, `Theory/05d`, `docs/STATUS.md` versus what the packages actually prove | COMPLETE |
| P9 | `findings/P9-selfcert-falsifiability.md` | The certification machinery itself: adversarial report, oracle erasure, independent reconstruction, four domain views, release provenance, circularity, falsifiability | COMPLETE |
| P10 | `findings/P10-rigor-sweep.md` | Hedges, hand-waving, vague quantifiers in the newly added prose | COMPLETE |

### Wave 2 — adversarial verification

| ID | Findings file | Scope | Status |
|---|---|---|---|
| V1..V8 | `findings/V-*.md` | 8 skeptics dispatched against the contested Critical/High findings | COMPLETE |
| ADJ | `findings/ADJUDICATION.md` | Evidence-weighted adjudication of contested findings | COMPLETE |

### Wave 3 — synthesis

| ID | File | Scope | Status |
|---|---|---|---|
| SYN | `REPORT.md` | Final consolidated report — see it for results | COMPLETE |

## Resume instructions

1. `cd` to the repo, confirm `git rev-parse HEAD` still reports `8ce6358...` (or note the drift).
2. Read this file and every `findings/*.md`. Each findings file carries its own `STATUS:` line at
   the top.
3. Re-dispatch only the tasks whose status is not `COMPLETE`. Partial findings files are usable —
   an interrupted agent's file is appended to, not restarted, unless its content is unusable.
4. Update this table as tasks complete.

## Outcome (all three waves complete)

Final report: `REPORT.md`. Adjudicated: 1 Critical, 1 High, 3 Medium, 5 Low. No false theorem found.
The Critical finding is a certification-validity failure (two of four domain approvals are stale
against canonical sources edited after approval). Five of eight adversarially-tested findings were
materially narrowed and two headline clauses were outright refuted.

**Remaining work, if this is picked up again:** the unchallenged wave-1 findings (~14 High, 46 Medium,
29 Low by investigator label) were never put to a skeptic and must not be treated as confirmed. The
five highest-value ones to test next are named in `REPORT.md` under "Coverage".

## Wave 4 — IN_PROGRESS (launched 2026-08-16 01:05)

Run ID `wf_a1fd026a-2f3` (task `w0fj9gyeh`): 11 skeptics + adjudicator. Five named targets plus six
grouped blocks covering all nine P9 High findings. `MAX_SKEPTICS` raised to 12.

Target-revision check at launch: `8ce6358` is an ancestor of HEAD and no target artifact differs;
the only working-tree changes are new uncommitted WIP (`solid_RG_theory.tex` guide and its change-log
entry), which this review does not touch.

Waves 1-3 finished ahead of the rate limit. The remaining work is adversarial testing of the
UNCHALLENGED wave-1 findings. Do not redo waves 1-3.

Dispatch skeptics against these five first:

| # | Finding | Location |
|---|---|---|
| 1 | (4.5) asserts the cross-`X` factorization §9 disclaims | `findings/P1-measure-probability.md:150` |
| 2 | Unconditional zero-defect criterion asserted `ESTABLISHED` on a release whose contract excludes the infinite tier | `findings/P2-information-vfe.md:160` |
| 3 | `CE4_tree_directed_KL_symbolic_half_log_3` does not test its named claim | `findings/P3-counterexamples-pointwise.md:163` |
| 4 | "Holonomy blindness" is inherited invariance, not blindness | `findings/P4-gauge-holonomy.md:33` |
| 5 | Six new `ESTABLISHED` theorems in `Theory/05d` carry no citation | `findings/P10-rigor-sweep.md:153` |

Then P9's eight remaining High findings on the certification machinery — the largest untested block.

**Do not re-test:** `P7-rg-coarsegraining.md:110` (duplicate of adjudicated M1) and
`P8-integration-overclaim.md:353` (duplicate of adjudicated C1).

Run with `workflows/wave2.js`, passing `args.contested` as `{id, severity, title, location,
one_line_evidence, source_file}` records; raise `MAX_SKEPTICS` above 8 if needed. Binding rules carry
over: CONFIRMED only on a reconstructed derivation, an executed command with real output, or a cited
primary source — never on agent agreement. Append a "Wave 4" section to `REPORT.md` when done.
