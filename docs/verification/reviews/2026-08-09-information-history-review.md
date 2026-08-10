# Independent self-review: Session 4 information histories

## Review disposition

The Session 4 implementation is suitable for integration against the frozen
Wave-0 interfaces. It remains a finite, application-specific laboratory. The
strongest supported result is that the implementation reproduces the declared
finite categorical score, fixed-channel Fisher-loss, quotient solve, duration,
and vector-field-defect calculations. Automatic semiconjugacy is not supported:
the registered fixture produces a clearly nonzero defect.

## Contract and ownership review

The launcher is a no-argument Python file with editable `RUN`, `THEORY`,
`NUMERICS`, and `OUTPUT` dictionaries. It adds the repository `src` directory
to `sys.path`, so a sanitized subprocess launched from a temporary directory
does not require an editable install or inherited `PYTHONPATH`. The exact
theory defaults, seven artifact names, five metric names, and uppercase claim
metadata vocabularies match the frozen registry.

The implementation consumes the existing `ExperimentConfig`, `RunStore`,
provenance, metric, categorical-family, fixed-channel Fisher, and fixture
validator interfaces without modifying them. It rejects rendering rather than
inventing a renderer. Validation of the discriminator, render boundary,
fixture digest, application ID, family construction, and complete numerical
history occurs before RNG creation or artifact-directory publication.

## Mathematical and numerical review

The fine and coarse VFE gradients use the KL objective for the exact family and
chart whose Fisher matrix preconditions the covector. Natural-gradient vectors
use `numpy.linalg.pinv` with the declared numerical reciprocal-condition
threshold. Rank-deficient behavior is exposed through rank, nullity,
positive-spectrum condition number, projector, and range-residual records.
There is no `numpy.linalg.inv` call in the Session 4 source.

The fixed-channel score/Fisher calculation uses the immutable fixture kernel.
Its finite-difference pushed score is computed by perturbing the fine family
and pushing through the same kernel; the conditional score and covariance are
computed analytically. The separate parameter-dependent control makes the
omitted channel-derivative term visible and is explicitly classified as an
assumption-boundary witness.

The typed semiconjugacy calculation uses the required minus sign. A literal
oracle catches a pinned plus-sign mutation. The fixture `2 x 4` matrix is typed
on probability coordinates, so the implementation first computes the fine
marginals `p(theta)`, applies the block average `A p(theta)`, and converts the
result to coarse log odds. Its analytic Jacobian
`diag(1/(A p * (1-A p))) A F_fine(theta)` is nonconstant and agrees with an
independent centered-difference oracle as well as a rational literal oracle at
a pinned point. The independently recomputed coarse field is not conflated
with the fixed-channel pushed score family. The run stores the probability
coordinates, Jacobian, `dC_theta(v_fine)`, and `v_coarse(C(theta))`, so the
defect is directly recomputable.

Fisher duration is evaluated on the saved polygonal history using the metric at
each parameter-segment midpoint. The registered comparison uses genuinely
different chart coordinates: `eta=2 theta`, Jacobian `2 I`, and transformed
metric `F_eta=F_theta/4`. Both chart paths and both segment-metric arrays are
saved and independently recomputed in tests. Omitting the inverse-Jacobian
factors doubles the duration, so the control is mutation-sensitive rather than
tautological. The same-endpoint detour control confirms that this duration is
path-dependent. These are finite numerical constructions, not a continuum
quadrature theorem or a physical-time interpretation.

## Test and evidence review

The strict TDD RED record at `.verification/information-history/red.xml`
contains 19 tests, 19 expected failures, zero errors, and zero skips because the
two Session 4 modules did not exist. A second RED record at
`controls-red.xml` fails on the first missing required control field. The
corresponding GREEN records pass.

The round-one focused JUnit record contains 23 tests, zero failures, zero
errors, and zero skips in 2.799 seconds. Branch-aware coverage reported 93.04%
line and 56.41% branch coverage for `information_history.py`, 96.77% line and
68.75% branch coverage for `information_history_experiment.py`, and 93.65%
line and 58.51% branch coverage in combination. The final full-suite JUnit
record contains 463 tests, zero failures, zero errors, and two skips in 25.693
seconds (461 passed).

An initial coverage command targeted both modules by import name and hit a
Python 3.14/NumPy collection error (`cannot load module more than once per
process`). A path-scoped rerun executed the tests, but the repository-wide
`fail_under` then included unrelated unexercised finite modules. The final
ignored lane coverage configuration restricts reporting to the two owned
production modules and preserves branch measurement. This tooling issue did
not affect ordinary focused or full-suite execution.

## Claim, evidence, and falsifier review

| Claim | `theorem_status` | `verification_state` | `claim_origin` | Evidence reviewed | Falsifier or open obligation |
|---|---|---|---|---|---|
| Saved analytic scores implement the declared smooth finite families. | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Literal softmax score/Fisher values and centered finite differences | A literal or finite-difference check exceeds its threshold after chart validation. |
| Fixed-channel Fisher information contracts by conditional covariance. | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Saved fine, pushed, and defect matrices; literal `diag(1/15, 1/14)` oracle | A current fixed-channel residual or PSD check fails under the theorem premises. |
| Moore-Penrose quotient solving is valid for this saved application. | `HYPOTHESIS` | `EVIDENCE_VERIFIED` | `APPLICATION_SPECIFIC` | Full-rank history plus rank-one redundant-statistic negative control | Nonzero range incompatibility, rank misclassification, or use of an undeclared regularization. |
| The finite duration control is chart invariant. | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Distinct chart paths, covariantly transformed segment tensors, and an omitted-pullback mutation | Nonzero transformed-duration residual or failure to distinguish the mutation. |
| The fixture fields are semiconjugate. | `OPEN` | `INCONCLUSIVE` | `PROJECT_NOVEL` | Coordinate-correct defect norm between `0.51637` and `0.54404`; literal/finite-difference Jacobian and wrong-sign oracles | A separately justified objective/metric/coarse-map compatibility theorem plus zero-defect evidence on its declared domain. |

## Concerns and boundaries

The independently declared coarse family is a transparent application choice,
not a canonical meta-agent geometry. Its nonzero defect cannot be generalized
to every possible coarse family, mobility, or comparison map. Conversely, the
fixed-channel Fisher contraction cannot be transferred to the independently
optimized coarse flow without semiconjugacy.

Pointwise Fisher equality, directional score recovery, and full statistical
experiment recovery remain distinct. The implementation diagnoses the first
two but makes no global recovery claim. The fixture validator establishes
structure and identity, not every theorem premise. Continuum theory,
universality, automatic sparse closure, intrinsic scale selection, canonical
pullback geometry, physical time, and physical law remain `OPEN` or are not
claimed.

No frozen-interface change or integration-only request was needed.
