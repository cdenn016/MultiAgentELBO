# Gauge-Holonomy Laboratory Results — 2026-08-09

## Result boundary

This record reproduces the finite, declared graph-link laboratory at implementation revision `2016042a0f10b13e9fbfc44b8f0741b4ed09eb95`, from contract base `b80df01f239c2f9a18842f6887cdeca67dff508f`. It is mechanical implementation and finite experimental evidence. It does **not** prove a mathematical theorem, identify a graph-link assignment with a base-manifold connection, establish a dynamical gauge symmetry, or establish a continuum limit, universality, or physical time.

The only tracked additions from the contract base through the reproduced implementation revision were:

- `run_gauge_holonomy_lab.py`
- `src/multiagent_elbo/geometry/discrete_holonomy.py`
- `src/multiagent_elbo/geometry/holonomy_experiment.py`
- `tests/test_discrete_holonomy.py`
- `tests/test_holonomy_experiment.py`

This result document is the sixth and only documentation path in the Session 5 allowlist. `git diff --name-only b80df01..2016042` produced exactly the five implementation paths above; the worktree was clean apart from ignored evidence.

## Environment and commands

All CPU evidence used `C:\Python314\python.exe` (Python `3.14.4`), NumPy `2.4.4`, pytest `9.0.2`, and Coverage.py `7.15.2`. No CUDA claim is made. The no-argument launcher used its editable default dictionaries:

```python
RUN = {"name": "gauge_holonomy", "seed": 20260809}
THEORY = {
    "experiment": "gauge_holonomy",
    "fixture": "two_scale_application_v1",
    "scenario": "nonflat_plaquette",
    "group": "GL+(2)",
}
NUMERICS = {
    "dtype": "float64", "atol": 1.0e-12, "rtol": 1.0e-10,
    "min_spd_rcond": 1.0e-12, "max_frame_condition": 1.0e6,
}
OUTPUT = {
    "root": "artifacts", "collect_diagnostics": False,
    "render_figures": False,
}
```

Focused mechanical check, with a worktree-local pytest base and JUnit output:

```powershell
C:\Python314\python.exe -m pytest tests/test_discrete_holonomy.py tests/test_holonomy_experiment.py `
  --basetemp=.pytest-tmp/task3-focused `
  --junitxml=.verification/gauge-holonomy/pytest-focused.xml -q -p no:cacheprovider
```

Coverage check (direct Coverage.py branch measurement was used):

```powershell
$env:COVERAGE_FILE = "$PWD/.verification/gauge-holonomy/.coverage"
C:\Python314\python.exe -m coverage run --branch -m pytest `
  tests/test_discrete_holonomy.py tests/test_holonomy_experiment.py `
  --basetemp=.pytest-tmp/task3-coverage -q -p no:cacheprovider
C:\Python314\python.exe -m coverage xml `
  -o .verification/gauge-holonomy/coverage.xml `
  --include='src/multiagent_elbo/geometry/discrete_holonomy.py,src/multiagent_elbo/geometry/holonomy_experiment.py'
```

The click-to-run evidence harness is invoked from the worktree with:

```powershell
Set-Location "<worktree>"
C:\Python314\python.exe .verification\gauge-holonomy\run_reproduction_evidence.py
```

The ignored harness runs the launcher with no arguments in a fresh isolated working directory, then loads that run's saved `config.json`, redirects only `output.root`, and invokes the experiment for a second-root replay. Its durable latest record is `.verification/gauge-holonomy/reproduction-evidence.json` (SHA-256 `069206202c1bfbd5894138238edcaec78619e52c00a6029c040ee6404b117e2c`).

The record preserves the exact launcher command and working directory, `time.perf_counter` around `subprocess.Popen`/`communicate` as its wall-clock method, and Windows `GetProcessMemoryInfo(PROCESS_MEMORY_COUNTERS_EX)` as its primary-process working-set metric. In the fresh recorded execution, wall-clock duration was `0.3770372999988467 s`; the maximum of `19` samples taken every `0.020 s` was `42,102,784` bytes (`40.15234375 MiB`). This is a sampled process-memory observation, not a hardware-capacity assertion.

## Parsed mechanical evidence

`pytest-focused.xml` was parsed as XML, not transcribed from console output: `tests=36`, `failures=0`, `errors=0`, `skipped=0`, and suite time `3.084 s`.

`coverage.xml` was parsed at the class/line and branch-condition level:

