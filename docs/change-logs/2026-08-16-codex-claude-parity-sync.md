# 2026-08-16 — Codex/Claude harness parity sync

Scope: user-level harness configuration under `~/.codex` and `~/.claude`. No repository source
files were modified by the harness work.

A second, unrelated workstream later the same day edited `solid_RG_theory.tex`; it is recorded in
the final section of this document, "Expository pass on `solid_RG_theory.tex`".

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

The remaining observations concern the permission configuration's breadth and layering, and were
reported to the user rather than changed, since they are deliberate risk-posture choices rather
than defects. Roughly forty of the surviving entries are hyper-specific one-offs, such as exact
`sed -n` line ranges, which are harmless but will never match again. The project-local
`MultiAgentELBO/.claude/settings.local.json` carries the same accumulation in ten entries and was
left alone. Details are in the configuration itself rather than recorded here.

## Phase 6 — claude-mem outage and autoheal repair

The claude-mem plugin update to 13.15.0 wedged the memory system for roughly twenty minutes. The
episode is worth recording because Phase 5 read `claude-mem-autoheal.ps1` and pronounced it sound.
That assessment was wrong. The script's detection logic was correct and its kill logic had gone
stale, so it ran at session start against precisely the failure it was written for and healed
nothing.

At 09:55:39 the plugin observed that the running worker was 13.8.1 against a 13.15.0 plugin and
recycled it. Graceful shutdown failed, reporting "Server is not running". The worker process died,
but `chroma-mcp.exe` — which the worker had spawned two seconds after binding its HTTP listener —
retained an inherited handle to that listening socket, so port 37780 remained in LISTEN attributed
to the dead worker pid 12152. Every replacement worker then failed to bind, and the supervisor's
liveness check, satisfied by the stale socket, short-circuited each retry with "Worker PID file
points to a live process, skipping duplicate spawn". Wedged spawn attempts accumulated to 105
processes. The `supervisor.json` bookkeeping was wrong on both tracked processes, naming a dead
worker and a dead chroma while a different chroma held the port.

The symptoms were diffuse enough to be worth naming. MCP search timed out at its configured
45,000 ms; `claude-mem status` hung for seven minutes, then reported "port in use but health is
unreachable" and exited 0, so anything gating on its exit code would read the wedge as healthy; and
the `UserPromptSubmit` hook timed out at 60 seconds. Killing all 105 accumulated processes did not
free the port. Only killing the chroma tree released the socket, whereupon a pending spawn bound it
and came up healthy from the versioned cache path rather than the marketplace path.

The guard failed for two independent reasons, each sufficient on its own. Chroma now runs from the
uv cache at `AppData\Local\uv\cache\archive-v0\...\Scripts\chroma-mcp.exe`, so it matched neither
the `Name='python.exe' OR Name='pythonw.exe'` filter nor the requirement that the command line
contain `\.claude-mem`; the holder was excluded twice over. Separately, workers now run under
`bun.exe`, so the `Name='node.exe'` filter matched nothing at all. Both filters were rewritten to
match on process identity rather than host binary or install location, and the two full
`Win32_Process` enumerations were collapsed into one, since a wedge can leave more than a hundred
processes behind and the scan runs against a hook timeout. That timeout was raised from 20 to 45
seconds in `~/.claude/settings.json`.

The patch was verified three ways. Run against the healthy worker the script is a no-op, exiting 0
in 0.94 seconds with the worker and its health endpoint untouched, because it short-circuits before
the enumeration. Compared side by side on live processes, the new chroma filter matches five
processes including `chroma-mcp.exe` where the old matched two and missed the holder entirely, and
the new worker filter matches the live bun worker where the old matched nothing. Both
`mcp-server.cjs` processes, which Claude Code and Codex manage, are excluded by the new filters.

