# panelA-ground-01-pifb2-deployed-action

*Recovered verbatim from workflow journal.jsonl, 2026-08-13. Agent aa3e5764.*

## summary

The live manuscript is C:/Users/chris and christine/Desktop/Research/manuscripts/PIFB2.tex (3956 lines); the Desktop/MultiAgentELBO/Theory/PIFB2.tex copy is byte-identical (md5 7dd428dd430928d4394292d1cd812a32). All three crosswalk line ranges verify without drift: :663-713 two-channel scalar, :155-176 two statistical manifolds, :929-954 fast/slow hierarchy.

THE DEPLOYED ACTION is the boxed canonical functional Eq. (eq:free_energy_functional_final) at :681-693, a FIVE-TERM family (so named at :1683, :3560). Term by term, all arguments SAME-TIME at one base point c, all integrations int_C ... dc over the base manifold C (:150), taken flat C=R^2 Euclidean in the working framework (:434), with the tower version integrating against sqrt(|g|)(c) dc (:1731):

(T1) sum_i int_C chi_i(c) KL(q_i(c)||p_i(c)) dc. Implicit unit weight = the alpha=1 specialization of alpha_i(c) (:694). Explicit chi_i.
(T2) lambda_h sum_i int_C chi_i(c) KL(s_i(c)||r_i(c)) dc. lambda_h>0, taken as lambda_h=1 in the standard active-inference reading; lambda_h=0 is the frozen-slow ablation (:694). Explicit chi_i.
(T3) sum_ij int_C [ beta_ij(c) KL(q_i||Omega_ij q_j) + tau beta_ij(c) log(beta_ij(c)/pitilde_ij(c)) ] dc. NO explicit chi: chi_ij=chi_i chi_j is absorbed into pitilde_ij := chi_ij pi_ij / sum_k chi_ik pi_ik (:694, :711).
(T4) sum_ij int_C [ gamma_ij(c) KL(s_i||OmegaTilde_ij s_j) + tau gamma_ij(c) log(gamma_ij(c)/pitilde^(s)_ij(c)) ] dc. Same absorbed-prior convention; gamma_ij=0 is the frozen model-alignment ablation (:713).
(T5) - sum_i int_C chi_i(c) E_{q_i(c)}[log p(o(c)|k_i,m_i)] dc. Explicit chi_i.

COEFFICIENTS. tau>0 is the single attention/entropy temperature, factorized in the working implementation as tau = kappa sqrt(K_q) with kappa a learnable scalar, and channel-specialized as kappa_beta = kappa sqrt(K_q) on the belief fiber, kappa_gamma = kappa sqrt(K_m) on the model fiber, coinciding only when K_m=K_q (:673, :2222, :3952). lambda_h is the only other coefficient in the boxed action.

BASE DERIVATIVES / CURVATURE / FRAME SMOOTHNESS ARE ABSENT from every one of T1-T5. No covariant or partial derivative of q, p, s, r appears anywhere in the file (zero grep hits for D_mu, nabla_mu, partial_mu q). The only such terms are OPTIONAL and inactive: gauge-field smoothness lambda_phi int ||grad phi_i||^2 sqrt(g) dc and Fisher mass terms (:713), with :958 stating "In the present studies no frame regularizer is included ... left to future work"; and the Yang-Mills penalty int tr(F_munu F^munu) sqrt(g) dc, whose Regime-I integrand vanishes identically by Maurer-Cartan (:713, :368).

TRANSPORT. Omega_ij(c) = exp[phi_i(c)] exp[-phi_j(c)] in G (:312-314) — a flat Cech coboundary, cocycle Omega_ij Omega_jk = Omega_ik with vanishing holonomy (:320-334, :208), NOT independent link data. The independent-link (Regime-II) promotion Omega_ij = U_i exp(delta_ij . G) U_j^{-1} exists (:374-379) but the checked-in pairwise twist scale and learning rate are zero (:449). OmegaTilde_ij equals Omega_ij as a group element under shared frames, but the reference implementation runs the INDEPENDENT-frame configuration with its own GL(K_m) bundle and frame phitilde_i (:459, :1673).

PRECISION SECTOR. alpha_i(c)>0 promoted at :742-752 with log-barrier R(alpha_i)=b_0 alpha_i - c_0 log alpha_i (:755), optimum alpha_i*(c)=c_0/(b_0+KL(q_i||p_i)) (:776-780), and exact envelope cancellation of the product-rule correction (:826). Active path: one scalar alpha_i* per agent, fixed b_0,c_0 (:811, :453).

TIMESCALES. eta_q : eta_s : eta_phi ~ 1 : eps : eps^2, eps<<1 (:963), imposed not derived (:933).

## extracts

### 1

{
  "label": "Canonical five-term action (boxed)",
  "location": "PIFB2.tex:681-693",
  "statement": "\\boxed{ F[{q_i},{p_i},{s_i},{r_i},{phi_i},{beta_ij},{gamma_ij}] = sum_i int_C chi_i(c) KL(q_i(c)||p_i(c)) dc + lambda_h sum_i int_C chi_i(c) KL(s_i(c)||r_i(c)) dc + sum_ij int_C [ beta_ij(c) KL(q_i || Omega_ij q_j) + tau beta_ij(c) log(beta_ij(c)/pitilde_ij(c)) ] dc + sum_ij int_C [ gamma_ij(c) KL(s_i || OmegaTilde_ij s_j) + tau gamma_ij(c) log(gamma_ij(c)/pitilde^{(s)}_ij(c)) ] dc - sum_i int_C chi_i(c) E_{q_i(c)}[log p(o(c) | k_i, m_i)] dc }  (label eq:free_energy_functional_final)",
  "status_tag": "DEPLOYED_CANONICAL"
}

