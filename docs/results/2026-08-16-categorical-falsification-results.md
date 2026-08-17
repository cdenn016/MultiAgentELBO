# Finite Categorical Falsification Results — 2026-08-16

## Result boundary

This record reports one execution of the finite categorical falsification
laboratory declared in
`docs/experiments/2026-08-16-finite-categorical-falsification/spec.md`, whose
metric contracts are pre-registered in `docs/hypotheses.md`. The design implements
the experiment called for in `gauge_vfe_rg_status.tex` section 9 and detailed in
`docs/derivations/2026-08-16-multiscale-two-channel-graph-vfe-rg/REPORT-part4-literature-experiment-verdict.md`
section 13.

Six agents sit at one contextual point on two directed three-cycles joined by two
cross edges. The structure group is $\mathbb Z_3$ carrying two distinct
representations, $\rho_b(k):z\mapsto z+k$ and $\rho_m(k):z\mapsto z+2k$, and every
agent state is a pair of laws drawn from finite orbit-closed families. Nothing is
Gaussian, deliberately, because Gaussian closure properties are special and would
confound a failure of the mechanism with a failure of the ansatz.

What follows is mechanical implementation and finite experimental evidence on one
declared instance. It does not prove a theorem, construct a rescaling map or a
renormalization group, establish persistence, or establish a continuum limit or
physical time. Two pre-registered falsifiers fired and one mandatory control
failed; those are the substantive results, and they are reported as results rather
than treated as defects to be tuned away.

## Environment and commands

Python 3.14.4, NumPy 2.4.4, pytest 9.0.2, CPU only. No CUDA claim is made and none
is needed: every quantity is a finite sum of rationals and logarithms of rationals.

```
python run_categorical_falsification_lab.py
python -m pytest -q -p no:cacheprovider tests/test_two_channel_gauge.py \
  tests/test_categorical_falsification_model.py tests/test_tower_vfe.py \
  tests/test_coarse_composition.py tests/test_closure_residual.py \
  tests/test_holonomy_retention.py tests/test_partition_dynamics.py \
  tests/test_downward_influence.py
```

The launcher's declared dictionaries use seed `20260816`, fixture
`two_channel_z3_v1`, admitted family `both`, eight null-control seeds, and two
hundred descent restarts, at `atol` $10^{-12}$ and `rtol` $10^{-10}$.

## What the six measurements found

### M1, the accounting identity holds

The tower free energy computed by flat enumeration of the joint agrees with the
sum of its six conditional-KL groups to $2.66\times10^{-15}$, against a
pre-registered refutation threshold of $10^{-12}$, across three observation records
and two recognition seeds. The falsifier did not fire.

The flat route materializes all 944,784 entries of the joint on the three-agent
reduced instance, sums them for the evidence, normalizes, and takes one flat
relative entropy, using no chain rule and no analytic marginalization. It does
evaluate the downward kernel as a per-agent product, because that product is the
declared definition of the kernel, so the two routes share the declared factor
builders and share nothing of the free-energy assembly. That is the sense in which
the agreement is a check, and no more is claimed for it. Setting the recognition
law to the exact posterior closes the gap to exactly zero and returns
$-\log p(o\mid X)$ to the bit. The joint sums to $0.99999999999999989$ over all
eight records, one unit in the last place below one.

The naive sum of local row potentials exceeds the free energy in every case, with
overcount between $0.7704$ and $0.7801$. Every declared interaction factor is an
edge of boundary size two, so the naive sum is exactly twice the overcount, which
the tests confirm. The naive sum is not an evidence bound and is labeled as such.

### M2, coarse-edge composition holds, and both aggregation traps are real

Nested pushforwards of the directed edge-event law through correlated endpoint
kernels compose to $5.55\times10^{-17}$, one to two units in the last place, with
mass preserved to within one unit in the last place at every step.

The literal three-node witness reproduces exactly. With occupancy
$(0.9,0.1,0)$ and the declared rows, pushing the event law gives
$\beta^c_{IJ}=0.9$ while uniform row averaging gives $0.5$, a discrepancy of
exactly $0.4$ at bit-exact equality. On the six-agent instance under its skewed
occupancies the same discrepancy reaches $0.0875$.

