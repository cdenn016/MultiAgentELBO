# Roadmap vs. two-wave audit — reconciliation

**Document under review:** `ChatGPT--MultiAgentELBO/docs/research-plans/2026-08-12-pifb2-continuum-roadmap.md` (174 lines, commit `24c02aa`)
**Standard:** `MultiAgentELBO/docs/audits/2026-08-11-ultradeep-expert-audit.md` (wave 1) and `.../2026-08-12-ultradeep-expert-audit-wave-2.md` (wave 2), plus `ultradeep-2026-08-11/*` and `ultradeep-wave2-2026-08-12/*`
**Execution policy:** CPU only. No GPU or CUDA job was started.

---

## 0. Repository state — confirmed, plus one divergence the brief did not anticipate

`git log --oneline` in both copies is identical through `24c02aa docs: add PIFB2 continuum research roadmap` on top of `c101b8a`. `diff -rq MultiAgentELBO/Theory ChatGPT--MultiAgentELBO/Theory` returns only `__pycache__` noise. Same repo, ChatGPT copy one commit ahead, as stated.

**The divergence that matters:** the audits are **untracked in the Desktop copy and absent from the ChatGPT copy.**

```
MultiAgentELBO/docs/audits/          -> 2026-08-11-post-fixed-ray-deep-audit.md (tracked)
                                        2026-08-11-ultradeep-expert-audit.md          (?? untracked)
                                        2026-08-12-ultradeep-expert-audit-wave-2.md   (?? untracked)
                                        ultradeep-2026-08-11/                          (?? untracked)
                                        ultradeep-wave2-2026-08-12/                    (?? untracked)
ChatGPT--MultiAgentELBO/docs/audits/ -> 2026-08-11-post-fixed-ray-deep-audit.md   ONLY
```

The roadmap was written in the ChatGPT copy, where **neither audit wave existed on disk**. Its declared basis (line 174) is `docs/derivations/2026-08-12-pifb2-elbo-program-decision/final-report.md`, which exists only in the ChatGPT copy and which never mentions A-NOGO, S1–S6, or `Theory/`. Most of what follows is therefore *non-collision through non-contact*, not disagreement. That changes the remedy: this is a merge problem before it is a science problem.

**S2 status, re-measured at the roadmap commit.** `git diff --stat aedc662..24c02aa -- src tests tools Theory` is **empty**. The roadmap commit adds 462 lines: 174 of plan and **288 of `docs/verification/build_pifb2_roadmap_ledger.py`** — a verification ledger for a plan. That script hard-codes `PIFB2 = Path(r"C:\Users\chris and christine\Desktop\Research\manuscripts\PIFB2.tex")` and `README = Path(r"C:\...\Desktop\MAgent_Model-main\README.md")` at `build_pifb2_roadmap_ledger.py:13-17`, reproducing wave-1 **S6** (`run_checks.py:324` hard-codes `C:\Python314\python.exe`) in a brand-new file, and binds to a source set containing **zero** references to `Theory/`. The Big Omission is mechanized, not merely rhetorical.

---

## 1. THE A-NOGO ADJUDICATION

### 1.1 The two theorems, precisely

`wave2-01-constructions.md:29-40` (Theorem A-NOGO) and its components:

- **A3.1 — equivariance, TRUE** (`wave2-01:238-241`): `F_mu[F.s ; F.pi, F.E] = F_mu[s ; pi, E]`. "*Immediate from (A2.1) and (A2.2) with `g_{alpha beta}` replaced by `k_alpha`.*" Verified to exactly `0.0` residual.
- **A3.2 — invariance at fixed background, FALSE** (`wave2-01:243-250`): witness `1.9606` vs `2.9274`.
- **A3.3 — orbit-space criterion** (`wave2-01:255-266`): invariant **iff** the fiberwise integrand descends to `B/G`.
- **A3.4 — constancy** (`wave2-01:268-278`): for a `G`-torsor fiber, `Aut_G(P)` acts simply transitively on sections, `B/G` is a point, so **every invariant functional on sections is constant.**
- **A3.5 — classification** (`wave2-01:280-294`): `G=(R^K,+)` on the Gaussian fiber leaves only the covariance field; `G=GL^+(K)`, `K>=2`, leaves only `r = (mu^T Sigma^{-1} mu)^{1/2}`, so every invariant has the form `int psi(c, r(s(c))) dmu`.

### 1.2 The roadmap's exact wording

**Line 114 (T2 row), verbatim:**

> `| T2: gauge covariance | One passive local gauge action applied to sections, likelihood data, comparison maps, and connections | Prove invariance of \(\mathcal S\), equivariance of its differential, and invariance of observables. Separate coordinate transitions, gauge fixing, and physical link fields. |`

**Kinematics, lines 56-64, verbatim:**

> "Agent \(i\) occupies a measurable or Lipschitz domain \(U_i\subseteq\mathcal C\) and carries sections
> $$ q_i,p_i\in\Gamma(E_q|_{U_i}), \qquad s_i,r_i\in\Gamma(E_s|_{U_i}), $$
> together with a support field \(\chi_i\), attention rows on nonempty overlap neighborhoods, and any declared connection or relational fields."

**Line 72:** "With simplex-valued attention fields \(\beta_i(c)\) and \(\gamma_i(c)\), overlap priors \(\pi^q,\pi^s\), information-geometric comparison maps \(L^q_{ij},L^s_{ij}\), and covariant derivatives supplied by a connection…"

### 1.3 Adjudication: T2 EVADES A-NOGO's O1 in substance, but its verb is wrong, and it evades by two independent routes it does not know it has

**Route 1 — the transformation is passive and simultaneous.** Line 114's hypothesis column is explicit: *"One passive local gauge action applied to **sections, likelihood data, comparison maps, and connections**."* This is the *simultaneous* transformation. Critically, the priors `p_i, r_i` are typed at line 59-61 as **sections of the same bundles** as `q_i, s_i` — not as fixed laws in a fixed chart. That is exactly the condition wave 2 identifies as load-bearing:

