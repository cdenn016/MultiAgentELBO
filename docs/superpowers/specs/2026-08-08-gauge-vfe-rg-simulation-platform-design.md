# Gauge-VFE-RG Simulation Platform Design

**Status:** Approved by delegated judgment on 2026-08-08. The user asked for autonomous overnight work and authorized best judgment.

**Repository:** `C:\Users\chris and christine\Desktop\MultiAgentELBO`

**Theory source:** The user-provided `Theory/` snapshot, byte-matched before implementation to the live Research-vault `manuscripts/gauge_vfe_rg/` source files. The snapshot is evidence input and is not edited by this build.

## 1. Objective

Build a research codebase that makes the finite, conditional `gauge_vfe_rg` theory executable, inspectable, and falsifiable. The first milestone must instantiate exact probability identities on small finite systems, record explicit countercontrols, and produce reproducible artifacts. Gaussian graph and renormalization experiments are a realization layer, not the definition of the theory.

The user-facing workflow has no command-line interface. Every run begins from an editable Python configuration dictionary in a click-to-run file. Numerical APIs remain importable so tests, notebooks, and future sweep launchers do not depend on module globals.

## 2. Non-negotiable boundaries

- No `argparse`, Click, Typer, or CLI-first interface.
- A launcher contains editable dictionaries and a thin `main()` only; numerical logic lives in the package.
- The fixed normalized generative law never takes a recognition law or posterior as input.
- Local agent and block objectives are coordinate views of one joint VFE; they are not summed as independent global objectives.
- A coarse operation pushes the reference measure, evidence measure, recognition law, and posterior through the same declared normalized Markov channel.
- Full finite interaction closure and retained sparse/pairwise approximation are separate. Every retained approximation reports its exact residual in the theorem's coordinate `G` norm; weighted L2 is only a separately named diagnostic.
- Gauge transformations are passive coordinate changes. Invariants must be checked against transformed representations of the same object.
- Gaussian information-form, Schur, determinant, generalized-pencil, and matrix-weighted graph claims remain under `realizations/gaussian/`.
- Singular Gaussian rays are not silently repaired with pseudoinverses or pseudodeterminants.
- RG depth, inference-path parameter, Fisher duration, and physical time remain distinct.
- Numerical checks corroborate only their declared finite endpoint. They do not prove attraction, universality, a thermodynamic limit, or a physical law.
- All settings that affect semantics, numerics, diagnostics, or artifacts are represented in typed configuration dictionaries and saved in resolved form.

## 3. Approaches considered

### A. Exact finite categorical core first — selected

Enumerate small finite state spaces, implement normalized measures and Markov channels exactly in float64, and verify evidence, ELBO/VFE, conditional-KL, Fisher, interaction, and attention identities before adding continuous realizations. This aligns with the terminal vault record, which says the next scientific step is a small explicit finite instantiation. It offers literal or hand-derived test oracles and exposes theory-typing errors early.

### B. Gaussian graph simulator first — rejected as the foundation

This makes matrix and RG pictures immediately intuitive, but risks treating the multivariate-Gaussian interaction subfamily as the ambient theory. Gaussian support remains important, but only as a plug-in after the finite probability core.

### C. Port MAgent or V3 and adapt it — rejected

Their launcher, typed-config, artifact, and reproducibility seams are useful. Their objectives and runtime paths are separate comparison architectures, however, and importing them would contaminate the exact-joint and coarse-channel semantics.

## 4. Milestone decomposition

### Milestone 0 — repository and theory provenance

Track the supplied theory snapshot without altering it, ignore generated caches/build products, record its source path, Research Git state, and per-file digest, and make a concrete Git revision before invoking the verification control plane.

### Milestone 1 — exact finite laboratory

Deliver a click-to-run finite categorical experiment over three binary agents. It must verify normalized measure-pair pushforward, evidence preservation, the exact VFE chain-rule gap, a local-to-collective block update identity, the conditional-score/Fisher contraction identity for a declared centered score, and a full-interaction decomposition with explicit retained residual. The finite vector check does not by itself establish DQM.

