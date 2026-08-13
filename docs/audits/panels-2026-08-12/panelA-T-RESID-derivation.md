# panelA-T-RESID-derivation

*Recovered verbatim from workflow journal.jsonl, 2026-08-13. Agent a0329fa7.*

## target

T-RESID — make $S_h^{\rm exact}=S_h^{\rm PIFB}+\varepsilon_h+c_h$ non-tautological by taking the tied-replica law of the exact two-channel run as the microscopic law, defining $C_h$ explicitly, and computing $\varepsilon_h$ and $c_h$ in closed form.

## status

PROVED

## theorem_statement

**Theorem (Residual dichotomy for the tied-replica microscopic law).**

Let $A$ be finite. Assume (H1)–(H6) below. Let $P_h^n=\bigotimes_{a\in A}P_a^n$ be the tied-replica generative joint of `typed-construction.md:71-85`, let $o=(o_a)$ be the admitted observation, and let $\Pi_{h,o}=P_h^n(\cdot\mid o,H_n)$ be its normalized posterior on $Z_h=\prod_a(\mathsf K_a\times\mathsf M_a\times J_a^q\times\mathsf K_a\times J_a^s\times\mathsf M_a)$.

**(0) Posterior block factorization.** $\Pi_{h,o}=\bigotimes_a\big[\pi_a^{\rm post}(dk,dm)\otimes\pi^q_{aj}u^n_{aj}(dx)\otimes\pi^s_{a\ell}v^n_{a\ell}(dy)\big]$ with $\pi_a^{\rm post}(dk,dm)=\ell_a(o_a\mid k,m)p_a(dk)r_a(dm)/p_a(o_a)$. The two replica blocks are *unchanged by conditioning on $o$*.

**(1) Blockwise-product rigidity (no generated multi-agent operator, at any order).** For **every** measurable blockwise coarse map $C_h(z)=(c_a(z_a))_{a\in A}$ and every product reference $\nu_h=\bigotimes_a\nu_a$ with $(C_h)_\#\Pi_{h,o}\sim\nu_h$, the exact effective action $S_h=-\log\frac{d(C_h)_\#\Pi_{h,o}}{d\nu_h}$ is $\nu_h$-a.e. a **sum of one-body terms** $S_h=\sum_a S_a(x_a)$. Consequently every Hoeffding–Möbius interaction component of $S_h$ relative to $\nu_h$ vanishes: $\Phi_B\equiv 0$ for all $|B|\ge 2$ ($\|S_h\|_{\mathcal G}$ is carried entirely by singletons). *No 3-body, no nonlocal, no cross-agent operator is ever generated.*

**(2) Label-retaining contraction: exact closure, $\varepsilon_h=0$, $c_h=0$.** If $c_a$ retains the source labels $(J^q_a,J^s_a)$ together with $(K_a,M_a,X_a,Y_a)$ (in particular $C_h={\rm id}$), then with $\nu_a=(p_a\otimes r_a)\otimes({\rm unif}_{J^q_a}\otimes\lambda_a)\otimes({\rm unif}_{J^s_a}\otimes\mu_a)$,
$$S_a = \underbrace{-\log\ell_a(o_a\mid k,m)}_{\text{PIFB2 observation}}\ \underbrace{-\log\pi^q_{aj}}_{\text{PIFB2 row prior}}\ \underbrace{-\log u_{aj}(x)}_{\text{PIFB2 peer energy}}\ \underbrace{-\log\pi^s_{a\ell}-\log v_{a\ell}(y)}_{\text{model channel}}+\text{const},$$
and $\mathcal F^X_h(R_h;o)=\mathbb E_{R_h}S_h-H_{\nu_h}(R_h)+\log Z_h-\log p_h(o)$ reproduces $\mathcal F^{\rm lag,1}_{\rm PIFB2,h}+\sum_a I_{\zeta_a}(K_a;M_a)$ **exactly**. Hence $\varepsilon_h=0$ and $c_h=0$: the tied-replica law closes exactly on the PIFB2 operator basis at $\tau=1$, unit private coefficients.

**(3) Label-marginalizing contraction: exact nonzero residual in closed form.** If $c_a(z_a)=(k,m,x,y)$ (labels integrated out, copies retained), then $(C_h)_\#\Pi_{h,o}=\bigotimes_a\pi^{\rm post}_a\otimes\bar u_a\otimes\bar v_a$ with $\bar u_a=\sum_j\pi^q_{aj}u^n_{aj}$, and relative to the PIFB2 peer basis $\{E_{aj}=-\log u_{aj}\}$ with prior coefficients,
$$\boxed{\ \varepsilon_a(x)\;=\;\log\frac{\prod_j u_{aj}(x)^{\pi^q_{aj}}}{\sum_j\pi^q_{aj}u_{aj}(x)}\;\le\;0\ }\qquad(\text{AM–GM / log-partition gap}),$$
plus the identical expression in $(v,y)$; $c_h=0$ for the unnormalized projection, and $c_h=-\sum_a\log Z_a^{q}Z_a^{s}\ \ge 0$ for the normalized (product-of-experts) projection, where $Z^q_a=\int\prod_j u_{aj}^{\pi^q_{aj}}d\lambda_a\in(0,1]$ is the weighted Bhattacharyya–Chernoff overlap (Hölder). Exactly:
$$\mathbb E_{R_h}[\varepsilon_h]=-\sum_a\Big[\mathbb E_{q_a}D_{\rm KL}\big(\pi^q_a\,\big\|\,\pi^{q,\rm post}_a(\cdot\mid X_a)\big)+\mathbb E_{s_a}D_{\rm KL}\big(\pi^s_a\,\big\|\,\pi^{s,\rm post}_a(\cdot\mid Y_a)\big)\Big],$$
and $\varepsilon_a\equiv0$ **iff** $u_{aj}=\bar u_a$ $\lambda_a$-a.e. for every $j\in\operatorname{supp}\pi^q_a$ (equivalently $X_a\perp J^q_a$ under $\Pi_{h,o}$).

