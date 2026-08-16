STATUS: IN_PROGRESS
ROLE: adversarial skeptic (wave 2), assigned to kill or confirm one wave-1 finding
TARGET REVISION: 8ce635807a6ca2a388255fc996c98f7c535e5843
FINDING UNDER ATTACK: `P3-High-1-strawman-negatives`
  title: "All five negative results refute premises the affirmative theory itself supplies; the
          final report concedes this for only two of the five"
  stated severity: High

# VERDICT: UPHELD_REDUCED — corrected severity **Low**

Both clauses of the finding's title are wrong as stated. A small residue survives, and it is not the
residue the finding names.

- **"All five refute premises the affirmative theory itself supplies"** — false, and false by the
  investigator's own table. Exactly two of the five (N2, N3) are premise deletions. N1 deletes no
  hypothesis (the investigator's own row says "none"). N4 and N5 refute *external* propositions and
  *declined converses*, which is a different logical object from a premise-deleted theorem.
- **"the final report concedes this for only two of the five"** — false as a reading of the
  paragraph. `final-report.md:40` is a single scope paragraph whose two sentences fence N2, N3
  (explicitly, as "premise-deleted overreach"), N4 ("Holonomy blindness is a full-law statement
  under explicit action/version/evaluator hypotheses"), and N5 ("marginal invariance is not
  full-law invariance"). N1's fence is in the companion theorem document at
  `construction-or-strongest-theorem.md:55`. The phrase "premise-deleted overreach" is applied to
  exactly the two witnesses that actually delete premises — which is correct usage, not an
  incomplete concession.
- **"none of the five was ever a plausible claim"** (the finding's load-bearing premise for calling
  them strawmen) — contradicted by this repository's own manuscript, which devotes an
  `\status{ESTABLISHED}` proposition and a section *titled* "Two agreements, and the cost of
  conflating them" to exactly two of the five conflations, and uses one of them as a load-bearing
  step in the proof of an affirmative corollary.

**What survives (Low):** `final-report.md:20` lists the five negatives in the same breath as the
affirmative construction, and the closure headline counts them among the seventeen
`EVIDENCE_VERIFIED` ancestors, without marking that they are insufficiency/sharpness witnesses over
a two-atom space rather than results of the same standing. That is a summary-prose calibration
issue in one sentence, it is disclosed correctly two paragraphs later and in
`counterexample-register.md:61,63`, and it overlaps almost entirely with the investigator's own
separate Medium finding on the `DERIVATION`/`supports: true` bookkeeping.

---

## 1. Relation to the principal reviewer's reconstructions

No contradiction. `P0-principal-reviewer-notes.md` reconstructs the parent-posterior version, parent
absolute continuity, the additive KL chain, and the recovery/equality-in-DPI theorem — all
affirmative, all on the Task-3 side. It says nothing about the five negative witnesses. Its standing
conclusion ("the mathematics is right; novelty and certification language are the live issues") is
consistent with my verdict here: this finding is a certification-language issue, correctly sized as
Low, not a High.

## 2. Attack 1 — the classification in the finding's own table defeats the finding's own title

The finding's table assigns to each negative "the hypothesis it deletes". Read the rows:

| | refuted proposition | investigator's own "hypothesis it deletes" |
|---|---|---|
| N1 | marginals determine the joint | **"none"** |
| N2 | split-channel VFE contraction | common-channel premise `C_Q = C_Π` |
| N3 | normalized model marginal forces evaluator compatibility | a.s. compatibility |
| N4 | trivial holonomy ⟹ agreement | "(7.3)" |
| N5 | marginal invariance ⟹ joint invariance | "(7.3) again; the theory never claims the converse" |

The N1 row states "none" and the N5 row states "the theory never claims the converse". Two of the
five rows therefore say, in the finding's own text, that these are *not* premise deletions. The title
nevertheless says "All five negative results refute premises the affirmative theory itself supplies."
The title over-reaches its own table.

N4 is the row that needs reconstruction rather than reading, so I did it.

### 2.1 Reconstruction of the N4 claim — the witness violates (7.3), but that is not what "premise-deleted" means

I read `evidence/direct-derivation.md` §7 in full (lines 383–465). The hypothesis set is

- (7.1) `(T_O^g × T_I^g)_# P_I(·|X) = P_I'(·|X')`
- (7.2) `(T_I^g)_# Π_{I,o,X} = Π'_{I,o',X'}`
- (7.3) `(T_I^g)_# Q_{I,o,X} = Q'_{I,o',X'}`
- (7.4) `C_A'(T_I^g Y, D) = C_A(Y, (T_A^g)^{-1} D)`

and the **conclusion** (7.5) is covariance of the three parent laws:
`(T_O^g × T_A^g)_# P_A = P_A'`, `(T_A^g)_# Π_{A,o,X} = Π'_{A,o',X'}`, `(T_A^g)_# Q_{A,o,X} = Q'_{A,o',X'}`.

Now take the finding's reading of CE-4 §5.1: two nodes as slices `(o,X)`, `(o',X')`, arrow `g` with
`T_I^g = id`, node laws `P = Bern(1/4)`, `Q = Bern(3/4)`. Then (7.3) reads `id_# P = Q`, i.e.
`P = Q`, which is false for these data. So the witness data **do** violate (7.3). That much of the
investigator's reconstruction is correct and I confirm it.

But the inference drawn from it — "It is exactly as premise-deleted as CE-2 and CE-3" — does not
follow, and the distinction is not pedantic:

- The premise-deleted statement here is `(7.1) ∧ (7.2) ∧ (7.4) ⟹ (7.5)`. CE-4 §5.1 is not an
  instance of it: the witness declares no `P_I`, no `Π_{I,o,X}`, no `C_A`, and no `T_A^g`. It cannot
  falsify a statement whose antecedent it never instantiates.
- The proposition CE-4 §5.1 actually refutes is `trivial holonomy ⟹ node laws agree`. That is not
  (7.5) with a premise removed. (7.5) never concludes agreement of anything; it concludes
  *covariance between slices*. Agreement is a different predicate.

So N4 refutes a proposition **external** to the theorem, not a weakened form of it. CE-2 and CE-3,
by contrast, are genuine sharpness witnesses in the textbook sense: each satisfies every remaining
hypothesis and falsifies the conclusion, so each proves the deleted hypothesis is not removable.
`counterexample-proofs.md:172` says exactly this for CE-2 — "it proves that the common-channel
hypothesis cannot be omitted."

The consequence for the finding: the report's use of the phrase "premise-deleted overreach" for
exactly N2 and N3 is **type-correct**, not an incomplete concession. Extending that phrase to N1,
N4, N5 as the finding's Fix demands would make the report *less* accurate, not more.

## 3. Attack 2 — the "concedes only two" reading of `final-report.md:40` does not survive reading line 40

Line 40 is one paragraph. Quoting the relevant two sentences in full:

> "Split-channel and incompatible-evaluator witnesses refute premise-deleted overreach rather than
> the conditional common-channel theorem. **Holonomy blindness is a full-law statement under
> explicit action/version/evaluator hypotheses; marginal invariance is not full-law invariance**,
> and raw retention preserves the complete joint marked record."

The bolded second sentence is the N4 and N5 fence: it states that the holonomy conclusion is
hypothesis-conditional (so trivial holonomy alone is asserted to give nothing) and states N5's
content as a limitation of the affirmative result. The finding quotes the first sentence and treats
the paragraph as stopping there.

N1's fence is in the theorem document, `construction-or-strongest-theorem.md:55`:

> "These identities do not reconstruct a joint law: the exact finite witnesses … verify marginal
> nonuniqueness and the failure of marginal invariance to imply joint invariance."

and again in `direct-derivation.md:244` and `:459`:

> ":244 — No converse or reconstruction theorem from these marginal identities is claimed here"
> ":459 — Forward projection gives marginal invariance whenever full-law invariance holds. No
>  converse or reconstruction theorem from separate marginal invariance is claimed here"

and in `counterexample-register.md:61`:

> "CE-2 and CE-3 refute theorems obtained by deleting the common-channel or compatibility premises,
> not the conditional theorem proved under those premises. CE-5 distinguishes marginal invariance
> from full-law invariance. CE-4 distinguishes trivial transport holonomy from equality of node
> laws."

The register addresses four of five by name in one paragraph, each in language matched to its type.
The finding cites register line 61 in its Location field and then does not use it.

**Net:** the correct statement is "the package fences all five; the specific phrase 'premise-deleted
overreach' is applied to the two witnesses that are premise deletions; N1 alone has no fence inside
`final-report.md` itself." That is a Low, and it is a different sentence from the one the finding
attacks.

## 4. Attack 3 — "none of the five was ever a plausible claim" is refuted by this repository's own manuscript

The finding's severity rests on the claim that the refuted universals are strawmen nobody would
assert. The manuscript in `Theory/` treats two of them as live errors, in its own words, at
`\status{ESTABLISHED}`.

**N1.** `Theory/03_probability.tex:430` —

> "In the Gaussian realization with at least two nondegenerate real coordinates, the marginals … are
> therefore **a lossy summary, and the next statement exhibits the loss**."

followed at `:433` by `\propositionheading{Coordinate marginals do not determine a sufficiently rich
joint}` `\status{ESTABLISHED}`, with a Gaussian proof. `Theory/05_elbo.tex:37` —

> "The consequence for this chapter is not stylistic. Marginal recognition laws cannot be substituted
> for the population law in an exact entropy or evidence calculation, and the following **makes the
> error exact rather than merely warning against it**."

The manuscript calls it *the error*, and then proves an "Extended total-correlation chain identity"
to quantify it. The proposition is then load-bearing in the proof of an affirmative result:
`Theory/05_elbo.tex:289`, proof of `cor:elbo-bound-tightness`, whose statement includes "Equality of
all coordinate marginals is not sufficient. `\status{ESTABLISHED}`" and whose proof discharges that
clause by citing `prop:prob-marginals-do-not-determine-joint`. And at
`Theory/06_general_coarsegraining.tex:690-694`:

> "Under the richness hypothesis of `prop:prob-marginals-do-not-determine-joint`, distinct joint laws
> can have identical coordinate marginals. **Identical transported marginals therefore do not imply**
> [the common-recovery condition]. `\status{ESTABLISHED}`"

That last passage is N1 and N5 combined, used to block an inference at a load-bearing point of the
coarse-graining chapter. A proposition whose negation is a cited step inside an affirmative
`ESTABLISHED` corollary is not a strawman.

**N4.** `Theory/12_philosophy.tex:215` is a section titled

> "**Two agreements, and the cost of conflating them**"

whose content (`:229–232`, `\status{ESTABLISHED}`) is precisely CE-4:

> "They are independent. A graph coboundary constrains links but leaves the means free. Conversely,
> under nontrivial holonomy, belief agreement can survive on the fixed subspace
> `μ_{i_0} ∈ ker(H_γ^b − I)`."

A manuscript does not title a section "the cost of conflating them" for a conflation nobody makes.
The two halves of that passage are exactly CE-4 §5.1 (frame agreement does not give belief
agreement) and CE-4 §5.2 (nontrivial holonomy can nonetheless leave a law fixed).

Note further that CE-4 §5.2's content is not a refutation at all — it is the **witness for an
affirmative assertion in the derivation**. `direct-derivation.md:459`:

> "Full-frame triviality is one sufficient way to make these actions identities, but **it is not
> necessary: a nontrivial action may stabilize the full law**."

An existence claim of that form requires a witness, and the fair-law bit flip `g(u)=1−u`,
`g_# Bern(1/2) = Bern(1/2)` is it. So one of the five registered negatives directly discharges a
claim the affirmative document makes. Calling it a strawman is simply wrong.

This does not literally satisfy the finding's stated falsifier (which asks for a passage *asserting*
one of the five universals). It defeats the finding's *reasoning* instead: the program's own
manuscript establishes that these conflations are errors worth proving against, which is what makes
the witnesses useful rather than empty.

## 5. Attack 4 — the finding's Evidence paragraph is inaccurate about the ledger

The finding states: "they are not recorded in `claim-ledger.json` at all (I enumerated all 19 claims
— none of them is a universal overreach statement)."

