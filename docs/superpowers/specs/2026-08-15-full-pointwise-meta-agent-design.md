# Full Pointwise Meta-Agent Program Design

**Date:** 2026-08-15
**Status:** Approved architecture; no theorem in this document is thereby established
**Repository baseline:** 8c0f4d5b4116ac3883665756a451e025f0712b97
**Primary tier:** normalized laws and Markov kernels on standard-Borel spaces
**Optional regular tiers:** parameterized statistical manifolds, smooth bundle data, and
finite-dimensional computational realizations

## Purpose

The released pointwise RG certificate begins with a finite agent network at one fixed base point
$r_*$. It proves exact channelwise marginal agreement, holonomy stabilization, normalized marked
network pushforward, and the common-channel VFE chain rule. It deliberately does **not** construct a
full meta-agent: the certified pair of parent marginals $(Q_q,Q_m)$ does not determine a correlated
recognition law, a generative joint, a posterior, or an autonomous variational system.

This design freezes the architecture for closing that pointwise gap. At one $r_*$ the target is a **full pointwise probabilistic datum** for a candidate parent, not yet a full geometric meta-agent. An agent in the governing geometry is a pair of local sections on a domain; a parent pair of sections still requires the later patchwise gluing theorem, and autonomy requires a further dynamics theorem. The order is load-bearing:

1. clean and standardize notation before adding another theorem;
2. type model-law spaces and generative-kernel families separately;
3. construct the full fine and parent probabilistic data through one normalized,
   recognition-independent coarse channel while structural data remain fixed;
4. derive parent marginals and the exact lossy VFE identity from those full laws;
5. state the joint full-law/channel holonomy obligations and dynamic closure boundary; and
6. after the pointwise datum closes, execute the comparison theorem, overlap-region gluing, and
   participatory nonequilibrium projects in that strict order.

The ambient construction is not Gaussian. Multivariate Gaussians may instantiate finite examples
or numerical algorithms, but they may not define the general belief fiber, model fiber, generative
kernel fiber, coarse channel, or meta-agent.

## Existing certified boundary

The following sources govern the inherited result and must not be silently weakened:

- solid_RG_theory.md and docs/derivations/2026-08-14-pointwise-meta-agent-rg/ certify the frozen
  pointwise two-channel result.
- Theory/06_general_coarsegraining.tex certifies normalized Markov-kernel pushforward, data
  processing, equality and recovery conditions, and unrestricted law-level barycenters.
- Theory/07b_agent_network_rg.tex certifies the common-channel VFE chain rule, fine--meta bridge
  kernels, marked attention closure, and the hypotheses of a complete finite effective theory.
- Theory/SPEC.md requires a fixed normalized generative joint, forbids a generative kernel from
  reading a recognition law or posterior, and distinguishes belief-law, model-law, and
  generative-kernel fibers.
- The released intervention packages compare analyst-declared protocol responses. They do not
  derive ontic actions, policies, or agents from passive data.

This project may use those results as lemmas. It must not mark the full meta-agent as established
until a new revision-bound proof package closes the obligations below.

## Phase 0: canonical notation and collision policy

Notation cleanup is a prerequisite, not a final copyedit. Before proving the new construction,
create one canonical symbol registry and make Theory/SPEC.md plus Theory/appendix_notation.tex agree
with it. For every symbol the registry records its type, domain and codomain, scope, status,
canonical source, legacy aliases, and forbidden uses.

### Canonical registry

