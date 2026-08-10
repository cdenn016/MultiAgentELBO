# Independent Review — Session 5 Gauge-Holonomy Laboratory

## Review identity and verdicts

- Contract base: `b80df01f239c2f9a18842f6887cdeca67dff508f`
- Reviewed branch head: `54e7faaa139f73a053c4be5463545dc4df9f780c`
- Scientific implementation revision: `54e7faaa139f73a053c4be5463545dc4df9f780c`
- Review role: independent reviewer-author; no production, test, launcher, result, theory, fixture, or scientific-evidence file was edited.

**Spec-compliance verdict: PASS WITH FINAL-GATE OBLIGATIONS.** The reviewed branch implements the frozen Session 5 artifact and metric inventories, all five scenarios, the required negative controls, no-argument launcher, scope exclusions, and exact lane allowlist. The unresolved shared-ledger and final-integration test obligations are not lane implementation failures, but they prevent program-level closure at this branch head.

**Code/scientific-quality verdict: APPROVE WITH FINAL-GATE OBLIGATIONS.** I found no remaining load-bearing gauge-theory, mathematical, or implementation defect in the declared finite `GL+(2)` laboratory. Exact rational recomputation agrees with the executable source and saved default bundle. Program-level approval remains contingent on the parent-owned fresh broad JUnit, coverage, artifact-reproduction, and revision-bound ledger gate; TDD RED chronology remains report-only process evidence.

## Sources and evidence reviewed

I read the full `b80df01..66c7260` review package once, the governing plan and frozen contract, all Task 1–3 reports, the result record, the relevant graph-link and trivialization sections of `Theory/SPEC.md` and `Theory/02_geometry.tex`, the operational-base-holonomy item in `Theory/appendix_claim_ledger.tex`, the Research-vault pages `[[Holonomy]]`, `[[Gauge transformation]]`, and `[[Gauge equivariance and geometric deep learning]]`, and the focused frame-condition fix at `54e7faaa139f73a053c4be5463545dc4df9f780c`.

The controlling convention is the frozen theory's endpoint-frame transformation of a transporter and conjugation of closed-loop graph holonomy (`Theory/02_geometry.tex:561-616`). The Research wiki correctly warns that vertex-coboundary links telescope while independent edge links can carry nontrivial graph holonomy. I treated the wiki as context and verified the load-bearing statements against the frozen theory and executable source.

Current mechanical evidence inspected read-only:

- `.verification/gauge-holonomy/pytest-focused.xml`: `36` tests, `0` failures, `0` errors, `0` skipped, suite time `3.084 s`.
- `.verification/gauge-holonomy/coverage.xml`: `discrete_holonomy.py` `346/395 = 87.59%` lines and `121/164 = 73.78%` branches; `holonomy_experiment.py` `188/193 = 97.41%` lines and `39/44 = 88.64%` branches. Both modules pass the frozen 80% line gate.
- `.verification/gauge-holonomy/reproduction-evidence.json`: SHA-256 `069206202c1bfbd5894138238edcaec78619e52c00a6029c040ee6404b117e2c`; launcher exit `0`; source and replay manifests complete; all seven semantic files byte-identical; all 53 saved arrays name- and value-identical.
- `.superpowers/sdd/2026-08-09-six-session-theory-simulation-buildout/task-2-fix3-regression.xml` and `task-2-fix3-postcommit.xml`: each records `37` tests, `0` failures, `0` errors, `0` skipped at `54e7faaa`; suite times are `2.926 s` and `2.992 s`, and each includes the frame-condition fail-fast test.
- Historical broad evidence: `.superpowers/sdd/2026-08-09-six-session-theory-simulation-buildout/task-2-full.xml` records `471` tests, `0` failures, `0` errors, `2` skipped at the initial Task 2 implementation revision. The later implementation fixes have focused, not broad, post-commit JUnit evidence.

I did not rerun the broad suite, as required by the review brief. No numerical output below is used to close a general mathematical claim.

