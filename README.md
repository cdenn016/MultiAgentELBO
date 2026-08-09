# MultiAgentELBO

MultiAgentELBO is an exact, finite simulation laboratory for studying the
conditional identities and explicit counterexamples in the `gauge_vfe_rg`
theory. The first foundation release contains two deliberately separated
layers:

- a universal finite categorical core for measures, Markov coarse graining,
  VFE/KL decompositions, Fisher contraction, full Hoeffding interactions, and
  finite relabeling metamorphics;
- a typed multivariate-Gaussian realization for matrix-weighted interactions,
  hard-identification/Galerkin restriction, Schur-complement marginalization,
  and passive local-frame congruence checks.

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

Then open either launcher, edit only its `RUN`, `THEORY`, `NUMERICS`, and
`OUTPUT` dictionaries, and run the file:

- `run_finite_lab.py` runs the exact finite laboratory.
- `run_gaussian_lab.py` runs the Gaussian realization laboratory.
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
| `THEORY` | `experiment`, `retained_interaction_order` | Selects the finite or Gaussian laboratory and the retained finite interaction order where applicable. |
| `NUMERICS` | `dtype`, `atol`, `rtol`, `min_spd_rcond`, `max_frame_condition` | Declares floating-point precision, comparison tolerances, and explicit Gaussian conditioning gates. |
| `OUTPUT` | `root`, `collect_diagnostics`, `render_figures` | Selects the artifact root and independently toggles diagnostic arrays and post-finalization rendering. |

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
    arrays.npz
    diagnostics.npz       # only when collect_diagnostics=True
```

The resolved configuration is content-addressed. Files are written through
same-directory temporary files and atomically replaced, the manifest becomes
complete only after its exact inventory is validated, and a complete run is
never silently overwritten. Rendering happens only after numerical
finalization and publishes to a sibling figure directory. A renderer failure
cannot change the numerical result or its bytes.

`render_figures=True` creates the requested PDF/300-DPI PNG pair automatically.
For a later pure replay, edit `REPLAY` in `make_figures.py` to point at a
finalized run. Replays use only saved `metrics.json` and `arrays.npz`; they do
not recompute the experiment.

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

The preregistered status and falsification rules for every named metric are in
`docs/hypotheses.md`. The current machine results and verification scope are in
`docs/results/2026-08-09-foundation-results.md`.

## Theory and evidence boundary

`Theory/` is a byte-matched, read-only snapshot of the Research-vault
`manuscripts/gauge_vfe_rg` source used to type the implementation. Its precise
revision, dirty-source caveat, and aggregate digest are recorded in
`docs/theory-provenance.md`.

Passing tests establish that this code reproduces the declared finite fixtures
and metamorphic identities. They do not prove the analytic theory, establish
DQM for an arbitrary statistical family, show that an arbitrary application
belongs to the declared Gaussian interaction family, or establish RG
attraction/universality. Continuum limits, nontrivial holonomy and connections,
attention composition, empirical partition selection, and universality studies
remain later milestones.

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

One Windows-only symlink regression is skipped when the current account lacks
the privilege needed to create a test symlink. The executed hard-link tests and
the static reparse-point checks still protect the artifact ownership boundary;
the skipped dynamic symlink case is reported explicitly in the results rather
than counted as exercised evidence.
