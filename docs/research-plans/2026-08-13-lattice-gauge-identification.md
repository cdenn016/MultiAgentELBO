# Is MAgent-on-a-grid a lattice gauge theory?

Date: 2026-08-13. Repo HEAD: `334c7ff`. Model repo cross-checked: `C:/Users/chris and christine/Desktop/MAgent_Model-main`.

Three lenses (`lgt-identification`, `continuum-limit`, `plaquette-elbo`) probed the identification; each
was attacked by a skeptic. Two of the three skeptics broke their lens's verdict. Where a skeptic found a
false retirement or a false novelty, the skeptic governs, and this report is written from the post-skeptic
position. Every load-bearing number below was recomputed here from scratch, not carried over.

## 1. Verdict

The kinematics are Wilson's, term for term, and must be cited rather than presented as construction: group-valued
links on oriented edges with reversal-inverse, the vertex gauge law, ordered-product transport, plaquette
holonomy on declared 2-cells, and the trace of the loop holonomy as the invariant observable. The dynamics
are not lattice gauge theory and cannot be made into it at the declared structure group, because there is no
Haar probability measure on `GL⁺(K,ℝ)`, no lattice spacing, and no volume limit on a finite declared agent
multigraph — and the plaquette action the model actually ships is gauge-noninvariant under the group it
declares. The correct name for the object is **a gauged lattice sigma model with an information divergence
and a state-dependent fiber metric, carrying Wilson kinematics on a general multigraph** — not lattice gauge
theory, not merely analogous to it, and not a special case of it in any sense that transports theorems.

## 2. Term-by-term correspondence

| This programme | Lattice gauge theory | Status |
|---|---|---|
| `Θ_e ∈ G` on oriented edge copies, `Θ_ē = Θ_e⁻¹` (`Theory/02_geometry.tex` eq. `geo-regime-two-links`) | Link variable `U_{x,μ} ∈ G`, `U_{-μ} = U_μ†` | **MATCHES** — verbatim |
| `Θ'_e = (a_i)⁻¹ Θ_e a_j` for `e: j→i` (eq. `geo-regime-two-gauge-law`) | `U_{x,μ} → g_x U_{x,μ} g_{x+μ̂}⁻¹` | **MATCHES** — same orientation; `a = g⁻¹`. Correspondence is stated in `PIFB2.tex:385`, absent from `Theory/02` |
| `open_path_transport` ordered product, last link leftmost | Path-ordered product of links | **MATCHES** |
| `plaquette_curvature` → `H(∂cell) − I` | Plaquette `U_p = U_μU_νU_μ†U_ν†` | **MATCHES** in form |
| `conjugacy_invariants` → `tr H`, `det H` | Wilson loop `W(C) = tr ∏ U_ℓ` | **MATCHES** (real links, no `Re` needed) |
| `trivialization_via_spanning_tree`, `_spanning_forest_frames` | Maximal-tree gauge fixing | **MATCHES** — classical, Creutz 1977 |
| `|E| − |V| + 1` fundamental cycles | Independent plaquettes / cycle basis | **MATCHES** |
| `G ≤ GL⁺(K,ℝ)`, noncompact | `G` compact (`SU(N)`, `U(1)`, `ℤ₂`) | **FAILS** — see §3.1 |
| Frobenius `Σ_p ‖W_p − I‖²_F` (`lattice_gauge.py:314`), `λ_ym = 0.1` by default | `β Σ_p (1 − (1/N)Re tr U_p)` | **FAILS** — not gauge-invariant at `GL⁺(K)`; measured rel. spread 3.50 on one orbit |
| No Haar measure, no `Z`, no sampler in either repo | `∏_ℓ dU_ℓ exp(−βS_W)`, normalized Haar | **FAILS** — no probabilistic sector exists |
| Matter = a probability law `q_i`; coupling `D_KL(q_i ‖ Θ_e# q_j)` | Matter = vector in a linear rep; `φ†_i U_e φ_j` | **FAILS** — genuinely different, and this is the one place the programme is ahead |
| Fiber metric = belief precision `Σ_i⁻¹`, state-dependent | Fixed invariant inner product on the rep | **FAILS** — different mechanism for invariance |
| Finite declared multigraph, `two_cells` a free argument to `InteractionComplex` | Regular lattice, 2-cells forced, spacing `a`, volume `|Λ|` | **FAILS** — no `a → 0`, no `|Λ| → ∞` |
| Dynamical links: `self.twists = nn.Parameter(...)` (`lattice_gauge.py:106`) | Links are the integration variable | **PARTIAL** — links are *optimized*, never *integrated*. This is gradient descent on a penalty, not lattice gauge theory |

## 3. Disanalogies

### 3.1 Noncompactness — what exactly it breaks

This is the disanalogy that breaks the most, and the corpus has previously stated both a right conclusion
from a wrong premise and a wrong conclusion from a right premise. The precise accounting:

**It does not break normalization of a single plaquette density.** The heat kernel of a left-invariant metric
on any Lie group is a normalized probability density with respect to Haar; Brownian motion on a Lie group is
stochastically complete because a left-invariant metric is complete and homogeneous, hence Ricci-bounded-below.
Finiteness of Haar is not required for that. The `plaquette-elbo` lens was right about this and the dispatch's
stated obstruction, as posed, is wrong.

**It does break normalization of the link-space law.** Route (a) needs `∏_p p_t(U_p)` normalized as a law on
`G^E`, not on `G^P`. Under the tree-plus-plaquette change of variables the `|E| − |P|` spanning-tree coordinates
are left free and integrated against Haar. That integral equals `Haar(G)^{|E|−|P|}`, which is 1 only because
compact Haar is a probability measure. On noncompact `G` it is infinite. The lens's own witness proves the point
against itself: `GL(1,ℝ)₊` is abelian, so its heat kernel *is* a class function and *is* gauge-invariant, yet the
Wilson law still diverges. Infinite Haar mass is the binding constraint; loss of Ad-invariance is a second,
independent one.

**It does break bi-invariance, hence gauge invariance of any metric-built plaquette term.** A connected Lie group
carries a bi-invariant metric iff it is isomorphic to compact × abelian (Milnor 1976, Lemma 7.5 — stated for
connected groups, so it applies to `GL⁺(K,ℝ)`, a point worth writing down since `GL(K,ℝ)` is disconnected).
For `K ≥ 2` there is none, so `−log p_t(U)` is not a class function and `‖·‖_F` is not conjugation-invariant.

