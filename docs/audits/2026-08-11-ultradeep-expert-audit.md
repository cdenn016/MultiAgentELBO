# Ultradeep multi-expert audit

Date: 2026-08-11
Code/theory baseline: `c101b8a` (working tree)
Audit-of-record predecessor: `docs/audits/2026-08-11-post-fixed-ray-deep-audit.md` (baseline `aedc662`)
Corpora audited: `MultiAgentELBO/` (src 24,684 LOC; tests 20,705 LOC; `Theory/` 17,534 lines TeX) and `Research/manuscripts/PIFB2.tex` (3,956 lines) plus the surrounding vault
Execution policy: CPU only. **No GPU or CUDA job was started.** All numerical re-derivation was done in an isolated Linux sandbox with float64/`Fraction`/`mpmath`.

Audit standard: the project goal as stated by the author — *a rigorous version of PIFB2.tex in which agents are local sections of associated bundles with statistical-manifold fibers over a noumenal principal G-bundle, evolving under a local and global variational free energy.*

## Method

Six independent expert reviews were run in parallel with non-overlapping scopes: (1) differential geometry / gauge structure, (2) information geometry and the ELBO, (3) renormalization and coarse-graining, (4) code correctness and numerics, (5) claim traceability and evidence integrity, (6) PIFB2-to-`Theory/` gap analysis. Each was instructed to re-derive rather than accept, to give file:line for every assertion, and to report what it checked and found *solid* as well as what it found broken.

Agent agreement was not treated as evidence. Every finding rated CRITICAL or HIGH below was re-verified by the coordinator directly against source; the verification log is at the end of this document and includes one case where the coordinator's check was **stronger** than the agent's claim and one where the agent's supporting detail did not reproduce.

Findings already recorded as AUD-01..AUD-22 in the predecessor audit are not restated. Their *status* is reported once, in Finding S2.

## Verdict

The mathematics that exists is substantially better than the surrounding apparatus suggests. Across four reviewers who independently re-derived roughly sixty identities symbolically or numerically, **zero algebraic errors were found** in the core chapters. The epistemic-status discipline is, on measurement, exemplary: 292 of 292 formal environments carry exactly one status tag, with no type mismatches and no citation-as-proof. Chapter 11's negative results are genuinely proved with verified counterexamples. The test suite caught all ten deliberate mathematical mutations injected into it.

The problems are not errors. They are four structural facts, and they are severe:

1. **The central object of the stated goal does not exist.** The variational free energy is never a functional of a section. It is `\Fenergy[Q_X; X, o]` — a functional of a recognition kernel over a *finite design* of context points. There are zero integrals over the base manifold anywhere in the corpus. The bundle layer and the variational layer are separated by a type wall that the manuscript itself proves cannot be closed by the one hypothesis offered to close it.
2. **The gauge sector is inert.** Curvature is never defined. Connections never enter the free energy. Chapter 2's bundle-theoretic results have no cross-file consumers. The gauge language is currently organizational rather than load-bearing.
3. **Zero of 22 prior audit findings were fixed.** The complete diff from the predecessor audit's baseline to HEAD is nine files, 23,367 insertions, all documentation. Not one source line changed. Meanwhile 29,043 lines of remediation *plans* were written for defects that remain live.
4. **The numerical evidence artifact binds to nothing.** Every file it claims to certify has changed since it was written, in both repository copies. All thirteen `\status{NUMERICAL}` claims are, by the project's own freshness policy, currently unbacked.

The honest summary is that this is a strong mathematical manuscript with a weak connection to its stated goal, wrapped in a verification apparatus larger than the science it protects and currently detached from it.

---

## S — Structural findings

### S1 — CRITICAL — The VFE is not a functional of a section

The goal sentence requires a free energy evaluated on local sections of an associated bundle. What exists is two layers that do not meet.

- Geometry layer: `Theory/02_geometry.tex:403` `def:geo-agent` types an agent as `q_i \in \Gamma(\mathcal C_i, \mathcal E_b|_{\mathcal C_i})`. This is static and carries no free energy.
- Variational layer: `Theory/03_probability.tex:15` fixes a **finite design** `D = {c_a} \subseteq \mathcal C`; `Theory/05_elbo.tex:222` defines `\Fenergy[Q_X; X, o] = -\Lelbo(Q_X; X)` over one joint kernel.
- `Theory/05b_local_collective_elbo.tex:18` drops the manifold entirely: "Let `(\mathsf X, \mathcal X)` be a standard Borel context space, let `V` be an arbitrary finite set of agents." At `05b:782`: "'agent' is not determined by the principal bundle."

