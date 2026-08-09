# Attention and Categorical-DQM Laboratories Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add no-CLI click-to-run attention and genuinely parameterized categorical-DQM laboratories with exact finite oracles, immutable artifacts, saved-artifact figures, and evidence-gated verification.

**Architecture:** A shared discriminated configuration and renderer-validation layer supports two independent finite mathematical cores. Attention transports the normalized state/receiver/source joint law before disintegration and separately recomputes scalar attention from gauge-covariant inputs; categorical DQM uses a positive finite exponential family, independent finite differences, and the existing fixed-kernel Fisher decomposition. Each experiment finalizes numerical artifacts before optional pure rendering.

**Tech Stack:** Python 3.14, NumPy float64, SciPy where already required, Matplotlib Agg, pytest 9, JSON/NPZ artifact bundles, Git-backed provenance.

## Global Constraints

- Work only in `C:\tmp\MultiAgentELBO-attention-dqm-20260809` on `codex/attention-dqm-labs-20260809`; preserve both existing live checkouts and their unrelated WIP.
- The application exposes no CLI. Launchers contain editable `RUN`, `THEORY`, `NUMERICS`, and `OUTPUT` dictionaries, a thin `main()`, an adjacent-`src` bootstrap, and no import-time run.
- Use `C:\Python314\python.exe`; this feature has no Torch or CUDA path.
- Follow strict red-green-refactor TDD. Every production behavior must first have a test that fails for the expected missing-behavior reason and uses independent literal expectations.
- All numerical arrays are float64, defensively copied, finite, and read-only at public boundaries. Masks are defensive read-only Boolean arrays.
- Attention pushes `gamma(y,i,j) = mu(y) eta(y,i,j)` through the state and node kernels before conditional disintegration. It never coarse-grains `beta` as the correct operation.
- The gauge check recomputes invariant contractions under matched local `GL+(2)` frame actions. Finite label permutation remains separately named relabeling naturality.
- The DQM channel is a concrete normalized `MarkovKernel` declared fixed and parameter-independent. The code must not claim that this assumption is mechanically verified across a channel family.
- Default rational-oracle and monotonic-ladder pass/fail metrics apply only to the preregistered default fixture and theta. Edited theta values retain generic identity checks and diagnostic controls.
- `metrics.json` keeps the established fields `value`, `tolerance`, `status`, `interpretation`, `assessment_scope`, and `theorem_status`; claim IDs live in metric keys.
- `metrics.json` and `arrays.npz` are always core. `diagnostics.npz` exists only when `collect_diagnostics=True`. Rendering begins only after `RunStore.finalize()`.
- Renderer status is accepted only when backed by a contained on-disk manifest with exact requested inventory and correct image SHA-256 values. Renderer failure cannot mutate numerical status or bytes.
- Numerical checks verify the implementation of declared finite objects. They do not prove arbitrary-family DQM, full experiment recovery, natural-flow semiconjugacy, nontrivial holonomy, or RG universality.
- Do not modify the Research vault. Offer an ingest after results, but write there only with separate user confirmation.
- Workers are not alone in the codebase: edit only assigned files, never revert another worker's edits, and adapt to already-integrated interfaces.

---

### Task 1: Discriminated Theory Configuration and Legacy Identity Guards

**Files:**
- Modify: `src/multiagent_elbo/config.py`
- Modify: `tests/test_config.py`

**Interfaces:**
- Produces: `AttentionTheoryConfig`, `CategoricalDqmTheoryConfig`, and `ExperimentTheoryConfig`.
- Preserves: existing `TheoryConfig`, canonical finite hash `ad296bae54057c87330a964e99c1ce6657bcfc2f769fd3d7211c5d6a6380e4f9`, and canonical Gaussian hash `30e8e0dd923c24a63d9ffc91e4b1d9740d15f576bb393f3106783fdd1b78085c` for the current launcher dictionaries.

- [ ] **Step 1: Write failing configuration-variant tests**

Add literal dictionary helpers and tests that request the not-yet-supported variants:

```python
def attention_theory() -> dict[str, object]:
    return {
        "experiment": "attention_marked_event",
        "fixture": "nested_nonuniform_v1",
    }


def dqm_theory() -> dict[str, object]:
    return {
        "experiment": "categorical_dqm",
        "fixture": "three_category_softmax_v1",
        "theta": [math.log(2.0), math.log(3.0)],
        "finite_difference_step": 1.0e-5,
        "dqm_step_sizes": [0.1, 0.05, 0.025, 0.0125],
    }


def test_attention_and_dqm_theory_configs_resolve_to_frozen_variants(tmp_path: Path):
    run, _, numerics, output = valid_dicts(tmp_path)
    attention = ExperimentConfig.from_dicts(run, attention_theory(), numerics, output)
    dqm = ExperimentConfig.from_dicts(run, dqm_theory(), numerics, output)
    assert isinstance(attention.theory, AttentionTheoryConfig)
    assert isinstance(dqm.theory, CategoricalDqmTheoryConfig)
    assert dqm.theory.theta == (math.log(2.0), math.log(3.0))
    assert dqm.theory.dqm_step_sizes == (0.1, 0.05, 0.025, 0.0125)
```

