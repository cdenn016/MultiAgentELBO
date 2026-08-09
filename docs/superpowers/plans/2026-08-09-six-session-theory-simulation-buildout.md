# Six-Session Gauge-VFE/RG Theory and Simulation Buildout

**Date:** 2026-08-09

**Repository:** `C:\Users\chris and christine\Desktop\MultiAgentELBO`

**Planning baseline:** `origin/main` at `e6ebdc3d6c2fb361c428ec8ac651d12a33c5d18e`

**Execution model:** six isolated worktrees and branches, followed by one serial integration pass

**User interface rule:** click-to-run Python launchers with editable configuration dictionaries; no CLI

**Theory source:** the frozen repository `Theory/` snapshot plus the Research-vault gauge-VFE/RG wiki and terminal-closure record

## 1. Objective

Build a research platform that can do two different jobs without conflating them:

1. verify implementations of the admitted finite gauge-VFE/RG identities with exact, symbolic, metamorphic, and mechanical evidence; and
2. run explicit multi-agent simulations that measure application-specific defects, failure modes, and conjectural behavior.

The next scientific target is an explicit two-scale finite application tuple and its measurable defects. It is **not** a universality claim. The finite conditional theory already establishes many identities under stated assumptions, but an application must still supply and check its scale channels, product references, recognition lifts, configuration maps, comparison isomorphisms, regularity, and any claimed semiconjugacy.

## 2. Nonnegotiable boundaries

- Do not modify `Theory/**`. It is a frozen comparison source.
- Do not treat numerical agreement as proof.
- Do not promote a finite positive trend to universality, a continuum limit, or a fixed-point theorem.
- Do not identify graph-link holonomy with base-connection holonomy without an explicit construction.
- Do not treat the Gaussian realization as the universal probability-law interface.
- Do not call an assumption-violating counterexample a theorem refutation.
- Do not add a command-line interface. Each laboratory has a `run_*.py` launcher containing editable dictionaries.
- Do not silently fall back from CUDA to CPU.
- Do not let CUDA results replace exact CPU oracles.
- Do not stash, reset, clean, overwrite, or absorb another session's work.
- Do not stage, commit, or merge `.verification/**`; runtime verification may generate ignored lane-local state there.

## 3. Claim typing and verification contract

Theory status and verification state are orthogonal. Every claim and metric must carry both fields; neither may be substituted for the other.

| `theorem_status` | Meaning in this program |
|---|---|
| `ESTABLISHED` | A conditional analytic identity from the frozen theory. Tests verify the implementation, not the mathematics. |
| `HYPOTHESIS` | An application-specific structure or premise that must be explicitly supplied and checked. |
| `CONJECTURE` | A mathematical claim not yet proved, principally the scoped scalarized Gaussian fixed-ray attraction claim. |
| `NUMERICAL` | A statement deliberately limited to finite computational evidence. |
| `OPEN` | A theoretical obligation not resolved by the present finite platform. |

| `verification_state` | Meaning in this program |
|---|---|
| `CANDIDATE` | Queued but not yet assessed. |
| `LLM_SUPPORTED` | Reasoned model assessment without eligible closure evidence. |
| `EVIDENCE_VERIFIED` | Closed by current, revision-bound, domain-eligible supporting evidence. |
| `REFUTED` | Closed by current, revision-bound, domain-eligible contradicting evidence. |
| `INCONCLUSIVE` | Terminal for this attempt with at least one named open obligation. |

Every claim also records `claim_origin` as `STANDARD`, `PROJECT_NOVEL`, or `APPLICATION_SPECIFIC`. An established project construction must not be presented as canonical RG, gauge theory, or FEP merely because its derivation is internally complete.

The following remain `OPEN` unless a separate proof program closes them: continuum or nondominated law theory, infinite-volume and two-index limits, universality, nonlinear attraction, general Oseledets structure, invariant retained spaces, continuous beta, Bayesian-RG equivalence, canonical pullback geometry, operational base holonomy, graph-to-base identification, intrinsic scale selection, and physical time or law.

## 4. Execution topology

### 4.1 Wave 0: serial contract freeze

Session 1 is the only writer during the contract freeze. Sessions 2-6 may inspect sources and prepare notes, but they must not begin repository edits until the freeze commit is published.

Session 1 creates one contract commit defining:

- experiment discriminators for the new laboratories;
- common configuration types and validation;
- the CPU/CUDA compute configuration contract;
- artifact and metric inventories;
- common theorem-status vocabulary;
- launcher naming;
- immutable shared interfaces.

Wave 0 also freezes a machine-readable, versioned application fixture at `tests/fixtures/two_scale_application_v1.json`. It encodes rational literals as strings, has a recorded SHA-256 application ID, and declares the exact fine/coarse state labels, four-agent interaction complex, one normalized fine-to-coarse channel, fine/coarse references, recognition family, configuration map, and comparison typing. Sessions 1, 2, 4, 5, and 6 consume this same fixture ID; they may derive lane-specific views but may not silently replace it with unrelated examples.

The shared fixture contains one fine-to-coarse arrow. Three-level channel composition is a separate Session-6 extension and is not part of the two-scale application claim.

Record the resulting commit as `<CONTRACT_FREEZE_SHA>`. All six implementation branches start from that exact commit.

### 4.2 Parallel waves

```text
                         Wave 0: contract freeze
                                  |
                all branches start at one exact SHA
                                  |
       +-----------+-----------+--+--------+-----------+-----------+
       |           |           |           |           |           |
   Session 1   Session 2   Session 3   Session 4   Session 5   Session 6
   application exact proof  enumerator  information gauge and   scale/RG
   and network  and oracles and stress  histories    holonomy    plus CUDA
       |           |           |           |           |           |
       +-----------+-----------+-----------+-----------+-----------+
                                  |
                    serial integration and rebind
                                  |
                   adversarial review and final gate
```

### 4.3 Integration rule

Parallel sessions never edit shared registries. After all lane commits are ready, Session 1 becomes the sole integration writer. Sessions 2-6 switch to read-only review, reproduction, and counterexample roles while integration is in progress.

## 5. Shared contract and collision controls

### 5.1 Wave-0 exclusive ownership

Only Session 1 may edit these paths during contract freeze:

