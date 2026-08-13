# panelA-T-SIMUL-derivation

*Recovered verbatim from workflow journal.jsonl, 2026-08-13. Agent a21c95b9.*

## target

T-SIMUL: settle the relationship between the LAGGED exact two-channel ELBO theorem (generative sources read q^n, recognition is q^{n+1}) and the SAME-TIME reciprocal coupling deployed in PIFB2/MAgent.

## status

PARTIAL

## theorem_statement

Let V be a finite agent set; for each i let X_i be an open subset of R^{d_i} and x_i |-> q_{x_i} a regular statistical model of densities on (W_i, nu_i) (H1-H4 below). Let Omega_ij = (T_ij)_# for fixed C^1 diffeomorphisms T_ij : W_j -> W_i with T_ji = T_ij^{-1}, independent of x. Put E_ij(x_i,x_j) = KL(q_{x_i} || Omega_ij q_{x_j}), define the two-slot functional

  Phi(x,y) = R(x) + sum_{i != j} beta_ij E_ij(x_i, y_j) + tau sum_{i != j} beta_ij log(beta_ij / pitilde_ij),

with R separable across agents, and set S := Phi o Delta (the deployed same-time PIFB2 scalar) and L(. | y) := Phi(., y) (the lagged, ELBO-exact scalar of the tied-replica theorem). Then:

(A) [DIAGONAL IDENTITY] S(x) = L(x | x) for EVERY x in X, not only at fixed points.

(B) [REACTION DECOMPOSITION] grad S = V^rec + R^react, where V^rec_i = grad_{x_i} R + sum_j beta_ij d_1 E_ij is the lagged (receiver-only) field and

  R^react_i(x) = sum_{l != i} beta_li d_2 E_li(x_l, x_i) = - b_i * E_{qbar_i}[ s_{x_i} ],
  b_i := sum_{l != i} beta_li,   qbar_i := (1/b_i) sum_l beta_li (Omega_il)_# q_{x_l},

s_{x_i} being the score of q_{x_i}. In an exponential family with sufficient statistic T_i, in NATURAL coordinates, R^react_i = b_i ( m_i - mbar_i ) where m_i = E_{q_i}[T_i] and mbar_i = E_{qbar_i}[T_i]. Hence R^react_i = 0 iff q_{x_i} is the M-projection (moment match) of the attention-weighted back-transported audience mixture qbar_i; in particular at exact transported consensus.

(C) [NON-BRIDGE / REFUTATION] With Euler step dt, the lagged scheme converges at rate O(dt) on compact time horizons to the ODE xdot = -V^rec(x), NOT to xdot = -grad S(x). The two limiting fields differ by R^react, which is O(1) in dt. Moreover V^rec is generically NOT the gradient of any C^2 potential: for three agents on a directed attention 3-cycle with beta = b > 0, unit self-precision a > 0 and mean-only Gaussian beliefs, the linearization of the lagged flow has eigenvalues -(a + 3b/2) +- i b sqrt(3)/2, complex for every b > 0, whereas every C^2 gradient flow linearizes to a symmetric matrix with real spectrum. Therefore "same-time PIFB2 is the dt -> 0 limit of the lagged ELBO-exact scheme" is FALSE.

(D) [POSITIVE SETTLEMENT] In the tied-replica inventory of the closed theorem, the belief and model label-copy blocks (J^q_a, X_a) and (J^s_a, Y_a) carry NO observation factor. Hence the marginal evidence of the generative joint is

  p^n(o) = prod_a integral p_a(dk) r_a(dm) L_a(o_a | k, m),

INDEPENDENT of the source laws u^n_{ab}, v^n_{ab}, hence of n and of any tie u_{ab} = (Omega_ab)_# q_b. Consequently the tied family {P_theta}_theta, theta := (q_b)_b, lies entirely on ONE level set of the log evidence e(theta) = log p_theta(o). By prop:gen-no-distinguished-target (Theory/04_generative.tex:130-157), and given 0 < p(o) < infinity, Q << P_theta(. | o) and the stated integrability, this yields the exact identity

  S(x) = - log p(o) + KL( Q_x || P_{theta = x}( . | o ) )   for every x,

so the deployed same-time PIFB2 scalar is a genuine upper bound on ONE FIXED number -log p(o) over the whole tied family, its descent is a genuine tightening of that bound, and its gradient flow is joint descent on the posterior-KL gap. The lagged theorem is exactly the E-step of this variational EM; R^react is exactly its M-step force.

(E) [SHARED-EQUILIBRIUM CHARACTERIZATION] Crit(S) = Fix(lagged) iff R^react vanishes on Crit(S) union Fix(lagged). The conjecture "the flows share equilibria iff the coupling is reciprocal-symmetric" is FALSE: under edge-symmetry (beta_ij E_ij(u,v) = beta_ji E_ji(v,u)) one gets R^react = V^{peer,rec} exactly, i.e. the peer force DOUBLES rather than vanishes, and the equilibria differ whenever the self force is nonzero. The correct nearby theorem is: edge-symmetry implies V^rec = grad( R + W/2 ), so the lagged flow is then potential descent on the HALF-COUPLED same-time functional.

## hypotheses

### 1

H1 (regular model). For each i, X_i subset R^{d_i} open; q_{x_i} > 0 nu_i-a.e.; (x,w) |-> q_x(w) is C^2 in x for nu_i-a.e. w, with local domination permitting two differentiations under the integral sign. This is Theory/05c_pullback_geometry.tex:30-42 hyp:pb-regular-models instantiated on each agent fiber.

### 2

H2 (frozen deterministic transport). Omega_ij = (T_ij)_# with T_ij : W_j -> W_i a fixed C^1 diffeomorphism, T_ji = T_ij^{-1}, INDEPENDENT of x. Justified operationally by PIFB2.tex:963 (eta_phi ~ eps^2 eta_q); if frames co-evolve, an extra frame-reaction term appears in grad S that is NOT covered here.

### 3

H3 (finiteness). E_ij(x_i,x_j) < infinity and q_{x_i} << Omega_ij q_{x_j} on the operating set; E_{Omega_il q_l} || s_{x_i} || < infinity for every active edge.

### 4

H4 (exactness of the Gaussian KL). All identities are stated at SPD floor eps = 0. PIFB2.tex:187 records that the implementation adds eps*I (KL_REGULARISER_EPS, default 1e-4) to the SECOND-argument covariance, so the deployed identities hold up to O(eps).

### 5