In the same RED test edit, add table-driven cases for missing/unknown variant keys, bad fixtures, Boolean/nonnumeric theta entries, wrong theta length, nonpositive/nonfinite finite-difference steps, empty or duplicate ladders, and nondecreasing ladders. Add legacy identity guards before touching production code:

```python
def test_legacy_launcher_config_hashes_remain_unchanged():
    finite = ExperimentConfig.from_dicts(
        {"name": "finite exact", "seed": 20260808},
        {"experiment": "finite_exact", "retained_interaction_order": 2},
        {
            "dtype": "float64", "atol": 1e-10, "rtol": 1e-9,
            "min_spd_rcond": 1e-12, "max_frame_condition": 1.0e6,
        },
        {
            "root": "artifacts", "collect_diagnostics": True,
            "render_figures": False,
        },
    )
    gaussian = ExperimentConfig.from_dicts(
        {"name": "gaussian realization", "seed": 20260808},
        {"experiment": "gaussian_realization", "retained_interaction_order": None},
        {
            "dtype": "float64", "atol": 1e-12, "rtol": 1e-10,
            "min_spd_rcond": 1e-12, "max_frame_condition": 1.0e6,
        },
        {
            "root": "artifacts", "collect_diagnostics": True,
            "render_figures": False,
        },
    )
    assert config_sha256(finite) == "ad296bae54057c87330a964e99c1ce6657bcfc2f769fd3d7211c5d6a6380e4f9"
    assert config_sha256(gaussian) == "30e8e0dd923c24a63d9ffc91e4b1d9740d15f576bb393f3106783fdd1b78085c"
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_config.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task1"
```

Expected: collection or assertion failure because the two new dataclasses/experiment names do not exist. Preserve the exact failure output in the Task 1 report before implementing any new configuration behavior.

- [ ] **Step 3: Implement exact experiment dispatch and validation**

Add these frozen types without changing the fields of legacy `TheoryConfig`:

```python
@dataclass(frozen=True)
class AttentionTheoryConfig:
    experiment: Literal["attention_marked_event"]
    fixture: Literal["nested_nonuniform_v1"]


@dataclass(frozen=True)
class CategoricalDqmTheoryConfig:
    experiment: Literal["categorical_dqm"]
    fixture: Literal["three_category_softmax_v1"]
    theta: tuple[float, float]
    finite_difference_step: float
    dqm_step_sizes: tuple[float, ...]


ExperimentTheoryConfig = (
    TheoryConfig | AttentionTheoryConfig | CategoricalDqmTheoryConfig
)
```

Change `ExperimentConfig.theory` to `ExperimentTheoryConfig`. In `from_dicts`, read and type-check `experiment` first, then apply an exact key set for that discriminant. For DQM, accept only `list` or `tuple` containers containing exact finite `float` values; reject `bool` and integers; require two theta values, a positive finite finite-difference step, and a nonempty unique strictly decreasing positive step ladder. Return tuples in the frozen dataclass.

- [ ] **Step 4: Run the full config/artifact GREEN regression**

Implement dedicated tuple helpers with field-specific `ConfigError` messages. Run:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_config.py tests/test_artifacts.py tests/test_runtime.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task1"
```

Expected: all selected tests pass and legacy hashes match exactly.

- [ ] **Step 5: Commit Task 1**

```powershell
git add src/multiagent_elbo/config.py tests/test_config.py
git commit -m "feat: add attention and DQM config variants"
```

---

### Task 2: Shared Metric and Renderer-Evidence Infrastructure

**Files:**
- Create: `src/multiagent_elbo/experiment_support.py`
- Create: `src/multiagent_elbo/rendering.py`
- Modify: `src/multiagent_elbo/finite/experiment.py`
- Modify: `src/multiagent_elbo/realizations/gaussian/experiment.py`
- Create: `tests/test_experiment_support.py`
- Modify: `tests/test_finite_experiment.py`
- Modify: `tests/test_gaussian_realization.py`

**Interfaces:**
- Produces: `MetricRecord`, `target_metric`, `lower_bounded_metric`, `readonly_array`, `validated_renderer_status`, and `record_figure_failure_safely` for both new experiments.
- Preserves: legacy metric JSON fields and finite/Gaussian numerical bytes.

- [ ] **Step 1: Write RED tests for shared metric records**

Create `tests/test_experiment_support.py` with literal assertions:

```python
def test_target_and_lower_bound_metrics_keep_established_json_schema():
    exact = target_metric(
        1.0e-13,
        1.0e-10,
        target=0.0,
        interpretation="identity",
        theorem_status="established_conditional_identity",
    )
    control = lower_bounded_metric(
        0.2,
        1.0e-10,
        lower_bound=0.1,
        interpretation="negative control",
        theorem_status="negative_control",
    )
    assert asdict(exact).keys() == {
        "value", "tolerance", "status", "interpretation",
        "assessment_scope", "theorem_status",
    }
    assert exact.status == "pass"
    assert control.status == "pass"