- `src/multiagent_elbo/config.py`
- `tests/test_config.py`
- `src/multiagent_elbo/experiment_support.py`
- `tests/test_experiment_support.py`
- `tests/fixtures/two_scale_application_v1.json`
- `environments/cuda-rtx5090-cu128.lock.txt`
- `pyproject.toml`, only for the approved development-coverage dependency and no CUDA/Torch runtime dependency
- `docs/superpowers/specs/2026-08-09-six-session-laboratory-contract.md`

The contract should reserve these experiment names:

- `multiagent_network`
- `theory_oracle`
- `finite_counterexample`
- `information_history`
- `gauge_holonomy`
- `scale_cocycle`
- `gaussian_fixed_ray`

The compute contract should be dictionary-driven and include at least:

```python
COMPUTE = {
    "backend": "cpu",          # "cpu" or "cuda"
    "dtype": "float64",       # explicit; never inferred silently
    "device_index": 0,
    "batch_size": 4096,
    "deterministic": True,
    "allow_tf32": False,
    "cpu_cuda_parity": True,
    "cuda_worker_python": r"C:\anaconda\python.exe",
    "heavy_sweep_enabled": False,
}
```

Wave 0 adds a backward-compatible optional fifth argument, `COMPUTE=None`, to `ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT, COMPUTE=None)`. Legacy four-dictionary calls remain CPU/float64 and byte-compatible. Wave 0 defines and smoke-tests all seven new laboratory schemas before freezing them.

The project remains Python 3.14+. The CUDA environment uses Python 3.12.7 and must not import the project package as if it were installed under a supported interpreter. Instead, freeze a versioned internal worker protocol: the Python 3.14 controller serializes validated JSON plus NPZ inputs, launches a standalone Python 3.12 CUDA worker, and validates its JSON/NPZ outputs. This is an internal implementation protocol behind a click-to-run launcher, not a user-facing CLI.

Wave 0 records the CUDA environment under `environments/cuda-rtx5090-cu128.lock.txt` and hashes that file in every CUDA run. It does not touch the user's untracked `uv.lock`. Invalid or unavailable CUDA must fail before RNG use or artifact creation. Exact-rational paths always use CPU regardless of the requested backend.

### 5.2 Frozen shared paths during parallel implementation

No lane may edit these paths:

- `src/multiagent_elbo/config.py`
- `src/multiagent_elbo/artifacts.py`
- `src/multiagent_elbo/runtime.py`
- `src/multiagent_elbo/experiment_support.py`
- `src/multiagent_elbo/rendering.py`
- `src/multiagent_elbo/figures.py`
- any package `__init__.py`
- `tests/test_config.py`
- `tests/test_launchers.py`
- `tests/test_figures.py`
- `README.md`
- `docs/hypotheses.md`
- `docs/verification/independent-reviews.md`
- `pyproject.toml`
- `.gitignore`
- `uv.lock`
- `Theory/**`
- existing `run_*.py` launchers
- `.verification/**` as a tracked deliverable; lane-local verification tools may generate ignored state there, but it is never staged or merged

If a lane needs a shared-interface change, it stops and writes a change request. It does not make the edit itself. Nonblocking requests are deferred to serial integration. If a change is genuinely blocking, all lanes halt; Session 1 publishes and reviews a new contract-freeze SHA; every affected lane is recreated or explicitly rebased onto that SHA; and all affected evidence is rerun before parallel work resumes. No lane may continue against a superseded contract.

### 5.3 Shared interfaces to preserve

- Backward-compatible `ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT, COMPUTE=None)` and canonical hashing.
- `RunStore.create`, typed writes, finalization, and failure records.
- Named RNG streams and recorded source/theory provenance.
- `MetricRecord` separation between implementation status and theorem status.
- Saved-artifact-only figure rendering and manifest validation.
- Fail-fast validation before RNG use or filesystem publication.

## 6. Six-session ownership board

| Session | Branch | Exclusive production paths | Primary laboratory |
|---|---|---|---|
| 1 | `codex/multiagent-application-20260809` | `src/multiagent_elbo/finite/agent_network.py`, `src/multiagent_elbo/finite/agent_network_experiment.py` | `run_multiagent_network_lab.py` |
| 2 | `codex/exact-theory-oracles-20260809` | `src/multiagent_elbo/finite/theory_oracles.py`, `src/multiagent_elbo/finite/theory_oracle_experiment.py` | `run_theory_oracle_lab.py` |
| 3 | `codex/finite-counterexamples-20260809` | `src/multiagent_elbo/finite/counterexamples.py`, `src/multiagent_elbo/finite/counterexample_experiment.py` | `run_finite_counterexample_lab.py` |
| 4 | `codex/information-histories-20260809` | `src/multiagent_elbo/finite/information_history.py`, `src/multiagent_elbo/finite/information_history_experiment.py` | `run_information_history_lab.py` |
| 5 | `codex/gauge-holonomy-agents-20260809` | `src/multiagent_elbo/geometry/discrete_holonomy.py`, `src/multiagent_elbo/geometry/holonomy_experiment.py` | `run_gauge_holonomy_lab.py` |
| 6 | `codex/scale-rg-cuda-20260809` | `src/multiagent_elbo/finite/scale_cocycle.py`, `src/multiagent_elbo/finite/scale_cocycle_experiment.py`, `src/multiagent_elbo/realizations/gaussian/fixed_ray.py`, `src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py`, `src/multiagent_elbo/cuda_backend.py`, `tools/cuda_worker.py` | `run_scale_cocycle_lab.py`, then `run_gaussian_fixed_ray_lab.py` |

Imports in lane tests must address the module directly; package exports are deferred to integration.

### 6.1 Exact lane allowlists

Lane commits are rejected if `git diff --name-only <CONTRACT_FREEZE_SHA>...HEAD` contains any path outside the lane's allowlist.