**It does break the Wilson trace action, but not by unboundedness alone.** Recomputed here on `SL(2,ℝ)` boosts
`U = diag(eᵗ, e⁻ᵗ)`, `det = 1` exactly, `1 − ½ tr U`: `−0.12763, −0.54308, −2.76220, −9.06766, −73.20995` at
`t = 0.5, 1, 2, 3, 5`. Unbounded below, so `exp(−S)` is not integrable. But the *stated mechanism*
"`1 − Re tr U/N` is unbounded below along noncompact directions" is false in general: on the unipotent
upper-triangular subgroup of `GL(3,ℝ)`, noncompact and unimodular, `tr U ≡ 3` identically, so the Wilson factor
is the constant 1 and the integral diverges purely from infinite Haar mass. Both mechanisms are real; neither is
universal; the conclusion (no Wilson Gibbs law at noncompact `G`) holds under either.

**It does break the shipped action's gauge invariance — and this is a live defect, not a closed sector.**
`MAgent_Model-main/gauge_agent/lattice_gauge.py:314` implements `yang_mills_action` in the Frobenius form
`S = (β/K) Σ_agent Σ_plaq ‖W(p) − I‖²_F √|g|`, wired into the objective at `full_vfe.py:2233-2239`
(`total = total + self.lambda_ym * R2`), with `lambda_ym: float = 0.1` as the default in both
`full_vfe.py:381` and `run_experiment.py:178`, and set to `0.1` in the checked-in configs
`runs/minimal/config.json:23` and `runs/hamiltonian_oscillator/config.json:23`. That action *is* bounded below
(it is a squared norm, `≥ 0`), so the claim "no minimization principle exists" is wrong. What it is not, is
gauge-invariant. Recomputed here, `K = 3`, `‖W − I‖²_F = 1.015420` at base, under five random `GL(3)` vertex
gauges: `0.9927, 0.8217, 3.8727, 2.0963, 0.3236` — relative spread 3.50. Under an orthogonal gauge:
`1.0154204711` vs `1.0154204711`, invariant to ten digits. Pinning the holonomy inside the compact stabilizer
does not rescue it: with `H` a rotation by 0.4 inside `Stab(e₁) = SO(2) ⊂ GL⁺(3)` and the one-parameter gauge
`A = diag(1, s, 1/s)`, `‖A⁻¹HA − I‖_F = 0.5619, 0.8105, 1.9518, 7.7892, 38.942` for `s = 1, 2, 5, 20, 100`,
while `tr(A⁻¹HA) = 2.8421219880` is fixed to ten digits throughout. The programme therefore ships, on by default,
a plaquette penalty whose value is an artifact of a gauge choice it declares to be unphysical. That is the single
most actionable finding in this sweep.

The same failure hits every metric-built diagnostic. On a 4-cycle with `GL⁺(2)` links, `λ₀` of the bare
connection Laplacian moves `0.01853858 → 0.00122033` under a random `GL⁺(2)` vertex gauge (rel. dev. 0.934),
and can be driven to zero by gauge alone: `A_i = diag(s, 1/s)` gives
`λ₀ = 3.060e−04, 1.268e−04, 1.154e−06, 1.426e−08, 1.162e−10` for `s = 1, 3, 10, 30, 100`. Under `SO(2)` gauges
the same quantity is invariant to `1.4e−12`. **Consequence for all future diagnostics: at `GL⁺(K)` only
conjugacy invariants of the loop holonomy are admissible. Frobenius plaquette norms and bare connection-Laplacian
eigenvalues are not.** The corpus already scoped this correctly at `overview.md:435` and `PIFB2.tex:408`;
worklog 3h.4 contradicts that scoping and must be withdrawn.

### 3.2 No measure, no partition function, no integration over links

Lattice gauge theory is a probability measure on link configurations; its entire content is the Haar integral
over links. Both repositories optimize links by gradient descent against a penalty. `grep` over
`MultiAgentELBO/src/` for Haar, partition function, Metropolis, Boltzmann, heat-bath, `β`, string tension, area
law returns zero hits. `MAgent_Model-main` has `nn.Parameter` twists and an autograd penalty — dynamical in the
optimization sense, quenched in the statistical sense. In LGT terms this is the one configuration in which none
of LGT's results hold. Nothing that depends on the measure — confinement, area law, phase structure, the
continuum limit, Fradkin–Shenker — is available, and none of it is available *in principle* at the declared group.

### 3.3 No spacing, no volume, and the wrong base

Every asymptotic statement in LGT lives in `a → 0` or `|Λ| → ∞`. A finite declared agent multigraph has neither
parameter. Worse, the two candidate lattices sit over different bases: the lattice-gauge identification lands on
the **agent interaction multigraph**, which `Theory/02_geometry.tex:562` declares "independently of `C`" and
which carries no refinement index; the roadmap's T8 continuum obligation refines a lattice `Λ_h` over the
**context base `C`**. Even a perfect identification on the agent graph would not touch T8, on base grounds alone.

### 3.4 Free versus discretized links

In LGT the link is the fundamental integration variable. In
`docs/derivations/.../evidence/lattice-continuum-asymptotics.md` the link is `U^h_{xy}`, defined to approximate
parallel transport of a *given* smooth connection, so the `h → 0` statement there is a consistency expansion on a
smooth sequence — which the file itself concedes at `:33-34`. The hard analysis (compactness modulo gauge)
appears only once the link is free.

### 3.5 Matter type

LGT matter is a vector in a linear representation with a fixed invariant inner product. Here matter is a
probability law and the coupling is an asymmetric divergence. The nearest standard comparators — the lattice
nonlinear sigma model and the principal chiral model — both use a fixed target metric and a compact group. The
gauged-bundle diffusion of Cassel et al. (2025) is `SO(d)` with vector-space fibers; the sigma flow of the same
group has a statistical-manifold target but no bundle, no gauge group, no connection, no curvature term.

### 3.6 Flat is not trivial, and the geometry the programme most wants is where this bites

Taken seriously, the identification immediately predicts twisted sectors, and the counterexample survived
skeptical attack and reproduces here exactly. On a `5×5` periodic grid, `K = 3`, with all links the identity
except an `x`-seam `diag(1,−1,−1)` and a `y`-seam `diag(−1,−1,1)` — commuting, so every plaquette holonomy is
exactly `I` — the recomputation gives `max‖H_p − I‖ = 0.0e+00` exactly, plaquette action `0.0`, and
`λ₀ = λ₁ = 0.38196601125011 > 0`. Conversely, with all links random rotations about `z`, plaquette action
`114.7482` and `max‖H_p − I‖ = 2.827`, yet `λ₀ = −1.6e−16` and the section `v_i ≡ e_z` has energy exactly zero.
So `λ₀ = 0` is neither necessary nor sufficient for flatness; the correct criterion is the existence of a
nonzero parallel section, i.e. a common fixed vector of the holonomy group. This is a `'t Hooft` twisted flux
(the pair lifts to anticommuting `SU(2)` elements, so it is a genuine `w₂`), and it lives on exactly the torus
topology that worklog 3h.2 nominates as the setting where the B4 bundle-topology clause becomes testable.

