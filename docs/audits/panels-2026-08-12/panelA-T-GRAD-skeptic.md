# panelA-T-GRAD-skeptic

*Recovered verbatim from workflow journal.jsonl, 2026-08-13. Agent a4b546f6.*

## survives

false

## confidence

high

## corrected_statement

PART I (items 1-4) SURVIVES essentially intact — I reproduced every symbolic and numerical figure independently — subject to three corrections. (i) In (A) the O(h) coefficient must be stated invariantly: c_3 = (1/2) g^F(D^A_mu q, nabla^(e)_mu D^A_mu q) + (1/6) T_AC(D^A_mu q, D^A_mu q, D^A_mu q), with nabla^(e) Amari's alpha=+1 connection. As displayed — with "(D^A_mu)^2 q" and W — it is chart-dependent term-by-term and (D^A_mu)^2 is undefined by the source geometry (Theory/05c_pullback_geometry.tex:99-107); only the sum is invariant. This is precisely the ambiguity Theory/05c_pullback_geometry.tex:578-587 warns of. (ii) §3.5 is wrong: for the fixed-covariance Gaussian mean submodel the exact h^4 coefficient is (1/4)g^F(w,w) + (1/3)g^F(v,u), not "(h^4/4)|w|^2 identically". (iii) (H2) must add E_theta[sup_{eta in U}|d_i ell_eta|] < inf and E_theta[sup_{eta in U}|d_i d_j ell_eta|] < inf (or derive them from (H2)(c) + convexity of U); (H2)(b) dominates d^alpha p_theta, not d^alpha log p_eta, and no lower bound on p is assumed. (D)'s "iff" holds only quantified over all sections and needs symmetric edge WEIGHTS.

PART II IS NOT REFUTED IN THE STRONG FORM. Its identities (E), (F), (G), the (5.3) limit, and (I) are all correct — I reproduced every quoted number — but the conclusion drawn from (H) is false. The correct statement:

THEOREM (corrected item 5). Under (H1)-(H7), with A = {i} x Lambda_h, belief sources the 2d base neighbours, u_{c,c'} = (Omega^A_{c,c'})_# q_i^n(c'), frozen beta = pi uniform, replication m_h = ceil(d h^{-2}), and private potential V(q) := KL(q||p) - E_zeta log ell, the EXACT one-step negative ELBO has a unique stationary point satisfying, in a chart, pointwise and uniformly on compact regular strata,

    q_i^{n+1}(c) - q_i^n(c) = (h^2/d) [ (1/2) Delta^{(e),A} q_i^n(c) - grad^{g^F} V(q_i^n(c)) ] + O(h^3),

where Delta^{(e),A} := Sum_mu nabla^(e)_mu D^A_mu combines the gauge connection A with Amari's alpha=+1 (exponential) connection on the fibre. Consequently:
 (a) The base-neighbour block is NOT a pure mass term with minimizer phi = 0. It is a FORWARD-EULER (minimizing-movement) step of a covariant diffusion with time step Delta t = h^2/d; the minimizer is phi* = (h/(2d)) Delta^{(e),A} q^n. In closed form the block's argmin is the exponential-family barycentre prod_b u_b^{beta_b} / Z of the transported neighbours — a discrete heat-kernel average. "The gradient operator acts on the wrong field" is wrong: acting on q^n is what an explicit discretisation requires.
 (b) m_h = ceil(d h^{-2}) is exactly the parabolic scaling Delta t proportional to h^2 — still a declaration, but the canonically forced one, not an arbitrary postulate. At d = 2 no weighting is needed at all.
 (c) The block's value at the diagonal is exactly (1/2) INT_C ||D^A q||^2_{g^F} dc + O(h^2). The covariant Fisher-Dirichlet term IS the block's energy.
 (d) THE TRUE RESIDUAL OBSTRUCTION, which the claim missed and which its own Part I exposes: the operator generated is Delta^{(e)}, whereas the Euler-Lagrange operator of (1/2) INT ||D^A q||^2_{g^F} is Delta^{(LC)} = Delta^{(e)} + (1/2)(g^F)^{-1} T_AC(D_mu q, D_mu q). The KL orientation of ANY ELBO (recognition in slot 1) forces alpha = +1; the reverse orientation forces alpha = -1 (m-projection / moment matching); neither is alpha = 0. Verified numerically to 6-7 digits with the alpha=0 and alpha=-1 mismatches O(1) and non-vanishing in h. Hence the ELBO's stationary sections are e-harmonic (Delta^{(e),A} q = grad^{g^F} V), NOT critical points of the Fisher-Dirichlet action. This is not repaired by evaluating at q^{n+1} = q^n; it persists at every fixed point. It vanishes exactly when T_AC(D_mu q, D_mu q) = 0 along the section — in particular on Gaussian mean submodels with fixed covariance, matching Theory/08_infogeometry.tex:238-247.

