# Attention and Categorical-DQM Laboratory Design

**Status:** Approved in chat on 2026-08-09.

**Repository:** `C:\Users\chris and christine\Desktop\MultiAgentELBO`

**Implementation branch:** `codex/attention-dqm-labs-20260809`, created from the freshly fetched `origin/main` revision `dce3fd5d7b4ad89da9d510cddb0f728833cba01c` in an isolated worktree. The existing Desktop and Documents checkouts contain unrelated work in progress and are not modified by this feature.

**Theory source:** The repository's frozen `Theory/` snapshot, particularly `07b_agent_network_rg.tex:1745-1776` for marked-event attention and `06_general_coarsegraining.tex:170-224` for DQM score transfer and Fisher contraction. The Research-vault terminal record and wiki were consulted for scope and status boundaries. The vault is read-only for this task unless the user separately approves an ingest.

## 1. Objective

Add two directly runnable, dictionary-configured finite laboratories:

1. `run_attention_lab.py` tests exact attention coarse-graining at the state-conditioned normalized marked-event law `eta_ij(y) = alpha_i(y) beta_ij(y)`. It compares direct and staged state-bridge plus node-partition pushforwards, checks normalization, recomputes the scalar attention law from genuinely gauge-covariant inputs before and after local frame changes, checks coherent finite relabeling, and demonstrates that a deliberately incorrect beta-only rule is nonassociative.
2. `run_categorical_dqm_lab.py` instantiates a genuinely parameterized positive categorical family. It compares analytic and finite-difference scores, checks a two-sided DQM remainder, and verifies that a fixed parameter-independent channel transfers the score by conditional expectation while losing Fisher information by the expected conditional covariance.

Both launchers follow the existing project contract: no application CLI, no hidden runtime arguments, no import-time experiment, and all user-editable settings in `RUN`, `THEORY`, `NUMERICS`, and `OUTPUT` dictionaries. Numerical logic remains importable independently of the launchers.

## 2. Approaches considered

### A. Deterministic oracle laboratories first -- selected

Use exact, preregistered finite fixtures with generic mathematical primitives underneath them. The default attention fixture has rational matrices and exact direct/staged and negative-control results. The default DQM fixture is a smooth finite softmax family evaluated at a parameter with rational probabilities and Fisher tensors. This gives independent literal test oracles, stable artifacts, and sharp failure localization.

The DQM parameter and numerical step ladder remain editable and content-bound in the resolved configuration. The rational oracle is attached only to the default parameter; generic identity checks continue to apply when the user changes it.

### B. Fully configurable partition and categorical-family engine immediately -- deferred

This would expose arbitrary state/node partitions, sufficient statistics, and channels in launcher dictionaries. It is flexible, but it expands validation and serialization before the core identities have a trusted executable reference.

### C. Multi-parameter and multi-partition sweeps immediately -- deferred

Sweeps are valuable for stability studies, but they obscure the first falsification target and require aggregation, selection, and uncertainty semantics that are not needed for the two requested laboratories.

## 3. Scientific boundaries

- Attention is coarsened through the normalized joint event law `eta_ij = alpha_i beta_ij`, never through the row-stochastic conditional matrix `beta` alone.
- A zero-occupancy receiver has no identified conditional source law. The implementation returns a zero representative row plus an explicit inactive mask; it never invents a uniform conditional row or compares inactive rows as data.
- `alpha`, `beta`, and `eta` are scalar under the manuscript's fiber-frame gauge action. The laboratory includes a genuine local `GL+(2)` frame metamorphic: vectors, covectors, and source-to-receiver links transform covariantly; invariant contractions are recomputed into `alpha`, `beta`, and `eta`; and the scalar laws must remain unchanged. Coherent finite-label relabeling is a separate naturality test and is not mislabeled as holonomy.
- The categorical family is analytically DQM because it has finite support, strictly positive smooth probabilities, and a smooth square-root map. A finite-support Taylor derivation is recorded as mathematical evidence separately from the numerical finite differences and remainder ladder, which verify only the implementation of this declared family.
- Fisher contraction requires a normalized channel that is fixed and parameter-independent. The experiment does not optimize, learn, or differentiate the channel.
- A vanishing Fisher defect means local score recoverability in a direction. It does not by itself establish recovery of the full statistical experiment.
- Neither laboratory establishes natural-gradient-flow semiconjugacy, Gaussian attraction, RG universality, a continuum limit, or a physical law.