**(4) Leading generated operator.** The cumulant expansion of $\varepsilon_a$ is $\varepsilon_a=-\tfrac12\kappa_2+\tfrac16\kappa_3-\cdots$ with $\kappa_n$ the cumulants of $E_{aJ}(x)$, $J\sim\pi^q_a$. Its leading term is the **two-source log-likelihood-ratio quadratic**
$$-\tfrac12\kappa_2(x)=-\tfrac14\sum_{j,j'}\pi^q_{aj}\pi^q_{aj'}\Big(\log\tfrac{u_{aj'}(x)}{u_{aj}(x)}\Big)^2 ,$$
which is quadratic in the attention row and therefore **outside the span of PIFB2's action** (linear in $\beta$ plus $\tau\beta\log\beta$). In expectation it splits exactly as
$$\mathbb E_{q_a}\big[-\tfrac12\kappa_2\big]=\underbrace{-\tfrac12\operatorname{Var}_{\pi^q_a}(D_{a\cdot})}_{\text{PIFB2's own }-\log Z_a\text{ at }\tau=1}\ \underbrace{-\tfrac14\sum_{j,j'}\pi^q_{aj}\pi^q_{aj'}\operatorname{Var}_{q_a}\!\log\tfrac{u_{aj'}}{u_{aj}}}_{\text{genuinely non-PIFB2}},\qquad D_{aj}=D_{\rm KL}(q_a\|u^n_{aj}).$$

**(5) Ordering theorem.** $\;D_{\rm KL}(q_a\|\bar u_a)\ \le\ -\log\sum_j\pi^q_{aj}e^{-D_{aj}}\ \le\ \sum_j\pi^q_{aj}D_{aj}$, the middle being PIFB2's envelope-reduced row $-\tau\log Z_a$ at $\tau=1$; the right gap is exactly $D_{\rm KL}(\pi^q_a\|\beta^*_a)$, the left gap is the Jensen gap of the concave $E\mapsto-\log\sum_j\pi_je^{-E_j}$ along $q_a$.

**(6) Lattice asymptotics (negative result).** Under the link-consistency/smoothness hypothesis (H7), writing $\log u_{aj}=\log q_a+hg_j+O(h^2)$, $\mathbb E_{q_a}g_j=0$:
$$\sum_j\pi_{aj}D_{aj}=\tfrac{h^2}{2}\textstyle\sum_j\pi_{aj}\operatorname{Var}_{q_a}(g_j)+O(h^3),\qquad D_{\rm KL}(q_a\|\bar u_a)=\tfrac{h^2}{2}\operatorname{Var}_{q_a}(\bar g)+O(h^3),\ \ \bar g=\textstyle\sum_j\pi_{aj}g_j,$$
$$\mathbb E_{q_a}\varepsilon_a=-\tfrac{h^2}{2}\,\mathbb E_{q_a}\!\operatorname{Var}_{\pi_a}(g_J)+O(h^3),\qquad c_a=-\log Z^q_a=\tfrac{h^2}{2}\big[\textstyle\sum_j\pi_{aj}\operatorname{Var}_{q_a}g_j-\operatorname{Var}_{q_a}\bar g\big]+O(h^3).$$
On a **balanced stencil** ($\bar g\equiv0$: symmetric neighbour set with symmetric row — the generic lattice case) the residual **exactly cancels the retained peer sector at leading order**, and the exact contracted relational action is $O(h^4)$, not $O(h^2)$. Under the $h^{d-2}$ edge weight of `lattice-continuum-asymptotics.md:20-22` PIFB2's Fisher–Dirichlet peer term survives at $O(1)$ while the exact contracted term $\to0$ like $O(h^2)$. **Therefore the Fisher-covariant Dirichlet peer sector is not generated by contracting the tied-replica law onto the replica coordinates.** Exact closed-form witness ($q=N(0,1)$, $u_\pm=N(\pm h,1)$, $\pi=(\tfrac12,\tfrac12)$): $\sum_j\pi_jD_{aj}=h^2/2$ exactly, while $D_{\rm KL}(q\|\bar u)=\tfrac{h^2}{2}-\mathbb E\log\cosh(hX)=\tfrac{h^4}{4}+O(h^6)$.

## hypotheses

### 1

(H1) $A$ finite and nonempty; $\mathsf K_a,\mathsf M_a,\mathsf O_a$ standard Borel; the tied-replica data $(p_a,r_a,L_a,\Omega^n_{ab},\widetilde\Omega^n_{ab},q^n_b,s^n_b)$ as declared at typed-construction.md:9-54, conditional on the history $H_n$.

### 2

(H2) $J^q_a,J^s_a$ finite and nonempty; $\pi^q_a,\pi^s_a$ strictly positive normalized rows (typed-construction.md:56-59; an all-zero row is excluded, boundary-counterexamples.md:76-79).

### 3

(H3) Positive finite evidence: $0<p_a(o_a)=\int\ell_a(o_a\mid k,m)p_a(dk)r_a(dm)<\infty$, and $\ell_a(o_a\mid\cdot,\cdot)>0$ $p_a\otimes r_a$-a.e. (the strict positivity is needed only for the equivalence $(C_h)_\#\Pi_{h,o}\sim\nu_h$ that the Hoeffding-Mobius statement (1) requires; absolute continuity alone suffices for (2),(3)).

### 4

(H4) $Q^{n+1}\ll\Pi_{h,o}$; equivalently $\zeta_a\ll p_a\otimes r_a$ and $q_a\ll u^n_{aj}$, $s_a\ll v^n_{a\ell}$ for every $j,\ell$ with positive recognition weight. All displayed terms finite, or extended-real conventions as at exact-elbo-proof.md:10-12.

### 5

(H5) [levels 2,3 only] A sigma-finite $\lambda_a$ on $\mathsf K_a$ with $u^n_{aj}\ll\lambda_a$ for all $j$, with densities written $u_{aj}$; likewise $\mu_a,v_{a\ell}$. For $\varepsilon_a$ to be finite $\lambda_a$-a.e. one needs $\{u_{aj}\}_{j\in\mathrm{supp}\,\pi^q_a}$ mutually equivalent; if two transported sources have disjoint supports then $\varepsilon_a=-\infty$ on a set of positive measure and the PIFB2 projection is not finite. (This is the measure-theoretic form of the hard-support caveat at boundary-counterexamples.md:76-79.)

### 6

(H6) [statement (1) only] The reference $\nu_h$ is a PRODUCT PROBABILITY measure, factorizing over $a$ and over the retained per-agent coordinates, with $(C_h)_\#\Pi_{h,o}\sim\nu_h$. This is exactly the premise the Hoeffding-Mobius projectors of 07b_agent_network_rg.tex:1193-1214 require ($\mathcal H_{\ell,A}=P_{\ell,A}L^\infty(\nu_\ell)$ with $\nu_\ell$ product). It is SATISFIED here by construction because $\Pi_{h,o}$ itself is a product; it is NOT automatic in general (07b:1160-1180 diagonal-cloning counterexample).

### 7

(H7) [statement (6) only] Link-consistency and smoothness: $\log u_{aj}=\log q_a+h g_j+\tfrac{h^2}{2}w_j+O(h^3)$ with $g_j,w_j\in L^2(q_a)$, $\mathbb E_{q_a}g_j=0$, and remainders uniform in $x$ on $\mathrm{supp}\,q_a$ and uniform over edges. This is the ASSERTED (not derived) hypothesis of lattice-continuum-asymptotics.md:4-9, plus the uniformity that file never states. The Gaussian witness in (6) needs none of it - it is exact in closed form.

### 8

(H8) The comparison is made at the level of the CONTRACTED FUNCTIONAL $\mathcal F^X_h(R_h;o)$, which is a functional of laws and hence type-compatible with PIFB2's $\mathcal F[\{q_i\},\ldots]$. It is NOT made between $S_h$ (a function on state space) and PIFB2's $\mathcal F$ (a functional on law space); those are different types.


## derivation

## 0. What was tautological, and what fixes it

`construction-or-strongest-theorem.md:14-20` writes $S_h^{\rm exact}=S_h^{\rm PIFB}+\varepsilon_h+c_h$ with $C_h$ specified only as "a measurable coarse map that is fixed independently of the recognition law" (`exact-contraction-proof.md:6-8`), $c_h$ never defined anywhere, and $\varepsilon_h$ characterized only as the difference. Four data must be declared before the identity has content: (i) the microscopic law, (ii) $C_h$, (iii) the reference measure (which must be a **product** for the Hoeffding–Möbius coordinates of `07b_agent_network_rg.tex:1193-1214` to exist), and (iv) the retained scope. I supply all four and compute.

---

## 1. The microscopic law and its posterior — block factorization

From `typed-construction.md:71-85`, conditional on $H_n$,
$$P_a^n(do,dk,dm,dj,dx,d\ell,dy)=p_a(dk)\,r_a(dm)\,L_a(do\mid k,m)\;\times\;\pi^q_{aj}u^n_{aj}(dx)\;\times\;\pi^s_{a\ell}v^n_{a\ell}(dy),\qquad P_h^n=\bigotimes_a P_a^n.$$

**Lemma 0 (posterior block factorization).** The likelihood density $\ell_a(o\mid k,m)$ depends on $z_a$ only through $(k,m)$. Hence conditioning on $o=o_a$ multiplies only the first block:
$$\Pi_{a,o_a}(dk,dm,dj,dx,d\ell,dy)=\underbrace{\frac{\ell_a(o_a\mid k,m)p_a(dk)r_a(dm)}{p_a(o_a)}}_{=:\;\pi^{\rm post}_a(dk,dm)}\;\otimes\;\pi^q_{aj}u^n_{aj}(dx)\;\otimes\;\pi^s_{a\ell}v^n_{a\ell}(dy),$$
with $p_a(o_a)=\int\ell_a(o_a\mid k,m)p_a(dk)r_a(dm)\in(0,\infty)$ by (H3), and $\Pi_{h,o}=\bigotimes_a\Pi_{a,o_a}$. ∎

**The replica blocks are untouched by the data.** Their posterior equals their prior. This single fact drives everything below.

The recognition family (`typed-construction.md:100-105`) is
$$Q_a^{n+1}(dk,dm,dj,dx,d\ell,dy)=\zeta_a(dk,dm)\,\beta_{aj}q_a(dx)\,\gamma_{a\ell}s_a(dy),\qquad q_a=({\rm pr}_K)_\#\zeta_a,\ s_a=({\rm pr}_M)_\#\zeta_a .$$
It is a product over the same three blocks. **The tie is the constraint that the $x$-marginal equals the $k$-marginal of $\zeta_a$ and the $y$-marginal equals its $m$-marginal.**

---

## 2. Statement (1): blockwise-product rigidity  [DERIVATION]

**Proposition.** Let $\Pi=\bigotimes_{a}\Pi_a$ on $\prod_a Z_a$ (standard Borel), $C(z)=(c_a(z_a))_a$ with each $c_a$ measurable, $\nu=\bigotimes_a\nu_a$, and $C_\#\Pi\ll\nu$. Then
$$C_\#\Pi=\bigotimes_a (c_a)_\#\Pi_a,\qquad S:=-\log\frac{dC_\#\Pi}{d\nu}=\sum_a S_a(x_a)\ \ \nu\text{-a.e.},\qquad S_a=-\log\frac{d(c_a)_\#\Pi_a}{d\nu_a}.$$

*Proof.* On measurable rectangles $\prod_a B_a$, $C_\#\Pi(\prod_a B_a)=\Pi(\prod_a c_a^{-1}B_a)=\prod_a\Pi_a(c_a^{-1}B_a)=\prod_a(c_a)_\#\Pi_a(B_a)$. Rectangles form a $\pi$-system generating the product $\sigma$-algebra, so the two measures agree (Dynkin). Each $(c_a)_\#\Pi_a\ll\nu_a$ (a null set in one factor pulls back to a null rectangle), and by Fubini the product of the factor densities is a version of the product density. Take $-\log$. ∎

**Corollary (Möbius components vanish above order 1).** Let $\Phi_B(x_B)=\sum_{B'\subseteq B}(-1)^{|B|-|B'|}S(x_{B'},x^\circ_{B^c})$ be the Hoeffding–Möbius component (`07b:1193-1200`). For $S=\sum_a S_a(x_a)$ and $|B|\ge2$: terms with $a\notin B$ contribute $S_a(x^\circ_a)$ for every $B'$ and cancel because $\sum_{B'\subseteq B}(-1)^{|B|-|B'|}=0$; for $a\in B$ the coefficient of $S_a(x_a)$ is $\sum_{B'\ni a}(-1)^{|B|-|B'|}=-\sum_{B''\subseteq B\setminus a}(-1)^{(|B|-1)-|B''|}=0$ whenever $|B|-1\ge1$, and symmetrically for $S_a(x^\circ_a)$. Hence $\Phi_B\equiv0$ for $|B|\ge2$. ∎

*(Verified numerically: max $|\Phi_{\{0,1\}}|$ over all configurations of a 2-agent, $K{=}3$, $M{=}2$, $J{=}2$ model $=3.6\times10^{-15}$.)*

**Reading.** $P_h^n$ is a product across $a$ **by construction** — `typed-construction.md:87-88` says so explicitly ("an existential witness, not a claim that all useful multi-agent generative laws factor across $a$"). Therefore substituting it *makes $\varepsilon_h$ determinate but simultaneously empties the cross-agent sector*. The generated all-to-all and four-body operators of CE-1/CE-2 (`adversarial-counterexamples.md:4-9`) cannot arise here. This settles the effective-action run's obligation "compute or bound its exact generated interaction coordinates" (`final-report.md:55`) for this law: **they are all zero above order 1.** It also shows the tied-replica law is the *wrong probe* for that obligation — its answer is trivial for structural reasons.

---

## 3. The three coarse maps and their exact contracted actions

### 3a. $C_h^{(1)}$: retain the private pair only

$$C^{(1)}_h(z)=(k_a,m_a)_{a\in A}\;:\;Z_h\longrightarrow X^{(1)}_h=\prod_a(\mathsf K_a\times\mathsf M_a).$$
Coordinate projection: measurable, deterministic, independent of $Q$ — satisfies `exact-contraction-proof.md:6-8` verbatim. By Lemma 0, $(C^{(1)}_h)_\#\Pi_{h,o}=\bigotimes_a\pi^{\rm post}_a$ **exactly** (no mixture is generated: the discarded blocks are independent of the retained ones under $\Pi$). With $\nu_a=p_a\otimes r_a$,
$$S^{(1)}_h(k,m)=\sum_a\big[-\log\ell_a(o_a\mid k_a,m_a)\big],\qquad \log Z^{(1)}_h=\sum_a\log p_a(o_a)=\log p_h(o).$$
Feeding into `exact-contraction-proof.md:29-32`, $\mathcal F^X_h(R;o)=\mathbb E_R S-H_{\nu}(R)+\log Z-\log p_h(o)$, and using $R^{(1)}_h=\bigotimes_a\zeta_a$, $-H_{\nu_a}(\zeta_a)=D_{\rm KL}(\zeta_a\|p_a\otimes r_a)=D_{\rm KL}(q_a\|p_a)+D_{\rm KL}(s_a\|r_a)+I_{\zeta_a}(K_a;M_a)$ (the chain rule of `exact-elbo-proof.md:34-48`), the $\log Z$ and $-\log p_h(o)$ cancel and
$$\boxed{\ \mathcal F^{X,(1)}_h(R_h;o)=\sum_a\Big[D_{\rm KL}(q_a\|p_a)+D_{\rm KL}(s_a\|r_a)+I_{\zeta_a}(K_a;M_a)-\mathbb E_{\zeta_a}\log\ell_a(o_a\mid K_a,M_a)\Big]\ }$$
— **exactly the private sector of the closed theorem, with the observation expectation taken over the joint $\zeta_a$.** (This incidentally resolves the observation-typing mismatch flagged between `PIFB2.tex:689` and `:669`: the contraction produces the joint-expectation form, not the $q_i$-only form.)

The **discarded** conditional KL: since both $Q_a$ and $\Pi_{a,o_a}$ are products over the three blocks, both conditionals are constant in $(k,m)$, and
$$\int D_{\rm KL}\big(Q(\cdot\mid x)\|\Pi_{h,o}(\cdot\mid x)\big)R_h(dx)=\sum_a\Big[D_{\rm KL}(\beta_a\|\pi^q_a)+\sum_b\beta_{ab}D_{\rm KL}(q_a\|u^n_{ab})+D_{\rm KL}(\gamma_a\|\pi^s_a)+\sum_b\gamma_{ab}D_{\rm KL}(s_a\|v^n_{ab})\Big],$$
using the label-copy chain rule of `exact-elbo-proof.md:64-83`. **This is the entire PIFB2 relational sector.**

> **First structural verdict.** At level 1, $S_h$ is pure one-body observation. $\varepsilon_h=0$ and $c_h=0$ against that basis, but **PIFB2's peer and attention operators are provably absent from $S_h$**: they are the posterior-conditional-lift gap that the contraction discards. They are recognition-side, not generative-side, objects. Crucially they are *not lost*: because of the tie, $q_a,s_a$ are the marginals of the retained $\zeta_a$, so the discarded term is a functional of $(R_h,\beta,\gamma)$ — the contraction loses no information about the objective, it merely relocates the relational sector out of the density action. Note also that `exact-contraction-proof.md:21-24`'s infimum is over *all* fine laws; the posterior-conditional lift $Q^\star$ is **not** in the tied family unless $\beta_a=\pi^q_a$ and $q_a=u^n_{ab}$ for all $b$, so for the operative family the identity is an inequality plus this gap.

*(Verified: 2-agent discrete model, $\mathcal F^{X,(1)}-\log p_h(o)$ vs private sector agree to $10^{-15}$; discarded KL vs relational sector agree to $10^{-15}$.)*

### 3b. $C_h^{(2)}$: retain private pair **and copies**, integrate out the **labels** — where the mixture appears

$$C^{(2)}_h(z)=(k_a,m_a,x_a,y_a)_{a\in A}.$$
Now the marginalization is nontrivial: $\sum_j\pi^q_{aj}u^n_{aj}(dx)=\bar u_a(dx)$, an **arithmetic mixture**. By Lemma 0,
$$(C^{(2)}_h)_\#\Pi_{h,o}=\bigotimes_a \pi^{\rm post}_a\otimes\bar u_a\otimes\bar v_a,\qquad \bar u_a=\sum_{j}\pi^q_{aj}u^n_{aj},\quad\bar v_a=\sum_\ell\pi^s_{a\ell}v^n_{a\ell}.$$
On the recognition side, $\sum_j\beta_{aj}q_a(dx)=q_a(dx)$, so $R^{(2)}_h=\bigotimes_a\zeta_a\otimes q_a\otimes s_a$. Therefore
$$\boxed{\ \mathcal F^{X,(2)}_h(R_h;o)=\mathcal F^{X,(1)}_h(R_h;o)+\sum_a\big[D_{\rm KL}(q_a\|\bar u_a)+D_{\rm KL}(s_a\|\bar v_a)\big].\ }$$
The discarded conditional KL is now the **label given the copy**. Under $Q$, $Q(j\mid x)=\beta_{aj}$ (product structure, independent of $x$). Under $\Pi$, $\Pi(j\mid x)=\pi^{q,\rm post}_{aj}(x):=\pi^q_{aj}u_{aj}(x)/\bar u_a(x)$ — a **softmax over sources**. Hence the discarded term is $\sum_a\mathbb E_{q_a}D_{\rm KL}(\beta_a\|\pi^{q,\rm post}_a(\cdot\mid X))+(\text{model channel})$.

**Consistency identity (algebra shown).**
$$D_{\rm KL}(q_a\|\bar u_a)+\mathbb E_{q_a}D_{\rm KL}\big(\beta_a\|\pi^{q,\rm post}_a(\cdot\mid X)\big)=D_{\rm KL}(\beta_a\|\pi^q_a)+\sum_j\beta_{aj}D_{\rm KL}(q_a\|u_{aj}).$$
*Proof.* Expand the left side:
$\int q_a\log\frac{q_a}{\bar u_a}+\int q_a\sum_j\beta_{aj}\log\frac{\beta_{aj}\bar u_a}{\pi_{aj}u_{aj}}
=\int q_a\log q_a-\int q_a\log\bar u_a+\sum_j\beta_{aj}\log\tfrac{\beta_{aj}}{\pi_{aj}}+\int q_a\log\bar u_a-\sum_j\beta_{aj}\int q_a\log u_{aj}$.
The two $\int q_a\log\bar u_a$ cancel. Using $\sum_j\beta_{aj}=1$ to distribute $\int q_a\log q_a$, the remainder is $\sum_j\beta_{aj}\log\frac{\beta_{aj}}{\pi_{aj}}+\sum_j\beta_{aj}\int q_a\log\frac{q_a}{u_{aj}}$. ∎
*(Verified to $10^{-15}$ on random $(J{=}4,K{=}5)$ data, and end-to-end on the 2-agent model.)*

Setting $\beta_a=\pi^q_a$ gives the **exact Jensen-gap identity**
$$\sum_j\pi^q_{aj}D_{\rm KL}(q_a\|u_{aj})-D_{\rm KL}(q_a\|\bar u_a)=\mathbb E_{q_a}D_{\rm KL}\big(\pi^q_a\,\big\|\,\pi^{q,\rm post}_a(\cdot\mid X)\big)\ \ge 0 .$$

### 3c. $C_h^{(3)}={\rm id}$ (or any label-retaining map): exact closure

With $\nu_a=(p_a\otimes r_a)\otimes({\rm unif}_{J^q_a}\otimes\lambda_a)\otimes({\rm unif}_{J^s_a}\otimes\mu_a)$, Lemma 0 gives $S_a$ as displayed in the theorem. Then $\mathbb E_{R}S_h$ supplies the observation term, the $-\log\pi^q_{aj}$ cross-entropy and the peer energies $E_{aj}(x)=-\log u_{aj}(x)$; $-H_{\nu}(R)$ supplies $D_{\rm KL}(\zeta_a\|p_a\otimes r_a)$, the row entropies $\sum_j\beta_{aj}\log\beta_{aj}$ and the copy entropies $-H(q_a),-H(s_a)$. Assembling, $-\log\pi_{aj}$ + row entropy $=D_{\rm KL}(\beta_a\|\pi^q_a)$ and $\sum_j\beta_{aj}\mathbb E_{q_a}E_{aj}-H(q_a)=\sum_j\beta_{aj}D_{\rm KL}(q_a\|u_{aj})$, reproducing `exact-elbo-proof.md:102-118` term for term:
$$\mathcal F^{X,(3)}_h=\mathcal F^{\rm lag,1}_{\rm PIFB2,h}+\sum_a I_{\zeta_a}(K_a;M_a),\qquad \varepsilon_h=0,\ c_h=0 .$$
*(Verified: closed theorem vs direct $D_{\rm KL}(Q\|\Pi)-\log p_h(o)$ agree to $2\times10^{-15}$.)*

---

## 4. $\varepsilon_h$ in closed form, and $c_h$ — the answer to step 3

Fix level 2 and the PIFB2 peer basis $\{E_{aj}=-\log u_{aj}\}_{j}$ with prior coefficients, so $S^{\rm PIFB}_{a,\rm rel}(x)=\sum_j\pi^q_{aj}E_{aj}(x)$. The exact action is $S^{(2)}_{a,\rm rel}(x)=-\log\bar u_a(x)=-\log\sum_j\pi^q_{aj}e^{-E_{aj}(x)}$. Hence
$$\varepsilon_a(x)=S^{(2)}_{a,\rm rel}-S^{\rm PIFB}_{a,\rm rel}=-\log\!\Big(\sum_j\pi_{aj}u_{aj}(x)\Big)+\sum_j\pi_{aj}\log u_{aj}(x)=\log\frac{\text{GM}_{\pi}\,u_{a\cdot}(x)}{\text{AM}_{\pi}\,u_{a\cdot}(x)}\ \le\ 0$$
by AM–GM (equivalently Jensen for $-\log$), with equality at $x$ iff all $u_{aj}(x)$ with $\pi_{aj}>0$ coincide.

**Binary answer.** For this microscopic law:
* **Across agents: $\varepsilon_h=0$ exactly, at every order** (Section 2). No 3-body term, no nonlocal term, no determinant.
* **Within the source row: $\varepsilon_h\neq0$ in general**, and equals exactly the AM–GM / log-partition gap above, **iff the labels are marginalized**. Retain the labels and $\varepsilon_h=0$ exactly.

**$c_h$ — first definition anywhere in the corpus.** Two conventions:
1. *Unnormalized projection* ($S^{\rm PIFB}$ need not be a log-density): $c_h=0$.
2. *Normalized projection*: require $S^{\rm PIFB}$ to be a genuine negative log-density. Its exponential is the **product-of-experts** $\prod_j u_{aj}^{\pi_{aj}}$, with normalizer $Z^q_a=\int\prod_j u_{aj}^{\pi_{aj}}\,d\lambda_a$. By generalized Hölder with exponents $1/\pi_{aj}$, $Z^q_a\le\prod_j(\int u_{aj}d\lambda_a)^{\pi_{aj}}=1$, and $Z^q_a>0$ iff the sources overlap. Then
$$\boxed{\ c_h=-\sum_a\big[\log Z^q_a+\log Z^s_a\big]\ \ge 0\ }$$
— the **weighted Bhattacharyya–Chernoff overlap deficit of the transported sources**. Gaussian instance: two equal-covariance sources at weight $\tfrac12$ give $-\log Z^q_a=\tfrac18\|\mu_1-\mu_2\|^2_{\Sigma^{-1}}$, the Bhattacharyya distance.
*(Verified $Z\le1$ in 20 000 random discrete trials, 0 violations.)*

**Exact expectation.** Combining with §3b at $\beta=\pi$,
$$\mathbb E_{R_h}[\varepsilon_h]=-\sum_a\Big[\mathbb E_{q_a}D_{\rm KL}\big(\pi^q_a\|\pi^{q,\rm post}_a(\cdot|X)\big)+\mathbb E_{s_a}D_{\rm KL}\big(\pi^s_a\|\pi^{s,\rm post}_a(\cdot|Y)\big)\Big].$$
*(Verified to $10^{-15}$ on the 2-agent model and on random rows.)* This replaces the run's unproved and dimensionally-suspect "uniformly bounded by $\|\varepsilon_h\|_\infty$" (`construction-or-strongest-theorem.md:22-24`) with an **exact equality**; no norm bound is needed.

**Rigorous norm bound (when one is wanted).** $-\varepsilon_a(x)=\log\mathbb E_{\pi_a}e^{-(E_{aJ}(x)-\mathbb E_{\pi_a}E_{aJ}(x))}$. Hoeffding's lemma (centered $W\in[c,d]$ $\Rightarrow$ $\log\mathbb Ee^{tW}\le t^2(d-c)^2/8$) at $t=1$ gives
$$0\ \le\ -\varepsilon_a(x)\ \le\ \tfrac18\Big(\max_{j\in{\rm supp}\pi_a}E_{aj}(x)-\min_{j}E_{aj}(x)\Big)^2=\tfrac18\Big(\max_{j,j'}\log\tfrac{u_{aj'}(x)}{u_{aj}(x)}\Big)^2 .$$
So $\|\varepsilon_h\|_\infty\le\tfrac18\sum_a\|{\rm range}_j E_{aj}\|_\infty^2$, finite iff the transported sources have uniformly comparable densities. *(Verified: 0 violations in 20 000 random trials.)* **This is what makes "$\|\varepsilon_h\|\to0$" a well-posed question at last — the norm, the ambient space ($L^\infty$ of the retained replica coordinate), and the controlling quantity (peer log-likelihood-ratio spread) are all now explicit.**

---

## 5. Step 4: what marginalizing the replicas costs — the cumulant series

$-\log\bar u_a(x)=-\log\mathbb E_{J\sim\pi^q_a}\big[e^{-E_{aJ}(x)}\big]=-\Lambda_x(-1)$ where $\Lambda_x(t)=\log\mathbb E_\pi e^{tE_{aJ}(x)}=\sum_{n\ge1}\kappa_n(x)t^n/n!$. Hence
$$-\log\bar u_a(x)=\kappa_1(x)-\tfrac12\kappa_2(x)+\tfrac16\kappa_3(x)-\cdots,\qquad \varepsilon_a(x)=-\tfrac12\kappa_2(x)+\tfrac16\kappa_3(x)-\cdots .$$

**First cumulant** $\kappa_1(x)=\sum_j\pi^q_{aj}E_{aj}(x)$ — **exactly the PIFB2 peer sector at $\beta=\pi$** (its $q_a$-expectation is $\sum_j\pi_{aj}D_{aj}+H(q_a)$, the entropy being absorbed by $-H_\nu(R)$).

**Second cumulant**, in manifestly pairwise-in-source form:
$$\kappa_2(x)=\sum_j\pi_{aj}E_{aj}^2-\Big(\sum_j\pi_{aj}E_{aj}\Big)^2=\tfrac12\sum_{j,j'}\pi_{aj}\pi_{aj'}\big(E_{aj}(x)-E_{aj'}(x)\big)^2 .$$
*(Verified identically equal numerically.)* So the **leading generated operator** is
$$-\tfrac12\kappa_2(x)=-\tfrac14\sum_{j,j'}\pi^q_{aj}\pi^q_{aj'}\Big(\log\tfrac{u_{aj'}(x)}{u_{aj}(x)}\Big)^2,$$
a **two-source (pairwise-in-label) log-likelihood-ratio quadratic**, entering with a **negative** sign — the mixture is heavier-tailed than the geometric mean, so peer disagreement *lowers* the exact action. PIFB2's action is linear in $\beta$ plus $\tau\beta\log\beta$ (`PIFB2.tex:681-693`), so this operator is **outside its span at every $\tau$ and every $\beta$**.

**Taking $q_a$-expectations splits it exactly** (using $\mathbb E_{q_a}\log\frac{u_{aj'}}{u_{aj}}=D_{aj}-D_{aj'}$ and $\sum_{jj'}\pi_j\pi_{j'}(D_j-D_{j'})^2=2{\rm Var}_{\pi}(D)$):
$$\mathbb E_{q_a}\big[-\tfrac12\kappa_2\big]=\underbrace{-\tfrac12{\rm Var}_{\pi^q_a}(D_{a\cdot})}_{\text{= PIFB2's own }-\log Z_a\text{ expansion at }\tau=1}\;\underbrace{-\tfrac14\sum_{j,j'}\pi_{aj}\pi_{aj'}{\rm Var}_{q_a}\!\log\tfrac{u_{aj'}}{u_{aj}}}_{\text{genuinely non-PIFB2}} .$$
*(Verified to $10^{-10}$ on random data.)* The first piece is what PIFB2 *already has* (its envelope reduction `PIFB2.tex:717-733` gives $-\log Z_a=\sum_j\pi_jD_j-\tfrac12{\rm Var}_\pi(D)+\cdots$ at $\tau=1$). **The second piece is the true residual**, and it vanishes iff the log-ratios $\log(u_{aj'}/u_{aj})$ are $q_a$-a.s. constant — i.e. iff the transported sources are $q_a$-a.s. mutually proportional, the same condition as the exact criterion in §4.

**Ordering theorem.** $\Psi(E):=-\log\sum_j\pi_je^{-E_j}$ is concave on $\mathbb R^{J}$ (it is $-{\rm lse}$ composed with a linear map) and satisfies $\Psi(E+c\mathbf 1)=\Psi(E)+c$. Jensen along $q_a$ with $\mathbb E_{q_a}E_{aj}=D_{aj}+H(q_a)$ gives
$$D_{\rm KL}(q_a\|\bar u_a)\;=\;\mathbb E_{q_a}\Psi(E(X))-H(q_a)\;\le\;\Psi(\mathbb E_{q_a}E(X))-H(q_a)\;=\;-\log\!\sum_j\pi_{aj}e^{-D_{aj}}\;\le\;\sum_j\pi_{aj}D_{aj},$$
the last step by Jensen again, with right-minus-middle $=D_{\rm KL}(\pi^q_a\|\beta^*_a)$ exactly, $\beta^*_{aj}=\pi_{aj}e^{-D_{aj}}/Z_a$. *(All three verified numerically.)*

> **This locates a precise gap in the nearest prior art.** `07b_agent_network_rg.tex:1818-1827` gives an exact log-sum-exp rule $E^c_J=-\tau\log[\frac{1}{\pi^c_J}\sum_{j\in J}\pi_je^{-E_j/\tau}]$ for coarsening the source label *within the row functional*, with status ESTABLISHED. At $\tau=1$ and full merge it produces exactly the **middle** term above. But eliminating the label from the underlying **joint law** produces the **left** term. The two differ by the Jensen gap of $\Psi$ along $q_a$ — a quantity 07b does not compute. `07b:1810-1814` anticipates the *structure* ("replacing it by one categorical row is a further coarse channel whose conditional KL appears in the chain rule") without evaluating the residual.

---

## 6. Step 5, the honest verdict: the lattice limit kills the peer sector

This is where the computation turns decisively negative for the effective-action program.

Under (H7) write $f_j:=\log(u_{aj}/q_a)=hg_j+h^2t_j+O(h^3)$ with $\mathbb E_{q_a}g_j=0$. Normalization $\mathbb E_{q_a}e^{f_j}=1$ forces $\mathbb E_{q_a}t_j=-\tfrac12{\rm Var}_{q_a}(g_j)$, so
$$D_{aj}=-\mathbb E_{q_a}f_j=\tfrac{h^2}{2}{\rm Var}_{q_a}(g_j)+O(h^3)\quad\text{(the Fisher expansion of \texttt{lattice-continuum-asymptotics.md:11-18})}.$$
With $\bar g:=\sum_j\pi_{aj}g_j$, $\bar u_a=q_a(1+h\bar g+O(h^2))$ and $\mathbb E_{q_a}\bar g=0$, so
$$\textstyle\sum_j\pi_{aj}D_{aj}=\tfrac{h^2}{2}\sum_j\pi_{aj}{\rm Var}_{q_a}(g_j)+O(h^3),\qquad D_{\rm KL}(q_a\|\bar u_a)=\tfrac{h^2}{2}{\rm Var}_{q_a}(\bar g)+O(h^3),$$
$$\mathbb E_{q_a}\varepsilon_a=-\tfrac{h^2}{2}\,\mathbb E_{q_a}{\rm Var}_{\pi_a}(g_J)+O(h^3),\qquad c_a=-\log Z^q_a=\tfrac{h^2}{2}\Big[\textstyle\sum_j\pi_{aj}{\rm Var}_{q_a}g_j-{\rm Var}_{q_a}\bar g\Big]+O(h^3).$$

**The exact contraction produces $\;I(\overline{\nabla\theta},\overline{\nabla\theta})\;$ where PIFB2 needs $\;\overline{I(\nabla\theta,\nabla\theta)}$** — the Fisher quadratic of the *prior-averaged* covariant derivative, not the prior-average of the per-edge Fisher quadratics. They differ by $\mathbb E_{q_a}{\rm Var}_{\pi_a}(g_J)$, and on a **balanced stencil** — symmetric neighbour set with symmetric row, the generic lattice case — $\bar g\equiv0$ and:

$$\boxed{\ \mathbb E_{q_a}\varepsilon_a=-\sum_j\pi_{aj}D_{\rm KL}(q_a\|u_{aj})+O(h^3):\ \text{the residual cancels the retained peer sector exactly at leading order.}\ }$$

**Exact closed-form witness (no hypothesis needed).** $q=N(0,1)$, $u_\pm=N(\pm h,1)$, $\pi=(\tfrac12,\tfrac12)$. Then $\sum_j\pi_jD_{aj}=h^2/2$ exactly, and since $\log\frac{q}{\bar u}=\frac{h^2}{2}-\log\cosh(hx)$ (verified pointwise to $10^{-13}$),
$$D_{\rm KL}(q\|\bar u)=\tfrac{h^2}{2}-\mathbb E\log\cosh(hX)=\tfrac{h^2}{2}-\Big(\tfrac{h^2}{2}-\tfrac{h^4}{4}+O(h^6)\Big)=\tfrac{h^4}{4}+O(h^6).$$
Quadrature confirms the ratio $D_{\rm KL}(q\|\bar u)/(h^4/4)\to1$: $0.837,\,0.951,\,0.987,\,0.997,\,0.999$ at $h=0.4,0.2,0.1,0.05,0.025$. In 2-D with four neighbours, $D_{\rm KL}(q\|\bar u)/(h^4/8)\to1$: $0.945,\,0.985,\,0.996$. Also $-\log Z^q_a=\tfrac18(2h)^2=h^2/2$ exactly $=$ the whole peer sector, as the general formula predicts. Asymmetric rows $\pi=(w,1-w)$ confirm the general law: $D_{\rm KL}(q\|\bar u)/[\tfrac{h^2}{2}(2w-1)^2]\to1$.

**Consequence.** Under the $h^{d-2}$ edge weight of `lattice-continuum-asymptotics.md:20-22` ($h^{-d}$ edges), PIFB2's Fisher–Dirichlet peer term survives at $h^{-d}\!\cdot\!h^{d-2}\!\cdot\!h^2=O(1)$, while the exact contracted relational action scales as $h^{-d}\!\cdot\!h^{d-2}\!\cdot\!h^4=O(h^2)\to0$. **The Fisher-covariant Dirichlet peer sector is not generated by contracting the tied-replica law onto the replica coordinates.** Under the normalized convention it is, to leading order, precisely the additive constant $c_h=-\sum_a\log Z^q_a$ — the Chernoff overlap deficit of neighbouring transported beliefs — and not a term of the density action at all. (This sharpens CE-2 of `boundary-counterexamples.md:16-37`, which found $-H(q)-\log Z_\beta$ left over from a product-of-experts latent, into a quantitative statement about which of the two normalizations carries the peer energy.)

**What would have to be true for $\|\varepsilon_h\|\to0$.** The absolute criterion is satisfiable but vacuous: $\|\varepsilon_h\|_\infty\le\tfrac18\sum_a\|{\rm range}_jE_{aj}\|_\infty^2\to0$ under (H7), yet the *retained* sector vanishes at the same $O(h^2)$ rate. The well-posed question is the **relative** residual $|\mathbb E\varepsilon_h|/|\mathbb E S^{\rm PIFB}_{h,\rm rel}|$, which tends to $\mathbb E_{q}{\rm Var}_\pi(g_J)/\mathbb E_\pi{\rm Var}_q(g_J)$ — equal to **1** on a balanced stencil (total cancellation), and $<1$ only to the extent the row is biased. It tends to $0$ **iff** ${\rm Var}_{\pi_a}(g_J)\to0$, i.e. iff all transported sources of an agent become $q_a$-a.s. proportional faster than each approaches $q_a$ — a strong local-consensus condition that a refining lattice does *not* supply, since neighbours in different directions have genuinely different $g_j$. Obligation (3) of `final-report.md:56` ("prove the retained PIFB residual vanishes in a declared norm uniformly on bounded-energy sublevels") must therefore be restated in a **relative** norm; in the absolute sup norm it is true and useless.

---

## 7. Which level, and what is *not* discharged

Per the target's step 1: **I am doing the state-level contraction throughout.** $C_h$ acts on the microscopic state space $Z_h$ and retains state-valued coordinates $(k_a,m_a,x_a,y_a,j_a,\ell_a)$. The comparison to PIFB2 is made at the level of the **contracted functional** $\mathcal F^X_h(R_h;o)$, which is a functional of laws and hence type-compatible with PIFB2's $\mathcal F[\{q_i\},\ldots]$ (H8). The comparison is *not* between $S_h$ and PIFB2's $\mathcal F$ — those are different types.

**The configuration-level alternative is unavailable for this microscopic law.** $P_h^n$ contains **no law-valued random variables**: $q_a$ and $s_a$ are variational parameters of $Q$, not coordinates of $P$ (`typed-construction.md:90-105`). There is therefore no measurable $C_h:Z_h\to$ (a space of laws), and no hyper-law on $\mathcal P(\mathsf K_a)$ is supplied. **The claim-ledger's `a-section-typing` MODELING_POSTULATE (`claim-ledger.json:16-20`) and release obligation #1 ("specify one normalized microscopic family whose slow variables are genuine sampled belief/model sections rather than recognition parameters", `release.json:11`, `final-report.md:52`) are NOT discharged by this substitution.** What is discharged is obligation "compute or bound its exact generated interaction coordinates" (`final-report.md:55`) — for this law they are all zero above order 1 — and, for the first time, the determinacy of $\varepsilon_h$ and $c_h$ themselves.

**Product reference is genuine, so the Hoeffding machinery applies.** The gotcha that $\varepsilon_h$ is undefined without a product reference (`07b:1193-1214`, with the failure witness at `07b:1160-1180`) is discharged here: $\Pi_{h,o}$ is *itself* a product (Lemma 0), so a product-probability $\nu_h$ equivalent to $(C_h)_\#\Pi_{h,o}$ exists under (H3),(H5). The exponential $3^{|V|}-1$ extraction cost of `07b:1228-1239` never bites, because all components live on singletons.

**Exact-image-invariance.** The non-tautological criterion of `07b:1487-1496` ($T_\ell(\operatorname{Ran}R_\ell)\subseteq\operatorname{Ran}R_{\ell+1}$) is satisfied trivially at level 3 (the retained scope is the whole space) and satisfied at level 1 in the trivial sense that the retained image is one-body and stays one-body. At level 2 it **fails**, and the obstruction is now explicit: the retained span $\{\sum_j\pi_{aj}E_{aj}\}$ is not invariant under label elimination, whose image is $-\log\sum_j\pi_{aj}e^{-E_{aj}}$.

## obstructions

### 1

THE PEER SECTOR IS NOT IN $S_h$. For every blockwise coarse map, PIFB2's peer and attention operators are absent from the exact effective density action. At level 1 they are the discarded posterior-conditional-lift gap; at level 2 the retained surrogate $D_{KL}(q_a\|\bar u_a)$ is a strictly different (smaller) object; only by retaining the source labels do they appear, and then the contraction is the identity and nothing has been coarse-grained. The effective-action program cannot obtain PIFB2's relational sector from this microscopic law by contraction.

### 2

LEADING-ORDER CANCELLATION IN THE LATTICE LIMIT. On a balanced stencil the label-marginalization residual is exactly minus the retained peer sector at $O(h^2)$, leaving $O(h^4)$. Verified in closed form ($q=N(0,1)$, $u_\pm=N(\pm h,1)$: peer $=h^2/2$ exactly, contracted $=h^4/4+O(h^6)$) and by quadrature in 1-D and 2-D. The Fisher-covariant Dirichlet term of lattice-continuum-asymptotics.md:20-22 is therefore NOT ELBO-derived from this law; under the normalized convention it is the additive constant $c_h$.

### 3

CROSS-AGENT SECTOR IS STRUCTURALLY EMPTY, SO THIS LAW CANNOT PROBE THE INTERESTING QUESTION. $P_h^n=\bigotimes_a P_a^n$ by construction (typed-construction.md:84-88 flags this as an existential witness). Blockwise-product rigidity then forces $\Phi_B\equiv0$ for $|B|\ge2$. Substituting the tied-replica law makes $\varepsilon_h$ determinate at the cost of trivializing the generated-multi-body-operator question that CE-1/CE-2 (adversarial-counterexamples.md:4-9) were designed to pose. A microscopic law with genuine cross-agent coupling is still needed.

### 4

SECTION TYPING UNDISCHARGED. $P_h^n$ has no law-valued coordinates, so the configuration-level ELBO is unavailable and claim-ledger.json:16-20 (a-section-typing, MODELING_POSTULATE) plus release.json:11 obligation #1 remain open. The results here are state-level only.

### 5

THE CONTRACTION INFIMUM IS NOT ATTAINED IN THE TIED FAMILY. exact-contraction-proof.md:21-24 takes the infimum over ALL fine laws with the given pushforward; the posterior-conditional lift is in the tied family only if $\beta_a=\pi^q_a$ and $q_a=u^n_{ab}$ for every $b$. For the operative family the identity is an inequality plus the explicit gap computed in §3a.

### 6

$\varepsilon_a=-\infty$ ON DISJOINT SUPPORTS. If two transported sources with positive prior weight have disjoint supports, the geometric mean vanishes and the PIFB2 projection is not finite. (H5) mutual equivalence is load-bearing, and the hard-support masking convention of boundary-counterexamples.md:76-79 must be applied by restricting the source set before the projection is formed.

### 7

ALL RESULTS ARE AT $\tau=1$, UNIT PRIVATE COEFFICIENTS, AND LAGGED SOURCES. The exact mismatch $(\tau-1)D_{KL}(\beta\|\pi)$ (boundary-counterexamples.md:39-50), the deployed $\tau=\kappa\sqrt{K_q}$ with learnable $\kappa$ (PIFB2.tex:673), the deployed adaptive $\alpha_i^*=c_0/(b_0+D_{KL})$ (PIFB2.tex:776-784), and the same-time obstruction (boundary-counterexamples.md:68-73) are all untouched. Nothing here bears on them.

### 8

(H7) IS ASSERTED, NOT DERIVED, AND THE UNIFORMITY IT NEEDS IS NOT IN THE SOURCE. lattice-continuum-asymptotics.md:4-9 stipulates link consistency; the $O(h^3)$ remainders are never claimed uniform over edges, which the summation requires. Only the Gaussian witness in §6 is hypothesis-free.

### 9

NO GAMMA-CONVERGENCE, NO PROCESS-LAW ELBO. Everything here is a finite-$A$, fixed-observation, counting-measure computation. The cell-volume prohibition of boundary-counterexamples.md:61-66 and CE-5 of both runs stand; no continuum process law is claimed or approached.


## novelty

"NEW. Prior art and how this differs, with citations I read:\n\n(1) The residual identity itself is currently a definition: $\\varepsilon_h$ and $c_h$ occur only at construction-or-strongest-theorem.md:19,22,23; $c_h$ is never defined anywhere in the corpus. This work gives $c_h$ its first definition ($c_h=-\\sum_a\\log Z^q_aZ^s_a$, the weighted Bhattacharyya-Chernoff overlap deficit) and gives $\\varepsilon_h$ a closed form.\n\n(2) $C_h$ is left abstract at exact-contraction-proof.md:6-8 ('a measurable coarse map'); no coarse map is constructed anywhere in the effective-action run. The three explicit maps here (levels 1-3) and their exact pushforwards are new.\n\n(3) The exact two-channel run uses the finite-mixture KL chain rule in the SPLITTING direction (exact-elbo-proof.md:64-83, :76 'the finite-mixture KL chain rule'), i.e. it keeps the label. This work goes the opposite way - eliminating the label - and computes what that costs. No prior artifact does.\n\n(4) NEAREST PRIOR ART: Theory/07b_agent_network_rg.tex:1818-1827 gives the exact row-blocking rule $E^c_J=-\\tau\\log[\\pi^{c,-1}_J\\sum_{j\\in J}\\pi_je^{-E_j/\\tau}]$, status ESTABLISHED, and 07b:1810-1814 notes that replacing a retained label vector by one categorical row is 'a further coarse channel whose conditional KL appears in' the chain rule. That rule coarsens the label INSIDE the row functional, on law-level energies $E_j=D_{KL}(q_a\\|u_{aj})$. Eliminating the label from the underlying JOINT LAW gives $D_{KL}(q_a\\|\\bar u_a)$ instead, and the ordering theorem of §5 shows these differ by the Jensen gap of the concave $\\Psi(E)=-\\log\\sum_j\\pi_je^{-E_j}$ along $q_a$. 07b does not compute that gap.\n\n(5) Theory/ has NO lattice, NO base-gradient energy, NO curvature term (verified in the ground sweep; 05c_pullback_geometry.tex:1359-1366 explicitly refuses to build a scalar gauged sigma energy, status NOT-CLAIMED). The $O(h^4)$-vs-$O(h^2)$ cancellation of §6 is therefore not a restatement of anything in Theory/.\n\n(6) boundary-counterexamples.md:16-37 (CE-2) already observes that a single-latent normalized product-of-experts leaves $-H(q)-\\log Z_\\beta$. This work sharpens that qualitative remark into the quantitative statement that $-\\log Z_a$ EQUALS the entire PIFB2 peer sector to $O(h^2)$ (exactly $h^2/2$ in the Gaussian witness), i.e. that PIFB2's Fisher-Dirichlet energy is a normalizer rather than a density term.\n\n(7) The blockwise-product rigidity proposition (§2) is elementary but is not stated anywhere in Theory/ or the three runs, and it is what actually settles the effective-action run's obligation 'compute or bound its exact generated interaction coordinates' (final-report.md:55) for this law.\n\nA text grep for 'Bhattacharyya|arithmetic mean|geometric mean|AM-GM|product-of-experts|log-sum-exp' over Theory/*.tex returns only 07b:649 (unrelated) and 07b:1824 (the row rule of item 4)."

## next_obligations

### 1

Restate the effective-action run's obligation (3) (final-report.md:56) in a RELATIVE norm. §6 shows the absolute criterion $\|\varepsilon_h\|_\infty\to0$ is satisfied and vacuous, because the retained sector vanishes at the same rate. The live question is $\limsup_h |\mathbb E\varepsilon_h|/|\mathbb E S^{PIFB}_{h,rel}|$, which §6 computes to be $\mathbb E_q Var_\pi(g_J)/\mathbb E_\pi Var_q(g_J)$ and equal to 1 on a balanced stencil.

### 2

Supply a microscopic law with GENUINE cross-agent coupling, since blockwise-product rigidity makes the tied-replica law structurally incapable of generating multi-body operators. The minimal repair is a shared latent or a non-blockwise (block-spin) coarse map $C_h$ whose coarse coordinates each read several agents' fine blocks - that is the only route by which a product law can produce Hoeffding components of order $\ge2$.

### 3

Decide the label question at the level of the research program. The computation shows PIFB2's peer and attention sector survives contraction if and only if the source labels $J^q_a,J^s_a$ are RETAINED as coarse configuration variables. Either (a) declare the labels part of the retained section inventory - which changes what 'a sampled belief section' means and must be reconciled with claim-ledger.json:16-20 - or (b) accept that the peer sector is a recognition-side object with no generative-density counterpart.

### 4

Discharge release obligation #1 (release.json:11) properly: exhibit a normalized microscopic family carrying LAW-VALUED coordinates (a hyper-law on $\mathcal P(\mathsf K_a)$), so that the configuration-level ELBO exists. The tied-replica law does not, and §7 shows why.

### 5

Redo §6 for the model channel with independent frames. §6 treats belief and model symmetrically, but PIFB2.tex:459 states the reference implementation gives the model fiber its own $GL(K_m)$ bundle with 'even the structure-group identification absent'. Check whether $\widetilde\Omega$-transported model sources on a refining lattice are balanced in the same sense; if not, the model channel may retain an $O(h^2)$ term the belief channel loses.

### 6

Prove or refute uniformity of the $O(h^3)$ remainder in (H7) over edges. The $h^{-d}$-edge summation in §6 needs it and lattice-continuum-asymptotics.md never states it; supply a uniform third-derivative / uniform domination hypothesis or a counterexample.

### 7

Test whether a nonuniform prior row can be tuned so that the exact contracted relational action reproduces the Fisher-Dirichlet term. §6 gives contracted $=\frac{h^2}{2}Var_{q_a}(\bar g)$ with $\bar g=\sum_j\pi_{aj}g_j$: this is a rank-one 'drift' quadratic in the averaged derivative, not a Dirichlet form. Determine whether ANY choice of $\pi^q_a$ recovers $\sum_\mu I(D_\mu\theta,D_\mu\theta)$, or prove it cannot (the natural conjecture, since $\|\bar\nabla\|^2\le\overline{\|\nabla\|^2}$ with equality only at zero variance).

### 8

Extend the exact residual formula to $\tau\ne1$. §5's ordering theorem is stated at unit temperature; the deployed $\tau=\kappa\sqrt{K_q}$ (PIFB2.tex:673) would require the tempered normalized model that boundary-counterexamples.md:39-50 says is missing. Determine whether the AM-GM gap has a $\tau$-deformed analogue (a Renyi/Chernoff-$\alpha$ gap) and whether it interacts with the $(\tau-1)D_{KL}(\beta\|\pi)$ mismatch.


## evidence_kind

DERIVATION (closed-form, with every identity independently verified: six exact KL identities to 1e-15 on random discrete data; end-to-end 2-agent model reproducing the closed theorem, both contraction levels, and the Mobius vanishing to 3.6e-15; symbolic SymPy computation of the h^4 cancellation and the Bhattacharyya normalizer; scipy quadrature confirming the h^4 law in 1-D and 2-D and the asymmetric-row generalization; Hoeffding-lemma bound and Z<=1 checked over 20,000 random trials each with zero violations). Numerics are corroboration only - every claim above is established by displayed algebra. Source citations verified by direct read: Research/manuscripts/PIFB2.tex:681-693, :717-733, :836-846; Theory/07b_agent_network_rg.tex:1193-1214, :1487-1496, :1810-1827; docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/{typed-construction.md, exact-elbo-proof.md, pifb2-crosswalk.md, boundary-counterexamples.md}; docs/derivations/2026-08-12-elbo-to-effective-section-action/{construction-or-strongest-theorem.md, evidence/exact-contraction-proof.md}. Note: Theory/PIFB2.tex does not exist in the worktree - the manuscript was read at "C:/Users/chris and christine/Desktop/Research/manuscripts/PIFB2.tex".