| New production module | Covered / executable lines | Line rate | Covered / total branches | Branch rate | 80% line gate |
| --- | ---: | ---: | ---: | ---: | --- |
| `discrete_holonomy.py` | 346 / 395 | 87.59% | 121 / 164 | 73.78% | PASS |
| `holonomy_experiment.py` | 188 / 193 | 97.41% | 39 / 44 | 88.64% | PASS |

The frozen gate is a line-coverage gate, so both modules clear it. The XML and its Coverage.py data file are ignored under `.verification/gauge-holonomy/`.

## Finalized launcher bundle and deterministic replay

The fresh harness's clean, finalized default bundle is:

```text
.verification/gauge-holonomy/runs/20260810T031446.506135Z/launcher-cwd/artifacts/gauge_holonomy/
10fbd1855196e092ecc5f36caa8af8d6ac1ce37b513c92c03f802de18535c317-20260809
```

Its manifest has `complete=true`, exactly nine complete files, `git_commit=4e15677e52004420156b3fde009aec643b4f3c9d`, `git_dirty=false`, CPU/float64 provenance, the four named RNG streams, and the project-module path in this worktree. The scientific implementation remains revision `2016042a0f10b13e9fbfc44b8f0741b4ed09eb95`; the newer manifest revision includes this first results-record commit only. The frozen application identity is `30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd`; the physical fixture SHA-256 is `a207eba1e9f3a36e80d809940405dce178f20c52dffc2482bbc24f4fc26df567`.

The harness's recorded replay method is `load source config.json; replace output.root only; run_holonomy_experiment`, with the replay call made from the worktree and output root `.verification/gauge-holonomy/runs/20260810T031446.506135Z/replay-root`. The resulting replay configuration hash is `dc1b6bde07ffee904e1e0c8f2fc7e8e1f9f0fa1c7484e1c5130a39a8c9e7f776`, differing only because output root is part of the resolved configuration. The JSON mechanically records `semantic_file_count=7`, `all_semantic_files_byte_identical=true`, `array_count=53`, `array_names_identical=true`, and `all_arrays_identical=true`.

| Semantic artifact | SHA-256 in source run | Second-root comparison |
| --- | --- | --- |
| `metrics.json` | `cc00c8517859af11a6abe86f6d733f79247d351d71a4f4cfa8b89a3329072f0c` | identical |
| `interaction_complex.json` | `54aa59a352ec68db5add77f55dc4eaa192ecb2f7a8fbe468e895c10be6c4ea3f` | identical |
| `oriented_links.npz` | `3d582d4fd098e6fe99d78f63d8c26474d2ed54caa4cb486b3f741e50a8aa9e7e` | identical |
| `vertex_frames.npz` | `7e113c428e506e4b4952174aff839e10648269a1f2f5d7a9133c02e2b0c3c06d` | identical |
| `cycle_holonomies.npz` | `a4d1dd0668c8a4fb919e02f58a6332f0a3719a9b130c42cd0d7f46c0a68d952c` | identical |
| `operational_record_laws.npz` | `031ccde4eb4ab0009b7bed2267d8ec6e2022b0f3f34a52830d797efa1a70522b` | identical |
| `aggregation_stages.npz` | `e27791c29194f63496d62250e0b833f75fa24b3dc16be5cfee528f5503097961` | identical |

## Metrics, literal oracles, and negative controls

The default nonflat run contains every frozen metric and all have `status=pass`:

| Metric | Observed value | Saved theorem / verification / origin fields |
| --- | ---: | --- |
| `passive_covariance_residual` | 0.0 | `ESTABLISHED` / `CANDIDATE` / `STANDARD` |
| `cycle_conjugacy_invariant_residual` | 0.0 | `ESTABLISHED` / `CANDIDATE` / `STANDARD` |
| `trivialization_residual` | 0.0 | `ESTABLISHED` / `CANDIDATE` / `PROJECT_NOVEL` |
| `operational_observable_residual` | 0.0 | `ESTABLISHED` / `CANDIDATE` / `PROJECT_NOVEL` |
| `broken_link_negative_control` | 0.07177704884455105 | `NUMERICAL` / `CANDIDATE` / `APPLICATION_SPECIFIC` |

The focused suite re-exercised the complete frozen scenario set. Its literal checks include: nonflat ordered cycle holonomy `[[2,2],[0,1]]`; coherently represented cycle `[[2,1],[0,1]]`; a nonflat tree-trivialization residual of `1.0`; operational logits `[0,2]` and probabilities `[0.11920292202211755, 0.8807970779778823]`; frustrated-path logits `[0,0]` versus `[0,2]` and signal gap `0.3807970779778823`; and staged direct and block totals `[[4,2]]`.

