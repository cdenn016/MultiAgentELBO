# Skeptic attack on P9-Critical-1-provenance

STATUS: COMPLETE

AGENT: adversarial skeptic (wave 2), assigned to kill or confirm one wave-1 finding
TARGET REVISION: `8ce635807a6ca2a388255fc996c98f7c535e5843` (checked out on `review/2026-08-15-deep-review`)
FINDING UNDER ATTACK: `P9-Critical-1-provenance` — "Two of the three provenance snapshots bind bytes
that were never committed and are now unrecoverable, so the one-way non-circular chain is unauditable
in principle" (`docs/reviews/2026-08-15-deep-review/findings/P9-selfcert-falsifiability.md:50-127`)

## VERDICT: UPHELD_REDUCED — corrected severity **High**

The finding's factual core about **one** snapshot survives an exhaustive recovery attempt. Its
headline claim about **two** snapshots is refuted by executed command output, as is its blanket
statement that no entry is reconstructible from git and its rhetorical claim that the tables "could
have been typed in any state and would look identical."

Corrected statement of the defect:

> **One** of the three provenance snapshots — `review_input_snapshot`, `snapshot_id`
> `corrected-pre-review-add1a69` — binds uncommitted working-tree bytes. Eleven of its sixteen
> recorded hashes exist nowhere in either git object store (reachable or unreachable) and nowhere in
> 55,535 files on disk across the repository, the originating worktree, and the entire codex session
> tree. Four of its fifteen recorded package paths did not exist in any form at the named HEAD
> `add1a69`. The release-facing prose (`evidence/release-assembly.json:125` bare
> `"git_head": "add1a69…"`; `construction-or-strongest-theorem.md`) presents this snapshot as bound to
> that commit without the "unstaged" qualifier that two of the four reviews do carry, and that
> presentation is materially misleading. The remaining two snapshots are fully auditable.

## What I did

Everything below is executed command output on the target revision, not a reading of either party's
prose.

### 1. The `fix_round_1_review_input_snapshot` is fully recoverable — this half of the finding is dead

The finding asserts (`P9-selfcert-falsifiability.md:109`):

> "The same holds for the fifteen artifact hashes under `fix_round_1_review_input_snapshot` that
> differ from the released values."

That is false. `release-provenance.json:66` records `"git_head": "1b18842d6f853ee32c2b4f8a1741b1738ce9890e"`
for that snapshot, and every entry in its table equals the bytes committed at that commit. I
recomputed all of them:

```
$ cd "C:/Users/chris and christine/Desktop/MultiAgentELBO"
$ P=docs/derivations/2026-08-15-full-pointwise-meta-agent
$ for f in <all 25 package paths in the table>; do git show "1b18842:$P/$f" | sha256sum; done
```

