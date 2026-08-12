# rm-04 — Referee report on the kinematic layer of the PIFB2 continuum roadmap

**Document under review:** `C:\Users\chris and christine\Documents\ChatGPT\MultiAgentELBO\docs\research-plans\2026-08-12-pifb2-continuum-roadmap.md`
(read in full; primary scope lines 30–68, T0/T2/T7 at 112/114/119, E1/E2 at 132–133).

**Reviewer's standpoint:** differential geometry and gauge theory. The question is not whether the
theorems are provable but whether the objects they quantify over exist, are uniquely typed, and are
mutually consistent. A theorem about an inconsistent kinematics is not worth proving.

**Execution policy: CPU only. No GPU or CUDA job was started or attempted.** All numerics in an
isolated Linux sandbox, `python3` with `numpy 2.2.6` / `sympy 1.14.0`, float64 and exact symbolic
where noted. Scripts and outputs are logged in §9.

**Corpora cross-read:** `MultiAgentELBO/docs/audits/2026-08-11-ultradeep-expert-audit.md`,
`.../ultradeep-2026-08-11/audit-01-geometry.md`, `.../ultradeep-wave2-2026-08-12/wave2-01-constructions.md`,
`MultiAgentELBO/Theory/02_geometry.tex` (772 lines), `Theory/05c_pullback_geometry.tex` (1391 lines),
`Theory/08_infogeometry.tex`, `Research/manuscripts/PIFB2.tex` (3956 lines).

---

## 0. Headline verdict

**The `ρ`-by-isometries question resolves in the roadmap's favour for the Gaussian showcase and
against it for the categorical showcase, and the reason is a theorem, not a modelling choice.**

1. `GL(K,ℝ)` acting on the Gaussian family by the declared *pushforward congruence*
   `(μ,Σ) ↦ (Aμ, AΣAᵀ)` **is** a Fisher–Rao isometry — verified to `7.6e-15` (§1.2), already
   proved in the corpus at `05c:59` and separately sourced at `08:97`. Not merely that: for `K ≥ 2`
   the affine group is the **entire identity component of the Fisher–Rao isometry group**
   (computed, §1.1b). `GL(K)` is not an arbitrary choice; it is the maximal one. **T2 does not fail
   here.**
2. For the categorical fiber the Fisher–Rao isometry group is **`S_{n+1}`, finite of order
   `(n+1)!`** (computed and proved, §1.1a). Therefore *no positive-dimensional Lie group acts on a
   categorical fiber by Fisher–Rao isometries*, and any connected `G` acts trivially. The
   roadmap's own multi-family requirements (E0 line 131, WP1 exit gate line 147, WP3 line 162)
   cannot be met with one fixed positive-dimensional `G`. **FATAL for those gates as written.**
3. The escape hatch at line 48 — "preserve, **or transform covariantly with**, the chosen
   information geometry" — is not available. **Lemma 1.3:** any map preserving the divergence
   `D_q` automatically preserves `g^F_q`, because Fisher *is* the Hessian of the divergence
   (verified §1.3). So invariance of the *peer and self* sectors alone already forces
   `ρ(G) ⊆ Isom(ℳ, g^F)`. Isometry is not an extra hypothesis that can be traded for covariance;
   it is a consequence of T2 restricted to the divergence sectors.
4. **Independent FATAL, previously unreported:** `κ∫‖F_A‖²dμ` cannot be both gauge-invariant and
   nonnegative for `G = GL(K,ℝ)`. The space of `Ad`-invariant symmetric bilinear forms on
   `gl(K,ℝ)` is exactly two-dimensional (`tr(XY)` and `tr X·tr Y`) and **every** element of it is
   indefinite — signature `(3,1)` for `K=2`, `(6,3)` for `K=3`, no positive-definite combination
   (exhaustive search, §1.5). T2 ("invariance of `𝒮`") and T4 ("positive covariant spatial terms",
   "bounded-below") are therefore **mutually inconsistent** for the showcase group. Line 13's claim
   that compactness of `G` is an *analytical* hypothesis "not an ontological commitment" is wrong
   for the curvature sector: compact type is a **kinematic** necessity and belongs in T0.

**The non-transitivity axiom T0 needs**, in one sentence:

> **(A-NT)** *The pair `(ρ_q, ℳ_q)` and the population `V` must satisfy: the diagonal
> `Aut_G(P)`-action on the full field tuple `Φ = (q_i, p_i, s_i, r_i, L^q_{ij}, L^s_{ij}, A,
> E^{obs}_i)_{i∈V}` has orbit space of positive dimension, and the action functional `𝒮` must be
> declared as a functional on `Φ/Aut_G(P)`; the invariant content is exhibited explicitly.*

The roadmap has **two** independent escapes from Theorem A-NOGO, and it should name both, because
the second is stronger and it survives even a torsor fiber (§2.2):

- **(E-a) non-transitive fiber action.** `ℳ_q/G` is nontrivial. Verified for the Gaussian fiber
  under `GL⁺(K)`: `ℬ/G ≅ [0,∞)` via `r = (μᵀΣ⁻¹μ)^{1/2}` — wave 2's computation **confirmed**
  (invariance `4.1e-12`; transitivity on level sets by explicit `A*` with residuals `≤1.1e-14`,
  §2.1). That is **one real number per belief per context**. Escape (E-a) alone is nearly vacuous.
- **(E-b) multiple sections, one gauge group.** With `N ≥ 2` agents at a common context the
  diagonal quotient has dimension `N·dim ℬ − dim G + dim(stab)`: for `K=4`, `N=1` gives **1**,
  `N=2` gives **12**, `N=8` gives **96** (computed, §2.2). Theorem A-NOGO is stated for a *single*
  section (`wave2-01:29-40`); the roadmap's action is a functional of a population, so A-NOGO does
  not apply to it. **This should be said explicitly in T0, with the dimension count.** It is the
  roadmap's strongest structural card and it is currently unplayed.

Severity summary (details and locations in §8):

| # | Rank | Finding |
|---|---|---|
| K1 | **FATAL** | `‖F_A‖²` is not simultaneously `Ad`-invariant and positive for `G=GL(K,ℝ)`; T2 ⟂ T4 |
| K2 | **FATAL** | No positive-dimensional `G` acts on a categorical fiber by isometries; E0/WP1/WP3 gates unsatisfiable as written |
| K3 | **STRUCTURAL** | T0 has no non-transitivity / orbit-space axiom (A-NT above) |
| K4 | **STRUCTURAL** | `L_{ij}` and `A` are given with no compatibility axiom; `hyp:geo-graph-base-transport` (`02:625-640`) is the missing declaration and is already written in the corpus |
| K5 | **STRUCTURAL** | T2 conflates passive well-definedness, active equivariance, and active invariance |
| K6 | **STRUCTURAL** | Line 48's "induced by declared probability-law transformations" is too weak; the load-bearing hypothesis is `hyp:pb-regular-models` (`05c:37-41`) |
| K7 | **STRUCTURAL** | T4 has no slice/gauge-fixing hypothesis; minimising sequences drift along noncompact gauge orbits |
| K8 | **TECHNICAL** | T7's `d=0` reduction destroys the *local* gauge group (`Aut_G(P)={*}→G` becomes global); E1 at `d=0` cannot test the central symmetry |
| K9 | **TECHNICAL** | E1 as written is confirmatory: constant gauge transformations are provably blind to the connection's inhomogeneous term (residual exactly `0.000e+00`, §6.1) |
| K10 | **TECHNICAL** | E1 has no mesh-scaling arm; the "correct" residual is pure `O(h²)` truncation (ratio `4.00` per halving, §6.1), so a fixed tolerance conflates truncation with gauge violation |
| K11 | **TECHNICAL** | E2's first arm is an algebraic identity (proved §6.2); only the second arm can fail, and only if a third "holonomy response" arm is added |
| K12 | **TECHNICAL** | The roadmap does not cite the 17.5k-line rigorous corpus that already discharges roughly half of T0 (§7) |
| K13 | **COSMETIC** | `u_i: U_i → P` at line 66 silently requires `P|_{U_i}` trivializable (audit G3 transfers verbatim) |

**Credit where due.** Line 66 is a correct and valuable repair of a real category error in
`PIFB2.tex:208`; line 160 is a correct and valuable classification of the implementation's terms;
line 32 correctly identifies the missing base cometric; line 104 correctly identifies an untyped
expectation. These are itemised in §3.1 and §8.

---

## 1. The `ρ: G → Diff(ℳ)` requirement (roadmap lines 40–48)

The roadmap requires (line 48) that `ρ_q, ρ_s` "must be induced by declared probability-law
transformations and must preserve, or transform covariantly with, the chosen information geometry."
This one sentence carries the whole of T2. I interrogate it in five parts.

### 1.1 The isometry groups, computed

**(a) The categorical simplex. `Isom(Δ_n°, g^F) ≅ S_{n+1}`, finite of order `(n+1)!`.**

*Computation* (`c1_simplex.py`, symbolic, `n=3`). With free coordinates `p_0..p_{n-1}` and
`p_n = 1−Σp_i`, the Fisher metric `g^F_{ij} = Σ_k ∂_i p_k ∂_j p_k / p_k` and the pullback of the
Euclidean metric under `x_k = 2√p_k` agree **identically as symbolic matrices**:

```
g_Fisher - g_sphere(radius 2) = Matrix([[0,0,0],[0,0,0],[0,0,0]]),     Σ_k x_k² = 4
```

so `(Δ_n°, g^F)` is isometric to the open positive orthant of `S^n(2)`, constant curvature `+1/4`.

*Proof of the isometry group.* The orthant is an intersection of `n+1` open hemispheres contained
in one open hemisphere, hence geodesically convex, so its intrinsic metric is the restricted
spherical metric. A self-isometry is therefore a local isometry between connected open subsets of
a space form and extends uniquely to `A ∈ O(n+1)`. `A` maps the open positive cone onto itself,
hence permutes its extreme rays while remaining orthogonal, hence is a permutation matrix.
Conversely every permutation preserves the orthant. `∎`

*Numerical corroboration:* `0 / 200` random `O(4)` elements preserve the open orthant; all `24`
permutation matrices do.

**Consequence.** `Isom(Δ_n°, g^F)` is a **finite** group. Any homomorphism `ρ: G → Isom(Δ_n°, g^F)`
from a connected Lie group is trivial. This is the sharpest statement in the report and it is
consistent with Chentsov's theorem: the Fisher metric is the *unique* metric invariant under
congruent Markov morphisms, so its isometries are exactly the relabellings of the sample space.

