# Independent Review — Session 5 Gauge-Holonomy Laboratory

## Review identity and verdicts

- Contract base: `b80df01f239c2f9a18842f6887cdeca67dff508f`
- Reviewed documentation/evidence head: `dd13cad54252e3e08d9357aa5c2f4cd7d67c4619`
- Evidence-source revision: `74a1894d20445f6f635f2a7bcc5f02fc8e874499`
- Scientific implementation revision: `74a1894d20445f6f635f2a7bcc5f02fc8e874499`
- Review role: independent reviewer-author; no production, test, launcher, result, theory, fixture, or scientific-evidence file was edited.

**Spec-compliance verdict: PASS WITH FINAL-GATE OBLIGATIONS.** The reviewed branch implements the frozen Session 5 artifact and metric inventories, all five scenarios, the required negative controls, no-argument launcher, scope exclusions, and exact lane allowlist. The unresolved shared-ledger and final-integration test obligations are not lane implementation failures, but they prevent program-level closure at this branch head.

**Code/scientific-quality verdict: APPROVE WITH FINAL-GATE OBLIGATIONS.** The final scoped re-review disposition is **ADDRESSED**: canonical immutable cell boundaries and the C901 refactor close the final review findings without changing the public API or mathematical product ordering. I found no remaining load-bearing gauge-theory, mathematical, or implementation defect in the declared finite `GL+(2)` laboratory. Exact rational recomputation agrees with the executable source and refreshed saved default bundle. Focused JUnit, coverage, and deterministic replay are refreshed at the final production revision. Program-level approval remains contingent on the parent-owned final broad JUnit and revision-bound ledger gate; earlier TDD RED chronology remains report-only process evidence.

## Sources and evidence reviewed

I read the full `b80df01..66c7260` review package once, the governing plan and frozen contract, all Task 1–3 reports, the result record, the relevant graph-link and trivialization sections of `Theory/SPEC.md` and `Theory/02_geometry.tex`, the operational-base-holonomy item in `Theory/appendix_claim_ledger.tex`, the Research-vault pages `[[Holonomy]]`, `[[Gauge transformation]]`, and `[[Gauge equivariance and geometric deep learning]]`, the frame-condition fix at `54e7faaa`, and the final immutable-boundary/C901 fix at `74a1894d20445f6f635f2a7bcc5f02fc8e874499`.

The controlling convention is the frozen theory's endpoint-frame transformation of a transporter and conjugation of closed-loop graph holonomy (`Theory/02_geometry.tex:561-616`). The Research wiki correctly warns that vertex-coboundary links telescope while independent edge links can carry nontrivial graph holonomy. I treated the wiki as context and verified the load-bearing statements against the frozen theory and executable source.

Current mechanical evidence inspected read-only:

- `.verification/gauge-holonomy/pytest-prelim2-focused.xml`: `38` tests, `0` failures, `0` errors, `0` skipped, suite time `3.259 s` at evidence-source revision `74a1894`.
- `.verification/gauge-holonomy/coverage-prelim2.xml`: `discrete_holonomy.py` `378/427 = 88.52%` lines and `121/164 = 73.78%` branches; `holonomy_experiment.py` `194/199 = 97.49%` lines and `43/48 = 89.58%` branches. Both modules pass the frozen 80% line gate after the final source fix.
- `docs/results/evidence/2026-08-10-gauge-holonomy-reproduction-2905cc3.json`: immutable sanitized extract of source-record SHA-256 `7104FAE7649AB0B6098453C8FD16F257D38CF2D9BFE82657C30E1B9C89BB0FA4`; launcher exit `0`; source commit `2905cc3`; source and replay manifests complete; all `7/7` semantic files byte-identical; all `53/53` saved arrays name- and value-identical. Recorded wall time is `0.5004997000032745 s` and sampled peak primary-process working set is `41,566,208` bytes. The ignored latest-run slot is mutable and is not cited as the durable record.
- Retained final-fix chronology: `task-1-final-fix-red.xml` records the intended immutable-boundary RED (`1` test, `1` failure, `0` errors); `task-1-final-fix-green.xml` records its GREEN (`1` test, `0` failures, `0` errors). Post-commit XML records `21/21` direct core tests and `38/38` Session 5 tests clean at `74a1894`.
- Ruff C901: a no-cache scan of both owned Session 5 production modules returns `All checks passed!`; the Task 1 report records the same post-commit result for the refactored core module.
- `.superpowers/sdd/2026-08-09-six-session-theory-simulation-buildout/task-2-fix3-regression.xml` and `task-2-fix3-postcommit.xml`: each records `37` tests, `0` failures, `0` errors, `0` skipped at `54e7faaa`; suite times are `2.926 s` and `2.992 s`, and each includes the frame-condition fail-fast test.
- Historical broad evidence: `.superpowers/sdd/2026-08-09-six-session-theory-simulation-buildout/task-2-full.xml` records `471` tests, `0` failures, `0` errors, `2` skipped at the initial Task 2 implementation revision. The later implementation fixes have focused, not broad, post-commit JUnit evidence.