Replacing a genuinely correlated endpoint kernel by the product of its own endpoint
marginals moves the coarse event law by $0.0514$. The trap named in the theory,
assuming $K=C\otimes C$ while the intermediate assignments are correlated, is
therefore measurable rather than hypothetical. The existing attention coarsening in
this repository hardwires that product form and cannot express the correlated case,
which is why a general endpoint kernel over ordered pairs had to be added.

### M3, pairwise closure is false here, and its falsifier fired

The largest generated three-body coefficient is $6.672\times10^{-2}$, so any
implementation reporting a pairwise coarse theory for this system is falsified.
Measured against the retained flow the model itself assigns, rather than against an
unweighted sup norm, the omitted many-body part is about two percent, and two
percent is the honest number to quote.

The measurement rests on a declaration the builder added and flagged: the block
parent must be eliminated exactly. An action built from the per-agent likelihood
and the declared per-edge divergences alone is exactly pairwise and would leave
nothing to measure. That control returns a triple coefficient of
$-4.4\times10^{-16}$, pure floating-point rounding and fourteen orders of magnitude
below the measured value, which is what pins the result as real.

An independent oracle checks the machinery. Eliminating the centre spin of an Ising
star with field $h_0$ and couplings $J_1,J_2,J_3$ gives a leading-order three-body
coefficient $2\,\mathrm{sech}^2(h_0)\tanh(h_0)J_1J_2J_3$, derived here and
reproduced by the implementation to sixteen digits. The exact coefficient
approaches it as the couplings shrink, with ratios $0.470$, $0.815$, $0.951$,
$0.988$, $0.997$ over successive halvings, the gap quartering each time as an
order-$\varepsilon^2$ correction should. No equality is asserted at finite coupling.
The coefficient vanishes exactly at both analytic degeneracies, zero field and any
zero coupling.

### M4, the predicted holonomy asymmetry is observable

All three predictions hold. On the block carrying nontrivial belief holonomy the
belief distortion is $+\infty$ under the orbit family, whose fixed sector is empty,
and $0.0872080$ under the whole simplex, whose fixed sector is the single uniform
law. The finite value equals $\log 3 - H(p)$ exactly, an independent closed form the
run reproduces to $10^{-16}$. The same block reaches exactly zero distortion in the
flat model channel at an explicit witness configuration, and both channels reach
zero on the flat block.

The infinite value is Proposition 8 realized rather than asserted: whether the
fixed sector is empty is a checkable property of the pair formed by the holonomy
group and the admitted family, and an infimum over the empty set is infinite by the
stated convention. It is carried through publication as an explicit sentinel rather
than dropped or clamped to a finite surrogate.

The theory falsifier did not fire. Twenty block-and-family pairs admit a
zero-distortion belief parent, namely every block whose induced belief holonomy is
trivial, so it is not the case that no coherent belief parent exists anywhere on
this cyclic graph.

The dressed-transport law normalizes to exactly one, in rationals, when the endpoint
factor is carried over all ordered pairs. Dropping it and restricting the sum to
members of the two blocks gives masses $1.27$, $2.30$, $1.50$ and $2.40$, so the
restricted form is not a probability measure under soft memberships. The barycenter
lies outside the represented group in the measured belief cases; it is computed,
guarded, and never composed, inverted, or used as a transport. Conditional
independence gives the convolution, and the converse is exhibited false by a
maximally dependent joint on $\mathbb Z_3$ whose composite still equals the
convolution of its marginals.

One limit is recorded rather than smoothed over. Stabilization without flatness has
no witness inside the orbit families, because no nontrivial element of $\mathbb Z_3$
fixes any of their laws. The witness is supplied on the uniform law of the simplex
family and is reported as exactly that, not as the general statement.

### M5, persistence fails, and the pipeline fails its own null control

The persistence falsifier fired. The best residence-to-relaxation ratio is $1.02$
against a pre-registered support threshold of ten, so there is no timescale
separation between partition persistence and belief relaxation, and the persistence
hypothesis fails on this instance. The noise amplitude is not a free knob that could
be tuned to avoid this: the exact coordinate update has temperature one, and any
other value is a tempered sector rather than the same objective.

