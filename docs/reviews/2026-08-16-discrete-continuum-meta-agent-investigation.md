# Investigation: from one-bit agent updates to an operational continuum

Date: 2026-08-16

Live manuscript revision: 50e6fbdf009f9ba8f01a602d3970b50a34b871fe

Scope: the two supplied notes, Theory/main.tex and its included chapters, the physicist-facing companion, and the related Research wiki pages. This is an investigation and construction proposal, not a theorem-release certificate. The claim-level triage record is stored separately at .verification/discrete-continuum-ledger.json.

## Verdict

The proposed conversion is physically meaningful, but not by the route stated in the supplied note.

A large population of discrete agents can admit a continuous effective description in the same sense that water admits hydrodynamics although it consists of atoms. The correct mechanism is a large-population scaling limit of coarse observables. A one-bit microscopic event changes an intensive field by order \(1/N\); if order \(N\) local events occur per macroscopic unit of time and the conditional drift, fluctuation, and tightness hypotheses close, the coarse process converges to an ODE, PDE, or diffusion. At every finite \(N\), the microscopic process remains discrete.

That conclusion does not produce a continuous RG-scale parameter. Continuous coarse state, continuous time, continuous context or space, and continuous scale are four different claims. The current manuscript supplies exact finite coarse-graining and finite scale structure, but it explicitly leaves the finite-to-continuum dynamical bridge open.

The supplied note also contains two mathematical errors. First,

\[
S_+=\{m\log 2+n\log 3:m,n\in\mathbb N_0\}
\]

is not dense in \(\mathbb R\) or \(\mathbb R_+\). It is locally finite. Its ordered gaps do shrink at large scale, but the nearby endpoints generally lie on incomparable blocking branches, so they are not small consecutive steps of one forward hierarchy. Second, compact structure groups do not globally remove the frame-averaging no-go. The proof in Theory/09_coarsegraining.tex:1044-1049 already uses an order-\(n\) rotation in the compact group \(\mathrm{SO}(K)\). A Karcher mean is uniquely equivariant on a sufficiently concentrated convex neighborhood, not globally on all compact-group configurations.

The strongest defensible research direction is therefore:

\[
\text{finite agent dynamics}
\longrightarrow
\text{selected coarse observables}
\longrightarrow
\text{large-}N\text{ path-law limit}
\longrightarrow
\text{continuous effective model},
\]

while retaining continuous RG scale as a separate problem.

## What Theory/main.tex already supplies

The finite theory is stronger than a heuristic block-spin analogy. Theory/06_general_coarsegraining.tex:170-224 proves exact Fisher contraction for a normalized, parameter-independent Markov channel. Theory/06_general_coarsegraining.tex:565-676 defines holonomy-conditioned transported-law disagreement and proves its zero criterion. Theory/07b_agent_network_rg.tex constructs the full static pointwise parent datum and records the exact VFE defect of discarding conditional information. Theory/09_coarsegraining.tex proves finite Gaussian and gauge-geometric aggregation results and states the deterministic frame-selection no-go.

The manuscript is also explicit about what these statements do not establish. The cluster and its weights are inputs, so the holonomy-conditioned score does not select a partition (Theory/06_general_coarsegraining.tex:672-676). The holonomy-retention construction does not select the child block, parent, partition, or membership channel (Theory/07b_agent_network_rg.tex:1875-1878). The static pointwise parent supplies no fine or parent evolution (Theory/07b_agent_network_rg.tex:2248-2263). Discrete scale endpoints do not determine a continuous beta function (Theory/07b_agent_network_rg.tex:2657-2699). The finite probability construction supplies no probability law on a continuum section space (Theory/03_probability.tex:474-483).

This means the proposed continuum is compatible with the manuscript, but is not already a consequence of it.

## Four different meanings of continuum

### Continuous state

