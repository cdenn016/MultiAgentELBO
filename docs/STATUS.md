# Programme status — punchlist

*Rebuilt 2026-08-13 (second pass, after worklog §3g–§3k). Read `overview.md` for the theory, the
worklog for the derivation front, `docs/research-plans/2026-08-13-tier0-decisions.md` for the six
declarations awaiting an answer, and this file for where everything stands.*

Status markers: **P** proven · **D** derived under stated hypotheses · **C** computed on an instance ·
**S** suggested · **O** open · **R** refuted or retracted.

---

## 1. The standing decision, and what it bought

**The link group is restricted to a compact subgroup.** That single declaration resolved six separate
open items, all of which had the same cause (worklog §3i.1): Yang–Mills non-definiteness, the
coercivity lemma, the invariant-versus-bounded dilemma for the plaquette density, `λ₀`'s
gauge-dependence, the infinite Haar measure, and the ELBO-derivability of the curvature term.

It also made the curvature term **derived rather than engineered** (§3i.2). With a Gibbs law on links
against Haar, the `U(1)` case is exactly von Mises with `Z = e^{−β}I₀(β)` in closed form; the
variational bound saturates at `−2.2e-16` on the true law and is strictly positive otherwise. The
noncompact control diverges (`1.7, 15.8, 8.7e3, 6.2e31, inf`). Compactness is what makes the evidence
exist.

Cost: the SPD sector stops being gauge. Under `O(K)` congruence preserves eigenvalues, so transports
rotate uncertainty but cannot rescale it. The reduction `GL(K)/O(K)` makes SPD **matter** rather than
gauge — but see §3j, that argument is Gaussian-specific.

---

## 2. Solid

| Result | Status | Where |
|---|---|---|
| Exact two-channel finite ELBO, tied-replica | **P** | `docs/derivations/.../exact-two-channel-finite-elbo/` |
| Total-correlation chain; pseudo-ELBO sign proposition | **P** | `Theory/05_elbo.tex:39-50`, `:95-113` |
| Exact finite-site KL contraction | **D** | conditional on §5's four hypotheses |
| Pullback geometry + exact defect cocycle | **P** | `Theory/05c` |
| Kernel–holonomy isomorphism `ker L_I ≅ Fix(Hol)` | **P** | `Theory/09:379,447` |
| Tree-free coarse score | **P** | `Theory/06_general_coarsegraining.tex:561` |
| Agent-network RG **equations** | **D** | `Theory/07b` — equations only; no interacting fixed point exists |
| Alignment ⟹ holonomy ∈ `Stab(q)`, not `= I` | **C** | §3e.2(i) |
| Fisher pencil is exactly `GL(K,ℝ)`-invariant | **C** | §3e/O5 — drift `1.0e-15` vs `1.499` scalar |
| Prior sector removes the support-boundary wall | **C** | O4 — uniform self-anchoring is a pure translation, does nothing |
| Shared latent gives genuine coupling, PIFB2's form at rank one | **C** | §3g.2 |
| `λ₀ = c·Σ‖F‖²`, linear, exponent 1.006 | **C** | §3h.3 — **compact `G` only** |
| Plaquette action is an exact negative-ELBO component | **C** | §3i.2 — compact `G` only |

---

## 3. Refuted, retracted, or closed negatively

| Item | Verdict |
|---|---|
| Adiabatic extent criterion `‖Q D^ω P‖ ≪ gap` | **R** — not scale-invariant, and unnecessary given `‖dP‖ ≤ ‖dL‖/gap` |
| Bare connection Laplacian `D⊗𝟙 − W^Ω` | **R** — non-self-adjoint under row-simplex `β`; use the `Theory/09` energy form |
| Self-anchoring repair for support boundaries | **R** — a uniform diagonal only translates the spectrum |
| `ε` as an RG scale / dendrogram | **R** — partitions refine as `ε` grows |
| `H¹` of the sheaf measures frustration | **R** — `dim H⁰ − dim H¹ = χ·K` identically |
| **Compactness rescue via `Stab(q)`** (§3h.4) | **R** — gauge acts by *conjugation*; `‖H−I‖_F` runs `0.836 → 227.8` with `tr H` fixed to 10 digits |
| Shared latent induces a frame coboundary | **R** — fails the self-edge identity; never a cocycle for `N ≥ 2` (sign contradiction) |
| Gauge structure generic over exponential families | **R** — needs a *homogeneous* fiber; Gamma/Beta have non-constant curvature |
| `κ_A` derivable by calibration; smallest nonzero update | **closed negatively** |
| `GL(K,ℝ)` scope restriction on the extent criterion | **R** — artifact of scalar weights |

---

## 4. Open, in dependency order

**Tier 0 — six declarations awaiting an answer.** Priced in
`docs/research-plans/2026-08-13-tier0-decisions.md` (1328 lines). D1 (`Ω_ij` typing) is largely
settled by §3h.1: free edge variables already exist as Regime II in `Theory/02`
`def:geo-graph-links`, with the coboundary an *optional* hypothesis. D3 (representation channel) now
couples to "which compact subgroup" and should be answered with it.