The more consequential result is the control. With transports and the belief family
randomized and the skeleton, occupancies, kernels, partition prior and capacity
bound held fixed, every block-formation statistic is unchanged, and the reference
run sits inside the null range on modal occupancy, maximum residence, ratio, largest
co-membership, and exit slope. **The pipeline fails its own null control.** What
blocking appears is produced by the partition prior and the capacity structure, not
by the declared holonomy asymmetry, and the designed cycle partition is in fact the
least persistent of the six candidates. Any claim that this instance exhibits
holonomy-driven block formation is unsupported, and the control is what establishes
that.

This is the outcome the specification anticipated when it made the null control
mandatory: a pipeline that finds blocks under randomized transports is detecting its
own blocking algorithm rather than the system.

The exit-time linearity verdict is withheld unless the sweep carries at least
thirty-two exit seeds, because at eight seeds the fit returns $R^2=0.27$ while at
fifty it returns $0.982$. A small sweep measures seed noise, not the basin. At full
power the fit is linear with $R^2=0.982$ and slope $1.49$, so the configuration is
metastable in the Arrhenius sense; it is simply shallow.

### M6, downward influence is real, and the control does not collapse

The declared downward kernel is not decorative: the influence supremum is
$0.557265$, strictly positive, so the primary falsifier did not fire.

The deterministic-pushforward control did not collapse. On the three-member blocks
it gives $0.676$ to $0.698$ against the declared $0.557$, and it drops below the
declared influence only for blocks of four or more. Whether the specification's
operationalization or the implementation is at fault is left open and recorded
rather than resolved. There is a structural reason to suspect the specification: a
deterministic parent is a statistic of its children, so distinct parent values have
disjoint fibers, and a supremum of total variation across distinct parent values
could be near maximal by construction rather than near zero. If that is right, the
quantity that should collapse is the within-fiber variation, and the pre-registered
prediction named the wrong statistic. This obligation is open.

It is also worth recording that the influence supremum is identical for all six
agents across both blocks, including the holonomy-carrying block and the flat one.
The proposed explanation is that the supremum ranges over the whole parent space
while the transports only permute it, so the statistic cannot distinguish the two
blocks. That explanation is plausible and unverified.

## Status of the sixteen metrics

Eleven metrics pass as implementation checks. Four are inconclusive by construction
rather than by outcome, because they bear on open hypotheses that one finite
instance can neither establish nor refute: claiming a pass would overstate what the
run shows, and claiming a failure would read as a software fault. The sharp
instance-level statements are carried by the falsifier verdicts published beside the
metrics, and the run status is inconclusive overall.

A metric status and a falsifier verdict are different things, and the laboratory
keeps them separate. A metric fails when the code fails; a falsifier fires when the
system behaves as the pre-registered refutation describes. The two disagree here on
purpose: the three-body metric passes precisely by correctly detecting the nonzero
coefficient that refutes pairwise closure.

Falsifiers fired: `M3_pairwise_closure_false`, `M5_no_timescale_separation`,
`M6_deterministic_control_did_not_collapse`, and
`NULL_pipeline_detects_its_own_blocking`.

## What this changes for the program

The exact finite layer survives its checks. The accounting identity, the
coarse-graining composition, the holonomy retention machinery, and the two
aggregation controls all behave as the theory says, and the predicted
belief-against-model asymmetry is directly observable.

The block-formation story does not survive. On this instance the free energy does
not select the designed partition, the designed partition is the least persistent of
the candidates, there is no timescale separation, and randomizing the entire gauge
structure changes nothing. That is consistent with the negative result the status
report already records, that with an unrestricted parent the free energy ranks no
partition and selection must come from declared structure. Here the declared
structure is doing all of the work, and the experiment makes that visible instead of
letting it hide behind a plausible-looking hierarchy.

## Obligations left open

Whether the M6 control was mis-specified or mis-implemented is unresolved, and it
should be settled before the downward-influence measurement is relied on. The
identical influence supremum across blocks needs verification rather than an
explanation. A null that also randomizes the partition prior and the capacity bound
would separate their contribution from the transports', which the present null
cannot do. Finally, the cross-model verification pass for this work has not been
completed; nothing here carries `EVIDENCE_VERIFIED`, and every claim above is at
most a candidate supported by executed output on one declared instance.
