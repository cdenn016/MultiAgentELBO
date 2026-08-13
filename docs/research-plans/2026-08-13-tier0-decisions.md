# Tier-0 decisions

**Date:** 2026-08-13
**Repository state at authoring:** HEAD `2927b0e`, branch `main`, working tree clean.
**Status of this document:** input to a single sitting. Nothing here is a derivation.

## 0. What this document is for

Six declarations currently block the programme. Each of them is a question about what a symbol
*means* or what an object *is* — not a question about whether a theorem is true. None of them can be
settled by more computation, and each of them, left open, silently invalidates work that is already
written. This document states each question exactly, enumerates the real options, and prices what
each option costs and unblocks against the actual corpus at file and line.

The six declarations are expected to take one sitting. Five of the six are declarations only: the
mathematics is finished, and what remains is an author-level commitment. The sixth (D1) is also a
declaration, but choosing one of its branches obligates an erratum wave across five files.

Two things this document is not. It is not a recommendation to be rubber-stamped: each brief was
independently checked, and in four of six cases the checker overturned the brief's recommendation.
Where that happened, this document carries the checker's version and says so in the text. It is also
not a citation of numbers: every measurement reported below was recomputed in a session scratchpad
and none of it has landed in the repository, so per the standing rule at
`docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md:1415-1417` (O3) none of it is
citable. It is reported here as decision input, not as evidence of record.

### 0.1 Status markers

Every substantive claim below carries one of four markers.

| Marker | Meaning |
| --- | --- |
| **[PROVEN]** | A proof or `\status{ESTABLISHED}` block exists in `Theory/`, and the citation was read against the primary source during pricing. |
| **[COMPUTED]** | Measured numerically on one or two synthetic instances this session. Reproducible but **not in the repository**; not citable until O3 is discharged. |
| **[ASSERTED]** | Stated somewhere in the corpus with no proof and no measurement, or stated by a brief without support. |
| **[CHECKER]** | A correction that overturned or re-priced the brief. Where a checker and a brief disagree, the checker governs and the correction is carried in the text. |

### 0.2 Dependency order, and which to answer first

**Answer D1 first.** Not because it is the most important but because it is the only one whose answer
can make the others moot. Under one of D1's readings the agent-graph holonomy is exactly the
identity, the connection Laplacian has a kernel of dimension `K` at every configuration, and D2, D3
and D4 are questions about an operator with nothing in it. D1 costs one paragraph. Every other
decision should wait for it.

The sections below are ordered by dependency, not by label:

| Order | Decision | Gated by | Why here |
| --- | --- | --- | --- |
| 1 | **D1** Ω-typing | — | Under the coboundary branch, D2/D3/D4 are vacuous. |
| 2 | **D3** representation channel | D1 | An operator has no matrix until the representation is named, so D3 precedes D2. |
| 3 | **D2** operator and pencil metric | D1, D3 | The fibre metric is forced once the channel is named; the pencil metric is not. |
| 4 | **D5** β/γ side | D1 | Its forced half is independent of everything; its coarse-map half decides whether the operator is recognition-dependent, which D4 needs. |
| 5 | **D4** normalization lift | D1, D3, D2, D5 | Whether the meta-agent is a law depends on the operator, the channel, and whether the coarse map is recognition-free. |
| 6 | **D6** observation binding | — | Independent of all five. Finite, fixed-mesh, zero runtime cost today. Can be answered at any point. |

D6 can be signed at any time and is the cheapest of the six to execute if it goes one way and the
most expensive if it goes the other. It is placed last only because nothing waits on it.

### 0.3 Standing items that are not decisions

Three items surfaced during pricing that the PI should see but should not spend the sitting on.

**Ledger drift — open, not repaired.** `.verification/ledger.json` is pinned at
`git:d892374…`; HEAD is `2927b0e`, **seven** commits ahead: `43c1342`, `cbacfc6`, `9e08c3f`,
`0dc389d`, `59fdf9e`, `52ba348`, `2927b0e`. Earlier notes in the corpus say two or five; seven is
correct (`git rev-list --count d892374..HEAD` = 7). Mode is `triage`, eight claims, seven at HIGH,
one at MEDIUM, **all eight with `status: null`** — none verified. [CHECKER] Further: every
`artifact_revision` in the file is the *identical* string, at lines 4, 12, 18, 35, 41, 47, 64, 70,
76, 93, 99, 116, 122, 139, 145, 162, 168, 174, 192, 198 — it is a single repo-level pin, not a
per-file digest, so all twenty bindings drifted together when any of the thirty changed files
changed. `Theory/PIFB2.tex` itself is unchanged since the pin, so its *line* references remain
accurate; its *binding* does not. Separately, `.verification/active.json` — cited at worklog
`:896-899` — does not exist at HEAD; `.verification/` contains `history`, `ledger.json`,
`overview-agent-ontology-final.json`, `overview-agent-ontology.json`, `wave0`. Do not re-pin as part
of this sitting; record it and schedule it.

**O3 applies to this document.** Every `[COMPUTED]` entry below lives in a session scratchpad. Per
worklog `:1415-1417`, no such number is citable. Two of them are worth an hour to land in `tests/`
before any of these declarations is written into `Theory/`: the pure-coboundary holonomy triple
(D1), and the transported-edge-metric congruence test (D2/D3).

**A free repair, unrelated to the six.** The sha256 recorded at
`docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/pifb2-crosswalk.md:29` is
**65 hex characters** and is therefore not a valid SHA-256. The true digest of `Theory/PIFB2.tex`
(3956 lines) is `f80e6dabd9e5485649066e227e80beff1dd2b1082cf786bcdaeedb8cbd080ec4` [COMPUTED,
verified independently by the checker]. Fix it whenever that file is next opened.

## D1 — What does Ω_ij denote?

### D1.1 The question

`Theory/appendix_notation.tex:498-505`, under the heading **"Three transports that must remain
distinct"**, declares three objects and forbids conflating them:

> Ω_γ and Ω̃_γ move laws between fibers over different base points in one channel. T_ij^x(c)
> compares two coordinates in the same principal fiber. Θ_e^x is a declared edge-copy variable on
> the interaction complex. Only an explicit hypothesis may identify the represented Θ_e^x with
> parallel transport along an assigned base curve.

[PROVEN — read verbatim at `Theory/appendix_notation.tex:498-504`.]

