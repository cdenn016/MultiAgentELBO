# Pre-registered hypothesis and implementation-check registry

This registry separates mathematical status from software evidence. A passing finite
test verifies the named implementation against its declared fixture; it does not prove a
universal theorem, establish differentiability in quadratic mean (DQM), verify that a
kernel is parameter-independent across an unexamined family, or establish RG universality.

## FIN-01 — Common-channel evidence preservation

- **Epistemic status:** Established conditional identity; current laboratory is an
  implementation check.
- **Prediction:** Pushing the reference and evidence submeasure through the same normalized
  Markov channel preserves total evidence mass.
- **Null:** The fine and coarse evidence masses differ beyond numerical tolerance.
- **Operationalization:** Record `abs(Z_fine - Z_coarse)` as
  `FIN-01_evidence_residual`.
- **Control:** The literal four-state measure pair and deterministic `A,A,B,B` channel.
- **Support threshold:** Residual at most `atol + rtol` and the current literal-oracle test
  passes.
- **Refutation threshold:** Residual greater than `atol + rtol` after measure and channel
  validation succeeds.
- **Inconclusive rule:** Any invalid measure, nonnormalized kernel, incomplete artifact, or
  nonfinite computation is inconclusive about the theorem and diagnoses the application or
  implementation first.
- **Theory source pointer:** `Theory/06_general_coarsegraining.tex`, normalized
  parameter-independent Markov coarse graining; `Theory/05_elbo.tex`, fixed-evidence VFE.

## FIN-02 — Finite VFE channel chain rule

- **Epistemic status:** Established conditional identity; current laboratory is an
  implementation check.
- **Prediction:** On the finite-support branch, fine VFE equals coarse VFE plus the
  coarse-law-weighted conditional KL loss.
- **Null:** The independently computed chain-rule residual is nonzero beyond tolerance.
- **Operationalization:** Record `fine_vfe - coarse_vfe - conditional_kl` as
  `FIN-02_vfe_chain_residual`; retain the structured extended-real branch separately.
- **Control:** The hand-derived posterior `(0.1,0.2,0.3,0.4)`, recognition
  `(0.2,0.3,0.1,0.4)`, and `A,A,B,B` channel, plus identity-channel and support-violation
  controls.
- **Support threshold:** Absolute finite-branch residual at most `atol + rtol` and agreement
  with the literal scalar oracle.
- **Refutation threshold:** A finite residual greater than `atol + rtol` after all support
  assumptions are verified.
- **Inconclusive rule:** An undefined `inf - inf` branch, failed support assumption, or
  incomplete run is inconclusive about the identity; the implementation must report the
  offending state instead of manufacturing a residual.
- **Theory source pointer:** `Theory/05_elbo.tex`, exact evidence identity and KL chain-rule
  domain; `Theory/06_general_coarsegraining.tex`, common-channel coarse law.

## FIN-03 — Fixed-outside local-to-collective VFE difference

- **Epistemic status:** Established conditional identity; current laboratory is an
  implementation check.
- **Prediction:** When before and after recognition laws have exactly the same outside
  marginal, their collective VFE difference equals the outside-weighted conditional block
  VFE difference.
- **Null:** The local and collective differences disagree beyond tolerance.
- **Operationalization:** Record `local_difference - collective_difference` as
  `FIN-03_block_update_residual`.
- **Control:** The enumerated two-binary-variable posterior and the preregistered before/after
  tables with outside marginal `(0.35,0.65)`.
- **Support threshold:** Absolute residual at most `atol + rtol` and both independently
  computed differences agree with `-0.06702325206172067`.
- **Refutation threshold:** Residual greater than `atol + rtol` with exactly equal outside
  marginals and finite KL terms.
- **Inconclusive rule:** Unequal outside marginals, nonfinite KL, or malformed block axes makes
  this reduced identity inapplicable and therefore inconclusive rather than refuted.
- **Theory source pointer:** `Theory/05b_local_collective_elbo.tex`, posterior block
  disintegration and fixed-outside block KL chain rule.

## INF-01 — Finite Fisher contraction defect