The pinned mutation restores exactly the original declared inverse pair `e01/e10` after an otherwise coherent passive transformation. The saved mutation record names only `e01` and `e10`; their inverse constraint remains valid, while the normalized operational observable changes by the positive gap above. Other passing negative controls reject omitted inverse links, forged/open-path cycle invariants, requested plaquette curvature on a tree, use of raw weights instead of a normalized operational law, and invalid fixture/scenario/group inputs before RNG, provenance, or run-store creation.

Figures are intentionally not exposed by this laboratory. Renderer-failure isolation is therefore not applicable. The focused fail-fast test `test_runner_rejects_invalid_data_before_rng_provenance_or_run_store` requests `render_figures=True` and verifies rejection before fixture loading, RNG construction, provenance collection, or run-directory creation.

## Claim, evidence, and falsifier ledger for this result record

The `CANDIDATE` values below are the serialized metric fields. They are deliberately not promoted by these numerical checks; the parent-owned shared verification ledger is the only place for final closure adjudication.

| Claim | theorem_status | verification_state | claim_origin | Current evidence | Falsifier / open obligation |
| --- | --- | --- | --- | --- | --- |
| The declared finite link implementation composes the pinned nonflat cycle and preserves its conjugacy invariants under the coherent passive frame convention. | `ESTABLISHED` | `CANDIDATE` | `STANDARD` | 36-test JUnit; literal cycle matrices; zero residuals; two-root replay. | A literal composition or passive-frame test mismatch; a derivation would still be needed for theorem closure. |
| The finite graph meets the implementation's declared flat/nonflat spanning-tree criterion. | `ESTABLISHED` | `CANDIDATE` | `PROJECT_NOVEL` | Literal residual `1.0` for the nonflat controls and zero metric residual. | A cycle/chord calculation or saved residual that disagrees; general mathematical scope remains conditional. |
| A normalized marked-event law has the documented coherent-frame observable invariance, and the declared broken pair produces an observable mismatch. | `ESTABLISHED` | `CANDIDATE` | `PROJECT_NOVEL` | Saved logits/probabilities, zero coherent residual, and pinned `0.07177704884455105` mutation gap. | Failure of law normalization, coherent equality, or the specified single-pair mutation check. |
| The default run is a reproducible finite computational artifact. | `NUMERICAL` | `CANDIDATE` | `APPLICATION_SPECIFIC` | Complete nine-file manifest, source/fixture identities, exact semantic hashes, and second-root equality of seven semantic files and 53 arrays. | Any source-hash, semantic-file, or array mismatch after replay at the same code/configuration. |
| The graph-link run establishes base-connection holonomy, dynamical gauge symmetry, a continuum limit, universality, or physical time. | `OPEN` | `INCONCLUSIVE` | `PROJECT_NOVEL` | Explicit scope fields all deny these in the saved interaction record. | Requires an explicit curve/connection bridge and the separately stated theory/application premises; this laboratory cannot supply them. |

## Remaining concerns

- This CPU result does not make any CUDA availability, parity, or performance claim.
- Direct Coverage.py produced the required branch-measurement XML.
- The launcher was run with no arguments. A temporary process-local Git safe-directory setting was needed in this sandbox to let the manifest bind the worktree revision; it did not alter repository configuration.
- The serialized metric verification states intentionally remain `CANDIDATE`; no mathematical proof or shared-ledger closure is claimed here.

## Explicit unresolved-assumption inventory

| Unresolved assumption or bridge | theorem_status | verification_state | Why this laboratory is insufficient |
| --- | --- | --- | --- |
| Graph-to-base curve/transport bridge | `OPEN` | `INCONCLUSIVE` | The artifacts declare finite graph links only; no base curve, principal connection, or identification of graph transport with base parallel transport is supplied. |
| Dynamical-symmetry premise | `OPEN` | `INCONCLUSIVE` | The checked passive coordinate covariance transforms links, states, and covectors coherently; no action, dynamics, or equivariant evolution law is declared or tested. |
| Continuum and universality premises | `OPEN` | `INCONCLUSIVE` | The run is one finite four-vertex construction with no scaling family, limiting measure, or universality argument. |
| Physical-time bridge | `OPEN` | `INCONCLUSIVE` | The finite calculations have no identified physical-time parameter or validated connection between computation, inference duration, and physical time. |
| Application-specific operational-law assumptions | `OPEN` | `INCONCLUSIVE` | States, marked-event covectors, observation vertex, and paths are declared numerical inputs. Their empirical or application-level interpretation and any external calibration are not established by the normalized-law calculation. |