### Milestone 2 — gauge and Gaussian realization

Deliver a second click-to-run experiment implementing vertexwise finite relabeling metamorphics and a separate Gaussian graph realization. It must verify congruence-covariant quadratic energies, generalized-spectrum invariance, aggregation closure/internal-edge cancellation, and declared negative controls.

### Milestone 3 — histories and nonautonomous scale studies

Add natural-gradient histories, Fisher arc length, attention marked-event-law coarsening, exact nonlinear scale cocycles, beta residuals after explicit comparison isomorphisms, and finite attacks on the fixed-ray conjecture. This milestone is not required for the first overnight slice.

## 5. Package architecture

```text
MultiAgentELBO/
  Theory/                              # supplied, read-only manuscript snapshot
  run_finite_lab.py                    # editable dictionaries; click to run
  run_gaussian_lab.py                  # editable dictionaries; click to run
  make_figures.py                      # replay saved metrics; no simulation coupling
  pyproject.toml
  README.md
  src/multiagent_elbo/
    __init__.py                        # narrow stable public API
    config.py                          # frozen typed configs and strict resolution
    runtime.py                         # named NumPy RNG streams and environment record
    artifacts.py                       # atomic run bundle and manifest
    finite/
      measures.py                      # finite measures, kernels, pushforwards
      vfe.py                           # posterior, VFE, conditional-KL identities
      fisher.py                        # scores, conditional expectation, defects
      interactions.py                  # finite product-reference Hoeffding/Mobius basis
      experiment.py                    # finite-lab orchestration and result type
    geometry/
      finite_gauge.py                  # finite relabeling/gauge metamorphics
    realizations/
      gaussian/
        interactions.py                # SPD self plus matrix-weighted Laplacian family
        gauge.py                       # block congruence and invariant pencils
        experiment.py                  # Gaussian-lab orchestration
    figures.py                         # pure renderers from saved result dictionaries
  tests/
    test_config.py
    test_measures.py
    test_vfe.py
    test_fisher.py
    test_interactions.py
    test_finite_experiment.py
    test_gaussian_realization.py
    test_artifacts.py
    test_launchers.py
  docs/
    theory-provenance.md
    hypotheses.md
    superpowers/specs/...
    superpowers/plans/...
```

Each numerical module owns one mathematical responsibility. Launcher files do not perform algebra, mutate resolved configuration, or construct hidden defaults.

## 6. Core interfaces and data flow

### 6.1 Configuration

`ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT)` rejects unknown keys, exact-type mistakes such as `bool` supplied for an integer, invalid probabilities, unreachable options, and unsupported combinations before seeding or filesystem writes. It returns frozen nested dataclasses. The canonical resolved JSON and SHA-256 hash are computed once and reused everywhere.

Named RNG streams are derived deterministically from one seed using `numpy.random.SeedSequence`: `problem`, `recognition`, `controls`, and `figures`. No module uses global `numpy.random` state.

### 6.2 Finite measures

`FiniteMeasure` stores a labeled finite support and nonnegative mass vector. `MarkovKernel` stores source/target labels and a row-stochastic matrix. Constructors validate finiteness, support identity, nonnegativity, and normalization where required.

`MeasurePair(reference, evidence_measure)` represents `rho` and the finite positive evidence submeasure `m_o = exp(-H_o) rho`, and enforces `m_o << rho`. `pushforward(kernel)` applies the same channel to both. Evidence is `m_o.total_mass`; the effective action is `-log(dm_o/drho)` only on positive coarse reference support. Pointwise likelihood density and evidence-submeasure mass are never conflated.

### 6.3 Exact VFE

For normalized posterior `pi = m/Z` and recognition law `q`,

`free_energy(q, pair) = KL(q || pi) - log(Z)`.

For a common channel `C`, the implementation reports:

- fine VFE;
- coarse VFE of `qC` against `piC`;
- conditional KL between reverse conditionals of `q` and `pi`;
- the residual `fine - coarse - conditional_kl` on the finite branch.

Zero-mass branches are explicit. Infinite extended values are represented as `math.inf`; an `inf-inf` residual is recorded as undefined rather than evaluated, and equality of two infinite values never licenses a recovery conclusion.

