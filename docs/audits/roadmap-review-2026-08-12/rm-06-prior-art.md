# RM-06 — Prior-art referee report on the PIFB2 continuum roadmap

**Document under review:** `docs/research-plans/2026-08-12-pifb2-continuum-roadmap.md`
**Date:** 2026-08-12
**Method note:** the arXiv API (`export.arxiv.org/api/query`) is **blocked from the sandbox** — `curl` returns
HTTP 403 `Connection blocked by network allowlist` over http and connection failure over https. All
retrievals below were done with WebSearch plus direct `arxiv.org/abs/...` fetches, which do work. Every
citation in this report was actually retrieved, not recalled.

---

## 0. Bottom line

Three findings dominate everything else.

1. **The sigma flow is closer than the audit realised on kinematics and further than it realised on
   analysis.** Cassel–Boll–Petra–Albers–Schnörr have the roadmap's Dirichlet sector *as their entire
   model* — a harmonic map from a compact Riemannian base into the Fisher–Rao simplex — but they have
   **no bundle, no gauge group, no connection, and explicitly no existence theorem**. They state in
   §1.3 that they "leave the problem of existence and global convergence of the gradient flow for
   future work." So T4 is *not* their theorem. It is nobody's theorem yet, in this exact setting.

2. **T4 is nevertheless mostly a known theorem with a target the author has not identified.** The
   Fisher–Rao simplex is *isometric to the open positive orthant of a round sphere of radius 2*, i.e.
   constant sectional curvature 1/4, with the orthant's circumradius `2·arccos(1/√c) < π`. That places
   it strictly inside the **Hildebrandt–Kaul–Widman regular-ball condition** `R√Λ < π/2` — the classical
   existence theorem for harmonic maps into positively curved targets. And for Gaussian fibers with
   `GL(K)` frames — the parent project's actual code — the fiber is a *homogeneous space*, which puts
   the whole Dirichlet sector inside Wood's harmonic-sections framework and **Loubeau–Sá Earp's flow
   theory, which already proves uniqueness, smoothness, short-time existence and sufficient conditions
   for long-time existence** (that is T6). The author is planning to spend months re-deriving this.

3. **The roadmap's T0 was already published by the author himself, in 2025, and is uncited.**
   `Preprints.org 202505.1773.v1` already contains: principal `G`-bundle over base `C`, *two* associated
   bundles (belief and model), an agent as a *pair of local sections*, an induced connection for
   parallel transport of beliefs, a generalized variational energy with KL terms, the Fisher metric on
   fibers, and a Yang–Mills field. WP0 is not new work; it is editing.

---

## 1. The sigma flow — settling how near

**Primary source retrieved.** J. Cassel, B. Boll, S. Petra, P. Albers, C. Schnörr, *Sigma Flows for
Image and Data Labeling and Learning Structured Prediction*, arXiv:2408.15946 (v2, 29 Aug 2024);
published **J. Math. Imaging Vis. (2025)**, doi:10.1007/s10851-025-01270-w. Full text read.

Lineage retrieved: Åström–Petra–Schmitzer–Schnörr, *assignment flows* (JMIV 2017); Savarino–Schnörr,
**Continuous-Domain Assignment Flows**, arXiv:1910.07287; Sitenko–Boll–Schnörr, assignment flows as
nonlocal graph PDE; Zern–Zeilmann–Schnörr, *Assignment flows for data labeling on graphs: convergence
and stability*, Information Geometry (2021); Schwarz et al., **Quantum State Assignment Flows**,
arXiv:2307.00075, Entropy 25(9):1253 (2023).