The only offered bridge is `hyp:prob-sampling-compatibility` (`03_probability.tex:436`), a HYPOTHESIS — and `prop:prob-compatibility-nonidentifiability` (`03_probability.tex:420`, ESTABLISHED) **proves it determines neither side**. The manuscript has proved that its own bridge does not carry load.

Coordinator verification: `grep -F 'int_{\mathcal C}'` and `grep -F 'int_{\mathcal{C}}'` over all 24 TeX files return **zero hits**. There is no free-energy integral over the base manifold in the corpus. The only functional notation is `\Fenergy[Q_X;X,o]` at `05_elbo.tex:222,404,436`.

Consequence: "local and global variational free energy" is currently realized as *per-agent versus per-block over a finite agent set*, not as *local-in-`\mathcal C` versus global-over-`\mathcal C`*. No sheaf-theoretic or partition-of-unity gluing result exists. This is the single gap that most determines whether the project reaches its stated goal.

Fix: define `\Fenergy` on sections and prove (a) well-definedness independent of local trivialization, (b) invariance under `\mathrm{Aut}_G(P)`, (c) consistency with `\Fenergy[Q_X]` on the finite design. Do it first on the tier already exhibited at `05d:235` (`P = \mathcal C_\ell \times G`, `G = (\mathbb R^K,+)`, flat `\omega`, constant Gram metric), where every ingredient is already in hand. This is the one genuinely hard piece of mathematics remaining, and everything else in the program is downstream of it.

### S2 — CRITICAL — Zero of 22 prior findings fixed; remediation effort is going into documents

`git diff --stat aedc662..HEAD -- src tests tools Theory` returns **empty**. Coordinator-verified. The three commits since the predecessor audit are `docs:` only.

Two reviewers independently re-executed probes for the known findings and reproduced the predecessor's exact numbers — including AUD-03 yielding `kl_divergence = -0.17851484105136778`, digit-for-digit identical to the figure in the prior report. All eight and thirteen findings respectively that were spot-checked are still present. AUD-20's flagged sentence is verbatim intact in the Research manuscript.

Against that, `docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-*.md` totals roughly 29,043 lines — about 1,053 lines of plan per unfixed finding. Wave E is 4,196 lines to correct one sentence. AUD-03, AUD-13, AUD-15, AUD-17 and AUD-18 are together a few hours of source edits; Wave A's plan for them is 3,078 lines.

There is also an architectural cause, not only a discipline one: `Theory/` is a declared read-only snapshot, so the repository is **structurally incapable of fixing any theory-side finding**. The claim-to-evidence loop cannot close by construction.

Fix: stop planning and edit source. Make `Theory/` writable, or relocate the obligation ledger to a writable location so evidence can propagate into it.

### S3 — HIGH — The gauge sector is inert: no curvature, no connection in the free energy, no downstream consumers

Coordinator verification: `curvature` appears **8 times across 17,534 lines** (`02:1, 05:1, 05d:1, 07b:1, 11:2, 12:2`), and the `02` occurrence is a `NOT-CLAIMED` disclaimer. There is **no** `F_\omega`, no `d\omega`, no `[\omega,\omega]`, no Ambrose–Singer anywhere in the corpus. `appendix_notation.tex` has no curvature entry.

The connection forms `\omega_b/\omega_m` appear **zero times** in `04_generative.tex`, `05_elbo.tex`, and `05b_local_collective_elbo.tex` — that is, nowhere in the generative model or in either free energy. Yet `05c:184-232` *proves* that the emergent pullback metric `h_s^\omega` depends on the connection exactly, with a counterexample at `05c:220-232`. So the geometry the theory produces is a function of exogenous data that no variational principle selects.

Label reference counts confirm the isolation: `eq:geo-cech-class` 1, `sec:geo-cech` 1, `def:geo-connections` 1, `hyp:geo-graph-base-transport` 1, `def:geo-agent` 1 — **all self-file only**. Because `hyp:geo-graph-base-transport` (`02:625-640`) is never invoked downstream, every holonomy result in chapters 6, 9, 11 and 7b is finite-graph linear algebra with no bundle content.

Fix: add curvature to chapter 2 (`F = d\omega + \tfrac12[\omega,\omega]`, Ambrose–Singer, flat iff path-independent), then either make `\omega` dynamical inside the VFE, or promote "`\omega` is exogenous and `h_s^\omega` is therefore not an observable" to an explicit ledger OPEN. The second is cheap and honest; the first is what would make the gauge language earn its place.

### S4 — HIGH — The interaction form is chosen and checked, never derived from covariance

This is the scientific gap that decides whether the framework is a gauge theory or a gauge-decorated model.

- `05b:66`: covariance "is imposed by requiring…" — a DEFINITION.
- `04_generative.tex:379` `hyp:gen-kernel-covariance` — a HYPOTHESIS.
- `06_gaussian.tex:297`: "The document does not claim that it is forced by anything."
- `07b:1257` explicitly disclaims uniqueness.