- **Epistemic status:** Established conditional score/covariance identity for a centered
  supplied score and a declared-fixed parameter-independent channel; current laboratory is
  an implementation check and does not establish DQM.
- **Prediction:** Fine Fisher minus coarse Fisher equals independently computed expected
  conditional score covariance, which is positive semidefinite and may be singular.
- **Null:** The matrix identity residual exceeds tolerance or the raw minimum symmetric
  eigenvalue is below its scale-aware negative tolerance.
- **Operationalization:** Record the residual matrix sup norm and raw minimum defect
  eigenvalue as `INF-01_fisher_identity_residual` and
  `INF-01_fisher_defect_min_eigenvalue`.
- **Control:** Uniform deterministic, nonuniform stochastic-weighting, identity-channel,
  genuinely lossy but score-recoverable, zero-tangent, and rank-one singular-PSD fixtures.
- **Support threshold:** Residual at most `atol + rtol * scale`; minimum eigenvalue at least
  `-(atol + rtol * scale)`; all literal values match without clipping, jitter, or Cholesky.
- **Refutation threshold:** A residual or negative eigenvalue outside those bounds after score
  centering, normalization, fixed-kernel applicability, and independent computations are
  confirmed.
- **Inconclusive rule:** An uncentered score, a parameter-dependent channel family, absent DQM
  evidence, or invalid finite law is inconclusive about the statistical-family theorem.
- **Theory source pointer:** `Theory/06_general_coarsegraining.tex`, Markov score
  contraction; `Theory/05c_pullback_geometry.tex`, Fisher defect pullback and contraction.

## INT-01 — Full interaction reconstruction and retained residual

- **Epistemic status:** Complete product-reference Hoeffding reconstruction is an established
  finite identity; sparse/pairwise closure is not automatic. The laboratory checks the
  implementation and exhibits a negative retained-space control.
- **Prediction:** All subset components reconstruct the action exactly, while pairwise
  retention of the four-spin fixture omits theorem-coordinate norm `0.7`, quotient sup norm
  `0.7`, and weighted L2 diagnostic `0.5`.
- **Null:** Full reconstruction has a nonzero residual beyond tolerance, or the discriminating
  retained-control values collapse or are conflated.
- **Operationalization:** Record `INT-01_reconstruction_residual` and the separately named
  theorem-coordinate, quotient-sup, and weighted-L2 metrics.
- **Control:** Pure three-spin interaction, four-spin two-triple fixture, and a nonuniform
  binary product reference that detects accidental uniform averaging.
- **Support threshold:** Reconstruction residual below `1e-12`; retained-control values within
  `atol + rtol` of `0.7`, `0.7`, and `0.5` respectively.
- **Refutation threshold:** Reconstruction residual at least `1e-12` on the literal fixtures,
  or any retained diagnostic differs from its independent oracle beyond tolerance.
- **Inconclusive rule:** A nonproduct or undeclared reference, nonfinite action, or unsupported
  retained order is outside this coordinate theorem and is inconclusive rather than refuting it.
- **Theory source pointer:** `Theory/07b_agent_network_rg.tex`, Hoeffding/Mobius projectors,
  exact action isomorphism, gauge covariance, and retained coordinate/action residuals.

## GAU-01 — Coordinate relabeling and congruence invariants

- **Epistemic status:** Finite Borel relabeling and matched inverse-congruence generalized
  spectrum are established coordinate identities under their typed hypotheses. Task 3 checks
  only componentwise finite relabeling; Gaussian congruence checks are deferred to Task 4.
- **Prediction:** Coherent relabeling of every finite measure, channel, product reference, and
  action preserves evidence, KL, VFE, conditional-KL loss, and reconstruction, and intertwines
  the retained projection. Matched Gaussian inverse congruence preserves quadratic energy and
  the generalized spectrum of a regular symmetric-definite pencil.
- **Null:** Any coherently transformed observable or intertwining square has a residual beyond
  tolerance.
- **Operationalization:** Task 3 records the maximum finite invariant/intertwining residual as
  `GAUGE_finite_relabeling_residual`; Task 4 will record energy, eigenpair, orthonormality, and
  spectrum residuals separately.