| Question | Answer | Evidence |
|---|---|---|
| **(a) Bundle or plain map?** | **Plain map.** `f: M → N` with `N = (int Δ_c, g_FR)` a *fixed* target manifold. No principal bundle, no associated bundle, no `P ×_ρ M_q`. The only bundle in the paper is the standard harmonic-map pullback bundle `T*M ⊗ f*TN`. | §1.3, §3: "The target manifold `(N,g)` will be the interior of the probability simplex … The domain manifold `(M,h)` … can be any compact Riemannian manifold." |
| **(b) Gauge group + connection?** | **No gauge group. No principal connection.** They do use non-metric **α-connections** on the *target* and the induced pullback connection — that is intrinsic information geometry, not gauge theory. There is no `F_A`, no gauge orbit, no covariance statement. | §4.3 "extension … from the metric connection to the α-family of connections". Their extra structure is instead a **state-dependent domain metric** `h_t = O(S_t)`, learned — an orthogonal move to the roadmap's. |
| **(c) Existence theorems?** | **None, and they say so.** "Since our scenario violates basic assumptions made in the literature above (`N` is open with positive sectional curvature, non-metric affine connection) … we leave the problem of existence and global convergence of the gradient flow for future work and solely focus on *geometric* aspects in this paper." What they *do* prove is a **Lyapunov/monotonicity result**: `dΦ/dt ≤ 0` with an explicit spectral bound via the Laplace–Beltrami eigenvalues (Prop. 4.5, eqs. 4.60–4.68), plus convergence to the simplex boundary under an entropic potential (§4.4). | arXiv:2408.15946 §1.3, §4.4 |
| **(d) Discrete-to-continuum result?** | **No.** The direction of travel is the opposite: they *start* from a graph model (assignment flow) and write down a continuum model that resembles it. There is no Γ-convergence, no FE convergence, no consistency-plus-compactness theorem linking the graph assignment flow to the sigma flow. Their §1.3 says compactness of `M` "substantiates numerical experiments with `N`-valued sigma flows on a graph embedded in `M`, i.e. after a discretization of `M`" — that is a motivation sentence, not a theorem. The neighbouring literature has *numerical integration* convergence (Zeilmann–Savarino–Petra–Schnörr, *Geometric numerical integration of the assignment flow*, Inverse Problems 2020) which is a time-stepping result, not a mesh-refinement/continuum-limit result. | arXiv:2408.15946 §1.3, §5 |

**What T1/T4/T6/T8 can actually import from them**

- **T1 (well-definedness):** import the *coordinate machinery* — their §4.2/4.3 gives explicit
  implementable expressions for the tension field in both affine coordinate systems (`θ`/`η`), the
  `ε`-regularised metric `g_ε = g + ε·I` used to keep things nondegenerate at the boundary, and the
  Christoffel symbols of the α-connections in `θ`-coordinates. This is genuinely reusable and would
  otherwise cost weeks.
- **T6 (dynamics):** import their **Lyapunov argument verbatim in structure** — the `dΦ/dt ≤ 0`
  computation (4.60a–4.63) plus the uniform spectral bound (4.67–4.68) is exactly the "prove
  `dS/dt = -‖grad S‖² ≤ 0`" obligation, done for the ungauged Dirichlet sector. Also import the
  entropic-potential trick from §4.4 that forces convergence to the simplex boundary.
- **T4 (existence):** import **nothing** — they punt. But import their *diagnosis* of why it is hard
  (open target, positive curvature, non-metric connection), which is a correct and non-obvious warning.
- **T8 (discretisation):** import **nothing from Schnörr**. Go to the Γ-convergence literature instead
  (§5 below).

**What remains genuinely new versus the sigma flow:** the principal bundle and associated statistical
bundle; the gauge group and its action on the fiber laws; the covariant derivative `D^A` in place of
`d`; the Yang–Mills term; the pairwise KL coupling between *overlapping* sections with entropic
attention weights; and multi-agent structure of any kind. The sigma flow has **one** field; the roadmap
has a population of overlapping sections. That difference is real.

---

## 2. Gauged sigma models / Yang–Mills–Higgs — how much of T4 is a known theorem

`η‖D^A q‖² + κ‖F_A‖²` with a nonlinear target *is* the Yang–Mills–Higgs functional with a nonlinear
Higgs field, a.k.a. a gauged sigma model. The literature is mature and the roadmap does not cite it.

**Retrieved results and their hypotheses:**