A meta-agent may represent density, concentration, temperature, a probability parameter, or a field amplitude by a real number even when every constituent record is binary. A binary alphabet does not make surprise, entropy, likelihood ratios, KL divergence, VFE, or posterior parameters integer-valued. For a Bernoulli outcome, \(-\log_2 p(x)\) is generally a real number.

At finite \(N\), an empirical density takes values on

\[
\left\{0,\frac1N,\frac2N,\ldots,1\right\}.
\]

Its mesh is \(1/N\), so the state becomes operationally continuous in a large-\(N\) limit.

### Continuous time

One local update per microscopic event is consistent with continuous macroscopic time. The required scaling is that a system with \(N\) active constituents has order \(N\) local events per unit macroscopic time. If instead the entire \(N\)-agent system is permitted only one event per fixed macroscopic unit, the large-\(N\) coarse dynamics freezes.

### Continuous context or space

The contextual manifold \(\mathcal C\) in the present manuscript is declared geometric structure; it is not derived from a sequence of agent graphs. A spatial continuum theorem would need an \(N\)-dependent metric graph or complex, mesh size tending to zero, graph or metric-measure convergence, local conservation or constitutive assumptions, and convergence of the connection and probability laws. Large population alone does not derive spacetime.

### Continuous RG scale

RG depth is a comparison index, not time and not automatically a continuous coordinate. A smooth scale bundle, interpolation, and scale connection are additional data in the current manuscript. Hydrodynamic continuity can hold while RG depth remains discrete.

## A conditional water theorem for meta-agents

The water analogy can be written as a standard fluid-limit theorem.

Let \(M_k^N\in N^{-1}\mathbb Z^d\) be a coarse observable of \(N\) discrete constituents after the \(k\)-th microscopic event. Assume

\[
\left\lVert M_{k+1}^N-M_k^N\right\rVert\leq \frac{c}{N},
\]

and, uniformly on compact state sets,

\[
\mathbb E\left[M_{k+1}^N-M_k^N\mid\mathcal F_k\right]
=\frac1N F(M_k^N)+o(N^{-1}),
\]

where \(F\) is Lipschitz. Define macroscopic time by \(t=k/N\). Then

\[
M_{\lfloor Nt\rfloor}^N
=M_0^N+\frac1N\sum_{k<Nt}F(M_k^N)+R_N(t)+\mathcal M_N(t).
\]

The predictable sum is a Riemann approximation to \(\int_0^tF(m(s))\,ds\). If the remainder is uniformly negligible and the martingale quadratic variation is \(O(N^{-1})\), then on every finite time interval,

\[
\sup_{t\leq T}\left\lVert M_{\lfloor Nt\rfloor}^N-m(t)\right\rVert
\longrightarrow0
\]

in probability, where

\[
\dot m=F(m).
\]

Under convergence of the rescaled conditional covariance and a Lindeberg condition, the fluctuation field

\[
\xi_N(t)=\sqrt N\left(M_{\lfloor Nt\rfloor}^N-m(t)\right)
\]

converges to a Gaussian diffusion. This is the density-dependent jump-process route developed by Kurtz in 1970, 1971, and 1978.

The theorem captures the physical mechanism. One atom or agent changes an intensive field imperceptibly; many local events accumulate into smooth drift; order-\(N^{-1/2}\) fluctuations survive around the deterministic limit. A spatially local version, with conservation laws and mesh refinement, is the route to hydrodynamic PDEs.

The current manuscript cannot invoke this theorem unconditionally because it has not declared the required microscopic transition generator, event-rate scaling, tightness hypotheses, or coarse-observable closure. Theory/07b_agent_network_rg.tex:2248-2263 correctly records that omission.

## What “the meta-agent experiences a continuum” should mean

The statement must be operational. Let \(C_N\) be the meta-agent's observation channel and let

\[
\mu_N=(C_N)_\#P_N
\]