| Concept | Canonical notation | Type and rule |
|---|---|---|
| Contextual base | $\mathcal C$ | Fixed base manifold or measurable contextual base; never time or RG depth by implication |
| Agent domain | $\mathcal C_i$ | Domain on which agent $i$ supplies its pair of local sections |
| Common overlap | $\mathcal U_A:=\bigcap_{i\in A}\mathcal C_i$ | Region occupied by every agent in $A$; reserve script $\mathcal U,\mathcal V$ for patches |
| Pointwise context | $r_*\in\mathcal U_A$ | One fixed base point for the present construction |
| Cover | $\mathfrak U$ | A declared cover of the relevant base region |
| Principal bundle | $\mathscr P_G\to\mathcal C$ | Never use bare $P$ for the bundle |
| Belief-law section | $q_i^b$ | Local section whose value is a normalized law on a state-belief fiber |
| Model-law section | $q_i^m$ | Local section whose value is a normalized law on a model space |
| Fine model space | $\mathsf M_i$ | Declared measurable space of generative-model coordinates or presentations |
| Fine model evaluation | $\operatorname{ev}_i:m_i\mapsto K^X_{i,m_i}$ | Measurable map into a declared generative-kernel fiber at fixed structural $X$; sample $m_i$ is not a model law |
| Parent model space | $\mathsf M_A$ | Model-coordinate component retained by the parent state space |
| Structural data | $X$, with $X_A=\chi_A(X)$ | Fixed conditioning data; neither randomized nor an output of $C_A$ |
| Parent random interface | $\xi_A\in\boldsymbol\Xi_A$ | Retained random parent/boundary interface coordinate in $\mathsf Z_A$; distinct from $X_A$ |
| Parent retained marks | $h_A\in\mathsf H_A$ | Boundary, component, or holonomy records retained when declared |
| Parent model evaluation | $\operatorname{ev}_A:m_A\mapsto K^{X_A}_{A,m_A}$ | Measurable map into $\operatorname{Kern}(\boldsymbol\Xi_A,\mathsf B_A\times\mathsf O_A\times\mathsf H_A)$ at fixed $X_A$ |
| Fine generative joint | $\mathbb P_I(Do,DY\mid X)$ | Fixed normalized law on observations and fine latent/model variables conditional on structural $X$ |
| Fine recognition law | $\mathbb Q_{I,o,X}$ | Normalized correlated recognition law conditional on admitted $o$ and $X$ |
| Fine posterior | $\boldsymbol\Pi_{I,o,X}$ | Posterior derived from $\mathbb P_I(\cdot\mid X)$, not an input to a generative kernel |
| Parent generative joint | $\mathbb P_A(Do_A,Dz_A\mid X)$ | Common-channel pushforward with the observation coordinate unchanged |
| Parent recognition law | $\mathbb Q_{A,o,X}$ | Common-channel pushforward of $\mathbb Q_{I,o,X}$ |
| Parent posterior | $\boldsymbol\Pi_{A,o,X}$ | Common-channel pushforward of $\boldsymbol\Pi_{I,o,X}$ |
| Parent belief/model marginals | $q_A^b,q_A^m$ | Derived projections of the full parent recognition law |
| Parent prior marginals | $p_A^b,p_A^m$ | Derived projections of the parent generative conditional; never replacements for the joint |
| Parent posterior marginals | $\boldsymbol\Pi_{A,o,X}^b,\boldsymbol\Pi_{A,o,X}^m$ | Derived projections of the full parent posterior, distinct from recognition marginals |
| Parent output space | $\mathsf Z_A=\mathsf B_A\times\mathsf M_A\times\boldsymbol\Xi_A\times\mathsf H_A$ | Retained random state only; structural $X_A$ remains outside |
| Coarse channel | $C_A:\mathsf Y_I\rightsquigarrow\mathsf Z_A$ | One normalized recognition-independent Markov kernel |
| Attention rows | $\beta_{ij},\gamma_{ij}$ | Conditional source rows in the belief and model channels |
| Receiver occupancy | $\alpha_i^x$ | External positive normalized receiver mass for channel $x$; not a learned attention logit |
| Joint edge event | $\eta_{ij}^q=\alpha_i^q\beta_{ij}$, $\eta_{ij}^m=\alpha_i^m\gamma_{ij}$ | Normalized law pushed by exact attention RG |
| Action functional | $\mathscr S$ | Variational action; reserve lowercase $a_t$ for behavioral action only if later declared |
| Auxiliary evolution parameter | $t$ | Typed only after a flow is supplied; not automatically physical time, base position, or RG depth |
| Deterministic moving coarse map | $c_t$ | Differentiable special case only; uppercase $C_A$ remains a Markov kernel |
| Intervention example | $R\to E\to O$ | Retained input, intervened target, and output in the released comparison package; ordinary $R$ is not an overlap region |

