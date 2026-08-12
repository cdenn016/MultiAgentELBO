# Audit 02 — Probability / ELBO / Exponential Families / Information Geometry

Adversarial rigor audit. Scope: `MultiAgentELBO/Theory/{03,04,05,05a,05b,05d,06,06a,07,08}*.tex`,
`src/multiagent_elbo/finite/*`, `realizations/gaussian/*`, and the corresponding PIFB2 sections.
Baseline: repo as mounted 2026-08-11. Prior audit `docs/audits/2026-08-11-post-fixed-ray-deep-audit.md`
read first; AUD-01..22 are not re-reported except where I re-probed them.

Everything labelled "verified" below was actually executed; the commands and outputs are quoted.

---

## Executive summary

The rigorous chapters in scope are, on the mathematics I could check, **unusually clean**. Chapter 5
(`05_elbo.tex`) is a genuinely correct measure-level ELBO development: one fixed normalized joint,
an extended-real functional defined for *every* probability law, a gap identity that never writes
`-inf + inf`, absolute continuity and log-integrability separated into (H3)/(H4) with explicit
witnesses showing (H4) is not implied by (H3). Chapter 8's Gaussian information geometry is correct
in every identity I recomputed. `05a` states minimality/regularity hypotheses and uses them where
required. The finite code is honestly typed (`fisher.py` carries `establishes_dqm: bool = False`;
the parameter-dependent-channel fixture is filed as `assumption_boundary`, not as a refutation).

The defects are therefore not arithmetic. They are **structural, of three kinds**:

1. **The rigorous development does not contain PIFB2's central results.** `Theory/SPEC.md` bans
   PIFB2 outright ("PIFB2 does not appear. Not as a source, not as a crosswalk, not as motivation").
   The consequence is that the state-level mean-field ELBO obstruction, the transformer-recovery
   theorem, the `-tau log Z` envelope reduction, the Brouwer equilibrium, the belief-configuration
   Gibbs lift, the mass/second-variation section and the timescale hierarchy have **no rigorous
   counterpart anywhere**, and **no ledger entry records their absence**. Against the stated project
   goal ("a rigorous version of PIFB2.tex") this is the single largest gap. HIGH.
2. **A handful of definitions are dressed as theorems** in `05b`, in violation of the manuscript's
   own SPEC §2.1 discipline.
3. **Two code/theory mismatches**: unconditional Moore–Penrose inversion of a possibly degenerate
   Fisher matrix, which `05d prop:hist-semidefinite-gradient-obstruction` explicitly forbids; and a
   categorical exponential family with no minimality check.

I also found a **constructive** result: PIFB2 explicitly declines to test the obstruction on the
reduced (envelope) potential it actually implements. I ran that test at 60 decimal digits and the
obstruction **also holds** for `-tau sum_i log Z_i` in an explicit witness. The manuscript is
understating what it can prove.

Nothing I checked is arithmetically wrong. No CRITICAL findings.

---

## Findings

### F1 — PIFB2's load-bearing results have no rigorous counterpart, and the gap is unrecorded
**Class: (b) MISSING DERIVATION. Severity: HIGH.**

`Theory/SPEC.md:16-20` forbids PIFB2 from appearing in the rigorous manuscript. Verified by grep
over all of `Theory/*.tex`:

```
Brouwer                : (none)
belief configuration   : (none)
mass matrix            : (none)
second variation       : (none)
adiabatic              : (none)
reduced free energy    : (none)
transformer            : (none)
dot-product            : (none)
third variation / mixture-open / state-level no-go : (none)
```

So the following PIFB2 results are **not** made rigorous and **not** listed as open in
`Theory/appendix_claim_ledger.tex`:

| PIFB2 result | Location | Rigorous counterpart |
|---|---|---|
| `thm:state_level_elbo_nogo` (mean-field ELBO obstruction) | `PIFB2.tex:3281` | **none** |
| `thm:transformer_recovery` (R1)-(R3),(N) | `PIFB2.tex:1195` | **none** |
| `-tau log Z` envelope reduction + envelope gradient | `PIFB2.tex:832-871` | **none** (see F10) |
| `thm:self_consistent_source_equilibrium` (Brouwer) | `PIFB2.tex:~3340` | **none** |
| `thm:belief_configuration_gibbs_lift` | `PIFB2.tex:3578` | **none** |
| mass matrix / reduced-Hessian identity | `PIFB2.tex:1413-1508` | **none** |
| timescale hierarchy / adiabatic reduction | `PIFB2.tex:929-963` | **none** |