- **Control:** Exact source/target permutation matrices and axiswise product permutations;
  relabeling recognition alone is pinned to KL delta `-0.04054651081081644`. The Gaussian
  ordinary-spectrum mismatch control is deferred.
- **Support threshold:** Every finite residual at most `atol + rtol`; later Gaussian residuals
  must satisfy their preregistered matrix tolerances.
- **Refutation threshold:** A coherent typed transform exceeds tolerance after all dimensions,
  orientations, and regularity assumptions are verified.
- **Inconclusive rule:** Arbitrary gauge fields, holonomy, singular pencils without a declared
  repair, or unmatched transformations are outside the identity and therefore inconclusive.
- **Theory source pointer:** `Theory/07b_agent_network_rg.tex`, finite Hoeffding gauge
  covariance; `Theory/08_infogeometry.tex`, generalized-spectrum congruence invariance.

## GAU-02 — Gaussian Galerkin aggregation under a declared family

- **Epistemic status:** Internal-edge cancellation and cut-weight addition are established
  conditional identities for the declared matrix-weighted Gaussian interaction family. The
  declaration that a modeled system belongs to that family is a hypothesis. Implementation
  tests are deferred to Task 4.
- **Prediction:** Hard-identification/Galerkin restriction annihilates internal edge energies,
  adds cut weights, and adds the declared self terms; it is not a Gaussian marginal.
- **Null:** The coarse precision differs from the independently assembled cut/self precision.
- **Operationalization:** Compare `S.T @ Lambda @ S` with the literal coarse operator and record
  block residuals; separately compute the Schur-complement marginal as a negative distinction
  control.
- **Control:** Three scalar nodes with self terms `(1,2,3)`, edge weights `4` and `5`, and
  partition `{0,1}|{2}`; the distinct Schur complement and an unrestricted-Kron nonclosure
  witness prevent mislabeling.
- **Support threshold:** Every coarse block agrees within the configured matrix tolerance and
  the internal first edge cancels while the cut second edge remains.
- **Refutation threshold:** A block residual exceeds tolerance after SPD, partition, and declared
  family validation succeeds.
- **Inconclusive rule:** Failure to establish family membership, invalid SPD inputs, or confusing
  Galerkin restriction with marginalization makes the application inconclusive.
- **Theory source pointer:** `Theory/09_coarsegraining.tex`, hard identification, internal-edge
  cancellation, and cut-edge aggregation; `Theory/06_gaussian.tex`, frame-dependent interaction
  family declaration.

## RG-01 — Attraction or universality of scalarized Gaussian rays

- **Epistemic status:** Conjectural/open and explicitly deferred. No Task 3 or Task 4 finite run
  can verify a universal claim.
- **Prediction:** Within a separately declared basin and comparison scheme, normalized coarse
  Gaussian operators approach a scalarized ray with decreasing angular and normalized-distance
  residuals across scales.
- **Null:** Residuals do not decrease, depend materially on blocking scheme, or converge to
  distinct rays under admissible initial conditions.
- **Operationalization:** Future multi-seed, multi-scheme trajectories of ray angle, normalized
  distance, off-family remainder, and scheme dispersion with fixed preregistered scale windows.
- **Control:** Matched initial spectra outside the proposed basin, alternate blocking schemes,
  and non-scalar matrix-weight witnesses.
- **Support threshold:** To be preregistered before execution; it must require repeatable
  cross-seed attraction and bounded scheme dispersion, not a single monotone trajectory.
- **Refutation threshold:** To be preregistered before execution; a robust nonattracting or
  scheme-dependent counterexample within the declared basin refutes that stated version.
- **Inconclusive rule:** Finite single-seed trends, unverified family closure, missing comparison
  isomorphisms, or an unspecified basin/window are inconclusive.
- **Theory source pointer:** `Theory/10_renormalization.tex`, scalarized restrictions and open
  universality boundary; `Theory/07_general_renormalization.tex`, comparison data and limiting
  obligations.
