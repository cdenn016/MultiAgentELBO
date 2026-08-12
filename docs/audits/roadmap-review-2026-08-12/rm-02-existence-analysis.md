# Referee report — analysis program of `2026-08-12-pifb2-continuum-roadmap.md`

**Scope.** T1, T3, T4, T6, T8, T9 of the theorem roadmap, and the WP1 exit gate
("at least two nonisomorphic statistical families instantiate the hypotheses").
Verdict format: each finding is ranked **[TRUTH]** (the statement as written is false or
ill-posed), **[PROVABILITY]** (true, but not by the stated method / needs added hypotheses),
or **[DIFFICULTY]** (true and provable, but expensive).

All curvature numbers below were computed here with sympy/numpy, not quoted. Scripts and
raw output are reproduced in §A.

---

## 0. Headline verdicts

**V1 — T4's weak lower semicontinuity is FINE, and the suspected obstruction is a false
alarm.** The reduced functional after T3's row elimination contains
$\Phi_\tau(D)=-\tau\log\sum_j\pi_{ij}e^{-D_{ij}/\tau}$, which is indeed **concave** in the
divergence vector. Concavity is *not* a wlsc hazard here, because $\Phi_\tau$ is also
**strictly increasing in each argument** and its argument $D$ depends on the sections
*pointwise* (order zero), so Rellich–Kondrachov upgrades weak $H^1$ convergence to a.e.
convergence and the composition (nondecreasing continuous) ∘ (lsc) is lsc; Fatou then
closes it, since $\Phi_\tau\ge 0$. Convexity is required only in the *gradient* slot, and
there the integrand $\xi^\top g^{\mathrm F}(q)\xi$ is quadratic and positive semidefinite,
so Ioffe's theorem applies. Proof in §4. **Do not spend effort relaxing the attention
sector.** What *is* missing are three unstated hypotheses (bounded **Lipschitz** $U_i$ —
"measurable" is not enough for Rellich; a **closed/proper** isometric embedding of the
fiber; a **fixed** connection or $d\le 3$ with bounded fiber).

**V2 — The curvature-sign finding is real but it bites T6, not T4.** Computed here:

| Family | Fisher–Rao model | Sectional curvature | Complete? | Bounded? |
|---|---|---|---|---|
| Categorical $\Delta_{n-1}$ | open positive orthant of the round sphere $S^{n-1}(2)$ via $p\mapsto 2\sqrt p$ | $\equiv +1/4$ (constant, verified $n=3,4$) | **No** (boundary at finite distance) | Yes, diam $=\pi$ |
| Univariate Gaussian | hyperbolic plane | $\equiv -1/2$ (constant) | Yes | No |
| **Multivariate Gaussian** $n\ge 2$ | homogeneous space of $\mathrm{Aff}(n)$ | **MIXED SIGN**: exactly $+1/4$ on *every* pure-mean 2-plane at *every* point (verified symbolically, $n=2$; numerically $n=3,4$); $[-1,0]$ on pure-covariance planes; global range $\approx[-1,+2/7]$ at $\Sigma=I$, $n=2$ | Yes (homogeneous) | No |

So the roadmap's two showcase families differ in curvature *sign*, in *completeness*, and
in *boundedness*. The audit's "+1/4 pure-mean sectional curvature" claim in PIFB2 is
**confirmed exactly**, and it is stronger than reported: $+1/4$ holds on every pure-mean
plane at every point, for every $n\ge2$, and $\sup K$ is strictly larger ($=2/7$ for
$n=2$, attained on a mixed mean/covariance plane; exact rational values $434/1521$ and
$41/144$ verified symbolically). The multivariate Gaussian is therefore **not NPC** and
**not a space form**, consistent with Skovgaard (1984).

**But**: the direct method is *curvature-blind*. Existence of energy minimizers in
$H^1(M,N)$ holds for **any** compact $N$ regardless of curvature (Morrey 1948). One proof
does cover both families for T4. The curvature-sign split kills **T6** — Eells–Sampson
requires $\mathrm{Riem}_N\le 0$ and applies to *exactly one* of the roadmap's showcase
families, the univariate Gaussian, i.e. the trivial one — and it degrades **full
regularity** in $d\ge3$ to a "regular ball" hypothesis.

**V3 — WP1's exit gate does fail, but for a different reason than curvature: coercivity
and completeness.** For the **categorical** fiber everything works: $2\sqrt p$ turns the
Dirichlet term into a *flat* Dirichlet energy into a compact, geodesically convex, closed
subset of a sphere — perfect coercivity and a weakly closed constraint set. For the
**Gaussian** fiber, the Fisher metric *degenerates* in the mean directions as
$\Sigma\to\infty$ ($g_{\mu\mu}=\Sigma^{-1}\to 0$), so a bounded action does **not** bound
$\|\nabla\mu\|_{L^2}$, and the divergence terms only grow like $\log\det\Sigma$ — far too
slowly to compensate. **The Gaussian fiber does not satisfy T1/T4's "coercive confinement"
hypothesis under the action as written.** [TRUTH-level for the exit gate.]

**V4 — The sharpest structural finding: gauge-invariant coercive confinement is
impossible whenever the gauge orbits in the fiber are noncompact.** See the Lemma in §3.
This means the roadmap's own declared failure condition (line 170, "if coercivity destroys
the intended ontology") is *triggered* by the current $\mathrm{GL}(K)$ / affine
realization, and that WP1's decision to assume **compact $G$** is not a convenience — it
is the *only* thing that makes the coercivity hypothesis compatible with T2.

**V5 — T4 as stated is false in the presence of a dynamical connection.** $\kappa\|F_A\|^2$
is gauge invariant, hence constant on gauge orbits, which are noncompact; $\|F_A\|_{L^2}$
does not control $\|A\|_{H^1}$ without gauge fixing. Even after Uhlenbeck gauge fixing,
Sedláček's theorem in $d=4$ produces a minimizer **on a possibly different bundle**. In
$d\ge5$ the Yang–Mills term is supercritical and there is no theory. [TRUTH]

---

## 1. How much of T4 is classical

### 1.1 Classical and directly citable

The Dirichlet sector $\eta_q\int\|D^Aq\|^2_{g^{\mathrm F}_q}$ is exactly the *vertical
energy* of a section of an associated bundle. The relevant frameworks:

* **Harmonic maps, existence of minimizers.** C. B. Morrey, *The problem of Plateau on a
  Riemannian manifold*, Ann. of Math. **49** (1948) 807–851. With $N$ compact and
  isometrically embedded in $\mathbb R^m$ (Nash), $H^1(M,N)=\{u\in H^1(M,\mathbb R^m):
  u(x)\in N\text{ a.e.}\}$ is weakly closed, the energy is convex in $\nabla u$, and the
  direct method gives a minimizer in any prescribed boundary class. **No curvature
  hypothesis.** This is a one-paragraph proof in any modern text (Lin–Wang, *The Analysis
  of Harmonic Maps and Their Heat Flows*, 2008; Simon, *Theorems on Regularity and
  Singularity of Energy Minimizing Maps*, 1996; Hélein, *Harmonic Maps, Conservation Laws
  and Moving Frames*, 2002).
* **Harmonic sections of fibre bundles.** C. M. Wood, *Harmonic sections of homogeneous
  fibre bundles*, Diff. Geom. Appl. **19** (2003) 193–210 — the bundle-valued version, with
  the vertical tension field as Euler–Lagrange operator. Also the Eells–Lemaire reports
  (Bull. LMS 1978, 1988) for the general variational framework.
* **Regularity.** R. Schoen & K. Uhlenbeck, *A regularity theory for harmonic maps*, JDG
  **17** (1982) 307–335: energy minimizers into compact $N$ are smooth off a closed
  singular set of Hausdorff dimension $\le d-3$. Full regularity for $d=2$ (Morrey 1948);
  full regularity for weakly harmonic maps from surfaces (Hélein 1991; Rivière, Invent.
  Math. **168** (2007) 1–22).
* **Small-image full regularity.** S. Hildebrandt, H. Kaul, K.-O. Widman, *An existence
  theorem for harmonic mappings of Riemannian manifolds*, Acta Math. **138** (1977) 1–16:
  if the image lies in a *regular ball* $B_R(p)$ with $R<\min(\mathrm{inj}\,N,
  \pi/(2\sqrt{\kappa}))$, $\kappa=\sup K_N$, the minimizer is smooth in any dimension.
