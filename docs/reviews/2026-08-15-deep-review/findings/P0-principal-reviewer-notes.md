STATUS: COMPLETE
AGENT: principal reviewer (Claude Opus 5), independent of the wave-1 panel
TARGET: 8ce635807a6ca2a388255fc996c98f7c535e5843

# Principal reviewer's independent notes

These are my own reconstructions, done before and alongside the wave-1 panel so that adjudication
rests on something other than aggregating agent opinion. Each item below is a derivation I carried
out myself from the statement in
`docs/derivations/2026-08-15-full-pointwise-meta-agent/construction-or-strongest-theorem.md`.

## Verified: the parent posterior is genuinely a version (statement 1)

The document asserts that \(o\mapsto\boldsymbol\Pi_{A,o,X}=\boldsymbol\Pi_{I,o,X}C_A\) is a selected
parent posterior version, proved "by a bounded-test-function calculation at the observation-kernel
level". I reconstructed it. For bounded measurable \(g\) on \(\mathsf O\) and \(f\) on \(\mathsf Z_A\),
put \(h(Y)=\int f(z)\,C_A(Y,dz)\), which is bounded and measurable because \(C_A\) is a kernel. Then

\[
\int g(o)\!\int\! f\,d\boldsymbol\Pi_{A,o,X}\;\mathbb P^{\mathsf O}_A(do)
=\int g(o)\!\int\! h\,d\boldsymbol\Pi_{I,o,X}\;\mathbb P^{\mathsf O}_I(do)
=\int g(o)h(Y)\,\mathbb P_I(do,dY)
=\int g(o)f(z)\,\mathbb P_A(do,dz),
\]

using preservation of the observation marginal in the first equality and the defining property of the
fine version in the second. So the pushforward of a version is a version **here**. This is the step I
expected to fail, and it does not. It survives because \(C_A\) acts only on the conditioned variable
\(Y\) and leaves \(o\) fixed; the general statement "a pushforward of a conditional law is a
conditional law of the pushforward" is false, but it is not what is being used.

**Verdict: CHECKS OUT.** Any wave-1 finding attacking this step should be treated as refuted unless it
exhibits a failure of one of the two equalities above.

## Verified: parent absolute continuity (statement 1)

\(\mathbb Q_{A,o,X}\ll\boldsymbol\Pi_{A,o,X}\). If \(\boldsymbol\Pi_A(N)=0\) then
\(\int C_A(Y,N)\,\boldsymbol\Pi_I(dY)=0\), so \(C_A(\cdot,N)=0\) \(\boldsymbol\Pi_I\)-a.s.; since
\(\mathbb Q_I\ll\boldsymbol\Pi_I\) the same holds \(\mathbb Q_I\)-a.s., whence
\(\mathbb Q_A(N)=\int C_A(Y,N)\,\mathbb Q_I(dY)=0\). **CHECKS OUT.**

## Verified: the additive KL chain and the defect (statement 4)

Lift both laws to \(\mathsf Y_I\times\mathsf Z_A\) through the *same* \(C_A\):
\(\tilde{\mathbb Q}(dY,dz)=\mathbb Q_{I,o,X}(dY)C_A(Y,dz)\) and
\(\tilde{\boldsymbol\Pi}(dY,dz)=\boldsymbol\Pi_{I,o,X}(dY)C_A(Y,dz)\). Because the second factor is
shared, \(d\tilde{\mathbb Q}/d\tilde{\boldsymbol\Pi}(Y,z)=(d\mathbb Q_I/d\boldsymbol\Pi_I)(Y)\), hence
\(\operatorname{KL}(\tilde{\mathbb Q}\|\tilde{\boldsymbol\Pi})=\operatorname{KL}(\mathbb Q_I\|\boldsymbol\Pi_I)\).
Disintegrating the joint over \(z\) and applying the chain rule for relative entropy gives exactly

\[
\operatorname{KL}(\mathbb Q_I\|\boldsymbol\Pi_I)
=\operatorname{KL}(\mathbb Q_A\|\boldsymbol\Pi_A)
+\int\operatorname{KL}\big(\widehat{\mathbb Q}(\cdot\mid z)\,\big\|\,\widehat{\boldsymbol\Pi}(\cdot\mid z)\big)\,\mathbb Q_A(dz).
\]

Every term is in \([0,+\infty]\) and nothing infinite is subtracted. **CHECKS OUT**, including the
extended-real handling, and the claimed \(\Delta_A\ge0\) is immediate.

