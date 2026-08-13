# panelA-ground-03-theory-corpus-sweep

*Recovered verbatim from workflow journal.jsonl, 2026-08-13. Agent aeffed50.*

## summary

Theory/ already contains a substantial, rigorously fenced exact coarse-graining apparatus, but NO spatial lattice, NO base-gradient term inside any free energy, and NO curvature term anywhere.

(A) Exact contraction/coarse-graining theorems. Law level: extended KL data processing with no absolute-continuity or finiteness hypothesis (06:65-72); DPI with sharp equality condition r(X)=r̄(Y) Q-a.s. under P≪Q and finite KL (06:85-105), plus pairwise Bayes recovery (06:124-129) and a counterexample showing infinite-KL equality gives no recovery (06:142-152). Fisher: I_Y ⪯ I_X with exact defect E Cov(ℓ|Y) under DQM plus a parameter-independent kernel normalized for every input, proved via Pollard's preservation theorem (06:170-224); equality is local score sufficiency only (06:243-253). ELBO: evidence-preserving channel monotonicity (06:258-302). Energy level: graph-exponential trace closure under the diagonal-affinity hypothesis, with the coarse normalizer explicitly not proved (06:368-404); Galerkin message-passing residual CH−H_cC=CH(I−PC) (06:437-446). Holonomy-conditioned marginal-law modes, path/root/gauge invariant (06:561-641). Kolmogorov projective extension with an explicit OPEN that it yields no continuum density, ELBO limit or RG flow (06:727-750). In 07b: the exact coarse VFE chain rule F_P(Q)=F_{P^c}(Q^c)+∫KL(conditional) (07b:34-57); the conditional-partition effective action e^{−H^c(z)}=∫e^{−H(y)}R_ρ(z,dy) (07b:112-127); real-analytic bounded action calculus with DQ=U, D²Q=−Cov (07b:190-227, 259-285); sup-norm nonexpansiveness ‖Q(φ)−Q(ψ)‖_∞≤‖φ−ψ‖_∞ (07b:309-313); L^p contraction with exact L² conditional-variance defect (07b:370-394); Dobrushin cocycle certificate (07b:434-514); exact Hoeffding/Möbius interaction isomorphism with sharp ‖H‖≤3^{|V|}−1 (07b:1224-1255); exact nonlinear interaction step with typed retained-projection residual and an exact-image-invariance iff (07b:1372-1508); exact hyperedge closure with an Ising-star witness against pairwise closure (07b:1530-1565). In 07: measure-pair arrow composition (07:111-137); typed base coarsening c_ℓ, κ_ℓ, P_ℓ(p·g)=P_ℓ(p)·κ_ℓ(g) with a genuine topological iff-existence condition and a Hopf-bundle failure witness (07:248-266); the descent biconditional q∘ρ̂_ℓ=ρ̂_{ℓ+1}(κ_ℓ)∘q (07:268-303). In 05c: sharp section descent (P1)⇔(P2)⇒(P3) (05c:715-751); covariant first-jet chain rule (05c:792-819); exact signed base Fisher comparison (05c:837-856); isotropy criterion (05c:921-972); ordered anomaly composition (05c:979-1032); Fisher-defect pullback contraction (05c:1115-1160); unconditional vertical defect cocycle (05c:1230-1257); base cocycle with exact residual and sharp criterion (05c:1267-1335). In 05d: exact averaging defect with three nonnegative terms (05d:1027-1075).

(B) Base-derivative sector: the object exists as a TENSOR but never as an energy. h_s^ω=(D^ω s)*g^F (05c:109-122) is exactly the gauged-sigma gradient density, and h^prod=w_b h_b+w_m h_m (05c:247-256) is the two-channel version; transported divergence equals ½ε²h_s^ω+O(ε³) (05c:556-570). Its integration is explicitly refused: a scalar gauged sigma energy needs a base cometric, base density, channel weights, boundary conditions, and a fixed/dynamical-connection decision, none selected (05c:1359-1366). Discrete Dirichlet forms DO exist on the agent graph: Σ(y_i−y_j)ᵀW_ij(y_i−y_j) (06_gaussian:111-117) and its gauge-covariant version Σ(z_i−Θ_e z_j)ᵀW_e(z_i−Θ_e z_j) (09:352-358), the latter with kernel = holonomy fixed space (09:379-399). Curvature: absent as a free-energy term everywhere.

(C) RG depth ℓ is a scale index in a thin category (07:14-42); the only spacing-like datum is a declared dimensionless block factor b>1 dividing betas by log b. No spatial spacing h exists anywhere.

(D) Fisher-as-KL-Hessian exists in mixed-jet form (05c:509-538) and exponential-family Hessian form (05a:138-148; 08:45-55).

## extracts