**Tier 1 — structural.**
- **O** No interacting fixed point in `07b`. Every exhibited fixed sector is trivial.
- **O** Cross-agent coupling of the *declared form*. A shared latent gives coupling but not PIFB2's
  form: rank-limited in the scalar case, never a cocycle in the fiber case.
- **O** The coarse map is recognition-dependent, breaking H2 of the exact contraction theorem.
- **O** Meta-agent extent. No criterion survived; the gap criterion provably cannot bound extent for
  `dim C ≥ 3`.

**Tier 2 — expensive.** Γ-convergence for manifold-valued graph Dirichlet energies with a connection.
**Not** retired by lattice gauge theory: LGT's continuum limit is a limit of measures with a running
coupling, not Γ-convergence of a deterministic functional at fixed coupling.

**Tier 3 — physicalization.** `Phys_α` is correctly typed but substantively empty. In `dim ≥ 2` the
base geometry is entirely connection-generated (rank-≤1 floor).

**Reading, not construction — do these before building more.**
- Which statistical families are homogeneous. Shima on homogeneous Hessian manifolds; Vinberg on
  homogeneous convex cones; Koecher–Vinberg classifies the symmetric ones by Euclidean Jordan
  algebras, a finite list. This is the honest answer to "what is the right general fiber class".
- Gauged nonlinear sigma models with symmetric-space targets (§3i.4).
- Wilson kinematics must be cited: `def:geo-graph-links` is Wilson 1974 §II; the spanning-tree
  trivialization is maximal-tree gauge fixing.

---

## 5. Deferred by decision

**Lossy communication (§3k).** Requiring `Ω_ij` to be a Fisher isometry *is* the assumption that
communication is lossless — and of 20000 random Markov kernels, zero had a Markov inverse, so lossless
means relabelling and nothing else. Dropping it costs the group (hence all of §3e–§3j) and buys two
things the programme lacks: a second independent obstruction to meta-agent formation, and an arrow of
time from the monotone Fisher defect. Recorded, not adopted. `Theory/05c`
`thm:pb-pullback-fisher-defect` already carries `Δ_F ⪰ 0` and is unconnected to the gauge story.

---

## 6. Verification and hygiene

- **Validated ledger is stale.** `.verification/ledger.json` pinned to `d892374`, many commits behind.
  Eight claims, **seven high severity, none verified**. Re-running the closure is the oldest
  outstanding task.
- **Witnesses** (seeded, assert in-script): `meta_agent_coherence_witness.py` (7 claims),
  `shared_latent_coupling_witness.py` (6), `u1_two_path_holonomy_witness.py` (4, plus `tests/`),
  `kl_expansion_check.py`.
- **Test suite**: 21 failed / 1092 passed / 15 skipped — 19 bind to a `.codex` path outside the repo,
  2 are a `render_figures` contradiction. None numerical.
- **Provenance.** `wave2-*`, `rm-0*`, `panel*` are this programme's own agent audit returns, not
  external review.
- Numbers in §3f live in session scratchpads and remain uncitable (obligation O3). §3g–§3k numbers are
  in committed witnesses.

---

## 7. Standing claim discipline

Say: PIFB2 is a gauge-motivated **effective action**; selected sectors admit **exact ELBO
realizations**; the base is a **context** manifold; pullbacks give positive-semidefinite
**semi**geometries. The gauge apparatus requires a **homogeneous** fiber and a **compact** link group.

Do not say: that the complete action has been derived from the exact ELBO; that `C` is space; that a
Fisher pullback is automatically nondegenerate or Lorentzian; that one bit equals `ℏ`; that the gauge
structure survives the generalization to arbitrary exponential families; that any construction is
**first** or **novel** without a literature check citing Dennis (2025), Sengupta et al. (2016), Wilson
(1974), Shima, and Vinberg; or that an internal audit return is external refereeing.

---

## 8. 2026-08-13 remediation correction — current authority

This section supersedes every conflicting claim above while preserving the earlier sections as a
dated record of the investigation. It incorporates the independent audit and the repaired
`shared_latent_coupling_witness.py` and `meta_agent_coherence_witness.py`. Source/theory remediation
revision `76af87b` has current revision-bound evidence: the full CPU suite contains 1,182 tests,
with 1,166 passed, 16 skipped, and zero failures or errors; both rigorous-theory release validators
exit zero; and the independent verifier review contains 183 tests, with 170 passed, 13 capability or
fixture skips, and zero failures or errors. The old ledger pin and the old
`21 failed / 1092 passed / 15 skipped` total in §6 are historical only. This closure makes no CUDA
claim. Evidence and hashes are recorded in
`docs/audits/evidence/2026-08-13-claude-opus-remediation/manifest.md`.