| Result | Statement / hypotheses | Citation |
|---|---|---|
| Direct method for the pure Yang–Mills sector | Existence of an absolute minimiser of the Yang–Mills functional in a wide class of bundles, **`dim M = 4`**, topological invariant preserved by the minimising process | K. Uhlenbeck / S. Sedlacek, *A direct method for minimizing the Yang–Mills functional over 4-manifolds*, Commun. Math. Phys. **86**(4):515–527 (1982) |
| YMH existence, nonlinear target, **`d = 2` with boundary** | Existence of YMH fields over a **Riemann surface with boundary**; free boundary condition on the section, Neumann on the connection; via Sacks–Uhlenbeck `α`-YMH regularisation as `α→1`; smoothness up to boundary under a gauge transformation; extends Ladyzhenskaya–Ural'ceva and Morrey regularity to coupled systems | *The boundary value problem for Yang–Mills–Higgs fields*, arXiv:1711.05976 |
| YMH regularity, coupled system, surfaces | Full regularity of weak solutions on surfaces via **Uhlenbeck's Coulomb gauge theorem** + **Rivière's regularity theory**; YMH-Dirac model | *Geometric analysis of the Yang–Mills–Higgs–Dirac model*, arXiv:1908.00430; J. Geom. Phys. (2022), doi:10.1016/j.geomphys.2022.104670 |
| YMH, **higher dimensions `n ≥ 4`** | Decay estimates near isolated singularities and a **removable singularity theorem** under conformally invariant energy bounds, for YMH fields **on a fiber bundle** with a general compact Riemannian fiber | B. Chen, *Removable singularities of Yang–Mills–Higgs fields in higher dimensions*, arXiv:2603.11926 |
| YMH gradient flow, higher dimensions | Long-time existence of the gradient flow for YMH `k`-functionals with Higgs self-interaction provided **`dim M < 2(k+1)`** | *Gradient flows of higher order Yang–Mills–Higgs functionals*, arXiv:2004.00420; J. Aust. Math. Soc. |
| Łojasiewicz–Simon for coupled YM energies | Gradient inequalities for coupled Yang–Mills energy functions — the standard route to convergence of the flow to a critical point | arXiv:1510.03815 |
| Gauged harmonic sections of *homogeneous* fibre bundles | The natural Dirichlet energy on sections of a homogeneous fibre bundle induces an abstract harmonicity condition; **uniqueness, smoothness, short-time existence, and sufficient conditions for long-time existence** of the geometric gradient flow are established | E. Loubeau, H. Sá Earp, *Harmonic flow of geometric structures*, arXiv:1907.06072; Ann. Glob. Anal. Geom. (2023), doi:10.1007/s10455-023-09928-7 — following C. M. Wood, *Harmonic sections of homogeneous fibre bundles*, Diff. Geom. Appl. **19**(2):193–210 (2003) |
| YMH applied to *labeling* on a manifold | Binary classification on a manifold recast as a YMH variational problem; classifier-section and connection **jointly minimise** curvature + covariant-derivative energy subject to hard data conditions; Bogomolny bound selects the gauge background; `G = Z_2`, `U(1)`, `SU(2)` examples | C. Vasii, *Yang–Mills–Higgs: A Geometric Theory of Binary Labels on Non-Contractible Spaces*, arXiv:2607.00999 (2026) |

**Verdict on T4.** The *structure* of the theorem — coercivity, weak compactness in a manifold-valued
Sobolev space, closed target constraint, weak lower semicontinuity, Uhlenbeck gauge fixing for the
connection sector — is a **standard argument** in this literature. The genuinely load-bearing
hypotheses are:

- **dimension.** Everything sharp is `d = 2` (surfaces) or `d = 4` (pure YM). For `d ≥ 3` with a
  nonlinear target the results retrieved are *removable-singularity* and *flow* results, not
  existence-of-minimisers. The roadmap's "`d`-dimensional base" is doing a lot of unpaid work. **If the
  author fixes `d = 2` he can likely cite his way to T4; if he insists on general `d` he is at the
  research frontier and should say so.**
- **target compactness/curvature.** The retrieved YMH results assume a **compact** Riemannian fiber
  (Chen arXiv:2603.11926 explicitly). The roadmap's coercive-confinement hypothesis is the right
  substitute, and for the simplex fiber the HKW regular-ball condition (§3) supplies it for free.

---

## 3. Statistical manifolds as sigma-model targets

**The fact the roadmap is missing.** Under `ξ_k = 2√p_k`, the Fisher–Rao metric on the open simplex
`ds² = Σ dp_k²/p_k` becomes the Euclidean metric restricted to the **positive orthant of a sphere of
radius 2** — i.e. the target has *constant positive sectional curvature `Λ = 1/4`*. (Retrieved:
*Information Geometry of the Probability Simplex: A Short Course*, arXiv:1911.01876; Nielsen,
*Fisher–Rao and pullback Hilbert cone distances on the multivariate Gaussian*, PMLR 221 (2023).)

Consequently: `√Λ = 1/2`, and the orthant's circumradius about the barycentre is `2·arccos(1/√c) < π`,
so **`R√Λ < π/2` holds for every finite label count `c`** — the *regular ball* hypothesis of

> S. Hildebrandt, H. Kaul, K.-O. Widman, *An existence theorem for harmonic mappings of Riemannian
> manifolds*, **Acta Math. 138**:1–16 (1977).

HKW proves existence for the Dirichlet problem when the boundary data lie in a uniformly regular ball
(closure meets no cut locus; `R√Λ < π/2`). **This is a direct, citable existence route for the roadmap's
Dirichlet sector with categorical fibers**, and it is exactly the theorem the sigma flow paper cites and
then declines to apply. See also *Harmonic maps into a hemisphere*, Ann. Sc. Norm. Sup. Pisa 12(1):81
(1985), for the sharp-radius boundary case.

**For Gaussian fibers the geometry is the opposite and also favourable-with-a-caveat.** The
one-dimensional / diagonal Gaussian family with the Fisher metric is hyperbolic (constant negative
curvature) — the Eells–Sampson/Hartman nonpositive-curvature case, where existence *and uniqueness* are
classical. But **the full multivariate Gaussian manifold is not NPC for dimension > 1**: some sectional
curvatures are positive (retrieved via Skovgaard, *A Riemannian geometry of the multivariate normal
model*, Scand. J. Statist. **11**:211–223 (1984), and Nielsen PMLR 221 (2023)). So the roadmap's
"Gaussian and categorical are two non-isomorphic instantiations" plan is sound, but the author must not
assume the Gaussian case is the easy one — **it is the harder one**, and WP1's exit gate should say so.

