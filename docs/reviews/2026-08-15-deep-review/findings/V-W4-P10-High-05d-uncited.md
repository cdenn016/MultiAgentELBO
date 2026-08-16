# Skeptic attack: W4-P10-High-05d-uncited

STATUS: COMPLETE
AGENT: wave-4 adversarial skeptic
TARGET REVISION: `8ce635807a6ca2a388255fc996c98f7c535e5843`, branch `review/2026-08-15-deep-review`
FINDING UNDER ATTACK: P10 `[High]` "Six new ESTABLISHED theorems in 05d carry no citation, and three
of them are classical results restated" (`P10-rigor-sweep.md:153-206`)

## VERDICT: UPHELD_REDUCED

**A real defect exists, and it is exactly one item, not three, and not six.** The syntactic-monoid
universal property is restated at `05d:1082-1128` with no attribution anywhere a reader of the
manuscript can see, and the borrowed notation `Syn(Φ)` is used without saying whose it is. That
survives every attack I could mount and I concede it.

**Everything else in the finding fails.** The SPEC-conformance charge is refuted outright: SPEC's
`ESTABLISHED` obligation is disjunctive and seven of the eight new `ESTABLISHED` items carry complete
proofs in place. The circle-heat theorem is not a classical result restated — the word "Blackwell"
does not occur in its statement or its proof, the garbling condition is written out as an explicit
Markov-kernel condition and proved, and the theorem is a construction with an exhibited witness. The
compact-quotient theorem is not "a continuous bijection compact→Hausdorff applied to the
Myhill–Nerode quotient"; that is one of its three steps, and the finding exhibits no source for the
other two. The "presented as a new result of this program" framing is contradicted by the package's
own literature policy and is not supported by the overview or SPEC prose it cites.

**Corrected severity: Medium**, scope reduced from six theorems / three classical restatements to
**one** result, reclassified from a SPEC-conformance-plus-attribution defect to a pure attribution
defect.

Verification note: `git diff 8ce6358 HEAD -- Theory/05d_relational_inference.tex` is empty, so the
working-tree file I read is byte-identical to the reviewed file.

---

## Attack 1 — the SPEC-conformance charge. REFUTED.

