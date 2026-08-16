# P10 — Rigor sweep of prose added 2026-08-15

STATUS: COMPLETE

Agent: P10 rigor-sweep investigator
Target revision: 8ce635807a6ca2a388255fc996c98f7c535e5843
Diff base: 060f80e5556e41e0f31aeafcd9ef8564c1544c16^

**Headline.** The mathematics added on 8/15 is, so far as I could check it, **correct**: I
reconstructed the soft-BSC total-variation diameters, the circle heat-kernel Blackwell separation,
the compact-quotient theorem, the syntactic-monoid universal property, and every step of the
full-pointwise-datum KL chain, and found no error. The defects are of a different kind — the
manuscript's headline theorem has no proof in the manuscript, its principal term $p_X(o)$ is never
declared there, six new ESTABLISHED results carry zero citations while three of them restate
classical theorems, one corollary is applied outside the domain its own definition declares, and the
release's two self-certifications (the notation scan and the status ledger) are narrower than the
prose that reports them. Severity totals: **Critical 0, High 2, Medium 6, Low 3**. Three further
`[Low]`-tagged blocks are not defects: two report verified-correct mathematics, and one is a
self-correction of my own earlier finding.

## Files to examine (checklist)

- [x] overview.md (8/15 diff) — read in full (diff hunks)
- [x] solid_RG_theory.md (8/15 diff) — read in full (diff hunks)
- [x] Theory/05d_relational_inference.tex (8/15 diff) — read in full (diff hunks)
- [x] Theory/07b_agent_network_rg.tex (8/15 diff) — read in full (diff hunks)
- [x] Theory/02_geometry.tex (8/15 diff) — read in full (rename-only)
- [x] Theory/03_probability.tex (8/15 diff) — read in full (diff hunks)
- [x] Theory/06_general_coarsegraining.tex (8/15 diff) — read in full (diff hunks)
- [x] Theory/SPEC.md (8/15 diff) — read in full (diff hunks)
- [x] docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md — read in full (499 lines)
- [x] docs/derivations/2026-08-14-operational-intervention-extensions/evidence/direct-derivation.md — read in full (553 lines)

---

## Method note: the standard hedge lexicon is nearly blind to this corpus

`hedge_scan.py` over the added lines returns 72 candidates, of which essentially **zero** are
defects: the "epistemic" hits are all technical `may` ("a finite VFE **may** be negative" — true and
proved), and the "vagueness" hits are all the technical term "almost surely". The corpus has been
written to evade the standard lexicon.

Its actual hedging vocabulary is a different, domain-specific set. Counts over ADDED LINES ONLY:

| token | overview.md + solid_RG_theory.md | Theory/*.tex | Theory/SPEC.md |
|---|---|---|---|
| declared / declare / Declare | 15 | 16 | 4 |
| selected | 9 | 7 | 5 |
| typed | 8 | 7 | 3 |
| admitted / admits | 8 | 7 | 2 |
| supplies / supply / Supply | 4 | 11 | 3 |
| "where retained" | 2 | 2 | 0 |
| "standard" (uncited) | 2 | 3 | 0 |

The first finding below is that the corpus's central rhetorical device — "declared" — is *usually*
honest and only twice load-bearing-but-empty. I resolved each occurrence class rather than flagging
the word.

**Hard citation count in the added mathematics: ZERO.** Command:

```
$ grep -c "cite" <added lines of 05d/07b/06/03/02>
0
```

Roughly 700 lines of new theorem-and-proof prose containing the syntactic-monoid universal property,
the relative-entropy chain rule, standard-Borel disintegration, the Ionescu-Tulcea/kernel-composition
measurability argument, Blackwell domination, and Effros-style smoothness of Borel equivalence
relations — with not one citation. The findings below pay those debts individually, supplying
Myhill/Nerode/Eilenberg for the syntactic monoid, Blackwell 1953 for domination, Dupuis-Ellis
Thm C.3.1 and Csiszar 1967 for the chain rule and DPI, and Becker-Kechris for "smooth".

---

## Findings

### [Medium] "Declared" is load-bearing in exactly two places where it names no hypothesis; elsewhere it is honest

**Location:** `Theory/07b_agent_network_rg.tex:76-190` (thm:rg-pointwise-parent-datum);
`Theory/05d_relational_inference.tex:1341-1380`, `1467-1513`; `solid_RG_theory.md` §11 CONDITIONAL block

**Claim as stated:** representative uses —
(a) 07b:95 "At an **admitted** $o$ with a finite positive evidence representative, supply a
normalized correlated recognition law";
(b) 07b:131 "Declare a jointly measurable normalized parent evaluator";
(c) 05d:1341 "Retain the mediator-replacement face, the ordered roles \(R\) as input/parameter and
\(O\) as output/observation, and one global typed response intertwiner for every protocol";
(d) 05d:1499 "under maps that preserve the marked mediator, circle heat geometry, ordered
\(R\)-to-\(O\) roles, compatible protocol map, and one global response intertwiner".

**Defect:** I checked all 35 occurrences of declared/declare/Declare in the added lines. **33 of 35
name a specific object with a specific property** and are legitimate — e.g. "Declare one normalized
measurable Markov-kernel channel $C_A:\mathsf Y_I\rightsquigarrow\mathsf Z_A$. It is fixed
independently of recognition, posterior, recognition parameters, and realized observation" (07b:88-95)
is a complete, checkable hypothesis, and eq. (7.4)/(4.4) of the derivation write the compatibility
conditions out as displayed equations. This is *not* the failure mode the reviewer's brief anticipated,
and I say so explicitly.

The two that fail are (a) and (c)/(d):

- **(a) "admitted $o$" and "$p_X(o)$" have no declaration anywhere in `Theory/`.** `grep -rn
  "p_X(o)\|lambda_X" Theory/*.tex` returns exactly two lines: `07b:171` and
  `appendix_claim_ledger.tex:202`, both *uses*. The object $p_X(o)$ is never defined in the
  manuscript. The derivation package supplies the missing declaration (direct-derivation.md §1
  lines 47-53: "fix a sigma-finite observation reference measure $\lambda_X$ with
  $\nu_X\ll\lambda_X$, choose one measurable density representative $p_X=d\nu_X/d\lambda_X$, and
  admit only the present $o$ with $0<p_X(o)<\infty$"), and explicitly says this is load-bearing:
  "This extra declaration is what makes a pointwise evidence term meaningful when $\mathsf O$ is
  continuous." The manuscript theorem therefore states a VFE identity whose principal term is
  undefined *in the manuscript*.
  This is not cosmetic: `Theory/03_probability.tex:214` establishes that a joint law determines
  *neither* pointwise posterior at an exceptional observation, and rules that "every later
  fixed-observation posterior, ELBO, or free-energy statement is asserted for
  $P^O_{\theta,X}$-almost every $o$ ... An everywhere pointwise statement instead requires a
  particular jointly measurable density, evidence representative, and regular-conditional version
  to be **declared as part of the model data**." `thm:rg-pointwise-parent-datum` makes an everywhere-
  pointwise statement and never invokes that declaration or cross-references
  $\mathsf O^{\mathrm{reg}}_{\theta,X}$.

- **(c)/(d) The comparison category is never defined in `Theory/`**, in either the soft-BSC or
  circle theorem. Both no-go theorems conclude "nonisomorphic in this category" / "does not identify
  this compact-Feller mediator experiment", but no `\definitionheading` in the added text gives
  objects and morphisms. The proof steps that actually consume the category — "an admitted protocol
  map preserves the marked mediator face" (05d:1377) and "under maps that preserve ... circle heat
  geometry" (05d:1499) — are the *only* specification in the manuscript, given in running prose.
  "Preserves circle heat geometry" in particular is undefined there, and it is exactly the
  hypothesis that makes the circle no-go a no-go rather than an open question.
  **Corrected below:** the category *is* fully defined in the 08-14 evidence package, section 1
  (the $(f_R,f_E,f_O,\Theta,U)$ quintuple). See the correction/sharpening finding at the end of
  this file. The defect is that the manuscript is not self-contained, not that the hypothesis is
  missing from the corpus.

**Evidence:** the greps above; `Theory/03_probability.tex:214` quoted; direct-derivation.md §1:45-53
quoted; the absence of any `\definitionheading{...}{def:hist-...category...}` in the 05d diff.

**Falsifier:** a declaration of $\lambda_X$ / $p_X$ / $\mathsf O^{\mathrm{adm}}$ elsewhere in
`Theory/` that my grep missed; or a `\definitionheading` for the marked-soft / circle comparison
category anywhere in the repository's `Theory/`.

**Fix:**
1. In 07b, before the theorem, add: "Fix a sigma-finite $\lambda_X$ on $\mathsf O$ with
   $\nu_X=\mathbb P_I^O(\cdot\mid X)\ll\lambda_X$, fix one measurable representative
   $p_X=d\nu_X/d\lambda_X$, and call $o$ *admitted* when $0<p_X(o)<\infty$ and the selected
   posterior versions of \Cref{...03...} are used at $o$. By
   \Cref{prop:prob-exceptional-observation} the statement below is pointwise in this declaration,
   not in the joint law alone."
2. Promote the two comparison categories to `\definitionheading`s with explicit object and morphism
   data, and restate both no-gos as "there is no isomorphism in $\mathsf{Cat}$" with $\mathsf{Cat}$
   the defined category. (This is a restatement, not a weakening: the mathematics below is correct.)

---

### [High] Six new "ESTABLISHED" theorems in 05d carry no citation, and three of them are classical results restated

**Location:** `Theory/05d_relational_inference.tex:1082-1128`
(prop:hist-operational-quotient-universal-property), `1130-1163`
(thm:hist-compact-operational-quotient), `1467-1513`
(thm:hist-circle-heat-intervention-nonidentifiability), plus `Theory/SPEC.md` §"operational-extension
certificate", `overview.md` §"operational-intervention boundary".

**Claim as stated:** 05d:1082-1104 — "Then \(\sim_\Phi\) is the largest two-sided monoid congruence
contained in the kernel relation of \(\Phi\). ... there is one unique surjective unital homomorphism
\(h:B\to\operatorname{Syn}(\Phi)\) ... If \(A\) is finite, it has minimum protocol-class cardinality
... \status{ESTABLISHED}". And SPEC.md: "Thus `Syn(Phi)` is terminal from finer to coarser quotients
and contextually fully abstract relative to the fixed operational data."

**Defect:** The proposition is the **syntactic monoid / syntactic congruence**, verbatim, with the
recognized language $L\subseteq A$ replaced by an arbitrary response $\Phi:A\to Y$ — a change that
alters no line of the proof. The notation $\operatorname{Syn}(\Phi)$ concedes the point. It is
presented as a new ESTABLISHED result of this program with no attribution, in a repository whose
`references.bib` has 466 entries and contains **no** Myhill, Nerode, Schützenberger, Eilenberg, or
Pin (verified by grep). Same for Blackwell domination in the circle theorem (no Blackwell 1953
entry) and for the compact-quotient theorem, whose content is the standard fact that a continuous
bijection from a compact space to a Hausdorff space is a homeomorphism, applied to the
Myhill–Nerode quotient.

I verified the mathematics: **all three proofs are correct** (reconstructions in R-3 and below). The
defect is a novelty/attribution one, and it is High rather than Medium because the surrounding
framing in `overview.md` ("The operational-intervention boundary is now exact in several declared
categories") and `SPEC.md` present these as the program's own boundary-advancing results.

**Evidence:**
- Primary source for the universal property: **J. Myhill, "Finite automata and the representation
  of events", WADD TR-57-624 (1957)**, and **A. Nerode, "Linear automaton transformations",
  Proc. AMS 9 (1958) 541–544**, which prove that the coarsest right/two-sided congruence saturating
  a set is unique and yields the minimal recognizing object. The monoid form with the universal
  factorization $h$ is **M. P. Schützenberger** via **S. Eilenberg, *Automata, Languages and
  Machines*, Vol. B (Academic Press, 1976), Ch. II** and **J.-E. Pin, *Varieties of Formal
  Languages* (Plenum, 1986), Ch. 3, Prop. 3.1**: the syntactic monoid $M(L)=A^*/{\sim_L}$ with
  $u\sim_L v \iff (\forall x,y)(xuy\in L \leftrightarrow xvy \in L)$ divides every monoid
  recognizing $L$, and $L$ is recognized by $M$ iff $M(L)$ divides $M$.