**Other target-side prior art retrieved:**

- K. Uohashi, *Harmonic maps relative to α-connections* (in *Geometric Theory of Information*, Springer
  2014) — harmonic maps between level surfaces of Hessian domains relative to α-connections. The sigma
  flow paper cites it and notes Uohashi's closing plea, "It is an important problem to find
  applications of non-trivial harmonic maps relative to α-connections." The roadmap is such an
  application. Cite it.
- N. Ay, J. Jost, H. V. Lê, L. Schwachhöfer, *Parametrized measure models*, **Bernoulli 24(3)** (2018),
  arXiv:1510.07305, and the book *Information Geometry* (Springer 2017) — the correct citation for the
  Fisher metric/Amari–Chentsov tensor **as a pullback**, which the audit already flags as making the
  roadmap's framing definitional rather than novel.
- G. Pistone, *Lagrangian function on the finite state space statistical bundle*, **Entropy 20(2):139**
  (2018); *Affine statistical bundle modeled on a Gaussian Orlicz–Sobolev space*, **Information
  Geometry** (2022), arXiv:2210.07641. Note: the audit says the parent project "does not cite" Pistone,
  but the **research vault already has him** — `sources/papers/pistone-2018-statistical-bundle-lagrangian.md`
  and `sources/papers/chirco-2022-statistical-bundle-dynamics.md`. The gap is in the manuscript, not the
  knowledge base.
- **Fisher–Rao gradient flow = replicator dynamics** is standard; the reaction–diffusion / birth–death
  PDE literature is the Wasserstein–Fisher–Rao family (arXiv:2405.15834, arXiv:2511.18060,
  arXiv:2506.05905). Relevant to T6 for *mobility choice*, but note this is Fisher–Rao on the space of
  measures over the base, which is a **different object** from Fisher–Rao in the fiber. Do not conflate
  them; a referee will.
- T. Enßlin, *Information field theory*, arXiv:1301.2556 — a Bayesian statistical field theory for
  spatially distributed signals. **Not** prior art for the roadmap: there the field is the *unknown* and
  the probability lives on field configurations; here each base point *carries* a distribution. Worth a
  one-line distinguishing citation to pre-empt the obvious referee question.

---

## 4. The gauge/bundle half — Schnörr's group already owns this too

This is the finding most likely to cost the author priority, and it is not in the audit.

- J. Cassel, F. Schlindwein, P. Albers, C. Schnörr, **Bundle Scale Spaces and Local Gauge Symmetries
  for Graph Networks**, SSVM 2025, LNCS 15668, doi:10.1007/978-3-031-92369-2_19. Node features modelled
  as **sections of associated vector bundles**; architectures equivariant under **local** group actions;
  diffusion PDEs on vector bundles via a generalized Laplacian; fixed points are **harmonic sections**;
  discretisation by **vector diffusion maps and lattice gauge theory** while respecting local symmetry.
- **Yang–Mills Meets Data**, arXiv:2510.19431 (2025). "Gauge symmetric methods for data representation
  … differential geometry of vector bundles … local symmetry and equivariance … discrete descriptions of
  vector bundles motivated by lattice gauge theory … gauge symmetric heat kernel operators closely
  related to **graph connection Laplacians** … we utilize a **discrete Yang–Mills energy**."
- D. Gonzalez-Alvarado, F. Schlindwein, J. Cassel, L. Steingruber, S. Petra, C. Schnörr, **Riemannian
  Patch Assignment Gradient Flows**, SSVM 2025, arXiv:2504.13024 — labelings as critical points of a
  **Lagrangian action functional**, integrated by Riemannian ascent.

So the Heidelberg group has (i) the Fisher–Rao-fiber harmonic map, (ii) the gauge/associated-bundle/
Yang–Mills-energy machinery, and (iii) action-functional formulations — **in three separate papers by
overlapping authors within eighteen months.** They have not merged (i) with (ii). The roadmap's merge is
therefore still open, but it is an *obvious next paper for a well-resourced group that is already
holding both halves*. This is a timing risk, and it argues strongly against a multi-year theorem
programme.

