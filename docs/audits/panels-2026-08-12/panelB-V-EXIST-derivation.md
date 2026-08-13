# panelB-V-EXIST-derivation

*Recovered verbatim from workflow journal.jsonl, 2026-08-13. Agent a79bd39c.*

## target

TARGET V-EXIST — is S_vol[q] = ∫_C sqrt(det h_{μν}) d^dc, h_{μν} = g^F(D^A_μ q, D^A_ν q), a viable variational object; and is the Polyakov bridge S_P[q,γ] a repair?

## status

OBSTRUCTED

## theorem_statement

Write F(ξ) = sqrt(det(ξᵀGξ)) for ξ ∈ R^{n×d} (n = dim of the statistical fiber, d = dim C) and G = g^F ≻ 0.

**V1 (CONVEXITY — good news, and it is not the binding constraint).** F is POLYCONVEX, hence quasiconvex, hence rank-one convex; F is NOT convex. Explicitly F(ξ) = ‖M_d(Lξ)‖₂ where G = LᵀL and M_d is the vector of all d×d minors. Consequence: Acerbi–Fusco applies and S_vol is sequentially weakly lower semicontinuous on W^{1,d}. Weak lower semicontinuity is NOT the obstruction.

**V1′ (vacuity).** By Cauchy–Binet, det h ≡ 0 identically whenever d > n. S_vol is identically zero — not merely degenerate — unless dim C ≤ dim(fiber) (≤ n_b + n_m for the two-channel product).

**V2 (COERCIVITY — REFUTED, in every dimension, for every fiber, with or without boundary data).** S_vol admits no coercivity estimate on any section space X ↪ W^{1,p}_loc that is closed under precomposition with Diff(C,∂C). Two independent witnesses: (W1) F ≡ 0 on the cone {rank ξ < d}, which contains rays of unbounded norm — an explicit family has S_vol ≡ 0 exactly with ‖Dq_k‖_{L²} → ∞; (W2) S_vol[q∘φ] = S_vol[q] EXACTLY for every φ ∈ Diff(C,∂C), and that orbit is unbounded in W^{1,p} whenever Dq ≢ 0. Hence no sublevel set of S_vol is bounded in any Sobolev norm, and the direct method cannot be run.

**V2′ (this is E6/PA-3 with a group that has no compact reduction).** V2(W2) is exactly the PA-3 lemma — invariance ⟹ constancy on orbits ⟹ no compact sublevel sets — applied with G replaced by Diff(C,∂C). PA-3's escape for the fiber sector (choose compact G ≤ GL(K)) is unavailable: Diff of a positive-dimensional manifold is never compact.

**V2″ (typing catastrophe).** By the area formula S_vol[q] = ∫_B #q^{-1}(y) dH^d_{g^F}(y): minimizing S_vol is a parametric Plateau problem in (B,g^F). Its compactness theory (Federer–Fleming) lives on integral CURRENTS in the fiber, not on sections over C. The relaxed minimizer generically is not the graph of a section, so the minimizer of S_vol is not an agent.

**V3 (RIGIDITY — S_vol is not one option, it is the ONLY one).** If S[q] = ∫_C f(h) d^dc is Diff(C)-invariant with f continuous, then f(AᵀhA) = |det A| f(h) for all A ∈ GL(d), which forces f(h) = f(I)·sqrt(det h) on the nondegenerate locus. Up to a gauge-invariant fiber prefactor W(q(c)) — and O1 (wave2-01:478) kills even that on the recommended tier — S_vol is the unique local Diff(C)-invariant first-order scalar.

**V4 (HOMOGENEITY OBSTRUCTION — the ELBO route and the Diff-invariant route can meet only at d = 2).** V3's cocycle at A = tI gives f(t²h) = t^d f(h): every Diff-invariant local action is homogeneous of degree d in Dq. By E2, any nearest-neighbour transported-KL lattice sum with probability-normalized weights is degree 2 in Dq at leading order. Degree d = degree 2 ⟺ d = 2. Equivalently, the Douglas comparison Area ≤ Dirichlet with equality iff conformal is a d = 2 fact only: for d ≥ 3, sup Area/Dirichlet = +∞.

