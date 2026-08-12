# RM-05 — Provenance fidelity and gate stress-test

**Subject:** `ChatGPT/MultiAgentELBO/docs/research-plans/2026-08-12-pifb2-continuum-roadmap.md` (175 lines)
**Auditor role:** research-integrity. Two jobs — provenance fidelity against the cited decision report, and pre-execution stress-test of E0–E7 / WP0–WP6 against failure mode T-04.
**Execution policy:** CPU only. **No GPU or CUDA job was started.** The one numerical check run (E2 tautology demonstration) used numpy/float64 in the Linux sandbox.

---

## 0. Verdict in one paragraph

The roadmap is a good document with a bad citation layer and an ungradeable experiment table. Its *conceptual* fidelity to the decision report is high — six of the seven counterexample-register items are correctly absorbed. Its *scope* fidelity on the headline claim is not: it applies a theorem proved for **frozen attention rows on a mean-field product family** to "the complete live-peer PIFB2 action", which is exactly the conflation wave-1 finding F3 flagged in PIFB2's own abstract. Two of its cited sources cannot be inspected (the `MAgent_Model-main` implementation, and the "separate revision-bound verification ledger" on which the word *verified* rests). And of the eight experiments, **three have gates that cannot fail** (E2 arm 1, E4 arm 1, and E5 in the negative branch), **five have no tolerance of any kind**, and **one (E7) is passable by tuning ~26 free parameters**. The word "tolerance" appears zero times in the file; so do "threshold", "effect size", "power", "confidence", "reachable", and "feasibility" (`grep -c -i` over the roadmap, each = 0). T-04 was caused by a threshold nobody checked for reachability. This roadmap freezes no thresholds at all, which is a different failure with the same root: the gates carry no arithmetic anyone could check.

---

# JOB 1 — PROVENANCE FIDELITY

## 1.1 Headline claim: faithful in modality, overreaching in scope

**Roadmap, line 9:**
> "The complete live-peer PIFB2 action **should not be represented** as the negative ELBO of one fixed joint law on the original agent-state variables."

Restated at **line 166** ("the complete live-peer action is not an ordinary fixed-joint state-level ELBO on the original variables") and **line 174** ("retaining the **verified** state-level ELBO obstruction").

**The decision report's actual statement, `final-report.md:18`:**
> "The live-peer term is a legitimate engineered configuration energy but, **on the theorem's stated open factorized family with fixed row variables**, is not the ordinary ELBO of one fixed normalized joint on the original state variables."

**`construction-or-strongest-theorem.md:4`:**
> "the scoped representation obstruction: **with row variables fixed on the declared fine site-factorized open family**, the live transported peer-KL scalar cannot equal, up to a constant, the negative ELBO of one fixed normalized joint…"

**The underlying theorem, `Research/manuscripts/PIFB2.tex:3280` (`thm:state_level_elbo_nogo`).** Its hypotheses, in full:

1. the factors `q_i ∈ Q_i` **vary independently** — i.e. the recognition law is the **product** `⊗_i q_i`, on a *mixture-open* family of strictly positive densities (`PIFB2.tex:3278`);
2. at least one nonself coefficient `β_ij > 0`, **appearing as a constant in the functional** — the rows are not varied;
3. `D³_{q_i q_j q_j} F_rest = 0` for `i ≠ j` — a structural hypothesis on everything outside the peer sector;
4. one active edge admits a tangent `h_j` with `g_ij := (T_ij h_j / T_ij q_j)²` bounded and **nonconstant** `q_i`-a.e.;
5. "All differentiated integrals below are assumed finite" (`PIFB2.tex:3278`) — flagged as weak rigor by wave 1 F2.

Conclusion: no `p_θ` on `∏_i X_i` **independent of q** and no constant `c` with `C(q) = KL(⊗_i q_i ‖ p_θ) + c` throughout the open product family.

And PIFB2's own scope remark, `PIFB2.tex:3333` (`rem:state_level_elbo_nogo_scope`):
> "…It does not exclude frozen source templates, restricted quadratic families, compatible auxiliary variables, a model selected after a fixed point, or a probability law over belief configurations. **If the attention optimum β\*(q) has already been substituted, its response derivatives define a different reduced functional and require a separate representation test.**"

**Verdict on phrasing — it is simultaneously weaker and stronger, in different dimensions:**

| Dimension | Theorem | Roadmap line 9 | Verdict |
|---|---|---|---|
| Modality | "there is no `p_θ`… " (impossibility) | "should not be represented" (prudential) | **Weaker** — and appropriately so for a strategy document. No objection. |
| Object | the frozen-`β` consensus functional `C(q)` | "the **complete** live-peer PIFB2 action" | **Stronger — SCOPE ERROR.** See §1.3. |
| Recognition family | product `⊗_i q_i`, mixture-open | unqualified | **Stronger.** `approach-registry.json:49` states the residual gap explicitly: "The obstruction does not classify every correlated or coarser recognition family." A correlated `Q` is not excluded by the theorem and is not excluded by the roadmap's sentence either — but the roadmap presents the sentence as settled. |
| Epistemic status | `claim-ledger.json:14` `"state": "INCONCLUSIVE"`; `release.json:7` `"terminal_status": null`; `final-report.md:10` "This is a **bounded checkpoint**." | line 174: "the **verified** state-level ELBO obstruction" | **Stronger.** See §1.2/§1.4. |

**Severity: HIGH (scientific + provenance).** The prudential modality is defensible. Dropping "with fixed row variables" and "on the product family" is not, because the roadmap's own T3 (line 115) plans to *eliminate the rows* and work with the reduced `−τ log Z` functional — i.e. it plans to operate precisely in the regime the theorem excludes.

## 1.2 What the source proves that the roadmap does not use