```

Run the file and confirm RED because `experiment_support` is absent.

- [ ] **Step 2: Implement the minimal shared metric helpers**

Move no existing experiment logic. Add the exact established field schema, two comparison helpers, and a `readonly_array(values, dtype=np.float64)` function that copies C-contiguously and marks the result nonwriteable.

- [ ] **Step 3: Write RED direct tests for evidence-backed renderer validation**

Add tests that construct real temporary PNG/PDF files and a real JSON manifest, then verify complete and failed statuses. Add forged cases for wrong run directory, wrong request ordering, uncontained manifest path, wrong image SHA-256, missing image, empty failure message, and an object with only `status="complete"`. Each forged case must raise `ValueError` containing `unbacked` or `invalid status`.

- [ ] **Step 4: Extract the Gaussian-strength validator**

Create `rendering.py` by extracting the already-covered Gaussian validator and safe failure recorder exactly, preserving its fail-closed exception boundary. The public validator must turn every malformed-object, missing-attribute, bad-path, path-resolution, missing-file, JSON-decode, malformed-record, and hashing failure into a controlled `ValueError` whose message contains `unbacked`; only an unsupported top-level status uses `invalid status`. It must not leak `AttributeError`, `TypeError`, `OSError`, `JSONDecodeError`, or `KeyError` for hostile renderer output.

After safely acquiring fields, require exact resolved run/output identity, exact request ordering, a contained existing `figure-manifest.json` or `figure-failure.json`, matching manifest status/run/request fields, and a list-valued figure inventory. A failed status requires an empty inventory and a nonempty message. A complete status requires exactly one record per requested figure in order, no failure message, basename-only PNG/PDF names, contained nonempty files, and exact SHA-256 values. `record_figure_failure_safely` must call the figure-layer recorder inside a broad secondary-failure guard so renderer error reporting can never alter or escape a finalized numerical result.

Delete the private duplicate from the Gaussian experiment and import these shared functions. Do not replace the guarded Gaussian behavior with a weaker pseudocode approximation.

- [ ] **Step 5: Harden the finite experiment through RED failure injection**

Add finite tests equivalent to the Gaussian forged-status and wrong-hash cases. Verify they fail against the current finite runner, which trusts only `.status`. Then route the finite runner through `validated_renderer_status` and `record_figure_failure_safely` after `RunStore.finalize()`.

- [ ] **Step 6: Run shared and legacy experiment regressions**

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_experiment_support.py tests/test_finite_experiment.py tests/test_gaussian_realization.py tests/test_figures.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task2"
```

Expected: all selected tests pass; renderer failures remain isolated from finalized numerical results.

- [ ] **Step 7: Commit Task 2**

```powershell
git add src/multiagent_elbo/experiment_support.py src/multiagent_elbo/rendering.py src/multiagent_elbo/finite/experiment.py src/multiagent_elbo/realizations/gaussian/experiment.py tests/test_experiment_support.py tests/test_finite_experiment.py tests/test_gaussian_realization.py
git commit -m "refactor: share evidence-backed experiment rendering"
```

---

### Task 3: State-Conditioned Marked-Event Attention Core

**Files:**
- Create: `src/multiagent_elbo/finite/attention.py`
- Create: `tests/test_attention.py`

**Interfaces:**
- Consumes: `NumericsConfig`, `ProbabilityMeasure`, and `MarkovKernel`.
- Produces: `AttentionDisintegration`, `StateConditionedAttentionLaw`, and `compose_kernels` with the signatures in the approved design.

- [ ] **Step 1: Write RED construction/disintegration tests with literal values**

Build a two-state test containing one positive state and one zero-probability state. Assert that `eta = alpha[..., None] * beta`, active rows recover the supplied conditionals, inactive state/receiver rows are zero with false masks, all arrays are read-only, and mutating constructor inputs after creation does not change stored arrays.

Use direct literal expectations, including:

```python
assert_allclose(law.eta_given_state[0], [[0.3, 0.2], [0.1, 0.4]])
assert_array_equal(result.positive_state_mask, [True, False])
assert_array_equal(result.positive_receiver_mask, [[True, True], [False, False]])
assert_array_equal(result.beta_given_state[1], np.zeros((2, 2)))
```

Run and confirm RED because `finite.attention` does not exist.

- [ ] **Step 2: Implement validated immutable construction and disintegration**

Implement:

```python
@dataclass(frozen=True)
class AttentionDisintegration:
    alpha_given_state: np.ndarray
    beta_given_state: np.ndarray
    positive_state_mask: np.ndarray
    positive_receiver_mask: np.ndarray


@dataclass(frozen=True, init=False)
class StateConditionedAttentionLaw:
    state_probability: ProbabilityMeasure
    receiver_labels: tuple[str, ...]
    source_labels: tuple[str, ...]
    eta_given_state: np.ndarray
    numerics: NumericsConfig
```

Its explicit constructor accepts `(state_probability, receiver_labels, source_labels, eta_given_state)` in that order; the classmethod `from_alpha_beta` accepts those first three arguments followed by `alpha_given_state` and `beta_given_state`.

Positive-probability states require unit conditional event mass; zero-probability states require an all-zero representative. `from_alpha_beta` requires normalized alpha on positive states, normalized beta on positive receiver rows, and zero beta representatives on inactive rows. Use exact positivity (`> 0.0`) for support masks and configured tolerances only for normalization comparisons.

- [ ] **Step 3: Add RED validation cases**

Cover wrong dimensions, duplicate/empty labels, nonfinite/negative entries, mismatched state count, nonunit active-state mass, nonzero inactive representatives, nonunit active beta rows, and a `ProbabilityMeasure`/kernel numerical-policy mismatch. Run and verify the intended validation branches fail before adding them.

- [ ] **Step 4: Implement minimal validation and rerun construction tests**

