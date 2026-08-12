# rm-03 — Referee report on the PIFB2 continuum action class

**Document under review:** `MultiAgentELBO/docs/research-plans/2026-08-12-pifb2-continuum-roadmap.md`
**Standard applied:** the document's own, line 11 — *"Effective field theories are designed from
primitives, symmetries, locality, admissible operators, and scale assumptions. The danger is
uncontrolled arbitrariness: adding terms without a classification principle…"*
**Date:** 2026-08-12
**Compute:** CPU only. All numerical claims below were executed (numpy/scipy/sympy); outputs quoted inline.

---

## 0. Verdict

**The classification principle exists, the roadmap already owns every piece of it, and the roadmap
does not state it.** The missing principle is not exotic: it is **Chentsov/Csiszár invariance** —
require every term to be a functional of the *laws*, invariant under sufficient statistics and
Markov morphisms of the declared sample spaces, in addition to the local gauge group. Under that
principle the admissible-operator list at derivative order ≤ 2 is short, computable, and **contains
four of the roadmap's six sectors as *derived*, uniquely-fixed objects**. That is a much better
result than the roadmap claims for itself.

It also produces three things the roadmap does not have:

1. **The Yang–Mills term is not admissible as written.** For non-compact `G` (the ontology's own
   default, and the code's `GL(K)`) there is no positive Ad-invariant form on `𝔤`; `κ‖F_A‖²` is
   either gauge-invariant and **unbounded below**, or positive and gauge-variant. Verified.
   There is a repair, and it is *in the enumerated list*: the Fisher-dressed curvature.
2. **The peer sector is variationally hollow if `L_ij` is a free field.** Verified numerically:
   `inf_{L∈GL(K)} KL(q_i‖L q_j)` depends on **nothing but two scalars**
   `m_i = μ_i^T Σ_i^{-1} μ_i`, and is exactly zero when `m_i = m_j`. The missing operator is the
   lattice-gauge plaquette/Wilson term tying `L` to the holonomy of `A`.
3. **Three admissible order-2 operators are absent**, and their absence is what makes the theory
   phenomenologically indistinguishable from a Markov random field: the **mixed gradient-alignment**
   term (the only operator that makes *peer* interaction propagate in the base), the **attention
   Dirichlet** term, and the **topological** terms (which are the *only* ones compatible with the
   parent project's "no intrinsic base geometry" commitment N1).

On falsifiability the blunt answer is **no, not as specified**. Of E7's five observables, three
(correlation length, consensus rate, scaling) are absorbed by `η_q/λ`, `τ_q` and `π_ij`; one
(holonomy response) is identically trivial in the implemented Regime I; and one (**defects**) is
**vacuous by topology** in the implemented realization — the order-parameter manifold is
`GL⁺(K)/SO(K−1) ≃ S^{K−1}`, and `π_n(S^{K−1}) = 0` for all `n < K−1`, so at `K_q ∈ [64, 768]` and
`d ∈ {1,2,3}` the theory predicts **exactly zero stable topological defects**. E7 as written cannot
distinguish PIFB2 from a Fisher-Rao MRF. Section 3 gives the repair: the only content the parameter
freedom *cannot* absorb is **universal** — critical exponents of the `O(K)`/Stiefel universality
class, defect classification, Goldstone counting, Ward identities.

Severity roll-up: **2 FATAL, 6 STRUCTURAL, 7 TECHNICAL, 3 COSMETIC.** Lines 9–11, 66, 104 and 106 of
the roadmap are, on inspection, correct and unusually candid; §8 records what should *not* be changed.

---

## 1. The operator enumeration (Question 1 — the central deliverable)

### 1.1 (i) Fields and transformation laws

| Symbol | Type | Gauge weight under `g: 𝒞 → G` | Base weight | Status |
|---|---|---|---|---|
| `q_i, p_i` | section of `E_q = P ×_{ρ_q} ℳ_q` over `U_i` | `q ↦ ρ_q(g)·q` (fiber diffeo) | scalar | dynamical (`p_i` = shadow/background) |
| `s_i, r_i` | section of `E_s` over `U_i` | `s ↦ ρ_s(g)·s` | scalar | dynamical (`r_i` background) |
| `A` | principal connection on `P` | `A ↦ gAg^{-1} − dg·g^{-1}` | 1-form | dynamical (Regime II) / pure gauge (Regime I) |
| `L^q_ij, L^s_ij` | automorphism of the fiber over `U_i∩U_j` | `L ↦ ρ(g) L ρ(g)^{-1}` (**adjoint type**) | scalar | undeclared: field or data |
| `β_ij, γ_ij` | simplex-valued | **singlet** | scalar | dynamical, eliminated at T3 |
| `χ_i, χ_ij` | `[0,1]`-valued | **singlet** | scalar | background (no EoM) |
| `π^q_ij, π^s_ij` | simplex-valued | **singlet** | scalar | background |
| `o` | observation data | see §4, T-9 — **breaks the symmetry** | scalar | background |
| `μ` | positive finite measure | singlet | density | background |
| `g^{-1}_𝒞` | base cometric (line 32) | singlet | `(2,0)` tensor | background |

Two derived objects the roadmap does not name but which the enumeration needs:
- `φ := log(dμ / dvol_g)` — a **dilaton**, manufactured by declaring `μ` and `g` independently.
- the **fundamental vector field** `X·q` of `X ∈ 𝔤` acting on the fiber; its Fisher norm is the
  only positive Ad-invariant form available (§1.4, O2.6).

### 1.2 (ii) Which symmetry group is being imposed

The roadmap never says. Four candidates, only one of which it actually uses:

| Package | Content | Status in the roadmap |
|---|---|---|
| **S1** | diagonal local gauge `𝒢 = C^∞(𝒞, G)` acting on **all agents simultaneously** | **imposed** (T2). Note it is *one* `g(c)` shared by `N` agents, not one per agent — so `Ω_ij = U_iU_j^{-1}` and `L_ij` are adjoint-type, and only `(N−1)dim G` of the `N dim G` frame functions are gauge-removable. |
| **S2** | S1 **+ statistical invariance**: every term is a functional of the *laws*, invariant under sufficient statistics / Markov morphisms of the declared sample spaces (Chentsov, Csiszár) | **available and not invoked**. This is the missing classification principle. |
| **S3** | S2 + `Diff(𝒞)` — no non-dynamical background tensors | **impossible** as the action stands: `μ`, `g^{-1}`, `χ_i`, `U_i` are all background. Only topological terms survive S3. |
| **S4** | S2 + agent permutation `S_N` | **not imposed**: `π_ij`, `L_ij`, `χ_i` are agent-labelled data. The action is `S_N`-*covariant*, not `S_N`-invariant. Fine, but it means the agent index carries physical content and `N → ∞` has no symmetry-protected limit. |

**S1 alone constrains almost nothing.** Any `G`-invariant function of the fiber points is admissible.
For the Gaussian/`GL⁺(K)` realization the invariant ring of `ℳ_q` is generated by the single scalar
`m = μ^T Σ^{-1} μ` (verified: `(gμ)^T(gΣg^T)^{-1}(gμ) = μ^TΣ^{-1}μ`), so S1 admits an entire
**free function** `V(m_i)` at derivative order 0. The roadmap's action contains no such term. Under
S1 that omission is arbitrary. **Under S2 it is derived**: `m = 2·KL(𝒩(μ,Σ)‖𝒩(0,Σ))` requires a
distinguished origin on the sample space, and a translation `x ↦ x + a` is a bijection hence a
sufficient statistic, so `m` is not S2-invariant. *S2 explains an omission S1 cannot.* That is the
first evidence S2 is the right principle.

### 1.3 (iii)+(iv) The enumeration, order by order, against the action

Contractions available: fiber = Fisher `g^F` (S2-canonical, **unique up to scale by Chentsov**);
base = `g^{-1}` (background, S3-forbidden); `𝔤` = **none positive and Ad-invariant for non-compact `G`**.

| # | Operator | S1 | S2 | In action (74–102)? | Verdict |
|---|---|---|---|---|---|
| **Order 0** ||||||
| O0.1 | `Λ · 1` (cosmological) | ✓ | ✓ | no | COSMETIC. Non-trivial once `φ ≠ 0` (O2.9). |
| O0.2 | `V(q_i)` — `G`-invariant single-law potential; `= V(m_i)` for Gaussian/`GL⁺` | ✓ (free function) | **✗** | no | **S2 justifies the omission.** Principle is predictive. |
| O0.3 | `D_f(q_i‖p_i)` | ✓ | ✓ (`f`-divergences are *exactly* the Markov-invariant two-law functionals) | **yes** | **DERIVED**, up to the choice of convex `f`. |
| O0.4 | `λ_s D_f(s_i‖r_i)` | ✓ | ✓ | **yes** | **DERIVED.** `λ_s` is a genuine free coupling. |
| O0.5 | `D_f(q_i‖L^q_ij q_j)`, `D_f(s_i‖L^s_ij s_j)` | ✓ (needs `L` adjoint-type) | ✓ | **yes** | **DERIVED**, given `L`. See F-2 for what `L` costs. |
| O0.6 | `D_f(q_i‖Φ(s_i))` — **belief↔model coupling**, `Φ: ℳ_s → ℳ_q` equivariant | ✓ | ✓ | **NO** | **MISSING, STRUCTURAL.** Without it the fast and slow channels touch only through `ℒ^obs`; the cross-scale-shadow story has no continuum representative and T5's EL system is block-triangular. |
| O0.7 | `τ_q D_KL(β_i‖π^q_i)` and `𝔼_{β_i}[D_q]` — **iff `β_i` is declared a section of a categorical bundle `E_ℓ`** | ✓ | ✓ | **yes** | **DERIVABLE ONLY AFTER A DECLARATION THE ROADMAP DOES NOT MAKE.** See §1.5 — this is the single highest-value repair. |
| O0.8 | `𝔼_{q_i}[−log p(o|k)]` | **✗** (see T-9) | **✗** (cross-entropy shifts by `𝔼_q[log|det J|]` under a sample-space bijection) | **yes** | **The unique symmetry-breaking term.** PIFB2 independently found this (`PIFB2.tex` §"Explicit Symmetry Breaking via Observations"; and the `−½Σ_i^{-1}` env-agent discrepancy is exactly the entropy that separates KL from cross-entropy). The principle *predicts where the anomaly sits*. |
| O0.9 | `𝔼_{γ_i}[D_q]`, `𝔼_{β_i}[D_s]`, joint label law `ζ_i(j_q,j_s)` | ✓ | ✓ | no | MISSING, TECHNICAL. `β ⟂ γ` is postulated, not derived. |
| **Order 1** ||||||
| O1.1 | `⟨J, D^A q_i⟩` with background 1-form `J` | ✓ if `J` declared | ✓ | no | **Correctly absent** — no such data is declared. |
| O1.2 | `⟨dχ_i, ·⟩`, `⟨dβ, ·⟩` | total derivatives | — | no | **Correctly absent.** |
| — | *The order-1 sector of the enumeration is empty and the action's order-1 sector is empty — the one place where the roadmap's list is provably complete.* | — | — | — | **COMPLETE** |
| **Order 2** ||||||
| O2.1 | `η_q g^{μν} g^F(D^A_μ q_i, D^A_ν q_i)` | ✓ (2-param family on the SPD sector) | ✓ **and UNIQUE up to scale** (Chentsov) | **yes** | **DERIVED AND UNIQUE.** Strongest term in the action. S2 is what pins `b = 0` in PIFB2's own two-parameter family `a tr(Σ^{-1}UΣ^{-1}V) + b tr(Σ^{-1}U)tr(Σ^{-1}V)` (`PIFB2.tex:2323`). Cite Chentsov and the term stops being a choice. |
| O2.2 | `η_s ‖D^A s_i‖²` | ✓ | ✓ | **yes** | **DERIVED AND UNIQUE.** |
| O2.3 | `η_ij g^{μν} g^F(D^A_μ q_i, (L^q_ij)_* D^A_ν q_j)` — **mixed gradient alignment** | ✓ | ✓ | **NO** | **MISSING, STRUCTURAL.** The action's entire peer sector is order-0, i.e. **ultralocal in the base**: agents interact only at coincident base points. E4 asks "do spatial terms create genuine base propagation?" — as written, only the *self*-Dirichlet term propagates, and peers never exchange information across base points. This is the natural exchange/ferromagnetic operator and the best candidate for an E7-discriminating term. |
| O2.4 | `η_β g^{μν} Σ_j ∂_μβ_ij ∂_νβ_ij / β_ij` — **attention Dirichlet** (Chentsov-canonical on the label simplex) | ✓ | ✓ | **NO** | **MISSING, STRUCTURAL.** With `η_β = 0`, `β` is eliminated pointwise (T3) and carries no compactness; the reduced integrand is merely measurable in `c`, which is exactly the regularity T8's Γ-convergence will lack. |
| O2.5 | `‖dχ_i‖²`, `χ_i‖D^A q_i‖²` | ✓ | ✓ | partial | See T-5. `χ_i` weights (a) and (b) but **not** (d). |
| O2.6 | `κ‖F_A‖²_{Killing/trace}` | **✗ for non-compact `G`** | ✗ | **yes** | **FATAL (F-1).** See §1.4. |
| O2.6′ | `κ g^{μα}g^{νβ} g^F_{q_i}(F_{μν}·q_i, F_{αβ}·q_i)` — **Fisher-dressed curvature** | ✓ | ✓ | no | **THE REPAIR. In the enumerated list.** §1.4. |
| O2.7 | `Σ_{ijk} Re tr(L_ij L_jk L_ki)` or `‖L_ij − 𝒫exp(−∫_γ A)‖²` — **plaquette / Wilson** | ✓ | ✓ | **NO** | **FATAL (F-2).** Without it `L` is a free field with no cost; see §1.6. This is also precisely the object E2 needs to compare "transition vs physical link". |
| O2.8 | `∫tr(F∧F)` (`d=4`), `∫tr F` (`d=2`, the `det`-`U(1)` factor of `𝔤𝔩(K)`), Chern–Simons (`d=3`) | ✓ | ✓ | **NO** | **MISSING, STRUCTURAL.** These are **metric-independent**, hence the *only* operators in the whole enumeration that survive **S3**. If the parent project's N1 ("no intrinsic base geometry", `audit-06:419`) is to be kept, the topological sector is the entire admissible derivative sector and `η, κ` must go. |
| O2.9 | `e^{nφ}`, `‖dφ‖²` with `φ = log(dμ/dvol_g)` | ✓ | ✓ | no | MISSING, TECHNICAL — manufactured by the roadmap's own line-32 decision. |
| **Order 4** ||||||
| O4.* | `‖F‖⁴`, `‖D^Aq‖⁴`, `(Δq)²` | ✓ | ✓ | no | Correctly truncated **iff** `ξ ≫ mesh` (§2). E3 tests exactly this. |

### 1.4 F-1 — the Yang–Mills term, verified

Executed (`numpy`, `K=4`, 2000 random `X ∈ 𝔤𝔩(4)`):

```
tr(X²) on gl(4):  min = −18.136   max = +29.845          → INDEFINITE
skew X:           tr(X²) = −6.889                        → κ‖F‖² unbounded below
Frobenius tr(XᵀX): ‖X‖² = 21.232 → ‖Ad_g X‖² = 109.375   → NOT Ad-invariant
```

So for `G = GL(K)` — the ontology's stated default and the code's actual group — you may have gauge
invariance **or** positivity, never both. This is not a technicality: **T4 (existence of minimizers)
requires coercivity, and the trace-form YM term destroys it in every skew direction of `𝔤`.**
Line 13 says compactness of `G` "may be imposed … as analytical hypotheses, not as ontological
commitments." That is exactly backwards for this term: **the presence of `κ‖F_A‖²` *forces* an
Ad-invariant positive form on `𝔤`, i.e. `G` compact (× abelian). The roadmap declines the
commitment its own action requires.**

**The repair is in the list.** The infinitesimal `𝔤`-action on the fiber supplies a
gauge-covariant positive form that `𝔤` itself does not have. Verified:

```
tr(F Σ Fᵀ Σ⁻¹) under F ↦ gFg⁻¹, Σ ↦ gΣgᵀ:  max gauge-variation over 500 samples = 7.06e−08
                                             min value over 500 samples = 6.437  (> 0)
full Fisher norm of the generator X∈gl(K) at (μ,Σ):  min over 500 = 5.273  (PSD)
generator in the stabiliser so(K−1):                 Fisher norm = 0.000000  (exact kernel)
```

Algebraically `tr(FΣFᵀΣ⁻¹) = ‖S⁻¹FS‖²_F` for `Σ = SSᵀ`, manifestly ≥ 0. So

> **O2.6′.**  `κ ∫ g^{μα}g^{νβ} g^F_{q_i}(F_{μν}·q_i, F_{αβ}·q_i) dμ`

is gauge-invariant, positive semidefinite, and degenerate **exactly** on the stabilizer algebra.
`κ` becomes a **field-dependent gauge coupling function** — entirely standard EFT practice (the
gauge kinetic function of a supergravity/string EFT), not an ad hoc dressing. Caveat to state
honestly: it is only positive *semi*definite, so it gives no coercivity in stabilizer directions;
those need either gauge fixing or an explicit mass/Higgs term.

### 1.5 The highest-value repair: declare the label bundle

`τ_q β_ij log(β_ij/π^q_ij)` looks like the paradigm "engineered" term. It is not — **provided one
extra declaration is made.** Add a third associated bundle

> `E_ℓ = P ×_{triv} Δ^{N−1}`, with `β_i ∈ Γ(E_ℓ|_{U_i})` a **categorical statistical section**
> (gauge singlet), `π^q_i` its background reference law.

Then, mechanically, from the same enumeration:
- `τ_q Σ_j β_ij log(β_ij/π^q_ij) = τ_q D_KL(β_i ‖ π^q_i)` **is O0.3** on the label fiber.
- `Σ_j β_ij D_q(q_i‖L_ij q_j) = 𝔼_{β_i}[D_q]` **is the canonical order-0 mixed invariant** (expectation
  of an `f`-divergence under a label law) — the same object the observation term is.
- `η_β‖D β_i‖²_{Fisher}` (O2.4) is then the *forced companion* the action is missing.

This converts sectors (b) and (c) from "effective interaction terms" (line 106) into **enumerated
members of the S2 list**, and it is precisely PIFB2's own mixture-of-sources / source-label
enlargement made kinematic instead of rhetorical. **Recommendation: WP0 should declare `E_ℓ`.**
Cost: it obliges the theory to give `β` a kinetic term, which changes T3 (no longer a pointwise
elimination) and T8 (now with the compactness it needs).

### 1.6 Summary of the comparison the brief asked for

| | Terms |
|---|---|
| **In the action AND in the enumerated list** | `D_q(q_i‖p_i)`, `λ_s D_s(s_i‖r_i)`, `D_q(q_i‖L^q_ij q_j)`, `D_s(s_i‖L^s_ij s_j)`, `η_q‖D^Aq‖²_{g^F}`, `η_s‖D^As‖²` — **six terms, all derived, two of them (the Dirichlet pair) unique up to scale.** |
| **In the action, in the list only after an undeclared enlargement** | `τ_q β log(β/π)`, `τ_s γ log(γ/π^s)`, `Σ_j β_ij D_q(·)` — admissible once `E_ℓ` is declared (§1.5). |
| **In the action, NOT derivable from any stated symmetry** | `κ‖F_A‖²` (F-1: not even well-signed for the stated `G`); `ℒ^obs` (the deliberate symmetry-breaking source — fine, but it must be *labelled* as such, not as an invariant term); `𝒮_{boundary/prior}` (unspecified functional). |
| **In the list, MISSING from the action** | `D_f(q_i‖Φ(s_i))` (O0.6); mixed gradient alignment (O2.3); attention Dirichlet (O2.4); plaquette/Wilson `L`–`A` coupling (O2.7); topological terms (O2.8); dilaton sector (O2.9); Fisher-dressed curvature (O2.6′). |

The last row is the interesting one. **The action is not over-full; it is under-full in exactly the
places where genuinely distinguishing physics would live** (spatial peer propagation, `L`-`A`
compatibility, topology). The arbitrariness the roadmap warns about is present, but it is
arbitrariness of *omission* more than of addition.

---

## 2. Power counting and scaling dimension (Question 2)

### 2.1 The assignment

Take `[𝒮] = 1` (nats — PIFB2 is explicit: *"ℱ is dimensionless in nats while a physical action
carries units of action"*). T7 forces `μ({∗}) = 1`, so **`μ` is a probability-like finite measure,
`[μ] = 1`, and `μ ≠ vol_g`.** Let `ℓ` be the length supplied by the line-32 cometric.

| Object | Dimension |
|---|---|
| `𝒞` | bare index manifold; `ℓ` enters only through `g_𝒞` |
| `μ` | `1` (finite, normalizable) |
| fiber coordinates `(μ_i, Σ_i)`, `q_i` | `1` (a law is dimensionless) |
| `D_q, D_s, β log β` | `1` (nats) |
| `λ_s, τ_q, τ_s, β_ij` | `1` |
| `‖D^A q‖²_{g^F}` | `ℓ^{-2}` ⇒ `[η_q] = [η_s] = ℓ²` |
| `‖F_A‖²` | `ℓ^{-4}` ⇒ `[κ] = ℓ⁴` |

### 2.2 Does line 32 rescue the EFT analogy? Partially, and at a price.

**It does supply a derivative expansion.** With `g_𝒞` declared, "order 2" is meaningful and higher
operators are suppressed. **It does not supply a scale.** The overall normalization of `g_𝒞` is
undetermined; `g → s²g` sends `η → η/s²`, `κ → κ/s⁴` and changes nothing observable. So `η_q, η_s, κ`
are not independently meaningful — only ratios are. There is exactly **one** emergent length:

> `ξ² := η_q / m_q²`, where `m_q²` is the second variation of the pointwise (order-0) sector.
> Dimensionless gauge coupling: `κ̂ := κ m_q² / η_q²`.

**Consequence for the EFT rhetoric.** "Irrelevant operator" here means *suppressed by `(a/ξ)^{2n}`
where `a` is mesh spacing*. That is a statement about **discretization error**, not about physics —
there is no independently measurable short-distance scale for the operator expansion to be an
expansion *in*. E3 (mesh refinement) tests it and is the right test. But the honest framing is:
**the theory is a Landau/sigma-model expansion around a smooth configuration, not a Wilsonian EFT
with a physical cutoff.** The roadmap should say "gradient expansion", not "effective field theory",
wherever the analogy is doing justificatory work.

### 2.3 The ontological cost of line 32

Three separate costs, one of them a live contradiction with the parent project:

1. **N1 collision.** `PIFB2.tex def:base_manifold` and `:2129` say `𝒞` "carries only the smooth index
   structure" and "no agent-independent geometry exists in the formalism"; `audit-06:419` states N1
   as "𝒞 carries no metric, no measure, no distinguished connection". `wave2-01:109` records the same
   for `μ`. **Line 32 declares a cometric. That is a direct contradiction with N1, and it is
   load-bearing** — every derivative term in the action needs it.
2. **A dilaton for free.** Declaring `μ` and `g` *independently* creates the gauge-invariant scalar
   `φ = log(dμ/dvol_g)` with no kinetic term and no equation of motion, rescaling every term by
   `e^φ`. Admissible operators `e^{nφ}`, `‖dφ‖²` are in the list and absent from the action.
   **Fix: set `μ = vol_g` and be done, or declare `φ` as a field.**
3. **The line-32 alternatives are not variants of one another.** The roadmap offers "a regulated
   section-induced metric or a declared nonlocal kernel" as escapes. The section-induced route
   replaces `g^{μν}` by the pullback `h = σ*g^F` — but then `‖D^Aq‖²_h` is built from `D^Aq` itself,
   turning the Dirichlet energy into a **volume (Nambu–Goto) functional**, degenerate wherever
   `rank h < d` (which `wave2-01` notes is *generic*: `rank h ≤ min(K, dim𝒞)`). **This is
   Polyakov versus Nambu–Goto, and only the Polyakov (declared-metric) form supports T1–T4 as
   stated** — the direct method in manifold-valued `H¹` does not apply to a degenerate volume
   functional.
   **Constructive fix:** keep the quadratic form but make `g_𝒞` an **auxiliary, non-propagating
   field** varied in the action (the Polyakov trick). On-shell it becomes the induced metric,
   restoring N1 ("no *primitive* base geometry"), while off-shell the functional stays quadratic and
   T4 goes through. In `d ≠ 2` this is not Weyl-invariant and generates a cosmological term (O0.1),
   which is why O0.1 should be in the action.

---

## 3. Free parameters versus predictions (Question 3)

### 3.1 The count

Counting real-valued free **functions on the base** (one "function" = one free field over `𝒞`),
for the realization the code actually implements:

| Free data | `N=8, d=2, K=3` | `N=64, d=2, K=64` | `N=1024, d=1, K=768` |
|---|---|---|---|
| scalar couplings `λ_s,τ_q,τ_s,η_q,η_s,κ` | 6 | 6 | 6 |
| base measure `μ` | 1 | 1 | 1 |
| base cometric `g` (line 32) | 3 | 3 | 1 |
| supports `χ_i, χ_ij` | 36 | 2 080 | 524 800 |
| attention priors `π^q_ij, π^s_ij` | 112 | 8 064 | 2 095 104 |
| comparison maps `L^q_ij, L^s_ij` | **1 008** | **33 030 144** | **1 235 742 621 696** |
| priors/hyper-priors `p_i, r_i` | 144 | 274 432 | 606 339 072 |
| connection `A` | 18 | 8 192 | 589 824 |
| **total free base-functions** | **1 328** | **33 322 922** | **1 236 352 170 504** |
| dynamical fields solved for (`q_i, s_i, A`) | 162 | 282 624 | 606 928 896 |
| **ratio free-data : dynamical-DOF** | **8.2 : 1** | **117.9 : 1** | **2 037 : 1** |

Plus **five infinite-dimensional choices**: the convex `f` fixing `D_q`; the convex `f` fixing `D_s`;
the observation likelihood family `p(o|k,m)`; `𝒮_{boundary/prior}` (entirely unspecified); and the
statistical families `ℳ_q, ℳ_s` themselves. Plus the discrete choices of `G`, `ρ_q`, `ρ_s`.

The dominant term is `L_ij` — `2N(N−1)dim G` functions — which the enumeration also shows has **no
cost term** (F-2). That combination (largest parameter block, zero action cost) is the worst
possible.

### 3.2 Which parameter absorbs which E7 observable

| E7 observable | Absorbing parameter | Verdict |
|---|---|---|
| **correlation length `ξ`** | `ξ² = η_q/m_q²`, and `m_q²` is itself tunable through `τ_q` (sharper attention ⇒ larger effective peer stiffness) and through `π_ij`. Any measured `ξ` is matched by one number. | **fully absorbed** |
| **consensus rate** | the T6 mobility ("integrated product Fisher metric **or another declared mobility**" — the roadmap explicitly leaves this open), plus `τ_q`, plus `π_ij`. Rate is a free reparameterization of flow time. | **fully absorbed** |
| **defects** | *not* a coupling — set by the topology of `G/H`. But see §3.3: **vacuous in the implemented realization.** | **vacuous, not absorbed** |
| **holonomy response** | identically trivial in Regime I (`F = 0` by Maurer–Cartan, `PIFB2.tex:142`); in Regime II it is set by the free boundary data of `A` and by `κ̂`. E2 already knows this. | **absorbed or trivial** |
| **scaling behaviour** | `τ = κ√K_q` is *chosen* to produce the observed dimension scaling (`PIFB2.tex:1231` derives `√d_k` from a variance argument *about the observed data*). Fitting `PPL = aK^b + c` with three free constants is not a prediction. | **fully absorbed** |

**Blunt answer: as specified, E7 is not a falsification test. Four of five observables are absorbed
by parameters the roadmap itself lists as free, and the fifth is empty.**

### 3.3 Why "defects" is empty in the realization that exists

The peer-sector order-parameter manifold is `G/H` with `H = Stab_{GL⁺(K)}(μ_i, Σ_i)`. For `μ_i ≠ 0`
this is `SO(K−1)`; `GL⁺(K)` deformation-retracts to `SO(K)`, so

> **order-parameter manifold `≃ SO(K)/SO(K−1) = S^{K−1}`**, and `π_n(S^{K−1}) = 0` for all `n < K−1`.

| `K` | `dim GL⁺` | `dim Stab` | vacuum manifold | lowest non-vanishing homotopy |
|---|---|---|---|---|
| 2 | 4 | 0 | `S¹` | `π₁ = ℤ` |
| 3 | 9 | 1 | `S²` | `π₂ = ℤ` |
| 4 | 16 | 3 | `S³` | `π₃` |
| 64 | 4 096 | 1 953 | `S⁶³` | `π₆₃` |
| 768 | 589 824 | 293 761 | `S⁷⁶⁷` | `π₇₆₇` |

Stable defects in base dimension `d` need `π_{d−1}` or `π_{d−2}` non-trivial. At the code's operating
point (`K_q` in the tens-to-hundreds, `d ∈ {1,2,3}`) **every relevant homotopy group vanishes and the
theory predicts exactly zero stable topological defects.** If `μ_i = 0` is admitted the vacuum is
`GL⁺(K)/SO(K)` ≃ point — contractible — and there are none at all.

**Constructive fix, and it is a real prediction.** Defects require a vacuum manifold with non-trivial
low homotopy. Two principled routes, both fixed by *discrete* data that no coupling can absorb:
- **compact `G`, small `K`**: `G = SO(3)`, `K = 3`, `d = 3` ⇒ `π₂(S²) = ℤ` ⇒ **hedgehogs**, with the
  known `O(3)`-model core structure and a pre-registrable core size `∼ ξ`.
- **gauge the discrete stabilizer**: let `L_ij` include `−I`, so the order parameter is a *director*
  not a vector and the manifold is `ℝP^{K−1}` ⇒ `π₁(ℝP^{K−1}) = ℤ₂` ⇒ **half-integer disclinations in
  `d = 2`**, with the nematic-universality energy `∼ (π/4)·η_q·log(R/a)` (a *parameter-free* ratio to
  the integer-defect energy). This is falsifiable, cheap, and CPU-testable.

### 3.4 What *is* falsifiable, given the parameter freedom

Only **universal** content survives. Recommend pre-registering exactly these for E7:

1. **Critical exponents.** The theory *is* a gauged nonlinear sigma model into `G/H ≃ S^{K−1}`
   (§6.3). Its universality class is fixed by `(d, K, symmetry-breaking pattern)`, i.e. `O(K)`.
   `ν, η, γ` are parameter-free and no coupling can move them. A Fisher-Rao MRF with the same
   order parameter lands in the *same* class — so this tests the *sigma-model* claim, not the
   *gauge* claim.
2. **Defect classification and defect-energy ratios** (§3.3) — discrete, rigid.
3. **Goldstone counting.** `dim G/H = K²−(K−1)(K−2)/2` gapless modes with `ω ∝ k²` under
   dissipative flow. A count, not a fit.
4. **Ward identities / gauge covariance residuals** — E1 already does this correctly.
5. **Finite vs infinite propagation speed** (§6.1) — the sharpest cheap discriminator, and it is not
   currently in E7.

**Recommendation for WP6's exit gate:** replace "at least one pre-registered prediction survives
ablations" with "at least one **universal** (exponent / homotopy / counting) prediction survives".
Otherwise the gate is satisfiable by curve-fitting.

---

## 4. Term-by-term typing audit (Question 4)

Line 104's own flagged bug is confirmed as a live bug in the parent manuscript:
`PIFB2.tex eq:free_energy_functional_final` writes `𝔼_{q_i(c)}[log p(o(c)|k_i, m_i)]` with `m_i`
unintegrated. **The roadmap is right and the flag should be carried into WP0 as a correction.**
Here are the others.

| # | Term | Finding | Severity | Fix |
|---|---|---|---|---|
| **T-1** | peer bracket `∫_{U_i∩U_j} χ_ij[β_ij D + τ β_ij log(β_ij/π)]` with `β_i(c) ∈ Δ^{N−1}` | **`χ_ij` multiplies the whole bracket while the simplex constraint `Σ_j β_ij = 1` runs over *all* `j`. Absent neighbours cost nothing and absorb attention mass.** Verified (`N=5`, 3 present, `τ=0.7`): optimal row `[0.074, 0.013, 0.042, 0.855, 0.017]` — **87.2% of the attention mass leaks to non-overlapping agents**; row value `−0.0899` versus the correctly-normalized `+0.7370`. **T3's closure obligation — "reduced log-partition values" `−τ log Z` — is FALSE for the action as literally written** (`−τ log Z = 0.7370 ≠ −0.0899`). Discrepancy 0.827 nats per row per point. | **FATAL** | Adopt PIFB2's absorbed-prior convention verbatim: `π̃_ij := χ_ijπ_ij / Σ_k χ_ikπ_ik`, `χ_ij` **inside** the prior, row normalized over the present set. PIFB2 already does this (`:713` ff.); the roadmap **regressed** from it. |
| **T-2** | `Σ_{i,j}` | **Not** double counting — the integrand is asymmetric (forward KL, row-normalized `β`), so ordered pairs are correct. But the **diagonal `j = i` is not excluded**, and `D_q(q_i‖L_ii q_i) = 0` is the *global minimum* of the logit, so `β*_ii ∝ π_ii` always wins the softmax. The strength of the entire consensus sector is therefore set by `π_ii` — another absorbing parameter, undeclared. | TECHNICAL | State whether `j = i` is in the sum; if yes, declare `π_ii` explicitly as the self-vs-peer precision and put it in the ablation list. |
| **T-3** | `β_ij` typing | It is a **field** on `U_i∩U_j` (line 72: "simplex-valued attention fields `β_i(c)`"), per-point simplex. Good news: `β ∈ L^∞` automatically (`‖β‖ ≤ 1`), and the row functional is **strictly convex** — Hessian `diag(τ/β_j)`, eigenvalues `[1.40, 2.33, 3.50]` for `τ=0.7`, `β=(.3,.2,.5)`. **T3's strict-convexity and uniqueness claims are correct.** Bad news: `β log β ∈ [−e^{-1}, 0]` is bounded but `−β log π` is not; "positive row priors" is too weak. | TECHNICAL | Strengthen T3's hypothesis to `log π^q_ij ∈ L¹(χ_ij μ)` (uniform positivity is enough and is what the proof needs). |
| **T-4** | `D_q(q_i ‖ L^q_ij q_j)` with differing supports | `KL = +∞` unless `q_i ≪ L q_j`. For Gaussian fibers, always finite. **For the categorical fiber that E0 mandates, generically infinite on the simplex boundary** — a positive-measure set. T1 says "extended-real conventions at singular boundaries", which is honest but does not give T4 a non-empty sublevel set with the compactness the direct method needs. | STRUCTURAL | Either (i) restrict the admissible set to `{q ≥ ε}` (compact — which T1 already wants), or (ii) use an `f`-divergence bounded on the closure (squared Hellinger, Jensen–Shannon). **Note the tension: (ii) breaks E5's exact-ELBO reading.** T4's analytic needs and E5's probabilistic semantics pull in opposite directions and the roadmap should say which wins. |
| **T-5** | `χ_i` smooth vs indicator; the Dirichlet term | The Dirichlet terms (d) are `∫_{U_i}‖D^Aq_i‖² dμ` **with no `χ_i`**, while (a) and (b) carry `χ_i, χ_ij`. If `χ_i` is smooth (PIFB2's choice, `:713`: "discontinuous `χ_i` would make the integrands distributional at support boundaries"), then the pointwise terms fade at `∂U_i` but the gradient term does not — the EL operator is undamped at the boundary and `𝒮_boundary` must supply BCs that are nowhere specified. If `χ_i` is an indicator, the first variation of (a) carries a boundary measure. | TECHNICAL | Weight (d) by `χ_i` too. **Cost to state honestly:** the operator then becomes degenerate-elliptic where `χ_i → 0`, requiring `χ_i` in the Muckenhoupt class `A₂` for the weighted `H¹` theory T4 uses. |
| **T-6** | `‖F_A‖²` and the base metric | It **does** need a base cometric — two indices to raise, plus a volume. Line 32 anticipates this correctly. But (i) the integration is `dμ` with `μ` independent of `vol_g` (⇒ dilaton, §2.3); (ii) the Ad-invariant-form problem (F-1); (iii) the integral is `∫_𝒞`, not `∫_{∪U_i}`, so outside all supports the term is pure source-free Yang–Mills whose minimizers are flat connections modulo a moduli space — `A` is undetermined there, and `‖F_A‖²` supplies no coercivity on that moduli space. | TECHNICAL (i,iii) / FATAL (ii) | Set `μ = vol_g`; restrict the YM integral to a declared domain or add boundary conditions; use O2.6′. |
| **T-7** | `L^q_ij` transformation law | Correct and correctly diagnosed at line 66. Since one `g(c)` acts diagonally on all agents, `L_ij` is an **adjoint-type** field, so `L_ij = id` is **not** a gauge-invariant condition unless `L` is central. The roadmap's insistence that intrinsic same-fiber comparison needs no transport, and that `Ω_ij = U_iU_j^{-1}` is a coboundary, is exactly right. | — (credit) | — |
| **T-8** | `L^q_ij` as a *free field* | See F-2 below. | **FATAL** | O2.7. |
| **T-9** | `ℒ^obs` and gauge invariance | T2 promises "invariance of `𝒮`". For a fixed observation `o` shared across agents this is **false**: `p(o|k)` would have to be `G`-invariant in `k`, which for transitively-acting `G` forces `p(o|k) = p(o)`. T2's actual content is *covariance of the map (data ↦ solution)* under simultaneous transformation of the data, which is weaker: **the gauge redundancy does not reduce the physical degree-of-freedom count once `o` is fixed.** PIFB2 states this correctly and calls it explicit symmetry breaking; the roadmap's T2 wording does not. | STRUCTURAL | Reword T2: "invariance of the source-free action; equivariance of the full action under simultaneous transformation of section, link, connection **and likelihood** data; explicit breaking by fixed observations." E1's design (transform *all* covariant inputs) already implements the correct statement — only the T2 prose is wrong. |
| **T-10** | frame DOF | `N` frame fields `U_i`, one gauge function `g(c)` ⇒ `(N−1)dim G` physically-relevant relative-frame functions, **none of which has a kinetic term in the action**. Their dynamics comes only from the alignment terms (as PIFB2 states). | TECHNICAL | Either add O2.3/O2.7, or declare the relative frames non-dynamical. |
| **T-11** | measure on each term | (a) `dμ` on `U_i`; (b),(c) `dμ` on `U_i∩U_j`; (d) `dμ` on `U_i`; (e) `dμ` on `𝒞`. **Four different domains, one measure, and `μ` normalized to `μ(𝒞)=1` by T7.** Then `∫_{U_i}` for `N` agents over a normalized base makes the self sector scale like `N·μ(U_i)` while the peer sector scales like `N²·μ(U_i∩U_j)` — the relative weight of self vs peer is a pure function of the *support geometry*, which is background data. | TECHNICAL | Declare the intended `N`-scaling (`1/N` on the peer sector is the usual mean-field normalization) or the large-`N` limit does not exist. |

---

## 5. The five-way taxonomy at line 106 (Question 5)

**Is it well defined and exhaustive? No — but it is *nearly* right and the fix is small.**

**Problem: three orthogonal axes are collapsed into one list.** "exact-local-ELBO / closed-ELBO /
effective" are about **probabilistic provenance**. "gauge-fixing" is about **symmetry status**.
"physical" is about **observability**. These are independent: a term can be *effective* and
*physical* (an effective term with gauge-invariant content — the peer KL, if `L` is frozen), or
*closed-ELBO* and *gauge-fixing*. Labels from different axes cannot be alternatives to one another.

**Also not exhaustive.** Four categories have no home: **kinematic/definitional** (`χ_i`, `μ`, `g_𝒞`
— these are not terms, they are the domain), **regulator** (the `ε`-floor on covariances,
`KL_REGULARISER_EPS = 1e−4`, which PIFB2 notes breaks its own exact invariance to `O(ε)`),
**topological** (O2.8 — metric-independent, no ELBO reading, but genuinely physical), and
**constraint** (the simplex, which is a Lagrange multiplier sector, not an energy).

**Recommended replacement — a 3-axis grid, one label per axis per term:**

| Axis | Values |
|---|---|
| **A. Provenance** | exact local ELBO · closed ELBO · effective · kinematic · regulator |
| **B. Symmetry status** | gauge-invariant · gauge-covariant · gauge-fixing · explicitly breaking (source) |
| **C. Observability** | enters a gauge-invariant observable · pure redundancy · topological · boundary |

Applied to the action: `D_q(q_i‖p_i)` = (exact-local-ELBO, invariant, observable). `β log(β/π)` =
(exact after `E_ℓ` is declared, invariant, observable). `ℒ^obs` = (exact-local-ELBO, **explicitly
breaking**, observable) — the current taxonomy has no box for this and it is the theory's single
most important term. `κ‖F_A‖²` = (effective, invariant-only-if-`G`-compact, observable-only-in-
Regime-II). `λ_φ‖∇φ_i‖²` = (kinematic, **gauge-fixing**, pure redundancy).

### 5.1 "A frame-smoothness term is gauge fixing unless it is reformulated invariantly" — CORRECT

Under `U_i ↦ g U_i` with `g(c)` local, `φ_i = log U_i` transforms inhomogeneously and
`λ_φ‖∇φ_i‖²` is not invariant: it selects a slice through the gauge orbit. **The roadmap's
classification is right.**

**The invariant reformulation it asks for.** The *relative* frames are the gauge-covariant data:
`Ω_ij = U_iU_j^{-1} ↦ g Ω_ij g^{-1}` — adjoint type, the same law as `L_ij`. Hence

> `λ_Ω Σ_{i<j} ∫_{U_i∩U_j} χ_ij ‖D^A Ω_ij‖² dμ`,  `D^A_μ Ω = ∂_μΩ + [A_μ, Ω]`,

with the norm taken in the **Fisher-dressed** form of §1.4 (the Killing form is unavailable for
non-compact `G` — the same obstruction as F-1, and PIFB2 states it independently: *"for non-compact
`G` the Killing form is indefinite and no positive-definite bi-invariant Riemannian metric exists"*).
This is gauge-invariant, positive, and it is a **genuinely different physical term** from the
gauge-fixing one: it penalizes spatial variation of *relative* frames, not of the frame slice. With
`A` frame-derived (Regime I) it degenerates back to redundancy; with `A` independent (Regime II) it
is new physics and is a close relative of the missing plaquette term O2.7.

### 5.2 "A curvature term is physical only when based on genuine connection data" — CORRECT but INCOMPLETE

Correct in the Regime I / Regime II sense: with `A = U^{-1}dU`, `F ≡ 0` by Maurer–Cartan, the term
vanishes identically and `κ` is unidentifiable. `PIFB2.tex:142` establishes this and E2 tests it.
Consistent with the rest of the construction — **credit.**

**Incomplete in two ways.** (i) Even with genuine connection data, `κ‖F_A‖²` is not physical for the
stated group: it is not sign-definite (F-1, verified). Genuine connection data is necessary, not
sufficient. (ii) The term as written is decoupled from the matter sector except through `D^A`; the
Fisher-dressed form O2.6′ makes the coupling explicit and is the version that is simultaneously
invariant, positive, and genuinely connection-dependent. Recommend amending line 106 to: *"a
curvature term is physical only when based on genuine connection data **and contracted with a
positive Ad-invariant form; for non-compact `G` no such form exists on `𝔤` and the contraction must
be supplied by the fiber Fisher metric.**"*

---

## 6. The honest alternatives (Question 6)

| Alternative | What it predicts differently, in one line | Can E7 distinguish it? |
|---|---|---|
| **6.1 Wasserstein/JKO gradient flow** of a free energy on measure-valued fields | **Finite propagation speed**: compactly-supported initial beliefs stay compactly supported, fronts move at finite speed with `x ∼ t^{1/3}`-type scaling. Fisher–Rao/natural-gradient flow has **infinite** propagation speed and exponential relaxation. | **Yes — and this is the sharpest cheap discriminator available.** It is **not in E7.** Add "front speed / support propagation from a compactly-supported perturbation" to E7. Caveat: T6 leaves the mobility metric free ("or another declared mobility"), so the metric must be **frozen in WP0** before this test has content. |
| **6.2 Bethe/Kikuchi region-graph free energy** | Exact on tree-structured overlap graphs; the weights are **messages** satisfying BP fixed-point equations, not a softmax of divergences; characteristic loop corrections and a Bethe-vs-true-free-energy gap that vanishes on trees. | **No, as written.** A tree-vs-loop ablation on the overlap graph would. Recommend adding: run identical configurations on a tree overlap graph and on the same graph plus one chord; Bethe is exact on the first, PIFB2 is not. This is a decisive, CPU-cheap test. |
| **6.3 Gauged nonlinear sigma model into a statistical manifold** | **This is not an alternative — it is the same theory.** Sectors (d)+(e)+the vacuum manifold `G/H` *are* a gauged NLSM with a potential. | **No, and it should not try.** The correct response is to **claim the identification**, which buys the entire off-the-shelf apparatus: `O(K)` universality class, `ε`-expansion exponents, asymptotic freedom in `d=2`, Goldstone counting, Mermin–Wagner (**no long-range order in `d=2` for continuous `G/H` at finite `τ`** — a hard, parameter-free prediction that E7 could check and that would falsify any claimed `d=2` consensus phase). |
| **6.4 Lattice gauge theory with matter in a nonlinear target** | Confinement/Higgs phase structure with **Wilson-loop area vs perimeter law** and Fradkin–Shenker complementarity between the confined and Higgs regions. | **Partially.** E7's "holonomy response" is a crude one-plaquette version. Measuring the Wilson loop as a function of loop area would distinguish. Note this alternative is also the source of the *missing* term O2.7 — the plaquette action. The roadmap is closer to lattice gauge theory than it realizes, and would benefit from adopting its discretization theory wholesale for T8. |
| **6.5 Markov random field with Fisher-Rao potentials** | Identical consensus phenomenology; **no gauge sector at all**, hence no holonomy, no frame DOF, no defects. Correlation length, consensus rate and scaling are **the same functions of the same couplings**. | **NO — and this is the finding that matters.** Three of E7's five observables are shared with this baseline. The two that are not (holonomy, defects) are respectively **trivial in Regime I** and **topologically vacuous at the implemented `K`** (§3.3). **As currently specified, E7 cannot distinguish PIFB2 from a Fisher-Rao MRF.** The only repairs are: promote to Regime II *and* measure Wilson loops (6.4), or engineer a non-trivial vacuum topology (§3.3). |

---

## 7. Ranked findings and fixes

### FATAL — the action is ill-defined or its stated theorems are false as written

**F-1. `κ‖F_A‖²` has no admissible contraction for the stated group.**
Verified: `tr(X²)` on `𝔤𝔩(4)` ranges `[−18.1, +29.8]`; skew directions give `tr(X²) < 0`; the
Frobenius form is positive but not Ad-invariant (`21.2 → 109.4` under `Ad_g`). Gauge invariance and
boundedness below are mutually exclusive. **T4 (existence of minimizers) is false with this term
for non-compact `G`.**
*Fix:* adopt **O2.6′**, the Fisher-dressed curvature
`κ ∫ g^{μα}g^{νβ} g^F_{q}(F_{μν}·q, F_{αβ}·q) dμ` — verified gauge-invariant to `7e−08` and PSD with
kernel exactly the stabilizer. Alternatively commit to compact `G` **ontologically**, not as an
"analytical hypothesis" (line 13).

**F-2. If `L^q_ij` is a field, the peer sector is variationally hollow.**
`L_ij` appears algebraically with no cost term, so `δ𝒮/δL = 0` drives the peer energy to its orbit
infimum. Verified over `GL(3)` by direct numerical minimization:
`inf_L KL(q_i‖L q_j) = 0` to `7e−17` whenever the orbit invariants agree (`m_i = m_j`); and the
infimum depends on **nothing except `(m_i, m_j)`** — spread `2.8e−16` across four completely
unrelated `(μ,Σ)` pairs with the same invariants. It equals a `K`-independent one-dimensional
formula `min_{t>0} ½[(1 + (√m_i − √(m_j t))²)/t − 1 + log t]` (matched to 5 decimals against the full
`GL(K)` optimization at four test points). **The live-peer sector, with `L` free, is a scalar
consensus model on one number per agent.**
*Fix:* either freeze `L_ij` as background data (then own it in the parameter count — it is the
largest block, §3.1), or add the **plaquette/Wilson term O2.7** tying `L` to the holonomy of `A`.
The second is what E2 actually needs and what makes the gauge sector dynamical.

**F-3 (from the typing audit, T-1). Attention mass leaks to non-overlapping agents.**
`χ_ij` outside the bracket + globally-normalized rows ⇒ 87.2% of the row's mass sits on absent
neighbours in a 5-agent test; the reduced value is `−0.0899` where T3 claims `−τ log Z = +0.7370`.
**T3's closure obligation is not derivable from the action as printed.**
*Fix:* restore PIFB2's absorbed-prior convention `π̃_ij = χ_ijπ_ij/Σ_kχ_ikπ_ik`. This is a
one-line regression from the manuscript, not a deep problem.

### STRUCTURAL — unprincipled or unfalsifiable as stated

- **S-1. No classification principle is named.** §1. *Fix:* declare **S2** (Chentsov/Csiszár
  statistical invariance) alongside the gauge group in WP0, and cite it where the Dirichlet term's
  uniqueness and the `f`-divergence class are invoked. This converts six of the action's terms from
  choices into consequences.
- **S-2. The label bundle `E_ℓ` is undeclared**, leaving the attention sector "engineered" when it
  need not be. §1.5. *Fix:* declare it; accept the obligation of an attention Dirichlet term O2.4.
- **S-3. The peer sector is ultralocal in the base.** O2.3 is missing, so peers interact only at
  coincident points and E4's propagation question is answered by the self-Dirichlet term alone.
  *Fix:* add the mixed gradient-alignment operator; it is the natural E7 discriminator.
- **S-4. E7 is not a falsification test.** §3.2–3.4. *Fix:* replace the WP6 exit gate with a
  **universal** prediction (exponents / homotopy / Goldstone counting); add front-speed (6.1) and
  tree-vs-loop (6.2) ablations; either raise the vacuum topology (§3.3) or drop "defects".
- **S-5. Line 32 contradicts the parent project's N1** and its two stated alternatives are
  Polyakov vs Nambu–Goto, not variants. §2.3. *Fix:* make `g_𝒞` an auxiliary field varied in the
  action; set `μ = vol_g`.
- **S-6. T2's invariance claim is too strong** once observations are fixed (T-9). *Fix:* reword to
  equivariance-plus-explicit-breaking; E1's design is already correct.

### TECHNICAL

T-2 (diagonal `j=i` and `π_ii`), T-3 (`log π ∈ L¹`), T-4 (KL infinite on the categorical boundary,
and the T4-vs-E5 tension), T-5 (`χ_i` missing from the Dirichlet term; `A₂` cost of adding it),
T-6 (i,iii) (`μ` vs `vol_g` dilaton; YM domain and moduli), T-10 (relative frames have no kinetic
term), T-11 (`N`-scaling of self vs peer sector is set by background support geometry).

### COSMETIC

O0.1 (cosmological constant absent — becomes non-trivial with a dilaton), O0.9 (`β ⟂ γ` postulated),
and the "effective field theory" phrasing, which should be "gradient expansion" wherever it carries
justificatory weight (§2.2).

---

## 8. Where the roadmap is already right — do not change these

This is a better document than most in its genre, and several of its judgements are ones a referee
would otherwise have had to supply.

1. **Lines 9–11.** Naming the standard, and naming the specific failure mode ("adding terms without
   a classification principle, changing them without empirical penalty, or confusing a useful energy
   with a derived probability model"), is correct and rare. The critique above is that the principle
   was not then supplied — not that the standard was wrong.
2. **Line 104, "This is a class to be narrowed by axioms, not yet a completed theorem."** Correct
   self-typing, and it is what makes the rest of the document reviewable.
3. **Line 104's observation-sector bug** (`𝔼_q[·]` on `k` cannot contain unintegrated `m`) is a
   **real live bug in `PIFB2.tex eq:free_energy_functional_final`**. Confirmed. Good catch.
4. **Line 66** — the separation of Čech transition function, gauge-fixing, and physical link field,
   and the observation that `Ω_ij = U_iU_j^{-1}` is a flat coboundary that cannot generate cycle
   holonomy — is exactly right, is the correct repair of PIFB2's one real category error, and is
   what E2 correctly operationalizes.
5. **Line 106's frame-smoothness verdict** is right (§5.1), and **the curvature verdict is right as
   far as it goes** (§5.2).
6. **Line 13** — refusing to make Gaussian fibers and `GL(K)` ontological — is right, and E0's
   two-family oracle is the correct test of it. (The one exception is `G`-compactness, which F-1
   shows the action *does* require ontologically.)
7. **The order-1 sector.** The action contains no first-derivative operators, and the enumeration
   confirms there are none to contain. This is the one sector where the term list is provably
   complete.
8. **T3's convexity claims** are correct: the row functional has Hessian `diag(τ/β_j)`, strictly
   positive on the open simplex, so strict convexity, uniqueness of `β*`, and the envelope derivative
   all hold — *once* T-1's normalization is repaired.
9. **The Regime I / Regime II discipline** inherited from `PIFB2.tex:142` is carried correctly into
   line 106 and E2, and is the reason the curvature sector's emptiness is documented rather than
   hidden.
10. **The hybrid decision** (line 9, line 28): action-first, ELBO as a consistency layer, with the
    live-peer action explicitly *not* claimed as a state-level ELBO. This is the correct call and it
    is consistent with the parent manuscript's own "ansatz, not a theorem" paragraph.

---

## 9. One-paragraph recommendation for WP0

Declare four things and most of this report's structural findings close at once: **(1)** the
classification principle — local gauge `C^∞(𝒞,G)` **plus** Chentsov/Csiszár statistical invariance,
with the admissible list truncated at two base derivatives; **(2)** the label bundle `E_ℓ`, which
promotes the attention sector from engineered to enumerated; **(3)** the status of `L_ij` — frozen
background *or* dynamical with a plaquette cost, never free-and-costless; **(4)** the base geometry
as an **auxiliary** field with `μ = vol_g`, which keeps N1 and keeps T4's quadratic functional.
Then replace `κ‖F_A‖²` by its Fisher-dressed form, add the mixed gradient-alignment and attention
Dirichlet terms, restore PIFB2's absorbed attention prior, and change WP6's exit gate to require a
**universal** prediction. The resulting action is shorter to justify than the present one, and every
term in it is derived.