> `wave2-01:221-227`: "**The two ways A2 fails, and they are the same computation.** If `pi` is declared as a *fixed law* in one chart rather than as a section, then in frame `u_beta` it reads `N(-g_{alpha beta}(c), Sigma_0)` instead of `N(0,Sigma_0)`… this is precisely the failure that CHECK B4 exhibits numerically (discrepancy `192.94`…)."

So the roadmap has, by typing choice, put itself in the regime of **Proposition A3.1 (true)**, not A3.2 (false). It does **not** transform sections against a fixed background. **T2 as written does not collide with A-NOGO's constancy result.** This is the correct answer and the roadmap deserves credit for it — the typing at line 59-61 is precisely the thing wave 2 had to insist on.

**Route 2 — the fiber is not a torsor.** A3.4's hypothesis is `B` a `G`-torsor. Roadmap line 13: *"The structural theory is neither Gaussian nor intrinsically \(\mathrm{GL}(K)\)… The fundamental objects are a principal \(G\)-bundle over the base and associated bundles whose fibers are general statistical manifolds."* Line 68 requires only finite-dimensional regular statistical manifolds. Generic such `M_q` is **not** a `G`-torsor, so `M_q/G` is not a point and A3.3 yields a nontrivial invariant class. A-NOGO's O1 is a statement about the *exhibited tier* (`05d:235`), not about the roadmap's general class.

**But three things are wrong, and one is a live trap.**

1. **The verb.** "Prove invariance of \(\mathcal S\)" (line 114) is the exact phrasing wave 2 says must be abandoned: "*Requirement (b) should be restated as **equivariance** on the triple `(s,pi,E)` — which is true and provable — rather than invariance*" (`wave-2 headline:61`); "*The requirement as stated is not merely unfulfilled; it is unfulfillable*" (`wave2-01:296-303`). Read in the standard sense — a functional of sections, invariant under `Aut_G(P)` — line 114's conclusion is false whenever the fiber is a torsor, and the roadmap's own T7 drives it into exactly that case.

2. **"Invariance of observables" is unqualified and will be violated on the roadmap's own backend.** T7 (line 119) reduces to PIFB2 `G`-attention and recovers `GL(K)` attention; WP3 (line 149) makes the Gaussian/`GL(K)` code the first backend; E1 (line 132) tests gauge invariance on that backend. On the Gaussian fiber with `G = GL^+(K)`, **Corollary A3.5** says the entire invariant content is the single scalar `r = (mu^T Sigma^{-1} mu)^{1/2}` per base point (verified: invariance of `r^2` to `1.3e-13`; explicit `A* in GL^+(4)` carrying one pair to another, `det A* = +0.419`, `wave2-01:292-294`). With `G = (R^K,+)` an invariant sees only the covariance field and is **blind to the mean** — where all inference content lives. Any observable E1 declares that is not a function of `r` (or of the covariance field) is either non-invariant or constant. E1 will pass trivially or fail confusingly, and the roadmap gives no criterion to tell which.

3. **The background carries a gauge fixing, and the roadmap never says so.** `wave2-01:300-303`: "*accept the consequence: the background data are not gauge-invariant, so the theory carries a gauge fixing inside its declared background, and the "noumenal" bundle is meaningful only relative to it.*" That admission belongs in WP0's exit gate.

### 1.4 Which theorem to cite, and the one-sentence correction

**Cite:** Proposition **A3.1** (`wave2-01:238`) as the provable statement; Theorem **A3.3** (`wave2-01:255`) as the criterion that determines what T2's "observables" may be; Corollaries **A3.4/A3.5** (`wave2-01:268,280`) as the binding scope warning for T7/WP3/E1. **Do not cite Theorem A-NOGO (b) as an obstacle** — the roadmap escapes it. In `Theory/`, cite `thm:pb-pullback-gauge-invariance` (`05c:124`, ESTABLISHED) and `eq:geo-local-reframing` (`02:159-161`) as prior art, with wave 2's two caveats (the jet gauge law `eq:pb-covariant-jet-gauge-law` is asserted not derived; the theorem is **false** at `05c:160` where `omega'` means a genuinely different connection — repair: use the frame-free `D^omega s = ver^omega o Ts`, two lines).

**Correction T2 needs, one sentence:**

> T2 proves **equivariance of `S` on the full datum** — `S[g . (q_i, p_i, s_i, r_i, L^q_{ij}, L^s_{ij}, A, L^obs)] = S[(q_i, p_i, s_i, r_i, L^q_{ij}, L^s_{ij}, A, L^obs)]` — **not** invariance of `S` under a gauge action on sections at fixed background, which Corollary A3.4 proves forces `S` to be constant whenever the fiber is a `G`-torsor; and its "observables" must be declared as functions on `M_q/G, M_s/G` per Theorem A3.3, which for the Gaussian `GL^+(K)` realization of T7 and WP3 is the single scalar `r = (mu^T Sigma^{-1} mu)^{1/2}`.

---

## 2. DOES THE ACTION EVADE O2? — YES, AND THIS IS THE ROADMAP'S BEST RESULT

### 2.1 The evasion is real

**O2** (`wave2-01:385-398`, Theorem A4.4(a)) has an explicit hypothesis: *"require `F_mu[s] = F[Q_X; X, o]` for every admissible pair `(s, Q_X)` related as in Theorem A4.1."* Only then does the deformation witness (`chi(c) = (c-0)(c-2)(c-4)`, `chi'|_D = (8,-4,8)`, CHECK 7) force `f` to be jet-free and expel `omega`.

**The roadmap explicitly declines that hypothesis.** Line 9: *"The complete live-peer PIFB2 action **should not be represented as the negative ELBO of one fixed joint law on the original agent-state variables**. It is an effective interaction action whose mathematical consequences can still be exact once its kinematics, admissible fields, and variational principle are declared."* Line 106: *"Live peer KL and attention-weighted neighbor consensus **are effective interaction terms** unless a separate enlarged generative construction is proved… The entire action may optionally admit a configuration-space Gibbs variational identity… **that identity is exact at a different level and is not the original state-level ELBO**."* Line 166 repeats it as the stable public description.

