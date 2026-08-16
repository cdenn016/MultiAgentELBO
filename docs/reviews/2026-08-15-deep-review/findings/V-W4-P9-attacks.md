# V-W4-P9-attacks — Skeptic attack on finding W4-P9-attacks

STATUS: IN_PROGRESS

AGENT: adversarial skeptic (wave 4)
TARGET REVISION: `8ce635807a6ca2a388255fc996c98f7c535e5843`
FINDING UNDER ATTACK: `W4-P9-attacks`, severity **High**, two grouped blocks at
`findings/P9-selfcert-falsifiability.md:187` (attack severity) and `:229` (missing attacks).

## Work log

- [x] Read `P0-principal-reviewer-notes.md` in full
- [x] Read both P9 finding blocks in full (`:187-225`, `:229-247`)
- [x] Read `evidence/adversarial-attacks.md` in full (all sixteen)
- [x] Dumped `adversarial-report.json` (all sixteen records + `attack_summary` + `review_adjudication`)
- [x] Read `problem-contract.json` (`target.literature_policy`, `target.boundary_conditions`)
- [x] Read `release.json`, `final-report.md`
- [x] Read the skill's own portfolio spec `references/adversarial-verification.md`
- [x] Inspected `evidence/finite_nongaussian_witness.py` + `finite-nongaussian-output.json`
- [x] Cross-checked L1 (`P1-High-1-prior-work`) in `ADJUDICATION.md`
- [ ] Primary-source check: Mayo SIST §1.2 severity requirement
- [ ] Primary-source check: Polyanskiy–Wu Thm 2.14
- [ ] Final classification table + verdict

## Interim result of the arithmetic check (recorded before source work)

The finding's own table has 16 rows and marks **14** of them "**No** — could not have succeeded"
(A1, A2, A3, A5, A6, A7, A8, A9, A10, A11, A12, A14, A15, A16). The tally sentence at `:217` says
"**13 of 16 cannot fail**" over that same enumeration `A1–A3, A5–A12, A14–A16`, which is
3 + 8 + 3 = **14** entries. The headline number in the finding's title is inconsistent with the
finding's own evidence table by one.
