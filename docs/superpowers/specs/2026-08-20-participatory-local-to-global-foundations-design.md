# Participatory Local-to-Global Foundations Design

**Date:** 2026-08-20  
**Status:** Proposed architecture; awaiting user approval before manuscript implementation  
**Repository baseline:** `9171363921d63047e61ccada2f9233c165087d43`  
**Frozen target:** `contract-sha256-368c9400e04e0700491b5a05ce03b074b8d146fa7243ce2327638237ab24a718`  
**Authoritative manuscript:** `C:\Users\chris and christine\Desktop\Research\manuscripts\gauge_vfe_rg`  
**Repository rule:** `Theory/` is a read-only synchronized snapshot, not the first edit target

## Purpose and decision

The manuscript will adopt a local-first descriptive order. It will begin with finite agents,
their law-valued epistemic states, their evaluated generative mechanisms, and the normalized
records produced at declared interactions. Complete population laws will enter only after an
explicit construction or selection:

\[
\left\{
\mathcal A_i,
G_{\theta,i,D},
\mathbb Q_{i,o,X},
K_a
\right\}_{i\in V,a\in\mathfrak A}
\longrightarrow
\begin{cases}
\mathbb P_{\theta,V} & \text{by normalized composition},\\
\mathbb Q_{V,o,X}\in
\operatorname{Cpl}\bigl((\mathbb Q_{i,o,X})_{i\in V}\bigr)
& \text{by a declared measurable selection},
\end{cases}
\longrightarrow
\mathcal L_V.
\]

This changes the explanatory dependency, not the need for joint probability laws. The exact
ELBO, correlation terms, gauge invariance, conditional free energies, and coarse-graining results
all require complete joint measures. The revision will therefore retain population-level
\(\mathbb P_{\theta,V}\) and \(\mathbb Q_{V,o,X}\), but it will no longer present them as primitive
objects that appear before the agent-local data from which they are constructed or selected.

The interpretive stance is participatory and Neo-Kantian in a restricted sense. Agent-relative
frames, model evaluators, and observation interfaces are treated as revisable conditions under
which relational records acquire inferential meaning. The mathematics does not establish an
agent-only ontology, a universal observer, consciousness, the physical creation of reality by
observation, or a background-free universe. Population laws are compatibility objects, not
agents or minds.

## Alternatives considered

### Cosmetic reorder

The smallest option would add a participatory paragraph to the introduction and rename a few
sections while retaining the primitive population signatures in the probability chapter. This
would not solve the dependency problem. The reader would still encounter \(P_\theta\) and \(Q_X\)
as unexplained global inputs before seeing the local kernels, model evaluators, recognition
marginals, and interaction records. The prose would claim a local-first architecture that the
definitions do not implement.

### Local-first construction inside the existing chapter graph

This is the selected design. Existing chapter labels and nearly all downstream theorem labels
remain stable. The geometry chapter clarifies what an agent carries. The probability chapter
introduces agent-block recognition laws, information interfaces, and coupling classes before any
population recognition law. The generative chapter constructs the population law from normalized
agent mechanisms and interaction-record kernels. The ELBO chapter selects a compatible population
recognition coupling and applies the existing measure-level identity. The philosophy chapter then
states the participatory interpretation and its limits.

This option changes the load-bearing order while reusing mathematics the manuscript already
contains: finite kernel composition, nonuniqueness of joints with fixed marginals, normalized
record attachment, exact ELBO/KL identities, total-correlation corrections, and once-only factor
accounting.

### New foundational part with replacement chapters

A third option would create new agent, interaction, coupling, and population-law chapters and move
the current chapters behind them. That would make the new order visually explicit, but it would
also disturb a large cross-reference graph and duplicate mature measure-theoretic material. It is
unnecessary for the present goal. A later major edition may adopt that organization after the
local-first definitions have stabilized.

## Foundational object types

### Geometric and probabilistic agent data

The existing geometric agent remains a section-bearing object over a declared contextual support.
Its belief and model sections take values in law fibers:

\[
q_i^b\in\Gamma(\mathcal C_i,\mathcal E_b|_{\mathcal C_i}),
\qquad
q_i^m\in\Gamma(\mathcal C_i,\mathcal E_m|_{\mathcal C_i}).
\]

The model-law section is not itself a generative kernel. Its value is a probability law over a
declared standard-Borel space \(\mathsf M_i\) of model presentations or coordinates. The agent's
generative-model structure is the pair

\[
\left(q_i^m,\operatorname{ev}_i\right),
\qquad
\operatorname{ev}_i:m_i\longmapsto K^X_{i,m_i},
\]

where \(K^X_{i,m_i}\) is a normalized evaluated generative mechanism of the declared type. An
agent with one definite model is the Dirac case \(q_i^m=\delta_{m_i}\). An agent uncertain over
or learning among models carries a non-Dirac model law. This realizes the intended conceptual
picture: an agent has beliefs and generative models, while keeping uncertainty over a model
distinct from the model mechanism evaluated at a presentation.

No generic linear structure follows. A selected family of probability laws may be convex, a
finite-dimensional smooth statistical model, an exponential family, a stratified family, or none
of these. Vector addition and unrestricted scalar multiplication do not preserve normalization or
positivity. Every tangent space, Fisher metric, natural gradient, or linear connection therefore
belongs to a separately declared regular tier.

For finite-design probability statements, define the agent block
\(\mathsf Y_{i,D}\) to contain that agent's declared belief and model coordinates across the
finite design. The agent-local recognition law is a normalized kernel

\[
\mathbb Q_i:\mathsf I_i\rightsquigarrow\mathsf Y_{i,D},
\qquad
\mathbb Q_{i,o,X}:=\mathbb Q_i(A_i(o,X),\cdot),
\]

where \(\mathsf I_i\) is an information interface and
\(A_i:\mathsf O_D\times\mathsf X\to\mathsf I_i\) is a declared measurable access map. The
minimal noncommittal realization takes \(\mathsf I_i=\mathsf O_D\times\mathsf X\) and
\(A_i=\operatorname{id}\). A stronger decentralized claim must restrict \(A_i\) to the agent's
state, incident records, boundary messages, or other typed local data.

Compatibility between the continuum sections and the finite block law remains a hypothesis. At
each design point, the belief and model section values must agree with the corresponding channel
marginals of \(\mathbb Q_{i,o,X}\) only when that compatibility is explicitly declared. Neither
side is defined from the other.

### Agent-local generative mechanisms

At each design point \(c_a\), the existing normalized component kernels will be bundled into
one agent-indexed conditional mechanism

\[
G_{\theta,i,a}:
\left(\mathsf X\times\mathsf Y_{\operatorname{pa}(i),a}\right)
\rightsquigarrow
\mathsf Y_{i,a}.
\]

In the current directed realization, \(G_{\theta,i,a}\) is the ordered composite of the existing
model and belief kernels \(P_{\theta,i}^{m}\) and \(P_{\theta,i}^{k}\), with all conditioning
coordinates typed. This notation is the precise replacement for the user's conceptual shorthand
\(P_i\). Calling it \(G_{\theta,i,a}\) avoids implying that it is an unconditional local
marginal and avoids collision with the final population law. The standing cross-design
hypothesis then forms the finite-design product
\(G_{\theta,i,D}:=\bigotimes_{a=1}^{M}G_{\theta,i,a}\), conditional on the corresponding
parent blocks. A future model with cross-design generative dependence would need new local
mechanisms and a new normalization proof.

The agent's evaluated model kernel \(K^X_{i,m_i}\), the directed transition
\(T_{i\leftarrow j}\), the normalized interaction-record kernel \(K_a\), and an undirected
positive potential \(\psi_{ij}\) are different types. They must not share a bare symbol.

### Interaction records

For each declared interaction record \(a\in\mathfrak A\) with scope
\(\partial a\subseteq V\), use a normalized Markov kernel

