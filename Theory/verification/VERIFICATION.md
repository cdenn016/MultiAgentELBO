# Numerical reproducibility package

This directory makes the manuscript's computational claims auditable without
confusing numerical agreement with mathematical proof.

The post-review source contains **13 literal `\status{NUMERICAL}` tokens**:

- 11 substantive, current-protocol claims;
- one scope summary; and
- one status-taxonomy entry.

Local chapter status registers were removed. Bare table cells such as
`& NUMERICAL &` are forbidden. The runner discovers every `*.tex` file under
the manuscript source root and fails closed if the number or order of tokens,
the declared check mapping, or the source manifest drifts.

Each mapped numerical token must be the sole status in its prose paragraph
(apart from the explicitly captioned Status taxonomy table), and its
`source_line_at_inventory` value in `claims.json` must equal the current
literal source line. This binds one semantic numerical claim to one token and
one source location.

## Run

The authenticated production entry is the externally approved one-line
`build_bootstrap_transport.txt`, supplied as raw ASCII standard input to fixed
Windows PowerShell. Its decoded readable audit body is
`build_bootstrap_reference.ps1.txt`; that readable file is not itself an
authenticated launcher. Bootstrap modes `NumericalUpdate` and
`NumericalVerify` authenticate and retain the source `run_checks.py` identity
before execution. The externally asserted transport byte count and SHA-256 are
release inputs, not values learned from the checkout being tested.

Direct checkout execution is an unauthenticated developer convenience only.
It can diagnose the runner contract, but it cannot establish production
release provenance. A convenience verification from the repository root is:

```powershell
& "C:\Python314\python.exe" -I -S manuscripts/gauge_vfe_rg/verification/run_checks.py `
  --verify C:\tmp\gauge-vfe-rg-results.json `
  --report C:\tmp\gauge-vfe-rg-verify-report.json
```

The corresponding unauthenticated convenience update is:

```powershell
& "C:\Python314\python.exe" -I -S manuscripts/gauge_vfe_rg/verification/run_checks.py `
  --update C:\tmp\gauge-vfe-rg-results.json `
  --source-revision <full-lowercase-40-hex-commit> `
  --report C:\tmp\gauge-vfe-rg-update-report.json
