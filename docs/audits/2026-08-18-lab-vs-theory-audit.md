# Deep audit — the lab against the theory — 2026-08-18

**Artifact revision:** `9171363` (tree `10865135`), working tree clean apart from four untracked build PDFs.
**Author model (lab and investigators):** Opus 5. **Verifier model:** Fable 5, cross-model per the standing rule.
**Question asked:** does the lab compute what the theory says it computes? Not code quality — the generic
sweep ran on 2026-08-18 (`2026-08-18-rescaling-lab-audit.md`, F1–F9, fixed in `4eed61f`) and was excluded.

Five domain investigators (variational, gauge theory, information geometry, implementation,
philosophy of science) returned 44 findings. Three Fable verifiers re-derived the critical and high
clusters from their own probes. Every verifier validated its seed against the published invariants
`site_sup = 1.432150`, `pair_sup = 0.016265` before trusting any number.

## The result that frames everything else

**Every published §16 number reproduces.** Independently written drivers re-derived `R_sup`
0.15574727/0.44140555, `R_cap` 0.20850148/0.56791627, `R_MI` 0.023012/0.025350 with gains +10.16%/+5.27%,
ceilings 4.9698e-06/1.4926e-05, M-part 0.58623/0.02508/0.08220/0.30649, λ=100 singleton 0.60491, M-anchor
0.55158/0.84034/0.90219/0.19639, M-cross-env 0.2009 (κ=32 ≡ 128), M-share 0.110452 vs 0.012538 at induced
pair sup 12.618, annealed 0.44061/0.48902, `coupled_blocking_descent` direct 0.46102 at acceptance 0.4722.
All seven committed figure PNGs regenerate byte-identically.

The arithmetic is sound and the record is honest. Every finding below concerns what the numbers **mean**.

## Test suite

    bare:                                       18 failed, 1445 passed, 17 skipped
    CUDA_VISIBLE_DEVICES=-1 PYTHONHASHSEED=0:             1463 passed, 17 skipped

All 18 failures from `tools/remediation_evidence.py:2508-2511`. Neither variable is documented anywhere;
the prior audit recorded only the CUDA half.

---

## Verified findings

Every item in this section was re-derived by a Fable verifier from its own probes at `9171363`.

### 1. The partition posterior charges nothing for a parent, and the published aggregation negatives invert when it does — CRITICAL

`partition_dynamics.py:413-418`, `:459`, `:502`; the omitted prior at `tower_vfe.py:46-56`, consumed at `:513`.

The block parent is chosen by `np.argmin` over a cross-scale cost and costs nothing, while the number of
parents varies with the candidate. So `cross(R,x) = Σ_B min_p Σ_{a∈B} c_a(x_a,p)`, and the all-singleton
partition is its exact minimizer at **every** configuration — verified constant to 8.9e-16 across all
531,441 configurations, minimal everywhere with margin ≥ 0.27 nats at both declared instances. The only
block-count term in the model is the Ewens prior, which sits outside `U` at `:502` and pushes the other way.

`PARENT_STATE_WEIGHTS` is the lab's own declared top prior on a 9-state parent space matching the partition
route's. Booking `E_Q[-log P_S(parent)]` inside the per-block parent optimization reverses the verdict:

| | published | with the declared prior booked |
|---|---|---|
| singletons, k=1 | 0.586234 | **0.000112** |
| direct, k=1 | 0.306494 | **0.958252** |
| singletons, λ=100 | 0.604915 | **0.000126** |

Worth 11.67 nats between the two candidates. The derivation report owning Proposition 4 names this exact
requirement and calls the top-prior route preferable.

*Verifier corrections:* the one-line inequality `min_p Σ f_a ≥ Σ min_p f_a` is an incomplete proof — a
second step on dressed-versus-undressed per-agent minima is required, and was supplied and checked (signed
minimum exactly 0.0), so the conclusion stands.

**Consequence:** amendments 10–14 need re-publication, not annotation. That is five §16 rows and the
ROADMAP's Layer-B and Layer-R narrative.

### 2. λ never reaches the block energy — HIGH

`coupling_readback.py:327-354`; couplings enter only at `participatory_blocking.py:114-118`.