- Primary source for strict Blackwell domination: **D. Blackwell, "Equivalent comparisons of
  experiments", Ann. Math. Statist. 24 (1953) 265–272** — the definition "$B$ is a garbling of $A$"
  used silently at 05d:1485.
- Grep: `grep -niE "myhill|nerode|schutzenberger|eilenberg|blackwell|pin19" references.bib` → no hits.

**Falsifier:** a citation to any of these in `Theory/` that covers the new propositions; or an
argument that the arbitrary-codomain $\Phi$ version is not an immediate transcription of the
language case (I checked: it is — the proof never uses that $Y=\{0,1\}$).

**Fix:** add `\citep{Myhill1957,Nerode1958}` / `\citep[Ch.~II]{Eilenberg1976}` at
prop:hist-operational-quotient-universal-property and restate its status line as
"\status{ESTABLISHED} (this is the syntactic-monoid universal property of
\citet{Eilenberg1976}, transcribed from recognized languages to an arbitrary response codomain; the
transcription is verbatim)". Add `\citep{Blackwell1953}` at the circle theorem. Add the three bib
entries.

---

### [Low] The circle heat no-go, the soft-BSC diameter computation, and the compact-quotient theorem all CHECK OUT

**Location:** `Theory/05d_relational_inference.tex:1130-1163`, `1341-1380`, `1467-1513`

This is a zero-defect result and I state it explicitly rather than manufacture findings.

**Reconstructions I performed:**

