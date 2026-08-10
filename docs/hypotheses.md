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
  spectrum are established coordinate identities under their typed hypotheses. The finite
  laboratory checks componentwise finite relabeling; the Gaussian laboratory checks the
  declared regular symmetric-definite inverse-congruence fixture.
- **Prediction:** Coherent relabeling of every finite measure, channel, product reference, and
  action preserves evidence, KL, VFE, conditional-KL loss, and reconstruction, and intertwines
  the retained projection. Matched Gaussian inverse congruence preserves quadratic energy and
  the generalized spectrum of a regular symmetric-definite pencil.
- **Null:** Any coherently transformed observable or intertwining square has a residual beyond
  tolerance.
- **Operationalization:** The finite laboratory records the maximum finite
  invariant/intertwining residual as `GAUGE_finite_relabeling_residual`. The Gaussian
  laboratory separately records `GAU-01_energy_residual`,
  `GAU-01_laplacian_energy_residual`, `GAU-01_generalized_spectrum_residual`,
  `GAU-01_eigenpair_residual`, `GAU-01_metric_orthogonality_residual`,
  `GAU-01_commuting_square_residual`, and literal determinant/ordinary-spectrum
  oracle residuals.
- **Control:** Exact source/target permutation matrices and axiswise product permutations;
  relabeling recognition alone is pinned to KL delta `-0.04054651081081644`. The Gaussian
  quadratic energies are pinned to `149/5` and `34/5`, while the ordinary-spectrum change
  under a nonorthogonal frame is retained as a negative control rather than mislabeled as an
  invariant. The commuting-square fixture pins the transformed prolongator and the coarse
  precisions `diag(6,8)` and `diag(6/25,2)`.
- **Support threshold:** Every finite residual is at most `atol + rtol`; every Gaussian
  residual satisfies its preregistered matrix tolerance and each negative control remains
  separated from zero by more than that tolerance.
- **Refutation threshold:** A coherent typed transform exceeds tolerance after all dimensions,
  orientations, and regularity assumptions are verified.
- **Inconclusive rule:** Arbitrary gauge fields, holonomy, singular pencils without a declared
  repair, or unmatched transformations are outside the identity and therefore inconclusive.
- **Theory source pointer:** `Theory/07b_agent_network_rg.tex`, finite Hoeffding gauge
  covariance; `Theory/08_infogeometry.tex`, generalized-spectrum congruence invariance.

## GAU-02 — Gaussian Galerkin aggregation under a declared family

- **Epistemic status:** Internal-edge cancellation and cut-weight addition are established
  conditional identities for the declared matrix-weighted Gaussian interaction family. The
  declaration that a modeled system belongs to that family is a hypothesis. The current
  Gaussian laboratory is an implementation check of the declared literal fixtures, not an
  empirical family-membership result.
- **Prediction:** Hard-identification/Galerkin restriction annihilates internal edge energies,
  adds cut weights, and adds the declared self terms; it is not a Gaussian marginal.
- **Null:** The coarse precision differs from the independently assembled cut/self precision.
- **Operationalization:** Compare `S.T @ Lambda @ S` with the literal coarse operator and record
  `GAU-02_galerkin_residual`; separately record the Schur-complement distinction, scalar Schur
  oracle, matrix-valued Schur oracle, and unrestricted-Kron nonclosure metrics.
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

## ATT-01 — Marked-event factorization and normalization

- **Epistemic status:** Established conditional finite-law identity; the current laboratory is
  an implementation check of one frozen deterministic fixture.
- **Prediction:** On every positive state and active receiver row, the joint marked-event law
  satisfies `eta = alpha * beta`; state-conditional event masses, receiver occupancies, and
  active source rows normalize, while inactive representatives remain zero.
- **Null:** A factorization or normalization residual exceeds its scale-aware tolerance.
- **Operationalization:** Record `ATT-01_factorization_residual` and
  `ATT-01_normalization_residual` over the saved fine, intermediate, direct-coarse, and
  staged-coarse laws.
- **Control:** Frozen `nested_nonuniform_v1` state probabilities and the explicit zero-occupancy
  row convention; constructor validation rejects nonnormalized or nonzero inactive rows.
- **Support threshold:** Both residuals are at most `atol + rtol * scale` and every stored law is
  finite and normalized on its declared support.
- **Refutation threshold:** Either residual exceeds its tolerance after the support masks,
  partitions, and saved arrays are validated.
- **Inconclusive rule:** A malformed law, incomplete artifact, undefined conditional on a null
  receiver, or a changed undeclared fixture is inconclusive about the general identity.