### 3.7 Positive definiteness versus ELBO-derivability

In LGT the plaquette action is manifestly nonnegative. `panelA-T-CURV-derivation.md:323` records that in the
ELBO-derived form the indefinite trace (Killing-type) contribution is forced. ELBO-derivability and positive
definiteness are in tension here, and that tension has no LGT counterpart at compact `G`.

## 4. RETIRED

Conservative list. A false retirement stops work on a real problem, so an item appears here only if it survived
the skeptic. Three items the lenses proposed for retirement were struck and appear in §5 or §6 instead.

**R1. The link kinematics are Wilson (1974) §II.** K. G. Wilson, "Confinement of quarks", *Phys. Rev. D* **10**(8)
(1974) 2445–2459, §II: link variables as discrete parallel transporters on oriented edges with reversal-inverse,
the site-wise gauge law `U_{x,μ} → g_x U_{x,μ} g_{x+μ̂}⁻¹`, the plaquette as the elementary closed loop, and the
trace of the ordered loop product as the gauge-invariant observable. Everything in
`Theory/02_geometry.tex` `def:geo-graph-links` and `sec:geo-regime-two` is that structure.
*Residual scope, corrected against the skeptic:* the citation gap is **one file**, not a corpus-wide defect.
`PIFB2.tex:380` already cites `WilsonConfinement1974, KogutSusskind1975, Creutz1983` for the link variable and
`PIFB2.tex:385` cites Wilson Eq. 12 and Creutz ch. 5 Eq. 5.1 for the gauge law; `references.bib` carries the
entries; the vault page `Lattice gauge theory.md` (created 2026-06-18) carries the whole identification.
`grep` over `Theory/*.tex` returns Wilson/Creutz/Kogut hits in `PIFB2.tex` only. Add the cross-reference to
`Theory/02_geometry.tex sec:geo-regime-two` and the matter is closed.

**R2. `prop:geo-trivializing-criterion` and `trivialization_via_spanning_tree` are maximal-tree gauge fixing.**
Primary source, corrected: M. Creutz, "Gauge fixing, the transfer matrix, and confinement on a lattice",
*Phys. Rev. D* **15** (1977) 1128, and Creutz, *Quarks, Gluons and Lattices* (CUP 1983) ch. 5 — given a maximal
tree, any lattice gauge field can be gauge-transformed so all tree links equal 1, uniquely up to constant gauge
transformations. **The `lgt-identification` lens cited `hep-lat/0203014` for this; that is wrong.** That paper is
David H. Adams, "Gauge fixing, families index theory, and topological features of the space of lattice gauge
fields", whose subject is families index theory for the overlap Dirac operator; the maximal-tree remark appears
only in an acknowledgment added in the v2 revision. Do not cite it. The discrete flat-bundle half should be cited
to Gao et al. (2021), which identifies graph synchronization with trivialization of a flat principal bundle;
**Kobayashi–Nomizu I Ch. II §9 is a smooth-manifold statement and does not treat graphs** — the lens's citation
there is also wrong.

**R3. `λ₀` of the graph connection Laplacian as a coherence order parameter is the frustration constant of `O(d)`
synchronization.** A. S. Bandeira, A. Singer, D. A. Spielman, "A Cheeger inequality for the graph connection
Laplacian", *SIAM J. Matrix Anal. Appl.* **34**(4) (2013) 1611–1630. Exact statement of what BSS prove, checked
against the paper rather than paraphrased: they define the `O(d)` frustration constant as a minimum over group
potentials `g: V → O(d)` of `ν(g) = (1/2d)(1/vol) Σ w_ij ‖g_i − ρ_ij g_j‖²_F`, prove a Cheeger-type inequality
relating it to the connection-Laplacian spectrum, and state the nullspace direction **one way only**: if a
consistent group potential exists then `d` orthogonal vectors annihilate the form. BSS's "consistency" is the
coboundary condition `ρ_ij = g_i g_j⁻¹`, i.e. flatness. **They do not prove the converse, and the converse is
false** (§3.6). Cite BSS for the frustration/spectral relationship; cite Singer & Wu (2012) and Gao et al. (2021)
for the nullspace/holonomy characterization. What is retired is the *novelty* of using `λ₀` as the order
parameter, not the specific claim 3h.3 made about it, which is refuted outright.

**R4. Worklog 3h.2's homology bookkeeping.** That a square lattice's elementary 2-cells are squares, that filling
them kills `H₁` on an open grid, and that `H₁ = 2` survives on the torus, is the ordinary cell structure of the
square lattice and the ordinary `H₁` of `T²`. Standard cellular homology (Hatcher, *Algebraic Topology*, §2.2).
That rank `H₁` depends on which 2-cells are attached is the *definition* of cellular homology, not a discovery;
and lattice gauge theory on irregular complexes is not new (Christ, Friedberg & Lee 1982). The programme's own
manuscript already records the modeling point at
`Research/manuscripts/magent_elbo_whitepaper/02_bundle_geometry.tex:229` and `08_information_geometry_gauge.tex:177`
("Discrete curvature additionally requires declared two-cells or plaquettes").

**R5. The `h^{d−4}` plaquette weight and the `½h⁴‖F‖²` plaquette expansion.** Wilson 1974 §II, reproduced in
Chatterjee, "Yang–Mills for probabilists" (arXiv:1803.01950) §3 including the `ε^{4−n}` exponent:
`Re Tr(I − U_p) = −½ε⁴ Tr(F_jk²) + O(ε⁵)`, hence `S(U) ≈ (ε^{4−n}/4) S_YM(A)`. Recomputed:
`(K − Re Tr H_p)/(½h⁴‖F‖²_F) = 1.0232, 0.9759, 0.9791, 0.9874, 0.9931` at `h = 0.2, 0.1, 0.05, 0.025, 0.0125`.
`docs/derivations/.../lattice-continuum-asymptotics.md` must cite this and claim no novelty for the exponents.
Its own honesty line ("consistency expansions on smooth sequences, not Γ-convergence proofs") is correct and
should stay.

