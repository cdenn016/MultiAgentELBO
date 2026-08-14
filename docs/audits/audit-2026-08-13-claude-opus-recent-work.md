# Deep multi-agent audit of the 2026-08-13 Claude Opus work

**Audited revision:** `f9ce06a5782dd5fd0392761cdd1872a983429326`
**Remote basis:** `origin/main` after `git fetch --prune origin`
**Comparison base:** `2927b0e2f4f5ec0717c16b70e950822048885a62`
**Audit branch:** `codex/claude-opus-audit-20260813`
**Source policy:** read-only. This audit changes no audited theory, witness, implementation, or status file.

## Verdict

The recent work contains useful constructions, but its current closure/status synthesis is **not safe
to use as build authority**. Four load-bearing claims are refuted at high severity:

1. higher-rank shared latents do not universally force negative KL edge weights;
2. the induced-transport cocycle no-go disappears when PIFB2's free positive edge coefficient is
   kept separate from the transport;
3. the support-boundary witness omits the support multiplier on the prior Hessian and therefore tests
   a different functional; and
4. the promoted Fisher edge operator uses the first covariance slot, not the transported second slot
   required by the declared directed forward KL.

Ten additional medium findings invalidate several diagnostic tables, theorem labels, and status
promotions without destroying their narrower valid cores. One low-severity byte-level documentation
defect is also confirmed. A proposed high finding about compact-link closure was dropped after
adversarial review because the governing definition uses the same compact group for links and vertex
gauges.

The immediate recommendation is to repair and reissue `docs/STATUS.md`, the two witness scripts, and
the affected worklog sections before using them to choose the next theory build. The finite exact
ELBO and existing connection-energy theorem are not refuted by this audit.

## Scope and method

The audited range adds or changes six files:

- `docs/STATUS.md`;
- `docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md`;
- `docs/research-plans/2026-08-13-lattice-gauge-identification.md`;
- `docs/research-plans/2026-08-13-tier0-decisions.md`;
- `docs/verification/meta_agent_coherence_witness.py`; and
- `docs/verification/shared_latent_coupling_witness.py`.

The review used independent implementation, numerical-linear-algebra, gauge-geometry,
information-geometry, variational, and source-reachability lanes. A source-only verifier then checked
the consolidated candidates. Every surviving high finding received a skeptic and defender challenge;
the coordinator retained or downgraded severity only after reconciling those challenges. The Research
vault was consulted read-only to preserve the existing boundaries between graph holonomy, base
holonomy, exact meta-agent ELBOs, and continuum claims.

Exact derivations are stored in
`docs/audits/evidence/2026-08-13-claude-opus-review/counterexample-derivations.md`. The deterministic
reproducer and its output are in the same directory.

## What survives the audit

Several useful results should be preserved while their claims are narrowed:

- A shared latent creates genuine cross-agent dependence, unlike the tied-replica product law.
- The rank-one scalar Gaussian construction has an exact positive symmetric graph-Laplacian split
  on its sampled proper-prior instance.
- The `Theory/09` energy-form connection Laplacian is symmetric positive semidefinite under its
  stated hypotheses; the bad four-regime table concerns a retired alternative operator.
- A simultaneously congruent generalized eigenproblem has a gauge-invariant generalized spectrum.
  What fails is identifying the witness's first-slot pencil with the Hessian of the stated forward KL.
- A normalized Gibbs-Haar law on compact-group link variables provides an exact variational model
  after those random link variables and their recognition law are declared.
- The exact retained-mode theorem remains
  `ker L ≅ Fix(Hol)`. The false step is replacing that theorem by an equivalence with flatness.
- Restricting the single governing link/gauge group to a compact subgroup is algebraically closed.
- The finite exact two-channel ELBO package and its literal-PIFB2 caveat are outside the refuted set.

## Findings summary

