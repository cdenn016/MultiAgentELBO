# panelA-T-CURV-derivation

*Recovered verbatim from workflow journal.jsonl, 2026-08-13. Agent a3c3d76a.*

## target

T-CURV: can a curvature (Yang-Mills/Wilson) sector be DERIVED from an exact ELBO term rather than postulated, and in what metric?

## status

PARTIAL

## theorem_statement

Let $(\mathsf K,\mathscr K)$ be a standard-Borel sample space, $G\le GL(K,\mathbb R)$ a closed subgroup (compactness NOT assumed) acting on $\mathsf K=\mathbb R^K$ by $x\mapsto gx$, and let $\mathcal B\subseteq\mathcal P(\mathsf K)$ be a $G$-invariant regular parametrized-measure model in the sense of Theory/05c_pullback_geometry.tex:30-42 (hyp:pb-regular-models). For $q\in\mathcal B$ and $Y\in\mathfrak g$ write $Y.q:=\tfrac{d}{dt}\big|_0(\exp tY)_\#q$ for the fundamental vertical vector at $q$, with $q$-score $\psi_Y:=d(Y.q)/dq\in L^2(q)$, and define the **belief-dressed Lie-algebra form**
$$\langle Y,Z\rangle_q\;:=\;g^F_q(Y.q,\,Z.q)\;=\;\mathbb E_q[\psi_Y\psi_Z].$$