Ordinary $\pi_{ij}$ remains the attention source prior where needed. Do not introduce $\varpi_i$
for receiver occupancy: $\varpi$ already denotes an associated-bundle projection in the governing
theory. The Greek letter $\varpi$ is a variant lowercase pi, pronounced “var-pie,” but its existing
geometric use controls here.

### Collision and migration rules

1. A symbol receives one semantic type within a theorem. Type changes require a new symbol, not a
   prose qualification.
2. Bare $P$ and $Q$ are permitted only as local dummy probability measures inside a
   self-contained lemma. Global laws use blackboard bold; the principal bundle uses
   $\mathscr P_G$.
3. The established section notation $q_i^{o,X},s_i^{o,X}$ retains its explicit dependencies.
   A semantic migration may use $q_i^{b;o,X},q_i^{m;o,X}$, but bare $s_i$ is not globally renamed.
   Only explicitly law-valued uses of $m_i$ in frozen pointwise-RG passages may be documented as
   local aliases; the sample latent $m_i\in\mathsf M_i$ remains $m_i$ and never denotes a law.
4. Previous root marginals $Q_q,Q_m$ migrate to $q_A^b,q_A^m$ at locally fixed $(o,X)$. The old
   theorem remains cited under its historical notation.
5. Do not introduce free-standing $P_q,P_m$ as if two marginals were a generative joint. When
   useful, $p_A^b,p_A^m$ are explicitly derived marginals of $\mathbb P_A$.
6. Structural data use $X$, overlap regions use $\mathcal U_A$, and the released intervention
   comparison retains ordinary $R,E,O$. Script and ordinary letters are not silently identified.
7. Every coarse symbol declares whether it is a deterministic map, Markov kernel, linear operator,
   or abstract categorical arrow. One symbol may not play several roles.
8. Every migrated source gets either a semantic replacement or a documented type-and-scope legacy
   alias. A canonical token may not have two types in one scope, and one alias may not resolve to
   multiple canonical entries in one scope.
9. Dependencies on $X$ and admitted $o$ remain visible in theorem definitions. Suppression is allowed
   only after a local sentence freezes them. No global replacement may alter frozen evidence.

Phase 0 ends only after a repository collision scan covers Theory/, solid_RG_theory.md,
overview.md, docs/STATUS.md, active design and plan documents, and the live worklog. The scan must
distinguish current sources from immutable released evidence.

## Phase 1: typed model spaces and evaluation

For each fine agent, let $\mathsf M_i$ be a standard-Borel space of generative-model coordinates or
presentations. A sample $m_i\in\mathsf M_i$ is distinct from the law-valued section
$q_i^{m;o,X}(r_*)\in\mathcal P(\mathsf M_i)$. Each fine evaluation family keeps its declared dependence
on structural $X$, observation variables, and other parents; it is not silently reduced to a kernel
from a state latent to an observation.

Fix structural data $X$ and define the retained parent structural datum $X_A=\chi_A(X)$. Both stay
outside the random coarse channel. Freeze one parent model-evaluation type:

$$
\operatorname{ev}_A:\mathsf M_A\longrightarrow
\operatorname{Kern}(\boldsymbol\Xi_A,
\mathsf B_A\times\mathsf O_A\times\mathsf H_A),
\qquad m_A\longmapsto K^{X_A}_{A,m_A}.
$$

