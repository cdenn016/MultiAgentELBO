# The rescaling map: design

Status: design, approved in outline 2026-08-17. Not yet implemented.

## What is actually missing

The finite lab can block: it takes a declared partition, eliminates children exactly, and
reads off the theory the parents obey. As of 2026-08-17 that step is measured correctly and
its truncation residual is known, $0.0063$ of the pairwise coupling on the declared
partition. What it cannot do is *iterate*, because the coarse theory is not returned to the
form of the fine one. Without that return there is no map on coupling space, no fixed point,
no linearization, and therefore no way to ask whether the generated many-body coupling is
irrelevant rather than merely small. Every open question in the status report reduces to
this.

A complete renormalization step is a coarse channel followed by an identification that puts
the result back on a common footing with its input. The lab has the first half. This design
supplies the second.

## The standing of Theory/07b

`Theory/07b_agent_network_rg.tex` already contains a section on the RG transformation and
beta functions, and it declares the structure: a blocking ratio $b$, a coarse channel $C_b$,
an identification kernel $I_b$, the composite $K_b = C_b I_b$, and a compatibility law
$K_{b_1 b_2} = K_{b_1} K_{b_2}$ whose failure it explicitly says would make the sequence "a
typed cocycle rather than an autonomous semigroup". It also records that flat connection
data "become a fixed connection only after a self-similar graph identification has been
declared".

This design does **not** treat that text as a specification to implement. The document is
author-derived, is not independently certified, and may be wrong; `docs/STATUS.md` already
records that its exhibited fixed sectors are all trivial. What it supplies is a set of
sharp, checkable claims, and the finite lab is the right instrument for checking them. The
compatibility law in particular is a genuine falsifier: it is stated, it is not exhibited on
any instance, and it can be tested directly once a rescaling map exists. If it fails, that
is a result about the theory, not a bug in the lab.

Accordingly the construction below is built to be able to fail, and the criteria for failure
are fixed in this document before anything is measured.

## Pre-registration discipline

An audit on 2026-08-17 found that the previous scale-related falsifier was withdrawn partly
because its threshold and its measurement direction had both been chosen after the data were
in hand. That is not to be repeated. Every threshold in the "Declared checks" section below
is fixed now, before implementation, with its justification stated. Any later change is an
amendment with a date and a reason, not an edit.

Where a criterion cannot be justified from first principles it is declared as unmotivated
and the corresponding check reports a number rather than a verdict. A check that cannot fail
is not a check.

## The declared self-similar family

A nested-cycle tower. A level-$k$ graph is a directed cycle of $n_k$ blocks; each block is a
level-$(k-1)$ graph; adjacent blocks are joined through designated boundary agents. Write
$C(n_d, \dots, n_1)$ for the tower. The working case is two levels, $m$ outer by $n$ inner,
giving $m \cdot n$ agents and blocking ratio $b = n$.

Cycle sizes are free parameters, not fixed at three. This is load bearing: with a single
ratio the compatibility law can only ever be probed as $b \circ b$, whereas free $m$ and $n$
allow blocking six agents by $b=6$ directly and comparing against $b=2$ followed by $b=3$.
Without that freedom the central claim of the theory under test cannot be tested at all.

Structure carried at every level, unchanged from the current instance: two channels, belief
and model, each a $Z_3$ representation with its own transports; per-agent occupancies; the
attention row configurations; the declared parent law. The state space is nine states per
agent at every level, which matters below.

## The renormalization step

Four stages. Two exist, one is forced, one is new.

**Coarse channel.** The blocking already implemented, with the Bayes kernel
$T(p \mid x_B) \propto P(p)\prod_{a \in B} K(x_a \mid p)$ normalized over parents so that
$\sum_p T(p \mid x_B) = 1$ and the partition function is preserved. This was corrected on
2026-08-17 and is checked against the declared per-edge energy to $3 \times 10^{-15}$.