\[
K_a:
\left(\mathsf X\times\mathsf Y_{\partial a,D}\right)
\rightsquigarrow
\mathsf O_a,
\qquad
K_a(X,y_{\partial a},\mathsf O_a)=1.
\]

A uniquely owned pairwise record may be written \(K_{\{i,j\}}\), or \(K_{ij}\) after a local
sentence fixes an orientation or ownership convention. It appears once. Writing both \(K_{ij}\)
and \(K_{ji}\) for one undirected record would double count it.

Once a record value \(o_a\) is fixed, its density
\(\ell_a(o_a\mid y_{\partial a},X)\) is a likelihood as a function of the latent coordinates. It
need not integrate to one over those latent coordinates. An undirected potential
\(\psi_{ij}(y_i,y_j)\) is not a record kernel and does not define a probability law until its
global normalizer is positive and finite.

## Construction of the population generative law

Let \(\Gamma\) be a finite directed acyclic graph with topological order
\(v_1,\ldots,v_N\). At each design point \(c_a\), the ordered composition

\[
\mathbb P_{\theta,V,a}^{Y}(dy_a\mid X)
:=
\overrightarrow{\prod_{\ell=1}^{N}}
G_{\theta,v_\ell,a}
\left(dy_{v_\ell,a}\mid y_{\operatorname{pa}(v_\ell),a},X\right)
\]

is a normalized measurable probability kernel. The proof is finite induction: integration of a
bounded measurable function against a probability kernel preserves boundedness and measurability,
and applying the construction to the constant function one gives unit mass. Under the manuscript's
declared conditional independence of design points,

\[
\mathbb P_{\theta,V}^{Y}(dy\mid X)
=\bigotimes_{a=1}^{M}\mathbb P_{\theta,V,a}^{Y}(dy_a\mid X).
\]

The current generative chapter already proves both results in component notation.

Conditional independence of the declared records given the latent configuration then gives

\[
\mathbb P_{\theta,V}(dy,do\mid X)
=
\mathbb P_{\theta,V}^{Y}(dy\mid X)
\prod_{a\in\mathfrak A}
K_a(X,y_{\partial a},do_a).
\]

This law is normalized for an arbitrary finite interaction hypergraph, even when the interaction
hypergraph contains cycles, because every record coordinate can be integrated out first. Each
record kernel contributes one and leaves the normalized latent law. The existing local/collective
chapter proves this statement. The generative chapter will gain an abstract construction
proposition establishing this seam, while the existing labeled local/collective theorem remains
in place as the detailed specialization. Local conditional VFE consequences and durable labels
therefore remain in the local/collective chapter.

Arbitrary reciprocal state conditionals do not receive the same treatment. Two binary
conditionals that respectively force \(Y_1=Y_2\) and \(Y_2=1-Y_1\) have no compatible joint.
Mutual state dependence therefore requires an acyclic ordering, an explicit temporal or
asynchronous schedule, a common-cause construction, or a globally normalized undirected model.

For an undirected positive-potential alternative,

\[
\mathbb P_{\theta,V}^{\psi}(dy\mid X)
=
Z_X^{-1}
\prod_{\{i,j\}\in E}\psi_{ij}(y_i,y_j;X)
\mathbb P_{\theta,V}^{Y}(dy\mid X),
\]

with

\[
0<Z_X=
\int
\prod_{\{i,j\}\in E}\psi_{ij}(y_i,y_j;X)
\mathbb P_{\theta,V}^{Y}(dy\mid X)<\infty.
\]

The current counterexample showing that locally normalized node terms and a positive edge
potential can still yield an infinite normalizer remains in place.

No generative factor may read \(\mathbb Q_{V,o,X}\), one of its marginals or parameters, or a
posterior derived from \(\mathbb P_{\theta,V}\). The existing fixed-joint prohibition remains
load-bearing. Reciprocal participation belongs in inference, messages, delayed dynamics, or a
separately normalized joint, not in a self-referential same-step generative factor.

## Construction and selection of the population recognition law

For each admitted \((o,X)\), define the unconstrained coupling class