`_kernel_model(graph, name)` takes only the graph and discards `instance.couplings`. Verified: `U(R,x)` is
`np.array_equal` between λ=1 and λ=100 across four candidate partitions and all 531,441 configurations.
Reweighting the λ=1 energies by the λ=100 flow alone reproduces the published λ=100 posterior. The M-bind
sweep acts solely through the flow; no coupling of any magnitude can move the partition-energy landscape.

Found independently by three investigators before verification.

### 3. The M-info row's confirmation is vacuous, and its sign is a theorem — CRITICAL

`cocycle_flow.py:324-332` (charge), `:338-342` (kernel).

**Blind to the correction it confirms.** Transports enter the sector charge only as a per-block additive
constant (`T_B = 1` for every block at both instances), so the root-framed charge is a cyclic relabeling of
the retired family-referenced one, and mutual information is relabeling-invariant. Measured difference in
`R_MI`: 3.4e-11 at k=1, 1.3e-11 at k=3 — roundoff, nine orders below the +10.2% gain. Meanwhile `R_sup`
differs by 6.4e-2 and 1.6e-1. The probe self-validates: the family-referenced `R_sup` reproduces the
*retired* published 0.144/0.406 exactly. `R_MI` cannot testify to the amendment-8 direction.

**The sign carries no information about the gauge charge.** `extended[p*sectors+s] = base_kernel[p] *
(charge==s)` makes the 9-label parent a deterministic function of the 27-label one, applied identically on
both blocks, with the denominator unchanged — verified by folding the 27-label coarse law onto the 9-label
control to 1.4e-13. So `R_MI(27) ≥ R_MI(9)` by data processing for every instance, ratio, coupling and
readout. Arbitrary same-cardinality readouts beat the gauge charge:

    gauge charge (root-framed Z_3)   +10.2%
    first-member belief coordinate   +67.4%
    random Z_3, seeds 0/1/2          +68.7% / +97.1% / +47.7%
    first-member state-index mod 3   +611.9%
    boundary-aware index readout     +4166.4%

The declared `constant_sector` control is an identity, not an independent check.

### 4. No production path re-expresses the parent law under regauging — MEDIUM (downgraded)

`cocycle_flow.py:201`, `:319-320`, `:746`, `coupling_readback.py:375` pass no `parent_priors`; only
`rescaling.py:380-392` (the C1 harness), `closure_residual.py:470-534` and `contraction_backend.py:159,176-177`
do. Verified at every cited line. The published instance's parent prior is non-uniform
(`[0.1111, 0.0667, 0.1778, 0.0444, 0.1556, 0.0889, 0.2, 0.0222, 0.1333]`), so the asymmetry is live.

**The investigator's headline magnitudes did not reproduce and are withdrawn.** Sweeping the full `3^6`
shift group in both raw and anchored constructions:

| statistic | claimed drift | verified drift |
|---|---|---|
| M-capacity | 33.9% | 33.4% |
| M-bundle | 60.7% | 9.7–15.3% |
| `R_MI` | 14.4% | **3.5% (k=1), 1.3% (k=3)** |

The claim's decisive sentence — that the drift exceeds the sector gain — is **wrong**: drift sits below the
gain at every published grid point and every λ (3.5% vs +10.2%, 2.9% vs +10.4%, 2.5% vs +11.2%, 3.3% vs
+16.8%). Magnitudes in the claimed range arise only under malformed variants (graph regauged without matter
or the reverse), which are not gauge transformations. Threading the re-expressed prior restores invariance
to ~1e-11.

So the defect is real and the docstring's unconditional "gauge-invariant by construction"
(`cocycle_flow.py:475-478`) is false as stated — but the M-info sector gain survives it. Severity
downgraded from critical to medium on the verified magnitudes.

*Also found:* the committed invariance test `tests/test_cocycle_flow.py:268-305` uses shifts that are zero
at both block roots, which is exactly why it passes despite the defect. And the largest genuine gauge
dependence is in the sup statistics, with a further ~6.3% retention drift at root-fixed shifts caused by the
anchored fine-sup denominator moving — an anchoring artifact, not the un-threaded prior.

### 5. Four checks cannot fail — HIGH