- **Theory source pointer:** `Theory/07b_agent_network_rg.tex`, Section "Exact attention between
  meta-agents," especially Equations `rg-attention-event-law` and `rg-meta-attention`.

## ATT-02 — Associative joint-law attention coarsening

- **Epistemic status:** Established conditional identity for normalized marked-event laws and
  nested Markov/node partitions; the registered run is a literal implementation check.
- **Prediction:** Direct and staged pushforward produce the same final `eta`, receiver
  occupancy `alpha`, active-row `beta`, and posterior reverse bridge, and agree with the frozen
  rational oracle.
- **Null:** Any direct/staged, literal-oracle, or reverse-bridge residual exceeds tolerance.
- **Operationalization:** Use every `ATT-02_*_residual` metric: direct/staged `eta`, `alpha`, and
  active `beta`; literal `eta`, `alpha`, and active `beta`; and the reverse bridge.
- **Control:** Explicit fine-to-middle, middle-to-coarse, and composed state/node kernels in
  `nested_nonuniform_v1`, with direct rational expectations computed independently.
- **Support threshold:** Every `ATT-02_*_residual` is at most `atol + rtol * scale`.
- **Refutation threshold:** A validated direct/staged or literal residual exceeds that bound.
- **Inconclusive rule:** Noncomposable kernels, changed partitions, invalid probability laws,
  nonfinite arrays, or comparison of inactive conditional rows makes this fixture inapplicable.
- **Theory source pointer:** `Theory/07b_agent_network_rg.tex`, Equation `rg-meta-attention` and
  the tower-property statement that joint-law pushforward, then disintegration, is associative.

## ATT-03 — Scalar gauge invariance after covariant recomputation

- **Epistemic status:** Established scalar gauge identity under coherent endpoint/frame
  transformations; the `GL+(2)` fixture is a finite metamorphic implementation check.
- **Prediction:** Coherent recomputation preserves occupancy/source logits, `alpha`, `beta`, and
  scalar `eta`; leaving the links untransformed produces a detectable nonzero gap.
- **Null:** A coherent residual exceeds tolerance or the broken-link gap collapses.
- **Operationalization:** Record `ATT-03_gauge_logits_residual`,
  `ATT-03_gauge_alpha_residual`, `ATT-03_gauge_beta_residual`,
  `ATT-03_gauge_eta_residual`, and `ATT-03_broken_link_gap_control`.
- **Control:** Frozen nonorthogonal positive-determinant local frames, correctly transformed
  vectors/covectors/links, and a matched broken-link negative control.
- **Support threshold:** All four coherent residuals are at most `atol + rtol * scale`, and the
  broken-link gap is greater than `1e-3` beyond numerical tolerance.
- **Refutation threshold:** A coherent residual exceeds tolerance after dimensions and endpoint
  orientations are verified, or the registered broken-link control is not detectably nonzero.
- **Inconclusive rule:** Singular/wrong-orientation frames, unmatched endpoint conventions,
  arbitrary connections or holonomy, or a different scoring map are outside this metamorphic.
- **Theory source pointer:** `Theory/07b_agent_network_rg.tex`, Section "Exact attention between
  meta-agents," where marked-event probabilities are gauge-invariant scalars.

## ATT-04 — Finite relabeling naturality

- **Epistemic status:** Finite relabeling naturality check; it does not assert invariance under
  an incoherent change of only one typed component.
- **Prediction:** A coherent cyclic relabeling of `eta` and both node partitions intertwines the
  coarse pushforward, while relabeling `eta` alone remains detectably different.
- **Null:** The coherent residual exceeds tolerance or the incoherent mismatch collapses.
- **Operationalization:** Record `ATT-04_relabeling_naturality_residual` and
  `ATT-04_incoherent_relabeling_gap_control`.
- **Control:** Frozen cyclic permutation with receiver and source partition kernels transformed
  in the same direction; the negative control keeps those kernels fixed.
- **Support threshold:** Coherent residual at most `atol + rtol * scale`; incoherent gap greater
  than `1e-3` beyond tolerance.
- **Refutation threshold:** The coherent square fails after permutation directions and partition
  labels are checked, or the frozen negative control becomes indistinguishable.
- **Inconclusive rule:** Duplicate labels, nonbijective maps, mismatched source/receiver types,
  or an undeclared relabeling action lies outside the finite naturality claim.
- **Theory source pointer:** `Theory/07b_agent_network_rg.tex`, typed node partitions and the
  joint marked-event pushforward in Equation `rg-meta-attention`.

