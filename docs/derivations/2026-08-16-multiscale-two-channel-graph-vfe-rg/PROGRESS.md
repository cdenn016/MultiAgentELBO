# RESUME LEDGER — multiscale two-channel graph VFE / RG investigation

**Purpose.** If the session is interrupted (rate limit, context reset), read this file first.
It records what has been read, what has been derived, what is still owed, and the exact next action.

**Run dir.** `docs/derivations/2026-08-16-multiscale-two-channel-graph-vfe-rg/`
**Skill.** `rigorous-theory-search` (invoked). Protocol references already read:
problem-contract, portfolio-search, proof-obligations, output-contract,
physics-information-audit, renormalization-effective-theory, adversarial-verification.

**Mode constraint from session prompt.** Do NOT spawn Agent subagents; do NOT use Workflow.
Do the work inline. Cross-model verification is therefore unavailable — record that as a
scope limitation in the final report rather than claiming verification.

---

## STATUS: COMPLETE — released INCONCLUSIVE, structural validator passes in release mode (exit 0)

Last updated: 2026-08-16, end of run.

Deliverables:
- `REPORT-part1-vfe-and-construction.md` (Q1, Q2)
- `REPORT-part2-parent-partition-graphrg.md` (Q3, Q4, Q5)
- `REPORT-part3-holonomy-blocks-dynamics.md` (Q6, Q7, Q8)
- `REPORT-part4-literature-experiment-verdict.md` (Q9, Q10, claim table, Theorem A, obligations, program)
- `construction-or-strongest-theorem.md`, `counterexample-register.md`, `final-report.md`
- `evidence/` (attacks, reconstruction, erasure); `_build_artifacts.py` regenerates all JSON.

Contract id: `contract-sha256-7d2c4a48da6b18e0d1dd177ba0e42e6ab6b625410e5cbefa9c9031dcfb9dd985`.

**Not done, by design:** no cross-model verification (session prohibits subagents), so no claim
carries EVIDENCE_VERIFIED. Row 55 of the claim table (§6 headings of arXiv:2412.12988) is
vault-recorded and was not re-verified verbatim — the HTML and PDF fetches truncated.

---

## 1. Reading log (what has actually been read)

| Source | Status | Key content extracted |
|---|---|---|
| `Theory/main.tex` | READ | Chapter order; shared macros; four parts. |
| `Theory/04_generative.tex` | READ | Fixed normalized generative law; **typing prohibition** (`req:gen-typing-prohibition`); no-distinguished-target prop; Gibbs counterexample (local normalization insufficient, `prop:gen-gibbs-counterexample`); passive $G\times G$ frame action; shared-link nonclosure counterexample. |
| `Theory/07c_full_graph_meta_agent_vfe.tex` | READ | The full-graph VFE `eq:full-graph-vfe-global`; generative factorization (HYPOTHESIS); exact 5-term decomposition (thm:full-graph-vfe-decomposition, ESTABLISHED); row free energies + Gibbs rows; $1/\beta$ NOT a metric; holonomy stabilization $(H_C)_\#Q_I=Q_I$; dressed edges $\Theta^{IJ}_{ij}$; edge-event pushforward; $K_\downarrow$; open next-theorem. |
| `Theory/06_general_coarsegraining.tex` | READ | Markov category; extended KL DPI (no AC needed); DPI equality iff $r(X)=\bar r(Y)$; pairwise Bayes recovery + infinite-equality counterexample; Fisher contraction (score projection) + Bernoulli counterexample separating Fisher equality from recovery; evidence-preserving channel ELBO monotonicity; **three distinct operations** (pushforward / energy precomposition / family restriction); graph-exponential trace closure w/ diagonal-affinity hypothesis; Galerkin message-passing residual $CH-H_cC=CH(I-PC)$; equivariant channels; partition naturality $S(P\cdot X)=PS(X)Q^\top$ (OPEN); holonomy-conditioned marginal-law modes $\mathfrak D^x_I$ (ESTABLISHED invariance). |
| `Theory/appendix_claim_ledger.tex` | READ | Full open-obligation list. Notably OPEN: continuum law theory; partition selector; Bayesian-RG bridge; fine–coarse semiconjugacy for the manuscript's own coarse natural gradient; infinite-volume limit; two-index limits; physical-time identification. ESTABLISHED: `thm:rg-pointwise-parent-datum`; operational intervention quotient. |
| `Theory/07b_agent_network_rg.tex` | PARTIAL (lines 1–340 read; section map obtained) | `thm:rg-exact-coarse-vfe` (VFE chain rule, ESTABLISHED); `thm:rg-pointwise-parent-datum` (full pointwise parent datum, ESTABLISHED); effective action/conditional-partition formula. Section map recorded below. |
| `Theory/03_probability.tex` | **NOT READ** | |
| `Theory/05_elbo.tex` | **NOT READ** | |
| `Theory/05b_local_collective_elbo.tex` | **NOT READ** | |
| `Theory/07_general_renormalization.tex` | **NOT READ** | |
| `Theory/10_renormalization.tex` | **NOT READ** | |
| `Theory/SPEC.md` | **NOT READ** | |
| `solid_RG_theory.md` / `.tex` | **NOT READ** | |
| `physicists_companion.tex` | **NOT READ** | |
| `Theory/grand_canonical_meta_agent_formation.tex` | **NOT READ** | |
| Research vault: `berman-2023-bayesian-renormalization.md` | **NOT READ** | |
| Research vault: `gabrielli-2025-network-renormalization.md` | **NOT READ** | |
| Research vault: `villegas-2023-laplacian-renormalization-group.md` | **NOT READ** | |
| Research vault: `garuccio-2023-multiscale-network-renormalization.md` | **NOT READ** | |
| arXiv:2305.10491 (Berman–Klinger–Stapleton) | **NOT CHECKED against primary** | |
| arXiv:2412.12988 (Gabrielli–Garlaschelli–Patil–Serrano) | **NOT CHECKED against primary** | |