- **C2 Wilson-charge conservation** (`rescaling.py:537-591`). Both ranks are counts of non-tree edges, so
  the comparison is the Euler identity `E − V + 1 = Σ_b(E_b − V_b + 1) + (E_cross − m + 1)`. Verified: 2000
  random group-element assignments on `C(2,3)` all give `(3,3)`; ~2550 draws over six graph shapes always
  equal `E − V + 1`; identity-breaking inputs raise *before* the comparison, so it is a tautology on its
  entire reachable domain. No span over any module is computed. *Correction:* the `passes` field also
  conjoins a cut-loop element equality that is a weak check rather than an inert one.
- **`ker L_I ≅ Fix(Hol)`**, marked **P** (`STATUS.md:39`, `Theory/09:379-399`). Executed checks compare
  integer dimensions only (`run_checks.py:2709-2711`, `:2750-2755`; `meta_agent_coherence_witness.py:355-388`).
  No root-evaluation or membership test exists anywhere in the live tree. Since `Fix(Hol_r)` and `Fix(Hol_r')`
  are conjugate they are always equidimensional: on an `SO(3)` instance the dimension surrogate passed at both
  roots 200/200 while wrong-root membership failed by 0.02–1.73 against ≤1.4e-14 at the correct root.
  *Mitigation:* shipped fixtures use identity tree links, so the hazard is unexercised today.
- **Four `scale_cocycle` composition residuals** (`scale_cocycle_experiment.py:202`) compare an expression
  to itself — `direct_channel` **is** the composed product. Two `ArithmeticError` guards
  (`scale_cocycle.py:394-395`, `:438-454`) are symbolic identities and can never fire.
- **Cross-scale staged aggregation** (`holonomy_experiment.py:386-429`) transports every contribution to
  vertex `"0"` *first*, then regroups, so it tests `(a+b)+(c+d) = a+b+c+d`. An honest staged aggregation
  gives path-dependent gaps of 1.0 and 2.0 on the same fixture.

### 6. `retained_interaction_order` gates no metric — HIGH

`finite/experiment.py:158-162`, `:285`; `scale_cocycle_experiment.py:152-153`, `:298`; no reader at all in
`gaussian_realization`. A required, type-validated key folded into the content-addressed run identity: 13
distinct config hashes, `metrics.json` byte-identical across every sweep value in all three experiments.
Every interaction metric is computed from a hardcoded `retain_interaction_order(interaction, 2)` sibling.

The theory-pure full-order path does exist and run — saved omitted sup exactly 0.0 at order 4 or `None`
against 0.7 at order 2. It is simply not what any metric is computed from.

### 7. The anchored Möbius anchor is a hidden gauge fixing — MEDIUM

`coupling_readback.py:152` hardcodes `anchor=(0,)*width` with no parameter or config key. Published C3 =
0.2035 reproduces exactly and moves to 0.392234 under a width-1 anchor; retention moves by 1.21–1.57× on the
published pipelines. *Corrections:* the claimed lower endpoint 0.196 did not reproduce (minimum 0.2014 over
67 anchor combinations), and the scope is narrower than claimed — the law-unit MI retention is **exactly**
anchor-invariant, so this applies to the sup-norm quantities and the C3 site-table defect only.

### 8. Smaller verified items

- **Parent selected by the cross-scale term alone** while `U = cross + graph` (`partition_dynamics.py:414-434`),
  contradicting the module's "exact conditional optimum" declaration at `:34-36`. The joint argmin differs on
  188,082 of 531,441 configurations; error bounded at 4.9e-3 nats, three orders below the deciding gaps.
- **The barrier attribution is contradicted by the decomposition** (`STATUS.md:378`). Cross-scale spread
  5.444631 nats; graph group ≤ 0.0195 nats and at the seed slightly favoring direct (−0.0086); Ewens prior
  favoring direct by 4.787492 nats. The whole barrier is the cross-scale group. *Correction:* the graph
  group is not "capped near log 2" — it has no such bound in principle; its measured maximum is 35× below
  log 2, which strengthens the contradiction.
