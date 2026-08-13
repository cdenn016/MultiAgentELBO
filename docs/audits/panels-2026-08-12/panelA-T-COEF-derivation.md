# panelA-T-COEF-derivation

*Recovered verbatim from workflow journal.jsonl, 2026-08-13. Agent a3407b57.*

## target

T-COEF: which of PIFB2/MAgent's deployed coefficients (τ = κ√K, λ_h, state-dependent α_i(c), and the smooth presence weight χ_i(c)) can be produced by the exact ELBO of a normalized generative model, and which are obstructed — with the exact extra terms each reachable coefficient forces into the action.

## status

PARTIAL

## theorem_statement

Standing setting (H1)-(H4): finite agent-site set A; standard-Borel fibers; a normalized generative law P fixed by the history H_n (lagged sources, no reading of Q^{n+1}), as in docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/typed-construction.md:61-88; a tied-replica recognition law Q that is a finite product of blocks, each block's law being exactly one of the tied objects q_a, s_a, β_a, γ_a (or the correlated private ζ_a), as in typed-construction.md:100-111; Q ≪ P(·|o) with finite KL; a declared σ-finite fiber reference ν, H_ν(q) := −∫ q log(dq/dν) finite. Write F := KL(Q‖P(·|o)) for the exact negative ELBO and S_PIFB for PIFB2's boxed scalar (PIFB2.tex:681-693) with belief temperature τ, model temperature τ_s, private self-weight α on KL(q‖p) and model weight λ_s on KL(s‖r).

LEMMA 0 (UNIT-ENTROPY PRINCIPLE). For any σ-finite μ dominating P and Q, F = −H_μ(Q) + ⟨Q, −log(dP/dμ)⟩. The second summand is affine in the joint law Q. Hence the only non-affine dependence of an exact negative ELBO on its recognition law is minus the Shannon entropy of that law, with coefficient exactly one. For a product Q = ⊗_t Q_t, H_μ(Q) = Σ_t H(Q_t), so a tied law entering N blocks enters F with entropy coefficient exactly −N, N ∈ ℤ_{≥0}. Replacing μ by fμ changes each H by an affine functional, so "the entropy coefficient" is reference-independent.

THEOREM A (TEMPERATURE QUANTIZATION). Let |J_a^q| ≥ 2, let exactly N_β ∈ ℤ_{≥0} factors of Q be categorical with law β on J_a^q, let all other factors' laws be β-free, and let P be ANY probability measure on the product latent space with P ≫ Q(β) and KL(Q(β)‖P) < ∞ on an open U ⊆ int Δ(J_a^q). If there exist c > 0, τ ∈ ℝ, a vector (E_b), a prior π̃ and a constant κ with
    KL(Q(β)‖P) = c[ τ Σ_b β_b log(β_b/π̃_b) + Σ_b β_b E_b ] + κ  for all β ∈ U,
then cτ = N_β. In particular the belief temperature satisfies τ = N_β/c and the model temperature τ_s = N_γ/c with N_β, N_γ ∈ ℤ_{≥0}, c the single global scale relating F to S_PIFB.

COROLLARY A1 (RATIONALITY OF RATIOS). τ/τ_s = N_β/N_γ ∈ ℚ, unconditionally in the above class. Under the additional hypothesis (H5) that P factorizes across the latent blocks (which the closed theorem's witness does, typed-construction.md:71-78) the same argument on the fiber blocks gives N_q = c(α+1) and N_s = c(λ_s+1), hence every pairwise ratio among {τ, τ_s, α+1, λ_s+1} is a ratio of nonnegative integers.

COROLLARY A2 (DEPLOYED TWO-CHANNEL OBSTRUCTION). PIFB2 runs τ_β = κ√K_q on the belief fiber and τ_γ = κ√K_m on the model fiber (PIFB2.tex:673). Then τ_β/τ_γ = √(K_q/K_m). Whenever K_q/K_m is not the square of a rational (e.g. K_q/K_m ∈ {2,3,5,6,7,8,10,...}), NO normalized generative model in the class realizes the deployed pair — independently of κ, of the global scale c, of tempering, of replication, and of latent-variable integration. OBSTRUCTED.

COROLLARY A3 (LEARNABLE κ IS ALMOST SURELY OBSTRUCTED). At PIFB2's canonical α = 1 (PIFB2.tex:694), Corollary A1 forces τ = 2N_β/N_q ∈ ℚ, hence κ ∈ (1/√K_q)·ℚ, a Lebesgue-null set. A continuously learnable κ (PIFB2.tex:673; MAgent gauge_agent/softmax_utils.py:12, numerical_monitor.py:14) is therefore almost surely not the coefficient of any exact ELBO in this class.

COROLLARY A4 (SMOOTH PRESENCE WEIGHT). The explicit χ_i(c) ∈ [0,1] on the self-KL terms T1 and T2 (PIFB2.tex:685-686) is a private coefficient and is quantized to ℤ_{≥0} ∩ [0,1] = {0,1}. Smooth bump supports (PIFB2.tex:711) are obstructed on those terms. The χ on the alignment blocks T3, T4 is free (it is absorbed into the prior π̃, PIFB2.tex:694, an affine redefinition), and the χ on the observation term T5 is free (it is a likelihood exponent) under the side condition of Theorem D.

THEOREM B (REPLICATION IS EXACT AND REACHES EXACTLY ℚ_{>0}). Two independent integer mechanisms exist, both exactly normalized, both with zero extra terms:
 (B1) REDUNDANT LABELS. P(dj_1..dj_{n'}, dx) = (Π_t π̃_{j_t}) u_{j_1}(dx), Q(dj_1..dj_{n'}, dx) = (Π_t β_{j_t}) q(dx). Then KL(Q‖P) = n' KL(β‖π̃) + Σ_b β_b KL(q‖u_b), with optimum β*_b ∝ π̃_b exp(−E_b/n'). This reaches τ ∈ {1,2,3,...}.
 (B2) COPY MULTIPLICITY. P(dj, dx_1..dx_n) = π̃_j Π_u u_j(dx_u), Q = β_j Π_u q(dx_u). Then KL(Q‖P) = KL(β‖π̃) + n Σ_b β_b KL(q‖u_b), i.e. effective τ = 1/n ∈ {1,1/2,1/3,...}.
 Combined, KL(Q‖P) = n'KL(β‖π̃) + n Σ_b β_b E_b = n · [PIFB2 row at τ = n'/n], so τ ∈ ℚ_{>0} exactly, with global scale c = n. Analogously α = m_q ∈ ℤ_{≥0} and λ_s = m_s ∈ ℤ_{≥0} by replicating the private state/model blocks, with the mutual-information correction I_{ζ_a}(K_a;M_a) unchanged.