### 07b section map (line numbers)
```
13   Law-level coarse-graining and the VFE identity
34   thm:rg-exact-coarse-vfe
76   thm:rg-pointwise-parent-datum
256  The exact effective likelihood and action
293  thm:rg-effective-action
330  Local bounded action chart and its derivatives
371  thm:rg-bounded-action-calculus
440  prop:rg-action-bounded-recentering
548  Canonical contraction and the bounded Dobrushin certificate
551  thm:rg-action-lp-contraction
615  prop:rg-dobrushin-cocycle
697  Score tangents, extensive block lift, inhabited spectrum
835  thm:rg-score-pushforward-defect
1052 thm:rg-gaussian-hermite-spectrum
1154 prop:rg-hermite-scope
1234 thm:rg-unital-essential-spectrum
1311 Exact finite-network interaction coordinates
1341 prop:rg-product-equivalence-not-preserved
1405 thm:rg-hoeffding-action-isomorphism
1473 prop:rg-interaction-rn-gauge-covariance
1545 Exact nonlinear interaction RG and retained projections
1695 Exact closure generates hyperedges
1748 Fine--meta bridge kernels
1799 Gauge-covariant cross-scale operators
1966 Exact attention between meta-agents
2155 Ordered-path closure and memory
2167 thm:rg-strong-lumpability
2249 open:rg-pointwise-parent-dynamics
2265 thm:rg-projection-memory
2359 The RG transformation and beta functions
2494 prop:rg-retained-beta-residual
2581 def:rg-scale-connection
2657 prop:rg-continuous-beta-underdetermined
2724 Fixed points, flows, and scaling operators
2973 thm:rg-complete-effective-theory
```

---

## 2. Facts established from the live theory (to reuse, not re-derive)

- **F1.** The exact multiscale VFE is `eq:full-graph-vfe-global`:
  $\mathcal F^{\rm ext}=-\log p_\theta(o|X)+\KL(\mathbb Q_\phi\|\boldsymbol\Pi_{\theta,o,X})$.
  Any additive term decomposition must come from a declared factorization. [07c, ESTABLISHED]