1. *Soft-BSC total variation, eq. (eq:hist-soft-bsc-tv).* With $P(O{=}0\mid E{=}0)=1-b$,
   $P(O{=}0\mid E{=}1)=b$ and $K_t(E{=}0\mid R{=}r)=t_r$:
   $Q_b(t)(O{=}0\mid R{=}r)=t_r(1-b)+(1-t_r)b=b+(1-2b)t_r$ ✓ (matches the proof line).
   With $R$ uniform on $\{0,1\}$,
   $\mathrm{TV}=\tfrac12\sum_{r,o}|Q_b(t)(r,o)-Q_b(t')(r,o)|
   =\tfrac12\sum_r \tfrac12\cdot 2|1-2b||t_r-t'_r|
   =\tfrac{|1-2b|}{2}(|t_0-t'_0|+|t_1-t'_1|)$ ✓.
   Diameter over $t\in[\epsilon,1-\epsilon]^2$: $\tfrac{|1-2b|}{2}\cdot 2(1-2\epsilon)=|1-2b|(1-2\epsilon)$.
   For $L_1=L(1/4,1/3)$, $b=1/3$, $|1-2b|=1/3$ → $(1-2\epsilon)/3$ ✓.
   For $L_2=L(1/3,1/4)$, $b=1/4$, $|1-2b|=1/2$ → $(1-2\epsilon)/2$ ✓.
   Interior separation with $t=(s_-,s_-)$, $t'=(s_+,s_+)$: $|1-2b|(s_+-s_-)$ ✓.
   Passive equality cross-check: $a\ast b=a(1-b)+b(1-a)$ gives $1/4\cdot 2/3+1/3\cdot 3/4=5/12$ and
   $1/3\cdot 3/4+1/4\cdot 2/3=5/12$ ✓, consistent with the "$\delta=5/12$" passive crossover used in
   thm:hist-randomized-hard-intervention-nonidentifiability and with the stated retained law
   $(7/24,5/24,5/24,7/24)$ since $\tfrac12(1-5/12)=7/24$ ✓.

2. *Circle heat, eq. (eq:hist-circle-heat-blackwell).* Suppose $H_s=H_tL$ for a Markov kernel $L$.
   Acting on $e_1(\theta)=e^{i\theta}$: $H_se_1=e^{-s}e_1$ and $(H_tL)e_1=H_t(Le_1)=H_tg$ with
   $g=Le_1$. Markov positivity: $|g|\le L|e_1|=1$. Fourier: $\widehat{H_tg}(1)=e^{-t}\widehat g(1)$,
   so $e^{-t}\widehat g(1)=e^{-s}$, i.e. $|\widehat g(1)|=e^{t-s}>1$, contradicting
   $|\widehat g(1)|\le\|g\|_\infty\le1$ ✓. Exactly the printed argument.
   Strictness witness: $\nu_\rho H_s=H_{\rho+s}(x_0,\cdot)$; if this equals $\mu H_t$ then
   $|\widehat\mu(1)|e^{-t}=e^{-(\rho+s)}$, so $|\widehat\mu(1)|=e^{t-s-\rho}>1$ for $\rho<t-s$,
   impossible for a probability measure ✓. (The printed proof writes $\widehat\nu(1)$ for the
   unknown $\widehat\mu(1)$ — a notation collision with $\nu_\rho$, cosmetic only.)
   Inclusion $\{\nu H_t\}\subseteq\{\nu H_s\}$: $\nu H_t=(\nu H_{t-s})H_s$ ✓.
   Joint Feller of $K_\nu(dE\mid R{=}r)=\nu(dE)$: $\int f\,dK_\nu(\cdot\mid r)=\int f\,d\nu$ is
   continuous in $(r,\nu)$ for the weak topology ✓, and $\mathcal P(\mathbb T)$ is compact
   metrizable ✓.

3. *Compact operational quotient.* Kernel of $S_D$ equals $\sim_\Phi$: pick $u_n\to u$, $v_n\to v$
   in $D$ (density + metrizability), joint continuity of multiplication and continuity of $\Phi$
   give $\Phi(uav)=\lim\Phi(u_nav_n)=\lim\Phi(u_nbv_n)=\Phi(ubv)$, uniqueness of limits from $Y$
   Hausdorff ✓. $Y^{D\times D}$ metrizable since $D$ countable ✓. $A/{\sim}$ compact,
   $S_D(A)$ Hausdorff, induced map a continuous bijection ⟹ homeomorphism ✓. $\pi\times\pi$ is
   closed (compact → Hausdorff) hence quotient ⟹ $\bar m$ continuous ✓.

4. *Soft-intervention monoid is a compact metrizable topological monoid* (def, 05d:1319). Joint
   continuity of $\star$ holds because $\{b_v=\bot_v\}$ is **clopen** (isolated adjunction), so
   $(a,b)\mapsto(a\star b)_v$ is continuous on each of two clopen pieces ✓. Finite DAG ⟹ finite
   product ⟹ compact metrizable ✓. The proof does not say this; the isolatedness hypothesis is
   stated in the definition and is exactly what is needed. Checks out.

**Nothing was found wrong in these four.** The defects attached to them are the categorial and
citation ones above, not arithmetic.

---

### [High] The headline theorem of the 8/15 release carries `\status{ESTABLISHED}` and has no proof anywhere in `Theory/`

**Location:** `Theory/07b_agent_network_rg.tex:76-178` (`thm:rg-pointwise-parent-datum`)

**Claim as stated:** the theorem runs 102 lines (07b:76-178) and ends
"...A bare equality $+\infty=+\infty$ supplies neither the zero-defect
criterion nor a recovery consequence. \status{ESTABLISHED}" — immediately followed by `\medskip` and
a NOT-CLAIMED remark, then `\section{The exact effective likelihood and action}`.

**Defect:** **there is no proof.** No `\paragraph{Proof.}`, no `\noindent\emph{Proof.}`, no
`$\square$`, and no cross-reference to any place where it is proved. This is not the file's
convention: `Theory/07b_agent_network_rg.tex` contains 13 `\theoremheading`s and **29** proof
paragraphs; the theorem immediately above it (`thm:rg-exact-coarse-vfe`, 07b:60-66) has a full proof
ending in `$\square$`.

The proof exists — in `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md`
sections 1-6, and partially in `Theory/06_general_coarsegraining.tex:301-331`. But:

```
$ grep -rn "rg-pointwise-parent-datum" Theory/
Theory/06_general_coarsegraining.tex:331:\Cref{thm:rg-pointwise-parent-datum}. \status{ESTABLISHED}
Theory/07b_agent_network_rg.tex:76:  \theoremheading{...}{thm:rg-pointwise-parent-datum}
Theory/07b_agent_network_rg.tex:1788: The full pointwise datum of \Cref{...} has two declared alternatives,
Theory/07b_agent_network_rg.tex:2165: The static construction of \Cref{...} supplies no fine evolution
Theory/appendix_claim_ledger.tex:191,222: (ledger citations)
```

and `grep -n "cg-pointwise-parent\|06_general\|derivations/" Theory/07b_agent_network_rg.tex`
returns **nothing**. The pointer runs 06 to 07b only; 07b points nowhere. Nor does 07b cite the
derivation package (`Theory/` contains no reference to `docs/derivations/` at all). So a reader of
the manuscript alone has an ESTABLISHED theorem with zero justification, and the one internal
pointer that exists is directed the wrong way.

`solid_RG_theory.md` defines the status word it is relying on: "ESTABLISHED means proved in the
contained package **or in the cited canonical theorem source**." Neither disjunct is satisfied
inside `Theory/`: the theorem is not proved there and it cites no source.

**Evidence:** the greps above; my reading of 07b:60-190 in full; counts
`grep -c "theoremheading"` = 13 vs `grep -cE "paragraph\{Proof|emph\{Proof"` = 29.

**Falsifier:** a proof of `thm:rg-pointwise-parent-datum` elsewhere in `Theory/*.tex`, or a
cross-reference from 07b to `Theory/06`'s "Pointwise parent specialization" paragraph or to the
derivation package. I searched for both and found neither.

**Fix (smallest repair):** after 07b:178 insert a proof paragraph:

> Normalization, the observation-marginal identity, and the selected posterior identity are the
> pointwise-parent specialization of `\Cref{thm:cg-evidence-preserving-channel}` recorded at
> `\eqref{eq:cg-pointwise-parent-posterior}`--`\eqref{eq:cg-pointwise-parent-posterior-test}`.
> Absolute continuity follows because $\boldsymbol\Pi_{A,o,X}(D)=0$ forces $C_A(Y,D)=0$
> $\boldsymbol\Pi_{I,o,X}$-a.s., hence $\mathbb Q_{I,o,X}$-a.s. by hypothesis, hence
> $\mathbb Q_{A,o,X}(D)=0$. The marginal identities are the definition of pushforward. Equation
> `\eqref{eq:rg-pointwise-parent-kl-chain}` is `\Cref{thm:rg-exact-coarse-vfe}` applied to the joint
> lifts $\widehat{\mathbb Q}=\mathbb Q_{I,o,X}\otimes C_A$ and
> $\widehat{\boldsymbol\Pi}=\boldsymbol\Pi_{I,o,X}\otimes C_A$, whose Radon-Nikodym derivative is
> $r(Y)=d\mathbb Q_{I,o,X}/d\boldsymbol\Pi_{I,o,X}$ and whose relative entropy therefore equals the
> fine one; the relative-entropy chain rule on a standard Borel product then splits it. $\square$

plus a `\Cref{eq:cg-pointwise-parent-posterior}` back-pointer. I verified each of those steps myself
— see the next finding.

---

### [Low] The mathematics of `thm:rg-pointwise-parent-datum` and derivation sections 1-7 CHECKS OUT

**Location:** `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md`
sections 1-7; `Theory/06_general_coarsegraining.tex:301-331`

Reported honestly as a zero-defect result. I re-derived every load-bearing step:

- **(3.2)/(3.5) posterior pushforward.** With indicators $\varphi=\mathbf 1_E$, $g=\mathbf 1_D$,
  (3.5) *is* the regular-conditional identity $\mathbb P_A(E\times D\mid X)=\int_E
  \boldsymbol\Pi_{A,o,X}(D)\nu_X(do)$ — no monotone-class step is even needed for that particular
  conclusion, so the shorter route taken in the `Theory/06` paragraph is sound. Checks out.
- **(3.6) absolute continuity.** Checks out (argument reproduced in the Fix above).
- **(6.2) lift density.** For bounded $\phi(Y,z)$:
  $\int\phi\,d\widehat{\mathbb Q}=\iint\phi(Y,z)C_A(Y,dz)\,r(Y)\boldsymbol\Pi_{I,o,X}(dY)
  =\int \phi\,r\,d\widehat{\boldsymbol\Pi}$, so
  $d\widehat{\mathbb Q}/d\widehat{\boldsymbol\Pi}=r(Y)$. Checks out.
- **(6.3).** $\mathrm{KL}(\widehat{\mathbb Q}\Vert\widehat{\boldsymbol\Pi})=\int r\log r\,
  d\widehat{\boldsymbol\Pi}=\int r(Y)\log r(Y)\,\boldsymbol\Pi_{I,o,X}(dY)$ since
  $C_A(Y,\mathsf Z_A)=1$. Checks out.
- **(6.4).** Chain rule applied to the $z$-disintegration of the lifts; the $z$-marginals are
  $\mathbb Q_{A,o,X}$ and $\boldsymbol\Pi_{A,o,X}$. Valid in $[0,+\infty]$. Checks out.
- **(6.7)/(6.8).** Both terms nonnegative and summing to a finite quantity implies both finite; the
  equality case is "nonnegative integrand, zero integral implies zero a.e." plus Gibbs. Checks out.
- **(6.12) converse.** $\mathrm{KL}(\mathbb Q_I\Vert\boldsymbol\Pi_I)\ \ge\
  \mathrm{KL}(\mathbb Q_A\Vert\boldsymbol\Pi_A)\ \ge\
  \mathrm{KL}(\mathbb Q_AR\Vert\boldsymbol\Pi_AR)=\mathrm{KL}(\mathbb Q_I\Vert\boldsymbol\Pi_I)$,
  so all three are equal; finiteness then gives $\Delta_A=0$ from (6.4). Checks out, and the
  finiteness premise really is needed and is correctly flagged.
- **(7.4)/(7.5) covariance.** $\int f(z')\,(T_A^g)_\#(\boldsymbol\Pi_{I,o,X}C_A)(dz')
  =\int\left[\int f(T_A^gz)C_A(Y,dz)\right]\boldsymbol\Pi_{I,o,X}(dY)
  =\int C_A'(f)(T_I^gY)\,\boldsymbol\Pi_{I,o,X}(dY)
  =\int C_A'(f)(Y')\,\boldsymbol\Pi'_{I,o',X'}(dY')$, using (7.4) then (7.2). The printed chain is
  exactly this. Checks out.