I dumped the five `NEG-*` claim records. Every one names the refuted universal inside its
`statement` field:

- `NEG-MARGINAL-DETERMINATION`: "… **refuting universal reconstruction of the full parent from those
  marginals**."
- `NEG-MODEL-MARGINAL-EVALUATION`: "… **refuting model-marginal sufficiency for evaluation
  compatibility**."
- `NEG-TRIVIAL-HOLONOMY-AGREEMENT`: "… **refuting trivial holonomy as sufficient for belief or model
  agreement**."
- `NEG-MARGINAL-HOLONOMY-JOINT`: "… **refuting marginal holonomy invariance as sufficient for
  full-law invariance**."
- `NEG-SPLIT-CHANNEL-VFE`: "… violate the **unconditional** common-channel contraction and VFE
  identity."

Four of five are phrased as "X is not sufficient for Y" — which is the correct, honest form of an
insufficiency/sharpness result, and it is machine-readable. The finding's claim that the ledger says
nothing about what is refuted is wrong. (This also partly undercuts the investigator's separate
Medium finding on the `DERIVATION`/`supports: true` encoding, item 3.)

## 6. What I concede

- The five negatives do not constrain the affirmative pointwise theorem. That part of the finding is
  correct and I do not dispute it.
- The investigator's arithmetic reproduction is correct; I did not re-run it, and I have no reason to
  doubt it. Nothing in my verdict depends on any number being wrong.