### 6.4 Local-to-collective coordinate identity

The finite laboratory disintegrates a joint posterior into a selected block and outside state. Two recognition laws share exactly the same outside marginal and differ only in the block conditional. The result reports the collective VFE difference and the outside-averaged conditional block-VFE difference. Their residual is the oracle; local VFEs are never summed over overlapping blocks. An approximate-outside mode, if later added, must retain the outside-marginal KL change.

### 6.5 Fisher contraction

A declared centered score for a finite parametric family is pushed through a fixed parameter-independent channel. The coarse score is computed by conditional expectation under the induced joint law. The laboratory reports fine Fisher information, coarse Fisher information, expected conditional score covariance, and the matrix residual. A recoverable-score control must have zero defect; an information-losing channel must have positive defect; the zero score is a valid zero tangent.

### 6.6 Full finite interactions

Against a declared product reference, all nonempty-subset Hoeffding/Mobius components are extracted and reassembled. The exact reconstruction residual must vanish. A retained order (for example pairwise) is an explicit projection; omitted components, the coordinate norm `sum_A ||g_A||_infinity`, and separately named quotient-sup and weighted-L2 diagnostics are persisted. A negative control must demonstrate a nonzero retained residual.

### 6.7 Gaussian realization

The Gaussian adapter builds an SPD precision from PSD self terms and symmetric PSD edge weights. Linear systems and log determinants use Cholesky or symmetric generalized-eigenvalue routines; explicit inverses are avoided. It implements:

- hard-identification/Galerkin aggregation `Lambda_c = S.T @ Lambda @ S`, explicitly distinct from Schur-complement Gaussian marginalization;
- block-diagonal passive frame changes applied by inverse congruence, with aggregation maps transformed in the same commuting square;
- scalar quadratic-energy invariance;
- generalized spectrum of `(L, Lambda)` under matched congruence;
- the flat aggregation formulas and internal-edge cancellation.

Condition numbers and Cholesky residuals are recorded. Near-singular or singular inputs fail with a typed domain error unless an experiment explicitly declares a different repaired model.

## 7. Click-to-run workflow

Each launcher exposes four small dictionaries:

```python
RUN = {"name": "finite_exact_smoke", "seed": 20260808}
THEORY = {"experiment": "finite_exact", "retained_interaction_order": 2}
NUMERICS = {"dtype": "float64", "atol": 1e-10, "rtol": 1e-9}
OUTPUT = {"root": "artifacts", "collect_diagnostics": True, "render_figures": True}
```

The guard calls a thin `main()` that resolves configuration, invokes `run_experiment(config)`, atomically publishes the run bundle, and returns the typed result. Tests and future sweep launchers import `run_experiment` directly. Figure rendering can be replayed independently and a rendering failure cannot invalidate numerical results.

## 8. Artifacts and reproducibility

Every run owns `artifacts/<run-name>/<config-hash>-<seed>/`. Existing completed runs are never silently overwritten. The run bundle contains:

- `config.json` with the resolved immutable configuration and its own hash;
- `manifest.json` with Git commit, dirty-tree digest, theory snapshot digest, input hashes, Python/NumPy/SciPy versions, platform, seed streams, and artifact completeness states;
- `metrics.json` with values, residuals, tolerances, and pass/fail/inconclusive dispositions;
- `arrays.npz` for exact numerical arrays;
- optional figures created from saved metrics rather than hidden simulator state.

JSON and NPZ publication uses sibling temporary files, flush/fsync where available, and `os.replace`. One provenance object is reused across all files. Diagnostics collection and figure rendering are independent toggles.

## 9. Pre-registered claim and experiment registry