* **Yang–Mills.** K. Uhlenbeck, *Connections with $L^p$ bounds on curvature*, CMP **83**
  (1982) 31–42, and *Removable singularities in Yang–Mills fields*, CMP **83** (1982)
  11–29; S. Sedláček, *A direct method for minimizing the Yang–Mills functional over
  4-manifolds*, CMP **86** (1982) 515–527.

**Bottom line:** with $A$ *fixed and smooth*, with a compact (or properly embedded closed)
fiber, and with the non-Dirichlet terms nonnegative and lsc, **T4 is essentially a
citation, not a theorem.** The roadmap should say so; claiming it as new invites a hostile
referee.

### 1.2 What is genuinely NOT covered

1. **The lower-order sector.** $D_q(q_i\|p_i)$, $\beta_{ij}D_q(q_i\|L_{ij}q_j)$ and the
   entropic attention term are not part of any harmonic-map theorem. For *existence* they
   are harmless (§4). For *regularity* they are not: the Euler–Lagrange system acquires a
   right-hand side $\nabla_q D$ that **blows up at the admissible boundary** (for the
   simplex, $\partial_{q_k}\mathrm{KL}=\log(q_k/p_k)+1\to-\infty$ as $q_k\to0$). Standard
   harmonic-map-with-RHS regularity assumes an $L^p$ or Morrey-bounded RHS. This is genuine
   new work, not covered.
2. **Two coupled sections in one integrand.** $D(q_i\|L_{ij}q_j)$ is a *bi-section* term
   over $U_i\cap U_j$. Harmonic-map theory is single-map. For wlsc this is fine (§4); for
   the Euler–Lagrange system and for any Uhlenbeck-type $\varepsilon$-regularity it means
   the monotonicity formula and the small-energy regularity theorem must be redone for a
   *coupled* system.
3. **Statistical target.** Two specifically statistical features have no analogue in the
   harmonic-map literature: (a) the target metric is the *same* object that appears in the
   Dirichlet term and in the divergence, so the "target geometry" and the "potential" are
   not independent data; (b) the natural admissible sets are open, with the divergence
   $\equiv+\infty$ on the boundary — an *extended-real* target functional, not the standard
   setting. The classical fix is the theory of *obstacle problems for harmonic maps*
   (Duzaar–Fuchs, Duzaar–Steffen), which is available but weaker.
4. **Gauged nonlinear target.** Yang–Mills–Higgs theory assumes a **linear** representation
   fiber. A gauged $\sigma$-model with a general nonlinear fiber is only well developed in
   $d=2$ with Kähler targets (Mundet i Riera, J. Reine Angew. Math. **528** (2000) 41–80;
   Cieliebak–Gaio–Salamon, IMRN 2000). For general statistical-manifold fibers in
   $d\ge3$ this is open.
5. **The dynamical connection.** §5.3.

---

## 2. The curvature computation, and what it does and does not threaten

### 2.1 Categorical / multinomial

$g^{\mathrm F}=\sum_i dp_i^2/p_i$; setting $x_i=2\sqrt{p_i}$ gives $dx_i=dp_i/\sqrt{p_i}$,
so $\sum dx_i^2=g^{\mathrm F}$ and $\sum x_i^2=4$. Hence

> **$(\Delta_{n-1}, g^{\mathrm F})$ is isometric to the open positive orthant of the round
> sphere of radius $2$**, so $K\equiv +1/4$, constant, for all $n$.

Verified symbolically for $n=3$ (Gaussian curvature $=1/4$) and $n=4$ (all five test
2-planes give exactly $1/4$).

Consequences, all computed:

* **Not complete.** $\partial\Delta$ is at finite distance ($d(p,q)=2\arccos\sum\sqrt{p_iq_i}$).
  The metric completion is the *closed* spherical simplex: **compact, geodesically convex**
  (intersection of the sphere with a convex cone; any two nonnegative unit vectors subtend
  an angle $\le\pi/2$, so the whole set lies in a closed hemisphere), a **manifold with
  corners**, diameter exactly $\pi$.
* **HKW threshold is exactly saturated by the diameter.** $\kappa=1/4\Rightarrow
  \pi/(2\sqrt\kappa)=\pi$. Vertex-to-vertex distance $=2\arccos 0=\pi$. But the *circumradius*
  about the uniform distribution is $2\arccos(1/\sqrt n)<\pi$, so **HKW applies for every
  finite alphabet** — with a constant that degenerates:

  | $n$ | 2 | 3 | 4 | 8 | 64 | $10^3$ | $10^5$ |
  |---|---|---|---|---|---|---|---|
  | circumradius $/\pi$ | 0.500 | 0.608 | 0.667 | 0.770 | 0.920 | 0.980 | 0.998 |

  **Any full-regularity theorem for categorical fibers is non-uniform in the alphabet
  size.** [DIFFICULTY, but it must appear in the theorem statement.]
* **Contractible.** $\pi_1=\pi_2=0$, so (i) **no bubbling** (harmonic-sphere bubbles need
  $\pi_2(N)\ne0$; Sacks–Uhlenbeck, Ann. of Math. **113** (1981) 1–24), and (ii) **Bethuel's
  density obstruction does not fire** (§5).
* **Convex-hull property.** Because the closed simplex is geodesically convex and sits in a
  regular ball, a minimizer with boundary data in the interior maps into the geodesic
  convex hull of that data (Jost/HKW convex-hull property), hence the obstacle constraint
  at $\partial\Delta$ is *inactive* and the minimizer is a genuine smooth harmonic
  section. **This is the clean positive result for the categorical fiber and should be
  stated as such.**

### 2.2 Gaussian

Fisher metric $ds^2=d\mu^\top\Sigma^{-1}d\mu+\tfrac12\mathrm{tr}(\Sigma^{-1}d\Sigma\Sigma^{-1}d\Sigma)$.

* **Univariate.** Computed symbolically: $K\equiv-1/2$. (Poincaré half-plane rescaled;
  Atkinson–Mitchell, Sankhyā A **43** (1981) 345–365.) Complete, Hadamard, NPC.
* **Multivariate, $n\ge2$.** Computed symbolically ($n=2$, full 5-dimensional Riemann
  tensor) and numerically with validated 4th-order finite differences ($n=2,3,4$):

  * $K(\partial_{\mu_a},\partial_{\mu_b}) = +1/4$ **exactly, at every $(\mu,\Sigma)$, for
    every $n\ge2$** (symbolic result for general $\Sigma$; numerical at $\Sigma=I$ for
    $n=3,4$ to 8 digits).
  * Pure-covariance 2-planes: $K\in[-1,0]$, nonpositive (the SPD affine-invariant sector,
    which is NPC; the slice $\{\mu=\text{const}\}$ is totally geodesic, being the fixed set
    of the isometry $x\mapsto 2\mu_0-x$).
  * Mixed planes interpolate and can exceed $1/4$: exact symbolic values $434/1521\approx
    0.28534$ and $41/144\approx0.28472$; numerical optimum $\sup K = 2/7 \approx 0.285714$
    for $n=2$ (min $=-1$).
  * **Why the mean plane is positively curved even though $\{\Sigma=\text{const}\}$ is
    intrinsically flat:** that slice is *not* totally geodesic, and the Gauss equation
    $K_M=K_N-\langle\mathrm{II}(X,X),\mathrm{II}(Y,Y)\rangle+\|\mathrm{II}(X,Y)\|^2$
    supplies the $+1/4$. This reproduces the reviewer's Gauss-equation verification in the
    PIFB2 audit.
  * Complete (homogeneous under $\mathrm{Aff}(n)=\mathrm{GL}(n)\ltimes\mathbb R^n$, hence
    complete by Hopf–Rinow), noncompact, unbounded, contractible, **not NPC, not a space
    form**. Consistent with L. T. Skovgaard, *A Riemannian geometry of the multivariate
    normal model*, Scand. J. Statist. **11** (1984) 211–223.

### 2.3 Where curvature bites — precise, non-overstated