Reject each malformed input with field-specific `TypeError` or `ValueError`. Require no filesystem or RNG dependency in this module.

- [ ] **Step 5: Write RED pushforward/composition tests with the exact three-state fixture**

Use the approved `mu=(1/2,1/3,1/6)`, `eta0`, cyclic `eta1`, transposed `eta2`, `C01`, `C12`, and nested node partitions. Pin final state mass `(2/3,1/3)` and:

```python
expected_middle_probability = np.array([5/6, 1/6])
expected_direct_bridge = np.array(
    [[9/16, 3/8, 1/16], [3/8, 1/4, 3/8]]
)
expected_middle_eta_y0 = np.array(
    [[3/20, 7/200, 23/200],
     [1/100, 1/200, 17/200],
     [3/10, 3/50, 6/25]]
)
expected_middle_alpha_y0 = np.array([3/10, 1/10, 3/5])
expected_middle_beta_y0 = np.array(
    [[1/2, 7/60, 23/60],
     [1/10, 1/20, 17/20],
     [1/2, 1/10, 2/5]]
)
expected_w0 = np.array([[683/1600, 273/1600], [401/1600, 243/1600]])
expected_w1 = np.array([[281/800, 187/800], [187/800, 145/800]])
```

Assert the first stage equals every middle literal, independently computed direct bridge weights and staged bridge composition both equal `expected_direct_bridge`, direct and staged final event laws equal the final literals, final alpha/beta equal the design fractions, and composed kernels equal independent literal products with correct labels.

- [ ] **Step 6: Implement joint-law pushforward and kernel composition**

Use:

```python
joint = state_probability.masses[:, None, None] * eta_given_state
coarse_joint = np.einsum(
    "yz,iI,jJ,yij->zIJ",
    state_channel.matrix,
    receiver_partition.matrix,
    source_partition.matrix,
    joint,
)
coarse_probability = state_probability.masses @ state_channel.matrix
```

Divide by coarse state probability only where it is strictly positive, return zero representatives elsewhere, and construct the result through the validated constructor. `compose_kernels(first, second)` requires `first.target_labels == second.source_labels`, identical numerics, and returns `first.matrix @ second.matrix`.

- [ ] **Step 7: Run the complete attention-core tests and commit**

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_attention.py tests/test_measures.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task3"
git add src/multiagent_elbo/finite/attention.py tests/test_attention.py
git commit -m "feat: add state-conditioned marked-event attention"
```

---

### Task 4: Gauge-Covariant Attention Evaluation

**Files:**
- Create: `src/multiagent_elbo/geometry/attention_gauge.py`
- Create: `tests/test_attention_gauge.py`

**Interfaces:**
- Consumes: `NumericsConfig`.
- Produces: `AttentionCovariantInputs`, `AttentionGaugeEvaluation`, `evaluate_attention`, and `transform_attention_inputs`.

- [ ] **Step 1: Write RED literal-logit and immutability tests**

Construct the exact two-node vectors, covectors, links, and frames from design section 6.4. Assert:

```python
assert_allclose(evaluation.occupancy_logits, [1.0, 5.0 / 3.0])
assert_allclose(
    evaluation.source_logits,
    [[5.0 / 2.0, 17.0 / 4.0], [-2.0 / 3.0, 7.0 / 6.0]],
)
assert_allclose(evaluation.eta, evaluation.alpha[:, None] * evaluation.beta)
assert evaluation.eta.sum() == pytest.approx(1.0)
```

Mutate original arrays and verify stored arrays do not change; all returned arrays must be nonwriteable.

- [ ] **Step 2: Implement stable scalar attention evaluation**

Validate shapes `(I,K)`, `(I,K)`, `(J,K)`, `(I,J,K,K)`, common positive fiber dimension, finiteness, and matching node dimensions. Compute occupancy/source logits by `einsum`, then stable softmax by subtracting each maximum before exponentiation. Return defensive read-only logits and scalar laws.

- [ ] **Step 3: Write RED matched-frame metamorphic and broken-link control**

Apply the exact nonorthogonal frames. Assert recomputed logits/alpha/beta/eta agree within `atol + rtol * scale`. Independently construct the incorrect transformed inputs that change vectors/covectors but leave links fixed and assert the eta sup gap exceeds `0.1` (the pinned fixture is about `0.210995`).

- [ ] **Step 4: Implement matched local-frame transformation with solves**

Implement the approved single-node-frame action:

```text
r_i' = G_i r_i
q_i' = q_i G_i^-1
k_j' = G_j k_j
U_ij' = G_i U_ij G_j^-1
```

`transform_attention_inputs` accepts one coherent frame family indexed by the shared node labels; it must not introduce an independent source-frame family. Validate every frame is finite square, has positive determinant, and has `np.linalg.cond(frame) <= numerics.max_frame_condition`. Use `np.linalg.solve` or transposed solves for covectors and right actions; do not materialize matrix inverses.

- [ ] **Step 5: Add RED invalid-frame tests, implement guards, and verify GREEN**

Test wrong count/shape, singular frames, negative determinant, nonfinite entries, and condition above the configured limit. Then implement the exact checks and rerun:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_attention_gauge.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task4"
```

- [ ] **Step 6: Commit Task 4**

