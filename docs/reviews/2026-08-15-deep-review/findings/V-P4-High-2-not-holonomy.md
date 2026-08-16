# Skeptic attack: P4-High-2-not-holonomy

STATUS: COMPLETE

- Target finding: `P4-High-2-not-holonomy`, stated severity **High**
- Finding text: `docs/reviews/2026-08-15-deep-review/findings/P4-gauge-holonomy.md:80-100`
- Location under attack: `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md` §7 (lines 381-463)
- Revision: `8ce635807a6ca2a388255fc996c98f7c535e5843`, branch `review/2026-08-15-deep-review`

## VERDICT: UPHELD_REDUCED — correct severity **Medium**, corrected scope below

The factual core survives every attack I could mount: §7 constructs and uses no connection, no
parallel transport along anything, no loop, and no curvature, and it never relates its arrows to the
holonomy structures this program does define. I verified that by reading §7 in full, by re-deriving
its theorem, and by executed search. Three things in the finding do not survive: the absolute
headline ("**Nothing** in §7 is holonomy") is false as literally written; the finding misses that
§7's name is *inherited* from `thm:cg-holonomy-kl-marginal` in `Theory/06`, whose acting group
`𝔥_I^x(r) = {T_λ^x : λ : r→r}` genuinely is a holonomy group (§2b below), which changes the defect
from "unearned decoration" to "a generalization that silently widened the acting group and kept the
name"; and **High** overstates a defect that invalidates no statement and no inference in the
package.

**Corrected finding statement.** §7 generalizes `Theory/06`'s holonomy-stabilization from marginals
to full laws by replacing the based-loop transport group with an unrestricted groupoid of supplied
bimeasurable isomorphisms, and retains the name "holonomy" for the widened object without recording
that the loop structure was dropped. No passage relates `T_I^g`, `T_A^g`, or `T_H^g` to the edge
transports, path transports, based-cycle holonomies, or root-frame changes this program defines.
Severity **Medium**: a scope-description defect in a certified target conjunct and in an
`\status{ESTABLISHED}` manuscript paragraph, invalidating no mathematics.

---

## 1. What §7 actually proves — my own reconstruction