NET VERDICT ON THE TARGET T-GRAD. The covariant Fisher-Dirichlet term is ELBO-derived as an ENERGY VALUE and as the generator of a covariant diffusion, under one declared and canonically forced parabolic replication. It is NOT ELBO-derived as a VARIATIONAL PRINCIPLE: the action whose Euler-Lagrange equations the ELBO iterates is not the Fisher-Dirichlet action unless the Amari-Chentsov contraction vanishes along the section. The claim's status "PARTIAL" is right; its Part II reasoning is not. Also unchanged: Theorem 4.1 is pointwise convergence at a fixed C^2 section, not Gamma-convergence; equicoercivity, liminf, recovery, interpolation topology, and gauge compactness remain open (lattice-continuum-asymptotics.md:33-37), and h_q^omega depends on the pair (omega, q), with passive gauge covariance only (Theory/05c_pullback_geometry.tex:146-154, 220-231).

## attacks

### 1

{
  "attack": "VECTOR 1 (HIDDEN HYPOTHESIS) \u2014 (H2)(b) does not license the differentiations actually performed. Lemma 2.1 and Prop 2.2 differentiate D(theta,eta) = const(theta) - INT p_theta log p_eta dnu three times in eta under the integral sign. (H2)(b) dominates |partial^alpha p_theta| <= G in L^1(nu); (H2)(c) dominates the THIRD log-derivative. Nothing in (H2) dominates partial^alpha log p_eta for |alpha| = 1,2 under E_theta. Since d_i log p = d_i p / p and NO lower bound on p_theta(x) is assumed, the |alpha|=1,2 log-derivative bounds do NOT follow from (b).",
  "verdict": "REPAIRABLE",
  "reasoning": "Real gap, cheap fix. Either add explicitly 'E_theta[sup_{eta in U}|d_i ell_eta|] < inf and E_theta[sup_{eta in U}|d_i d_j ell_eta|] < inf', or derive them from (H2)(c) + convexity of U + finiteness at a single eta_0 in U by the mean value theorem: |d_i d_j ell_eta| <= |d_i d_j ell_{eta_0}| + diam(U) B(x). The Bartlett identities themselves (steps (ii),(iii)) ARE correctly licensed by (H2)(b), because those differentiate INT p_theta dnu, not the log. The claim's own remark that '(c) is what makes the third-order Taylor remainder UNIFORM ... the ground-phase audit correctly flags that the prior run never states it' is right; it just stopped one order short. Does not touch any conclusion."
}

### 2

{
  "attack": "VECTOR 1/5 (HIDDEN HYPOTHESIS + LEVEL CONFUSION) \u2014 statement (A)'s O(h) coefficient is not a well-defined geometric object as displayed. (A) writes the coefficient as INT sum_mu [(1/2) g^F(D^A_mu q, (D^A_mu)^2 q) - (1/6) W(D_mu q, D_mu q, D_mu q)]. But (D^A_mu)^2 q is nowhere defined: Theory/05c_pullback_geometry.tex:99-107 defines D^omega s as a VERTICAL-VALUED ONE-FORM along s and states 'it is not a linear covariant derivative on a vector space of sections'; iterating it requires a connection on VE that is never declared. What the derivation actually uses is w = theta-hat''(0), the CHART second derivative, which is not a tangent vector (it picks up psi''(v,v) under theta -> psi(theta)). W_ijk = E[d_i d_j d_k log p] is likewise not a tensor.",
  "verdict": "WEAKENS_SCOPE",
  "reasoning": "I verified the defect is in the STATEMENT, not the value: (1/2)g(v,w) and (1/2)Gamma^(e)(v,v,v) are individually chart-dependent, but their sum is (1/2)g^F(v, nabla^(e)_v v) with nabla^(e) Amari's alpha=+1 connection, which IS invariant, and T_AC is a tensor. So the correct invariant form is c_3 = (1/2)g^F(D^A_mu q, nabla^(e)_mu D^A_mu q) + (1/6)T_AC(D^A_mu q, D^A_mu q, D^A_mu q). The claim's own (3.2) is this, unlabelled. Consequence: \u00a73.4's headline decomposition into 4.392910 and -7.612181 is chart-dependent bookkeeping, so the sub-claim '(1/2)g^F(v,w) is NOT a total derivative' is not chart-invariant; only the aggregate int c_3 = -3.219270 != 0 is, and that does suffice for 'the O(h) term is not a total derivative'. This is exactly the ambiguity Theory/05c_pullback_geometry.tex:578-587 flags ('It also contains the covariant acceleration of s-hat and the connection coefficient selected by the one-sided divergence jet'); the claim cites that warning and then reintroduces the ambiguity in its own display."
}