| ID | Severity | Status | Finding |
|---|---|---|---|
| H1 | High | Refuted claim | The asserted universal `R >= 2` positive-KL obstruction has an exact rank-two counterexample. |
| H2 | High | Refuted claim | The fiber cocycle no-go absorbs the free `beta_ab` coefficient into `Omega_ab`. |
| H3 | High | Refuted claim | The support witness leaves the prior Hessian active after literal support has vanished. |
| H4 | High | Refuted claim | The promoted first-slot Fisher pencil is not the Hessian of the declared directed forward KL. |
| M1 | Medium | Confirmed defect | The four-regime diagnostic uses transpose instead of stored inverse off `O(K)` and never row-normalizes. |
| M2 | Medium | Scope/status drift | The Gibbs-Haar construction is exact for a new model, not the current fixed-link model or point-curvature dynamics. |
| M3 | Medium | Refuted extrapolation | `lambda_0 = 0 iff flat iff meta-agent` is false in both directions. |
| M4 | Medium | Type/scope error | A toroidal interaction graph does not by itself test contextual-base bundle topology. |
| M5 | Medium | Refuted necessity | Nonhomogeneous statistical fibers can still carry nontrivial nontransitive gauge actions. |
| M6 | Medium | Refuted generalization | A homogeneous statistical manifold need not be a symmetric space or split as claimed. |
| M7 | Medium | Verification gap | Standalone witnesses are not collected regression tests; several printed PASS claims lack assertions. |
| M8 | Medium | Missing hypotheses | `d >= K` is not sufficient for invertibility, and correction rank need not equal latent dimension. |
| M9 | Medium | Overlabeling | The scalar rank-one split is an exact flat alignment skeleton, not literally the complete PIFB2 action. |
| M10 | Medium | Authority conflict | Current STATUS/worklog promotions conflict with the newer Tier-0 and lattice reports that correct them. |
| L1 | Low | Confirmed hygiene defect | The worklog contains a BEL byte and LaTeX escapes replaced by tab characters. |
| D1 | Dropped | Refuted audit candidate | Compact links are closed under vertex gauges when both use the same declared compact group. |

## High-severity findings

### H1. The universal higher-rank positivity obstruction is false

**Locations:** `shared_latent_coupling_witness.py:120-151,304-307`;
`2026-08-12-elbo-to-continuum-action-worklog.md:1636-1655,1712-1714`;
`docs/STATUS.md:76-80`.

The witness checks one seeded random loading for each latent rank and then prints and asserts that
rank-two-or-higher corrections cannot retain positive graph-KL weights. The same file later concedes
that the computation is only generic evidence and that existence remains open. The worklog and
STATUS nevertheless promote the universal obstruction and use it to steer the buildout.

An exact counterexample takes `D = I4`, `T = I2`, and loading rows
`(1, .1), (1, .2), (1, .3), (1, .4)`. The Woodbury correction has rank two; all six unique graph
weights are positive; all four residual prior precisions are positive; and the split residual is
exactly zero. The minimum edge weight is `2/11 ≈ 0.181818` and the minimum residual prior is
`9/55 ≈ 0.163636`.

**Impact:** the current Tier-1 obstruction is mathematically false and can prematurely stop a viable
shared-latent construction. The counterexample does not show that arbitrary directed row-simplex
attention is representable.

**Required repair:** replace every universal either/or statement with a sampled-generic observation;
add the exact positive rank-two control; and formulate the actual representability problem with the
row-simplex, directedness, proper-prior, and entropy requirements explicit.

### H2. The induced-transport cocycle no-go fixes away a free coefficient

**Locations:** `shared_latent_coupling_witness.py:180-200,229-277`;
`2026-08-12-elbo-to-continuum-action-worklog.md:1663-1702`; `docs/STATUS.md:61,76-80`.

The proof reads the complete off-diagonal precision coefficient as `Omega_ab`. The declared quadratic
actually contains the product `beta_ab W_ab Omega_ab`. Absorbing `beta_ab` into `Omega_ab` is exactly
what creates the reported self-edge and cocycle failure.

For three two-dimensional agents, choose `S_a = T = I`, loading matrices `Lambda_a = R_a` with
`R_a in SO(2)`, `beta_ab = 1/4`, `W_ab = I`, and `Omega_ab = R_a R_b^T`. Woodbury gives the exact
cross-block `-(1/4) R_a R_b^T`; the transport has exact self-edges and exact cocycle; and the residual
prior is `I/4`. The reproduced maximum cocycle residual is `3.60e-16`.

**Impact:** the claimed sign-contradiction theorem and its design inference toward necessarily free
noncocycle edge data are false. The result remains scoped to the Gaussian quadratic sector and does
not construct the attention entropy or full recognition model.

**Required repair:** separate edge strength, metric, and transport before asking whether transport is
a cocycle; replace the universal no-go by an identifiability statement about their product.

### H3. The prior does not remove the literal PIFB2 support wall

**Locations:** `meta_agent_coherence_witness.py:372-456`;
`2026-08-12-elbo-to-continuum-action-worklog.md:905-931`; `docs/STATUS.md:44`;
`Theory/PIFB2.tex:680-711,742-752`.