- **Session 1:** its two production files above; `run_multiagent_network_lab.py`; `tests/test_agent_network.py`; `tests/test_agent_network_experiment.py`; `docs/results/2026-08-09-multiagent-network-results.md`; `docs/verification/reviews/2026-08-09-multiagent-network-review.md`.
- **Session 2:** its two production files above; `run_theory_oracle_lab.py`; `tests/test_theory_oracles.py`; `tests/test_theory_oracle_experiment.py`; `docs/results/2026-08-09-theory-oracle-results.md`; `docs/verification/reviews/2026-08-09-theory-oracle-review.md`.
- **Session 3:** its two production files above; `run_finite_counterexample_lab.py`; `tests/test_counterexamples.py`; `tests/test_counterexample_experiment.py`; `docs/results/2026-08-09-finite-counterexample-results.md`; `docs/verification/reviews/2026-08-09-finite-counterexample-review.md`.
- **Session 4:** its two production files above; `run_information_history_lab.py`; `tests/test_information_history.py`; `tests/test_information_history_experiment.py`; `docs/results/2026-08-09-information-history-results.md`; `docs/verification/reviews/2026-08-09-information-history-review.md`.
- **Session 5:** its two production files above; `run_gauge_holonomy_lab.py`; `tests/test_discrete_holonomy.py`; `tests/test_holonomy_experiment.py`; `docs/results/2026-08-09-gauge-holonomy-results.md`; `docs/verification/reviews/2026-08-09-gauge-holonomy-review.md`.
- **Session 6:** all six production/worker files above; `run_scale_cocycle_lab.py`; `run_gaussian_fixed_ray_lab.py`; `tests/test_scale_cocycle.py`; `tests/test_scale_cocycle_experiment.py`; `tests/test_gaussian_fixed_ray.py`; `tests/test_gaussian_fixed_ray_experiment.py`; `tests/test_cuda_backend.py`; `docs/experiments/2026-08-09-gaussian-fixed-ray-preregistration.md`; `docs/results/2026-08-09-scale-cocycle-results.md`; `docs/results/2026-08-09-gaussian-fixed-ray-results.md`; `docs/verification/reviews/2026-08-09-scale-rg-cuda-review.md`.

## 7. Session 1: explicit application tuple and multi-agent network

### 7.1 Scientific duty

Construct one fully explicit two-scale finite application tuple rather than assuming that the abstract theorem applies automatically.

The first fixture should use a small exact state space, for example four binary agents with a declared hypergraph and a partition such as `{0,1}|{2,3}`. It must explicitly supply:

- finite agent and hyperedge sets;
- correlated baseline law;
- normalized interaction-record kernels;
- observation/evidence submeasure;
- recognition and posterior laws;
- fine-to-coarse Markov channel;
- fine and coarse reference laws;
- a declared product or block-product reference equivalent to the target law for Hoeffding coordinates;
- recognition lift or right inverse, where claimed;
- configuration coordinates and coarse map;
- comparison isomorphisms;
- declared local blocks and their axes.

The local-to-collective fixture must validate exact equality of the outside marginal before and after the block update, absolute continuity of both recognition laws with respect to the relevant posterior, and finite KL on both sides. If approximate outside marginals are studied, the full outside-marginal KL term must be retained rather than silently dropped.

### 7.2 Implementation deliverables

- Exact enumeration of the fine joint law and coarse pushforward.
- Global VFE and posterior-KL gap.
- Local-to-collective finite-difference identity.
- Evidence preservation under latent-only coarsening.
- Complete Hoeffding interaction reconstruction.
- One-arrow fine-to-coarse action for the shared two-scale fixture; two-step composition belongs to Session 6's three-level extension.
- Scenario families with editable dictionaries, initially:
  - aligned/consensus interactions;
  - frustrated interactions;
  - asymmetric evidence quality;
  - one higher-order hyperedge.
- Artifact arrays containing laws, channels, interactions, local changes, and scale maps.

### 7.3 Required negative controls

- A non-normalized channel rejected before artifact creation.
- A recognition lift that fails the right-inverse check.
- An overlapping-local-objective sum that disagrees with the correct collective difference.
- Pairwise-only reconstruction of a fixture with a nonzero higher-order interaction.
- A parameter-dependent channel labeled outside the fixed-channel theorem.

### 7.4 Stop conditions

- Missing application premises leave the applicability claim's `verification_state=INCONCLUSIVE`; they do not change its `theorem_status` or refute the conditional theorem.
- No neural agents or learned channel are added in this lane.
- No physical interpretation of scale or time is claimed.

## 8. Session 2: analytic validation, exact oracles, and formalization

### 8.1 Scientific duty

Provide independent mathematical evidence rather than recomputing production outputs through the same implementation path.

### 8.2 Implementation deliverables

- Standard-library `fractions.Fraction` oracles for the smallest fixtures.
- Independent symbolic derivations for:
  - evidence and ELBO decomposition;
  - conditional-score and Fisher-defect identity;
  - marked-event direct/staged pushforward;
  - Hoeffding reconstruction and retained residual;
  - Gaussian congruence, Galerkin restriction, and Schur complement;
  - the explicit two-scale Jacobian and commuting diagrams frozen as literals in `two_scale_application_v1.json`.
- A click-to-run oracle laboratory that records exact numerators/denominators separately from floating-point comparisons.
- A theorem-assumption matrix connecting every checked identity to its load-bearing premises.
- Optional Lean scaffold, only after finite statements and conventions are frozen:
  - kernel composition and evidence preservation;
  - finite conditional expectation/Fisher identity;
  - marked-event associativity;
  - Hoeffding reconstruction.

### 8.3 Required anti-tautology controls

- Literal fixtures must not be generated by the production function under test.
- The oracle must use a separate representation and code path.
- Mutation probes must demonstrate that reversed channel orientation, omitted source mass, or wrong conditional weights fail.
- A kernel-checked proof closes only the encoded finite theorem and assumptions.

### 8.4 Stop conditions

- Do not add SymPy or Lean dependencies without an approved shared-contract change.
- Numerical equality alone cannot change a mathematical claim to `EVIDENCE_VERIFIED`.
- Any theorem/application mismatch is reported precisely with `verification_state=INCONCLUSIVE` until resolved.
- Generic oracle infrastructure is completed on the lane branch. Any derivation that depends on another lane's production implementation is performed read-only after integration; the oracle lane must not infer a moving statement from sibling code.

## 9. Session 3: exhaustive enumeration, metamorphics, and counterexamples

### 9.1 Scientific duty

Search the smallest finite domains exhaustively for implementation defects, minimal counterexamples, and assumption-boundary witnesses.

### 9.2 Implementation deliverables