### 2

{
  "label": "Pointwise version (no integral, same five terms)",
  "location": "PIFB2.tex:664-672",
  "statement": "F(c) = sum_i D_KL(q_i(c)||p_i(c)) + lambda_h sum_i D_KL(s_i(c)||r_i(c)) + sum_{i,j} beta_ij(c) D_KL(q_i(c)||Omega_ij(c) q_j(c)) + tau sum_{i,j} beta_ij(c) log(beta_ij(c)/pi_ij(c)) + sum_{i,j} gamma_ij(c) D_KL(s_i(c)||OmegaTilde_ij(c) s_j(c)) + tau sum_{i,j} gamma_ij(c) log(gamma_ij(c)/pi^{(s)}_ij(c)) - sum_i E_{q_i(c)}[log p(o(c)|k_i)]  (label eq:pointwise_free_energy). NOTE the observation term here has NO m_i, unlike :689.",
  "status_tag": "DEPLOYED_POINTWISE"
}

### 3

{
  "label": "Temperature: literal symbol and deployed numeric factorization",
  "location": "PIFB2.tex:673",
  "statement": "\"the temperature tau > 0 controls attention sharpness. In the working implementation the temperature is factorized as tau = kappa*sqrt(K_q), with kappa a learnable scalar and the sqrt(K_q) factor the dimension scaling familiar from scaled dot-product attention ... The single symbol tau is written for both channels but specializes per channel by the fiber dimension: on the belief fiber tau = kappa_beta = kappa*sqrt(K_q), and on the model fiber kappa_gamma = kappa*sqrt(K_m), the two coinciding only when K_m = K_q.\"",
  "status_tag": "COEFFICIENT"
}

### 4

{
  "label": "Hyper-prior weight lambda_h and absorbed pair-presence prior",
  "location": "PIFB2.tex:694",
  "statement": "\"where the pair-presence-absorbed prior is pitilde_ij(c) := chi_ij(c) pi_ij(c) / sum_k chi_ik(c) pi_ik(c) (and analogously pitilde^{(s)}_ij), and lambda_h > 0 is the hyper-prior weight on the model-channel term, taken as lambda_h = 1 in the standard active-inference reading. Setting lambda_h = 0 defines a frozen-slow-subsystem ablation ... The belief self-term KL(q_i||p_i) is shown with implicit unit weight, the canonical alpha = 1 specialization of the per-agent self-coupling weight alpha_i(c).\"",
  "status_tag": "COEFFICIENT"
}

### 5

{
  "label": "Optimal attention row (softmax)",
  "location": "PIFB2.tex:695-708",
  "statement": "beta*_ij(c) = chi_ij(c) pi_ij(c) exp[ -(1/tau) KL(q_i(c) || Omega_ij q_j(c)) ] / sum_k chi_ik(c) pi_ik(c) exp[ -(1/tau) KL(q_i(c) || Omega_ik q_k(c)) ]  (label eq:beta_optimal). Analogous gamma*_ij with OmegaTilde_ij, s_j, pi^{(s)}_ij.",
  "status_tag": "DERIVED_STATIONARY"
}

### 6

{
  "label": "Transport operator definition \u2014 flat coboundary",
  "location": "PIFB2.tex:311-316",
  "statement": "\"Omega_ij(c) = exp[phi_i(c)] exp[-phi_j(c)] in G\" (label eq:transport_def). \"This group element transforms agent j's representations into agent i's frame, acting on probability distributions through the representation rho: G -> Aut(B) as Omega_ij[q_j](c) := rho(Omega_ij(c)) q_j(c).\" For Gaussians: mu_j -> R_ij mu_j, Sigma_j -> R_ij Sigma_j R_ij^T.",
  "status_tag": "FLAT_COBOUNDARY"
}

### 7

{
  "label": "Cocycle / vanishing holonomy lemma",
  "location": "PIFB2.tex:320-334",
  "statement": "Lemma (Vanishing Holonomy): \"For gauge transport of the form Omega_ij = g_i g_j^{-1} with vertex-local group elements g_i in G, the holonomy around any closed loop vanishes: H_ijk = Omega_ij Omega_jk Omega_ki = I. Equivalently, the cocycle condition Omega_ij Omega_jk = Omega_ik holds for all triples.\"",
  "status_tag": "FLAT_COBOUNDARY"
}

### 8

{
  "label": "Regime I vs Regime II convention",
  "location": "PIFB2.tex:142",
  "statement": "\"In Regime I the connection is the pure-gauge object A^(i)_mu(c) = U_i^{-1}(c) partial_mu U_i(c) ... the inter-agent transport Omega_ij = U_i U_j^{-1} is a Cech cocycle, and the curvature F^(i)_munu vanishes identically by the Maurer-Cartan identity. The active matter-transport path uses this Regime-I cocycle.\"",
  "status_tag": "CURVATURE_ABSENT"
}

