# Scientific-integrity remediation contracts

Wave 0 freezes the public contracts and evidence protocol needed by the
scientific-integrity remediation program. It closes contract completeness
only. Wave 0 does not remediate an audit defect, and none of AUD-01 through
AUD-22 is resolved, refuted, or promoted by this wave.

## Frozen records

- [Audit disposition](audit-disposition-v1.json) assigns each audit item one
  owner wave, reproducer, guard, and evidence class.
- [Compatibility inventory](compatibility-inventory-v1.json) freezes the
  public surfaces and migration policies that later waves must preserve.
- [Status and failure contract](status-failure-contract-v1.json) separates
  status namespaces and freezes the last-permitted-effect ordering.
- [Historical fixed-ray bundles](historical-fixed-ray-bundles-v1.json) pins
  the tracked historical bytes by path, size, and SHA-256.
- [Verification snapshot](verification-contract-v1.json) pins the installed
  verification skill used for Wave 0 closure.
- [Evidence-index schema](remediation-evidence-v1.schema.json) closes the
  public candidate and closure evidence-index shape.

The governing documents are the reviewed
[Wave 0 plan](../../superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md),
the approved
[program design](../../superpowers/specs/2026-08-11-scientific-integrity-remediation-program-design.md),
and the source
[deep-audit report](../../audits/2026-08-11-post-fixed-ray-deep-audit.md).

## Status boundaries

For repository-produced records, producer verification_state is exactly CANDIDATE.
Assessment decisions and external verification-ledger states occupy
different namespaces and cannot be substituted for that producer state.

Historical bundle records support compatibility checks and reproduction at
their recorded revisions. These historical bundles are never upgraded, rewritten,
or treated as current scientific promotion merely because their bytes remain
available.

## Revision-bound evidence

Let P be the clean implementation-parent commit containing all Wave 0
contracts and tooling. The targeted, subsystem, and full CPU suites are run at
P; their scrubbed candidate evidence is published in a single evidence-only
commit E, where E is the exact child of P.

Closure then reruns those suites at E and produces uncommitted closure evidence
bound to tested head E and implementation parent P. The exact-child closure evidence
is not committed.
Candidate evidence at another revision, evidence copied from another run, or
an unreviewed historical bundle cannot close a current claim.

Each candidate pipeline, and separately for each closure pipeline, requires one
process-scoped CPU environment covering the suites, builder, and validator. Set
`CUDA_VISIBLE_DEVICES=-1` and `PYTHONHASHSEED=0`; remove
`MULTIAGENTELBO_RUN_CUDA_TESTS`, `VFE3_TEST_DEVICE`, and
`CUBLAS_WORKSPACE_CONFIG` before the first suite, and keep that environment for
every command in that pipeline. Do not rely on per-command or per-shell state
that can disappear before evidence construction. A missing or changed CPU pin
consumes that revision's attempt: preserve its raw diagnostics, publish nothing,
and restart from a new clean parent rather than retrying the same destination.

Wave 0 may close only the contract-completeness and historical-byte-pin
checks. The 22 audit findings remain INCONCLUSIVE_PENDING_OWNER_WAVE until
their assigned implementation waves provide domain-eligible closure evidence.
