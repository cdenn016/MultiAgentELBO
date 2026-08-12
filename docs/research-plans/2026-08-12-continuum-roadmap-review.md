# Review — PIFB2 continuum action and exact-ELBO research roadmap

Date: 2026-08-12
Document under review: `docs/research-plans/2026-08-12-pifb2-continuum-roadmap.md` (175 lines, commit `24c02aa`)
Method: six expert referees run in parallel — audit reconciliation, geometric analysis / existence theory, effective-action classification, gauge kinematics, provenance and gates, prior art — followed by independent coordinator verification of every FATAL and CRITICAL claim.
Execution policy: CPU only. No GPU or CUDA job was started.
Prior context: `Desktop\MultiAgentELBO\docs\audits\2026-08-11-ultradeep-expert-audit.md` and `...\2026-08-12-ultradeep-expert-audit-wave-2.md`.

## Verdict

This is a serious document and much better than the plans that preceded it. Lines 9–11, 32, 66, 104 and 106 are correct where the parent manuscript was wrong, and line 66 in particular independently repairs the one genuine category error in `PIFB2.tex` — the conflation of a Čech transition function with a physical transport. Referees credited ten separate items. The self-awareness is real, not decorative.

It also has two **fatal technical defects**, both of which make T2 and T4 mutually unsatisfiable as written; it **duplicates roughly two thirds of its own theorem roadmap** with work already finished in `Theory/` in the same repository; several of its acceptance gates **cannot fail**; and its "Relationship to the existing code" section describes an implementation that **is not in this repository**, quoting a README sentence that **does not exist**.

Net: a lateral move with one real advance, one regression, and large silent duplication. It proposes about twenty-five new obligations and discharges zero of the roughly forty defects already on the books.

---

## 1. Two fatal findings

### F-1 — The Yang–Mills term cannot be both gauge-invariant and bounded below for `G = GL(K,\mathbb R)`

Found independently by two referees (action-class and gauge-kinematics). **Coordinator-verified directly.**

The `Ad`-invariant symmetric bilinear forms on `\mathfrak{gl}(K,\mathbb R)` form a two-dimensional space spanned by `\mathrm{tr}(XY)` and `\mathrm{tr}X\,\mathrm{tr}Y`. No combination is positive definite:

```
K=2   a·tr(XY) + b·trX·trY      eigenvalue range        pos.def
      a=1 b=0                   [-1.000, +1.000]        False
      a=1 b=-1/K                [-1.000, +1.000]        False
      a=1 b=5                   [-1.000, +11.000]       False
K=3, K=4                        identical pattern       False
```

And the form that *is* positive definite is not invariant:

```
Frobenius  tr(XᵀY):  before = -4.8590   after Ad = -66.3065   Ad-invariant?  False
Killing    tr(XY):   before = +0.3631   after Ad = +0.3631    Ad-invariant?  True   (indefinite)
```