### 9

{
  "label": "Independent link data exists but is INACTIVE",
  "location": "PIFB2.tex:374-379, :449",
  "statement": ":374-379: \"Omega_ij = U_i exp(delta_ij . G) U_j^{-1} ... Setting delta_ij = 0 recovers the Regime I cocycle and the vanishing-holonomy lemma.\" :449 (executable contract): \"Active: pairwise matter alignment uses the Regime-I vertex cocycle Omega_ij = U_i U_j^{-1}, while a separate lattice field contributes the configured Frobenius self-action. Opt-in/test-only: independent pairwise connection transport. The checked-in pairwise twist scale and learning rate are zero, so that path is inactive.\"",
  "status_tag": "INACTIVE_SECTOR"
}

### 10

{
  "label": "OmegaTilde_ij \u2014 model-fiber transport, independent in the reference implementation",
  "location": "PIFB2.tex:423, :459",
  "statement": ":423: \"The model-coupling term gamma_ij KL(s_i||OmegaTilde_ij s_j) uses the model-fiber transport OmegaTilde_ij : B_model -> B_model, equal to Omega_ij as a group element but acting on a different fiber.\" :459: \"in the independent-frame configuration of the reference implementation the model fiber carries its own GL(K_m) bundle and frame field phitilde_i ..., OmegaTilde_ij becomes an independent transport, and even the structure-group identification is absent, leaving the cross-scale shadows as the only inter-channel coupling.\"",
  "status_tag": "TRANSPORT_TYPING"
}

### 11

{
  "label": "No cross-bundle morphism between belief and model channels",
  "location": "PIFB2.tex:459",
  "statement": "\"the canonical functional (eq:free_energy_functional_final) contains no cross-bundle morphism coupling the model and belief channels; the two channels couple only through the gauge-frame sector and the within-channel cross-scale shadows of Eq. (eq:cross_scale_shadow).\"",
  "status_tag": "FACTORIZATION"
}

### 12

{
  "label": "Base derivatives / curvature / frame smoothness \u2014 all OPTIONAL and inactive",
  "location": "PIFB2.tex:713",
  "statement": "\"On base manifolds of dimension >= 1 the gauge frame fields additionally induce the connection one-form A_mu^(i)(c) = U_i^{-1} partial_mu U_i and gauge curvature F_munu^(i); optional regularizers include gauge-field smoothness lambda_phi int ||grad phi_i||^2 sqrt(g) dc and Fisher mass terms. A Yang-Mills curvature penalty int tr(F_munu F^munu) sqrt(g) dc is sometimes invoked ..., but the frame-derived Regime-I integrand vanishes identically by the Maurer-Cartan identity. Any nonzero lattice self-action belongs to a separately configured independent connection sector.\"",
  "status_tag": "CURVATURE_ABSENT"
}

### 13

{
  "label": "Frame smoothness explicitly NOT included",
  "location": "PIFB2.tex:958",
  "statement": "\"In the present studies no frame regularizer is included: the frames evolve only through the alignment terms of F, in which the coordinate phi_i enters through the transport operators ... A gradient penalty lambda_phi sum_i int ||grad phi_i(c)||^2 dc would smooth the frame fields spatially and is left to future work.\"",
  "status_tag": "SMOOTHNESS_ABSENT"
}

### 14

{
  "label": "Precision sector: log-barrier regularizer",
  "location": "PIFB2.tex:746-757",
  "statement": "F_i^adaptive = int_C chi_i(c)[ alpha_i(c) D_KL(q_i(c)||p_i(c)) + R(alpha_i(c)) ] dc + F_i^align - int_C chi_i(c) E_{q_i(c)}[log p(o(c)|k_i,m_i)] dc  (eq:free_energy_adaptive), with R(alpha_i) = b_0 alpha_i - c_0 log alpha_i, b_0>0, c_0>0 (eq:precision_regularizer).",
  "status_tag": "PRECISION_SECTOR"
}

### 15

{
  "label": "Precision sector: closed-form optimum",
  "location": "PIFB2.tex:776-780",
  "statement": "\\boxed{ alpha_i*(c) = c_0 / (b_0 + D_KL(q_i(c)||p_i(c))) }  (label eq:state_dependent_alpha). Strictly convex: g''(alpha_i)=c_0/alpha_i^2>0, so alpha_i* is the unique global minimizer (:781).",
  "status_tag": "PRECISION_SECTOR"
}

### 16

{
  "label": "Precision sector: exact envelope cancellation",
  "location": "PIFB2.tex:826",
  "statement": "partial_theta( alpha_i* D_KL + R(alpha_i*) ) = ((alpha_i*)^2/c_0)(b_0 + D_KL) partial_theta D_KL = alpha_i* partial_theta D_KL, \"the envelope form, since b_0 + D_KL = c_0/alpha_i*. The product-rule correction is therefore canceled exactly by the regularizer's theta-dependence.\"",
  "status_tag": "ENVELOPE"
}

### 17

