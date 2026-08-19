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
  homogeneous convex cones, whose T-algebra classification is open-ended; Koecher–Vinberg
  classifies only the *symmetric* cones — homogeneous **and** self-dual — by Euclidean Jordan
  algebras, a finite list. The finite answer is available for the symmetric case alone, and any
  exit gate that wants it has to declare self-duality rather than derive it from homogeneity.
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

---

## 9. 2026-08-14 finite collective-lift correction -- current authority

This section supersedes any conflicting reading above while preserving the earlier status record.
It closes one exact finite categorical joint-lift instance and leaves the general program open.

| Topic | Corrected status and boundary |
|---|---|
| Three-agent parity lift | **P.** For six paired binary channels, fixed p_kappa = p_0 + kappa chi D with |kappa| < 1 is positive, normalized, smooth, a marginal right inverse, and an immersion. Every proper marginal is product. For fixed marginals it is one parity line in a 57-dimensional Frechet fiber, not an arbitrary correlated-family construction. |
| Relabeling symmetry | **P/typed.** Paired simultaneous complements and typed agent permutations are exact symmetries. Odd independent channel complements require pseudoscalar kappa. No within-pair belief--model swap, GL(K) action, or Lie connection follows. |
| Agent-block VFE | **P.** With any one two-channel agent block varied and its four-bit outside marginal fixed, the outside-averaged conditional VFE difference and differential equal the corresponding global VFE restriction exactly. This is objective compatibility, not an intervention or convergence theorem. |
| Fisher residual | **P.** Generally, G_J - G_w = K - C + sum_i (1-w_i)G_i. Equality on a tangent subspace is exactly vanishing of that restricted bilinear residual. Here pairwise independence makes C = 0, and K is positive definite for nonzero kappa. At the center c = kappa/64, G_J = 4I_6/(1-c^2); the unit-weight residual is 4c^2 I_6/(1-c^2), hence 4I_6/16383 at kappa = 1/2. Full-tangent weighted equality requires every w_i = 1/(1-c^2); unit weights agree only at kappa = 0. |
| Ordering boundary | **P/limited.** The positive residual is parity-family-specific. The older two-bit smooth lift has an indefinite joint-minus-product Fisher difference, so no general Loewner ordering is restored. |
| Declared hyperedge record | **P/D.** With uniform prior, the supplied normalized record K_hyp(1|x) = (1+c chi(x))/2 has evidence 1/2, posterior p_kappa, tight VFE log 2, and product-lift excess -log(1-c^2)/2. It is an engineered three-agent hyperedge factor, not derived pairwise locality, conditional independence, or canonical agency. |
| Remaining scope | **O.** Arbitrary-family lift existence, canonical selection, coarse-graining preservation, independent odd relabeling without an interaction pseudoscalar, GL(K), interventions, autonomous agency, continuum laws, physical geometry/time/units, and renormalization remain open. Kappa is fixed relational or nomological data; promoting it requires an interaction-state type plus identifiability and rank checks. |

---

## 10. 2026-08-14 canonical dependence-selection certificate -- current authority

This chronological correction supersedes earlier claims only within the finite dependence-selection
scope stated below; all earlier sections remain as the historical record. The governing certificate
is `docs/derivations/2026-08-14-canonical-dependence-selection/`, with contract digest
`8112f0083a554a4df3b5de3875174d0b0cbfeee36a7bc2ea20e78c8cf9da6b39`.
It releases the frozen absolute-selector target as **COMPLETE_NEGATIVE**.