| path | recorded in `fix_round_1` | recomputed at `1b18842` | match |
|---|---|---|---|
| `adversarial-report.json` | `a2f0c1f7…` | `a2f0c1f7767b7e73479abf353f11502e2bce2393fcc8769b8ba923a9140a5450` | ✓ |
| `approach-registry.json` | `d9f92621…` | `d9f92621d421002341bc711d4a4da63496cc7f0c38c6fae5be9af2872644b8c5` | ✓ |
| `claim-ledger.json` | `2ec20d0d…` | `2ec20d0df74f406d391486b7ea959f7f67bdaf44c15c0ee9fb1528947c652020` | ✓ |
| `construction-or-strongest-theorem.md` | `4498334a…` | `4498334ad927febf67ac4148e4407a73aa4bf3b26e5d04f0c4f273fc77eb75a0` | ✓ |
| `counterexample-register.md` | `59be1c06…` | `59be1c062463bc9337c6edc34f90ab5df828a2c7b2b5247792a732d50deb2159` | ✓ |
| `dependency-dag.json` | `ac28d445…` | `ac28d44546eb576fa3816282200b79ff481bd74934cacebaaab50b13dfa21246` | ✓ |
| `evidence/adversarial-attacks.md` | `edc9f7d8…` | `edc9f7d8632bd24e781cf137ff2c84570ebee4dea414adf35e3028c443c38546` | ✓ |
| `evidence/counterexample-proofs.md` | `59c38ed4…` | `59c38ed4181b2f8fbf2b573c79cb7257516c7e2d91e44dbea870c953406de6fc` | ✓ |
| `evidence/direct-derivation.md` | `2aa70b07…` | `2aa70b07751d07712a3d9395f77817317d48d77d97c3fd5fb8cd1a3f6fda226a` | ✓ |
| `evidence/finite-nongaussian-output.json` | `7092ec0a…` | `7092ec0a0dce059c2fcfc177ec288b0b708481aa9eace7a6ee657e3a1dc21e0c` | ✓ |
| `evidence/finite_nongaussian_witness.py` | `204effc2…` | `204effc256fcc89d9b6cbaa80d33b88eac845b7bfe2694653b0e204eb4760b48` | ✓ |
| `evidence/independent-reconstruction.md` | `f74f74bb…` | `f74f74bb93c240f28016b550fe58a4643d487ee8a517d40faa77d69cacde0df9` | ✓ |
| `evidence/notation-collision-report.json` | `11499c35…` | `11499c353b6b32ed783629302690877e337054a7e5c61a74cb9aa35224363684` | ✓ |
| `evidence/notation-registry.json` | `c4ee4c4c…` | `c4ee4c4ccfbf88689539f318a6b850dc0e1b2e00b5f4c08d04655561feb21813` | ✓ |
| `evidence/notation-standard.md` | `cfe662fa…` | `cfe662fa42a3e4aed5c55d14851604cfd24f2579c8188d7bda00f579f4be3695` | ✓ |
| `evidence/notation_scan.py` | `0c11294e…` | `0c11294e10b8a832e6e0f6fc88eacda7865f12e994a8a6ea7ddb56a19d7f6a62` | ✓ |
| `evidence/oracle-erasure.md` | `c957a173…` | `c957a17307ed7839b77fb804be83e9e721f0f8d64cc46a67e36b532625b50c72` | ✓ |
| `evidence/release-assembly.json` | `a6134a6f…` | `a6134a6f766e61fff2194882a4ec72031ccd328ef099713714f0d889619765fa` | ✓ |
| `evidence/reviews/view-dynamics-scope.md` | `d55a6945…` | `d55a69454e8377ae3de156640471d777730caa21e0f569c68330d717d04d9938` | ✓ |
| `evidence/reviews/view-gauge-holonomy.md` | `431a63b0…` | `431a63b06b90277ce2697d6d57a86054346564d2bb449cf11fe3673bd6fb42ba` | ✓ |
| `evidence/reviews/view-information-vfe.md` | `c291869c…` | `c291869ccb7d518f2df85c43f60319e59654c2769e0fdc8b07373a53430525d4` | ✓ |
| `evidence/reviews/view-probability-kernel.md` | `14f7f00f…` | `14f7f00fdbc0a3e2f67357c249aa631eae336940f7ea99d9aad3b164f423b27e` | ✓ |
| `final-report.md` | `d3a5cae2…` | `d3a5cae2eee88155387b85d6337cca015f2c725b9f56a4852c2ace4bb85d369c` | ✓ |
| `problem-contract.json` | `e74764ab…` | `e74764ab2db321fe269b48f3e45dca2e16a713df58a83c14d17233f26ab00e08` | ✓ |
| `release.json` | `458cb9b7…` | `458cb9b724e5e7c2b20bd0fc2e68b28f36d2545df08a1ede699e9b39e1aec369` | ✓ |

25/25 package entries match, plus the design-spec entry `a302a046…` which the wave-1 investigator
himself verified equals the `1b18842` bytes in their CRLF worktree rendering. Eleven of these 26
entries differ from the `final_release_snapshot` values, and all eleven are recoverable. The
"WITHHOLD, 0/0/2" fix-round-1 record is therefore fully auditable against committed bytes, exactly as
its `git_head` field claims.

The finding's own headline count — "**two** of the three provenance snapshots" — is wrong. It is one.
Stage 2 and stage 3 are both fully recomputable; the investigator verified stage 3 himself
(`P9-selfcert-falsifiability.md:494`).

### 2. The stage-1 recovery attempt: eleven of sixteen hashes genuinely do not exist anywhere

I gave the finding every chance to die here and it did not.

