# Gauge-VFE-RG Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first exact finite and Gaussian simulation laboratories for the conditional `gauge_vfe_rg` theory, with click-to-run config dictionaries, reproducible atomic artifacts, and evidence-gated verification.

**Architecture:** A finite categorical probability core implements measure-pair pushforward, exact VFE decompositions, Fisher contraction, and full finite interactions. Gauge tests are representation metamorphics, while all matrix-weighted Gaussian/RG machinery is isolated under `realizations/gaussian`. Thin launchers resolve frozen typed configuration and call importable experiment APIs.

**Tech Stack:** Python 3.14, NumPy 2.x, SciPy 1.x, Matplotlib 3.x, pytest 9.x, standard-library dataclasses/JSON/hashlib/pathlib.

## Global Constraints

- No `argparse`, Click, Typer, or CLI-first interface.
- User settings live in editable Python dictionaries in click-to-run files.
- Launchers contain no mathematical implementation and expose a thin `main()`.
- The supplied `Theory/` snapshot is read-only and must remain byte-identical to its pre-build state.
- Universal finite probability code must not import Gaussian realization modules.
- A fixed generative law must never accept recognition state as an input.
- Every coarse identity applies one declared normalized Markov channel to all compared measures.
- Retained sparse/pairwise approximations always report an explicit full-space residual in the theorem's coordinate `G` norm; weighted L2 may be recorded only as a separately named diagnostic.
- Gaussian singularity is an error unless a distinct repaired model is explicitly declared; no silent pseudoinverse.
- Config validation occurs before RNG creation and before artifact-directory creation.
- Resolved configuration is frozen, canonicalized once, hashed once, and recorded in every run manifest.
- Named RNG streams derive from one `numpy.random.SeedSequence`; no global NumPy RNG state.
- All JSON/NPZ artifacts publish atomically and runs never silently overwrite prior complete results.
- Numerical checks are finite corroboration only and never close universality, attraction, infinite-volume, or physical-law claims.
- American English is required in code, comments, docs, and artifacts.

---

### Task 1: Repository foundation, strict configuration, and atomic run store

**Files:**
- Create: `.gitignore`
- Create: `.gitattributes`
- Create: `pyproject.toml`
- Create: `src/multiagent_elbo/__init__.py`
- Create: `src/multiagent_elbo/config.py`
- Create: `src/multiagent_elbo/runtime.py`
- Create: `src/multiagent_elbo/artifacts.py`
- Create: `tests/test_config.py`
- Create: `tests/test_runtime.py`
- Create: `tests/test_artifacts.py`
- Create: `docs/theory-provenance.md`
- Copy without modification: `C:\Users\chris and christine\Desktop\Research\manuscripts\references.bib` to `references.bib`
- Track without modification: `Theory/**` except generated caches/build products

**Interfaces:**
- Produces: `ExperimentConfig.from_dicts(run, theory, numerics, output) -> ExperimentConfig`
- Produces: `canonical_config_json(config) -> str` and `config_sha256(config) -> str`
- Produces: `RngStreams.from_seed(seed) -> RngStreams`
- Produces: `RunStore.create(config, provenance) -> RunStore`
- Produces: `RunStore.write_json(name, payload)` and `RunStore.write_npz(name, arrays)`
- Produces: `collect_provenance(repo_root, theory_root, config_hash, streams) -> dict[str, object]`

- [ ] **Step 1: Write strict configuration tests**

Create tests that name the breaks they catch:

```python
def test_unknown_config_key_is_rejected():
    run, theory, numerics, output = valid_dicts()
    run["mystery"] = 1
    with pytest.raises(ConfigError, match="unknown run key: mystery"):
        ExperimentConfig.from_dicts(run, theory, numerics, output)

def test_bool_is_not_accepted_as_integer_seed():
    run, theory, numerics, output = valid_dicts()
    run["seed"] = True
    with pytest.raises(ConfigError, match="seed must be an int, not bool"):
        ExperimentConfig.from_dicts(run, theory, numerics, output)

def test_invalid_config_has_no_filesystem_side_effect(tmp_path):
    run, theory, numerics, output = valid_dicts(tmp_path)
    theory["retained_interaction_order"] = 0
    with pytest.raises(ConfigError):
        ExperimentConfig.from_dicts(run, theory, numerics, output)
    assert list(tmp_path.iterdir()) == []
```

