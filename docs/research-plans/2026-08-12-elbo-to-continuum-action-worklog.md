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

> **CLOSED 2026-08-13 — see §4.1(i).** The covariant cancellation holds. On the symmetric stencil the
> full \(h^3\) coefficient (Amari–Chentsov, exponential-connection and covariant-acceleration parts
> together) cancels exactly and pointwise at every site, by \(\pm\)-parity of the transported-back
> curve, with no discrete integration by parts and no boundary term. Derived by the T-GRAD agent and
> independently reproduced symbolically by its skeptic, who supplied a shorter proof that does not
> depend on the second or third jet of the curve. **(C3) now holds in the covariant setting.** One
> correction carried over: the *one-sided* \(O(h)\) coefficient must be stated invariantly as
> \(c_3=\tfrac12g^F(D^A_\mu q,\nabla^{(e)}_\mu D^A_\mu q)+\tfrac16T_{\rm AC}(D^A_\mu q,D^A_\mu q,D^A_\mu q)\);
> the form displayed in §4.1 as \((D^A_\mu)^2q\) and \(W\) is chart-dependent term by term.

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

> **RESOLVED 2026-08-13.** Both panels were recovered from `journal.jsonl`. Results are in **§4b**;
> the verbatim returns are landed at `docs/audits/panels-2026-08-12/`. The recovery instructions
> below are retained because they worked and are the operative procedure for any future cutoff.

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

*Superseded 2026-08-13 — items 2 and 3 are done (§4.1(i), §4.3). Revised list:*

1. **Settle the T-COEF dispute (§4.4).** The derivation and its skeptic reach opposite verdicts on
   whether PIFB2's deployed coefficients are ELBO-reachable, and it reduces to one clean modelling
   question: *may a generative model declare a block-multiplicity prior matched to the recognition
   multiplicity?* If yes, the \(\sqrt{K_q/K_m}\) obstruction dissolves; if that counts as tuning the
   model to the answer, it stands. Nothing from T-COEF is exportable until this is decided, and it is
   the cheapest decisive item on the list.
2. **Chase the connection mismatch (§4.1(iii)).** The ELBO generates \(\Delta^{(e)}\) (Amari
   \(\alpha=+1\), forced by KL orientation) while the Fisher-Dirichlet action's Euler–Lagrange
   operator is \(\Delta^{(LC)}\). Determine whether some *other* action is the ELBO's genuine
   variational principle — the natural candidate being the one whose EL operator is \(\Delta^{(e)}\)
   — or whether an ELBO simply has no variational principle in this class. Note the gap vanishes
   exactly where \(T_{\rm AC}(D_\mu q,D_\mu q)=0\), which is also where \(d=2\) works in §4.6; those
   are plausibly one phenomenon and worth checking as such.
3. **Write up the \(d=2\) induced-volume bound (§4.6).** \(S_{\rm vol}=\inf_{\mathfrak g}\lim_h
   \mathcal F^{\rm base}_{h,\mathfrak g}\) is a genuine variational bound with a genuine minimum,
   numerically confirmed to \(1.7\times10^{-16}\). It is the strongest base-geometry result the
   programme has, and it is currently recorded in no manuscript. Carry the three caveats: \(\rho\)
   stays exogenous, attainment fails on the rank-drop locus (\(\inf\), not \(\min\)), and every
   one-parameter fiber is excluded.
4. **Discharge §3d.7 obligations 3–4** — gauge-invariance of the statistic under non-abelian \(G\)
   (needs a conjugacy-class invariant, not an element), and whether curve-mediated coupling relaxes
   `hyp:gen-design-product` identically to §3c or strictly further. Untouched by either panel.
5. **Supply a microscopic law with genuine cross-agent coupling** (§4.3). Blockwise-product rigidity
   makes the tied-replica law structurally incapable of generating multi-body operators, so the
   effective-action question cannot be posed on it. Minimal repair: a shared latent, or a
   non-blockwise block-spin \(C_h\) whose coarse coordinates each read several agents' fine blocks.
6. **Consolidate the four repositories** before further theory expansion (§3b.3). Still outstanding,
   and §4b has now added a fifth artifact set that lives only in transcript directories.

---

## 4b. RESULTS (recorded)

**Recovery, 2026-08-13.** Both panels were recovered from `journal.jsonl`, as §4 anticipated. The
panels had *not* produced nothing — they had very nearly finished.

| Panel | Dispatched | Returns recorded | Lost |
|---|---|---|---|
| A `wf_f576312d-d2a` | 14 | **13** — 3 grounding, all 5 derivations, all 5 skeptics | the final synthesis agent (cut mid-run, no salvageable text) |
| B `wf_0bb5bbd2-10a` | 9 | **3** — V-EXIST, V-TYPE, V-BRIDGE | V-DIFF and all skeptics (cut mid-run, no salvageable text) |

