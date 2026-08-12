# Audit 01 — Geometry and gauge structure (adversarial)

Date: 2026-08-11
Scope: `MultiAgentELBO/Theory/{02_geometry, 05c_pullback_geometry, 11_obstructions, appendix_notation, 07b, 08}.tex`,
`MultiAgentELBO/src/multiagent_elbo/geometry/*.py`, `realizations/gaussian/gauge.py`,
`Research/manuscripts/PIFB2.tex` (One Rung + Part II signature/pullback).
Prior audit read and not re-reported: `docs/audits/2026-08-11-post-fixed-ray-deep-audit.md` (code-centric; near-zero overlap with this scope).

## Executive summary

Chapter 02 and Chapter 05c are, on the mathematics I checked line by line, correct. I re-derived
eleven identities across 02, 05c, 08 and 11 and found no algebraic error. The passive/active and
`G x G`/`G` distinctions are honored everywhere I looked, and Chapter 02 repairs PIFB2's real
category error (transition function used as inter-agent transport). The defects are structural, not
computational. First: no curvature 2-form is defined anywhere in the corpus, and the principal
connections never appear in the generative or ELBO chapters, so the gauge sector is inert and the
central object `h_s^omega` depends exactly on data no principle selects. Second, and measurably: the
genuinely bundle-theoretic content of Chapter 02 — the Cech class, the associated-bundle parallel
transports, the covariant defects, the graph-to-base transport bridge — has zero downstream
references. Third, three existence questions are assumed rather than hypothesized: local frames over
agent supports, manifold structure of the law fibers, and global sections. Fourth, Chapter 02 has 17
untagged prose blocks carrying load-bearing claims, a direct SPEC 2.1 violation. Fifth, the geometry
code implements none of Chapter 02 or 05c and is hard-coded to `GL+(2,R)`.

## Findings

### G1 — The gauge sector is never dynamical: no curvature anywhere, and the connections never enter the free energy
**Severity: HIGH. Type: (b) missing derivation, partly self-declared as (e) scope.**

Location / evidence:
- `grep -c -i curvature Theory/*.tex` yields exactly one hit in `Theory/02_geometry.tex:397`, and it is a
  disclaimer: *"The connections in \eqref{eq:geo-principal-connections} are chosen data; no curvature
  or transport is inferred from the agent frames. \status{NOT-CLAIMED}"*.
- No occurrence anywhere in `Theory/*.tex` of `d\omega`, `[\omega,\omega]`, `F_\omega`, "structure
  equation", or "Ambrose". `appendix_notation.tex` has entries for `\omega_b,\omega_m`,
  `\Omega_\gamma`, `D^\omega s`, `h_s^\omega` (lines 66-93) and **no curvature entry**.
- `grep -c "omega_b\|omega_m" Theory/*.tex` returns hits only in `02, 05c, 05d, 07b, 12,
  appendix_notation`. It returns **zero** in `04_generative.tex`, `05_elbo.tex`,
  `05b_local_collective_elbo.tex`. The variational free energy is functionally independent of
  `omega_b, omega_m`.
- `Theory/05c_pullback_geometry.tex:184-232` (`prop:pb-pullback-connection-change`) proves that
  `h_s^omega` changes exactly under a change of connection, and gives the counterexample
  (`eq:pb-connection-dependence-example`, 05c:220-232): the same section over `C = R` gives `h = 0`
  for the zero connection and `h = a_0^2 dx^2` for `A' = a_0 dx`.
- `Theory/05c_pullback_geometry.tex:1362-1367` concedes the point: *"A scalar gauged sigma energy
  would additionally require ... a decision about whether the connection is fixed or dynamical. None
  is selected by `h_s^omega` or `c_s^omega`. \status{NOT-CLAIMED}"*.

Why this matters: the development has connections, horizontal distributions, and parallel transports
but no field strength, no Ambrose-Singer, and no equation of motion for `omega`. Combined with the
exact connection dependence, the pullback metric — the object the project goal treats as the
emergent geometry — is not an observable of the variational theory. It is a function of an exogenous
choice. This is the one place where the rigorous development is *weaker* than PIFB2, which at least
states `F = 0` in Regime I by Maurer-Cartan and `F != 0` in Regime II (`PIFB2.tex:142`, `:353`).