- **F2.** Exact 5-term hierarchical decomposition holds under declared factorizations of
  $\mathbb P$ and $\mathbb Q$ along the SAME ordering. [07c thm:full-graph-vfe-decomposition]
- **F3.** Coarse VFE chain rule: $\mathcal F_P(Q_o)=\mathcal F_{P^c}(Q^c_o)+\int \KL(\widehat Q(dy|z)\|\widehat\Pi(dy|z))Q^c(dz)$,
  extended-real, no finiteness needed for the identity. [07b thm:rg-exact-coarse-vfe]
- **F4.** $\Delta_A=0$ iff discarded conditionals agree a.s.; finite-fine-KL needed for
  ordinary subtraction and for the pairwise common-recovery equivalence. [07b thm:rg-pointwise-parent-datum]
- **F5.** DPI equality is PAIRWISE; experiment-level sufficiency needs one parameter-independent
  reverse kernel for all $\theta$ simultaneously. Counterexample at 06 §cg-fisher-contraction.
- **F6.** Marginals do NOT determine joints (`prop:prob-marginals-do-not-determine-joint`).
  So a correlated recognition law cannot be rebuilt from marginals.
- **F7.** $1/\beta_{ij}$ is a directed, row-relative surprisal, not a metric. At the Gibbs optimum
  $\ell^b_{ij}=D^b_{ij}+\tau\log Z_i$. [07c, ESTABLISHED]
- **F8.** Holonomy-blind parent requires $(H_C)_\#Q_I=Q_I$ on ALL retained loops; this is a
  stabilizer condition, NOT flatness, and does not select $I$. [07c + 06 thm:cg-holonomy-kl-marginal]
- **F9.** Local normalization of node/edge potentials does NOT give a finite partition function
  (Gaussian $e^{cy_1y_2}$ counterexample). [04 prop:gen-gibbs-counterexample]
- **F10.** Typing prohibition: no generative factor may read the recognition law/posterior.
  [04 req:gen-typing-prohibition]
- **F11.** Galerkin/message-passing residual $CH-H_cC=CH(I-PC)$; exact coarse propagation iff
  range$(P)$ is $H$-invariant (for $R$-self-adjoint $H$). [06 prop:cg-message-passing-residual]

---

## 3. Deliverable outline (the answer the user asked for)

Required sections, in order:
1. Physicist-facing statement of full VFE + architecture diagram.
2. Typed mathematical construction (Q1).
3. Exact VFE + conditional-KL decomposition, all normalizers/base measures/AC/extended-real (Q2).
4. Three parent-influence mechanisms + impossibility of imposing deterministic pushforward
   AND independent same-time cause together (Q3).
5. Partition variables inside the model; variational update; anti-degeneracy priors (Q4).
6. Graph RG by pushing $(\eta^b,\eta^m)$ then disintegrating (Q5): directed, zero weights,
   overlaps, distinct b/m partitions, nested composition.
7. Non-flat connection data exactly; $H_\#Q=Q$ necessity/sufficiency; distribution of $\Theta^{IJ}_{ij}$ (Q6).
8. Spontaneous block formation: 3+ competing mechanisms, hypotheses, counterexamples (Q7).
9. Cross-scale natural gradient + semiconjugacy/lumpability defect; optimization vs physical time (Q8).
10. Bayesian RG + network RG + Laplacian RG + additive-hidden-variable multiscale model (Q9).
11. Minimal finite categorical/non-Gaussian falsification experiment (Q10).
12. Claim table with ESTABLISHED / CONDITIONAL / CONJECTURE / NUMERICAL / OPEN.
13. Strongest defensible theorem + unresolved proof obligations + staged simulation program.

---

## 4. Next action

WRITING PHASE. All reading done (incl. 07b 2359–2600 beta section and 2973–3067 closure theorem).

- [x] `REPORT-part1-vfe-and-construction.md` — physicist statement, architecture diagram, typing
      fork (Reading A / Reading B), Q1 typed construction + Prop 1 (tower normalization),
      Q2 Theorem 2 (exact decomposition) + all normalizers/base measures/AC/extended-real boundary,
      double-counting and marginal-reconstruction corollaries.
