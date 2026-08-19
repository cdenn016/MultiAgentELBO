# Remediation of the lab-versus-theory audit — 2026-08-18

Response to every item on the punch list of `2026-08-18-lab-vs-theory-audit.md`. Baseline
`9171363`. Test suite before the work: 1463 passed, 17 skipped under
`CUDA_VISIBLE_DEVICES=-1 PYTHONHASHSEED=0`. After: 1485 passed, 17 skipped, including 21 new
regression tests in `tests/test_lab_vs_theory_audit_remediation.py` that pin each repaired
behavior to the number the audit's verifier derived independently.

Every measurement below was executed on the declared seed after validating it against the
published invariants `site_sup = 1.432150`, `pair_sup = 0.016265`, exactly as the audit's
verifiers did.

## 1. The parent now costs something — critical, fixed, amendments 10–14 republished

`partition_dynamics.py` books `E_Q[-log P_S(parent)]` inside the per-block parent optimization,
using the tower's own declared top prior `tower_vfe.PARENT_STATE_WEIGHTS` on the same nine-element
parent space the partition route uses. The per-block cost is now
`min_p [ Σ_{a∈B} c_a(x_a, p) − log P_S(p) ]`, so opening a block is charged, and the all-singleton
partition is no longer the exact minimizer of the cross-scale group by construction. An instance
whose parent space has a different cardinality carries no declared top prior and falls back to the
maximum-entropy law on its parents, which is not inert either — it charges `log |S|` nats per
opened block.

The reproduction matches the audit's verifier to six decimals:

| | published | audit prediction | re-measured |
|---|---|---|---|
| singletons, k=1 | 0.586234 | 0.000112 | **0.000112** |
| direct, k=1 | 0.306494 | 0.958252 | **0.958252** |
| singletons, λ=100 | 0.604915 | 0.000126 | **0.000126** |

Amendments 10–14 were re-taken in full and written to
`docs/results/2026-08-18-amendments-10-14-republication.json`; STATUS §16 and the ROADMAP Layer-B
and Layer-R rows carry the new numbers with the retired ones named. The verdicts that changed:
M-part reverses from singleton-modal to direct-modal at both instances; M-bind's modal class is
direct at every λ; M-anchor's modal flip disappears and becomes a relative statement about where
mass moves; M-flow's quenched/annealed reversal is withdrawn entirely as an artifact of the free
parent; M-cross-env and M-share keep their mechanisms and change their magnitudes. The seven
committed figures were regenerated from the re-taken measurements.

## 2. λ never reaches the block energy — high, restated

Restated rather than rewired, because the construction is right and the reading was wrong.
`_kernel_model` builds the block energy from level-invariant declared structure, and the
instance's couplings enter only through the level's Boltzmann flow. That is what Proposition 4
says: replacing the point-mass child recognition law by the flow shifts every candidate by the
same flow entropy. Putting couplings into `K_down` would be a different theory, not a bug fix.

The structural fact is now stated in `_kernel_model`, `blocking_posterior` and the
`participatory_blocking` module docstring, and it is *tested* —
`test_no_coupling_scale_moves_the_block_energy_landscape` asserts `U(R, x)` is bit-identical
between λ=1 and λ=100. The claim "no formation transition on this ray" is withdrawn in STATUS and
the ROADMAP: a coupling sweep is a flow reweighting and cannot move the landscape, so its flatness
is a property of the construction rather than evidence about formation.

## 3. The M-info confirmation — critical, withdrawn and replaced with a real control

"Confirming the amendment-8 direction" is struck from `STATUS.md` and `ROADMAP.md`. Two reasons
are now recorded in both the documents and the `capacity_information_retention` docstring. The
sign of any sector gain is a data-processing theorem, because the enlarged label is a
deterministic refinement of the nine-state one applied identically on both blocks with the
denominator unchanged. And the declared `constant_sector` control collapses the axis and
reproduces the nine-state law by construction, so it is an identity.

