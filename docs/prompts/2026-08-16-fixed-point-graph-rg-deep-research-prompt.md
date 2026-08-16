# Deep-research prompt: fixed-point graph renormalization of gauge-VFE agents

Use the following prompt verbatim with Opus 5 or Fable 5. Give the model access to the repository and Research vault paths named below.

## Prompt

You are a research-level mathematical physicist specializing in variational inference, gauge theory, statistical mechanics, complex networks, and renormalization. Investigate the following problem from first principles and against the supplied live theory. Do not assume the desired conclusion. Distinguish exact theorems, conditional constructions, controlled approximations, conjectures, and physical interpretations.

Read the complete manuscript assembled by `C:\Users\chris and christine\Desktop\MultiAgentELBO\Theory\main.tex`. Pay particular attention to `03_probability.tex`, `04_generative.tex`, `05_elbo.tex`, `05b_local_collective_elbo.tex`, `06_general_coarsegraining.tex`, `07_general_renormalization.tex`, `07b_agent_network_rg.tex`, `07c_full_graph_meta_agent_vfe.tex`, and `10_renormalization.tex`. Consult `Theory/SPEC.md`, `solid_RG_theory.md`, `physicists_companion.tex`, and `Theory/grand_canonical_meta_agent_formation.tex` for boundaries and interpretation. The general theory uses arbitrary standard-Borel or smooth statistical model spaces; multivariate Gaussians are only an optional computational realization.

Use the Research vault at `C:\Users\chris and christine\Desktop\Research`. Read `sources/papers/berman-2023-bayesian-renormalization.md`, `sources/papers/gabrielli-2025-network-renormalization.md`, `sources/papers/villegas-2023-laplacian-renormalization-group.md`, and `sources/papers/garuccio-2023-multiscale-network-renormalization.md`. Check them against the primary papers, especially Berman, Klinger, and Stapleton, “Bayesian Renormalization,” arXiv:2305.10491, and Gabrielli, Garlaschelli, Patil, and Serrano, “Network renormalization,” arXiv:2412.12988. Do not treat a review's open problem as a solved theorem.

All scale-0 agents lie at one fixed contextual point (c_*\in\mathcal C). There is no assumed physical length, lattice, translation symmetry, momentum space, or tree. The finite directed network may contain cycles. Each ordered edge has two generally non-flat transports, (Omega_{ij}^b) for beliefs and (Omega_{ij}^m) for model presentations. Nontrivial loop holonomy is allowed and must not be penalized to the identity without a separately justified physical hypothesis.

The belief and model channels have normalized directed source rows (eta_{ij}) and (gamma_{ij}), external receiver occupancies (alpha_i^b,alpha_i^m), and joint edge-event laws (eta_{ij}^b=alpha_i^beta_{ij}), (eta_{ij}^m=alpha_i^mgamma_{ij}). Their transported energies are