| # | Source result | Where | Roadmap use | Sev |
|---|---|---|---|---|
| U-1 | **The exact cross-scale Gaussian exception.** At zero within-scale coupling with a nondegenerate top prior, the stacked precision is SPD, the joint is proper, MF coordinate ascent is Gauss–Seidel on an SPD system, and "**In this regime the ELBO interpretation is exact and the fixed point exists and is unique**". | `PIFB2.tex:3337`; registered at `approach-registry.json:43` as a valid restricted realization ("zero-within-scale hierarchies") | **Not mentioned anywhere.** Line 106 lists candidate exact sectors (self-prior, observation, fixed-connection Markov field, covariant Dirichlet) and omits the single strongest *proved* exact-ELBO result available. E5 would answer this in its first hour if it knew about it. | **HIGH** |
| U-2 | The obstruction **does not classify correlated or coarser recognition families**. | `approach-registry.json:49` | Not mentioned. The roadmap's claim-discipline paragraph (line 166) would be materially stronger and *more* defensible with this caveat in it. | MED |
| U-3 | Exact row minimization is **already verified finitely** (`β* = π e^{−E/τ}/Z`, value `−τ log Z`; wave 1 checked `min_β L = −0.10738678690` vs `−τ log Z = −0.10738678695`). `approach-registry.json:22`: "the current manuscript supplies the intended action skeleton **and exact row minimization**". | `approach-registry.json:22` | T3 (line 115) lists row elimination as an unproved target with no note that the pointwise algebra is banked and only the *measurable-selection / envelope-in-`L¹`* part is new. Wastes the head start. | MED |
| U-4 | The source is an explicitly **non-terminal bounded checkpoint** with `terminal_status: null`, `certificate_claim: null`, `evidence: []`, `assumptions: []`, and `dependency-dag.json:5 "edges": []`. | `release.json:7-8`, `claim-ledger.json:5-6`, `dependency-dag.json:5` | The roadmap's "Executive decision" (lines 7–13) reads as settled. Line 174 calls the obstruction "verified". Nothing signals the source's own INCONCLUSIVE state. | **HIGH** |
| U-5 | Three of four adversarial attacks are `"disposition": "OPEN"` (`base-measure-and-domain`, `ultralocality`, `gauge-and-noncompactness`); only `state-elbo-conflation` is `SURVIVES_WITH_SCOPE`. | `adversarial-report.json:13,23,40,31` | The three OPENs are correctly folded into T0/T5/WP1 — **good, credit given**. But the one that *survived with scope* is the one whose scope the roadmap drops. Exactly inverted. | — |

## 1.3 Roadmap assertions with no support in the source

| # | Roadmap assertion | Line | Support found | Sev |
|---|---|---|---|---|
| A-1 | "the **complete** live-peer PIFB2 action should not be represented as the negative ELBO…" | 9, 166 | Source scopes to frozen rows (`final-report.md:18`). Reduced case explicitly deferred by PIFB2 itself (`3333`). **Unsupported as stated.** | **HIGH** |
| A-2 | "retaining the **verified** state-level ELBO obstruction" | 174 | `claim-ledger.json` `evidence: []`. The verification is delegated to "a separate revision-bound verification ledger" (`final-report.md:14`) which is **not in the bundle and not in any mounted repo** — see §1.5. | **HIGH (provenance)** |
| A-3 | The MAgent code "represents Gaussian belief and model fields, covariance fields, supports, and `GL(K)`-type frames over a **grid-shaped base**; performs **volume-weighted aggregation**; and contains self, peer, observation, frame, curvature, and optional base-neighbor sectors." | 158 | **Code absent.** See §1.5. | **CRITICAL (provenance)** |
| A-4 | "**Its README** correctly states that the population coupling is an engineered consensus energy rather than the negative ELBO of one fixed population joint." | 158 | `grep -n -i "engineer\|consensus\|population"` over `MultiAgentELBO/README.md` and `ChatGPT--MultiAgentELBO/README.md` (223 lines each) → **zero hits in both**. The README quoted does not exist in either mounted repo. | **CRITICAL (provenance)** |
| A-5 | "Its **fixed-connection, attention-free covariant Markov-field term** is identified as a closed-ELBO member… Its **frame-smoothness term** is gauge fixing. Its **frame-derived connection** is pure gauge." | 160 | Four specific claims about a codebase that is not present. The *propositions* are individually plausible (item 5 of the counterexample register supports the last one as a theorem) but the attribution "already present in the implementation" is uncheckable. | HIGH |
| A-6 | "T7… Prove that derivative and curvature sectors vanish and the theory reduces to **PIFB2 `G`-attention**." | 119 | No source states PIFB2's zero-dimensional limit is "`G`-attention"; PIFB2's attention is `GL(K)`-flavored. This is a design proposal, correctly, but it is stated in the grammar of a recovery. | LOW |
| A-7 | "The structural theory **is** neither Gaussian nor intrinsically `GL(K)`." | 13 | This is the roadmap's own proposal, not a finding. It is honest one sentence later ("Gaussian fibers and `GL(K)` frames are one tractable realization used by the present code") but the indicative "is" overstates. | LOW |

**Correctly used, and worth crediting.** Six of seven `counterexample-register.md` items are absorbed cleanly and in the right places:

| Register item | Roadmap |
|---|---|
| 1 missing base measure (`:4`) | line 32 — verbatim in spirit, plus the two alternatives |
| 2 locally defined sections in global integrals (`:6`) | lines 56, 78, 85, 91 — self terms on `U_i`, pair terms on `U_i∩U_j` |
| 3 empty attention row (`:8`) | T3 line 115, "fixed nonempty measurable neighbor sets; positive row priors" |
| 4 ultralocal base dynamics (`:10`) | T5 line 117 ("must be identified as pointwise, not propagating") and E4 |
| 5 pure-gauge transport (`:12`) | line 66 — correctly stated as a theorem |
| 6 noncompact gauge escape (`:14`) | lines 13, 147 — compact `G` as an analytical hypothesis, not an ontological one |
| 7 fixed-joint obstruction (`:16`) | lines 9, 166 — **scope stripped** |

That is a genuinely careful absorption of a technical source. The defect is concentrated in item 7 and in the two absent artifacts.

## 1.4 Frozen vs reduced — the scope error, precisely

**A correction to the tasking first.** The frozen/reduced finding is **wave 1, finding F3**, not wave 2. It is at `docs/audits/2026-08-11-ultradeep-expert-audit.md:136` and in full at `docs/audits/ultradeep-2026-08-11/audit-02-infogeometry.md:139-165`. `grep -rni "frozen\|freez" ultradeep-wave2-2026-08-12/wave2-01-constructions.md` returns **zero hits**; `grep -rn "3.54085"` across `docs/audits/` returns exactly two hits, both wave 1. The numbers in the tasking are correct; the file attribution is not.

**The wave-1 F3 computation** (`audit-02-infogeometry.md:153-156`, mpmath 60 dps, two agents, one active peer source per row plus a null source, `τ = 0.8`):

```
frozen-beta consensus C(q)        D3_{q1 q2 q2} = -1.94227605348e-5
reduced  -tau * sum_i log Z_i(q)  D3_{q1 q2 q2} = -3.54085893855e-5
fixed-joint mean-field control    D3            = -3.63009224554e-65   (numerical zero)
```

