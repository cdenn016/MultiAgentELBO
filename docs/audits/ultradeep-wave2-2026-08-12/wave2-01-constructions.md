# Wave 2, item 01 — Two constructions attempted

Date: 2026-08-11. Execution policy: **CPU only. No GPU or CUDA job was started or attempted.**
All numerics: `numpy 2.2.6` / `sympy 1.14.0`, float64 and exact rational/symbolic where noted, in
the isolated Linux sandbox. Scripts and their outputs are transcribed in §4.

Baseline read: `docs/audits/2026-08-11-ultradeep-expert-audit.md` (items 1 and 2 of "Shortest
credible path"), `docs/audits/ultradeep-2026-08-11/audit-06-pifb2-gap.md`, and the primary sources
`Theory/02_geometry.tex`, `03_probability.tex`, `04_generative.tex`, `05_elbo.tex`,
`05c_pullback_geometry.tex`, `05d_relational_inference.tex`, `12_philosophy.tex`,
`appendix_claim_ledger.tex`, `SPEC.md`.

---

## 0. Headline verdict

**Task A partially succeeds and then breaks, and the break is a theorem.**

What is achievable, in full and with proof: a frame-independent, measurable, `[0,+\infty]`-valued
free energy on local sections; an exact consistency identity with the finite-design
`\Fenergy[Q_X;X,o]` carrying a nonnegative cross-context total-correlation defect (this *replaces*
`hyp:prob-sampling-compatibility` with something that is a theorem, not a hypothesis, and that
identifies in the direction that matters); a first variation, a natural-gradient flow on section
space, and exponential convergence to a minimizer that is verified to be the exact contextwise
Bayesian posterior.

What is provably **not** achievable, on the very tier the audit recommends (`05d:235`):

> **Theorem A-NOGO.** Let `\mathcal C` be positive-dimensional, `P\to\mathcal C` principal with
> group `G`, `\mathcal E_b = P\times_{\widehat\rho_b}\mathcal B` with `\mathcal B` a `G`-torsor
> (the exhibited tier is one), `D\subset\mathcal C` a finite design, and consider
> `\mathcal F_\mu[s]=\int_{\mathcal C} f(c,s(c),D^\omega s(c))\,d\mu(c)` on a section class closed
> under compactly supported deformation. Then:
> (a) well-definedness under change of trivialization is achievable in complete generality;
> (b) `\mathrm{Aut}_G(P)`-invariance forces `\mathcal F_\mu` to be **constant**, hence is
> incompatible with reproducing a nonconstant `\Fenergy`;
> (c) consistency with the finite-design `\Fenergy` forces `f` to be **independent of
> `D^\omega s`**, hence forces the connection out of the free energy entirely.
> Therefore no functional of the displayed form satisfies the audit's three requirements
> (a), (b), (c) of `S1` with a nonconstant, connection-dependent free energy.

This upgrades audit finding **S3** ("the gauge sector is inert; connections never enter the free
energy") from an observation about what the manuscript happens to contain into a **necessity
proof about what it can contain**, given its own finite-design commitment.

**Task B succeeds.** N3(a) is provable in about two pages from
`prop:gen-product-evidence-invariance` plus `hyp:gen-kernel-covariance`, exactly as the audit
estimated. It is proved below, with a numerical witness and a firing negative control. But the
converse analysis shows the theorem is *far* stronger than gauge equivalence and correspondingly
*far* weaker philosophically than the project wants: the record-law map is blind to the connection
(which is not an argument of any generative kernel), blind to all off-design section values, and
blind to the topology of `P` (because every principal bundle is trivial over a finite set). Under
the manuscript's own idle-wheel criterion (`12_philosophy.tex:77`), proving N3(a) argues for
*removing* the bundle by parsimony, not for its noumenality. That must be stated, and §2.4 states
it.

---

# 1. TASK A — the free energy on sections

## 1.0 The tier, written out

I work at `def:hist-finite-configuration-tier` (`05d:235-273`), which the audit correctly
identifies as the cheapest available home. Every item below is already declared there; I add
nothing to the geometry.

- Base: `\mathcal C_\ell` compact smooth, with a **declared** finite positive Borel measure
  `\mu_\ell` and a measurable weight `w:\mathcal C_\ell\to(0,\infty)` bounded above and below.
- Principal bundle: `P=\mathcal C_\ell\times G` trivial, `G=(\R^K,+)` abelian, `\omega` the flat
  connection.
- Representation: `\rho_b(g)x = x+g` on the **sample** fiber `\mathsf K=\R^K`; the law action is
  the pushforward `\widehat\rho_b(g)q=(\rho_b(g))_\# q` of `eq:geo-pushforward-actions`.
- Fiber: `\mathcal B=\{\mathcal N(m,\Sigma_0):m\in\R^K\}` with `\Sigma_0\succ0` fixed, so
  `\widehat\rho_b(g)\mathcal N(m,\Sigma_0)=\mathcal N(m+g,\Sigma_0)` and the fiber Fisher form is
  the constant `g^F=\Sigma_0^{-1}`.
- Associated bundle `\mathcal E_b=P\times_{\widehat\rho_b}\mathcal B`, quotient convention
  `(u\cdot g,\beta)\sim(u,\widehat\rho(g)\beta)` (`eq:geo-quotient-convention`).

Two facts about this tier that I use repeatedly and that are worth isolating now, because the
audit's obstacle list guesses wrong about one of them.

**Fact T1 (the represented action is a Fisher–Rao isometry, automatically).** The audit lists
"whether `\rho` is by isometries of Fisher–Rao (if not, A2 fails)" as a candidate obstacle. It is
not an obstacle, and not only on this tier. The manuscript declares the law action to be a
*pushforward along a bimeasurable sample-coordinate change* (`eq:geo-pushforward-actions` together
with `hyp:pb-regular-models`, `05c:37-39`). Pushforward along a parameter-independent bimeasurable
bijection is a statistical isometry — this is exactly `prop:pb-statistical-tensor-descent`
(`05c:59`). So the isometry property is a consequence of the declarations already in the
manuscript, not an extra hypothesis. Numerically confirmed (CHECK A2a: Fisher form agrees to
`2.9e-15` under a random invertible sample map; the control with a rank-deficient sample map fires
with discrepancy `1.31`). Obstacle dismissed with proof.

**Fact T2 (`\mathcal B` is a `G`-torsor).** `G=(\R^K,+)` acts on `\mathcal B\cong\R^K` by
translation: freely and transitively. This innocuous-looking fact is what kills A3 (§1.3) and it
is a property of the exhibited tier as declared, not something I introduced.

## 1.1 A1 — the candidate definition, and the four choices it forces

Write `U\subseteq\mathcal C` open, `s\in\Gamma(U,\mathcal E_b)`.

**Candidate.**

```
  F_mu[s ; pi, E]  =  \int_U [ KL( s(c) || pi(c) )  +  < E(c), s(c) > ] w(c) d mu(c)     (A1)
```

with the four choices below. I state each choice, the reason, and the price.

**(i) Base measure.** There is no intrinsic measure on `\mathcal C`; `def:geo-context-base`
(`02:16`) declares smooth structure and nothing else, and `appendix_claim_ledger.tex` records that
no canonical connection is selected anywhere. I therefore take `\mu` to be **exogenous declared
data**, on exactly the same footing as `\omega`, and I write it into the functional's name. This
is not a dodge; `def:hist-finite-configuration-tier` already declares `\mu_\ell` and already
integrates against it in `eq:hist-finite-configuration-metric`, so the manuscript has already paid
this price once, for the configuration metric, without remarking on it. The price is recorded as
obstruction **O3** in §1.6, and it includes a direct collision with the manuscript's own N1
commitment ("the finite design is a declared subset, not a random sample from a law on
`\mathcal C`. No expectation over contexts is used", `12_philosophy.tex:33-38`): a positive finite
`\mu` normalizes to a probability law on `\mathcal C`, which is precisely what that sentence
forbids. **Task A and the N1 half of Task B are in direct tension, and one of them has to give.**

There is one genuinely reassuring result here, and I prove it in §1.5: for a jet-free integrand
and an unconstrained section class, the *minimizer* is `\mu`-almost-everywhere independent of
`\mu`. Non-canonicity of `\mu` corrupts the value of the free energy but not the inference it
selects, as long as no term couples distinct contexts. The moment a coupling term is added, `\mu`
becomes load-bearing on the argmin — and §1.4 shows every admissible coupling term is excluded.

**(ii) Integrand: pointwise VFE density, not Fisher-length-weighted.** The two candidates are a
pointwise divergence density and something built from the Fisher pullback `h_s^\omega`
(`eq:pb-fisher-pullback`). I take the pointwise density. Three independent arguments, developed in
§§1.4–1.5, force this: finite-design consistency forbids jet dependence (Theorem A4.4); the
`L^2`-Fisher metric is strong but only `C^1` for jet-free objectives, and the manuscript supplies
its own `H^1` counterexample against gradient-energy objectives (`05d:344-353`); and a
Fisher-length weighting `\sqrt{\det h_s^\omega}` is degenerate whenever `\mathrm{rank}\,h_s^\omega
< \dim\mathcal C`, which on the exhibited tier is generic (`h_s^\omega = dm^\top\Sigma_0^{-1}dm`
has rank `\le\min(K,\dim\mathcal C)`). The two terms in (A1) are the two terms of the finite-design
free energy: a divergence against a background and an expected energy.

**(iii) Function space.** `s\in L^2_\mu(U;\mathcal E_b)`, meaning: `s` is a Borel section with
`\KL(s(\cdot)\Vert\pi(\cdot))\in L^1(w\mu)` and `\langle E,s\rangle\in L^1(w\mu)`. On the exhibited
tier, identifying `s` with its mean field `m:U\to\R^K` (legitimate because `\mathcal B\cong\R^K`),
this is exactly `\mathcal Q^{L^2}=L^2(\mu;\R^K)` of `05d:333`, whose metric
`\mathsf G^{L^2}(V,W)=\int V^\top\Sigma_0^{-1}W\,w\,d\mu` the manuscript already proves strong
under two-sided bounds on `w` and `\Sigma_0`. Measurability is not an obstacle: relative entropy is
jointly lower semicontinuous, hence jointly Borel, on `\mathcal P(S)^2` for `S` Polish, and
`\langle E,s\rangle` is Borel by the kernel Fubini theorem. This dispatches the audit's
"measurability of `c\mapsto q(c)`" candidate obstacle (**O7**, dismissed).

**(iv) Boundary and decay.** On compact `\mathcal C_\ell` with finite `\mu_\ell`, none needed. On
noncompact `\mathcal C`, the finiteness requirement in (iii) *is* the decay condition: `s\to\pi` at
infinity in the `w\mu`-weighted relative-entropy sense. No boundary term appears because no
derivative of `s` appears; this is a further consequence of choice (ii) and it is why the first
variation in §1.5 has no integration by parts.

**Background data are part of the definition.** `\pi\in\Gamma(U,\mathcal E_b)` is a *section*, not
a fixed law in a fixed chart, and `E` is a *section of the associated function bundle*
`P\times_{\rho_b^\ast}\mathcal M(\mathsf K)`, transforming by `E_\beta(c)=E_\alpha(c)\circ
\rho_b(g_{\alpha\beta}(c))`. Both requirements are forced by A2 below, and the second is exactly
`eq:gen-gauge-pushforward-obs` (`04:394-398`), the third line of `hyp:gen-kernel-covariance`. The
same hypothesis Task B needs is the hypothesis Task A needs; this is not a coincidence and §2.2
explains why.

## 1.2 A2 — frame independence: **PROVED**, in complete generality

Let `u_\alpha,u_\beta:U\to P` be two local frames with `u_\beta=u_\alpha\cdot g_{\alpha\beta}`,
`g_{\alpha\beta}:U\to G`. Write `\beta_\alpha,\beta_\beta:U\to\mathcal B` for the local
representatives of `s`, and `\pi_\alpha,\pi_\beta` for those of `\pi`.

**Step 1, the transformation law.** By `eq:geo-quotient-convention`,

```
  [u_beta(c), beta_beta(c)] = [u_alpha(c) g_ab(c), beta_beta(c)]
                            = [u_alpha(c), rho^(g_ab(c)) beta_beta(c)] ,
```

so `\beta_\alpha=\widehat\rho(g_{\alpha\beta})\beta_\beta`, that is
`\beta_\beta=\widehat\rho(g_{\alpha\beta})^{-1}\beta_\alpha`, in agreement with
`eq:geo-local-reframing` (`02:159-161`). Identically `\pi_\beta=\widehat\rho(g_{\alpha\beta})^{-1}
\pi_\alpha`.

**Step 2, the divergence term.** Write `r=\rho_b(g_{\alpha\beta}(c))^{-1}`, a bimeasurable
bijection of `(\mathsf K,\mathscr K)`. Then `A\mapsto r^{-1}A` is a `\sigma`-algebra isomorphism,
so `P\ll Q \iff r_\#P\ll r_\#Q`, and where absolute continuity holds,
`\dfrac{d(r_\#P)}{d(r_\#Q)}=\dfrac{dP}{dQ}\circ r^{-1}`. Hence

```
  KL( r_# P || r_# Q ) = \int log( dP/dQ o r^{-1} ) d(r_# P)
                       = \int log( dP/dQ ) dP  =  KL( P || Q ),                     (A2.1)
```

and the value `+\infty` transfers in both directions. Therefore
`\KL(\beta_\beta(c)\Vert\pi_\beta(c))=\KL(\beta_\alpha(c)\Vert\pi_\alpha(c))`.

**Step 3, the energy term.** With the declared transformation law for `E`,

```
  < E_beta(c), beta_beta(c) >  = \int E_alpha(c)( rho(g) x ) d( (rho(g)^{-1})_# beta_alpha(c) )(x)
                               = \int E_alpha(c)( rho(g) rho(g)^{-1} y ) d beta_alpha(c)(y)
                               = < E_alpha(c), beta_alpha(c) > .                     (A2.2)
```

**Step 4.** Summing, `f_\beta(c)=f_\alpha(c)` pointwise on `U`, so the integrand is a
frame-independent `[0,+\infty]`-valued Borel function on `U`; `\mu` and `w` are base objects and
frames do not touch them. Hence `\mathcal F_\mu[s;\pi,E]` is independent of the trivialization.
`\square`

**What this proof used, and what it did not.** It used only measurability of the group action,
that the action on laws is a pushforward along a bimeasurable bijection, that `\pi` is a section,
and that `E` is a section of the associated function bundle. It used **no** smoothness, **no**
connection, **no** Lie structure, **no** finite-dimensionality, and **no** manifold structure on
`\mathcal B`. A2 therefore holds at the general measurable tier of `02:135`, which is a stronger
result than the audit asked for. The audit's candidate obstacle "the fiber `\mathcal B` is only a
manifold under extra hypotheses (G7)" therefore does not touch A2 (**O5**, dismissed for A2; still
live for A5).

**A2 also survives a jet term.** Had I kept `D^\omega s` in the integrand, A2 would still hold, by
`eq:pb-covariant-jet-gauge-law` and `thm:pb-pullback-gauge-invariance` (`05c:124`). So A2 is not
where the construction breaks. This matters: it means the failures in §§1.3–1.4 are not
bookkeeping failures.

**The two ways A2 fails, and they are the same computation.** If `\pi` is declared as a *fixed
law* in one chart rather than as a section, then in frame `u_\beta` it reads
`\mathcal N(-g_{\alpha\beta}(c),\Sigma_0)` instead of `\mathcal N(0,\Sigma_0)`, and the divergence
changes by `\tfrac12(m+g)^\top\Sigma_0^{-1}(m+g)-\tfrac12 m^\top\Sigma_0^{-1}m`. If `E` is declared
per-chart rather than as a section of the associated function bundle, the same discrepancy appears
in the energy term; this is precisely the failure that CHECK B4 exhibits numerically (discrepancy
`192.94` when `eq:gen-gauge-pushforward-obs` is violated, against `9.9e-14` when it is respected).
The passive frame-dependence of a chart-declared background and the active gauge non-invariance of
§1.3 are one computation seen twice.

## 1.3 A3 — `\mathrm{Aut}_G(P)`-invariance: **REFUTED as invariance, PROVED as equivariance**

Let `F\in\mathrm{Aut}_G(P)` over `\mathrm{id}_{\mathcal C}`, inducing `\bar F:\mathcal E_b\to
\mathcal E_b`, `[u,\beta]\mapsto[F(u),\beta]`, and acting on sections by `F\cdot s:=\bar F\circ s`.
Writing `F(u_\alpha)=u_\alpha\cdot k_\alpha` with `k_\alpha:U\to G` (`02:171-177`), the local
representative of `F\cdot s` is `\widehat\rho(k_\alpha)\beta_\alpha`.

**Proposition A3.1 (equivariance, true).**
`\mathcal F_\mu[F\cdot s;\,F\cdot\pi,\,F\cdot E] = \mathcal F_\mu[s;\pi,E]`.
*Proof.* Immediate from (A2.1) and (A2.2) with `g_{\alpha\beta}` replaced by `k_\alpha`. `\square`
Verified numerically to exactly `0.0` residual (CHECK 4).

**Proposition A3.2 (invariance at fixed background, false).**
`\mathcal F_\mu[F\cdot s;\pi,E]\ne\mathcal F_\mu[s;\pi,E]` in general.
*Witness.* Exhibited tier, `K=1`, `\pi\equiv\mathcal N(0,\Sigma_0)` as a section, `E=0`,
`\mathcal F_\mu[s]=\tfrac12\int m(c)^2\Sigma_0^{-1}w\,d\mu`. The gauge transformation with local
function `\lambda:\mathcal C\to\R` sends `m\mapsto m+\lambda`, giving
`\tfrac12\int (m+\lambda)^2\Sigma_0^{-1}w\,d\mu`. Verified numerically: `1.9606` against `2.9274`
(CHECK 4). This is the section-space analogue of the manuscript's own active-gauge counterexample
at `05c:150-154`.

The interesting statement is not either of these. It is the classification of what an invariant
free energy *could* be.

**Theorem A3.3 (orbit-space criterion).** Let `\mathcal F_\mu[s]=\int_{\mathcal C}f(c,s(c))\,d\mu`
be frame-independent, with `\mu` of full support and `G` connected. Then `\mathcal F_\mu` is
`\mathrm{Aut}_G(P)`-invariant if and only if, for `\mu`-almost every `c`, the fiberwise integrand
`f_\alpha(c,\cdot)` is constant on `\widehat\rho(G)`-orbits, that is, if and only if it descends to
the orbit space `\mathcal B/G`.
*Proof.* Frame-independence says exactly that `f` is a well-defined function on the total space
`\mathcal E_b`, equivalently that `f_\alpha(c,\beta)` is an arbitrary function of `(c,\beta)` in a
fixed frame. Gauge invariance requires `f_\alpha(c,\widehat\rho(k(c))\beta)=f_\alpha(c,\beta)` for
every gauge function `k` and every section value `\beta`. That every triple `(c,g,\beta)` is
realized by some smooth `k` and some smooth section is the evaluation-surjectivity argument the
manuscript already makes at `04:359-364` for connected `G` by smooth interpolation in disjoint
coordinate neighborhoods. Conversely orbit-constancy gives invariance term by term. `\square`

**Corollary A3.4 (gauge triviality on the exhibited tier).** On
`def:hist-finite-configuration-tier`, `\mathcal B` is a free transitive `G`-space (Fact T2), so
`\mathcal E_b\cong P` as a principal `G`-bundle, `\Gamma(\mathcal C,\mathcal E_b)` is a torsor under
`\mathrm{Aut}_G(P)\cong C^\infty(\mathcal C,G)`, and `\mathcal B/G` is a single point. Hence
**every `\mathrm{Aut}_G(P)`-invariant functional on sections is constant.**
*Proof.* For sections `s_1,s_2` the difference field `\kappa=m_2-m_1` is smooth, and the gauge
transformation with local function `\kappa` carries `s_1` to `s_2`; the action is free because
`s\cdot\tau=s` forces `\tau=e`. Simple transitivity plus invariance gives constancy; alternatively
apply Theorem A3.3 with a one-point orbit space. `\square`
The transitivity step is verified constructively (CHECK 4: `\Vert F_{\lambda^\ast}\cdot s-s_2\Vert
=4.4\mathrm{e}{-16}`).

**Corollary A3.5 (classification on the Gaussian belief fiber).** Let
`\mathcal B_b=\{\mathcal N(\mu,\Sigma)\}\cong\R^K\times\mathrm{SPD}(K)` with the pushforward
action.
For `G=(\R^K,+)` acting by translation, `\mathcal B_b/G\cong\mathrm{SPD}(K)`, so every
`\mathrm{Aut}_G(P)`-invariant local free energy is a functional of the **covariance field alone**
and cannot see the mean.
For `G=\mathrm{GL}^+(K)` with `K\ge2`, `\mathcal B_b/G\cong[0,\infty)` parameterized by
`r(\mu,\Sigma)=(\mu^\top\Sigma^{-1}\mu)^{1/2}`, so every such functional has the form
`\int_{\mathcal C}\psi(c,r(s(c)))\,d\mu(c)`; for `K=1` the invariant is the signed `\mu/\sigma`.
*Proof of the `\mathrm{GL}^+` case.* Invariance of `r` is immediate. Completeness: normalize by
`\Sigma^{-1/2}` and use transitivity of `SO(K)` on the sphere of radius `r`, which lies in
`\mathrm{GL}^+`. `\square`
Verified numerically: invariance of `r^2` to `1.3e-13`; explicit `A^\ast\in\mathrm{GL}^+(4)`
carrying one pair to another with residuals `4.4\mathrm{e}{-16}` and `4.4\mathrm{e}{-15}` and
`\det A^\ast=+0.419` (CHECK A3.3).

**Reading.** Requirement (b) of the audit's fix list — "invariance under `\mathrm{Aut}_G(P)`" —
is, on the recommended tier, equivalent to the free energy being constant, and on the full Gaussian
tier with the translation group it is equivalent to the free energy being blind to the entire mean
sector, which is where all inference content lives. The requirement as stated is not merely
unfulfilled; it is unfulfillable. The repair is to state requirement (b) as **equivariance on the
triple `(s,\pi,E)`**, which is Proposition A3.1, and to accept the consequence: the background data
are not gauge-invariant, so the theory carries a gauge fixing inside its declared background, and
the "noumenal" bundle is meaningful only relative to it.

## 1.4 A4 — consistency with the finite-design functional: **PROVED, with an exact defect, and then a no-go**

This is where `hyp:prob-sampling-compatibility` is replaced by something that identifies.

**The structural move.** Take the fiber to be the **population fiber at one context**,
`\mathcal B^{\mathrm{pop}}=\mathcal P\big(\prod_{i\in V}(\mathsf K_i\times\mathsf M_i)\big)`, rather
than a per-agent law fiber. This is the one modification I make to the manuscript's geometry, and
it is what kills direction (i) of `prop:prob-compatibility-nonidentifiability` (`03:418`): the
non-identification there is "coordinate marginals do not determine a sufficiently rich joint", and
it evaporates once the fiber value *is* the joint at that context rather than a family of
marginals.

**Theorem A4.1 (design consistency with exact cross-context defect).** Assume
`hyp:gen-design-product` (`04:96`), so `P_\theta=\bigotimes_{a}P_{\theta,a}`. Let `Q_X(\cdot\mid o)
\in\mathcal P(\mathsf Y_D)` be *any* recognition law, with design marginals `Q_a`. Define the
design-restricted section `s_Q(c_a):=[u_\alpha(c_a),Q_a]`, which is frame-independent by A2, and
set `\mu_D=\sum_a\delta_{c_a}`, `w\equiv1`. Then, whenever the classical domain
`hyp:elbo-evidence-domain` holds,

```
  F[ Q_X ; X, o ]  =  \int_{\mathcal C} f( c, s_Q(c) ) d mu_D(c)  +  TC_D( Q_X ),        (A4.1)

  f( c_a, Q_a ) = E_{Q_a}[ log q_a(Y_a) - log p_{theta,a}( o_a, Y_a | X ) ] ,
  TC_D( Q_X )   = KL( Q_X || (x)_a Q_a )  >= 0 ,
```

with equality `\Fenergy=\int f\,d\mu_D` exactly when `Q_X` is design-product.
*Proof.* `\Fenergy[Q_X]=\E_{Q}[\log q]-\sum_a\E_{Q_a}[\log p_{\theta,a}]` by
`eq:gen-design-product`. Write `-H(Q)=\E_Q[\log q]` and `-\sum_a H(Q_a)=\sum_a\E_{Q_a}[\log q_a]`;
then `\mathrm{TC}_D(Q)=\sum_a H(Q_a)-H(Q)` gives `\E_Q[\log q]=\sum_a\E_{Q_a}[\log q_a]+
\mathrm{TC}_D(Q)`. Substituting gives (A4.1). `\square`
Verified numerically: `M=3`, `K=2`, correlated Gaussian `Q` on `\R^6`, residual
`\vert\Fenergy-(\sum_a\Fenergy_a+\mathrm{TC}_D)\vert=1.42\mathrm{e}{-14}` in closed form, with a
`4\times10^6`-sample Monte Carlo cross-check agreeing at `0.78` standard errors; **control**: for
design-product `Q` the defect is exactly `0.0` and the residual is `1.42\mathrm{e}{-14}` (CHECK 1).

**Why (A4.1) is the right replacement for `hyp:prob-sampling-compatibility`.** The manuscript's
bridge is a *hypothesis* asserting that section values equal recognition marginals, and
`prop:prob-compatibility-nonidentifiability` proves it determines neither side. (A4.1) is not a
hypothesis. The section is *constructed from* `Q_X` by design-marginalization, so the map
`Q_X\mapsto s_Q` is total and well defined; and the information lost in that construction is not
discarded but exhibited as the nonnegative term `\mathrm{TC}_D(Q_X)`. Direction (i) of the
non-identification is removed by the population fiber; direction (i)'s residue, the cross-design
dependence, is measured exactly. This is the base-manifold analogue of `eq:obs-global-ledger`
(`05b:441`), where total correlation is likewise the exact local-to-global gap, and it delivers
item 5 of the audit's shortest path ("local-to-global over `\mathcal C` with an exact defect
term") as a free corollary, without a partition of unity.

**Direction (ii) does not go away, and cannot.**

**Proposition A4.2 (design-supported measures do not identify a section).** If
`\mathrm{supp}\,\mu\subseteq D` and the section class contains a nonzero deformation supported off
`D`, then `\mathcal F_\mu` is constant on the fibers of the evaluation map
`\mathrm{ev}_D:\Gamma\to\prod_a(\mathcal E_b)_{c_a}`, each of which is infinite-dimensional.
*Proof.* Immediate; the deformation witness is the bump construction of
`prop:prob-compatibility-nonidentifiability`(ii). `\square`
So `\mathcal F_{\mu_D}` is a functional of finitely many fiber values. It is a "functional on
sections" in name only.

**Proposition A4.3 (unisolvence restores identification, and coincides with metric
nondegeneracy).** Replace `\Gamma` by the finite-dimensional tier `\mathcal Q_\ell=\{s_\xi\}` of
`def:hist-finite-configuration-tier` and let `\mathrm{Ev}_D\in\R^{MK\times N}` be the design
evaluation matrix with blocks `\phi_b(c_a)`. Then `\mathrm{ev}_D` is injective on `\mathcal Q_\ell`
if and only if `\mathrm{rank}\,\mathrm{Ev}_D=N` (hence necessarily `N\le MK`), and this is
**exactly** the condition under which the configuration Gram form of
`eq:hist-configuration-gram` at `\mu=\mu_D`,
`\Phi=\mathrm{Ev}_D^\top(\mathrm{diag}(\rho)\otimes\Sigma_0^{-1})\mathrm{Ev}_D`, is positive
definite.
Verified numerically on the manuscript's own `S^1` example (`05d:325-329`): with
`\{\phi_a\}=\{1,\cos\theta,\sin\theta\}`, `K=1`, three design points give
`\mathrm{rank}\,\mathrm{Ev}_D=3` and `\mathrm{eig}(\Phi)\subset\{1.30,1.68,3.02\}`; two design
points give rank `2` and `\lambda_{\min}(\Phi)=0` exactly (CHECK 3). The exact continuum Gram
matrix `\Phi=\mathrm{diag}(1,\tfrac12,\tfrac12)`, `\det=\tfrac14`, is reproduced symbolically
(CHECK 2), matching `05d:327`.
This identifies the *same* rank condition as the manuscript's degeneracy remark at `05d:320-323`
("whenever `N>MK` the metric is degenerate") and as the design-identifiability condition. That
coincidence is worth stating in the manuscript as a lemma; it is currently unremarked.

Now the no-go.

**Theorem A4.4 (finite-design consistency forces a jet-free integrand).** Let
`\mathcal F_\mu[s]=\int f(c,s(c),D^\omega s(c))\,d\mu` with `\mathrm{supp}\,\mu\subseteq D`, and
require `\mathcal F_\mu[s]=\Fenergy[Q_X;X,o]` for every admissible pair `(s,Q_X)` related as in
Theorem A4.1. Then:
(a) if for some `a` the section class contains two sections agreeing at every point of `D` but with
different `D^\omega s(c_a)`, then `f(c_a,\cdot,\cdot)` does not depend on its jet argument, and the
connection `\omega` is provably absent from `\mathcal F_\mu`;
(b) if the class is unisolvent on `D`, so that no such pair exists, then the jet dependence of `f`
is **not identified** by the consistency requirement: for any `\varphi`, replacing `f` by
`f+\varphi(c,D^\omega s)-\varphi(c,J(\mathrm{ev}_D s))` — where `J` is the jet-from-values map that
unisolvence supplies — satisfies the same requirement.
*Proof.* (a) Evaluate the consistency requirement on the two sections; the right-hand sides agree
because `\Fenergy` depends on `s` only through `\{Q_a\}=\{s(c_a)\}`; subtract. (b) The added terms
cancel on the design by construction. `\square`
The deformation required in (a) is explicit and elementary: with `D=\{0,2,4\}\subset\R` take
`\chi(c)=(c-0)(c-2)(c-4)`, which vanishes at every design point while
`\chi'\vert_D=(8,-4,8)\ne0` (CHECK 7). Any `C^\infty` or `C^1` section class on a
positive-dimensional base contains such deformations. Case (a) is therefore the generic case, and
case (b) holds only for rigid finite-dimensional families in which "the space of sections" is a
relabeling of `\R^N`.

**Theorem A4.5 (a genuine integral is not consistent with any finite-design functional).** If
`\mu(\mathcal C\setminus D)>0` and `f(c,\cdot)>0` on a set of positive `\mu`-measure off `D`, then
`\mathcal F_\mu[s]-\Fenergy[Q_X;X,o]=\int_{\mathcal C\setminus D}f\,d\mu>0`, and this difference is
not a function of `Q_X`. Hence `\mathcal F_\mu` can at best be an *extension* of `\Fenergy`, and
the extension is not determined: every `\mu` with `\mu\vert_D=\mu_D` gives one. This is the exact
content of `open:prob-continuum-theory` (`03:443`), now localized: the underdetermination is not a
technical gap in the projective-limit construction, it is present already at the level of the
functional.

**Summary of A4.** Consistency in the sense the audit asked for is *achievable* — Theorem A4.1
does it, with an exact defect and a proof rather than a hypothesis — but only for a jet-free
integrand and only against a design-supported measure. Buying consistency costs the connection.

## 1.5 A5 — first variation, flow, well-posedness

Identify `s` with `m\in L^2(\mu;\R^K)` and write `\varepsilon_c(m):=\langle E(c),\mathcal N(m,
\Sigma_0)\rangle`. Then

```
  F_mu[m]  =  \int_C w(c) [ 1/2 |m - m_pi|^2_{Sigma_0^{-1}}  +  eps_c(m) ] d mu(c) ,
  delta F_mu[V] = \int_C w(c) [ < Sigma_0^{-1}(m - m_pi), V > + < grad eps_c(m), V > ] d mu(c) .
```

With the configuration metric `\mathsf G(U,V)=\int w\langle\Sigma_0^{-1}U,V\rangle\,d\mu` of
`eq:hist-finite-configuration-metric` — which is exactly the `L^2(\mathcal C,\mu)` metric induced
by the fiberwise Fisher–Rao form, the natural candidate the audit names — Riesz representation
gives the natural gradient

```
  grad F_mu (m)(c)  =  ( m(c) - m_pi(c) )  +  Sigma_0 grad eps_c( m(c) )     mu-a.e.       (A5.1)
```

and the flow `\dot m=-\mathrm{grad}\,\mathcal F_\mu(m)`. Verified numerically: the identity
`\delta\mathcal F[V]=\mathsf G(\mathrm{grad}\,\mathcal F,V)` holds to `1.4\mathrm{e}{-9}` at a
central-difference step of `10^{-6}` (CHECK 6).

**Three structural observations, all of them consequences of jet-freeness.**

First, the flow is a **decoupled family of ODEs indexed by `c`**. No derivative of `m` appears, so
distinct contexts never talk to each other. The section space is doing no work beyond bookkeeping,
and neither is `\omega`.

Second, **the minimizer is `\mu`-independent**. Since (A5.1) vanishes pointwise, the stationary
condition is a pointwise equation whose solution does not involve `\mu`; changing `\mu` (keeping
full support) changes the value of `\mathcal F_\mu` but not its argmin up to `\mu`-null sets. This
is the reassuring half of obstruction O3.

Third, **well-posedness is clean and the constants are explicit**. If `\nabla\varepsilon_c` is
globally Lipschitz uniformly in `c` and measurable in `c`, Picard–Lindelöf in `L^2(\mu;\R^K)`
gives a unique global solution; if `\varepsilon_c` is `\lambda`-convex, `\mathcal F_\mu` is
`(1+\lambda)`-strongly convex in the `\mathsf G` metric and the flow contracts exponentially at
rate `\lambda_{\min}(I+\Sigma_0\nabla^2\varepsilon)`. For the quadratic energy
`\varepsilon_c(m)=\tfrac12\vert m-o_c\vert^2_{\Sigma_o^{-1}}` the flow matrix is
`A=I+\Sigma_0\Sigma_o^{-1}` with `\mathrm{eig}(A)=\{1.861,4.784\}` and rate `1.861`; integrating to
`T=20` lands within `1.0\mathrm{e}{-13}` of the fixed point, and `\Vert\mathrm{grad}\,\mathcal F
(m^\ast)\Vert_\infty=1.6\mathrm{e}{-15}` (CHECK 6). **Control**: the fixed point equals the exact
contextwise Gaussian posterior mean to `4.4\mathrm{e}{-16}`, confirming that the construction
recovers Bayesian inference contextwise and is not an artifact.

**What would need to be true, and what fails if the integrand is not jet-free.** Well-posedness
needs `\mathsf G` strong, which `05d:334-340` supplies under two-sided bounds on `w` and
`\Sigma_0`, and it needs `\mathcal F_\mu` to be `C^1` on `L^2`. The manuscript states in its own
voice that "the price is that `\Fenergy` must be `C^1` on `L^2`, which excludes gradient-energy
objectives" and supplies the witness: on `S^1` with `\Gamma=H^1`,
`\Fenergy(Q)=\tfrac12\int\vert Q'\vert^2`, the configuration `Q=\sum_k k^{-2}\sin k\theta` has no
`L^2` gradient (`05d:344-353`). A Fisher-pullback term is a gradient-energy objective. So the
`L^2`-Fisher metric — the audit's natural candidate, and the manuscript's declared standing tier
(`hyp:hist-standing-configuration-tier`) — is well-posed **only** for the jet-free integrand.
This is a third, independent route to the same conclusion as Theorem A4.4 and Corollary A3.4.

## 1.6 A6 — where it breaks, ranked

**O1 — CRITICAL. Gauge invariance and nonconstancy are incompatible on the recommended tier.**
Precise statement: Theorem A3.3 and Corollary A3.4. `\mathcal B` is a `G`-torsor, so
`\mathcal B/G` is a point, `\mathrm{Aut}_G(P)` acts simply transitively on
`\Gamma(\mathcal C,\mathcal E_b)`, and every invariant functional is constant. Requirement (b) of
the audit's fix list is unfulfillable as stated. Repair: state it as equivariance on
`(s,\pi,E)` (Proposition A3.1) and accept that the background data carry a gauge fixing. Cost of
the repair: the theory's gauge-invariant content is *relative* configuration only, which on this
tier is a single `\R^K`-valued field, and the bundle contributes nothing beyond a global torsor
structure.

**O2 — CRITICAL. Finite-design consistency forces the connection out of the free energy.**
Precise statement: Theorem A4.4(a), reinforced independently by the `C^1`-on-`L^2` failure in §1.5.
This converts audit finding S3 from an observation into a necessity proof. Any future attempt to
put `\omega` into `\Fenergy` must break one of: the finite design (`03:15`),
`hyp:gen-design-product` (`04:96`), or the `L^2` standing tier
(`hyp:hist-standing-configuration-tier`, `05d:355`).

**O3 — HIGH. No canonical base measure, and declaring one contradicts N1.** `\mu` is exogenous, on
the same footing as `\omega`, and a positive finite `\mu` normalizes to a probability law on
`\mathcal C`, which `12_philosophy.tex:33-38` explicitly disclaims ("No expectation over contexts
is used"). Mitigation: for jet-free integrands the argmin is `\mu`-independent (§1.5), so the
damage is confined to the value of the functional. But the mitigation is available only in the
regime O2 already forces, so it is not an escape.

**O4 — HIGH. Off-design non-identification of the section is irreparable for finite `\mu`.**
Proposition A4.2. Repairable only by restricting to a unisolvent finite-dimensional class
(Proposition A4.3), which makes "section space" a relabeling of `\R^N` and removes every
sheaf-theoretic or local-to-global question the goal sentence is interested in.

**O5 — MEDIUM. Fiber manifold status (audit G7).** Dismissed for A2, which is purely measurable.
Dismissed on the exhibited tier for A5, since `\{\mathcal N(m,\Sigma_0)\}` is an embedded
submanifold of `\mathcal P(\R^K)` diffeomorphic to `\R^K`. Live at the general tier: `02:69-74`
declares `\mathcal B_x\subseteq\mathcal P(\mathsf K)` a subset and `05c:52-57` gives it tangent
spaces; the first variation of §1.5 needs the manifold structure and `hyp:pb-regular-models`, not
merely `hyp:geo-smooth-tier`.

**O6 — DISMISSED WITH PROOF. Whether `\rho` acts by Fisher–Rao isometries.** It does,
automatically, because the manuscript declares the law action to be a pushforward
(`eq:geo-pushforward-actions`) along a parameter-independent bimeasurable bijection
(`hyp:pb-regular-models`). Fact T1, `prop:pb-statistical-tensor-descent`, verified at `2.9e-15`
with a firing rank-deficiency control.

**O7 — DISMISSED. Measurability of `c\mapsto q(c)`.** Relative entropy is jointly lower
semicontinuous hence Borel on `\mathcal P(S)^2` for Polish `S`; the energy pairing is Borel by the
kernel Fubini theorem. Requires only that `\mathsf K` be standard Borel, `\mathcal B` Borel in
`\mathcal P(\mathsf K)`, `s` Borel — all declarable and consistent with `03_probability.tex`.

**O8 — LOW. Noncompact `\mathcal C`.** Handled by the integrability requirement in §1.1(iii),
which is the decay condition `s\to\pi` at infinity in the `w\mu`-weighted relative-entropy sense.
No obstruction, and no canonical choice either.

**O9 — DISMISSED, with a positive note the manuscript should keep.** Existence of local sections
(audit G3) is not an issue for Gaussian fibers: `\R^K\times\mathrm{SPD}(K)` is contractible, so
`\mathcal E_b` admits global sections over any base regardless of the topology of `P`. Topology
obstructs frames, never agents. This is audit finding G4 and it is one line to state.

## 1.7 The one route by which `\omega` could still earn its place

O2 forbids `\omega` from entering the integrand. It does not forbid `\omega` from constraining the
*background*. Require the prior section to be `\omega`-parallel, `D^\omega\pi=0`. Then a global
parallel background exists on `U` if and only if the holonomy group of `\omega` restricted to `U`
has a fixed point in `\mathcal B` under `\widehat\rho`; and for a `G`-torsor fiber
`\widehat\rho` has a fixed point if and only if the holonomy is trivial. So on the exhibited tier:

> A global parallel background section of `\mathcal E_b` exists if and only if `\mathrm{Hol}(\omega)
> =\{e\}`. The obstruction to declaring a gauge-covariant background is exactly the holonomy.

This puts `\omega` into the theory as an *existence obstruction for the background data* rather
than as a term in the energy, it survives Theorem A4.4 (the integrand stays jet-free), it survives
Corollary A3.4 (the pair `(s,\pi)` has a nontrivial invariant), and it is the first place in the
program where curvature would be doing work. It does not make holonomy observable in the record —
§2.3 shows that is separately blocked — but it is the shortest path from "the gauge sector is
inert" to "the gauge sector constrains what backgrounds are declarable". I recommend it as the
successor task.

---

# 2. TASK B — the noumenal indistinguishability theorem N3(a)

## 2.1 B1 — precise statement

**The observation record.** `o\in\mathsf O_D=\prod_{a=1}^M\prod_{i\in V}\mathsf O_{i,a}` with
`\mathscr O_D` the product `\sigma`-algebra (`eq:prob-observation-space`, `03:30`). A **record
statistic** is any measurable `\Psi:(\mathsf O_D,\mathscr O_D)\to(S,\mathscr S)`.

**The datum.** A *bundle-with-connection-and-section datum over the design `D`* is
`\mathfrak D=(P,\omega_b,\omega_m,(\mathcal C_i,u_i^b,u_i^m)_{i\in V},(q_i,s_i)_{i\in V},\theta,X)`
with `P\to\mathcal C` principal `G`, `\omega_x` principal connections (`def:geo-connections`),
`u_i^x` local frames (`eq:geo-frame-sections`), `q_i\in\Gamma(\mathcal C_i,\mathcal E_b\vert
_{\mathcal C_i})` and `s_i\in\Gamma(\mathcal C_i,\mathcal E_m\vert_{\mathcal C_i})`
(`def:geo-agent`), and `(\theta,X)` generative data satisfying `def:prob-structural-kernel-
signatures` and `cons:gen-finite-directed-law`.

**The induced law.** `\Lambda(\mathfrak D):=P^O_{\theta,X}=P_\theta(\cdot\times\mathsf Y_D\mid X)`,
the `\mathsf O_D`-marginal of `eq:gen-design-product`.

**The equivalence.** `\mathfrak D\cong\mathfrak D'` when there is a `G`-equivariant diffeomorphism
`F:P\to P'` with `\pi'\circ F=\pi` (an isomorphism of principal bundles covering
`\mathrm{id}_{\mathcal C}`), such that `\omega'_x=(F^{-1})^\ast\omega_x`, `\mathcal C_i'=\mathcal
C_i`, the sections intertwine, `q_i'=\bar F_b\circ q_i` and `s_i'=\bar F_m\circ s_i` where
`\bar F_x[u,\beta]=[F(u),\beta]`, and `(\theta',X')` is obtained from `(\theta,X)` by
`hyp:gen-kernel-covariance` for the frame comparison induced by `F`.

**Theorem N3(a).** If `\mathfrak D\cong\mathfrak D'` then `\Lambda(\mathfrak D')=\Lambda
(\mathfrak D)` as probability measures on `(\mathsf O_D,\mathscr O_D)`. Consequently
`\Psi_\#\Lambda(\mathfrak D')=\Psi_\#\Lambda(\mathfrak D)` for every record statistic `\Psi`, no
record statistic separates the two data, and `p_{\theta'}(o\mid X')=p_\theta(o\mid X)` for
`\nu_D^O`-almost every `o`, so the evidence, the exact identity `thm:elbo-exact-identity`, and the
free energy of correspondingly transported recognition laws all agree.

## 2.2 B2 — proof

*Step 1 (the isomorphism produces exactly the passive product action).* Set `\hat u_i^x:=F\circ
u_i^x`. Because `F` is `G`-equivariant and covers the identity, `\hat u_i^x` is a smooth local
section of `P'` over `\mathcal C_i`. If `\mathfrak D'` carries declared frames `u_i^{x\prime}`,
then each principal fiber of `P'` is a right `G`-torsor, so there are unique smooth
`g_i^x:\mathcal C_i\to G` with `\hat u_i^x=u_i^{x\prime}\cdot g_i^x` — the same torsor argument
that gives `eq:geo-relative-frame` at `02:57-65`. Evaluating on the design gives
`g_{a,i}^x=g_i^x(c_a)` and represented operators `R_{a,i}^x=\rho_x(g_{a,i}^x)`. These are precisely
the elements of the passive product of `def:gen-product-action` (`04:376`), and by the
smooth-interpolation argument at `04:359-364` every such element is realized when `G` is connected.

*Step 2 (the sections have identical coordinates in the transported frames).* Let `\beta_i` be the
local representative of `q_i` in `u_i^b`, so `q_i(c)=[u_i^b(c),\beta_i(c)]`. Then
`q_i'(c)=\bar F_b(q_i(c))=[F(u_i^b(c)),\beta_i(c)]=[\hat u_i^b(c),\beta_i(c)]`, so in the
transported frame the coordinate is unchanged; in the declared frame `u_i^{b\prime}` the quotient
convention `eq:geo-quotient-convention` gives the coordinate `\widehat\rho_b(g_i^b(c))\beta_i(c)`.
The model channel is identical with `b` replaced by `m`. So the entire difference between the two
data, expressed in their declared frames, is the passive change of coordinates by `R^b` and `R^m`.

*Step 3 (evidence invariance).* By hypothesis `(\theta',X')` satisfies `hyp:gen-kernel-covariance`
(`04:379`, equations `eq:gen-gauge-pushforward-model`, `eq:gen-gauge-pushforward-state`,
`eq:gen-gauge-pushforward-obs`) for these `R`. Apply `prop:gen-product-evidence-invariance`
(`04:408`): with `T(o,y)=(o,Ry)` and `R=\bigoplus_{a,i}(R^b_{a,i}\oplus R^m_{a,i})`,

```
   P_{theta'}( . | X' )  =  T_#  P_theta( . | X )                                     (B2.1)
```

as measures, with no density or reference-measure hypothesis. Since `T` is the identity in the
observation coordinate, `\mathrm{pr}_{\mathsf O_D}\circ T=\mathrm{pr}_{\mathsf O_D}`, hence

```
   Lambda( D' ) = (pr)_# T_# P_theta = ( pr o T )_# P_theta = (pr)_# P_theta = Lambda( D ) .
```

Pushing forward by any measurable `\Psi` preserves the equality, and
`eq:gen-gauge-evidence-invariance` gives the almost-everywhere density statement. `\square`

*Numerical witness and control.* A two-agent chain with `K=2`, `d_m=3`, `d_o=2`, linear-Gaussian
kernels, and random invertible `R^b_1,R^b_2\in\mathrm{GL}(2)`, `R^m_1,R^m_2\in\mathrm{GL}(3)`,
simulated with common noise draws so that the two models are realized on one probability space:
the observation records agree **pathwise** to `9.9\mathrm{e}{-14}` over `4\times10^5` draws, while
the latents differ by up to `136.2` and satisfy `y'=Ry` to `6.8\mathrm{e}{-14}`; record means and
covariances agree to `1.2\mathrm{e}{-16}` and `1.1\mathrm{e}{-13}`. **Control**: omitting the
`R^{b-1}` factor in the observation kernel, that is violating `eq:gen-gauge-pushforward-obs` alone,
produces record discrepancies up to `192.9`. The hypothesis is load-bearing and the check can fail
(CHECK B1–B4).

*Two honesty notes belong with the proof.* First, `\omega_b` and `\omega_m` never appear in
`eq:gen-kernels` and are never used in the argument; the requirement `\omega'=(F^{-1})^\ast\omega`
in the definition of the equivalence is inert. Second, `hyp:gen-kernel-covariance` is a
`HYPOTHESIS`, imposed rather than derived (audit S4; `05b:66`, `06_gaussian.tex:297`). N3(a) is
therefore `ESTABLISHED` as an implication, and the strength of the noumenal reading equals the
strength of the covariance declaration, no more. The proof is not circular — composition along the
topological ordering and marginalization are genuine steps, and the existence of `\theta'` inside a
declared parameter family is a substantive closure requirement that the linear-Gaussian
realization witnesses — but the conclusion is a formal consequence of a declared symmetry.

## 2.3 B3 — the converse, sharply: the fiber is enormous

**Question.** Is `\Lambda` injective modulo the equivalence of §2.1? **No, and the failure is not
marginal.** `\Lambda` factors as

```
   Dat  --res_D-->  Dat_D  --Lambda_D-->  P( O_D ) ,                                   (B3.1)
```

where `\mathrm{res}_D` retains only the frame-expressed fiber values at the design points and the
generative parameter, and forgets everything else. Four nested layers sit inside the fibers of
`\mathrm{res}_D`, in increasing order of severity.

*(F1) The gauge orbit.* Theorem N3(a). This is the layer the project wants.

*(F2) The entire space of connections.* `\omega_b,\omega_m` are not arguments of any factor of
`eq:gen-kernels`, so `\Lambda(P,\omega,s,\theta)=\Lambda(P,\omega',s,\theta)` for **all** pairs of
connections, isomorphic or not. The fiber contains an affine space modeled on
`\Omega^1(\mathcal C,\mathrm{Ad}\,P)`, infinite-dimensional whenever `\dim\mathcal C\ge1` and
`\mathfrak g\ne0`. Holonomy conjugacy classes are therefore invisible to `\Lambda` for a trivial
reason, and no strengthening of N3(a) can be extracted from the connection sector.

*(F3) All sections agreeing on the design.* By `prop:prob-compatibility-nonidentifiability`(ii),
the fiber contains every section obtained by a bump deformation supported off `D`;
infinite-dimensional whenever `\mathcal C\setminus D` has nonempty interior and the fiber is
positive-dimensional.

*(F4) All principal `G`-bundles over `\mathcal C`.* Every principal bundle is trivializable over a
finite set, so `P\vert_D\cong D\times G` for every `P`. The generative kernels read only
frame-expressed coordinates at design points; hence for any two bundles `P,P'` over the same
`\mathcal C` with the same `G` there exist data with identical record laws. Explicit witness:
`\mathcal C=S^2`, `G=U(1)`, `P_n` the circle bundle with `c_1=n\in H^2(S^2;\Z)\cong\Z`. For
`n\ne n'` the bundles are non-isomorphic, yet the induced record laws coincide for every finite
design. **`\Lambda` does not separate Chern classes.**

*(F5) Ordinary statistical non-identifiability, on top of all of the above.* Even after quotienting
`\mathfrak{Dat}_D` by the passive product group of `def:gen-product-action`, `\Lambda_D` is not
injective: distinct `\theta` can induce the same observation marginal, as
`prop:gen-moving-target-witness` (`04:163`) already exhibits with `e(Q_\beta)=\log(1/2)` constant
across an injectively varying family.

**Statement of what the actual fiber is.** The record law is a function of the design-restricted,
frame-expressed, jet-zero data modulo the passive product group, and not an injective function even
of that. In particular the fiber over any record law contains the whole connection space, the whole
off-design section space, and every isomorphism class of principal `G`-bundle over `\mathcal C`.
**The noumenal claim delivered by N3(a) is therefore much stronger than gauge equivalence, and its
strength comes from the finiteness of the design rather than from any symmetry.**

## 2.4 B4 — what the theorem does and does not deliver

*It delivers a scope theorem, and that is genuinely useful.* Any future claim that some
observation-record statistic detects holonomy, curvature, or bundle topology is refuted in advance
for finite designs, by (F2) and (F4). This partially **closes in the negative** the ledger's
"Operational base holonomy (open)" entry (`appendix_claim_ledger.tex:242-256`): the requested tuple
— a named bundle and connection, an assigned base loop, a gauge-invariant population-record
statistic, and two data with distinct holonomy conjugacy classes and differing statistic laws —
**cannot exist for any finite design**, because the connection is not an argument of any generative
kernel. The open problem should be restated for refining or infinite designs, where it remains
genuinely open and where `open:prob-continuum-theory` (`03:443`) is the blocking obligation.

*It does not license "the substrate is inaccessible".* It licenses the much narrower "the declared
finite-design record-law map is constant on isomorphism classes, and in fact on a far larger set".
The reasons it holds are two features of the declared model, not two discoveries: the connection is
not an argument of any generative kernel, and every `G`-bundle is trivial over a finite set. Change
either and the theorem is unavailable. A reader who takes N3(a) as evidence that reality has an
inaccessible substrate has read a consequence of `03_probability.tex:15` as a consequence of the
world.

*It cuts against chapter 12, not for it.* `12_philosophy.tex:77` adopts an explicit idle-wheel
criterion: "a posit with no trace in any declared observable is removed by parsimony". N3(a) proves
that the bundle, the connection, and the off-design section values leave **no trace in any declared
observable**. Under the chapter's own criterion, proving N3(a) is an argument for removing the
bundle from the empirical content of the theory, not for calling it noumenal. This is the single
most important thing to say plainly, and the draft in §2.5 says it. The honest positive framing is
the one the theorem actually supports: the bundle is *organizational* structure whose role is to
make the covariance declaration statable and the frame bookkeeping consistent, and N3(a) is the
theorem that certifies the bookkeeping does not leak into the predictions.

*One further limit.* The theorem is conditional on `hyp:gen-kernel-covariance`, which the
manuscript declares rather than derives. Until audit finding S4 is addressed by a classification
theorem, N3(a) says: *if* the model was built covariant, *then* its records cannot see the frames.
That is worth proving and worth stating, and it is not the same as showing that covariance is
forced.

## 2.5 B5 — SPEC-compliant LaTeX, ready to paste

Intended home: `Theory/12_philosophy.tex`, replacing or following `sec:phil-noumenon`. Label
prefixes follow `SPEC.md` §4 and the `eq:phil-*` convention already used at `eq:phil-holonomy`.
Statuses: one visible tag per delimited claim, each claim in its own paragraph, no adjacent tags.
No bullets, no banned phrases, no spacing macros, American English.

```latex
\section{Record indistinguishability of isomorphic bundle data}
\label{sec:phil-record-indistinguishability}

The preceding section adopted an idle-wheel criterion and left open whether the
principal bundle leaves a trace in any declared observable.  This section
settles the question in one direction and states precisely how much less that
settles than the word ``noumenal'' suggests.  The argument uses no new
hypothesis: it assembles \Cref{hyp:gen-kernel-covariance} and
\Cref{prop:gen-product-evidence-invariance} over the design of
\Cref{def:prob-finite-design}.

\definitionheading{Bundle datum over a design}{def:phil-bundle-datum}
A \emph{bundle datum over the design $D$} is the tuple
\begin{equation}
\mathfrak D
=\bigl(P,\omega_b,\omega_m,(\mathcal C_i,u_i^b,u_i^m)_{i\in V},
(q_i,s_i)_{i\in V},\theta,X\bigr),
\label{eq:phil-bundle-datum}
\end{equation}
in which $\pi:P\to\mathcal C$ is the principal bundle of
\Cref{def:geo-principal-systems}, $\omega_b$ and $\omega_m$ are the connections
of \Cref{def:geo-connections}, the frames are those of
\eqref{eq:geo-frame-sections}, the sections are those of
\Cref{def:geo-agent}, and $(\theta,X)$ carry the generative data of
\Cref{def:prob-structural-kernel-signatures}.  Its \emph{record law} is the
observation marginal
\begin{equation}
\Lambda(\mathfrak D)
:=P_\theta\bigl(\cdot\times\mathsf Y_D\given X\bigr)
\in\mathcal P(\mathsf O_D,\mathscr O_D),
\label{eq:phil-record-law}
\end{equation}
and a \emph{record statistic} is any measurable map
$\Psi:(\mathsf O_D,\mathscr O_D)\to(S,\mathscr S)$.  Nothing is proved by these
declarations. \status{DEFINITION}

\definitionheading{Isomorphism of bundle data}{def:phil-datum-isomorphism}
Two bundle data are \emph{isomorphic} when there is a $G$-equivariant
diffeomorphism $F:P\to P'$ with $\pi'\circ F=\pi$, so that $F$ covers
$\operatorname{id}_{\mathcal C}$, such that
$\omega_x'=(F^{-1})^{*}\omega_x$ and $\mathcal C_i'=\mathcal C_i$ for each
channel and agent, such that the induced maps
$\bar F_x[u,\beta]=[F(u),\beta]$ on the associated bundles intertwine the
sections,
\begin{equation}
q_i'=\bar F_b\circ q_i,
\qquad
s_i'=\bar F_m\circ s_i,
\label{eq:phil-intertwined-sections}
\end{equation}
and such that $(\theta',X')$ is obtained from $(\theta,X)$ by
\Cref{hyp:gen-kernel-covariance} for the frame comparison that $F$ induces.
This is a declared equivalence and proves nothing on its own.
\status{DEFINITION}

\theoremheading{Isomorphic bundle data induce one record law}{thm:phil-record-indistinguishability}
Let $\mathfrak D$ and $\mathfrak D'$ be isomorphic in the sense of
\Cref{def:phil-datum-isomorphism}.  Then
\begin{equation}
\Lambda(\mathfrak D')=\Lambda(\mathfrak D)
\label{eq:phil-record-equality}
\end{equation}
as probability measures on $(\mathsf O_D,\mathscr O_D)$.  Consequently
$\Psi_{\#}\Lambda(\mathfrak D')=\Psi_{\#}\Lambda(\mathfrak D)$ for every record
statistic $\Psi$, no record statistic separates the two data, and
$p_{\theta'}(o\given X')=p_\theta(o\given X)$ for $\nu_D^O$-almost every $o$,
so the exact identity of \Cref{thm:elbo-exact-identity} holds with the same
evidence on both sides. \status{ESTABLISHED}

\paragraph{Proof.}
Write $\hat u_i^x:=F\circ u_i^x$.  Equivariance of $F$ and $\pi'\circ F=\pi$
make $\hat u_i^x$ a smooth local section of $P'$ over $\mathcal C_i$, so the
right $G$-torsor property of the fibers of $P'$ gives unique smooth maps
$g_i^x:\mathcal C_i\to G$ with $\hat u_i^x=u_i^{x\prime}\cdot g_i^x$; this is
the argument that produced \eqref{eq:geo-relative-frame}.  Evaluating at the
design points and representing gives
$R_{a,i}^x=\rho_x\bigl(g_i^x(c_a)\bigr)$, which are elements of the passive
product of \Cref{def:gen-product-action}.  If $\beta_i$ denotes the local
representative of $q_i$ in the frame $u_i^b$, then
\eqref{eq:phil-intertwined-sections} and the quotient convention
\eqref{eq:geo-quotient-convention} give
\begin{equation}
q_i'(c)=[F(u_i^b(c)),\beta_i(c)]
=[u_i^{b\prime}(c),\widehat\rho_b(g_i^b(c))\beta_i(c)],
\label{eq:phil-transported-coordinates}
\end{equation}
and identically in the model channel, so the whole difference between the two
data in their declared frames is the passive coordinate change by $R^b$ and
$R^m$.  \Cref{hyp:gen-kernel-covariance} holds for these representations by
assumption, so \Cref{prop:gen-product-evidence-invariance} gives
$P_{\theta'}(\cdot\given X')=T_{\#}P_\theta(\cdot\given X)$ with
$T(o,y)=(o,Ry)$.  Because $T$ is the identity in the observation coordinate,
the observation projection satisfies
$\operatorname{pr}\circ T=\operatorname{pr}$, whence
$\Lambda(\mathfrak D')=(\operatorname{pr}\circ T)_{\#}P_\theta
=\operatorname{pr}_{\#}P_\theta=\Lambda(\mathfrak D)$.  Pushing forward by a
measurable $\Psi$ preserves the equality, and the density statement is
\eqref{eq:gen-gauge-evidence-invariance}.
$\square$

The connections play no part in that proof.  They are not arguments of any
factor of \eqref{eq:gen-kernels}, so the requirement
$\omega_x'=(F^{-1})^{*}\omega_x$ in \Cref{def:phil-datum-isomorphism} is inert
and the following strengthening costs nothing. \status{ESTABLISHED}

\corollaryheading{The record law does not read the connection}{cor:phil-connection-blindness}
For any two principal connections $\omega,\omega'$ on the same $P$ and any
fixed remaining data, the induced record laws coincide.  The fiber of
$\Lambda$ through a bundle datum therefore contains an affine space modeled on
$\Omega^1(\mathcal C,\operatorname{Ad}P)$, which is infinite dimensional
whenever $\dim\mathcal C\geq1$ and $\mathfrak g\neq0$.
\status{ESTABLISHED}

\corollaryheading{No finite design reads bundle topology}{cor:phil-finite-design-topology}
Every principal $G$-bundle is trivializable over a finite subset of the base,
so $P\vert_D$ is trivial for every $P$ and every design.  Because the
generative kernels read only frame-expressed coordinates at design points,
for any two principal $G$-bundles over $\mathcal C$ there exist bundle data
with identical record laws.  A witness is $\mathcal C=S^2$ with $G=U(1)$ and
the circle bundles $P_n$ of first Chern class $n$: for $n\neq n'$ the bundles
are not isomorphic, while for every finite design the induced record laws
agree. \status{ESTABLISHED}

\propositionheading{The fiber of the record map is strictly larger than a gauge orbit}{prop:phil-record-fiber}
The record map factors through the design-restricted, frame-expressed values of
the sections together with $\theta$.  Its fibers contain the gauge orbit of
\Cref{thm:phil-record-indistinguishability}, the connection space of
\Cref{cor:phil-connection-blindness}, the bundle classes of
\Cref{cor:phil-finite-design-topology}, and every section that agrees with the
given one on $D$, the last by the deformation witness of
\Cref{prop:prob-compatibility-nonidentifiability}.  Even after quotienting by
the passive product of \Cref{def:gen-product-action} the induced map is not
injective, since \Cref{prop:gen-moving-target-witness} exhibits an injectively
varying family with constant evidence. \status{ESTABLISHED}

The reading these results support is narrower than the vocabulary of the
preceding section invites.  What is proved is that the declared finite-design
record law is constant on isomorphism classes of bundle data, and constant on a
much larger set besides; the reasons are that the connection is not an argument
of any generative kernel and that a finite design sees only finitely many
fibers.  Both are features of the declared model rather than conclusions about
what any inquiry could reach. \status{ESTABLISHED}

The manuscript does not claim that
\Cref{thm:phil-record-indistinguishability} shows any substrate to be
inaccessible in principle, and it does not claim that the theorem selects
between the two readings left open at the end of
\Cref{sec:phil-noumenon}. \status{NOT-CLAIMED}

Under the idle-wheel criterion declared at the start of
\Cref{sec:phil-noumenon}, these results argue for removing the bundle from the
empirical content of the theory rather than for calling it noumenal, since a
posit with no trace in any declared observable is removed by parsimony and
\Cref{cor:phil-connection-blindness} and \Cref{cor:phil-finite-design-topology}
prove there is no such trace at any finite design.  The role the bundle
retains is organizational: it is what makes the covariance declaration
\Cref{hyp:gen-kernel-covariance} statable and the frame bookkeeping of
\Cref{ch:geometry} consistent, and
\Cref{thm:phil-record-indistinguishability} is the theorem certifying that this
bookkeeping does not leak into the predictions. \status{DEFINITION}

\openproblemheading{Holonomy in a refining design}{open:phil-refining-holonomy}
The ledger entry on operational base holonomy asks for a named bundle and
connection, an assigned base loop, a gauge-invariant population-record
statistic, and two admissible connection data with distinct represented
holonomy conjugacy classes whose statistic laws differ.
\Cref{cor:phil-connection-blindness} shows that no such tuple exists for any
finite design, so the obligation is settled negatively in that regime and
should be restated for a refining family of designs.  Settling the restated
form requires the projective system, section-space topology, tightness, and
continuum reference measure listed at
\Cref{open:prob-continuum-theory}, together with a generative kernel that reads
the connection; the present typing of \eqref{eq:gen-kernels} supplies
none of these. \status{OPEN}
```

**Notes for the integrator.** `\Cref{cor:phil-finite-design-topology}` uses one standard fact —
every principal bundle over a finite discrete space is trivializable — which should carry a
citation to `Nakahara2003` or `Husemoller1994` if the latter is added to the bibliography. The
`\openproblemheading` paragraph should replace, not duplicate, the "Operational base holonomy
(open)" entry in `appendix_claim_ledger.tex:242-256`, whose finite-design half is now closed. Two
of the audit's citation gaps can be paid here at no cost: `Sengupta2016NeuronalGauge` belongs in
the opening paragraph as the direct precursor, and `vanFraassen1980` is already cited in the
chapter and should be the anchor for the idle-wheel paragraph.

---

# 3. What replaces the audit's fix list

The audit asked, at `S1`, for a functional satisfying (a) well-definedness under change of
trivialization, (b) `\mathrm{Aut}_G(P)`-invariance, and (c) consistency with `\Fenergy[Q_X]` on the
finite design. The findings above say (a) is achievable in complete generality, (b) is
unfulfillable as stated, and (c) is achievable but costs the connection. The repaired list is:

(a) unchanged, and now proved at the measurable tier — §1.2;
(b') **equivariance** of `\mathcal F_\mu[s;\pi,E]` under the simultaneous `\mathrm{Aut}_G(P)`
action on the triple, together with the orbit-space classification saying what an invariant
functional could have been — §1.3;
(c') the **exact** consistency identity `\Fenergy[Q_X;X,o]=\int f\,d\mu_D+\mathrm{TC}_D(Q_X)`,
which is a theorem replacing `hyp:prob-sampling-compatibility`, plus the unisolvence condition
under which the design identifies the section and which coincides with nondegeneracy of the
configuration Gram metric — §1.4;
(d') the two no-go theorems, A4.4 and A4.5, recorded as `ESTABLISHED` negative results, since they
explain why the gauge sector is inert and prevent the program from spending further effort trying
to un-inert it by adding terms;
(e') the successor task: `\omega`-parallel background sections, whose existence obstruction is
exactly the holonomy — §1.7.

---

# 4. Computations run

All in `/tmp/w2` on the sandbox, CPU only, `python3` with `numpy 2.2.6` and `sympy 1.14.0`.
No GPU or CUDA job was started or attempted.

| Script | What it checks | Result |
|---|---|---|
| `check1.py` | Theorem A4.1: `\Fenergy=\sum_a\Fenergy_a+\mathrm{TC}_D` in closed form for correlated Gaussian `Q` on `\R^6`, `M=3`, `K=2` | residual `1.42e-14`; `TC_D = 1.0235` |
| `check1.py` | same, `4\times10^6`-sample Monte Carlo cross-check | `121.9592 ± 0.0402` against exact `121.9906`, `0.78` s.e. |
| `check1.py` | **control**: design-product `Q` | `TC_D = 0.0` exactly; residual `1.42e-14` |
| `check2.py` | exact `S^1` Gram matrix, sympy integration | `\Phi=\mathrm{diag}(1,\tfrac12,\tfrac12)`, `\det=\tfrac14`, eigenvalues `\{1,\tfrac12\}` — matches `05d:327` |
| `check2.py` | Prop A4.3, unisolvence vs `\lambda_{\min}(\Phi)` | `M=3`: rank 3, `\Phi\succ0`; `M=2`: rank 2, `\lambda_{\min}=0` |
| `check2.py` | Prop A3.1/A3.2/Cor A3.4 | invariance fails (`1.9606` vs `2.9274`); equivariance residual `0.0`; transitivity witness `4.44e-16` |
| `check2.py` | (A2.1) on the tier | KL difference under simultaneous translation `-4.44e-16` |
| `check6.py` | A5 first variation `\delta\mathcal F[V]=\mathsf G(\mathrm{grad}\mathcal F,V)` | `1.35e-9` at FD step `1e-6` |
| `check6.py` | A5 flow: `\Vert\mathrm{grad}\mathcal F(m^\ast)\Vert_\infty`, convergence at `T=20`, rate | `1.55e-15`; `1.03e-13`; rate `1.861 = \lambda_{\min}(I+\Sigma_0\Sigma_o^{-1})` |
| `check6.py` | **control**: minimizer equals exact contextwise Gaussian posterior mean | `4.44e-16` |
| `check6.py` | Theorem A4.4(a) deformation witness | `\chi\vert_D=(0,0,0)`, `\chi'\vert_D=(8,-4,8)` |
| Fisher check | Fact T1: pushforward by invertible sample map preserves `g^F` (mean-only and full Gaussian) | `2.89e-15` and `5.33e-14` |
| Fisher check | **control**: rank-deficient sample map | discrepancy `1.3087`, control fires |
| orbit check | Cor A3.5: `r^2=\mu^\top\Sigma^{-1}\mu` invariant under `\mathrm{GL}^+(4)`; completeness by explicit `A^\ast` | `1.29e-13`; residuals `4.4e-16`, `4.4e-15`; `\det A^\ast=+0.419`, `\det Q=+1.0` |
| `checkB2.py` | Theorem N3(a): records pathwise identical under `R`, `4\times10^5` draws | `9.95e-14` |
| `checkB2.py` | latents genuinely move: `\Vert y'-y\Vert=136.24` but `\Vert y'-Ry\Vert` | `6.84e-14` |
| `checkB2.py` | record-law moments | mean `1.25e-16`, covariance `1.14e-13` |
| `checkB2.py` | **control**: violate `eq:gen-gauge-pushforward-obs` only | discrepancy `192.94`, control fires |

Computation is not proof. Every claim above that is tagged as a theorem carries a proof in the
text; the numbers are consistency checks with controls, run to catch sign and convention errors,
and they did catch two during development (a transposition in the natural-gradient formula and a
right-versus-left action error in the fixed-point solve, both corrected before the results above).