- Bounded enumeration over rational probability laws and normalized channels.
- Small set partitions and channel compositions.
- Boolean and low-cardinality interaction actions.
- State relabelings and compatible channel conjugations.
- Retained-space invariance searches.
- Deep-composition and tolerance-scaling stress matrices.
- Extended-real VFE cases with structured support-violation provenance.
- Minimal witness minimization and deterministic serialization.

Every candidate must record:

```text
claim_id
inside_declared_domain
assumptions_satisfied
smallest_witness
exact_or_numeric
observed_residual
classification
```

### 9.3 Required negative controls

- `q>0, p=0` produces an extended-real result and never evaluates `inf - inf` as a numeric residual.
- A parameter-dependent channel breaks the fixed-channel score theorem in a pinned fixture.
- Relabeling only one law changes KL by a pinned nonzero amount.
- Coarsening conditional attention weights without source masses disagrees generically with joint marked-event pushforward.
- Pairwise retained spaces fail on a higher-order fixture.
- Near-singular SPD inputs are either rejected or handled under an explicitly different model.

### 9.4 Stop conditions

- A witness outside theorem premises is an assumption-boundary example, not a refutation.
- Enumeration bounds are configuration data and must be saved.
- Large brute-force jobs may not move to CUDA until the Session-6 backend passes CPU/CUDA parity.

## 10. Session 4: information histories and semiconjugacy defect

### 10.1 Scientific duty

Build regular finite histories where the score, Fisher tensor, VFE gradient, natural-gradient field, and coarse comparison map are all explicitly defined.

### 10.2 Implementation deliverables

- A genuinely parameterized finite categorical family with an open parameter neighborhood.
- Analytic and finite-difference scores.
- Fine and coarse Fisher matrices with rank and conditioning diagnostics.
- VFE gradients and the matching Fisher-Rao metric of the same declared family and chart.
- Natural-gradient vector field on the identifiable tangent quotient, with range compatibility and an explicit quotient or pseudoinverse rule for singular directions. If another positive metric is explored, label the result a generic Riemannian gradient rather than a natural gradient.
- Fisher arc length computed from that same Fisher metric along a saved history.
- Separate inference-orbit parameter, RG depth, information duration, and any displayed wall-clock time.
- Exact vector-field semiconjugacy defect:

  ```text
  D_semiconj = dC_theta(v_fine) - v_coarse(C(theta))
  ```

- Directional as well as full-matrix equality diagnostics.

### 10.3 Required negative controls

- Parameter-dependent channel counterexample.
- Rank-deficient Fisher example with no hidden inverse.
- A coarse map that does not intertwine the vector fields.
- Same endpoints with different Fisher arc lengths.
- A chart reparameterization showing that raw coordinate speed is not information duration.

### 10.4 Stop conditions

- Score/Fisher identities require a fixed parameter-independent channel.
- Full recovery, directional recovery, and equality at one parameter must not be conflated.
- Finite-difference agreement does not establish DQM for an arbitrary family; smoothness comes from the declared family.

## 11. Session 5: nonflat gauge links, holonomy, and agent scenarios

### 11.1 Scientific duty

Add a declared finite interaction complex with nontrivial cycles, oriented group-valued links, vertex frame changes, and an operational record statistic.

### 11.2 Implementation deliverables

- Graph vertices, oriented edges, inverse-edge convention, and declared 2-cells/plaquettes.
- `GL+(K)` or an explicitly smaller group with validated frames.
- Link transformation `U_ij -> G_i U_ij G_j^-1`.
- Cycle holonomy and conjugacy-class invariants.
- Exact trivialization/cycle criterion for the chosen finite graph.
- Coupling of transported agent states to a normalized marked-event or observation law.
- Operational observables that can be compared before and after passive frame changes.
- Multi-agent scenarios:
  - flat tree control;
  - flat cyclic connection;
  - nonflat plaquette;
  - frustrated evidence transport;
  - staged agent aggregation.

### 11.3 Required negative controls

- Break a single transformed link while transforming all other objects correctly.
- Omit one inverse in a link action.
- Treat an open path as a gauge-invariant scalar.
- Use a tree and falsely request plaquette curvature.
- Report link holonomy without an operational law, which must remain insufficient for an operational-holonomy claim.

### 11.4 Stop conditions

- Graph-link results remain distinct from base-connection holonomy.
- Passive gauge covariance does not imply dynamical gauge symmetry.
- No bundle or connection is inferred merely from a matrix-valued fixture.

## 12. Session 6: scale cocycle, Gaussian fixed-ray attack, and RTX 5090 acceleration

### 12.1 Scientific duty

Implement exact finite scale composition and retained beta diagnostics first. Only then attack the scoped Gaussian fixed-ray conjecture with preregistered numerical experiments.

### 12.2 Scale-cocycle deliverables

- A sequence of normalized, recognition-independent Markov channels.
- Direct versus staged pushforward of every typed law.
- Conditional log-Laplace coarse action.
- Reverse/posterior bridge.
- Explicit comparison and rescaling isomorphisms.
- Nonautonomous derivative cocycle.
- Retained projection plus exact residual.
- Comparison-typed beta and transported beta residual.
- Full-subset interaction closure under coarse action.

### 12.3 Gaussian fixed-ray deliverables

- Pin the scalarized cone, matrix direction, primitive spatial map, Perron/factorization premise, basin, hierarchy, and blocking schemes.
- Commit `docs/experiments/2026-08-09-gaussian-fixed-ray-preregistration.md` before any confirmatory sweep. It freezes the quantified finite domain, exact job table, initial-condition population, paired blocking schemes, primary endpoint and scale window, practical effect threshold, success/counterevidence/inconclusive thresholds, precision or power target, multiplicity policy, exclusion rules, compute budget, holdout, and stopping rule.
- Run the preregistered sizes, seeds, initial conditions, partitions, and paired blocking schemes.
- Record:
  - projective ray angle;
  - normalized coupling distance;
  - off-family nonlinear remainder;
  - retained beta residual;
  - basin exits;
  - blocking-scheme dispersion;
  - conditioning and rejected-run counts.
- A positive trend is `NUMERICAL`. Floating-point counterevidence remains `NUMERICAL` with an `INCONCLUSIVE` mathematical verification state. `verification_state=REFUTED` requires an exact analytic/rational witness or rigorously interval-certified witness satisfying every preregistered premise of the scoped conjecture.