{
  "label": "Envelope theorem: reduced free energy",
  "location": "PIFB2.tex:836-846",
  "statement": "\\boxed{ F_red[{q_i}] = sum_i D_KL(q_i||p_i) - tau sum_i log Z_i - E_q[log p(o|{k_i})] }  (label eq:free_energy_reduced), \"with E_ij = D_KL(q_i||Omega_ij q_j) and Z_i = sum_j pi_ij exp(-E_ij/tau); the support weights chi_i are suppressed for readability in the display.\"",
  "status_tag": "ENVELOPE"
}

### 18

{
  "label": "Exact row identity F_full(beta*) = -tau log Z_i",
  "location": "PIFB2.tex:717-733",
  "statement": "F_{i,full}(beta,x) = sum_j beta_ij E_ij(x) + tau sum_j beta_ij log(beta_ij/pitilde_ij), Z_i(x) = sum_j pitilde_ij exp[-E_ij(x)/tau]; \"Minimization on the row simplex gives beta*_ij = pitilde_ij exp(-E_ij/tau)/Z_i and the exact identity F_{i,full}(beta*(x),x) = F_{i,red}(x) = -tau log Z_i(x)\", with dF_red = sum_j beta*_ij dE_ij. \"The checked-in FullVFE path constructs Eq. (eq:attention_full_reduced_identity) for both alignment channels, adds it to one scalar total, and calls automatic differentiation on that total. The boxed form ... is therefore the executable authority used throughout.\"",
  "status_tag": "ENVELOPE"
}

### 19

{
  "label": "Timescale hierarchy eta_q : eta_s : eta_phi",
  "location": "PIFB2.tex:963",
  "statement": "\"We impose the characteristic ratio eta_q : eta_s : eta_phi ~ 1 : epsilon : epsilon^2 with epsilon << 1, the canonical slow primitive being the generative model s; the adiabatic approximation this ratio would license is conditional on the fast-equilibrium hypothesis stated next.\" Relaxation times: t_s ~ eps^{-1} t_q, t_phi ~ eps^{-2} t_q.",
  "status_tag": "TIMESCALES"
}

### 20

{
  "label": "Timescale separation is imposed, not derived",
  "location": "PIFB2.tex:933",
  "statement": "\"the within-scale fast/slow/very-slow/fixed separation is imposed to match each field's role in information processing rather than derived from the variational structure\". Fast: q_i; learning-timescale: p_i (updated on the slow M-step, no independent intermediate timescale); slow: s_i; very slow: phi_i; hyper-priors r_i fixed at the slowest timescale.",
  "status_tag": "TIMESCALES"
}

### 21

{
  "label": "Fast subsystem functional",
  "location": "PIFB2.tex:938-943",
  "statement": "F_fast[{q_i}] = sum_i int chi_i(c) KL(q_i(c)||p_i(c)) dc + sum_ij int beta_ij(c) KL(q_i(c)||Omega_ij[q_j(c)]) dc - sum_i int chi_i(c) E_{q_i}[log p(o(c)|k_i)] dc, with beta held at beta*_ij. \"the attention-entropy block tau beta_ij log(beta_ij/pitilde_ij) ... is independent of q_i and is omitted from the displayed scalar\"; eta_q ~ O(1) (:945).",
  "status_tag": "FAST_BLOCK"
}

### 22

{
  "label": "Slow subsystem functional",
  "location": "PIFB2.tex:950-954",
  "statement": "F_slow[{s_i}] = lambda_h sum_i int chi_i(c) KL(s_i(c)||r_i(c)) dc + sum_ij int gamma_ij(c) KL(s_i(c)||OmegaTilde_ij[s_j(c)]) dc, with gamma held at gamma*_ij; \"Natural gradient descent on models follows d s_i/dt = -eta_s natgrad_{s_i} F_slow with learning rate eta_s << eta_q\".",
  "status_tag": "SLOW_BLOCK"
}

### 23

{
  "label": "Two statistical manifolds and their typing",
  "location": "PIFB2.tex:160-176",
  "statement": "B_state = {N(mu,Sigma) : mu in R^{K_q}, Sigma > 0} over latent state k in R^{K_q}; B_model = {N(mu,Sigma) : mu in R^{K_m}, Sigma > 0} over generative-model parameters m in R^{K_m}; each with Fisher-Rao metric. \"Beliefs q_i and priors p_i both take values in B_state, while generative models s_i and hyper-priors r_i both take values in B_model. The two manifolds are generically distinct because the latent state k and the model parameters m are different objects with different sample spaces, possibly of different dimensions.\"",
  "status_tag": "TYPING"
}

### 24

{
  "label": "Ansatz status of the functional (manuscript's own fence)",
  "location": "PIFB2.tex:678",
  "statement": "\"The functional displayed below is an ansatz, not a theorem. Its form was fixed by requiring that every term transform covariantly ... it is not obtained from a single normalized generative model over the joint population state. ... On a sample space enlarged by a declared source label, and under a topologically ordered source mask, the divergence-scored row is the exact coordinate update of a fixed normalized joint provided the link covariance is set to the transported sender covariance and the temperature is unity. ... The row at the operating temperature tau = kappa sqrt(K) used throughout this manuscript is therefore not the exact coordinate of any model in that family; the exact construction carries an additional per-source log-determinant logit which the engineered form omits. The tie itself is a declared postulate rather than a derived identity.\"",
  "status_tag": "STATUS_FENCE"
}