- [ ] **Step 2: Run the configuration tests and confirm RED**

Run: `C:\Python314\python.exe -m pytest tests/test_config.py -q -p no:cacheprovider`

Expected: collection/import failure because `multiagent_elbo.config` does not exist.

- [ ] **Step 3: Implement frozen typed configuration**

Implement exact-key parsing for:

```python
@dataclass(frozen=True)
class RunConfig:
    name: str
    seed: int

@dataclass(frozen=True)
class TheoryConfig:
    experiment: Literal["finite_exact", "gaussian_realization"]
    retained_interaction_order: int | None

@dataclass(frozen=True)
class NumericsConfig:
    dtype: Literal["float64"]
    atol: float
    rtol: float

@dataclass(frozen=True)
class OutputConfig:
    root: Path
    collect_diagnostics: bool
    render_figures: bool

@dataclass(frozen=True)
class ExperimentConfig:
    run: RunConfig
    theory: TheoryConfig
    numerics: NumericsConfig
    output: OutputConfig
```

Reject `retained_interaction_order < 1`, nonpositive tolerances, path traversal in run names, non-`float64`, exact-type mistakes, and all unknown keys. Canonical JSON uses sorted keys and compact separators; the hash is lowercase SHA-256.

- [ ] **Step 4: Verify configuration GREEN**

Run the command from Step 2. Expected: all configuration tests pass with no warnings.

- [ ] **Step 5: Write failing RNG and artifact tests**

Test that two equal seeds produce identical named stream draws, distinct stream names do not produce equal initial draws, a canonical hash is stable across source-dictionary insertion order, a completed run is not overwritten, JSON publication leaves no temporary file, and all manifest/config references carry the same config hash.

- [ ] **Step 6: Run RNG/artifact tests and confirm RED**

Run: `C:\Python314\python.exe -m pytest tests/test_runtime.py tests/test_artifacts.py -q -p no:cacheprovider`

Expected: import failure for missing runtime/artifact interfaces.

- [ ] **Step 7: Implement named streams and atomic run store**

Use `SeedSequence(seed).spawn(4)` for streams named `problem`, `recognition`, `controls`, and `figures`. Publish JSON through a same-directory temporary file, `flush`, `os.fsync`, and `os.replace`. Publish NPZ through an opened binary temporary file so NumPy cannot append an unexpected suffix. A run path is `<root>/<sanitized-name>/<config-hash>-<seed>` and creation fails closed when a complete manifest already exists.

- [ ] **Step 8: Verify RNG/artifact GREEN and foundation suite**

Run: `C:\Python314\python.exe -m pytest tests/test_config.py tests/test_runtime.py tests/test_artifacts.py -q -p no:cacheprovider`

Expected: all tests pass; no `.tmp` files remain.

- [ ] **Step 9: Record theory provenance without modifying Theory**

Write `docs/theory-provenance.md` with the source path, Research `HEAD`, dirty-state caveat, snapshot timestamp, byte-match result for the 44 supplied non-cache files, and the rule that the archived `current-results.json` is revision-bound rather than fresh evidence. Add ignore rules for `__pycache__`, `*.pyc`, pytest caches, TeX auxiliaries, `artifacts/`, and `.superpowers/`. Keep `.verification/ledger.json` and durable verification evidence trackable.

- [ ] **Step 10: Run source-preservation and packaging checks**

Run a hash comparison between tracked `Theory/` files and the pre-build manifest. Run: `C:\Python314\python.exe -m pytest tests/test_config.py tests/test_runtime.py tests/test_artifacts.py -q -p no:cacheprovider`.

Expected: zero theory-content differences and all foundation tests pass.

- [ ] **Step 11: Commit Task 1**

Commit message: `feat: establish typed reproducible experiment foundation`