**R6. The softmin/Gibbs-envelope bound on a normalized recognition row.** The `plaquette-elbo` lens listed this as
genuinely new with the words "I found no statement of this anywhere in the corpus". It is in the corpus, with the
same proof, in a strictly stronger form, at `docs/audits/roadmap-review-2026-08-12/rm-02-existence-analysis.md:358`:
`0 ≤ Φ_τ(D) ≤ min_j(D_j + τ log(1/π_j))`, with the functional written at `:18`. The diagonal-self-source
consequence is rm-02's finding **D-5** at `:691` and `:402-408` verbatim: "with a diagonal entry it is uniformly
bounded, contributing zero coercivity and no consensus pressure." The underlying algebra is already classified as
textbook by the programme's own prior-art audit at `rm-06-prior-art.md:242-244` ("textbook entropic
regularisation / Sinkhorn / soft-min"), and independently is Boyd & Vandenberghe §3.1.5. This is exactly the
rediscovery failure mode `rm-06` and `wave2-06` have caught twice before, and it recurred inside a report whose
brief was to prevent it.

**R7. The Higgs/confinement phase-structure question, on narrowed grounds.** Fradkin & Shenker, *Phys. Rev. D*
**19** (1979) 3682. Retire it because `G ≤ GL(K,ℝ)` is noncompact and the matter is a probability law with no
fixed magnitude and no fundamental-representation structure — **not** on the grounds that "there is no measure to
have a phase diagram". That third leg is struck: `rm-06-prior-art.md` T9 charters an optional Gibbs completion
whose "only content is proving `0 < Z < ∞` for this action". The measure is chartered, not categorically absent.
*Verification note:* the primary-source characterization of Fradkin–Shenker could not be confirmed against APS
(HTTP 403). Recorded as unverified, not disputed.

## 5. NARROWED

**N1. T8's continuum limit — the LGT framing is retired, the theorem obligation is not.**
LGT's continuum limit is a *critical* limit of *measures* at a *running* coupling: Chatterjee arXiv:1803.01950 §5,
verbatim — "It is believed that in dimension four ... many of the non-Abelian lattice models of interest have
`β_c = ∞`. That is, one needs to take `β → ∞` while sending the lattice spacing `ε → 0`." T8 wants Γ-convergence
of a deterministic functional at fixed coefficients, whose payoff is convergence of minimizers. Different objects.
Further, the rigorous LGT side is far weaker than the dispatch assumed: Balaban proved *ultraviolet stability*
(subsequential compactness), not construction; Chatterjee §6 closes with "there is yet no construction of a
continuum limit of a lattice gauge theory in any dimension higher than two where Wilson loop variables have been
shown to have nontrivial behavior." So LGT retires nothing on T8 and the roadmap's pricing of T8 as expensive
stands. What must change is only the *comparison*: stop pricing T8 against "LGT has had a continuum limit since
the 1970s."
*Skeptic corrections carried:* the `continuum-limit` lens's claimed bridge — "the only rigorous bridge between
the two registers is Γ-convergence of large-deviation rate functionals (Mariani 2012)" — is not supported. The
arXiv record gives journal ref *Ann. Sc. Norm. Super. Pisa Cl. Sci. (5)* **(2018)**, so "Ann. SNS Pisa 18(3), 2012"
splices a 2018 volume onto a preprint year; and the abstract contains no lattice measure, no Gibbs measure, no
temperature and no `β`. The "only bridge" superlative is false on its face — Γ-convergence of Gibbs free energies
at low temperature is a standing literature (Modica–Mortola 1977; Alberti–Bellettini 1998) and Varadhan's lemma
is a second bridge. The §5 verdict (different limits) is correct; the bridging paragraph decorating it is not.

**N2. `rm-06:277` and `docs/STATUS.md:78` — a survey defect, not a refuted claim.**
Read verbatim, `rm-06:277` says the four enumerated García Trillos–Slepčev-lineage citations are all scalar/`ℝⁿ`
(true of them), and that extending Γ-convergence to manifold-valued graph Dirichlet energies **with a gauge
connection** is real new work. That is a *conjunction*. Canevari & Segatti, *Arch. Ration. Mech. Anal.* **229**
(2018) 125–186 (arXiv:1612.07720), kill the first conjunct only: they prove discrete-to-continuum Γ-convergence
for unit-norm tangent vector fields on a triangulated shell — sections of the unit tangent bundle with the
*induced Levi-Civita* connection on a *fixed* surface, at two scalings, with Poincaré–Hopf charge accounting.
There is no gauge group, no free link variable, and no connection in the functional's argument list.
So: `rm-06:277`'s stated new work is untouched, and the correction owed is to its literature survey. By contrast
`docs/STATUS.md:78`'s stronger phrasing — "García Trillos–Slepčev covers only scalar/`ℝⁿ`. **Nothing exists.**"
— is wrong as written and must be corrected. The `S^{N−1}`/`RP^n` spin-system lineage
(Alicandro–Cicalese–Ponsiglione; Badal–Cicalese–De Luca–Ponsiglione, *CMP* **358**, 2018; arXiv:2010.14280) is a
further decade of the same technology.
*Caveat on the display:* the `E(v) = ½∫|Dv|²` form with `D` the covariant derivative should be pinned to a section
number in the published paper before it is used to overturn a roadmap line; it was read from the preprint.

**N3. Spectral discrete-to-continuum for connection Laplacians exists, but does not cover the roadmap's setting.**
Singer & Wu, "Vector diffusion maps and the connection Laplacian", *CPAM* **65**(8) (2012) 1067–1144, and
"Spectral convergence of the connection Laplacian from random samples", arXiv:1306.1587, prove eigenvalue and
eigenvector convergence of the graph connection Laplacian to the manifold connection Laplacian. **Scope, against
the lens's over-generalization:** the abstract scopes this to connection Laplacians "over the manifold by
considering its principle bundle structure" from i.i.d. random samples — the connection is supplied by the
geometry, not prescribed, and the hypotheses are random sampling plus a kernel bandwidth, not an arbitrary
prescribed `O(d)` connection on an arbitrary graph and emphatically not a lattice `Λ_h` with free links. Cite as a
suggestive base case, not an off-the-shelf theorem. Note also that no roadmap item asserted the negative this was
retiring: `STATUS.md:78` and `rm-06:277` both state a Γ-convergence obligation and say nothing about spectral
convergence.

**N4. Noncompact-target coercivity — the machinery exists and was never searched.**
The claim "every existing manifold-valued discrete-to-continuum Γ-convergence result uses a compact target, and
nothing supplies noncompact equicoercivity" is too strong. The declared fibre `GL(K)/O(K)` is the SPD cone, which
under the affine-invariant metric is Cartan–Hadamard/NPC (Bhatia, *Positive Definite Matrices*, ch. 6), and the
multivariate-Gaussian Fisher–Rao manifold has nonpositive sectional curvature (Skovgaard 1984). Korevaar & Schoen,
*Comm. Anal. Geom.* **1**(3–4) (1993) 561–659, build `W^{1,2}` energy for maps into NPC/metric-space targets
precisely as a limit of *discrete* average difference quotients, and prove compactness and lower semicontinuity
in exactly that noncompact-target setting; Jost's equilibrium-maps line (*Calc. Var.* **2** (1994) 173–204) is the
parallel construction. Honest scope: KS energies are averaged difference quotients over a Riemannian domain, not
a lattice-graph energy, and the result is not stated as a Γ-limit. So this narrows rather than closes — but
"nothing supplies this" is false, and the omission is the same survey failure charged against `rm-06:277`.