### 25

{
  "label": "Cross-scale shadow priors (definition of p_i and r_i)",
  "location": "PIFB2.tex:1665-1671",
  "statement": "p_i^{(s)}(c) = Omega_{i,I}[q_I^{(s+1)}](c),  r_i^{(s)}(c) = OmegaTilde_{i,I}[s_I^{(s+1)}](c)  (label eq:cross_scale_shadow). \"The apparent four-field hierarchy r -> s -> p -> q is in fact two primitive fields (q, s) at each scale connected by cross-scale transport\" (:1673).",
  "status_tag": "PRIOR_TYPING"
}

### 26

{
  "label": "Ouroboros multi-generation model-fiber fragment",
  "location": "PIFB2.tex:1708-1712",
  "statement": "F_ouro[s_i; {s_{I_k}^{(s+k)}}] = sum_{k>=1} lambda_0 rho^k KL( s_i || OmegaTilde_{i,I_k}[s_{I_k}^{(s+k)}] )  (label eq:ouroboros_F), rho in (0,1) the per-generation discount, lambda_0 > 0 the overall ancestral coupling strength. \"The k=1 term is the multi-generation generalization of the single-scale model hyper-prior lambda_h KL(s_i||r_i) ... (with lambda_0 rho in the role of lambda_h). The fragment is model-fiber only.\" On the belief fiber the depths enter via a moment-pooled prior p_i = sum_k rho^k Omega_{i,A_k}[q_{A_k}] / sum_k rho^k, not an additive chain.",
  "status_tag": "TOWER"
}

### 27

{
  "label": "Integration measure across the tower",
  "location": "PIFB2.tex:1731",
  "statement": "\"Throughout the tower the curvature of the base manifold is carried uniformly: every per-scale free-energy term is integrated against the volume form sqrt(|g|)(c) dc, with the base volume form read once and threaded to every scale, so that a flat base reduces sqrt(|g|) to unity.\"",
  "status_tag": "MEASURE"
}

### 28

{
  "label": "Working framework: flat base, Gaussian fibers, gauge group",
  "location": "PIFB2.tex:434",
  "statement": "\"Both fibers are Gaussian. The canonical gauge group is G = GL(K_q, R) acting on the belief fiber ... The base manifold is flat, C = R^2 with Euclidean geometry. Gauge frames are smooth and slowly varying ...\" Sacrificed (:436): \"path-dependent parallel transport (holonomy), non-Gaussian belief structures, heterogeneous agent types, curved base-manifold geometry, and gauge-field curvature F_munu altogether (Regime-I flatness).\"",
  "status_tag": "DOMAIN"
}

### 29

{
  "label": "Support functions chi_i are smooth, not indicators",
  "location": "PIFB2.tex:711",
  "statement": "\"chi_i(c) in [0,1] is agent i's presence function, chi_ij(c) = chi_i(c) chi_j(c) is the soft pairwise presence, and chi_ij is absorbed into the attention prior pitilde_ij in the alignment integrand so that the row-simplex constraint sum_j beta_ij(c) = 1 remains uniform across pairs. ... We adopt the smooth-section convention chi_i : C -> [0,1] rather than a hard {0,1} indicator ... The reference implementation represents spatial supports with smooth bump functions.\"",
  "status_tag": "MEASURE"
}

### 30

{
  "label": "Rigorous-RG appendix uses a finite grid and hard chi",
  "location": "PIFB2.tex:3755",
  "statement": "\"Fix a finite grid Lambda_s subset C at scale s and an index set I_s of microscopic agents. The scale-s state is X_s = {x_i} with x_i = (q_i, p_i, U_i, chi_i) where ... chi_i(c) in {0,1}. ... The microscopic free energy F_s : X_s -> R u {+inf} takes the multi-agent KL form of Section (sec:one_rung), and the variational Gibbs measure is dP_s = Z_s^{-1} exp[-F_s/T_cfg] dnu_s.\"",
  "status_tag": "MEASURE"
}

### 31

{
  "label": "Entropy-suppressed surrogate (NOT the deployed action)",
  "location": "PIFB2.tex:1348-1353, :2224-2231, :2239",
  "statement": ":1350: F[{q_i}] = sum_i D_KL(q_i||p_i) + sum_{i,k} beta_ik D_KL(q_i||Omega_ik[q_k]) - sum_i E_{q_i}[log p(o_i|theta)]  (eq:extended_free_energy), described at :1348 as \"the entropy-suppressed fixed-beta form of Eq. (eq:free_energy_functional_final) with explicit sensory evidence\". :2227-2230 gives S = sum_i alpha_i KL(q_i||p_i) + sum_i lambda_h KL(s_i||r_i) + sum_ij beta_ij(mu_i,Sigma_i,phi_i) KL(q_i||Omega_ij[q_j]) + sum_ij gamma_ij(...) KL(s_i||OmegaTilde_ij[s_j]). :2239: \"They are not equal to grad_x F_red ... These formulas characterize the surrogate only.\"",
  "status_tag": "SURROGATE_NOT_DEPLOYED"
}

### 32