I did not rerun the broad suite, as required by the review brief. No numerical output below is used to close a general mathematical claim.

## Independent exact recomputation

The executable traversal convention in `discrete_holonomy.py:316-341` left-multiplies each successive link. For the default square, let

\[
B=\begin{pmatrix}1&1\\0&1\end{pmatrix},\qquad
D=\begin{pmatrix}2&0\\0&1\end{pmatrix},
\]

with `e01=I`, `e12=B`, `e23=I`, and `e30=D` as constructed in `holonomy_experiment.py:99-147`. I recomputed the following with exact rational matrix arithmetic.

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

so `trace=3`, `determinant=2`, and `discriminant=3^2-4(2)=1`. These exact values match the literals saved by `cycle_holonomy` and `conjugacy_invariants` (`discrete_holonomy.py:344-411`) and the default artifact.

**Falsifier:** any executable or saved product other than `[[2,2],[0,1]]`, or any characteristic invariant other than `(3,2,1)` for these literals.

### Coherent passive conjugacy

For an edge `source -> target`, the code applies

\[
\Theta'_e=A_{\mathrm{target}}^{-1}\Theta_e A_{\mathrm{source}}
\]

at `discrete_holonomy.py:590-605`, matching `Theory/02_geometry.tex:571-576`. Around a closed loop, the intermediate vertex factors cancel, leaving

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

Using the tree edges `e01`, `e12`, and `e23` rooted at vertex `0`, the exact frames constructed by `trivialization_via_spanning_tree` (`discrete_holonomy.py:458-575`) are

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

For the default operational literals at `holonomy_experiment.py:269-307`, the transported total is

\[
x=(1,0)^T+I(1,1)^T=(2,1)^T.
\]

The two event covectors give logits `(0,2)`, and the stable softmax at `discrete_holonomy.py:673-682` gives

\[
p=\left(\frac{1}{1+e^2},\frac{e^2}{1+e^2}\right),
\qquad \sum_m p_m=1.
\]

For mark values `(0,1)`, the observable is exactly `e^2/(1+e^2)`, numerically `0.8807970779778824`. Under the coherent passive transformation, the transported total becomes `(1,1)^T`, the signal covector becomes `(2,0)`, and the logits remain `(0,2)`. Thus both the normalized law and its scalar expectation are invariant for this declared construction.

**Falsifier:** a probability sum different from one, a coherent logit/observable mismatch, or acceptance by `operational_observable` of an object that is not a normalized `OperationalRecordLaw`.

### Exactly-one-link-pair broken control

