# ELBO → continuum action: live worklog

**Date:** 2026-08-12
**Branch:** `codex/elbo-effective-action-derivation`
**Worktree:** `C:/tmp/MultiAgentELBO-elbo-action-019ff75d`
**Status:** IN PROGRESS — durable record kept against session/rate-limit loss.

**Research question.** Can the effective lattice/continuum PIFB2 action be *derived* from the exact
multi-agent ELBO theory, rather than postulated? And what precisely is the compatible theory
relating PIFB2's engineered action to the exact ELBO?

---

## 0. Inherited state (three completed rigorous-theory-search runs)

| Run | Location | Terminal status | What it established |
|---|---|---|---|
| Exact two-channel finite ELBO | `docs/derivations/2026-08-12-exact-two-channel-finite-elbo/` | **COMPLETE_AFFIRMATIVE** | Tied-replica normalized joint whose exact negative ELBO equals the lagged unit-temperature two-channel PIFB2 scalar plus \(\sum_a I_{\zeta_a}(K_a;M_a)\) |
| ELBO → effective section action | `docs/derivations/2026-08-12-elbo-to-effective-section-action/` | INCONCLUSIVE | Exact finite-lattice KL contraction; \(S_h^{\rm exact}=S_h^{\rm PIFB}+\varepsilon_h+c_h\); residual uncontrolled |
| ELBO–PIFB2 fast/slow program | `docs/derivations/2026-08-12-elbo-pifb2-fast-slow-program/` | INCONCLUSIVE | Lagged transported-peer KL identity, exact fast-state profiling identity, compact-subgroup reduction |

### The closed theorem (do not re-derive)

