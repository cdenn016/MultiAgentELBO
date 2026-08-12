# PIFB2 continuum action and exact-ELBO research roadmap

**Status:** Internal theorem-and-experiment plan
**Date:** 2026-08-12
**Research objective:** Construct a rigorous theory of interacting agents as sections of statistical bundles over a higher-dimensional base, with a PIFB2-type action as the primary continuum theory and exact ELBO theory as a probabilistic realization and consistency layer.

## Executive decision

The program should be action-first but not action-only. Its primitive continuum object is a gauge-covariant action on configurations of agent sections. The exact ELBO remains indispensable for determining which action sectors arise from normalized generative models, for providing exact finite inference semantics, and for exposing incompatible assumptions. The complete live-peer PIFB2 action should not be represented as the negative ELBO of one fixed joint law on the original agent-state variables. It is an effective interaction action whose mathematical consequences can still be exact once its kinematics, admissible fields, and variational principle are declared.

“Engineered” is not a defect by itself. Effective field theories are designed from primitives, symmetries, locality, admissible operators, and scale assumptions. The danger is uncontrolled arbitrariness: adding terms without a classification principle, changing them without empirical penalty, or confusing a useful energy with a derived probability model. PIFB2 becomes rigorous when its ontology and action are typed, its allowed term class is constrained, existence and dynamics are proved, discretization is controlled, and competing simpler theories are tested.

The structural theory is neither Gaussian nor intrinsically \(\mathrm{GL}(K)\). The fundamental objects are a principal \(G\)-bundle over the base and associated bundles whose fibers are general statistical manifolds. Gaussian fibers and \(\mathrm{GL}(K)\) frames are one tractable realization used by the present code. Compactness of \(G\) and compact or coercively controlled fiber domains may be imposed in the first existence theorem as analytical hypotheses, not as ontological commitments.

## Similarities, differences, advantages, and risks

| Question | PIFB2-type action theory | Exact-ELBO theory | Recommended hybrid |
|---|---|---|---|
| Primitive object | Section configuration and action functional | Fixed normalized generative law and recognition law | Action is primary; exact laws realize selected sectors |
| Agent | Belief and model sections, support, and local frame data over a base domain | Coordinate or block in a joint measurable state | Connect them only through an explicit realization or lift |
| Interaction | Transported peer divergence, spatial coupling, and gauge terms | Fixed probabilistic factors, kernels, and latent variables | Classify every term as exact, approximate, effective, geometric, or gauge-fixing |
| Base manifold | Load-bearing domain for overlap, fields, derivatives, and propagation | Not required by the bare ELBO identity | Declare the base measure and geometry independently |
| Dynamics | Euler–Lagrange or natural-gradient field flow | Coordinate ascent, posterior inference, or variational flow | Compare flows only after declaring a configuration metric and realization map |
| Principal advantage | Directly represents the intended interacting section-agents | Exact normalization, evidence bounds, and posterior semantics | Preserves the intended ontology without overstating probabilistic derivation |
| Principal risk | Ad hoc terms, ill-typed integrals, gauge confusion, or no continuum limit | Exact mathematics about coordinate blocks rather than full section-agents | More bookkeeping and more explicit bridge obligations |
| Failure condition | No well-defined action, minimizer, flow, gauge covariance, or stable discretization | No fixed normalized joint or mismatch with the claimed coordinate update | A failure in one layer does not automatically refute the other; the bridge is a separate claim |

An ELBO-first derivation program is strongest for local observation likelihoods, self-prior terms, source-label variables, fixed spatial priors, and controlled variational approximations. It is weakest when asked to derive the full live-peer action, because the peer templates move with the variational population. An action-first program represents the intended ontology directly but must earn scientific constraint through theorem closure and distinguishing predictions. The hybrid assigns each tool to the question it can actually answer.

## Geometric and statistical kinematics

