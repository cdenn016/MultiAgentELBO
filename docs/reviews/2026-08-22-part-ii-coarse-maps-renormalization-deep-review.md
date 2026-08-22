# Deep review of Part II: General Coarse Maps and Renormalization

**Review date:** 2026-08-22
**Reviewed repository:** `C:\Users\chris and christine\Desktop\MultiAgentELBO`
**Reviewed commit:** `fb17e3aef9ba2d575734558eb3c493930bc8c71d`
**Primary laboratory target:** simultaneous renormalization of a decorated directed agent-overlap network above one fixed base point $c_*$

## Executive verdict

Part II contains the ingredients for an exact fixed-context theory, but it does
not yet assemble them into one closed renormalization map for the object the
laboratory is trying to build. The network topology and the beliefs, model
presentations, gauge frames, transports, attention-event laws, interaction
records, and memory attached to that topology are not separate RG problems.
They are coupled coordinates of one decorated network above $c_*$, and an
exact coarse step must push their joint law through one
recognition-independent structural channel.

The extension from one $c_*$ to a family over
$(c_*-\mathrm{d}c,c_*+\mathrm{d}c)$ is a later geometric problem. It requires
sections, descent, gluing, changing active-agent sets, vertical bundle maps,
and compatibility with horizontal transport. It should not be used as the
definition of the current fixed-context laboratory, and the fixed-context
laboratory does not establish it.

The strongest existing foundation is `07b_agent_network_rg.tex`. It correctly
states that general exact closure requires induced hyperedges, marked
attention events, full root-framed holonomy data, and path-space memory, and
that a pairwise memoryless graph with one averaged link is a truncation. The
main defects are concentrated in the shorter synthesis chapter
`07c_full_graph_meta_agent_vfe.tex`, plus one status overclaim at the end of
`07b`. In particular, the `ESTABLISHED` statement that genuine overlapping
membership can be handled by replacing indicator sums with expectations is
false as written: it does not preserve normalization.

The current `rg_v2` laboratory is narrower than the desired decorated-network
RG. It implements a static, fixed-context, finite probabilistic DAG with exact
belief/model laws, evaluators, and a dense retained interaction record. It does
not implement an overlap or attention graph, gauge frames or holonomy,
multiscale composition, autonomous dynamics, or sections over the base. Its
design document states these exclusions honestly, so they are program gaps,
not hidden code defects.

## Scope, evidence, and review method

Part II is included by `Theory/main.tex` in this order:

1. `Theory/06_general_coarsegraining.tex`
2. `Theory/07_general_renormalization.tex`
3. `Theory/07b_agent_network_rg.tex`
4. `Theory/07c_full_graph_meta_agent_vfe.tex`

The review read those files together with the governing `Theory/SPEC.md`, the
claim ledger and notation appendix, the current recursive-laboratory design,
the active launcher/config path, and the implementation contracts. Independent
passes covered variational/RG closure, gauge and holonomy typing, base-section
geometry, and active laboratory reachability. A separate adversarial pass then
tried to refute every proposed high-severity issue. The dispositions below
record the narrowed results of that pass rather than agreement by vote.

The source binding is:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `Theory/06_general_coarsegraining.tex` | 35,010 | `FA10620D2A1D0E51B5A50B88D0A7434AFCDE6A0112AF062E74FED586E97D7166` |
| `Theory/07_general_renormalization.tex` | 53,716 | `CEDA98A49F4122DE39D70F784288860AB727ABFA217A92B1230591E6CE76BCAD` |
| `Theory/07b_agent_network_rg.tex` | 157,534 | `67F9803A064C5F9E61299C18CDE2C67DB8CCDF3389E52F827712DE28977EEEFA` |
| `Theory/07c_full_graph_meta_agent_vfe.tex` | 16,949 | `6A4F9806F1AE6EB6DEDBAD171E8FD8466F39F42E04D6A5149DC97344F64BB723` |
| `Theory/SPEC.md` | 73,499 | `853B0784833F93777BA4FF4FCAC086FC1C8794E09322762916AF4248B9FABC2E` |
| `rg_v2/coarse_agent.py` | 72,987 | `0C086E9C7890BB9943A83AA5B251AF62CE224741631C49FB48CE87833E158179` |
| `rg_v2/contracts.py` | 19,719 | `3B67E9DADA9DD67C4BE8A8FF62DE81D8DA1CAC42B2B7A5E7DF1BDFFF4A01AE6B` |
| `docs/superpowers/specs/2026-08-21-rg-v2-recursive-coarse-agent-closure-design.md` | 38,760 | `9210805E668BFDA409A2231ABB3FBDC8E26EB82E62AB50C19E691F1F6CF5F17A` |

