# Ultradeep multi-expert audit — wave 2

Date: 2026-08-12
Predecessor: `docs/audits/2026-08-11-ultradeep-expert-audit.md` (wave 1, same session)
Execution policy: CPU only. **No GPU or CUDA job was started**, and the CUDA test lane was excluded from every mutation run, per instruction.

Wave 1 mapped the corpus and found four structural problems. Wave 2 was aimed at what wave 1 could only flag: it attempted the missing constructions rather than describing them, checked proofs rather than identities, tried to break theorems rather than re-derive them, read the two largest chapters properly, mutation-tested the modules wave 1 skipped, and established priority against the literature.

Wave 2 also **corrected wave 1 in four places**. Those corrections are recorded in full below, because an audit that does not audit itself is worth little.

---

## The finding that outranks everything else

**You appear to have a public priority date on the project's central construction, and you are not citing it.**

The reviewing agent located **Robert C. Dennis, "Epistemic Gauge Theory," Preprints.org 202505.1773.v1, 23 May 2025, DOI 10.20944/preprints202505.1773.v1**, and quotes its abstract:

> "…pullbacks of geometric quantities unique to each agent. Agents are constructed as pairs of local sections of associated bundles `E_i` to a principal `G`-bundle `N` composed of a base manifold `C` and Lie group `G`. Agents interact via induced connections and evolve according to a generalized variational energy."

That is this project's goal sentence, published, dated May 2025.

Coordinator verification: the Preprints.org record **resolves** (the page fetched successfully at 81,938 characters, though too large to read in full in-session). A case-insensitive search for "epistemic gauge" across all `.tex`, `.bib` and `.md` files in **both** `MultiAgentELBO/` and `Research/` returns **zero hits**. There is no corresponding entry in `references.bib`.

Separately and fully verified: `references.bib` contains four self-citations — `Dennis2025it` (which is PIFB2 itself), `dennis2025inertia`, `Dennis2025trans`, `Dennis2026metaentropy` — and **every one is cited zero times in `Theory/`**.

Two consequences, and the second is the serious one. First, the priority date for the core construction is May 2025, not 2026, which is good news you are discarding. Second, a referee who finds a 2025 preprint by the same author containing the same construction, uncited, will not read it as an oversight. Please confirm the preprint is yours and add it, along with the other four self-citations, before anything else in this report is acted on. This is a fifteen-minute fix with an asymmetric downside if skipped.

---

## Wave 2 verdict

Three results dominate.

**The red team could not break anything.** After systematic attacks on non-compactness, KL asymmetry and infinities, non-commuting generators, coarse-map composition, obstruction scope, and quantifier order, **no object was found that satisfies every hypothesis of a stated `Theory/` theorem and violates its conclusion**. Every defect the red team found lies in the code's numerical domain, not in a theorem. Combined with wave 1's sixty verified identities and wave 2's proof-level pass, the mathematics should now be regarded as genuinely sound. That is an unusual thing to be able to write about a manuscript of this size.

**But the central construction is not merely missing — it is partly impossible, and now provably so.** Wave 1 reported that the free energy is never a functional of a section. Wave 2 attempted the construction and got a theorem instead: the three properties the object needs cannot hold together. Details in the next section. This converts wave 1's largest open item from "hard work remaining" into "the specification must change", which is more useful.

**The proof-level pass found one real error**, in a proposition wave 1's identity-checking could not have caught, because the algebra is fine and the hypothesis is wrong.

---

## W1 — Theorem A-NOGO: the section-valued free energy cannot have all three required properties

The construction was attempted on the tier the manuscript itself exhibits at `05d:235` (`P = \mathcal C \times G`, `G = (\mathbb R^K,+)` abelian, flat `\omega`, constant Gram metric). Two of the four requirements were **achieved with proof**, and two were shown to be **unachievable together**.

**Achieved.**
- *Frame independence* (requirement A2) is proved — and at the *measurable* tier, which is stronger than asked. It needs only that `\hat\rho` is pushforward along a bimeasurable bijection, that `\pi` is a section, and that `E` is a section of the associated function bundle, the last being exactly `eq:gen-gauge-pushforward-obs`. It survives a jet term. Frame independence is not the obstacle.
- *Consistency with the finite-design ELBO* (A4) is proved as an **exact identity**, and it replaces `hyp:prob-sampling-compatibility` — the hypothesis wave 1 identified as the broken bridge — with a theorem, because the section is *constructed from* `Q_X` rather than posited alongside it:

  `\Fenergy[Q_X;X,o] = \int f(c, s_Q(c))\, d\mu_D + \mathrm{TC}_D(Q_X)`, with `\mathrm{TC}_D = \KL(Q \| \bigotimes_a Q_a) \ge 0`, equality iff `Q` is design-product.

  Verified numerically: residual `1.4e-14`; control with product `Q` gives `\mathrm{TC} = 0` exactly. **This single identity also delivers wave 1's shortest-path item 5** (local-to-global over `\mathcal C` with an exact defect).

