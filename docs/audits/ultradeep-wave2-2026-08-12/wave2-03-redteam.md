# Wave 2 / Red team — adversarial attempt to break the theory

Date: 2026-08-11. Baseline: `MultiAgentELBO` working tree (`Theory/` 16,821 lines TeX; `src/` as shipped),
`Research/manuscripts/PIFB2.tex`.
Execution policy: **CPU only. No GPU or CUDA job was started.** All numerics in an isolated Linux
sandbox with float64 / `Fraction` / `mpmath` (80 dps) / `sympy`.

Mandate: break the theory. Credit only for counterexamples that satisfy **every** stated hypothesis.

---

## Verdict up front

**No confirmed break.** Across roughly 30 attacks on 8 target classes I could not construct a single
object that satisfies all the hypotheses of a stated `Theory/` result and violates its conclusion.
Two apparent breaks dissolved on careful re-derivation and are recorded below as self-refutations.
What I did find are **four calibration / diagnostic defects in the code's declared numerical domain**
(quantified, reproducible), **three load-bearing-hypothesis witnesses** that show which hypotheses are
doing real work, and **one correction to a Wave-1 finding (RG-7), which is overstated.**

---

## 1. Confirmed breaks of stated theorems

**None.**

The closest thing to a break is a *gate* defect, not a *theorem* defect, reported as F-1 below. Every
theorem I attacked survived; the list of surviving attacks is in §5 and is itself the main evidence.

---

## 2. Findings: gates, diagnostics, calibration (real defects, no theorem falsified)

### F-1 — HIGH — The declared numerical domain is not calibrated to the tolerance the results are graded at

**What is claimed.** `prop:ig-generalized-spectrum-invariance` (`Theory/08_infogeometry.tex:438`) says
that for `Λ ≻ 0`, `L = Lᵀ`, and any invertible `T`, the pencil `(L, Λ)` and the reframed pencil
`(T⁻ᵀLT⁻¹, T⁻ᵀΛT⁻¹)` have the *same* generalized eigenvalues. The proof is a two-line similarity
argument and is correct; I re-derived it and could not break it.

The implementation is `apply_frame_change` (`src/multiagent_elbo/realizations/gaussian/gauge.py:151`).
Its **declared** numerical domain is `max_frame_condition = 1.0e6` (`config.py:145`) for the frames
and `min_spd_rcond = 1.0e-12` (`config.py:144`) for the precision. The residual
`GAU-01_generalized_spectrum_residual` is graded at `tolerance = numerics.atol + numerics.rtol`
(`realizations/gaussian/experiment.py:90`, `:225`), i.e. `1.010e-10` at the shipped settings.

**Witness 1 — frames inside the frame gate.** Random `GL⁺(2)` frames with condition number exactly
`1.0e5` (gate limit `1.0e6`), acting on the *same* interaction structure as the frozen fixture
(`A₁=diag(2,3)`, `A₂=diag(4,5)`, `W=[[1,0.2],[0.2,2]]`):

```
GATES: frame cond max = 1.0000e+05   (limit 1.0e+06)          -> PASS
       precision rcond = 3.1150e-01  (min_spd_rcond 1.0e-12)  -> PASS
GRADED tolerance atol+rtol = 1.010e-10
GAU-01_generalized_spectrum_residual (original frame) = 1.2106e-16   pass
GAU-01_generalized_spectrum_residual (reframed)       = 8.5140e-08   FAIL   (843x tolerance)
GAU-01_eigenpair_residual                             = 1.8617e-16
GAU-01_metric_orthogonality_residual                  = 2.5267e-07
spec(orig)       = [-1.21e-16, -3.42e-17, 0.413722651, 0.526288458]
spec(reframed)   = [-2.80e-10,  8.51e-08, 0.413722723, 0.526288460]
spec(exact 80dps)= [ 5.23e-82,  1.59e-81, 0.413722651, 0.526288458]
```

**Witness 2 — precision inside the SPD gate, with *orthogonal* frames (cond = 1).**
`A_i = diag(1, 1e-11)`, `W = 0.5·diag(1e-11, 1e-11)`, frames = a single 2×2 rotation by 0.7 rad:

```
GATES: frame cond max = 1.0000e+00                            -> PASS
       precision rcond = 1.0000e-11  (min_spd_rcond 1.0e-12)  -> PASS with 10x margin
GAU-01_generalized_spectrum_residual (reframed) = 3.3835e-06   FAIL  (33,500x tolerance)
spec(reframed)   = [..., 1.00000390e-11, 5.00003384e-01]
spec(exact 80dps)= [..., 1.00000000e-11, 5.00000000e-01]
```

An *orthogonal* reframing — the most benign possible change of local trivialization — moves the
claimed gauge-invariant generalized spectrum in the fifth significant digit, inside the declared SPD
domain.

**Calibration scan (all gates passing; `tol = 1.010e-10`):**

| frames cond | spec forward err | eigenpair resid | metric-orth resid |
|---|---|---|---|
| 1e3 | 1.116e-11 | 2.69e-17 | 2.96e-11 |
| 3e3 | 3.098e-11 | 4.42e-17 | 1.28e-10 |
| **1e4** | **4.062e-10** | 2.91e-17 | 1.16e-09 |
| 1e5 | 8.514e-08 | 5.41e-17 | 2.53e-07 |
| 3e5 | 1.850e-06 | 3.25e-17 | 2.59e-06 |

| precision rcond (orthogonal frames) | spec forward err | eigenpair resid | metric-orth resid |
|---|---|---|---|
| 1e-6 | 6.083e-12 | 4.76e-11 | 3.45e-11 |
| **1e-8** | **1.035e-09** | 2.24e-09 | 5.52e-09 |
| 1e-11 | 3.384e-06 | 2.78e-06 | 7.94e-06 |

**Conclusion.** For the shipped `atol/rtol`, the safe frame-condition ceiling is ≈ `3e3` — **300×
below the declared `max_frame_condition = 1e6`** — and the safe `min_spd_rcond` is ≈ `1e-7` — **five
orders of magnitude above the declared `1e-12`**. The two gates and the grading tolerance were chosen
independently and are not mutually consistent. `Theory/08_infogeometry.tex:520` correctly says the
check "establishes numerical usability only for that protocol"; the defect is that the *declared
domain* of the shipped function is far wider than the protocol it was validated on
(frozen frames `diag(2,1)`, `diag(1,3)`, cond 2 and 3).

### F-2 — MED-HIGH — `GAU-01_eigenpair_residual` is a backward error and cannot certify the spectrum

`_generalized_diagnostics` (`gauge.py:69-88`) normalises the eigenpair residual by
`(‖L‖ + |d|·‖Λ‖)·‖v‖`. Because the eigenvectors are Λ-orthonormal, ill-conditioned Λ inflates `‖v‖`
and deflates the reported residual. Directly demonstrated:

```
frames cond 3e5:  eigenpair residual = 3.249e-17   (looks perfect)
                  actual spectrum forward error = 1.850e-06   (18,000x tolerance)
```

The metric `GAU-01_eigenpair_residual` is published in `experiment.py:238` with the interpretation
"Normalized generalized-eigenpair residual in both frames". It is a valid *backward* error and carries
**no information about the forward error** of the quantity the chapter calls a gauge invariant. It
should not be presented alongside `GAU-01_generalized_spectrum_residual` as corroboration.

**Robustness offset (record this too):** in *every* failing case above,
`GAU-01_metric_orthogonality_residual` also exceeded tolerance, and it did so conservatively (at
frames cond 3e3 it fires at 1.28e-10 while the spectrum error is still only 3.1e-11). So I could
**not** produce a silently wrong published number: no input passes the gates *and* all three graded
diagnostics *and* returns a wrong spectrum. The orthogonality residual is doing real work.

### F-3 — LOW-MED — The interaction-family membership test is a 1e-10 neighbourhood of the family, not the family

`prop:cg-kron-leaves-family` (`09_coarsegraining.tex:97`) turns on exact asymmetry: the manufactured
Kron block `W₁₃Λ₃₃⁻¹W₂₃ = (1/19)[[9,3],[4,14]]` is not symmetric, hence not an admissible weight.
I re-derived the whole witness through the shipped code:

```
Lambda_33 = [[4,1],[1,5]]  det = 19
19 * W13 L33^-1 W23 = [[9,3],[4,14]]     matches the manuscript exactly
symmetric? False
leading minors of Lambda: [2, 6, 18, 48, 102, 233]   matches the manuscript exactly
```

