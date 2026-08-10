# Shared Scientific Contract Remediation Design

Date: 2026-08-10
Status: approved for implementation planning
Base revision: `d38f24ca506dd37fd74dacd8d2abab3c3175bdc9`

## Purpose

The merged laboratories currently implement several scientific concepts with incompatible conventions. These mismatches are hidden by two-state involutions, diagonal conditioning fixtures, lane-local stress checks, and producer-issued verification labels. This remediation establishes shared scientific contracts while retaining independent laboratory implementations and exact counterexample oracles.

The governing research boundary remains the finite, conditional, two-scale theory described by the existing laboratory contract and Research wiki. The work does not claim a continuum theorem, universality, or CUDA validation.

## Goals

1. Use one explicit permutation convention across finite laws, channels, actions, and gauge relabeling.
2. Use a shared spectral reciprocal-condition policy for SPD conditioning.
3. Make accepted numerical configuration fields affect the decisions they describe.
4. Make required stress controls participate in experiment status.
5. Correct assumption-boundary metadata and reserve `EVIDENCE_VERIFIED` for validated ledgers.
6. Add cross-producer tests that can detect convention drift rather than comparing one implementation with itself.
7. Preserve existing public package import paths where compatibility is practical.

## Non-goals

- Artifact content hashing, tamper detection, Git provenance hardening, or other security work.
- CUDA, GPU parity, continuum constructions, thermodynamic-limit claims, or Gaussian heavy sweeps.
- A general experiment-framework rewrite, registry-dispatch refactor, or performance optimization.
- Unrelated changes to launcher configuration or the user's live launcher WIP.

## Architecture

### Canonical finite permutations

A shared finite-permutation module will define one typed permutation object whose stored public convention is `old_to_new`. It will validate a nonempty bijection, derive `new_to_old`, and provide explicit pullback operations for one-dimensional laws, channel source and target axes, and tensor axes.

The geometry package will re-export this shared type so existing imports of `multiagent_elbo.geometry.FinitePermutation` remain stable. Session-3 helpers will accept the typed permutation internally. Narrow compatibility adapters may accept a tuple only when the parameter name states its convention, such as `old_to_new`; no internal API will accept an unlabeled raw tuple.

The defining three-state fixture is the non-involutive cycle `(1, 2, 0)`. Applying the same typed object through Session 3 and finite-gauge must produce identical laws, channels, and action pullbacks. Composition and inversion must satisfy the group-action law. The existing two-state swap remains a regression case but is not sufficient evidence by itself.

### Shared SPD conditioning assessment

Exact rational code will continue to establish symmetry and positive definiteness before any floating-point conditioning computation. Conditioning will then use the spectral reciprocal condition

$$
r_{\mathrm{cond}}(A)=\lambda_{\min}(A)/\lambda_{\max}(A)
$$

for symmetric positive-definite matrices. The shared assessment will use a symmetric eigensolver and record the minimum eigenvalue, maximum eigenvalue, reciprocal condition, configured threshold, method, and decision.

`NumericsConfig.min_spd_rcond` is the canonical threshold. A value below the threshold is rejected. A value clearly above it is accepted. A value satisfying `abs(rcond - threshold) <= atol + rtol * abs(threshold)` is `INCONCLUSIVE`; it is never silently accepted. The determinant-volume quantity may remain only as a separately named diagnostic and must not be labeled a condition number or control acceptance.

The shared policy must make consistent decisions for the existing Gaussian producer and the exact finite counterexample producer. The required fixtures include diagonal matrices, a correlated two-dimensional matrix that the old proxy falsely accepted, and a three-dimensional diagonal matrix that the old proxy falsely rejected.

### Numerical-policy reachability

Every accepted numerical field relevant to an advertised decision must affect that decision. Shared fields that do not apply to a laboratory must be serialized explicitly as `not_applicable`, not presented as active controls. For Session 3:

- `min_spd_rcond` controls the SPD conditioning threshold.
- `atol` and `rtol` control near-threshold classification and floating comparison metrics.
- Exact rational equalities remain exact and do not acquire artificial tolerances.
- `max_frame_condition` is used only by frame-conditioning paths and is serialized as `not_applicable` for Session 3.

Published artifacts will serialize requested and effective numerical policies wherever exact arithmetic intentionally bypasses a floating tolerance.

### Stress and status flow

Required stress checks will be represented as typed metric records or typed status-bearing assessments. Aggregate experiment status will consume them alongside the primary metrics. A failed required invariant produces `fail`; an unresolved near-threshold or unsupported assessment produces `inconclusive`.

Expected negative controls use positive success semantics. For example, the retained-order negative control passes when the omitted higher-order residual is strictly positive, and the near-singular control passes when the shared conditioning policy rejects the matrix for the recorded reason.