The control is the load-bearing part: `D³_{q_i q_j q_j} KL(⊗q ‖ p) = 0` **identically** for any fixed `p` (`PIFB2.tex:3308`, `eq:fixed_joint_third_variation_zero`), so a nonzero value certifies non-representability. F3's conclusion: the stronger (reduced) claim "appears **provable, not merely open**" — a witness, not a proof.

**Does the decision report cover the reduced case?** **No.** Both places where it states the result carry the frozen-row qualifier: `final-report.md:18` ("with fixed row variables") and `construction-or-strongest-theorem.md:4` ("with row variables fixed"). The two JSON restatements drop it — `counterexample-register.md:16` and `approach-registry.json:38` say only "on the scoped open factorized family" — so the scope is present in the prose and already eroding in the machine-readable layer.

**Does the roadmap distinguish them?** **No — and it conflates them in a way that matters, because its own plan lives in the reduced regime.**

- Line 9 / line 166 assert the obstruction for the **complete** action.
- **T3, line 115**, plans exactly the substitution that produces the reduced functional: "Prove strict convexity, unique `β*, γ*`, **reduced log-partition values**, measurable dependence on fields, and **the envelope derivative**."
- After T3, `S` *is* the reduced functional `S_rest − τ Σ log Z`. The frozen-`β` theorem does not apply to it. The roadmap never says so.
- **E5, line 136**, is the experiment that would settle it, and it is written with no reference to the frozen/reduced split and no reference to the `D³` instrument that would decide it in ten lines.
- Line 174's word "verified", applied to an obstruction whose reduced form has one numerical witness and no proof, is the point at which a strategy document becomes a claim.

**Severity: HIGH (scientific).** This is F3 reproduced at the roadmap layer. F3's complaint was that PIFB2's abstract states the frozen-`β` obstruction two sentences after describing the reduced functional, so "a reader will merge them". The roadmap merges them explicitly.

**Two-line fix, both cheap:**
1. Line 9 → "…the complete live-peer PIFB2 action, **with its attention rows held fixed and on a mean-field product recognition family**, should not be represented…"
2. Add one sentence: "The obstruction for the **reduced** (row-eliminated) functional is **not proved**. A 60-dps witness (`D³ = −3.54e-5` against a fixed-joint control of `−3.63e-65`) indicates it is provable; proving it is a WP5 deliverable, and E5 should compute it as its first case."

The second is upside, not just correction: it converts an audit finding into a named, small, likely-winnable theorem.

## 1.5 The absent code and the absent ledger

**`MAgent_Model-main` — ABSENT.** Searches run, all over the three mounted repos (`MultiAgentELBO/`, `ChatGPT--MultiAgentELBO/`, `Research/`):

| Search | Result |
|---|---|
| `grep -rn "MAgent_Model-main"` (all repos, all file types) | **0 hits** |
| `grep -rn -i "MAgent_Model\|MAgent Model\|MAgent code" --include=*.{md,tex,py,json,bib}` | 0 hits in either code repo; hits in `Research/` only, all referring to the *model* (`MAgent_exact_elbo_whitepaper.tex`, wiki notes), never a directory |
| `find … -maxdepth 3 -type d -iname "*agent*"` | only `MultiAgentELBO/.git/worktrees/*` — no `MAgent_Model` tree |
| `grep -rn -i "volume-weighted\|volume_weight" src/ README.md` | **0 hits** |
| `grep -rn -i "grid" src/multiagent_elbo/` | 2 files (`figures.py`, `finite/experiment.py`) — plotting grids, not a base manifold |

What *is* in this repository is `src/multiagent_elbo/` — `artifacts.py`, `conditioning.py`, `config.py`, `cuda_backend.py`, `experiment_support.py`, `figures.py`, `rendering.py`, `runtime.py`, and the `finite/`, `geometry/`, `realizations/` packages. That is the **finite laboratory** wave 1 audited: finite agent sets, finite designs, `Fraction`/float64 exact lanes, no base-manifold integrals at all (`grep -F 'int_{\mathcal C}'` over 24 TeX files returns **zero**, wave-1 S1 coordinator log). It is not a grid-shaped continuum discretization with volume-weighted aggregation. The roadmap's §"Relationship to the existing code" (lines 156–162) describes a **different codebase**.

**Severity: CRITICAL (provenance).** This is precisely the defect class wave 1 named at S6: "31 cited evidence paths are absent… A hash of an unobtainable file cannot fail, and therefore carries no information." Lines 156–162 make seven checkable technical claims about code the reader cannot inspect, and one of them (A-4, the README quotation) is checkably **false against the READMEs that do exist here**. Note the roadmap is *self-aware* enough to date the inspection ("inspected on 2026-08-12", line 174) — so this is most likely a real external repo the author has locally. That does not fix it. Either vendor it, path-cite it with a commit hash, or mark the whole section `> [!note] Describes an external repository not in this tree` and drop the README paraphrase.

**The "separate revision-bound verification ledger" — ABSENT.** `final-report.md:14` and `construction-or-strongest-theorem.md:4` both delegate the *only* verified result to it, and it has no path, no ID, and no hash. `grep -rln "state_level_elbo_nogo\|state-level ELBO obstruction\|state-level no-go"` over `Research/docs`, `Research/manuscripts`, `Research/wiki`, `ChatGPT--MultiAgentELBO/docs` returns five files: `PIFB2.tex` and `PIFB2.aux` (the theorem itself), `Research/wiki/themes/Inference machinery — variational EM and filtering.md` (a synthesis note), the `final-report.md` making the claim, and the roadmap repeating it. The one file named `verified-ledger.md` (`Research/manuscripts/verified-ledger.md`, 545 lines) is the **GL(K) manuscript** ledger — its frontmatter reads `title: GL(K) Manuscript Verified Ledger` and its scope is `GL(K)_attention.tex`, `GL(K)_supplementary.tex`, `PIFB.tex`, `meta_entropy.tex`, `belief_inertia.tex`. It contains no entry for the state-level no-go.

So the chain is: **roadmap line 174 "verified" → `final-report.md:14` "a separate revision-bound verification ledger" → nothing resolvable.** Meanwhile `claim-ledger.json:5-6` reads `"assumptions": []`, `"evidence": []`, and the sole claim is `INCONCLUSIVE`. **Severity: HIGH (provenance).** The theorem in `PIFB2.tex:3280` is real and its algebra was independently confirmed by wave 1 to 11 digits — so the *underlying mathematics* is fine. What is missing is the artifact the word "verified" points at. Repair: cite `PIFB2.tex:3280 (thm:state_level_elbo_nogo)` and `audit-02-infogeometry.md:127-137` directly, and delete the reference to an unnamed ledger.