What the rigorous document *does* supply in place of the obstruction is weaker and, in one respect,
opposite in sign:

- `req:gen-typing-prohibition` (`04_generative.tex:120`) — a **DEFINITION**, explicitly "proves
  nothing";
- `prop:gen-no-distinguished-target` (`04_generative.tex:130`) — establishes only that a
  `Q`-indexed family selects no member;
- `prop:gen-moving-target-witness` (`04_generative.tex:163`) — **refutes** three stronger readings
  with a closed-form binary witness (`e(Q_beta) = log(1/2)` for all beta).

That is a good, honest triple, but it is not the obstruction, and a reader of either document cannot
determine which PIFB2 claims survived rigorization.

**Fix.** Add a PIFB2 crosswalk appendix (or, if SPEC's ban is inviolable, a separate crosswalk
document) listing each PIFB2 Level-2 theorem with status `ESTABLISHED-HERE / OPEN / NOT-CLAIMED /
SUPERSEDED`. Minimally, add the seven rows above to `appendix_claim_ledger.tex` as `OPEN`.

---

### F2 — The obstruction proof hand-waves its analytic hypotheses
**Class: (c) WEAK RIGOR. Severity: MEDIUM.** `PIFB2.tex:3279`.

> "All differentiated integrals below are assumed finite."

That single sentence discharges: (i) three differentiations under the integral sign in
`eq:consensus_third_variation`; (ii) finiteness of `D^3` of `F_rest`; (iii) the interchange needed
to conclude `int a_i g_ij = Var_{q_i}(g_ij)`. No dominating function is exhibited, no `L^1`
majorant, no statement that `t -> KL(q_i(s) || T_ij q_j(t))` is `C^3` on a neighborhood of `0`.

Two further silent hypotheses:
- `g_ij = (T_ij h_j / T_ij q_j)^2` requires `T_ij q_j > 0` `q_i`-a.e. This is never stated. For a
  general "mass-preserving positive linear transport" it can fail on a positive-measure set, at
  which point `g_ij` is undefined rather than merely unbounded.
- The admissibility of `a_i = q_i (g_ij - E_{q_i} g_ij)` is argued only from boundedness of
  `g_ij`. Mixture-openness as defined at `PIFB2.tex:3279` requires `q_i + t a_i in Q_i` for *all*
  small `|t|`; boundedness gives nonnegativity but not membership in `Q_i` unless `Q_i` is the full
  positive-density set.

Contrast `Theory/05d_relational_inference.tex:400-425`, which for the analogous differentiation
writes out a chartwise `L^1(Q_{B^c})` dominating function `G_K(b)` for every multi-index
`|alpha| <= 2`. That is the standard this repo has already set for itself.

**Fix.** State the domination hypothesis (e.g. `sup_{|t|<=t_0} |d^2/dt^2 log(T q_j(t))| in L^1(q_i)`),
assume `T_ij q_j > 0` `q_i`-a.e., and either define `Q_i` as the full positive-density class or
verify closure under the constructed perturbation.

**Verified.** The algebra of the proof itself is correct. At 60 dps (`mpmath`), with `n = 3`,
`tau = 0.8`, zero-mass tangents `a_1, h_2`:

```
single-edge  D3_{q1 q2 q2}[a1,h2,h2] = 7.6952955572e-8
Var_{q1}(g12)                        = 7.6952955572e-8      (agree to 11 digits)
fixed-joint mean-field control  D3   = -3.63009224554e-65   (numerical zero)
```

So `eq:consensus_third_variation`, the choice of `a_i`, and `eq:fixed_joint_third_variation_zero`
are all confirmed.

---

### F3 — The obstruction is proved only at frozen attention; the abstract does not say so — and the untested case is provable
**Class: (e) OVERCLAIM (adjacency). Severity: MEDIUM.** `PIFB2.tex:59` (abstract) vs
`PIFB2.tex:3330` (`rem:state_level_elbo_nogo_scope`).

The remark is honest: "If the attention optimum `beta*(q)` has already been substituted, its
response derivatives define a different reduced functional and require a separate representation
test." But the abstract states the obstruction two sentences after asserting that the checked-in
implementation "differentiates this scalar total" — i.e. next to a description of the *reduced*
functional to which the theorem does not apply. A reader will merge them.

**I ran the missing test.** Same 60-dps setup, two agents, one active peer source per row plus a
null source, `tau = 0.8`:

```
frozen-beta consensus C(q)          D3_{q1 q2 q2} = -1.94227605348e-5
reduced  -tau * sum_i log Z_i(q)    D3_{q1 q2 q2} = -3.54085893855e-5
fixed-joint mean-field control      D3            = -3.63009224554e-65
```