The tracked worktree was clean before this report. Four preexisting untracked
PDFs were present and were not touched.

This review does not assign formal verification-ledger closure. The repository
ledger at `.verification/ledger.json` is a triage ledger bound to commit
`f9ce06a5782dd5fd0392761cdd1872a983429326`, not the reviewed revision. The
`Theory/verification/current-results.json` artifact is bound to the different
source root `manuscripts/gauge_vfe_rg`; it records a 41,612-byte `07b` and does
not include `07c`, whereas the reviewed `Theory/07b_agent_network_rg.tex` is
157,534 bytes. Its 29 passing checks therefore do not verify this Part II.
No code tests or TeX build were run because this was a read-only source review.

## The object that should renormalize at fixed $c_*$

The three levels in the review request separate into two current components and
one later extension. A fourth axis, RG depth, must also be kept distinct from
the base coordinate.

| Axis | Mathematical object | Relation to the current laboratory |
|---|---|---|
| Agent network at $c_*$ | vertices, directed incidence, overlap or assignment data, edge and hyperedge event structure | Part of the current target |
| Agent data at $c_*$ | belief and model full laws, evaluators, frames, transports, cross-channel maps, holonomy, attention marks, retained records, memory | Part of the same current target |
| Base coordinate $c$ | a family $c\mapsto\mathcal N_c$, local sections, active-set changes, transition and gluing data | Later geometric extension |
| RG depth $\ell$ | a composable family of coarse channels between retained state spaces | Required even at one fixed $c_*$; not physical time |

The fixed-context target should be declared as one decorated state, for
example

\[
\mathcal N_{\ell,c_*}
=
\left(
V_\ell,E_\ell,\mathcal H_\ell;
\{Z_i\}_{i\in V_\ell};
R_\ell,\eta_\ell^b,\eta_\ell^m;
\{\Theta_e^b,\Theta_e^m\};
\{H_I^b,H_I^m,V_e^b,V_e^m\};
\mathcal R_\ell,\mathcal M_\ell
\right).
\]

Here $Z_i$ is the full probabilistic agent datum rather than a tuple of
marginals; $R_\ell$ is a hard partition or a normalized assignment kernel;
$\eta^b,\eta^m$ are joint marked receiver-source event laws rather than only
row-normalized conditionals; $H_I^x,V_e^x$ are root-framed holonomy and
dressed boundary data; $\mathcal R_\ell$ contains induced interaction
records/hyperedges; and $\mathcal M_\ell$ contains whatever path memory is
needed for exact dynamic closure. The exact state can be larger than this, but
it cannot generally be smaller in each of these directions while retaining the
corresponding claim of exact closure.

One normalized, recognition-independent Markov kernel should then act on this
augmented state:

\[
C^{c_*}_{\ell+1\leftarrow\ell}:
\mathsf Y_{\ell,c_*}\rightsquigarrow
\mathsf Y_{\ell+1,c_*}.
\]

If membership is latent, $R_\ell$ belongs to the augmented fine state on
which this channel acts. The same structural channel must push all three law
families,

\[
P_{\ell+1}=P_\ell C^{c_*}_{\ell+1\leftarrow\ell},
\qquad
\Pi_{\ell+1}=\Pi_\ell C^{c_*}_{\ell+1\leftarrow\ell},
\qquad
Q_{\ell+1}=Q_\ell C^{c_*}_{\ell+1\leftarrow\ell}.
\]