```powershell
git add src/multiagent_elbo/geometry/attention_gauge.py tests/test_attention_gauge.py
git commit -m "feat: add gauge-covariant attention metamorphics"
```

---

### Task 5: Positive Categorical Family and DQM/Fisher Analysis

**Files:**
- Create: `src/multiagent_elbo/finite/categorical.py`
- Create: `src/multiagent_elbo/finite/categorical_dqm.py`
- Create: `tests/test_categorical_dqm.py`

**Interfaces:**
- Consumes: `ProbabilityMeasure`, `MarkovKernel`, and `fisher_channel_decomposition`.
- Produces: `CategoricalExponentialFamily`, fine/pushed centered finite differences, `DqmRemainderLadder`, and `CategoricalDqmAnalysis`.

Use these exact public names:

```python
family.log_probabilities(theta)
family.probabilities(theta)
family.probability_measure(theta)
family.score(theta)
family.fisher_information(theta)

centered_log_probability_finite_difference(family, theta, step)
centered_pushed_log_probability_finite_difference(family, theta, channel, step)
normalized_dqm_remainder_ladder(family, theta, direction, step_sizes)
analyze_categorical_dqm(
    family,
    theta,
    channel,
    finite_difference_step,
    direction,
    dqm_step_sizes,
)
```

`DqmRemainderLadder` contains read-only `step_sizes`, `positive`, and `negative` vectors. `CategoricalDqmAnalysis` contains the base probability, analytic and finite-difference fine scores, finite-difference pushed score, `FisherChannelResult`, the remainder ladder, and the two scope strings.

- [ ] **Step 1: Write RED exact-family tests**

Instantiate labels `("x0","x1","x2")`, zero base logits, and statistics `((1,0),(0,1),(0,0))`. At theta `(log 2, log 3)`, pin:

```python
assert_allclose(family.probabilities(theta), [1/3, 1/2, 1/6])
assert_allclose(
    family.score(theta),
    [[2/3, -1/2], [-1/3, 1/2], [-1/3, -1/2]],
)
assert_allclose(
    family.fisher_information(theta),
    [[2/9, -1/6], [-1/6, 1/4]],
)
```

Also test score centering at at least three literal theta values and defensive read-only outputs.

- [ ] **Step 2: Implement the stable finite exponential family**

Implement logits `base_logits + sufficient_statistics @ theta`; compute log normalization by max-shifted log-sum-exp; derive `score = statistics - p @ statistics`; and compute Fisher by an explicit weighted outer-product `einsum`. Reject wrong theta shape, nonfinite matrix products, zero represented probabilities, and nonunit probability output.

- [ ] **Step 3: Write RED fine and pushed finite-difference tests**

Use step `1e-5` and channel:

```python
channel = ((1.0, 0.0), (0.0, 1.0), (0.5, 0.5))
```

Compare centered differences of `log p_theta` with the analytic score and centered differences of `log(p_theta @ K)` with exact conditional score `((7/15,-1/2),(-1/3,5/14))`. Require sup errors below `1e-8`.

- [ ] **Step 4: Implement finite differences with effective-step validation**

For every coordinate, form copied `theta_plus/minus`, reject if either rounds back to theta, evaluate log probabilities independently, and divide by `2*step`. The pushed version validates labels/numerics and requires strictly positive pushed probabilities at both perturbations.

- [ ] **Step 5: Write RED Fisher and two-sided DQM ladder tests**

Pin coarse probability `(5/12,7/12)`, coarse Fisher `((7/45,-1/6),(-1/6,5/28))`, and conditional covariance/defect `diag(1/15,1/14)`. For direction `(3/5,-4/5)` and steps `(0.1,0.05,0.025,0.0125)`, pin approximate ladders:

```text
positive = (0.00559638, 0.00280237, 0.00140217, 0.000701326)
negative = (0.00562600, 0.00280979, 0.00140403, 0.000701790)
```

Assert both sequences strictly decrease and the Fisher identity residual is below `1e-12`.

- [ ] **Step 6: Implement the analysis and stable DQM remainder**

Compute each signed likelihood-ratio deviation as:

```python
delta_log = family.log_probabilities(theta + signed_step * direction) - base_log
ratio_minus_one = np.expm1(0.5 * delta_log)
linear = 0.5 * signed_step * (analytic_score @ direction)
normalized = np.sqrt(np.sum(base_probability * (ratio_minus_one - linear) ** 2)) / step
```

Return a frozen `DqmRemainderLadder` and a frozen `CategoricalDqmAnalysis` that contains analytic/FD scores, the existing `FisherChannelResult`, and scope strings `finite_positive_smooth_exponential_family` and `declared_fixed_parameter_independent`.

- [ ] **Step 7: Add RED support/perturbation boundary tests and implement guards**

Cover malformed family shapes, duplicate/empty labels, Boolean/nonfinite theta, nonpositive step, nonunit direction, empty/nondecreasing/duplicate ladder, perturbations that round back, underflowed zero source probability, and zero pushed probability. Require explicit failure before a nonfinite result is returned.