be the law of the observed coarse state. If \(\mu_N\) converges to a continuous law \(\mu\) in Wasserstein or bounded-Lipschitz distance, then every admitted finite-resolution Lipschitz probe has asymptotically the same expectation under \(\mu_N\) and \(\mu\). That is a precise sense in which the discrete and continuous descriptions are indistinguishable to the meta-agent.

It is not true in unrestricted total variation. If \(\mu_N\) is supported on the finite lattice \(N^{-1}\mathbb Z^d\) and \(\mu\) has a density, then the lattice has probability one under \(\mu_N\) and zero under \(\mu\). The total-variation distance is maximal for every finite \(N\). An observer allowed to ask whether the state lies exactly on the lattice can always detect the discreteness.

The claim is therefore relative to the meta-agent's admitted protocols and resolution. In the response language of Theory/05d_relational_inference.tex, one can define a contextual operational pseudometric

\[
d_{\mathrm{op}}(P_N,P_\infty)
=\sup_{u,v\in A}\sup_{f\in\mathcal F}
\left|
\mathbb E_{P_N^{uav}}f-\mathbb E_{P_\infty^{uav}}f
\right|,
\]

where \(A\) is the admitted protocol monoid and \(\mathcal F\) is the meta-agent's declared probe class. The operational continuum statement is \(d_{\mathrm{op}}\to0\), not literal equality of discrete and continuous ontologies. A stronger decision-theoretic version can use Le Cam deficiency between the finite and limiting experiments.

This formulation fits the program's scale-relative view of physics. A bacterium, a human, and a university can carry different effective generative models because their observation channels and actionable probes differ. It does not require one unique microscopic physics to be reconstructed by every scale.

## Blocking: agreement and holonomy do not select the block

For a fixed connected candidate cluster \(I\), the manuscript transports each constituent law to a root and defines

\[
\mathfrak D_I^x
=\inf_{Q\in\mathscr Q_{I,\mathrm{fix}}^x}
\sum_{i\in I}w_i\,\mathrm{KL}(P_i^x\Vert Q).
\]

When the infimum is attained, \(\mathfrak D_I^x=0\) exactly when all transported laws equal one holonomy-invariant law. This is a compatibility theorem for a proposed cluster. It is not a search procedure over clusters.

The distinctions are:

\[
\begin{array}{ll}
H=I
& \text{loop transport is flat in the represented frame},\\
H_\#Q=Q
& \text{the candidate parent law is invariant under loop transport},\\
\mathfrak D_I^x=0
& \text{the transported constituent laws actually agree}.
\end{array}
\]

Every tree is flat because it has no cycles, but agents on a tree can disagree arbitrarily. Singletons also attain zero disagreement. Therefore any objective containing only disagreement selects the trivial all-singleton partition.

The supplied note also conflates law invariance with vector support. For a Gaussian \(Q=\mathcal N(m,C)\),

\[
H_\#Q=Q
\quad\Longleftrightarrow\quad
Hm=m,\qquad HCH^\top=C.
\]

It does not require \(Q\) to be supported on the vector fixed space \(\ker(H-I)\). Theory/09_coarsegraining.tex:818-828 gives a full-support isotropic Gaussian preserved by a holonomy with only a one-dimensional vector fixed space.

The flat reciprocal-fold singularity is not a theorem against blocking flat clusters. Theory/11_obstructions.tex:20-75 concerns an unanchored two-residual Gaussian precision. At \(H=I\), its kernel is the \(K\)-dimensional space of transport-consistent collective modes. Adding a positive anchor makes the precision positive definite. From an RG viewpoint, this zero mode is the collective coordinate one expects to retain, not evidence that the block cannot exist.

## A defensible block-selection principle

The next construction should optimize over connected partitions rather than treat a compatibility test as a selector. One possible objective is

\[
\mathcal J_\lambda(\mathcal P)
=\sum_{I\in\mathcal P}
\left[
\mathfrak D_I^b
+\kappa\mathfrak D_I^m
+c_F L_F(I)
+c_V\Delta_I
\right]
+\lambda|\mathcal P|
+c_\partial B(\mathcal P).
\]