### 12.4 RTX 5090 backend contract

The CUDA backend is optional and isolated. It is used for batched floating-point sweeps, not exact proofs.

Required interpreter and preflight:

```powershell
C:\anaconda\python.exe -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

Planning-time preflight on 2026-08-09 confirmed Torch `2.10.0.dev20251210+cu128`, `cuda=True`, `NVIDIA GeForce RTX 5090`, and compute capability `(12, 0)`. Execution sessions must repeat the preflight because this environment evidence is time-dependent.

The Python 3.14 controller and standalone Python 3.12 worker must:

- require `torch.cuda.is_available()` and the requested device;
- exchange only the frozen versioned JSON/NPZ protocol and validate schema, shapes, dtypes, hashes, and job ID on both sides;
- record requested and effective backend/dtype per output array and metric;
- record Python executable path/hash, Python version, exact Torch build/environment digest, CUDA runtime, driver, cuDNN/cuBLAS versions, OS, device name, compute capability, actual precision controls, actual determinism controls, kernel/batch strategy, sweep-manifest hash, retry/resume lineage, and peak allocated/reserved memory;
- provide no import-time CUDA allocation;
- provide no silent CPU fallback;
- leave global default device, dtype, and RNG state unchanged in the controller;
- derive explicit Torch generator substreams from immutable job IDs and never draw scientific inputs independently on CPU and CUDA;
- set `CUBLAS_WORKSPACE_CONFIG` in the controller before worker process creation;
- call `torch.use_deterministic_algorithms(True, warn_only=False)` before the first CUDA operation and record the actual state;
- test batch-size and job-schedule invariance;
- compare every new kernel family through a three-lane matrix: Python 3.14 CPU, Python 3.12 worker CPU, and Python 3.12 worker CUDA;
- transfer identical CPU-generated literal inputs into both worker lanes;
- define dtype- and condition-scaled `atol`/`rtol` for every array, scalar metric, invariant, and status/rejection decision;
- include remainder batches, zero support, near-boundary SPD, high conditioning, and noncontiguous input shapes in parity tests;
- run a fixed sentinel subset from the production sweep through the full parity matrix;
- use `float64` for scientific correctness and confirmation; `float32` is screening or throughput-only;
- treat `bfloat16` as exploratory only and never use it for near-singular Fisher/SPD conclusions;
- recompute every primary endpoint, basin exit, rejection, threshold-near case, and worst-conditioned stratum in CUDA float64 and CPU float64;
- predeclare decision-stability rules for dtype changes and near-degenerate eigenspaces;
- check finiteness, symmetry, support, and normalization on-device and after transfer;
- serialize results through the existing `RunStore` contract;
- isolate optional Torch imports inside the CUDA module.

Torch is not a project runtime dependency: it belongs to the separately recorded worker environment frozen in Wave 0. Session 6 must not edit `pyproject.toml`. A newly discovered worker dependency is a blocking contract request and triggers the halt/re-freeze protocol. The durable environment record pins the actual Torch/CUDA build and all worker dependencies.

Scientific GPU jobs default to one heavy job at a time with fixed batch size. Before a heavy run, inspect GPU occupancy and active compute processes without killing them; require an idle-GPU check and explicit operator opt-in. OOM is a recorded failed job, never a trigger for silent batch adaptation. Jobs use immutable, resumable, idempotent IDs. Other sessions may continue CPU development and tests in parallel.

Correctness sweeps and performance benchmarks are separate artifacts. Performance runs require warmup, explicit synchronization, CUDA events or `torch.utils.benchmark`, repeated samples, peak memory, and recorded clock/thermal context; ordinary unsynchronized wall time is invalid for asynchronous CUDA work.

### 12.5 Confirmatory sweep protocol

Use the GPU for a preregistered confirmatory matrix, not an open-ended search that reports only favorable runs.

- Run a small pilot solely to estimate runtime, memory, numerical range, and failure modes.
- Freeze and hash the exact planned-job table before the confirmatory sweep. Record the sampling population and semantic meaning of each seed.
- Pair identical initial conditions across blocking schemes and baselines.
- Choose the number of independent initial conditions from a recorded confidence-interval-width or power target; use at least 30 per stochastic condition unless that calculation justifies another count.
- Reserve a confirmatory holdout that is not used for threshold or basin tuning.
- Retain per-seed outputs, not only averages.
- Report all planned, completed, rejected, retried, and missing jobs. Report medians, robust dispersion, paired/hierarchical uncertainty across independent initial conditions, bootstrap confidence intervals, multiplicity-adjusted secondary results, basin-exit rate, rejection rate, and missing/nonfinite counts.
- Separate exploratory from confirmatory conditions in both artifacts and prose.
- Repeat selected same-seed CUDA runs to measure nondeterminism; deterministic claims require byte or tolerance criteria fixed in advance.
- Compare float32 throughput results with float64 CPU and CUDA reference subsets.
- Do not stop early based on whether the conjecture appears supported.

### 12.6 Required negative controls

- Wrong channel-composition order.
- Retained projection that is not intertwined by the comparison map.
- Pairwise-only truncation after a coarse step that generates higher-order interactions.
- Noncommuting blocking schemes.
- CPU/CUDA parity mutation.
- Requested CUDA on the CPU interpreter or unavailable device must fail before artifacts.

## 13. Wave schedule

### Wave 0: contract and statement freeze

| Session | Work |
|---|---|
| 1 | Write and test shared schemas, statuses, compute contract, and experiment registry. Publish `<CONTRACT_FREEZE_SHA>`. |
| 2-6 | Read-only source mapping and literal-fixture preparation. No repository edits. |

### Wave 1: six parallel foundations

| Session | Work |
|---|---|
| 1 | Explicit application tuple and exact multi-agent enumerator. |
| 2 | Exact-rational oracle packet and theorem-assumption matrix. |
| 3 | Rational small-domain enumeration and boundary classification. |
| 4 | Categorical history, Fisher geometry, and arc-length primitives. |
| 5 | Interaction complex, oriented links, and holonomy metamorphics. |
| 6 | Exact scale composition, retained residual, and CPU reference kernels. |

### Wave 2: six parallel scientific tests

| Session | Work |
|---|---|
| 1 | Consensus, frustration, asymmetric-evidence, and higher-order multi-agent scenarios. |
| 2 | Independent derivations for the frozen application statement and generic identities; optional formal proofs. Producer-specific audits wait for Wave 3. |
| 3 | Frozen-fixture and lane-local metamorphics, stress matrix, and minimal counterexamples. Cross-producer checks wait for Wave 3. |
| 4 | Natural-gradient histories and semiconjugacy-defect experiments. |
| 5 | Nonflat plaquette and operational marked-event simulations. |
| 6 | Beta diagnostics, CUDA parity, then preregistered Gaussian fixed-ray sweeps. |

### Wave 3: serial integration with parallel read-only review

| Session | Work |
|---|---|
| 1 | Sole writer: merge lanes, update exports/launchers/figures/docs, resolve shared interfaces. |
| 2 | Mathematical derivation audit of merged producer code; attempt to falsify theorem/application alignment and hand integration-only test designs to Session 1. |
| 3 | Code, cross-laboratory metamorphic, artifact, and stress audit; hand integration-only test designs to Session 1. |
| 4 | Independently reproduce information-history outputs. |
| 5 | Independently reproduce gauge/holonomy outputs and check operational scope. |
| 6 | Independently reproduce CPU/CUDA parity and Gaussian sweep summaries. |

## 14. Per-lane definition of done

Every lane returns all of the following:

1. Branch name, base SHA, final commit SHA, and exact changed-path list.
2. Focused JUnit XML stored in ignored `.verification/<lane>/pytest.xml` or an explicit temporary path.
3. Parsed test counts from that XML, never from console memory.
4. Machine-readable coverage XML with at least 80% line coverage for new production modules and no unexplained regression in touched modules. Wave 0 must add or approve the development-only coverage tool.
5. One no-argument click-to-run launcher with editable dictionaries and no `argparse`.
6. A sanitized subprocess launcher test with no editable install or inherited `PYTHONPATH`.
7. Same-seed deterministic metrics and array-bundle checks across two output roots.
8. Validation-before-RNG and validation-before-artifact tests.
9. Renderer-failure isolation if figures are exposed.
10. At least one independently derived literal oracle.
11. At least one pinned negative control that fails under the intended mutation.
12. A lane-unique result document under `docs/results/`.
13. A lane-unique review under `docs/verification/reviews/`.
14. A claim/evidence table with `theorem_status`, `verification_state`, `claim_origin`, evidence type, and falsification condition.
15. A list of unresolved assumptions with the appropriate `OPEN` theorem status or `INCONCLUSIVE` verification state.
16. Exact commands, interpreter paths, environment records, runtime, and peak-memory records.
17. No edits outside the lane's owned paths, mechanically checked against its allowlist.

## 15. Experiment artifact contract

Every run bundle should contain:

- canonicalized configuration and hash;
- source revision and dirty-tree binding;
- theory snapshot digest;
- interpreter and dependency versions;
- RNG seed names and values;
- input hashes;
- metric records with `theorem_status`, `verification_state`, `claim_origin`, and effective backend/dtype;
- exact or floating-point provenance;
- arrays required to recompute every reported metric;
- failure manifest if publication or rendering fails;
- figure manifest for saved-artifact-only rendering;
- CPU/CUDA device and precision provenance when applicable.

Numerical publication must finalize before rendering. A renderer failure must not mutate or invalidate the numerical bundle.

## 16. Integration order

Create `codex/theory-simulation-integration-20260809` from `<CONTRACT_FREEZE_SHA>`, then integrate in this order:

1. Session 2 exact-oracle infrastructure.
2. Session 1 application tuple and multi-agent core.
3. Session 3 enumerator and counterexamples.
4. Session 4 information histories.
5. Session 5 gauge/holonomy.
6. Session 6 scale cocycle and CUDA backend.
7. Session 6 Gaussian fixed-ray attack, only if its prerequisites are satisfied.
8. Shared package exports and launcher registry.
9. Saved-artifact renderers and figure tests.
10. README, hypotheses registry, consolidated results, and independent reviews.

If any merge changes a mathematical convention, Session 2 must re-audit every dependent identity. If any merge changes configuration, dependency, device behavior, or artifact inputs, affected experiment evidence must be reproduced.

## 17. Final verification gate

The integration owner must complete these steps at the final integration SHA:

1. Run the complete CPU suite with `C:\Python314\python.exe` and emit JUnit XML.
2. Run machine-readable coverage and enforce the new-module threshold.
3. Run the Python 3.12 worker CPU lane and dedicated CUDA lane with `C:\anaconda\python.exe` after verifying CUDA availability, device identity, environment hash, and idle-GPU status.
4. Parse all JUnit and coverage files mechanically.
5. Reproduce every published laboratory bundle from saved configurations.
6. Re-render every figure from saved artifacts only.
7. Verify deterministic replay hashes where promised.
8. Run independent mathematical and code reviews.
9. Start a fresh ignored verification ledger at the final SHA.
10. Record one claim per check and close it only with domain-eligible evidence.
11. Validate the ledger.
12. Keep the live ledger and activation marker uncommitted.

Closure rules:

- Mathematics requires a derivation or formal proof.
- Code and experiment claims require current mechanical or reproduced evidence.
- Application hypotheses require explicit witness objects and checked premises.
- A conjecture can be refuted by an in-domain counterexample but not verified by finite positive runs.
- Missing eligible evidence or unresolved reviewer disagreement yields `verification_state=INCONCLUSIVE`; it does not alter `theorem_status`.

## 18. Dispatch prerequisites and Wave-0 prompt

This plan must be committed and reachable by every session before dispatch. Do not send the six implementation prompts while `<CONTRACT_FREEZE_SHA>` is still a placeholder or while the contract spec/fixture is absent.

First send only this Wave-0 prompt to Session 1:

```text
You are the sole Wave-0 contract owner for MultiAgentELBO.