## ATT-NEG-01 — Beta-only nonassociativity control

- **Epistemic status:** Deliberately incorrect coarse-graining control, not a candidate theorem.
- **Prediction:** Equal-row averaging of normalized `beta` without receiver occupancy has a
  direct/staged gap `1/10` and direct-versus-correct joint-law gap `1/20` in the frozen fixture.
- **Null:** Either pinned gap is indistinguishable from zero or misses its rational target.
- **Operationalization:** Record `ATT-NEG-01_beta_only_associativity_gap` and
  `ATT-NEG-01_beta_only_correct_gap`.
- **Control:** Apply the wrong rule to the same nested partitions used by ATT-02 so only omission
  of `alpha` distinguishes it from the exact construction.
- **Support threshold:** The gaps equal `1/10` and `1/20`, respectively, within
  `atol + rtol * scale`.
- **Refutation threshold:** A frozen-fixture gap misses its target after the wrong rule and
  rational oracle are independently checked.
- **Inconclusive rule:** A changed fixture can have different or accidentally zero gaps; without
  a preregistered literal target it is diagnostic rather than pass/fail evidence.
- **Theory source pointer:** `Theory/07b_agent_network_rg.tex`, Section "Exact attention between
  meta-agents," which requires pushing `eta`, not `beta` alone.

## DQM-01 — Positive categorical-family DQM and numerical corroboration

- **Epistemic status:** Analytically established for the declared smooth positive finite
  exponential family by a finite-support Taylor derivation; finite differences and the
  remainder ladder are separate numerical implementation checks.
- **Prediction:** Probabilities normalize, analytic scores center, centered finite differences
  reproduce the analytic score, and both default normalized two-sided remainder sequences
  decrease toward zero.
- **Null:** The analytic finite-support Taylor argument fails for the declared family, or an
  implementation residual/default ladder check violates its registered threshold.
- **Operationalization:** Record all `DQM-01_*` metrics, including literal probability/score
  residuals at `theta=(log 2, log 3)`, analytic/FD error, final normalized remainder, and
  positive/negative ladder monotonicity.
- **Control:** Three positive softmax categories with zero base logits, statistics
  `((1,0),(0,1),(0,0))`, direction `(3/5,-4/5)`, FD step `1e-5`, and ladder
  `(0.1,0.05,0.025,0.0125)`.
- **Support threshold:** The analytic finite-support derivation supplies the DQM proof;
  normalization, centering, FD, and literal residuals meet scale-aware tolerances; the final
  normalized remainder is at most `0.0125`; both default ladders strictly decrease.
- **Refutation threshold:** A counterexample to positivity/smooth Taylor expansion refutes the
  family claim. A failed FD/ladder threshold refutes only the numerical implementation check.
- **Inconclusive rule:** Nonpositive support, invalid perturbations, nonfinite values, an edited
  theta/ladder without frozen monotonicity thresholds, or numerical cancellation is inconclusive
  about DQM.
- **Theory source pointer:** `Theory/07b_agent_network_rg.tex`, Definition `rg-dqm-score`;
  `Theory/06_general_coarsegraining.tex`, Theorem `cg-fisher-contraction`. The family-specific
  Taylor derivation is recorded in the approved design document.

## INF-02 — Conditional score and categorical Fisher loss

- **Epistemic status:** Established conditional identity for a DQM family and a declared-fixed,
  normalized, parameter-independent Markov channel; the run is an implementation check.
- **Prediction:** The coarse score is the fine score's conditional expectation, agrees with an
  independently pushed centered-FD score, and satisfies `I_fine - I_coarse = E Cov(score|Z)`
  with a PSD, detectably positive defect in the frozen lossy fixture.
- **Null:** The conditional-score/FD or Fisher residual exceeds tolerance, the defect has an
  eigenvalue below its negative tolerance, or the positive-loss control collapses.
- **Operationalization:** Record `INF-02_conditional_score_fd_residual`,
  `INF-02_fisher_identity_residual`, `INF-02_fisher_defect_min_eigenvalue`,
  `INF-02_positive_loss_trace_control`, and the default literal coarse/Fisher residuals.
- **Control:** Frozen `3 x 2` channel, independent pushed finite differences, rational coarse
  probability/score/Fisher tensors, and defect `diag(1/15,1/14)`.
- **Support threshold:** Score and matrix residuals meet scale-aware tolerances; minimum defect
  eigenvalue is within its PSD allowance; loss trace exceeds tolerance; literal residuals pass.