\[
\operatorname{Cpl}(\mathbb Q_{\bullet,o,X})
:=
\left\{
R\in\mathcal P\left(\prod_{i\in V}\mathsf Y_{i,D}\right):
(\operatorname{pr}_i)_\#R=\mathbb Q_{i,o,X}
\text{ for every }i
\right\}.
\]

The class is nonempty because it contains the independent product coupling

\[
\mathbb Q^{\otimes}_{V,o,X}
=\bigotimes_{i\in V}\mathbb Q_{i,o,X}.
\]

It is convex because marginalization is affine. The product construction is also measurable in
\((o,X)\) when the component laws are measurable kernels. This establishes availability of one
population recognition kernel without imposing mean field as the only admissible dependence
model.

The manuscript will strengthen its current Gaussian nonuniqueness witness to the general finite
criterion: the unconstrained coupling class is a singleton if and only if at most one marginal is
non-Dirac. If two marginals \(\mu,\nu\) are non-Dirac, choose measurable sets \(A,B\) with
\(0<\mu(A),\nu(B)<1\), put \(f=1_A-\mu(A)\) and \(g=1_B-\nu(B)\), and define

\[
dR_\varepsilon(x,y)
=
\left[1+\varepsilon f(x)g(y)\right]d\mu(x)d\nu(y),
\qquad 0<|\varepsilon|<1.
\]

The density is nonnegative, integrates to one, preserves both marginals, and varies with
\(\varepsilon\). Tensoring with the remaining marginals gives distinct population couplings. If
all but one marginal are Dirac, the fixed coordinates and the remaining marginal determine the
joint.

A correlated population recognition law is therefore additional probabilistic data:

\[
\mathbb Q_{V,o,X}
=
\mathsf S_{o,X}
\left((\mathbb Q_{i,o,X})_{i\in V}\right),
\qquad
\mathbb Q_{V,o,X}\in
\operatorname{Cpl}(\mathbb Q_{\bullet,o,X}),
\]

where \(\mathsf S\) is a declared measurable selection rule. A copula, common latent variable,
ordered recognition conditionals, graphical recognition family, or product restriction may
supply such a rule. Local marginals alone cannot.

Additional support, moment, record-consistency, gauge, or conditional-independence constraints
define

\[
\operatorname{Cpl}_{\mathcal R}(\mathbb Q_\bullet)
=
\operatorname{Cpl}(\mathbb Q_\bullet)\cap\mathcal R.
\]

The product coupling does not prove this intersection nonempty. Feasibility and measurable
selection are separate theorems or explicit hypotheses for each constrained family.

## Exact population ELBO and local-to-global decompositions

Once \(\mathbb P_{\theta,V}\) has been constructed and a compatible
\(\mathbb Q_{V,o,X}\) selected, the current measure-level ELBO applies without conceptual change.
At a regular observation with positive finite evidence and selected posterior
\(\boldsymbol\Pi_{\theta,V,o,X}\), define

\[
\mathcal L_V^{\mathrm{ext}}
(\mathbb Q_{V,o,X};X,o)
:=
\log p_{\theta,V}(o\mid X)
-
\operatorname{KL}
\left(
\mathbb Q_{V,o,X}
\middle\Vert
\boldsymbol\Pi_{\theta,V,o,X}
\right).
\]

Then

\[
\log p_{\theta,V}(o\mid X)
-\mathcal L_V^{\mathrm{ext}}
=
\operatorname{KL}
\left(
\mathbb Q_{V,o,X}
\middle\Vert
\boldsymbol\Pi_{\theta,V,o,X}
\right),
\]

and equality of the lower bound with the log evidence holds exactly when the two joint measures
are equal. Under the current domination, absolute-continuity, and log-integrability hypotheses,
the extended functional has the familiar finite split

\[
\mathcal L_V
=
\mathbb E_{\mathbb Q_{V,o,X}}
\left[
\log p_{\theta,V}(o,Y\mid X)
-\log q_{V,o,X}(Y)
\right].
\]