Read the committed plan:
docs/superpowers/plans/2026-08-09-six-session-theory-simulation-buildout.md

Work in an isolated branch/worktree from the fetched origin/main named by the
plan. Preserve all live WIP. Implement only the Wave-0 paths in section 5.1:
the seven discriminated schemas, backward-compatible optional COMPUTE config,
orthogonal claim fields, the versioned two-scale literal fixture and digest,
the Python-3.14-controller/Python-3.12-worker protocol schema, the CUDA
environment record, coverage tooling, smoke configurations, and the shared
contract spec. Do not implement any scientific lane.

Run focused tests and independent contract review. Commit the freeze. Return:
1. CONTRACT_FREEZE_SHA;
2. exact changed paths;
3. parsed JUnit and coverage results;
4. fixture/application SHA-256;
5. CUDA environment-file SHA-256;
6. any unresolved contract decision.

Do not authorize Sessions 2-6 until the contract review is approved.
```

After Wave 0 passes, the coordinator substitutes the concrete SHA into six separate prompt copies, verifies that the contract spec and fixture are reachable from that SHA, and only then creates the six implementation worktrees.

## 19. Copy-ready common prompt

Paste this before the lane-specific prompt for every implementation session:

```text
You are one of six parallel sessions building MultiAgentELBO.

