# Ultradeep peer review of `Theory/` — INTERIM record

**Manuscript:** *Gauge-Covariant Variational Free Energy and Renormalization* (Robert C. Dennis),
`C:\Users\chris and christine\Desktop\MultiAgentELBO\Theory` — 22 `.tex` files, ~13,000 lines,
1,687 `\status{}` tags, 306-line open-obligation appendix.

**Date:** 2026-08-09. **Status: INCOMPLETE — session budget exhausted mid-pass.**
This file exists so the pass can be resumed without re-running the agents that already finished.

## Step 0 findings (settled before review began)

- The vault ledger `C:\Users\chris and christine\Desktop\Research\manuscripts\verified-ledger.md`
  (545 lines) covers GL(K), PIFB/PIFB2, belief_inertia, meta_entropy, and the MAgent exact-ELBO
  white paper. It has **zero entries for `gauge_vfe_rg`**. This is the manuscript's first recorded
  referee pass; nothing was pre-settled, and every lens reviewed cold.
- `Theory/` is byte-identical to the vault's `manuscripts/gauge_vfe_rg` (four files spot-checked
  with `diff -q`; `docs/theory-provenance.md` records all 44 files matching by SHA-256). No
  snapshot-drift problem to review around.
- Review rule given to every agent: items honestly fenced OPEN in `appendix_claim_ledger.tex` are
  **not** defects. A finding against a fenced item counts only if the fence is in the wrong place
  (something used as established secretly depends on the open item) or the fenced statement is
  itself wrong.

## Panel deployment

Wave 1 — domain lenses (8): gauge theory (`02`, `05c`, `11`); differential geometry (`02`, `05c`,
`05d`); information geometry (`05a`, `08`, `05c` Fisher/Amari only); variational + measure theory
(`03`, `04`, `05`, `05b`); RG/stat-mech (`06_general`, `07_general`); exact network RG (`07b`, its
own agent — 2,828 lines); numerical/matrix analysis (the five Gaussian chapters + numerical
provenance); philosophy of science (`01`, `12`, `11`, claim ledger).

Wave 2 — cross-cutting (4): citation/primary-source + prior-art positioning; notation/label/counter
integrity; verification-harness fidelity; cross-chapter dependency and hypothesis discharge.

Wave 3 (adversarial skeptic pass) — **not run.** Findings below are therefore *unverified by an
adversarial pass* except where two independent lenses converged, which is noted inline.

**Completed at time of writing: 2 of 12.** Ten agents were still running.

---

## COMPLETED — Verification-harness and numerical-claim fidelity

All evidence below came from executed commands (hashing, grepping, targeted recomputation), not
from reading the manuscript's self-description.

### V1 (critical) Two of three load-bearing numerical claims have no executed evidence

`claims.json` declares 30 checks (union of `check_ids` and `supplemental_check_ids`);
`current-results.json` contains 29. The missing one is `CHK-CG-FACTOR-GAP-STRESS-3138`.