The entropy term is joint. It cannot be replaced by a sum of agent-marginal entropies. For a
product baseline \(\bigotimes_i\rho_i\), the exact extended identity is

\[
\operatorname{KL}
\left(\mathbb Q_{V,o,X}\middle\Vert\bigotimes_i\rho_i\right)
=
\operatorname{TC}(\mathbb Q_{V,o,X})
+\sum_i
\operatorname{KL}(\mathbb Q_{i,o,X}\Vert\rho_i).
\]

For a directed correlated baseline, the exact chain rule uses conditional recognition laws in the
same topological order:

\[
\operatorname{KL}
\left(\mathbb Q_{V,o,X}\middle\Vert\mathbb P_{\theta,V}^{Y}\right)
=
\sum_{\ell=1}^{N}
\mathbb E
\operatorname{KL}
\left(
\mathbb Q_{v_\ell\mid v_1:\ell-1}
\middle\Vert
G_{\theta,v_\ell,D}
(\cdot\mid Y_{\operatorname{pa}(v_\ell)},X)
\right).
\]

No general sum of marginal agent complexities follows from this formula. Likewise, incident local
VFEs do not sum to the collective VFE because a shared record occurs in every incident conditional
objective. The current once-only factor accounting remains the governing identity.

## Participatory and Neo-Kantian interpretation

The introduction will state the interpretation only after the formal dependency is visible:

> The theory begins with finitely many agents, their local law sections and evaluated generative
> mechanisms, and normalized kernels for records produced through their interactions. Complete
> population laws enter only after an explicit compatibility construction. They encode the joint
> dependence required by evidence and free-energy identities but are not additional agents and
> need not be represented by any participant.

The philosophy chapter will locate the Neo-Kantian role in the agent-relative structures, not in
the fixed global base alone:

> An agent's frame, model evaluator, and admissible observation interface determine how relational
> records acquire inferential meaning for that agent. These structures are interpreted as
> revisable conditions of possible experience within the model, not as universal and immutable
> forms imposed on every possible knower. This is an interpretation of the formal architecture,
> not a consequence of its probability theorems.

Participation means reciprocal inferential dependence mediated by relational records inside a
fixed normalized model. Records generated through relations change posterior and predictive
states. No posterior is fed back as an input to the same-step generative kernel. This preserves
the current fixed-joint prohibition while allowing agent beliefs and model laws to evolve under a
later declared inference or action dynamics.

Kant's constitutive reversal supplies historical lineage but not the multiple agent-indexed
frames, learned model evaluators, or probability constructions used here. Reichenbach's revisable
coordinating principles and Cassirer's relation-first account are closer interpretive precedents.
Wheeler remains a bounded analogy for participatory ordering. None of these sources proves the
mathematics or supplies evidence for the ontology. The manuscript will cite primary texts and
state this scope explicitly.

The following statements remain forbidden without new constructions or evidence: that everything
that exists is an agent; that the population law is a universal agent; that local laws uniquely
determine correlation; that observations create physical existence; that gauge invariance proves
ontological objectivity; that the VFE is already a physical action; that a model-law section is a
generative kernel; that reciprocal conditionals automatically form a normalized joint; or that
the fixed contextual base and principal bundle emerge from agents.

## Canonical notation and collision policy