### 3

{
  "attack": "VECTOR 3 (ASYMMETRY OF KL) \u2014 was the third-order term actually computed, and does argument order matter? Independently recomputed symbolically (SymPy, exact Gaussian integrals over the (mu,sigma) chart, deliberately non-natural so Gamma^(e) != 0).",
  "verdict": "FAILS_TO_LAND",
  "reasoning": "Every stated quantity reproduces EXACTLY. g^F = diag(1/sigma^2, 2/sigma^2); T_112 = 2/sigma^3, T_222 = 8/sigma^3; Gamma^(e)_{12,1} = Gamma^(e)_{21,1} = -2/sigma^3, Gamma^(e)_{22,2} = -6/sigma^3; W_112 = 2/sigma^3, W_222 = 10/sigma^3; W(d,d,d) = (6a^2 b + 10 b^3)/sigma^3 = -(T_AC + 3 Gamma^(e))(d,d,d), difference identically 0. Identity (3.1) W_ijk = -(T_ijk + G_ki,j + G_kj,i + G_ij,k) holds for all 8 index triples. Forward t^3 coefficient = -(1/6)W exactly; reverse t^3 = -(1/6)W + (1/6)T_AC; reverse - forward = 125 a^2 b/343 + 500 b^3/1029, matching the claim's quoted expression exactly. The +/- parity cancellation is exact: with theta-hat(eps) = theta_0 + eps v + eps^2 w/2 + eps^3 u/6 and free symbols, the h^3 coefficient of E(+h)+E(-h) is IDENTICALLY 0, independent of w and u. The parity argument is even more robust than the claim says: f(eps) := D(theta_0, theta-hat(eps)) is a single C^3 function of one variable with f(0)=f'(0)=0, so f(h)+f(-h) contains only even powers by elementary parity. Item 2 is correct and is the strongest part of the claim."
}

### 4

{
  "attack": "VECTOR 6 (TAUTOLOGY / hidden error) \u2014 \u00a73.5's exactly-solvable witness claims 'E(+h)+E(-h) = h^2|v|^2_J + (h^4/4)|w|^2_J identically' for the Gaussian mean submodel with fixed covariance.",
  "verdict": "REPAIRABLE",
  "reasoning": "FALSE as written. Symbolically, with the transported-back curve carried to third order, the exact h^4 coefficient is (1/4)g^F(w,w) + (1/3)g^F(v,u) where u = theta-hat'''(0); I confirmed the residual E(+h)+E(-h) - [h^2|v|^2 + h^4((1/4)|w|^2 + (1/3)<v,u>)]/C is exactly 0. The claim omits the (1/3)g^F(v,u) term and asserts 'identically', which holds only when u = 0. Consequence: the follow-on 'the symmetric lattice functional is exact up to a computable (h^4/8) sum_c |w|^2_J' is incomplete by (h^4/6) sum_c g^F(v,u). Purely a computational slip; it does not affect any convergence statement or any conclusion, since both terms are O(h^4)."
}

### 5