Here \(L_F(I)\) is the Fisher-information loss of the declared normalized channel, \(\Delta_I\) is the exact discarded-conditional VFE defect, \(B(\mathcal P)\) is an optional boundary or cut cost, and \(\lambda|\mathcal P|\) penalizes leaving every agent as its own block. Holonomy-invariant parent families can be imposed as a hard constraint; alternatively, a richer parent can retain holonomy as internal state.

Fisher isometry is a fidelity constraint, not a selector by itself. Theory/06_general_coarsegraining.tex:170-224 proves

\[
I_{\mathrm{fine}}-I_{\mathrm{coarse}}
=\mathbb E\,\operatorname{Cov}(\ell_{\mathrm{fine}}\mid Z)\succeq0,
\]

with equality exactly when the score is measurable from the coarse statistic. This is local score preservation. It does not make the channel unique, imply global experiment recovery, make the support continuous, or intertwine dynamics.

Sweeping \(\lambda\) can generate candidate resolution levels, but nestedness is not automatic. A genuine hierarchy needs a nested-partition constraint or a theorem that the minimizers are monotone. Exact ties should return an invariant argmin set or a distribution over partitions; a forced deterministic tie-break can reintroduce the symmetry obstruction.

## Compact groups and the frame-mean no-go

Theory/09_coarsegraining.tex:1044-1049 proves that no map

\[
F:\mathrm{GL}^+(K)^n\longrightarrow\mathrm{GL}^+(K)
\]

is both left equivariant and permutation symmetric. The proof chooses an order-\(n\) rotation \(v\in\mathrm{SO}(K)\) and the tuple

\[
(I,v,\ldots,v^{n-1}).
\]

Left multiplication by \(v\) cyclically permutes the tuple. Symmetry leaves \(F\) fixed, while equivariance sends it to \(vF\), forcing the range of \(F\) into the proper fixed space of \(v\) and making \(F\) singular.

The same tuple lies inside the compact subgroup \(\mathrm{SO}(K)\). Compactness therefore does not produce a global single-valued deterministic escape. A compact Riemannian group has Fréchet minimizers, but symmetric configurations can have several. On \(\mathrm{SO}(2)\), the pair \((I,-I)\) has two intrinsic midpoints. Afsari's center-of-mass theorem gives uniqueness when the data lie in a sufficiently small convex ball. The correct result is a locally unique equivariant Karcher mean in an approximate-agreement regime, or a global set-valued or stochastic mean.

The SPD cone is different. With the affine-invariant metric it is a nonpositively curved symmetric space, and its Fréchet mean is globally unique and congruence equivariant. This does not refute the frame no-go because

\[
\mathrm{SPD}(K)\simeq\mathrm{GL}^+(K)/\mathrm{SO}(K).
\]

Passing from a frame \(g\) to \(gg^\top\) discards its right-orthogonal component. An SPD mean can canonically aggregate covariances or metrics; it cannot reconstruct the discarded frame orientation or holonomy. The manuscript's forward-KL Gaussian barycenter is also a moment-matching barycenter, not in general the affine-invariant SPD mean.

The safe construction is to average covariance or metric data on SPD while keeping a root frame as a gauge choice, or to retain the relative transports and holonomy mark explicitly.

## Gaussian rescaling and continuous scale

For iid centered Gaussian constituents with variance \(\sigma^2\), consider

\[
Z_\alpha=b^{-\alpha}\sum_{i=1}^bX_i.
\]

Then

\[
\operatorname{Var}(Z_\alpha)=b^{1-2\alpha}\sigma^2.
\]

Preserving the same nondegenerate Gaussian law uniquely gives

\[
\alpha=\frac12.
\]

