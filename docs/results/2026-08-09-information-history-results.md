# Session 4 information-history results

## Scope and configuration

This result is a finite CPU/float64 implementation check for the immutable
`two_scale_application_v1` application. The validated application ID is
`30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd`; the
physical fixture-file SHA-256 is
`a207eba1e9f3a36e80d809940405dce178f20c52dffc2482bbc24f4fc26df567`.
Structural fixture validation does not by itself certify every application
premise.

The click-to-run configuration used `experiment="information_history"`,
`fixture="two_scale_application_v1"`, `family="categorical_softmax"`, 16 saved
history points, step size `0.05`, seed `20260809`, and the frozen float64
numerics. The configuration SHA-256 was
`b782727d0d3f5a75360131bc1b0a77c60109974e6f8bf9762fbc100b72bd782e`.
The sanitized launcher run was published under the ignored lane evidence tree
at
`.verification/information-history/fix-round1-launcher-final/artifacts/information_history/b782727d0d3f5a75360131bc1b0a77c60109974e6f8bf9762fbc100b72bd782e-20260809`.

## Declared finite model

The fine family is the open four-dimensional softmax chart whose sufficient
statistics are the four binary coordinates of the 16 fine labels. Its VFE is
the KL divergence from that family member to the fixture posterior. The
coarse comparison family is a separate open two-dimensional softmax chart on
the four coarse labels. The fixture declares its block-average matrix `A` on
probability coordinates, not natural coordinates. The implemented comparison
therefore sends fine natural parameters through
`theta -> p(theta)=E_theta[T]=sigmoid(theta) -> A p(theta) -> logit(A
p(theta))`; the final log odds are the coarse natural parameters `C(theta)`.
Its target is the fixed-channel pushforward of the fine posterior.
Fine and coarse VFE gradients and Fisher matrices are therefore computed in
the same declared family and chart on each side of the comparison.

The fixed Markov channel is used separately for the score-projection and
Fisher-loss identities. The coarse comparison vector field is not identified
with that pushed score family. The exact vector-field comparison stored at
every history point is

`D_semiconj = dC_theta(v_fine) - v_coarse(C(theta))`.

Every natural-gradient solve uses the Moore-Penrose pseudoinverse on the
identifiable tangent quotient and records rank, nullity or rank loss,
positive-spectrum conditioning, and the covector range residual. The
implementation never calls an ordinary inverse for this purpose.

The saved derivative is the state-dependent Jacobian
`dC_theta = diag(1 / (A p * (1 - A p))) A F_fine(theta)`. Thus the fixture
probability-coordinate matrix is never applied directly to a natural
parameter or natural-gradient vector.

## Numerical metrics