There is no classification theorem showing that gauge covariance *constrains* the admissible coupling family. Without one, "gauge-covariant" is a property the model was built to have, not a principle that generates it. The manuscript is admirably honest about this, but honesty about a gap does not close it.

Fix: prove a classification — under the declared equivariance and locality requirements, the admissible pairwise couplings form family X, of which the sandwich/transport form is the unique (or a characterized) member. Even a restricted classification on the Gaussian tier would be a genuine result.

### S5 — HIGH — The numerical evidence artifact certifies nothing current

Coordinator verification, run directly:

```
inventory_manifest.source_root = "manuscripts/gauge_vfe_rg"
MultiAgentELBO/Theory              tex: MATCH=1  MISMATCH=23  MISSING=0
Research/manuscripts/gauge_vfe_rg  tex: MATCH=1  MISMATCH=23  MISSING=0
protocol files (claims.json, run_checks.py, requirements.txt, VERIFICATION.md):
                                   MISMATCH in BOTH copies, 4/4
```

This is stronger than the reviewing agent's claim: the artifact fails to bind in **both** repository copies, and every protocol file has drifted too. By the project's own declared freshness policy, all thirteen `\status{NUMERICAL}` claims are unbacked as of this baseline. `06_gaussian.tex:294` nonetheless still says "its **current output** corroborates."

Two further defects in the same artifact: 26 of 35 claim_ids it references do not exist in `claims.json` (74% dangling), and `CHK-CG-FACTOR-GAP-STRESS-3138` is absent entirely.

Fix: re-run `run_checks.py`. This is roughly twelve seconds of CPU and restores all thirteen claims. Then bind the artifact to one canonical source root and make regeneration a precondition of any tagged NUMERICAL claim.

### S6 — HIGH — The apparatus cannot be run by anyone, and guards a repository that is not present

`Theory/verification` is 17,857 LOC (`run_checks.py` 10,443; `build_audit.py` 5,473; `lifecycle_gate.py` 1,941) against 16,484 LOC of science and a 24-file manuscript. `manifest-policy.json` and `lifecycle_gate.py` require paths under `manuscripts/gauge_vfe_rg/**` and `docs/derivations/2026-08-03-*` that do not exist in this repository, and nothing invokes them. `run_checks.py:324` hard-codes `C:\Python314\python.exe` and `:44` hard-codes a specific user's site-packages; the script refuses to run under any other interpreter. **No independent party can execute a single check.**

Separately, 31 cited evidence paths are absent because they live under the gitignored `.verification/` tree — including `ledger.json`, which the predecessor audit names as its own closure authority, and the 957-test JUnit record. A hash of an unobtainable file cannot fail, and therefore carries no information.

Fix: delete or externalize the inert machinery; de-hardcode the interpreter; either track the evidence or stop citing it.

---

## D — Domain findings

Severity in brackets. Type: ERR = outright error, GAP = missing derivation, HW = hand-wave / weak rigor, VAC = true-by-construction / vacuous, OVR = overclaim.

### Geometry and gauge structure

| # | Sev | Type | Finding | Location |
|---|---|---|---|---|
| G3 | MED | GAP | "Choose an open support `C_i` and sections `u_i^b: C_i \to P`" — a section exists only if `P\|_{C_i}` is trivializable, and the syntax admits `C_i = C`. Counterexample: `C = S^2`, Hopf bundle, one agent with `C_1 = C`. | `02_geometry.tex:46-53` |
| G4 | MED | GAP | No characteristic class, Chern class, contractibility, or partition-of-unity anywhere. A cheap and valuable missing result: `B_b \cong \mathbb R^K \times \mathrm{SPD}(K)` is contractible, hence **global agent sections always exist in the Gaussian realization** regardless of `P`'s topology. Topology obstructs frames, never agents. | corpus-wide |
| G5 | MED | HW | 17 untagged prose blocks in ch.2. Worst: `02:135-137`, the smooth-associated-bundle claim on which all of `05c` rests — untagged and unproved. Also `02:301-306` constructs `\Omega_\gamma` without checking independence from the chosen point of `P_{\gamma(0)}`. | `02_geometry.tex` |
| G6 | MED | — | No module anywhere implements `\mathcal C`, `P`, `\omega`, a section, `D^\omega s`, or `h_s^\omega`. `discrete_holonomy.py:149-156` hard-codes `GL^+(2,\mathbb R)` with no dimension parameter; `finite_gauge.py` is permutation relabeling. Chapters 2 and 5c have zero computational witness. | `geometry/*.py` |
| G7 | MED | HW | `B_x \subseteq P(K)` is declared a *subset* (`02:69-74`) then given tangent spaces `T_p B_x` (`05c:52-57`). A parametrized model's image is a manifold only under injectivity plus immersion; never assumed. | `02`, `05c` |
| G8 | LOW-MED | HW | `H_I^x: \pi_1(\Gamma_I, r_I) \to G` asserted a "representation", tagged ESTABLISHED, with no descent proof and no homomorphism convention — under ch.2's ordering it is naturally an *anti*-homomorphism. | `07b:1648-1653` |
| G9 | LOW | ERR | `{U : \mathrm{cond}(U) \le \kappa}` is admitted as if a group; it is not closed under multiplication. | `gaussian/gauge.py:36-52` |