Let \((\mathcal C,\mu)\) be a smooth \(d\)-dimensional manifold with a positive smooth density or finite Radon measure. If the action contains local derivatives, the theory must also declare a base cometric, elliptic tensor, or other contraction structure. A smooth manifold has no canonical volume form and a coordinate symbol \(dc\) is not enough. If no primitive base geometry is desired, the alternatives are a regulated section-induced metric or a declared nonlocal kernel on \(\mathcal C\times\mathcal C\).

Let

$$
\pi:P\longrightarrow\mathcal C
$$

be a principal \(G\)-bundle for a Lie group \(G\). Let \(\mathcal M_q\) and \(\mathcal M_s\) be regular statistical manifolds of probability laws on declared sample spaces, equipped with Fisher metrics \(g_q^{\mathrm F},g_s^{\mathrm F}\) and divergences \(D_q,D_s\), initially KL. The group acts through family-preserving smooth actions

$$
\rho_q:G\longrightarrow\operatorname{Diff}(\mathcal M_q),
\qquad
\rho_s:G\longrightarrow\operatorname{Diff}(\mathcal M_s),
$$

which must be induced by declared probability-law transformations and must preserve, or transform covariantly with, the chosen information geometry. The associated statistical bundles are

$$
E_q=P\times_{\rho_q}\mathcal M_q,
\qquad
E_s=P\times_{\rho_s}\mathcal M_s .
$$

Agent \(i\) occupies a measurable or Lipschitz domain \(U_i\subseteq\mathcal C\) and carries sections

$$
q_i,p_i\in\Gamma(E_q|_{U_i}),
\qquad
s_i,r_i\in\Gamma(E_s|_{U_i}),
$$

together with a support field \(\chi_i\), attention rows on nonempty overlap neighborhoods, and any declared connection or relational fields. The belief and model statistical manifolds need not be isomorphic, finite-dimensional in the final theory, or members of the same parametric family.

A local gauge frame is a local section \(u_i:U_i\to P\). On \(U_i\cap U_j\), the transition function between \(u_i\) and \(u_j\) is a change of coordinates, not automatically a physical interaction. If \(\Omega_{ij}\) is only the representation of this transition, then it is pure gauge bookkeeping and has cocycle consistency. Intrinsic comparison of two sections in the same associated fiber needs no additional physical transport. Nontrivial relational physics requires one of two extra structures: a connection \(A\) whose parallel transport compares separated base points, or an independent overlap/link automorphism \(L_{ij}\) with a declared transformation law. The specialization \(\Omega_{ij}=U_iU_j^{-1}\) is the flat coboundary case and cannot generate nontrivial cycle holonomy by itself.

For the first theorem, \(\mathcal M_q\) and \(\mathcal M_s\) should be finite-dimensional regular statistical manifolds with analytically controlled admissible subsets. Sufficient hypotheses include a nondegenerate Fisher metric, finite and jointly lower-semicontinuous KL on the admissible domain, smoothness on its interior, and either compact admissible targets or coercive confinement. Gaussian, categorical, and suitable exponential-family manifolds should be treated as examples satisfying different versions of these hypotheses. The general theorem should be stated in terms of these properties, not in Gaussian coordinates.

## Proposed action class

With simplex-valued attention fields \(\beta_i(c)\) and \(\gamma_i(c)\), overlap priors \(\pi^q,\pi^s\), information-geometric comparison maps \(L^q_{ij},L^s_{ij}\), and covariant derivatives supplied by a connection, the canonical action class is

$$
\begin{aligned}
\mathcal S
={}&
\sum_i\int_{U_i}\chi_i
\left[
D_q(q_i\Vert p_i)
+\lambda_sD_s(s_i\Vert r_i)
+\mathcal L_i^{\mathrm{obs}}
\right]\,d\mu
\\
&+\sum_{i,j}\int_{U_i\cap U_j}\chi_{ij}
\left[
\beta_{ij}D_q(q_i\Vert L^q_{ij}q_j)
+\tau_q\beta_{ij}\log\frac{\beta_{ij}}{\pi^q_{ij}}
\right]\,d\mu
\\
&+\sum_{i,j}\int_{U_i\cap U_j}\chi_{ij}
\left[
\gamma_{ij}D_s(s_i\Vert L^s_{ij}s_j)
+\tau_s\gamma_{ij}\log\frac{\gamma_{ij}}{\pi^s_{ij}}
\right]\,d\mu
\\
&+\eta_q\sum_i\int_{U_i}\lVert D^Aq_i\rVert_{g_q^{\mathrm F}}^2\,d\mu
+\eta_s\sum_i\int_{U_i}\lVert D^As_i\rVert_{g_s^{\mathrm F}}^2\,d\mu
+\kappa\int_{\mathcal C}\lVert F_A\rVert^2\,d\mu
+\mathcal S_{\mathrm{boundary/prior}} .
\end{aligned}
$$

