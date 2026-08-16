# P1 — Measure-Theoretic Probability Review

STATUS: COMPLETE

**Reviewer role:** independent investigator, measure-theoretic probability (standard Borel spaces,
Markov kernels, disintegration, regular conditional probability, absolute continuity,
Radon–Nikodym derivatives, almost-sure qualifiers).

**Target revision:** 8ce635807a6ca2a388255fc996c98f7c535e5843 (branch review/2026-08-15-deep-review)

**Stance:** internal attestations (claim ledger, adversarial report, internal domain reviews,
oracle-erasure records) are NOT evidence and are not inherited. Only the mathematics is evaluated.

## Files to examine

- [x] docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md (READ IN FULL, 498 lines)
- [x] docs/derivations/2026-08-15-full-pointwise-meta-agent/construction-or-strongest-theorem.md (READ IN FULL, 118 lines)
- [x] docs/derivations/2026-08-15-full-pointwise-meta-agent/problem-contract.json (READ IN FULL, 76 lines)
- [x] docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/independent-reconstruction.md (READ IN FULL, 62 lines)
- [x] (context) claim-ledger.json claim ids/states/assumptions (enumerated programmatically)
- [x] (context) docs/change-logs/2026-08-15.md and commits f4b1a61, 063a5bb (the late a.s.-qualifier repair)
- [x] (context) targeted greps of evidence/reviews/*.md for the specific points at issue

## Headline verdict

**The measure-theoretic core of Sections 1–3, 5, and 6 is correct.** I reconstructed every
load-bearing step and additionally verified them on an exact finite instance with a non-injective
channel. No step in the parent-construction / posterior-version / absolute-continuity / KL-chain
argument is false, and the one step the review brief flagged as "most likely to be wrong"
(pushforward of a conditional version) is in fact correct *because* of a hypothesis the document
states explicitly and correctly.

The defects I found are of the second kind the brief anticipates: **claims that are true but whose
surrounding notation or framing asserts more than the proof delivers**, plus one genuinely
unqualified almost-sure statement, one untyped object, and several certification-hygiene problems.
No Critical finding. Counts: Critical 0, High 3, Medium 6, Low 2 (11 total).

**The single most consequential finding is prior art inside this same repository.** Sections 1–3 and
the whole of §6 other than the defect term restate four results that have been sitting in
`Theory/06_general_coarsegraining.tex` since commit `bd46058` (2026-08-08) with `\status{ESTABLISHED}`
and with primary-source citations that the new package drops. See finding [High-1].

---

## Findings

### [High-1] Sections 1–3 and §6 restate four theorems already ESTABLISHED in this repository a week earlier, with no citation and no hypothesis mapping — violating the frozen contract's own `literature_policy`

**Location:** `evidence/direct-derivation.md` §§1–3 and §6 (lines 25–150, 246–379) vs.
`Theory/06_general_coarsegraining.tex` at revision `060f80e^` (added by commit `bd46058`,
2026-08-08): `thm:cg-kl-dpi-extended`, `cor:cg-pairwise-bayes-recovery`,
`cor:cg-dpi-infinite-equality-warning`, `thm:cg-evidence-preserving-channel`.
Contract clause: `problem-contract.json:74`.

**Claim as stated:**
> `problem-contract.json:74` — "Use only checked primary sources **or released repository
> derivations** for invoked theorems; record exact statements and hypothesis mappings."
> `construction-or-strongest-theorem.md:106` — "Kernel integration proves normalization and preserves
> the observation marginal. Equation-level disintegration against bounded observation and parent test
> functions proves the posterior version globally. Null-set transfer through the same kernel proves
> parent absolute continuity. ... The posterior conditional supplies the forward recovery direction,
> while data processing through a separately assumed common reverse kernel proves the finite
> converse."
> `claim-ledger.json` — `PARENT-NORMALIZATION`, `POSTERIOR-PUSHFORWARD`,
> `COMMON-CHANNEL-ABSOLUTE-CONTINUITY`, `VFE-FINITE-ZERO-DEFECT-RECOVERY` each recorded as
> `EVIDENCE_VERIFIED` with `EV-TASK3-DIRECT-DERIVATION` as evidence.

**Defect:** These are not new derivations. The pre-existing theorem statements are the same theorems
under a renaming `(\mathsf X,\mathsf Y,K,P_o,Q_o) \mapsto
(\mathsf Y_I,\mathsf Z_A,C_A,\boldsymbol\Pi_{I,o,X},\mathbb Q_{I,o,X})`, and in several places the
new text reproduces the older proof move for move. Nothing in the package cites them, maps their
hypotheses, or records that these ancestors were already closed. The contract required exactly that,
and the four internal domain reviews reporting Critical/High/Medium `0/0/0` did not surface it.

**Evidence (verbatim, from `git show 060f80e^:Theory/06_general_coarsegraining.tex`):**

*Prior `thm:cg-evidence-preserving-channel`* — matches (3.1), (3.3), (3.4), (3.5), and the version
remark at :45/:141:
> "Let `$\mathsf O$, $\mathsf X$, and $\mathsf Y$` be standard Borel. Fix one normalized joint
> `$P(do,dx)$` and fix a measurable regular-conditional kernel `$o\mapsto P_o$` of `$X$` given `$O$`
> under `$P$`. Let `$K:\mathsf X\rightsquigarrow\mathsf Y$` be a Markov channel satisfying
> `$K(x,\mathsf Y)=1$` for every `$x\in\mathsf X$`, and suppose that it does not read the arbitrary
> recognition law `$Q_o$`. Define `\bar P(do,dy)=\int K(x,dy)P(do,dx), \bar P_o:=P_oK` for every
> `o`, `\bar Q_o:=Q_oK`. The declared kernel `$o\mapsto\bar P_o$` is a regular conditional law of
> `$Y$` given `$O$` under `$\bar P$`, **including its selected exceptional-point values**. Fix a
> selected regular observation `$o$` and use the same declared evidence density representative
> `$p(o)$` for the fine and coarse slices. Then `$\bar P^O=P^O$` ... `\status{ESTABLISHED}`"

with the proof:
> "Normalization of `$K$` preserves the observation marginal. Kernel integration makes
> `$o\mapsto(P_oK)(B)$` measurable ... `\int_A(P_oK)(B) P^O(do) = \int_A\int_{\mathsf X}K(x,B)P_o(dx)
> P^O(do) = \bar P(A\times B)`. A `$\pi$--$\lambda$` extension proves the regular-conditional
> identity. Thus the pointwise declaration `$\bar P_o:=P_oK$` selects a compatible version rather
> than applying an almost-sure identity at an arbitrarily fixed exceptional observation."

This is the new (3.5) proof, the new (3.3), and the new :45/:141 version discussion, all four.

*Prior `cor:cg-pairwise-bayes-recovery`* — matches (6.9), (6.10), (6.11), (6.12) exactly:
> "Let `\(R_Q(y,dx)\)` be a regular conditional law of `\(X\)` given `\(Y=y\)` under `\(\mathbb Q\)`.
> Then `\(QKR_Q=Q\)`, and under `\eqref{eq:cg-kl-equality}`, `\(PKR_Q=P\)`. Conversely, any one
> kernel `\(R\)` recovering both `\(P\)` and `\(Q\)` forces equality in `\eqref{eq:cg-kl-dpi}`.
> `\status{ESTABLISHED}`" — proof: "Disintegration gives the first identity. ... The converse follows
> by applying data processing through `\(K\)` and then `\(R\)`."

The new (6.10) is `QKR_Q=Q`; the new (6.11) is `PKR_Q=P` under equality; the new (6.12) is the stated
converse, with the same one-line DPI-through-`K`-then-`R` proof.

*Prior `cor:cg-dpi-infinite-equality-warning`* — matches the new :379:
> "Equality `$\KL(PK\Vert QK)=\KL(P\Vert Q)=+\infty$` alone need not imply a common reverse kernel
> recovering `$P$` and `$Q$`. `\status{ESTABLISHED}`" — with a finite counterexample proof.

*Prior `thm:cg-kl-dpi-extended`* — supplies (6.2) and the DPI used in (6.12), **with citations the
new package drops**:
> "`\frac{d(PK)}{d(QK)}=\bar r,\quad \KL(PK\Vert QK)\leq\KL(P\Vert Q)` ... equality holds exactly
> when `r(X)=\bar r(Y)` `\(\mathbb Q\)`-almost surely. ... This is the information-loss theorem of
> `\citet{Kullback1951,Csiszar1967}` in kernel form."

`Kullback1951` and `Csiszar1967` are live keys in `Theory/references.bib` (lines 717, 726).
`grep -rniE "kullback|csisz|kallenberg|dupuis|..."` over the entire 8/15 derivation package returns
**zero hits**: the new package cites neither the primary sources nor the repository theorem.

Commit date confirmation: `git log -1 --format="%h %ad" bd46058` → `bd46058 2026-08-08`, i.e. seven
days before the program's first commit `ceffda2`.

**What is actually new**, stated fairly: the product typing
`\mathsf Z_A=\mathsf B_A\times\mathsf M_A\times\boldsymbol\Xi_A\times\mathsf H_A`; the upgrade of the
DPI *inequality plus separate equality condition* to the *additive chain identity* (6.4) with the
named nonnegative defect `\Delta_A` (a genuine strengthening, and the correct one); the reformulation
of the equality condition from `r(X)=\bar r(Y)` `\boldsymbol\Pi`-a.s. to conditional-law equality
`\mathbb Q_{A,o,X}`-a.s. at (6.8) (equivalent, not stronger); the evaluator disintegration §4; the
named marginals §5; the groupoid covariance §7; the dynamics typing §8. The affirmative
probabilistic core is not new.

**Falsifier:** A citation, hypothesis-mapping table, or "prior repository result" note anywhere in
the 8/15 package pointing at `Theory/06_general_coarsegraining.tex`. I grepped the package for
`06_general`, `cg-`, `Kullback`, `Csiszar` and for `\cite`: nothing. Also falsified if
`Theory/06_general_coarsegraining.tex` were itself written by this program — it was not; the four
results are present at `060f80e^`, and the program's only edit to that file (`fe08359`) changed two
lines.

**Fix:** Add to `direct-derivation.md` §§1–3 and §6 an explicit "prior results invoked" note naming
`thm:cg-evidence-preserving-channel`, `thm:cg-kl-dpi-extended`, `cor:cg-pairwise-bayes-recovery`,
`cor:cg-dpi-infinite-equality-warning` with the symbol map, restore the `Kullback1951, Csiszar1967`
citations, and change the ledger evidence for `PARENT-NORMALIZATION`, `POSTERIOR-PUSHFORWARD`, and
`VFE-FINITE-ZERO-DEFECT-RECOVERY` to record that these ancestors were already closed. Restrict the
package's novelty statement to (6.4), §4, §5, §7, §8.

---

### [High-2] Equation (4.5) literally asserts the cross-X factorization that §9 explicitly disclaims, and the violation is normative, not incidental

**Location:** `evidence/direct-derivation.md` §4, lines 156–208 (esp. (4.1) at :163, (4.5) at :204);
also `construction-or-strongest-theorem.md` :42, :50, and `problem-contract.json` :35 (`ev_A` typing).

**Claim as stated:**
> (4.5) `\mathbb P_A(db_A,do,dh_A\mid \xi_A,m_A,X) = K^{X_A}_{A,m_A}(\xi_A;db_A,do,dh_A) \quad\mu_A^{M\Xi}\text{-almost surely}.`

and, at :498,
> "It supplies no ... cross-(X) factorization."

**Defect:** In the induced tier the evaluator is *defined* as `K^{X_A}_{A,m_A}(\xi_A;\cdot) :=
G_A^X(m_A,\xi_A;\cdot)` (:190), and `G_A^X` is constructed by disintegrating `P_A(\cdot\mid X)` — it
depends on the *fine* datum `X`, not on `X_A=\chi_A(X)`. Displaying it with the superscript `X_A`
asserts, on the face of the equation, exactly the factorization through `X_A` that §9 disclaims.
Equation (4.5) then reads with `X` on the left and `X_A` on the right, which is a false statement
under a literal reading. The document contains the correct caveat (:190: "The notation `X_A` does
not prove cross-`X` factorization ... is an additional premise"), but the caveat sits inside the
induced-tier paragraph while the notation is used globally, including in (7.6) at :454 and in the
released strongest-theorem statement.

**Evidence:** Trace of the definition chain in the document itself:
- :176–:188 — `\mu_A^{M\Xi}(\cdot\mid X)` is the `(M_A,\Xi_A)` marginal of `\mathbb P_A(\cdot\mid X)`;
  (4.3) determines `G_A^X` from `\mathbb P_A(\cdot\mid X)` alone.
- :190 — "Choosing `K^{X_A}_{A,m_A}(\xi_A;\cdot)=G_A^X(m_A,\xi_A;\cdot)`".
- Therefore two fine data `X\neq X'` with `\chi_A(X)=\chi_A(X')` and different `\mathbb P_I(\cdot\mid X)`
  produce different induced kernels carrying the *same* symbol `K^{X_A}_{A,m_A}`.
Concretely: take `\mathsf M_A=\boldsymbol\Xi_A=\{*\}`, `\mathsf W_A=\{0,1\}`, `\chi_A` constant, and
`\mathbb P_A(\cdot\mid X)` giving `W_A` mass `(1/3,2/3)` while `\mathbb P_A(\cdot\mid X')` gives
`(2/3,1/3)`. Both have the same `X_A`; the induced kernels differ; the notation says they are one
object.

**The violation is normative.** `evidence/notation-standard.md:33` — the package's own *normative*
registry — declares:
> "| Parent evaluation | `$\operatorname{ev}_A(m_A)=K^{X_A}_{A,m_A}$` | Measurable normalized kernel
> in `$\operatorname{Kern}(\boldsymbol\Xi_A,\mathsf B_A\times\mathsf O_A\times\mathsf H_A)$`. |"

and immediately above it, line 20, the *fine* evaluation is registered with the fine datum:
> "| Model evaluation | `$\operatorname{ev}_i(m_i)=K^X_{i,m_i}$` | ... evaluation at fixed structural
> `$X$`. |"

So the registry deliberately contrasts `K^X_{i,m_i}` with `K^{X_A}_{A,m_A}`: the parent evaluator is
normatively typed as a function of `X_A`. The same file's collision contract at line 44 says "One
canonical token has one semantic type in a theorem. A type change requires another symbol." The
induced tier gives `K^{X_A}` a second semantic type (a function of `X`), which by the package's own
rule requires a different symbol. The fail-closed scanner reports zero unclassified collisions
because it matches tokens, not types — `notation_scan.py`'s failure conditions
(`notation-standard.md:54`) are all lexical.

**Falsifier:** A statement in the package (which I did not find) declaring `K^{X_A}` to be *notation
for a family indexed by the pair `(X_A, X)`*, or a hypothesis that the induced kernel is
`\chi_A`-measurable in `X`. Also falsified if `\chi_A` is somewhere required injective. I checked
`evidence/notation-standard.md` in full and queried every `X_A`-bearing entry of
`evidence/notation-registry.json`; the `\operatorname{ev}_A` registry entry gives
`domain_codomain: "M_A -> Kern(Xi_A,B_A x O_A x H_A)"` and forbidden uses
`["recognition-dependent kernel","model law"]` — no `X`-dependence escape clause.

**Fix:** Write the induced object as `K^{X}_{A,m_A}` (or `G^X_A`) and reserve the `X_A` superscript
for the predeclared tier, where dependence on `X_A` alone is a genuine standing hypothesis. One
symbol change; no mathematics moves.

---

### [Medium] (7.6) is the one almost-sure statement in the derivation with no measure and no defined exceptional set

**Location:** `evidence/direct-derivation.md` §7, lines 448–457.

**Claim as stated:**
> "(7.6) `(T_B^g\times T_O^g\times T_H^g)_\# K^{X_A}_{A,m}(\xi;\cdot) = K^{X_A'}_{A,T_M^gm}(T_\Xi^g\xi;\cdot)`
> holds on the compatibility domain. Equations (4.4) and (7.6) then make the transformed generative
> conditional compatible with the transformed evaluator."

**Defect:** "the compatibility domain" is used exactly once in the entire package and is never
defined. Every other exceptional set in the derivation is named with its measure —
`\nu_X`-a.e. (:45), `\boldsymbol\Pi_{I,o,X}`-a.e. and `\mathbb Q_{I,o,X}`-a.s. (:143),
`\mu_A^{M\Xi}`-a.e. (:197, :206, :210), `\widehat{\boldsymbol\Pi}_{I,o,X}`-a.s. (:264),
`\mathbb Q_{A,o,X}`-a.s. (:342). Equation (7.6) is a *hypothesis* of the covariance branch and is
carried by `ASM-HOLONOMY-BLIND-DATA` in the ledger; a hypothesis whose exceptional set is unnamed
cannot be checked by a user of the theorem. The correct qualifier is deducible — it must be
`\mu_A^{M\Xi}(\cdot\mid X)`-almost every `(m,\xi)`, so that the pushforward statement lands
`(T_M^g\times T_\Xi^g)_\#\mu_A^{M\Xi}=\mu_A'^{M\Xi}`-a.e. and composes with (4.4) — but the document
does not say it, and the second sentence ("Equations (4.4) and (7.6) then make ... compatible") is
asserted with no proof and no null-set bookkeeping at all.

**Evidence:** `grep -rn "compatibility domain"` over the whole package returns three hits: the
derivation line 457, and two lines in the *internal* gauge-holonomy review
(`evidence/reviews/view-gauge-holonomy.md:56,116`) which reuse the same undefined phrase
("on the transported compatibility domain") rather than defining it. No definition exists.
Note also that the composition argument silently needs `T_M^g` and `T_\Xi^g` to be *bimeasurable
bijections* individually (a pushforward of a disintegration is a disintegration of the pushforward
only when the conditioning map is invertible); the document asserts bimeasurability of `T_A^g`
(:385–:393) and only that `T_A^g` "decomposes into measurable maps" (:448), which is weaker.

**Falsifier:** A definition of "compatibility domain" elsewhere in the tracked repository that
supplies a measure and a set. I grepped the package directory only; a definition in
`Theory/*.tex` would weaken this finding to Low.

**Fix:** Replace "holds on the compatibility domain" with "holds for
`\mu_A^{M\Xi}(\cdot\mid X)`-almost every `(m_A,\xi_A)`", and add the one-line proof that
`(T_M^g\times T_\Xi^g)` bimeasurable transports the a.e. statement to the target slice.

---

### [Medium] `\mathbb Q_{A,o,X}` is typed as an "observation-indexed kernel" although `\mathbb Q_{I,o,X}` is only ever declared at one observation and is never assumed measurable in `o`

**Location:** `evidence/direct-derivation.md` :55–:62 ((1.2)) and :121–:128 ((3.4)).

**Claim as stated:**
> ":121  Define, as observation-indexed kernels and not merely as isolated slices,
> (3.4) `\boldsymbol\Pi_{A,o,X}=\boldsymbol\Pi_{I,o,X}C_A, \quad \mathbb Q_{A,o,X}=\mathbb Q_{I,o,X}C_A`."

**Defect:** For `\boldsymbol\Pi` the kernel typing is earned: (1.1) supplies a *measurable*
regular-conditional kernel `o\mapsto\boldsymbol\Pi_{I,o,X}`, and composition with `C_A` preserves
measurability. For `\mathbb Q` nothing of the sort is available. (1.2) fixes "a normalized, possibly
correlated recognition law `\mathbb Q_{I,o,X}\in\mathcal P(\mathsf Y_I)`" — a single measure — and
`problem-contract.json:25` is explicit that it is supplied "at one admitted `(o,X)`"
(likewise `ASM-RECOGNITION-AC`: "At the admitted `(o,X)` ..."). Measurability of
`o\mapsto\mathbb Q_{I,o,X}` is never hypothesized, and outside the admitted `o` the object does not
exist. Calling `\mathbb Q_{A,o,X}` an observation-indexed kernel therefore types an object that has
not been given that type, in a document whose stated method is exact typing.

**Evidence:** `problem-contract.json` :25 — "every normalized correlated recognition law
`Q_{I,o,X}` absolutely continuous with respect to `Pi_{I,o,X}`" appears in the quantifier list with
no measurability-in-`o` clause; `ASM-RECOGNITION-AC` (claim-ledger) — "At the admitted `(o,X)`,
`Q_{I,o,X}` is a normalized correlated recognition law ...". `direct-derivation.md` contains no
hypothesis on `o\mapsto\mathbb Q_{I,o,X}`.

Downstream harm is nil: every later use of `\mathbb Q_{A,o,X}` (§5 (5.2)–(5.3), §6, §7 (7.3)) is at
the single admitted `o`. So this is a typing overstatement, not a broken proof.

**Falsifier:** A hypothesis anywhere in the package that `o\mapsto\mathbb Q_{I,o,X}` is a measurable
kernel. I did not find one.

**Fix:** Split the sentence: "`\boldsymbol\Pi_{A,\cdot,X}` is defined as an observation-indexed
kernel; `\mathbb Q_{A,o,X}` is defined at the admitted `o` only, and no measurability in `o` is
claimed or used."

---

### [Medium] The frozen contract's domain quantifies over "admitted **regular** observations", a term the derivation never defines and never uses

**Location:** `problem-contract.json` :30 (`domains`), :25 (`quantifiers`), :57 (`premises`);
`construction-or-strongest-theorem.md` :12; `evidence/direct-derivation.md` :45, :53.

**Claim as stated:**
> `problem-contract.json:30` — "Admitted regular observations `o` with finite unchanged evidence."
> `problem-contract.json:57` — "`Pi_{I,o,X}` is a selected posterior derived from `P_I` at an
> admitted regular observation `o`."

**Defect:** The derivation defines "admitted" (:45 "a point at which this selected version, its
evidence representative, and every later slice-wise expression are declared to be used"; :53 "admit
only the present `o` with `0<p_X(o)<\infty`") but never defines "regular", and the word "regular"
never appears in the derivation except inside "regular conditional probability" (:23, :31, :141,
:424 — a different, standard use). A contract whose universal quantifier ranges over a class named
by an undefined adjective does not have a checkable domain. Because the derivation's actual
admission condition is `0<p_X(o)<\infty` plus a version declaration, the honest reading is that
"regular" is vestigial — but a reader cannot know that, and a notation scanner reporting "zero
unclassified collisions" did not catch it because it is a natural-language term, not a symbol.

**Evidence:** `grep -n "regular" evidence/direct-derivation.md` returns lines 23, 31, 141, 424, 498;
all five are "regular conditional probabilit(y|ies)", "regular-conditional kernel",
"regular conditionals", or "regular presentation quotient". None defines a regular *observation*.

**Falsifier — checked and closed.** I read `evidence/notation-standard.md` in full (54 lines) and
queried every `regular`-bearing entry of `evidence/notation-registry.json`. Neither defines a
"regular observation"; the only registry hit is `"selected regular conditional derived from the fine
generative joint"`, which is the unrelated standard term. `grep -rn "regular observation"` over
`Theory/` shows the term is inherited from `Theory/06_general_coarsegraining.tex:273` ("Fix a
selected regular observation `$o$`") and `Theory/appendix_notation.tex:302` ("The slice is primary at
a selected regular observation"), where it is *also* undefined. So the term is legacy vocabulary
carried into a frozen contract's domain specification without ever having been given a definition
anywhere in the repository. This finding stands at Medium.

**Fix:** Either delete "regular" from the three contract strings, or define it in §1 of the
derivation as exactly the admission condition `0<p_X(o)<\infty` together with the declared version.

---

### [Medium] The invoked *standard* theorems carry no primary sources either (companion to [High-1], which covers the repository derivations)

**Location:** `problem-contract.json` :67–:74 (`permitted_theorems`, `literature_policy`) vs.
`evidence/direct-derivation.md` (whole file).

**Claim as stated:**
> `problem-contract.json:74` — "Use only checked primary sources or released repository derivations
> for invoked theorems; record exact statements and hypothesis mappings. No novelty or priority
> claim is made."
> `problem-contract.json:67–71` — permitted theorems: normalized Markov-kernel pushforward and
> composition; existence and use of regular conditional probabilities and disintegrations; "KL data
> processing and the common-channel conditional-KL chain rule".

**Defect:** The derivation invokes at least four standard theorems — the disintegration/rcp
existence theorem on standard Borel spaces (:23, :176, :278), the monotone-class/functional
monotone-class theorem (:112, :141), the relative-entropy chain rule for disintegrations in
`[0,+\infty]` (:286–:302), and the data-processing inequality for KL under Markov kernels (:370) —
and cites no source for any of them. There is no bibliography, no theorem-number reference, and no
"hypothesis mapping" record anywhere in the package. A grep for the obvious primary sources
(Kallenberg, Dupuis–Ellis, Csiszár, Bogachev, Ambrosio, Parthasarathy, Doob, Cover & Thomas,
Léonard, Dudley, Billingsley, Klenke, Durrett, Folland) over the whole package returns **zero
hits**. The chain rule at (6.4) is precisely the load-bearing step and is the one most in need of a
statement-level citation, because its validity in `[0,+\infty]` without integrability hypotheses is
exactly what the argument leans on.

**Evidence:** command run —
`grep -rniE "kallenberg|dupuis|csisz|bogachev|ambrosio|parthasarathy|doob|cover *& *thomas|rockafellar|leonard|dudley|billingsley|klenke|durrett|folland" .` in
`docs/derivations/2026-08-15-full-pointwise-meta-agent/` → no output. Likewise no `\cite`, `[1]`,
or "Theorem N.N of" pattern in `direct-derivation.md`.

For the record, the correct citations are: disintegration / rcp existence — Kallenberg,
*Foundations of Modern Probability* (2nd ed.), Theorem 6.3 (Disintegration) and Theorem 5.3
(existence of regular conditional distributions on Borel spaces); relative-entropy chain rule in
`[0,+\infty]` — Dupuis & Ellis, *A Weak Convergence Approach to the Theory of Large Deviations*
(1997), Theorem B.2.1 / the chain-rule lemma for relative entropy on Polish product spaces;
DPI for relative entropy — Csiszár, "Information-type measures of difference of probability
distributions and indirect observations", *Studia Sci. Math. Hungar.* 2 (1967), and the standard
`f`-divergence monotonicity statement therein.

**This is a citation regression, not merely an omission.** The pre-existing repository theorem that
the new §6 restates ([High-1]) *does* cite the primary sources: `Theory/06_general_coarsegraining.tex`
at `060f80e^` closes the DPI proof with "This is the information-loss theorem of
`\citet{Kullback1951,Csiszar1967}` in kernel form", and both keys are live in
`Theory/references.bib` (lines 717 and 726). The 8/15 package restates the result and drops the
citations.

**Falsifier:** A bibliography or hypothesis-mapping artifact elsewhere in the repository bound to
this package. `release-assembly.json` / `release-provenance.json` list artifacts, not sources; I did
not find a bibliography. I also read `evidence/notation-standard.md` in full — it fixes symbols and
explicitly "proves no theorem" (line 4); it carries no citations.

**Fix:** Add a short "Invoked standard theorems" subsection to `direct-derivation.md` naming the
three results above with their exact hypotheses and the mapping to `\mathsf O`, `\mathsf Y_I`,
`\mathsf Z_A`. This is required by the contract, not optional.

---

### [Medium] The two evaluator "tiers" are not two tiers: within the theorem's pointwise scope, the predeclared tier is exactly the set of families a.e.-equal to the induced one

**Location:** `evidence/direct-derivation.md` §4 :174 ("There are exactly two valid construction
tiers"), :192–:199; `construction-or-strongest-theorem.md` :46.

**Claim as stated:**
> ":174 There are exactly two valid construction tiers."
> `construction-or-strongest-theorem.md:46` — "There are two valid tiers. First, a selected
> disintegration of `\mathbb P_A` proves existence ... Second, a family predeclared independently of
> `\mathbb P_A` is supplied as a normalized jointly measurable hypothesis and separately requires the
> explicit hypothesis that it agrees almost surely with the selected conditional ..."

**Defect:** Hypothesis (4.4) says `K^{X_A}_{A,m_A}(\xi_A;\cdot) = G_A^X(m_A,\xi_A;\cdot)` for
`\mu_A^{M\Xi}(\cdot\mid X)`-a.e. `(m_A,\xi_A)`. Since the theorem is explicitly pointwise in one
fixed `X` (:6, :498), (4.4) pins the predeclared family to the induced one up to a
`\mu_A^{M\Xi}`-null set and nothing else. The "second tier" therefore contains exactly the
equivalence class of `G_A^X` and adds no object the first tier does not already supply — its only
freedom is the choice of values on a null set, which §4 itself immediately identifies as the residual
freedom of the induced tier as well (:210 "values on a `\mu_A^{M\Xi}`-null set are version choices").
The framing "exactly two valid construction tiers" implies a genuine dichotomy where the mathematics
gives one object and a null-set relabeling.

The place where the predeclared tier *would* have independent content is across several `X` in a
fiber of `\chi_A` — a single `K^{X_A}` required to be a.e.-equal to `G_A^X` for every such `X` is a
real restriction. But that is precisely the cross-`X` setting the theorem excludes (:190, :498).

**Evidence:** Direct reading of (4.4) at :195–:199 together with the pointwise scope declaration at
:6 ("This theorem is pointwise in this one `X`") and :498 ("supplies no ... cross-`X`
factorization"). No witness in `counterexample-proofs.md`'s `NEG-MODEL-MARGINAL-EVALUATION` shows a
predeclared family that satisfies (4.4) and is not a.e.-equal to the induced conditional — the
witness shows the opposite direction (a family that *violates* the seam), which is consistent with
my reading.

**Falsifier:** An example in the package of a predeclared evaluator satisfying (4.4) that differs
from `G_A^X` on a set of positive `\mu_A^{M\Xi}` measure. Such an example cannot exist, which is the
point.

**Fix:** Restate as: "There is one construction — the selected disintegration `G_A^X` — and one
compatibility seam. A predeclared family is admissible exactly when it lies in the
`\mu_A^{M\Xi}(\cdot\mid X)`-a.e. equivalence class of `G_A^X`. The predeclared tier acquires
independent content only in the excluded cross-`X` setting."

---

### [High-3] The prose claims the pointwise construction has been made "meaningful" for continuous `\mathsf O`, but only the evidence term is treated; the KL term has the identical null-slice pathology and receives only a fiat declaration

**Location:** `evidence/direct-derivation.md` §1 :45–:53; §6 :306–:333 ((6.5)–(6.7));
`problem-contract.json` :30, :41.

**Claim as stated:**
> ":45 The selected kernel is declared on every observation, while (1.1) determines it only
> `\nu_X`-almost everywhere. An admitted observation `o` is a point at which this selected version,
> its evidence representative, and every later slice-wise expression are declared to be used. No
> arbitrary conditional version is silently evaluated on an unspecified null slice."
> ":53 This extra declaration is what makes a pointwise evidence term meaningful when `\mathsf O` is
> continuous."

**Defect:** Line 53 asserts that the declaration of a `\lambda_X`-density representative makes the
*pointwise evidence term* meaningful. It does no such thing in any sense stronger than "we picked
one" — and, more to the point, the same problem afflicts the *other* summand of (6.5), the KL term,
which depends on `\boldsymbol\Pi_{I,o,X}` at a `\nu_X`-null point. Both `-\log p_X(o)` and
`\operatorname{KL}(\mathbb Q_{I,o,X}\Vert\boldsymbol\Pi_{I,o,X})` are, at an atomless `\nu_X`,
functions of an arbitrary version choice and **not** functions of the model data
`(\mathbb P_I(\cdot\mid X),\lambda_X,o,\mathbb Q_{I,o,X})`. Consequently
`\mathcal F_I(o,X)`, `\mathcal F_A(o,X)` and `\Delta_A(o,X)` — the quantities the package calls the
pointwise VFE and the pointwise defect, and about which the zero-defect criterion (6.8) and the
recovery equivalence (6.12) are stated — can be given essentially arbitrary values by a different
admissible selection, with every hypothesis of the theorem still satisfied. The theorem is a true
statement about the *declared objects*; it is not a statement about the model at `o`. §9's long list
of non-claims (:498) does not include this, and line 53's "meaningful" invites the opposite reading.

**Evidence (explicit construction).** Take `\mathsf O=[0,1]` with `\lambda_X=` Lebesgue,
`\mathsf Y_I=\{0,1\}`, and `\mathbb P_I(do,dY\mid X)=\mathrm{Leb}(do)\otimes\mathrm{Ber}(1/2)`.
Then `\nu_X=\mathrm{Leb}`, `p_X\equiv 1` is a valid everywhere-finite representative, and the
`\nu_X`-a.e. class of rcps is `\{\boldsymbol\Pi_{I,o,X}=\mathrm{Ber}(1/2)\}`.
- Version A: `\boldsymbol\Pi^{A}_{I,o,X}=\mathrm{Ber}(1/2)` for all `o`.
- Version B: `\boldsymbol\Pi^{B}_{I,o,X}=\mathrm{Ber}(1/2)` for `o\neq 1/2`, and
  `\boldsymbol\Pi^{B}_{I,1/2,X}=\delta_0`.
Both are measurable kernels satisfying (1.1) exactly. Admit `o=1/2` (`p_X(1/2)=1\in(0,\infty)`, so
it is admitted under the derivation's own condition at :53) and take
`\mathbb Q_{I,o,X}=\delta_0`, which is absolutely continuous with respect to *both* versions.
Then
`\mathcal F_I = -\log 1 + \operatorname{KL}(\delta_0\Vert\mathrm{Ber}(1/2)) = \log 2` under Version A,
and `\mathcal F_I = -\log 1 + \operatorname{KL}(\delta_0\Vert\delta_0) = 0` under Version B.
With `C_A=\mathrm{id}`, `\Delta_A=0` in both cases but `\mathcal F_A` inherits the same split.
Replacing `\delta_0` at `o=1/2` by `\mathrm{Ber}(\varepsilon)` makes `\mathcal F_I` any value in
`[0,\infty]`. Every frozen premise holds throughout.

Note this is *not* a counterexample to any displayed equation: (6.4)–(6.8) hold for each version
separately. It is a demonstration that the pointwise quantities are selection artifacts, so the
theorem is materially weaker than "a pointwise VFE closure for continuous observations".

**Falsifier:** A hypothesis in the package that `\nu_X(\{o\})>0` at admitted observations, or a
canonicity requirement on the version (e.g. `o` is a continuity/Lebesgue point of a chosen
continuous representative, or `\mathsf O` is discrete). `problem-contract.json:30` requires only
"finite unchanged evidence"; `:41` requires only finiteness of KL terms; neither excludes null
slices, and :47–:53 is written specifically for the continuous case, so no such hypothesis exists.

**Fix:** Add to §9's non-claim list and to the contract's `boundary_conditions`: "When
`\nu_X(\{o\})=0`, the numerical values of `\mathcal F_I`, `\mathcal F_A`, and `\Delta_A` are
determined by the declared version and are not functionals of
`(\mathbb P_I(\cdot\mid X),\lambda_X,\mathbb Q_{I,o,X},o)`; all statements at the admitted `o` are
statements about the declared objects." And soften :53 from "makes a pointwise evidence term
meaningful" to "fixes one finite representative for the evidence term; it does not make the value
canonical."

---

### [Medium] The hash-bound primary evidence artifact states that claims the released ledger closes as `EVIDENCE_VERIFIED` "remain CANDIDATE"

**Location:** `evidence/direct-derivation.md` :244 and :459, vs. `claim-ledger.json` (all 19 claims
`EVIDENCE_VERIFIED`) and `release.json` (`COMPLETE_AFFIRMATIVE`).

**Claim as stated:**
> ":244 ... the corresponding Task-4 claims remain (\texttt{CANDIDATE})."
> ":459 ... the Task-4 marginal-versus-joint claim remains (\texttt{CANDIDATE})."

**Defect:** `direct-derivation.md` is the artifact whose SHA-256
`2aa70b07751d07712a3d9395f77817317d48d77d97c3fd5fb8cd1a3f6fda226a` is recorded in
`construction-or-strongest-theorem.md:110` as the evidence closing the theorem, and it was last
edited at commit `1b18842` — *after* the Task-4 witnesses landed at `add1a69`. It therefore ships in
the certified release asserting a claim state that the same release contradicts. The internal
information/VFE review saw this and classified it as "nonblocking editorial"
(`evidence/reviews/view-information-vfe.md:140`), which is a disposition, not a repair.

**Evidence:** commands run —
`git log --oneline -- .../evidence/direct-derivation.md` → `1b18842, 22b5b36, d287164` (so the file
was edited at `1b18842`, which is after `add1a69`);
`python -c "hashlib.sha256(open(...).read())"` → `2aa70b07751d0771...` matching the recorded hash;
enumeration of `claim-ledger.json['claims']` → all 19 states are `EVIDENCE_VERIFIED`, including
"There exist finite parent laws with identical belief and model marginals but distinct dependence"
and "There exist full parent laws with invariant coordinate marginals but noninvariant joint
dependence".

**Falsifier:** A statement in the release binding `direct-derivation.md` as a *frozen Task-3
snapshot* explicitly exempt from Task-4 status updates. `release-assembly.json` binds it as current
evidence, not as a historical snapshot.

**Fix:** Replace both sentences with "no converse or reconstruction theorem is proved *here*; the
corresponding negative claims are closed by `evidence/counterexample-proofs.md`." One-sentence edit,
then rebind the hash.

---

### [Low] `evidence/independent-reconstruction.md` contradicts itself on the release state and disclaims its own independence

**Location:** `evidence/independent-reconstruction.md` :6, :8, :62.

**Claim as stated:**
> ":8 This is a sequential role-separated derivation by the Task-5 assembler, not independent-agent
> agreement. ... Accordingly, the result below supports the mathematical ancestors but does not
> promote `target` from `CANDIDATE` or set a terminal release status."
> ":62 ... All four corrected-byte domain reviews are current and `APPROVE` ... after their final
> hash binding, `target` is `EVIDENCE_VERIFIED`."

**Defect:** Within one 62-line file, §"Method" says the four domain reviews' inputs predate the
correction pass and that same-view re-review "remains a separate release gate", while §"Result"
declares them current and concludes the promotion. Separately, :6 asserts "It does not use
`evidence/direct-derivation.md` as an outline" — an unverifiable claim about the author's own
process, and :8 concedes the artifact is by the same agent. The artifact is registered in the ledger
as `EV-TASK5-INDEPENDENT-RECONSTRUCTION`, kind `DERIVATION`. Under the review brief's rules of
evidence (and under the repository's own verification policy that "agreement among agents is not
closure"), a same-author reconstruction is corroboration of arithmetic at best; the file's title and
ledger registration overstate it, and the file itself says so.

**Evidence:** the three quoted lines, read in full. Ledger evidence enumeration shows
`EV-TASK5-INDEPENDENT-RECONSTRUCTION | DERIVATION`, alongside four `AGENT_ASSESSMENT` review items.

**Falsifier:** A record showing the reconstruction was produced by a separate agent without access
to the derivation. :8 states the opposite.

**Fix:** Rename to `sequential-reconstruction.md`, downgrade the ledger evidence kind, and delete
either :8's non-promotion sentence or :62's promotion sentence so the file states one release state.

---

### [Low] `(7.2)` and the groupoid arrows never state `o' = T_O^g(o)`

**Location:** `evidence/direct-derivation.md` :385–:424.

**Claim as stated:**
> ":385 Let an arrow `g:(o,X)\to(o',X')` have bimeasurable actions `T_O^g:\mathsf O\to\mathsf O'`,
> `T_I^g:\mathsf Y_I\to\mathsf Y_I'`, `T_A^g:\mathsf Z_A\to\mathsf Z_A'` ..."
> ":404 (7.2) `(T_I^g)_\#\boldsymbol\Pi_{I,o,X}=\boldsymbol\Pi'_{I,o',X'}`"

**Defect:** The relation between the arrow's target observation `o'` and the action `T_O^g` on the
observation space is never stated. Without `o'=T_O^g(o)`, (7.1) (which transports the *joint*, hence
the observation marginal, by `T_O^g`) and (7.2) (which relates the posterior slice at `o` to the
slice at an unrelated `o'`) are not linked, and the two hypotheses could be jointly unsatisfiable or
vacuous depending on the reader's reading. The proof of (7.5) at :440–:446 does not use the relation,
so nothing displayed is false; the hypothesis set is simply under-specified.

**Evidence:** full read of §7; `o'` appears only as a subscript, never as an image of `o`.

**Falsifier:** A statement elsewhere fixing `o'=T_O^g(o)`. I found none in the package.

**Fix:** Add "with `o'=T_O^g(o)` and `X'` the declared target datum" to the arrow definition at :385.

---

## Things that check out (reported honestly)

I reconstructed each of these and additionally ran an exact finite verification
(script: scratchpad `p1_check.py`; `O={a,b}`, `Y_I={0,1,2}`, `Z_A={u,v}` so `C_A` is genuinely
non-injective; exact `Fraction` arithmetic for all measures).

Read together with [High-1]: everything in this section that concerns §§1–3 and (6.9)–(6.12) checks
out *and* was already established in `Theory/06_general_coarsegraining.tex` before this program
began. Both statements are true simultaneously — the mathematics is right, and it is not new.

**Q1 — the parent triple is well defined. CORRECT.**
(3.1) defines `\mathbb P_A` by integrating the kernel against `\mathbb P_I`; joint measurability of
`(o,Y)\mapsto\int 1_F(o,z)C_A(Y,dz)` follows from kernel measurability by the functional
monotone-class argument the document cites at :112; countable additivity by monotone convergence;
normalization from `C_A(Y,\mathsf Z_A)=1` for **every** `Y` (not a.e. — the document states the
everywhere version at :84, which is what is needed). The observation marginal is **proved**, not
assumed: `f\equiv1` in (3.2) gives `C_A f\equiv 1` and hence (3.3). Verified numerically:
parent mass `=1` exactly, and `\nu_A=\nu` exactly as rationals.

**Q2 — the disintegrations are correctly invoked. CORRECT.**
Three disintegrations are used: (1.1) rcp of `Y` given `O` under `\mathbb P_I`; (4.3) conditional of
`(B_A,O,H_A)` given `(M_A,\Xi_A)` under `\mathbb P_A`; (6.x) conditional of `Y` given `z` under each
lift. All three disintegrate a *probability* measure on a finite product of standard Borel spaces
over a coordinate projection — the exact hypotheses of the standard theorem (Kallenberg Thm 6.3), and
finiteness makes σ-finiteness vacuous. The only σ-finiteness that actually matters is the one the
document declares correctly: `\lambda_X` σ-finite with `\nu_X\ll\lambda_X` for the RN derivative
(:47). The disintegrating measure is stated correctly in each case (`\nu_X`; `\mu_A^{M\Xi}`; the
`z`-marginals `\mathbb Q_{A,o,X}` and `\boldsymbol\Pi_{A,o,X}`).
On a.s.-uniqueness: the argument **does** pick versions and then use pointwise properties of them,
but it says so, four separate times (:45, :141, :210, :424) — it is declared, not silent. The
residual consequence of that declaration is the [High] finding above; the handling of *uniqueness*
itself is correct.

**Q3 — the "pushforward of a version is a version" step. CORRECT, and correct for the right reason.**
This is the step the brief flagged as most likely to be wrong. It is not wrong here, because `C_A`
acts only on the conditioned variable and leaves the *conditioning* variable `O` fixed (:84). The
proof at (3.5) is complete: extend (1.1) from indicators to bounded measurable `g` by monotone class,
apply it to `g=C_Af`, and use `\mathbb P_A^O=\nu_X` from (3.3). Equivalently, the joint
`\mathbb P_I\otimes C_A` on `\mathsf O\times\mathsf Y_I\times\mathsf Z_A` has conditional law of
`(Y,Z)` given `O=o` equal to `\boldsymbol\Pi_{I,o,X}(dY)C_A(Y,dz)`, whose `z`-marginal is
`\boldsymbol\Pi_{I,o,X}C_A`.
Verified numerically: `\boldsymbol\Pi_{I,o}C_A` equals `P_A(o,\cdot)/\nu(o)` exactly, as rationals,
for both `o`, with a non-injective `C_A`.
**The hypothesis is load-bearing and the document states it.** I built the counterexample that shows
what fails without it: with the same data but a channel that *also* coarsens `O` by the constant map,
the true parent posterior given `o_A=*` is `(15/32,17/32)` while the pushforward
`\boldsymbol\Pi_{I,a}C_A` is `(1/2,1/2)` — not a version. The brief's warning is real; the document's
hypothesis "the observation coordinate ... stay[s] outside it" (:84) is exactly the right exclusion.

**Absolute continuity under a non-injective channel (3.6). CORRECT.**
The brief warns that `\ll` need not survive pushforward. For a *Markov kernel* it does, and the
document's three-line proof at :143 is the standard one and is valid: `\boldsymbol\Pi_A(D)=0`
`\Rightarrow` `C_A(\cdot,D)=0` `\boldsymbol\Pi_I`-a.e. `\Rightarrow` (by (1.2)) `\mathbb Q_I`-a.e.
`\Rightarrow` `\mathbb Q_A(D)=0`. What does *not* survive — and what the document correctly does not
claim — is preservation of the Radon–Nikodym derivative or of the KL value; those are handled by the
defect term.

**Q5 — almost-sure qualifiers. CORRECT except (7.6).**
I audited every a.s./a.e. statement in `direct-derivation.md`:
`\nu_X`-a.e. at :45 (measure on `\mathsf O`) ✓;
`\boldsymbol\Pi_{I,o,X}`-a.e. and `\mathbb Q_{I,o,X}`-a.s. at :143 (measures on `\mathsf Y_I`) ✓;
`\mu_A^{M\Xi}(\cdot\mid X)`-a.e. at :197, :206, :210 (measure on `\mathsf M_A\times\boldsymbol\Xi_A`) ✓;
`\widehat{\boldsymbol\Pi}_{I,o,X}`-a.s. at :264 for the RN derivative (correct — RN derivatives are
a.e.-unique with respect to the *dominating* measure) ✓;
`\mathbb Q_{A,o,X}`-a.s. at :342 for the zero-defect criterion (correct — the defect integral is
against `\mathbb Q_{A,o,X}`, not `\boldsymbol\Pi_{A,o,X}`) ✓;
version remark at :424 ✓.
The late repair recorded in the change log added exactly this `\mathbb Q_{A,o,X}` qualifier to
`Theory/appendix_notation.tex` (commit `063a5bb`); the derivation already carried it at :342. The one
statement lacking a measure is (7.6) at :457 — the [Medium] finding above.
A point the document does not remark on but which is needed and does hold: (6.11) uses `R_{\Pi,o,X}`,
a version determined only `\boldsymbol\Pi_{A,o,X}`-a.e., inside an integral against
`\mathbb Q_{A,o,X}`. This is legitimate *only* because (3.6) gives
`\mathbb Q_{A,o,X}\ll\boldsymbol\Pi_{A,o,X}`, so the version ambiguity is `\mathbb Q_{A,o,X}`-null.
The dependency is real and the conclusion is correct.

**Section 6 (extended KL chain, zero-defect, recovery). CORRECT.**
(6.2): for bounded `g`, `\int g\,d\widehat{\mathbb Q}=\int(\int g(Y,z)C_A(Y,dz))r(Y)\,d\boldsymbol\Pi_I
=\int g\,r\,d\widehat{\boldsymbol\Pi}`, so `r(Y)` is the joint derivative ✓ (verified exactly).
(6.3): `\int\phi_0(r)\,d\widehat{\boldsymbol\Pi}=\int\phi_0(r)\,d\boldsymbol\Pi_I` since the
`Y`-marginal of the lift is `\boldsymbol\Pi_I` ✓. The document's insistence on the nonnegative
generator `\phi_0(t)=t\log t-t+1` rather than raw `t\log t` (:286) is the correct technical care and
is not decoration — it is what makes the `[0,+\infty]` statement well posed without integrability
hypotheses.
(6.4): the standard relative-entropy chain rule for disintegrations over a Polish factor, valid in
`[0,+\infty]`. Verified numerically to `3.8e-17`:
`KL(Q_I‖Π_I)=0.028316506132566`, `KL(Q_A‖Π_A)=0.003476252202919`, `Δ_A=0.024840253929648`.
(6.8): zero integral of a nonnegative function against `\mathbb Q_{A,o,X}` iff a.e. zero, plus
`KL=0` iff equality ✓.
(6.10): holds for *any* channel, exactly — verified (`Π_A R = Π_I` exactly as rationals even though
`Δ_A>0`).
(6.12) converse: `KL(Q_I‖Π_I)\ge KL(Q_A‖Π_A)\ge KL(Q_AR‖Π_AR)=KL(Q_I‖Π_I)` forces equality, and
finiteness permits the subtraction ✓. The document's restriction of the two-way equivalence to the
finite tier, and its explicit statement that `+\infty=+\infty` supplies nothing (:379), are both
correct and are the conservative direction.
One honest scope note: (6.6) adds no content beyond (6.4), because `-\log p_X(o)` is *identical* at
both scales by (3.3) and cancels. The document says so itself at :320. The VFE framing is a relabel
of the KL chain rule.

**Q6 — marginals are projections. CORRECT, and trivially so.**
(5.2) *defines* the six parent marginals as coordinate pushforwards; nothing is defined
independently and then asserted consistent. (5.3) verifies one of the six identities and the other
five are identical in form. The claim "all named parent marginals are derived projections and do not
reconstruct the joints" is therefore true by construction on the forward half; the non-reconstruction
half is carried by the Task-4 witnesses (outside my scope). The same holds for the fine local laws
`q_i^{b;o,X}`, `q_i^{m;o,X}` at (1.3), which are also definitions (:64–:73), and the document says so.
Worth stating plainly: §9's "Section 5 derives, rather than posits, all belief and model marginals"
is accurate in the sense that no marginal is an independent posit, but no *theorem* is being proved
in §5 — it is a definition plus one line of Fubini.

**Q4 — separation of the two evaluator tiers. The induced tier does NOT smuggle in the predeclared
hypotheses, and the compatibility condition uses the right measure and null set.**
In the induced tier, `K:=G_A^X` makes (4.3) an exact identity, so no a.e. hypothesis is imported;
disintegration on standard Borel spaces delivers a kernel normalized at *every* point and jointly
measurable, which is exactly the type (4.1) demands, so the existence claim is genuinely a conclusion.
(4.4) is stated with `\mu_A^{M\Xi}(\cdot\mid X)`, the marginal that (4.3) integrates against — the
correct measure and the correct null set. The document's care at :172 (that (4.2) is an abbreviation
and no σ-algebra on an abstract kernel space is inferred) is the right call and avoids a real trap.
The separation is genuine; the residual problems are the notation (finding 1) and the fact that the
"second tier" is a null-set relabeling of the first (finding 6).

---

## Coverage

**Read in full:**
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md` (498 lines)
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/construction-or-strongest-theorem.md` (118 lines)
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/problem-contract.json` (76 lines)
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/independent-reconstruction.md` (62 lines)
- `docs/change-logs/2026-08-15.md`
- diffs of commits `f4b1a61` and `063a5bb` (the late a.s.-qualifier repair)

- `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation-standard.md` (54 lines)
- `Theory/06_general_coarsegraining.tex` at revision `060f80e^`, lines 62–160 and 255–330 (the four
  prior theorems establishing [High-1]); the current-revision counterpart lines 266–282

**Sampled / queried programmatically (not read in full):**
- `claim-ledger.json` — all 19 claim ids, states and statements enumerated; all 11 assumptions and
  11 evidence records enumerated. Proof bodies not present in this file.
- `evidence/notation-registry.json` — every entry containing `X_A`, `regular`, `K^`, or `ev`
  extracted and inspected.
- `Theory/appendix_notation.tex` lines 228–310 and the diffs of `f4b1a61`, `063a5bb` against it.
- `Theory/references.bib` — confirmed `Kullback1951` (line 717) and `Csiszar1967` (line 726) exist.
- `evidence/reviews/view-information-vfe.md`, `view-gauge-holonomy.md`, `view-probability-kernel.md`,
  `view-dynamics-scope.md` — grepped only, for the specific points at issue (`CANDIDATE` staleness,
  "compatibility domain"). Per the brief, these are attestations and were not treated as evidence.
- Whole package grepped for primary-source citations (zero hits) and for `compatibility domain`
  (three hits, no definition).

**Not reached (outside my scope or not needed for the questions asked):**
- `evidence/counterexample-proofs.md`, `evidence/finite_nongaussian_witness.py`,
  `evidence/finite-nongaussian-output.json` — the five negative conjuncts. Not read; the affirmative
  findings above do not depend on them. Recommend a separate pass.
- `evidence/adversarial-attacks.md`, `evidence/oracle-erasure.md`, `release.json`,
  `release-assembly.json`, `release-provenance.json`, `adversarial-report.json`,
  `approach-registry.json`, `dependency-dag.json`, `final-report.md`, `counterexample-register.md`.
- `evidence/notation_scan.py` (640 lines) and `notation-collision-report.json` (5732 lines) — not
  read; my claim that the scanner is lexical rests on its stated failure conditions at
  `notation-standard.md:54`, not on reading the code. A reader wanting to contest [High-2] should
  check the scanner for semantic type checking.
- The rest of `Theory/*.tex` (SPEC.md, 07b_agent_network_rg.tex, appendix_claim_ledger.tex, etc.) —
  the manuscript surfaces the change log says were edited in the same session. Given [High-1], a
  systematic diff of the 8/15 manuscript integration against the 2026-08-08 snapshot is worth a
  separate pass; I checked only `06_general_coarsegraining.tex` and `appendix_notation.tex`.
- The predecessor package `docs/derivations/2026-08-14-pointwise-meta-agent-rg`.

**Verification artifact:** exact finite check committed alongside this report at
`docs/reviews/2026-08-15-deep-review/findings/P1-finite-check.py`. Run with any CPython
(pure `fractions`/`math`; no torch, no model). It asserts (3.1), (3.3), (3.5), (3.6), (6.2), (6.4),
(6.10) and prints the necessity counterexample for the "observation unchanged" hypothesis. Output
reproduced inline in the "Things that check out" section.
