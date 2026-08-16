# Skeptic adjudication: W4-P4-High-1-blindness

STATUS: COMPLETE

- Target finding: `W4-P4-High-1-blindness`, stated severity **High**
- Finding text: `docs/reviews/2026-08-15-deep-review/findings/P4-gauge-holonomy.md:33-77`
- Location under attack: `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md`
  §7 (lines 381-463); `claim-ledger.json` `HOLONOMY-BLIND-FULL-LAW` (:399-416) and
  `ASM-HOLONOMY-BLIND-DATA` (:42-44)
- Revision: `8ce635807a6ca2a388255fc996c98f7c535e5843`, branch `review/2026-08-15-deep-review`
- Executed artifact: `docs/reviews/2026-08-15-deep-review/findings/V-W4-P4-High-1-check.py`

## VERDICT: UPHELD_REDUCED — correct severity **Medium**, and it must NOT be counted as a second Medium alongside P4-High-2

The isotropy specialization the finding rests on is correct; I reconstructed it symbolically and then
verified it on two exhibited finite models. At an admitted isotropy arrow, (7.2)/(7.3) *are* the
assumption that the fine laws are invariant, and the same-slice conclusion in (7.5) is that assumption
carried through an assumed-equivariant kernel in one substitution. The configuration a gauge reader
hears in the word "blind" — the parent fails to register a motion the fine level registers — is not a
consequence of (7.1)-(7.6) and cannot be witnessed by any datum admitted under
`ASM-HOLONOMY-BLIND-DATA`. That much survives every attack I could mount, including my own exhibited
counter-datum.

Three things do not survive.

1. **The finding's own remedy is wrong on the mathematics.** Fix 2 asserts the erasure theorem "is
   strictly not implied by (7.1)-(7.6)". It is the `T_A^g = id` instance of the identity §7 *itself
   displays* at lines 443-445, provable from (7.4) alone with no hypothesis on `Π_I` or `Q_I`
   (§2 below, check C1). The package therefore already carries the erasure statement as an
   unhighlighted specialization; what it lacks is the corollary's *name*, not its proof.
2. **The title overstates the exclusion.** Erasing channels are *not* excluded by
   `ASM-HOLONOMY-BLIND-DATA` — I exhibit an admitted datum whose channel destroys a fine coordinate
   outright (§3). What is excluded is a *witness*: an admitted arrow at which the fine law moves and
   the parent law does not. And in exactly that sub-case (`T_A^g = id`), §7's stated same-slice
   conclusion `(T_A^g)_#Π_A = Π_A` degenerates to `id_# Π_A = Π_A`, a tautology.
3. **High is not supportable.** No statement in the package is false, no inference fails, and every
   prose restatement — `direct-derivation.md:459`, `:496`, ledger `:400`, `problem-contract.json:51`,
   `Theory/SPEC.md:822-826`, `Theory/appendix_claim_ledger.tex:208-212`, `final-report.md:40` — states
   the content conditionally and accurately. The loose noun lives in the §7 heading, the phrase
   "holonomy-blind covariance theorem" at `:463`, and the claim/assumption ids.

**Corrected finding statement.** §7's branch name asserts erasure ("blind", contrasted at `:461` with
"exact retention" and listed alongside "quotient by conjugacy, averaged group element, path erasure")
while the theorem delivers inherited invariance: at an admitted isotropy arrow the fine laws are
*assumed* invariant by (7.2)/(7.3), and (7.5) restates that assumption downstream of an
assumed-equivariant channel. No admitted datum can exhibit a fine motion the parent misses. Severity
**Medium**: a naming/scope-description defect in a certified target conjunct and in an
`\status{ESTABLISHED}` manuscript paragraph (`Theory/07b:1787-1810`), invalidating no mathematics.

---

## 1. Relation to P4-High-2 (already reduced to Medium in wave 2) — SAME LABEL, DIFFERENT WORD, ONE FIX

Per my brief I must say this explicitly. **This is not the same defect restated, but it is the second
half of the same defective label, and the two must be reported as one finding and counted once.**

- P4-High-2 attacks **"holonomy"**: §7 has no connection, no transport, no loop, no curvature; the
  name was inherited from `thm:cg-holonomy-kl-marginal`, whose acting group `𝔥_I^x(r)` is a genuine
  based-loop transport group, and silently widened to an unrestricted groupoid.
