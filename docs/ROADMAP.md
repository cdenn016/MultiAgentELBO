# Roadmap: a fully built gauge-VFE theory of agents as local sections

*Written 2026-08-17, after the rescaling-map results. This document federates; it supersedes
nothing. `docs/STATUS.md` is the sole claim authority. `solid_RG_theory.md` §12 supplies the
meta-agent phase ordering and is used here as a working document, not an authority: STATUS §14
records that its release's certification apparatus carries stale domain approvals, an unauditable
provenance snapshot, and two open obligations, and the adjacent multiscale package is WITHHELD
under four high-severity findings (`docs/reviews/2026-08-16-claude-multiscale-vfe-rg-review.md`).
The rescaling design with its two amendments
(`docs/superpowers/specs/2026-08-17-rescaling-map-design.md`) is the authority for the RG
laboratory. Status markers follow STATUS: **P** proven, **D** derived under hypotheses, **C**
computed on an instance, **O** open, **R** refuted.*

## The target, stated once

The finished theory has six layers, and "fully built" means each layer closes its own exit gate
with evidence under the repository's verification discipline. Kinematics: a base context manifold
$\mathcal C$, a principal bundle $\mathscr P_G \to \mathcal C$ with a declared compact structure
group, and two associated bundles — $E_q$ with a belief-statistical-manifold fiber and $E_m$ with a
model fiber carrying an evaluation map $\operatorname{ev}: m \mapsto K_m$ — such that an agent is a
local section of $E_q \times E_m$ over its support $\mathcal C_i$. Action: one typed variational
free energy whose every term is either derived from a declared generative model or declared with
its price stated. Blocking: a reference-relative rule that forms parents from child blocks, with
its two routes and their competition explicit. Renormalization: the typed cocycle of
coarse-graining maps above a base point, with its checks and its fixed structures labeled by ratio
and architecture. Sections: the promotion of every pointwise object to local sections with gluing,
which is the layer that first licenses the phrase "agents as local sections" at all. Dynamics: the
coupled cross-scale action and the nonequilibrium mechanisms, gated last.

Today the theory is pointwise: everything established lives at one fixed $r_* \in \mathcal U_A$.
That is not a defect of the program but its declared staging — the layers below are ordered so
that no later layer's language is used before its gate closes.

## Layer K: kinematics

| Item | Status | Where |
|---|---|---|
| Compact link group declaration and its six consequences | **D** | STATUS §1 |
| Gauge structure requires a homogeneous fiber | **R** for generic families | STATUS §3 |
| SPD sector is matter, not gauge, under $O(K)$ | **D**, Gaussian-specific | STATUS §1, §3j |
| $\Omega_{ij}$ as free edge data (Regime II) | **D** | Tier-0 D1, settled |
| Notation standard (Phase 0) | **complete** | `solid_RG_theory.md` §12 |

What remains. The fiber class for $E_q$ and $E_m$ must be declared from the honest list: which
statistical families are homogeneous is answered by Koecher--Vinberg through Euclidean Jordan
algebras, a finite classification, and that reading task (STATUS §4) gates the declaration. The
compact subgroup and the representation channel (Tier-0 D3) must be declared together. Exit gate:
one declared triple (group, fiber, representations) with compactness and homogeneity hypotheses
attached to every downstream theorem that needs them.

## Layer A: the action

| Item | Status | Where |
|---|---|---|
| Exact two-channel finite ELBO, tied-replica | **P** | STATUS §2 |
| PIFB2 as gauge-motivated effective action | declared, not derived | STATUS §7 |
| Alignment term $\mathrm{KL}(q_i \| \Omega_{ij} q_j)$ in selected exact sectors | **P/C** | STATUS §2, §8 |
| Plaquette (Wilson) term as exact negative-ELBO component | **D, conditional model only** | STATUS §8 |
| $\lambda_0 = c \cdot \Sigma \|F\|^2$, linear | **C**, compact only | STATUS §2 |
| Wilson term wired into finite partition selection, budget identity | **C** | finite lab, 2026-08-17 |