`cocycle_flow.py` gains a `readout` parameter with the operative control the audit asked for:
`readout="first_member"` carries the same number of labels and no gauge charge. Measured:

| | k=1 | k=3 |
|---|---|---|
| gauge charge, 27 labels | +10.16% | +5.27% |
| first-member control, 27 labels | **+67.43%** | **+38.64%** |

The charge is not distinguished among three-label readouts at this seed, and the sector gain is
now reported against the control. Figure 2B draws all three bars.

## 4. Four checks that could not fail — high, all four now executed

**C2 Wilson charge.** The rank comparison is retained as bookkeeping but no longer decides
`passes`. `check_wilson_charge_conservation` now writes each parent's retained interior loop and
the fine lift of the coarse cycle as integer vectors of the fine edge space, expresses them in the
fundamental basis of the fine cycle space, and requires them to generate that lattice exactly —
full rank *and* unit elementary divisors, by Hermite reduction over the integers. A family
spanning a finite-index sublattice passes a rank test and fails this one. Verified: the declared
C(3,3) tower spans with `fine_rank = 4`; the routine rejects index-2 sublattices, rank deficiency,
and dropped generators, and accepts redundant unimodular families.

**`ker L_I ≅ Fix(Hol)`.** `run_checks.py` gains a triangle with non-identity tree links — the
shipped fixtures had identity tree links, which is exactly why the dimension surrogate passed at
every root. The isomorphism is now executed: kernel vectors evaluated at a root lie in that root's
fixed space (residual `4.8e-15`), fixed vectors extend by transport back into the kernel
(`1.4e-15`), and wrong-root membership fails by `0.144`, with the based holonomies genuinely
differing across roots (spread `1.007`) so the test is exercised rather than vacuous.

**`scale_cocycle` composition residuals.** The direct channel was the composed product, so four
residuals compared an expression with itself. `DIRECT_FINE_TO_MACRO_ROWS` is now declared as
literal rationals and the composition is checked against it: gap `0` as declared, and `1/1000`
under a one-row perturbation.

**Staged aggregation.** The scenario transported every contribution to the global root before
grouping, testing `(a+b)+(c+d) = a+b+c+d`. Each block is now summed at its own root frame and only
the block totals are carried up, so the two routes traverse different paths. Direct `[4, 2]`
against staged `[3, 2]`, gap `1.0`. The gap is reported as a new metric
`staged_aggregation_path_dependence`, lower-bounded on non-trivializable connections and
target-zero on trivializable ones — so it is falsifiable in both directions, and `flat_cycle`
exercises the zero side.

## 5. `retained_interaction_order` — high, threaded

`finite_exact` gains three `INT-01_retained_order_*` metrics computed from the configured
projection. The declared interaction `0.3 x1x2x3 + 0.4 x1x2x4` has exactly two nonzero Hoeffding
components, both of order three, so the omission norms have exact closed forms: `0.7/0.7/0.5` for
order ≤ 2 and `0.0/0.0/0.0` for order ≥ 3. `metrics.json` now differs across the sweep and each
metric is pinned to a predicted value rather than reported. `scale_cocycle` threads the same key
into its truncation: `pairwise_truncation_control` is `0.32394712` at order ≤ 2 and `0.0` at order
≥ 3. `gaussian_realization` decomposes no interaction and reads the key nowhere; rather than split
the shared schema and rewrite every published gaussian config hash, `TheoryConfig` now says so
explicitly.

## 6. `parent_priors` — medium, threaded, and the docstring corrected

`one_step_pair_retention`, `capacity_pair_retention`, `capacity_information_retention`,
`initial_step` and `iterated_step` all take `parent_priors` and pass it to the kernel. The
unconditional "gauge-invariant by construction" is replaced by a statement of when invariance
holds and what it costs when the prior is left fixed.