Theory/07b_agent_network_rg.tex:1052-1087 already contains the resulting normalized Gaussian block and Hermite spectrum. The manuscript correctly says that this normalization is not a general theorem. Correlations change the normalization; stable non-Gaussian fixed laws can change the exponent; density fields use \(1/N\) while fluctuation fields use \(1/\sqrt N\). Rescaling is derived only after the retained observable and fixed-law criterion have been specified.

The mixed \(2/3\) scale argument does not derive a continuous beta. For every finite \(T\),

\[
S_+\cap[0,T]
\]

is finite because \(m\leq T/\log2\) and \(n\leq T/\log3\). The set is not dense. Its ordered gaps tend to zero as scale tends to infinity, but the close points trade extra factors of two against fewer factors of three. Their exponent pairs are generally incomparable in the forward partial order. Every actual forward increment adds at least \(\log2\).

Allowing \(m,n\in\mathbb Z\) produces a dense additive group, but negative exponents require inverse refinement maps. Lossy coarse-graining generally has no inverse. Even a set of dense labels would not supply typed comparison maps, composition coherence, path independence, continuity, or a generator.

A viable continuous-scale program needs one of three additional structures: a family of forward steps whose log-scale mesh tends to zero; a reversible refinement representation on a dense group; or an independent thermodynamic or momentum-shell limit with coherent comparison maps. Fixed heterogeneous integer blocking alone is insufficient.

## Proposed construction program

The theory can be extended without making Gaussian families the definition of an agent or meta-agent.

First, define a sequence of finite networks and microscopic transition laws. The general tier should use standard-Borel state spaces and general statistical manifolds; binary and Gaussian models are worked realizations only.

Second, select connected blocks and normalized coarse channels by an explicit compression-fidelity objective such as \(\mathcal J_\lambda\). Require gauge covariance, the appropriate holonomy branch, and recognition independence. Use the same channel for the generative, posterior, and recognition laws so the existing VFE identity remains applicable.

Third, define the meta-observables \(M^N=C_N(Y^N)\) and state the exact large-\(N\) diagonal: population size, block depth, observation resolution, event-rate scaling, and any spatial mesh must all be named. Theory/07_general_renormalization.tex:882-989 already proves that population and maximal-depth limits need not commute.

Fourth, prove tightness and path-law convergence. The first target should be the conditional ODE/diffusion theorem above. A spatial hydrodynamic theorem comes later and needs locality, conservation or constitutive laws, and graph-to-space convergence.

Fifth, prove operational equivalence relative to the parent protocol and probe class. Fisher loss controls local parameter distinguishability; Wasserstein or bounded-Lipschitz convergence controls finite-resolution observables; Le Cam distance controls statistical decision problems. None substitutes for the others.

Sixth, treat participatory feedback separately. If a meta-agent's inferred state changes microscopic transition rates, the drift becomes endogenous, for example \(F(m,\pi_m)\). A mean-field or controlled-diffusion limit may still exist under Lipschitz feedback, propagation of chaos, and uniform protocol control. This is a new dynamical model and is not supplied by the present fixed static channel. Such feedback is a plausible route to cross-scale nonequilibrium, but it must be derived rather than read into the static theorem.

Only after these steps should one ask whether a continuous RG-scale semigroup also exists. Hydrodynamic continuum emergence does not depend on that answer.

## Corrections to the supplied notes