---

### Task 2: Finite measure-pair, exact VFE, and local-to-collective identities

**Files:**
- Create: `src/multiagent_elbo/finite/__init__.py`
- Create: `src/multiagent_elbo/finite/measures.py`
- Create: `src/multiagent_elbo/finite/vfe.py`
- Create: `tests/test_measures.py`
- Create: `tests/test_vfe.py`

**Interfaces:**
- Consumes: `NumericsConfig`
- Produces: `FiniteMeasure`, `ProbabilityMeasure`, `MarkovKernel`, `MeasurePair`
- Produces: `kl_divergence(q, p) -> float`
- Produces: `free_energy(q, pair) -> float`
- Produces: `vfe_channel_decomposition(q, pair, channel) -> VfeChannelResult`
- Produces: `block_update_decomposition(posterior, q_before, q_after, block_axes) -> BlockUpdateResult`

- [ ] **Step 1: Write failing finite-measure tests from literal fixtures**

Use support `("00", "01", "10", "11")`, reference masses `rho=(0.25,0.25,0.25,0.25)`, unnormalized evidence-submeasure masses `m_o=(0.2,0.4,0.6,0.8)`, and deterministic channel rows `A,A,B,B`. Assert fine and coarse evidence both equal literal `2.0`, coarse reference is `(0.5,0.5)`, coarse evidence submeasure is `(0.6,1.4)`, fine density `dm_o/drho` is `(0.8,1.6,2.4,3.2)`, coarse density is `(1.2,2.8)`, and a non-row-stochastic matrix is rejected.

- [ ] **Step 2: Run finite-measure tests and confirm RED**

Run: `C:\Python314\python.exe -m pytest tests/test_measures.py -q -p no:cacheprovider`

Expected: import failure for the missing finite package.

- [ ] **Step 3: Implement validated finite measures and kernels**

Preserve ordered labels and validate uniqueness. `FiniteMeasure` permits finite nonnegative mass; `ProbabilityMeasure` additionally requires total mass one within configured tolerance. `MarkovKernel` requires finite nonnegative entries and row sums one. Pushforward is right multiplication by the kernel matrix. `MeasurePair(reference, evidence_measure)` enforces `m_o << rho`; `posterior()` normalizes the finite positive evidence submeasure and refuses zero evidence. Never call `m_o` a pointwise likelihood.

- [ ] **Step 4: Verify finite-measure GREEN**

Run the command from Step 2. Expected: all tests pass.

- [ ] **Step 5: Write failing VFE chain-rule tests with hand-derived values**

Use posterior `p=(0.1,0.2,0.3,0.4)`, recognition `q=(0.2,0.3,0.1,0.4)`, and channel `A,A,B,B`. Assert:

```python
fine_kl = 0.2*log(2.0) + 0.3*log(1.5) + 0.1*log(1.0/3.0)
coarse_kl = 0.5*log(5.0/3.0) + 0.5*log(5.0/7.0)
assert result.fine_vfe == pytest.approx(fine_kl - log(2.0))
assert result.coarse_vfe == pytest.approx(coarse_kl - log(2.0))
assert result.conditional_kl == pytest.approx(fine_kl - coarse_kl)
assert result.residual == pytest.approx(0.0, abs=1e-12)
```

Add a support-violation case that returns a structured extended-real result with `fine_vfe=math.inf`, the offending state, and `residual=None`; do not evaluate `inf-inf`. Add a recoverable channel control with finite zero conditional KL and zero ordinary residual.

- [ ] **Step 6: Write a failing local-to-collective block-update test**

Use a literal two-binary-variable posterior table `[[0.10,0.20],[0.30,0.40]]`, with rows the block variable `y0`, columns the outside variable `y1`, and `block_axes=(0,)`. The conditional pairs are `q(y0|y1=j)`. With outside marginal `(0.35,0.65)`, use `q_before=[[0.21,0.13],[0.14,0.52]]` from conditionals `((0.6,0.4),(0.2,0.8))` and `q_after=[[0.14,0.325],[0.21,0.325]]` from `((0.4,0.6),(0.5,0.5))`. In the test, compute the expected outside-weighted conditional posterior-KL difference by explicit scalar expressions, not a production helper, and assert both it and the collective VFE difference equal `-0.06702325206172067`. The identity is for a difference; evidence and local-normalizer constants cancel.