| Topic | Governing result and boundary |
|---|---|
| Absolute law-valued selector | **COMPLETE_NEGATIVE / REFUTED.** Conditional on admitting both explicitly declared marginal-compatible refinements `R_1/3` and `R_1/2` and requiring a single-valued section, the fair source law is sent to two distinct, non-relabeling-equivalent target joint laws with the same fair/fair singleton marginals. No absolute selector can satisfy both naturality equations. Split admission is a declared hypothesis, not a theorem about every morphism class. |
| Local naturality and uniqueness | **P/typed.** Naturality under coordinatewise, independently tensored finite Markov kernels forces the unique marginal section `S_X(mu_1,...,mu_n) = tensor_i mu_i`. This is not naturality under generic all-`FinStoch` kernels. |
| Maximal morphism class | **P/typed.** In a wide marginal-compatible category containing that full fixed-arity local class, a natural section exists exactly when every admitted arrow preserves product laws. Preparations force uniqueness, but the category premise contains every fixed-arity local kernel. The product-preserving arrows therefore form the maximal such category, and the product section is unique there. |
| Full VFE and Fisher recovery | **P/negative.** Singleton retention is noninjective and cannot determine full-joint VFE/KL or Fisher geometry. Equal singleton marginals admit a product law with zero KL and a positive correlated law with positive KL against the same positive product posterior. At the symmetric parity controls, `kappa = 0` and `kappa = 1/2` retain the same singleton family but have full Fisher tensors `4 I_6` and `(65536/16383) I_6`. |
| Typed-intervention recovery | **INCONCLUSIVE** for the broad unconditional claim because the ambient typed category and the required internal nonisomorphism have not been formalized. Conditional on the August 13 direct, latent, and null-extended BSC presentations being nonisomorphic objects in one declared typed-category forgetful fiber, universal two-sided recovery is impossible. This does not forbid a conventional right inverse that selects one representative. |
| Reference-relative selection | **P/conditional.** For finite `(p,T,m)`, a finite-KL minimizer of `D(q||p)` subject to `E_q T=m` exists exactly when `m` lies in `conv T(supp p)`, is unique as a law, and has support `{x in supp p : T(x) in F_m}`, where `F_m` is the minimal face of `conv T(supp p)` containing `m`. For deterministic `f`, reference `p`, and `r << f_#p`, the KL-minimizing completion is unique and composes along nested deterministic maps when each stage uses the pushed reference. These are reference-, support-, feasibility-, and map-typed results, not an absolute selector. |
| Retained Fisher quotient and blocks | **P/conditional.** For `rho: Theta -> N`, `rad(rho^*g) = d rho^{-1}(rad g)`; it equals `ker d rho` exactly when `im d rho` meets `rad g` trivially. Constant rank yields the positive-definite vector-bundle quotient, not automatically a global quotient manifold. Declared blocks require kernel splitting for direct quotient decomposition, Fisher orthogonality for additive energy, and the bracket/projectability and global typing conditions for descent. |
| Promoted parity rank | **P/limited.** The promoted family `(theta,kappa) -> Q_(theta,kappa)` has full-joint rank seven, while singleton retention has rank six with kernel exactly `span{partial_kappa}`. This closes the earlier augmented-rank check for this family only. Rank does not select agent blocks, supply intervention types, or agentize the law. |
| Supersession and remaining scope | Earlier phrases that canonical selection is open are superseded only by the scoped absolute no-go and the reference-relative replacements above. Earlier statements that rank checks remain are superseded only by the promoted parity rank calculation. **OPEN:** arbitrary-family lifts, coarse-preserving nonproduct selection, `GL(K)` covariance, autonomous agency, continuum laws, global quotient and block projectability without their stated hypotheses, physical geometry, physical time, units, and renormalization. |

---

## 11. 2026-08-14 finite typed-intervention certificate -- current authority

This chronological correction supersedes the earlier typed-intervention
`INCONCLUSIVE` wording only inside the frozen finite BSC category. The governing package is
`docs/derivations/2026-08-14-typed-intervention-nonidentifiability/`, with target digest
`efe715cba81c2000403811015e6cecb599f4023133543b5cb0ae77288bccc874`. Its frozen universal
passive-identifiability target is released as **COMPLETE_NEGATIVE**.

| Topic | Governing result and boundary |
|---|---|
| Raw and reduced categories | **D/P.** `FinTIP_(R,O)^iso` is the declared groupoid of finite normalized typed DAG presentations with every partial hard assignment. Total right override makes each context set a monoid. Equality of the complete two-sided contextual retained-response signature is an equivalence and a two-sided congruence. It defines `Red : FinTIP_(R,O)^iso -> FinRIE_(R,O)^iso`; retaining the identity-class response defines `Ubar_pass : FinRIE_(R,O)^iso -> FinObs_(R,O)^iso`. |
| Same-signature passive-identifiability target | **R/P.** The chains `L(1/4,1/3)` and `L(1/3,1/4)` have the same roles, binary cardinalities, edges, mediator target, passive crossover `5/12`, and complete passive retained law `(7/24,5/24,5/24,7/24)` in lexicographic coordinate order `(R,O)=(0,0),(0,1),(1,0),(1,1)`. Each reduction has fifteen classes. The first model's `do(E=0)` law `(1/3,1/6,1/3,1/6)` is absent from the complete second-model response image under all four admitted typed boundary flips, so the reduced experiments are nonisomorphic. |
| Null-extension control | **P/C.** An independent isolated binary node is invisible after every assignment to it and every one of the 27 partial `{R,E,O}` contexts. Forgetting that node induces an identity- and response-preserving quotient-monoid isomorphism. Null-node inventory does not carry the negative certificate. |
| Recovery typing | **P/R.** `Ubar_pass` is not essentially injective on the declared BSC subcategory, so no universal `R Ubar_pass ~= id_FinRIE` exists there. This does not refute a conventional representative-selecting section `Ubar_pass R ~= id_FinObs`. |
| Diagnostic boundary | **D.** The mediator-output total-variation contrasts `1/3` and `1/2` are exact diagnostics, but an arbitrary protocol-class bijection need not preserve the named mediator pair. The complete four-relabeling response-image mismatch is the proof invariant. |
| Supersession and remaining scope | **O.** The finite theorem does not establish category canonicity, a minimal realization, arbitrary latent-dilation equivalence, soft/stochastic/continuous interventions, autonomous agency, continuum/gauge/RG extension, VFE emergence, or any identification with physical geometry, time, units, constants, or ontology. Those category-independent and physicalization questions remain open. |