### 1

{
  "label": "Exact coarse VFE chain rule (the law-level coarse-graining identity)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/07b_agent_network_rg.tex:34-57",
  "statement": "thm:rg-exact-coarse-vfe: 'F_P(Q_o) = F_{P^c}(Q_o^c) + \u222b_Z KL( Q\u0302_o(dy|z) || \u03a0\u0302_o(dy|z) ) Q_o^c(dz)'. Hypotheses: P fixed normalized joint on standard-Borel spaces, o regular, Q_o \u226a \u03a0_o, C a fixed Markov kernel that 'does not read Q_o and does not alter the observation coordinate' (07b:24), extended-real sums with the common finite evidence term separated. Explicitly NOT covered (07b:68-73): different generative and recognition channels, a fitted rather than pushed-forward P^c, simultaneous coarse-graining of the observation.",
  "status_tag": "ESTABLISHED"
}

### 2

{
  "label": "Exact effective likelihood/action by conditional partition",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/07b_agent_network_rg.tex:112-127",
  "statement": "thm:rg-effective-action: 'exp[-H_o^c(z)] = \u222b exp[-H_o(y)] R_\u03c1(z,dy)' \u03c1^c-a.e., and 'Z(o) = \u222b exp[-H_o^c(z)] \u03c1^c(dz)'. R_\u03c1 is a reverse conditional of Y given Z under \u03c1(dy)C(y,dz). Staged and direct effective likelihoods agree a.e. when conditional versions come from the same joint tower. Convention e^{-\u221e}=0; equalities are a.e. statements (07b:91-94).",
  "status_tag": "ESTABLISHED"
}

### 3

{
  "label": "Extended KL data processing, no regularity hypotheses at all",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/06_general_coarsegraining.tex:65-72",
  "statement": "thm:cg-kl-dpi-extended: 'For arbitrary probability laws P,Q \u2208 P(X) and every Markov kernel K: X \u21dd Y, KL(PK||QK) \u2264 KL(P||Q) in [0,+\u221e]. No absolute-continuity or finiteness hypothesis is required.'",
  "status_tag": "ESTABLISHED"
}

### 4

{
  "label": "Fisher contraction is local: score projection and exact defect",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/06_general_coarsegraining.tex:170-224",
  "statement": "thm:cg-fisher-contraction: under DQM at \u03b80 with score in L\u00b2_0, and K a 'parameter-independent Markov kernel normalized for every input', the coarse family is DQM with score \u2113\u0304 = E[\u2113|\u03c3(Y)], and 'I_Y(\u03b80) \u2aaf I_X(\u03b80), I_X \u2212 I_Y = E Cov(\u2113_{\u03b80}(X)|Y) \u2ab0 0'. Equality exactly when the score is Y-measurable. Proof uses Pollard's Le Cam DQM decomposition and Pollard's preservation theorem for measurable statistics.",
  "status_tag": "ESTABLISHED"
}

### 5

{
  "label": "Fisher equality is not recovery (counterexample)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/06_general_coarsegraining.tex:243-253",
  "statement": "'Fisher equality at one parameter is local score sufficiency, not global recovery.' Bernoulli witness with Pr(A=1)=1/2+\u03b8/4, Pr(B=1)=1/2+\u03b8\u00b2/4, K discarding B: at \u03b8=0 fine and coarse Fisher agree and are nonzero, yet no parameter-independent reverse kernel recovers the experiment.",
  "status_tag": "ESTABLISHED"
}

### 6

{
  "label": "Graph-exponential trace closure under diagonal affinity",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/06_general_coarsegraining.tex:368-404",
  "statement": "thm:cg-graph-exponential-closure: under u(z,z)=\u03a5 t(z)+u_0 (eq:cg-diagonal-affinity, 06:359-363, status HYPOTHESIS), hard identification gives \u03b1_I = \u03a3_{i\u2208I}\u03b1_i + \u03a5* \u03a3_{{i,j}\u2286I} \u03b2_ij, \u03b2_IJ = \u03a3 \u03b2_ij, plus a constant c_P(\u03b8). 'The induced parameter map is linear. A normalized coarse law exists if and only if Z\u0304_P(\u03b8) < \u221e.' Proof note: 'The proof is algebraic and does not prove (eq:cg-coarse-normalizer).' Also 06:413-420: 'This theorem states conditional energy closure, not normalized-law closure.'",
  "status_tag": "ESTABLISHED (closure) / HYPOTHESIS (normalizer)"
}

### 7