That is the precise sense in which the network, beliefs, models, frames, and
directed interactions renormalize together. They need not use the same
coordinate formula: belief and model data live in distinct associated bundles
and use channel-specific representations. They must, however, be outputs of
one typed structural coarse step if the common-channel VFE identity is being
claimed.

The exact category is therefore a category of normalized decorated-network
laws and Markov kernels, not ordinary directed graphs. An ordinary pairwise
graph is recovered only by a declared projection. The resulting conditional KL
or reconstruction residual measures what that projection discards.

## Findings

| ID | Severity | Finding | Adversarial disposition |
|---|---|---|---|
| P2-1 | High | Genuine overlapping membership in `07c` does not preserve edge-event normalization | Upheld for overlap; rejected for stochastic hard partitions |
| P2-2 | High | `07c` holonomy stabilization and edge dressing are not typed in the parent frame | Upheld |
| P2-3 | High | The recursively declared graph state omits receiver occupancy or the joint event law needed by its own next-scale formula | Upheld |
| P2-4 | High | The adaptive graph construction in `07c` is recognition-side only and does not instantiate the common $P/\Pi/Q$ channel | Upheld only for `07c`; rejected as a criticism of `07b` |
| P2-5 | High | `07b` overstates which hypotheses of its conditional closure theorem are exhibited | Upheld; theorem itself remains valid conditionally |
| P2-6 | Medium | The pointwise parent theorem is a valid abstract probability theorem, but not yet a typed fixed-fiber theorem over $c_*$ | Upheld as an interpretation/typing gap |
| P2-7 | Medium | Normalization of the downward kernel does not imply bidirectionally coupled optimization | Upheld by an exact counterexample |
| P2-8 | Low | Base-point and coarse-map notation obscures the separation between $c$ and $\ell$ | Upheld editorially |

### P2-1: overlapping membership duplicates probability mass

**Location:** `Theory/07c_full_graph_meta_agent_vfe.tex:281-296`, especially
the sentence after Equation `full-graph-edge-pushforward`.

The deterministic formula

\[
\eta^{x,s+1}_{IJ}
=\sum_{i\in I}\sum_{j\in J}\eta^{x,s}_{ij}
\]

is correct when the blocks form a partition. It also remains normalized when
one first samples a hard partition and then averages the resulting pushforward
over a distribution of hard partitions. The problem is the additional claim
that *overlapping* membership can be handled by replacing the indicators with
expectations under $Q_R^s$.

Let $n_i$ be the number of coarse blocks that contain fine vertex $i$. If
ordinary membership indicators are used, then

\[
\sum_{I,J}\eta^c_{IJ}
=\sum_{i,j}\eta_{ij}n_i n_j.
\]

For one fine directed event $(i,j)$ with $\eta_{ij}=1$, let both endpoints
belong fully to both coarse blocks $A$ and $B$. The proposed formula gives

\[
\eta^c_{AA}=\eta^c_{AB}=\eta^c_{BA}=\eta^c_{BB}=1,
\]

so the coarse mass is four. Concentrating $Q_R^s$ on that overlap relation
does not repair the failure. The `ESTABLISHED` status is therefore too strong
for the overlapping case.

The exact repair is to use a normalized assignment kernel. For conditionally
independent endpoint assignments, introduce

\[
m_\ell(I\mid i,R)\ge 0,
\qquad
\sum_I m_\ell(I\mid i,R)=1,
\]

and define

\[
\eta^{c}_{IJ}
=\sum_{i,j}\eta_{ij}
\mathbb E_R
\left[m_\ell(I\mid i,R)m_\ell(J\mid j,R)\right].
\]

If the two endpoint assignments are correlated, the product must be replaced
by a normalized joint assignment kernel
$M_\ell(I,J\mid i,j,R)$. Composition then requires a
Chapman-Kolmogorov law for the assignment kernels and simultaneous retention of
the marks needed by the next step. If “overlap” instead means literal
replication with unit weight in every containing block, the result is a finite
measure with multiplied mass, not the asserted pushed probability law; it must
be given different semantics and an explicit renormalization.

