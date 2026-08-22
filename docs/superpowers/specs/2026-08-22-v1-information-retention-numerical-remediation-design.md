# V1 Information-Retention Numerical Remediation Design

## Status and authorization

This addendum was authorized by the user on 2026-08-22 after the recursive
renormalization Phase 2 broad gate failed twice in the unchanged v1 numerical
audit. It supersedes the Phase 2 prohibition on editing the specific v1 files
listed below, but it does not relax any other Release 1 or Phase 2 boundary.

## Problem

`capacity_information_retention` rejects a positive mutual-information
denominator below `MI_CEILING_FLOOR`, but it accepts exact zero and negative
roundoff. Exact zero makes the reported retention ratio undefined; negative
roundoff is not a valid mutual information. The current fallback maps an exact
zero denominator to a retention value of zero, which misstates an undefined
measurement.

The separate one-step pair-retention audit pins eight-decimal reproducibility
even though the published result is `0.155747`. Fresh processes have produced
values between `0.15574727268694233` and `0.15574737198930919`; both round to
the published six-decimal result. The dynamically regenerated IPF fixture and
optimized floating-point contractions do not promise bitwise or eight-decimal
identity across process histories.

## Authorized behavior

`capacity_information_retention` must reject a nonfinite fine mutual
information and every finite value at or below `MI_CEILING_FLOOR`. The error
must continue to identify the denominator as an inadmissible retention
measurement. Deterministic tests must cover exact zero, negative roundoff,
positive sub-floor roundoff, and a value above the floor.

The published one-step retention contract remains `0.155747` at six decimal
places. Its regression must use zero relative tolerance and an absolute
half-unit-in-the-last-published-place tolerance of `5e-7`. This is a precision
correction to the audit assertion, not a change to the scientific result.
The capacity-retention value and all other v1 scientific assertions remain
unchanged.

## Authorized files

The remediation may modify only:

- `src/multiagent_elbo/finite/cocycle_flow.py`;
- `tests/test_lab_vs_theory_audit_remediation.py`;
- `tests/rg_v2/test_legacy_regression.py`;
- `rg_v2/data/legacy_rescaling_v1.json`;
- `docs/change-logs/2026-08-22.md`.

The already pending Phase 2 replay test and 2026-08-21 log edits remain owned
by the original Phase 2 Task 7 and must not be staged with this amendment.

## Frozen-baseline protocol

The numerical behavior and its tests are committed first. A second commit
re-pins `_BASELINE` in `test_legacy_regression.py` to that exact numerical-fix
commit and regenerates `legacy_rescaling_v1.json` through the existing explicit
`RG_V2_REFRESH_LEGACY_BASELINE=1` route. `cocycle_flow.py` must not be added to
the exempt `_SEAMS`; its new blob remains protected by the refreshed baseline.

The regenerated capture must preserve the complete launcher configuration
identities, source-fixture hash, semantic artifact hashes, and serialized
metric records. Only revision-binding fields may change unless an executed
comparison demonstrates and explains a scientifically intended difference.

## Verification

The numerical task uses test-first evidence for the invalid denominator
boundary, followed by the complete audit-remediation and cocycle-flow modules.
The rebaseline task runs the explicit refresh gate and then the normal frozen
legacy regression file. After both task reviews pass, the original Phase 2
Task 7 reruns its consolidated focused JUnit and one broad CPU JUnit with
`CUDA_VISIBLE_DEVICES=-1` and `PYTHONHASHSEED=0`. Completion requires zero
failures and zero errors; no CUDA result is claimed.

## Nonclaims

This amendment does not alter the recursive Phase 2 construction, its
artifacts, metrics, exact rational oracles, or scientific interpretation. It
does not establish RG dynamics, scale composition, fixed points,
universality, a continuum limit, or an ontological agent claim.