§7's entire mathematical content is: for an arrow `g:(o,X)→(o',X')` with bimeasurable
`T_O^g, T_I^g, T_A^g`, hypotheses (7.1)-(7.4) imply (7.5). I reconstructed the load-bearing step
without reading either party's prose. For measurable `D ⊆ Z_A'` and any fine law `μ` on `Y_I`:

    [(T_A^g)_#(μ C_A)](D) = (μ C_A)((T_A^g)^{-1} D)
                          = ∫ C_A(Y, (T_A^g)^{-1} D) μ(dY)
                          = ∫ C_A'(T_I^g Y, D) μ(dY)          [(7.4), applied left-to-right]
                          = ∫ C_A'(Y', D) [(T_I^g)_# μ](dY')  [change of variables, T_I^g bimeasurable]
                          = ([(T_I^g)_#μ] C_A')(D).

Set `μ = Π_{I,o,X}` and apply (7.2); set `μ = Q_{I,o,X}` and apply (7.3); adjoin `T_O^g` and apply
(7.1) for the generative half. That is (7.5). The identity is correct, and the orientation of the
inverse image in (7.4) is on the correct side.

The complete list of structure this uses is: bimeasurability of `T_I^g` and `T_A^g`; the intertwining
(7.4); the three pushforward hypotheses; and, for the family, groupoid composition/inversion so that
arrows compose. **Nothing else enters.** No connection form, no horizontal distribution, no path, no
lift, no loop, no curvature is available to enter, because none is defined anywhere in §7. The result
is the standard equivariance fact for Markov kernels — an equivariant kernel carries covariant laws
to covariant laws — stated over a groupoid of measurable isomorphisms rather than a group.

I also checked the one structural escape that would rescue the name: a groupoid can carry a
connection if it fibers over a base groupoid and one chooses a cleavage/splitting, in which case
holonomy is the failure of that splitting to be functorial on loops. §7 has no base groupoid and no
fibration; the actions are *given directly on the arrows*, so there is no second object over which
two different arrows could sit and hence no possible curvature. The escape is unavailable.

**Executed check** (`sed -n '381,463p' direct-derivation.md | grep -inE "connection|transport|loop|curvature|cycle|parallel|edge|graph|path"`):

    81:The alternative is exact retention rather than blindness. Declare (\mathsf H_A) to include
       measurable component roots, the raw root-framed based-holonomy representation, and dressed
       boundary marks, ... No quotient by conjugacy, averaged group element, path erasure, or
       holonomy-blind invariance is asserted. ...

One hit in 83 lines, and it is the *retention* paragraph (line 461), matching on "path erasure".
Zero hits for `connection`, `transport`, `loop`, `curvature`, `cycle`, `parallel`. The investigator's
grep reproduces.

## 2. Attack A — is "holonomy" declared in a technical sense this program supplies? NO, and the
   program's actual definition makes the usage worse, not better

This was the strongest available kill and it fails in the opposite direction. The program *does*
define holonomy, precisely, in at least three places, and §7's object is not an instance of any of
them:

- `Theory/02_geometry.tex:590-597`, `eq:geo-link-holonomy`: for a closed edge-labeled walk
  `γ=(e_0,…,e_{r-1})` with `i_r=i_0`, `H^x(γ) = ∏_a Θ_{e_a}^x`, `\status{ESTABLISHED}`. Closed walk,
  ordered product of link elements. Theory/02:637-639 even warns that "graph holonomy and
  base-connection holonomy are unrelated" absent a curve assignment — i.e. the manuscript is
  scrupulous about the word elsewhere.
- `Theory/appendix_notation.tex:291`: "represented graph holonomy group and its closure in the
  represented matrix group".
- `docs/derivations/2026-08-14-pointwise-meta-agent-rg/evidence/direct-derivation.md:16-38,54`: edge
  transports `T_{ij}^x : Z_j^x → Z_i^x` with `T_{ji}=(T_{ij})^{-1}`, ordered path transport `T_γ^x`,
  based-cycle holonomy `H_c^x`, a reciprocal path groupoid, fundamental cycles from a rooted spanning
  tree, and `ker L_x ≅ Fix(Hol_r^x)`. That is a genuine discrete connection with genuine loops.

§7's groupoid has objects `(o,X)` — an admitted observation paired with fixed structural data — not
vertices, not base points, not fibers. Its arrows are supplied bimeasurable bijections. Nothing in
the frozen bytes identifies `T_I^g` or `T_A^g` with `T_{ij}^x`, `T_γ^x`, `H_c^x`, the graph
fundamental group, or a change of root frame. I searched the whole 08-15 package for that bridge:

    grep -rniE "root[- ]gauge|conjugat|frame change|change of root|change of frame|T_H" *.md *.json evidence/
    → evidence/direct-derivation.md:451   (T_B^g × T_O^g × T_H^g)_#          [the only T_H occurrence]
    → evidence/reviews/view-gauge-holonomy.md:111  (the same formula, quoted)

`T_H^g` exists as a component action on the `H_A` factor in (7.6) and is never said to be conjugation
by a root-frame change or anything else. The 08-15 `notation-standard.md:23,33` lists `H_A` as a
factor of `Z_A` with **no gloss at all** — it never says `H_A` is a holonomy record space, so the
package does not even declare the naming convention locally.

The package's own gauge reviewer reaches the same structural conclusion:
`evidence/reviews/view-gauge-holonomy.md:175` — "the abstract joint groupoid is extra application
data; it is not automatically reconstructed from the separate marginal path groupoids", and `:79` —
"Existence or uniqueness of such a joint lift is not derived from marginal holonomy, and the theorem
does not claim it." So the missing bridge is acknowledged inside the frozen bytes, and the "the
investigator misread it" kill is unavailable.

Standard terminology also has a correct name for what §7 built, and it is not holonomy. The groupoid
whose objects are base points and whose arrows are equivariant fiber isomorphisms is the
Atiyah/gauge groupoid, `Mor(At(P)) = (P×P)/G`; a connection is *additional* data (a functor from the
path groupoid, equivalently a splitting of the Atiyah sequence, with curvature the obstruction to
splitting as Lie algebroids), and holonomy is what that additional data produces on loops. Holonomy
itself is defined only relative to a connection and a loop: "Given connection on a bundle ∇ over a
space X, its parallel transport around some loop γ:[0,1]→X, γ(0)=γ(1)=x₀ yields an element
hol_∇(γ) ∈ G in the automorphism group of the fiber" (nLab, *holonomy*). Ambrose–Singer, *A theorem
on holonomy*, Trans. Amer. Math. Soc. **75** (1953) 428-443, is real and says what the investigator
says it says: the curvature form generates the holonomy group. (I could not verify the
Kobayashi–Nomizu locator at section granularity — "Vol. I, Ch. II §4" is an unchecked pin. It is not
load-bearing; the definitional point is settled by the two sources above.)

So the escape hatch named in my brief — "if the term is used in a defined technical sense declared
elsewhere, this reduces to terminology" — does not apply. The program's declared technical sense is
the graph holonomy, and §7 does not instantiate it. That makes the label a *collision with this
program's own notation*, not a harmless local convention.

The collision is sharper than the finding says, and this is the one place I would strengthen it.
`Theory/11_obstructions.tex:422` states: "Chapter~\ref{ch:geometry} distinguishes **three
holonomies**, and everything in this section uses only graph-link holonomy … Neither side of
\eqref{eq:obs-tension} refers to the base holonomy of a smooth connection along curves of `\mathcal
C`." The manuscript therefore maintains an explicit three-way taxonomy (graph-link, base-connection,
represented) and polices it chapter by chapter. §7's usage is a **fourth, undeclared** sense. Worse,
the program already has a precise name for §7's kind of object: `Theory/02_geometry.tex:700-708`
defines the represented frame change `R_i^b=\rho_b(g_i)`, `R_i^m=\rho_m(g_i)` induced by a principal
section rechoice `u_i'=u_i g_i^{-1}` — a *gauge transformation*, not a holonomy. A groupoid of
supplied measurable isomorphisms acting on the fine and parent spaces is the measurable analogue of
that, and its isotropy at `(o,X)` is a gauge stabilizer; the holonomy subgroup is what a connection
would carve out of it.