**Confirmed negative (useful):** the gauge-equivariant CNN literature — T. Cohen, M. Weiler, B. Kicanaoglu,
M. Welling, *Gauge Equivariant Convolutional Networks and the Icosahedral CNN*, ICML 2019,
arXiv:1902.04615; M. Weiler, P. Forré, E. Hoogeboom, M. Welling, *Coordinate Independent Convolutional
Networks*, arXiv:2106.06020 — uses **linear representations `ρ: G → Aut(V)` on vector-space fibers**
throughout. Searches for a gauge-equivariant architecture with a *statistical-manifold* (nonlinear,
non-vector) fiber returned nothing. That specific substitution is real, though as the audit says, small.

---

## 5. Multi-agent / interacting variational fields

**What exists.**

- **KL consensus on densities.** G. Battistelli, L. Chisci, *Kullback–Leibler average, consensus on
  probability densities, and distributed state estimation with guaranteed stability*, **Automatica
  50(3):707–718 (2014)** — agents hold PDFs, the consensus target is the minimiser of the sum of KL
  divergences, which is the normalised **geometric mean** (logarithmic opinion pool). This is the
  roadmap's peer-KL coupling term, on a graph, with a stability theorem. Also *Distributed Bayesian
  filtering using logarithmic opinion pool for dynamic sensor networks*, Automatica (2018). **The
  roadmap's peer sector is a continuum-base lift of a solved discrete problem.** Cite it or a referee will.
- **f-divergence opinion dynamics.** *Mathematical measures of societal polarisation*, arXiv:2208.05080 —
  opinions as probability distributions compared by KL/Hellinger.
- **Kinetic/mean-field opinion dynamics.** Toscani-lineage Boltzmann-type PDEs for opinion
  distributions; Degond et al., *Continuum dynamics of the intention field under weakly cohesive social
  interactions*, arXiv:1607.06372 — a continuum **intention field**. These take the mean field *over
  agents*; the roadmap instead indexes agents by a base manifold. Different limit, related toolkit.

**Confirmed negative.** Searches for a continuum limit of interacting *Bayesian* agents where each base
point carries a full distribution and neighbours couple by KL *inside a gauge-covariant action* returned
nothing. The multi-agent sector of the roadmap has no direct competitor. It is also the sector with the
least mathematical leverage — it is the part most likely to be dismissed as "an engineered consensus
energy," which the project's own README already concedes.

**Author's existing vault coverage** (`Desktop/Research/wiki`, `cluster/social-physics`): he already has
`Belief inertia`, `Mass as Fisher information`, `Hamiltonian belief dynamics`, `Sociophysics`,
`SocialPhysics`, and the theme page *Statistical physics of social systems and collective behavior*, plus
`manuscripts/belief_inertia.tex`. Battistelli–Chisci and the Degond intention field do **not** appear.
Those are the two cheapest ingests.

---

## 6. The entropic / softmax sector (T3)

**What is known.** `min_β [ β·D + τβ log(β/π) ]` over the simplex giving softmax and `-τ log Z` is
textbook entropic regularisation / Sinkhorn / soft-min. Recent explicit statements retrieved:

- *Scaled-Dot-Product Attention as One-Sided Entropic Optimal Transport*, arXiv:2508.08369 (2025) —
  proves the attention forward pass **is** the exact solution of a degenerate one-sided entropic OT
  problem, and that the resulting information geometry (the Fisher matrix on attention distributions)
  dictates the backward pass. This is T3's pointwise content, published, with the Fisher-geometric
  refinement the roadmap has not thought of.
- T. Enßlin et al., *Attention to Entropic Communication*, arXiv:2307.11423.
- The sigma flow's own §4.4 entropic potential, and the assignment-flow "S-flow" softmax structure, plus
  the transformer comparison in arXiv:2408.15946 §5.3.

**Confirmed negative — and this is the roadmap's best card.** Searches for attention weights as *fields
on overlaps* `U_i ∩ U_j`, eliminated by an **envelope theorem inside a continuum action functional**,
with the reduced `-τ log Z` re-entering as an effective potential and the envelope derivative feeding the
Euler–Lagrange system, returned **nothing**. The pointwise algebra is old; the statement that the
elimination is measurable in the base, that the reduced functional is still weakly lower semicontinuous,
and that the envelope derivative is the correct first variation, is **not** in the literature. T3 is the
one theorem target in the roadmap that is genuinely new *and* small enough to finish.

---

## 7. Deliverable — T0–T9 importability table