- [ ] **Step 8: Run the full DQM-core selection and commit**

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py tests/test_fisher.py tests/test_measures.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5"
git add src/multiagent_elbo/finite/categorical.py src/multiagent_elbo/finite/categorical_dqm.py tests/test_categorical_dqm.py
git commit -m "feat: add parametric categorical DQM analysis"
```

---

### Task 6: Attention Experiment and Click-to-Run Launcher

**Files:**
- Create: `src/multiagent_elbo/finite/attention_experiment.py`
- Create: `run_attention_lab.py`
- Create: `tests/test_attention_experiment.py`

**Interfaces:**
- Consumes: Tasks 1-4, `RunStore`, provenance helpers, shared metric helpers, and shared renderer validation.
- Produces: `AttentionExperimentResult` and `run_attention_experiment(config, *, renderer=None)`.

`AttentionExperimentResult` contains `run_dir`, `config_hash`, numerical `status`, immutable metric and array mappings, `figure_status`, and optional `figure_dir`, matching the established finite experiment result shape.

- [ ] **Step 1: Write RED exact experiment tests**

Create an attention config helper with all four existing output keys. Assert the runner rejects non-`ExperimentConfig` and the wrong experiment before patchable RNG/provenance/filesystem seams execute. Assert the default run emits pass metrics with stable keys:

```text
ATT-01_factorization_residual
ATT-01_normalization_residual
ATT-02_direct_staged_eta_residual
ATT-02_direct_staged_alpha_residual
ATT-02_direct_staged_active_beta_residual
ATT-02_literal_eta_residual
ATT-02_literal_alpha_residual
ATT-02_literal_active_beta_residual
ATT-02_reverse_bridge_residual
ATT-03_gauge_logits_residual
ATT-03_gauge_alpha_residual
ATT-03_gauge_beta_residual
ATT-03_gauge_eta_residual
ATT-03_broken_link_gap_control
ATT-04_relabeling_naturality_residual
ATT-04_incoherent_relabeling_gap_control
ATT-NEG-01_beta_only_associativity_gap
ATT-NEG-01_beta_only_correct_gap
```

Pin beta-only gaps `1/10` and `1/20`; pin every identity residual to configured tolerance. `active_beta` means the maximum absolute residual only over receiver rows whose alpha mass is strictly positive. `gauge_logits` is the maximum over occupancy and source logits; the separate alpha, beta, and eta metrics ensure a downstream normalization bug cannot hide behind invariant logits.

- [ ] **Step 2: Implement the preregistered fixture and metrics**

Construct only the approved rational state/node fixture and gauge fixture. Compute direct/staged paths through separately composed kernels. Compute reverse bridges independently from joint state mass. Implement the beta-only rule privately by column aggregation plus equal receiver-row averaging; do not expose it as the correct core API. For relabeling naturality, use an explicit cyclic node permutation matrix `P`, transform every state slice as `P.T @ eta[y] @ P`, transform both node partitions as `P.T @ partition`, and compare with the unchanged coarse labels. The mismatch control transforms eta but deliberately leaves the partitions fixed.

Persist core arrays sorted by name. Put state channels, reverse bridges, frames, transformed inputs, and mismatch-control intermediates in diagnostics. Record provenance scopes `pre_registered_state_conditioned_marked_event_fixture` and `scalar_gauge_plus_finite_relabeling`.

- [ ] **Step 3: Write RED artifact/toggle/determinism tests**

Parameterize all four combinations of `collect_diagnostics` and `render_figures`. Assert exact manifest inventory, optional diagnostics, figure status, no figure path when disabled, cross-root byte equality for `metrics.json` and `arrays.npz`, immutable result mappings, and same-seed deterministic NPZ bytes.

- [ ] **Step 4: Implement finalization-before-rendering and failure isolation**

Follow this order exactly:

```text
validate config and every fixture
compute metrics and arrays
derive streams/config hash/provenance
RunStore.create
write sorted metrics and arrays
optionally write diagnostics
RunStore.finalize
compute numerical status
optionally render requested=("attention_composition",)
validate the returned on-disk figure manifest
record renderer failure safely without changing numerics
```

- [ ] **Step 5: Write RED launcher behavior in the owned experiment test, then add `run_attention_lab.py`**

Before creating the launcher, add a file-loader test to `tests/test_attention_experiment.py` that imports the expected root path under `sys.argv=["run_attention_lab.py","--invalid"]`, asserts no files are written and no `parser` exists, overrides only `OUTPUT.root`, calls `main()`, and receives `AttentionExperimentResult`. Confirm RED because the launcher path is absent.

Then mirror the existing root launcher bootstrap and dictionaries exactly. The default has `RUN.name="attention_marked_event"`, seed `20260809`, the Task 1 attention theory dictionary, float64 tolerances, and independent output toggles. `main()` prints run directory, numerical status/metric count, and figure status; imports do no work.

- [ ] **Step 6: Run the attention experiment selection and commit**

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_attention.py tests/test_attention_gauge.py tests/test_attention_experiment.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task6"
git add src/multiagent_elbo/finite/attention_experiment.py run_attention_lab.py tests/test_attention_experiment.py
git commit -m "feat: add click-to-run attention laboratory"
```

---

### Task 7: Categorical-DQM Experiment and Click-to-Run Launcher

**Files:**
- Create: `src/multiagent_elbo/finite/categorical_dqm_experiment.py`
- Create: `run_categorical_dqm_lab.py`
- Create: `tests/test_categorical_dqm_experiment.py`

**Interfaces:**
- Consumes: Tasks 1, 2, and 5 plus the existing artifact/provenance system.
- Produces: `CategoricalDqmExperimentResult` and `run_categorical_dqm_experiment(config, *, renderer=None)`.

