# Gauge-VFE-RG Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first exact finite and Gaussian simulation laboratories for the conditional `gauge_vfe_rg` theory, with click-to-run config dictionaries, reproducible atomic artifacts, and evidence-gated verification.

**Architecture:** A finite categorical probability core implements measure-pair pushforward, exact VFE decompositions, Fisher contraction, and full finite interactions. Gauge tests are representation metamorphics, while all matrix-weighted Gaussian/RG machinery is isolated under `realizations/gaussian`. Thin launchers resolve frozen typed configuration and call importable experiment APIs.

**Tech Stack:** Python 3.14, NumPy 2.x, SciPy 1.x, Matplotlib 3.x, pytest 8.x, standard-library dataclasses/JSON/hashlib/pathlib.

## Global Constraints

- No `argparse`, Click, Typer, or CLI-first interface.
- User settings live in editable Python dictionaries in click-to-run files.
- Launchers contain no mathematical implementation and expose a thin `main()`.
- The supplied `Theory/` snapshot is read-only and must remain byte-identical to its pre-build state.
- Universal finite probability code must not import Gaussian realization modules.
- A fixed generative law must never accept recognition state as an input.
- Every coarse identity applies one declared normalized Markov channel to all compared measures.
- Retained sparse/pairwise approximations always report an explicit full-space residual.
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

Use support `("00", "01", "10", "11")`, reference masses `(0.25, 0.25, 0.25, 0.25)`, likelihood masses `(0.2, 0.4, 0.6, 0.8)`, and deterministic channel rows `A,A,B,B`. Assert fine and coarse evidence both equal literal `2.0`, coarse reference is `(0.5, 0.5)`, coarse likelihood is `(0.6, 1.4)`, and a non-row-stochastic matrix is rejected.

- [ ] **Step 2: Run finite-measure tests and confirm RED**

Run: `C:\Python314\python.exe -m pytest tests/test_measures.py -q -p no:cacheprovider`

Expected: import failure for the missing finite package.

- [ ] **Step 3: Implement validated finite measures and kernels**

Preserve ordered labels and validate uniqueness. `FiniteMeasure` permits finite nonnegative mass; `ProbabilityMeasure` additionally requires total mass one within configured tolerance. `MarkovKernel` requires finite nonnegative entries and row sums one. Pushforward is right multiplication by the kernel matrix. `MeasurePair.posterior()` normalizes its finite positive likelihood measure and refuses zero evidence.

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

Add a support-violation case that returns `math.inf` and identifies the offending state. Add a recoverable channel control with zero conditional KL.

- [ ] **Step 6: Write a failing local-to-collective block-update test**

Use a literal two-binary-variable posterior table `[[0.10,0.20],[0.30,0.40]]`. Construct `q_before` and `q_after` with the same second-variable marginal `(0.35,0.65)` and literal conditionals `((0.6,0.4),(0.2,0.8))` versus `((0.4,0.6),(0.5,0.5))`. In the test, compute the expected outside-weighted conditional KL difference by explicit scalar expressions, not a production helper, and assert equality to the collective KL difference.

- [ ] **Step 7: Run VFE tests and confirm RED**

Run: `C:\Python314\python.exe -m pytest tests/test_vfe.py -q -p no:cacheprovider`

Expected: missing VFE interface failures.

- [ ] **Step 8: Implement VFE and block decompositions**

Compute KL only on `q>0`; return infinity when `q>0` and `p=0`. Build reverse conditionals from each source measure and the shared channel. The conditional-KL term is weighted by the coarse recognition law. For the block identity, require exactly equal outside marginals within tolerance and compute both sides independently.

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

At a uniform four-state law, use statistic `t=(-1,0,1,2)`, centered score `(-1.5,-0.5,0.5,1.5)`, and channel `A,A,B,B`. Assert fine Fisher `1.25`, coarse score `(-1,1)`, coarse Fisher `1.0`, conditional-covariance defect `0.25`, and residual zero. Add an identity-channel control with zero defect and a constant-score rejection case.

- [ ] **Step 2: Run Fisher tests and confirm RED**

Run: `C:\Python314\python.exe -m pytest tests/test_fisher.py -q -p no:cacheprovider`

Expected: missing Fisher interface failure.

- [ ] **Step 3: Implement analytic finite Fisher decomposition**

Support vector and matrix-valued scores with the final axis as parameter dimension. Center-check the score, compute conditional means using joint probability mass, and report fine/coarse Fisher matrices, expected conditional covariance, eigenvalue diagnostics, and residual.

- [ ] **Step 4: Verify Fisher GREEN**

Run the command from Step 2. Expected: all tests pass.

- [ ] **Step 5: Write failing interaction tests**

Use three independent uniform spin axes `{-1,+1}` and values `phi(x)=0.7*x1*x2*x3`. Assert the empty component is zero, all node/pair components are zero, the triple component equals `phi`, full reconstruction residual is below `1e-12`, and the pairwise-retained residual norm is literal `0.7`. Add a nonuniform binary product-reference fixture to catch accidental uniform averaging.