- [ ] **Step 7: Run VFE tests and confirm RED**

Run: `C:\Python314\python.exe -m pytest tests/test_vfe.py -q -p no:cacheprovider`

Expected: missing VFE interface failures.

- [ ] **Step 8: Implement VFE and block decompositions**

Compute KL only on `q>0`; return infinity with an undefined numeric residual when `q>0` and `p=0`. Build reverse conditionals from each source measure and the shared channel. The conditional-KL term is weighted by the coarse recognition law. For the reduced block identity, require exactly equal outside marginals and compute both sides independently. If a future approximate mode is added, it must retain and report the outside-marginal KL change instead of asserting the reduced identity.

- [ ] **Step 9: Verify Task 2 GREEN and regression suite**

Run: `C:\Python314\python.exe -m pytest tests/test_measures.py tests/test_vfe.py tests/test_config.py tests/test_runtime.py tests/test_artifacts.py -q -p no:cacheprovider`

Expected: all tests pass.

- [ ] **Step 10: Commit Task 2**

Commit message: `feat: add exact finite VFE laboratory core`

---

### Task 3: Fisher contraction, full interactions, finite gauge metamorphics, and finite launcher

**Files:**
- Create: `src/multiagent_elbo/finite/fisher.py`
- Create: `src/multiagent_elbo/finite/interactions.py`
- Create: `src/multiagent_elbo/finite/experiment.py`
- Create: `src/multiagent_elbo/geometry/__init__.py`
- Create: `src/multiagent_elbo/geometry/finite_gauge.py`
- Create: `tests/test_fisher.py`
- Create: `tests/test_interactions.py`
- Create: `tests/test_finite_experiment.py`
- Create: `tests/test_launchers.py`
- Create: `run_finite_lab.py`
- Create: `docs/hypotheses.md`

**Interfaces:**
- Consumes: Task 1 config/runtime/artifacts and Task 2 finite measures/VFE
- Produces: `fisher_channel_decomposition(probability, score, channel) -> FisherChannelResult`
- Produces: `hoeffding_decompose(values, axis_references) -> InteractionDecomposition`
- Produces: `apply_site_relabeling(...)` and gauge-invariance residuals
- Produces: `run_finite_experiment(config) -> FiniteExperimentResult`

- [ ] **Step 1: Write failing Fisher tests with literal oracles**

At a uniform four-state law, use statistic `t=(-1,0,1,2)`, centered score `(-1.5,-0.5,0.5,1.5)`, and channel `A,A,B,B`. Assert fine Fisher `1.25`, coarse score `(-1,1)`, coarse Fisher `1.0`, conditional-covariance defect `0.25`, and residual zero. Add a weighting-discriminating stochastic oracle `p=(1/2,1/3,1/6)`, `score=(-1,1,1)`, and `K=((1,0),(1/2,1/2),(0,1))`; assert `p_c=(2/3,1/3)`, coarse score `(-1/2,1)`, fine Fisher `1`, coarse Fisher `1/2`, and defect `1/2`. Add an identity-channel control, a genuinely lossy channel with fiber-constant score `(-1,-1,1,1)` and zero defect, accept the zero constant score as a valid zero tangent, and reject a nonzero constant vector because it is not centered. Add a two-parameter singular-PSD control with score rows `[(-3/2,-1),(-1/2,1),(1/2,-1),(3/2,1)]`, whose defect is `[[1/4,1/2],[1/2,1]]` with eigenvalues `(0,5/4)`; do not require positive definiteness or add jitter. Type this as the finite conditional-expectation/covariance identity for a supplied centered score and declared-fixed parameter-independent kernel; the vector test alone does not establish DQM or verify parameter independence across a family.

- [ ] **Step 2: Run Fisher tests and confirm RED**