The witness models departure by sending only one edge weight to zero while it adds
`alpha * prior[i]` to every agent block without a presence multiplier. PIFB2 instead multiplies the
self-prior term by the same agent-presence function `chi_i`. At an actual support boundary,
`chi_i -> 0`, both the incident coupling and the local prior Hessian vanish for finite `alpha_i`.

Replaying the witness matrices with the declared support factor gives `lambda_min = 0` and three
zero modes for the departing three-dimensional agent. The witness's positive floor `0.09048` is a
result for edge dropout of an anchored, still-present agent, not support departure.

**Impact:** O4 is not discharged, the full-Hessian positive floor is not evidence about literal PIFB2,
and the downstream extent/order-parameter rewrite is unsupported.

**Required repair:** pass `chi` through the assembler and scale every local and pair term exactly as
the functional does. Distinguish edge dropout, support approach on a fixed ambient space, and deletion
of the departed block.

### H4. The promoted Fisher operator uses the wrong KL slot

**Locations:** `meta_agent_coherence_witness.py:283-369`;
`2026-08-12-elbo-to-continuum-action-worklog.md:885-903`; `docs/STATUS.md:43`;
`2026-08-13-tier0-decisions.md:705-721`; `Theory/PIFB2.tex:182-187,511-512`.

The witness assembles `W_{i<-j} = w Sigma_i^{-1}`. The mean Hessian of the declared forward
divergence `KL(q_i || Omega_ij#q_j)` is instead

`W_{i<-j}^{KL} = w (Omega_ij Sigma_j Omega_ij^T)^{-1}`.

The witness's simultaneous-congruence proof is correct for its independently declared first-slot
pencil. It does not supply the claimed KL/Hessian warrant. Tier-0 independently selects the second
slot, reports a `1.05e-1` operator change and an `-8.7%` eigenvalue change, and says the covariance
equality needed to identify the two slots is not granted. A finite-difference check gives Hessian
error `1.16` for the first slot and `1.39e-17` for the second slot on a two-dimensional unequal-
covariance control.

**Impact:** this changes the load-bearing meta-agent spectrum and can change any thresholded coherence
decision near a boundary. The documents currently present two incompatible authoritative operators.

**Required repair:** select the directed second-slot operator when claiming an exact KL Hessian. If
the first-slot pencil is retained, label it an independent reading convention and withdraw O16/KL
closure claims.

## Medium-severity findings

### M1. The four-regime table does not exercise its labels

`_retracted_laplacian` stores `O[(j,i)] = inv(g)` but uses `O[(i,j)].T` for the reverse block. In the
nonorthogonal cells that is a different operator. Its “row-simplex” branch draws independent positive
edge weights but never normalizes receiver rows. The independent reproducer obtains a relative
operator mismatch of `0.371`; its sampled row sums are approximately `1.95, 1.48, 1.73, 1.47`, not
one.

The adversarial panel downgraded this from high because the helper is explicitly retired, the active
energy form remains symmetric positive semidefinite, and the valid algebraic reason for retiring the
old operator does not rely on this table. Correct or relabel the table and add real row-normalized
controls.

### M2. The plaquette ELBO result is conditional on a different random-link model

`2026-08-12-elbo-to-continuum-action-worklog.md:1914-1949` correctly constructs a proper Gibbs-Haar
law after declaring random compact-group links. That construction has variational free energy
`beta E_q[S] + E_q log q`; the displayed formula omits `beta`, although the numerical table retains
`beta = 2`.

The overreach is promoting that construction into the current fixed/point-link model and inferring
that free-energy descent drives a point curvature to zero and therefore forms meta-agents. The newer
lattice report at lines 406-445 already says the implemented penalty is engineered/MAP, a
nondegenerate `q(Theta)` is absent, and variational inference would approach a posterior rather than
force a point link to the flat minimizer. Reissue STATUS so the conditional construction and current
model cannot be confused.

### M3. Curvature, flatness, and meta-agent existence are not equivalent

The exact theorem is `ker L ≅ Fix(Hol)`, not `lambda_0 = 0 iff flat`. A nonidentity rotation about a
common axis has nonzero holonomy but fixes that axis and therefore has a zero mode. Conversely, a flat
torus can have commuting global monodromies with no common fixed vector. The reproducer gives
`||H-I|| = 0.836`, `||L z|| = 0`, and `lambda_min = -1.0e-15` for the curved common-axis control.