## Independent exact recomputation

The executable traversal convention in `discrete_holonomy.py:282-306` left-multiplies each successive link. For the default square, let

\[
B=\begin{pmatrix}1&1\\0&1\end{pmatrix},\qquad
D=\begin{pmatrix}2&0\\0&1\end{pmatrix},
\]

with `e01=I`, `e12=B`, `e23=I`, and `e30=D` as constructed in `holonomy_experiment.py:99-151`. I recomputed the following with exact rational matrix arithmetic.

### Ordered cycle and characteristic invariants

The ordered boundary is `("e01", "e12", "e23", "e30")`, hence

\[
H=\Theta_{30}\Theta_{23}\Theta_{12}\Theta_{01}
=DIBI
=\begin{pmatrix}2&2\\0&1\end{pmatrix}.
\]

Its characteristic polynomial is

\[
\chi_H(\lambda)=\lambda^2-3\lambda+2,
\]

so `trace=3`, `determinant=2`, and `discriminant=3^2-4(2)=1`. These exact values match the literals saved by `cycle_holonomy` and `conjugacy_invariants` (`discrete_holonomy.py:310-375`) and the default artifact.

**Falsifier:** any executable or saved product other than `[[2,2],[0,1]]`, or any characteristic invariant other than `(3,2,1)` for these literals.

### Coherent passive conjugacy

For an edge `source -> target`, the code applies

\[
\Theta'_e=A_{\mathrm{target}}^{-1}\Theta_e A_{\mathrm{source}}
\]

at `discrete_holonomy.py:521-536`, matching `Theory/02_geometry.tex:571-576`. Around a closed loop, the intermediate vertex factors cancel, leaving

\[
H'=A_0^{-1}HA_0.
\]

With the experiment's `A_0=D` and all other `A_i=I`, exact multiplication gives

\[
H'=D^{-1}HD
=\begin{pmatrix}2&1\\0&1\end{pmatrix}.
\]

Its trace, determinant, and discriminant remain `(3,2,1)`. This is conjugacy covariance, not equality of matrix entries and not dynamical gauge symmetry.

**Falsifier:** failure of the exact equality `H'=A_0^{-1}HA_0`, or a changed characteristic polynomial under a coherent passive re-trivialization.

### Spanning-tree trivialization criterion

Using the tree edges `e01`, `e12`, and `e23` rooted at vertex `0`, the exact frames constructed by `trivialization_via_spanning_tree` (`discrete_holonomy.py:424-508`) are

\[
V_0=I,\quad V_1=I,\quad V_2=B,\quad V_3=B.
\]

The chord required by a graph coboundary would be

\[
V_0V_3^{-1}=B^{-1}
=\begin{pmatrix}1&-1\\0&1\end{pmatrix},
\]

but the nonflat chord is `D`. Their entrywise residual is

\[
D-B^{-1}=\begin{pmatrix}1&1\\0&0\end{pmatrix},
\]

whose maximum absolute entry is exactly `1`. The fundamental cycle has the nonidentity `H` above, so the graph links are not trivializable. Replacing the chord by `B^{-1}` gives `B^{-1}IBI=I`, proving the pinned flat-cycle control. This is the finite spanning-tree equivalence proved in `Theory/02_geometry.tex:597-616`; it says nothing by itself about principal-bundle topology or base-connection curvature.

**Falsifier:** a nonidentity fundamental-cycle product accepted as exactly trivializable, an identity product rejected, or a chord residual inconsistent with the constructed tree frames.

### Normalized marked-event law and operational observable

For the default operational literals at `holonomy_experiment.py:254-298`, the transported total is

\[
x=(1,0)^T+I(1,1)^T=(2,1)^T.
\]

The two event covectors give logits `(0,2)`, and the stable softmax at `discrete_holonomy.py:615-620` gives

\[
p=\left(\frac{1}{1+e^2},\frac{e^2}{1+e^2}\right),
\qquad \sum_m p_m=1.
\]

