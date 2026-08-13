# panelA-T-GRAD-derivation

*Recovered verbatim from workflow journal.jsonl, 2026-08-13. Agent a6ea5ca8.*

## target

T-GRAD — derive the covariant Fisher gradient (Dirichlet) term of the continuum action from an exact ELBO term, at fixed finite N, refining only the base lattice

## status

PARTIAL

## theorem_statement

PART I (PROVED — deterministic lattice→continuum theorem, items 1–4).

Let C = (R/LZ)^d be the flat d-torus with Euclidean metric; let Λ_h = (hZ/LZ)^d, L/h ∈ N. Let π: P → C be a smooth principal G-bundle with connection ω (local form A ∈ C^1(C, g⊗R^d)); let ρ: G → Bimeas(K) be a smooth action on a standard-Borel sample space by parameter-independent bimeasurable maps, ρ̂(g) := ρ(g)_# the induced action on laws, B a K-dimensional regular parametrized-measure model on K preserved by ρ̂ with induced parameter action Θ: G × Θ_B → Θ_B, E = P ×_{ρ̂} B the associated bundle, and Ω^A_{c,c'}: E_{c'} → E_c the ω-parallel transport along the straight segment. Let q: C → E be a C^2 section with image in a compact regular stratum, and let

  D^A_μ q := ver^ω(Tq(∂_μ)) = ∂_μ θ + ζ_{A_μ}(θ) ∈ T_{q(c)}B,  ‖D^A q‖²_{g^F(q)} := Σ_{μ=1}^d g^F_{q(c)}(D^A_μ q, D^A_μ q),

