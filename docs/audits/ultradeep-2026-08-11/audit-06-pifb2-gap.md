# Audit 06 — PIFB2 → Theory/ Gap Analysis

**Role:** referee gap analysis between the stated goal ("a rigorous version of PIFB2.tex — agents as
local sections of associated bundles with statistical manifold fibers to a noumenal principal
G-bundle evolving under a local/global variational free energy") and the current state of
`MultiAgentELBO/Theory/`.

**Corpora read.**
- Target: `C:\Users\chris and christine\Desktop\Research\manuscripts\PIFB2.tex` (3956 lines).
- Development: `C:\Users\chris and christine\Desktop\MultiAgentELBO\Theory\*.tex` (16,821 lines,
  20 chapters + 3 appendices), `Theory\SPEC.md` (54 KB), `Theory\appendix_claim_ledger.tex`.
- Cross-refs: `Research\manuscripts\magent_elbo_whitepaper\09_pifb2_crosswalk.tex`,
  `MultiAgentELBO\references.bib`, `Research\wiki\`.

**Status-tag census** (my search: `grep -oh '\status{[A-Z-]*}' Theory/*.tex | sort | uniq -c`):
501 ESTABLISHED, 137 DEFINITION, 75 OPEN, 60 HYPOTHESIS, 58 NOT-CLAIMED, 13 NUMERICAL,
3 CONJECTURE. This is an unusually disciplined manuscript. The problem is not honesty. The problem
is *what* it has chosen to be rigorous about.

---

## 0. Executive verdict

`Theory/` is **not** a rigorous version of PIFB2. It is a rigorous version of a *different, adjacent*
theory that shares PIFB2's vocabulary. Specifically:

1. The central object of the goal sentence — a free energy functional **on the space of sections**
   of an associated bundle — **does not exist anywhere in `Theory/`**. The bundle layer
   (Ch. 2) and the variational layer (Ch. 3–5) are separated by a deliberate **type wall**, and the
   only bridge across it is `hyp:prob-sampling-compatibility`
   (`Theory/03_probability.tex:436`, `\status{HYPOTHESIS}`), which the manuscript **itself proves is
   non-identifying in both directions** (`prop:prob-compatibility-nonidentifiability`,
   `03_probability.tex:420`, `\status{ESTABLISHED}`).
2. Consequently "agents evolve under a local/global VFE" is proved for agents-as-*indices*
   (`Theory/05b_local_collective_elbo.tex`, finite set `V` over a standard Borel context space
   `(X, 𝒳)`), **not** for agents-as-*sections*.
3. The corpus has ~2 chapters' worth of genuinely new, publishable mathematics
   (`05c_pullback_geometry.tex`, `05b_local_collective_elbo.tex`) and ~10 chapters' worth of RG
   machinery whose connection to the bundle program is thin.
4. It cites **zero** Friston, zero Parr, zero Da Costa, zero Ramstead, zero Sakthivadivel, zero
   Sengupta, zero Cohen/Weiler/Bronstein, zero Wilson, zero Vaswani. This is a fatal positioning
   defect at any venue that would care about this program.

The shortest path to publication is **not** to finish PIFB2. It is to extract the one theorem
`Theory/` already almost has — *gauge-covariant informational pullback geometry with an exact
horizontal-defect cocycle* — and publish that, with the bundle-to-ELBO bridge repaired.

---

## 1. Coverage map: PIFB2 construction → Theory/ status

Legend: **P&P** present & proved · **P-OPEN** present but the key step is OPEN/HYPOTHESIS ·
**WEAKER** present in a strictly weaker form · **ABSENT** (search stated) · **EXCL** deliberately
excluded by SPEC.md.

| # | PIFB2 construction (PIFB2.tex line) | Theory/ counterpart (file:line, label) | Status |
|---|---|---|---|
| 1 | Base manifold `𝒞` as index/context space, no intrinsic geometry, "domain of inquiry not a thing" (`PIFB2.tex:144`, `def:base_manifold`) | `02_geometry.tex:16` `def:geo-context-base` — finite-dim smooth second-countable Hausdorff manifold; explicitly *not* the population index set, not the interaction graph, not spacetime; "fixed and timeless" (`02_geometry.tex:20-33`) | **P&P** — stronger and cleaner than PIFB2 |
| 2 | Statistical manifolds as fibers `ℬ_state`, `ℬ_model`, Gaussian, Fisher–Rao (`PIFB2.tex:155`) | `02_geometry.tex:67-78` law fibers `ℬ_b ⊆ 𝒫(K)`, `ℬ_m ⊆ 𝒫(M)`; upgraded to statistical manifolds only under `hyp:geo-smooth-tier` (`02_geometry.tex:103`, HYPOTHESIS); Gaussian is a *declared realization* (`06_gaussian.tex:4`) | **P&P**, correctly weakened |
| 3 | Fisher metric descends to fiber; `ρ(g)` acts by isometry (`PIFB2.tex:212-230`) | `05c_pullback_geometry.tex:59` `prop:pb-statistical-tensor-descent` — Fisher **and** Amari–Chentsov tensors descend to *vertical* tensors on `𝓔_x = P ×_{ρ̂_x} ℬ_x`; load-bearing hypothesis: the `G`-action is a parameter-independent bimeasurable sample-coordinate change (`05c:84-87`) | **P&P** — this is *better* than PIFB2 and is a real result |
| 4 | Principal `G`-bundle `π: 𝒩 → 𝒞` (`PIFB2.tex:189`) | `02_geometry.tex:40` `def:geo-principal-systems`, `π: P → 𝒞`, smooth principal right `G`-bundle for a Lie group `G` | **P&P** |
| 5 | Associated bundles `𝓔 = 𝒩 ×_ρ ℬ` (`PIFB2.tex:212`) | `02_geometry.tex:120` `def:geo-associated-bundles`, `𝓔_b = P ×_{ρ̂_b} ℬ_b`, `𝓔_m = P ×_{ρ̂_m} ℬ_m`, quotient convention `eq:geo-quotient-convention` | **P&P** |
| 6 | Agent = smooth section of associated bundles (`PIFB2.tex:231`, `def:Agent`) | `02_geometry.tex:403` `def:geo-agent`: `𝒜^i = (𝒞_i; q_i, s_i, u_i^b, u_i^m)` with `q_i ∈ Γ(𝒞_i, 𝓔_b\|_{𝒞_i})` | **P&P as a definition; DEAD as a variational object** — see §2 |
| 7 | Gauge frame `φ_i: 𝒰_i → 𝔤`, transport `Ω_ij = exp(φ_i)exp(−φ_j)` (`PIFB2.tex:301`, `eq:transport_def`) | Two *distinct* objects, deliberately not conflated: (a) principal-frame sections `u_i^b, u_i^m` and unique relative field `h_i` with `u_i^m = u_i^b · h_i` (`02_geometry.tex:57-65`, ESTABLISHED); (b) independently declared **graph links** `Θ^b_e, Θ^m_e` (`02_geometry.tex:562` `def:geo-graph-links`) | **WEAKER + BETTER** — PIFB2 conflates transport with cocycle; Theory separates them and makes the identification an OPEN obligation (`appendix_claim_ledger.tex:~261` "Graph-to-base identification (open)") |
| 8 | Regime I / Regime II connection split, Maurer–Cartan `F=0` (`PIFB2.tex:136` conv., `sec:connection_forms`) | `02_geometry.tex:279` `def:geo-connections`: two independent principal connections `ω_b, ω_m ∈ Ω¹(P, 𝔤)`, no pure-gauge restriction; difference descends to an `Ad(P)`-valued 1-form | **P&P and stronger** — Theory never restricts to Regime I |
| 9 | Cognitive frames = gauge frames, Role A / Role B (`PIFB2.tex:301`) | Only the passive/active distinction: passive reframing `eq:geo-local-reframing` vs. the single principal gauge group `Aut_G(P)` with `k_i^m = h_i^{-1} k_i^b h_i` (`02_geometry.tex:168-181`) | **WEAKER** — Role B (frame as cognitive state) is gone; correctly so |
| 10 | Five-term VFE functional over `𝒞` (`PIFB2.tex:675`, `eq:free_energy_functional_final`) | **ABSENT as written.** In its place: `𝓕[Q_X; X, o] = −ℒ(Q_X; X)` on a *finite design* `D = {c_a}_{a=1}^M ⊆ 𝒞` (`05_elbo.tex:222`, `03_probability.tex:15`). Search: `grep -n 'int_{\\mathcal C}' Theory/*.tex` returns 11 hits, **all** in `05d_relational_inference.tex` (Fisher lengths/metrics), **none** a free-energy integral | **ABSENT / REPLACED** |
| 11 | Belief coupling `β_ij KL(q_i ‖ Ω_ij q_j)` (`PIFB2.tex:530-660`) | Replaced by normalized interaction kernels `K_a` on hyperedges (`05b:18` `hyp:local-interaction-kernels`, HYPOTHESIS), and Gaussian "interaction family" `06_gaussian.tex:97` `def:gauss-interaction-family` | **WEAKER, correctly** |
| 12 | Softmax attention `β*_ij ∝ π_ij exp(−KL/τ)` derived from mixture-of-sources (`PIFB2.tex:530`, `eq:beta_optimal`) | `05b:547` `prop:obs-attention-elbo`, ESTABLISHED — exact posterior + exact **row softmax** optimum `eq:obs-attention-recognition-optimum` (`05b:579`), from a *latent source label inside the fixed joint*, not a mean-field ansatz | **P&P and stronger** — this is Theory's cleanest improvement over PIFB2 |
| 13 | Attention priors / masking / ALiBi / RoPE (`PIFB2.tex:596`) | ABSENT. Search: `grep -ric 'ALiBi\|RoPE\|positional' Theory/*.tex` → 0 | **EXCL** (SPEC.md:26 "The executable does not appear") |
| 14 | Conditional representation theorem for forward KL / geometric-mean Boltzmann belief (`PIFB2.tex:2956`) | Partially: `09_coarsegraining.tex:639` `prop:cg-gaussian-forward-kl-barycenter` (Gaussian); `06_general_coarsegraining.tex:561` `thm:cg-holonomy-kl-marginal` (holonomy-conditioned weighted forward-KL infimum, path/root/gauge-independent) | **P&P in the Gaussian tier** |
| 15 | State-dependent precision `α_i(c)` + envelope theorem + reduced free energy (`PIFB2.tex:735-875`) | ABSENT. Search: `grep -ric 'envelope' Theory/*.tex` → 1 hit, `05d_relational_inference.tex`, unrelated. No `α_i` precision sector, no log-barrier | **ABSENT** |
| 16 | Environmental agents / observations as agent–agent couplings (`PIFB2.tex:877`) | `05b:716` `def:obs-operational-environment-node` + `05b:721` `thm:obs-agent-interaction-equivalence`, ESTABLISHED | **P&P** |
| 17 | Timescale hierarchy `η_q : η_s : η_φ ~ 1 : ε : ε²`, adiabatic/Born–Oppenheimer (`PIFB2.tex:929`) | **ABSENT.** Searches: `grep -ric 'timescale\|time-scale\|adiabatic\|fast subsystem' Theory/*.tex` → 0 for all four; `slow` → 1 hit in `07_general_renormalization.tex` (unrelated) | **ABSENT** |
| 18 | Natural-gradient dynamics on `ℝ^K × 𝕊⁺ × G`, dexp regularity, retraction (`PIFB2.tex:965`, `prop:dexp_regularity`) | Only the *finite-dimensional block* version: `05b:668-694` `sec:local-natural-gradient` — `η̇_i = −γ_i G_i^{-1} ∇_{η_i}F`, `dF/dt ≤ 0` (`eq:obs-global-dissipation`), ESTABLISHED, but explicitly requires block-diagonal Fisher metric (`05b:696-700` "Block orthogonality is load bearing"). No group sector, no retraction, no dexp | **WEAKER** |
| 19 | Transformer recovery (`PIFB2.tex:1006-1300`, `thm:transformer_recovery`) | **ABSENT.** Searches on `Theory/*.tex`: `transformer` → 0, `query` → 0, `multi-head` → 0, `WikiText` → 0, `GPT` → 0. `softmax` → 6 (variational, not QKV); `attention` → 67 (variational source label) | **EXCL** (SPEC.md:19-22) |
| 20 | WikiText-103 aggregate dimension sweep, `b = −1.048919` (`PIFB2.tex:1304`) | **ABSENT.** `appendix_numerical_provenance.tex` (150 lines) contains only deterministic replacement checks e.g. `CHK-GAUSS-CONDITIONING` (`06_gaussian.tex:351`, `\status{NUMERICAL}`) | **EXCL** |
| 21 | Mass / stiffness / second variation / velocity-quadratic metric (`PIFB2.tex:1325-1530`) | **ABSENT.** Searches: `stiffness` → 0, `mass matrix` → 0. `mass` (~20 hits) is always measure-theoretic ("total mass", "evidence mass `M_ℓ`") or "mass pencil" (`10_renormalization.tex:368`, a generalized-eigenvalue object) | **ABSENT / EXCL** |
| 22 | Meta-agent as gauge-covariant variational barycenter (`PIFB2.tex:1537`, `eq:meta_agent_barycenter`, `prop:barycenter_existence`) | Two partial counterparts: `09_coarsegraining.tex:639` `prop:cg-gaussian-forward-kl-barycenter` + `:700` `cor:cg-compact-holonomy-barycenter` (ESTABLISHED, but **compact-closure holonomy only**); and the primary definition, which is *not* a barycenter at all: a meta-agent is **just a block `B ⊆ V`** (`05b:189-194`, `05b:306-308`) | **WEAKER** — the *definitional* meta-agent lost its bundle content |
| 23 | Free-energy improvement licensing criterion + threshold detector (`PIFB2.tex:1590-1616`) | **ABSENT.** Searches: `free energy improvement` → 0; `detector` → 2 hits (`06_general_coarsegraining.tex`, unrelated usage) | **ABSENT** |
| 24 | Cross-scale shadow priors `p_i^{(s)} = Ω_{i,I}[q_I^{(s+1)}]` (`PIFB2.tex:1662`, `eq:cross_scale_shadow`) | **ABSENT as a construction.** Nearest: the levelwise geometric RG state `07_general_renormalization.tex:153` `def:rg-geometric-state`, which builds `𝒞_ℓ`, `G_ℓ`, `𝒫_ℓ → 𝒞_ℓ` per level but supplies **no downward prior-assignment rule** | **ABSENT** |
| 25 | RG spine / parametric form preservation across scales (`PIFB2.tex:1679`) | Extensively developed and **substantially harder** than PIFB2's: `07_general_renormalization.tex` + `07b_agent_network_rg.tex` (2828 lines). Key results: `thm:rg-exact-coarse-vfe` (`07b:34`), `thm:rg-effective-action` (`07b:112`), `thm:rg-fixed-point-equations` (`07b:2489`), `thm:rg-complete-effective-theory` (`07b:2735`) | **P&P, far beyond PIFB2** |
| 26 | Coarse-grained *bundle* over a coarser base | `07_general_renormalization.tex:249-285`: base coarsening `c_ℓ: 𝒞_ℓ → 𝒞_{ℓ+1}`, group hom `κ_ℓ`, equivariant `𝒫_ℓ` with `𝒫_ℓ(p·g) = 𝒫_ℓ(p)·κ_ℓ(g)`, associated scale map `C_{ℓ,s}[p,z] = [𝒫_ℓ(p), q_{ℓ,s}(z)]`; **existence is a genuine topological iff-condition** (`07:258-266`, Hopf-bundle failure witness) | **P&P — the single best thing in the corpus that PIFB2 lacks entirely** |
| 27 | Descent of a fine section to a coarse section | `05c_pullback_geometry.tex:677-688`: `Ψ∘s` is only a section of the pullback `f*Ē`; descent is `\status{HYPOTHESIS}` (`eq:pb-coarse-related-sections`). `cor:pb-meta-perceived-geometry` (`05c:1172`) is conditional on it | **P-OPEN** — correctly flagged |
| 28 | Ouroboros tower, apex closure, multi-generation discount (`PIFB2.tex:1703`, `eq:ouroboros_F`) | **EXCL** (SPEC.md:19-22 names "the Ouroboros tower" as out of scope). Residual: `11_obstructions.tex:239` `prop:obs-declared-root-unavoidable` — *the tower cannot self-close; the apex prior cannot be derived*. This is a rigorous **refutation** of apex closure | **EXCL, and refuted** |
| 29 | Prospective participatory validation protocol (`PIFB2.tex:1732`) | `11_obstructions.tex:247` `sec:obs-participatory` and `12_philosophy.tex:251` `sec:phil-participatory` — the participatory content is retyped as "the inference is observer-indexed", with `Wheeler1990` cited once and immediately disclaimed (`12_philosophy.tex:273-274`) | **WEAKER by design** |
| 30 | Time as information flow / Fisher arc length (`PIFB2.tex:1828`) | `05d_relational_inference.tex` (1624 lines) — Fisher clocks, `thm:hist-fisher-clock-invariance` (`05d:594`), record-clock contraction `thm:hist-record-clock-contraction`, obstruction to a global unit clock (`eq:hist-nonexact-clock-example`). Physical-time identification is `\status{OPEN}` (`appendix_claim_ledger.tex:~290`) | **P&P (as pure math) + OPEN (as physics)** |
| 31 | It From Bit pullback: information geometry → base geometry (`PIFB2.tex:1867`) | `05c_pullback_geometry.tex:109` `def:pb-informational-pullbacks` + `:124` `thm:pb-pullback-gauge-invariance` (passive gauge covariance) + `:321` `thm:pb-pullback-rank-quotient` (constant-rank quotient) + `:837/:858` exact signed base comparison / positivity criterion + `:979` `thm:pb-anomaly-composition` | **P&P — the strongest genuinely new mathematics in the corpus** |
| 32 | Lorentzian signature from complexified frame twist (`PIFB2.tex:1894-2014`) | **EXCL.** `Lorentzian` → 2 hits, both disclaimers (`05d:1622`; `12_philosophy.tex:46`: "supplies no Lorentzian signature, causal cones, spacetime measure, gravitational field equation, or identification of `𝒞` with physical spacetime") | **EXCL** |
| 33 | Consensus metric / gauge-orbit average / observable sectors (`PIFB2.tex:2015`) | **ABSENT** as a metric construction. `consensus` appears in `06_gaussian.tex`, `08_infogeometry.tex`, `10_renormalization.tex`, and `12_philosophy.tex:239` explicitly *warns against* overloading the word | **ABSENT** |
| 34 | Gravity / measurement / macroscopic objects (`PIFB2.tex:2070`) | **EXCL.** `gravity` → 0; `gravit` → 1 (in an exclusion list at `12_philosophy.tex:47`) | **EXCL** |
| 35 | Consciousness / qualia / hard problem (`PIFB2.tex:2086`) | **EXCL.** `consciousness` → 0, `qualia` → 0 | **EXCL** |
| 36 | Lahav–Neemeh inter-frame transformation law (`PIFB2.tex:301`, `sec:lahav_convergence`) | **ABSENT.** `LahavNeemeh2022/2025` exist in `references.bib` but are cited **zero times** in `Theory/` | **EXCL** |
| 37 | Kantian noumenal reading (`PIFB2.tex:73`, O3) | `12_philosophy.tex:65` `sec:phil-noumenon` (`noumen` → 5 hits, all in ch. 12) — an "idle-wheel criterion" that argues the noumenal posit does **no work** unless a holonomy-conditioned observable is exhibited, which is `\status{OPEN}` | **P-OPEN — but see §5, it is philosophy not theorem** |
| 38 | Obstructions/no-gos | `11_obstructions.tex`: flat reciprocal fold singular (`cor:obs-flat-fold-singular`, `11:57`), kernel = holonomy eigenvalue-1 multiplicity (`prop:obs-reciprocal-pair-kernel`, `11:42`), declared root unavoidable (`11:239`), normalizer depends on the graph link (`11:120`), holonomy shrinks the kernel (`11:334`), unique Gaussian-star fixed point + contraction (`thm:obs-star-fixed-point-contraction`, `11:256`) | **P&P — genuinely new, entirely absent from PIFB2** |

**Coverage tally.** Of 38 PIFB2 constructions: 13 present & proved (several strictly stronger),
5 present-but-weaker, 3 present-as-gap, **8 absent without being excluded** (rows 10, 15, 17, 22-def,
23, 24, 33 and the section-valued VFE), and 9 deliberately excluded.

---

## 2. The central object: does `Theory/` deliver it?

**No. It delivers half of it, in two disjoint pieces, joined by a hypothesis it proves is lossy.**

### 2.1 What exists

Every *geometric* ingredient of the goal sentence exists, in one place, with the right generality:

| Piece | Where |
|---|---|
| base manifold | `02_geometry.tex:16` `def:geo-context-base` |
| structure group | `02_geometry.tex:46` (abstract Lie group `G`) |
| principal bundle | `02_geometry.tex:40` `def:geo-principal-systems`, `eq:geo-principal-bundle` |
| representations | `02_geometry.tex:80-95`, `ρ_b, ρ_m` on samples; `ρ̂_b, ρ̂_m` pushforward on laws |
| fiber = statistical manifold | `02_geometry.tex:67-78` + `hyp:geo-smooth-tier` (`:103`) + `prop:pb-statistical-tensor-descent` (`05c:59`) |
| associated bundle | `02_geometry.tex:120` `def:geo-associated-bundles` |
| section = agent | `02_geometry.tex:403` `def:geo-agent` |
| connection(s) | `02_geometry.tex:279` `def:geo-connections`, two independent `ω_b, ω_m` |

The **closest thing to a master definition** is `def:geo-agent`, quoted verbatim
(`02_geometry.tex:403-416`):

> `\definitionheading{Agent}{def:geo-agent}`
> `𝒜^i = (𝒞_i; q_i, s_i, u_i^b, u_i^m)` … with
> `q_i ∈ Γ(𝒞_i, 𝓔_b|_{𝒞_i})`, `s_i ∈ Γ(𝒞_i, 𝓔_m|_{𝒞_i})` … `\status{DEFINITION}`

and its restatement at `12_philosophy.tex:163`:

> "agents are sections of associated law bundles, and a global reference frame exists only under
> the corresponding principal-bundle trivialization hypothesis. `\status{DEFINITION}`"

**Note what is missing from `def:geo-agent`: any free energy.** The agent is a static
geometric datum. Nothing in it evolves.

### 2.2 The type wall

The VFE lives on a *different object*. `03_probability.tex:15` declares a **finite design**
`D = {c_a}_{a=1}^M ⊆ 𝒞` and builds the stacked latent space
`𝖸_D = ∏_a ∏_i (𝖪_{i,a} × 𝖬_{i,a})` (`03_probability.tex:27`). The recognition object is *one*
Markov kernel `Q_X(dY | o)` into `𝒫(𝖸_D)` (`05_elbo.tex:13` `def:elbo-recognition-kernel`), and
`𝓕[Q_X; X, o] = −ℒ(Q_X; X)` (`05_elbo.tex:222`).

The manuscript is explicit that this is a different object
(`03_probability.tex:42`):

> "Evaluating a distribution-valued section returns something else entirely: `q_i^{o,X}(c_a)` is a
> probability measure on `𝖪_{i,a}` … and neither is an element of `𝖸_D`."

and (`03_probability.tex:415`):

> "The two constructions have different domains. … Neither is defined in terms of the other, so
> their outputs coincide only if that is declared."

The declaration is `hyp:prob-sampling-compatibility` (`03_probability.tex:436`,
`\status{HYPOTHESIS}`). And `prop:prob-compatibility-nonidentifiability`
(`03_probability.tex:420`, `\status{ESTABLISHED}`) proves that this hypothesis
**determines neither side**: (i) it does not determine `Q_X` (the joint is not recoverable from
marginals — copula freedom, `05_elbo.tex:~30` citing `Nelsen2006`); (ii) it does not determine the
sections (bump-function deformation away from `D`).

**Consequence.** "A section evolves under a VFE" is not a statement `Theory/` can currently make.
The variational variable is `Q_X ∈ 𝒫(𝖸_D)`; the section is a shadow of it at `M` points, and even
that correspondence is `M`-to-many both ways.

The `05b` local/collective chapter goes further and **drops the manifold entirely**:
`hyp:local-interaction-kernels` (`05b:18`) starts "Let `(𝖷, 𝒳)` be a standard Borel context space,
let `V` be an arbitrary finite set of agents" — the smooth base `𝒞` is not used at all. The bundle
survives only as an optional remark ("Its state **may** contain a belief-law point in
`(𝓔_b)_{c_i}`", `05b:23`). By `05b:782` the manuscript concedes: "'agent' is not determined by the
principal bundle or by variational [structure]".

### 2.3 What is missing and where it should live

| Missing piece | Where it should live |
|---|---|
| **A functional `𝓕: Γ(𝒞, 𝓔_b) × Γ(𝒞, 𝓔_m) → ℝ ∪ {+∞}`** — a VFE whose *argument is a section* | A new chapter between `05_elbo` and `05c`, or a new section §`05e`. Requires a declared base measure `μ` on `𝒞` (currently forbidden: `12_philosophy.tex:33-38` "the finite design is a declared subset, not a random sample from a law on `𝒞`. No expectation over contexts is used") |
| **A local VFE indexed by a base point**, `𝓕_c(σ)`, and a global one `𝓕(σ) = ∫_𝒞 𝓕_c(σ) dμ(c)` | Same place. The current local/global pair (`05b`) is indexed by *agent blocks* `B ⊆ V`, not by base points |
| **The relation between local-in-`c` and global-in-`c`** | Absent. The existing `thm:obs-local-global-potential` (`05b:347`) is an equality in the *agent-block* direction; there is no `c`-direction analogue |
| **Gauge covariance of the section-valued functional** | Would follow from `prop:gen-product-evidence-invariance` (`04_generative.tex:408`) *if* the functional were sectionwise — but that proposition is about `𝖸_D` |
| **A well-posedness theorem** (existence of a minimizing section, lower semicontinuity on a declared topology on `Γ`) | Absent. `05d:109` `hyp:hist-regular-section-space` declares a "regular space of section pairs `𝔖_i`" and warns "**No such structure follows merely from writing down all smooth sections**" — the right warning, but the structure is never supplied except in the one exhibited finite-dimensional tier (`05d:235` `def:hist-finite-configuration-tier`, `P = 𝒞_ℓ × G` with `G = (ℝ^K, +)` and flat `ω`) |

Note the last row: `05d_relational_inference.tex:235-280` **already contains a worked
finite-dimensional section space with a metric and a regularity theorem**
(`thm:hist-finite-tier-regularity`, `05d:275`). This is the natural home for the missing functional
and is by far the cheapest repair available.

---

## 3. Load-bearing bridges

### (i) Why must the fiber be a statistical manifold, and how does `G` act on it?

**EXISTS AND PROVED — and it is the corpus's best result.**

- *How `G` acts*: `02_geometry.tex:80-95`. Two independent representations `ρ_b: G → Aut(𝖪)`,
  `ρ_m: G → Aut(𝖬)` on **sample** spaces, inducing law-level actions
  `ρ̂_x(g) q = (ρ_x(g))_# q` (`eq:geo-pushforward-actions`). The manuscript's warning at
  `02_geometry.tex:97-100` — "Multiplying a matrix into a density is not the pushforward" — is
  exactly the error PIFB2 risks at `PIFB2.tex:212` when it writes
  `ρ_state(g)·𝒩(μ,Σ) = 𝒩(gμ, gΣgᵀ)` without distinguishing the two levels.
- *Why statistical*: `05c_pullback_geometry.tex:59` `prop:pb-statistical-tensor-descent`,
  `\status{ESTABLISHED}` — because `ρ̂_x(g)` is induced by a **parameter-independent bimeasurable
  change of sample coordinates**, it is a statistical isometry, so `g^F_x` and the Amari–Chentsov
  tensor `𝒯_x` are `G`-invariant and descend to *vertical* tensors on `𝓔_x`. The load-bearing
  remark (`05c:84-87`): "Closure under an arbitrary diffeomorphism of the parameter chart would
  not prove statistical isometry."

**Gap.** The *necessity* direction is never argued. The manuscript proves "if the fiber is a
statistical manifold and `G` acts by sample-coordinate change, then the tensors descend". It does
not prove or even discuss "the fiber **must** be a statistical manifold" — which is the goal
sentence's word. The obvious argument (Chentsov/Ay–Jost–Lê–Schwachhöfer uniqueness: the Fisher
metric is the only Markov-invariant metric, so any `G`-invariant fiber geometry compatible with
statistical morphisms is Fisher) is **available** and **not made**: `Cencov1982` is cited exactly
once (`08_infogeometry.tex`), and never in `02_geometry.tex` or `05c`. This is a one-paragraph fix
with large payoff.

### (ii) How do local free energies aggregate to a global one, and what is the exact gap?

**EXISTS AND PROVED — for agent blocks; ABSENT for base points.**

The main theorem, verbatim (`05b_local_collective_elbo.tex:347-372`):

```latex
\theoremheading{Exact local--global potential identity}{thm:obs-local-global-potential}
... Then
\mathcal F_o^{\rm ext}(Q')-\mathcal F_o^{\rm ext}(Q)
=\E_{Q_{B^c}}\left[\mathcal F_{B,o}^{\rm ext}(r'_B;Y_{B^c})-\mathcal F_{B,o}^{\rm ext}(r_B;Y_{B^c})\right].
Thus every exact local conditional update is a coordinate update of the same
collective VFE.  \status{ESTABLISHED}
```

This is an **equality, not an inequality** — stronger than what PIFB2 attempts. Three important
refinements:

- The "gap" is not additive slack but a **counting identity**: the singleton local VFEs
  over-count shared factors, `Σ_i H_{{i},o} = Σ_a |∂a| E_{a,o}` (`05b:463-486`,
  `eq:obs-singleton-incident-counting`), so `Σ_i 𝓕_i ≠ 𝓕`.
- The single-count ledger is `eq:obs-global-ledger` (`05b:441-450`):
  `𝓕 = TC(Q) + Σ_i KL(Q_i‖ρ_i) + 𝔼_Q[Σ_a E_{a,o}]`, with `TC(Q) = KL(Q ‖ ⊗_i Q_i)`.
  Total correlation *is* the exact local-to-global gap. Clean and correct.
- Explicit non-licence (`05b:383-387`): "**Independently replacing all correlated full conditionals
  need not define any joint recognition law, so such a parallel prescription is not licensed.**"

**Gap.** This is aggregation over the *index set* `V`. The goal sentence's "local" almost certainly
means "local on `𝒞`" (local sections!). There is **no** result relating `𝓕` restricted to
`𝒰 ⊆ 𝒞` to `𝓕` on `𝒞`, no sheaf/gluing statement, no partition-of-unity argument. Searching for
`sheaf`, `gluing`, `partition of unity` in `Theory/*.tex` returns nothing relevant.

### (iii) Is the coupling DERIVED from gauge covariance, or CHOSEN and then checked?

**CHOSEN AND CHECKED. The manuscript says so, repeatedly, in its own voice.**

Three quotes settle it:

1. `05b:66-75`: "Bundle covariance is **imposed by requiring** each `K_a` to be invariant under
   simultaneous changes of the incident agent frames and the factor frame. **One concrete
   realization** gives factor `a` its own principal frame … `\status{DEFINITION}`" — tagged
   DEFINITION, not THEOREM.
2. `04_generative.tex:379` `hyp:gen-kernel-covariance`, `\status{HYPOTHESIS}` — the covariance of
   the generative kernels under `(R^b_i, R^m_i)` is *declared*, and only then does
   `prop:gen-product-evidence-invariance` (`04_generative.tex:408`) conclude
   `p_{θ'}(o|X') = p_θ(o|X)`.
3. `06_gaussian.tex:297`: "this is adopted as a **declared restriction**. … **The document does not
   claim that it is forced by anything**, and `prop:gauss-interaction-family-thin` records that it
   is a **measure-zero restriction** on the space of Gaussian recognition laws. `\status{HYPOTHESIS}`"
   Corroborated at `06_gaussian.tex:234` ("it is **not a consequence** of the general
   linear-Gaussian directed model") and `06a_generative_gaussian.tex:307`.

The nearest thing to a classification is `07b:1257-1290`, which explicitly disclaims uniqueness:
"componentwise/permutation realization is the declared sufficient hypothesis here, **not the only
logically possible one**" — with a genuinely instructive counterexample (a product-Haar-preserving
shear of `𝕋²` mixing singleton and pair components).

The only "forcing" theorem in the corpus is about aggregation, not coupling:
`10_renormalization.tex:122` `prop:grg-positive-additive-linear` ("Positive additive rules are
forced to be linear").

**This is the single biggest *scientific* gap.** The whole appeal of a gauge formulation is that
covariance *constrains* the interaction. If the coupling is postulated and merely checked, the
gauge language is decoration. PIFB2 is honest about this too (`PIFB2.tex:675`: "The functional
displayed below is an **ansatz, not a theorem**"), so neither document has this. It is the
result that would make the program.

### (iv) How does coarse-graining act on sections and on the bundle itself?

**Bundle: EXISTS AND PROVED. Sections: EXISTS AS GAP. Meta-agent-as-section: ABSENT.**

- *On the bundle* — the best result in the RG half. `07_general_renormalization.tex:153`
  `def:rg-geometric-state` gives a level-indexed base `𝒞_ℓ`, group `G_ℓ`, principal bundle
  `ϖ_ℓ: 𝒫_ℓ → 𝒞_ℓ`, and associated bundles `𝓔_{ℓ,b}, 𝓔_{ℓ,m}`. The coarsening data is
  `c_ℓ: 𝒞_ℓ → 𝒞_{ℓ+1}`, `κ_ℓ: G_ℓ → G_{ℓ+1}`, `𝒫_ℓ` with
  `𝒫_ℓ(p·g) = 𝒫_ℓ(p)·κ_ℓ(g)` (`07:249-253`), descending to
  `C_{ℓ,s}[p,z] = [𝒫_ℓ(p), q_{ℓ,s}(z)]` **iff** `q_{ℓ,s}` intertwines through `κ_ℓ`
  (`eq:rg-scale-intertwiner`, `07:268`). And, crucially, existence of `𝒫_ℓ` is a **genuine
  topological condition** — iff `𝒫_ℓ ×_{κ_ℓ} G_{ℓ+1} ≅ c_ℓ^* 𝒫_{ℓ+1}`, with an explicit failure
  witness (Hopf bundle over `S²`, `07:258-266`). PIFB2 has nothing remotely like this.
- *On sections* — blocked and correctly flagged. `05c:677-680`: "$\Psi\circ s$ is only a section
  of the pullback bundle `f*Ē` along `f`; **a fine section does not by itself define a section on
  `𝒞̄`**. `\status{DEFINITION}`" The descent relation `Ψ∘s = s̄∘f` is
  `\status{HYPOTHESIS}` (`eq:pb-coarse-related-sections`, `05c:684`), and everything downstream
  (`cor:pb-meta-perceived-geometry`, `05c:1172`) inherits it.
- *Does a meta-agent live in a bundle over a coarser base?* **No.** The primary definition
  (`05b:189-194`) makes a meta-agent a block `B ⊆ V`; the refined one (`07b:1620-1626`) makes it a
  connected component of a block with a rooted spanning tree. The bundle reading is an optional
  add-on the manuscript explicitly says the bundles do not supply
  (`07:209-220`: "These components are **not supplied by the associated bundles alone**").

So: PIFB2's meta-agent-as-coarse-section is *not* delivered, but the harder half — the coarse
bundle itself, with its obstruction — *is*. The missing link is exactly the descent hypothesis.

### (v) What dynamics does the VFE generate, and in what sense is it a gradient flow?

**EXISTS AND PROVED in a restricted setting; ABSENT in the bundle setting.**

`05b:668-694` (`sec:local-natural-gradient`), `\status{ESTABLISHED}`:
`η̇_i = −γ_i G_i^{-1} ∇_{η_i}F` gives `dF/dt = −Σ_i γ_i (∇_{η_i}F)^T G_i^{-1}(∇_{η_i}F) ≤ 0`.
This is a genuine natural-gradient descent statement. But:

- It requires a **product recognition family with block-diagonal Fisher metric**
  `G(η) = ⊕_i G_i(η_i)`, and the manuscript flags this: "Block orthogonality is load bearing. With
  a nondiagonal Fisher metric, the global natural gradient mixes agents and independent local
  inversions are a different dynamics" (`05b:696-700`). Note the tension with the whole point of
  Ch. 5, which is that the recognition law is *correlated*.
- The attention sector gets an exact **replicator** flow: `β̇^Q_{ij} = −γ_i β^Q_{ij}(c_{ij} − Σ_k β^Q_{ik}c_{ik})`
  with dissipation `= −γ_i Var_{β^Q_i}(c_{ij}) ≤ 0` (`05b:648-668`). Nice, and new relative to PIFB2.
- **Convergence** is proved in exactly one place: `11_obstructions.tex:256`
  `thm:obs-star-fixed-point-contraction` — unique fixed point and geometric contraction with rate
  `ρ = λ_max(P_b^{-1/2} B P_b^{-1/2}) < 1` for the Gaussian star. In general it is **OPEN**:
  `05_elbo.tex:637` `open:elbo-alternating-convergence`.
- **Absent entirely** (my searches over `Theory/*.tex`): `Wasserstein` → 0, `optimal transport` → 0,
  `Fokker-Planck` → 0, `Langevin` → 0, `JKO` → 0, `mirror descent` → 0. `Lyapunov` appears once, in
  a hedge (`05d:841`). PIFB2's `Łojasiewicz` convergence argument (`PIFB2.tex:1728`) has no
  counterpart.
- No dynamics on the **section space** and no dynamics on the **group sector** (PIFB2's
  `U̇_i = −η_φ U_i ξ_i` with `dexp` regularity, `PIFB2.tex:965-1005`, has no counterpart —
  `dexp` → 0 hits).

---

## 4. Scope drift

### 4.1 Added, that PIFB2 did not need

| Addition | Volume | Verdict |
|---|---|---|
| `07b_agent_network_rg.tex` — exact bounded action calculus, DQM scores, Gaussian Hermite block spectrum, positive-unital essential spectrum, Hoeffding action isomorphism, projection-memory recurrence (Zwanzig/Nakajima), typed beta functions, exhaustive fixed-point equations | **2828 lines = 17% of the corpus** | Real mathematics, but it is *operator-theoretic RG*, not gauge-bundle theory. It could be its own paper. It is the single largest misallocation of effort relative to the stated goal |
| `06_general_coarsegraining.tex` + `07_general_renormalization.tex` — Markov-category coarse channels, extended DPI with equality conditions, evidence-preserving channels, scale cocycles, tempered comparison trivializations | 1935 lines | Mostly standard (DPI, Bayes recovery) with careful equality conditions. Value: the typed separation of marginalization / energy precomposition / family restriction (`06:326-331`) is genuinely clarifying and cites nobody for it (see §7) |
| `03_probability.tex` measure-theoretic hygiene — reference measures, regular conditionals, mixed coordinates, Fréchet-class/copula non-identifiability | 449 lines | Necessary but could be an appendix. Currently it *creates* the type wall of §2 rather than bridging it |
| `07_restrictions.tex`, `08_infogeometry.tex`, `09/10` Gaussian tier | ~2000 lines | Legitimate "worked realization", but three chapters is generous |
| Obstruction results (`11_obstructions.tex`) | 422 lines | **Keep all of it.** These are the paper's teeth and PIFB2 has nothing like them |

### 4.2 Dropped, that the goal sentence requires

1. **The section-valued free energy functional.** Row 10 above. Without it the goal sentence is
   literally unsatisfied.
2. **Local-in-`𝒞` vs global-in-`𝒞`.** The goal says "local/global variational free energy". `Theory/`
   reads "local" as "per agent block". That may be a defensible reinterpretation but it is *not*
   what the sentence says, and the sheaf-theoretic reading is the interesting one.
3. **Dynamics of the section / of the frame.** PIFB2's whole point is that `q_i(c)`, `φ_i(c)` *flow*.
   `Theory/` has flows only in finite-dimensional parameter charts.
4. **Meta-agent as a section over a coarser base.** The bundle-level coarse map exists; the
   section-level object does not.
5. **A reason the fiber must be statistical.** §3(i).

### 4.3 The WikiText-103 sweep and transformer recovery

**They have no counterpart, and — with one qualification — they should not.**

Searches on `Theory/*.tex`: `transformer` → 0, `WikiText` → 0, `query` → 0, `GPT` → 0. This is
enforced by `SPEC.md:26` ("The executable does not appear"). That is the right call for a
mathematics paper: PIFB2's own fence F6 concedes the sweep is "an aggregate within-architecture
description, not a competitive quality comparison", that per-seed records are unavailable, that
`K_q = 90` rests on two seeds, and that the three largest dimensions "occupy a different
optimization regime" (`PIFB2.tex:118`). It would not survive a referee.

The **qualification**: the *attention* result should not have been thrown out with the experiment.
`prop:obs-attention-elbo` (`05b:547`) already derives an exact row softmax
`β*_{ij} ∝ π_{ij} exp(−c_{ij}/τ)` from a latent source label inside a fixed normalized joint — a
strictly better derivation than PIFB2's mean-field ansatz, with the exact-lift conditions worked out
(the `09_pifb2_crosswalk.tex` shows the tie `R_ij = Ω_ij Σ_j Ω_ij^T` forces `τ = 1`, so the deployed
`τ = κ√K` operating point is *not* an exact coordinate). A single remark saying "specializing to
`Ω = I`, isotropic Gaussians, and gauge-fixed frames recovers scaled dot-product attention" would
cost two paragraphs and buy the paper its entire ML audience. **Currently `Vaswani2017` exists in
`references.bib` and is cited zero times in `Theory/`.** That is leaving money on the table.

---

## 5. The "noumenal" commitment

### 5.1 Current status: philosophy, correctly labelled, and self-defeating

`noumen` appears 5 times, all in `12_philosophy.tex` (`:65, :69, :74, :118`). The chapter's
`sec:phil-noumenon` ("When a noumenal reading earns its keep") adopts an **idle-wheel criterion**:
"a posit with no trace in any declared observable is removed by parsimony `\status{DEFINITION}`",
immediately followed by "No result in this chapter derives the declared rule.
`\status{NOT-CLAIMED}`".

It then argues the noumenal reading currently **fails** its own test. The candidate observable is
graph-link holonomy `H^b_γ = Θ^b_{e_0}···Θ^b_{e_{r-1}}` (`eq:phil-holonomy`), whose conjugacy class
is reframing-invariant (`\status{ESTABLISHED}`); but "In the flat graph-link specialization every
loop product telescopes", so "the resulting identity observable gives the noumenal reading no
additional work". And "The graph-link observable is **not claimed to be evidence of base curvature
or bundle topology**. `\status{NOT-CLAIMED}`". Two OPEN obligations follow, mirrored in
`appendix_claim_ledger.tex:242-262` ("Operational base holonomy (open)", "Graph-to-base
identification (open)").

Earlier, `12_philosophy.tex:~52-60`: two readings are compatible (Kantian scaffolding vs. noumenal
structure), and "No equation selects between the two. `\status{NOT-CLAIMED}`".

So: **there is currently no theorem with noumenal content.** The word appears only in a chapter
that argues against its own load-bearing use.

### 5.2 Is there rigorous content available? Yes — three theorems, two of which are nearly proved.

The goal sentence's "noumenal" decomposes into three checkable claims. Sketches:

**N1 (no intrinsic base geometry — already true by construction).**
*Statement.* `𝒞` carries no metric, no measure, no distinguished connection, and no probability law;
every geometric tensor on `𝒞` appearing in the theory is of the form `σ*T` for a section `σ` and a
declared connection `∇`.
*Status.* Effectively established but never stated as a theorem. Evidence: `def:geo-context-base`
declares only smooth structure; `12_philosophy.tex:33-38` "the finite design is a declared subset,
not a random sample from a law on `𝒞`. No expectation over contexts is used"; the pullback tensors
of `def:pb-informational-pullbacks` (`05c:109`) are the *only* base tensors in the manuscript; and
`appendix_claim_ledger.tex:~275` records "**No canonical connection is selected anywhere in this
manuscript.**"
*Work needed:* **writing only.** Collect the negations into one proposition in `02_geometry.tex`.

**N2 (agent-relative geometries are gauge-related — already proved, needs promotion).**
*Statement.* For two agents `i, j` whose frames differ by `g_{ij}: 𝒰 → G` and whose sections agree
after transport, the pulled-back informational metrics satisfy `G_i = Ad^*_{g_{ij}} G_j` (passive
covariance); hence no agent's pullback geometry is privileged.
*Status.* `thm:pb-pullback-gauge-invariance` (`05c:124`, `\status{ESTABLISHED}`, "Passive gauge
covariance of the covariant pullbacks") is precisely this, plus
`prop:pb-pullback-connection-change` (`05c:184`) for the connection dependence.
*Work needed:* **writing only.** Restate as a corollary with the noumenal gloss.

**N3 (indistinguishability — the real theorem, and it is not proved).**
*Statement (sketch).* Let `𝔓 = (P → 𝒞, ω)` and `𝔓' = (P' → 𝒞, ω')` be two principal-bundle-with-
connection data over the same base, and let `Rec(𝔓)` denote the set of laws of the observation
record `o ∈ 𝖮_D` induced by admissible generative parameters over `𝔓`. If `𝔓` and `𝔓'` are related
by a bundle isomorphism over `id_𝒞` (equivalently, if the represented graph-link holonomies
`H^b_γ` are conjugate for every loop `γ`), then `Rec(𝔓) = Rec(𝔓')`; and conversely, there exist
non-isomorphic `(𝔓, ω)`, `(𝔓', ω')` with `Rec(𝔓) = Rec(𝔓')`. **No population record statistic
distinguishes them.**
*Status.* **Not proved, and the manuscript knows exactly what it would take.**
`appendix_claim_ledger.tex:242-256` spells out the required tuple: "a named principal bundle and
connection, an assigned base loop, a gauge-invariant population-record statistic, a typed map from
the connection data to its record law, and two admissible connection data sets for which every
declared non-holonomy input is fixed, the represented loop holonomies have distinct conjugacy
classes, and the statistic's induced distributions differ" — and states "**No such tuple or
empirical evidence is presently supplied. `\status{OPEN}`**".
*Assessment.* The **negative** half (invariance: isomorphic data ⟹ identical record laws) is within
reach — it should follow from `prop:gen-product-evidence-invariance` (`04_generative.tex:408`) plus
`hyp:gen-kernel-covariance`, since a bundle isomorphism induces exactly the `R`-pushforward `T` that
proposition already handles. **Proving N3(a) turns "noumenal" from philosophy into a theorem in
roughly two pages**, and it is by far the highest-value/lowest-cost item in this audit. The converse
(non-isomorphic data with equal record laws) is genuinely harder and can be left as an open problem,
or answered in a toy case (`G = U(1)`, `𝒞 = S¹`, flat vs. non-flat with rational holonomy).

---

## 6. Viability verdict and shortest path

### 6.1 Diagnosis

`Theory/` is a 17k-line monograph carrying at least three separable papers, none of which is
currently the paper the goal sentence describes:

- **Paper A** (`02` + `05c` + parts of `05d`): *Connection-relative informational pullback geometry
  on associated statistical bundles.* Genuinely new, self-contained, proved. ~5000 lines of source.
- **Paper B** (`03` + `04` + `05` + `05a` + `05b` + `11`): *Exact local and collective evidence
  bounds for interacting agents, with obstructions.* Solid, mostly proved, but nearly free of bundle
  content.
- **Paper C** (`06_general` + `07_general` + `07b` + `09` + `10`): *Exact effective scale theory for
  agent networks.* Large, technical, and only loosely coupled to A and B.

Trying to publish all three as one monograph is why the goal sentence is not met: no chapter is
responsible for the joint object.

### 6.2 The shortest credible path — Paper A+, with the bridge repaired

Target a mathematical-physics / information-geometry venue with **Paper A plus the bridge**, and
demote B and C to companions.

**The 5 results that would make it publishable:**

1. **`𝓕` on sections (the missing master object).** Define
   `𝓕_μ(σ) = ∫_𝒞 f(σ(c), ∇σ(c)) dμ(c)` for a declared base measure `μ` and a local density `f`
   built from KL against a declared fiberwise reference section, and prove: (a) `𝓕_μ` is
   well-defined in `[0,+∞]`; (b) it is **gauge-invariant** under `Aut_G(P)`; (c) its restriction to
   the finite design `D` with `μ = Σ_a δ_{c_a}` reproduces `𝓕[Q_X]` of `05_elbo.tex:222` under
   `hyp:prob-sampling-compatibility` **and a declared product-recognition restriction**.
   *Home:* new §`05e`, immediately after `05b`. *Cost:* hard mathematics, but bounded —
   `05d:235-280` already exhibits a finite-dimensional section space where this is
   a finite Gram-matrix computation. **This is the deliverable that makes the goal sentence true.**
2. **Local-to-global on `𝒞`.** With `{χ_α}` a partition of unity subordinate to `{𝒰_α}`, prove
   `𝓕_μ(σ) = Σ_α 𝓕_{χ_α μ}(σ|_{𝒰_α})` exactly (trivial once (1) is additive in `μ`) and, more
   substantively, that the minimizer over `Γ(𝒞, 𝓔)` is **not** the glue of local minimizers, with
   the exact defect equal to a total-correlation-type term. The `05b` ledger
   (`eq:obs-global-ledger`) is the template.
3. **N3(a): gauge-indistinguishability.** §5.2 above. Isomorphic bundle-with-connection data induce
   identical observation-record laws. Two pages from
   `prop:gen-product-evidence-invariance` + `hyp:gen-kernel-covariance`.
4. **Necessity of the statistical fiber.** Chentsov / Ay–Jost–Lê–Schwachhöfer: among `G`-invariant
   fiberwise 2-tensors natural under statistical morphisms, the Fisher metric is unique up to scale;
   hence "the fiber is a statistical manifold" is forced, not chosen. `AyJostLeSchwachhofer2017` and
   `Cencov1982` are already in the bib. One page.
5. **One gradient-flow theorem on sections.** On the exhibited tier (`05d:235`,
   `P = 𝒞_ℓ × G`, `G = (ℝ^K,+)`, flat `ω`, `𝒬_ℓ ≅ ℝ^N` with constant Gram metric `𝖦_ℓ`), prove that
   `σ̇ = −𝖦_ℓ^{-1}∇𝓕_μ(σ)` exists, is unique, and converges to the unique minimizer, with an explicit
   rate. The Gaussian-star contraction theorem (`thm:obs-star-fixed-point-contraction`, `11:256`) is
   the model; this is the section-space analogue. Achievable.

Optional 6th, if cheap: **restore the attention/transformer remark** (one page, no experiment).

**Claims to demote or cut:**

- **Cut** `07b_agent_network_rg.tex` from the paper entirely → companion paper C. 2828 lines, its
  key theorem `thm:rg-complete-effective-theory` (`07b:2735`) consumes ~15 separately declared
  data and is "a closure theorem over declared data, not a derivation".
- **Cut** the Gaussian realization to one chapter (merge `06_gaussian`, `06a`, `07_restrictions`,
  `08_infogeometry` into one "worked realization" chapter of ~40 pages).
- **Demote** `conj:grg-fixed-b-attraction` (`10_renormalization.tex:250`) to a remark; it is the
  corpus's only `\conjectureheading` and it is not needed.
- **Demote** `12_philosophy.tex` to a 3-page discussion, *unless* N3 is proved — in which case
  promote its noumenal section to a theorem and keep it.
- **Cut** `cor:cg-holonomy-cross-morphism` (`06_general_coarsegraining.tex:668`) or prove it; a
  `\corollaryheading` tagged `\status{HYPOTHESIS}` is a typographical contradiction a referee will
  flag.

### 6.3 Hard mathematics vs. writing/organization

| Task | Kind | Estimate |
|---|---|---|
| (1) `𝓕` on sections, well-definedness + gauge invariance | **Hard math** (measure on `Γ`, lower semicontinuity, coercivity) | The main risk. Mitigate by doing it first on the exhibited finite-dim tier |
| (2) local-to-global on `𝒞` with exact defect | **Medium math** | Follows (1) |
| (3) N3(a) indistinguishability | **Easy math** — assembly of existing pieces | Highest value/cost ratio in the whole audit |
| (4) Fisher-necessity via Chentsov | **Writing + one citation** | Trivial |
| (5) section gradient flow on the exhibited tier | **Medium math** | Template exists (`thm:obs-star-fixed-point-contraction`) |
| Splitting the monograph into A/B/C | **Organization** | Mechanical but large |
| Adding ~60 missing citations (§7) | **Writing** | Mechanical, mandatory |
| Attention/transformer remark | **Writing** | One page |

**Bottom line:** three of the five results are writing or assembly; only (1) and (5) are real
mathematics, and (5) is tractable on the tier the manuscript already exhibits. A defensible
standalone paper is roughly one hard theorem away, not five.

---

## 7. Literature positioning

### 7.1 The headline defect

Citation density in `Theory/`: **101 `\cite*` commands / 81 unique keys across 96,957 words** —
about **1.4 citations per 1000 words**, extraordinarily sparse for a theoretical monograph.
Chapters with **zero** citations: `01_introduction.tex`, `appendix_notation.tex`,
`appendix_claim_ledger.tex`, `appendix_numerical_provenance.tex`. Near-zero:
`05c_pullback_geometry.tex` (68 KB, **2 citation commands**), `05d_relational_inference.tex`
(84 KB, 3), `07b_agent_network_rg.tex` (136 KB, 6), `11_obstructions.tex` (36 KB, 2),
`05b_local_collective_elbo.tex` (35 KB, 1).

**An introduction with zero citations will be desk-rejected.**

### 7.2 Cited zero times in `Theory/` despite existing in `references.bib`

| Author / program | Bib key(s) present | Cited in Theory/ |
|---|---|---|
| Friston (FEP, active inference) | `Friston2010`, `Friston2017`, `Friston2018`, `Friston2023PhysReports`, `friston2016active`, `friston2008hierarchical`, +9 more | **0** |
| Parr | `parr2022active`, `Parr2022` | **0** |
| Da Costa | `dacosta2021bayesian` | **0** |
| Ramstead | `ramstead2020variational`, `Ramstead2019`, `ramstead2023bayesian` | **0** |
| Sakthivadivel (Bayesian mechanics) | `Sakthivadivel2022` | **0** |
| Sengupta & Friston (neuronal gauge theory) | `Sengupta2016NeuronalGauge`, `sengupta2017gauge` | **0** |
| Cohen & Welling (G-CNN, gauge CNN) | `Cohen2016`, `cohen2019gauge` | **0** |
| Weiler (steerable, coordinate-independent CNNs) | `weiler20183d`, `weiler2021coordinate` | **0** |
| Bronstein (geometric deep learning) | `Bronstein2021` | **0** |
| Wilson (RG) | `Wilson1971`, `Wilson1974`, `WilsonConfinement1974` | **0** |
| Bény–Osborne (information-geometric RG) | `beny2015information` | **0** |
| Vaswani (attention) | `Vaswani2017` | **0** |
| Lahav–Neemeh | `LahavNeemeh2022/2025` | **0** |

This is not a minor omission. `Sengupta2016NeuronalGauge` is the *direct precursor* on the
gauge-FEP axis — PIFB2 says so explicitly (`PIFB2.tex:128`: "this is the closest direct precursor on
the gauge-FEP axis"). `Theory/` does not mention it. Likewise
`weiler2021coordinate` ("Coordinate Independent Convolutional Networks") is the closest existing
work to `02_geometry.tex`'s entire construction and is not cited.

### 7.3 Absent from `references.bib` entirely (and from the vault)

Verified by grep across `references.bib` and `Research/wiki/`, `Research/sources/`:

- **Fritz, Markov categories / categorical probability.** Zero hits anywhere in the vault or bib
  (the only "categorical probability" hits are softmax distributions). Yet
  `06_general_coarsegraining.tex:28` proves `prop:cg-markov-category` ("Markov kernels form a
  category") — **this is Fritz/Cho–Jacobs/Panangaden territory being rederived without citation.**
  The subsequent typed separation of coarse operations is essentially a Markov-category argument.
- **Bauer–Bruveris–Michor** (uniqueness of the Fisher metric, diffeomorphism-invariance version).
  Absent. Needed for §6.2 item (4).
- **Villani / Ambrosio / Kantorovich / JKO** (optimal transport, Wasserstein gradient flows).
  Absent. A referee will ask why the flow is Fisher–Rao and not Wasserstein; there must be an answer
  and a citation.
- **Bethe / Kikuchi** (only `Yedidia2005` exists, uncited). The `eq:obs-global-ledger` decomposition
  `𝓕 = TC + Σ KL + 𝔼[E]` is close to a region-graph / Bethe free-energy statement and should say so.

### 7.4 Where the work genuinely differs

Being fair, three things here are not standard:

1. **`prop:pb-statistical-tensor-descent` + the covariant pullback family** (`05c`). Amari and
   Ay–Jost–Lê–Schwachhöfer give the fiber geometry; Cohen/Weiler give the equivariant-field
   machinery; **nobody I can find pulls the Fisher/Amari–Chentsov tensors down to a base manifold
   through a section and a connection and computes the horizontal defect cocycle**
   (`thm:pb-fisher-defect-cocycle` `05c:1230`, `thm:pb-base-defect-cocycle` `05c:1267`,
   `thm:pb-anomaly-composition` `05c:979`). This is the paper.
2. **`thm:obs-local-global-potential`** (`05b:347`) — an *exact* local-to-global potential identity
   for correlated (non-mean-field) recognition laws on an agent hypergraph, with the exact
   overcounting identity. Bayesian mechanics (Ramstead/Da Costa/Sakthivadivel) constructs
   single-agent flows on statistical manifolds; it does not have this.
3. **The obstruction results** (`11_obstructions.tex`), especially
   `prop:obs-declared-root-unavoidable` (a rigorous no-go against self-closing hierarchies, i.e.
   against PIFB2's own Ouroboros apex) and `prop:obs-reciprocal-pair-kernel`
   (`dim ker J = dim ker(H − I)`, tying degeneracy to holonomy). Negative results of this
   specificity are rare in this literature and are the most referee-proof material in the corpus.

### 7.5 Where claimed novelty is already standard

- The associated-bundle construction itself (`def:geo-associated-bundles`) is textbook
  (`Nakahara2003` is cited — good). The `𝒞 → P → 𝓔` chain with local frames and transition
  cocycles is standard fiber-bundle theory; the manuscript is careful never to overclaim it, which
  is correct.
- Fields of statistical fibers with a gauge group and parallel transport between neighboring frames
  is **exactly** the setting of Cohen et al. 2019 (gauge-equivariant CNNs) and
  Weiler et al. 2021 (coordinate-independent CNNs). The vault knows this
  (`Research/wiki/themes/Gauge equivariance and geometric deep learning.md`; `Research/wiki/concepts/Agents as fibre-bundle sections.md`) and neither manuscript cites it.
- "Markov kernels form a category" and the DPI-with-equality material are standard
  (Čencov, Cho–Jacobs, Fritz).
- The Fisher-metric-contraction-under-coarse-graining idea is Bény–Osborne
  (`beny2015information`, in the bib, uncited in `Theory/`) — `thm:cg-fisher-contraction`
  (`06_general_coarsegraining.tex:170`) is a sharpened version of it and must say so.
- The forward-KL Gaussian barycenter (`prop:cg-gaussian-forward-kl-barycenter`) is moment matching;
  standard.

---

## 8. Summary table of required actions

| Priority | Action | Kind |
|---|---|---|
| P0 | Define `𝓕` on sections; prove well-definedness, gauge invariance, and design-restriction consistency | hard math |
| P0 | Prove N3(a) gauge-indistinguishability of the record law | easy math (assembly) |
| P0 | Add ~60 citations; rewrite `01_introduction.tex` with a related-work section | writing |
| P1 | Local-to-global decomposition over `𝒞` with exact defect | medium math |
| P1 | Section gradient flow + convergence on the exhibited finite-dim tier (`05d:235`) | medium math |
| P1 | Cite Chentsov / Ay–Jost–Lê–Schwachhöfer for fiber necessity | writing |
| P1 | Cite Fritz / Cho–Jacobs for the Markov-category material; add entries to bib | writing |
| P1 | Cite Cohen/Weiler/Bronstein and Sengupta–Friston; state the delta explicitly | writing |
| P2 | Split `07b_agent_network_rg.tex` out as a companion paper | organization |
| P2 | Compress the Gaussian tier from 4 chapters to 1 | organization |
| P2 | Add a one-page attention/transformer-limit remark (no experiment) | writing |
| P2 | Fix `cor:cg-holonomy-cross-morphism` (a corollary tagged HYPOTHESIS) | writing |
| P3 | Address Wasserstein/JKO: say why Fisher–Rao and not OT | writing |