The global npm CLI was updated from 13.5.4 to 13.15.0 so that CLI, plugin, and worker agree; the
install did not trigger a recycle and the running worker survived it. Two notes on the guard's own
drift: the 13.8.1 version pin recorded in Phase 5 was retired earlier the same day, and the
`$fixedCache` path it leaves behind still points at a 13.8.1 directory.

The underlying defect is upstream and unfixed. The bundled `worker-service.cjs` launches chroma
through the MCP SDK's `StdioClientTransport`, which spawns with
`stdio: ["pipe","pipe", stderr ?? "inherit"]` and `shell: false`. Passing stdio handles forces
`bInheritHandles=TRUE` on the Windows `CreateProcess` call, which duplicates every inheritable
handle in the worker into the child, the freshly bound listener socket among them. Ordering the
spawn before the bind, marking the listen socket non-inheritable, or spawning chroma from a helper
process that owns no listener would each break the chain. Upstream is already adjacent to this,
having fixed `isPortInUse` returning false for zombie-held ports in v13.12.2, which addresses the
symptom rather than the inheritance that produces it. Until that changes, any worker recycle while
chroma is running can re-pin the port, and version bumps are exactly what trigger recycles.

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

---

# Expository pass on `solid_RG_theory.tex`

Scope: `solid_RG_theory.tex` only. Driven by a reader punch list of undefined terms, undefined
symbols, missing figures, one notation collision, and one overstated certification claim. Four
parallel investigator agents traced every item to the canonical sources before any edit was made;
no definition below was invented.

## Definitions added

- **New Section 2, "The four objects."** Prose definitions of the generative law, the recognition
  law, the posterior, and the Markov channel, placed before the physics dictionary. Records why the
  generative law is fixed before recognition (a moving joint leaves no fixed evidence target), what
  "selected version" means (conditional probability is unique only up to an observation-null set),
  and what "normalized" buys over an aggregation matrix or Galerkin projection.
- **New Section 3.2, "Kernels, presentations, and the evaluation map."** Defines a kernel, defines a
  *generative* kernel as one conditional factor of the DAG-ordered composition, and explains `ev_i`
  as compile-and-instantiate from a model presentation to that kernel. States the three distinct
  types (law over presentations / presentation / kernel) and why non-injectivity of `ev_i` is
  retained rather than quotiented away.
- **Section 4.1.** Defines `p_i^x` and `T_ij^x`, with `T^q = Omega` and `T^m = Omega-tilde`, and the
  reciprocity condition. These were previously used in eq. (4) without ever being introduced.
- **Section 4.4.** States the two-channel zero-distortion theorem explicitly as a three-way
  equivalence, and defines the path transport `T_{gamma_i}` and the root-frame law
  `P_i = (T_{gamma_i})_# p_i`. Previously the theorem was referenced by name only.
- **Section 5.1.** Defines the structural data `X` (DAG, design incidence, geometric data, fixed
  mechanism parameters) and why it stays outside the channel; explains `do`/`dy` as integrator
  notation rather than derivatives; explains absolute continuity and why its failure is `+infinity`
  rather than a large finite penalty.
- **Section 8.1.** Defines "comparison law" as the free variable of the optimization and explains
  the extended support convention.
- **Section 9.1.** Defines the normalized membership channel and contrasts it with a replicated
  cover, whose column sums exceed one.

## Sections rewritten for motivation

- **Section 5.3 (new), "The parent evaluator."** Unpacks "induced from the pushed generative law by
  disintegration" into the disintegration statement, the direction of conditioning, and the
  compatibility identity. Adds the binary witness showing why a predeclared evaluator needs
  almost-sure agreement: the swapped family `ev'(m) = K_{1-m}` is equally normalized and equally
  measurable yet disagrees on parent mass 1/2.
- **Section 5.4.** New opening paragraph stating the argumentative role of the section: it closes off
  the cheaper route in which the consensus pair `(Q_q, Q_m)` would be declared the meta-agent. Adds
  that both directed divergences between the two joints are `+infinity`, so marginal agreement
  coexists with maximal joint disagreement.