### Information geometry and the ELBO

| # | Sev | Type | Finding | Location |
|---|---|---|---|---|
| F1 | HIGH | GAP | Seven PIFB2 Level-2 results have no rigorous counterpart **and no ledger entry**: the state-level ELBO no-go, transformer recovery, the `-\tau\log Z` envelope reduction, Brouwer equilibrium, the Gibbs configuration lift, the mass/reduced-Hessian section, and the timescale hierarchy. Grep over `Theory/*.tex` returns nothing for Brouwer, mass matrix, second variation, adiabatic, reduced free energy, transformer, or dot-product. | corpus-wide |
| F3 | MED | OVR **+ constructive** | The obstruction is proved only at **frozen** `\beta`, yet the abstract states it adjacent to the claim that the implementation differentiates the *reduced* scalar, to which the theorem does not apply. The reviewer then **ran the missing test** (mpmath, 60 dps, 2 agents, n=3, `\tau=0.8`): reduced potential `D^3 = -3.54085893855\mathrm{e}{-5}` versus fixed-joint control `-3.63\mathrm{e}{-65}` (exact zero). The stronger claim appears **provable, not merely open**. | `PIFB2.tex:3279-3330`; `05b` |
| F4 | MED | VAC | `thm:obs-collective-vfe` and `thm:obs-local-multiagent-elbo` are boxed `:=` definitions tagged ESTABLISHED, whose proofs consist of applying KL `\ge 0` to a quantity just defined. Split into definition plus one-line proposition. | `05b:153`, `05b:294` |
| F5 | MED | HW | The local–global potential identity holds for correlated `Q`; the descent corollary silently narrows to *product* families without flagging it. Block-diagonal Fisher is stated as a hypothesis but is automatic for product families. "Local" equivocates — the flow is graph-local only under the `P_0`-conditional condition at `05b:63-65`, never re-invoked. | `05b:670-708` |
| F6 | MED | — | `prop:hist-semidefinite-gradient-obstruction` demands a justified quotient or declared regularization before any pseudoinverse. `information_history.py:138-143` applies `np.linalg.pinv` unconditionally, computes `range_residual` — the exact solvability test — *afterwards*, and never gates on it. | `05d:560`; `information_history.py` |
| F10 | MED | GAP | `05b` never states `F_i^{\mathrm{att}}(\beta^*) = -\log Z_i`, the bridge on which PIFB2's entire envelope argument rests. | `05b` |
| F2 | MED | HW | "All differentiated integrals below are assumed finite" discharges three differentiations under the integral plus two unstated hypotheses — against a repo that elsewhere writes explicit chartwise `L^1` dominating functions (`05d:400-425`). | `PIFB2.tex:3279` |
| F7 | LOW-MED | — | `categorical.py:44-68` accepts non-minimal sufficient statistics; `hyp:exp-regular-minimal` is unenforced, and the resulting singular Fisher flows into F6. | `categorical.py` |

### Renormalization and coarse-graining