Verbatim returns are extracted; the per-agent `agent-<id>.jsonl` files of the lost agents contain no
final answer text, so those four are genuinely unrecoverable and would have to be re-run.

Both panels ran blind to §3b (PA-1…PA-13), exactly as §4 warned. Each result below therefore carries
an explicit reconciliation line. **The synthesis below is written here, by hand, in place of the lost
synthesis agent.**

Every derivation was returned with its own adversarial skeptic (Panel A only). The skeptics are not
decoration: **four of five refused to certify their target**, and in two cases the correction is more
valuable than the original claim.

### 4.1 T-GRAD — the covariant \(O(h^3)\) cancellation is CLOSED; a new and sharper obstruction replaces it

Derivation status **PARTIAL**; skeptic verdict `survives: false`, but the skeptic *strengthens* the
positive half and overturns the derivation's own negative half.

**(i) §2's standing caveat is discharged. This was ranked next-step #2 and it is now closed.**
On the symmetric (all-directed-edge) stencil, with genuine transport \(\Omega^A_{c,c+h}\ne
\Omega^A_{c,c-h}\),

$$\tfrac{h^{d-2}}{2}\sum_{c\in\Lambda_h}\sum_\mu\big[E_{c,+\mu}(h)+E_{c,-\mu}(h)\big]
=\tfrac12\int_{\mathcal C}\|D^Aq\|^2_{g^F}\,dc+O(h^2).$$