Thus, at fixed $X_A$, the model point and retained random interface generate at least the parent
belief coordinate, observation, and retained marks. The family is jointly measurable and
normalized. Evaluation need not be injective. If one quotients presentations by
$m\sim m'$ exactly when their evaluated kernels agree, standard-Borel, Hausdorff, or smooth
regularity of that quotient is an additional theorem; the default construction retains
presentations.

An agent may be uncertain over, or maintain a population of, generative models. At fixed $(o,X)$,
the definite-model case is $q_i^{m;o,X}=\delta_{m_i}$. A changing human, bacterium, or university model is represented
by a path of model laws and evaluated kernels only after a dynamics is declared.

The distinction is mandatory:

- $q_i^b$ is a law over state-belief variables;
- $q_i^m$ is a law over model coordinates or presentations;
- $m_i$ is a sample model coordinate and $K^X_{i,m_i}$ is its normalized evaluated kernel; and
- $\mathbb P_I(Do,DY\mid X)$ is the fixed full generative law, assembled without reading
  $\mathbb Q$ or $\boldsymbol\Pi$.

At a smooth statistical-manifold tier, differentiability in quadratic mean, common domination,
score integrability, Fisher nondegeneracy, and quotient regularity are separate hypotheses. None
follows from the standard-Borel construction. Gaussian families are optional computational
subclasses only.

## Phase 1: full fine probabilistic datum

Fix a finite active agent set $I$ at $r_*$ and fixed structural data $X$. Let $\mathsf Y_I$ contain
all fine random variables required by the declared theory, including state-belief samples $k_i$,
model samples $m_i$, dependence data, and exact-closure records. Supply

$$
\mathbb P_I(do,dY\mid X),\qquad
\boldsymbol\Pi_{I,o,X}(dY),\qquad
\mathbb Q_{I,o,X}(dY)\ll\boldsymbol\Pi_{I,o,X}(dY),
$$

where the posterior is a selected regular conditional of the fixed generative law at an admitted
$o$, and the recognition law is correlated. The displayed local pairs $(q_i^b,q_i^m)$ are declared
marginals of $\mathbb Q_{I,o,X}$. Marginals do not determine the joint lift.

The fine datum must pass four checks: normalization and recognition independence of generation;
posterior derivation from $\mathbb P_I(\cdot\mid X)$; recovery of the displayed sections with
support/integrability hypotheses; and explicit structural $X$, observation $o$, and evidence event.

## Phase 1: one common pointwise coarse channel

Declare one normalized Markov channel

$$
C_A:\mathsf Y_I\rightsquigarrow
\mathsf Z_A,
\qquad
\mathsf Z_A=\mathsf B_A\times\mathsf M_A\times\boldsymbol\Xi_A\times\mathsf H_A,
$$

fixed by structural coarse data and independent of recognition, posterior, and realized observation.
It acts only on random fine variables. Structural $X$ remains fixed and
$X_A=\chi_A(X)$ remains outside $C_A$. The observation space is unchanged in this phase, so
$\mathsf O_A=\mathsf O$ and $o_A=o$.

Apply the same channel to generation, posterior, and recognition:

$$
\begin{aligned}
\mathbb P_A(do,dz\mid X)
&=\int_{\mathsf Y_I}C_A(Y,dz)\,\mathbb P_I(do,dY\mid X),\\
\boldsymbol\Pi_{A,o,X}&=\boldsymbol\Pi_{I,o,X}C_A,\\
\mathbb Q_{A,o,X}&=\mathbb Q_{I,o,X}C_A.
\end{aligned}
$$

This triple is the full pointwise probabilistic datum for the candidate parent. It is not yet a
pair of local sections over $\mathcal U_A$, a full geometric meta-agent, or an autonomous dynamics.
With $(o,X)$ fixed in this subsection, its recognition marginals are

$$
q_A^b=(\operatorname{pr}_b)_\#\mathbb Q_{A,o,X},
\qquad
q_A^m=(\operatorname{pr}_m)_\#\mathbb Q_{A,o,X}.
$$

The model coordinate earns its generative interpretation only if one jointly measurable regular
conditional version satisfies