Verified on the full `3^6` shift group, regauging graph, matter and parent law together: relative
drift `5.74%` with the prior untied, `2.7e-9` with it threaded. The audit's downgrade to medium
stands — the drift sits below the sector gain — and the defect is real.

## 7. The Möbius anchor — medium, exposed and swept

`mobius_couplings` takes an `anchor`, threaded through the read-back and the retention
measurements, defaulting to the declared `DECLARED_ANCHOR_STATE`. `anchor_swept_sup` reports the
pinned value beside the swept range. Over all 729 anchors of the coarse triple, the one-step pair
retention runs `0.1295`–`0.1874` at k=1 (pinned `0.1557`, range 37.2% of the pinned value) and
`0.3759`–`0.4621` at k=3 (pinned `0.4414`, range 19.5%). The pinned values stand as published; the
range now travels with them in STATUS. The MI retention is exactly anchor-invariant, so this
qualifies the sup-norm quantities only — matching the audit's own narrowing of the finding.

## 8. Ewens concentration — medium, threaded, and the verdict is a surface

`_kernel_model`, `blocking_posterior` and `anchored_posterior` take `concentration`;
`BlockingPosterior` records the value it was taken at, so a posterior cannot be reported without
it. `concentration_surface` reports the modal class across a grid and brackets every crossing.
Bisected to nine digits, the modal class crosses from the direct block to singletons at
`θ = 6.117084` (k=1) and `θ = 6.173072` (k=3). The declared `θ = 1` verdict is a point on a
reported surface.

## 9. The MI ceiling at roundoff — medium, raises

`capacity_information_retention` raises when the boundary ceiling falls below `MI_CEILING_FLOOR
= 1e-12` rather than dividing one roundoff residue by another. At λ=0 the ceiling is
`1.128338e-16` and the call now raises; the declared instances sit at `4.97e-6` and `1.49e-5`,
six orders above the floor. The exclusion is enforced by code instead of by declaration in a
design document.

## 10. Low-severity items

`CUDA_VISIBLE_DEVICES=-1` and `PYTHONHASHSEED=0` are documented in the README as required rather
than optional, with the eighteen-test failure they cause named. `run_rescaling_figures.py` has the
`sys.path` insert every other root launcher carries and runs without `PYTHONPATH`. The §16 barrier
attribution went out with the M-share rewrite rather than being restated. The C3 statistic is
named: `0.204` is a sup-norm anchored log-density, and the laws differ by TV `0.042` and KL
`0.0050`, so "order one" is a statement about the coupling vector and not a distributional one —
the refutation itself is unaffected and survived every artifact hypothesis the audit tested. The
Koecher–Vinberg citation is corrected in both STATUS and the ROADMAP: it classifies *symmetric*
cones, homogeneous **and** self-dual; homogeneity alone is Vinberg's open-ended T-algebra
classification. The multiscale package's WITHHELD status is reconciled — it was already stale when
written, its ten findings having been repaired in `cec901e`/`23b1e19`/`b16e37d` and accepted — so
the Proposition-4 citation ban is lifted, with the caveat that the repairs bought review
acceptance and not a ledger closure state, and that Proposition 4 as implemented before
2026-08-18 is retired with amendments 10–14.

## Not done, and why

Two findings the audit recorded were left alone deliberately, and neither is on the punch list.

The parent is selected by the cross-scale term plus the prior rather than by the joint argmin over
all of `U`; the audit bounded the error at `4.9e-3` nats, three orders below the deciding gaps.
The `partition_dynamics` module docstring now says exactly what is minimized instead of claiming
the exact conditional optimum.

The two `ArithmeticError` guards at `scale_cocycle.py:394-395` and `:438-454` are symbolic
identities that can never fire. They are dead assertions rather than wrong ones, and removing them
was not requested.

The whole `docs/verification` ledger question — both ledgers in triage with zero closure states,
151 and 72 commits behind HEAD — is outside a code punch list and is left where the audit put it,
in the unverified CANDIDATE section.
