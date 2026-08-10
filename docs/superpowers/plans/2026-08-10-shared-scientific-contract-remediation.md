# Shared Scientific Contract Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace convention-dependent scientific seams with shared typed permutation and spectral-conditioning contracts, make Session-3 controls affect run status, and emit scientifically honest candidate and boundary metadata.

**Architecture:** Two focused shared modules own finite permutations and SPD spectral classification. Existing laboratories keep independent scientific formulas, but consume those shared input and decision contracts; Session 3 publishes typed stress assessments and derives aggregate status from every required control. Historical revision-bound documents remain intact, while a new remediation result and review record supersede affected current claims.

**Tech Stack:** Python 3.14, dataclasses, `fractions.Fraction`, NumPy, SciPy, pytest, pytest-cov, JUnit XML, JSON/NPZ run artifacts, Git.

## Global Constraints

- Work only in the isolated `codex/shared-scientific-contracts-20260810` worktree based on `d38f24ca506dd37fd74dacd8d2abab3c3175bdc9`.
- Preserve the user's Desktop checkout and its modified launchers, untracked review directory, and `uv.lock` exactly.
- Use American English in code, tests, comments, commits, and documents.
- Use `C:\Python314\python.exe` for CPU tests; make no CUDA claim and do not add a CUDA lane.
- Store permutations canonically as `old_to_new`; derive `new_to_old`; do not pass unlabeled permutation tuples inside production code.
- Establish exact rational symmetry and positive definiteness before floating spectral conditioning.
- Define reciprocal conditioning as `lambda_min / lambda_max` for a symmetric positive-definite matrix.
- Classify `abs(rcond - threshold) <= atol + rtol * abs(threshold)` as `inconclusive`.
- Keep determinant-volume diagnostics separately named and never use them for conditioning acceptance.
- Make `min_spd_rcond`, `atol`, and `rtol` reach Session-3 decisions; serialize `max_frame_condition` as `not_applicable` there.
- A failed required stress check yields run status `fail`; an inconclusive required check yields `inconclusive` unless another required check fails.
- Producer-generated scientific records use `verification_state="CANDIDATE"`; only a validated final-revision ledger may promote a claim.
- Assumption-boundary witnesses use `inside_declared_domain=false`, `assumptions_satisfied=false`, and `classification="assumption_boundary"`.
- Do not add artifact tamper detection, Git-provenance hardening, registry refactors, performance work, continuum claims, or Gaussian heavy sweeps.
- Every production change follows red-green-refactor and ends with a focused test run and a small commit.

---

## File Responsibility Map

- Create `src/multiagent_elbo/finite/permutations.py`: canonical finite permutation type, validation, inverse/composition, and law/channel/tensor pullbacks.
- Modify `src/multiagent_elbo/geometry/finite_gauge.py`: import and use the shared permutation type; retain geometry behavior without a second convention.
- Modify `src/multiagent_elbo/geometry/__init__.py` and `src/multiagent_elbo/finite/__init__.py`: compatibility re-exports.
- Modify `src/multiagent_elbo/finite/counterexamples.py`: typed relabeling, canonical projection residual, exact SPD membership, and candidate boundary records.
- Create `src/multiagent_elbo/conditioning.py`: typed spectral reciprocal-condition assessment.
- Modify `src/multiagent_elbo/realizations/gaussian/interactions.py`: use the shared spectral decision after existing symmetry and Cholesky validation.
- Modify `src/multiagent_elbo/finite/counterexample_experiment.py`: effective numerical policy, measured stress records, status aggregation, and candidate metadata.
- Modify applicable `*_experiment.py` producers under `src/multiagent_elbo/finite/`, `src/multiagent_elbo/geometry/`, and `src/multiagent_elbo/realizations/gaussian/`: stop self-promoting new records to `EVIDENCE_VERIFIED`.
- Modify focused tests under `tests/`: literal three-cycle oracles, cross-producer metamorphics, SPD reversals, config reachability, stress gating, and metadata boundaries.
- Create `docs/results/2026-08-10-shared-scientific-contract-remediation-results.md`: current-revision results and supersession statement.
- Create `docs/verification/reviews/2026-08-10-shared-scientific-contract-remediation-review.md`: independent scientific review record.
- Create ignored `.verification/shared-scientific-contract-remediation/ledger.json`: final-SHA verification ledger generated only after code and docs are fixed.

### Task 1: Canonical Finite Permutations

**Files:**
- Create: `src/multiagent_elbo/finite/permutations.py`
- Modify: `src/multiagent_elbo/finite/__init__.py`
- Modify: `src/multiagent_elbo/geometry/finite_gauge.py:1-120`
- Modify: `src/multiagent_elbo/geometry/__init__.py:1-30`
- Test: `tests/test_finite_permutations.py`
- Test: `tests/test_finite_experiment.py:1-180`