Repository: C:\Users\chris and christine\Desktop\MultiAgentELBO
Base exactly: <CONTRACT_FREEZE_SHA>
Create your named codex/* branch in a separate isolated worktree.

Read first:
- docs/superpowers/plans/2026-08-09-six-session-theory-simulation-buildout.md
- docs/superpowers/specs/2026-08-09-six-session-laboratory-contract.md
- Theory/SPEC.md
- docs/hypotheses.md
- the theory sources named by your lane

You are not alone in the repository. Edit only your explicitly owned paths.
Do not revert, stash, reset, clean, or absorb another session's changes.
Do not edit shared registries, package exports, figures, README, hypotheses,
Theory/**, pyproject.toml, uv.lock, or existing launchers. Verification tools may
write ignored lane-local .verification/** state, but never stage or merge it.

Use TDD. Every identity needs an independent literal oracle and a named negative
control. Every launcher is click-to-run with editable dictionaries and no CLI.
Validation must occur before RNG use or artifact creation. Preserve RunStore,
provenance, metric, and saved-artifact rendering contracts.

Record theorem_status, verification_state, and claim_origin separately.
Numerical agreement is not proof. If you need a shared-interface change, stop
and report it; never continue against a superseded contract SHA.

Return:
1. base and final commit SHA;
2. changed paths;
3. parsed focused JUnit counts and XML path;
4. launcher command, configuration, and artifact path;
5. exact oracle and negative-control results;
6. claim/evidence/falsifier table;
7. unresolved assumptions and integration requests.
```

## 20. Copy-ready lane prompts

### Session 1 prompt

```text
Lane: explicit application tuple and multi-agent network.
Branch: codex/multiagent-application-20260809.
Own only src/multiagent_elbo/finite/agent_network.py,
src/multiagent_elbo/finite/agent_network_experiment.py,
and every other exact Session-1 path in section 6.1. Own no wildcard or unlisted path.

First perform the Wave-0 contract-freeze assignment if no freeze SHA exists.
Then implement the explicit four-agent/two-scale finite tuple, exact joint and
coarse laws, recognition lift checks, local/global VFE differences, complete
interactions, the one-arrow coarse action, and the four declared scenarios. Pin every
application premise and the required negative controls. Do not claim physical
time, universality, or learned-agent behavior.
```

### Session 2 prompt

```text
Lane: analytic validation and exact oracles.
Branch: codex/exact-theory-oracles-20260809.
Own only src/multiagent_elbo/finite/theory_oracles.py,
src/multiagent_elbo/finite/theory_oracle_experiment.py,
and every other exact Session-2 path in section 6.1. Own no wildcard or unlisted path.

Build independent Fraction-based oracles and derivations for the existing and
new finite identities. Maintain a theorem-assumption matrix. Use mutation probes
to prove anti-tautology. Propose, but do not add, SymPy or Lean dependencies
without approval. No floating-point check may be labeled a mathematical proof.
```

### Session 3 prompt

```text
Lane: exhaustive finite enumeration, metamorphics, and counterexamples.
Branch: codex/finite-counterexamples-20260809.
Own only src/multiagent_elbo/finite/counterexamples.py,
src/multiagent_elbo/finite/counterexample_experiment.py,
and every other exact Session-3 path in section 6.1. Own no wildcard or unlisted path.

Enumerate bounded rational laws, channels, partitions, actions, and relabelings.
Minimize and serialize witnesses. Record whether every premise is satisfied.
Exercise extended-real, parameter-dependent-channel, wrong-gauge, beta-alone,
higher-order, deep-composition, and conditioning controls. Never call an
outside-domain witness a theorem refutation.
```

### Session 4 prompt

```text
Lane: information histories and semiconjugacy defect.
Branch: codex/information-histories-20260809.
Own only src/multiagent_elbo/finite/information_history.py,
src/multiagent_elbo/finite/information_history_experiment.py,
and every other exact Session-4 path in section 6.1. Own no wildcard or unlisted path.

Implement regular categorical histories, analytic/FD scores, fine/coarse Fisher,
VFE gradients, Fisher-Rao natural-gradient fields on the identifiable quotient,
Fisher arc length from that same metric, and the
exact vector-field semiconjugacy defect. Keep RG depth, inference parameter,
information duration, and wall time distinct. Include rank-deficient and
parameter-dependent-channel negative controls.
```

### Session 5 prompt

```text
Lane: discrete gauge links, holonomy, and agent scenarios.
Branch: codex/gauge-holonomy-agents-20260809.
Own only src/multiagent_elbo/geometry/discrete_holonomy.py,
src/multiagent_elbo/geometry/holonomy_experiment.py,
and every other exact Session-5 path in section 6.1. Own no wildcard or unlisted path.

Declare the interaction complex, oriented links, inverse convention, 2-cells,
vertex frames, cycle holonomy, and operational marked-event observable. Implement
flat and nonflat scenarios with exact gauge metamorphics and broken-link controls.
Do not identify graph holonomy with base-connection or operational holonomy
without the explicit bridge required by the plan.
```

### Session 6 prompt

```text
Lane: scale cocycle, Gaussian fixed-ray attack, and RTX 5090 acceleration.
Branch: codex/scale-rg-cuda-20260809.
Own only src/multiagent_elbo/finite/scale_cocycle.py,
src/multiagent_elbo/finite/scale_cocycle_experiment.py,
src/multiagent_elbo/realizations/gaussian/fixed_ray.py,
src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py,
src/multiagent_elbo/cuda_backend.py,
tools/cuda_worker.py,
and every other exact Session-6 path in section 6.1. Own no wildcard or unlisted path.

Implement exact CPU scale composition and retained beta residuals first. Add the
isolated CUDA backend only after small-case CPU parity is pinned. Use
C:\anaconda\python.exe for every CUDA claim and record device/dtype provenance.
Then preregister and run the scoped multi-seed/multi-scheme Gaussian fixed-ray
attack. Keep heavy_sweep_enabled=False through pilot, parity, preregistration,
idle-GPU review, and explicit operator opt-in. Positive finite trends remain
NUMERICAL and cannot verify universality; mathematical refutation requires an
exact or rigorously interval-certified in-domain witness.
```

## 21. Coordinator checklist

Before dispatch:

- [ ] Confirm this plan commit is reachable by every session.
- [ ] Fetch `origin` and record `origin/main`.
- [ ] Confirm live WIP paths and hashes; do not touch them.
- [ ] Create one isolated Wave-0 worktree.
- [ ] Complete and review the contract-freeze commit.
- [ ] Confirm the contract spec, application fixture, environment record, and coverage contract exist at the freeze commit.
- [ ] Replace `<CONTRACT_FREEZE_SHA>` with the concrete SHA in all six rendered prompts.
- [ ] Create six isolated branches/worktrees from that SHA.
- [ ] Give every session the common prompt and its lane prompt.

During parallel work:

- [ ] Enforce exclusive ownership.
- [ ] Defer nonblocking shared-interface requests to integration; halt and re-freeze all lanes for a blocking change.
- [ ] Keep lane evidence revision-bound and uncommitted under `.verification/`.
- [ ] Allow only Session 6 to own CUDA backend code and heavy GPU scheduling.
- [ ] Require separate `theorem_status`, `verification_state`, and `claim_origin` fields in progress reports.
- [ ] Stop any lane that drifts into continuum or universality claims.

Before integration:

- [ ] Require clean lane status and exact changed-path lists.
- [ ] Parse focused JUnit XML.
- [ ] Parse coverage XML and enforce the threshold.
- [ ] Reject any changed path outside the lane's exact allowlist.
- [ ] Confirm launcher and artifact reproduction.
- [ ] Confirm independent oracle and negative control.
- [ ] Review shared-interface requests before merging.

Before publication:

- [ ] Integrate serially in the specified order.
- [ ] Run full CPU and dedicated CUDA verification at the final SHA.
- [ ] Reproduce artifacts and figures.
- [ ] Complete mathematical and implementation reviews.
- [ ] Rebuild and validate the final ignored claim ledger.
- [ ] Fetch remote state again and compare incoming integration paths with every live-WIP path and hash, including semantic pairs such as an incoming `pyproject.toml` versus the user's untracked `uv.lock`.
- [ ] Rehearse integration in a disposable worktree and verify no overlap with `run_attention_lab.py`, `run_categorical_dqm_lab.py`, `docs/reviews/**`, `uv.lock`, or any newly discovered WIP.
- [ ] Stop for the user if an incoming path overlaps live WIP; never overwrite, stash, reset, or clean it.
- [ ] Fast-forward the `main` ref only after the final gate passes; update a dirty live checkout only after the separate overlap audit says it is safe.

## 22. Program exit criteria

This buildout is complete when:

- one explicit two-scale finite multi-agent tuple satisfies every declared application premise;
- exact and independent oracles cover every load-bearing finite identity used by the simulations;
- small-domain enumeration finds no in-domain implementation counterexample, or found defects are fixed and rebound;
- information histories report a well-typed semiconjugacy defect rather than assuming it vanishes;
- gauge scenarios distinguish passive covariance, graph holonomy, and operational claims;
- scale experiments report full, retained, and transported residuals;
- the Gaussian conjecture has a preregistered attack with honest finite conclusions;
- the RTX 5090 path has small-fixture CPU parity and complete provenance;
- all click-to-run launchers, artifacts, and figures reproduce at the final revision;
- the final revision has current mechanical evidence, independent mathematical review, and a validated ignored ledger;
- all remaining continuum, universality, canonical-geometry, and physical-time obligations remain explicitly `OPEN` unless separately proved.

## 23. Primary planning sources

- `Theory/SPEC.md`
- `Theory/appendix_claim_ledger.tex`
- `docs/hypotheses.md`
- `docs/superpowers/specs/2026-08-08-gauge-vfe-rg-simulation-platform-design.md`
- `docs/results/2026-08-09-foundation-results.md`
- `docs/results/2026-08-09-attention-categorical-dqm-results.md`
- `C:\Users\chris and christine\Desktop\Research\wiki\projects\Gauge-Theoretic Multi-Agent VFE Model.md`
- `C:\Users\chris and christine\Desktop\Research\wiki\themes\Gauge VFE ELBO curriculum.md`
- `C:\Users\chris and christine\Desktop\Research\sources\manuscripts\gauge-vfe-rg-terminal-theory-closure-2026-08-08.md`

The Research vault was consulted read-only. Any ingestion of this buildout plan into the wiki requires separate user approval.

## 24. Planning review record

Three independent read-only reviewers challenged the draft and approved the revised plan:

- theory reviewer: approved after separating theorem status from verification state, binding the common application fixture, adding missing local-global/Hoeffding premises, fixing the scale-count dependency, requiring the Fisher-Rao quotient, and tightening mathematical-refutation evidence;
- parallel-work reviewer: approved after adding the Wave-0-only dispatch gate, exact allowlists, producer-independent parallel tasks, blocking re-freeze protocol, coverage gate, and dirty-WIP fast-forward audit;
- GPU/numerical reviewer: approved after defining the Python 3.14 controller/Python 3.12 worker boundary, environment lock, enforced determinism, three-lane parity, scientific precision policy, preregistered paired sweep, and idle-GPU scheduling.

This is planning approval, not implementation or theorem closure. Wave 0 has not yet been executed, no new laboratory exists, and no mathematical claim is closed by these reviews.
