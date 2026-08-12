# Audit 05 — Claim Traceability, Status-Tag Integrity, and Process Proportionality

Auditor scope: claims-to-evidence mapping, `\status{}` discipline, the open ledger, oracle
independence, results-doc overclaim, process theater, unfalsifiability, prior-review fix rate.
Math depth is out of scope (other auditors).

Repos audited at:
- `C:\Users\chris and christine\Desktop\MultiAgentELBO` @ `c101b8a`
- `C:\Users\chris and christine\Desktop\Research` @ `1793a4d`

---

## 0. Verdict in one paragraph

The epistemic-status discipline inside the LaTeX theorem grammar is the best I have seen in an
AI-assisted research program, and it is not a veneer: 292 of 292 formal environments carry exactly
one status tag, zero adjacent-tag violations, zero multi-status paragraphs, and every ESTABLISHED
result without a `Proof` block carries its argument inline. **The failure is not in the tagging. It
is that the entire evidence layer beneath the tags is detached from the claims it is supposed to
support.** The only numerical-evidence artifact in the manuscript binds to zero of twenty-three
current source files. The 28,213-line verification apparatus is governed against repository paths
that do not exist here and is invoked by nothing. Every JUnit, coverage, and replay artifact cited
by the results documents lives in a gitignored tree and is absent — including the ledger that the
2026-08-11 audit names as its own closure authority. Twenty-two audit findings were recorded,
adjudicated, and planned across 23,367 lines of documentation, and **zero were fixed**: since the
audit baseline, not one line of source has changed. And the flagship confirmatory experiment —
attacking the manuscript's single CONJECTURE — used a preregistered success threshold that was
subsequently proven mathematically unreachable, so it could never have confirmed anything. The
bookkeeping is immaculate. It is bookkeeping about bookkeeping.

---

## 1. Findings table

| ID | Sev | Type | One-line |
|---|---|---|---|
| T-01 | CRITICAL | UNSUPPORTED CLAIM | Sole numerical artifact binds 0/23 current `.tex` and 0/4 protocol files; all 13 NUMERICAL claims currently unbacked |
| T-02 | CRITICAL | UNFIXED PRIOR FINDING | 22/22 audit findings unfixed; 23,367 lines of remediation docs, 0 lines of remediation code |
| T-03 | CRITICAL | PROCESS THEATER | 28,213-line verification apparatus governs non-existent paths, is never invoked, and requires one hard-coded interpreter path |
| T-04 | CRITICAL | UNFALSIFIABILITY | Preregistered confirmatory threshold proven unreachable by construction; experiment could not have succeeded |
| T-05 | HIGH | UNFIXED PRIOR FINDING | Ultradeep peer review: 18 findings, 5 adjudicated, 0 fixed; `Theory/` is architecturally unfixable |
| T-06 | HIGH | CIRCULAR EVIDENCE | 31 cited evidence paths absent from repo, incl. `.verification/ledger.json`, the audit's own closure authority |
| T-07 | HIGH | STATUS VIOLATION | 174/501 ESTABLISHED tags sit on prose with no proof, no citation, no internal pointer |
| T-08 | HIGH | UNSUPPORTED CLAIM | Open ledger omits an entire chapter's obligations and is structurally frozen against new evidence |
| T-09 | MEDIUM | STATUS VIOLATION | "Every nontrivial statement carries one of the following tags" is false: 19 untagged normative scope rulings |
| T-10 | MEDIUM | STATUS VIOLATION | Two physics-facing OPEN items name no obstruction, breaking the OPEN tag's own promise |
| T-11 | MEDIUM | CIRCULAR EVIDENCE | Theory oracles are implementation-independent but assumption-identical; agreement is silent about the theory |
| T-12 | MEDIUM | PROCESS THEATER | Results docs devote an order of magnitude more text to hashes than to science |
| T-13 | LOW | OVERCLAIM | 17-significant-figure reporting of bootstrap medians |

---

## 2. CRITICAL findings

### T-01 — The numerical evidence artifact binds to nothing in the current manuscript
**Type: UNSUPPORTED CLAIM. Severity: CRITICAL.**

`Theory/verification/current-results.json` is the only executed-evidence record in the manuscript.
Its `inventory_manifest` binds every source file by SHA-256. I recomputed all of them:

```
OK=1 MISMATCH=23 MISSING=0     (the 1 "OK" is a directory-level artifact, not a .tex file)
01_introduction.tex   recorded=2237a4294736138d  current=256e836c3439745e
02_geometry.tex       recorded=43a9bab3155d967f  current=8a39f1c6d2e0ac92
...  (all 23 chapters + appendices mismatch)
protocol files: claims.json MISMATCH, run_checks.py MISMATCH,
                requirements.txt MISMATCH, VERIFICATION.md MISMATCH
```

By the repo's own stated policy (`Theory/appendix_numerical_provenance.tex`, "Freshness and scope"):
"Any source, protocol, input, dependency, or environment change requires a new run before the
numerical evidence is current." Every input has changed. **Therefore every `\status{NUMERICAL}`
claim in the chapters is, right now, backed by no valid artifact.**

Corroborating drift:
- Artifact records `total_NUMERICAL_occurrences: 11`; the current chapters contain **13**.
- Artifact contains **29** checks; `appendix_numerical_provenance.tex` describes a **30**-check package.
- Artifact's `overall_status: "PASS"` and `mapping_validation.status: "PASS"` sit at top level with
  no staleness field. A machine consumer reading this file learns "PASS".