- **Section 6.1.** Explains the fiber picture behind "disintegrate over the parent state," and
  replaces the bare assertion about the weighting measure with the reason: relative entropy is an
  expectation under its left argument, so the weight must be the recognition marginal.
- **Section 8.2.** New opening explaining why the section exists (the zero-distortion theorem is
  otherwise a knife-edge result), plus the explicit bound: `delta_x = sqrt(eps_x / (2 eta_min))`
  uniform per tree edge, then `dist_T(u,v) * delta_x`. States the two costs, linear accumulation in
  graph distance and spanning-tree dependence.
- **Section 9.2.** Adds the type-mismatch argument for why the joint edge-event law pushes forward
  and the conditional attention row does not, with a worked finite case: pushing the joint gives the
  parent row `(0.45, 0.55)`, row averaging gives `(0.25, 0.75)`. Verified by direct computation.
- **Section 9.3.** Unpacks conditional boundary marks, connected-component labels, and internal
  based holonomy, why averaging leaves the group (mean of the two planar quarter-turns is the zero
  matrix), and what "another theorem" would have to supply.
- **Section 10.1.** States up front that the comparison theorem is open, so the definition precedes
  the result it serves. Explains analyst-declared probe, declared preparation law, the hard/soft
  distinction against Pearl's do-operator, and what "typed" means. Adds the binary-symmetric-channel
  non-identifiability witness: `(a,b) = (1/4,1/3)` and `(1/3,1/4)` share the passive law
  `(7/24, 5/24, 5/24, 7/24)` but respond differently to `do(E=0)`. Verified by exact rational
  computation.

## Defects corrected

- **Notation collision on `R`.** Section 8.1 used `R` for an arbitrary comparison law while Section
  10.1 uses `R` for the retained input of the `R -> E -> O` chain. Section 8.1 is renamed to `Q`,
  matching `Theory/06_general_coarsegraining.tex`; Section 10.1 keeps `R`, which is canonical
  throughout `Theory/05d_relational_inference.tex` and `Theory/appendix_notation.tex`. A
  translation box records the disambiguation.
- **Overstated certification status.** The "What is established" box claimed
  `COMPLETE_AFFIRMATIVE`. The release file records `COMPLETE_AFFIRMATIVE_WITH_CORRECTIONS`, which
  is not among the three terminal values the release schema admits, and the package does not pass
  its own release-mode validator (invalid status token plus several stale artifact hashes, both
  documented in the package erratum as deliberate). The box now reports the ledger state
  `EVIDENCE_VERIFIED` and the boundary box carries the packaging caveat.
- **Unexplained digest.** New Section 12.1 explains that the 64-hex string is the SHA-256 of the
  canonical JSON serialization of the frozen `target` object in the package problem contract, why a
  digest is quoted at all, and what the frozen conjunction asserts.
- **Provenance gap.** Section 14 now lists `Theory/03_probability.tex`, `Theory/04_generative.tex`,
  `Theory/05d_relational_inference.tex`, and the two appendices among the canonical sources, and
  records that the two-channel theorem in its edge-weighted form and the forward-KL barycenter
  identity live in the 2026-08-14 derivation package rather than in the theory chapters. Also flags
  that "two-channel theorem" is this guide's shorthand and collides with an unrelated finite-ELBO
  result elsewhere in the project docs.

## Figures added

Three hand-coded TikZ figures, each rendered and visually inspected before integration. `tikz` and
its libraries were added to the preamble, along with a `deepgreen` color.

1. **Figure 1 (Section 5)** — the coarse-graining step: fine triple, one common channel acting on
   all three laws, parent triple, external conditioning on `(X, o)`, and the defect identity.
2. **Figure 2 (Section 6.1)** — disintegration over the parent state: fibers, the blow-up of one
   fiber showing a sharp recognition conditional against a broad posterior conditional, and the
   between-fiber / within-fiber split of the chain rule.