{
  "label": "Wilson / Frobenius plaquette self-action (separate lattice sector)",
  "location": "PIFB2.tex:400-407, :416",
  "statement": "S_Wilson[delta] = beta sum_{(i,j,k)} (1 - (1/K_q) W_ijk), with W_ijk = Re Tr[exp(delta_ij.G) exp(delta_jk.G) exp(delta_ki.G)]; beta -> inf implies H_ijk -> I. :416: \"The checked-in multi-agent configuration selects ym_bounded=True with the default ym_action_form='frobenius'; it therefore uses a nonnegative Frobenius frame-metric plaquette penalty ... Its active pairwise attention transport is the Regime-I vertex cocycle; the independent pairwise Regime-II connection is inactive.\" Frobenius form: ||H_t - I||_F^2.",
  "status_tag": "SEPARATE_SECTOR"
}

### 33

{
  "label": "Gaussian KL closed form used by every alignment term",
  "location": "PIFB2.tex:183-187",
  "statement": "KL(N(mu_1,Sigma_1)||N(mu_2,Sigma_2)) = (1/2)[ log(|Sigma_2|/|Sigma_1|) + tr(Sigma_2^{-1} Sigma_1) + (mu_2-mu_1)^T Sigma_2^{-1} (mu_2-mu_1) - K_q ]  (label eq:gaussian_kl). Footnote: implementation adds SPD floor eps*I to Sigma_2 (KL_REGULARISER_EPS, default 1e-4); exact at eps=0.",
  "status_tag": "CLOSED_FORM"
}

### 34

{
  "label": "Renyi alpha-divergence generalization of the alignment functional",
  "location": "PIFB2.tex:1290-1301",
  "statement": "\"The framework extends, on the domain where the divergence is finite, to the one-parameter Renyi family D_alpha(q||p) with order alpha in (0,inf)\\{1}, and the alpha -> 1 limit recovers the KL.\" beta_ij^{(alpha)} = softmax_j( -D_alpha(q_i||Omega_ij q_j)/tau ). \"The order parameter alpha here is distinct from the per-agent prior precision alpha_i.\"",
  "status_tag": "OPTIONAL_GENERALIZATION"
}

### 35

{
  "label": "Symbol conventions (canonical overloading register)",
  "location": "PIFB2.tex:3948, :3952",
  "statement": ":3948: \"The bare kappa is the positive attention-temperature scalar, with kappa_beta = kappa sqrt(K_q) and kappa_gamma = kappa sqrt(K_m); the indexed kappa_ij and kappa_IJ in the renormalization-group appendix instead denote raw conductances.\" :3952: \"The unsubscripted tau is the attention and entropy temperature ... alpha_i is the per-agent variational precision weighting the agent's own belief-prior coupling alpha_i KL(q_i||p_i) ... beta_ij is the inter-agent attention weight on belief alignment, and gamma_ij is the inter-agent coupling on the model channel ... t_q, t_s, and t_phi are the characteristic belief, model, and frame times.\"",
  "status_tag": "NOTATION"
}


## gotchas

### 1

LINE NUMBERS VERIFIED, NO DRIFT. The crosswalk's cited ranges are correct against the file I opened: :663-713 is the two-channel scalar (subsections 'The Pointwise Variational Free Energy' at :661 and 'The Complete Free Energy Functional' at :675), :155-176 is 'Statistical Manifolds: Beliefs and Models', :929-954 is the fast/slow hierarchy. Both PIFB2.tex copies (Research/manuscripts and Desktop/MultiAgentELBO/Theory) are byte-identical, md5 7dd428dd430928d4394292d1cd812a32, 3956 lines, mtime Jul 28 07:20. Reading either is equivalent; I read the Research/manuscripts one.

### 2

