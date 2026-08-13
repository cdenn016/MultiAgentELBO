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