This is a class to be narrowed by axioms, not yet a completed theorem. Every term must be typed on its actual domain. In particular, the observation sector must choose between \(\mathbb E_{q_i}[-\log p(o\mid k)]\) and a joint recognition law \(\zeta_i(k,m)\) for \(\mathbb E_{\zeta_i}[-\log p(o\mid k,m)]\). An expectation under a belief law on \(k\) cannot contain an unintegrated random model variable \(m\).

The first action specification should label every summand. Self-prior and properly constructed observation terms may have exact local-ELBO status. A fixed-connection Markov-field prior or covariant Dirichlet term may have closed-ELBO status. Live peer KL and attention-weighted neighbor consensus are effective interaction terms unless a separate enlarged generative construction is proved. A frame-smoothness term is gauge fixing unless it is reformulated invariantly. A curvature term is physical only when based on genuine connection data. The entire action may optionally admit a configuration-space Gibbs variational identity after a proper reference probability and a finite partition function are proved; that identity is exact at a different level and is not the original state-level ELBO.

## Theorem roadmap

| Target | Minimum hypotheses | Closure obligation |
|---|---|---|
| T0: typed kinematics | Measured base; principal \(G\)-bundle; associated statistical bundles; declared gauge action, sample spaces, overlaps, and boundary conditions | Produce a canonical action in which every law, divergence, measure, random variable, and transformation is typed. |
| T1: well-definedness | Manifold-valued \(H^1\) sections; compact or coercively confined admissible fiber subsets; nondegenerate Fisher metrics; finite lower-semicontinuous divergences | Prove measurability, integrability, and differentiability on the admissible interior, with extended-real conventions at singular boundaries. |
| T2: gauge covariance | One passive local gauge action applied to sections, likelihood data, comparison maps, and connections | Prove invariance of \(\mathcal S\), equivariance of its differential, and invariance of observables. Separate coordinate transitions, gauge fixing, and physical link fields. |
| T3: attention-row elimination | Fixed nonempty measurable neighbor sets; positive row priors; \(\tau_q,\tau_s>0\) | Prove strict convexity, unique \(\beta^\ast,\gamma^\ast\), reduced log-partition values, measurable dependence on fields, and the envelope derivative. |
| T4: existence of minimizers | T0–T3; positive covariant spatial terms; bounded-below observation sector; compact target or coercive confinement | Use the direct method for manifold-valued Sobolev maps: coercive bounds, weak compactness, strong \(L^2\) convergence, closed target constraints, and weak lower semicontinuity. |
| T5: first variation | Sufficient regularity for smooth variations | Derive receiver, sender, attention, connection, and covariant base-derivative terms. Without spatial terms the equations must be identified as pointwise, not propagating. |
| T6: dynamics | Integrated product Fisher metric or another declared mobility on section space | Prove \(d\mathcal S/dt=-\lVert\operatorname{grad}\mathcal S\rVert^2\leq0\) and local well-posedness. Treat global existence separately. |
| T7: zero-dimensional reduction | \(\mathcal C=\{\ast\}\), \(\mu(\{\ast\})=1\) | Prove that derivative and curvature sectors vanish and the theory reduces to PIFB2 \(G\)-attention. Recover \(\mathrm{GL}(K)\) attention only as a specialization with additional representation and statistical-family assumptions. |
| T8: discretization limit | Stable quadrature, consistent transports and covariant differences, shape-regular grids or meshes | Prove consistency plus compactness, then \(\Gamma\)-convergence, finite-element convergence, or an equivalently strong continuum result. |
| T9: optional Gibbs completion | Proper configuration-space reference probability and \(0<Z<\infty\) | Prove the configuration-level variational identity and keep it distinct from state-level ELBO semantics. |

