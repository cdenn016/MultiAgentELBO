# ELBO–PIFB2 construction roadmap

Date: 2026-08-12

Status: finite two-channel theorem closed; continuum derivation remains open.

## Decision

The next theory should be **ELBO-founded and effective-action organized**. PIFB2 supplies the
field ontology and candidate operator basis; the exact ELBO program supplies normalization,
probability typing, entropy, and a non-circular derivation test. The current MAgent code is a
legacy prototype and numerical intuition source, not the specification for the replacement
implementation.

The number of agents \(N\) is fixed and finite (for example, 923). The continuum limit refines the
base lattice; it is not an \(N\to\infty\) population limit. Thermodynamic and large-population
limits are later theories.

## 1. Typed fast/slow state

For agent \(i\) at base point \(c\) and scale \(\ell\):

- \(q_{i,\ell}(c)\) is the fast **recognition density** (modern: variational density or approximate
  posterior) over hidden states \(k_i\).
- \(s_{i,\ell}(c)\) is the agent's slow **generative-model section**. In the current PIFB2
  probability representation it is a normalized law over model parameters \(m_i\), so it is also
  the model-parameter marginal of the variational law when those parameters are inferred. This
  double role does not make \(s_i\) merely another fast recognition density: it encodes which
  generative model the agent believes or uses.
- \(L_i(do_i\mid k_i,m_i,c)\) is the normalized observation/likelihood kernel. The section \(s_i\),
  the hidden-state prior or dynamics, and \(L_i\) together determine the agent's predictive
  generative model. If the agent has a point model \(\theta_i\), use
  \(s_i=\delta_{\theta_i}\).
- A non-factorized observation term uses a joint recognition marginal
  \(\zeta_i(dk_i,dm_i)\); \(q_i\otimes s_i\) is a declared mean-field specialization, not a default.

The fast/slow split is a modeling postulate unless backed by a singular-perturbation theorem.
At fixed slow structure \(S\), the exact state-level identity is

\[
\mathcal F_{\rm state}[Q;S,o]
=-\log p(o\mid S)
+D_{\rm KL}\bigl(Q\Vert P(\cdot\mid o,S)\bigr).
\]

Thus unrestricted profiling yields \(\inf_Q\mathcal F_{\rm state}=-\log p(o\mid S)\); a restricted
recognition family leaves the posterior-KL gap. A dynamical adiabatic reduction additionally needs
a stable normally hyperbolic fast minimizer \(q^*(S)\). At finite fast temperature, integrate over
\(q\) and retain the fluctuation determinant rather than replacing the integral by an infimum.

## 2. Transported recognition-field interaction

Use the typed term