Since `D^3_{q_i q_j q_j} KL(prod q || p) = 0` identically for any fixed `p`, the nonzero value for
the reduced potential shows that **the envelope potential the implementation actually descends is
also not the negative ELBO of any fixed state-level joint**, in this witness.

**Fix.** Either (a) prove the reduced case (the third-variation computation is a chain rule through
`-tau log Z`; the witness above shows a proof will not be obstructed by an identical vanishing), or
(b) put the frozen-`beta` scope qualifier into the abstract sentence itself.

---

### F4 — Definitions presented in the grammar of theorems
**Class: (d) VACUOUS / TRUE-BY-CONSTRUCTION. Severity: MEDIUM (SPEC violation), LOW (math).**

- `05b_local_collective_elbo.tex:153` `\theoremheading{Collective interaction VFE}` — the boxed
  display is `F_o^ext(Q) := -log Z(o) + KL(Q||Pi_o)`. A `:=`.
- `05b_local_collective_elbo.tex:294` `\theoremheading{Local multi-agent ELBO}` — likewise
  `F_{B,o}^ext(r_B;b) := -log Z_B(b) + KL(r_B||Pi_{o,B})`.

Both carry `\status{ESTABLISHED}` and a "Proof". The only non-definitional content is
`L <= log Z` with equality iff `Q = Pi_o`, which is nonnegativity of relative entropy applied to a
quantity just defined to be `log Z` minus that relative entropy. SPEC.md §2.1 requires `DEFINITION`
to "say plainly that nothing is being proved", and treats grammar/status mismatch as a defect.

**Fix.** Split each into `\definitionheading` (the boxed `:=`) plus a one-line
`\propositionheading` for the bound and equality case.

Marginal cases, reported for completeness, not as defects: `thm:obs-local-global-potential`
(`05b:347`) is a genuine theorem (a chain-rule identity, correctly hypothesized on a *shared*
outside marginal); `thm:obs-agent-interaction-equivalence` (`05b:721`) is Kallenberg's
randomization lemma plus a trivial converse, correctly cited.

---

### F5 — "Local evolution is collective descent" silently narrows the family and drops the locality hypothesis
**Class: (c) WEAK RIGOR. Severity: MEDIUM.** `05b_local_collective_elbo.tex:670-708`.

Three issues in one short section:

1. **Silent narrowing.** `thm:obs-local-global-potential` (`05b:347`) holds for arbitrary correlated
   `Q = Q_{B^c} r_B`. The descent corollary `eq:obs-local-natural-gradient` is stated only for a
   "regular product recognition family". The chapter's own headline — that local objectives are
   coordinate potentials of the collective — is therefore *not* what the dynamics section proves.
   The narrowing is never flagged.
2. **Block-diagonality is a theorem, not a hypothesis.** `05b:675` assumes
   `G(eta) = (+)_i G_i(eta_i)`. For a product family this is automatic (Fisher information of a
   product of independent families is the direct sum). Stating it as a hypothesis, and then writing
   "Block orthogonality is load bearing. With a nondiagonal Fisher metric..." (`05b:696`), reads as
   if the product family could have a nondiagonal metric. It cannot; the warning applies to
   *non-product* families, which the corollary already excluded.