| Concept | Canonical notation | Rule |
|---|---|---|
| Belief-law section | \(q_i^b\) | Agent-local law-valued section; retain explicit \((o,X)\) dependencies where present |
| Model-presentation law section | \(q_i^m\) | Law over model coordinates or presentations; not a generative kernel |
| Model presentation | \(m_i\in\mathsf M_i\) | Random or selected model coordinate |
| Evaluated model mechanism | \(\operatorname{ev}_i(m_i)=K^X_{i,m_i}\) | Normalized kernel with a declared domain and codomain |
| Agent finite block | \(\mathsf Y_{i,D}\) | Belief and model coordinates attached to agent \(i\) over the finite design |
| Agent information interface | \(A_i:\mathsf O_D\times\mathsf X\to\mathsf I_i\) | Declares what the recognition kernel may read |
| Agent recognition law | \(\mathbb Q_{i,o,X}\) | Block law; its channel/design marginals may match section values by hypothesis |
| Agent generative mechanism | \(G_{\theta,i,a}\), block \(G_{\theta,i,D}\) | Normalized conditional kernel assembled from the existing local components |
| Directed transition | \(T_{i\leftarrow j}\) | Normalized over the receiving state; belongs to an order or schedule |
| Interaction-record kernel | \(K_a\), pairwise \(K_{\{i,j\}}\) | Normalized over the record coordinate and counted once |
| Undirected potential | \(\psi_{ij}\) | Nonnegative factor requiring a finite positive global normalizer |
| Population generative law | \(\mathbb P_{\theta,V}\) | Constructed normalized joint; foundational population uses of \(P_\theta\) migrate in the same revision |
| Coupling class | \(\operatorname{Cpl}(\mathbb Q_\bullet)\) | All joint laws with the declared agent-block marginals |
| Population recognition law | \(\mathbb Q_{V,o,X}\) | Measurably selected coupling; foundational population uses of \(Q_X\) migrate in the same revision |
| Selected posterior | \(\boldsymbol\Pi_{\theta,V,o,X}\) | Derived regular conditional of \(\mathbb P_{\theta,V}\), never a generative input |
| Meta-agent | \(\mathcal A_A\) only after construction | Requires a coarse state, interfaces, model evaluator, recognition law, and update rule |

This policy is consistent with the approved full-pointwise meta-agent design, which reserves
blackboard-bold symbols for full joint laws and keeps \(q_i^b,q_i^m\) for section values. The new
agent-block law \(\mathbb Q_{i,o,X}\) is an intermediate object that the earlier design did not
name. Foundational population uses of \(P_\theta,Q_X\) migrate in this revision without defining
duplicate aliases. Generic lemma-local probability measures, generic statistical families in
later chapters, and the distinct fine/coarse tower notation keep their established symbols when
their types differ. No theorem will use one symbol for both a local marginal and a population
joint.

## Manuscript migration map

| Source | Required change | Stable material |
|---|---|---|
| `Theory/SPEC.md` | Amend the opening contract so local agent data are primitive and global laws are constructed or selected; add the coupling-selection and interpretation boundaries | Fixed-joint prohibition, status taxonomy, standard-Borel and reference-measure rules |
| `Theory/01_introduction.tex` | Open with the local-first dependency and move interaction-record construction before the first global ELBO display | Reading map, established downstream results, chapter labels |
| `Theory/02_geometry.tex` | Clarify the law-fiber/model-evaluator pair and move or preview the agent definition before extended global geometry; state the absence of generic linear structure | Principal bundle, associated bundles, frame changes, connections, holonomy proofs |
| `Theory/03_probability.tex` | Replace the primitive population signatures with local blocks, information interfaces, local recognition kernels, compatibility hypotheses, coupling existence, and nonuniqueness; forward-reference constructed/selected global laws | Measure/reference setup, RN and regular-conditional results, support/integrability rules |
| `Theory/04_generative.tex` | Retitle and reframe as local-to-global construction; define \(G_{\theta,i,a}\) and \(G_{\theta,i,D}\); add an abstract normalized record-extension proposition | Existing kernel composition, exact normalization, fixed-joint prohibition, undirected alternative, gauge covariance |
| `Theory/05_elbo.tex` | Begin with selected \(\mathbb Q_{V,o,X}\in\operatorname{Cpl}(\mathbb Q_\bullet)\); preserve the full joint entropy and exact ELBO | Extended identity, equality criterion, total correlation, E/M-coordinate results |
| `Theory/05b_local_collective_elbo.tex` | Retain the labeled record-kernel normalization specialization and reference the earlier abstract seam; preserve conditional/local VFEs and once-only factor accounting | Conditional VFE, unilateral-change identity, observation/message equivalence, attention results |
| `Theory/12_philosophy.tex` | Relocate the Kantian role from a global-base dichotomy to revisable agent-relative frames/models/interfaces; state that global laws are not agents; keep Wheeler bounded | Status fences, observational-closure hypothesis, operational tests, open ontology claims |
| `Theory/appendix_notation.tex` | Add local block laws, coupling class, selection rule, and the four-way kernel/potential distinction; record legacy aliases | Existing bundle, coarse-channel, posterior, and RG registry |
| `Theory/references.bib` | Verify or add primary Kant, Reichenbach, Cassirer, Wheeler, Kallenberg, and graphical-model sources with exact scope | Existing valid citation keys and historical attributions |