---

## 12. 2026-08-15 operational-intervention extensions -- current authority

This chronological correction supersedes the blanket open wording in Section 11 only inside the
frozen extension categories. The governing package is
`docs/derivations/2026-08-14-operational-intervention-extensions/`, with target digest
`af08539e8868b09e5165943d91c488c6e06a00ac7a00b1d408ae22ddca6ee7e1`. Its frozen conjunction is
released as **COMPLETE_AFFIRMATIVE**.

| Topic | Governing result and boundary |
|---|---|
| Contextual operational quotient | **P.** For fixed monoid `A` and response `Phi`, write `pi:A->Syn(Phi)`. Every response-compatible `q:A->B` with `Phi=psi q` admits one unique surjective unital `h:B->Syn(Phi)` satisfying `pi=h q` and `barPhi h=psi`; arrows run from finer `B` to coarser `Syn(Phi)`. For finite `A`, this gives minimum protocol-class cardinality and uniqueness over `A` only. A bare response object can have automorphisms, and no raw latent/DAG realization is minimized. |
| Compact topological quotient | **P/conditional.** If `A` is compact metrizable with jointly continuous multiplication and `Phi` is continuous into a metrizable Hausdorff space, a countable dense contextual signature realizes `Syn(Phi)` as compact metrizable with continuous multiplication and response. The continuous terminal factor additionally retains the compact-Hausdorff and quotient-map hypotheses. |
| Normalized marked-soft BSC experiment | **R/P.** The BSC pair with equal passive retained law has exact marked mediator-face diameters `(1-2epsilon)/3` and `(1-2epsilon)/2` for `0<epsilon<1/2`, with strict-interior witnesses. Identification from the passive retained law is refuted when morphisms preserve the mediator target, ordered `R`-to-`O` boundary, and one global response map. |
| Independent affine randomization | **R/P.** Independent selectors form `Delta(S)` under convolution. An exact fifteen-coordinate contextual minor has determinant `(2b-1)^6(2delta-1)^3/32`, nonzero for both released models. Randomized equivalence is equality, and every admitted affine unital convolution isomorphism restricts to the forbidden hard isomorphism. Convexification destroys the old unmatched-response invariant, so this contextual-rank proof is load-bearing. |
| Standard-Borel and compact-Feller tiers | **P/typed.** On a finite DAG of standard-Borel node spaces and palettes, declared normalized pointwise kernel families with jointly measurable evaluations give a Borel retained response by finite recursion. The construction supplies an algebraic quotient but does not by itself establish a standard-Borel quotient; that requires an exhibited smooth classifier or stronger topology. Compact-Polish nodes, compact palettes, isolated baseline symbols, and jointly Feller mechanisms give a compact metrizable quotient with weakly continuous response. Finite-coordinate does not mean finite cardinality. |
| Circle heat-kernel witness | **R/P.** The ordered chains `m(dR)H_s(R,dE)H_t(E,dO)` and `m(dR)H_t(R,dE)H_s(E,dO)` have the same passive retained law. Yet `H_s` strictly Blackwell-dominates `H_t`, and `{nu H_t}` is a proper subset of `{nu H_s}`, with positive smooth witness `nu_rho=H_rho(x_0,dot)` for `0<rho<t-s`. Identification from the passive retained law is refuted in the frozen compact-Feller heat category. |
| Morphism boundary | **D/typed.** Every admitted typed BSC or circle experiment comparison uses one global tuple of compatible typed state maps, protocol map, and protocol-independent response intertwiner. The ordered roles are `R` input/parameter and `O` output/observation. Target/type coloring is retained where declared and, on the circle, heat geometry is retained. Target erasure, boundary exchange, and time reversal define different categories. |
| Supersession and remaining scope | **O.** Blanket claims that every soft, stochastic, or continuous extension is open are superseded only by the preceding frozen results. Correlated/shared-noise or adaptive selectors and identification of null-version point interventions from almost-sure passive observational conditionals remain open, as do noncompact quotients, category canonicity, arbitrary latent dilation, raw minimal realization, fixed-observation ELBO/VFE recovery, autonomous agency, base-manifold continuum/gauge/RG dynamics, and every physical or ontological identification. |

---

## 13. 2026-08-15 full meta-agent construction roadmap -- OPEN/TODO

This section records the next dependency order only. It proves no theorem, modifies no release, and
does not promote the certified fixed-$r_*$ pair of parent marginals to a full pointwise probabilistic
meta-agent datum. The pointwise certificate remains authoritative for exactly its frozen
conjunction; the full datum still requires generative, recognition, and posterior objects plus the
VFE and model interfaces. Even that completed fixed-point datum is not a geometric meta-agent;
geometric language requires patchwise local sections and gluing in Phase 4.

