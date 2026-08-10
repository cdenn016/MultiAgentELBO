# MultiAgentELBO

MultiAgentELBO is an exact, finite simulation laboratory for studying the
conditional identities and explicit counterexamples in the `gauge_vfe_rg`
theory. The current release contains eleven deliberately separated
layers:

- a universal finite categorical core for measures, Markov coarse graining,
  VFE/KL decompositions, Fisher contraction, full Hoeffding interactions, and
  finite relabeling metamorphics;
- a typed multivariate-Gaussian realization for matrix-weighted interactions,
  hard-identification/Galerkin restriction, Schur-complement marginalization,
  and passive local-frame congruence checks;
- an exact finite marked-event attention laboratory for normalized
  `eta = alpha * beta`, associative joint-law coarsening, scalar gauge
  metamorphics, and beta-only negative controls; and
- a positive three-category exponential-family laboratory separating the
  analytic finite-support DQM derivation from finite-difference, remainder,
  conditional-score, and Fisher-loss implementation diagnostics;
- exact multi-agent network, independent theory-oracle, and finite
  counterexample laboratories for the frozen two-scale application;
- information-history and gauge-holonomy laboratories with typed scope and
  explicit negative controls; and
- exact scale-cocycle and preregistered Gaussian fixed-ray laboratories, with
  the CUDA-dependent fixed-ray claim left inconclusive until its operator gate
  and float64 sentinel prerequisites are satisfied.

The repository does not expose an application CLI. Experiment choices live in
plain configuration dictionaries at the top of click-to-run Python files.

## Start here

The project requires Python 3.14 with NumPy, SciPy, and Matplotlib. The local
machine used for this release runs it with `C:\Python314\python.exe`. If the
dependencies are not already available, install the project once from the
repository directory:

```powershell
C:\Python314\python.exe -m pip install -e ".[test]"
```

Then open any laboratory launcher, edit only its `RUN`, `THEORY`, `NUMERICS`, and
`OUTPUT` dictionaries, and run the file:

- `run_finite_lab.py` runs the exact finite laboratory.
- `run_gaussian_lab.py` runs the Gaussian realization laboratory.
- `run_attention_lab.py` runs the state-conditioned marked-event attention
  laboratory.
- `run_categorical_dqm_lab.py` runs the positive categorical DQM/Fisher
  laboratory.
- `run_multiagent_network_lab.py` runs the exact two-scale multi-agent cases.
- `run_theory_oracle_lab.py` runs independent literal theory oracles.
- `run_finite_counterexample_lab.py` runs the bounded counterexample catalog.
- `run_information_history_lab.py` runs finite information histories.
- `run_gauge_holonomy_lab.py` runs the finite graph-link holonomy scenarios.
- `run_scale_cocycle_lab.py` runs the exact three-level scale cocycle.
- `run_gaussian_fixed_ray_lab.py` runs the non-heavy CPU pilot; it does not
  opt into CUDA or the confirmatory sweep.
- `make_figures.py` replays figures from an already finalized run without
  rerunning the numerical experiment.

The launchers insert their adjacent `src/` directory themselves, so they also
run directly from a fresh checkout without an editable install once the three
runtime dependencies are present. They accept no command-line flags and do no
work merely by being imported.

## Configuration dictionaries

| Dictionary | Fields | Meaning |
|---|---|---|
| `RUN` | `name`, `seed` | Human-readable run identity and the root seed for four named RNG streams. |
| `THEORY` (`finite_exact`, `gaussian_realization`) | `experiment`, `retained_interaction_order` | Selects the foundation laboratory and the retained finite interaction order where applicable. |
| `THEORY` (`attention_marked_event`) | `experiment`, `fixture` | Selects the frozen `nested_nonuniform_v1` marked-event fixture. |
| `THEORY` (`categorical_dqm`) | `experiment`, `fixture`, `theta`, `finite_difference_step`, `dqm_step_sizes` | Selects the frozen positive categorical family, parameter, centered-difference step, and two-sided DQM diagnostic ladder. |
| `THEORY` (six-session buildout) | Experiment-specific fields frozen in `docs/superpowers/specs/2026-08-09-six-session-laboratory-contract.md` | Selects one of `multiagent_network`, `theory_oracle`, `finite_counterexample`, `information_history`, `gauge_holonomy`, `scale_cocycle`, or `gaussian_fixed_ray`. |
| `NUMERICS` | `dtype`, `atol`, `rtol`, `min_spd_rcond`, `max_frame_condition` | Declares floating-point precision, comparison tolerances, and explicit Gaussian conditioning gates. |
| `OUTPUT` | `root`, `collect_diagnostics`, `render_figures` | Selects the artifact root and independently toggles diagnostic arrays and post-finalization rendering. |
| `COMPUTE` (Session 6 only) | Frozen backend, dtype, device, determinism, worker, and heavy-sweep fields | Keeps ordinary CPU execution separate from the gated CUDA worker protocol. |

Configuration validation is strict: missing or unknown keys, unsupported
types, invalid tolerances, and incompatible experiment selections fail before
the RNG or filesystem is touched. Only `float64` is admitted in this first
release.

## Artifact contract

A numerical run is written to:

```text
<root>/<sanitized-run-name>/<config-sha256>-<seed>/
    config.json
    manifest.json
    metrics.json
    arrays.npz or one or more named numeric archives
    diagnostics.npz       # experiment-specific and optional
    additional JSON records declared by the experiment contract
```