{
  "attack": "VECTOR 8 (COUNTEREXAMPLE) + VECTOR 2 (ORDER OF LIMITS) \u2014 THE DECISIVE ATTACK. (H) claims 'the only dependence on the free recognition variable is a positive-definite Fisher MASS term whose unique minimizer is phi = 0', 'the block acts as an infinitely stiff pin', 'the gradient operator acts on the wrong field'. I computed the block's exact minimizer in closed form on the claim's own d=1 circle/Gaussian instance.",
  "verdict": "KILLS_IT",
  "reasoning": "The block is Sum_b beta_b KL(q^{n+1}(c) || eta_b). For Gaussians this has a CLOSED-FORM argmin: m* = (Sum beta_b m_b/s_b^2)/(Sum beta_b/s_b^2), s* = 1/sqrt(Sum beta_b/s_b^2) \u2014 i.e. the EXPONENTIAL-family (e-geodesic) barycentre of the transported neighbours, equivalently the normalised geometric mean prod_b u_b^{beta_b}/Z (since Sum_b beta_b = 1, Sum_b beta_b KL(q||u_b) = KL(q||u-bar_beta) - log Z_beta). The minimizer is NOT theta^n. It is eps* = (h^2/(2d)) Delta^{(e),A} q^n, where Delta^{(e),A} := Sum_mu nabla^{(e)}_mu D^A_mu is the Laplacian of the gauge connection A composed with Amari's alpha=+1 connection on the fibre. Measured against the analytic prediction at four base points: max error 2.70e-2 (h=1e-2), 2.71e-4 (h=1e-3), 3.01e-6 (h=1e-4) \u2014 clean O(h^2) convergence. Adding the private potential V(q) = KL(q||p) the EXACT closed-form stationary point of the FULL one-step ELBO obeys q^{n+1} - q^n = (h^2/d)[(1/2)Delta^{(e),A} q^n - grad^{g^F} V(q^n)] + O(h^3), verified to 6-7 digits (errors 3.5e-3 -> 3.5e-5 -> 6.6e-7). So the block is a FORWARD-EULER / minimizing-movement step of a covariant diffusion with time step Delta t = h^2/d, and the Dirichlet energy is the energy that drives it. The claim's error is a pure order-of-limits error: it takes h -> 0 at FIXED phi, obtains a limit functional whose phi-dependence is a pure mass term, and reads the minimizer off the DEGENERATE limit. The true minimizer is phi*_h = (h/(2d))Delta^{(e),A}q^n -> 0 \u2014 consistent with the limit, but the limit has destroyed exactly the O(h) information that carries the dynamics. 'The gradient operator acts on the wrong field' is simply wrong: acting on q^n is what an EXPLICIT time discretisation requires."
}

### 6

{
  "attack": "NEW OBSTRUCTION the claim missed, and which its own Part I tool exposes: WHICH connection's Laplacian does the ELBO produce? The Euler-Lagrange operator of (1/2) INT ||D^A q||^2_{g^F} is the Levi-Civita (harmonic-map) Laplacian Delta^{(LC)}. I tested the ELBO's operator against the whole Amari alpha-family Gamma^{(alpha)} = Gamma^{(e)} + ((1-alpha)/2)T_AC.",
  "verdict": "KILLS_IT",
  "reasoning": "The ELBO's KL orientation (recognition in slot 1) forces alpha = +1 EXACTLY. Measured argmin vs (1/2)Delta^{(alpha)} at h=1e-4, two base points: forward block matches alpha=+1 to 5.8e-7 and 3.0e-6 while missing alpha=0 by 1.2 and 6.6 and alpha=-1 by 2.3 and 13 \u2014 and the alpha=0/-1 mismatches do NOT shrink with h. (Reverse orientation, shown for contrast, matches alpha=-1 to 4.4e-7 / 1.3e-6, the m-projection / moment average.) Therefore Delta^{(e),A} q = grad^{g^F} V is the ELBO's stationarity condition, whereas the Fisher-Dirichlet action's is Delta^{(LC),A} q = grad^{g^F} V, and Delta^{(LC)} = Delta^{(e)} + (1/2)(g^F)^{-1} T_AC(D_mu q, D_mu q). I verified this connection relation independently: the harmonic-map EL equation for the metric diag(1/sigma^2, 2/sigma^2) has Christoffels Gamma^mu_{mu sigma} = -1/sigma, Gamma^sigma_{mu mu} = 1/(2 sigma), Gamma^sigma_{sigma sigma} = -1/sigma, which reproduces Gamma^{(e)} + (1/2)T_AC exactly. CONSEQUENCE: the ELBO delivers the covariant Fisher-Dirichlet term as an ENERGY VALUE and as the generator of a covariant diffusion, but NOT as a variational principle \u2014 its stationary sections are e-harmonic, not critical points of the Fisher-Dirichlet action. This is the genuine residual obstruction. It is NOT repaired by the claim's (P2) (evaluation at q^{n+1}=q^n): it persists at every fixed point. Striking irony: the discrepancy is exactly (1/2)T_AC, the SAME Amari-Chentsov tensor the claim correctly isolates in \u00a73.2 as the KL-argument-order defect. The claim found the murder weapon in Part I and did not connect it to Part II."
}