| Topic | Corrected status and boundary |
|---|---|
| Finite presentation descent | **P/C.** Collapsed retained-variable VFE descends under equality of the retained joint law. Full auxiliary-latent VFE equals the collapsed VFE plus an expected conditional KL; on the support-qualified tier, posterior completion or minimization over auxiliary lifts removes that defect. Strictly positive parameterwise-equal retained families have the same retained Fisher tensor and every common `C^1` pullback. Full-joint Fisher tensors, node inventories, and interventions do not generally descend. Paired marginals admit distinct smooth positive lifts with different VFE and Fisher pullbacks, so canonical agentization and lift selection remain open. |
| Shared-latent rank | **P/D.** For positive-definite private and latent covariances, the Woodbury correction satisfies `rank(C) = rank(Lambda) <= R`; equality with the declared width `R` requires full column rank of `Lambda`. Latent width alone neither forces nor forbids positive edge weights. |
| Positive KL split | **C.** An exact rank-two Gaussian control has strictly positive KL edge weights and a proper residual prior. A separate rank-one control shows that a proper residual prior is an independent side condition. |
| Induced transports | **C/D.** A cross-block identifies the product `beta_ab W_ab Omega_ab`, not `Omega_ab` alone. After dividing out declared positive `beta` and invertible `W`, an exact `N=3`, `K=d=2` rotation construction has a nontrivial transport cocycle, exact precision reconstruction, and a proper residual prior. The previous universal cocycle no-go is withdrawn. |
| Invertibility | **P.** `d >= K` is only necessary. The exact condition for the induced `K x K` coefficient is `rank(Lambda_b M Lambda_a^T) = K` (with the appropriate private-covariance factors, which do not change rank when invertible). |
| Relation to PIFB2 | **D/C.** The rank-one construction is an exact flat, symmetric, unnormalized scalar mean-alignment skeleton. It is not the complete directed, row-normalized, two-channel PIFB2 functional; the phrase “exactly PIFB2” remains withdrawn. |
| Support departure | **D/C.** There is no prior-generated positive spectral wall at literal departure: the local prior Hessian is `chi_i alpha_i Lambda_{p,i}` and vanishes with `chi_i`. For every positive receiver presence, canonical row normalization cancels its common factor; at exactly `chi_i=0` the row is `0/0`. A fixed-ambient extension or active-set deletion convention is therefore required. Edge dropout with `chi_i=1` is a different operation. |
| Forward-KL Hessian | **P/C.** For directed `(i,j)` meaning sender `j` to receiver `i`, the fixed-covariance, frozen-`beta` mean Hessian uses `beta_ij (Theta_ij Sigma_j Theta_ij^T)^{-1}`. Reverse KL is a separate directed edge. `M = direct-sum Sigma_i^{-1}` remains only an interim reading metric; normalized-row response, threshold, and extent are open. |
| Retired four-regime table | **P/C.** The only universal conclusion is the exact identity cell: orthogonal reciprocal links plus symmetric weights make the retired operator equal the energy form. Other seeded cells are diagnostics. Countercontrols show that a nonorthogonal link need not create a negative-real-part spectrum and a symmetric row-stochastic system need not become asymmetric. |
| Kernel and holonomy | **P.** On each connected component `I_alpha`, assuming invertible represented transports with inverse reverse transports and positive-definite represented edge weights, root evaluation gives `ker L_{I_alpha} ≅ Fix(Hol_{r_alpha})`; hence `ker L_I ≅ direct-sum_alpha Fix(Hol_{r_alpha})`. Neither nontrivial holonomy nor point curvature is equivalent to an empty kernel, and flatness is not equivalent to meta-agent existence. |
| Graph versus base geometry | **O/typed.** Agent-graph links, base connection holonomy, and bundle topology remain distinct. Identifying them requires declared node-to-base anchors, assigned base curves or cells, and an equality to the corresponding parallel transports. No such identification follows from the graph witness alone. |
| Gibbs-Haar plaquette term | **D, conditional model only.** It is an exact negative-ELBO component only after declaring a new random compact-link Gibbs-Haar generative model (including the inverse-temperature coefficient and entropy term). It is not derived from the current fixed-link ELBO and does not by itself derive current-model curvature dynamics. |
| Fiber symmetry | **P/typed.** Homogeneity is sufficient for transitive full-fiber reach, not necessary for every gauge action: nonhomogeneous statistical manifolds can have nontransitive isometry sectors. A homogeneous space need not be symmetric; the symmetric-space conclusion is valid for the SPD covariance sector or where a symmetric-pair hypothesis is separately proved. |

Revision-bound CPU closure is issued for source/theory revision `76af87b`; cite the exact derivations,
claim ledgers, and durable JUnit evidence for individual claims. The current globally installed
verification skill is a coherent schema-1.1 upgrade whose nine active files differ from the frozen
schema-1.0 contract. That mismatch correctly fails closed. Preserve v1 and its historical evidence;
a versioned v2 builder/contract migration remains **open** rather than silently refreshing v1.
