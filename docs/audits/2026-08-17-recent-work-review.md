# Audit of the 2026-08-17 session, and its remediation

Scope: commits `aafc2c3..8b8ee06`, all of 2026-08-17. Four expert investigators swept the
closure/M3 mathematics, the gauge and holonomy work, the pre-registration record, and the
experiment wiring.

**Verification status: incomplete.** A cross-model verifier (Opus, per the standing
cross-model rule) was dispatched against the findings and was stopped before it returned a
single verdict. Everything below therefore rests on the investigators' own executed
evidence, which I reproduced independently for the load-bearing items before acting on
them, and not on an independent adjudication. Findings marked *reproduced* were re-run by
the orchestrator; the rest were acted on from investigator evidence alone.

## What was actually wrong

The session's headline claim was that the M3 coarse-graining metric had been corrected to
measure in its pre-registered direction. The audit found that the correction was real but
that its framing, its threshold, and the implementation underneath it were all defective.

### The measurement itself carried four independent defects

*Reproduced.* All four are in the coarse-direction closure code and all four moved the
published numbers.

The first is an orientation bug. Divergence tables are indexed `[receiver_state,
source_state]`, but they were broadcast into the child tensor by `reshape`, which fills
axes in ascending order. On any edge whose receiver has the higher agent index the row axis
landed on the source, so the energy evaluated was $\eta_{ij} \mathrm{KL}(q_j \| \Omega_{ij}
q_i)$ rather than the declared $\eta_{ij} \mathrm{KL}(q_i \| \Omega_{ij} q_j)$. Three of the
eight reference edges were affected, including both cycle-closing edges. The corrected
tensor now reproduces the declared per-edge energy to $2.7\times10^{-15}$ over sampled child
states; before the fix it differed by up to $4.9\times10^{-2}$ nats, which exceeds the
entire pairwise coefficient the module reports.

The second is a missing coupling. Every other consumer of the same edge-event law
multiplies by the declared $\kappa$; the closure module did not, so it ran at half the
declared coupling in both directions.

The third is the parent measure. Both directions hard-coded a uniform parent prior where
the declared law, `PARENT_STATE_WEIGHTS`, is not uniform. This is what the module docstring
had described as "the exact block configuration law of the declared model", which it was
not.

The fourth is the blocking map. The contraction weight was $\prod_a K(x_a \mid p)$,
normalized over children for fixed parent, so $\sum_p T(p \mid x) \neq 1$ and the map did
not preserve the partition function; $Z'/Z$ was $1.4\times10^{-3}$. That is a Bayes
posterior over parents, not a real-space blocking kernel, while the surrounding prose called
it "the direction a renormalization step actually runs". The kernel is now the normalized
Bayes posterior under the declared parent law, which satisfies $\sum_p T(p \mid x) = 1$
exactly and preserves $Z$.

A fifth, smaller asymmetry: the flow-weighted residual centered the retained part on its
flow mean but not the omitted part, though the justification given for centering applies
verbatim to both. Both are now centered.

### The falsifier that fired was never the pre-registered falsifier

The specification registers a conjunction: the three-body coefficient is nonzero *while the
implementation reports a pairwise coarse theory*. The shipped verdict evaluated only the
first conjunct, and the specification's own reference calculation says that conjunct is
generically true. The recorded M3 firing was therefore an artifact of an incomplete verdict
function, and would not have fired as written on either elimination direction's data. This
is a direction-independent ground for withdrawal that costs nothing after the fact, and it
is now the ground the documents give.

### The pre-registration did not say what the documents claimed it said

*Reproduced against git history.* The two halves of M3 have different standing and the
session's documents merged them. For CFL-07 the specification does name the projection onto
the declared parent family, so redirecting it corrects a genuine deviation. For CFL-06 the
specification's three-body item names no elimination direction at all, and the
pre-registration entry as of `4a0cc0b` asked only for a nonzero coefficient with a lower
bound above zero. Both the direction and the smallness threshold were fixed on 2026-08-17,
after the first measurements. The claim that "the specification had pre-registered the other
elimination" was false of the entry it appeared in.

The $0.10$ threshold occurs exactly twice in the repository, in that sentence and in the
code, and is derived from nothing. On the pre-fix numbers it had no power to separate the
two directions: the against direction scored $0.046$ and $0.044$, comfortably inside the
window it was meant to exclude. After the implementation fixes it does separate them
($0.0063$ coarse against $0.28$ and $0.21$), but that is a fact discovered after the
threshold was chosen, not a reason the choice was principled. The documents now say this
plainly and mark CFL-06 as recording a number rather than surviving a test.

### The metric could not fail

`CFL-06` was registered as a lower-bounded metric with bound $0.0$ on a quantity that is a
ratio of absolute values, so it passed for every input including infinity. It is now an
upper-bounded metric against the stated threshold and can fail.

### Stale assertions of the withdrawn verdict

Three places still asserted the withdrawn result after the commit that claimed to withdraw
it, including the manuscript's own summary of what the experiment found ("pairwise closure
is false here") and the results document's example of the metric-versus-falsifier
distinction. All corrected.

### Reported partitions