### 7

{
  "attack": "VECTOR 2 (ORDER OF LIMITS) applied to (P2) as the claim frames it: 'the iterated limit lim_{h->0} lim_{n->inf} whose exchange is unproven', invoking Theory/07_general_renormalization.tex two-index non-commuting limits.",
  "verdict": "WEAKENS_SCOPE",
  "reasoning": "The citation is genuine \u2014 I read Theory/07_general_renormalization.tex:1064-1077, which does record 'Smooth-section support, continuum ELBO convergence, and connection convergence remain additional open obligations. status{OPEN}'. But the framing is wrong once the diffusion structure is exposed. n and h are not independent indices to be exchanged: they are COUPLED by the parabolic relation n ~ T d / h^2 that my step formula fixes. What survives h -> 0 with n h^2 -> T d is a FLOW on [0,T], not a static action, and the relevant open problem is consistency-plus-stability of an explicit Euler scheme (a Lax-equivalence question), not a limit exchange. Likewise the claim's (F) framing \u2014 m_h = ceil(d h^{-2}) is 'an extra declared h-dependent generative postulate ... nothing derives a replication multiplicity that grows like the inverse square of the lattice spacing' \u2014 is materially overstated: m_h = ceil(d h^{-2}) IS precisely Delta t = h^2/d, the unique parabolic scaling that gives a nondegenerate diffusive continuum limit. It remains a declaration, but a canonically forced one, not an arbitrary one. The claim's own \u00a76.2 (d=2 needs no weighting at all) already hints at this and it is correct: at d = 2, h^{d-2} = 1 and the raw unit-coefficient block converges to (1/4) INT ||D^A q||^2."
}

### 8

{
  "attack": "VECTOR 7 (SCOPE INFLATION) \u2014 does the stated theorem quantify over more than the proof delivers? Checked (C) and (D).",
  "verdict": "WEAKENS_SCOPE",
  "reasoning": "Three real over-quantifications, none fatal. (i) (C) says both limits 'are the connection-relative Fisher pullback h_q^omega ... integrated against Lebesgue measure'. h_q^omega (Theory/05c_pullback_geometry.tex:109-122) is a Sym^2 T*C tensor; the limit is its DELTA-TRACE against the declared Euclidean base cometric. (D) supplies the correction (G^{mu nu} = second moment of the edge measure) but (C) as displayed conflates a 2-tensor with a scalar. Relatedly, the exact finite-h gauge invariance is FIBRE-gauge only; the lattice functional is not invariant under base diffeomorphisms, since the base metric, lattice, and trace are all declared. (ii) (D)'s 'the h^3 coefficient ... vanishes iff that third moment vanishes' is true only when quantified over ALL sections; for a fixed section the contraction M_3^{mu nu rho} c_{3,mu nu rho} can vanish with M_3 != 0. (iii) 'centrally symmetric edge set' silently requires symmetric WEIGHTS w_k = w_{-k}, not just symmetric displacements. Separately, (C) is not new: PIFB2.tex:341 already states 'Omega_ij -> g_i Omega_ij g_j^{-1} and q_j -> rho(g_j)q_j so that ... the pairwise KL KL(q_i || Omega_ij q_j) becomes invariant by KL invariance under common pushforward'."
}

### 9

