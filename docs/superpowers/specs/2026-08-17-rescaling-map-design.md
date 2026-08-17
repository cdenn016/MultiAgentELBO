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

## Risks

The optimizer is the main one, and C4 exists to expose it rather than to hope. Second, the
$3\times3$ instance may be too small for a fixed point to be meaningful, since the parent
pool caps interaction orders and a two-level tower gives a short flow; if so the answer is a
deeper tower, which is compute-cheap for the reason given above but was declared out of
scope and would be an amendment. Third, the boundary-agent convention joining adjacent
blocks is a genuine modeling choice that the audit's finding about reciprocal versus
independent edge conventions shows is easy to get quietly wrong; it is declared explicitly
in phase one and tested under both conventions.