Relabeling stress will compute an actual residual from transformed objects. It will not serialize a literal zero independently of the Boolean result. A forced false coherence result must prevent a passing experiment.

### Claim and assumption metadata

Scientific producers emit `verification_state="CANDIDATE"` by default. Numerical execution may establish a metric's runtime status, but only a validated revision-bound ledger promotes a claim to `EVIDENCE_VERIFIED`.

`theorem_status` and `claim_origin` remain independent of verification state. Established standard identities may retain `theorem_status="ESTABLISHED"` and `claim_origin="STANDARD"` while their newly generated application record remains `CANDIDATE`.

Every assumption-boundary witness records:

- `inside_declared_domain=false`;
- `assumptions_satisfied=false`;
- `classification="assumption_boundary"`;
- a falsification or applicability explanation in its interpretation or witness metadata.

Support-violating KL pairs therefore cannot be serialized as ordinary inside-domain catalog records.

## Components and ownership

The implementation plan will map the final paths after a current source inspection. The intended responsibilities are:

- a shared finite-permutation module: typed convention, inverse, composition, and pullback helpers;
- a shared numerical-conditioning module: spectral assessment and threshold classification;
- `finite/counterexamples.py`: exact objects and independent oracles adapted to shared conventions;
- `geometry/finite_gauge.py`: compatibility re-export and use of the shared permutation type;
- `finite/counterexample_experiment.py`: effective numerical policy, status-bearing stress metrics, and candidate metadata;
- Gaussian conditioning call sites: use or compare against the shared assessment without changing unrelated Gaussian dynamics;
- focused tests: literal oracles, cross-producer metamorphics, mutation controls, and configuration reachability;
- result and review documents: updated values, statuses, evidence limits, and supersession record.

Independent producer formulas remain separate. The shared layer standardizes inputs, transformations, and acceptance policies; it does not compute both sides of a purported cross-check through one implementation.

## Error handling

- Invalid permutations fail before transformation with a precise bijection error.
- Ambiguous raw permutation tuples are rejected at new shared boundaries.
- Nonsymmetric or non-SPD rational matrices fail before spectral conditioning.
- Nonfinite eigenvalues or eigensolver failure yield a typed inconclusive assessment or a dedicated validation error before publication.
- Unsupported numerical-policy combinations fail before RNG and artifact creation.
- Required failed or inconclusive stress assessments prevent `status="pass"`.

## Test strategy

Implementation follows red-green-refactor for each behavior:

1. A three-cycle cross-producer test fails under the current inverse convention.
2. Composition and inverse tests pin the canonical group action.
3. The correlated two-dimensional and diagonal three-dimensional SPD witnesses fail under the current determinant proxy.
4. Configuration-mutation tests demonstrate that `min_spd_rcond`, `atol`, and `rtol` reach their intended decisions.
5. Stress mutation tests force each required predicate to fail or become inconclusive and assert aggregate status.
6. Metadata tests require producer state `CANDIDATE` and correct assumption-boundary flags.
7. Existing two-state, exact-KL, Fisher, marked-event, channel-composition, and gauge-equivariance tests remain green.
8. Focused JUnit and coverage run first, followed by the complete CPU suite with `C:\Python314\python.exe`.

CUDA tests are not required because this remediation changes CPU finite conventions and shared scientific metadata only. Any incidental CUDA claim remains outside scope.

## Documentation and evidence

Affected result and review documents will identify the previous records as superseded, list requested and effective numerical policies, distinguish exact SPD membership from numerical spectral conditioning, and state that producer records are candidates until ledger promotion.

A fresh ignored verification ledger will be started only after the final implementation SHA is fixed. Code and experiment claims will close from current JUnit, coverage, and reproduced artifact evidence. Mathematical claims will rely on exact derivations or literal algebraic oracles rather than numerical agreement alone.

The Research vault is consulted for context but will not be modified without explicit user confirmation.

## Acceptance criteria

The remediation is complete when all of the following hold:

1. The same typed three-cycle gives identical relabeling outputs across all applicable producers.
2. The two former SPD decision reversals are corrected under the shared spectral policy.
3. Legal numerical-policy changes alter the intended decisions, and unsupported policies fail before effects.
4. Every required stress failure prevents a passing run.
5. Generated claims are `CANDIDATE`, and all boundary witnesses carry correct domain and assumption flags.
6. Cross-producer tests use independent implementations and include a pinned mutation that fails.
7. Focused coverage is at least 80 percent for every new production module.
8. The complete CPU suite passes from machine-readable JUnit output.
9. A validated final-SHA claim ledger records the scientific closure evidence.
10. No artifact-security, Git-provenance, CUDA, continuum, registry, or unrelated performance work enters the change set.