The finding grounds High severity partly on `Theory/SPEC.md:70` ("ESTABLISHED ... obligation 'Give
the proof or the citation'"). I read SPEC.md:71 directly. The row is:

> | `ESTABLISHED` | Proved here, **or** a standard result cited to a source that has been checked. |
> Give the proof **or** the citation. A citation must be to a real source you have checked. |

The obligation is a disjunction, and the first disjunct is satisfied. The nine headings the 8/15
commit added to 05d (`git diff f655ba5 8ce6358 -- Theory/05d_relational_inference.tex |
grep -E '^\+.*heading'`), with status and proof presence checked line by line:

| line | label | status | proof in place |
|---|---|---|---|
| 1082 | `prop:hist-operational-quotient-universal-property` | ESTABLISHED | `\paragraph{Proof.}` 1115-1128, ends `\(\square\)` |
| 1130 | `thm:hist-compact-operational-quotient` | ESTABLISHED | 1148-1160, `\(\square\)` |
| 1319 | `def:hist-normalized-soft-intervention-monoid` | ESTABLISHED (tag at :1339, on a claim embedded in the definition) | **none** |
| 1341 | `thm:hist-soft-bsc-target-face-nonidentifiability` | ESTABLISHED | yes, `\(\square\)` |
| 1382 | `def:hist-affine-randomized-intervention-monoid` | DEFINITION | n/a |
| 1396 | `thm:hist-randomized-hard-intervention-nonidentifiability` | ESTABLISHED | yes, `\(\square\)` |
| 1426 | `prop:hist-standard-borel-intervention-semantics` | ESTABLISHED | yes, `\(\square\)` |
| 1450 | `cor:hist-compact-feller-operational-quotient` | ESTABLISHED | yes, `\(\square\)` |
| 1467 | `thm:hist-circle-heat-intervention-nonidentifiability` | ESTABLISHED | yes, `\(\square\)` |

Two corrections fall out. First, the count "six" is wrong in both directions: there are **eight**
new `ESTABLISHED` tags, not six, and **seven** of them discharge the SPEC obligation by proof.
Second, the one item that does not carry a proof paragraph — the compact-metrizable-topological-monoid
claim folded into `def:hist-normalized-soft-intervention-monoid:1334-1339` — is not among the three
the finding names, and P10 itself reconstructed it and recorded "Checks out" at `P10:255-259`.

So "carries no citation" is true and is **not a rule violation** for the seven proved items. The
finding's own concession ("I verified the mathematics: all three proofs are correct") already removes
correctness from the table; removing SPEC-conformance leaves attribution alone.

## Attack 2 — the citation practice is document-wide, not something the 8/15 commit changed. CONFIRMED.

`\cite*` counts over `Theory/*.tex`, executed:

```
0/205  01_introduction     2/772  02_geometry      3/483  03_probability   1/477  04_generative
6/660  05_elbo             3/393  05a_expfamily    1/783  05b              2/1393 05c
3/2837 05d                 4/372  06_gaussian      3/794  06_general_cg    1/308  06a
5/1170 07_general_renorm   4/438  07_restrictions  4/2981 07b              15/574 08_infogeometry
4/1065 09_coarsegraining  14/625  10_renormalization 2/422 11_obstructions 6/343  12_philosophy
101/3956 PIFB2
```

The formal development (05x, 06, 07b) runs at one to three citations per thousand lines throughout;
only the survey chapters cite densely. 05d at 3/2837 sits exactly on the house convention that
predates the commit. The 8/15 work did not introduce a citation practice; it wrote inside one. This
does not excuse the missing attribution for a named classical theorem, but it does remove "a
repository with 466 bib entries chose not to cite here" as an aggravating fact — the same is true of
every formal chapter.

I did verify the finding's grep: `Theory/references.bib` has 466 entries and contains no Myhill,
Nerode, Schützenberger, Eilenberg, Pin, or Blackwell. That part of the evidence stands.

## Attack 3 — is the universal property really the classical theorem? CONCEDED, and I re-derived it.

I reconstructed `prop:hist-operational-quotient-universal-property` from its statement rather than
adjudicating from P0's or P10's prose. With `a ∼_Φ b ⟺ Φ(uav)=Φ(ubv)` for all `u,v ∈ A`:

- *Equivalence*: equality of the family `(Φ(uav))_{u,v}`.
- *Congruence*: `Φ(u(xay)v) = Φ((ux)a(yv)) = Φ((ux)b(yv)) = Φ(u(xby)v)` by associativity alone.
- *Inside `ker Φ`*: take `u=v=1`.
- *Largest*: if `≈` is a congruence inside `ker Φ` and `a ≈ b`, then `uav ≈ ubv`, so
  `Φ(uav)=Φ(ubv)`, so `a ∼_Φ b`.
- *Factorization*: for surjective unital `q:A↠B` with `Φ=ψq`, `q(a)=q(b)` gives
  `q(uav)=q(u)q(a)q(v)=q(ubv)`, hence `Φ(uav)=ψq(uav)=ψq(ubv)=Φ(ubv)`, so `ker q ⊆ ∼_Φ`; therefore
  `h(q(a)) := π(a)` is well defined, unital, multiplicative, surjective, and unique with `hq=π`
  because `q` is onto; `Φ̄h q = Φ = ψq` and surjectivity of `q` give `Φ̄h=ψ`.
- *Finite minimality*: `h` onto gives `|B| ≥ |Syn(Φ)|`; finiteness plus equality gives bijectivity.

**No step uses anything about `Y`.** Setting `Y={0,1}` and `Φ=1_L` returns the textbook statement
verbatim, and setting `A=X^*` returns the free-monoid form. The transcription is exactly as the
finding says: nothing in the proof knows the codomain.

Source check (not from memory). Adámek, Milius and Urbat, *Syntactic Monoids in a Category*
(arXiv:1504.02694), rendered text: the syntactic congruence is "u∼v iff for all x,y∈X*: xuy∈L ⇔
xvy∈L" (Example 33, Definition 36); the syntactic monoid is characterized as "the smallest
X-generated monoid recognizing L" with every recognizing morphism factoring through it (Definition
32); and the introduction attributes it: "A key concept, introduced by Rabin and Scott (and earlier
in unpublished work of Myhill), is the *syntactic monoid* of a language L." For the arbitrary-monoid
form, Pin defines the syntactic congruence of a subset of an arbitrary monoid by the same formula.