The implementation must edit the authoritative Research manuscript first. The repository snapshot
will be regenerated or synchronized only after the authoritative TeX compiles and the Research
worktree's unrelated WIP has been preserved. The current repository `Theory/` tree must not be
edited as though it were the source of truth.

## Dependency-preservation rules

The implementation will retain `ch:geometry`, `ch:probability`, `ch:generative`, `ch:elbo`, and
`ch:local-collective-elbo`. Existing downstream references therefore continue to resolve. Mature
theorem labels remain in their present files unless a proof must move with a newly prior
definition. A relocated theorem receives a compatibility label or a deliberate global reference
update in the same change.

The population generative law must exist before posterior, evidence, and ELBO definitions. The
agent-local recognition laws and coupling class must exist before the population recognition law
is selected. The selected population law must exist before any exact joint entropy, total
correlation, or local conditional disintegration. Gauge pushforwards must act on the local data and
commute with the construction or selection before population-level gauge invariance is restated.
No later coarse-graining theorem may infer a full parent agent from parent marginals alone.

The fixed-joint prohibition and the common-channel coarse-graining rule remain unchanged. A local
recognition update may depend on incident records and received messages, but a generative factor
may not read the live recognition law it is meant to approximate. A meta-agent is not identified
with a marginal or a population summary; it requires the full typed construction already frozen
in the 2026-08-15 meta-agent design.

## Stable labels and scope-sensitive migration

The include order in `Theory/main.tex` will not change. The chapter labels `ch:geometry`,
`ch:probability`, `ch:generative`, `ch:elbo`, and `ch:local-collective-elbo` remain stable. The
probability labels `eq:prob-rcp`, `eq:prob-rcp-density`, `eq:prob-kernel-kl-partitions`,
`thm:prob-kernel-rn-measurable-version`, `cor:prob-common-reference-joint-density`,
`hyp:prob-regular-observation`, `hyp:prob-classical-split-elbo`,
`def:prob-recognition-marginals`, and `prop:prob-marginals-do-not-determine-joint` retain their
current mathematical roles.

The existing interface labels `def:prob-structural-kernel-signatures`,
`eq:prob-generative-signature`, `eq:prob-recognition-signature`, and
`def:elbo-recognition-kernel` are durable consumers' entry points. Their displayed content may
change from primitive global declarations to admitted-completion or selected-coupling interfaces,
but their identifiers will remain. Likewise, `prop:obs-interaction-normalization`,
`hyp:local-interaction-kernels`, `eq:obs-interaction-joint`, `eq:obs-global-ledger`, and
`eq:obs-singleton-incident-counting` remain in the local/collective chapter.

The notation migration is scope sensitive. Population uses in Chapters 1 and 3 through 5b move
to blackboard-bold indexed laws. Generic theorem-local dummy measures remain \(P,Q\). Generic
statistical families in later information-geometric chapters are inspected rather than
mechanically renamed. The established full-law tiers \(\mathbb P_I,\mathbb Q_I\) in the network-RG
chapter and \(\mathbb P_\theta,\mathbb Q_\phi\) in the hierarchical tower retain their distinct
scopes. No equation introduces \(\mathbb P_{\theta,V}:=P_\theta\) or an analogous alias.

## Implementation sequence