**Interfaces:**
- Produces: `FinitePermutation.from_old_to_new(old_to_new: Sequence[int]) -> FinitePermutation`.
- Produces: `FinitePermutation.from_matrix(matrix: Sequence[Sequence[float]]) -> FinitePermutation` for the existing matrix-facing geometry seam.
- Produces: properties `size: int`, `new_to_old: tuple[int, ...]`, and `matrix: np.ndarray`.
- Produces: `inverse() -> FinitePermutation` and `then(after: FinitePermutation) -> FinitePermutation`, where `p.then(q)` means apply `p`, then `q`.
- Produces: `pullback_axis(values: object, axis: int = 0) -> np.ndarray`, `pullback_law(values: Sequence[object]) -> tuple[object, ...]`, and `pullback_channel(rows, target_permutation)`.
- Preserves: `from multiagent_elbo.geometry import FinitePermutation` and `from multiagent_elbo.geometry.finite_gauge import FinitePermutation`.

- [ ] **Step 1: Write failing constructor, three-cycle, group-law, and compatibility tests**

```python
def test_three_cycle_has_one_canonical_direction_and_explicit_inverse():
    cycle = FinitePermutation.from_old_to_new((1, 2, 0))
    assert cycle.old_to_new == (1, 2, 0)
    assert cycle.new_to_old == (2, 0, 1)
    assert cycle.pullback_law((Fraction(1, 5), Fraction(3, 10), Fraction(1, 2))) == (
        Fraction(1, 2), Fraction(1, 5), Fraction(3, 10)
    )
    assert cycle.then(cycle.inverse()).old_to_new == (0, 1, 2)


def test_composition_matches_sequential_pullback():
    p = FinitePermutation.from_old_to_new((1, 2, 0))
    q = FinitePermutation.from_old_to_new((2, 0, 1))
    values = np.arange(9).reshape(3, 3)
    np.testing.assert_array_equal(
        p.then(q).pullback_axis(values, axis=0),
        q.pullback_axis(p.pullback_axis(values, axis=0), axis=0),
    )


def test_geometry_matrix_adapter_builds_the_same_permutation():
    matrix = ((0, 1, 0), (0, 0, 1), (1, 0, 0))
    assert FinitePermutation.from_matrix(matrix) == FinitePermutation.from_old_to_new(
        (1, 2, 0)
    )
```

- [ ] **Step 2: Run the new tests and verify the missing module/API failure**

Run: `C:\Python314\python.exe -m pytest tests/test_finite_permutations.py tests/test_finite_experiment.py -q --basetemp=.pytest-tmp/task1-red`

Expected: FAIL during import because `multiagent_elbo.finite.permutations` and the named constructors do not exist.

- [ ] **Step 3: Implement the immutable permutation type and migrate finite-gauge**

```python
@dataclass(frozen=True)
class FinitePermutation:
    old_to_new: tuple[int, ...]

    @classmethod
    def from_old_to_new(cls, old_to_new: Sequence[int]) -> "FinitePermutation":
        values = tuple(old_to_new)
        if not values:
            raise ValueError("old_to_new permutation must be nonempty")
        if any(type(value) is not int for value in values):
            raise TypeError("old_to_new entries must be ints")
        if sorted(values) != list(range(len(values))):
            raise ValueError("old_to_new must be a bijection over 0..n-1")
        return cls(values)

    @property
    def new_to_old(self) -> tuple[int, ...]:
        inverse = [0] * self.size
        for old, new in enumerate(self.old_to_new):
            inverse[new] = old
        return tuple(inverse)

    def pullback_axis(self, values: object, axis: int = 0) -> np.ndarray:
        return np.take(np.asarray(values), self.new_to_old, axis=axis)
```

Move matrix construction, composition, inverse, read-only matrix materialization, and channel pullback into this module. Replace `_pull_axis` in `finite_gauge.py` with `permutation.pullback_axis(...)`; do not retain the old local dataclass.

- [ ] **Step 4: Run permutation and finite-gauge tests**

Run: `C:\Python314\python.exe -m pytest tests/test_finite_permutations.py tests/test_finite_experiment.py -q --basetemp=.pytest-tmp/task1-green`

Expected: PASS, including the non-involutive cycle, composition, inverse, matrix adapter, and existing swap behavior.

- [ ] **Step 5: Commit the canonical permutation contract**

```powershell
git add src/multiagent_elbo/finite/permutations.py src/multiagent_elbo/finite/__init__.py src/multiagent_elbo/geometry/finite_gauge.py src/multiagent_elbo/geometry/__init__.py tests/test_finite_permutations.py tests/test_finite_experiment.py
git commit -m "refactor: unify finite permutation convention"
```

