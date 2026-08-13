# Programme status — punchlist

*Rebuilt 2026-08-13. Read `overview.md` for the theory, the worklog for the derivation front, and this
file for where everything actually stands. Every entry cites the artifact that settles it.*

Status markers: **P** proven · **D** derived under stated hypotheses · **C** computed on an instance ·
**S** suggested/structural · **O** open · **R** refuted or retracted.

---

## 1. Solid — build on these

| Result | Status | Where |
|---|---|---|
| Exact two-channel finite ELBO on a tied-replica inventory | **P** | `docs/derivations/2026-08-12-exact-two-channel-finite-elbo/`, `COMPLETE_AFFIRMATIVE` |
| `KL(ζ‖p⊗r) = KL(q‖p) + KL(s‖r) + I_ζ(K;M)` | **P** | median residual 1.1e-16, max 2.7e-15 over 2×10⁵ instances |
| Total-correlation chain + pseudo-ELBO sign proposition | **P** | `Theory/05_elbo.tex:39-50`, `:95-113` (ESTABLISHED) |
| Exact finite-site KL contraction | **D** | conditional on four hypotheses — see §5 arrow table |
| Gauge-covariant informational pullback + exact defect cocycle | **P** | `Theory/05c` `thm:pb-fisher-defect-cocycle`, `thm:pb-base-defect-cocycle` |
| Kernel–holonomy isomorphism `ker L_I ≅ Fix(Hol_r)` | **P** | `Theory/09:379,447` `eq:cg-fixed-rank` |
| Tree-free coarse score (path-, root-, gauge-independent) | **P** | `Theory/06_general_coarsegraining.tex:561` |
| Agent-network RG *equations* | **D** | `Theory/07b` `thm:rg-fixed-point-equations` — equations only, see §3 |
| Exact fast-state profiling; compact-subgroup Haar reduction | **P** | `overview.md` §6 |

### New this session

| Result | Status | Where |
|---|---|---|
| Belief alignment ⟹ graph holonomy ∈ `Stab(q)`, **not** `= I` | **C** | `meta_agent_coherence_witness.py` C1 — `‖H−I‖=0.0895`, `‖Hq−q‖=1.6e-16` |
| That condition is what makes compression tree-independent | **C** | C2 — two trees agree to 2.0e-16; break one edge → 0.975 |
| Fisher pencil `(L^Ω, ⊕Σ_i^{-1})` is **exactly `GL(K,ℝ)`-invariant** | **C** | C6 — drift 1.0e-15 vs 1.499 for scalar weights; gauge acts by congruence on both halves |
| The prior sector removes the support-boundary wall | **C** | C7 — `λ₀` bounded away from 0 throughout departure |
| Shared latent generates PIFB2's KL form exactly, at rank one | **C** | `shared_latent_coupling_witness.py` C2 — `β_ab = c v_a v_b` to 2.2e-16 |
| Shared latent induces an invertible transport when `d ≥ K` | **C** | C5 — `Ω_ab = Λ_a M Λ_bᵀ S_b^{-1}` |
| That transport is **never a cocycle** for `N ≥ 2` | **P** | C6 — requires `F = T^{-1}/(1−N)`, negative definite while `F ⪰ 0` |

---

## 2. Refuted, retracted, or closed negatively — stop working on these

| Item | Verdict | Where |
|---|---|---|
| Adiabatic extent criterion `‖Q D^ω P‖ ≪ gap` | **R** — not scale-invariant, hence vacuous; also unnecessary, Kato gives the projector from the gap alone | worklog §3f.0, §3f.2 |
| Bare connection Laplacian `D⊗𝟙 − W^Ω` | **R** — non-self-adjoint under row-simplex `β`; indefinite off `O(K)` | §3f.0 R1; scoped by C5 of the coherence witness |
| Self-anchoring repair for support boundaries | **R** — a uniform diagonal is a pure translation, gaps unchanged to 4.4e-15 | C7 |
| `ε` as an RG scale / dendrogram | **R** — partitions *refine* as `ε` grows; monotonicity fails | §3f |
| `H¹` of the sheaf measures frustration | **R** — `dim H⁰ − dim H¹ = χ·K` identically | §3f.4 |
| Berry curvature for a real rank-1 block | **R** — projected connection is flat with `Z/2` holonomy | §3f |
| §4.7 Amari–Chentsov over-unification | **R** — refuted by a Poisson-fibre `d=2` run, `T_skew > 0` everywhere | worklog §4.7 |
| "Every Ad-invariant form on `gl(K,ℝ)` is indefinite" | **R** — `(tr X)(tr Y)` is invariant and nonnegative; the real no-go is positive-definiteness | `overview.md` §7 |
| B4's holonomy clause "defeated" | **R** — "unavailable"; record law reproduced to `TV = 0` by a flat connection with a declared twist | `overview.md` §7, §8 |
| `κ_A` derivable by calibration | **closed negatively** — no calibration of a *linear* conversion is ever a derivation | `overview.md` §2.3 |
| A smallest nonzero update | **closed negatively** — `inf KL = 0` on both declared tiers | `overview.md` §2.3 |
| `S_phys/ℏ = f(I_nat)` as stated | **R** — log-base invariance forces `f` constant; needs `f(I/I₀)` | `overview.md` §2.3 |
| `GL(K,ℝ)` scope restriction on the extent criterion (O16) | **R** — an artifact of scalar weights; the Fisher weight restores full invariance | C6 |