## 4. Configuration design

`ExperimentConfig.theory` becomes a discriminated union while preserving the serialized shape of existing finite and Gaussian configurations:

```python
@dataclass(frozen=True)
class TheoryConfig:
    experiment: Literal["finite_exact", "gaussian_realization"]
    retained_interaction_order: int | None

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
```

`ExperimentConfig.from_dicts` dispatches on `THEORY["experiment"]`, rejects unknown or missing keys for that experiment, rejects `bool` where a real number is required, canonicalizes lists to tuples, and validates all values before seeding or filesystem writes. Existing finite and Gaussian resolved JSON and configuration hashes remain byte-stable because no new nullable fields are added to their theory object.

For the DQM experiment, `theta` must contain exactly two finite float values, the finite-difference step must be finite and strictly positive, and the DQM ladder must be nonempty, finite, strictly positive, strictly decreasing, and free of duplicates. Before publishing a run, the experiment evaluates every required perturbed parameter and rejects any point whose represented probability or pushed probability is nonfinite or zero. It also rejects a perturbation that rounds back to the unperturbed parameter. The DQM claim is not extended across a floating-point support change. Strict monotonicity of the remainder ladder is a pass criterion only for the preregistered default theta and step ladder; edited settings retain the remainder table as a diagnostic and continue to run the analytic/finite-difference identities.

Default launcher dictionaries are:

```python
# run_attention_lab.py
RUN = {"name": "attention_marked_event", "seed": 20260809}
THEORY = {
    "experiment": "attention_marked_event",
    "fixture": "nested_nonuniform_v1",
}

# run_categorical_dqm_lab.py
RUN = {"name": "categorical_dqm", "seed": 20260809}
THEORY = {
    "experiment": "categorical_dqm",
    "fixture": "three_category_softmax_v1",
    "theta": [math.log(2.0), math.log(3.0)],
    "finite_difference_step": 1.0e-5,
    "dqm_step_sizes": [0.1, 0.05, 0.025, 0.0125],
}
```

Both launchers reuse the existing float64 `NUMERICS` and independent `OUTPUT` toggles. Changing any theory or numerical setting changes the canonical configuration hash and run path.

## 5. Package architecture

```text
run_attention_lab.py
run_categorical_dqm_lab.py
src/multiagent_elbo/
  config.py
  figures.py
    finite/
    attention.py
    attention_experiment.py
    categorical.py
    categorical_dqm.py
    categorical_dqm_experiment.py
  geometry/
    attention_gauge.py
  rendering.py
tests/
  test_attention.py
  test_attention_gauge.py
  test_attention_experiment.py
  test_categorical_dqm.py
  test_categorical_dqm_experiment.py
  test_config.py
  test_figures.py
  test_launchers.py
```

The two mathematical primitive modules are pure and filesystem-free. Experiment modules own only preregistered fixtures, metric evaluation, artifact publication, optional diagnostics, and post-finalization rendering. The existing `RunStore`, provenance, named RNG, and renderer-failure isolation contracts are reused without changing the mathematics of earlier laboratories.

## 6. Marked-event attention model

### 6.1 Core types and operations

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

    @classmethod
    def from_alpha_beta(
        cls,
        state_probability: ProbabilityMeasure,
        receiver_labels: Sequence[str],
        source_labels: Sequence[str],
        alpha_given_state: ArrayLike,
        beta_given_state: ArrayLike,
    ) -> "StateConditionedAttentionLaw": ...

    def disintegrate(self) -> AttentionDisintegration: ...

    def pushforward(
        self,
        state_channel: MarkovKernel,
        receiver_partition: MarkovKernel,
        source_partition: MarkovKernel,
    ) -> "StateConditionedAttentionLaw": ...