Both load-bearing appendix claims — `NUM-CG-FACTOR-GAP-STRESS-SCHEDULE` and
`NUM-CG-FACTOR-GAP-BOUNDARY-PROTOCOL`, i.e. `appendix_numerical_provenance.tex:71` and `:128` —
map to exactly that one check. The artifact's `summary.checks` reads `{"PASS": 29, "FAIL": 0,
"INCONCLUSIVE": 0}`. The 3,138-case protocol has never been recorded as run in any committed
artifact. The third load-bearing claim (`NUM-GAUSS-CONDITIONING`) does have artifact evidence.

*Fix:* run the governed 30-check regeneration and commit it, or retag `:71` and `:128` to an
explicitly unexecuted status and set `current_protocol_reproducible: null` with a
`missing_obligation` in both `claims.json` entries.

### V2 (critical) The appendix publishes 16 measured quantities with no machine-readable backing

`appendix_numerical_provenance.tex:43–58` prints an eight-row table of achieved condition-number
minima and maxima. Those are reductions computed at runtime (`run_checks.py:4866–4881`), not
declared constants. Grepping all seven distinctive mantissas against `run_checks.py`,
`claims.json`, and `current-results.json` returns **no matches**. Sixteen published numbers with
zero backing.

This contradicts the appendix's own rule 28 lines earlier (`:28`): "The generated JSON record is
the authority for exact counts and numerical values; this appendix intentionally does not
duplicate seed lists or result tables that can drift."

By contrast the four boundary-witness values *are* frozen constants at `run_checks.py:118–123`
matching the appendix exactly — so those are declared expectations, not measurements. But `:94–95`
says "The check mechanically recomputes all four quantities and requires PASS," and no artifact
records that PASS.

Main text is otherwise clean: a sweep of all 24 `.tex` files for artifact-derived numeric literals
found only the two appendix tables. No chapter quotes a residual, tolerance, or PASS status
sourced from the stale artifact. Two present-tense overreaches: `06_gaussian.tex:294` "its current
output corroborates the characterization" and `:351` "Its output concerns only that sampler."

### V3 (high) Source binding is void — and by far more than "older artifact" conveys

Recomputed SHA-256 over raw bytes for all 24 manifest entries. Path mapping holds 1:1
(`source_root: manuscripts/gauge_vfe_rg` → `Theory/`, 24 = 24, nothing missing either direction).

    MATCH   (1): 06a_generative_gaussian.tex
    DRIFTED (23): total byte delta = +302,996
      07b_agent_network_rg.tex        41,612 ->  136,451   +94,839
      05d_relational_inference.tex    36,841 ->   84,440   +47,599
      05c_pullback_geometry.tex       37,884 ->   67,859   +29,975
      07_general_renormalization.tex  26,906 ->   53,716   +26,810
      appendix_notation.tex           12,282 ->   31,717   +19,435
      appendix_numerical_provenance.tex 2,089 ->    8,824    +6,735
      ... 17 more

    protocol_files:
      run_checks.py    manifest=101,898  disk=401,798  delta=+299,900
      VERIFICATION.md  manifest=  3,185  disk= 21,270  delta= +18,085
      claims.json      manifest=  8,883  disk= 11,452  delta=  +2,569
      requirements.txt manifest=     38  disk=     89  delta=     +51

The artifact was not produced by a slightly earlier package. It was produced by a runner one
quarter the current size, against a manuscript ~300 KB shorter, under a different inventory and a
6.7× shorter protocol document. The artifact records `inventory.observed_total: 11` against 13
tags today, because `appendix_numerical_provenance.tex` carried zero `\status{NUMERICAL}` at run
time and now carries two — the two load-bearing ones.

*Fix:* state the drift quantitatively in the appendix rather than as "older".

### V4 (high) `CHK-RG-NONCOMMUTING-FLOATING` is structurally incapable of failing

`run_checks.py:5455–5481`, gate at `:5461`:

    bar = q.T @ lap @ q
    quotient_eigen = sla.eigvalsh(bar, bar)          # generalized pencil (bar, bar)
    quotient_error = float(np.max(np.abs(quotient_eigen - 1.0)))
    passed = quotient_error <= 1.0e-10

This solves `bar v = λ bar v`. For any SPD `bar` the spectrum is identically 1, regardless of
whether `lap` is a graph Laplacian, whether `q` spans the positive quotient, or whether any
manuscript claim holds. Confirmed adversarially: `bar = diag(1e-3, 7.0, 900.0, 2.5)` gives
`[1. 1. 1. 1.]` and passes. The recorded `quotient_eigenvalue_max_error: 8.881784197001252e-16` is
LAPACK `sygv` roundoff, ~6 orders inside the gate. The check measures the linear-algebra backend,
not the theory — and `VERIFICATION.md:333` declares supplemental checks "remain mandatory."

*Fix:* compare against an independent reference form, matching the sibling `check_rg_mass_pencil`
pattern at `:5493`; or drop it and remove it from `supplemental_check_ids`.

### V5 (medium) The 3,138-case acceptance band is 1e-4 relative, not reference-grade

`run_checks.py:4790–4799`:

    tolerance = max(_roundoff_scale(record.value, reference, dimension=..., multiplier=512.0),
                    1.0e-4 * abs(reference),
                    2.0e-8)

The roundoff term never binds — it would require `512·n·ε > 1e-4`, impossible for n ≤ 16. Measured:
at n=16 the active tolerance is 2.278e-03, which is 5.5e7× the roundoff term and ~6.4e11 ulps wide.
The tolerance is honestly declared in `claims.json.stated_tolerance`; the problem is the prose,
which presents "3,138 successful independent 100-digit exact-binary64 references" as the accuracy
evidence. A 100-digit reference discriminating at 1e-4 buys little over binary64. The all-case and
control paths also use different multipliers (512.0 vs 256.0) with no stated reason, declared
nowhere.

### V6 (medium) The check named "conditioning" never gates on conditioning

`run_checks.py:2202–2270`, gate at `:2246`. `condition_numbers` is computed for all 200 draws and
reported (`median 96.06`, `maximum 2743.45`) but appears in no predicate. The gate is
`min(min_eigenvalues) > 0 and nullity == k and symmetric_offdiag_controls == 0`. Of these,
positive-definiteness is near-automatic: self terms are built as `m @ m.T / k` with `m` a k×k
standard normal (`:2217`), SPD almost surely. The one discriminating predicate is the negative
control. Backs `\status{NUMERICAL}` at `06_gaussian.tex:351`, `load_bearing: true` — the only
load-bearing claim with artifact evidence. The manuscript sentence is appropriately hedged, so the
claim is not overstated; the check is weaker than its name.

### V7 (medium) 19 of 29 checks discharge nothing; 22 cited claim ids do not exist

Checks discharging no `claims.json` entry: all 12 CG checks and all 7 RG checks — the bulk of the
suite and the ones nearest the paper's title. They cite 22 claim ids absent from `claims.json`
(`NUM-CG-AGGREGATION`, `NUM-RG-GENERALIZED-SPECTRUM`, `SUPPLEMENT-RG-NONCOMMUTING-FLOATING`, …).

Cause: the five CG/RG chapters carry `NUMERICAL = 0` — all `ESTABLISHED`/`DEFINITION`/
`HYPOTHESIS`/`OPEN`. That is a defensible design (`VERIFICATION.md:332–334` explains the tightened
manuscript stopped tagging every corroborating endpoint), but the validator only enforces
claim→check (`run_checks.py:9427–9430` reads `claim["check_ids"]` only), so the reverse direction
has rotted freely. Same asymmetry at `check_cg_factor_gap_stress` (`:4988`), which declares only
`NUM-CG-FACTOR-GAP-BOUNDARY-PROTOCOL` while `claims.json` maps both load-bearing claims to it.

### V8 (medium) `VERIFICATION.md` describes a package the artifact cannot instantiate

| VERIFICATION.md | artifact |
|---|---|
| `:220–222` "30 deterministic checks plus `CHK-SOURCE-INVENTORY`; PASS requires all 31" | 29 checks, no `CHK-SOURCE-INVENTORY` |
| `:81` "closes the schema-3 result envelope" | `"schema_version": "2.1"` |
| `:6` "13 literal `\status{NUMERICAL}` tokens: 11 substantive" | `total_NUMERICAL_occurrences: 11`, `substantive_claims: 9` |

`run_checks.py:8494–8497` uses `zip(raw_checks, PRODUCTION_CHECK_IDS, strict=True)` with 30
expected ids, so the committed artifact cannot be re-verified even in `--verify` mode; it raises
rather than reporting FAIL. `VERIFICATION.md:69–73` does disclose the 29-check status, but the
surrounding document describes the 31-check contract in the present tense.

### V9 (medium) The declared source-binding gate is unsatisfiable in this checkout

`VERIFICATION.md:156–162` states the manifest comparison "admits no line-ending normalization …
A Windows checkout materialized with CRLF while `S` stores LF is therefore rejected." The repo
configures exactly that: `.gitattributes:4` is `Theory/** text eol=crlf`; `git check-attr` confirms
`eol: crlf`; blob-vs-worktree deltas equal the line counts (`06_gaussian.tex` 38,957 → 39,329).
Under the stated rule, the regeneration the appendix says "remains required" would be rejected in
this checkout before any check ran.

*Note:* this is scoped to the snapshot repo. The manuscript's home is the Research vault, where
the layout differs — confirm there before acting.

### V10 (clean, credit in the report) Inventory completeness and drift

`claims.json`'s assertion "One entry corresponds to one literal `\status{NUMERICAL}` occurrence"
holds **exactly**: 13 occurrences across 6 files (`01_introduction` 2, `06_gaussian` 3,
`07_restrictions` 1, `08_infogeometry` 3, `11_obstructions` 2, `appendix_numerical_provenance` 2),
13 entries, every `occurrence_index` resolving, zero uninventoried, zero line drift. The inventory
layer is sound; the evidence layer beneath it is not.

---

## COMPLETED — Philosophy of science / framing

Tag census in scope: 847 macros — 501 ESTABLISHED, 137 DEFINITION, 75 OPEN, 60 HYPOTHESIS,
58 NOT-CLAIMED, 13 NUMERICAL, 3 CONJECTURE.

This lens hand-verified four `11_obstructions` results and all four recompute correctly: the
reciprocal-pair kernel `ker J = {(Θ_e v, v) : v ∈ ker(H−I)}`; the K=1 witness
`det(J + p₀I) = p₀² + p₀(a + a⁻¹)²` with its unique minimizer and curvature `A''(1) = −4/(p₀+4)`,
correctly identified as a *maximum* of the isolated log-normalizer contribution and explicitly
declined as a force along a gauge orbit; the Schur factorization
`det J = (det(I−H))²/(det R_e · det R_f)`; and the star contraction rate
`ρ = λ_max(P_b^{−1/2} B P_b^{−1/2}) < 1` with the correct `KL = ½‖e_t‖²_{P_b}` consequence.

### P1 (high) The one positive interpretive conclusion is mis-tagged and mis-cited

`12_philosophy.tex:183–187`, tagged `\status{DEFINITION}`: "This supports an epistemic /
structural-realist reading in Worrall's sense \citep{Worrall1989}."

Three convergent problems. (i) DEFINITION promises "nothing is being proved and the text says so"
(`01_introduction.tex:168`); "supports" is an evidential relation. (ii) The manuscript applies the
correct fence to both neighbours — ontic SR is "available but unsupported" OPEN (`:189–192`),
moderate SR "proposes, but does not establish" OPEN (`:204–206`). Only the reading the invariants
list was built for escapes an OPEN. (iii) Worrall 1989 (*Dialectica* 43(1–2):99–124) argues from a
**diachronic** premise — Fresnel's equations retained under Maxwell's incompatible ontology — that
structure survives theory succession. `eq:phil-invariants` is a **synchronic** list of quantities
invariant under passive reframing inside one fixed formalism. That is gauge redundancy, which
licenses *less* commitment to the redundant coordinates, not more.

The on-point literature is Lyre, "Holism and structuralism in U(1) gauge theory" (*SHPMP* 35, 2004)
and Healey, *Gauging What's Real* (OUP 2007) — and Lyre's argument runs through Aharonov–Bohm, an
observable sensitive to holonomy, which `12_philosophy.tex:154–155` concedes is absent: "It also
does not construct a population observable sensitive to base holonomy. \status{NOT-CLAIMED}".
Compounding this, `I_struct` includes `[H_γ^b]_conj` and `[H_γ^m]_conj`, which the chapter's own
idle-wheel criterion (`:77–78`) plus the NOT-CLAIMED at `:112` disqualify from carrying realist
weight.

### P2 (high) The contract's universality claim is false, and fails exactly at the framing layer

`01_introduction.tex:156–157`: "Every nontrivial statement carries one of the following tags."

The untagged statements are the scope-setters, not filler:
- `11_obstructions.tex:4` — "the concrete obstructions in this chapter concern particular Gaussian
  realizations and must not be promoted to no-go theorems for arbitrary belief or model fibers"
  (an untagged scope ruling governing every no-go in the chapter);
- `:332` — "Reading the corollary as a statement about cyclicity is a misreading, and the correct
  reading inverts the relation between the two halves of this document" (untagged, thesis-level);
- `:222`, `:237`; `12_philosophy.tex:340–343` (the chapter's closing verdict);
  `appendix_numerical_provenance.tex:130–137` ("What a passing run means").

Propositions get tags; interpretations do not. Since the tags derive their meaning from the
untagged framing, the apparatus is off at the layer where reader entitlement is set.

### P3 (high) The two physics-facing OPEN items break the OPEN tag's own promise

`01_introduction.tex:172` promises OPEN means "What would settle it, and what obstructs it, are
named." Audited all 32 ledger items. Most honor it in both directions — "or give a counterexample
in the declared family" (`:44`), "or prove endpoint degeneracy for a stated class" (`:217`), "or
find its boundary" (`:235`), "Either a proper witness or a proof under properness" (`:190`), "or
prove insensitivity for that same declared controlled class" (`:249`).

The two exceptions are "Physical-time identification" (`:289–295`) and
`claim:physical-law-identification` (`:298–304`). Both give only a requirements list and name no
obstruction and no negative closure. A checklist for supplying an entire empirical science is not
a settlement condition in Mayo's sense (*Error and the Growth of Experimental Knowledge*, 1996) —
no test could be severe against it because no test is specified. Because
`claim:physical-law-identification` carries the same numbered `\openproblemheading` apparatus as
genuinely tractable items and is cross-referenced from `01_introduction.tex:150`,
`12_philosophy.tex:293–297`, and `07b_agent_network_rg.tex:2700`, it acquires the standing of a
live research item one theorem from discharge. It is not one.

*Fix:* move both into a separately headed "Statements this work makes no attempt to settle", or
supply the missing halves — for physical time, the obstruction is that Fisher duration is
reparameterization-invariant and metric-relative, so any calibration is underdetermined up to
choice of metric.

### P4 (high) The interpretation chapter cites the one obstruction that helps it and none of three that constrain it

`12_philosophy.tex` contains exactly five cross-references, and the only obstruction-chapter result
among them is `thm:obs-agent-interaction-equivalence` — the one that *supports* the participatory
reading. Absent: `cor:obs-flat-fold-singular`, `prop:obs-declared-root-unavoidable`,
`prop:obs-normalizer-link-dependence`, `eq:obs-tension`.

The omission is load-bearing. `11_obstructions.tex:239–245` proves that in any finite DAG
generative model at least one latent has no parents, so no finite acyclic construction can have
every prior constituted by other latents — and comments that "The ambition behind the fold was to
eliminate the declared root … within finite acyclic models the ambition is unachievable for
structural reasons rather than for want of ingenuity." That is a refutation of the strong form of
the participatory closure ambition. The NOT-CLAIMED list at `:264–266` omits it, so a reader of
chapter 12 alone takes the self-constituting-prior reading as unsupported rather than as proved
impossible.

### P5 (medium) ESTABLISHED conflates "proved here" with "cited standard result"

`01_introduction.tex:167` merges two distinct reader entitlements. With 501 ESTABLISHED tags and
no distinguishing mark — and no related-work or novelty statement anywhere in the introduction —
no reader can determine what the manuscript contributes. Concrete symptom: `12_philosophy.tex:4`
declares "This chapter proves no mathematical result," yet the chapter carries seven ESTABLISHED
tags, four of which supply no locator (`:44`, `:109`, `:115`, `:237`). Three are in fact backed
(`02_geometry.tex:594–595`, `:613–616`, `prop:obs-reciprocal-pair-kernel`) but the reader gets no
pointer. `:109` is load-bearing: the gauge-invariance of `[H_γ]_conj` is what puts it into
`eq:phil-invariants` and thus into the structural-realism argument.

### P6 (medium) NOT-CLAIMED applied to a statement the same paragraph argues is false

`11_obstructions.tex:177–183`. The contract states NOT-CLAIMED "is never used for a refuted
statement" (`01_introduction.tex:180–182`). The paragraph declines the improper-endpoint reading of
Berman, Klinger & Stapleton (*MLST* 4:045011, 2023; verified at `references.bib:4411`) *and*
supplies a positive argument that it is wrong (with a proper prior the `T ↓ 0` endpoint is that
prior, hence proper). That is a refutation, not a declination. The neighbouring `:185` NOT-CLAIMED
is by contrast a correct declination, which makes the mis-tag conspicuous.

### P7 (medium) CONJECTURE is a near-dead tag

Three occurrences across 847 tags: the taxonomy row itself, `conj:grg-fixed-b-attraction`
(`10_renormalization.tex:261`), and the ledger restatement of that same conjecture. One
substantive conjecture in the whole manuscript. Everything risky routes to OPEN (75) or
NOT-CLAIMED (58), neither of which asserts anything that could turn out false. The seven-tag table
advertises a graded scale of commitment; the operative distinction is binary — proved, or not
addressed. In Lakatos's terms the programme has no excess empirical content. Not a defect in the
mathematics, but the taxonomy invites the reader to credit falsifiable positions the author has
deliberately not staked.

*Fix:* state plainly that the document asserts one conjecture and all other unproved statements
carry no commitment; or promote the statements actually believed (Kron congruence-diagonal
maximality boundary; fixed-ray attraction beyond the scalarized cone).

### P8 (low) "Timeless Inference Histories" is fenced against the wrong chapter

`main.tex:110` (subtitle) and `main.tex:21` (pdfkeywords). The fence at `12_philosophy.tex:51–55`
says the word "has an equally narrow meaning in \Cref{ch:relational-inference}" — but *timeless*
does not occur anywhere in `05d_relational_inference.tex`. Its four occurrences are `main.tex:21`,
`main.tex:110`, `02_geometry.tex:28`, `09_coarsegraining.tex:624`. The disclaimer points at a
chapter where the term is absent, while the subtitle and the PDF metadata that indexers harvest
carry a Barbour/Rovelli term of art unqualified.

### Lens assessment

Discipline is real, not a veneer. Strongest evidence: `11_obstructions` states the boundary of each
no-go rather than the headline (`:88–90`) and closes by restricting itself to graph-link holonomy
with no inference to bundle topology (`:422`); and `appendix_numerical_provenance.tex:130–137`
states plainly that a passing run "does not prove a theorem, genericity, an asymptotic limit,
universality, or a physical interpretation," with the body honoring it (`11_obstructions.tex:235`,
"The propositions, not the computation, establish the claim"). Every philosophy-chapter citation
checked against primary sources was accurate (van Fraassen 1980 pp. 11–12, Esfeld & Lam 2008,
Ladyman & Ross 2007, Hoffman/Singh/Prakash 2015, Wheeler 1990, Gelman & Meng 1998 — the
path-sampling identity is correct as written, Berman/Klinger/Stapleton 2023). No
manuscript-as-authority circularity of the usual kind.

Where the contract fails, it fails along one axis: **the apparatus is switched off at the
interpretive layer.** Fixing P1–P8 would leave the epistemic contract genuinely exemplary.

---

## Cross-lens convergence

The verification-harness lens and the philosophy lens independently reached the 29-vs-30-check gap
and the unbacked appendix numbers, from different directions (executed hashing vs. reading the
NUMERICAL tag's promise). That convergence is worth more than either report alone and partly
substitutes for the skeptic pass that was not run.

## Reviewer-side correction already applied

The philosophy lens reported that the declared run command path
`manuscripts/gauge_vfe_rg/verification/run_checks.py` names a directory that does not exist.
**Discounted.** It exists in the Research vault, which is the manuscript's home; it is wrong only
relative to this snapshot repo. Downgraded to a scoping note.

## SUPERSEDED IN PART — read the adjudication log first

A second session (2026-08-09, later) ran the Wave-3 adversarial pass that was never dispatched.
Every finding it tested was downgraded. **V1, V2, V4, V8, P1, and P4 below are wrong as written**;
`2026-08-09-ultradeep-peer-review-ADJUDICATIONS.md` in this directory carries the corrected
statements and the executed evidence. Do not cite the severities in this file. In particular:
V1 critical to medium, V2 critical to medium, V4 high to low, P1 high to low, P4 high to low
(refuted), V8 mostly retracted. V1/V2-stale/V3/V8 are one defect and should merge. Three of four
philosophy findings failed by reading a symbol as provenance when it encoded subject matter.

## What remains

- Ten Wave-1/Wave-2 agents had not reported: gauge theory, differential geometry, information
  geometry, variational/measure theory, RG/stat-mech, exact network RG (`07b`), numerical/matrix
  analysis of the Gaussian realization, citations/prior-art, notation/labels/counters, and
  cross-chapter dependency.
- Wave 3 (adversarial skeptic on every high/critical finding) was never dispatched. **No finding
  above has survived an adversarial pass.** Treat V1–V10 and P1–P8 as strong but unrefuted rather
  than as confirmed.
- `verified-ledger.md` has not been updated. Nothing here has been written to the vault.