{
  "label": "Base coarsening, group homomorphism, equivariance, and the topological iff with Hopf failure",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/07_general_renormalization.tex:248-266",
  "statement": "'Let c_\u2113: C_\u2113 \u2192 C_{\u2113+1} be smooth, let \u03ba_\u2113: G_\u2113 \u2192 G_{\u2113+1} be a Lie-group homomorphism, and let P_\u2113: \ud835\udcab_\u2113 \u2192 \ud835\udcab_{\u2113+1} cover c_\u2113 and obey P_\u2113(p\u00b7g) = P_\u2113(p)\u00b7\u03ba_\u2113(g).' 'Existence of such a map is a genuine topological condition on the declared data, not a normalization: an equivariant P_\u2113 over c_\u2113 exists if and only if the extended bundle \ud835\udcab_\u2113 \u00d7_{\u03ba_\u2113} G_{\u2113+1} is isomorphic to the pullback c_\u2113*\ud835\udcab_{\u2113+1} as a principal G_{\u2113+1}-bundle over C_\u2113. It can fail, for instance for the Hopf bundle over S\u00b2 against the trivial bundle with c_\u2113 the identity... every statement that uses P_\u2113 inherits it.'",
  "status_tag": "ESTABLISHED"
}

### 8

{
  "label": "Fiber-map descent biconditional to an associated scale map",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/07_general_renormalization.tex:268-303",
  "statement": "'q_{\u2113,s} \u2218 \u03c1\u0302_{\u2113,s}(g) = \u03c1\u0302_{\u2113+1,s}(\u03ba_\u2113(g)) \u2218 q_{\u2113,s}' holds iff q descends to C_{\u2113,s}[p,z]=[P_\u2113(p), q_{\u2113,s}(z)] covering c_\u2113. Degenerate caveat recorded: if B_{\u2113+1,s} reduces to a single G-fixed point the condition is vacuously true. Two further hypotheses are consumed at the information-geometric tier and 'neither follows from affinity of the law pushforward on the cone of measures': family closure of the underlying kernel, and smoothness of q_{\u2113,s} between the declared parametrized-measure models.",
  "status_tag": "ESTABLISHED"
}

### 9

{
  "label": "Sharp section descent (the coarse section descent hypothesis)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/05c_pullback_geometry.tex:715-751",
  "statement": "thm:pb-section-descent: for f a surjective smooth submersion and \u03a8 a bundle morphism over f, (P1) \u2203 Q\u0304 with \u03a8\u2218Q = Q\u0304\u2218f, (P2) \u03a8\u2218Q constant on each fiber of f, (P3) T^V\u03a8(D^\u03c9 Q(X)) + A_\u03a8(Q(c);X) = 0 for X \u2208 ker T_c f. '(P1) and (P2) are equivalent, both imply (P3), and (P3) implies (P2) when the fibers of f are connected.' Descended Q\u0304 is unique, automatically smooth and automatically a section. Submersion is load bearing: f(x)=x\u00b3 gives Q\u0304(y)=N(y^{1/3},1), continuous but not differentiable at 0. The descent hypothesis itself is eq:pb-coarse-related-sections at 05c:682-689, status HYPOTHESIS.",
  "status_tag": "ESTABLISHED"
}

### 10

{
  "label": "Fisher defect pullback and contraction (the composition-law section)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/05c_pullback_geometry.tex:1115-1160",
  "statement": "thm:pb-pullback-fisher-defect: 'Assume the preceding Markov hypotheses and D\u03a8 = 0 along s. Then \u0394_F^\u03a8 \u2ab0 0 and h_s^\u03c9 \u2212 f*h\u0304_{s\u0304}^{\u03c9\u0304} = (D^\u03c9 s)* \u0394_F^\u03a8 \u2ab0 0.' \u0394_F^\u03a8(u,u)=E Var(\u2113_u | Y). Markov hypotheses listed at 05c:1078-1104: pushforward of a parameter-independent Markov kernel normalized in the strong sense N(x,K\u0304)=1 for EVERY x, gauge-equivariant, plus family closure N_*(B)\u2286B\u0304, smoothness of q, coarse instantiation of hyp:pb-regular-models, and a common \u03c3-finite dominating measure for the DQM transfer.",
  "status_tag": "ESTABLISHED"
}

### 11

{
  "label": "Fisher defect cocycle and its non-additive base pullback",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/05c_pullback_geometry.tex:1230-1302",
  "statement": "thm:pb-fisher-defect-cocycle: '\u0394_F^{\u03a812\u2218\u03a801} = \u0394_F^{\u03a801} + (T^V\u03a801)* \u0394_F^{\u03a812}. This identity is unconditional: it uses neither the connections nor any section.' thm:pb-base-defect-cocycle: the base residual N = \u03b402 \u2212 \u03b401 \u2212 f01*\u03b412 has three exact forms; the sharp base cocycle holds 'if and only if \u0394_F^{\u03a812}(v_X,v_X) = \u0394_F^{\u03a812}(\u016b_X,\u016b_X) for every X', equivalently \u0394_F^{\u03a812}(A_X, 2v_X + A_X) = 0. Mixing conventions 'inflates the residual by exactly 2\u0394_F^{\u03a812}(A_X,A_Y)'.",
  "status_tag": "ESTABLISHED"
}