\[
D_{\rm KL}\!\left(q_i\middle\| (\Omega_{ij})_\#q_j\right).
\]

The pushforward is essential: \(q_j\) lives in agent \(j\)'s fiber. Call this a **transported
recognition-field interaction** or **relational inference coupling**. “Consensus” describes only
the zero-energy condition \(q_i=(\Omega_{ij})_\#q_j\). With asymmetric KL, directed weights,
observations, priors, incompatible transports, or holonomy, the same interaction can produce
compromise, clustering, frustration, or nonequilibrium currents.

Its nonlinearity is not a defect. The exactness question is whether it arises from a normalized
law that is fixed independently of the same-step recognition factors.

### Exact dynamical realization: lagged source-label model

At time \(n+1\), condition on the previous recognition configuration and define

\[
r_{ij}^{n}=(\Omega_{ij}^{n})_\#q_j^{n},\qquad
P_i^n(dj,dx)=\pi_{ij}r_{ij}^{n}(dx),\qquad
Q_i^{n+1}(dj,dx)=\beta_{ij}q_i^{n+1}(dx).
\]

Then

\[
D_{\rm KL}(Q_i^{n+1}\Vert P_i^n)
=D_{\rm KL}(\beta_i\Vert\pi_i)
+\sum_j\beta_{ij}D_{\rm KL}\!\left(q_i^{n+1}\middle\|r_{ij}^{n}\right).
\]

Both endpoint beliefs fluctuate through time, but the conditional generative law does not read
the same-step variational law. This is the recommended first exact implementation target.
Nonunit temperature requires a separately normalized tempered model; row entropy cannot simply
be rescaled while leaving its normalizers behind.

### Exact finite two-channel theorem: closed

The construction has now been completed for fixed finite \(N\) and a finite base lattice. In
addition to the belief source law
\(u_{ij}^n=(\Omega_{ij}^n)_\#q_j^n\), introduce the slow-model source law
\(v_{ij}^n=(\widetilde\Omega_{ij}^n)_\#s_j^n\). Independent receiver-local relational copies make
the history-conditioned generative law a product of normalized finite mixtures. Restricting the
recognition family so that those copies reuse the private marginals \(q_i\) and \(s_i\) gives the
exact negative ELBO

\[
\begin{aligned}
\mathcal F_h^{n+1}=\sum_i\Big[&D_{\rm KL}(q_i\Vert p_i)
+D_{\rm KL}(s_i\Vert r_i)
-\mathbb E_{\zeta_i}\log \ell_i(o_i\mid K_i,M_i)
+I_{\zeta_i}(K_i;M_i)\\
&+D_{\rm KL}(\beta_i\Vert\pi_i^q)
+\sum_j\beta_{ij}D_{\rm KL}(q_i\Vert u_{ij}^n)\\
&+D_{\rm KL}(\gamma_i\Vert\pi_i^s)
+\sum_j\gamma_{ij}D_{\rm KL}(s_i\Vert v_{ij}^n)\Big].
\end{aligned}
\]

Thus the two transported KL channels are not guessed penalties in this model: they are exact
finite-mixture KL components. Under the explicit mean-field restriction
\(\zeta_i=q_i\otimes s_i\), the mutual-information correction vanishes and this equals the
lagged, unit-temperature, unit-private-coefficient PIFB2 scalar. For correlated state/model
recognition the mutual information is mandatory. The theorem is an existence result for a tied-
replica representation, not a uniqueness or microscopic-emergence theorem.

The verified construction, proof, counterexamples, and release record are in
[`2026-08-12-exact-two-channel-finite-elbo`](../derivations/2026-08-12-exact-two-channel-finite-elbo/construction-or-strongest-theorem.md).

### Equilibrium/RG realization: configuration law

Promote \(\widehat q_i,\widehat s_i\) to genuine random coordinates on a complete configuration
space and derive their coarse law from an independently specified microscopic law. A Gibbs law
defined by exponentiating the desired action is an exact representation, but it is circular as an
emergence derivation. Configuration entropy and partition normalizers remain mandatory.

### Noncircular emergence candidate: empirical measures

Let \(q_i\) be an empirical measure of many microscopic samples or messages. Relative-entropy
rate functions can then arise by large deviations. Transported weighted peer terms require an
explicit source-label/fixed-count construction and a proof of the finite-sample corrections. This
is the most promising emergence route, but it remains open.

The lagged process and the equilibrium configuration law must not be identified without an
invariant-measure or detailed-balance theorem.

## 3. Gauge-group ladder

Because the fiber has dimension \(K\), the simple rotation group is \(SO(K)\), not \(SO(N)\).
Begin with an arbitrary closed compact subgroup \(G\le GL(K,\mathbb R)\) in a declared
representation. Haar averaging supplies a positive \(G\)-invariant inner product, so after a
basis change \(G\subseteq O(K)\). This includes finite groups, tori, block products, and real
representations of \(U(m),SU(m)\), and \(Sp(m)\), not only \(SO(K)\).

The compact theory gets a normalized Haar reference and positive Wilson-type curvature sector.
It should prove the finite-lattice theorem and deterministic continuum limit first.

Do not discard full \(GL(K)\). Its polar structure separates compact rotations from an SPD
scale/shear sector that may encode covariance, precision, nonmetricity, or model complexity. But
those modes are physical only if the theory adds a transforming SPD/Fisher metric \(M\), controls
\(D_A M\), and defines gauge-invariant observables. Raw Frobenius curvature is not invariant under
general conjugation, and noncompact gauge volume is not normalizable. “Complexity increases” is a
hypothesis until a quotient-invariant observable and a dynamical prediction are specified.

## 4. Fixed-\(N\) lattice-to-continuum program

1. Specify a normalized finite-lattice microscopic process with fast \(q\), slow \(s\), source
   labels, observations, links, and proper references.
2. Contract exactly to the selected sampled section variables.
3. Decompose the exact density action into all interaction scopes.
4. Project onto the PIFB2 operator basis and retain
   \(S_h^{\rm exact}=S_h^{\rm PIFB}+\varepsilon_h+c_h\).
5. Prove a residual bound uniform on bounded-energy sublevels.
6. Use cell weights \(h^d\) for pointwise sectors, transmissibilities \(h^{d-2}\) for base-edge
   Fisher terms, and compact Wilson weights \(h^{d-4}\) for plaquettes.
7. Prove equicoercivity modulo gauge, liminf, recovery, support/boundary convergence, and topology
   control. This establishes a deterministic action limit.
8. Only then attempt the stronger process-law limit: common Polish embedding, tightness,
   reference-law and partition convergence, and relative-entropy liminf/recovery.

## 5. Replacement-code milestone sequence

The new ELBO–PIFB2 codebase should be built only after the following interfaces are frozen:

1. probability types and reference measures;
2. fast/slow update semantics;
3. transport direction and source-label semantics;
4. compact group representation and gauge action;
5. exact normalization/entropy ledger;
6. lattice weights and boundary conventions;
7. retained operator basis plus residual diagnostics.

MAgent should be used for qualitative comparison and test-vector generation, never as the
mathematical oracle. The finite-\(N\), lagged-source probability theorem is now the specification
for the first replacement milestone; implementation remains to be done. That implementation
should start with compact \(G\le GL(K)\), both transported channels, explicit source-label
entropies, and the correlated \(\zeta_i\) correction. The second milestone should implement
configuration-law contraction and operator-residual accounting. The third should test lattice
refinement. The full \(GL(K)\) and thermodynamic-\(N\) programs come afterward.

## Closure boundary

Established now: the typed distinction between fast recognition section \(q\), slow generative-
model section \(s\), and likelihood kernel \(L\); the normalized finite tied-replica witness; the
exact two-channel lagged ELBO identity; its mutual-information correction and mean-field
specialization; finite-horizon iteration; passive gauge invariance; the exact profiling identity;
and compact-subgroup reduction by invariant inner product. Open: same-time reciprocal emergence
from a fixed microscopic law, nonunit-temperature realization, adiabatic validity, vanishing PIFB
residual, deterministic full gauge-field convergence, continuum process-law ELBO, and a coercive
normalized full-\(GL(K)\) theory.