EVERY SUMMAND IS SAME-TIME. There is NO lagged argument anywhere in the deployed action. The string 'lagged' occurs zero times as a word: all four grep hits (:462, :466, :1898, :2084) are the substring inside 'flagged'. Every alignment term evaluates q_i(c) and q_j(c) at the SAME base point and the SAME instant; F carries no time argument at all. The only time-differenced object in the file is a DIAGNOSTIC, not an action term: Delta p_i(t) = int_C KL(p_i^{(s)}(x;t) || p_i^{(s)}(x;t-1)) dx at :1696. A prover mapping the closed lagged theorem (u^n_ab = (Omega^n_ab)_# q^n_b) onto PIFB2 must supply the lag itself; PIFB2 does not contain it.

### 3

NO BASE DERIVATIVES ANYWHERE IN THE MATTER SECTOR. Zero occurrences of D_mu, nabla_mu, partial_mu q, or 'covariant derivative' acting on q, p, s, or r in the whole 3956-line file. The five-term action contains no kinetic term for the statistical fields. Base derivatives appear ONLY through phi via A_mu = U^{-1} partial_mu U, and both terms built from it are optional AND inactive: lambda_phi int ||grad phi_i||^2 sqrt(g) dc is 'not included ... left to future work' (:958), and the Yang-Mills tr(F F) integrand 'vanishes identically by the Maurer-Cartan identity' in Regime I (:713, :368). Do not import a base-gradient or curvature sector into PIFB2 and then claim ELBO agreement; the manuscript's deployed action has neither.

### 4

Omega_ij IS A FLAT COBOUNDARY, NOT INDEPENDENT LINK DATA. Omega_ij = exp(phi_i) exp(-phi_j) (:312-314) with the cocycle Omega_ij Omega_jk = Omega_ik and identically vanishing holonomy (:320-334). Independent link data EXISTS in the manuscript as the Regime-II edge-relaxed form Omega_ij = U_i exp(delta_ij . G) U_j^{-1} (:374-379), but the checked-in pairwise twist scale and learning rate are ZERO, so that path is inactive (:449, :416). Answer to the posed question: flat coboundary in the deployed action.

### 5

OmegaTilde_ij IS NOT Omega_ij IN THE DEPLOYED CODE. Under shared frames they are the same group element in two representations (:423), but 'in the independent-frame configuration of the reference implementation the model fiber carries its own GL(K_m) bundle and frame field phitilde_i ... and even the structure-group identification is absent' (:459, :1673). A proof that ties the two channels through one frame field is proving the shared-frame variant, not the reference implementation.

### 6

THE OBSERVATION TERM IS TYPED INCONSISTENTLY BETWEEN THE TWO DISPLAYS AND DOES NOT MATCH THE THEOREM'S JOINT EXPECTATION. At :689 the integrand is -chi_i E_{q_i(c)}[log p(o(c) | k_i, m_i)] — the likelihood conditions on BOTH k_i and m_i, but the expectation is taken over q_i ALONE, with no s_i (or joint zeta_i) expectation. At :669 the pointwise version drops m_i entirely: -E_{q_i(c)}[log p(o(c)|k_i)]. The closed theorem's term is -E_{zeta_a} log l_a(o_a | K_a, M_a), an expectation over the JOINT (K,M). Matching these requires either declaring zeta_a = q_a (x) s_a and averaging over s_i as well, or restricting to the :669 form. This is a real typing mismatch, not a notational one.

### 7

chi WEIGHTING IS NOT UNIFORM ACROSS TERMS. The self-terms (T1, T2) and the observation term (T5) carry an EXPLICIT chi_i(c) factor. The two alignment blocks (T3, T4) carry NO explicit chi: chi_ij = chi_i chi_j is absorbed into the normalized prior pitilde_ij := chi_ij pi_ij / sum_k chi_ik pi_ik (:694, :711). The two bookkeepings coincide only for hard masks chi_ij in {0,1}. Also note T2 (lambda_h KL(s||r)) carries chi_i while T4 (model alignment) does not — an asymmetry easy to miss.

### 8

SYMBOL COLLISIONS THAT WILL BREAK A CARELESS TRANSCRIPTION. (a) beta is BOTH the attention weight beta_ij AND the Wilson lattice coupling in S_Wilson = beta sum (1 - W/K_q) at :403. (b) alpha is BOTH the per-agent precision alpha_i(c), the Renyi divergence order alpha (:1291), AND the Regime-I/II relaxation scalar alpha in [0,1] at :416 — disambiguated only by subscript presence (:3952, :1301). (c) s is BOTH the generative-model field s_i AND the scale index (s) (:3946). (d) kappa is the temperature scalar in the body but denotes raw conductances as kappa_ij/kappa_IJ in the RG appendix (:3948). (e) tau_q, tau_s, tau_p are detector dispersion temperatures, NOT the attention temperature; relaxation times use t exclusively (:3952). (f) M is attention compatibility, mass/stiffness block, or finite-size diagnostic by decoration (:3948).

### 9

TWO DISTINCT SCALARS ARE BOTH CALLED THE FREE ENERGY; ONLY ONE IS DEPLOYED. The boxed Eq. (eq:free_energy_functional_final) with the attention-entropy blocks IS the executable authority: 'The checked-in FullVFE path constructs Eq. (eq:attention_full_reduced_identity) for both alignment channels, adds it to one scalar total, and calls automatic differentiation on that total' (:733). The ENTROPY-SUPPRESSED surrogate S (:1350 eq:extended_free_energy, :2227) drops the entropy blocks and is explicitly disavowed as not what the optimizer differentiates (:2239, :733, :871). F_red = sum_i KL(q_i||p_i) - tau sum_i log Z_i - E[log p] (:836-845) is the ENVELOPE REDUCTION of the boxed action at beta = beta*, not a third independent action.

### 10

THE MANUSCRIPT ALREADY CONCEDES THE ANSATZ STATUS AND THE tau=1 OBSTRUCTION AT :678. It states that the functional 'is an ansatz, not a theorem', 'is not obtained from a single normalized generative model over the joint population state', that the exact-coordinate reading requires 'the link covariance is set to the transported sender covariance and the temperature is unity', that 'the row at the operating temperature tau = kappa sqrt(K) used throughout this manuscript is therefore not the exact coordinate of any model in that family', and that 'the exact construction carries an additional per-source log-determinant logit which the engineered form omits'. Do not re-derive this as a new finding, and do not cite :678 as independent confirmation of the closed theorem — it is a back-reference TO the companion exact-ELBO treatment.

### 11

DEPLOYED tau IS NOT 1. tau = kappa sqrt(K_q) on the belief channel and kappa sqrt(K_m) on the model channel, kappa a LEARNABLE scalar (:673, :2222, :3952). The closed theorem's exact equality is at unit temperature. The channel split also means a single tau in the written action is a notational compression: the two channels genuinely run different temperatures unless K_m = K_q (:673).

### 12

DEPLOYED SELF-COUPLING IS NOT UNIT-COEFFICIENT ON THE ACTIVE PATH. The boxed action shows KL(q_i||p_i) at implicit weight 1, but 'The reference implementation instead evaluates the scalar per-agent optimum (eq:state_dependent_alpha) as its live path' (:784), i.e. alpha_i* = c_0/(b_0 + KL(q_i||p_i)) with the log-barrier R in the graph. The constant-alpha = 1 case is an ABLATION that 'a future emergence study must record' (:784). The closed theorem assumes unit private coefficients; PIFB2's active path does not.

### 13

lambda_h = 1 IS A READING, NOT A CONFIGURED VALUE. :694 says lambda_h > 0 'taken as lambda_h = 1 in the standard active-inference reading'. The executable contract at :448 instead reports model_lr_ratio = 0.01 as the deployed fast/slow separation, and notes it 'supplies separation but not block-coordinate optimization' — a LEARNING-RATE ratio, not the action coefficient lambda_h. Do not conflate them.

### 14

eta IS EXCLUSIVELY A LEARNING RATE IN PIFB2, NEVER AN ACTION COEFFICIENT. eta_q, eta_s, eta_phi (and eta_mu, eta_Sigma at :969-971) parameterize the gradient flow, not the functional. The ratio 1 : eps : eps^2 (:963) is IMPOSED (:933), and the adiabatic approximation it would license is explicitly conditional on a fast-equilibrium hypothesis 'certified only in restricted regimes ... with no interior fixed point established for the fully coupled, state-dependent GL^+(K_q) system' (:963).

### 15

INTEGRATION DOMAIN VARIES BY SECTION — pick the right one. Body: int_C ... dc over the smooth base manifold C (Def. :148-151), taken flat C = R^2 Euclidean in the working framework (:434), with smooth bump chi_i (:711). Tower: same terms against the volume form sqrt(|g|)(c) dc (:1731). Rigorous-RG appendix: a FINITE GRID Lambda_s subset C with HARD chi_i in {0,1} and a Gibbs reference measure dnu_s, explicitly excluding raw Haar on noncompact GL^+(K_q) (:3755). Zero-dimensional transformer limit: C collapses to a single point x_0 (:1012), so all int_C vanish and only the finite sums over token-agents survive. The closed theorem's finite agent-site set A corresponds to the LAST of these, not to the body's continuum integral.

### 16

p_i AND r_i ARE NOT FREE PRIORS. They are DEFINED as transported parent posteriors: p_i^{(s)} = Omega_{i,I}[q_I^{(s+1)}], r_i^{(s)} = OmegaTilde_{i,I}[s_I^{(s+1)}] (:1665-1671). The manuscript flags this as 'a structural commitment of the framework rather than a theorem of standard hierarchical variational inference' (:1675). Any ELBO argument treating p_a, r_a as fixed base measures is proving something about a DIFFERENT object than PIFB2's deployed self-terms, unless the parent is frozen.

### 17

THE RECOGNITION FACTORIZATION IS BUILT IN, NOT ASSUMED. PIFB2 has NO joint recognition over (k_i, m_i): 'the canonical functional contains no cross-bundle morphism coupling the model and belief channels' (:459). So the mutual-information correction I_{zeta_a}(K_a;M_a) of the closed theorem has no PIFB2 counterpart to match — PIFB2 sits at zeta_a = q_a (x) s_a by construction. This is a structural fact of the manuscript (cite :459), not a licence to assert the theorem applies; the tau, alpha_i, lag, and observation-typing mismatches above are independent and remain.

### 18

THE ACTION IS NOT GAUGE-INVARIANT IN THE FULL LOCAL SENSE AS DEPLOYED. :341 states the functional is invariant under the full local action 'exactly when all statistical fields, including the observation model and any frozen hyper-prior, are transformed together, and fails to be invariant only when a fixed field is exempted from the action. We use the global diagonal redundancy as the working notion because the implementation holds the observation channel fixed.' So the deployed symmetry is the GLOBAL DIAGONAL right-translation U_i -> U_i g only.

### 19

KL(q||p) IS COMPUTED WITH AN SPD FLOOR BY DEFAULT. Footnote at :187: the implementation adds eps*I to the SECOND-argument covariance (KL_REGULARISER_EPS, default 1e-4), so Eq. (eq:gaussian_kl) 'holds exactly as written on the pure path eps = 0 ... and up to O(eps) terms at the default floor.' Exact-identity claims must declare eps = 0.

### 20

eq:ouroboros_F SUPERSEDES lambda_h FOR THE MULTI-GENERATION CASE, AND ONLY ON THE MODEL FIBER. :1712: 'The k=1 term is the multi-generation generalization of the single-scale model hyper-prior lambda_h KL(s_i||r_i) (with lambda_0 rho in the role of lambda_h ...), so the immediate-parent model coupling is carried once by this fragment rather than separately. The fragment is model-fiber only.' On the belief fiber the deeper generations enter through a moment-POOLED prior inside the single KL(q_i||p_i), not as an additive chain, and 'an explicit additive belief chain remains unimplemented'.