Run: `C:\Python314\python.exe -m pytest tests/test_fisher.py -q -p no:cacheprovider`

Expected: missing Fisher interface failure.

- [ ] **Step 3: Implement analytic finite Fisher decomposition**

Support scores shaped `(n,)` or `(n,d)`, promote the scalar form internally to `(n,1)`, and use fixed result ranks: joint mass `(n,m)`, coarse probability `(m,)`, coarse score `(m,d)`, and Fisher/defect/residual arrays `(d,d)`. Center-check each parameter coordinate with `abs(p @ score)[j] <= atol + rtol*max(1, p @ abs(score[:,j]))`. Compute conditional means from `p_x*K_xz`, assigning zero only as the explicit representative on unreachable coarse targets. Compute fine Fisher, coarse Fisher, and expected conditional covariance independently from their weighted outer-product definitions; only then form `residual = fine - coarse - covariance`. Use scale-aware symmetric-eigenvalue PSD diagnostics without clipping, jitter, Cholesky, or positive-definite assumptions. Return read-only defensive copies in a frozen `FisherChannelResult`.

- [ ] **Step 4: Verify Fisher GREEN**

Run the command from Step 2. Expected: all tests pass.

- [ ] **Step 5: Write failing interaction tests**

Use three independent uniform spin axes `{-1,+1}` and values `phi(x)=0.7*x1*x2*x3`. Assert the empty component is zero, all node/pair components are zero, the triple component equals `phi`, and full reconstruction residual is below `1e-12`. Add a discriminating four-spin pairwise-retained oracle `phi=0.3*x1*x2*x3+0.4*x1*x2*x4`: its theorem-coordinate `G` residual norm is `0.3+0.4=0.7`, its quotient sup norm is `0.7`, and its separately named weighted L2 diagnostic is `sqrt(0.3**2+0.4**2)=0.5`. Add a nonuniform binary product-reference fixture to catch accidental uniform averaging.

- [ ] **Step 6: Run interaction tests and confirm RED**

Run: `C:\Python314\python.exe -m pytest tests/test_interactions.py -q -p no:cacheprovider`

Expected: missing interaction interface failure.

- [ ] **Step 7: Implement full subset decomposition and retained projection**

For each subset, conditionally average over complement axes against the declared product reference and apply Boolean inclusion-exclusion. Store components by sorted tuple of axis indices, reconstruct by broadcasting, and report omitted components, the theorem-coordinate norm `sum_A ||g_A||_infinity`, the action quotient sup norm, and a separately labeled weighted L2 diagnostic.

- [ ] **Step 8: Write failing finite gauge metamorphic tests**

For row-law permutation matrices use `q'=q P_X`, `p'=p P_X`, `rho'=rho P_X`, `m'=m P_X`, and `K'=P_X.T K P_Z`, so `q'K'=(qK)P_Z`. Push every axis reference forward, pull the action/value array back, and intertwine the retained projection. Assert invariant evidence, KL, VFE, conditional-KL loss, and full-interaction residuals. Pin the negative control to Task 2: flip the first bit of `q` only, giving `q'=(0.1,0.4,0.2,0.3)`, and assert `KL(q'||p)-KL(q||p)=(log(2)-log(3))/10=-0.04054651081081644`. Scope this laboratory to componentwise finite Borel relabelings, not arbitrary gauge fields or holonomy.

- [ ] **Step 9: Implement finite relabeling helpers and verify interaction/gauge GREEN**

Run: `C:\Python314\python.exe -m pytest tests/test_interactions.py tests/test_finite_experiment.py -q -p no:cacheprovider`

Expected: all tests pass.

- [ ] **Step 10: Write failing launcher smoke test**

Load `run_finite_lab.py` by file path, replace only the output root with `tmp_path`, call `main()`, and assert a typed result plus one complete run bundle. Assert the module contains no parser object by behavior: importing it neither reads process arguments nor writes files.

- [ ] **Step 11: Implement the finite experiment and click-to-run launcher**