{
  "attack": "VECTOR 4 (NORMALIZATION) \u2014 hunt for a dropped log-normalizer, the single most common failure mode here. Checked: the m_h replication, the Gibbs envelope in (G), the Var_pi(E) expansions, and the \u00a75.7(i) smeared-kernel gap.",
  "verdict": "FAILS_TO_LAND",
  "reasoning": "No dropped normalizer. The m_h replication is legitimate and exactly licensed by boundary-counterexamples.md:52-59 ('Positive integer coefficients can be represented by repeated independent copies with tied recognition'), which I read; the product of m_h i.i.d. normalized label-copy factors with tied recognition gives KL = m_h [KL(beta||pi) + Sum beta_b KL(q||u_b)] exactly, INCLUDING the row-entropy term, and the claim correctly multiplies that term too. The overall h^d is a GLOBAL rescaling of the whole functional (uniform lattice), so it does not fall foul of boundary-counterexamples.md:61-66's site-dependent cell-weight prohibition \u2014 argmin is unchanged. The envelope algebra checks: -log Z = E-bar - (1/2)Var_pi(E) + O(E^3) and KL(beta*||pi) = (1/2)Var_pi(E) + O(E^3); I reproduced the claim's \u00a75.3 numbers to every quoted digit (1.334592e-05 vs 1.336111e-05; 8.348336e-07 vs 8.350694e-07; 5.218816e-08 vs 5.219184e-08; 3.261933e-09 vs 3.261990e-09), and Var_pi(E) = (h^4/4)Var_mu(g_mu) with pi uniform on 2d neighbours. \u00a75.7(i)'s 'gap is EXACTLY K/2' is also correct: E_y KL(q(c)||N(Omega y, C)) - KL(q(c)||N(Omega mu_{c'}, C)) = (1/2)tr(C^{-1} Omega Sigma_{c'} Omega^T) = K/2 when C = Omega Sigma_{c'} Omega^T. Item (G) stands as proved."
}

### 10

{
  "attack": "Attempt to break the (E) SCALING NO-GO \u2014 can the h^{-2} relative weight be obtained without replication? Tried: enlarging the source label set (spread beta over 2d*m_h labels); making the row non-uniform; tempering; a fixed prior-section source; a fixed reference field.",
  "verdict": "FAILS_TO_LAND",
  "reasoning": "(E) is correct and I could not break it. Enlarging the label set does not help: within ONE label-copy block Sum_b beta_b = 1, so Sum_b beta_b KL(q||u_b) <= max_b KL(q||u_b) = O(h^2) regardless of how the row is spread; the ratio gradient-sector : observation-sector is bounded by O(h^2) : 1. Tempering only rescales the entropy term, not the energies (and the claim's own \u00a75.3 shows tau is invisible at leading order anyway). So you genuinely need replication of the BLOCK, not of the labels. The only remaining escape is to make the likelihood itself h-dependent so that -E log ell = O(h^2), which is a postulate of the same weight as m_h. The claim's 'after ANY single global rescaling lambda_h ... the required relative weight is h^{-2} -> inf while beta_{c,c'} <= 1' is a correct strict no-go inside the stated theorem."
}

### 11

{
  "attack": "Attempt to break the (I) GENERAL NO-GO for Q-independent sources, and its stated consequence 'the Dirichlet integral of a genuinely free field is unreachable by ANY Q-independent source'.",
  "verdict": "WEAKENS_SCOPE",
  "reasoning": "The inequality itself is correct and elementary: if liminf min_{c'~c} KL(q(c)||u_{c,c'}) >= delta > 0 on S of positive measure, then h^{d-2} Sum_edges KL >= d delta |S| h^{-2} -> +inf. And the consequence \u2014 finiteness forces the source field to agree with the recognition section to O(h) in the Fisher metric \u2014 is right. But the reading 'kills it' does not follow. Agreement to O(h) between the current iterate and the lagged source is EXACTLY what a stable explicit time discretisation of a parabolic flow does; it is a CFL-type constraint, not a pathology. My step formula makes this quantitative: the exact stationary point has ||q^{n+1} - q^n||_{g^F} = O(h^2), comfortably inside the O(h) requirement. So (I) does not obstruct; it merely certifies the parabolic scaling. Its genuine force is narrower: it rules out sources at O(1) Fisher distance (fixed prior section, fixed reference field), which is a real and useful negative."
}

### 12