### 12

{
  "label": "Connection-relative Fisher pullback: the only base-derivative quadratic form in Theory/",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/05c_pullback_geometry.tex:109-122",
  "statement": "def:pb-informational-pullbacks: 'h_s^\u03c9(X,Y) = g^F_{s(c)}(D^\u03c9 s(X), D^\u03c9 s(Y))' and 'c_s^\u03c9(X,Y,Z) = T_{s(c)}(D^\u03c9 s X, D^\u03c9 s Y, D^\u03c9 s Z)', with D^\u03c9 s := ver^\u03c9 \u2218 Ts the connection-split covariant first jet (05c:98-107). 'The first is called a semimetric until its nondegeneracy is proved.' This is the gauged-sigma-model gradient density as a TENSOR on the base; it is never integrated into a scalar anywhere in Theory/.",
  "status_tag": "DEFINITION"
}

### 13

{
  "label": "Explicit refusal to build a gradient/sigma energy \u2014 the exact missing data",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/05c_pullback_geometry.tex:1359-1366",
  "statement": "'The chapter has constructed vertical tensors and their functorial defects. A scalar gauged sigma energy would additionally require a base cometric, a base density, channel weights, boundary conditions, and a decision about whether the connection is fixed or dynamical. None is selected by h_s^\u03c9 or c_s^\u03c9. \\status{NOT-CLAIMED}'",
  "status_tag": "NOT-CLAIMED"
}

### 14

{
  "label": "Two-channel weighted product geometry (belief + model gradient sectors)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/05c_pullback_geometry.tex:247-287",
  "statement": "hyp:pb-weighted-product-geometry: 'If one joint geometry is required, choose constants w_b, w_m > 0 and define h^prod = w_b h_{i,b}^{\u03c9_b} + w_m h_{i,m}^{\u03c9_m}. Unit weights are a specialization rather than a consequence of the common principal bundle.' Cross-scale integrated comparison needs (X1) f_#\u03bc = \u03bc\u0304 and (X2) w\u0304_x \u2218 f \u2264 w_x; independently declared coarse weights with w\u0304_x\u2218f > w_x 'break positivity even when every channel has zero horizontal defect and a genuine Markov fiber map'.",
  "status_tag": "HYPOTHESIS"
}

### 15

{
  "label": "Transported divergence is quadratic in the covariant base derivative",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/05c_pullback_geometry.tex:556-587",
  "statement": "cor:pb-transported-divergence-quadratic: 'D(s(c), \u015d_\u03b3(\u03b5)) = (\u03b5\u00b2/2) h^\u03c9_{s,D}(\u03b3\u0307(0),\u03b3\u0307(0)) + O(\u03b5\u00b3)', and for the regular KL contrast h^\u03c9_{s,D} = h_s^\u03c9. Caveat: 'The coefficient of \u03b5\u00b3 ... is not determined by c^\u03c9_{s,D} alone. It also contains the covariant acceleration of \u015d_\u03b3 and the connection coefficient selected by the one-sided divergence jet.'",
  "status_tag": "ESTABLISHED"
}

### 16

{
  "label": "Fisher metric as the mixed second jet of KL; Amari\u2013Chentsov as third-jet difference",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/05c_pullback_geometry.tex:509-538",
  "statement": "prop:pb-kl-divergence-jets: 'On a regular statistical model satisfying the integrability hypotheses of hyp:pb-regular-models, the mixed second jet of KL(p||q) is the Fisher metric, and the difference of the two mixed third jets is the Amari\u2013Chentsov tensor.' Proof computes \u2212\u2202_i\u2202'_j KL = E_\u03b8[\u2113_i\u2113_j], \u2212\u2202_i\u2202_j\u2202'_k KL = E[(\u2113_i\u2113_j+\u2202_i\u2113_j)\u2113_k], \u2212\u2202'_i\u2202'_j\u2202_k KL = E[\u2113_k \u2202_i\u2113_j], difference E[\u2113_i\u2113_j\u2113_k]. Hypotheses at 05c:30-42: DQM, positive-definite Fisher, third-power integrability of every score direction, domination sufficient to differentiate through third order.",
  "status_tag": "ESTABLISHED"
}

### 17