**Coarse connection.** The transport between adjacent parents is the Wilson line along the
fine path joining their block roots, composed with the dressed boundary generators the
mark-carrying parent already retains. This is not a free choice: gauge covariance of the
coarse theory requires the coarse link to transform as a link under simultaneous frame
changes at the two block roots, and the path-ordered product of fine transports is the only
construction that does. It also closes a defect found in the same audit and deferred at the
time, that blocking discarded the holonomy of every cut loop and so made total curvature a
function of the partition rather than of the connection. Under this construction the
holonomy of each coarse cycle equals the fine holonomy of the region it encloses, which is
an exact identity and is declared as a check below.

**Graph identification.** The coarse graph of an $m$-cycle of blocks is an $m$-cycle. The
identification relabels the $m$ parents as $m$ agents in cyclic order, preserving
orientation and the boundary-agent convention. This is an isomorphism of directed graphs and
carries no freedom once the boundary convention is fixed.

**State identification.** The identity. Parent states and child states already inhabit the
same nine-element space, and the declared parent law has exactly nine entries, so no state
rescaling is available or needed. This is a property of the construction, not a choice, and
it removes what is usually the most delicate part of a real-space rescaling.

The composite maps a declared parameter vector to a declared parameter vector of the same
type, so it iterates.

## Reading the coarse couplings back into the family

The exact coarse theory carries interaction orders above pair order; the declared family
does not. Three routes are computed, one primary and two as controls, and all three are
reported every step.

**Primary: variational projection.** Choose the family parameters minimizing
$\mathrm{KL}\!\left(\pi_{\text{coarse}} \,\|\, \pi_{\text{family}}(\theta)\right)$, where
both sides are the normalized Boltzmann laws of their actions. This is the same operation
the agents perform, so the truncation error and the variational gap are one object rather
than two, and the residual already measured by the closure metric becomes directly
comparable to it. It is not the classical choice; classical real-space RG reads couplings off
by decimation and truncation, and Monte Carlo RG matches correlation functions. Its
justification here is thematic coherence with a variational free energy program plus modern
precedent in information-theoretic renormalization. That precedent is orientation only: no
citation in this section has been checked against a primary source, and none may enter a
manuscript until it has.

**Seed and control: Möbius truncation.** The anchored Möbius decomposition already separates
the coarse action by interaction order. Its pairwise components are the classical
decimation-and-truncation answer. They seed the optimizer, and the difference between the
seed and the converged projection is reported every step. This is the safeguard against the
optimizer inventing structure: an optimizer in a local minimum will look like flow, and the
only way to see that is to keep the deterministic answer alongside it. If the two disagree
by more than the declared tolerance the step is reported as unresolved rather than
averaged.

**Diagnostic: moment matching.** Three declared observables matched exactly: the holonomy of
each cycle, the flow-averaged divergence across each coarse edge, and the receiver
occupancies. Computed only when the first two routes disagree beyond C4, to adjudicate which
has moved.

## Exactness and precision

The lab's arithmetic discipline is that Möbius inversion runs on rationals so that
alternating sums cannot cancel approximately. That discipline is preserved by where the work
is split. The expensive object is the contraction over child states, which is floating point
regardless and runs in float64. The Möbius decomposition runs on the *coarse* action, which
has $9^m$ entries — $729$ for three parents — and stays exact on `Fraction`. Nothing about
moving the contraction to the GPU touches the exact layer.

Reduced precision is not admissible for the contraction. The measured three-body components
are of order $10^{-4}$ against pairwise components of order $10^{-1}$, a ratio near
$10^{-3}$, and bfloat16 carries roughly three decimal digits. float32 is permitted only for
the largest instances and only with the existing parity machinery reporting the float64
disagreement.

## Compute