**N5. The `d = 2` induced-volume result.** `S_vol[q] = inf_g lim_{h→0} F^base_{h,g}[q]` stays live, but its
novelty is the bookkeeping, not a theorem, and the write-up must say so. "`S_vol` = inf over an auxiliary metric
of a Dirichlet-type form" *is* the Nambu–Goto = `inf_γ` Polyakov statement, which the lens itself concedes is
textbook string theory; and the remaining ingredient — `√det h` concave and 1-homogeneous on the `2×2` PSD cone,
hence the infimum of the linear forms dominating it — is Minkowski's determinant inequality (Horn & Johnson,
*Matrix Analysis*, 2nd ed., Thm 7.8.21) plus the standard concave-conjugate/support-function representation.
Both halves textbook. Separately, 2D Yang–Mills (Driver, Sengupta, Lévy) shares only the symbol `d = 2`: it
constructs a measure for a compact group. Do not cite one for the other.

**N6. Route (a) — heat-kernel plaquette priors — is exact, textbook, and conditional.** For compact `G` on a
planar lattice, independent per-plaquette heat-kernel priors give a normalized law on link configurations with
`Z ≡ 1`; this is the Driver–Sengupta formula for the 2D Yang–Mills measure and the Menotti–Onofri heat-kernel
lattice action, and it is standard mathematics. Three corrections to how the lens stated it. *(i)* Attribution:
the Driver–Sengupta *formula* is attributed in the literature to Sengupta, *Mem. AMS* **126** no. 600 (1997) and
Lévy, *Mem. AMS* **166** no. 790 (2003); Driver, *CMP* **123** (1989) constructs the continuum `YM₂` measure on
the plane via lattice convergence and lassos. Citing Driver 1989 for the i.i.d.-heat-kernel joint law places the
statement in the wrong paper of the pair. *(ii)* The change of variables was justified by a determinant of an
*integer* boundary matrix, which is an abelianized statement and does not establish Haar-preservation on `G^E` for
nonabelian `G`; the correct argument is the standard lasso/tree-gauge triangular substitution, where each step is
a left or right translation and preserves Haar by unimodularity. The Monte Carlo check on `SO(3)` is consistent
with the conclusion, so the conclusion stands and the stated proof does not. *(iii)* It does not satisfy
`Theory/04`'s `prop:gen-exact-normalization`, whose proof is by reverse-topological integration over a directed
design product; it attains `Z ≡ 1` by a third route. And the whole construction is a plane/simply-connected
statement: on the torus the plaquette rows lose exactly one rank (Bianchi) and miss exactly two cycle-space
directions, matching 3h.2's `H₁ = 2`, so two Polyakov-loop priors become part of the model data — and those are
precisely the non-contractible monodromies the proposed torus experiment is meant to probe.

## 6. UNTOUCHED, and what is actually new

### Still open

**U1. Coercivity / Yang–Mills non-definiteness at noncompact `G`** (`overview.md` §7). *Reopened*, having been
claimed closed by worklog 3h.4. The aligned-block argument — holonomy lies in `Stab(q) = O(K−1)`, which is
compact, so `−tr(XY)` is available — does not give a gauge-invariant action, because a definite Ad-invariant form
on the *holonomy* algebra buys nothing unless the *gauge group* is simultaneously reduced. §3.1 measures the
failure. `overview.md:435` already has the correct scoping (the reduction requires `D^ω s = 0`, so a coercive
fixed-inner-product curvature sector and a nonzero base semimetric are mutually exclusive by construction);
3h.4 contradicts it. Withdraw 3h.4.

**U2. The shipped plaquette penalty is gauge-noninvariant under the declared group, on by default.** Not a
research question — a defect. Either reduce the structure group to a compact subgroup for the `R2` sector, or
replace `‖W − I‖²_F` with a conjugacy invariant. Until then no `λ_ym`-dependent result is a statement about the
model rather than about a gauge choice.

**U3. Γ-convergence for a lattice functional of a *free* connection.** Confirmed absent by an arXiv metadata sweep
reproduced here: `all:"Gamma-convergence" AND all:"lattice gauge"` → 0; `abs:"Gamma-convergence" AND
abs:"Yang-Mills"` → 0; `abs:"gauge invariant" AND abs:"Gamma-limit"` → 0. Nearest neighbours are Christiansen &
Halvorsen, "A simplicial gauge theory", *J. Math. Phys.* **53** (2012) 033501 (gauge-invariant discretization plus
consistency, no Γ-limit) and Canevari–Dipasquale–Orlandi, arXiv:2206.03327 (abelian `U(1)`, continuum,
coupling-constant limit, not a mesh limit). **Stated limitation, which must travel with the claim:** arXiv's API
indexes title and abstract only. That is the same method that missed Canevari–Segatti in the corpus survey this
report criticizes, so this negative is provisional and cannot simultaneously ground "confirmed absent" here while
grounding a "refuted" verdict there.

**U4. A discrete/lattice analogue of Uhlenbeck's `L^p`-curvature compactness theorem.** The genuinely expensive
residue of T8 — not "manifold-valued", which is done. Searches found only the continuum theorem (Uhlenbeck,
*CMP* **83** (1982) 31–42; Wehrheim, *Uhlenbeck Compactness*, EMS 2004) and no lattice analogue outside Balaban's
RG-internal estimates. *Provenance:* this is **not new to this pass** —
`docs/research-plans/2026-08-12-continuum-roadmap-review.md:159` already records "A discrete Uhlenbeck gauge-fixing
theorem does not exist", and `docs/audits/panels-2026-08-12/panelA-T-GRAD-derivation.md:444` already enumerates
the full missing list including "equicoercivity modulo gauge with uniform ellipticity `λI ⪯ g^F ⪯ ΛI` on a
declared compact stratum of `Sym₊₊` (the Gaussian fiber fails this as `Σ → 0` or `∞`)". Listing it as a discovery
of this sweep would inflate the yield.

**U5. Whether nontrivial fixed points exist** (`Theory/07b`). LGT contributes nothing: its entire content is link
dynamics under a measure, and there is no measure here.