### Task 2: Typed Session-3 Relabeling and Projection Residuals

**Files:**
- Modify: `src/multiagent_elbo/finite/counterexamples.py:82-120,286-382`
- Modify: `src/multiagent_elbo/finite/counterexample_experiment.py:140-380`
- Test: `tests/test_counterexamples.py:60-180`
- Test: `tests/test_counterexample_experiment.py:360-430`

**Interfaces:**
- Consumes: `FinitePermutation` from Task 1.
- Changes: `ExactAction.relabel(axis_permutations: Sequence[FinitePermutation]) -> ExactAction`.
- Changes: `relabel_law(law: ExactLaw, permutation: FinitePermutation) -> ExactLaw`.
- Changes: `relabel_channel(channel: ExactChannel, source_permutation: FinitePermutation, target_permutation: FinitePermutation) -> ExactChannel`.
- Produces: `retained_projection_residual(action, transformed_action, axis_permutations, retained_order) -> Fraction`.
- Removes: `pairwise_interaction_residual`, whose sum-of-component-suprema does not equal the canonical omitted-action sup norm.

- [ ] **Step 1: Write failing three-cycle cross-producer and residual-oracle tests**

```python
def test_three_cycle_matches_geometry_pullback_for_law_channel_and_action():
    cycle = FinitePermutation.from_old_to_new((1, 2, 0))
    law = ExactLaw((Fraction(1, 5), Fraction(3, 10), Fraction(1, 2)))
    channel = ExactChannel(((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    action = ExactAction((3,), (Fraction(2), Fraction(3), Fraction(5)))
    assert relabel_law(law, cycle).masses == tuple(cycle.pullback_law(law.masses))
    assert relabel_channel(channel, cycle, cycle).rows == tuple(
        tuple(row) for row in cycle.pullback_channel(channel.rows, cycle)
    )
    assert action.relabel((cycle,)).values == tuple(cycle.pullback_law(action.values))


def test_projection_residual_is_the_canonical_omitted_action_sup_norm():
    action = ExactAction((2, 2, 2, 2), FOUR_AXIS_LITERAL_VALUES)
    projection = project_action(hoeffding_decompose_action(action), retained_order=1)
    assert projection.residual == Fraction(17, 16)
    assert retained_projection_residual(
        action, action.relabel((SWAP, IDENTITY, IDENTITY, IDENTITY)),
        (SWAP, IDENTITY, IDENTITY, IDENTITY), 1
    ) == 0
```

Define `FOUR_AXIS_LITERAL_VALUES` as the exact tuple `(0, 0, -1, 0, 1, 0, 0, 0, 0, 0, 1, -1, 1, -1, 0, -1)` and define `SWAP` and `IDENTITY` as typed literal permutation fixtures. This regression must not invoke the production decomposition to construct its expected `17/16` value. The old component-sup helper returns `25/16` for this witness at retained order one.

- [ ] **Step 2: Run focused tests and verify the convention and 25/16 residual failures**

Run: `C:\Python314\python.exe -m pytest tests/test_counterexamples.py tests/test_counterexample_experiment.py -q --basetemp=.pytest-tmp/task2-red`

Expected: FAIL because Session 3 accepts raw tuples in the inverse convention and the orphan residual helper returns `25/16` for the pinned four-axis witness.

- [ ] **Step 3: Migrate every Session-3 relabeling call to typed permutations**

```python
def relabel_law(law: ExactLaw, permutation: FinitePermutation) -> ExactLaw:
    _require_permutation_size(permutation, len(law.masses), "law")
    return ExactLaw(permutation.pullback_law(law.masses))


def retained_projection_residual(
    action: ExactAction,
    transformed_action: ExactAction,
    axis_permutations: Sequence[FinitePermutation],
    retained_order: int,
) -> Fraction:
    original = project_action(hoeffding_decompose_action(action), retained_order)
    transformed = project_action(
        hoeffding_decompose_action(transformed_action), retained_order
    )
    expected = original.retained.relabel(axis_permutations)
    return max(
        abs(left - right)
        for left, right in zip(transformed.retained.values, expected.values)
    )
```

Use `FinitePermutation.from_old_to_new((1, 0))` at the catalog boundary. Store `old_to_new` in artifacts. Replace the literal stress residual with the measured exact residual returned above.

- [ ] **Step 4: Run Session-3 and finite-gauge focused tests**

Run: `C:\Python314\python.exe -m pytest tests/test_finite_permutations.py tests/test_finite_experiment.py tests/test_counterexamples.py tests/test_counterexample_experiment.py -q --basetemp=.pytest-tmp/task2-green`

Expected: PASS; the three-cycle cross-producer oracle must fail if either convention is locally reversed.

