STATUS: COMPLETE
ROLE: adversarial skeptic (wave 2)
TARGET FINDING: `P10-High-2-established-no-proof` (P10-rigor-sweep.md, block at line 266)
REVIEW TARGET REVISION: 8ce635807a6ca2a388255fc996c98f7c535e5843
WORKING REVISION: 429a75642ed3d2a58f9a1cfeccf4281eb8a14a42 (`git diff --stat 8ce6358 HEAD -- Theory/ docs/theory-provenance.md solid_RG_theory.md overview.md` is empty, so every file quoted below is byte-identical to the target)

# Verdict: UPHELD_REDUCED — real defect, correct severity is Medium, not High

The finding's mechanical core is true and I reproduced it independently. Its headline clause —
"has no proof anywhere in `Theory/`" — is false, and its characterization "a reader of the
manuscript alone has an ESTABLISHED theorem with zero justification" overstates the state of the
manuscript. What survives is a broken audit trail on a theorem that is in fact proved in the same
document, which is a presentational/spec-compliance defect, not a proof gap.

The defense my brief told me to test (that the repo's convention makes ESTABLISHED mean "proved in
the hash-bound derivation package and cited from the manuscript", so a pointer to
`docs/derivations/` would be conforming) fails outright, and fails twice. It is dismissed in §3.

---

## 1. What I verified mechanically (the finding's factual core: TRUE)

**1.1 The theorem carries `\status{ESTABLISHED}` and has no proof block.** `Theory/07b_agent_network_rg.tex:76`
opens `\theoremheading{Full pointwise probabilistic datum for a candidate parent}{thm:rg-pointwise-parent-datum}`;
the statement runs to line 178 ending `...neither the zero-defect criterion nor a recovery
consequence. \status{ESTABLISHED}`, then `\medskip`, then a `\status{NOT-CLAIMED}` remark
(179–185), then `\section{The exact effective likelihood and action}` at 187. No `\paragraph{Proof.}`,
no `\emph{Proof.}`, no `$\square$`.

**1.2 The block contains no cross-reference of any kind.** This is stronger than what the finding
claimed and I checked it directly:

```
$ sed -n '76,186p' Theory/07b_agent_network_rg.tex | grep -n "Cref\|ref{"
99:\eqref{eq:rg-pointwise-parent-defect} agree $\mathbb Q_{A,o,X}$-almost surely. Finite fine KL is
```

The single hit is a self-reference to the theorem's own equation. Zero `\Cref` out of the block.
So under *either* candidate convention, the second disjunct of ESTABLISHED ("cited to a source")
is unsatisfied — there is nothing to resolve, conforming or not.

**1.3 It is the sole such statement in the compiled manuscript, and the only `thm:` in that
condition.** I wrote a script that maps every `\theoremheading`/`\propositionheading`/
`\corollaryheading`/`\lemmaheading` in all `\input`-ed chapters (`PIFB2.tex` and `main.tex`
excluded; `PIFB2.tex` is not in `main.tex`) to the proof markers occurring before the next heading
or `\section`. Executed output:

```
$ python scratchpad/proofmap_all.py
total headings (theorem/prop/cor/lem): 234
headings with no proof marker before next heading/section: 9
  05_elbo.tex                          524  prop:elbo-exact-m-coordinate
  05_elbo.tex                          590  prop:elbo-evidence-monotonicity
  05d_relational_inference.tex        1588  cor:hist-retained-vfe-selection-descent
  05d_relational_inference.tex        1628  prop:hist-declared-block-quotient-boundary
  05d_relational_inference.tex        2493  prop:hist-noncollapse
  06_gaussian.tex                      291  cor:gauss-invertible-gain-factor
  07_restrictions.tex                  276  cor:restrict-mean-cost-data
  07b_agent_network_rg.tex              76  thm:rg-pointwise-parent-datum
  11_obstructions.tex                   57  cor:obs-flat-fold-singular
```

Eight of the nine are `prop:`/`cor:`. I read two of them for calibration and the manuscript's
practice for an unlabeled justification is unambiguous: the argument is written into the statement
body with explicit cross-references. `prop:elbo-evidence-monotonicity` (05:590) ends "The first
inequality is `\Cref{thm:elbo-extended-gap}` at \(\theta^{\mathrm{new}}\), the second is
\eqref{eq:elbo-acceptance}, and the final equality is the zero-gap case..."; `cor:obs-flat-fold-singular`
(11:57) is a one-substitution consequence of the lemma proved immediately above it.
`thm:rg-pointwise-parent-datum` does neither. Within `07b` alone the count is exact: 29 headings,
29 proof markers, and the only heading whose block contains none is line 76.