- **(6.5)/(6.6) VFE.** $\mathcal F=-\log p_X(o)+\mathrm{KL}$ is the standard identity; adding a
  fixed finite real preserves the extended-real equality; "a finite VFE may be negative" is correct
  precisely because $p_X$ is a density against a general sigma-finite $\lambda_X$ and may exceed 1.
  Checks out.

The derivation is careful in places where a weaker document would not be: it distinguishes the
induced from the predeclared evaluator tier and writes the compatibility hypothesis (4.4) as a
displayed equation rather than assuming it; it says explicitly that (7.2) is a **version**
hypothesis that almost-sure uniqueness does not supply; it says the presentation quotient needs its
own regularity theorem; and it states that the $X_A$ notation does **not** prove cross-$X$
factorization. Those are the right calls. **Nothing in sections 1-7 is wrong.**

---

### [Medium] `thm:rg-pointwise-parent-datum` is a typed restatement of the Markov-kernel DPI-with-defect; the added prose never says so, and does not carry the chain-rule citation the rest of the manuscript already has

**Location:** `Theory/07b_agent_network_rg.tex:153-178`;
`overview.md` "Full pointwise candidate-parent theorem"; `solid_RG_theory.md` "Phase 1"

**Claim as stated:** overview.md — "**Full pointwise candidate-parent theorem** ... manuscript status
**ESTABLISHED**, release ledger `EVIDENCE_VERIFIED`, terminal status `COMPLETE_AFFIRMATIVE` ... a
normalized recognition-independent $C_A$ sends the fine generative joint, selected posterior-version
family, and correlated recognition law to a normalized parent triple with the observation
unchanged."

**Defect:** stripped of typing, the content of `eq:rg-pointwise-parent-kl-chain` is

$$\mathrm{KL}(Q\Vert\Pi)=\mathrm{KL}(QK\Vert\Pi K)+\int \mathrm{KL}\bigl(\widehat Q(\cdot\mid z)\big\Vert\widehat\Pi(\cdot\mid z)\bigr)(QK)(dz)$$