**Impossible.**
- **O1 — gauge invariance forces constancy.** The Gaussian belief fiber `\mathcal B = \{N(m,\Sigma_0)\}` is a **`G`-torsor**, so `\mathcal E_b \cong P`, and `\mathrm{Aut}_G(P)` acts **simply transitively** on `\Gamma(\mathcal C, \mathcal E_b)`. Every `\mathrm{Aut}_G(P)`-invariant functional on sections is therefore **constant**. The general criterion is proved: `\mathcal F` is invariant iff its integrand descends to `\mathcal B/G`. The classification is explicit — for `G = (\mathbb R^K,+)` an invariant free energy sees only the covariance field and is blind to the mean; for `G = GL^+(K)`, `\mathcal B/G \cong [0,\infty)` via `r = (\mu^\top\Sigma^{-1}\mu)^{1/2}`.
- **O2 — finite-design consistency forces a jet-free integrand**, and therefore forces the connection *out* of the free energy. Deformation witness: `\chi` vanishing on `D` with `\chi'|_D = (8,-4,8)`. Independently confirmed by the manuscript's own `H^1` counterexample at `05d:344-353`: the `L^2`-Fisher metric is `C^1` only for jet-free objectives.

**Statement.** *No functional of the form `\int f(c, s, D^\omega s)\,d\mu` on sections is simultaneously gauge-invariant, consistent with the finite-design ELBO, and non-constant with genuine connection dependence.*

**What this means for the program.** Requirement (b) should be restated as **equivariance** on the triple `(s,\pi,E)` — which is true and provable — rather than invariance, with the explicit acknowledgment that the background carries a gauge fixing. And **O2 upgrades wave-1 finding S3 from an observation to a necessity proof**: the connection is absent from the free energy not by oversight but because putting it there breaks finite-design consistency. The one surviving route for `\omega` is to require `D^\omega\pi = 0`; a parallel background exists iff `\mathrm{Hol}(\omega) = \{e\}`.

