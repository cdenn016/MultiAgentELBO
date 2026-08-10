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
oracle catches a pinned plus-sign mutation. The independently recomputed
coarse field is not conflated with the fixed-channel pushed score family. The
run stores both `dC(v_fine)` and `v_coarse(C(theta))`, so the defect is directly
recomputable.

Fisher duration is evaluated on the saved polygonal history using the metric at
each parameter-segment midpoint. Relabeling the same vertices leaves this
quantity invariant, and a linear chart test transforms the Fisher metric by the
inverse-square Jacobian. The same-endpoint detour control confirms that this
duration is path-dependent. These are finite numerical constructions, not a
continuum quadrature theorem or a physical-time interpretation.

## Test and evidence review

The strict TDD RED record at `.verification/information-history/red.xml`
contains 19 tests, 19 expected failures, zero errors, and zero skips because the
two Session 4 modules did not exist. A second RED record at
`controls-red.xml` fails on the first missing required control field. The
corresponding GREEN records pass.

The final focused JUnit record contains 21 tests, zero failures, zero errors,
and zero skips in 2.379 seconds. Branch-aware coverage reported 93.43% line
coverage for `information_history.py` and 96.77% for
`information_history_experiment.py`; combined line coverage was 94.07%. The
final full-suite JUnit record contains 461 tests, zero failures, zero errors,
and two pre-existing platform skips in 23.264 seconds.

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
| The finite duration controls are reparameterization invariant. | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Same-vertex relabeling and covariant linear-chart transformation | Nonzero transformed-duration residual for the identical geometric path. |
| The fixture fields are semiconjugate. | `OPEN` | `INCONCLUSIVE` | `PROJECT_NOVEL` | Defect norm between `0.54064` and `0.54537`; wrong-sign mutation oracle | A separately justified objective/metric/coarse-map compatibility theorem plus zero-defect evidence on its declared domain. |

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