{
  "label": "Fisher as Hessian of the exponential-family potential; KL is Bregman, NOT a finite Fisher quadratic",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/05a_expfamily.tex:138-148,325-340",
  "statement": "prop:exp-cumulants-fisher: '\u2207A(\u03b8) = E_\u03b8[T], \u2207\u00b2A(\u03b8) = Cov_\u03b8(T). The Hessian is the Fisher information in the natural chart.' And eq:exp-kl-bregman: 'KL(Q_\u03d1||Q_\u03b8) = A(\u03b8) \u2212 A(\u03d1) \u2212 \u27e8\u2207A(\u03d1), \u03b8\u2212\u03d1\u27e9 = D_A(\u03b8,\u03d1)', with the explicit warning 'This is the exact exponential-family divergence; in general it is not a finite-displacement Fisher quadratic.' Same identity restated as g_\u03b7 = \u2207\u00b2_\u03b7 A(\u03b7) = Cov_q(T(Y)) at 08_infogeometry.tex:45-50 and g_\u03c4 = g_\u03b7^{-1} = Hessian of the conjugate at 08:51-55.",
  "status_tag": "ESTABLISHED"
}

### 18

{
  "label": "The one place where KL IS exactly a discrete gauge-Dirichlet term",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/08_infogeometry.tex:238-256",
  "statement": "'KL( N(\u03bc_i,C_ij) || N(\u03bc_j,C_ij) ) = \u00bd(\u03bc_i\u2212\u03bc_j)\u1d40 J_ij (\u03bc_i\u2212\u03bc_j) = \u00bd g^mean_{(\u03bc,C_ij)}(\u03bc_i\u2212\u03bc_j, \u03bc_i\u2212\u03bc_j). Thus pairwise KL is exactly one half of the associated mean-sector Fisher quadratic. Summing these typed edge quadratics defines the corresponding NK\u00d7NK connection-Laplacian energy; the assembled matrix L is not inserted into a single K-dimensional edge term. For a regular non-Gaussian family, freezing the Fisher tensor at one parallel base law gives the analogous form only as the local second-order term of transported KL. Outside these Gaussian or frozen-local hypotheses, a sample-space L is not a recognition Fisher tensor or a natural-gradient operator.'",
  "status_tag": "ESTABLISHED"
}

### 19

{
  "label": "Discrete gauge-covariant Dirichlet energy on the agent graph (connection Laplacian)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/09_coarsegraining.tex:352-358,379-399",
  "statement": "eq:cg-connection-laplacian-energy: 'z\u1d40 L_I z = \u03a3_{e=(i,j)\u2208E_I} (z_i \u2212 \u0398_e z_j)\u1d40 W_e (z_i \u2212 \u0398_e z_j)', hypotheses \u0398_e \u2208 GL(K), \u0398_\u0113 = \u0398_e^{-1}, W_e \u227b 0. prop:cg-kernel-holonomy: root evaluation is a linear isomorphism ker L_{I_\u03b1} \u2245 Fix(Hol_{r_\u03b1}), so dim ker L_I = \u03a3_\u03b1 dim Fix(Hol_{r_\u03b1}). The ungauged version is eq:gauss-interaction-energy at 06_gaussian.tex:111-117: 'y\u1d40\u039by = \u03a3_i y_i\u1d40 A_i y_i + \u03a3_{i<j}(y_i\u2212y_j)\u1d40 W_ij (y_i\u2212y_j)'. NOTE: these are quadratic forms on the LATENT SAMPLE space over the agent graph, not derivatives on the contextual base.",
  "status_tag": "DEFINITION / ESTABLISHED"
}

### 20

{
  "label": "RG depth is not inference time and not a spacing",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/05d_relational_inference.tex:1555-1599",
  "statement": "Section 'RG depth is not inference time': 'The integer \u2113 records RG depth. It is not a parameter on an inference history, and the sequence ... is not a temporal trajectory.' prop:hist-coordinate-independence: 'Scale depth \u2113, an orbit parameter r, and Fisher duration \u03c4^{(\u2113)} are distinct typed quantities: \u2113 is a discrete scale index, r is a chosen oriented parameter on a selected orbit, and \u03c4 is metric-relative arc length from a chosen origin.' Echoed at 07_general_renormalization.tex:52 ('the scale diagram itself introduces no time variable, and RG depth is not the intrinsic inference duration'), 10_renormalization.tex:417, 01_introduction.tex:117, appendix_notation.tex:526.",
  "status_tag": "ESTABLISHED"
}

### 21