| # | Sev | Type | Finding | Location |
|---|---|---|---|---|
| RG-1 | HIGH | OVR/VAC | `eq:rg-kernel-semigroup` is *declared*, never instantiated for any `(C_b, I_b)` pair, and `thm:rg-complete-effective-theory` then **assumes it as a hypothesis**. The one proved semigroup is congruence associativity — true for every `S`, holding before rescaling and before any identification makes it an endomorphism. There is a rigorous scale *cocycle*; there is no verified renormalization *semigroup*. | `07b:2130`, `07b:2751` |
| RG-2 | HIGH | VAC | The lab's headline cocycle metric is identically zero by construction. `scale_cocycle_experiment.py:202` sets `fine_to_macro = fine_to_middle.compose(middle_to_macro)`; `scale_cocycle.py:159-163` defines `compose` as `_matmul`; line 366 then compares `direct_channel.matrix` to `_matmul(first.matrix, second.matrix)`. **Coordinator-verified: the same expression on both sides.** It tests nothing, and it is not the RG semigroup in any case. | `finite/scale_cocycle*.py` |
| RG-3 | MED-HIGH | VAC | `retained_beta_diagnostics` computes three "residual forms" that are the same polynomial for all inputs; its `ArithmeticError` can never fire. This is a **second instance of AUD-17**, which is itself unremediated — `base_fisher_cocycle_residual_forms` still accepts a nonsymmetric indefinite "Fisher defect" and returns three equal values. | `scale_cocycle.py:377-395` |
| RG-4 | MED | OVR | "This is the promised inhabited relevance spectrum" — but the model is i.i.d. scalar Gaussians: no agents, no interactions, no gauge, inside a chapter titled *Exact Renormalization of Agent Networks*. No mode of `DT_\ell^{\mathcal G}` is classified anywhere. | `07b:961` |
| RG-6 | MED-HIGH | VAC | `thm:rg-complete-effective-theory` takes ~16 supplied hypotheses and argues "each operation is closed in the stated collection, so their finite composition is closed." True by construction; "complete" and "exact" are unearned. | `07b:2751` |
| RG-7 | MED | ERR | **PIFB2 internal contradiction.** `prop:barycenter_existence` asserts gauge-equivariance citing a theorem that **assumes `G` compact**, while the actual group `GL^+(K_q)` is noncompact. PIFB2:1575 then *proves* no equivariant permutation-symmetric frame map exists and that the implemented additive form "is not gauge-equivariant at all" — yet 1644, 1804 and the section title still assert covariance. | `PIFB2.tex:1559,1575,1644,1804` |
| RG-8 | MED | ERR | Sign inconsistency within one chapter: `e^{-\bar E}` at `06:320` versus `e^{+\mathcal E}` at `06:392` for the coarse normalizer. | `06_general_coarsegraining.tex` |
| RG-5 | MED | VAC | `thm:rg-fixed-point-equations` is labelled "Exhaustive"; its proof opens "is the definition of invariance." | `07b` |
| RG-15 | MED | — | PIFB2's apex closure `p_i^{(\mathrm{top})} = \sum \bar w_j \Omega[q_j]` is a prior constituted by posteriors — untyped against the generative/recognition prohibition `Theory/` enforces. `eq:ouroboros_F` has augmented-joint backing only for `k=1`. | `PIFB2.tex` |

### Code and numerics (new findings only; AUD-01..22 status is S2)

| # | Sev | Type | Finding | Location |
|---|---|---|---|---|
| N-01 | HIGH | provenance | `RngStreams.from_seed(config.run.seed)` is called in 12 experiment modules; **exactly one** consumes a generator (`gaussian/experiment.py:415`). Elsewhere the seed is hashed into config identity, the run-directory name, and RNG provenance, with **zero effect on output**. Worse, `fixed_ray_experiment.py:2758-2762` hard-codes master seeds, so the 40-job confirmatory study ignores `run.seed` entirely and is a single deterministic point that cannot be re-drawn. | corpus-wide |
| N-02 | HIGH | VAC | `premises_passed=True` and `gpu_gate_complete=True` are passed as **literals** at the only production call site, and both are load-bearing conjuncts of `support` and `forced_inconclusive`, published as `"premises_passed": true`. **Coordinator-verified:** `grep premises_passed=False` across 20,705 test lines returns **zero hits**. Directly contradicted by `fixed_ray_diagnostics.py:265`, which records `"actual_run_premises_validated": False`. | `fixed_ray_experiment.py:2503`; `confirmatory_analysis.py:488-510` |
| N-03 | HIGH | numerical | The CUDA-repeatability lane runs the same kernel twice with deterministic algorithms on, so it must be bit-identical — but is graded at `rtol = 1.67e-10`. Injected drift of `1e-11` and `1e-10` both pass. The determinism check cannot detect a determinism failure. *(Reported from code reading; no GPU was run.)* | `parity_diagnostics` |
| N-09 | MED | method | The `-0.02` endpoint regresses the **raw** angle, which decays geometrically. Observed OLS slopes span `-0.0057 .. -0.000086` across all 60 (job, scheme) pairs — unreachable by construction. On `\log\theta` the same data gives `-0.916284..-0.916245`, i.e. `\log 0.4` to `4\mathrm{e}{-5}`. The failure is a linear-versus-log scale error in the endpoint definition. | `fixed_ray` |
| N-10 | MED | theater | Both frozen "spatial maps" are row-stochastic (`\lambda_1 = 1`, `\vert\lambda_2\vert = 0.4` and `0.2`), and `iterate_fixed_ray` is `c \leftarrow Ac` with no normalization. Convergence to the Perron ray is textbook Perron–Frobenius, independent of the VFE, gauge, or RG theory. The gate/sentinel/holdout/bootstrap/Holm apparatus sits on top of `A^n c` for a fixed 6×6 stochastic matrix. | `fixed_ray` |
| N-05 | MED | provenance | `canonical_config_json` **drops the entire `compute` section** from the hash when COMPUTE is absent; 7 of 12 launchers omit it, so backend, dtype, batch size and worker interpreter fall outside config identity. | `config.py:622-624` |
| N-06 | MED | — | `float32`, `bfloat16`, `allow_tf32` and `device_index>0` are parser-legal, cross-validated, hashed, and unexecutable. Extends AUD-07 by two more ignored fields. | `config.py`, `cuda_backend.py` |
| N-07 | MED | VAC | `FisherChannelResult.defect_is_psd` is PSD by construction (a sum of nonnegatively weighted Grams); 3000 random draws never produced a negative eigenvalue. It is asserted in `test_fisher.py:153` as though it were a theorem check. | `fisher.py` |
| N-08 | MED | ERR | `all_parity_passed` and `scientific_decision_parity_passed` are the same variable, then checked as two independent conditions. | `fixed_ray_experiment.py:1947,2355` |