```

If `--source-revision` is omitted in update mode, the runner uses the current
full `HEAD`. `--source-revision` is rejected in verify mode. `--update` and
`--verify` are mutually exclusive and each requires a result path. A report
target must differ from the result and must be outside the repository. An
update target must likewise be outside the repository, except for the exact
canonical `verification/current-results.json` path. Every invocation prints
the complete strict JSON operation report. A fresh safe `--report` target may
receive a failure document. An existing report is never overwritten on a
precommit failure; the current diagnostic remains on standard output. A
success report contains an invocation-unique lowercase 32-hex
`transaction_receipt_id` and a 64-hex `published_result_sha256`. Consumers
must require `ok=true`, `input_unchanged=true`, and exact equality among the
current result's raw SHA-256, `input_sha256_before`, `input_sha256_after`, and
`published_result_sha256`, in addition to exact lexical result path, protocol
profile, source revision, and a fresh receipt.

The checked-in `current-results.json` is still the older 29-check artifact. It
is intentionally historical and this implementation does not regenerate it.
It is not evidence for the 30-check package described below. A separately
governed evidence regeneration remains required before that evidence is
current.

## Files and binding

- `claims.json` maps every numerical-status token to its semantic claim,
  protocol, checks, and disposition. It and `manifest-policy.json`
  independently carry the exact `gauge-vfe-rg-production-v1` profile marker.
- `run_checks.py` is the deterministic CPU entry point.
- `result.schema.json` closes the schema-3 result envelope, dependency map,
  manifest entries, and four-field check records.
- `manifest-policy.json` declares the nonshrinkable protocol profile, recursive
  classes, exact inputs, style search order, governed namespaces, and explicit
  exclusions. The separately marked `synthetic-test-fixture-v1` profile is a
  closed test-fixture envelope; production mode cannot infer it from a
  top-level `checks` list.
- `lifecycle_gate.py` and `build_audit.py` close the revision and build-artifact
  lanes and are themselves bound inputs.
- `build_bootstrap_reference.ps1.txt` is the readable audit body.
  `build_bootstrap_transport.txt` is the exact governed one-line ASCII
  transport; strict base64 decoding must reproduce the reference bytes
  byte-for-byte. Both files and `tests/test_build_bootstrap.py` are mandatory
  at every production lifecycle endpoint.
- Every release phase enumerates the complete commit DAG reachable from its
  newer endpoint but not from its older endpoint (`rev-list newer ^older`).
  Every newly reachable commit is checked against the phase baseline, and
  every immediate parent-to-child edge whose child is newly reachable is
  checked independently. Parents already reachable from the older endpoint are
  baseline anchors rather than new phase commits; their trees still must load
  so their outgoing phase edges satisfy the same path, status, type, and
  regular-blob policy without a skip or waiver.
- Post-`W` lifecycle and publication purity uses the same complete
  newly-reachable enumeration for `W..HEAD`, `W..P`, and `P..HEAD`. Every
  returned tree must equal `W` on the entire protected path union, including
  existence, mode, object type, and blob identity. Per-edge checks are not
  needed for this lane because exact comparison of every newly reachable tree
  to the fixed `W` baseline detects each transient protected state directly.
  A newly imported pre-`W` side commit that lacks `W`'s protected state is
  rejected; an unrelated integration is admissible only when every imported
  tree preserves the exact `W` protected projection.
- `requirements.txt` is a strict six-line exact-pin contract for NumPy 2.4.4,
  SciPy 1.17.1, SymPy 1.14.0, mpmath 1.3.0, pypdf 6.12.2, and pytest 9.0.2.
  All six packages are mandatory. Results record non-null provenance for each;
  metadata, the dependency map, provenance versions, and the exact pins must
  agree. Uniform LF and uniform CRLF checkout bytes are both parsed; BOMs,
  mixed endings, bare carriage returns, whitespace, ranges, and comments fail.
- `current-results.json` is excluded from its own manifest, as is the compiled
  `main.pdf`; neither exclusion can be enlarged by editing the policy.

The production TeX lane binds the bibliography by the logical name
`references`. `BIBINPUTS` is exactly the absolute `manuscripts` directory and
`BSTINPUTS` is exactly the admitted style directory; neither value carries a
trailing search-list separator that would restore a default lookup path. The
retained BibTeX AUX and BLG snapshots must report exactly `plainnat` /
`plainnat.bst` and `references` / `references.bib`. The build audit acquires
deny-write/delete read handles for the complete isolated build-file inventory
before M0, derives hashes and semantic parses from those same held bytes, and
retains the handles through M1 and audit-report publication. Canonical
`main.fls` must be byte-identical to the retained pass-4 recorder, and every
recorded repository input must already belong to the prelocked source
envelope. The audit report itself is published only to an absent path with a
CreateNew/no-replace handle retained through exact SHA-256 marker emission; a
raced-in or preexisting target is preserved unchanged.

The manifest maps every bound repository-relative POSIX path to the SHA-256
digest and byte count of its raw worktree bytes. Discovery includes every TeX
source recursively, `SPEC.md`, the bibliography, every existing style
candidate in search order, `build.ps1`, all verification core files, and every
recursive `test_*.py`. Any other regular file in a governed namespace must be
an allowed explicit exclusion or discovery fails. Missing files, symlinks,
junctions, reparse traversal, path escape, duplicate/case-colliding paths, and
pre/post-read metadata drift fail closed. A literal `bound_paths` list may add
inputs but cannot replace or shrink the required recursive declarations.

Every Git subprocess receives an environment with all caller-provided `GIT_*`
variables removed and uses the fixed Git executable with
`--no-replace-objects`. Nonempty graft, shallow-boundary, local alternate, or
HTTP-alternate metadata is rejected around ancestry and object reads.
Source-tree lookup uses literal
pathspecs with exactly one NUL-terminated record. The full governed path set is
also enumerated from the source revision and must equal both current discovery
and the stored manifest, so deleting a committed recursive TeX or `test_*.py`
cannot shrink verification. The recorded source
revision `S` must resolve to itself and be an ancestor of current `HEAD=E`.
Each current retained raw manifest entry and stored manifest entry must equal
the byte count and SHA-256 of the regular blob at `S`. This comparison admits
no line-ending normalization: untracked `.gitattributes`,
`.git/info/attributes`, `core.autocrlf`, custom clean filters, `ident`, and
working-tree encodings cannot relax a raw-byte mismatch.
A Windows checkout materialized with CRLF while `S` stores LF is therefore
rejected; production and evidence worktrees must contain the exact blob bytes.
The release protocol assumes no concurrent writer can create, use, and restore
Git administrative metadata wholly between one subprocess's stable preflight
and postflight checks; kernel directory-event monitoring is intentionally
outside this verifier profile.

Persisted JSON is the project-specific compact canonical form: UTF-8,
`ensure_ascii=False`, sorted keys, `separators=(",", ":")`, finite values only,
and no trailing newline. Parsing rejects invalid UTF-8, duplicate keys,
nonfinite constants, overflow-to-infinity numbers, malformed input, and any
byte representation that is not this form. This is not a claim of RFC 8785/JCS
number canonicalization. The semantic digest authenticates exactly the entire
top-level document except `generated_at_utc` and
`semantic_payload_digest`; same-named nested fields remain authenticated.
`protocol_profile` is therefore authenticated. `source_dirty=false` is the
derived statement that this governed path set binds byte-for-byte to `S`; it
is not a claim that unrelated, ungoverned worktree paths are clean.

The runner's admitted child startup is the fixed
`C:\Python314\python.exe -I -S` invocation. Before any third-party import, the
stdlib-only bootstrap parses the exact pins, inventories and hashes every
actual RECORD file, and authenticates all six distributions. Only NumPy,
SciPy, SymPy, and mpmath are imported at runtime; pypdf and pytest remain
metadata-only. A meta-path finder rejects undeclared fixed-site modules, and
each delegated loader is bound to its M0 file hash from `create_module` through
`exec_module`. Bytecode writes are disabled and a fresh, non-reparse, empty
cache prefix must remain empty. Python, Git, dependency bytes, current `HEAD`,
and the cache policy are compared exactly at run M0, before persistence, after
staging, and at final closure. The hardcoded manifest-policy path is locked
first; the runner then discovers, source-binds, and transactionally retains
deny-write/delete handles for the exact governed set. Policy, claims, schema,
requirements, and manifest reads are served from those same handles. Exact
rediscovery, raw bytes, handle identity, lexical-path identity, and source
binding are rechecked before publication. On Windows, retained kernel handles
also deny executable and result-file replacement across the relevant evidence
window. These controls trust the Windows kernel, NTFS identity and sharing
semantics, the verifier process, and the fixed interpreter installation; they
do not authenticate transitive DLLs and are not a malware-resistance claim.

Update construction is in-memory and repository-read-only. Canonical result
and report bytes are staged through dedicated deny-write/delete, rename-capable
Windows handles without changing either target. All M1 source, governed-input,
tool, dependency, and report-staging closure runs before either target is
published, and every retained evidence handle is closed before commit. The
two-file commit order is deliberately result first, report second. The exact
published result handle transitions without an unguarded interval to a strict
retained read handle, its raw hash is checked, and it remains held through
report commit. A report-commit failure may therefore leave a valid new result,
but it leaves any old report untouched and emits a failed diagnostic with no
`published_result_sha256`; the old report is mechanically stale by hash and
receipt. Every failure before result commit preserves both existing result and
existing report bytes. A fresh absent report may receive a failure document.
There is no corrective rewrite of a previously published success report.

Verify mode reads the result through one retained Windows handle, cross-checks
that held file identity against the lexical path, independently rebuilds the
manifest before and after recomputation, runs all checks freshly in memory,
stages the report, and retains the result handle through report commit. It
never writes the result. Production results contain
the 30 deterministic numerical checks plus `CHK-SOURCE-INVENTORY`; PASS requires
all 31 ordered checks to be present exactly once and to pass.

## Stable factorization-gap protocol

`CHK-CG-FACTOR-GAP-STRESS-3138` is a new frozen protocol with seed `20260803`.
It regenerates 3,138 case-bound SPD matrices and partitions across dimensions
2 through 16 and nominal pre-transform generator-condition labels from 1
through `1e14`, records matrix and partition SHA-256 digests, and includes 18
designated exact-input controls evaluated at 100 decimal digits. Every record's
legacy `condition_number` field remains the nominal label; its
`achieved_condition_number` field is exactly `numpy.linalg.cond` of that same
digest-bound regenerated matrix. Repeated calls with the same schedule are
byte-for-byte deterministic at the record level.

The achieved 2-norm condition-number ranges are:

| stratum | minimum | maximum |
|---|---:|---:|
| global | `1` | `1.015265553314175e14` |
| general | `1` | `1.015265553314175e14` |
| exact block diagonal | `1` | `1.0075938532153164e14` |
| near decoupled | `1.0000000000000002` | `9.273791153286738e8` |
| scale | `1` | `1.0036120669923527e14` |
| permutation | `1` | `1.0071935024197442e14` |
| nested refinement | `1` | `1.0077056571347422e14` |
| 100-digit controls | `1.0000000000000004` | `1.0048132000124055e14` |

Only the global schedule is claimed to reach achieved conditioning near
`1e14`. Dimension-two exact-block cases contain two scalar blocks and therefore
do not realize their nominal targets; the near-decoupled stratum likewise does
not attain its high nominal labels. The runtime check separately counts all
3,138 attempted schedule cases, successfully evaluated 100-digit exact-binary64
references, and completed production-reference comparisons. PASS requires
3,138 in each category and zero failures, while every failure retains its
complete case identity and diagnostics. The 18 controls remain a designated
stratum, not the sole all-case evidence.

The ordinary implementation uses Cholesky factors, SciPy triangular solves,
canonical-correlation singular values, and `log1p(-rho**2)`. It does not form an
explicit inverse or subtract log determinants. A value within
`64*n*epsilon` of the singular-value boundary is routed to a 200-decimal-digit
evaluation of the exact binary64 input. A second binary64 solve backend defines
the raw-excursion diagnostic as the maximum observed across those two declared
binary64 backends. Exact-input domain violations and
raw excursions whose discrepancies exceed the operational guard fail closed.
The exact-input value path is also used when
`kappa_2(precision)*epsilon >= 1e-4`, when global power-of-two normalization
would lose a nonzero entry, or when a binary64 Cholesky, solve, SVD, or condition
diagnostic is unusable. This is a frozen-suite conditioning trigger, not a
universal perturbation radius; a nonfinite binary64 condition estimate triggers
adaptive-precision exact-dyadic Cholesky certification and reevaluation rather
than rejection. Cholesky and
solve residuals remain local backward diagnostics only. Their finite-health
gate is `64*gamma_n`, where `gamma_n=n*u/(1-n*u)` and binary64 unit roundoff is
`u=epsilon/2`; this gate is not used as a forward bound on `rho`, the gap,
relative entropy, monotonicity, scale invariance, or any oracle comparison.
Forward comparisons use independent exact-binary64 high-precision references
and separately labeled endpoint-roundoff or declared protocol-acceptance
policies. Early `range-or-condition`, `binary64-linear-algebra`, and
`binary64-svd` fallbacks occur before residual evaluation, so
`cholesky_residual`, `solve_residual`, `residual_tolerance`, `backward_error`,
and their corresponding aggregates are `null`. A residual-health fallback
instead retains each finite binary64 measurement, including finite values above
the health threshold. A field is `null` only when no finite usable numeric
diagnostic exists, either because an attempted measurement is nonfinite or
because a derived diagnostic requires an unavailable constituent;
independently finite siblings remain numeric. The finite threshold method
retains the
`binary64-residual-health` reason. Nonfinite method suffixes identify
`nonfinite-cholesky`, `nonfinite-solve`, or `nonfinite-tolerance`, listing
multiple causes in fixed Cholesky, solve, tolerance order. These local backward
diagnostics do not become forward-error bounds or enter a forward tolerance.
In all cases, `null` denotes neither failure nor zero. The zero-step one-block
result continues to report numeric zero diagnostics. The `GapStep` API retains
the fieldwise residual quartet. `FactorizationCaseRecord` serializes only the
aggregate `backward_error_bound`, `maximum_cholesky_residual`, and ordered
`evaluation_methods` tuple, not per-step solve or tolerance values. Despite
its compatibility name, numeric `backward_error_bound` is an aggregate of
one-ULP-up summaries of already rounded local residual measurements; it is
not a certified perturbation or forward-error bound.

The compatibility field `residual_derived_clip_bound` does not assert a general
residual-to-forward-error theorem. On the boundary path it reports the
outward-rounded discrepancy between the maximum raw binary64 `rho**2` and its
high-precision exact-input value. The positive-excursion witness is a separate
focused regression fixture, not an ordinary 3,138-case schedule outcome. It
binds matrix SHA-256
`45310a74550d3759fed0f83f71a6cf3b0f45942499361d723a2248bbe243e2e3`, exact
gap `22.777105858844084`, raw excursion `4.440892098500626e-16`, outward
allowance `9.432369402326953e-16`, and PASS status. The runtime check
mechanically recomputes all four quantities. A nearest-below-one clipped value
is not accepted as the gap. The compatibility
fields `clipping_applied` and `clipping_amount` identify an admitted positive
cross-backend excursion and its maximum excess above one; they do not describe
a numerical adjustment used to obtain the returned value.

## Coverage

The suite contains **30 deterministic checks** covering:

- Gaussian interaction structure, conditioning, and exact Kron witnesses;
- Gaussian restriction identities, the 3,138-case stable determinant-gap
  protocol, and information-geometric charts;
- generalized-spectrum gauge invariance;
- exact aggregation, holonomy, admissible partitions, associativity,
  bi-additivity, singular limits, frame cancellation, and equivariance;
- finite RG ray, sector, invariant-face, homogeneous, noncommuting-limit, and
  mass-pencil endpoints; and
- star/fold and reciprocal-pair determinant, kernel, and normalizer identities.

Some checks are supplemental because the tightened manuscript no longer
repeats a numerical tag for every corroborating endpoint. They remain mandatory
and are listed explicitly in `claims.json`.

## Interpretation

`PASS` means that the current source and protocol reproduce the declared finite
endpoint within its recorded tolerance. It does **not** prove a theorem,
genericity, convergence, universality, blocking-scheme independence, or a
physical law. Analytic statements are closed only by derivation or an eligible
primary source; asymptotic and physical claims remain open until their separate
obligations are discharged.