### P2-2: the `07c` holonomy and dressing formulas lack a parent-frame type

**Location:** `Theory/07c_full_graph_meta_agent_vfe.tex:232-261`, compared
with `Theory/02_geometry.tex:602-608` and
`Theory/07b_agent_network_rg.tex:1810-1854`.

A cycle word $H_C^x$ is based at a microscopic vertex. Under a gauge change it
is conjugated in that vertex's frame. Equation
`full-graph-holonomy-stabilization` applies this object directly to a parent law
$Q_I^x$, but `07c` never identifies the cycle base with the parent root and
never transports the holonomy into the parent frame. This is a type error, not
only an omitted convention.

For example, take

\[
H=\begin{pmatrix}0&-1\\1&0\end{pmatrix},
\qquad
Q_I=\mathcal N(0,I),
\]

so $H_\#Q_I=Q_I$. Under the microscopic frame change
$a=\operatorname{diag}(2,1)$, the same holonomy is represented by

\[
H'=a^{-1}Ha
=\begin{pmatrix}0&-1/2\\2&0\end{pmatrix}.
\]

Applying $H'$ directly to the unchanged parent-coordinate law produces
covariance $\operatorname{diag}(1/4,4)$, so the displayed stabilization
statement is not frame invariant without the missing parent-frame dressing.

The next formula introduces $\Omega^x_{Ii}$ and $\Omega^x_{jJ}$, but neither
symbol is defined in the active Theory tree and no endpoint transformation law
is supplied. A notation match in the excluded `PIFB2.tex` cannot type an active
Part II formula. The correct construction is already present in `07b`: choose a
root $r_I$, use tree transports $\tau^x_{I\leftarrow i}$, retain a based
holonomy representation
$H_I^x:\pi_1(\Gamma_I,r_I)\to G$, and define

\[
V_e^x
=\tau^x_{I\leftarrow i}\Theta_e^x
(\tau^x_{J\leftarrow j})^{-1}.
\]

`07c` should either reuse those objects and their endpoint gauge laws or remove
its duplicate formulas. It should not overload $\Omega$ for a microscopic
link, an internal path product, and a cross-scale dressing leg.

### P2-3: the declared recursive graph state loses the receiver law

**Location:** `Theory/07c_full_graph_meta_agent_vfe.tex:61-67,150-168,281-296`.

The scale datum declares

\[
G_s=(\beta^s,\gamma^s,\Omega^{b,s},\Omega^{m,s}),
\]

while the hierarchical law contains only $Z_s,G_s,R_s$. Receiver
occupancies $\alpha^b,\alpha^m$ appear later as “external,” and the actual
joint event laws are $\eta^b=\alpha^b\beta$ and
$\eta^m=\alpha^m\gamma$. Yet the next-scale formula requires $\eta^s$ in
order to construct $\eta^{s+1}$, $\alpha^{s+1}$, and the next conditional
rows. The declared state is therefore not closed under its own recursive map.

The omission cannot be repaired from $\beta$ alone. Let two receivers have
rows $\beta_1=(1,0)$ and $\beta_2=(0,1)$, and merge them into one parent
receiver. If their occupancies are $(p,1-p)$, the parent row is
$(p,1-p)$. Every $p\in[0,1]$ gives the same retained fine $\beta$ but a
different parent row. This is the obstruction already stated correctly in
`Theory/07b_agent_network_rg.tex:1969-1997` and
`Theory/appendix_notation.tex:392-396`.

The minimal repair is to make $\eta^{b,s}$ and $\eta^{m,s}$ part of $G_s$,
or retain each $\alpha^{x,s}$ together with its conditional row. Retaining
$\eta$ is cleaner because it is the normalized object that pushes linearly;
$\alpha$ and $\beta$ are then recovered by marginalization and
disintegration on positive occupancy.

### P2-4: `07c` does not push the adaptive graph through the common law triad