## 2b. The best defense of the package, which the finding does not consider: the name is inherited
   from a genuine holonomy statement that §7 generalizes

This is the one thing my attack turned up that materially changes how the defect should be described,
and it is not in the finding.

§7's opening sentence (line 383) says the proof "starts from full-law covariance data rather than
from marginal stabilization such as `h_# q_A^x = q_A^x`". That `h` is not decorative. In
`Theory/06_general_coarsegraining.tex:564-601` the canonical theory defines, for a root `r` and paths
`γ_i : i → r`,

    P_i^x = (T_{γ_i}^x)_# q_i^x,
    𝔥_I^x(r) = { T_λ^x : λ : r → r },                       [based loop transports]
    𝒬_{I,fix}^x(r) = { Q ∈ ℳ_r^x : (H)_# Q = Q for every H ∈ 𝔥_I^x(r) },

and `thm:cg-holonomy-kl-marginal` characterizes zero forward-KL score as a "holonomy-stabilized
parallel marginal-law section". There `𝔥_I^x(r)` is a genuine holonomy group — loops based at `r`,
transported by the graph connection — and "holonomy-stabilized" is fully earned.

§7 is the full-law generalization of exactly that statement: `(H)_# Q = Q` with `H` ranging over loop
transports becomes `(T_A^g)_# Π_A = Π_A` with `T_A^g` ranging over *arbitrary supplied* bimeasurable
isomorphisms. So the word is not conjured from nothing; it is inherited from a predecessor whose
acting group was a real holonomy group. **The defect is that the generalization silently widened the
acting group from `𝔥_I^x(r)` to an unrestricted groupoid and kept the name, without a sentence
recording that the loop structure — the thing that made the earlier name correct — had been dropped.**
That is a precise, small, and genuine defect, and it is a labeling defect.

## 3. Attack B — the headline is too strong; the retention branch IS about holonomy

Here the finding loses ground. §7 line 461 declares `H_A` to contain "measurable component roots, the
**raw root-framed based-holonomy representation**, and dressed boundary marks" and requires `C_A` to
output them jointly. Those records are exactly the `H_c^x` / rooted-tree-framed objects of the 08-14
construction (`2026-08-14.../direct-derivation.md:251-316`; `Theory/07b:1618-1673` gives the
simultaneous root-framed state `(root feature, H_I^x, {V_e^x})`). Equation (7.6) carries a component
action `T_H^g` on that same factor. So §7 *does* reference genuine holonomy data of this program;
what it does not do is prove anything with connection-theoretic content, or connect its arrows to
those records.

The investigator's own Evidence paragraph concedes this ("the retention paragraph at line 461, which
refers to records produced by the 08-14 *graph* construction") and the Fix proposes exactly the
missing `T_H^g` bridge — so the body is accurate and only the title and the four-bullet "Defect"
list overreach. Correct statement of the defect:

> No theorem in §7 has connection-theoretic content. The blindness branch is covariance of a Markov
> kernel under a groupoid of measurable isomorphisms, and no passage relates `T_I^g`, `T_A^g`, or
> `T_H^g` to the edge transports, path transports, based-cycle holonomies, or root-frame changes that
> this program defines. The retention branch names real holonomy records but proves only that a
> pushforward through a kernel whose codomain contains them retains their joint law.

## 4. Attack C — severity. High is not supported

`High` in this review is doing work it has not earned here.

1. **No statement in §7 is false and no inference fails.** (7.1)-(7.6) are hypotheses on supplied
   data, not assertions about constructed objects; the derivation of (7.5) is correct (§1 above); the
   same-slice restriction at line 459 is correctly fenced. The finding identifies no defective
   mathematics — its own remedy (a) is a rename.
2. **The document's own summary already states the correct content.** `direct-derivation.md:496`:
   "Section 7 proves **full-law covariance** under the complete joint hypotheses and supplies raw
   holonomy retention as the alternative." `final-report.md:40`: "Holonomy blindness is a full-law
   statement under explicit action/version/evaluator hypotheses." `Theory/SPEC.md:822` and
   `Theory/appendix_claim_ledger.tex:208` restate it conditionally and accurately. The loose noun
   survives in the §7 heading, the phrase "holonomy-blind covariance theorem" (line 463), and the
   claim/assumption ids — i.e. in labels, while every prose statement of the content is right.
3. **The theorem is a schema over supplied actions.** `ASM-HOLONOMY-ALTERNATIVE-DECLARATION`
   (`claim-ledger.json:15`) and the contract's "declared joint fine and parent holonomy actions"
   (`problem-contract.json:51`) make the actions an *input*. An applier who supplies represented
   graph-holonomy or root-gauge actions instantiates the schema honestly. The name is broader than
   the content; it is not a claim the content contradicts.
4. **Nothing downstream leans on the mislabel.** I searched every use of "holonomy-blind" in
   `Theory/` and `docs/derivations/`: `Theory/07b:1790,1808`, `Theory/SPEC.md:822`,
   `Theory/appendix_claim_ledger.tex:208`, and ledger/DAG ids. None derives a flatness, curvature,
   loop-independence, or transport conclusion from §7. The defect propagates as a name, not as a
   false consequence.

What keeps it above `Low`: the mislabel sits inside a certified target conjunct ("establish exactly
one declared full-law holonomy alternative", `claim-ledger.json:210`, state `EVIDENCE_VERIFIED`) and
has been copied into the canonical manuscript at `Theory/07b:1787-1810` under `\status{ESTABLISHED}`,
immediately after the root-gauge discussion and reusing `g` — where a reader who knows
`eq:geo-link-holonomy` will mis-scope it. A certified conjunct that misnames its own subject inside a
manuscript that defines that subject precisely is a real, fixable scope-description defect.
**Medium.**

## 5. Relation to the principal reviewer's notes

No contradiction. `P0-principal-reviewer-notes.md` reconstructs statements 1, 4, and the recovery
theorem; it does not reconstruct §7, and it records the panel's §7 concern approvingly at :233. P0
does set a precedent that a non-correctness defect can be High (:235) — but P0's High is for the
flagship theorem being a re-derivation of results already `ESTABLISHED` in the same repository, which
changes what the release *is*. A branch name that overstates its subject while the branch's stated
content is accurate is a smaller thing, and grading both High flattens a distinction the final report
needs.

## 6. Also refuted along the way

- "The investigator asserted a counterexample without exhibiting one" — not applicable; this finding
  rests on absence of structure, and the absence is mechanically checkable (§1).
- "The standard result they cite does not say what they claim" — checked; nLab's definition and
  Ambrose–Singer both support the investigator. Only the Kobayashi–Nomizu section pin is unverified.

## FALSIFIER OF MY OWN ATTACK

Primary: exhibit a passage in the frozen bytes (or in `Theory/`) that draws a connection-theoretic
conclusion *from* §7 — flatness, curvature, loop-independence, path erasure, or a claim that the
parent cannot detect a based-cycle holonomy `H_c^x` — or that declares `T_H^g` to be conjugation by a
root-frame change on the retained records. Either would make the mislabel load-bearing on a
mathematical conclusion rather than on a name, and `High` would be correct. I searched for both and
found neither (§2, §4.4). I then closed the obvious residual gap: every "holonomy" occurrence in
`Theory/11_obstructions.tex` (19) and `Theory/12_philosophy.tex` (14) is about graph-link holonomy in
the Gaussian reciprocal-pair and operational-trace arguments — `11:37,51,90,332-393,422` and
`12:104-154,231,305-342` — and none cites, uses, or depends on §7. I also enumerated every "holonomy"
line in `Theory/06_general_coarsegraining.tex` (22) and `Theory/09_coarsegraining.tex` (32): all are
genuine graph-holonomy statements predating this work — `06:542-744` (holonomy-conditioned
marginal-law modes, based loop transports, conjugation of the holonomy group under a root change) and
`09:375-431,630-824,1058-1062` (kernel–holonomy fixed-space isomorphism, fundamental-cycle
holonomies, loop-holonomy actions on transported laws) — and none derives from §7. So the mislabel is
nowhere load-bearing in the manuscript. What I did **not** do is read `Theory/06` and `Theory/09` in
full, only every holonomy-bearing line and its context.

Secondary: if this review's rubric treats "a certified target conjunct misnames its subject" as High
by the same standard P0 applied to attribution, my reduction to Medium is a rubric disagreement, not
an evidentiary one, and the finding stands at High.

## Sources checked (not from memory)

- nLab, *holonomy* — definition requiring a connection, parallel transport, and a based loop:
  https://ncatlab.org/nlab/show/holonomy
- nLab, *Atiyah groupoid* — objects `X`, morphisms `(P×P)/G` (equivariant fiber isomorphisms); a
  connection is a further splitting/path-groupoid functor, curvature its obstruction:
  https://ncatlab.org/nlab/show/Atiyah+groupoid
- W. Ambrose and I. M. Singer, "A theorem on holonomy", *Trans. Amer. Math. Soc.* **75** (1953)
  428-443 — the curvature form generates the holonomy group (citation verified):
  https://www.semanticscholar.org/paper/A-THEOREM-ON-HOLONOMY-Ambrose-Singer/2b6b62dba8279e4b28869cfb5d41851fc64bf78c
- A. S. Bandeira, A. Singer, D. A. Spielman, "A Cheeger Inequality for the Graph Connection
  Laplacian", *SIAM J. Matrix Anal. Appl.* **34**(4) (2013) 1611-1630 — the graph connection
  Laplacian the 08-14 package's `ker L_x ≅ Fix(Hol_r^x)` belongs to:
  https://epubs.siam.org/doi/10.1137/120875338
- NOT verified: the Kobayashi-Nomizu locator "Vol. I, Ch. II §4". Not load-bearing.
