# Deep review of the 2026-08-15 theory work — final report

**Target:** `8ce635807a6ca2a388255fc996c98f7c535e5843` (merge of PR #4). 67 files, 17,560 insertions.
**Diff base:** `060f80e5556e41e0f31aeafcd9ef8564c1544c16^`.
**Method:** ten independent expert investigators (wave 1); nineteen adversarial skeptics across two
waves against every Critical and High finding; evidence-weighted adjudication; plus the principal
reviewer's own reconstructions, recorded before the panel reported. No finding below is promoted on
agent agreement — each rests on a reconstructed derivation, an executed command, or a primary source.
**Detail:** `findings/P0`–`P10` (investigators), `findings/V-*` (skeptics),
`findings/ADJUDICATION.md` (wave 2), `findings/ADJUDICATION-W4.md` (wave 4).

## Bottom line

Nothing found in either wave shows a false theorem. The mathematics is correct wherever three
independent parties reconstructed it, and the fencing around it is unusually careful and repeatedly
sharper than what the panel proposed as its own fix. What outruns the mathematics is the certification
apparatus. Two of the four domain approvals backing `EVIDENCE_VERIFIED` are stale against canonical
sources edited after approval — and one of those edits inserted the certified theorem into the very
file cited as canonical for it. That is a genuine certification-validity failure, and it is the only
Critical finding that survived adversarial attack.

The novelty problem is real but much smaller than the panel filed it, and I was among those who
overstated it. The flagship theorem's measure-theoretic and information-theoretic core restates four
results this repository already had marked `ESTABLISHED` a week earlier. But the contract explicitly
disclaims novelty, three of four reviews map the derivation onto those ancestors by exact line range,
and the residual defect is that the mathematics document itself carries no pointer.

## Adjudicated findings

Eight findings were put to adversarial skeptics in wave 2 and then adjudicated (wave 4 follows below). Every one has a surviving
evidence-backed core; in five of eight that core is materially narrower than the filed headline. That
ratio is itself a result: the panel's instinct was right more often than its severity.

### Critical

**C1 — Two of four domain reviews satisfy their own stated falsification condition and were shipped
anyway.** (`evidence/reviews/view-*.md`, `release-assembly.json:73,86,99,112`)

`view-probability-kernel.md:31` and `view-gauge-holonomy.md:30` bind `Theory/06` at
`4891a8f5…` and `Theory/07b` at `5eb15949…`. At the released revision those files hash `fa10620d…` and
`268f9c3b…`. Both reviews carry an explicit post-review-mutation-of-a-canonical-source falsifier clause,
and both bind the mutated files. No re-review and no re-hash exists anywhere in the repository.

The mutation is not cosmetic: `git diff --stat 1b18842 8ce6358 -- Theory/` is +29 on `Theory/06` and
+153 on `Theory/07b`, and the `07b` insertion is the entire
`\theoremheading{Full pointwise probabilistic datum…}{thm:rg-pointwise-parent-datum}` block. The
certified proposition was written into the canonical source *after* the reviews that bind that source
approved. All four reviews are nonetheless stamped `BOUND_CURRENT_APPROVE`, and the promotion of
`target` to `EVIDENCE_VERIFIED` rests on those approvals.

No theorem is false and nothing mathematical depends on this. It is Critical under the second disjunct
of the rubric — the certification is invalid — and nothing more. Scope corrected from the filed
"four reviews" to two: `view-information-vfe.md`'s falsifiers are all mathematical and
`view-dynamics-scope.md` binds no canonical source.

### High

**H1 — The first of three provenance snapshots binds bytes that are unrecoverable.**
(`evidence/release-provenance.json`)

Recomputed against git: `review_input_snapshot` verifies **0 of 15** entries at the `add1a69` it names
(11 mismatch, 4 name paths that did not exist at that commit — including
`evidence/adversarial-attacks.md`, `independent-reconstruction.md`, `oracle-erasure.md`). An exhaustive
search of all 1,418 blobs in the object store, including unreachable ones, recovers 4 of 15.

The filed headline said *two* of three snapshots. That is refuted by execution: `fix_round_1` verifies
26/26 at `1b18842` and the final snapshot 26/26 at `8ce6358`. Two of three stages are fully auditable,
`direct-derivation.md` is recoverable and byte-identical across `1b18842`, `8ce6358` and HEAD, and the
one-way non-circular structure of the claim does hold. Reduced Critical → High.

### Medium

**M1 — The flagship theorem carries `\status{ESTABLISHED}` with neither proof nor pointer.**
`thm:rg-pointwise-parent-datum` (`Theory/07b:76-190`); a grep of that span for proof markers returns
one `\eqref` to its own equation. `Theory/SPEC.md:70` defines `ESTABLISHED` as "Proved here, or a
standard result cited to a source that has been checked", and `:29-30` ("Nothing in this document is a
report on a prior manuscript. It stands alone") forecloses repair by pointing at `docs/derivations/`.
The filed clause "no proof anywhere in `Theory/`" is false: `thm:rg-exact-coarse-vfe`
(`Theory/07b:34-66`), ten lines above, states the identical content *with* a proof giving exactly the
right argument. A broken audit trail, repairable by a five-line proof paragraph and two cross-references.

**M2 — §7's "holonomy" theorem has no connection-theoretic content.** A grep of
`direct-derivation.md:381-465` for connection/transport/loop/curvature/parallel returns four hits: the
heading, "holonomy groupoid", and two lines in the *retention* branch. The theorem (7.1)–(7.5) uses
bimeasurability, an intertwining, three pushforward hypotheses and groupoid composition — no connection
form, no lift, no loop, no curvature. The filed headline "nothing in §7 is holonomy" is false (line 461
is genuine holonomy data), and the name is inherited from `Theory/06:564-601`, where
`thm:cg-holonomy-kl-marginal` defines a real based-loop transport group `𝔥_I^x(r)`. The defect is that
the full-law generalization silently widened the acting group from loop transports to an unrestricted
groupoid and kept the name. A scope-description defect in a certified conjunct.

**M3 — `solid_RG_theory.md` is named for a theory it does not contain.** Zero occurrences of
"semigroup"; no rescaling kernel, beta function, blocking ratio, relevant/irrelevant classification, or
universality; the only "fixed point" hit is the base point `r_*`. The certified channel has no declared
inverse-direction map, so it admits no iterate and no flow. But four supporting claims fail:
`:247-252` does display a composed-scale law `C_20(B|i) = Σ_A C_21(B|A)C_10(A|i)`, and the charge that
the absence goes unfenced is refuted by `docs/STATUS.md:41,77,193,215` and `overview.md:560-565`, whose
fencing is sharper than the fix the finding proposed. What survives is one local documentation defect:
the file's "Certified boundary" section omits the obligation named in the file's own title.

### Low

**L1 — The mathematics document cites none of the theorems it re-derives.** `grep -c "Theory/"` on
`evidence/direct-derivation.md` → 0; `grep -rn "cg-"` over the package → 0; `grep -rni
"kullback\|csisz"` → 0. Read alone, §3 and §6 present as first derivations. The contract-violation and
"no citation anywhere" clauses are **refuted**: `literature_policy` is disjunctive ("checked primary
sources **or released repository derivations**") and ends "No novelty or priority claim is made", and
three of four reviews cite the ancestors by line range with mapping sentences. One cross-reference line
per section repairs it. *I filed this at High and was overridden on my own evidence; see the correction
in `findings/P0`.*

**L2 — Three limitation lists omit a gap the package's own attack register records.** A single-point
change to a posterior version on a Lebesgue-null set moves `F_I` from `log 2` to `0`. The
mathematics of the finding is sound, but the charge that the KL term is untreated is refuted:
`direct-derivation.md:45` covers "every later slice-wise expression", and attack **A4 "Null posterior
versions"** dispositions this for `VFE-CHAIN-EXTENDED` specifically. What survives is that §9,
`construction-or-strongest-theorem.md:118` and `final-report.md:40` — all advertised as the exact
limitations — omit it.

**L3 — One sentence over-reads the five negative witnesses.** `final-report.md:20` lists them inside
the "strongest verified result" sentence with no type marker. The filed claim that all five refute
premises the theory supplies is contradicted by the finding's own table (exactly two are premise
deletions — the two the report already concedes), and the claim that they are absent from
`claim-ledger.json` is refuted by dumping it (all five present, four in explicit "X is not sufficient
for Y" form). The premise "none was ever plausible" is refuted by this repo's own manuscript:
`Theory/05_elbo.tex:37` makes the marginal-substitution error "exact rather than merely warning
against it".

**L4 (new, wave 2)** — no `fingerprint_sha256` in any provenance snapshot is reproducible; no
construction rule is documented anywhere in the package.

**L5 (new, wave 2)** — `Theory/07b:151`'s unhedged "No displayed marginal pair reconstructs any of the
corresponding full laws" lacks the nondegeneracy hypothesis
`prop:prob-marginals-do-not-determine-joint` requires, and is falsified by the one-point parent case
the surrounding text permits.

## What actually checks out

This is the larger part of the evidence and carries equal weight.

**The mathematics is correct wherever it was reconstructed.** Verified by hand from the statements
alone, then independently by the skeptics: that `o ↦ Π_{A,o,X} = Π_{I,o,X}C_A` is genuinely a selected
parent posterior version — the bounded-test-function calculation goes through because `C_A` acts only
on the conditioned variable and leaves `o` fixed, so the general (false) claim "a pushforward of a
conditional law is a conditional law of the pushforward" is *not* what is used; that
`Q_{A,o,X} ≪ Π_{A,o,X}` by null-set transfer; that the additive extended-real chain
`KL(Q_I‖Π_I) = KL(Q_A‖Π_A) + Δ_A` holds with every term in `[0,+∞]` and nothing infinite subtracted;
that the zero-defect criterion holds unconditionally in the direction claimed, and that the finiteness
premise is correctly placed on the *subtraction* only; and that the recovery theorem (6.9)–(6.12) is
the classical equality-in-DPI/sufficiency characterization, correctly proved with the fence in the
right place.

**The three strongest results are the ones nobody successfully attacked.**

- *The circle heat-pair no-go.* I planted the objection that `H_sH_t = H_tH_s`, so the two chains cannot
  differ by their composite. The construction survives it, and the resolution is the substance: the
  intervention cuts at the mediator, exposing whichever kernel is *downstream*. Verified in Fourier
  through passive equality, the garbling `H_t = H_sH_{t-s}`, strictness (a reverse Markov map would need
  unbounded multipliers `e^{λ_n(t-s)}`), and strict soft-set inclusion via the stated witness
  `ν_ρ = H_ρ(x_0,·)`. The strongest single item across both packages.
- *The compact metrizable operational quotient.* Survives both traps. The relation is closed (an
  intersection of preimages of a Hausdorff diagonal), and the countable dense contextual signature is
  load-bearing — it is what buys metrizability, since `Y^{A×A}` need not be metrizable. Joint, not
  merely separate, continuity of multiplication follows because `π` is closed on a compact Hausdorff
  space, so `π×π` is again a quotient map. This is where a sloppy argument lands in compact
  right-topological semigroup territory; this one does not.
- *Syntactic-congruence terminality*, with the finite-cardinality fence stated correctly (surjectivity
  gives `|B| ≥ |Syn(Φ)|` always; equality forces bijectivity only in the finite case).

**The fencing is real, not decorative.** `docs/STATUS.md` and `overview.md:560-565` state flatly that
"exact" governs the equations and not the existence of a fixed point, that every exhibited fixed sector
is trivial, and that renormalization remains open. `direct-derivation.md:45` and attack A4 disclose the
null-slice version dependence and decline any canonical-null-version claim. The contract states outright
that no novelty or priority claim is made. Several wave-1 findings alleged overclaims the package had
already fenced, and those clauses were refuted.

**Two of three provenance stages are fully auditable** (26/26 and 26/26), and the derivation document is
recoverable and byte-identical across all three revisions.

## Remediation status (2026-08-16)

C1, H1 and H2 have been remediated at the documentation level; see
`docs/derivations/2026-08-15-full-pointwise-meta-agent/POST-RELEASE-CORRECTIONS.md`, which is
authoritative over the release artifacts. `terminal_status` is now
`COMPLETE_AFFIRMATIVE_WITH_CORRECTIONS` across `release.json`, `release-assembly.json`,
`final-report.md`, `construction-or-strongest-theorem.md`, `Theory/SPEC.md`, `overview.md`,
`solid_RG_theory.md`, `docs/STATUS.md`, and the closure record; the two stale reviews are re-stamped
`BOUND_STALE_PRE_INTEGRATION` and carry a notice at their head; provenance stage 1 carries
`audit_status: UNAUDITABLE` with the measured counts; and the bare `REJECTED_ALL_16` now carries the
fence the attacks artifact already had, with the attack count removed as a ground from
`release_gate.reason`.

**The frozen `problem-contract.json` and the mathematical evidence artifacts
(`direct-derivation.md`, `counterexample-proofs.md`, `finite_nongaussian_witness.py`) were
deliberately not modified**, so the target digest `15336a68…` and the hashes that bind the actual
proofs remain valid.

**One obligation cannot be closed by documentation and remains open:** C1's proper fix is *re-running*
`VIEW-PROBABILITY-KERNEL` and `VIEW-GAUGE-HOLONOMY` against `8ce6358` bytes. That is a new review, not
an edit, and has not been done. Until it is, the release rests on two derivation-backed domain views
and two that are correctly marked stale. H1's stage-1 bytes are unrecoverable, so marking it
unauditable is the honest terminal state rather than a repair.

## Punch list

Ordered by value. Items 1–3 are the ones that matter. Items 1–3 are now **addressed as far as
documentation can address them**; see the remediation status above for the one that still needs a
real re-review.

1. **Re-run the two stale domain reviews against `8ce6358` bytes and re-stamp, or withdraw
   `COMPLETE_AFFIRMATIVE` until they are re-run.** This is the only Critical item. Re-hash `Theory/06`
   and `Theory/07b` in `view-probability-kernel.md` and `view-gauge-holonomy.md`, or record explicitly
   that the approvals bind a pre-integration snapshot and do not extend to the released revision.
2. **Give `thm:rg-pointwise-parent-datum` a proof paragraph** — the argument already exists ten lines
   above at `thm:rg-exact-coarse-vfe` — or downgrade its `\status{}`. Under `SPEC.md`'s own rule,
   pointing at `docs/derivations/` is not available as a repair.
3. **Repair `release-provenance.json` stage 1**, or mark it explicitly unauditable. Four entries name
   paths that did not exist at the commit the snapshot claims as its `git_head`.
4. Add one cross-reference line to `direct-derivation.md` §3 and §6 naming
   `thm:cg-evidence-preserving-channel`, `cor:cg-pairwise-bayes-recovery`, `thm:cg-dpi-equality` and
   `thm:rg-exact-coarse-vfe`, and carry `Kullback1951`/`Csiszar1967` forward.
5. Rename §7's branch to state what it proves — invariance under a declared groupoid of measurable
   isomorphisms — or restrict the acting group to loop transports so the inherited name is earned.
6. Either add the missing obligation to `solid_RG_theory.md`'s "Certified boundary" section or retitle
   the file.
7. Add the null-slice version dependence to the three limitation lists; add a type marker to the five
   negative witnesses at `final-report.md:20`; document the `fingerprint_sha256` construction rule;
   hedge `Theory/07b:151`.

## Wave 4 — the unchallenged High findings, adversarially tested

All fourteen unchallenged High findings were put to eleven skeptics (five named targets individually,
P9's nine certification findings in six thematic blocks). Detail in `findings/ADJUDICATION-W4.md` and
`findings/V-W4-*.md`.

**One survives at High. One is refuted outright. Two merge into findings already adjudicated. The
other seven drop to Medium or Low.**

### New High

**H2 — The 16/16 attack-rejection rate carries no information, and the release presents it as
certification evidence.** Independent reclassification of all sixteen attacks gives **15 of 16**
decided by a frozen premise or an explicit non-claim — worse than filed — and catches an arithmetic
slip in the investigator's own table. The essentiality rescue fails: six of them *are* genuine
premise-essentiality tests, but their disposition is invariant to whether the witness exists, so both
branches of the counterfactual yield `REJECTED`. Severity criterion: Mayo, *Statistical Inference as
Severe Testing* (CUP 2018) section 1.2; Popper, *LScD* sections 6 and 82.

The defect is **not** where it was filed. `evidence/adversarial-attacks.md:4` self-fences honestly —
"`REJECTED` ... does not mean the stronger shortcut is true" — a sentence the finding elided with an
ellipsis. The overclaim is `evidence/release-assembly.json:181`, a bare
`"attack_disposition": "REJECTED_ALL_16"` inside `final_certification_evidence` feeding the release
gate. Verified directly.

### New Medium

- **M4** — `CE4_tree_directed_KL_symbolic_half_log_3` does not test its named claim (confirmed by
  execution and strengthened); `counterexample-proofs.md:198-202` should be struck from its location.
- **M5** — the `ESTABLISHED`-without-citation defect in `Theory/05d`, scope cut from six theorems and
  three classical restatements to a smaller set. The circle-heat theorem is **not** among the
  classical restatements.
- **M6** — the independent reconstruction is not outline-independent. The only wave-4 sub-finding no
  skeptic could dent: the shared section order is **contingent**, with 42,636 admissible orders over
  the load-bearing steps, so "the mathematics forces the order" fails. The release-facing
  outline-independence claim is unsupported; the reconstruction's mathematics is not in question.
- **M7** — an evidence-discipline gap between the 8/14 and 8/15 packages survives machine-reading of
  both ledgers, partly but not wholly explained by subject matter.
- P4's "holonomy blindness" finding **merges into M2**; it is the same defect restated and must not
  be double-counted.

### New Low

**L6** (4.5)'s cross-`X` notation, defused by the `:190` caveat — notation hygiene. **L7** the
contract's `/target/regularity` clause contradicts `/target/statement`, `/target/quantifiers`,
`VFE-CHAIN-EXTENDED` and `final-report.md:40`. **L8** the 0/0/0 counts come from a fix-then-count
loop over a real, git-recoverable pre-fix error. **L9** the fourth conjunct is a modeling declaration
(the strong charge, that the released theorem *contradicts* the contract, is refuted). The
missing-hostile-attack charge merges into **L1**.

**On L7 the direction of the defect is inverted from how it was filed.** `git show --stat fe08359`
shows the commit introducing the unconditional wording touched no package file: the *manuscript* is
the corrected surface and the *package labels* are stale. The release's summary artifacts
under-describe what its own hash-bound derivation proves, and the investigator's proposed fix would
have made the documentation less accurate. This skeptic also re-derived the chain identity and
zero-defect criterion from scratch, ran 20,000 random finite instances (max
|KL_I - (KL_A + Delta_A)| = 2.66e-15, zero criterion mismatches), and exhibited a non-vacuous
infinite tier — independently corroborating `findings/P0`.

### Refuted

**W4-P9-ledger-eligibility.** All nine `target.evidence_ids` enumerated verbatim against the ledger's
own `kind` field: three `DERIVATION`, six `AGENT_ASSESSMENT`, and no script or `SYMBOLIC_CHECK`
attached to `target` at all — those bind only the five `NEG-*` claims. Closure rests on derivations.
The charge worked only by importing an eligibility rule from a separate verification protocol that
this package never adopted.

## Calibration

**Nineteen findings across waves 2 and 4 were put to adversarial skeptics. Three survived at their
filed severity**; sixteen were narrowed, merged, or refuted. Investigator severity ran roughly one to
two levels hot, and several findings' *locations* were wrong even where their cores were right — H2
blamed the honest artifact rather than the release gate; M4 cited a proof file that should be struck
from its location line. Apply the same correction factor to anything below.

## Coverage and what this review does not establish

All 2 Critical and all 14 High findings have now been adversarially tested and adjudicated. **The 46
Medium and 29 Low findings have not been**, and remain unchallenged rather than confirmed; given the
calibration above, assume they are overstated. Two apparent Highs were duplicates already adjudicated
and are not double-counted (`P7:110` = M1; `P8:353` = C1).

No code was executed beyond the packages' own witness scripts, the skeptics' independent verification
scripts, and git/hash verification. No claim in this report rests on a `.verification/` ledger state,
on the reviewed package's internal attestations, or on agreement among agents.

## Final tally

| Severity | Count | Items |
|---|---|---|
| Critical | 1 | C1 stale domain approvals |
| High | 2 | H1 provenance stage 1; H2 attack-portfolio certification evidence |
| Medium | 7 | M1-M7 |
| Low | 9 | L1-L9 |
| Refuted | 3 | one finding outright; two headline clauses |

No false theorem was found in either package.