**U6. Whether holonomy is observable from records.** B4 stands as settled for the connection; it does not bite on
`Ω_ij/Θ_e`, which is an argument of the transported KL. Untouched by anything in this sweep.

### Genuinely new, after the skeptic's deletions

Four of the eight novelty claims raised by the lenses were struck. What survives:

**G1. The matter sector: exact gauge invariance under the full noncompact `GL(K)` from the divergence itself.**
Under `z_i ↦ A_i⁻¹z_i`, `Θ_e ↦ A_i⁻¹Θ_eA_j`, both arguments of `D(q_i ‖ Θ_e# q_j)` are pushed forward by the same
invertible map `A_i⁻¹`, and a divergence is invariant under a common bimeasurable bijection. Standard lattice
matter actions get invariance from compactness plus a fixed inner product; this one does not need either.
**Status corrected from Proven to Standard-with-citation:** the underlying invariance is Kullback & Leibler,
*Ann. Math. Statist.* **22** (1951) 79–86, and the `f`-divergence version is Chentsov/Amari invariance. The
residue that is actually new is the one `rm-06-prior-art.md` T2 already isolated a day earlier: *that
`ρ: G → Diff(M_q)` is a nonlinear, family-preserving action rather than a linear representation.* Per that row's
own instruction — "State it in one proposition, do not write a chapter."

**G2. Gauge covariance forces `W_e` to be a `(0,2)` tensor, and a fixed weight fails.** Verified: with `W = I`,
`(z_i − Θz_j)ᵀW(z_i − Θz_j)` moves `2.1535957634 → 1.6979106789` under random `GL⁺(3)` gauges (rel. dev. 2.1e−1);
with `W = Σ_i⁻¹` transported as `A_i⁻¹Σ_iA_i⁻ᵀ`, invariant to 6.8e−16. `Theory/09_coarsegraining.tex:222` writes
the energy with a general `W_e`, and a reader will assume a fixed weight, which makes the chapter
gauge-noncovariant. That correction is owed. **But do not write "forced":** the uniqueness claim is false.
Executed counterexample — `W_alt = Σ_i⁻¹ + 1.7(Σ_i⁻¹μ_i)(Σ_i⁻¹μ_i)ᵀ` is SPD (eigenvalues 0.1106, 0.2450, 0.4420),
is not proportional to `Σ⁻¹`, and is equally invariant (rel. dev. 8.6e−16). `Σ⁻¹` is singled out by the
second-order KL expansion (`Theory/05c prop:pb-kl-divergence-jets`), not by the gauge argument. Writing "forced"
into `Theory/09` would install a false uniqueness claim.

**G3. Freely declared 2-cells as a modeling knob, stated as a consequence rather than a fact.** The homology is
textbook (R4) and the observation is already in the manuscript. What is not yet followed through is the
consequence: because `InteractionComplex` takes `two_cells` as an independent argument, "how much monodromy
survives" is a *design decision*. Worklog 3h.2 identifies it ("one declares which cycles bound") and stops.

**G4. The twisted-flat sector on the torus as a concrete obstruction to the meta-agent narrative** (§3.6). This is
new *to the programme* — it is standard `'t Hooft` flux in LGT — and it is the sharpest available refutation of
3h.4's framing, because it fires on the exact topology the B4 experiment wants.

### Struck from "genuinely new"

Conjugacy invariants as the "only" admissible route on `GL⁺(K)` — textbook invariant theory (Procesi 1976,
Razmyslov 1974: the ring of invariants of matrix tuples under simultaneous conjugation is generated by traces of
words, i.e. exactly Wilson loops), the "only" clause is false (the spectrum of the non-symmetric
`D ⊗ I − Θ` is exactly gauge-invariant, since `L(Θ') = S⁻¹L(Θ)S` with `S = blockdiag(A_i)`), and the prescription
is already in-repo at `docs/reviews/2026-07-12-belief-inertia-ultradeep-peer-review.md:258` and `PIFB2.tex:408`.
The softmin envelope bound (R6). The compact-vs-`GL(K)` "correct mechanism" (Milnor + Yau, both textbook, and not
the binding constraint — §3.1). And the headline framing that the LGT identification is itself a discovery: the
vault page `Lattice gauge theory.md` has carried it since 2026-06-18, and worklog 3h.1 says so directly
("Non-flat edge variables are therefore not new construction").

## 7. The plaquette ELBO question: derived or engineered

**The curvature term as implemented is ENGINEERED.** `Theory/05_elbo.tex:220` fixes `θ` before the ELBO is
defined, and `prop:elbo-subspace-support-singular` (`:139-147`) gives `KL = +∞` for a Dirac recognition law on a
Lebesgue-dominated posterior. So a learned point value `Θ̂` plus an added `λ_ym‖W(Θ̂) − I‖²_F` is penalized MAP,
not an ELBO component. That is exactly what `MAgent_Model-main` runs: `nn.Parameter` twists, a Frobenius penalty,
a free coefficient `λ_ym = 0.1`. It must not be described as ELBO-derived.