def compose_kernels(first: MarkovKernel, second: MarkovKernel) -> MarkovKernel: ...
```

For every positive-probability state, `alpha_given_state[y]` is normalized across receivers and every active receiver row of `beta_given_state[y]` is normalized across sources. The constructor forms `eta_given_state[y,i,j] = alpha[y,i] beta[y,i,j]`. A zero-probability state or zero-occupancy receiver is represented by a zero conditional row and an explicit false mask. The constructor validates ordered labels, shape, finite nonnegative entries, conditional normalization, and matching numerical policy, then takes defensive copies. Returned arrays are read-only.

Let `mu(y)` be the state probability, `C(y,z)` a fixed state channel, and `R(i,I)` and `S(j,J)` receiver/source partition kernels. The normalized joint marked law is

```text
gamma(y,i,j) = mu(y) eta(y,i,j).
```

The exact pushforward first transports that one joint law:

```text
gamma_coarse(z,I,J)
    = sum_(y,i,j) C(y,z) R(i,I) S(j,J) gamma(y,i,j),
mu_coarse(z) = sum_y mu(y) C(y,z),
eta_coarse(z,I,J) = gamma_coarse(z,I,J) / mu_coarse(z)
```

on positive coarse-state mass. This is the finite posterior-bridge conditional expectation, because `mu(y) C(y,z) / mu_coarse(z)` is the reverse bridge. On zero coarse-state mass, the implementation returns zeros and a false state mask.

Within each positive coarse state, receiver occupancy is the row marginal of `eta_coarse`; on positive receiver rows, the conditional source matrix is `eta_coarse / alpha_coarse[..., None]`. The masks identify exactly which entries may be interpreted as conditional laws.

Composition obeys

```text
push(push(gamma, C01, R01, S01), C12, R12, S12)
    = push(gamma, C01 C12, R01 R12, S01 S12).
```

This tests both Markov composition of the global joint law and the tower property of the induced reverse bridges after disintegration.

### 6.2 Exact attention fixture

Use three fine states with probability

```text
mu = (1/2, 1/3, 1/6)
```

and four fine nodes. At the base state `y0`, use

```text
alpha = (1/20, 1/4, 1/10, 3/5)

beta =
  ((1/2,  1/4,  1/5,  1/20),
   (1/4,  1/5,  1/10, 9/20),
   (1/20, 1/20, 1/20, 17/20),
   (1/5,  3/10, 1/10, 2/5))
```

Let `eta0 = diag(alpha) beta`. Define two additional normalized state-conditioned event laws without introducing new floating literals:

```text
eta1[i,j] = eta0[(i - 1) mod 4, (j - 1) mod 4]
eta2 = eta0.T
```

The nested state channels are

```text
C01 = ((1, 0),
       (1, 0),
       (0, 1))

C12 = ((3/4, 1/4),
       (1/4, 3/4))

C02 = C01 C12
    = ((3/4, 1/4),
       (3/4, 1/4),
       (1/4, 3/4))
```

The middle and final state probabilities are `(5/6, 1/6)` and `(2/3, 1/3)`. The direct reverse-bridge weights over `(y0,y1,y2)` are `(9/16,3/8,1/16)` at final state `w0` and `(3/8,1/4,3/8)` at `w1`. Staged bridge composition must reproduce these weights.

The nested deterministic partitions are

```text
fine -> middle:  (A, A, B, C)
middle -> coarse: (U, U, V)
fine -> coarse:   (U, U, U, V)
```

At base state `y0`, the exact first node-partition event law and disintegration are

```text
eta_middle =
  ((3/20, 7/200, 23/200),
   (1/100, 1/200, 17/200),
   (3/10, 3/50, 6/25))

alpha_middle = (3/10, 1/10, 3/5)

beta_middle =
  ((1/2, 7/60, 23/60),
   (1/10, 1/20, 17/20),
   (1/2, 1/10, 2/5))
```

For the base-state node-only oracle, direct and staged node pushforward both produce

```text
eta_coarse = ((1/5, 1/5),
              (9/25, 6/25))
