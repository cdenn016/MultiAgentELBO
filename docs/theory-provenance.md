# Theory snapshot provenance

`Theory/` is a supplied, read-only snapshot of
`C:\Users\chris and christine\Desktop\Research\manuscripts\gauge_vfe_rg`.
It is evidence input to this repository, not an implementation output. No
build task may modify its tracked contents.

## Snapshot check

- Verification timestamp (UTC): `2026-08-09T03:37:25.7960884Z`
- Research Git revision: `b4f8b204168eb317717180f137a33b01f0a28143`
- Research dirty-state caveat: the Research checkout reported 50 porcelain
  status entries at verification time. The revision records the committed base,
  not a clean-source guarantee.
- Comparison: all 44 supplied non-cache files were present in both trees and
  had identical SHA-256 digests; there were zero path or content differences.
- Deterministic aggregate digest of the 44 tracked snapshot files:
  `571caaea14ebbc4c325fbec528aca63fb5f53db502207bf5e69f41262406f1dd`.

The comparison excludes TeX build products and Python caches, including
`main.lot`, `main.out`, `main.synctex.gz`, and `main.toc`. Future source checks
must compare the tracked `Theory/` content against this snapshot record before
claiming preservation.

## Evidence boundary

`Theory/verification/current-results.json` is an archived, revision-bound
record. It is not fresh evidence for the current implementation. Fresh code or
experiment claims require current machine-readable outputs bound to the active
worktree revision.