The runner starts from all coherently transformed links, then replaces only `e01` and `e10` with their original inverse pair (`holonomy_experiment.py:209-213`). The saved artifact independently yields the changed oriented-label set `{'e01','e10'}` and preserves `broken_e10 @ broken_e01 = I`.

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
| Exact Session 5 allowlist | PASS | `git diff --name-only b80df01..dd13cad` contains exactly the seven Session 5 paths: two production modules, two tests, launcher, result document, and this review. Any additional tracked path is a failure. |
| Frozen fixture reachability | PASS | `_load_fixture` validates the fixture and frozen application ID before use (`holonomy_experiment.py:77-86`); `_scenario_fixture` consumes its vertices, oriented edges, and 2-cell (`:99-147`). Independent canonical hashing reproduced application ID `30a4bd...20cd` and physical SHA-256 `a207...f567`. A mismatched hash or unused replacement fixture falsifies this. |
| Scenario/group reachability | PASS | All five frozen scenarios affect edge/cell construction or scenario-specific arrays (`holonomy_experiment.py:42-49, 99-147, 336-440`); group and scenario are rejected unless exact (`:638-650`). Focused JUnit contains all five scenario cases. |
| Validation before RNG/artifacts | PASS | Type, discriminator, fixture, group, scenario, renderer, fixture identity, complex, link, frame-condition, and scenario calculations occur before RNG begins at `holonomy_experiment.py:667` and `RunStore.create` later in the same method. The general fail-fast test at `tests/test_holonomy_experiment.py:348-408` and frame-condition test at `:411-436` replace runtime seams with forbidden sentinels. Any invalid input reaching those sentinels or creating output falsifies this. |
| Frame-condition configuration reachability | PASS | Commit `54e7faaa` passes the full `NumericsConfig` into `_scenario_arrays` and tolerance-aware checks every scenario vertex frame before passive transformation (`holonomy_experiment.py:178-208`). A ceiling of `1.0` rejects vertex `0`, whose condition number is `2.0`; both 37-test fix XML files are clean and the final 38-test focused XML retains the test. Acceptance above the configured ceiling or reaching RNG/provenance/RunStore falsifies this. |
| Ordered transport and passive covariance | PASS | Source implements last-link-leftmost path composition and the endpoint-frame law (`discrete_holonomy.py:316-341, 590-605`). Exact recomputation above agrees. |
| Trivialization/cycle criterion | PASS | Tree frames, fundamental cycles, every-edge residual, and identity test are all executed at `discrete_holonomy.py:458-575`; the literal flat/nonflat test is `tests/test_discrete_holonomy.py:254-272`. |
| Normalized operational law | PASS | Stable softmax normalization and typed observable are implemented at `discrete_holonomy.py:644-725`; coherent/broken literals are pinned at `tests/test_discrete_holonomy.py:322-397`. |
| Required negative controls | PASS | The focused suite rejects a missing inverse, open-path invariants, tree plaquette curvature, raw weights, and link-only operational promotion, and proves the exactly-one-undirected-pair mutation (`tests/test_discrete_holonomy.py:185-415`; `tests/test_holonomy_experiment.py:248-290`). |
| Saved decision reconstructability | PASS | `interaction_complex.json` records rule, observed value, reference, tolerance, applicability, and component values for every metric (`holonomy_experiment.py:554-623`). I recomputed all five statuses from the saved record; all match `metrics.json`. The default NPZs reproduce the cycle, invariants, residual, laws, and changed link pair. |
| Result-status propagation | PASS | Flat tree emits an inconclusive cycle comparison and aggregate result; failure outranks inconclusive, which outranks pass (`holonomy_experiment.py:441-469, 702-709`; test `tests/test_holonomy_experiment.py:166-181`). |
| Deterministic replay | PASS | Scientific implementation commit `74a1894` is preserved in the later durable replay-evidence capture at source commit `2905cc3`; the rerun differs only in `output.root`, and all `7/7` semantic hashes and `53/53` array comparisons match. The source manifest is complete with nine files, CPU/float64 provenance, and `git_dirty=false`. Any same-code/config semantic mismatch falsifies this. |
| Sanitized launcher isolation | PASS | The launcher is no-argument and inserts its own `src` path (`run_gauge_holonomy_lab.py:8-11, 20-60`). The focused JUnit includes `tests/test_holonomy_experiment.py:467-508`, which removes Python path/home variables, uses `-I`, and asserts the loaded experiment module is from this worktree. |
| JUnit and coverage | PASS FOR LANE-FOCUSED GATE | Mechanical parsing gives `38/38` focused tests, `88.52%` line/`73.78%` branch coverage for `discrete_holonomy.py`, and `97.49%` line/`89.58%` branch coverage for `holonomy_experiment.py`, above the frozen 80% line threshold. A current XML count or module line rate below those values falsifies this record. |
| Claim-field separation | PASS | Metrics explicitly set theorem status, verification state, and origin independently (`holonomy_experiment.py:441-519`); the result remains `NUMERICAL/CANDIDATE/APPLICATION_SPECIFIC` (`:710-721`). Passing thresholds do not promote verification state. |
| Scope exclusions | PASS | The saved scope denies base-connection identification, dynamical symmetry, continuum, universality, and physical time (`holonomy_experiment.py:554-570`); provenance repeats `graph_to_base_identification=false` (`:678-687`). The result record keeps graph-to-base and operational-base holonomy `OPEN/INCONCLUSIVE`, consistent with `Theory/02_geometry.tex:625-640` and `Theory/appendix_claim_ledger.tex:243-260`. No bundle-topology claim is made. |

## Strict TDD audit

Task 1 and Task 2 reports preserve exact RED/GREEN commands, expected failure signatures, repair loops, focused JUnit paths, and commit identities. The final tests are mutation-named and exercise the defects described by the reports. Commit sequencing also shows the factory-control, artifact-reconstructability, single-pair mutation, launcher-isolation, and status-propagation fixes as separate commits.

This is a credible TDD process record. For the final immutable-boundary repair specifically, retained machine-readable RED and GREEN XML show the named mutation test failing before the repair and passing afterward, followed by clean 21-test Task 1 and 38-test Session 5 post-commit suites. Earlier RED worktree states and RED JUnit files were not retained as revision-bound machine-readable evidence, and Git history commits their tests and production together. I therefore evidence-verify the final repair loop, but accept the earlier TDD chronology only as a documented process fact rather than an independently reproducible write-order claim.

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