---

# JOB 2 — GATE STRESS-TEST

## 2.0 The T-04 template

`docs/audits/ultradeep-2026-08-11/audit-05-traceability.md:192-231`. Preregistration froze "a slope of at most `-0.02` radians per scale" as the support threshold. The later certificate proved `rational_slope_lower_bound = -9/625 = -0.01438895606`, `rational_margin_above_threshold = 7/1250 = 0.0056`, `paired_support_boundary_reachable: false`, `certificate_status: "certified_unreachable"`. Forty confirmatory jobs, 640 serial CUDA exchanges, 3,644 GPU-seconds, a five-job parity sentinel, 240 controller/worker comparisons, an operator gate and an environment-lock digest were spent on an experiment with **one reachable outcome**. Wave-1 N-09 identifies the proximate cause: the endpoint regressed the **raw** angle, which decays geometrically, when the linear structure lives on `log θ` (`-0.916284..-0.916245` = `log 0.4` to `4e-5`).

The generalizable lesson has three parts, and only the first is usually noticed:
- **(a) reachability** — is the threshold inside the attainable range?
- **(b) scale** — is the endpoint defined on the scale where the effect is linear?
- **(c) firing** — has the gate ever been observed to reject anything?

Part (c) is the one this project fails most often: wave-1 N-02 (`premises_passed=True` as a literal, `grep premises_passed=False` over 20,705 test lines → **0 hits**), N-07 (`defect_is_psd` PSD by construction), RG-2/RG-3 (identical expressions compared to each other), wave-2 W5 (`minimum_diagonal = Fraction(1,10**100) > 0`; `inside_declared_domain` / `assumptions_satisfied` boolean literals at all four call sites).

## 2.1 E0–E7

Legend: **CANNOT FAIL** = the gate is satisfied by any correct-or-incorrect implementation, or by a theorem. **UNGRADEABLE** = no threshold exists, so neither pass nor fail is determinable. **TUNABLE** = passable by parameter search.

| Exp | Gate as written (line) | Defect | Sev |
|---|---|---|---|
| **E0** | "Match values, attention optima, and directional derivatives for at least categorical and Gaussian fiber realizations, including asymmetric interactions." (131) | **UNGRADEABLE.** No tolerance, no norm, no configuration count, no seed policy. Worse, no *correspondence*: a categorical fiber and a Gaussian fiber have different sample spaces, so "match values" is undefined until a declared statistical isomorphism (e.g. 2-point categorical ↔ 1-D Gaussian) fixes what is being compared to what. Under strict reading (exact equality) it can never pass in float64; under loose reading it can never fail. | **HIGH** |
| **E1** | "Apply random local gauge transformations to all covariant inputs. Require invariant action values and correctly transformed gradients; show separately that explicit gauge fixing changes." (132) | **Not a scientific test — a bug-catcher.** Wave-1 S4 is decisive: covariance "is imposed by requiring…" (`05b:66`, a DEFINITION), `hyp:gen-kernel-covariance` is a HYPOTHESIS (`04:379`), `06_gaussian.tex:297` "The document does not claim that it is forced by anything", `07b:1257` disclaims uniqueness. E1 verifies a property the code was **built to have**. Real, but it discriminates implementations, not theories. **Plus a live numerical trap:** wave-2 F-1 measured `apply_frame_change` passing all gates (`max_frame_condition = 1e6`, `min_spd_rcond = 1e-12`) while residuals hit `8.514e-08` and `3.384e-06` against a `1.01e-10` grading tolerance — **843×** and **33,500×**. "Random local gauge transformations" from a noncompact `G` will fail E1 for conditioning reasons at any nontrivial draw. Measured safe ceilings: frame cond ≈ `3e3`, `min_spd_rcond` ≈ `1e-7`. | MED (sci) / **HIGH** (will misfire) |
| **E2** | "Compare pure transition/coboundary links with independent link or connection data. **Require trivial loop holonomy in the former** and controlled nontrivial holonomy only in the latter." (133) | **ARM 1 CANNOT FAIL — it is a theorem.** `counterexample-register.md:12`: "If every comparison map is `U_iU_j^{-1}`, cycle holonomy is trivial." The roadmap itself states it as a theorem at **line 66**. The product telescopes: `(U_1U_2^{-1})(U_2U_3^{-1})…(U_nU_1^{-1}) = I` identically. **Verified on CPU** (numpy, float64, `K=4`, 5-edge cycle `0→2→5→3→1→0`): deviation from `I` = `3.5585e-14` at frame conditions up to `1.7e3`; inserting a singular value of `1e-9` (cond ≈ `1e9`) gives `3.5600e-14` — **unchanged to three digits**. The arm measures BLAS round-off and is insensitive even to catastrophic conditioning. **Arm 2 is UNGRADEABLE:** "controlled nontrivial holonomy" has no predicted value, so any nonzero number passes. | **CRITICAL** |
| **E3** | "Use manufactured smooth section fields on refined meshes and **estimate convergence** of quadrature, covariant derivatives, action values, and gradients." (134) | **UNGRADEABLE — no rate.** "Estimate convergence" names a quantity to report, not a criterion. No mesh sequence, no norm, no expected order, no refinement count. Every possible outcome passes. | **HIGH** |
| **E4** | "Perturb one region with `η_q=η_s=0` and with positive coefficients. **The first case should remain ultralocal**; the second should follow the PDE behavior derived in T5." (135) | **ARM 1 CANNOT FAIL as stated** — `counterexample-register.md:10` already proves it: "With no derivative or nonlocal kernel involving `q_i` and `s_i`, perturbations at distinct base points do not couple." At `η=0` the off-site response is **identically zero by the structure of the functional**, so arm 1 measures round-off exactly as E2 arm 1 does. *However*, there is real content one layer down that the gate does not name: the **discretization** can introduce spurious coupling (quadrature stencils, global normalizers, `ℓ²` projections, shared support masks). Rewritten as a leak test it becomes the most valuable experiment in the table. **Arm 2 UNGRADEABLE:** no decay law, no length scale, no tolerance. | **HIGH** |
| **E5** | "**Construct or fail to construct** a normalized fixed joint for every sector. Compare exact source-label updates with engineered attention across temperatures and family-specific assumptions. Report residuals explicitly." (136) | **NO FAILURE CRITERION.** "Fail to construct" is unobservable: absence of a construction after finite effort is not evidence of impossibility, and no effort bound is stated. As written the negative branch can never be legitimately recorded and the gate has no stopping rule. **And the decidable instrument already exists and is not named:** `eq:fixed_joint_third_variation_zero` (`PIFB2.tex:3308`) gives `D³_{q_i q_j q_j} = 0` identically for *any* fixed `p_θ`, so a nonzero `D³` **certifies** non-realizability in exact arithmetic. Wave 1 F3 already ran it with a working control (`−3.63e-65`). E5 should be a decision procedure, not a search. | **HIGH** |
| **E6** | "Compare automatic derivatives, finite directional derivatives, natural-gradient steps, and action dissipation." (137) | **UNGRADEABLE, and a classic false-pass.** No tolerance, no step-size schedule. At a single fixed `h`, autodiff and finite differences agree to ≈`√ε` for both correct and subtly-wrong gradients — the comparison only has power as an *error-vs-h slope*. And "action dissipation" gates on `dS/dt ≤ 0`, a one-sided inequality that a **broken** integrator satisfies trivially at small enough step. T6 (line 118) states the sharp identity `dS/dt = −‖grad S‖²`; the experiment drops the equality and keeps the inequality. | **HIGH** |
| **E7** | "Pre-register observables such as correlation length, consensus rate, defects, holonomy response, and scaling behavior; compare against simpler consensus, Markov-field, and transformer baselines across seeds and sizes." (138) | **TUNABLE + UNGRADEABLE + no analysis plan.** (i) No observable is operationally defined. (ii) No baseline is specified — *which* consensus model, *which* Markov field, *which* transformer at what size trained on what. (iii) No effect size, no power calculation, no primary endpoint, no multiplicity correction: 5 observables × 3 baselines × seeds × sizes is ≥ 15 comparisons, and wave-2 W5 scored `confirmatory_analysis.py` at **5/15** on mutation with **Holm → Bonferroni**, a reversed sign-test tail, `95% → 90%` CI, and a dropped two-sided factor all surviving undetected. (iv) **Tunability**: the action at lines 76–102 carries **6 free scalars** (`λ_s, τ_q, τ_s, η_q, η_s, κ`), **≈13 free functions/structures** (`μ`, the base cometric, `χ_i`, `χ_ij`, `π^q`, `π^s`, `L^q`, `L^s`, `D_q`, `D_s`, `L^obs`, `A`, `S_boundary`), and **7 structural choices** (`G`, `ρ_q`, `ρ_s`, `M_q`, `M_s`, base dimension `d`, the cover `{U_i}`) — **≈26 degrees of freedom** against a target as soft as "predicts more than generic consensus optimization". With that freedom and no frozen parameters, E7 is passable by search. (v) The roadmap says "pre-register" but names no registrar, no timing relative to pilot data, and no parameter freeze. | **CRITICAL** |