T4 is the decisive first milestone. It establishes that the action defines a nonempty variational theory. T7 proves that the existing zero-dimensional intuition is an exact limit. T8 establishes that a higher-dimensional implementation approximates the declared continuum theory rather than merely resembling it.

## Experiment roadmap

Experiments test implementations, bridges, and predictions; they do not prove mathematical theorems. Every run should freeze the action version, discretization, configuration, seed policy, and machine-readable outputs.

| Experiment | Question | Acceptance gate |
|---|---|---|
| E0: multi-family zero-dimensional oracle | Is the reduction independent of a hidden Gaussian assumption? | Match values, attention optima, and directional derivatives for at least categorical and Gaussian fiber realizations, including asymmetric interactions. |
| E1: gauge test | Are observables invariant and gradients equivariant for the declared \(G\)-action? | Apply random local gauge transformations to all covariant inputs. Require invariant action values and correctly transformed gradients; show separately that explicit gauge fixing changes. |
| E2: transition versus physical link | Is gauge bookkeeping being mistaken for interaction? | Compare pure transition/coboundary links with independent link or connection data. Require trivial loop holonomy in the former and controlled nontrivial holonomy only in the latter. |
| E3: mesh refinement | Does the code approximate one continuum action? | Use manufactured smooth section fields on refined meshes and estimate convergence of quadrature, covariant derivatives, action values, and gradients. |
| E4: propagation ablation | Do spatial terms create genuine base propagation? | Perturb one region with \(\eta_q=\eta_s=0\) and with positive coefficients. The first case should remain ultralocal; the second should follow the PDE behavior derived in T5. |
| E5: ELBO realization audit | Which terms have exact probabilistic semantics? | Construct or fail to construct a normalized fixed joint for every sector. Compare exact source-label updates with engineered attention across temperatures and family-specific assumptions. Report residuals explicitly. |
| E6: dynamics consistency | Does the numerical update implement the metric analyzed in T6? | Compare automatic derivatives, finite directional derivatives, natural-gradient steps, and action dissipation. |
| E7: distinguishing phenomenology | Does the theory predict more than generic consensus optimization? | Pre-register observables such as correlation length, consensus rate, defects, holonomy response, and scaling behavior; compare against simpler consensus, Markov-field, and transformer baselines across seeds and sizes. |

The phrase “physics from cognition” should remain a long-range hypothesis. Action decrease, attention patterns, or emergent visual structure are not sufficient evidence. Credible evidence begins with predictions stable under mesh refinement and structural ablations that distinguish the theory from simpler coupled optimization systems.

## Work packages and gates

| Package | Deliverable | Exit gate |
|---|---|---|
| WP0: freeze ontology | A concise specification choosing the base measure and geometry, principal \(G\)-bundle, associated statistical fibers, connection/link status, likelihood typing, supports, and boundary conditions | No symbol in the action is multiply typed or undefined; Gaussian and \(\mathrm{GL}(K)\) are explicitly examples. |
| WP1: restricted continuum core | A theorem-first manuscript proving T0–T4 for compact \(G\) and analytically controlled regular statistical manifolds | Independent proof review closes well-definedness, gauge covariance, row elimination, and existence. At least two nonisomorphic statistical families instantiate the hypotheses. |
| WP2: variational dynamics | Full first variation, section-space metric, T5–T6, and smooth benchmark solutions | Independent derivation and numerical directional-derivative oracles agree; dissipation is reproduced by the reference integrator. |
| WP3: pure implementation | A minimal implementation of exactly the frozen action, with fiber and group interfaces | E0–E4 pass. The current Gaussian/\(\mathrm{GL}(K)\) code is mapped as one backend, not treated as the abstract theory. |
| WP4: continuum bridge | T7–T8 and a mesh-refinement report | The zero-dimensional equality is exact and at least one higher-dimensional discretization converges. |
| WP5: probabilistic crosswalk | Exact-ELBO realization ledger and optional T9 construction | Every action sector is labeled exact, approximate, effective, geometric, gauge-fixing, or open. |
| WP6: scientific tests | Controlled E5–E7 comparison against simpler baselines | At least one pre-registered prediction survives family, group, seed, size, mesh, and structural ablations before RG or physics claims advance. |