[
D_{ij}^b=D_{\rm KL}(q_i^b\Vert(\Omega_{ij}^b)_\#q_j^b),
\qquad
D_{ij}^m=D_{\rm KL}(q_i^m\Vert(\Omega_{ij}^m)_\#q_j^m).
]

The correct row free energies include entropy relative to reference rows:

[
\Phi_i^b=\sum_j\beta_{ij}D_{ij}^b+\tau_i^bD_{\rm KL}(\beta_i\Vert\pi_i^b),
\qquad
\Phi_i^m=\sum_j\gamma_{ij}D_{ij}^m+\tau_i^mD_{\rm KL}(\gamma_i\Vert\pi_i^m).
]

Both divergences and rows evolve under descent. The heuristic (1/\beta_{ij}) is only a directed row-relative interaction length, not automatically a metric. Investigate better intrinsic scales based on edge-event laws, raw conductances, reversible symmetrizations, directed Laplacians, diffusion, or information geometry.

The full VFE must come from one normalized multiscale generative kernel (mathbb P_	heta(do,dW\mid X)) fixed before recognition and one normalized correlated recognition kernel (mathbb Q_phi(dW\mid o,X)):

[
\mathcal F^{\rm ext}[\mathbb Q_phi;X,o]
=-\log p_	heta(o\mid X)
+D_{\rm KL}(\mathbb Q_phi\Vert\boldsymbol\Pi_{	heta,o,X}).
]

Any decomposition into observation, self, graph-edge, partition, parent-child, connection, or residual terms must be derived from a declared factorization of these laws or a normalized Gibbs factor with its partition function. Otherwise call it a composite free-energy potential, not an ELBO. Do not double-count a shared interaction factor by summing local coordinate potentials. Do not reconstruct a correlated recognition law from its marginals.

Answer these questions:

1. Construct the most general tractable normalized finite-depth joint containing belief laws, model-presentation laws, (eta,gamma), non-flat transports, stochastic partitions, retained holonomy marks, and parent variables.
2. Derive the exact VFE and conditional-KL decomposition. Identify every normalizer, base measure, absolute-continuity condition, and finite-versus-extended-real boundary.
3. Compare three mechanisms for parent influence: top-down generative kernels with bottom-up recognition, delayed parent-to-child feedback, and normalized undirected reciprocal Gibbs factors. Explain why an instantaneous deterministic pushforward parent and an independent same-time parent cause cannot simply be imposed together.
4. Put partition variables inside the probabilistic model. Derive their variational update and the priors or complexity terms preventing all-singleton and all-in-one-block degeneracies.
5. Define graph RG by pushing (eta^b,eta^m) and then disintegrating parent rows. Treat directed graphs, zero weights, overlaps, distinct belief/model partitions, and nested composition.
6. Treat non-flat connection data exactly. Determine when (H_\#Q=Q) is necessary or sufficient for a holonomy-blind parent and when the parent must retain root, path, representation, or boundary data. Study the distribution of dressed microscopic transports (Theta_{ij}^{IJ}=\Omega_{Ii}\Omega_{ij}\Omega_{jJ}), not only a mean.
7. Determine whether descent can spontaneously produce persistent scale-1 blocks, then scale-2 blocks, on a generic cyclic graph. State timescale-separation, spectral-gap, metastability, closure, and persistence hypotheses. Give counterexamples showing why low transported KL or large (eta) alone is insufficient.
8. Derive cross-scale natural-gradient equations and the semiconjugacy or lumpability defect. Separate optimization time from physical time. State what flux, delay, nonreciprocity, stochastic drive, or antisymmetric sector is needed for sustained nonequilibrium and Wheelerian feedback.
9. Evaluate Bayesian renormalization as a model-space relevance criterion and network-renormalization frameworks as topology/scale mechanisms. Identify what each contributes and what remains unsolved for a directed two-channel gauge network. Include Laplacian RG and the additive-hidden-variable multiscale model.
10. Propose a minimal finite categorical or non-Gaussian experiment falsifying the hierarchy mechanism before any Gaussian implementation. Measure partition persistence, VFE accounting, closure residual, holonomy retention, coarse-edge composition, and downward influence.

Begin with a physicist-facing statement of the full VFE and a diagram of the multiscale architecture. Then give a typed mathematical construction, exact derivations, and a table marking each claim ESTABLISHED, CONDITIONAL, CONJECTURE, NUMERICAL, or OPEN. Include at least three competing block-formation mechanisms. Give explicit counterexamples to false shortcuts. End with the strongest defensible theorem, unresolved proof obligations, and a staged simulation program.

Do not assume flat edges, a tree, a unique hierarchy, a unique latent DAG, a unique microscopic physics, Euclidean distance, a momentum cutoff, Gaussianity, or that (1/\beta) is a metric. Do not infer autonomous agency or physical spacetime from static coarse-graining. Do not identify Bayesian inference and RG without matching their domains and scale orientations. Cite primary sources with exact identifiers and identify statements that come only from a review or project manuscript.