**(1) [DERIVATION]** $D_{\rm KL}\!\big(q\,\|\,(\exp\varepsilon Y)_\#q\big)=\tfrac12\varepsilon^2\langle Y,Y\rangle_q+\tfrac{\varepsilon^3}{6}\big(3\mathbb E_q[\psi_Y L_2]+\mathbb E_q[\psi_Y^3]\big)+O(\varepsilon^4)$, with $L_2=\partial_\varepsilon^2\log\frac{d(\exp\varepsilon Y)_\#q}{d\nu}\big|_0$. Hence for a plaquette holonomy $H_P=\exp\!\big(h^2F_{\mu\nu}(c)+O(h^3)\big)$,
$$\boxed{\;D_{\rm KL}\!\big(q\,\|\,(H_P)_\#q\big)=\tfrac12h^4\,\big\|F_{\mu\nu}(c).q\big\|^2_{g^F(q)}+O(h^5).\;}$$

**(2) [DERIVATION, Riemann-sum consistency only]** With plaquette weight $h^{d-4}$ and a remainder uniform over plaquettes, $\sum_P h^{d-4}D_{\rm KL}(q\|(H_P)_\#q)\to\tfrac12\int_{\mathcal C}\sum_{\mu<\nu}\|F_{\mu\nu}(c).q(c)\|^2_{g^F(q(c))}\,dc$ with error $O(h)$. This is a **Fisher-weighted, state-dependent Yang-Mills energy**, not $\|F\|_F^2$.

**(3) [FORMAL PROOF — THE PAYOFF; NOT REFUTED]** For every $g\in G$ (noncompact permitted) and every $Y,Z\in\mathfrak g$,
$$\boxed{\;\big\langle \mathrm{Ad}_gY,\ \mathrm{Ad}_gZ\big\rangle_{\,g_\#q}\;=\;\langle Y,Z\rangle_q\;}$$
i.e. $\|F_{\mu\nu}.q\|^2_{g^F(q)}$ is **exactly invariant** under the simultaneous local gauge transformation $F\mapsto\mathrm{Ad}_{g(c)}F$, $q\mapsto \widehat\rho(g(c))_\#q$. The invariance is pointwise in $c$ and holds for arbitrary **local** $g(c)$, requires no $\mathrm{Ad}$-invariant inner product on $\mathfrak g$, no normalized Haar measure, and no compactness — only that $g$ act by a parameter-independent bimeasurable bijection of the sample space. **This supplies a conjugation-invariant curvature energy for any closed subgroup of $GL(K,\mathbb R)$, including noncompact ones.**

**(4a) [FORMAL PROOF, Gaussian closed form]** For $q=\mathcal N(\mu,\Sigma)$, $\Sigma\succ0$, and $Y\in\mathfrak{gl}(K,\mathbb R)$:
$$\langle Y,Y\rangle_q=\operatorname{tr}(Y^2)+\operatorname{tr}\!\big(\Sigma Y^{\!\top}\Sigma^{-1}Y\big)+\mu^{\!\top}Y^{\!\top}\Sigma^{-1}Y\mu=\tfrac12\|W+W^{\!\top}\|_F^2+|Ww|^2,$$
with $W=\Sigma^{-1/2}Y\Sigma^{1/2}$, $w=\Sigma^{-1/2}\mu$. Each of the three trace terms is separately conjugation-invariant.

**(4b) [FORMAL PROOF, degeneracy]** $\operatorname{rad}\langle\cdot,\cdot\rangle_q=\mathfrak g_q=\{Y:\ Y\mu=0,\ Y\Sigma+\Sigma Y^{\!\top}=0\}$, the isotropy algebra, $\cong\mathfrak{so}(K-1)$ if $\mu\ne0$ and $\cong\mathfrak{so}(K)$ if $\mu=0$. Invisible curvature directions are exactly the $\Sigma$-orthogonal rotations fixing $\mu$.

**(4c) [DERIVATION, multi-agent nondegeneracy]** For $N$ agents at one base point sharing **one** connection, $\operatorname{rad}\sum_i w_i\langle\cdot,\cdot\rangle_{q_i}=\bigcap_i\mathfrak g_{q_i}$. This is trivial iff $\{\Sigma_1^{-1/2}\Sigma_i\Sigma_1^{-1/2}\}$ generates $M_K(\mathbb R)$ modulo the mean conditions; in particular **two agents whose relative covariance $\Sigma_1^{-1/2}\Sigma_2\Sigma_1^{-1/2}$ has $K$ distinct eigenvalues make the total form positive definite on all of $\mathfrak{gl}(K,\mathbb R)$, for every $K$.**

**(4d) [COUNTEREXAMPLE, coercivity]** Unconditional coercivity **FAILS**. On the consensus configuration $q_1=\dots=q_N$ the radical is $\mathfrak g_{q_1}$, of dimension $\ge(K-1)(K-2)/2$, nonzero for $K\ge3$; $\lambda_{\min}$ has no positive lower bound on belief-configuration space and degenerates continuously as $\Sigma\to t\Sigma$, $t\to\infty$ (rate $t^{-1}$). With **per-agent** connections $F^{(i)}$ (PIFB2's own typing, PIFB2.tex:429,713) the multi-agent repair does not apply at all.

**(5) [DERIVATION + inherited COUNTEREXAMPLE, provenance]** The **lagged** self-loop $\beta_{aP}D_{\rm KL}\!\big(q_a^{n+1}\,\|\,(H_P)_\#q_a^{n}\big)$ **is** an exact term of the closed tied-replica ELBO (take $b=a$, $\Omega^n_{aa}:=H_P$). The **same-time** loop $D_{\rm KL}(q\|(H_P)_\#q)$ is **not**: it is the diagonal value $q^{n+1}=q^n$ of the lagged term, and imposing it as an identity makes the generative denominator read the recognition law — the same-time reciprocity obstruction. Moreover, off the diagonal the term equals $\tfrac12\|\Delta-h^2v_F\|^2_{g^F}+O(\|\cdot\|^3)$, which the belief update $\Delta$ can drive to zero, so **the exact ELBO term is a curvature penalty only after profiling against the belief-pinning terms**; in base dimension $d=2$ (PIFB2's working base, PIFB2.tex:434) profiling annihilates it to leading order.

## hypotheses

### 1

(H1) Regularity. hyp:pb-regular-models, Theory/05c_pullback_geometry.tex:30-42: finite-dimensional smooth parametrized-measure model, differentiability in quadratic mean, positive-definite Fisher form, third-power integrability of every score direction used, domination sufficient to differentiate the divergence expressions through third order. Needed for the O(eps^3) remainder in (1). The Gaussian family on R^K with Sigma strictly positive definite satisfies all of this; the singular stratum det Sigma = 0 is excluded.

### 2

(H2) Represented action is a sample-coordinate change. Same hypothesis, 05c:37-39: 'the represented action rho_hat_x(g) is induced by a parameter-independent bimeasurable change of sample coordinates and preserves B'. This is the ONLY structural hypothesis used in the invariance theorem (3). GL(K,R) acting linearly on R^K satisfies it; compactness is nowhere used.

### 3

(H3) Score integrability of the fundamental field. psi_Y := d(Y.q)/dq must exist and lie in L^2(q). For q with smooth positive density f and linear V(x)=Yx, psi_Y(x) = -[(grad log f(x))^T Y x + tr Y], which is a quadratic polynomial for Gaussian q, hence in L^2(q). Zero mean E_q[psi_Y]=0 follows from mass conservation (divergence theorem with decay).

### 4

(H4) Link consistency / BCH plaquette expansion. H_P = exp(h^2 F_{munu}(c) + O(h^3)) for links U_mu(x) = exp(h A_mu(x)) with A a smooth Lie-algebra-valued field and F_{munu} = d_mu A_nu - d_nu A_mu + [A_mu, A_nu]. This is the standard lattice-gauge BCH identity but is a HYPOTHESIS in this program, of exactly the status of docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/lattice-continuum-asymptotics.md:4-9. It is NOT derived from any ELBO.

### 5

(H5) Uniform remainder for (2). The O(h^5) in the plaquette expansion must be uniform over plaquettes; otherwise the sum of h^{-d} plaquettes at weight h^{d-4} does not have error O(h). lattice-continuum-asymptotics.md never claims uniformity; I state it as required.

### 6

(H6) Regime-II promotion. F is identically zero for the deployed flat coboundary Omega_ij = exp(phi_i)exp(-phi_j) (PIFB2.tex:142, :353, :434), so the whole sector is vacuous unless the links are promoted to independent data. PIFB2 has that promotion but its checked-in twist scale and learning rate are zero (PIFB2.tex:418, :449 per ground extract).

### 7

(H7) Shared principal connection for (4c). The multi-agent nondegeneracy repair requires ONE connection A on the base with all agents sections of associated bundles of the SAME principal bundle in (possibly different) representations. PIFB2 instead writes a per-agent F^{(i)}_{munu} (PIFB2.tex:429, :713); under that typing (4c) does not apply.

### 8

(H8) Both fields transform. Invariance in (3) requires F -> Ad_g F AND q -> g_# q simultaneously. If q is exempted (held as a fixed background), invariance fails - the exact analogue of PIFB2.tex:341 ('fails to be invariant only when a fixed field is exempted from the action').

### 9

(H9) Finiteness/scope for (5). The closed tied-replica theorem is stated for a FINITE agent-site set with 'Refining the base and taking N -> infinity are not part of this construction' (docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/typed-construction.md:6-7). Every continuum statement in (2) is therefore outside its certified scope.

### 10

(H10) Quadratic-model hypothesis for the profiling result in (5). The screening computation assumes the non-loop free energy is locally F_other(theta') ~ F_other(theta_0) + (1/2)|theta'-theta_0|^2_M with M = m g^F positive definite and theta_0 the previous-step optimum. This is a local expansion, not a global statement.


## derivation

## 0. Setup, and what is being asked

Fix a base point $c$. Work in the belief fiber $\mathsf K=\mathbb R^K$ with structure group $G\le GL(K,\mathbb R)$ acting linearly, $x\mapsto gx$. The induced action on laws is pushforward, $T_g(\mu):=g_\#\mu$; write $\widehat\rho(g)=T_g$. Let $\mathcal B\subseteq\mathcal P(\mathbb R^K)$ be a $G$-invariant regular model (H1,H2).

For $Y\in\mathfrak g$ define the **fundamental vertical vector** at $q$,
$$Y.q:=\frac{d}{dt}\Big|_{0}(\exp tY)_\#q ,$$
a signed measure of total mass $0$. This is the object Theory writes $\zeta_\xi\beta$ (Theory/05c_pullback_geometry.tex:175: "$\zeta_\xi$ is the fundamental vertical field of $\xi\in\mathfrak g$ for the represented action"). Its $q$-score is $\psi_Y:=d(Y.q)/dq$. For $q$ with smooth positive density $f$ and $V(x)=Yx$,
$$Y.q=-\operatorname{div}(fV)\,dx,\qquad \psi_Y(x)=-\big[(\nabla\log f(x))^{\!\top}Yx+\operatorname{tr}Y\big],\qquad \mathbb E_q[\psi_Y]=0. \tag{0.1}$$

Define the **belief-dressed Lie-algebra form**
$$\langle Y,Z\rangle_q:=g^F_q(Y.q,Z.q)=\mathbb E_q[\psi_Y\psi_Z],\qquad g^F \text{ as in Theory/05c:44-53 (eq:pb-fiber-fisher).} \tag{0.2}$$

**Provenance note (novelty fencing).** This exact form is already in the manuscript, as a by-product of the isotropy criterion: Theory/05c_pullback_geometry.tex:946-949 states "$\mathcal Q_\Psi=\mathfrak a^*\mathfrak k_{\bar s(f(c))}$ with $\mathfrak k_{\bar\beta}(\xi,\eta)=\bar g^F(\bar\zeta_\xi\bar\beta,\bar\zeta_\eta\bar\beta)\succeq0$, whose radical is exactly $\bar{\mathfrak g}_{\bar\beta}$." So (0.2) and the identification of its radical with the isotropy algebra are **ESTABLISHED, not new**. What is new is evaluating it on the **curvature** $F_{\mu\nu}$ and reading the result as a gauge-invariant Yang-Mills energy; grep over `Theory/*.tex` for `Yang-Mills|plaquette|Wilson|Killing form|Ad-invariant` returns **zero hits**, and `05c:1359-1366` explicitly refuses to build any scalar energy from these tensors ("A scalar gauged sigma energy would additionally require a base cometric, a base density, channel weights, boundary conditions, and a decision about whether the connection is fixed or dynamical. None is selected... \status{NOT-CLAIMED}").

---

## 1. The second-order pushforward-KL expansion  [DERIVATION]

Let $q_\varepsilon:=(\exp\varepsilon Y)_\#q$ and $L(\varepsilon,x):=\log\frac{dq_\varepsilon}{dq}(x)$, $L(0,\cdot)=0$. Under (H1) expand $L=\varepsilon L_1+\tfrac{\varepsilon^2}{2}L_2+\tfrac{\varepsilon^3}{6}L_3+O(\varepsilon^4)$ in $L^3(q)$, with $L_1=\psi_Y$. Normalization $\mathbb E_q[e^{L}]=\int dq_\varepsilon=1$ gives, order by order,
$$\mathbb E[L_1]=0,\qquad \mathbb E[L_2]=-\mathbb E[L_1^2],\qquad \mathbb E[L_3]=-3\mathbb E[L_1L_2]-\mathbb E[L_1^3]. \tag{1.1}$$
Since $D_{\rm KL}(q\|q_\varepsilon)=-\mathbb E_q[L]$,
$$D_{\rm KL}\big(q\,\big\|\,(\exp\varepsilon Y)_\#q\big)=\tfrac12\varepsilon^2\,\mathbb E_q[\psi_Y^2]+\tfrac{\varepsilon^3}{6}\Big(3\mathbb E_q[\psi_YL_2]+\mathbb E_q[\psi_Y^3]\Big)+O(\varepsilon^4). \tag{1.2}$$
The leading coefficient is $\tfrac12 g^F_q(Y.q,Y.q)=\tfrac12\langle Y,Y\rangle_q$, which is exactly claim (1) of the target. (The third-order coefficient is *not* the Amari–Chentsov tensor alone: `prop:pb-kl-divergence-jets`, Theory/05c:509-538, is a statement about **mixed** third jets; here both arguments move together and $L_2$ enters. I record the correct coefficient rather than the mis-citable one.)

**Numerical verification.** $K=3$, random $\Sigma\succ0$, $\mu$, $Y$; Gaussian KL in closed form against (1.2):
```
eps=1e-2  (KL - .5 eps^2 <Y,Y>)/eps^3 = 28.2933
eps=1e-3                              = 28.1520
eps=1e-4                              = 28.1382     (stable cubic constant)
Monte-Carlo (3e6) of (3 E[psi L2] + E[psi^3])/6      = 27.64   (agrees to MC/FD error)
```

**Plaquette.** With (H4), $H_P=\exp\!\big(h^2F_{\mu\nu}+h^3C+O(h^4)\big)$. Substituting into (1.2) with $\varepsilon Y\rightsquigarrow h^2F_{\mu\nu}+h^3C$ and expanding the quadratic form bilinearly,
$$D_{\rm KL}\big(q\,\|\,(H_P)_\#q\big)=\tfrac12h^4\|F_{\mu\nu}.q\|^2_{g^F(q)}+h^5\,g^F_q(F_{\mu\nu}.q,\,C.q)+O(h^6)=\tfrac12h^4\|F_{\mu\nu}.q\|^2_{g^F(q)}+O(h^5). \tag{1.3}$$

---

## 2. The $h^{d-4}$ weight  [DERIVATION — Riemann-sum consistency, NOT $\Gamma$-convergence]

A region of volume $|\mathcal C|$ carries $\sim|\mathcal C|h^{-d}$ sites and $P_d:=d(d-1)/2$ plaquette orientations per site. Assigning each plaquette weight $h^{d-4}$ and using (1.3),
$$\sum_{\text{plaquettes}}h^{d-4}\,D_{\rm KL}(q\|(H_P)_\#q)=\sum_{\text{sites}}h^{d}\sum_{\mu<\nu}\tfrac12\|F_{\mu\nu}.q\|^2_{g^F(q)}\;+\;\underbrace{O\!\big(h^{-d}\cdot h^{d-4}\cdot h^5\big)}_{=O(h)}$$
$$\longrightarrow\;\boxed{\;\tfrac12\int_{\mathcal C}\ \sum_{\mu<\nu}\big\|F_{\mu\nu}(c).q(c)\big\|^2_{g^F(q(c))}\,dc\;}\tag{2.1}$$
The error bound $O(h)$ **requires** (H5), uniformity of the $O(h^5)$ over plaquettes; without it the sum is uncontrolled. This is the same ceiling the prior run states for itself: "These are consistency expansions on smooth sequences, not $\Gamma$-convergence proofs" (`docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/lattice-continuum-asymptotics.md:33-34`). I claim no more.

**The metric is the answer to the target's second question.** (2.1) is Yang-Mills in the metric
$$m_q(F,F'):=g^F_q(F.q,F'.q)\ \ \text{on }\mathfrak g,$$
a **state-dependent, positive-semidefinite, $\mathrm{Ad}$-equivariant** bilinear form — *not* $\operatorname{tr}(F_{\mu\nu}F^{\mu\nu})$ and *not* $\|F\|_F^2$. Contrast the prior run's Wilson sector, which derives $r-\operatorname{Re}\operatorname{Tr}H_p=\tfrac12h^4\|F_{\mu\nu}\|^2_{\rm HS}+O(h^5)$ **"for a compact gauge group in a unitary representation"** (`lattice-continuum-asymptotics.md:25-32`). That is a *different metric* on a *strictly smaller class of groups*.

---

## 3. INVARIANCE — the payoff.  [FORMAL PROOF. Result: **INVARIANT**, not refuted.]

**Lemma 3.1 (pushforward is a Fisher isometry).** Let $g$ act on $\mathsf K$ by a bimeasurable bijection $r_g$, independent of the statistical parameter. If a tangent signed measure $\delta\mu$ has $q$-score $\psi$, then $(r_g)_\#\delta\mu$ has $(r_g)_\#q$-score $\psi\circ r_g^{-1}$, and
$$g^F_{(r_g)_\#q}\big((r_g)_\#\delta\mu,(r_g)_\#\delta\mu\big)=\mathbb E_{(r_g)_\#q}\big[(\psi\circ r_g^{-1})^2\big]=\mathbb E_q[\psi^2]=g^F_q(\delta\mu,\delta\mu).$$
*Proof.* For measurable $A$: $\big((r_g)_\#\delta\mu\big)(A)=\delta\mu(r_g^{-1}A)=\int_{r_g^{-1}A}\psi\,dq=\int_A(\psi\circ r_g^{-1})\,d\big((r_g)_\#q\big)$, which identifies the score; the second equality is change of variables. $\square$
This is precisely `prop:pb-statistical-tensor-descent`, Theory/05c:59-74 — an **APPLICABLE_THEOREM** whose hypotheses I have verified hold here (H2). Its proof there reads: "Pushforward defines the unitary map $L^2(p)\to L^2((r_g)_\#p)$ given by $f\mapsto f\circ r_g^{-1}$... The pushforward integration identity preserves the second and third score moments."

**Lemma 3.2 (equivariance of the fundamental vector).** For all $g\in G$, $Y\in\mathfrak g$, $q\in\mathcal B$:
$$(\mathrm{Ad}_gY).\big(g_\#q\big)\;=\;g_\#\big(Y.q\big).$$
*Proof.* $\displaystyle(\mathrm{Ad}_gY).(g_\#q)=\frac{d}{dt}\Big|_0\big(\exp(t\,gYg^{-1})\big)_\#(g_\#q)=\frac{d}{dt}\Big|_0\big(g\exp(tY)g^{-1}g\big)_\#q=\frac{d}{dt}\Big|_0 g_\#\big((\exp tY)_\#q\big)=g_\#\Big(\frac{d}{dt}\Big|_0(\exp tY)_\#q\Big)$, the last step because $\mu\mapsto g_\#\mu$ is linear and bounded (test weakly: $\langle g_\#\mu,\varphi\rangle=\langle\mu,\varphi\circ g\rangle$ and differentiate in $t$). $\square$

**Theorem 3.3 (conjugation invariance).** For every $g\in G$ and $Y,Z\in\mathfrak g$,
$$\langle \mathrm{Ad}_gY,\ \mathrm{Ad}_gZ\rangle_{g_\#q}=\langle Y,Z\rangle_q .$$
*Proof.* By Lemma 3.2 the two arguments are $g_\#(Y.q)$ and $g_\#(Z.q)$; by Lemma 3.1 the Fisher inner product of pushforwards equals the Fisher inner product of the originals. $\square$

**Corollary 3.4 (full local gauge invariance of the energy density).** Under a local gauge transformation $g(c)$, the plaquette based at $c$ transforms by conjugation, $H_P\mapsto g(c)H_Pg(c)^{-1}$, hence $F_{\mu\nu}(c)\mapsto\mathrm{Ad}_{g(c)}F_{\mu\nu}(c)$ (homogeneous — the curvature has **no** inhomogeneous $dg\,g^{-1}$ term), and the matter section transforms as $q(c)\mapsto g(c)_\#q(c)$. Both objects sit at the same base point and carry the same $g(c)$. By Theorem 3.3 the integrand of (2.1) is invariant **pointwise in $c$ for arbitrary local $g(c)$**, and the base measure $dc$ is untouched. $\square$

**What was NOT used:** compactness; an $\mathrm{Ad}$-invariant positive-definite form on $\mathfrak g$ (none exists on $\mathfrak{gl}(K,\mathbb R)$ — the Killing form $B(X,Y)=2K\operatorname{tr}(XY)-2\operatorname{tr}X\operatorname{tr}Y$ is indefinite); normalized Haar measure (absent for noncompact $G$); any gauge slice, quotient, or Jacobian. The form $m_q$ is not $\mathrm{Ad}$-**invariant**; it is $\mathrm{Ad}$-**equivariant**, and the belief $q$ is the object that carries the equivariance. That is why noncompactness is irrelevant.

**Therefore: this construction supplies a conjugation-invariant curvature energy for ANY closed subgroup of $GL(K,\mathbb R)$, including noncompact ones.** This directly resolves the standing obstruction recorded at `docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/adversarial-counterexamples.md:20-25` (CE-4: "$\|H-I\|_F^2$ is not invariant under $H\mapsto g^{-1}Hg$ in $GL(K)$... changes the norm by $t^{-2}$") and at `evidence/pifb2-sector-map.md:4-22` ("Raw $GL(K)$ positive curvature | Obstructed"). It also *supersedes* the guessed repair at `docs/derivations/2026-08-12-elbo-pifb2-fast-slow-program/evidence/compact-and-gl-group-program.md:14-30` — see §4.2.

**Explicit Gaussian verification of Theorem 3.3** (algebraic, no limits). With $q=\mathcal N(\mu,\Sigma)$, $g_\#q=\mathcal N(g\mu,g\Sigma g^{\!\top})$, $Y'=gYg^{-1}$, each of the three terms of the closed form (4.1) below is separately invariant:
- $\operatorname{tr}(Y'^2)=\operatorname{tr}(gY^2g^{-1})=\operatorname{tr}(Y^2)$;
- $\operatorname{tr}(\Sigma'Y'^{\!\top}\Sigma'^{-1}Y')=\operatorname{tr}\!\big(g\Sigma g^{\!\top}\cdot (g^{\!\top})^{-1}Y^{\!\top}g^{\!\top}\cdot(g^{\!\top})^{-1}\Sigma^{-1}g^{-1}\cdot gYg^{-1}\big)=\operatorname{tr}(g\,\Sigma Y^{\!\top}\Sigma^{-1}Y\,g^{-1})=\operatorname{tr}(\Sigma Y^{\!\top}\Sigma^{-1}Y)$;
- $\mu'^{\!\top}Y'^{\!\top}\Sigma'^{-1}Y'\mu'=\mu^{\!\top}g^{\!\top}(g^{\!\top})^{-1}Y^{\!\top}g^{\!\top}(g^{\!\top})^{-1}\Sigma^{-1}g^{-1}gYg^{-1}g\mu=\mu^{\!\top}Y^{\!\top}\Sigma^{-1}Y\mu$.

**Numerical verification** ($K=3$, four random $g=\exp(B)$, $B$ Gaussian, i.e. wildly noncompact):
```
det g=+0.9499 cond= 32.44  Fisher: 56.7912408543 -> 56.7912408543   Frobenius:  10.52 ->  975.79
det g=+0.0637 cond=349.20  Fisher: 56.7912408543 -> 56.7912408546   Frobenius:  10.52 -> 3846.66
det g=+1.9205 cond=  9.80  Fisher: 56.7912408543 -> 56.7912408543   Frobenius:  10.52 ->   95.08
det g=+22.013 cond=  3.19  Fisher: 56.7912408543 -> 56.7912408543   Frobenius:  10.52 ->   19.09
```
Ten-digit invariance of the Fisher form against a $366\times$ swing in the Frobenius energy.

---

## 4. The cost: degeneracy, isotropy, coercivity

### 4.1 Gaussian closed form  [FORMAL PROOF]

Take $q=\mathcal N(\mu,\Sigma)$, $\Sigma\succ0$, $V(x)=Yx$. From (0.1), with $z=x-\mu\sim\mathcal N(0,\Sigma)$,
$$\psi_Y(x)=z^{\!\top}\Sigma^{-1}Yz+z^{\!\top}\Sigma^{-1}Y\mu-\operatorname{tr}Y,\qquad \mathbb E[z^{\!\top}\Sigma^{-1}Yz]=\operatorname{tr}(\Sigma^{-1}Y\Sigma)=\operatorname{tr}Y\ \Rightarrow\ \mathbb E_q[\psi_Y]=0.$$
Quadratic$\times$linear cross terms are third central moments of a centered Gaussian, hence $0$. Using $\operatorname{Cov}(z^{\!\top}Az,z^{\!\top}Bz)=2\operatorname{tr}(A_s\Sigma B_s\Sigma)$ with $A_s=\tfrac12(\Sigma^{-1}Y+Y^{\!\top}\Sigma^{-1})$ and the identity $\Sigma(\Sigma^{-1}Z+Z^{\!\top}\Sigma^{-1})\Sigma=Z\Sigma+\Sigma Z^{\!\top}$, one gets $2\operatorname{tr}(A_s\Sigma B_s\Sigma)=\operatorname{tr}(YZ)+\operatorname{tr}(\Sigma Y^{\!\top}\Sigma^{-1}Z)$, and the linear part contributes $\mu^{\!\top}Y^{\!\top}\Sigma^{-1}Z\mu$. Hence
$$\boxed{\ \langle Y,Y\rangle_{\mathcal N(\mu,\Sigma)}=\operatorname{tr}(Y^2)+\operatorname{tr}\!\big(\Sigma Y^{\!\top}\Sigma^{-1}Y\big)+\mu^{\!\top}Y^{\!\top}\Sigma^{-1}Y\mu\ }\tag{4.1}$$
Substituting $Y=\Sigma^{1/2}W\Sigma^{-1/2}$, $w=\Sigma^{-1/2}\mu$ diagonalizes it:
$$\langle Y,Y\rangle_q=\operatorname{tr}(W^2)+\|W\|_F^2+|Ww|^2=\tfrac12\|W+W^{\!\top}\|_F^2+|Ww|^2\ \ \succeq 0. \tag{4.2}$$
*Numerical check:* trace form $56.79124085429073$, $W$-form $56.79124085429069$, Monte-Carlo $\mathbb E_q[\psi_Y^2]$ ($4\times10^6$ samples) $56.75$.

### 4.2 What the ELBO adds to the guessed repair  [decomposition]

Write $S=\tfrac12(W+W^{\!\top})$, $A=\tfrac12(W-W^{\!\top})$. Then
$$\underbrace{\langle Y,Y\rangle_q}_{\text{ELBO-derived}}=\underbrace{\|W\|_F^2}_{\text{= the prior run's }W_M(H),\ M=\Sigma^{-1}}+\underbrace{\operatorname{tr}(W^2)}_{\text{trace/Killing form — INDEFINITE}}+\underbrace{|Ww|^2}_{\text{mean sector}}=2\|S\|_F^2+|Ww|^2. \tag{4.3}$$
The middle term is $\operatorname{tr}(Y^2)$; on skew $W$ it equals $-\|W\|_F^2$ and exactly cancels the first. So:
- `compact-and-gl-group-program.md:14-30` proposes the SPD dressing $W_M(H)=\operatorname{Tr}[M^{-1}(H-I)^{\!\top}M(H-I)]$ with $M^g=g^{\!\top}Mg$. Setting $M=\Sigma^{-1}$ (the **belief precision**) reproduces the transformation law exactly and gives $h^4\|W\|_F^2$ — which is invariant **and strictly positive definite**. That run listed as unmet obligations "nondegeneracy of $M$, control of $D_AM$, a gauge quotient or slice, and a finite reference law". My result **supplies $M=\Sigma^{-1}$ canonically and derives it** rather than declaring it, and shows a gauge quotient/slice and a finite Haar reference are *not needed at all* (Theorem 3.3).
- But the honest trade is: the **ELBO forces the indefinite trace form to be added**, and that is exactly what makes the derived energy degenerate. Positive-definiteness and ELBO-derivability are in tension; the dressed Frobenius is definite but postulated, the Fisher form is derived but degenerate.

### 4.3 The isotropy algebra  [FORMAL PROOF]

$\psi_Y$ is a polynomial in $z$; since $\mathcal N(\mu,\Sigma)$ with $\Sigma\succ0$ has full support, $\psi_Y=0$ $q$-a.s. iff it vanishes identically. Matching degrees:
- quadratic: $\Sigma^{-1}Y+Y^{\!\top}\Sigma^{-1}=0\iff Y\Sigma+\Sigma Y^{\!\top}=0$;
- linear: $\Sigma^{-1}Y\mu=0\iff Y\mu=0$;
- constant: $\operatorname{tr}Y=0$, automatic from the first (if $S:=\Sigma^{-1}Y$ is skew then $\operatorname{tr}Y=\operatorname{tr}(\Sigma S)=-\operatorname{tr}(\Sigma S)=0$).

Hence
$$\operatorname{rad}\langle\cdot,\cdot\rangle_q=\mathfrak g_q=\{Y:\ Y\mu=0,\ Y\Sigma+\Sigma Y^{\!\top}=0\},\tag{4.4}$$
which is exactly the Lie algebra of $\operatorname{Stab}_G(q)=\{g:g\mu=\mu,\ g\Sigma g^{\!\top}=\Sigma\}$. (Consistent with 05c:946-949, "whose radical is exactly $\bar{\mathfrak g}_{\bar\beta}$", and with the orbit–stabilizer theorem on the finite-dimensional Gaussian manifold.) Equivalently by (4.2): $\langle Y,Y\rangle_q=0\iff W$ skew and $Ww=0$.

**Explicitly which curvature directions are invisible.** Parametrize $Y=\Sigma^{1/2}W\Sigma^{-1/2}$:
$$\mathfrak g_q\;\cong\;\{W\in\mathfrak{so}(K):\ Ww=0\}\;\cong\;\begin{cases}\mathfrak{so}(K-1),&\mu\ne0,\ \dim=\tfrac{(K-1)(K-2)}{2},\\[2pt]\mathfrak{so}(K),&\mu=0,\ \dim=\tfrac{K(K-1)}{2}.\end{cases}$$
So the invisible directions are precisely the **$\Sigma$-orthogonal rotations that fix the mean** — i.e. exactly the curvature that does not change what the agent believes. Notable consequences:
- $K=2,\ \mu\ne0$: $\dim\mathfrak g_q=0$; a **single** agent already gives a positive-definite form on all of $\mathfrak{gl}(2,\mathbb R)$. *(Numerics: eigenvalues $[0.1267,2.0013,2.5084,4.0321]$, rank $4/4$.)*
- $K=3,\ \mu\ne0$: $\dim=1$. *(Numerics: rank $8/9$, smallest eigenvalue $0$ to machine precision.)*
- $K=3,\ \mu=0$: $\dim=3=\mathfrak{so}(3)$. *(Numerics: rank $6/9$.)*
- **Compact-group blindness:** for $G=SO(K)$ in the standard representation and isotropic beliefs $q=\mathcal N(0,\sigma^2I)$, $\mathfrak g_q=\mathfrak{so}(K)\supseteq\mathfrak g$, so the Fisher–Yang-Mills energy is **identically zero**. Where the classical Wilson action is well-behaved, this one is vacuous; where the classical action fails ($GL$), this one works. They are complementary, not competing. *(Numerical witness: $Y_0$ skew-in-$\Sigma$ with $Y_0\mu=0$ has $\langle Y_0,Y_0\rangle_q=5.6\times10^{-17}$ while $\|Y_0\|_F^2=0.699$.)*
- **Uncertainty scaling:** under $\Sigma\mapsto t\Sigma$ at fixed $\mu$, $W$ is unchanged and $|Ww|^2\mapsto t^{-1}|Ww|^2$. High-uncertainty agents see less curvature, and the radical grows from $\mathfrak{so}(K-1)$ to (asymptotically) $\mathfrak{so}(K)$ at rate $t^{-1}$. Sharp beliefs ($\Sigma\to0$) give an unbounded coupling. The sector is **non-uniformly elliptic** in the belief.

### 4.4 Does summing over agents restore nondegeneracy?  [DERIVATION]

The total form at a base point is $m:=\sum_i w_i\langle\cdot,\cdot\rangle_{q_i}$, $w_i>0$. Each summand is $\succeq0$, so by polarization
$$\operatorname{rad}m=\bigcap_i\mathfrak g_{q_i}. \tag{4.5}$$
This is exactly the argument of `prop:pb-product-radical`, Theory/05c:289-297 ("the two degenerate channel tensors can jointly be nondegenerate exactly when their null distributions have zero intersection") — an **ESTABLISHED template**, applied here to $N$ agents rather than $2$ channels.

Compute the intersection. Conjugating by $\Sigma_1^{1/2}$ (legitimate: by Theorem 3.3 this moves every $\mathfrak g_{q_i}$ consistently) we may take $\Sigma_1=I$, so $\bigcap_i\mathfrak g_{q_i}\subseteq\{Y\ \text{skew}\}$ and the conditions become $[Y,\Sigma_i]=0$ and $Y\mu_i=0$ for all $i$.

**(a) Distinct covariances suffice — two agents, any $K$.** If $\Sigma_2$ (in the $\Sigma_1$-normalized frame) has $K$ distinct eigenvalues, then in its eigenbasis $[Y,\Sigma_2]_{ij}=Y_{ij}(\lambda_j-\lambda_i)=0$ forces $Y_{ij}=0$ for $i\ne j$, and skewness forces $Y_{ii}=0$; hence $Y=0$. **Two agents with generic distinct covariances make the total curvature form positive definite on all of $\mathfrak{gl}(K,\mathbb R)$.** More generally $\operatorname{rad}m=\{0\}$ whenever the commutant of $\{\Sigma_1^{-1/2}\Sigma_i\Sigma_1^{-1/2}\}$ contains no nonzero skew matrix — in particular whenever the $\Sigma_i$ generate $M_K(\mathbb R)$ as an algebra.
*(Numerics, $K=3$: $\mathcal N(0,I)$ alone $\to$ rank $6/9$; $\mathcal N(0,I)+\mathcal N(0,\operatorname{diag}(1,2,5))\to$ rank $\mathbf{9/9}$; $\mathcal N(0,I)+\mathcal N(0,\operatorname{diag}(1,1,3))$ (repeated eigenvalue) $\to$ rank $8/9$.)*

**(b) Equal covariances, distinct means.** With all $\Sigma_i=I$, $\bigcap_i\mathfrak g_{q_i}=\{Y\ \text{skew}:Y|_{V}=0\}$, $V=\operatorname{span}\{\mu_i\}$. A skew $Y$ killing $V$ maps everything into $V^\perp$, so $\bigcap\cong\mathfrak{so}(K-\dim V)$: trivial iff $\dim V\ge K-1$. **You need $K-1$ agents with independent means.**

**(c) The failure mode is dynamically selected — the decisive negative.** If $q_1=\cdots=q_N$ (consensus), (4.5) gives $\operatorname{rad}m=\mathfrak g_{q_1}$, of dimension $\ge(K-1)(K-2)/2$, nonzero for $K\ge3$. *(Numerics: two identical $\mathcal N(0,I)$ $\to$ rank $6/9$, no gain over one.)* Consensus is precisely what PIFB2's alignment terms $\beta_{ij}\mathrm{KL}(q_i\|\Omega_{ij}q_j)$ and $\gamma_{ij}\mathrm{KL}(s_i\|\widetilde\Omega_{ij}s_j)$ drive toward. **The degeneracy is not generic-in-measure-zero; it sits on the attractor of the rest of the action.**

**(d) Coercivity verdict.** Pointwise positive definiteness gives $m_c\succ0$ but not $\lambda_{\min}(m_c)\ge\lambda_0>0$. Since $\lambda_{\min}$ is a continuous function of $(\mu_i,\Sigma_i)$ vanishing on the consensus set and decaying like $t^{-1}$ under $\Sigma\mapsto t\Sigma$, **no uniform lower bound holds on belief-configuration space**, and the beliefs are themselves optimization variables. Therefore:
- **CONDITIONAL coercivity holds**: restrict the configuration space by a uniform eigenvalue-separation / anisotropy constraint (e.g. $\lambda_{\min}\big(\sum_i m_{q_i(c)}\big)\ge\lambda_0>0$ uniformly in $c$) and (2.1) is uniformly elliptic and coercive modulo gauge — enough for the direct method, given the remaining $\Gamma$-convergence obligations.
- **UNCONDITIONAL coercivity FAILS**: a minimizing sequence can drive the beliefs toward isotropic consensus (rewarded by the alignment terms) while $|F|\to\infty$ inside the growing radical at zero curvature cost.
- **Under PIFB2's own per-agent typing $F^{(i)}_{\mu\nu}$ (PIFB2.tex:429, :713) the repair (a) does not apply at all**: each term $\|F^{(i)}.q_i\|^2$ is tested only by its own agent's belief, and its radical $\mathfrak g_{q_i}$ is never intersected with anything. (H7) — a shared principal connection — is load-bearing.

---

## 5. Honest ELBO provenance  [DERIVATION + inherited COUNTEREXAMPLE]

### 5.1 The lagged self-loop **is** an exact ELBO term

In the closed theorem, the belief-relational block is (`docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/exact-elbo-proof.md:60-84`)
$$\mathcal F_a^q=D_{\rm KL}(\beta_a\|\pi_a^q)+\sum_{b\in J_a^q}\beta_{ab}\,D_{\rm KL}\big(q_a^{n+1}\,\big\|\,u^n_{ab}\big),\qquad u^n_{ab}=(\Omega^n_{ab})_\#q^n_b,$$
where $\Omega^n_{ab}:\mathsf K_b\to\mathsf K_a$ is *any* measurable transport stored in the history $H_n$ (`evidence/typed-construction.md:37-54`). Self-sources are admissible — the register speaks of "$N=1$ with self-sources **excluded**" as a special case (`evidence/boundary-counterexamples.md:76`), so $b=a$ is in scope.

**Take $b=a$ and $\Omega^n_{aa}:=H_P$, the plaquette holonomy at agent $a$'s site.** Then $u^n_{aP}=(H_P)_\#q^n_a$ is a genuine normalized probability law measurable w.r.t. $H_n$, every factor of $P^n_h$ remains normalized, and the exact ELBO of `exact-elbo-proof.md` contains, verbatim and with no approximation,
$$\boxed{\ \beta_{aP}\;D_{\rm KL}\!\Big(q_a^{n+1}\ \Big\|\ (H_P)_\#\,q_a^{n}\Big).\ }\tag{5.1}$$
This **is** ELBO-derived. A source-label block whose source law is the agent's own transported belief is structurally identical to a peer block; the only difference is that the transport is a closed loop and the source index is the agent itself. It is *not* self-referential, because the source is the **lagged** $q^n_a$ from the conditioned history, not the optimization variable.

### 5.2 The same-time loop is obstructed — the reciprocity obstruction reappears

The target's loop term $D_{\rm KL}(q_i\|(H_P)_\#q_i)$ has the **same** law on both sides. That requires the generative factor $u_{aP}=(H_P)_\#q^{n+1}_a$ to read the recognition law, so $P^n_h$ depends on $Q^{n+1}$, the fixed-joint hypothesis fails, and the identity $\mathcal F=-\log p(o)+\mathrm{KL}(Q\|P(\cdot|o))$ has no fixed $P$. This is exactly CE-6: "Replacing $q_b^n,s_b^n$ in the generative kernel by the current optimization variables $q_b^{n+1},s_b^{n+1}$ makes the purported fixed joint depend on its recognition law. The one-step ELBO proof then fails" (`evidence/boundary-counterexamples.md:68-73`); same mechanism as CE-1 of the fast-slow run and CE-3 of the effective-action run. **Answer to the target's question: yes — the same-time loop term is exactly the same-time reciprocity obstruction, and curvature is NOT ELBO-derivable by the same-time route.**

**A smeared conditional does not rescue it.** [DERIVATION, small negative] Suppose one tries a fixed joint $P(dx,dx')=m(dx)\,k(x,dx')$ with tied recognition $Q=q\otimes q$ (same $q$ on both copies). Then
$$D_{\rm KL}(Q\|P)=D_{\rm KL}(q\|m)+\mathbb E_{x\sim q}\,D_{\rm KL}\big(q\,\|\,k(x,\cdot)\big)=D_{\rm KL}(q\|m)-H(q)-\mathbb E_{x\sim q}\mathbb E_{x'\sim q}\log k(x,x').$$
Matching this to $D_{\rm KL}(q\|(H_P)_\#q)=-H(q)-\mathbb E_{x'\sim q}\log\big((H_P)_\#q\big)(x')$ forces $\mathbb E_{x\sim q}\log k(x,x')=\log\big((H_P)_\#q\big)(x')$ for a.e. $x'$, i.e. $k(x,\cdot)\equiv(H_P)_\#q$ — the same-time dependence again. **Within the label-copy family, the marginal $(H_P)_\#q$ cannot be replaced by any conditional kernel.** The lag is the only exact route.

### 5.3 What (5.1) actually equals off the diagonal, and the screening theorem  [DERIVATION under (H10)]

Let $q^n=q_{\theta_0}$, $q^{n+1}=q_{\theta_0+\Delta}$, and let $v_F$ be the parameter representative of $F_{\mu\nu}.q$ (the Gaussian family is $GL(K)$-closed, so $(H_P)_\#q_{\theta_0}=q_{\theta_0+h^2v_F+O(h^3)}$). Then
$$D_{\rm KL}\big(q^{n+1}\|(H_P)_\#q^n\big)=\tfrac12\big\|\Delta-h^2v_F\big\|^2_{g^F}+O(\|\cdot\|^3). \tag{5.2}$$
Setting $\Delta=0$ recovers $\tfrac12h^4\|F.q\|^2$ — **the pure curvature term is the diagonal value of the exact lagged term, nothing more.** Off the diagonal (5.2) is minimized to **zero** at $\Delta=h^2v_F$: *by itself, the loop term is not a curvature penalty at all; the belief simply follows the holonomy.* The curvature energy is whatever survives after profiling against the belief-pinning terms $\mathrm{KL}(q_a\|p_a)$, $-\mathbb E\log\ell_a$, and the peer alignment.

**Screening theorem (quadratic model, (H10)).** Let the non-loop terms be $\tfrac12\|\Delta\|^2_{M}$ with $M=m\,g^F$, $m>0$, and let the site carry $P_d=d(d-1)/2$ plaquettes each at weight $n$. Minimizing $\tfrac{m}{2}\|\Delta\|^2+\tfrac n2\sum_P\|\Delta-h^2v_P\|^2$ gives $\Delta^\ast=\frac{nh^2}{m+P_dn}\sum_Pv_P$ and profiled value
$$\mathcal S_{\rm eff}=\tfrac{h^4}{2}\Big[n\textstyle\sum_P\|v_P\|^2-\tfrac{n^2}{m+P_dn}\big\|\sum_Pv_P\big\|^2\Big]\ \xrightarrow[\ n/m\to\infty\ ]{}\ \tfrac{n h^4}{2}\sum_P\big\|v_P-\bar v\big\|^2,\quad \bar v=\tfrac1{P_d}\textstyle\sum_Pv_P.$$
*(Numerically verified: $P_d=3$, $m=1$; profiled $\to$ $\tfrac n2\sum\|v-\bar v\|^2$ to 5 digits at $n=10^6$, versus unprofiled $\tfrac n2\sum\|v\|^2$, ratio $0.5865$.)*
Reading:
- **The belief screens exactly one direction: the site-average curvature $\bar F$.** The deviatoric part survives with an unreduced coefficient. No saturation for $P_d\ge2$, i.e. $d\ge3$.
- **In $d=2$, $P_d=1$ and $\bar v=v_1$: the screening is TOTAL.** To leading order the ELBO-derived curvature sector vanishes identically after belief relaxation. $d=2$ is exactly PIFB2's working base ("The base manifold is flat, $\mathcal C=\mathbb R^2$ with Euclidean geometry", PIFB2.tex:434). **In the deployed base dimension, this route yields no curvature action.**
- If instead one reads (2.1) as a *deterministic action* in $(A,q)$ with no profiling, no screening occurs and the full $\tfrac{n}{2}h^4\sum_P\|v_P\|^2$ stands. The two readings genuinely differ; the ELBO reading is the profiled one.

### 5.4 The $h^{d-4}$ weight inside a normalized ELBO  [DERIVATION]

In (5.1) the coefficient is $\beta_{aP}\in[0,1]$ with $\sum_b\beta_{ab}=1$. So the weight $h^{d-4}$ is **not** representable as an attention weight when $d<4$ (it exceeds $1$ and diverges as $h\to0$). Two consequences:
- **$d\ge4$**: $h^{d-4}\le1$, representable directly by an attention weight; $d=4$ is the marginal case with weight $\equiv1$ — the classical Yang-Mills critical dimension recovered from ELBO bookkeeping.
- **$d<4$**: use replication. `boundary-counterexamples.md:52-59` records "Positive integer coefficients can be represented by repeated independent copies with tied recognition". Take $n_h=\lceil h^{d-4}\rceil$ **dedicated single-source replica blocks** per plaquette per agent; with a single source, $\pi_{aP}=1$ forces $\beta_{aP}=1$ and $\mathrm{KL}(\beta\|\pi)=0$, so each block contributes exactly $D_{\rm KL}(q^{n+1}_a\|(H_P)_\#q^n_a)$ with unit coefficient and $n_h$ of them give coefficient $n_h$. The rounding error is $\le1$, i.e. relative $O(h^{4-d})\to0$. **Cost:** the generative inventory grows like $h^{d-4}$, and $N\to\infty$ is explicitly outside the closed theorem's scope (`typed-construction.md:6-7`). This is a genuine construction, not a notational weight: it avoids the trap of `boundary-counterexamples.md:60-66` ("Multiplying a site term by a cell volume $w_x$ changes its probabilistic meaning unless the generative law is changed by replication, tempering, or an explicitly normalized weighted model") by using replication, which that same passage licenses.

---

## 6. Verdict on T-CURV

| Sub-target | Verdict |
|---|---|
| (1) $\tfrac12\varepsilon^2 g^F_q(Y.q,Y.q)+O(\varepsilon^3)$; $\tfrac12h^4\|F.q\|^2+O(h^5)$ | **DERIVED**, numerically verified |
| (2) $h^{d-4}$ $\Rightarrow$ Fisher-weighted Yang-Mills integral | **DERIVED** as Riemann-sum consistency under a uniform remainder; **not** $\Gamma$-convergence |
| (3) Conjugation invariance for noncompact $GL(K)$ | **PROVED. NOT REFUTED.** Full local gauge invariance, no compactness, no Haar, no slice |
| (4) Degeneracy = isotropy algebra; multi-agent repair | **PROVED** (Gaussian closed form, $\mathfrak{so}(K-1)/\mathfrak{so}(K)$); repair works with $\ge2$ generic covariances **and one shared connection**; **unconditional coercivity FAILS**, degeneracy sits on the consensus attractor |
| (5) Exact ELBO provenance | **PARTIAL**: lagged self-loop exact; same-time loop **obstructed** (reciprocity); pure loop term is the diagonal value only; belief screening kills it entirely at $d=2$ |

**Net:** curvature **is** ELBO-derivable, but only as a *lagged* self-source block, and the honest object is not $\int\operatorname{tr}(F_{\mu\nu}F^{\mu\nu})$ nor $\int\|F\|_F^2$ but $\int\sum_{\mu<\nu}\|F_{\mu\nu}.q\|^2_{g^F(q)}$ — degenerate on the belief's isotropy algebra, screened by the belief update, but **exactly conjugation-invariant for arbitrary noncompact structure groups**. The invariance result stands on its own and is the piece worth exporting.

## obstructions

### 1

SAME-TIME LOOP IS NOT ELBO-DERIVABLE. The pure loop term KL(q||(H_P)_# q) with the same law on both sides forces the generative factor to read the recognition law, breaking the fixed-joint hypothesis. This is CE-6 verbatim (docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/boundary-counterexamples.md:68-73). The only exact route is the lagged term KL(q^{n+1} || (H_P)_# q^n), whose value equals the loop term only on the diagonal q^{n+1}=q^n. I also proved (DERIVATION, section 5.2) that no conditional/smeared kernel k(x,.) can substitute for the marginal (H_P)_# q inside a label-copy block, so the lag is the unique escape within this family.

### 2

BELIEF SCREENING. Under the quadratic-model hypothesis (H10), profiling the exact lagged term over the belief update leaves only the deviation of each plaquette from the site-average curvature. In base dimension d=2 there is exactly ONE plaquette orientation, so the screening is total and the ELBO-derived curvature sector vanishes to leading order. d=2 is PIFB2's deployed base (PIFB2.tex:434). The sector is nonvacuous only for d >= 3.

### 3

UNCONDITIONAL COERCIVITY FAILS, AND THE FAILURE IS DYNAMICALLY SELECTED. rad(sum_i m_{q_i}) = intersection_i g_{q_i}, which equals g_{q_1} (dimension >= (K-1)(K-2)/2, nonzero for K >= 3) on the consensus configuration q_1 = ... = q_N. Consensus is the attractor of PIFB2's own alignment terms. lambda_min also degenerates like t^{-1} under Sigma -> t Sigma. So no uniform ellipticity bound exists on belief-configuration space and no unconditional existence-of-minimizers theorem follows. Only a CONDITIONAL coercivity statement survives (restrict to a uniform anisotropy/eigenvalue-separation set).

### 4

PER-AGENT CURVATURE KILLS THE MULTI-AGENT REPAIR. The nondegeneracy argument requires a single shared principal connection so that one F is tested against all beliefs. PIFB2 writes a per-agent F^{(i)}_{munu} (PIFB2.tex:429, :713). Under that typing each term ||F^{(i)}.q_i||^2 has radical g_{q_i} and nothing intersects it; the sector is degenerate for every K >= 3.

### 5

COMPACT-GROUP BLINDNESS. For G = SO(K) in the standard representation with isotropic beliefs N(0, sigma^2 I), the isotropy algebra is all of so(K) and the Fisher-Yang-Mills energy is identically zero. The construction is complementary to the classical Wilson action (lattice-continuum-asymptotics.md:25-32, compact unitary reps only), not a strict generalization of it.

### 6

THE PLAQUETTE EXPANSION IS NOT ELBO-DERIVED. H_P = exp(h^2 F + O(h^3)) is the standard lattice BCH identity but enters here as hypothesis (H4), of exactly the status of lattice-continuum-asymptotics.md:4-9. Nothing in any ELBO produces it. The h^{d-4} counting is Riemann-sum consistency and requires an unproved uniformity of the O(h^5) remainder over plaquettes (H5).

### 7

CONTINUUM LIMIT REMAINS FULLY OPEN. The closed theorem is finite-N with 'Refining the base and taking N -> infinity are not part of this construction' (typed-construction.md:6-7). Everything in section 2 is outside its certified scope. All the standing obligations remain: common interpolation topology, equicoercivity modulo gauge, liminf, recovery, boundary/topology control, uniformly vanishing truncation residual (lattice-continuum-asymptotics.md:33-37), plus the separate process-law ELBO obligation (release.json:10-15).

### 8

THE SECTOR IS VACUOUS IN THE DEPLOYED ACTION FOR AN INDEPENDENT REASON. In Regime I, Omega_ij = exp(phi_i)exp(-phi_j) is a flat Cech coboundary, so H_P = I identically and every loop KL is exactly zero (PIFB2.tex:142, :353, :434). Regime-II promotion is required, and PIFB2's checked-in pairwise twist scale and learning rate are zero (:418, :449 per ground extract). Nothing here changes that.

### 9

ELBO-DERIVABILITY AND POSITIVE-DEFINITENESS ARE IN TENSION. The decomposition <Y,Y>_q = ||W||_F^2 + tr(W^2) + |Ww|^2 shows the ELBO forces the indefinite trace (Killing-type) form tr(W^2) to be added to the positive-definite dressed Frobenius ||W||_F^2, and it is exactly that addition which creates the radical. A definite invariant exists (the dressing alone) but is postulated; the derived one is degenerate. There is no route in this construction that gives both.


## novelty

"MIXED. Three ingredients are ALREADY IN Theory/ and I do not claim them: (i) the bilinear form itself and the identification of its radical with the isotropy algebra - Theory/05c_pullback_geometry.tex:946-949, 'k_{barbeta}(xi,eta) = bar g^F(bar zeta_xi bar beta, bar zeta_eta bar beta) >= 0, whose radical is exactly bar g_{bar beta}' (inside thm:pb-isotropy-criterion, :921-949); (ii) invariance of g^F under the represented action - prop:pb-statistical-tensor-descent, Theory/05c:59-74, whose proof is the pushforward-unitary argument I reuse as Lemma 3.1; (iii) the polarization argument that a sum of PSD forms is nondegenerate iff the radicals intersect trivially - prop:pb-product-radical, Theory/05c:289-308 (two-channel version). NEW, and absent from both Theory/ and all three prior runs: (a) the evaluation of that form on the CURVATURE, i.e. the Fisher-weighted Yang-Mills energy int sum_{mu<nu} ||F_munu . q||^2_{g^F(q)} dc - grep over Theory/*.tex for 'Yang-Mills|plaquette|Wilson|Killing form|Ad-invariant' returns ZERO hits, and Theory/05c:1359-1366 explicitly refuses to construct any scalar energy from these tensors (\\status{NOT-CLAIMED}); (b) Theorem 3.3, that this energy is conjugation-invariant for NONCOMPACT closed subgroups of GL(K,R) with no Ad-invariant form, no Haar measure and no gauge slice - this directly resolves the sector listed as 'Raw GL(K) positive curvature | Obstructed' at docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/pifb2-sector-map.md:4-22, and answers the gap flagged at docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/gauge-invariance-proof.md:50-52 ('Compactness becomes important only when one integrates over dynamical links or frames using a normalized Haar reference and seeks coercive curvature actions'); (c) the explicit Gaussian closed form (4.1)-(4.2) and the isotropy algebra so(K-1)/so(K); (d) the decomposition (4.3) showing that the prior run's guessed SPD dressing W_M(H)=Tr[M^{-1}(H-I)^T M (H-I)] with M^g = g^T M g (docs/derivations/2026-08-12-elbo-pifb2-fast-slow-program/evidence/compact-and-gl-group-program.md:14-30) is exactly the middle term with M = Sigma^{-1} the belief precision - so that run's four unmet obligations ('nondegeneracy of M, control of D_A M, a gauge quotient or slice, and a finite reference law') are answered by deriving M rather than declaring it, at the cost of the indefinite trace term the ELBO forces alongside it; (e) the multi-agent nondegeneracy criterion and its two-agent sufficiency; (f) the belief-screening theorem and the d=2 total-screening result; (g) the h^{d-4} replica accounting inside a normalized ELBO row. Note the prior Wilson result (lattice-continuum-asymptotics.md:25-32) is a DIFFERENT metric (Frobenius/HS) on a strictly smaller class (compact groups in unitary reps) and is not superseded so much as complemented."

## next_obligations

### 1

Prove or refute a UNIFORM spectral-gap hypothesis: characterize the subset of belief configurations on which lambda_min(sum_i w_i <.,.>_{q_i}) >= lambda_0 > 0 uniformly in c, and determine whether the rest of the PIFB2 action (alignment + observation + precision sector) keeps a minimizing sequence inside it. Without this there is no existence-of-minimizers theorem for the Fisher-Yang-Mills sector.

### 2

Decide the connection typing. Prove the multi-agent nondegeneracy repair either (i) for one shared principal connection - in which case state the bundle hypothesis explicitly and reconcile it with PIFB2's per-agent F^{(i)} at :429, :713 - or (ii) show it fails under per-agent connections and record that as the operative case for the reference implementation.

### 3

Remove hypothesis (H10). The screening theorem is a local quadratic-model computation. Derive the profiled curvature action from the actual coupled stationarity conditions of the full lagged ELBO (self + observation + peer alignment + loop), including the cross-agent coupling that makes the belief Hessian non-block-diagonal, and verify or overturn the d=2 total-screening conclusion.

### 4

Supply the uniformity in (H5). Prove a uniform-in-plaquette bound on the O(h^5) remainder of (1.3) under stated third-derivative domination and uniform-mesh hypotheses; without it the h^{-d} x h^{d-4} x O(h^5) = O(h) error estimate is not established.

### 5

Extend beyond Gaussian fibers. The closed form (4.1) and the so(K-1)/so(K) radical are Gaussian-specific. Compute <Y,Y>_q and its radical for at least one non-Gaussian exponential family closed under a GL action, and check whether the radical is still exactly the isotropy algebra (05c:946-949 says yes in general; verify the score-integrability hypothesis (H3) is not doing hidden work).

### 6

Formulate the sector as a gauge-invariant OBSERVABLE, not just an invariant density. compact-and-gl-group-program.md:28-30 requires 'Any complexity growth must be formulated as a gauge-invariant observable before it is physical'. Determine whether int sum_{mu<nu} ||F.q||^2 dc, being a genuine gauge scalar, discharges that obligation, and whether a normalized Gibbs law exp(-S) on the noncompact link variables now exists (the invariance removes the Haar obstruction for the ACTION but not for the reference MEASURE - that remains open).

### 7

Close or refute the d>=3 continuum limit for the deviatoric (screened) sector: equicoercivity modulo gauge, liminf, recovery sequence, boundary/topology control, and a uniformly vanishing truncation residual, on the conditional-coercivity set from obligation 1. Then separately the process-law ELBO (release.json:10-15 items 3-4).

### 8

Check whether the lagged self-loop block (5.1) is consistent with the exact-image-invariance criterion Theory/07b_agent_network_rg.tex:1487-1496 under coarse-graining, i.e. whether the plaquette sector is closed under the RG step or generates hyperedges (07b:1530-1565). If it generates, the sector is a truncation with a residual and the h^{d-4} scaling is scheme-dependent.


## evidence_kind

FORMAL_PROOF (item 3, gauge invariance: Lemmas 3.1-3.2 + Theorem 3.3, plus an independent explicit algebraic verification in the Gaussian case and 10-digit numerical confirmation under noncompact GL(3,R) with condition numbers up to 349); FORMAL_PROOF (item 4a/4b, Gaussian closed form and isotropy algebra, by polynomial-identity argument on the score, cross-checked against Monte Carlo and eigen-rank computations); DERIVATION (items 1, 2, 4c, 5, with all steps given); APPLICABLE_THEOREM (Theory/05c:59-74 prop:pb-statistical-tensor-descent for Fisher invariance, hypotheses verified at (H2); Theory/05c:289-308 prop:pb-product-radical as the polarization template; Theory/05c:946-949 for radical = isotropy algebra); COUNTEREXAMPLE (item 4d, consensus configuration defeats coercivity; compact-isotropic configuration annihilates the energy identically); inherited COUNTEREXAMPLE (item 5, boundary-counterexamples.md:68-73 same-time reciprocity). Numerical work is confirmatory only and closes nothing: scripts at C:/Users/CHRISA~1/AppData/Local/Temp/claude/C--Users-chris-and-christine-Desktop-MultiAgentELBO/0ad1292e-01a7-43f7-8c22-fc72b0c10f6c/scratchpad/curv.py and curv2.py.
