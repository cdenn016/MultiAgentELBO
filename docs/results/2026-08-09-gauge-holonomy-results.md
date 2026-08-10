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

Coverage check (the `pytest-cov` plugin is incompatible with this Python 3.14/NumPy environment, so the permitted direct Coverage.py route was used):

```powershell
$env:COVERAGE_FILE = "$PWD/.verification/gauge-holonomy/.coverage"
C:\Python314\python.exe -m coverage run --branch -m pytest `
  tests/test_discrete_holonomy.py tests/test_holonomy_experiment.py `
  --basetemp=.pytest-tmp/task3-coverage -q -p no:cacheprovider
C:\Python314\python.exe -m coverage xml `
  -o .verification/gauge-holonomy/coverage.xml `
  --include='src/multiagent_elbo/geometry/discrete_holonomy.py,src/multiagent_elbo/geometry/holonomy_experiment.py'
```

The no-argument reproduction command, run from an isolated output directory, was:

```powershell
C:\Python314\python.exe "<worktree>\run_gauge_holonomy_lab.py"
```

It completed in `0.372418 s`; the sampled primary-process peak working set was `41,922,560` bytes (`39.980469 MiB`). The focused test invocation completed in `3.406 s` wall-clock time. This memory number is an observed Windows working-set maximum, not a hardware-capacity assertion.

## Parsed mechanical evidence

`pytest-focused.xml` was parsed as XML, not transcribed from console output: `tests=36`, `failures=0`, `errors=0`, `skipped=0`, and suite time `3.084 s`.

`coverage.xml` was parsed at the class/line and branch-condition level:

| New production module | Covered / executable lines | Line rate | Covered / total branches | Branch rate | 80% line gate |
| --- | ---: | ---: | ---: | ---: | --- |
| `discrete_holonomy.py` | 346 / 395 | 87.59% | 121 / 164 | 73.78% | PASS |
| `holonomy_experiment.py` | 188 / 193 | 97.41% | 39 / 44 | 88.64% | PASS |

The frozen gate is a line-coverage gate, so both modules clear it. The XML and its Coverage.py data file are ignored under `.verification/gauge-holonomy/`.

## Finalized launcher bundle and deterministic replay

The clean, finalized default bundle is:

```text
.verification/gauge-holonomy/launcher-cwd-provenance/artifacts/gauge_holonomy/
10fbd1855196e092ecc5f36caa8af8d6ac1ce37b513c92c03f802de18535c317-20260809
```

Its manifest has `complete=true`, exactly nine complete files, `git_commit=2016042a0f10b13e9fbfc44b8f0741b4ed09eb95`, `git_dirty=false`, CPU/float64 provenance, the four named RNG streams, and the project-module path in this worktree. The frozen application identity is `30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd`; the physical fixture SHA-256 is `a207eba1e9f3a36e80d809940405dce178f20c52dffc2482bbc24f4fc26df567`.

The saved `config.json` was read, its output root alone was redirected to `.verification/gauge-holonomy/replay-root`, and the experiment was rerun. The resulting configuration hash changed to `f449dfe154f3c5c50f40f5e0a5344eddd6932ee12428f19a651b36680810e8b7` solely because its output root is part of the resolved configuration. The default run and second root had identical `metrics.json`, `interaction_complex.json`, and all five scientific NPZ bundles byte-for-byte; all `53` saved arrays had equal names, shapes, dtypes, and values.

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
- Direct Coverage.py was required because `pytest-cov` fails during Python 3.14/NumPy instrumentation with a duplicate module-load error. Coverage.py still produced the required branch-measurement XML.
- The launcher was run with no arguments. A temporary process-local Git safe-directory setting was needed in this sandbox to let the manifest bind the worktree revision; it did not alter repository configuration.
- The serialized metric verification states intentionally remain `CANDIDATE`; no mathematical proof or shared-ledger closure is claimed here.