**Location:** `Theory/07c_full_graph_meta_agent_vfe.tex:69-101,281-296`, in
contrast with `Theory/07b_agent_network_rg.tex:16-31,76-116,1969-2035`.

An initial criticism that Part II lacked a common augmented-channel treatment
was too broad. `07b` defines one recognition-independent $C$ and pushes the
generative joint, selected posterior, and recognition law through it. It also
contains a normalized augmented receiver-source-label construction and places
$\eta$ in the fine and coarse law tuples. Those parts are sound.

The narrower defect survives in `07c`. Its stochastic-membership sentence
constructs coarse attention by expectation under $Q_R^s$ alone. That can
define a recognition-side statistic, but it does not display the corresponding
generative and posterior graph-event pushforwards, and it does not establish
that one recognition-independent map acts on all three. This matters whenever
the graph and partition are part of the latent state and the exact VFE
chain rule is invoked.

The repair is to include $(R_s,\eta_s,\text{marks})$ in the augmented latent
space, define one normalized structural channel on that space, and apply it to
$\mathbb P_\theta$, $\boldsymbol\Pi_{\theta,o,X}$, and
$\mathbb Q_\phi$. Their distributions of $R_s$ may differ; the structural
map conditioned on a realized $R_s$ must be the same. `07c` should refer back
to the `07b` common-channel theorem rather than presenting a recognition-only
expectation as the full exact step.

### P2-5: the closure theorem assumes an open equivariant-version problem

**Location:** `Theory/06_general_coarsegraining.tex:520-528` and
`Theory/07b_agent_network_rg.tex:3053-3104`.

The complete finite law-level gauge-VFE theorem in `07b` is a valid conditional
theorem. One explicit premise is the existence of globally gauge-equivariant,
jointly measurable versions of every disintegration used for its bridge
kernels, and the proof correctly calls this a supplied hypothesis. The problem
is the subsequent assertion that every premise except rescaling-kernel
composition has been exhibited.

`06_general_coarsegraining.tex:526-528` says the opposite: an equivariant
conditional version does not follow automatically from Bayes recovery and is
an additional hypothesis or theorem, especially for noncompact groups. It is
labeled `OPEN`. No construction theorem elsewhere in the active Theory tree
discharges it.

The closure theorem should remain `ESTABLISHED` as an implication from its
listed hypotheses. The instantiation paragraph should say that both
scale-compatible rescaling kernels and globally equivariant jointly measurable
conditional versions remain supplied hypotheses. Alternatively, Part II must
add a theorem under explicit action/properness/compactness conditions that
constructs the required versions. As written, the theorem is sound but the
claim of an exhibited exact instance is overstated.

### P2-6: the pointwise theorem is not yet a fixed-fiber theorem

**Location:** `Theory/07b_agent_network_rg.tex:76-125` and
`Theory/SPEC.md:208-243,833-868`.

The theorem fixes $r_*\in\mathcal U_A$, then defines abstract standard-Borel
spaces $\mathsf Y_I,\mathsf Z_A$ and a channel
$C_A:\mathsf Y_I\rightsquigarrow\mathsf Z_A$. The fixed point does no work in
the types or proof. No child section is evaluated at $r_*$, no source or
target is identified as a fiber above $r_*$, and the channel is not declared
vertical over the identity of the base point.

The probability theorem remains valid because it does not need base geometry.
What is unproved is the stronger interpretation that it constructs a
meta-agent *above the same base point*. For that reading, the manuscript should
either define evaluated spaces
$\mathsf Y_{I,c_*},\mathsf Z_{A,c_*}$ and a vertical channel
$C_{A,c_*}$, or label the current statement explicitly as an abstract
law-level theorem and add a separate fiber-realization proposition. This is
also why the theorem does not imply gluing over $\mathcal U_A$, a boundary the
governing specification already records as open.

### P2-7: the downward kernel need not couple parent and child optimization

**Location:** `Theory/07c_full_graph_meta_agent_vfe.tex:82-87,301-326`.

The only formal condition on $K_\downarrow^s$ is that it is a normalized
measurable kernel. Such a kernel may ignore its parent argument. Let parent and
child variables be binary, take a uniform parent prior, and choose

