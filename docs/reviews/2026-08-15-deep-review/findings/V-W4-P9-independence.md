# V-W4-P9-independence — Skeptic attack on W4-P9-independence

STATUS: COMPLETE
AGENT: wave-4 adversarial skeptic (Claude Opus 5)
TARGET REVISION: 8ce635807a6ca2a388255fc996c98f7c535e5843, branch `review/2026-08-15-deep-review`
FINDING UNDER ATTACK: `W4-P9-independence` (stated severity **High**), from
`findings/P9-selfcert-falsifiability.md:251` and `:280`

**VERDICT: UPHELD_REDUCED. Corrected severity: Medium.**

Half (b) — the structural-isomorphism charge — survives every attack I could mount, and my own
reconstruction makes it *stronger* than the investigator stated. Half (a) — the oracle-erasure
charge — is factually accurate but is largely a criticism of the `rigorous-theory-search` protocol,
which documents this exact limitation itself, rather than a defect this package introduced. The
grouped **High** averages a Medium-grade certification defect with a Low-grade protocol complaint.

---

## Summary of what I did

I did not adjudicate by reading either party's prose. I:

1. Read `direct-derivation.md` (498 lines), `independent-reconstruction.md` (62),
   `counterexample-proofs.md` (222), and `oracle-erasure.md` (42) in full.
2. Enumerated every file in the 8/15 package to test the "no mechanical residue" claim.
3. Loaded the package's **own** `dependency-dag.json` and computed, by exact enumeration, how many
   orderings the mathematics actually permits — the question the finding says "is the whole question."
4. Computed the pairwise order agreement between the two documents, partitioned into DAG-forced and
   DAG-free pairs.
5. Reproduced the investigator's n-gram overlap numbers independently.
6. Read the `rigorous-theory-search` skill's own specification of what oracle erasure must produce.

Scripts used are in the session scratchpad (`topo.py`, `pairs.py`, `ngram.py`); all are ~40 lines and
read only the committed artifacts.

---

## Part (b): the structural-isomorphism charge — **UPHELD, and strengthened**

### The attack I was told to make, and why it fails

> "Independent reconstructions of the SAME theorem from the SAME premises will naturally share order
> because the mathematics forces it (you must have the channel before the pushforward, the pushforward
> before the chain rule, the chain rule before the defect)."

This is the right attack and it is refutable with the package's own machine-readable artifact. The
package ships `dependency-dag.json`, a 28-edge DAG over the target and its 18 closure claims. That
file *is* the statement of which orderings the mathematics forces. I enumerated them.

**Executed (exact enumeration over `dependency-dag.json`, prerequisites-first topological orders):**

```
Total topological orders of the full DAG (target included): 46714792320
Total topological orders of the 14 non-target claims:       43836629760
Topological orders of the affirmative closure alone (13):        42636
```

The spine the attack names *is* forced, and it is short:
`POINTWISE-TYPING → PARENT-NORMALIZATION → POSTERIOR-PUSHFORWARD →
COMMON-CHANNEL-ABSOLUTE-CONTINUITY → VFE-CHAIN-EXTENDED → VFE-FINITE-ZERO-DEFECT-RECOVERY`,
plus `MODEL-FAMILY-NORMALIZATION → EVALUATION-COMPATIBILITY` and
`{HOLONOMY-BLIND, HOLONOMY-RETENTION} → HOLONOMY-ALTERNATIVE`.

Everything else is free. `DERIVED-MARGINALS`, the evaluator block, the KL block, the holonomy block,
and `DYNAMICS-SCOPE` are mutually incomparable: nothing in §6 uses the marginals of §5, nothing in §5
or §6 uses the evaluator kernel of §4, and §8 uses none of them. **The order is contingent, not
forced.** That answers the finding's central question against the package.

### The quantification the finding asked for

I mapped each of the 18 closure claims to its position in each document. The reconstruction labels its
own claim IDs inline (lines 18, 20, 22, 24, 28, 30, 32, 36, 38, 42, 46, 48, 52, 54, 58), so this
mapping is *read off the artifact*, not inferred. For the package side I used
`direct-derivation.md` §1–§8 for the affirmative claims and `counterexample-proofs.md` §2–§5 for the
five `NEG-*` claims.

**Executed (pairwise order comparison, 18 claims, 153 pairs):**