H5 (for D). Tied-replica inventory exactly as in the closed theorem: generative joint is a product over agents of (private block with likelihood) x (belief label-copy block) x (model label-copy block), with NO observation factor attached to either copy block; 0 < p(o) < infinity; Q^{n+1} << P^n(. | o), which requires beta_ab > 0 => pi_ab > 0 and q_a << u_ab (this CAN FAIL under hard supports, see boundary-counterexamples.md:74-79); the ELBO log-density terms integrable. These are exactly the hypotheses of prop:gen-no-distinguished-target, Theory/04_generative.tex:133-136.

### 6

H6 (for C). beta held fixed (or at beta* with the envelope substitution already made), one-sided Lipschitz vector fields on a compact invariant set for the Gronwall step, uniform mesh Euler discretization, lag depth L fixed or L*dt -> 0.

### 7

H7 (for E). Edge-symmetry beta_ij E_ij(u,v) = beta_ji E_ji(v,u) pointwise on X_i x X_j. For KL this needs forward = reverse divergence, which for Gaussians holds in the mean-only sector with a common covariance and ORTHOGONAL transports preserving it. It does NOT hold generically.

### 8

H8 (excluded). tau = 1, unit private coefficients, no alpha_i(c) precision sector, no base-gradient or curvature sector, no chi weighting asymmetry. These mismatches are independent of T-SIMUL and are NOT addressed here.


## derivation

========================================================================
0. WHAT I READ AND VERIFIED (all citations opened in this session)
========================================================================
- "C:/Users/chris and christine/Desktop/Research/manuscripts/PIFB2.tex" (3956 lines; the live copy). Read :59 (abstract), :522, :594, :733, :1329, :1441, :2430, :3270-3420, :3503, :3628.
- C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/05b_local_collective_elbo.tex:1-130, :330-783.
- C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/11_obstructions.tex:1-130.
- C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/04_generative.tex:95-174.
- C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-pifb2-fast-slow-program/evidence/transported-peer-derivations.md (full).
- CODE (read-only): "C:/Users/chris and christine/Desktop/MAgent_Model-main/gauge_agent/full_vfe.py":832-930, :1627-1722; gauge_agent/softmax_utils.py variational_attention_objective.
Numerical/symbolic verification scripts written to the session scratchpad only (/tmp/chk1..7.py); no repository file was created, edited or deleted.

========================================================================
1. SCOPING THE STANDING OBSTRUCTION (T-SIMUL.1)
========================================================================

1.1 The theorem, exactly. PIFB2.tex:3281-3308, Theorem "State-level mean-field ELBO obstruction" (thm:state_level_elbo_nogo). Hypotheses, verbatim-checked:
  (i) factors q_i in Q_i vary INDEPENDENTLY over a MIXTURE-OPEN family (defined at :3279: every zero-mass tangent h_i with h_i/q_i in L^inf(q_i) generates q_i + t h_i in Q_i for small |t|);
  (ii) at least one nonself beta_ij > 0, HELD FIXED;
  (iii) C(q) = F_rest(q) + sum_{a != b} beta_ab KL(q_a || T_ab q_b), with D^3_{q_i q_j q_j} F_rest = 0 for i != j;
  (iv) for one active edge (i,j) the tangent statistic g_ij := (T_ij h_j / T_ij q_j)^2 is bounded and NONCONSTANT q_i-a.e.
Conclusion: there is NO density p_theta on prod_i X_i, INDEPENDENT of q, and no constant c, with C(q) = KL( (x)_i q_i || p_theta ) + c throughout the open product family.

1.2 I re-derived the proof mechanism to confirm the scope is exactly as advertised.
For a fixed joint, KL((x)_i q_i || p) = sum_i integral q_i log q_i - integral (prod_i q_i) log p. The entropy is separable (each summand reads one factor) and the energy is MULTI-AFFINE (affine in each factor separately). Hence the mixed third variation D^3_{q_i q_j q_j} is identically zero: the entropy contributes nothing because no summand contains both q_i and q_j, and the energy contributes nothing because it is affine in q_j so its second q_j-variation vanishes. This is (eq:fixed_joint_third_variation_zero), :3308.
For the live peer term, with q_i(s) = q_i + s a_i and q_j(t) = q_j + t h_j, linearity of T_ij gives T_ij q_j(t) = T_ij q_j + t T_ij h_j, and
  d/ds d^2/dt^2 KL(q_i(s) || T_ij q_j(t)) |_{0} = d^2/dt^2 [ - integral a_i log(T_ij q_j(t)) ] |_0 = + integral a_i (T_ij h_j / T_ij q_j)^2 = integral a_i g_ij,
matching (eq:consensus_third_variation), :3312. Choosing a_i = q_i (g_ij - E_{q_i}[g_ij]) (zero mass; a_i/q_i in L^inf because g_ij is bounded) gives Var_{q_i}(g_ij) > 0. Contradiction. Verified.

1.3 THEREFORE what the obstruction does NOT forbid. Its two load-bearing hypotheses are (a) the ambient sample space is exactly prod_i X_i, the ORIGINAL agent-state variables, with no auxiliary coordinates; and (b) p_theta is q-INDEPENDENT. Any construction that breaks either is untouched. PIFB2's own scope remark (:3330-3332) lists: frozen source templates, restricted quadratic families, compatible auxiliary variables, a model selected after a fixed point, a probability law over belief configurations. It also warns (:3332) that if beta*(q) has been substituted, the reduced functional needs a SEPARATE representation test.

1.4 WHY THE TIED-REPLICA THEOREM COEXISTS WITH IT. Two independent reasons, both decisive on their own.
  (R1) DIFFERENT INVENTORY. The closed theorem's sample space is not prod_a X_a. It is prod_a [ (K_a, M_a) x (J^q_a, X_a) x (J^s_a, Y_a) ] - a private block plus TWO label-copy blocks per agent. Hypothesis (a) of the no-go fails by construction. The auxiliary copy blocks are exactly the "compatible auxiliary variables" that :3332 concedes are not excluded, and they are precisely what produces the categorical KL(beta_a || pi_a) block that a bare state-level joint cannot produce (this is 05b_local_collective_elbo.tex:487-600's latent-source-label mechanism, prop:obs-attention-elbo).
  (R2) LAGGED SOURCE. In the closed theorem u^n_{ab} = (Omega^n_{ab})_# q^n_b, and q^n belongs to the CONDITIONED HISTORY, not to the law being optimized at n+1. So the generative density is literally q^{n+1}-independent: hypothesis (b) of the no-go is satisfied, but its CONTRADICTION MECHANISM is void, because the third variation D^3_{q_i q_j q_j} of the lagged functional is identically zero for i != j - q_j^{n+1} does not appear in row i's peer term at all. There is nothing to contradict. This is the same observation the fast-slow run makes qualitatively at transported-peer-derivations.md:33-36 ("This is exact because q^n belongs to the conditioned history"); the third-variation reason is the quantitative version.
  Note the two reasons are complementary: (R2) alone rescues the peer KL; (R1) is additionally needed to obtain the attention entropy and to avoid the product-of-experts residue recorded as CE-2 in the exact run's counterexample-register.md:4-14.

