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
| P1 | `findings/P1-measure-probability.md` | Standard-Borel construction, channel pushforward, disintegration, posterior version selection, absolute continuity, a.s. qualifiers | PENDING |
| P2 | `findings/P2-information-vfe.md` | Extended-real KL chain additivity, defect `Delta_A`, extended-real VFE identity, finite tier, recovery equivalence | PENDING |
| P3 | `findings/P3-counterexamples-pointwise.md` | The five finite negative constructions; execute `finite_nongaussian_witness.py` | PENDING |
| P4 | `findings/P4-gauge-holonomy.md` | Holonomy blindness branch, typed actions, equivariance/covariance/isotropy hypotheses, `\mathscr P_G` vs scale-bundle split | PENDING |
| P5 | `findings/P5-category-operational.md` | Protocol-quotient terminality, finite minimality, compact-metrizable quotient; novelty vs Myhill-Nerode / syntactic monoid / topological algebra literature | PENDING |
| P6 | `findings/P6-blackwell-comparison.md` | Marked-soft face diameters, 15-coordinate affine determinant, circle heat-chain Blackwell dominance and soft response nesting; execute `recompute.py` | PENDING |
| P7 | `findings/P7-rg-coarsegraining.md` | `solid_RG_theory.md`, `Theory/06_general_coarsegraining.tex`, `Theory/07b_agent_network_rg.tex` 8/15 additions and their coherence with the pointwise datum | PENDING |
| P8 | `findings/P8-integration-overclaim.md` | Every 8/15 claim in `overview.md`, `Theory/SPEC.md`, `appendix_claim_ledger.tex`, `Theory/05d`, `docs/STATUS.md` versus what the packages actually prove | PENDING |
| P9 | `findings/P9-selfcert-falsifiability.md` | The certification machinery itself: adversarial report, oracle erasure, independent reconstruction, four domain views, release provenance, circularity, falsifiability | PENDING |
| P10 | `findings/P10-rigor-sweep.md` | Hedges, hand-waving, vague quantifiers in the newly added prose | PENDING |

### Wave 2 — adversarial verification

| ID | Findings file | Scope | Status |
|---|---|---|---|
| V1..Vn | `findings/V-*.md` | One skeptic per contested Critical/High wave-1 finding | PENDING |
| ADJ | `findings/ADJUDICATION.md` | Evidence-weighted adjudication of contested findings | PENDING |

### Wave 3 — synthesis

| ID | File | Scope | Status |
|---|---|---|---|
| SYN | `REPORT.md` | Final consolidated review report, severity-ranked, with a punch list | PENDING |

## Resume instructions

1. `cd` to the repo, confirm `git rev-parse HEAD` still reports `8ce6358...` (or note the drift).
2. Read this file and every `findings/*.md`. Each findings file carries its own `STATUS:` line at
   the top.
3. Re-dispatch only the tasks whose status is not `COMPLETE`. Partial findings files are usable —
   an interrupted agent's file is appended to, not restarted, unless its content is unusable.
4. Update this table as tasks complete.