Of six declared candidate partitions only two carry the three blocks a three-body coupling
needs, and one of those two has no connected block and cannot be measured. The published
table's other two rows were introduced on 2026-08-17 and are not declared candidates; they
are now labeled exploratory, and the unmeasurable declared candidate is now reported.

### The object being blocked

The fine action is the auxiliary pairwise child theory, not the declared generative tower.
The tower's scale-0 conditional factorizes over agents given the parent, so blocking it
would give an exactly pairwise parent theory with no three-body term. The measurement is
still the right question to ask — whether blocking a genuinely pairwise child theory stays
pairwise — but it is not a measurement of the tower's own coarse-graining, and the module
and results document now say so.

### The gauge side carried its own critical defect

*Reproduced by the implementing agent against pre-fix code.* `regauge` in the mark-carrying
parent applied a single uniform shift to every block boundary leg, while the induced gauge
action moves the two orientations oppositely: under a block-constant gauge, a leg whose
receiver lies inside the block picks up $-g$ and one whose source lies inside picks up
$+g$. The code preserved the difference of the two legs where the gauge action preserves
their sum, so `root_gauge_orbit` and `orbit_representative` were orbits of a different
$Z_3$ action than the gauge action — which is the module's load-bearing claim. The
presentation was pushed the wrong way too, by $\rho(+\text{shift})$ where the compensating
matter rule gives $\rho(-\text{shift})$; regauging the model and comparing cost tables
agrees exactly at $-1$ and deviates by $1.98$ at $+1$. The test that claimed to pin this
regauged with the code's own `regauge` on both sides and never recomputed the datum, so it
could not have failed. All fixed, with four replacement tests that fail against the
pre-fix code.

Three further gauge defects, all fixed: backward traversal hard-coded reciprocity, so the
"independent" edge convention never reached the transport layer and silently used negated
forward elements instead of its declared reverse arcs; the bi-directed face set excluded
two-cycles, which is exactly where independent-convention curvature lives; and the two
conventions were not matched controls, because the reverse-element draws advanced the
shared random stream and changed the attention rows. The reference skeleton's
`downward_kernel` hashes identically before and after the transport change, which is what
lets the closure numbers above stand.

### The test suite claim

*Reproduced by the investigator against a pre-session worktree.* The session reported "19
pre-existing failures in `test_remediation_evidence.py`". The count is right and the
attribution is wrong: 18 are in that file and one is in `test_markdown_hygiene.py`. The 18
are an environment gate, not a defect — under the harness's declared environment
(`CUDA_VISIBLE_DEVICES=-1`) that file passes 168/13-skipped. The 19th is a real defect,
also pre-existing: stray C0 control bytes in
`docs/prompts/2026-08-16-fixed-point-graph-rg-deep-research-prompt.md`, now stripped.
Neither is caused by the M3 work. Confirmed after remediation: that file passes
168/13-skipped under `CUDA_VISIBLE_DEVICES=-1`, and the rest of the suite is 1227 passed,
3 skipped.

### Not fixed

`theory.admitted_family` is validated, recorded, and read by no measurement — all three
legal values produce identical CFL-08. The Wilson charge is not conserved under blocking: a
partition disposes of gauge-invariant holonomy that a coarse theory ought to carry, and the
total curvature charge is a function of the partition rather than of the connection.
Composing the retained boundary generators into coarse plaquettes is the fix and is
feature-scale work, deliberately deferred.

## Corrected numbers

Coarse direction, post-fix, at the reference record:

| partition | two-body | three-body | ratio | flow residual |
|---|---|---|---|---|
| $\{1,2\}\{3,4\}\{5,6\}$ (declared) | $9.90\times10^{-2}$ | $6.20\times10^{-4}$ | $0.0063$ | $0.00016$ |
| $\{2,3\}\{1,6\}\{4,5\}$ (exploratory) | $1.12\times10^{-1}$ | $1.54\times10^{-4}$ | $0.0014$ | $0.00004$ |
| $\{1,2,3\}\{4,5\}\{6\}$ (exploratory) | $1.35\times10^{-1}$ | $1.98\times10^{-3}$ | $0.0147$ | $0.00051$ |

Against direction, on the same dimensionless footing: $0.28$ and $0.21$ on the two declared
blocks, with five-agent sup norms $1.21$, $2.19$, $1.25$, $2.24$, $1.41$ — no decay.

The qualitative conclusion is unchanged and is now better supported: in the coarse-graining
direction the generated three-body coupling is small against the pairwise one, and the
elimination that runs the other way behaves very differently. What changed is that the
separation is now a factor of roughly forty in a scale-free ratio rather than a factor of
four, the numbers come from a partition-function-preserving blocking map, and the claim is
fenced by what the pre-registration actually said.

## What remains open

The single binding constraint on a second renormalization scale is still the missing
rescaling map. Whether the small generated coupling is *irrelevant* under iterated blocking,
as opposed to small at one step, is unmeasured and needs a fixed point to linearize about.
The instance caps the parent pool at three labels, so one blocking step admits exactly one
order above pair order and a decay hierarchy is not something this instance can exhibit.