| Question | Curvature-sensitive? | Verdict for the roadmap |
|---|---|---|
| **T4 existence of minimizers (direct method)** | **NO** | Morrey's argument is curvature-blind. One proof covers both families. **Curvature does not threaten T4.** |
| **Bubbling / attainment in a homotopy class** | Yes, via $\pi_2(N)$, not via $K$ | Both fibers contractible ⇒ **no bubbling**. Non-issue here. |
| **Full interior regularity, $d\ge3$** | **YES** | HKW needs image in a ball of radius $<\pi/(2\sqrt{\sup K})$. Simplex: threshold $\pi$, satisfied but non-uniform in $n$. Multivariate Gaussian: $\sup K=2/7$ ⇒ threshold $\pi\sqrt7/(2\sqrt2)\approx2.94$, but the manifold is unbounded so the hypothesis must be *earned*, not assumed. Without it: partial regularity only (Schoen–Uhlenbeck). |
| **Uniqueness in a class; convexity of energy** | **YES** | Hartman (Canad. J. Math. **19** (1967) 673–687) and Al'ber need $\mathrm{Riem}_N\le0$. Fails for the simplex and for the multivariate Gaussian. **No uniqueness should be claimed.** |
| **T6 global existence of the flow (Eells–Sampson)** | **YES, decisively** | Eells–Sampson (Amer. J. Math. **86** (1964) 109–160) requires $\mathrm{Riem}_N\le0$. Applies to **only** the univariate Gaussian. §6. |

**Honest statement of the consequence for WP1's exit gate.** The two showcase families
*can* be covered by a single T4, because the direct method is insensitive to curvature.
They *cannot* be covered by a single T6, and they *cannot* be covered by a single
regularity theorem. The exit gate does fail — but the operative difference is
**completeness/boundedness and coercivity** (§3), not curvature.

---

## 3. Coercivity vs. the intended ontology

### 3.1 Categorical fiber

KL blow-up is **not** a symmetric coercivity mechanism. $\mathrm{KL}(q\|p)=\sum q\log(q/p)$
is $+\infty$ only when $p_k\to0$ with $q_k>0$; if $q_k\to0$ with $p_k>0$ it stays finite
(indeed $\mathrm{KL}(\cdot\|p)\le\log(1/\min_kp_k)$ is *bounded* on the whole closed
simplex). So:

> **The pointwise term $D_q(q_i\|p_i)$ confines the model section $p_i$ away from
> $\partial\Delta$, and does nothing whatsoever to confine the belief section $q_i$.**

This asymmetry is not noted in the roadmap and it matters: $q_i$ may reach the simplex
boundary at finite cost, where the peer terms $D(q_i\|L q_j)$ are also finite but where
$g^{\mathrm F}$ is singular and the Euler–Lagrange RHS blows up.

The *actual* coercivity mechanism for the categorical fiber is not KL at all — it is
**compactness of the closed target**. The change of variable $x=2\sqrt p$ makes
$\eta_q\int\|D^Aq\|^2_{g^{\mathrm F}}$ literally $\eta_q\int|D^Ax|^2$ with $x$ valued in a
compact convex subset of $S^{n-1}(2)$. Then $H^1$ bounds, weak compactness, and closedness
of the constraint set are immediate. Interaction with wlsc is clean (§4). **Recommendation:
state the categorical case in the $2\sqrt p$ chart; it converts the whole analysis into
textbook harmonic-map theory.**

### 3.2 Gaussian fiber

What confines what:

* $\Sigma_1\to0$ (first argument): $\mathrm{KL}\sim\tfrac12\log\det\Sigma_2/\det\Sigma_1\to+\infty$. ✔ but only **logarithmically**.
* $\Sigma_1\to\infty$: $\tfrac12\mathrm{tr}(\Sigma_2^{-1}\Sigma_1)\to\infty$, linearly. ✔
* $\Sigma_2\to0$: $\mathrm{tr}(\Sigma_2^{-1}\Sigma_1)\to\infty$. ✔
* $\|\mu_1-\mu_2\|\to\infty$: quadratic. ✔
* **$\mu_1=\mu_2\to\infty$ and $\Sigma_1=\Sigma_2\to\infty$ together: KL $\equiv0$.** ✘

That last line is the crux. **KL is coercive only in the *difference* of its arguments.**
The action is invariant (or nearly so) under simultaneously moving *all* sections by the
same fiber isometry, and $\mathrm{Aff}(n)$ acts transitively with noncompact orbits.
Minimizing sequences can therefore escape to infinity at zero cost.