- [ ] **Step 5: Commit typed Session-3 relabeling**

```powershell
git add src/multiagent_elbo/finite/counterexamples.py src/multiagent_elbo/finite/counterexample_experiment.py tests/test_counterexamples.py tests/test_counterexample_experiment.py
git commit -m "fix: type finite relabeling and projection residuals"
```

### Task 3: Shared Spectral SPD Conditioning

**Files:**
- Create: `src/multiagent_elbo/conditioning.py`
- Modify: `src/multiagent_elbo/finite/counterexamples.py:480-535`
- Modify: `src/multiagent_elbo/realizations/gaussian/interactions.py:20-75`
- Test: `tests/test_conditioning.py`
- Test: `tests/test_counterexamples.py:180-250`
- Test: `tests/test_gaussian_realization.py:120-210`

**Interfaces:**
- Produces: `ConditioningDecision = Literal["pass", "fail", "inconclusive"]`.
- Produces: frozen `SpectralConditioningAssessment(minimum_eigenvalue, maximum_eigenvalue, reciprocal_condition, threshold, boundary_tolerance, method, decision, reason)`.
- Produces: `assess_spectral_spd(matrix: object, *, min_rcond: float, atol: float, rtol: float) -> SpectralConditioningAssessment`.
- Changes: `validate_full_rank_spd(matrix, *, min_rcond, atol, rtol) -> SpectralConditioningAssessment`; it still performs exact Sylvester membership first.
- Preserves: Gaussian `_validate_spd(...) -> tuple[np.ndarray, float, float]`, translating shared `fail` and `inconclusive` decisions into `GaussianNumericalError` messages.

- [ ] **Step 1: Write failing decision-reversal and boundary tests**

```python
def test_spectral_policy_rejects_correlated_matrix_old_proxy_false_accepted():
    matrix = np.array([[1.0, 1.0 - 1.0e-12], [1.0 - 1.0e-12, 1.0]])
    result = assess_spectral_spd(
        matrix, min_rcond=1.0e-12, atol=0.0, rtol=0.0
    )
    assert result.decision == "fail"
    assert result.reciprocal_condition < 1.0e-12


def test_spectral_policy_accepts_repeated_small_diagonal_old_proxy_false_rejected():
    result = assess_spectral_spd(
        np.diag([1.0, 1.0e-7, 1.0e-7]),
        min_rcond=1.0e-12,
        atol=0.0,
        rtol=0.0,
    )
    assert result.decision == "pass"
    assert result.reciprocal_condition == pytest.approx(1.0e-7)


def test_threshold_band_is_inconclusive_and_tolerances_are_reachable():
    matrix = np.diag([1.0, 1.05e-6])
    assert assess_spectral_spd(
        matrix, min_rcond=1.0e-6, atol=0.0, rtol=0.0
    ).decision == "pass"
    assert assess_spectral_spd(
        matrix, min_rcond=1.0e-6, atol=1.0e-7, rtol=0.0
    ).decision == "inconclusive"
    assert assess_spectral_spd(
        matrix, min_rcond=1.0e-6, atol=0.0, rtol=0.1
    ).decision == "inconclusive"
```

- [ ] **Step 2: Run conditioning tests and verify the missing shared policy failure**

Run: `C:\Python314\python.exe -m pytest tests/test_conditioning.py tests/test_counterexamples.py tests/test_gaussian_realization.py -q --basetemp=.pytest-tmp/task3-red`

Expected: FAIL because the shared assessment does not exist and the exact finite path still uses determinant/diagonal proxies.

- [ ] **Step 3: Implement spectral assessment and adapt both producers**

```python
@dataclass(frozen=True)
class SpectralConditioningAssessment:
    minimum_eigenvalue: float
    maximum_eigenvalue: float
    reciprocal_condition: float
    threshold: float
    boundary_tolerance: float
    method: Literal["symmetric_eigenvalue_ratio"]
    decision: ConditioningDecision
    reason: str


def assess_spectral_spd(matrix: object, *, min_rcond: float, atol: float, rtol: float) -> SpectralConditioningAssessment:
    values = np.asarray(matrix, dtype=np.float64)
    eigenvalues = scipy.linalg.eigvalsh(values, check_finite=True)
    minimum = float(eigenvalues[0])
    maximum = float(eigenvalues[-1])
    rcond = minimum / maximum
    band = atol + rtol * abs(min_rcond)
    if abs(rcond - min_rcond) <= band:
        decision = "inconclusive"
    elif rcond < min_rcond:
        decision = "fail"
    else:
        decision = "pass"
    return SpectralConditioningAssessment(
        minimum, maximum, rcond, min_rcond, band,
        "symmetric_eigenvalue_ratio", decision,
        _conditioning_reason(decision),
    )
```