- **Refutation threshold:** An identity/PSD threshold fails after DQM, score centering, channel
  normalization, and parameter-independence are established.
- **Inconclusive rule:** The kernel object records but cannot prove independence across theta;
  an uncentered score, parameter-dependent channel, absent DQM evidence, or invalid law is
  inconclusive about the theorem.
- **Theory source pointer:** `Theory/06_general_coarsegraining.tex`, Theorem "Score projection
  and Fisher loss," Equations `cg-score-projection` and `cg-fisher-loss`.

## INF-NEG-01 — Unweighted coarse-score control

- **Epistemic status:** Deliberately incorrect weighting control.
- **Prediction:** Column-normalized kernel weights without fine-law mass differ from the correct
  conditional score by sup norm `4/21` at the default fixture.
- **Null:** The wrong-weight gap collapses to zero or misses `4/21` beyond tolerance.
- **Operationalization:** Record `INF-NEG-01_wrong_weight_gap` at the frozen default; edited
  theta emits only `INF-NEG-01_wrong_weight_gap_diagnostic` with inconclusive status.
- **Control:** Compare the wrong score against the conditional-expectation score while holding
  the fine law, analytic score, and channel fixed.
- **Support threshold:** Default gap equals `4/21` within `atol + rtol * scale`.
- **Refutation threshold:** The frozen default gap misses that rational oracle after both weight
  formulas are independently evaluated.
- **Inconclusive rule:** At edited theta there is no preregistered rational target; the gap is
  diagnostic and cannot be promoted to a pass/fail claim.
- **Theory source pointer:** `Theory/06_general_coarsegraining.tex`, Equation
  `cg-score-projection`, which uses joint-law conditional weights.

## RG-01 — Attraction or universality of scalarized Gaussian rays

- **Epistemic status:** Conjectural/open and explicitly deferred. No Task 3 or Task 4 finite run
  can verify a universal claim.
- **Prediction:** Within a separately declared basin and comparison scheme, normalized coarse
  Gaussian operators approach a scalarized ray with decreasing angular and normalized-distance
  residuals across scales.
- **Null:** Residuals do not decrease, depend materially on blocking scheme, or converge to
  distinct rays under admissible initial conditions.
- **Operationalization:** Future multi-seed, multi-scheme trajectories of ray angle, normalized
  distance, scalarized-ray construction residual, and scheme dispersion with fixed preregistered
  scale windows. The construction residual is a roundoff consistency diagnostic, not an
  unrestricted-dynamics endpoint.
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

## Six-session buildout registry supplement

The following experiment-level entries bind the seven frozen laboratory
discriminators to their claim boundary. Exact metric names, artifact inventories,
fixtures, and thresholds are frozen in
`docs/superpowers/specs/2026-08-09-six-session-laboratory-contract.md`; the lane
result records contain the realized values. A passing finite run closes only the
named implementation or fixture claim.

### BUILD-01 — Multi-agent network application

- **Epistemic status:** Exact finite application identities are established under
  the checked premises; consensus, frustration, and higher-order interpretations
  outside the fixture remain hypotheses.
- **Prediction:** The frozen application tuple preserves evidence, reconstructs the
  Hoeffding action, and matches the declared local/collective and recognition-lift
  identities.
- **Null and controls:** Any registered residual exceeds its exact or scale-aware
  bound; the overlapping-local-objective and recognition-lift mutations must remain
  detectably nonzero.
- **Inconclusive rule:** A changed application digest, failed premise, unsupported
  scenario, or incomplete artifact prevents application-level closure.
- **Current state:** The lane record reports passing CPU fixture checks.
  Integration-wide verification state is assigned only by the validated live
  final-SHA ledger, not by this registry.

### BUILD-02 — Independent theory oracles

- **Epistemic status:** Standard finite identities with independent exact-arithmetic
  derivations; agreement is an implementation check, not a new theorem.
- **Prediction:** Production ELBO, Fisher-defect, Gaussian linear-algebra,
  Hoeffding, and marked-event values agree with independently constructed oracles.
- **Null and controls:** A production/oracle residual exceeds its registered bound;
  literal commuting-diagram mutations must be rejected or remain separated.
- **Inconclusive rule:** A missing theorem premise, changed frozen application, or
  incomplete exact numerator/denominator record prevents closure.
- **Current state:** The lane record reports passing results for all five CPU
  oracles. Integration-wide verification state is assigned only by the validated
  live final-SHA ledger.