| ID | Status | Prediction and null | Primary observable | Closure rule |
|---|---|---|---|---|
| FIN-01 | established conditional identity; implementation check | A common normalized channel preserves evidence mass; null is nonzero change. | `abs(Z_fine-Z_coarse)` | implementation verified only by exact/literal finite oracle plus passing current test |
| FIN-02 | established conditional identity; implementation check | Fine VFE equals coarse VFE plus conditional KL on the finite branch; null is nonzero residual. | chain-rule residual or structured infinite branch | implementation verified by hand-derived fixture and independent paths |
| FIN-03 | established conditional identity; implementation check | A block update with exactly fixed outside marginal has the same local and collective VFE difference. | delta residual | implementation verified by enumerated joint fixture |
| INF-01 | established conditional identity; implementation check | Fisher loss equals conditional score covariance and is PSD for a declared centered score. | matrix residual and minimum eigenvalue | implementation verified by analytic categorical score and losing/recoverable controls |
| INT-01 | established full-space identity plus retained-model diagnostic | Full finite interactions reconstruct exactly; a retained pairwise space can fail to close. | reconstruction and theorem-coordinate truncation norms | exact reconstruction plus a nonzero negative-control residual |
| GAU-01 | established coordinate identity; implementation check | Passive frame changes preserve quadratic energy and matched generalized spectrum under inverse congruence. | energy/spectrum residuals | hand-derived control plus seeded positive-orientation GL(K) metamorphics |
| GAU-02 | established conditional on the declared Gaussian interaction family | Flat Galerkin aggregation annihilates internal edges and adds cut weights. | coarse-block residuals | literal two-cluster matrix fixture and Schur-complement negative control |
| RG-01 | conjecture attack, later | Declared scalarized Gaussian rays may attract in a stated basin. | ray angle, normalized distance, remainder, scheme dispersion | never `EVIDENCE_VERIFIED` as a universal claim from finite trends |

Every experiment records supports/refutes/inconclusive thresholds before execution and carries a named control. A failed theorem-implementation check diagnoses the implementation or its applicability assumptions; it does not refute the theorem until those are independently cleared.

## 10. Testing and verification

Implementation follows strict red-green-refactor TDD. Expected values are literals or independently hand-derived fixtures, not results computed by the production helper under test. The first suite covers validation-before-effects, exact normalization, zero-support behavior, measure-pair pushforward, VFE chain rule, local/global delta, Fisher defect, interaction reconstruction/residual, gauge metamorphics, Gaussian aggregation, deterministic same-seed output, unique artifact ownership, canonical config hashing, atomic interruption behavior, and launcher smoke runs.

The project verification ledger is `.verification/ledger.json`. It is started only after the repository has a concrete `HEAD`, and it is rebound and validated against the final live artifact revision. Code and experiment claims require current machine-readable test output. Mathematics claims cite the frozen derivations; numerical agreement alone never closes them. Missing applicable evidence or unresolved disagreement is `INCONCLUSIVE`.

## 11. Error policy

- Invalid configuration: fail before RNG or artifact creation.
- Negative/nonfinite mass or non-stochastic channel: typed validation error.
- Unsupported absolute continuity: return an extended-real result with the failing support identified.
- Non-SPD Gaussian input: typed domain error with minimum-eigenvalue/Cholesky diagnostics; no silent regularization.
- Numerical tolerance failure: complete the run bundle with a failed disposition and all diagnostics; do not omit the artifact.
- Figure failure: numerical bundle remains valid and manifest marks the figure failed.

## 12. Success criteria for the first build slice

The first slice is complete when:

1. the supplied theory snapshot is tracked without content changes and its provenance is recorded;
2. both click-to-run launchers complete on CPU float64 with no CLI arguments;
3. all pre-registered FIN, INF, INT, and GAU implementation checks have passing current tests and named controls;
4. same-seed runs are numerically identical and publish nonclobbering, atomically written bundles;
5. a machine-readable JUnit file reports the exact current test totals;
6. `.verification/ledger.json` validates against the final Git/worktree digest; and
7. documentation states what was corroborated, what remains a conditional application obligation, and what remains open.

## 13. Explicit deferrals

No neural training, GPU path, checkpoint/resume engine, distributed execution, parameter sweep manager, GUI, web dashboard, arbitrary continuous state space, infinite-volume limit, learned coarse channel, automated partition selection, or universality claim belongs in Milestones 0–2. The interfaces leave room for them without prebuilding them.