### Sharp replacements

- **E0.** Declare the fiber correspondence explicitly (2-point categorical ↔ 1-D Gaussian via a named statistical isomorphism). Gate: `|S_cat − S_gauss| / (1+|S_gauss|) < 1e-10`; attention optima agree in `ℓ∞` to `< 1e-10`; directional derivatives agree with central differences at the *measured* `O(h²)` slope `2.0 ± 0.1` over `h ∈ [1e-2, 1e-5]`, noise floor located and excluded. `N ≥ 32` random configurations, seeds recorded and **consumed** (wave-1 N-01: `RngStreams.from_seed` is called in 12 modules and consumed in exactly **one**). **Firing control:** a fiber implementation with one deliberately wrong KL constant must be rejected — run it and publish that it failed.
- **E1.** Sample `g` from a declared measure on **compact** `G` (consistent with WP1's own compact-`G` restriction). Report invariance residual as a *function* of `cond(g)`; declare the ceiling from measurement, not from hope (wave-2 F-1: ≈`3e3`, not `1e6`). Replace any backward-error metric with a forward one (wave-2 F-2: `GAU-01_eigenpair_residual` read `3.249e-17` while true forward spectral error was `1.850e-06`). **Firing control:** the frame-smoothness term (which the roadmap itself calls gauge fixing, line 160) must *fail* invariance. A gauge test with no non-invariant control is a tautology with extra steps.
- **E2.** Invert both arms. **Arm 1 → sensitivity:** perturb a coboundary by `ε` and report the smallest `ε` the holonomy estimator resolves — a power curve, not a null. **Arm 2 → recovery:** construct a link field with *analytically computed* holonomy `H_true` and gate on `‖H_est − H_true‖ / ‖H_true‖ < tol`. Delete "require trivial holonomy in the former"; it is line 66 restated as an experiment.
- **E3.** Manufactured solutions with known exact `S`. Mesh sequence `h, h/2, h/4, h/8`. Gate on **observed order** `p_obs = log₂(e_h / e_{h/2}) ∈ [p−0.25, p+0.25]` for the declared element/quadrature order `p`, over ≥3 successive ratios, separately for quadrature, covariant derivative, action, and gradient. **Feasibility precondition (T-04-shaped):** verify *before running* that the finest level's expected error exceeds the float64 noise floor — otherwise the last refinement saturates, `p_obs` collapses, and you will have burned the sweep on an unreachable criterion.
- **E4.** Arm 1 → **discretization-leak test**: "off-site response ≤ `B` where `B = c·ε·‖·‖` is stated in advance; if exceeded, name the term responsible." Arm 2 → gate on the T5-derived correlation length `ξ(η)` within a stated relative tolerance, over ≥3 values of `η` spanning a decade, with the fitted exponent of `ξ(η)` compared to the derived exponent.
- **E5.** Per sector, compute `D³_{q_i q_j q_j}` in exact/high-precision arithmetic **with the fixed-joint control alongside every reported number** (F3's `−3.63e-65` is the model). Classify: **NON-REALIZABLE** (`|D³|` above a certified bound), **CANDIDATE** (`D³ = 0` to declared precision) → then a bounded construction attempt in a *declared* family with a *stated* effort budget, or **OPEN**. First case to run: the reduced `−τ Σ log Z` functional (§1.4). Second: the zero-within-scale cross-scale hierarchy, where the answer is already **proved exact** (§1.2, U-1).
- **E6.** Gate on the finite-difference error *slope* (`2.0 ± 0.1` for central differences over a declared decade, noise floor excluded), not on agreement at one `h`. Gate dissipation on the **relative residual of `dS/dt + ‖grad S‖²`**, not on `dS/dt ≤ 0`. **Firing control:** a deliberately wrong mobility metric must break the identity.
- **E7.** This one needs to be rewritten, not patched. One **primary** observable with an operational definition and a **predicted sign and magnitude**. Named baselines with named configurations. Parameters frozen and hashed **before** any baseline is run. A power calculation giving the seed/size budget. A single preregistered decision rule with a named multiplicity correction. Everything else is secondary and labelled exploratory. Until that exists, WP6 (which depends on E7) cannot be reached.

## 2.2 WP0–WP6

| WP | Exit gate (line) | Decidable? | Notes | Sev |
|---|---|---|---|---|
| **WP0** | "No symbol in the action is multiply typed or undefined; Gaussian and `GL(K)` are explicitly examples." (146) | **YES — mechanically.** | The **only** objectively decidable gate in the table, and cheap: build a symbol table and assert one type per symbol. It also has **known failing input**, so it will fire immediately: wave-2 W4 tabled 15 notation drifts with file:line on both sides — `Θ` as an affine map at `05d:259`, as `Θ_ℓ f = f∘ϑ^{-1}` at `07b:1262`, against SPEC's `Θ_e^x ∈ G`; `Φ` as a Gram matrix at `05d:282` vs the cross-bundle morphism; `τ` as Fisher clock, `G`-valued transport, softmax temperature, **and** tier label. Make "or undefined" decidable by shipping a closed symbol inventory. | — (good) |
| **WP1** | "**Independent proof review closes** well-definedness, gauge covariance, row elimination, and existence. At least two nonisomorphic statistical families instantiate the hypotheses." (147) | **Arm 1 NO — opinion. Arm 2 YES.** | *Who* is independent? Wave 1 and wave 2 were LLM agents in the same session. *What standard?* This project's internal notion of "closed" has a measured ≈35% false-positive rate: wave-1 T-07, **174 of 501 ESTABLISHED tags sit on prose with no proof, no citation, and no pointer**; wave-2 07B-S2, `07b` carries **81 ESTABLISHED and 0 HYPOTHESIS in 2,828 lines**. Arm 2 is genuinely good — sharpen by naming the families in advance and requiring a per-hypothesis check table with a witness or proof for each. **Feasibility precondition, and this is a live T-04 risk:** T1/T4 (lines 113, 116) require "compact or coercively confined admissible fiber subsets". The **categorical simplex interior is not compact** (KL diverges at the boundary) and the **Gaussian mean space is not compact**. If the two announced example families do not satisfy the theorem's own compactness hypotheses, WP1's second arm is unreachable — and that is discoverable in ten lines *before* the manuscript is written. Check it first. | **HIGH** |
| **WP2** | "Independent derivation and numerical directional-derivative oracles **agree**; dissipation is **reproduced** by the reference integrator." (148) | **NO — both arms.** | "Agree" and "reproduced" carry no tolerance. Inherits E6 wholesale; fix together. Note wave-1 T-11: `theory_oracles.py` is genuinely implementation-independent (stdlib `Fraction`, imports nothing from the package) but **assumption-identical** — "it can indict an encoding, never the theory." An oracle sharing the derivation's assumptions is a consistency check, not an independent one. Say which kind WP2 is buying. | **HIGH** |
| **WP3** | "**E0–E4 pass.** The current Gaussian/`GL(K)` code is mapped as one backend, not treated as the abstract theory." (149) | **NO (arm 1). YES if operationalized (arm 2).** | Arm 1 inherits every defect above: E0/E3/E4-arm-2 have no thresholds, E2-arm-1 and E4-arm-1 cannot fail. "E0–E4 pass" is currently **ungradeable by construction**. Arm 2 becomes decidable as a grep: the abstract layer contains zero Gaussian- and zero `GL(K)`-specific symbols. Make it that grep and run it in CI. | **HIGH** |
| **WP4** | "The zero-dimensional equality **is exact** and at least one higher-dimensional discretization **converges**." (150) | **Arm 1 YES if "exact" is defined; arm 2 NO.** | Say whether "exact" means *symbolic identity* (sympy — decidable, and the right choice) or numerical agreement (needs a tolerance). "Converges" without a rate is E3's defect again. | MED |
| **WP5** | "Every action sector is **labeled** exact, approximate, effective, geometric, gauge-fixing, or open." (151) | **YES as completeness — but TRIVIALLY SATISFIABLE.** | Labelling every sector "open" passes the gate. The gate has zero correctness content. **Fix:** require a certificate per label — *exact* ⇒ display the normalized joint and the equality up to a constant; *effective* ⇒ display the nonzero `D³` witness **with its fixed-joint control**; *gauge-fixing* ⇒ display the transformation that changes it; *open* ⇒ name the specific missing lemma. Then "open" stops being free. | **HIGH** |
| **WP6** | "At least one pre-registered prediction **survives** family, group, seed, size, mesh, and structural ablations before RG or physics claims advance." (152) | **NO — and it is the gate T-04 already broke.** | "Survives" is undefined. Six ablation axes with no multiplicity plan and no per-axis criterion. And structurally: T-04's preregistered prediction "survived" nothing — it was *reported inconclusive*, and the classification "was determined by the design, not by the data" (`audit-05-traceability.md:216`). WP6 reproduces the form of that preregistration without the fix. It must inherit the feasibility certificate below as a hard precondition or it repeats T-04 across six axes instead of one. | **CRITICAL** |

---

## 2.3 The missing gate — Feasibility Certificate (FC)

Mandatory precondition for **every** preregistration in this project. One page, ≤30 lines of arithmetic, committed **before** the run directory is created, hash recorded in the run config. If it takes longer than a page, the endpoint is not yet well defined — that is itself the finding.

**FC-1 — Endpoint, on the right scale.**
State the primary endpoint as a one-line function of raw outputs, naming the scale explicitly (raw / log / normalized / rank). Justify the scale by the expected functional form. *T-04's proximate cause was a raw-vs-log error: the raw angle decays geometrically, OLS slopes spanned `−0.0057 .. −0.000086`; on `log θ` the same data gives `−0.916284..−0.916245`, i.e. `log 0.4` to `4e-5` (wave-1 N-09).*

**FC-2 — Attainable range, in exact arithmetic.**
Compute `[lo, hi]` for the endpoint over the declared basin / configuration space, in rational or interval arithmetic, at the **least-favorable admissible configuration**. Publish `lo` and `hi` as exact numbers. *T-04's certificate did exactly this — `−9/625` — six days late.*

**FC-3 — Reachability assertion.**
Assert `lo < threshold < hi` and publish the margin as an exact rational. **If the threshold lies outside `[lo, hi]`, the preregistration is VOID — do not run.** *T-04: `rational_margin_above_threshold = 7/1250`, `paired_support_boundary_reachable: false`, and it ran anyway for 3,644 GPU-seconds.*

**FC-4 — Falsifiability assertion (the mirror of FC-3).**
State the outcome that would falsify the hypothesis, and confirm **it too** is attainable under FC-2. An experiment with one reachable outcome is not an experiment. Both branches must be inside `[lo, hi]`.

**FC-5 — Two controls, run before the real run.**
Publish one input that **must fail** the gate (firing control) and one that **must pass** (null control). Run both and record the outcomes. **A gate never observed to reject anything is not a gate.** *Wave-1 N-02: `premises_passed=True` as a literal, `grep premises_passed=False` over 20,705 test lines → 0 hits. Wave-1 N-07: `defect_is_psd` PSD by construction, 3000 draws never negative, asserted as a theorem check. Wave-2 W5: `minimum_diagonal = Fraction(1,10**100)`, so the test asserts `1/10^100 > 0`; `inside_declared_domain` and `assumptions_satisfied` boolean literals at all four call sites.*

**FC-6 — Tautology sweep.**
Enumerate every conjunct of the gate and mark each: computed / literal / by-construction. **Delete or replace every non-computed conjunct.** *Wave-1 RG-2: `direct_channel.matrix` compared to `_matmul(first.matrix, second.matrix)` where `direct_channel` **is** `first.compose(second)` and `compose` **is** `_matmul` — the same expression on both sides, coordinator-verified. Wave-1 RG-3: three "residual forms" that are the same polynomial for all inputs, with an `ArithmeticError` that can never fire.* **For this roadmap, FC-6 rejects E2 arm 1 and E4 arm 1 on sight.**

**FC-7 — Resolution floor, measured not declared.**
State the smallest effect the instrument resolves at the declared tolerance **and conditioning**, by measurement. Assert `|threshold − null| > floor`. *Wave-2 F-1: declared `max_frame_condition = 1e6`, measured safe ≈ `3e3` (300× lower); declared `min_spd_rcond = 1e-12`, measured safe ≈ `1e-7` (five orders higher); residuals at 843× and 33,500× the grading tolerance with all gates green.*

**FC-8 — Every soft verb gets a number.**
Every "match", "agree", "converge", "reproduce", "survive", "remain", "follow", "close" in the gate gets a tolerance and a norm. For convergence: expected rate, refinement count, and the acceptance band on the **observed** order. **In this roadmap that is E0, E1, E2, E3, E4, E5, E6, E7, WP1, WP2, WP3, WP4, WP6 — thirteen of fifteen gates.**

**FC-9 — Analysis plan, frozen and hashed.**
Primary endpoint; number of comparisons; multiplicity correction **by name**; CI level and sidedness; decision rule; seed budget from a power calculation. Hash it. *Wave-2 W5: `confirmatory_analysis.py` scored **5/15** on mutation — Holm→Bonferroni, a reversed sign-test tail, `95%→90%` CI, a dropped half-width `/2`, and a dropped two-sided factor of 2 **all survived**. "You could silently swap Holm for Bonferroni, halve the confidence interval, or reverse a test tail, and no test would notice."*

**FC-10 — Seeds consumed, not decorated.**
Assert the seed reaches a generator that affects output. *Wave-1 N-01: `RngStreams.from_seed(config.run.seed)` is called in **12** experiment modules and consumed in exactly **one** (`gaussian/experiment.py:415`); elsewhere the seed is hashed into config identity, the run-directory name, and RNG provenance with **zero effect on output**. `fixed_ray_experiment.py:2758` hard-codes master seeds, so the 40-job study is a single deterministic point that cannot be re-drawn.*

**Adoption cost:** FC-1..FC-4 and FC-6 are arithmetic — the ten lines that would have caught T-04. FC-5 and FC-10 are one test each. FC-7..FC-9 are writing. Total: under a day for the whole checklist, against 3,644 GPU-seconds for the single episode it prevents.

---

# JOB 3 — PROCESS PROPORTIONALITY

**The pattern to beat** (wave-1 S2, coordinator-verified): `git diff --stat aedc662..HEAD -- src tests tools Theory` → **empty**. Zero of 22 findings fixed. ~29,043 lines of remediation plans, ≈1,053 lines of plan per unfixed finding; Wave E is 4,196 lines to correct **one sentence**. Verification apparatus 28,213 lines against 16,821 lines of theory. Wave-1 T-05: the prior peer review produced 18 findings, 3 adjudicated, **0 fixed**.

**What this roadmap breaks — and it is real:**

1. **It is 175 lines.** Against a 29,043-line baseline that is a factor-of-166 reduction. This is the first artifact in the sequence that is shorter than the thing it discusses.
2. **WP0 is 2–4 pages and its gate is mechanically decidable.** That is the single best item in the document: small, cheap, checkable, and it has known failing input (wave-2's 15 notation drifts) so it will fire on day one. If nothing else in this roadmap happens, WP0 should.
3. **It sequences, and it fences.** Line 168 names three artifacts "in order"; line 168 defers RG closure, scale-free fixed points, and broad phenomenology until they agree; line 140 refuses "physics from cognition" as evidence. Line 170 pre-commits to informative failure. Wave 1 praised this project's scope-denial discipline as genuinely excellent, and this document sustains it.
4. **It does not overclaim novelty or completion.** Line 11 concedes "This is a class to be narrowed by axioms, not yet a completed theorem."

**What it repeats — and this is the larger part:**

1. **It does not sequence doing before planning. It sequences planning → writing → doing, with doing last.** Line 168: "First, complete WP0 as a two- to four-page ontology and action specification. Second, write the restricted T0–T4 theorem manuscript… Third, implement a small fiber-agnostic numerical oracle and run E0–E4." Two of the three artifacts are documents; code is third. Given a repository where **zero of 22 + zero of 18 findings are fixed** and the highest-value action available is *twelve seconds of CPU* (wave-1 S5: re-run `run_checks.py`, restore all thirteen `\status{NUMERICAL}` claims — deferred for three days while 23,367 lines of plans were written), producing two more documents before touching code is the same reflex in a smaller container.
2. **Zero commitment to fixing existing defects. Measured:** `grep -c -i` over the roadmap → `"AUD-"` **0**, `"T-04"` **0**, `"remediation"` **0**, `"audit"` **1** (E5's own title). No mention of the 22 AUD findings, the 18 prior review findings, T-04, the evidence artifact that binds to nothing in **both** repository copies, the read-only-`Theory/` root cause that makes fixes *structurally impossible*, the uncited Dennis 2025 preprint (a fifteen-minute fix with asymmetric downside), or wave-2's four proof gaps at `05c:124`, `04:408`, `05b:547`, `07:263`. **WP1 proposes a new manuscript and WP3 proposes a new implementation on top of a corpus with 40 known unfixed defects.**
3. **WP3 is a rewrite that would inherit three known structural test blind spots.** Wave-2 W5 identified them with one-line fixes: all four permutations in `gauge_fixture` are **involutions** (`old_to_new == new_to_old`), so gauge *direction* is undetectable by construction; `adjacent_pairs` is **doubly stochastic**, so every finite difference is exactly orthogonal to the Perron ray and `‖(I−P)d‖ == ‖(I−6P)d‖`; the Hoeffding fixture is symmetric about zero, so the quotient seminorm is indistinguishable from the sup-norm. Fix the fixtures before writing the backend, or the new backend gets the old blindness.
4. **The roadmap adds 25 new obligations** (10 theorem targets, 8 experiments, 7 work-package gates) to a project that has not discharged its existing ones. WP6's six ablation axes — family, group, seed, size, mesh, structural — is a combinatorial expansion of exactly the apparatus wave 1 measured at 28,213 lines. The roadmap's obligations are *specifications* rather than *verification code*, which is a meaningful difference and I credit it; but the direction of travel is still net-more-apparatus.
5. **The experiment table reproduces the T-04 defect class in a new form.** T-04 was a threshold frozen without a reachability check. E0–E7 freeze **no thresholds at all** — zero occurrences of "tolerance", "threshold", "effect size", "power", "p-value", "confidence", "reachable", "feasibility" in 175 lines. That is not an improvement on T-04; it is the same failure moved one step earlier, from *an unreachable criterion* to *no criterion*. And E2 arm 1 and E4 arm 1 are gates the source's own counterexample register **proves** cannot fail — a defect the register would have caught if the roadmap had been checked against it in the direction I checked it here.

**Blunt verdict.** The roadmap breaks the pattern in **form** and repeats it in **substance**. The form matters — 175 lines with a decidable first gate is a real change from 29,043 lines with none, and the author should be told that the shift is visible. But this is the fourth planning artifact produced before the first defect is fixed, and the honest test is arithmetic: **the roadmap proposes ~25 new obligations and discharges 0 of 40 existing ones.** No sequencing argument survives that ratio.

**What I would actually do with the next cycle**, in order, with the roadmap intact behind it:

0. Twelve seconds of CPU: re-run `run_checks.py`, rebind the evidence artifact. Thirteen NUMERICAL claims recover. (Wave-1 S5.)
1. Fifteen minutes: add Dennis 2025 + the four uncited self-citations to `references.bib`. (Wave-2, the finding that outranks everything else.)
2. Make `Theory/` writable, or move the ledger out of it. Until then **no finding in this project can ever be closed**, and every plan written against it is decorative. (Wave-1 S2 root cause; wave-1 T-08.)
3. Fix the four proof gaps — `05c:124` (two lines, via the frame-free form), `04:408` (display the root identities; N3(a) depends on it), `05b:547` (the supplied `KL(β‖β*) − log Z` identity, verified to `8.9e-16`), `07:263` (specify `κ_ℓ = id`). Hours, not plans.
4. Fix the three test fixtures. Three fixtures recover most of the missing 21% mutation score.
5. **Then** WP0. It is genuinely the right next planning artifact — and it will land on a repository where the previous cycle's findings are closed, which is the thing this project has never once done.

Then repair the roadmap: the two scope sentences of §1.4, the provenance repairs of §1.5, and FC-8 applied to all thirteen soft gates.

---

## Appendix — searches run

| Purpose | Command | Result |
|---|---|---|
| `MAgent_Model-main` present? | `grep -rn "MAgent_Model-main"` over `MultiAgentELBO`, `ChatGPT--MultiAgentELBO`, `Research`, `outputs` | **0 hits** |
| MAgent code tree present? | `grep -rn -i "MAgent_Model\|MAgent Model\|MAgent code" --include=*.{md,tex,py,json,bib} -l`; `find … -maxdepth 3 -type d -iname "*agent*"` | 0 in code repos; `Research/` hits are the *model* name only. Only `*agent*` dirs are `.git/worktrees/*` |
| Grid base / volume weighting? | `grep -rn -i "volume-weighted\|volume_weight" src/ README.md`; `grep -rn -i "grid" src/multiagent_elbo/ -l` | 0 / 0; `grid` only in `figures.py`, `finite/experiment.py` (plotting) |
| README claim (A-4)? | `grep -n -i "engineer\|consensus\|population"` on both `README.md` (223 lines each) | **0 hits in both** |
| Verification ledger for the no-go? | `grep -rln "state_level_elbo_nogo\|state-level ELBO obstruction\|state-level no-go"` over `Research/docs`, `Research/manuscripts`, `Research/wiki`, `ChatGPT--MultiAgentELBO/docs` | 5 files: `PIFB2.tex`, `PIFB2.aux`, one wiki theme note, `final-report.md`, the roadmap. `Research/manuscripts/verified-ledger.md` is the **GL(K)** ledger (frontmatter `title: GL(K) Manuscript Verified Ledger`), no no-go entry |
| Frozen/reduced finding location | `grep -rni "frozen\|freez" ultradeep-wave2-2026-08-12/wave2-01-constructions.md`; `grep -rn "3.54085" docs/audits/` | **0** in wave2-01; the finding is wave 1 F3 at `2026-08-11-ultradeep-expert-audit.md:136` and `ultradeep-2026-08-11/audit-02-infogeometry.md:139-165` |
| Quantitative vocabulary in roadmap | `grep -c -i` for tolerance / threshold / "effect size" / power / p-value / confidence / reachab / feasib / significance / "sample size" | **0 each** |
| Prior-defect vocabulary in roadmap | `grep -c -i` for `AUD-` / `T-04` / remediation / audit | 0 / 0 / 0 / **1** (E5's title) |
| E2 arm-1 tautology | numpy float64, `K=4`, 5-edge cycle, coboundary `U_aU_b^{-1}` | `‖H−I‖_F = 3.5585e-14` at frame cond ≤ `1.7e3`; **`3.5600e-14`** with a `1e-9` singular value inserted (cond ≈ `1e9`) — unchanged. Arm 1 measures round-off and is blind to conditioning |

*No GPU or CUDA job was started at any point.*