Two further obstacles were found (no canonical base measure, which also contradicts the manuscript's own N1 at `12_philosophy:33-38`; and off-design non-identification, repairable only by unisolvence, which reduces "section space" to a relabeling of `\mathbb R^N`). Three suspected obstacles were **dismissed with proof**, including the important one: `\rho` *is* automatically a Fisher–Rao isometry, following from the manuscript's own pushforward declaration (verified `2.9e-15`, with a firing control).

## W1b — The noumenal theorem N3(a) is proved, and its converse is the interesting part

N3(a) is proved in three steps from `prop:gen-product-evidence-invariance` and `hyp:gen-kernel-covariance`. Numerical witness: records **pathwise** identical to `9.9e-14` over `4\times10^5` draws while the latents move by `136.2` and satisfy `y' = Ry`; a control violating `eq:gen-gauge-pushforward-obs` alone fires at `192.9`. A paste-ready SPEC-compliant LaTeX section (`sec:phil-record-indistinguishability`) is in the wave-2 report: 2 definitions, 1 theorem with full proof, 2 corollaries, 1 proposition, 1 open problem, 11 status tags, zero banned phrases, zero bullets, verified programmatically.

The converse is where the content is. The map from bundle data to record laws has an **enormous fiber**: the gauge orbit (F1), the *entire* connection space (F2 — `\omega` is not an argument of any generative kernel), all sections agreeing on the design (F3), and **all principal `G`-bundles** (F4 — every bundle is trivial over a finite set; witness `\mathcal C = S^2`, `G = U(1)`, Hopf bundles of distinct Chern number giving identical record laws). The map does not separate Chern classes.

**Be careful with the philosophy.** The theorem does *not* license "the substrate is inaccessible". It holds because `\omega` is not in the likelihood and the design is finite — both features of the declared model, not discoveries about reality. Under chapter 12's own idle-wheel criterion it is an argument for *removing* the bundle from the empirical content, not for noumenality. What it does deliver, concretely: it **closes the ledger's "Operational base holonomy (open)" negatively for all finite designs**, and should be restated for refining designs.

## W2 — Proof-level verification: one error, four gaps, three silent hypotheses

Twenty proofs were read line by line. **Nothing circular was found anywhere.** Ratings: 12 PROOF COMPLETE, 3 GAP, 3 SILENT HYPOTHESIS, 2 ERROR, 1 proves a different statement.

**The error — `prop:prob-marginals-do-not-determine-joint`, `03_probability.tex:391`, top severity.** The stated hypothesis is that `Y_D` contains at least two nondegenerate real *coordinates*, but `def:prob-recognition-marginals` (`03:385`) marginalizes onto **blocks** `pr^k_{i,a}: Y_D \to K_{i,a}`, not scalar coordinates. The proof's step "embedding this pair in any two coordinates of `Y_D`" is false when both coordinates lie inside one block. Counterexample satisfying the stated hypothesis: `|V| = 1`, `M = 1`, `K_{1,1} = \mathbb R^2`, `M_{1,1} = \{0\}` — two nondegenerate real coordinates exist, yet the marginal family is `\{q_{1,1}, \delta_0\}` with `pr^k` a bimeasurable bijection, so it determines `Q_X` exactly. Verified: the manuscript's own witness pair has identical scalar marginals but block marginals at `\KL = 0.3393564486857903`. Repair: require two nondegenerate **blocks**. This propagates to `prop:prob-compatibility-nonidentifiability`(i), `03:387`, and `05_elbo:32`. A secondary defect in the same proposition: the statement reads universally, the proof is existential, and the universal version needs a condition on the *law* (at least two non-Dirac block marginals), not on the space.

**Gaps.**
- `thm:pb-pullback-gauge-invariance` (`05c:124`): `eq:pb-covariant-jet-gauge-law` is the entire content and is asserted, not derived. Deriving it needs the chain rule on `c \mapsto \hat\rho(g(c))^{-1}\beta(c)` plus `T\hat\rho(g)\circ\zeta_\xi = \zeta_{\mathrm{Ad}_g\xi}\circ\hat\rho(g)`, with the `g^{-1}dg` term cancelling against `dg`. Also `\omega'` means the gauge-transformed local representative here but a genuinely different principal connection at `05c:160`, **where the theorem is false**. Clean repair available: `D^\omega s = \mathrm{ver}^\omega\circ Ts` is frame-free, and so is `g^F`, making the theorem immediate in two lines.
- `prop:gen-product-evidence-invariance` (`04:408`): the induction has no base case. "Apply along the topological ordering" starts at a root, and the root covariance identities are never displayed — `hyp:gen-kernel-covariance` ends "with the analogous root identities" (`04:399`). **This matters disproportionately**, because N3(a) is built on this proposition.
- `prop:obs-attention-elbo` (`05b:547`): "Lagrange multiplication proves it" establishes neither uniqueness nor interiority. Exact repair supplied and verified to `8.9e-16`: `F_i^{\mathrm{att}}(\beta) = \KL(\beta\|\beta^*) - \log Z`.
- Hopf failure witness (`07:263-266`): `\kappa_\ell` is unspecified and the claim fails for trivial `\kappa_\ell`. Repair: specify `\kappa_\ell = \mathrm{id}_{U(1)}`. The iff itself was verified correct in both directions.

**Silent hypotheses.** `def:rg-geometric-state` (`07:153`) asserts induced horizontal distributions on the associated bundles, which requires smooth fibers and smooth actions — but `hyp:geo-smooth-tier` is referenced only in chapters 2 and 5c, never in chapter 7. Parallel transport survives without it; horizontal distributions do not. The `05b` descent corollary (`05b:670-700`) presupposes `\mathbb E_{Q_{B^c}}|\log Z_B| < \infty`, and `F \in C^1` gives Peano existence but not uniqueness, so "the trajectory" is unlicensed.

**Adjudication of wave-1 finding F4 (definitions dressed as theorems): partially upheld, and softened.** The boxed displays are indeed definitions, but each environment also asserts the range, the identification, and the bound with its equality case — a genuine one-line proposition. `thm:obs-local-multiagent-elbo` additionally restricts to `R_{B,o}`, whose fullness is proved nontrivially at `05b:262-272`. Correct verdict: a definition and its immediate corollary merged into one environment, not a vacuous theorem. Separately, both cite `thm:elbo-extended-gap` outside its literal (H1)–(H2) hypotheses; the transfer is sound but unchecked.

**`prop:obs-declared-root-unavoidable` proves a different statement.** With exogenous `X`, every latent can have a parent and its factor is not unconditional. What holds is that some latent has no *latent* parent. Two-word repair; the section's use of it is unaffected.

**Unused hypotheses** (each suggesting the result is stronger than stated): standard Borel in `thm:rg-strong-lumpability`; `\Theta_i \in GL^+(K)` in `thm:obs-star-fixed-point-contraction` (verified to hold with `\Theta_1 = 0`); `Q_o \ll \Pi_o` in `thm:rg-exact-coarse-vfe`; positive-definite Fisher in `prop:pb-statistical-tensor-descent`.

## W3 — Red team: no break, and one calibration defect worth fixing

Explicit "no break found" on non-compact `G`, KL asymmetry and infinities, non-commuting `\phi`, coarse-graining composition, obstruction scope, and quantifier slips, and on chapters 6, 7, 7b, 8, 9 and 11.

**F-1 (HIGH) — the conditioning gates are not calibrated to the tolerance the results are graded at.** `prop:ig-generalized-spectrum-invariance` is exactly true, and `apply_frame_change` implements it with `max_frame_condition = 1e6` and `min_spd_rcond = 1e-12`, while `experiment.py` grades the residual at `atol + rtol = 1.01e-10`. Two witnesses in which **all gates pass**:

| witness | residual | multiple of tolerance |
|---|---|---|
| frames at cond `1e5` (limit `1e6`), ordinary interaction | `8.514e-08` | **843×** |
| precision rcond `1e-11` (gate `1e-12`), *orthogonal* frames (cond 1) | `3.384e-06` | **33,500×** |

In the second case the reported invariant moves in the fifth significant digit under a mere rotation. Measured safe ceilings: frame condition `\approx 3e3` (300× below the declared limit) and `min\_spd\_rcond \approx 1e-7` (five orders above the declared value).

**F-2 (MED-HIGH)** — `GAU-01_eigenpair_residual` cannot certify the spectrum: it is a backward error normalized by `\|v\|`, and `\Lambda`-orthonormal eigenvectors inflate `\|v\|`. At frames of condition `3e5` it reads `3.249e-17` while the true forward spectrum error is `1.850e-06`. Mitigating and worth recording: `metric_orthogonality_residual` fires in *every* failing case, so the red team could produce **no silently wrong published number**.

**Robustness evidence, which deserves to be recorded as such.** Across 350,236 comparable partition pairs there were **zero** violations of refinement monotonicity, gap nonnegativity, or the exact equality condition, with block-min KL and determinant gap agreeing to `1.78e-15`. The Fisher identity residual is **exactly 0.0** with a subnormal `5e-324` atom. Chain rule at `4.16e-17` with zero atoms, and correct `inf`/`None` branches when the fine KL is infinite and the coarse KL finite. `parameter_dependent_channel_fixture` has zero fine Fisher and positive pushed Fisher and *would* refute `thm:cg-fisher-contraction` — except the channel is parameter-dependent, and the record is correctly tagged `assumptions_satisfied=False`, enforced in `CandidateRecord.__post_init__`. One apparent violation of `eq:obs-star-rate` was self-refuted as a float64 noise-floor artifact.

## W4 — Chapters 05d and 07b: most of the corpus's largest chapter is terminal

| | `05d` (1,624 lines) | `07b` (2,828 lines) |
|---|---|---|
| Formal results | 29 | 35 |
| With a mathematical consumer outside the chapter | **6 (20.7%)** | **5 (14.3%)** |
| Referenced nowhere in the corpus | 15 | **26** |
| Referenced nowhere even internally | 4 | **12** (including 2 theorems and the final corollary) |
| Lines in a section with any external consumer | ~700 (43%) | **752 (26.6%)** |

Four of `07b`'s five external consumers are a single file, `08_infogeometry.tex`.

**07B-S2 (HIGH) — `07b` carries ZERO `\status{HYPOTHESIS}` tags in 2,828 lines.** Coordinator-verified: 81 ESTABLISHED, 10 DEFINITION, 1 OPEN, 1 NOT-CLAIMED — 87% ESTABLISHED, and no hypothesis tag at all. Twelve restrictions adopted by choice were enumerated (semigroup compatibility, product equivalence at both scales, retained-projection intertwining, tempering, Bochner domain, Schauder basis, the Krein–Rutman resolvent assumption, and others), none tagged. For comparison, `05d` carries 11 HYPOTHESIS tags and `09` carries 3. Given that wave 1 praised the corpus's tag discipline as exemplary, this chapter is the conspicuous exception and should be retagged before anything else in it is trusted.

**07B-S4 (HIGH) — strip the agent language and nothing agent-specific survives.** `\Fenergy` appears on **2 lines out of 2,828**, both in the first theorem. "Agent" appears on 19. The entire gauge and graph sector is lines `1619–1743` — roughly 130 lines — in which `\Theta_e` appears **once** and `\pi_1(` appears **once**, used in zero other sections and zero other files. What remains is Markov-kernel coarse-graining, done well. `thm:rg-strong-lumpability` and the 90-line Mori–Zwanzig `thm:rg-projection-memory` have zero references anywhere.

**05d verdict: favorable.** "History" is well-typed (a `C^1` representative into a declared regular space, quotiented by orientation-preserving `C^1` diffeomorphisms, with self-intersections retained). Fisher arc-length reparameterization invariance was verified by explicit computation, and the `\phi' > 0` step is genuinely load-bearing and correctly flagged. `hyp:hist-exact-vfe-lift` is invoked exactly once (`05d:518`), correctly and conditionally, and **the OPEN status of the global clock is honored everywhere** — `T` is constructed only inside the conditional and never used again, and `05d:1609-1614` refuses the identification explicitly. One real defect: `thm:hist-global-clock-exactness` **delivers no clock** — its first biconditional is a tautology (the definition of exact), the criterion is Poincaré's, and the one worked instance *fails* it. A consequence of the single `C^2` hypothesis at `05d:227` plus a constant Gram metric is that all seven theorems of §§4–10 (1,104 lines, 68% of the chapter) are gradient-flow arc-length calculus for an arbitrary `C^2` function on `\mathbb R^N`.

**Notation drift** (the failure mode `SPEC.md` exists to prevent): `\Theta`, `\Phi` and `\tau` each carry three to six incompatible meanings that collide with SPEC-fixed uses — `\Theta^\ell_g` as an affine map at `05d:259` and `\Theta_\ell f = f\circ\vartheta^{-1}` at `07b:1262` against SPEC's `\Theta_e^x \in G`; `\Phi` as a Gram matrix at `05d:282` against the cross-bundle morphism; `\tau` as Fisher clock, `G`-valued transport, softmax temperature, and tier label. Fifteen drifts are tabled with file:line on both sides in the wave-2 report.

**Sign check:** all 42 exponentiated actions in `07b` are `e^{-H}`; zero `e^{+H}`. No analogue of wave-1's RG-8.

## W5 — Mutation testing: 78.8%, with a concentrated failure

**Overall mutation score 93/118 = 78.8%**, run entirely in a scratch copy at `/tmp/mae`; the user's repository was verified unmodified afterwards.

Baseline honesty: 891 tests collect; 125 fail, and **all 125 failures are environmental** — 32 are literally `FileNotFoundError: 'C:\anaconda\python.exe'`, plus hardcoded `C:\Python314\python.exe`, `ctypes.WinDLL`, and a missing preregistration document. The primary oracle was therefore a 21-file mathematics lane of 476 tests with zero baseline failures.

Perfect scores (100%): `attention.py`, `categorical.py`, `agent_network.py`, `discrete_holonomy.py`, `categorical_dqm.py`, `counterexamples.py`, `theory_oracles.py`.

The failure is concentrated:

| Module | Score | Notable survivors |
|---|---|---|
| `confirmatory_analysis.py` | **5/15** | sign-test tail reversed; **Holm → Bonferroni**; `<=` → `<` at the frozen `-0.02` boundary; two-sided factor 2 dropped; **95% → 90% CI**; half-width `/2` dropped; bootstrap median |
| `finite_gauge.py` | **2/6** | `P^\top CQ \to PCQ`; two transposes; `m@P \to P@m` |
| `information_history.py` | **5/10** | rank counts `\|\lambda\|`; symmetrization dropped; condition number inverted; `used_pseudoinverse` always True |

The statistical layer of the flagship confirmatory analysis is the least protected code in the repository: **you could silently swap Holm for Bonferroni, halve the confidence interval, or reverse a test tail, and no test would notice.**

Three survivors have verified structural root causes rather than merely missing tests, and each has a one-line fix:
- All four permutations in `gauge_fixture` are **involutions** (`old_to_new == new_to_old`, `matrix == matrix^\top`), so gauge *direction* is undetectable by construction. One non-involutive fixture kills all four `finite_gauge` mutants.
- `adjacent_pairs` is **doubly stochastic**, so every finite difference is exactly orthogonal to the Perron ray and the projector removes nothing — `\|(I-P)d\| == \|(I-6P)d\|`. The other frozen scheme, `balanced_alternating`, would expose it.
- The Hoeffding fixture is symmetric about zero, so the quotient seminorm `(\max-\min)/2` is indistinguishable from the sup-norm.

**Three more cannot-fail assertions**, in the style of wave-1's N-02: `positive_definite: minimum_diagonal > 0` where `minimum_diagonal = Fraction(1, 10**100)` is a constant, so the test asserts that `1/10^{100} > 0`; and `inside_declared_domain` / `assumptions_satisfied` are boolean **literals** at all four call sites, asserted `is True`, with zero `=False` occurrences in tests.

**The coverage-versus-mutation gap is the instructive number.** Line coverage is 86% and flat (80–100%); mutation score is bimodal. `confirmatory_analysis.py` is 80% covered but only 33% mutation-killed; `finite_gauge.py` is 90% covered and 33% killed; `permutations.py` has 100% line coverage and 83% mutation score, while `agent_network.py` has 82% coverage and 100% mutation score. Line coverage ranks these two backwards; mutation testing corrects it. Track the latter.

The reviewing agent discarded two of its own mutations as invalid no-ops rather than counting them as survivors — the right call, and worth noting as evidence the number is honest.

## W6 — Novelty: three claims survive, six die

**Survive, ranked.**
1. **The horizontal-defect calculus** — `thm:pb-anomaly-composition` (`05c:979`), `thm:pb-fisher-defect-cocycle` (`05c:1230`), `thm:pb-base-defect-cocycle` (`05c:1267`). No prior art after eight logged searches. The sign-convention theorem — that mixing conventions inflates the residual by exactly `2\Delta_F(A,A)` — is the signature of a real derivation rather than a restatement.
2. **The exact connection-dependence of `h_s^\omega`** (`05c:156-232`) with its counterexample, against passive-only gauge covariance. A negative result about the author's own framework, very well defended, and the sharpest available critique of Sengupta–Friston.
3. **The holonomy factorization of the Gaussian normalizer** (`11:120`, `11:355`) and the holonomy-constrained barycenter (`09:700`).

**Die.**
- The pullback framing itself is **definitional**: Ay–Jost–Lê–Schwachhöfer, *Parametrized measure models*, Bernoulli 24(3) 2018, arXiv:1510.07305 — "a natural definition of the Fisher metric and the Amari-Chentsov tensor as the pullback of tensors." Already in your bibliography.
- `\mathrm{ver}^\omega\circ Ts` plus a fiber metric is **harmonic sections**: C. M. Wood, *Differential Geometry and its Applications* 19(2):193–210 (2003); the vertical energy is `\mathrm{tr}_g h_s^\omega`. Also gauged sigma models.
- A field of Fisher–Rao fibers over a base is an **active ML programme**: Schnörr et al., sigma flow, arXiv:2408.15946 — "harmonic map from a Riemannian domain manifold to a statistical manifold with the Fisher-Rao metric". The assignment flow (JMIV 2017) is the discrete version. This is the nearest live competitor and it is not cited.
- **Chapter 2 is Cohen ICML 2019 (arXiv:1902.04615) / Weiler arXiv:2106.06020, item for item**, with a nonlinear statistical fiber in place of a vector fiber. The difference is real but small. Damage: HIGH.
- `prop:obs-declared-root-unavoidable` is "every finite DAG has a source" — textbook (Lauritzen 1996 §3, already cited twice). Demote to a remark.
- `cor:obs-flat-fold-singular` is **IGMRF impropriety**: Besag & Kooperberg, Biometrika 82(4):733–746 (1995); Rue & Held 2005, ch. 3.
- `prop:cg-markov-category` is `BorelStoch`: Lawvere 1962 / Giry LNM 915 (1982).
- Fisher contraction: Čencov owns uniqueness, AJLS the monotonicity formula, and **Bény–Osborne PRA 92:022330 own the RG framing chapter 9 actually uses** — in your bibliography, cited zero times.

**Sengupta–Friston, read in full** (PLoS Biol 14(3):e1002400, 2016, plus arXiv:1705.06614): it is a **programmatic essay**. The "manifold" is one agent's sufficient statistics, the "connection" is the Levi-Civita connection of the Fisher metric, and the "gauge field" is precision/attention. There is no base, no structure group, no principal bundle, no sections, no curvature, no multi-agent structure, and **no theorem**. Their usage is arguably a category error — Levi-Civita is not a gauge field — and saying so precisely is the clearest available justification for `Theory/` existing at all. But `Theory/`'s own gauge sector is currently inert (wave-1 S3, now strengthened by W1's O2), so write that comparison and fix curvature together, or a referee will make the point for you.

**Positioning sentence, as drafted:**

> We show that the geometry a belief field induces on its context space is gauge-covariant but not connection-independent, and we compute the exact defect: a horizontal-defect calculus with a closed composition law, an unconditional vertical Fisher cocycle, and a sharp base-cocycle residual.

**The better paper hiding in here.** *"Connection-relative informational pullbacks: gauge covariance, connection dependence, and a horizontal-defect calculus"* — essentially `05c` verbatim, to *Information Geometry* or *Differential Geometry and its Applications*. Note what this does: **all four of wave 1's structural criticisms attack the free-energy layer**, and this paper contains no free energy. No base integral, no gluing, no noumenon, no philosophy. It is also the only place in the corpus where wave 2 found unanticipated mathematics. A second extraction is `prop:obs-attention-elbo` (`05b:547`) — exact row softmax from a latent source label — flagged probably-novel but not exhaustively searched.

---

## Corrections to wave 1

Recorded in full. Four wave-1 items were wrong or overstated.

1. **RG-7 (PIFB2 barycenter equivariance) — overstated; downgrade MED/ERROR to LOW/citation-scope.** The forward-KL Gaussian barycenter is *exactly* equivariant under all of `GL^+(K)` — no compactness required, not even `|\det g| = 1` — because KL is invariant under a common invertible pushforward. Verified along an unbounded family with `\|g\|_2` up to `2.7e45`: relative equivariance error at machine epsilon, score gap `\le 5.2e-13`. PIFB2:1577 already says this. The remaining defect is only that PIFB2:1559 and :1644 cite a compact-`G` theorem for it.
2. **RG-8 (sign inconsistency at `06:320` vs `06:392`) — misclassified; ERROR becomes notation drift.** `\bar E` at `06:320` is an energy; `\mathcal E_\theta` at `06:392` is a natural-parameter pairing (`def:cg-graph-exponential-energy`, `06:345`), so `e^{+\mathcal E}` is correct there. The defect is symbol reuse, not a sign error.
3. **The Čencov recommendation was wrong. Do not act on it.** Wave 1 listed "Fisher-necessity via Chentsov" as an easy win. Čencov **is** cited and handled *well* at `08:493-515`, including an honest statement of why it does not apply directly to `\mathbb R^n` latents (coordinator-verified). The theorem that *does* apply, and which is genuinely missing, is **Bauer–Bruveris–Michor**, Bull. LMS 48(3):499–506, arXiv:1411.5577.
4. **The Bethe/Kikuchi comparison for `thm:obs-local-global-potential` was wrong.** Region graphs are approximations with counting numbers; this is an exact two-term chain rule. The correct owners are blocked/structured coordinate-ascent variational inference: Saul–Jordan 1995, Jordan et al., *Machine Learning* 37 (1999), Wainwright–Jordan 2008 §5 — all already in your bibliography. The increment is generality only. Relatedly, the real Fritz overlap is not `prop:cg-markov-category` but the sufficiency and DPI-equality results in `sec:cg-kl-recovery` (Adv. Math. 370:107239, arXiv:1908.07021).

One wave-1 finding was **softened**: F4's "definitions dressed as theorems" is better described as a definition merged with its immediate corollary (see W2). One was **strengthened**: S3's inert gauge sector is now backed by a necessity proof (W1's O2), not just an observation. And one wave-1 praise item **held up under re-measurement**: the tolerance discipline in `tests/` — a grep for tolerances `\ge 1e-3` returns zero in wave 2 as well.

---

## Revised path forward

Wave 1's list, corrected by wave 2. Ordered by value per unit of effort.

**Do first, this week.**
0. **Cite the 2025 preprint and the four self-citations in `references.bib`.** Fifteen minutes; asymmetric downside if skipped.
1. **Fix `prop:prob-marginals-do-not-determine-joint`** (`03:391`): change "coordinates" to "blocks", and add the law-level condition for the universal reading. Propagate to `03:387`, `prop:prob-compatibility-nonidentifiability`(i), and `05_elbo:32`.
2. **Retag `07b`.** Eighty-one ESTABLISHED and zero HYPOTHESIS in 2,828 lines is the single largest breach of your own contract, in the corpus's largest chapter.
3. **Close the four proof gaps** — `05c:124` (two lines, using the frame-free form), `04:408` (display the root identities; N3(a) depends on it), `05b:547` (the supplied `\KL(\beta\|\beta^*) - \log Z` identity), `07:263` (specify `\kappa_\ell = \mathrm{id}`).
4. **Recalibrate the conditioning gates** to the tolerance results are graded at: frame condition `\approx 3e3`, `min\_spd\_rcond \approx 1e-7`. Replace `GAU-01_eigenpair_residual` with a forward spectral error.
5. **Fix the three structural test blind spots** — a non-involutive permutation fixture, the `balanced_alternating` scheme, an asymmetric Hoeffding fixture — and write tests for the confirmatory statistics layer (Holm, CI width, test tails). Three fixtures and a handful of tests recover most of the missing 21% mutation score.

**Then, the structural decision.**
6. **Restate the section-valued free-energy requirement as equivariance, not invariance**, per Theorem A-NOGO, and adopt the proved consistency identity `\Fenergy[Q_X] = \int f\,d\mu_D + \mathrm{TC}_D` as the replacement for `hyp:prob-sampling-compatibility`. This retires wave 1's item 1 in its original form and delivers item 5 at the same time.
7. **Paste in the N3(a) section** (already written and SPEC-compliant), including the honest B4 scope paragraph and the negative closure of the ledger's operational-base-holonomy item.
8. **Extract the `05c` geometry paper.** It is the strongest, most defensible, most likely-novel content, and it is immune to every structural criticism in this audit because it contains no free energy.

**Cut or demote.** `07b`: 73% terminal, no agent-specific content, no hypothesis tags — either extract the ~750 load-bearing lines or spin it out as a Markov-kernel coarse-graining companion paper. `thm:hist-global-clock-exactness`: retag, since it delivers no clock. `prop:obs-declared-root-unavoidable`: demote to a remark. `\Theta`, `\Phi`, `\tau`: disambiguate the fifteen tabled drifts.

**Recommended order overall:** cite Dennis 2025 and Sengupta 2016 → extract the `05c` geometry paper → extract the attention paper → return to the section-valued free energy with two papers already banked.

---

## Coordinator verification log — wave 2

| Claim | Check | Result |
|---|---|---|
| `07b` has zero HYPOTHESIS tags | `grep -o '\status{[A-Z-]*}' Theory/07b_agent_network_rg.tex \| sort \| uniq -c` | 81 ESTABLISHED, 10 DEFINITION, 1 OPEN, 1 NOT-CLAIMED, **0 HYPOTHESIS**. `05d` for contrast: 11 HYPOTHESIS. **Confirmed.** |
| Čencov is cited and handled well (wave-2 correction to wave 1) | Read `Theory/08_infogeometry.tex:493` | Cites `\citep{Cencov1982}`, states the finite-simplex uniqueness, and explains why Campbell's cone extension is a characterization but not uniqueness up to scale. **Correction upheld; wave 1 was wrong.** |
| Self-citations uncited | `grep` each bib key across `Theory/*.tex` | `Dennis2025it`, `dennis2025inertia`, `Dennis2025trans` — **0 citations each**. `Dennis2026metaentropy` likewise absent. **Confirmed.** |
| "Epistemic Gauge Theory" absent | case-insensitive search across `.tex`/`.bib`/`.md` in both repos | **Zero hits.** No bib entry. **Confirmed.** |
| The 2025 preprint exists | fetched `preprints.org/manuscript/202505.1773/v1` | Page **resolves** (81,938 characters; too large to read in full in-session). Abstract quoted by the reviewing agent. **Author confirmation requested** rather than asserted. |
| No novelty overclaim in the manuscript | `grep -ic "to our knowledge\|for the first time"` across all `Theory/*.tex` | **Zero hits.** The manuscript does not overclaim novelty anywhere. **Confirmed** — and this is to its credit. |

Not independently re-verified by the coordinator: the A-NOGO torsor argument and its numerical witnesses; the `03:391` counterexample; the mutation scores; the red-team conditioning witnesses; the priority searches. Each is reported with commands and outputs in the corresponding wave-2 report.

Per-domain wave-2 reports: `wave2-01-constructions.md` (979 lines, includes the paste-ready LaTeX), `wave2-02-proofs.md`, `wave2-03-redteam.md` (475 lines), `wave2-04-chapters.md` (877 lines), `wave2-05-mutation.md`, `wave2-06-novelty.md`.