### Traceability and evidence

| # | Sev | Type | Finding | Location |
|---|---|---|---|---|
| T-04 | CRITICAL | — | **The flagship experiment could not have confirmed.** The preregistration froze a support threshold of `-0.02` rad/scale; the later exact certificate proves `rational_slope_lower_bound = -9/625 = -0.01439` and `paired_support_boundary_reachable: false`, margin `7/1250`. The criterion was mathematically unreachable from the moment it was frozen, yet 40 jobs and 3,644 GPU-seconds were spent. No gate caught it; ten lines of rational arithmetic would have. It targets `conj:grg-fixed-b-attraction`, the manuscript's only substantive conjecture. | preregistration vs certificate |
| T-05 | HIGH | — | The prior ultradeep peer review produced 18 findings; 3 adjudicated, **0 fixed**. All 8 philosophy findings verified verbatim present. Ten of eleven declared review lenses never reported. | `docs/reviews/2026-08-09-*` |
| T-07 | HIGH | — | **174 of 501 ESTABLISHED tags** sit on prose with no proof, no citation, and no `\Cref`/`\eqref` pointer. Concentrated in `09_coarsegraining` (26), `07b` (22), and — most damning — `12_philosophy.tex`, whose first line reads "This chapter proves no mathematical result." | corpus-wide |
| T-08 | HIGH | — | The ledger omits two structural-realism OPENs (`12_philosophy.tex:196,210`) and **cannot absorb evidence**: the fixed-ray certificate bears directly on its *Scalarized attraction* entry and cannot propagate, because `Theory/` is read-only. | `appendix_claim_ledger.tex` |
| T-09 | MED | — | 291 of 876 substantial paragraphs untagged (33%), including 19 untagged **normative scope rulings** (e.g. `11_obstructions.tex:4,332`) against a contract requiring a tag on every nontrivial statement. | corpus-wide |
| T-11 | MED | — | `theory_oracles.py` is genuinely implementation-independent (stdlib `Fraction`, imports nothing from the package) but **assumption-identical**: it can indict an encoding, never the theory. The project states this itself, correctly. | `theory_oracles.py` |

### Literature positioning

Citation density is **101 cite commands per 96,957 words ≈ 1.4 per thousand**. `01_introduction.tex` has **zero citations** — on its own a desk-reject risk. `05c` is 68 KB with 2 citations; `07b` is 136 KB with 6; `05b` is 35 KB with 1.

Present in `references.bib` and cited **zero times** in `Theory/`: Friston (15 entries), Parr, Da Costa, Ramstead, Sakthivadivel, **Sengupta–Friston neuronal gauge theory** (which PIFB2 itself calls "the closest direct precursor"), Cohen & Welling, **Weiler coordinate-independent CNNs** (the closest existing work to chapter 2), Bronstein, Bény–Osborne, Vaswani, Lahav–Neemeh.

Absent from bib and vault entirely: **Fritz / Markov categories** — yet `06_general_coarsegraining.tex:28` proves `prop:cg-markov-category` and the typed coarse-operation separation is a Markov-category argument, rederived without citation. Also absent: Bauer–Bruveris–Michor; Villani / Ambrosio / JKO (a referee will ask why Fisher–Rao and not Wasserstein); Bethe/Kikuchi region-graph free energies, which `eq:obs-global-ledger` closely resembles.

Genuinely novel, and worth foregrounding: (a) covariant informational pullbacks with the horizontal-defect cocycle (`05c:979,1230,1267`) — pulling Fisher and Amari–Chentsov to a base through section plus connection does not appear in the literature; (b) `thm:obs-local-global-potential` for *correlated* recognition laws; (c) the obstruction chapter, especially `prop:obs-declared-root-unavoidable`, which is a rigorous no-go against PIFB2's own Ouroboros apex closure.