\[
K_\downarrow(z_s\mid z_{s+1})=\frac12,
\qquad
Q_S=\operatorname{Bern}(a),
\qquad
Q_s(\cdot\mid z_{s+1})=\operatorname{Bern}(b).
\]

Up to an observation constant, the displayed objective becomes

\[
\mathcal F
=\operatorname{KL}(\operatorname{Bern}(a)\Vert\operatorname{Bern}(1/2))
+\operatorname{KL}(\operatorname{Bern}(b)\Vert\operatorname{Bern}(1/2)),
\]

whose mixed derivative is zero. The parent and child optimizations decouple.
Lines 321-326 should say that bidirectional coupling occurs when the downward
kernel depends nontrivially on the parent coordinate and the chosen
parameterization transmits that dependence to the cross-scale VFE. If a
universal coupling claim is intended, those sensitivity hypotheses and a
nonzero cross-derivative result must be proved.

### P2-8: the base coordinate and RG depth need a stable notation contract

Part II fixes $r_*$ in the pointwise theorem, the laboratory request and the
closing target of `07c` use $c_*$, and the general geometric chapters use
coarse maps of the base while `07c` postpones its fixed-context scope until its
closing paragraph. This invites a reader to identify a change of base point
with a change of scale.

Use $c_*$ consistently for the fixed base point, $U\ni c_*$ for a base
neighborhood, $f_\ell:C_\ell\to C_{\ell+1}$ for an actual base coarse map,
and $\ell$ only for RG depth. Declare at the start of `07b` and `07c` whether
all graph variables are evaluated in the fiber above one fixed $c_*$.

## What Part II already gets right

The law-level coarse VFE theorem in `07b:16-73` is the correct backbone. It
pushes $(P,\Pi,Q)$ through one recognition-independent channel, preserves the
observation evidence, and identifies the VFE change with discarded conditional
information. It also states the exclusions: fitted coarse generative models,
recognition-dependent channels, and simultaneous observation coarsening are
not silently covered.

The opening of `07b:4-11` gives the correct general closure boundary. Exact
coarse closure of an interacting directed network generally leaves the class
of pairwise memoryless graphs. Induced hyperedges, marked edge events,
root-framed holonomy, dressed boundary generators, and path memory are not
decorative extras; they are the retained variables that make the exact image
closed. A smaller graph family is a truncation whose error must be measured.

The rooted gauge construction in `07b:1810-1854` is substantially better typed
than its compressed restatement in `07c`. It distinguishes belief and model
representations within one principal bundle, bases holonomy at a chosen root,
and gives boundary transports the correct two-endpoint transformation law.

The attention-event construction in `07b:1969-2035` also has the right order:
form the normalized joint receiver-source law $\eta=\alpha\beta$, push
$\eta$, recover $\alpha$ by marginalization, and disintegrate to obtain
$\beta$. It explicitly says that the next scale must retain $\eta^c$, not
$\beta^c$ alone.

`07c` correctly distinguishes its normalized hierarchical VFE from the later
composite potential. Lines 53-56 state that the complete VFE is the normalized
joint-law expression, and lines 225-227 say the composite is not automatically
an evidence bound. That warning should be retained.

The general coarse-map chapters also preserve an important distinction between
pointwise vertical coarse channels and genuine base-space coarse maps. Their
open boundaries around section descent, gluing, and connection compatibility
are consistent with `Theory/SPEC.md:861-868,900-906`. The problem is not that
the theory lacks every distinction; it is that the current Part II order does
not foreground the fixed-$c_*$ decorated-network object that the laboratory
actually targets.

## Current laboratory coverage at the reviewed revision

The active launcher `run_renormalization_v2_recursive_lab.py:15-31` selects
only `lf4_two_parent_recursive_v1`. The fixture and runtime enforce one shared
`context_id`, but that value is a string identifier, not a base point equipped
with a neighborhood, bundle, or connection.

