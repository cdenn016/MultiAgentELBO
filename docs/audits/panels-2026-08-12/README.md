# Recovered agent-panel returns, 2026-08-12 (landed 2026-08-13)

Two panels were dispatched on 2026-08-12 and the session ended before either reported. These files
are their **verbatim returns**, recovered on 2026-08-13 from the `journal.jsonl` of each workflow
transcript directory, exactly as the recovery procedure in the worklog anticipated.

**Read the digested version first:**
`docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md` §4b. It reconciles every result
against the prior art in §3b (PA-1…PA-13), which both panels ran blind to, and records which claims
survived their adversarial pass. These raw files are the evidence behind that section.

## Panel A — `wf_f576312d-d2a`, continuum action

14 agents dispatched, **13 returns recovered**. Structure: 3 grounding extractors → 5 derivations
(effort max) → 1 dedicated adversarial skeptic per derivation (effort max) → 1 synthesis.

| File | Role | Headline |
|---|---|---|
| `panelA-ground-01-pifb2-deployed-action.md` | grounding | the deployed five-term PIFB2 action, term by term, with line citations |
| `panelA-ground-02-effective-action-run-and-Ch.md` | grounding | `C_h`, `eps_h`, `c_h` as they actually appear in the corpus; confirms the tautology |
| `panelA-ground-03-theory-corpus-sweep.md` | grounding | what `Theory/` already contains: no lattice, no base-gradient energy, no curvature term |
| `panelA-T-GRAD-derivation.md` | derivation | PARTIAL — covariant Dirichlet limit proved; Part II claims a mass-term refutation |
| `panelA-T-GRAD-skeptic.md` | skeptic | `survives: false` — **but strengthens Part I and overturns Part II**; supplies the connection mismatch |
| `panelA-T-CURV-derivation.md` | derivation | PARTIAL — Fisher-weighted Yang–Mills, conjugation-invariant for noncompact `G` |
| `panelA-T-CURV-skeptic.md` | skeptic | `survives: false` — invariance survives exactly; adds a necessary support hypothesis |
| `panelA-T-RESID-derivation.md` | derivation | PROVED — closed forms for `eps_h` and `c_h` |
| `panelA-T-RESID-skeptic.md` | skeptic | `survives: false` — headline vacuous, statement (4) false; the residual identity survives |
| `panelA-T-COEF-derivation.md` | derivation | PARTIAL — temperatures are block counts; deployed pair OBSTRUCTED |
| `panelA-T-COEF-skeptic.md` | skeptic | `survives: false` — **reversal**, not correction; see worklog §4.4, unresolved |
| `panelA-T-SIMUL-derivation.md` | derivation | PARTIAL — the same-time/lagged bridge is refuted |
| `panelA-T-SIMUL-skeptic.md` | skeptic | **`survives: true`** — the only certified target |

**Lost:** the synthesis agent (`a809b31ccfc755523`), cut mid-run with no salvageable text. The
synthesis in worklog §4.7 was written by hand in its place.

## Panel B — `wf_0bb5bbd2-10a`, induced-volume action

9 agents dispatched, **3 returns recovered** — the derivation tier only.

| File | Role | Headline |
|---|---|---|
| `panelB-V-EXIST-derivation.md` | derivation | OBSTRUCTED — non-coercive on `Diff` orbits; `S_vol` is the *unique* invariant scalar |
| `panelB-V-TYPE-derivation.md` | derivation | OBSTRUCTED — typing is mixed and the load-bearing half is generative |
| `panelB-V-BRIDGE-derivation.md` | derivation | PARTIAL — refuted at `d >= 3`, **genuine variational bound at `d = 2`** |

**Lost:** V-DIFF (`aeec2824a94f01c83`) and the entire skeptic tier, all cut mid-run with no
salvageable text. The three surviving agents were mutually blind and converged, which partly
substitutes for the missing adversarial pass — but only on the points where all three agree. Panel B
results carry correspondingly less weight than Panel A's.

## Provenance and caveats

- Recovered from `journal.jsonl` in each workflow's transcript directory; `resumeFromRunId` does not
  survive a session boundary, so the journal was the operative route.
- Files are rendered from the agents' structured returns. Field order is normalized for reading;
  **no content is edited, summarized, or abridged**.
- Both panels ran **without sight of** `docs/audits/roadmap-review-2026-08-12/` (`rm-01`…`rm-06`).
  Novelty claims in these files are therefore unreliable where they overlap PA-1…PA-13 — most
  sharply on T-CURV, where the Fisher-dressed curvature repair was already named in `rm-03` §0.
  Worklog §4b does that reconciliation; these files do not.
- Skeptic `survives: false` does **not** mean the target failed. In three of four cases the skeptic
  kept the substantive result and corrected its framing or hypotheses. Read the
  `corrected_statement` field, not the boolean.
