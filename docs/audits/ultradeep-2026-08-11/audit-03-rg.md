# Audit 03 — Coarse-graining, renormalization, scale structure, obstructions

Adversarial rigor audit. Scope: `MultiAgentELBO/Theory/{06_general_coarsegraining, 07_general_renormalization,
07b_agent_network_rg, 09_coarsegraining, 10_renormalization, 11_obstructions}.tex`,
`Theory/appendix_claim_ledger.tex`, `src/multiagent_elbo/finite/{scale_cocycle,scale_cocycle_experiment,
counterexamples,counterexample_experiment,permutations}.py`, and
`Research/manuscripts/PIFB2.tex` §§ Coarse-Graining I–IV and Prospective Validation.

Baseline read: `Theory/SPEC.md`, `Theory/appendix_claim_ledger.tex`,
`docs/audits/2026-08-11-post-fixed-ray-deep-audit.md`.

Everything below marked "verified" was recomputed independently (sympy over ℚ, exact `Fraction`
arithmetic, or numpy) — the exact commands and numbers are in §0.

---

## 0. What I recomputed, and what came out

| Claim | Method | Result |
|---|---|---|
| `thm:rg-gaussian-hermite-spectrum` eigenvalues `b^{1-k/2}` | sympy exact integration of `E[He_k(X)\|Z=z]` for `b∈{2,3,5,7}`, `k=1..8` | **exact match, all 32 cases**. Also Monte-Carlo `N=4e6`, `b∈{2,3,5}`: `b=5,k=1` gives 2.23607 vs 2.23607 (rel err 4e-16); `b=3,k=3` 0.57656 vs 0.57735 (1.4e-3, MC noise) |
| Exponents `y_k = log_b b^{1-k/2} = 1-k/2` | direct | `y_1=1/2` relevant, `y_2=0` marginal, `y_k<0` for `k≥3`. **Matches the standard Gaussian/CLT block-spin fixed point.** |
| Hilbert–Schmidt norm `Σ b^{2-k} = b²/(b-1)` | direct | correct |
| Correlated boundary `b^{1-k/2}[1+(b-1)ρ]^{k/2}` | direct | correct; differs from uncorrelated for every `ρ≠0`, `k≥1` |
| `thm:rg-hoeffding-action-isomorphism` sharpness `(4p-1)^n-(2p-1)^n` | exact enumeration over `{-1,1}^n`, `n=1..4`, `p∈{1/2,3/4,9/10}` | **exact match, all 12 cases**; `→3^n−1` as `p↑1` |
| `prop:rg-contraction-no-fixed-ray` | numpy, 200 alternating iterations | period-2 attractor; even limit `[1, 1.41421356]` = Perron ray of `BA=[[3,2],[4,3]]`; odd limit `[1, 0.70710678]` = `A[1,√2]`. **Correct.** |
| `prop:grg-aggregation-semigroup` `A_{S₂}A_{S₁}=A_{S₁S₂}` | numpy, `K=2`, 6→3→2 blocking | `max\|lhs−rhs\| = 3.55e−15` |
| `prop:obs-holonomy-determinant-factorization` `det J=(det(I−H))²/(det Rₑ det R_f)` | numpy, `K=3`, 3 random draws | exact to machine precision (e.g. `1.573544e−3` both sides) |
| `cor:obs-flat-fold-singular` `dim ker J = K` | numpy, `K=3`, flat `Θ_f=Θ_e^{-1}` | `rank(J)=3` of 6 → `dim ker = 3 = K`, all draws |
| `prop:obs-normalizer-link-dependence` `det(J+p₀I)=p₀²+p₀(a+a⁻¹)²`, `A''(1)=−4/(p₀+4)` | by hand | correct |
| `eq:rg-heat-susceptibility` limit `→α` | Karamata + differentiation by hand | correct: `Γ(α+2)/Γ(α) − (Γ(α+1)/Γ(α))² = α(α+1)−α² = α` |
| `cor:cg-compact-holonomy-barycenter` | independent Reynolds-operator derivation | correct; `P(M(a_H)) = M_{2,H} − a_H a_Hᵀ = C_H`, `C_H ≻ 0`, unconstrained minimizer lies in the constraint set → unique |
| PIFB2 `GL⁺(K)^n → GL⁺(K)` no-go | by hand | correct: `U_j=v^{j-1}`, `v` of order `n` ⟹ `(v−I)F(U)=0`, `F(U)` invertible ⟹ `v=I` |
| **Code:** `cocycle_composition_residual` | ran the fixture construction | **identically 0 by construction** (see RG-2) |
| **Code:** `base_fisher_cocycle_residual_forms` three forms | exact `Fraction`, 5 random nonsymmetric indefinite matrices | **all three identical every time** — tautology (AUD-17, unremediated) |
| **Code:** `retained_beta_diagnostics` three forms | exact `Fraction`, 5 random setups | **all three identical every time** — second, previously unreported tautology (RG-3) |