For mark values `(0,1)`, the observable is exactly `e^2/(1+e^2)`, numerically `0.8807970779778824`. Under the coherent passive transformation, the transported total becomes `(1,1)^T`, the signal covector becomes `(2,0)`, and the logits remain `(0,2)`. Thus both the normalized law and its scalar expectation are invariant for this declared construction.

**Falsifier:** a probability sum different from one, a coherent logit/observable mismatch, or acceptance by `operational_observable` of an object that is not a normalized `OperationalRecordLaw`.

### Exactly-one-link-pair broken control

The runner starts from all coherently transformed links, then replaces only `e01` and `e10` with their original inverse pair (`holonomy_experiment.py:194-199`). The saved artifact independently yields the changed oriented-label set `{'e01','e10'}` and preserves `broken_e10 @ broken_e01 = I`.

With the transformed states and covectors but this broken pair, the transported total is `(3/2,1)^T`, the logits are `(0,3)`, and the signal-probability gap is exactly

\[
\frac{e^3}{1+e^3}-\frac{e^2}{1+e^2}
=\frac{e^2(e-1)}{(1+e^2)(1+e^3)}
>0,
\]

numerically `0.071777048844550775`. The saved floating result is `0.07177704884455105`, differing only by floating evaluation order.

**Falsifier:** more or fewer than the declared inverse pair changing, loss of the inverse constraint, or a zero/nonfinite operational gap for these literals.

## Contract and implementation audit