That is the sharpest true form of the finding, and it is sharper than the count the investigator
reported (they compared 13 `\theoremheading`s against 29 proof markers, which is apples to oranges —
29 is the count of *all* heading classes).

## 2. Where the finding is wrong: the mathematics is proved in `Theory/`

The finding's title clause and its "zero justification" sentence do not survive. Every load-bearing
assertion inside 07b:76–178 is a typed specialization of a result proved, with `$\square$`, inside
`Theory/`. I reconstructed the central one myself rather than taking either party's word.

**2.1 The KL chain and the defect (07b:156–170) are `thm:rg-exact-coarse-vfe`, proved ten lines
above the disputed theorem.** 07b:34–57 states, for a fixed joint \(P\), posterior \(\Pi_o\),
recognition \(Q_o\ll\Pi_o\) and a channel \(C:\mathsf Y\rightsquigarrow\mathsf Z\) that does not
read \(Q_o\) and does not touch \(o\), with lifts \(\widehat Q_o=Q_o\otimes C\),
\(\widehat\Pi_o=\Pi_o\otimes C\),

\[
\Fenergy_P(Q_o)=\Fenergy_{P^c}(Q_o^c)+\int_{\mathsf Z}\KL\bigl(\widehat Q_o(dy\mid z)\Vert\widehat\Pi_o(dy\mid z)\bigr)Q_o^c(dz),
\]

and 07b:59–66 proves it. Substituting \((\mathsf Y,\mathsf Z,C,Q_o,\Pi_o)\mapsto(\mathsf Y_I,\mathsf Z_A,C_A,\mathbb Q_{I,o,X},\boldsymbol\Pi_{I,o,X})\)
and carrying the fixed structural parameter \(X\) along gives
\eqref{eq:rg-pointwise-parent-kl-chain}–\eqref{eq:rg-pointwise-parent-defect} verbatim. My own
reconstruction of the underlying step, done independently: for bounded \(\phi\),
\(\int\phi\,d\widehat{\mathbb Q}=\iint\phi(Y,z)C_A(Y,dz)r(Y)\boldsymbol\Pi_I(dY)=\int\phi r\,d\widehat{\boldsymbol\Pi}\)
with \(r=d\mathbb Q_I/d\boldsymbol\Pi_I\), so \(d\widehat{\mathbb Q}/d\widehat{\boldsymbol\Pi}=r(Y)\)
and \(\KL(\widehat{\mathbb Q}\Vert\widehat{\boldsymbol\Pi})=\int r\log r\,d\boldsymbol\Pi_I=\KL(\mathbb Q_I\Vert\boldsymbol\Pi_I)\)
because \(C_A(Y,\mathsf Z_A)=1\); disintegrating the lifts over \(z\), whose marginals are
\(\mathbb Q_{A,o,X}\) and \(\boldsymbol\Pi_{A,o,X}\), and applying the relative-entropy chain rule on
a standard Borel product splits it, everything in \([0,+\infty]\). This agrees with the principal
reviewer's reconstruction (P0, "Verified: the additive KL chain and the defect") and with P10's own
`[Low]` finding at line 329. No contradiction with P0 anywhere in this attack.

**2.2 Normalization, the unchanged observation marginal, and the selected parent posterior version
(07b:105–116) are proved in `Theory/06`.** `thm:cg-evidence-preserving-channel` (06:258–284) is
proved at 06:286–302 by a \(\pi\)–\(\lambda\) extension, and the paragraph "Pointwise parent
specialization" (06:304–331) writes the specialization in the disputed theorem's own notation,
displays the defining test-function identity \eqref{eq:cg-pointwise-parent-posterior-test}, says
"This is a typed specialization of the preceding theorem, not a second posterior-pushforward
theorem", and closes with "The associated KL/VFE loss is the common-channel chain rule of
`\Cref{thm:rg-exact-coarse-vfe}`, specialized in `\Cref{thm:rg-pointwise-parent-datum}`."