THEOREM C (NO EXACT TEMPERATURE RESCALING; TEMPERING AND ITS EXACT RESIDUE).
 (C1) NO-RESCALING LEMMA. Let ν be σ-finite, u, w probability densities w.r.t. ν, τ > 0, C ∈ ℝ. If KL(q‖w) = (1/τ)KL(q‖u) + C for every q in a convex set 𝒬 of ν-densities containing two distinct elements with finite entropy and finite KLs, then τ = 1, w = u ν-a.e., C = 0. No choice of source law whatsoever reproduces a pure temperature rescaling of a peer energy.
 (C2) EXACT TEMPERED ROW. With u_b^{(τ)} := u_b^{1/τ}/Z_b, Z_b := ∫ u_b^{1/τ} dν (Gaussian case: u_b^{(τ)} = N(m_b, τ S_b)), the model P(dj,dx) = π̃_j u_j^{(τ)}(dx) is exactly normalized and
     KL(q‖u_b^{(τ)}) = (1/τ) KL(q‖u_b) + (1/τ − 1) H_ν(q) + log Z_b,
     τ · KL(Q‖P) = [ τ KL(β‖π̂) + Σ_b β_b E_b ] + (1−τ) H_ν(q) − τ log W,
   where π̂_b := (π̃_b/Z_b)/W, W := Σ_k π̃_k/Z_k. For Gaussian sources on ℝ^K,
     log Z_b = (K/2)[(1−1/τ)log 2π + log τ] + ((τ−1)/(2τ)) log|S_b|,
   so β*_b ∝ π̃_b |S_b|^{−(τ−1)/(2τ)} exp(−E_b/τ). The per-source term is β-DEPENDENT: it is NOT absorbable into a constant c_h; it is absorbable only into the attention prior. It is j-independent (hence harmless) exactly when |S_b| is b-independent, which for PIFB2's Regime-I coboundary Ω_{ab} = e^{φ_a}e^{−φ_b} (PIFB2.tex:311-316) requires |det Ω_{ab}|² |Σ_b| to be b-independent, e.g. common source covariance and unimodular transports (tr φ_a = tr φ_b, i.e. φ ∈ 𝔰𝔩(K)) — not generic for G = GL(K_q,ℝ) (PIFB2.tex:434). The entropy term (1−τ)H_ν(q) is exactly the entropy-coefficient defect created by the illegal multiplication of an exact ELBO block by τ (Lemma 0), and PIFB2's action contains no such term.

THEOREM D (LIKELIHOOD TEMPERING GIVES A FREE REAL GLOBAL SCALE). Replace ℓ_a(o|k,m) by ℓ_a^θ/c_θ(k,m), c_θ(k,m) := ∫ ℓ_a(o|k,m)^θ ν_a(do), θ > 0. The model is exactly normalized and the exact ELBO observation term is −θ E_ζ log ℓ_a + E_ζ log c_θ(K_a,M_a). If ℓ_a is a location family in the observation with (k,m)-independent noise — in particular the Gaussian observation model of PIFB2's working framework (PIFB2.tex:434) — then c_θ is constant and the extra term is a pure additive constant. Consequently each individual coefficient of S_PIFB is a free positive real; only the RATIOS of Corollary A1 are quantized. This is the exact generalized-Bayes / Bissiri-Holmes-Walker normalization check: BHW's Gibbs posterior is normalized in the parameter, not in the data, and using it as a generative likelihood requires the extra factor c_θ, which is a constant only under the location-family hypothesis.

THEOREM E (STATE-DEPENDENT PRECISION DICHOTOMY).
 (E1) HEAT-EQUATION TEST. Under (H5) with the isotropic Gaussian sub-family q = N(μ, vI_K), an exact-ELBO q-part F satisfies ∂_v F − ½Δ_μ F = −N_q K/(2v) with N_q ∈ ℤ_{≥0}, because the affine part ∫ q ψ dν is heat-null. Applying this to PIFB2's envelope-reduced precision sector G(q) := c_0 log(b_0 + D_KL(q‖p)) (the exact value of min_α[α D + R(α)] with R from PIFB2.tex:755) gives an implied block count
     N(v,m) = −(2v/K)[∂_v G − ½Δ_μ G],  m := |μ|²,
   which is a nonconstant function of (v,m) (e.g. K=2, c_0=b_0=1, p=N(0,I): N = 1.000 at (v,m)=(1,0), 0.4444 at (1,1), 0.7652 at (2,0), −0.0245 at (2,3)). Hence G is NOT −N_q H(q) + affine for ANY constant N_q, so it is not the recognition-dependent part of any fixed normalized joint with tied q-blocks. OBSTRUCTED.
 (E2) DICHOTOMY. A constant coefficient α on KL(q‖p) is reachable iff α ∈ ℤ_{≥0} (relative to the global scale c). A genuinely state-dependent coefficient α(q) is reachable ONLY as a PROFILED exact ELBO over an extra latent Λ, and the unreduced exact ELBO then carries the term KL(ξ‖ρ) ≥ 0 which S_PIFB does not contain.
 (E3) EXACT LATENT-COUNT CONSTRUCTION. On the marked space ⊔_N 𝖪^N with P(N, dk_{1:N}) = ρ(N) Π p(dk_t) and Q(N, dk_{1:N}) = ξ(N) Π q(dk_t), KL(Q‖P) = KL(ξ‖ρ) + E_ξ[N]·KL(q‖p) EXACTLY. Profiling ξ gives F_red(D) = −log Σ_{n≥0} ρ_n e^{−nD−h_n}, whose derivative α(D) = F_red′(D) = E[n | D] is the reachable class of state-dependent precisions: nonnegative, nonincreasing in D, and the mean of a tilted lattice law.
 (E4) THE GAMMA IDENTITY AND ITS OBSTRUCTION. min_{α>0}[α D + b_0 α − c_0 log α] = c_0 log(b_0 + D) + c_0 − c_0 log c_0, while −log E_{Gamma(shape c_0, rate b_0)}[e^{−ΛD}] = c_0 log(b_0 + D) − c_0 log b_0. The two agree identically up to the D-free constant c_0(1 + log(b_0/c_0)). So PIFB2's log-barrier envelope is, as a functional of the belief, exactly the fully-optimized (Gibbs) variational free energy of a Gamma(c_0, b_0) latent precision. But the required conditional model must contribute Λ·KL(q‖p) at fixed Λ, which by Lemma 0 forces Λ ∈ ℤ_{≥0}; and the representing measure of (b_0+D)^{−c_0} is the Gamma density on (0,∞), which by uniqueness of Laplace transforms is not lattice-supported. Hence the identity is a functional coincidence, not an exact-ELBO realization. Moreover PIFB2's α_i*(c) is a MAP (PIFB2.tex:771), i.e. a Dirac recognition law on a continuous latent, whose KL against the Gamma prior is +∞ — a Dirac ξ has no exact ELBO at all.

THEOREM F (LATENT TEMPERATURE DOES NOT UNLOCK REAL τ). With a latent redundancy count N ~ ρ on ℤ_{≥0} and conditional row n·KL(β‖π̃) + Σβ_b E_b, profiling ξ gives −log Σ_n ρ_n e^{−n u} + Σβ_b E_b with u := KL(β‖π̃). This equals τ u for all u ≥ 0 iff the probability generating function satisfies G(z) = z^τ, i.e. iff ρ = δ_τ with τ ∈ ℤ_{≥0}. A nondegenerate ρ instead yields a state-dependent effective temperature τ_eff(β) = E[N | u] that is nonincreasing in u. Real constant τ remains unreachable; a Dirac recognition on a continuous temperature latent has KL = +∞ against a nonatomic prior, and against an atomic prior with mass ρ_0 it contributes the constant −log ρ_0 while leaving the Theorem C residues intact.

## hypotheses

### 1

(H1) Finite agent-site set A; standard-Borel fibers K_a, M_a, O_a; normalized private laws p_a, r_a; normalized observation kernel L_a with jointly measurable density ell_a; one admitted observation o_a with positive finite evidence. (typed-construction.md:9-33)

### 2

(H2) The generative law P_h^n is fixed conditional on the history H_n: sources u_ab = (Omega_ab)_# q_b^n and v_ab = (OmegaTilde_ab)_# s_b^n are LAGGED and do not read Q^{n+1}. All results here are one-step lagged statements; the same-time reciprocal case remains open in all three prior runs.

### 3

(H3) TIED-REPLICA RECOGNITION: Q is a finite product of blocks whose laws are exactly q_a, s_a, beta_a, gamma_a (or the correlated private zeta_a). Warped ties (a block whose law is a nonlinear function of q, e.g. q^theta/Z) leave the family; the theorems do not apply to them. Mixture-tying with mutually singular components stays inside the theorems' conclusion because it still contributes integer entropy multiples.