### BUILD-03 — Minimal finite counterexamples

- **Epistemic status:** Explicit in-domain witnesses can refute an overbroad claim;
  bounded enumeration cannot prove the absence of other counterexamples.
- **Prediction:** The pinned catalog exhibits support failure, marked-event source
  mismatch, parameter-dependent-channel score failure, relabeling mismatch, and
  pairwise-truncation failure within the declared bounds.
- **Null and controls:** A witness collapses, is not minimal under the frozen search
  order, or fails exact rational replay; relabeling and retained-order metamorphics
  guard catalog construction.
- **Inconclusive rule:** Search outside the enumerated state/denominator bounds or a
  changed ordering rule is not covered by the catalog.
- **Current state:** The lane record reports five replayable finite witnesses.
  Integration-wide verification state is assigned only by the validated live
  final-SHA ledger.

### BUILD-04 — Information histories

- **Epistemic status:** Fisher pullback and range identities are established under
  their regularity premises; the finite history and semiconjugacy values are
  application-specific numerical diagnostics.
- **Prediction:** Analytic and finite-difference scores agree, Fisher defects and
  natural-gradient range residuals meet tolerance, information duration is chart
  invariant, and the declared semiconjugacy defect remains measurable.
- **Null and controls:** Any identity residual exceeds tolerance; rank-deficient,
  sign-mutation, and same-endpoint path controls must retain their registered
  separation.
- **Inconclusive rule:** Rank, support, smoothness, or comparison-map premise failure
  makes the corresponding identity inapplicable rather than refuted.
- **Current state:** The lane record reports passing deterministic CPU history
  checks. Integration-wide verification state is assigned only by the validated
  live final-SHA ledger.

### BUILD-05 — Gauge holonomy and operational records

- **Epistemic status:** Finite graph-link covariance and conjugacy statements are
  established under typed frame changes; physical or continuum interpretation is
  limited to the declared operational fixture.
- **Prediction:** Passive frame changes preserve the registered observables and cycle
  invariants, flat cases trivialize, and a broken link remains detectably different.
- **Null and controls:** Covariance, conjugacy, or operational residuals exceed their
  bounds; the broken-link control collapses or a nonflat cycle is mislabeled flat.
- **Inconclusive rule:** Ill-conditioned frames, absent comparison data, or a claim
  about continuum connection geometry lies outside this finite experiment.
- **Current state:** The lane record reports the five finite scenarios and controls;
  its own shared-ledger obligation remains distinct. Integration-wide verification
  state is assigned only by the validated live final-SHA ledger.

### BUILD-06 — Exact scale cocycle

- **Epistemic status:** The finite three-level composition and retained-residual
  identities are exact under the frozen extension; generated higher-order values are
  numerical/application-specific.
- **Prediction:** Direct and staged pushforwards, posterior bridges, derivative
  cocycles, and equivalent beta-residual forms agree, while wrong-order and fixed-
  projection mutations remain separated.
- **Null and controls:** Any exact residual is nonzero, the generated triple term
  collapses, or a typed wrong-order mutation is silently accepted.
- **Inconclusive rule:** A changed comparison isomorphism, interaction basis, or
  extension digest requires a new preregistration and evidence run.
- **Current state:** The lane record reports passing CPU scale identities and finite
  generated-interaction diagnostics. Integration-wide verification state is
  assigned only by the validated live final-SHA ledger.

### BUILD-07 — Gaussian fixed-ray pilot and CUDA parity

- **Epistemic status:** Finite CPU trajectories are `NUMERICAL`; attraction and
  universality remain open. CUDA parity is a separate open implementation claim.
- **Prediction:** Within the frozen pilot population, projective angle and normalized
  distance are reported across scales without basin exit, blocking-scheme dispersion
  remains measured, and a float64 CUDA sentinel eventually agrees with the CPU
  controller and worker within the preregistered bound.
- **Null and controls:** Noncommuting blocking schemes must remain distinguishable,
  the commuting mutation must collapse, and an injected parity mutation must fail.
- **Inconclusive rule:** Pilot-only execution, absent CUDA gate, missing operator
  opt-in, an unverified worker/environment hash, or an unrun confirmatory job table
  leaves the CUDA and attraction claims inconclusive.
- **Current state:** The CPU pilot metric records retain their lane-scoped states;
  integration-wide state is assigned only by the validated live final-SHA ledger.
  CUDA parity and confirmatory attraction remain `INCONCLUSIVE`.
  `heavy_sweep_enabled=false` and `confirmatory_executed=false`.