In the standing coupling contract β_ij D_KL(q_i ‖ (Ω_ij)_# q_j) at `overview.md:48-49`, and in the
tied-replica source u_ab = (Ω_ab)_# q_b at
`docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/typed-construction.md:51`, which
of the three is Ω_ij — and if it is Θ_e, is it permanently specialized to the coboundary
Θ_e = U_i U_j^{-1} of `hyp:geo-flat-links`?

### D1.2 What it blocks

Nothing that reads a loop product can proceed. Under the coboundary reading every agent-graph loop
product is the identity, measured at 3.97e-15 on a 5-cycle-plus-chord witness and 3.72e-15 on a
triangle [COMPUTED]. That makes vacuous, in the strongest sense of the word:

- worklog `:713-719` §3e.2(i), the Stab(q) result and its ‖H−1‖ = 0.0895 witness;
- worklog `:734-738` §3e.2(iv), λ₁ as a frustration order parameter;
- worklog `:752-757` §3e.2(vi), the structure-group flow G → Stab(q);
- worklog `:721-726` §3e.2(ii), two-tree agreement;
- `Theory/09_coarsegraining.tex:390-398` `eq:cg-fixed-rank`;
- `Theory/07b_agent_network_rg.tex:1648-1673`, the based holonomy representation;
- `Theory/02_geometry.tex:557-641`, the whole of §sec:geo-regime-two;
- `Theory/PIFB2.tex:387-418`, the Wilson observable and S_Wilson.

It also blocks obligations O5, O6, O10, O12, O14, O15 and O16 (worklog `:1426-1505`), each of which
is a statement about the spectrum, kernel or curvature of an operator built from Ω. The worklog says
it in terms at `:1226`: *"nothing should be built until it is [settled]."*

### D1.3 If the coboundary reading is correct, an entire line of work is vacuous

This must be said without softening, because the corpus currently under-states it in one direction
and over-states it in another, and a decision made on the current text would be made on a wrong
price sheet either way.

If Ω_ij = U_i U_j^{-1}, then:

1. **Every agent-graph loop product is the identity, by a one-line telescoping proof.** No
   experiment can produce otherwise. The measured 3.97e-15 is floating-point error, not a small
   holonomy. [COMPUTED, and [PROVEN] as algebra.]
2. **λ₁ of the connection Laplacian is identically zero and dim ker L^Ω = K at every
   configuration.** Measured: (a) coboundary gives exactly three zero eigenvalues at K = 3 with
   λ₁ = 0; (c) non-coboundary gives λ₁ = 2.19e-2 and dim ker = 0 [COMPUTED]. The "frustration order
   parameter" has no referent.
3. **The `Theory/07b` tree-dependence defect does not exist, and neither does its repair.** Two
   distinct spanning trees give compressed meta-states agreeing to 1.64e-16 relative [COMPUTED] —
   *for free*, as an identity. worklog `:721-726` reports 2.0e-16 as a *result*; under the
   coboundary reading it is a tautology. A cocycle test on a coboundary-constructed transport tests
   only floating-point error. So the three prescribed `07b` edits at worklog `:1362-1370` become
   unnecessary.
4. **`Theory/09` `prop:cg-kernel-holonomy` loses all content**: f_I = K · (number of components), a
   constant. [PROVEN, given the reading.]

The corpus's own statement of this, at worklog `:1411-1412`, is wrong in **both** directions.

- It **under-counts**: it does not list §3e.2(ii)'s two-tree agreement, which is an identity under
  the coboundary reading and therefore empties along with the rest.
- It **over-counts**: it asserts that "the entire geometric-phase construction of §3f.2 step 4" is
  empty. That is false, and it was measured twice, by the brief and independently by the checker.
  With pure coboundary Ω, ambient connection A ≡ 0, and P the exact rank-K kernel projector of L^Ω
  over a 2-D base, the Wilczek–Zee curvature of the coherent subbundle is **nonzero**:
  ‖F^M‖_F = 6.557e-01 with Kato meta-holonomy per unit area 0.6554 as r → 0, matching the direct
  curvature to 0.05%; the checker reproduced the phenomenon independently at ‖F^M‖_F = 1.1235 on a
  different seed [COMPUTED, two independent instances]. The control — forcing a common Maurer–Cartan
  form U_i = g_i V(c) — drives it to 1.34e-19. The mechanism is the Gauss equation
  F^M = P F^ω P + II′∧II with the first term zero and the second not: a subbundle of a *flat* bundle
  need not be parallel (Kobayashi–Nomizu 1963, Ch. II §7). The kernel is
  span{(U_1(c)w, …, U_N(c)w)}, a subspace that moves with c unless the U_i share a common right
  factor.

So under the coboundary reading the honest accounting is: §3e.2(i), (ii), (iv) and (vi) are empty;
§3f.2 step 4 survives; the corpus says the opposite of both halves.

### D1.4 What the corpus actually says

**`Theory/` is internally consistent and already answers the question.** `Theory/02_geometry.tex:561`
`def:geo-graph-links` declares "a finite interaction multigraph 𝔍 = (V, E, ¯) declared
**independently** of 𝒞", with a fixed-point-free reversal involution, parallel copies allowed, and
only Θ_ē^x = (Θ_e^x)^{-1} imposed [PROVEN, read verbatim]. `Theory/02:587-588` states the links are
"not determined by the other, by h_i, by Φ or Φ̃, **by pointwise frame comparison**, or by a
principal connection". `Theory/02:618-621` states the decision in terms: "For T^x evaluated at one
common context the criterion is automatic by the Čech cocycle law. Its nontrivial graph content
concerns the independently declared Θ^x." The coboundary specialization is `hyp:geo-flat-links` at
`Theory/02:645-654`, carrying `\status{HYPOTHESIS}`. `Theory/09_coarsegraining.tex:346-350` types
Θ_e as free GL(K) with Θ_ē = Θ_e^{-1} and W_e ≻ 0 and **no cocycle**, then builds Hol_{r_α} and
`eq:cg-fixed-rank` on that alone.

**`Theory/PIFB2.tex` is also self-consistent and takes the opposite default.** `:311-315`
`eq:transport_def` defines Ω_ij(c) = exp[φ_i(c)] exp[−φ_j(c)]; `:320-334` `thm:vanishing_holonomy`
proves H_ijk = I from it; `:436` says the working framework "sacrifice[s] path-dependent parallel
transport (holonomy) … altogether (Regime I flatness)". But PIFB2 also already writes the escape at
`:373-380` `eq:edge_relaxed_omega`, Ω_ij = U_i exp(δ_ij·G) U_j^{-1}, "the standard lattice-gauge
link variable [Wilson 1974; Kogut–Susskind 1975; Creutz 1983]", with the link law
Ω_ij ↦ g_i Ω_ij g_j^{-1} at `:382`.

[CHECKER] The brief called `overview.md:43` "the single defective line". That over-reaches twice.
First, `overview.md:43` reads `| Ω_ij, Ω̃_ij | fiber maps | transports of belief / model from j's
frame into i's |` — a type and a direction, both of which the represented Θ_e satisfies, since
Ω_ij = U_i τ_ij U_j^{-1} does map j-frame content into i's frame. The defect at `:43` is
**under-specification, not misassignment**. Second, `Theory/PIFB2.tex:208` is a stronger and
uncited locus: it identifies Ω_ij *as* the Čech transition function, states it "satisfies the Čech
cocycle condition", says "this Čech data is the coboundary of the family {U_i}", and declares
"Transition data that is not a coboundary (nontrivial bundle topology) is out of scope". That
paragraph is the strongest textual evidence in the corpus for the coboundary reading and the brief
never cited it. In fairness to PIFB2, the same paragraph already separates Ω_ij's two roles —
"Ω_ij enters as a transport operator between agents rather than as a gluing map" — and already points
at the Regime-II promotion "in which the link variables acquire an independent edge-local connection
δ_ij". So `:208` is a re-scope, not a contradiction; but it is a full paragraph, not a line.

**The shipped code implements the Θ_e reading.**
`src/multiagent_elbo/geometry/discrete_holonomy.py:590-605` `passive_transform_links` applies
Θ′_e = A_target^{-1} Θ_e A_source, the link-variable law of `Theory/02` `eq:geo-regime-two-gauge-law`,
and `:554-575` `trivialization_via_spanning_tree` *tests* whether a link family is a coboundary
rather than constructing it as one. [CHECKER] This is narrower than the brief presented it: those are
holonomy-lab entry points over hard-coded GL⁺(2), and there is **no** simulator in this repository
that computes β_ij D_KL(q_i ‖ (Ω_ij)_# q_j) from vertex frames. The code shows the holonomy
*tooling* is Θ-typed; it does not show the coupling *path* is.

**The panel's own live construction already assumes the answer.** worklog `:1065` (§3f.2 step 1)
writes Ω_ij(c) = φ_i(c)^{-1} τ_ij(c) φ_j(c) — option (c) up to the naming convention U_i := φ_i^{-1}.

**Sibling-manuscript precedent, verified verbatim.**
`C:/Users/chris and christine/Desktop/Research/manuscripts/verified-ledger.md:134`: "**Regime-I
holonomy is exactly trivial; any open holonomy question belongs to edge-relaxed Regime II.**" The
same reduction applies here without modification: it is a statement about the parameterization
Ω = U U^{-1}, not about the fiber, the group, or the base.

### D1.5 Options

Five options, not three. The dispatch's original set omitted the third transport named in the
question (Ω_γ) and substituted a fourth object; the checker put Ω_γ and a separated variant of the
coboundary branch back on the sheet, and both are material.

| | Option | One-line statement |
| --- | --- | --- |
| **(a)** | Pure coboundary | Ω_ij is T_ij under `hyp:geo-common-trivializations`; Ω = U_i U_j^{-1}; no independent edge datum exists. |
| **(a′)** | T_ij as a Čech cocycle, **without** declaring P\|𝒞₀ trivial | Ω_ij is T_ij; the cocycle law is automatic at `Theory/02:495-503`, so holonomy is already e_G, but the bundle-topology sector survives. |
| **(b)** | Per-agent principal bundles | Each agent carries P_i → 𝒞_i with its own ω_i; Ω_ij is a declared bundle isomorphism over the overlap. |
| **(c)** | Represented interaction-complex link Θ_e | Ω_ij := ρ̂_b(Θ_{e(j→i)}), free G-valued edge data, link law Ω ↦ g_i Ω g_j^{-1}; the coboundary is `hyp:geo-flat-links`, a specialization. |
| **(d)** | Base parallel transport Ω_γ | Ω_ij := Ω_{γ_ij} under `hyp:geo-graph-base-transport` (`Theory/02:625-634`), with a declared curve assignment γ_e. |

**Option (a) — pure coboundary.**
*Unblocks:* immediately consistent with `PIFB2.tex:208`, `:311-336` and `:436` as written, and with
the sibling GL(K) ledger. No new mathematics is owed. Removes the Wilson-action coercivity problem
from the agent-graph sector, since there is no independent connection to fund.
*Costs:* forfeits the only non-Gaussian route to a "meta-agent" object — with λ₁ ≡ 0 the
Bandeira–Singer–Spielman frustration constant is identically zero, so criterion (A) of worklog
`:913-935` degenerates and criterion (C) becomes the only surviving coarse-graining criterion. Also
forfeits worklog `:1321-1334` §3f.4 item 4's fixed-ray RG sector, whose "pair Hoeffding coordinate"
is literally wΘ_ij.
*Empties:* the nine items listed in §D1.2, with the corrections of §D1.3 — §3e.2(ii) empties (the
brief's list under-counted) and §3f.2 step 4 does **not** (the corpus's list over-counted).
*Downstream:* promote `hyp:geo-flat-links` (`Theory/02:645-654`) to a standing declaration and strike
or re-scope `Theory/02:587-588` and `:618-621`, which assert the opposite; add the coboundary
constraint to `Theory/09:346-350`; restate `Theory/09:379-399` with f_I = K·(#components); rewrite
`Theory/07b:1618-1724` as coboundary bookkeeping; mark `PIFB2.tex:373-418` an unrealized extension
and strike `:2138` item C1. [CHECKER] Three corrections to the brief's rewrite list: (i)
`overview.md:433` needs **no** edit — its B4 row is entirely about the §8 curve-mediated
presentation and contains no graph-transport clause; the item to withdraw is the second half of
worklog `:746-750`. (ii) `overview.md:435` must be **struck** from the rewrite column — that row is
about the ambient principal connection and the κ‖F_A‖² coercivity question, which survives all
options unchanged; only the `PIFB2.tex:408` half of the citation is an agent-graph item, and (a)
does retire that. (iii) `overview.md:43` needs no edit under (a). Conversely, (a) must **add**
`PIFB2.tex:416` and `:449` to its rewrite column: `:449` reads "Opt-in/test-only: independent
pairwise connection transport. The checked-in pairwise twist scale and learning rate are zero, so
that path is inactive" — deactivated, not abolished, whereas (a)'s own statement abolishes it.
*New obligation:* (a) is inconsistent with `hyp:geo-graph-base-transport` (`Theory/02:625-634`)
whenever the base connection has nontrivial represented monodromy on a graph-realizable loop, and
parallel edge copies are explicitly permitted at `Theory/02:562`. Under (a) either that hypothesis is
withdrawn, or §8's Θ ≠ 0 configuration cannot be realized on the agent graph.
*Reversibility:* cheap in text, expensive in credibility — un-promoting a hypothesis later restores
nine results a companion erratum had withdrawn.

**Option (a′) — the cocycle without the bundle triviality.** [CHECKER — this option was missing.]
Option (a) silently bundles two separable declarations. Declaration 1: Ω = T_ij. By
`eq:geo-cech-cocycle` at `Theory/02:495-503` (`\status{ESTABLISHED}` at `:504`, proved at `:506-508`
from uniqueness of the same-point coordinate change), T_ij T_jl = T_il holds **automatically** — so
declaration 1 alone already forces the agent-graph holonomy to e_G with no triviality assumption.
Declaration 2 is `hyp:geo-common-trivializations` (`:538-549`, `\status{HYPOTHESIS}`), which declares
P|𝒞₀ trivial and only then yields the global coboundary form. Under (a′) the entire nine-item
empties list still fires verbatim, but `eq:geo-cech-class:512-516` and the bundle-topology sector
**survive** — which matters, because `overview.md:433` explicitly keeps the bundle-topology clause
alive and names T² (curvature) and S² (Chern classes) as its tests. Option (a)'s parameter count —
"(N−1)·dim G parameters, with the |E| edges carrying zero further content" — is valid only under
declaration 2 and is wrong under (a′). **A PI choosing the coboundary branch should know he can have
holonomy-triviality without buying bundle-triviality.**

**Option (b) — per-agent bundles.**
*Unblocks:* formally licenses nontrivial loop products; gives PIFB2's per-agent connection A^{(i)}
(`PIFB2.tex:349-358`) an honest home.
*Costs:* strictly dominated. The set of equivariant isomorphisms P_j|𝒞_ij → P_i|𝒞_ij is a torsor
over Gau(P_i|𝒞_ij); the loop product is the identity or not exactly according to an *independent
choice inside that torsor* — which is the same G-valued datum τ_e that option (c) declares directly.
(b) therefore buys, over and above (c), only the global freedom [P_i] ≠ [P_j], at the price of
re-typing the ambient geometry chapter. [CHECKER] Two corrections. First, (b) does not *falsify* an
ESTABLISHED result: the `\status{ESTABLISHED}` tag at `Theory/02:524` certifies the implication and
the characterization, which hold verbatim per agent; "There is one principal bundle" at `:510` is an
ambient setup declaration, and (b) revises a declaration. Second — and this is a real defect the
brief missed — (b) **does** empty something. Its own statement scopes Ω_ij to an overlap 𝒞_ij, but
`Theory/02:562` declares the interaction multigraph independently of 𝒞, and the coupling contract at
`overview.md:48-49` and `typed-construction.md:38-51` conditions only on finite source sets J_a^q
with no support-overlap predicate, while agents carry compact supports. Under (b),
β_ij D_KL(q_i ‖ (Ω_ij)_# q_j) has **no argument** for any disjoint-support pair. (b) silently
re-couples the agent graph to base-overlap structure, and its own new-obligation list covers only
overlaps where P_i ≇ P_j, not 𝒞_ij = ∅, which is the live case.
*Reversibility:* hard. Reverting means re-establishing the single-Čech-class theorem and re-auditing
`Theory/05c` and `06a`.

**Option (c) — the represented link Θ_e.**
*Unblocks:* everything in (a)'s empties list, restored as live content, plus O5, O6, O10, O12, O14,
O15, O16. Measured contrast on one witness: ‖H−I‖_F = 1.640 vs 3.97e-15; λ₁ = 2.19e-2 vs 0;
dim ker L^Ω = 0 vs 3 [COMPUTED]. Sharpens `overview.md:433`'s B4 row rather than emptying it — the
≥3-base-point cocycle-consistency test named there is exactly the coboundary test
`discrete_holonomy.py:554-575` already implements, so O15 becomes a runnable experiment rather than a
fiat answer.
*Costs the exact two-channel theorem nothing.* Measured: tied-replica edge-KL sum
34.472343526719 vs 34.472343526719, |Δ| = 0.000e+00 bit-identical, under a GL(3) lattice gauge with
a transport family whose cocycle residual is 1.42 [COMPUTED]. The derivation's own hypotheses require
only measurability (`typed-construction.md:42-46`) and the endpoint-conjugation link law
(`gauge-invariance-proof.md:18`) [PROVEN, read at source].
*Real costs, three, all bounded.* (1) `PIFB2.tex:320-334` `thm:vanishing_holonomy` must acquire an
explicit "Regime I, δ_ij = 0" scope tag rather than being "invoked throughout the manuscript"
(`:318`). (2) `PIFB2.tex:2570`'s cross-observer consensus is the one genuine cocycle consumer found
in the corpus; the sentence already fences itself, so this is a scope tag, not a retraction. (3)
[CHECKER — re-priced from an obligation to a cost] The τ_e become state-bearing data with no
declared prior or action. For noncompact GL⁺(K) the Wilson trace action is unbounded below
(`PIFB2.tex:408`) and the Frobenius plaquette penalty is not conjugation-invariant (`:416`). If τ is
dynamical, (c) inherits a coercivity problem that (a) does not. This belongs in the cost column, not
in a downstream footnote, and it leans on `overview.md:558-560` (open decision 7) going a particular
way.
*Empties:* nothing. Two things are demoted from theorem to specialization: `hyp:geo-flat-links`
(already `\status{HYPOTHESIS}`) and `PIFB2.tex:449`'s executable-contract row, which is a statement
about a config default, not about the theory. A non-default opt-in path existing is what matters; its
being off by default is not a defect and must not be filed as one.
*Downstream — re-priced.* [CHECKER] The brief called this "short". It is not. `overview.md:43` gains
a disambiguating cross-reference (not a retyping); `overview.md:433`'s B4 row is strengthened;
`overview.md` §9 gains a line noting item 7 now gates the τ-sector action. On the PIFB2 side the
cost is materially larger than the brief's three lines: `:320` (lemma scope tag), `:2570` (consensus
scope tag), `:436` (rephrase as a statement about the checked-in configuration), **plus** `:208` (the
transition-function paragraph must be re-scoped in full), `:311-314` (the *defining* equation becomes
a specialization, so the equation is retyped, not merely its lemma), and `:2216` (the natural-gradient
appendix derives every gradient through the two-exponential parameterization). No change required to
`Theory/appendix_notation.tex:498-504`, `Theory/02:557-641`, `Theory/09:346-350` and `:379-399`,
`Theory/07b:1648-1673`, the exact two-channel derivation, or `discrete_holonomy.py`.
*New obligations:* (i) declare Θ_{e(i→i)} = e_G explicitly — the tied-replica source set J_a^q does
not exclude b = a, and under (c) Ω_aa = I is a declaration rather than an identity; (ii) replace the
coboundary fast path `Theory/02:663-666` by `eq:geo-regime-two-residual:669-673`, which `Theory/02`
already supplies; (iii) declare whether τ obeys a cocycle on triples (it must not, or (c) collapses
to (a) up to conjugation) and whether the τ are dynamical or fixed data; (iv) [CHECKER] **re-index
the tied-replica construction from ordered pairs to oriented edges.** `Theory/02:562-563` allows
parallel copies and indexes Θ_e by oriented edge; `typed-construction.md:38-51` indexes transports by
ordered pair, Ω_ab^n : 𝖪_b → 𝖪_a, with no edge index. Under (c) the standing contract cannot express
two distinct links between the same ordered pair — which is exactly the configuration `overview.md`
§8's two-path witness uses.
*Reversibility:* the most reversible of the five. Specializing back is exactly setting τ ≡ e_G, i.e.
invoking `hyp:geo-flat-links`, which remains in the manuscript. No ESTABLISHED result is contradicted
in either direction.

**Option (d) — base parallel transport Ω_γ.** [CHECKER — this option was missing, and it is the
third transport the question itself names.]
*Statement:* Ω_ij := Ω_{γ_ij} under `hyp:geo-graph-base-transport` (`Theory/02:625-634`,
ρ̂_b(Θ_e^b) = Ω_{γ_e}), with a declared curve assignment γ_e.
*Unblocks:* it makes `overview.md` §8's U(1) curve-mediated witness an **instance** of the standing
contract rather than an exception. It is the only reading under which ω becomes an argument of a
generative kernel, so the record-law state-bearing criterion at `overview.md:75-87` applies to the
connection directly — which is precisely why B4's holonomy clause is currently unavailable on the
graph. It costs the `Theory/09` and `07b` holonomy machinery nothing, since represented graph-loop
products then equal base-loop parallel transports (`Theory/02:637-640`).
*Costs:* it converts `overview.md` §9 item 5 ("which curve mediates inter-agent transport") from a
side question into the gating decision, and it requires a declared γ_e for every edge. Not priced
further: this option was surfaced by the checker and has not been traced through the corpus at the
level the other four have. **It is not yet fully priced, and the document says so rather than
guessing.**

**A de-overloading hybrid, worth a sentence.** [CHECKER] Nothing forces one symbol to win. The
corpus already types both objects distinctly at `Theory/appendix_notation.tex:498-504`. The hybrid:
declare Ω_ij := ρ̂_b(Θ_{e(j→i)}) as a defined abbreviation for the standing contract, and add a
separate `overview.md` §2 row for T_ij carrying the existing `:43` wording. Under this route
`PIFB2.tex:208` keeps Ω_ij-as-transition-function under the T name with **zero** rewrite, and the
edits land instead on `overview.md:48-49`, `overview.md:352-353` and `typed-construction.md:38-51`.
Given that (c)'s real PIFB2 cost is six loci rather than three, this may be the actual cheapest
route.

### D1.6 Recommendation

**Option (c), with `hyp:geo-flat-links` retained as a named specialization.** The checker upheld the
recommendation and re-priced it; the re-pricing is carried above.

Five reasons, in decreasing weight.

1. **It is not a new commitment.** `Theory/appendix_notation.tex:498-504` already names three
   transports and assigns the agent graph to Θ_e; `Theory/02:587-588` and `:618-621` already state
   that the graph content is the independently declared Θ; `Theory/09:346-350` already types Θ_e as a
   free GL(K) link with no cocycle and builds `prop:cg-kernel-holonomy` on that alone. [PROVEN, all
   four read at source by two independent readers.] The corpus is consistent; `overview.md:43` is
   under-specified and `PIFB2.tex:208` reads the other way.
2. **It costs the load-bearing theorem nothing.** The tied-replica edge-KL sum is bit-identical under
   a GL(3) lattice gauge with cocycle residual 1.42 [COMPUTED], and the derivation's hypotheses
   require only measurability and the link law [PROVEN at `typed-construction.md:38-46` and
   `gauge-invariance-proof.md:15-25`].
3. **Option (b) is strictly dominated** — it delivers no holonomy that (c) does not, and it breaks
   the coupling contract on disjoint-support pairs.
4. **Option (a) is coherent and cheap but its price sheet in the corpus is wrong in both
   directions**, as set out in §D1.3. A decision taken on worklog `:1411-1412` as written would be
   taken on bad information.
5. **It is what the holonomy tooling executes** — `discrete_holonomy.py:590-605` applies the link law
   and `:554-575` tests trivializability. [CHECKER: narrower than the brief claimed; the coupling
   path is not implemented anywhere in `src/`.]

**Consider (a′) before signing (a), and price (d) before rejecting it.** If the PI's instinct is the
coboundary branch, (a′) delivers the same holonomy-triviality while keeping the bundle-topology
sector that `overview.md:433` still names as live. And (d) is the only reading that makes §8 an
instance rather than an exception; §8 is already running it.

### D1.7 What would overturn the recommendation

1. A load-bearing use of the cocycle Ω_ij Ω_jk = Ω_ik inside `Theory/` that cannot be re-derived or
   scope-tagged. Exactly one consumer was found — `PIFB2.tex:2570` — and it already fences itself in
   the same sentence. A second, unfenced consumer inside `Theory/` would shift weight to (a).
2. A decision on `overview.md:558-560` (item 7) in favour of full GL(K,ℝ) **together with** a
   demonstration that no bounded-below, conjugation-invariant action exists for the τ_e sector.
   `PIFB2.tex:408` and `:416` already establish half of that; if no admissible prior can be
   exhibited, (c)'s τ are undeclarable dynamical data and (a) becomes the honest reading.
3. A demonstration that the §3e.2(i) witness (‖H−1‖ = 0.0895) was generated from a coboundary family
   — impossible at 3.97e-15 by computation, but the witness lives in a session-local scratchpad (O3)
   and could not be read.
4. A decision to withdraw `hyp:geo-graph-base-transport` outright, which severs τ from any
   base-connection interpretation and reduces (c) to bookkeeping with no geometric warrant.

### D1.8 Cost to decide

Declaration only. Option (c): one clarifying line at `overview.md:43`, two scope tags plus four
re-scopes in `PIFB2.tex` (`:208`, `:311-314`, `:320`, `:436`, `:2216`, `:2570`), and **no change to
`Theory/`**. Option (a) or (a′): a comparable declaration plus a companion erratum wave across five
files — a day of editing plus the withdrawal of nine results. Option (b): weeks; it needs
`Theory/02` §sec:geo-cech rewritten and `Theory/05c` re-derived. Option (d): unpriced.

## D3 — In which representation is the coherent block defined?

### D3.1 The question

Is "the coherent block of a meta-agent" defined in the defining/vector representation acting on the
belief mean, the symmetric-square representation acting on the covariance by congruence, the full
Gaussian belief (μ, Σ) as one object, or the separately-declared model-channel representation ρ_m
with (γ, Ω̃)?

### D3.2 What it blocks

Nothing that says "meta-agent" has a referent until this is fixed. Criterion (A) at worklog
`:913-935` and construction step 1 at `:1062-1071` are declared μ-only with the fence "the Σ-channel
needs a different Laplacian on ℝ^{N·K(K+1)/2} built from ρ_Sym2(Ω), with a different rank and a
different gap locus". worklog `:1193-1199` lists "a declared representation channel" as a hypothesis
the programme has **not** granted, so every gap, λ₁, wall and extent number in §3f is conditional on
it. `Theory/09:373-375` defines Fix(Hol) on ℝ^K and `:379` proves ker L_I ≅ Fix(Hol) in that space
alone — the theorem the whole compression rests on is a defining-representation theorem.

[CHECKER] **This decision *is* obligation O6** (worklog `:1432-1437`): "Declare the representation
channel — μ, Sym², or the model channel — or prove the three coherent blocks coincide. *Settled by:*
computing all three on one configuration and reporting whether the coherent index sets agree." That
computation has now been done, so O6's evidential half is discharged and only the declaration
remains. Price it as a declaration, not as a declaration plus a day.

### D3.3 What the corpus says, and the contradiction

**The corpus already answers this and §3f contradicts it.** `Theory/02_geometry.tex:80-95` declares
one representation per channel on the sample space, ρ_b : G → Aut(𝖪) and ρ_m : G → Aut(𝖬), with the
action on laws declared to be the pushforward, ρ̂_b(g)q = (ρ_b(g))_# q, and a warning at `:97-99`:
"Multiplying a matrix into a density is not the pushforward." `prop:geo-moment-pushforward` at
`:427-441` states the consequence: one and the same R = ρ_b(g) gives μ′ = Rμ **and** Σ′ = RΣRᵀ.
[PROVEN, `\status{ESTABLISHED}`.] So the Sym² action on Σ is not an independent channel — it is the
induced second-moment action of the single declared ρ_b. Meanwhile `Theory/02:87` states that ρ_b and
ρ_m "need not be equivalent, faithful, or of equal dimension", so the model channel genuinely is a
third, incommensurable extent, by declaration.

**The contradiction:** worklog `:1068-1071` and `:1193-1199` treat μ and Sym² as two
separately-choosable channels; `Theory/02:89-99` and `:427-441` say they are one pushforward. Nothing
in `Theory/` licenses a μ-only transport of a belief.

**The premise of the obligation is confirmed by measurement.** On a K6 complete graph, K = 3, SO(3),
with a frustration criterion at threshold 0.02 over 57 subsets: |μ| = 56, |Sym² with trace| = 57
(**every** subset — the criterion is vacuous), |traceless Sym²| = 42, |model| = 50; μ ⊃ traceless-Sym²
strictly with |μ \ Sym²₀| = 14; model is not nested. On a second configuration with a state-based
criterion: |mean| = 12, |covariance-AIRM| = 10, |model| = 4, |all three| = 2. [COMPUTED, two
instances.] dim Fix(Hol) also differs between representations at the same holonomy: vector / Sym² /
traceless = 1/2/1 for a generic rotation, 0/1/0 for a dense SO(3) pair. **The three index sets do not
agree.**

Two further findings that were not in the panel. First, the Sym²-with-trace criterion is vacuous
because the identity section Z_i ≡ I satisfies I − ρ(R)I = 0 for every R ∈ O(K), so Sym² always
contains the trivial representation and λ₁ ≡ 0 [COMPUTED, 1.8e-16]. Second, **the Sym² coherent
block leaves the SPD cone**: drawing 4000 random representatives from a rank-m block gives 0.0%
non-PSD at rank 1, **54.5% at rank 2**, 75.7% at rank 3, and every traceless representative has
tr X = 0 hence λ_min < 0 < λ_max and is never a covariance [COMPUTED].

**A corpus instance of the same divergence, uncited by the brief.** [CHECKER] `Theory/09:815-832`
already exhibits H = diag(1,−1,−1) ∈ SO(3) with nontrivial represented holonomy and f_I = 1 < K which
nonetheless preserves N(0, σ²I₃), so "all transported marginal KL values zero"
(`\status{ESTABLISHED}`), with the moral at `:830-832`: "Transported KL therefore measures marginal
occupation of the available law modes, not the dimension of the state-independent structural fixed
section." That line must be re-scoped by any option whose coherence criterion *is* a transported
divergence.

### D3.4 Options

| Option | Statement | Verdict |
| --- | --- | --- |
| (a) mean only | Block defined in ρ_def on ⊕ℝ^K; Σ and model play no part. | Requires a new declaration contradicting `Theory/02:89-99`; the meta-agent is then not an agent. |
| (b1) ℝ^K ⊕ Sym(K) as one linear rep | One Laplacian on the reducible sum. | Sym² summand is vacuous on compact G (57/57 subsets admitted); block representative is non-PSD 54.5% of the time at rank 2. |
| (b2) Gaussian manifold, Fisher/AIRM | Single pushforward; edge discrepancy is the transported Gaussian divergence; meta-belief is (precision-weighted mean, AIRM Karcher mean). | Typing correct; representative half is where the checker overturned it. |
| (c) two or three separate notions | Channel-labelled extents, never combined. | Contradicts `Theory/02:89-99`; leaves "the extent" two- or three-valued, which is what O6 exists to remove. |
| (d) coherent in **all** channels | Conjunction across μ, Σ and model. | Rejected: the model conjunct is not type-checkable (`Theory/02:87` gives no intertwiner) and contradicts `overview.md:47-49`'s doctrine that agents may hold different generative models. Rarity 1.2× to >100× against mean-only [COMPUTED]. |
| **(b2-minus)** mean tie with **free** covariance | Single pushforward, both moments define the extent, but covariances are **not** aggregated; the meta-belief is the tied mean with per-agent covariance retained. | [CHECKER — missing option] The object `Theory/` already proves finite. |

**Option (a) is mispriced in the corpus and in the brief.** The brief prescribed weakening
`Theory/02:403-416` `def:geo-agent` to admit a mean-vector object. [CHECKER] That is the wrong
prescription — it would propagate to `def:geo-associated-bundles` and contradict `overview.md:35`
("The action **must** be by pushforward"), damaging the typing of every *ordinary* agent to
accommodate the meta-agent. The honest consequence of (a) is that the meta-agent is simply **not an
agent**: price it as "a structural block, not an agent", which is a smaller edit and a larger
scientific cost. `overview.md:14-18`'s agent-only ontology and the hierarchy aspiration are what
break, not the definition.

**Option (b2) and where it fails.** Its typing half is correct and survives every objection. Its
representative half does not. [CHECKER] The brief claimed that adopting (b2) makes criterion (C) and
the G(P) = G_tie + G_fact result "statements about the same object as criterion (A)/(B)". They are
not. `Theory/09:915` states that "the admissible mean-only family leaves covariance unrestricted",
and `eq:cg-mean-tie-cost` (`:919-926`) takes the infimum over Σ ≻ 0 **free**. (b2)'s single Karcher
Σ_M replaces the block's covariances with one — that is covariance **identification**, whose exact
cost is `Theory/09:966` `eq:cg-epsilon-divergence`, G_ε = G_tie + (r/2)log(1/ε) − r/2 + …, with
`Theory/09:987-988` (`\status{ESTABLISHED}`) concluding "identification is a generative construction,
not a finite recognition restriction". worklog `:890-895` reproduces this to 2.8e-14 and states "The
finite object is the *mean tie with free covariance*, not identification." **So (b2) buys the type
"normalized Gaussian law" by a declaration that costs the variational warrant, and the brief booked
that cost as an unblock.** It was the brief's recommendation reason (2), and it is priced backwards.

Three further costs of (b2) the brief did not list. [CHECKER] (i) The AIRM Karcher mean is nonlinear,
so the Σ sector has no ι_I (`Theory/09:444-460` `eq:cg-partial-properness` is a *linear* full-column
injection) and no exact nested-composition theorem (`Theory/09:468-479`
`prop:cg-nested-sections-compose`) — the multi-level RG has no covariance-sector analogue. (ii)
`Theory/09:1044-1049` (`\status{ESTABLISHED}`: for K ≥ 2, n ≥ 2 no F : GL⁺(K)^n → GL⁺(K) is both
left-equivariant and permutation-symmetric) blocks the *frame* half of the Aff(K)-valued meta
transports that (b2)'s re-typing of O14 requires. (iii) Criterion (B)'s characteristic-class results
at worklog `:941-950` do not merely "lose the eigen-ray": a barycentric representative has no sign
ambiguity, so w₁ and c₁ either vanish or must be redone for a transported nonlinear barycentre, which
needs a root/spanning-tree choice over a region with nontrivial holonomy.

**A retraction (b2) requires, which must be written down.** [CHECKER] worklog `:1440-1442` gives O7's
reason as "Fréchet/Karcher barycentre repairs are unavailable because GL⁺(K) admits no bi-invariant
Riemannian metric", citing Milnor (1976) at `:1297-1298`. That is a non-sequitur for the covariance
sector: AIRM is not a bi-invariant metric on a *group*, it is the GL(K)-invariant metric on the
*symmetric space* SPD(K) = GL(K)/O(K), which exists precisely because the isotropy O(K) is compact,
and its invariance is under congruence, a different action from left translation. Milnor's result and
`Theory/09:1044-1049` remain correct about the **frame** sector. So adopting the AIRM machinery
requires an erratum against worklog `:1440-1442` and a scope narrowing of the Milnor invocation, and
O7 stays live for the frame/transport sector regardless.

**Option (b2-minus) — the missing option.** [CHECKER] Keep the single declared pushforward, let the
transported Gaussian divergence with both moments define the extent, but do **not** aggregate the
covariances: the meta-belief is the tied mean with per-agent covariance retained, i.e. a law on the
block's product space rather than a single K-dimensional Gaussian. Warrant: `Theory/09:915-926`
`eq:cg-mean-tie-cost` (ESTABLISHED, covariance free) and worklog `:961-963`'s criterion-(C) family.
It avoids the divergent identification cost, the Karcher machinery, the nonlinear coarse map that
voids `Theory/09:444-460` and `:468`, and the Aff(K) re-typing. It costs: the meta-fiber is
|I|·K-dimensional, so `Theory/09:390-399`'s f_I is a statement about the tied sector only, and
meta-of-meta needs a declared product-fiber convention. **Every option on the original sheet assumed
the meta-fiber is K-dimensional; none considered the product-fiber object that recognition
restriction actually delivers.**

### D3.5 Recommendation

The checker overturned the brief's recommendation of (b2). What survives, and what this document
recommends, is a **split declaration**:

**Adopt the typing half now.** Declare that inside the belief channel there is one pushforward acting
on (μ, Σ) together, per `Theory/02:89-94` `eq:geo-pushforward-actions` and `:427-441`
`prop:geo-moment-pushforward`; and that the model channel is a separate extent by declaration, per
`Theory/02:87`. This is free — it removes a contradiction rather than adding a commitment — and it
disposes of (a), (c) and (d) on the corpus's own typing. (d) is rejected outright: its model conjunct
is not type-checkable and contradicts `overview.md:47-49`.

**Adopt the edge metric now, in the corrected form.** The transported edge metric of D2 below, with
β retained as a scalar multiplier: W_e^eff = w_e · W_e. [CHECKER] The brief's phrasing — "replacing
the scalar weight by the matrix edge metric" — reads as dropping w_e = (β_ij+β_ji)/2 entirely, which
would make `Theory/09:352-357`'s L independent of the attention rows and destroy the support-boundary
wall at worklog `:1154` (a departing agent would no longer decouple, because W_e ≻ 0 regardless of
β). A positive scalar cannot break congruence covariance, and the measurement confirms it: matrix
metric with β retained, λ₁ 0.328288 → 0.328288, relative 2.54e-15, full generalized spectrum
5.41e-16, against 2.81e-01 for the scalar-weight pencil [COMPUTED].

**Defer the representative half** — Karcher aggregate (b2) versus mean-tie-with-free-covariance
(b2-minus) — until D5 is answered, because (b2)'s operator is built from Σ as well as β, so the
coarse map becomes belief-dependent in a second variable and D5's own dilemma applies verbatim.

This is strictly cheaper than the brief's recommendation and does not pre-commit a second
declaration.

### D3.6 What would overturn it

(i) An amendment to `Theory/02:89-99` replacing the pushforward by a linear action on a mean-vector
fiber — that would make (a) coherent at the price of `overview.md:430`'s invariant content. (ii)
Evidence that on programme configurations d_Σ is a monotone function of d_μ (Spearman ≳ 0.95), in
which case the μ-only extent is a faithful proxy; the two ensembles bracket this at +0.095 to +0.904
and nobody has measured it on real configurations. **This is the single cheapest discriminating
experiment on the whole sheet.** (iii) A record-level observable compatible with B4 whose value
depends on the coherent index set in one channel only. (iv) A declaration that the Σ-channel is the
operative channel, in which case the μ-sector Fisher edge metric must be rederived there.

## D2 — Which symmetric PSD operator, and which pencil metric?

### D2.1 The question

Which symmetric PSD operator on ⊕_i ℝ^K, and which pencil metric, replaces the retracted §3e.2(iii)
operator L^Ω = D ⊗ 1 − W^Ω — specifically (i) is the edge fibre metric the Euclidean I with a scalar
weight w_e, or a transported SPD W_e(c); and (ii) is the pencil metric ⊕Σ_i^{-1}, or the interaction
precision Λ = ⊕Σ_i^{-1} + L^Ω, or none?

### D2.2 What it blocks

Criterion (A) at worklog `:913-935` is stated entirely as the generalized spectrum of the pencil
(L^Ω(c), M(c)) and its Riesz projector, and is flagged there as "[Derived] … and was **not** itself
recomputed; it is the single most load-bearing untested assembly in this section". Everything
downstream reads off it: step 2 (`:1078-1083`), step 3's Riesz projector and covariant Kato formula
(`:1085-1103`), step 4's ∇^M = P∇^ω P and Gauss equation (`:1105-1147`), the wall table
(`:1152-1158`), and disagreements 1–3 (`:977-1029`). O16 (`:1499-1505`) states the consequence:
"Until this or O5 is done, **every result in §3f about the gap, λ₁ and the extent is a compact-G
result**" — which contradicts the declared typing at `overview.md:33`.

### D2.3 What the corpus provides, and what it does not

`Theory/09_coarsegraining.tex:352-358` `eq:cg-connection-laplacian-energy` is
zᵀL_I z = Σ_e (z_i − Θ_e z_j)ᵀ **W_e** (z_i − Θ_e z_j) with **matrix** weights, hypothesis W_e ≻ 0 at
`:346-350` [PROVEN, read verbatim]. `prop:cg-kernel-holonomy` (`:379-425`) consumes only W_e ≻ 0 and
Θ_e ∈ GL(K). `thm:cg-rectangular-endpoint-closure` (`:300-341`) puts this in the degree-zero cellular
sheaf category and says at `:336-338` that it "is gauge covariant and strictly larger than the
fixed-K group-link family". `Theory/08_infogeometry.tex:438-447`
`prop:ig-generalized-spectrum-invariance` proves congruence invariance of the pencil (L, Λ) — its
hypothesis is that **both** members transform by the same congruence; `:484` states the standing
prohibition that a chart-dependent spectral criterion "states nothing about the model".

What the corpus does **not** provide: any pencil (L^Ω, ⊕Σ_i^{-1}); any fibre metric making the
retracted operator self-adjoint; any Π_0^R or λ_+ for a c-varying metric (`:524-526` says "constant
matrices"); any Cheeger inequality for a matrix-weighted form or a general SPD pencil.

**Contradiction.** Worklog R1 at `:856-860` cites `eq:cg-connection-laplacian-energy` but rewrites it
with a **scalar** w_e = ½(β_ij+β_ji), substituting the Euclidean fibre norm for the corpus's SPD W_e
— discarding exactly the degree of freedom that carries GL(K) covariance. The corpus already contains
what O16 asks to be "constructed".

**Shipped code.** `src/multiagent_elbo/realizations/gaussian/interactions.py:172-178` assembles L with
Θ_e = I — no transport at all — and validates matrix PSD edge weights at `:161-167`; `gauge.py:195`
applies `_inverse_congruence` to the assembled operator and `:211,217` pairs it with `precision` = Λ.
So no shipped object is L^Ω, and the worry that the deployed operator is silently asymmetric resolves
negatively: it has no Ω to be asymmetric about.

**A false premise in O1, which must be corrected before the re-run is scheduled.** [CHECKER] O1
(worklog `:1403-1405`) proposes settling the retraction by "computing ‖L−Lᵀ‖/‖L‖ on the committed
seed in `docs/verification/meta_agent_coherence_witness.py`; if nonzero (it will be)…". Executed: it
is **0.0 exactly** at all three call sites (`:154`, `:181`), because those sites pass
β = [1.0]·len(edges), `:175` sets O[(j,i)] = g.T, and `:65` returns 0.5·(L+Lᵀ) regardless. The
committed witness already computes the symmetric energy form and equals `Theory/09`'s w_e I form to
5.00e-16 [COMPUTED]. R1's 0.178–0.830 band came from off-repo lens scratchpads, not from the
committed witness. There is nothing to "re-run"; there is something to **rewrite**.

### D2.4 The measurements

All [COMPUTED], N = 5–6, K = 3, float64, and reproduced independently by the checker where marked.

| Quantity | Euclidean W_e = w_e I | Transported W_{i←j} = (Ω_ij Σ_j Ω_ijᵀ)^{-1} |
| --- | --- | --- |
| Re-assembly vs congruence, ‖L̂ − AᵀLA‖/‖AᵀLA‖ at ‖log g‖_F = 0.798 / 1.595 | 0.372 / 0.819 (checker: 1.82 at 1.39) | 4.79e-16 / 2.87e-16 (checker: 1.79e-14) |
| Generalized-spectrum drift (units of spectral spread) | 0.630 / 2.78 | 9.11e-16 / 1.21e-15 |
| Projector covariance error | 0.189 / 0.416 | 7.32e-15 / 5.67e-15 |
| Kernel–holonomy dim ker = dim Fix(Hol) | holds | holds (8/8 configurations) |

Two further results decide the sub-questions.

**The transported metric is forced, not chosen.** ½zᵀLz reproduces Σ_{i≠j} β_ij KL(q_i ‖ (Ω_ij)_# q_j)
up to a z-independent constant to relative residual 2.69e-16 (checker: 1.08e-15) — the exact
mean-sector quadratic of the coupling contract at `overview.md:47-49`, carrying the **second-slot**
covariance, with **no** shared-covariance hypothesis needed. And the algebra is exact, not merely
numerical: W′_{i←j} = (T_i Ω Σ_j Ωᵀ T_iᵀ)^{-1} = T_i^{-T} W T_i^{-1}, so the edge energy is invariant
by construction, whereas W = wI is not a bilinear-form transformation. `Theory/08:438-447` is a
correct proposition applied to a pair that does not meet its hypothesis.

**The pencil metric is a reading convention, not a discriminating choice.** [CHECKER — this
overturned the brief.] Lx = d·Λx with Λ = A + L is **identical** to Lx = ν·Ax under the monotone map
d = ν/(1+ν): max|d − ν/(1+ν)| = 2.66e-15, and the lowest-3 spectral projectors under the two metrics
agree to 8.55e-15. So Λ buys no separation, no ordering, no eigenvector, no projector, no gauge
property — only a relabelling of the axis into [0,1], which `Theory/08:461`'s own proof shows holds
for **any** A ⪰ 0 including A = I. Worse, the map is nonlinear, so it does **not** preserve the gap
*ratios* criterion (A) is built from: on one and the same operator, λ₄/λ₃ = 4.5543 under ⊕Σ^{-1} and
1.4817 under Λ. The brief called this sub-choice "free" and it moves the headline number by 3×.

**And Λ carries an unpriced conflation.** [CHECKER] The diagonal blocks of Λ^{-1} differ from Σ_i by
92%/93%/97% relative. Under Λ = ⊕Σ_i^{-1} + L^Ω, Σ_i is simultaneously agent i's belief covariance
(transported inside W_{i←j} and inside `overview.md:49`'s contract) and the self-term of a joint
precision whose marginals are nothing like Σ_i. `Theory/08:236` is the standing prohibition on
exactly this move: "The equality is of components in matched charts, not of objects … cannot be used
as evidence that a construction defined on one space transfers to the other."

### D2.5 Options and recommendation

The brief offered four options and recommended (c) — transported edge metric paired against Λ. The
checker upheld the operator half and rejected the metric half. What this document recommends is the
**split**:

**(i) Declare the fibre metric now, transported, with β retained.**
W_e^eff(c) = w_e(c) · (Ω_ij(c) Σ_j(c) Ω_ij(c)ᵀ)^{-1}, summed over both orientations, inside
`Theory/09` `eq:cg-connection-laplacian-energy`. This is forced by three independent arguments: it is
the exact mean-sector quadratic of the programme's own coupling contract (2.69e-16 / 1.08e-15); it is
exactly congruence-covariant by algebra, so `Theory/08:438-447` applies rather than being cited
inapplicably; and `Theory/09:346-350` already requires only W_e ≻ 0, with `prop:cg-kernel-holonomy`'s
proof at `:401-425` consuming nothing more. It closes O16 and lifts the compact-G fence at worklog
`:1504-1505`. **The directed second-slot form is the one with the KL warrant**; the first-slot form
Σ_i^{-1} used in the D4 brief moves the operator by 1.05e-1 and λ₁ by −8.7% and requires the
shared-covariance hypothesis that worklog `:1190-1192` records as **not granted**.

**(ii) Do not declare the pencil metric now.** It is provably a monotone reading convention on a
fixed set of projectors; it interacts with the threshold that worklog `:953-954` says is "not settled
by anything in this panel" and that O12 (`:1465-1471`) owns; and choosing Λ silently commits to the
Σ_i double-role that `Theory/08:236` forbids. Declare it **with** the threshold, not ahead of it. If
a metric must be named for interim work, name ⊕Σ_i^{-1} — it is O5's literal proposal, it delivers
identical eigenvectors and projectors, and it avoids the conflation.

**(iii) Two unlisted edits that either choice requires.** [CHECKER] `Theory/09:346-348` declares "For
each undirected internal edge, choose **one** orientation"; a two-orientation directed sum with
distinct W and distinct β requires replacing that convention with a multigraph or directed-sum
clause. And on the code side, `interactions.py:154-157` canonicalizes every edge to
`(min, max)` and raises `"duplicate reversed edge is not allowed"`, `:165` symmetrizes each edge
block, `:188` stores under the canonical key — so the change is to the edge keying, the duplicate
check, the per-edge symmetrization and the `from_self_and_edges` signature, not the "transport
argument" the brief priced.

Two costs that survive under any choice: **the Cheeger route is forfeit** — no matrix-edge-metric
version of the Bandeira–Singer–Spielman two-sided bound exists, so the quantitative half of the
coherence criterion at worklog `:1030-1032` is lost, not merely unverified; and **the float64
well-posedness cap** is cond(M) ≲ 1e9 (lowest generalized eigenvalue −3.75e-6 at 1.2e11, −0.186 at
1.2e15) [COMPUTED].

**One mis-citation to fix while editing.** [CHECKER] `overview.md:546-551` is open decision 2
(Physicalization rule) and decision 3 (Units and constants). Open decision 7, "Compact G vs full
GL(K)", is at `overview.md:558-560`. And `overview.md:51-53` — "Start with compact G; full GL(K) is a
later extension" — is the standing convention that most directly prices this decision and it went
uncited throughout.

### D2.6 What would overturn it

(i) D1 resolved as the coboundary reading: then the transports carry no content beyond frame change,
all gauge-covariance questions are vacuous, and the Euclidean form is correct by default. (ii) A
Cheeger-type two-sided bound shown to require scalar weights and compact G with no matrix-edge-metric
generalization, **together with** a decision that the quantitative criterion matters more than
frame-independence. (iii) A demonstration that the block-edge gap collapse under precision disparity
(182 → 9.7 → 1.18 as Σ₀ → εI, versus Euclidean holding 135 → 137) is a defect rather than correct
KL-unit behaviour. (iv) A configuration where the operator choice changes the *identity* of the block
rather than only its *extent* — none was found at strong separation, and the comparison is vacuous at
weak separation, so this is [COMPUTED on two instances] and could fail at larger K.

## D5 — Are β and γ generative-side or recognition-side?

### D5.1 The question

Are the attention rows β and γ generative-side declared structure or recognition-side optimised
variables — and which of the three distinct rows the corpus already carries is "attention", and which
one may a coarse map C_h be built from?

### D5.2 What it blocks

`overview.md:340`'s exact-contraction arrow requires "a recognition-independent measurable C_h"; the
literal hypothesis is `Theory/06_general_coarsegraining.tex:262-264`. Worklog `:883-889` (R4) reports
that a β-built coarse map violates it, so every meta-agent extent defined through L^Ω is currently
unwarranted. Worklog `:1450-1455` (O9) is an either/or whose branches lead to opposite architectures.
`overview.md:556-557` (open decision 6) is stated and unanswered and gates whether profiling the base
cometric is an ELBO operation or empirical Bayes — the ledger claim `coefficient-model-choice`.

### D5.3 The corpus carries three rows, and the question has been posed as two-way because the middle one is unnamed

1. **π** — the fixed label prior, declared generative data inside P at `typed-construction.md:56-59`,
   appearing in the generative joint at `:73-77`, independently at `Theory/05b:494-498`, and named
   "the fixed recognition-independent label baseline" at `Theory/07b:1779-1786`. Constant,
   recognition-independent, latent-independent. [PROVEN.]
2. **β^P(y)** — the generative posterior row, `Theory/05b:551-557`,
   β^P_ij(y) = π_ij e^{−D_ij(y)/τ_i} / Σ_k π_ik e^{−D_ik(y)/τ_i}. Recognition-independent but indexed
   by the latent state. [PROVEN.]
3. **β^{Q*}** — the recognition optimum, `Theory/05b:575-579`, with E_{Q_Y}D in the exponent.
   `Theory/05b:602-608` states in terms that these are different objects.

### D5.4 The forced half

`typed-construction.md:100-105` declares β_a and γ_a as recognition rows inside Q_a; π^q, π^s sit in
P. `exact-elbo-proof.md:64-73` gives F_a^q = D_KL(β_a ‖ π_a^q) + Σ_b β_ab D_KL(q_a ‖ u_ab), assembled
at `:110-115`. The row-entropy term is therefore not a penalty but the **exact label-block KL between
them**, and D_KL(β‖π) is well-formed only if β is recognition-side and π is its generative
counterpart. [PROVEN, read at source by two readers.]

**This settles half the question and nothing more.** β and γ are recognition rows. Declaring them
generative pins them and pays a measured price: F(b) − F(β*) = KL(b ‖ β*) exactly (residual max
1.93e-12 over 20,000 rows), which at b = π is median 1.8618 nats, p95 4.7513, max 11.8737 per row per
channel per agent [COMPUTED]. It also empties both row-entropy terms and both softmax-optimum results
and removes two of eight terms from the closed theorem's boxed identity. The asymmetric variant (β
recognition, γ generative) has no derivational warrant anywhere — `Theory/05b:488-600` derives both
rows by one identical calculation — and worklog `:1510-1512` records the fast/slow separation
unproven with the circularity attack SUSTAINED.

Two contradictions must be resolved either way. `overview.md:484-486` calls β "the declared source
row" — a generative reading — while worklog `:885-888` declares both recognition rows. And the
shipped code takes a third position: `src/multiagent_elbo/finite/attention.py:52,111,124` types the
row as `beta_given_state` with shape (state_count, receivers, sources), which is the β^P(y) typing,
while `src/multiagent_elbo/geometry/attention_gauge.py:110-111` computes a softmax from a bilinear
form with no π term and no temperature — an implicit uniform prior with an inverted sign convention.
Neither module constructs β^{Q*}.

[CHECKER] The `overview.md:485` edit is not a rename under any option. The line reads "η_q is **fixed
by the declared source row β and the declared m_h** — a declared coefficient, not a measure of
dependence". But the boxed exact identity at `exact-elbo-proof.md:102-117` carries the transported-KL
coefficient as β_ab, the recognition row; the π substitution is right only at leading order in h
(β* = π + O(h²), `panelB-V-TYPE-derivation.md:131-137`). Under the recognition-side declaration β is
an optimised variable, so the punchline "a declared coefficient" fails at finite h regardless of which
symbol is written. The required edit is a **status change**, not a rename.

### D5.5 The unforced half: which row may weight a coarse map

The brief recommended π and justified it by disqualifying β^P(y) on `Theory/06:56-58`. [CHECKER] That
is a source misuse. `Theory/06:56-58` reads "Parameter independence is load bearing: a family K_θ is
a parameter-dependent model transformation, not one channel between experiments" — θ indexes the
experiment family {P_θ}, not the kernel's own argument. The actual hypothesis of
`thm:cg-evidence-preserving-channel` is `Theory/06:262-264`: a Markov channel K : X ⇝ Y with
K(x, Y) = 1 for every x, which does not read the arbitrary recognition law Q_o. **A kernel that varies
with its source point is the definition of a kernel.** Since `Theory/05b:511-512` puts no live
recognition distribution in D_ij ("The energy D_ij is a fixed gauge-invariant function of latent
sample-level states and declared transports"), β^P(y) is recognition-independent and H2-compliant.
O9's original wording at worklog `:1449-1455` is defensible.

Two further findings dismantle the brief's case for π. [CHECKER]

- **π does not make the extent deterministic, because no numerical π exists.**
  `typed-construction.md:56-59` requires only that π^q be "normalized positive source rows"; no
  numerical π is declared anywhere on the agent graph, and a grep over `src/` for
  `label_prior|source_prior|prior_row|pi_q` returns nothing. Measured on a fixed graph varying only
  the row: uniform-π λ₁ = 0.358959; β^{Q*} = 0.050634; β^P(y) over 400 latent draws, min–max spread
  **322%** of the mean; **admissible declared π ~ Dirichlet(1) over 400 draws, min–max spread 162% of
  the mean** [COMPUTED]. The π-built extent is a functional of a number nobody has declared, with
  spread of the same order as the randomness used to disqualify β^P(y). π requires a construction.
- **π-only would empty an ESTABLISHED result.** `Theory/07b:1744-1830` (`sec:rg-meta-attention`) is
  an existing coarse-graining of the attention block built from a **latent-indexed** row:
  `07b:1748-1755` writes η_ij(y) = α_i(y) β_ij(y), and `:1766-1770` coarse-grains
  η^c_IJ(z), α^c_I(z), β^c_IJ(z). A prohibition on latent-indexed rows puts that out of scope.

**And a hard constraint no row-only option satisfies.** [CHECKER] `Theory/07b:1747-1748`
(`\status{ESTABLISHED}`): "A row-stochastic matrix β_ij is a conditional law of a source given a
receiver. It cannot be coarse-grained without the receiver law", with `:1775`: "The next scale must
push the joint law η^c, not β^c alone." Every option on the original sheet builds a coarse map from
a **row**. The corpus says that is insufficient.

The one point in π's favour that survives: `Theory/07b:1816-1826` `eq:rg-attention-log-sum-exp`
already gives π^c_J = Σ_{j∈J} π_j with a matching log-sum-exp coarse energy,
`\status{ESTABLISHED}`, associating for nested partitions — so the "exhibit a π-built channel"
obligation is **partly discharged**, contrary to the brief.

### D5.6 Recommendation

**Split the decision, and ratify only the forced half in this sitting.**

Declare: β and γ are recognition rows; π^q and π^s are their generative counterparts; D_KL(β‖π) at
τ = 1 is the exact label-block KL. This is forced by `exact-elbo-proof.md:64-73` and is uncontested
by any checker. It answers `overview.md:556-557` (open decision 6) for the variational row.

**Do not declare the coarse-graining row in this sitting.** Present it as a separate sub-decision with
four priced candidates and no default:

| Candidate | H2 status | Cost |
| --- | --- | --- |
| π | Compliant | Requires a numerical π nobody has declared; 162% spread over admissible π [COMPUTED]; empties `Theory/07b:1744-1815`. |
| β^P(y) | Compliant (`Theory/05b:511-512`) | Extent becomes a fine-sample random variable, 322% spread [COMPUTED]. Already what `07b:1748-1770` and `attention.py:124` use. |
| η = α·β (joint marked-event law) | Compliant | The only candidate consistent with `07b:1747-1748` and `:1775`. Already computed at `attention_gauge.py:113`. Not otherwise priced. |
| Row-free, W_e = I on declared design edges | Vacuously compliant | Licensed by `Theory/09:402` (the kernel-holonomy proof consumes only W_e ≻ 0, never the weight values) and by the measurement that dim ker L^Ω is row-invariant. Declares no numbers. Loses the divergence warrant of D2's transported metric. |

Note the tension with D2: D2's recommended fibre metric carries β as a scalar multiplier, so the
row-free candidate and D2's transported metric are not jointly available. If the row-free candidate is
attractive, D2's β-retention argument (the support-boundary wall at worklog `:1154`) must be
re-examined.

**What D5 does not decide.** Not one option changes whether the meta-agent is an ELBO object. The only
route in the corpus that delivers a meta-agent with a variational warrant is criterion (C) at worklog
`:956-973`, coarse-graining by recognition-family restriction, whose exact excess negative ELBO is
G(P) = G_tie(P) + G_fact(P) with unit coefficients (`Theory/09:917-928` plus `:1001-1009`), verified
here to 1.78e-15 across all 203 partitions of six agents with an interior argmin [COMPUTED]. G(P) is a
functional of (Λ, μ, P) alone: no β, no γ, no π. And `Theory/06:329-331` states that restricting a
recognition family is neither a Markov pushforward nor an energy precomposition, so
`thm:cg-evidence-preserving-channel` and its H2 never enter that route at all. **D5 is orthogonal to
the meta-agent's ELBO status.** What it decides is whether the spectral/L^Ω route can ever be a coarse
channel, and whether the continuum base cometric is declared or profiled.

### D5.7 What would overturn it

(i) A demonstration that "meta-agent extent" is meant as a fact about **inferred** beliefs rather than
declared design — then a π-built extent measures the wrong thing (the two differ by 53.9%–85.9% in λ₁
across the two instances measured [COMPUTED]) and the honest answer is that L^Ω drops out of
coarse-graining exactly as worklog `:1454-1455` says. (ii) An explicit Markov channel K : X ⇝ Y
satisfying `Theory/06:258` built from π or from η. (iii) A derivation of the fast/slow separation
(CE-3) that survives the SUSTAINED circularity attack, exhibiting the separating small parameter
worklog `:1514-1516` says does not exist — that would supply the missing warrant for the asymmetric
option.

## D4 — By what rule does the meta-agent become a normalized law?

### D4.1 The question

By what declared rule does the meta-agent of a coherent block become a normalized law — a point of the
belief fiber ℬ_b ⊆ 𝒫(𝖪) (`Theory/02:70-73`, `overview.md:34`) — and what residual gauge group does
that rule leave? Equivalently: is the meta-agent defined **spectrally** (a low eigen-ray of the pencil,
which then needs a lift) or **variationally** (the KL-minimizer over the tie family, which needs no
lift)?

### D4.2 What it blocks

Until this is declared the spectral meta-agent is not a section of a bundle of normalized laws, so it
is not an agent (worklog `:1443`). Four things stop: the (B)-tier "belief representative" criterion of
worklog `:937-954` and its w₁/c₁ obstruction theory; O14 (`:1482-1485`), so the RG tower has one level
only; the `Theory/07b` tree-dependence repair at worklog `:1362-1370`, which must replace C_x by
either ι_I or a spectral low-block frame and cannot be written without D4; and any meta-level free
energy, so tier (C) of worklog `:910-911` is empty.

### D4.3 The stated no-go is a category error

worklog `:1440` justifies "no GL(K)-invariant lift exists" by the coercivity lemma at
`rm-02-existence-analysis.md:282-290`, which reads: "If some orbit ρ(G)·m is noncompact, then no
ρ(G)-invariant V has compact sublevel sets." That quantifies over invariant **functions** V with
compact sublevel sets. A lift is an equivariant section-selection λ with λ(g·x) = g·λ(x); it has a
different quantifier structure and no sublevel sets. **The lemma does not apply.** [PROVEN — the
checker verified this independently and it survives.]

The correct no-go is one line: the center ℝ*·I ⊂ GL(K) acts trivially on P(V) but by scaling on V, so
any equivariant λ : P(V) → V\{0} satisfies λ([z]) = cλ([z]) for all c > 0, forcing λ ≡ 0. No lift
depending on the **ray alone** exists. That no-go is defeated by any auxiliary datum that transforms —
and one exists: with a congruence-covariant edge metric, the M-normalized eigenvector is equivariant
to 3.8e-14 [COMPUTED].

### D4.4 But no lift can make the spectral object a belief mean

Take g = −I globally: Ω ↦ (−I)Ω(−I)^{-1} = Ω and Σ ↦ Σ, so the data are exactly invariant
(‖L′−L‖ = 0.0, ‖M′−M‖ = 0.0) while every member's mean flips sign. With β from a softmax of the
transported KL, the energies are quadratic in μ, so z(−μ) − z(μ) = 0.0 exactly. **The spectral object
is even in the member means; a belief mean is odd.** [COMPUTED, and [PROVEN] as algebra — the energies
are quadratic, hence β and hence L are even.] Strict equivariance therefore forces the meta-mean to
vanish, and what survives is the ℤ/2 the panel already measured as w₁ (⟨v(2π), v(0)⟩ = −1.000000000000
at worklog `:944-947`).

Two consequences. The Fisher normalization sets Σ_i r_i² = 1 exactly, pinning the single gauge
invariant that `overview.md:430` (Cor A3.5) says **is** the mean-sector content — so the lifted object
is informationally the projective object plus a chart. And at exact coherence the ambiguity is not a
ray at all: dim ker = K, so "the low eigenvector" is an arbitrary element of a K-dimensional kernel.

### D4.5 The variational object, and where the brief overreached

The variational route defines the meta-agent as the KL-minimizer over the tie family. Measured: G_tie
against `Theory/09:918-927` `eq:cg-mean-tie-cost` to 1.6e-16; `eq:cg-epsilon-divergence` at `:956-967`
to 4.0e-12 at ε = 1e-6, confirming that identification diverges and the **mean tie with free
covariance** is the finite object, which `Theory/09:987-989` states in terms; gauge equivariance of the
law to 1.2e-15 and 3.3e-16; the meta-invariant r_M gauge-invariant to 6.2e-15 and **not pinned to 1**;
and the mean **odd and degree-1 homogeneous** in the member means (a(−μ) + a(μ) = 0.0;
‖a(5μ) − a(μ)‖/‖a‖ = 4.000000000000) [COMPUTED].

That is the object the lift was invented to produce, and it produces it without a declaration. But the
brief's recommendation was overturned on four counts, each with a measured consequence.

1. **It is priced as the variational route and delivered as variational-plus-spectral.** The
   recommendation's clause "range ι_I = ker L_I, **or** the pencil low block" is not a garnish: with
   generic transports dim ker L_I = 0 (λ_min = 0.09587) [COMPUTED], so on any frustrated block the
   pure variational definition types **nothing**, and the pencil low block is all that is left. That
   silently imports the entire spectral option — the `Theory/09:357` edge-metric edit, D2's
   obligations, the ungranted shared-covariance hypothesis of `Theory/08:239-245`, and O12
   (`:1465-1471`) — none of which appears in its downstream list.
2. **"The law is already written down at `Theory/09:452-458`" is false.** `Theory/09:451-459` contains
   only L_I ι_I = 0, Λ_c = ι_Pᵀ Λ ι_P ⪰ 0, and the properness iff. There is no mean, and Λ_c^{-1} is
   never called a covariance. `Theory/09:931-932` gives the tie optimizer's covariance as **Λ^{-1}**,
   the full NK × NK inverse. Λ_c^{-1} appears only as the pushforward of Λ^{-1} under one specific
   readout A = Λ_c^{-1} ιᵀ Λ (exact to 6.3e-17), while the Moore–Penrose readout gives a different
   coarse covariance (2.44% relative). **A declared readout map is required, and the `Theory/09` edit
   is a new proposition plus proof, not a paragraph.**
3. **It quietly fixes a parent law.** "Under the closed theorem's product recognition family Λ = M"
   contradicts `Theory/09:30-36`, where Λ is the coupled interaction precision with off-diagonal
   blocks −W_ij, and `Theory/09:912` makes p = N(μ, Λ^{-1}) the target. The substitution changes the
   answer by tens of percent: a* by 38.8%, r_M by 98% (1.0495 vs 2.0784) on one instance. It also
   costs the variational warrant that is the route's whole justification: with Λ = M the Pythagorean
   step fails, F(r) − F(q*) = 22.7011 against KL(r‖q*) = 21.7080 [COMPUTED], so G_tie is a consensus
   divergence, not the excess VFE that worklog `:1316-1320` claims.
4. **The ground for rejecting the spectral lift is applied asymmetrically.** ι_I is defined only
   "after choosing bases" (`Theory/09:444-447`); re-choosing by h ∈ GL(f_I) sends a ↦ h^{-1}a, exact
   to 2.4e-16, a 45.5% change in the coordinate. The brief reports this as a virtue ("re-rooting to
   4.2e-16") while condemning the spectral lift for "a full GL(K)-worth". The variational route does
   win the comparison — its invariants ι a and r_M are canonical under re-basing — but that argument
   must be made, not obtained by presenting one measurement twice with opposite signs.

One cost the brief inflated. [CHECKER] The topological witnesses at worklog `:944-947` (w₁ via
⟨v(2π), v(0)⟩ = −1.000000000000, c₁ = +1) **cannot** change under a change of positive-definite fibre
metric: the set of such metrics is convex, so the low-block projector bundle deforms by homotopy
wherever the gap stays open. Measured at −1.000000000000 for Euclidean, constant SPD, and c-dependent
SPD, at min gaps 1.500000 / 0.288420 / 0.047619 [COMPUTED]. Only the metric-dependent quantities — the
Kato ratio and accumulated rotation Θ at `:950-954`, and the gap/λ₁ numbers — need recomputation.

### D4.6 Recommendation

**The variational definition, scoped to the stratum where it exists, with the parent law and the
readout declared.** Concretely, four clauses:

1. **Type.** The meta-agent is a normalized law on the abstract fixed fiber
   F_I = ⊕_α Fix(Hol_{r_α}) of `Theory/09:438-442`, over a **stratified** base. `Theory/09:463-465`
   already states that "rank jumps produce strata rather than a smooth bundle", and f_I ranges over
   {0,…,K} with the configuration. It is a section of a ℬ_b-bundle only on the stratum f_I = K, i.e.
   exactly when every represented holonomy element is the identity (`Theory/09:427-428`).
2. **Domain.** Declare the object on the f_I > 0 stratum. Declare f_I = 0 **OPEN pending O12**
   (`:1465-1471`) rather than covering it with "or the pencil low block". This also makes the
   declaration independent of D2's edge metric: ker L_I is metric-independent, because
   `Theory/09:414-415`'s proof uses only W_e ≻ 0, so the kernel is {z : z_i = Θ_e z_j} whatever W_e is
   (‖L ι‖ = 1.2e-15 with W_e = I) [COMPUTED]. **No `Theory/09:357` edit is needed for D4.**
3. **Parent and readout.** Declare which Λ the meta-agent is the projection of — the coupled
   interaction precision of `Theory/09:30-36` carries the variational warrant; the product-family M
   does not — and declare the readout map, since Λ_c^{-1} and the Moore–Penrose coarse covariance
   differ by 2.44%.
4. **Residual gauge.** GL(F_I) acting on the coordinate, with ι a and r_M as the canonical
   invariants. Not ℤ/2, and not O(K).

**Keep the Fisher-pencil lift as a separately priced frame declaration, not as a fallback clause.** If
a frame for the tie subspace is ever wanted, it is available; it carries its own `Theory/08:239-245`
shared-covariance hypothesis, which worklog `:1190-1192` records as not granted, and it must be priced
as its own decision.

**One further caution.** O7 (worklog `:1438-1443`) is only partly answered by this. Per D3's checker,
the Milnor/`Theory/09:1044-1049` no-go remains correct about the **frame** sector: no
left-equivariant permutation-symmetric F : GL⁺(K)^n → GL⁺(K) exists, so the frame half of any
Aff(K)-valued meta transport (O14) is blocked whatever D4 decides.

### D4.7 What would overturn it

(i) A demonstration that the spectral low block is the second-order expansion of a constrained
forward-KL score at λ₁ > 0 (O12) **with the member means entering the expansion** — the evenness
result says they cannot enter through L^Ω or M, so such a derivation would have to introduce a
linear-in-μ term. (ii) A declared use for the meta-agent that needs only a direction and never an
expectation, in which case the projective object is correct and cheaper. (iii) A proof that ker L_I is
generically nontrivial in the deployed regime — the measurement says dim ker = 0 for generic GL(3)
holonomy, so the variational tie exists only on the flat/partially-fixed stratum. (iv) D1 resolved as
the coboundary reading, under which dim ker = K everywhere and D4 is moot rather than answered.

## D6 — Under which expectation is the observation term typed?

### D6.1 The question

Under which expectation is the PIFB2 observation term to be typed — the joint private law
ζ_i = q_i ⊗ s_i over (k_i, m_i), the predictive marginal −E_{q_i} log ∫L(o|k_i,m)s_i(dm), or a
state-only kernel with no model argument — given that `Theory/PIFB2.tex:689` and `:750` write
E_{q_i(c)}[log p(o(c)|k_i, m_i)] with m_i free and absent from the functional's declared argument list
at `:684`, so the displayed functional is not a well-defined functional of its own arguments?

### D6.2 What it blocks

`pifb2-crosswalk.md:17` records the observation row as "Typing mismatch; not matched by this theorem"
— the only non-exact row in a table whose other entries at `:14-22` all read "Exact". The theorem
document has already retreated from the PIFB2 name because of it: the `d892374..HEAD` diff of
`construction-or-strongest-theorem.md` renames `F_PIFB2` to `F_JT` and adds "It does not identify its
joint-private observation term with the literal PIFB2 observation display". `overview.md:378-395`
carries the standing public statement "Equality to the literal PIFB2 observation term is not proved
and is not currently well-posed", and the ledger claim `literal-observation-crosswalk` sits at HIGH /
INCONCLUSIVE. Downstream, `panelA-T-SIMUL-derivation.md` obstruction #8 records that its §5 bound
"inherits whichever convention is declared".

### D6.3 The census, corrected

Across the **multi-agent** observation operator in `Theory/PIFB2.tex`, exactly **two** displays carry
m_i (`:689`, `:750`) plus one prose citation (`:918`). **Sixteen** are state-only: `:669`, `:841`
(boxed), `:855`, `:907`, `:911`, `:941`, `:1350`, `:1361`, `:1389`, `:1390`, `:1417`, `:2679`,
`:2715`, `:2822`, `:3211`, `:3221`. [PROVEN by direct read; all nine spot-checked lines verified
verbatim by the checker.]

[CHECKER] Three corrections to the brief's framing of the census. First, `grep -c "log p(o"` returns
**24**, not 19; the five extra lines (`:518`, `:2125`, `:2600`, `:2602`, `:2604`) are single-agent
preliminaries and are legitimately out of scope, but the claim as stated does not reproduce — scope it
as "the multi-agent observation operator". Second, the E2 prescription at
`docs/reviews/2026-08-13-response-to-interim-theory-review.md:49-52` does **not** miss `:689` — that
is its own header target — so it under-scopes by **eleven** loci (`:841`, `:855`, `:907`, `:911`,
`:1350`, `:1361`, `:1389`, `:1390`, `:1417`, `:2715`, `:3221`) and by **one** boxed equation
(`:841`), not ten and two. Third, and orthogonally to the m_i question: `:841` (boxed
`eq:free_energy_reduced`) writes −E_q[log p(o|{k_i})], a **population** expectation of a **joint**
likelihood over the whole state tuple with a single observation symbol, while its own envelope
gradient at `:855` writes −χ_i ∇ E_{q_i}[log p(o_i|k_i)], per-agent expectation, per-agent
observation, per-agent likelihood. Those are not the same functional unless the likelihood factorizes
as ∏_i p(o|k_i), declared nowhere in 3956 lines. **This is a second, independent typing inconsistency
that survives every option and that E2 also misses.**

Two loci acquire a term under joint or predictive typing and stand under state-only:
`Theory/PIFB2.tex:951` F_slow (no observation term) and `:862-865` `eq:envelope_gradient_model` (no
observation term). One paragraph breaks under joint typing: `:903` states that env agents have no
model or hyper-prior sections, so `:918`'s claim that "every term in the free energy is written as an
agent-to-agent or agent-to-environmental-agent coupling" does not survive an s-expectation.

**Runtime.** `src/multiagent_elbo/` has zero occurrences of `gamma` — the model channel is
unimplemented. The only executable observation channel is `observation_record_kernel` in
`tests/fixtures/two_scale_application_v1.json:134`, consumed at
`src/multiagent_elbo/finite/agent_network.py:148-150`: 16 rows indexed by the 16 joint fine states,
two record labels. **The deployed kernel is state-only.** No shipped number changes under any option
today, which makes this the cheapest moment to decide — before `finite-environment-runtime-gap` is
discharged with an implementation that hard-codes one reading.

### D6.4 Options

| Option | Statement | Exactness |
| --- | --- | --- |
| (a) joint | Bind m_i under the declared product law ζ_i = q_i ⊗ s_i. | Exact negative ELBO of p(dk)r(dm)L(o\|k,m), verified to 1.776e-15 [COMPUTED]. |
| (b) predictive, live s | −E_q log ∫L(o\|k,m)s(dm) with s the live recognition marginal. | **No exact realization.** Eliminated. |
| (c) state-only | Delete m_i; declare the observation channel state-only. | Joint and predictive coincide identically (3.331e-16); matches sixteen loci and the runtime. |
| **(d) plug-in** | −E_{q_i}[log p(o\|k_i, m̂_i(c))] with m̂_i := E_{s_i}[M] a deterministic functional of s_i. | [CHECKER — missing] Not an exact ELBO, but well-defined in the existing argument list. |
| **(e) scope now, declare later** | Adopt (c)'s three-locus edit as the manuscript's typing **and** name the joint form as the declared enlargement under which the crosswalk row closes exactly. | [CHECKER — missing] |

**(b) is eliminated on the evidence.** With the live recognition marginal as the mixing law the
generative kernel depends on the recognition object, so {P_s} is a Q-indexed family, and the one
rescue in the corpus — evidence invariance along the tie — is unavailable because the tied object sits
inside the likelihood. Measured: p_s(o) spreads by 0.1656 across eight recognition marginals, so the
evidence moves and there is no fixed number for the scalar to bound [COMPUTED]. The frozen-ν variant
**is** exact (4.441e-16) but is option (c) under a renamed kernel. [CHECKER] The brief attached
`thm:state_level_elbo_nogo` (`PIFB2.tex:3281`) as authority for this; that theorem is about the
alignment sector (its hypotheses quantify over nonself β_ij > 0 and third derivatives of F_rest), and
a one-body predictive term sits inside F_rest and satisfies them. **Strike the citation; the
elimination stands on the evidence spread alone.**

**(a) versus (c) is a modelling commitment, not a typo fix.** Under (c) the generative-model sector
never learns from observations — which is exactly what `:951` F_slow and `:862-865` already print — and
is driven only by KL(s_i‖r_i) and the γ-alignment. Under (a) it does. That is the whole question.

**Three corrections to the brief's case for (a).** [CHECKER, and the checker returned this brief.]

1. **"Nothing is emptied" is contradicted by the brief's own structural-break paragraph.**
   `PIFB2.tex:918`'s claim is *emptied* under joint typing, not merely edited, because `:915`'s
   replacement −E_{q_i}[log q_{e_k}] is a q_i-only expectation and `:903` gives env agents no model
   section. That belongs in the empties column where the PI will see it.
2. **`overview.md:387-394` must be retained, not withdrawn.** It records a measured gap
   E_q[KL(s‖s^{(o,k)})] ⪰ 0, unbounded in model uncertainty — reproduced here in closed form as
   d²v/(2(v+1)) + (v − log(1+v))/2, giving 0.15342640972 / 47.69243974 / 4995.39478 / 499993.09224 at
   v = 1 / 100 / 1e4 / 1e6 [COMPUTED, two independent readers]. Under (a) that is not a counterfactual
   about a rejected convention; it is the standing statement of how far the adopted scalar sits above
   the predictive model's evidence. **It is the price of (a).**
3. **(a) re-types m, and that cost is unpriced.** Exactness under ζ = q ⊗ s is against the generative
   law p(dk)r(dm)L(o|k,m) — m drawn from the hyper-prior per inference episode. But `PIFB2.tex:167`
   defines m as "the generative-model parameters", `:1351` puts the world model in the slow pair
   (s_i, r_i), and `:944-954` gives η_s ≪ η_q. Adopting (a) converts m from a slow learned parameter
   into a per-observation resampled latent, against the timescale hierarchy at `:929-954`.

**The corroboration the brief offered for (a) is not independent.** [CHECKER]
`panelA-T-RESID-derivation.md:129` ("the contraction produces the joint-expectation form") takes as
its target "the tied-replica law of the exact two-channel run", defines the private object as the pair
(k_a, m_a), sets R^(1)_h = ⊗_a ζ_a **by choice**, and then invokes the chain rule from
`exact-elbo-proof.md`, in the same evidence package as the crosswalk. The contraction retains ζ_a
because the coarse map was defined to retain it. It is the same declaration in a different coordinate.
With that leg withdrawn, the brief's own crux stands undefended: **joint typing cannot be derived; it
must be declared.**

**And (a) loads a second ledger claim.** [CHECKER] The brief disclosed that (a) adds an obligation to
`environmental-interaction-ontology` (`.verification/ledger.json:7`, obligations `:23-26`). It did not
disclose that (a) also makes the deployed state-only kernel a strict non-instance of the manuscript
functional, so discharging `finite-environment-runtime-gap` (`:88`) afterwards requires implementing a
model-argument likelihood in a `src/` tree where the model channel does not exist. Under (c), (d) or
(e) that implementation cost is zero or unchanged.

**Option (d), the plug-in typing.** [CHECKER — missing option, and it may dominate.] Write the term as
−Σ_i ∫χ_i E_{q_i(c)}[log p(o(c)|k_i, m̂_i(c))] with m̂_i := E_{s_i}[M] a deterministic functional of
s_i. This is well-defined in the argument list at `:684` **as it stands**, because s_i is already
declared there — the well-posedness defect is repaired with no enlargement of the recognition law, no
I_ζ term, and no change to the generative class. It gives the model channel an observation coupling,
so `:951` and `:862-865` both gain a term, which was the brief's stated reason for preferring (a) over
(c). It preserves m as a slow learned parameter, so it does not incur (a)'s cost against `:167`,
`:944-954` and `:1351`. And it is the typing the manuscript already uses elsewhere: `:1350` writes
−Σ_i E_{q_i}[log p(o_i|θ)] with θ a conditioning parameter outside the expectation, expanded at
`:1364` as N(o_i; θ, Σ_{o_i}). Its honest cost: it is not an exact negative ELBO, so
`pifb2-crosswalk.md:17` stays inexact — the same cost as (c), bought with the model coupling (c)
forgoes.

**Option (e), scope now and declare later.** [CHECKER — missing option.] Adopt (c)'s three-locus edit
as the manuscript's typing (matching sixteen loci and the shipped runtime) **and** add one declared
remark naming −E_{q_i ⊗ s_i}[log p(o|k_i, m_i)] as the model-coupled enlargement under which the
crosswalk row closes exactly. This removes the ill-posedness today at (c)'s price and strictly
dominates (c) on (c)'s only stated loss: `panelA-T-RESID-derivation.md:129` is retained as a true
statement about the enlargement instead of being emptied. It hands
`environmental-interaction-ontology` no new obligation and does not commit
`finite-environment-runtime-gap` to a model-argument likelihood.

### D6.5 Recommendation

**No recommendation between (a) and (c)/(d)/(e) is offered here, because the brief's case for (a) did
not survive checking and the question reduces to one the PI must answer directly:**

> Does the generative-model channel learn from observations, yes or no?

- **No** → (c), or better (e), which is (c) plus a scoping remark and costs one extra paragraph.
- **Yes, and exactness of the crosswalk row matters more than the timescale hierarchy** → (a), with
  `overview.md:387-394` retained as its price and the m re-typing recorded.
- **Yes, and the timescale hierarchy matters more than exactness** → (d), which is the cheapest way to
  give the model channel a data coupling and which nobody has priced against (a) yet.

If pressed for a default: **(e)**. It removes the ill-posedness at two hours of manuscript work, keeps
every downstream document true, hands no new obligation to two HIGH ledger claims, and leaves both (a)
and (d) reachable. But this is a scoping default, not a resolution.

### D6.6 What would overturn it

(i) A declared intent that the model channel is observation-blind — this is the single most likely
thing to settle it, and it is a question only the PI can answer. (ii) A definition of the observation
likelihood's m-dependence: PIFB2 never specifies it, and `:2715` evaluates it as Gaussian with **fixed**
precision Λ_{o_i}; if the intended dependence is through the precision rather than the mean, the
appendix stationarity at `:2828-2832` does not survive (a) verbatim and (a)'s cost rises materially.
(iii) An exact negative-ELBO realization of the predictive term with a live mixing law — none was
constructed and the obstruction is given above, but such a construction would revive (b) and would be a
new result.

### D6.7 Cost to decide, and two free repairs

Declaration only; the mathematics is finished and every residual is at machine precision. Execution:
(a) is roughly a day for the manuscript (two displays, eleven reconciliation loci, two equations that
gain a term, the `:913-918` env-agent re-derivation) plus half a day for eleven downstream documents;
(c) is roughly two hours plus the same half-day; (e) is (c) plus a paragraph; (d) is between them and
unpriced downstream. All carry zero runtime cost today.

While the files are open: fix the 65-character sha256 at `pifb2-crosswalk.md:29`, and record the
`:841`/`:855` population-joint versus per-agent inconsistency as its own item — it is real, it is
independent of D6, and no option resolves it.

## Decision sheet

Six lines. Fill in, hand back.

**D1 — Ω_ij typing.** Which of (a) pure coboundary / (a′) T_ij cocycle without bundle triviality /
(b) per-agent bundles / (c) represented link Θ_e / (d) base parallel transport Ω_γ?

> Answer: ______________________

*Recommended: (c). Triggers under (c): one clarifying line at `overview.md:43`; six re-scopes in
`PIFB2.tex` (`:208`, `:311-314`, `:320`, `:436`, `:2216`, `:2570`); no change to `Theory/`; four new
obligations including re-indexing `typed-construction.md` from ordered pairs to oriented edges.
Triggers under (a)/(a′): an erratum wave withdrawing nine named results across five files — but §3f.2
step 4 survives and §3e.2(ii) does not, contrary to worklog `:1411-1412`. Answer this one first;
under (a)/(a′), D2, D3 and D4 are questions about an operator with nothing in it.*

**D3 — representation channel.** Adopt the single-pushforward typing inside the belief channel
(`Theory/02:89-94`, `:427-441`), with the model channel a separate extent (`Theory/02:87`)?

> Answer: ______________________
> Representative half — defer to after D5? Yes / No: ______________________

*Recommended: yes to the typing half, yes to deferring the representative. Triggers: disposes of the
μ-only, split-channel and all-channels options; discharges O6, whose evidential half is already done;
requires an erratum against worklog `:1440-1442`'s Milnor invocation if the AIRM machinery is later
adopted.*

**D2 — operator and pencil metric.** (i) Fibre metric: Euclidean w_e I, or transported
w_e·(Ω_ij Σ_j Ω_ijᵀ)^{-1}? (ii) Pencil metric: ⊕Σ_i^{-1}, Λ = ⊕Σ_i^{-1} + L^Ω, or defer?

> (i) Answer: ______________________
> (ii) Answer: ______________________

*Recommended: (i) transported, with β retained as a scalar multiplier; (ii) defer, with ⊕Σ_i^{-1} as
the interim reading. Triggers under (i): closes O16 and lifts the compact-G fence at worklog
`:1504-1505`; requires replacing `Theory/09:346-348`'s one-orientation convention; requires changes to
the edge keying, duplicate check and `from_self_and_edges` signature in `interactions.py:128-188`;
forfeits the Cheeger route outright. Note that the pencil metric is provably a monotone reading
convention on fixed projectors and moves gap ratios by 3× — do not let it be presented as free. Also
correct worklog `:1403-1405`: the committed witness already returns 0.0.*

**D5 — β/γ side.** Ratify β and γ as recognition rows with π^q, π^s their generative counterparts?
And separately: which row may weight a coarse map — π, β^P(y), η, or none (row-free)?

> Rows: ______________________
> Coarse-map row: ______________________

*Recommended: ratify the rows (forced by `exact-elbo-proof.md:64-73`); leave the coarse-map row open.
Triggers: answers `overview.md:556-557` for the variational row; requires a status change at
`overview.md:485`, not a rename. Note `Theory/07b:1747-1748` (ESTABLISHED): no row can be
coarse-grained without the receiver law, so every row-only candidate is insufficient as stated and η
is the only candidate consistent with it. Note also that the row-free candidate conflicts with D2(i)'s
β retention.*

**D4 — normalization lift.** Spectral (eigen-ray plus a declared lift) or variational (KL-minimizer
over the tie family)? If variational: which parent Λ, and which readout map?

> Route: ______________________
> Parent Λ: ______________________
> Readout: ______________________

*Recommended: variational, scoped to the f_I > 0 stratum, with the f_I = 0 stratum declared OPEN
pending O12; parent = the coupled interaction precision of `Theory/09:30-36` (the product-family M
costs the variational warrant, F(r) − F(q*) = 22.7011 vs KL = 21.7080); readout must be declared
because Λ_c^{-1} and Moore–Penrose differ by 2.44%; residual gauge is GL(F_I) with ι a and r_M
canonical. Triggers: a new proposition plus proof in `Theory/09` after `:458`, not a paragraph;
voids O7's stated coercivity justification (category error, corrected in the text) while leaving O7
live for the frame sector.*

**D6 — observation binding.** Does the generative-model channel learn from observations?
Then: joint ζ = q ⊗ s / predictive / state-only / plug-in m̂ = E_s[M] / state-only-plus-declared-
enlargement?

> Learns from observations, yes/no: ______________________
> Typing: ______________________

*No recommendation offered; the brief's case for joint typing did not survive checking. Default if
undecided: state-only plus a declared enlargement remark — two hours of manuscript work, no new
obligations on two HIGH ledger claims, both other routes still reachable. Triggers under joint typing:
eleven reconciliation loci beyond E2's list, two equations gain a term, `PIFB2.tex:913-918` is emptied,
`overview.md:387-394` is retained as the price, m is re-typed from slow parameter to per-episode
latent, and `finite-environment-runtime-gap` acquires an implementation obligation. Independent of the
other five; can be answered at any point.*

## Open items carried forward, not decided here

1. **Ledger drift.** Pin `git:d892374`, HEAD `2927b0e`, seven commits. All twenty `artifact_revision`
   entries carry the same repo-level string, so all twenty bindings drifted together. Eight claims,
   seven HIGH, all `status: null`, mode `triage`. `.verification/active.json` does not exist at HEAD.
   Report only; do not re-pin during the sitting.
2. **O3 — witnesses not in the repository.** Every `[COMPUTED]` number in this document lives in a
   session scratchpad. Two are worth an hour each before any declaration is written into `Theory/`:
   the pure-coboundary holonomy/λ₁/tree-dependence triple (D1) and the transported-edge-metric
   congruence test (D2/D3).
3. **`pifb2-crosswalk.md:29`** — 65-character sha256; correct digest is
   `f80e6dabd9e5485649066e227e80beff1dd2b1082cf786bcdaeedb8cbd080ec4`.
4. **`PIFB2.tex:841` vs `:855`** — population-joint versus per-agent observation typing, independent
   of D6, unresolved by any option, and not on E2's list.
5. **Option (d) of D1 (Ω_γ under `hyp:geo-graph-base-transport`) is not fully priced.** It was
   surfaced late and has not been traced through the corpus at the level of the other four. §8 is
   already running it.
6. **O7 for the frame sector** stays live under every D4 answer: `Theory/09:1044-1049`
   (`\status{ESTABLISHED}`) blocks any left-equivariant permutation-symmetric aggregation on
   GL⁺(K)^n, so O14's Aff(K)-valued meta transports have no frame half.
7. **The Cheeger route** is forfeit under D2's recommended fibre metric. The quantitative half of the
   coherence criterion at worklog `:1030-1032` is lost, not merely unverified, and nothing in the
   corpus replaces it.