**Phase 0 -- notation standard, before new mathematics.** The base is $\mathcal C$, agent supports
are $\mathcal C_i$, and the overlap patch for a candidate block $A$ is
$\mathcal U_A=\bigcap_{i\in A}\mathcal C_i$. Bare $R$ is not an overlap region; intervention text
retains the typed roles $R$ input/parameter, $E$ mediator, and $O$ output/observation. A principal
bundle is $\mathscr P_G\to\mathcal C$; full generative and recognition laws are $\mathbb P$ and
$\mathbb Q$; and the posterior is $\boldsymbol\Pi$. The symbol $\varpi$ remains reserved for the
established projection notation. Receiver occupancy remains $\alpha_i^x$, with
$\eta_{ij}^q=\alpha_i^q\beta_{ij}$ and $\eta_{ij}^m=\alpha_i^m\gamma_{ij}$; these $\alpha_i^x$ are
external occupancy or sampling weights, not new transformer attention parameters. New full-law
work uses $q_i^b$ and $q_i^m$. The symbol $m_i$ remains a model sample or presentation wherever so
typed; only explicitly law-valued frozen-RG occurrences may receive the local alias $q_i^m$.
Preserve the distinct dependencies $s_i^{o,X}$ and $q_i^{o,X}$; bare $s_i$ is not globally renamed.
A model point $m$ becomes a generative mechanism only through a declared normalized-kernel
evaluation map $m\mapsto K_m$. General statistical model spaces are primary; multivariate Gaussians remain optional
computational realizations. The phase closes only with one authoritative symbol table, migration
table, and collision scan. The normalized pointwise coarse channel is $C_A$; a moving deterministic
coarse map is $c_t$.

| Order | OPEN deliverable | Exit condition before the next phase |
|---|---|---|
| 1 | Full pointwise probabilistic meta-agent datum at fixed $r_*$ | Type $\mathbb Q_I$, $\mathbb P_I$, and $\boldsymbol\Pi_I$; declare one normalized recognition-independent coarse channel $C_A$ while keeping the structural $X_A=\chi_A(X)$ outside that channel; construct $\mathbb Q_A$, $\mathbb P_A$, and $\boldsymbol\Pi_A$; derive belief/model marginals rather than treating them as a substitute for the joint laws. This is not yet a geometric meta-agent. |
| 2 | Pointwise VFE and holonomy closure | Prove the common-channel conditional-KL defect and normalization; declare the joint holonomy actions; prove coarse-channel equivariance and the appropriate covariance or invariance of $\mathbb P_A$, $\mathbb Q_A$, and $\boldsymbol\Pi_A$. A relation $h_\#q_A^x=q_A^x$ is only marginal compatibility. A holonomy-blind path-independent parent needs full-law compatibility, while a richer parent may retain holonomy as internal state. A dynamical statement must also prove the relevant sector is flow-invariant. |
| 3 | Comparison-category theorem | After the full pointwise probabilistic meta-agent datum closes, prove how target erasure, boundary exchange, time reversal, protocol-dependent relabeling, and latent dilation change the comparison problem. Interventions remain analyst-declared probes, not ontic actions inserted into the dynamics. |
| 4 | Extension across $\mathcal U_A$ | Promote pointwise laws to local sections and prove gluing, cocycle, regularity, and path-consistency conditions while treating active-set changes, soft or multiple membership, and rank/stabilizer jumps. Only after this exit gate is geometric meta-agent language eligible. |
| 5 | Participatory and cross-scale nonequilibrium | **OPEN.** Derive reciprocal scale coupling from one typed action or controlled reduction. Frozen gradient flow may equilibrate; Wheelerian feedback, moving coarse maps, open flux, stochastic driving, or antisymmetric sectors require separate proofs and must not be inferred from the pointwise certificate. |

The detailed ordered roadmap is in `solid_RG_theory.md`, Section 12. Central theorem chapters and
release metadata remain unchanged until the relevant exit conditions are proved and independently
verified.

## 14. 2026-08-15 full pointwise probabilistic datum -- current authority

The governing release is
docs/derivations/2026-08-15-full-pointwise-meta-agent/release.json, bound to target digest
15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87. The canonical manuscript
status is **ESTABLISHED**. The package records ledger state EVIDENCE_VERIFIED and terminal release
status COMPLETE_AFFIRMATIVE_WITH_CORRECTIONS; those are evidence-package labels, not replacements for
manuscript claim status. The corrections are to the certification apparatus and not the mathematics:
two of the four domain approvals are stale against canonical sources edited after they approved, the
first provenance snapshot is unauditable (0 of 15 entries verify), and the sixteen-attack rejection
count is not evidence. Two certification obligations are open. See
docs/derivations/2026-08-15-full-pointwise-meta-agent/POST-RELEASE-CORRECTIONS.md.