Already standard and should not be claimed: associated bundles; fields-of-fibers-with-transport is Cohen 2019 / Weiler 2021 exactly (the vault knows this — `Research/wiki/themes/Gauge equivariance and geometric deep learning.md` — and neither manuscript cites it); the Markov-kernel category; Fisher contraction under coarse-graining is Bény–Osborne; the forward-KL Gaussian barycenter is moment matching.

---

## What is genuinely solid

This should not be lost in the list above. Reviewers were instructed to report it explicitly, and it is substantial.

**Mathematical correctness.** Roughly sixty identities were independently re-derived across four reviewers; **no algebraic error was found in the core chapters**. Verified in full: the Hermite spectrum `b^{1-k/2}` (exact sympy integration, `b \in \{2,3,5,7\}`, `k = 1..8`, all 32 cases, plus Monte Carlo at `N = 4\times10^6`) with a relevant/marginal/irrelevant classification matching the standard block-spin Gaussian fixed point; Hoeffding sharpness `(4p-1)^n - (2p-1)^n`; the chapter-8 Gaussian information geometry end to end (mean block `9.1e-13`, Schur quotient `9.2e-13`, spectrum matching `1 + \mu'\Lambda\mu`); the `05b` local–global potential identity at `4.44e-16` on correlated `P_0`; PIFB2's envelope reduction (`\min_\beta L = -0.10738678690` versus `-\tau\log Z = -0.10738678695`); the Gauss-equation `+1/4` sectional curvature; `eq:obs-holonomy-det` for general `K`.

**Chapter 11 is exemplary.** Every negative result is genuinely proved with counterexamples that were verified numerically, and scoping discipline is maintained throughout.

**Status-tag discipline.** 292 of 292 formal environments carry exactly one status. Zero untagged environments, zero type mismatches, zero adjacent tags, zero multi-status paragraphs across 847 tags. Zero citation-as-proof and zero circular chapter citations were found — the exact failure mode two reviewers were sent to find. Independent tag censuses by two reviewers agreed exactly (847 = 501/137/75/60/58/13/3).

**The test suite is strong.** Ten deliberate mathematical mutations were injected; **all ten were caught**: KL direction flip (4 tests fail), `free_energy` logZ sign (1), conditional covariance centring (5), softmax max-shift removal (1), covector gauge law (1), quotient sup-norm (1), the `2\arcsin` factor (18), `\beta` projection removal (17), Schur sign (13), `defect_is_psd \to True` (1). A tolerance grep across all tests for anything `\ge 1e-3` returns exactly one intentional boundary test.

**Engineering.** Cholesky and `solve` rather than `inv` in the Gaussian production path; `eigvalsh` only on symmetrized matrices; numerically stable softmax; `expm1`; exact `Fraction` lanes with canonical literal parsing. `rendering.py` is genuinely fail-closed. `artifacts.py` rejects symlinks, junctions, hardlinks, duplicate inodes and undeclared entries. **Zero `warnings.warn` and zero bare `except: pass` in `src`.**

**Specific structural repairs `Theory/` makes to PIFB2, which should be preserved and highlighted.** PIFB2 at `:208` uses `\Omega_{ij} = U_i U_j^{-1}` as *both* a Čech transition function *and* an inter-agent transport with `KL > 0` — incompatible uses. Chapter 2 types `T_{ij}` (Čech) apart from `\Theta_e` (graph link). This is the rewrite's single most valuable contribution. Likewise, Fisher/Amari–Chentsov descent to the associated bundle — the hard part of the associated-bundle construction — is *proved* at `05c:59-88`, not assumed, with the bimeasurable-action hypothesis correctly isolated as load-bearing. AUD-20's connectedness-implies-common-fixed-point fallacy does **not** appear in `Theory/`; `06_gaussian.tex:122` explicitly corrects it. No universality-from-one-exponent, no thermodynamic-limit smuggling, and no monotonicity-direction error was found anywhere, including the one place a sign error would have been fatal.

**Integrity.** `hypotheses.md` carries 16 of 17 explicit refutation thresholds and ships deliberately-wrong labelled negative controls. The endpoint-feasibility certificate publishes its own experiment's ill-posedness. Those are real.

---

## Shortest credible path

Ordered by value per unit of effort. Items 2, 3, 5, 6 and 7 are assembly and writing; only item 1 is hard mathematics.