But `GaussianInteraction.from_self_and_edges` admits any edge weight whose relative Frobenius
asymmetry is `≤ atol + rtol = 1.01e-10` and then **silently symmetrises it**:

```
edge weight [[1,0],[1e-11,1]]  -> ACCEPTED, returned block differs from input by 5e-12
edge weight [[1,0],[1e-8, 1]]  -> rejected ("not symmetric within tolerance")
```

Consequence is benign for the *energy* (only the symmetric part enters the quadratic form) but the
membership predicate implemented is not the predicate the proposition is about. Worth one sentence in
the code docstring; not a theorem defect.

### F-4 — LOW — `retain_interaction_order` cannot compute the quantity `thm:rg-hoeffding-action-isomorphism` bounds

The theorem's `‖H_ℓ‖ ≤ 3^{|V|} − 1` is a bound on `Σ_{A≠∅} ‖P_A f‖_∞`. `retain_interaction_order`
rejects `maximum_order = 0` (`interactions.py:151`), so the shipped projector cannot return the sum
over *all* nonempty subsets. I had to reimplement it to check the theorem (see §5, where it verified
exactly).

---

## 3. Load-bearing-hypothesis findings ("this would break if H were dropped")

### L-1 — `cor:cg-compact-holonomy-barycenter`: compactness is load-bearing, and the proof under-signals *why*

Statement (`09_coarsegraining.tex:700`): `H ⊂ GL(K)` a represented holonomy group with **compact
closure**; then `N(a_H, C_H)` is the unique minimiser of the forward-KL objective over `H`-invariant
nondegenerate Gaussians, with score `½[log det C_H − Σ a_i log det C_i]`.

The proof justifies compactness once, explicitly, via "*Every element of the compact matrix group
`closure(H)` has `|det h| = 1`*" — which is the step that makes the `log det C_i` terms survive.

**Witness that this justification is not the load-bearing one.** Take `K = 2` and
`H = { diag(2^k, 2^{-k}) : k ∈ ℤ }`. Then:

- `H` is a subgroup of `GL⁺(2)`; ✓
- `H` is **closed** in `GL(2)` (it is discrete with no accumulation point in `GL(2)`); ✓
- every `h ∈ H` has `det h = 1`, so the proof's stated compactness consequence **holds**; ✓
- `H` is **not compact**. ✗

Under this `H` the corollary's conclusion fails completely, not marginally: `hCh^ᵀ = C` for all
`k ∈ ℤ` forces `C` diagonal and `4^k C₁₁ = C₁₁`, hence `C₁₁ = 0`, so **the `H`-invariant nondegenerate
Gaussian family is empty**, the constrained minimiser does not exist, and `eq:cg-gaussian-haar-score`
has no referent. The orbit "average" diverges:

```
symmetric Cesaro average of h^k I h^kT over k = -m..m:
  m=1  diag = [1.75, 1.75]
  m=3  diag = [12.19, 12.19]
  m=6  diag = [420.10, 420.10]
  m=10 diag = [66576.25, 66576.25]
```

**This is not a break** — the corollary assumes compact closure and my witness violates it. It is the
requested explicit `GL⁺(2)` divergence: a sequence along which the claimed invariant blows up as soon
as compactness is dropped. The actionable point is that the *proof text* names only the `|det h| = 1`
consequence of compactness, which my counterexample satisfies; the two genuinely load-bearing
consequences (existence of a normalised Haar probability measure, and nonemptiness of the invariant
family) are used silently. One added sentence would fix this.

`appendix_notation.tex:225-227` already flags "A finitely generated `H` need not be closed. Haar
averaging in the compact-closure theorem is over `closure(H)`, after explicitly assuming that this
closure is compact." That discipline is correct and should be preserved.

### L-2 — The sandwich transport is load-bearing; the additive form breaks the cocycle at first order

Attack on target 4 (`Ω_ij = exp(φ_i)exp(−φ_j)` vs `exp(φ_i − φ_j)`), non-abelian `gl(2)`, with
`φ_i = s·[[0,1],[0,0]]`, `φ_j = s·[[0,0],[1,0]]`:

```
s=0.05  ||Om - exp(phi_i - phi_j)||_F / ||Om||_F = 1.2502e-03
s=0.20                                            2.0036e-02
s=0.50                                            1.2477e-01
s=1.00                                            4.2954e-01
```

Cocycle check with three genuinely non-commuting frames
`φ = {0.3X, 0.4Y, 0.2(X−Y)+0.1·diag(1,−1)}`:

```
sandwich form: ||Om01 Om12 - Om02||_F   = 6.21e-17
               ||Om01 Om12 Om20 - I||_F = 2.32e-16
additive form: ||A01 A12 - A02||_F      = 8.51e-02      <-- cocycle FAILS
               ||A01 A12 A20 - I||_F    = 8.76e-02      <-- holonomy FAILS
```

So `Ω_ij Ω_jk = Ω_ik` is exact for the sandwich form for arbitrary non-commuting `φ` (it is a
coboundary, no commutativity needed), and the additive surrogate violates it at O(‖[φ_i,φ_j]‖).
**I found no place in `Theory/` or in `src/` where the two forms are conflated** — `grep` for
`expm|logm` over all of `src/` returns exactly one hit, `np.expm1` in `categorical_dqm.py:294`, i.e.
there is no matrix exponential in the codebase at all, so the slide cannot occur there. PIFB2 states
the distinction correctly and explicitly at `:343`.

Where the additive form *is* used is PIFB2's **implementation** frame barycenter `φ_I = Σ w_i φ_i`
(`PIFB2.tex:1573`, `:1644`), declared as "first-order BCH, accurate to `O(‖φ_i‖²)`". Quantified:

```
w = (1/2, 1/2), phi_a = 0.6 X, phi_b = 0.6 Y  (||phi||_F = 0.60)
|| exp(sum w phi) - A exp(1/2 log(A^-1 B)) ||_F / ||.|| = 9.49e-03
```

i.e. ~1% at ‖φ‖ ≈ 0.6. The manuscript's `O(‖φ‖²)` claim is honest and the constant is small; the
number is offered so it can be stated rather than asserted.

### L-3 — `thm:obs-star-fixed-point-contraction`: `P₀ ≻ 0` is exactly load-bearing, as the text says

`11_obstructions.tex:330` says "The strict anchor `P₀ ≻ 0` is essential. If it is weakened to
`P₀ ⪰ 0`, the symmetric matrix `S` can have eigenvalue one, and neither uniqueness nor geometric
contraction follows." Confirmed numerically: with `Θ = {[[1,2],[0,1]], rot(π/2)}`, `R = {I, diag(3,½)}`:

```
P0 = I                   rho = 0.866347218667577   worst observed ratio = 0.866347218667258   OK
P0 = diag(1e-9, 1)       rho = 0.999999999666667   worst = 0.999999999666667                  OK (tight)
P0 = diag(1e-14, 1)      rho = 0.999999999999996   worst = 0.999999999999997                  OK (tight)
P0 = [[2,1.9],[1.9,2]]   rho = 0.956215145792495   worst = 0.956215145792495                  OK (tight)
```

The bound is attained, not merely satisfied, and degrades continuously to `ρ → 1` exactly as `P₀`
approaches the boundary. `n = 0` (empty constituent set) gives `B = 0`, `ρ = 0`, one-step convergence,
as the text says.

---

## 4. Self-refutations (apparent breaks that dissolved) — report these, they matter

### SR-1 — Wave 1 finding **RG-7 is overstated**

RG-7 asserts an internal contradiction: `prop:barycenter_existence` (`PIFB2.tex:1559`) asserts
gauge-equivariance citing a theorem that assumes `G` compact, while the actual group `GL⁺(K_q)` is
noncompact.

I set out to build the divergence and instead proved the opposite for the object in question. **The
forward-KL Gaussian barycenter is exactly equivariant under all of `GL⁺(K)`; no compactness, and not
even `|det g| = 1`, is needed.** The reason is elementary: KL is invariant under a common invertible
pushforward, so `Σ w_i KL(g_#q̃_i ‖ q)` at `q = g_#q'` equals `Σ w_i KL(q̃_i ‖ q')`, and argmin
commutes with `g_#`. Equivalently, moment matching is equivariant term by term:
`μ̄ ↦ gμ̄`, `C̄ ↦ gC̄gᵀ`. Numerically, along an unbounded family in `GL⁺(2)`
(`g_t = diag(e^t, e^{-t})·[[1,t],[0,1]]`, `‖g‖₂` up to `2.7e45`):