| Requirement | Verdict | Evidence and falsification condition |
| --- | --- | --- |
| Exact Session 5 allowlist | PASS | `git diff --name-only b80df01..54e7faaa` contains exactly the seven Session 5 paths: two production modules, two tests, launcher, result document, and this review. Any additional tracked path is a failure. |
| Frozen fixture reachability | PASS | `_load_fixture` validates the fixture and frozen application ID before use (`holonomy_experiment.py:77-88`); `_scenario_fixture` consumes its vertices, oriented edges, and 2-cell (`:99-151`). Independent canonical hashing reproduced application ID `30a4bd...20cd` and physical SHA-256 `a207...f567`. A mismatched hash or unused replacement fixture falsifies this. |
| Scenario/group reachability | PASS | All five frozen scenarios affect edge/cell construction or scenario-specific arrays (`holonomy_experiment.py:42-49, 99-151, 319-426`); group and scenario are rejected unless exact (`:624-640`). Focused JUnit contains all five scenario cases. |
| Validation before RNG/artifacts | PASS | Type, discriminator, fixture, group, scenario, renderer, fixture identity, complex, link, frame-condition, and scenario calculations occur before RNG begins at `holonomy_experiment.py:667` and `RunStore.create` later in the same method. The general fail-fast test at `tests/test_holonomy_experiment.py:348-408` and frame-condition test at `:411-436` replace runtime seams with forbidden sentinels. Any invalid input reaching those sentinels or creating output falsifies this. |
| Frame-condition configuration reachability | PASS | Commit `54e7faaa` passes the full `NumericsConfig` into `_scenario_arrays` and tolerance-aware checks every scenario vertex frame before passive transformation (`holonomy_experiment.py:178-208`). A ceiling of `1.0` rejects vertex `0`, whose condition number is `2.0`; both 37-test fix XML files are clean. Acceptance above the configured ceiling or reaching RNG/provenance/RunStore falsifies this. |
| Ordered transport and passive covariance | PASS | Source implements last-link-leftmost path composition and the endpoint-frame law (`discrete_holonomy.py:282-306, 521-536`). Exact recomputation above agrees. |
| Trivialization/cycle criterion | PASS | Tree frames, fundamental cycles, every-edge residual, and identity test are all executed at `discrete_holonomy.py:424-508`; the literal flat/nonflat test is `tests/test_discrete_holonomy.py:235-257`. |
| Normalized operational law | PASS | Stable softmax normalization and typed observable are implemented at `discrete_holonomy.py:575-636`; coherent/broken literals are pinned at `tests/test_discrete_holonomy.py:303-379`. |
| Required negative controls | PASS | The focused suite rejects a missing inverse, open-path invariants, tree plaquette curvature, raw weights, and link-only operational promotion, and proves the exactly-one-undirected-pair mutation (`tests/test_discrete_holonomy.py:184-393`; `tests/test_holonomy_experiment.py:248-290`). |
| Saved decision reconstructability | PASS | `interaction_complex.json` records rule, observed value, reference, tolerance, applicability, and component values for every metric (`holonomy_experiment.py:540-616`). I recomputed all five statuses from the saved record; all match `metrics.json`. The default NPZs reproduce the cycle, invariants, residual, laws, and changed link pair. |
| Result-status propagation | PASS | Flat tree emits an inconclusive cycle comparison and aggregate result; failure outranks inconclusive, which outranks pass (`holonomy_experiment.py:427-455, 688-696`; test `tests/test_holonomy_experiment.py:166-181`). |
| Deterministic replay | PASS | The durable replay differs only in `output.root`; seven semantic hashes and all 53 array comparisons match. The source manifest is complete with nine files, CPU/float64 provenance, and `git_dirty=false`. Any same-code/config semantic mismatch falsifies this. |
| Sanitized launcher isolation | PASS | The launcher is no-argument and inserts its own `src` path (`run_gauge_holonomy_lab.py:8-11, 20-60`). The focused JUnit includes `tests/test_holonomy_experiment.py:439-480`, which removes Python path/home variables, uses `-I`, and asserts the loaded experiment module is from this worktree. |
| JUnit and coverage | PASS FOR LANE-FOCUSED GATE | Mechanical parsing gives 36/36 focused tests and 87.59%/97.41% line coverage, above the frozen 80% line threshold. A current XML count or module line rate below those values falsifies this record. |
| Claim-field separation | PASS | Metrics explicitly set theorem status, verification state, and origin independently (`holonomy_experiment.py:427-504`); the result remains `NUMERICAL/CANDIDATE/APPLICATION_SPECIFIC` (`:697-706`). Passing thresholds do not promote verification state. |
| Scope exclusions | PASS | The saved scope denies base-connection identification, dynamical symmetry, continuum, universality, and physical time (`holonomy_experiment.py:540-558`); provenance repeats `graph_to_base_identification=false` (`:657-674`). The result record keeps graph-to-base and operational-base holonomy `OPEN/INCONCLUSIVE`, consistent with `Theory/02_geometry.tex:625-640` and `Theory/appendix_claim_ledger.tex:243-260`. No bundle-topology claim is made. |

## Strict TDD audit

Task 1 and Task 2 reports preserve exact RED/GREEN commands, expected failure signatures, repair loops, focused JUnit paths, and commit identities. The final tests are mutation-named and exercise the defects described by the reports. Commit sequencing also shows the factory-control, artifact-reconstructability, single-pair mutation, launcher-isolation, and status-propagation fixes as separate commits.

This is a credible TDD process record, but the RED worktree states and RED JUnit files were not retained as revision-bound machine-readable evidence. Git history commits tests and production together. I therefore accept TDD compliance as a documented process fact for this lane but do not classify the exact write-order claim as independently evidence-verified.

## Claim boundary and scientific interpretation

- The exact derivations above verify the named finite literal identities. They do not prove every admissible `GL+(2)` numerical input is handled stably.
- The general passive conjugacy and graph-coboundary statements are standard/frozen-theory mathematics; the JUnit and residuals check their implementation, not their truth.
- The marked-event map is a declared project/application construction. Its algebraic covariance does not establish empirical relevance.
- Graph links become represented base parallel transports only after the explicit curve assignment and transport-identification hypothesis in `Theory/02_geometry.tex:625-640`.
- The open operational-base-holonomy obligation requires a named principal bundle and connection, base loop, gauge-invariant population statistic, and controlled connection-to-law map (`Theory/appendix_claim_ledger.tex:243-253`). This laboratory deliberately does not supply them.
- Passive coordinate covariance does not prove an equivariant dynamical evolution law.
- Nothing here establishes bundle topology, continuum or thermodynamic limits, universality, nonlinear attraction, or physical time.