- **The Ewens concentration is hardwired** at `Fraction(1)` (`coupling_readback.py:351`) with no override
  reachable from `blocking_posterior`; the block-count prior the theory names is unreachable from the
  published route. The modal class crosses at θ = 0.8784 (k=1) / 0.8844 (k=3) — *not* the claimed 0.888,
  where singletons are already modal.
- **λ=0 returns retention from roundoff** (`cocycle_flow.py:517`): `R_MI = 0.073916` from a ceiling of
  1.128338e-16, larger than every genuine k=1 value; the 27-label variant returns 2.48, violating the
  `R_MI ≤ 1` bound. No published number is contaminated, and the design spec declares the exclusion at
  `2026-08-17-rescaling-map-design.md:597-598`, so this is guarded by declaration rather than by code.
- **Sup-norm versus MI units** (`STATUS.md:372`): `R_sup² = 0.024257` against `R_MI = 0.023012` at k=1
  (ratio 1.054), residual factor 2.92 at k=3. The level comparison is largely a units artifact; the *gain*
  half of the claim survives. The repo's own figure code already draws the square-law check.

---

## Unverified findings — CANDIDATE, investigator-only

These were not put through a verifier and must not be treated as closed.

**Documentation and governance.** Five of the eight §16 rows are produced by the Proposition-4 posterior,
which lives in the multiscale package `ROADMAP.md:214` forbids citing; Proposition 4 is not among the three
named survivors, and Corollary 6 — which explains the null control — is in the same document and never
cited. That WITHHELD status was itself already stale when written: all four High and six Medium findings were
repaired the previous evening in `cec901e`/`23b1e19`/`b16e37d` and accepted in full.
`appendix_claim_ledger.tex:215` cites `COMPLETE_AFFIRMATIVE` where the release records
`COMPLETE_AFFIRMATIVE_WITH_CORRECTIONS`, omitting that the certified proposition was written into
`Theory/07b` *after* the reviews binding that file by SHA-256 approved. The Layer-K exit gate cites
Koecher–Vinberg for homogeneity when it classifies *symmetric* cones; homogeneity alone is Vinberg's
T-algebra classification, which is open-ended. The quasi-1D Perron–Frobenius diagnosis is marked **D** while
`Theory/07b:2869` stamps the same sentence `NUMERICAL`. Amendments 3–14 each landed in the same commit as
their results. The repo states the chain more confidently than the project's own vault, which carries
"tentative — not independently verified" on every one of these runs. Both ledgers are in triage with zero
closure states, 151 and 72 commits behind HEAD.

**Quenched-only publication.** The annealed object is direct-modal at every λ including λ=0 (0.4412 →
0.4356) where quenched is singleton-modal; the coupled λ=100 posterior sits within 3% of the pair-free null
against the ~0.28 of class mass a crossing would require. Consistent with finding 2 and pointing the same
way as finding 1, but not separately verified.

**Wiring.** No committed runner emits the §16 statistics — `run_rescaling_figures.py` is the only root
launcher missing the `sys.path` insert and dies at import, carries no config dictionaries and writes no
`RunStore`, so §16 sits outside the artifact contract. `config.json` drops the `compute` section for the
eight launchers omitting `COMPUTE`. Four `COMPUTE` keys are validated and never consulted; `allow_tf32=True`
names a mode the worker unconditionally refuses. `contraction_backend` defaults to CUDA with a hardcoded
interpreter outside `ExperimentConfig`, so the "CUDA is reserved for gaussian_fixed_ray" freeze has a second
door — and a published §16 number came through it. `finite_counterexample` accepts bounds `(4,8)` and
enumerates `(2,4)`, disclosed in the artifact.

**Theory-side.** The compact-link-group declaration has no executable representative — the only admissible
group is `GL+(2)`, noncompact, hardcoded as a `Literal`; the von Mises and SL(2,R) evidence exists only as a
prose table. The Wilson term wired into partition selection is monotone-decreasing under refinement with cut
faces charged nowhere, a second force toward singletons. "Typed cocycle" names a chain of composed maps with
no cocycle identity checked anywhere. On the declared Z₃ instance `Fix(Hol) ≠ ∅` iff `Hol = {0}`, so it
cannot distinguish "holonomy ∈ Stab(q)" from "= identity"; the pure path exists on the augmented family and
the SO(3) witness carries the claim properly.

