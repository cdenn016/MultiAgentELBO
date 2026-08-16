# 2026-08-16 — Codex/Claude harness parity sync

Scope: user-level harness configuration under `~/.codex` and `~/.claude`. No repository source
files were modified.

## Motivation

Codex was observed completing tasks far more slowly than Claude. The suspected cause was the
`verification` and `superpowers:verification-before-completion` skills. That hypothesis was
refuted: `~/.codex/skills/verification` is a Windows **junction** pointing at
`~/.claude/skills/verification`, so the two harnesses execute byte-identical verification logic;
the `Stop` hook invoking `verification_gate.py` is configured identically in
`~/.claude/settings.json` and `~/.codex/hooks.json`; and `superpowers` is v6.3.0 on both sides.
`~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md` differ only by a precedence preamble and one
reworded sentence.

The real driver was skill/agent divergence. Codex carried a `red-blue-debate` skill that Claude
does not have, defaulting to `panel=full` — roughly 32–36 agent dispatches per invocation, every
dispatch in ultrathink mode. Codex's stale copies of `peer-review`, `rigor-sweep`, and
`deep-audit` routed contested-claim work into it, where Claude's newer copies route the same work
to a two-agent `audit-skeptic` / `audit-defender` pair. Codex's skill copies predated Claude's
de-debate migration and also lacked the cross-model verification section.

## Changes

A timestamped backup of the prior state was written to `~/.codex/_backup-20260816-074132/`
containing the original `skills/` and `agents/` trees.

The `red-blue-debate` skill directory was removed from `~/.codex/skills/`. Twenty debate
scaffolding agents were removed from `~/.codex/agents/`: `blue-team`, `red-team`, `debate-judge`,
`debate-canon-cop`, `debate-chief-judge`, `debate-coordinator-blue`, `debate-coordinator-red`,
the three `debate-judge-*` variants, and the ten `debate-expert-*` agents.

All shared skill directories were resynced from `~/.claude/skills/` to `~/.codex/skills/`, since
Claude's copies were in every case the newer and already de-debated versions. `verification` was
skipped because it is a junction to Claude's copy and is therefore already shared.
`skill-creator` was skipped because Codex ships its own under `skills/.system/`.
`rigorous-theory-search` was newly propagated to Codex.

Two audit agents that Claude had and Codex lacked were ported from Markdown to Codex's TOML agent
schema (`name`, `description`, `developer_instructions`): `audit-ml-engineer` and
`audit-philosophy-of-science`. Their absence was why Codex's `rigor-sweep` had dropped the
corresponding routing lines and substituted `debate-expert-philosophy-of-science`.

## Verification