- [ ] `REPORT-part2-parent-partition-graphrg.md` — Q3 (three mechanisms + impossibility trichotomy),
      Q4 (partition inside model, Gibbs update, DEGENERACY PROPOSITION), Q5 (graph RG).
- [ ] `REPORT-part3-holonomy-blocks-dynamics.md` — Q6, Q7, Q8.
- [ ] `REPORT-part4-literature-experiment-verdict.md` — Q9, Q10, claim table, strongest theorem,
      obligations, staged simulation program, scope/limitations.
- [ ] Fill skill JSON artifacts + `final-report.md` + `counterexample-register.md`, run validator.
- [ ] Short chat summary.

---

## 4b. ADDITIONAL reading completed (round 2)

| Source | Key content |
|---|---|
| `Theory/05b_local_collective_elbo.tex` | FULL READ. Interaction-record model; collective VFE `thm:obs-collective-vfe`; block-conditional VFE `thm:obs-local-multiagent-elbo`; **exact local–global potential identity** `thm:obs-local-global-potential`; additive ledger with total correlation `eq:obs-global-ledger`; **singleton incident-counting identity** `eq:obs-singleton-incident-counting` ($\sum_i H_{\{i\}} = \sum_a |\partial a| E_a$ — the overcounting proof); **attention as latent source label** `prop:obs-attention-elbo` (this is where $\Phi^{\rm att}_i=\sum\beta D+\tau\KL(\beta\|\pi)$ becomes an ELBO sector); correlated ledger `eq:obs-attention-correlated-ledger` retains conditional TC; local natural gradient = block of collective flow (block-diagonal Fisher load-bearing); observation–interaction equivalence via randomization lemma. |
| `Theory/07_general_renormalization.tex` §Bayesian comparison (1092–1171) | BKS typed comparison; $D_\tau=J_G I^{-1}J_G^\top$; Bayesian-RG bridge OPEN; Mehta–Schwab scoped. |
| `Theory/10_renormalization.tex` §516–626 | Literature boundary: BKS/LRG/MSM/graph-learning; LRG heat blocks $K_{ij}\mapsto g_i^{-1}K_{ij}g_j$ NOT gauge-invariant node affinities. |
| `Theory/03_probability.tex` §415–484 | `prop:prob-marginals-do-not-determine-joint`; compatibility determines neither side; continuum OPEN with the concrete reference-measure obstruction. |
| `Theory/grand_canonical_meta_agent_formation.tex` | FULL READ. Stage I–V. Canonical row = Gibbs ensemble; grand-canonical EDGE occupation $\rho^*_{ij}=\sigma[\logit\pi^E+(\mu-\epsilon)/\tau_E]$; grand potential $\Phi_E$ and conjugacy $-\partial\Phi_E/\partial\mu=\rho^*$; **mean-field coherence instability $2Jc\rho_0>a$** with quartic correction $-J^2c^2\rho_0(1-\rho_0)/(2\tau_E)$; membership grand potential; Lyapunov law under fixed controls; driven balance. Explicitly says $\mathcal G$ is a *proposed addition*, not an ELBO. |
| `solid_RG_theory.md` | FULL READ. §2 $\ker L_I\cong\mathrm{Fix}(\mathrm{Hol}_r)$; flatness ≠ stabilization (both directions refuted); §3 two-channel zero-distortion theorem; §4 forward-KL barycenter $M=\sum w_iP_i$ exact identity; §5 Pinsker/TV tree bound; §6 **scalar + marked event-law coarse-graining with component-indexed roots**; §7 hard/soft/replicated cover (replicated cover NOT a Markov kernel; doubles mass); §8 common-channel VFE closure; §9 moving-map chain rule $\dot z=\partial_tc_t+Dc_tX_t$; **§10 eight shortcut failures (table)**; §11 **"The obligation named in this file's own title is OPEN" — no RG group exists: no rescaling map, no beta, no blocking ratio, no relevant/irrelevant classification**; §12 phase roadmap (Phases 1–2 ESTABLISHED, 3–5 OPEN). |
| `Theory/07b` §1695–2360 | Hyperedge closure by Möbius `eq:rg-mobius-potentials`; Ising-star cubic counterexample to pairwise closure; posterior bridge kernels; **component-indexed gauge-covariant cross-scale operators** with $\mathsf C_x\mathsf P_x=I$ and nested-composition condition `eq:rg-linear-nested-compatibility`; **exact meta-attention by pushing $\eta$ then disintegrating** `eq:rg-meta-attention`; evidence-weighted receiver reweighting `eq:rg-attention-evidence-weights`; log-sum-exp source merge `eq:rg-attention-log-sum-exp`; **Hom operator $\mathsf T^x_{IJ}$ needs Bochner integrability; conditional mean need not lie in $R_x(G)$ (±π/2 rotations average to 0); correlated marks/features counterexample $(I,v),(-I,-v)$**; meta-attention KL split; **standard-Borel strong lumpability** `thm:rg-strong-lumpability` + weak-lumpability 3-state counterexample; `open:rg-pointwise-parent-dynamics` semiconjugacy defect $\delta_t$; **exact projection-memory (Mori–Zwanzig) recurrence** `thm:rg-projection-memory` + autonomy corollary + $\mathsf{QTP}\neq0$ witness. |
| Vault: berman-2023 | READ. Fisher metric as emergent RG scale; $\tau=1/T$; pushforward inverse Fisher $= $ ERG diffusion kernel; information-shell scheme thresholds $\mathcal I_{ii}$; **note records: stiff/sloppy↔relevant/irrelevant is the paper's interpretive claim, rigorous only in the CFT/Zamolodchikov case**; IB link NOT derived; authors concede connections "largely conceptual"; §3.1 spectral vs §4.2 diagonal mismatch. |
| Vault: gabrielli-2025 | READ. Three-step program; GR/LRG/MSM table; failure taxonomy (renormalizability = additivity of the defining parameter); scale-free ≠ scale-invariant; §6 open problems incl. **simultaneous renormalization of topology and dynamics** and **"Parameter (ir)relevance: an information-theoretic perspective"** (prose, zero equations — promissory note). |
| Vault: villegas-2023 | READ. $\rho(\tau)=e^{-\tau L}/Z$, $C(\tau)=-dS/d\log\tau$; diffusion-equivalence supernodes by thresholding $\rho'_{ij}=\rho_{ij}/\min(\rho_{ii},\rho_{jj})$; semigroup not group; typing caveat (self terms ⇒ killed diffusion). |
| Vault: garuccio-2023 | READ. Uniqueness theorem: $p_{ij}=1-e^{-\delta x_ix_jf(d_{ij})}$ is the ONLY form invariant under all partitions; $x$ additive; $d$ renormalizes as fitness-weighted $f$-mean; $\delta$ invariant; $\alpha$-stable annealed variant makes the flow a GROUP. |
| **PRIMARY CHECK** arXiv:2305.10491 | VERIFIED: title, authors (Berman, Klinger, Stapleton), v1 2023-05-17 / v3 2023-10-09, MLST 4(4) 045011. Abstract quoted. Eq. (44) pushforward Fisher confirmed; Eq. (55) $\Theta^>_\Lambda=\{\theta_i:\mathcal I_{ii}>\Lambda\}$ confirmed. **Confirmed: the paper does NOT treat directed graphs, network partitions, or holonomy.** |
| **PRIMARY CHECK** arXiv:2412.12988 | VERIFIED: title "Network Renormalization", authors Gabrielli/Garlaschelli/Patil/Serrano, v1 2024-12-17, Nat. Rev. Phys. 7:203–219 (2025). Abstract quoted. **§6 open-problem headings could NOT be re-verified verbatim this session (HTML/PDF fetch truncated).** Partial confirmation obtained: the review does NOT claim any framework solves simultaneous renormalization of topology + dynamics; it states compatibility of a coarse-graining with the dynamics "has to be considered as an additional consistency requirement." Cite §6 headings as VAULT-RECORDED, not re-verified here. |