```
DAG-FORCED pairs (one is a transitive prerequisite of the other):  39
DAG-FREE   pairs (mutually incomparable -> author's free choice): 114

Of the 114 FREE pairs, the reconstruction kept the package's relative order in 49 (43.0%)
Inverted free pairs: 65
  breakdown of the inversions: {('AFF','NEG'): 40, ('NEG','AFF'): 25}

AFFIRMATIVE closure only (13 nodes): FREE pairs = 39; same relative order = 39; inversions = NONE
NEGATIVE block only  (5 nodes, ALL mutually free): FREE pairs = 10; same relative order = 10
```

Read that carefully, because it is sharper than the investigator's table:

- **Within the affirmative closure the reconstruction matched the direct proof on 39 of 39 free
  ordering choices. Zero inversions.** It selected one of 42,636 admissible orders and it selected the
  direct proof's.
- **Within the negative block it matched on 10 of 10 free pairs.** Those five nodes have *zero*
  prerequisite edges — they are the only claims in the entire closure whose position is wholly
  unconstrained — and it reproduced `counterexample-proofs.md`'s order exactly (marginal determination,
  split channel, model-marginal evaluation, trivial holonomy, marginal-vs-joint holonomy), with the
  same witnesses and the same numbers (binary square correlated/anticorrelated; `Q=Π=Bern(1/2)` through
  identity vs constant-zero; `K_0(B{=}1)=1/4`, `K_1(B{=}1)=3/4` swapped; identity-transport two-node
  tree; first-coordinate bit flip).
- **Every one of the 65 inversions is a cross-block AFF/NEG pair.** That is the signature of exactly
  one edit: moving a block. The reconstruction made precisely **one** ordering decision differently
  from the package, and it moved the one block that carries no dependency constraints at all.

So `independent-reconstruction.md:6`'s "The reconstruction proceeds in a different order" is
technically true and substantively empty. Prepending a dependency-free block is the cheapest possible
permutation and demonstrates nothing about derivational route.

### Technique identity — confirmed by my own reading

The investigator claims no step is proved a second way. I checked each load-bearing step against both
texts:

| step | direct | reconstruction |
|---|---|---|
| channel normalization | §2: "normalization gives \(C_A1=1\)" | :28 "its kernel action satisfies `C_A 1=1`" |
| posterior pushforward | (3.5): "(1.1), (3.2), and Tonelli" | :30 "substitute the fine disintegration into the parent integral and apply Tonelli" |
| absolute continuity | §3: "\(C_A(Y,D)=0\) for \(\Pi_{I,o,X}\)-a.e. \(Y\)" | :32 "its channel probability is zero `Pi_I`-almost surely" |
| KL chain | (6.2): derivative of the lift is \(r(Y)\) because the channel factor is shared | :46 "joint Radon-Nikodym derivative is the fine derivative because the conditional channel factor is identical" |
| recovery converse | :370 "Data processing through \(C_A\) and then through \(R\)" | :48 "data processing in both directions" |
| holonomy covariance | §7: "Substitution into the defining integrals" | :52 "moved through each defining integral" |

Same route at every step. Genuinely independent routes for the one substantive result exist and were
not taken: the extended-valued chain rule can be obtained from the Gelfand–Yaglom–Perez
finite-partition supremum definition of relative entropy, or from the Donsker–Varadhan variational
representation; the zero-defect converse can be obtained directly from Csiszár's sufficiency
characterization rather than a two-sided DPI sandwich. Either would have been a second route. Neither
appears.

### n-gram figures reproduce exactly

I recomputed the investigator's lexical-freshness numbers from the committed bytes:

```
n=4: recon 4-grams=1354  shared with direct= 57  (4.2%)
n=5: recon 5-grams=1361  shared with direct= 34  (2.5%)
n=6: recon 6-grams=1363  shared with direct= 23  (1.7%)
n=8: recon 8-grams=1363  shared with direct= 14  (1.0%)
```

Identical to the four lines reported at `P9-selfcert-falsifiability.md:308-311`. Their claim that
eleven of the fourteen shared 8-grams come from the metadata header is also exact — I printed all
fourteen; eleven are the `rigorous-theory-search-metadata` comment. The remaining three are
*mathematical*, and they sit at load-bearing steps: "equality of the finite fine and coarse kl",
"of the finite fine and coarse kl values" (the recovery converse), and "same slice invariance follows
only for isotropy arrows" (the isotropy caveat). The investigator's mechanical work is reproducible
and correct, and the residual lexical overlap points at the same two places their structural analysis
does. I concede this half entirely.

### The best defense available to the package, and why it fails

The strongest defense is not the one the finding anticipated. It is:

> The reconstruction declares its inputs as `problem-contract.json`, `claim-ledger.json`, and
> `dependency-dag.json` — not `direct-derivation.md`. If the *ledger's* claim listing already fixes the
> order, then reproducing that order is following the declared inputs, not the proof's outline.