### C2 — Final broad regression JUnit remains pending

**Impact:** parent-owned final-integration gate; focused JUnit, coverage, and replay are refreshed.

The historical `471`-test broad JUnit predates commits `fe15a43`, `2016042`, and the final production fix `74a1894`. The lane refresh closes the focused obligations with a clean 38-test JUnit and post-fix coverage for both production modules at the scientific implementation revision. The immutable deterministic launcher/replay extract was captured later at source commit `2905cc3`, whose Session 5 production content still includes `74a1894` unchanged. No final broad-suite JUnit was part of this lane review; that separate integration obligation is recorded below.

**Resolved when:** the integration owner runs and mechanically parses the complete CPU suite at the final integration SHA. C1 separately requires the final revision-bound ledger. Any broad-suite failure, error, or unexplained skip reopens this approval.

### C3 — RED history is documented but not mechanically reproducible

**Impact:** process-audit limitation only.

The reports give specific RED failure counts and messages for the earlier lane work, but those pre-production RED states are not committed and their JUnit records are not retained. The final immutable-boundary repair is the exception: its named RED and GREEN XML are retained and mechanically parsed. This limitation therefore does not weaken the current code evidence, but an auditor cannot independently replay the exact ordering of the earlier fixes.

**Resolved when:** future lanes retain revision-bound RED artifacts or patch snapshots, or explicitly classify TDD chronology as report-only process evidence.

## Resolved and superseded findings

### R1 — RESOLVED: `max_frame_condition` is enforced by the laboratory

The earlier C4 concern was correctly reclassified as blocking and is superseded by commit `54e7faaa139f73a053c4be5463545dc4df9f780c`. `_scenario_arrays` now receives `NumericsConfig`, computes every declared vertex-frame condition number, and applies the configured ceiling with the contract tolerances before passive transformation, RNG, provenance, `RunStore.create`, or artifact publication (`holonomy_experiment.py:178-208, 638-667`).

The focused mutation test sets `max_frame_condition=1.0`, rejects vertex `0` with condition number `2.0`, forbids all three runtime seams, and proves no artifact root is created (`tests/test_holonomy_experiment.py:411-436`). Mechanical parsing of both `task-2-fix3-regression.xml` and `task-2-fix3-postcommit.xml` gives `37` tests, `0` failures, `0` errors, and `0` skipped. This resolves the configuration-reachability and fail-fast obligations for the declared scenario frames.

`min_spd_rcond` remains inapplicable because this laboratory has no SPD input. The seed reaches named-stream provenance but not scientific arrays because the declared experiment is deterministic.

### R2 — RESOLVED: canonical cells are immutable at the validation boundary

Commit `74a1894d20445f6f635f2a7bcc5f02fc8e874499` canonicalizes each cell into immutable tuple storage before `InteractionComplex` retains it (`discrete_holonomy.py:105-140`). The mutation test passes a mutable source cell, mutates it after construction, and proves both the stored boundary and holonomy result remain unchanged (`tests/test_discrete_holonomy.py:112-130`). The retained final-fix RED XML records exactly one test and one expected failure; the GREEN XML records the same test passing, and the post-commit Task 1 and Session 5 XML files record `21/21` and `38/38` clean tests. The final scoped re-review disposition is **ADDRESSED**.

### R3 — RESOLVED: complexity refactor preserves the public API and mathematics

The final repair extracts only private helpers. A no-cache Ruff C901 scan is clean for all functions in both owned Session 5 production modules. Public signatures remain intact, and the load-bearing product order remains last-link-leftmost in `open_path_transport` (`discrete_holonomy.py:316-341`); the interaction-record ordering (`holonomy_experiment.py:554-623`) and operational-law interface (`discrete_holonomy.py:685-709`) are likewise preserved. The clean focused suite, exact recomputations, refreshed coverage, and 7/7-file plus 53/53-array deterministic replay support behavioral preservation. These numerical and mechanical checks verify implementation behavior at the recorded revision; they do not prove the general mathematics.

## Final decision

**APPROVE WITH FINAL-GATE OBLIGATIONS.** The final scoped re-review disposition is **ADDRESSED**. The finite graph-link implementation, exact literal oracles, passive covariance, spanning-tree criterion, normalized operational law, isolated broken-pair control, frame-condition preflight, immutable canonical-cell boundary, public API and product ordering, artifact reconstruction, and scientific scope agree. No load-bearing code, gauge-theory, mathematical, or scientific defect remains. C1 and C2 are mandatory parent-owned final-integration gates; C3 is a report-only limitation for the earlier TDD chronology. The former C4 is resolved and superseded by `54e7faaa`; the final immutable-boundary and C901 findings are resolved by `74a1894`.
