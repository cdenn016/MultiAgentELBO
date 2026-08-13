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
| Exact two-channel finite ELBO | `docs/derivations/2026-08-12-exact-two-channel-finite-elbo/` | **COMPLETE_AFFIRMATIVE** | Tied-replica normalized joint whose exact negative ELBO equals the joint-typed lagged unit-coefficient two-channel scalar \(\mathcal F_{\rm JT,h}^{\rm lag,1}\) plus \(\sum_a I_{\zeta_a}(K_a;M_a)\); equality to the literal PIFB2 observation sector remains open |
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
\begin{aligned}
\mathcal F_h^{n+1}=\sum_{a\in A}\Big[&
D_{\rm KL}(q_a\|p_a)+D_{\rm KL}(s_a\|r_a)+I_{\zeta_a}(K_a;M_a)
-\mathbb E_{\zeta_a}\log\ell_a(o_a\mid K_a,M_a)\\
&+D_{\rm KL}(\beta_a\|\pi_a^q)+\sum_b\beta_{ab}D_{\rm KL}(q_a\|u^n_{ab})\\
&+D_{\rm KL}(\gamma_a\|\pi_a^s)+\sum_b\gamma_{ab}D_{\rm KL}(s_a\|v^n_{ab})\Big]\\
&=\mathcal F_{\rm JT,h}^{\rm lag,1}+\sum_{a\in A}I_{\zeta_a}(K_a;M_a).
\end{aligned}
$$

Under \(\zeta_a=q_a\otimes s_a\) the correction vanishes and equality to the declared
joint-typed scalar is **exact**. This does not prove equality to the observation term printed in
literal `Theory/PIFB2.tex`: its pointwise form omits the model expectation, while its displayed
full functional leaves the model variable unbound. Under a normalized predictive reading and state-model mean field, the joint-minus-predictive
observation objective is a nonnegative posterior KL. For correlated \(\zeta\) it is instead a
sign-indefinite difference of two conditional KLs. The literal
PIFB2 crosswalk therefore remains **INCONCLUSIVE** until that source is repaired and reverified.

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
- **(C3) The weight \(h^{d-2}\) is forced by edge counting.** *(CORRECTED 2026-08-13 — the original
  read "Therefore the weight is forced, not chosen", which overreached twice. (a) The forcing is by
  **counting alone**, not by the \(h^3\) cancellation: an \(O(h^3)\) per-bond remainder contributes
  \(O(h)\) and vanishes in the limit regardless, so the symmetric stencil improves the **rate** from
  \(O(h)\) to \(O(h^2)\) but is not needed for the limit to exist — see the explicit "correction to
  the worklog's framing of E2/C3" at `panelB-V-BRIDGE-derivation.md:63`, confirmed numerically by an
  oriented uncancelled sum converging to the same target at \(O(h)\) in both flat and covariant
  settings. (b) "Forced" holds for the unique deterministic **Riemann-sum** weight; the exact ELBO is
  a counting-measure sum with unit coefficients and supplies \(h^{d-2}\) only via the declared integer
  replication \(m_h=\lceil dh^{-2}\rceil\) of §4.1(ii) — canonically forced parabolic scaling, but
  still a declared postulate.)* With \(\sim h^{-d}\) sites and a
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

**Location:** `docs/audits/roadmap-review-2026-08-12/` (tracked in **this** repo since `caa4a15`; the
former absolute `Documents/ChatGPT` path was stale and contradicted `:650-651` below)
(six referee reports `rm-01` … `rm-06`), plus a fourth derivation run
`docs/derivations/2026-08-12-pifb2-elbo-program-decision/` (terminal_status `null`, bounded checkpoint).

**These were NOT visible to the §3 agents** — they live in the `Documents/ChatGPT` copy, and the
agents were pointed at the tmp worktree. Every §4 result must therefore be reconciled against
this section before any novelty claim is made.

### 3b.1 Findings that pre-empt or correct this session's framing

| # | Finding | Source | Effect on §3 targets |
|---|---|---|---|
| **PA-1** | **"Fisher-dressed curvature" is already identified as the repair** for the \(GL(K)\) curvature problem. | `rm-03-action-class.md:0` (verdict §0 item 1) | **T-CURV is not novel as an idea.** Only the *ELBO-derivation route* (holonomy KL) may be new. Do not claim the construction. |
| **PA-2** *(CORRECTED 2026-08-13)* | For \(G=GL(K,\mathbb R)\), \(K\ge2\), there is **no positive-definite** Ad-invariant inner product on \(\mathfrak{gl}(K,\mathbb R)\), hence no fixed-inner-product \(\kappa\|F_A\|^2\) that is both gauge-invariant and **coercive**. The Ad-invariant symmetric bilinear forms are exactly the 2-dim space \(\{a\,\mathrm{tr}(XY)+b\,\mathrm{tr}X\,\mathrm{tr}Y\}\). With \(S=E_{12}+E_{21}\), \(A=E_{12}-E_{21}\) traceless and \(\mathrm{tr}(S^2)=+2\), \(\mathrm{tr}(A^2)=-2\): every form with \(a\ne0\) is **indefinite** — signature \((3,1)\) for \(K=2\), \((6,3)\) for \(K=3\), the trace direction flipping across \(a+bK=0\) (the Killing form sits on that degenerate locus, signature \((2,1,1)\)/\((5,3,1)\)). But the line \(a=0,\ b>0\) gives \(b\,(\mathrm{tr}X)(\mathrm{tr}Y)\), which **is** Ad-invariant (verified to \(2.8\times10^{-14}\)) and **nonnegative** — degenerate, rank 1, radical \(\mathfrak{sl}(K,\mathbb R)\), i.e. Maxwell for the determinant line and identically zero on \(\mathfrak{sl}(K)\)-valued connections. **So "every element is indefinite" is FALSE; the correct no-go is positive-definiteness.** | `rm-04-gauge-kinematics.md` §1.5 — **erratum:** rm-04 overstates in three places (§0(4) at :43-46, the §1.5 box at :295-299, and finding K1 at :879); only the computation at :285-288 and the ledger at :984, both scoped to positive-definiteness, are correct as written. Do not edit rm-04 — it is an archived verbatim return. | Compact type is necessary **and sufficient** for a *fixed* definite Ad-invariant form, hence for a coercive fixed-inner-product curvature sector, and belongs in T0 **in that scope**. It is **not** required for invariance or nonnegativity as such — §4.2 exhibits a state-dependent Fisher-dressed form that is exactly invariant for noncompact \(G\), at the cost of degeneracy on the isotropy algebra and non-coercivity along gauge orbits. The referee predicted exactly this before T-CURV ran. |
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

**REBUILT 2026-08-13 (E12(iv)) from `git ls-files` at HEAD. The pre-consolidation table below was
stale and contradicted `:650-651` in this same file; it is superseded.**

| Location | Has | Missing |
|---|---|---|
| `Desktop/MultiAgentELBO` (**this repo, `main`**) | `Theory/`, PIFB2 copy, ultradeep audit waves 1–2, continuum roadmap + review, **all four derivation runs**, **`rm-01`…`rm-06`**, the 16 recovered panel returns, this worklog, both verification scripts, the interim review and its adjudication cluster | — |
| `Documents/ChatGPT/MultiAgentELBO` (`main` @ `e1f8795`, 11 behind) | a stale checkout; five untracked interim-review reproduction artifacts not present in the Desktop checkout | everything landed after `e1f8795` |
| `Desktop/Research` | live `PIFB2.tex` (byte-identical to the repo copy), wiki, `magent_elbo_whitepaper` | the derivation and audit material |

The `C:/tmp/MultiAgentELBO-elbo-action-019ff75d` worktree was **removed on 2026-08-13** (it held no
unmerged commits; `HEAD = e1f8795` was already an ancestor of `main`). The branch ref survives.

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

~~A base-neighbour block is precisely residual cross-design dependence.~~ **WITHDRAWN 2026-08-13**
— see §3c.9. That identification is false: the base-neighbour sector is available on a *strictly
design-product* generative law. What the sector actually costs is a transported label-copy block
\((J_a,X_a)\) added to `Theory/04`'s declared generative class, not a relaxation of
`hyp:gen-design-product`. `hyp:gen-design-product` is nonetheless the *mildest* of O2's
three escapes and the only one already tagged `HYPOTHESIS` rather than `ESTABLISHED` — it is a
declared modelling choice, not a theorem, and it is stated in the manuscript as excluding exactly
the thing the gradient sector needs.

### 3c.3 The resulting statement, and where A4.4 does bite

> **Proposition (session result, DERIVATION + APPLICABLE_THEOREM A4.4). CORRECTED IN PLACE
> 2026-08-13 (E3(2)); see §3c.9 for the witness.**
> At every fixed finite lattice \(\Lambda_h\) (itself a finite design), the base-neighbour
> transported-KL sector is an **exact** negative-ELBO component of a normalized generative law that
> is a strict **product** over design points conditional on \(H_n\). What it costs is **not** a
> relaxation of `hyp:gen-design-product` but the addition of an \(H_n\)-measurable transported
> label-copy channel \((J_a,X_a)\) to the declared generative class of `Theory/04`, plus the
> replication multiplicity \(m_h\).
> Its \(h\to0\) limit, when it exists, is a **jet** functional and therefore — by Theorem A4.4(a),
> whose hypotheses now hold — is **not** the ELBO of any finite design.
>
> ~~such a law exists iff `hyp:gen-design-product` is relaxed~~ — **WITHDRAWN**, §3c.9.

So the layered picture is not merely defensible, it is **forced**:

| Object | Status |
|---|---|
| Exact ELBO at finite \(\Lambda_h\), cross-design coupling allowed | **EXACT** (tied-replica + base-neighbour block) |
| \(h\to0\) limit \(=\tfrac12\int\|D^Aq\|^2_{g^F}\) | limit of exact ELBOs; **not itself a finite-design ELBO** |
| Identification of the limit with a finite-design ELBO | **REFUTED** by A4.4(a) |

### 3c.9 CORRECTION 2026-08-13 — what the base-neighbour sector actually costs