At one fixed \(r_*\in\mathcal U_A=\bigcap_{i\in I}\mathcal C_i\), with finite child block \(I\),
parent label \(A\), fixed structural \(X\), and \(X_A=\chi_A(X)\) outside the random channel, one
normalized recognition-independent
\(C_A:\mathsf Y_I\rightsquigarrow\mathsf Z_A\) pushes the fixed fine generative joint, selected
posterior-version family, and correlated recognition law to normalized
\(\mathbb P_A\), \(\boldsymbol\Pi_{A,o,X}\), and \(\mathbb Q_{A,o,X}\). The observation space remains
\(\mathsf O\). A parent model evaluator is either induced by standard-Borel disintegration or is a
predeclared jointly measurable normalized kernel family satisfying the separate almost-sure
compatibility condition. Recognition, prior, and posterior marginals are derived coordinate
projections; they do not replace or reconstruct the full laws.

The common-channel KL chain is additive in \([0,+\infty]\). Adding the same finite real
\(-\log p_X(o)\) to both KL terms gives an extended-real VFE identity; a finite VFE may be negative.
Without a finiteness premise, \(\Delta_A=0\) exactly when the discarded conditional recognition and
posterior laws agree \(\mathbb Q_{A,o,X}\)-almost surely. Finite fine KL is required for ordinary
subtraction \(\mathcal F_I-\mathcal F_A=\Delta_A\) and for the stated two-way pairwise
common-recovery equivalence. Family-wide common recovery requires simultaneous hypotheses for every
family member. Holonomy blindness additionally requires typed actions, full fine-law covariance,
compatible selected posterior versions, \(C_A\) equivariance, evaluator covariance, and
fixed-\((o,X)\) isotropy for same-slice invariance. The raw-root retention alternative preserves the
holonomy coordinate and selects no membership.

Static Phases 1--2 are closed only at this pointwise level. Canonical coarse-channel, membership, or
partition selection; the frozen comparison category; family-wide recovery absent its simultaneous
hypotheses; extension and gluing across \(\mathcal U_A\); parent local sections; a geometric
meta-agent; autonomy; agency; nonequilibrium persistence; continuum limits; physical time; unique
latent DAG or microscopic physics; and ontology remain **OPEN**. Dynamics also remains **OPEN**:
neither a deterministic semiconjugacy nor a Markov semigroup or generator intertwining follows from
the static release.

## 15. 2026-08-17 rescaling map and the refuted compatibility law -- current authority

This section supersedes conflicting readings of the `Theory/07b` RG sections and of §2's
"Agent-network RG equations" row, while those earlier entries stand as the dated record. The
rescaling map's identification half was built in the finite categorical laboratory
(`src/multiagent_elbo/finite/rescaling.py`, `coupling_readback.py`, `cocycle_flow.py`;
pre-registered design and two dated amendments in
`docs/superpowers/specs/2026-08-17-rescaling-map-design.md`), and its checks ran with thresholds
fixed before measurement. All results below are **C** (computed on declared finite instances).

| Topic | Result and boundary |
|---|---|
| Step construction | **C.** Gauge covariance of the composite step to `1e-12`, with the declared parent law forced to transform as root-frame data; exact Wilson-line holonomy conservation with interior block holonomy retained as marks. |
| Compatibility law | **R (measured).** `K_{b1 b2} = K_{b1} K_{b2}` fails by `0.204` against the pre-registered `1e-10`, with a lossless intermediate projection; the defect is the Bayes kernel composition and is of the same order (`0.12`–`0.19`) at every accessible depth and factorization. **Naming corrected 2026-08-18:** `0.204` is the sup norm of the *anchored log-density* difference in the read-back gauge, not a distance between laws. The laws themselves differ by total variation `0.042` and KL `0.0050`, so "order one" is a statement about the coupling vector and must not be read distributionally. The refutation is unaffected and survived every artifact hypothesis tested — the flat control gives a *larger* defect (`0.452` vs `0.204`), 24 edge-order permutations give only `{0.1994, 0.2035}`, and the kernel-level gap is `0.721`. The flow is a typed cocycle; `07b` now records this after its compatibility equation, whose label is renamed `eq:rg-kernel-compatibility`, and its closure theorem carries the caution that no exhibited kernel family satisfies the scale-composition hypothesis. |
| Fixed structures | **C.** Per-ratio composites (blocking plus self-similar re-tiling) contract (spectral radius `0.78`–`0.83`) onto factorized fixed structures (pairwise block at machine zero, on a provably invariant and measured-attracting subspace; pair-sector eigenvalues near `0.17`); ratio-two and ratio-three fixed structures differ by `0.81` relative sup. Level-local only; no universality or exponent claim. |
| Diagnosis | **D.** Single-boundary towers are quasi-one-dimensional (Perron–Frobenius transfer matrix), so factorized fixed structures are the expected 1D outcome; which boundary-multiplicity architectures sustain interaction is a declared open measurement (bundled towers). |

## 16. 2026-08-18 regenerated attention, boundary multiplicity, and capacity -- current authority

This section supersedes the triviality reading of §15, which stands as the record of the
**passive** channel (coupling inherited through blocking with attention frozen). Amendments 3–6
of the rescaling design declared these measurements before running them; all results are **C**
(computed on declared finite instances), report-only by declaration, with post-hoc readings
labeled in the amendments.