The one-family fit in worklog section 3h.3 may remain a valid numerical observation. Remove only the
universal extrapolation in section 3h.4 and the derived meta-agent narrative.

### M4. Interaction-graph topology is not contextual-base topology

The worklog first says the graph is declared independently of the contextual base, then claims a
toroidal agent graph makes the base-bundle topology clause testable. A graph torus can sit over a
contractible base, and a nontrivial base bundle can be paired with a tree. Require an anchor/cellular
map into the base, edge paths, and equality between graph links and connection parallel transports
before interpreting graph monodromy as base topology.

### M5. Homogeneity is sufficient, not necessary, for gauge structure

Nonconstant curvature prevents a transitive isometry group; it does not prevent every nontrivial
group action. Gamma sample scaling sends `(a,b)` to `(a,b/c)` and is a continuous Fisher isometry on
the rate orbit. The reproduced pullback residual is `1.11e-16`. Beta also has the discrete reflection
that exchanges its two shape parameters. Replace “gauge apparatus requires a homogeneous fiber” by
an orbitwise statement: homogeneity provides full-fiber reach, while general fibers may still carry
nontransitive gauge sectors.

### M6. Homogeneous does not imply symmetric

The general claim that a homogeneous fiber splits into compact gauge and symmetric-space matter is
false. A homogeneous space is generally `G/H`; being symmetric requires an additional involution or
the bracket condition `[m,m] subset h`. The full location-covariance Gaussian affine space fails that
condition, although its covariance cone `SPD(K) = GL(K)/O(K)` is symmetric. Narrow the statement to
the SPD sector or prove the symmetric-pair hypotheses for each family.

### M7. The promoted witnesses are not regression-closed

Normal pytest collection is restricted to `tests/`; no collected test imports either recent witness.
The dedicated witness-test probe collected zero tests. `meta_agent_coherence_witness.py` Claim 4 has
no assertions, and several other printed PASS statements assert only one seeded subclaim. Both
witnesses also retain scope paragraphs that contradict code they now run. `docs/STATUS.md:117-119`
overstates them as fully assertion-backed.

Refactor claim computations into importable functions, add positive and negative regression tests,
and bind status claims to JUnit artifacts rather than unconditional print statements.

### M8. Rank and invertibility conclusions omit rank hypotheses

`d >= K` is necessary but not sufficient for the induced block to be invertible; both loading maps
must have adequate rank and the middle factor must be nonsingular. A `d = K = 2` rank-one loading has
determinant zero. Similarly, the Woodbury correction rank is at most the latent dimension and equals
it only under full-column-rank/nondegeneracy hypotheses. Replace every `iff d >= K` and
`#latents = rank` statement with the exact rank bounds.

### M9. “Exactly PIFB2” overlabels a useful scalar skeleton

The rank-one result is an exact symmetric unnormalized scalar mean-alignment quadratic in the flat
identity-transport case. Literal PIFB2 also has directed row-normalized attention, source-label
entropy/prior terms, two transported law channels, and proper typing; the witness's residual diagonal
can be negative. Rename the result instead of discarding it.

### M10. The current authority files contradict their own corrections

The worklog and STATUS close the first-slot metric, support wall, plaquette dynamics, rank
obstruction, cocycle obstruction, and homogeneity necessity while the Tier-0 and lattice reports in
the same revision explicitly correct several of them. A reader cannot determine which recent file is
authoritative. Reissue STATUS only after the source claims and witnesses agree, then pin every line to
the new validated ledger revision.

## Low-severity finding

### L1. Byte-level documentation corruption

The worklog contains a BEL byte (`0x07`) at byte offset `70278`. Tabs also replaced intended LaTeX
escapes around lines 916 and 924-926, producing malformed `alpha`, `times`, and `to` expressions.
Add a C0-control scan to documentation checks and restore the literal escapes.

## Dropped candidate

The initial geometry lane claimed that compact link values were not closed under retained full-GL
vertex gauges. The challenge found that `Theory/02_geometry.tex` defines both link values and vertex
reframings in the same group `G`; setting that `G` to a compact subgroup makes
`a_i^{-1} Theta_e a_j` stay in `G` by closure. The candidate is therefore dropped. A short explicit
sentence that the compact declaration also restricts vertex gauges would prevent the ambiguity.

## Adversarial challenge record