So `\kappa\int\|F_A\|^2` at line 99 is either not gauge-invariant (breaking **T2**) or not bounded below (breaking **T4**'s coercivity and direct method). **T2 ⟂ T4.**

This makes line 13 wrong in an important way. It says compactness of `G` "may be imposed in the first existence theorem as an analytical hypothesis, not as an ontological commitment." Compactness is not analytical convenience here — it is **kinematic**, required at T0 for the curvature term to exist at all, and independently required for `0 < Z < \infty` at T9. The roadmap declines the commitment its own action needs.

Two fixes, both already available:
- Replace `\|F_A\|^2` with the **Fisher-dressed curvature** `g^F(F\cdot q, F\cdot q)` — invariant, PSD, kernel exactly the stabilizer, and `\kappa` becomes a field-dependent gauge coupling, which is standard practice. A referee verified invariance to `7\mathrm{e}{-8}`.
- Or reduce the structure group to a compact `G` (or compact type) and state it in T0.

### F-2 — The categorical fiber admits no continuous gauge group, so the multi-family gate is unsatisfiable

The Fisher–Rao metric on the open simplex `\Delta_n^\circ` is isometric to the positive orthant of the round sphere `S^n(2)` under `p \mapsto 2\sqrt p`. Its isometry group is therefore **finite**: `\mathrm{Isom}(\Delta_n^\circ, g^F) \cong S_{n+1}`, of order `(n+1)!` (verified symbolically; `0/200` random `O(4)` elements preserve the orthant, all 24 permutations do).

Consequence: no positive-dimensional Lie group acts on the categorical fiber by Fisher–Rao isometries. A connected `G` acts trivially, so `F_A \equiv 0` identically, at every base dimension.

This breaks three gates at once: **E0** (line 131, "at least categorical and Gaussian fiber realizations"), **WP1**'s exit gate (line 147, "at least two nonisomorphic statistical families instantiate the hypotheses"), and line 162's demand for an early non-Gaussian backend. With one fixed `G`, they cannot be satisfied by that pair.

The good news is that the Gaussian side is *better* than the roadmap claims. `GL(K,\mathbb R)` **does** act by Fisher–Rao isometries on the multivariate Gaussian family under the declared pushforward congruence `(\mu,\Sigma)\mapsto(A\mu, A\Sigma A^\top)` — verified to `7.6\mathrm{e}{-15}`, and already proved in-corpus at `05c:59`. Stronger: a referee computed the curvature-annihilator algebra and found `\mathrm{Isom}^\circ(\mathrm{MVN}, g^F) = GL^+(K)\ltimes\mathbb R^K` exactly for `K = 2,3`. `GL(K)` is not one choice among many — it is the maximal one. That is a result worth stating in the paper.

Fix: replace the categorical showcase with `\mathrm{SPD}(K)` under `GL(K)` congruence, or make `G` depend on the fiber and confine T7 to Gaussians.

---

## 2. What the roadmap gets right, and the A-NOGO adjudication

**T2 evades Theorem A-NOGO.** This was the main risk going in, and the roadmap clears it — twice.

Wave 2 proved that for a `G`-torsor fiber, `\mathrm{Aut}_G(P)` acts simply transitively on sections, so every gauge-invariant functional on sections is constant. The roadmap escapes because line 114 applies "one passive local gauge action applied to **sections, likelihood data, comparison maps, and connections**" — a simultaneous transformation — and, decisively, lines 59–61 type the priors `p_i, r_i` as **sections** rather than fixed chart data. That is exactly the condition wave 2 identified as load-bearing (a chart-declared prior is where invariance fails, numerically `192.94` versus `9.9\mathrm{e}{-14}`). Second independent escape: line 13 makes the fibers general statistical manifolds rather than torsors, so the no-go's hypothesis fails generically. A third, stronger escape a referee identified: A-NOGO is stated for a *single* section, while the roadmap's action is a **population** functional — the diagonal quotient has dimension `96` at `N=8, K=4`, and this escape works even on a torsor fiber.

**But T2's verb is wrong.** "Prove invariance of `\mathcal S`" is the precise phrasing wave 2 showed to be unfulfillable. The correct statement is equivariance of `\mathcal S` on the full datum `(q_i, p_i, s_i, r_i, L^q_{ij}, L^s_{ij}, A, \mathcal L^{obs}_i)`, with observables required to be functions on `\mathcal M/G`. One-sentence fix, and the roadmap should cite the no-go to explain why the sentence is phrased that way.

**The roadmap also escapes obstruction O2, and this is its best structural result.** Wave 2's second obstruction — that consistency with the finite-design ELBO forces a jet-free integrand, expelling the connection — has as its hypothesis that the section functional *equals* the finite-design ELBO. Line 9 explicitly declines that, and line 106 labels the live-peer terms effective. So the Dirichlet and curvature sectors survive. **O2 is not an objection to this roadmap.** Say so plainly in the document.

**Other correct items**, verified: line 66's four clauses on transition versus link versus connection all check out against `02:449-483`, `02:502`, `02:557-622`; line 160's four-way term classification is correct on every clause and stated more crisply than anywhere in `Theory/` or `PIFB2.tex`; line 32's observation that a smooth manifold has no canonical volume form is a genuine catch (it is wave-2 obstruction O3, found independently); and the typing bug flagged at line 104 — an expectation under a belief law on `k` cannot contain an unintegrated model variable `m` — is a **real live bug** in `PIFB2.tex`'s `eq:free_energy_functional_final`.

---

## 3. The duplication: about two thirds of T0–T9 is already done in this repository

Line 174 names only `PIFB2.tex`, the `MAgent_Model-main` implementation, and the decision report. It does not mention `Theory/` — 16,821 lines of finished rigorous development in the very repository the roadmap is committed to.

| Target | Already covered | Where |
|---|---|---|
| T0 typed kinematics | **~90%** | `02:16,40,67-78,80-95,120,282,340,403`; `05c:59` proves Fisher + Amari–Chentsov descent to the associated bundle |
| T1 well-definedness | ~70% | `03:249,296,313,185`; `05d:109,235,275,333-340` |
| T2 gauge covariance | **~85%** | `05c:124`, `02:159-181`, `04:379,408`, `05:361`, plus wave 2's equivariance proposition |
| T3 row elimination | **~95%** | `05b:547` gives the unique interior minimizer verbatim; wave 2's `\KL(\beta\|\beta^*) - \log Z` closes it to `8.9\mathrm{e}{-16}` |
| T4 existence | ~10% | genuinely new — correctly identified as the decisive milestone |
| T5 first variation | ~40% | wave 2 already states T5's own caveat |
| T6 dynamics | ~50%, and **refuted as written** | `05d:344-353`: the `L^2`-Fisher metric has no gradient for jet objectives |
| T7 zero-dim reduction | ~75% | `audit-06` already contains the 38-row crosswalk |
| T8 discretization | ~15% | `03:443` states the obstruction more sharply than T8 does |
| T9 Gibbs completion | **~80%**, and partly refuted | the whitepaper's `07_configuration_elbo.tex` is the chapter; `04:244` already refutes `0<Z<\infty` |

Genuinely new: **2.5 of 10 T-items.** WP0 as scoped duplicates `02_geometry.tex` at *lower* generality. Its real content is three items: the base measure/cometric declaration (which collides with the manuscript's own N1), `L_{ij}` as an overlap field, and a definition of `F_A`. It should be a two-page delta, not a from-scratch ontology.

The highest value-per-effort item in the whole review: `hyp:geo-graph-base-transport` at `02:625-640` is tagged HYPOTHESIS and has **zero references anywhere in the corpus** (this was wave-1 finding G2). It is exactly the missing `L_{ij}`-versus-`A` compatibility declaration the roadmap needs. Consuming it closes G2 and the roadmap's gap simultaneously.

---

## 4. Provenance failures

**CRITICAL — the described implementation is not here.** `MAgent_Model-main` returns **zero hits** across both `MultiAgentELBO` copies; it appears only in `Research/` planning documents. And line 158's quotation — "Its README correctly states that the population coupling is an engineered consensus energy rather than the negative ELBO of one fixed population joint" — is checkably false: `grep -ic` for `engineer`, `consensus` and `population` returns **0, 0, 0 in both READMEs**. Lines 156–162 describe code the reader cannot inspect and attribute to it a sentence it does not contain. This is precisely wave-1 finding S6's "31 cited-but-absent evidence paths", reproduced in a new document.

**HIGH — "verified" is unsupported.** Line 174 says "the verified state-level ELBO obstruction". The source `claim-ledger.json` has `assumptions: []`, `evidence: []`, and its sole claim marked **INCONCLUSIVE**; `release.json` has `terminal_status: null`; `final-report.md:10` calls it a "bounded checkpoint". (Coordinator-verified.)

**HIGH — scope overreach on the headline claim.** The obstruction theorem at `PIFB2.tex:3280` requires (a) **frozen** attention rows and (b) a mean-field **product** family. The decision report preserves both qualifiers. The roadmap drops both and asserts it for "the **complete** live-peer action" (lines 9, 166) — while its own T3 plans to eliminate the rows and work with the reduced `-\tau\log Z` functional, which is exactly the regime `PIFB2.tex:3333` says requires a separate test. Wave-1 finding F3 already computed that reduced case (third derivative `-3.54\mathrm{e}{-5}` against a fixed-joint control at `-3.63\mathrm{e}{-65}`) and concluded the stronger claim looks provable but is not yet proved. The roadmap should distinguish frozen from reduced in one sentence.

**Unused proved results.** The roadmap never mentions PIFB2's exact cross-scale Gaussian exception (`PIFB2.tex:3337` — "the ELBO interpretation is exact and the fixed point exists and is unique"), which is the strongest proved exact-ELBO result available and the obvious first case for E5.

---

## 5. Gates that cannot fail

| Gate | Problem |
|---|---|
| **E2 arm 1** | CRITICAL — tautology. A coboundary link has trivial holonomy *as a theorem* (the product telescopes), which the roadmap itself states at line 66. Verified: `\|H-I\|_F = 3.5585\mathrm{e}{-14}`, and **unchanged at `3.5600\mathrm{e}{-14}`** after inserting a `1\mathrm{e}{-9}` singular value (condition number `\approx 1\mathrm{e}9`). The arm measures BLAS round-off and is blind to catastrophic conditioning. Keep it as a convention regression test — it would catch the live ordering defect at `07b:1650` — but do not call it evidence. |
| **E4 arm 1** | HIGH — the counterexample register already proves off-site response is identically zero at `\eta = 0`. |
| **E5 negative branch** | HIGH — "fail to construct" has no stopping rule. A decidable instrument exists and is unnamed: `D^3_{q_iq_jq_j} = 0` identically for any fixed `p_\theta` certifies non-realizability in exact arithmetic. |
| **WP5** | HIGH — labelling every sector "open" passes the gate. |
| **E0, E3, E6, WP2–WP4** | Ungradeable. `grep -ci` over the roadmap returns **0** for each of: tolerance, threshold, effect size, power, p-value, confidence, reachable, feasibility. Thirteen of fifteen gates use a soft verb — match, agree, converge, survives — with no number attached. |
| **E7** | CRITICAL — tunable. See below. |

**On E7 and falsifiability, the blunt answer is no.** A referee counted roughly 26 free parameters (6 scalars, ~13 functions and structures, 7 structural choices) against a demand to "predict more than generic consensus optimization", with no baseline specification, effect size, power, or multiplicity plan. Each proposed observable has an absorbing parameter: correlation length is absorbed by `\eta_q/m_q^2`, consensus rate by the T6 mobility (explicitly left free) and `\tau_q`, scaling by `\tau = \kappa\sqrt{K}` which was chosen to fit, and holonomy response is identically trivial in Regime I. Worse, **defects are topologically vacuous**: the order-parameter manifold is `GL^+(K)/SO(K-1)\simeq S^{K-1}`, and `\pi_n(S^{K-1}) = 0` for `n < K-1`, so at `K_q \in [64, 768]` and `d \le 3` the theory predicts **exactly zero stable defects**.

Only *universal* content survives that parameter freedom: `O(K)`-class exponents, defect classification, Goldstone counting (`\dim G/H`), Ward identities, Mermin–Wagner in `d = 2`. WP6's gate should require a universal prediction. Two cheap decisive tests the roadmap lacks: **front speed** (finite for a Wasserstein/JKO flow, infinite for Fisher–Rao) and **tree-versus-loop overlap graphs** (Bethe is exact on trees, this theory is not).

**Given finding T-04** — the last preregistered experiment froze a threshold that was mathematically unreachable, and burned 40 jobs before anyone checked — every preregistration in this project should require a feasibility certificate first: compute the attainable bound in exact arithmetic and prove the threshold lies strictly inside it, *before* freezing. Ten lines would have voided that experiment. A full checklist is in `rm-05-provenance-gates.md`.

---

## 6. The analysis program: better than feared, with three real traps

**The suspected wlsc obstruction to T4 is a false alarm — do not relax the attention sector.** T3's `-\tau\log Z` is concave in the divergence vector, which looks fatal for weak lower semicontinuity. It is not: `\Phi_\tau` is strictly increasing in each argument and its argument is an *order-zero* function of the sections, so Rellich–Kondrachov upgrades weak `H^1` to a.e. convergence, (nondecreasing continuous)∘(lsc) is lsc, and Fatou closes it. Convexity is needed only in the gradient slot, where the integrand is quadratic PSD and Ioffe's theorem applies. Three hypotheses must be *added*, though: bounded **Lipschitz** domains `U_i` (merely "measurable" breaks Rellich), a **closed proper** isometric embedding of the fiber, and a **fixed** connection.

**Trap 1 — the Gaussian fiber fails the coercivity hypothesis.** `g^F_{\mu\mu} = \Sigma^{-1} \to 0`, so bounded action does not bound `\|\nabla\mu\|_{L^2}`; KL grows only like `\log\det\Sigma`, and is coercive only in the *difference* of its arguments (`\mu_1 = \mu_2 \to \infty` costs nothing). So WP1's exit gate fails on the Gaussian side too — for coercivity reasons, independent of F-2's failure on the categorical side.

**Trap 2 — and this is the crux the roadmap's own line 170 anticipates.** A referee proved: gauge-invariant coercive confinement exists **iff the fiber gauge orbits are compact**. A fixed-point anchor is a Higgs potential breaking `G \to G_{m_0}`. For the current `GL(K)` backend the orbits are noncompact, so **T2 and T4's coercivity are mutually incompatible** — the roadmap's stated failure condition is triggered, not hypothetical. This is the same conclusion F-1 reaches by a different route, which is worth noting: two independent arguments say the structure group must be compact or the action must be amended.

**Trap 3 — curvature, computed not quoted.** Categorical: `K \equiv +1/4`, incomplete (boundary at finite distance), bounded. Univariate Gaussian: `K \equiv -1/2`, complete, unbounded. Multivariate Gaussian `n\ge2`: **mixed** — exactly `+1/4` on every pure-mean plane at every point, `[-1,0]` on covariance planes, `\sup K = 2/7`, `\inf K = -1` at `n=2`. PIFB2's "+1/4 pure-mean" claim is confirmed exactly and is stronger than stated. The direct method is curvature-blind (Morrey 1948), so **curvature does not threaten T4**. It kills **T6**: Eells–Sampson requires nonpositive target curvature and applies to exactly one showcase family, the trivial univariate Gaussian.

Two lucky breaks worth stating as lemmas: both showcase fibers are **contractible** (exponential families have convex parameter domains), so `\pi_2 = 0` and both Bethuel's density obstruction and Sacks–Uhlenbeck bubbling fail to fire in every dimension. And in the `x = 2\sqrt p` chart the categorical case becomes textbook: flat Dirichlet energy into a compact geodesically convex subset of a sphere.

**T9 is not "optional", it is ill-typed for `d \ge 2`.** No reference measure charges `H^1` (a Gaussian free field lives in `H^{1-d/2-\epsilon}`), so `q(c) \in \mathcal M_q` is meaningless pointwise; `d=3` is non-renormalizable and `d=4` is trivial or a Millennium problem. Split it into a finite-mesh statement (elementary) and an explicitly open continuum one.

**Recommended split of T4** into **T4a** (compact fiber, fixed connection — instantiated by the categorical case in the spherical chart) and **T4b** (noncompact fiber, requiring an added gauge-invariant confinement potential — the Gaussian case). That meets WP1's exit gate honestly, via two theorems and an explicit amendment to the action.

---

## 7. Prior art: how much of this is already someone else's theorem

| Target | Status |
|---|---|
| **T0** | **Already done by you, uncited** — `Preprints.org 202505.1773.v1` (May 2025) already has the principal `G`-bundle, two associated bundles, agent as a pair of local sections, induced connection, and a generalized variational energy with KL and a fiber Fisher metric. WP0 is editing, not research. Cite it. |
| **T4** | Substantially **Hildebrandt–Kaul–Widman**, Acta Math. 138:1–16 (1977). The fact the roadmap misses: the Fisher–Rao simplex is a radius-2 spherical orthant with `\Lambda = 1/4` and circumradius `2\arccos(1/\sqrt c) < \pi`, so the regular-ball condition `R\sqrt\Lambda < \pi/2` **holds for every finite alphabet**. Plus Sedláček/Uhlenbeck CMP 86(4):515 (1982) for the Yang–Mills sector at `d=4`. |
| **T6** | Substantially **Loubeau–Sá Earp**, arXiv:1907.06072 / Ann. Glob. Anal. Geom. (2023), following Wood (2003): uniqueness, smoothness, short-time existence and long-time conditions for the Dirichlet gradient flow **on sections of homogeneous fibre bundles**. `GL(K)/O(K)` is homogeneous, so it applies to your actual code almost verbatim. WP2 is largely redundant. |
| **T2** | Cohen arXiv:1902.04615, Weiler arXiv:2106.06020, and Cassel et al. SSVM 2025 — node features as sections of associated bundles with local gauge equivariance and harmonic-section fixed points. One proposition, not a chapter. |
| **T3** | **GENUINELY NEW** — the only one. Pointwise softmax-as-entropic-OT is published; attention weights as *fields on overlaps* eliminated by an envelope theorem inside a continuum action returned nothing across the referee's searches. |
| **T8** | Most expensive and least supported. The right import is García Trillos–Slepčev `\Gamma`-convergence, all of it scalar-valued; manifold-valued plus gauge is genuine new work. A discrete Uhlenbeck gauge-fixing theorem does not exist. |

**The nearest competitor, settled.** Cassel, Boll, Petra, Albers, Schnörr, *Sigma Flows for Image and Data Labeling*, arXiv:2408.15946, JMIV 2025. Their setup is a harmonic map from a Riemannian domain into the Fisher–Rao simplex — the roadmap's Dirichlet sector almost exactly. But: no bundle (a plain map into a fixed manifold), no gauge group, no principal connection, no `F_A`, and **no existence theorem** — §1.3 says explicitly that their scenario violates the standing assumptions and they "leave the problem of existence and global convergence of the gradient flow for future work." They prove only a Lyapunov decrease. T4 is not their theorem.

The strategic warning: **the Heidelberg group holds both halves.** Fisher–Rao harmonic maps (arXiv:2408.15946), associated-bundle local-gauge harmonic sections (SSVM 2025), and a discrete Yang–Mills energy on data bundles (*Yang–Mills Meets Data*, arXiv:2510.19431) — three papers, overlapping authors, eighteen months, funded. The merge is their obvious next paper.

---

## 8. Recommended revision

**Before touching the roadmap:**

0. Cite `Preprints.org 202505.1773.v1` and the four self-citations already sitting uncited in `references.bib`.
1. Fix line 174: replace "verified" with the ledger's actual `INCONCLUSIVE`; delete or relocate lines 156–162 until the described implementation is in the repository; correct the false README quotation.
2. Distinguish frozen-`\beta` from reduced-potential in the headline claim (one sentence).

**Structural amendments to the plan:**

3. **Resolve F-1.** Adopt the Fisher-dressed curvature `g^F(F\cdot q, F\cdot q)`, or declare `G` of compact type in T0. Either way, delete the claim at line 13 that compactness is merely analytical.
4. **Resolve F-2.** Replace the categorical showcase with `\mathrm{SPD}(K)` under `GL(K)` congruence, or let `G` depend on the fiber. Then state the good news: `GL^+(K)\ltimes\mathbb R^K` is the *full* isometry group of the Gaussian Fisher–Rao metric, so the implementation's group is maximal rather than arbitrary.
5. **Fix T2's verb** — equivariance on the full datum, observables on `\mathcal M/G` — and add the non-transitivity axiom to T0, with the population-quotient dimension count as the escape that actually carries the weight.
6. **Split T4** into T4a (compact fiber, fixed connection) and T4b (noncompact fiber plus a gauge-invariant confinement potential), and add the three missing hypotheses (Lipschitz domains, closed proper embedding, fixed connection).
7. **Rewrite line 174's source boundary** to include `Theory/`, collapse WP0 to the three-item delta, and cut WP1 to T4 alone. Consume `hyp:geo-graph-base-transport` (`02:625-640`) as the `L_{ij}`/`A` compatibility axiom.
8. **Put numbers on every gate.** Retire E2 arm 1 and E4 arm 1 as regression tests rather than evidence; give E0/E3/E6 tolerances and E3 a convergence *rate*; require a *universal* prediction at WP6; add the front-speed and tree-versus-loop tests. Adopt a feasibility certificate as a mandatory precondition for any frozen threshold.
9. **Demote T9** to a finite-mesh statement plus an explicitly open continuum problem.
10. **Insert a defect gate ahead of WP0.** The roadmap adds ~25 obligations and discharges none of the ~40 outstanding. At minimum, fix the `03:391` hypothesis error, retag `07b`, and repair the three test fixtures that E1/E2/E7 depend on — the involutive `gauge_fixture`, the doubly-stochastic `adjacent_pairs` scheme, and `confirmatory_analysis.py` at 5/15 mutation score — since those experiments cannot mean anything until they are fixed.

**And the strategic recommendation, which every referee independently reached:** extract `05c_pullback_geometry.tex` first. It is 1,392 lines, 24 numbered results, all proofs closed, no TODOs — finished. It survived every novelty search. It is already continuum. And it contains **no free energy**, which is why all four of the parent audit's structural criticisms pass it by. Ship it in weeks; then a short second paper on T3 alone at `d \le 1`, paired with `prop:obs-attention-elbo` (`05b:547`); then, if at all, the continuum program scoped to `d = 2`, where T4 and T5 become citation-plus-lemma and T6 comes from Loubeau–Sá Earp.

---

## Coordinator verification log

| Claim | Check | Result |
|---|---|---|
| Yang–Mills contraction impossible for `GL(K,\mathbb R)` | Enumerated `Ad`-invariant forms `a\,\mathrm{tr}(XY)+b\,\mathrm{tr}X\,\mathrm{tr}Y` on `\mathfrak{gl}(K)`, `K=2,3,4`; eigenvalue ranges; `Ad`-invariance of Frobenius vs Killing | No positive-definite invariant combination at any `K`. Frobenius PD but not invariant (`-4.859 \to -66.31`); `\mathrm{tr}(XY)` invariant but indefinite. **Confirmed, two referees independently.** |
| `MAgent_Model-main` absent | `grep -ril` across all three mounts | Zero hits in both `MultiAgentELBO` copies; appears only in `Research/` planning docs. **Confirmed.** |
| Line 158's README quotation | `grep -ic engineer\|consensus\|population` on both READMEs | **0, 0, 0 in both.** The quoted sentence does not exist. **Confirmed.** |
| "Verified" obstruction | Read `claim-ledger.json` | `assumptions: []`, `evidence: []`, sole claim INCONCLUSIVE. **Confirmed.** |
| Repo divergence | `git log` both copies | Same repository; ChatGPT copy is exactly one commit ahead (`24c02aa` on `c101b8a`). `git diff --stat aedc662..24c02aa -- src tests tools Theory` is **empty**. **Confirmed.** |

**Correction to my own tasking.** In briefing the provenance referee I attributed the frozen-versus-reduced obstruction finding to `wave2-01-constructions.md`. It is wave-1 finding **F3**, at `2026-08-11-ultradeep-expert-audit.md:136` and `ultradeep-2026-08-11/audit-02-infogeometry.md:139-165`. The referee caught the misattribution and verified the numbers were right regardless. Recorded here because an audit that does not audit itself is worth little.

Per-referee reports: `rm-01-audit-reconciliation.md`, `rm-02-existence-analysis.md` (841 lines), `rm-03-action-class.md` (581 lines), `rm-04-gauge-kinematics.md` (996 lines), `rm-05-provenance-gates.md`, `rm-06-prior-art.md`.