The Proposition above says such a law "exists iff `hyp:gen-design-product` is relaxed". **That clause
is withdrawn.** It is either tautological (if "a law coupling design points" just means "a law that is
not a design product") or false (if it means the sector *requires* such a law). Established by
independent recomputation during the referee adjudication:

- **"\(\Leftarrow\)" is refuted by an explicit witness.** A 3-site cycle with 2 neighbours per site,
  \(K=3\), nontrivial permutation transports, admits an exact negative-ELBO decomposition (residual
  \(3.6\times10^{-15}\)) with a **strictly positive** base-neighbour transported-KL sector
  (\(0.496109389\)) under a generative joint whose total correlation across design points is
  \(7.4\times10^{-17}\) — i.e. `hyp:gen-design-product` holding **exactly**.
- **"\(\Rightarrow\)" is unsupported.** Relaxing the hypothesis produces an interaction energy
  \(-\mathbb E\log\psi(k_a,k_b)\), not a transported KL — verified symbolically to
  \(5.6\times10^{-17}\), and numerically a different functional with a different value (0.3063 vs
  0.2532 on a matched instance). Cross-design dependence is neither necessary nor sufficient.

**The corrected statement.** *At every fixed finite \(\Lambda_h\) the base-neighbour transported-KL
sector is an exact negative-ELBO component of a normalized generative law that is a strict product
over design points conditional on \(H_n\). What it costs is not `hyp:gen-design-product` but the
addition of an \(H_n\)-measurable transported label-copy channel \((J_a,X_a)\) to the declared
generative class of `Theory/04`, plus the replication multiplicity \(m_h\).*

So the sector **does** cost a modification of the generative model — just not the one named. The
\(h\to0\) row of the table above is unaffected: A4.4(a) still applies to the limit.

Two inherited loci now carry the withdrawn premise and must be flagged where they are read:
`panelB-V-BRIDGE-derivation.md:67` (H5) and `:314` (OB-12), both self-labelled as inherited.

*Provenance: raised as Finding 2 of `docs/reviews/2026-08-12-pifb2-elbo-program-interim-theory-review.md`,
upheld at high severity under adversarial verification. The same lagged/contemporaneous dichotomy was
reached independently and blind by the T-GRAD panel agent.*

---

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
independence *across contexts*. **STRUCK 2026-08-13, in both directions — see §3c.9.** The claim
that the Dirichlet sector "vanishes identically iff `hyp:gen-design-product` holds" is refuted on
"\(\Leftarrow\)" by an explicit exact-ELBO witness on a strictly design-product law, and unsupported
on "\(\Rightarrow\)" because relaxing the hypothesis yields an interaction energy, not a transported
KL. The most that survives: *a nonzero transported-KL sector requires a generative channel that reads
beliefs at other contexts; it does not require, and is not implied by, stochastic cross-design
dependence.* Correspondingly \(\eta_q\) is **fixed by the declared source row \(\beta\) and the
declared replication \(m_h=\lceil dh^{-2}\rceil\)** (§4.1(ii)) — with \(\sum\beta=1\) and cell weight
\(h^d\) the coefficient of \(\tfrac12\int\|D^Aq\|^2_{g^F}\) is forced to exactly 1. It is a declared
coefficient, **not** a measure of dependence, and roadmap experiment **E4** must be re-worded
accordingly: it tests a postulated term, not a probabilistic hypothesis.

### 3c.5 The idle-wheel consequence — why this is load-bearing

`Theory/12_philosophy.tex:77` adopts an explicit **idle-wheel criterion**: *a posit with no trace in
any declared observable is removed by parsimony.*

Observe: with **no** base-derivative and no otherwise-nonlocal-in-\(\mathcal C\) term, the entire
action is a sum of independent pointwise problems indexed by \(c\). The theory factorizes over
\(\mathcal C\) completely; \(\mathcal C\) could be replaced by an arbitrary index set carrying a
measure and nothing whatsoever changes. **The smooth manifold structure of \(\mathcal C\) is then
idle in exactly the sense that chapter uses to license removal.**

Combining with §3c.2:

> **CORRECTED 2026-08-13 (E3(5); the withdrawn form is preserved below for the record).**
> **\(\mathcal C\) earns its manifold structure iff the action contains a term coupling distinct
> contexts. Such a term is available from an exact finite ELBO with `hyp:gen-design-product`
> **intact**, via a lagged, history-measurable transported label-copy channel.** The idle-wheel half
> is untouched: without a base-derivative sector the action factorizes over \(c\) entirely.
>
> ~~The base-derivative sector is precisely what saves \(\mathcal C\) from being an idle wheel, and
> that sector exists iff `hyp:gen-design-product` is relaxed. Hence \(\mathcal C\) earns its
> manifold structure iff the generative model admits cross-context dependence.~~
> **WITHDRAWN** — refuted in both directions by §3c.9. "⇐" fails against an explicit exact-ELBO
> instance on a strictly design-product law (total correlation \(7.4\times10^{-17}\)) that still
> carries a strictly positive base-neighbour sector; "⇒" is unsupported, since relaxing the hypothesis
> yields an interaction energy \(-\mathbb E\log\psi(k_a,k_b)\), a different functional with a
> different value, not a transported KL.

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
- generates nontrivial holonomy **whenever \(A\) is not gauge-trivial**. *(CORRECTED 2026-08-13 —
  the original said "iff \(A\) has curvature", which is false in one direction. Nonzero curvature
  implies nontrivial restricted holonomy (Ambrose–Singer); the converse fails, since a flat
  connection on a base with nontrivial \(\pi_1\) has nontrivial monodromy and identically zero
  curvature. That is exactly the situation of the \(S^1\) witness in §3d.8.)*

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
   reach different reconciliations. The residual is *not noise* — it is **holonomy**: the monodromy
   of \(A\) around \(\gamma'\circ\gamma^{-1}\). On a base of dimension \(\ge2\) the infinitesimal
   version of the same residual is curvature (cf. the plaquette expansion in §4.2); on a
   1-dimensional base it is flat monodromy and curvature vanishes identically.
2. **Consensus obstruction is topological.** Global agreement is reachable iff the holonomy group has
   a fixed point in the fiber under \(\hat\rho\); for a \(G\)-torsor fiber, iff the holonomy is
   trivial. This is precisely the criterion `wave2-01:534-549` (§1.7) derived for the existence of a
   parallel *background*, now applying to the *interaction*. Frustration becomes an invariant of the
   flat connection modulo gauge — a point of \(\mathrm{Hom}(\pi_1(\mathcal C),G)/\mathrm{conj}\).
   *(CORRECTED 2026-08-13: it is **not** a bundle invariant. In the §3d.8 witness the bundle is
   trivial (\(H^2(S^1;\mathbb Z)=0\)) and the holonomy varies continuously over the modulus space
   \(U(1)\).)*
3. **A derived correlation length.** Weighting a curve by its information length (`05c:589`, vertical
   Fisher length) gives \(w(\gamma)\sim e^{-L(\gamma)/\xi}\) and hence a decay scale that is
   **not** derived — *(CORRECTED 2026-08-13: the \(\omega\)-horizontal lift has vertical Fisher
   length \(L^\omega=0\) identically, by `05c` `prop:pb-curve-taxonomy` (ESTABLISHED), and §3d.1's
   transport **is** the horizontal lift. So \(w(\gamma)=e^{-L(\gamma)/\xi}\equiv1\) for every curve
   and every \(\xi\): the weight is not merely underived, it is vacuous. If a weight is wanted,
   declare the **section-curve** length \(L^\omega(s\circ\gamma)=\int\sqrt{h^\omega_s(\dot\gamma,\dot\gamma)}\)
   instead and label \(\xi\) an explicit free parameter. The standing warning against this exact use
   is already at §3c.8.)* — relevant to roadmap experiment E7, whose correlation-length
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

### 3d.8 THE U(1) TWO-PATH WITNESS — EXACT MOMENT CERTIFICATE AND CONTROLS

Script: `docs/verification/u1_two_path_holonomy_witness.py`. Derivation:
`docs/derivations/2026-08-13-u1-record-moment-derivation.md`. Focused tests:
`tests/test_u1_two_path_holonomy_witness.py`.

**Setup.** \(\mathcal C=S^1\); \(G=U(1)\) with connection
\(A=(\Theta/2\pi)\,d\varphi\), full-loop monodromy \(e^{i\Theta}\); fiber = 2-D
Gaussians with \(U(1)\) acting by pushforward under rotation. Agent \(j\) is at
\(\varphi=0\), agent \(i\) at \(\varphi_0=\pi/2\); the direct and long paths have
transport angles \(a_1,a_2\) with \(a_1-a_2=\Theta\). The normalized generative model
uses a path label \(J\), relational copy \(X\sim(\mathrm P_J)_\#q_j\), and observation
\(O\mid X\sim\mathcal N(X,\sigma_o^2I)\).

**Correction to the previous numerical argument.** A minimum over a finite gauge grid is only an
upper bound on the gauge-orbit infimum and cannot prove separation. The load-bearing observable is
instead the marginalized record moment

\[
S(\Theta):=\|\mathbb E[O\mid\Theta]\|^2
=\|\mu\|^2\frac{1+\cos\Theta}{2}.
\]

It is gauge invariant because a passive endpoint change rotates the mean without changing its norm.
For the declared \(\|\mu\|=1\), \(S(0)=1\) and \(S(\pi/2)=1/2\), proving that these selected record
laws are not gauge-equivalent without observing the latent path label.

| \(\Theta\) | \(S(\Theta)=\|\mathbb E O\|^2\) | \(\operatorname{tr}\operatorname{Cov}(O)\) |
|---|---:|---:|
| 0 | 1.0000000000 | 0.9450000000 |
| \(\pi/8\) | 0.9619397663 | 0.9830602337 |
| \(\pi/4\) | 0.8535533906 | 1.0914466094 |
| \(\pi/2\) | **0.5000000000** | 1.4450000000 |
| \(\pi\) | 0.0000000000 | 1.9450000000 |
| \(3\pi/2\) | 0.5000000000 | 1.4450000000 |
| \(2\pi\) | 1.0000000000 | 0.9450000000 |

**CHECK 1 — exact separation and equivalences. PASS.** The exact separator gap is
\(S(0)-S(\pi/2)=0.5\). Periodicity is checked componentwise with the exact common gauge
\(g=-k\varphi_0\), giving maximum mismatch \(2.45\times10^{-16}\). The equal-weight mirror
equivalence \(\Theta\leftrightarrow2\pi-\Theta\) is checked with
\(g=\pi/2+\Theta/2\) plus label interchange, giving mismatch \(2.22\times10^{-16}\). Raw total
variation \(0.3278284444\) for \(0\) versus \(\pi/2\) is retained only as a quadrature diagnostic.

**CHECK 2 — passive gauge invariance. PASS.** Over 200 deterministic random endpoint frame changes,
the maximum drift of \(S\) is \(5.55\times10^{-16}\) and the maximum drift of the relational KL
terms is \(3.11\times10^{-15}\).

**CHECK 3 — exact coboundary and presentation controls. PASS.** For
\(A=d\lambda_\Theta\), \(\lambda_\Theta(\varphi)=\Theta\sin\varphi/(2\pi)\), both routes have the
same endpoint angle \(\alpha\); the exact gauge \(g=-\alpha\) maps every tested law to the
\(\Theta=0\) representative with component error \(0\). Thus the raw record law is not
\(\Theta\)-independent; the exact statement is that all these laws lie in one gauge orbit.

The executable counterpresentation sets the connection to zero and supplies the same two group
twists as ordinary label-conditional kernel parameters. Its components match the curve-mediated
components exactly (error \(0\)). Therefore this record identifies a relative group twist within
the selected family, not its connection origin across broader model classes.

**CHECK 4 — finite-mixture KL identity. PASS.** Direct quadrature gives
LHS \(=2.4495355549129756\), RHS \(=2.4495355549129770\), residual
\(1.3322676295501878\times10^{-15}\). The finite-mixture KL chain rule itself is analytic; this
number is numerical corroboration.

**What this establishes.** The normalized curve-mediated construction has selected monodromy
parameters that change an observable gauge-invariant record moment, and its label-copy ELBO identity
survives. This is a one-family existence witness, not connection identifiability. Curvature, bundle
topology, nonabelian groups, live recognition sources, and presentation-invariant physicalization
remain open. A multi-point cocycle-constrained comparison is a proposed discriminator, not a proved
necessary or sufficient repair.

### 3d.7 Status and obligations

**Status (UPDATED 2026-08-13): WITNESSED WITHIN A CONSTRAINED PRESENTATION.** The observable moment
and exact gauges close the finite \(S^1,U(1)\) existence calculation. The flat-twist control prevents
an ontological reading: the same record law has a zero-connection presentation. Remaining obligations
are to define the admitted presentation-equivalence relation, show that a proposed physical readout
descends to its quotient or derive a canonical agentization, extend any separator to nonabelian
conjugacy classes, and separately treat curvature/topology on a higher-dimensional base.

---

## 3e. AGENT → META-AGENT RENORMALIZATION — the coherence criterion, and the extent question

*Opened 2026-08-13. Point-wise results are computed and committed; the extent criterion is under
investigation and is NOT established. Witness: `docs/verification/meta_agent_coherence_witness.py`
(seed 20260813, four claims, all asserted in-script).*

### 3e.1 The object

At a fixed base point \(c\), the active agent set is \(A(c)=\{i:c\in\mathcal C_i\}\), carrying a
weighted directed graph with attention rows \(\beta_{ij}(c)\) (belief) and \(\gamma_{ij}(c)\) (model)
and fiber transports \(\Omega_{ij}(c)\), \(\widetilde\Omega_{ij}(c)\). These transports are
**vertical**: they act within the fiber over one \(c\). They are not the principal connection
\(\omega\), which compares fibers at *different* base points. The two holonomies that result are
different objects and must not be conflated.

The proposal under investigation is that renormalization in this programme is
agent → meta-agent coarse-graining on that weighted network, with a **species** being a block aligned
in the model channel (\(D_{\rm KL}(s_i\|\widetilde\Omega_{ij}s_j)\approx0\), agents that agree how the
world works) and a **meta-agent** a block aligned in the belief channel
(\(D_{\rm KL}(q_i\|\Omega_{ij}q_j)\approx0\), agents that agree what state it is in).

### 3e.2 Established point-wise (COMPUTED, seed-committed)

**(i) Alignment does not force trivial holonomy; it forces the holonomy into the stabilizer.**
If \(q_i=(\Omega_{ij})_\#q_j\) on every edge of a loop, composing around the loop carries \(q_i\) to
itself, so the loop holonomy satisfies \(H\in\mathrm{Stab}(q_i)\) — and no more. Witness: a 4-agent
\(SO(3)\) block with alignment exact on all four edges to \(10^{-16}\) has
\(\|H-\mathbb 1\|_F=0.0895\), eigenvalues \(\{1,\,0.998\pm0.063i\}\), while
\(\|Hq_0-q_0\|=1.6\times10^{-16}\). The holonomy is invisible to the aligned belief without being
trivial. **The condition is not \(\Omega_{ik}\Omega_{kl}\Omega_{lj}\Omega_{ji}=\mathbb 1\).**

**(ii) \(H\in\mathrm{Stab}(q)\) is exactly what makes coarse-graining well posed.** Two distinct
spanning trees over an aligned block give compressed meta-states agreeing to \(2.0\times10^{-16}\)
relative; breaking alignment on one single chord edge restores tree-dependence at \(0.975\).
**This is the repair for the standing high-severity defect** that `Theory/07b`'s compressed
meta-state is spanning-tree dependent (counterexample at 150% relative difference; centralizer of the
based holonomy group of dimension exactly 1, so no root gauge reconciles two trees).

**(iii) The connection Laplacian is the right operator.** With
\(L^\Omega=D\otimes\mathbb 1-W^\Omega\), \((W^\Omega)_{ij}=\beta_{ij}\Omega_{ij}\) in \(K\times K\)
blocks, the low eigenvector on an aligned block **is** the meta-agent belief: \(|\cos|=1.0\) against
every local \(q_i\) to ten digits. The plain graph Laplacian discards \(\Omega_{ij}\) and cannot see
frustration at all, so it is not the appropriate operator here.

**(iv) Kernel dimension is the wrong diagnostic; \(\lambda_1\) is the order parameter.** A single
\(SO(3)\) cycle always fixes an axis, so a zero mode survives frustration. With two independent
non-commuting cycles the common fixed space is \(\{0\}\) in both regimes, and what separates them is
the magnitude: \(\lambda_1=3.5\times10^{-5}\) near-flat versus \(5.4\times10^{-2}\) frustrated, a
factor \(\sim1500\) at the committed seed.

Consequently **alignment is the trigger and holonomy is the obstruction**, not the other way round:
alignment implies the holonomy condition for free, so no separate holonomy test is needed to decide
when to coarse-grain. What holonomy detects is *failure* — a block with small pairwise KLs but
holonomy outside the common stabilizer is **frustrated**: locally everyone agrees, globally no
consistent meta-belief exists, and further local agreement will not produce one.

**(v) Scope note on B4.** The agent-graph holonomy is observable in a way the base holonomy provably
is not. B4 turns on the connection not being an argument of any generative kernel; but
\(\Omega_{ij}\) appears directly inside the transported KL coupling and inside the tied-replica source
\(u_{ab}=(\Omega_{ab})_\#q_b\). The graph transports **are** kernel arguments by construction, so
B4's hypothesis fails for them without any curve-mediated construction.

**(vi) Structure-group flow.** Alignment forces \(\mathrm{Hol}\subseteq\mathrm{Stab}(q)\), and for a
Gaussian belief \(\mathrm{Stab}(q)=O(K-1)\) at \(\mu\ne0\). Each coarse-graining step therefore
reduces the structure group \(G\to\mathrm{Stab}(q)\), making the RG a flow on structure groups as
well as on laws. This inherits the either/or of §7's obstruction rows: the reduced group is compact,
so a coercive \(\|F\|^2\) becomes available at the meta level exactly where \(D^\omega s=0\), which is
where the base semimetric vanishes.

### 3e.3 The extent question — OPEN

Agents are sections with supports, so a meta-agent formed by coherence at \(c\) is not a point object
either, and §3e.2 says nothing about its extent over \(\mathcal C\). The working hypothesis, **not
established**:

The coherent block is the low-lying spectral subspace of \(L^\Omega(c)\) with spectral projector
\(P(c)\). Spectral subspaces are smooth in \(c\) exactly where their eigenvalues stay isolated, so
smoothness of the meta-agent is a *consequence* of an open gap rather than a hypothesis to impose.
The meta-agent then persists on the connected region where (a) the gap separating its block stays
open and (b) the rate at which parallel transport drags the projector is small against that gap,
\(\|Q\,D^\omega P\|\ll\mathrm{gap}\) with \(Q=\mathbb 1-P\) — an **adiabatic** condition, so the
meta-agent carries a velocity tolerance and not merely a spatial one. Gap closings would then be the
merge/split events, i.e. the RG events proper, and the induced meta-connection would be
\(\nabla^M=P\nabla^\omega P\), whose curvature carries a geometric-phase term (non-abelian
Wilczek–Zee if the coherent subspace is degenerate, abelian Berry if not).

Three wall types are distinguishable and are probably **not** equivalent: the members' supports run
out (\(\bigcap_{i\in I}\mathcal C_i\), a hard combinatorial boundary at which the operator changes
*dimension*, so perturbation theory does not cover it); the gap closes (the genuine RG event); or the
block stays gapped but drifts out of coherence, \(\lambda_1\) rising past threshold with no crossing.
Which binds first is unknown.

Two further possibilities worth testing, both currently CONJECTURED. If the coherent subbundle is
topologically nontrivial over a region, no globally consistent meta-agent exists there *even though
the gap never closes* — a topological answer to the extent question, sharper than any threshold. And
the geometric phase may inherit observability from the graph transports by (v), in which case it
would be the first observable curvature in the programme.

### 3e.4 The most likely failure point

The coarse map is built from the spectral projector of \(L^\Omega\), which depends on \(\beta\). If
the attention rows are **recognition-side** variational parameters, the coarse map is
recognition-**dependent**, and `Theory/09`'s exact contraction theorem — which requires a
recognition-independent \(C_h\) — does not apply. The meta-agent would then be a well-defined
geometric object with no exact ELBO reading, i.e. outside the programme's own typing. This is open
decision 6 (\(\gamma\) recognition-side or generative-side) forced by the RG rather than by the
gradient sector, and it should be settled before anything is built on this construction.

Note also that `.verification/ledger.json` claim `genuine-coupling-before-continuum` (severity
**high**, state INCONCLUSIVE) states that tied product replicas alone cannot generate the required
cross-agent interaction family — which is precisely the coupling a meta-agent needs in order to
exist. If this construction supplies it, that claim closes; if not, the reason will be informative.

### 3e.5 Prior art — assume standard until shown otherwise

None of §3e.2 should be presented as novel without a literature check. The relevant existing
frameworks are cellular sheaves and the sheaf Laplacian (Hansen–Ghrist; \(H^0\) = global sections =
the consensus space, \(H^1\) = the obstruction, which is plausibly what this programme calls
frustration); the connection Laplacian and vector diffusion maps (Singer–Wu); angular synchronization
and its Cheeger-type inequalities (Bandeira–Singer–Spielman), which would supply the quantitative
form of the coherence criterion; the adiabatic theorem with a spectral gap (Kato); Berry and
Wilczek–Zee phases; and von Neumann–Wigner codimension counting for eigenvalue crossings. Laplacian
renormalization for networks (Villegas et al.) and geometric renormalization
(García-Pérez et al.) are adjacent but assume scalar/unweighted diffusion, so their applicability to
gauge-valued transports is exactly what needs checking. **A six-lens panel with adversarial
verification is in flight on all of this** (run `wf_f802b8e6-3c0`; resume with
`Workflow({scriptPath: …/meta-agent-extent-renormalization-wf_f802b8e6-3c0.js, resumeFromRunId: "wf_f802b8e6-3c0"})`).

## 3f. META-AGENT EXTENT — six-lens panel returns, synthesis (2026-08-13)

*Panel `wf_f802b8e6-3c0`, six lenses (`adiabatic-criterion`, `induced-connection`,
`sheaf-and-prior-art`, `elbo-consistency`, `repair-07b`, `obstruction-topology`), each followed by an
adversarial verification pass against its own Proven/Derived claims. This section is the synthesis.*

**Provenance discipline for everything below.** The synthesis author recomputed nothing. Every
numeric in this section is attributed to the lens that produced it, and every such number is
**[Computed on an instance]** — a witness with a stated \(N\), \(K\), \(G\) and base dimension — not
a theorem. Claim tags used throughout: **[Proven]** (a proof is written and its steps are checkable),
**[Derived]** (follows from a stated proven result plus explicitly named hypotheses, no new proof
obligation), **[Computed]** (measured on a specific instance, no generality claimed), **[Suggested]**
(a reading consistent with the evidence that nobody established), **[Conjectured]** (proposed, no
evidence). The only citations asserted below are those the synthesis author verified this session
against the primary source; the ones that could not be verified are named as such in §3f.4.

The one-line verdict: **the working hypothesis of §3e.3 is refuted in its stated form, and no lens
replaced it with a single criterion, because "meta-agent" is currently three different objects with
three different extents.** The refutation of the adiabatic clause is unanimous across four lenses on
two independent grounds. Two clauses survive: the coherent block is a spectral object, and the
induced connection \(P\nabla^\omega P\) is a genuine connection with a nonzero geometric-phase
curvature. Everything else in §3e.3 must be rewritten.

### 3f.0 Retractions and corrections to §3e — do these before reading further

**(R1) §3e.2(iii) is wrong as literally written. [Computed, four lenses independently]** The operator
declared there, \(L^\Omega=D\otimes\mathbb 1-W^\Omega\) with \((W^\Omega)_{ij}=\beta_{ij}\Omega_{ij}\)
and row-simplex \(\beta\), is **not self-adjoint**. Self-adjointness requires
\(\beta_{ij}\Omega_{ij}=(\beta_{ji}\Omega_{ji})^{\mathsf T}\), which under the cocycle
\(\Omega_{ji}=\Omega_{ij}^{-1}\) forces both \(\Omega_{ij}\in O(K)\) and \(\beta_{ij}=\beta_{ji}\);
row-stochastic attention gives neither. Measured relative asymmetry
\(\|L-L^{\mathsf T}\|/\|L\|\): 0.178–0.830 (`adiabatic-criterion`), 0.347 (`sheaf-and-prior-art`),
0.45 (`induced-connection`) — three independent constructions, same conclusion. Consequences: 6 to 14
of 18 eigenvalues complex with \(\max|\mathrm{Im}\,\lambda|=0.5697\), eigenvector condition number up
to 75.4, and \(\min\mathrm{Re}\,\lambda=-0.1466<0\), i.e. **indefinite**. A non-self-adjoint operator
has no orthogonal spectral projector, no variational characterisation of "the low-lying subspace", no
Cheeger inequality, and Hansen–Ghrist Thm 3.1 (\(\ker\Delta^k=H^k\)) does not apply to it. The
correct operator is the one this repository already writes down: the symmetric sheaf energy form
`Theory/09_coarsegraining.tex` `eq:cg-connection-laplacian-energy`,
$$
z^{\mathsf T}L^\Omega(c)\,z=\sum_{e=(i,j)\in E(c)}w_e(c)\,\big\|z_i-\Omega_{ij}(c)z_j\big\|^2 ,
\qquad w_e=\tfrac12(\beta_{ij}+\beta_{ji}),
$$
which is symmetric PSD for **any** \(\Omega\in GL(K,\mathbb R)\), and which coincides with the §3e.2
form to \(8.4\times10^{-17}\) if and only if \(\Omega\in O(K)\) and \(\beta\) is symmetrised
(otherwise the two differ by 19–31%). `docs/verification/meta_agent_coherence_witness.py` must be
re-run against the energy form and §3e.2(iii) amended. Until that is done, §3e.2(iii) and (iv) are
**withdrawn** as stated; §3e.2(i), (ii), (v), (vi) are unaffected because they do not use
self-adjointness.

> **O1 DISCHARGED 2026-08-13.** The witness now assembles the `Theory/09` energy form
> \(z^\top Lz=\sum_e(z_i-\Theta_ez_j)^\top W_e(z_i-\Theta_ez_j)\) — note the \(j\)-diagonal block is
> \(\Theta^\top W\Theta\), not \(W\), which is what makes it PSD off \(O(K)\) — and adds CLAIM 5, a
> four-regime table locating the failure exactly. **The two failure modes are independent**:
> asymmetry is caused by row-stochastic \(\beta\), indefiniteness by \(\Theta\) leaving \(O(K)\).
> Measured: \(SO(3)\) with symmetric weights gives asymmetry \(0.0\) and the two operators are
> **bit-identical** (both \(+5.351372\times10^{-2}\)); \(SO(3)\) with row-simplex \(\beta\) gives
> asymmetry \(0.342\) but stays positive (\(+0.0737\)); \(GL(3,\mathbb R)\) with symmetric weights is
> symmetric but **indefinite** (\(-0.6293\)); both together give \(0.460\) and \(-0.3907\). The energy
> form is PSD in all four (\(\min\) eig \(+3.0\times10^{-2}\) to \(+4.4\times10^{-1}\)).
> **Consequence for the retraction:** §3e.2's claims (iii) and (iv) were computed with \(SO(3)\)
> transports and uniform weights, i.e. in the single cell where the two operators coincide, so their
> *numbers* stand — but only under the narrower hypotheses \(\Theta\in O(K)\) and symmetric weights,
> which §3e did not state. R1's retraction is correct in general and over-broad for this witness; the
> claims are **reinstated with those hypotheses attached**, and the general-\(GL(K)\) case remains
> the energy form's alone.

> **O5 DISCHARGED 2026-08-13, and it repairs O16.** CLAIM 6 of the same witness assembles the pencil
> \((L^\Omega,\bigoplus_i\Sigma_i^{-1})\) with the edge weight taken as the **Fisher metric at the
> endpoint the residual lives in**, \(W_e=w_e\Sigma_i^{-1}\) for \(e=(i,j)\), rather than a scalar.
> Result: the generalized spectrum is **exactly \(GL(K,\mathbb R)\) gauge invariant** — drift
> \(1.0\times10^{-15}\) under a random per-agent \(A_i\in GL(3,\mathbb R)\), against \(1.5\) for the
> scalar weight. The mechanism is that gauge acts by **congruence on both halves of the pencil**:
> with \(z_i\mapsto A_iz_i\), \(\Theta_e\mapsto A_i\Theta_eA_j^{-1}\), \(\Sigma_i\mapsto A_i\Sigma_iA_i^{\mathsf T}\),
> both \(L\) and \(M\) transform as \(X\mapsto A^{-\mathsf T}XA^{-1}\) (residuals \(2.3\times10^{-15}\)
> and \(2.6\times10^{-15}\)), and congruence preserves the generalized spectrum identically.
> Eigenvectors transform as \(v\mapsto Av\) (\(|\cos|=1.000000000000\)). The kernel–holonomy
> isomorphism survives the Fisher weighting: a genuinely parallel section gives
> \(\|Lz\|/\|z\|=1.5\times10^{-15}\) and generalized \(\lambda_1=3.8\times10^{-16}\).
>
> **This overturns the panel's scope restriction.** §3f.1 and O16 record that the criterion is well
> posed only for \(G\le O(K)\). That is a property of the *scalar* weight, not of the construction:
> with the Fisher weight the criterion is well posed for **full \(GL(K,\mathbb R)\)**. O16's
> "transported edge metric \(W_e(c)\)" is therefore not open research — it is \(\Sigma_i^{-1}\), and
> it is already the metric the programme declares on the belief fiber. What remains genuinely open in
> O16 is only the \(c\)-dependence and the model channel.

> **O4 DISCHARGED 2026-08-13, negatively for the proposed repair and positively for the programme's
> own free energy.** CLAIM 7 settles §3f.1 disagreement 2. In the **bare** connection Laplacian a
> support boundary is a genuinely distinct wall: as the departing agent's couplings vanish its
> diagonal block tends to \(0\), injecting \(K\) spurious zero modes that descend into the kernel, so
> the bottom-of-spectrum gap closes in **both** regimes (measured: 6 modes below \(10^{-8}\) at
> \(w_{
m out}=0\) in the flat case, 4 in the frustrated case, against 3 and 1 before departure).
> O4's predicted split — frustrated giving an avoided crossing, flat an exact meeting at the kernel —
> is **not** what happens; both collapse to the kernel.
>
> **The O4 self-anchoring repair does nothing.** A uniform self-weight makes \(L\mapsto L+a\mathbb 1\),
> a pure translation: every gap is unchanged to \(4.4	imes10^{-15}\). It removes the zero crossing
> and leaves the degeneracy exactly where it was.
>
> **What removes the wall is the prior sector the free energy already carries.** The term
> \(\chi_iD_{
m KL}(q_i\|p_i)\) contributes \(lpha_i\Lambda_{p,i}\) on the diagonal, and because
> prior precisions are agent-specific and generically distinct, the departing agent's block tends to
> **its own prior** rather than to zero. Nothing reaches the kernel and the departure becomes a smooth
> limit: \(\lambda_0\) runs \(0.134	o0.100	o0.090\) (flat) and \(0.355	o0.100	o0.090\)
> (frustrated) as \(w_{
m out}	o0\), bounded away from \(0\) throughout.
>
> **Consequence, and it is a correction to this whole section.** The right operator for the extent
> question is the Hessian of the **full** free energy — coupling **plus** prior — not the bare
> connection Laplacian. §3e and §3f both used the bare form. With the prior sector included there is
> no kernel at all, so "\(\lambda_1\) as order parameter" has to be restated relative to the prior
> floor, which is consistent with the panel's independent finding that \(\lambda_1\) carries a
> state-independent floor. The two wall types **do** unify, but through \(\Lambda_{p,i}\), not through
> an ad-hoc self-weight.

**(R2) §3e.2(ii)'s novelty claim is downgraded. [Established elsewhere in this manuscript]** The
tree-free repair for `Theory/07b`'s compressed meta-state is **already proved in this repository** at
two tiers: `Theory/06_general_coarsegraining.tex:561` (`thm:cg-holonomy-kl-marginal`, a path-, root-
and gauge-independent forward-KL coarse score over the holonomy-fixed parent family) and
`Theory/09_coarsegraining.tex:379,447` (\(\ker L_I\cong\mathrm{Fix}(\mathrm{Hol}_r)\) with
tree-independent range of \(\iota_I\)), with the metric-weighted projector \(\Pi_0^R\) and transverse
rate \(\lambda_+\) at `:524-549`. The \(2.0\times10^{-16}\) two-tree agreement of §3e.2(ii) is a
numerical confirmation on an instance, not a new repair. What is genuinely open is only that
`07b` §`sec:rg-gauge-cross-scale` (`:1618-1724`) cites none of it. See §3f.5.

**(R3) The exact condition in §3e.2(ii) is weaker than alignment. [Computed, `repair-07b`]** The tree
ambiguity vanishes identically whenever the *state* is a holonomy-fixed parallel section
\(z\in\ker L_I\), regardless of whether the holonomy is trivial (residual \(1.7\times10^{-15}\)
against a baseline of 0.500). Flatness is sufficient, not necessary.

**(R4) §3e.4's predicted failure point fired. [Computed/Derived, `elbo-consistency`]** The coarse map
built from \(\beta\) *is* recognition-dependent, and this breaks hypothesis H2 of `Theory/09`'s exact
contraction theorem. Within the scope of the closed two-channel theorem \(\beta\) **and** \(\gamma\)
are recognition rows (they appear in the variational family
\(Q_a=\zeta_a\,\beta_{aj}q_a(dx)\,\gamma_{a\ell}s_a(dy)\); see `typed-construction.md`), which settles
`overview.md` §9 open decision 6 *within that theorem's scope* on the recognition side. Building
\(L^\Omega\) from optimised rows \(\beta^{Q^*}\) rather than generative rows \(\beta^{P}\) moved the
Fiedler value by 24.7% on that lens's instance. Separately, the literal map "replace
\(\{q_i\}_{i\in I}\) by a single \(q_M\)" has **infinite** free energy: as a recognition restriction
its exact cost is \(G_{\rm tie}+(r/2)\log(1/\varepsilon)+O(1)\), reproduced to \(2.8\times10^{-14}\)
against `Theory/09` `eq:cg-epsilon-divergence`. The finite object is the *mean tie with free
covariance*, not identification.

**(R5) Ledger drift, reported not repaired.** `.verification/active.json` →
`overview-agent-ontology-final.json` is pinned to `git:43c1342`; `HEAD` is now `9e08c3f` (the panel
dispatch saw `cbacfc6`; the pin is now two commits stale). Not re-pinned, per instruction. Three
lenses reported it independently.

### 3f.1 The criterion, as precisely as the surviving evidence supports

No lens delivered a single criterion, and the reason is structural rather than a failure of effort.
`obstruction-topology` isolated it and it organises the whole panel: **three distinct objects are
being carried under the name "meta-agent", and they have three different extents.**

- **(A) the coherent subbundle** — the spectral projector \(P(c)\) and its image, a rank-\(m\)
  subbundle of \(\bigoplus_i E_i\);
- **(B) a belief representative** — a section or frame of that subbundle, i.e. an actual \(\mu_M(c)\);
- **(C) an ELBO agent** — a normalized law with a variational warrant, which is what
  `overview.md` §2's typing actually demands.

**Criterion for (A). [Derived]** Let \(L^\Omega(c)\) be the symmetric energy form of (R1) on
\(\bigoplus_{i\in A(c)}\mathbb R^K\), and let \(M(c)=\bigoplus_i\Sigma_i(c)^{-1}\) be the Gaussian
mean-sector Fisher metric. Fix \(c_0\) and a subset \(\sigma_{\rm lo}(c_0)\) of the generalized
spectrum of the pencil \((L^\Omega(c_0),M(c_0))\) separated from the rest. Then the coherent
subbundle extends as an analytic rank-\(m\) subbundle over exactly the connected component of \(c_0\)
in
$$
\mathcal E_A(c_0)\;=\;\Big\{\,c\in\textstyle\bigcap_{i\in I}\mathcal C_i\;:\;\sigma_{\rm lo}(c)
\ \text{remains separated from the rest of the generalized spectrum}\Big\},
$$
with \(P(c)\) the Riesz contour integral \(\frac{1}{2\pi i}\oint(\zeta-L)^{-1}d\zeta\), **and no
further condition of any kind.** In particular there is no adiabatic clause. This is Kato's contour
construction plus the pencil covariance of `Theory/08_infogeometry.tex:438`
(`prop:ig-generalized-spectrum-invariance`); the pencil is needed because a passive frame rechoice
\(z_i\mapsto a_i^{-1}z_i\) acts on \(L^\Omega\) by **congruence** \(L\mapsto A^{\mathsf T}LA\), not
similarity, so the ordinary spectrum is not a gauge invariant off \(O(K)\) (`repair-07b`: eigenvalues
shift by 6.77× the entire spectral spread under a \(GL(K)\) rechoice; ordinary projector fails
covariance at 127% of \(\|P\|\); generalized spectrum invariant to \(6.4\times10^{-16}\) and
projector covariant to \(4\times10^{-15}\)). Because \(M\succ0\) and \(L^\Omega\succeq0\), the pencil
is symmetric-definite, so the generalized spectrum is real and "low-lying" is well defined — the
pencil repairs the ordering problem of (R1) and the gauge problem simultaneously. That composite
statement is **[Derived]** from two lenses' separately computed results and was **not itself
recomputed**; it is the single most load-bearing untested assembly in this section.

**Criterion for (B). [Computed, with a proven codimension count]** A global belief representative
over a region \(R\subseteq\mathcal E_A\) exists iff the characteristic class of the block bundle over
\(R\) vanishes, and the degree of that class is \(\mathrm{codim}(\text{crossing locus})-1\): for real
symmetric \(L^\Omega\) (orthogonal transports, real block) crossings have codimension 2 and the
obstruction is \(w_1\in H^1(R;\mathbb Z/2)\); for \(SO(2)\)-valued transports \(L^\Omega\) is secretly
complex Hermitian, crossings have codimension **3** (not 2 — the dispatch's own statement was wrong,
and the correction matters because it fixes which class and which sphere), and the obstruction is
\(c_1\in H^2(R;\mathbb Z)\). Both are exhibited: a 3-agent \(O(2)\) family over \(S^1\) whose gap is
constant at 0.228436 and never closes, yet whose meta-agent belief returns as its own negative,
\(\langle v(2\pi),v(0)\rangle=-1.000000000000\); and a 3-agent \(U(1)\) family with
\(c_1=+1.000000000\) exactly, on spheres of four radii around the flux-\(\pi\) frustration point. So
**a meta-agent can fail to have a globally defined belief on a region where the gap never closes**,
and that failure is invisible to every gap-based criterion. If in addition one wants the
representative to be *approximately parallel*, the right quantity is the scale-invariant accumulated
rotation \(\Theta(\gamma)=\int_\gamma\|D^\omega P\|\,ds\) along a path, with the covariant Kato bound
\(\|D^\omega P\|\le\|Q(D^\omega L)P\|/\mathrm{gap}\) verified at ratio 0.374–0.856 over 8 base points.
The threshold on \(\Theta\) — \(\pi/2\), 1, or something derived from free energy — is **not settled
by anything in this panel**, so the "extent" it defines is currently a free parameter.

**Criterion for (C). [Computed on the Gaussian tier / Derived there]** The spectral construction does
not deliver an ELBO agent and cannot be patched into one by any step this panel found. What does
deliver one is a different operation entirely: coarse-graining by **recognition-family restriction**,
the third of `Theory/06`'s three operations and the only one that keeps the fixed joint and the same
evidence. For a Gaussian posterior \(\mathcal N(\mu,\Lambda^{-1})\) and the partition-structured
family \(\mathcal F_P=\{\mathcal N(\nu,\Sigma):\nu\in\mathrm{range}(S_P),\ \Sigma\ \text{block-diagonal
over }P\}\), the mean and covariance sectors decouple exactly and the excess negative ELBO is
$$
G(P)\;=\;G_{\rm tie}(P)+G_{\rm fact}(P),
$$
`Theory/09`'s own two quantities **with unit coefficients**, verified to \(4.4\times10^{-15}\) across
all 203 partitions of six agents. \(G_{\rm tie}\) increases under merging, \(G_{\rm fact}\) decreases
(Fischer 1908), and their coefficient-free sum is nonmonotone with an interior argmin that recovers
planted block structure. The extent is then
\(\mathcal E_C(P)=\{c:P\ \text{remains the argmin of}\ G(\cdot;c)\}\), and the RG events are
**transversal crossings of two smooth free-energy branches** (slope difference 15.2 at
\(c^\*=0.8478\)) — a first-order transition in a discrete label. On that instance \(\lambda_1\) of the
coupling operator was **constant at 0.400 straight through the event**.

**Where the lenses disagree, and why — not averaged.**

1. *Does the support bind?* `adiabatic-criterion` measures the support as the **widest** candidate
   extent and concludes it never binds: about \(c_0=2.0\) on an 8-agent \(K=3\) \(SO(3)\) witness over
   a 1-D base the four candidates order strictly as support \([1.10,3.90]\supset\) gap\(>\!0.25\)
   \([1.60,3.75]\supset\) \(\|D^\omega P\|<1\) \([1.50,3.10]\supset\) two-meta-agent decomposability
   \([1.50,2.30]\), with the \(\lambda_1\)-sublevel set \([1.10,2.55]\) nested in none of them; the
   binding constraint is adiabatic/decomposability at \(c\approx3.10\), 30% of the support width
   before any support boundary. `obstruction-topology` concludes the opposite, that support
   boundaries dominate: at \(\partial\mathcal C_i\) the departing weights \(\beta_{i\cdot}\to0\), the
   \(i\)-block decouples and contributes \(K\) eigenvalues descending **linearly** (measured
   \(\mathrm{gap}=4.000\times10^{-3}\) at \(\varepsilon=10^{-3}\) and \(4.000\times10^{-6}\) at
   \(\varepsilon=10^{-6}\), exactly \(3\varepsilon\)), and \(\{\beta_{i\cdot}(c)=0\}\) is **one**
   equation, hence codimension 1, hence it disconnects \(\mathcal C\). These are not in conflict once
   the questions are separated: only codimension-1 loci can *topologically bound* an extent, and both
   lenses agree independently that for a strictly positive softmax \(\beta\) the only reachable
   codimension-1 loci are the support boundaries themselves; but in the measured witness the extent is
   *metrically* bounded strictly inside the support by a soft condition that disconnects nothing. Both
   are right about their own quantity. **Resolution: the support boundary is the only wall that can
   bound the extent topologically, and it does so by acting through the parallelism condition, not
   through the gap.**
2. *Is the active-set change a level crossing?* `adiabatic-criterion` says no: softening the support
   embeds the varying-dimension family in a fixed \(\mathbb R^{NK}\), and the event is an **avoided**
   crossing with minimum gap \(1.179\times10^{-2}\), stable to within 27% over a 16× sweep of the
   departing agent's coupling amplitude, with the hard-truncated operator the exact limit of the soft
   one (spectral difference \(4.4\times10^{-15}\)); the obstruction that actually bites is the
   adiabatic one (\(\|D^\omega P\|\) spikes to 3.507 while the gap is still 0.311) at
   \(c^\*=3.5300\), 15.7% of the support width inside the support. `obstruction-topology` says the gap
   closes exactly linearly. The reason for the disagreement: they measure **different gaps**.
   `obstruction-topology` measures the bottom-of-spectrum gap of the full operator, which does go to
   zero because \(0\) always sits at the bottom of a Laplacian's spectrum where the coherent block
   lives; `adiabatic-criterion` measures the block-edge gap between the coherent block and the
   descending modes, which has a positive minimum. **[Suggested]** the two agree once one asks whether
   the coherent block itself has a zero mode at the wall: if the block is frustrated
   (\(\lambda_1>0\)) the descending modes pass below it and the event is an avoided crossing plus a
   relabelling of "low-lying"; if the block is flat (\(\lambda_1=0\)) they meet the kernel exactly.
   Nobody tested that. It is obligation O4.
3. *Codimension of the gap-closing locus.* Three answers, all correct in their own regime, and the
   regime is fixed by the structure group and by the mechanism. Generic crossings inside the
   real-symmetric stratum: codimension 2 (von Neumann–Wigner; `sheaf-and-prior-art` confirms by a GOE
   gap-cumulative exponent of 2.128 against the predicted 2). Complex Hermitian (\(SO(2)\) links):
   codimension 3 (`obstruction-topology`, by orbit-dimension count and by exhaustive search — 0.00 of
   random 2-parameter Hermitian families reach a crossing, 0.97 of 3-parameter families do).
   Non-generic *coupling-vanishing* loci, where one scalar weight gates a whole \(K\)-dimensional
   sector: codimension 1 (`adiabatic-criterion`, on a \(105\times40\) grid the curve
   \(w_{\rm out}(c,b)=0\) has gap \(\equiv0\) to \(5.7\times10^{-16}\) along it and minimum gap
   \(1.66\times10^{-2}\) off it). Non-normal \(L^\Omega\) for \(G\not\le O(K)\): the repeated-eigenvalue
   locus is the zero set of one real discriminant, again codimension 1, and there the individual
   eigenprojector **diverges**, \(\mathrm{gap}\asymp C\,\mathrm{dist}^{1/2}\),
   \(\|P\|\asymp C'\mathrm{dist}^{-1/2}\) (`induced-connection`, measured \(C=1.087\),
   \(C'=0.1611\)). **Consequence that no averaging can soften: for \(\dim\mathcal C\ge3\) the
   codimension-2 and -3 crossing loci have connected complement, so they can never disconnect the base
   and never bound an extent.** They can only generate \(\pi_1\) and a holonomy. The
   "gap closings are the RG events" clause of §3e.3 is therefore refuted as the *dominant* mechanism
   even where it is not refuted outright.
4. *What the order parameter measures.* `sheaf-and-prior-art` supplies the quantitative criterion the
   programme was asking for — the Bandeira–Singer–Spielman two-sided bound (below) — while
   `adiabatic-criterion` and `elbo-consistency` independently show \(\lambda_1\) is the **wrong**
   order parameter for coherence: it is a functional of \((\beta,\Omega)\) alone and is exactly blind
   to the belief section. It carries a state-independent quadratic floor
   \(\lambda_1\approx0.0399\,\|\log\Omega\|_F^2\) (\(K=3\), random \(GL(3,\mathbb R)\) on 8 edges;
   \(0.029\) for the matched \(SO(3)\) control, so not a \(GL\) artefact), so
   \(\{\lambda_1<\varepsilon\}\) is a **holonomy-magnitude test**, globally empty once
   \(\overline{\|\log\Omega\|}_F\gtrsim0.50\) at \(\varepsilon=10^{-2}\), no matter how well the
   agents agree; and `elbo-consistency` exhibits \(\lambda_1=0\) with the information residual rising
   without bound (0.1116 → 0.8047 → 2.3076). These are consistent: BSS bounds \(\lambda_1\) against
   *frustration of the transport system*, which is exactly what it measures, and that is not agent
   coherence. `Theory/09` already records the same limitation for the holonomy-fixed rank \(f_I\)
   ("a state-independent structural admissibility criterion … it does not require the constituent
   belief means to coincide"); this panel extends it from the kernel dimension to the bottom
   eigenvalue.
5. *Is \(\varepsilon\) an RG scale?* No, and the failure is not marginal. Structurally, if
   \(L^\Omega\) is exactly block-diagonal for a partition then every spectral projector is, so the
   exact decomposition is a property of \(L^\Omega\) alone and carries no \(\varepsilon\)-dependence.
   Empirically, against a tolerance \(\delta=0.08\), raising \(\varepsilon\) **refines** the induced
   partition (at \(c=1.6\): \(\{\rm ALL\}\to\{A|B\}\to\{013|B|2\}\to\{01|23|B\}\), three splits, zero
   merges) — the opposite of coarsening — and monotonicity fails outright at \(c=2.4\), where the
   sequence is \(\{\rm ALL\}\to\{A|B\}\) at \(\varepsilon=2.300\to\{\rm ALL\}\) at
   \(\varepsilon=3.982\). **There is no dendrogram.**

**What survives of §3e.3 verbatim, and it is exactly one clause.** The induced meta-agent connection
is \(\nabla^M=P\nabla^\omega P\) and its curvature carries a geometric-phase term. This is
**[Proven]** as a connection and **[Derived]** as a Gauss equation, and **[Computed]** as nonzero:
see §3f.2 step 4.

### 3f.2 The construction, in order, each step with its status

**Step 1 — the \(c\)-varying family. [Derived; the definition is a declaration, the properties are
proved]** Over a base \(\mathcal C\) with active set \(A(c)=\{i:c\in\mathcal C_i\}\), define
\(L^\Omega(c)\) by the sheaf energy of (R1), with \(w_e(c)=\tfrac12(\beta_{ij}(c)+\beta_{ji}(c))\)
and \(\Omega_{ij}(c)=\varphi_i(c)^{-1}\tau_{ij}(c)\varphi_j(c)\). This form is symmetric PSD for any
\(\Omega\in GL(K,\mathbb R)\). Pair it with \(M(c)=\bigoplus_i\Sigma_i(c)^{-1}\) and work with the
pencil. **Hypotheses consumed, one of them not granted by the programme:** (i) the fibre is
\(\mathbb R^K\) carrying the *defining* representation, i.e. this is the \(\mu\)-channel only — the
\(\Sigma\)-channel needs a different Laplacian on \(\mathbb R^{N\cdot K(K+1)/2}\) built from
\(\rho_{\mathrm{Sym}^2}(\Omega)\), with a different rank and a different gap locus; (ii) \(L^\Omega\)
is a Fisher/KL object **only** under the shared-covariance hypothesis of
`Theory/08_infogeometry.tex:239-256` — outside it \(L^\Omega\) is not the Hessian of any divergence
and the spectral construction has no information-geometric warrant, which `08:253-255` states in
terms; (iii) under that same hypothesis the pairwise KL is *symmetric*, so the quadratic form is
**blind to the coupling contract's slot order** \(E_{ij}=D(q_i\|(\Omega_{ij})_\#q_j)\) — the
directedness first appears in the log-det/trace terms the hypothesis deletes.

**Step 2 — the coherent subspace. [Derived on the compact tier; open on the \(GL\) tier]** Take the
low-lying part of the generalized spectrum of \((L^\Omega(c),M(c))\). On the compact tier this is the
ordinary low-lying spectral subspace and the BSS machinery applies. Off it, only the pencil is
well-typed, and even then Hansen–Ghrist prove the Cheeger route does not extend to non-invertible
restriction maps (§3f.4), so the two-sided guarantee is lost precisely where `Theory/09`'s
coarse-graining category (unequal vertex dimensions, \(GL(V_I)\) automorphisms) wants to live.

**Step 3 — the projector. [Derived]** \(P(c)\) is the Riesz contour integral, analytic on the whole
gap-open region with no smallness hypothesis. Its derivative obeys the covariant Kato formula
\(D^\omega P=\frac{1}{2\pi i}\oint R\,(D^\omega L)\,R\,d\zeta\), proved algebraically and verified to
\(2.0\times10^{-10}\) against central differences (`adiabatic-criterion`). Persistence under a base
increment is Davis–Kahan, \(\|\sin\Theta(P(c),P(c+\delta))\|\le\|\delta L\|/\mathrm{gap}\), verified
7/7 with 2–15× slack. **The adiabatic clause of §3e.3 is refuted here, twice over.** It is not
scale-invariant: rescaling every edge weight by 100 leaves \(P\) and \(\|D^\omega P\|=0.266634\)
bit-identical while the gap goes \(1.67771\to167.771\), driving the ratio from 15.893 to 0.001589 for
identical geometry (`adiabatic-criterion`); independently, \(\beta\to s\beta\) leaves \(P\) and the
second fundamental form exactly invariant while scaling every gap by \(s\) (gap
\(0.602707\to6.027068\) for \(s=0.5\to5.0\), \(P\) unchanged; `induced-connection`). And it is
unnecessary: \(\|dP\|\le\|dL\|/\mathrm{gap}\) makes it a *consequence* of the gap plus a bound on
\(\|dL\|\), verified across gap 1.438 down to 0.123 with \(\|dP/dc\|=2.12\!-\!5.23\) against bounds
\(8.74\!-\!102.15\) (`sheaf-and-prior-art`); and the ratio was measured at 115.6 while the projector
was converging with \(\|P(s)-P(s/2)\|=1.5\times10^{-4}\) (`obstruction-topology`). **There is also no
adiabatic theorem available to invoke.** Kato 1950 and its descendants govern an evolution
*generated by the gapped operator*; here \(L^\Omega\) supplies the gap and \(\omega\) generates the
transport, there is no \(T\) and no rate parameter to send to zero. The exact unconditional
replacement is step 4.

**Step 4 — the induced connection. [Proven, Derived, Computed — in that order]**
**[Proven]** For any smooth field of idempotents \(P\) of constant rank in a bundle with connection
\(\nabla=d+A\), \(\nabla^M:=P\nabla P\) is a genuine connection on \(\mathrm{im}\,P\): it is
\(C^\infty\)-linear in \(X\) and satisfies Leibniz, \(\nabla^M_X(fs)=(Xf)s+f\nabla^M_Xs\) using
\(Ps=s\). No fibre metric, no orthogonality of \(P\), no self-adjointness of any generating operator
is consumed — so the construction survives the live oblique Riesz projector of (R1). Leibniz residual
\(\le1.8\times10^{-12}\).
**[Derived]** With \(\mathrm{II}:=Q(\nabla P)P\) and \(\mathrm{II}':=P(\nabla P)Q\), one has
\(P(\nabla P)P=0\) identically and the exact Gauss equation
$$
F^M \;=\; P F^\omega P \;+\; \mathrm{II}'\wedge\mathrm{II},
\qquad\text{with Codazzi}\quad Q(d^\nabla \mathrm{II})P \;=\; Q F^\omega P,
$$
verified to \(4.8\times10^{-10}\) relative with an oblique projector, Codazzi residual
\(4.0\times10^{-10}\) against magnitude 4.04. Two consequences. First, **leakage out of the coherent
subbundle along \(\gamma\) is exactly \(\int\|\mathrm{II}(\dot\gamma)\|\)** — an identity, needing no
smallness hypothesis, and this is what replaces the refuted adiabatic condition. Second, an
obstruction theorem: **if \(QF^\omega P\ne0\) at any \(c\), no coherent subbundle of that rank is
parallel near \(c\).** Nobody has computed \(QF^\omega P\) on an actual programme configuration.
**[Computed]** The geometric-phase term is real and nonzero with ambient curvature and ambient
holonomy exactly zero: on a 5-agent \(SO(3)\) cycle with \(A\equiv0\), \(\|F^M\|=1.78\times10^{-2}\)
and \(\|\mathrm{Hol}^M-\mathbb 1\|=6.60\times10^{-3}\), orthogonal to \(6.9\times10^{-11}\), with
\(\mathrm{tr}\,\mathrm{Hol}^M\) invariant to \(7.2\times10^{-12}\) under a **noncompact**
\(GL(3)^5\) gauge of condition number 20.3. Independently, Kato transport around loops of radius
0.20/0.10/0.05 in a 2-D base gives \(\|H-\mathbb 1\|/\mathrm{area}=0.012572/0.012247/0.012142\)
(Richardson limit 0.012107) against the local Wilczek–Zee curvature
\(\|P[D_cP,D_bP]P\|_F=0.010932\) — area-proportional and matching to 11%.
**Three fences on this, all load-bearing.** (a) *The user's own guess — that the criterion is
smoothness of the induced connection from \(c\) to \(c+dc\) — is refuted by direct control:* in the
exactly-parallel configuration \(\|dP\|=2.6323\), the projector moves at \(O(1)\), while
\(\|\mathrm{II}\|=1.2\times10^{-10}\); the vanishing is a cancellation between \(dP\) and \([A,P]\).
Smoothness of \(P\) is generic and carries no information. The criterion is the covariant
\(\mathrm{II}=0\), which holds exactly iff the pulled-back per-agent forms
\(\alpha_i:=U_i^{-1}A^{(i)}U_i+U_i^{-1}dU_i\) all coincide (spread \(1.7\times10^{-14}\) with
\(\|\mathrm{II}\|=1.2\times10^{-10}\), versus spread 2.34 with \(\|\mathrm{II}\|=1.86\) in the
control). (b) *"An exactly parallel meta-agent has no informational geometry" is false for rank
\(\ge2\):* subbundle-parallel (\(\mathrm{II}=0\)) is strictly weaker than section-parallel
(\(D^\omega s=0\)); with a common nonzero \(\alpha\) (\(\|\alpha\|=1.1459\)) one gets \(F^M=F^\alpha\)
with \(\|F^\alpha\|=0.3267\) and \(h^\omega_{\rm meta}\ne0\). The two coincide only at rank 1. (c)
*For a real rank-1 block there is no geometric-phase curvature at all:* \(\langle v,v\rangle=1\)
forces \(\langle v,dv\rangle=0\), so \(P\nabla P\) on a real line subbundle is identically flat and
its entire content is the \(\mathbb Z/2\) monodromy. "Berry-type" is correct only in the complex or
rank-\(\ge2\) sector, and there the right name is **Wilczek–Zee**, not Berry.

**Step 5 — the walls. [Computed; codimension counts Derived]** Four wall types, not equivalent, and
the panel's own numbers place them:

| Wall | Locus | Codim | Disconnects \(\mathcal C\)? | Status |
|---|---|---|---|---|
| Support boundary (coupling vanishes) | \(\{\beta_{i\cdot}(c)=0\}=\partial\mathcal C_i\) | 1 | **Yes** | Computed: gap \(=3\varepsilon\) over six decades; block-edge crossing avoided, min \(1.179\times10^{-2}\) |
| Generic crossing, real symmetric | von Neumann–Wigner seam | 2 | No (for \(\dim\mathcal C\ge3\)) | Derived; GOE exponent 2.128 vs 2 |
| Generic crossing, complex Hermitian (\(SO(2)\) links) | diabolical point | 3 | No | Derived + exhaustive search |
| Non-normal discriminant (\(G\not\le O(K)\)) | real discriminant zero set | 1 | **Yes** | Computed: 83.1% of a one-parameter loop had complex spectrum, 10 wall crossings |
| Structure-group jump \(\mathrm{Stab}(q):O(K\!-\!1)\to O(K)\) | \(\{\mu(c)=0\}=\{r(c)=0\}\) | \(K\) | No for \(\dim\mathcal C<K\) | Derived |

Two riders. Kato's refinement rescues part of the RG-event picture: the **total** projector for a
group of eigenvalues stays bounded and analytic through a crossing *internal to the group*
(\(\|P_2\|_2=1.000078\) measured through an exceptional point), so only **boundary-traversing**
crossings can be RG events; §3e.3 conflates the two. And the merge of two meta-agents, when it
happens, is not a spectral event at all: it is a continuous crossover of the block-decomposability
residual \(r(\Pi)=\|P-\sum_{I\in\Pi}\Pi_I P\Pi_I\|_F/\|P\|_F\), rising \(0.0304\to0.2668\) **while the
gap is at its maximum** (\(0.258\to1.755\to0.582\)).

### 3f.3 Hypotheses consumed, including those the programme has not granted

Granted by the programme and used freely: finite fixed \(N\); agents are sections over supports
\(\mathcal C_i\subseteq\mathcal C\), so \(A(c)\) is \(c\)-dependent; \(\beta_{ij}(c)\) simplex-valued
and strictly positive (softmax); \(\Omega_{ij}(c)\) invertible fibre maps at fixed \(c\); the
Gaussian backend for the \(\mu\)-sector.

**Not granted, and each one is load-bearing.**

1. **\(G\le O(K)\), i.e. compactness.** Every spectral statement in §3f.1–§3f.2 outside the Fisher
   pencil requires it. The sheaf energy uses the Euclidean fibre norm, invariant under
   \(z_i\mapsto g_iz_i\) iff every \(g_i\) is orthogonal; under a \(GL(K)\) rechoice the block gap
   shifts 1.45%/8.0%/16.5%/25.9% and \(\lambda_1\) by 0.88%/1.57%/16.1%/47.5% at
   \(\|\log g\|_F=0.074/0.149/0.297/0.594/1.188\), while an \(SO(3)\) rechoice leaves the energy
   exactly invariant. `overview.md`'s standing convention *recommends* compact \(G\) but the declared
   typing is \(G\le GL(K,\mathbb R)\); this panel's results are compact-\(G\) results unless the
   Fisher pencil is adopted. This is the finite-dimensional shadow of the settled Yang–Mills row (no
   positive-definite \(\mathrm{Ad}\)-invariant form on \(\mathfrak{gl}(K,\mathbb R)\)).
2. **A fibre metric making \(L^\Omega\) self-adjoint** — see (R1). Not declared anywhere.
3. **Symmetrised attention**, \(w_e=\tfrac12(\beta_{ij}+\beta_{ji})\). The energy form imposes it;
   the declared typing does not supply it, and `Theory/07b:1748` explicitly declares \(\beta\) a
   *row-stochastic conditional law*. Symmetrising is a modelling decision with no stated warrant.
4. **The shared-covariance hypothesis** `Theory/08:239-256`. Without it \(L^\Omega\) is not the
   Hessian of a divergence. With it, the quadratic form cannot see the directed slot order of the
   coupling contract.
5. **A declared representation channel.** The construction is \(\mu\)-only. \(\mu\)-channel and
   \(\Sigma\)-channel Laplacians on the same graph give \(\dim\ker\) 1 vs 2 at twist 0.45 and
   reorganise their block boundary at different twists (index 8 vs 9 at twist 1.6). For orthogonal
   links \(\mathrm{Sym}^2\) contains the trivial representation, so the \(\Sigma\)-channel carries a
   permanent extra coherent mode (the trace/scale direction) that is an artefact of the representation
   and not a coherence fact about the agents. The model channel \((\gamma,\widetilde\Omega)\) is a
   third, independent extent.
6. **A normalization lift from the eigen-ray to a law.** The low eigenvector is defined up to scale,
   so the construction yields a section of a *projectivised* bundle, not a point of a fibre of
   normalized laws. This is not cosmetic: by `wave2-01` Cor A3.5 the entire gauge-invariant content of
   one belief section is \(r=(\mu^{\mathsf T}\Sigma^{-1}\mu)^{1/2}\), which is exactly homogeneous of
   degree 1 in the eigenvector's normalisation (measured 0.400768 / 1.482843 / 0.801537 for scalings
   \(1/3.7/-2\)) — **the one quantity the meta-agent could carry as an invariant is precisely the one
   the spectrum does not fix.** Any norm-based lift is a gauge fixing to \(O(K)\), and the programme's
   own coercivity lemma forbids a \(GL(K)\)-invariant one.
7. **Recognition-independence of the coarse map** (`Theory/09`'s H2). Fails — see (R4).
8. **Real-analyticity of \(c\mapsto L^\Omega(c)\).** Local finiteness of the multiplicity
   stratification needs it (Łojasiewicz–Hironaka); for merely smooth dependence the degeneracy locus
   can be an arbitrary closed set and there is no stratification at all. Nowhere established.
9. **A cocycle for the induced meta-agent transports.** The natural projected family
   \(\Omega^{\rm meta}_{\alpha\beta}=P_\alpha\Omega P_\beta\) does **not** compose — median 0.90
   relative failure even when the ambient family composes exactly — and is undefined across a rank
   change. So the meta-agent is one type short of an agent: it is a section of a projectivised bundle
   with a well-defined \(GL(K)^N\)-covariant connection and a gauge-invariant holonomy trace, and that
   is all.
10. **A typing contradiction that has to be resolved before any of this is meaningful.**
    `overview.md` §2 declares \(\Omega_{ij}(c)\) to be fibre maps between frames **at the same base
    point**. Read literally that makes \(\Omega_{ij}=\varphi_i^{-1}\varphi_j\) a coboundary, which
    forces trivial agent-graph holonomy — contradicting §3e.2(i)'s \(\|H-\mathbb 1\|_F=0.0895\).
    Either the agents carry distinct principal bundles over \(\mathcal C\), or the graph transports
    carry content beyond frame change (as `adiabatic-criterion` writes them,
    \(\Omega_{ij}=\varphi_i^{-1}\tau_{ij}\varphi_j\) with a genuine \(\tau\)). **Under the first
    reading the entire agent-graph holonomy and geometric-phase construction is empty.** This is
    cheap to settle and nothing should be built until it is.

### 3f.4 Prior art — what is standard, and what if anything is new

This repository has been burned by presenting a rediscovery as a contribution. The following is
stated bluntly. **Almost the entire construction of §3e.2 and §3e.3 is standard mathematics under
names this programme was not using.** Citations below were checked this session against the primary
source unless marked otherwise.

*Standard, verified this session:*

- **The object itself.** An agent graph with a \(K\)-dimensional stalk per agent and invertible
  orthogonal edge transports *is* a cellular sheaf / discrete \(O(K)\)-vector bundle, and \(L^\Omega\)
  is its degree-0 sheaf Laplacian. Hansen & Ghrist, *Toward a Spectral Theory of Cellular Sheaves*,
  arXiv:1808.01513, §3.6 ("Comparison with Previous Constructions", p. 17 of the v2 PDF), verbatim:
  *"The graph connection Laplacian, introduced by Singer and Wu in [SW12], is simply the sheaf
  Laplacian of an \(O(n)\)-vector bundle over a graph."* Published as J. Appl. Comput. Topology
  3(4):315–358 (2019). **`Theory/09_coarsegraining.tex:334-336` already cites `HansenGhrist2019`** —
  the repository already knew this and §3e.2(iii) restated it as a discovery.
- **The connection Laplacian.** Singer & Wu, *Vector Diffusion Maps and the Connection Laplacian*,
  Comm. Pure Appl. Math. 65(8):1067–1144 (2012), doi:10.1002/cpa.21395.
- **"The low eigenvector is the meta-agent belief"** is Singer's spectral relaxation for
  synchronization.
- **"\(\lambda_1\) is the order parameter, not the kernel dimension"** is the
  Bandeira–Singer–Spielman frustration constant, \(\eta(x)=\langle x,Lx\rangle/\langle x,Dx\rangle\),
  with the **two-sided** guarantee this programme is not yet using:
  \(\lambda_1(L)\le\min_{\|x_v\|=1\ \text{or}\ 0}\eta(x)\le\sqrt{10\,\lambda_1(L)}\).
  Bandeira, Singer & Spielman, *A Cheeger Inequality for the Graph Connection Laplacian*, SIAM J.
  Matrix Anal. Appl. 34(4):1611–1630 (2013), arXiv:1204.3873; reproduced as Hansen–Ghrist eq. (7.1),
  p. 33 of the v2 PDF, verified verbatim this session. Instance check: \(0.0983\le0.3897\le0.9915\).
- **§3e.2(i) is \(H^0\) of a local system.** "Belief alignment forces \(H\in\mathrm{Stab}(q_i)\), not
  \(H=\mathbb 1\)" is precisely \(\dim H^0\ge1\), i.e. \(H^0=\) the monodromy invariants (verified:
  \(\dim\ker=\dim\) invariant subspace exactly, 3 vs 3, 1 vs 1, 0 vs 0 across flat, common-axis and
  generic bundles).
- **Limits of the Cheeger machinery.** Hansen–Ghrist §7.1 prove the rounding approach does **not**
  extend to restriction maps that are merely partial isometries, with an explicit two-vertex
  counterexample (\(\mathcal F(v_1)=\mathcal F(v_2)=\mathbb R^2\), \(\mathcal F(e)=\mathbb R\),
  \(\mathcal F_{v_1\trianglelefteq e}=[1\ 0]\), \(\mathcal F_{v_2\trianglelefteq e}=[\tfrac12\
  \tfrac{\sqrt3}{2}]\)), verified verbatim in the v2 PDF this session. So the quantitative extent
  criterion is available **only** while \(\Omega_{ij}\) stays invertible-and-orthogonal; the moment
  the programme moves to \(G\le GL(K,\mathbb R)\), or to the non-invertible coarse-graining maps of
  `Theory/09`'s own category, the two-sided guarantee is not merely unproven — the standard proof
  route is known to fail.
- **Crossing codimension.** von Neumann & Wigner, *Über das Verhalten von Eigenwerten bei
  adiabatischen Prozessen*, Physikalische Zeitschrift 30:467–470 (1929).
- **Projector persistence.** Davis & Kahan, *The Rotation of Eigenvectors by a Perturbation. III*,
  SIAM J. Numer. Anal. 7(1):1–46 (1970), doi:10.1137/0707001.
- **The geometric phase.** For a degenerate block it is Wilczek & Zee, *Appearance of Gauge Structure
  in Simple Dynamical Systems*, Phys. Rev. Lett. 52(24):2111–2114 (1984). Berry (1984) and Simon
  (1983) are the abelian Hermitian *line*-bundle case and are the **wrong** citation for a rank-\(m\)
  coherent block.
- **The adiabatic theorem, and why it does not apply.** Kato, *On the Adiabatic Theorem of Quantum
  Mechanics*, J. Phys. Soc. Japan 5:435–439 (1950), doi:10.1143/JPSJ.5.435, is a theorem about a
  unitary evolution \(U_T(s)\) generated by a time-dependent Hamiltonian, concluding
  \(\lim_{T\to\infty}(1-P(s))U_T(s)P(0)=0\). This programme has no dynamics on \(\mathcal C\).
  Should a dynamics ever be declared, the applicable theorem is Avron, Fraas, Graf & Grech,
  *Adiabatic Theorems for Generators of Contracting Evolutions*, Comm. Math. Phys. 314(1):163–191
  (2012), arXiv:1106.4661 — **not** Kato 1950, not Avron–Seiler–Yaffe, not Nenciu.

*Standard, content confirmed by recomputation but citation NOT verified against the primary text:*

- **Kato's Riesz total projection**, its analyticity on the gap-open region, and the derivative
  formula: content verified numerically to \(3.4\times10^{-15}\) / \(2.0\times10^{-10}\), but Kato,
  *Perturbation Theory for Linear Operators* is paywalled and web search returned only chapter titles.
  Anyone writing this up must open the book. In particular whether **Rellich's theorem** (analytic
  eigenvalues and eigenprojections for a self-adjoint holomorphic family of *one* real variable, valid
  *through* crossings) is Ch. II §6 is unverified — and it matters, because in a 1-D base it says the
  projector families continue analytically through a crossing, weakening "gap closings bound the
  extent" further still.
- Herzberg–Longuet-Higgins \(\mathbb Z/2\) sign change on encircling a conical intersection (measured
  exactly \(-1.0\) on the canonical example); Whitney (b) regularity of orbit-type stratifications for
  proper Lie group actions; Milnor (1976) on the nonexistence of a bi-invariant metric on
  \(GL^+(K)\) (cited by one lens as Lemma 7.5 — **lemma number unverified**, paper confirmed as *Adv.
  Math.* 21(3):293–329); Neal & Hinton (1998) for partial coordinate updates; Bishop ch. 10 / Beal
  (2003) for structured variational families; Fischer (1908) for the determinant inequality behind
  \(G_{\rm fact}\)'s monotonicity.

*Candidate new content — and it is thin. None of it is spectral.*

1. **The stalk is a normalized probability law with a transported-KL edge discrepancy**, rather than a
   vector with a Euclidean one, and the doubling into belief \((\beta,\Omega)\) and model
   \((\gamma,\widetilde\Omega)\) channels on one graph. **Do not claim this.** Hansen–Ghrist §3.6
   cites `[Gao16]` as using "a sheaf Laplacian-like construction to study noninvertible
   correspondences between probability distributions on surfaces"; nobody retrieved it. Obligation
   O11.
2. **The Fisher pencil \((L^\Omega,\bigoplus_i\Sigma_i^{-1})\)** as the gauge-invariant replacement
   for the ordinary spectrum. This is an *application* of `Theory/08:438`
   `prop:ig-generalized-spectrum-invariance` to the connection Laplacian, not a new theorem. Its
   value is that it repairs \(GL(K)\) non-invariance and spectral reality at one stroke; it is
   recombination.
3. **\(G(P)=G_{\rm tie}(P)+G_{\rm fact}(P)\) with unit coefficients** as the exact excess VFE of the
   partition-structured Gaussian recognition family, and the observation that the coefficient-free sum
   is nonmonotone with an interior argmin. This supplies exactly the "different nonmonotone
   functional" that `Theory/09:1013-1019` records as **OPEN**, and is the one item in this panel that
   looks like a genuine contribution. It is Gaussian-tier only.
4. **A fixed sector with nonzero interaction coordinate**: the massless connection-Laplacian Gaussian,
   whose decimation closes exactly on the family (\(3\times10^{-11}\) relative), preserves holonomy to
   \(3.3\times10^{-16}\), and flows by \(r'=r^2+4r\) in \(r=m/w\), giving relevance exponent
   \(y=\log_2 4=2\) at block factor 2, with the transport itself as the pair Hoeffding coordinate
   \(w\Theta_{ij}\). Fences: it is a fixed **ray**, not a fixed measure pair (`07b`
   `eq:rg-fixed-action-ray`, and `07b:2660-2662` says the ray tier is strictly weaker); at \(m=0\) the
   law is improper on \(\ker L\) and needs a declared pin; exhaustiveness needs a declared self-similar
   graph identification (`07b:2716-2718`); and \(y=2\) is convention-relative in the sense of
   `07b:2689-2694`. It is a **partial** discharge of the ledger claim `genuine-coupling-before-continuum`
   — one Gaussian instance, action tier, fixed ray only — and must be recorded as such, not as a
   closure. It is also invisible to `07b`'s own declared interaction Banach space
   \(\mathcal G_\ell=\bigoplus_A P_{\ell,A}L^\infty(\nu_\ell)\), because the pair coordinate
   \(g_{ij}(z)=\Lambda_{ij}z_iz_j\) is unbounded and therefore not an element of it — the same norm
   separation `07b:812-819` already flags.

Everything else — the families-over-a-base indexing, extent-as-gap-open-region, the projected
connection, the geometric-phase term, the \(\varepsilon\)-threshold hierarchy, the merge/split
structure — is recombination of the standard material above. On network renormalization specifically:
neither Laplacian RG (Villegas et al.) nor geometric RG (García-Pérez et al.) applies as-is, because
both are defined for scalar-weighted networks and neither has a place for a gauge-valued transport.
A targeted search for an \(\exp(-\tau L^\Omega)\)-based sheaf/connection-Laplacian RG returned
nothing, but absence of a hit is weak evidence and the search must be repeated before any novelty
claim (obligation O11).

One correction to the prior-art guess in §3e.5: **\(H^1\) of the sheaf is not frustration, and if any
draft says so it is false.** On a graph \(\dim H^0-\dim H^1=\chi\cdot K\) identically (verified,
residual 0 across flat, partially-aligned and generic bundles, \(=-6\) in each case), so \(H^1\) is
fixed by \(H^0\) and the Euler characteristic and carries no independent information. Frustration is
\(\lambda_1>0\); the only cohomological content is the boolean \(H^0=0\iff\lambda_1>0\).

### 3f.5 What this does and does not do for `Theory/07b`'s tree-dependence defect

**What it does.** It locates the defect precisely and it names the repair, which already exists in
this manuscript. `07b` §`sec:rg-gauge-cross-scale` (`:1618-1724`) is the only place the defect lives.
Its tree-transported feature \(C_x\) (`:1678-1685`) is a *tree-indexed family* of maps whose stated
covariance identity (`:1689-1693`) is true for each fixed tree but is not single-valued on gauge
orbits; `07b` half-admits this itself at `:1698-1707`, where strict nested composition needs an extra
tree-compatibility hypothesis that `Theory/09`'s kernel construction proves **without any
hypothesis** (`prop:cg-nested-sections-compose`, `Theory/09:468`). The concrete edits, all of them
identified and **none of them made** (the `Theory/` write gate at §6.1 applies):

1. `07b:1678-1685` — replace \(C_x\) by the injection \(\iota_I\) with range \(\ker L_I\)
   (`Theory/09:444-449`), or by the Fisher-pencil low-block injection.
2. `07b:1698-1704` — delete `eq:rg-linear-nested-compatibility` and cite
   `prop:cg-nested-sections-compose`.
3. `07b:2747-2748` — the closure-theorem hypothesis clause naming "component-rooted forests together
   with their simultaneous raw root-framed holonomy maps, root features, and dressed boundary
   generators", and `:2766-2768` — the proof sentence "Rooted dressing gives the separate
   gauge-covariant channel maps" — both name a tree as a hypothesis of a conclusion (`:2756`) that
   asserts gauge covariance of the whole collection.

It also sharpens what makes the compression well posed: not flatness, and not even alignment, but
\(z\in\ker L_I\) (R3). And it identifies the exact RG invariant across blocking: **the based holonomy
conjugacy class**, preserved to \(3.3\times10^{-16}\) under contraction.

**What it does not do.** Four things, and they are the reasons this section is not a repair note.

- **The \(\lambda_1>0\) extension has no divergence-tier warrant.** At \(\lambda_1=0\) the
  correspondence \(\ker L\cong\mathrm{Fix}(\mathrm{Hol})\) is exact and
  `thm:cg-holonomy-kl-marginal` supplies a path-, root- and gauge-independent score. At
  \(\lambda_1>0\) there is no fixed parent law and no exact cancellation mechanism. **This is the
  single unproved step of the entire proposal**, and everything about approximately-coherent
  meta-agents rests on it.
- **\(\lambda_1\) is not level-independent, so "the gap" is not an RG-invariant statement.** Under one
  Galerkin blocking step at exact block flatness the fine kernel is reproduced to
  \(6.7\times10^{-15}\) but the transverse gap **rises 61%** (0.0780 → 0.1257), because coarse
  Rayleigh–Ritz eigenvalues are variational upper bounds. \(\lambda_1=\Theta(\theta^2)\) with
  \(\theta\) the holonomy defect is a composite of an exactly-marginal quantity and a finite-size
  scale; a scale-free frustration coordinate should carry the RG statement instead.
- **Two different "spectral gaps" are being used interchangeably in the corpus and must be
  reconciled.** `PIFB2.tex` `eq:rg_constrained_gap` defines \(m_I=\lambda_{I,w}\cdot\lambda_{\min}(F(q_I))\)
  where \(\lambda_{I,w}\) is a weight-constrained Rayleigh quotient of the **ordinary scalar** graph
  Laplacian of symmetrised \(\beta\) — no transports at all — tensored with the Fisher metric. This
  session's \(L^\Omega\) is the connection Laplacian. Different operators, different kernels: the
  scalar one always has the constant vector in its kernel, the connection one has
  \(\ker=\mathrm{Fix}(\mathrm{Hol})\), which the witnesses show can be 1- or 0-dimensional. No result
  bounds \(m_I\) and \(\lambda_1(L^\Omega)\) against each other, and `PIFB2:3861` already relies on
  \(\|H^{-1}\|\le m_I^{-1}\) for the anharmonic remainder.
- **It does not close `genuine-coupling-before-continuum`.** See §3f.4 item 4.

### 3f.6 Open obligations, ranked cheapest-decisive first

**O1. Retract and re-run §3e.2(iii)–(iv).** *Settled by:* computing \(\|L-L^{\mathsf T}\|/\|L\|\) on
the committed seed in `docs/verification/meta_agent_coherence_witness.py`; if nonzero (it will be),
replace the operator with the `Theory/09` energy form and re-assert the four claims. Every spectral
clause downstream depends on this. Cost: one afternoon.

**O2. Resolve the \(\Omega_{ij}\) typing contradiction** (§3f.3 item 10). *Settled by:* one paragraph
in `overview.md` §2 declaring either that agents carry distinct principal bundles over
\(\mathcal C\), or that \(\Omega_{ij}=\varphi_i^{-1}\tau_{ij}\varphi_j\) with \(\tau\) carrying
content beyond frame change. Under the coboundary reading the agent-graph holonomy of §3e.2(i) and
the entire geometric-phase construction of §3f.2 step 4 are **empty**. Cost: a declaration. Decisive
in the strongest sense.

**O3. Move the witnesses into the repository.** All numerics in this section live in session-local
scratchpads (`family.py`, `fam2.py`, `t1.py`–`t12.py` and their siblings). *Settled by:* moving them
under `tests/` or `tools/` with seeds. Until then **no number in §3f is citable**. Cost: an hour.

**O4. Settle which gap is meant at a support boundary** (§3f.1 disagreement 2). *Settled by:* running
the bottom-of-spectrum gap and the block-edge gap on one witness with \(\lambda_1>0\) and one with
\(\lambda_1=0\), and reporting which closes. Predicted **[Suggested]**: frustrated block → avoided
crossing plus relabelling; flat block → exact meeting at the kernel. Also test the self-anchoring
repair (a strictly positive self-weight \(\beta_{ii}>0\) surviving departure, so \(L_{ii}\to\beta_{ii}I\)
rather than 0), which would potentially unify the two wall types. Cost: a day.

**O5. Declare the operator and the metric.** *Settled by:* one page adopting the `Theory/09` energy
form plus the Fisher pencil \((L^\Omega,\bigoplus\Sigma_i^{-1})\), with a test verifying that the
generalized spectrum is real and \(P\mapsto A^{-1}PA\) under congruence. Two lenses measured the
pieces (\(6.4\times10^{-16}\), \(4\times10^{-15}\)); nobody assembled and tested them together, and
that assembly is the load-bearing step of §3f.1 criterion (A).

**O6. Declare the representation channel** — \(\mu\), \(\mathrm{Sym}^2\), or the model channel — or
prove the three coherent blocks coincide. They demonstrably do not for \(SO(3)\) links.
*Settled by:* computing all three on one configuration and reporting whether the coherent index sets
agree. Cost: a day. If they do not agree, "the extent of a meta-agent" has no referent until a channel
is chosen.

**O7. Declare the normalization lift** from the eigen-ray to a normalized law, and name the residual
gauge group it fixes. *Settled by:* a declaration. Any norm-based lift reduces \(GL(K,\mathbb R)\) to
\(O(K)\), and no \(GL(K)\)-invariant lift exists by the programme's own coercivity lemma;
Fréchet/Karcher barycentre repairs are unavailable because \(GL^+(K)\) admits no bi-invariant
Riemannian metric and the bi-invariant trace form on \(\mathfrak{gl}(K)\) is indefinite. Until this is
done the spectral meta-agent is **not a section of a bundle of normalized laws**, i.e. not an agent.

**O8. Verify `[Gao16]`** before any novelty claim about probability-law stalks, and repeat the
sheaf-Laplacian-RG search with the terms "connection Laplacian von Neumann entropy",
"sheaf Laplacian entropy renormalization", and the higher-order Laplacian RG follow-up. *Settled by:*
retrieving and reading the paper. Cost: an hour. Blocks §3f.4 candidate item 1.

**O9. Decide \(\beta^{P}\) versus \(\beta^{Q^*}\) at the programme level.** *Settled by:* reading
whether `Theory/09`'s contraction theorem permits \(C_h\) to depend on recognition parameters. If the
coarse map is built from \(L^\Omega\) at all it must use \(\beta^{P}\), and then the extent is a
random variable measurable w.r.t. the fine sample rather than a fact about \(c\). If extent must be
deterministic given the record, it comes from \(G(P)\) and \(L^\Omega\) drops out of coarse-graining
entirely, retaining only its role in `prop:cg-kernel-holonomy` as the rank indicator.

**O10. Compute \(QF^\omega P\) on an actual programme configuration.** *Settled by:* one computation.
If nonzero anywhere, no coherent subbundle is parallel there and exact parallelism must be **dropped**
from the design goals rather than approximated.

**O11. Get the Kato citation right, at page level**, and settle whether Rellich's theorem is Ch. II
§6. *Settled by:* opening the book. Rellich matters: in a 1-D base it permits analytic continuation
of the projector *through* a crossing, which weakens the RG-event reading further.

**O12. Prove or refute the divergence-tier warrant at \(\lambda_1>0\)** — is the low-lying block of
the Fisher pencil the second-order expansion of a constrained forward-KL score over an approximately
holonomy-fixed parent family? Exact at \(\lambda_1=0\); unproved at \(\lambda_1>0\). This is **the**
unproved step. Expensive, and nothing about approximately-coherent meta-agents is legitimate without
it. A necessary sub-step: supply the Davis–Kahan constant properly — one lens *fitted*
\(\sin\theta\approx15.5\,\lambda_1\) on one instance; the bound should read
\(\sin\theta\le C\lambda_1/\mathrm{gap}\) with \(C\) and the correct denominator **derived**.

**O13. Extend \(G(P)\) beyond the Gaussian tier, and settle whether \(\arg\min_P G\) is generically
unique with connected level sets over \(c\).** The mean/covariance decoupling is a Gaussian fact; the
partition-restricted infimum exists in general but has no closed form. One lens's sweep gives 168/300
interior on unstructured instances and a single clean crossing on a planted one; nothing rules out a
partition whose optimal region is **disconnected** in \(c\), which would make "the extent of a
meta-agent" not a region at all. Also required if extents are to be compared across different agent
*inventories* rather than partitions of a fixed one: a partition prior / description cost, which
reintroduces the \(\log J_P\) convention problem of `Theory/09:901-903`.

**O14. Give the meta-agent transports either a derivation respecting the cocycle, or a declaration as
fresh primitives.** The projected family \(P_\alpha\Omega P_\beta\) fails composition at median 0.90
relative even when the ambient family composes exactly, and is undefined across a rank change. Without
this the meta-agent has no edges and cannot itself be coarse-grained — the RG has one level only.

**O15. Settle whether the geometric phase is record-observable.** Session-established item 4 says the
graph transports **are** kernel arguments, so B4's hypothesis fails for them; but \(c_1\), the
Wilczek–Zee curvature and \(\mathrm{tr}\,\mathrm{Hol}^M\) are computed from eigenvectors, which are
derived objects, not records. The verdict is split and must be recorded that way: the
\(\mathrm{II}\)-quadratic half of \(F^M\) is a deterministic functional of the \(\Omega_{ij}(c)\)
family alone and escapes B4's load-bearing hypothesis, while the \(PF^\omega P\) half remains hidden
by B4 untouched — and the geometric-phase half **inherits §8's exact confound unchanged** (a flat
re-declaration of the transports as free kernel parameters reproducing the record exactly).
*Settled by:* running the \(S^2\) witness (built by `obstruction-topology`, never run against B4)
under a design with both halves nonzero and the \(\ge3\)-base-point cocycle constraint that
`overview.md` §7's B4 row already identifies as the way to break the confound.

**O16. Repair the \(GL(K,\mathbb R)\) gauge non-invariance of the *energy* if the pencil is not
adopted** — construct a transported edge metric \(W_e(c)\) making the energy invariant under
\(z_i\mapsto g_iz_i\) for \(g_i\in GL(K,\mathbb R)\), and check whether the resulting operator is
still PSD with the kernel–holonomy isomorphism intact. `Theory/09` `thm:cg-rectangular-endpoint-closure`
already carries the right category (cellular sheaf Laplacian with edge metrics \(W_e\succ0\) and
rectangular endpoint maps). Until this or O5 is done, **every result in §3f about the gap,
\(\lambda_1\) and the extent is a compact-\(G\) result.**

**O17. Establish the fast/slow reduction or drop the timescale language.** The profiling identity
\(\inf_Q\mathcal F_{\rm state}=-\log p(o|S)\) is exact only when the exact posterior is admitted; a
meta-agent is by construction a *restricted* family, so profiling acquires exactly the gap \(G(P)\).
The uniformly attracting normally hyperbolic fast branch (CE-3) remains unproven and the aggregate
attack `attack-circularity-equilibrium-gl` is recorded SUSTAINED; \(\beta\) and \(\gamma\) sit in the
same functional at the same step at unit temperature with no separating small parameter; and
\(\gamma\) is recognition-side by (R4), so "the model channel is generative and therefore RG-stable"
is not available as a justification. What is supported is only the weak reading: belief and model
alignment are two coordinate blocks of one free energy whose relative rates are a **declared
mobility**, not a theorem.

**O18. Report/repair the ledger drift** (R5), and log §3f.4 item 4 against
`genuine-coupling-before-continuum` as a *partial* discharge.

**Scope fence on every number in this section.** \(K=3\), \(G=SO(3)\) or \(O(2)\)/\(U(1)\),
\(N=3\)–\(8\), 1-D and 2-D bases, float64, CPU-only, on the repository's `.venv` interpreter
(numpy 2.4.4, scipy 1.17.1). Nothing is claimed for large \(K\), for the \(GL(K,\mathbb R)\) fibre,
or for the model channel. The floor constant \(C\approx0.04\) in \(\lambda_1\approx C\|\log\Omega\|_F^2\)
was measured for \(K=3\) on 8 edges; its \(K\)- and edge-count dependence are unmeasured, and the
crossover \(\|\log\Omega\|_F\approx0.50\) will move with both. No lens audited `src/multiagent_elbo`
to check whether the shipped code actually constructs \(L^\Omega\), or in which form — if it uses
row-stochastic asymmetric \(\beta\) without symmetrisation, (R1) applies to the shipped operator
immediately and not merely on the \(GL\) tier.

---

## 3g. GENUINE CROSS-AGENT COUPLING — a shared latent, and the rank obstruction

*Opened 2026-08-13. Witness: `docs/verification/shared_latent_coupling_witness.py`, seed 20260813,
four claims asserted in-script. Addresses validated-ledger claim `genuine-coupling-before-continuum`
(HIGH, INCONCLUSIVE).*

### 3g.1 The gap

The tied-replica law is blockwise-product by construction, \(P_h^n=\bigotimes_aP_a^n\), so its total
correlation is identically zero and it cannot carry a multi-body operator. That is why
\(\varepsilon_h=0\) only at \(C_h=\mathrm{id}\) and why the effective-action question cannot be posed
on it. The minimal repair named in the roadmap is a shared latent.

### 3g.2 What a shared latent buys [COMPUTED]

Take \(z\sim N(0,T)\), \(k_a\mid z\sim N((\Lambda z)_a,\sigma_a^2)\), so
\(\Sigma=D+\Lambda T\Lambda^{\mathsf T}\) with \(D=\mathrm{diag}(\sigma_a^2)\).

**(i) Genuine dependence.** \(\mathrm{TC}=0\) exactly for the product law; \(\mathrm{TC}=0.740\) for
the shared-latent law. The structural obstruction is removed.

**(ii) With one latent the induced interaction is *exactly* PIFB2's form.** Integrating out \(z\)
gives \(-\log p(k)=\tfrac12k^{\mathsf T}\Sigma^{-1}k\), and the unique Laplacian-plus-diagonal split
of \(\Sigma^{-1}\) is
\[
\tfrac12k^{\mathsf T}\Sigma^{-1}k
=\sum_{a<b}\tfrac12\beta_{ab}(k_a-k_b)^2+\sum_a\tfrac12\pi_ak_a^2,
\qquad \beta_{ab}=c\,v_av_b,\quad v=D^{-1}\lambda,
\]
with \(c=\tau^2/(1+\tau^2\lambda^{\mathsf T}D^{-1}\lambda)\). Verified: Sherman–Morrison to
\(1.2\times10^{-15}\), \(\beta_{ab}=cv_av_b\) to \(2.2\times10^{-16}\), split exact to \(0\), energy
residual \(-2.8\times10^{-16}\), all \(\beta_{ab}>0\). **So a genuinely coupled law does generate the
transported-KL coupling the programme declares** — in the flat case, where the transport is the
identity.

### 3g.3 The rank obstruction [COMPUTED] — this is the finding

The number of shared latents equals the rank of the induced coupling, but positivity fails as soon as
there is more than one:

| \(R\) latents | rank\((D^{-1}-\Sigma^{-1})\) | all \(\beta_{ab}>0\) | \(\min\beta_{ab}\) |
|---|---|---|---|
| 1 | 1 | yes | \(+0.0211\) |
| 2 | 2 | no | \(-0.1990\) |
| 3 | 3 | no | \(-0.0494\) |
| 5 | 5 | no | \(-0.2841\) |

A sum of KLs is nonnegative term by term, so a negative weight cannot be represented by one. Hence a
shared-latent law delivers **either** the transported-KL form (\(R=1\), and then the attention matrix
is rank one) **or** higher-rank attention (and then the coupling is not a sum of KLs) — not both.
PIFB2 deploys a general row-stochastic \(\beta\), whose rank runs up to \(N-1\).

That is a sharper statement of `genuine-coupling-before-continuum` than the ledger currently carries.
The obstruction is not that coupling cannot be generated; it is that **the declared functional form
and the declared attention rank cannot be had simultaneously from this mechanism.**

### 3g.4 Two side conditions [COMPUTED]

Same-sign loadings are necessary: flipping one sign gives \(\beta_{01}=-0.512\), repulsive. And the
residual diagonal need not be a valid prior precision — one entry came out at \(-0.129\), an improper
induced prior. Both must be declared rather than assumed.

### 3g.5 The fiber-valued case: a transport IS induced, but it is never a connection [COMPUTED + PROVEN]

Extending to \(K\)-dimensional fibers, \(k_a\mid z\sim N(\Lambda_az,S_a)\), Woodbury gives the
off-diagonal block \(-B_a\Lambda_aM\Lambda_b^{\mathsf T}B_b\) with
\(M=(T^{-1}+\sum_b\Lambda_b^{\mathsf T}S_b^{-1}\Lambda_b)^{-1}\). Reading it against the
transported-KL form with the Fisher weight \(W_{ab}=S_a^{-1}\) (per O5) gives, up to scale,
\[
\Omega_{ab}=\Lambda_aM\Lambda_b^{\mathsf T}S_b^{-1},
\]
invertible iff \(d\ge K\). So a **nontrivial transport is induced** — answering §3g.5's own next
question affirmatively. Woodbury verified to \(2.4\times10^{-15}\), \(\operatorname{rank}\Omega=K\).

**But it is not a frame coboundary, and this is a no-go rather than a genericity statement.**
*(Wording corrected 2026-08-13: the earlier "never a connection" conflated two objects. The
**declared** frame transport \(\Omega_{ij}=g_ig_j^{-1}\) certainly IS a connection — verified self-edge
\(2.4\times10^{-16}\), cocycle \(3.1\times10^{-16}\), loop holonomy \(4.8\times10^{-16}\) — and being a
coboundary it is **identically flat for any frames whatsoever**; likewise a frame field on the base
gives \(A=g^{-1}dg\) with curvature \(2.2\times10^{-11}\). The claim here concerns the **induced**
coupling only.)* The induced object fails the **self-edge identity** first,
\(\|\Omega_{aa}-\mathbb 1\|=1.51\), and the cocycle failure is downstream of that. It is
"coboundary-shaped" — it factors as \((\Lambda_aM)(\Lambda_b^{\mathsf T}S_b^{-1})=A_aB_b\) — but
\(B_b\ne A_b^{-1}\), so it is not \(g_ag_b^{-1}\) for any frames \(g\). Formally:
\(\Omega_{ab}\Omega_{bc}=\Omega_{ac}\) requires \(F_bM=\mathbb 1\) for every \(b\), where
\(F_b=\Lambda_b^{\mathsf T}S_b^{-1}\Lambda_b\succeq0\). Since \(M^{-1}=T^{-1}+\sum_bF_b\), that forces
all \(F_b\) equal to a common \(F\) with \(F(1-N)=T^{-1}\), i.e.
\[
F=\frac{T^{-1}}{1-N},
\]
**negative definite for every \(N\ge2\)** while \(F\) is PSD by construction. Contradiction. No choice
of loadings, private covariances, or latent prior repairs it. Measured mismatches \(0.87\)–\(2.17\)
on random data; with *identical* agents (so the "all \(F_b\) equal" half is free) the deviation is
still \(1.065\) at \(N=2\) rising to \(1.531\) at \(N=8\), and the improper-prior limit
\(T\to\infty\) tends to \(\|\mathbb 1/N-\mathbb 1\|\ne0\).

**Two independent obstructions, then.** In the scalar case the mechanism is rank-limited (§3g.3); in
the fiber case the induced transport is not a connection. Both say the same thing in different
coordinates: a shared latent supplies genuine coupling, but not coupling of PIFB2's *declared form*.
This bears directly on decision **D1** — a genuinely coupled generative law induces **free edge data**,
not a cocycle and a fortiori not a coboundary, which is evidence for D1 option (c) and against the
`PIFB2.tex:208` reading that puts non-coboundary transport data out of scope.

### 3g.6 What is open

The witness is scalar (\(K=1\)), centred Gaussian, one base point, so the transport is the identity
and \(\beta_{ab}(k_a-k_b)^2\) is the **flat** case of the transported KL. Whether a shared latent can
generate \(\beta_{ab}\|k_a-\Omega_{ab}k_b\|^2\) with nontrivial \(\Omega\) is the obvious next
witness and is not addressed. Adding \(z\) also modifies `Theory/04`'s declared generative class,
exactly as the label-copy block \((J_a,X_a)\) did, and costs a declaration. The recognition side is
untouched: a factorized \(Q=q(z)\otimes\bigotimes_aQ_a\) carries a mean-field gap that has not been
priced. Finally, §3g.3's negative is generic, not universal — it shows positivity fails for random
same-sign loadings at \(R\ge2\), not that no \(R\ge2\) loading matrix yields an all-positive
\(\beta\); whether that set is nonempty is open and is the cheapest way to overturn this section.

---

## 3h. CURVATURE AND META-AGENT FORMATION - 2-cells from attention, and the order parameter

*Opened 2026-08-13. All results COMPUTED on instances; none proved in general. Scope fence at 3h.5.*

### 3h.1 Free edge variables already exist in the corpus

`Theory/02_geometry.tex` `def:geo-graph-links` (`sec:geo-regime-two`) already declares free
\(\Theta_e^b,\Theta_e^m\in G\) on a finite interaction **multigraph** declared independently of
\(\mathcal C\), with \(\Theta_{\bar e}=\Theta_e^{-1}\) and vertex gauge \(\Theta'_e=(a_i)^{-1}\Theta_ea_j\).
`hyp:geo-flat-links` (`:645-656`) is the *optional* coboundary specialization
\(\Theta_e=U_iU_j^{-1}\), tagged `\status{HYPOTHESIS}`, whose own text says it excludes represented
graph holonomy in either channel. **Non-flat edge variables are therefore not new construction - they
are Regime II, already declared, and D1 is only asking which is default.**

Frames alone buy flatness at every level: \(\Theta_{ij}=g_ig_j^{-1}\) telescopes around every loop
(self-edge \(2.4\times10^{-16}\), cocycle \(3.1\times10^{-16}\), holonomy \(4.8\times10^{-16}\)), and a
frame field on the base gives \(A=g^{-1}dg\) with curvature \(2.2\times10^{-11}\).

### 3h.2 Attention triangles as 2-cells [COMPUTED]

A cycle is not automatically a 2-cell; one *declares* which cycles bound, and **the declaration is
not canonical - its shape follows the interaction structure.** *(Corrected 2026-08-13: the first
version of this section used transformer-flavoured supports - causal masks, sliding windows - which
are artifacts of sequence modelling and do not apply here. The interaction multigraph is declared
independently of \(\mathcal C\) and need not resemble any of them.)*

Filling all **triangles** (the clique complex), \(\operatorname{rank}H_1\):

| interaction topology | E | T | cycles | rank H1 |
|---|---|---|---|---|
| **2D grid 5x5 (MAgent-like)** | 40 | **0** | 16 | **16** |
| 2D grid 5x5 on torus | 50 | **0** | 26 | **26** |
| ring \(n=12\) | 12 | 0 | 1 | 1 |
| Erdos-Renyi \(n=16,p=0.18\) | 14 | 1 | 2 | 1 |
| ring lattice \(k=4\) (clustered) | 32 | 16 | 17 | 1 |
| complete \(n=8\) | 28 | 56 | 21 | **0** |

**A grid has no triangles at all** - zero clustering - so triangle-filling fills nothing and every
cycle stays monodromy. Only the complete graph reaches \(H_1=0\) that way. Triangles are the right
2-cells only for clique-y interaction structures.

For a lattice the elementary plaquettes are **squares**, which is exactly lattice gauge theory:

| grid | E | faces | cycles | rank H1 |
|---|---|---|---|---|
| 5x5 open | 40 | 16 | 16 | **0** (pure curvature) |
| 5x5 torus | 50 | 25 | 26 | **2** (curvature + two non-contractible loops) |

Two consequences. **`MAgent_Model` on a grid with \(GL(K)\) links and square plaquettes is a lattice
gauge theory** - Wilson plaquettes and all - a far more direct connection to existing machinery than
the programme currently claims anywhere. And **the torus retains \(H_1=2\) under any face filling**;
that irreducible monodromy is precisely the setting in which B4's bundle-topology clause becomes
testable, using the programme's own prototype topology with periodic boundaries. The \(U(1)\)
two-path witness sits on the ring, \(H_1=1\), which is why its holonomy is monodromy rather than
curvature and why it cannot test the curvature clause.

### 3h.3 Curvature controls the coherence order parameter [COMPUTED] - the main result

Writing \(\Theta_e=g_ig_j^{-1}\exp(s\,p_e)\), a coboundary times a genuine edge perturbation, holding
the gauge fixed and varying \(s\):

| \(s\) | plaquette action | \(\lambda_0\) | ratio |
|---|---|---|---|
| 0.00 | 0.000000 | \(-0.0\times10^{-8}\) | - |
| 0.01 | 0.040567 | 0.00028589 | 0.00705 |
| 0.05 | 1.018643 | 0.00727783 | 0.00714 |
| 0.20 | 16.436154 | 0.12133323 | 0.00738 |
| 0.40 | 65.108484 | 0.48025678 | 0.00738 |

Fitted exponent \(1.006\). \(\lambda_0\) vanishes **exactly** at zero curvature and grows **linearly**
in the plaquette action, ratio \(\to0.00705\) as \(s\to0\), so
\(\lambda_0=c\sum_{\rm plaq}\|F\|^2+O(F^4)\). The coherence order parameter of 3e is controlled by the
curvature.

### 3h.4 What that means for meta-agent formation

Curvature is the **obstruction** to a meta-agent, not its cause: \(\lambda_0=0\) iff flat iff a
parallel section exists iff a consistent meta-belief exists. The intuition that curvature drives
agents into meta-agents is correct only in the **dynamical** reading. If \(\Theta\) carries its own
plaquette action, minimizing it drives \(F\to0\), and by 3h.3 that is *identically* driving
\(\lambda_0\to0\). **Curvature is the free-energy cost of not being a meta-agent; descending it is what
forms one.** Curvature is the potential, not the force.

The compactness obstruction does not bite. Yang-Mills non-definiteness forbids a coercive
\(\|F\|^2\) for noncompact \(G\), but for an **aligned** block the holonomy lies in
\(\mathrm{Stab}(q)=O(K-1)\) (3e.2(i),(vi)), which is compact, so \(-\operatorname{tr}(XY)\) is
available on the holonomy algebra. The curvature term is definite exactly on the blocks near being
meta-agents, degenerating only where the block is far from coherent - where the construction claims
nothing anyway.

### 3h.4a CORRECTION 2026-08-13 - the compactness rescue in 3h.4 is REFUTED

3h.4 argued that Yang-Mills non-definiteness does not bite because an aligned block's holonomy lies in
\(\mathrm{Stab}(q)=O(K-1)\), which is compact. **That is wrong, and the error is instructive.** The
gauge acts by **conjugation**, and the Frobenius norm is invariant only under *orthogonal*
conjugation. Where the holonomy *sits* is irrelevant; what matters is the conjugating element.

Executed with \(H\) a rotation by \(0.6\) pinned **inside \(SO(3)\)**, conjugated by
\(g=\exp\mathrm{diag}(s,-s,0)\in GL(3,\mathbb R)\):

| \(\|\log g\|\) | \(\operatorname{tr}(gHg^{-1})\) | \(\|gHg^{-1}-\mathbb 1\|_F\) |
|---|---|---|
| 0.000 | 2.6506712298 | 0.836 |
| 0.849 | 2.6506712298 | 1.899 |
| 2.121 | 2.6506712298 | 11.344 |
| 4.243 | 2.6506712298 | **227.79** |

The trace is conserved **exactly** to ten digits - it is a conjugacy invariant - while the Frobenius
norm runs over two and a half orders of magnitude on a single gauge orbit. Independently measured by
the panel: \(\lambda_0\) relative deviation \(9.3\times10^{-1}\) under a \(GL^+\) gauge versus
\(1.4\times10^{-12}\) under \(SO(2)\), with \(\lambda_0\) driven from \(3.06\times10^{-4}\) to
\(1.16\times10^{-10}\) by a boost alone.

**Consequence for 3h.3.** The law \(\lambda_0=c\sum\|F\|^2\) was computed at \(G=SO(3)\), where both
sides are orthogonally invariant, so it is correct there and **does not transfer to
\(GL(K,\mathbb R)\)** - where \(\lambda_0\) is not even gauge-invariant and therefore is not an order
parameter at all.

**The real obstruction, and it is the old one wearing a new hat.** For noncompact \(G\) the plaquette
density can be gauge-invariant or smooth at flatness, not both:

- \(\|W-\mathbb 1\|_F^2\): nonnegative and smooth at \(W=\mathbb 1\), **not** conjugation-invariant.
- \(1-\tfrac1N\operatorname{Re}\operatorname{tr}W\): conjugation-invariant, but **unbounded below** on
  noncompact \(G\) (panel: \(-73.2\) for an \(SL(2,\mathbb R)\) boost of rapidity 5).
- the class-function spectral density: conjugation-invariant, but its gradient needs **distinct**
  eigenvalues, and at \(W\approx\mathbb 1\) all \(K\) eigenvalues coalesce - degenerate exactly at the
  configuration the term is meant to drive toward.

This is §7's Yang-Mills row in a third guise: invariance and coercivity are in tension for noncompact
\(G\), and here the tension shows up as invariance versus differentiability at the target.

**LIVE DEFECT.** `MAgent_Model-main/gauge_agent/lattice_gauge.py:314` implements
`yang_mills_action` with `action_form='frobenius'` as the **default**, wired at
`full_vfe.py:2233-2239` with `lambda_ym` defaulting to \(0.1\) (`full_vfe.py:381`) and set to \(0.1\)
in shipped configs (`runs/minimal/config.json:23`, `runs/hamiltonian_oscillator/config.json:23`). So a
**gauge-non-invariant** curvature penalty is on by default in shipped runs. The file's own docstring
already records the trade-off and offers `action_form='spectral'` as the conjugation-invariant
alternative, together with its gradient degeneracy at \(W\approx\mathbb 1\). Neither branch is
correct as it stands for \(GL^+(K)\); the honest options are to restrict the link group to a compact
subgroup, or to build the density from conjugacy invariants that stay differentiable at the identity.

### 3h.4b The lattice-gauge identification, settled

**Kinematics: Wilson's, term for term, and must be cited.** Group-valued links on oriented edges with
reversal-inverse, the vertex gauge law, ordered-product path transport, plaquette holonomy on declared
2-cells, and trace/determinant conjugacy invariants - i.e. Wilson loops. `Theory/02` `def:geo-graph-links`
is Wilson 1974 §II kinematics; `prop:geo-trivializing-criterion` and `trivialization_via_spanning_tree`
are flat-bundle classification over a graph plus maximal-tree gauge fixing (Kobayashi-Nomizu I Ch. II
§9; Creutz 1983). Present these as standard.

**Dynamics: not lattice gauge theory, and nothing on the roadmap's OPEN list is retired by it.** LGT
is a probability measure on link configurations, requiring a normalizable Haar measure (fails: \(GL^+\)
is unimodular but its Haar measure is infinite, so \(Z\) diverges before any action is chosen), a
lattice spacing, and a volume limit. A finite declared multigraph has neither parameter, so there is no
area law, no string tension, no continuum limit to inherit. The matter sector is also not standard: LGT
matter is a vector in a linear representation with a fixed invariant inner product, whereas here it is a
probability law coupled by an asymmetric divergence with a state-dependent fiber metric - a gauged
lattice sigma model with an information divergence, which is not a named model in that literature.

Also retired as standard, not as results: 3h.3's *qualitative* claim that \(\lambda_0\) vanishes exactly
at zero curvature is textbook \(O(d)\) synchronization (Bandeira-Singer-Spielman, SIAM J. Matrix Anal.
Appl. 34(4):1611-1630, 2013); and 3h.2's square-2-cell homology is the ordinary cell structure of the
square lattice with the ordinary \(H_1\) of the torus. What survives as this programme's own is the
*linear* law with its constant, and only at compact \(G\).

### 3h.5 Scope, and what is not established

\(K=3\), \(G=SO(3)\), \(n=6\)-\(8\), one base point, unit edge weights, dense graph for 3h.3. The
linear law is fitted on instances, not proved; the constant \(c=0.00705\) is graph- and
weight-dependent and its dependence is unmeasured. \(\lambda_0\) here is the bottom of the **bare**
energy form, and O4 established that the operator carrying the prior sector has no kernel, so the
statement must be restated relative to the prior floor before it is used for extent. No claim is made
that a plaquette action is ELBO-derived; whether \(\|F\|^2\) has an exact negative-ELBO reading is
open and is the obvious next question. Both **declared** and **dynamical** \(\Theta\) are to be built
out; only the declared case is exercised above.

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

**The consequential negative — SCOPE-RESTRICTED 2026-08-13.** The framing "which both agree on" was
wrong: the skeptic denies that balanced stencils are generic and holds that the **deployed** rows
recover the sector at \(O(1)\). Independently recomputed retained fractions of the peer sector at
\(O(h^2)\): **0.900** for a causal two-left-neighbour row \(m=(-1,-2)\); **0.360** \(=(2w-1)^2\) for
an ALiBi-like \(\pi=(0.8,0.2)\); **1** for single-source agents. PIFB2 deploys exactly these row types
(causal masking, ALiBi, learned position bias, `PIFB2.tex:709`), so the headline
"the Fisher-covariant Dirichlet peer sector is not generated" is a **balanced-stencil artifact** and
must not be cited unrestricted. On a balanced stencil the label-marginalization
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
all.

> **RETRACTED 2026-08-13.** This paragraph originally continued: *"It also explains the \(d=2\)
> coincidence in 4.6 and the Gaussian-fixed-covariance escape in 4.1 as the same phenomenon: both are
> exactly where the Amari–Chentsov contraction drops out."* That is **wrong**, and contradicted by its
> own source: `panelB-V-BRIDGE-derivation.md:17` states that the statistical nature of the target
> (curvature of \(g^F\), the Amari–Chentsov tensor) plays **no** role in the \(d=2\) selection, which
> is a homogeneity/Weyl fact about \(h\) as an abstract PSD tensor. Refuted directly: the \(d=2\) raw
> unit-coefficient bond sum converges cleanly with a **Poisson** fibre, for which
> \(T_{\rm skew}=A'''=e^\theta>0\) everywhere. The accurate unification is the classical
> scale-invariance of a two-derivative energy density in two dimensions — `V-BRIDGE:197`: *"not an
> analogy; it is an identity."* The hedged form of the same guess survives at next-step #2, where it
> is correctly marked "plausibly one phenomenon and worth checking as such"; **do not let it steer the
> search for the connection-mismatch repair.**

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

### 6.1 `Theory/` write gate (added 2026-08-13)

Nothing from §4b goes into `Theory/` without a **per-result `SPEC.md:17` compliance check**, in
addition to the existing rm-01…rm-06 reconciliation gate. `SPEC.md:17` excludes PIFB2 as source,
crosswalk, motivation, and remark. It is currently **honored** — zero PIFB references across the 20
chapters, and `PIFB2.tex` is not `\input` by `main.tex`.

But the exclusion is narrower than a blanket ban: **`SPEC.md:20-25` explicitly licenses** (a) deriving
a categorical source-label attention \(\beta_{ij}\) from a fixed normalized interaction-record joint,
and (b) holonomy-conditioned projection of transported marginal laws — the two constructions this
programme most wants to export. Applying the gate result by result:

| Result | `Theory/` admissible? |
|---|---|
| §4.1(i) covariant \(O(h^3)\) parity cancellation | **Yes** — no PIFB2 crosswalk |
| §4.1(iii) connection mismatch (\(\alpha=+1\) vs Levi-Civita) | **Yes** |
| §4.2 belief-dressed Ad-invariance for noncompact \(G\) | **Yes** |
| §4.6 the \(d=2\) induced-volume bound | **Yes** |
| §4.3 \(\varepsilon_h\), \(c_h\) | **No** — defined as a residual against \(S_h^{\rm PIFB}\); PIFB2 *is* the crosswalk |
| §4.4 the \(\tau=\kappa\sqrt{K_q}\) obstruction | **No** — same reason, and the dispute is unresolved |

Blocked results belong in a distinct synthesis manuscript, or require a deliberate author revision of
the SPEC. *(Raised as Finding 7 of the interim referee review; the review's blanket "keep it outside
`Theory/`" over-reaches, since it quotes `SPEC.md:17` without `:20-25`.)*