| Metric | Value | Tolerance | Status | `theorem_status` | `verification_state` | `claim_origin` |
|---|---:|---:|---|---|---|---|
| `score_finite_difference_residual` | `4.03577726793003e-11` | `1.01e-8` | pass | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` |
| `fisher_defect_residual` | `8.32667268468867e-17` | `1.01e-10` | pass | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` |
| `natural_gradient_range_residual` | `5.55111512312578e-17` | `1.01e-10` | pass | `HYPOTHESIS` | `EVIDENCE_VERIFIED` | `APPLICATION_SPECIFIC` |
| `arc_length_reparameterization_residual` | `0` | `1.01e-10` | pass | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` |
| `semiconjugacy_defect_norm` | `0.5440411403038589` | `1e-6` detection threshold | pass | `OPEN` | `INCONCLUSIVE` | `PROJECT_NOVEL` |

The last metric passes because the registered negative control detects
nonintertwining. It does not claim that semiconjugacy holds. Across the saved
history, defect norms ranged from `0.5163724693809197` to
`0.5440411403038589`; the largest entrywise Jacobian change between the first
and last saved points was `0.013773205418011858`.

The fine Fisher rank was four at every saved point. The fixed-channel pushed
Fisher rank was two, while the independently declared coarse-family Fisher
rank was two. Maximum positive-spectrum condition numbers were approximately
`1.03910`, `4.92129`, and `1.01667`, respectively. These finite diagnostics do
not establish conditioning outside the saved orbit.

The final Fisher information duration of the saved fine history was
`0.4188028623634348`. The inference-orbit parameter, RG depths `[0, 1]`,
information duration, and measured wall time are stored as separate fields or
provenance records; RG depth and Fisher duration are not interpreted as
physical time.

## Independent controls

The parameter-dependent-channel boundary witness has a conditional-expected
score of zero but an actual coarse score `(1/2, -1/2)` at the pinned point. Its
observed gap was `0.4999999999921733`. This is outside the fixed-channel score
theorem and is not a theorem refutation.

The redundant-statistic Fisher control had rank one in a two-coordinate
chart. Its Moore-Penrose range residual was exactly zero, and the saved arrays
reproduce `F v = -dF`. A separate literal two-coordinate channel control has
one recoverable direction but not pointwise full-matrix Fisher equality; no
global statistical-experiment recovery is inferred from either pointwise
calculation.

Two categorical histories with identical endpoints had midpoint-polygonal
Fisher durations `0.49585165802515613` and `1.2918882704080712`. Thus endpoints
do not determine the realized duration. Under a linear chart scaling by two,
the transformed path is `eta=2 theta`, its orientation-preserving Jacobian is
`2 I`, and the transformed Fisher tensors are `F_eta=F_theta/4`. The two
independent chart calculations both gave duration `0.4188028623634348`, while
the pinned omitted-pullback mutation gave `0.8376057247268696`. The pinned
wrong-plus-sign semiconjugacy mutation missed its literal minus-sign oracle by
`1.5`.

## Artifact and runtime record

The finalized run contains exactly the seven registered NPZ artifacts plus the
standard `metrics.json`, `config.json`, and `manifest.json`. The artifacts save
fine, pushed, and independent coarse scores; Fisher matrices, defect and rank
diagnostics; VFE gradients; quotient natural-gradient fields; both chart
paths, segment tensors, and the omitted-pullback mutation; and all probability
coordinates, state-dependent Jacobians, and typed semiconjugacy vectors needed
to recompute the five metrics.

The representative sanitized run used `C:\Python314\python.exe`, Python
3.14.4, NumPy 2.4.4, and SciPy 1.17.1. Numerical work took
`0.08269470000050205` seconds and reached `115807` bytes of peak Python memory
as measured by `tracemalloc`. The manifest binds base Git revision
`b80df01f239c2f9a18842f6887cdeca67dff508f`, dirty-tree digest
`7a694ff970d029161d524401341865378323e1a2d4bd29b5a128b0506395cf5c`,
theory digest
`a7fddfcb8c67dbec71c7a35d0e415313a38154719e05d6ccd73672a810939343`,
the fixture hash, resolved configuration hash, dependencies, and all named RNG
spawn keys. Result documentation was written after this numerical run and is
not part of that prepublication dirty-tree digest.

## Claim, evidence, and falsifier table

| Claim | `theorem_status` | `verification_state` | `claim_origin` | Evidence type | Falsification condition |
|---|---|---|---|---|---|
| Analytic finite-softmax scores agree with centered finite differences on the saved orbit. | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Float64 implementation check plus literal score oracles | A validated score residual exceeds `1.01e-8`. |
| The fixed-channel Fisher defect is conditional score covariance. | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Analytic contraction and independently saved matrix terms | A validated residual exceeds `1.01e-10` or the defect violates its PSD tolerance. |
| The declared quotient rule is compatible with the saved VFE covectors. | `HYPOTHESIS` | `EVIDENCE_VERIFIED` | `APPLICATION_SPECIFIC` | Range residuals plus a rank-deficient control | A saved covector has range residual above `1.01e-10`, or the implementation uses an undeclared inverse/regularizer. |
| Fisher polygonal length is unchanged by the registered orientation-preserving linear chart change. | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Distinct path coordinates, explicit Jacobian, transformed segment tensors, and an omitted-pullback mutation | The two independently recomputed durations differ beyond tolerance, or the mutation is not detected. |
| The fixture coarse map automatically semiconjugates the independently recomputed natural-gradient fields. | `OPEN` | `INCONCLUSIVE` | `PROJECT_NOVEL` | The observed nonzero defect is evidence against this instance, not a universal theorem | A future declared compatible construction proves and numerically reproduces zero defect throughout its stated domain. |

## Explicitly unresolved or not claimed

The run does not establish DQM for an arbitrary family, parameter independence
for a fitted channel, global or automatic semiconjugacy, full statistical
experiment recovery from one parameter, canonical pullback geometry,
intrinsic scale selection, continuum or thermodynamic limits, universality,
Gaussian attraction, a fixed-point theorem, physical time, or a physical law.
The midpoint polygonal arc length is a finite saved-history construction; it is
not a proof about continuum trajectories. No renderer is exposed by this lane.