with ζ the fundamental vector field of the Θ-action and g^F the Fisher metric of B. Assume (H1)–(H7) below. Then, with E_{c,±μ}(h) := KL(q(c) ‖ (Ω^A_{c, c±he_μ})_# q(c±he_μ)):

(A) [oriented-edge form] h^{d-2} Σ_{c∈Λ_h} Σ_{μ=1}^d E_{c,+μ}(h) = (1/2)∫_C ‖D^A q‖²_{g^F} dc + O(h), and if additionally q ∈ C^3 the O(h) coefficient is exactly
    ∫_C Σ_μ [ (1/2) g^F_{q(c)}(D^A_μ q, (D^A_μ)² q) − (1/6) W_{q(c)}(D^A_μ q, D^A_μ q, D^A_μ q) ] dc,
   W_{ijk}(θ) := E_θ[∂_i∂_j∂_k log p_θ], equivalently −(1/6)W = (1/6)T_AC + (1/2)Γ^{(e)} with T_AC the Amari–Chentsov tensor E_θ[ℓ_iℓ_jℓ_k] and Γ^{(e)}_{ij,k} = E_θ[(∂_i∂_jℓ)ℓ_k] the exponential-connection coefficient. This O(h) term is generically NONZERO and is NOT a total derivative.

(B) [symmetric / all-directed-edge form, which is the form the ELBO's source block actually produces]
    (h^{d-2}/2) Σ_{c∈Λ_h} Σ_{μ=1}^d [E_{c,+μ}(h) + E_{c,−μ}(h)] = (1/2)∫_C ‖D^A q‖²_{g^F} dc + O(h²) (C^4 data; o(h) under C^3).
   The full h³ coefficient — Amari–Chentsov, exponential-connection, AND covariant-acceleration parts together — cancels EXACTLY and POINTWISE at every site by ±-parity of the transported-back curve. No discrete integration by parts and no boundary term is involved.

(C) [gauge covariance] Each summand, and hence each lattice functional, is exactly invariant at every finite h under passive local frame change g: C → G. Both limits are the connection-relative Fisher pullback h_q^ω of Theory/05c_pullback_geometry.tex:109-122 integrated against Lebesgue measure; they depend on ω, not only on q.

(D) [base cometric is declared, not derived] For a general site-edge set {a_k}⊂R^d with weights w_k, the leading term is (1/2) g^F_{ij}(D_μ q)^i (D_ν q)^j G^{μν} with G^{μν} = Σ_k w_k a_k^μ a_k^ν, the SECOND MOMENT of the edge-displacement measure; the h³ coefficient is contracted with its THIRD moment, and vanishes iff that third moment vanishes (in particular for every centrally symmetric edge set).

PART II (REFUTED — item 5; the ELBO origin does not survive in the required form).

Let A = {i}×Λ_h, and instantiate the tied-replica theorem (docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/typed-construction.md, exact-elbo-proof.md) with the belief source set of agent-site (i,c) equal to its 2d base neighbours and lagged sources u_{c,c'} = (Ω^A_{c,c'})_# q_i^n(c'). Then:

(E) [scaling no-go] The exact negative ELBO is a counting-measure sum in which every block carries coefficient ≤ 1 (β is a probability row). After ANY single global rescaling λ_h the base-neighbour sector and the private/observation sectors cannot both have finite nonzero limits: the required relative weight is h^{-2} → ∞ while β_{c,c'} ≤ 1. With λ_h = h^d the gradient sector vanishes; with λ_h = h^{d-2} the observation sector diverges as h^{-2}.

(F) [repair of (E), by postulate] Replicating the base-neighbour label-copy block m_h := ⌈d h^{-2}⌉ times per agent-site keeps P_h^n normalized and Q-independent and multiplies the block by exactly m_h (licensed by boundary-counterexamples.md:52-59: positive integer coefficients are representable by repeated independent copies with tied recognition). This reconciles the scalings, but m_h is an extra declared h-dependent generative postulate, not a consequence of the theorem.

(G) [row entropy — the answer to 5(a) vs 5(b)] BOTH freezing β = π and optimizing β give the SAME limit. At unit temperature the envelope value is −log Z = Ē − (1/2)Var_π(E) + O(E³) with Ē = Σ_b π_b E_b, and the optimized row entropy is exactly KL(β*‖π) = (1/2)Var_π(E) + O(E³) = (h⁴/8)Var_μ(g^F(D^A_μ q, D^A_μ q)) + O(h⁶). After m_h and h^d weighting this contributes (d/8)h² ∫Var_μ(g^F(D_μq,D_μq)) dc → 0. The row-entropy term VANISHES; it neither diverges nor leaves a finite extra term. Moreover at temperature τ ≠ 1 the leading term Ē is unchanged (only the O(h⁴) correction is τ-dependent), so the deployed τ = κ√K_q is invisible to the gradient sector at leading order.

(H) [DECISIVE NEGATIVE — the lag converts the Dirichlet term into a mass term] Because the source field must be H_n-measurable, the block scores q_i^{n+1}(c) against transported q_i^n(c'). Write q_i^{n+1} = exp_{q_i^n}(hφ) for the rescaled increment φ. Then with the (F) weighting

  h^d Σ_{c∈Λ_h} m_h Σ_b β_b KL( q_i^{n+1}(c) ‖ (Ω^A)_# q_i^n(c') )  →  (d/2)∫_C g^F_{q_i^n}(φ, φ) dc + (1/2)∫_C ‖D^A q_i^n‖²_{g^F} dc.

The covariant-Fisher Dirichlet integral appears, but as an ADDITIVE CONSTANT of the frozen history section; the only dependence on the free recognition variable is a positive-definite Fisher MASS term whose unique minimizer is φ = 0. At the h^{-2} strength required to produce a Dirichlet limit the base-neighbour block acts as an infinitely stiff pin to the previous section (a belief-inertia term), not as a Dirichlet smoother of the current one. Any configuration with q^{n+1} ≠ q^n on a positive-measure set makes the block diverge as h^{-2}.

(I) [general no-go] If the sources u_{c,c'} are Q-independent and lim inf_h min_{c'~c} KL(q(c)‖u_{c,c'}) ≥ δ > 0 on a set S ⊆ C of positive measure, then h^{d-2}Σ_{edges}KL ≥ d δ |S| h^{-2}(1+o(1)) → +∞. Finiteness of the limit therefore FORCES the generative source field to agree with the recognition section to O(h) in the Fisher metric. This is a self-consistency (fixed-point) condition, not an identity, and holds for every d ≥ 1.

CONCLUSION. Items 1, 2, 3, 4 are PROVED. Item 5 is REFUTED in the strong form: the gradient sector is NOT genuinely ELBO-derived. It is available only (i) after an extra declared h-dependent replication postulate, AND (ii) only at a self-consistent stationary configuration q_i^{n+1} = q_i^n, i.e. in the iterated limit lim_{h→0} lim_{n→∞} whose exchange is unproven. The status of Part I is therefore a deterministic-action theorem about a fixed smooth section, not an ELBO derivation.

## hypotheses

### 1

(H1) Base: C = (R/LZ)^d flat torus, Euclidean metric, Λ_h = (hZ/LZ)^d with L/h ∈ N. (Torus chosen to eliminate boundary terms; on a domain with boundary the interior estimate is unchanged and the O(h) boundary layer contributes h^{d-2}·O(h^{-(d-1)})·O(h²) = O(h) → 0.)

### 2

(H2) Model regularity (an explicit unpacking of Theory/05c_pullback_geometry.tex:30-42, hyp:pb-regular-models). Θ ⊆ R^K open, {p_θ} densities w.r.t. a σ-finite ν. (a) For ν-a.e. x, θ ↦ p_θ(x) is strictly positive and C^3 on Θ. (b) Local domination: for every compact Θ_0 ⊂ Θ there is an open U with Θ_0 ⊂ U, Ū ⊂ Θ compact and convex, and G ∈ L^1(ν) with |∂^α p_θ(x)| ≤ G(x) for all |α| ≤ 3, θ ∈ U, ν-a.e. x. (c) Third-order score domination: there is B ≥ 0 with sup_{η∈U}|∂_i∂_j∂_k log p_η(x)| ≤ B(x) and M_3 := sup_{θ∈U} E_θ[B] < ∞. (d) g^F(θ) = E_θ[ℓ_iℓ_j] is finite, continuous and positive definite on U. (b) is what licenses the first and second Bartlett identities; (c) is what makes the third-order Taylor remainder UNIFORM over lattice sites — the ground-phase audit correctly flags that the prior run never states it.

### 3

(H3) Group action: ρ: G → Bimeas(K) acts by PARAMETER-INDEPENDENT bimeasurable sample-coordinate changes preserving B (05c:37-41). This is exactly the hypothesis of prop:pb-statistical-tensor-descent (05c:59-63) and it is what makes ρ̂(g) a g^F-isometry, T_AC-preserving, and KL-invariant. It fails for arbitrary diffeomorphisms of a parameter chart (05c:84-87).

### 4

(H4) Section: q: C → E is C^2 (C^3 for the identified O(h) coefficient in (A); C^4 for the O(h²) rate in (B)), with image contained in a compact subset Θ_0 of the regular stratum. Compactness of C + continuity gives a compact U ⊃ Θ_0 containing all transported-back points θ̂_c(ε) for |ε| ≤ h_0, uniformly in c.

### 5

(H5) Connection: A ∈ C^1(C, g ⊗ R^d) is FIXED (declared, not dynamical), and Θ: G × Θ_B → Θ_B is smooth, so ε ↦ θ̂_c(ε) is C^2 (resp. C^3, C^4) with derivatives bounded uniformly in c ∈ C. Determination of ω is part of the data: h_q^ω is connection-dependent (05c:220-231 exhibits h = 0 vs h = a_0²dx² for the same section).

### 6

(H6) All KL divergences are finite on the relevant edges, i.e. the transported neighbour law is mutually absolutely continuous with q(c). Guaranteed by (H2)(a) + (H4) for small h. Exact-identity claims require the SPD floor eps = 0 (PIFB2.tex:187, KL_REGULARISER_EPS default 1e-4 gives only O(eps) agreement).

### 7

(H7) For Part II only: the tied-replica hypotheses of docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/typed-construction.md — finite agent-site set, standard-Borel blocks, normalized positive source rows, positive finite evidence, absolute continuity of Q against the fixed-observation slice of P_h^n, and sources that are H_n-measurable (Q-independent).


## derivation

DERIVATION. All five required items are worked below. Classification tags: {DERIVATION}, {APPLICABLE_THEOREM}, {COUNTEREXAMPLE}, {CONJECTURE}. Every claim about a document carries a file:line citation I actually opened. Two independent machine verifications were run (symbolic, SymPy; numerical, high-resolution lattice) and are reported inline with their exact numbers.

════════════════════════════════════════
§0. WHAT THE ESTABLISHED SOURCES ALREADY GIVE, AND WHAT THEY DO NOT
════════════════════════════════════════

Theory/05c_pullback_geometry.tex:556-570 (cor:pb-transported-divergence-quadratic, status ESTABLISHED) gives the INTRINSIC second-order statement D(s(c), ŝ_γ(ε)) = (ε²/2) h^ω_{s,D}(γ̇,γ̇) + O(ε³) with h^ω_{s,D} = h_s^ω for the regular KL contrast. Theory/05c:578-587 then states explicitly that the ε³ coefficient "is not determined by c^ω_{s,D} alone. It also contains the covariant acceleration of ŝ_γ and the connection coefficient selected by the one-sided divergence jet." That is a WARNING, not a computation; §3 below computes it.

docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/lattice-continuum-asymptotics.md:11-18 gives the same expansion in a parameter chart, and :20-22 gives h^{d-2} "by counting"; :33-34 concedes "These are consistency expansions on smooth sequences, not Gamma-convergence proofs." No convergence theorem, no uniformity, no remainder identification, and no ELBO-origin analysis exists anywhere. Theory/ contains NO lattice at all (verified by the ground phase and by my own grep over Theory/*.tex: the only "lattice" hits are Banach lattice at 07b:1054,1104 and Boolean-lattice Möbius projectors at 07b:1191). Theory/05c:1359-1366 (status NOT-CLAIMED) records that a scalar gauged sigma energy "would additionally require a base cometric, a base density, channel weights, boundary conditions, and a decision about whether the connection is fixed or dynamical. None is selected."

I therefore treat Part I as work to be done from scratch, and I record in §6 exactly which of 05c:1359-1366's five missing data the lattice supplies (all five, as DECLARATIONS, not derivations).

════════════════════════════════════════
§1. ITEM 3 — WHERE D^A COMES FROM: TRANSPORT, THE VERTICAL/HORIZONTAL SPLIT, GAUGE COVARIANCE
════════════════════════════════════════
{DERIVATION}

This must come first because items 1, 2, 4 all expand along the transported-back curve.

1.1 The associated bundle and why ρ_* is NOT matrix multiplication.
Let (K, 𝒦) be standard Borel and ρ: G → Bimeas(K) an action by bimeasurable bijections, parameter-independent (H3). The induced action on laws is the PUSHFORWARD ρ̂(g) := ρ(g)_#: P(K) → P(K). It preserves the model B and hence induces Θ: G × Θ_B → Θ_B on parameters. E := P ×_{ρ̂} B. The fundamental vertical field of ξ ∈ g at θ ∈ Θ_B is

  ζ_ξ(θ) := (d/dt)|_{t=0} Θ(exp(tξ), θ) ∈ T_θ B.

Theory/05c:177-182 is explicit that this is the only available object: "For a general law fiber B ⊆ P(K) the fiber is not a vector space and the linear expression ρ̂_{x*}(A) is undefined; it is available only in a declared fiberwise-linear associated-vector-bundle realization, where it agrees with ζ_{A(X)}." I use ζ throughout.

CONCRETE INSTANCE (the deployed one). G = GL(K_q,R), K = R^{K_q}, ρ(g)k = gk. Then ρ̂(g)N(μ,Σ) = N(gμ, gΣg^T) — this matches PIFB2.tex:316 verbatim ("transforming μ_j ↦ R_{ij}μ_j and Σ_j ↦ R_{ij}Σ_j R_{ij}^⊤"), and for ξ ∈ gl(K_q),

  ζ_ξ(μ, Σ) = (ξμ, ξΣ + Σξ^T).

Note the congruence (sandwich) form in the covariance slot. This is emphatically NOT "matrix multiplication on a density"; a density-level version does not exist because ρ̂(g) changes the reference measure by the Jacobian |det g|.

1.2 The vertical/horizontal split, verified explicitly.
In a local trivialization P|_U ≅ U × G with local connection form A = A_μ dc^μ, Theory/05c:172-177 fixes the convention frame-free: "in a local trivialization the horizontal lift of X at (c,β) is (X, −ζ_{A(X)}β)". Hence at e = (c, θ):

  T_e E = V_e E ⊕ H^ω_e E,  V_e E = T_θ B,  H^ω_e E = { (X, −ζ_{A(X)}(θ)) : X ∈ T_c C }.

For the section c ↦ (c, θ(c)) we have Tq(X) = (X, ∂_X θ). Subtracting the horizontal lift of X at q(c):

  ver^ω(Tq(X)) = (X, ∂_Xθ) − (X, −ζ_{A(X)}θ) = (0, ∂_Xθ + ζ_{A(X)}θ).

  ⟹  D^A_μ q := ver^ω(Tq(∂_μ)) = ∂_μθ + ζ_{A_μ}(θ) ∈ T_{q(c)} B.   (1.1)

This is a genuinely VERTICAL object: a tangent vector to the manifold of laws, i.e. (as a signed measure) a mass-zero measure ≪ q(c) whose Radon–Nikodym derivative — the score of the direction — lies in L²_0(q(c)). Its Fisher norm is g^F_{q(c)}(D^A_μq, D^A_μq) = ‖d(D^A_μ q)/dq(c)‖²_{L²(q(c))}. This is Definition eq:pb-fisher-pullback (Theory/05c:109-122), h_q^ω(X,Y) = g^F(D^ω q(X), D^ω q(Y)).

1.3 The transport expansion, and that it produces exactly (1.1).
Let Ω^A_{c,c'} : E_{c'} → E_c be ω-parallel transport along the straight segment. In the trivialization the horizontal-lift ODE gives, along c(ε) = c + ε e_μ,

  Ω^A_{c, c+he_μ} = ρ̂( exp( ∫_c^{c+he_μ} A ) ) + O(h²) = ρ̂( exp(h A_μ(c)) ) + O(h²).

Define the TRANSPORTED-BACK CURVE (Theory/05c:543-547, eq:pb-transported-section-curve)

  θ̂_c(ε) := Θ( g_c(ε), θ(c + ε e_μ) ),  g_c(ε) := the transport group element,  θ̂_c(0) = θ(c).   (1.2)

Differentiating at ε = 0 and using (d/dε)|_0 Θ(g_c(ε), θ(c)) = ζ_{A_μ(c)}(θ(c)):

  θ̂_c'(0) = ∂_μθ(c) + ζ_{A_μ(c)}(θ(c)) = D^A_μ q(c).   (1.3)

This reproduces Theory/05c:549-553, eq:pb-transported-section-velocity, which I have thus verified rather than merely cited. NOTE: (1.2) is defined for ε ∈ [−h, h] along the SAME base line, so the two lattice neighbours c ± h e_μ are the two endpoints θ̂_c(+h), θ̂_c(−h) of ONE smooth curve through ε = 0. This single fact is what drives the crux cancellation in §3. The opposite sign convention for A flips ζ → −ζ; since the limit functional is quadratic in D^A and A is arbitrary declared data, nothing downstream depends on the choice.

1.4 Gauge covariance is EXACT at finite h (not only in the limit).
Under a passive local frame change g: C → G, q'(c) = ρ̂(g(c)^{-1}) q(c) and Ω'_{c,c'} = ρ̂(g(c)^{-1}) Ω_{c,c'} ρ̂(g(c')). Since ρ̂(g) is a bimeasurable pushforward, KL is invariant under a COMMON pushforward of both arguments, so

  KL( q'(c) ‖ Ω'_{c,c'#} q'(c') ) = KL( ρ̂(g_c^{-1})q(c) ‖ ρ̂(g_c^{-1}) Ω_{c,c'#} q(c') ) = KL( q(c) ‖ Ω_{c,c'#} q(c') ).   (1.4)

Every summand of the lattice functional is separately invariant, at every h, before any limit. In the limit this is thm:pb-pullback-gauge-invariance (Theory/05c:124-144). {APPLICABLE_THEOREM — hypotheses: (H3) supplies the parameter-independent bimeasurable representation required by prop:pb-statistical-tensor-descent, Theory/05c:59-63, whose proof at :65-82 is exactly the pushforward-unitary argument.}

TWO SCOPE LIMITS I do not hide. (i) This is PASSIVE covariance only. Theory/05c:146-154 gives the active counterexample: on the trivial R-bundle over R with the normal location fiber, an active bundle automorphism carries h = 0 to dx². (ii) h_q^ω depends on ω: Theory/05c:220-231 gives h = 0 for the zero connection vs h^{A'} = a_0² dx² for A' = a_0 dx on the SAME constant section. So the limit functional is a functional of the PAIR (ω, q), and the lattice inherits this exactly. PIFB2.tex:341's caveat (deployed symmetry is the global diagonal redundancy only, because the observation channel is held fixed) does not bite here: the gradient sector contains no observation channel.

════════════════════════════════════════
§2. ITEM 1 — THE LOCAL EXPANSION, WITH UNIFORM REMAINDER
════════════════════════════════════════
{DERIVATION, with hypotheses of the cited APPLICABLE_THEOREM verified}

Write D(θ, η) := KL(p_θ ‖ p_η) = ∫ p_θ log p_θ dν − ∫ p_θ log p_η dν, and prime for η-derivatives.

LEMMA 2.1 (jets of KL in the second argument). Under (H2), on U:
 (i) D(θ, θ) = 0;
 (ii) ∂'_i D(θ, η)|_{η=θ} = −E_θ[ℓ_i(θ)] = 0;
 (iii) ∂'_i∂'_j D(θ, η)|_{η=θ} = −E_θ[∂_i∂_j log p_θ] = E_θ[ℓ_iℓ_j] = g^F_{ij}(θ);
 (iv) ∂'_i∂'_j∂'_k D(θ, η) = −E_θ[∂_i∂_j∂_k log p_η], and sup_{θ,η∈U} |·| ≤ M_3 < ∞.

Proof. Only the second integral depends on η, and (H2)(b),(c) license differentiation under the integral sign three times (dominated convergence with dominating function G for the p_θ-side normalizations and B for the η-side log-derivatives). (ii): E_θ[ℓ_i] = ∫∂_i p_θ dν = ∂_i ∫ p_θ dν = 0, the first Bartlett identity, licensed by (H2)(b) at |α| = 1. (iii): the displayed equality of the two expressions is the second Bartlett identity, obtained from ∂_i∂_j∫p_θ dν = 0 ⟹ E_θ[∂_i∂_jℓ + ℓ_iℓ_j] = 0, licensed by (H2)(b) at |α| = 2. (iv) is immediate with the bound from (H2)(c). ∎

Note that (iii) is the DIAGONAL second jet in the second argument, whereas Theory/05c:509-538 (prop:pb-kl-divergence-jets) states the MIXED jet −∂_i∂'_j KL = E_θ[ℓ_iℓ_j]. Both equal g^F; they are different identities and I use (iii). Hypotheses of prop:pb-kl-divergence-jets: it requires hyp:pb-regular-models (05c:30-42), which (H2) instantiates verbatim; I additionally verified its content symbolically (§3.4).

PROPOSITION 2.2 (uniform Taylor). Under (H2), for θ ∈ Θ_0 and η ∈ U with the segment [θ,η] ⊂ U,

  | D(θ, η) − (1/2) g^F_θ(η−θ, η−θ) | ≤ (K³ M_3 / 6) |η − θ|³.   (2.1)

Proof. Taylor's theorem with Lagrange remainder applied to η ↦ D(θ,η) on the convex set U, using Lemma 2.1(i)–(iii) for the vanishing/identified low-order terms and 2.1(iv) for the uniform third-derivative bound. ∎

The constant in (2.1) is UNIFORM over θ ∈ Θ_0 and hence over lattice sites. This is precisely the uniformity the prior run's lattice-continuum-asymptotics.md never states (it writes O(h³) with no uniformity claim), and without it the h^{-d}-fold sum of the remainders is uncontrolled.

COROLLARY 2.3 (the required statement, item 1). For a C² curve t ↦ θ(t) in U with θ(0) = θ_0, θ'(0) = v,

  KL( p_{θ_0} ‖ p_{θ(t)} ) = (1/2) t² g^F_{θ_0}(v, v) + R(t),  sup |R(t)| ≤ C t³,

with C depending only on K, M_3 and sup_{|t|≤h_0}|θ''(t)|. If the curve is C³ with θ''(0) = w, θ'''(0) = u, then the exact t³ coefficient is

  (1/2) g^F_{θ_0}(v, w) − (1/6) W_{θ_0}(v, v, v),  W_{ijk}(θ) := E_θ[∂_i∂_j∂_k log p_θ].   (2.2)

Proof. Write Δ(t) = θ(t) − θ_0 = tv + (t²/2)w + O(t³). Then (1/2)g(Δ,Δ) = (t²/2)g(v,v) + (t³/2)g(v,w) + O(t⁴), and the cubic term of the Taylor expansion contributes (1/6)(−W)(v,v,v)t³ + O(t⁴) by Lemma 2.1(iv) evaluated at η = θ_0. Sum. ∎

Combining with (1.3): with θ̂_c the transported-back curve of (1.2), v = D^A_μ q(c) and Corollary 2.3 gives

  E_{c,±μ}(h) = (h²/2) g^F_{q(c)}(D^A_μq, D^A_μq) ± h³ · c_3(c,μ) + O(h⁴),  c_3 := (1/2)g^F(v,w) − (1/6)W(v,v,v).   (2.3)

This is the quantitative, uniform form of cor:pb-transported-divergence-quadratic (Theory/05c:556-570).

════════════════════════════════════════
§3. ITEM 2 — THE CRUX: WHICH ARGUMENT ORDER, THE THIRD ORDER, AND WHETHER IT SURVIVES
════════════════════════════════════════
{DERIVATION + independent symbolic verification}

3.1 Identification of W with the Amari–Chentsov and exponential-connection tensors.
Set T_AC,ijk := E_θ[ℓ_iℓ_jℓ_k] (Theory/05c:50-53, eq:pb-fiber-amari) and Γ^{(e)}_{ij,k} := E_θ[(∂_i∂_j log p_θ) ℓ_k] (Amari's α = 1 connection). Differentiating the second Bartlett identity E_θ[∂_i∂_j ℓ] = −g_ij in θ_k, and separately differentiating g_ij = E_θ[ℓ_iℓ_j]:

  Γ^{(e)}_{ij,k} + W_{ijk} = −∂_k g_ij,  ∂_k g_ij = T_AC,ijk + Γ^{(e)}_{ki,j} + Γ^{(e)}_{kj,i}
  ⟹  W_{ijk} = −( T_AC,ijk + Γ^{(e)}_{ki,j} + Γ^{(e)}_{kj,i} + Γ^{(e)}_{ij,k} ).   (3.1)

Contracting with v³ (∂_i∂_jℓ is symmetric in i,j): −W(v,v,v) = T_AC(v,v,v) + 3Γ^{(e)}(v,v,v), so the t³ coefficient (2.2) is equivalently

  c_3 = (1/2) g^F(v,w) + (1/6) T_AC(v,v,v) + (1/2) Γ^{(e)}(v,v,v).   (3.2)

SYMBOLIC VERIFICATION (SymPy). Model N(μ,σ²) in the chart θ = (μ,σ) — deliberately NOT an exponential-family natural chart, so Γ^{(e)} ≠ 0. Computed exactly:
  g = diag(1/σ², 2/σ²);  T_AC: T_112 = 2/σ³, T_222 = 8/σ³;  Γ^{(e)}: Γ_{12,1} = Γ_{21,1} = −2/σ³, Γ_{22,2} = −6/σ³;  W: W_112 = 2/σ³, W_222 = 10/σ³.
Identity (3.1) contracted with δ = (a,b): W(δ,δ,δ) = (6a²b + 10b³)/σ³ and −(T_AC + 3Γ^{(e)})(δ,δ,δ) = −[(6a²b+8b³) + 3(−4a²b−6b³)]/σ³ = (6a²b + 10b³)/σ³. IDENTITY CONFIRMED.

3.2 WHICH argument order matters at third order, and by exactly how much.
Expanding the exact Gaussian KL symbolically at θ_0 = (1/3, 7/5), δ = (a,b):
  forward  KL(p_{θ_0} ‖ p_{θ_0+tδ}):  t² coeff = (1/2)g(δ,δ) ✔;  t³ coeff = −(1/6)W(δ,δ,δ) ✔ (matches (2.2) exactly, and also matches (3.2));
  reverse  KL(p_{θ_0+tδ} ‖ p_{θ_0}):  t³ coeff = −(1/6)W + (1/6)T_AC.
  DIFFERENCE (reverse − forward) at t³ = (1/6) T_AC(δ,δ,δ), verified symbolically to be exactly (125 a²b/343 + 500 b³/1029) = (1/6)T_AC(δ,δ,δ).
This is an independent confirmation of Theory/05c:509-538 ("the difference of the two mixed third jets is the Amari–Chentsov tensor"), and it answers the item-2 question directly: THE ARGUMENT ORDER CHANGES THE h³ TERM BY EXACTLY ONE SIXTH OF THE AMARI–CHENTSOV TENSOR, and by nothing at second order. Independent analytic cross-check on an exponential family in natural coordinates (Γ^{(e)} = 0, W = −T_AC): forward = (t²/2)g + (t³/6)T_AC, reverse = (t²/2)g + (t³/3)T_AC — both reproduced exactly by (2.2)/(3.2).

3.3 THE CRUX RESOLVED: exact pointwise ±-cancellation, NOT integration by parts.
By (1.2) the two lattice neighbours of c in direction μ are θ̂_c(+h) and θ̂_c(−h) of ONE smooth curve. Hence by (2.3),

  E_{c,+μ}(h) + E_{c,−μ}(h) = h² g^F_{q(c)}(D^A_μq, D^A_μq) + O(h⁴).   (3.3)

THE ENTIRE h³ TERM CANCELS EXACTLY AND POINTWISE AT EVERY SITE — the Amari–Chentsov part, the exponential-connection part, AND the covariant-acceleration part g^F(v,w) together. No discrete summation by parts is used; there are no boundary terms; the cancellation is insensitive to the section, the connection, the argument order, and the base geometry. It is pure parity of the transported-back curve.

SYMBOLIC VERIFICATION. With θ̂(ε) = θ_0 + εv + (ε²/2)w + (ε³/6)u and free symbols v_1,v_2,w_1,w_2,u_1,u_2, the exact Gaussian KL gives E(+h) + E(−h) = h²(v_1² + 2v_2²)/σ_0² + O(h⁴) with h³ coefficient identically 0, independently of w and u. CONFIRMED.

3.4 What happens if you do NOT symmetrize — and why it is still harmless, but only just.
For the one-sided (oriented unordered-edge) sum the h³ term does NOT cancel pointwise. It nevertheless dies by power counting, because h^{d-2} · h³ · (number of edges ~ d h^{-d}) = O(h). But it is NOT zero at order h, and — contrary to a natural guess — it is NOT a total derivative:

NUMERICAL VERIFICATION (this is the check that caught and killed my own initial "it integrates away" argument). Setup: d = 1, C = circle [0,1), fiber N(μ,σ²), G = GL(1,R)_+ acting by x ↦ gx so ρ̂(g)N(μ,σ²) = N(gμ, g²σ²), ζ_α(μ,σ) = (αμ, ασ); μ(c) = 0.3+0.4 sin2πc, σ(c) = 1+0.3 cos2πc, α(c) = 0.5+0.6 sin4πc; transport = exact abelian path-ordered exponential exp(∫A). Target (1/2)∫‖D^Aq‖²_{g^F} dc = 4.529833403250.

  M      one-sided S1        err1        err1/h      symmetric S2        err2        err2/h²
   64    4.4755538671    −5.428e−02    −3.47389     4.5258130936    −4.020e−03    −16.46719
  256    4.5170074516    −1.283e−02    −3.28344     4.5295820712    −2.513e−04    −16.47129
 1024    4.5266738865    −3.160e−03    −3.23535     4.5298176948    −1.571e−05    −16.47155
 2048    4.5282575682    −1.576e−03    −3.22731     4.5298294761    −3.927e−06    −16.47160

One-sided error is Θ(h) with Richardson-extrapolated coefficient −3.21927. Predicted from (2.2): ∫[(1/2)g^F(v,w) − (1/6)W(v,v,v)]dc = 4.392910 − 7.612181 = −3.219270. AGREEMENT TO SIX SIGNIFICANT FIGURES. Note the two pieces are individually large and of opposite sign and do NOT cancel; and I checked numerically that ∫(1/4) d/dc[g^F(v,v)] dc = −5.6e−11 ≈ 0 (a genuine total derivative on the circle) while ∫(1/2)g^F(v,w) dc = +4.392910 ≠ 0. Hence (1/2)g^F(v,w) is NOT a total derivative: the chart second derivative w = (D^A_μ)²q is not the Levi-Civita covariant derivative of g^F, so metric-compatibility of the GAUGE transport (which does hold, by (H3)) does not make the acceleration term integrate away. This is the correct resolution of the ambiguity flagged at Theory/05c:578-587.

Symmetric error is Θ(h²) with coefficient −16.4716, stable to six figures from M = 512 onward. CONFIRMED.

3.5 Exactly-solvable witness. In the Gaussian mean submodel with FIXED common covariance, Theory/08_infogeometry.tex:238-247 gives KL(N(μ_i,C)‖N(μ_j,C)) = (1/2)(μ_i−μ_j)^T J (μ_i−μ_j) exactly. Then W ≡ 0 and (2.3) is exact with no remainder: E(+h)+E(−h) = h²|v|²_{J} + (h⁴/4)|w|²_{J} identically. The h³ term is thus entirely a covariance-sector / non-location effect, and the symmetric lattice functional is exact up to a computable (h⁴/8)Σ_c|w|²_J.

3.6 General edge sets — the invariant form of the crux.
For a site-edge set {a_k} ⊂ R^d with weights w_k, the leading and subleading terms are

  Σ_k w_k E_{c,a_k}(h) = (1/2) g^F_{ij}(D_μq)^i(D_νq)^j M_2^{μν} + (1/6)·(third-jet tensor)·M_3^{μνρ} + O(h⁴),
  M_2^{μν} := Σ_k w_k a_k^μ a_k^ν,  M_3^{μνρ} := Σ_k w_k a_k^μ a_k^ν a_k^ρ.

CONCLUSION OF THE CRUX: the h³ term is contracted with the THIRD MOMENT of the edge-displacement measure and vanishes identically whenever that third moment vanishes — in particular for every centrally symmetric edge set, which includes the standard 2d-neighbour cubic lattice and the 6-neighbour triangular lattice. Since the exact ELBO's source block for agent-site (i,c) scores q(c) against ALL its neighbours (a centrally symmetric set), the ELBO's own structure automatically supplies the symmetrization and therefore the exact cancellation. That is the one genuinely favourable structural fact discovered here.

════════════════════════════════════════
§4. ITEM 4 — RIEMANN-SUM CONVERGENCE, RATES, AND WHAT FAILS FOR H¹
════════════════════════════════════════
{DERIVATION}

THEOREM 4.1. Under (H1)–(H6) with q ∈ C²:
 (a) h^{d-2} Σ_{c∈Λ_h} Σ_{μ=1}^d E_{c,+μ}(h) = (1/2)∫_C ‖D^Aq‖²_{g^F} dc + O(h);
 (b) (h^{d-2}/2) Σ_{c∈Λ_h} Σ_{μ=1}^d [E_{c,+μ}(h)+E_{c,−μ}(h)] = (1/2)∫_C ‖D^Aq‖²_{g^F} dc + o(h), improving to O(h²) for q ∈ C⁴ with fourth-order domination.

Proof. Write f(c) := ‖D^Aq(c)‖²_{g^F(q(c))} = Σ_μ g^F_{q(c)}(D^A_μq, D^A_μq). By (H2)(d) (continuity of g^F), (H4) (q ∈ C¹ suffices here) and (H5) (A ∈ C⁰), f is continuous on the compact C, hence uniformly continuous with modulus ω_f.
Step 1 (Riemann sum). h^d Σ_{c∈Λ_h} f(c) = Σ_c ∫_{Q_c} f(c) dx where Q_c is the cell of volume h^d, so |h^dΣ_c f(c) − ∫_C f| ≤ |C| ω_f(√d h) → 0. If f ∈ C¹, the midpoint/vertex rule gives O(h); if f ∈ C² and the rule is the symmetric one, O(h²).
Step 2 (uniform local error). By (H4)+(H5) the transported-back points θ̂_c(ε), |ε| ≤ h_0, lie in a fixed compact U for all c, so Proposition 2.2's constant is uniform in c. By Corollary 2.3 with the C² curve, |E_{c,+μ}(h) − (h²/2)g^F(D_μq,D_μq)| ≤ C h³ uniformly in (c, μ).
Step 3 (assembly, one-sided). h^{d-2}Σ_cΣ_μ E_{c,+μ} = (1/2) h^d Σ_c f(c) + Err, |Err| ≤ h^{d-2}·(d·|C| h^{-d})·C h³ = d|C|C·h. Combining with Step 1 gives (a).
Step 4 (assembly, symmetric). By (3.3) the h³ terms cancel pointwise, leaving a per-pair remainder that is o(h³) uniformly under C³ data (Peano remainder with a uniform modulus, using uniform continuity of the third-order jets on the compact U × Θ_0) and O(h⁴) under C⁴ data. The same counting gives o(h) resp. O(h²). ∎

RATES CONFIRMED NUMERICALLY in §3.4: Θ(h) one-sided, Θ(h²) symmetric.

WHAT FAILS FOR MERELY H¹ SECTIONS. Six distinct failures, all real:
 (F1) SAMPLING. For d ≥ 2, H¹(T^d) ⊄ C⁰, so q(c) is not defined at lattice points and the lattice functional is not defined at all. (For d = 1, H¹ ↪ C^{0,1/2}, so only the remaining failures apply.)
 (F2) NO POINTWISE TAYLOR. Even for a precise representative, Corollary 2.3 needs a C² curve; without it the h² coefficient cannot be extracted site by site, and the correct statement would have to be Γ-convergence, which I do not prove.
 (F3) THE h³ TERM IS NOT INTEGRABLE. c_3 is cubic in D^Aq, so identifying the correction needs D^Aq ∈ L³; H¹ gives only L². By Sobolev, H¹(T^d) controls θ in L^{2d/(d-2)} but ∇θ only in L². So the O(h) coefficient in Theorem 4.1(a) does not exist for H¹ data.
 (F4) NO EQUICOERCIVITY. ∫‖D^Aq‖²_{g^F(q)} is a NONLINEAR (state-dependent-coefficient) Dirichlet integral; a Γ-limit needs λI ⪯ g^F(θ) ⪯ ΛI uniformly over the range of θ. For the Gaussian fiber g^F blows up as Σ → 0 and degenerates as Σ → ∞, so sublevel sets are not H¹-compact without an a priori bound confining Σ to a compact subset of Sym_{++}. This is exactly the "compact regular stratum" restriction already registered at claim-ledger.json:207 and the "Singular Fisher strata" failure test at approach-registry.json:117 of the effective-action run.
 (F5) +∞ VALUES. If neighbouring transported laws become mutually singular, an edge KL is +∞ and the lattice functional is not real-valued.
 (F6) NO LINEAR STRUCTURE FOR RECOVERY SEQUENCES. B is a manifold, not a vector space; a Γ-limit construction needs a declared chart or isometric embedding to interpolate, and the answer is chart-dependent unless the interpolation is intrinsic.

SCOPE LIMIT STATED PLAINLY. Theorem 4.1 is POINTWISE convergence of the functional at each fixed C² section. It is NOT Γ-convergence; convergence of minimizers is NOT established. This is the same ceiling recorded at lattice-continuum-asymptotics.md:33-37 ("a common interpolation topology, equicoercivity modulo gauge, liminf, recovery, boundary/topology control, and uniformly vanishing truncation residual"), none of which I supply.

════════════════════════════════════════
§5. ITEM 5 — DOES THE ELBO ORIGIN SURVIVE? (IT DOES NOT)
════════════════════════════════════════
{DERIVATION + COUNTEREXAMPLE}

Instantiate the closed theorem (typed-construction.md:37-111, exact-elbo-proof.md:60-95) with A = {i} × Λ_h and, for a = (i,c), belief source set J_a^q = the 2d base neighbours, sources u_{c,c'} = (Ω^A_{c,c'})_# q_i^n(c'). The exact block is, verbatim from exact-elbo-proof.md:70-72,

  F_a^q = KL(β_a ‖ π_a^q) + Σ_{c'} β_{a,c'} KL( q_a ‖ u_{c,c'} ),  coefficient 1, counting measure over A.   (5.1)

5.1 OBSTRUCTION (E): THE SCALING NO-GO. {DERIVATION}
Per site the sectors of the exact ELBO scale as: private self KL(q‖p) = Θ(1); observation −E_ζ log ℓ = Θ(1); row entropy ≥ 0; base-neighbour block = Σ_{c'}β_{c,c'}·Θ(h²) ≤ Θ(h²) since β is a probability row. There are Θ(h^{-d}) sites. For a common global rescaling λ_h to make BOTH the observation sector and the gradient sector finite and nonzero one needs simultaneously λ_h h^{-d} = Θ(1) and λ_h h^{-d} β h² = Θ(1), i.e. β = Θ(h^{-2}) → ∞, contradicting β ≤ 1. Hence:
  • λ_h = h^d: self and observation sectors converge to ∫KL(q‖p)dc and −∫E log ℓ dc; the GRADIENT SECTOR VANISHES (it is O(h²)).
  • λ_h = h^{d-2}: the gradient sector converges to (1/(2d))∫‖D^Aq‖²; the OBSERVATION SECTOR DIVERGES as h^{-2}, and so does the self sector unless p = q + O(h).
This is a strict no-go WITHIN the theorem as stated, and it is not fixed by any choice of prior row, temperature, or coefficient. Note also that h^{d-2} is not even a quadrature weight: it is (cell volume h^d) × h^{-2}, so boundary-counterexamples.md:61-66's prohibition ("Multiplying a site term by a cell volume w_x changes its probabilistic meaning unless the generative law is changed by replication, tempering, or an explicitly normalized weighted model") applies a fortiori.

5.2 REPAIR (F): REPLICATION IS ADMISSIBLE, BUT IT IS A POSTULATE. {DERIVATION}
Replicate the base-neighbour label-copy block m_h times per agent-site: generative variables (J^{(k)}, X^{(k)}), k = 1..m_h, i.i.d. with law π_{a,c'} u_{c,c'}(dx), recognition tying every copy to the same (β_a, q_a). Each factor is normalized, P_h^n remains normalized and Q-independent, |A|·m_h is finite, and the KL over the product block is exactly m_h times (5.1). This is the sanctioned route: boundary-counterexamples.md:52-59, "Positive integer coefficients can be represented by repeated independent copies with tied recognition; arbitrary real coefficients require a powered or generalized construction and its normalizers." Choosing m_h := ⌈d h^{-2}⌉ (an integer; the ceiling costs a relative O(h²)) and frozen β = π uniform on the 2d neighbours gives, per site,

  m_h · (1/(2d)) Σ_{b=1}^{2d} E_b = (d h^{-2})(1/(2d)) · h² ‖D^Aq‖² = (1/2)‖D^Aq‖²,

so h^d Σ_c → (1/2)∫‖D^Aq‖² dc — the target's constant, with the self and observation sectors simultaneously finite. The scalings are reconciled. BUT m_h is an extra DECLARED, h-DEPENDENT generative postulate: nothing in the ELBO, in PIFB2, or in Theory/ derives a replication multiplicity that grows like the inverse square of the lattice spacing. It is the exact lattice-field-theory statement "the kinetic term carries two derivatives" reinserted as a copy count. Honest label: POSTULATE.

5.3 ANSWER TO 5(a) vs 5(b): BOTH WORK, AND THE ROW ENTROPY VANISHES. {DERIVATION + numerical verification}
At unit temperature the envelope identity (PIFB2.tex:717-733) gives min_β[KL(β‖π) + Σ_bβ_bE_b] = −log Z, Z = Σ_bπ_b e^{−E_b}, β*_b = π_b e^{−E_b}/Z. Expanding for E_b = O(h²):

  −log Z = Ē − (1/2)Var_π(E) + O(E³),  Ē := Σ_bπ_bE_b;  KL(β*‖π) = (1/2)Var_π(E) + O(E³).   (5.2)

With π uniform on the 2d neighbours and E_{(±,μ)} = (h²/2)g_μ, g_μ := g^F(D^A_μq, D^A_μq):

  Ē = (h²/(2d)) ‖D^Aq‖²  (the ± parity of §3.3 is already built into Ē),
  Var_π(E) = (h⁴/4) Var_μ(g_μ),  Var_μ(g) := (1/d)Σ_μ g_μ² − ((1/d)Σ_μ g_μ)².

Hence with m_h = ⌈dh^{-2}⌉ and cell weight h^d:
  • frozen β = π  ⟶ (1/2)∫‖D^Aq‖² dc exactly as in 5.2;
  • optimized β* ⟶ the SAME limit, differing by m_h·(1/2)Var_π(E)·h^d·h^{-d} = (d/8) h² ∫Var_μ(g_μ) dc = O(h²) → 0;
  • the row-entropy term contributes KL(β*‖π) summed = (d/8)h²∫Var_μ(g_μ)dc → 0.
ANSWER: BOTH (a) and (b) are available and give the identical limit; the row-entropy term VANISHES (it does not diverge and leaves no finite extra term), at rate exactly h² with the explicit coefficient (d/8)∫Var_μ(g^F(D_μq,D_μq))dc, which is ≥ 0 and vanishes iff the Fisher–Dirichlet density is directionally isotropic. β* concentrates on π at rate O(h²).

NUMERICAL VERIFICATION (d = 3, anisotropic g_μ = (1.3, 2.9, 0.4), uniform π on 6 sources): KL(β*‖π) vs (1/2)Var_π(E): 1.334592e−05 vs 1.336111e−05 (h = 0.1); 8.348336e−07 vs 8.350694e−07; 5.218816e−08 vs 5.219184e−08; 3.261933e−09 vs 3.261990e−09 (h = 0.0125). Ratio 16.0 per halving of h — exactly h⁴ per copy. Also verified Ē − (−log Z) = (1/2)Var_π(E) to four figures at every h. CONFIRMED.

BONUS: TEMPERATURE IS INVISIBLE AT LEADING ORDER. At temperature τ the block is τKL(β‖π) + Σβ_bE_b with envelope −τ log Z_τ = Ē − Var_π(E)/(2τ) + O(E³/τ²). The LEADING term Ē is τ-independent. So the (τ−1)KL(β‖π) mismatch that is fatal for the exact finite identity (boundary-counterexamples.md:39-50; PIFB2.tex:673, :678) is O(h²) in the gradient sector and does not obstruct the Dirichlet limit. This is a genuinely new and favourable fact.

5.4 OBSTRUCTION (H): THE DECISIVE NEGATIVE — THE LAG TURNS THE DIRICHLET TERM INTO A MASS TERM. {DERIVATION + COUNTEREXAMPLE}
The theorem's sources are H_n-measurable: u_{c,c'} = (Ω^A_{c,c'})_# q_i^n(c'). The target's displayed formula "KL( q_i(c) ‖ (Ω^A_{c,c'})_# q_i(c') )" drops the time superscripts and thereby HIDES a mixed-time object. Restore them: the block scores q_i^{n+1}(c) against transported q_i^n(c'). At h = 0 the second argument tends to q_i^n(c), NOT to the first argument. Therefore:

  KL( q_i^{n+1}(c) ‖ (Ω^A)_# q_i^n(c±he_μ) ) = KL( q_i^{n+1}(c) ‖ q_i^n(c) ) + O(h)  = Θ(1), not Θ(h²).

With the m_h = ⌈dh^{-2}⌉ weighting of 5.2 the block then DIVERGES as h^{-2}∫KL(q^{n+1}‖q^n)dc. To keep it finite the increment must be O(h). Set q_i^{n+1}(c) = exp_{q_i^n(c)}(hφ(c)) with φ a bounded C⁰ vertical field (in a chart, θ^{n+1} = θ^n + hφ). Then with v_μ := D^A_μ q_i^n and Δ_± := θ̂^n_c(±h) − θ^{n+1}(c) = h(±v_μ − φ) + O(h²), Proposition 2.2 gives

  Σ_± KL = (h²/2)[ g^F(φ−v_μ, φ−v_μ) + g^F(φ+v_μ, φ+v_μ) ] + O(h³) = h²[ g^F(φ,φ) + g^F(v_μ,v_μ) ] + O(h³).

Summing over μ, applying m_h(1/(2d)) and h^dΣ_c:

  ⟶  (d/2) ∫_C g^F_{q^n}(φ, φ) dc  +  (1/2) ∫_C ‖D^A q^n‖²_{g^F} dc.   (5.3)

READ (5.3) CAREFULLY. The covariant-Fisher Dirichlet integral IS there — but it is an ADDITIVE CONSTANT determined entirely by the FROZEN history section q^n. The only dependence on the free recognition variable is (d/2)∫g^F(φ,φ), a positive-definite Fisher MASS term whose unique minimizer is φ ≡ 0. At the h^{-2} strength required to produce a Dirichlet limit, the exact-ELBO base-neighbour block is an infinitely stiff PIN TO THE PREVIOUS SECTION — a belief-inertia term — not a Dirichlet smoother of the current one. The gradient operator acts on the wrong field.

NUMERICAL VERIFICATION (same d = 1 setup, frozen q^n as in §3.4, free fluctuation φ = (0.7cos2πc + 0.2, 0.45sin2πc − 0.15)):
predicted limit ∫[g^F(φ,φ) + ‖D^Aq^n‖²]dc = 9.579677488 (mass part 0.520011, frozen-Dirichlet part 9.059667).
lattice values h^{-2}·h·Σ_c(block): M = 64: 9.541981604; 256: 9.571704669; 1024: 9.577774925; 4096: 9.579207511; 16384: 9.579560348. Errors −3.77e−2, −7.97e−3, −1.90e−3, −4.70e−4, −1.17e−4: ratio 4.0 per fourfold refinement, i.e. Θ(h). CONFIRMED, including the split into mass + constant.

5.5 THE GENERAL NO-GO (I). {DERIVATION}
PROPOSITION. Let the sources u_{c,c'} be Q-independent (H_n-measurable or otherwise declared) and suppose there are δ > 0 and S ⊆ C of positive Lebesgue measure with lim inf_{h→0} min_{c'∼c} KL(q(c) ‖ u_{c,c'}) ≥ δ for sampled sites c ∈ S. Then h^{d-2}Σ_{edges}KL ≥ h^{d-2}·(d|S|h^{-d})(1+o(1))·δ = d δ |S| h^{-2}(1+o(1)) → +∞, for every d ≥ 1.
CONSEQUENCE. Finiteness of the h^{d-2}-weighted limit FORCES KL(q(c)‖u_{c,c'}) → 0 a.e., and O(h²)-smallness forces q(c) = (the h → 0 limit of the source field) + O(h) in the Fisher metric. The recognition section is therefore pinned to a declared generative field to within O(h). The Dirichlet integral of a genuinely free field is unreachable by ANY Q-independent source, not merely by the lagged one. This also kills the variants I checked: u = transported fixed prior section p_i(c'); u = a fixed reference field; and (see 5.7) any smeared-diagonal edge kernel.

5.6 WHAT WOULD BE NEEDED, AND WHY IT IS BLOCKED.
To make the Dirichlet integral a functional of the free field, the second slot must carry q_i^{n+1}(c') — the generative law must read the current recognition law. That is exactly the same-time obstruction, recorded identically in all three prior runs (boundary-counterexamples.md:68-73: "Replacing q_b^n, s_b^n in the generative kernel by the current optimization variables makes the purported fixed joint depend on its recognition law. The one-step ELBO proof then fails."; fast-slow transported-peer-derivations.md:33-36; effective-action CE-3). PIFB2.tex:678 concedes the same in its own words. Note the target's framing — "the SOURCE being the same agent i at a neighbouring base site c' rather than a peer agent" — does NOT weaken the obstruction: (i,c') is a distinct element of A whose recognition marginal is being optimized simultaneously, so it is structurally identical to a peer. The three named escape routes are (a) lag — taken here, and refuted by 5.4; (b) promote the section to a genuine configuration coordinate and derive its law by contraction — OPEN; (c) empirical-measure/weighted-transported LDP — OPEN with zero verified results (fast-slow approach-registry.json:49-61).

5.7 TWO FURTHER ROUTES I CHECKED AND THAT FAIL. {COUNTEREXAMPLE}
(i) SMEARED-DIAGONAL EDGE KERNEL. Replace the transported-marginal source by a genuine two-endpoint generative block P_e(dx,dy) = ν(dy)k(dx|Ωy) with recognition Q_e = q(c) ⊗ q(c'). Then the ELBO term is E_{y∼q(c')}KL(q(c)‖k(·|Ωy)), which by convexity strictly EXCEEDS KL(q(c)‖Ω_#q(c')). For Gaussians with link covariance C the gap is computed exactly: with C = ΩΣ_{c'}Ω^T (the transported SENDER covariance) the gap is EXACTLY K/2 per source — a configuration-independent constant, but one that after the m_h = h^{-2} weighting diverges as (K/2)h^{-2}; and in any case C = ΩΣ_{c'}Ω^T makes the generative kernel read the sender's current covariance, i.e. Q-dependent, which is forbidden. With a FIXED declared link covariance C_0 the term is (1/2)[log(|C_0|/|Σ_c|) + tr(C_0^{-1}Σ_c) + |Δμ|²_{C_0^{-1}} + tr(C_0^{-1}ΩΣ_{c'}Ω^T) − K]: its mean sector does produce a Dirichlet form but with the DECLARED cometric C_0^{-1}, not the Fisher metric Σ_c^{-1}; and its covariance sector is Θ(1), not Θ(h²), so it diverges. This is an independent rediscovery of PIFB2.tex:678's own statement that "requiring the coordinate update to reduce to a divergence score ... forces the link covariance to be τ times the transported sender covariance and then forces τ = 1."
(ii) TOPOLOGICALLY ORDERED SWEEP. A lexicographic Gauss–Seidel sweep makes each site's BACKWARD neighbours already-updated, so both slots carry q^{n+1} and the h = 0 mismatch disappears. Each sub-step is then an exact ELBO. But (a) the SUM over sites of these per-site ELBOs is not the negative ELBO of any single joint — the source laws change from sub-step to sub-step, so there is no single fixed Π_o and Theory/05b_local_collective_elbo.tex:347-362 (thm:obs-local-global-potential), which does license "sequential exact coordinate minimization", does not apply; 05b:386-387 further warns that "Independently replacing all correlated full conditionals need not define any joint recognition law, so such a parallel prescription is not licensed". (b) A topological order can cover only the backward neighbours, so this route is intrinsically ONE-SIDED and forfeits the exact ±-cancellation of §3.3, degrading the rate from O(h²) to O(h) with the nonzero Amari–Chentsov/acceleration correction of §3.4.

5.8 VERDICT ON ITEM 5. The gradient sector is NOT genuinely ELBO-derived. It requires TWO extra postulates: (P1) an h-dependent integer replication multiplicity m_h = ⌈dh^{-2}⌉ of the base-neighbour label-copy block (admissible, normalized, but declared); and (P2) evaluation at a self-consistent stationary configuration q_i^{n+1} = q_i^n, i.e. the iterated limit lim_{h→0} lim_{n→∞}, whose exchange is unproven and which sits squarely in the two-index non-commuting-limits regime of Theory/07_general_renormalization.tex:862-1027 (prop:rg-noncommuting-limits, with :1064-1077 recording the exchange as OPEN). Absent (P2), (5.3) is what the exact ELBO actually delivers, and it is a mass term plus a constant.

════════════════════════════════════════
§6. BYPRODUCTS
════════════════════════════════════════

6.1 THE BASE COMETRIC IS THE EDGE SECOND MOMENT — discharging one of Theory/05c:1359-1366's five NOT-CLAIMED obligations. By §3.6, M_2^{μν} = Σ_k w_k a_k^μ a_k^ν is the base cometric, M_3 the tensor controlling the h³ term, h^d Lebesgue the base density, w_b = 1 / w_m = 0 the channel weights (belief channel only), the torus the boundary condition, and A fixed the connection decision. All five data 05c:1359-1366 lists as unselected are therefore SELECTED BY THE LATTICE — as declarations, not derivations. A non-isotropic neighbour graph yields an anisotropic continuum Dirichlet form; the cubic lattice's isotropy is a choice.
6.2 d = 2 IS MARGINAL. At d = 2, w_h = h^0 = 1: the RAW exact ELBO block with unit coefficients, counting measure, no replication and no cell weight already converges, to (1/4)∫‖D^Aq‖² dc. Since PIFB2's working framework is exactly C = R² (PIFB2.tex:434), this is the one dimension where the gradient sector needs no weighting postulate at all. The self and observation sectors still diverge as h^{-2} there, so this does not by itself rescue §5.1.
6.3 TEMPERATURE-INDEPENDENCE at leading order (§5.3) — the deployed τ = κ√K_q obstruction does not reach the gradient sector.

════════════════════════════════════════
§7. LEDGER
════════════════════════════════════════
Item 1 — PROVED (Lemma 2.1, Prop 2.2, Cor 2.3; hypotheses (H2) stated; symbolically verified).
Item 2 — PROVED, and it is the strongest result here: h³ coefficient computed exactly as (1/2)g^F(v,w) − (1/6)W(v,v,v) = (1/2)g^F(v,w) + (1/6)T_AC(v,v,v) + (1/2)Γ^{(e)}(v,v,v); argument-order difference is exactly (1/6)T_AC; the term CANCELS EXACTLY AND POINTWISE under ± symmetry (not by integration by parts, which I disproved numerically), and is Θ(h) with a nonzero, non-total-derivative coefficient in the one-sided form. Numerically confirmed to six significant figures.
Item 3 — PROVED (vertical/horizontal split (1.1) computed explicitly; ζ used, not matrix multiplication; exact finite-h gauge covariance (1.4)).
Item 4 — PROVED for C² sections with rate O(h) (one-sided) / o(h)→O(h²) (symmetric); six explicit H¹ failure modes stated. NOT Γ-convergence.
Item 5 — REFUTED in the strong form; the exact limit of what the ELBO delivers is computed in (5.3) and numerically confirmed.
OVERALL: PARTIAL. The analytic claim as literally displayed in the target ("for a smooth section and w_h = h^{d-2}, ... → (1/2)∫‖D^Aq‖²") is TRUE and proved. The ELBO-derivation claim is FALSE as stated and requires two named postulates.

## obstructions

### 1

DECISIVE (item 5): the lag converts the Dirichlet term into a mass term. Because the tied-replica theorem's sources must be H_n-measurable, the base-neighbour block scores q_i^{n+1}(c) against transported q_i^n(c'). Writing q^{n+1} = exp_{q^n}(hφ), the block converges to (d/2)∫g^F_{q^n}(φ,φ)dc + (1/2)∫||D^A q^n||²_{g^F}dc: the Dirichlet integral is an additive CONSTANT of the frozen history section and the free recognition variable enters only through a positive-definite Fisher MASS term with unique minimizer φ=0. Numerically confirmed (predicted 9.579677488, lattice at M=16384 gives 9.579560348, error Θ(h)). The gradient operator acts on the wrong field.

### 2

GENERAL NO-GO: for ANY Q-independent source field u_{c,c'}, if KL(q(c)||u_{c,c'}) stays ≥ δ>0 on a positive-measure set then h^{d-2}Σ_{edges}KL ≥ dδ|S|h^{-2} → +∞, for every d ≥ 1. Finiteness forces the recognition section to be pinned to the declared generative field to O(h) in the Fisher metric. This kills the lagged source, a fixed prior section source, and a fixed reference field alike.

### 3

SCALING NO-GO within the theorem as stated: the exact ELBO is a counting-measure sum in which every block carries coefficient ≤ 1 (β is a probability row), while the gradient sector needs relative weight h^{-2} → ∞ against the observation sector. With λ_h = h^d the gradient sector vanishes; with λ_h = h^{d-2} the observation sector diverges as h^{-2}. Repairable only by the declared h-dependent replication postulate m_h = ⌈d h^{-2}⌉ (admissible per boundary-counterexamples.md:52-59, but NOT derived from anything).

### 4

The Dirichlet result is POINTWISE convergence of the functional at each fixed C² section, NOT Γ-convergence. Convergence of minimizers is not established; equicoercivity, liminf, recovery, interpolation topology and gauge compactness are all missing (the standing ceiling of lattice-continuum-asymptotics.md:33-37).

### 5

The h^{d-2}-weighted limit requires C² sections with image in a compact regular stratum. For H¹ sections six independent failures apply: pointwise sampling undefined for d ≥ 2; no pointwise Taylor; the h³ coefficient needs D^A q ∈ L³ which H¹ does not give; no equicoercivity because g^F degenerates as Σ → 0 or ∞ on the Gaussian fiber; edge KLs may be +∞; and B is a manifold so recovery sequences need a declared chart or embedding.

### 6

The limit functional depends on the CONNECTION, not only on the section (Theory/05c:220-231 gives h = 0 vs a_0²dx² for the same section under two connections), and the gauge invariance established is PASSIVE only (Theory/05c:146-154 gives an active automorphism carrying h = 0 to dx²). The lattice inherits both, exactly.

### 7

Two alternative constructions checked and refuted: (i) a smeared-diagonal two-endpoint edge kernel yields E_y KL(q(c)||k(·|Ωy)) which strictly exceeds the transported KL — the gap is exactly K/2 per source when the link covariance is the transported sender covariance (which is itself Q-dependent, hence forbidden), and with a fixed declared link covariance the mean sector carries the DECLARED cometric rather than g^F and the covariance sector is Θ(1) and diverges; (ii) a topologically ordered Gauss–Seidel sweep makes each sub-step an exact ELBO but the sum over sites is not the ELBO of any single joint, and it is intrinsically one-sided, forfeiting the exact O(h³) cancellation.

### 8

Item 5's repair (P2) requires the iterated limit lim_{h→0} lim_{n→∞}. Exchange of the two indices is unproven and sits in the regime where Theory/07_general_renormalization.tex:862-1027 (prop:rg-noncommuting-limits) proves limits do not commute in general, with :1064-1077 recording exchange as OPEN.


## novelty

SUBSTANTIALLY NEW. Prior art and exactly what it does and does not contain:

ALREADY PRESENT (and I build on, not repeat): (1) Theory/05c_pullback_geometry.tex:556-570, cor:pb-transported-divergence-quadratic — the intrinsic second-order statement D(s(c), ŝ_γ(ε)) = (ε²/2)h^ω(γ̇,γ̇) + O(ε³), status ESTABLISHED. My Prop 2.2/Cor 2.3 upgrade it to a UNIFORM remainder, which is what the lattice sum needs. (2) Theory/05c:509-538, prop:pb-kl-divergence-jets — mixed second jet = Fisher, third-jet difference = Amari–Chentsov; I verified it symbolically rather than citing it alone. (3) Theory/05c:109-122, def:pb-informational-pullbacks — h_s^ω, the target of the limit. (4) Theory/08_infogeometry.tex:238-247 — the exactly-solvable Gaussian fixed-covariance case KL = ½ Fisher quadratic, used as an exact witness. (5) docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/lattice-continuum-asymptotics.md:11-18 and :20-22 — the h² expansion in a parameter chart and h^{d-2} by edge counting; :33-34 concedes these are "consistency expansions on smooth sequences, not Gamma-convergence proofs". (6) boundary-counterexamples.md:52-59 (integer replication licence), :61-66 (cell-volume prohibition), :68-73 (same-time obstruction). (7) Theory/05b_local_collective_elbo.tex:347-388 (sequential coordinate updates licensed for a FIXED joint only).

EXPLICITLY ABSENT FROM Theory/ AND ALL THREE PRIOR RUNS: there is NO spatial lattice anywhere in Theory/ (my own grep confirms the only "lattice" hits are Banach lattice at 07b:1054,1104 and Boolean-lattice Möbius projectors at 07b:1191), no Riemann-sum or convergence statement, no Dirichlet energy in any free energy, and no base-derivative term in any action. Theory/05c:1359-1366 (status NOT-CLAIMED) explicitly refuses to build the scalar gauged sigma energy for want of "a base cometric, a base density, channel weights, boundary conditions, and a decision about whether the connection is fixed or dynamical."

NEW HERE: (a) the exact h³ coefficient (1/2)g^F(v,w) − (1/6)W(v,v,v) = (1/2)g^F(v,w) + (1/6)T_AC + (1/2)Γ^{(e)}, which DISCHARGES the open warning at Theory/05c:578-587 ("the coefficient of ε³ ... is not determined by c^ω_{s,D} alone. It also contains the covariant acceleration ... and the connection coefficient selected by the one-sided divergence jet") — that locus flags the ambiguity but never computes it; (b) the exact pointwise ±-parity cancellation theorem, and the numerical disproof that the acceleration piece is a total derivative (∫(1/2)g^F(v,w) = +4.392910 ≠ 0 while ∫(1/4)d/dc[g^F(v,v)] = −5.6e−11); (c) the convergence theorem with rates Θ(h) one-sided / Θ(h²) symmetric, replacing "consistency expansion"; (d) the six-item H¹ failure list; (e) the ENTIRE item-5 analysis — the β ≤ 1 scaling no-go, the m_h = ⌈dh^{-2}⌉ replication repair, the exact row-entropy computation KL(β*||π) = (h⁴/8)Var_μ(g_μ) with its vanishing, the leading-order τ-independence, and above all the mass-term theorem (5.3) which is the decisive negative and appears nowhere; (f) the general Q-independent-source no-go valid for all d ≥ 1; (g) the base cometric as the edge second moment and the h³ term as the edge third moment, which selects four of 05c:1359-1366's five missing data; (h) the observation that d = 2 (PIFB2.tex:434's working framework) is the marginal dimension at which the raw counting-measure ELBO block already converges with no weighting postulate; (i) the exact K/2 gap for the smeared-diagonal edge kernel, an independent rediscovery of PIFB2.tex:678's link-covariance/τ=1 concession from the opposite direction.

The mass-term result (5.3) is a genuinely new obstruction: it is NOT the same statement as the known same-time obstruction (boundary-counterexamples.md:68-73), which says only that a same-time source breaks normalization. (5.3) says what the LAGGED (legal) construction actually converges to, and shows it is structurally the wrong object — a Fisher mass term pinning the update to the history, plus a constant — rather than merely an approximation to the right one.

## next_obligations

### 1

Attack the exact-image-invariance criterion, not 'eps_h → 0'. If the gradient sector is to be recovered as an EXACT retained coordinate rather than a postulate, target Theory/07b_agent_network_rg.tex:1487-1496: closure holds iff T_ℓ(Ran R_ℓ) ⊆ Ran R_{ℓ+1}. Note the prerequisite the prior run never states: the Hoeffding–Möbius coordinates of 07b:1193-1214 require a PRODUCT reference measure ν, and 07b:1160-1180 shows a deterministic cloning channel destroys product equivalence. Under lattice refinement |V_h| ~ h^{-d} and the coordinate-to-sup-norm cost 3^{|V|}−1 is SHARP (07b:1228-1239), so any residual argument that must go coordinate-wards is exponentially hard in h^{-d}.

### 2

Decide the status of the replication postulate m_h = ⌈d h^{-2}⌉. Either (i) derive a growing base-neighbour copy count from an independently specified microscopic family — e.g. show that a microscopic law with h^{-2} independent relational channels per site arises by contraction from a declared fine model — or (ii) record it permanently as a declared generative postulate in the claim ledger, on the same footing as PIFB2.tex:678's 'The tie itself is a declared postulate rather than a derived identity'.

### 3

Test whether the mass term of (5.3) is the correct physical object rather than a defect. (5.3) says the exact-ELBO base-neighbour sector at Dirichlet strength is (d/2)∫g^F(φ,φ) + const, i.e. a Fisher-metric penalty on the RESCALED BELIEF INCREMENT φ = (q^{n+1}−q^n)/h. That is exactly a belief-inertia / natural-gradient-step-size term. Determine whether the deployed MAgent dynamics are in fact governed by this rather than by a spatial Dirichlet term, which is an empirically decidable question about the reference implementation.

### 4

Prove or refute the exchange lim_{h→0} lim_{n→∞} = lim_{n→∞} lim_{h→0} for the belief update, which is the only route from (5.3) back to the target's claim. This must contend with Theory/07_general_renormalization.tex:862-1027 (prop:rg-noncommuting-limits) and the fast-slow run's open obligation 'Prove the fast/slow singular-perturbation hypotheses or retain the coupled dynamics' — specifically a uniformly attracting, normally hyperbolic fast branch (fast-slow-effective-action.md:26-36), uniformly in h.

### 5

Upgrade Theorem 4.1 from pointwise to Γ-convergence. Required and currently missing: an interpolation topology on section space (B is a manifold, so declare a chart or an isometric embedding), equicoercivity modulo gauge with uniform ellipticity λI ⪯ g^F ⪯ ΛI on a declared compact stratum of Sym_{++} (the Gaussian fiber fails this as Σ → 0 or ∞), liminf and recovery sequences, and compactness of the gauge sector. Only then does convergence of MINIMIZERS follow.

### 6

Extend the h³ analysis to non-centrally-symmetric neighbour graphs. §3.6 shows the h³ term contracts with the edge third moment M_3^{μνρ}; for graphs where M_3 ≠ 0 (e.g. a honeycomb site, or any directed/topologically ordered source mask) the Amari–Chentsov and acceleration corrections survive at Θ(h). Any implementation using a directed source mask (PIFB2.tex:678's 'topologically ordered source mask') is in this regime and should carry the correction explicitly.

### 7

Redo the whole calculation for the MODEL channel s_i with OmegaTilde. PIFB2.tex:459 records that in the reference implementation the model fiber carries its own GL(K_m) bundle and frame field, so OmegaTilde is an independent transport and even the structure-group identification is absent. The two-channel weighted product h^prod = w_b h_b + w_m h_m (Theory/05c:247-256) is a HYPOTHESIS, and the cross-scale comparison conditions (X1) f_#μ = μ̄ and (X2) w̄∘f ≤ w (05c:263-269) must be declared before any joint gradient sector is written.

### 8

Do not import the curvature/Wilson sector by analogy. lattice-continuum-asymptotics.md:25-32 derives h^{d-4} for COMPACT groups in unitary representations only; CE-4 of two separate runs shows the raw Frobenius curvature is not GL-conjugation invariant (factor t^{-2}) and full GL(K,R) has no normalized Haar measure. The gradient sector proved here uses only that ρ̂(g) is a g^F-isometry, which holds for GL; the curvature sector does not inherit that.


## evidence_kind

Derivation from first principles (Lemma 2.1 / Prop 2.2 / Cor 2.3 / Thm 4.1, with all differentiation-under-the-integral and Bartlett-identity hypotheses stated), plus one applicable-theorem invocation with hypotheses verified (prop:pb-statistical-tensor-descent, Theory/05c:59-63), plus three counterexample-grade negative results (the scaling no-go, the mass-term computation (5.3), the general Q-independent-source no-go), all cross-checked by two independent machine verifications: exact symbolic computation in SymPy (Fisher/Amari-Chentsov/e-connection/W tensors for N(mu,sigma^2) in a non-natural chart; identity W = -(T_AC + 3Gamma^(e)); forward and reverse third-order KL coefficients; the +/-h cancellation with free symbols for the second and third jets) and a high-resolution lattice computation on a 1-D gauged circle with exact abelian transport (Dirichlet limit 4.529833403250 recovered; one-sided error Theta(h) with coefficient -3.21927 vs predicted -3.219270, six-figure agreement; symmetric error Theta(h^2); mass-term limit 9.579677488 recovered at Theta(h); row entropy KL(beta*||pi) = (1/2)Var_pi(E) confirmed to four figures with exact h^4 scaling). No claim rests on numerical agreement alone: every numerical check confirms an independently derived identity, and one numerical check (section 3.4) refuted an intermediate argument of mine and forced its correction.