{
  "label": "The only spacing-like datum is a declared dimensionless block factor b",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/07b_agent_network_rg.tex:2124-2168",
  "statement": "'Let b > 1 label one blocking ratio. A genuine RG step consists of a coarse channel C_b and a declared rescaling/identification kernel I_b that returns the target to a common measurable state space.' Discrete beta: 'B_b^H[H;\u03c1] = (R_b^H[H;\u03c1] \u2212 H) / log b.' Same log b normalization at 07_general_renormalization.tex:843-848 (\u03c5_a = log|\u03c1_a| / log b) and at 05c_pullback_geometry.tex:1210-1219 ('base diffeomorphisms i_\u2113: C_\u2113 \u2192 C_*, a block factor b_\u2113 > 1', B_{h,\u2113} = (h\u0303_{\u2113+1} \u2212 h\u0303_\u2113)/log b_\u2113). No length, mesh, or spacing h appears anywhere.",
  "status_tag": "ESTABLISHED / DEFINITION"
}

### 22

{
  "label": "Two-index (size n, depth \u2113) limits do not commute",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/07_general_renormalization.tex:862-1027",
  "statement": "'A finite-volume RG family has two indices X_{n,\u2113}, 0 \u2264 \u2113 \u2264 L(n), where n controls system size and \u2113 RG depth', with three distinct limits. prop:rg-noncommuting-limits proves fixed-depth thermodynamic and maximal-depth limits differ, using the exact Galerkin path-Laplacian quotient S_{m,b}\u1d40 L_m S_{m,b} = L_{m/b} and the arccos spectral count. Closing note: 'Proving an exchange of limits or a nontrivial diagonal limit remains open. \\status{OPEN}'",
  "status_tag": "ESTABLISHED (non-commutation) / OPEN (exchange)"
}

### 23

{
  "label": "Exact Hoeffding interaction coordinates and the product-reference premise",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/07b_agent_network_rg.tex:1224-1255,1160-1180",
  "statement": "thm:rg-hoeffding-action-isomorphism: E_\u2113 and H_\u2113 are bounded inverse linear isomorphisms between G_\u2113 (\u2113\u00b9 direct sum of all nonempty-hyperedge M\u00f6bius components) and the action quotient, with \u2016E_\u2113\u2016 \u2264 1 and \u2016H_\u2113\u2016 \u2264 3^{|V_\u2113|} \u2212 1, the latter sharp. Premise: \u03c0_\u2113 ~ \u03bd_\u2113 with \u03bd_\u2113 a PRODUCT reference at every admitted scale, and prop:rg-product-equivalence-not-preserved shows the diagonal-cloning channel destroys it: 'There is no product probability \u03bd_1 on {0,1}\u00b2 equivalent to \u03c0_1.'",
  "status_tag": "ESTABLISHED"
}

### 24

{
  "label": "Exact closure generates hyperedges; pairwise closure is false",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/07b_agent_network_rg.tex:1530-1565",
  "statement": "M\u00f6bius potentials \u03a6_A^c(z_A) = \u03a3_{B\u2286A}(\u22121)^{|A|\u2212|B|} H_o^c(z_B, z^\u2218_{B^c}) invert to H_o^c(z) = \u03a3_{A\u2286P} \u03a6_A^c(z_A): 'Thus the full hypergraph family is exactly closed.' And: 'Pairwise closure is false in general' \u2014 eliminating an Ising star centre gives \u2212log 2cosh(h_0 + \u03a3 J_r s_r) with cubic coefficient 2 sech\u00b2(h_0) tanh(h_0) J_1J_2J_3 + O(J\u2075), nonzero whenever h_0 J_1J_2J_3 \u2260 0.",
  "status_tag": "ESTABLISHED"
}

### 25

{
  "label": "Exact averaging defect over the base, and the convexity hypothesis that can fail",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/05d_relational_inference.tex:1018-1091",
  "statement": "thm:hist-averaging-defect: under hyp:hist-joint-convexity, \u0394_F^\u03a8 \u2ab0 0, weight condition w\u0304\u2218f \u2264 w, the defect \u0394_avg(Z) = \u222b_{C_\u2113} w g^F(Z,Z) d\u03bc \u2212 \u222b_{C_{\u2113+1}} w\u0304 \u1e21^F(TR Z, TR Z) d\u03bc\u0304 is nonnegative, and under (JC-const) splits into channel loss + weight gap + context gap, all nonnegative. Failure witness: 'the statement that averaging over the base loses information is false without it' \u2014 centered normal fiber in the moment chart gives \u0394_avg \u2192 \u22121/4, negative exactly for \u03b4 < \u221a2 \u2212 1.",
  "status_tag": "ESTABLISHED"
}

### 26

{
  "label": "Continuum limit is open everywhere it is mentioned",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/06_general_coarsegraining.tex:746-750",
  "statement": "'Consistency alone does not put the limit on continuous or smooth sections, define a continuum reference density, justify an ELBO limit, or produce an RG flow. Those conclusions require support regularity, compatible kernels and rescalings, convergence or uniform integrability of the functionals, and a declared topology. \\status{OPEN}'. Same obligation at 07_general_renormalization.tex:1064-1077, 03_probability.tex:443-444, and appendix_claim_ledger.tex:15-19 ('Continuum law theory (open)') and 80-92 ('Infinite-volume RG limit (open)').",
  "status_tag": "OPEN"
}