### 4

(H4) Q << P(.|o) with finite KL on the relevant open set; a common sigma-finite reference mu; all displayed differential entropies H_nu finite. Reference nu declared; conclusions are nu-independent because a change of reference shifts H by an affine functional.

### 5

(H5) For the fiber-block corollaries (alpha, lambda_s, chi on T1/T2): P factorizes across the latent blocks, so that -E_Q log P is AFFINE in each tied law. This is exactly the closed theorem's witness (typed-construction.md:71-78). Without (H5), -E_Q log P is only a polynomial of degree <= block multiplicity, and the fiber-block conclusions require instead a recognition family containing a nondegenerate mixture segment.

### 6

(H6) For the heat-equation test (Theorem E1): the recognition family contains the isotropic Gaussian sub-family {N(mu, v I_K)}; psi = -log(dP/dmu) is such that A(mu,v) = int N(mu,vI) psi is finite and twice differentiable with differentiation under the integral sign valid (Gaussian-integrable dominating envelope). PIFB2's deployed fibers are Gaussian (PIFB2.tex:160-176, :434), so the sub-family is available.

### 7

(H7) For Theorem A only: |J_a^q| >= 2 and the recognition row ranges over an open subset of the simplex interior. PIFB2 optimizes beta over the row simplex (PIFB2.tex:694, :717-733), so this holds. The all-zero-row and empty-source edge cases are excluded as in boundary-counterexamples.md:74-79.

### 8

(H8) For Theorem C: a declared sigma-finite fiber reference nu against which the powers u_b^{1/tau} are integrable, i.e. Z_b < infinity. For Gaussian sources this holds for every tau > 0. For heavy-tailed sources with tau > 1 it can fail.

### 9

(H9) For Theorem D: c_theta(k,m) = int ell_a(o|k,m)^theta nu_a(do) is finite and independent of (k,m). Verified symbolically for the Gaussian location family with (k,m)-independent noise covariance. It FAILS whenever the observation noise depends on the latent state or model parameter (e.g. heteroscedastic or precision-learning likelihoods).

### 10

(H10) Exact-identity claims require the SPD floor eps = 0 in the Gaussian KL (PIFB2.tex:187, KL_REGULARISER_EPS default 1e-4); at the default floor every identity below holds only up to O(eps).

### 11

(H11) The identification of an exact ELBO with c * S_PIFB carries a single global positive scale c. Coefficients are pinned only relative to c; this is why individual coefficients are free reals (Theorem D) while their ratios are quantized (Corollary A1).


## derivation

## 0. Why the entropy is the whole story

Write F := KL(Q‖P(·|o)) and pick any σ-finite μ dominating both. Then

    F = ∫ Q log(dQ/dμ) − ∫ Q log(dP/dμ) = −H_μ(Q) + ⟨Q, −log(dP/dμ)⟩.

The second summand is a linear functional of the joint law Q. So **every exact negative ELBO is (minus) one Shannon entropy plus one affine functional, and the entropy carries coefficient exactly one.** For a product Q = ⊗_t Q_t, H_μ(Q) = Σ_t H(Q_t). A law that is *tied* across N blocks therefore appears with entropy coefficient exactly −N, N ∈ ℤ_{≥0}. This is LEMMA 0; every obstruction below is a corollary of it, and every construction below is an exercise in arranging block counts.

Reference-independence: replacing μ by fμ sends H_μ(q) ↦ H_μ(q) + ∫ q log f, an affine change. So "the coefficient of the entropy" is well defined modulo the affine part, which is what the theorems assert.

Now expand PIFB2's target. Using KL(q‖w) = −H_ν(q) − ∫ q log w:

    α KL(q‖p)              contributes −α H_ν(q)
    Σ_b β_b KL(q‖u_b)      contributes −(Σ_b β_b) H_ν(q) = −H_ν(q)      [row simplex, PIFB2.tex:694]
    τ KL(β‖π̃)              contributes −τ H(β)
    −E_q log ℓ             is affine in q
    λ_s KL(s‖r) + Σ_b γ_b KL(s‖v_b)  contributes −(λ_s+1) H_ν(s)
    τ_s KL(γ‖π̃^s)          contributes −τ_s H(γ)

So matching F = c·S_PIFB + const forces, blockwise,

    **N_q = c(α+1),  N_s = c(λ_s+1),  N_β = c τ,  N_γ = c τ_s,   all N ∈ ℤ_{≥0}.**   (★)

Everything in this report is (★) plus the exact bookkeeping of what happens when you try to break it.

---

## 1. THEOREM A: proof of the quantization of τ

Hypotheses (H7). Q(β) has exactly N_β categorical factors with law β; other factors are β-free; P is arbitrary with P ≫ Q(β) and finite KL on an open U ⊆ int Δ.

By Lemma 0, F(β) = −N_β H(β) + R(β) where R(β) := −E_{Q(β)}[log dP/dμ] − (β-free entropies). Because Q(β) = (⊗_{t=1}^{N_β} β) ⊗ (β-free blocks),

    E_{Q(β)}[log dP/dμ] = Σ_{j_1…j_{N_β}} β_{j_1}⋯β_{j_{N_β}} · c_{j_1…j_{N_β}},   c := ∫ log(dP/dμ) dQ_other,

a homogeneous polynomial of degree N_β in β. So R is a polynomial of degree ≤ N_β.

Suppose F(β) = c[τ Σ_b β_b log(β_b/π̃_b) + Σ_b β_b E_b] + κ = −cτ H(β) + A(β), A affine. Subtracting,

    (N_β − cτ) H(β) = R(β) − A(β) − κ =: Π(β),  a polynomial of degree ≤ Deg := max(N_β, 1).

Restrict to the segment β(t) = (t, θ−t, β_3^0, …) ⊆ U, θ := β_1^0 + β_2^0 fixed, t in an open interval. Then

    −H(β(t)) = t log t + (θ−t) log(θ−t) + const,
    d^k/dt^k[−H(β(t))] = (k−2)! [ (−1)^k t^{−(k−1)} + (θ−t)^{−(k−1)} ]  for k ≥ 2.

For every **even** k ≥ 4 this equals (k−2)![t^{−(k−1)} + (θ−t)^{−(k−1)}] > 0 on the whole interval. (Verified symbolically: k=4 gives 2/t³ + 2/(θ−t)³; k=6 gives 24/t⁵ + 24/(θ−t)⁵; k=8 gives 720/t⁷ + 720/(θ−t)⁷.) Choose an even k > Deg. The k-th derivative of Π vanishes identically, so (N_β − cτ)·(strictly positive) = 0, hence **cτ = N_β**. ∎

The same argument applied to γ gives cτ_s = N_γ. Note it used *nothing* about P beyond normalization — no product structure, no tempering restriction, no Gaussianity. This is why Corollary A1's ratio statement τ/τ_s = N_β/N_γ ∈ ℚ is unconditional in the class.

For the fiber blocks I need (H5). Under (H5), P is a product over blocks, so −E_Q log P is affine in each tied law separately even at multiplicity > 1, and F(q) = −N_q H_ν(q) + affine(q). On the isotropic Gaussian sub-family q = N(μ, vI_K), with the heat identity ∂_v N(x;μ,vI) = ½Δ_μ N(x;μ,vI), any affine functional A(μ,v) = ∫ q ψ satisfies ∂_v A − ½Δ_μ A = 0, while −N_q H_ν(q) = −(N_q K/2) log v + const gives −N_q K/(2v). Hence

    **∂_v F − ½ Δ_μ F = −N_q K/(2v),  N_q ∈ ℤ_{≥0}.**   (HEAT TEST)