---

## Cleared — checked and found sound

KL argument order is `KL(receiver ‖ transported source)` at all thirteen call sites, no flip, matching
`Theory/PIFB2.tex:208`. Nats throughout; zero support returns `+inf` uniformly. `_block_bayes_kernel:589`
normalizes over the parent axis — a genuine child→parent Markov kernel in the declared direction, so
`R_MI ≤ 1` is a real data-processing theorem. Fisher matches `Theory/05c` eq. `pb-fisher-defect-score-variance`,
correctly typed with `establishes_dqm=False`. Schur complement and Galerkin match `Theory/09:50-166`.
Hoeffding/Möbius decomposition correct. C1 gauge covariance is a genuine test, not a both-sides transform:
exhaustive `3^6` sweep, worst deviation 1.33e-15, and interior-only regauging confirms it is not inert. Path
ordering consistent throughout. `attention_gauge` genuinely `GL⁺(K)`-invariant over 200 random frame families
to condition 1e6. The artifact contract holds in all four clauses, including the executed never-overwrite
guarantee. No silent dispatch fallback; no silent CUDA fallback. `NUMERICS` conditioning gates enforced and
raising. `Z = e^{−β}I₀(β)` correct to 1.5e-14. Berker–Ostlund / Migdal–Kadanoff attribution correct.
Ewens/CRP form standard. `Theory/07b` cites the lab as *refuting* its own compatibility law — the direction
is lab-refutes-theory, not circular. The exposition companions are not cited as authority anywhere.

**C3 comes out stronger.** Its refutation survived every artifact hypothesis tested: the flat control gives a
*larger* defect (0.452 vs 0.204), 24 edge-order permutations give only {0.1994, 0.2035}, and the kernel-level
gap is 0.721. Only the wording needs work — 0.204 is a sup anchored log-density, while the laws differ by
TV 0.042 and KL 0.0050, so "order one" should not be read distributionally.

---

## Punch list, ranked

1. **[critical]** Book `E_Q[-log P_S(parent)]` inside the per-block parent optimization
   (`partition_dynamics.py:413-418`) using the model's declared parent-state law, and re-publish
   amendments 10–14.
2. **[high]** Either put `instance.couplings` into the block energy or restate M-bind as a
   flow-reweighting sweep and withdraw the "no formation transition" reading (`coupling_readback.py:327-354`).
3. **[critical]** Strike "confirming the amendment-8 direction" from `STATUS.md:372` and `ROADMAP.md:116`;
   add a same-cardinality non-charge readout as the operative control and report the sector gain against it
   (`cocycle_flow.py:338-342`).
4. **[high]** Replace the C2 rank comparison with an executed span check over the fine cycle space
   (`rescaling.py:574-579`); add a root-evaluation and membership test for `ker L_I ≅ Fix(Hol)` or downgrade
   its **P**; build `scale_cocycle`'s direct channel from independently declared data; sum each block at its
   own root frame in the staged-aggregation scenario.
5. **[high]** Thread `retained_interaction_order` into the `INT-01_*` metrics or drop it from the schemas
   and the frozen `config_keys`.
6. **[medium]** Thread `parent_priors` through the production paths and correct the unconditional
   "gauge-invariant by construction" docstring; the sector gain itself stands.
7. **[medium]** Expose the Möbius anchor and report the anchor-swept range beside the pinned value for the
   sup-norm statistics.
8. **[medium]** Thread `prior` and `concentration` through `blocking_posterior` and report M-part/M-bind as
   a surface; the published verdict sits ~0.6 nats of log-odds from a flip on a hardwired knob.
9. **[medium]** Raise rather than divide when the MI ceiling is at roundoff scale (`cocycle_flow.py:517`).
10. **[low]** Document `CUDA_VISIBLE_DEVICES=-1` and `PYTHONHASHSEED=0`; add the `sys.path` insert to
    `run_rescaling_figures.py`; correct the §16 barrier attribution, the C3 statistic's name, and the
    Koecher–Vinberg citation; reconcile the Proposition-4 citation ban and the stale WITHHELD status.