I searched the whole repository for any acknowledgment: `grep -rniE
"syntactic|myhill|nerode|schutzenberger|schützenberger|eilenberg"` over `*.tex *.md *.json` returns
**zero** hits in `Theory/` and one hit in the derivation package
(`problem-contract.json:19`, which uses "the syntactic response quotient Syn(Phi)" as a name, not as
an attribution). I also grepped `05d:1000-1550` for "classical", "standard result", "well known",
"textbook", "automat*": nothing. A reader of the chapter gets no signal.

**Conceded. This one is real.**

## Attack 4 — the circle-heat theorem as a "classical result restated". REFUTED.

The finding's title asserts three classical restatements and its body supplies the third as "Same for
Blackwell domination in the circle theorem (no Blackwell 1953 entry)". Two facts kill this.

First, the manuscript does not lean on the eponym at all. `grep -n "Blackwell"
Theory/05d_relational_inference.tex` returns **nothing**. The name survives only inside the
non-rendering equation label `eq:hist-circle-heat-blackwell` and in one summary sentence in
`Theory/appendix_claim_ledger.tex:155`. What the theorem states at `05d:1483-1488` is an explicit
Markov-kernel condition:

> `H_t = H_s H_{t-s}`, but no Markov kernel `L` satisfies `H_s = H_t L`.

Nothing is imported under a borrowed name; the condition is written out and proved.

Second, I reconstructed the proof, and it is a construction with an exhibited witness, not a
restatement of anybody's theorem. `H_τ e_n = e^{-n²τ} e_n` gives `H_sH_t = H_{s+t}`, so both chains
retain `m(dR)H_{s+t}(R,dO)`. Forward garbling is `H_t = H_s H_{t-s}` with `H_{t-s}` Markov. For the
converse, if `H_s = H_t L` put `g = Le_1`; Markov positivity gives `‖g‖_∞ ≤ L1 = 1`, while matching
first Fourier coefficients in `H_t g = e^{-s}e_1` forces `|ĝ(1)| = e^{t-s} > 1`, contradicting
`|ĝ(1)| ≤ ‖g‖_∞ ≤ 1`. Soft-set inclusion is `νH_t = (νH_{t-s})H_s`. Strictness uses the exhibited
witness `ν_ρ = H_ρ(x_0,·)` with `0 < ρ < t-s`: `ν_ρH_s = H_{ρ+s}(x_0,·)`, and `νH_t = H_{ρ+s}(x_0,·)`
would force `|ν̂(1)| = e^{t-s-ρ} > 1`, impossible for a probability measure. Every step checks.

This agrees with P0's independent Fourier reconstruction (`P0:162-183`), which rates it "a clean,
genuinely good construction and the strongest single item across both packages." I did not defer to
that note; I redid it. Blackwell 1953 supplies the *definition* of comparison by garbling — a
citation worth adding for the appendix sentence, at Low severity — and supplies no part of this
theorem's content. **Counting it among "classical results restated" is wrong.**

## Attack 5 — the compact-quotient theorem as "the standard compact→Hausdorff fact". REFUTED as stated.

The finding characterizes `thm:hist-compact-operational-quotient` as "the standard fact that a
continuous bijection from a compact space to a Hausdorff space is a homeomorphism, applied to the
Myhill–Nerode quotient". Reading the proof at `05d:1148-1160`, it has three steps, and that fact is
one of them:

1. **Kernel of the countable signature.** `S_D(a) = (Φ(uav))_{(u,v)∈D×D}` has kernel exactly `∼_Φ`,
   because any `u,v ∈ A` are approximated by sequences in `D` and joint continuity of multiplication
   plus continuity of `Φ` promotes agreement on `D×D` to agreement in all contexts. This is what buys
   metrizability: the full signature lands in `Y^{A×A}`, which need not be metrizable, while
   `Y^{D×D}` is a countable product and is. The countable dense set is load-bearing, exactly as P0
   records at `P0:138-142`, and it is not the compactness fact.
2. **Compact → Hausdorff continuous bijection is a homeomorphism.** This is the standard fact, and
   the finding is right that it is standard.
3. **Descent of multiplication is *jointly* continuous** because `π×π` is a continuous surjection
   from a compact space to a Hausdorff space and hence a quotient map, so `m̄(π×π) = πm` gives
   continuity of `m̄`. Without this one lands in separate continuity and compact right-topological
   semigroup territory.