The Wilson term's standing is the load-bearing subtlety. It is an exact ELBO component only after
declaring a random compact-link Gibbs--Haar generative model; it is not derived from the
fixed-link ELBO, and pretending otherwise is the kind of claim STATUS §7 forbids. The open
decision, Tier-0 in character: either adopt the random-link generative model as the declared
theory (the Wilson term is then derived, and links become random variables everywhere, including
in the RG layer), or keep fixed links and carry the Wilson term as a declared effective addition
with its coupling a parameter. The finite laboratory realizes either choice exactly and is the
instrument for pricing them. Exit gate: one typed action, every term derived-or-declared, realized
exactly on a finite instance.

## Layer B: blocking, which is where the stabilizer and curvature enter

The blocking criteria the theory already possesses, precisely stated:

- **Stabilizer route.** $\ker L_I \cong \mathrm{Fix}(\mathrm{Hol})$ is proven (Theory/09), and
  alignment forces holonomy into $\mathrm{Stab}(q)$, not to the identity (**C**). A block whose
  based holonomy fixes an admitted presentation can form a holonomy-blind parent. This is the
  $H \# Q = Q$ condition, and its lab form is the stabilized route of the mark-carrying module.
- **Retention route.** A block whose holonomy fixes nothing still forms a parent that carries its
  marks — root presentation, holonomy group, dressed boundary generators as one root-gauge orbit —
  at a declared capacity price. Blocking is therefore never forbidden, only priced (**C**, audited
  2026-08-17). Curvature enters as price twice: the retention charge and the Wilson term.
- **Transported agreement.** $\mathrm{KL}(q_i \| \Omega_{ij} q_j) \approx 0$ grades block quality:
  the downward kernels are Gibbs laws in exactly this transported mismatch, and approximate
  agreement is a total-variation statement (`solid_RG_theory.md` §5), not a new axiom.
- **What no criterion does: select membership.** The absolute law-valued selector is
  **COMPLETE_NEGATIVE** (STATUS §10). Selection is reference-relative by theorem, not by taste.
  The lab's declared mechanism is the partition posterior — block energies plus an Ewens or
  block-count prior — and the theory must own that this posterior is part of the declared model.

What remains. The extent problem is open (no criterion survived; the gap criterion provably cannot
bound extent for $\dim \mathcal C \ge 3$). The pointwise VFE closure and its defect
$\Delta_A$ are established (Phases 1--2); the comparison-category theorem (Phase 3) is the next
theorem in that line. Exit gate: a declared block-formation rule with proved gauge equivariance at
the theory level — the lab's C1 is the finite pilot of exactly that statement — and no canonical-
agentization claim anywhere.

## Layer R: renormalization above one base point

This layer moved decisively on 2026-08-17, and its results now constrain the others.

| Result | Status | Consequence |
|---|---|---|
| Complete step: coarse channel + Wilson-line connection + read-back + identification | **C**, tested | the step iterates |
| C1 gauge covariance to $10^{-12}$; parent law is frame data | **C** | pilot for Layer B equivariance |
| C2 holonomy conservation, exact; cut-loop defect closed | **C** | connection survives blocking |
| C3 compatibility $K_{b_1 b_2} = K_{b_1} K_{b_2}$ | **R** — defect 0.204 vs $10^{-10}$ | the flow is a typed cocycle |
| C6 composition defect, all factorization pairs, homogeneous 6-cycle | **C** — order one | typing is generic, not a tower artifact |
| Per-ratio passive composites contract (radius 0.83) to factorized fixed structures | **C** | pairwise coupling irrelevant in the passive channel |
| Passive fixed structures depend on the ratio (relative sup 0.81) | **C** | even endpoints are typed |
| Diagnosis: single-boundary-agent towers are quasi-one-dimensional | **D** | passive triviality was architectural |
| Wilson charge conserved: retained generators + coarse cycle span the fine cycle space | **C** | no loop's charge is dropped by blocking |
| Boundary multiplicity saturates: retention 0.156/0.441/0.564 at k = 1/3/6 | **C** | thicker boundaries cannot rescue the passive channel |
| Sector capacity, corrected 2026-08-18: root-framed belief-charge parents raise retention (0.209/0.568 vs 0.156/0.441 at k = 1/3), still below one | **C** | the 2026-08-17 null was a frame artifact of a gauge-dependent charge (audit F8); capacity was binding at this seed |
| M-info (amendment 9): MI retention R_MI ≤ 1 by data processing; 0.023→0.025 at k = 1 and 0.067→0.070 at k = 3 going from 9 to 27 labels | **C** | the blocking transmits 2–7% of boundary information; sup-norm retention overstates it by an order of magnitude; the sector gain survives in the law but small |
| M-part (amendment 10): the partition posterior, given the choice, selects the singleton partition (0.586) over direct (0.306) over staged (0.08/0.025); null control within 1% | **C** | no aggregation is free-energy-favored at this seed; staged is not preferred; the selection is prior-and-kernel dominated because the seed carries nothing to bind |
| M-bind (amendment 11): coupling-scale sweep lambda 0–100; ceiling grows as lambda² (5e-6 → 5e-2 nats) yet the modal class is singletons at every lambda and R_MI is flat-to-declining | **C** | no formation transition on this ray — the singleton preference is structural, not a weak-coupling artifact; transmission is kernel-limited, not signal-limited; the binding candidate moves to the likelihood sector |
| M-anchor (amendment 12): the environment restored as a blockable agent class; uniform anchors flip modal to direct (0.55/0.84), distinct control anti-binds (0.90 singletons), shared pairs pull the aligned blocking 8x | **C** | environmental binding licensed — condensation follows shared evidence, and the posterior selects the anchor-aligned placement, not just the ratio |
| M-flow (amendment 12): annealed joint dynamics on (x, R), sampler validated against the exact marginal; bare-instance verdict reverses quenched (direct 0.44 modal vs singletons 0.586) | **C** | the theory's process is more aggregation-prone than its frozen landscape; the M-part/M-bind negatives were statements about the quenched update on environment-free levels |
| Regenerated attention sustains interacting fixed structures (pair sup 0.58–0.62, sustained/injected 1.25) | **C** | horizontal glue is re-bound per level, not inherited |
| Typing survives regeneration (RC6 0.17–0.27; R-cross 0.64) | **C** | the cocycle reading governs both channels |