**Verdict: the roadmap's structure escapes O2 by dropping A-NOGO's premise, deliberately and with a stated reason.** The derivative terms `eta_q||D^A q_i||^2` (line 97) and the curvature term `kappa||F_A||^2` (line 99) therefore survive. This is an important and favorable finding and should be stated plainly: **wave 2's O2 is not an objection to this roadmap.** It is an objection to the *other* program — the one that tries to make the section functional equal `F[Q_X]` — and the roadmap has already chosen the other branch. Arriving at that independently, from the decision report rather than from A-NOGO, is a genuine convergence.

A second, quieter escape: A4.4(a) also needs `supp mu subseteq D`. The roadmap declares `mu` a positive smooth density or finite Radon measure on a `d`-dimensional `C` (line 32) — not design-supported. A4.5 (`wave2-01:406-413`) then applies instead, and says only that `F_mu` is an *extension* of `F[Q_X]`, non-unique. The roadmap does not claim uniqueness, so A4.5 is not violated either.

### 2.2 The residual obligation — and it is larger than the roadmap thinks

**What T7 must actually prove.** T7 (line 119) is: `C = {*}`, `mu({*}) = 1`; *"Prove that derivative and curvature sectors vanish and the theory reduces to PIFB2 \(G\)-attention."* Note:

- The first half is **near-vacuous**. At `C = {*}` there are no base directions, so `D^A q_i` and `F_A` have nothing to contract; their vanishing is definitional, not a theorem.
- The second half is a **crosswalk**, not a limit theorem. And it has a known negative constraint: `Research/manuscripts/magent_elbo_whitepaper/09_pifb2_crosswalk.tex` already shows the tie `R_ij = Omega_ij Sigma_j Omega_ij^T` **forces `tau = 1`**, so the deployed `tau = kappa sqrt(K)` operating point is *not* an exact coordinate (`audit-06-pifb2-gap.md:382-385`). T7 must respect that, and the roadmap does not mention it.
- **The theorem T7 should state and does not** is limit-commutation: that `argmin` of the `d`-dimensional theory converges to `argmin` of the zero-dimensional one as the spatial couplings go to zero (`eta_q, eta_s, kappa -> 0`), i.e. that the reduction commutes with T4's minimization. Absent that, T7 says only "setting the base to a point deletes the base terms", which nobody doubted.
- **Crucially, T7 does not restore consistency.** It is a reduction to PIFB2, and PIFB2's live-peer sector is itself not a state-level ELBO (that is the *verified* obstruction the decision report and wave-1 F3 both record). So no T-item anywhere re-supplies the constraint A-NOGO's O2 removed.

**Does WP5's realization ledger replace it? No — it is strictly weaker, and the roadmap should say so.** WP5 (line 151): *"Every action sector is labeled exact, approximate, effective, geometric, gauge-fixing, or open."* That is a **per-sector bookkeeping** obligation replacing a **global derivation** requirement. It solves the *honesty* problem (which sectors have probabilistic semantics) and does nothing for the *constraint* problem (why these sectors and not others). A label is not a derivation.

**Consequently the entire burden of term-class constraint falls on a classification theorem that the roadmap names but never schedules.** Line 11 states the danger exactly — *"The danger is uncontrolled arbitrariness: adding terms without a classification principle"* — and line 104 concedes *"This is a class to be narrowed by axioms, not yet a completed theorem."* But **no T-item, no WP, and no exit gate is a classification theorem.** T2 is covariance *verification* of a chosen class, not derivation of it. This is wave-1 **S4** verbatim, unaddressed, and O2's removal makes it *more* load-bearing than it was, not less. It is the roadmap's largest silent liability.

**Two further residuals the roadmap inherits without knowing:**
- T9's hypothesis `0 < Z < infinity` (line 121) already has a **proved counterexample in the same repository**: `Theory/04_generative.tex:244` `prop:gen-gibbs-counterexample`, ESTABLISHED — *"Normalized node potentials and an everywhere positive, finite, continuous edge potential need not give finite `Z_X`"*, with the explicit witness `psi_i = (2pi)^{-1/2} e^{-y_i^2/2}`, `psi_12 = e^{c y_1 y_2}`, `c >= 1`. T9 must clear this; `prop:gen-exact-normalization` (`04:205`) shows the directed construction that *avoids* needing `Z` at all.
- T8's closure column (line 120) is the numerical-analysis half only. The probabilistic half is enumerated at `Theory/03_probability.tex:443` `open:prob-continuum-theory`, which states the obstruction is **concrete, not laborious**: *"The reference measures are finite products… the same construction does not extend to infinitely many non-probability factors, so a continuum theory cannot obtain its reference measure by the route used here… Until that is done, a continuum energy has no density to be the exponent of."*

---

## 3. AUDIT-FINDING COVERAGE TABLE