alpha_coarse = (2/5, 3/5)
beta_coarse = ((1/2, 1/2),
               (3/5, 2/5))
```

For the complete state-channel plus node-partition fixture, direct and staged pushforwards must both produce the following conditional event laws:

```text
eta_coarse(w0) = ((683/1600, 273/1600),
                  (401/1600, 243/1600))

alpha_coarse(w0) = (239/400, 161/400)
beta_coarse(w0) = ((683/956, 273/956),
                   (401/644, 243/644))

eta_coarse(w1) = ((281/800, 187/800),
                  (187/800, 145/800))

alpha_coarse(w1) = (117/200, 83/200)
beta_coarse(w1) = ((281/468, 187/468),
                   (187/332, 145/332))
```

These literals independently pin the posterior-bridge weights, joint-law pushforward, node aggregation, and final disintegration rather than merely comparing two calls to the same helper.

### 6.3 Deliberately incorrect beta-only control

The negative control is evaluated on the base state `y0`. It equally averages conditional rows inside each receiver block after source aggregation, discarding the occupancy weights. It is private experiment code, not a reusable mathematical API.

For a receiver block `I` and source block `J`,

```text
beta_wrong[I,J] = (1 / |I|) sum_(i in I) sum_(j in J) beta[i,j].
```

The direct and staged wrong rules give

```text
beta_wrong_direct = ((11/20, 9/20),
                     (3/5,   2/5))

beta_wrong_staged = ((9/20, 11/20),
                     (3/5,   2/5))
```

Their sup-norm associativity failure is exactly `1/10`. Each wrong result differs from the correct conditional law by `1/20`. The control passes only when these separations are present; an accidentally zero separation is a failed negative control.

### 6.4 Gauge invariance and relabeling naturality

The gauge test does not pass frames to a function that simply ignores them. It constructs the scalar attention law from typed gauge-covariant inputs in a two-dimensional local fiber at each node:

```text
r_i       receiver vector
q_i       receiver covector
k_j       source vector
U_ij      source-j to receiver-i transport

occupancy_logit_i = q_i r_i
source_logit_ij   = q_i U_ij k_j
alpha             = softmax_i(occupancy_logit)
beta_i            = softmax_j(source_logit_i)
eta_ij            = alpha_i beta_ij.
```

The pinned two-node gauge fixture uses

```text
r0 = (1, 2)                 q0 = (2, -1/2)
r1 = (-1, 1)                q1 = (1/3, 2)
k0 = (1, -1)                k1 = (2, 1/2)

U00 = ((1, 0), (0, 1))      U01 = ((1, 1/2), (0, 1))
U10 = ((2, 0), (1/3, 1))    U11 = ((1, 0), (-1/4, 3/2))

G0 = ((2, 1/2), (0, 1))
G1 = ((1, 0), (1/3, 3/2))
```

The independent invariant logits are

```text
occupancy_logits = (1, 5/3)
source_logits = ((5/2, 17/4),
                 (-2/3, 7/6)).
```

For independently chosen, fixed, positive-determinant and well-conditioned local frames `G_i`, recompute the law after

```text
r_i'  = G_i r_i
q_i'  = q_i G_i^-1
k_i'  = G_i k_i
U_ij' = G_i U_ij G_j^-1.
```

Both contractions are invariant algebraically, so the recomputed logits, `alpha`, `beta`, and `eta` must agree within scale-aware float64 tolerance. Frame determinants and condition numbers are validated before transformation, and linear solves are used instead of materializing inverses. The fixture uses nonorthogonal `GL+(2)` matrices and nonidentity links so the check is not reducible to Euclidean orthogonal invariance. A negative control transforms the vectors but intentionally leaves the links fixed and must change the resulting event law.

Separately, a cyclic node permutation is applied coherently to the event law and both partition axes. The pulled-back coarse event law must agree exactly with the original result. Relabeling only `eta` while leaving a partition fixed is a mismatch control and must generically differ. This metric is named `finite_relabeling_naturality`; it is not presented as holonomy or as a replacement for the local-frame gauge test.

## 7. Parametric categorical DQM model

### 7.1 Generic finite exponential family

`CategoricalExponentialFamily` stores base logits `b_x` and sufficient statistics `T_xa` and defines

```text
p_theta(x) = exp(b_x + T_x theta - logsumexp(b + T theta)).
```

It exposes stable log probabilities, probabilities, analytic scores, and Fisher information:

```text
score_theta(x) = T_x - E_p[T]
I(theta) = sum_x p_theta(x) score_theta(x) score_theta(x).T.
```

Validation requires finite arrays, at least two categories, at least one parameter, consistent dimensions, and finite theta. Probabilities are strictly positive by construction in float64 for the preregistered regime. Every returned array is a defensive, read-only value.

### 7.2 Exact default family and channel

The default two-parameter family is

```text
p_theta = softmax(theta_0, theta_1, 0).
```

At `theta_star = (log 2, log 3)`, the independent exact oracles are

```text
p = (1/3, 1/2, 1/6)