Sanity checks (symbolic): for F = α·KL(N(μ,vI)‖N(0,I)) the test returns exactly N = α; for the affine functional A = ∫ q |x|⁴ = K(K+2)v² + 2(K+2)v|μ|² + |μ|⁴ it returns 0. Both as required.

### Corollary A2 (the sharpest hit on the deployed configuration)

PIFB2.tex:673 states verbatim that "on the belief fiber τ = κ_β = κ√K_q, and on the model fiber κ_γ = κ√K_m, the two coinciding only when K_m = K_q". Both channels share the single global scale c, so by Theorem A applied twice,

    τ_β/τ_γ = N_β/N_γ ∈ ℚ,   but the deployed ratio is √(K_q/K_m).

√(K_q/K_m) ∈ ℚ iff K_q/K_m is the square of a rational. For K_q/K_m ∈ {2,3,5,6,7,8,10,11,12,…} it is not. **In those configurations no normalized generative model in the class produces the deployed temperature pair** — for any κ, any c, any tempering, any replication, any latent. κ cancels from the ratio, which is why this obstruction cannot be dodged by tuning. It is defeated only by tying the fibers (K_m = K_q), which is exactly what MAgent's `tie_model_fibers` path does (gauge_agent/agents.py:911, :983).

### Corollary A3 (learnable κ)

At PIFB2's canonical α = 1 (PIFB2.tex:694), (★) gives N_q = 2c so c = N_q/2, and cτ = N_β, hence τ = 2N_β/N_q ∈ ℚ. With τ = κ√K_q this forces κ ∈ (1/√K_q)·ℚ, a Lebesgue-null set. MAgent learns κ as a continuous scalar (gauge_agent/softmax_utils.py:12 "tau_eff = kappa * sqrt(K)"; numerical_monitor.py:14 "tau_effective(kappa,K) = max(kappa,1e-6)*sqrt(K)"). **Almost every value the optimizer can produce is off the admissible set.**

### Corollary A4 (the smooth presence function)

χ_i(c) ∈ [0,1] multiplies KL(q_i‖p_i) and λ_h KL(s_i‖r_i) explicitly (PIFB2.tex:685-686) and is a *smooth* bump, not an indicator (PIFB2.tex:711). At one agent-site a, χ_a is a private coefficient, so by (★) it is quantized to ℤ_{≥0} ∩ [0,1] = {0,1}. Smooth χ on T1/T2 is obstructed. By contrast:
 • χ_ij on T3/T4 is *absorbed into the prior* π̃_ij (PIFB2.tex:694) — an affine redefinition, entropy-free, exactly reachable;
 • χ_i on T5 is a likelihood exponent, exactly reachable by Theorem D under (H9).
This is a term-by-term verdict, and it independently corroborates the manuscript's own choice of hard χ_i ∈ {0,1} in the rigorous-RG appendix (PIFB2.tex:3755) — that appendix is sitting in exactly the quantized case.

---

## 2. THEOREM B: replication — exact, and exactly ℚ_{>0}

The task's route (a) is correct but reaches only τ ≤ 1. There is a *second*, dual mechanism it does not anticipate, which reaches τ ≥ 1. Both are exactly normalized; both were verified by brute-force summation over the full product space.