```
||g||_2=3.85e+00  mean equivariance err=0.00e+00  cov rel err=1.16e-16  score gap=0.00e+00
||g||_2=7.57e+02  mean equivariance err=5.68e-14  cov rel err=1.53e-16  score gap=1.44e-15
||g||_2=9.72e+09  mean equivariance err=9.54e-07  cov rel err=2.36e-16  score gap=3.83e-14
||g||_2=2.69e+45  mean equivariance err=3.17e+29  cov rel err=1.63e-16  score gap=5.23e-13
```

(the growing absolute mean error at `‖g‖ ~ 1e45` is float64 rounding relative to entries of size
`1e45`; the *relative* error is at machine epsilon throughout, and the minimised score is exactly
invariant.)

Where compactness genuinely bites is the **frame** Karcher mean `eq:meta_agent_frame_barycenter`, and
`PIFB2.tex:1573` already concedes that in full ("`GL⁺(K_q)` is noncompact and admits no bi-invariant
Riemannian metric [Milnor 1976, Lemma 7.5]"), and `:1577` explicitly separates the two:
"*the frame mean uses a bi-invariant group distance in the compact case, while the M-projection belief
barycenter uses forward KL ..., whose invariance is common-pushforward invariance rather than group
bi-invariance*."

**Corrected form of RG-7:** the defect is a *citation-scope* slip at `PIFB2.tex:1559` and `:1644` —
those sentences cite `thm:rg_covariance` (compact hypotheses) for a belief-barycenter equivariance
that holds unconditionally and has a two-line proof. It is not a contradiction and not a mathematical
error. The fix is to prove the belief-barycenter equivariance directly, in two lines, and reserve the
compactness citation for the frame sector. Severity should drop from MED/ERR to LOW/citation-scope.

### SR-2 — Apparent violation of the star contraction rate

My first run reported `ρ = 0.866347` with a worst observed contraction ratio `0.866659 > ρ`, i.e. an
apparent violation of `eq:obs-star-rate`. It is an artefact: the ratios were taken over 200 sweeps and
the later ones divide two quantities that are both at the float64 noise floor (`~1e-16`). Restricting
to iterates above the noise floor gives `worst = 0.866347218667258 ≤ ρ = 0.866347218667577`.
**No violation.** Recorded because it is exactly the kind of false positive a red team should discard.

---

## 5. Attacks that FAILED (this is the robustness evidence — please keep it)

Each line: what was attacked, how, and the numeric outcome.

**Chapter 11 (obstructions).**
- `prop:obs-reciprocal-pair-kernel` with a **defective** holonomy `H = [[1,1],[0,1]]` (eigenvalue 1,
  algebraic multiplicity 2, geometric multiplicity 1) — the case most likely to break a
  "kernel = fixed space" claim. `dim ker J = 1 = dim ker(H−I)` for every `R_e, R_f` tested. Holds.
- `eq:obs-holonomy-det` `det J = det(I−H)²/(det R_e det R_f)` over defective `H`, rotation `H`,
  non-normal flat `Θ_e`, and non-commuting `Θ_e, Θ_f`: relative error `≤ 3.0e-15` in every
  well-conditioned case. (It fails numerically at `det R ~ 1e±16`, which is float64 cancellation,
  not a defect in the identity.)
- `prop:obs-normalizer-link-dependence` re-derived symbolically in sympy:
  `det(J + p₀I) − [p₀² + p₀(a+1/a)²] = 0` exactly; `A'(1) = 0`; `A''(1) + 4/(p₀+4) = 0` exactly.
- `cor:obs-flat-fold-singular`, `cor:obs-holonomy-kernel-shrinkage`, `prop:obs-star-definite`,
  `prop:obs-star-meanfield-coordinate`, `prop:obs-anchor-coercivity`,
  `prop:obs-holonomy-determinant-factorization`, `prop:obs-declared-root-unavoidable`: all re-derived
  by hand; all correct, all correctly scoped. Chapter 11's stated "boundary of the no-go" paragraph
  is genuinely a boundary, not a hedge.
- Only degenerate scope slip found: `prop:obs-declared-root-unavoidable` is vacuously satisfiable by
  a model with **zero** latents ("every prior is constituted by other latents" is vacuously true).
  Harmless; noted for completeness.

**Chapter 9 (Gaussian coarse-graining).**
- `prop:cg-kron-leaves-family` re-derived through the shipped code; matches the manuscript
  digit-for-digit including the leading minors `2, 6, 18, 48, 102, 233`.
- `thm:cg-congruence-diagonal-kron`: attacked the M-matrix step (does the per-channel Schur
  complement stay a loopy Laplacian?). It does: `(Λ_D)_EE` per channel is a nonsingular symmetric
  M-matrix, its inverse is entrywise nonnegative, so Schur off-diagonals stay `≤ 0` and row sums stay
  `≥ 0`. The non-commuting witness `X = H diag(1,2)Hᵀ`, `Y = H diag(3,1)Hᵀ`, `H = [[1,1],[0,1]]`
  reproduces `XY − YX = [[0,−5],[5,0]]` exactly.
- `thm:cg-qualified-maximality`: attacked the relative-interior step and the "commuting symmetric
  matrices are simultaneously orthogonally diagonalisable" step. Both correct; the eliminated
  diagonal really does collapse to `M` by the construction `A_e = M − ε(X+Y)`.
- `prop:cg-gaussian-forward-kl-barycenter` and `cor:cg-compact-holonomy-barycenter`: re-derived; the
  score `½[log det C̄ − Σ a_i log det C_i]` and the Haar-projected version both check out. See L-1
  for the load-bearing hypothesis.

**Chapter 7 (restrictions) — 350,236 comparable pairs, randomized search.**
- `thm:restrict-determinant-gap`: closed-form block-minimised KL vs the determinant gap over 300
  random `J ≻ 0` and **all** set partitions: `max |difference| = 1.78e-15`.
- Nonnegativity of the gap: **0 violations**.
- The *exact equality condition* (gap `= 0` iff `J_bc = 0` for all distinct blocks): **0 violations**.
- `prop:restrict-refinement-monotonicity` over every comparable pair in the refinement lattice for
  `n = 2..5`: **0 violations** in 350,236 tested pairs.
- `prop:restrict-nonnested-unordered` numbers verified: gaps `0.0589` and `0.5493` at `(a,b)=(0.8,0.2)`.

**Chapter 7b (agent-network RG).**
- `thm:rg-hoeffding-action-isomorphism` sharpness `Σ_{A≠∅}‖P_A f‖_∞ = (4p−1)ⁿ − (2p−1)ⁿ`, computed
  with the *shipped* `hoeffding_decompose`: exact to `≤ 3.6e-15` for `n = 2,3` and
  `p ∈ {0.5, 0.7, 0.9, 0.99}`, and always `< 3ⁿ − 1`. The norm bound
  `Σ_A 2^{|A|} = 3ⁿ` argument is correct.
- `thm:rg-strong-lumpability` (both directions) and the weak-lumpability counterexample on
  `Y = {1,2,3}` re-derived by hand: correct, including the measurable-selection caveat.
- `thm:rg-projection-memory` and `cor:rg-resolved-autonomy` re-derived, including the
  `T(x,y) = (x,x)` witness showing `QTP ≠ 0` with all memory kernels vanishing: correct.
- `prop:rg-product-equivalence-not-preserved` (the diagonal-cloning channel that leaves the
  product-reference tier — target 5's "normalized Markov arrow that leaves the admitted tier"):
  the manuscript **already constructs it**, proves it, and refuses to admit a target Hoeffding
  decomposition there. This is the attack I was asked to run; the theory anticipates it.
- `V_ℓ = ∅` (empty agent set) is explicitly handled at `07b:1155-1159`.

**Chapter 6 (general coarse-graining) / KL asymmetry and infinities (target 3).**
- `thm:cg-kl-dpi-extended` is stated in `[0,+∞]` with *no* absolute-continuity or finiteness
  hypothesis; `thm:cg-dpi-equality` adds finiteness only for the equality characterisation; and
  `cor:cg-dpi-infinite-equality-warning` supplies the counterexample showing the finiteness
  hypothesis cannot be dropped. I could not improve on this — the chapter has already run the attack.
- Forward vs reverse KL: `prop:cg-gaussian-forward-kl-barycenter` (forward, moment matching),
  `thm:cg-holonomy-kl-marginal` (forward in the parent), `prop:restrict-gaussian-reverse-kl` (reverse)
  are consistently and separately typed. `PIFB2.tex:1545` even calls out the direction flip between
  `eq:beta_optimal` and `eq:meta_agent_barycenter` explicitly. No slide found.
- `eq:obs-correlated-complexity-ledger` `KL(Q‖⊗ρ_i) = TC(Q) + Σ KL(Q_i‖ρ_i)` in `[0,+∞]`: all three
  terms nonnegative, so no `∞ − ∞` can arise. Correct.

**Code, degenerate and boundary inputs (target 1).**
- Chain rule `vfe_channel_decomposition` with zero-probability atoms in *both* `q` and the evidence
  submeasure, plus an unreachable coarse state: residual `4.16e-17`.
- Fine KL `= +∞` while coarse KL is finite (`0.693`): returns
  `fine_vfe=inf, coarse_vfe=0.693…, conditional_kl=inf, residual=None, offending_state='x1'` —
  correct on all four fields, including refusing to compute a residual.
- `K = 1` (one-state probability space): `KL = 0`, `F = 0.3567`, chain-rule residual `0.0`. No crash.
- `fisher_channel_decomposition` with a **subnormal** atom (`p_c = 5e-324`) isolated by the channel and
  a score of magnitude `1e8` on that atom: residual **exactly 0.0** at every tested magnitude
  (`1e-15, 1e-100, 1e-300, 5e-324`). The `where=coarse_probability>0` guards hold.
- `block_update_decomposition` with an infinite collective KL: raises rather than returning garbage.
  With outside marginals differing by `1e-17`: accepted, residual `−5.6e-17`.
- Hoeffding decomposition against a reference with a **zero-mass atom**: reconstruction residual
  exactly `0.0` (the top component is defined as the remainder, so exactness is structural).
- `GaussianInteraction`: single agent / `K=1` / empty edge set → OK; **self-loop** → rejected;
  **multi-edge / duplicate reversed edge** → rejected; **disconnected component with zero self term**
  → rejected as not positive definite; negative edge weight → rejected. Partition with an empty
  block, or a repeated vertex → rejected. Schur retaining none → rejected. No crash, no garbage.
- `FinitePermutation`'s `np.argmax` (the only `argmax` in `src/`) is guarded by an exact
  zero-one / unit-row-and-column-sum validation, so ties cannot occur.

**Counterexample hypothesis audit (target 6).**
- `parameter_dependent_channel_fixture`: I verified the exact gap is `1/(1−θ²)`
  (`θ=0 → 1`, `θ=1/2 → 4/3`, `θ=−3/4 → 16/7`, `θ=9/10 → 100/19`, all exact `Fraction` matches). The
  fixture has **zero** fine Fisher information and **positive** pushed Fisher information — which
  would refute `thm:cg-fisher-contraction` if the channel were parameter-independent. It is not, and
  the record is correctly tagged `inside_declared_domain=False`, `assumptions_satisfied=False`,
  `classification='assumption_boundary'`. This is a correctly-typed negative control, not a
  hypothesis-missing counterexample. `CandidateRecord.__post_init__` **enforces** that tagging
  (`counterexamples.py:203-206`), which is exactly the right guard.

**Target 8 (quantifier / scope slips).** The chapters I attacked are unusually careful here:
`prop:restrict-refinement-monotonicity` is explicitly "for every comparable pair" and immediately
followed by `prop:restrict-nonnested-unordered`; `prop:ig-generalized-spectrum-invariance` is
immediately followed by the singular-pencil caveat `(L,Λ) = (L,L)`; `thm:cg-holonomy-kl-marginal`
separates "infimum attained" from "infimum zero but not attained". I found no proved-at-a-point /
used-on-a-neighbourhood slip in `Theory/`. The one real family-vs-fixture slip is F-1 above, and it
lives in the **code's declared domain**, not in a theorem.

---

## 6. Summary table

| ID | Sev | Type | Finding |
|---|---|---|---|
| F-1 | HIGH | calibration | `max_frame_condition=1e6` and `min_spd_rcond=1e-12` admit inputs where the graded identity residual exceeds `atol+rtol=1.01e-10` by up to 4.5 orders. Safe values ≈ `3e3` and `1e-7`. |
| F-2 | MED-HIGH | diagnostic | `GAU-01_eigenpair_residual` is a backward error: `3.2e-17` alongside a forward spectrum error of `1.85e-6`. Cannot corroborate the spectrum. |
| F-3 | LOW-MED | gate | Interaction-family membership is tested as "symmetric within `1e-10` relative", then silently symmetrised; the predicate implemented is not the one `prop:cg-kron-leaves-family` is about. |
| F-4 | LOW | tooling | `retain_interaction_order` rejects `maximum_order=0`, so the shipped projector cannot compute the norm `thm:rg-hoeffding-action-isomorphism` bounds. |
| L-1 | — | load-bearing | `cor:cg-compact-holonomy-barycenter` fails hard if compactness is weakened to "closed + \|det h\|=1"; explicit `GL⁺(2)` witness with divergent orbit average and empty invariant family. Proof text names only the non-essential consequence of compactness. |
| L-2 | — | load-bearing | Sandwich `Ω_ij` satisfies the cocycle exactly for non-commuting `φ` (`6e-17`); the additive surrogate violates it by `8.5e-2`. No conflation found in `Theory/` or `src/` (there is no matrix exponential in `src/` at all). |
| L-3 | — | load-bearing | `P₀ ≻ 0` in `thm:obs-star-fixed-point-contraction`: rate is attained, not slack, and degrades to `ρ→1` at the boundary exactly as the text states. |
| SR-1 | — | correction | **Wave-1 RG-7 is overstated.** The belief barycenter is exactly `GL⁺(K)`-equivariant with no compactness; PIFB2:1577 says so. Downgrade to a citation-scope slip at PIFB2:1559/:1644. |
| SR-2 | — | self-refute | Apparent violation of the star contraction rate was a float64 noise-floor artefact. |

---

## 7. Reproduction

All scripts are self-contained, CPU-only, and were run with `PYTHONPATH=src` from the repository root
under Python 3.10.12 / numpy 2.2.6 / scipy 1.15.3 / sympy 1.14.0 / mpmath 1.3.0.

| script | covers |
|---|---|
| `/tmp/atk_gauge.py`, `/tmp/atk_gauge2.py`, `/tmp/atk_gauge3.py` | F-1, F-2 (80-dps `mpmath` reference spectrum) |
| `/tmp/atk_ch11.py`, `/tmp/atk_star2.py` | Chapter 11 stress, sympy normalizer identity, SR-2 |
| `/tmp/atk_group.py` | SR-1, L-1, L-2 |
| `/tmp/atk_restrict.py` | Chapter 7 randomized 350k-pair search |
| `/tmp/atk_finite.py`, `/tmp/atk_fisher2.py`, `/tmp/atk_inf.py`, `/tmp/atk_degen.py` | degenerate / infinite / subnormal code paths, Hoeffding sharpness, Kron witness |

---

## 8. Honest closing assessment

I was sent to break this and could not. The mathematics in `Theory/` survived every attack I could
construct, including the ones the brief predicted would be most likely to land: non-compact `G`
(the theory assumes compact closure explicitly, and the assumption is correctly load-bearing);
KL asymmetry and infinities (the chapters state their results in `[0,+∞]` and supply their own
finiteness counterexample); the non-abelian transport form (the sandwich form is a coboundary and the
cocycle is exact without commutativity, and the codebase contains no matrix exponential to slide on);
coarse-map composition leaving the admitted tier (`prop:rg-product-equivalence-not-preserved`
constructs exactly that arrow and refuses to admit it); and boundary/degenerate inputs (the finite
lab rejects self-loops, multi-edges, empty blocks, repeated vertices, and singular assemblies, and
returns exact residuals at subnormal masses).

Wave 1's verdict that the mathematics is strong survives an adversarial second pass, and one Wave-1
finding (RG-7) should be softened as a result. The remaining exposure is not in the theorems but in
the numerical domain the code declares for itself: `max_frame_condition` and `min_spd_rcond` are set
several orders of magnitude looser than the tolerance at which the results derived from them are
graded, and one of the three published gauge diagnostics is structurally incapable of detecting the
resulting error.
