# P4 — Gauge theory / fiber bundles / holonomy — adversarial review

STATUS: COMPLETE
Counts: Critical 0 / High 2 / Medium 5 / Low 1
Reviewer: independent investigator (gauge theory & fiber bundles)
Target revision: 8ce635807a6ca2a388255fc996c98f7c535e5843 (branch review/2026-08-15-deep-review)
Diff base: 060f80e5556e41e0f31aeafcd9ef8564c1544c16^

## Files to examine

- [x] docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md (read in full)
- [x] docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/reviews/view-gauge-holonomy.md (read in full)
- [x] docs/derivations/2026-08-15-full-pointwise-meta-agent/construction-or-strongest-theorem.md (read in full)
- [x] docs/derivations/2026-08-15-full-pointwise-meta-agent/claim-ledger.json (holonomy entries)
- [x] docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/counterexample-proofs.md §5
- [x] docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation-standard.md
- [x] docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation-registry.json
- [x] docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation_scan.py (hazard detector)
- [x] docs/derivations/2026-08-14-pointwise-meta-agent-rg/evidence/direct-derivation.md §1-2, §7
- [x] commit 3f5f49b "docs: correct scale-bundle notation" (full diff)
- [x] git diff -- Theory/02_geometry.tex (complete)
- [x] Theory/05c_pullback_geometry.tex §scale-connection-defect + all `\mathscr P` occurrences
- [x] git diff -- Theory/appendix_notation.tex (complete)
- [x] git diff -- overview.md (complete)
- [x] git diff -- Theory/07b_agent_network_rg.tex (complete)
- [x] Theory/07_general_renormalization.tex:140-270 (scale bundle, added for the bundle-split question)
- [x] evidence/adversarial-attacks.md A9-A12, A16

---

## Findings

### [High] "Holonomy blindness" is inherited invariance, not blindness; the hypotheses exclude the only case in which the word "blind" would carry content

**Location:** `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md` §7 (lines 381-463); `claim-ledger.json` claim `HOLONOMY-BLIND-FULL-LAW` and assumption `ASM-HOLONOMY-BLIND-DATA`; `construction-or-strongest-theorem.md:94`.

**Claim as stated:**
- direct-derivation.md:459 — "Equation (7.5) is covariance between source and target slices. Same-slice invariance follows only for isotropy arrows that fix the declared (X) and admitted (o), preserve the selected versions, and identify the source and target spaces."
- direct-derivation.md:463 — "A concrete parent declaration chooses its semantics: either it invokes the **holonomy-blind covariance theorem** under (7.1)--(7.6), or it retains the raw records and declines a blindness claim."
- claim-ledger.json `HOLONOMY-BLIND-FULL-LAW` — "Under typed source/target groupoid actions, full fine-law covariance, compatible selected posterior versions, recognition covariance, C_A equivariance, and evaluation covariance, full parent generative, posterior, and recognition laws are covariant; same-slice invariance follows only on the fixed-(o,X) stabilizer."

**Defect:** The same-slice ("blindness") statement is a one-line corollary in which the substantive content is *assumed at the fine level*, and the case that would make the word "blindness" mean anything is *excluded by hypothesis*.

Specialize the arrow `g` to an isotropy arrow: `(o',X') = (o,X)`, source and target spaces identified, so `C_A' = C_A`, `Π'_{I,o',X'} = Π_{I,o,X}`, `Q'_{I,o',X'} = Q_{I,o,X}`. Then hypotheses (7.2) and (7.3) read

    (T_I^g)_# Π_{I,o,X} = Π_{I,o,X},     (T_I^g)_# Q_{I,o,X} = Q_{I,o,X}.

That is: **the fine datum is assumed invariant under the action.** The conclusion (7.5) restricted to the same slice is

    (T_A^g)_# Π_{A,o,X} = Π_{A,o,X},     (T_A^g)_# Q_{A,o,X} = Q_{A,o,X},

which follows in one line from (7.4) by the change-of-variables computation the package itself gives. Nothing about coarse-graining is used, and nothing is erased: the parent is invariant *because the fine level already was*. Nothing here is peculiar to a coarse channel — the same statement holds for any equivariant map applied to any invariant measure.

