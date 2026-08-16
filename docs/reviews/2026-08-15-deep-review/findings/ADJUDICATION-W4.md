STATUS: COMPLETE
AGENT: principal reviewer, adjudicating wave 4 directly
TARGET: 8ce635807a6ca2a388255fc996c98f7c535e5843

# Wave 4 adjudication

The wave-4 adjudicator agent died on a connection error after all eleven skeptics completed. I
adjudicated from the eleven skeptic files on disk plus my own checks, under the same binding rules:
CONFIRMED only on a reconstructed derivation, an executed command with real output, or a cited
primary source; never on agent agreement; correctness and attribution defects kept separate.

## Verdict table

| Finding (all filed High) | Skeptic verdict | ADJUDICATED severity | Basis |
|---|---|---|---|
| W4-P9-attacks (a) — 13 of 16 attacks cannot fail | UPHELD_REDUCED | **High** | Skeptic's independent reclassification (15/16, not 13); I verified the relocation myself |
| W4-P3-CE4 — check does not test its named claim | UPHELD_REDUCED | **Medium** | Executed; mechanical core confirmed and strengthened |
| W4-P10-05d — six `ESTABLISHED` theorems uncited | UPHELD_REDUCED | **Medium** | Scope cut from six/three to a smaller set |
| W4-P9-independence (b) — reconstruction not outline-independent | **UPHELD** (part b) | **Medium** | Order shown contingent, not forced: 42,636 admissible orders |
| W4-P9-regression — 8/15 weaker than 8/14 discipline | UPHELD_REDUCED | **Medium** | Both ledgers machine-read |
| W4-P4-blindness — inherited invariance, not blindness | UPHELD_REDUCED | **merged into M2** | Skeptic: "must NOT be counted as a second Medium alongside P4-High-2" |
| W4-P1-crossX — (4.5) asserts the disclaimed factorization | UPHELD_REDUCED | **Low** | Notation hygiene; `:190` caveat defuses it |
| W4-P2-infinite-tier — unconditional criterion outside contract | UPHELD_REDUCED | **Low** | Contract self-contradiction; direction of defect inverted |
| W4-P9-counts — 0/0/0 from a fix-then-count loop | UPHELD_REDUCED | **Low** | Real pre-fix error confirmed via git |
| W4-P9-fourth-conjunct — released theorem contradicts contract | UPHELD_REDUCED | **Low** | Charge (ii), the strong one, refuted |
| W4-P9-attacks (b) — missing hostile-referee attacks | UPHELD_REDUCED | **merged into L1** | Duplicative |
| W4-P9-ledger-eligibility — closes on ineligible evidence | **REFUTED** | **None** | Nine `evidence_ids` enumerated verbatim |

Eleven findings tested, all eleven filed at High. **One survives at High. One is refuted outright.
Two merge into findings already adjudicated in wave 2. The remaining seven drop to Medium or Low.**

## The one finding that survives at High

**H2 — The 16/16 attack-rejection rate carries no information, and the release presents it as
certification evidence anyway.**

The skeptic reclassified all sixteen attacks independently and got **15 of 16** decided by a frozen
premise or an explicit non-claim — worse than the filed 13, and it caught an arithmetic slip in the
investigator's own table (14 "No" rows against a stated tally of 13). It also killed the rescue I
proposed in the brief: six of the thirteen *are* premise-essentiality tests (A5, A6, A7, A9, A10
clean, A2 partial), which is real mathematics, but their **disposition is invariant to whether the
witness exists** — both branches of the counterfactual yield `REJECTED` — so the count still conveys
nothing about the theorem. Severity criterion: Mayo, *Statistical Inference as Severe Testing* (CUP
2018) §1.2; Popper, *LScD* §§6, 82.

**The skeptic relocated the defect, and I verified the relocation myself.** The finding blamed
`evidence/adversarial-attacks.md`, quoting it with an ellipsis that elided the exculpatory sentence.
The artifact is honest — `adversarial-attacks.md:4` reads, in full:

> `REJECTED` means the attack does not defeat the recorded scoped claim because a cited derivation or
> counterexample supplies the needed condition. **It does not mean the stronger shortcut is true.**

The overclaim is one file over. `evidence/release-assembly.json:181` carries a bare
`"attack_disposition": "REJECTED_ALL_16"` inside `final_certification_evidence`, with no such fence,
feeding the release gate. That is where the repair belongs.

## Where I depart from a skeptic

**W4-P9-independence.** The skeptic filed the whole grouped finding at Medium but marked part (b)
**UPHELD** — not reduced — having found no defense: the shared section order is *contingent*, with
42,636 admissible orders on the load-bearing steps, so "the mathematics forces the order" (the
defense I proposed in the brief) fails. I adjudicate part (b) at Medium and record that it is the
only wave-4 sub-finding no skeptic could dent. The release-facing claim of outline-independence is
unsupported; the *mathematics* of the reconstruction is not in question.

**W4-P2-infinite-tier.** The skeptic's most useful result is that the **direction of the defect is
inverted**. `git show --stat fe08359` shows the commit that introduced the unconditional wording
touched no package file, so the manuscript is the *corrected* surface and the package labels are
*stale* — the release's summary artifacts under-describe what its own hash-bound derivation proves.
The investigator's proposed fix (demote the manuscript's `\status{ESTABLISHED}`) would make the
documentation less accurate. What survives is genuine but small: `/target/regularity`'s unqualified
"finite terms wherever KL or VFE expressions are displayed" contradicts `/target/statement`,
`/target/quantifiers`, the `VFE-CHAIN-EXTENDED` ledger entry, and `final-report.md:40`. A
self-contradictory contract clause. Low.

This one also corroborates P0 independently: the skeptic reconstructed the chain identity and the
zero-defect criterion from scratch and ran 20,000 random finite instances, max
`|KL_I − (KL_A + Δ_A)| = 2.66e-15`, zero criterion mismatches, and exhibited a non-vacuous infinite
tier (`Y = ℕ×ℤ₂`, `C_A` the projection, `Δ_A = Σ_n q_n KL(t_n‖Unif)` positive or zero while
`KL_I = KL_A = +∞`).

## The refutation

**W4-P9-ledger-eligibility — REFUTED.** All nine `target.evidence_ids` enumerated verbatim against
the ledger's own `kind` field: three `DERIVATION` (`EV-TASK3-DIRECT-DERIVATION`,
`EV-TASK4-COUNTEREXAMPLE-DERIVATIONS`, `EV-TASK5-INDEPENDENT-RECONSTRUCTION`) and six
`AGENT_ASSESSMENT`. No script and no `SYMBOLIC_CHECK` is attached to `target` at all — those bind
only the five `NEG-*` claims. Closure therefore rests on derivations, and the charge worked only by
importing an eligibility rule from the user's separate `verification` skill that this package never
adopted. Violating a rule you declared is High; failing one you never adopted is not a finding
against this package.

## Calibration note

Across waves 2 and 4, **nineteen findings were put to adversarial skeptics. Three survived at their
filed severity** (the stale domain approvals at Critical, the provenance stage at High after a
headline correction, and this attack-portfolio finding at High). Sixteen were narrowed, merged, or
refuted. Investigator severity in this review ran roughly one to two levels hot, and several
findings' *locations* were wrong even when their cores were right — the attack-portfolio finding
blamed the honest artifact rather than the release gate; the CE4 finding cited a proof file that
should be struck from its location line. Any future use of the unchallenged Medium and Low findings
should assume the same correction factor.