| Desired component | Current source status | Evidence boundary |
|---|---|---|
| Fixed context | Present | All source and coarse specifications share one `context_id`; this is an identifier only |
| Full finite belief/model laws | Present | `rg_v2/contracts.py:79-209`; pushforward and marginals in `rg_v2/coarse_agent.py:1155-1184` |
| Model presentations and evaluators | Present | `rg_v2/contracts.py:102-169`; evaluator construction in `rg_v2/coarse_agent.py:600-679` |
| Directed structure | Partial | `parent_ids` gives a directed generative DAG, not the directed overlap/attention graph |
| Dense interaction-record closure | Present | Record hyperedges in `rg_v2/contracts.py:213-234`; dense construction in `rg_v2/coarse_agent.py:682-708` |
| Sparse/local pairwise closure | Negative control | The obstruction is intentionally detected in `rg_v2/coarse_agent.py:939-982` |
| Receiver-source event law and overlapping assignment | Absent | No $\eta$, normalized membership kernel, overlap domain, adjacency, or attention state |
| Gauge frames, transports, and holonomy | Absent | No executable frame/transport/holonomy field; the generic `max_frame_condition` launcher key has no recursive-path consumer |
| Repeated scale composition | Absent | One fine-to-coarse construction; the runtime loop is over observations, not RG levels |
| Autonomous or physical dynamics | Absent | `CoarseUpdateDatum` is an exact Bayes marginal table, not a time evolution |
| Sections and gluing over $C$ | Absent | No neighborhood, local section, base map, transition function, connection, or first jet |

These are source-level reachability statements, not executed validation. The
design document itself excludes gauge marks, section/gluing data, another
blocking map, a semigroup theorem, and autonomous dynamics. It also identifies
direct-versus-staged composition as the next experiment. The implementation
should retain that sequence rather than claiming that “recursive” already
means multiscale closure.

## Recommended laboratory sequence

The shortest route to the stated fixed-$c_*$ goal is incremental, but every
increment should extend one declared decorated-state contract.

### 1. Close composition for the existing probabilistic state

Run the already planned direct-versus-staged experiment on the current finite
belief/model and dense-record state. Define two nested coarse maps and compare
the direct pushforward with their composition for the generative, posterior,
and recognition laws. This is the first mechanical gate for the scale axis and
should precede additional graph or gauge coordinates.

### 2. Add normalized membership and joint edge-event laws

Introduce a typed hard-partition/assignment-kernel contract and make
$\eta^b,\eta^m$ retained state. Include separate controls for deterministic
hard partitions, randomized hard partitions, normalized soft membership, and
literal unnormalized overlap. Required invariants are total event mass,
$\alpha$ marginal recovery, row normalization on positive occupancy, and
direct-versus-staged equality. The literal-overlap control should fail unless a
new finite-measure semantics is explicitly selected.

### 3. Add the gauge-retained state without averaging it away

For each connected coarse component, retain a root, tree transports, raw
root-framed holonomy, and dressed boundary links for belief and model channels.
Test endpoint covariance under independent frame rechoices, invariance of the
simultaneous root-gauge orbit, and equivalence of compatible tree choices. A
single averaged group element may be added only as a truncation together with
its residual or the conditional distribution it replaces.

### 4. Assemble one common augmented channel

Place node laws, membership, edge events, gauge marks, dense records, and any
needed memory in one fine state. Apply the same structural channel to
$(P,\Pi,Q)$. Check normalization and the exact VFE chain rule before adding a
learned coarse approximation. A learned/fitted coarse generative model is a
second step whose mismatch from the exact pushforward should be reported
separately.

### 5. Treat pairwise graph recovery as a projection experiment

Once the exact dense decorated state exists, project it back to the desired
pairwise directed architecture. Measure the discarded conditional KL,
interaction-record residual, holonomy residual, and memory residual. This
turns “does the graph renormalize?” into a falsifiable closure question: exact
if all residuals vanish, controlled truncation if they are bounded, and not
closed otherwise.

### 6. Extend to a neighborhood only after the pointwise channel composes