for a Markov kernel $K$ — the exact-deficiency form of the data-processing inequality, obtained by
the relative-entropy chain rule applied to the joint lift. The remaining conclusions are (i)
pushforward of a probability measure under a Markov kernel is a probability measure, and (ii) a
kernel acting only on the conditioned variable carries a regular conditional probability to a
regular conditional probability. The genuinely new content is the *typing* — which coordinates are
retained, which hypotheses the evaluator seam needs, and the version-selection discipline. That
contribution is real, and the prose never claims otherwise in so many words; but it also never says
that the analytic core is standard, and the release framing ("terminal status
COMPLETE_AFFIRMATIVE", "Phase 1 ESTABLISHED", headline of the 8/15 live front) invites the opposite
reading.

**Evidence:** the reconstruction in the preceding finding derives the entire chain from the DPI plus
the chain rule. Primary source for the chain rule in the extended-valued Polish-space form is
**P. Dupuis and R. S. Ellis, *A Weak Convergence Approach to the Theory of Large Deviations*
(Wiley, 1997), Theorem C.3.1**: for Polish $\mathcal X,\mathcal Y$ and $\gamma,\tau\in
\mathcal P(\mathcal X\times\mathcal Y)$,
$R(\gamma\Vert\tau)=R(\gamma_1\Vert\tau_1)+\int R(\gamma(\cdot\mid x)\Vert\tau(\cdot\mid x))\,
\gamma_1(dx)$, both sides permitted to be $+\infty$. The DPI itself is
**I. Csiszar, "Information-type measures of difference of probability distributions and indirect
observations", Studia Sci. Math. Hungar. 2 (1967) 299-318** — already `@article{Csiszar1967}` in
`references.bib`.

Note also that the repository **already** cites the chain rule properly at
`Theory/05_elbo.tex:452` — "regular conditional distributions of the posterior exist and the
relative entropy chain rule is available \citep{Klenke2020}" — with `Klenke2020` at
`references.bib:4438`. The new theorem (07b:153-160) invokes the same fact with no citation and no
cross-reference. The derivation package is likewise unsourced: its section 6 says only "invoking the
**standard extended-valued chain theorem** through the nonnegative generator
$\phi_0(t)=t\log t-t+1$ and its monotone truncations". That is a proof sketch, not a proof, in the
document that is supposed to *be* the proof.

**Falsifier:** a place in the added material that states the DPI/chain-rule provenance, or a
citation at 07b:157.

**Fix:** at 07b:153 write "Apply the same normalized Markov-kernel channel $C_A$ ... The additive
identity in $[0,+\infty]$ — the exact-deficiency form of the Markov data-processing inequality
\citep{Csiszar1967}, obtained from the relative-entropy chain rule on a standard Borel product
\citep{Klenke2020,DupuisEllis1997} — is ...". Add `DupuisEllis1997` to `references.bib`. In
`overview.md` and `solid_RG_theory.md`, replace "the released full pointwise theorem" framing with
"the released theorem types the parent datum and specializes the exact-deficiency data-processing
identity to it".

---

### [Medium] `cor:hist-compact-feller-operational-quotient` applies a definition outside the domain that definition declares, and its proof therefore has a gap

**Location:** `Theory/05d_relational_inference.tex:1319-1339` (definition) and `1450-1465` (corollary)

**Claim as stated:**
Definition (05d:1320): "For a finite DAG **on finite state spaces**, let \(J_v\) be a compact subset
of the normalized stochastic-kernel polytope at node \(v\), **with its Euclidean, equivalently
evaluation-subspace, topology**. ... This is a compact metrizable topological monoid."
Corollary (05d:1450): "If the node spaces are **compact Polish**, the palettes are compact
metrizable, each \(\bot_v\) is isolated, and all baseline and replacement kernels are jointly Feller
..., then the finite-coordinate right-override monoid in
\eqref{eq:hist-normalized-soft-right-override} has weakly continuous retained response. Its
contextual quotient is compact metrizable with continuous multiplication and response.
**Finite-coordinate does not mean finite cardinality.**"

**Defect:** the corollary's hypothesis (compact Polish node spaces) is strictly weaker than the
definition's (finite state spaces), so `eq:hist-normalized-soft-right-override` as defined does not
exist under the corollary's hypotheses. Two concrete breakages:

1. There is no "Euclidean topology" on the stochastic-kernel set at a node with an infinite compact
   Polish state space, and "Euclidean, equivalently evaluation-subspace" is then a false
   equivalence: for kernels into an infinite compact Polish space the setwise/evaluation topology
   and the weak topology genuinely differ, and only the latter is compact.
2. The definition's assertion "This is a compact metrizable topological monoid" was justified (in
   the definition's own sentence, and in the derivation package's Theorem 4 proof) by finiteness of
   the polytope dimension. The corollary needs that same conclusion for compact-metrizable palettes
   and **never re-establishes it** — yet `\Cref{thm:hist-compact-operational-quotient}`, which the
   corollary's proof invokes, has "compact metrizable monoid with jointly continuous multiplication"
   as a hypothesis. The corollary's two-sentence proof addresses only response continuity.

The slogan "Finite-coordinate does not mean finite cardinality" is the hedge that papers over this:
it shows the author noticed the tension and patched it with a disclaimer instead of restating the
definition.

**Evidence:** the two quoted hypothesis clauses are incompatible in the direction used. The
derivation package hits the same seam and handles it slightly better but still loosely — its
section 7 opens "Assume **in addition** that all node spaces are compact Polish", which is not an
addition to section 4's "finite node state spaces" but a replacement of it, and its Theorem 7 proof
asserts "Compactness and multiplication were proved in Theorem 4 without using finiteness of palette
cardinality" — true of palette *cardinality*, but Theorem 4's compactness argument did use the
finite-dimensional polytope.

**Falsifier:** a reading on which "finite state spaces" in the definition is not a hypothesis of the
construction but only of the accompanying response-continuity remark. I do not think that reading
survives "let $J_v$ be a compact subset of the normalized stochastic-kernel polytope ... with its
Euclidean ... topology", which is the palette's *definition*.

**Fix (one sentence each):**
- In the definition, split the topological hypothesis: "let $J_v$ be a compact metrizable space of
  normalized kernels at node $v$ — for finite state spaces, a compact subset of the stochastic-kernel
  polytope in its Euclidean, equivalently evaluation, topology; in general, a compact metrizable set
  of kernels in the topology declared for that tier."
- In the corollary's proof, add: "Compactness and joint continuity of $\star$ hold in this tier as
  well: $\prod_v(\{\bot_v\}\sqcup J_v)$ is a finite product of compact metrizable spaces, and since
  each $\{b_v=\bot_v\}$ is clopen, $(a,b)\mapsto(a\star b)_v$ is continuous on each of two clopen
  pieces."

---

### [Medium] "Smooth" carries two incompatible technical meanings, and the release's own notation scan is structurally incapable of catching it

**Location:** `Theory/05d_relational_inference.tex:1437-1448`, and the same sentence propagated to
`Theory/SPEC.md`, `overview.md`, `solid_RG_theory.md`

**Claim as stated:** 05d:1437 "The construction supplies an algebraic contextual quotient but does
not by itself establish a standard-Borel quotient; that requires an exhibited **smooth** classifier
or stronger topological hypotheses." 05d:1448 "Standard Borelness alone does not make the
uncountable contextual equivalence relation **smooth**."

**Defect:** here "smooth" is the descriptive-set-theoretic notion — an equivalence relation $E$ on a
standard Borel $X$ is *smooth* iff there is a Borel $f:X\to Z$ into a standard Borel space with
$xEy \iff f(x)=f(y)$ (Effros; see H. Becker and A. S. Kechris, *The Descriptive Set Theory of Polish
Group Actions*, LMS Lecture Note Series 232, Cambridge, 1996, sections 1-2). Everywhere else in the
same file and the same manuscript, "smooth" means $C^\infty$: 05d:110 "smooth sections", :113
"specified smooth locally convex manifold structure", :1600 "For a smooth retained-law map
$\rho:\Theta\to N$", :2202 "No result here establishes that the projectable set is a smooth
submanifold", :2310 `prop:hist-coarse-map-smoothness`; and `Theory/02_geometry.tex` builds the whole
smooth tier on that meaning.

The collision is not benign. Within twenty lines, 05d:1437-1456 says "does not ... establish a
standard-Borel quotient; that requires an exhibited **smooth** classifier" and then "Compact-Polish
state spaces ... give a compact metrizable quotient". A reader carrying the manuscript's own
definition of "smooth" concludes that the obstruction is about differentiability and that
compactness supplies differentiability. Both are false. The sentence is propagated verbatim into
all three human-facing summaries.

**Evidence:** the line-by-line usage above (`grep -n "smooth" Theory/05d_relational_inference.tex`).
And the release's own notation certificate cannot see it:
`docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation-registry.json` lists 39
`expected_symbols`, all LaTeX macros (`C_A`, `\mathscr P_G`, `\boldsymbol\Pi_{A,o,X}`, ...), and

```
$ grep -c "smooth" .../evidence/notation-collision-report.json
0
```

The scanner is symbol-based; a natural-language term carrying two technical meanings is outside its
detection model. So the "Phase 0: collision-free notation standard — COMPLETE" claim in
`solid_RG_theory.md` section 12 is true of symbols only, and the document does not say so.