The launcher defines `RUN`, `THEORY`, `NUMERICS`, and `OUTPUT`. `main()` resolves them and calls `run_finite_experiment`. The experiment uses the pre-registered literal fixtures, named controls, and writes config, manifest, metrics, and arrays. Each metric has `value`, `tolerance`, `status`, and `interpretation` fields.

- [ ] **Step 12: Document the hypothesis registry**

Write complete FIN-01, FIN-02, FIN-03, INF-01, INT-01, GAU-01, GAU-02, and deferred RG-01 entries with epistemic status, prediction, null, operationalization, control, support threshold, refutation threshold, inconclusive rule, and theory source pointer. FIN-01/02/03, INF-01, INT-01, finite relabeling invariance, generalized-spectrum congruence, and Gaussian aggregation under its declared family are established conditional identities whose tests verify this implementation; the Gaussian interaction-family declaration is a hypothesis; RG attraction/universality remains conjectural or open.

- [ ] **Step 13: Verify Task 3 GREEN and same-seed determinism**

Run the finite launcher twice against separate temporary roots with the same seed and compare metrics/arrays byte-for-byte after excluding path/time provenance. Run: `C:\Python314\python.exe -m pytest tests/test_fisher.py tests/test_interactions.py tests/test_finite_experiment.py tests/test_launchers.py -q -p no:cacheprovider`.

Expected: all tests pass and both semantic outputs match.

- [ ] **Step 14: Commit Task 3**

Commit message: `feat: add finite Fisher interaction and gauge experiments`

---

### Task 4: Gaussian realization, replayable figures, documentation, and current verification

**Files:**
- Create: `src/multiagent_elbo/realizations/__init__.py`
- Create: `src/multiagent_elbo/realizations/gaussian/__init__.py`
- Create: `src/multiagent_elbo/realizations/gaussian/interactions.py`
- Create: `src/multiagent_elbo/realizations/gaussian/gauge.py`
- Create: `src/multiagent_elbo/realizations/gaussian/experiment.py`
- Create: `src/multiagent_elbo/figures.py`
- Create: `tests/test_gaussian_realization.py`
- Create: `tests/test_figures.py`
- Create: `run_gaussian_lab.py`
- Create: `make_figures.py`
- Create: `README.md`
- Create: `docs/results/2026-08-08-foundation-results.md`
- Create: `.verification/ledger.json`
- Create: `docs/verification/pytest-foundation.xml`
- Modify: `src/multiagent_elbo/config.py`
- Modify: `tests/test_config.py`
- Modify: `run_finite_lab.py`

**Interfaces:**
- Consumes: Task 1 config/runtime/artifacts
- Produces: `GaussianInteraction.from_self_and_edges(...)`
- Produces: `aggregate_precision(interaction, partition) -> GaussianAggregationResult`
- Produces: `apply_frame_change(...) -> GaussianGaugeResult`
- Produces: `run_gaussian_experiment(config) -> GaussianExperimentResult`
- Produces: `render_run(run_dir, output_dir) -> FigureManifest`

- [ ] **Step 1: Write failing Gaussian aggregation tests from a literal matrix**

For scalar self terms `(1,2,3)`, edges `w12=4`, `w23=5`, and partition `{0,1}|{2}`, assert the fine precision is

```python
[[5.0, -4.0, 0.0],
 [-4.0, 11.0, -5.0],
 [0.0, -5.0, 8.0]]
```

and the coarse precision is `[[8.0,-5.0],[-5.0,8.0]]`. Use code edges `(0,1):4` and `(1,2):5` with partition `{0,1}|{2}`. Assert the internal first edge cancels and the cut second edge remains. Name the public operation `galerkin_aggregate_precision` and tag its result as an operator-level hard-identification/Galerkin restriction, never a Gaussian marginal or pushed-forward law. Pin the distinct scalar Schur-complement marginal obtained by eliminating node 1 as `[[39/11,-20/11],[-20/11,63/11]]`. Add the exact `K=2` unrestricted-Kron nonclosure witness whose Schur matrix is `1/19*[[33,2,-9,-3],[2,41,-4,-14],[-9,-4,37,6],[-3,-14,6,40]]`; its manufactured off-diagonal weight `1/19*[[9,3],[4,14]]` is asymmetric. Reject an indefinite self/edge construction without adding jitter. Permit scalar shorthand only for a consistently scalar `K=1` system; reject mixed block sizes, self-loops, duplicate reversed edges, and partitions with missing, repeated, overlapping, or empty blocks.