For a finite agent-site set \(A\), conditional on history \(H_n\), with private block
\((K_a,M_a)\sim p_a\otimes r_a\) and likelihood \(L_a(do\mid k,m)\); belief label-copy block
\((J_a^q,X_a)\) with law \(\pi^q_{aj}u^n_{aj}\), \(u^n_{ab}=(\Omega^n_{ab})_\#q^n_b\); model
label-copy block \((J_a^s,Y_a)\) with law \(\pi^s_{a\ell}v^n_{a\ell}\),
\(v^n_{ab}=(\widetilde\Omega^n_{ab})_\#s^n_b\); and tied recognition
\(Q_a^{n+1}=\zeta_a(dk,dm)\,\beta_{aj}q_a(dx)\,\gamma_{a\ell}s_a(dy)\):

$$
\mathcal F_h^{n+1}=\sum_{a\in A}\Big[
D_{\rm KL}(q_a\|p_a)+D_{\rm KL}(s_a\|r_a)+I_{\zeta_a}(K_a;M_a)
-\mathbb E_{\zeta_a}\log\ell_a(o_a\mid K_a,M_a)
$$
$$
+D_{\rm KL}(\beta_a\|\pi_a^q)+\sum_b\beta_{ab}D_{\rm KL}(q_a\|u^n_{ab})
+D_{\rm KL}(\gamma_a\|\pi_a^s)+\sum_b\gamma_{ab}D_{\rm KL}(s_a\|v^n_{ab})\Big]
$$
$$
=\;\mathcal F_{\rm PIFB2,h}^{\rm lag,1}+\sum_{a\in A}I_{\zeta_a}(K_a;M_a).
$$

Under \(\zeta_a=q_a\otimes s_a\) the correction vanishes and equality is **exact**.

**Typing (settled).** \(q_i\) = fast recognition density over hidden states \(k_i\);
\(s_i\) = slow generative-model section, realized as a law over model parameters \(m_i\);
\(L_i(do\mid k,m)\) = normalized likelihood kernel. Predictive model
\(\overline L_i(do\mid k)=\int L_i(do\mid k,m)s_i(dm)\).

**Open on entry.** Same-time reciprocal coupling; \(\tau\neq1\); non-unit/adaptive coefficients;
base-gradient and curvature sectors (absent from the finite probability theorem);
lattice → continuum limit.

---

## 1. Structural observations driving this session

1. **\(S_h^{\rm exact}=S_h^{\rm PIFB}+\varepsilon_h+c_h\) is currently a tautology.** \(\varepsilon_h\)
   is *defined* as the difference. It becomes a scientific statement only once the microscopic law
   is specified. The natural specification is the tied-replica joint that is already proved
   normalized — i.e. **feed run #3 into run #2**. This connection had not been made.
2. **The gradient sector should be derivable, not postulated**, because the Fisher metric *is* the
   Hessian of KL. See §2 — verified.
3. **Curvature may likewise be derivable**, via loop-holonomy KL, and if so it comes out
   *Fisher-weighted* rather than Frobenius — which would resolve the standing conjugation-invariance
   obstruction to a noncompact \(GL(K)\) theory.

---

## 2. VERIFIED RESULT — second/third-order KL expansion and stencil cancellation

**Reproduce:** `docs/verification/kl_expansion_check.py` (this run's script; exact symbolic
computation, three exponential families: Poisson, Bernoulli, Exponential).

For a regular exponential family \(q_\theta(x)=\exp(\theta T(x)-A(\theta))\), with Fisher metric
\(g^F=A''(\theta)\) and Amari–Chentsov skewness tensor \(T_{\rm skew}=A'''(\theta)\):

$$
D_{\rm KL}(q_{\theta+h}\|q_\theta)=\tfrac12 g^F h^2+\tfrac13 T_{\rm skew}h^3+O(h^4)
$$
$$
D_{\rm KL}(q_\theta\|q_{\theta+h})=\tfrac12 g^F h^2+\tfrac16 T_{\rm skew}h^3+O(h^4)
$$

**Status:** DERIVATION, confirmed symbolically in three families with agreeing coefficients.

Consequences:

- **(C1) Argument order is invisible at second order, visible at third.** The two orders share the
  Fisher term exactly and differ by \(\tfrac16 T_{\rm skew}h^3\). KL asymmetry therefore does not
  corrupt the metric that emerges.
- **(C2) The \(h^3\) term is odd in \(h\) and cancels on a symmetric nearest-neighbour stencil.**
  Summing \(+h\) and \(-h\) neighbours of the same site gives \(g^F h^2+O(h^4)\), in *both*
  argument orders. Verified concretely (Gaussian scale family, exact closed form: pair sum has
  \(h^3\) coefficient exactly \(0\)).
- **(C3) Therefore the weight \(h^{d-2}\) is forced, not chosen.** With \(\sim h^{-d}\) sites and a
  symmetric stencil,
  $$\sum_{\langle c,c'\rangle}h^{d-2}D_{\rm KL}\big(q(c)\,\|\,q(c')\big)\;\longrightarrow\;\tfrac12\int_{\mathcal C}\|\nabla q\|^2_{g^F}\,dc$$
  with **no** surviving Amari–Chentsov correction and relative error \(O(h^2)\).

**Caveat not covered by this check (delegated to the T-GRAD agent).** With a nontrivial connection
the two neighbours are compared through *different* transports \(\Omega_{c,c+h}\) vs
\(\Omega_{c,c-h}\). The transport contributes its own \(O(h)\) piece, so the odd/even cancellation
is **not automatic** in the covariant setting and must be redone there. Until that is closed, (C3)
holds for the flat/trivial-transport case only.

---

## 3. Deployed investigation (14 agents, workflow `wf_f576312d-d2a`)

Script: `.claude/.../workflows/scripts/elbo-to-pifb2-continuum-action-wf_f576312d-d2a.js`

Structure: 3 grounding extractors → 5 theorem attempts (effort max) → 1 dedicated adversarial
skeptic per attempt (effort max) → 1 synthesis.

| Key | Target | Question |
|---|---|---|
| `fisher-gradient` | **T-GRAD** | Base-neighbour transported KL → covariant Fisher Dirichlet \(\|D^Aq\|^2_{g^F}\). Must settle: the covariant \(O(h^3)\) cancellation; where \(D^A\) comes from (pushforward, *not* matrix action on a density); Riemann-sum convergence for \(C^2\) vs \(H^1\); and whether the recognition weight \(\beta\) must be frozen to \(\pi\) (which would make the sector postulated, not derived) |
| `curvature` | **T-CURV** | Plaquette holonomy KL \(D_{\rm KL}(q\|(H_P)_\#q)\to\tfrac12h^4\|F_{\mu\nu}\!\cdot\!q\|^2_{g^F}\). Decisive sub-questions: is \(\|F\!\cdot\!q\|^2_{g^F}\) conjugation-invariant (→ noncompact \(GL(K)\) becomes admissible); is the isotropy-algebra degeneracy fatal to coercivity; and does the loop term require a genuinely self-referential source (→ same-time obstruction reappears and curvature is *not* ELBO-derivable this way) |
| `residual-closure` | **T-RESID** | Take the tied-replica joint as *the* microscopic law; compute \((C_h)_\#P_h(\cdot\mid o)\) in closed form; determine whether \(\varepsilon_h=0\) or exhibit the leading generated operator. Marginalizing the replica blocks makes a mixture, and \(-\log\) of a mixture generates the higher-body/nonlocal terms — first two cumulants required |
| `coefficients` | **T-COEF** | Which of \(\tau\neq1\), \(\lambda_s\), \(\alpha_i(c)\) arise from *normalized* models. Routes: replication (\(\tau=1/n\) only), tempering (must retain \(\log Z\) — is it \(\beta\)-dependent?), latent precision variable. Verdict table: coefficient → construction → extra term it forces |
| `same-time` | **T-SIMUL** | Scope the standing obstruction; prove fixed-point value agreement and test gradient agreement; test integrability of the same-time field (Jacobian symmetry); and — highest value — whether lagged vs same-time differ by \(O(dt)\) so same-time PIFB2 is the \(dt\to0\) limit of an exactly-ELBO-derived scheme |

Skeptic mandate (all five): hidden hypotheses, order-of-limits swaps, KL asymmetry at third order,
dropped log-normalizers, state-vs-configuration level confusion, tautology, scope inflation, and an
explicit two-agent / two-site counterexample attempt.

---

## 3b. PRIOR ART DISCOVERED MID-SESSION — read before accepting any §4 result

**Location:** `C:/Users/chris and christine/Documents/ChatGPT/MultiAgentELBO/docs/audits/roadmap-review-2026-08-12/`
(six referee reports `rm-01` … `rm-06`), plus a fourth derivation run
`docs/derivations/2026-08-12-pifb2-elbo-program-decision/` (terminal_status `null`, bounded checkpoint).

**These were NOT visible to the §3 agents** — they live in the `Documents/ChatGPT` copy, and the
agents were pointed at the tmp worktree. Every §4 result must therefore be reconciled against
this section before any novelty claim is made.

### 3b.1 Findings that pre-empt or correct this session's framing

| # | Finding | Source | Effect on §3 targets |
|---|---|---|---|
| **PA-1** | **"Fisher-dressed curvature" is already identified as the repair** for the \(GL(K)\) curvature problem. | `rm-03-action-class.md:0` (verdict §0 item 1) | **T-CURV is not novel as an idea.** Only the *ELBO-derivation route* (holonomy KL) may be new. Do not claim the construction. |
| **PA-2** | \(\kappa\|F_A\|^2\) **cannot** be both gauge-invariant and nonnegative for \(G=GL(K,\mathbb R)\). Ad-invariant symmetric bilinear forms on \(\mathfrak{gl}(K,\mathbb R)\) form exactly a 2-dim space (\(\mathrm{tr}(XY)\), \(\mathrm{tr}X\,\mathrm{tr}Y\)); **every** element is indefinite — signature \((3,1)\) for \(K=2\), \((6,3)\) for \(K=3\). Exhaustive search. | `rm-04-gauge-kinematics.md` §0(4), §1.5 | Confirms the motivation for T-CURV, and makes compact type a **kinematic** necessity belonging in T0, not an analytical convenience. |
| **PA-3** | **Lemma (gauge-invariant confinement).** If some fiber gauge orbit is **noncompact**, no \(\rho(G)\)-invariant \(V\) has compact sublevel sets — it is constant on that orbit. Hence **no gauge-invariant coercive confinement exists**. If \(G\) is compact, Haar-averaging any coercive \(W\) gives one. | `rm-02-existence-analysis.md` §3.3, finding **T-3** | **Corrects this session's framing.** Invariance does **not** rescue noncompact \(GL(K)\): invariance and coercivity are in *tension*, not alliance. A Fisher-dressed curvature term fixes the *invariance/positivity* defect but supplies **no coercivity** along noncompact orbits. Anchoring at a fiber point is a **Higgs potential** breaking \(G\to G_{m_0}\). |
| **PA-4** | **Fisher is the Hessian of the divergence**, hence any map preserving \(D_q\) automatically preserves \(g^F_q\); so invariance of the self+peer sectors alone already forces \(\rho(G)\subseteq\mathrm{Isom}(\mathcal M,g^F)\). | `rm-04` §0(3), Lemma 1.3 | The base fact underlying §2 is **already in the corpus**. §2's genuine increment is only the *third-order coefficients* \((1/3\) vs \(1/6)\) and the *stencil cancellation*. Claim no more than that. |
| **PA-5** | For the **categorical** fiber the Fisher–Rao isometry group is \(S_{n+1}\), **finite**. No positive-dimensional Lie group acts on a categorical fiber by Fisher–Rao isometries; any connected \(G\) acts trivially. | `rm-04` §0(2), §1.1a | **FATAL** for the "two nonisomorphic families instantiate the hypotheses" gate with one fixed positive-dimensional \(G\). Constrains every multi-family plan. |
| **PA-6** | For Gaussian fibers, \(GL(K)\) acting by pushforward congruence \((\mu,\Sigma)\mapsto(A\mu,A\Sigma A^\top)\) **is** a Fisher–Rao isometry (verified to \(7.6\times10^{-15}\)), and for \(K\ge2\) the affine group is the **entire identity component** of the isometry group. \(GL(K)\) is the maximal choice, not an arbitrary one. | `rm-04` §0(1), §1.1b; corpus at `Theory/05c_pullback_geometry.tex:59` | Supports keeping \(GL(K)\) as the ontology while using compact \(G\) for the analysis. |
| **PA-7** | **The Gaussian fiber fails the coercivity hypothesis.** \(g^F_{\mu\mu}=\Sigma^{-1}\to0\), so bounded action gives no \(L^2\) bound on \(\nabla\mu\); KL grows only like \(\log\det\Sigma\); and KL is coercive only in the **difference** of its arguments — \(\mu_1=\mu_2\to\infty,\ \Sigma_1=\Sigma_2\to\infty\) costs **zero**. | `rm-02` §3.2, finding **T-2** | Any continuum existence claim on Gaussian fibers needs an amended action. |
| **PA-8** | After row elimination the peer sector is a soft-**min**, \(\Phi_\tau(D)\le\min_j(D_{ij}+\tau\log(1/\pi_{ij}))\); with a diagonal entry it is **uniformly bounded** — zero coercivity, no consensus pressure. | `rm-02` §4.1, **D-5** | Directly relevant to T-COEF and to what \(\tau\) means physically. |
| **PA-9** | Curvature of the showcase fibers, computed exactly: categorical \(\equiv+1/4\) (isometric to the positive orthant of \(S^{n-1}(2)\)); univariate Gaussian \(\equiv-1/2\); **multivariate Gaussian mixed-sign**, \(+1/4\) on every pure-mean plane at every point, \([-1,0]\) on pure-covariance planes, \(\sup K=2/7\) for \(n=2\). Not NPC, not a space form. | `rm-02` §2, App. A | Kills a single T6 (Eells–Sampson needs \(\mathrm{Riem}\le0\), covers only the univariate Gaussian). Does **not** threaten existence — the direct method is curvature-blind. |
| **PA-10** | Much of the continuum existence programme is **classical, not new**: Morrey (1948) for existence (curvature-blind), Schoen–Uhlenbeck for partial regularity, HKW for regular-ball full regularity, Wood for harmonic sections, Grohs–Hardering–Sander for manifold-valued FE convergence. Both showcase fibers are **contractible**, so Bethuel density and Sacks–Uhlenbeck bubbling do not fire. | `rm-02` §1.1, §5.2; `rm-06` §0(2) | "T4 is essentially a citation, not a theorem" with fixed smooth \(A\) and compact target. Claiming it as new invites a hostile referee. |
| **PA-11** | The sigma-flow literature (Cassel–Boll–Petra–Albers–Schnörr, arXiv:2408.15946, JMIV 2025) has the Dirichlet sector as its **entire model** — harmonic map from a compact base into the Fisher–Rao simplex — with **no bundle, no gauge group, no connection, and explicitly no existence theorem**. | `rm-06` §1 | Nearest prior art; T4 in the bundle setting is genuinely nobody's theorem yet. |
| **PA-12** | **T0 was already published by the author in 2025 and is uncited** — Preprints.org `202505.1773.v1` contains the principal \(G\)-bundle, two associated bundles, agent as a pair of local sections, induced connection, KL-term variational energy, Fisher metric on fibers, and a Yang–Mills field. | `rm-06` §0(3) | WP0 is editing, not new work. |
| **PA-13** | \(T9\) (configuration-space Gibbs) is **ill-typed for \(d\ge2\)**: any reference measure making \(\int\|D^Aq\|^2\) the quadratic form is a GFF, which a.s. lives in \(H^{1-d/2-\epsilon}\) and is not function-valued for \(d\ge2\); the \(\mathcal S\)-finite configurations are a **null set**. Also \(Z=\infty\) at finite mesh for noncompact \(G\). | `rm-02` §8, **T-5** | Bounds how far any "exact continuum Gibbs VFE" claim can go. |

### 3b.2 Consequence for this session

The §3 panel is running **without** PA-1…PA-13. Expect rediscovery and false novelty claims,
particularly on T-CURV (PA-1) and on any coercivity optimism (PA-3). A **reconciliation pass**
against `rm-01`…`rm-06` is mandatory before anything from §4 is written into `Theory/`.

### 3b.3 Repository fragmentation — a merge problem before it is a science problem

`rm-01` §0 already flagged this and it has since got worse. Four locations, none complete:

| Location | Has | Missing |
|---|---|---|
| `Desktop/MultiAgentELBO` | `Theory/`, PIFB2 copy, ultradeep audit waves 1–2 (untracked), continuum roadmap + review | the four derivation runs; `rm-01`…`rm-06` |
| `Documents/ChatGPT/MultiAgentELBO` (`main` @ `e1f8795`) | four derivation runs, `rm-01`…`rm-06` | ultradeep audit waves 1–2 |
| `C:/tmp/MultiAgentELBO-elbo-action-019ff75d` (`codex/elbo-effective-action-derivation`) | three derivation runs, this worklog | `rm-01`…`rm-06`, ultradeep waves, program-decision run |
| `Desktop/Research` | live `PIFB2.tex`, wiki, `magent_elbo_whitepaper` | everything above |

`rm-01` also records that the continuum roadmap was authored in a copy where **neither audit wave
existed on disk**, and that `build_pifb2_roadmap_ledger.py:13-17` hard-codes absolute paths to
`Desktop/Research/manuscripts/PIFB2.tex` and `Desktop/MAgent_Model-main/README.md`, binding the
ledger to a source set containing **zero** references to `Theory/`. Consolidation should precede
further theory expansion.

---

## 3c. RECONCILIATION OF T-GRAD WITH OBSTRUCTION O2 / THEOREM A4.4

Derived in-session by reading, not by the §3 panel. This is the most consequential result so far
because O2 appeared to kill T-GRAD outright, and on precise reading it does not — it *characterizes*
it.

### 3c.1 The apparent obstruction

`docs/audits/ultradeep-wave2-2026-08-12/wave2-01-constructions.md:488` — **O2, CRITICAL**:

> Finite-design consistency forces the connection out of the free energy. […] Any future attempt to
> put \(\omega\) into \(\mathcal F\) must break one of: the finite design (`03:15`),
> `hyp:gen-design-product` (`04:96`), or the \(L^2\) standing tier
> (`hyp:hist-standing-configuration-tier`, `05d:355`).

**Theorem A4.4(a)** (`wave2-01-constructions.md:385`), exact hypotheses: let
\(\mathcal F_\mu[s]=\int f(c,s(c),D^\omega s(c))\,d\mu\) with \(\operatorname{supp}\mu\subseteq D\),
and *require* \(\mathcal F_\mu[s]=\mathcal F[Q_X;X,o]\) for every admissible related pair. If the
section class contains two sections agreeing at every design point but with different
\(D^\omega s(c_a)\), then \(f(c_a,\cdot,\cdot)\) does not depend on its jet argument and \(\omega\)
is provably absent. The deformation is elementary (\(D=\{0,2,4\}\), \(\chi=(c)(c-2)(c-4)\),
\(\chi|_D=0\), \(\chi'|_D=(8,-4,8)\)), so case (a) is **generic**.

### 3c.2 Why T-GRAD escapes at finite \(h\) — the functional is two-point, not jet

A4.4's hypothesis is that \(\mathcal F_\mu\) has the **local** form: a single integral of a pointwise
density in \((\text{value},\text{jet})\). The base-neighbour source-label block does not produce
such an object. It produces

$$
\mathcal F^{\rm base}_h=\sum_{\langle c,c'\rangle\subset\Lambda_h}\beta_{cc'}\,
D_{\rm KL}\!\big(q(c)\,\big\|\,(\Omega^A_{c,c'})_\#q(c')\big)
\;+\;\sum_c D_{\rm KL}(\beta_c\|\pi_c),
$$

which is a **two-point (finite-difference) functional of section values at two design points**. It
is not a function of any jet. A4.4 therefore **does not apply to it**, and the term is an exact ELBO
component at every fixed \(h>0\) by the same tied-replica mechanism already proved normalized.

**What T-GRAD does break is exactly one of O2's three named escapes: `hyp:gen-design-product`.**
Verbatim (`Theory/04_generative.tex:89-97`, `\status{HYPOTHESIS}`):

> Distinct design points are conditionally independent given \(X\):
> \(P_\theta(do,dY\mid X)=\bigotimes_{a=1}^{M}P_{\theta,a}(do_a,dY_a\mid X)\).
> This modeling hypothesis **excludes residual cross-design dependence**.

A base-neighbour block is precisely residual cross-design dependence. It is the *mildest* of O2's
three escapes and the only one already tagged `HYPOTHESIS` rather than `ESTABLISHED` — it is a
declared modelling choice, not a theorem, and it is stated in the manuscript as excluding exactly
the thing the gradient sector needs.

### 3c.3 The resulting statement, and where A4.4 does bite

> **Proposition (session result, DERIVATION + APPLICABLE_THEOREM A4.4).**
> At every fixed finite lattice \(\Lambda_h\) (itself a finite design), the base-neighbour
> transported-KL sector is an **exact** negative-ELBO component of a normalized generative law that
> couples neighbouring design points; such a law exists iff `hyp:gen-design-product` is relaxed.
> Its \(h\to0\) limit, when it exists, is a **jet** functional and therefore — by Theorem A4.4(a),
> whose hypotheses now hold — is **not** the ELBO of any finite design.

So the layered picture is not merely defensible, it is **forced**:

| Object | Status |
|---|---|
| Exact ELBO at finite \(\Lambda_h\), cross-design coupling allowed | **EXACT** (tied-replica + base-neighbour block) |
| \(h\to0\) limit \(=\tfrac12\int\|D^Aq\|^2_{g^F}\) | limit of exact ELBOs; **not itself a finite-design ELBO** |
| Identification of the limit with a finite-design ELBO | **REFUTED** by A4.4(a) |

Theorem A4.5 (`wave2-01:406`) sharpens the last row: if \(\mu\) charges \(\mathcal C\setminus D\),
then \(\mathcal F_\mu\) can at best be an **extension** of the finite-design ELBO and the extension
is **not determined** — every \(\mu\) agreeing on \(D\) gives one. Along a *refining* family
\(\Lambda_h\downarrow\) the limit is pinned by the sequence, which is the only sense in which the
continuum object is determined. This localizes `open:prob-continuum-theory` (`03:443`) exactly.

### 3c.4 Ontological payoff — stated correctly

**Retracted phrasing.** An earlier draft of this section said "spatial propagation in the base".
That is a category error. \(\mathcal C\) is a *context* manifold, explicitly **not** space:
`Theory/02_geometry.tex:20-33` declares it is not the population index set, not the interaction
graph, and not spacetime; PIFB2 calls it the "domain of inquiry, not a thing".

**What a base derivative actually means.** An agent is a section \(q_i:\mathcal C_i\to\mathcal E_b\),
so \(q_i(c)\) is agent \(i\)'s belief **in context \(c\)**. Then \(D^Aq_i\) is the covariant rate at
which that belief changes as the *context* varies, and

$$\eta_q\int_{\mathcal C}\|D^Aq_i\|^2_{g^F}\,d\mu$$

is a **contextual-coherence (generalization) prior**: nearby contexts must carry nearby beliefs. It
is the information-geometric analogue of a Gaussian-process / RKHS smoothness prior, not a
transport of signals through space.

**It is a self term, not an interaction term.** Peer coupling in PIFB2 is *pointwise* in \(c\):
\(\beta_{ij}(c)D_{\rm KL}(q_i(c)\|\Omega_{ij}(c)_\#q_j(c))\) at a shared context, on the overlap
\(U_i\cap U_j\). Base derivatives couple agent \(i\) to **itself** at neighbouring contexts. These
are structurally different couplings and must not be conflated.

**The correct restatement.** The Dirichlet sector is the ELBO signature of relaxed conditional
independence *across contexts*; it vanishes identically iff `hyp:gen-design-product` holds. So
\(\eta_q\) is **the strength of admitted cross-context dependence in the generative model**, not a
free regularization weight, and roadmap experiment **E4** tests a probabilistic hypothesis rather
than a postulated term.

### 3c.5 The idle-wheel consequence — why this is load-bearing

`Theory/12_philosophy.tex:77` adopts an explicit **idle-wheel criterion**: *a posit with no trace in
any declared observable is removed by parsimony.*

Observe: with **no** base-derivative and no otherwise-nonlocal-in-\(\mathcal C\) term, the entire
action is a sum of independent pointwise problems indexed by \(c\). The theory factorizes over
\(\mathcal C\) completely; \(\mathcal C\) could be replaced by an arbitrary index set carrying a
measure and nothing whatsoever changes. **The smooth manifold structure of \(\mathcal C\) is then
idle in exactly the sense that chapter uses to license removal.**

Combining with §3c.2:

> **The base-derivative sector is precisely what saves \(\mathcal C\) from being an idle wheel, and
> that sector exists iff `hyp:gen-design-product` is relaxed. Hence \(\mathcal C\) earns its
> manifold structure iff the generative model admits cross-context dependence.**

This also names the propagation mechanism correctly. Information does move from \((i,c)\) to
\((j,c')\), but by a chain — \((i,c)\xrightarrow{\text{contextual coherence}}(i,c')
\xrightarrow{\text{pointwise overlap}}(j,c')\) — i.e. **inferential propagation across contexts**,
never spatial propagation.

### 3c.6 The base-measure problem, and an untried candidate

`Theory/05c_pullback_geometry.tex:1362-1366`, `\status{NOT-CLAIMED}`, verbatim:

> A scalar gauged sigma energy would additionally require a base cometric, a base density, channel
> weights, boundary conditions, and a decision about whether the connection is fixed or dynamical.
> None is selected by \(h_s^\omega\) or \(c_s^\omega\).

and obstruction **O3** adds that declaring a positive finite \(\mu\) normalizes to a probability law
on \(\mathcal C\), which `12_philosophy.tex:33-38` explicitly disclaims. So the Dirichlet form
\(\int\|D^Aq\|^2_{g^F}d\mu\) needs two exogenous objects the ontology refuses to supply.

**Candidate that needs neither — the induced-volume action.** `05c` already constructs the
informational pullback \(h^\omega_s=\sigma^*g^F\), i.e.
\(h_{\mu\nu}=g^F(D^A_\mu q,D^A_\nu q)\). Its own determinant supplies a volume form:

$$
\mathcal S_{\rm vol}[q]=\int_{\mathcal C}\sqrt{\det\big(g^F(D^A_\mu q,\,D^A_\nu q)\big)}\;d^dc .
$$

This is diffeomorphism-invariant on \(\mathcal C\), requires **no** base cometric and **no** base
density, and is literally "It From Bit": the base's volume element is manufactured by the
information geometry rather than declared. It is the Nambu–Goto / minimal-surface analogue of the
Dirichlet (Polyakov) form.

**Status: CONJECTURE / direction, not a result.** Honest caveats:
- **Absent from the corpus.** Searched `Theory/*.tex` for `sqrt{\det}`, `volume form`, `induced
  volume`, `Nambu`, `minimal surface`, `densitized` — no hits. (PIFB2 does use \(\sqrt{|g|}\), but
  see §3c.7 — that is an *intrinsic* base metric, the opposite move.)
- **It is not the \(h\to0\) limit of the lattice KL sum.** That limit gives the Dirichlet/Polyakov
  form with exogenous \(\mu\). Nambu–Goto is a *different* functional, classically equivalent to
  Polyakov only after integrating out an auxiliary worldvolume metric. **No ELBO derivation of
  \(\mathcal S_{\rm vol}\) is claimed or currently in sight.**
- **Degenerate on the rank-drop locus.** \(\det h=0\) wherever the pullback loses rank. `05c:318`
  (`thm:pb-pullback-rank-quotient`) already supplies the constant-rank/radical/quotient machinery
  this would need, including an explicit constant-rank-one witness at `05c:431`.

### 3c.7 A direct PIFB2 ↔ Theory incompatibility on exactly this point

`PIFB2.tex:1731` (verbatim): "every per-scale free-energy term is integrated against the volume form
\(\sqrt{|g|}(c)\,dc\), with the base volume form read once and threaded to every scale, so that a
flat base reduces \(\sqrt{|g|}\) to unity".

**PIFB2 therefore assumes an intrinsic base metric \(g\) on \(\mathcal C\)** — and a default flat
one. `Theory/` refuses exactly this: no canonical metric, connection, or measure on \(\mathcal C\)
(N1; `appendix_claim_ledger.tex` "No canonical connection is selected anywhere in this manuscript";
`12_philosophy.tex:33-38` "No expectation over contexts is used").

This is a **structural incompatibility between the two documents**, not a notational one, and it
sits precisely on the question of what \(\mathcal C\) is. Any unified theory must pick one of:
(i) declare an intrinsic base geometry and drop N1; (ii) keep N1 and use a section-induced volume
(§3c.6); or (iii) keep N1 and accept that the theory is ultralocal in \(\mathcal C\), with the
manifold structure idle (§3c.5). **PIFB2 currently takes (i) implicitly and without argument.**

### 3c.8 Curves in \(\mathcal C\) — already developed, and unused by PIFB2

`Theory/05d_relational_inference.tex` and `05c` contain substantial machinery for curves in the base
that PIFB2 has not drawn on: the vertical/horizontal/section curve taxonomy
(`prop:pb-curve-taxonomy`, `05c:621`), vertical Fisher length (`05c:589`), Fisher duration on a
selected history (`05d:573`), the obstruction to a global unit-speed clock (`05d:771`), and record
clocks with exact Markov loss (`05d:844`). Two standing warnings apply to any use of them:
`05c:1368` — vertical Fisher length "does not generate an orbit, identify a physical time
coordinate, or compare independently evolved fine and coarse paths"; and `05d:658` — a base probe
along an ordering "is not an agent inference history".

**Caveat carried forward.** This does not yet establish the limit exists. §2 proves the
scalar/flat-transport case; the covariant \(O(h^3)\) cancellation with \(\Omega^A_{c,c+h}\ne
\Omega^A_{c,c-h}\) remains the open half (T-GRAD item 2/3). And PA-3 still applies: none of this
supplies coercivity for noncompact \(G\).

---

## 3d. CURVE-MEDIATED INTER-AGENT TRANSPORT — the route that unblocks operational holonomy

Raised by the PI. Recorded here because it appears to defeat the standing negative result, and it
does so by changing precisely the hypothesis that negative result names as load-bearing.

### 3d.1 The construction

Agents \(i,j\) are sections over \(U_i,U_j\subseteq\mathcal C\). PIFB2 currently couples them only on
the **pointwise overlap**, comparing \(q_i(c)\) with \((\Omega_{ij}(c))_\#q_j(c)\) at a shared \(c\).
Proposed generalization: for a curve \(\gamma\) in \(\mathcal C\) from \(c_j\in U_j\) to
\(c_i\in U_i\), with \(\mathrm P_\gamma\) the parallel transport of the connection \(A\) along
\(\gamma\), couple

$$
D_{\rm KL}\big(q_i(c_i)\;\big\|\;(\mathrm P_\gamma)_\#\,q_j(c_j)\big).
$$

This requires **no overlap at all** — agents with disjoint domains can interact, mediated by a path.

### 3d.2 It unifies three couplings that currently look unrelated

| \((\text{agent pair},\ \gamma)\) | Recovered object |
|---|---|
| \(i\ne j\), \(\gamma\) constant (\(c_i=c_j\)) | PIFB2's present pointwise overlap coupling |
| \(i=j\), \(\gamma\) infinitesimal (one lattice edge) | the base-neighbour block of §3c \(\Rightarrow\) Dirichlet sector |
| \(i\ne j\), \(\gamma\) of finite length | the new nonlocal relational coupling |

All three are one expression at different parameters. The Dirichlet sector and the peer sector stop
being separate postulates and become the short- and long-curve limits of a single interaction.

### 3d.3 It makes \(\Omega_{ij}\) derived rather than posited

The standing criticism of \(\Omega_{ij}=e^{\phi_i}e^{-\phi_j}\) is that it is a **flat coboundary** —
pure gauge bookkeeping that "cannot generate nontrivial cycle holonomy by itself"
(continuum roadmap line 66, credited by the referee synthesis as independently repairing the one
genuine category error in PIFB2). Setting \(\Omega_{ij}:=\mathrm P_\gamma(A)\) instead:
- derives the transport from the connection rather than declaring it;
- gives the cocycle property automatically under concatenation of curves;
- generates nontrivial holonomy **iff** \(A\) has curvature.

This is exactly the first of the two repairs the roadmap itself names ("a connection \(A\) whose
parallel transport compares separated base points, or an independent overlap/link automorphism").

### 3d.4 Why this defeats the finite-design no-go — the decisive point

`wave2-01-constructions.md:695-713` (**B4**) states the standing negative result:

> Any future claim that some observation-record statistic detects holonomy, curvature, or bundle
> topology is refuted in advance for finite designs, by (F2) and (F4). This partially **closes in the
> negative** the ledger's "Operational base holonomy (open)" entry […] the requested tuple […]
> **cannot exist for any finite design, because the connection is not an argument of any generative
> kernel.**

and (F2), `wave2-01:662-667`:

> \(\omega_b,\omega_m\) are not arguments of any factor of `eq:gen-kernels`, so
> \(\Lambda(P,\omega,s,\theta)=\Lambda(P,\omega',s,\theta)\) for **all** pairs of connections […]
> Holonomy conjugacy classes are therefore invisible to \(\Lambda\) for a trivial reason.

And critically, `wave2-01:709-711` states its own defeat condition:

> The reasons it holds are two features of the declared model, not two discoveries: **the connection
> is not an argument of any generative kernel**, and every \(G\)-bundle is trivial over a finite set.
> **Change either and the theorem is unavailable.**

**Curve-mediated transport changes the first, by construction.** In the tied-replica witness the
source law \(u^n_{ab}=(\Omega^n_{ab})_\#q^n_b\) is a **generative-side** object — it sits inside
\(P_a^n\), not inside the recognition law. Setting \(\Omega^n_{ab}:=\mathrm P_\gamma(A)\) therefore
places the connection **inside a generative kernel**. (F2) then fails at its hypothesis, not at its
conclusion.

It also attacks (F4). The transport \(\mathrm P_\gamma\) depends on \(A\) along the **whole curve**,
including points off the design \(D\). The record therefore ceases to be a function of
design-restricted data alone, so "every principal bundle is trivializable over a finite set" no
longer suffices to identify record laws across bundles.

**Consequence.** The ledger entry "Operational base holonomy (open)"
(`appendix_claim_ledger.tex:242-256`), which B4 closed in the negative *for the declared model*,
reopens as genuinely open — and now with a concrete candidate construction rather than a wish.

### 3d.5 The candidate observable, and the phenomenology

Take two curves \(\gamma,\gamma'\) from \(c_j\) to \(c_i\). Then
\((\mathrm P_{\gamma'})_\#q_j\) and \((\mathrm P_\gamma)_\#q_j\) differ by the holonomy of the loop
\(\gamma'\!\circ\!\gamma^{-1}\), whose **conjugacy class is gauge-invariant**. So the disagreement
between the two channels is a gauge-invariant functional of the holonomy.

Predicted phenomenology, stated as consequences to be tested rather than results:
1. **Path-dependent disagreement.** Two agents linked by two different chains of intermediaries
   reach different reconciliations. The residual is *not noise* — it is curvature.
2. **Consensus obstruction is topological.** Global agreement is reachable iff the holonomy group has
   a fixed point in the fiber under \(\hat\rho\); for a \(G\)-torsor fiber, iff the holonomy is
   trivial. This is precisely the criterion `wave2-01:534-549` (§1.7) derived for the existence of a
   parallel *background*, now applying to the *interaction*. Frustration becomes a bundle invariant.
3. **A derived correlation length.** Weighting a curve by its information length (`05c:589`, vertical
   Fisher length) gives \(w(\gamma)\sim e^{-L(\gamma)/\xi}\) and hence a decay scale that is
   *derived* rather than fitted — relevant to roadmap experiment E7, whose correlation-length
   observable was judged absorbable by free parameters (`rm-03` §0).
4. **The bundle stops being empirically idle.** `wave2-01:715-719` observes that under
   `12_philosophy.tex:77`'s own idle-wheel criterion, N3(a) is an argument for *removing* the bundle
   from the theory's empirical content. Curve-mediated transport is the modification that would give
   it empirical content instead.

### 3d.6 Which curve? — and the tie to the chosen horn

The construction needs a curve-selection rule. Options, with costs:
- **(a) Declared curve set** (a communication structure embedded in \(\mathcal C\)): extra exogenous
  data, and it re-imports a graph the theory was trying to derive.
- **(b) Geodesics of the induced metric.** Under the It-From-Bit horn the base *does* acquire a
  metric, \(h_{\mu\nu}=\sigma^*g^F\). Its geodesics are then determined by the beliefs, so **agents
  communicate along geodesics of the information-induced geometry**. No exogenous data; fully
  self-consistent with §3c.6. Degenerate exactly on the rank-drop locus.
- **(c) Sum over curves** with weight \(w(\gamma)\): a Wilson-line / propagator structure,
  \(\sum_\gamma w(\gamma)D_{\rm KL}(q_i\|(\mathrm P_\gamma)_\#q_j)\), which is the natural
  lattice-gauge-theory object and connects to the plaquette sector.

(b) is the option consistent with the horn already chosen and should be tried first.

### 3d.8 THE U(1) TWO-PATH WITNESS — COMPUTED, ALL CHECKS PASS

Script: `docs/verification/u1_two_path_holonomy_witness.py`. Deterministic; run it.

**Setup.** \(\mathcal C=S^1\); \(G=U(1)\) with connection \(A=(\Theta/2\pi)\,d\varphi\), full-loop
holonomy \(\Theta\); fiber = 2-D Gaussians with \(U(1)\) acting by pushforward under rotation
(a genuine statistical isometry, per `Theory/05c:59`). Agent \(j\) at \(\varphi=0\), agent \(i\) at
\(\varphi_0=\pi/2\); path \(\gamma\) the direct arc, \(\gamma'\) the other way round, so the two
transports differ by exactly \(\Theta\). Generative model: source label \(J\in\{\gamma,\gamma'\}\)
with prior \(\pi_J\), relational copy \(X\sim u_J=(\mathrm P_J)_\#q_j\), observation
\(o\mid X\sim\mathcal N(X,\sigma_o^2I)\).

**Correction made during the computation.** The raw record law is **not** gauge invariant — a gauge
rotation at \(c_i\) rotates every mixture component in common, so \(p(\cdot\mid\Theta)\) transforms
*covariantly*. Comparing raw record laws conflates gauge-variant overall rotation with genuine
holonomy content. The correct gauge-invariant separation is the distance between **gauge orbits**,
\(d([p_a],[p_b])=\min_{g\in U(1)}\mathrm{TV}((R_g)_\#p_a,\;p_b)\). All results below use it.

| \(\Theta\) | raw TV (gauge-variant) | **orbit distance** | statistic (rad) |
|---|---|---|---|
| 0 | 0.0000000000 | 0.0000000000 | 0.000000 |
| \(\pi/8\) | 0.0722670605 | 0.0374350525 | 0.392699 |
| \(\pi/4\) | 0.1560546769 | 0.1302672342 | 0.785398 |
| \(\pi/2\) | 0.3278284444 | **0.3190849227** | 1.570796 |
| \(\pi\) | 0.5540257212 | 0.3974578354 | 3.141593 |
| \(3\pi/2\) | 0.6705317582 | 0.3190849227 | 1.570796 |
| \(2\pi\) | 0.6963750163 | **8.02e-17** | 0.000000 |

**CHECK 1 — separation. PASS.** Orbit distance at \(\Theta=\pi/2\) is \(0.319>0\): the record laws
are **not gauge-equivalent**, so holonomy is detected on a finite design. At \(\Theta=2\pi\) the
orbit distance returns to \(8\times10^{-17}\), so the record depends only on the holonomy **element**
\(e^{i\Theta}\), not on the connection representative. (The raw TV at \(2\pi\) is large purely
because the whole configuration is rotated — pure gauge, correctly quotiented out.)

**CHECK 2 — gauge invariance. PASS.** Over 200 random \(g(c_i),g(c_j)\in U(1)\): max drift of the
separating statistic \(1.1\times10^{-15}\); max drift of the relational KL terms
\(3.1\times10^{-15}\). Both are \(\mathrm{Aut}_G(P)\)-invariant, and for abelian \(U(1)\) the
statistic *is* the holonomy (conjugacy class = element).

**CHECK 3 — flat-coboundary control. PASS.** With PIFB2's declared transport
\(\Omega_{ij}=e^{i\varphi_i}e^{-i\varphi_j}\), the angle depends only on the endpoints, the loop
product is identically 0, and the record law is **exactly** \(\Theta\)-independent (TV \(=0\) to
machine zero at every \(\Theta\) tested). B4's negative is reproduced under the declared transport.
**The separation in CHECK 1 is therefore caused by the connection, not by the two-path construction
per se.**

**CHECK 4 — the ELBO identity survives \(\Omega\to\mathrm P_\gamma\). PASS.** Direct quadrature on
the joint label-copy space against the closed-form right-hand side:
LHS \(=2.4495355549\), RHS \(=2.4495355549\), \(|{\rm LHS}-{\rm RHS}|=5.5\times10^{-13}\).
\((\mathrm P_\gamma)_\#q_j\) is a pushforward of a probability law by a measurable bijection, hence
normalized, so the finite-mixture KL chain rule of the closed theorem holds verbatim. **Obligation 1
of §3d.7 is discharged.**

**What this establishes.** The separating tuple that `appendix_claim_ledger.tex:242-256` requested —
a named bundle and connection, an assigned base loop, a gauge-invariant record statistic, and two
connection data with distinct holonomy conjugacy classes whose induced record laws differ — **exists**
under curve-mediated transport. This does not contradict B4: B4's hypothesis is that the connection
is not an argument of any generative kernel, and `wave2-01:709` states "Change either and the theorem
is unavailable." Curve-mediated transport changes exactly that.

**Scope — this is a witness, not a theorem.** It establishes existence for one bundle, one connection
family, one fiber, one statistic, one design. It does **not** establish that holonomy is recoverable
in general, nor identifiability of the connection from records, nor anything about non-abelian \(G\)
where the statistic must be a conjugacy-class invariant rather than an element. Obligation 2 of
§3d.7 is discharged **as an existence witness only**; obligations 3 and 4 remain.

### 3d.7 Status and obligations

**Status: CONJECTURE with a specific defeat-condition argument.** What is established is only that
the *hypothesis* of the B4 no-go fails under this construction — not that a separating pair of
connections exists. Obligations, in order:
1. Verify the modified source law \((\mathrm P_\gamma)_\#q_j\) still yields a **normalized**
   generative kernel (it does, being a pushforward of a probability law by a measurable bijection) and
   that the tied-replica ELBO identity of (E1) survives verbatim with \(\Omega\to\mathrm P_\gamma\).
   *Expected easy.*
2. Exhibit the separating tuple B4 requires: a named bundle and connection, an assigned loop, a
   gauge-invariant record statistic, and two connection data with distinct holonomy conjugacy classes
   whose induced record laws **differ**. Natural first witness: \(G=U(1)\), \(\mathcal C=S^1\) or
   \(T^2\), Gaussian fiber, two agents, two paths. *This is the decisive computation.*
3. Check gauge-invariance of the proposed statistic under \(\mathrm{Aut}_G(P)\), and that it depends
   on the conjugacy class only.
4. Determine whether curve-mediated coupling breaks `hyp:gen-design-product` (it does — the source at
   \(c_j\) enters the kernel at \(c_i\)) and therefore whether it is the *same* relaxation as §3c or
   a strictly larger one.

---

## 4. RESULTS — PENDING / RESUME HERE

Two agent panels were dispatched and had **not returned** when the session ended. Their results are
not in this document and must be treated as unknown, not as absent.

### Panel A — `wf_f576312d-d2a` (continuum action), 14 agents

Targets: **T-GRAD** covariant Fisher Dirichlet limit · **T-CURV** Fisher-dressed curvature from
holonomy KL · **T-RESID** feed the tied-replica law into the contraction and compute
\(\varepsilon_h\) · **T-COEF** \(\tau\neq1\), \(\lambda_s\), \(\alpha_i(c)\) from normalized models ·
**T-SIMUL** same-time vs lagged. Structure: 3 grounding extractors → 5 derivations (effort max) →
1 adversarial skeptic each (effort max) → synthesis.

```
script     C:\Users\chris and christine\.claude\projects\
           C--Users-chris-and-christine-Desktop-MultiAgentELBO\
           0ad1292e-01a7-43f7-8c22-fc72b0c10f6c\workflows\scripts\
           elbo-to-pifb2-continuum-action-wf_f576312d-d2a.js
transcript ...\0ad1292e-01a7-43f7-8c22-fc72b0c10f6c\subagents\workflows\wf_f576312d-d2a\
```

### Panel B — `wf_0bb5bbd2-10a` (induced-volume action), 9 agents

Targets: **V-BRIDGE** Polyakov→Nambu–Goto reduction in general \(d\), and whether \(\gamma=h\) is a
minimum or a saddle · **V-TYPE** is \(\gamma\) recognition-side (profiling stays an ELBO) or
generative-side (profiling is empirical Bayes) · **V-DIFF** \(\mathrm{Diff}(\mathcal C)\) invariance,
surviving observables, constraints, local d.o.f. in \(d=1,2,3\), and whether O3 dissolves ·
**V-EXIST** quasiconvexity and coercivity of \(\sqrt{\det h}\).

```
script     C:\Users\chris and christine\.claude\projects\
           C--Users-chris-and-christine-Desktop-MultiAgentELBO-Theory\      <- note the -Theory suffix
           0ad1292e-01a7-43f7-8c22-fc72b0c10f6c\workflows\scripts\
           itfrombit-induced-volume-action-wf_0bb5bbd2-10a.js
transcript ...\0ad1292e-01a7-43f7-8c22-fc72b0c10f6c\subagents\workflows\wf_0bb5bbd2-10a\
```

### How to recover them

**`resumeFromRunId` is same-session only.** After a session boundary the documented resume path is
not available, so do **not** count on it. The reliable recovery route is:

1. **Read `journal.jsonl`** in each transcript directory. It records every agent's actual return
   value, so whatever completed before the cutoff is recoverable verbatim. Do this *first* — do not
   assume the panels produced nothing.
2. Individual `agent-<id>.jsonl` files in the same directory hold per-agent transcripts if the
   journal is incomplete.
3. If little or nothing survived, the scripts are self-contained and re-runnable as-is via
   `Workflow({scriptPath: ...})`. Both embed the full established-state briefing, so they do not
   depend on conversation context.

**Before re-running, patch both scripts' `COMMON` block** to point at
`docs/audits/roadmap-review-2026-08-12/` (now landed in this repo). Both panels ran *without* sight
of `rm-01`…`rm-06` and will otherwise rediscover known results and claim novelty they do not have —
specifically on T-CURV (the Fisher-dressed curvature is already named as the repair in `rm-03` §0
and its invariance verified to ~7e-8) and on any coercivity optimism (PA-3).

**Reconcile every returned finding against §3b (PA-1…PA-13) and §3c–§3d before recording it.**

### Highest-value next steps, in order

1. **Discharge §3d.7 obligations 3–4** — gauge-invariance of the statistic under non-abelian \(G\)
   (needs a conjugacy-class invariant, not an element), and whether curve-mediated coupling relaxes
   `hyp:gen-design-product` identically to §3c or strictly further.
2. **Close the covariant \(O(h^3)\) cancellation** (§2 caveat). This is the one gap between the
   verified flat-transport result and the covariant Dirichlet limit. Small, self-contained, decisive.
3. **T-RESID by hand if the panel did not land it** — take the tied-replica joint as *the*
   microscopic law and compute \((C_h)_\#P_h(\cdot\mid o)\) in closed form. This is what converts
   \(S_h^{\rm exact}=S_h^{\rm PIFB}+\varepsilon_h+c_h\) from a tautology into a computation.
4. **Consolidate the four repositories** before further theory expansion (§3b.3).

---

## 4b. RESULTS (recorded)

*(none yet — the two panels above are the outstanding source)*

### 4.1 T-GRAD
_pending_

### 4.2 T-CURV
_pending_

### 4.3 T-RESID
_pending_

### 4.4 T-COEF
_pending_

### 4.5 T-SIMUL
_pending_

### 4.6 Synthesis
_pending_

---

## 5. Standing constraints for this programme

- \(N\) is **fixed and finite**. The continuum limit refines the base lattice only; it is not an
  \(N\to\infty\) population limit. Thermodynamic limits are a later theory.
- Gauge group: start with a closed **compact** \(G\le GL(K,\mathbb R)\) (Haar averaging gives an
  invariant inner product, so \(G\) conjugates into \(O(K)\)). \(K\) is the **fiber** dimension, so
  the simple rotation group is \(SO(K)\), not \(SO(N)\). Full \(GL(K)\) is a later extension and
  requires a transforming SPD/Fisher metric, coercivity control, and a gauge-invariant definition of
  "complexity" — none of which follow automatically from enlarging the group.
- MAgent is a **legacy prototype and test-vector source**, not the mathematical oracle. The
  replacement codebase is built from the theorem, not from MAgent internals.
- Do not describe the complete PIFB2/MAgent action as derived from the exact ELBO. The defensible
  claim is layered: exact ELBO is the microscopic foundation; PIFB2 is the proposed effective
  operator basis; closure and the continuum limit are open.

## 6. Write policy for this session

Read-only outside this worktree. The Research vault (`Desktop/Research`) and MAgent are untouched.
Nothing is ingested into the wiki without explicit confirmation.