The resolved configuration is content-addressed. Files are written through
same-directory temporary files and atomically replaced, the manifest becomes
complete only after its exact inventory is validated, and a complete run is
never silently overwritten. Rendering happens only after numerical
finalization and publishes to a sibling figure directory. A renderer failure
cannot change the numerical result or its bytes.

`render_figures=True` creates the requested PDF/300-DPI PNG pair automatically
where the launcher exposes inline rendering. For a later pure replay, edit
`REPLAY` in `make_figures.py` to point at a finalized run. Replays use only
saved `metrics.json` and the complete numeric archives listed in the manifest;
they do not recompute the experiment. The shared renderer supports the seven
new diagnostic figures `multiagent_network`, `theory_oracles`,
`finite_counterexamples`, `information_history`, `gauge_holonomy`,
`scale_cocycle`, and `gaussian_fixed_ray`.

## What is checked

The finite launcher exercises implementation checks for:

- evidence-mass preservation under a common Markov channel;
- the finite VFE channel chain rule, including structured support violations;
- the fixed-outside local-to-collective VFE difference;
- Fisher loss as conditional score covariance;
- exact full-interaction reconstruction and pairwise-retention counterexamples;
- coherent componentwise finite relabeling and a deliberately mismatched
  negative control.

The Gaussian launcher exercises implementation checks for:

- the distinction between Galerkin restriction and Schur marginalization;
- scalar and matrix-valued Schur-complement literal oracles;
- an unrestricted-Kron nonclosure witness;
- inverse-congruence energy, determinant, log-determinant, generalized-spectrum,
  eigenpair, and metric-orthogonality identities;
- the noninvariance of ordinary Laplacian eigenvalues under nonorthogonal local
  frame changes;
- SPD, reciprocal-condition, positive-orientation, and frame-condition gates.

The attention launcher exercises implementation checks for:

- exact marked-event factorization and normalization, including inactive-row
  representatives;
- direct-versus-staged state and node pushforward of `eta`, followed by
  disintegration into `alpha` and active-row `beta`;
- independently pinned rational values and reverse state bridges;
- coherent local `GL+(2)` recomputation and finite node relabeling; and
- broken-link, incoherent-relabeling, and beta-only controls that remain
  detectably separated from the exact construction.

The categorical DQM launcher exercises implementation checks for:

- probability normalization, score centering, and analytic-versus-centered-FD
  fine scores;
- the positive/negative normalized square-root likelihood remainder ladder;
- conditional-expectation coarse scores versus independently pushed FD scores;
- Fisher loss as expected conditional score covariance, including positive
  loss and PSD checks; and
- literal rational oracles plus an intentionally wrong unweighted-score
  control at the default parameter.

The six-session buildout additionally checks exact application tuples,
independent rational oracles, minimal finite counterexamples, Fisher-metric
history lengths and semiconjugacy defects, graph-link holonomy and operational
marked-event laws, exact nonautonomous scale composition, and a bounded
Gaussian fixed-ray CPU pilot. Each laboratory preserves separate
`theorem_status`, `verification_state`, and `claim_origin` fields. The fixed-ray
CUDA parity metric remains `INCONCLUSIVE`; no CPU result is presented as CUDA
evidence.

The preregistered status and falsification rules for every named metric are in
`docs/hypotheses.md`. The foundation record remains in
`docs/results/2026-08-09-foundation-results.md`; the attention/DQM results and
current full-suite evidence are in
`docs/results/2026-08-09-attention-categorical-dqm-results.md`. The seven new
lane records and the serial-integration summary are indexed by
`docs/results/2026-08-10-six-session-integration-results.md`.

## Theory and evidence boundary

`Theory/` is a byte-matched, read-only snapshot of the Research-vault
`manuscripts/gauge_vfe_rg` source used to type the implementation. Its precise
revision, dirty-source caveat, and aggregate digest are recorded in
`docs/theory-provenance.md`.

Passing tests establish that this code reproduces the declared deterministic
finite fixtures and metamorphic identities. The categorical family's DQM status
comes from its finite-support smooth-positive Taylor derivation; the remainder
ladder only corroborates that implementation numerically. These checks do not
establish DQM for an arbitrary family, infer parameter-independence of an
unexamined channel family, make beta-only coarsening associative, show that an
external system belongs to the Gaussian or marked-event fixtures, or establish
RG attraction/universality. The holonomy laboratory establishes only its
declared finite graph-link identities and operational fixture. Continuum
limits, continuum connections, empirical partition selection, and universality
studies remain later milestones.

## Repository map

```text
src/multiagent_elbo/finite/                 exact finite probability layer
src/multiagent_elbo/geometry/               finite relabeling metamorphics
src/multiagent_elbo/realizations/gaussian/  Gaussian-only adapter
src/multiagent_elbo/figures.py              pure saved-artifact renderer
Theory/                                     frozen theory input
tests/                                      literal, boundary, and integration checks
docs/                                       design, plan, hypotheses, results, evidence
```

Run the complete test suite with:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider
```

The post-reconciliation integration JUnit record contains 698 collected tests: 696
passed, zero failed, zero errored, and two were skipped for the Windows symlink
privilege described below. CUDA parity and the heavy confirmatory sweep are not
part of this CPU count.

Two Windows-only symlink regressions are skipped when the current account lacks
the privilege needed to create test symlinks: one numerical-artifact ownership
case and one figure-publication escape case. The executed hard-link tests and
the static reparse-point checks still protect the ownership boundaries; both
skips are reported explicitly rather than counted as exercised evidence.