- `final-report.md:20` does list the five negatives in the "Strongest verified result" sentence
  without a type marker, and the "seventeen transitive ancestors, all `EVIDENCE_VERIFIED`" headline
  counts them. A reader who reads only that sentence will over-read five two-atom insufficiency
  witnesses as substantive theorems. That is real. It is a summary-prose calibration defect of the
  kind the review brief classifies as "the claim is correctly fenced in the derivation and only the
  SUMMARY prose is loose" — which changes the severity and the location, not the mathematics.
- The correct fix is **not** the finding's proposed sentence (which would misapply "premise-deleted"
  to three witnesses that delete no premise). The correct fix is one clause at `final-report.md:20`:
  *"…and five exact finite insufficiency witnesses establishing that the common-channel,
  compatibility, and full-law hypotheses are not removable and that marginal-level data do not
  determine joint-level structure."*

## 7. Corrected finding

> **[Low]** `final-report.md:20` lists the five negative constructions among the "strongest verified
> result" without marking them as insufficiency/sharpness witnesses, and the seventeen-ancestor
> closure count includes them on a par with the affirmative construction. The scope is stated
> correctly at `final-report.md:40`, `counterexample-register.md:61,63`,
> `construction-or-strongest-theorem.md:55`, and `direct-derivation.md:244,459`; only the
> one-sentence summary is uncalibrated. No mathematics is affected, and the "premise-deleted"
> characterization applies to exactly two of the five, which is exactly where the report applies it.