---

## 1. Headline answers to the audit questions

**Is there an RG at all?** There is a rigorously typed **scale diagram** and a rigorously typed
**derivative cocycle** with a two-parameter composition law (`prop:rg-cocycle-composition`), growth
rates (`def:rg-mode-exponents`), and a beta functional (`def:rg-interaction-beta`). There is **no
verified semigroup**, **no autonomous map on a theory space**, and **no nontrivial fixed point with
a computed relevant/irrelevant spectrum for the agent-network map `T_ℓ^𝒢`**. The semigroup property
`K_{b₁b₂}=K_{b₁}K_{b₂}` is *declared* wherever it is used and never instantiated (RG-1); the code
metric that appears to test it is definitionally zero (RG-2). The only inhabited relevance spectrum
in the manuscript belongs to i.i.d. scalar Gaussians with no agents, no interactions, and no gauge
structure (RG-4). The manuscript is mostly honest about all of this — the defects are of framing,
of one assumed-not-proved hypothesis, and of two code checks that cannot fail.

**Exactness (`thm:rg-exact-coarse-vfe`).** The identity is **correct and unconditional** — it needs
no lumpability, because `P^c` is *defined* as `PC` and the theorem claims nothing about the coarse
theory's form. It is the KL chain rule plus `KL(Q_o‖Π_o)=KL(Q̂_o‖Π̂_o)`. Direction is right (fine
VFE ≥ coarse VFE). Lumpability content lives correctly elsewhere. The word "exact" is nevertheless
load-bearing marketing in the chapter title and closure theorem (RG-9, RG-6).

**Hermite spectrum.** Verified exactly. Standard result, correctly stated, correctly scoped, and the
"fixed Fisher norm" normalization is *explicitly* identified by the manuscript as the sole reason any
eigenvalue exceeds one (`07b:964–971`). No hidden work. **Solid.**

**Fixed points and attraction.** The AUD-20 fallacy (connectedness ⟹ common fixed point) **does not
appear** in `MultiAgentELBO/Theory/`; `06_gaussian.tex:122` explicitly corrects the scalar-graph
intuition for matrix weights. `gaussian_fixed_ray` is **not** promoted: `conj:grg-fixed-b-attraction`
stays CONJECTURE with its three missing obligations named, and the ledger keeps it CONJECTURE. Basin,
existence, uniqueness are properly OPEN. **Solid.**

**Meta-agent / barycenter.** `Theory/` does **not** define the meta-agent as a barycenter (it is a
coarse channel / declared block). The Gaussian forward-KL (M-projection) barycenter is a separate,
correctly proved construction with existence, uniqueness, and a correct Haar-constrained variant.
PIFB2 *does* define the meta-agent as a barycenter and there its frame half is provably not
gauge-equivariant on the actual group (RG-7).

**Tower / Ouroboros.** `Theory/` **refutes** the Ouroboros apex architecture (`cor:obs-flat-fold-singular`,
verified) and replaces it with a truncated tower + declared prior or an apex latent with a proved
contraction theorem. No infinite tower is claimed and no consistency proof is offered or needed.
PIFB2 keeps the apex closure and does not type it against the generative/recognition prohibition
(RG-15). "Same free energy up and down" is **not** proved in either document, and PIFB2 says so
(`1681`, `1685`: parametric form preservation *fails* under Schur elimination on sparse fine graphs).

**Infinite volume / universality.** No thermodynamic-limit-flavored conclusion is smuggled anywhere.
`10_renormalization.tex:422` states outright "Equality of one exponent is not equality of universality
classes." `prop:rg-noncommuting-limits` is a genuine, correctly proved obstruction. **Solid.**

**Monotonicity directions.** Every one checked is correct: `eq:cg-kl-dpi-extended` (KL ↓),
`eq:cg-elbo-monotone` (ELBO ↑), `eq:rg-vfe-chain-rule` (fine VFE ≥ coarse VFE),
`eq:cg-fisher-loss` (`I_Y ⪯ I_X`), `eq:rg-action-lp-contraction`, `eq:rg-extensive-fisher-defect`.
The one place where a "Fisher information increases" reading would be a fatal sign error — the
`√b` replication lift — is explicitly disarmed at `07b:854–869` with a proof that no Markov kernel
realizes replication. **No direction errors found.**

**Obstructions.** Genuinely proved with explicit, verifiable counterexamples, not "we could not do
it". Verified numerically. **Solid.**

---

## 2. Findings

### RG-1 — The RG semigroup is a hypothesis at every use site and is never instantiated
**(OVERCLAIM + VACUOUS/TRUE-BY-CONSTRUCTION, HIGH)**