- [ ] **Step 6: Run interaction tests and confirm RED**

Run: `C:\Python314\python.exe -m pytest tests/test_interactions.py -q -p no:cacheprovider`

Expected: missing interaction interface failure.

- [ ] **Step 7: Implement full subset decomposition and retained projection**

For each subset, conditionally average over complement axes against the declared product reference and apply Boolean inclusion-exclusion. Store components by sorted tuple of axis indices, reconstruct by broadcasting, and report omitted components plus their weighted L2 norm.

- [ ] **Step 8: Write failing finite gauge metamorphic tests**

Permute each binary site's labels independently in a joint law, recognition law, and deterministic coarse channel. Assert invariant evidence, KL, VFE, conditional-KL loss, and full-interaction reconstruction norm after transforming all typed objects. Add a negative control that transforms the recognition law but not the generative measure and therefore changes VFE.

- [ ] **Step 9: Implement finite relabeling helpers and verify interaction/gauge GREEN**

Run: `C:\Python314\python.exe -m pytest tests/test_interactions.py tests/test_finite_experiment.py -q -p no:cacheprovider`

Expected: all tests pass.

- [ ] **Step 10: Write failing launcher smoke test**

Load `run_finite_lab.py` by file path, replace only the output root with `tmp_path`, call `main()`, and assert a typed result plus one complete run bundle. Assert the module contains no parser object by behavior: importing it neither reads process arguments nor writes files.

- [ ] **Step 11: Implement the finite experiment and click-to-run launcher**

The launcher defines `RUN`, `THEORY`, `NUMERICS`, and `OUTPUT`. `main()` resolves them and calls `run_finite_experiment`. The experiment uses the pre-registered literal fixtures, named controls, and writes config, manifest, metrics, and arrays. Each metric has `value`, `tolerance`, `status`, and `interpretation` fields.

- [ ] **Step 12: Document the hypothesis registry**

Write complete FIN-01, FIN-02, FIN-03, INF-01, INT-01, GAU-01, GAU-02, and deferred RG-01 entries with prediction, null, operationalization, control, support threshold, refutation threshold, inconclusive rule, and theory source pointer.

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

and the coarse precision is `[[8.0,-5.0],[-5.0,8.0]]`. Assert the internal `w12` contribution cancels and the cut `w23` remains. Reject an indefinite self/edge construction without adding jitter.

- [ ] **Step 2: Write failing Gaussian gauge tests**

Use a two-agent, two-dimensional SPD system and deterministic invertible frame matrices with non-unit determinant. Transform precision and Laplacian by matched block congruence. Assert one literal quadratic-energy control and seeded metamorphic residuals below `1e-10`; assert generalized eigenvalues of `(L,Lambda)` agree below `1e-9`; assert ordinary eigenvalues generally differ as the negative control.

- [ ] **Step 3: Run Gaussian tests and confirm RED**

Run: `C:\Python314\python.exe -m pytest tests/test_gaussian_realization.py -q -p no:cacheprovider`

Expected: missing Gaussian package failure.

- [ ] **Step 4: Implement stable Gaussian realization**

Validate symmetry and PSD edge/self blocks with `scipy.linalg.eigh`; require assembled precision SPD with Cholesky. Use `cho_factor`/`cho_solve`, `slogdet` only after SPD validation, and `scipy.linalg.eigvalsh(L, Lambda)` for regular pencils. Record minimum eigenvalues, condition numbers, and residuals. Never call `pinv`.

- [ ] **Step 5: Verify Gaussian GREEN**

Run the command from Step 3. Expected: all tests pass.

- [ ] **Step 6: Write failing Gaussian launcher and figure tests**

Assert click-to-run behavior, typed results, complete atomic run bundle, independent `collect_diagnostics` and `render_figures` toggles, and rendering entirely from saved metrics/arrays. A deliberately failing renderer must mark the figure failed without altering metrics or replacing an existing valid image.

- [ ] **Step 7: Implement Gaussian launcher and pure figure replay**

`run_gaussian_lab.py` follows the same four-dictionary shape as the finite launcher. `make_figures.py` has an editable dictionary containing `run_dir`, `output_dir`, and requested figure names. Render at least a VFE/Fisher identity residual panel for the finite lab and fine/coarse generalized-spectrum panel for the Gaussian lab.

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

Add one claim each for strict config/side-effect ordering, evidence/VFE identities, local-global identity, Fisher contraction, full-interaction reconstruction/residual, finite gauge metamorphics, Gaussian aggregation, Gaussian gauge invariants, atomic/reproducible artifacts, and both launcher integrations. Use current JUnit and run artifacts for code/experiment evidence; use the frozen theorem derivations only for mathematical provenance.

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