`CategoricalDqmExperimentResult` contains `run_dir`, `config_hash`, numerical `status`, immutable metric and array mappings, `channel_scope`, `figure_status`, and optional `figure_dir`.

- [ ] **Step 1: Write RED default metric/oracle tests**

Assert stable generic keys:

```text
DQM-01_normalization_residual
DQM-01_score_centering_residual
DQM-01_finite_difference_score_residual
DQM-01_two_sided_remainder_final
INF-02_conditional_score_fd_residual
INF-02_fisher_identity_residual
INF-02_fisher_defect_min_eigenvalue
INF-02_positive_loss_trace_control
```

At the exact default theta, additionally require literal-oracle residual keys and `INF-NEG-01_wrong_weight_gap` equal to `4/21` within tolerance. Wrong-experiment rejection must occur before RNG or writes.

- [ ] **Step 2: Implement default and edited-theta metric semantics**

Build the approved family/channel/direction and call Task 5 functions. Always emit generic analytic/FD/Fisher checks. Detect the default theta and ladder by exact resolved tuple equality; only then emit rational-oracle, monotonic-ladder, and pinned wrong-weight pass/fail metrics. For every theta, store the step vector and both remainder ladders in core arrays so diagnostics-off figure replay remains possible. For edited theta, keep the wrong-weight gap as a generic diagnostic metric/array without making default literal thresholds status-bearing; only detailed wrong-score intermediates belong in optional diagnostics.

The wrong score is exactly:

```python
wrong_score = (channel.matrix.T @ analytic_score) / channel.matrix.sum(axis=0)[:, None]
```

Record `channel_scope="declared_fixed_parameter_independent"` in provenance and the frozen typed result; do not serialize a string into the numeric NPZ archive.

- [ ] **Step 3: Write RED artifact, custom-theta, and renderer tests**

Cover all four output-toggle combinations, cross-root semantic bytes, custom finite theta without default-oracle metric keys, invalid perturbation failure before publication, complete backed rendering, renderer exception isolation, forged complete/failed status, and secondary failure-record errors.

- [ ] **Step 4: Implement publication and post-finalization rendering**

Use the same order and shared helpers as Task 6, requesting only `("categorical_dqm",)`. Core arrays include theta, fine/coarse probabilities, analytic/FD fine/coarse scores, Fishers, defect, residual, channel, direction, steps, and positive/negative ladders. Joint masses, per-target covariance contributions, and wrong-score arrays are optional diagnostics.

- [ ] **Step 5: Write RED launcher behavior, then add `run_categorical_dqm_lab.py`**

Before creating the launcher, add the same import-side-effect and overridden-output-root behavior test to `tests/test_categorical_dqm_experiment.py`; confirm RED because the root file is absent. Then use the exact dictionary values from the design, including `math.log(2.0)`, `math.log(3.0)`, step `1e-5`, and ladder `[0.1,0.05,0.025,0.0125]`. Keep the adjacent-`src` bootstrap before package imports and an import-safe `main()` with no argument parsing.

- [ ] **Step 6: Run the DQM experiment selection and commit**

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py tests/test_categorical_dqm_experiment.py tests/test_fisher.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task7"
git add src/multiagent_elbo/finite/categorical_dqm_experiment.py run_categorical_dqm_lab.py tests/test_categorical_dqm_experiment.py
git commit -m "feat: add click-to-run categorical DQM laboratory"
```

---

### Task 8: Saved-Artifact Figures, Launcher Integration, Documentation, and Evidence Closure

**Files:**
- Modify: `src/multiagent_elbo/figures.py`
- Modify: `src/multiagent_elbo/finite/__init__.py`
- Modify: `src/multiagent_elbo/geometry/__init__.py`
- Modify: `tests/test_figures.py`
- Modify: `tests/test_launchers.py`
- Modify: `README.md`
- Modify: `docs/hypotheses.md`
- Create: `docs/results/2026-08-09-attention-categorical-dqm-results.md`
- Modify: `docs/verification/independent-reviews.md`
- Replace: `docs/verification/pytest-foundation.xml`
- Update after the final commit, without recommitting: `.verification/ledger.json`

**Interfaces:**
- Consumes: all preceding tasks.
- Produces: pure replay names `attention_composition` and `categorical_dqm`, public package exports, current documentation, JUnit evidence, and a final validated claim ledger.

- [ ] **Step 1: Write RED saved-artifact figure tests**

Create finalized runs with Tasks 6 and 7, then call `render_run` for each new name. Assert nonempty PNG/PDF, 3.5-inch figure width through renderer construction tests, 300-DPI manifest metadata, requested order, deterministic hashes on repeat replay, and no mutation of numerical bundle hashes. Add missing-array, nonfinite-array, corrupt-hash, and transactional renderer-failure cases.

- [ ] **Step 2: Implement attention and DQM figure renderers**

Extend `_FIGURE_FILENAMES` and dispatch. The attention figure uses four compact panels: direct coarse eta at both final states, staged-minus-direct residual, and beta-only-minus-correct residual. The DQM figure compares analytic/FD scores and plots positive/negative normalized remainder against step on log-log axes. Read only saved metrics/arrays.

Preserve existing finite/Gaussian figure functions and bytes. Make the new manifest caption experiment-specific from saved values; do not reuse `n=1 exact fixture` for DQM. Retain Agg, local style contexts, PDF metadata suppression, atomic staging, and Okabe-Ito plus redundant markers/line styles.

- [ ] **Step 3: Write RED launcher integration tests**

Extend `tests/test_launchers.py` to import both new launchers under invalid `sys.argv` with no side effects; override only `OUTPUT.root` and run `main()`; and execute each launcher in a sanitized temporary CWD with `PYTHONPATH=""` and no arguments. Assert `status=pass`, exactly one complete manifest, and no parser attribute.

- [ ] **Step 4: Wire exports and complete launcher/figure GREEN**

Export only the intended stable primitive/result/run interfaces from finite and geometry package initializers. Run:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_figures.py tests/test_launchers.py tests/test_attention_experiment.py tests/test_categorical_dqm_experiment.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task8"
```