- [ ] **Step 2: Write failing Gaussian gauge tests**

Use `W=[[1,1/5],[1/5,2]]`, `A1=diag(2,3)`, `A2=diag(4,5)`, `L=[[W,-W],[-W,W]]`, `Lambda=diag(A1,A2)+L`, positive-orientation local frame blocks whose assembled matrix is `T=diag(2,1,1,3)`, and `x=(1,2,-1,1)`. With coordinates `x'=T x`, transform both operators by inverse congruence `Lambda'=T^{-T}Lambda T^{-1}` and `L'=T^{-T}LT^{-1}`, using linear solves rather than forming an explicit inverse. Assert `x^T Lambda x=x'^T Lambda' x'=149/5` and the corresponding `L` energy is `34/5`. Pin the independent generalized roots to `{0,0,(5077-5*sqrt(14785))/10802,(5077+5*sqrt(14785))/10802}`, approximately `{0,0,0.413722650732677663,0.526288458321201249}`; also assert `det(Lambda)=10802/25`, `det(Lambda')=5401/450`, and the Cholesky-derived log-determinant difference is `-2*log(6)`. Record normalized eigenpair residuals and `V.T@Lambda@V-I`, not only agreement between two calls to the same eigensolver. Pin the negative control: ordinary `L` spectra are `{0,0,3±sqrt(29)/5}` before and `{0,0,(125±sqrt(1513))/72}` after. Do not parse transformed `L'` back into row-sum edge blocks.

Add a commuting-square aggregation control. If `y=S z`, `y'=T_f y`, and `z'=T_c z`, transform `S'=T_f S T_c^{-1}` and assert `S'^T Lambda' S'=T_c^{-T}(S^T Lambda S)T_c^{-1}`. For `S=[I;I]`, the literal `T_f` above, and `T_c=diag(5,2)`, assert `S'=[[2/5,0],[0,1/2],[1/5,0],[0,3/2]]`, `S.T@Lambda@S=diag(6,8)`, and `S'.T@Lambda'@S'=diag(6/25,2)`. Holding `S` fixed is permitted only when `T_f S=S T_c`. The frame API accepts an `(N,K,K)` collection, validates each local block's positive determinant and condition number, assembles the block diagonal internally, and returns transformed prolongators as general matrices.

- [ ] **Step 3: Run Gaussian tests and confirm RED**

Run: `C:\Python314\python.exe -m pytest tests/test_gaussian_realization.py -q -p no:cacheprovider`

Expected: missing Gaussian package failure.

- [ ] **Step 4: Implement stable Gaussian realization**

Extend `NUMERICS` with explicit persisted float toggles `min_spd_rcond` in `(0,1]` and `max_frame_condition` in `[1,infinity)`, with strict finite validation; update both launchers and configuration tests. Validation order is shape/dimension, finiteness, normalized symmetry residual, symmetric projection only within tolerance, block PSD checks with `atol+rtol*scale`, assembly, repeated finiteness/symmetry checks, Cholesky, reciprocal-condition gate, frame-condition gate, then the generalized eigensolve. Cholesky success alone does not establish acceptable conditioning. Use Cholesky solves and compute log determinant as `2*sum(log(diag(C)))`; use `scipy.linalg.eigh(L,Lambda)` for the regular pencil and retain eigenvectors for residual diagnostics. Record raw minimum eigenvalues and condition numbers as chart-dependent diagnostics, not gauge invariants. Never clamp eigenvalues, add jitter, form an explicit inverse, or call `pinv`. Generate seeded positive-orientation local frames with bounded prescribed singular spectra and add a separate over-conditioned typed-error control.