- W4-P4-High-1 attacks **"blind"**: nothing is erased; the invariance is assumed upstream.

They are logically independent — repairing either leaves the other standing ("blind covariance
theorem" and "holonomy-inherited-invariance theorem" are both still wrong) — but they are defects of
*one string* in *three places* (§7 heading, `:463`, the two ids), repaired by *one rename*.
P4's own Medium "the dichotomy is not a dichotomy" (`P4-gauge-holonomy.md:104-116`) is a third facet
of the same string.

One provenance difference is worth recording because it cuts slightly *against* the package.
`git log -S"holonomy-blind"` shows "holonomy" is inherited vocabulary but **"blind" is coined by this
work**: it first appears in `docs/derivations/2026-08-15-full-pointwise-meta-agent/` at `ceffda2`
("docs: plan full meta-agent construction") and enters the manuscript at `b9ba51f` (`Theory/07b:1790`,
`:1808`). `grep -rn "blind" Theory/` returns only those two lines plus `SPEC.md:822,825`,
`appendix_claim_ledger.tex:208,212` and one unrelated "phase-blind" at `07b:625`. So unlike
"holonomy", "blind" is not a legacy term being widened; it is a new term introduced without a
definition anywhere in the package, whose only operative gloss is by contrast at `:461`.

**Recommendation for the final report:** merge into a single Medium finding, "§7's branch label
`holonomy-blind` misdescribes on both words", with P4-High-2's structural half and this finding's
inheritance half as its two components. Do not tally two Mediums.

## 2. My reconstruction: the pushforward step is immediate, and it never touches (7.2)/(7.3)

I re-derived §7's load-bearing step without reading either party's prose. For measurable `D ⊆ Z_A'`
and *any* law `μ` on `Y_I`, using only the intertwining (7.4)
`C_A'(T_I^g Y, D) = C_A(Y, (T_A^g)^{-1} D)`:

    [(T_A^g)_#(μ C_A)](D) = (μ C_A)((T_A^g)^{-1} D)
                          = ∫ C_A(Y, (T_A^g)^{-1} D) μ(dY)
                          = ∫ C_A'(T_I^g Y, D) μ(dY)
                          = ∫ C_A'(Y', D) [(T_I^g)_#μ](dY')
                          = ([(T_I^g)_#μ] C_A')(D).                                      (*)

`(*)` is an identity in `μ`. It agrees with the investigator's reconstruction and with the wave-2
skeptic's, and with the document's own displayed line (`:443-445`), whose *first* equality is exactly
`(*)` and whose *second* equality is the sole use of (7.2).

Executed confirmation (`V-W4-P4-High-1-check.py`, check C1, on the investigator's parity model
`C_A(y)=δ_{y₁⊕y₂}`, `T_I(y)=(1⊕y₁,y₂)`, `T_A(z)=1⊕z`):

    (7.4) holds with BOTH actions nontrivial: True
    C1  max |(T_A)_#(mu C_A) - [(T_I)_#mu] C_A'| over 2000 random mu : 0.0

**Isotropy specialization.** For `g:(o,X)→(o,X)` with source and target identified, the version
family is indexed by the object, so `Π'_{I,o',X'} = Π_{I,o,X}` and `C_A' = C_A`. Then (7.2)/(7.3) read

    (T_I^g)_# Π_{I,o,X} = Π_{I,o,X},        (T_I^g)_# Q_{I,o,X} = Q_{I,o,X},

and `(*)` gives `(T_A^g)_# Π_{A,o,X} = Π_{A,o,X}` immediately. Executed (check C2):

    C2  (7.2) at the isotropy arrow, (T_I)_#Pi_I == Pi_I : True     <-- fine-level invariance, assumed
        conclusion (7.5), (T_A)_#Pi_A == Pi_A            : True     <-- inherited in one substitution
        drop (7.2): mu = delta_(0,0), (T_A)_#(mu C_A) == mu C_A ? False

So the same-slice conclusion is the same-slice hypothesis moved through an equivariant kernel, and it
fails the moment the fine hypothesis is dropped. **The finding's central reconstruction is correct.**

The one genuinely non-immediate ingredient in §7 is the *selected-version* qualification, and the
document flags it rather than gliding past it (`:424`: "almost-sure uniqueness of regular conditionals
does not choose covariant null-slice values automatically"). That honesty is why this is a naming
defect and not a proof gap.

## 3. Where the finding overreaches: erasing channels ARE admitted, and the erasure theorem IS in §7

**(a) The hypotheses do not exclude erasure.** Take `Y_I = {0,1}²`, `Z_A = {0,1}`,
`C_A(y,·) = δ_{y₁}` (destroys `y₂` outright), `T_I(y) = (y₁, 1⊕y₂)`, `T_A = id`. Then (7.4) holds
(check C3: `True`), and with `Π_I = Q_I =` uniform on `{0,1}²` the fine laws are `T_I`-invariant, so
(7.2)/(7.3) hold. This datum satisfies `ASM-HOLONOMY-BLIND-DATA` with a maximally lossy channel. The
finding's title ("the hypotheses exclude the only case in which blind would carry content") is
therefore imprecise: what is excluded is a *witness of the loss at the level of the laws*, not lossy
channels.

**(b) In precisely the erasure configuration, §7's stated conclusion is a tautology.** For that datum
`T_A = id`, so (7.5) same-slice reads `id_# Π_A = Π_A`. All the content sits upstream in `(*)`, which
§7 does not isolate. This *sharpens* the finding rather than killing it, and should replace the
title's claim.

**(c) The finding's Fix 2 is wrong.** It proposes adding "if `C_A(T_I^g Y, D) = C_A(Y, D)` for all
`Y,D` then `[(T_I^g)_#μ]C_A = μC_A` for every fine law `μ`" and asserts this "is strictly not implied
by (7.1)-(7.6)". Set `T_A^g = id` and `C_A' = C_A` in (7.4): the hypothesis becomes exactly channel
invariance and `(*)` becomes exactly the conclusion. The proposed theorem is a one-substitution
instance of the package's own displayed computation. Executed on the erasure datum with a
*non-invariant* fine law (check C3):

    fine law NOT invariant:  (T_I)_#mu == mu ? False
    parent law IS blind:     [(T_I)_#mu] C_A == mu C_A ? True
    erasure holds for EVERY mu, max deviation over 2000 random mu : 0.0

and the same datum with `μ = δ_{(0,0)}` fails (7.2), confirming it is outside the certified branch:

    (7.2) demands fine invariance. For mu = delta_(0,0) this FAILS: False
      -> the datum is EXCLUDED from the certified branch.

So the correct statement is: **the package proves the erasure fact and never names it, while naming
"blindness" after the case in which nothing is erased.** That is a labeling inversion, and it is
cheaper to fix than the finding claims — one sentence, not a new theorem.

## 4. The kills I tried and could not land

**Attack A — "blind" is a declared internal term meaning "invariant", so the investigator misread.**
Fails. `problem-contract.json:51-52` and `Theory/SPEC.md:822-826` do use "holonomy-blind invariance"
to mean invariance under the declared action, and the ancestor `Theory/06:571-580` defines
`𝒬_{I,fix}^x(r) = {Q : (H)_#Q = Q ∀H ∈ 𝔥_I^x(r)}`, so "stabilized/fixed" is the program's established
notion. But (i) `blind` is nowhere *defined* in the package (§1, git provenance), and (ii) the
document's own contrast defeats the reading: `:461` — "The alternative is **exact retention rather
than blindness** … No quotient by conjugacy, averaged group element, path erasure, or holonomy-blind
invariance is asserted" — puts `holonomy-blind invariance` in a list of three erasure operations and
opposes the branch to retention. `:463` repeats it: "either it invokes the holonomy-blind covariance
theorem …, or it **retains the raw records** and declines a blindness claim." An opposition between
keeping and losing information is the erasure reading, asserted by the package itself. The escape is
unavailable.

**Attack B — the hypothesis is stated elsewhere in the package, so the criticism is a misread.** I
searched the problem contract, the claim ledger, the notation standard, the four domain reviews, the
independent reconstruction, and the oracle-erasure record. Every one of them restates the branch
correctly and none of them states the inheritance observation. Closest is
`evidence/oracle-erasure.md:18` — "The holonomy-blind premises state fine-law covariance … not parent
covariance. The parent conclusion still requires pushing those identities through the defining
integrals." That is the package's *defense* of nontriviality, and `(*)` shows the push is one change
of variables. `view-gauge-holonomy.md:57` grades "Covariance versus same-slice stabilizer invariance"
`EVIDENCE_VERIFIED` on the basis of "Source/target groupoid typing and isotropy restriction" — i.e.
the domain reviewer certified the restriction without remarking that the restriction is what makes the
statement inherited.

**Attack C — the package's own adversarial suite already answers this.** It does not.
`adversarial-attacks.md:70-92` runs A9 (marginal/full-law confusion), A10 (trivial holonomy ⇒
agreement), A11 (erased marks). None asks whether the blindness branch can exhibit blindness. Worse
for the package, A11's response (`:90`, and `adversarial-report.json:140`) reads "If a construction
erases them, it must instead satisfy every blindness/covariance hypothesis or decline both claims" —
routing erasing channels to the blindness branch, which is the erasure connotation operating inside
the certification record. The disjunction is not false (declining is permitted, and §3(a) shows some
erasing channels do satisfy the hypotheses), so this does not make anything wrong; it does show the
misleading reading is live inside the frozen bytes and not merely in an outside reader's ear.

**Attack D — the counterexample is asserted, not exhibited.** Inapplicable, and I closed the gap
anyway: the finding's "falsifier" paragraph reasons correctly but exhibits nothing. §3 above supplies
both an admitted erasing datum and an excluded blindness witness, executed.

**Attack E — severity is the whole finding.** Partly lands; see §5.

## 5. Severity

`High` is not supported, for the reasons wave 2 applied to P4-High-2 and which apply verbatim here.

1. **Nothing is false.** (7.1)-(7.6) are hypotheses on supplied data; (7.5) follows; `:459` fences the
   same-slice case explicitly ("isotropy arrows that fix the declared `X` and admitted `o`,
   **preserve the selected versions**, and identify the source and target spaces" — that clause *is*
   the fine-invariance hypothesis, stated in the derivation).
2. **Every prose restatement is accurate.** `:496` — "Section 7 proves **full-law covariance** under
   the complete joint hypotheses"; ledger `:400` — "…laws are covariant; same-slice invariance follows
   only on the fixed-`(o,X)` stabilizer"; `final-report.md:40` — "Holonomy blindness is a full-law
   statement under explicit action/version/evaluator hypotheses." The word "blind" never appears in a
   sentence that misstates the content; it appears in labels and in the `:461`/`:463` contrast.
3. **Nothing downstream leans on the erasure reading.** `grep -rniE "cannot detect|does not see|
   unable to distinguish|erase|erasure|indistinguishable"` over the package returns only the oracle-
   erasure audit artifact, A11, and the retention paragraph. No flatness, path-independence, or
   information-loss conclusion is drawn from §7 anywhere in `Theory/` or `docs/derivations/`.

What keeps it above `Low`, exactly as for P4-High-2: the label sits inside a certified target conjunct
with ledger state `EVIDENCE_VERIFIED`, and has been copied into the manuscript at `Theory/07b:1790`,
`:1808` under `\status{ESTABLISHED}`. A newly coined term whose plain reading is contradicted by the
theorem it names, inside a document certified `COMPLETE_AFFIRMATIVE`, is a real and cheap-to-fix
scope-description defect. **Medium** — merged with P4-High-2, not additional to it.

## 6. Relation to the principal reviewer's notes

No contradiction. `P0-principal-reviewer-notes.md` reconstructs statement 1, the KL chain, the
recovery theorem, and the operational package; it does not reconstruct §7, and at `:257` it records
the panel's §7 concern approvingly without independently adjudicating it. P0's post-wave-2 correction
(`:228-252`) also establishes the precedent I am following: a defect that touches labels and framing
rather than mathematics gets graded on what it invalidates, and P0 reduced its own High to Low on
exactly that reasoning.

## 7. Correct minimal repair (replacing the finding's Fix)

1. Rename the branch and both ids: `HOLONOMY-BLIND-FULL-LAW` → `PARENT-COVARIANCE-EQUIVARIANT-CHANNEL`,
   `ASM-HOLONOMY-BLIND-DATA` → `ASM-PARENT-COVARIANCE-DATA`; §7 heading and `:463` phrase → "typed
   covariance / inherited-invariance theorem". This is the same edit that repairs P4-High-2.
2. One sentence after `:459`: *at an isotropy arrow (7.2)/(7.3) assert invariance of the fine laws, so
   the same-slice conclusion is inherited invariance, not an erasure statement.*
3. One sentence after `:445` naming the `T_A^g = id` specialization of the displayed identity: *when
   `T_A^g = id`, (7.4) is channel invariance and the same computation gives `[(T_I^g)_#μ]C_A = μC_A`
   for every fine law `μ`, with no hypothesis on `Π_I` or `Q_I` — this, not (7.5), is the statement
   that the parent cannot register the motion.*
4. Rewrite `:461`/`:463` so the two branches are not opposed as keeping-versus-losing (this is P4's
   separate Medium; the same edit closes it).

## FALSIFIER OF MY OWN ATTACK

Primary: exhibit a reading on which `Π'_{I,o',X'} ≠ Π_{I,o,X}` at an arrow `g:(o,X)→(o,X)` — i.e. a
place in the frozen bytes where the selected-version family is indexed by *arrows* or by a groupoid
object carrying more than `(o,X)` with distinct declared versions, so that (7.2) at an isotropy arrow
is a covariance condition rather than an invariance assumption. Then the same-slice conclusion would
not be inherited and the finding's core would fail, taking my UPHELD half with it. I checked `:385`
("arrows `g:(o,X)→(o',X')`"), `:404` (`Π_{I,o,X}` indexed by the slice), `:424`, `:459`
("preserve the selected versions"), `claim-ledger.json:42-44`, and `evidence/notation-standard.md`,
and found the family indexed by `(o,X)` throughout, with no arrow-dependent version.

Secondary, for my reduction to Medium: if this review's rubric grades "a certified conjunct whose name
asserts the opposite of what it proves" as High, my reduction is a rubric disagreement rather than an
evidentiary one, and the finding stands at High — but even then it must be merged with P4-High-2 and
the merged finding graded once.

Tertiary, for my §3 refutation: if the intended meaning of (7.4) is the manuscript's symmetric form
`C_A(g·Y, g·D) = C_A(Y,D)` (`Theory/07b`, `eq:rg-pointwise-parent-holonomy-channel`) under a
*declared* action for which `T_A^g = id` is not an admitted arrow type, then the `T_A^g = id`
specialization would be outside the schema and the finding's "the package never states it" would be
correct. I read `:1790-1802` and the surrounding paragraph: the actions are supplied as data with no
faithfulness or nontriviality requirement on the `Z_A` action, so `T_A^g = id` is admitted.

## Sources / artifacts checked

- `evidence/direct-derivation.md:381-463`, `:492-500` (read in full)
- `claim-ledger.json:42-44`, `:399-449`; `problem-contract.json:51-54`;
  `construction-or-strongest-theorem.md:94`
- `evidence/adversarial-attacks.md:70-92`; `adversarial-report.json:134-141`;
  `evidence/oracle-erasure.md:18,30`; `evidence/independent-reconstruction.md:52-54`;
  `evidence/reviews/view-gauge-holonomy.md:54-57,135,143,147,173`
- `Theory/06_general_coarsegraining.tex:556-610` (ancestor `𝔥_I^x(r)`, `𝒬_{I,fix}^x(r)`,
  `thm:cg-holonomy-kl-marginal`); `Theory/07b_agent_network_rg.tex:1787-1810`;
  `Theory/SPEC.md:815-830`; `Theory/appendix_claim_ledger.tex:200-216`
- `git log -S"holonomy-blind"` over `Theory/07b_agent_network_rg.tex` and `docs/`
- Executed: `docs/reviews/2026-08-15-deep-review/findings/V-W4-P4-High-1-check.py` (checks C1/C2/C3;
  output quoted verbatim in §2-§3)
- Prior adjudication read in full: `V-P4-High-2-not-holonomy.md`; `P0-principal-reviewer-notes.md`