- 26 of 35 `claim_id`s referenced by the artifact's checks (e.g. `NUM-CG-AGGREGATION`,
  `NUM-RG-RAY-KERNEL`, `NUM-CG-HOLONOMY`) **do not exist** in the current `claims.json`, which has
  only 13 claims. That is *evidence with no claim*, at a 74% rate.
- `CHK-CG-FACTOR-GAP-STRESS-3138` is referenced by two load-bearing claims
  (`appendix_numerical_provenance.tex:71`, `:128`) and is **absent from the artifact entirely**.

**Credit where due:** the appendix states the problem in print ("The checked-in
`verification/current-results.json` is the older 29-check artifact. It is not evidence for this
30-check package."). That is honest and it is why this is not fraud. But the *chapters* do not
inherit the disclaimer. `06_gaussian.tex:294` says the check's "**current output** corroborates the
characterization"; `06_gaussian.tex:351`, `08_infogeometry.tex:195/334/488`, `11_obstructions.tex:235/420`
and `07_restrictions.tex:298` all speak of runs in the present tense. A reader of chapter 6 who
never reaches appendix page 4 is misinformed.

**Falsifier:** re-run `run_checks.py` at the current revision and the finding evaporates. Per the
adjudication log, this is "twelve seconds of CPU". It has not been done in three days of work.

---

### T-02 — Twenty-two audit findings: recorded, adjudicated, planned, and not one fixed
**Type: UNFIXED PRIOR FINDING. Severity: CRITICAL. This is the top-severity finding.**

`docs/audits/2026-08-11-post-fixed-ray-deep-audit.md` retained 22 defects (3 high, 15 medium, 4 low)
against baseline `aedc662`. The complete diff from that baseline to `HEAD`:

```
git diff --stat aedc662 HEAD
 .gitattributes                                         |    3 +
 docs/audits/2026-08-11-post-fixed-ray-deep-audit.md    |  202 +
 ...remediation-wave-0.md                               | 1974 +
 ...remediation-wave-a.md                               | 3078 +
 ...remediation-wave-b.md                               | 6169 +
 ...remediation-wave-c.md                               | 3929 +
 ...remediation-wave-d.md                               | 2796 +
 ...remediation-wave-e.md                               | 4196 +
 ...remediation-program-design.md                       | 1020 +
 9 files changed, 23367 insertions(+)
```

**Zero source files. Zero test files. 23,367 lines of plans — 1,053 lines of planning per finding.**
Wave E is 4,196 lines devoted to correcting *one sentence* in one manuscript paragraph.

I sampled 8 findings and verified their status in current source. **8/8 still present:**

| Finding | Verification method | Status |
|---|---|---|
| AUD-03 (probability/ELBO invariants destroyed by loose tolerances) | executed probe | **PRESENT** — constructed a `ProbabilityMeasure` of total mass 0.8 and total mass 0.0; `kl_divergence` returned `-0.17851484105136778`, **the exact value the audit reported** |
| AUD-13 (read-only arrays re-writable) | executed probe | **PRESENT** — `m.masses.setflags(write=True); m.masses[0] = -5.0` → `[-5. 0.5]` |
| AUD-12 (mutable RNG spawn keys) | executed probe | **PRESENT** — mutating `spawn_keys` changed `provenance()` from `[0]` to `[999]` without regenerating |
| AUD-18 (negative KL) | inspection | **PRESENT** — `finite/vfe.py:35-42` byte-identical to audited lines; no stable summation |
| AUD-15 (rcond mismatch) | inspection | **PRESENT** — `information_history.py:80-81` uses `rcond*max(1,λmax)`; `:138` `np.linalg.pinv(rcond=rcond)` uses `rcond*λmax` |
| AUD-17 ("Fisher cocycle" is only a bilinear identity) | inspection | **PRESENT** — `scale_cocycle.py:438` still named `base_fisher_cocycle_residual_forms`; `_matrix()` at `:34-40` validates only rectangularity — no symmetry, no PSD, no provenance |
| AUD-09 (inert scale-cocycle toggles) | grep | **PRESENT** — `retained_interaction_order` returns 0 hits in `scale_cocycle_experiment.py`; the option is still accepted and still inert |
| AUD-20 (connectedness → common fixed point) | inspection | **PRESENT** — `Research/manuscripts/magent_elbo_whitepaper/08a_coarse_graining.tex` still reads "Agents that are coupled at all therefore share a flow and **reach the same fixed point**" |

**True fix rate: 0/22 (0%).** The audit's own line 23 is the tell: "`EVIDENCE_VERIFIED` verifies that
each stated defect exists; it does not promote any scientific theorem." The verification apparatus
was used to certify that the bugs are real, then stopped.

This matters scientifically, not just hygienically. AUD-03 means the core probability/KL/ELBO types
can be silently invalidated by a parser-valid config; AUD-17 means a metric labeled "Fisher" in a
published results table has no established connection to Fisher information.

---

### T-03 — The verification apparatus governs a repository that is not this one
**Type: PROCESS THEATER. Severity: CRITICAL.**

`Theory/verification/` contains 28,213 lines of Python (`run_checks.py` 10,443; `build_audit.py`
5,473; `lifecycle_gate.py` 1,941; plus tests), roughly 720 KB. It is inert here:

1. **It governs paths that do not exist.** `manifest-policy.json` `required_paths` lists
   `manuscripts/gauge_vfe_rg/SPEC.md`, `manuscripts/references.bib`,
   `manuscripts/gauge_vfe_rg/verification/*`. `lifecycle_gate.py:31-40` requires
   `docs/derivations/2026-08-03-gauge-vfe-rg-remediation` and
   `docs/superpowers/plans/2026-08-03-gauge-vfe-rg-review-remediation.md`. **All absent from
   MultiAgentELBO.** Its `_DERIVATION_ROOT`, `_PRODUCTION_MARKERS`, `_CURRENT_RESULT`, and
   `_TRACKED_PDF` constants all point outside this tree.
2. **Nothing invokes it.** Grepping the whole repo for `run_checks|build_audit|lifecycle_gate`
   outside `Theory/verification/` returns hits only inside a stale `.superpowers/worktrees/`
   snapshot of the repo itself. No launcher, no test, no CI, no `pyproject.toml` entry point.
3. **It is not runnable by anyone else.** `run_checks.py:324` hard-codes
   `_FIXED_PYTHON_EXECUTABLE = Path(r"C:\Python314\python.exe")`; `:44` hard-codes
   `C:\Users\chris and christine\AppData\Roaming\Python\Python314\site-packages`; `:7946` requires
   the literal startup line `C:\Python314\python.exe -I -S`. Executing `--help` on any other
   interpreter yields: *"production verifier startup requires C:\Python314\python.exe -I -S before
   third-party imports."* An independent reviewer cannot reproduce a single check.

Proportionality, in lines:

| Artifact | Lines |
|---|---|
| Verification apparatus (inert) | 28,213 |
| Remediation plans + specs (0 findings fixed) | 29,043 |
| `Theory/build.ps1` (single build script) | 3,566 |
| **The actual theory (`Theory/*.tex`)** | **16,821** |
| Simulation source `src/` | 24,684 |
| Tests | 20,705 |
| All results + reviews + audits | 3,054 |

**There is 3.4x more governance code and planning prose than there is theory.** The build script for
one document is 3,566 lines — 21% of the manuscript it builds.

None of this machinery constrains a scientific claim. Name the specific items that constrain nothing:
`lifecycle_gate.py` (validates S/E/C/W commit ordering in a repo whose layout it does not match),
`build_audit.py` (audits LaTeX build products against absent paths), `manifest-policy.json`
(governs `manuscripts/gauge_vfe_rg/**`), and the four-file protocol hash binding in
`current-results.json` (all four hashes already stale). Deleting all of it would not weaken a single
scientific claim in this repository by one bit.

---

### T-04 — The flagship confirmatory experiment could not have confirmed
**Type: UNFALSIFIABILITY (inverted). Severity: CRITICAL.**

`conj:grg-fixed-b-attraction` (`10_renormalization.tex:250`) is the **only substantive CONJECTURE in
the entire 847-tag manuscript**. The Gaussian fixed-ray program exists to attack it.

The preregistration `docs/experiments/2026-08-09-gaussian-fixed-ray-preregistration.md:82` froze:
> "The practical attraction threshold is a slope of at most `-0.02` radians per scale."

and `:84` requires "the upper endpoint of the two-sided 95% paired bootstrap confidence interval for
the median angle slope is at most `-0.02`" for a support classification.

The later exact-rational certificate (`docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic/fixed_model_support_certificate.json`) proves:

```
"rational_slope_lower_bound":        -9/625   = -0.01438895606312301
"rational_margin_above_threshold":    7/1250  =  0.0056
"paired_support_boundary_reachable": false
"certificate_status":                "certified_unreachable"
```

Under the frozen basin `[1/4,4]^6`, the two frozen maps, scales 4–8, raw-angle OLS, and the paired
least-favorable maximum, **no admissible job can produce a slope at or below -0.02.** The
preregistered support criterion was mathematically impossible from the moment it was frozen.

Consequences:
- 40 confirmatory jobs, 640 serial CUDA exchanges, 3,644 seconds of GPU time (AUD-21), a five-job
  parity sentinel, 240 controller/worker comparisons, an operator gate, and an environment-lock
  digest were all expended on an experiment with one reachable outcome.
- The reported "inconclusive" classification is not a scientific result. It was determined by the
  design, not by the data.
- **No gate caught this.** The apparatus verified hashes, parity, determinism, seeds, job IDs, and
  basin-exit rates flawlessly around a question that could not be answered. Ten lines of exact
  rational arithmetic *before* execution would have caught it — which is precisely what the
  certificate later did.

The project reports this honestly ("the `-0.02` practical-support boundary is structurally
unreachable... It does not refute attraction and does not prove a mechanism") and that honesty is
real. But the honesty is applied *post hoc* to a design failure that the entire preregistration and
gating apparatus was nominally built to prevent. **This single episode is the strongest available
evidence that the process apparatus increases confidence in bookkeeping, not in science.**

Related unfalsifiability, correctly labeled: `docs/hypotheses.md` RG-01 states its own support and
refutation thresholds as "To be preregistered before execution" — i.e. the one genuinely scientific
hypothesis in the registry has no thresholds at all. That is honest but it means RG-01 is currently
untestable as written.

---

## 3. HIGH findings

### T-05 — Prior peer review: 18 findings, 5 adjudicated, 0 fixed, and `Theory/` cannot be fixed
**Type: UNFIXED PRIOR FINDING. Severity: HIGH.**

`docs/reviews/2026-08-09-ultradeep-peer-review-INTERIM.md` raised V1–V10 and P1–P8 (18 findings).
`...-ADJUDICATIONS.md` contains verdicts for **3** (V1, V2, V4) with 5 verdict lines. The interim
document itself states: *"Wave 3 ... was never dispatched. **No finding above has survived an
adversarial pass.**"* and *"Ten Wave-1/Wave-2 agents had not reported"* — gauge theory, differential
geometry, information geometry, measure theory, RG/stat-mech, `07b`, numerical analysis, citations,
notation, cross-chapter dependency. **Ten of eleven planned review lenses never reported at all.**

I verified all 8 philosophy findings against current source. **8/8 still present verbatim:**

| | Claim | Current source | Status |
|---|---|---|---|
| P1 | evidential "supports" tagged DEFINITION | `12_philosophy.tex:183-187` — "This supports an epistemic structural-realist reading in Worrall's sense" ... `\status{DEFINITION}` | UNFIXED |
| P2 | "Every nontrivial statement carries a tag" is false | `01_introduction.tex:156` intact; untagged scope rulings at `11_obstructions.tex:4`, `:332`, `12_philosophy.tex:340-343` intact | UNFIXED |
| P3 | two OPENs name no obstruction | `appendix_claim_ledger.tex:289-295` (Physical-time), `:298-304` (Physical-law) — both still pure requirements lists | UNFIXED |
| P4 | philosophy chapter cites only the helpful obstruction | 5 cross-refs, `cor:obs-flat-fold-singular` still absent | UNFIXED |
| P5 | ESTABLISHED conflates proved-here with cited | `12_philosophy.tex:4` "This chapter proves no mathematical result" + 7 ESTABLISHED tags, incl. bare `\status{ESTABLISHED}` at `:115` and `:237` | UNFIXED |
| P6 | NOT-CLAIMED on a refuted statement | `11_obstructions.tex:177-183` — argues the improper-endpoint reading is wrong, then tags `\status{NOT-CLAIMED}` | UNFIXED |
| P7 | CONJECTURE is a near-dead tag | independently recounted: **exactly 3** CONJECTURE tags (taxonomy row + `conj:grg-fixed-b-attraction` + its ledger restatement) among 847 | UNFIXED |
| P8 | subtitle fenced against wrong chapter | `main.tex:110` subtitle and `main.tex:21` pdfkeywords carry "Timeless Inference Histories"; `12_philosophy.tex:51` fences it to `ch:relational-inference`; "timeless" occurs **zero times** in `05d_relational_inference.tex` | UNFIXED |

**Fix rate: 0/18.** And this is structural, not neglectful: `docs/theory-provenance.md` declares
`Theory/` "a supplied, read-only snapshot... **No build task may modify its tracked contents**." My
independent tag census reproduces the reviewer's exactly (847 = 501/137/75/60/58/13/3), confirming
the manuscript is byte-unchanged since the review. **The repository is architecturally incapable of
acting on any review finding about the theory.** Reviews of `Theory/` in this repo are write-only.

P7 deserves emphasis on its own terms. Three CONJECTURE tags against 75 OPEN and 58 NOT-CLAIMED
means the operative epistemic scale is binary — proved, or not addressed. A seven-value taxonomy
advertising graded commitment, operating as a two-value one, invites the reader to credit
falsifiable positions the author has deliberately not staked.

### T-06 — The cited evidence does not exist in the repository
**Type: CIRCULAR EVIDENCE. Severity: HIGH.**

I resolved every repository path cited by `docs/results/*.md`, `docs/audits/*.md`,
`docs/reviews/*.md`. **31 cited evidence paths are absent.** All lie under the gitignored
`.verification/` tree (`.gitignore:25`). Including:

- `.verification/ledger.json` and `.verification/active.json` — named by the audit (line 23) as the
  authority recording all 22 findings as `EVIDENCE_VERIFIED`. **Absent.**
- `.verification/deep-audit-runtime/full2-aedc662.xml` — the audit's 957-test JUnit record, cited by
  SHA-256 `206674472AA...`. **Absent.**
- `.verification/deep-audit-runtime/audit-core-probes.json` — the audit's own mechanical probe.
  **Absent.**
- `.verification/gauge-holonomy/pytest-prelim2-focused.xml`, `coverage-prelim2.xml` — the 38-test
  and coverage numbers in the holonomy results doc. **Absent.**
- Every session-1/2/3/4 replay artifact and coverage file. **Absent.**

The `.verification/` directory in the working tree contains exactly **one** file:
`wave0/postmerge-pytest.xml`. `artifacts/` is likewise gitignored.

Tracked evidence is 31 files, essentially the two fixed-ray evidence bundles and eight review
markdown documents. Everything else is a SHA-256 of a file no reader can obtain. **A hash of an
unavailable file is not provenance; it is an assertion with a hexadecimal costume.** It cannot be
checked, so it cannot fail, so it carries no information.

### T-07 — 174 ESTABLISHED tags with no proof, no citation, no pointer
**Type: STATUS VIOLATION. Severity: HIGH.**

SPEC §2.1: ESTABLISHED means "Proved here, or a standard result cited to a source that has been
checked. **Give the proof or the citation.**"

Census of the 501 ESTABLISHED tags:
- 176 attach to a formal heading block. These are in excellent shape (§5).
- **325 attach to plain prose paragraphs.** Of those, **174 contain no `Proof`, no `\cite*`, and no
  `\Cref{thm:|prop:|cor:|lem:|eq:}` or `\eqref` pointer.**

Per file: `09_coarsegraining` 26, `07b_agent_network_rg` 22, `07_general_renormalization` 16,
`05c_pullback_geometry` 15, `05b_local_collective_elbo` 11, `05d_relational_inference` 10,
`08_infogeometry` 10, `01_introduction` 9, `02_geometry` 9, `06_general_coarsegraining` 9,
`03_probability` 8, `05_elbo` 6, `10_renormalization` 5, `11_obstructions` 5, `12_philosophy` 4,
remainder 6.

I read a sample. In body chapters most are genuine one-step arguments where the paragraph *is* the
proof (e.g. `02_geometry.tex:353`) — defensible. The indefensible cluster is the summary and
interpretive chapters: `01_introduction.tex` (9 tags) forward-declares results as ESTABLISHED with
no locator, and `12_philosophy.tex` (4) does the same in a chapter whose own first line reads "This
chapter proves no mathematical result." That is P5, uncorrected and now quantified.

**Recommendation the reviewer already made and which remains unimplemented:** split ESTABLISHED into
`PROVED-HERE` and `CITED-STANDARD`. With 501 undifferentiated tags and no related-work section, a
reader cannot determine what the manuscript contributes.

### T-08 — The open ledger is incomplete and structurally frozen
**Type: UNSUPPORTED CLAIM. Severity: HIGH.**

`appendix_claim_ledger.tex` holds 31 `\item[...]` obligations plus one `\openproblemheading` (32
total, matching the reviewer's count). It is substantive and well written. Two defects:

**(a) Omitted obligations.** The chapters carry 44 OPEN tags. Grepping the ledger for
`realis|structural` returns **zero hits**. The two structural-realism obligations —
`12_philosophy.tex:196` (ontic SR "available but unsupported", `\status{OPEN}`) and `:210` (moderate
SR fit "proposes, but does not establish", `\status{OPEN}`) — are **absent from the central
open-obligation ledger**, even though the ledger does carry the neighboring physical-time and
physical-law items. The interpretive chapter's obligations are selectively ledgered.

Also absent: the equivariance-of-Bayes-recovery obligation at `06_general_coarsegraining.tex:499`
("an equivariant conditional version is an additional hypothesis or theorem, especially for
noncompact groups") is only approximately covered by the "Partition selection and experiment-level
recovery" item, which speaks to recovery kernels and partition selectors, not equivariance.

**(b) The ledger cannot absorb evidence.** The ledger's `Scalarized attraction (conjecture)` entry
(`:197-203`) is unchanged since 2026-08-08. On 2026-08-10/11 the lab produced an exact rational
certificate directly bearing on it (T-04). Nothing propagated. It *cannot* propagate:
`Theory/` is a read-only snapshot by declared policy. **The claim-to-evidence loop is open by
construction — the lab can produce evidence, and no mechanism exists to route it back into the
ledger it bears on.** This is the deepest traceability defect in the project, because it means the
elaborate apparatus can never actually close a claim.

---

## 4. MEDIUM / LOW findings

### T-09 — "Every nontrivial statement carries one of the following tags" is false
**STATUS VIOLATION. MEDIUM.** `01_introduction.tex:156`. Counting substantial prose paragraphs
(≥250 chars, ≥40 lowercase words, excluding proofs and macro blocks): **291 of 876 (33.2%) carry no
status tag.** Most are legitimately connective. But **19 untagged paragraphs carry normative or
scope rulings**, i.e. exactly the layer at which reader entitlement is set. Worst examples:

- `11_obstructions.tex:4` — "the concrete obstructions in this chapter concern particular Gaussian
  realizations and **must not be promoted to no-go theorems** for arbitrary belief or model fibers."
  An untagged scope ruling governing every no-go in the chapter.
- `11_obstructions.tex:332` — "Reading the corollary as a statement about cyclicity is a misreading,
  and **the correct reading inverts the relation between the two halves of this document**."
  Untagged, thesis-level.
- `02_geometry.tex:168` — "These two passive coordinate choices **must not be confused** with a
  product gauge symmetry." Untagged, and this is the notational discipline the whole SPEC §3 rests on.
- `10_renormalization.tex:263` — "This statement freezes every matrix direction. **It is not a
  theorem** about the full coupling cone..." Untagged, and it is the scope fence on the manuscript's
  only conjecture.
- `05_elbo.tex:149`, `03_probability.tex:344`, `08_infogeometry.tex:76`, `06_gaussian.tex:6`, and 11 more.

**Either tag them or soften the contract sentence.** The current text promises universality the
document does not deliver.

### T-10 — Two OPEN items break the OPEN tag's promise
**STATUS VIOLATION. MEDIUM.** SPEC §2.1: OPEN requires "State exactly what would settle it, and what
the obstruction is." `appendix_claim_ledger.tex:289-295` (Physical-time identification) and
`:298-304` (`claim:physical-law-identification`) each supply only a requirements list — "a named
target system, an observable and estimator, a frozen validation and uncertainty protocol, a baseline
margin, probability-level closure, and held-out evidence" — and **name no obstruction**. A checklist
for supplying an entire empirical science is not a settlement condition. Because
`claim:physical-law-identification` carries the same numbered `\openproblemheading` apparatus as
genuinely tractable items and is cross-referenced from `01_introduction.tex:150`,
`12_philosophy.tex:293-297`, and `07b_agent_network_rg.tex:2700`, it acquires the standing of a live
research item one theorem from discharge. It is not one. **This is the point at which PIFB2's
admittedly-unfalsifiable participatory reading has been inherited into the rigorous chapters wearing
a tag that promises tractability.** The other 30 ledger items honor the promise; these two do not.

### T-11 — The theory oracles are implementation-independent but not theory-independent
**CIRCULAR EVIDENCE. MEDIUM.** I read `src/multiagent_elbo/finite/theory_oracles.py` (1,493 lines)
and compared it against `finite/vfe.py`, `finite/measures.py`.

**Genuinely independent along three axes:** (i) numeric representation — exact `fractions.Fraction`
and a `FormalLogSum` over prime `log(p)` atoms vs. float64/NumPy; (ii) code path — it imports
**nothing** from `multiagent_elbo` and nothing from NumPy, only stdlib; (iii) intermediate
quantities — `exact_fisher_defect` builds the joint, coarse masses, coarse scores, and conditional
covariance explicitly, where `vfe.py::_reverse_conditional` uses a vectorized divide. Agreement
therefore genuinely detects float bugs, sign conventions, orientation errors, and support-branch
mistakes. This is real differential testing and it is well built.

**But it is not verification of the theory.** Both encode the *same identities from the same source*.
`exact_evidence_elbo` and `free_energy` compute the same functional; `exact_fisher_defect` and
`vfe_channel_decomposition` encode the same chain rule. **No possible run can produce disagreement
that indicts the theory** — only disagreement that indicts one of two encodings of it. The tests in
`test_theory_oracles.py` (1,125 lines) are consistency checks between two spellings of one claim.

**Credit:** `docs/results/2026-08-09-theory-oracle-results.md:14-19` says this correctly and
explicitly: "The mathematical evidence is the independent derivation in
`docs/verification/reviews/2026-08-09-theory-oracle-review.md`; the small floating residuals below
corroborate code behavior but do not prove any identity." That review file exists and is tracked.
This is the correct architecture and the correct disclosure. The finding is MEDIUM, not HIGH, purely
because the project already says it. What would raise it: any later doc that cites oracle agreement
as evidence *for* a theorem. I found none.

Same verdict for `tests/test_shared_scientific_contracts.py`: it checks that two producers agree on
a three-cycle permutation and an SPD assessment. Valuable integration testing; scientifically silent.

### T-12 — Provenance-to-science ratio in the results documents
**PROCESS THEATER. MEDIUM.** `docs/results/2026-08-09-gauge-holonomy-results.md` is 164 lines.
Roughly 70 are hashes, digests, coverage percentages, `GetProcessMemoryInfo` working-set samples,
and wall-clock timings. The scientific content is **five metrics on one four-vertex graph**: four
exact zeros and one nonzero negative control (`0.07177704884455105`). The document records that a
25-sample memory probe peaked at 41,566,208 bytes. It does not record a second graph, a second
scenario family, or a sensitivity analysis. Same pattern in
`2026-08-09-gaussian-fixed-ray-results.md` lines 13–40 (eight SHA-256 values before the first number
of scientific interest) and `2026-08-09-theory-oracle-results.md` lines 20–60.

To be clear about what is *not* wrong: I searched every results doc for headline overclaim and found
essentially none. The strongest sentences are uniformly scoped — "verify the current implementation
against its declared finite fixtures and negative controls. They are numerical/software evidence,
not a proof of the analytic theory or of RG universality"
(`2026-08-09-foundation-results.md:14-16`); "does **not** prove a mathematical theorem, identify a
graph-link assignment with a base-manifold connection, establish a dynamical gauge symmetry, or
establish a continuum limit, universality, or physical time" (holonomy results `:5`). The
`n=1 exact fixture` figure caption is exemplary. **"Exact" is used correctly throughout**, meaning
exact rational arithmetic, and is repeatedly qualified as fixture-scoped.

### T-13 — Precision theater in reported statistics
**OVERCLAIM. LOW.** `2026-08-09-gaussian-fixed-ray-results.md:46-47` reports a 30-job bootstrap
median as `-0.00026786510016806844` (17 significant figures) with interval
`[-0.00029802317797700826, -0.00021070275415133334]`. With n=30 and 10,000 resamples, roughly two
significant figures are meaningful. The same doc reports `-0.0002678651001680694` and
`-0.0002678651001680684` in different places — differing in the 16th digit, i.e. reporting float
noise as data.

---

## 5. What is genuinely well done — and it is a lot

**This section is not a courtesy. The status discipline inside the formal grammar is the strongest
feature of this project and it should be preserved intact through any remediation.**

**1. Theorem-grammar status coverage is effectively perfect.** I parsed every
`\theoremheading|\propositionheading|\corollaryheading|\lemmaheading|\definitionheading|\hypothesisheading|\conjectureheading|\openproblemheading|\constructionheading|\requirementheading`
block in all 23 files — 292 environments:

```
proposition/ESTABLISHED 120   theorem/ESTABLISHED 56    definition/DEFINITION 50
hypothesis/HYPOTHESIS   23    corollary/ESTABLISHED 23  openproblem/OPEN 4
lemma/ESTABLISHED        2    construction/ESTABLISHED 1  requirement/DEFINITION 1
corollary/HYPOTHESIS     1    conjecture/CONJECTURE 1
```
**292/292 carry a status. Zero untagged. Zero type mismatches** — no CONJECTURE in theorem grammar,
no ESTABLISHED on a `definitionheading`, no DEFINITION on a theorem. The one
`corollary/HYPOTHESIS` is a deliberate and correct labeling of a conditional corollary.

**2. Zero structural SPEC §2.1 violations.** SPEC forbids adjacent status tags and multiple statuses
in one prose paragraph. Grep for adjacent tags: **0 hits**. Paragraphs with >1 status tag outside
the taxonomy table: **0**. This is a nontrivial constraint held across 847 tags and 16,821 lines.

**3. Every ESTABLISHED result without a `Proof` block carries its argument inline.** Only 6 of 202
ESTABLISHED formal results lack a proof marker, and I read all six
(`05_elbo.tex:524`, `:590`; `05d_relational_inference.tex:1280`; `06_gaussian.tex:291`;
`07_restrictions.tex:276`; `11_obstructions.tex:57`). All six are one-step derivations where the
argument is written into the statement itself — e.g. `cor:gauss-invertible-gain-factor`: "Indeed,
`prop:gauss-edge-local-characterization` makes `T_i` idempotent, and multiplying `T_i^2=T_i` by
`T_i^{-1}` gives `T_i=I`." **I found zero cases of citation-as-proof and zero circular
chapter-to-chapter citations.** The single citation-adjacent case (`prop:elbo-evidence-monotonicity`
→ `Dempster1977, Neal1998`) supplies a complete inline proof and cites only for the classical
reduction. This was the specific failure mode I was sent to find, and it is not here.

**4. The results documents' scope-denial discipline is exemplary.** Every lane document carries an
explicit "does not claim" list. `2026-08-09-gauge-holonomy-results.md` goes further with a per-result
**"Claim, evidence, and falsifier ledger"** naming the falsifier for each claim, plus an **"Explicit
unresolved-assumption inventory"** with four `OPEN/INCONCLUSIVE` bridges (graph-to-base curve,
dynamical symmetry, continuum/universality, physical time) and why the lab is insufficient for each.
That is better practice than most published physics papers.

**5. `docs/hypotheses.md` is a real preregistration instrument.** 17 entries, 16 with an explicit
**Refutation threshold**, plus Null, Control, Support threshold, Inconclusive rule, and a Theory
source pointer. It also honestly labels which "hypotheses" are software checks rather than science:
"Established conditional identity; current laboratory is an implementation check." Two entries are
deliberate negative controls (`INF-NEG-01`, `ATT-NEG-01`) whose stated epistemic status is
"Deliberately incorrect weighting control" — a project that ships intentionally wrong controls and
labels them as such is doing something right.

**6. Negative controls are present and non-degenerate.** Every metric table pairs zero residuals with
nonzero controls: `GAUGE_mismatch_kl_delta_control = -0.0405`, `GAU-01_ordinary_spectrum_change_control
= 1.8007`, `GAU-02_schur_distinction_control = 4.4545`, `INT-01_theorem_coordinate_g_norm_control =
0.7`. The foundation doc explains *why* they matter: "they show that the test suite can distinguish
theorem-coordinate G norm from weighted L2, detect incomplete relabeling, and expose pairwise
interaction nonclosure." SPEC §2.3's demand for controls is honored where it is checkable.

**7. The `appendix_numerical_provenance.tex` "What a passing run means" paragraph** is the single
best paragraph in the manuscript: "They do not prove a theorem, genericity, an asymptotic limit,
universality, or a physical interpretation... A missing protocol for an empirical statement remains
inconclusive even when every implemented check passes." Body chapters honor it
(`11_obstructions.tex:235`, "The propositions, not the computation, establish the claim").

**8. The endpoint-feasibility certificate is exemplary self-criticism.** Exact rational arithmetic,
six enumerated required premises, and the conclusion reported as refuting *its own criterion's
reachability* rather than the conjecture: "It does not refute attraction and does not prove a
mechanism." A project willing to publish a certificate that its own flagship experiment was
ill-posed is not a project trying to fool anyone.

**9. The producer/verifier separation is sound in principle.** Producers may only emit
`verification_state=CANDIDATE`; promotion is reserved to an external ledger. AUD-05 was raised
precisely because a helper could promote a caller premise. The discipline is correct; the problem
(T-06) is that the external ledger does not exist in the repository.

**Conclusion for §5:** the epistemic contract is the project's crown jewel and it holds *exactly
where it is mechanically checkable* — in the theorem environments, the metric tables, and the scope
denials. It fails exactly where it is not mechanically checkable — in prose (T-07, T-09), in the
interpretive layer (T-10), and in the linkage between claims and artifacts (T-01, T-06, T-08).

---

## 6. Claims with no traceable evidence / evidence with no claim

**Claims with no traceable evidence:**

| Claim | Location | Nominal evidence | Actual status |
|---|---|---|---|
| `NUM-CG-FACTOR-GAP-STRESS-SCHEDULE` | `appendix_numerical_provenance.tex:71` | `CHK-CG-FACTOR-GAP-STRESS-3138` | Check **absent** from the artifact entirely |
| `NUM-CG-FACTOR-GAP-BOUNDARY-PROTOCOL` | `:128` | same | same |
| All 11 other NUMERICAL claims | `06_gaussian`, `07_restrictions`, `08_infogeometry`, `11_obstructions` | 9 `CHK-*` in `current-results.json` | Artifact binds **0/23** current sources; stale in every input |
| 174 prose ESTABLISHED assertions | 20 files (§T-07) | none | no proof, no citation, no pointer |
| 2 structural-realism OPENs | `12_philosophy.tex:196`, `:210` | ledger | **absent from the ledger** |
| 22 audit defects marked `EVIDENCE_VERIFIED` | `.verification/ledger.json` | that ledger | **file absent from repo** |

**Evidence with no claim:**

| Evidence | Claim it references | Status |
|---|---|---|
| 26 `claim_id`s in `current-results.json` checks (`NUM-CG-AGGREGATION`, `NUM-RG-RAY-KERNEL`, `NUM-CG-HOLONOMY`, `REVIEW-R07-KRON-NONCLOSURE`, `RG-HOMOGENEOUS-EXACT`, …) | — | **Not in `claims.json`** (26 of 35 = 74% dangling) |
| 20 `supplemental_check_ids` in `claims.json` | — | Referenced by no claim entry |
| `theory_oracles.py` + 1,125-line test suite | — | Verifies an encoding, not a theorem (by design and by disclosure) |
| 28,213 lines in `Theory/verification/` | — | Governs a repository layout that does not exist here |
| `docs/verification/pytest-foundation.xml` (198 tests) | — | Software regression evidence; maps to no theory claim |

---

## 7. Recommendations, ordered by scientific value per unit effort

1. **Re-run `run_checks.py` at the current revision.** Twelve seconds of CPU restores the evidentiary
   status of all 13 NUMERICAL claims. This is the single highest-value action available and it has
   been deferred for three days while 23,367 lines of plans were written.
2. **Fix AUD-03, AUD-13, AUD-15, AUD-17, AUD-18 before writing another plan line.** Five findings,
   all touching core mathematical types, all with a known one-file fix, all with a reproducer
   already written in the audit. Estimated: hours. Wave A's plan for them: 3,078 lines.
3. **Delete or externalize `Theory/verification/*.py`, `lifecycle_gate.py`, `build_audit.py`, and
   `manifest-policy.json` from this repository.** 28,213 lines that constrain nothing here. If they
   belong to the Research vault, they should live there. Their presence creates a false impression
   of governance.
4. **Track the evidence or stop citing it.** Either commit `.verification/` JUnit/coverage/ledger
   artifacts (they are small) or remove the 31 dangling hash citations. A SHA-256 of an
   unobtainable file is decoration.
5. **Make `Theory/` writable, or move the ledger out of `Theory/`.** As long as the manuscript is
   read-only in the repo that produces evidence about it, no finding can ever be fixed and no
   evidence can ever close a claim. This is the root cause of T-05 and T-08.
6. **Add a pre-execution feasibility check to the preregistration gate.** Before any confirmatory
   run, compute the reachable range of the primary endpoint over the declared basin and assert the
   success threshold lies inside it. T-04 would have been a ten-line assertion.
7. **Split ESTABLISHED into PROVED-HERE and CITED-STANDARD**, and either tag the 19 normative scope
   rulings or soften `01_introduction.tex:156`.
8. **Move `claim:physical-law-identification` and `Physical-time identification` out of the
   openproblem apparatus** into a separately headed "Statements this work makes no attempt to
   settle", or supply the missing obstruction halves.
9. **Impose a plan-to-code budget.** A remediation plan longer than the code it changes is a
   symptom, not a safeguard. Current ratio: infinite.

---

## 8. The blunt version

This project has built a magnificent instrument for measuring whether it has followed its own
procedure, and has not yet used it to find out whether its claims are true. The status tags are
excellent. The scope denials are excellent. The negative controls are excellent. And then: the
evidence file matches nothing, the evidence directories are empty, the verification code points at a
repository that isn't there, twenty-two known bugs sit untouched under twenty-three thousand lines of
plans to fix them, and the one experiment aimed at the one conjecture was arithmetically incapable of
succeeding.

The pattern is legible. Every artifact whose production is *itself* verifiable — a hash, a manifest,
a gate, a tag, a plan — is produced abundantly and to a high standard. Every artifact whose value
depends on a judgment that cannot be mechanically checked — is this experiment well-posed, is this
bug worth fixing today, does this evidence actually bear on this claim — is deferred. The apparatus
has become a way of being productive without being exposed.

The good news is that the diagnosis implies a cheap cure, because the hard part is already done. The
theory is written, the labs work, the controls are real, and the honesty is genuine and unusual. What
is missing is twelve seconds of CPU, a handful of one-file bug fixes, and a decision to stop writing
plans.