**A different curvature term is DERIVED, under stated hypotheses, and it is not the one being used.** The
lagged self-source route — setting `Ω_aa := H_P` in the tied-replica belief-relational block — is type-admissible
and gives the exact energy `D_KL(q_a ‖ (H_P)_# q_a^n)`, which expands as
`½h⁴‖F_{μν}(c).q‖²_{g^F(q)} + O(h⁵)` (`worklog:2036-2037`; note the `h⁴`, which the `plaquette-elbo` lens dropped
and which any comparison against 3h.3's fitted constant `c = 0.00705` would have to carry). Hypotheses: `Θ`
history-fixed, source-label block typing, the small-`h` expansion. This is Fisher-weighted and state-dependent,
**not** `‖F‖²_F`, and the corpus says so at `:2061` — "complementary to the classical Wilson action, not a
generalization of it."

**The two are not proportional, and the derived one vanishes where the fitted law was measured.** Recomputed:
for `K = 3` centred Gaussians with isotropic `S = I` and a skew generator, `D_KL(N(0,S) ‖ N(0,HSHᵀ))` is
`−5.6e−17, 1.1e−16, −1.1e−16` at `h = 0.2, 0.1, 0.05` — identically zero to machine precision — while the same
`S` with a symmetric generator gives `7.320e−02, 1.879e−02, 4.770e−03` (ratio → 4, quadratic), and anisotropic
`S = diag(1, 0.35, 2.5)` with the skew generator gives `7.413e−02, 1.904e−02, 4.809e−03`. Worklog 3h.3 fitted
`λ₀ = c Σ_plaq‖F‖²` against the **bare** form at `G = SO(3)` — precisely the configuration where the derived
energy supplies zero gradient. The chain "descend `F` ⟹ descend the plaquette action ⟹ `λ₀ → 0`" is broken at its
first link.

**So 3h.5's question stays OPEN, and the `plaquette-elbo` lens's instruction to close it as corpus drift is
rejected.** `worklog:1811` pins the referent — "`λ₀` here is the bottom of the **bare** energy form" — and §4.2 of
the same file answers a different question for the dressed energy while explicitly disclaiming the bare `‖F‖²`.
The lens's own F7 (functional mismatch) proves this; F7 and its F10 cannot both be right. Closing the item would
stop work on a live question.

Additional constraints on any future answer. Even the route (a) heat-kernel construction (N6) is a *generative*
statement: `−log ∏_p p_t(U_p)` is a normalized prior, and a prior enters `E_Q[log p − log q]` only if `Θ` carries a
non-degenerate recognition law `q(Θ)` on `G`. I grepped for such a declaration and found none. So the honest
status of route (a) is "answered conditionally on a declaration not yet made", not retired. And under route (c),
minimizing `F` over `q(Θ)` drives the *belief about* curvature to its posterior, not the curvature to zero: the
unit-coefficient entropy holds `q` spread over the prior's support. Zero curvature minimizes the plaquette block
in isolation at a point mass — the branch excluded above. Under route (b), `Θ` is history-fixed
(`typed-construction.md:37-54`) and there is no `Θ`-descent at all.

One further caution, and it is the reason `λ_ym` cannot simply be reinterpreted as a derived coupling. The softmin
envelope does **not** make the plaquette sector non-extensive, contrary to the claim it was offered for. With one
row per agent over its four incident plaquettes, all at energy 5, the total is `20, 80, 320, 1280, 5120` for
`4, 16, 64, 256, 1024` agents — fully extensive in lattice volume. And with all 16 plaquettes at a common energy
`a` under a uniform row, the optimized block equals `a` exactly (ratio `1.000000` at `a = 0.5, 2, 5, 20, 200`);
the reported saturation at `log 16` was an artifact of hard-coding one plaquette at exactly zero energy, and the
bound `min_P E_P + log(1/π_min)` bounds nothing absolute because `min_P E_P` is itself unbounded. What survives is
only rm-02's D-5: the block is insensitive to every plaquette but the flattest **in its own row**.

## 8. Adjudication record

| Lens | Skeptic verdict | Governing outcome |
|---|---|---|
| `lgt-identification` | broke it (`verdict holds: false`) | Live link sector confirmed in `MAgent_Model-main`; "no action, no dynamics, path unreachable" struck. Four of five novelty claims struck. Three citations wrong. |
| `continuum-limit` | held (`verdict holds: true`) | Core verdict stands. `rm-06:277` demoted from Refuted to survey defect; `STATUS.md:78` still wrong. Mariani and BSS citations struck; Singer–Wu scope narrowed; F9's proof invalid though its conclusion survives. |
| `plaquette-elbo` | broke it (`verdict holds: false`) | Headline novelty refuted verbatim from `rm-02:358`; extensivity claim refuted by computation; F10's "report drift, do not re-open" rejected as a false retirement contradicted by the lens's own F7. |

Verification note for the ledger: `.verification/ledger.json` remains pinned at `git:d892374` with eight claims,
seven HIGH, none verified. Drift reported; not re-pinned.

## 9. Citations owed

```bibtex
@article{WilsonConfinement1974,
  author  = {Wilson, Kenneth G.},
  title   = {Confinement of quarks},
  journal = {Physical Review D},
  volume  = {10},
  number  = {8},
  pages   = {2445--2459},
  year    = {1974},
  doi     = {10.1103/PhysRevD.10.2445},
  note    = {Section II: link variables, gauge law, plaquette, Wilson loop.
             Already in references.bib; the residual gap is the cross-reference
             from Theory/02_geometry.tex sec:geo-regime-two.}
}

@book{Creutz1983,
  author    = {Creutz, Michael},
  title     = {Quarks, Gluons and Lattices},
  publisher = {Cambridge University Press},
  year      = {1983},
  note      = {Ch. 5: gauge law Eq. 5.1; maximal-tree gauge fixing.}
}

@article{Creutz1977GaugeFixing,
  author  = {Creutz, Michael},
  title   = {Gauge fixing, the transfer matrix, and confinement on a lattice},
  journal = {Physical Review D},
  volume  = {15},
  pages   = {1128},
  year    = {1977},
  doi     = {10.1103/PhysRevD.15.1128},
  note    = {Correct primary source for maximal-tree gauge fixing.
             REPLACES the erroneous hep-lat/0203014 attribution.}
}

@article{BandeiraSingerSpielman2013,
  author  = {Bandeira, Afonso S. and Singer, Amit and Spielman, Daniel A.},
  title   = {A {C}heeger inequality for the graph connection {L}aplacian},
  journal = {SIAM Journal on Matrix Analysis and Applications},
  volume  = {34},
  number  = {4},
  pages   = {1611--1630},
  year    = {2013},
  eprint  = {1204.3873},
  note    = {Cite for the frustration/spectral relationship ONLY.
             BSS prove consistency => lambda = 0, not the converse.}
}

@article{SingerWu2012VDM,
  author  = {Singer, Amit and Wu, Hau-Tieng},
  title   = {Vector diffusion maps and the connection {L}aplacian},
  journal = {Communications on Pure and Applied Mathematics},
  volume  = {65},
  number  = {8},
  pages   = {1067--1144},
  year    = {2012},
  note    = {With arXiv:1306.1587 for spectral convergence.
             Scope: connection induced by the manifold's principal-bundle
             structure, i.i.d. samples -- not an arbitrary prescribed connection.}
}

@article{CanevariSegatti2018,
  author  = {Canevari, Giacomo and Segatti, Antonio},
  title   = {Defects in Nematic Shells: a $\Gamma$-convergence discrete-to-continuum approach},
  journal = {Archive for Rational Mechanics and Analysis},
  volume  = {229},
  pages   = {125--186},
  year    = {2018},
  doi     = {10.1007/s00205-017-1215-z},
  eprint  = {1612.07720},
  note    = {Manifold-valued discrete-to-continuum Gamma-convergence on a
             nontrivial bundle. Induced Levi-Civita connection, fixed surface,
             no gauge group -- narrows rm-06:277, does not refute it.}
}

@article{KorevaarSchoen1993,
  author  = {Korevaar, Nicholas J. and Schoen, Richard M.},
  title   = {Sobolev spaces and harmonic maps for metric space targets},
  journal = {Communications in Analysis and Geometry},
  volume  = {1},
  number  = {3-4},
  pages   = {561--659},
  year    = {1993},
  note    = {Noncompact/NPC-target energy from discrete difference quotients,
             with compactness and lower semicontinuity. Relevant to the SPD fibre.}
}

@article{Milnor1976,
  author  = {Milnor, John},
  title   = {Curvatures of left invariant metrics on {L}ie groups},
  journal = {Advances in Mathematics},
  volume  = {21},
  pages   = {293--329},
  year    = {1976},
  note    = {Lemma 7.5: a CONNECTED Lie group admits a bi-invariant metric iff
             it is compact x vector group. Applies to GL+(K,R).}
}

@article{Procesi1976,
  author  = {Procesi, Claudio},
  title   = {The invariant theory of $n \times n$ matrices},
  journal = {Advances in Mathematics},
  volume  = {19},
  pages   = {306--381},
  year    = {1976},
  note    = {With Razmyslov (1974). Invariants of matrix tuples under simultaneous
             conjugation are generated by traces of words = Wilson loops.
             Retires the "conjugacy invariants" novelty claim.}
}

@article{MenottiOnofri1981,
  author  = {Menotti, Pietro and Onofri, Enrico},
  title   = {The action of {SU}({N}) lattice gauge theory in terms of the
             heat kernel on the group manifold},
  journal = {Nuclear Physics B},
  volume  = {190},
  pages   = {288--300},
  year    = {1981}
}

@article{Sengupta1997,
  author  = {Sengupta, Ambar},
  title   = {Gauge theory on compact surfaces},
  journal = {Memoirs of the American Mathematical Society},
  volume  = {126},
  number  = {600},
  year    = {1997},
  note    = {With Levy, Mem. AMS 166 no. 790 (2003): correct source for the
             Driver-Sengupta formula. Driver CMP 123 (1989) constructs the
             continuum YM_2 measure on the plane and is a DIFFERENT statement.}
}

@article{Driver1989,
  author  = {Driver, Bruce K.},
  title   = {{YM}$_2$: continuum expectations, lattice convergence, and lassos},
  journal = {Communications in Mathematical Physics},
  volume  = {123},
  pages   = {575--616},
  year    = {1989}
}

@article{FradkinShenker1979,
  author  = {Fradkin, Eduardo and Shenker, Stephen H.},
  title   = {Phase diagrams of lattice gauge theories with {H}iggs fields},
  journal = {Physical Review D},
  volume  = {19},
  pages   = {3682--3697},
  year    = {1979},
  note    = {Cited to CLOSE the phase-structure line: compact G, fundamental
             fixed-magnitude Higgs. Characterization not verified against the
             primary source (APS returned HTTP 403).}
}

@article{ChatterjeeYMProbabilists2018,
  author  = {Chatterjee, Sourav},
  title   = {Yang--{M}ills for probabilists},
  eprint  = {1803.01950},
  year    = {2018},
  note    = {Sec. 3 for the eps^{4-n} Wilson weight; Sec. 5 for the critical
             continuum limit and beta_c = infinity in 4D; Sec. 6 for Balaban
             (UV stability, not construction) and the "no construction above
             two dimensions" assessment.}
}

@article{Uhlenbeck1982,
  author  = {Uhlenbeck, Karen K.},
  title   = {Connections with $L^p$ bounds on curvature},
  journal = {Communications in Mathematical Physics},
  volume  = {83},
  pages   = {31--42},
  year    = {1982},
  note    = {The continuum theorem. NO lattice analogue exists; that gap is U4.}
}

@article{ChristFriedbergLee1982,
  author  = {Christ, Norman H. and Friedberg, Richard and Lee, T. D.},
  title   = {Random lattice field theory},
  journal = {Nuclear Physics B},
  volume  = {202},
  pages   = {89--125},
  year    = {1982},
  note    = {Lattice gauge theory on irregular complexes. Retires the novelty
             of "general multigraph" as such.}
}

@article{KullbackLeibler1951,
  author  = {Kullback, S. and Leibler, R. A.},
  title   = {On information and sufficiency},
  journal = {Annals of Mathematical Statistics},
  volume  = {22},
  pages   = {79--86},
  year    = {1951},
  note    = {Invariance of KL under a common invertible pushforward. Downgrades
             the transported-KL gauge-invariance claim from Proven to
             Standard-with-citation.}
}

@article{ChristiansenHalvorsen2012,
  author  = {Christiansen, Snorre H. and Halvorsen, Tore G.},
  title   = {A simplicial gauge theory},
  journal = {Journal of Mathematical Physics},
  volume  = {53},
  pages   = {033501},
  year    = {2012},
  eprint  = {1006.2059},
  note    = {Nearest neighbour to U3: gauge-invariant discretization with
             consistency analysis, no Gamma-limit.}
}

@book{BoydVandenberghe2004,
  author    = {Boyd, Stephen and Vandenberghe, Lieven},
  title     = {Convex Optimization},
  publisher = {Cambridge University Press},
  year      = {2004},
  note      = {Sec. 3.1.5: max_i x_i <= log sum_i e^{x_i} <= max_i x_i + log n.
               The softmin envelope bound is this.}
}

@article{DonskerVaradhan1975,
  author  = {Donsker, M. D. and Varadhan, S. R. S.},
  title   = {Asymptotic evaluation of certain {M}arkov process expectations
             for large time},
  journal = {Communications on Pure and Applied Mathematics},
  year    = {1975},
  note    = {Correct primary for min_q {E_q[E] + KL(q||pi)} = -log sum pi e^{-E};
             or Dupuis & Ellis (1997) Prop. 1.4.2. Wainwright & Jordan Sec. 3.6
             is conjugate duality over mean parameters, a different theorem.}
}

@book{Bhatia2007,
  author    = {Bhatia, Rajendra},
  title     = {Positive Definite Matrices},
  publisher = {Princeton University Press},
  year      = {2007},
  note      = {Ch. 6: the SPD cone under the affine-invariant metric is
               Cartan-Hadamard. Relevant to N4.}
}
```

Corrections owed in the corpus, all small: add the Wilson/Creutz cross-reference to
`Theory/02_geometry.tex sec:geo-regime-two`; state the `Θ'_e = (a_i)⁻¹Θ_e a_j` ↔ `U → g_x U g_{x+μ̂}⁻¹`
correspondence there so a reader does not hit an apparent inversion; correct `docs/STATUS.md:78`'s "Nothing
exists"; note in `Theory/09_coarsegraining.tex:222` that `W_e` must transform as a `(0,2)` tensor and that a fixed
weight is gauge-noncovariant, without writing "forced"; withdraw worklog 3h.4; and fix the shipped `R2` sector or
scope every `λ_ym` result as gauge-dependent.