Validate finite numeric inputs and positive eigenvalues explicitly. In `counterexamples.py`, retain exact square/symmetry/Sylvester checks before converting to float and calling this function. Rename `diagonal_spd_conditioning` to `diagonal_spd_condition_number` and retain it only as a diagnostic.

- [ ] **Step 4: Run shared, finite, and Gaussian conditioning tests**

Run: `C:\Python314\python.exe -m pytest tests/test_conditioning.py tests/test_counterexamples.py tests/test_gaussian_realization.py -q --basetemp=.pytest-tmp/task3-green`

Expected: PASS; both old decision reversals are corrected, and Gaussian and exact-finite paths agree on the common matrices.

- [ ] **Step 5: Run module coverage and commit**

Run: `C:\Python314\python.exe -m pytest tests/test_conditioning.py tests/test_finite_permutations.py --cov=multiagent_elbo.conditioning --cov=multiagent_elbo.finite.permutations --cov-report=term-missing --cov-fail-under=80 -q --basetemp=.pytest-tmp/task3-coverage`

Expected: PASS with at least 80 percent line coverage for both new modules.

```powershell
git add src/multiagent_elbo/conditioning.py src/multiagent_elbo/finite/counterexamples.py src/multiagent_elbo/realizations/gaussian/interactions.py tests/test_conditioning.py tests/test_counterexamples.py tests/test_gaussian_realization.py
git commit -m "fix: share spectral SPD conditioning policy"
```

### Task 4: Effective Session-3 Policy and Status-Bearing Stress Controls

**Files:**
- Modify: `src/multiagent_elbo/finite/counterexample_experiment.py:50-490`
- Test: `tests/test_counterexample_experiment.py:1-500`

**Interfaces:**
- Consumes: `SpectralConditioningAssessment` and typed relabeling residuals from Tasks 2-3.
- Produces: frozen `StressAssessment(name, value, tolerance, status, expected, interpretation)`.
- Changes: `_catalog(config)` returns primary metrics plus `Mapping[str, StressAssessment]`.
- Produces: `_aggregate_status(metrics, stress) -> Literal["pass", "fail", "inconclusive"]` with failure precedence over inconclusive.
- Serializes: `numerical_policy.requested`, `numerical_policy.effective`, and `numerical_policy.not_applicable` in `stress_matrix.json`.

- [ ] **Step 1: Write failing config-reachability and stress-gating tests**

```python
def test_session3_numerical_policy_is_serialized_and_reaches_conditioning(tmp_path):
    passing = run_finite_counterexample_experiment(
        experiment_config(tmp_path / "pass", min_spd_rcond=1.0e-99, atol=0.0, rtol=0.0)
    )
    failing = run_finite_counterexample_experiment(
        experiment_config(tmp_path / "fail", min_spd_rcond=1.0e-101, atol=0.0, rtol=0.0)
    )
    assert passing.status == "pass"
    assert failing.status == "fail"
    stress = json.loads((failing.run_dir / "stress_matrix.json").read_text("utf-8"))
    assert stress["numerical_policy"]["requested"]["min_spd_rcond"] == 1.0e-101
    assert stress["numerical_policy"]["not_applicable"]["max_frame_condition"] == 1.0e6


def test_required_relabel_failure_prevents_pass(monkeypatch, tmp_path):
    monkeypatch.setattr(counterexample_experiment, "retained_projection_residual", lambda *args, **kwargs: Fraction(1))
    result = run_finite_counterexample_experiment(experiment_config(tmp_path))
    assert result.status == "fail"


def test_near_threshold_conditioning_is_inconclusive(tmp_path):
    result = run_finite_counterexample_experiment(
        experiment_config(tmp_path, min_spd_rcond=1.0e-100, atol=1.0e-101, rtol=0.0)
    )
    assert result.status == "inconclusive"
```

Also add one mutation test per required control: deep composition, relabeling, retained-space negative control, and conditioning. Each mutation must change aggregate status.

- [ ] **Step 2: Run experiment tests and verify that config and stress are currently inert**

Run: `C:\Python314\python.exe -m pytest tests/test_counterexample_experiment.py -q --basetemp=.pytest-tmp/task4-red`

Expected: FAIL because the producer hardcodes `1e-12`, serializes a literal relabel residual, and aggregates only primary metrics.

- [ ] **Step 3: Implement typed stress assessments and aggregate status**

```python
@dataclass(frozen=True)
class StressAssessment:
    name: str
    value: str
    tolerance: str
    status: MetricStatus
    expected: str
    interpretation: str


def _aggregate_status(
    metrics: Mapping[str, MetricRecord],
    stress: Mapping[str, StressAssessment],
) -> MetricStatus:
    statuses = [record.status for record in metrics.values()]
    statuses.extend(record.status for record in stress.values())
    if "fail" in statuses:
        return "fail"
    if "inconclusive" in statuses:
        return "inconclusive"
    return "pass"
```