**Falsifier:** a definition of "smooth equivalence relation" somewhere in `Theory/` that
disambiguates the two uses. I found none.

**Fix:** replace both occurrences with the unambiguous term — "...that requires the contextual
equivalence relation to be concretely classifiable (*smooth* in the descriptive-set-theoretic sense
of \citet{BeckerKechris1996}, i.e. Borel reducible to equality on a standard Borel space), or
stronger topological hypotheses" — and add one line to `solid_RG_theory.md` section 12 Phase 0
recording that the collision scan covers symbols, not terminology.

---

### [Medium] "An exact fifteen-coordinate minor" — the minor is never specified, so the determinant identity is unverifiable from the manuscript

**Location:** `Theory/05d_relational_inference.tex:1396-1414`
(`thm:hist-randomized-hard-intervention-nonidentifiability`); `Theory/SPEC.md`, randomized paragraph

**Claim as stated:** "For each released fifteen-class BSC monoid, the deterministic complete
two-sided contextual vectors are linearly independent. **An exact fifteen-coordinate minor**, with
\(\delta\) denoting passive crossover, has $\det M(b,\delta)=\frac{(2b-1)^6(2\delta-1)^3}{32}$,
which is nonzero for both models at \(\delta=5/12\)."

**Defect:** "an exact fifteen-coordinate minor" identifies no minor. The complete contextual
signature is a $15\times900$ matrix (15 protocol classes by 15 left contexts by 15 right contexts by
4 retained atoms), so the stated value is specific to one of astronomically many candidate minors. A
reader cannot check the identity, and the identity is what certifies rank 15, which is what the
whole randomized no-go rests on.

**Evidence / resolution — I paid this one down.** The minor is pinned only in
`docs/derivations/2026-08-14-operational-intervention-extensions/evidence/recompute.py`
(`SELECTED_COLUMNS`). I ran it:

```
$ python docs/derivations/2026-08-14-operational-intervention-extensions/evidence/recompute.py
```

Exit 0. Relevant output, cross-checked against my own hand computation:

- class order `["noop","O0","O1","E0","E1","R0","R0O0","R0O1","R0E0","R0E1","R1","R1O0","R1O1","R1E0","R1E1"]`
- selected flat column indices `[0,1,2,3,12,14,16,18,20,42,300,301,302,312,316]`
  (flat index = 4*(15*left_class + right_class) + atom)
- $L_1$ ($b=1/3$, $\delta=5/12$): Gaussian elimination, integer Bareiss, and the closed formula all
  give $-1/5038848$; hand check $(-1/3)^6(-1/6)^3/32=-1/(729\cdot216\cdot32)=-1/5038848$. Agrees.
- $L_2$ ($b=1/4$, $\delta=5/12$): all three give $-1/442368$; hand check
  $(-1/2)^6(-1/6)^3/32=-1/(64\cdot216\cdot32)=-1/442368$. Agrees.
- `minor_rank = complete_contextual_rank = 15` for both.
- soft face at $\epsilon=1/8$: diameters $1/4$ and $3/8$, matching $(1-2\epsilon)/3=1/4$ and
  $(1-2\epsilon)/2=3/8$ from my independent derivation.
- the $5/6,1/6$ convexification claim: $\tfrac56(3/8,1/8,3/8,1/8)+\tfrac16(1/8,3/8,1/8,3/8)
  =(1/3,1/6,1/3,1/6)$, equal to $L_1$'s `do(E=0)` response. Agrees.

So the identity is **true**. The defect is purely that the manuscript does not say which minor, and
`Theory/` never references the script (`grep -n "derivations/" Theory/*.tex` returns nothing). The
script itself is scrupulous: it records `"exact_rational_values_are_corroborative_not_proofs": true`.

**Falsifier:** a specification of the fifteen columns inside `Theory/` that I missed.

**Fix:** the logical need is only linear independence, so state that and demote the determinant to a
witness: "the deterministic complete two-sided contextual vectors have rank fifteen; on the fifteen
coordinates listed in the released `recompute.py` (contexts $(\mathrm{noop},\mathrm{noop})$,
$(\mathrm{noop},E_0)$, $(\mathrm{noop},E_1)$, $(\mathrm{noop},R_0)$, $(\mathrm{noop},R_1)$,
$(R_0,\mathrm{noop})$, $(R_0,E_0)$, $(R_0,E_1)$ with the indicated atoms) the minor is
$(2b-1)^6(2\delta-1)^3/32$, nonzero at $\delta=5/12$." Or prove rank 15 directly and drop the
determinant.

---

### [Low] Vague quantifiers and dropped hypotheses in the summary prose — resolved

**Location:** `overview.md`, operational-intervention boundary paragraph; `Theory/07b:181`

All three are framing prose, not load-bearing steps, and all three resolve by substitution:

1. **"The operational-intervention boundary is now exact in `several` declared categories."**
   RESOLVED: the number is **five** — (i) finite hard typed BSC
   (`thm:hist-finite-typed-intervention-nonidentifiability`), (ii) the marked normalized soft
   mediator face (`thm:hist-soft-bsc-target-face-nonidentifiability`), (iii) independently
   randomized affine (`thm:hist-randomized-hard-intervention-nonidentifiability`), (iv) declared
   standard-Borel (`prop:hist-standard-borel-intervention-semantics`), (v) compact-Feller with the
   circle pair as witness (`cor:hist-compact-feller-operational-quotient`,
   `thm:hist-circle-heat-intervention-nonidentifiability`). Replace "several" with "five".