$$
\mathbb P_A(db_A,do,dh_A\mid \xi_A,m_A,X)
=K^{X_A}_{A,m_A}(\xi_A;db_A,do,dh_A)
$$

for almost every $(\xi_A,m_A)$ under the corresponding marginal of $\mathbb P_A(\cdot\mid X)$.
This compatibility concerns $C_A$, the fine generative law, and the predeclared evaluation family;
it does not follow from a recognition marginal.

The prior marginals $p_A^b,p_A^m$ are projections of the selected parent generative conditional,
and $\boldsymbol\Pi_{A,o,X}^b,\boldsymbol\Pi_{A,o,X}^m$ are projections of the parent posterior.
They are not aliases for $q_A^b,q_A^m$ and do not replace a correlated full law. Independent parent
channels define another approximation problem with an explicit mismatch residual.

## Phase 2: lossy exact VFE closure

Let the observation evidence be finite and unchanged by $C_A$. Form the two bridge lifts by
attaching the same channel to $\mathbb Q_{I,o,X}$ and $\boldsymbol\Pi_{I,o,X}$. Standard-Borel
disintegration must yield

$$
\mathcal F_I(o,X;\mathbb Q_{I,o,X})
=\mathcal F_A(o,X;\mathbb Q_{A,o,X})+\Delta_A(o,X),
$$

where

$$
\Delta_A(o,X)=
\int_{\mathsf Z_A}
\operatorname{KL}\!\left(
\widehat{\mathbb Q}_{I,o,X}(dy\mid z)
\middle\Vert
\widehat{\boldsymbol\Pi}_{I,o,X}(dy\mid z)
\right)\mathbb Q_{A,o,X}(dz)\geq0.
$$

This is an exact identity for a generally lossy coarse-graining. The defect measures inference
information discarded inside the fibers of $C_A$; it is not a numerical error. For finite fine KL,
$\Delta_A=0$ exactly when the discarded conditional recognition and posterior laws agree almost
surely. The equivalent common-recovery-kernel criterion may be used when its hypotheses hold.

Loss is compatible with meta-agency. A university-scale meta-agent need not retain the fine beliefs
and models of every student and faculty member. What must be retained is whatever boundary or
interface information the declared parent law uses. The theorem must report $\Delta_A$ rather than
equating lossy coarse-graining with exact microscopic reconstruction.

## Phase 2: holonomy alternatives

The released pointwise RG certificate already supplies separate belief/model marginal stabilization
$h_\#q_A^x=q_A^x$ on positive-event components. That statement is inherited here; it is not a new
full-parent criterion, and it is insufficient for a correlated datum.

A holonomy-blind parent must declare a joint holonomy action on the complete fine and parent random
spaces, prove equivariance of $C_A$ under those actions, and prove compatibility of the full
generative, posterior, and recognition laws and of $\operatorname{ev}_A$. In kernel notation, the
channel obligation has the form

$$
C_A(g\cdot Y,g\cdot D)=C_A(Y,D)
$$

for every admitted joint holonomy element $g$ and measurable parent event $D$, with the exact fine
and parent actions stated. The corresponding full-law invariance or covariance must hold for
$\mathbb P_A(\cdot\mid X)$, $\boldsymbol\Pi_{A,o,X}$, and $\mathbb Q_{A,o,X}$; separate marginal
invariance is only a projection consequence. Full-frame triviality is sufficient but not necessary.

Alternatively, retain component roots, raw root-framed holonomy, and boundary records in
$\mathsf H_A$. Then the parent does not erase path information and makes no holonomy-blind
invariance claim. Holonomy compatibility and membership selection remain separate obligations.

## Phase 2: dynamic closure boundary

Only after a fine vector field or Markov evolution is declared may the pointwise parent be called a
dynamical meta-agent. For a differentiable fine flow $\dot y=V_t(y)$, a differentiable moving
coarse map $c_t$, and a candidate parent flow $\overline V_t$, define the semiconjugacy defect