The finding exhibits no source stating steps 1 and 3 for a compact metrizable monoid with a countable
dense context set, and I could not find one; the topological syntactic-monoid literature I am aware of
runs through profinite/Stone duality, not this hypothesis set. Under the review's own rules of
evidence, asserting "this is the standard fact X" without exhibiting a source that says it is exactly
the failure mode a skeptic is supposed to catch. **The characterization does not survive.** What
remains true is narrower: the *object* being topologized is the syntactic quotient, so the same
attribution debt as Attack 3 propagates here by inheritance — one debt, not a second classical
restatement.

## Attack 6 — "presented as a new ESTABLISHED result of this program". REFUTED as to novelty, partly conceded as to visibility.

The finding's stated reason for High rather than Medium is that "the surrounding framing in
`overview.md` ... and `SPEC.md` present these as the program's own boundary-advancing results". I read
both.

`overview.md:80-89` says "The operational-intervention boundary is now exact in several declared
categories, always relative to fixed protocol data, target/type coloring where retained, ordered
external roles, and admitted morphisms", then states the factorization and closes "Neither result
selects a raw DAG or latent realization." That is a claim about the state of *this development*, not
about originality. There is no priority language, no "we prove for the first time", no "new".
`Theory/SPEC.md:726-743` is the same content in ASCII with the load-bearing hypotheses named
("Compactness and the quotient-map hypotheses are load-bearing").

The package's own contract is stronger against the finding.
`docs/derivations/2026-08-14-operational-intervention-extensions/problem-contract.json`,
`literature_policy`, verbatim:

> "Standard monoid, probability-kernel, compactness, Feller, Blackwell, and heat-semigroup facts must
> be proved directly or mapped hypothesis by hypothesis in the package. **No novelty, priority,
> exhaustive-literature, VFE/ELBO, agency, gauge/RG, or ontology claim is made.**"

That policy (i) explicitly names *Blackwell* and *monoid* facts as standard things to be proved
directly rather than claimed, (ii) requires exactly the direct proofs that were in fact given, and
(iii) disclaims priority in terms. The 8/15 work did what its own contract told it to do. This is the
same structure as the P0 correction at `P0-principal-reviewer-notes.md:228-252`, where the principal
reviewer withdrew a High attribution-and-process charge to **Low** on finding a disjunctive
`literature_policy` ending "No novelty or priority claim is made".