| Finding | Verdict | Roadmap line that does (or fails to do) it |
|---|---|---|
| **S1** — VFE not a functional of a section (`Theory/02:403` vs `05_elbo:222`; zero base integrals) | **ADDRESSED BY REDEFINITION** | Lines 76-102 build an *action* on sections; T0-T4 typed. But line 9 explicitly severs the ELBO tie, so the object S1 asked for (a *free energy* on sections consistent with `F[Q_X]`) is still not delivered — a different, weaker-probabilistic/stronger-geometric object is. Wave 2 **proved the identity that would have delivered S1** (`F[Q_X] = int f dmu_D + TC_D`, residual `1.4e-14`, `wave2-01:318-339`) and the roadmap does not adopt it. |
| **S2** — 0/22 prior findings fixed; 29,043 lines of plans | **CONTRADICTED / AGGRAVATED** | `git diff --stat aedc662..24c02aa -- src tests tools Theory` is **empty**. Commit `24c02aa` adds 174 plan lines + 288 lines of ledger script. Plans now ~22,142 lines in `docs/superpowers/plans/` alone. Line 168 ("The next cycle should produce three artifacts in order") schedules more writing before any source edit. |
| **S3** — inert gauge sector, no curvature, connections absent from VFE | **PARTIALLY ADDRESSED — best coverage in the document** | Line 99 introduces `kappa int ||F_A||^2 dmu`, the program's first curvature term. Line 66 separates Cech transition from physical link and identifies `Omega_ij = U_i U_j^{-1}` as the flat coboundary case. Line 160: "Its frame-derived connection is pure gauge, while nontrivial curvature requires independent link data." E2 tests it. **Residual:** `F_A` is never defined (no `dA + (1/2)[A,A]`, no fiber metric on `Lambda^2 (x) ad P`) — the same absence wave 1 measured in `Theory/` (`grep` for `F_omega`, `d omega`, `[omega,omega]`, Ambrose: zero hits). And wave2-01 §1.7's surviving route for `omega` (`D^A pi = 0`; parallel background exists **iff** `Hol(omega) = {e}`) is not adopted. |
| **S4** — coupling chosen, not derived (`05b:66` "imposed by requiring"; `04:379` HYPOTHESIS; `06_gaussian:297` "The document does not claim that it is forced by anything"; `07b:1257` disclaims uniqueness) | **IGNORED — and now more load-bearing** | Named at lines 11 and 104; assigned to **no T-item, no WP, no exit gate**. WP0's gate is typing; T2's is covariance verification. With O2's constraint gone (§2.2), this is the only remaining source of term-class discipline. |
| **S5** — evidence artifact certifies nothing; 23/24 TeX mismatch and 4/4 protocol mismatch in **both** copies; fix is ~12 s of CPU | **IGNORED** | Not mentioned. |
| **S6** — apparatus unrunnable; `run_checks.py:324` hard-codes `C:\Python314\python.exe`; 31 cited evidence paths absent | **IGNORED AND REPRODUCED** | Every E-item (line 127: "machine-readable outputs") and WP3's gate ("E0-E4 pass") require a runnable harness; wave-2 W5 measured 125/891 baseline test failures, all environmental, 32 of them `FileNotFoundError: 'C:\anaconda\python.exe'`. And the roadmap's own new `build_pifb2_roadmap_ledger.py:13-17` hard-codes three absolute Windows paths. |
| **Self-citation / priority** — Dennis, "Epistemic Gauge Theory," Preprints.org 202505.1773.v1, 23 May 2025; zero hits for "epistemic gauge" in both repos; four self-cites in `references.bib` cited zero times | **IGNORED** | No bibliography, no priority statement, no positioning. WP1's deliverable is a "theorem-first manuscript" (line 147) — the item wave 2 ranked "do first, this week, fifteen minutes, asymmetric downside if skipped" is unscheduled. |
| **`03:391`** — `prop:prob-marginals-do-not-determine-joint` proves coordinates where the definition marginalizes onto **blocks**; counterexample `\|V\|=1, M=1, K_{1,1}=R^2, M_{1,1}={0}`; propagates to `03:387`, `prop:prob-compatibility-nonidentifiability`(i), `05_elbo:32` | **IGNORED — and depended upon** | E5 (line 136: "Construct or fail to construct a normalized fixed joint for every sector") and WP5's ledger rest on the non-identification results this error propagates into. |
| **`07b` zero HYPOTHESIS tags** — 81 ESTABLISHED, 10 DEFINITION, 1 OPEN, 1 NOT-CLAIMED, **0 HYPOTHESIS** in 2,828 lines | **PARTIALLY ADDRESSED (deferred, not fixed)** | Line 168: "Work on RG closure, scale-free fixed points, or broad phenomenology should wait until those artifacts agree." Compatible with the audit's "cut or demote"; but retagging is a today-task and is unscheduled. |
| **`confirmatory_analysis.py` mutation 5/15** — sign-test tail reversed, **Holm -> Bonferroni**, `<=` -> `<` at the frozen `-0.02` boundary, two-sided factor 2 dropped, **95% -> 90% CI**, half-width `/2` dropped, bootstrap median all survive; 80% line coverage, 33% mutation-killed | **IGNORED AND DEPENDED UPON** | E7 (line 138: "Pre-register observables… compare against simpler consensus, Markov-field, and transformer baselines **across seeds and sizes**") lands squarely on the least-protected code in the repository. `holm_adjust` is confirmed live at `confirmatory_analysis.py:79,374,478`. E7 cannot yield a trustworthy multiplicity-corrected result today. |
| *(also)* **N-01** — `RngStreams.from_seed` at 15 call sites, exactly one consumes a generator; `fixed_ray_experiment.py:2758-2762` hard-codes master seeds | **IGNORED AND DEPENDED UPON** | Line 127: "Every run should freeze the action version, discretization, configuration, **seed policy**, and machine-readable outputs." The seed policy is currently a no-op on output. |
| *(also)* **Wave-2 W5 structural blind spots** — all four `gauge_fixture` permutations are **involutions** (`tests/test_finite_experiment.py:41`), so gauge *direction* is undetectable by construction; `adjacent_pairs` is doubly stochastic; Hoeffding fixture symmetric | **IGNORED AND DEPENDED UPON** | E1 and E2 (lines 132-133) are gauge-direction and holonomy tests. On the current fixtures they cannot fail. |
| *(also)* **Wave-2 W3 F-1** — conditioning gates 843x and 33,500x looser than the tolerance results are graded at; safe ceilings `cond ~ 3e3`, `min_spd_rcond ~ 1e-7` | **IGNORED AND DEPENDED UPON** | E0, E3, E6 are numerical-agreement gates. |
| *(also)* **T-04** — flagship preregistered `-0.02` endpoint was mathematically unreachable (`-9/625 = -0.01439`) from the moment it was frozen; 40 jobs, 3,644 GPU-seconds | **IGNORED (methodological)** | E7 pre-registers observables with no feasibility-certificate gate. The audit's cheapest lesson — ten lines of rational arithmetic before spending compute — is unincorporated. |
| **Wave-1 G1/G2** — Cech content and base transport have zero downstream consumers; `Omega_ij` conflated in PIFB2 | **CORRECTLY INTERNALIZED — CREDIT** | See §4. |