- [ ] **Step 5: Update user and scientific documentation**

README must list four click launchers, discriminated THEORY fields, attention/DQM checks, and exact scope boundaries. `docs/hypotheses.md` must add ATT-01 through ATT-NEG-01, DQM-01, INF-02, and INF-NEG-01 with prediction, null, operationalization, controls, support/refutation thresholds, inconclusive rules, and frozen Theory pointers. The results document must record exact resolved configs, artifact paths/hashes, metric values, JUnit totals, environment, reviewer findings, and the distinction between analytic derivation and numerical corroboration.

- [ ] **Step 6: Run both click-to-run laboratories and pure figure replays**

Use temporary output-root edits only through imported launcher dictionaries in a controlled test helper or a copied resolved config; do not modify committed launcher defaults merely to run verification. Record the two finalized run paths and confirm every metric passes, diagnostics and figures follow toggles, and artifact manifests are complete.

- [ ] **Step 7: Run current full-suite machine evidence**

Write JUnit directly to `docs/verification/pytest-foundation.xml` using a writable/elevated test invocation as needed:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider --basetemp="C:\tmp\multiagent-elbo-attention-dqm-final" --junitxml=docs/verification/pytest-foundation.xml
```

Parse the XML for exact `tests`, `failures`, `errors`, and `skipped`; never report counts from progress output.

- [ ] **Step 8: Run static checks and commit the implementation/evidence revision**

```powershell
C:\Python314\python.exe -m compileall -q src run_attention_lab.py run_categorical_dqm_lab.py
git diff --check
git status --short
git add src/multiagent_elbo/figures.py src/multiagent_elbo/finite/__init__.py src/multiagent_elbo/geometry/__init__.py tests/test_figures.py tests/test_launchers.py README.md docs/hypotheses.md docs/results/2026-08-09-attention-categorical-dqm-results.md docs/verification/independent-reviews.md docs/verification/pytest-foundation.xml
git commit -m "feat: integrate attention and DQM laboratory evidence"
```

Confirm `Theory/` has no changes and both protected live checkouts retain their original WIP.

- [ ] **Step 9: Rebind and validate the verification ledger at the live final revision**

Use the installed verification skill only after every source, test, result, documentation, and review commit exists and broad-review fixes are finished. Start the control plane at that live final `HEAD`; this records `git:<HEAD>:sha256:<digest>` while deliberately excluding `.verification` content from the digest. Rebind all legacy claims affected by shared config/rendering changes, and add separate current ATT, categorical-DQM/Fisher, and launcher/figure workflow claims. Mathematical DQM evidence cites the finite-support Taylor derivation; numerical remainder trends are not proof evidence. Run the repository verification gate against the live final revision and require zero invalid entries or unresolved obligations before closure.

- [ ] **Step 10: Preserve the validated live ledger without invalidating its binding**

```powershell
git diff --exit-code HEAD -- . ":(exclude).verification"
git status --short
```

The installed gate includes the live commit hash in `artifact_revision`; therefore a tracked ledger cannot contain and remain validated against the hash of the same commit that contains it. Do not create an impossible self-referential ledger commit. Leave the freshly validated `.verification/ledger.json` as the sole intentional tracked worktree modification, with any activation marker confined to `.verification`, and record the final `HEAD`, ledger digest, clean non-verification diff check, and this control-plane constraint in the handoff. This is an `EVIDENCE_VERIFIED` live-final-revision ledger, not an `INCONCLUSIVE` fallback. A later publication workflow must regenerate and validate the ledger after any commit that changes `HEAD`.

---

## Execution Order and Review Gates

Tasks 1 and 2 establish shared seams. Tasks 3 and 4 form the attention mathematical slice; Task 5 is the independent DQM mathematical slice. Tasks 6 and 7 integrate each slice without sharing owned files. Task 8 is the sole owner of shared figure, launcher-test, export, documentation, and verification surfaces.

The user explicitly requested multiple expert agents, so execute with `superpowers:subagent-driven-development`. Dispatch a fresh implementer for each task, generate a task-scoped diff package, require both specification-compliance and code-quality review, and resolve every Critical/Important finding before advancing. After Task 8, run one broad whole-branch review, one consolidated fix wave if needed, and a scoped re-review. Any post-ledger source, test, result, or configuration edit invalidates the affected evidence: the consolidated fixer must rerun machine evidence and rebind/revalidate the ledger before the branch-finishing workflow.