| Supplied claim | Disposition | Correct statement |
|---|---|---|
| Agreement, \(H=I\), or \(H_\#Q=Q\) selects blocks | False as a selection claim | These conditions score or certify a fixed candidate block. A partition objective and anti-singleton term are still required. |
| \(H_\#Q=Q\) means \(Q\) lives in \(\operatorname{Fix}(H)\) | False | For Gaussian \(Q\), it means \(Hm=m\) and \(HCH^\top=C\); the law may have full support. |
| Flatness makes blocking invalid because the reciprocal fold is singular | Misread | The theorem concerns an unanchored reciprocal Gaussian potential. Its flat zero mode is the transport-consistent collective sector; anchoring or retaining/quotienting that sector changes the conclusion. |
| Compact subgroups defeat the frame-mean no-go | False globally | The obstruction already occurs inside \(\mathrm{SO}(K)\). Karcher uniqueness is local under concentration; global means may be set-valued. |
| SPD AIRM mean defeats the frame no-go | Different problem | It canonically averages covariance or metric data after quotienting orthogonal frame information. |
| Fisher isometry selects the coarse map | False | It is local score preservation for a declared channel and generally has many solutions. |
| \(b^{-1/2}\) Gaussian rescaling is derived | True in the iid Gaussian fixed-law sector | It is not a universal rescaling theorem. |
| \(\mathbb N_0\log2+\mathbb N_0\log3\) is dense | False | It is locally finite; only its far-right gaps shrink. Nearby points are generally incomparable histories. |
| One-bit updates forbid continuous flow | False | A large-\(N\) fluid or diffusion limit is possible when coarse jumps vanish and event rates, drift, covariance, and tightness scale appropriately. |
| A large meta-agent can experience a continuum | Conditionally correct | Define experience operationally through its observation channel and probe class, then prove convergence in the corresponding response metric. |

## Evidence and literature

The primary manuscript anchors are Theory/03_probability.tex:474-483, Theory/06_general_coarsegraining.tex:167-253 and 565-676, Theory/07_general_renormalization.tex:862-1027, Theory/07b_agent_network_rg.tex:1052-1205, 1870-1878, 2248-2263, and 2581-2699, Theory/09_coarsegraining.tex:371-435, 639-679, 818-828, and 1028-1049, Theory/11_obstructions.tex:20-75, and Theory/appendix_claim_ledger.tex:217-302.

The related Research wiki pages are "Renormalization-group flow of beliefs," "Meta-agents and hierarchical emergence," "SPD-manifold geometry and Riemannian optimization," and "Holonomy." They support the same separation between finite exact coarse-graining, declared continuous scale, SPD geometry, and unresolved meta-agent dynamics. No Research-vault file was modified.

External primary references:

1. T. G. Kurtz, "Solutions of Ordinary Differential Equations as Limits of Pure Jump Markov Processes," Journal of Applied Probability 7 (1970), 49-58, https://doi.org/10.1017/S0021900200026929.
2. T. G. Kurtz, "Limit Theorems for Sequences of Jump Markov Processes Approximating Ordinary Differential Processes," Journal of Applied Probability 8 (1971), 344-356, https://doi.org/10.2307/3211904.
3. T. G. Kurtz, "Strong Approximation Theorems for Density Dependent Markov Chains," Stochastic Processes and their Applications 6 (1978), 223-240, https://doi.org/10.1016/0304-4149(78)90020-0.
4. B. Afsari, "Riemannian \(L^p\) Center of Mass: Existence, Uniqueness, and Convexity," Proceedings of the American Mathematical Society 139 (2011), 655-673, https://doi.org/10.1090/S0002-9939-2010-10541-5.
5. N. Ay, J. Jost, H. V. Lê, and L. Schwachhöfer, "Information Geometry and Sufficient Statistics," Probability Theory and Related Fields 162 (2015), 327-364, https://doi.org/10.1007/s00440-014-0574-8.
6. C. E. Shannon, "A Mathematical Theory of Communication," Bell System Technical Journal 27 (1948), 379-423 and 623-656, https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf.

## Status

The hydrodynamic conversion is a viable conditional theorem and a coherent next phase. It is not proved by the current static meta-agent construction. The proposed mixed-\(2/3\) continuous-scale derivation and global compact-group escape should not be used. The most direct research step is to add a declared microscopic jump process and prove the large-\(N\) operational continuum theorem for one selected family of coarse observables, while keeping continuous RG scale, graph-to-space geometry, and participatory feedback as separately typed extensions.