$$
\delta_t
=\partial_tc_t+Dc_t\,V_t-\overline V_t\circ c_t.
$$

Exact trajectory semiconjugacy on the declared state class is $\delta_t=0$. Autonomous closure
additionally requires declared autonomous fine and parent vector fields, a fixed coarse map (or a
correctly typed autonomous extension that incorporates the map's evolution), and well-posed fine
and parent flows on their stated existence domains. Approximate closure requires a declared norm,
state class, time interval, and error bound. For stochastic or kernel dynamics, replace this
display by the proper generator, lumpability, or path-law condition rather than treating a Markov
channel as a differentiable map.

The $\partial_tc_t$ term is mandatory for adaptive memberships or a changing coarse map. The
parameter $t$ acquires no physical or ontological interpretation merely from this equation.

## Downstream Phase 3: comparison theorem

The comparison theorem begins only after $\mathbb P_A$, $\mathbb Q_{A,o,X}$,
$\boldsymbol\Pi_{A,o,X}$, and their channel are fixed. It must state one typed comparison category
and prove what changes when the category is enlarged or reduced. At minimum it distinguishes:

- preservation versus erasure of the intervention target;
- fixed input and output boundary roles in $R\to E\to O$;
- forward orientation versus time reversal;
- one protocol-independent typed relabeling versus protocol-dependent relabelings; and
- retained response experiments versus raw latent or DAG presentations.

Interventions are analyst-declared modifications used to ask whether two generative presentations
make different response predictions. They are not primitive actions performed by the agents and
are not evidence that the underlying system contains a controller. The theorem may compare
operational semantics; it may not infer a unique latent DAG or microscopic physics.

## Downstream Phase 4: extension across an overlap patch

For $r\in\mathcal U_A$, the weights, transports, agent laws, model evaluations, and coarse channel
may all vary with $r$. A patchwise meta-agent requires a jointly measurable or suitably smooth
family $r\mapsto C_{A,r}$ and parent laws that glue under the declared bundle transitions.

The patchwise project must address:

1. compatibility of local pointwise channels on overlaps of subpatches;
2. cocycle and gauge-equivariance conditions for both belief and model bundles;
3. changing positive-support graphs, active agent sets, and connected components;
4. stabilizer or rank jumps, which may force a stratified rather than smooth parent bundle;
5. normalized soft multiple membership versus literal replicated covers with multiplicity;
6. measurable or smooth selection of roots, forests, and retained holonomy data; and
7. a patchwise VFE defect whose integrability over the base is proved rather than assumed.

No pointwise theorem automatically supplies this gluing. Only after compatible parent fiber values glue to local parent sections may the construction be called a geometric meta-agent. The notation $\mathcal U_A$ makes the
dependency visible and prevents collision with intervention inputs or retained parameters.

## Downstream Phase 5: participatory nonequilibrium and emergent agency

This phase remains **OPEN/TODO** until the full static meta-agent is established. Its starting
hypothesis is intentionally austere: no primitive action, plan, controller, or policy variable is
required in the ontology; sub-agents, agents, and meta-agents may all be states of one coupled
variational dynamics. Whether agency emerges from that dynamics is a theorem target, not a premise.

A closed gradient flow of a fixed coercive objective commonly relaxes toward its critical set and
does not by itself establish sustained nonequilibrium behavior. Candidate mechanisms that must be
typed and tested separately include:

- reciprocal fine-to-coarse and coarse-to-fine coupling;
- an adaptive coarse channel or dynamically selected memberships;
- open-system boundary flux and environmental exchange;
- antisymmetric, Hamiltonian, kinetic, or other non-gradient sectors;
- stochastic forcing, delay, or retained memory; and
- Wheelerian participation in which the emergent parent changes the conditions under which its
  constituents update.

Upward aggregation and downward constraint must descend from one tower action, a constrained
reduction, or another proved composition rule. Adding independent VFEs at several scales risks
double-counting the same evidence or interaction factor.

The later project must define graded operational criteria for emergent agency, such as persistent
boundary maintenance, endogenous state-dependent influence, cross-scale closure, and robustness to
admitted perturbations. Those criteria may be probed counterfactually, but the probes are not
thereby ontic control variables.

## Rejected shortcuts

1. **Two parent marginals are the meta-agent.** Rejected because they omit dependence, the
   generative joint, posterior, and exact VFE object.
2. **Choose separate coarse maps for recognition and generation.** Rejected for the exact theorem;
   it destroys the common-channel chain rule unless an explicit mismatch term is added.
3. **Let the parent generative kernel read the recognition law.** Rejected by the fixed-joint
   typing prohibition.
4. **Define the model fiber as a Gaussian parameter vector.** Rejected as an ambient definition;
   it is only one computational realization of a general model-law and evaluation architecture.
5. **Use trivial holonomy as the clustering rule.** Rejected because it is neither sufficient for
   belief agreement nor necessary for state stabilization, and it does not select a partition.
6. **Interpret information loss as failed coarse-graining.** Rejected; the conditional-KL defect
   is the exact price of discarded microscopic inference information.
7. **Add independent fine and coarse VFEs to obtain participation.** Rejected absent a composition
   theorem because it can double-count evidence and factors.
8. **Start with the full overlap region.** Deferred until the pointwise law and channel types are
   closed; otherwise gluing multiplies unresolved pointwise ambiguities.

## Deliverables and verification gates

The implementation phase must produce:

1. a canonical symbol registry plus a machine-checkable collision report, with legacy aliases and
   immutable-evidence exclusions;
2. a release-validated derivation package under
   docs/derivations/2026-08-15-full-pointwise-meta-agent/;
3. direct proofs of model evaluation typing, common-channel full-law construction, parent posterior
   identity, derived-marginal relations, parent evaluation compatibility, and the exact
   conditional-KL defect;
4. counterexamples showing that marginals do not determine the full parent, independent channels
   do not inherit the exact VFE identity, and holonomy alone does not select the cluster;
5. an explicit finite non-Gaussian witness as the primary executable example, with a Gaussian
   realization labeled optional and computational;
6. independent probability and kernel, information-geometric, gauge and holonomy, and dynamics
   reviews;
7. an adversarial scope review that checks every **ESTABLISHED**, **CONDITIONAL**, **OPEN**, and
   interpretive statement;
8. scoped integration into Theory/SPEC.md, Theory/appendix_notation.tex, the relevant theorem
   chapters, solid_RG_theory.md, overview.md, docs/STATUS.md, and the August 12 worklog only after
   release validation; and
9. a separate roadmap for the comparison, overlap-patch, and participatory-nonequilibrium phases,
   none of which may inherit **ESTABLISHED** from the pointwise construction.

Mathematical claims close only through derivation or proof. Finite computations may corroborate a
witness but do not prove the general theorem. The release must bind its claim ledger to the exact
artifact revision, inputs, and validator output before any central status is promoted.

## Claim boundary

This phase may establish one full, normalized, generally lossy pointwise probabilistic datum obtained by a
common recognition-independent channel from a declared fine generative joint, posterior, and
correlated recognition law. It may establish the parent model-evaluation compatibility, derived
parent marginals, exact VFE chain rule and conditional-information defect, and sharply typed
holonomy alternatives.

It may not claim that this pointwise datum is already a pair of local sections or a full geometric meta-agent; that marginal agreement canonically determines the full joint; that holonomy
canonically selects membership; that the parent reconstructs all microscopic information; that a
Gaussian family is the general theory; that a static pointwise construction yields an autonomous
agent; that gradient descent alone produces sustained nonequilibrium behavior; that analyst
interventions are ontic actions; that a unique latent DAG or microscopic physics is recovered; or
that the construction glues across $\mathcal U_A$ without the later patchwise theorem.