---

## 3. Open — the real gaps, in dependency order

### Tier 0 — declarations, not derivations. One sitting. Gate everything below.
Full pricing in `docs/research-plans/2026-08-13-tier0-decisions.md` (1328 lines, options costed, checked).

- **D1** what `Ω_ij` denotes — same-point frame comparison, interaction-complex link `Θ_e`, or base transport. Recommendation: the link variable, coboundary retained as a named specialization. **§3g.5 is new evidence for this**: a genuinely coupled law induces free edge data, not a cocycle. Contradiction to resolve: `appendix_notation.tex:498-504` and `Theory/09:346-350` say link variable; `PIFB2.tex:208` says Čech transition function with non-coboundary data out of scope.
- **D3** which representation carries the coherent block (`μ`, `Sym²`, model channel) — they demonstrably disagree for `SO(3)`.
- **D2** operator and metric — largely settled by C6; adopt the `Theory/09` energy form with the Fisher pencil.
- **D5** `β` generative-side or recognition-side. Within the closed theorem's scope both `β` and `γ` are recognition rows, which breaks H2 — see below.
- **D4** normalization lift from eigen-ray to a law. May dissolve: the finite variational object is the mean tie with free covariance.
- **D6** observation-term typing, `PIFB2.tex:689` — `m_i` unbound and not among the declared arguments at `:684`. Joint typing must be adopted by fiat, since the two repairs pull opposite ways.

### Tier 1 — structural blockers
- **O** No interacting fixed point exists in `07b`. Every exhibited fixed sector is trivial (identity channel, one-point coarse space, or constant likelihood forcing the Hoeffding interaction coordinate to vanish). The linearization is stated at a hypothetical `(H_*, ρ_*)` never shown to exist. **The RG has no content at the interaction tier until one is exhibited.**
- **O** Cross-agent coupling of the *declared form*. A shared latent supplies genuine coupling but not PIFB2's form: rank-limited in the scalar case (§3g.3), never a cocycle in the fiber case (§3g.5). Ledger claim `genuine-coupling-before-continuum` stands, now with a sharper diagnosis.
- **O** The coarse map is recognition-dependent, breaking H2 of `Theory/09`'s exact contraction. The meta-agent is therefore not an ELBO object via the spectral route. Surviving route: the excess-VFE decomposition `G(P) = G_tie + G_fact`.
- **O** Meta-agent extent. No criterion survived the panel. The gap criterion provably *cannot* bound extent for `dim C ≥ 3`, since crossings there cannot disconnect the base.

### Tier 2 — expensive, correctly scheduled last
- **O** Γ-convergence for manifold-valued graph Dirichlet energies carrying a gauge connection: equicoercivity, liminf, recovery sequences, interpolation topology, gauge compactness. `rm-06:277` prices it as the most expensive item in the roadmap. García Trillos–Slepčev covers only scalar/`ℝⁿ`. Nothing exists.

### Tier 3 — physicalization
- **O** `Phys_α` is correctly typed but substantively empty: no connection, causal cone, signature, operator content, or action coefficient derived.
- **O** In `dim ≥ 2` the base geometry is entirely connection-generated — the connection-independent floor of `h^ω` has rank ≤ 1 for the declared Gaussian fiber, so some `ω` makes `det h ≡ 0` for every section. "Geometry from information" has no content there without a principled connection selection.
- **O** Cross-agent aggregation theorem — `overview.md` §2.2 currently declines it.

---

## 4. Verification and hygiene

- **Validated ledger is stale.** `.verification/ledger.json` is pinned to `d892374`; HEAD is many commits past it. Eight claims, **seven at high severity, none verified** — all `INCONCLUSIVE` or `LLM_SUPPORTED`. Re-running the closure is the single most overdue task.
- **Witness scripts** (seeded, assert in-script): `u1_two_path_holonomy_witness.py` (4 checks + `tests/`), `kl_expansion_check.py`, `meta_agent_coherence_witness.py` (7 claims), `shared_latent_coupling_witness.py` (6 claims).
- **Test suite**: 21 failed / 1092 passed / 15 skipped. 19 failures bind to a `.codex` path outside the repo; 2 are a `render_figures` contradiction between the launchers and their tests. None are numerical.
- **`Theory/` is read-only** except `PIFB2.tex` and `references.bib`, recorded as post-snapshot additions in `docs/theory-provenance.md`. The live PIFB2 authority is `Desktop/Research/manuscripts/PIFB2.tex`, byte-identical.
- **Provenance caution.** `wave2-*`, `rm-0*` and `panel*` are this programme's own multi-agent audit returns, not external review. Panel B returns had no adversarial pass.

---

## 5. Standing claim discipline

Say: PIFB2 is a gauge-motivated **effective action**; selected sectors admit **exact ELBO realizations**; the grid code is a discretization *candidate*; the base is a **context** manifold; connection-relative Fisher pullbacks give gauge-invariant positive-semidefinite **semi**geometries.

Do not say: that the complete action has been derived from the exact ELBO; that `C` is space; that a Fisher pullback is automatically nondegenerate or Lorentzian; that one bit equals `ℏ`; that any construction is **first** or **novel** without a literature check citing Dennis (2025) and Sengupta et al. (2016); or that an internal audit return is external refereeing.