All 27 remaining Codex agent TOML files parse under `tomllib` with `name` and `description`
present; zero failures. Grep for `red-blue-debate`, `debate-expert`, `red-team`, `blue-team`,
`debate-judge`, and `00_claim` across `~/.codex/skills`, `~/.codex/agents`, `~/.codex/AGENTS.md`,
and `~/.codex/config.toml` returns only the eleven `audit-*` agents, whose matches are the
intentional negative statements ("Standalone — needs no debate scaffolding", "do not look for
`00_claim.md`") that appear identically in fourteen of Claude's own agent definitions.

Skill rosters are now identical apart from `skill-creator`. Claude's twenty-two agents are all
present on the Codex side.

## Phase 2 — agent retirement and structural parity

The five Codex-only agents were retired at the user's direction: `data-engineer`,
`vfe-codebase-auditor`, `vfe-cross-manuscript-consistency`, `vfe-experiment-analyst`, and
`vfe-manuscript-reviewer`. Copies are preserved under
`~/.codex/_backup-20260816-074132/retired-agents/`. All five instructed the model to read a
knowledge base at `.Codex/agents/vfe-knowledge/*.md` that no longer exists, so they were partly
broken independently of the parity question. Agent rosters are now identical at 22 each.

Two capabilities the retired agents covered were rebuilt as skills rather than agents, since
adding agents raises fan-out cost and that was the defect being removed. `cross-manuscript-consistency`
audits notation, equation-form, citation-key, style, and narrative drift across the eight `.tex`
files in `Research\manuscripts\`, a gap `peer-review` does not fill because it owns whole-manuscript
review in the singular. `experiment-analysis` interprets run output — provenance pinning, anomaly
classification against literature priors, seed-count and power discipline, and next experiments
carrying explicit falsification criteria. Both are self-contained and do not depend on the missing
knowledge base.

Shared skills were converted from copies to Windows junctions pointing at `~/.claude/skills`.
Twenty-four were converted; `verification` was already a junction, which is precisely why it was
the only skill that had not drifted. Divergence is now structurally impossible rather than a thing
to remember. Propagation was verified by writing a probe string into a Claude-side skill,
confirming it appeared on the Codex side, and removing it.

Agents cannot be junctioned because the two harnesses use different formats, so they are generated
instead. `~/.claude/scripts/harness_parity.py` treats `~/.claude/agents/*.md` as the source of
truth and regenerates `~/.codex/agents/*.toml`, pruning orphans, with a `--check` mode that reports
drift and exits nonzero. Two defects in the initial converter were found and fixed by validating
every output with `tomllib`: Python's `repr()` emits `\'` for embedded apostrophes, which TOML
rejects, so a correct TOML basic-string encoder replaced it; and YAML-quoted frontmatter values
were being double-quoted. All 22 outputs now parse.

Regenerating from the Claude side initially dropped a `Research Vault (auto)` footer that existed
only in Codex's TOMLs. Rather than restore it downstream, it was added to the Claude `.md` sources,
because agent definitions state explicitly that `CLAUDE.md` does not auto-load into subagents —
meaning Claude's investigator agents had never carried the wiki pointer at all. Per-agent lens
wikilinks were recovered verbatim from the backup. A pre-existing inconsistency surfaced in the
process: five of six `verifier-*` agents already carried the footer and `verifier-adjudicator` did
not; it was made uniform.

A `SessionStart` parity-guard hook was added to both `~/.claude/settings.json` and
`~/.codex/hooks.json`, running `harness_parity.py --check`. It was tested by inducing drift in a
generated TOML, confirming detection and a nonzero exit, then restoring.

Both configuration directories were placed under git with allowlist `.gitignore` files that ignore
everything by default and re-include only tracked configuration, so credentials, transcripts, and
the telemetry database cannot be committed even as new files appear. `~/.claude` tracks 213 files
at commit `3345cc8`; `~/.codex` tracks 26 at `473f12d`, deliberately excluding `skills/` since
those are junctions into the Claude repo. `core.autocrlf` is `false` in both so skill bytes are not
rewritten on checkout.

## Phase 3 — skill cleanup and audit

Codex was launched and enumerated its skills, closing the outstanding load risk from phase 2. The
check found one genuine breakage first: `topology-geometry-guide`'s description was an unquoted
YAML scalar containing a colon-space, which a strict parser rejects. Claude's loader is lenient so
it had never surfaced, and Codex's prior single-quote normalization had been masking it — the
junction migration would have broken that skill on Codex. Fixed as a block scalar; all 31
Codex-visible `SKILL.md` files now parse and Codex enumerates every skill, with
`cross-manuscript-consistency` and `experiment-analysis` present and `red-blue-debate` absent.

`topology-geometry-guide` also carried `README.md`, `_toc.md`, and a `modules/` tree left by an
automated conversion dated 2025-11-08. They contradicted the real content, declaring it LOW
confidence and unverified, directing the reader to a research checklist before trusting anything,
ordering updates to `metadata.sources` and `metadata.confidence` fields absent from the
frontmatter, and calling an `adn_skills()` tool that does not exist here. `core-guidance.md` was a
strictly inferior duplicate of `SKILL.md`. All of it was deleted. Research wiki pointers were added
to the Riemannian, Lie-group, SPD, and gauge-bundle sections, naming only pages verified to exist
in the vault.

An audit of the remaining skills found one substantial defect. `research-paper-writing` contained a
185-line "Hermes Agent Integration" section written for a different agent platform: it documented
`skill_view()` and `skill_manage()`, a tool vocabulary of `delegate_task`, `execute_code`,
`web_extract`, `cronjob`, `send_message`, `todo`, and `memory`, a `.hermes/plans/` path, and six
skills that are not installed. Following it would have produced calls to functions that do not
exist. It was rewritten against this harness's actual tools, skills, and subagents, including the
project's CUDA-interpreter rule. Smaller fixes: an `arxiv` reference corrected to `arxiv-database`,
`web_search`/`web_extract` to `WebSearch`/`WebFetch`, a nonexistent `plotly` skill reference in
`networkx`, one UK spelling in `audit-numerical-analyst`, and two banned-phrase uses.

`~/.claude/scripts/audit_skills.py` was written to find these and retained. It checks frontmatter
validity, wikilink resolution against the vault, skill/agent/file reference resolution,
foreign-harness tool APIs, leftover conversion scaffolding, and the project's style rules. Its
first version produced 105 findings of which almost all were false positives — prohibition lists
counted as violations, Python list literals read as wikilinks, "meta-analyses" flagged as UK
spelling — so it was corrected to strip code and tables, skip lines stating a rule, and resolve
sub-skills, plugin skills, and built-in harness skills. It now reports zero findings. It also
reports that skill descriptions cost roughly 5,400 tokens of context in every session; that is
recorded as information, not a defect, since shortening descriptions degrades trigger accuracy.

The parity-guard hook proved itself during this work by catching the Claude-side spelling edit and
reporting the Codex agent as stale before it was regenerated.

## Phase 4 — agent audit

The mechanical checks in `audit_skills.py` already covered the agents and were clean, so this pass
read them. Four defects surfaced.

The six `verifier-*` agents declared no `tools`, and therefore inherited every tool including
`Write` and `Edit`. That contradicts their own design: each states that any uncommitted edit to a
tracked file invalidates the artifact pin it is validating, and each returns a structured result
that the *caller* writes into the ledger, so none has a reason to modify files. Explicit
least-privilege grants were added — read plus execute for the four gathering roles,
`Agent` additionally for the orchestrator because it dispatches views, and a narrower grant for the
adjudicator, which gathers no evidence at all. Scratch output still works through Bash redirection
into `.verification/`.

`verifier-adjudicator` carried a Research Vault footer copied from `verifier-skeptic` earlier in
this same session — a defect introduced by the phase-2 footer restoration, which had assumed the
blocks were uniform when they are in fact role-tuned in both their opening directive and their
closing line. It told the adjudicator to consult the wiki "before you build your attack" and to
"attack from the primary source", neither of which the adjudicator does. Rewritten for the role:
the wiki interprets already-recorded evidence and establishes scope and supersession, and can never
itself close a claim, because an out-of-tree file is not covered by the ledger's artifact pin.

Three agents — `audit-implementation-engineer`, `audit-numerical-analyst`, and
`performance-engineer` — instructed the model to use `.venv/Scripts/python.exe` at the repo root as
the CPU interpreter. No agent used the globally configured `$CPU_PYTHON` and `$CUDA_PYTHON`. That
matters because `.venv` exists in `V3_Transformer` and `MultiAgentELBO` but not in `vfe_4.0` or
`Research`, and because agents state explicitly that `CLAUDE.md` does not auto-load into them, so
there was no fallback to correct the drift. All three now use the env vars, which resolve
everywhere, with the repo-local venv noted as an alternative where present.

Nine `audit-*` descriptions advertised a five-field findings block while their bodies — and
`deep-audit` and `rigor-sweep` — specify six. The descriptions now name `Falsifies` too, which
matters because the description is what a dispatcher reads when choosing an agent and specifying a
format.

Checked and found sound, not changed: the cross-model verification policy is implemented in exactly
the eight roles `CLAUDE.md` names, with frontmatter `model` correctly documented in each as a
fallback for the default Opus deployment; `audit-implementation-engineer` omits the `Skill` tool
deliberately, since its lens is config tracing rather than symbolic verification; the apparent
generic web-framework content in `python-pro` and `performance-engineer` consists of negative
statements listing what does not exist in this codebase; and the dated freshness claims are
self-limiting and instruct re-verification before citing.

One parity limitation is worth recording: Codex agent TOML supports only `name`, `description`, and
`developer_instructions`. It has no `tools` or `model` field, so the least-privilege restriction and
the cross-model fallback apply on the Claude side only. Codex agents run with default tools.

## Phase 5 — hooks and settings audit

Hook wiring was verified by execution rather than inspection. Every referenced script resolves on
disk in both harnesses. The parity guard returns OK, the main guard exits 0 silently outside
`V3_Transformer`, and the verification gate returns `{}` with exit 0 on a well-formed Stop payload.
The gate emits `decision: block` only when its stdin does not parse, which is the correct
fail-closed posture for a gate and not a defect, though it does mean a change to the harness's hook
payload format would block every turn until noticed.

Two wiring defects were fixed. The Stop hook declared no timeout in either harness while every
`SessionStart` hook declared 20 to 30 seconds; because it runs at the end of every turn, a hang in
the gate would hang every turn. It now declares 30 seconds. Codex was also missing the
`v3-main-guard` `SessionStart` hook that Claude runs; since the script matches on the origin URL and
no-ops everywhere except `V3_Transformer`, running it on both is the parity-correct state. Both
harnesses now run an identical set of three `SessionStart` hooks and one `Stop` hook.

`permissions.allow` held 160 entries, of which 25 were provably dead and were removed. Twenty-one
name `V13_Gauge_Transformer`, a repository that no longer exists on disk; two invoke `/tmp` scripts
that are gone; `Bash(python3 -c ':*)` is malformed quoting superseded by the working
`Bash(python3 -c ' *)`; and `Bash(cat)` matches only a bare argument-less `cat`. The removal was
verified by comparing parsed objects rather than text: 25 removed, none added, order of survivors
preserved, and every non-permissions key unchanged. An initial write flipped the file to CRLF and
produced a 510-line diff; it was normalized back to LF, reducing the diff to the nine insertions and
thirty-three deletions that were actually intended.

`v3-main-guard.sh` and `claude-mem-autoheal.ps1` were read and found sound. The guard is
origin-URL scoped, fast-forward only, and always exits 0. The autoheal script resolves the worker
port from configuration rather than hardcoding it, acts only on the dead-owner wedge signature, and
pins claude-mem to 13.8.1. The two harnesses invoke it differently — Claude wraps it in
`claude-mem-nodew.exe` and Codex calls PowerShell directly — which is a deliberate difference to
suppress a console window, not drift.

Reported rather than changed, because these are the user's risk-posture choices: `permissions` has
135 allow entries and **zero `deny` and zero `ask` rules**, and the allow list includes
`Bash(rm:*)`, `Bash(curl:*)`, `Bash(git push *)`, `Bash(git add *)`, and `Bash(pip install:*)`.
Roughly forty of the surviving entries are hyper-specific one-offs, such as exact `sed -n '500,510p'`
line ranges, which are harmless but will never match again. Note also that the newly added
`autoMode` block soft-denies pushes to this public repository's default branch while
`permissions.allow` contains `Bash(git push *)`; which layer takes precedence was not determined
here and is worth confirming before relying on either. The project-local
`MultiAgentELBO/.claude/settings.local.json` carries the same one-off accumulation in ten entries
and was left alone.

## Outstanding

Tier 3 housekeeping (VACUUM of `logs_2.sqlite`, pruning `_backup-*`, clearing the stale
`.codex-global-state.json.tmp-*` files) was assigned to Codex and is not done here.

## Unresolved: `~/.codex/logs_2.sqlite`

The file is 3.87 GiB. It holds a single `logs` table of Rust `tracing` output written by the Codex
process itself — TRACE (420,860 rows), INFO (315,802), DEBUG (236,789), WARN (6,941), ERROR (108) —
dominated by `codex_api::sse::responses` and `codex_core::stream_events_utils` internals. This
content is never placed in the model's context window; it is local disk telemetry only, so it has
not been consuming context.

Row pruning is functioning: the autoincrement counter has reached 119,824,193 lifetime rows while
only 980,500 are retained. The problem is that the file is never compacted — 521,364 free pages at
4,096 bytes each amount to 1.99 GiB of freed-but-unreclaimed space against 1.88 GiB of live data.
Running `VACUUM`, or simply deleting the file while Codex is closed (it is a log and is recreated
on next start), reclaims roughly 2 GiB. This was not performed because Codex was running and
holding the database open.