Fix: (a) add a curvature section to Chapter 02 — define `F^omega = d\omega + (1/2)[\omega,\omega]`,
prove the associated-bundle holonomy consequence, and prove `F = 0 <=> transport is path-independent
on simply connected opens`; this also makes rigorous the exact statement PIFB2 relies on. (b) Then
either add a connection-dependent term to the VFE (Yang-Mills on `omega`, or a sigma-model term
`|D^omega s|^2` integrated against a declared base cometric and density) and derive the
`omega`-variation, or promote "the connection is exogenous, hence `h_s^omega` is not an observable"
from a chapter-boundary remark to a headline scope statement in `01_introduction.tex` and a named
`OPEN` entry in `appendix_claim_ledger.tex`.

### G2 — Chapter 02's genuinely bundle-theoretic content has zero downstream use
**Severity: HIGH. Type: (d) vacuous-or-trivial (structure present but inert).**

Location / evidence — reference counts across all of `Theory/*.tex`:

| label | total refs | refs outside `02_geometry.tex` |
|---|---|---|
| `eq:geo-cech-class` (the single-Cech-class statement) | 1 | 0 |
| `sec:geo-cech` (whole Cech / topology section) | 1 | 0 |
| `eq:geo-base-parallel-transports` (`Omega_gamma`, `\widetilde Omega_gamma`) | 2 | 0 |
| `def:geo-connections` | 1 | 0 |
| `hyp:geo-graph-base-transport` (the only graph-link -> base-connection bridge) | 1 | 0 |
| `def:geo-covariant-defects` | 1 | 0 |
| `prop:geo-trivializing-criterion` | 1 | 0 |
| `def:geo-agent` | 1 | 0 |
| `prop:geo-moment-pushforward` | 1 | 0 |

Cross-file use of Chapter 02 is confined to `hyp:geo-smooth-tier`, `eq:geo-quotient-convention`,
`eq:geo-local-reframing`, `eq:geo-local-connection-b/-m`, `eq:geo-relative-frame`,
`eq:geo-diagonal-gauge-functions`, `eq:geo-tildephi-gauge-law`, `eq:geo-regime-two-gauge-law`,
`def:geo-graph-links`, `sec:geo-cross-morphisms`, `sec:geo-diagonal`,
`hyp:geo-common-trivializations` — i.e. to the *coordinate-transformation bookkeeping* and the
*graph links*, never to the bundle topology or the base transport.

Consequences, both material:
1. Because `hyp:geo-graph-base-transport` (02:625-640) is never invoked, every holonomy result in
   the corpus (`06_gaussian`, `09_coarsegraining` 32 hits, `11_obstructions` 20 hits, `07b` 8 hits)
   is finite-graph algebra over independently declared `Theta_e`, with no principal-bundle content
   whatsoever. The chapters say so honestly (11:422, 12:111, 12:326), so this is not an overclaim —
   but it means "gauge theory" in the corpus reduces to lattice link algebra plus passive relabeling.
2. `eq:geo-cech-class` (`[T^b] = [T^m] = [P|_{C_0}]`) is the entire topological payload of the "one
   common principal bundle" architecture that SPEC 0 declares to be the ambient theory. It is proved
   and then never used. Nothing downstream would change if the two channels had independent bundles
   plus a declared relative field.

Fix: either exhibit at least one downstream theorem that consumes `[T^b] = [T^m]` or `Omega_gamma`
(the natural candidate: a global consensus frame exists iff the class is trivial, or an obstruction
to a globally flat comparison across the agent cover), or move `sec:geo-cech` and
`sec:geo-three-transports` behind an explicit "available but presently unconsumed" heading and say so
in `01_introduction.tex`, so a reader is not led to believe the topology is doing work.

### G3 — Existence of the local frames `u_i^b, u_i^m : C_i -> P` is assumed, not hypothesized
**Severity: MEDIUM. Type: (b) missing hypothesis.**

Location: `Theory/02_geometry.tex:46-53` — *"For each agent `i`, choose an open support
`C_i \subseteq C` and two local principal-frame sections `u_i^b, u_i^m : C_i -> P`."*