The repository already has `src/multiagent_elbo/cuda_backend.py`, a side-effect-free
controller for a standalone worker with a versioned protocol, canonical array hashing, dtype
parity diagnostics, and CPU/CUDA backend selection. The contraction goes through that
protocol rather than through a new path, so reproducibility and CPU/GPU parity come from
machinery that already exists and is tested.

Verified on this machine: RTX 5090, torch 2.10.0.dev+cu128, CUDA available, bf16 supported.
Per repository convention, anything importing torch runs under `C:/anaconda/python.exe`;
bare `python` is CPU-only and silently deselects CUDA work.

Dense contraction cost is $9^{N}$ for $N$ agents:

| agents | states | float64 | float32 | verdict |
|---|---|---|---|---|
| 6 | $5.3\times10^{5}$ | 4 MB | 2 MB | trivial |
| 8 | $4.3\times10^{7}$ | 344 MB | 172 MB | comfortable |
| 9 | $3.9\times10^{8}$ | 3.1 GB | 1.6 GB | fits, the $3\times3$ case |
| 10 | $3.5\times10^{9}$ | 27.9 GB | 14 GB | float32 only |
| 11 | $3.1\times10^{10}$ | 251 GB | 126 GB | infeasible dense |

The $3\times3$ working case is comfortable. Iteration does not grow this: the recursion runs
on couplings, not on graph size, so each step costs one block-plus-boundary contraction
however long the flow runs. Depth is therefore not a compute constraint, and transfer-matrix
contraction along cycles is deferred until an instance past ten agents is actually wanted.

## Declared checks

Thresholds fixed before measurement. Checks one through three are exact identities with no
free tolerance beyond arithmetic; four and five are quantitative.

**C1, gauge covariance of the step.** Applying a gauge transformation to the fine model and
then renormalizing must equal renormalizing and then applying the induced coarse gauge
transformation. Criterion: agreement to $10^{-12}$ on the coarse action. Failure refutes the
construction, not the theory.

**C2, holonomy conservation.** The holonomy of each coarse cycle equals the fine holonomy of
the region it encloses, exactly, as group elements. Criterion: exact equality. Failure means
the coarse connection is wrong.

**C3, compatibility.** $K_{b_1 b_2} = K_{b_1} K_{b_2}$ after the declared identifications,
tested on at least one instance admitting two distinct factorizations of the same total
ratio, for example $6 = 6$ against $6 = 2 \times 3$ against $6 = 3 \times 2$. Criterion:
resulting coupling vectors agree to $10^{-10}$. This is the sharp test of the theory's
autonomy claim. Failure is a result: the flow is a typed cocycle, fixed-point language is
unlicensed, and everything downstream must be restated in those terms. Note in advance that
$2 \times 3$ and $3 \times 2$ need not agree even when the theory is right, if the two
orderings block genuinely different subgraphs; the instance must be chosen so that both
orderings are legitimate blockings of the same tower, and if no such instance exists the
check is reported as not performed rather than as passed.

