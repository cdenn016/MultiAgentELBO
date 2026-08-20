# Theory snapshot sync — 2026-08-20

The clean authoritative source was
`C:\Users\chris and christine\.codex\visualizations\2026\08\20\01a01f1c-b8b0-7c13-b4ba-fd31a2d8063b\research-participatory-foundations-worktree`
at full revision `451af943493d5ee1621f30410a9698a4e02251c2`. The clean target baseline was
`11591968e2919e3bfeb4c7ed687b252cbfb9513e` on branch
`codex/participatory-local-to-global-20260820`.

All twelve authorized snapshot files differed and were copied byte-for-byte from
`manuscripts/gauge_vfe_rg/` to `Theory/`. Source and target SHA-256 values are identical:

| Copied target | SHA-256 |
|---|---|
| `Theory/01_introduction.tex` | `E578946866701996B070183DFC7F09A1A351FBAAC45DE5BBEB32AB7C8128AEE9` |
| `Theory/02_geometry.tex` | `A00317158A5AFF44D53DE64F7F0CEAD9A66B4A6FAB6D1164427C58FBB89A9694` |
| `Theory/03_probability.tex` | `087AE7A739D55486F0D809BDDD850E9A5F237B096BB407CC4ED719A0AF103492` |
| `Theory/04_generative.tex` | `DC4BCDE30606D0CDF49323EC43C263811A9C7A9E13C8B2E8051EB3AD8922B293` |
| `Theory/05_elbo.tex` | `7F5C41D23F675EF4654FAF311052C6FBCFA98A432BA9DCCF567ED5BB7E0AAEA1` |
| `Theory/05b_local_collective_elbo.tex` | `347ABE8D1D31E5C8AB54E9DA903FBD3198FD7CF0B5B36B3EC9BE293B412FE63D` |
| `Theory/05c_pullback_geometry.tex` | `B274B84EE76AE10F50BBE69EAF8E82158AFFF329FCF003287216ECDDE064A817` |
| `Theory/05d_relational_inference.tex` | `E79B71FAE6035271ADAAE1614BDB1AEB13B03BFC2DAD191F68A632854D3FA827` |
| `Theory/12_philosophy.tex` | `228D6C2B569C67BB8C8872DA6A1D678EF8ACB983536F4E5DBA3BF6DF14084F3B` |
| `Theory/SPEC.md` | `E77BB835683B2E76B6715864BF50256B97769462F285228A78DBE27E2F34FBD8` |
| `Theory/appendix_notation.tex` | `D2E6354349EA1C8E30F28948F2153CC6FCC0CFDA4B7C1A47536EBA3CD517B826` |
| `Theory/references.bib` | `AF7EAC4C058E03D8D8B0952366EFD8F86D561569939EB267D2899EE54CF64CF3` |

The pre-copy bibliography delta was only the missing `Reichenbach1965` entry and its separator
blank line, with no removals. The existing design was marked approved and implemented; a concise
note records the final integrated review's `Acc_i`, `ev_{i,a}`, and `D_i` refinements without
changing its historical repository baseline or frozen target.

The authoritative Research PDF build for the source revision recorded exit codes `0/0/0/0`, 343
pages, and SHA-256
`EA84D6C1825E91C6400BFDB276ECAC69E9D7D4D347A744E81D424C0876EC95A5`.
The PDF was excluded from the target sync, and `Theory/main.pdf` remains absent and untracked. No
target LaTeX build was run.

Target-only `Theory/PIFB2.tex`, `Theory/scientific_report.sty`, and
`Theory/verification/current-results.json` were not modified. Their preserved pre/post SHA-256
values are, respectively,
`F80E6DABD9E5485649066E227E80BEFF1DD2B1082CF786BCDAEEDB8CBD080EC4`,
`92A5A44847B2A748E1999DF55CD21C108204BEA79DA21F7265214708BAA25BFA`, and
`F414A7CE5EC8D1FF61CC4B8DFA9065D3B5EFFF1656549DA88C9199D6C3943456`.
The archived `current-results.json` remains stale and is not evidence for Research revision
`451af943493d5ee1621f30410a9698a4e02251c2`. Codebase tests were skipped by user direction; no
test result is claimed. The original dirty checkouts and the authoritative source worktree were
left untouched. The existing `docs/change-logs/2026-08-20.md` was not overwritten.

## Physicist's companion consistency update

The repository-root `physicists_companion.tex` was aligned with the approved local-first Theory
snapshot. Its opening and variational summary now begin with agent-indexed belief and model-law
sections, access interfaces, evaluated generative mechanisms, local recognition laws, and
interaction-record kernels. They distinguish the normalized population generative law constructed
from those local mechanisms from the correlated population recognition law selected from the
local-marginal coupling class. Neither population law is interpreted as an agent or observer.

The companion now explains that a probability-law fiber is convex but not canonically linear and
that this typing retains, rather than removes, an agent's generative-model datum: a law over model
presentations together with the incidence-wise evaluator that turns a presentation into a
normalized mechanism. It also reserves `meta-agent` for a separately constructed coarse state,
observation interface, evaluated mechanism, recognition law, and update rule; an arbitrary
block-coordinate aggregate is not relabeled as a meta-agent.

The participatory section now records the bounded Neo-Kantian reading of local frames, evaluators,
and access interfaces as constitutive but revisable conditions of inferential meaning. It states
that the interpretation supplies neither consciousness, a population mind, physical creation by
observation, background independence, nor a physical action principle. The status table was
updated to retire the earlier non-gauge-covariant null sector-capacity result and to report the
positive but subunit root-framed covariant uplift under its declared numerical protocol.

Both expanded mapping summaries use page-breaking long tables so neither is deferred or clipped.
A fresh standalone Tectonic build exited zero with 32 pages and 259,215 bytes; its SHA-256 is
`8A9F3C8CEB1A3D4FB533A19303C039841CF5C0EEDD27167F1C9961F73FA5A12F`. Visual inspection of
the dictionary, participatory, status, and continuation pages found no clipping or overlap.