---

## 5. Derivations / findings completed

- **D1 (typing fork, load-bearing).** $D^b_{ij}=\KL(q^b_i\|(\Omega^b_{ij})_\#q^b_j)$ admits two
  incompatible typings.
  (A) **State-level:** $q^b_i$ is a *component of the latent sample* $y_i$ (a point of the
  associated-bundle fiber $(\mathcal E_b)_{c_i}$, as 05b explicitly permits). Then $D_{ij}$ is a
  measurable function of $y$, admissible inside a generative factor, and — under label exclusivity
  `eq:obs-attention-augmented-likelihood` + constant-row recognition
  `eq:obs-attention-recognition-factorization` — $\Phi^b_i$ IS an exact sector of the collective
  VFE, but with $\E_{Q_Y}D_{ij}$ in place of $D_{ij}$; row optimum
  $\beta^*\propto\pi e^{-\E_Q D/\tau}$.
  (B) **Recognition-marginal:** $q^b_i$ IS the marginal of $\mathbb Q_\phi$. Then $D^b_{ij}$ is a
  *functional of the recognition law*; inserting it into a generative factor violates
  `req:gen-typing-prohibition`. $\Phi$ is then a composite potential, NOT an ELBO sector.
  The user's problem statement does not disambiguate. **This is the single sharpest answer to
  "is the row free energy part of the ELBO."**
- **D2.** $\beta^{Q\star}_i \neq \E_{Q_Y}[\beta^P_i(Y)]$ in general (05b, ESTABLISHED); equal iff all
  $D_{ij}(Y)-D_{ik}(Y)$ are $Q_Y$-a.s. constant. So "average the softmax" is a shortcut failure.
- **D3.** Overcounting: $\sum_i H_{\{i\},o}=\sum_a|\partial a|E_{a,o}$. Summing singleton local
  potentials overcounts each factor by its scope size.
- **D4.** RG status: the project's own `solid_RG_theory.md` §11 states there is currently **no RG
  group** — no rescaling/identification map, no beta function, no blocking ratio, no
  relevant/irrelevant classification. Only a consistent *family* of coarse-grainings
  ($C_{20}=C_{21}C_{10}$). Any claim of "graph RG" must respect this.

---

## 6. Counterexamples available (from live theory, to reuse) + new ones to construct

Existing (ESTABLISHED in-repo, reusable with citation):
1. KL-threshold clustering is not transitive (Bernoulli 1/10→1/2→9/10, threshold 0.6).
2. Zero marginal KL does not control full VFE (parity/anti-parity joints).
3. Trivial holonomy ⇏ belief agreement (two-node tree, Gaussian means $\pm ae_1$, KL $2a^2$).
4. Belief agreement ⇏ trivial holonomy ($\mathrm{diag}(1,-1,-1)$ stabilizes isotropic Gaussian).
5. Spectral gap is not an intrinsic agreement scale (two-node gap $2c$, rescalable).
6. One-way KL does not control reverse KL ($\log 2$ vs $+\infty$).
7. Gaussian projection breaks nonlinear boundary actions (residual $2\lambda a^4$).
8. Replicated cover doubles mass (total mass 2).
9. Local normalization ⇏ finite $Z$ (Gaussian $e^{cy_1y_2}$, $c\ge1$).
10. Pairwise closure fails (Ising star, cubic coefficient $2\,\mathrm{sech}^2 h_0\tanh h_0 J_1J_2J_3$).
11. Averaged group element is not a group element ($\pm\pi/2$ rotations average to $0$).
12. Correlated marks/features: $(I,v),(-I,-v)$ have zero means but mean product $v$.
13. Weak ≠ strong lumpability (3-state chain).
14. Infinite KL equality carries no recovery ($\{a,b,c\}\to\{u,v\}$).
15. Fisher equality ≠ recovery (Bernoulli $\theta/4$, $\theta^2/4$ at $\theta=0$).

NEW ones needed for this deliverable (Q7, Q3, Q5):
- N1: large $\eta_{ij}$ + low $D_{ij}$ but no persistent block (to be constructed).
- N2: deterministic-pushforward parent AND independent same-time parent cannot coexist.
- N3: zero-weight / disconnected-parent pathology in the pushforward rule.
- N4: distinct belief/model partitions ⇒ no common parent node set.