1.5 A SEPARATE, WEAKER OBSTRUCTION I checked and set aside. 05b_local_collective_elbo.tex:422-485 ("Additive accounting is a different construction") is NOT the live-KL no-go. It is an exact COUNTING identity: eq:obs-singleton-incident-counting at :461-468 shows sum_{i in V} H_{{i},o} = sum_a |partial a| E_{a,o}, so summing singleton-local VFEs overcounts every shared record by its scope size. :477-478 states explicitly "This is a counting identity, not a universal no-go for arbitrary decompositions", and :480-485 says ordered chain rules or nonlocal counting shares can restore additivity. This bears on double-counting an undirected edge, not on same-time reciprocity. Similarly 11_obstructions.tex:88-90 fences its own no-go to "exactly the conjunction of the reciprocal-pair energy, no SPD anchor, and flat parallel-edge holonomy H = I", and :69-74 shows an SPD anchor restores definiteness. Neither is an obstruction to T-SIMUL.

========================================================================
2. THE TWO-SLOT FUNCTIONAL AND THE REACTION DECOMPOSITION (T-SIMUL.2)
========================================================================

2.1 Setup. Define, on X = prod_i X_i,
  Phi(x,y) = R(x) + sum_{i != j} beta_ij E_ij(x_i, y_j) + tau sum_{i != j} beta_ij log( beta_ij / pitilde_ij ),
with E_ij(u,v) = KL(q_u || Omega_ij q_v) and R(x) = sum_i [ KL(q_{x_i} || p_i) + ... - E[log l_i] ] separable. The entropy block is x-free at fixed beta. Then, EXACTLY:
  same-time PIFB2 scalar  S(x) = Phi(x,x)      = (Phi o Delta)(x),   Delta the diagonal embedding;
  lagged tied-replica scalar  L(x | x^n) = Phi(x, x^n).
The whole of T-SIMUL is the difference between RESTRICTING Phi to the diagonal and PARTIALLY EVALUATING Phi at a frozen second slot.

2.2 [DERIVATION] Value agreement (part A of the theorem). S(x) = Phi(x,x) = L(x | x^n) whenever x^n = x. Immediate. IMPORTANT DEFLATION: this holds at EVERY diagonal point, not merely at fixed points. The requested "at a fixed point the two actions take the same value" is therefore true but carries no information about stationarity, because value agreement on a submanifold constrains only the derivative ALONG that submanifold, never the derivative transverse to it. All the content of T-SIMUL is transverse.

2.3 [DERIVATION] Reaction decomposition (part B). Chain rule on Phi o Delta:
  grad_{x_i} S(x) = d_{x_i}^{(slot 1)} Phi(x,x) + d_{x_i}^{(slot 2)} Phi(x,x)
                  = [ grad_{x_i} R + sum_j beta_ij d_1 E_ij(x_i,x_j) ]  +  [ sum_{l != i} beta_li d_2 E_li(x_l, x_i) ]
                  =: V^rec_i(x)  +  R^react_i(x).