**Object-store scan.** I enumerated *every* object in both relevant object stores with
`git cat-file --batch-all-objects` (which includes unreachable and dangling objects, so it
supersedes `git fsck --lost-found`), streamed each blob's content, and computed SHA-256 of both its
raw bytes and its CRLF rendering:

- `C:/Users/chris and christine/Desktop/MultiAgentELBO/.git` — 3377 objects, 1418 blobs
- `C:/Users/chris and christine/.codex/visualizations/2026/08/13/019ffb08-b1cf-7120-9f79-7635e62c4d0a/.git`
  — 3219 objects, 1327 blobs. **This is the store the finding never searched.** The originating
  worktree `C:/tmp/MultiAgentELBO-full-meta-agent-implementation-20260815` is not a worktree of the
  Desktop repo at all; its `.git` file reads
  `gitdir: C:/Users/chris and christine/.codex/visualizations/2026/08/13/019ffb08-…/.git/worktrees/MultiAgentELBO-full-meta-agent-implementation-20260815`.
  Searching it was the most promising way to kill the finding. It produced the identical result.

Both stores gave the same answer:

```
ce3494750e04… RI problem-contract.json                   not-found
787132b16d03… RI approach-registry.json                  not-found
862dd5501451… RI claim-ledger.json                       not-found
ac28d44546eb… RI dependency-dag.json                     FOUND(raw) 1908cc3b6a77…
59be1c062463… RI counterexample-register.md              FOUND(raw) 328562afb2e5…
71c563725989… RI construction-or-strongest-theorem.md    not-found
bfbe5238accc… RI adversarial-report.json                 not-found
b46ace5e52de… RI release.json                            not-found
730c28d4ebd5… RI final-report.md                         not-found
2aa70b07751d… RI evidence/direct-derivation.md           FOUND(raw) b755f00dc8c7…
f2c6bf6899ad… RI evidence/adversarial-attacks.md         not-found
d25ad3b8b6f8… RI evidence/independent-reconstruction.md  not-found
249e18fb17fa… RI evidence/oracle-erasure.md              not-found
0943400855096… RI evidence/release-assembly.json         not-found
a302a046e886… RI design.md                               FOUND(crlf) ae788d4bad65…
```

**Filesystem scan.** I hashed every `.md/.json/.txt/.diff/.patch/.py/.bak/.orig` file — 55,535 files
— under the originating worktree, the whole of `C:/Users/chris and christine/.codex`, and the target
repository, testing both raw and LF-normalized forms:

```
files hashed: 55535
NO MATCHES for any of the 11 unrecovered review-input hashes
```

**Reflogs and stashes.** `git stash list` empty in both repos; the originating worktree's reflog runs
`ceffda2 → … → add1a69 → 1b18842 → … → 063a5bb` with no intermediate state, and `git fsck --unreachable`
output is a subset of what `--batch-all-objects` already covered.

**The CRLF escape route is closed independently.** `git show add1a69:.gitattributes` line 16 already
contains `docs/derivations/2026-08-15-full-pointwise-meta-agent/** text eol=lf`, so the worktree bytes
at review time were LF; and in any case my scan tested the CRLF rendering of every blob in both stores
against all sixteen targets and matched only the design spec.

The investigator's stated falsifier — "Produce any commit, stash, reflog entry, or surviving worktree
in this repository whose `problem-contract.json` hashes to `ce349475…`" — is therefore **not met**. I
tried harder than he did and got the same answer.

### 3. Corroboration that the state was real and was never committed

`git show <rev>:…/problem-contract.json | wc -l` gives 67 lines at `22b5b36`, 67 at `add1a69`, 76 at
`1b18842`, 76 at HEAD. The codex session transcript
`~/.codex/sessions/2026/08/15/rollout-2026-08-15T13-56-30-….jsonl` records an executed command whose
output is `ce3494750e04a421…\t74\tdocs/derivations/2026-08-15-full-pointwise-meta-agent/problem-contract…`,
and a second whose output is `add1a69f2b83550d13abd330c13f4b4e8e9138b9` followed by
`ce3494750e04a421…  docs/…/problem-contract.json`. A 74-line intermediate between a committed 67 and a
committed 76 is exactly a real, uncommitted working state. Two conclusions follow, and they cut in
opposite directions:

1. The bytes were real and the hash was really computed from them at a time when `HEAD` was `add1a69`.
   This **refutes** the finding's claim that the tables "are unfalsifiable tokens that could have been
   typed in any state and would look identical" (`:113`). An external, timestamped execution record
   exists.
2. The 67 → 76 jump confirms the 74-line state was never committed. The bytes are genuinely gone from
   the repository, which is what the finding's core asserts.

The transcripts are private local files outside the release. They rebut fabrication; they do not
repair third-party auditability of the published package, because no reader of the repository has
them.

### 4. Where the finding overstates beyond the headline

**"It is not [reconstructible from git], for any of the sixteen entries" (`:117`) is false for five.**
Recomputed:

| entry | recorded | recoverable at |
|---|---|---|
| `docs/superpowers/plans/2026-08-15-full-pointwise-meta-agent.md` | `6dde35db…` | **`add1a69` itself**, and `1b18842`, and HEAD |
| `evidence/direct-derivation.md` | `2aa70b07…` | `1b18842` and HEAD `8ce6358` |
| `dependency-dag.json` | `ac28d445…` | `1b18842` and HEAD |
| `counterexample-register.md` | `59be1c06…` | `1b18842` |
| `docs/superpowers/specs/…-design.md` | `a302a046…` | `1b18842` and HEAD (CRLF rendering) |

The plan file entry is recoverable at the named HEAD, contradicting "for any of the sixteen entries"
directly. And the mathematically load-bearing artifact is the second row: `evidence/direct-derivation.md`
at `2aa70b07…` is byte-identical to the file checked out at HEAD right now
(`sha256sum docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md` →
`2aa70b07751d07712a3d9395f77817317d48d77d97c3fd5fb8cd1a3f6fda226a`). So a third party **can** verify
that the derivation the four domain reviews claim to have read is exactly the derivation now in the
repository. The claim that "the binding detects nothing" is too strong: for the artifact that carries
the mathematics, the binding detects substitution and reports none.

**The non-circularity claim itself is intact.** `release-provenance.json:6-9` asserts only that the
review-input and final snapshots are distinct and that the final record excludes its own SHA-256. Both
are checkable and both hold: the tables differ (eleven entries differ between fix-round-1 and final
alone), and `"excluded_self_path": "evidence/release-provenance.json"` is honored. What fails is
auditability of stage 1, not non-circularity.

### 5. What survives, and is worth reporting at High

- **Four of the fifteen recorded paths did not exist at `add1a69` in any form.**
  `git ls-tree add1a69 .../evidence/` returns only `counterexample-proofs.md`, `direct-derivation.md`,
  `finite-nongaussian-output.json`, `finite_nongaussian_witness.py`, `notation-collision-report.json`,
  `notation-registry.json`, `notation-standard.md`, `notation_scan.py`.
  `evidence/adversarial-attacks.md`, `evidence/independent-reconstruction.md`,
  `evidence/oracle-erasure.md`, `evidence/release-assembly.json` and the whole `evidence/reviews/`
  directory are absent. A record labeled `git_head: add1a69` that lists hashes for files not present at
  `add1a69` is a defective provenance record, not a rounding error. Three of the four are substantive
  evidence documents, not bookkeeping, so what the reviews examined in the adversarial portfolio, the
  independent reconstruction, and the oracle-erasure argument is not recoverable.