The unconditional zero-defect criterion also checks out: \(\Delta_A\) is an integral of a nonnegative
integrand, so it vanishes iff the integrand vanishes \(\mathbb Q_{A,o,X}\)-a.e., and the integrand is a
KL, which vanishes iff the two conditional laws agree. No finiteness is needed for this direction,
and the document correctly says so. The finiteness premise is correctly required only for the
*subtraction* \(\mathcal F_I-\mathcal F_A=\Delta_A\).

## Open concern (mine): novelty of the central identity — NOT a correctness finding

The identity above is the chain rule for relative entropy applied to a joint lift through a common
kernel, with \(\Delta_A\) the expected conditional relative entropy of the discarded coordinates.
That is a textbook decomposition, not a new theorem; the classical discrete form is the relative-entropy
chain rule (Cover & Thomas, *Elements of Information Theory*, Thm 2.5.3), and the general kernel form
is standard. Likewise, statement 4's "zero defect iff a common reverse recovery kernel exists" is, as
far as I can reconstruct it, the equality case of the data-processing inequality — i.e. sufficiency
of the channel in the Blackwell/Csiszár sense, with the recovery kernel as the reverse map.

The mathematics is right. The question the review must answer is what is *new*: the construction
appears to be a careful, correctly-fenced assembly of standard measure-theoretic and
information-theoretic facts in this program's notation, rather than a new theorem. That is a
legitimate and useful thing to have written down, but it is not what "COMPLETE_AFFIRMATIVE,
EVIDENCE_VERIFIED, no unresolved obligations" connotes. Attribution and novelty are the live issues,
not correctness. Wave-1 agents P5, P8, and P9 carry the corresponding scopes; this note records that
I reached the same suspicion independently on the probabilistic side.

**Action for the final report:** the headline should distinguish (a) the mathematics is correct,
(b) the fencing is unusually careful and honest, and (c) the novelty is thin and the certification
language oversells it.

## The recovery theorem (6.9)–(6.12) is the classical equality-in-DPI / sufficiency theorem

Read `evidence/direct-derivation.md:348-379`. The forward direction uses the posterior reverse kernel
supplied by disintegration; the converse assumes finite fine KL plus a normalized \(R\) satisfying
both recovery identities and concludes \(\Delta_A=0\) by data processing through \(C_A\) then \(R\).