Use `config.numerics.atol`, `config.numerics.rtol`, and `config.numerics.min_spd_rcond` at every advertised floating decision. Preserve exact zero comparisons for exact rational composition/projection checks. Define negative-control success positively: retained-space passes only when the omitted residual is strictly positive; near-singular rejection passes only when the shared spectral decision is `fail` for the recorded threshold.

- [ ] **Step 4: Run Session-3 experiment tests and artifact replay assertions**

Run: `C:\Python314\python.exe -m pytest tests/test_counterexample_experiment.py tests/test_counterexamples.py -q --basetemp=.pytest-tmp/task4-green --junitxml=.pytest-tmp/task4-focused.xml`

Expected: PASS, and the JUnit XML must report zero failures and zero errors.

- [ ] **Step 5: Commit policy and status reachability**

```powershell
git add src/multiagent_elbo/finite/counterexample_experiment.py tests/test_counterexample_experiment.py
git commit -m "fix: gate Session 3 on effective stress policy"
```

### Task 5: Candidate-Only Producer Metadata and Honest Boundaries

**Files:**
- Modify: `src/multiagent_elbo/finite/counterexamples.py:150-190,430-480`
- Modify: `src/multiagent_elbo/finite/counterexample_experiment.py:70-210`
- Modify: producer call sites returned by `rg -l 'verification_state="EVIDENCE_VERIFIED"' src/multiagent_elbo --glob '*experiment.py'`
- Modify: the matching focused experiment tests returned by `rg -l 'EVIDENCE_VERIFIED' tests --glob 'test_*experiment.py'`
- Test: `tests/test_experiment_support.py`
- Test: `tests/test_counterexample_experiment.py`

**Interfaces:**
- Consumes: existing `MetricRecord.verification_state` and `CandidateRecord.verification_state` enums.
- Establishes: producer output uses `CANDIDATE`; `INCONCLUSIVE` remains valid for unresolved applicability or unavailable evidence.
- Establishes: support-violating KL candidates are assumption-boundary records, not in-domain catalog successes.
- Does not change: `theorem_status`, `claim_origin`, metric runtime `status`, or historical revision-bound documentation.

- [ ] **Step 1: Write failing producer and boundary metadata tests**

```python
def test_generated_session3_records_are_candidates_and_support_failures_are_boundaries(tmp_path):
    result = run_finite_counterexample_experiment(experiment_config(tmp_path))
    assert {metric.verification_state for metric in result.metrics.values()} == {"CANDIDATE"}
    records = json.loads((result.run_dir / "candidate_records.json").read_text("utf-8"))
    assert {record["verification_state"] for record in records} == {"CANDIDATE"}
    support = [record for record in records if record["claim_id"] == "support_boundary"]
    assert support
    assert all(record["inside_declared_domain"] is False for record in support)
    assert all(record["assumptions_satisfied"] is False for record in support)
    assert all(record["classification"] == "assumption_boundary" for record in support)


@pytest.mark.parametrize("runner,config_factory", ALL_LAB_RUNNERS)
def test_laboratory_producers_do_not_self_promote(runner, config_factory, tmp_path):
    result = runner(config_factory(tmp_path))
    assert all(
        metric.verification_state != "EVIDENCE_VERIFIED"
        for metric in result.metrics.values()
    )
```

Build `ALL_LAB_RUNNERS` from explicit imports and literal pairs in the test; do not discover producers dynamically at runtime.

- [ ] **Step 2: Run metadata-focused tests and verify current self-promotion failures**

Run: `C:\Python314\python.exe -m pytest tests/test_experiment_support.py tests/test_counterexample_experiment.py tests/test_agent_network_experiment.py tests/test_attention_experiment.py tests/test_categorical_dqm_experiment.py tests/test_information_history_experiment.py tests/test_scale_cocycle_experiment.py tests/test_theory_oracle_experiment.py tests/test_holonomy_experiment.py tests/test_gaussian_fixed_ray_experiment.py -q --basetemp=.pytest-tmp/task5-red`

Expected: FAIL at each producer still emitting `EVIDENCE_VERIFIED`, and at the support-boundary records currently marked inside-domain.

- [ ] **Step 3: Replace producer-issued promotion with candidate states**

```python
return target_metric(
    value,
    tolerance,
    target=target,
    interpretation=interpretation,
    theorem_status=theorem_status,
    verification_state="CANDIDATE",
    claim_origin=claim_origin,
)
```

