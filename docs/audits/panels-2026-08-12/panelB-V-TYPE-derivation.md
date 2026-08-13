# panelB-V-TYPE-derivation

*Recovered verbatim from workflow journal.jsonl, 2026-08-13. Agent a6cd48b9.*

## target

TARGET V-TYPE — settle whether the auxiliary base cometric gamma is recognition-side (A) or generative-side (B), determine whether it splits, specify the repair if (B), and state the honest headline for each case.

## status

OBSTRUCTED

## theorem_statement

THE TYPING IS MIXED, AND THE LOAD-BEARING HALF IS GENERATIVE (case B). Moreover, the Polyakov bridge fails independently of the typing.

Write the emergent base object in densitized form, g^{mu nu}(c) = rho(c) gamma^{mu nu}(c), as it actually appears in the h->0 limit of the base-neighbour ELBO block (E3).

(T1) DECOMPOSITION [PROVED]. Under the tied-replica mechanism of typed-construction.md:61-111, the four ingredients of g^{mu nu} type as follows:
  (i)  SUPPORT / coupling topology (which design pairs are neighbours): GENERATIVE. It is the edge set of the interaction complex, declared as part of the configuration X (Theory/03_probability.tex:51), and it exists at all only if hyp:gen-design-product is relaxed (Theory/04_generative.tex:89-96).
  (ii) DENSITY rho(c) d^dc: GENERATIVE / experimental-design. It is the design measure and its refinement schedule; Theory/12_philosophy.tex:33-38 types it as "a declared subset, not a random sample from a law on C".
  (iii) REFERENCE ROW pi_{cc'} (the point gamma is pulled toward): GENERATIVE. It is a source prior, a declared component of X (Theory/PIFB2.tex:3422 lists "graph or source priors" inside X), and Theory/03_probability.tex:63 forbids the generative kernel from reading any recognition object.
  (iv) ANISOTROPY / conformal shape (the direction-dependence of gamma at fixed trace): RECOGNITION. It is the base-neighbour row beta_{cc'}, a factor of Q (typed-construction.md:100-105), and eliminating it is an exact ELBO tightening.
Recognition is further constrained by beta << pi (else KL(beta||pi) = infinity): recognition can degenerate a coupling direction to zero but can NEVER create one the generative model lacks.

(T2) FREEZING [PROVED]. At the unit coefficients that the exact-ELBO theorem delivers (exact-elbo-proof.md:136-139: "This equality has unit state-self, model-self, peer-energy, and categorical-KL coefficients"), the per-site row prior KL(beta_c||pi_c) is O(1) while the data it trades against is O(h^2). Hence the exact row optimum satisfies beta* = pi + O(h^2) and moving beta an O(1) distance from pi costs O(1) per site against an O(h^2) gain — a cost/benefit ratio h^{-2} -> infinity. THE RECOGNITION FREEDOM OVER THE BASE COMETRIC IS ASYMPTOTICALLY FROZEN: at leading order gamma^{mu nu} = pi^{mu nu}, the generative row. So in the continuum action the base cometric IS the generative coupling design, and optimizing it is variational EM / type-II maximum likelihood, not ELBO tightening. CASE (B).

(T3) THE ONE WINDOW WHERE (A) SURVIVES [PROVED]. Replicating the transported neighbour copy n_h times per edge is exactly normalized and gives, exactly, KL(Q||P) = KL(beta||pi) + n_h sum_b beta_b KL(q||u_b). With n_h = Theta(h^{-2}) the two terms balance and the row optimum reshapes gamma at O(1). n_h is itself a GENERATIVE structural datum (how many copies P draws). So case (A) holds for the SHAPE of gamma only, and only after the generative model has been given a replication schedule tuned to the refinement. The forced weight h^{d-2} of (E2)/(C3) factors as h^d (Riemann-sum normalization, design-side) times h^{-2} (per-edge replication, generative-side).

(T4) THE PROFILE IS NOT THE INDUCED VOLUME [PROVED, three independent routes]. The exact value of the recognition-side profiling is the soft-min free energy Phi(c) = -log sum_{c'} pi_{cc'} exp(-n_h D_KL(q(c) || (Omega^A_{cc'})_# q(c'))). Its continuum leading form is a SMALLEST-EIGENVALUE (soft lambda_min) functional of the informational pullback h_{mu nu}, not sqrt(det h):
  (a) CONSTRAINT ROUTE. Normalization sum_b beta_b = 1 is a TRACE constraint on gamma. inf{<gamma,h> : gamma psd, tr gamma = 1} = lambda_min(h). The determinant would require a UNIMODULAR constraint det gamma = 1, which gives (det h)^{1/d}, and neither is (det h)^{1/2}. A probability row cannot encode an unnormalized cometric, so the ELBO cannot supply the SCALE of gamma at all — only its direction.
  (b) HOMOGENEITY ROUTE. The soft-min is asymptotically 1-homogeneous under h -> s h (verified: s = 1,10,100,1000 gives 0.99, 6.09, 51.10, 501.10), while sqrt(det h) is d/2-homogeneous (2.83, 89.4, 2828, 89443). These agree only at d = 2.
  (c) CONCAVITY ROUTE. Any profile inf_w{<w,h> + V(w)} is an infimum of affine functions of h, hence CONCAVE in h, for every V, proper or not. By Minkowski's determinant theorem det^alpha is concave on PSD_d iff alpha <= 1/d, so det^{1/2} is concave iff d <= 2. Explicit d=3 witness: f(I)=1, f(4I)=8, chord 4.5, midpoint f(2.5 I)=3.9528 < 4.5. THEREFORE FOR d >= 3 THE INDUCED-VOLUME ACTION IS NOT THE PROFILE-OUT OF ANY AUXILIARY FIELD COUPLING LINEARLY TO h — no ELBO, no prior, no scaling can produce it. And for d = 1, 2 the profile must be positively homogeneous, forcing V to be (the closure of) a convex INDICATOR, i.e. an IMPROPER prior — which breaks the normalization of P on which the whole exact-ELBO theorem rests (typed-construction.md:80 "Every displayed factor is normalized").

(T5) THE POLYAKOV BRIDGE IS A SADDLE, NOT A BOUND [PROVED]. The claim in the task brief is arithmetically correct — for d != 2, delta S_P / delta gamma = 0 gives h_{mu nu} = (1/2) gamma_{mu nu}(tr_gamma h - (d-2)), trace gives tr_gamma h = d, hence gamma = h and S_P = integral sqrt(det h) (verified symbolically in d = 3 and numerically in d = 2,3,4,5 to 0.0e+00). BUT along the conformal ray gamma = t h,
    S_P(t) = sqrt(det h) * t^{d/2 - 1} * (d + (2-d) t) / 2,
    d^2 S_P/dt^2 |_{t=1} = sqrt(det h) * d (2 - d) / 4.
For d >= 3 this is NEGATIVE: gamma = h is a MAXIMUM in the Weyl direction and S_P(t) -> -infinity as t -> infinity (d=3: -20356 at t=256; d=4: -2.66e6). So inf_gamma S_P = -infinity. An ELBO is defined by an INFIMUM over the auxiliary family; a profiling that is a maximum in a noncompact direction is not a variational bound and the profiled functional is not obtained by tightening anything. d = 1 is a genuine minimum (einbein), d = 2 is degenerate (Weyl-invariant: S_P is exactly t-independent). THE BRIDGE IS AVAILABLE ONLY FOR dim C <= 2, AND EVEN THERE ONLY WITH AN IMPROPER WEIGHT PRIOR BY (T4c).

## hypotheses

### 1

FINITE DESIGN, FIXED N. A is a finite agent-site set; the continuum limit refines the base lattice only (worklog:406-407). Theory/02_geometry.tex:25-26 warns the finite design is 'not a continuum limit or a discretization theorem'.

### 2

NORMALIZATION. Every generative factor and every recognition factor is a probability law (typed-construction.md:80, :100-111). This is what forces the TRACE constraint sum_b beta_b = 1 in (T4a) and forbids the improper priors of (T4c). Dropping it dissolves the exact-ELBO theorem.

### 3

hyp:gen-design-product (Theory/04_generative.tex:89-96, status HYPOTHESIS) IS RELAXED. Without this there is no base-neighbour block at all and no gamma of any type; C is then an idle wheel by Theory/12_philosophy.tex:77-78 (worklog E5).

### 4

REGULAR EXPONENTIAL-FAMILY FIBERS for the KL expansion D_KL(q_{th+h}||q_th) = (1/2) g^F h^2 + (1/3) T_skew h^3 + O(h^4) (worklog:79-86, E2); plus hyp:pb-regular-models for the pushforward action.

### 5

SYMMETRIC NEAREST-NEIGHBOUR STENCIL and C^2 sections, so the Amari-Chentsov h^3 term cancels (worklog:93-96). FLAT TRANSPORT ONLY: the covariant cancellation with Omega_{c,c+h} != Omega_{c,c-h} is still open (worklog:102-106) and every h-order statement below inherits that caveat.

### 6

h_{mu nu} POSITIVE DEFINITE on the region considered. Theory/05c_pullback_geometry.tex:122 calls h_s^omega 'a semimetric until its nondegeneracy is proved'; on the rank-drop locus (05c:325-341, and the explicit constant-rank-one witness at 05c:429-432) gamma = h is not invertible and the entire Polyakov variation is ill-posed.

### 7

AUXILIARY COUPLES LINEARLY to the neighbour KLs. This is exactly what the label-copy / replication mechanism produces (conditionally i.i.d. copies give an additive log-likelihood), and it is the only mechanism established in the corpus. (T4c) is a theorem ONLY about this class; an auxiliary entering the transports Omega or the fiber law itself would be nonlinear in h and is not covered.

### 8

ABSOLUTE CONTINUITY beta << pi (typed-construction.md:111), which is what makes the support of gamma generative-side and irreversibly so.


## derivation

## 0. A notation collision that must be fixed before anything is written down

`gamma` is ALREADY TAKEN. In the closed theorem it is the MODEL-channel recognition row: `Q_a^{n+1} = zeta_a(dk,dm) beta_{aj} q_a(dx) gamma_{a l} s_a(dy)` (typed-construction.md:100-105) with block `D_KL(gamma_a || pi_a^s) + sum_b gamma_{ab} D_KL(s_a || v_{ab}^n)` (exact-elbo-proof.md:91-94). Using `gamma` for the base cometric will produce silent errors in exactly the sector under discussion. Use `g^{mu nu}` (densitized) or `lambda_{mu nu}`. Below I write `G` for the base cometric.

## 1. Trace: where G actually enters

The base-neighbour block (worklog §3c.2, worklog:214-217) is

    F_h^base = sum_{<c,c'>} beta_{cc'} D_KL( q(c) || (Omega^A_{c,c'})_# q(c') )  +  sum_c D_KL(beta_c || pi_c).

Reading it against the tied-replica typing:

| ingredient | where it lives | citation | side |
|---|---|---|---|
| `pi_{cc'}` source row | factor of `P_a^n` | typed-construction.md:56-59, :61-78 | GENERATIVE |
| `Omega^A_{c,c'}` transport | factor of `P_a^n` via `u_{ab}^n = (Omega_{ab}^n)_# q_b^n` | typed-construction.md:37-54 | GENERATIVE (lagged; reads `H_n`, not the live `Q`) |
| edge set / which `c'` are sources | configuration `X`: "A configuration may carry the finite interaction complex ... with its edge set" | Theory/03_probability.tex:51 | GENERATIVE |
| design `D`, its measure, its refinement | "the finite design is a declared subset, not a random sample from a law on C. No expectation over contexts is used." | Theory/12_philosophy.tex:33-38 | GENERATIVE / declared |
| `beta_{cc'}` | factor of `Q_a^{n+1}` | typed-construction.md:100-105 | RECOGNITION |

PIFB2 independently types the same objects: `X` is "a slow generative configuration of prior and transition parameters, supports, **graph or source priors**, precision fields, and frame or edge-connection variables. It does not contain the variational posterior densities `q_i` or `s_i`" (Theory/PIFB2.tex:3422). And Theory/03_probability.tex:63 makes it a hard type rule: "The arguments of the generative kernel are `theta` and `X` and nothing else. A recognition law, a recognition parameter, and a posterior are not among them."

So the answer is not a judgement call. `pi`, the edge set, the design and its density are `X`. `beta` is `Q`. **G is built from BOTH.**

## 2. What G IS, constructed from the lattice

Directions `e_1..e_d`, neighbours `c +- h e_mu`, row entries `beta_mu^{+-}(c)` with `sum_mu (beta_mu^+ + beta_mu^-) = 1`. By (E2)/(C3),

    D_KL(q(c) || Omega_# q(c +- h e_mu)) = (1/2) h^2 h_{mu mu}(c) + O(h^4)

on a symmetric stencil (the `h^3` Amari-Chentsov term cancels between the `+` and `-` neighbours). Hence

    sum_{c'} beta_{cc'} D_KL = (1/2) h^2 sum_mu B^mu(c) h_{mu mu}(c) + O(h^4),    B^mu := beta_mu^+ + beta_mu^-,  sum_mu B^mu = 1.

Define `G^{mu nu}(c) := B^mu(c) delta^{mu nu}` in the lattice frame. Summing over `~ h^{-d}` sites with the design measure `h^d`:

    F_h^base  ->  (1/2) h^{2-d} * integral_C  G^{mu nu} h_{mu nu} d^d c   +   (row prior).

**Three structural facts fall out immediately, and they are the whole answer.**

**(a) G is trace-normalized, not scale-free.** `sum_mu G^{mu mu} = 1` pointwise, because `beta_c` is a probability row. A Polyakov `gamma^{mu nu}` ranges over the full cone of positive-definite cometrics. **A probability row cannot represent an unnormalized cometric.** The ELBO can supply the DIRECTION of G and never its SCALE.

**(b) The scale is the design.** The overall factor multiplying the invariant pairing is the design density `rho(c) d^dc` and the global `h^{2-d}`; neither is a recognition variable. This is precisely obstruction O3 (wave2-01-constructions.md:495-500: "`mu` is exogenous, on the same footing as `omega`"), unmoved.

**(c) G is diagonal in the frame the stencil declares.** Off-diagonal components of G exist only if `P` has declared diagonal neighbours. The FRAME is generative.

## 3. The freezing theorem — why the answer is (B) at unit coefficients

Exact row elimination at unit temperature (verified numerically to 4.4e-16, three trials):

    min_beta [ KL(beta||pi) + sum_b beta_b D_b ] = -log sum_b pi_b e^{-D_b} =: Phi_pi(D),     beta*_b = pi_b e^{-D_b} / Z.

Expanding for small `D`:  `Phi_pi(D) = <D>_pi - (1/2) Var_pi(D) + O(D^3)`.

With `D_b = O(h^2)`:  `beta* = pi + O(h^2)`, `KL(beta*||pi) = O(h^4)`, and the profiled value is `<D>_pi + O(h^4)`. Verified:

    h=1e-1: max|beta*-pi| = 8.0e-4 (~h^2),  KL(beta*||pi) = 3.1e-6 (~h^4)
    h=1e-2: max|beta*-pi| = 4.9e-6 (~h^2),  KL(beta*||pi) = 1.5e-10 (~h^4)
    h=1e-3: max|beta*-pi| = 3.4e-8 (~h^2),  KL(beta*||pi) = 2.8e-14 (~h^4)

So the continuum action carries `G^{mu nu} = pi^{mu nu}` — the GENERATIVE row — at leading order, with the recognition correction entering two orders down. Equivalently, off-shell: moving `beta` an `O(1)` distance from `pi` costs `O(1)` per site (`h^{-d}` total) to buy at most `O(h^2)` per site (`h^{2-d}` total); the ratio is `h^{-2} -> infinity`. **Recognition cannot afford to move the base cometric in the continuum limit.** Profiling `pi` instead is a generative-parameter optimization: it minimizes an upper bound on `-log p_theta(o)` over `theta`, i.e. variational EM / type-II maximum likelihood / empirical Bayes. That is legitimate as an algorithm and illegitimate as "the ELBO is exact".

## 4. The mixed case worked out — the one window where (A) is real

The escape is to break the `O(1)`-vs-`O(h^2)` mismatch. Replicate the transported neighbour copy `n` times per edge:

    P(j, x_1..x_n) = pi_j prod_r u_j(x_r),    Q(j, x_1..x_n) = beta_j prod_r q(x_r)
    ==>  KL(Q||P) = KL(beta||pi) + n sum_j beta_j KL(q||u_j)      [EXACT for every n]

verified by brute-force enumeration (|X|=4, m=3, n=3): 1.059356670797 vs 1.059356670797, diff 8.9e-16. `P` stays normalized, so this is still an exact-ELBO construction.

With `n_h = Theta(h^{-2})` both terms are `O(1)` per site and the row optimum reshapes G at `O(1)`. **This is the honest content of the mixed case: the SHAPE of the base cometric is recognition-side and genuinely profiled; the SCALE, SUPPORT, REFERENCE ROW, FRAME, and now the REPLICATION SCHEDULE `n_h` are generative.** And note what `n_h` does to the forced weight: `h^{d-2} = h^d * h^{-2}` splits into a Riemann-sum normalization (design) times a replication count (generative). Nothing in the ELBO chooses `n_h = h^{-2}`; it is tuned by hand to the refinement, which is exactly a generative-side model-selection act.

The corpus already flags the exact move I am making: PIFB2's scope remark on the state-level no-go (Theory/PIFB2.tex:3332) reads "**If the attention optimum `beta*(q)` has already been substituted, its response derivatives define a different reduced functional and require a separate representation test.**" The row-elimination profiling is a legitimate ELBO tightening; the object it produces is a DIFFERENT functional and does not inherit the ELBO label for free.

## 5. What the profiled object actually is — and it is not an induced volume

**(a) Constraint route.** `inf { <G,h> : G psd, tr G = 1 } = lambda_min(h)`. Verified d=3: `lambda_min = 3.001134`, value at `G = v_min v_min^T` = `3.001134`; d=4: `4.000030` vs `4.000030`. The KL potential softens `min` into `log-sum-exp`. For contrast, the UNIMODULAR constraint `det G = 1` gives `(det h)^{1/d}` by AM-GM (d=3: 6.530705; d=4: 5.915820) and `sqrt(det h)` (d=3: 16.689375; d=4: 34.996929) is neither. A probability row gives a trace constraint; only a determinant constraint could give a determinant, and no normalized row supplies one.

**(b) Homogeneity route.** Under `h -> s h` with `h = diag(1,2,4)`, uniform `pi`:

    s:        1        10       100      1000
    softmin:  0.9945   6.0919   51.0986  501.0986      (asymptotically degree 1)
    sqrt(det):2.8284   89.4427  2828.4   89442.7       (degree d/2 = 3/2)

These functions have different homogeneity degrees for every `d != 2`. No choice of `pi`, `n_h`, or lattice refinement can reconcile them.

**(c) Concavity route — the strongest.** `F(h) = inf_w { <w,h> + V(w) }` is an infimum of AFFINE functions of `h`, hence CONCAVE in `h`, for every `V` whatsoever. By Minkowski's determinant theorem (APPLICABLE_THEOREM: `det^alpha` is concave on PSD_d iff `alpha <= 1/d`; hypotheses — symmetric positive semidefinite matrices, real scalar `alpha` — hold verbatim here), `det^{1/2}` is concave iff `d <= 2`. Explicit witness along the conformal ray, `d = 3`: `f(I) = 1`, `f(4I) = 8`, chord `4.5`, midpoint `f(2.5 I) = 3.9528 < 4.5`; `d = 4`: chord `8.5`, midpoint `6.25`. (`d = 1, 2` show no violation, as required.)

> **PROPOSITION (no-go, this session).** For `dim C >= 3`, the induced-volume functional `integral sqrt(det h) d^dc` is not the profile-out of ANY auxiliary field that couples linearly to the neighbour KLs — in particular it is not obtainable from any tied-replica / label-copy / replication ELBO, with any prior, proper or improper, at any scaling.

For `d = 1, 2` concavity survives but the profile must then be positively homogeneous of degree `d/2 <= 1`; a concave positively-1-homogeneous function is a support function, so its concave conjugate `V` is a convex INDICATOR (`0` on a set, `+infinity` off it), i.e. an IMPROPER prior — `exp(-V)` has infinite mass on a cone. `d = 1` needs `V(w) = c/w`, and `integral_0^infinity e^{-c/w} dw = infinity`. Improper priors break `P`'s normalization, and normalization is the load-bearing hypothesis of the entire exact-ELBO theorem.

## 6. The Polyakov bridge fails on its own terms for d >= 3

Take `S_P[q,G] = (1/2) integral sqrt(|gamma|) (gamma^{mu nu} h_{mu nu} - (d-2)) d^dc`. Using `delta sqrt(gamma) = -(1/2) sqrt(gamma) gamma_{mu nu} delta gamma^{mu nu}`:

    delta S_P = (1/2) integral sqrt(gamma) [ h_{mu nu} - (1/2) gamma_{mu nu}(tr_gamma h - (d-2)) ] delta gamma^{mu nu}
    ==> h_{mu nu} = (1/2) gamma_{mu nu}(tr_gamma h - (d-2));  tracing:  tr_gamma h (1 - d/2) = -(d/2)(d-2)  ==>  tr_gamma h = d  (d != 2)
    ==> gamma_{mu nu} = h_{mu nu},  S_P|_on-shell = (1/2) integral sqrt(det h) (d - (d-2)) = integral sqrt(det h).

Verified symbolically in `d = 3` (all six components of `dS/dgamma^{mu nu}` vanish at `gamma^{-1} = h`) and numerically in `d = 2,3,4,5` (`S_P(gamma=h) - sqrt(det h) = 0.0e+00`). **The brief's algebra is correct.**

Now the conformal direction `gamma = t h`:

    S_P(t) = sqrt(det h) * t^{d/2-1} * (d + (2-d) t) / 2,
    dS_P/dt = -sqrt(det h) * d (d-2) t^{d/2-2} (t-1) / 4      [stationary at t = 1, all d],
    d^2 S_P/dt^2 |_{t=1} = sqrt(det h) * d (2-d) / 4.

    d=1: +sqrt(det h)/4      MINIMUM         S_P(t) -> +infinity  (einbein: genuine inf)
    d=2:  0                  degenerate      S_P(t) constant      (Weyl invariance; the inf is over the unimodular class and equals sqrt(det h))
    d=3: -3 sqrt(det h)/4    MAXIMUM         S_P -> -infinity     (numerically: 10.06 at t=1, -10.06 at t=4, -20356 at t=256)
    d=4: -2 sqrt(det h)      MAXIMUM         S_P -> -infinity     (40.9 at t=1, -2.66e6 at t=256)

> **PROPOSITION (conformal-mode obstruction).** For `dim C >= 3`, `inf_gamma S_P[q,gamma] = -infinity` and `gamma = h` is a MAXIMUM in the Weyl direction. A variational bound is by definition an INFIMUM over the auxiliary family. The Polyakov form therefore cannot be an ELBO-profiling in `d >= 3` under EITHER typing (A) or (B). This is the conformal-factor problem of Euclidean quantum gravity, imported wholesale.

## 7. The repair (item 3), and why it relocates rather than removes the problem

The repair is not new machinery — it is **PIFB2's own Theorem `thm:nested_state_configuration_vfe` (Theory/PIFB2.tex:3444-3459)** instantiated at `X := G`. Promote the base cometric to a configuration-level latent, which Theory/03_probability.tex:65 already licenses: "Later chapters may make `X` random, but only within this fixed measurable space, and **at a different probability level**. Doing so introduces a configuration prior in `P(X)` and a configuration recognition kernel ... neither is denoted by any symbol reserved above for a state-level object." Then

    J[R, Q] = T_cfg D_KL(R || P_0)  +  T_cfg integral_{Met(C)} F_state[Q_G ; G, o] R(dG),
    J[R,Q] = -T_cfg log p_theta(o) + T_cfg D_KL( R(dG) Q_G(dY) || P_theta(dG, dY | o) ),

so `-J/T_cfg` IS a genuine ELBO for one normalized hierarchical model. **THE EXTRA TERM IS EXACTLY `T_cfg D_KL(R || P_0)` — a KL between a recognition law over base cometrics and a prior over base cometrics.** Its optimum is a GIBBS LAW over base geometries, `R*(dG) ∝ P_0(dG) exp(-F_state[G]/T_cfg)`, not a delta at the profiled minimum; the delta is recovered only as `T_cfg -> 0`, and in that limit the prior term drops out and you are back to type-II ML.

Two hard constraints on `P_0`, and they are the punchline.

**(i) It must confine the conformal mode, and by §6 that is impossible for a scale-invariant prior.** `F_state[G] -> -infinity` like `-(d-2) t^{d/2} integral sqrt(det h) / 2` along `G -> tG`, so `Z = integral P_0 exp(-F_state/T_cfg) = infinity` unless `P_0` decays faster than a stretched exponential of order `t^{d/2}` — and the required rate depends on `integral sqrt(det h)[q]`, i.e. on the live section. No fixed prior works uniformly over the section class unless `integral sqrt(det h)` is bounded a priori.

**(ii) A Diff(C)-invariant proper prior does not exist.** This is E6 / PA-3 (rm-02 §3.3, finding T-3, as recorded at worklog:147) applied one level up with `G_gauge = Diff(C)`: Diff(C)-orbits in `Met(C)` are noncompact, an invariant function is constant on an orbit, so no Diff(C)-invariant function has compact sublevel sets and no invariant confining potential exists. Descending to superspace `Met(C)/Diff(C)` removes the diffeomorphism direction but NOT the Weyl fiber `G -> tG`, which is not gauge for `d != 2` and is exactly the divergent direction. The DeWitt supermetric — the standard Diff-covariant choice — is indefinite precisely in the conformal direction, so its Gaussian is not normalizable: the same obstruction, and it is a known open problem in physics, not a gap in this derivation.

**Natural priors, and what each costs.** (1) Wishart/inverse-Wishart on `G(c)` pointwise: proper and confining, but requires a reference scale matrix `Psi(c)` — i.e. **a declared base cometric**. (2) Split `G = rho^{2/d} Ghat` with `det Ghat = 1`, put Haar (SL(d)) on `Ghat` and a proper prior on `rho`: the conformal class is then genuinely free and derived, but `rho`'s prior is **a declared base density**. (3) DeWitt: Diff-covariant, not normalizable. **Every proper prior declares either a base cometric or a base density — exactly the two objects `Theory/05c_pullback_geometry.tex:1362-1366` records as NOT-CLAIMED and O3 (wave2-01:495-500) records as contradicting N1.** The repair is mathematically valid and it RELOCATES N1's problem from the action to the prior; it does not remove it. It also introduces a new free parameter `T_cfg` which is not fixed by anything.

One further corpus constraint on the repair: `F_vac` "may contain only observation-free structural energies in the declared variables `X`; it cannot contain live `q_i`, `s_i`, or their peer-KL terms" (Theory/PIFB2.tex:3471). The pairing `G^{mu nu} h_{mu nu}` DOES contain live `q` — so it must sit in `F_state[Q_G; G, o]`, not in `F_vac`. That is consistent (`F_state` is allowed to depend on `X`), but it means the base-geometry sector is a state-level energy conditioned on a configuration-level geometry, and PIFB2.tex:3503 warns that the alignment term "has two coherent placements ... Using both for the same interaction would count that edge twice."

## 8. Check against the corpus's state-level / configuration-level warnings

These are the warnings the task asked me to find, and the construction collides with three of them.

- `Theory/03_probability.tex:63` — the generative kernel reads only `theta` and `X`; "a factor that reads a posterior makes the joint a function of the object it is supposed to be conditioned into." **The Polyakov `G` is meant to be pinned by `h_{mu nu}[q]`, a functional of the LIVE recognition section. If `G` is generative, this is a flat violation. This is the single sharpest reason the answer must be (B)-with-repair rather than a naive (B).**
- `Theory/04_generative.tex:130-157` (`prop:gen-no-distinguished-target`) — if a generative factor is replaced by a `Q`-indexed family, every member still satisfies its own ELBO identity but "The family itself selects no joint as 'the model'", and a divergence decrease certifies improvement only along a level set of the evidence `e(Q)`. **Making `G` depend on `q` without the configuration-level lift lands exactly in this moving-target regime.**
- `Theory/PIFB2.tex:3281-3302` (`thm:state_level_elbo_nogo`) and `:3332` — the peer-KL sector is not a fixed state-level ELBO; the escapes explicitly named are "frozen source templates, restricted quadratic families, **compatible auxiliary variables**, a model selected after a fixed point, or a probability law over belief configurations." **`G` as a configuration-level latent is exactly the "compatible auxiliary variable" escape, so §7's repair is the corpus-sanctioned route — and it is a configuration-level route, i.e. NOT a state-level ELBO.**
- `Theory/05d_relational_inference.tex:340` — "`F` must be `C^1` on `L^2`, which excludes gradient-energy objectives", with the `S^1`, `H^1` witness at `:344-353` and the standing tier at `:355-361`. A Fisher-pullback term IS a gradient-energy objective, so the whole sector sits outside the declared standing configuration tier. This is the independent third route to A4.4 recorded at wave2-01:465-474.

## 9. What this does and does not damage

It does NOT damage: (E1) the exact finite two-channel ELBO; (E3) the base-neighbour block as an exact ELBO component at finite `h`; the escape from A4.4 at finite `h`; (E5) the idle-wheel argument for why `C` earns its manifold structure. Those stand untouched.

It DOES damage: the specific claim that `S_P` "is the `h->0` limit of the ELBO-derived lattice KL sum" while `S_vol` is its on-shell value, and the inference that "the exogenous cometric and density are auxiliary fields whose on-shell values are determined by the beliefs, and N1 survives." The density is never determined by the beliefs (§2b), the on-shell relation is a saddle not a bound for `d >= 3` (§6), and the ELBO's own profile is a soft-min, not a determinant (§5).

What is left standing, and it is not nothing: **`S_vol = integral sqrt(det h) d^dc` remains a perfectly good POSTULATED, Diff(C)-invariant action requiring no base cometric and no base density.** `sqrt(det h_{mu nu}) d^dc` is a genuine density because `h_{mu nu}` is a genuine `(0,2)`-tensor (Theory/05c_pullback_geometry.tex:109-122, gauge-covariant by `thm:pb-pullback-gauge-invariance` at 05c:124-128). It removes the `sqrt(|g|)(c) dc` of `Theory/PIFB2.tex:1731` and with it the intrinsic base metric that contradicts N1. That is a real gain — it is just an ENGINEERED action, in PIFB2's own honest register ("an engineered scalar rather than a fixed state-level generative-model ELBO", Theory/PIFB2.tex:3407), not an ELBO-derived one.

And there is a genuine, ELBO-exact alternative that nobody has written down: the soft-min functional `Phi(c) = -log sum_{c'} pi_{cc'} exp(-n_h D_KL(q(c) || Omega_# q(c')))`. It is an exact ELBO component at every finite `h`, its recognition-side profiling is legitimate, and its continuum leading form is a soft-`lambda_min` of `h_{mu nu}`. Its known defect is already in the corpus: PA-8 (rm-02 §4.1, D-5, worklog:152) — a soft-min with a diagonal entry is UNIFORMLY BOUNDED, hence gives zero coercivity. Verified here: `Phi_pi(D) <= min_b (D_b + log(1/pi_b))`, and the unnormalized Poisson-count variant profiles to `sum_mu nu_mu(1 - e^{-D_mu})`, bounded by `sum nu_mu` (verified to 1e-10). So the choice facing the PI is a strict trade: **Diff(C)-invariance and coercivity (`S_vol`, engineered) versus ELBO-exactness (`Phi`, frame-dependent and non-coercive). You cannot presently have both, and §5-§6 prove that the Polyakov construction does not bridge them.**

## obstructions

### 1

CONFORMAL-MODE OBSTRUCTION (decisive, typing-independent). For dim C >= 3, inf_gamma S_P = -infinity and gamma = h is a MAXIMUM in the Weyl direction (d^2 S_P/dt^2 |_{t=1} = sqrt(det h) d(2-d)/4 < 0). An ELBO is an infimum over the auxiliary family, so the Polyakov bridge is not a variational bound under EITHER typing. Only d = 1 (genuine minimum, einbein) and d = 2 (degenerate, Weyl-invariant) escape.

### 2

CONCAVITY OBSTRUCTION (decisive). Any auxiliary coupling linearly to the neighbour KLs profiles to a CONCAVE function of h. By Minkowski's determinant theorem det^{1/2} is concave on PSD_d iff d <= 2. Hence for d >= 3 the induced volume is not the profile of any such auxiliary, with any prior, at any scaling. Explicit witness: f(I)=1, f(4I)=8, chord 4.5, f(2.5I)=3.9528.

### 3

PROPERNESS OBSTRUCTION (decisive in the remaining dimensions). In d = 1, 2 the profile must be positively homogeneous of degree d/2 <= 1; concave positively-1-homogeneous functions are support functions, so the weight prior must be an improper convex indicator. Improper priors break the normalization of P on which the exact-ELBO theorem rests (typed-construction.md:80).

### 4

TRACE-CONSTRAINT OBSTRUCTION (structural). Normalization sum_b beta_b = 1 forces tr G = 1 pointwise. A probability row cannot encode an unnormalized cometric, so the ELBO can never supply the SCALE of the base cometric. Trace-constrained profiling gives lambda_min(h); the determinant requires a unimodular constraint det G = 1, which no normalized row supplies.

### 5

O3 SURVIVES UNTOUCHED (wave2-01-constructions.md:495-500). The base density rho(c) d^dc is the design measure. Theory/12_philosophy.tex:33-38: 'the finite design is a declared subset, not a random sample from a law on C. No expectation over contexts is used.' Nothing in the construction derives it.

### 6

FREEZING (why the answer is B). At the unit coefficients the exact-ELBO theorem delivers (exact-elbo-proof.md:136-139), beta* = pi + O(h^2) and the off-shell cost/benefit ratio for moving G is h^{-2} -> infinity. The recognition freedom over the base cometric is asymptotically frozen to the generative row unless a generative-side replication schedule n_h = Theta(h^{-2}) is declared by hand.

### 7

NO DIFF(C)-INVARIANT PROPER PRIOR (blocks the natural repair). E6/PA-3 (rm-02 §3.3, T-3; worklog:147) with G_gauge = Diff(C): orbits in Met(C) are noncompact, so no invariant function has compact sublevel sets, so no invariant confining prior and no normalizable invariant Gibbs law. Descending to superspace does not remove the Weyl fiber, which is exactly the divergent direction. Every PROPER prior declares either a base cometric or a base density -- N1's two forbidden objects.

### 8

TYPING VIOLATION IF G IS GENERATIVE AND q-DEPENDENT. Theory/03_probability.tex:63 forbids any generative factor from reading a recognition object. The Polyakov relation gamma = h[q] makes the base cometric a functional of the live section. Only the configuration-level lift (Theory/03_probability.tex:65, Theory/PIFB2.tex:3444-3459) resolves this, and it is explicitly a DIFFERENT probability level.

### 9

OPEN, INHERITED. The covariant O(h^3) stencil cancellation with Omega_{c,c+h} != Omega_{c,c-h} is unproved (worklog:102-106); every h-order statement here inherits the flat-transport caveat. Also unaddressed: h_{mu nu} degeneracy on the rank-drop locus (05c:325-341, 05c:429-432), where the Polyakov variation is ill-posed outright.


## novelty

NOVEL to the corpus, with prior art on the surrounding pieces.

ABSENT from Theory/ and docs/: grepped Theory/*.tex and the whole docs/ tree for `Polyakov`, `Nambu`, `induced volume`, `induced-volume`, `auxiliary cometric`, `einbein`, `empirical Bayes`, `type-II`, `evidence maximi` -- ZERO substantive hits. The single hit, Theory/05c_pullback_geometry.tex:425 ("independent of the selected auxiliary metric connection"), is about a fiber-side metric connection in a Lie-derivative argument and is unrelated. The induced-volume proposal itself exists only as the worklog's own §3c.6 (worklog:322-344), tagged "Status: CONJECTURE / direction, not a result", with the self-caveat at worklog:340: "No ELBO derivation of S_vol is claimed or currently in sight." This session upgrades that caveat from "not in sight" to "provably impossible in the linear-coupling class" (§5c, §6).

PRIOR ART THAT THIS BUILDS ON, cited not re-derived:
- The typing rules: Theory/03_probability.tex:51 (edge set inside X), :63 (generative kernel reads only theta, X), :65 (configuration level is a different probability level).
- hyp:gen-design-product: Theory/04_generative.tex:89-96, status HYPOTHESIS.
- The moving-target proposition: Theory/04_generative.tex:130-157.
- The pullback h_s^omega = sigma* g^F: Theory/05c_pullback_geometry.tex:109-122; gauge covariance :124-128; radical/rank quotient :325-341; constant-rank-one witness :429-432; the NOT-CLAIMED boundary ("a base cometric, a base density, channel weights, boundary conditions...") :1362-1366.
- Gradient-energy exclusion from the standing tier: Theory/05d_relational_inference.tex:340, :344-353, :355-361.
- Idle-wheel criterion and the no-law-on-C disclaimer: Theory/12_philosophy.tex:33-38, :77-78.
- The sqrt(|g|)(c) dc incompatibility: Theory/PIFB2.tex:1731 (read and confirmed verbatim).
- The state-level no-go and its scope, which is the warning the task asked me to find: Theory/PIFB2.tex:3281-3302, :3330-3332 ("compatible auxiliary variables" as a named escape; "If the attention optimum beta*(q) has already been substituted ... require a separate representation test"), :3407, :3418, :3422, :3471, :3503, :3516.
- The repair mechanism is PIFB2's OWN theorem: Theory/PIFB2.tex:3444-3459 (thm:nested_state_configuration_vfe). Instantiating it at X := G is the new step; the theorem is not new.
- A4.4 / A4.5 / O2 / O3: docs/audits/ultradeep-wave2-2026-08-12/wave2-01-constructions.md:385-404, :406-413, :488-493, :495-500, :465-474.
- Soft-min boundedness (PA-8, rm-02 §4.1 D-5) and the invariance-vs-coercivity lemma (PA-3, rm-02 §3.3 T-3): recorded at worklog:152 and worklog:147. I APPLY PA-3 at a new level (Diff(C) acting on Met(C)) rather than restating it.
- Minkowski's determinant theorem is classical, not new.
- The conformal-factor problem of Euclidean quantum gravity is classical; identifying it as what the induced-volume horn imports is, so far as the corpus shows, new here.

NEW IN THIS RUN: (1) the four-way ingredient typing of the base cometric with citations on both sides; (2) the freezing theorem beta* = pi + O(h^2) and the h^{-2} cost/benefit ratio; (3) the exact n-copy replication identity KL(Q||P) = KL(beta||pi) + n sum beta KL(q||u) and the factorization h^{d-2} = h^d * h^{-2} into a design piece and a generative-replication piece; (4) the three independent proofs that the ELBO profile is a soft-lambda_min and not sqrt(det h); (5) the conformal-mode obstruction to the Polyakov bridge for d >= 3; (6) the identification of KL(beta||pi) as the already-present prior-over-base-geometries term.

## verdict_for_commit

DO NOT COMMIT to the induced-volume horn AS AN ELBO STATEMENT. Commit to it, if at all, as a POSTULATED action, and say so in the same sentence.

Blunt version. The proposal in the brief has two halves and both fail, for different and independent reasons.

Half one: "gamma is an auxiliary field whose on-shell value is determined by the beliefs, so N1 survives." FALSE as stated. Only the SHAPE of gamma is belief-determined, and even that only under a hand-tuned generative replication schedule n_h = Theta(h^{-2}); at the unit coefficients the exact-ELBO theorem actually delivers, the shape is frozen to the generative row pi with O(h^2) deviation. The SCALE, the SUPPORT, the FRAME, and the REFERENCE ROW are generative/design data throughout, and the scale cannot ever be recognition-side because a probability row is trace-normalized. You would not be removing the exogenous cometric and density; you would be renaming them pi and rho and putting them in a different chapter. Obstruction O3 (wave2-01:495-500) is untouched.

Half two: "S_P on-shell = S_vol, and S_P is the h->0 limit of the ELBO-derived lattice KL sum." The first clause is arithmetically true and I verified it. The second is false, and the two clauses are incompatible anyway. For dim C >= 3 the gamma-stationary point is a MAXIMUM in the Weyl direction and inf_gamma S_P = -infinity; an ELBO is an infimum, so this is not a bound-tightening operation in any dimension above 2. Independently, any auxiliary coupling linearly to the neighbour KLs profiles to a CONCAVE function of h, and det^{1/2} is not concave for d >= 3 (Minkowski). Independently again, what the ELBO's own gamma-elimination returns is the soft-min -log sum pi e^{-D}, a soft-smallest-eigenvalue of h, not its determinant -- different constraint set (trace, not unimodular), different homogeneity degree (1, not d/2). Three independent proofs, all pointing the same way.

If a reviewer who knows string theory reads "vary gamma, get Nambu-Goto, therefore it is an ELBO", they will ask in one line why the conformal mode does not blow the infimum to minus infinity, and there is no answer. That question would be asked in public.

WHAT TO COMMIT TO INSTEAD. Two options, both honest, and the corpus already has the vocabulary for both.

(1) Keep S_vol as an ENGINEERED Diff(C)-invariant action. This is a real gain: it deletes the sqrt(|g|)(c) dc of PIFB2.tex:1731 and with it the intrinsic base metric that contradicts N1, and sqrt(det h_{mu nu}) d^dc is a genuine invariant density because h is a genuine tensor (05c:109-128). Say plainly that it is engineered, in exactly PIFB2's own register at PIFB2.tex:3407 ("an engineered scalar rather than a fixed state-level generative-model ELBO"). Claim Diff(C)-invariance and N1-compatibility. Claim NO ELBO derivation. Note also the untreated degeneracy on the rank-drop locus (05c:325-341, 05c:429-432).

(2) Take the configuration-level lift, which is the only genuinely variational route and is PIFB2's OWN theorem (thm:nested_state_configuration_vfe, PIFB2.tex:3444-3459) instantiated at X := G. The extra term is exactly T_cfg D_KL(R || P_0), a KL from a recognition law over base cometrics to a prior over base cometrics. This is legitimate. But be honest about the bill: (a) it lives at a different probability level, so it is not a state-level ELBO and PIFB2.tex:3332 already says so; (b) it introduces a free T_cfg; (c) by E6/PA-3 applied to Diff(C) there is NO proper Diff(C)-invariant prior, and every proper prior declares either a reference cometric or a base density -- so N1's problem is relocated to the prior, not removed; (d) for d >= 3 the configuration Gibbs law is not even normalizable, because F_state -> -infinity along the conformal ray, so the repair does not rescue the induced-volume form specifically.

THE HEADLINES THE PI ASKED FOR.

Case (A), the defensible recognition-side claim, one sentence: "At every finite design the anisotropy of the emergent base cometric is a recognition variable, and eliminating it is an exact ELBO tightening whose value is the soft-min free energy -log sum_{c'} pi_{cc'} exp(-D_KL(q(c) || Omega_# q(c'))); in this sense the base CONFORMAL structure -- not the base geometry -- is the evidence-optimal one, and the continuum object it converges to is a smallest-eigenvalue functional of the informational pullback, not its induced volume."

Case (B), the true statement about the load-bearing part, one sentence: "The scale, support, reference row, and frame of the base cometric are generative and design data, so selecting them by minimizing the free energy is variational EM / type-II maximum likelihood, and the honest claim is 'the cross-context coupling structure that maximizes the evidence induces a base geometry' -- an empirical-Bayes model-selection statement, for which the words 'exact ELBO' must not be used."

ONE MORE THING, DO IT BEFORE ANYTHING IS DRAFTED: the symbol gamma is already the MODEL-channel recognition row in the closed theorem (typed-construction.md:100-105, exact-elbo-proof.md:91-94). Using it for the base cometric in this exact sector will cause a real error, not a cosmetic one. Rename to g^{mu nu} or lambda_{mu nu} now.