That is precisely the classical characterization of **equality in the data-processing inequality**:
for \(\mathbb Q\ll\boldsymbol\Pi\) and a channel \(C\), \(\operatorname{KL}(\mathbb QC\|\boldsymbol\Pi C)
=\operatorname{KL}(\mathbb Q\|\boldsymbol\Pi)<\infty\) holds iff \(C\) is sufficient for the pair, iff
there is a kernel \(R\) with \(\mathbb QCR=\mathbb Q\) and \(\boldsymbol\Pi CR=\boldsymbol\Pi\)
(Csiszár's sufficiency theory for \(f\)-divergences; the quantum analogue is Petz recovery). The
derivation is correct and the finiteness fence is in the right place — the converse genuinely needs it,
since \(\infty=\infty\) carries no information, and the text says exactly that at line 379.

**Verdict: CHECKS OUT, and is classical.** Together with the KL chain, this means the two central
information-theoretic results of the pointwise package are correct restatements of standard theory in
the program's notation. That is worth having; it is not a new theorem, and the surrounding
`COMPLETE_AFFIRMATIVE` apparatus does not distinguish the two.

## Operational-intervention package: my own reconstructions

From `docs/derivations/2026-08-14-operational-intervention-extensions/construction-or-strongest-theorem.md`.

### Item 1 (terminality) — CORRECT, and textbook

\(a\equiv_\Phi b\iff\Phi(uav)=\Phi(ubv)\ \forall u,v\) is the **syntactic congruence**. Everything
asserted about it is classical and I re-derived all of it in a few lines: it lies in \(\ker\Phi\)
(take \(u=v=1\)); it is a congruence; it contains every congruence inside \(\ker\Phi\) (if \(\sim\)
is such and \(a\sim b\) then \(uav\sim ubv\) so \(\Phi\) agrees). Terminality is likewise immediate —
for response-compatible \(q\) with \(\Phi=\psi q\), \(q(a)=q(b)\Rightarrow q(uav)=q(ubv)\Rightarrow
\Phi(uav)=\Phi(ubv)\Rightarrow a\equiv_\Phi b\), so \(\ker q\subseteq{\equiv_\Phi}\), which is exactly
what makes \(h\) well defined; surjectivity and uniqueness follow from surjectivity of \(q\).

This is the syntactic-monoid universal property (Myhill; Nerode; Schützenberger; see Pin,
*Varieties of Formal Languages*, Ch. 2, and Eilenberg, *Automata, Languages and Machines* Vol. B).
The finite-cardinality fence is also correct: \(h\) surjective forces \(|B|\ge|\mathrm{Syn}(\Phi)|\),
and equality forces bijectivity **only** in the finite case, which the document explicitly says.

**Verdict: mathematically correct; novelty is the issue, not correctness.** The document's own
hedging ("Bare-object unique rigidity is never asserted after the quotient map from \(A\) has been
forgotten") is precisely right and is backed by the four-element power-set union monoid witness.

### Item 2 (compact metrizable quotient) — CORRECT, and the countable dense set is load-bearing

I reconstructed this and it survives the two traps I set for the panel.

*Closedness.* \({\equiv_\Phi}=\bigcap_{u,v}\{(a,b):\Phi(uav)=\Phi(ubv)\}\) is an intersection of
preimages of the diagonal of the Hausdorff space \(Y\) under continuous maps, hence closed. A closed
equivalence relation on a compact Hausdorff space has compact Hausdorff quotient with \(\pi\) closed.

*Metrizability.* The full signature \(\sigma(a)=(\Phi(uav))_{u,v\in A}\) lands in \(Y^{A\times A}\),
which need not be metrizable. Restricting to a countable dense \(D\) gives
\(\sigma_D:A\to Y^{D\times D}\), a countable product and so metrizable, and by continuity plus density
\(\sigma_D\) has exactly the same fibers as \(\sigma\). So the countable dense contextual signature is
doing real work — it is what buys metrizability — and is not rhetorical.

*Joint (not merely separate) multiplication continuity.* Because \(A\) is compact Hausdorff and
\(\pi\) is closed, \(\pi\times\pi\) is again a closed continuous surjection and hence a quotient map,
so the continuous map \((a,b)\mapsto\pi(ab)\) descends jointly continuously. This is the place where a
sloppy argument would deliver only separate continuity and land in compact right-topological
semigroup territory; the construction does not make that error.

**Verdict: CHECKS OUT.** This is the most technically substantive result in either package.

### Item 3 (marked-soft face diameters) — CONSISTENT on the arithmetic I can do independently

The stated separation for a strict-interior parent-independent pair is \(|1-2b|(s_+-s_-)\), and on
\([\epsilon,1-\epsilon]^2\) the supremum of \(s_+-s_-\) is \(1-2\epsilon\). So the diameter is
\(|1-2b|(1-2\epsilon)\): for \(b=1/3\) this is \((1-2\epsilon)/3\) and for \(b=1/4\) it is
\((1-2\epsilon)/2\), matching the two stated values. The mechanism is that the diameter depends on the
**downstream** parameter, which is what differs between \(L(1/4,1/3)\) and \(L(1/3,1/4)\).
I have not verified the underlying total-variation computation that produces \(|1-2b|(s_+-s_-)\);
that is P6's assignment.

### Item 6 (circle heat pair) — CORRECT, and it answers the objection I planted

I gave P6 the objection that \(H_sH_t=H_tH_s\) on the circle, so the two chains cannot be
distinguished by their composite. The construction survives it, and the resolution is the substance
of the result: the intervention **cuts at the mediator**, replacing \(K(dE\mid R)\) by a constant
\(\nu\). What then reaches \(O\) is the kernel *downstream* of the cut — \(H_t\) in \(P_1\) and
\(H_s\) in \(P_2\). The composite being symmetric is exactly why the passive laws agree; the
asymmetry lives entirely in which factor survives the cut. Same mechanism as item 3.

I verified the rest in Fourier. On the circle \(H_\tau\) is the multiplier \(e^{-\lambda_n\tau}\).
- Passive equality: both composites are \(H_{s+t}\), so both retained laws are \(m(dR)H_{s+t}(R,dO)\). ✓
- Garbling: \(H_t=H_sH_{t-s}\), so \(H_s\) Blackwell-dominates \(H_t\). ✓
- Strictness: \(H_s=H_tL\) would force multipliers \(e^{\lambda_n(t-s)}\), which are unbounded, so no
  Markov \(L\) exists. ✓
- Soft-set inclusion: \(\nu H_t=(\nu H_{t-s})H_s\), so \(\{\nu H_t\}\subseteq\{\nu H_s\}\). ✓
- Strict inclusion via the stated witness \(\nu_\rho=H_\rho(x_0,\cdot)\), \(0<\rho<t-s\): then
  \(\nu_\rho H_s=H_{\rho+s}(x_0,\cdot)\), and \(\nu H_t=H_{\rho+s}(x_0,\cdot)\) would need
  \(\hat\nu(n)=e^{\lambda_n(t-s-\rho)}\), unbounded, contradicting \(|\hat\nu|\le1\) for a probability
  measure. ✓

**Verdict: CHECKS OUT in full.** This is a clean, genuinely good construction and the strongest
single item across both packages. It should be reported as such.

## CONFIRMED BY MY OWN INSPECTION: the flagship theorem restates this repository's own prior results

Wave-1 investigator P1 reported that the 8/15 derivation restates theorems already `ESTABLISHED` in
this repository. I verified this independently rather than taking it on report, because it is the
finding that most changes the assessment of the work. It holds.

`Theory/06_general_coarsegraining.tex` **at the 8/15 diff base** (i.e. before any of this work),
added by commit `bd46058`, already contains:

**`thm:cg-evidence-preserving-channel`** (`\status{ESTABLISHED}`), verbatim:

> Define \(\bar P(do,dy)=\int K(x,dy)P(do,dx)\), \(\bar P_o:=P_oK\) for every \(o\) […] The declared
> kernel \(o\mapsto\bar P_o\) is a regular conditional law of \(Y\) given \(O\) under \(\bar P\),
> including its selected exceptional-point values. […] Then \(\bar P^O=P^O\).

That is statement 1 of the 8/15 "full pointwise meta-agent" theorem, symbol for symbol, with \(C_A\)
in place of \(K\): the channel pushforward, the pushed posterior being a *version* including its
selected exceptional values, and preservation of the observation marginal. It is also exactly the
identity I reconstructed at the top of this file and marked CHECKS OUT — I was re-deriving the repo's
own week-old theorem, as was the 8/15 package.

**`cor:cg-pairwise-bayes-recovery`** (`\status{ESTABLISHED}`), verbatim:

> Then \(QKR_Q=Q\), and under \eqref{eq:cg-kl-equality}, \(PKR_Q=P\). Conversely, any one kernel \(R\)
> recovering both \(P\) and \(Q\) forces equality in \eqref{eq:cg-kl-dpi}.
> **Proof.** […] The converse follows by applying data processing through \(K\) and then \(R\).

That is the 8/15 (6.9)–(6.12) recovery theorem, including the *same one-line converse argument*
("data processing through \(C_A\) and then through \(R\)", new derivation line 370).

**`cor:cg-dpi-infinite-equality-warning`** (`\status{ESTABLISHED}`) is the new line 379
("\(+\infty=+\infty\) supplies neither (6.8) nor (6.12)"), and the prior version proves it with an
exhibited three-point counterexample.

**`thm:cg-kl-dpi-extended`** (`\status{ESTABLISHED}`) is the extended-real DPI, proved with the same
nonnegative generator \(\phi_0(t)=t\log t-t+1\) that reappears at line 286 of the new derivation — and
it carries `\citet{Kullback1951,Csiszar1967}`, the attribution the new package does not repeat.

**Assessment.** The measure-theoretic and information-theoretic core of the 8/15 flagship release is a
re-derivation of four results this repository already had marked `ESTABLISHED` a week earlier, shipped
as a new hash-bound `COMPLETE_AFFIRMATIVE` release with no citation to the prior internal results and
without the Kullback/Csiszár attribution the prior version carried. My earlier note that these results
are "classical, not new" understated it: they are not merely classical, they are *already in this
repo*, with proofs, with correct citations.

This does **not** make the 8/15 work empty. What is genuinely added is the typed parent
belief/model/evaluator/holonomy decoration, the pointwise \(r_*\)/\(X\)/admitted-\(o\) framing, and the
five finite witnesses. But those are the parts the panel found weakest (see P3 on the witnesses and P4
on "holonomy"), and the strongest-looking parts of the release are the borrowed ones.

**Severity: High**, and it is an *attribution and process* defect, not a correctness defect. The
mathematics is right. What failed is the certification apparatus: a process that runs sixteen
adversarial attacks, an oracle-erasure pass, an independent reconstruction, and four expert reviews,
and does not notice that the theorem was already proved in the same repository, is not measuring what
its `EVIDENCE_VERIFIED` label claims to measure.

## Note on the certification language

`final-report.md` states "Unresolved obligations: None within the frozen target and its transitive
dependency closure." That sentence is true and nearly contentless: the contract was frozen to a scope
the derivation could close, and the same agent chose the scope, wrote the proof, attacked it, reviewed
it four ways, and adjudicated it. The list of things explicitly NOT established (§"Scope and
limitations") is long and is where the actual research state lives. The certification apparatus should
be read as bookkeeping, not as evidence.