3. **Figure 3 (Section 9)** — network coarse-graining: soft membership channel with a split child,
   pushforward of the joint edge-event law, recovery of the parent occupancy and attention row.

## Verification performed

- `latexmk -pdf` to a fixed point: 0 errors, 0 undefined references, 25 pages.
- Each figure rendered standalone to PNG and inspected; collisions found and fixed in all three
  (overlapping call-out, label-on-arrowhead, self-loop labels behind the formula box).
- The two new numerical examples were computed rather than quoted: the attention-row pushforward
  discrepancy and the binary-symmetric-channel passive/interventional laws, the latter in exact
  rational arithmetic.

Not done: no `.pdf` was written into the repository, and the release package's validator failures
were reported in the manuscript but not repaired.

## Grand-canonical network and meta-agent manuscript

Added `Theory/grand_canonical_meta_agent_formation.tex`, a physicist-facing development of the
network thermodynamic analogy. The manuscript uses the exact row free energy, separates the
adaptive fine-agent network from literal grand-canonical edge occupation, constructs pointwise
meta-agents and their recursive network, and records the participatory nonequilibrium extension as
a conditional proposal rather than an established theorem. Four hand-coded TikZ figures show the
fine network, the edge-occupation threshold, the meta-agent feedback loop, and the recursive tower.

---

# New companion manuscript: `physicists_companion.tex`

Scope: one new file, `physicists_companion.tex`, plus a small style fix applied to
`solid_RG_theory.tex`. Requested as a graduate-physicist-level orientation to the *full* theory
buildout (`Theory/main.tex`, 17 chapters in four parts plus three appendices), in the same visual
and rhetorical style as `solid_RG_theory.tex`, with physical analogies.

## Sources read