1. **Define `\Fenergy` on sections** and prove well-definedness under change of trivialization, `\mathrm{Aut}_G(P)`-invariance, and consistency with `\Fenergy[Q_X]` on the finite design. Start on the tier at `05d:235` where every ingredient already exists. Without this the project does not reach its stated goal. *(Hard; the one real research risk.)*
2. **Prove the noumenal commitment as a theorem.** It is currently philosophy — `noumen` has 5 hits, all in `12_philosophy.tex`. Three statements are available: N1 (the base carries no intrinsic geometry) is already true and needs only stating; N2 (agent geometries are gauge-related) is already proved at `thm:pb-pullback-gauge-invariance`, `05c:124`; **N3(a), that isomorphic bundle-with-connection data yield identical observation-record laws**, is about two pages from `prop:gen-product-evidence-invariance` (`04_generative.tex:408`) plus `hyp:gen-kernel-covariance`. N3(a) is the highest value-to-cost ratio in this entire audit — it converts the project's central philosophical posit into a rigorous indistinguishability theorem.
3. **Re-run `run_checks.py`** and repair the artifact binding. Twelve seconds of CPU restores thirteen NUMERICAL claims (S5).
4. **Fix AUD-03/13/15/17/18 and N-01/N-02/RG-2/RG-3 in source.** Hours of editing. Stop writing remediation plans (S2).
5. **Local-to-global over `\mathcal C`** with an exact defect term, using a partition of unity; `eq:obs-global-ledger` (`05b:441`) is the template.
6. **Fix the citation problem.** Add Sengupta–Friston, Weiler, Cohen–Welling, Fritz, Bény–Osborne, Vaswani, and a Wasserstein-versus-Fisher–Rao paragraph. `01_introduction.tex` having zero citations is independently disqualifying at any venue.
7. **Reinstate the attention result.** `05b:547` `prop:obs-attention-elbo` already derives exact row softmax from a latent source label inside a fixed joint — strictly stronger than PIFB2's mean-field ansatz. `Vaswani2017` sits in the bib, cited zero times. One page buys the entire ML readership. (The WikiText-103 sweep is correctly excluded and should stay excluded; PIFB2's own fence F6 concedes two seeds at `K_q = 90`.)

**Demote or cut:** `07b_agent_network_rg.tex` (2,828 lines, 17% of the corpus, barely coupled to the bundle program) to a companion paper; the four Gaussian-realization chapters to one; `conj:grg-fixed-b-attraction` to a remark; `12_philosophy.tex` to three pages unless N3(a) lands. Retag `thm:rg-complete-effective-theory` honestly and rename "renormalization" to "scale cocycle" wherever no semigroup is verified.

---

## Coordinator verification log

Claims rated CRITICAL or HIGH were re-checked directly rather than accepted from the reviewing agent.

| Claim | Check run | Result |
|---|---|---|
| No source change since prior audit | `git diff --stat aedc662..HEAD -- src tests tools Theory` | Empty. **Confirmed.** |
| Evidence artifact does not bind | SHA-256 of all 24 TeX + 4 protocol files against `inventory_manifest`, in both repo copies | 23/24 TeX mismatch and 4/4 protocol mismatch **in both copies**. **Confirmed, and stronger than reported** — the agent checked only one copy. |
| Curvature absent | `grep -c curvature Theory/*.tex`; search for `F_\omega`, `d\omega`, `[\omega,\omega]`, Ambrose | 8 total occurrences, one of them a NOT-CLAIMED disclaimer; zero hits for the curvature objects. **Confirmed.** |
| VFE is not a functional of a section | `grep -F 'int_{\mathcal C}'` and `'int_{\mathcal{C}}'` across all TeX; `grep -n 'Fenergy\['` | Zero base-manifold integrals. Only `\Fenergy[Q_X;X,o]`. **Confirmed.** The agent's supporting detail ("11 hits in `05d`") did **not** reproduce; the conclusion holds on a stricter search than the one offered for it. |
| Cocycle residual is vacuous | Read `scale_cocycle_experiment.py:202,234,366` and `scale_cocycle.py:155-163` | `compose` returns `_matmul`; `direct_channel` *is* `first.compose(second)`; line 366 compares that to `_matmul(first, second)`. Identical expression on both sides. **Confirmed.** |
| `premises_passed` is a literal | `grep -rn premises_passed src/`; `grep -rn 'premises_passed=False' tests/ \| wc -l` | Literal `True` at `fixed_ray_experiment.py:2503`; **0** occurrences of `False` across 20,705 test lines. **Confirmed.** |

Reported-but-not-independently-verified: the injected-mutation results (N-03, and the ten-mutation test-suite result), the `mpmath` third-derivative computation in F3, and the Hermite spectrum re-derivation. These were executed by reviewing agents with their commands and outputs recorded in the per-domain reports; they were not re-run by the coordinator.

Per-domain reports: `audit-01-geometry.md`, `audit-02-infogeometry.md`, `audit-03-rg.md`, `audit-04-code.md`, `audit-05-traceability.md`, `audit-06-pifb2-gap.md`.