**2.3 The "stated two-way pairwise common-recovery equivalence" (07b:175–177) is proved in
`Theory/06`.** `thm:cg-dpi-equality` (06:85–122, proved, cited to Kullback 1951 and Csiszár 1967)
plus `cor:cg-pairwise-bayes-recovery` (06:124–140, proved both directions) plus
`cor:cg-dpi-infinite-equality-warning` (06:142–152, proved by an explicit three-point counterexample)
are exactly the pairwise recovery equivalence and exactly the reason 07b:177 says a bare
\(+\infty=+\infty\) yields no recovery consequence. 06:154–165 supplies the family-wide caveat
07b:176 repeats.

**2.4 Absolute continuity and marginal non-determination have proved homes too.**
`prop:prob-density-absolute-continuity` (03:363–376, proved) plus the pushforward density
computation inside the proof of `thm:cg-kl-dpi-extended` (06:74–82) cover
\(\mathbb Q_{A}\ll\boldsymbol\Pi_A\); `prop:prob-marginals-do-not-determine-joint` (03:433–437,
proved by a two-dimensional Gaussian correlation witness) covers 07b:151. Standard-Borel
disintegration, used for the induced evaluator tier at 07b:127–135, is the fact the manuscript
already leans on globally (e.g. 03:181, 06:132, 07b:62).

So the correct statement is: **the theorem is proved in the manuscript, in four different places,
and the manuscript never says so at the point of claim.** The finding conceded "partially in
`Theory/06`" and then discounted it; the concession is larger than the finding allows.

## 3. Why the defense in my brief fails (this is what keeps the finding alive at all)

The hypothesized convention — ESTABLISHED = proved in the hash-bound derivation package, cited from
the manuscript — is not this repo's manuscript convention, and adopting it would make the manuscript
*more* nonconforming, not less.

- **`Theory/SPEC.md:69–71`, the authoring authority:** "`ESTABLISHED` | Proved here, or a standard
  result cited to a source that has been checked. | **Give the proof or the citation.**"
  `SPEC.md:108`: "Established theorems remain at their proofs." `SPEC.md:58`: the tag goes
  "immediately after the statement it governs".
- **`Theory/01_introduction.tex:167`**, the promise actually printed to the reader, is required by
  SPEC §2.1 to be word-for-word identical and is: "`ESTABLISHED` & Proved here, or a standard result
  cited to a source that has been checked."
- **`Theory/SPEC.md:27–30` forbids the escape hatch:** "The executable does not appear... no
  line-number citations to any repository. Nothing in this document is a report on a prior
  manuscript. **It stands alone.**" A pointer from `07b` to `docs/derivations/` would itself violate
  the spec. Consistent with that, `grep -rn "derivations" Theory/*.tex` returns no reference to
  `docs/derivations/` from any in-scope chapter.
- **`solid_RG_theory.md:16` is a different vocabulary, and says so:** "ESTABLISHED means proved in
  the contained package or in the cited canonical theorem source... **The manuscript status of the
  full datum is ESTABLISHED.** Its release metadata records ledger state `EVIDENCE_VERIFIED`..."
  That sentence separates the manuscript status from the package ledger state rather than deriving
  one from the other. `Theory/appendix_claim_ledger.tex:187–215` does the same and supplies no proof
  location either — it restates the theorem and asserts the status.
- **The binding is absent in both directions.** `grep -rln "rg-pointwise-parent-datum" docs/` matches
  only wave-1 review files, never the derivation package; and the package title "Full pointwise
  probabilistic datum" appears in `Theory/`, `overview.md`, and review files but not inside
  `docs/derivations/2026-08-15-full-pointwise-meta-agent/`. There is no cross-link to declare
  conforming or nonconforming.

So the finding is not killed by convention. An obligation the manuscript itself prints to its
readers is unmet, on the theorem the 8/15 release is built around.

## 4. Why the severity is Medium, not High

In a rigor review of a theory manuscript, High should mark "the claim may be false, or its proof is
missing from the corpus." Neither holds. The mathematics is correct (my §2.1 reconstruction; P0's
independent reconstruction; P10's own `[Low]` block at 329–372), it is proved inside `Theory/`, and
the repair is the five-line proof paragraph plus two `\Cref`s that the investigator already drafted.
What remains is a spec violation and a broken audit trail: the reader cannot get from the claim to
its warrant. That is a real must-fix defect on a headline claim in a document whose SPEC calls
status legibility its central discipline — which is why it is Medium and not Low — but it is not a
proof gap, and reporting it as one misstates the manuscript's actual condition in a review whose
whole purpose is to state that condition accurately.

Corrected finding text I would accept:

> **[Medium]** `thm:rg-pointwise-parent-datum` (07b:76–178) carries `\status{ESTABLISHED}` with
> neither a proof block nor a single cross-reference in its statement block — the only one of 234
> formal statements in the compiled manuscript in that condition, and the only `thm:`-class
> statement among the nine that lack a labeled proof. Its constituents are proved in `Theory/`
> (07b:34–66; 06:258–331; 06:65–165; 03:363–437), so this is a missing local discharge, not a proof
> gap. Under `SPEC.md:71` and `01_introduction.tex:167` the obligation is "give the proof or the
> citation", and `SPEC.md:27–30` forbids discharging it by pointing at `docs/derivations/`; the
> repair must therefore be internal.

## 5. Spun-off defect found while attacking (separate, Low, mine not the investigator's)

The missing assembly had one concrete cost. 07b:151 states flatly "No displayed marginal pair
reconstructs any of the corresponding full laws," with no nondegeneracy hypothesis, inside the
ESTABLISHED block. The result it silently specializes,
`prop:prob-marginals-do-not-determine-joint` (03:433–437), carries the hypothesis "at least two
nondegenerate real coordinates" and states the exception explicitly: "Without it the conclusion can
fail: for one agent and one design point with \(\mathsf K_{i,a}=\mathsf M_{i,a}=\{0\}\), the space
\(\mathsf Y_D\) is a singleton and its unique law is determined by its marginals."

Counterexample within 07b's own stated premises, which require only that the factors be *nonempty*
standard Borel (07b:84–89): take \(\mathsf B_A=\mathsf M_A=\boldsymbol\Xi_A=\mathsf H_A=\{*\}\), so
\(\mathsf Z_A\) is a one-point standard Borel space; take \(C_A(Y,\cdot)=\delta_*\), which is
normalized, measurable and recognition-independent; take \(\mathbb Q_{I,o,X}=\boldsymbol\Pi_{I,o,X}\)
so \(\mathbb Q_I\ll\boldsymbol\Pi_I\). Then \(\mathbb Q_{A,o,X}=\delta_*\) is the unique probability
measure on \(\mathsf Z_A\), and the displayed pair \((q_A^b,q_A^m)=(\delta_*,\delta_*)\) determines
it. Every premise of the theorem holds and the sentence is false. The same over-general wording has
already propagated to `appendix_claim_ledger.tex:197–198` and `appendix_notation.tex:58`. Fix:
add the nondegeneracy hypothesis and cite `\Cref{prop:prob-marginals-do-not-determine-joint}`.
This is a hypothesis-omission defect of its own; I do not count it as evidence for High on the
finding under attack.

## 6. Relation to the principal reviewer's notes

No contradiction. P0 reconstructed the parent posterior version, parent absolute continuity, the
additive KL chain with its defect, and the recovery theorem, and recorded all of them as CHECKS OUT
and classical. My §2.1 is an independent reconstruction of the same chain and agrees. P0's live
issue — novelty and certification language, not correctness — is orthogonal to this finding and is
carried by P5/P8/P9. Nothing in this attack rests on agreement with P0; §2.1 was derived before
comparing.

## Falsifier of my own attack

Two things would overturn this verdict in opposite directions.

- **Toward REFUTED:** a documented rule in this repo saying ESTABLISHED is discharged by the
  mathematics existing anywhere in the corpus, with no local proof or citation required. I searched
  `SPEC.md` for `specializ|restate|reprove|proof.*omitted|without proof` and found no such
  exemption, and `SPEC.md:108` says the opposite. Produce that rule and the finding dies.
- **Toward the original High:** exhibit any assertion inside 07b:76–178 that is *not* a typed
  specialization of `03:363–437`, `06:65–165`, `06:258–331`, or `07b:34–66`, and that is not proved
  anywhere else in `Theory/` — i.e. a component whose truth is actually open. I checked
  normalization, the observation marginal, the selected posterior version, \(\mathbb Q_A\ll\boldsymbol\Pi_A\),
  the KL chain, \(\Delta_A\ge0\), the zero-defect criterion, the finiteness fence, the recovery
  equivalence, evaluator existence, and the marginal claim; the last one is defective for a
  different reason (§5, dropped hypothesis) and the rest are all covered. Find an eleventh
  assertion that is not, and High is correct.

Scripts used (kept out of the repo): `scratchpad/proofmap.py`, `scratchpad/proofmap_all.py`.