Compounding this: **the Dirichlet term degenerates in the same limit.** $g^{\mathrm
F}_{\mu\mu}=\Sigma^{-1}\to0$, so $\int(\nabla\mu)^\top\Sigma^{-1}\nabla\mu<\infty$ gives no
$L^2$ bound on $\nabla\mu$ when $\Sigma$ is large. The only term growing with $\Sigma$ is
$\log\det\Sigma$, which cannot produce an $L^\infty$ bound. **Conclusion: T1/T4's "compact
target or coercive confinement" hypothesis is NOT satisfied by the Gaussian fiber under the
action as written.** [TRUTH-level for WP1's exit gate.]

### 3.3 The crux: does confinement break gauge covariance? — **Yes, unless $G$ is compact.**

> **Lemma (gauge-invariant confinement).** Let $\rho:G\to\mathrm{Diff}(\mathcal M)$ and
> $E=P\times_\rho\mathcal M$. A function $V:\mathcal M\to\mathbb R$ induces a well-defined
> (gauge-invariant) function on $E$ **iff** $V$ is $\rho(G)$-invariant.
> (a) If some orbit $\rho(G)\cdot m$ is **noncompact**, then no $\rho(G)$-invariant $V$ has
> compact sublevel sets: $V$ is constant on that orbit, so every sublevel set meeting it
> contains it. **Hence no gauge-invariant coercive confinement exists.**
> (b) If $G$ is **compact**, all orbits are compact, and for any coercive $W$ the Haar
> average $V(m)=\int_G W(\rho(g)m)\,dg$ is $\rho(G)$-invariant and coercive. **Hence
> gauge-invariant coercive confinement exists.**

Consequences, stated bluntly:

* Anchoring at a fixed fiber point $m_0\in\mathcal M_q$ (e.g. a penalty $d(q,m_0)^2$) is
  **not** gauge invariant; it breaks $G$ down to the isotropy subgroup $G_{m_0}$. In physics
  language this is a **Higgs potential**, and choosing a confinement point is an explicit
  (or spontaneous) breaking of the gauge group to the stabiliser of the vacuum. The roadmap
  should say this in exactly those words; it already has the vocabulary ("frame-smoothness
  term is gauge fixing"), and confinement belongs in the same ledger.
* For the **current MAgent realization** — $\mathrm{GL}(K)$ frames, Gaussian fibers,
  $\mathrm{Aff}(n)$-type action with noncompact orbits — case (a) applies. **T2 and T4's
  coercivity hypothesis are mutually incompatible in the existing backend.** The
  roadmap's own line-170 failure condition ("if coercivity destroys the intended ontology,
  the action class must be revised") is thereby *triggered*, not hypothetical. [TRUTH]
* **WP1's assumption of compact $G$ is therefore load-bearing, not a convenience.** This
  should be promoted from a remark ("that makes quotient and existence arguments
  controllable") to a stated necessity, with the Lemma as justification. It also gives a
  second, independent reason for compact $G$ at T9 (§8: finite Haar measure).

**Constructive alternatives, with costs.**

| Fix | What it buys | Cost |
|---|---|---|
| **Compact $G$** (Haar-averaged invariant potential) | Genuine gauge-invariant coercivity | Excludes $\mathrm{GL}(K)$ and $\mathrm{Aff}(n)$ from the abstract layer; the existing code becomes a *non-conforming* backend, not "one backend" |
| **Based gauge group**: fix Dirichlet data on $\partial\mathcal C$ and restrict to $g|_{\partial\mathcal C}=\mathrm{id}$ | Standard in gauge theory; kills the flat noncompact directions | Requires $\partial\mathcal C\ne\emptyset$ (or a marked point); residual symmetry is only the based gauge group; T2 must be restated for it |
| **Quotient**: minimize on $\Gamma(E)\times\mathcal A/\mathcal G$ | Existence *modulo* symmetry | Orbit space is not a manifold (reducible connections ⇒ orbifold points); needs a slice theorem; the minimizer exists in the quotient, possibly not upstairs |
| **Concentration-compactness** (Lions) modulo the $\mathrm{Aff}(n)$ action | Existence after translation | Only works if the loss of compactness is exactly the symmetry; the "dichotomy" alternative must be excluded, which is real work |
| **Restrict the admissible $\Sigma$-window** to $\epsilon I\preceq\Sigma\preceq RI$ | Compact target, everything trivial | Directly destroys the intended ontology (beliefs of unbounded/vanishing uncertainty excluded); must be declared as a modelling assumption |

---

## 4. Weak lower semicontinuity — worked out

**Setting.** $U_i\subset\mathcal C$ bounded with **Lipschitz** boundary (this is required,
not optional — see below). $N=\mathcal M_q$ **properly** isometrically embedded as a
**closed** subset of $\mathbb R^m$ (Nash + properness). Sections identified locally with
$u_i\in H^1(U_i,\mathbb R^m)$, $u_i(c)\in N$ a.e. Connection $A$ **fixed and smooth** for
this proposition (the dynamical case is §5.3). Hypotheses:

* (H1) $D:N\times N\to[0,+\infty]$ is lsc, $\ge0$, finite and continuous on the admissible interior.
* (H2) $L^q_{ij}$ continuous fibrewise.
* (H3) $g^{\mathrm F}:N\to\mathrm{Sym}^+$ continuous, positive semidefinite (may blow up).
* (H4) $\pi^q_{ij}>0$, $\tau_q>0$, $\chi,\chi_{ij}\ge0$ measurable and bounded.

> **Proposition.** Under (H1)–(H4) the reduced functional $\mathcal S_{\mathrm{red}}$
> obtained by pointwise elimination of $\beta,\gamma$ is well defined, measurable, bounded
> below by $0$, and **sequentially weakly lower semicontinuous** on $\{u\in H^1: u\in N
> \text{ a.e.}\}$ with the weak $H^1$ topology.

**Proof, term by term.**

**(a) Row elimination is legitimate (this is T3, and T3 is true).** For a.e. $c$, the map
$\beta\mapsto\langle\beta,D\rangle+\tau\sum_j\beta_j\log(\beta_j/\pi_j)$ is **strictly
convex** on the simplex (the entropy is strictly convex, the linear part is affine), so the
minimizer is unique: $\beta^\ast_j=\pi_je^{-D_j/\tau}/Z$, $Z=\sum_j\pi_je^{-D_j/\tau}$, with
value $\Phi_\tau(D)=-\tau\log Z$. Measurability of $c\mapsto\beta^\ast(c)$ is immediate from
the closed formula. The **interchange of the pointwise minimum with the integral** is the
one nontrivial step and follows from the theory of normal integrands: Rockafellar–Wets,
*Variational Analysis*, Thm. 14.60. The envelope derivative $\partial\Phi_\tau/\partial
D_j=\beta^\ast_j$ is Danskin's theorem (differentiability because the argmin is unique).
**T3 is correct as stated; cite Rockafellar–Wets rather than hand-waving "measurable
dependence".** [PROVABILITY, minor.]

**(b) Properties of $\Phi_\tau$ that actually matter.**
* $\Phi_\tau$ is $C^\infty$ on $[0,\infty)^n$ and extends continuously to $[0,+\infty]^n$;
* $\partial\Phi_\tau/\partial D_j=\beta^\ast_j\in(0,1)$: **strictly increasing in each argument**;
* $\Phi_\tau$ is **concave** in $D$ ($\log\sum\pi e^{-D/\tau}$ is convex in $D$);
* $0\le\Phi_\tau(D)\le\min_j\big(D_j+\tau\log(1/\pi_j)\big)$ — since $Z\le1$ gives the lower bound and $Z\ge\pi_je^{-D_j/\tau}$ the upper.

**(c) The concavity is a red herring.** Take $u^n\rightharpoonup u$ in $H^1$. Since $U_i$ is
bounded Lipschitz, **Rellich–Kondrachov** gives $u^n\to u$ in $L^2$ and, on a subsequence,
**a.e.** Hence $D^n_{ij}(c):=D(u^n_i(c)\|L_{ij}u^n_j(c))$ satisfies $\liminf_n D^n_{ij}(c)\ge
D_{ij}(c)$ a.e. by (H1)+(H2). Because $\Phi_\tau$ is **continuous and nondecreasing** in
each argument, the composition of a nondecreasing continuous function with an lsc function
is lsc:
$$\liminf_n \Phi_\tau\big(D^n(c)\big)\ \ge\ \Phi_\tau\big(D(c)\big)\quad\text{a.e.}$$
and since $\Phi_\tau\ge0$, **Fatou** yields $\liminf_n\int\Phi_\tau(D^n)\ge\int\Phi_\tau(D)$. ∎

> **The concavity would be fatal only if $D$ converged *merely weakly*.** It does not: $D$ is
> an order-zero (pointwise) function of the sections, and the compact embedding
> $H^1\hookrightarrow\hookrightarrow L^2$ upgrades weak to strong to a.e. Convexity is needed
> only in the *gradient* slot. **T4 does not need relaxation on account of T3.** [Non-finding,
> recorded so it is not re-litigated.]

**(d) Pointwise divergence terms.** Same argument, one step shorter. Note in particular that
**joint convexity of KL is not needed** — only nonnegativity and lsc. This is worth stating
because it means the theorem survives replacing KL by any nonnegative lsc divergence
($\alpha$-divergences, Rényi, Bregman), which is what the roadmap's "initially KL" wants.

**(e) Dirichlet term.** $F(u,\xi)=\xi^\top g^{\mathrm F}(u)\xi$ is a normal integrand,
$\ge0$, continuous in $u$ on the admissible set, and **convex (quadratic PSD) in $\xi$** —
exactly the hypothesis of A. D. Ioffe, *On lower semicontinuity of integral functionals I*,
SIAM J. Control Optim. **15** (1977) 521–538 (see also Buttazzo, *Semicontinuity, Relaxation
and Integral Representation*, 1989). wlsc holds under $u^n\to u$ in $L^1$, $\nabla u^n
\rightharpoonup\nabla u$ in $L^1$. ✔ Blow-up of $g^{\mathrm F}$ at $\partial\Delta$ is
harmless for lsc (it only makes the integrand larger). **Degeneracy** of $g^{\mathrm F}$
(Gaussian, $\Sigma\to\infty$) is also harmless for lsc — it destroys **coercivity**, not
wlsc (§3.2). Keep the two properties separate; the roadmap currently conflates them under
"positive covariant spatial terms".

**(f) Constraint.** $\{u:u(c)\in N\text{ a.e.}\}$ is closed under a.e. convergence iff $N$
is **closed in $\mathbb R^m$**. For the simplex this is automatic (compact). For the
Gaussian family, a **proper** isometric embedding must be exhibited — Nash gives an
isometric embedding; properness (closed image) is an extra requirement that the roadmap
must discharge. [PROVABILITY.]

### 4.1 A real consequence of doing T3 honestly — the peer sector is a soft-**min**

From (b): $\Phi_\tau(D)\le\min_j\big(D_{ij}+\tau\log(1/\pi^q_{ij})\big)$, and
$\Phi_\tau\to\min_jD_{ij}$ as $\tau\to0$. So after row elimination **the peer sector asks
agent $i$ to agree with its single best-matching neighbour, not with its neighbourhood.**
Worse: if the diagonal $j=i$ is in the row with $L_{ii}=\mathrm{id}$ (so $D_{ii}=0$, and
$U_i\cap U_i=U_i$ makes it available in the roadmap's $\sum_{i,j}$), then $Z\ge\pi^q_{ii}$
and
$$\mathcal S_{\text{peer}}\ \le\ \tau_q\log(1/\pi^q_{ii})\cdot\mu(U_i),$$
**uniformly bounded**: the entire peer sector can be violated at bounded cost, contributes
**zero coercivity**, and cannot enforce consensus at all. This is a *modelling* finding, not
an analysis obstruction, but it is exactly the kind of thing WP1 should surface before WP6
tries to distinguish the theory from "generic consensus optimization". **Recommendation:
exclude the diagonal from the attention row explicitly, and state the coercivity budget of
the peer sector as $O(\tau\log(1/\pi_{\min}))$, i.e. negligible.** [DIFFICULTY / modelling.]

---

## 5. The $H^1$ / dimension issue

### 5.1 What is true per dimension

| $d$ | Function space | Existence (matter sector, $A$ fixed) | Regularity |
|---|---|---|---|
| **1** | $H^1\subset C^{0,1/2}$ | Trivial | Smooth |
| **2** | critical; $H^1\subset\mathrm{VMO}$, not $C^0$; smooth maps **dense** (Schoen–Uhlenbeck, JDG **18** (1983) 253–268) | ✔ | **Full** interior regularity of minimizers (Morrey 1948); weakly harmonic maps from surfaces smooth (Hélein 1991; Rivière 2007) |
| **3, 4** | smooth maps dense **iff $\pi_2(N)=0$** (Bethuel, Acta Math. **167** (1991) 153–206) | ✔ | **Partial only**: $\dim_{\mathcal H}\mathrm{sing}\le d-3$ (Schoen–Uhlenbeck 1982). Canonical counterexample $x/|x|:B^3\to S^2$ is minimizing (Brezis–Coron–Lieb, CMP **107** (1986) 649–705; Lin 1987) |
| **$\ge5$** | as above | ✔ for the matter sector | Partial only; YM sector has no theory |

### 5.2 The roadmap gets lucky on density and bubbling

Bethuel's obstruction and Sacks–Uhlenbeck bubbling both turn on $\pi_2(N)$. **Both showcase
fibers are contractible** — $\Delta_{n-1}$ is convex, and $\mathbb R^n\times\mathrm{SPD}(n)$
is convex-in-coordinates — so $\pi_2=0$ and:

* $C^\infty(M,N)$ **is** dense in $H^1(M,N)$ in every dimension;
* there are **no bubbles**, so the infimum over sections is attained;
* the space of sections of $E_q\to\mathcal C$ is nonempty and connected (contractible
  fibers ⇒ global sections exist, all homotopic), so T4 has no topological content on the
  matter side.

This is a genuine and quotable robustness property of **exponential-family fibers**: they
are contractible because their natural parameter domains are convex. **State it explicitly
in the manuscript** — it converts a scary-looking hypothesis into a triviality and it will
be the first thing a referee checks.

### 5.3 The dimension constraint comes from the *gauge* sector, not the matter sector

With $A$ dynamical:

* $F_A=dA+A\wedge A$ is quadratic in $A$: to pass to the limit in $A\wedge A$ one needs
  $A^n\to A$ strongly in $L^4$. $H^1\hookrightarrow\hookrightarrow L^4$ **compactly for
  $d\le3$**, continuously but not compactly at $d=4$, and not at all for $d\ge5$.
* $\|F_A\|_{L^2}$ does **not** bound $\|A\|_{H^1}$: the functional is constant on
  noncompact gauge orbits. One needs **Uhlenbeck gauge fixing** (CMP **83** (1982) 31–42),
  which requires smallness of $\|F\|_{L^{d/2}}$ on small balls — controlled by
  $\|F\|_{L^2}$ **only when $d\le4$**.
* Even in $d=4$, Sedláček's direct method (CMP **86** (1982) 515–527) yields a Yang–Mills
  minimizer **possibly on a different bundle** — energy can bubble off and change the
  topological type. So *"there exists a minimizer in the given principal bundle $P$"* is
  **not** what the classical theorem gives.
* The covariant derivative $D^Aq=dq+\rho_*(A)q$ couples the two sectors multiplicatively.
  For $d\le3$ with a **bounded** fiber (categorical) this is fine: $A^n\to A$ in $L^2$ and
  $q^n$ bounded a.e. give $\rho_*(A^n)q^n\to\rho_*(A)q$ in $L^2$, so the integrand is
  convex in $\nabla q$ plus a strongly convergent perturbation. For an **unbounded** fiber
  (Gaussian) $q\notin L^\infty$ and the product needs Hölder control that the action does
  not supply.

> **Recommended honest statement of T4.**
> *(i) $d\le3$, compact $G$, categorical (or compact-target) fiber, $A$ dynamical:* provable,
> with Uhlenbeck gauge fixing. Full interior regularity via HKW.
> *(ii) $d=4$:* provable only in Sedláček's weakened form (minimizer in a possibly different
> bundle); partial regularity.
> *(iii) $d\ge5$:* **do not claim**. State T4 for the matter sector with a **fixed smooth
> connection** and record the dynamical-$A$ case as open (cf. Tian, Ann. of Math. **151**
> (2000) 193–268, for what "stationary" replaces "minimizing" with).
> *(iv) Gaussian fiber, any $d$:* not provable under the action as written (§3.2); needs an
> amended action.

---

## 6. T6 — what the dissipation identity must actually say

$d\mathcal S/dt=-\|\mathrm{grad}\,\mathcal S\|^2\le0$ is a **tautology** once a gradient
flow is declared, as the prompt notes. The content must be:

**(a) Is the "integrated product Fisher metric" a Riemannian metric on section space?**
It is an $L^2$-type metric on $\Gamma(E)$, hence a **weak** Riemannian metric: the topology
it induces is strictly weaker than the manifold topology, the Riesz isomorphism
$T\Gamma\to T^\ast\Gamma$ is not surjective, and the space is **not complete**. Two
consequences the roadmap should absorb:

* **Vanishing geodesic distance.** P. Michor & D. Mumford, *Vanishing geodesic distance on
  spaces of submanifolds and diffeomorphisms*, Doc. Math. **10** (2005) 217–245: $L^2$-type
  metrics on infinite-dimensional mapping/shape spaces can have **identically zero**
  geodesic distance. Any statement about "distance in configuration space" under this metric
  must be checked, not assumed.
* **$\mathrm{grad}\,\mathcal S$ is only densely defined.** Because $\mathcal S$ contains
  $\int\|D^Aq\|^2$, its differential is $H^{-1}$-valued; the $L^2$-Riesz representer exists
  only on a dense domain. So "gradient flow on a Riemannian manifold" is a *metaphor*; the
  object is a **semilinear degenerate parabolic system**. The rigorous alternative is a
  metric-space gradient flow (curve of maximal slope, Ambrosio–Gigli–Savaré), which is
  available but (i) yields only energy-dissipation-inequality solutions, and (ii) the good
  theory needs $\lambda$-convexity along generalized geodesics, which **fails** for the
  positively curved fibers.

**(b) Global existence is not "separate", it is largely FALSE.**

* Harmonic-map heat flow with $\mathrm{Riem}_N\le0$: global existence + convergence
  (Eells–Sampson 1964). **Applies only to the univariate Gaussian.**
* $d=2$, positively curved targets: finite-time blow-up (Chang–Ding–Ye, JDG **36** (1992)
  507–515); global weak solutions with finitely many singularities (Struwe, Comment. Math.
  Helv. **60** (1985) 558–581).
* $d\ge3$: finite-time blow-up (Coron–Ghidaglia 1989); global weak solutions with partial
  regularity (Chen–Struwe, Math. Z. **201** (1989) 83–103).
* Yang–Mills heat flow: only **weakly parabolic** (gauge degeneracy) — DeTurck/Donaldson
  gauge fixing is mandatory. Global existence $d\le3$ (Råde, J. Reine Angew. Math. **431**
  (1992) 123–163); $d=4$ global weak with finitely many singularities (Struwe, Calc. Var.
  PDE **2** (1994) 123–150); **finite-time blow-up known for $d\ge5$** (Naito; Grotowski;
  Gastel).

**Constructive fix, and it is a good one.** For positively curved but *small-image* targets,
global existence and convergence do hold: if the flow's image stays in a **regular ball**,
the standard convexity of $d^2(\cdot,p)$ plus the maximum principle give global existence
and subconvergence (HKW 1977 circle of ideas; Hamilton, *Harmonic Maps of Manifolds with
Boundary*, LNM 471, 1975; Jost, *Riemannian Geometry and Geometric Analysis*). **T6 should
be stated as: global existence *conditional on an a priori regular-ball estimate*, and that
estimate should be proved from the divergence terms.** Cost: the estimate is real work and
may fail.

**(c) The replicator obstruction — specific to the categorical fiber.** The Fisher-natural
gradient on the simplex is the Shahshahani/replicator field. Its faces $\{p_k=0\}$ are
**invariant**: support can be lost but never regained, and the mobility $ (g^{\mathrm
F})^{-1}\to0$ at $\partial\Delta$ makes the boundary sticky. So the flow can converge to a
configuration on which the divergence terms are $+\infty$ — i.e. **the $\omega$-limit of the
dissipative flow need not lie in the admissible set of T1/T4.** This is a concrete way in
which T6 and T4 fail to be about the same object, and it deserves an explicit statement.
[TRUTH-level for the "flow converges to a minimizer" narrative.]

---

## 7. T8 — is $\Gamma$-convergence the right tool?

**Yes, but it is useless alone.** The *fundamental theorem of $\Gamma$-convergence*
(De Giorgi–Franzoni; Dal Maso, *An Introduction to $\Gamma$-Convergence*, 1993, Thm 7.8;
Braides, *$\Gamma$-convergence for Beginners*, 2002) gives convergence of minima and of
minimizers **only when paired with equi-coercivity**. The roadmap's T8 row correctly says
"consistency plus compactness", so the shape is right; the substance is missing.

**What must be supplied.**

1. **A common topology.** Discrete configurations live on nodes/edges; continuum sections on
   $\mathcal C$. One needs an interpolation/embedding operator. **Piecewise-linear
   interpolation does not work** — linear combinations of fiber points leave the fiber. The
   correct machinery is:
   * **Geodesic finite elements** — O. Sander, *Geodesic finite elements of higher order*,
     IMA J. Numer. Anal. **36** (2016) 238–266; P. Grohs, H. Hardering, O. Sander,
     *Optimal a priori discretization error bounds for geodesic finite elements*, Found.
     Comput. Math. **15** (2015) 1357–1411; H. Hardering, *$L^2$-discretization error bounds
     for maps into Riemannian manifolds*, Numer. Math. (2017/18).
   * **Projection-based finite elements** — Grohs–Hardering–Sander–Sprecher, SIAM J. Numer.
     Anal. **57** (2019) 1478–1495.
   These give **optimal a priori $H^1$ and $L^2$ error bounds for discretizations of
   harmonic maps into smooth manifolds** — precisely T8's matter-sector target, and the
   single most useful citation in this section. Caveat: they are *local* statements near a
   smooth, stable continuum solution, not a global $\Gamma$-limit. For the categorical fiber
   the projection is the nearest-point retraction onto the spherical simplex — explicit and
   well conditioned away from the corners.
2. **Equi-coercivity uniform in the mesh.** Everything in §3 must hold with constants
   independent of $h$. For the gauge sector this needs a **discrete Uhlenbeck gauge-fixing
   theorem**. To my knowledge no such theorem exists in the generality required.
3. **Closedness of the target under the interpolation.** Geodesic/projection FE preserve the
   fiber by construction. ✔

**Known discrete-to-continuum $\Gamma$-convergence results, and the warning they carry.**

* R. Alicandro & M. Cicalese, *A general integral representation result for continuum limits
  of discrete energies with superlinear growth*, SIAM J. Math. Anal. **36** (2004) 1–37.
* R. Alicandro, M. Cicalese, A. Gloria, *Integral representation results for energies defined
  on stochastic lattices and application to nonlinear elasticity*, ARMA **200** (2011)
  881–943; and *Variational description of bulk energies for bounded and unbounded spin
  systems*, Nonlinearity **21** (2008).
* R. Alicandro, M. Cicalese, M. Ponsiglione, *Variational equivalence between Ginzburg–Landau,
  XY spin systems and screw dislocations energies*, Indiana Univ. Math. J. **60** (2011)
  171–208; Alicandro–Cicalese, *Variational analysis of the asymptotics of the XY model*,
  ARMA **192** (2009).

> **Warning these results carry.** For $S^1$- or $S^2$-valued spins the $\Gamma$-limit at
> the natural scaling is **not** the Dirichlet energy: vortex/defect energies appear at
> logarithmic scalings, and the limit functional acquires terms with no continuum-action
> counterpart.

For the **matter sector** this danger is defused: both showcase fibers are contractible, so
$\pi_1=\pi_2=0$ and no topological defects can form. For the **gauge sector** it is fully
live: $\pi_1(G)\ne0$ for most compact $G$ ($\pi_1(U(1))=\mathbb Z$, $\pi_1(SO(3))=\mathbb
Z/2$), so lattice-gauge configurations genuinely carry defects and one should *expect*
defect terms in any honest $\Gamma$-limit.

**Lattice gauge theory continuum limits are as hard as advertised.** Rigorous results exist
only in special situations: $d=2$ Yang–Mills measure constructed (Driver; Sengupta; Lévy),
recently shown universal across Wilson/Villain/Manton actions; $U(1)_4$ lattice → continuum
(Driver, CMP 1987); non-Abelian YM$_4$ with a mass gap is a **Clay Millennium Problem**
(Jaffe–Witten). Note these are *probabilistic* scaling limits, a different (harder) question
from the deterministic variational one, but the deterministic side is not better served: the
plaquette expansion $U_p=\exp(a^2F+O(a^3))$ gives **pointwise consistency on smooth
connections** trivially, and that is *not* $\Gamma$-convergence — the $\Gamma$-liminf and the
compactness for non-smooth sequences are the entire difficulty.

> **Recommended scope for T8.** Split it. **T8a:** fix a smooth connection; prove
> geodesic-FE / projection-FE convergence with rates for the matter sector, citing
> Grohs–Hardering–Sander. This is achievable and publishable. **T8b:** gauge sector —
> prove *consistency only* (pointwise convergence of the lattice action on smooth
> configurations) and state explicitly that no $\Gamma$-convergence or compactness result is
> claimed. Merging the two into one row of the roadmap misrepresents a Millennium-adjacent
> problem as a work package. [TRUTH-level for the row as written.]

---

## 8. T9 — badly under-scoped, and ill-typed for $d\ge2$

The proposal is a Gibbs measure $e^{-\mathcal S}$ on a configuration space of sections with
$0<Z<\infty$. This is not a technical loose end; it is a **Euclidean field theory
construction** of a nonlinear $\sigma$-model coupled to a gauge field.

**The type error.** Any reference measure for which $\int\|D^Aq\|^2$ is the quadratic form
is a Gaussian free field. The GFF in dimension $d$ lives in $H^{1-d/2-\epsilon}$ and is
**a.s. not in $H^1$**; for $d\ge2$ it is **not function-valued** at all. So under any such
measure the statement "$q(c)\in\mathcal M_q$ pointwise" is meaningless, and the
configuration space carrying the measure is *not* the configuration space on which
$\mathcal S$ is defined. **The $\mathcal S$-finite configurations form a null set.** This is
the fundamental obstruction and it is not repairable by choosing a nicer $\mathcal S$.

**Dimension by dimension.**

* $d=1$: fine. Wiener measure / Brownian motion on $\mathcal M$; $Z<\infty$ for compact
  $\mathcal M$. Genuinely provable.
* $d=2$: $\sigma$-models are perturbatively renormalizable and (for $K>0$ targets)
  asymptotically free; **rigorous construction is open in general**. 2D Yang–Mills *is*
  constructed (Driver, Sengupta, Lévy).
* $d=3$: the $\sigma$-model coupling has mass dimension $2-d<0$, i.e. **perturbatively
  non-renormalizable**. Compare $\varphi^4_3$, which required Glimm–Jaffe-level work and is
  a *much* easier (linear-target) problem. No construction known.
* $d=4$: $\varphi^4_4$ is **trivial** (Aizenman 1981; Fröhlich 1982; Aizenman–Duminil-Copin,
  Ann. of Math. **194** (2021) 163–235). Non-Abelian YM$_4$ is a Clay Millennium Problem.

**Even at fixed mesh, $Z<\infty$ needs compact $G$.** The integral runs over the gauge orbit;
for noncompact $G$ (e.g. $\mathrm{GL}(K)$) the gauge volume is infinite and $Z=+\infty$
unless one gauge-fixes with a Faddeev–Popov determinant. For compact $G$, Haar is a
probability measure and the finite-mesh statement is elementary. **This is the third
independent argument for compact $G$** (cf. §3.3, §5.3).

> **Honest status.** Split T9. **T9a (finite mesh):** elementary; $0<Z<\infty$ follows from
> coercivity + compact $G$ + a reference product measure. Worth one page; it is what the
> code can actually realize. **T9b (continuum, $d\ge2$):** **open**, in part
> Millennium-level. It should be **removed from the theorem table**, not listed as
> "optional" — "optional" implies it is achievable at will, which is the single most
> misleading line in the roadmap. [TRUTH]

---

## 9. Ranked findings

### Threaten the TRUTH of a stated theorem

| # | Finding | Where | Fix / cost |
|---|---|---|---|
| **T-1** | **T4 is false as stated with a dynamical connection.** Gauge orbits are noncompact; $\|F_A\|_{L^2}$ gives no $H^1$ bound. In $d=4$ the best classical result (Sedláček) yields a minimizer on a *possibly different* bundle; $d\ge5$ has no theory. | T4, §5.3 | Fix $A$ smooth (matter sector only) — cheap, but abandons the gauge dynamics; or restrict to $d\le3$ + Uhlenbeck gauge fixing — real work; or weaken the conclusion to "in some bundle". |
| **T-2** | **The Gaussian fiber does not satisfy the coercivity hypothesis.** $g^{\mathrm F}_{\mu\mu}=\Sigma^{-1}\to0$ so the action does not bound $\|\nabla\mu\|_{L^2}$; KL grows only like $\log\det\Sigma$; KL is coercive only in the *difference* of its arguments. **WP1's exit gate fails on the Gaussian side.** | T1, T4, WP1, §3.2 | Add a confining potential (see T-3); or bound the admissible $\Sigma$-window (destroys the ontology); or replace $g^{\mathrm F}$ in the Dirichlet term by a complete auxiliary metric (changes the theory). |
| **T-3** | **Gauge-invariant coercive confinement is impossible when the fiber gauge orbits are noncompact** (Lemma §3.3). Anchoring at a fixed fiber point is a Higgs potential and breaks $G\to G_{m_0}$. The existing $\mathrm{GL}(K)$/affine backend hits exactly this. The roadmap's own line-170 failure condition is triggered. | T2 vs T4, §3.3 | **Compact $G$** (Haar-averaged invariant potential exists) — but this excludes the current backend from the abstract layer; or the **based gauge group** with boundary data; or quotient/concentration-compactness. |
| **T-4** | **T6's global existence is largely false, not merely deferred.** Eells–Sampson needs $\mathrm{Riem}_N\le0$ and applies to *exactly one* showcase family (univariate Gaussian, $K\equiv-1/2$). $K\equiv+1/4$ (categorical) and $\sup K=2/7>0$ (multivariate Gaussian) put both other cases outside it; blow-up is known in $d=2$ (Chang–Ding–Ye) and $d\ge3$ (Coron–Ghidaglia), and for YM flow in $d\ge5$. | T6, §2, §6 | State T6 as *conditional* global existence under an a priori regular-ball estimate (HKW/Hamilton/Jost circle); prove that estimate. Cost: real work, may fail. |
| **T-5** | **T9 is ill-typed for $d\ge2$**: no reference measure charges $H^1$, so "sections" is the wrong configuration space; $d=3$ non-renormalizable, $d=4$ trivial/Millennium. Also $Z=\infty$ at finite mesh for noncompact $G$. | T9, §8 | Split into a provable finite-mesh statement and an explicitly open continuum statement. Remove "optional". |
| **T-6** | **The categorical flow's $\omega$-limit can leave the admissible set.** Fisher-natural gradient on the simplex is the replicator field; faces are invariant and the mobility vanishes there, so the flow can converge to configurations where the divergences are $+\infty$. T4 and T6 are then not about the same object. | T4 vs T6, §6(c) | Prove a strict-interior a priori bound, or state T6 on the closed simplex with the extended-real functional and accept boundary limits. |

### Threaten PROVABILITY AS STATED (true, but the stated route is incomplete)

| # | Finding | Fix / cost |
|---|---|---|
| **P-1** | "Measurable or Lipschitz domain $U_i$" — **Lipschitz and bounded is mandatory**, since the whole wlsc argument runs on Rellich–Kondrachov. | Free: tighten the hypothesis. |
| **P-2** | The direct method needs a **closed (proper)** isometric embedding of the fiber, not just an isometric one. Automatic for the simplex; must be constructed for $\mathbb R^n\times\mathrm{SPD}(n)$. | Standard but must be discharged. |
| **P-3** | T3's min/integral interchange is a measurable-selection statement; cite Rockafellar–Wets Thm 14.60 and Danskin, don't assert. T3 is otherwise correct and easy. | Free. |
| **P-4** | T5 assumes "sufficient regularity for smooth variations" — in $d\ge3$ that is **exactly what is not available** (partial regularity only). The first variation is valid distributionally / off the singular set. | Restate T5 for weak/stationary solutions; add HKW hypotheses if smooth variations are wanted. |
| **P-5** | The Euler–Lagrange RHS $\nabla_qD$ **blows up at the admissible boundary**, so harmonic-map-with-RHS regularity does not apply off the shelf. | Genuine new work, or an a priori interior bound. |
| **P-6** | T8 needs equi-coercivity, a manifold-valued interpolation operator, and (gauge sector) a discrete Uhlenbeck gauge-fixing theorem that does not exist. | Split T8a/T8b as in §7. |
| **P-7** | The "integrated product Fisher metric" is a **weak** metric with possibly vanishing geodesic distance (Michor–Mumford) and $\mathrm{grad}\,\mathcal S$ only densely defined. "Gradient flow on a Riemannian manifold" is not literally correct. | Reframe as a parabolic system, or as a metric-space gradient flow (weaker solution concept; $\lambda$-convexity fails under positive curvature). |
| **P-8** | Full regularity for the categorical fiber via HKW has a constant $2\arccos(1/\sqrt n)\uparrow\pi$: **non-uniform in the alphabet size**. | State the $n$-dependence in the theorem; do not claim a uniform constant. |

### DIFFICULTY only (or non-findings, recorded so they are not re-litigated)

| # | Finding |
|---|---|
| **D-1** | **The wlsc worry about $-\tau\log Z$ is a non-finding.** Concavity is irrelevant because $\Phi_\tau$ is nondecreasing and its argument converges a.e. (Rellich), not weakly. Proof in §4. Do not relax T4 on this account. |
| **D-2** | **Both showcase fibers are contractible**, so Bethuel's density obstruction and Sacks–Uhlenbeck bubbling both fail to fire. This is a robustness property of exponential-family fibers (convex parameter domains) and should be stated as a lemma — it is the first thing a referee will probe. |
| **D-3** | The categorical case becomes textbook in the chart $x=2\sqrt p$: flat Dirichlet energy into a compact geodesically convex subset of $S^{n-1}(2)$, plus a convex-hull argument that makes the boundary obstacle inactive. **Write the categorical case in this chart.** |
| **D-4** | wlsc of the divergence terms needs only nonnegativity and lsc, **not** joint convexity of KL — so the theorem survives replacing KL by $\alpha$-/Rényi/Bregman divergences, which the roadmap wants. |
| **D-5** | After T3, the peer sector is a soft-**min**, bounded above by $\min_jD_{ij}+\tau\log(1/\pi_{ij})$; with a diagonal entry it is **uniformly bounded**, contributing zero coercivity and no consensus pressure. Modelling consequence; exclude the diagonal and re-budget coercivity. |
| **D-6** | The multivariate Gaussian is **not** a space form and not NPC; its Fisher–Rao distance has no closed form, which will complicate any numerical oracle built on geodesic distance (E0/E6). |

---

## 10. Recommended restatement of the WP1 milestone

Split T4 into two theorems that are honestly different:

> **T4a (compact-fiber, fixed-connection).** Let $\mathcal C$ be a compact $d$-manifold with
> smooth positive density; $U_i\subset\mathcal C$ bounded Lipschitz; $G$ compact; $A$ a fixed
> smooth connection; $\mathcal M_q,\mathcal M_s$ regular statistical manifolds whose closures
> are compact and properly embedded, with $g^{\mathrm F}$ continuous and positive definite on
> the admissible set and $D$ nonnegative, lsc, extended-real. Then $\mathcal S_{\mathrm{red}}$
> is wlsc and coercive on $\prod_iH^1(U_i,\overline{\mathcal M})$ and attains its minimum
> subject to the declared boundary data. **Instantiated by the categorical fiber.** For
> $d\ge3$, minimizers are partially regular; if the boundary data lie in a compact
> geodesically convex subset of the open simplex, minimizers are smooth (HKW), with a
> constant degenerating as $n\to\infty$.

> **T4b (noncompact fiber).** Same, with "compact closure" replaced by a **gauge-invariant
> coercive confinement potential $V$**. By the Lemma of §3.3, such a $V$ exists iff the fiber
> gauge orbits are compact; for compact $G$ it can be constructed by Haar averaging. **The
> Gaussian fiber requires such a $V$ to be added to the action** — the action as written does
> not confine $(\mu,\Sigma)$, and its Dirichlet term degenerates as $\Sigma\to\infty$.

Then WP1's exit gate is met honestly: two nonisomorphic families instantiate the hypotheses,
but **by different theorems and with an explicit amendment to the action in the Gaussian
case**. Claiming a single theorem for both, with the current action, is the one thing that
should not survive review.

---

## A. Computations

Environment: CPU only, sympy 1.14.0 + numpy. No GPU/CUDA used.

**A.1 Categorical simplex (exact, sympy).** Metric $g_{ij}=\delta_{ij}/p_i+1/p_n$ on the
simplex in the first $n-1$ coordinates; full Christoffel/Riemann computation.
```
n=3 outcomes (2-dim simplex):  Gaussian curvature K = 1/4
n=4 outcomes (3-dim simplex):  K = 1/4  on all five tested 2-planes
                               (coordinate planes and two generic planes)
```

**A.2 Univariate Gaussian (exact, sympy).** $g=\mathrm{diag}(1/\sigma^2,2/\sigma^2)$:
```
K = -1/2   (constant)
```

**A.3 Bivariate Gaussian (exact, sympy).** 5-dimensional, coordinates $(m_1,m_2,a,b,c)$ with
$\Sigma=\left(\begin{smallmatrix}a&b\\b&c\end{smallmatrix}\right)$; full Riemann tensor. At
$\mu=0,\Sigma=I$:
```
K(d_m1, d_m2) = 1/4      K(d_m1, d_a) = -1/2     K(d_m1, d_b) = -1/4
K(d_m1, d_c)  = 0        K(d_m2, d_a) =  0       K(d_m2, d_b) = -1/4
K(d_m2, d_c)  = -1/2     K(d_a,  d_b) = -1/2     K(d_a,  d_c) =  0
K(d_b,  d_c)  = -1/2
PURE-MEAN plane at GENERAL (mu, Sigma):  K = 1/4   (exact, position-independent)
mixed planes (exact rationals):  434/1521 = 0.285339 ,  41/144 = 0.284722   (> 1/4)
```

**A.4 Multivariate Gaussian $n=1..4$ (numerical, 4th-order central differences of $g$,
$h=10^{-3}$; validated against A.2/A.3 to 6–8 digits).**
```
n=1  dim=2   ALL 2-planes: [-0.500000, -0.500000]
n=2  dim=5   K(pure-mean)=+0.250000  ALL: [-0.976611, +0.279789]
             pure-MEAN: [+0.250000,+0.250000]   pure-COV: [-1.000000, 0.000000]
n=3  dim=9   K(pure-mean)=+0.250000  ALL: [-0.860509, +0.258988]
             pure-MEAN: [+0.250000,+0.250000]   pure-COV: [-0.987937,-0.000592]
n=4  dim=14  K(pure-mean)=+0.250000  ALL: [-0.691095, +0.167435]
             pure-MEAN: [+0.250000,+0.250000]   pure-COV: [-0.887543,-0.003955]
Nelder-Mead refinement, n=2:  sup K = +0.28571429 (= 2/7),  inf K = -1.00000000
```
(The `ALL`-row ranges are random scans and under-report the extremes for larger $n$; the
refined $n=2$ values and the exact rationals in A.3 are the authoritative ones. The
pure-mean value $+1/4$ is exact and position-independent by homogeneity.)

**A.5 Simplex geometry vs. the HKW threshold.**
```
kappa = 1/4  =>  HKW regular-ball threshold  pi/(2 sqrt kappa) = pi = 3.141593
circumradius about the uniform distribution = 2 arccos(1/sqrt n):
  n=2    1.570796  (0.500 pi)      n=8      2.418858  (0.770 pi)
  n=3    1.910633  (0.608 pi)      n=64     2.890937  (0.920 pi)
  n=4    2.094395  (0.667 pi)      n=1024   3.079082  (0.980 pi)
                                   n=1e5    3.135268  (0.998 pi)
diameter of the closed simplex (vertex to vertex) = 2 arccos(0) = pi  (== threshold)
```

---

## B. References

Reference details below are given from standard knowledge and should be checked against the
originals before they enter a manuscript.

Aizenman, M. (1981), *Proof of the triviality of $\varphi^4_d$ field theory*, CMP 86, 1–48 ·
Aizenman, M. & Duminil-Copin, H. (2021), *Marginal triviality of the scaling limits of
critical 4D Ising and $\varphi^4_4$ models*, Ann. of Math. 194, 163–235 ·
Alicandro, R. & Cicalese, M. (2004), SIAM J. Math. Anal. 36, 1–37 ·
Alicandro, R., Cicalese, M. & Gloria, A. (2011), ARMA 200, 881–943 ·
Alicandro, R., Cicalese, M. & Ponsiglione, M. (2011), Indiana Univ. Math. J. 60, 171–208 ·
Ambrosio, L., Gigli, N. & Savaré, G. (2008), *Gradient Flows in Metric Spaces* ·
Amari, S. & Nagaoka, H. (2000), *Methods of Information Geometry* ·
Atkinson, C. & Mitchell, A. F. S. (1981), Sankhyā A 43, 345–365 ·
Bethuel, F. (1991), Acta Math. 167, 153–206 ·
Braides, A. (2002), *$\Gamma$-convergence for Beginners* ·
Brezis, H., Coron, J.-M. & Lieb, E. (1986), CMP 107, 649–705 ·
Buttazzo, G. (1989), *Semicontinuity, Relaxation and Integral Representation* ·
Calvo, M. & Oller, J. M. (1990), J. Multivariate Anal. 35, 223–242 ·
Chang, K.-C., Ding, W.-Y. & Ye, R. (1992), JDG 36, 507–515 ·
Chen, Y. & Struwe, M. (1989), Math. Z. 201, 83–103 ·
Cieliebak, K., Gaio, A. R. & Salamon, D. (2000), IMRN ·
Coron, J.-M. & Ghidaglia, J.-M. (1989), C. R. Acad. Sci. Paris 308, 339–344 ·
Dal Maso, G. (1993), *An Introduction to $\Gamma$-Convergence* ·
Driver, B. (1987/1989), CMP ·
Duzaar, F. & Fuchs, M., obstacle problems for harmonic maps ·
Eells, J. & Lemaire, L. (1978, 1988), *(Two) Report(s) on Harmonic Maps*, Bull. LMS ·
Eells, J. & Sampson, J. H. (1964), Amer. J. Math. 86, 109–160 ·
Glimm, J. & Jaffe, A. (1987), *Quantum Physics* ·
Grohs, P., Hardering, H. & Sander, O. (2015), Found. Comput. Math. 15, 1357–1411 ·
Grohs, P., Hardering, H., Sander, O. & Sprecher, M. (2019), SIAM J. Numer. Anal. 57, 1478–1495 ·
Hamilton, R. (1975), *Harmonic Maps of Manifolds with Boundary*, LNM 471 ·
Hardering, H. (2017/18), Numer. Math. ·
Hartman, P. (1967), Canad. J. Math. 19, 673–687 ·
Hélein, F. (2002), *Harmonic Maps, Conservation Laws and Moving Frames* ·
Hildebrandt, S., Kaul, H. & Widman, K.-O. (1977), Acta Math. 138, 1–16 ·
Ioffe, A. D. (1977), SIAM J. Control Optim. 15, 521–538 ·
Jaffe, A. & Witten, E., *Quantum Yang–Mills Theory* (Clay Millennium Problem description) ·
Jost, J., *Riemannian Geometry and Geometric Analysis* ·
Lévy, T. (2003), Mem. AMS ·
Lin, F.-H. & Wang, C. (2008), *The Analysis of Harmonic Maps and Their Heat Flows* ·
Michor, P. & Mumford, D. (2005), Doc. Math. 10, 217–245 ·
Morrey, C. B. (1948), Ann. of Math. 49, 807–851 ·
Mundet i Riera, I. (2000), J. Reine Angew. Math. 528, 41–80 ·
Nash, J. (1956), Ann. of Math. 63, 20–63 ·
Råde, J. (1992), J. Reine Angew. Math. 431, 123–163 ·
Rivière, T. (2007), Invent. Math. 168, 1–22 ·
Rockafellar, R. T. & Wets, R. J.-B. (1998), *Variational Analysis* ·
Sacks, J. & Uhlenbeck, K. (1981), Ann. of Math. 113, 1–24 ·
Sander, O. (2016), IMA J. Numer. Anal. 36, 238–266 ·
Schoen, R. & Uhlenbeck, K. (1982), JDG 17, 307–335; (1983), JDG 18, 253–268 ·
Sedláček, S. (1982), CMP 86, 515–527 ·
Sengupta, A. (1997), Mem. AMS ·
Shahshahani, S. (1979), Mem. AMS 211 ·
Simon, L. (1996), *Theorems on Regularity and Singularity of Energy Minimizing Maps* ·
Skovgaard, L. T. (1984), Scand. J. Statist. 11, 211–223 ·
Struwe, M. (1985), Comment. Math. Helv. 60, 558–581; (1994), Calc. Var. PDE 2, 123–150 ·
Tian, G. (2000), Ann. of Math. 151, 193–268 ·
Uhlenbeck, K. (1982), CMP 83, 31–42 and CMP 83, 11–29 ·
Wood, C. M. (2003), Diff. Geom. Appl. 19, 193–210.