| Target | Verdict | Basis |
|---|---|---|
| **T0** typed kinematics | **ALREADY DONE BY THE AUTHOR** (uncited) | R. C. Dennis, *Epistemic Gauge Theory*, Preprints.org **202505.1773.v1** (23 May 2025) already has the principal `G`-bundle over `C`, two associated bundles, agent = pair of local sections, induced connection for belief transport, generalized variational energy with KL terms, fiber Fisher metric, and a Yang–Mills field. WP0 is a rewrite, not a discovery. **Must be cited in any submission.** Supporting formalism: Ay–Jost–Lê–Schwachhöfer arXiv:1510.07305 + *Information Geometry* (2017); Pistone Entropy 20(2):139 (2018). |
| **T1** well-definedness | **ADAPTABLE** | Manifold-valued Sobolev spaces `W^{1,2}(M,N)` are standard (Jost, *Riemannian Geometry and Geometric Analysis*, ch. 9 — cited by arXiv:2408.15946 §1.2.2 for `Γ`-convergence lower semicontinuity of the harmonic energy). Import the `ε`-regularised Fisher metric `g_ε = g + εI` and the explicit `θ`/`η`-coordinate expressions from arXiv:2408.15946 §4.2–4.3 wholesale. New work: only the extended-real conventions at the simplex boundary and the typing of the overlap integrals. |
| **T2** gauge covariance | **IMPORTABLE (largely)** | Standard associated-bundle gauge covariance: Cohen et al. arXiv:1902.04615, Weiler et al. arXiv:2106.06020; Cassel–Schlindwein–Albers–Schnörr SSVM 2025 (doi:10.1007/978-3-031-92369-2_19) for the sections-of-associated-bundles version; arXiv:2510.19431 for the discrete gauge-symmetric formulation. The audit already rates this chapter "Cohen/Weiler item for item, damage HIGH." Genuinely new: only that `ρ: G → Diff(M_q)` is a **nonlinear, family-preserving** action rather than a linear rep. State it in one proposition, do not write a chapter. |
| **T3** attention-row elimination | **GENUINELY NEW** (the field-theoretic part only) | Pointwise softmax-from-entropic-regularisation is known: arXiv:2508.08369 (exact one-sided entropic OT), arXiv:2307.11423. **Nothing found** on simplex-valued attention *fields* on overlaps eliminated by an envelope theorem inside a continuum action, with measurable selection + preserved lower semicontinuity + the envelope derivative as first variation. **This is the highest-value/lowest-cost target in the roadmap.** |
| **T4** existence of minimizers | **ADAPTABLE — largely someone else's theorem, with a target the author has not identified** | Not the sigma flow's (they explicitly defer it: arXiv:2408.15946 §1.3). But: (i) Fisher–Rao simplex ≅ sphere orthant, `Λ = 1/4`, circumradius `< π` ⇒ **Hildebrandt–Kaul–Widman, Acta Math. 138:1–16 (1977)** regular-ball condition `R√Λ < π/2` is *satisfied*; (ii) direct method for the YM sector: **Sedlacek/Uhlenbeck, CMP 86(4):515 (1982)**, `d = 4`; (iii) coupled YMH existence on surfaces with boundary: **arXiv:1711.05976**; (iv) higher-`d` YMH on fiber bundles with compact fiber: **B. Chen arXiv:2603.11926**. **Caveat: the sharp results are `d = 2` or `d = 4`. For general `d` with a nonlinear target this is frontier, not textbook.** Fix `d = 2` and T4 becomes a citation exercise plus a coercivity lemma. |
| **T5** first variation | **IMPORTABLE** | The YMH Euler–Lagrange system (harmonic-map equation coupled to the YM equation) is written out in the YMH literature: arXiv:1908.00430, arXiv:2603.11926, arXiv:1711.05976. The Fisher-fiber tension field in `θ`/`η` coordinates is written out in arXiv:2408.15946 §4.2. The only new terms are the peer-KL and attention variations. This is a weekend of algebra plus a symbolic check, not a work package. |
| **T6** dynamics (`dS/dt ≤ 0`, local well-posedness) | **IMPORTABLE for the homogeneous-fiber case; ADAPTABLE otherwise** | **Loubeau–Sá Earp, arXiv:1907.06072, Ann. Glob. Anal. Geom. (2023)** already prove uniqueness, smoothness, **short-time existence, and sufficient conditions for long-time existence** for the gradient flow of the Dirichlet energy on **sections of homogeneous fibre bundles**, following **Wood, Diff. Geom. Appl. 19(2):193–210 (2003)**. For Gaussian fibers with `GL(K)` frames — the parent project's actual code — the fiber `GL(K)/O(K)` **is** homogeneous, so this applies almost verbatim. Also import the explicit dissipation + spectral bound from arXiv:2408.15946 (4.60–4.68), and Łojasiewicz–Simon for coupled YM energies (arXiv:1510.03815) for convergence to critical points. **WP2 as scoped is largely redundant.** |
| **T7** zero-dimensional reduction to softmax attention | **ADAPTABLE / partly anticipated** | The assignment-flow ↔ transformer correspondence is already published: arXiv:2408.15946 §5.3 "Relation with the Transformer Network Architecture" and the abstract's "structural similarities to transformer network architectures." Attention-as-entropic-OT: arXiv:2508.08369. Also *Gauge Fiber Bundle Geometry of Transformers* (OpenReview `sPCLRX1yOY` — abstract not retrievable, OpenReview served a bot challenge; flagged as an unresolved check). The `μ({∗}) = 1` degeneration argument itself is trivial once T0 is typed. Low value; state as a remark, not a theorem. |
| **T8** discretisation limit | **ADAPTABLE — and NOT available from Schnörr** | The assignment-flow lineage has **numerical-integration** convergence (Zeilmann–Savarino–Petra–Schnörr, *Geometric numerical integration of the assignment flow*, **Inverse Problems 36(3):034003 (2020)**; Zern–Zeilmann–Schnörr, *Assignment flows for data labeling on graphs: convergence and stability*, **Information Geometry 4:355–404 (2021)**) — time-stepping, not mesh refinement. The right import is the **discrete-to-continuum Γ-convergence** literature: **N. García Trillos & D. Slepčev**, *A variational approach to the consistency of spectral clustering* (ACHA 2018) and the graph total-variation/`p`-Dirichlet continuum-limit papers; *Consistency of Dirichlet partitions*, SIAM J. Math. Anal. (doi:10.1137/16M1098309); *Γ-convergence of nonlocal Dirichlet energies with penalty formulations of Dirichlet boundary data*, SIAM J. Math. Anal. (doi:10.1137/23M1604746). **All of it is for scalar/`R^n`-valued fields.** Extending Γ-convergence to *manifold-valued* graph Dirichlet energies with a gauge connection is real new work. Lattice-gauge discretisation respecting local symmetry is in arXiv:2510.19431 and SSVM 2025 doi:10.1007/978-3-031-92369-2_19 — import that, prove the Γ-limit yourself. **T8 is the most expensive item in the roadmap.** |
| **T9** optional Gibbs completion | **IMPORTABLE / low value** | Configuration-space Gibbs variational identity is standard statistical mechanics (Donsker–Varadhan / Gibbs variational principle); the only content is proving `0 < Z < ∞` for this action, which is a coercivity corollary of T4. The roadmap already correctly marks it optional. Do not spend time here. |