| Finding | Skeptic | Defender | Coordinator |
|---|---|---|---|
| H1 rank obstruction | Requested downgrade because a later caveat says “generic” | Upheld high: universal worklog/STATUS still steer Tier 1 | **High, refuted** |
| H2 cocycle no-go | Conceded the free positive edge coefficient defeats the proof | Exact rotation construction, proper prior, exact coefficient match | **High, refuted** |
| H3 support prior | Conceded; only an edge-dropout reinterpretation could save it | Literal support factor produces three zero modes | **High, refuted** |
| H4 Fisher slot | Argued the abstract first-slot pencil is a valid convention | Showed it is promoted as KL-derived and moves the headline eigenvalue by 8.7% | **High, refuted as KL closure; abstract congruence result retained** |
| M1 regime table | Downgrade: retired helper, active energy form unaffected | Agreed after proving executable mismatch | **Medium** |
| M2 plaquette ELBO | Downgrade: newly declared Gibbs model is mathematically exact | Conditional construction retained; current-model dynamics withdrawn | **Medium** |
| M3 curvature equivalence | Downgrade: sampled fit can remain local | Exact fixed-space counterexamples retained | **Medium** |
| M9 exact PIFB2 label | Downgrade: narrow skeleton and caveats are useful | Rename rather than discard | **Medium** |
| Dropped compact-link finding | Refuted the premise: one group `G` is used throughout | Original counterexample assumed two different allowed groups | **Dropped** |

## Mechanical verification

All commands used the CPU interpreter; this audit makes no CUDA claim.

- Both recent standalone witnesses exited zero at the pinned revision and produced byte-for-byte
  identical replay output.
- Targeted holonomy tests: **43 passed, 0 failed, 0 skipped** in 3.515 seconds. The JUnit file covers
  `tests.test_u1_two_path_holonomy_witness`, `tests.test_discrete_holonomy`, and
  `tests.test_holonomy_experiment`.
- Broad bounded CPU lane: **945 tests, 0 failures, 0 errors, 3 skipped** in 188.596 seconds. It excluded
  `test_attention_experiment.py`, `test_categorical_dqm_experiment.py`,
  `test_remediation_evidence.py`, and `test_manuscript_build.py`; it is therefore not a full-suite
  closure claim.
- An earlier bounded full-suite attempt reached 882 tests with no source-test failure before the
  command wrapper aborted at its 180-second/output boundary and wrote one internal error. It is
  retained only as historical evidence, not counted as a pass.
- A dedicated probe for tests named after the two new witnesses collected **zero tests**.
- The audit counterexample reproducer exits zero and asserts all reported counterexamples.

Primary evidence is under
`docs/audits/evidence/2026-08-13-claude-opus-review/`, including JUnit XML, source hashes,
deterministic stdout, exact derivations, the counterexample reproducer, and byte-scan output.

## Required remediation order

1. **Invalidate and reissue status authority.** Mark H1-H4 as refuted/open in `docs/STATUS.md`; remove
   stale test totals and bind the replacement to a current validated ledger.
2. **Repair the shared-latent witness.** Add the exact rank-two control; separate `beta`, `W`, and
   `Omega`; state exact rank hypotheses; rename the scalar skeleton; and remove contradictory scope
   text.
3. **Repair the meta-agent witness.** Thread `chi` through every term; choose the second-slot KL
   metric or label the first-slot pencil independent; fix the retired table; and replace print-only
   PASS statements with assertions plus negative controls.
4. **Reconcile the worklog with its newer reports.** Preserve the conditional Gibbs-Haar result, but
   withdraw the current-model and point-curvature dynamics inference; replace the flatness iff chain
   with `ker L ≅ Fix(Hol)`; restore graph/base typing; and narrow homogeneity/symmetric-space claims.
5. **Add collected tests and rerun closure.** Add importable tests for every promoted witness claim,
   rerun the full CPU suite without exclusions or honestly record remaining obligations, and issue a
   revision-bound claim ledger.

## Buildout advice after remediation

Do not move from these witnesses directly into continuum physicalization. The highest-leverage next
gate remains finite and presentation-aware:

1. define the equivalence relation under environment-node split/merge, null-agent insertion, and
   observationally identical kernel dilations;
2. prove which exact VFE and informational readouts descend to that quotient, or exhibit a decisive
   no-go;
3. construct the collective joint-law lift and shared Fisher semigeometry on the quotient; and
4. only then revisit continuum actions, emergent spacetime, or dimensionful constants.

The corrected shared-latent examples should be used as witnesses inside that theorem, not as proof
that literal PIFB2 or a physical ontology has already emerged.