`Theory/07b_agent_network_rg.tex:2124-2145`:
```
Compatibility means, after the declared canonical identifications,
    K_{b1 b2} = K_{b1} K_{b2}.                                   (eq:rg-kernel-semigroup)
...
Equation~\eqref{eq:rg-kernel-semigroup} makes R_{b1b2} = R_{b2} R_{b1};
otherwise the sequence is a typed cocycle rather than an autonomous semigroup.  \status{ESTABLISHED}
```
The `ESTABLISHED` tag governs only the trivial implication "semigroup ⟹ semigroup". The condition
itself is never verified for any concrete `(C_b, I_b)` pair anywhere in the manuscript.

`Theory/07b_agent_network_rg.tex:2751-2752` then lists, among the ~16 supplied hypotheses of the
closure theorem, "*rescaling kernels satisfying \eqref{eq:rg-kernel-semigroup}*". So the theorem that
is supposed to certify the whole apparatus **assumes** the property that would make it an RG.

The only *proved* semigroup is `prop:grg-aggregation-semigroup` (`10_renormalization.tex:51-70`),
`S₂ᵀ(S₁ᵀΛS₁)S₂ = (S₁S₂)ᵀΛ(S₁S₂)` — associativity of congruence, true for every `S` (verified to
3.6e-15), and it holds **before** the rescaling `ζ_ℓ` and **before** any identification makes the map
an endomorphism. The manuscript itself concedes this twice
(`10_renormalization.tex:82-85`: "Without that identification, \eqref{eq:grg-flow} is a cocycle of
positive maps, not an autonomous dynamical system"; `07:146-148`).

*Fix.* Either (a) exhibit one explicit triple `(C_b, I_b, ζ_b)` — e.g. equal-block Galerkin with
`I_b` the coordinate relabeling and `ζ_b = b^{s_W}` — and verify `K_{b₁b₂}=K_{b₁}K_{b₂}` on the
identified space, with the verification in code; or (b) retag `eq:rg-kernel-semigroup` `HYPOTHESIS`,
say in the chapter abstract that no instance is exhibited, and rename "renormalization" to "scale
cocycle" wherever the semigroup is the operative content. PIFB2's `thm:rg_semigroup`
(`PIFB2.tex:3785-3800`) is the right model: it proves pushforward functoriality and then states
explicitly that it "expresses composability of the coarse-graining morphisms, **not an RG semigroup
acting on a coupling space Θ**".

---

### RG-2 — `cocycle_composition_residual` is identically zero by construction
**(VACUOUS/TRUE-BY-CONSTRUCTION, HIGH — code)**

`src/multiagent_elbo/finite/scale_cocycle_experiment.py:194`:
```python
fine_to_macro = fine_to_middle.compose(middle_to_macro)
```
and `src/multiagent_elbo/finite/scale_cocycle.py:155-163`, `compose` returns
`ExactMarkovChannel(..., _matmul(self.matrix, downstream.matrix))`. Then
`scale_cocycle_experiment.py:365-367`:
```python
channel_cocycle_gap = _maximum_gap(
    direct_channel.matrix, _matmul(first.matrix, second.matrix)
)
```
compares `_matmul(A,B)` against `_matmul(A,B)`. I reran the exact fixture construction:
`direct_channel.matrix IS matmul(A,B) bitwise: True`.

The headline "cocycle" metric of the scale-cocycle lab therefore (i) cannot fail, (ii) cannot detect
any implementation error, and (iii) is not the RG semigroup identity of RG-1 in any case — it is
matrix-product associativity.

*Fix.* Declare the macro-level arrow **independently** in the fixture (a separately given
`fine_to_macro` row set) and check it against the staged composite; that turns the metric into a real
test of Chapman–Kolmogorov consistency of the fixture. Separately, add a test of
`eq:rg-kernel-semigroup` including the rescaling/identification kernels `I_b`.

*(Related but distinct from AUD-09, which flagged inert config toggles in the same file.)*

---

### RG-3 — `retained_beta_diagnostics` cross-check is a second algebraic tautology (extends AUD-17)
**(VACUOUS, MEDIUM-HIGH — code)**

`src/multiagent_elbo/finite/scale_cocycle.py:377-395` computes three "residual forms" and raises
`ArithmeticError("retained beta residual forms disagree")` if they differ. They cannot differ:

- `residual_difference = δ⁻¹[(exact_out − g) − (retained_out − g)] = δ⁻¹(I − R̂)exact_out`
- `residual_identified = δ⁻¹(I − R̂)exact_out` — *literally the same expression*
- `residual_native = δ⁻¹ J (I − R) native_out`, and since `exact_out = J·native_out` and
  `R̂ = J R J⁻¹`, this equals `δ⁻¹(I − J R J⁻¹)J native_out = δ⁻¹ J(I − R)native_out`.

I confirmed over ℚ with 5 random invertible `J` and random idempotent `R`: identical every time.
The exported metric `retained_beta_equivalent_forms_residual` is therefore structurally 0.

AUD-17 flagged exactly this pattern for `base_fisher_cocycle_residual_forms`
(`scale_cocycle.py:438-454`). That finding is **unremediated at this revision** — I confirmed the
function still accepts a nonsymmetric, indefinite `fisher_defect = ((0,5),(-3,-7))` and returns three
equal values (`−23` each). And the same defect now exists in a **second** function that AUD-17 did
not cover.

*Fix.* Make the coarse retained projection an **independently declared** matrix rather than
`J R J⁻¹`, so that the intertwining `R̂ = J R J⁻¹` becomes a testable hypothesis with a nonzero
negative control; keep the current identity only as a renamed algebraic regression test.

---

### RG-4 — The only inhabited relevance spectrum belongs to a model with no agents, no interactions, and no gauge
**(OVERCLAIM by framing, MEDIUM)**

`Theory/07b_agent_network_rg.tex:961`: "This is the promised inhabited relevance spectrum, and it
locates precisely where the growth comes from."

The theorem it refers to is i.i.d. scalar `N(0,1)` under `Z = b^{-1/2}Σ_i X_i` — the classical
Gaussian fixed point of the block-spin/CLT map. It sits inside a chapter titled *Exact Renormalization
of Agent Networks*, immediately after the interaction machinery. **No mode of `DT_ℓ^𝒢` — the actual
agent-network step — is classified anywhere in the manuscript.** The interaction sector's only
spectral statements are the Dobrushin *upper* bound (`prop:rg-dobrushin-cocycle`, sufficient-only,
correctly flagged) and the sup-norm non-expansiveness (`eq:rg-nonlinear-action-sup-contraction`),
both of which forbid relevance rather than exhibit it.

Mitigation already present: `prop:rg-hermite-scope` clause four says the theorem "says nothing about
interaction scores or higher Hoeffding sectors", and the ledger records the extension OPEN. That is
why this is MEDIUM and not HIGH.

*Fix.* Rewrite the sentence to "For the independent scalar Gaussian realization — and for no
interaction sector proved here — all three relevance classes are inhabited", and add one sentence
stating that no relevance classification exists for `T_ℓ^𝒢`.

---

### RG-5 — `thm:rg-fixed-point-equations` "Exhaustive fixed-point equations": definition masquerading as theorem
**(DEFINITION-AS-THEOREM, MEDIUM)**

`Theory/07b_agent_network_rg.tex:2489-2525`. The proof opens: *"The first equation is the definition
of invariance on the common rescaled measure space."* No class is named over which "exhaustive" is
meant, and no enumeration is given. The text later partly retracts (`2703`: "without claiming that
every model class admits a closed-form enumeration"), which is precisely the retraction that makes
the title wrong.

*Fix.* Rename to "Typed fixed-point equations at each tier" and state the content as: *these are
equivalent characterizations of invariance of the measure pair, the action, and the action ray.*
That is what is proved and it is worth having.

---

### RG-6 — `thm:rg-complete-effective-theory`: true by construction, and "Complete"/"exact" are unearned
**(VACUOUS/TRUE-BY-CONSTRUCTION + WEAK RIGOR, MEDIUM-HIGH)**

`Theory/07b_agent_network_rg.tex:2735-2772`. Roughly sixteen hypotheses are supplied, including
"*every induced effective hyperedge*", "*full path laws or their exact memory kernels*", "*globally
gauge-equivariant jointly measurable versions of every disintegration*", and "*rescaling kernels
satisfying \eqref{eq:rg-kernel-semigroup}*". The proof is a list of cross-references plus one
argument: *"Each operation is closed in the stated collection, so their finite composition is closed."*

That sentence is the entire load-bearing content and it is not established. Closure of each operation
in the collection is what would need proving; several listed objects are *supplied by hypothesis*
rather than produced by the operations, which is precisely how the theorem becomes true by
construction. Meanwhile "Complete" is not discharged (nothing is shown exhaustive) and "exact" means
only "the displayed identities hold for the pushed-forward objects" — the manuscript itself proves
the coarse theory leaves any fixed finite family (`sec:rg-hypergraph-closure`, "Exact closure
generates hyperedges").

*Fix.* Rename to "Closure of the declared collection under the declared operations", and give one
short paragraph per operation exhibiting that its output type lies in the collection, marking which
items are supplied rather than derived.

---

### RG-7 — PIFB2: the frame half of the "gauge-covariant barycenter" is provably not gauge-covariant, and the manuscript asserts both
**(ERROR — internal contradiction / hypothesis dropping, MEDIUM)**

`Research/manuscripts/PIFB2.tex:1559`, `prop:barycenter_existence`:
> "...and the map `({q_i},{U_i}) ↦ q_I^*` commutes with the base-local diagonal gauge action
> (Theorem `thm:rg_covariance`)."

Proof (`:1563`) closes with: *"Equivariance is the statement of Theorem `thm:rg_covariance`."*

But `thm:rg_covariance` (`PIFB2.tex:3806-3818`) opens: *"Assume `G` is compact with locally unique
Karcher means..."*. The framework's gauge group is `GL⁺(K_q)`, **noncompact**, as PIFB2 itself
establishes two paragraphs later (`:1571`, via Milnor's bi-invariant-metric lemma).

Then `PIFB2.tex:1575` proves — correctly, I verified it — that **no left-equivariant
permutation-symmetric map `GL⁺(K_q)^n → GL⁺(K_q)` exists for `K_q ≥ 2`, `n ≥ 2`**, and that
"*The additive form `φ_I = Σ w_i φ_i` is not gauge-equivariant at all*", and that the earlier
"`O(‖φ_i‖²)`" accuracy claim "*names the wrong controlling parameter*".

Yet the contradicted statements are still present, uncorrected:
- `PIFB2.tex:1644`: "the reference implementation's additive first-order BCH frame realizes it only
  to `O(‖φ‖²)`" — the very claim `:1575` refutes.
- `PIFB2.tex:1804` (Conclusion): "a meta-agent is the **gauge-covariant** forward-KL barycenter of
  its constituents, carrying the **proved** covariance theorem" — no compactness qualifier.
- The section title itself: "Coarse-Graining I: The Meta-Agent as Gauge-Covariant Barycenter".

Note the belief half *is* equivariant for any invertible pushforward (`KL(h#a‖h#b)=KL(a‖b)`), but
only **conditionally on frame equivariance**, since `Ω_{Ii}=U_I U_i^{-1}` carries `U_I`.

*Partial mitigation the manuscript already supplies, and which I checked holds.* `U_I` is pure gauge:
constituent laws depend on `(U_I,μ_I,Σ_I)` only through `(m,S)`. I extended the check to *sibling*
couplings, which the manuscript does not do: `KL(q_I ‖ Ω_{IJ} q_J)` with `Ω_{IJ}=U_I U_J^{-1}` equals
`KL(N(m_I,S_I) ‖ N(m_J,S_J))` — `U_I` and `U_J` both cancel. So the non-equivariance is a defect of
presentation and of the deployed frame rule, not a hole in the observables. Hence MEDIUM.

*Fix.* Restate `prop:barycenter_existence` with the compactness hypothesis in the statement; delete
or correct `:1644`; qualify `:1804` and the section title; and add the sibling-coupling invariance
computation, which strengthens the pure-gauge argument.

---

### RG-8 — Sign/convention inconsistency in the coarse normalizer (`06_general_coarsegraining.tex`)
**(ERROR, MEDIUM)**

Same chapter, two incompatible conventions for "energy":
- `:317-321`  `\bar P(dz) = e^{-\bar E(z)} \bar ν(dz) / \bar Z`
- `:390-394`  `\bar Z_{\mathcal P}(θ) = ∫ e^{+\mathcal E_θ(ι_{\mathcal P}\bar z)} ν_0^{⊗\mathcal P}(d\bar z) < ∞`

`07b` uses `m = e^{-H}ρ` throughout, so the `e^{+𝓔}` at `:392` is the outlier. Either `𝓔_θ` is a
log-density and should not be called an energy, or the normalizer has a sign error. Additionally
`:350` — "*This is an unnormalized energy until its integral relative to `ν_0^{⊗V}` is finite*" — is
malformed: it is `e^{±𝓔}` whose integral must be finite, not `𝓔`.

The coarse *parameter* map is unaffected — I verified `α_I = Σ_{i∈I}α_i + Υ*Σ_{{i,j}⊆I}β_{ij}`,
`β_{IJ} = Σ_{i∈I,j∈J}β_{ij}`, `c_{\mathcal P} = ⟨Σ_I Σ_{{i,j}⊆I}β_{ij}, u_0⟩` by direct substitution;
it is correct. Only the normalizer display is wrong or undeclared.

*Fix.* One sign, plus rephrase `:350` as "the model is normalized only once `∫e^{-𝓔_θ}dν_0^{⊗V}` is
finite".

---

### RG-9 — "Exact coarse VFE" is exactness of an identity, not of a theory-space map
**(MISSING DERIVATION / naming, MEDIUM)**

`Theory/07b_agent_network_rg.tex:34-66`. The identity
`F_P(Q_o) = F_{P^c}(Q_o^c) + ∫ KL(Q̂_o(dy|z)‖Π̂_o(dy|z)) Q_o^c(dz)`
is **correct and unconditional**: `KL(Q_o‖Π_o) = KL(Q̂_o‖Π̂_o)` because attaching the same kernel `C`
to both arguments leaves the Radon–Nikodym derivative a function of `y` alone, and the chain rule
splits the joint KL. No partition, lumping, strong or weak lumpability hypothesis is needed —
because `P^c := PC` by definition, and nothing is claimed about the coarse theory's *form*.

That is the whole point and it should be said in the theorem: the "exactness" is not the coarse VFE
reproducing the fine one (it does not; they differ by the discarded conditional KL), nor the coarse
theory remaining in the interaction family (it does not; `sec:rg-hypergraph-closure`).

The genuine lumpability content is correctly located elsewhere and correctly proved:
`thm:rg-strong-lumpability` (`:1946-2007`, standard-Borel, with a clean weak-vs-strong separating
witness at `:2009-2020`), `thm:cg-graph-exponential-closure` with its diagonal-affinity hypothesis
`u(z,z)=Υt(z)+u₀`, and `prop:rg-product-equivalence-not-preserved` (diagonal-cloning channel,
correct). None of these is over-generalized.

*Fix.* Append one sentence to `thm:rg-exact-coarse-vfe`: "The identity holds for every normalized
recognition-independent kernel; closure of the coarse theory in any declared parametric family is a
separate hypothesis (`\Cref{thm:cg-graph-exponential-closure,thm:rg-strong-lumpability}`)."

---

### RG-10 — No nontrivial fixed point of the actual map; the only Gaussian candidate is degenerate
**(MISSING DERIVATION, MEDIUM — largely already conceded)**

The only fixed points exhibited (`07b:2704-2714`) are: the identity channel (fixes everything), the
terminal channel + one-point identification (constant IR theory), and strictly `α`-stable baselines
with **constant likelihood** `m_o = Z(o)ρ` — i.e. the free theory. The Gaussian candidate
(`10:146-159`) is the `A=0` ray, whose precision is singular so it is not a Gaussian law at all;
and after the dense normalization `ζ = b²` the coupling-sector map is the **identity on all of
`Sym^K`**, so the "fixed point" is a `K(K+1)/2`-dimensional plane of fixed points with every
transverse direction marginal. `prop:grg-full-cone-blocked` correctly shows Birkhoff cannot rescue it
(invariant faces `𝓕_U` obstruct primitivity; the candidate ray is on `∂𝒦_N`).

All of this is stated. `10:305-308` marks attraction/uniqueness/scheme-independence OPEN;
`conj:grg-fixed-b-attraction` stays CONJECTURE with primitivity, factorization, and fixed hierarchy
named as missing. **The `gaussian_fixed_ray` work is not promoted anywhere in `Theory/`** — I grepped
for it; the chapters and the ledger both keep it CONJECTURE.

*Fix.* State once, plainly, in `sec:rg-fixed-points`, that every fixed point exhibited in this
manuscript is trivial or free, and that no interacting fixed point is known. Currently the reader has
to assemble this from four places.

---

### RG-11 — `thm:rg-unital-essential-spectrum` assumes a standard theorem rather than citing it
**(WEAK RIGOR, LOW-MEDIUM)**

`Theory/07b_agent_network_rg.tex:1062-1064`: "*Assume that whenever `r(U)>r_ess(U)`, the value `r(U)`
is a pole of the resolvent and `U*` has a nonzero positive eigenfunctional `λ`…*". This is the
standard consequence of positivity plus isolated peripheral spectrum on a Banach lattice
(Krein–Rutman / de Pagter circle of results). Assuming it reduces the theorem's own content to a
two-line pairing computation `r(U)λ(1)=λ(U1)=λ(1)` — which I verified is correct, including the
quasi-interior argument for `λ(1)>0`.

*Fix.* Cite the standard statement with its hypotheses (Schaefer, *Banach Lattices and Positive
Operators*, or Meyer-Nieberg) or say explicitly that the hypothesis is *assumed and not derived here*
and name what would discharge it. SPEC §2.2 requires one of the two.

---

### RG-12 — Scale-cocycle experiment sets `Δs = 1`, which is not an admissible block ratio
**(WEAK RIGOR, LOW — code)**

`src/multiagent_elbo/finite/scale_cocycle_experiment.py:301`: `beta_delta_log_scale = F(1)`, and
`:640` serializes `"delta_log_scale": "1"` into provenance. Since `Δs_ℓ = log b_ℓ`
(`eq:rg-cumulative-log-scale`), `Δs=1` means `b=e`, which is not an integer blocking ratio for any
scheme used elsewhere in the manuscript. The division is therefore a no-op and the reported betas are
unnormalized differences.

*Fix.* Record `b` explicitly alongside, and note in the provenance that exact-rational arithmetic
forces a surrogate `Δs`.

---

### RG-13 — Undischarged hand-waves flagged by SPEC §2.2
**(WEAK RIGOR, LOW)**

- `Theory/09_coarsegraining.tex:788`: "*This follows from the weighted variance identity in the
  `C_0^{-1}` inner product.*" governs an `ESTABLISHED` display
  (`eq:cg-fixed-covariance-pairwise-identity`). The identity **is** true — I checked:
  `Σ_i a_i‖m_i−m̄‖² = ½ΣΣ a_i a_j‖m_i−m_j‖²` and `D_SKL = ½‖m_i−m_j‖²_{C_0^{-1}}` for common
  covariance, giving `¼ΣΣ a_i a_j‖m_i−m_j‖²` on both sides — but SPEC §2.2 bans exactly this phrasing.
  Two lines would discharge it.
- `Theory/06_general_coarsegraining.tex:444-446`: the qualifier "*for orthogonal projection `PC`*"
  in `prop:cg-message-passing-residual` is vacuous — `PC = P R_c^{-1}PᵀR` is *always* the
  `R`-orthogonal projector onto `range P` by `eq:cg-galerkin-data`. (The equivalence itself is
  correct; I verified both directions via `ker C = (range P)^{⊥_R}`.)

---

### RG-14 — "Functoriality" on the thin scale category is a restated hypothesis
**(OVERCLAIM, LOW)**

`Theory/07_general_renormalization.tex:305-318`: "*Identity arrows have identity components, so these
laws make the family a functor on the thin category of the finite scale set.*" On a thin category any
family of composable arrows satisfying the composition laws is a functor; the content is exactly the
laws `c_{ℓ+1}∘c_ℓ`, `κ_{ℓ+1}∘κ_ℓ`, `𝒫_{ℓ+1}∘𝒫_ℓ`, `q_{ℓ+1,s}∘q_{ℓ,s}`, which are **imposed** two
sentences earlier ("*For a genuine multi-step scale functor, the maps … also obey their respective
composition laws*"). Honestly signposted, so LOW — but "functor" should not be read anywhere as a
proved diagram. **No commuting diagram for coarse-graining is drawn or checked anywhere in the
manuscript.**

---

### RG-15 — PIFB2 apex closure: a prior constituted by the population's posteriors, untyped
**(MISSING DERIVATION, MEDIUM)**

`Research/manuscripts/PIFB2.tex` §Coarse-Graining IV sets
`p_i^{(top)}(x) = Σ_j w_j(x) Ω_{i,j}[q_j](x)` with `w_j ∝ exp(−K̄L_j)`. Both the *arguments* and the
*weights* are current beliefs, including agent `i`'s own. This is exactly the architecture the Theory
rewrite forbids under its typing prohibition (SPEC §5: "A generative kernel … may not take a
recognition law, a recognition parameter, or **a posterior** as an input") and the architecture
`11_obstructions.tex` replaces by a declared top prior or an apex latent. PIFB2 flags only that the
dropped dispersion term "is uncontrolled when the collective is globally incoherent" and that
validation is prospective; it does not type the apex closure at all.

Separately, `eq:ouroboros_F` `Σ_{k≥1} λ₀ρ^k KL(s_i ‖ Ω̃[s_{I_k}])` has **no augmented-joint backing
for `k ≥ 2`**. `app:augmented_joint` (`lem:shadow_mf_optimum`) derives only the depth-1 shadow. The
cited precedents (West–Harrison discounting, Genest–Zidek log-linear pooling) are analogies, and the
manuscript presents them as such — but the fragment is nevertheless added to a free energy that is
elsewhere claimed to be an evidence bound.

*Fix.* Type the apex closure explicitly: either declare it a *recognition-side* coordinate update
(legitimate, as `11_obstructions.tex:252-254` argues for the star) or declare it a fitted prior that
breaks the ELBO reading, and say which. Give `k≥2` an augmented joint or mark it a declared
regularizer with no evidence-bound status.

---

## 3. What I checked and found SOLID

Substantial, and worth recording explicitly since the failure mode of an adversarial audit is to bury
it.

1. **`06_general_coarsegraining.tex` is essentially clean.** `thm:cg-kl-dpi-extended` (correct
   extended-real DPI with the `φ₀(t)=t log t − t + 1` generator, no signed integral rearranged),
   `thm:cg-dpi-equality` with its exact equality condition, `cor:cg-pairwise-bayes-recovery`,
   `cor:cg-dpi-infinite-equality-warning` (a genuinely sharp 3-point counterexample — I verified the
   contradiction `(PK)R` assigns ≥1/4 to `c`), `thm:cg-fisher-contraction` (Pollard DQM route,
   correct, with the `A`/`B` Bernoulli witness separating Fisher equality from experiment recovery),
   `prop:cg-markov-category`, `prop:cg-equivariant-channels`, `prop:cg-message-passing-residual`,
   `thm:cg-holonomy-kl-marginal`, `cor:cg-holonomy-cross-morphism`, `thm:cg-projective-cylinder-law`.
   All checked; all correct.
2. **The Hermite theorem and its scope proposition** — exactly verified, correctly scoped, and the
   normalization dependence explicitly disclosed. The `He₃` witness for two-sided normalizer
   divergence is correct, and the explicit warning that `−x²` is *not* such a witness
   (`π(e^{tx²})=(1−2t)^{-1/2}` finite on `(−½,½)`) is the kind of care that is usually absent.
3. **`prop:rg-noncommuting-limits`** — a real, correctly proved obstruction. Path Laplacian
   eigenvalues, the exact Galerkin quotient `S_{m,b}ᵀL_m S_{m,b}=L_{m/b}`, the arccos IDS limit, and
   the `Path₁` maximal-depth collapse all check out. The orthonormalized-vs-unnormalized `b^{-ℓ}`
   bookkeeping is stated.
4. **`eq:rg-heat-susceptibility`** — the Abelian/Karamata computation gives exactly `α`; the converse
   Tauberian direction is explicitly *not* asserted; the warning about dividing entropy by
   `log|V_n|` destroying the plateau is correct and rarely stated.
5. **`prop:rg-dobrushin-cocycle`** — both controls are correct: the `R₁R₀` two-step witness (rows
   both `(1/2,1/2)`, composed coefficient 0, so one-step contraction is not necessary) and the
   `R_k=(1−a_k)I+a_kJ`, `a_k=2^{-k-2}` witness (`∏δ_k>0`, so one-step contraction is not sufficient).
   Compatibility of both with the declared level laws checks out.
6. **`prop:rg-superexponential-distortion`** and `thm:rg-tempered-comparison` — correct, and the
   `J_k u = e^{k²}u` witness genuinely separates mode-normalization tempering from trivialization
   tempering.
7. **`thm:rg-projection-memory` / `cor:rg-resolved-autonomy`** (Nakajima–Zwanzig at the discrete
   linear tier) — the recurrence is correct and the "sufficient but not necessary" witness
   (`T(x,y)=(x,x)`, `QTP≠0` but `CTQ=0`) is correct. Historical attribution is scoped properly.
8. **`prop:rg-fixed-object-nonimplication`** — six clean non-implication witnesses across tiers, all
   correct. This is exactly the kind of negative result the field usually omits.
9. **`thm:rg-hoeffding-action-isomorphism`** — bound and sharpness both exactly verified. The
   `3^{|V|}−1` exponential dependence is honestly flagged as *not* dimension-free, and
   `cor:rg-interaction-tempered` correctly turns it into a hypothesis of the mode theory.
10. **The whole barycenter section in `09_coarsegraining.tex`** — `prop:cg-gaussian-forward-kl-barycenter`
    and `cor:cg-compact-holonomy-barycenter` are correct, with existence and uniqueness properly
    established via strict convexity of the log-partition / the trace-log inequality. The `2I_K`
    non-compactness witness is correct. The two examples separating structural holonomy rank from
    transported marginal KL (`trivial holonomy, KL = 2a²` vs `H=diag(1,−1,−1)`, `f_I=1`, all KLs zero)
    are correct and genuinely illuminating.
11. **`11_obstructions.tex`** — every negative result is *proved*, with counterexamples I verified
    numerically. `prop:obs-reciprocal-pair-kernel`, `cor:obs-flat-fold-singular`,
    `prop:obs-holonomy-determinant-factorization` (`det J = det(I−H)²/(det Rₑ det R_f)` — exact),
    `prop:obs-normalizer-link-dependence` (including the correct observation that `a=1` is a strict
    *maximum* of the isolated log-normalizer term, not a minimum),
    `thm:obs-star-fixed-point-contraction` (`ρ = λ_max(P_b^{-1/2}BP_b^{-1/2}) < 1`, with `P₀≻0`
    correctly identified as essential and the `P₀⪰0` failure mode named). The scoping discipline —
    "*Never generalize the scoped no-go to all cycles or all reciprocal models*" — is maintained
    throughout.
12. **The claim ledger is accurate.** I spot-checked eight entries against their chapters; every one
    correctly describes what is open and what would close it. The infinite-volume entry in particular
    enumerates the right obligations (projective cylinder laws, DLR, tightness, free-energy-density
    convergence, connection/cross-morphism limits).
13. **No AUD-20-style fallacy, no universality-from-one-exponent, no thermodynamic-limit smuggling,
    no monotonicity direction error** anywhere in the six chapters audited.

---

## 4. Recommended remediation order

1. **RG-2, RG-3** (code, cheap, high value): make the two tautological cross-checks into real tests;
   remediate the still-open AUD-17.
2. **RG-1** (structural): exhibit one verified `(C_b, I_b, ζ_b)` semigroup instance, or retag and
   rename. This is the single change that most affects whether the document can honestly say "RG".
3. **RG-6, RG-5, RG-4** (naming and framing): rename `Complete`/`Exhaustive`, scope the "inhabited
   spectrum" sentence.
4. **RG-8** (one sign), **RG-9** (one sentence), **RG-13** (two lines) — trivial edits.
5. **RG-7, RG-15** (PIFB2): remove the internal contradiction about frame equivariance; type the
   apex closure. If PIFB2 is being superseded by `Theory/`, note instead that `Theory/` already
   *refutes* the PIFB2 apex architecture and declines the PIFB2 meta-agent barycenter definition —
   that divergence should be recorded somewhere, because a reader holding both documents will
   otherwise assume the barycenter definition survived.
6. **RG-11, RG-12, RG-14** — citation hygiene and provenance.