**Score:** of ten targets — 1 already done by the author, 3 importable, 4 adaptable, 1 genuinely new
(T3), 1 expensive-and-new (T8). **The roadmap's own "decisive first milestone" (T4) is the one where
the author is closest to re-deriving a 1977 theorem.**

---

## 8. Strategic recommendation

**Extract `05c` first. Do not start the continuum programme.**

The reasoning is not sentiment; it is the intersection of three retrieved facts.

1. **`05c` is finished and the continuum programme is nine work packages from finished.** `05c` is 1,392
   lines / ~30 pages, 24 numbered results, every proof written out to `□`, no TODOs, worked
   counterexamples with exact rational arithmetic, and only three external citations. Its external
   cross-references (≈6 into ch. 02, 2 into the RG chapter) are inlineable in an afternoon. The audit's
   own recommendation — submit it as *"Connection-relative informational pullbacks: gauge covariance,
   connection dependence, and a horizontal-defect calculus"* to *Information Geometry* or *Diff. Geom.
   Appl.* — is correct and I found nothing to disturb it.

2. **`05c` does not need the continuum programme.** It is already smooth/continuum from the start —
   smooth base `C`, smooth principal bundle, `ver ∘ Ts` jets, Frobenius/contact arguments — but its base
   is *context space*, not a continuum of agents, and it explicitly declines to introduce a base measure,
   a base integral, a free energy, or a law on sections. **The PIFB2 continuum roadmap adds exactly the
   ingredients `05c` refuses, and every wave-1 structural criticism attacks the free-energy layer that
   `05c` does not contain.** So the roadmap moves *away* from the defensible content: it re-attaches the
   attack surface that `05c`'s scope discipline removed. T9 in particular ("optional Gibbs completion")
   is the roadmap voluntarily re-opening the exact wound.