## gotchas

### 1

ABSENT — spatial lattice. Searched Theory/*.tex case-insensitively for 'lattice|mesh spacing|lattice spacing': the ONLY hits are 'Banach lattice' (07b:1054, 07b:1104, appendix_notation:396) and 'Boolean-lattice' Möbius projectors (07b:1191, appendix_notation:362). Also searched 'finite difference|finite-difference|spacing|discretiz|grid': ONE hit, 05b_local_collective_elbo.tex:368 ('finite-difference hypotheses permit the remaining subtraction'), plus 02_geometry.tex:26 which says the contextual base is 'a subset of C, not a continuum limit or a discretization theorem'. There is no h, no h^d, no volume element per site anywhere. Do NOT cite Theory/ for lattice regularization; it must be built from scratch.

### 2

ABSENT — gauge curvature / field strength. Searched 'plaquette|Wilson|Yang-Mills|F_A|field strength|structure equation|Bianchi|two-form|2-form|d\omega|curvature form' across Theory/*.tex: zero real hits (the single 'F_A' match, 09_coarsegraining.tex:486, is a fixed-section space F_A, unrelated). The word 'curvature' occurs 8 times total and EVERY occurrence is either (i) a disclaimer — 02_geometry.tex:397 'the connections ... are chosen data; no curvature or transport is inferred', 07b:996 'no gauge link, holonomy, or curvature datum enters the scalar theorem', 11_obstructions.tex:422 and 12_philosophy.tex:111,326 'not claimed to be evidence of base curvature or bundle topology' — or (ii) 'preconditioned curvature' meaning the Hessian eigenvalue of a quadratic ELBO (05_elbo.tex:629) and a normalizer second derivative label (11_obstructions.tex:150). There is NO curvature term in any free energy in Theory/.

### 3

ABSENT — Gamma-convergence / Dirichlet form. Searched 'Gamma-convergence|epi-conver': zero hits. Searched 'Dirichlet': all five hits are the Dirichlet DISTRIBUTION in the Gamma–Dirichlet bridge (10_renormalization.tex:473,492,495,505,623), not a Dirichlet energy or Dirichlet form. 'Sobolev' and 'elliptic' appear only as hypotheses declared missing (appendix_claim_ledger.tex:170,182; 05d:341,352,991).

### 4

The base-derivative object h_s^ω = (D^ω s)*g^F is CONNECTION-DEPENDENT, not canonical. 05c:220-231 exhibits N(0,1) constant section on trivial translation bundle over R: zero connection gives h = 0, connection A' = a_0 dx gives h^{A'} = a_0² dx². Any 'Dirichlet term' built from h_s^ω therefore carries the choice of ω as physical content, and 05c:146-154 warns that gauge invariance of h_s^ω is PASSIVE covariance only — an active bundle automorphism can carry h = 0 to dx².

### 5

Do NOT conflate the graph Laplacian energies with a base-derivative term. 06_gaussian.tex:111-117 and 09_coarsegraining.tex:352-358 give Σ(y_i−y_j)ᵀW_ij(y_i−y_j) and Σ(z_i−Θ_e z_j)ᵀW_e(z_i−Θ_e z_j) — these are quadratic forms on the LATENT SAMPLE SPACE indexed by the agent graph, not derivatives along the contextual base C. 08_infogeometry.tex:236 and 08:251-256 explicitly forbid the conflation: 'Outside these Gaussian or frozen-local hypotheses, a sample-space L is not a recognition Fisher tensor or a natural-gradient operator', and 08:230-234 lists the contextual base as a FOURTH space distinct from sample space, recognition parameter manifold, and model parameter space.

### 6

The Fisher pullback contraction h_s^ω − f*h̄ ⪰ 0 (thm:pb-pullback-fisher-defect) needs TWO independent guards, not one. (i) Vanishing horizontal defect DΨ = 0, which by thm:pb-isotropy-criterion (05c:921-949) means 𝔄_P(X) ∈ isotropy subalgebra of the coarse section value — strictly weaker than the principal identity P*ω̄ = dκ∘ω. (ii) Genuinely Markov, parameter-independent, equivariant fiber map plus family closure, smoothness of q, coarse regular-model instantiation, and a common dominating measure (05c:1078-1104). Drop guard (i) and positivity CAN FAIL: 05c:902-906 gives h_s^ω − f*h̄ = −a² dx² ≺ 0 at zero information loss. The correct unconditional statement is the signed identity h − f*h̄ = δ_Ψ − X_Ψ − Q_Ψ (05c:837-847), where X_Ψ is sign-indefinite and Q_Ψ ⪰ 0 both enter with MINUS signs.

### 7

The base-level Fisher-defect cocycle is NOT additive. The vertical cocycle (05c:1237-1242) is unconditional, but its base pullback carries the exact residual N of thm:pb-base-defect-cocycle (05c:1267-1302), and 05c:1284-1289 warns that mixing the ū-convention with the v-convention inflates the residual by exactly 2Δ_F^{Ψ12}(A_X,A_Y). Likewise horizontal defects compose by an ORDERED law A_{Ψ02} = T^VΨ12(A_{Ψ01}) + A_{Ψ12}(Ψ01(e); Tf01 X), and writing it as a plain sum is 'a type error before any question of correctness arises' (05c:1010-1014; same warning at 07:395-407).

### 8

Every theorem that uses the equivariant principal scale map P_ℓ inherits a topological existence obligation that can fail (07:258-266, Hopf bundle over S² against the trivial bundle with c_ℓ = id). A lattice-to-continuum program that assumes P_ℓ exists at every step is assuming something the manuscript flags as a genuine condition, not a normalization.

### 9

Fisher-as-Hessian-of-KL exists in Theory/ only in MIXED-jet form: −∂_i∂'_j KL(p_θ||p_η)|_{η=θ} = E_θ[ℓ_iℓ_j] (05c:509-538). The pure one-argument second derivative is not the theorem, and 05a:338-340 explicitly warns 'in general it is not a finite-displacement Fisher quadratic'. The ONE exact finite-displacement case is Gaussian with fixed common covariance in the mean submodel (08:242-247). Do not silently upgrade a local second-order expansion into a finite-difference identity.

### 10

Retained/truncated flows are not the exact flow. The exact interaction step T_ℓ^G is closed only under exact-image-invariance r^G_{ℓ+1}(g) = 0 on Ran R_ℓ (07b:1487-1494), and 07b:2318-2323 exhibits a retained beta reporting a line of fixed points while the exact step generates an omitted component. Also, exact closure generates hyperedges of ALL orders (07b:1532-1546) — a pairwise/2-body effective action is a truncation with a computable residual, not the effective theory (stated in the chapter preamble, 07b:8-11).

### 11

Beta functions in Theory/ are doubly scheme dependent: by smooth coupling reparameterization β'(g') = (1/c)Df(g)β(g) (07:830-833), AND by the moving cross-scale comparison frame — 07b:2325-2341 shows even the identity native step acquires β_ℓ(g) = (a_ℓ/a_{ℓ+1} − 1)g in a moving trivialization. Any exponent extracted from a lattice→continuum program must declare its comparison scheme.

### 12

Averaging over the base does NOT unconditionally lose information. thm:hist-averaging-defect requires hyp:hist-joint-convexity (05d:1018-1025), which 'holds in the location sector with fixed fiber covariance and in the law chart, and it fails in the covariance sector of the Gaussian moment chart'. The failure witness at 05d:1077-1091 has strictly negative defect tending to −1/4.

### 13

Do not treat the integral ∫_{C_ℓ} w g^F(∂_V s, ∂_V s) dμ (05d:265-271 configuration metric; 05d:711-718 continuum clock; 05d:1035-1042 averaging defect) as a Dirichlet energy. Its derivative ∂_V is in the CONFIGURATION direction (a tangent vector to section space), not in the base direction. It is an L² metric on section space. The genuinely base-derivative integrand would be h_s^ω, and no such integral appears anywhere in Theory/. Also 05d:725-731 flags that even this single-integral form presumes 'contextual locality' — if the recognition law couples s(c) and s(c'), the exact configuration metric carries a DOUBLE integral over C × C.

### 14

Sup-norm nonexpansiveness of the bounded action map (07b:309-317, ‖Q(φ)−Q(ψ)‖_∞ ≤ ‖φ−ψ‖_∞) means no relevant direction can arise in the bounded measure-pair action sector under isometric identifications. Growth must come from the extensive score-replication lift (07b:516-526) or the extensive interaction assembly. A continuum program that hopes to produce a relevant gradient operator inside the bounded action sector alone is blocked by this estimate.

### 15

'RG depth ℓ' and 'lattice spacing h' are NOT the same and cannot be silently identified. Theory/ types ℓ as a discrete index of a thin scale category (07:14-42) with declared comparison data (re-embeddings or reference isomorphisms, 07:45-61) and a declared dimensionless block factor b > 1; the base maps c_ℓ: C_ℓ → C_{ℓ+1} are just smooth maps with no metric contraction attached. Introducing h = h_0 b^{-ℓ} would be new declared data requiring a base metric that Theory/ never supplies (see the missing 'base cometric' in 05c:1362-1366).