---

## 4. WHERE THE ROADMAP IS RIGHT AND THE AUDIT IS SUPERSEDED — verified, and credited

**Line 66, verbatim:**

> "On \(U_i\cap U_j\), the transition function between \(u_i\) and \(u_j\) is a change of coordinates, not automatically a physical interaction. If \(\Omega_{ij}\) is only the representation of this transition, then it is pure gauge bookkeeping and has cocycle consistency. Intrinsic comparison of two sections in the same associated fiber needs no additional physical transport. Nontrivial relational physics requires one of two extra structures: a connection \(A\) whose parallel transport compares separated base points, or an independent overlap/link automorphism \(L_{ij}\) with a declared transformation law. **The specialization \(\Omega_{ij}=U_iU_j^{-1}\) is the flat coboundary case and cannot generate nontrivial cycle holonomy by itself.**"

This is correct, and it is **provably** correct, because `Theory/` already proves it:

- `02_geometry.tex:502` `eq:geo-cech-cocycle`: `T_ii = e_G`, `T_ji = (T_ij)^{-1}`, `T_ij T_jl = T_il` — "cocycle consistency", ESTABLISHED.
- `02_geometry.tex:519` `eq:geo-coboundary-form`: `T_ij^x = U_i^x (U_j^x)^{-1}` **is exactly** the roadmap's `Omega_ij = U_i U_j^{-1}`, and is proved equivalent to triviality of `P|_{C_0}`.
- `02_geometry.tex:561` `def:geo-graph-links`: independently declared `Theta_e^b, Theta_e^m` with their own gauge law `eq:geo-regime-two-gauge-law` — the roadmap's "independent overlap/link automorphism `L_ij` with a declared transformation law".
- `02_geometry.tex:597` `prop:geo-trivializing-criterion`: coboundary form **iff** every closed internal walk has trivial product — the exact "cannot generate nontrivial cycle holonomy" statement, ESTABLISHED with proof.
- `02_geometry.tex:646` `hyp:geo-flat-links` / `eq:geo-flat-regime`: declares `Theta_e^x = T_ij^x = U_i^x(U_j^x)^{-1}`, and the following prose reads *"This excludes represented graph holonomy in either channel."*
- `02_geometry.tex:625` `hyp:geo-graph-base-transport`: the roadmap's *other* route (a connection whose transport compares separated base points), with the warning *"Without the curve assignment and these equalities, graph holonomy and base-connection holonomy are unrelated."*

**Line 160, verbatim:** *"Its fixed-connection, attention-free covariant Markov-field term is identified as a closed-ELBO member, whereas the attention-weighted neighbor term is an effective consensus regularizer. Its frame-smoothness term is gauge fixing. **Its frame-derived connection is pure gauge, while nontrivial curvature requires independent link data.**"*

This is also correct and matches `Theory/02_geometry.tex:397` (NOT-CLAIMED: *"The connections… are chosen data; no curvature or transport is inferred from the agent frames"*) and wave-1 **G1**'s diagnosis. The roadmap's E2 acceptance gate ("Require trivial loop holonomy in the former and controlled nontrivial holonomy only in the latter") is a correctly-designed test of exactly the finding wave 1 raised.

**Credit, stated plainly.** Lines 66 and 160 fully internalize wave-1 **G1**, **G2** and **S3**, and line 66 in particular resolves the `Omega_ij` conflation that wave 1 called *"the rewrite's single most valuable contribution"* (`2026-08-11-ultradeep-expert-audit.md:211`). On this axis the roadmap is not behind the audit; it is level with `Theory/`'s proved position and correctly proposes the two remedies. **The only defect is that it presents as a design decision what is already an ESTABLISHED proposition in the repository it is committed to.**

---

## 5. THE BIG OMISSION — T0-T9 mapped to existing `Theory/` work

Roadmap **line 174 (Source boundary), verbatim:**

> "This roadmap is based on the live Research/manuscripts/PIFB2.tex and MAgent_Model-main implementation inspected on 2026-08-12, plus docs/derivations/2026-08-12-pifb2-elbo-program-decision/final-report.md."

`MultiAgentELBO/Theory/` — 16,821 lines of TeX across 24 files, in the repository the roadmap is committed to — is **not named**. Neither is `Research/manuscripts/magent_elbo_whitepaper/` (3,883 lines). `build_pifb2_roadmap_ledger.py` hard-binds the same three sources and hashes them; `Theory/` appears nowhere in it.

### 5.1 Concrete mapping

