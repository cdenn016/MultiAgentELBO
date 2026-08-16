# P8 — Integration / Overclaim Audit (claim-vs-proof)

STATUS: IN_PROGRESS

Reviewer role: claim auditing — compare what the integrated manuscript ASSERTS against what the
supporting derivation packages actually PROVE; find every place scope widens between proof and prose.

Review target: `8ce635807a6ca2a388255fc996c98f7c535e5843` (branch `review/2026-08-15-deep-review`).
Diff base: `060f80e5556e41e0f31aeafcd9ef8564c1544c16^`.

## Files to examine (checklist)

Integration surfaces (the ASSERTIONS):
- [ ] `overview.md` (8/15 diff)
- [ ] `Theory/SPEC.md` (8/15 diff)
- [ ] `Theory/appendix_claim_ledger.tex` (8/15 diff, ~140 added lines)
- [ ] `Theory/05d_relational_inference.tex` (8/15 diff)
- [ ] `Theory/01_introduction.tex`, `Theory/03_probability.tex`, `Theory/04_generative.tex` (8/15 diff)
- [ ] `docs/STATUS.md` (8/15 diff)

Ground truth (the PROOFS):
- [ ] `docs/derivations/2026-08-15-full-pointwise-meta-agent/final-report.md` + `evidence/`
- [ ] `docs/derivations/2026-08-14-operational-intervention-extensions/final-report.md` + `evidence/`

Specific hunts:
- [ ] H1 "full" pointwise candidate-parent theorem — does "full" mislead? does anything downstream glue?
- [ ] H2 finiteness fence — every use of `F_I - F_A = Delta_A` / recovery equivalence without finite fine KL
- [ ] H3 conditional theorems presented as unconditional (standard-Borel, normalized common channel,
      evaluator, finite KL, holonomy branch)
- [ ] H4 every added ledger row: status vs actual evidence; scope vs frozen contract
- [ ] H5 "Say this, and not more" boilerplate in overview.md — sentence-by-sentence support check
- [ ] H6 silent retractions — claims weakened/removed on 8/15 without a recorded change

## Claim-by-claim table

(populated incrementally below)

## Findings

(populated incrementally below)