score =
  (( 2/3, -1/2),
   (-1/3,  1/2),
   (-1/3, -1/2))

K = ((1,   0),
     (0,   1),
     (1/2, 1/2))

p_coarse = (5/12, 7/12)

conditional_score =
  (( 7/15, -1/2),
   (-1/3,   5/14))

I_fine =
  (( 2/9, -1/6),
   (-1/6,  1/4))

I_coarse =
  (( 7/45, -1/6),
   (-1/6,   5/28))

Fisher_defect = I_fine - I_coarse =
  ((1/15, 0),
   (0, 1/14))
```

The defect is strictly positive definite with minimum eigenvalue `1/15`, making the PSD control sensitive to sign errors. A deliberately wrong score omits the source probability and uses only column-normalized kernel weights:

```text
wrong_score(z) = sum_x K(x,z) score(x) / sum_x K(x,z)
```

for positive-support target columns. It differs from the correct conditional score by exactly `4/21` in sup norm and is recorded as a weighting negative control.

### 7.3 Analytic DQM evidence

For every category `x` in the declared finite support, `p_theta(x)` is positive and smooth. Therefore `f_x(theta) = sqrt(p_theta(x))` is continuously differentiable and

```text
gradient f_x(theta) = (1/2) sqrt(p_theta(x)) score_theta(x).
```

Finite-dimensional Taylor expansion gives, for an arbitrary two-sided vector increment `h`,

```text
sqrt(p_(theta+h)(x))
  - sqrt(p_theta(x))
  - (1/2) sqrt(p_theta(x)) score_theta(x).T h
  = r_x(h),

r_x(h) = o(||h||).
```

Because the support is finite,

```text
sum_x r_x(h)^2 = o(||h||^2).
```

This is the two-sided finite-support DQM definition with the displayed analytic score. The derivation is the mathematical evidence for this specific family. The executable remainder table below is a separate implementation check and is not used as the proof.

### 7.4 Finite-difference and DQM checks

For each parameter coordinate, use centered finite differences of `log p_theta` and independently of `log(p_theta K)`. Compare them respectively with the analytic fine score and the conditional-expectation coarse score.

For direction `v = (3/5, -4/5)`, both signs, and the configured positive step ladder, record

```text
|| sqrt(p_(theta+h v) / p_theta)
   - 1
   - (h/2) score_theta v ||_(L2(p_theta)) / |h|.