The full \(h^3\) coefficient — Amari–Chentsov, exponential-connection, **and** covariant-acceleration
parts together — cancels **exactly and pointwise at every site** by \(\pm\)-parity of the
transported-back curve. No discrete integration by parts, no boundary term. The skeptic recomputed
this symbolically (SymPy, exact Gaussian integrals in a deliberately non-natural chart so
\(\Gamma^{(e)}\ne0\)), reproduced every quantity exactly, called it "the strongest part of the
claim", and supplied a shorter proof: \(f(\varepsilon):=D(\theta_0,\hat\theta(\varepsilon))\) is a
single \(C^3\) function of one variable with \(f(0)=f'(0)=0\), so \(f(h)+f(-h)\) has only even powers
by elementary parity — **independent of the second and third jet of the transported-back curve**.
So (C3) of §2 now holds in the covariant setting, not just the flat one.

One-sided edges are genuinely worse: \(\Theta(h)\) rather than \(\Theta(h^2)\), with the \(O(h)\)
coefficient generically nonzero and *not* a total derivative (\(\int c_3=-3.219270\ne0\)).

**Correction accepted (skeptic, `WEAKENS_SCOPE`).** The \(O(h)\) coefficient must be stated
invariantly as
\(c_3=\tfrac12 g^F(D^A_\mu q,\nabla^{(e)}_\mu D^A_\mu q)+\tfrac16 T_{\rm AC}(D^A_\mu q,D^A_\mu q,D^A_\mu q)\)
with \(\nabla^{(e)}\) Amari's \(\alpha=+1\) connection. As the derivation displayed it — with
\((D^A_\mu)^2q\) and \(W_{ijk}=\mathbb E[\partial_i\partial_j\partial_k\log p]\) — it is
chart-dependent term by term, and \((D^A_\mu)^2\) is undefined by the source geometry
(`Theory/05c:99-107`: \(D^\omega s\) is a vertical-valued one-form, "not a linear covariant
derivative on a vector space of sections"). Only the sum is invariant. This is exactly the ambiguity
`Theory/05c:578-587` flags, and the derivation reintroduced it in its own display. Also: §3.5's
Gaussian witness omits a \(\tfrac13 g^F(v,u)\) term at \(O(h^4)\) — a slip, affecting no conclusion.

**(ii) The derivation's Part II ("REFUTED — the lag turns the Dirichlet term into a mass term") is
itself refuted.** The derivation argued that because sources are \(H_n\)-measurable, the block
becomes \(\tfrac d2\int g^F_{q^n}(\varphi,\varphi)+\text{const}\), a positive-definite Fisher **mass**
term with unique minimizer \(\varphi=0\) — "the gradient operator acts on the wrong field". The
skeptic computed the block's exact minimizer in closed form on the derivation's own \(d=1\)
circle/Gaussian instance and found this is an **order-of-limits error**: taking \(h\to0\) at fixed
\(\varphi\) destroys precisely the \(O(h)\) information that carries the dynamics. The true minimizer
is the exponential-family (e-geodesic) barycentre \(\prod_b u_b^{\beta_b}/Z\) of the transported
neighbours — a discrete heat-kernel average — giving

$$q^{n+1}_i(c)-q^n_i(c)=\frac{h^2}{d}\Big[\tfrac12\Delta^{(e),A}q^n_i(c)-\operatorname{grad}^{g^F}V(q^n_i(c))\Big]+O(h^3),$$

verified to 6–7 digits with clean \(O(h^2)\) convergence (errors \(3.5\times10^{-3}\to3.5\times10^{-5}
\to6.6\times10^{-7}\)). **The base-neighbour block is a forward-Euler / minimizing-movement step of a
covariant diffusion with time step \(\Delta t=h^2/d\), and the Fisher-Dirichlet energy is the energy
that drives it.** Its value at the diagonal is exactly \(\tfrac12\int\|D^Aq\|^2_{g^F}dc+O(h^2)\).
A corollary worth keeping: the replication postulate \(m_h=\lceil dh^{-2}\rceil\) is exactly the
parabolic scaling \(\Delta t\propto h^2\) — still a declaration, but the canonically forced one
rather than an arbitrary one, and at \(d=2\) no weighting is needed at all.

**(iii) NEW OBSTRUCTION — the connection mismatch. This is the real residual obstruction and neither
§2 nor §3c saw it.** The operator the ELBO generates is \(\Delta^{(e),A}=\sum_\mu\nabla^{(e)}_\mu D^A_\mu\),
whereas the Euler–Lagrange operator of \(\tfrac12\int\|D^Aq\|^2_{g^F}\) is the harmonic-map
(Levi-Civita) Laplacian
\(\Delta^{(LC)}=\Delta^{(e)}+\tfrac12(g^F)^{-1}T_{\rm AC}(D_\mu q,D_\mu q)\).
Tested against the whole Amari \(\alpha\)-family: the ELBO's KL orientation (recognition in slot 1)
forces \(\alpha=+1\) **exactly** — matched to \(5.8\times10^{-7}\), while missing \(\alpha=0\) by
\(1.2\) and \(\alpha=-1\) by \(2.3\), mismatches that do **not** shrink with \(h\). (Reverse
orientation matches \(\alpha=-1\), the m-projection.)

> **Net T-GRAD verdict.** The covariant Fisher-Dirichlet term is ELBO-derived **as an energy value**
> and **as the generator of a covariant diffusion**, under one canonically forced parabolic
> replication. It is **not** ELBO-derived **as a variational principle**: the ELBO's stationary
> sections are \(e\)-harmonic (\(\Delta^{(e),A}q=\operatorname{grad}^{g^F}V\)), not critical points of
> the Fisher-Dirichlet action. The gap is exactly \(T_{\rm AC}(D_\mu q,D_\mu q)\), and it vanishes iff
> the Amari–Chentsov contraction vanishes along the section — in particular on Gaussian mean
> submodels with fixed covariance (`Theory/08_infogeometry.tex:238-247`). It persists at every fixed
> point and is *not* repaired by evaluating at \(q^{n+1}=q^n\).

Unchanged and still open: this is pointwise convergence at a fixed \(C^2\) section, **not**
\(\Gamma\)-convergence. Equicoercivity, liminf, recovery sequences, interpolation topology and gauge
compactness all remain missing, and six independent failures block the \(H^1\) case.

*Reconciliation.* Consistent with §3c: the two-point functional escapes A4.4 at finite \(h\), and the
limit is a jet functional. PA-4 stands — the Fisher-as-KL-Hessian base fact is corpus prior art; the
genuine increment is the third-order coefficients and the parity cancellation, now covariant. The
connection mismatch is new and is not anticipated by any of PA-1…PA-13.

### 4.2 T-CURV — invariance proved for noncompact \(G\), but PA-1 and PA-3 both bite

Derivation status **PARTIAL**; skeptic verdict `survives: false` with an exportable surviving core.

**Surviving core (skeptic-certified, "the one exportable piece").** With the belief-dressed
Lie-algebra form \(\langle Y,Z\rangle_q:=g^F_q(Y.q,Z.q)=\mathbb E_q[\psi_Y\psi_Z]\):

$$\big\langle \mathrm{Ad}_gY,\ \mathrm{Ad}_gZ\big\rangle_{\,g_\#q}=\langle Y,Z\rangle_q
\qquad\text{for every }g\in G\text{ (noncompact permitted).}$$

No compactness, no \(\mathrm{Ad}\)-invariant form on \(\mathfrak g\), no Haar measure, no gauge slice.
Verified to 12 digits at \(\operatorname{cond}(g)\) up to 99, while the Frobenius energy swings by
\(679\times\). The plaquette expansion gives
\(D_{\rm KL}(q\|(H_P)_\#q)=\tfrac12h^4\|F_{\mu\nu}(c).q\|^2_{g^F(q)}+O(h^5)\), a **Fisher-weighted,
state-dependent** Yang–Mills energy, not \(\|F\|_F^2\).

**Hypothesis the derivation missed (skeptic, necessary).** \(\psi_Y\in L^2(q)\) is **not** sufficient;
one needs \(q\sim g_\#q\) for \(g\) near the identity, i.e. \(\operatorname{supp}q\) is
\(G\)-invariant. Counterexample: uniform on the disc, where \(\psi_Y=-1\in L^2(q)\),
\(\langle Y,Y\rangle_q=1\), yet \(D_{\rm KL}(q\|q_\varepsilon)=+\infty\) while the claimed expansion
is finite. Holds automatically for Gaussians with \(\Sigma\succ0\).

**Reconciliation — PA-1 fires as predicted, and so does PA-3.** The skeptic independently reached
§3b's conclusion without having seen it: the invariance is a corollary of
`prop:pb-statistical-tensor-descent` (`05c:59-74`, already `ESTABLISHED`) evaluated on fundamental
vertical fields, and the form together with the radical identification is already `ESTABLISHED` at
`05c:946-949`. **Do not claim the construction** (PA-1). What is genuinely new is the evaluation on
the *curvature* and the noncompactness statement. And PA-3 is confirmed from the other side: the
invariance discharges only the norm-invariance clause; **it supplies no coercivity**, and the
derivation's own obstruction list agrees — \(\operatorname{rad}(\sum_i m_{q_i})=\bigcap_i\mathfrak g_{q_i}\)
degenerates on exactly the consensus configuration that PIFB2's own alignment terms drive toward.

Four further obstructions returned, all recorded: the same-time loop is not ELBO-derivable (CE-6, only
the lagged term escapes); **belief screening makes the sector vanish to leading order at \(d=2\)**,
which is PIFB2's deployed base (`PIFB2.tex:434`), so it is nonvacuous only for \(d\ge3\); PIFB2's
**per-agent** \(F^{(i)}_{\mu\nu}\) (`:429`, `:713`) kills the multi-agent nondegeneracy repair, which
needs one shared connection; and for \(G=SO(K)\) with isotropic beliefs the energy vanishes
identically, so this is **complementary to** the classical Wilson action, not a generalization of it.

### 4.3 T-RESID — status **PROVED**, but the skeptic finds the headline vacuous and one clause false

Derivation status **PROVED**; skeptic verdict `survives: false`, `confidence: high`.

**What survives, and it is the real result.** The label-marginalizing contraction has an exact
closed-form residual, and the skeptic upgraded it from an expectation identity to a *pointwise
algebraic* one:

$$\varepsilon_a(x)=\log\frac{\prod_j u_{aj}(x)^{\pi^q_{aj}}}{\sum_j\pi^q_{aj}u_{aj}(x)}
=-D_{\rm KL}\big(\pi^q_a\,\big\|\,\pi^{q,\rm post}_a(\cdot\mid x)\big)\le0,$$

zero iff \(X_a\) is independent of \(J^q_a\). This gives \(c_h\) its **first definition anywhere in
the corpus** (\(c_h=-\sum_a\log Z^q_aZ^s_a\), a weighted Bhattacharyya–Chernoff overlap deficit) and
\(\varepsilon_h\) its first closed form. Before this, \(\varepsilon_h\) and \(c_h\) occurred in
exactly three lines of the whole corpus and \(c_h\) was never defined.

**Struck by the skeptic.** (1) Blockwise-product rigidity is *true but vacuous* — a restatement of the
product hypothesis; it proves nothing about any law with cross-agent coupling and does not discharge
`final-report.md:55`. (2) The label-retaining contraction has \(C_h\) a bimeasurable relabeling of the
identity, so it is `exact-elbo-proof.md:141-147` verbatim; since the microscopic law was *engineered*
to have this ELBO, it establishes nothing about PIFB2's effective-action status, and \(c_h=0\) only
under the unnormalized convention. (3) Statement (4) is false as written (two independent
counterexamples). (4) Extra hypotheses are needed: the product reference must be of *probability*
laws with the stated domination, and the Hoeffding–Möbius space needs \(S_h\in L^\infty(\nu_h)\),
which **fails for Gaussian sources under Lebesgue**.

**The consequential negative, which both agree on.** On a balanced stencil the label-marginalization
residual is *exactly minus* the retained peer sector at \(O(h^2)\), leaving \(O(h^4)\) — verified in
closed form (\(q=N(0,1)\), \(u_\pm=N(\pm h,1)\): peer \(=h^2/2\) exactly, contracted
\(=h^4/4+O(h^6)\)) and by quadrature in 1-D and 2-D. So the criterion \(\|\varepsilon_h\|_\infty\to0\)
is satisfied **and vacuous**; the live question is the *relative* one, which is computed and equals 1
on a balanced stencil. And because \(P^n_h=\bigotimes_aP^n_a\) by construction, this law is
**structurally incapable** of generating multi-body operators — substituting it makes \(\varepsilon_h\)
determinate at the cost of trivializing the very question CE-1/CE-2 were designed to pose.

> So T-RESID converts the tautology into a computation, as intended, and the computation says the
> tied-replica law is the wrong microscopic law for the question. A law with genuine cross-agent
> coupling — a shared latent, or a non-blockwise block-spin \(C_h\) — is still needed.

### 4.4 T-COEF — derivation and skeptic reach nearly opposite conclusions. UNRESOLVED, and this is now the sharpest open dispute.

Derivation status **PARTIAL**; skeptic verdict `survives: false`, `confidence: high`. Unlike 4.1–4.3
the disagreement here is not a correction but a **reversal**, and there was no third agent to break it.

**Derivation's claim.** A "unit-entropy principle": the only non-affine dependence of an exact
negative ELBO on its recognition law is minus the Shannon entropy, with coefficient exactly one; a law
entering \(N\) blocks enters with entropy coefficient exactly \(-N\in\mathbb Z_{\le0}\). Hence
temperatures are **block counts** (proved via non-polynomiality of Shannon entropy on a simplex
segment), all pairwise ratios among \(\{\tau,\tau_s,\alpha+1,\lambda_s+1\}\) are rational, and
therefore PIFB2's deployed pair \(\tau_\beta=\kappa\sqrt{K_q}\), \(\tau_\gamma=\kappa\sqrt{K_m}\)
(`PIFB2.tex:673`) is **OBSTRUCTED** whenever \(K_q/K_m\) is not a rational square — \(\kappa\)-free
and scale-free. Learnable \(\kappa\) admissible only on a Lebesgue-null set. Smooth \(\chi\)
obstructed on T1/T2. State-dependent \(\alpha^*_i(c)\) obstructed.

**Skeptic's counter.** Lemma 0 is the special case of a *deterministic* block count. Randomize the
multiplicity: a tied law whose block multiplicity is a \(Q\)-random variable \(N_\theta\) enters with
entropy coefficient \(-\mathbb E_Q[N_\theta]\in(-\infty,0]\) — **integer iff \(N_\theta\) is a.s.
constant** (verified numerically to \(8.3\times10^{-17}\)). Declaring the generative multiplicity
prior \(\rho:=\xi\) makes \(D_{\rm KL}(\xi\|\rho)=0\) and the coefficient an arbitrary nonnegative
real. On this reading Theorem A is correct but is a theorem about a *hypothesis* (a.s. constant block
count), not about ELBOs, and Corollaries A1–A4 are false without it. The skeptic reports an
end-to-end verification at \(K_q=2\), \(K_m=3\), \(\kappa=1\), irrational ratio \(\sqrt{2/3}\),
concluding that **every constant coefficient PIFB2 deploys is exactly reachable with zero residue**,
and \(\chi\) is reachable as a Bernoulli presence probability reproducing T1, T2 and T5 at once.

**Assessment for the record.** The dispute reduces to one modelling question: *is a generative model
permitted to declare a block-multiplicity prior matched to the recognition multiplicity?* If yes the
skeptic is right and the obstruction dissolves; if that is ruled out as tuning the model to the
answer, the derivation stands. This is exactly the kind of question the roadmap-review referees were
convened for, and it is **not settled here**. Both readings are recorded; neither is to be exported
to `Theory/` until it is.

Three of the derivation's obstructions are *not* touched by the skeptic's mechanism and stand
independently: there is **no** law \(w\) with \(D_{\rm KL}(q\|w)=\tau^{-1}D_{\rm KL}(q\|u)+\text{const}\)
unless \(\tau=1\) (so tempering is provably the closest possible and its residue unavoidable);
tempering leaves a \(\beta\)-dependent normalizer with Gaussian coefficient
\(\tfrac{\tau-1}{2\tau}\log|S_b|\), absorbable only into the attention prior and vanishing only under
a non-generic unimodular gauge condition \(GL(K_q)\) does not supply; and it leaves an entropy residue
\((1-\tau)H_\nu(q)\) that PIFB2's action has no term for. These quantify `PIFB2.tex:678`'s own
qualitative concession.

### 4.5 T-SIMUL — the only target whose skeptic upholds it. `survives: true`.

Derivation status **PARTIAL**; skeptic verdict `survives: true`, `confidence: high`, with (A), (B),
(C), (E) intact and (D) surviving as an identity but with its headline inference struck.

**(A) Diagonal identity.** \(S(x)=L(x\mid x)\) for *every* \(x\), not only at fixed points. The
skeptic notes this is true by definition and therefore constrains only derivatives *along* the
diagonal, and insists the word "deployed" be dropped: \(S\) is the \(\tau=1\), unit-coefficient,
\(\chi\)-free skeleton, not PIFB2's actual functional.

**(B) Reaction decomposition.** \(\nabla S=V^{\rm rec}+R^{\rm react}\) with

$$R^{\rm react}_i(x)=-b_i\,\mathbb E_{\bar q_i}[s_{x_i}],\qquad
b_i=\sum_{l\ne i}\beta_{li},\quad \bar q_i=\tfrac1{b_i}\sum_l\beta_{li}(\Omega_{il})_\#q_{x_l},$$

equal to \(b_i(m_i-\bar m_i)\) in exponential-family natural coordinates. It vanishes iff \(q_{x_i}\)
is the M-projection of the attention-weighted back-transported audience mixture — in particular at
exact transported consensus. The skeptic verified the Gaussian case forces \(\Sigma_i\) to equal the
mixture covariance **including between-component dispersion** (eigenvalues 0.6125, 1.4414 vs
weighted-average 0.3912, 1.2529), matching `PIFB2.tex:1602`'s "dispersion term included". The
decomposition needs no frozen-frame hypothesis and survives co-evolving frames.

**(C) The bridge is REFUTED — this settles a standing open question in the negative.** The lagged
scheme converges at \(O(dt)\) to \(\dot x=-V^{\rm rec}(x)\), **not** to \(\dot x=-\nabla S(x)\); the
fields differ by \(R^{\rm react}\), which is \(O(1)\) in \(dt\). Moreover \(V^{\rm rec}\) is
generically not the gradient of any \(C^2\) potential: on a directed attention 3-cycle with mean-only
Gaussian beliefs the linearization has eigenvalues \(-(a+3b/2)\pm ib\sqrt3/2\), **complex for every
\(b>0\)**, whereas every \(C^2\) gradient flow linearizes to a symmetric matrix with real spectrum.
The skeptic confirms this is discretization-independent — it holds for the delay ODE, Gauss–Seidel
sweeps, and the \(dt\)-free exact-argmin update alike.

> **"Same-time PIFB2 is the \(dt\to0\) limit of the lagged ELBO-exact scheme" is FALSE.** This was
> §4's ranked highest-value T-SIMUL question and it is now answered, negatively and robustly.

**(D) Positive settlement, with its headline struck.** The belief and model label-copy blocks carry no
observation factor, so the marginal evidence \(p^n(o)=\prod_a\int p_a(dk)r_a(dm)L_a(o_a\mid k,m)\) is
independent of the source laws, hence of \(n\) and of any tie: the tied family lies entirely on **one
level set of the log evidence**. This yields \(S(x)=-\log p(o)+D_{\rm KL}(Q_x\|P_{\theta=x}(\cdot\mid o))\)
for every \(x\). But the tie makes \(\{P_\theta\}\) a \(Q\)-indexed family, so
`thm:state_level_elbo_nogo` (`PIFB2.tex:3281`) still correctly forbids the strong reading. The honest
statement is **"a valid bound on a fixed number via a moving model"**, not "an exact ELBO of one fixed
joint". The skeptic additionally refutes the EM reading.

**New obstruction, previously unrecorded.** Even with perfectly symmetric energies and priors, live
softmax \(\beta^*\) is generically **not** symmetric because the row partition functions differ
(verified: \(\max|\beta^*-\beta^{*\top}|=0.547\) at \(N=4\), \(K=3\), \(\tau=0.7\)). This kills the
halving repair on the deployed softmax path. Edge-symmetry also fails independently on the deployed
path because \(GL(K_q)\) transports act on full covariances.

**Checkable prediction.** Under edge-symmetry the lagged flow equals the same-time flow at *halved*
peer coupling. Even where edge-symmetry fails this predicts a systematic factor-2 offset between any
ELBO-calibrated peer coefficient and the deployed \(\beta\) — testable in MAgent by comparing a
detached-sender ablation against the live path at doubled coupling.

### 4.6 Panel B — the induced-volume horn (§3c.6). Three independent agents, one verdict: **do not commit, except at \(d=2\).**

V-EXIST and V-TYPE returned `OBSTRUCTED`; V-BRIDGE returned `PARTIAL`. V-DIFF and all Panel-B
skeptics were lost. The three surviving agents were mutually blind and **converged**, which
substitutes for the missing adversarial pass on the points where all three agree.

**The Polyakov algebra is correct.** Varying \(\gamma\) does give \(\gamma_{\mu\nu}=h_{\mu\nu}\) and
\(S_P|_{\rm on-shell}=S_{\rm vol}\); \(\Lambda=d-2\) is forced uniquely (by injectivity of
\(t\mapsto t^{1-d/2}\) on \((0,\infty)\) for \(d\ne2\)). Verified symbolically at \(d=1,2,3,4\).
**That is the only half that works.**

**Why it fails for \(d\ge3\) — four independent proofs, no two sharing an assumption:**

1. **Conformal mode.** \(\gamma=h\) is a **saddle** of signature \((d(d+1)/2-1,\,1)\), and along the
   conformal ray \(f(\Omega)=\tfrac12(d\Omega^{d-2}-(d-2)\Omega^d)\to-\infty\). So
   \(\inf_\gamma S_P=-\infty\) pointwise. An ELBO is an infimum and is bounded below by
   \(-\log p(o)\); "minimize the free energy over \(\gamma\)" is not a mischaracterization to be
   softened into "extremize" — **the objective has no infimum**. Restated as stationarity it is a
   Virasoro-type *constraint*, and a constraint supplies no bound, hence no variational-inference
   reading. §4 recorded this as unchecked; it is now checked and negative.
2. **Homogeneity / concavity.** \(\sqrt{\det h}\) is degree-\(d/2\) homogeneous and strictly convex
   along rays; any nearest-neighbour transported-KL lattice sum is degree-1 homogeneous and linear in
   \(h\); an infimum of affine functions is concave. By Minkowski's determinant theorem
   \(\det^{1/2}\) is concave on \(\mathrm{PSD}_d\) **iff \(d\le2\)**. So no auxiliary field entering
   linearly can produce \(S_{\rm vol}\) at \(d\ge3\), Polyakov or otherwise, and no additive constant
   repairs it (\(1,\lambda,\lambda^{d/2}\) are linearly independent for \(d\ne2\)).
3. **The \((d-2)\) term.** It *does* have a lattice counterpart — the ELBO's site sector — but
   matching demands \(f_{\rm site}\equiv-(d-2)/2\), a strictly **negative** constant per design point.
   Every ELBO site block except \(-\mathbb E\log\ell\) is nonnegative, and a negative constant needs an
   observation reference measure of total mass \(\ne1\), breaking exactly the normalization hypothesis
   that certifies the closed theorem. Lattice reading: refining the design would lower the free energy
   without bound — obstruction 1 in disguise.
4. **Non-coercivity, and it is PA-3 again.** \(S_{\rm vol}[q\circ\varphi]=S_{\rm vol}[q]\) **exactly**
   for every \(\varphi\in\mathrm{Diff}(\mathcal C,\partial\mathcal C)\), and those orbits are unbounded
   in every Sobolev norm. No sublevel set is bounded; the direct method is dead in every dimension, on
   every fiber, with any boundary data. **PA-3's escape — pick compact \(G\) — does not exist here:
   \(\mathrm{Diff}\) of a positive-dimensional manifold is never compact.** Committing to
   \(S_{\rm vol}\) converts a fixable obstruction into an unfixable one.

**Two further structural defects.** \(F\equiv0\) on \(\{\operatorname{rank}\xi<d\}\), a cone containing
rays of unbounded norm — an explicit family has \(S_{\rm vol}\equiv0\) *exactly* while
\(\|Dq_k\|_{L^2}\to\infty\), so minimizing \(S_{\rm vol}\) actively drives the belief field toward rank
deficiency (the Nambu–Goto crumpling instability). And by the area formula \(S_{\rm vol}\) is a
parametric Plateau problem whose compactness theory lives on integral **currents**; the relaxed
minimizer generically is not the graph of a section, so **the minimizer of \(S_{\rm vol}\) is not an
agent** — contradicting the ontology at `Theory/02_geometry.tex:16-34`. Also \(\det h\equiv0\)
identically whenever \(d>\dim\mathcal B\) (Cauchy–Binet).

**Rigidity — the finding that should change the plan.** If \(S[q]=\int f(h)\) is
\(\mathrm{Diff}(\mathcal C)\)-invariant with \(f\) continuous, then \(f(A^\top hA)=|\det A|f(h)\),
forcing \(f(h)=f(I)\sqrt{\det h}\). \(S_{\rm vol}\) is **the unique** local
\(\mathrm{Diff}(\mathcal C)\)-invariant first-order scalar. So there is no better invariant action to
go looking for, and combined with the non-coercivity the conclusion is not "\(S_{\rm vol}\) is hard"
but:

> **Full base-diffeomorphism invariance and existence-by-the-direct-method are incompatible.** That is
> the clean negative.

**Where it *does* work — \(d=2\), and better than anyone in this programme had argued.** Four things
line up and they are the same fact seen four ways: the forced bond weight \(h^{d-2}=1\); every Bravais
lattice supplies a **unimodular** densitized cometric, so the ELBO carries the lattice's conformal
structure and is blind to its scale; the cosmological constant \((d-2)\) vanishes, so no term without
an ELBO origin is needed; and \(\sqrt{\det h}\) is concave and 1-homogeneous on the \(2\times2\) PSD
cone, hence *exactly* the infimum of the linear forms dominating it — which is precisely the lattice
form. The result

$$S_{\rm vol}[q]=\inf_{\mathfrak g}\ \lim_{h\to0}\ \mathcal F^{\rm base}_{h,\mathfrak g}[q]\qquad(d=2)$$

is a genuine variational **bound** with a genuine **minimum**, not a saddle, saturated exactly on the
conformal class of \(h\). Numerically confirmed to \(1.7\times10^{-16}\) with exact Gaussian KL on real
lattices. V-BRIDGE's own assessment: "that is a publishable theorem and it is the strongest thing this
programme has produced on base geometry." Three tempering caveats: N1 is only **half** saved
(unimodularity leaves the site density \(\rho\) exogenous, and the site sector is the bulk of the
ELBO); attainment still fails on the rank-drop locus, so the theorem reads \(\inf\), not \(\min\); and
\(d=2\) excludes every one-parameter fiber (\(\dim\mathcal B\ge2\) is hard).

**On the typing question (V-TYPE).** The answer is **mixed, and the load-bearing half is generative.**
Support, density and reference row are all generative/design data; only the **anisotropy** is
recognition-side. Worse, it is *frozen*: at the unit coefficients the exact theorem actually delivers,
\(\beta^*=\pi+O(h^2)\) and the cost/benefit ratio for moving \(\gamma\) an \(O(1)\) distance is
\(h^{-2}\to\infty\). And the **scale** can never be recognition-side, because a probability row is
trace-normalized — the ELBO's own \(\gamma\)-elimination returns a soft-*min* (a soft smallest
eigenvalue of \(h\)), not a determinant: different constraint set, different homogeneity degree.

> **Net Panel B verdict.** §3c.6's conjecture is resolved, and against itself. The induced-volume horn
> does **not** remove the exogenous cometric and density — it renames them \(\pi\) and \(\rho\) and
> moves them to a different chapter. Keep \(S_{\rm vol}\) if at all as an **engineered**
> \(\mathrm{Diff}(\mathcal C)\)-invariant action, stated as engineered in PIFB2's own register
> (`PIFB2.tex:3407`), which is still a real gain — it deletes `PIFB2.tex:1731`'s \(\sqrt{|g|}(c)dc\)
> and with it the intrinsic base metric that contradicts N1 (§3c.7). **Claim no ELBO derivation**,
> except at \(d=2\), where the bound is genuine and should be written up.

Worth recording that §3c.6's own caveats were right on both counts it flagged ("not the \(h\to0\)
limit of the lattice KL sum"; "degenerate on the rank-drop locus"), and that
`wave2-01-constructions.md:134-136` had already rejected \(\sqrt{\det h^\omega_s}\) for the rank
reason. The PI was re-proposing an object the wave-2 audit had already turned down.

### 4.7 Synthesis (written by hand — the synthesis agent was lost)

**What moved.**

1. **§2's covariant \(O(h^3)\) gap is closed** (4.1), by a pointwise parity argument that is more
   robust than expected — it does not depend on the second or third jet of the transported-back curve.
   Ranked next-step #2 is done.
2. **The same-time bridge is refuted** (4.5), robustly and discretization-independently. The standing
   T-SIMUL question is closed in the negative.
3. **The induced-volume horn is resolved against itself for \(d\ge3\) and confirmed for \(d=2\)** (4.6),
   by four independent arguments from three mutually blind agents.
4. **\(\varepsilon_h\) and \(c_h\) now have closed forms** (4.3) — \(c_h\)'s first definition anywhere —
   at the cost of showing this microscopic law cannot pose the question it was substituted to answer.

**The one genuinely new obstruction: the connection mismatch (4.1(iii)).** The ELBO's KL orientation
forces Amari's \(\alpha=+1\); the Fisher-Dirichlet action's Euler–Lagrange operator is Levi-Civita
(\(\alpha=0\)). The gap is \(\tfrac12(g^F)^{-1}T_{\rm AC}(D_\mu q,D_\mu q)\), it does not shrink with
\(h\), and it persists at every fixed point. This is sharper than the obstruction it replaces, because
it is not about limits or hypotheses — it is a statement about which operator an ELBO can generate at
all. **It also explains the \(d=2\) coincidence in 4.6 and the Gaussian-fixed-covariance escape in 4.1
as the same phenomenon: both are exactly where the Amari–Chentsov contraction drops out.**

**A pattern across all five Panel A targets.** Every sector reaches the same shape of answer: the ELBO
supplies the *energy value* exactly, and fails to supply the *variational principle*, the *coercivity*,
or the *measure*. T-GRAD gives the Dirichlet energy but the wrong stationarity operator; T-CURV gives
an invariant curvature density but no coercivity (PA-3) and nothing at \(d=2\); T-RESID gives an exact
residual but on a law with no cross-agent content; Panel B gives an exact \(d=2\) bound but leaves
\(\rho\) exogenous. This is consistent enough to be worth stating as a program-level finding rather
than five separate caveats.

**Reconciliation summary against §3b.** PA-1 fired exactly as predicted (T-CURV construction is not
novel; only the noncompactness route is). PA-3 fired twice, once as predicted on T-CURV and once
unforeseen on \(\mathrm{Diff}(\mathcal C)\), where it is fatal rather than fixable. PA-4 stands. No
returned result contradicts rm-01…rm-06. **Nothing here is cleared for `Theory/` yet** — 4.4 is an
unresolved dispute, and 4.1's positive half needs the invariant restatement of \(c_3\) before it is
written down.

**Missing and worth re-running:** Panel B's V-DIFF (\(\mathrm{Diff}(\mathcal C)\) invariance,
surviving observables, local d.o.f. in \(d=1,2,3\), whether O3 dissolves) — though 4.6 has largely
answered it in the negative — and Panel B's skeptic tier. Both scripts are self-contained and
re-runnable; patch the `COMMON` block per §4 first.

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