What I concede: `Theory/SPEC.md:29` says "Nothing in this document is a report on a prior manuscript.
It stands alone", which forecloses repairing the manuscript by pointing at `docs/derivations/`. So
the contract's disclaimer does not reach the reader of 05d, and SPEC §7 does carry an explicit norm,
"Prior art that must be cited rather than claimed" (`SPEC.md:917`), even though its enumerated list
(algebraic multigrid, matrix-weighted consensus, Sylvester's law of inertia, Birkhoff/Hilbert) does
not include Myhill–Nerode. The residual defect is that a manuscript governed by a stated
cite-prior-art norm restates a 1950s theorem, and borrows its notation, with no signal.

## Severity calibration

The finding claims High. Three independent calibration points put it at Medium or below.

1. **This review's own adjudicated precedent.** `ADJUDICATION.md:20,127-149` takes P10-High-2 — the
   *flagship* theorem of the release carrying `\status{ESTABLISHED}` with **no proof and no citation
   anywhere in `Theory/`**, a flat violation of the SPEC row — and adjudicates it **Medium**, "a
   citation/audit-trail defect under the rubric, not a proof gap". The defect here is strictly
   weaker: the proofs are present, so SPEC is satisfied, and only outside attribution is absent. A
   strictly weaker defect cannot carry a higher severity than the one already adjudicated Medium.
2. **The domain specialist reached Medium on the same material.** `P5-category-operational.md:202`
   logs "Theorems 1, 2 and Corollary 2.1 are the classical syntactic-monoid theorem, with zero
   attribution anywhere in the repository" at **[Medium]**, and records the `literature_policy`
   mitigation itself at `P5:264-272`. P10 and P5 found the same defect and differ only in severity.
3. **Scope collapse.** Of the three claimed classical restatements, one survives. Of the six claimed
   uncited ESTABLISHED theorems, the correct count is eight, and seven of them satisfy the rule the
   finding invokes.

**Corrected: Medium**, scoped to `prop:hist-operational-quotient-universal-property` at
`05d:1082-1128` (and, by inheritance of the object, the `Syn(Φ)` notation at
`thm:hist-compact-operational-quotient`). Low is defensible on the strength of the no-novelty policy
and the house citation convention; I do not go below Medium because SPEC §7 states a prior-art norm
and the chapter is declared to stand alone.

The fix the finding proposes is right and cheap, and should be adopted at reduced scope: three bib
entries (Myhill 1957, Nerode 1958, Eilenberg 1976 or Pin 1986) and one sentence at `05d:1113` saying
the proposition is the syntactic-monoid universal property transcribed from recognized languages to
an arbitrary response codomain. Add `Blackwell1953` for the eponym at
`appendix_claim_ledger.tex:155` (Low). Do **not** attach a classical attribution to
`thm:hist-circle-heat-intervention-nonidentifiability` or to steps 1 and 3 of
`thm:hist-compact-operational-quotient`; no source has been exhibited for those and doing so would
misattribute the program's own work.

## Falsifier of my own attack

Any one of these would show my verdict is wrong:

- A primary source stating the compact-quotient theorem's step 1 or step 3 — a compact metrizable
  monoid with jointly continuous multiplication, continuous response into metrizable Hausdorff `Y`,
  and a countable dense context set realizing the contextual quotient as a compact metrizable image
  — under those hypotheses. That would restore the finding's second classical restatement and push
  the severity back toward High.
- A sentence in `Theory/`, `overview.md`, `docs/STATUS.md`, or the release front matter that claims
  novelty or priority for `Syn(Φ)` or the operational quotient. I grepped `overview.md:70-100`,
  `SPEC.md:726-760`, and `05d:1000-1550` and found fenced state-of-development language only; a
  priority sentence I missed would restore High.
- A source in which "Blackwell domination" is not merely the definition of garbling but supplies a
  step of the circle-heat argument, which would make my Attack 4 wrong.
- A reading of `SPEC.md:71` on which the "or" is conjunctive — i.e. an instance elsewhere in the
  manuscript where a proved `ESTABLISHED` result was nevertheless treated as defective for lacking a
  citation. That would revive the SPEC-conformance charge and, with it, the count of six or eight.

## Contradiction with P0, and how it resolves

My verdict does not contradict `P0-principal-reviewer-notes.md`; it agrees with both of P0's relevant
reconstructions and disagrees with P10's use of them. P0 item 1 (`P0:111-128`) reaches the same
conclusion as my Attack 3 — classical, correctly proved, novelty is the issue — and P0 item 6
(`P0:162-183`) reaches the same conclusion as my Attack 4, that the circle construction is genuinely
good and not a restatement. P10 lumped the circle theorem into a title clause its own body does not
support and that P0's Fourier reconstruction contradicts; on that clause P0's reconstruction is
correct and I confirmed it independently. P0's severity precedent at `P0:228-252` (attribution defect
with an explicit no-novelty policy → Low) and the adjudicated P10-High-2 precedent (→ Medium) bracket
the correct answer, and Medium is the right end of that bracket because the manuscript, unlike the
derivation package, carries no disclaimer and is declared to stand alone.

## Commands and files of record

- `git diff 8ce6358 HEAD -- Theory/05d_relational_inference.tex` → empty
- `git diff f655ba5 8ce6358 -- Theory/05d_relational_inference.tex | grep -E "^\+.*heading"` → the
  nine new headings tabulated above
- `grep -n "Blackwell" Theory/05d_relational_inference.tex` → no output
- `grep -rniE "syntactic|myhill|nerode|schutzenberger|eilenberg" --include=*.tex --include=*.md
  --include=*.json .` → no hit in `Theory/`; one naming hit at
  `docs/derivations/2026-08-14-operational-intervention-extensions/problem-contract.json:19`
- `grep -niE "myhill|nerode|schutzenberger|eilenberg|blackwell" Theory/references.bib` → no output;
  `grep -c "^@" Theory/references.bib` → 466
- Per-chapter `\cite*` counts, tabulated above
- Read directly: `Theory/SPEC.md:29,55-95,726-760,890-920`; `Theory/05d_relational_inference.tex:1040-1204,1319-1345,1455-1524`;
  `overview.md:70-100`;
  `docs/derivations/2026-08-14-operational-intervention-extensions/problem-contract.json`
- Source fetched: arXiv:1504.02694 (Adámek, Milius, Urbat, *Syntactic Monoids in a Category*) via
  ar5iv — Example 33 / Definition 36 (syntactic congruence), Definition 32 (smallest recognizing
  monoid, factorization), §1 attribution to Rabin–Scott and Myhill