- **Two of the four reviews drop the disclosure the other two carry.**
  `view-information-vfe.md:10` — "plus the exact unstaged Task-5 bytes below. Because the draft is
  intentionally unstaged, the Git revision alone is not its identity" — and `view-gauge-holonomy.md:10`
  ("corrected frozen unstaged bytes") are honest. `view-probability-kernel.md:6` ("bound to Git `HEAD`
  `add1a69…` … and the corrected pre-review mathematical/payload snapshot below") and
  `view-dynamics-scope.md:8` ("Frozen source revision: `add1a69…`") do not. Neither does
  `release-assembly.json:125`'s bare `"git_head"`. The disclosure exists in the package but not on the
  release-facing surface.
- **Independent, smaller auditability gap I found while attacking this one.** None of the three
  `fingerprint_sha256` values (`6735ec9b…`, `7479e84d…`, `5d3703b3…`) is reproducible from its own
  artifact table by any documented or plausible construction. I tried 76 constructions per snapshot
  (sorted/insertion order × six separators × path-hash / hash-only / hash-path orderings × trailing
  newline, plus canonical and indented JSON serializations); none matched, and `grep -rn fingerprint`
  over the package finds no algorithm. This affects the **final** snapshot too, so it is not covered by
  the wave-1 finding as written. Severity: Low on its own — the per-file table is the operative
  binding and it does check out — but it should be recorded.

## Why High and not Critical

Half the finding's stated scope is refuted by executed command output: `fix_round_1` binds committed
bytes at the commit it names, all 26 entries. The structural non-circularity claim holds. Stage 3
holds. The load-bearing derivation is byte-verifiable against HEAD. No mathematical claim in the
package depends on any of this, and the principal reviewer's independent reconstructions of the KL
chain, the parent-version argument, and the recovery theorem are untouched by it — my verdict does not
contradict any P0 reconstruction, because P0 makes no provenance claim.

## Why not Medium

The investigator's own falsifier sets Medium as the floor conditional on the bytes being recoverable.
They are not. I searched two complete object stores including all unreachable objects, both reflogs,
and 55,535 files on disk, and produced none of the eleven. A published record that names a commit
which does not contain four of its listed files, and whose eleven other listed hashes no reader can
ever check, is more than mislabeling.

## FALSIFIER OF MY OWN ATTACK

Two distinct facts would overturn parts of this verdict.

1. **Against my reduction to one snapshot:** exhibit any entry of `fix_round_1_review_input_snapshot`
   whose recorded hash is *not* the `1b18842` blob — i.e. show that
   `git show 1b18842:docs/derivations/2026-08-15-full-pointwise-meta-agent/<path> | sha256sum`
   disagrees for some path. I ran that for all 25 package paths and every one agreed; a single
   disagreement would restore "two of three."
2. **Against my upholding of stage 1:** produce the eleven missing byte-strings. The most credible
   route, which I identified but did not complete, is replaying the `apply_patch` stream in
   `~/.codex/sessions/2026/08/15/*.jsonl` forward from the `add1a69` blob to reconstruct a 74-line
   `problem-contract.json`; if the reconstruction hashes to `ce3494750e04a421d6700c970ccbffb7f37efcde3c6998b59970ceaf49600936`,
   the stage-1 bytes are recoverable after all and this drops to Medium (mislabeling a snapshot with a
   git head that does not contain it). My targeted extraction found no
   `*** Update File: …problem-contract.json` hunk in the 2026-08-15 session logs, but I did not
   exhaustively decode every escaping variant in those transcripts, so I cannot rule the
   reconstruction out.

## Recommended corrected wording for the final report

> One of the three provenance snapshots — `review_input_snapshot` / `corrected-pre-review-add1a69` —
> binds working-tree bytes that were never committed. Eleven of its sixteen recorded hashes are
> unrecoverable from the repository, and four of its listed paths did not exist at the commit it names,
> so a reader cannot check what the four domain reviews actually read for those artifacts. The other
> two snapshots bind committed bytes and were recomputed in full. The mathematically load-bearing
> artifact, `evidence/direct-derivation.md`, is byte-identical across the review-input record, commit
> `1b18842`, and HEAD, so the derivation the reviews claim to have read is verifiable. The release
> should either commit the review-input payload before obtaining reviews against it, or state plainly
> that stage 1 is an unstaged working-tree state with no independently recoverable form and drop the
> bare `"git_head": "add1a69…"` framing.

## Reproduction

```
git show <rev>:docs/derivations/2026-08-15-full-pointwise-meta-agent/<path> | sha256sum
git ls-tree add1a69 docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/
git --git-dir <store> cat-file --batch-all-objects --batch-check='%(objectname) %(objecttype)'
```
Scripts used (scratchpad, not committed):
`scan_blobs.py` (object-store SHA-256 sweep, raw + CRLF), `scan_fs.py` (55,535-file disk sweep),
`fingerprint.py` (76 fingerprint constructions per snapshot).