| Roadmap item | Already discharged in `Theory/` (or the whitepaper) | Coverage |
|---|---|---|
| **T0 typed kinematics** — measured base; principal `G`-bundle; associated statistical bundles; declared gauge action, sample spaces, overlaps, boundary conditions | `02:16 def:geo-context-base` (smooth, no intrinsic geometry — the roadmap's line-32 warning, already made) · `02:40 def:geo-principal-systems` · `02:67-78` law fibers + `02:103 hyp:geo-smooth-tier` · `02:80-95 eq:geo-pushforward-actions` **with the warning at `02:97-100` "Multiplying a matrix into a density is not the pushforward"** = roadmap line 48's requirement, already enforced · `02:120 def:geo-associated-bundles` + `eq:geo-quotient-convention` · `02:282 def:geo-connections` (two independent `omega_b, omega_m`) · `02:340 def:geo-covariant-defects` · `02:403 def:geo-agent` = roadmap lines 56-64 in content, including per-agent domains and the two channels · `sec:geo-cech` 02:486-534 · `def:geo-graph-links` 02:561 · `05c:59 prop:pb-statistical-tensor-descent` (Fisher **and** Amari-Chentsov descend to vertical tensors on `P x_rho B`) = roadmap line 40, **proved** · `03:12-330` typing/measurability plumbing | **~90%** |
| **T1 well-definedness** — measurability, integrability, differentiability, extended-real conventions | `03:249 cor:prob-kernel-kl-measurability` · `03:296 prop:prob-kernel-integration-measurability` · `03:313 def:prob-log-density-ratio-convention` (= "extended-real conventions at singular boundaries", verbatim in effect) · `03:185 thm:prob-kernel-rn-measurable-version` · `05d:109 hyp:hist-regular-section-space` with the exact warning *"No such structure follows merely from writing down all smooth sections"* · `05d:235 def:hist-finite-configuration-tier` + `05d:275 thm:hist-finite-tier-regularity` · `05d:333-340` `Q^{L2} = L^2(mu;R^K)` proved **strong** under two-sided bounds | **~70%** |
| **T2 gauge covariance** | `05c:124 thm:pb-pullback-gauge-invariance` (ESTABLISHED; wave-2 gaps noted) · `05c:184 prop:pb-pullback-connection-change` + counterexample `05c:220-232` · `02:159-181` passive reframing + `Aut_G(P)` with `k_i^m = h_i^{-1} k_i^b h_i` · `04:379 hyp:gen-kernel-covariance` + `04:408 prop:gen-product-evidence-invariance` · `05_elbo:361 cor:elbo-independent-frame-invariance` · **plus** `wave2-01:163-303`, the complete T2 answer with proofs (A2 at the *measurable* tier), the correct statement (A3.1), the criterion (A3.3), and the classification (A3.4/A3.5), all with numerics | **~85%, and the missing 15% is the correction in §1.4, not new mathematics** |
| **T3 attention-row elimination** — strict convexity, unique `beta*`, reduced log-partition, measurable dependence, envelope derivative | `05b:547 prop:obs-attention-elbo`, ESTABLISHED: `F_i^att(beta_i) = KL(beta_i||pi_i) + tau_i^{-1} sum_j beta_ij E D_ij` with *"Its **unique interior minimizer** on the positive-prior source simplex"* `eq:obs-attention-recognition-optimum` — the roadmap's `beta*` exactly. Missing piece (wave-1 **F10**) is `F^att(beta*) = -log Z`; **wave-2 W2 supplies it verified to `8.9e-16`**: `F_i^att(beta) = KL(beta||beta*) - log Z`, which delivers both the reduced value **and** the envelope derivative. Measurable dependence on fields = `03:296`. Wave-1 numerically confirmed PIFB2's envelope reduction: `min_beta L = -0.10738678690` vs `-tau log Z = -0.10738678695`. | **~95% — T3 is one paragraph** |
| **T4 existence of minimizers** — direct method, coercivity, weak compactness, weak lower semicontinuity | **Genuinely absent.** Zero hits corpus-wide for "direct method", "Gamma-convergence"; "lower semicontinuous" only in `05a_expfamily.tex`; "coercive" only in `05a`, `11`. Nearest: `05d:275` (finite-dim tier), `11:256 thm:obs-star-fixed-point-contraction` (unique fixed point + geometric contraction, Gaussian star), `05d:320-323` degeneracy condition, and `wave2-01:364-381` Prop A4.3 identifying `rank Ev_D = N` with metric positive-definiteness. | **~10% — genuinely new, correctly called the decisive milestone** |
| **T5 first variation** | Absent for sections (zero "Euler-Lagrange", zero "first variation"). Present in charts: `05b:668-694 sec:local-natural-gradient`. **`wave2-01:419-474` derives it for the jet-free sector** (A5.1, verified `1.4e-9`) and states the roadmap's own T5 caveat first: *"the flow is a **decoupled family of ODEs indexed by `c`**. No derivative of `m` appears, so distinct contexts never talk to each other."* = roadmap line 117 *"Without spatial terms the equations must be identified as pointwise, not propagating."* | **~40%** |
| **T6 dynamics** — `dS/dt = -\|grad S\|^2 <= 0`, local well-posedness | `05b:668-694` dissipation ESTABLISHED (with "Block orthogonality is load bearing", `05b:696-700`) · `05b:648-668` exact replicator flow, dissipation `-gamma_i Var(c_ij) <= 0` · `11:256` contraction rate · `05_elbo:610 prop:elbo-finite-step-nonmonotonicity` (**finite natural-gradient steps need not be monotone — directly constrains E6**) · `05_elbo:637 open:elbo-alternating-convergence` · `05d:560 prop:hist-semidefinite-gradient-obstruction` (a semidefinite tensor cannot be silently inverted — bites T6's "declared mobility") · `wave2-01:453-463` Picard-Lindelohf well-posedness with explicit rate. **AND a refutation:** `05d:344-353` exhibits `Q = sum_k k^{-2} sin(k theta)` on `S^1` with `Gamma = H^1`, `F(Q) = (1/2) int |Q'|^2`, having **no `L^2` gradient** — so T6's stated metric (the "integrated product Fisher metric", i.e. `L^2`-Fisher) does **not** admit a gradient flow once `eta_q||D^A q_i||^2` is present. | **~50%, and one existing counterexample refutes T6 as written** |
| **T7 zero-dimensional reduction** | `Theory/` is *already* the zero-dimensional theory: `03:15 def:prob-finite-design`, zero base integrals corpus-wide (coordinator-verified). The PIFB2 correspondence is written: `magent_elbo_whitepaper/09_pifb2_crosswalk.tex`, `10_executable_crosswalk.tex`, and **`audit-06-pifb2-gap.md:56-99` is a 38-row PIFB2-construction -> `Theory/`-label table with per-row status** — that table *is* T7's crosswalk, already done. Constraint T7 must respect: the crosswalk shows `R_ij = Omega_ij Sigma_j Omega_ij^T` forces `tau = 1`. | **~75%; genuinely new content is only the `d -> 0` limit-commutation statement, which T7 does not ask for** |
| **T8 discretization limit** | Absent numerically (zero "quadrature", "finite element", "mesh"). But the obligation is enumerated, and **more sharply than T8 states it**, at `03:443 open:prob-continuum-theory`: refining designs, projective/Kolmogorov system, topology and sigma-algebra on the section space, tightness, functional convergence, control of gauge and reference-measure choices under refinement, and normalizability — with *"The last item is where the obstruction is concrete rather than merely laborious… a continuum energy has no density to be the exponent of."* | **~15% (the obligation list, not the theorem) — and T8 omits the concrete obstruction** |
| **T9 optional Gibbs completion** — configuration-level variational identity, kept distinct from state-level ELBO | **Already written as a full chapter**: `Research/manuscripts/magent_elbo_whitepaper/07_configuration_elbo.tex`, "Configuration Thermodynamics and the Nested ELBO" — hierarchical measure `eq:hierarchical-generative-measure`, configuration recognition kernel `eq:configuration-recognition-kernel`, semidirect joint `eq:hierarchical-recognition-law`, `eq:nested-configuration-evidence-identity`, `eq:hierarchical-elbo-definition`, `eq:hierarchical-elbo-gap`, `eq:hierarchical-elbo-equality-condition`. Its own figure caption already draws T9's required distinction (*"not agents or substitutes for the section-bearing agent ontology"*). **And its hypothesis has a proved counterexample**: `Theory/04:244 prop:gen-gibbs-counterexample`, ESTABLISHED. | **~80% written; hypothesis already obstructed** |

### 5.2 Duplication risk, quantified

- **Directly bearing on T0-T3, T5-T7, T9:** `02_geometry.tex` (772), `03_probability.tex` (449), `04_generative.tex` (477), `05_elbo.tex` (660), `05b_local_collective_elbo.tex` (783), the T2/T5-relevant core of `05c_pullback_geometry.tex` (~700 of 1,391), the section-space/metric material of `05d_relational_inference.tex` (~450 of 1,624), `07_general_renormalization.tex:145-290` (~145), plus whitepaper `07_configuration_elbo.tex` and `09_pifb2_crosswalk.tex`. **Conservatively ~4,500-5,000 lines of already-proved TeX, i.e. 27-30% of the `Theory/` corpus.**
- **Plus ~1,000 lines of already-*executed* wave-2 construction work** (`wave2-01-constructions.md`): A2 proved at the measurable tier, A3.1/A3.3/A3.4/A3.5, A4.1 with residual `1.4e-14`, A4.3, A4.4, A5.1 with well-posedness and explicit rates — with numerics, controls, and paste-ready SPEC-compliant LaTeX.
- **Genuinely new in the roadmap: T4, T8, and the jet/curvature sectors of T5-T6** — 2.5 of 10 T-items.
- **Concrete exposure.** WP0's deliverable (line 146) is *"A concise specification choosing the base measure and geometry, principal `G`-bundle, associated statistical fibers, connection/link status, likelihood typing, supports, and boundary conditions."* Every item on that list except **the base measure and cometric** is already declared and typed in `02_geometry.tex` + `03_probability.tex`, at higher generality (the measurable tier) than WP0 proposes. WP1's deliverable (line 147) is *"a theorem-first manuscript proving T0-T4"*; executed against line 174's source boundary it will re-derive `02_geometry.tex` and `05c:30-130` from scratch, re-prove `prop:obs-attention-elbo`, and rediscover A3.5 the first time someone runs E1 on the Gaussian backend. **Estimated waste: essentially all of WP0 and the T0-T3 portion of WP1.**
- **What WP0 should actually contain — the delta, three items.** (1) The base measure `mu` and base cometric that `Theory/` deliberately withholds (`12_philosophy:33-38` forbids a law on `C`; declaring one is wave-2 obstruction **O3** and *contradicts* the manuscript's own N1 — the roadmap must adjudicate this, and line 32 shows it already understands the problem). (2) The independent overlap automorphism `L^q_{ij}, L^s_{ij}` as a first-class field with a declared transformation law — `Theory/` has `Theta_e^x` on a graph (`02:561`) but not on base overlaps. (3) `F_A`: its definition, and the fiber metric on `Lambda^2 (x) ad P` that `||F_A||^2` contracts against — absent from `Theory/` and from the roadmap alike.

---

## 6. WHAT THE ROADMAP SILENTLY ASSUMES IS SOUND — ranked by damage

1. **S4 / `hyp:gen-kernel-covariance` is a derivation.** It is not (`05b:66` "imposed by requiring", DEFINITION; `04:379` HYPOTHESIS; `06_gaussian:297` "The document does not claim that it is forced by anything"; `07b:1257` disclaims uniqueness). **Corrupts:** T2's scientific meaning (verifying a designed property), E1's interpretation, and — after O2's constraint is dropped — the admissibility of the entire term class. **This is the top item.**
2. **The statistics and gauge test harness is trustworthy.** It is not: `confirmatory_analysis.py` 5/15 mutation (Holm->Bonferroni, 95%->90% CI, tail reversal all survive); `finite_gauge.py` 2/6 with all four `gauge_fixture` permutations involutions (`tests/test_finite_experiment.py:41`), making gauge *direction* undetectable by construction; `adjacent_pairs` doubly stochastic; seed has zero effect on output (N-01, 15 `from_seed` call sites, one consumer). **Corrupts:** E1, E2, E6, E7 — four of eight experiments — and line 127's "seed policy".
3. **`prop:prob-marginals-do-not-determine-joint` (`03:391`) is correct.** It is not (coordinates vs blocks; counterexample verified, block marginals at `KL = 0.3393564486857903`). Propagates to `prop:prob-compatibility-nonidentifiability`(i), `03:387`, `05_elbo:32`. **Corrupts:** E5's and WP5's non-identification reasoning.
4. **The verification apparatus can gate anything.** It cannot (S5: 23/24 TeX + 4/4 protocol mismatch in both copies; S6: hard-coded interpreter, 31 absent evidence paths, 125/891 environmental test failures). **Corrupts:** WP1's exit gate ("independent proof review"), WP3's ("E0-E4 pass"), and every "acceptance gate" in the experiment table.
5. **`prop:gen-product-evidence-invariance` (`04:408`) is complete.** Wave-2 W2: the induction **has no base case**; "the root covariance identities are never displayed". Anything the roadmap builds on evidence invariance under the passive product action inherits it.
6. **`thm:pb-pullback-gauge-invariance` (`05c:124`) is proved as stated.** Wave-2 W2: `eq:pb-covariant-jet-gauge-law` is asserted, not derived; and the theorem is **false** at `05c:160` where `omega'` denotes a genuinely different connection. T2's jet sector rests on it. Two-line frame-free repair available.
7. **Conditioning gates are calibrated.** They are not (843x and 33,500x looser than grading tolerance; safe ceilings `cond ~ 3e3`, `min_spd_rcond ~ 1e-7`). **Corrupts:** E0, E3, E6 numerics on the `GL(K)` backend.

**Direct T/E dependencies on broken code or theory:** T2 -> `05c:124` (item 6) and `04:408` (item 5); T3 -> `05b:547`'s Lagrange gap (repair supplied); T6 -> refuted as stated by `05d:344-353`; T9 -> obstructed by `04:244`; E1/E2 -> involutive fixtures (item 2); E5 -> `03:391` (item 3); E6 -> `prop:elbo-finite-step-nonmonotonicity` (`05_elbo:610`) and item 7; E7 -> `confirmatory_analysis.py` (item 2) and N-01.

---

## 7. VERDICT

**A lateral move with one genuine structural advance, one serious regression, and a large silent duplication — not a restart that discards proved work, because it never encountered it.**

*The genuine advance.* Line 9's executive decision — declaring the live-peer action an **effective interaction action** rather than the negative ELBO of a fixed joint — is the correct structural response to wave-2's **O2**, reached independently from the decision report. It is what preserves the derivative and curvature sectors that O2 would otherwise expel, and it converts wave 1's largest open item into a well-posed alternative program rather than an impossible one. Lines 66 and 160 correctly internalize G1/G2/S3 and match `Theory/02_geometry.tex`'s proved separation of Cech transition from physical link. E2 is a well-designed test of the exact thing wave 1 called inert. T4 and T8 are genuinely new and correctly prioritized. That is real content.

*The regression.* It is the fourth planning document on a pile the audit measured at ~22,142 plan lines in `docs/superpowers/plans/` alone, committed `docs:`-only against a source tree that has not changed since `aedc662` — and it ships 288 lines of new verification apparatus, with hard-coded absolute Windows paths, for a 174-line plan. It schedules **none** of wave 2's six "do first, this week" items. Four of its eight experiments depend on test code the audit proved cannot fail.

*The duplication.* Roughly 27-30% of the `Theory/` corpus, plus a whitepaper chapter, plus ~1,000 lines of already-executed wave-2 construction, bear directly on T0-T3 and T5-T7 and T9 — and none of it is in the roadmap's source boundary or its ledger script.

### The three changes that would most improve it

1. **Fix T2's verb and E1's gate.** Replace "Prove invariance of \(\mathcal S\)" with the equivariance-on-the-full-datum statement of §1.4; cite A3.1, A3.3, A3.4/A3.5 and `Theory/05c:124` + `02:159-181`; and rewrite E1's acceptance gate to test equivariance on the transformed datum **plus** the `M/G` classification, with the explicit expectation that on the Gaussian `GL^+(K)` backend of T7/WP3 the invariant content is the single scalar `r = (mu^T Sigma^{-1} mu)^{1/2}`. Add the honest consequence: the background carries a gauge fixing. *(Cost: one table row and one experiment row. Prevents a false theorem and a meaningless test.)*

2. **Rewrite line 174 and collapse WP0 to a delta.** Add `MultiAgentELBO/Theory/` and `Research/manuscripts/magent_elbo_whitepaper/` to the source boundary and to `build_pifb2_roadmap_ledger.py`. Replace WP0's full ontology spec with the three-item delta of §5.2: the base measure and cometric (adjudicating the O3/N1 collision), `L_ij` as a first-class overlap field with a transformation law, and a definition of `F_A` with its fiber metric. Then cut WP1 to **T4 alone**, citing `02_geometry.tex` for T0, `03`+`05d:109-360` for T1, §1.4 for T2, and `05b:547` + wave-2's `KL(beta||beta*) - log Z` for T3. *(This is the single largest saving available: it converts a manuscript into an addendum plus one hard theorem.)*

3. **Insert a defect gate ahead of WP0, and promote S4 to a numbered T-item.** The gate contains exactly the audit items the T/E program depends on: **S4 as T2b — a classification theorem** (line 11 names the danger; with O2's constraint gone it is the only remaining discipline on the term class), `03:391` blocks-not-coordinates, tests for the confirmatory statistics layer (Holm, CI width, test tails), one non-involutive `gauge_fixture`, real seed plumbing, and a re-run of `run_checks.py` (~12 s of CPU, restores 13 NUMERICAL claims). Add the Dennis 2025 priority citation. *(Fifteen minutes to hours each; without them E1, E2, E5, E6, E7 produce numbers nobody should believe.)*

**One correction to fold in while editing:** T6 as written is refuted by `Theory/05d:344-353`. The "integrated product Fisher metric" is the `L^2`-Fisher metric, and the manuscript's own `H^1` counterexample shows a gradient-energy objective has no `L^2` gradient. With `eta_q||D^A q_i||^2` present, T6 must declare an `H^1`-type mobility or restrict the admissible class — and say which.