I checked. The ledger lists its claims in this order: `POINTWISE-TYPING, MODEL-FAMILY-NORMALIZATION,
PARENT-NORMALIZATION, POSTERIOR-PUSHFORWARD, COMMON-CHANNEL-ABSOLUTE-CONTINUITY,
EVALUATION-COMPATIBILITY, DERIVED-MARGINALS, VFE-CHAIN-EXTENDED, VFE-FINITE-ZERO-DEFECT-RECOVERY,
HOLONOMY-BLIND-FULL-LAW, HOLONOMY-RETENTION, HOLONOMY-ALTERNATIVE, DYNAMICS-SCOPE, NEG-×5.` That is
the direct proof's order up to a single transposition of `MODEL-FAMILY-NORMALIZATION`. So the defense
has real factual footing.

It still fails, for two independent reasons:

1. **The reconstruction did not follow the ledger order either.** The ledger puts the five `NEG-*`
   claims *last*; the reconstruction puts them *first*. So the document departs from its declared
   inputs' ordering exactly once — and that single departure is the block move already shown to be
   free. On every other free choice it tracks both the ledger and the direct proof.
2. **It relocates the outline rather than eliminating it.** The ledger is a same-package, same-session,
   same-author artifact whose ordering matches the direct proof to within one transposition. "I used
   the ledger, not the proof" is not independence in any sense a reader of `final-report.md:28` would
   understand.

### One point I raised against the finding and then withdrew