{
  "attack": "Full independent numerical reproduction of PART I (items 1-4) on the claim's exact instance: d=1 circle, N(mu,sigma^2) fibre, G = GL(1,R)_+ with rho-hat(g)N(mu,s^2) = N(g mu, g^2 s^2), zeta_a(mu,s) = (a mu, a s), mu(c)=0.3+0.4 sin 2 pi c, sigma(c)=1+0.3 cos 2 pi c, alpha(c)=0.5+0.6 sin 4 pi c, exact abelian holonomy exp(INT A).",
  "verdict": "FAILS_TO_LAND",
  "reasoning": "Every single quoted figure reproduces to all digits given. Target (1/2)INT||D^A q||^2_{g^F} dc = 4.529833403250 (claim: 4.529833403250). One-sided S1 at M = 64/256/1024/2048: 4.4755538671 / 4.5170074516 / 4.5266738865 / 4.5282575682 \u2014 identical to the claim's table. Symmetric S2: 4.5258130936 / 4.5295820712 / 4.5298176948 / 4.5298294761 \u2014 identical. err1/h -> -3.47389, -3.28344, -3.23535, -3.22731, Richardson -3.21927 (claim: -3.21927). err2/h^2 = -16.46719, -16.47129, -16.47155, -16.47160 (claim: -16.4716). Predicted O(h) coefficient: INT(1/2)g(v,w) = 4.392910, INT-(1/6)W(v,v,v) = -7.612181, sum -3.219270 \u2014 all three identical to the claim, agreeing with Richardson to six significant figures. INT d/dc[g(v,v)] over the circle = 7.7e-11 (a genuine total derivative), confirming the total-derivative cross-check. Theorem 4.1's O(h) / O(h^2) rates, the six H^1 failure modes, and the exact finite-h passive gauge covariance (KL invariance under a common bimeasurable pushforward, with Omega'_{c,c'} = rho-hat(g_c^{-1}) Omega_{c,c'} rho-hat(g_{c'})) all hold. I also re-verified the source citations I depend on: Theory/05c_pullback_geometry.tex:30-42, 59-63, 109-122, 124-144, 146-154, 172-182, 220-231, 509-538, 543-553, 556-570, 578-587, 1359-1366; exact-elbo-proof.md:60-118; boundary-counterexamples.md:52-59, 61-66, 68-73; lattice-continuum-asymptotics.md:11-22, 33-37; Theory/05b_local_collective_elbo.tex:347-362, 386-387; Theory/08_infogeometry.tex:238-247; PIFB2.tex:187, 316, 341, 434, 673, 678, 717-733. All check out. The grep is also right: Theory/*.tex contains NO lattice construction (only Banach lattice at 07b:1054,1104 and Boolean lattice at 07b:1191)."
}

### 13

{
  "attack": "Full independent numerical reproduction of the claim's (5.3) limit identity in \u00a75.4 \u2014 the displayed mathematical content of the DECISIVE NEGATIVE, as distinct from its interpretation.",
  "verdict": "FAILS_TO_LAND",
  "reasoning": "The IDENTITY is correct and I reproduce it exactly. With phi = (0.7 cos 2 pi c + 0.2, 0.45 sin 2 pi c - 0.15): frozen-Dirichlet INT||D^A q^n||^2 = 9.059667 (claim 9.059667), mass INT g^F(phi,phi) = 0.520011 (claim 0.520011), predicted limit 9.579677488 (claim 9.579677488). Lattice values at M = 64/256/1024/4096/16384: 9.541981604 / 9.571704669 / 9.577774925 / 9.579207511 / 9.579560348 \u2014 identical to the claim's quoted values, Theta(h) convergence. So h^d Sum_c m_h Sum_b beta_b KL(q^{n+1}(c) || (Omega^A)_# q^n(c')) -> (d/2)INT g^F(phi,phi) + (1/2)INT ||D^A q^n||^2 is PROVED. I attacked the identity and it holds. What fails is only the inference drawn from it \u2014 see the decisive attack above. Worth noting the claim is right on a smaller point the target got wrong: the target's displayed 'KL(q_i(c) || (Omega^A)_# q_i(c'))' does drop the time superscripts and hide a mixed-time object (boundary-counterexamples.md:68-73 and PIFB2.tex:678 both record the same-time obstruction), and \u00a75.7's two alternative routes (smeared-diagonal kernel; Gauss-Seidel sweep) are correctly refuted, the latter against Theory/05b_local_collective_elbo.tex:386-387."
}