The reading a gauge theorist takes from "the parent datum is blind to holonomy on the same slice" is the opposite: that the parent *cannot detect* a gauge motion that the fine level *does* detect. Formally that statement is

    (∗)  [(T_I^g)_# Π_{I,o,X}] C_A = Π_{I,o,X} C_A   with   (T_I^g)_# Π_{I,o,X} ≠ Π_{I,o,X},

which is equivalent (for all fine laws) to **channel invariance** `C_A(T_I^g Y, ·) = C_A(Y, ·)`, i.e. `C_A` constant on `T_I^g`-orbits. That is a genuine, nontrivial, easily stated theorem — and the package never states it. Worse, its hypothesis set forbids the witness: (7.2)/(7.3) at an isotropy arrow force `(T_I^g)_# Π_{I,o,X} = Π_{I,o,X}`, so no datum satisfying `ASM-HOLONOMY-BLIND-DATA` can exhibit (∗) with a strict inequality. **The certified "blindness" branch is, on its own hypotheses, incapable of exhibiting any blindness.**

**Evidence (reconstruction).** The forward computation, which I checked and which is correct:

    [(T_A)_#(μ C_A)](D) = (μ C_A)((T_A)^{-1}D)
                        = ∫ C_A(Y,(T_A)^{-1}D) μ(dY)
                        = ∫ C_A'(T_I Y, D) μ(dY)            [by (7.4)]
                        = ∫ C_A'(Y',D) μ'(dY')              [μ' = (T_I)_#μ]
                        = (μ' C_A')(D).

Set `μ = Π_{I,o,X}`, `μ' = (T_I)_#Π_{I,o,X}`. On the same slice, (7.2) says `μ' = μ`, hence the right-hand side is `Π_{I,o,X}C_A = Π_{A,o,X}` and the left is `(T_A)_#Π_{A,o,X}`. The entire content of the conclusion is the substitution `μ' = μ`, which is hypothesis (7.2). This is inheritance of invariance under an equivariant map, a standard one-line fact (see e.g. the elementary equivariance lemma for Markov kernels: if `K` intertwines group actions and `μ` is `G`-invariant then `μK` is `G`-invariant).

**Non-vacuity of the surrounding hypotheses (reported honestly):** the hypothesis set is *not* vacuous. A nontrivial model of (7.2)-(7.4) with `T_I ≠ id` and `T_A ≠ id`: let `Y_I = {0,1}^2`, `Z_A = {0,1}`, `C_A(y,·) = δ_{y_1 ⊕ y_2}` (parity), `T_I(y_1,y_2) = (1⊕y_1, y_2)`, `T_A(z) = 1⊕z`. Then `C_A(T_I y, D) = δ_{1⊕y_1⊕y_2}(D) = δ_{y_1⊕y_2}(T_A^{-1}D) = C_A(y, T_A^{-1}D)`, so (7.4) holds with both actions nontrivial. Taking `Π = Q =` uniform on `{0,1}^2` satisfies (7.2)-(7.3). So the theorem has models; the finding is not that it is empty, it is that its conclusion is its hypothesis pushed through an assumed-equivariant map.

**Falsifier:** Exhibit a datum satisfying `ASM-HOLONOMY-BLIND-DATA` with an isotropy arrow `g` such that `(T_I^g)_# Π_{I,o,X} ≠ Π_{I,o,X}` while `Π_{A,o,X}` is `T_A^g`-invariant. If such a datum exists, the "blindness" reading has content under the stated hypotheses and this finding is wrong. (I claim none exists: (7.2) at an isotropy arrow with identified source/target spaces is literally `(T_I^g)_# Π_{I,o,X} = Π'_{I,o,X} = Π_{I,o,X}`.)

**Fix (smallest repair).** Two edits, both cheap:
1. Rename the claim and the branch. `HOLONOMY-BLIND-FULL-LAW` should be `PARENT-COVARIANCE-UNDER-EQUIVARIANT-CHANNEL`, and §7's "holonomy-blind covariance theorem" should read "covariance/inherited-invariance theorem". State plainly: *the parent inherits whatever invariance the fine datum is assumed to have.*
2. If a blindness statement is actually wanted, add the one-line theorem that supplies it: **if `C_A(T_I^g Y, D) = C_A(Y, D)` for all `Y, D` (channel invariance, i.e. `T_A^g = id` in (7.4)), then `[(T_I^g)_#μ]C_A = μC_A` for every fine law `μ`, with no hypothesis on `Π_I` or `Q_I`.** That is the genuine erasure statement, it is strictly not implied by (7.1)-(7.6), and it is proved by the same three lines.

---

### [High] Nothing in §7 is holonomy: no connection, no parallel transport, no loop, no curvature — the "holonomy" branch is invariance under an abstract groupoid of measurable isomorphisms

**Location:** `direct-derivation.md` §7 heading (line 381) and lines 385-463; `claim-ledger.json` target statement ("establish exactly one declared full-law holonomy alternative"); `view-gauge-holonomy.md` throughout.

**Claim as stated:** direct-derivation.md:381-393 — "## 7. Full-law holonomy alternatives … Let an arrow (g:(o,X)\to(o',X')) have bimeasurable actions `T_O^g`, `T_I^g`, `T_A^g` … Assume composition and inverses agree with the groupoid laws."

**Defect:** The objects of this groupoid are pairs `(o,X)` — an admitted observation and a fixed structural datum. They are not points of a base manifold, not points of `U_A`, and not fibers of any bundle. The arrows are bimeasurable bijections of standard-Borel spaces. There is:
- no connection form and no horizontal distribution anywhere in §7;
- no parallel transport (nothing is transported along anything);
- no loop in any base space — the "same-slice" specialization is an arrow from the object `(o,X)` to itself in an abstract groupoid, i.e. an element of an isotropy group, not the holonomy of a loop;
- no curvature and therefore no possible statement about flatness, and no Ambrose–Singer content.

Holonomy is defined for a connection on a bundle as the group of parallel-transport maps around loops based at a point (Kobayashi–Nomizu, *Foundations of Differential Geometry* I, Ch. II §4; Ambrose–Singer 1953). The §7 construction has none of the ingredients. Calling `T^g` a holonomy is a naming choice with no supporting structure. The document is explicit that the construction "is pointwise in this one `X`" and "supplies no … full geometric section over `U_A`" (line 498) — so there is no base along which anything could be transported and no loop for a holonomy to be taken around.

The package's *own* genuine holonomy lives elsewhere: the released 2026-08-14 package defines edge transports `T_{ij}^x : Z_j^x → Z_i^x` on a positive-support graph, path transports `T_γ^x`, based cycle holonomies `H_c^x`, a reciprocal path groupoid, and the connection-Laplacian identity `ker L_x ≅ Fix(Hol_r^x)` (`docs/derivations/2026-08-14-pointwise-meta-agent-rg/evidence/direct-derivation.md:6-60`). That *is* a discrete connection (a gain graph / connection graph in the sense of Zaslavsky; the Laplacian statement is the Singer–Wu / Bandeira–Singer–Spielman connection-Laplacian kernel result), with genuine loops and genuine holonomy. §7's abstract `(o,X)` groupoid is a different object entirely, and §7 never relates `T_I^g` or `T_A^g` to the edge transports `T_{ij}^x`, to the graph fundamental group, or to any change of root frame.

**Evidence:** grep of §7 (direct-derivation.md:381-463) for `connection`, `transport`, `loop`, `curvature`, `cycle`, `parallel`: zero hits. The only occurrences of "holonomy" in §7 are (i) the section heading, (ii) the phrase "typed holonomy groupoid" at line 383, and (iii) the retention paragraph at line 461, which refers to records produced by the 08-14 *graph* construction. The blindness half of the "alternative" therefore never touches holonomy at all.

**Falsifier:** Point to a connection, a horizontal lift, or a loop in §7 from which `T_I^g` or `T_A^g` is constructed; or a stated correspondence `T^g = Hol_c^x` for some cycle `c` of the 08-14 graph.

**Fix:** Either (a) restate §7's first half honestly as "covariance of the parent datum under a typed groupoid of measurable symmetries", dropping "holonomy" from the heading, the claim id, and the assumption id; or (b) supply the missing bridge — declare `T_H^g` to be the change-of-root-frame/conjugation action on the retained root-framed holonomy records of the 08-14 construction, and *then* the word is earned. Option (b) is the substantive repair and is not currently done anywhere in the package.

---

### [Medium] The two "holonomy alternatives" are statements about different mathematical objects, so the dichotomy is not a dichotomy

**Location:** `direct-derivation.md:463`; `construction-or-strongest-theorem.md:94`; `claim-ledger.json` claim `HOLONOMY-ALTERNATIVE`.

**Claim as stated:** direct-derivation.md:463 — "A concrete parent declaration chooses its semantics: either it invokes the holonomy-blind covariance theorem under (7.1)--(7.6), or it retains the raw records and declines a blindness claim."

**Defect:** Branch A is a statement about invariance of the parent laws under an abstract `(o,X)`-groupoid action. Branch B is a statement about what the *state space* `H_A` and the channel `C_A` are declared to contain (component roots, root-framed based-holonomy representation, dressed boundary marks). These are not two answers to one question; they are answers to two unrelated questions. Nothing prevents a single parent from satisfying both simultaneously — e.g. `H_A` retains the full root-framed record *and* the datum happens to be invariant under some measurable symmetry `T^g`. The package half-acknowledges this ("does not assert logical exclusivity, because blindness and retention can coexist for different retained coordinates or quotient levels", construction:94), but then still frames the two as an "either/or" that a declaration must choose between, and the certified target conjunct is "establish exactly one declared full-law holonomy alternative". "Exactly one" of two non-exclusive, non-comparable statements is not a mathematical condition; it is a documentation convention.

**Evidence:** Branch A's conclusion quantifies over arrows `g` of the `(o,X)` groupoid and constrains `P_A, Π_A, Q_A`. Branch B's conclusion is `(3.1)` and `(3.4)` applied to a channel whose codomain factor `H_A` contains the records — i.e. it is the *definition* of pushforward, restated. Branch B asserts nothing that is not already true of every `C_A` in §§1-3: "full parent pushforwards retain their joint laws and correlations" (`HOLONOMY-RETENTION`) is true of any Markov-kernel pushforward by construction and has no holonomy content whatsoever. Its only content is the declaration that `H_A` is big enough — a typing decision, not a theorem.

**Falsifier:** Exhibit a parent datum for which branches A and B are provably incompatible, or a nonvacuous consequence of `HOLONOMY-RETENTION` that does not follow from "the pushforward of a law through a Markov kernel is a law".

**Fix:** Demote `HOLONOMY-RETENTION` from a theorem to a *definition/typing declaration* (which is what it is), and replace the "either/or" with "these are independent declarations; a parent may make both".

---

### [Medium] "Isotropy" is redefined to include stabilization of the data, and the ledger's restatement drops the data half

**Location:** `direct-derivation.md:459`; `claim-ledger.json` `HOLONOMY-BLIND-FULL-LAW` and `ASM-HOLONOMY-BLIND-DATA`.

**Claim as stated:**
- derivation:459 — "Same-slice invariance follows only for isotropy arrows that fix the declared (X) and admitted (o), preserve the selected versions, and identify the source and target spaces."
- ledger `HOLONOMY-BLIND-FULL-LAW` — "same-slice invariance follows only on the **fixed-(o,X) stabilizer**."
- ledger `ASM-HOLONOMY-BLIND-DATA` — "same-slice invariance additionally restricts to the **stabilizer of fixed o and X**."

**Defect:** Two distinct notions are being run together, and the ledger keeps only the weaker one.
- *Isotropy group of the groupoid object* `(o,X)`: arrows `g : (o,X) → (o,X)`. This is a condition on the **action** (typing).
- *Stabilizer of the datum*: arrows with `(T_I^g)_# Π_{I,o,X} = Π_{I,o,X}` and `(T_I^g)_# Q_{I,o,X} = Q_{I,o,X}`. This is a condition on the **data**.

The load-bearing hypothesis is the second. The derivation's restrictive clause "preserve the selected versions" smuggles it in under the name "isotropy". The ledger statement, which is what the certification actually records as `EVIDENCE_VERIFIED`, says only "the fixed-(o,X) stabilizer" — which, read with the standard meaning of "stabilizer of a point of the object set", is the isotropy group and does *not* by itself give same-slice invariance.

Answering the review question directly: **the isotropy hypothesis, as written, is an assumption about the data wearing the name of an assumption about the action.** (It is technically recoverable: under the blanket assumption that every arrow of the groupoid satisfies (7.2)-(7.3), an isotropy arrow automatically stabilizes the selected versions, because `Π'_{I,o',X'} = Π_{I,o,X}` when `(o',X') = (o,X)` and the spaces are identified. So the ledger statement is rescuable by that reading — but only by the reading that makes Finding 1 sharper, since it means the fine-level invariance is a standing hypothesis on every arrow.)

**Evidence:** The package's own review knows the difference — `view-gauge-holonomy.md:124` says "A nonidentity action can lie in the stabilizer of a particular law. The finite bit flip `g(u)=1-u` stabilizes `Bernoulli(1/2)`" — which is exactly the observation that `Stab(law) ⊋ {id}` and `Stab(law) ⊆ Iso(object)` are different sets. Yet the derivation and the ledger both use one word for both.

**Falsifier:** A reading of `claim-ledger.json` `HOLONOMY-BLIND-FULL-LAW` under which "the fixed-(o,X) stabilizer" already entails preservation of the selected posterior and recognition versions without appeal to (7.2)-(7.3) holding for all arrows.

**Fix:** In the ledger, replace "the fixed-(o,X) stabilizer" with "arrows in the isotropy group of `(o,X)` that additionally stabilize the selected posterior and recognition versions"; or state explicitly that (7.2)-(7.3) are standing hypotheses on every arrow of the groupoid, in which case say so in `ASM-HOLONOMY-BLIND-DATA`.

---

### [Medium] Commit 3f5f49b, advertised as correcting the scale-bundle typing, introduced an unregistered third spelling `\mathscr P` for the root bundle inside Theory/05c

**Location:** `Theory/05c_pullback_geometry.tex:911, 919, 926`; commit `3f5f49b` "docs: correct scale-bundle notation"; `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation-standard.md:44`.

**Claim as stated:** notation-standard.md:44 — "One canonical token has one semantic type in a theorem. A type change requires another symbol. … **The principal object is always $\mathscr P_G$**; full laws use $\mathbb P$, $\mathbb Q$, and $\boldsymbol\Pi$." Registry row: "Principal bundle | $\mathscr P_G\to\mathcal C$ | Common principal $G$-bundle; **bare $P$ is forbidden for this global object**."

**Defect:** The commit changed 05c from `\Omega^1(\mathscr P_G,\bar{\mathfrak g})` to `\Omega^1(\mathscr P,\bar{\mathfrak g})` and from `f^*\operatorname{Ad}\bar P` to `f^*\operatorname{Ad}\bar{\mathscr P}`. The *target*-side change (`\bar P → \bar{\mathscr P}`) removes a bare-`P` violation and is an improvement. The *source*-side change is a regression: in that paragraph the source bundle is a principal `G`-bundle over `\mathcal C` — i.e. it is exactly the registry's `\mathscr P_G\to\mathcal C` — and it is now spelled with an unregistered symbol.

The result is a within-chapter collision of precisely the kind the notation program exists to prevent: `Theory/05c_pullback_geometry.tex` writes the principal bundle over `\mathcal C` as `\mathscr P_G` at lines 63, 82, 159, 162, 166, 221 and as bare `\mathscr P` at lines 911 and 919. Neither `\mathscr P` nor `\bar{\mathscr P}` appears in `notation-registry.json`'s `expected_symbols` or `symbols` list.

**Evidence:**
```
$ git show 3f5f49b -- Theory/05c_pullback_geometry.tex
-$\mathcal P$ over $f$ with Lie-group homomorphism $\kappa$ and law-fiber map
+$\mathcal P:\mathscr P\to\bar{\mathscr P}$ over
+$f:\mathcal C\to\bar{\mathcal C}$ with Lie-group homomorphism
+$\kappa:G\to\bar G$ and law-fiber map $q$, in the sense of
-\in\Omega^1(\mathscr P_G,\bar{\mathfrak g}).
+\in\Omega^1(\mathscr P,\bar{\mathfrak g}).
-$\Omega^1(\mathcal C;f^*\operatorname{Ad}\bar P)$, and
+$\Omega^1(\mathcal C;f^*\operatorname{Ad}\bar{\mathscr P})$, and
```
Current tree, unsubscripted `\mathscr P` in Theory/*.tex:
```
Theory/05c_pullback_geometry.tex:911:$\mathcal P:\mathscr P\to\bar{\mathscr P}$ over
Theory/05c_pullback_geometry.tex:919:\in\Omega^1(\mathscr P,\bar{\mathfrak g}).
Theory/05c_pullback_geometry.tex:926:$\Omega^1(\mathcal C;f^*\operatorname{Ad}\bar{\mathscr P})$, and
```
and `\mathscr P_G` for the same object in the same file at 63, 82, 159, 162, 166, 221.

**Falsifier:** Evidence that in 05c §"scale-connection defect", `\mathcal C` denotes a generic source base rather than the registry's fixed contextual base, so that the source bundle is genuinely not `\mathscr P_G`. (I checked: 05c line 63 defines `\mathcal E_x=\mathscr P_G\times_{\widehat\rho_x}\mathcal B_x` over the same `\mathcal C`, and line 221 sets `\mathcal C=\R` with `\mathscr P_G` trivial — so `\mathcal C` is the same base throughout the chapter.)

**Fix:** Restore `\mathscr P_G` on the source side and register a canonical symbol for the coarse target bundle, e.g. `\bar{\mathscr P}_{\bar G}\to\bar{\mathcal C}`, adding it to `notation-registry.json`.

---

### [Medium] The notation scanner's "fail-closed" guarantee is a hand-written hazard whitelist; the scale-bundle rule it added is line-local and evadable, and the new `\mathscr P` spelling is invisible to it

**Location:** `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation_scan.py:369-396` (`_hazards`), `:428-448` (per-line call site); `notation-standard.md:52-54`.

**Claim as stated:** notation-standard.md:54 — "`notation_scan.py` … **fails closed** on an invalid registry, any unclassified active collision, occupancy written as $\varpi_i$, a new bare global $P_A$ or $Q_A$, a law-valued sample $m_i$, or a use of $C_A$ as both kernel and matrix/operator."

**Defect:** "Any unclassified active collision" overstates what the scanner can see. `_hazards(text)` is a fixed list of literal tokens and regexes applied **one line at a time**. A collision that is not on the enumerated list, or that straddles a line break, is simply not a hazard as far as the scanner is concerned. The scale-bundle rule added by 3f5f49b —
```python
if "\\mathscr P_G" in text and "\\mathcal C_\\ell" in text:
    tokens.append("\\mathscr P_G (scale redefinition)")
```
— fires only when both tokens appear on the *same source line*. In LaTeX, where line breaks are cosmetic, this is trivially evaded by reflowing.

**Evidence (executed):**
```
$ python -c "<load notation_scan.py>; print(ns._hazards(...))"
one_line_offender    -> ['\\mathscr P_G (scale redefinition)']
split_line_1         -> []      # r'a trivial principal bundle \mathscr P_G='
split_line_2         -> []      # r'\mathcal C_\ell\times G with G=(\R^K,+).'
bare_mathscr_P_root  -> []      # the actual current 05c:911 text
omega1_mathscrP      -> []      # the actual current 05c:919 text
AdbarmathscrP        -> []      # the actual current 05c:926 text
```
And the full scan on the current tree passes:
```
$ python docs/.../notation_scan.py --registry docs/.../notation-registry.json --root .
notation collision scan: PASS (13 documented legacy; 103 immutable)
EXIT=0
```
So the scanner reports PASS on a tree that contains the unregistered `\mathscr P` root-bundle spelling documented in the previous finding. The bare-`P` regex explicitly exempts it via the negative lookbehind `(?<!\\mathscr )`.

**Falsifier:** A code path in `notation_scan.py` that validates *every* `\mathscr`-prefixed principal-bundle token against the registry, rather than only the enumerated hazards.

**Fix:** Add an allowlist check: any occurrence matching `\\mathscr\s*P[^_]` or `\\mathscr P_\{?[^G\ell]` in an active source is an `unclassified_collision` unless registered. And make the scale-redefinition rule operate on a paragraph/joined window rather than a single line.

---

### [Medium] `HOLONOMY-RETENTION` is an analytic restatement of the definition of pushforward, and its recorded falsifier cannot be satisfied

**Location:** `claim-ledger.json` claim `HOLONOMY-RETENTION`; `direct-derivation.md:461`; `Theory/07b_agent_network_rg.tex` "Full-law holonomy alternatives" paragraph.

**Claim as stated:** ledger — "When H_A and C_A explicitly retain roots, raw root-framed holonomy, and boundary marks, full parent pushforwards retain their joint laws and correlations, with no quotient, averaged-link, or holonomy-blind claim." Falsifier — "A retained record measurable in H_A whose joint parent distribution is not its pushforward through C_A."

**Defect:** `P_A`, `Π_{A,o,X}`, and `Q_{A,o,X}` are *defined* in (3.1) and (3.4) as pushforwards through `C_A`. So "the joint parent distribution of an `H_A`-measurable record is its pushforward through `C_A`" is true by definition, and the recorded falsifier ("a record whose joint parent distribution is *not* its pushforward through `C_A`") describes a logically impossible object. A claim whose falsifier cannot be instantiated is not a theorem; it is a definition. Its actual content is the *typing declaration* `ASM-HOLONOMY-RETENTION-DATA` — that `H_A` is declared large enough to hold the records — which is an input, not a result.

`direct-derivation.md:461` states this plainly and correctly ("Then (3.1) and (3.4) retain their joint distributions and every correlation with the other parent coordinates **by definition of full-law pushforward**") — the derivation is honest; the ledger then records the same sentence as an `EVIDENCE_VERIFIED` mathematical claim and lists it among the target's static ancestors, and `Theory/07b` stamps it `\status{ESTABLISHED}`.

**Evidence:** `direct-derivation.md:99-101` defines `P_A(do,dz|X) = ∫ C_A(Y,dz) P_I(do,dY|X)`; `:124-127` defines `Π_{A,o,X} = Π_{I,o,X}C_A`, `Q_{A,o,X} = Q_{I,o,X}C_A`. There is no independent characterization of the parent laws against which the retention statement could be tested.

**Falsifier:** An independent definition of `P_A` (not as the `C_A`-pushforward) in the package, against which the retention identity would be a substantive claim.

**Fix:** Reclassify `HOLONOMY-RETENTION` in the ledger as a definition/typing declaration rather than a `MATHEMATICAL` claim with state `EVIDENCE_VERIFIED`, and change `\status{ESTABLISHED}` to `\status{DEFINITION}` in `Theory/07b`.

---

### [Medium] `Theory/07b` places the "holonomy-blind" hypothesis immediately after the root-gauge discussion and reuses the symbol `g`, inviting the false reading that the parent is blind to the root gauge group

**Location:** `Theory/07b_agent_network_rg.tex:1787-1810` (paragraph "Full-law holonomy alternatives", eq. `eq:rg-pointwise-parent-holonomy-channel`); preceding paragraph ending `:1785`; following paragraph `R_x:G\to\operatorname{GL}(V_x)` at `:1812`.

**Claim as stated:**
```latex
require
\begin{equation}
C_A(g\mathbin{\cdot}Y,g\mathbin{\cdot}D)=C_A(Y,D),
\label{eq:rg-pointwise-parent-holonomy-channel}
\end{equation}
for every admitted arrow and measurable parent event
```

**Defect:** Three problems compound.
1. `g` in this equation is an *arrow of the abstract `(o,X)` groupoid* from `thm:rg-pointwise-parent-datum`'s setting. In the immediately preceding paragraph and the immediately following one, `g` and `G` denote the root structure group of `\mathscr P_G` ("root-gauge-equivariant isomorphism of presentations"; `R_x:G\to\operatorname{GL}(V_x)`). Nothing in `07b` ties the two. A reader arriving from the root-framed-holonomy paragraph above will read `g` as a gauge transformation and the equation as "the channel is gauge-invariant". It is not that statement, and no theorem in the package supplies that statement.
2. `g·Y` and `g·D` is *group-action* notation for what the text calls "typed groupoid actions". A groupoid arrow `(o,X)→(o',X')` in general moves between different spaces; writing one `C_A` on both sides silently specializes to a group acting on fixed `Y_I` and `Z_A`.
3. In `07b`'s single-space rendering there are no primes, so "require the fine generative and recognition laws to be **covariant**" literally reads as *invariant*: `g·P_I = P_I`, `g·Q_{I,o,X} = Q_{I,o,X}`. The stated conclusion is then that the parent laws are invariant. This is the manuscript-level form of Finding 1, and here it is unmistakable: assume the fine laws invariant and the channel equivariant, conclude the parent laws invariant.

**Evidence:** `Theory/07b_agent_network_rg.tex:1784-1810` as quoted. The notation registry contains no entry for a groupoid-arrow symbol, and `notation_scan.py` has no hazard rule for `g`. The 8/15 notation program audited `P`, `P_A`, `Q_A`, `m_i`, `C_A`, `\varpi_i`, `Q_q`, `Q_m`, `C_t` and missed the one collision the new text actually introduced.

**Falsifier:** A declaration anywhere in `07b` or the derivation package that the groupoid arrows `g` act through `\widehat\rho_b,\widehat\rho_m` from a common element of the root structure group `G`.

**Fix:** Rename the groupoid arrow throughout the paragraph, and add one sentence: "the arrows here are abstract measurable symmetries and are not assumed to be root gauge transformations; no relation to `\mathscr P_G`, its connections, or their holonomy is asserted."

---

### [Medium] The one hypothesis carrying the evaluator seam under the action, (7.6), is qualified by an undefined "compatibility domain"

**Location:** `direct-derivation.md:448-457`.

**Claim as stated:** `:457` — "holds on the compatibility domain. Equations (4.4) and (7.6) then make the transformed generative conditional compatible with the transformed evaluator."

**Defect:** "The compatibility domain" is never defined in the package. Grep over `docs/derivations/2026-08-15-full-pointwise-meta-agent/` and `Theory/` returns exactly three occurrences: `direct-derivation.md:457`, and `reviews/view-gauge-holonomy.md:56` and `:116` (the latter adding a further undefined qualifier, "the *transported* compatibility domain"). Everywhere else in the package the null-set convention is stated precisely — (4.4) is qualified "for `μ_A^{MΞ}(·|X)`-almost every `(m_A,ξ_A)`", (4.5) "`μ_A^{MΞ}`-almost surely", (6.8) "`Q_{A,o,X}`-almost surely". (7.6), the *only* hypothesis that makes the evaluator survive the action, is the one left with an undefined qualifier. As written it is not a well-posed hypothesis: one cannot check it without knowing which measure's null sets are exempt (source `μ_A^{MΞ}(·|X)`, target `μ_A'^{MΞ}(·|X')`, or their common support).

Additionally, the sentence "Equations (4.4) and (7.6) then make the transformed generative conditional compatible with the transformed evaluator" asserts a disintegration-transport step that is never proved: that if `Φ` is a bimeasurable bijection with `Φ_# P_A = P_A'` respecting the `(M_A,Ξ_A)`/`(B_A,O,H_A)` split, then the pushforward of a selected source conditional is a version of the target conditional. This is true and standard, but it is asserted in half a sentence in a document that elsewhere proves every disintegration step explicitly (compare §3's monotone-class argument for (3.5)).

**Falsifier:** A definition of "compatibility domain" elsewhere in the package that I missed.

**Fix:** Replace "on the compatibility domain" with "for `μ_A^{MΞ}(·|X)`-almost every `(m_A,ξ_A)`", and add the one-line disintegration-transport lemma.

---

### [Medium] The 8/15 rename left the root bundle spelled bare `P` in `overview.md`, on lines the same diff rewrote

**Location:** `overview.md:591, 728, 798` (`overview.md` is an `active_roots` entry in `notation-registry.json`).

**Claim as stated:** `notation-standard.md` registry row — "Principal bundle | `$\mathscr P_G\to\mathcal C$` | Common principal `$G$`-bundle; **bare `$P$` is forbidden for this global object**." The 8/15 diff renamed `overview.md:33` and `:35` accordingly.

**Defect:** Three bare-`P` occurrences denoting the root principal bundle survive in the same file, two of them on lines the 8/15 diff *added*:
```
overview.md:591:  ... for a \(G\)-torsor fiber, \(\mathrm{Aut}_G(P)\) acts simply transitively on sections ...
overview.md:728:  Which of \(\mathcal C,P,G,\omega\), incidence, and interaction kernels must be reconstructed
overview.md:798:  theorems. \(P\), \(G\), \(\omega\), the interaction incidence, and the record kernels are
```
`git diff 060f80e^..8ce6358 -- overview.md` shows `:728` and `:798` inside `+` hunks — the rewrite of §9 and of the "Say this, and not more" block re-introduced the forbidden spelling in the same commit range that outlawed it. `\mathrm{Aut}_G(P)` at `:591` is the gauge group of the principal bundle, exactly the object the standard reserves for `\mathscr P_G`.

The scanner catches none of them. Its bare-`P` regex requires either the literal `\operatorname{Aut}_G(P)` (the file uses `\mathrm{Aut}_G(P)`) or the words "principal bundle"/"principal connection" within 50 characters; `\(\mathcal C,P,G,\omega\)` has neither.

**Evidence:** grep output above, reproduced against the working tree at HEAD, plus `python .../notation_scan.py --root .` → `notation collision scan: PASS`.

**Falsifier:** A registry rule classifying `overview.md` §8-§10 as immutable or outside the active line range. (Checked: `overview.md` is listed in `active_roots` and the scanner reported it among active files.)

**Fix:** Replace `P` with `\mathscr P_G` at `overview.md:591, 728, 798`, and add `\\mathrm\{Aut\}_G\(P\)` and the bare list-context `,P,` to the hazard regex.

---

### [Low] The sixteen adversarial attacks do not probe either of the two central holonomy defects

**Location:** `evidence/adversarial-attacks.md` A9-A11, A16; `adversarial-report.json`.

**Claim as stated:** `construction-or-strongest-theorem.md:114` — "independent reconstruction, semantic oracle erasure, and **sixteen adversarial attacks all pass**."

**Defect:** The three holonomy attacks are A9 (marginal invariance → joint invariance), A10 (trivial holonomy → agreement/membership), A11 (records erased despite a retention claim). All three attack the *retention* side and the *marginal/joint* seam. None asks (i) whether §7 contains any holonomy at all — no attack tests the identification of `T^g` with parallel transport around a loop; or (ii) whether the blindness branch's hypothesis set can exhibit blindness — no attack tests whether (7.2)/(7.3) at an isotropy arrow already force fine-level invariance. The attack set is therefore not evidence about the two defects reported as Findings 1 and 2; it is evidence about three narrower hazards.

**Falsifier:** An attack in `adversarial-attacks.md` that raises the naming or vacuity question. (I read A9-A12 and A16 in full and scanned the file; none does.)

**Fix:** Add two attacks — "the blindness branch contains no holonomy" and "the blindness branch's hypotheses imply the fine datum is already invariant, so 'blindness' is vacuous" — and answer them on the merits.

---

## Things that check out

Reported honestly; these are places where I looked for a defect and did not find one.

1. **The covariance computation (7.1)-(7.5) is correct.** I reconstructed the pushforward argument independently, including the product-test-function step for the generative law, using `∫ f(T_A z)C_A(Y,dz) = ∫ f(z')C_A'(T_I Y,dz')` — which is exactly (7.4) in pushforward form. Posterior and recognition identities follow the same way. No error.
2. **The inverse image in (7.4) is on the correct side,** and the types are right: `D ⊆ Z_A'`, `(T_A^g)^{-1}D ⊆ Z_A`.
3. **`Theory/07b` eq. `eq:rg-pointwise-parent-holonomy-channel` is equivalent to (7.4)** in the single-space case: substituting `D' = g·D` in `C_A(g·Y,g·D)=C_A(Y,D)` gives `C_A(g·Y,D') = C_A(Y,g^{-1}·D')`. Consistent; not a discrepancy.
4. **The channel-equivariance hypothesis has nontrivial models** — explicit `Z/2` parity example with both actions nontrivial, built and verified (Finding 1). The blindness branch is not vacuous in the "no models" sense.
5. **The version hypothesis (7.2) is genuinely load-bearing and correctly flagged.** Generative covariance determines the posterior covariance only `ν_X`-a.e.; declaring covariant values on the exceptional slice is a real extra hypothesis, and `direct-derivation.md:424` says so. Most write-ups of this kind get that wrong; this one does not.
6. **The Čech statement in `Theory/02_geometry.tex:510-520` is correct.** The proof gives `u_j^m = u_i^b T_{ij}^b h_j` and `u_j^m = u_i^b h_i T_{ij}^m`, hence `T_{ij}^m = h_i^{-1}T_{ij}^b h_j` — exactly the nonabelian coboundary relation `g'_{ij} = λ_i^{-1}g_{ij}λ_j`, so `[T^b] = [T^m]` in `\check H^1(\{\mathcal C_i\};\mathcal G)` (Kobayashi–Nomizu, *Foundations of Differential Geometry* I, §I.5: construction of a bundle from transition functions, and the equivalence criterion for cohomologous cocycles). The 8/15 diff to this passage is a pure rename and introduces no error.
7. **The two bundles are genuinely different objects — this is not a rename dressed as a correction.** `Theory/07_general_renormalization.tex:154-180` declares, at each level `ℓ`, a base `\mathcal C_\ell`, a Lie group `G_\ell`, a principal `G_\ell`-bundle `\varpi_\ell:\mathscr P_\ell\to\mathcal C_\ell`, connections `\omega_{\ell,b},\omega_{\ell,m}\in\Omega^1(\mathscr P_\ell,\mathfrak g_\ell)`, and scale maps `\mathcal P_\ell:\mathscr P_\ell\to\mathscr P_{\ell+1}` covering `c_\ell` with `\mathcal P_\ell(p·g)=\mathcal P_\ell(p)·\kappa_\ell(g)`. Different base, different structure group, different Lie algebra, own connections. `\mathscr P_G\to\mathcal C` with group `G` and `\omega_b,\omega_m\in\Omega^1(\mathscr P_G,\mathfrak g)` (`Theory/02:282-290`) is a different object.
   **But the separation is pre-existing, not 8/15 work.** `Theory/07_general_renormalization.tex` is untouched by the 8/15 diff (`git diff --name-only 060f80e^..8ce6358 -- Theory/07_general_renormalization.tex` → empty; the file's only commit is `bd46058`). What 8/15 did is (i) rename the root bundle `P → \mathscr P_G` across `Theory/01,02,04,05c,06a,appendix_notation` and `overview.md`, and (ii) repair one genuine collision at `Theory/05d:238`, where `\mathscr P_G` had been written for a bundle over `\mathcal C_\ell`. Item (ii) is a real typing fix. Commit `3f5f49b`'s own message, "correct scale-bundle notation", is accurate; calling the 8/15 work a "bundle split" would overstate it.
8. **`Theory/07:251-265`'s obstruction statement is correct and unusually careful.** An equivariant `\mathcal P_\ell` over `c_\ell` exists iff `\mathscr P_\ell\times_{\kappa_\ell}G_{\ell+1}\cong c_\ell^*\mathscr P_{\ell+1}` as principal `G_{\ell+1}`-bundles over `\mathcal C_\ell`; the Hopf-bundle counterexample is right. This is the standard extension-of-structure-group criterion (`\kappa_*` on `\check H^1(\mathcal C_\ell;G_\ell)\to\check H^1(\mathcal C_\ell;G_{\ell+1})`).
9. **The 08-14 package's graph holonomy is genuine and correctly stated.** `2026-08-14-pointwise-meta-agent-rg/evidence/direct-derivation.md:6-60` builds a gain graph (edge transports `T_{ij}^x` with `T_{ji}=(T_{ij})^{-1}`), path transports, based cycle holonomies, a reciprocal path groupoid, and `\ker L_x\cong\operatorname{Fix}(\operatorname{Hol}_r^x)` for positive-definite edge weights. I re-derived the kernel identity: `z ∈ ker L` iff `z_i = T_{ij}z_j` on every support edge; fixing a root and using a spanning tree determines `z` from `z_r`, and consistency around fundamental cycles is exactly `z_r ∈ Fix(Hol_r)`. This is the connection-Laplacian result of Singer–Wu (vector diffusion maps) and Bandeira–Singer–Spielman (Cheeger inequality for the graph connection Laplacian). The semidefinite-weight caveat ("edgewise visibility `W_e^{1/2}(z_i-T_{ij}z_j)=0`") is correct. So is the nonabelian caveat: spanning the graph cycle space controls only the abelianization, and triangles suffice only when their based boundary words *normally* generate `\pi_1` — a chordless `C_4` is the standard counterexample. This is the one place in the corpus where "holonomy" is used correctly.
10. **The finite holonomy witnesses in `counterexample-proofs.md` §5 are arithmetically correct.** `KL(Ber(1/4)‖Ber(3/4)) = (1/4)log(1/3)+(3/4)log 3 = (1/2)log 3 > 0`, symmetric under swap; the bit flip stabilizes `Ber(1/2)`; `T(b,m)=(1-b,m)` sends the correlated law on `{(0,0),(1,1)}` to the anticorrelated law on `{(0,1),(1,0)}` with both marginals fair. All three do what they are claimed to do, and they establish `NEG-TRIVIAL-HOLONOMY-AGREEMENT` and `NEG-MARGINAL-HOLONOMY-JOINT` as stated.
11. **`direct-derivation.md:498`'s exclusion list is honest** about what is not supplied ("no statistical manifold, DQM structure, Fisher metric, ... full geometric section over `\mathcal U_A`, ... cross-`X` factorization"). The scope fencing throughout §§1-6 is careful; my findings concern §7 and the notation program, not the probabilistic core.

---

## Answers to the four assigned questions

**Q1. Holonomy blindness.**
(a) *Theorem or definitional consequence?* Formally a theorem; substantively a one-line corollary whose conclusion is its hypothesis pushed through an assumed-equivariant map. Of the six hypotheses, exactly **one** does transfer work — channel equivariance (7.4). Two — full fine-law covariance (7.2) and recognition covariance (7.3) — *are the conclusion at the fine level* once specialized to the same slice. One — generative covariance (7.1) — is needed only for the `P_A` half and is nearly redundant given (7.2) plus observation covariance. One — evaluator covariance (7.6) — concerns a different object and does not enter the three law identities. One — fixed-`(o,X)` isotropy — is the specialization that turns covariance into invariance and, combined with (7.2)/(7.3), silently becomes a stabilization hypothesis on the data. See Findings 1 (High) and 4 (Medium).
(b) *Is the isotropy hypothesis about the action or the data?* As written at `direct-derivation.md:459` it is about the action *plus* a restrictive clause ("preserve the selected versions") that is about the data; the ledger's restatement keeps only the action half. Under the reading that (7.2)-(7.3) are standing hypotheses on every arrow, isotropy-of-the-action already implies stabilization-of-the-data — which is precisely why the blindness conclusion is vacuous in the interesting sense. See Finding 4.
(c) *Does channel equivariance have a nontrivial model?* **Yes.** `Y_I={0,1}^2`, `Z_A={0,1}`, `C_A(y,·)=δ_{y_1⊕y_2}`, `T_I(y_1,y_2)=(1⊕y_1,y_2)`, `T_A(z)=1⊕z`; both actions nontrivial, (7.4) verified by direct substitution.

**Q2. Connection and parallel transport?**
**No, not in the 8/15 pointwise construction.** §7 has no connection form, no horizontal distribution, no parallel transport, no curvature, and no loop. The "loop" the same-slice statement is around is an arrow from the abstract groupoid object `(o,X)` to itself — an isotropy-group element of a groupoid whose objects are (admitted observation, structural datum) pairs, not points of a base. The construction is explicitly at one `r_*` and explicitly does not glue over `\mathcal U_A`, so there is nothing for a holonomy to be taken around. A genuine discrete connection with genuine holonomy *does* exist in the released 2026-08-14 package and in `Theory/07b`'s root-framed records; §7 never connects `T_I^g,T_A^g` to any of it. See Findings 2 (High) and 6 (Medium).

**Q3. The bundle split.**
The two bundles **are** genuinely different objects (different base, structure group, Lie algebra, connections, and scale maps with a correctly stated topological obstruction). But that separation predates the 8/15 work and lives in `Theory/07_general_renormalization.tex`, which the 8/15 diff does not touch. The 8/15 contribution is a global rename `P → \mathscr P_G` plus one genuine collision repair at `Theory/05d:238`. Surviving conflations found: `Theory/05c:911,919` spells the root bundle bare `\mathscr P` (unregistered, introduced *by* the repair commit) while the same file spells the same object `\mathscr P_G` at six other lines; `overview.md:591,728,798` still spells it bare `P`, two of those on lines the 8/15 diff added. `Theory/02`, `Theory/appendix_notation.tex`, and `Theory/07b` are internally consistent on the bundle symbols. See Findings 5, 6, and 9.

**Q4. Cocycle / equivariance conditions asserted vs. verified.**
Mostly honest, with two exceptions.
- (7.4), (7.6), and `07b`'s `eq:rg-pointwise-parent-holonomy-channel` are stated as *hypotheses* on supplied data, not asserted of constructed objects. Correct practice.
- The Čech cocycle law and the class equality `[T^b]=[T^m]` in `Theory/02:495-520` are actually **proved**, and the proofs are correct.
- **Exception 1:** the disintegration-transport step at `direct-derivation.md:457` is asserted in half a sentence, never proved, and its null-set qualifier is an undefined "compatibility domain". True but unverified. See Finding 8.
- **Exception 2:** no hypothesis anywhere ties the decomposed action `T_B^g×T_M^g×T_Ξ^g×T_H^g` to the ambient theory's *single* gauge group. `Theory/02:167-176` is emphatic that the ambient gauge group is the single group of `G`-equivariant automorphisms of `\mathscr P_G`, whose two local descriptions satisfy `k_i^m = h_i^{-1}k_i^b h_i` and are therefore "related, not independent". §7's decomposed action imposes no such relation between `T_B^g` and `T_M^g`. The abstract statement is not *wrong* — it is more general than, and unconnected to, the ambient gauge structure. That disconnection is exactly what makes the word "holonomy" unearned. The package's own `view-gauge-holonomy.md` falsification condition #1 names this hazard and then discharges it by inspection rather than by exhibiting the missing bridge hypothesis.

---

## Assessment of the internal domain review

`evidence/reviews/view-gauge-holonomy.md` returns **C/H/M: none, APPROVE**. Its mathematics is, as far as it goes, correct: §2's event-level pushforward calculation, §5's projection functoriality, and §8's recomputation of the three finite witnesses all check out and I reproduced them. What it does not do is ask whether the object it is verifying is the object the surrounding prose names. It verifies covariance and calls it "holonomy blindness" 23 times without once asking where the connection, the loop, or the curvature is; and its §4 ("Covariance is not same-slice invariance") stops one step short of the observation that same-slice invariance is, under (7.2)-(7.3), the assumed fine invariance restated. Its own falsification condition #1 is precisely on target and is discharged by assertion. Consistent with the review mandate, I treated its APPROVE as a claim to be tested, not as evidence; the two High findings above survive it.

---

## Coverage

**Read in full:**
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md` (498 lines)
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/reviews/view-gauge-holonomy.md` (200 lines)
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/construction-or-strongest-theorem.md` (118 lines)
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation-standard.md` (54 lines)
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation-registry.json` (all symbol rows relevant to bundles)
- `git show 3f5f49b` (complete diff)
- `git diff 060f80e^..8ce6358 -- Theory/02_geometry.tex` (complete)
- `git diff 060f80e^..8ce6358 -- Theory/appendix_notation.tex` (complete)
- `git diff 060f80e^..8ce6358 -- Theory/07b_agent_network_rg.tex` (complete)
- `git diff 060f80e^..8ce6358 -- overview.md` (complete)

**Read in part (sections named):**
- `claim-ledger.json` — all `HOLO*` assumptions and claims plus the `target` claim, extracted programmatically
- `evidence/counterexample-proofs.md` §5 (holonomy boundary witnesses) and §6
- `evidence/adversarial-attacks.md` A9-A12, A16
- `evidence/notation_scan.py` — `_hazards`, `classify_occurrence` tail, `scan_active_sources` call site, `_self_test` fixtures; executed the scanner and probed `_hazards` directly
- `docs/derivations/2026-08-14-pointwise-meta-agent-rg/evidence/direct-derivation.md` §§1-2 and §7
- `Theory/02_geometry.tex` lines 160-180, 470-560, 720-780
- `Theory/05c_pullback_geometry.tex` lines 860-960, plus grep of all `\mathscr P` occurrences
- `Theory/07_general_renormalization.tex` lines 140-270
- `Theory/appendix_notation.tex` lines 340-380
- `git diff -- Theory/05d_relational_inference.tex` first ~140 lines (skimmed; content is monoid/operational-quotient theory, outside this panel's scope)

**Not reached:**
- `Theory/06_general_coarsegraining.tex` and `Theory/09_coarsegraining.tex` — cited by the internal review at `:491-499`, `:643-647`, `:808-832`, `:427-435`, `:1051-1065` in support of its argument. I did not verify those citations. If another panelist has capacity, the Gaussian-holonomy claim at `09:808-832` ("nontrivial represented holonomy can preserve an isotropic Gaussian even when the structural fixed sector is proper") is the one worth spot-checking.
- `Theory/03_probability.tex`, `Theory/06a_generative_gaussian.tex`, `Theory/SPEC.md`, `Theory/appendix_claim_ledger.tex` diffs.
- `evidence/independent-reconstruction.md`, `evidence/oracle-erasure.md`, `release-assembly.json`, `release-provenance.json` — deliberately not consulted as evidence, per mandate; not audited as artifacts either.
- The remaining ~180 lines of the `Theory/05d_relational_inference.tex` addition (soft-intervention monoid, BSC nonidentifiability, circle heat pair) — outside gauge/holonomy scope.
- No TeX compile was attempted; findings on `.tex` files are source-level.

STATUS: COMPLETE