The neighborhood theory should begin with a measurable or smooth family
$c\mapsto C^c_{\ell+1\leftarrow\ell}$ of vertical channels. It must specify
how active-agent covers change, how parent labels and fibers glue, how the
channel intertwines transition functions, and whether covariant first jets
commute. A true base map $f_\ell:C_\ell\to C_{\ell+1}$ is a further
operation and should not be inferred from a family of vertical channels.

## Recommended Part II organization

Part II would be easier to use if its logical order matched the laboratory
dependency order.

1. Begin with a roadmap that names the four independent axes: network
   combinatorics, probabilistic/gauge decorations, base coordinate $c$, and
   RG depth $\ell$.
2. Present the universal common-channel probability calculus first: normalized
   Markov kernels, the $P/\Pi/Q$ pushforward, conditional-information defect,
   and composition.
3. Make fixed-$c_*$ decorated agent-network RG the primary finite
   construction. Put node-law, event-law, hyperedge, gauge, and memory closure
   in one state contract.
4. Present the normalized hierarchical graph VFE as a multiscale model built
   from those composable fixed-context channels. Remove or correct the duplicate
   formulas in `07c`.
5. Only then extend pointwise objects to families of sections over a base
   neighborhood, with descent, gluing, and horizontal compatibility stated as
   separate obligations.
6. Reserve genuine base-space RG, continuum limits, beta functions, and
   physical interpretations for the final layer.

If physically reordering the chapters is undesirable, an explicit dependency
diagram and scope declaration at the start of Part II would accomplish most of
the same work. The central statement should be that the current laboratory
lives in one fiber over $c_*$, while its scale index varies inside that fixed
fiber.

## Relation to external RG frameworks

The manuscript is right to treat several outside frameworks as comparison
lenses rather than interchangeable definitions of the present RG object.

Bayesian renormalization studies coarse distinguishability and relevance in a
statistical-model or parameter-space setting. It informs the information-loss
and Fisher-geometric interpretation of a channel, but it does not by itself
supply the directed incidence, marked event laws, or gauge-holonomy state of an
agent network. See [Berman and Klinger, Bayesian Renormalization
(2023)](https://arxiv.org/abs/2305.10491).

Laplacian renormalization uses diffusion or spectral scales of a graph to
identify and aggregate network modes. It is a candidate partition or scale
selector, not an exact pushforward of the complete belief/model/gauge law. See
[Villegas et al., Laplacian Renormalization Group for Heterogeneous Networks
(2022)](https://arxiv.org/abs/2203.07230) and [Gabrielli et al., A Short
Introduction to the Laplacian Renormalization Group
(2024)](https://arxiv.org/abs/2406.02337).

Multiscale network-renormalization models can close a specified random-network
family under a prescribed hierarchy, often through additive hidden variables.
That is genuine model-family closure, but it is not universal closure for the
decorated gauge-VFE state. See [Garuccio et al., Network Renormalization
(2020)](https://arxiv.org/abs/2009.11024).

These comparisons suggest useful selectors and diagnostics. None removes the
need to define the exact retained state and common channel for the current
fixed-$c_*$ laboratory.

## Final assessment

The desired fixed-point program is mathematically coherent if “the network
renormalizes” means that a normalized common channel maps a sufficiently rich
decorated network law to another law of the same enlarged type. It is not
generally coherent if it means that beliefs, models, frames, and a directed
overlap network all collapse back to an ordinary pairwise memoryless graph with
one averaged link and no retained residual. `07b` already states this
obstruction; Part II should make it the organizing principle.

The immediate manuscript corrections are local: repair overlap normalization,
retain $\eta$ or $\alpha$, reuse the rooted gauge objects from `07b`, push the
adaptive graph through the common law triad, weaken the exhibited-premises
claim, qualify bidirectional coupling, and type the pointwise theorem as either
abstract law-level or genuinely vertical over $c_*$. The immediate laboratory
priority remains the already planned direct-versus-staged composition gate,
followed by joint event laws and then gauge-retained state. Sections over $C$
should remain explicitly open until that fixed-context channel is composable.