Apply this only at artifact-producing experiment seams. Keep explicitly inconclusive records inconclusive. Change `parameter_dependent_channel_witness` and `_record` defaults to `CANDIDATE`. Correct support violations to `inside=False`, `assumptions=False`, `classification="assumption_boundary"`, and include an applicability explanation naming the absolute-continuity premise.

- [ ] **Step 4: Run all metadata-focused tests**

Run: `C:\Python314\python.exe -m pytest tests/test_experiment_support.py tests/test_counterexample_experiment.py tests/test_agent_network_experiment.py tests/test_attention_experiment.py tests/test_categorical_dqm_experiment.py tests/test_information_history_experiment.py tests/test_scale_cocycle_experiment.py tests/test_theory_oracle_experiment.py tests/test_holonomy_experiment.py tests/test_gaussian_fixed_ray_experiment.py -q --basetemp=.pytest-tmp/task5-green`

Expected: PASS; no newly emitted producer metric or candidate record self-promotes to `EVIDENCE_VERIFIED`.

- [ ] **Step 5: Commit metadata remediation**

```powershell
git add src/multiagent_elbo tests
git diff --cached --check
git commit -m "fix: reserve evidence verification for ledgers"
```

Before committing, inspect `git diff --cached --name-only` and unstage any path unrelated to the explicit producer/test list.

### Task 6: Cross-Producer Mutation Matrix and Complete CPU Regression

**Files:**
- Create: `tests/test_shared_scientific_contracts.py`
- Modify: production files only if a test exposes a contract defect; repeat red-green before each fix.

**Interfaces:**
- Consumes: canonical permutations, spectral conditioning, Session-3 status aggregation, and candidate metadata from Tasks 1-5.
- Produces: one integration-level regression file with independent literal oracles and pinned mutations.

- [ ] **Step 1: Add the complete independent contract matrix**

```python
def test_same_three_cycle_agrees_across_exact_and_geometry_producers():
    cycle = FinitePermutation.from_old_to_new((1, 2, 0))
    masses = (Fraction(1, 5), Fraction(3, 10), Fraction(1, 2))
    expected = (Fraction(1, 2), Fraction(1, 5), Fraction(3, 10))
    assert relabel_law(ExactLaw(masses), cycle).masses == expected
    np.testing.assert_allclose(cycle.pullback_axis(np.asarray(masses, float)), expected)


def test_inverse_convention_mutation_is_detected():
    cycle = FinitePermutation.from_old_to_new((1, 2, 0))
    values = np.array([0.2, 0.3, 0.5])
    correct = cycle.pullback_axis(values)
    mutated = np.take(values, cycle.old_to_new)
    assert np.max(np.abs(correct - mutated)) == pytest.approx(0.3)


def test_determinant_proxy_mutations_reverse_both_required_spd_cases():
    correlated = np.array([[1.0, 1.0 - 1.0e-12], [1.0 - 1.0e-12, 1.0]])
    repeated = np.diag([1.0, 1.0e-7, 1.0e-7])
    assert determinant_volume_proxy(correlated) < 1.0e12
    assert assess_spectral_spd(correlated, min_rcond=1e-12, atol=0.0, rtol=0.0).decision == "fail"
    assert determinant_volume_proxy(repeated) > 1.0e12
    assert assess_spectral_spd(repeated, min_rcond=1e-12, atol=0.0, rtol=0.0).decision == "pass"
```

Define `determinant_volume_proxy` inside the test only; it is a pinned negative-control mutation, not production code. Add explicit tests for composition/inverse, Gaussian-vs-finite decision equality, stress-failure aggregation, tolerance-band inconclusive status, and boundary metadata.

- [ ] **Step 2: Run the integration matrix**

Run: `C:\Python314\python.exe -m pytest tests/test_shared_scientific_contracts.py -q --basetemp=.pytest-tmp/task6-contracts --junitxml=.pytest-tmp/task6-contracts.xml`

Expected: PASS with zero failures/errors and every mutation distinguished from the corrected path.

- [ ] **Step 3: Run the complete CPU suite with machine-readable output**

Run: `C:\Python314\python.exe -m pytest -m "not cuda" -q --basetemp=.pytest-tmp/task6-full --junitxml=.pytest-tmp/task6-full.xml`

Expected: PASS. Parse `.pytest-tmp/task6-full.xml` and record exact collected, passed, skipped, failure, error, and elapsed-time values; do not copy counts from console progress.

- [ ] **Step 4: Run focused coverage for the new modules**

Run: `C:\Python314\python.exe -m pytest tests/test_conditioning.py tests/test_finite_permutations.py tests/test_shared_scientific_contracts.py --cov=multiagent_elbo.conditioning --cov=multiagent_elbo.finite.permutations --cov-branch --cov-report=term-missing --cov-report=xml:.pytest-tmp/task6-coverage.xml --cov-fail-under=80 -q --basetemp=.pytest-tmp/task6-coverage`