3. **The continuum programme is in a race the author cannot win.** The Heidelberg group holds the
   Fisher–Rao harmonic map (arXiv:2408.15946), the associated-bundle/local-gauge/harmonic-sections
   machinery (SSVM 2025, doi:10.1007/978-3-031-92369-2_19), and a discrete Yang–Mills energy on data
   bundles (arXiv:2510.19431) — three papers, overlapping authors, eighteen months, DFG SPP 2298 funding.
   Merging (i) and (ii) is their obvious next paper. Meanwhile the roadmap's decisive milestone T4 is
   substantially HKW 1977 plus Sedlacek 1982, and its T6 is substantially Loubeau–Sá Earp 2023. A solo
   author should not spend WP1+WP2 (the roadmap's own critical path) re-deriving those while a funded
   group with both halves in hand closes the gap.

**Concrete sequence I would recommend instead.**

1. **Now (weeks, not months): extract and submit `05c`.** Add an abstract, inline the six ch. 02
   cross-references, fix the two-line proof gap the audit flags at `05c:124`, and add the prior-art
   paragraph this report supplies (Wood 2003 for harmonic sections; AJLS arXiv:1510.07305 for the
   pullback framing; Cohen/Weiler for the equivariance context; Sengupta–Friston as the thing being
   critiqued). The horizontal-defect calculus survived eight logged searches in the audit and nothing in
   my ten-plus searches disturbed it. **Ship it before someone else needs it.**

2. **Then (a short second paper, not a programme): T3 alone.** The entropic elimination of attention
   *fields* on overlaps, with measurable selection, preserved lower semicontinuity, and the envelope
   derivative — in the zero-dimensional and `d = 1` settings where everything is provable. It is the one
   target with a confirmed negative search result, it is small, and it is the honest bridge between the
   attention literature and the information-geometry literature. Pair it with the already-flagged
   secondary extraction candidate `prop:obs-attention-elbo` (`05b:547`).

3. **Only then, and scoped down: `d = 2`.** If the continuum programme proceeds, fix the base to a
   surface. At `d = 2` T4 and T5 become citation-plus-lemma (arXiv:1711.05976, arXiv:1908.00430, HKW
   1977) rather than research, T6 comes from Loubeau–Sá Earp for homogeneous fibers, and the author
   reaches a submittable continuum paper in a fraction of WP1+WP2. **Drop T7 to a remark and drop T9
   entirely.** Keep T8 as an explicitly-labelled open problem — it is the genuinely hard, genuinely new
   piece, and it should not gate anything else.

4. **Cite the 2025 preprint.** `Preprints.org 202505.1773.v1` is the author's own and contains T0.
   Failing to cite it in a journal submission is a duplicate-publication exposure, not just a courtesy
   lapse.

---

## 9. Searches run (including the ones that returned nothing)

Negative results are load-bearing; these are the queries whose emptiness supports the novelty claims
for T3 and the fiber-nonlinearity claim in T2.

**Productive:** sigma flow / Schnörr / harmonic map to statistical manifold · assignment flow
continuum limit / Zeilmann · gauged sigma model / YMH existence and regularity · YMH minimizers direct
method higher dimensions · quantum state assignment flows · Dennis *Epistemic Gauge Theory* · Batard–
Sochen equivariant diffusion on vector bundles · Bundle Scale Spaces / local gauge symmetries / graph
networks · *Yang–Mills Meets Data* · Riemannian patch assignment gradient flows · HKW regular ball ·
Fisher–Rao simplex ≅ sphere orthant · multivariate Gaussian Fisher curvature / Skovgaard · YMH on
Riemann surfaces · García Trillos–Slepčev Γ-convergence · Pistone statistical bundle · Enßlin
information field theory · Uohashi α-connection harmonic maps · KL-average consensus on densities ·
Wasserstein–Fisher–Rao gradient flows · SDPA as entropic OT · Wood harmonic sections.

**Empty (negative results):**
- *"gauge equivariant neural network fiber probability simplex associated bundle statistical manifold
  fiber gauge group acting on distributions"* — the equivariant-CNN literature uses **linear** reps on
  vector fibers only. Supports the "nonlinear statistical fiber" novelty, small as it is.
- *"attention weights as fields eliminated envelope theorem entropic regularization continuum action
  functional field theory of attention overlaps"* — returned only pointwise/architectural results
  (arXiv:2508.08369, arXiv:2307.11423). **Supports T3 as genuinely new.**
- *"gauge-covariant / covariant Dirichlet energy + Fisher statistical manifold + Yang–Mills term
  minimizers existence"* — returned generic YMH and the unrelated Vasii label paper (arXiv:2607.00999).
  No one has written the roadmap's action.
- *"continuum limit interacting Bayesian agents opinion dynamics probability distribution KL coupling
  mean-field PDE"* — returned kinetic opinion dynamics over agent-space, not base-indexed belief fields.
  Supports the multi-agent sector as unoccupied (though low-leverage).
- *"free energy principle / active inference continuum field theory agents sections bundle"* — nothing
  with bundles or sections. Consistent with the audit's read of Sengupta–Friston as a programmatic essay.

**Blocked / unresolved:**
- arXiv API: HTTP 403, `Connection blocked by network allowlist` (sandbox). Worked around with
  WebSearch + `arxiv.org/abs/` fetches.
- OpenReview `sPCLRX1yOY` (*Gauge Fiber Bundle Geometry of Transformers*): served a browser-verification
  challenge; abstract not retrieved. **Flagged as an open check bearing on T7.**
- arXiv:2607.00999 PDF returned no machine-readable text; details recovered via search of the HTML
  version. Author and abstract confirmed, full text not read.