## 8. Falsifier of my own attack

My verdict is wrong if any of the following holds.

1. **The line-40 second sentence is not a fence for N4/N5.** If a reader can show that "Holonomy
   blindness is a full-law statement under explicit action/version/evaluator hypotheses; marginal
   invariance is not full-law invariance" is asserting the affirmative holonomy result rather than
   bounding it, then the concession really does name only two and the finding's factual half stands.
   My reading rests on the sentence sitting inside the "Scope and limitations" section; if that
   section heading were not present, the reading would be weaker.
2. **CE-4 §5.1 is an instance of the premise-deleted theorem after all.** If the frozen types supply
   default `P_I`, `Π_{I,o,X}`, `C_A` for a bare two-node transport datum — so that the witness does
   instantiate (7.1), (7.2), (7.4) and falsify (7.5) — then N4 is a genuine premise deletion and the
   finding's table row is right. I found no such defaulting in `problem-contract.json` or §7, but I
   did not read §§1–6 of `direct-derivation.md` in full.
3. **`Theory/12_philosophy.tex` and `Theory/03_probability.tex` are not part of the affirmative
   theory this package certifies.** My strawman rebuttal uses the manuscript as evidence that the
   conflations are live errors. If the derivation package is meant to stand independently of
   `Theory/` — and the finding's own falsifier does name `Theory/` as in scope, so I believe it does
   not — that leg weakens, though the `direct-derivation.md:459` "it is not necessary" witness for
   CE-4 §5.2 survives regardless.
4. **The residual is not Low.** If the deep review concludes that mis-scoped closure counting in a
   certification artifact is itself a High-severity reporting defect, then the residue I concede
   would be re-graded upward. I judge Low because the correct scope statement is present in four
   documents including the same paragraph of the same file.

## 9. Method and evidence actually used

Read in full: `evidence/counterexample-proofs.md` (222 lines), `final-report.md` (40),
`counterexample-register.md` (63), `construction-or-strongest-theorem.md` (118),
`evidence/direct-derivation.md` §§7–9 (lines 370–498), `P3-counterexamples-pointwise.md` (667),
`P0-principal-reviewer-notes.md` (192).
Executed: JSON dump of the five `NEG-*` records from `claim-ledger.json`;
`grep -rn "prob-marginals-do-not-determine-joint" Theory/*.tex` (5 hits, listed above);
targeted reads of `Theory/03_probability.tex:425-470`, `Theory/05_elbo.tex:25-40,275-292`,
`Theory/06_general_coarsegraining.tex:680-700`, `Theory/12_philosophy.tex:215-250`.
Reconstructed by hand: the §7 hypothesis-to-conclusion map, and the claim that CE-4 §5.1 does not
instantiate the premise-deleted statement.
Attempted and **not** obtained: an external primary source for "trivial cycle holonomy ⟺ existence
of a global potential" (Bandeira–Singer–Spielman 2013 arXiv:1204.3873 and Singer–Wu arXiv:1102.0075
were fetched; neither states the definition in the form I recalled). I therefore make no external
attribution claim, and the strawman rebuttal in §4 rests entirely on repository passages I read
directly.

STATUS: COMPLETE