The document was written against the manuscript, not from memory. Read in full:
`Theory/01_introduction.tex` (which carries the program's own reading map and status taxonomy),
`Theory/02_geometry.tex`, `Theory/11_obstructions.tex`, `Theory/12_philosophy.tex`, and
`Theory/appendix_claim_ledger.tex` (the central open-obligation ledger). Read in part:
`Theory/05b_local_collective_elbo.tex` (collective/local VFE and the attention section),
`Theory/05c_pullback_geometry.tex` (covariant jets and pullback tensors),
`Theory/07_general_renormalization.tex` (the scale category),
`Theory/08_infogeometry.tex` (gauge invariants of the interaction precision). The full index of
typed results (`\theoremheading`, `\conjectureheading`, `\openproblemheading`) was extracted across
all chapters to fix what is proved versus conjectured versus open.

## Structure of the new document

Thirteen sections, 21 pages. Orientation and a one-paragraph summary; a physicist's dictionary
table; the gauge structure (base, two associated representations, law-valued fibers, three
holonomies); the variational core (evidence/ELBO/free energy, the typing prohibition, infinite
penalties); many agents (collective versus local free energy, attention); information geometry on
the base; coarse graining and renormalization; the Gaussian realization; the reciprocal-fold no-go;
a status table; takeaways; a reading path.

## Physical analogies used, and their fidelity

Deployed where the correspondence is exact and labeled as suggestive where it is not:

- `Theta_e` as a lattice link variable and `H(gamma)` as a Wilson loop. Exact — including the
  trivializing criterion, which is literally the lattice statement that a configuration is pure
  gauge iff every Wilson loop is trivial.
- The two associated bundles as two matter sectors in inequivalent representations (fundamental
  and adjoint). Exact for the group action; the departure is that the fibers are spaces of
  probability laws and the group acts by pushforward, which is called out explicitly.
- `A_i = (u_i)^* omega` with the `Ad + Maurer-Cartan` law as the gauge potential. Exact.
- The exact evidence identity as the Gibbs-Bogoliubov-Feynman bound, with the gap being the
  relative entropy of the trial ensemble against the true one. Exact structural match.
- The typing prohibition as "you may not let the Hamiltonian depend on your trial state".
- Subspace-supported recognition laws costing `+infinity` rather than a large finite penalty.
- The local-global potential identity as exact block-coordinate descent on one Landau-type
  functional (cavity/block mean field made exact), including why parallel updates fail.
- Softmax attention as a Gibbs measure over which neighbor to attend to, with `pi` as degeneracy
  and `tau` as temperature; its natural-gradient flow is the replicator equation with descent rate
  equal to minus the variance of the fitness-like quantity (Fisher's fundamental theorem shape).
- Fisher metric as a susceptibility (Hessian of the log partition function; fluctuation-response).
- The pullback `h_s^omega` as an induced metric in the worldvolume sense, explicitly relative to a
  connection that is never canonically chosen.
- Blocking as Kadanoff block-spin, with exact closure generating hyperedges read as the familiar
  proliferation of couplings.
- The scale-diagram-versus-RG distinction as the rescaling step after blocking, with the honest
  note that here the rescaling is declared rather than derived.
- Pencil invariance as "only dimensionless ratios are physical": a reframing `T = cI` rescales the
  ordinary spectrum by `c^-2`, so absolute-eigenvalue thresholds are chart statements.
- The flat unanchored reciprocal fold as a pure-gauge zero mode, with `det J = det(I-H)^2 /
  (det R_e det R_f)` depending on the links only through the Wilson loop, and nontrivial holonomy
  lifting the degeneracy — presented as the Aharonov-Bohm situation, where a ring degeneracy
  depends only on the enclosed flux and threading flux splits it.
- Precision addition as inverse-variance weighting with transports inserted, arising as a theorem
  rather than a convention.

## Honesty content carried over from the manuscript

The document reproduces the manuscript's status discipline rather than smoothing it. It states
that the base is not spacetime and carries no signature, causal cones, measure, or field equation;
that Fisher duration is not physical time; that RG depth is not inference time; that graph-link
holonomy is not evidence of base curvature or bundle topology; that no canonical connection is
selected anywhere; that there is no continuum limit, no thermodynamic limit, no derived rescaling,
and no proved nontrivial fixed point with a basin; and that identification of any limiting object
with a physical law is open. A status table summarizes established / hypothesis / numerical / open
/ not-claimed across the whole program.

## Figures added

Three hand-coded TikZ figures, each rendered standalone and visually inspected before integration:

1. **Figure 1** — the ambient geometry: base, principal fiber with two frame choices related by
   `h`, belief fiber drawn as a covariance ellipse, model fiber drawn as a law over presentations,
   two connections transporting along a base curve, and the cross morphisms.
2. **Figure 2** — three holonomies side by side (graph-link, base-connection, Cech class) with a
   footer stating exactly what would be needed to identify any two of them.
3. **Figure 3** — a scale diagram versus a renormalization map, showing that the declared
   identifications `I_l` are what make a fixed point a well-posed question.

## Also changed

`solid_RG_theory.tex`: removed the LaTeX spacing macros (`\,`) introduced in the earlier pass, per
the house rule against them. Seven occurrences in the new document and three in the older one were
rewritten; both still compile identically.

## Verification

- `physicists_companion.tex`: `latexmk -pdf` to a fixed point, 0 errors, 0 undefined references,
  0 overfull boxes, 21 pages.
- `solid_RG_theory.tex` after the spacing-macro edit: 0 errors, 0 undefined references, 25 pages.
- Each figure rendered standalone to PNG and inspected; collisions found and fixed in all three
  (arc/label collisions in Figure 1, a reserved-key clash and formula overlaps in Figure 2, and a
  footer box that was shrinking Figure 2's panels inside `\resizebox`).
- Style checks run over the new document: no banned phrases, no British spellings, no LaTeX
  spacing macros.

Not done: no `.pdf` was written into the repository, and no claim in the manuscript was
independently re-verified — the companion reports the manuscript's own status tags rather than
re-adjudicating them.