**(b) The multivariate Gaussian family. `Isom°(ℳ_{MVN}, g^F) = Aff(K,ℝ)° = GL⁺(K)⋉ℝ^K` for `K ≥ 2`;
strictly larger (`PGL(2,ℝ)`, dimension 3) for `K = 1`.**

*Computation* (`c3_isom.py`, symbolic metric → exact `∂g`, `∂²g` at `(0,I)` → Christoffel →
Riemann → curvature-annihilator `h(p) = {A ∈ so(T_pℳ) : A·R_p = 0}` by SVD rank):

```
K=1  dim M = 2   scalar curvature at (0,I) = -1.000000
      curvature-annihilator dim h(p) <= 1   (dim so(K) = 0)
      => dim Isom <= 3      dim Aff(K,R) = 2   *** Isom STRICTLY LARGER ***
K=2  dim M = 5   scalar curvature at (0,I) = -3.500000
      h(p) <= 1  (dim so(2)=1)  => dim Isom <= 6 = dim Aff(2,R)   EQUAL
K=3  dim M = 9   scalar curvature at (0,I) = -9.000000
      h(p) <= 3  (dim so(3)=3)  => dim Isom <= 12 = dim Aff(3,R)  EQUAL
```

*Argument.* `Aff(K,ℝ)` acts transitively by isometries (verified in §1.2 and recorded at `08:97`),
with isotropy `O(K)` at `(0,I)`; `dim ℳ = K(K+3)/2 = dim Aff(K) − dim O(K)`. Hence `Isom` acts
transitively and `dim Isom = dim ℳ + dim Isom_p`. Any isometry fixing `p` preserves `R_p`, so the
isotropy algebra embeds in `h(p)`; the computation gives `dim h(p) = dim so(K)` for `K = 2,3`.
Since `Aff(K,ℝ)` acts effectively (kernel: `Aμ+b=μ ∀μ` and `AΣAᵀ=Σ ∀Σ` force `A=I, b=0`), the
bound is attained and `Isom° = Aff(K,ℝ)°`. For `K=1`, `dim ℳ = 2` and the scalar curvature `−1`
gives sectional curvature `−1/2`: the model is the hyperbolic plane, `Isom ≅ PGL(2,ℝ)`, dimension
`3 > 2 = dim Aff(1,ℝ)`. `∎`

**Reading.** `GL(K)⋉ℝ^K` is not one arbitrary group among many for the Gaussian fiber. For `K ≥ 2`
it is *the* isometry group. The roadmap's hedge at line 13 ("The structural theory is neither
Gaussian nor intrinsically `GL(K)`") is correct as a statement about the abstract layer but
understates a genuine result: *given* the Gaussian fiber, `GL(K)` is forced.

### 1.2 Does the implementation's `GL(K)` act by Fisher–Rao isometries? **Yes — for the declared action.**

The declared law action is the pushforward `\widehat ρ_b(g)q = (ρ_b(g))_# q`
(`02:88-94`, `eq:geo-pushforward-actions`), which for `ρ_b(g)x = Ax` gives
`(μ,Σ) ↦ (Aμ, AΣAᵀ)`. `PIFB2.tex:1102` uses exactly this ("transported moments
`(Ω_{ij}μ_j, Ω_{ij}Σ_jΩ_{ij}ᵀ)`"), and `02:434-441` (`prop:geo-moment-pushforward`,
`eq:geo-precision-inverse-congruence`) types it.

*Verification* (`c2_gauss.py`, `K=4`, 200 random `(μ,Σ,A)` per row, max relative discrepancy of
the Fisher quadratic form):

| action on `(μ,Σ)` | max rel. Fisher discrepancy | verdict |
|---|---|---|
| `(Aμ, AΣAᵀ)` — declared pushforward | `7.649e-15` | **isometry** |
| `(Aμ+b, AΣAᵀ)` — affine | `5.998e-15` | **isometry** |
| `(Aμ, Σ)` — mean-only `GL` | `6.319e+00` | not an isometry |
| `(μ, AΣAᵀ)` — covariance-only | `1.317e+01` | not an isometry |
| `Σ⁻¹μ ↦ Σ⁻¹μ+v`, `Σ` fixed — natural-parameter tilt | `2.187e+01` | not an isometry |

So the answer to the assignment's central question is: **the implementation's group acts by
isometries, provided the action is the full congruence.** The three failure modes are the
family-preserving diffeomorphisms that are *not* sample-space pushforwards. They are not
hypothetical: the natural-parameter tilt is the canonical exponential-family group action, and it
is exactly the action that makes a fiber a torsor (§2). Two of them appear in the literature the
roadmap draws on.