**C4, projection agreement.** The variational and Möbius coupling vectors agree to a
relative $0.05$ per step, measured as
$\lVert \theta_{\text{var}} - \theta_{\text{M\"ob}} \rVert_\infty / \lVert \theta_{\text{M\"ob}} \rVert_\infty$
over the pairwise block of the parameter vector. Justification: the measured one-step
truncation residual is $0.0063$, so a disagreement an order of magnitude above the quantity
being truncated indicates the optimizer rather than the physics. Outside this band the step
reports unresolved.

**C5, residual growth.** The per-step projection gap, tracked across iterations. This is the
irrelevance question and it is deliberately declared *without* a pass threshold, because no
principled value is available in advance and inventing one is the error this project already
made once. The check reports the sequence and its ratio, and the interpretation is stated
after the fact and labeled as such.

## Outcomes and what each would mean

All four are informative and none is a failure of the work.

A fixed point with the generated coupling irrelevant would license the truncation under
iteration and close the oldest open question in the status report. A fixed point with it
relevant would mean the pairwise family is not closed under the flow and the declared family
must grow. Only trivial fixed points would corroborate what `STATUS.md` already records from
`07b` and would bound how much the construction can deliver. Failure of C3 would refute the
autonomous-semigroup claim and is the most consequential single outcome available here,
because it invalidates the framing rather than the numbers.

## Phasing and gates

Phase one builds the parametric family, the coarse connection, and the GPU contraction path,
and runs C1 and C2. These are exact identities needing no optimizer, so a defect surfaces
before anything subtle is layered on.

Phase two adds the three coupling routes and closes the step, then runs C3 and C4.

Phase three iterates, looks for fixed points, linearizes, and reports C5 with eigenvalues.

The gate is C3. If compatibility fails, phase three still runs but reports a cocycle rather
than a flow, and no fixed-point or relevance claim is made.

## Out of scope

A continuum limit, a persistence claim, physical RG flow, and any statement about
nonrenormalizability. Transfer-matrix contraction. Instances past ten agents. Deeper towers
than two levels except where a third level is needed for C3.

## Amendment, 2026-08-17: phase three under the failed C3

Reason. C3 was run and failed decisively: blocking the declared C(2, 3) tower by
six directly disagrees with blocking by the inner triangles and then by two, by
$0.204$ in sup norm on the final site couplings against the declared $10^{-10}$,
with a provably lossless intermediate projection, so the failure is the Bayes
kernel composition itself and not the truncation. Per the gate declared above,
phase three runs but reports a cocycle, and this amendment fixes, before any
phase-three measurement, what that means.

**Restatement.** The renormalization data is a typed cocycle: one map per level
pair, composing only along the tower of levels, with no autonomous map on
coupling space. "Fixed point" is replaced by **fixed ray at a declared ratio**:
a reduced coupling vector reproduced up to a per-step scale $\lambda_k$ under
the declared identification, with the rescaled residual reported. No relevance,
universality, or exponent claim is licensed; eigenvalues reported below are
level-local contraction data of the cocycle at a declared point, nothing more.

**Declared flow instances.** Deeper flows come from directly declared
homogeneous cycle instances, which the risk section anticipated would need an
amendment; they are compute-cheap because iteration runs on couplings.
Homogeneous seeds are constructed by procedure, not by hand: tile the site
table of coarse site one and the pair table of coarse edge one-two from the
measured C(3, 3) working-case step, with belief element $1$ and model element
$0$ on every edge. F1: the C(3, 3) tower blocked to a 3-cycle and then to one
site (the inhomogeneous working case; C5 sequence). F2: the homogeneous
8-cycle at ratio two, $8 \to 4 \to 2$ (belief holonomy $2$, conserved). F2b:
the homogeneous 9-cycle at ratio three, $9 \to 3 \to 1$. F3: the homogeneous
6-cycle blocked three ways, by six directly, by two then three, and by three
then two — on a plain cycle every consecutive-block partition is legitimate,
so this recovers the full factorization panel that the nested tower could not
license. A uniform element on a 6-cycle is necessarily flat in $Z_3$; F3
therefore probes composition, not holonomy, and says so.

**Declared measurements.** C5 as declared: the per-step truncation residual
and projection gap, reported without a threshold. C6, composition defect: at
matched final levels, the sup-norm disagreement of coupling vectors between
staged and direct routes, reported as a sequence with successive ratios and
**no pass threshold**, because none is justifiable in advance; whether the
defect contracts (asymptotic semigroup, the standard situation off a fixed
point) or persists (irreducibly typed cocycle) is stated after the fact and
labeled as such. C7, fixed-ray residual: on homogeneous flows at cycle length
at least three (the 2-cycle merges both edge directions into one pair table
and leaves the reduced type), reduce each level to one site table and one
pair table, fit $\lambda_k$ by least squares over the order-one-and-two
block, and report the relative sup residual. The label "fixed ray" may be
applied only when that residual lies within the step's own instrument
resolution, the larger of its C4 ratio and its relative truncation residual —
a claim below the level at which the two read-back routes themselves agree is
not resolvable by this instrument. **Linearization**: the reduced homogeneous
self-map at ratio two on the declared 6-cycle (site plus pair block, 72
anchored parameters), differentiated centrally on the Moebius read-back for
determinism, its spectrum reported under the level-local label above.

**Out of scope of this amendment.** Modifying the kernel family so that it
closes under composition and restores a semigroup is the natural next design;
it is a separate one and is not smuggled in here.

## Amendment 2, 2026-08-17: the reduced self-map and its fixed structure

Reason. The linearization declared above was run and returned spectral radius
$0.779$ at the declared 6-cycle seed: the reduced self-map at ratio two, which
is the blocking composed with the self-similar re-tiling identification that
`Theory/07b` says a fixed connection requires, is a local contraction. A
contraction's fixed point is reachable by iteration at negligible cost, and
measuring it is the completion of "looks for fixed points" that the typed
cocycle actually licenses. What is fixed is a point of the declared composite
map $R_b = \mathrm{reduce} \circ C_b \circ \mathrm{tile}_L$, not of an
autonomous flow; the C6 result stands, and the composite's dependence on the
declared ratio is itself the next falsifier.

Declared measurements, fixed before running. M-fix: iterate $R_2$ on the
6-cycle and $R_3$ on the 9-cycle from the declared seed until the sup change
falls below $10^{-9}$ or a declared iteration cap; report the iteration count,
the final change, the fixed vector's site and pair sup norms, and, at the
ratio-two fixed point, the Jacobian spectrum. M-cross: the relative sup
difference between the ratio-two and ratio-three fixed vectors, reported with
**no threshold** — agreement would be a cross-ratio universality of the fixed
structure, disagreement would confirm that even the fixed structures are typed
by the ratio, and which of these obtains is stated after the fact and labeled
as such. The trivial outcome is declared in advance: the zero coupling vector
is not fixed under $R_b$, because the downward kernels inject transported
mismatch content on their own, so a fixed point is nontrivial by construction
and finding one is not by itself evidence of anything beyond the map's
continuity.

## Amendment 3, 2026-08-17: boundary multiplicity and the one-step pair retention

Reason. The measured fixed structures are factorized, and the diagnosis is architectural: the
declared family joins blocks through one boundary edge, so instances are quasi-one-dimensional
and triviality is the expected outcome. The network-native question is whether boundary
multiplicity — several fine couplings cut per block boundary, the hierarchical-lattice
mechanism — can sustain pairwise interaction under blocking. This amendment declares the
smallest measurement that bears on it, before running it.

**Declared instances.** Homogeneous circulant coupling instances: cycle length $L$ with declared
chord offsets, every site carrying the seed site table and every edge of every declared offset
carrying the seed pair table in cycle orientation, belief element $1$ on offset-one edges and
$0$ on chords, model element $0$ everywhere. The panel is $L = 6$ with offsets $\{1\}$ and
$\{1,2\}$, and $L = 8$ with offsets $\{1\}$, $\{1,2\}$, and $\{1,2,3\}$, all blocked
consecutively at ratio two, giving $k = 1, 3$ and $k = 1, 3, 6$ cut couplings per block
boundary respectively. Offsets never reach $L/2$, so no reciprocal pair arises.

**Declared measurement, M-bundle.** The one-step pair retention factor
$R(k) = \lVert\theta^{\mathrm{pair}}_{\mathrm{coarse}}\rVert_\infty /
\lVert\theta^{\mathrm{pair}}_{\mathrm{fine}}\rVert_\infty$, with both sup norms over the full
anchored pairwise block and the coarse couplings read back by the exact Moebius route with all
coarse pairs admitted (chords can couple next-nearest parents, and truncating them silently
would manufacture retention loss). Reported per $(L, \text{offsets})$ alongside the coarse
three-body truncation residual, with **no pass threshold**: whether $R$ crosses one, and at
what $k$, is the result, and any extrapolation beyond the measured $k$ is labeled as such.
The known limitation is declared now: the phase-one coarse connection refuses parallel coarse
links, so this measurement runs at the coupling level through the blocking contraction alone,
and a bundle-aware coarse connection (one declared link plus retained inter-block plaquette
marks) is a separate construction with its own checks if $R(k)$ makes it worth building.

## Amendment 4, 2026-08-17: regenerated attention at the coarse level

Reason. Every measurement so far treats the coarse pairwise coupling as passively inherited:
blocked, read back, blocked again. The theory it instantiates does not work that way — attention
is regenerated at every level from the current beliefs and the transported divergence,
$\beta_{IJ} \propto \exp(-\overline D_{IJ}/\tau)$, and the ingredients of that regeneration are
exactly the objects the measurements showed do **not** decay: the coarse connection is conserved
and the coarse beliefs are order one. The passive results (factorized fixed structures, the
M-bundle saturation) therefore bound the inherited channel only, and the regenerated channel
must be measured before any triviality conclusion is drawn about the theory.

**Declared construction.** After each blocking step: compute, per channel and per coarse edge,
the flow-averaged transported divergence $\overline D^c_{IJ}$ under the step's own coarse flow
law using the coarse connection's element (the moment-diagnostic observable); form rows over
each receiver's declared sources plus the self loop by
$\beta^c_{IJ} \propto \exp(-\overline D^c_{IJ}/\tau)$ with declared temperature $\tau = 1$;
take uniform occupancies $\alpha_I = 1/m$; and add the regenerated alignment energy
$\sum_c \kappa_c\, \alpha_I \beta^c_{IJ}\, D^c_{IJ}(p_I, p_J)$ to the coarse action before the
next level. Both $\tau$ and the uniform $\alpha$ are declared, not derived, and are recorded as
such. The construction owes a covariance check before any measurement is read: connection-
dependent rows lose phase one's rows-independent-of-the-connection argument, so the C1 identity
must be re-verified for the regenerated action, at the same $10^{-12}$.

**Declared measurement, M-regen.** The fixed structure of the ratio-two regenerated composite
on the declared 6-cycle, iterated from the declared seed to sup change $10^{-9}$ or a declared
cap. Declared in advance to keep the reading honest: the regenerated term is a pair-sector
source built from the conserved connection, so factorized theories are **no longer invariant by
construction**, and a nonzero pairwise fixed block is expected rather than evidential. What is
reported, without thresholds: the fixed pairwise sup norm against the one-step injected scale
(does regeneration sustain more coupling than it injects, or less); whether the map remains a
contraction; and the passive-versus-regenerated comparison at the same seed. Interpretation
after the fact, labeled.

## Amendment 5, 2026-08-17: completeness measurements on the regenerated cocycle

Reason. M-regen established that the regenerated composite sustains interacting fixed
structures. Three declared report-only measurements complete the comparison between the passive
and regenerated readings before the documents are updated; none carries a threshold, and each
interpretation is stated after the fact and labeled.

**RC6, regenerated composition defect.** The C6 statistic on regenerated flows of the
homogeneous 6-cycle: staged routes regenerate at every intermediate level with edges, the
direct route has no intermediate level to regenerate, and the final single-site Moebius site
tables are compared in sup norm. Declared in advance: under regeneration the staged and direct
routes differ *by construction*, because intermediate levels act — a larger defect than the
passive 0.15--0.19 is the expected direction, and the number measures how much level activity
adds to the typing, not whether typing occurs.

**R-ray.** The one-step ray comparison between the declared 6-cycle seed and the regenerated
coarse couplings at ratio two, reported as scale and relative residual beside the passive
values (scale 1.16, residual 0.15 at 8 to 4; the regenerated comparison runs at 6 to 3).

**R-cross.** The regenerated ratio-two fixed vector on the 6-cycle against the regenerated
ratio-three fixed vector on the 9-cycle, relative sup difference, beside the passive 0.81.
Whether the interacting fixed structures remain ratio-typed is the question; either answer is
a result. The 9-cycle iteration routes each application through the declared worker protocol.

## Amendment 6, 2026-08-18: sector-carrying parents and the capacity question

Reason. The parent state space has been pinned to the child's nine states at every level — the
block-spin convention, declared in the original design as the identity state identification.
The M-bundle saturation suggested that pin is a genuine information bottleneck: however many
couplings cross a block boundary, the correlation they mediate must be encoded in nine parent
states. The theory's retention route already licenses larger parents at a declared capacity
price, and the physical reading is the irreducible-sector decomposition (two spins jointly
carry singlet-plus-triplet, and the sector label is what no transport can change). This
amendment declares the smallest sector extension and its one-step measurement.

**Declared construction.** The sector of a block configuration is its belief-channel $Z_3$
charge: $s(x_B) = \sum_{a \in B} k_a \bmod 3$, where $k_a$ is the unique orbit coordinate of
agent $a$'s belief component relative to the first family member (the orbit is free because
the belief seed is asymmetric). The extended blocking kernel is
$T\bigl((p,s) \mid x_B\bigr) = T(p \mid x_B)\,\mathbf 1[s = s(x_B)]$, the audited Bayes kernel
with a deterministic sector readout, normalized over the $27$ parent labels by construction.
The coarse action lives on the $27$-state parent alphabet and is read back by the exact
Moebius route with all coarse pairs admitted.

**Declared measurement, M-capacity.** The one-step pair retention factor with sector-carrying
parents, $R_{\mathrm{cap}}$, on the homogeneous 6-cycle at ratio two with offsets $\{1\}$ and
$\{1,2\}$, reported beside the passive nine-state values ($0.156$ and $0.441$). **Declared
control:** the same computation with the sector readout replaced by the constant label must
reproduce the nine-state retention exactly, which pins the machinery. No pass threshold; the
declared reading rule, fixed now: retention is compared per unit of injected capacity, the
sector map is one declared charge among many, and a rise in $R_{\mathrm{cap}}$ licenses only
the statement that capacity was binding at this seed, not that this sector map is canonical.
Iterating sector-carrying parents (a 27-state level-two theory) requires extending the
downward kernels to the enlarged alphabet and is a separate construction, declared out of
scope for this amendment.

## Amendment 7, 2026-08-18: temperature robustness of the regeneration result

Reason. M-regen was run at the declared $\tau = 1$, an unmotivated constant, and the standing
of "regeneration restores interaction" should not rest on one knob setting. Declared
measurement, report-only: the regenerated ratio-two fixed structure on the declared 6-cycle at
$\tau \in \{0.5, 1, 2, 4\}$, reporting per value the convergence, the fixed pairwise sup, and
the one-step injected sup. No threshold; whether the interacting character persists across the
sweep is the result, and the expected direction is declared for honesty: larger $\tau$ flattens
the rows toward uniform and smaller $\tau$ sharpens them, so the injected scale should vary
monotonically with $\tau$ while the qualitative question is whether the fixed pairwise block
remains nonzero at order the injection everywhere in the sweep.

## Risks

The optimizer is the main one, and C4 exists to expose it rather than to hope. Second, the
$3\times3$ instance may be too small for a fixed point to be meaningful, since the parent
pool caps interaction orders and a two-level tower gives a short flow; if so the answer is a
deeper tower, which is compute-cheap for the reason given above but was declared out of
scope and would be an amendment. Third, the boundary-agent convention joining adjacent
blocks is a genuine modeling choice that the audit's finding about reciprocal versus
independent edge conventions shows is easy to get quietly wrong; it is declared explicitly
in phase one and tested under both conventions.