3. **"Local" equivocates.** The flow requires `E_{Q_{B^c}}[...]`, i.e. agent `i` must know the
   outside marginal. That is *graph*-local only when `Z_B(b)` and `Pi_{o,B}(.|b)` depend on `b` only
   through neighbors of `i` — which needs the condition stated 600 lines earlier at `05b:63-65`
   ("A graph-local Markov blanket requires the additional condition that the regular conditionals of
   `P_0` have the corresponding locality") and never re-invoked. For correlated `P_0`,
   `P_{0,B}(dy_B|b)` depends on all of `b`, and the "local" flow is not local in any operational
   sense.

**Fix.** (i) State the corollary for arbitrary `Q_{B^c}` with block coordinates, or say why the
product restriction is needed. (ii) Demote block-diagonality to a remark with a one-line proof.
(iii) Re-invoke the `P_0`-locality condition explicitly in this section, and say what "local" means
when it fails.

---

### F6 — Code applies a pseudoinverse the theory explicitly forbids applying silently
**Class: (c) WEAK RIGOR / code-theory mismatch. Severity: MEDIUM.**

`Theory/05d_relational_inference.tex:560` `prop:hist-semidefinite-gradient-obstruction` ends:

> "A justified metric quotient or a separately declared regularization is therefore required before
> an inverse or pseudoinverse is used."

`src/multiagent_elbo/finite/information_history.py:138-143`:

```python
pseudoinverse = np.linalg.pinv(fisher, rcond=rcond_value, hermitian=True)
projector = fisher @ pseudoinverse
range_residual = float(np.linalg.norm(gradient - projector @ gradient, ord=np.inf))
natural_gradient = -(pseudoinverse @ gradient)
```

The residual `||g - P g||` is exactly the quantity that decides whether `G x = g` is solvable — i.e.
whether a natural gradient exists at all — and it is **computed after the pseudoinverse is applied
and never gated on**. `used_pseudoinverse` is set from `nullity > 0`, not from solvability. A caller
receives a finite `natural_gradient` vector even in the `prop:hist-semidefinite-gradient-obstruction`
"no solution" branch.

To be fair: the naming `inverse_rule = "moore_penrose_identifiable_tangent_quotient"` is *correct*
mathematics when `g in range(G)` — the class `[G^+ g] in T/ker G` is then canonical, since any two
solutions differ by `ker G`. The defect is that the precondition is diagnosed but not enforced.

**Fix.** Raise (or return a typed `unsolvable` result) when `range_residual` exceeds a declared
scale-relative threshold, and record the declared quotient/regularization in the result object.
This is separate from, and compounded by, known **AUD-15** (rank threshold `rcond*max(1,lmax)` at
`information_history.py:80` vs `pinv`'s `rcond*lmax` at `:138`), which I confirm is still present.

---

### F7 — Categorical exponential family accepts non-minimal sufficient statistics
**Class: (c) WEAK RIGOR. Severity: LOW-MEDIUM.**
`src/multiagent_elbo/finite/categorical.py:44-68`, `:137-145`.

`CategoricalExponentialFamily.__init__` validates shape and finiteness of
`sufficient_statistics` but never checks that no nonzero `a` makes `<a, T>` constant across labels —
i.e. `hyp:exp-regular-minimal` (`05a_expfamily.tex:163`) and the positive-definiteness conclusion of
`prop:exp-minimal-fisher-nondegenerate` (`05a:169`) are not enforced. `fisher_information` then
returns a singular Gram matrix, which flows straight into the unconditional `pinv` of F6.

The repo evidently knows this: `information_history.py:666-673` deliberately builds a
`rank_family` fixture to exercise the rank-deficient path. So the degeneracy is intentional as a
*control*, but there is no way for a caller to assert minimality when it is required.

**Fix.** Add a `minimal` property computed from `rank(T - 1 mean(T)^T) == parameter_count`, and a
`require_minimal=True` constructor flag used by any path that treats the Fisher form as a
Riemannian metric.

---

### F8 — Circular/vacuous hypothesis clause in the cumulant proposition
**Class: (c) WEAK RIGOR. Severity: LOW.** `05a_expfamily.tex:138-161`.

The statement is conditioned "at every interior parameter **where local exponential domination
permits differentiation under the integral**", and the proof then shows local exponential domination
holds at *every* interior point (via `|x|^r <= C(e^{eps x} + e^{-eps x})`). The conditional clause is
therefore vacuous; it makes the result look weaker and more hypothesis-laden than it is, and invites
readers downstream to think they must re-check it.

**Fix.** State it unconditionally on `int N` and keep the domination argument in the proof.

---

### F9 — AUD-03 (structural tolerances destroy probability invariants) confirmed still open
**Class: (a) ERROR (known). Severity: MEDIUM.** `finite/measures.py:67-70`, `:99-101`.

Re-probed at HEAD:

```python
n = NumericsConfig('float64', 2.0, 2.0)
ProbabilityMeasure(('a','b'), [0.0, 0.0], n)          # ACCEPTED, total_mass = 0.0
MarkovKernel(('a','b'), ('x','y'), [[0,0],[0,0]], n)  # ACCEPTED
```

Not re-reported as new; recorded because it is remediation item #1 in the prior audit and is still
live, and because F6/F7 above sit on top of the same "diagnose but do not enforce" pattern.

Note the sharper probe in the prior report (masses `(0.4, 0.4)`) is now *rejected* at
`rtol = atol = 0.1`; the defect requires `atol >= 0.2`. The class of the defect is unchanged.

---

### F10 — The bridge equation for PIFB2's envelope claim is missing from the rigorous chapter
**Class: (b) MISSING DERIVATION. Severity: LOW-MEDIUM.** `05b_local_collective_elbo.tex:568-600`.

`prop:obs-attention-elbo` derives `F_i^att(beta) = KL(beta||pi) + (1/tau) sum_j beta_j E[D_j]` and its
softmax minimizer. It never states the value at the minimum, which is exactly
`F_i^att(beta*) = -log Z_i`, `Z_i = sum_k pi_k exp(-E_{Q_Y}[D_k]/tau)` — the identity on which the
whole PIFB2 envelope / potential-descent argument rests. One line would connect the two documents.

Related and correctly handled: `05b:641-646` states that the "familiar" row functional
`sum_j beta_j E[D_j] + tau KL(beta||pi)` equals `tau F_i^att` and that **for `tau != 1` it is not an
independently weighted sector of one standard global ELBO**. PIFB2 runs at `tau = kappa sqrt(K_q)`
(`PIFB2.tex:673`) and concedes the point at `PIFB2.tex:678`. The two documents agree; only the
bridge equation is absent.

---

### F11 — "Potential descent" conflates conservativity with descent
**Class: (e) OVERCLAIM. Severity: LOW-MEDIUM.** `PIFB2.tex:59` (abstract).

> "...its active update is potential descent rather than a nonintegrable softmax-response field."

What is proved is that the field is *conservative* (the gradient of `-tau sum_i log Z_i`). Descent
additionally needs a step-size/acceptance condition — which is precisely
`prop:elbo-finite-step-nonmonotonicity` (`05_elbo.tex:610`), whose closed form
`L(theta+) - L(theta) < 0 for alpha > 2/d_max` shows finite natural-gradient steps can *increase* the
free energy. Separately, `PIFB2.tex:2493` says the gauge sector uses a **left-trivialized group
retraction**, which is not a step of the same gradient flow at all.

**Fix.** Say "conservative / potential field" in the abstract, and cite the step-size requirement.

---

### F12 — Minor items
- `08_infogeometry.tex:41-43` "The family is regular and minimal, so the Legendre map is a
  bijection" is asserted with a citation but not checked for the specific chart. Trivial to
  discharge (`<a,T> = a_1' y + tr(A_2 y y')` is a.e. constant only for `a = 0`; `N = R^n x Sym_{--}`
  is open). **(c), LOW.**
- `finite/vfe.py:184` requires *bitwise* equality of outside marginals
  (`np.array_equal(before_outside, after_outside)`). Mathematically correct, but any float-derived
  pair of conditionals fails it; I had to construct dyadic-rational fixtures to exercise the
  function. Conservative rather than wrong. **(c), LOW.**
- `05_elbo.tex:39` `thm:elbo-total-correlation-chain`: the monotone-limit paragraph alone would not
  suffice; the explicit branch audit that follows is what carries the singular cases, and it is
  complete. No defect, noted so a future editor does not delete the second paragraph. **(c), LOW.**

---

## Verified solid (what I actually recomputed)

All checks below were executed in the session workspace (`numpy`, `mpmath` at 60 dps).

**Local vs collective free energy (`05b`).** Two agents, two binary latents, a *correlated*
baseline `P_0`, three factors with overlapping scopes.
- `thm:obs-local-global-potential` (`05b:347`): `F_o(Q') - F_o(Q) = E_{Q_{B^c}}[F_B(r') - F_B(r)]`
  reproduced to `4.44e-16`.
- `eq:obs-local-global-decomposition` (`05b:373`) energy form reproduced to `4.44e-16`.
- `eq:obs-singleton-incident-counting` (`05b:461`): `sum_i H_{{i},o} = sum_a |da| E_{a,o}` verified
  exactly on all states.
- `src/.../finite/vfe.py::block_update_decomposition` residual `1.11e-16` on an independent dyadic
  fixture.
- **The chapter's refusal to claim a summed-local bound is correct and necessary.** Over 2000 random
  3-factor systems, the outside-averaged sum of local log-evidences exceeded `log Z(o)` in 40 cases
  and fell below it in 1960 — so `sum_i L_i` bounds `log Z` in **neither** direction. The chapter
  never claims it does; this is the trap it avoids. The exact gap term is the counting identity plus
  the outside-KL term in `eq:obs-local-global-decomposition`; double counting of shared records is
  handled by the `|da|` multiplicity in `eq:obs-singleton-incident-counting`, and the chapter says
  plainly (`05b:474-478`) that the local VFEs "are not themselves the single-count ledger".

**Information geometry (`08`), general `n = 3`, random SPD `Lambda`, nonzero `mu`, Frobenius-paired
symmetric chart:**
- `eq:ig-meanblock` `(1 + mu'Lam mu)Lam + Lam mu mu' Lam`: max error `9.1e-13`.
- `eq:ig-crossblock` `-u' Lam B Lam mu`: max error `5.7e-14`.
- second block unchanged from the moment chart: exact `0.0`.
- `cor:ig-expectation-mean-quotient`: Schur complement equals `Lambda` to `9.2e-13`.
- `cor:ig-mean-block-discrepancy`: eigenvalues of `Lam^{-1} g_[mumu]` came out
  `{164.09003485, 164.09003485, 327.18006970}` against predicted `1 + mu'Lam mu = 164.09003485`
  (multiplicity `n-1`) and `1 + 2 mu'Lam mu = 327.18006970` (multiplicity 1). Exact match.
- `prop:ig-pullback-vs-pushforward` `B'Lam B - (B'Lam^{-1}B)^{-1} = (B'Lam Bp)(Bp'Lam Bp)^{-1}(Bp'Lam B)`:
  `1.3e-15`.
- `eq:ig-lognormalizer`, `eq:ig-expectation`, `eq:ig-dual-inverse` checked by hand
  (`dA/dS = mu mu' + C = M_2`; `g_tau = g_eta^{-1}` since `dtau/deta = g_eta`). Correct.
- `prop:ig-hermite-exponential-domain` (`08:364`) checked by hand: `N_1(t) = e^{t^2/2}`,
  `N_2(t) = e^t (1+2t)^{-1/2}` finite iff `t > -1/2`, odd `k>=3` divergent for all `t != 0`, even
  `k>=4` finite iff `t >= 0`. Correct.
- `prop:ig-generalized-spectrum-invariance` / `-localization` (`08:438`, `08:457`): correct,
  including the `det(L - d L) == 0` singular-pencil caveat and `dim ker L >= K`.
- The Campbell-vs-Chentsov distinction at the end of the chapter ("a characterization, but not
  uniqueness up to scale") is right and is rarely stated correctly in this literature.
- The whole "chart correction" section (`08:73-188`) is, in my view, the strongest passage in scope:
  it identifies and repairs a real and common error (calling the expectation-chart mean block "the
  precision") and distinguishes restriction from quotient explicitly.

**Exponential families (`05a`).** `eq:exp-kl-bregman` and `eq:exp-kl-dual-bregman` checked by hand
(argument order of the dual Bregman divergence is correctly reversed); `eq:exp-projection-kkt` is the
correct stationarity condition for `D_{A*}(tau, tau_theta)` on `{B tau = b}`. Regularity (`N` open),
minimality, and the local-exponential-domination argument are all present and used where needed.
`prop:exp-domain-boundary-no-law` and `prop:exp-fixed-point-no-law` correctly separate the operator
cone from the probability layer; the `A(theta) = -1/2 log theta` witness with `Psi(theta)=theta/2` is
correct. No use of a Fisher metric on a family not established regular.

**Fisher / natural gradient.** `src/.../finite/fisher.py`: the law-of-total-covariance identity
`I_fine = I_coarse + E[Cov(score | z)]` reproduced with residual `2.22e-16`, defect PSD, and — this
is the important part — the result object carries `establishes_dqm = False` and
`identity_scope = "finite_centered_score_fixed_kernel"`. This is **not** an unearned
data-processing/Chentsov claim; it is the algebraic identity, correctly typed.
`Theory/05d:860` `thm:hist-record-clock-contraction` states the genuine monotonicity via score
projection + law of total variance, with parameter-independence load-bearing, an explicit
counterexample when it fails (`05d:~906`), and — notably — the *retirement* of the `b`-fold
replication pseudo-counterexample (`05d:918-931`), which is a subtle point handled correctly.
`finite/counterexamples.py:437-500` supplies the exact rational parameter-dependent-channel control
(fine Fisher `0`, coarse Fisher `1/(1-theta^2) > 0`) filed as `assumption_boundary`, not as a
refutation. Correct. So: the "Fisher contraction" is a genuine monotonicity result, not a numerical
observation, and its hypothesis boundary is exhibited by construction.

**Envelope / attention (PIFB2).** All verified numerically (`n = 4` sources, `d = 3` state
dimensions, quadratic energies):
- `F_i,full(beta*) = -tau log Z_i`: `min_beta L = -0.10738678690` vs `-tau log Z = -0.10738678695`.
- envelope gradient `dF_red = sum_j beta*_j dE_j`: error `6.4e-11`. (Danskin is not even needed:
  the minimizer is unique by strict convexity of the entropy on the simplex, and `-tau log Z` is
  directly differentiable whenever the `E_j` are.)
- reduced-Hessian identity `Hess F_red = sum_j beta*_j Hess E_j - tau^{-1} Cov_{beta*}(grad E)`
  (`PIFB2.tex:1413`): error `3.8e-7` against central finite differences (that is the FD floor).
- `Cov_beta(X) = (1/2) sum_{j,k} beta_j beta_k (X_j - X_k)(X_j - X_k)'`: `2.2e-16`, so the
  `D_i^2/(2 tau)` spectral bound follows.
- The `alpha*` product-rule algebra at `PIFB2.tex:827-829` checked by hand: with
  `alpha* = c_0/(b_0 + D)`, differentiating through `alpha*` gives prefactor
  `alpha*(1 - alpha* D/c_0) = (alpha*)^2 b_0/c_0`. Correct as printed.
- Softmax/entropy-regularization sign and temperature placement in
  `prop:obs-attention-elbo` (`05b:547`) checked by hand: `KL(beta^Q||beta^P) = KL(beta^Q||pi) +
  tau^{-1} sum beta^Q D + log Z`; the row contribution to the collective VFE derived independently
  from the augmented joint `P_0^Y (x) prod pi_i` matches `eq:obs-attention-full-contribution`
  exactly; unique interior minimizer `softmax(-E[D]/tau)` on the positive-prior simplex. Correct.
- Replicator flow `eq:obs-attention-replicator` and dissipation `-gamma Var_beta(c)` (`05b:652-666`)
  checked by hand; the missing `+1` from `d(b log b)/db` correctly drops out of the centered form.
  `eq:rg-attention-beta-softmax` (`07b:2479`) likewise correct, including the `E_J tau_dot/tau^2`
  term.
- `05b:602-608` correctly warns `beta^{Q*} != E_{Q_Y}[beta^P(Y)]`, and `05b:610-639` gives the
  correlated-conditional ledger with the extra `E_{Q_Y} TC(Q_{J|Y})` term — i.e. it refuses to
  assert a row softmax under an unrestricted coupled family. That is the right refusal.

**Attention recovery honesty (PIFB2 `thm:transformer_recovery`).** The learned bilinear `M` is
**not** smuggled: it is hypothesis **(R3)**, "an object external to the gauge data", with the
consequence spelled out ("Replacing that cross term by the learned bilinear ... **replaces** the KL
rather than reducing it: the resulting score is itself a divergence only for orthogonal `M`" —
correct, since `||mu_i - M mu_j||^2` matches the score only when `||M mu_j|| = ||mu_j||`). The
key-norm problem is handled correctly and at length: the concentration argument is **rejected** as
insufficient (fluctuation `O(sigma_0^2 sqrt(d_k))` is the same order as the content logits after
`tau = kappa sqrt(d_k)`), and (N) is given three exact realizations plus the honest statement that
outside them "the KL limit gives a distance/RBF-style attention with a residual key-dependent bias
rather than pure dot-product attention". The untied route's forced positive self-scores
`Q_j'K_j = mu_j' Sigma_j^{-1} mu_j > 0` and the resulting **incomparability** of the two function
classes are stated. Sign and temperature bookkeeping check out
(`beta ~ exp(+mu_i' M mu_j/(tau sigma^2))` with `M = sigma^2 W_Q W_K'`, `tau = kappa sqrt(d_k)`).
This is the most honest attention-recovery write-up I have audited.

**Measure theory (`03`), generative (`04`), restrictions (`07`).**
- `thm:prob-mixed-family-common-domination` (`03:87`): correct, both directions, including the
  moving-atom nondominability witness.
- `thm:prob-kernel-rn-measurable-version` (`03:185`): the partition-martingale construction is
  correct, and the caveat "independently selecting an RN derivative for each `x` does not establish
  joint measurability" is exactly the right warning.
- The `phi(o)phi(y)` / `phi(0)psi(y)` null-slice witness (`03:170`) correctly justifies the
  a.e.-in-`o` qualifier that every later ELBO statement inherits.
- `prop:gen-exact-normalization` (`04:205`): reverse-topological Tonelli argument, correct. **The
  evidence is a genuine normalized marginal likelihood density**, not a partition function in
  disguise; `05b`'s `Z(o) = int L_o dP_0` is likewise the record-marginal density w.r.t. the declared
  product `nu = (x)_a nu_a`, and `Z_B(b)` is the genuine conditional evidence of the incident
  records given the outside state. Every kernel in `hyp:local-interaction-kernels` is normalized by
  type before any density is extracted (`03:123-137`).
- `thm:restrict-determinant-gap` (`07:90`): `(1/2)[sum_b log det J_bb - log det J] >= 0` — I
  independently re-derived this from `KL(N(mu, blockdiag(J_bb^{-1})) || N(mu, J^{-1}))`; the trace
  term is exactly `n`, so the gap is Fischer's inequality. Sign and orientation correct, and it
  matches `Theory/verification/tests/test_factorization_gap.py`'s independent 100-digit `mpmath`
  oracle `(sum log det block - log det whole)/2`.
- `hyp:elbo-evidence-domain` (H1)-(H4) with the Gaussian/Cauchy witness for (H4) and the
  `c/(n (log n)^2)` witness showing finite KL does not imply (H4): both correct.
- `prop:elbo-total-correlation-signs` (`05:66`): the sign is right and is the point — substituting
  marginal entropies gives a *larger* pseudo-ELBO that is not a bound.

**Hoeffding / ANOVA (item 9).** `07b_agent_network_rg.tex:1130-1240`. The product-reference premise
is explicit (`pi_l ~ nu_l`, `nu_l` a product), it is **not** assumed preserved —
`prop:rg-product-equivalence-not-preserved` gives the diagonal-cloning counterexample showing no
equivalent product reference exists at the target — and, critically, the decomposition is stated in
`L^infty` with `||g|| = sum_A ||g_A||_inf`, **never** as an `L^2(pi)` orthogonal decomposition. The
projector orthogonality `P_A P_B = 1_{A=B} P_A` is w.r.t. the product `nu`, which is the only place
it holds. I checked the two quantitative claims by hand: `sum_{A != empty} 2^{|A|} = 3^n - 1`, and
the sharpness witness `sum_{A != empty} ||P_A f||_inf = (4p-1)^n - (2p-1)^n -> 3^n - 1` (recomputed:
`||P_A f||_inf = (2p)^{|A|}(2p-1)^{n-|A|}`, summing to `(4p-1)^n`). Both correct.
`finite/interactions.py` and `counterexamples.py::hoeffding_decompose_action` use uniform-product
references, consistent with the premise. **No use beyond the admitted scope was found.**

**KL hygiene (item 8).** `prop:elbo-subspace-support-singular` (`05:139`) is the exact mechanism
forbidding subspace-supported recognition laws, with the correct scope note that a proper *closed*
support subset is not enough (the `Unif[0,1/2]` vs `Unif[0,1]` example, `KL = log 2`).
`prop:elbo-relative-log-representation` (`05:193`) handles the `-u log u <= 1/e` negative-part bound
so the extended integral is well defined in `(-inf, +inf]`. `finite/vfe.py::_kl_arrays` returns
`inf` with the offending state label rather than a NaN. In the Gaussian realization the SPD
requirement is **mathematically necessary**, not a band-aid: `hyp:gen-lg-spd` (`06a:90-99`) is what
makes every conditional a normalized density, and `prop:elbo-subspace-support-singular` shows that
relaxing it to PSD makes the bound `-infinity` rather than large-but-finite. (The *tolerance* gates
in `realizations/gaussian/interactions.py` are a separate, numerical matter and are already
AUD-14/AUD-19.)

---

## Next steps (priority order)

1. **Write the PIFB2 crosswalk** (F1). Seven `OPEN` ledger rows minimum. This is the difference
   between "a rigorous version of PIFB2" and "a rigorous document adjacent to PIFB2".
2. **Close the reduced-potential representation test** (F3). The `-tau sum log Z` third variation is
   a chain rule; my witness shows the target statement is true, so this is provable, not merely
   open. Then fix the abstract sentence.
3. **Discharge F2's analytic hypotheses** in the obstruction proof, to the standard already set by
   `05d`'s chartwise `L^1` domination (`eq:hist-chartwise-vfe-envelope`).
4. **Enforce what you diagnose** (F6, F7, F9): gate on `range_residual`; add a minimality check to
   `CategoricalExponentialFamily`; separate structural normalization policy from numerical
   comparison tolerance. These three are one pattern, not three bugs.
5. **Re-grammar `05b`'s two definitions-as-theorems** and repair the natural-gradient section
   (F4, F5) — restate for correlated `Q`, or say why not, and re-invoke the `P_0`-locality condition.
6. **Add the one-line bridge** `F_i^att(beta*) = -log Z_i` to `05b` (F10).
7. Cosmetic: F8 (drop the vacuous clause), F11 (say "conservative", not "descent"), F12.