2. **"Under compact-metrizable monoid and continuous-response hypotheses, a countable dense
   contextual signature realizes a compact metrizable quotient"** drops two of the four hypotheses
   `thm:hist-compact-operational-quotient` actually uses: *jointly* continuous multiplication, and
   $Y$ metrizable **Hausdorff**. Both are load-bearing — joint continuity is what gives
   $u_nav_n\to uav$, and Hausdorffness is what makes the limit unique in the density argument.
   `Theory/SPEC.md` states all four correctly and even flags them ("Compactness and the quotient-map
   hypotheses are load-bearing"); `overview.md` should copy SPEC's sentence.

3. **"generally lossy"** (07b:181). RESOLVED exactly: the loss is $\Delta_A(o,X)\ge0$ of
   `eq:rg-pointwise-parent-defect`, zero iff the two discarded conditionals agree
   $\mathbb Q_{A,o,X}$-a.s. Replace with "lossy with exact loss $\Delta_A(o,X)$".

---

### [Low] `EVIDENCE_VERIFIED` and `COMPLETE_AFFIRMATIVE` appear in the human-facing start page without definition

**Location:** `solid_RG_theory.md`, "Status key" and section 11; `overview.md`, "Full pointwise
candidate-parent theorem"

**Claim as stated:** "Its release metadata records ledger state `EVIDENCE_VERIFIED`, terminal status
`COMPLETE_AFFIRMATIVE`, and target digest `15336a68...`"; and section 11 "The current package
terminal status is COMPLETE_AFFIRMATIVE for the exact frozen full-datum conjunction, and its
`target` ledger entry is EVIDENCE_VERIFIED. Those package labels report release evidence; the
canonical manuscript theorem is ESTABLISHED."

**Defect:** the Status key defines ESTABLISHED / CONDITIONAL / DIAGNOSTIC / OPEN-TODO and then
introduces two *further* status words that it does not define, in typewriter font that reads as
external certification. The one disambiguating clause — "Those package labels report release
evidence" — does not say what "release evidence" is or who produced it, and the same document's
definition of ESTABLISHED ("proved in the contained package") makes clear that the answer is: the
same construction, in the same package.

**Fix:** append to the Status key — "`EVIDENCE_VERIFIED` and `COMPLETE_AFFIRMATIVE` are states of
the release package's own machine-readable ledger, assigned by the construction that produced the
package. They record that the package's internal checks and recompute scripts ran and agreed; they
are not an independent review and carry no weight beyond the proofs they point to."

---

### [Medium] The 8/15 rename left bare `Q` denoting a **principal bundle** in the chapter it renamed, and the release's own collision scan reports PASS because it cannot see unregistered symbols

**Location:** `Theory/02_geometry.tex:723-762` (`\section{Optional product-gauge extension}`);
standard at `solid_RG_theory.md` section 12 Phase 0 and `Theory/SPEC.md` Phase-0 block;
certificate at
`docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation-collision-report.json`

**Claim as stated:** the Phase-0 standard (`solid_RG_theory.md` section 12, repeated in `SPEC.md`):
"$\mathscr P_G\to\mathcal C$ denotes a principal bundle when that object is needed. Full generative
and recognition laws use $\mathbb P$ and $\mathbb Q$, and the posterior uses $\boldsymbol\Pi$.
**Bare $P$ and $Q$ may occur only as explicitly local dummy measures or inside a frozen historical
theorem whose types are stated nearby.**" And: "### Phase 0: collision-free notation standard --
COMPLETE ... The exit gate is closed by the authoritative registry, migration record, scanner
self-test, and stored collision report in the full-datum package."

**Defect:** the rename pass edited `Theory/02_geometry.tex:729` ("replace the ambient
$\mathscr P_G$ by") and left the next three lines untouched:

```latex
\pi_b:P_b\to\mathcal C,  \qquad  \pi_m:P_m\to\mathcal C,  \qquad
Q=P_b\times_{\mathcal C}P_m,
```
"where $Q$ is a principal $G_b\times G_m$-bundle" (02:736), and again at 02:752
"$Q\times_{G_b\times G_m}\operatorname{Map}(\mathcal B_b,\mathcal B_m)$".

So bare $Q$ denotes a **principal bundle** in the live geometry chapter. This is neither a "local
dummy measure" nor a "frozen historical theorem" — it is `\section{Optional product-gauge
extension}`, a current normative section, and the whole point of the 8/15 $P\to\mathscr P_G$ rename
was to stop principal bundles from colliding with probability symbols. $Q$ is the recognition-law
letter throughout `Theory/03` (`Q_X(\cdot\mid o)`), `Theory/05`, `Theory/05b`
(`$\KL(Q'\Vert\Pi_o)$`), and the new `\mathbb Q_I,\mathbb Q_A`. $P_b,P_m$ have the same problem
in the milder direction that bare $P$ at least has a documented legacy alias.

**Evidence:** the quoted lines; and the certificate cannot detect it. The registry
(`notation-registry.json`) has 39 `expected_symbols` and no entry for bare `Q`, `P_b`, or `P_m`; the
scanner (`notation_scan.py:355-356`) works by finding a *registered canonical token* and testing the
surrounding context against that symbol's `forbidden_uses` list. An **unregistered** symbol used for
a registered symbol's concept is outside its detection model. Result:

```
status: PASS
counts: {'canonical': 837, 'documented_legacy': 15, 'immutable_evidence': 91,
         'unclassified_collision': 0}
```

with `Theory/02_geometry.tex` in `source_coverage.active_files`. The scan scanned the file and
passed it. Note also that the registry *legitimizes* bare `P` for bundles by listing
`legacy_aliases: [{alias: "P", scope: "legacy principal-bundle passages"}]` under `\mathscr P_G` —
which contradicts the Phase-0 prose rule that bare `P` may occur "only as explicitly local dummy
measures or inside a frozen historical theorem".

**Falsifier:** a reading on which `sec:geo-product-extension` counts as a "frozen historical
theorem"; or a rule elsewhere in the standard that exempts principal bundles other than
$\mathscr P_G$ and $\mathscr P_\ell$.

**Fix:** rename to $\mathscr P_b,\mathscr P_m,\mathscr P_{b\times m}$ throughout
`sec:geo-product-extension` (7 occurrences); delete the bare-`P` legacy alias from the registry or
restrict its `scope` to the specific frozen passages; and amend the Phase-0 exit-gate sentence in
`solid_RG_theory.md` to "the scan verifies that registered symbols are used with their registered
concepts; it does not detect an unregistered symbol carrying a registered concept, and terminology
collisions in prose are out of scope."

---

### [Low] `Theory/03_probability.tex` `def:prob-model-evaluation` types a Chapter-3 object at a point defined only in Chapter 12 and the notation appendix

**Location:** `Theory/03_probability.tex:75, 88, 91`

**Claim as stated:** "A model-law section has value $q_i^{m;o,X}(r_*)\in\mathcal P(\mathsf M_i)$";
"The model-law section $q_i^{m;o,X}(r_*)$, that coordinate, and its evaluated kernel
$K^X_{i,m_i}$ are three different types"; "In the definite-presentation case the law is
$q_i^{m;o,X}(r_*)=\delta_{m_i}$."

**Defect:** $r_*$ is a point of $\mathcal U_A=\bigcap_{i\in I}\mathcal C_i$. Neither $r_*$ nor
$\mathcal U_A$ nor the child block $I$ exists in Chapter 3; `grep -n "r_\*"
Theory/03_probability.tex` returns exactly those three lines and nothing that introduces the symbol.
It is declared only in `Theory/SPEC.md:196` and `Theory/appendix_notation.tex:25`, and used in the
body only from Chapter 12 (`07b:80`). So a `\status{DEFINITION}` in the measure-theoretic typing
chapter evaluates a section at a point whose definition arrives nine chapters later.

The evaluation at $r_*$ is also gratuitous: nothing in `def:prob-model-evaluation` — the
presentation space, the evaluation map, joint measurability, normalization, or the type distinction
it exists to make — depends on which base point is chosen.

**Evidence:** the greps above.

**Falsifier:** a Chapter-3 declaration of $r_*$ that I missed.

**Fix:** write "A model-law section over $\mathcal C_i$ has values $q_i^{m;o,X}(c)\in\mathcal
P(\mathsf M_i)$ for $c\in\mathcal C_i$" and drop $r_*$ from all three lines.

---

### [Low] Correction and sharpening of the comparison-category finding: the categories ARE defined — in the evidence package, not the manuscript

**Location:** `docs/derivations/2026-08-14-operational-intervention-extensions/evidence/direct-derivation.md`
section 1 vs `Theory/05d_relational_inference.tex:1341-1380`, `1467-1513`

I said above that the comparison category is "never defined". That is right about `Theory/`, and I
am correcting it about the corpus as a whole: the 08-14 derivation package **does** define it, at
its section 1:

> "an admitted relabeling is one global quintuple $(f_R,f_E,f_O,\Theta,U)$. The three $f$ maps are
> invertible typed state maps and preserve the ordered roles $R$=input/parameter, $E$=mediator,
> $O$=output/observation. Pushing every baseline and replacement kernel through them induces the
> single protocol-monoid isomorphism $\Theta$. The single protocol-independent boundary-response
> isomorphism $U$ obeys $\Phi'(\Theta(a))=U(\Phi(a))$... For ordinary retained laws, $U$ is the
> pushforward induced by $f_R\times f_O$. **In the circle tier the state maps also intertwine every
> heat kernel.** No map in this category exchanges $R$ with $O$, reverses the chain orientation,
> erases the mediator face, or chooses a different response relabeling for different protocols."

That is a complete, checkable morphism specification, and with it the circle no-go is airtight: if
$f_O$ intertwines every $H_r$, then $(f_O)_\#(\nu H_t)=((f_O)_\#\nu)H_t$, so
$(f_O)_\#\mathcal R_t=\mathcal R_t\ne\mathcal R_s$, contradicting Theorem 9. I verified that step.

**The sharpened statement of what actually holds** (what I would put in the manuscript in place of
"under maps that preserve ... circle heat geometry"):

> Fix the category whose objects are the two marked mediator experiments and whose isomorphisms are
> quintuples $(f_R,f_E,f_O,\Theta,U)$ with $f_\bullet$ bimeasurable bijections preserving the
> ordered roles, $f_E$ and $f_O$ intertwining every $H_r$, $\Theta$ the induced protocol-monoid
> isomorphism, and $U=(f_R\times f_O)_\#$ the single protocol-independent response intertwiner. In
> that category the two chains are nonisomorphic. **What remains open** is whether an isomorphism
> exists when $f_O$ is allowed to be an arbitrary bimeasurable bijection of $\mathbb T$: that would
> require $(f_O)_\#\{\nu H_t\}=\{\nu H_s\}$, and neither a construction nor an obstruction is given
> here. The heat-intertwining hypothesis is therefore load-bearing, not cosmetic.

The same sharpening applies to `thm:hist-soft-bsc-target-face-nonidentifiability`: the proof needs
exactly "every admitted isomorphism restricts to a total-variation-preserving bijection of the
marked mediator faces", and that follows from the quintuple definition, not from anything stated in
`Theory/`.

**Fix:** transplant the section-1 quintuple into `Theory/05d` as a `\definitionheading` and reference
it from both no-go theorems.

---

## Summary counts

By severity: **Critical 0, High 2, Medium 6, Low 3 defects**, plus 3 `[Low]`-tagged non-defect
blocks (two verified-correct results reported honestly, one self-correction).

By file (primary location; defects only):

| file | High | Medium | Low |
|---|---|---|---|
| `Theory/07b_agent_network_rg.tex` | 1 | 2 | 0 |
| `Theory/05d_relational_inference.tex` | 1 | 3 | 0 |
| `Theory/02_geometry.tex` | 0 | 1 | 0 |
| `Theory/03_probability.tex` | 0 | 0 | 1 |
| `overview.md` / `solid_RG_theory.md` / `Theory/SPEC.md` | 0 | (shared with the rows above) | 2 |

By hedge category, after triage of the 72 lexicon candidates plus the 100 corpus-specific tokens:

| category | candidates | load-bearing | resolution |
|---|---|---|---|
| "declared / declare" | 35 | 2 | 33 name a specific checkable hypothesis (dropped); 2 sharpened |
| "admitted" | 17 | 1 | "admitted $o$" hides an undeclared $\lambda_X,p_X$ — sharpened, fix given |
| "selected" | 21 | 0 | every use names an explicit version-selection hypothesis; correctly used |
| "typed" | 18 | 0 | framing; the typing is written out where it matters |
| "where retained" | 4 | 2 | folded into the comparison-category finding |
| "standard" uncited | 5 | 2 | chain rule and kernel-integration measurability — citations supplied |
| vague quantifier | 3 | 1 | "several" resolved to "five" |
| unquantified magnitude | 2 | 1 | "generally lossy" resolved to $\Delta_A(o,X)$ |
| epistemic ("may") | 32 | 0 | all technical; "a finite VFE may be negative" is proved |
| "almost" | 27 | 0 | all the technical term "almost surely" |

**Load-bearing vs framing.** The two High findings and four of the six Medium findings sit in
load-bearing mathematical steps (missing proof; undefined $p_X$ under which the VFE identity is
stated; the corollary applied outside its definition's domain; the unspecified minor certifying rank
15; the terminology collision that changes what "does not establish a standard-Borel quotient"
means; the residual bundle-$Q$ collision). The remaining Medium (citation/novelty) and all Low
findings sit in framing prose and status vocabulary.

**What did not need paying down.** Contrary to the brief's expectation, "declared" in this corpus is
overwhelmingly an honest device: it names an object and a property and the property is then used.
The document is also unusually good at rung-5 residual statements — "Without a finiteness premise,
$\Delta_A=0$ exactly when..."; "family-wide recovery still requires simultaneous hypotheses"; "that
requires an exhibited [classifier] or stronger topology"; "Disintegration proves existence of the
induced tier; it does not validate an arbitrary predeclared evaluator" — each of which is exactly
the precise-open-problem form this skill asks for. I found no instance of a hedge concealing a false
statement.

## Coverage

**Read in full:**
- `git diff 060f80e^ 8ce6358 -- overview.md solid_RG_theory.md` (387 diff lines) — every hunk.
- `git diff ... -- Theory/05d_relational_inference.tex Theory/07b_agent_network_rg.tex
  Theory/02_geometry.tex Theory/03_probability.tex Theory/06_general_coarsegraining.tex`
  (778 diff lines) — every hunk.
- `git diff ... -- Theory/SPEC.md` (207 diff lines) — every hunk.
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md` — all 499
  lines.
- `docs/derivations/2026-08-14-operational-intervention-extensions/evidence/direct-derivation.md` —
  all 553 lines.
- `Theory/07b_agent_network_rg.tex:60-190` in the current file (to confirm the absent proof).
- `Theory/02_geometry.tex:720-762` in the current file.
- `Theory/appendix_claim_ledger.tex:185-225` in the current file.
- `docs/derivations/.../evidence/notation-registry.json` in full.

**Sampled / targeted:**
- `docs/derivations/2026-08-14-.../evidence/recompute.py` — lines 195-324 read; whole script
  **executed** (exit 0, output captured and cross-checked by hand for the determinant, the soft-face
  diameters, the passive law, and the 5/6-1/6 mixture).
- `docs/derivations/2026-08-15-.../evidence/notation_scan.py` — grepped for its token/forbidden-use
  logic (lines 20, 164, 355-356, 500-537), not read in full.
- `notation-collision-report.json` — structure and summary counts read via a script; the 837-entry
  `canonical` list not read entry by entry.
- `references.bib` — grepped for the specific sources at issue (Myhill, Nerode, Schützenberger,
  Eilenberg, Pin, Blackwell, Dupuis, Kallenberg, Klenke, Csiszár, Kechris); 466 entries not read.
- `Theory/03_probability.tex` and `Theory/05_elbo.tex` — targeted greps for reference measures, the
  chain rule, and the exceptional-observation proposition; not read in full.

**Not reached (out of scope or not needed for this sweep):**
- The other evidence files in both packages: `adversarial-attacks.md`, `counterexample-proofs.md`,
  `independent-reconstruction.md`, `oracle-erasure.md`, `reviews/*.md`, `claim-ledger.json`,
  `adversarial-report.json`, `release*.json`, `construction-or-strongest-theorem.md`,
  `counterexample-register.md`. Per the brief I treated none of these as evidence, and did not read
  them. **Consequence:** the soft-BSC and randomized proofs' full detail lives in
  `counterexample-proofs.md`, which I did not read; I verified those two results independently
  instead (by hand, and by executing `recompute.py`).
- `Theory/` chapters not in scope: 01, 04, 05, 05a, 05b, 05c, 06_gaussian, 06a, 07, 07_restrictions,
  08-12, `appendix_notation.tex` (grepped only).
- `docs/change-logs/2026-08-15.md`, `docs/STATUS.md`, `docs/superpowers/*` — out of scope.
- `finite_nongaussian_witness.py` (466 lines) in the 8/15 package — not run, not read.
- I did **not** attempt to falsify the pre-existing
  `thm:hist-finite-typed-intervention-nonidentifiability`, on which the randomized no-go depends by
  reduction; it predates the 8/15 diff and is outside scope. If that theorem is wrong, the
  randomized result falls with it.