```

The square-root likelihood ratio is evaluated from log probabilities using `expm1(0.5 * delta_log_probability)` rather than subtracting nearly equal square roots. The default ladder is `(0.1, 0.05, 0.025, 0.0125)`. Its normalized remainder must decrease toward zero for both signs. The final default values are approximately `7.02e-4`; tests use scale-aware tolerances and do not treat the numerical trend as an analytic proof. For edited theta or step ladders, monotonicity is diagnostic rather than a universal pass condition.

The production Fisher path computes:

1. the analytic fine score and fine Fisher tensor;
2. the joint mass `p_x K_xz`;
3. the conditional-expectation coarse score;
4. the coarse Fisher tensor;
5. expected conditional score covariance;
6. the independently formed residual `I_fine - I_coarse - defect`.

The coarse finite-difference score is an additional independent oracle rather than an input to the conditional-expectation calculation.

The API accepts a concrete `MarkovKernel`, not a callable channel family. The result and manifest explicitly record `channel_scope = "declared_fixed_parameter_independent"`. This is a load-bearing assumption, not something inferred mechanically from the kernel object; generic rejection or verification of parameter dependence is outside this laboratory.

## 8. Metrics and claim registry

| ID | Status | Observable | Passing requirement |
|---|---|---|---|
| ATT-01 | Established conditional identity; implementation check | factorization and normalization residuals | scale-aware zero |
| ATT-02 | Established conditional identity; implementation check | direct-versus-staged state-bridge and node-partition residuals for `eta`, `alpha`, and active-row `beta` | scale-aware zero and exact fixture literals |
| ATT-03 | Established scalar-gauge identity; implementation check | recomputed local-frame invariant logits, `alpha`, `beta`, and `eta` | scale-aware zero; broken-link negative control nonzero |
| ATT-04 | Finite relabeling naturality check | coherent relabeling residual | scale-aware zero; incoherent mismatch control nonzero |
| ATT-NEG-01 | Deliberately incorrect control | beta-only direct/staged and correct/wrong separations | `1/10` and `1/20` at the default fixture; nonzero generally |
| DQM-01 | Analytically established for the declared smooth positive finite family; numerical implementation check separate | finite-support Taylor derivation, analytic/finite-difference score error, and two-sided remainder ladder | derivation bound to family; FD error within tolerance; default remainder sequences decrease |
| INF-02 | Established conditional identity; implementation check | coarse conditional/FD score error and Fisher covariance residual | scale-aware zero |
| INF-NEG-01 | Deliberately incorrect control | unweighted-versus-conditional score gap | `4/21` at the default fixture; nonzero generally |

Metric JSON deliberately retains the established schema: `value`, `tolerance`, `status`, `interpretation`, `assessment_scope`, and `theorem_status`. Claim IDs remain in stable metric keys such as `ATT-02_direct_staged_eta_residual`; no incompatible comparator/disposition schema is introduced. The default exact-oracle and pinned negative-control values are emitted as pass/fail checks only when the resolved default fixture and parameter are used. A changed parameter receives the generic analytic/finite-difference and identity checks, while any wrong-weight gap is retained as a diagnostic rather than pretending the rational default literals still apply.

## 9. Artifact contract

Each laboratory writes the existing immutable numerical bundle:

- `config.json`
- `manifest.json`
- `metrics.json`
- `arrays.npz`
- optional `diagnostics.npz`

Attention core arrays include state probabilities, state-conditioned fine, middle, direct-coarse, staged-coarse, and beta-only-control `alpha`, `beta`, `eta`, and active masks. Diagnostics include state channels, reverse bridges, node partition kernels, local gauge frames and transformed covariant inputs, permutation matrices, and relabeled intermediates.

DQM core arrays include theta, probabilities, analytic and finite-difference scores, the fixed channel, coarse probabilities and scores, fine/coarse Fisher tensors, defect, identity residual, step ladder, and two-sided remainder table. Diagnostics include joint masses, conditional covariance contributions, and the unweighted-score control.

`collect_diagnostics` controls only the optional diagnostic bundle. `render_figures` is evaluated only after numerical finalization; rendering failure cannot change numerical metric bytes or status. The new laboratories use a shared Gaussian-strength renderer validator that checks the returned status against the on-disk figure manifest, containment, inventory, and content hashes. Forged, missing, or unbacked success/failure results are rejected and recorded as rendering failures without changing the finalized numerical bundle. Invalid configuration fails before RNG creation or filesystem writes.

Runs under different artifact roots necessarily have different resolved output configuration and run-directory hashes. Holding every semantic input and the seed fixed while changing only `OUTPUT["root"]` must nevertheless produce byte-identical `metrics.json` and `arrays.npz`; root-dependent `config.json` and manifest fields are not compared as if they were identical. Existing completed bundles are never overwritten.

## 10. Figures and visual-companion decision

No separate interactive visualization or GUI accompanies this feature. The mathematical relations are more clearly represented by exact arrays and small saved-artifact figures than by a new user interface.

The existing pure renderer gains two names:

- `attention_composition`: four compact panels showing direct coarse `eta` at each final state, the staged-minus-direct residual summarized over states, and the beta-only-minus-correct residual.
- `categorical_dqm`: analytic-versus-finite-difference score comparison and a log-log two-sided DQM remainder ladder.

Figures are reconstructed only from finalized `metrics.json` and `arrays.npz`, use the established noninteractive and transactional rendering policy, and remain optional through the existing output dictionary. Captions are experiment-specific: the attention plot says that it is a finite exact state-conditioned fixture, while the DQM plot identifies the resolved theta and finite-difference/remainder settings. Neither reuses the older hardcoded `n=1 exact fixture` caption.

## 11. Test strategy

Implementation follows red-green-refactor TDD. Required independent tests include:

### Attention primitives

- exact `eta = diag(alpha) beta`, nonnegativity, and unit mass;
- validation of shapes, labels, finiteness, normalization, and numerical-policy agreement;
- defensive copies and read-only outputs;
- positive-state/receiver disintegration and explicit zero-state/zero-occupancy masks without NaN or Inf;
- literal middle and final rational matrices;
- direct/staged state-bridge plus node-partition equality, exact reverse-bridge weights, and independent kernel composition;
- genuine local `GL+(2)` recomputation invariance plus a broken-link transformation negative control;
- coherent cyclic relabeling naturality plus an incoherent mismatch control;
- pinned beta-only direct/staged failure `1/10` and correct/wrong separation `1/20`.

### Categorical DQM primitives

- stable normalization and analytic score centering at multiple theta values;
- exact default probabilities, scores, coarse scores, Fisher tensors, and defect;
- fine and pushed-family centered finite differences against analytic oracles;
- both signs of the DQM remainder and decreasing default step ladder;
- strict-positive-defect PSD checks and the `4/21` wrong-weight control;
- rejection of malformed families, theta, ineffective perturbations, zero represented support, and invalid steps;
- explicit fixed-parameter-independent channel scope without claiming that a bare kernel object proves that assumption.

### Integration

- strict discriminated configuration parsing with unchanged legacy canonical JSON;
- all four output-toggle combinations for both experiments;
- deterministic numerical artifacts across roots;
- wrong-experiment rejection before seeding or writes;
- rendering failure isolation after numerical finalization, including forged or unbacked renderer statuses;
- figure replay from finalized artifacts only;
- launcher imports have no side effects;
- sanitized subprocess click-to-run tests with no editable install, no `PYTHONPATH`, and no arguments.

The final suite is recorded as current JUnit XML. Independent code and mathematical reviews must resolve all Critical and Important findings before closure.

## 12. Verification and completion

The existing `.verification/ledger.json` is extended with one claim per ATT/DQM/INF check and rebound to the final artifact revision. Code and experiment claims require current machine-readable tests and reproduced launcher artifacts. Mathematical status comes from the frozen derivations, not numerical agreement. The ledger must validate before reporting evidence closure.

The feature is complete when:

1. both root launchers run by clicking or direct Python execution with no arguments;
2. the default rational and finite-difference oracles pass;
3. attention direct and staged state-bridge plus node-partition event-law pushforwards agree while the beta-only control fails as pinned;
4. categorical analytic and finite-difference scores agree and the Fisher-defect identity closes;
5. local-frame gauge, zero-occupancy, relabeling, validation, artifact, rendering, and deterministic-replay tests pass;
6. the full suite has zero failures and errors in current JUnit evidence;
7. the verification ledger validates at the final revision; and
8. documentation states the exact finite scope and all deferred claims.

## 13. Explicit deferrals

This slice does not add arbitrary family/partition serialization, learned attention, neural training, parameter sweeps, GPU code, continuous-state DQM, bundle-valued attention, nontrivial `GL(K)` holonomy, natural-gradient histories, partition selection, continuum limits, or universality tests. The pure APIs are designed so later laboratories can add these without weakening the exact oracle boundary.