**Amendments 10–14 were republished on 2026-08-18.** The lab-versus-theory audit of that day
(`docs/audits/2026-08-18-lab-vs-theory-audit.md`, finding 1) established that the Proposition-4
block energy charged nothing for a block's parent. The parent coordinate is a variable of the
declared tower and its point mass contributes `E_Q[-log P_S(parent)]`; that term was omitted, and
the omission was not neutral. With a free parent the per-block minimum decomposes agent by agent,
so `cross(R, x) = Σ_B min_p Σ_{a∈B} c_a(x_a, p)` and the all-singleton partition is the exact
minimizer at **every** configuration — verified constant to 8.9e-16 across all 531,441
configurations. The singleton verdicts of amendments 10–14 were therefore a property of the
construction, not a measurement. Booking the declared top prior (`tower_vfe.PARENT_STATE_WEIGHTS`,
the same nine-element parent space the partition route uses) reverses them: it is worth 11.67 nats
between the two candidates at the declared seed. Every re-taken number below comes from
`docs/results/2026-08-18-amendments-10-14-republication.json`; the retired values are named in
each row. Nothing outside the partition posterior moved — the retention, capacity, and ceiling
numbers of amendments 3–9 are unchanged and were reproduced independently by the audit.

| Topic | Result and boundary |
|---|---|
| M-bundle (amendment 3) | **C.** One-step pair retention versus cut couplings per block boundary: `0.156`, `0.441`, `0.564` at `k = 1, 3, 6`, length-independent at fixed `k`, sublinear with collapsing increments, no crossing of one. Thickening the boundary alone does not rescue the passive channel. |
| Regenerated attention (amendment 4) | **C.** Rows regenerated per level from flow-averaged transported divergences over the conserved connection (declared `tau = 1`, uniform occupancies); the regenerated coarse action passes the C1 covariance identity to `1e-11`. M-regen: the regenerated composites converge to **interacting** fixed structures — pair sup `0.579` (ratio 2, 110 iterations) and `0.625` (ratio 3, 34 iterations, worker) against the passive machine zero — with sustained-over-injected `1.246`, so the inherited and regenerated channels equilibrate above the injection floor. The passive triviality is a frozen-attention artifact. |
| Completeness (amendment 5) | **C.** The typing survives regeneration: RC6 composition defects `0.165`–`0.265` (passive `0.152`–`0.190`; larger by construction since intermediate levels act); R-ray residual `0.296` at the seed; R-cross `0.644` relative sup between the ratio-2 and ratio-3 interacting fixed structures (passive `0.806`). The flow is a typed cocycle in both channels; fixed-structure language still requires a declared ratio. |
| M-capacity (amendment 6, re-measured under amendment 8) | **C, reversed.** With the root-framed gauge-covariant sector charge (2026-08-18 audit, F8), sector-carrying parents (27 labels: presentation times belief-channel `Z_3` charge referenced to the block root through the spanning-tree transport) **raise** one-step retention: `0.209` vs `0.156` at `k = 1`, `0.568` vs `0.441` at `k = 3`, with the constant-sector control reproducing the nine-state values exactly and retention still below one. The 2026-08-17 values (`0.144`, `0.406`) used a family-referenced charge that shifts under a sample-shift gauge and are retired. Declared caveat stands: the sup statistic dilutes across alphabets; the alphabet-comparable statistic is M-info (amendment 9, next row), measured the same day. |
| M-info (amendment 9) | **C.** The alphabet-comparable capacity statistic: boundary mutual-information retention `R_MI = I(P1;P2) / I(X_B1;X_B2)`, both by exact marginalization, with `R_MI <= 1` a data-processing theorem (the coarse law is the pushforward of the fine law through the per-block kernels) and the statistic gauge-invariant by construction. Ceiling `I(X_B1;X_B2)`: `4.97e-6` nats at `k = 1`, `1.49e-5` at `k = 3` — the declared seed's boundary is weakly correlated (pair sup `0.0163`). Retention: `R_MI(9) = 0.0230` vs `R_MI(27) = 0.0254` at `k = 1` (`+10.2%` relative), `0.0667` vs `0.0702` at `k = 3` (`+5.3%`). **Corrected reading, 2026-08-18 (audit finding 3):** the earlier sentence that this confirms the amendment-8 direction is **withdrawn**, on two grounds. First, the sign is a theorem, not a measurement: `extended[p*sectors+s] = base_kernel[p] * (charge==s)` makes the 27-label parent a deterministic refinement of the 9-label one, applied identically on both blocks with the denominator unchanged, so `R_MI(27) ≥ R_MI(9)` by data processing for every instance, ratio, coupling and readout. Second, the declared `constant_sector` control collapses the sector axis and reproduces the nine-state law by construction — an identity, not an independent check. The operative control is a same-cardinality readout carrying no gauge charge, and it beats the charge everywhere: the first member's own belief coordinate gains `+67.4%` at `k = 1` and `+38.6%` at `k = 3` against the charge's `+10.2%`/`+5.3%`. The charge is not distinguished among three-label readouts at this seed, and the honest statement is the size of the gain *relative to a non-charge readout*, which is negative. The magnitude reading survives: the blocking transmits only 2–7% of the boundary information, so the sup-norm retentions (`0.156`–`0.568`) overstate informational retention by roughly an order of magnitude. All statements are seed-local by declaration. |
| M-part (amendment 10) | **C, republished 2026-08-18 — and the verdict reverses.** Participatory blocking: the Proposition-4 partition posterior (flow-averaged derived energy, Ewens prior at concentration one, temperature one, untempered) selects the blocking at each level from the declared cycle candidates. With the parent priced, the modal class at level zero is the **direct single block** at both declared 6-cycle instances (`0.958`/`0.955`), with the staged classes far behind (ratio 3: `0.039`/`0.042`; ratio 2: `0.0023`/`0.0021`) and singletons at `1.1e-4`/`1.1e-4`. **Retired:** the 2026-08-17 reading "the modal class is the singleton partition (`0.586`/`0.576`) … no aggregation is favored at this seed" and everything that followed from it. That verdict was the unpriced parent, not the seed. What survives is the *shape* of the competition, not its winner: the derived energy still opposes the Ewens rich-get-richer prior and the ordering among the aggregating classes is unchanged (direct > ratio 3 > ratio 2). Placement-symmetry check: within-class gaps `4.4e-6`/`1.1e-3`, so the min-root convention with the identity-holonomy flat mixture is still not exactly re-rooting equivariant on wrapped blocks, reported as declared. Reading per the declared rule: **aggregation is free-energy-favored at this seed**, and the whole-system block is what the posterior selects; the open question is no longer whether anything binds but why the intermediate ratios lose to the extreme. The verdict is concentration-dependent — see the M-part surface row. |
| M-bind (amendment 11) | **C, republished 2026-08-18 — and it is a statement about the flow, not the landscape.** Coupling-scale sweep: pair table scaled by `lambda ∈ {1, 3, 10, 30, 100}` (pair sup up to `1.63`), all instruments re-run per grid point. The ceiling `I(X_B1;X_B2)` grows as `lambda^2` to within 2% across four decades (`4.97e-6` to `4.86e-2` nats at `k = 1`), with saturation just beginning at `lambda = 100`. The partition posterior barely moves: the modal class is the **direct block at every lambda**, `0.9583` at `lambda = 1` rising to `0.9616` at `lambda = 100`, no crossing anywhere. **Retired:** "the modal class is the singleton partition at every lambda … the singleton preference is structural" — that was the unpriced parent. Two corrections to how this row may be read at all (audit finding 2). First, `lambda = 0` is now **excluded by code rather than by declaration**: its boundary-information ceiling is `1.13e-16` nats, so a retention ratio there divides one roundoff residue by another, and `capacity_information_retention` raises. Second, and structurally: `_kernel_model` builds the block energy from the level-invariant declared structure and never from `instance.couplings`, so `U(R, x)` is `np.array_equal` between `lambda = 1` and `lambda = 100` across all 531,441 configurations and all candidate partitions. **No coupling of any magnitude can move the partition-energy landscape.** A coupling sweep here reweights which configurations the energy is averaged over — it is a flow reweighting — and the flatness of the modal class along it is a property of the construction, not evidence about formation. The claim "no formation transition on this ray" is withdrawn as unsupported by this instrument. The `R_MI` reading survives unchanged and is what the sweep does measure: flat-to-declining (`0.0230` to `0.0142` at `k = 1`), so transmission is **kernel-limited, not signal-limited** — the `t ≈ 0.15` per-edge factor is a property of the Bayes channel, which does not adapt to signal. |
| M-anchor (amendment 12) | **C, republished 2026-08-18 — the mechanism survives, the modal flip does not.** The environment restored as a blockable agent class: one pinned agent per site (identity transport, two-channel divergence field, dressing rides the audited instruments; the coarse environment blocks by MAP under the declared downward kernels, and re-dressing the undressed coarse reproduces the audited coarse exactly). With the parent priced, direct aggregation is already modal on the bare instance, so no anchor pattern flips a modal class and the row can no longer be read as licensing binding by a flip. What the anchors do is still directional and still separates the patterns: **uniform** anchors *deepen* direct (`0.9592` at `k_env = 0.5` to `0.9826` at `8`) while draining the aligned pairing (`1.09e-3` to `1.97e-4`); the **distinct** control also deepens direct (`0.9588` to `0.9705`) and leaves the aligned pairing flat (`1.12e-3` to `1.18e-3`); **shared-pairs** anchors move mass the other way, lifting the aligned ratio-2 placement 32-fold (`1.21e-3` to `3.92e-2` at `k_env = 8`) and pulling direct down to `0.815`, the only pattern that costs the whole-system block anything. The placement gap remains physics (`0.038` at `k_env = 8`): the posterior still selects the placement matching the environment, not just the ratio. **Retired:** the specific masses `0.552`/`0.840`/`0.902` and the realized anchored path `6 → 1`. Surviving reading, now as a relative statement: shared evidence pulls toward the blocking that shares it, uniform evidence pulls toward the whole, and no shared evidence does neither. |
| M-flow (amendment 12) | **C, republished 2026-08-18 — the reversal was an artifact and is withdrawn.** Joint dynamics on `(x, R)` targeting the annealed joint `exp(-A) P(R) exp(-U)`, compared against the exactly computed annealed marginal. With the parent priced, quenched and annealed **agree**: on the bare instance direct is modal both ways (`0.9583` quenched, `0.9619` annealed exact), and with shared-pair anchors at `k_env = 2` both remain direct-modal (`0.9434` quenched, `0.9450` annealed). The Jensen gap between `E_w[U]` and the joint is now numerically small and changes no verdict. **Retired in full:** "the annealed verdict reverses the quenched one" and the reading built on it, that "the M-part/M-bind singleton preference was a property of the quenched update on environment-free levels". Both the reversal and the preference it explained were consequences of the free parent. The instrument itself — an exactly computed annealed marginal beside the quenched update — is unaffected and remains the right comparison; it simply has nothing to separate at this seed. |
| M-cross-env (amendment 13) | **C, republished 2026-08-18 — the mechanism is unchanged and the numbers are new.** Shared-pairs strength sweep `k_env ∈ {8, 16, 32, 64, 128}`, computed exactly per point: the aligned placement's mass **saturates** at `0.0388` by `k_env = 64` (identical to six decimals thereafter — the frozen limit reached numerically), direct stays modal at `0.812`; the distinct control is clean (direct `0.963`, aligned `0.00116`). **Retired:** the plateau value `0.201` and the singleton-modal reading (`0.617`). No crossing, and the declared reading is unchanged in substance: pinning saturates before condensing. The mechanism the saturation exposes is untouched by the correction, because it is structural rather than numerical — the per-site pinned dressing **factorizes over sites**, so at infinite inertia two agents pinned to the same value are indistinguishable from two agents with private duplicate evidence, and a point-mass environment aligns but cannot correlate. Consequence, still the declared next construction: binding-by-shared-evidence in the correlation sense requires **finite-inertia environmental agents**, whose fluctuations, integrated out, induce effective coupling between co-attached neighbors. |
| M-share (amendment 14) | **C, republished 2026-08-18 — the channel decomposition survives with new magnitudes.** Finite-inertia shared environments implemented by exact marginalization (induced group potential decomposed by the anchored Moebius route; the `m→∞` limit reproduces the amendment-13 pinned values, and the private-duplicate control induces exactly zero pair coupling, both tested). Per the declared rule, correlation binding is still **not licensed**: the aligned placement's mass rises monotonically in inertia toward the pinned plateau (`0.00641 → 0.03924` at `k_env = 8`) and never exceeds it. The control contrast still isolates the correlation channel as real: at `m = 0` the shared agents give the aligned pairing **5.6×** the private-duplicate control (`0.00641` vs `0.00114`) on an induced pair sup of `12.62`, and the contrast closes as the environment freezes (`m = 64`: `0.03924` vs `0.03924`, exactly the point of amendment 13). **Retired:** the magnitudes `0.110`/`0.194`, the `9×` contrast, and the claim that at `(k_env = 8, m = 0)` the free shared environment "tips direct modal (`0.366`)" — direct is now modal everywhere, so that sentence no longer distinguishes anything and is withdrawn rather than restated. Surviving reading: **alignment and correlation are competing channels for the aligned-placement statistic, not composing ones** — maximal alignment (the pinned limit) beats maximal correlation at this seed, and no pattern condenses the aligned pairing. |
| M-part surface (2026-08-18, audit item 8) | **C.** The Ewens concentration was hardwired at one and unreachable from the published route; it is now a parameter of `blocking_posterior`, and the verdict is reported as a surface. The modal class crosses from the direct block to singletons at `theta = 6.117` (`k = 1`) and `theta = 6.173` (`k = 3`), bracketed by bisection to nine digits. At the declared `theta = 1` the direct block holds `0.958`; the published verdict is therefore not a knife-edge in the concentration, but it is a point on a surface and is quoted as one. |
| Anchor sweep (2026-08-18, audit item 7) | **C.** The anchored Moebius read-back pinned its ground state at the all-zero anchor with no parameter and no config key, which is a gauge fixing every sup-norm statistic moves with. Swept over all 729 anchors of the coarse triple, the one-step pair retention runs `0.1295`–`0.1874` at `k = 1` (pinned `0.1557`, range `37.2%` of the pinned value) and `0.3759`–`0.4621` at `k = 3` (pinned `0.4414`, range `19.5%`). The pinned values stand as published; the range now travels with them. The mutual-information retention is exactly anchor-invariant, being a functional of the law alone, so this qualifies the sup-norm quantities only. |