## Remaining concerns and required follow-up

### C1 — Final shared verification closure is absent at this head

**Impact:** program publication blocker, not a Session 5 implementation defect.

The current serialized metrics remain `CANDIDATE`, as they should. The only validated task ledger is historical and bound to Task 1 commit `068cbbb`; an activation marker remains, and no current shared `.verification/ledger.json` exists. The parent/final integration lane must start a fresh ledger at the final integration SHA, record separate code, experiment, mathematics, and scope claims with domain-eligible evidence, validate it, and remove the activation marker through the normal gate. This review did not alter the parent-owned control plane.

**Resolved when:** the final integration revision has a validated ignored ledger and no stale activation; otherwise every attempted closure remains `INCONCLUSIVE`.

### C2 — Final integration evidence is not revision-bound to the frame-condition fix

**Impact:** parent-owned final-integration gate; focused Session 5 behavior is current.

The `471`-test broad JUnit was produced at the initial Task 2 implementation revision. Commits `fe15a43`, `2016042`, and `54e7faaa` then changed `holonomy_experiment.py` and its tests. The two fresh 37-test XML files close the focused frame-condition regression at `54e7faaa`, but the existing coverage XML and launcher/replay bundle predate this fix, and no broad-suite JUnit is bound to it. Per the review brief, I did not rerun the broad suite, coverage, or artifact harness.

**Resolved when:** the integration owner runs and mechanically parses the complete CPU suite and coverage, reproduces the published artifact bundle, and validates the ledger at the final integration SHA. Any failure, error, unexplained skip, threshold regression, replay mismatch, or stale ledger binding reopens this approval.

### C3 — RED history is documented but not mechanically reproducible

**Impact:** process-audit limitation only.

The reports give specific RED failure counts and messages, but the pre-production RED states are not committed and their JUnit records are not retained. This does not weaken the current code evidence, but an auditor cannot independently replay the exact historical ordering.

**Resolved when:** future lanes retain revision-bound RED artifacts or patch snapshots, or explicitly classify TDD chronology as report-only process evidence.

## Resolved and superseded finding

### R1 — RESOLVED: `max_frame_condition` is enforced by the laboratory

The earlier C4 concern was correctly reclassified as blocking and is superseded by commit `54e7faaa139f73a053c4be5463545dc4df9f780c`. `_scenario_arrays` now receives `NumericsConfig`, computes every declared vertex-frame condition number, and applies the configured ceiling with the contract tolerances before passive transformation, RNG, provenance, `RunStore.create`, or artifact publication (`holonomy_experiment.py:178-208, 638-667`).

The focused mutation test sets `max_frame_condition=1.0`, rejects vertex `0` with condition number `2.0`, forbids all three runtime seams, and proves no artifact root is created (`tests/test_holonomy_experiment.py:411-436`). Mechanical parsing of both `task-2-fix3-regression.xml` and `task-2-fix3-postcommit.xml` gives `37` tests, `0` failures, `0` errors, and `0` skipped. This resolves the configuration-reachability and fail-fast obligations for the declared scenario frames.

`min_spd_rcond` remains inapplicable because this laboratory has no SPD input. The seed reaches named-stream provenance but not scientific arrays because the declared experiment is deterministic.

## Final decision

**APPROVE WITH FINAL-GATE OBLIGATIONS.** The finite graph-link implementation, exact literal oracles, passive covariance, spanning-tree criterion, normalized operational law, isolated broken-pair control, frame-condition preflight, artifact reconstruction, and scientific scope agree. No load-bearing code, gauge-theory, mathematical, or scientific defect remains. C1 and C2 are mandatory parent-owned final-integration gates; C3 is a report-only TDD chronology limitation. The former C4 is resolved and superseded by `54e7faaa`.