WP0 must precede further large theoretical or code expansion. WP1 should begin with a compact group because that makes quotient and existence arguments controllable, while the general ontology remains a principal \(G\)-bundle for an arbitrary declared Lie group. WP3 should expose interfaces for the statistical manifold, divergence, group action, connection, and quadrature. It should not hard-code Gaussian coordinates or \(\mathrm{GL}(K)\) identities into the abstract layer.

## Relationship to the existing code

The MAgent code is a valuable finite realization of the broader architecture. It represents Gaussian belief and model fields, covariance fields, supports, and \(\mathrm{GL}(K)\)-type frames over a grid-shaped base; performs volume-weighted aggregation; and contains self, peer, observation, frame, curvature, and optional base-neighbor sectors. Its README correctly states that the population coupling is an engineered consensus energy rather than the negative ELBO of one fixed population joint.

Several distinctions already present in the implementation should become theory-level classifications. Its fixed-connection, attention-free covariant Markov-field term is identified as a closed-ELBO member, whereas the attention-weighted neighbor term is an effective consensus regularizer. Its frame-smoothness term is gauge fixing. Its frame-derived connection is pure gauge, while nontrivial curvature requires independent link data. These are strengths because they expose the boundaries rather than hiding them.

The principal implementation gap is not the absence of tensor operations. It is the absence of a frozen general continuum target and a convergence theorem. The abstract layer should therefore be specified before rewriting the runtime. The present Gaussian and \(\mathrm{GL}(K)\) path should become the first backend and oracle. A categorical or other non-Gaussian backend should be added early to prove that the architecture, tests, and theorem statements do not silently depend on Gaussian formulas.

## Claim discipline and immediate sequence

The stable description should be: PIFB2 is a gauge-motivated effective action for interacting section-valued agents; selected sectors admit exact ELBO realizations; the complete live-peer action is not an ordinary fixed-joint state-level ELBO on the original variables; and a normalizable configuration-space Gibbs lift is exact at another level. The grid code is a finite discretization candidate until T8 closes. The base is a context manifold unless a physical interpretation is separately derived.

The next cycle should produce three artifacts in order. First, complete WP0 as a two- to four-page ontology and action specification. Second, write the restricted T0–T4 theorem manuscript with general statistical-manifold assumptions and explicit examples. Third, implement a small fiber-agnostic numerical oracle and run E0–E4. Work on RG closure, scale-free fixed points, or broad phenomenology should wait until those artifacts agree.

Success means there is a typed principal-bundle configuration space, a gauge-covariant and lower-semicontinuous action, an attained minimizer in a nontrivial regime, an exact zero-dimensional reduction, and a convergent discretization. Failure is equally informative: if coercivity destroys the intended ontology, if the group action does not preserve the statistical structure, if gauge invariance conflicts with the interaction, or if mesh refinement has no stable limit, the action class must be revised before physical interpretation.

## Source boundary

This roadmap is based on the live Research/manuscripts/PIFB2.tex and MAgent_Model-main implementation inspected on 2026-08-12, plus docs/derivations/2026-08-12-pifb2-elbo-program-decision/final-report.md. The current manuscript and code use Gaussian fibers and \(\mathrm{GL}(K)\)-type realizations in many formulas. This plan deliberately generalizes those implementation choices to statistical-manifold fibers associated to a principal \(G\)-bundle while retaining the verified state-level ELBO obstruction and the finite-versus-continuum boundary.