V^rec is precisely grad_x L(x | y) evaluated on the diagonal y = x - i.e. the lagged field. R^react is the back-reaction of agent i on every agent that LISTENS to i (i's audience), a slot the lagged scheme structurally never differentiates.
NUMERICAL VERIFICATION: N = 3 agents, K = 2, full Gaussian (mean and Cholesky-parameterized covariance), random GL transports, random asymmetric beta. Finite-difference check gave || grad S - (V^rec + R^react) ||_inf = 2.7e-9 with || grad S || = 19.8. Crucially, || R^react || = 12.6 against || V^rec || = 14.0: the reaction term is the SAME ORDER as the receiver term, not a perturbation.

2.4 [DERIVATION] CLOSED FORM OF THE REACTION TERM. Under H1-H3, write Omega_li = (T_li)_# so (Omega_li q_{x_i})(z) = q_{x_i}(T_li^{-1} z) |det DT_li|^{-1}. Then
  d_{x_i} KL(q_l || Omega_li q_{x_i}) = - integral q_l(z) d_{x_i} log q_{x_i}(T_li^{-1} z) dz
                                      = - integral (Omega_il q_l)(w) s_{x_i}(w) dw          [ w = T_li^{-1} z, Omega_il = Omega_li^{-1} ]
                                      = - E_{Omega_il q_l} [ s_{x_i} ],
where s_{x_i} = d_{x_i} log q_{x_i} is the score. The Jacobian factor is x_i-free and drops. Summing,
  R^react_i(x) = - sum_l beta_li E_{Omega_il q_l}[ s_{x_i} ] = - b_i E_{qbar_i}[ s_{x_i} ],   b_i = sum_l beta_li,  qbar_i = (1/b_i) sum_l beta_li Omega_il q_l.
Because E_{q_{x_i}}[ s_{x_i} ] = 0 identically, this is a pure DISCREPANCY:
  R^react_i(x) = - b_i integral ( qbar_i - q_{x_i} ) s_{x_i} .
INTERPRETATION: qbar_i is the attention-weighted mixture of i's AUDIENCE's beliefs, each pulled back into i's own frame. R^react is i's weighted maximum-likelihood score for fitting q_{x_i} to that pooled audience.
EXPONENTIAL FAMILY. If q_x(w) = exp( <x, T(w)> - A(x) ) then s_x = T - E_{q_x}[T], so IN NATURAL COORDINATES
  R^react_i = b_i ( m_i - mbar_i ),   m_i = E_{q_i}[T_i],   mbar_i = E_{qbar_i}[T_i].
So the reaction force is exactly a MOMENT MISMATCH between agent i and its pooled back-transported audience; the flow xdot = -grad S drives m_i -> mbar_i, i.e. an M-projection / barycenter step.
SYMBOLIC VERIFICATION (sympy, exact): for 1-D Gaussians with scalar transport a, both identities check to exactly 0: d E_21/d mu_1 + E_{Omega_12 q_2}[ d/d mu_1 log q_1 ] = 0 and d E_21/d v_1 + E_{Omega_12 q_2}[ d/d v_1 log q_1 ] = 0; and in natural coordinates (eta_1, eta_2) of the Gaussian, d E_21 / d eta_k - ( E_{q_1}[T_k] - E_{q_2}[T_k] ) = 0 for k = 1,2.
CROSS-CHECK AGAINST THE MANUSCRIPT: PIFB2.tex:1602 independently finds that the meta-agent barycenter "is therefore an exact M-step coordinate ... It is not, however, an E-step coordinate". The reaction term is the within-scale generalization of exactly that object. This is corroboration from an independent computation in the manuscript.

2.5 [DERIVATION] IS R^react A TOTAL DERIVATIVE? Since grad_{x_i} W = V^{peer,rec}_i + R^react_i where W(x) = sum_{i != j} beta_ij E_ij(x_i,x_j) is the full peer block, we have R^react = grad W - V^{peer,rec}. grad W is always closed, so R^react is a gradient field IFF V^{peer,rec} is. It is therefore NOT generically a total derivative: in the N = 3 Gaussian test the relative antisymmetry of the Jacobian of V^rec was 0.81 (against a symmetric-to-4e-5 Jacobian for grad S).
EXACT CLOSEDNESS CRITERION. Writing d_1, d_2 for the two slots, the Jacobian block condition for V^rec (equivalently R^react) to be closed on a simply connected domain is
  beta_ik d_2 d_1 E_ik (x_i, x_k)  =  [ beta_ki d_2 d_1 E_ki (x_k, x_i) ]^T   for every i != k.
This is EXACTLY the Monderer-Shapley exact-potential condition. APPLICABLE_THEOREM: Monderer and Shapley, "Potential Games", Games and Economic Behavior 14 (1996) 124-143, Theorem 4.5 - for a smooth game on a product of intervals with C^2 payoffs, an exact potential exists iff d^2 u_i / d x_i d x_j = d^2 u_j / d x_i d x_j for all i,j. Hypothesis check: our strategy sets X_i are open and we may restrict to a convex product neighborhood (convex, hence the theorem's product-of-intervals hypothesis holds coordinatewise); the costs J_i(x) = R_i(x_i) + sum_j beta_ij E_ij(x_i,x_j) are C^2 under H1-H3; the entropy block is x-free at fixed beta. So the theorem applies with u_i = -J_i. CONSEQUENCE: the LAGGED SCHEME IS BEST-RESPONSE / GRADIENT PLAY IN AN N-PLAYER GAME whose players are the agents; PIFB2's same-time S is the CANDIDATE POTENTIAL; and the game is an exact potential game precisely under the displayed condition.
In score form, the two sides of the condition are two cross-covariances taken under DIFFERENT reference measures:
  d_2 d_1 E_ik = - Cov_{q_i} ( s_{x_i}, sigma_k ),   d_2 d_1 E_ki = - Cov_{Omega_ik q_k} ( s_{x_i}, sigma_k ),   sigma_k(w) := s_{x_k}(Omega_ki w).
They coincide when q_i = Omega_ik q_k (transported consensus), where the condition collapses to beta_ik = beta_ki. So: AT A CONSENSUS CONFIGURATION, THE LAGGED FIELD IS CLOSED IFF THE ATTENTION MATRIX IS SYMMETRIC THERE (given a nondegenerate cross-covariance).

2.6 [COUNTEREXAMPLE] THE CONJECTURE "LAGGED AND SAME-TIME SHARE EQUILIBRIA IFF THE COUPLING IS RECIPROCAL-SYMMETRIC" IS FALSE.
Under edge-symmetry beta_li E_li(u,v) = beta_il E_il(v,u) (hypothesis H7),
  R^react_i = sum_l beta_li d_{x_i} E_li(x_l, x_i) = sum_l beta_il d_1 E_il(x_i, x_l) = V^{peer,rec}_i.
So the reaction term does NOT vanish - it EQUALS the receiver term. The peer force DOUBLES. Explicitly, with N = 2, K = 1, Omega = 1, common unit covariance, beta_12 = beta_21 = b, self term (a/2)(mu_i - m_i)^2 and m = (1,0):
  lagged equilibrium (a=b=1):  mu* = (2/3, 1/3);   same-time equilibrium: mu* = (3/5, 2/5).
They differ. Verified numerically at b = 0.5, 1.0, 2.0 (lagged at coupling b coincides with same-time at coupling b/2 in every case, which is exactly the halving statement below). So reciprocal symmetry is neither necessary nor sufficient for shared equilibria.
THE CORRECT NEARBY THEOREM (part E). Under edge-symmetry, V^rec = grad( R + W/2 ). Hence the lagged flow IS potential descent - on the HALF-COUPLED same-time functional. VERIFIED: N = 4, K = 3, mean-only Gaussians, orthogonal Regime-I coboundary transports Omega_ij = U_i U_j^T, symmetric beta: || V^rec - (1/2) grad W ||_inf = 8.9e-10.
NECESSARY CAVEAT ON edge-symmetry UNDER LIVE SOFTMAX. beta*_ij = pi_ij exp(-E_ij/tau) / Z_i. With E symmetric and pi symmetric, M := pi exp(-E/tau) is symmetric and beta* = D^{-1} M with D = diag(Z). Then beta* is symmetric iff Z_i = Z_j on every connected component of the support graph, i.e. iff beta* is doubly stochastic. THIS GENERICALLY FAILS. VERIFIED: N = 4, K = 3, exactly symmetric E and uniform pi, tau = 0.7 gave Z = (0.2223, 0.3210, 0.0458, 0.2817) and max | beta* - (beta*)^T | = 0.547. So the halving repair is available for FROZEN symmetric beta and is destroyed by the softmax row normalization. This is a real and previously unrecorded obstruction.
TRUE CHARACTERIZATION OF SHARED EQUILIBRIA. Fix(lagged) = { V^rec = 0 }, Crit(S) = { V^rec + R^react = 0 }. Therefore Crit(S) intersect Fix(lagged) = { V^rec = 0 and R^react = 0 }, and the two sets are equal iff R^react vanishes on their union. By 2.4, R^react_i = 0 iff q_{x_i} moment-matches its pooled back-transported audience qbar_i - in an exponential family, iff m_i = mbar_i. The clean sufficient condition is transported consensus q_l = Omega_li q_{x_i} on every active in-edge, where R^react = 0 by the zero-mean-score identity.

========================================================================
3. INTEGRABILITY OF THE SAME-TIME FIELD (T-SIMUL.3)
========================================================================

3.1 [DERIVATION] PIFB2's abstract claim (:59: "The checked-in multi-agent implementation differentiates this scalar total, so its active update is potential descent rather than a nonintegrable softmax-response field") is MATHEMATICALLY CORRECT AND ESSENTIALLY TRIVIAL. If the code assembles an explicit C^2 scalar T(x) and calls autodiff, the field is grad T and its Jacobian is Hess T, symmetric by Schwarz/Clairaut. There is no theorem to prove. The manuscript already says this at :1441 ("In both cases the full receiver-plus-sender Hessian is symmetric") and :733.

3.2 [DERIVATION] EXPLICIT HESSIAN OF THE ENVELOPE-REDUCED SCALAR (the requested Jacobian computation). With T(x) = -tau sum_i log Z_i(x), Z_i = sum_j pitilde_ij exp( -E_ij(x)/tau ):
  grad T = sum_{i,j} beta*_ij grad E_ij                      (envelope; beta*_ij = pitilde_ij e^{-E_ij/tau} / Z_i)
  Hess T = sum_{i,j} beta*_ij Hess E_ij  -  (1/tau) sum_i Cov_{beta*_i} ( grad E_{i.} , grad E_{i.} ).
Derivation of the second term: d_{x_m} beta*_ij = -(1/tau) beta*_ij ( d_{x_m} E_ij - sum_l beta*_il d_{x_m} E_il ), so sum_{ij} (d_{x_m} beta*_ij) d_{x_k} E_ij = -(1/tau) sum_i Cov_{beta*_i}( d_{x_m} E_{i.}, d_{x_k} E_{i.} ). BOTH TERMS ARE MANIFESTLY SYMMETRIC in (m,k), and the softmax-response term is a nonnegative-definite covariance entering with a MINUS sign - the attention response uniformly REDUCES curvature by an amount scaling as 1/tau.
VERIFIED numerically (N=3, K=2, mean-only, orthogonal transports, tau=0.6): || Hess_numeric - [ sum beta* Hess E - (1/tau) sum_i Cov ] ||_inf = 8.8e-5 against a Hessian of scale 2.0 (finite-difference noise); and min eig of the covariance block = -3.4e-17, i.e. PSD to machine precision.

3.3 [CODE VERIFICATION, EVIDENCE_VERIFIED] THE SHARP CONTENT OF THE ABSTRACT'S CLAIM IS "NO detach ON THE SENDER". I read the deployed path. In "C:/Users/chris and christine/Desktop/MAgent_Model-main/gauge_agent/full_vfe.py", belief_alignment (:836-918) calls E = self._compute_pairwise_kl(mu_q, sigma_q, system, transport_fn) at :857, and inside _compute_pairwise_kl (:1627-1722) the SENDER tensors are

    mu_j    = mu.unsqueeze(0).expand(N, -1, *mu.shape[1:])
    sigma_j = sigma.unsqueeze(0).expand(N, -1, *sigma.shape[1:])
    mu_t    = transport_mean(transport, mu_j);  sigma_t = transport_covariance(transport, sigma_j)
    E = self._divergence(mu_i, sigma_i, mu_t, sigma_t)

with NO .detach() anywhere on mu_j / sigma_j / mu_t / sigma_t on any of the three branches (transport_fn provider, single-shot vertex-local, chunked). The .detach() calls at :918 apply only to the returned diagnostics beta and E, not to the differentiated scalar weighted.sum(). CONCLUSION: the deployed field really is V^rec + R^react. The code is same-time in the STRONG sense (both slots differentiated), so it is NOT the lagged scheme even in the small-step limit. The abstract's claim is code-verified.
COROLLARY WORTH RECORDING: "detach the sender" and "lag the sender" are the SAME operation computationally. Any implementation that detaches peers for stability silently switches from the integrable same-time field to the generically nonintegrable lagged field.

3.4 [SYNTHESIS - the inversion] PIFB2 disavows the receiver-only field V^rec at :2430 ("This field is not the gradient of S_surr and is generically nonintegrable"), :3400-3407 ("an optional update approximation") and :1441 ("A nonpotential running rule appears only after the additional receiver-only truncation"). What the manuscript does NOT say, and what section 5 below proves, is that V^rec IS EXACTLY THE CONTINUUM-TIME FIELD OF THE LAGGED, ELBO-EXACT SCHEME. So the field the manuscript disavows on integrability grounds is the ELBO-derived one, and the field it deploys is the one that is NOT the gradient-of-a-lagged-ELBO. Integrability and lagged-ELBO-exactness pull in opposite directions. This is the central previously-unrecorded tension in the program, and section 6 resolves it.

========================================================================
4. THE LAG AS A DISCRETIZATION - REFUTED AS STATED (T-SIMUL.4)
========================================================================

4.1 [DERIVATION, TRUE] The VALUE gap is O(dt). Along any C^1 trajectory with bounded velocity, on a set where d_2 E is locally bounded,
  L( x(t) | x(t - dt) ) - S( x(t) ) = - dt sum_{i != j} beta_ij d_2 E_ij( x_i(t), x_j(t) ) . xdot_j(t) + O(dt^2).
So the two SCALARS differ by O(dt). This is the whole of the intuition behind item 4, and it is correct.

4.2 [REFUTATION] The FLOW gap is O(1), and the continuum limits are DIFFERENT ODEs. The error in the intuition is a slot error, not a magnitude error. When one differentiates the lagged functional with respect to x_i, one does NOT differentiate through x_j(t - dt), because that is conditioned history - that is the entire content of the lag and the entire reason the tied-replica theorem is exact (transported-peer-derivations.md:33-36). The missing object R^react_i = sum_l beta_li d_2 E_li is a derivative WITH RESPECT TO A DIFFERENT SLOT, and it carries no factor of dt. Sending dt -> 0 perturbs the point at which d_1 is evaluated by O(dt); it never restores d_2. Formally: with Euler step dt and lag depth L (fixed, or L dt -> 0),
  x^{n+1} = x^n - dt grad_1 Phi( x^n, x^{n-L} )   -->   xdot = - grad_1 Phi(x,x) = - V^rec(x),
whereas the same-time scheme gives xdot = - grad( Phi o Delta )(x) = - ( V^rec + R^react )(x).

4.3 [COUNTEREXAMPLE, decisive] THE LAGGED CONTINUUM FLOW IS NOT A GRADIENT FLOW OF ANY C^2 POTENTIAL. Take N = 3, K = 1, mean-only unit-variance Gaussians, Omega = 1, DIRECTED attention 3-cycle beta_{12} = beta_{23} = beta_{31} = b > 0 (all other beta zero), self term (a/2)(mu_i - m_i)^2. Then with P the cyclic permutation:
  lagged field Jacobian    J_lag = a I + b ( I - P ),
  same-time field Jacobian J_sim = a I + b ( 2I - P - P^T )   (the undirected triangle graph Laplacian).
Spectra: eig(-J_lag) = { -a - 3b/2 +- i b sqrt(3)/2, -a } - COMPLEX for every b > 0; eig(-J_sim) = { -a, -a - 3b, -a - 3b } - real. VERIFIED numerically at a = b = 1: lagged spectrum {-2.5 +- 0.866i, -1}, same-time spectrum {-4, -4, -1}.
Every gradient flow xdot = -grad f with f in C^2 linearizes to -Hess f, a SYMMETRIC matrix, whose spectrum is REAL. Therefore the lagged continuum flow is not the gradient flow of any C^2 potential near that point, a fortiori not of S. QED.
This is a genuine dynamical separation, not a bookkeeping one: the lagged flow SPIRALS into consensus, the same-time flow does not.

4.4 [NUMERICAL CONFIRMATION] Same system with a = b = 1, m = (1,0,0), x0 = (0.3,-0.8,0.5), horizon T = 3:
  dt        | lagged Euler - lagged ODE |    | lagged Euler - same-time Euler |
  0.100         4.95e-3                           1.3410e-1
  0.050         2.33e-3                           1.3354e-1
  0.020         8.99e-4                           1.3329e-1
  0.010         4.44e-4                           1.3323e-1
  0.005         2.21e-4                           1.3320e-1
  0.002         8.79e-5                           1.3318e-1
The lagged scheme converges to ITS OWN limit ODE at first order in dt (Gronwall behaves exactly as expected under H6). The gap to the same-time scheme is FROZEN at 0.1332 and does not shrink. The equilibria also differ: lagged mu* = (0.5714, 0.1429, 0.2857) versus same-time mu* = (0.5, 0.25, 0.25), and R^react at the lagged equilibrium is (0.2857, -0.4286, 0.1429), nonzero.

4.5 VERDICT ON ITEM 4. The proposed bridge is REFUTED. "Same-time PIFB2 is the dt -> 0 limit of an exactly-ELBO-derived lagged scheme" is FALSE, for any Lipschitz hypotheses whatsoever: Lipschitzness is exactly what makes the lagged scheme converge cleanly to the WRONG limit. The only surviving true statements are (4.1) the O(dt) value gap, (4.2/4.4) the O(dt) convergence of the lagged scheme to xdot = -V^rec, and the conditional repair of 2.6: under edge-symmetry with FROZEN symmetric beta, V^rec = grad(R + W/2), so the lagged limit is the same-time flow WITH EVERY PEER COEFFICIENT HALVED - a factor-2 coefficient discrepancy, not an identity, and unavailable under live softmax because the row normalizers break beta symmetry.

========================================================================
5. THE POSITIVE SETTLEMENT: EVIDENCE INVARIANCE OF THE COPY BLOCKS
========================================================================

Item 4's bridge fails, but a stronger and honest bridge exists, and it is a genuine theorem.

5.1 [DERIVATION] LEMMA (evidence invariance). In the tied-replica inventory the generative joint is
  P^n(dk, dm, dj^q, dx, dj^s, dy, do) = prod_a [ p_a(dk_a) r_a(dm_a) L_a(do_a | k_a, m_a) ] . [ pi^q_{a j^q} u^n_{a j^q}(dx_a) ] . [ pi^s_{a j^s} v^n_{a j^s}(dy_a) ].
Neither copy block carries an observation factor. Integrating the latent coordinates at fixed o,
  p^n(o) = prod_a [ integral p_a(dk) r_a(dm) L_a(o_a | k,m) ] . [ sum_j pi^q_{aj} integral u^n_{aj}(dx) ] . [ sum_l pi^s_{al} integral v^n_{al}(dy) ]
         = prod_a integral p_a(dk) r_a(dm) L_a(o_a | k,m) . 1 . 1,
because the pi rows are probability vectors and every u, v is a probability measure. Hence p^n(o) DOES NOT DEPEND ON u^n, v^n - hence not on n, and not on any tie u_ab = (Omega_ab)_# q_b. Status: DERIVATION, and it is a two-line integration that anyone can check.

5.2 [APPLICABLE_THEOREM] Declare theta := (q_b)_b as a GENERATIVE parameter, so u_ab := (Omega_ab)_# q_{theta_b}. For each fixed theta, P_theta is a normalized joint that does not read the recognition law Q - req:gen-typing-prohibition (Theory/04_generative.tex:120-124) is satisfied. The TIE theta_i = x_i is a constraint on the optimization, not a violation of the model's typing; but it does make {P_theta} a Q-indexed family, so prop:gen-no-distinguished-target (04:130-157) governs. Its hypotheses (04:133-136) are H5. Its conclusion (04:137-142) is the exact identity log p_theta(o) = ELBO(Q) + KL(Q || P_theta(. | o)), and its sharp criterion (04:156-157) is: "a divergence decrease certifies improvement relative to one fixed reference value exactly when the two members lie on one level set of e", e(theta) = log p_theta(o).
BY 5.1, e IS CONSTANT ON THE ENTIRE TIED FAMILY. The criterion is satisfied for every pair of members, unconditionally. Therefore
  S(x) = - log p(o) + KL( Q_x || P_{theta=x}( . | o ) )   for every x in X,
with -log p(o) = - sum_a log integral p_a r_a L_a(o_a | . ) ONE FIXED NUMBER.

5.3 [THEOREM, the settlement] Consequently:
  (i) The deployed same-time PIFB2 scalar is a valid UPPER BOUND on a single fixed negative log evidence, uniformly over the whole tied family. It is not merely "an engineered consensus energy".
  (ii) Descent on S is a genuine tightening of the bound gap KL(Q_x || P_x(. | o)); nothing moves underneath it.
  (iii) THE LAGGED THEOREM IS THE E-STEP of this variational EM (differentiate S in the recognition slot: V^rec), AND THE REACTION TERM IS ITS M-STEP FORCE (differentiate in the generative-parameter slot: R^react). Section 2.4's closed form R^react_i = b_i (m_i - mbar_i) is exactly a weighted-maximum-likelihood score equation, and its zero is the M-projection of the pooled back-transported audience - which is why PIFB2.tex:1602 independently found the meta-agent barycenter to be "an exact M-step coordinate".
  (iv) TIGHTNESS. The copy blocks carry no likelihood, so their posterior equals their prior: P_theta(J^q_a = j, X_a in dx | o) = pi^q_{aj} u_{aj}(dx), against recognition beta_aj q_a(dx). The bound is attained iff beta_a = pi^q_a, gamma_a = pi^s_a, q_a = u_{ab} and s_a = v_{ab} on every source with positive prior (total transported consensus with untilted attention), and the private block is exact. This is EXACTLY the locus where R^react = 0 (section 2.4) - the two conditions agree, which is a nontrivial internal consistency check.
  (v) NO CONFLICT WITH THE NO-GO. thm:state_level_elbo_nogo requires (a) sample space prod_i X_i with no auxiliaries and (b) p_theta q-independent. The construction violates BOTH: the space carries the copy blocks, and P_theta moves with theta. The price of (b) is precisely that the evidence could move; Lemma 5.1 pays it by showing the evidence does NOT move. Nothing is cheated.

5.4 SCOPE OF 5.3. This settles the STATUS of the same-time functional and the ROLE of the lagged theorem inside it. It does NOT deliver: tau != 1 (the exact mismatch remains (tau - 1) KL(beta || pi), boundary-counterexamples.md:46-51), nonunit private coefficients or the live alpha_i*(c) path (PIFB2:784), the m_i typing of the observation term (:669 vs :689), the base-gradient and curvature sectors (absent from the finite theorem), or the continuum limit. Those are independent of T-SIMUL.

========================================================================
6. THE SANOV / EMPIRICAL-MEASURE ROUTE (T-SIMUL.5) - ONE PARAGRAPH
========================================================================
Credible but it delivers the LAGGED action, not the same-time one, so it does not settle T-SIMUL. Read q_i as the empirical measure of M microscopic messages held by agent i. Sanov gives, for finite alphabet by the method of types, the exact statement that CONDITIONALLY on agent j's realized empirical measure q_j, if i's messages are drawn i.i.d. from Omega_ij q_j then Pr( L^{(i)}_M in B_delta(q_i) | L^{(j)}_M = q_j ) = exp( -M KL(q_i || Omega_ij q_j) + O(log M) ). That is exactly the tied-replica peer energy - and it is LAGGED by construction, because the conditioning fixes j's measure before i's is drawn. Two agents drawing from each other SIMULTANEOUSLY is not a conditional Sanov statement at all; it is a mean-field Gibbs measure, whose LDP rate is the free energy of the interacting system and which requires an independently specified microscopic law (Dawson-Gartner / McKean-Vlasov type). Positing P proportional to exp(-S_PIFB) to get it back is exactly CE-2 of the fast-slow run (counterexample-register.md:4-12): insertion, not derivation. So the honest first theorem of this programme is a QUENCHED FINITE-M SANOV THEOREM WITH TRANSPORTED REFERENCE: on a finite alphabet of size A, uniformly over (q_i, q_j) in a compact subset of the interior of the simplex product and over the declared transports,
  -(1/M) log Pr( L^{(i)}_M = q_i | L^{(j)}_M = q_j ) = KL( q_i || Omega_ij q_j ) + ((A-1)/(2M)) log M + (1/M) c(q_i) + o(1/M),
with c the explicit Stirling/Fisher-determinant constant. That is provable today by the method of types plus a uniform Stirling expansion; it would give the first quantitative finite-sample correction to the peer block, of size O(log M / M), and it would confirm the peer energy as an extensive rate rather than an ansatz. It would NOT produce same-time reciprocity, and it must not be advertised as doing so. The prior runs already register this route at disposition "open" with zero verified results (fast-slow approach-registry.json:49-61; exact-run approach-registry.json:76-91), and my assessment is that it should be re-scoped from "route to same-time coupling" to "route to a finite-M correction of the lagged coupling", where it is genuinely tractable.

========================================================================
7. WHAT T-SIMUL NOW IS
========================================================================
The relationship is NOT "same-time is the continuum limit of lagged" (refuted, 4.3-4.4). It is:
  SAME-TIME PIFB2  =  TIED VARIATIONAL EM on the tied-replica family, differentiating both the recognition slot and the generative-parameter slot of one scalar;
  LAGGED THEOREM   =  its E-step, exact at frozen theta;
  DIFFERENCE       =  the M-step force R^react_i = b_i ( m_i - mbar_i ), an audience-moment mismatch, O(1) and computable in closed form;
  BOUND STATUS     =  valid, because the auxiliary copy blocks carry no likelihood, so the evidence is invariant along the tie (Lemma 5.1) and prop:gen-no-distinguished-target's level-set criterion is met unconditionally.
That is defensible, checkable, and strictly stronger than "we guessed the term". It is also strictly weaker than "the deployed action is an exact ELBO of one fixed joint on the agent states" - which remains false, by thm:state_level_elbo_nogo, for the reasons that theorem actually gives.

## obstructions

### 1

The tie theta_i = x_i makes {P_theta} a Q-indexed family, so the same-time functional is an ELBO of a MOVING generative law. Lemma 5.1 removes the sting (the evidence is constant along the tie), but it does NOT make P_theta q-independent, so thm:state_level_elbo_nogo (PIFB2.tex:3281) still correctly forbids the strong reading. The settlement is 'valid bound on a fixed number via a moving model', not 'exact ELBO of one fixed joint'.

### 2

Lemma 5.1 requires Q << P_theta(.|o), i.e. beta_ab > 0 => pi_ab > 0 AND q_a << u_ab. Under hard supports the peer KL can be +infinity and masks must be applied by RESTRICTING THE SOURCE SET before the KL is formed (exact run, boundary-counterexamples.md:74-79). PIFB2's chi_i are smooth bumps (:711), which helps, but the absolute-continuity condition is not automatic and I did not verify it for the deployed configuration.

### 3

The halving repair (V^rec = grad(R + W/2)) needs edge-symmetry beta_ij E_ij(u,v) = beta_ji E_ji(v,u). For KL this demands forward = reverse divergence, true for Gaussians only in the mean-only sector with a common covariance and covariance-preserving (orthogonal) transports. PIFB2 deploys GL(K_q) transports on full covariances (:434), so edge-symmetry FAILS on the deployed path.

### 4

Even with perfectly symmetric energies and priors, live softmax beta* is generically NOT symmetric because the row partition functions Z_i differ (verified: max|beta* - beta*^T| = 0.547 at N=4, K=3, tau=0.7). Symmetry requires Z_i = Z_j on each connected component, i.e. beta* doubly stochastic. This kills the halving repair on the deployed softmax path and is a previously unrecorded obstruction.

### 5

Frames are frozen throughout (H2). PIFB2 imposes eta_phi ~ eps^2 eta_q (:963) but does not freeze phi. If Omega_ij(x) co-varies, grad S acquires an additional frame-reaction term not covered by section 2; the whole reaction decomposition would need re-derivation on the bundle. I did not attempt this.

### 6

The reaction decomposition and its closed form assume beta held fixed or already at beta*(x) with the envelope substitution made. If beta is on an independent flow at finite rate (not at its row optimum), the envelope identity fails and grad S acquires the beta-response terms; PIFB2 itself flags this at :3332 ('If the attention optimum beta*(q) has already been substituted, its response derivatives define a different reduced functional and require a separate representation test').

### 7

The E-step/M-step reading gives descent on the posterior-KL gap but NOT convergence: simultaneous (rather than alternating) E and M descent has no general convergence theorem, and PIFB2's own existence results (:3409) are restricted to frozen-beta orthogonal-transport settings with no interior fixed point established for the coupled state-dependent GL^+(K_q) system.

### 8

The observation term typing mismatch is untouched: PIFB2:689 writes -chi_i E_{q_i}[log p(o|k_i,m_i)] (likelihood reads m_i, expectation only over q_i), :669 drops m_i entirely, and the closed theorem's term is -E_{zeta_a} log l_a(o_a|K_a,M_a) over the JOINT. Section 5's bound inherits whichever convention is declared; I did not resolve which.

### 9

tau != 1 and the live alpha_i*(c) precision path remain exactly as open as before. The exact tau mismatch (tau-1) KL(beta||pi) is unaffected by anything proved here.


## novelty

NEW. Exhaustively checked. (1) Zero hits across all of Theory/*.tex and all three docs/derivations/ runs for 'potential game', 'Monderer', 'pseudo-gradient', 'reaction term', 'back-reaction', 'receiver-only', 'sender-only', 'audience', 'M-projection', 'moment matching'. (2) PIFB2.tex:1441, :2430 and :3400-3407 DO already know the receiver-only field V^rec is generically nonintegrable and that the full receiver-plus-sender Hessian is symmetric - but they classify V^rec as 'an optional update approximation' and NEVER identify it as the continuum-time field of the lagged ELBO-exact scheme. That identification (section 4.2) and its spiral-sink counterexample (4.3) are new, and they invert the manuscript's framing. (3) The reaction closed form R^react_i = -b_i E_{qbar_i}[s_{x_i}] = b_i (m_i - mbar_i) is new; the manuscript has only its CROSS-SCALE special case, PIFB2.tex:1602 ('The strict barycenter is therefore an exact M-step coordinate'), and does not connect it to the within-scale peer term. (4) The evidence-invariance lemma (5.1) is new: the exact two-channel run never computes the marginal p^n(o) of its own tied-replica joint (grep over that entire run directory returns nothing on evidence marginals), and its release.json:7-10 carries same-time-emergence at INCONCLUSIVE. (5) The fast-slow run states the lag is load-bearing at transported-peer-derivations.md:33-36 and names three escape routes, but computes no gradients and settles nothing; my sections 2-5 are the quantitative version of that qualitative note. (6) The softmax row-normalization obstruction to beta* symmetry (2.6) appears nowhere.

## next_obligations

### 1

Verify the absolute-continuity side condition Q^{n+1} << P^n(.|o) for the deployed MAgent configuration (smooth chi_i, GL(K_q) transports, SPD-floored covariances). Lemma 5.1's ELBO identity is void without it, and hard-support masking must restrict the source set before the KL, never multiply by zero.

### 2

Extend the reaction decomposition to co-evolving frames: recompute grad S on the bundle with Omega_ij(phi) live, and determine whether the frame-reaction term is again an M-step force (i.e. whether phi_i also plays a generative-parameter role) or a genuinely new sector. This is the one hypothesis (H2) whose failure would damage section 5.

### 3

Settle whether simultaneous E+M descent on S converges. The E-step is contractive under PIFB2:3409's frozen-beta orthogonal hypotheses; the M-step is a moment-matching map. Prove or refute a Lyapunov/normal-hyperbolicity statement for the coupled flow, or exhibit a limit cycle. Note the reaction term is the standard source of EM oscillation.

### 4

Prove the quenched finite-M Sanov theorem with transported reference stated in section 6, on a finite alphabet, with a uniform Stirling remainder. This is tractable today by the method of types and would supply the first quantitative correction to the peer block, of size O(log M / M). Re-scope the LDP approach registry entries from 'route to same-time coupling' to 'finite-M correction of the lagged coupling'.

### 5

Decide the observation-term typing (PIFB2:669 vs :689 vs the closed theorem's joint zeta_a expectation) and re-state section 5's bound under the chosen convention. This is a one-line fix in the algebra but changes what -log p(o) actually is.

### 6

Record the factor-2 result as a coefficient audit item: under edge-symmetry the lagged flow equals the same-time flow at HALVED peer coupling. Even where edge-symmetry fails, this predicts a systematic factor-2 offset between any ELBO-calibrated peer coefficient and the deployed beta, which is empirically checkable in MAgent by comparing a detached-sender ablation against the live path at doubled coupling.

### 7

Recheck section 2's identities at SPD floor eps > 0 (KL_REGULARISER_EPS = 1e-4, PIFB2:187). The reaction closed form uses the exact score identity E_{q}[s] = 0, which the floored KL breaks at O(eps); quantify whether the deployed floor perturbs R^react at O(eps) or O(eps/tau).


## evidence_kind

Mixed: DERIVATION (sections 1.2, 2.2-2.4, 3.2, 4.1-4.2, 5.1-5.3) + APPLICABLE_THEOREM (Monderer-Shapley 1996 Thm 4.5 for the exact-potential criterion, section 2.5; prop:gen-no-distinguished-target Theory/04_generative.tex:130-157 for the moving-target bookkeeping, section 5.2) + COUNTEREXAMPLE (section 2.6 refuting the reciprocal-symmetry conjecture; section 4.3 spiral-sink refuting the dt->0 bridge; section 2.6 softmax row-normalization killing beta* symmetry) + EVIDENCE_VERIFIED (symbolic sympy verification of the reaction closed form to exactly 0; finite-difference verification of the reaction decomposition to 2.7e-9, of the envelope Hessian formula to 8.8e-5 on scale 2.0, of the halving proposition to 8.9e-10; source-code verification that MAgent_Model/gauge_agent/full_vfe.py:1627-1722 applies no detach to the sender). Numerics are used ONLY to confirm identities already derived analytically and to exhibit counterexamples; no theorem here rests on numerical agreement.