**The precise hypothesis the roadmap needs is already in the corpus.** `hyp:pb-regular-models`
(`05c:30-46`) requires that "the represented action `\widehat ρ_x(g)` is induced by a
parameter-independent bimeasurable change of sample coordinates and preserves `ℬ_x`", and
`prop:pb-statistical-tensor-descent` (`05c:59-88`) *proves* from that hypothesis that the action
preserves `g^F` and the Amari–Chentsov tensor and that both descend to the associated bundle. That
proposition explicitly flags the hypothesis as load-bearing (`05c:84-87`: "Closure of a set of
parameter values under an arbitrary diffeomorphism of its parameter chart would not prove
statistical isometry"). The roadmap's line 48 phrase "induced by declared probability-law
transformations" admits an arbitrary diffeomorphism of `ℳ` and therefore does **not** imply what
T2 needs. **Finding K6 (STRUCTURAL, one-line fix):** replace line 48 with the corpus hypothesis and
cite `05c:37-41` and `05c:59`.

### 1.3 Lemma: divergence invariance already forces Fisher isometry — the "transform covariantly" escape is empty

**Lemma 1.3.** Let `ℳ` be a regular statistical manifold and `D` a divergence with the standard
second-order expansion `D(p‖γ(t)) = ½t²g^F_p(γ̇,γ̇) + O(t³)` (KL has it; this is the definition of
Fisher as the Hessian of the divergence). If `Φ ∈ Diff(ℳ)` satisfies `D(Φa‖Φb) = D(a‖b)` for all
`a,b`, then `Φ*g^F = g^F`.

*Proof.* Fix `p` and `u ∈ T_pℳ`, take `γ(t)` with `γ(0)=p`, `γ̇(0)=u`. Both sides of
`D(Φp‖Φγ(t)) = D(p‖γ(t))` are `C²` in `t` and vanish to first order; equating the second
derivatives at `t=0` gives `g^F_{Φp}(TΦu,TΦu) = g^F_p(u,u)`; polarise. `∎`

*Numerical check* (`c2_gauss.py`, `K=4`): `KL(p‖p+tv)/(t²/2) = 1.3733916406` against
`g^F(v,v) = 1.3729979106` at `t=10⁻³`, agreeing to `O(t)` as required.

**Consequences for the roadmap.**

1. The disjunction at line 48 is not a disjunction. If `𝒮`'s divergence sectors — which carry the
   bulk of its content — are gauge-invariant, then `ρ(G) ⊆ Isom(ℳ,g^F)` and the Dirichlet sector's
   invariance is automatic. Conversely, an action that distorts `g^F` also distorts `D`: for the
   Gaussian mean-only `GL` action, `KL` moves by `3.19e-01` relative; for the natural-parameter
   tilt by `2.85e-01`; for the categorical tilt, `KL(a‖b)=0.24187` becomes `0.22994` while a
   permutation reproduces `0.24187029026937165` against `0.24187029026937168` (§9, C1d).
   **There is no sector in which a non-isometric `ρ` is safe.**
2. The converse inclusion is strict, which matters for T0's classification. The full hierarchy,
   with a verified strictness witness at each step (`c11_hier.py`):

   ```
   {sample-space pushforwards} ⊆ {D-isometries} ⊆ {Fisher-Rao isometries} ⊆ {family-preserving diffeos}
   ```

   For `Δ_n` all four coincide with `S_{n+1}` at the first three positions and the last is
   infinite-dimensional (tilting: pullback metric differs by Frobenius norm `2.658`). For MVN(1),
   the elliptic `PSL(2,ℝ)` element (`θ=0.7`) is a Fisher isometry (discrepancy `8.2e-06`, at
   finite-difference accuracy) but **not** a KL isometry (discrepancy `9.773`), while the affine
   control is a KL isometry to `1.1e-14`. So `{Fisher} ⊋ {D-isometries}` strictly. **T0 must say
   which of the three it is declaring.** The safe and provable choice is the first.

### 1.4 The multi-family requirement is not satisfiable with one positive-dimensional `G` — K2, FATAL

Combining §1.1a and Lemma 1.3:

> **Proposition.** Let `ℳ_q` be the interior of the `n`-simplex with its Fisher metric and let `G`
> be a connected Lie group acting on `ℳ_q` so that `𝒮`'s divergence sectors are gauge-invariant.
> Then `ρ_q(G) ⊆ S_{n+1}` and, `G` being connected, `ρ_q` is trivial.

What survives on a categorical backend with a **finite** structure group `Γ ⊆ S_{n+1}`:

- `P → 𝒞` is a covering space; `Aut_Γ(P)` is discrete; there is a **unique** connection and it is
  flat. `A` is not a variational field and `F_A ≡ 0` identically, for every base dimension.
- `D^A q` is the ordinary derivative in a locally constant trivialization, so the Dirichlet sector
  `η_q∫‖D^Aq‖²_{g^F}` survives and is gauge-invariant.
- `ℳ_q/Γ` is the ordered simplex, of full dimension `n`, so escape (E-a) holds trivially and the
  theory is non-vacuous — but for a reason that has nothing to do with gauge structure.

So a categorical backend is a legitimate instance of T0–T4 and a **degenerate** instance of T2 and
T7: it cannot distinguish the gauge theory from a plain consensus model on `ℳ_q`. This directly
defeats the stated purpose of E0 (line 131: "Is the reduction independent of a hidden Gaussian
assumption?"), of WP1's exit gate (line 147: "At least two nonisomorphic statistical families
instantiate the hypotheses"), and of line 162 ("A categorical or other non-Gaussian backend should
be added early to prove that the architecture, tests, and theorem statements do not silently depend
on Gaussian formulas"). They will pass — and the passing will be uninformative, because the gauge
sector is empty on one arm.

**Required repair.** Either (i) restate the multi-family gate as *"at least two non-isomorphic
statistical families each with a positive-dimensional Fisher-isometry group"* and produce a second
such family (candidates: the location-scale family of an elliptical model, `SPD(K)` with the
affine-invariant metric under `GL(K)` congruence, the von Mises–Fisher family under `SO(K)`, or a
product of Gaussian fibers with a block-diagonal `G`) — or (ii) accept a *family-dependent*
structure group `G(ℳ)`, in which case T0 must be restated with `G` as a function of the fiber and
T7's "recover `GL(K)` attention" becomes a Gaussian-only statement. Option (i) is much better and is
achievable: `SPD(K)` under `GL(K)` congruence is the natural second family and is already in the
project's orbit.

### 1.5 The curvature sector is not gauge-invariant for `G = GL(K,ℝ)` — K1, FATAL

`κ∫_𝒞‖F_A‖²dμ` (line 99) requires two contractions: a base cometric on the two form indices
(the roadmap correctly flags this at line 32) **and** an inner product on the Lie algebra `𝔤` for
the value index. Under a gauge transformation `F_A ↦ Ad_g F_A`, so gauge invariance of the term
requires that inner product to be `Ad`-invariant.

*Computation* (`c5_holonomy.py`, exhaustive linear solve for symmetric `B` on `gl(K,ℝ)` with
`B([Z,X],Y)+B(X,[Z,Y])=0` for all `Z`, plus a `61×61` grid search over combinations):

```
gl(2,R): dim{Ad-invariant symmetric bilinear forms} = 2   (span: tr(XY), tr X tr Y)
    signature of tr(XY): 3 positive, 1 negative  => INDEFINITE
    any positive-definite combination a*tr(XY)+b*trX trY ?  -> NONE
gl(3,R): dim = 2;  signature of tr(XY): 6 positive, 3 negative;  positive-definite combination: NONE
```

This is the expected structural fact — a Lie algebra carries an `Ad`-invariant inner product iff
the group is of compact type — but it is worth having it computed, because the consequence for the
roadmap is exact and severe:

> For `G = GL(K,ℝ)` with `K ≥ 2`, the term `κ∫‖F_A‖²dμ` is **either** gauge-invariant and
> indefinite (built from `tr(F∧⋆F)`, hence unbounded below, destroying T4's direct method and
> T6's dissipation argument), **or** positive and gauge-non-invariant (built from the Frobenius
> norm, which is invariant only under `O(K)` conjugation — i.e. it is a gauge-fixing term to
> `O(K)`, exactly as line 160 already says of the frame-smoothness term).

**T2 and T4 are inconsistent for the showcase group.** The repair is one of:
(a) declare `G` compact or of compact type in **T0**, not as an analytic hypothesis in T4 —
this contradicts line 13's "Compactness of `G` … may be imposed in the first existence theorem as
analytical hypotheses, not as ontological commitments";
(b) take `G = SO(K)` or `O(K)` for the Gaussian fiber, at the cost of shrinking `ℳ_q/G` (the
covariance sector's `GL`-invariant `r` degenerates and the invariant content grows — this is
*good* for §2, and it is the option I recommend);
(c) drop the curvature sector and adopt wave 2 §1.7's proposal instead — put `ω` into the theory as
the existence obstruction for an `ω`-parallel background section, where holonomy is the exact
obstruction, rather than as a term in the energy.

Note the corroboration: audit finding **RG-7** independently records that
`PIFB2.tex:1559,1575,1644,1804` asserts gauge equivariance of a barycenter construction by citing a
theorem that assumes `G` compact while the actual group is `GL⁺(K_q)`. That is the *same*
noncompactness biting in a second place. It will keep biting until `G`'s type is declared in T0.

### 1.6 What line 48 should say

```
ρ_q, ρ_s are declared as homomorphisms G → Aut(𝖪,𝒦) resp. Aut(𝖬,𝓜) into the groups of
bimeasurable, parameter-independent sample-coordinate automorphisms preserving ℳ_q, ℳ_s;
the induced law actions are the pushforwards ρ̂_x(g)q = (ρ_x(g))_# q.  By
prop:pb-statistical-tensor-descent (05c:59) these preserve g^F_x, 𝒯_x, and every f-divergence,
and descend to the associated bundles.  The maximal such G is Isom(ℳ_x,g^F_x), which is
Aff(K,ℝ) for the Gaussian fiber with K ≥ 2 and S_{n+1} for the categorical fiber; a fiber
admitting no positive-dimensional isometry group admits no nondiscrete gauge structure.
G is further required to be of compact type wherever ‖F_A‖² appears.
```

---

## 2. The torsor problem, and the non-transitivity axiom T0 needs

### 2.1 Verification of wave 2's Gaussian quotient

Wave 2 `Corollary A3.5` (`wave2-01:280-294`) computes `ℬ_b/G ≅ [0,∞)` for the full Gaussian fiber
under `GL⁺(K)`, `K ≥ 2`, parameterised by `r(μ,Σ) = (μᵀΣ⁻¹μ)^{1/2}`.

**Confirmed, independently** (`c4_quotient.py`):

```
invariance of r² over 500 random (μ,Σ,A) ∈ GL⁺(4):  max rel. discrepancy 4.097e-12
transitivity on level sets, explicit A*:
   K=2  r1=0.277621 r2=0.277621  det A* = +0.7703  ||A*μ1−μ2||=2.0e-16  ||A*Σ1A*ᵀ−Σ2||=2.1e-15
   K=4  r1=0.570541 r2=0.570541  det A* = +2.3395  ||A*μ1−μ2||=1.0e-15  ||A*Σ1A*ᵀ−Σ2||=1.1e-14
```

Construction of `A*`: `Σ^{-1/2}` normalises the covariance and `SO(K)` (transitive on spheres for
`K ≥ 2`, and inside `GL⁺`) rotates `Σ^{-1/2}μ` to `r e_1`. For `K=1`, `GL⁺(1)=ℝ_{>0}` gives the
signed invariant `μ/σ ∈ ℝ`; the full `GL(1)` gives `|μ|/σ ∈ [0,∞)`.

**What it means.** Under a single-section, fixed-background reading of gauge invariance, the entire
invariant content of a Gaussian belief at a context is *one nonnegative number*: the Mahalanobis
norm of its mean. The direction of the mean and the whole shape of `Σ` are pure gauge. Escape
(E-a) is technically available and practically almost empty.

### 2.2 The escape the roadmap actually has, and A-NOGO's real scope

Theorem A-NOGO (`wave2-01:29-40`) is stated for `𝓕_μ[s] = ∫f(c,s(c),D^ω s(c))dμ(c)` — **one**
section. Corollary A3.4 (`wave2-01:268-278`) concludes constancy because `Γ(𝒞,ℰ_b)` is a *torsor*
under `Aut_G(P)`. The roadmap's action (lines 74–102) is a functional of `4|V|` sections plus link
fields plus a connection, all acted on by **one** `Aut_G(P)`. That diagonal action is not
transitive as soon as `|V| ≥ 2`, and the failure of transitivity is quantitative:

*Computation* (`c4_quotient.py`, `K=4`, linearised stabiliser `{X ∈ gl(K) : Xμ_i = 0,
XΣ_i + Σ_iXᵀ = 0 ∀i}` by SVD rank):

| `N` agents at one context | `dim ℬ^N` | `dim gl(K)` | `dim` stabiliser | `dim` quotient |
|---|---|---|---|---|
| 1 | 14 | 16 | 3 | **1** (= the `r` of §2.1) |
| 2 | 28 | 16 | 0 | **12** |
| 3 | 42 | 16 | 0 | **26** |
| 8 | 112 | 16 | 0 | **96** |

And on wave 2's own torsor tier (`ℬ = {N(m,Σ_0)}`, `G=(ℝ^K,+)`, `K=4`):

| `N` | `dim ℬ^N` | orbit dim | quotient dim |
|---|---|---|---|
| 1 | 4 | 4 | **0** — A-NOGO applies, invariants are constant |
| 2 | 8 | 4 | **4** — the differences `m_i − m_j` are invariant |
| 5 | 20 | 4 | **16** |

**This is the correct and complete answer to the assignment's item 2:** the roadmap's escape from
A-NOGO is not primarily the generality of its statistical manifolds. It is the *plurality of its
sections*. A torsor fiber is fine; a torsor fiber with one section is not. `𝒮`'s peer sector
`D_q(q_i‖L^q_{ij}q_j)` and its self sector `D_q(q_i‖p_i)` are relative quantities and are therefore
exactly the invariant content. The observation sector `ℒ^{obs}_i` is invariant **only if** the
likelihood data are declared as a section of the associated function bundle,
`E_β(c) = E_α(c)∘ρ_b(g_{αβ}(c))` (wave 2 §1.1, `eq:gen-gauge-pushforward-obs` at `04:394-398`);
if declared per-chart it breaks invariance — wave 2's CHECK B4 measures the break at `192.94`.

### 2.3 The axiom, written out

> **T0(A-NT) — non-degeneracy of the gauge quotient.** Let
> `Φ = (q_i,p_i,s_i,r_i,χ_i,L^q_{ij},L^s_{ij},A,E^{obs}_i)_{i∈V}` be the full field tuple and let
> `𝒢 = Aut_G(P)` act diagonally by its declared laws (§4). Declare:
> **(i)** every field that enters `𝒮` and is not a base scalar is a *section*, not a fixed chart
> datum; **(ii)** `𝒮` descends to `Φ/𝒢`; **(iii)** exhibit a generating set of `𝒢`-invariants and
> a lower bound `dim(Φ/𝒢) ≥ …` witnessing non-vacuity, together with the single-agent orbit space
> `ℳ_q/G` and the diagonal orbit space for `|V| ≥ 2`.
> For the Gaussian fiber with `G = GL⁺(K)`: `ℳ_q/G ≅ [0,∞)`; the diagonal quotient over `N` agents
> has dimension `N·K(K+3)/2 − K²` for `N ≥ 2` and the invariants are generated by
> `μ_iᵀΣ_j^{-1}μ_k` and the spectra of `Σ_i^{-1}Σ_j`.

### 2.4 Corollary for T4 — K7, STRUCTURAL

T4 (line 116) proposes the direct method with "coercive bounds, weak compactness, strong `L²`
convergence, closed target constraints, and weak lower semicontinuity". None of that survives a
gauge-invariant functional: `𝒮` is constant on `𝒢`-orbits, `𝒢 = C^∞(𝒞,G)` is infinite-dimensional
and, for `G = GL(K,ℝ)`, noncompact. A minimising sequence can drift along its own gauge orbit to
infinity in the `H¹` norm while `𝒮` stays bounded, so coercivity in `H¹` is **false** as stated.
This is the classical Yang–Mills situation and its resolution is standard: minimise on the
quotient, or impose a gauge-fixing condition with a slice theorem (Coulomb/Uhlenbeck gauge). T4's
hypothesis list contains no such item. Adding a gauge-fixing hypothesis is the minimum; a slice
theorem for `Aut_G(P)` acting on manifold-valued `H¹` sections is a real research obligation and
should be its own line in the theorem table.

---

## 3. Connection versus transition versus link (line 66)

### 3.1 Clause-by-clause verification — the roadmap is right on all four, and this is a genuine repair

Line 66 reads: *"A local gauge frame is a local section `u_i:U_i→P`. On `U_i∩U_j`, the transition
function between `u_i` and `u_j` is a change of coordinates, not automatically a physical
interaction. If `Ω_{ij}` is only the representation of this transition, then it is pure gauge
bookkeeping and has cocycle consistency. Intrinsic comparison of two sections in the same
associated fiber needs no additional physical transport. Nontrivial relational physics requires one
of two extra structures: a connection `A` … or an independent overlap/link automorphism `L_{ij}` …
The specialization `Ω_{ij}=U_iU_j^{-1}` is the flat coboundary case and cannot generate nontrivial
cycle holonomy by itself."*

| clause | verdict | evidence |
|---|---|---|
| local gauge frame = local section `u_i:U_i→P` | **correct, with an unstated hypothesis** | `02:40-53` `def:geo-principal-systems`; existence requires `P\|_{U_i}` trivializable — audit **G3** transfers verbatim (K13) |
| transition function is a coordinate change, not an interaction | **correct** | `02:449-483` `sec:geo-regime-one`, `eq:geo-frame-comparison` (`02:457`), gauge law `eq:geo-regime-one-gauge-law` (`02:465`): "The comparisons are same-point changes of coordinates. They involve no curve and no connection." (`02:481-483`) |
| cocycle consistency | **correct** | `eq:geo-cech-cocycle` (`02:502`): `T_{ii}=e`, `T_{ji}=T_{ij}^{-1}`, `T_{ij}T_{jl}=T_{il}` |
| intrinsic comparison in one fiber needs no transport | **correct and load-bearing** | Two sections evaluated at the same `c` live in the same fiber `(ℰ_q)_c`; the transition appears in the *coordinate formula* and cancels from the *value*. If `q_i,q_j` are two representatives of **one** section the divergence is identically `0` — which is exactly what `PIFB2.tex:208` contradicts (see below) |
| relational physics needs `A` or an independent `L_{ij}` | **correct** | `02:557-622` `def:geo-graph-links` types `Θ_e` independently: "Neither is determined by the other, by `h_i`, … or by a principal connection" (`02:586-588`) |
| `Ω_{ij}=U_iU_j^{-1}` is the flat coboundary case, no cycle holonomy | **correct, and it is a theorem** | proved below and at `prop:geo-trivializing-criterion` (`02:605-620`); `hyp:geo-flat-links` (`02:646-658`, `eq:geo-flat-regime` `02:653`) states "This excludes represented graph holonomy in either channel" |

**This paragraph fixes a real error, and the referee should say so plainly.** `PIFB2.tex:208`
declares `Ω_{ij}=U_iU_j^{-1}` "the transition function" satisfying the Čech cocycle condition, then
in the *same paragraph* writes: *"in the dynamics the agent beliefs `q_i` are distinct sections
compared within a common frame, with `KL(q_i‖Ω_{ij}q_j)>0` generically, so `Ω_{ij}` enters as a
transport operator between agents rather than as a gluing map"*. Those are incompatible readings of
one symbol, and the same manuscript at `PIFB2.tex:142` correctly notes that Regime I has `F ≡ 0` by
Maurer–Cartan. `Theory/02` repairs this by typing `T_{ij}` (`02:449-483`) apart from `Θ_e`
(`02:557-622`); the ultradeep audit calls it "the most valuable repair the rewrite has achieved so
far" (`audit-01-geometry.md:306-312`) and "the rewrite's single most valuable contribution"
(`2026-08-11-ultradeep-expert-audit.md:211`). **Line 66 imports that repair into the roadmap
correctly and independently. It should be credited, and it should cite `02:449-483` and
`02:557-622` so that the repair is traceable rather than rediscovered.**

Line 160 is a second, independent correct repair, and deserves the same credit: "Its
fixed-connection, attention-free covariant Markov-field term is identified as a closed-ELBO member,
whereas the attention-weighted neighbor term is an effective consensus regularizer. Its
frame-smoothness term is gauge fixing. Its frame-derived connection is pure gauge, while nontrivial
curvature requires independent link data." Every clause matches `Theory` and the audits
(`02:646-658`; `PIFB2.tex:142`; `audit-01-geometry.md:204-208`). This is the correct classification
and it is stated more crisply here than anywhere in the parent corpus.

### 3.2 Are `L_{ij}` and `A` independent data? — K4, STRUCTURAL

The roadmap's action uses **both** `L^q_{ij}, L^s_{ij}` (line 72, lines 87 and 93) and `A` (line 72,
lines 97–99). It never states their relationship. Three observations, in order of increasing
importance.

**(i) `L_{ij}` is not parallel transport, and cannot be.** The peer integrals are
`∫_{U_i∩U_j} χ_{ij}[β_{ij}D_q(q_i‖L^q_{ij}q_j)]dμ` — both arguments evaluated at the **same** base
point `c`. Parallel transport along a path from `c` to `c` is the holonomy of that loop; along the
constant path it is the identity. So `L_{ij}(c)` is a *vertical* automorphism of the single fiber
`(ℰ_q)_c` — a Higgs-type field, not a transport. The naive compatibility guess ("`L_{ij}` =
parallel transport along a chosen path, up to a link field") is therefore **not** the right axiom;
if imposed literally it would force `L_{ij} = id` and kill the peer sector.

**(ii) Gauge covariance does not constrain them at all.** With `L^q_{ij} ↦ ρ̂(g(c))L^q_{ij}ρ̂(g(c))^{-1}`
(`Ad`-covariance; `eq:geo-regime-two-gauge-law` at `02:576` is the discrete form) and
`A ↦ Ad_g A + g\,dg^{-1}` (`eq:geo-local-connection-b` at `02:319`), *each term of `𝒮` is separately
invariant*. I verified the peer sector's invariance and the fire of two controls
(`c7_e1.py`, `K=3`, `N=5` agents):

```
S_peer                                = 15.4986532302
correct co-transform (L -> g L g^-1)  rel.dev = 6.304e-15
control A: L NOT transformed          rel.dev = 1.239e+00
control B: wrong law L -> g L g^T     rel.dev = 9.382e-01
control C: ρ = mean-only, L correct   rel.dev = 1.713e+00
```

So gauge covariance is **silent** on the `L`–`A` relationship. The roadmap cannot get the axiom for
free from T2.

**(iii) The consequence of leaving them independent, and the axiom that is already written.**
Independent `L` and `A` give the theory **two unrelated holonomies**: a graph holonomy
`H(γ)=∏Θ_{e_a}` on cycles of the interaction graph (`eq:geo-link-holonomy`, `02:592`) and a base
holonomy of `A` on loops in `𝒞`. `Theory` says exactly this and says it once: *"Without the curve
assignment and these equalities, graph holonomy and base-connection holonomy are unrelated."*
(`02:642-645`). The bridge is `hyp:geo-graph-base-transport` (`02:625-640`,
`eq:geo-link-pt-hypothesis` `02:632`): choose contexts `c_i ∈ 𝒞_i` and curves `γ_e` from `c_j` to
`c_i` and impose `ρ̂_b(Θ^b_e) = Ω_{γ_e}`. It is tagged `HYPOTHESIS` and, per audit **G2**
(`audit-01-geometry.md:76`), it has **zero references anywhere in the corpus**.

> **Missing axiom for T0 (K4).** Declare, once, which of three regimes holds:
> **(L1) `L_{ij}` induced by `A`** — `hyp:geo-graph-base-transport` (`02:625-640`) with a declared
> context assignment `c_i` and curve assignment `γ_e`; then graph holonomy = represented base
> holonomy, the curvature sector has a physical consumer, and E2's two arms are one experiment.
> **(L2) `L_{ij}` independent** — then `𝒮` carries two holonomies and T5's variation must be taken
> in both; E2 must say which it is measuring; and the theory owes a statement of why the redundancy
> is not double counting.
> **(L3) `L_{ij}` `A`-parallel** — `D^AL_{ij}=0` on `U_i∩U_j`; existence of such an `L` is
> obstructed by the holonomy of `A` restricted to `U_i∩U_j` (a fixed-point condition for the
> holonomy group acting by `Ad`). This is the strongest and most interesting option and it is the
> exact analogue of wave 2 §1.7's proposal for the background section (`wave2-01:534-551`).
>
> The roadmap says none of these. T0's closure obligation ("every law, divergence, measure, random
> variable, and transformation is typed") is **not met** until it does.

---

## 4. T2: the corrected statement — K5, STRUCTURAL

T2 currently reads (line 114): *"Minimum hypotheses: One passive local gauge action applied to
sections, likelihood data, comparison maps, and connections. Closure obligation: Prove invariance of
`𝒮`, equivariance of its differential, and invariance of observables. Separate coordinate
transitions, gauge fixing, and physical link fields."*

Three distinct statements are compressed into "invariance of `𝒮`", and they have different truth
values.

- **(T2a) passive well-definedness.** `𝒮` is independent of the choice of local trivialization.
  **True in complete generality**, proved at the *measurable* tier by wave 2 §1.2
  (`wave2-01:164-219`), with no smoothness, no connection, no Lie structure, no finite
  dimensionality. For the jet sector it is `thm:pb-pullback-gauge-invariance` (`05c:124-145`).
- **(T2b) active equivariance on the full tuple.** `𝒮[F·Φ] = 𝒮[Φ]` for `F ∈ Aut_G(P)` acting on
  **every** field simultaneously. **True**, wave 2 Proposition A3.1 (`wave2-01:238-241`, verified
  residual exactly `0.0`), and verified here for the peer and Dirichlet sectors at `6.3e-15` and
  `6.4e-16`.
- **(T2c) active invariance at fixed background.** `𝒮[F·s;π,E] = 𝒮[s;π,E]` with `π,E` held fixed.
  **False** — wave 2 Proposition A3.2 (`wave2-01:243-250`, witness `1.9606` vs `2.9274`), and the
  active/passive counterexample is already in the corpus at `05c:146-154`.

**T2 must ask for (T2a) and (T2b) and must explicitly disclaim (T2c),** recording that the
background data therefore carry a gauge fixing, which is precisely wave 2's obstruction O1
(`wave2-01:478-486`).

**The exact co-transforming list.** Writing `g:𝒰→G` for the frame change (passive) or
`k:𝒞→G` for the automorphism's local function (active), with `ρ̂_x(g)` the pushforward law action:

| object | type | transformation law | source |
|---|---|---|---|
| `q_i,p_i` | `Γ(ℰ_q\|_{U_i})` | `β ↦ ρ̂_q(g)^{-1}β` | `eq:geo-local-reframing` `02:157` |
| `s_i,r_i` | `Γ(ℰ_s\|_{U_i})` | `β ↦ ρ̂_s(g)^{-1}β` | idem |
| `L^q_{ij}, L^s_{ij}` | fiber automorphisms over `U_i∩U_j` | `L ↦ ρ̂(g_i) L ρ̂(g_j)^{-1}`; with one bundle and one gauge function, `L ↦ Ad_{ρ̂(g)}L` | `eq:geo-regime-two-gauge-law` `02:576` |
| `A` | `Ω¹(𝒰,𝔤)` | `A ↦ Ad_{g^{-1}}A + g^{-1}dg` | `eq:geo-local-connection-b/m` `02:319/322` |
| `F_A` | `Ω²(𝒰,Ad P)` | `F ↦ Ad_{g^{-1}}F` | requires an `Ad`-invariant norm — see §1.5 |
| `E^{obs}_i` (likelihood/energy data) | section of `P×_{ρ^*}ℳ(𝖪)` | `E ↦ E∘ρ_q(g)` | `eq:gen-gauge-pushforward-obs` `04:394-398` |
| `π^q_{ij}, π^s_{ij}, τ_q, τ_s, β_{ij}, γ_{ij}` | base scalars / simplex-valued | **invariant** | — |
| `χ_i, χ_{ij}` | base scalars | **invariant** | — |
| `μ`, base cometric | base data | **invariant**; frames do not touch them | wave 2 §1.2 Step 4 |
| `δ𝒮/δq_i` | *cotangent* | `∇ ↦ ρ̂(g)^{-*}∇`, i.e. `g^{-T}` in the linear realization | verified §6.1 |

The last row is a trap and E1 must respect it: comparing the transformed gradient against the
*tangent* law rather than the cotangent law produces a false alarm on correct code. Measured
(`c7_e1.py`): `‖∇' − g^{-T}∇‖/‖∇‖ = 1.594e-09` (correct, at finite-difference accuracy) versus
`‖∇' − g∇‖/‖∇‖ = 3.244e+00` (naive law).

**Corrected T2.**

> **T2 (gauge covariance).** *Hypotheses:* T0 with `ρ_x` declared as in §1.6; the co-transformation
> table above declared for every field; `G` of compact type wherever `‖F_A‖²` appears.
> *Obligations:* (a) prove **passive well-definedness** of every sector under change of local
> trivialization, at the measurable tier where possible; (b) prove **active equivariance** of `𝒮`
> under the simultaneous `Aut_G(P)`-action on the full tuple `Φ`, sector by sector, and equivariance
> of `δ𝒮` with the cotangent law; (c) **disclaim** active invariance at fixed background, exhibit
> the orbit-space classification (`wave2-01:255-266`, Theorem A3.3) saying what an invariant
> functional could have been, and record that the declared background is a gauge fixing;
> (d) exhibit the invariant content per (A-NT); (e) prove that `Ω_{ij}` never appears except as a
> coordinate cancellation, and that the physical content of the link sector is the conjugacy class
> of `H(γ)=∏Θ_{e_a}` (`02:592`).

---

## 5. T7: the zero-dimensional reduction

### 5.1 The derivative and curvature sectors — the roadmap is right, and for one more reason than it gives

With `𝒞={*}` and `d=0`: `T_*𝒞 = {0}`, so `Ω¹({*},𝔤)=0` and `Ω²=0`. Hence

- `A ≡ 0` is the only 1-form, so `F_A ≡ 0` and `κ∫‖F_A‖²dμ = 0`. ✔
- `D^A q = ver^A ∘ Tq : T_*𝒞 → V ℰ_q` is the zero map from the zero space, so `‖D^Aq‖²_{g^F}=0`
  and `η_q∫‖D^Aq‖² = 0`. ✔ Note this is stronger than "the connection drops out": *the covariant
  derivative has no domain*. There is no residual weak form.
- `μ({*})=1` turns `∫…dμ` into evaluation. ✔
- The base-cometric obligation of line 32 evaporates, since there are no form indices to contract.
  Worth saying: T7 is the **only** point in the roadmap where line 32's missing declaration is not
  needed, which is why the `d=0` intuition felt complete.

**So the first clause of T7 is correct.** But the reduction does something the roadmap does not
mention and should:

> **T7 destroys the local gauge group.** `Aut_G(P)` over a point is `C^∞({*},G) = G`: a *global*
> (rigid) symmetry, not a local one. Every statement T2 makes about *local* gauge covariance is
> untestable at `d=0`. In particular the connection's inhomogeneous transformation term
> `g^{-1}dg` is identically zero, so a code that implements only `A ↦ Ad_{g^{-1}}A` passes every
> `d=0` test (verified: relative deviation exactly `0.000e+00`, §6.1). **T7 is therefore not an
> exactness certificate for the gauge sector**, and E1 must not be run only at `d=0`.

### 5.2 Overlaps and the support field

With `𝒞={*}`, each `U_i ⊆ {*}` is `∅` or `{*}`. Agents with `U_i=∅` carry the empty section and drop
out. Every surviving pair therefore satisfies `U_i∩U_j = {*} ≠ ∅`: **the interaction graph is
complete.** That is the intended PIFB2 configuration (dense all-to-all attention), so the reduction
is sound — but it forces a declaration the roadmap has not made:

- If `χ_{ij}` is **derived** from the overlap (`χ_{ij} = 1_{U_i∩U_j≠∅}` or `χ_iχ_j`), then at `d=0`
  it is identically the all-ones mask and *cannot* express a causal or sparse attention mask. The
  transformer limit T7 targets is then the encoder (bidirectional) case only.
- If `χ_{ij}` is **independent declared data**, then at `d=0` it is exactly the attention mask, and
  the causal mask of a decoder-only transformer is recovered as `χ_{ij} = 1_{j≤i}`. This is a nice
  result and the roadmap should claim it.

`χ_i` at `d=0` degenerates to a per-agent nonnegative scalar weight — an agent-presence/importance
mask. It does no topological work (there is no locality to encode) but it is not inert. **T0 must
declare whether `χ_{ij}` is derived from `(χ_i,U_i∩U_j)` or independent.** (TECHNICAL.)

### 5.3 The second clause: exactly which assumptions the `GL(K)`-attention specialization needs

T7 says "Recover `GL(K)` attention only as a specialization with additional representation and
statistical-family assumptions." Correct in spirit; here is the complete list, from
`PIFB2.tex:1137-1147` (`thm:transformer_recovery`) plus what is needed to reach it, cross-checked
against `audit-02-infogeometry.md:73` and `audit-06-pifb2-gap.md:378-386`.

**Family and representation assumptions (not implied by T0):**

- **(F)** `ℳ_q = {N(μ,Σ) : μ∈ℝ^{d_k}, Σ∈SPD(d_k)}` — a Gaussian fiber.
- **(Rep)** `ρ_q` is the defining representation of `GL(d_k)` on the sample space, `ρ_q(g)x = gx`,
  with the pushforward law action `(μ,Σ) ↦ (gμ, gΣgᵀ)` (`02:88-94`, `02:434-441`).
- **(D)** `D_q = KL` specifically, not a general divergence: the closed-form score at
  `PIFB2.tex:1099-1103` is the Gaussian KL and no other `f`-divergence gives it.
- **(τ)** `τ_q = 1`. `audit-06-pifb2-gap.md:381-383` records that the tie
  `R_{ij}=Ω_{ij}Σ_jΩ_{ij}ᵀ` forces `τ=1`, so the deployed operating point `τ=κ√{d_k}` is **not**
  an exact coordinate of the reduction.
- **(V)** a source-only value map `W_V` for the value aggregation (`PIFB2.tex:1146`).

**PIFB2's own four reductions, verbatim (`PIFB2.tex:1141-1144`):**

- **(R1)** Isotropic shared covariances `Σ_i = σ²I` for all `i`, `σ²>0` held finite in the joint
  scaling limit.
- **(R2)** Shared frames `U_i=U`, hence trivial pairwise transport `Ω_{ij}=I`. PIFB2 explicitly
  notes that the weaker `Ω_{ij}∈O(d_k)` "removes only the geometric bias `S(Ω_{ij})` and does not
  suffice for the cross-term reduction".
- **(R3)** A separately learned shared bilinear `M=σ²W_QW_Kᵀ ∈ GL(d_k)` **replacing** the cross
  term, "an object external to the gauge data".
- **(N)** Key-norm constancy: `‖K_j‖` constant in `j`, or the residual key bias absorbed into a
  learned per-key bias.

**The referee's addition, which T7 must state.** (R1) and (R2) are *not gauge-invariant conditions*;
they are **gauge fixings**. The isotropic slice `{Σ=σ²I}` is preserved exactly by the conformal
subgroup `ℝ_{>0}×O(d_k) ⊂ GL(d_k)`, not by `GL(d_k)`: `g(σ²I)gᵀ = σ²ggᵀ = σ²I` iff `g∈ℝ_{>0}·O(d_k)`.
And (R2) sets the transport to the identity. Therefore:

> **The `GL(K)`-attention specialization is exactly the limit in which the gauge structure is
> switched off.** (R2) trivialises the transport; (R3) supplies, from outside the theory, the object
> that the trivialised transport vacated; PIFB2's own fence F1 says so ("Hypothesis (R3) makes this
> a recovery, not a derivation", `PIFB2.tex:1146`). T7's second clause must therefore be worded so
> that recovering standard attention is **not** evidence for the gauge theory. `PIFB2.tex:1008` and
> `:98` are already careful; the roadmap should inherit that care verbatim.

Note also that the stronger, cleaner result the corpus already owns is not PIFB2's: `05b:547`
`prop:obs-attention-elbo` derives an **exact row softmax** `β*_{ij} ∝ π_{ij}exp(−c_{ij}/τ)` from a
latent source label inside a fixed normalized joint — a derivation, not a mean-field ansatz
(`audit-02` row 12; `audit-06:379-380`). T3 should cite it rather than re-derive it, and T7 should
route the attention recovery through it.

---

## 6. E1 and E2 as tests

### 6.1 Making E1 sharp

E1 (line 132) currently asks to "apply random local gauge transformations to all covariant inputs.
Require invariant action values and correctly transformed gradients; show separately that explicit
gauge fixing changes." As written this is **confirmatory**: it has no positive controls, no
sector decomposition, no mesh arm, and it does not specify that the gauge function must vary over
the base. I built the test that fires and measured what each variant detects.

*Setup* (`c7_e1.py`, `c10_mesh.py`): base `𝒞=[0,1]`, `K=3`, Gaussian fiber, `G=GL(3,ℝ)` by
congruence, a smooth section field `(μ(c),Σ(c))`, a `gl(3)`-valued connection `A(c)`, the Dirichlet
sector `∫‖D^Aq‖²_{g^F}dc` with `D^Aμ = μ' − Aμ`, `D^AΣ = Σ' − AΣ − ΣAᵀ` (the correct associated
covariant derivative for the congruence action; I verified `D^{A'}(gq) = Tρ̂(g)D^Aq` algebraically
and numerically). `S₀ = 6.94233283`.

```
perturbation                                            |dS|/S0, g'(c)≠0   |dS|/S0, g const
(P0) everything transformed correctly                   1.049e-05          6.397e-16
(P1) ρ = mean-only GL action (Σ NOT pushed forward)     1.696e+00          4.356e+00
(P2) connection law misses the inhomogeneous dg·g^-1    5.130e+00          0.000e+00
(P3) Fisher metric frozen at the untransformed Σ        1.166e+01          1.438e+02
```

**Four design requirements follow, and each of them is a defect in E1 as written.**

1. **The gauge function must be non-constant.** (P2) — a code that implements
   `A ↦ Ad_g A` and forgets `dg·g^{-1}` — is detected at `5.13` with `g'(c)≠0` and at **exactly
   zero** with constant `g`. A constant-gauge E1 is blind to the connection's defining property.
   This is the same fact as §5.1 and it means **E1 at `d=0` cannot test T2.**
2. **The residual must be reported as a function of mesh spacing.** The (P0) residual of `1.049e-05`
   is *not* a gauge violation; it is `O(h²)` truncation in the difference operator. Verified
   (`c10_mesh.py`):

   ```
     Nc      correct       broken-connection   broken-ρ(mean-only)
      200   1.659e-04     8.865e+00           3.216e+00
      400   4.091e-05     8.874e+00           3.210e+00  (ratio 4.05)
      800   1.018e-05     8.879e+00           3.207e+00  (ratio 4.02)
     1600   2.539e-06     8.881e+00           3.205e+00  (ratio 4.01)
     3200   6.343e-07     8.882e+00           3.204e+00  (ratio 4.00)
   ```

   Ratio `4.00` per halving confirms `O(h²)`; the two defects are `O(1)` and mesh-independent. A
   *fixed* tolerance conflates the two: at `Nc=200` a genuine `10⁻⁴`-scale gauge violation would be
   indistinguishable from truncation. **E1's acceptance gate must be "the residual decays at the
   discretization's order under refinement", not "the residual is below `ε`".** This also folds E1
   into E3 and makes E3's mesh study do double duty.
3. **The test must be run sector by sector, with the isometry-specific positive control.** The
   requirement that would actually fail if `ρ` were not by isometries is (P1)/(P3): replace the
   declared congruence by a *family-preserving but non-pushforward* action and require the residual
   to be `O(1)`. Two canonical controls, both of which fire:
   - **Gaussian control:** `(μ,Σ)↦(Aμ,Σ)` (mean-only `GL`) — Dirichlet residual `1.70`, peer
     residual `1.71`, and (by Lemma 1.3) both must fire, which they do.
   - **Categorical control:** exponential tilting `p ↦ p·e^θ/Z` — Fisher pullback differs by
     Frobenius norm `2.658`; `KL(a‖b)=0.24187` becomes `0.22994`. This is the *right* control for
     the categorical backend because tilting is the canonical `(ℝ^n,+)` action there.
   A single summed action value can cancel between sectors; per-sector reporting cannot.
4. **The gradient arm must use the cotangent law** (§4, last row) and should include the
   tangent-law comparison as a *deliberate false alarm* to prove the harness discriminates:
   `1.594e-09` (correct) versus `3.244e+00` (naive).

**Additional controls, all measured to fire:** `L_{ij}` left untransformed → `1.239`; `L_{ij}` given
the wrong law (`gLgᵀ` instead of `gLg^{-1}`) → `0.938`; background `π` or `E^{obs}` declared
per-chart rather than as a section → wave 2 measured `192.94` (`wave2-01:226-229`), which the
roadmap should reuse verbatim.

**Recommended E1 acceptance gate.** *For each sector `k` and each backend, report
`R_k(h) = |𝒮_k(g·Φ) − 𝒮_k(Φ)| / (|𝒮_k(Φ)| + s_k)` for a non-constant `g` with `‖log g‖ ≳ 1` at
three mesh resolutions; require `R_k(h) = O(h^p)` at the scheme's order `p`; require every one of
the six named controls to produce `R_k = O(1)` mesh-independently; require the gradient residual
under the cotangent law to be `O(h^p)` and under the tangent law to be `O(1)`; and report
`dim ρ(G)` and `dim ℳ_q/G` per backend so that a vacuous gauge sector cannot pass by being empty.*

### 6.2 E2: proving the coboundary arm is a control, not a tautology — and which arm can fail

**Proposition (E2's first arm).** Let `Ω_{ij}=U_iU_j^{-1}` with `U_i ∈ G`. Then for every closed
walk `γ = (i_1 → i_2 → … → i_r → i_1)`, `H(γ) = Ω_{i_1i_2}Ω_{i_2i_3}⋯Ω_{i_ri_1} = e`.

*Proof.* `(U_1U_2^{-1})(U_2U_3^{-1})⋯(U_rU_1^{-1}) = U_1U_1^{-1} = e` by telescoping. `∎`

This is `prop:geo-trivializing-criterion` (`02:605-620`) in the forward direction, and it is an
**algebraic identity**, not an empirical fact. *Verification:* max `‖H(γ)−I‖_∞` over 1800 random
closed walks of lengths 2–7 on 6 vertices with `K=3`: `3.409e-13` (`c5_holonomy.py`).

**Converse (which makes E2's second arm well-posed).** For a *connected* interaction graph, a link
assignment `{Θ_e}` has `H(γ)=e` for every closed walk **iff** `Θ_e = V_iV_j^{-1}` for some vertex
frames `V`. *Proof:* pick a spanning tree, set `V` at the root to `e`, transport along tree edges;
trivial holonomy makes the definition path-independent and forces every non-tree edge to agree.
This is the reverse direction of `prop:geo-trivializing-criterion` (`02:614-620`) verbatim.

**Therefore E2 is testing `H¹(graph; G) ≠ 0`.** The correct test is on a **basis of the cycle
space**, of rank `|E| − |V| + 1`, not on one loop. Measured on a 6-vertex, 8-edge graph
(cycle rank 3):

```
coboundary links  : fundamental-cycle deviations  1.65e-14, 1.28e-14, 2.14e-14
independent links : fundamental-cycle deviations  14.652,   162.447,  473.376
```

**Which arm can actually fail.**

- **Arm 1 (coboundary ⟹ trivial holonomy): can fail only on an implementation bug.** It is not a
  tautology *as a code test* — it is a strong one, because it catches exactly the two convention
  errors this project has a history of: the edge-ordering convention and the inverse convention.
  Audit **G8** (`audit-01-geometry.md:238-253`) records that under `Theory`'s ordering
  (`eq:geo-link-holonomy`, `02:592`, edges `e_a : i_{a+1}→i_a`, product left to right) the natural
  map `π_1 → G` is an **anti**-homomorphism unless `π_1` is given the opposite product, and that
  the descent proof (requiring `Θ_{\bar e}=(Θ_e)^{-1}`, declared at `02:566-569`) is never written.
  Arm 1 is precisely the test that fires on that error. It should be kept, and relabelled a
  *convention regression test* rather than a scientific control.
- **Arm 2 (independent links ⟹ controlled nontrivial holonomy): can genuinely fail, in two ways.**
  (a) The declared `Θ` may be cohomologous to a coboundary by accident — hence the cycle-basis
  requirement above. (b) **The action may be blind to holonomy even when holonomy `≠ e`.** This is
  the real risk and it is predicted by the parent corpus: audit **S3** finds the connections appear
  **zero times** in `04_generative.tex`, `05_elbo.tex`, `05b_local_collective_elbo.tex`
  (`2026-08-11-ultradeep-expert-audit.md:66-68`), and wave 2's Theorem A4.4(a) proves that
  finite-design consistency *forces* a jet-free integrand, i.e. forces the connection out
  (`wave2-01:385-398`, obstruction O2 at `wave2-01:488-493`).

**E2 therefore needs a third arm.** *Vary the holonomy conjugacy class of the independently declared
link (or of `A`) along a one-parameter family and report the response of at least one declared
gauge-invariant observable of `𝒮` — the minimised action value, the attention optimum `β*`, or the
peer-sector value. If the response is identically zero to machine precision, the link sector is
inert and the "gauge theory" label is unearned for that action version.* This is the single most
informative experiment in the whole roadmap and it is currently missing.

Finally, E2 must state **which holonomy** it measures — graph or base — since without
`hyp:geo-graph-base-transport` (`02:625-640`) they are unrelated (`02:642-645`). Cf. K4.

---

## 7. What `Theory/02_geometry.tex` and `05c_pullback_geometry.tex` already give the roadmap

The roadmap's source boundary (line 174) names `Research/manuscripts/PIFB2.tex`,
`MAgent_Model-main`, and one derivation report. It does **not** name the 17,534-line rigorous
corpus in the same repository, roughly half of whose content is T0. This is K12 and it is cheap to
fix.

### 7.1 T0 obligations already discharged

| T0 obligation (line 112) | Discharged at | Status there |
|---|---|---|
| principal `G`-bundle, typed | `def:geo-principal-systems`, `02:39-53`, `eq:geo-principal-bundle` `02:44` | DEFINITION |
| local frames `u_i:U_i→P`, relative frame field | `eq:geo-frame-sections` `02:52`, `eq:geo-relative-frame` `02:62` | ESTABLISHED |
| law fibers as subsets of `𝒫(𝖪)`, not kernels | `eq:geo-law-fibers` `02:73` with the explicit warning `02:75-79` | DEFINITION |
| the group action **on laws** = pushforward | `eq:geo-representations` `02:85`, `eq:geo-pushforward-actions` `02:93`, and the warning "Multiplying a matrix into a density is not the pushforward" `02:97-99` | DEFINITION + ESTABLISHED |
| smooth tier for differential statements | `hyp:geo-smooth-tier` `02:103-110` | HYPOTHESIS |
| associated statistical bundles + quotient convention | `def:geo-associated-bundles` `02:119-131`, `eq:geo-quotient-convention` `02:131` | DEFINITION |
| passive gauge law on sections | `eq:geo-local-reframing` `02:157` | ESTABLISHED |
| pointwise frame comparison `T_{ij}` (the roadmap's `Ω_{ij}`) and its gauge law | `sec:geo-regime-one` `02:449-483`, `eq:geo-frame-comparison` `02:457`, `eq:geo-regime-one-gauge-law` `02:465` | ESTABLISHED |
| Čech cocycle, class, coboundary criterion (E2's arm 1) | `eq:geo-cech-cocycle` `02:502`, `eq:geo-cech-class` `02:515`, `eq:geo-coboundary-form` `02:522` | ESTABLISHED |
| independent link fields `L_{ij}` with a declared transformation law | `def:geo-graph-links` `02:560-586`, `eq:geo-regime-two-links` `02:569`, `eq:geo-regime-two-gauge-law` `02:576` | DEFINITION |
| graph holonomy and its conjugacy-class invariance | `eq:geo-link-holonomy` `02:592` and `02:594-596` | ESTABLISHED |
| **coboundary ⟺ trivial holonomy** (E2, both directions) | `prop:geo-trivializing-criterion` `02:605-620` | ESTABLISHED |
| the flat/coboundary specialization and its consequence | `hyp:geo-flat-links` `02:646-658`, `eq:geo-flat-regime` `02:653` | HYPOTHESIS |
| connections on `P`, induced associated-bundle transport | `def:geo-connections` `02:282-299`, `eq:geo-principal-connections` `02:286`, `eq:geo-base-parallel-transports` `02:297` | DEFINITION |
| local connection gauge law (E1's (P2)) | `eq:geo-local-connection-b/-m` `02:319/322` | ESTABLISHED |
| endpoint law for represented transports | `eq:geo-pt-gauge-b/-m` `02:329/332` | ESTABLISHED |
| **the `L`–`A` bridge (K4)** | `hyp:geo-graph-base-transport` `02:625-640`, `eq:geo-link-pt-hypothesis` `02:632` | HYPOTHESIS, **zero downstream references** |
| Gaussian moment pushforward / precision congruence | `prop:geo-moment-pushforward` `02:428-446`, `eq:geo-precision-inverse-congruence` `02:439` | ESTABLISHED |
| regularity for statistical tensors (the correct form of line 48) | `hyp:pb-regular-models` `05c:30-46`, esp. `05c:37-41` | HYPOTHESIS |
| **Fisher and Amari–Chentsov descend to the associated bundle** | `prop:pb-statistical-tensor-descent` `05c:59-88` | ESTABLISHED |
| covariant first jet `D^A s` for **nonlinear** fibers | `eq:pb-covariant-first-jet` `05c:106` and the warning `05c:108-111` | DEFINITION |
| the Dirichlet integrand `‖D^Aq‖²_{g^F}` as a base tensor | `def:pb-informational-pullbacks` `05c:112-122`, `eq:pb-fisher-pullback` `05c:114` | DEFINITION |
| **pullback passive gauge invariance** (T2a for the jet sector) | `thm:pb-pullback-gauge-invariance` `05c:124-145` | ESTABLISHED |
| the active/passive distinction, with counterexample | `05c:146-154` | ESTABLISHED |
| exact dependence of the pullback on the chosen connection | `prop:pb-pullback-connection-change` `05c:184-232`, counterexample `05c:220-232` | ESTABLISHED |
| degeneracy of the Dirichlet integrand (`rad h = ker D^A s`) | `05c:321-350`, plus `05c:380-386`, `05c:397-404`, `05c:429-465` | ESTABLISHED |
| `GL(K)` is a Fisher–Rao isometry group of MVN, with citation | `08_infogeometry.tex:97` (`PineleStrapassonCosta2020` eq. 8, plus a recorded typo correction) | ESTABLISHED |

**That is a substantial fraction of T0 and essentially all of T2(a).** WP0 (line 146) can be a
two-page *delta* against `Theory/02` and `05c` rather than a from-scratch ontology.

Two free positives the roadmap should also import:

- **Global sections always exist for its showcase fibers.** `ℝ^K×SPD(K)` and the open simplex are
  contractible, so `ℰ_q` admits global smooth sections over any paracompact base regardless of the
  topology of `P` (audit **G4**, `audit-01-geometry.md:128-150`). Topology obstructs *frames*, never
  *agents*. This closes an existence question T0/T1 would otherwise have to open.
- **The peer sector's divergence invariance holds at the purely measurable tier** — no smoothness,
  no Lie structure, no manifold (wave 2 §1.2, `wave2-01:207-214`). T2(a) can be proved before T1.

### 7.2 Known defects that transfer

| defect | where | how it transfers to the roadmap |
|---|---|---|
| `eq:pb-covariant-jet-gauge-law` (`05c:133-136`) is **asserted**: "In a local frame, the vertical jet transforms by the tangent representation" — no derivation that `ver^ω` intertwines the action on a *nonlinear* fiber | inside the proof of `thm:pb-pullback-gauge-invariance` at `05c:124` | This is precisely the step T2(a) must supply for `‖D^Aq‖²_{g^F}`. The roadmap inherits an unproved step at the heart of its Dirichlet sector. It is true and short — it follows from `hyp:geo-smooth-tier` plus equivariance of the horizontal lift — but it must be written. |
| `hyp:geo-smooth-tier` (`02:103-110`) is referenced only at `02:136`, `02:202`, `02:283`, `05c:33` — **zero references in `07b_agent_network_rg.tex`** (verified by grep over all of `Theory/*.tex`) | ch. 7 | Every RG/coarse-graining statement the roadmap might build on (T8, WP6) uses holonomy algebra without the smooth tier under which `D^ω` and `h_s^ω` exist. T8 must re-declare it. |
| **G3** — `u_i:𝒞_i→P` exists only if `P\|_{𝒞_i}` is trivializable; the syntax admits `𝒞_i=𝒞`; counterexample `𝒞=S²`, Hopf bundle | `02:46-53` | Transfers **verbatim** to roadmap line 66. Fix: add "`U_i` is chosen so that `P\|_{U_i}` is trivializable" and note that the agent supports therefore form a trivializing cover — a modelling constraint the roadmap has not recorded. (K13) |
| **G7** — `ℬ_x ⊆ 𝒫(𝖪)` declared a *subset* then given tangent spaces; image of a parametrised model is a manifold only under injectivity + immersion | `02:69-74` vs `05c:52-57` | Partially fixed by roadmap line 68 ("nondegenerate Fisher metric"), which delivers *local* identifiability. Global injectivity is still unassumed. T1 should close it explicitly. |
| **G1/S3** — no curvature 2-form is defined anywhere in the corpus; `curvature` appears 8 times in 17,534 lines and the `02` occurrence (`02:397`) is a `NOT-CLAIMED` disclaimer | corpus-wide | The roadmap's `κ∫‖F_A‖²` has **no rigorous counterpart at all** to build on, and §1.5 shows it cannot be built for `G=GL(K,ℝ)`. This is the largest genuinely new mathematics the roadmap proposes and it should be scoped as such. |
| **G2** — the bundle-theoretic content of ch. 2 (Čech class, `Ω_γ`, `hyp:geo-graph-base-transport`, `def:geo-covariant-defects`) has **zero** cross-file references | `audit-01-geometry.md:68-104` | The roadmap is the first document with a *use* for `hyp:geo-graph-base-transport` (K4). Consuming it would simultaneously close audit G2 and the roadmap's missing axiom. This is the highest value-per-effort item in the whole review. |
| **G9** — `{U : cond(U) ≤ κ}` admitted as if a group; not closed under multiplication | `realizations/gaussian/gauge.py:36-52` (confirmed present: `_validate_frames`, condition-number rejection at the read I performed) | E1's "random local gauge transformations" will compose admitted frames and silently leave the declared domain. E1 must revalidate after composition or declare the admissible set explicitly as a generating set, not a group. |

---

## 8. Findings, ranked

**FATAL** (kinematics inconsistent as declared)

- **K1.** `κ∫‖F_A‖²dμ` (line 99) cannot be simultaneously `Ad`-invariant and nonnegative for
  `G=GL(K,ℝ)`, `K≥2`. Computed: the `Ad`-invariant symmetric forms on `gl(K,ℝ)` form a 2-dimensional
  space spanned by `tr(XY)` and `tr X·tr Y`, and `tr(XY)` has signature `(3,1)` for `K=2` and
  `(6,3)` for `K=3`, with no positive-definite combination. T2 (line 114) and T4 (line 116,
  "positive covariant spatial terms", "bounded-below observation sector") are therefore mutually
  inconsistent for the showcase group. **Line 13 is wrong**: compact type is a kinematic hypothesis
  belonging in T0, not an analytic hypothesis belonging in T4. Corroborated independently by audit
  RG-7 (`PIFB2.tex:1559,1575,1644,1804`).
- **K2.** No positive-dimensional Lie group acts on a categorical fiber by Fisher–Rao isometries:
  `Isom(Δ_n°,g^F) ≅ S_{n+1}`, finite. Combined with Lemma 1.3 (divergence invariance forces
  isometry), the multi-family gates at lines 131, 147 and 162 are unsatisfiable with one fixed
  positive-dimensional `G`, and the categorical backend has `F_A ≡ 0` identically at every base
  dimension. Repair: replace the categorical showcase with `SPD(K)` under `GL(K)` congruence, or
  make `G` a function of the fiber and restrict T7 to the Gaussian case.

**STRUCTURAL** (missing axiom)

- **K3.** T0 has no non-transitivity / orbit-space axiom. Statement (A-NT) in §2.3, with the two
  escapes (E-a) non-transitive fiber action and (E-b) plural sections under a diagonal group. The
  second is the strong one and A-NOGO does not apply to it, because A-NOGO is stated for a single
  section (`wave2-01:29-40`).
- **K4.** No compatibility axiom relating `L^q_{ij},L^s_{ij}` to `A`. Three regimes (L1)/(L2)/(L3)
  in §3.2; the corpus already contains the (L1) declaration as `hyp:geo-graph-base-transport`
  (`02:625-640`), unreferenced anywhere. `L_{ij}` is *not* parallel transport (both arguments at the
  same base point); the guess in the assignment is wrong and the axiom must be stated differently.
- **K5.** T2 conflates passive well-definedness (true in general), active equivariance on the full
  tuple (true), and active invariance at fixed background (false). Corrected statement and the exact
  co-transformation table in §4.
- **K6.** Line 48's "induced by declared probability-law transformations" admits arbitrary
  diffeomorphisms of `ℳ`; the load-bearing hypothesis is `hyp:pb-regular-models` (`05c:37-41`)
  ("parameter-independent bimeasurable change of sample coordinates"), and `05c:84-87` says
  explicitly that closure under an arbitrary parameter-chart diffeomorphism "would not prove
  statistical isometry". Replacement text in §1.6.
- **K7.** T4 has no slice/gauge-fixing hypothesis. `𝒮` is constant on `Aut_G(P)`-orbits and
  `Aut_G(P)=C^∞(𝒞,G)` is infinite-dimensional and noncompact, so `H¹` coercivity is false as stated
  and the direct method must run on the quotient. A slice theorem for `Aut_G(P)` on manifold-valued
  `H¹` sections is a research obligation and deserves its own row in the theorem table.

**TECHNICAL**

- **K8.** T7 destroys the local gauge group: `Aut_G(P)` over a point is the rigid group `G`, the
  inhomogeneous connection term vanishes identically, and a code implementing only global covariance
  passes every `d=0` test. T7 is not an exactness certificate for the gauge sector. Also: with
  `𝒞={*}` all surviving pairs overlap, so the interaction graph is complete (intended), and T0 must
  declare whether `χ_{ij}` is derived from `(χ_i,U_i∩U_j)` — in which case the `d=0` mask is forced
  to be all-ones and only bidirectional attention is recoverable — or independent, in which case the
  causal mask is `χ_{ij}=1_{j≤i}` and should be claimed.
- **K9.** E1 is confirmatory as written: constant gauge transformations are provably blind to the
  connection's inhomogeneous term (residual exactly `0.000e+00`). Requires non-constant `g(c)` with
  `‖log g‖ ≳ 1`, per-sector reporting, six named positive controls, and the cotangent gradient law
  (§6.1).
- **K10.** E1 has no mesh-scaling arm; the "correct" residual is `O(h²)` truncation (ratio `4.00`
  per halving), so a fixed tolerance cannot separate truncation from a genuine gauge violation. The
  gate should be a convergence-order statement, which also merges E1 into E3 at no cost.
- **K11.** E2's first arm is an algebraic identity (telescoping) and can fail only on an
  implementation bug — a good regression test for audit G8's ordering/inverse conventions, but not
  a scientific control. The second arm needs a cycle-basis test (rank `|E|−|V|+1`) rather than a
  single loop, and E2 needs a **third arm** measuring the *response* of a declared observable to the
  holonomy conjugacy class. Without it E2 cannot detect the inert-gauge-sector failure that audit S3
  and wave 2's O2 both predict.
- **K12.** The roadmap does not cite `Theory/02_geometry.tex` or `05c_pullback_geometry.tex`; §7
  maps roughly half of T0 and all of T2(a) onto existing labels. WP0 should be a delta document.
- **K13.** Line 66's `u_i:U_i→P` silently requires `P|_{U_i}` trivializable (audit G3); the
  consequence — agent supports must form a trivializing cover — is a modelling constraint that
  should be recorded, not just a pedantic one.

**COSMETIC / credit**

- Line 32 correctly identifies that a smooth manifold has no canonical volume form and that a
  cometric or elliptic tensor must be declared. This is the same obstruction wave 2 records as O3
  (`wave2-01:496-500`), and the roadmap states it more clearly than the parent corpus does.
- Line 66 is a correct and independent repair of `PIFB2.tex:208`'s transition/transport conflation
  (§3.1). It should cite `02:449-483` and `02:557-622`.
- Line 104 correctly refuses `𝔼_{q_i}[−log p(o|k,m)]` with an unintegrated `m`. This is a genuine
  typing catch and it is in the same class as `req:gen-typing-prohibition` (`04:120`).
- Line 160's four-way classification (closed-ELBO Markov-field term / effective consensus
  regulariser / gauge-fixing frame-smoothness term / pure-gauge frame-derived connection) is
  correct on every clause and is stated more crisply than anywhere in `Theory` or `PIFB2`.
- Line 13's refusal to identify the abstract layer with Gaussian/`GL(K)` is right in spirit —
  though §1.1b shows that *given* the Gaussian fiber, `GL(K)⋉ℝ^K` is not a choice but the whole
  isometry group, which is a stronger statement than the roadmap makes for itself.

---

## 9. Computations run

All in `/tmp/rm04` on the isolated Linux sandbox, CPU only, `python3` with `numpy 2.2.6` and
`sympy 1.14.0`. **No GPU or CUDA job was started or attempted** (`nvidia-smi` absent).

| script | what it checks | result |
|---|---|---|
| `c1_simplex.py` | `g^F` on `Δ_3°` equals the pullback of the round metric under `x_k=2√p_k` (symbolic) | difference is the exact zero matrix; `Σx_k²=4` |
| `c1_simplex.py` | which `O(4)` elements preserve the open orthant | `0/200` random rotations; all `24` permutations |
| `c1_simplex.py` | exponential tilting is not a Fisher isometry | `‖Φ*g^F − g^F‖_F = 2.658`; control at `θ=0`: `0.0` |
| `c1_simplex.py` | tilting is not a KL isometry; permutation is | `0.24187 → 0.22994`; permutation `0.24187029026937165` vs `…68` |
| `c2_gauss.py` | five candidate `GL(K)` actions on the Gaussian fiber, `K=4` | pushforward `7.6e-15`, affine `6.0e-15`; mean-only `6.32`, cov-only `13.2`, nat-tilt `21.9` |
| `c2_gauss.py` | Fisher is the Hessian of KL (Lemma 1.3) | `1.3733916406` vs `1.3729979106` at `t=10⁻³` |
| `c2_gauss.py` | KL invariance of the three actions | pushforward `8.2e-16`; mean-only `0.319`; nat-tilt `0.285` |
| `c3_isom.py` | Riemann tensor of the MVN Fisher metric at `(0,I)` and `dim{A∈so : A·R=0}`, `K=1,2,3` | scalar curvature `−1, −3.5, −9`; `h(p) = 1,1,3`; `dim Isom ≤ 3, 6, 12` vs `dim Aff = 2, 6, 12` |
| `c4_quotient.py` | invariance of `r²=μᵀΣ⁻¹μ` under `GL⁺(4)` | `4.097e-12` over 500 draws |
| `c4_quotient.py` | transitivity of `GL⁺(K)` on level sets of `r`, explicit `A*` | `K=2`: residuals `2.0e-16`, `2.1e-15`, `det A*=+0.7703`; `K=4`: `1.0e-15`, `1.1e-14`, `det A*=+2.3395` |
| `c4_quotient.py` | diagonal quotient dimension, `K=4`, `N=1,2,3,8` | `1, 12, 26, 96`; stabiliser dims `3,0,0,0` |
| `c4_quotient.py` | torsor tier, `N` sections | `N=1` quotient `0` (A-NOGO); `N=2` quotient `4`; `N=5` quotient `16` |
| `c5_holonomy.py` | coboundary links give trivial holonomy, 1800 random closed walks, lengths 2–7 | max `‖H−I‖_∞ = 3.409e-13` |
| `c5_holonomy.py` | fundamental-cycle holonomy, 6 vertices / 8 edges / cycle rank 3 | coboundary `1.7e-14 … 2.1e-14`; independent `14.65, 162.4, 473.4` |
| `c5_holonomy.py` | `Ad`-invariant symmetric forms on `gl(2,ℝ)`, `gl(3,ℝ)`; exhaustive `61×61` search for a positive-definite combination | dim `2` both; signatures `(3,1)` and `(6,3)`; **NONE** positive definite |
| `c7_e1.py` | Dirichlet sector gauge test, four perturbations × {non-constant, constant} `g` | table in §6.1; `(P2)` exactly `0.000e+00` under constant `g` |
| `c7_e1.py` | peer sector with `L_{ij}`: correct law and three controls | `6.3e-15`; controls `1.239`, `0.938`, `1.713` |
| `c7_e1.py` | gradient equivariance under cotangent vs tangent law | `1.594e-09` vs `3.244e+00` |
| `c10_mesh.py` | mesh scaling of the E1 residual, `Nc = 200…3200` | correct residual ratio `4.05, 4.02, 4.01, 4.00` (`O(h²)`); defects mesh-independent at `8.88` and `3.20` |
| `c11_hier.py` | elliptic `PSL(2,ℝ)` element on MVN(1): Fisher isometry but not KL isometry | Fisher `8.2e-06` (FD accuracy); KL `9.773`; affine control `1.1e-14` |

Computation is not proof. Every statement above tagged as a proposition, lemma or theorem carries a
proof in the text; the numbers are consistency checks with firing controls, run to catch sign and
convention errors. Two were caught during development and corrected before the results above: a
transposition in the cotangent gradient law, and a mislabelled "control" in `c2_gauss.py` (the
mean-only action with orthogonal `A` is an isometry only on the isotropic slice `Σ=σ²I`, not for
general `Σ`; the row is reported in §1.2 without that mislabel).
