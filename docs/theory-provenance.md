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

## Participatory local-to-global snapshot sync — 2026-08-20

The authoritative source was the clean isolated Research worktree
`C:\Users\chris and christine\.codex\visualizations\2026\08\20\01a01f1c-b8b0-7c13-b4ba-fd31a2d8063b\research-participatory-foundations-worktree`
at revision `451af943493d5ee1621f30410a9698a4e02251c2`. The target began clean at
`11591968e2919e3bfeb4c7ed687b252cbfb9513e` on branch
`codex/participatory-local-to-global-20260820`.

Twelve authorized source files differed and were copied into `Theory/` byte-for-byte. Each row
records the SHA-256 shared by the authoritative source and synchronized target after the copy:

| Target path | SHA-256 | Byte identity |
|---|---|---|
| `Theory/01_introduction.tex` | `E578946866701996B070183DFC7F09A1A351FBAAC45DE5BBEB32AB7C8128AEE9` | source = target |
| `Theory/02_geometry.tex` | `A00317158A5AFF44D53DE64F7F0CEAD9A66B4A6FAB6D1164427C58FBB89A9694` | source = target |
| `Theory/03_probability.tex` | `087AE7A739D55486F0D809BDDD850E9A5F237B096BB407CC4ED719A0AF103492` | source = target |
| `Theory/04_generative.tex` | `DC4BCDE30606D0CDF49323EC43C263811A9C7A9E13C8B2E8051EB3AD8922B293` | source = target |
| `Theory/05_elbo.tex` | `7F5C41D23F675EF4654FAF311052C6FBCFA98A432BA9DCCF567ED5BB7E0AAEA1` | source = target |
| `Theory/05b_local_collective_elbo.tex` | `347ABE8D1D31E5C8AB54E9DA903FBD3198FD7CF0B5B36B3EC9BE293B412FE63D` | source = target |
| `Theory/05c_pullback_geometry.tex` | `B274B84EE76AE10F50BBE69EAF8E82158AFFF329FCF003287216ECDDE064A817` | source = target |
| `Theory/05d_relational_inference.tex` | `E79B71FAE6035271ADAAE1614BDB1AEB13B03BFC2DAD191F68A632854D3FA827` | source = target |
| `Theory/12_philosophy.tex` | `228D6C2B569C67BB8C8872DA6A1D678EF8ACB983536F4E5DBA3BF6DF14084F3B` | source = target |
| `Theory/SPEC.md` | `E77BB835683B2E76B6715864BF50256B97769462F285228A78DBE27E2F34FBD8` | source = target |
| `Theory/appendix_notation.tex` | `D2E6354349EA1C8E30F28948F2153CC6FCC0CFDA4B7C1A47536EBA3CD517B826` | source = target |
| `Theory/references.bib` | `AF7EAC4C058E03D8D8B0952366EFD8F86D561569939EB267D2899EE54CF64CF3` | source = target |

Before the bibliography copy, its only delta was the missing `Reichenbach1965` entry and its
separator blank line; there were no removed lines. The approved design retained its historical
repository baseline and frozen target while recording that the final integrated review refined
the access, per-incidence evaluator, and sparse-incidence notation to
`Acc_i`, `ev_{i,a}`, and `D_i`.

The authoritative Research build associated with this source revision recorded command exit
codes `0/0/0/0`, 343 pages, and PDF SHA-256
`EA84D6C1825E91C6400BFDB276ECAC69E9D7D4D347A744E81D424C0876EC95A5`.
`main.pdf` was deliberately excluded: no tracked or untracked `Theory/main.pdf` was created.
No LaTeX build was rerun in the target.

Target-only `Theory/PIFB2.tex` and `Theory/scientific_report.sty` were excluded and retain
SHA-256 values `F80E6DABD9E5485649066E227E80BEFF1DD2B1082CF786BCDAEEDB8CBD080EC4`
and `92A5A44847B2A748E1999DF55CD21C108204BEA79DA21F7265214708BAA25BFA`,
respectively. `Theory/verification/current-results.json` was also excluded and retains SHA-256
`F414A7CE5EC8D1FF61CC4B8DFA9065D3B5EFFF1656549DA88C9199D6C3943456`.
That JSON remains archived and stale: it is not evidence for Research revision
`451af943493d5ee1621f30410a9698a4e02251c2`. Codebase tests were skipped by user direction,
and no test result is claimed for this sync.