**V5 (Polyakov on-shell reduction — the PI's claim is CONFIRMED).** Varying γ in S_P = ½∫sqrt|γ|(γ^{μν}h_{μν} − (d−2)) gives h_{μν} = ½γ_{μν}(tr_γ h − (d−2)); tracing gives (d−2)(tr_γ h − d) = 0, so for d ≠ 2, tr_γ h = d and γ_{μν} = h_{μν}, and S_P|on-shell = ∫sqrt(det h) = S_vol. For d = 2 the trace equation is vacuous and γ is fixed only up to a Weyl factor, with the same on-shell value.

**V6 (Polyakov bridge BREAKS for d ≥ 3).** Under a constant Weyl rescaling γ → λγ, S_P(λ) = ½[λ^{d/2−1}A − (d−2)λ^{d/2}V] with A ≥ 0, V > 0. For d ≥ 3 this → −∞ as λ → ∞: **S_P is unbounded below**, and γ = h is a MAXIMUM in the conformal direction, i.e. a saddle of the joint functional. Since a negative ELBO satisfies F = KL(Q‖P(·|o)) − log p(o) ≥ −log p(o) > −∞ for any normalized model, **for d ≥ 3 the γ-varied S_P cannot be the negative ELBO of any normalized model.** For d = 1 (einbein) and d = 2 (Weyl-invariant) S_P is bounded below and γ = h is a genuine minimum.

**V7 (gauge-fixing γ does not rescue d ≠ 2).** Minimizing over the unimodular slice det γ = 1 gives ½(d·(det h)^{1/d} − (d−2)), which is a function of (det h)^{1/d}, equal to sqrt(det h) only for d = 2.

**V8 (option (a) as stated is false on its own terms).** S_P[φ*q, φ*γ] = S_P[q,γ] exactly, so the JOINT Polyakov functional carries precisely the same Diff(C,∂C) invariance as S_vol and V2 applies to it verbatim. "S_P keeps coercivity" is true only at FIXED γ; coercivity in q at fixed γ is not coercivity of the joint problem.

## hypotheses

### 1

(H1) hyp:pb-regular-models (Theory/05c_pullback_geometry.tex:30-42): finite-dimensional smooth parametrized-measure model, differentiability in quadratic mean, POSITIVE-DEFINITE Fisher form, third-power integrability of every score direction. Needed for h = σ*g^F to be defined and for rad h = ker D^ω s (05c:321-331).

### 2

(H2) Fixed, nondynamical connection ω. The quasiconvexity transfer (D^A q = ∂q + ρ_*(A)q is an AFFINE shift of ∂q by a function of (c,u) only) requires this; a dynamical A must be re-analysed. Independently required by roadmap-review:134.

### 3

(H3) C compact (or variations compactly supported) with bounded LIPSCHITZ boundary — required for Rellich–Kondrachov in any wlsc argument (roadmap-review:134 lists this as a hypothesis that must be ADDED, since 'merely measurable' breaks Rellich).

### 4

(H4) Closed proper isometric embedding of the statistical fiber into some R^N (roadmap-review:134), so that manifold-valued wlsc reduces to the constrained Euclidean statement.

### 5

(H5) n = dim B >= d = dim C, else V1' makes S_vol identically zero. With the two-channel weighted product (hyp:pb-weighted-product-geometry, 05c:247-256) the effective n is n_b + n_m.

### 6

(H6) For the wlsc statement V1 only: two-sided bounds on g^F along the fiber region visited. This FAILS on the Gaussian fiber (g^F_{mu mu} = Sigma^{-1} -> 0; PA-7 / roadmap-review:136), so V1 is conditional there even though it is unconditional on the gradient variable.

### 7

(H7) V2, V3, V4, V6, V8 require NONE of H3-H6. They are algebraic/invariance statements and hold for every fiber, every gauge group, every boundary condition, and every d >= 1.

### 8

(H8) For V6's ELBO-typing corollary: the model is normalized with finite evidence p(o) < infinity (this is exactly the standing hypothesis of E1, verified COMPLETE_AFFIRMATIVE in the exact-two-channel-finite-elbo run).


## derivation

SETUP. In a local principal frame over U ⊆ C, write the fiber as an n-dimensional statistical manifold B with Fisher metric G = g^F_{q(c)} ≻ 0 (H1), and the covariant first jet (eq:pb-covariant-first-jet, 05c:98-103) as a matrix ξ = D^ω q(c) ∈ R^{n×d}, ξ_{aμ} = ∂_μ q^a + (ρ_*A_μ)^a(q). Then (eq:pb-fisher-pullback, 05c:112-114) h_{μν} = G(ξe_μ, ξe_ν) = (ξᵀGξ)_{μν}, and the proposed action is S_vol[q] = ∫_C F(ξ) d^dc with F(ξ) = sqrt(det(ξᵀGξ)).

Because ξ = ∂q + Z(c,q) with Z a function of (c,q) only (H2), every convexity property in ξ transfers verbatim to a property in ∂q for each fixed (c,q); the connection is analytically inert here. This is the only role H2 plays.

═══════════════════════════════════════════════════════════════════
§1. CONVEXITY. [DERIVATION + APPLICABLE_THEOREM]
═══════════════════════════════════════════════════════════════════

Lemma 1.1 (Cholesky conjugation). Write G = LᵀL. Then ξᵀGξ = (Lξ)ᵀ(Lξ), so F(ξ) = Φ(Lξ) with Φ(η) = sqrt(det(ηᵀη)) the CLASSICAL parametric area integrand. L acts on the target (row) index only, and is invertible.

Lemma 1.2 (transfer). Polyconvexity, quasiconvexity and rank-one convexity are each preserved under η = Lξ with L invertible on the target index.
  • Quasiconvexity: ∫_D Φ(Lξ + Dψ) ≥ |D|Φ(Lξ) for all ψ ∈ C_c^∞(D;R^n). Since F(ξ + Dφ) = Φ(Lξ + D(Lφ)) and φ ↦ Lφ is a bijection of C_c^∞(D;R^n), the quasiconvexity inequality for Φ is exactly the one for F.
  • Polyconvexity: by Cauchy–Binet applied to each r×r block, every r-minor of Lξ is a fixed linear combination of the r-minors of ξ: det((Lξ)_{I,J}) = Σ_K det(L_{I,K}) det(ξ_{K,J}). A convex function of the minors of Lξ is therefore a convex function of the minors of ξ.
  • Rank-one convexity: rank(Lξ) = rank(ξ) and L(a⊗b) = (La)⊗b, so rank-one lines map to rank-one lines.

Proposition 1.3 (the classical fact, and its source). For η ∈ R^{n×d} with d ≤ n, Cauchy–Binet gives
      det(ηᵀη) = Σ_{|I| = d} (det η_{I,:})²,
hence Φ(η) = ‖M_d(η)‖₂, the Euclidean norm of the vector of TOP-ORDER minors of η. The Euclidean norm is convex, so Φ is a convex function of the d×d minors of η, i.e. Φ is POLYCONVEX by Ball's definition (J.M. Ball, "Convexity conditions and existence theorems in nonlinear elasticity", Arch. Rat. Mech. Anal. 63 (1977) 337–403). Polyconvex ⟹ quasiconvex ⟹ rank-one convex for Borel-measurable, locally bounded f (Dacorogna, *Direct Methods in the Calculus of Variations*, 2nd ed., Springer 2008, Thm. 5.3); F is continuous, so this applies. Quasiconvexity is Morrey's condition (C.B. Morrey, "Quasi-convexity and the lower semicontinuity of multiple integrals", Pacific J. Math. 2 (1952) 25–53).

Theorem V1. F(ξ) = sqrt(det(ξᵀGξ)) is polyconvex, quasiconvex and rank-one convex, and is NOT convex.
Proof. Polyconvexity: Lemmas 1.1–1.3 give F(ξ) = ‖M_d(Lξ)‖₂ with M_d(Lξ) a fixed linear image of M_d(ξ); a norm composed with a linear map is convex. Quasiconvexity and rank-one convexity follow by Dacorogna Thm. 5.3.
Non-convexity, explicit witness (d = n = 2, G = I): F(diag(1,0)) = 0, F(diag(0,1)) = 0, F(½diag(1,1)) = ¼ > 0 = ½(0+0). CHECK 3.
Independent direct proof of rank-one convexity: along ξ + t a⊗b every d×d minor of L(ξ + t a⊗b) is AFFINE in t (verified to 1.4e-14, CHECK 4), so F = ‖affine(t)‖₂ is convex in t. □

Numerical confirmation of Lemma 1.3 + Lemma 1.1: sqrt(det(ξᵀGξ)) = ‖M_d(Lξ)‖₂ to < 1e-8 relative at (n,d) ∈ {(2,2),(3,2),(5,3),(4,4),(6,2)} with random SPD G (CHECK 1/2).

Corollary 1.4 (two channels). With h^prod = w_b h_b + w_m h_m (eq:pb-weighted-channel-pullback, 05c:249-253), set Z = [√w_b L_b D^{ω_b}q ; √w_m L_m D^{ω_m}s], an ((n_b+n_m)×d) matrix LINEAR in the joint gradient. Then h^prod = ZᵀZ exactly (verified to 2.8e-14, CHECK 5). So sqrt(det h^prod) is the induced volume of the section into the PRODUCT fiber with metric w_b g_b ⊕ w_m g_m, and is polyconvex JOINTLY in (Dq, Ds). This is the correct generalization and it also raises the effective n to n_b + n_m, relaxing V1′.

Corollary 1.5 (wlsc holds — the analysis does NOT fail here). F is exactly d-homogeneous: F(tξ) = t^d F(ξ). By Hadamard, det h ≤ Π_μ h_{μμ}, so 0 ≤ F(ξ) ≤ C|ξ|^d with C = C(‖G‖,d). Acerbi–Fusco (E. Acerbi, N. Fusco, "Semicontinuity problems in the calculus of variations", Arch. Rat. Mech. Anal. 86 (1984) 125–145; Dacorogna Thm. 8.11): a Carathéodory integrand, quasiconvex in ξ, with 0 ≤ f ≤ C(1 + |u|^p + |ξ|^p), is sequentially weakly lower semicontinuous on W^{1,p}. With p = d and H3–H6, S_vol is sequentially wlsc on W^{1,d}. **Verifying the hypotheses honestly: the upper p-growth bound holds; the LOWER bound c|ξ|^p − C required for the two-sided (necessary-and-sufficient) form fails catastrophically — see §2.** So the semicontinuity half of the direct method is fine and the compactness half is destroyed.

Proposition V1′ (vacuity for d > n). Cauchy–Binet has an empty index set when d > n: there are no d×d minors, hence det(ξᵀGξ) ≡ 0. Verified numerically at (n,d) ∈ {(2,3),(3,5),(1,2)}: |det h| ≤ 2.3e-27 (CHECK 9). So S_vol ≡ 0 unless dim C ≤ dim(fiber). *This is a special case of a fact already in the corpus:* wave2-01-constructions.md:134-136 records that "a Fisher-length weighting sqrt(det h_s^ω) is degenerate whenever rank h_s^ω < dim C, which on the exhibited tier is generic (h_s^ω = dmᵀΣ₀^{-1}dm has rank ≤ min(K, dim C))."

═══════════════════════════════════════════════════════════════════
§2. COERCIVITY. [FORMAL_PROOF — this is the catastrophe]
═══════════════════════════════════════════════════════════════════

Theorem V2. Let X be any Banach space of sections continuously embedded in W^{1,p}_loc(C;E) for some p ∈ [1,∞), closed under q ↦ q∘φ for φ ∈ Diff(C,∂C). Then there is NO increasing unbounded ψ with S_vol[q] ≥ ψ(‖q‖_X) − C. Moreover for every q with Dq ≢ 0 on a set of positive measure, the sublevel set {S_vol ≤ S_vol[q]} is unbounded in X.

Witness W1 (rank-degeneracy cone). F(ξ) = 0 ⟺ rank ξ < d, and this set is a cone containing the rays {t ξ₀ : t > 0} for any rank-deficient ξ₀. Explicitly, on C = (0,1)^d, d ≥ 2, take a fixed nonconstant C¹ curve γ: R → B and q_k(c) = γ(k c¹). Then D q_k has rank ≤ 1 < d, so
      S_vol[q_k] = 0   EXACTLY,   for every k,
while ‖Dq_k‖²_{L²} = k ∫|γ′|²_{g^F} → ∞. Verified: S_vol = 0.0e+00 for k = 1,10,100,1000 while ‖Dq‖²_{L²} = 1, 1e2, 1e4, 1e6 (CHECK 8B). Interpretation: a section may have arbitrarily violent contextual variation in one direction at literally zero cost, provided it is constant in some other base direction.

Witness W2 (exact Diff(C,∂C)-invariance). For φ ∈ Diff(C,∂C), h_{q∘φ} = Dφᵀ (h_q∘φ) Dφ, so sqrt(det h_{q∘φ}) = (sqrt(det h_q)∘φ)·|det Dφ| and the change-of-variables formula gives
      S_vol[q∘φ] = ∫ (sqrt(det h_q)∘φ)|det Dφ| d^dc = ∫ sqrt(det h_q) d^dc = S_vol[q],   EXACTLY.
Verified by quadrature on (0,1)², n = 3, with a nontrivial boundary-fixing diffeo: S_vol 0.85456664 → 0.85456658, relative difference 6.8e-08, while Dirichlet energy changes by a factor 1.129 (CHECK 13). Explicit unbounded orbit, boundary-fixing: φ_k(c¹,c²) = ((c¹)^k, c²) on (0,1)². Then
      k = 1,2,4,8,16 :  S_vol = 0.854567, 0.854565, 0.854554, 0.854511, 0.854334  (constant to quadrature error)
      k = 1,2,4,8,16 :  Dirichlet = 1.3416, 1.6515, 2.6305, 4.6514, 8.6927 → ∞     (CHECK 15).
So a minimizing sequence for S_vol can be made unbounded in W^{1,2}; no subsequence has a weak limit. □

Theorem V2′ (this is E6/PA-3 with Diff(C,∂C) in place of the fiber gauge group). PA-3 (rm-02 §3.3, finding T-3; restated at roadmap-review:138): if a functional is invariant under a group with a noncompact orbit, it is constant on that orbit and therefore has no sublevel set with compact closure. Apply with the group Diff(C,∂C) and the exact invariance of W2. The proof is one line and the conclusion is unconditional.
**The escape available in the fiber sector is NOT available here.** E6/PA-3's repair for Aut_G(P) is "choose G compact ≤ GL(K), Haar-average" (worklog:407-412). Diff(M) for dim M ≥ 1 is an infinite-dimensional Fréchet Lie group and is never compact; it admits no compact reduction, and no subgroup reduction is available because full Diff-invariance is precisely the property S_vol was chosen for (it is what removes the exogenous base cometric and density, 05c:1362-1366). **Committing to S_vol converts the ONE obstruction the PI can fix into TWO, one of which is unfixable by the known repair.**

Theorem V2″ (the relaxation leaves the section category). By the area formula, S_vol[q] = ∫_B #{c ∈ C : q(c) = y} dH^d_{g^F}(y): S_vol is the g^F-Hausdorff d-measure of the image of C, counted with multiplicity. Minimizing it subject to boundary data is a parametric Plateau problem in (B, g^F). The compactness that V2 denies to sections is restored only in the geometric-measure-theoretic category — Federer–Fleming compactness for integral currents (H. Federer, W. Fleming, "Normal and integral currents", Ann. Math. 72 (1960) 458–520) yields mass-minimizing d-currents in B. Such a minimizer need not be, and generically is not, the graph of a map from C, and it may be singular (Almgren/Federer regularity bounds). Since the entire ontology is "an agent IS a section q_i : C_i → E_b" (Theory/02_geometry.tex:16-34; Theory/12_philosophy.tex:25-29), **the minimizers of S_vol are not agents.** The honest relaxation is the Cartesian-currents framework (Giaquinta–Modica–Souček, *Cartesian Currents in the Calculus of Variations*, Springer 1998), which is a different ontology, not a technical fix.

Corollary V2‴ (d = 1 is already in the manuscript, with the warning attached). For d = 1, S_vol = ∫ sqrt(h_s^ω(γ̇,γ̇)) dλ is EXACTLY eq:pb-section-curve-length (05c:627-631), and prop:pb-curve-taxonomy (05c:621-635) already PROVES its invariance under orientation-preserving C¹ reparameterization. 05c:1368-1370 already attaches \status{NOT-CLAIMED}: vertical Fisher length "does not generate an orbit, identify a physical time coordinate, or compare independently evolved fine and coarse paths." The d = 1 shadow of S_vol, its exact reparameterization invariance, and a warning about what it cannot do, are all already in the corpus.

═══════════════════════════════════════════════════════════════════
§3. RIGIDITY — S_vol is forced, which makes things worse, not better. [FORMAL_PROOF]
═══════════════════════════════════════════════════════════════════

Theorem V3. Let S[q] = ∫_C f(h(c)) d^dc with f : Sym²_{≥0}(R^d) → [0,∞) continuous, and suppose S[φ*q] = S[q] for every φ ∈ Diff(C) and every q. Then f(h) = f(I)·sqrt(det h) for every SPD h.
Proof. Under c ↦ u = φ(c), h ↦ Dφᵀ(h∘φ)Dφ and d^dc = |det Dφ|^{-1} d^du, so invariance for all q and all φ requires the cocycle
      f(AᵀhA) = |det A| f(h)   for all A ∈ GL(d), h SPD,
since every A ∈ GL(d) is realized as Dφ(c₀) for some local diffeomorphism.
  Step 1 (A = tI): f(t²h) = t^d f(h) — f is homogeneous of degree d/2 in h, i.e. degree d in Dq.
  Step 2 (h = I): f(AᵀA) = |det A| f(I) = f(I) sqrt(det(AᵀA)). Every SPD matrix is of the form AᵀA. □
Numerical confirmation: sqrt(det ·) satisfies the cocycle to 4e-13 across random A, h at d = 2,3; tr(h) violates it by O(10), (tr h)^{d/2} by O(10), and det(h)^{1/d} by O(1) at d = 3 while coinciding with sqrt(det h) at d = 2 as it must (CHECK 16).
Remark. Allowing a fiber-scalar prefactor W(q(c)) gives f = W(q)sqrt(det h); W must be G-invariant, and on the recommended tier obstruction O1 (wave2-01-constructions.md:478-486: B is a G-torsor, so every invariant functional is constant) forces W constant. The classification is then complete: **S_vol is the unique local, Diff(C)-invariant, gauge-invariant first-order action.** There is no "better Diff-invariant choice" to look for.

═══════════════════════════════════════════════════════════════════
§4. THE HOMOGENEITY OBSTRUCTION — d = 2 or nothing. [DERIVATION]
═══════════════════════════════════════════════════════════════════

Theorem V4. A Diff(C)-invariant local first-order action is homogeneous of degree d in Dq (Theorem V3, Step 1; verified symbolically for d = 1,2,3,4, CHECK 10). By E2 (this session, verified symbolically in three exponential families),
      D_KL(q_{θ+h}‖q_θ) = ½ g^F h² + ⅓T_skew h³ + O(h⁴),
so every nearest-neighbour transported-KL lattice sum with probability-normalized weights (Σ_b β_{ab} = 1, which bounds the weights by 1 and by PA-8 makes the reduced sector a bounded soft-min) is homogeneous of degree **2** in Dq at leading order. Therefore:
      a Diff-invariant local action can be the h → 0 limit of an ELBO-derived lattice KL sum only if d = 2.

Equivalent geometric form. Writing λ₁,…,λ_d for the eigenvalues of h, the Dirichlet density is ½Σλ_i and the volume density is (Πλ_i)^{1/2}. Their ratio (Πλ)^{1/2}/(½Σλ) is homogeneous of degree d/2 − 1 in the common scale, so it is bounded only for d = 2. Verified: sup over sampled h of Area/Dirichlet = 1.0000 at d = 2 (attained exactly at λ₁ = λ₂, i.e. CONFORMAL h), and unbounded for d ≥ 3 — explicitly, at λ = s·1 the ratio is 0.667, 2.108, 6.667 for s = 1,10,100 at d = 3, and 0.500, 5.000, 50.000 at d = 4 (CHECK 11). **The Douglas comparison Area ≤ Dirichlet, with equality iff conformal — the entire basis of the Douglas–Radó solution of Plateau — is a d = 2 fact and nothing else.**

═══════════════════════════════════════════════════════════════════
§5. THE POLYAKOV BRIDGE. [DERIVATION; the PI's algebra is right, the conclusion is not]
═══════════════════════════════════════════════════════════════════

Proposition V5 (γ-variation; PI's claim CONFIRMED). Using δ√|γ| = −½√|γ| γ_{μν} δγ^{μν} and δ(γ^{μν}h_{μν}) = h_{μν}δγ^{μν},
      δS_P = ½∫√|γ| [ h_{μν} − ½γ_{μν}(tr_γ h − (d−2)) ] δγ^{μν} d^dc,
so the Euler–Lagrange equation is h_{μν} = ½γ_{μν}(T − (d−2)) with T := γ^{ab}h_{ab}. Contracting with γ^{μν}: T = (d/2)(T − (d−2)), i.e. (d−2)(T − d) = 0.
  • d ≠ 2: T = d, hence h_{μν} = ½γ_{μν}(d − (d−2)) = γ_{μν}, and S_P|on-shell = ½∫√(det h)(d − (d−2)) = ∫√(det h) = S_vol. ✔
  • d = 2: the trace equation is vacuous; γ_{μν} = (2/T)h_{μν} is a solution for EVERY conformal factor, and the value is still S_vol.
Verified symbolically for d = 1,2,3,4: EL residual at γ = h is identically 0 in all components, and S_P|on-shell = √(det h) exactly (CHECK 6). For d = 2, the EL residual is identically 0 for γ = w·h^{-1} for every w > 0, symbolically in w (CHECK 14).

Theorem V6 (the bridge BREAKS for d ≥ 3). Under a constant Weyl rescaling γ → λγ: √|λγ| = λ^{d/2}√|γ| and (λγ)^{μν} = λ^{-1}γ^{μν}, so with A := ∫√|γ| tr_γ h ≥ 0 and V := ∫√|γ| > 0,
      S_P(λ) = ½[ λ^{d/2−1} A − (d−2) λ^{d/2} V ].
  d = 1: (A + Vλ)/(2√λ) → +∞ at both ends; unique minimum at λ = A/V.        BOUNDED BELOW — genuine minimization.
  d = 2: ≡ A/2, independent of λ (Weyl invariance).                            BOUNDED BELOW — genuine minimization.
  d = 3: √λ(A − Vλ)/2 → 0⁺ as λ→0⁺, → −∞ as λ→∞; critical point A/(3V) is a MAX.  UNBOUNDED BELOW.
  d = 4: λ(A − 2Vλ)/2 → 0⁺ as λ→0⁺, → −∞ as λ→∞; critical point A/(4V) is a MAX.  UNBOUNDED BELOW.
(Symbolic limits and critical points, CHECK 7; confirmed by direct probing of the joint functional, CHECK 12: at d = 1,2 the point γ = h is a local MINIMUM over random SPD probes and along the Weyl ray; at d = 3,4 local probes reach 5.398 < 11.414 and 43.836 < 59.510, and the Weyl ray reaches −2785 and −2.36e5.)

Corollary V6′ (ELBO typing contradiction). For any normalized generative model with finite evidence, the negative ELBO satisfies F = D_KL(Q‖P(·|o)) − log p(o) ≥ −log p(o) > −∞ (this is the identity underlying E1, COMPLETE_AFFIRMATIVE). A functional unbounded below is therefore not the negative ELBO of any normalized model. **For d ≥ 3, S_P with γ free is not an ELBO, and the γ-variation that produces γ = h is a maximization, not the tightening of a bound.** The two halves of the proposal — "γ is a free auxiliary field whose on-shell value is determined by the beliefs" and "S_P is the h → 0 limit of the ELBO-derived lattice KL sum" — are mutually inconsistent for d ≥ 3.

Proposition V7 (gauge-fixing γ does not rescue d ≠ 2). On the unimodular slice det γ = 1, AM–GM on the eigenvalues of γ^{-1}h (whose determinant is det h) gives tr(γ^{-1}h) ≥ d(det h)^{1/d}, with equality at γ = h/(det h)^{1/d}. So the gauge-fixed value is ½(d(det h)^{1/d} − (d−2)), which depends on det(h)^{1/d}, NOT sqrt(det h). Verified: at d = 3, gauge-fixed value 7.862 vs S_vol 13.162; at d = 4, 10.129 vs 30.963; at d = 2 they agree exactly (2.32686 = 2.32686) (CHECK 12).

Theorem V8 (option (a) does not keep coercivity). S_P[φ*q, φ*γ] = S_P[q,γ] exactly for φ ∈ Diff(C,∂C), since h, γ and the density all transform covariantly. Hence the JOINT Polyakov functional has exactly the Diff-orbit invariance of Theorem V2/V2′, and its sublevel sets are unbounded for the same one-line reason. What is true — and it is a real and useful truth — is that at FIXED γ the q-problem is the Dirichlet form ½∫√|γ| γ^{μν}h_{μν}, which is **convex** (not merely quasiconvex) in Dq, coercive as c‖Dq‖²_{L²(γ)}, and trivially wlsc. Coercivity in q at fixed γ is not coercivity of the joint problem, and it is fixing γ, not varying it, that buys the analysis.

═══════════════════════════════════════════════════════════════════
§6. THE TWO GROUPS, THE QUOTIENT, AND REDUCIBLE CONFIGURATIONS (item 3)
═══════════════════════════════════════════════════════════════════

(a) Does invariance make existence WORSE? Yes, strictly. E6/PA-3 says invariance and coercivity are in tension whenever orbits are noncompact. S_vol is invariant under Diff(C,∂C) × Aut_G(P) — two infinite-dimensional groups. For the fiber factor the known repair is compact G ≤ GL(K) (worklog:407-412; roadmap-review:177). For Diff(C,∂C) there is no repair: it is never compact, and its orbits are exactly the unbounded ones of CHECK 15. Under S_vol, PA-3 fires twice and can be answered once.

(b) Can minimizers exist only in the quotient? Quotienting does not restore compactness, it only relabels the failure. Two distinct singular strata:
  • BASE-REDUCIBLE (non-immersive) sections, rank D^ω q < d. This is exactly the locus thm:pb-pullback-rank-quotient (05c:321-348) must exclude by hypothesis ("If D^ω s has CONSTANT rank…"), and 05c:456-465 supplies the explicit witness h_s = 4x²dx² whose "pointwise quotients do not assemble into a vector bundle across that point." Worse, 05c:429-454 (prop:pb-contact-null-counterexample) exhibits a CONSTANT-rank case whose radical is a contact distribution, not a foliation — so even constant rank does not give a quotient manifold. And wave2-01:134-136 records that on the exhibited tier rank drop is GENERIC.
  • FIBER-REDUCIBLE sections, nontrivial stabilizer in G. For a Gaussian fiber point, Stab_{GL(K)}(N(0,I)) = O(K) is nontrivial, so reducibility is generic rather than exceptional; O1 (wave2-01:478-486) is the extreme case in which every invariant functional is constant. This is the standard mechanism by which gauge quotients fail to be manifolds (Donaldson–Kronheimer, *The Geometry of Four-Manifolds*, OUP 1990, §4.2.2).

(c) Slice theorem? The available results do not apply.
  • Palais' slice theorem needs a PROPER action (compact/locally compact group). Diff(C,∂C) acting on sections by precomposition is not proper: a constant section has isotropy equal to the whole group, so orbits of nearby full-rank and rank-deficient sections cannot be separated and the quotient is not Hausdorff where it matters.
  • Ebin's slice theorem (D. Ebin, "The manifold of Riemannian metrics", Proc. Symp. Pure Math. 15 (1970) 11–40) is for Diff acting on METRICS, where the action IS proper because the isotropy group (the isometry group) is compact. It does not transfer to Diff acting on maps or sections.
  • The one positive result is Cervera–Mascaró–Michor ("The action of the diffeomorphism group on the space of immersions", Diff. Geom. Appl. 1 (1991) 391–401): Diff(M) acts freely and properly on the space of FREE IMMERSIONS, and Imm_free(M,N)/Diff(M) is a smooth manifold. It fails us three times over: it needs immersions — precisely the full-rank condition S_vol neither enforces nor penalizes; Imm is OPEN, hence not weakly closed, so a weak limit of immersions is generically not an immersion and the direct method cannot be run inside it; and it is a Fréchet-manifold statement, not a Banach/Sobolev completeness statement.
Conclusion for (b)–(c): the quotient is a non-Hausdorff stratified space, singular exactly on the locus that minimizing sequences run into. In d = 2, and only there, the residual after quotienting is finite-dimensional (conformal structures modulo Diff = Teichmüller space, plus Douglas' three-point condition to kill the Möbius noncompactness) — which is precisely why Plateau is solved in d = 2 and p-branes for p ≥ 2 have no controlled variational theory.

═══════════════════════════════════════════════════════════════════
§7. WHAT S_vol ACTUALLY IS, AND THE REFORMULATION I RECOMMEND (item 4)
═══════════════════════════════════════════════════════════════════

S_vol has a precise, standard information-theoretic identity that nobody in the corpus has named: by V2″ it is the Fisher–Rao Riemannian volume of the image family {q(c) : c ∈ C} ⊂ B. That is the **Jeffreys volume** (H. Jeffreys, "An invariant form for the prior probability in estimation problems", Proc. R. Soc. A 186 (1946) 453–461), equivalently **Rissanen's parametric complexity / geometric-complexity term** in normalized-maximum-likelihood MDL (J. Rissanen, "Fisher information and stochastic complexity", IEEE Trans. Inf. Theory 42 (1996) 40–47; V. Balasubramanian, Neural Comput. 9 (1997) 349–368; Myung–Balasubramanian–Pitt, PNAS 97 (2000) 11170–11175), where log ∫√(det I(θ))dθ is a code length. So S_vol has the type of a COMPLEXITY PENALTY, not of a whole action. That is exactly consistent with §2: minimizing a complexity penalty alone drives the model family to collapse onto a lower-dimensional image, which is precisely witness W1.

THE RECOMMENDED REFORMULATION — option (c), a corrected version of (a):
  1. **γ is not an auxiliary field to be varied; γ IS the design.** The lattice Λ_h's neighbour graph and its h^{d−2} weights (E2/C3) determine a discrete Dirichlet form whose continuum limit is ½∫√|γ|γ^{μν}h_{μν} for a γ read off the lattice geometry; anisotropic refinement gives anisotropic γ. So the "exogenous base cometric and density" of 05c:1362-1366 and of obstruction O3 are not intrinsic structures on C and are not dynamical fields — they are carried by the finite design.
  2. **This is already what A4.5 says.** wave2-01-constructions.md:406-413: when μ charges C∖D, F_μ is at best an EXTENSION and "the extension is not determined: every μ with μ|_D = μ_D gives one"; along a refining family the limit is pinned by the sequence. Identify the two objects: **the refining sequence is γ.** O3 and A4.5 are the same fact stated twice.
  3. **N1 survives, in the manuscript's own words.** 02_geometry.tex:25-26: "The finite design D is a finite subset of C, not a continuum limit or a discretization theorem." 12_philosophy.tex:34-35: "the finite design is a declared subset, not a random sample from a law on C. No expectation over contexts is used." Declaring a DESIGN is the manuscript's standing position; declaring a metric on C is what N1 forbids. The base geometry is a property of the inquiry, not of C. That is a defensible and, I think, a genuinely attractive ontological claim, and it removes the PIFB2 incompatibility at Theory/PIFB2.tex:1731 (verified verbatim; identical line in the live copy at Desktop/Research/manuscripts/PIFB2.tex:1731) by reinterpreting √|g|(c)dc as design density rather than intrinsic base metric.
  4. **Primary object: the fixed-γ Dirichlet form.** Convex in Dq, coercive as ‖Dq‖²_{L²(γ)}, wlsc by Ioffe, an exact ELBO component at every finite lattice by E3, degree-2 in Dq matching E2. Every good property survives.
  5. **S_vol demoted from action to invariant.** Keep it, but as a Diff-invariant DIAGNOSTIC: by Theorem V3 it is the unique such local scalar, and by §7 it is the geometric complexity of the context-indexed model family. Reporting it alongside the design-dependent action gives a design-independent number — exactly the quantity with which to test whether conclusions depend on the design. That is a real role, honestly typed.
  6. **The well-posed research question that replaces "does N1 survive".** Not "can the base geometry be manufactured from h" (V6/V8 say the manufacturing step is a saddle and breaks the ELBO typing) but: **for which section classes and which refining families is the h → 0 limit independent of the refining sequence, modulo Diff(C)?** That is a Γ-convergence / design-independence question, it is precisely what A4.5 leaves open, and it is answerable.
  7. **If the PI nonetheless insists on a Diff-invariant primary action, it must be d = 2.** Three independent arguments converge: V6 (boundedness below / genuine minimization only at d ≤ 2), V4 (homogeneity match with the ELBO lattice limit only at d = 2), and §6(c) (conformal gauge, finite-dimensional residual moduli, Douglas–Radó only at d = 2). The coordinator independently reached d = 2 by a different route (roadmap-review:186: "the continuum program scoped to d = 2").

HONEST LIMIT ON THE RECOMMENDATION. Option (c) restores coercivity in the base sector conditional on two-sided bounds on g^F along the visited fiber region. That FAILS on the Gaussian fiber (g^F_{μμ} = Σ^{-1} → 0; PA-7, roadmap-review:136). This is a pre-existing defect independent of S_vol, and the recommended split T4a/T4b (roadmap-review:146,180) is the right response. The correct comparison is: **the Dirichlet form is coercive in the directions g^F controls; S_vol is coercive in no direction at all, on no fiber, in no dimension.**

## obstructions

### 1

O-V1 NON-COERCIVITY (fatal, unconditional). S_vol is exactly constant on Diff(C,∂C)-orbits, and those orbits are unbounded in every Sobolev norm. No sublevel set is bounded; the direct method cannot be run in any section space, any dimension, any fiber, any gauge group, any boundary data. Verified numerically (CHECK 13, CHECK 15). This is E6/PA-3 applied to a group that admits no compact reduction.

### 2

O-V2 ZERO-COST RANK DEGENERACY (fatal, independent of O-V1). F vanishes identically on {rank ξ < d}, a cone containing rays of unbounded norm. An explicit section family has S_vol ≡ 0 EXACTLY while ‖Dq_k‖_{L²} → ∞ (CHECK 8B). Already recorded, for the same object, at docs/audits/ultradeep-wave2-2026-08-12/wave2-01-constructions.md:134-136 as the audit's stated reason for rejecting sqrt(det h) in favour of a pointwise density.

### 3

O-V3 THE MINIMIZERS ARE NOT SECTIONS (typing catastrophe). By the area formula S_vol is a parametric Plateau problem in the fiber; its compactness theory (Federer–Fleming) lives on integral currents, and the relaxed minimizer generically is not the graph of a map from C. The variational principle's solutions are not agents, contradicting the ontology at Theory/02_geometry.tex:16-34 and Theory/12_philosophy.tex:25-29.

### 4

O-V4 S_P IS UNBOUNDED BELOW FOR d ≥ 3. Under γ → λγ, S_P(λ) = ½[λ^{d/2−1}A − (d−2)λ^{d/2}V] → −∞. γ = h is a MAXIMUM in the conformal direction, so the on-shell reduction to S_vol is a saddle, not a minimization (CHECK 7, CHECK 12). A negative ELBO is bounded below by −log p(o); therefore for d ≥ 3 the γ-varied S_P is not the negative ELBO of any normalized model. The two halves of the proposal are mutually inconsistent for d ≥ 3.

### 5

O-V5 HOMOGENEITY MISMATCH. Every Diff(C)-invariant local first-order action is degree d in Dq (Theorem V3 Step 1); every nearest-neighbour transported-KL lattice sum with normalized weights is degree 2 in Dq (E2). They can coincide only at d = 2. Equivalently, Area ≤ Dirichlet with equality iff conformal is a d = 2 fact: sup Area/Dirichlet = 1 at d = 2 and +∞ for d ≥ 3 (CHECK 11).

### 6

O-V6 VACUITY FOR d > n. Cauchy–Binet forces det h ≡ 0 when dim C exceeds the fiber dimension (CHECK 9). With the two-channel product the threshold is n_b + n_m, but the constraint is hard and must be stated wherever S_vol appears.

### 7

O-V7 THE QUOTIENT IS NOT WORKABLE. Diff(C,∂C) does not act properly on sections (constant sections have full isotropy), so Palais and Ebin do not apply; Cervera–Mascaró–Michor applies only on free immersions, which form an OPEN, weakly non-closed set in the Fréchet category. Both reducible strata are generic here: base-reducible (rank drop — 05c:456-465 explicit witness; 05c:429-454 shows even constant rank need not foliate) and fiber-reducible (Stab_{GL(K)}(N(0,I)) = O(K); O1 at wave2-01:478-486).

### 8

O-V8 UNIMODULAR GAUGE-FIXING DOES NOT REPAIR d ≠ 2. Minimizing over det γ = 1 gives ½(d·(det h)^{1/d} − (d−2)), a function of det(h)^{1/d}, equal to sqrt(det h) only at d = 2 (CHECK 12).

### 9

O-V9 (inherited, not caused by S_vol) The Gaussian fiber fails coercivity for the Dirichlet form too (g^F_{μμ} = Σ^{-1} → 0; PA-7 / roadmap-review:136). Option (c) must be scoped by T4a/T4b, not oversold.


## novelty

PARTIALLY PRE-EMPTED — the PI is re-proposing an object his own wave-2 audit already rejected, and the worklog already flags the key caveats.

ALREADY IN THE CORPUS (do not claim):
• `docs/audits/ultradeep-wave2-2026-08-12/wave2-01-constructions.md:134-136` — sqrt(det h_s^ω) named explicitly and REJECTED: "a Fisher-length weighting `\sqrt{\det h_s^\omega}` is degenerate whenever `rank h_s^\omega < dim C`, which on the exhibited tier is generic (`h_s^\omega = dm^T Σ_0^{-1} dm` has rank ≤ min(K, dim C))." This is a special case of my O-V2 and O-V6, and it was one of the audit's three stated reasons for choosing the pointwise density instead.
• `C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md:333-344` — §3c.6 already tags S_vol \status{CONJECTURE} with the two caveats that matter: "It is not the h→0 limit of the lattice KL sum" and "Degenerate on the rank-drop locus."
• `Theory/05c_pullback_geometry.tex:621-635` (prop:pb-curve-taxonomy) — the d = 1 case of S_vol and its exact reparameterization invariance are already PROVED; `05c:1368-1370` already attaches the \status{NOT-CLAIMED} warning.
• `Theory/05c_pullback_geometry.tex:321-348, 429-465` — the constant-rank hypothesis, the rank-jump counterexample (h_s = 4x²dx²) and the non-involutive constant-rank radical are all already established.
• PA-3 / E6 itself (`rm-02` §3.3 T-3, restated at `docs/research-plans/2026-08-12-continuum-roadmap-review.md:138`).
• d = 2 scoping was independently recommended by the coordinator at `roadmap-review:186`.

NEW IN THIS RUN (searched Theory/*.tex and docs/** for "quasiconvex", "polyconvex", "Morrey", "Nambu", "Polyakov", "minimal surface", "induced volume": ZERO hits anywhere; the only "det h" hits are wave2-01:134 and unrelated |det h| = 1 lines at Theory/09_coarsegraining.tex:759 and wave2-03-redteam.md:168-193):
1. The convexity classification (Theorem V1) with the Cholesky-conjugation lemma showing the g^F-weighted integrand is the classical area integrand precomposed with an invertible target map, hence inherits polyconvexity; plus Corollary 1.4, that the two-channel weighted product is the induced volume of the STACKED section and is therefore jointly polyconvex.
2. The exact non-coercivity theorem V2/V2′ — recognizing that O-V1 is PA-3 applied to Diff(C,∂C), a group with no compact reduction, so committing to S_vol converts a fixable obstruction into an unfixable one.
3. The rigidity theorem V3: S_vol is the UNIQUE local Diff(C)-invariant first-order scalar.
4. The homogeneity obstruction V4 pinning d = 2, derived from V3 Step 1 together with E2.
5. Theorem V6: S_P is unbounded below for d ≥ 3, γ = h is a conformal-direction maximum, and the resulting ELBO-typing contradiction (a negative ELBO is bounded below).
6. The identification γ = the design, reconciling obstruction O3 with Theorem A4.5 as one fact rather than two.
7. Naming S_vol as the Jeffreys/Rissanen geometric complexity of the context-indexed model family — which gives it an honest role as a diagnostic and explains why minimizing it alone collapses the section.

## verdict_for_commit

DO NOT COMMIT TO THE INDUCED-VOLUME HORN AS THE PRIMARY ACTION. It trades a typing problem for an analysis catastrophe, and the catastrophe is strictly worse than the problem it solves.

Blunt summary of the trade. The typing problem was: the Dirichlet form needs an exogenous base cometric and density (05c:1362-1366, obstruction O3). The catastrophe you buy is: (i) the functional is exactly constant on Diff(C,∂C)-orbits, so no sublevel set is bounded in any Sobolev norm and the direct method is dead in every dimension, on every fiber, with any boundary data (Theorem V2, verified numerically); (ii) this is your own PA-3 lemma firing again, now with a group that has no compact reduction — the repair that saved the fiber sector (pick compact G) does not exist for Diff(C); (iii) the functional's own relaxation leaves the section category, so its minimizers are integral currents in the fiber and not agents; and (iv) sqrt(det h) is degree d in Dq while every ELBO-derived lattice KL sum is degree 2, so the two objects can be the same only at d = 2.

On the specific claim under test: your Polyakov algebra is CORRECT. Varying γ does give γ_{μν} = h_{μν} and S_P|on-shell = S_vol for d ≠ 2; I verified the Euler–Lagrange residual symbolically at d = 1,2,3,4. But for d ≥ 3 that variation is a MAXIMIZATION over the conformal factor and S_P is unbounded below (S_P(λ) = ½[λ^{d/2−1}A − (d−2)λ^{d/2}V] → −∞). A negative ELBO is bounded below by −log p(o). So the two halves of the proposal — "γ is an auxiliary field whose on-shell value is determined by the beliefs" and "S_P is the continuum limit of the ELBO-derived lattice sum" — are mutually inconsistent for d ≥ 3. And option (a) does not keep coercivity: S_P[φ*q, φ*γ] = S_P[q,γ] exactly, so the joint functional has precisely the same non-coercivity as S_vol. What buys you the good analysis is FIXING γ, not varying it. That distinction is the whole ballgame and the proposal as written elides it.

The finding that should change your plan. Theorem V3 says S_vol is not one Diff-invariant option among several — it is the ONLY local Diff-invariant first-order scalar built from h. So there is no better Diff-invariant action to go looking for. Combined with V2, the conclusion is not "S_vol is hard" but "no local Diff(C)-invariant action admits the direct method." Full base-diffeomorphism invariance and existence-by-the-direct-method are incompatible, full stop. That is the clean negative.

RECOMMENDATION: (c), a corrected version of (a). Treat γ and the base density as DESIGN data, not as intrinsic structure and not as a dynamical field. The refining lattice family Λ_h supplies γ; that is exactly the object Theorem A4.5 (wave2-01:406-413) already says pins the otherwise-undetermined continuum extension — O3 and A4.5 are the same fact stated twice. N1 survives in the manuscript's own words (02:25-26; 12_philosophy:34-35: the design is a declared subset, not a law on C), and this reinterprets PIFB2.tex:1731's √|g|(c)dc as design density rather than intrinsic base metric, which removes E8's incompatibility without abandoning either document. The primary object becomes the fixed-γ Dirichlet form: convex (not merely quasiconvex) in Dq, coercive, wlsc, degree-2 matching E2, and an exact ELBO component at every finite lattice by E3. Keep S_vol — but as the unique Diff-invariant DIAGNOSTIC, which is what it is good for: by the area formula it is the Jeffreys/Rissanen geometric complexity of the family {q(c)}, a design-independent number to report alongside a design-dependent action, and precisely the right statistic for testing whether your conclusions depend on the design. The open question then becomes well-posed and answerable: for which section classes is the h → 0 limit independent of the refining sequence modulo Diff(C)? That is a Γ-convergence problem, not a mystery.

Two further things you need to hear. First, the wave-2 audit already rejected this exact object for a special case of the reason I am giving (wave2-01:134-136 names sqrt(det h_s^ω) and rejects it as generically degenerate), and your own worklog §3c.6 already records "it is not the h→0 limit of the lattice KL sum" — so the horn was flagged twice before this run and the flags were correct. Second, if you insist on a Diff-invariant primary action anyway, the ONLY defensible dimension is d = 2, and three fully independent arguments say so (boundedness below of S_P; homogeneity match with the KL limit; existence of a conformal gauge reducing Diff to finite-dimensional moduli). Your coordinator independently recommended scoping the continuum program to d = 2 by an entirely different route (roadmap-review:186). Three arguments and a referee converging on d = 2 is the strongest signal in this whole file.