The last row reframes the oldest negative result. `Theory/07b`'s trivial fixed sectors and the
measured trivial fixed structures share one cause: the declared self-similar family joins blocks
through single boundary edges, and one-dimensional thin-boundary systems are trivial by
Perron--Frobenius. The theory's object is a directed $\beta_{ij}$ network, not a lattice, so the
lattice question "in what dimension does interaction survive" becomes "which $\beta_{ij}$
architectures renormalize to interacting fixed structures" — boundary multiplicity against
per-link attenuation, with hierarchical-graph RG (Berker--Ostlund, Migdal--Kadanoff) as the
network-native precedent for survival. Citations here are from memory and are not manuscript-ready
until checked.

Items 1 through 3 of the original ordered work closed on 2026-08-17/18 (the 07b cocycle
rewrite, Wilson-charge conservation, and the boundary-multiplicity sweep, run at the coupling
level on circulant instances), and amendments 4 through 8 added and answered the regeneration,
capacity, and robustness questions, with the capacity answer corrected under amendment 8 after
the 2026-08-18 audit retired the gauge-dependent sector charge. The alphabet-comparable
capacity statistic then closed the same day (amendment 9, M-info): retention is bounded by one
as a data-processing theorem, the blocking transmits 2–7% of the boundary information at the
declared seed, and the sector gain is confirmed in direction but only +10%/+5% relative — the
sup norm overstated both the retention and the sector effect. Participatory blocking then
closed as declared (amendment 10, M-part): given the choice, the Proposition-4 posterior
prefers no aggregation at all at this seed (singletons 0.586, direct 0.306, staged 0.08/0.025),
with the pair-free null control within 1% of the coupled posteriors — the same diagnosis as
M-info from the other side: the tiled seed's coupling content is informationally negligible, so
neither capacity nor formation questions have anything to bind on. Ordered work now:

1. Amendment 12 follow-ups. The environmental-binding question is answered (M-anchor: uniform
   anchors bind, distinct anchors anti-bind, shared pairs pull the aligned placement eightfold
   without crossing at the declared strengths) and the process-landscape gap is measured
   (M-flow: the annealed joint reverses the quenched verdict on the bare instance). Open in
   order of leverage: the shared-pairs condensation crossing (the anchor strength at which the
   aligned pairing becomes modal — bracketed above k_env = 8 or absent, one declared sweep);
   the regenerated channel composed with the environmental dressing (deferred in amendment 12);
   and the sight-limited participatory variant, whose staged-proposability prediction now has a
   live target since the annealed process actually favors aggregation.
