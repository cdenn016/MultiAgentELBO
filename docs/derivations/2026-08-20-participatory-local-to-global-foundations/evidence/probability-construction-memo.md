<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-368c9400e04e0700491b5a05ce03b074b8d146fa7243ce2327638237ab24a718","schema_version":"rigorous-theory-search/v1","target_digest":"368c9400e04e0700491b5a05ce03b074b8d146fa7243ce2327638237ab24a718"} -->
# Probability-construction investigator memo

This memo records a construction portfolio proposed by an independent probability-theory lane.
It is design evidence, not a proof certificate or theorem closure.

## Construction boundary

The local-first architecture has an unavoidable asymmetry:

\[
\{G_{\theta,i,D},\mathbb Q_{i,o,X},K_a\}
\longrightarrow
\begin{cases}
\mathbb P_{\theta,V} & \text{by normalized ordered composition},\\
\mathbb Q_{V,o,X}\in\operatorname{Cpl}(\mathbb Q_{\bullet,o,X})
& \text{by a declared coupling selection}.
\end{cases}
\]

Ordered normalized generative mechanisms determine a population law. Agent-local recognition
laws determine only a coupling class in general. The global recognition law therefore requires a
dependence object or selection rule beyond the marginals.

The existing manuscript already separates a model-presentation law, a sampled presentation, and
its evaluated generative kernel in `Theory/03_probability.tex:68-99`. The proposed rewrite will
name \((q_i^m,\operatorname{ev}_i)\) as the agent's generative-model structure and retain the
Dirac definite-model case.

## Proposed proposition portfolio

For a finite DAG, measurable normalized kernels compose in topological order to a unique
normalized joint determined by the declared mechanisms and order. This is already established in
the current specialized construction at `Theory/04_generative.tex:52-87` and
`Theory/04_generative.tex:202-222`.

Arbitrary reciprocal state conditionals need not be compatible. On two binary variables, one
conditional can force equality and the other inequality; no joint can give probability one to
both disjoint events. Reciprocal dependence therefore requires an ordering, schedule, common-cause
model, or globally normalized undirected construction.

Normalized interaction-record kernels attach to an existing latent joint without requiring an
acyclic interaction hypergraph. Integrating every record coordinate first contributes unit mass
and recovers the normalized latent law. This is the existing result at
`Theory/05b_local_collective_elbo.tex:18-95`. An abstract construction seam belongs in the
generative chapter, while the detailed labeled specialization should remain in Chapter 5b.

The notation must distinguish a normalized record kernel \(K_a\), a directed transition
\(T_{i\leftarrow j}\), an evaluated model mechanism \(K^X_{i,m_i}\), and an unnormalized
potential \(\psi_{ij}\). The current normalizer counterexample at
`Theory/04_generative.tex:224-268` remains the correct boundary for potentials.

For fixed \((o,X)\), the unconstrained coupling class is nonempty because it contains the finite
product law. It is convex. On standard-Borel spaces it is a singleton exactly when at most one
marginal is non-Dirac. If two marginals \(\mu,\nu\) are non-Dirac, choose sets \(A,B\) of
nontrivial probability, put \(f=1_A-\mu(A)\), \(g=1_B-\nu(B)\), and define

\[
dR_\varepsilon(x,y)
=\left[1+\varepsilon f(x)g(y)\right]d\mu(x)d\nu(y),
\qquad 0<|\varepsilon|<1.
\]

The density is nonnegative, normalized, and preserves both marginals. Distinct values of
\(\varepsilon\) give distinct couplings. Tensoring with the remaining marginals yields the
population counterexample. The converse follows because Dirac coordinates are fixed almost
surely. This strengthens the current Gaussian witness at `Theory/03_probability.tex:430-437`.

Additional constraints define an intersection of the coupling class with a feasible set. Product
existence says nothing about the nonemptiness of that intersection. Pointwise selection also does
not automatically supply a measurable kernel in \((o,X)\). Feasibility and measurable selection
remain hypotheses until separately constructed.

Once the population generative law and selected recognition coupling exist, the current extended
ELBO applies. The classical expected-log split requires the manuscript's existing domination,
absolute-continuity, and integrability hypotheses. For a product baseline, complexity separates
into the sum of local marginal divergences plus total correlation. For a directed baseline, the
exact chain rule uses recognition conditionals in the same order, not agent marginals. No generic
sum of marginal agent complexities follows.

## Status boundary

Finite kernel composition, normalized record attachment, product-coupling existence, general
coupling nonuniqueness, the exact ELBO, total-correlation correction, conditional KL chain rules,
and once-only record accounting are proof obligations intended for `ESTABLISHED` status. The
choice of DAG or schedule, the local access maps, the interaction set, a nonproduct coupling
selector, and any constrained coupling feasibility are definitions or hypotheses. Canonical
correlated coupling, continuum-section probability measures, physical dynamics, and a derived
action principle remain open.

Primary mathematical sources proposed for exact scope are Kallenberg, *Foundations of Modern
Probability*, third edition, DOI `https://doi.org/10.1007/978-3-030-61871-1`, and Wainwright and
Jordan, *Graphical Models, Exponential Families, and Variational Inference*, DOI
`https://doi.org/10.1561/2200000001`. No novelty claim follows from those standard constructions.