A section over `C_i` exists if and only if `P|_{C_i}` is trivializable. That is guaranteed only after
shrinking to a trivializing neighborhood; it is not a property of an arbitrary open subset, and the
definition's syntax admits `C_i = C`. Counterexample within the definition as written: `C = S^2`,
`P` the Hopf `U(1)`-bundle, one agent with `C_1 = C`. No `u_1^b` exists, yet
`def:geo-principal-systems` instructs the reader to choose one. A proper-open counterexample:
`C = S^2 x R`, `C_i = S^2 x (0,1)`, `P` the pullback of Hopf.

The omission has modeling content, not just pedantic content: the *same* `C_i` is both the agent's
belief/model support (`eq:geo-agent-sections`, 02:410-415) and the frame domain. Requiring the frame
therefore constrains how large an agent's domain may be, and forces the agent supports to be a
trivializing cover. Nothing in the corpus records that coupling.

Fix: add to `def:geo-principal-systems` the clause "`C_i` is chosen so that `P|_{C_i}` is
trivializable, which is always achievable after shrinking by local triviality", tag it `HYPOTHESIS`,
and add one sentence noting that the agent population's supports therefore form a trivializing cover.

### G4 — Section existence is never settled, and in the declared Gaussian realization the answer deflates the hedging
**Severity: MEDIUM. Type: (b) missing derivation.**