I initially noted that `independent-reconstruction.md:46` invokes "the same finite `-log p_X(o)`" with
no antecedent anywhere in the document — no σ-finite reference measure, no density representative, no
\(0<p_X(o)<\infty\) admission condition — all of which `direct-derivation.md:47-53` declares. That
would have been evidence the reconstruction silently imports the direct proof's setup. **It does not
hold up**: `ASM-EVIDENCE-REPRESENTATIVE` in the ledger states exactly this ("A sigma-finite observation
reference and one density representative p_X are declared, 0<p_X(o)<infinity at the admitted regular
observation, and the identical representative is reused at both scales"), and the contract is a
declared input. This is an exposition gap in the reconstruction, nothing more, and I record it at
negligible weight.

### Where the defect actually lives

`final-report.md:28`, the release-facing sentence: "rebuilds the closure **without using the direct
proof as its outline**." The artifact's own honest qualifier at `:8` — "a sequential role-separated
derivation by the Task-5 assembler, not independent-agent agreement" — is dropped there. Note that `:8`
fences *agent* independence, which is a different and weaker claim than *outline* independence; it does
not fence `:6`. And `release-assembly.json:193` consumes the result: the gate `reason` reads "All static
ancestors have eligible direct evidence; **reconstruction and oracle erasure pass**; all sixteen attacks
are rejected; …". So the unsupported claim is load-bearing for the release gate, not merely decorative.

**Part (b) verdict: UPHELD.** I found no defense. The order is contingent (42,636 admissible orders on
the affirmative closure), the reconstruction matched the package on 49/49 within-block free choices,
its single reordering moved the only dependency-free block, and every proof technique is reused.

---

## Part (a): the oracle-erasure charge — **factually correct, severity overstated**

### (a1) "No mechanical residue exists" — **VERIFIED TRUE**

I enumerated every file in the 8/15 package. There are 27:

```
adversarial-report.json, approach-registry.json, claim-ledger.json,
construction-or-strongest-theorem.md, counterexample-register.md, dependency-dag.json,
final-report.md, problem-contract.json, release.json,
evidence/{adversarial-attacks.md, counterexample-proofs.md, direct-derivation.md,
  finite-nongaussian-output.json, finite_nongaussian_witness.py, independent-reconstruction.md,
  notation-collision-report.json, notation-registry.json, notation-standard.md, notation_scan.py,
  oracle-erasure.md, release-assembly.json, release-provenance.json,
  __pycache__/notation_scan.cpython-314.pyc},
evidence/reviews/{view-dynamics-scope.md, view-gauge-holonomy.md, view-information-vfe.md,
  view-probability-kernel.md}
```

The only erasure artifact is the 42-line prose `oracle-erasure.md`. There is no erased copy of the
premise set, no diff, no re-derivation against erased text, and no scan script. The two scripts present
(`finite_nongaussian_witness.py`, `notation_scan.py`) belong to the witness and notation audits. The
investigator's contrast with those two audits is accurate.

### (a2) "The test has no failure mode" — **true, but it is a protocol property, not a package defect**

This is where the finding overreaches, and it is the one place I can push back with a source.

The `rigorous-theory-search` skill *specifies* that this check is unmechanized and self-performed.
`references/output-contract.md:39`:

> "Prior-leak detection is the narrowest of these checks and must not be read as mechanized oracle
> erasure. The validator matches only the literal token `SEARCH_PRIOR_AFFIRMATIVE` … Detecting
> paraphrased dependence is a semantic judgment the validator cannot make, and it remains entirely a
> certification and adversarial obligation discharged by the oracle-erasure pass."

and `SKILL.md:54`:

> "The paraphrase scan is unmechanized… **Perform that scan yourself** against premises, assumptions,
> and load-bearing steps. Passing shows only that the prior was unnecessary; **it does not prove the
> theorem**."

`references/adversarial-verification.md:9` says the same. So the protocol demands a prose semantic
scan by the same agent, concedes it cannot be mechanized, and states in advance that passing proves
nothing. The package delivered exactly that and labeled it exactly as prescribed: `claim-ledger.json`
types `EV-TASK5-ORACLE-ERASURE` as `kind: AGENT_ASSESSMENT` with `side_conditions` "Oracle erasure is a
certification audit and is not itself mathematical proof" and "The literal-token validator cannot detect
paraphrased prior dependence."

This is also not specific to the 8/15 release. Every derivation package in the repository has the same
shape, and none ships an erasure script:

```
2026-08-12-elbo-pifb2-fast-slow-program/               10 lines | no erasure script
2026-08-12-elbo-to-effective-section-action/           11 lines | no erasure script
2026-08-12-exact-two-channel-finite-elbo/              12 lines | no erasure script
2026-08-13-finite-presentation-descent-joint-fisher/   84 lines | no erasure script
2026-08-14-canonical-dependence-selection/            114 lines | no erasure script
2026-08-14-collective-joint-lift-fisher/               46 lines | no erasure script
2026-08-14-operational-intervention-extensions/       101 lines | no erasure script
2026-08-14-pointwise-meta-agent-rg/                    26 lines | no erasure script
2026-08-14-typed-intervention-nonidentifiability/     114 lines | no erasure script
2026-08-15-full-pointwise-meta-agent/                  42 lines | no erasure script
```

(The `.py` files in those `evidence/` directories are all witness/recompute scripts for the
mathematics.) Including the 8/14 operational package that P9 elsewhere holds up as the more severe
comparator — its 101-line erasure file is prose too, structured identically.

So (a2), correctly stated, is: *the rigorous-theory-search protocol's oracle-erasure step is
unfalsifiable by construction, and the protocol says so.* That is a legitimate observation about the
method and a fair thing for the review to say. It is not a High-severity defect **this package
introduced**, and grading it as one misattributes a protocol limitation to an author who complied with
the protocol and reproduced its disclaimer verbatim.

### (a3) "The release counts it anyway" — **true and package-specific**

This is the part of (a) that is genuinely the package's own. Three mechanical facts:

- `release-assembly.json:193` gate `reason` includes "reconstruction and **oracle erasure pass**".
- `claim-ledger.json` `target.evidence_ids` includes `EV-TASK5-ORACLE-ERASURE`.
- `oracle-erasure.md:42` reads: "This pass demonstrates only that no desired conclusion was smuggled
  into the premises; the direct and reconstructed derivations remain the mathematical evidence. All
  four corrected-byte domain reviews are current and `APPROVE` … so oracle erasure leaves no release
  obligation open and `target` is `EVIDENCE_VERIFIED`."

The 8/14 comparator does **not** do this — its erasure file ends at the disclaimer ("This result shows
only that the preference was logically unnecessary; it is not an additional proof of the theorem.") and
stops. Appending the promotion to the disclaimer is unique to 8/15 and is a real inconsistency.

But (a3) is the same defect as the separately-filed `V-W4-P9-ledger-eligibility` item ("The ledger
closes `target` as EVIDENCE_VERIFIED using evidence the ledger itself types as ineligible",
`P9-selfcert-falsifiability.md:356`). Carrying it at High here as well double-counts one defect across
two findings.

**Part (a) verdict: UPHELD_REDUCED to Low.** (a1) is verified. (a2) is a true criticism of the method
rather than of this package's execution of it. (a3) is real but duplicated.

---

## Relation to the principal reviewer's reconstructions

No conflict. `P0-principal-reviewer-notes.md` independently re-derived the posterior pushforward, the
parent absolute continuity, the additive KL chain and defect, and the (6.9)–(6.12) recovery theorem,
and marked all four **CHECKS OUT**. Nothing in this finding, and nothing in my attack, disputes any of
them. The mathematics is correct; what is at issue is whether a second document that re-words that
mathematics constitutes independent evidence for it.

P0's calibration is directly relevant to severity and I follow it. P0 rated the prior-work finding High
as an "attribution *and process*" defect, then **withdrew the process half** on evidence it checked
itself and re-adjudicated the residual at **Low**, on the reasoning that a defect the package disclosed
elsewhere is not a High. The same test applied here splits the grouped finding: the outline-independence
claim is **not** disclosed elsewhere (`:8` fences agent independence, a different claim; `final-report.md:28`
asserts outline independence flatly), so (b) survives at Medium; the erasure's evidential weakness **is**
disclosed — in the artifact, in the ledger's `side_conditions`, and in the governing protocol — so (a)
drops to Low.

P0's closing note is the correct frame for both: "The certification apparatus should be read as
bookkeeping, not as evidence."

---

## Verdict

**UPHELD_REDUCED — corrected severity Medium** (stated: High).

- **(b) structural isomorphism: UPHELD, and strengthened by my own reconstruction.** The shared order
  is contingent, not forced: the package's own DAG admits 42,636 orderings of the affirmative closure
  and 4.4×10¹⁰ of the full closure; only 39 of 153 claim pairs are order-forced. The reconstruction
  matched the direct proof on **49 of 49** free within-block ordering choices with zero inversions, and
  its sole reordering moved the five `NEG-*` claims — the only nodes in the closure with no prerequisite
  edges — while preserving their internal order and their exact witnesses. Every proof technique is
  reused; at least two genuinely independent routes for the one substantive step exist and were not
  taken. The release-facing claim at `final-report.md:28` is unsupported and is consumed by the release
  gate. Standing alone this is Medium: a checkable, release-facing overclaim about evidence, with no
  mathematical statement wrong and no proof gap.
- **(a) oracle erasure: UPHELD_REDUCED to Low.** No mechanical residue exists — verified by
  enumeration. But the governing protocol specifies an unmechanized self-performed semantic scan and
  states in advance that passing proves nothing; the package complied and reproduced that disclaimer in
  the artifact and in the ledger's `side_conditions`; and all ten packages in the repo share the shape.
  The package-specific residue — appending "`target` is `EVIDENCE_VERIFIED`" to the disclaimer and
  citing erasure in the gate `reason` — is real but is the same defect already filed as
  `V-W4-P9-ledger-eligibility`.

**Recommended disposition:** ungroup. Record (b) at **Medium** with the quantification above
substituted for the investigator's heading table, which understates it. Record (a) at **Low**, and
relocate its (a2) content to a review-level observation about the `rigorous-theory-search` protocol
rather than a finding against this release. The investigator's proposed fix for (b) —
rewriting `final-report.md:28` to "a role-separated second pass by the same author, in the same order as
the direct proof and using the same techniques; it re-expresses rather than re-routes the argument" — is
correct as written and I endorse it verbatim.

---

## Falsifier of my own attack

My verdict is wrong if any of the following holds:

1. **Against my UPHELD of (b):** exhibit one load-bearing affirmative step that
   `independent-reconstruction.md` proves by a route absent from `direct-derivation.md` — a
   finite-partition-supremum or Donsker–Varadhan derivation of the extended chain rule, or a direct
   Csiszár-sufficiency proof of the recovery converse — **or** exhibit one pair of closure claims whose
   relative order is inverted between the two documents *within* either block. My pair scan found zero
   such inversions among 49 free within-block pairs; producing one falsifies the strongest part of my
   agreement with the investigator.
2. **Against my reduction of (a):** show that `rigorous-theory-search` *does* require a machine-readable
   erasure artifact and that I misread `references/output-contract.md:39`, `SKILL.md:54`, and
   `references/adversarial-verification.md:9`. Then the omission is package-specific after all and the
   grouped High is right.
3. **Against my severity call generally:** show that some downstream claim in the repository relies on
   the reconstruction or the erasure as *mathematical* support rather than as certification bookkeeping.
   Then the defect propagates into the mathematics and High is right. I checked `target.evidence_ids`
   and found the reconstruction and erasure listed alongside `EV-TASK3-DIRECT-DERIVATION`; since P0
   independently verified the direct derivation, removing both certification artifacts leaves the
   mathematics standing, which is why I hold at Medium.
4. **Against (a1) specifically:** produce an erased-premise artifact, diff, or scan script anywhere in
   the 8/15 package or its provenance chain that my enumeration missed. That would refute (a1) outright
   and push the finding below Low, not above it.