Expected: PASS and at least 80 percent line coverage for each new production module. Remove only a root `.coverage` file created by this command after confirming its exact path; retain the XML under ignored `.pytest-tmp`.

- [ ] **Step 5: Commit the integration matrix**

```powershell
git add tests/test_shared_scientific_contracts.py
git diff --cached --check
git commit -m "test: enforce shared scientific contracts"
```

### Task 7: Reproduce Artifacts, Document Supersession, and Validate the Final Ledger

**Files:**
- Create: `docs/results/2026-08-10-shared-scientific-contract-remediation-results.md`
- Create: `docs/verification/reviews/2026-08-10-shared-scientific-contract-remediation-review.md`
- Modify: `docs/results/2026-08-10-six-session-integration-results.md`
- Create ignored: `.verification/shared-scientific-contract-remediation/ledger.json`
- Create ignored: `.verification/shared-scientific-contract-remediation/report.md`

**Interfaces:**
- Consumes: the final code SHA and Task-6 JUnit/coverage outputs.
- Produces: a revision-bound result record, independent review, and validated claim ledger.
- Does not modify: historical result/review files whose recorded revisions predate this remediation.

- [ ] **Step 1: Reproduce the no-argument Session-3 bundle twice from clean output roots**

Run: `C:\Python314\python.exe run_finite_counterexample_lab.py`

Then rerun with only the output root changed to a second temporary root. Compare `metrics.json`, `enumeration_bounds.json`, `candidate_records.json`, `minimal_witnesses.json`, `stress_matrix.json`, and exact rational NPZ numerator/denominator arrays semantically. Record current hashes, catalog count, minimal witnesses, measured relabel residual, spectral assessment fields, numerical policy, and aggregate status.

- [ ] **Step 2: Write the current-revision result document**

```markdown
## Scientific closure

| Contract | Current result | Evidence boundary |
|---|---:|---|
| Three-cycle relabeling | exact residual `0` | finite typed permutation only |
| Correlated SPD control | `fail` | spectral reciprocal condition |
| Repeated-small-diagonal SPD control | `pass` | spectral reciprocal condition |
| Producer verification state | `CANDIDATE` | ledger promotion is external |

The prior Session-3 artifact bundle remains a historical revision-bound record. This document supersedes its current scientific-contract interpretation; it does not rewrite the historical bytes or claim a continuum, CUDA, or security result.
```

Populate the table with reproduced exact values and the final code SHA. Include requested/effective Session-3 policy and the two corrected old-proxy reversals.

- [ ] **Step 3: Perform and write an independent scientific review**

The review must independently reconstruct the three-cycle oracle, both SPD decisions, stress aggregation, support-boundary flags, and producer candidate states from source plus generated artifacts. It must state `APPROVED`, `REJECTED`, or `INCONCLUSIVE`, list any residual Important issue, and identify the exact revision reviewed.

- [ ] **Step 4: Commit documentation and fix the final SHA**

```powershell
git add docs/results/2026-08-10-shared-scientific-contract-remediation-results.md docs/verification/reviews/2026-08-10-shared-scientific-contract-remediation-review.md docs/results/2026-08-10-six-session-integration-results.md
git diff --cached --check
git commit -m "docs: record shared scientific contract remediation"
```

- [ ] **Step 5: Create and validate the final-SHA verification ledger**

Use the installed `verification` skill. Record one claim per check for:

1. canonical three-cycle and group laws;
2. shared spectral decisions and exact SPD membership ordering;
3. `min_spd_rcond`, `atol`, and `rtol` reachability;
4. required stress gating;
5. candidate-only producer metadata and assumption-boundary flags;
6. focused module coverage;
7. complete CPU JUnit closure;
8. deterministic semantic replay;
9. allowlisted tracked paths and preserved Desktop WIP.

Each closed code/experiment claim must cite current mechanical evidence bound to the final SHA. Mathematical claims must cite a literal derivation or exact oracle. Validate the ledger before reporting closure; unresolved eligible evidence yields `INCONCLUSIVE`, not promotion by consensus.

- [ ] **Step 6: Final repository checks**

Run:

```powershell
git diff --check origin/main...HEAD
git status --short
git log --oneline --decorate -8
git diff --name-only origin/main...HEAD
```

Expected: clean isolated worktree; only plan/spec, shared scientific modules, their direct producers/tests, and the new remediation documentation differ from `origin/main`. Confirm the Desktop checkout still has exactly its original protected WIP paths.

If the ledger is valid and the review is approved, follow `superpowers:finishing-a-development-branch` for the user-authorized commit/push/merge/fast-forward lifecycle. If any scientific claim remains inconclusive, stop before merge and report the precise open obligation.
