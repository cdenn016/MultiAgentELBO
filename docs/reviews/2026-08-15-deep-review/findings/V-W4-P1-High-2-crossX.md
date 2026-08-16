STATUS: COMPLETE
AGENT: wave-4 adversarial skeptic (Claude Opus 5)
TARGET: 8ce635807a6ca2a388255fc996c98f7c535e5843, branch review/2026-08-15-deep-review
FINDING UNDER ATTACK: W4-P1-High-2-crossX
VERDICT: UPHELD_REDUCED — corrected severity **Low** (notation hygiene), not High (correctness)

# Attack on W4-P1-High-2-crossX

The finding claims three things, in decreasing order of load. (i) Equation (4.5) is *"a false
statement under a literal reading"*, because its right-hand side carries superscript `X_A` while its
left-hand side conditions on `X`, and the induced-tier object is built from the fine `X`. (ii) The
violation is *normative*: the package's own notation registry types the parent evaluator as a
function of `X_A`, so the induced tier gives one token a second semantic type, which the registry's
collision contract forbids. (iii) The document's caveat is confined to one paragraph while the
notation is used globally.

All three fail. What survives is that the superscript is misleading, that the derivation's symbol is
out of step with the *package's own claim ledger*, and that the string can collide in (7.6). That is
a one-symbol cosmetic defect, and the investigator's proposed fix is the right fix. It is not a
correctness defect and it is not High.

## 1. Reconstruction: (4.5) is a definitional restatement of (4.3), and is true

I did not adjudicate this from either party's prose. I redid the step.

Fix `X` as §1 requires. Let `W_A = B_A x O x H_A` and let `mu := mu_A^{MΞ}(. | X)` be the
`(M_A, Ξ_A)`-marginal of `P_A(. | X)`. All factors are standard Borel (§1, :15–:23), so
`P_A(. | X)` is a Borel probability measure on the standard-Borel product `W_A x M_A x Ξ_A` and the
disintegration theorem (Rokhlin; Kallenberg, *Foundations of Modern Probability*, disintegration of a
law on a product of Borel spaces along a coordinate map) supplies a Markov kernel
`G_A^X : M_A x Ξ_A ~> W_A`, unique up to `mu`-null sets, with

    P_A( (M_A,Ξ_A) in D, (B_A,O,H_A) in E | X ) = ∫_D G_A^X(m_A,ξ_A; E) mu(dm_A,dξ_A).     (4.3)

By the *definition* of a regular conditional distribution, (4.3) says exactly

    G_A^X(m_A,ξ_A; .) is a version of P_A( (B_A,O,H_A) in . | (M_A,Ξ_A)=(m_A,ξ_A), X ),  mu-a.s.   (*)

Line :190 then **defines** `K^{X_A}_{A,m_A}(ξ_A; .) := G_A^X(m_A,ξ_A; .)`. Substituting the definiendum
for the definiens in (*) yields, character for character including the `mu_A^{MΞ}`-a.s. qualifier,

    P_A(db_A,do,dh_A | ξ_A,m_A,X) = K^{X_A}_{A,m_A}(ξ_A;db_A,do,dh_A)   mu_A^{MΞ}-a.s.     (4.5)

So (4.5) is (4.3) with a defined name substituted. Its truth is insensitive to the decoration on the
`K` symbol, because a superscript is a part of a name, not a predicate. There is no proposition in
(4.5) that says "this object is determined by `X_A`". The word "false" does not apply.

For (4.5) to carry the content the investigator ascribes, the package would have to additionally
stipulate a family `(x_A,m_A,ξ_A,E) ↦ K^{x_A}_{A,m_A}(ξ_A;E)` on the *range* of `chi_A` with
`K^{chi_A(X)} = G_A^X` for every `X`. No such stipulation exists, and the package says so repeatedly
(§2 below). The finding's reading supplies the missing premise itself and then convicts the document
of it.

## 2. The finding's counterexample confirms a disclaimer; it contradicts no statement

The exhibited example — `M_A = Ξ_A = {*}`, `W_A = {0,1}`, `chi_A` constant, `P_A(.|X)` giving
`(1/3,2/3)` and `P_A(.|X')` giving `(2/3,1/3)` — is arithmetically correct. With `M_A x Ξ_A` a
singleton, `mu` is a point mass and `G_A^X(*,*;.)` is just the `W_A`-marginal, so `G_A^X ≠ G_A^{X'}`
while `chi_A(X) = chi_A(X')`. It establishes:

> the induced kernel is not a function of `chi_A(X)` alone.

That is precisely what `direct-derivation.md:190` asserts in its own words, and what `:6` asserts
globally. The example therefore falsifies nothing in the package; it is a witness *for* the
document's disclaimer. A counterexample that instantiates a proposition the target already states is
not a counterexample. It also requires two structural data, which §1 (`:6`) excludes from the
theorem's scope.

## 3. The "caveat is local, the notation is global" charge is factually wrong

The investigator cites `:190` as the caveat and calls it paragraph-local. The **global** fence is
`direct-derivation.md:6`, in §1 "Fixed structural data", *before the first `K` appears anywhere in
the document*:

> "This theorem is pointwise in this one \(X\). It makes no claim that two values \(X,X'\) with
> \(\chi_A(X)=\chi_A(X')\) induce the same parent law. Such a cross-\(X\) claim would require a
> separately measurable factorization through \(X_A\)."

`grep -n "direct-derivation.md:6\|line 6\|§1"` over the whole of `P1-measure-probability.md` returns
no citation of `:6` in this finding or anywhere else in that file. The investigator missed the one
passage that most directly answers the charge.

The fence is not stated once, or twice. Enumerated by mechanical search over the package:

| Location | Text |
|---|---|
| `evidence/direct-derivation.md:6` | "pointwise in this one \(X\) … no claim that two values \(X,X'\) …" |
| `evidence/direct-derivation.md:190` | "The notation \(X_A\) does not prove cross-\(X\) factorization … is an additional premise." |
| `evidence/direct-derivation.md:498` | "It supplies no … cross-\(X\) factorization." |
| `construction-or-strongest-theorem.md:118` | "The theorem is pointwise in one fixed \(X\). It makes no claim of cross-\(X\) sufficiency through \(X_A\) …" |
| `claim-ledger.json:9` (`ASM-POINTWISE-STANDARD-BOREL`) | "… no cross-X factorization through X_A is asserted." |
| `claim-ledger.json:69` | "The theorem is pointwise in one fixed X and does not infer cross-X sufficiency from X_A=chi_A(X)." |
| `approach-registry.json:30, :54, :177` | "No cross-X factorization through X_A and no patchwise family are proved." |
| `evidence/adversarial-attacks.md:120` (A15) + `adversarial-report.json:186` (`ATTACK-CROSS-X-GLUING`) | the package **pre-registered this exact attack** and dispositioned it `REJECTED` on the fixed-`X` scope |
| `final-report.md:40` | "It does not establish cross-`X` sufficiency …" |
| `evidence/reviews/view-probability-kernel.md:41` | "no cross-`X` factorization is inferred (`evidence/direct-derivation.md:6-6`)" — the domain review cites line 6 by number |

The investigator cited `construction-or-strongest-theorem.md:42` and `:50` as offending locations
without reporting `:118` of the same file, which fences them.

## 4. The normative charge fails on the registry's own type fields

This is the finding's strongest-looking limb and it does not survive contact with
`evidence/notation-registry.json`. The two entries:

```
{"canonical":"\\operatorname{ev}_A", "type":"normalized measurable kernel family",
 "domain_codomain":"M_A -> Kern(Xi_A,B_A x O_A x H_A)", ...}
{"canonical":"\\operatorname{ev}_i", "type":"normalized measurable kernel family at fixed X",
 "domain_codomain":"M_i -> declared generative-kernel fiber", ...}
```

Three consequences, each fatal to limb (ii):

1. **`ev_A` is not typed as a function of `X_A`.** Its declared `domain_codomain` is
   `M_A -> Kern(Xi_A, ...)`. `X_A` does not appear in it. The investigator quotes this exact string
   in his own falsifier paragraph and reads it as "no `X`-dependence escape clause" — but it equally
   contains no `X_A`-dependence *typing*, which is what his normative charge requires. The registry
   simply does not type the superscript as an argument.
2. **`ev_i` carries superscript `X` and its `domain_codomain` omits `X` too** (`M_i -> declared
   generative-kernel fiber`), with `X` demoted to the prose `type` field, "at fixed structural `X`".
   So under the registry's *own uniform convention* the structural superscript is a fixed-scope
   decoration in both entries, not an argument. The claimed "deliberate contrast" between `K^X_i` and
   `K^{X_A}_A` is a contrast of decoration, not of type.
3. **No type change, hence no collision-contract breach.** The contract at `notation-standard.md:44`
   is "One canonical token has one semantic type in a theorem." The canonical token is
   `\operatorname{ev}_A`; its one semantic type is "normalized measurable kernel family,
   `M_A -> Kern(Xi_A, B_A x O_A x H_A)`". The induced object and the predeclared object both satisfy
   that type exactly. Parameter provenance is not part of the declared type, so the induced tier does
   not install "a second semantic type".

Incidentally, the investigator's remark that the scanner "matches tokens, not types" understates the
situation and, in doing so, removes the last support from the normative framing. `notation_scan.py`
does not read `direct-derivation.md` at all. `notation-registry.json` puts `docs/derivations` in
`immutable_roots` but then lists `docs/derivations/2026-08-15-full-pointwise-meta-agent` in
`immutable_exclusions`, while `active_roots` admits only that package's `notation-standard.md`.
Executed check:

```
$ python -c "... json.load('evidence/notation-collision-report.json') ..."
active files: 33
['docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation-standard.md']
direct-derivation scanned as active: False
immutable count: 0
direct-derivation in immutable: False
```

So the scanner's `unclassified_collision: 0` says nothing whatever about §4 — but by the same token
the scanner never *certified* §4 either. Nothing false was asserted by the certification apparatus
on this point. This weakens the finding rather than strengthening it.

## 5. The investigator's own falsifier is triggered — by the claim ledger

His falsifier reads: "A statement in the package (which I did not find) declaring `K^{X_A}` to be
notation for a family indexed by the pair `(X_A, X)`". He reports checking `notation-standard.md` and
`notation-registry.json`. The declaration is in `claim-ledger.json`, and it is per-tier and explicit:

- `ASM-MODEL-EVALUATION-FAMILY` (`:34`): *"**For the predeclared tier only, at fixed X_A** the family
  `(m_A,xi_A,E)->K^{X_A}_{A,m_A}(xi_A;E)` is supplied …"*
- `MODEL-FAMILY-NORMALIZATION` (`:259`): *"Disintegration of the pushed parent law **at fixed X**
  proves existence of an induced normalized jointly measurable kernel family
  `(m_A,xi_A,E)->K^{X_A}_{A,m_A}(xi_A;E)` …"*, whose `assumption_ids` is exactly
  `["ASM-POINTWISE-STANDARD-BOREL"]`, i.e. the assumption whose text ends "no cross-X factorization
  through X_A is asserted".

The ledger therefore already draws the exact line the finding's Fix proposes — `X_A`-indexing for the
predeclared tier, `X`-indexing for the induced tier — and already fences the induced claim on the
no-cross-`X` assumption. Only the *symbol* in the derivation body fails to record the distinction.

## 6. Nothing downstream uses a cross-`X` factorization

This was the decisive substantive question. I enumerated every occurrence of the token in the
package.

`evidence/direct-derivation.md`: `:158`, `:163`, `:168` (statement of the family's type, (4.1)/(4.2));
`:190` (the induced choice, plus the caveat); `:196` ((4.4), the *predeclared compatibility
hypothesis*); `:205` ((4.5)); `:452`–`:453` ((7.6)).
`construction-or-strongest-theorem.md`: `:42`, `:50`.
Elsewhere: `notation-standard.md:20,:33`, `approach-registry.json:37`, `claim-ledger.json:34,:259`,
`evidence/reviews/view-gauge-holonomy.md:112-113`.

No step anywhere performs an inference of the form `chi_A(X)=chi_A(X') ⇒ kernels equal`, integrates
over `X_A`, or invokes measurability in `X_A`. §5, §6, §8 and §9 never mention `K` at all; §6's KL
chain, the finite-tier VFE identity and the recovery criterion are built entirely from `C_A`,
`Q_{I,o,X}`, `Pi_{I,o,X}`, and use no evaluator. The `X_A` superscript is therefore inert: delete it
and replace it with `X` throughout and not one line of mathematics changes — which is exactly what
the investigator's own Fix says ("One symbol change; no mathematics moves"). A notation whose removal
changes nothing cannot be carrying a false theorem.

## 7. What actually survives — and it is Low

Three residues, all real, all cosmetic.

**(a) The derivation's symbol disagrees with the ledger's per-tier indexing.** `claim-ledger.json`
says "at fixed X" for the induced family and "at fixed X_A" for the predeclared one; the derivation
writes `K^{X_A}` for both. That is internal drift between two artifacts of the same release, and the
one-symbol fix repairs it.

**(b) §7 is the one place with two structural data in scope, and there the string can collide.**
`:6`'s "pointwise in this one \(X\)" does not literally cover §7, which introduces an arrow
`g:(o,X)→(o',X')` with primed spaces and laws. (7.6) reads

    (T_B^g x T_O^g x T_H^g)_# K^{X_A}_{A,m}(ξ;.) = K^{X_A'}_{A,T_M^g m}(T_Ξ^g ξ;.)

Every other target object in §7 is primed (`C_A'`, `P_I'`, `Pi'_{I,o',X'}`), but the evaluator is
disambiguated only by the superscript. On the diagonal fiber `chi_A(X) = chi_A(X')` the two strings
become identical while denoting kernels into different spaces `W_A` and `W_A'`. That is a genuine
ambiguity. Its blast radius is nil for correctness: (7.6) is a *hypothesis* of an optional branch
("model evaluation is covariant **only when** the additional kernel identity (7.6) holds"), so the
degenerate reading yields a stronger assumption, never a false conclusion. `X_A'` is also never
defined anywhere in the package (only `:453` and the review echo at `view-gauge-holonomy.md:113` use
it); presumably `chi_A(X')`.

**(c) The superscript is misleading in isolation.** The document evidently felt the hazard — it wrote
a caveat at `:190` and again at `:498` and again at `:6`. A reader who opens §4 cold can misread it.
That is a real reason to change the symbol, and it is the whole of the defect.

## 8. Relation to P0

`P0-principal-reviewer-notes.md` contains no reconstruction touching §4, the evaluator, or the `X_A`
superscript; its verified items are the parent-posterior-version identity, parent absolute
continuity, the additive KL chain, and the recovery/DPI-equality theorem. **No contradiction with P0
arises**, and P0's general assessment ("the fencing is unusually careful and honest") is consistent
with what I found here: the cross-`X` non-claim is one of the most heavily fenced statements in the
package, including a pre-registered adversarial attack against exactly this charge.

## 9. Verdict

**UPHELD_REDUCED. Corrected severity: Low.** Category: notation hygiene / internal artifact
consistency, not correctness, not a proof gap.

- (4.5) is **not** false. It is (4.3) with a defined symbol substituted, and it is true at the fixed
  `X` the theorem declares.
- The normative-violation charge is **refuted** by the registry's own `type`/`domain_codomain` fields,
  which type neither `ev_A` on `X_A` nor `ev_i` on `X`.
- The "caveat is local" charge is **refuted** by `direct-derivation.md:6` plus nine further fences the
  investigator did not cite, including the package's own pre-registered attack A15.
- The counterexample is arithmetically sound but targets a proposition the document already asserts.
- Nothing downstream uses `X_A`-determination; the superscript is inert.
- The proposed Fix is correct and should be applied: write `K^X_{A,m_A}` (or keep `G_A^X`) for the
  induced object and reserve `K^{X_A}` for the predeclared tier, matching what `claim-ledger.json`
  already says. Extend it to (7.6) and define `X_A'`.

## Falsifier of this attack

My verdict is wrong if a step anywhere in the package *derives* a conclusion from the premise that
the induced evaluator is determined by `X_A` — i.e. an inference `chi_A(X)=chi_A(X') ⇒ K equal`, an
integral or measurability argument in `X_A`, or a single `X_A`-indexed evaluator quantified over more
than one `X` in a conclusion rather than a hypothesis. I enumerated all fifteen occurrences of the
token across `direct-derivation.md`, `construction-or-strongest-theorem.md`, `notation-standard.md`,
`approach-registry.json`, `claim-ledger.json`, and `evidence/reviews/`, and found none; (7.6) is the
only two-`X` site and it is a hypothesis. If such a step exists in a file I did not enumerate, the
notation is load-bearing, the finding becomes a correctness defect, and High is correct.

Secondarily, my verdict is wrong if `\operatorname{ev}_A`'s registry entry is not the operative type
declaration for `K^{X_A}` — e.g. if `Theory/SPEC.md` or `Theory/appendix_notation.tex` (both listed as
its `canonical_sources`) types the parent evaluator with `X_A` in its domain. I did not check those
two files; that is the one open obligation in this attack.