**(B2) Copy multiplicity (the task's route).** Give the receiver n i.i.d. relational copies under a single shared label:

    P(dj, dx_1..dx_n) = π̃_j Π_{u=1}^n u_j(dx_u),   Q(dj, dx_1..dx_n) = β_j Π_{u=1}^n q(dx_u).

    KL(Q‖P) = Σ_j β_j[ log(β_j/π̃_j) + n KL(q‖u_j) ] = KL(β‖π̃) + n Σ_b β_b E_b.

Numerically verified for n = 1,2,3 against brute force (residual ≤ 3.3e-16). The energy is multiplied by n; the row entropy stays at coefficient 1. Reading this as n × [PIFB2 row at τ] gives **τ = 1/n ∈ {1, 1/2, 1/3, …}**. Confirmed: only reciprocal integers, and never τ > 1.

**(B1) Redundant labels (new).** Give the receiver n′ i.i.d. source labels of which only the first is read by the copy:

    P(dj_1..dj_{n′}, dx) = (Π_{t=1}^{n′} π̃_{j_t}) · u_{j_1}(dx),   Q(dj_1..dj_{n′}, dx) = (Π_t β_{j_t}) q(dx).

P is normalized (a probability on labels times a Markov kernel to X). Expanding,

    KL(Q‖P) = Σ_{j_1..j_{n′}} Π_t β_{j_t} [ Σ_t log(β_{j_t}/π̃_{j_t}) + KL(q‖u_{j_1}) ]
            = **n′ KL(β‖π̃) + Σ_b β_b E_b.**

Numerically verified for n′ = 1,2,3,4 against brute force (residual ≤ 2.0e-15). Row entropy multiplied by n′; energy untouched. Minimizing on the simplex gives β*_b ∝ π̃_b exp(−E_b/n′), verified numerically against PIFB2's softmax (PIFB2.tex:695-708) to 2e-9 for n′ = 2,3. **This reaches τ ∈ {1,2,3,…} with unit row-energy coefficient and NO extra term of any kind.**

**Combined.** n′ redundant labels and n copies of the read source give n′KL(β‖π̃) + n Σβ_b E_b = n·[PIFB2 row at τ = n′/n]. With the global scale carried consistently (m_o repeated observations, m_q, m_s replicated private blocks), the exact negative ELBO is

    F = m_q KL(q‖p) + m_s KL(s‖r) + m_o(−E_ζ log ℓ) + I_ζ(K;M) + n′_β KL(β‖π̃) + n_β Σβ E + n′_γ KL(γ‖π̃^s) + n_γ Σγ E^s,

with seven independent positive-integer multiplicities. (Private replication verified: with m_q i.i.d. K-blocks and m_s i.i.d. M-blocks and ζ on the "live" pair only, KL = m_q KL(q‖p) + m_s KL(s‖r) + I_ζ(K;M) − E_ζ log ℓ; the mutual-information correction of exact-elbo-proof.md:44-55 is unchanged.) Matching F = c·S_PIFB gives c = m_o = n_β = n_γ and τ = n′_β/c, τ_s = n′_γ/c, α = m_q/c, λ_s = m_s/c: **all positive rationals with a common denominator c, exactly as (★) predicts, with zero extra terms.**

At PIFB2's own normalization (unit observation coefficient, unit row-energy coefficient), c = 1 and the reachable set collapses to **τ, τ_s, α, λ_s ∈ ℤ_{≥0}**.

---

## 3. THEOREM C: tempering — verifying the roadmap warning

The roadmap warns (2026-08-12-elbo-pifb2-construction-roadmap.md:88-89): "Nonunit temperature requires a separately normalized tempered model; row entropy cannot simply be rescaled while leaving its normalizers behind." **VERIFIED, and quantified.**

### (C1) No-rescaling lemma (a stronger statement than tempering-specific)

Suppose some normalized w satisfies KL(q‖w) = (1/τ)KL(q‖u) + C for all q in a convex 𝒬 with two distinct elements. Rearranged,

    (1 − 1/τ) ∫ q log q dν = ∫ q log(w u^{−1/τ}) dν + C.

The right side is affine in q. The left is (1−1/τ) times the strictly convex functional q ↦ ∫ q log q. On the segment q_t = (1−t)q_0 + tq_1 the right side is affine in t and the left is strictly convex (τ>1) or strictly concave (τ<1) — contradiction unless τ = 1. Then ∫ q log(w/u) = −C for all q ∈ 𝒬 gives log(w/u) = −C ν-a.e., and normalization gives C = 0, w = u. ∎

**So no source law whatsoever — tempered, mixed, reweighted, anything — reproduces a pure temperature rescaling of the peer energy.** Tempering is not one option among many; it is the best available approximation, and Theorem C2 computes exactly how it fails.

### (C2) The exact tempered row and its three residues

Set u_b^{(τ)} := u_b^{1/τ}/Z_b, Z_b := ∫ u_b^{1/τ} dν. Each u_b^{(τ)} is a probability, so P(dj,dx) = π̃_j u_j^{(τ)}(dx) is exactly normalized and KL(Q‖P) is an honest exact ELBO row. Direct expansion (verified numerically to 5.6e-17 on a two-atom fiber, τ = 2.7):

    KL(q‖u_b^{(τ)}) = (1/τ) KL(q‖u_b) + (1/τ − 1) H_ν(q) + log Z_b.

Therefore, with π̂_b := (π̃_b/Z_b)/W and W := Σ_k π̃_k/Z_k,

    KL(Q‖P) = KL(β‖π̂) + (1/τ) Σ_b β_b E_b + (1/τ − 1) H_ν(q) − log W,
    **τ · KL(Q‖P) = [ τ KL(β‖π̂) + Σ_b β_b E_b ] + (1−τ) H_ν(q) − τ log W.**

Three residues relative to PIFB2's row τKL(β‖π̃) + Σβ_b E_b:

 **(E1) Per-source log-normalizer, β-DEPENDENT.** The prior is distorted π̃ ↦ π̂ ∝ π̃/Z. The optimum moves:
    β*_b ∝ π̃_b Z_b^{−1} exp(−E_b/τ),
 versus PIFB2's β*_b ∝ π̃_b exp(−E_b/τ). This is **NOT absorbable into a constant c_h**. It is absorbable into the attention prior, and only there. For Gaussian sources on ℝ^K (symbolically verified):

    log Z_b = (K/2)[(1 − 1/τ)log 2π + log τ] + ((τ−1)/(2τ)) log|S_b|,   log Z_b|_{τ=1} = 0,

 so **β*_b ∝ π̃_b |S_b|^{−(τ−1)/(2τ)} exp(−E_b/τ)** — exactly the "additional per-source log-determinant logit which the engineered form omits" that PIFB2.tex:678 concedes qualitatively, now with its coefficient. Note also that u_b^{(τ)} = N(m_b, τ S_b), matching :678's "the link covariance is τ times the transported sender covariance". This route *is* the construction :678 points to; what is new here is the coefficient and the next residue.

 **When is E1 harmless?** Exactly when Z_b is b-independent, i.e. |S_b| is b-independent. With S_b = Ω_ab Σ_b Ω_ab^T under PIFB2's Regime-I coboundary Ω_ab = e^{φ_a}e^{−φ_b} (PIFB2.tex:311-316), |S_b| = e^{2 tr(φ_a − φ_b)}|Σ_b|. Harmless iff e^{2tr(φ_a−φ_b)}|Σ_b| is b-independent — e.g. common source covariance and unimodular transports (tr φ_a = tr φ_b, i.e. frames in SL(K)). PIFB2's canonical group is GL(K_q,ℝ) (PIFB2.tex:434), so this is a genuine, checkable, non-generic gauge restriction, not an idealization.

 **(E2) Entropy defect (1−τ)H_ν(q), β-independent but q-DEPENDENT and reference-dependent.** PIFB2's action contains no bare belief-entropy term. Lemma 0 explains exactly what this is: the exact row has entropy coefficient −1 (one copy block); multiplying by τ makes it −τ, and (1−τ)H_ν(q) is precisely the defect. **The entropy term is the fingerprint of the illegal rescaling.** It is not absorbable into c_h while q is free. Sign: for τ > 1 the exact model rewards diffuse beliefs; for τ < 1 it rewards sharp ones.
 It *can* be cancelled by tempering a second block in the opposite direction (e.g. private prior p^{1/σ}/Z_p with 1/σ + 1/τ = 2), but the cancellation is rigid: it locks α = 2τ − 1, so the freedom is spent, not gained.

 **(E3) −τ log W: a pure constant.** Absorbable into c_h. This is the *only* residue that the effective-action run's c_h can legitimately swallow.

---

## 4. THEOREM D: the one genuinely free real knob

Replace ℓ_a by ℓ_a^θ/c_θ(k,m), c_θ(k,m) := ∫ ℓ_a(o|k,m)^θ ν_a(do). This is exactly normalized in the observation. The exact ELBO observation term is

    −θ E_ζ log ℓ_a + E_ζ[log c_θ(K_a, M_a)].

The second term is a **per-state log-normalizer**, the observation-channel analogue of E1. It is a pure constant iff c_θ is (k,m)-independent. Symbolic check for the Gaussian location family ℓ(o|k) = N(o; k, R): c_θ = √2 (√2/2)^θ (πR)^{(1−θ)/2}/√θ, with ∂c_θ/∂k = 0. **Constant.** PIFB2's working framework has Gaussian fibers and a fixed observation channel (PIFB2.tex:434, :341), so (H9) holds there.

This is the promised generalized-Bayes check. Bissiri–Holmes–Walker / Grünwald safe-Bayes construct the Gibbs posterior π(θ)ℓ^θ/∫π ℓ^θ, normalized **in the parameter**. Using ℓ^θ as a *generative likelihood* requires normalization **in the data**, which is the factor c_θ. BHW never needs it; an exact ELBO does. Under (H9) it is a constant; under heteroscedastic or precision-learning likelihoods it is a q-dependent extra term and the construction fails.

Consequence: θ is a free positive real that rescales the whole information sector against the evidence. So *every individual* coefficient of S_PIFB is a free real; what is quantized is only the set of ratios in Corollary A1. Note also that likelihood tempering moves α and λ_s *together* and leaves τ at 1 — it is not a temperature knob.

---

## 5. THEOREM F: latent temperature

Route (c) for τ. Let the redundancy count N ~ ρ on ℤ_{≥0} be latent, with conditional row n KL(β‖π̃) + Σβ_b E_b (Theorem B1 at each n). Recognition ξ on N. Then, exactly,

    F = KL(ξ‖ρ) + E_ξ[N]·KL(β‖π̃) + Σ_b β_b E_b,

and profiling ξ gives F_red = −log Σ_n ρ_n e^{−n u} + Σ_b β_b E_b with u := KL(β‖π̃). Requiring F_red − Σβ_b E_b = τ u for all u ≥ 0 means the generating function G(z) := Σ_n ρ_n z^n equals z^τ on (0,1]. A probability generating function is analytic at 0, and z^τ is analytic at 0 only for τ ∈ ℤ_{≥0}. **So even a fully profiled latent temperature yields only integer τ.** For nondegenerate ρ one instead gets a state-dependent τ_eff(β) = E[N | u] = d/du F_red, nonincreasing in u — the attention temperature *cools* as the row diverges from its prior. That is a genuinely different theory from PIFB2's state-independent learnable κ, and it is the only exactly-normalized adaptive-temperature mechanism I found.

A Dirac recognition ξ = δ_{τ} on a *continuous* temperature latent has KL(δ_τ‖ρ) = +∞ against any nonatomic ρ — no exact ELBO at all. Against an atomic ρ with mass ρ_0 at τ it contributes the constant −log ρ_0 (harmless), but the Theorem C residues E1 and E2 remain untouched because the conditional model is still tempered.

---

## 6. THEOREM E: state-dependent precision

### (E1) The obstruction

PIFB2's adaptive sector is α_i(c) KL(q_i‖p_i) + R(α_i), R(α) = b_0α − c_0 log α (PIFB2.tex:746-757), with envelope optimum α_i*(c) = c_0/(b_0 + D) (PIFB2.tex:776-780) and the exact envelope cancellation of PIFB2.tex:826. Its **reduced value** is (symbolically verified)

    min_{α>0}[ αD + b_0α − c_0 log α ] = **c_0 log(b_0 + D) + c_0 − c_0 log c_0**,  D := KL(q‖p).

Apply the HEAT TEST to G(q) := c_0 log(b_0 + D). With q = N(μ, vI_K), p = N(0, I_K), m := |μ|²,
D = ½[Kv + m − K − K log v], and the implied block count N(v,m) := −(2v/K)[∂_v G − ½Δ_μ G] evaluates (K=2, c_0=b_0=1) to

    (v,m) = (1,0) → 1.000000 ;  (1,1) → 0.444444 ;  (2,0) → 0.765197 ;  (2,3) → −0.024516 ;  (0.5,0.2) → 0.743407 ;  (3,5) → −0.159951.

Not constant; not even nonnegative. Since an exact ELBO with tied q-blocks must return a constant nonnegative integer, **G is not the recognition-dependent part of any fixed normalized joint with tied q-blocks.** OBSTRUCTED. (Control: for F = αD the same test returns exactly α; for an arbitrary affine functional it returns 0.)

The same conclusion holds on a two-atom fiber without any Gaussian hypothesis: requiring c_0 log(b_0+D) = ND + affine forces, at the point D = 0, N = c_0/b_0, and then the second-order condition reduces to D′²/(b_0+D) + D D″/b_0 = 0 with both terms nonnegative, forcing D ≡ 0.

### (E2)–(E3) What state dependence actually costs, and what it buys

A constant coefficient is reachable iff it is a nonnegative integer (relative to c). A state-dependent one is reachable **only as a profiled ELBO**, and the unprofiled exact ELBO then carries KL(ξ‖ρ) explicitly — a term S_PIFB does not have. The clean exactly-normalized realization is a *marked* latent space: ⊔_N 𝖪^N with P(N, dk_{1:N}) = ρ(N)Π p(dk_t), Q(N, dk_{1:N}) = ξ(N)Π q(dk_t). Verified by brute force (residual 1.1e-16):

    **KL(Q‖P) = KL(ξ‖ρ) + E_ξ[N]·KL(q‖p),  exactly.**

Profiling ξ gives F_red(D) = −log Σ_n ρ_n e^{−nD−h_n}, concave and nondecreasing in D, with **α(D) = F_red′(D) = E[n | D]** — the reachable class of exactly-normalized state-dependent precisions: nonnegative, nonincreasing in D (since α′ = −Var[n] ≤ 0), and always a tilted lattice mean. PIFB2's α* = c_0/(b_0+D) is nonnegative and nonincreasing, so it is *qualitatively* in this class.

### (E4) The Gamma identity, and why it is a coincidence rather than a realization

PIFB2 already identifies R with a Gamma negative log-density: PIFB2.tex:758-763 gives p(α|b_0,c_0) = b_0^{c_0+1}α^{c_0}e^{−b_0α}/Γ(c_0+1), i.e. **Gamma(shape c_0+1, rate b_0)**, and PIFB2.tex:771 states plainly that α_i* is "the fixed-hyperparameter MAP precision". What is new is the *marginal* comparison. Symbolically,

    min_α[αD + R(α)]                        = c_0 log(b_0 + D) + c_0 − c_0 log c_0,
    −log E_{Gamma(shape c_0, rate b_0)}[e^{−ΛD}] = c_0 log(b_0 + D) − c_0 log b_0,
    difference = c_0(1 + log(b_0/c_0)),  with d/dD ≡ 0.

**PIFB2's envelope-reduced precision sector equals, up to an exact D-free constant, the fully optimized variational free energy of a Gamma(c_0, b_0) latent precision.** Note the shape shifts by one: MAP of Gamma(c_0+1) = marginal of Gamma(c_0). They coincide identically when b_0 = c_0/e.

But this is a functional coincidence, not an exact-ELBO realization, for two independent reasons:
 (i) The conditional model must contribute Λ·KL(q‖p) at fixed Λ. By Lemma 0 that requires Λ tied q-blocks, so **Λ ∈ ℤ_{≥0}**. The representing measure of (b_0+D)^{−c_0} is the Gamma density on (0,∞), and by uniqueness of Laplace transforms no lattice-supported ρ reproduces it.
 (ii) Substituting tempering for replication does not repair it: with p^Λ/Z(Λ) the conditional gives ΛD − (1−Λ)H_ν(q) + log Z(Λ), and profiling yields −H_ν(q) − Λ̃(w) with w := ∫ q log p. Demanding that this be a function of D = −H − w alone forces Λ̃′ ≡ 1, i.e. ρ̃ = δ_1, i.e. α ≡ 1.
 (iii) Separately, PIFB2's α* is a **MAP**, i.e. a Dirac recognition on a continuous latent, and KL(δ_α‖Gamma) = +∞. A MAP-profiled sector is not an exact ELBO of anything.

So the precision sector is *nearly* ELBO-founded and the near-miss is exactly characterizable: right functional form, wrong (continuous) representing measure, and a point-estimate recognition where a diffuse one is required.

---

## 7. VERDICT TABLE

| Coefficient (as deployed) | Reachable? | Construction | Extra term forced into the action |
|---|---|---|---|
| τ ∈ {1,2,3,…} | **YES**, exact | n′ redundant i.i.d. source labels, only label #1 read (Thm B1) | **none** |
| τ ∈ {1, 1/2, 1/3, …} | **YES**, exact | n i.i.d. relational copies per label (Thm B2) | **none**, but global scale ×n |
| τ ∈ ℚ_{>0} | **YES**, exact | n′ labels × n copies; c = n; observation counted c times (Thm B) | **none**; all coefficients share denominator c |
| τ ∈ ℝ∖ℚ, one channel | **NO as an exact-ELBO coefficient**; reachable only up to the residues below | tempered sources u_b^{1/τ}/Z_b (Thm C2) | (a) β-dependent per-source logit −log Z_b = −((τ−1)/2τ)log|S_b| in the Gaussian case, absorbable **only into the attention prior**, not into c_h; (b) belief-entropy term (1−τ)H_ν(q), not in PIFB2; (c) harmless constant −τ log W |
| τ_β = κ√K_q *and* τ_γ = κ√K_m together | **NO — OBSTRUCTED** | — | none exists: the required ratio √(K_q/K_m) must be rational (Cor. A2). Escapes: K_m = K_q, or K_q/K_m a rational square |
| τ = κ√K_q with α = 1, κ learnable real | **NO for a.e. κ** | — | admissible κ set is (1/√K_q)·ℚ, Lebesgue-null (Cor. A3) |
| state-dependent τ_eff(β) | **YES**, exact | latent redundancy count N ~ ρ, profiled (Thm F) | **KL(ξ‖ρ)** in the unprofiled action; τ_eff is forced *nonincreasing* in KL(β‖π̃) — a different theory from a constant learnable κ |
| α ∈ ℤ_{≥0} on KL(q‖p) | **YES**, exact | α replicated private state blocks (Thm B) | **none**; I_ζ(K;M) unchanged |
| λ_s ∈ ℤ_{≥0} on KL(s‖r) | **YES**, exact | λ_s replicated private model blocks | **none** |
| λ_h = 1 (PIFB2.tex:694) | **YES**, exact | one private model block; already in the closed theorem | **none** |
| α, λ_s ∈ ℝ_{>0} individually | **YES**, exact | temper the likelihood at exponent θ (Thm D) | pure constant **iff** ∫ℓ(o|k,m)^θ ν(do) is (k,m)-free (holds for Gaussian/location likelihoods; **fails** for heteroscedastic ones, where it becomes E_ζ log c_θ(K,M)) |
| α, λ_s with irrational ratio (α+1)/(λ_s+1) | **NO — OBSTRUCTED** (under H5) | — | Cor. A1 |
| non-integer α by power prior p^α/Z_p | reachable only with a residue | fractional/power prior | **−(1−α)H_ν(q)**, reference-dependent; plus harmless log Z_p. Verified: KL(q‖p^α/Z_p) = αKL(q‖p) − (1−α)H_ν(q) + log Z_p |
| state-dependent α_i(c), any form | **YES for the class α(D) = E[n | D]** (nonneg., nonincreasing, tilted-lattice mean) | latent replica count on a marked space; KL(Q‖P) = KL(ξ‖ρ) + E_ξ[N]KL(q‖p) exactly (Thm E3) | **KL(ξ‖ρ)** — absent from S_PIFB |
| PIFB2's specific α* = c_0/(b_0+D) | **NO — OBSTRUCTED** | — | heat test returns a nonconstant, sometimes negative implied block count (Thm E1). Its reduced value *equals* the Gamma(c_0,b_0) marginal free energy up to the constant c_0(1+log(b_0/c_0)) (Thm E4), but the representing measure is continuous, hence not a block count; and the deployed α* is a MAP (Dirac ⇒ KL = +∞) |
| smooth χ_i(c) ∈ (0,1) on T1, T2 | **NO — OBSTRUCTED** | — | quantized to {0,1} (Cor. A4). Matches the manuscript's own hard χ in PIFB2.tex:3755 |
| χ_ij on T3, T4 | **YES**, exact | already absorbed into π̃_ij (PIFB2.tex:694) | **none** (affine prior redefinition) |
| χ_i on T5 (observation) | **YES**, exact real | likelihood exponent θ = χ_i (Thm D) | constant, under (H9) |

**One-line summary.** Non-unit coefficients on *entropy-carrying* blocks are block counts: integers, up to one global scale. Non-unit coefficients on *affine* pieces (priors, likelihood exponents) are free reals. τ, α, λ_s, and χ|_{T1,T2} are all of the first kind; the attention prior and the observation exponent are of the second. The single strongest consequence is that the deployed pair (κ√K_q, κ√K_m) is obstructed unless K_q/K_m is a rational square, and that with α = 1 a continuously learnable κ is admissible only on a null set.

## obstructions

### 1

OBSTRUCTION 1 (two-channel irrationality, decisive). Corollary A2: the deployed temperature pair tau_beta = kappa*sqrt(K_q), tau_gamma = kappa*sqrt(K_m) (PIFB2.tex:673) requires tau_beta/tau_gamma = sqrt(K_q/K_m) to be a ratio of nonnegative integers. Whenever K_q/K_m is not the square of a rational, NO normalized generative model in the tied-replica class realizes the pair, for any kappa, any global scale, any tempering, any replication, any latent. kappa cancels, so tuning cannot dodge it. Escape: tie the fibers (K_m = K_q, MAgent gauge_agent/agents.py:911) or restrict K_q/K_m to rational squares.

### 2

OBSTRUCTION 2 (learnable kappa). Corollary A3: at PIFB2's canonical alpha = 1 (PIFB2.tex:694), tau must be rational, so kappa must lie in (1/sqrt(K_q))*Q, a Lebesgue-null set. A continuously learned kappa (gauge_agent/softmax_utils.py:12) is almost surely inadmissible.

### 3

OBSTRUCTION 3 (no exact temperature rescaling). Theorem C1: there is NO probability law w with KL(q||w) = (1/tau)KL(q||u) + const for all q in a nondegenerate convex family, unless tau = 1 and w = u. Tempering is not one option among many; it is provably the closest possible, and its residue is unavoidable.

### 4

OBSTRUCTION 4 (tempering leaves a beta-dependent normalizer). Theorem C2: the tempered row's optimum is beta*_b prop to pi_b Z_b^{-1} exp(-E_b/tau), Gaussian log Z_b = const + ((tau-1)/(2tau)) log|S_b|. This is NOT absorbable into a constant c_h; it is absorbable only into the attention prior. It vanishes only under the non-generic gauge condition that |Omega_ab Sigma_b Omega_ab^T| be b-independent (unimodular frames + common source covariance), which GL(K_q,R) (PIFB2.tex:434) does not supply.

### 5

OBSTRUCTION 5 (tempering leaves a belief-entropy term). Theorem C2: the residue (1-tau)H_nu(q) is q-dependent and reference-dependent, and PIFB2's action has no belief-entropy term. By Lemma 0 it is exactly the entropy-coefficient defect created by multiplying an exact ELBO block by tau. Cancelling it by counter-tempering the private prior is possible but rigidly locks alpha = 2tau - 1.

### 6

OBSTRUCTION 6 (state-dependent precision). Theorem E1: the heat-equation test on the isotropic Gaussian sub-family returns a nonconstant, sometimes negative implied block count for PIFB2's envelope-reduced sector c_0 log(b_0 + D_KL(q||p)). Hence it is not the recognition-dependent part of any fixed normalized joint with tied q-blocks. Compounded by: the deployed alpha* is a MAP (PIFB2.tex:771), i.e. a Dirac recognition on a continuous latent, whose KL against the Gamma prior is +infinity.

### 7

OBSTRUCTION 7 (Laplace uniqueness blocks the Gamma realization). Theorem E4: (b_0+D)^{-c_0} has a unique representing measure, the Gamma(c_0,b_0) density on (0,infinity). Block counts are lattice-valued. So the exact functional identity between PIFB2's envelope and the Gamma marginal free energy cannot be promoted to an exact-ELBO realization. Substituting tempering for replication forces Lambda = 1 identically.

### 8

OBSTRUCTION 8 (smooth support functions). Corollary A4: the explicit chi_i(c) in (0,1) on T1 and T2 (PIFB2.tex:685-686) is a private coefficient and is quantized to {0,1}. PIFB2 declares chi_i smooth precisely to keep the bundle language well typed (PIFB2.tex:711), so the smooth-section convention and the exact-ELBO reading are in direct conflict on those two terms.

### 9

SCOPE LIMIT A. All results are for the LAGGED conditional model. The same-time reciprocal case is untouched and remains open in all three prior runs (exact run CE-6; fast-slow CE-1; effective-action CE-3): the generative denominator would read Q^{n+1}.

### 10

SCOPE LIMIT B. Theorem A is unconditional in P, but the fiber-block corollaries (alpha, lambda_s, chi on T1/T2) need hypothesis (H5) that P factorizes across latent blocks, or a recognition family containing a nondegenerate mixture segment. On a strictly parametric family (Gaussians) with a non-product P, the argument reduces to the heat test, which needs (H6).

### 11

SCOPE LIMIT C. The tied-replica hypothesis (H3) is load bearing. If a recognition block's law is allowed to be a nonlinear function of the displayed q (a warped tie, e.g. q^theta/Z), the entropy count changes and the theorems do not apply. Warping does NOT rescue tau, however: the tau argument uses only the categorical beta blocks. Mixture-tying with mutually singular components also stays inside the conclusion, since it still contributes integer multiples of H(beta).

### 12

SCOPE LIMIT D. Theorem D's free real scale requires (H9): int ell(o|k,m)^theta nu(do) independent of (k,m). It holds for Gaussian/location likelihoods with (k,m)-independent noise and FAILS for heteroscedastic or precision-learning observation models, where the extra term E_zeta log c_theta(K,M) is genuinely state dependent.

### 13

SCOPE LIMIT E. Nothing here addresses the continuum limit. Per boundary-counterexamples.md:60-66, multiplying site terms by cell volumes is not an exact finite-law ELBO; the quantization theorem is a statement about counting measure on a finite index set and does not survive naive quadrature weighting. A cell weight h^d is precisely a non-integer private coefficient and falls under Obstruction 8's mechanism.


## novelty

Partly new. What is ALREADY on record, and must not be re-claimed: (1) the tau != 1 mismatch (tau-1)D_KL(beta||pi) is computed at docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/boundary-counterexamples.md:39-50; (2) the one-sentence, unproved assertion "Positive integer coefficients can be represented by repeated independent copies with tied recognition; arbitrary real coefficients require a powered or generalized construction and its normalizers" is at the same file :52-59; (3) the roadmap warning "row entropy cannot simply be rescaled while leaving its normalizers behind" is at docs/research-plans/2026-08-12-elbo-pifb2-construction-roadmap.md:88-89; (4) PIFB2.tex:678 already concedes that tau = 1 is forced, that the link covariance must be tau times the transported sender covariance, and that "the exact construction carries an additional per-source log-determinant logit which the engineered form omits"; (5) PIFB2.tex:758-763 already identifies R(alpha) = b_0 alpha - c_0 log alpha with the negative log-density of Gamma(shape c_0+1, rate b_0), and PIFB2.tex:771 already states that alpha_i* is "the fixed-hyperparameter MAP precision". NEW here: (a) Lemma 0, the unit-entropy principle, and Theorem A, the first PROOF that a temperature is a block count, via non-polynomiality of Shannon entropy on a simplex segment (all even derivatives of order >= 4 strictly positive) -- no such result appears in Theory/*.tex or any of the three derivation runs (grep for "unit entropy|entropy coefficient|quantiz|replica count|tempered prior|power prior|fractional posterior|Bissiri|Grunwald|safe Bayes" over Theory/ and docs/derivations returns only Theory/05_elbo.tex:53, an unrelated partition-refinement "quantization"); (b) Corollary A1, the rationality of all pairwise ratios among {tau, tau_s, alpha+1, lambda_s+1}; (c) Corollary A2, the sqrt(K_q/K_m) obstruction to the deployed two-channel temperature pair, which is kappa-free and scale-free -- this is a new, decisive, checkable negative result about the deployed configuration; (d) Corollary A3, that a continuously learnable kappa is admissible only on a Lebesgue-null set; (e) Corollary A4, the term-by-term chi verdict (obstructed on T1/T2, free on T3/T4/T5) and its corroboration of the hard chi in PIFB2.tex:3755; (f) Theorem B1, the redundant-label mechanism reaching tau in {1,2,3,...} -- the task's route (a) as posed reaches only tau <= 1, and the tau >= 1 direction appears nowhere in the corpus; (g) Theorem C1, the no-rescaling lemma, which is strictly stronger than the tempering-specific warning: no source law of any kind rescales a KL; (h) the exact Gaussian coefficient (tau-1)/(2tau) on log|S_b|, quantifying PIFB2.tex:678's qualitative concession, together with the exact gauge side condition (unimodular frames, common source covariance) under which it is harmless; (i) the entropy residue (1-tau)H_nu(q), which appears nowhere in PIFB2 or the runs, and its identification as the entropy-coefficient defect; (j) Theorem D, the exact data-side normalization check on the BHW/safe-Bayes route, with the symbolic verification that the Gaussian location family makes it constant; (k) Theorem E1, the heat-equation obstruction to any state-dependent coefficient, with the numerical implied-block-count table; (l) Theorem E3, the exact marked-space identity KL(Q||P) = KL(xi||rho) + E_xi[N] KL(q||p) and the characterization alpha(D) = E[n|D] of the reachable state-dependent precisions; (m) Theorem E4, the exact constant c_0(1 + log(b_0/c_0)) between PIFB2's MAP-of-Gamma(c_0+1) envelope and the marginal-of-Gamma(c_0) free energy, and the Laplace-uniqueness obstruction to realizing it; (n) Theorem F, that even a fully profiled latent temperature gives only integer tau (probability generating function z^tau analytic at 0 iff tau in Z), plus the observation that the only exactly-normalized adaptive temperature must be nonincreasing in KL(beta||pi).

## next_obligations

### 1

Decide the deployed fiber dimensions. Corollary A2 is decisive but conditional: record K_q and K_m for every checked-in MAgent configuration and mark each as ADMISSIBLE (K_q/K_m a rational square, in particular the tied-fiber path gauge_agent/agents.py:911) or OBSTRUCTED. I could not resolve this from the worktree; MAgent's dims are configurable and no default was located.

### 2

Extend Theorem A past hypothesis (H3). Prove or refute: does the quantization survive recognition families whose blocks are nonlinear functions of the displayed q, s, beta, gamma (warped ties)? The tau conclusion is already robust (it uses only the categorical blocks); the alpha/lambda_s conclusions are not.

### 3

Remove hypothesis (H5) from the fiber-block corollaries, or exhibit a non-product P for which a non-integer alpha is exactly reachable on the Gaussian family. The heat test (H6) is currently the only route there and it needs differentiation under the integral sign.

### 4

Compute the numerical cost of the tempering residues on the deployed system. Both residues are explicit: the logit shift ((tau-1)/2tau) log|S_b| and the entropy term (1-tau)H_nu(q). Evaluate ||beta*_tempered - beta*_PIFB|| and the induced free-energy gap on a checked-in MAgent run to convert Obstructions 4-5 from qualitative to quantitative.

### 5

Test the gauge escape for Obstruction 4. Determine whether restricting the frame group to SL(K_q) (traceless phi_i) with a common source covariance is compatible with the rest of PIFB2's dynamics; if so, tempering becomes exact up to the entropy residue alone.

### 6

Decide the precision sector. Either (i) replace the log-barrier envelope by the marked-space latent-count construction of Theorem E3, accepting KL(xi||rho) in the action and a lattice-valued precision, or (ii) retain the envelope and re-label the precision sector as an explicitly non-ELBO regularizer. The manuscript's own note that a normalized learned hierarchy 'remains prospective' (PIFB2.tex:771) is the natural place to record whichever is chosen.

### 7

Re-type the smooth presence functions. Corollary A4 puts the smooth-section convention (PIFB2.tex:711) in conflict with the exact-ELBO reading on T1 and T2. Either move chi_i entirely into the prior and the likelihood exponent (where it is free), or adopt hard masks on the self terms as PIFB2.tex:3755 already does.

### 8

Carry the quantization theorem into the continuum program. A cell weight h^d on a pointwise sector (roadmap step 6, 2026-08-12-elbo-pifb2-construction-roadmap.md:168-169; lattice-continuum-asymptotics.md:22-23) is a non-integer private coefficient and is obstructed by the same mechanism as smooth chi. Determine whether the continuum action can only ever be a deterministic Gamma-limit object rather than an exact process-law ELBO, which would sharpen release obligation (4) of the effective-action run.

### 9

Settle the same-time case. Every result here is conditional on the lagged model (H2). Whether the quantization survives a same-time reciprocal construction is untested and depends on whichever escape route (configuration-law promotion or empirical-measure LDP) is eventually taken.


## evidence_kind

FORMAL_PROOF (Lemma 0, Theorems A, C1, F; Corollaries A1-A4) + DERIVATION (Theorems B, C2, D, E2-E4, verified by exact symbolic computation and brute-force enumeration) + COUNTEREXAMPLE/OBSTRUCTION (Theorem E1, the heat-equation test with an explicit nonconstant implied block count). All numerical checks: redundant-label identity residual <= 2.0e-15 for n'=1..4; copy-replication residual <= 3.3e-16 for n=1..3; tempered-KL identity residual 5.6e-17; power-prior identity residual 1.5e-16; marked-space latent-count identity residual 1.1e-16; softmax optimum vs PIFB2 beta* agreement to 2e-9; envelope-minus-Gamma-marginal difference symbolically D-free with d/dD = 0 exactly; Gaussian log Z_b coefficient matches (tau-1)/(2tau) exactly (symbolic difference 0); Gaussian location-family tempered-likelihood normalizer has d/dk = 0 exactly.
