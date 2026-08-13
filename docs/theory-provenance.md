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

The experiment manifest also records a runtime tree digest using the explicitly
versioned framing `sorted-relative-posix-path-nul-raw-sha256-digest-v1`, excluding
Python caches and `.pyc` files. For this snapshot that digest is
`a7fddfcb8c67dbec71c7a35d0e415313a38154719e05d6ccd73672a810939343`.
The two aggregate values use different framing conventions; per-file SHA-256
comparison, not equality between the aggregate values, is the preservation check.

The comparison excludes TeX build products and Python caches, including
`main.lot`, `main.out`, `main.synctex.gz`, and `main.toc`. Future source checks
must compare the tracked `Theory/` content against this snapshot record before
claiming preservation.

## Post-snapshot additions — outside the read-only scope (recorded 2026-08-13)

The 44-file record above is **no longer a complete inventory of `Theory/`**. Two files were added
after the snapshot, by commit `90fcd42` ("docs: land ultradeep audits, roadmap review, and PIFB2
source"), and are **not** present in the snapshot source tree
`Desktop/Research/manuscripts/gauge_vfe_rg` (which no longer contains a `PIFB2.tex` at all):

- `Theory/PIFB2.tex`
- `Theory/references.bib`

These two are **outside** the read-only declaration of line 5–6 and outside the 44-file digest at
line 17–18. The digest and the "zero path or content differences" statement remain valid for the 44
snapshot files only, and must not be read as covering the two additions.

Consequence for editing. `Theory/PIFB2.tex` is a *copy*; the live authority is
`Desktop/Research/manuscripts/PIFB2.tex`, verified byte-identical (3956 lines, `diff` clean), so line
numbers transfer unchanged. Edits to PIFB2 — including the outstanding observation-term binding at
`:689` — should be made against the Research-vault copy and the repo copy re-synced, not applied to
`Theory/PIFB2.tex` in place. The remaining 44 files stay read-only: changes to them require the
per-result `SPEC.md:17` compliance gate recorded in the worklog's write policy.

## Evidence boundary

`Theory/verification/current-results.json` is an archived, revision-bound
record. It is not fresh evidence for the current implementation. Fresh code or
experiment claims require current machine-readable outputs bound to the active
worktree revision.