- [ ] **Step 5: Verify Gaussian GREEN**

Run the command from Step 3. Expected: all tests pass.

- [ ] **Step 6: Write failing Gaussian launcher and figure tests**

Assert click-to-run behavior, typed results, complete atomic run bundle, independent `collect_diagnostics` and `render_figures` toggles, and rendering entirely from saved metrics/arrays. A deliberately failing renderer must mark the figure failed without altering metrics or replacing an existing valid image.

- [ ] **Step 7: Implement Gaussian launcher and pure figure replay**

`run_gaussian_lab.py` follows the same four-dictionary shape as the finite launcher. `make_figures.py` has an editable dictionary containing `run_dir`, `output_dir`, and requested figure names. Render at least a signed VFE/Fisher identity-residual panel for the finite lab and matched generalized-spectrum panel for the Gaussian lab. Use a local `matplotlib.rc_context` so imports do not mutate global style: 3.5-inch publication width, 8/9/7-point body/axis/tick typography, hidden top/right spines, the Okabe-Ito colorblind-safe palette, and redundant marker/line encodings that remain legible in grayscale. Signed residuals use a symmetric scale with visible zero and tolerance boundaries; exact zeros are annotated rather than displaced. Export vector PDF plus 300-DPI PNG from the saved arrays/metrics with the noninteractive Agg backend. These are deterministic enumerated identity diagnostics, not sample estimates, so captions state `n=1 exact fixture` and do not invent error bars or significance marks.

- [ ] **Step 8: Verify launchers, figures, and full suite GREEN**

Run: `C:\Python314\python.exe -m pytest -q -p no:cacheprovider --junitxml=docs/verification/pytest-foundation.xml`

Expected: exit code zero; the JUnit XML reports zero failures/errors and contains the exact current test total.

- [ ] **Step 9: Run both click-to-run laboratories**

Run: `C:\Python314\python.exe run_finite_lab.py`

Run: `C:\Python314\python.exe run_gaussian_lab.py`

Expected: each prints its owned artifact directory and a concise status summary; both exit zero; no command-line arguments are required.

- [ ] **Step 10: Start and populate the verification control plane**

Run from the repository root:

```powershell
& "C:\Python314\python.exe" "C:\Users\chris and christine\.codex\skills\verification\scripts\verification_gate.py" start --cwd . --ledger .verification/ledger.json --mode closure
```

Add one implementation claim each for strict config/side-effect ordering, evidence/VFE identities, local-global identity, Fisher contraction, full-interaction reconstruction/residual, finite relabeling metamorphics, Gaussian aggregation, Gaussian frame invariants, atomic/reproducible artifacts, and both launcher integrations. Use current JUnit and run artifacts for code/experiment evidence. If mathematical claims are included, they require current derivation evidence from the frozen theory snapshot and must remain distinct from the code claims; JUnit and numerical agreement cannot close universal mathematics.

- [ ] **Step 11: Validate the ledger against the final live revision**

After all source/result files are staged into the intended final tree, rebind or restart the ledger if its artifact digest changed, then run:

```powershell
& "C:\Python314\python.exe" "C:\Users\chris and christine\.codex\skills\verification\scripts\verification_gate.py" validate .verification/ledger.json --cwd .
```

Expected: validation succeeds with no intermediate `CANDIDATE` or `LLM_SUPPORTED` state in closure mode. Any missing current evidence is `INCONCLUSIVE` with a named obligation.

- [ ] **Step 12: Write README and results report**

Document environment setup, two-click launcher workflow, config fields, artifact schema, exact source/theory boundary, current test totals read from JUnit, experiment results, negative controls, and deferred/open claims. Do not say the simulations prove the theory or RG universality.

- [ ] **Step 13: Re-run final verification after documentation changes**

Run the full pytest/JUnit command, both launchers, theory hash preservation check, and verification-gate validation on the exact final worktree. Inspect generated figures for nonempty readable output.

- [ ] **Step 14: Commit Task 4**

Commit message: `feat: complete gauge VFE RG foundation laboratories`