The first implementation phase will revise the authoritative `SPEC.md` and notation registry,
then compile. The second phase will revise the introduction and the agent/model-fiber explanation.
The third phase will add local recognition interfaces and the coupling theorems to the probability
chapter. The fourth will reframe the existing generative composition, add the abstract
record-extension seam while retaining the detailed labeled specialization, and preserve the
typing prohibition. The fifth will reframe the exact
ELBO and local/collective chapters. The sixth will revise the philosophy chapter and bibliography.
Only after the Research manuscript compiles and its cross-references stabilize will the repository
snapshot, provenance record, and daily change log be updated.

The work will be implemented in one coordinated revision rather than as disconnected chapter
patches. No result will be retagged as established merely because it is standard or because an
expert agent endorsed it. New propositions will carry complete proofs or exact primary-source
scope. Interpretive declarations will remain definitions or hypotheses.

## Validation and acceptance criteria

The mathematical acceptance checks are:

1. every displayed local generative mechanism has a declared domain, codomain, normalization
   variable, and dependency order;
2. every interaction record is owned and counted exactly once;
3. the directed composition proof yields a normalized \(\mathbb P_{\theta,V}\), while reciprocal
   conditionals and undirected potentials are fenced by their separate existence conditions;
4. the product coupling proves nonemptiness of the unconstrained recognition class, and an
   explicit perturbation proves nonuniqueness when two marginals are non-Dirac;
5. every constrained coupling family either has a construction or is marked as a hypothesis;
6. the exact ELBO is applied only to one constructed joint and one selected joint, with support and
   integrability conditions unchanged;
7. no marginal-entropy substitution appears without the total-correlation correction;
8. gauge transformations preserve the constructed joint probabilities, KL divergences, and ELBO;
9. no downstream coarse or meta-agent result treats marginals as a full joint; and
10. the words agent, model law, model presentation, evaluated kernel, record kernel, transition,
    potential, population law, posterior, and meta-agent retain distinct types.

The interpretive acceptance checks are local-access, joint-extension, coupling, relational-record,
non-idleness, meta-agent typing, action-principle, and representation tests. In particular, an
agent update that requires unmediated access to the analyst's full \(\mathbb P_{\theta,V}\),
\(\mathbb Q_{V,o,X}\), or covariance has not yet been implemented as a decentralized participatory
mechanism. Calling the VFE a physical action remains prohibited until a path-space functional,
admissible variations, boundary conditions, and equations of motion are separately supplied.

Mechanical validation will include a clean LaTeX build of the authoritative manuscript, an
undefined-reference and duplicate-label scan, a notation-collision scan across the manuscript and
governing specification, the existing theory-oracle and documentation tests, and one broader CPU
test pass under the repository's declared environment. Any CUDA claim would use the configured
CUDA interpreter, but this manuscript revision has no planned GPU requirement.

## Primary-source scope

The finite-kernel and standard-Borel construction may cite Kallenberg, *Foundations of Modern
Probability*, third edition, Springer, 2021, DOI
`https://doi.org/10.1007/978-3-030-61871-1`. The graphical-model factorization context may retain
Wainwright and Jordan, *Graphical Models, Exponential Families, and Variational Inference*, 2008,
DOI `https://doi.org/10.1561/2200000001`. Kant's *Critique of Pure Reason*, Reichenbach's
*The Theory of Relativity and A Priori Knowledge*, Cassirer's *Substance and Function*, and
Wheeler's participatory essays support bounded historical comparisons only. They do not establish
the local-to-global probability construction or a physical ontology.

No novelty claim is licensed by this design. The contribution is the manuscript-specific assembly
of standard probability constructions, gauge-typed agent data, exact variational identities, and
a disciplined participatory interpretation.

## Approval gate

No authoritative manuscript source will be changed until the user approves this written design.
Approval authorizes the local-first dependency rewrite, the explicit coupling layer, the
agent/model-evaluator clarification, the bounded participatory interpretation, and the required
`SPEC.md` amendment. Any request to make global laws disappear, to identify them with an agent, or
to claim a physical action principle would require a new design because it would change the frozen
target and invalidate this contract.