2. Extended downward kernels for enlarged parent alphabets, which is what iterating
   sector-carrying parents requires (declared out of scope in amendment 6). M-bind prices this
   down: the sector gain stays small (+10% to +17% in R_MI) at every measured coupling, and
   transmission is kernel-limited, so a richer alphabet buys little until the kernel family
   itself changes.
3. Regenerated-channel dynamics beyond the fixed structure: attention temperature and occupancy
   are declared, not derived — deriving them from the coarse level's own row free energy is the
   theory-faithful upgrade and connects the RG layer to the attention theorems of Layer A.
4. Semigroup restoration as a separate design: a kernel family closed under composition, priced
   against what it costs the Bayes-exactness of the coarse channel. Regeneration removed its
   urgency for interaction but not for composability: both channels remain order-one typed.

## Layer S: from a point to sections

Phase 4 of `solid_RG_theory.md` §12, open. Promote every pointwise object — laws, parent data,
and now the RG step itself — to local sections over $\mathcal U_A$, with gluing, cocycle,
regularity, and path-consistency proofs, and with active-set changes, soft membership, and
stabilizer jumps treated rather than assumed away. Only past this gate does "agents as local
sections of $E_q$ and $E_m$" become licensed language, and only here does the new object this
roadmap adds appear: the RG cocycle as a family over $\mathcal C$ — whether the typed maps
measured at one $r_*$ vary covariantly as the base point moves, which is the precise form of
"renormalize the network above the manifold". The continuum question ($\Gamma$-convergence for
manifold-valued graph Dirichlet energies with a connection, Tier 2) stays behind this gate and is
not retired by lattice gauge theory.

## Layer D: dynamics and participation

Phase 5, open, gated last: fine dynamics, moving coarse maps, the semiconjugacy defect, one
coupled multiscale action without double counting, and only then any claim about sustained
nonequilibrium or agency. Nothing in the layers above feeds this one until Layer S closes, and the
static results must not be quietly promoted into dynamical ones.

## Standing verification debt

Two certification debts precede new construction on the meta-agent line, because a roadmap that
builds on withheld or under-certified releases inherits their defects silently.

First, the pointwise-datum release behind Phases 1--2: STATUS §14 keeps the mathematics ESTABLISHED
but records two open certification obligations, two stale domain approvals against edited sources,
and a provenance snapshot in which zero of fifteen entries verify. Closing those obligations, or
narrowing the ESTABLISHED label to what a refreshed certification actually covers, comes before any
Layer S work that cites the pointwise theorems.

Second, the multiscale two-channel graph-VFE package is WITHHELD with four high-severity findings
(random occupied sets ill-type the tower joint; the parent-coordinate Gibbs update omits live
descendant terms; the dressed-transport law omits the soft endpoint kernel; the convolution
converse is false) and six medium ones. Its repair order is declared in the review. Until repaired,
no layer may cite that package's promoted claims; its surviving structures — the edge-event law
$\eta$ as the graph-level coarse primitive with linear Markov pushforward, the retention of full
dressed-transport laws for non-flat connections, and the Reading A/B distinction — may be used
where the review says they survive. The review's external anchors (Garuccio--Lalli--Garlaschelli
2023 for prescribed-hierarchy closure; Zheng--Garcia-Perez--Boguna--Serrano 2024 for
protocol-relative weighted aggregation) also sharpen Layer R's framing: closure is relative to a
declared family and aggregation protocol, which is the same lesson C3 taught from inside.

## The spine, in one place

Immediate (weeks, on built machinery): R1 cocycle rewrite of 07b; R2 Wilson-charge conservation;
R3 bundled towers and the rate-versus-multiplicity sweep; R4 posterior-selected blocking; and, in
parallel, the standing verification debt — repair or narrow the two under-certified releases
before anything cites them. Declarations that gate everything upstream (Tier-0 in character): the
compact subgroup with its representation channel; the fiber class from the Koecher--Vinberg
reading; fixed-link-plus-declared-Wilson versus the Gibbs--Haar random-link model. Theorems next
in line: Phase 3 comparison category; Layer B equivariance at theory level; then Phase 4 sections
and gluing, which unlocks the RG-over-$\mathcal C$ object; then $\Gamma$-convergence; then
Phase 5. Every item carries the
standing discipline of STATUS §7: effective action, context manifold, semigeometries, compact
group, homogeneous fiber — and, added by this week's results, no autonomous-flow or fixed-point
language for the RG without a declared ratio and architecture attached.