Evidence: `grep -i "characteristic class\|chern\|stiefel\|euler class\|obstruction cocycle\|classifying
space\|contractible\|partition of unity\|paracompact" Theory/*.tex` returns **nothing**.
`11_obstructions.tex` is not about bundle obstructions at all — it is about the singularity of the
flat unanchored reciprocal Gaussian pair (11:20-135, `cor:obs-flat-fold-singular`). It says so
clearly, but a reader arriving from the project goal ("agents are LOCAL SECTIONS ... obstruction
theory") will look there and find nothing. `02_geometry.tex:552-555` supplies only a *sufficient*
condition (a `G`-fixed point in the fiber gives a global section).

The missing result is short and it changes the reading of the whole "local sections" hedge. In the
declared Gaussian realization the belief fiber is `B_b = {N(mu,Sigma)} ~ R^K x SPD(K)`, which is
contractible. A fiber bundle with contractible fiber over a paracompact base admits a global smooth
section. Equivalently, `E_b ~ V (+) Met(V)` for the associated vector bundle `V = P x_{rho_b} R^K`,
and a global section is a pair (vector field on `V`, Riemannian metric on `V`), both produced by a
partition of unity. So: **global agents always exist in the Gaussian realization, whatever the
topology of `P`.** Topology can obstruct a global *frame*; it never obstructs a global *agent*.

Fix: add this as a two-paragraph `ESTABLISHED` proposition to Chapter 02 or Chapter 06. It costs
nothing, it is correct, and it correctly tells the reader where the topology bites and where it does
not. If the intent is instead to keep an obstruction story alive, state the general obstruction
(`H^{k+1}(C; pi_k(B_x))`) and give a fiber for which it is nonzero.

### G5 — SPEC 2.1 violation: 17 untagged prose blocks in `02_geometry.tex`, several load-bearing
**Severity: MEDIUM. Type: (c) weak rigor / SPEC violation.**

`SPEC.md` 2.1: *"A claim with no status is a defect."* `02_geometry.tex` carries 38 `\status{}` tags
and 17 substantial (>150 char) prose blocks with none. The worst four:

1. **`02:135-137`** — *"At the general tier these are associated measurable bundles. Under
   \Cref{hyp:geo-smooth-tier} they are smooth associated bundles."* This is the smooth-structure
   claim on which all of Chapter 05c rests. Untagged and unproved. (It is true: `G` acts freely and
   properly on `P x B_x` because it does so on `P`, so the quotient is a smooth fiber bundle — but
   that is exactly the sentence that is missing.)
2. **`02:301-306`** — the *construction* of the associated-bundle parallel transports `Omega_gamma`
   via horizontal lifts. Untagged, and with no verification that the result is independent of the
   chosen point of `P_{gamma(0)}`. It is, by equivariance of the lift and the quotient convention,
   but that one line is absent while the analogous one-liners are supplied elsewhere.
3. **`02:308-312`** — *"Their difference `omega_m - omega_b` is horizontal and Ad-equivariant, hence
   descends to an Ad(P)-valued one-form on `C`."* Untagged, and load-bearing: `05c:158-166`
   (`eq:pb-connection-difference`) consumes it directly.
4. **`02:168-181`** — the derivation of `eq:geo-diagonal-gauge-functions` (`k_i^m = h_i^{-1} k_i^b
   h_i`). This is a genuine `ESTABLISHED` result with an argument, presented as commentary with no
   tag, and it is cited from `04_generative.tex:365-370`.

Fix: tag all 17; supply the two missing one-line verifications in items 1 and 2.

### G6 — `src/.../geometry/` implements neither Chapter 02 nor Chapter 05c, and its gauge structure is hard-coded to `GL+(2,R)`
**Severity: MEDIUM. Type: (a)+(e) code-theory mismatch / scope.**

Locations:
- `geometry/discrete_holonomy.py:149-156` — `_gl_positive_2` rejects anything but a finite `2x2`
  positive-determinant matrix. `np.eye(2)` at `:333`, `:481`, `:567`; two-vector states at `:264`,
  `:620`, `:656`; `2x2` frames at `:585`; `(M,2)` covectors at `:637`. There is no dimension
  parameter anywhere in the module. So the implemented structure group is `GL+(2,R)` in its defining
  representation, one channel only — no `rho_b` vs `rho_m`, no relative frame `h_i`, no base
  manifold.
- No module anywhere in `src/multiagent_elbo/` implements `C`, `P`, `omega`, an associated bundle, a
  section, `D^omega s`, or `h_s^omega`. Grepping for `principal|connection|associated_bundle`
  returns only docstring *disclaimers* (`discrete_holonomy.py:3-8`,
  `holonomy_experiment.py:3-6`, `:490`, `:565`).
- `geometry/finite_gauge.py` is finite permutation relabeling metamorphics, correctly disclaimed at
  `:92-93` (*"not an API for arbitrary gauge fields, connections, or holonomy"*) but placed in
  `geometry/` under a "gauge" name.

Note this is *not* a SPEC violation: `SPEC.md` 0 explicitly forbids the Theory document from citing
the executable. It is a project risk: the two most mathematically load-bearing chapters have no
computational witness at all, while the audited geometry code is a `K = 2` lattice-gauge toy.

Related but distinct from prior finding **AUD-06**: that finding concerned an unvalidated
`matrix_dimension` reaching a hard-coded 2x2 fixed-ray system. Here the module has *no* dimension
concept at all, so no mislabeling is possible — but the same "2 is the only supported dimension"
pattern recurs in a second package and is still unfixed as a class.

One consistency note in the code's favor and one tension: the nontrivial holonomy exercised at
`holonomy_experiment.py:141` (`e30 = diag(2,1)`, giving cycle holonomy `[[2,2],[0,1]] != I`) comes
from an *independently declared* link, i.e. Chapter 02's Regime II (`sec:geo-regime-two`), not from a
coboundary. That is exactly right relative to Theory. It is, however, the opposite of PIFB2's
implemented core, which is Regime I with `Omega_ij = U_i U_j^{-1}` and hence identically trivial
holonomy (`PIFB2.tex:142`, `:336`, `:449`).

Fix: give `discrete_holonomy.py` a declared `K` with a `GL+(K)` validator and a fail-before-write
dimension check; and either add one minimal numerical witness of Chapter 05c (trivial `P` over
`C = R^n`, a chosen `gl(K)`-valued `A`, a Gaussian section, compute `D^omega s` and `h_s^omega`,
verify `rad h = ker D^omega s` and the connection-change formula), or state in the repo README that
Chapters 02 and 05c are unimplemented by design.

### G7 — `B_x ⊆ P(K)` is treated as a manifold; the identifiability that makes it one is never assumed
**Severity: MEDIUM. Type: (b) missing hypothesis / type conflation.**

Locations: `02_geometry.tex:69-74` declares `B_b ⊆ P(K)` as a **subset** of the space of probability
measures. `02_geometry.tex:104-105` then calls it *"a finite-dimensional smooth parametrized-measure
model"*. `05c_pullback_geometry.tex:52-57` writes `T_p B_x` and `g^F_{x,p}(u,v) = E_p[l_u l_v]` on it.

A parametrized measure model in the sense of Ay-Jost-Le-Schwachhofer is a *map* `theta -> p_theta`
from a parameter manifold; its **image** is a manifold only if the map is injective and an immersion
onto its image. Non-identifiable families have non-manifold or non-Hausdorff images and a degenerate
Fisher form. `hyp:pb-regular-models` (05c:30-46) assumes *"a positive-definite Fisher form"*, which
delivers local identifiability, but that is asserted of the model, not of the subset, and global
injectivity is never assumed anywhere.

This is an inconsistency of care rather than of belief: the corpus is careful about identifiability
elsewhere (`03_probability.tex:396-437`, `09_coarsegraining.tex:1041`).

Fix: declare `B_x` as the image of an injective immersion with the induced smooth structure and say
so once, or carry the parameter manifold explicitly and form `E_x = P x_{rho_x} Theta_x` with the
action lifted to parameters — the latter is what the equivariance argument in
`prop:pb-statistical-tensor-descent` effectively uses anyway.

### G8 — The based holonomy map `H_I^x : pi_1(Gamma_I, r_I) -> G` is asserted without a homomorphism convention or a well-definedness proof
**Severity: LOW-MEDIUM. Type: (c) weak rigor.**

Location: `Theory/07b_agent_network_rg.tex:1648-1653`, `eq:rg-full-holonomy-representation`, inside a
block tagged `\status{ESTABLISHED}` at `07b:1674`. The label calls it a *representation*.

Two things are owed. (i) Descent to `pi_1`: homotopy classes of loops in a graph are reduced words,
so descent requires `Theta^x_{\bar e} = (Theta^x_e)^{-1}` (declared at `02:566-569`) to cancel
backtracking. Two lines, never written. (ii) With Chapter 02's ordering convention
(`eq:geo-link-holonomy`, 02:589-593: edges `e_a : i_{a+1} -> i_a`, product taken left to right),
concatenation of loops reverses the matrix order, so the natural map is an **anti**-homomorphism
`pi_1 -> G` unless `pi_1` is given the opposite product. Calling it a representation without
resolving this is a real, if small, defect at this document's stated rigor bar.

Fix: state the convention explicitly, add the two-line descent proof, and say whether it is a
homomorphism into `G` or into `G^op`.

### G9 — `gaussian/gauge.py` admits frames from a bounded-condition-number subset of `GL+(K)`, which is not a subgroup
**Severity: LOW. Type: (c) weak rigor.**

Location: `src/multiagent_elbo/realizations/gaussian/gauge.py:36-52` — `_validate_frames` rejects any
block with `cond(block) > numerics.max_frame_condition` (and requires `det > 0`). The admitted set
`{U in GL+(K) : cond(U) <= kappa}` is not closed under multiplication: `cond(UV) <= cond(U)cond(V)`
is the only general bound, and two admitted frames can compose out of the domain.

No current result is broken, because every check in the module is pointwise. But any statement of the
form "covariance under the gauge group" evaluated on this set is covariance under a generating set,
not under a group, and a future test that composes two admitted frames will silently leave the
declared domain.

Fix: docstring note that this is a numerical admissibility domain and explicitly not a subgroup;
revalidate after any composition.

### G10 — PIFB2 `prop:4d_signature`: correct but coordinate-trivial, and the `K_q >= 6` bound contradicts the "disjoint-support" descriptor
**Severity: LOW. Type: (d) vacuous-or-trivial + one concrete numeric inconsistency.**

Locations: `Research/manuscripts/PIFB2.tex:1968-1969` (proposition), `:1928` (Postulate traceorth),
`:1960` (the 2D concession), `:63` (abstract).

(i) I verified the computation. With `phi = psi_tau S + sum_a psi_a T_a` in an abelian subalgebra and
`A_mu = d_mu phi`, cross terms vanish (`tr(ST) = 0` for skew `S` and symmetric `T`;
`tr(T_a T_b) = 0`), so
`G_{mu nu} = tr(S^2) d_mu psi_tau d_nu psi_tau + sum_a tr(T_a^2) d_mu psi_a d_nu psi_a`, which has
signature `(-,+,+,+)` where the four differentials are independent. Correct. But this is exactly the
flat Minkowski metric written in the coordinates `(psi_tau, psi_x, psi_y, psi_z)` up to constant
rescalings — the gauge apparatus supplies only the constants `tr(T_a^2)`. The manuscript concedes
precisely this for the 2D case at `:1960` (*"a form obtainable on any manifold with no gauge
theory"*) and calls the 4D case *"coordinate-flat"* at `:63`, so this is disclosed rather than
hidden. Recording it here because the rigorous Theory should not import it as-is.

(ii) Concrete inconsistency: `:1928` states that `prop:4d_signature` is *"the commuting
disjoint-support realization"*. Three traceless diagonal generators with **pairwise disjoint
supports** need at least 6 coordinates beyond the 2 consumed by `S`, i.e. `K_q >= 8`. The stated
bound `K_q >= 6` is sufficient only under mere trace-orthogonality on 4 *shared* coordinates
(the traceless diagonal matrices on 4 coordinates form a 3-dimensional space admitting an orthogonal
basis). One of the two statements is wrong.

Fix: change the bound to `K_q >= 8`, or drop "disjoint-support" from Postulate traceorth and say
"mutually trace-orthogonal on a shared 4-coordinate block".

## What is actually solid

Reported so the synthesis does not spend effort re-attacking these.

1. **Passive vs active gauge, and `G x G` vs `G`.** Kept straight at every site I checked:
   `01:47-49`, `02:168-181`, `02:578-585`, `04:359-372`, `06_general_coarsegraining:492-497`,
   `06a:167-171`, `07b:1644-1646`, `appendix_claim_ledger:31-36`. I found no slip. The ledger's
   "Regular frame-coordinate quotient (open)" entry is honored everywhere.
2. **PIFB2's transport/transition-function conflation is fixed by Chapter 02.** `PIFB2.tex:208`
   calls `Omega_ij = U_i U_j^{-1}` a Cech transition function and then, in the same paragraph,
   an inter-agent transport with `KL(q_i || Omega_ij q_j) > 0` generically. Those are incompatible:
   a transition function relates two representatives of *one* section, forcing the KL to vanish.
   Chapter 02 resolves this by typing `T_ij` (pointwise Cech comparison, `02:448-483`) apart from
   `Theta_e` (independently declared graph links, `02:557-622`), exactly as `SPEC.md` 3 requires.
   This is the most valuable repair the rewrite has achieved so far and should be protected.
3. **Q3 (a pure-gauge transport has identically zero holonomy) is handled, not contradicted.**
   `02:646-658` (`hyp:geo-flat-links`) sets `Theta_e = U_i U_j^{-1}` and states that this *"excludes
   represented graph holonomy in either channel"*; `06_gaussian:156` repeats it; `11:422` and
   `12:111`, `12:326` disclaim base-curvature readings; `PIFB2:142` declares Regime I flat by
   Maurer-Cartan. I searched for a place claiming nonzero holonomy from a coboundary form and found
   none.
4. **Descent of the Fisher and Amari-Chentsov tensors to the associated bundle is proved, not
   assumed** (`05c:59-88`, `prop:pb-statistical-tensor-descent`), with the load-bearing hypothesis
   (`rho_x(g)` induced by a *parameter-independent bimeasurable* sample-coordinate change) isolated
   at `05c:39-41` and flagged as load-bearing at `05c:84-87`. The `GL(K)` isometry fact for the MVN
   Fisher-Rao metric is separately sourced at `08:97`, with a correction to a typo in the cited
   survey. This is the hard part of Q2 and it is done correctly.
5. **Rank / degeneracy of the pullback (Q7) is fully handled.** `05c:321-350` proves
   `rad h_s^omega = ker D^omega s` and gives the constant-rank quotient; `05c:380-386` adds the
   involutivity requirement for a quotient manifold; `05c:397-404` adds the separate basicness
   requirement with a connection-independent criterion; `05c:429-452` gives a constant-rank
   **nonintegrable** counterexample (the contact form `dz - x dy`); `05c:455-465` gives a rank-jump
   counterexample. The Lorentzian reading is explicitly declined at `12:46-49` (`NOT-CLAIMED`),
   which is the correct call given that a Fisher pullback is PSD by construction.
6. **Connection dependence is proved exactly with a counterexample rather than hand-waved**
   (`05c:184-232`), and the active-vs-passive distinction for the pullback carries its own explicit
   counterexample at `05c:144-152`.
7. **Identities I re-derived and confirmed correct**: `eq:geo-relative-frame-law`,
   `eq:geo-diagonal-gauge-functions`, `eq:geo-cross-map-gluing`, `eq:geo-map-bundle-frame-conversion`
   (including the `f_i = phi` consistency check), `eq:geo-cech-cocycle`; the horizontal-lift sign
   convention `(X, -zeta_{A(X)} beta)` and `eq:pb-jet-connection-change` in 05c; `eq:obs-holonomy-det`
   in 11 (`det J = det(I-H)^2 / (det R_e det R_f)`, verified for general `K` via `J = M^T M` and a
   Schur complement, not just the `K = 1` witness the text gives); `prop:ig-generalized-spectrum-
   invariance` and `prop:ig-frame-dependent-spectra-determinants(ii)` in 08. No errors.
8. **PIFB2's `+1/4` sectional curvature claim (`PIFB2:429`) checks out.** At `Sigma = I` the second
   fundamental form of the mean slice is `II(d_a, d_a) = E_aa` and `II(d_a, d_b) = (E_ab + E_ba)/2`;
   the Gauss equation gives `K = 0 - 0 + 1/4`. The mixed-sign claim for the MVN Fisher-Rao manifold
   is correct.
9. **PIFB2 does not hide the triviality of its bundle.** `PIFB2:208` states outright that its Cech
   data is the coboundary of `{U_i}`, that the reconstructed bundle is canonically trivializable, and
   that *"the bundle language is organizational rather than a source of topological generality"*.
   The Q1 suspicion is confirmed for PIFB2 and is openly declared there. Chapter 02 goes strictly
   beyond it by retaining nontrivial classes — but see G2 for why that generality is currently inert.
10. **`discrete_holonomy.py` matches Theory 02's transformation laws exactly**:
    `passive_transform_links` (`:590-605`) implements `Theta' = A_target^{-1} Theta A_source`, matching
    `eq:geo-regime-two-gauge-law`; `passive_transform_states` (`:608-623`) gives `z' = A^{-1} z`;
    `passive_transform_covectors` (`:626-641`) gives `c' = A^T c`, so `c^T z` is exactly invariant.
    The `broken` scenario in `holonomy_experiment.py:207-211` (one link left untransformed) is a
    genuine negative control, not a tautology. The module docstrings correctly refuse to identify
    graph links with base connections.

## Highest-value next steps

1. **Decide the status of `omega` and say it once, prominently.** If exogenous: add an `OPEN` ledger
   entry "no principle in this development selects the principal connections; `h_s^omega` is
   therefore connection-relative and not an observable", and echo it in `01_introduction.tex`. If it
   is meant to become dynamical, that is the theory's largest missing chapter. (G1)
2. **Write the curvature section for Chapter 02**: `F^omega = d\omega + (1/2)[\omega,\omega]`, its
   Ad-equivariance, the induced curvature on the associated bundles, Ambrose-Singer, and
   `F = 0 <=> local path-independence`. This is short, standard, `ESTABLISHED`, and it is the one
   structure PIFB2 has that the rigorous rewrite currently lacks. (G1)
3. **Add the three short existence statements**: local frame trivializability as a stated hypothesis
   (G3); global Gaussian section existence via contractible fiber (G4); manifold structure of `B_x`
   via injective immersion (G7). Each is one proposition; together they close every existence
   question in this scope.
4. **Either consume or relabel the inert bundle material.** The cleanest consumer is a proposition of
   the form "a globally flat comparison across the agent cover exists iff `[T^x]` is trivial", which
   would connect `sec:geo-cech` to `prop:geo-trivializing-criterion` and to `06_gaussian`'s flat
   comparison hypothesis in one stroke. (G2)
5. **Sweep `02_geometry.tex` for untagged claims** — it is the only chapter checked with a
   systematic tag deficit, and its tag density (38 tags / 772 lines) is well below `05c`'s
   (67 / 1391 with far denser tagging of commentary). (G5)
6. **Give `geometry/` a dimension parameter and one Chapter-05c numerical witness.** Verifying
   `rad h_s^omega = ker D^omega s` and `eq:pb-fisher-connection-change` numerically on a trivial
   bundle over `R^3` is a day of work and would be the first computational contact with the
   chapter the project goal is built on. (G6)
