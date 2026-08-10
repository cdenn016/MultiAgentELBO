# Six-Session Laboratory Contract Freeze

Status: interface definition. This document freezes the shared implementation
contract for the six scientific sessions. It does not prove an application
hypothesis, certify a laboratory, establish universality, construct a continuum
limit, or establish a fixed-point theorem.

The contract was prepared against `origin/main` revision
`777be5398cd938abbbc1ac035d3fb5b2f0c32a7e`. The finite theory is established
only under its declared normalized-channel, reference-measure,
product-reference, bundle/configuration-map, recognition-lift, regularity,
related-section, and comparison-isomorphism hypotheses. A later laboratory must
check the applicable premises for its concrete data.

## User interface and scientific boundaries

Every laboratory remains a no-argument, click-to-run Python file with editable
configuration dictionaries. No `argparse` interface or other user-facing CLI is
part of this contract. An internal standalone worker process may accept the
versioned JSON/NPZ protocol below; that protocol is infrastructure behind a
launcher, not a user interface.

The following separations are mandatory:

- Numerical agreement is implementation or finite experimental evidence, not a
  mathematical proof.
- Finite trends do not establish universality, a thermodynamic or continuum
  limit, nonlinear attraction, or a fixed-point theorem.
- Graph-link holonomy is not base-connection holonomy unless an explicit curve
  assignment and transport identification are supplied.
- The Gaussian realization is one probability-law realization, not the ambient
  probability-law interface.
- A counterexample outside a theorem's hypotheses is an assumption-boundary
  witness, not a refutation of the conditional theorem.
- CUDA is optional acceleration for floating-point sweeps. It cannot replace an
  exact CPU oracle and it never falls back silently to CPU.

## Configuration API

The shared entry point is:

```python
ExperimentConfig.from_dicts(RUN, THEORY, NUMERICS, OUTPUT, COMPUTE=None)
```

The first four dictionaries retain their previous strict schemas. When
`COMPUTE` is omitted, the resolved effective compute record is CPU/float64, but
the compute record is omitted from canonical JSON. Consequently, every legacy
four-dictionary canonical JSON byte string and configuration SHA-256 remains
unchanged.

When `COMPUTE` is supplied, it has exactly these keys:

```python
COMPUTE = {
    "backend": "cpu",                 # "cpu" or "cuda"
    "dtype": "float64",              # float64, float32, or bfloat16
    "device_index": 0,
    "batch_size": 4096,
    "deterministic": True,
    "allow_tf32": False,
    "cpu_cuda_parity": True,
    "cuda_worker_python": r"C:\anaconda\python.exe",
    "heavy_sweep_enabled": False,
}
```

All keys and primitive types are exact; a Boolean is never accepted as an
integer. Device indices are nonnegative, batch sizes are positive, and the
worker path is absolute. CPU uses device index zero. Exact-rational experiments
are CPU-only. CUDA is reserved by this freeze for `gaussian_fixed_ray` and
requires CPU/CUDA parity. Float64 is the correctness and confirmation dtype.
Float32 is CUDA screening/throughput only and bfloat16 is CUDA exploratory only;
both require the explicitly enabled heavy sweep. TF32 is permitted only for an
explicit nondeterministic CUDA float32 screening run. A future widening of any
of these rules is a shared-contract change.

Validation completes before RNG construction, worker launch, run-directory
creation, or artifact publication. CUDA availability is runtime evidence and is
not inferred during pure configuration resolution.

## Frozen experiment discriminators and schemas

The discriminator order is normative:

1. `multiagent_network`
2. `theory_oracle`
3. `finite_counterexample`
4. `information_history`
5. `gauge_holonomy`
6. `scale_cocycle`
7. `gaussian_fixed_ray`

Each schema rejects missing and unknown keys.

### `multiagent_network` — Session 1

Launcher: `run_multiagent_network_lab.py`.

```python
THEORY = {
    "experiment": "multiagent_network",
    "fixture": "two_scale_application_v1",
    "scenario": "aligned",  # aligned, frustrated, asymmetric_evidence, higher_order
    "arithmetic": "exact_rational",
}
```

Artifacts: `fine_law`, `coarse_law`, `fine_to_coarse_channel`,
`hoeffding_interactions`, `local_collective_differences`, and
`configuration_scale_map`.

Metrics: `evidence_residual`, `elbo_gap_residual`,
`local_collective_residual`, `hoeffding_reconstruction_residual`,
`recognition_lift_residual`, and `pairwise_retained_residual`.

### `theory_oracle` — Session 2

Launcher: `run_theory_oracle_lab.py`.

```python
THEORY = {
    "experiment": "theory_oracle",
    "fixture": "two_scale_application_v1",
    "oracle_set": "core_identities",
    "arithmetic": "exact_rational",
}
```

Artifacts: `exact_numerators`, `exact_denominators`,
`theorem_assumption_matrix`, and `literal_commuting_diagrams`.

Metrics: `elbo_oracle_residual`, `fisher_defect_oracle_residual`,
`marked_event_associativity_residual`, `hoeffding_oracle_residual`, and
`gaussian_linear_algebra_oracle_residual`.

### `finite_counterexample` — Session 3

Launcher: `run_finite_counterexample_lab.py`.

```python
THEORY = {
    "experiment": "finite_counterexample",
    "fixture": "counterexample_catalog_v1",
    "max_states": 4,
    "max_denominator": 8,
    "arithmetic": "exact_rational",
}
```

Artifacts: `enumeration_bounds`, `candidate_records`, `minimal_witnesses`, and
`stress_matrix`. Candidate records retain `claim_id`,
`inside_declared_domain`, `assumptions_satisfied`, `smallest_witness`,
`exact_or_numeric`, `observed_residual`, and `classification`.

Metrics: `support_violation_count`, `parameter_dependent_channel_gap`,
`single_law_relabeling_gap`, `marked_event_source_mass_gap`, and
`pairwise_truncation_residual`.

### `information_history` — Session 4

Launcher: `run_information_history_lab.py`.

```python
THEORY = {
    "experiment": "information_history",
    "fixture": "two_scale_application_v1",
    "family": "categorical_softmax",
    "history_steps": 16,
    "step_size": 0.05,
}
```

Artifacts: `history_parameters`, `scores`, `fisher_matrices`,
`vfe_gradients`, `natural_gradient_fields`, `information_durations`, and
`semiconjugacy_defects`.

Metrics: `score_finite_difference_residual`, `fisher_defect_residual`,
`natural_gradient_range_residual`, `arc_length_reparameterization_residual`,
and `semiconjugacy_defect_norm`.

### `gauge_holonomy` — Session 5

Launcher: `run_gauge_holonomy_lab.py`.

```python
THEORY = {
    "experiment": "gauge_holonomy",
    "fixture": "two_scale_application_v1",
    "scenario": "nonflat_plaquette",
    # flat_tree, flat_cycle, nonflat_plaquette,
    # frustrated_transport, or staged_aggregation
    "group": "GL+(2)",
}
```

Artifacts: `interaction_complex`, `oriented_links`, `vertex_frames`,
`cycle_holonomies`, `operational_record_laws`, and `aggregation_stages`.

Metrics: `passive_covariance_residual`,
`cycle_conjugacy_invariant_residual`, `trivialization_residual`,
`operational_observable_residual`, and `broken_link_negative_control`.

### `scale_cocycle` — Session 6

Launcher: `run_scale_cocycle_lab.py`.

```python
THEORY = {
    "experiment": "scale_cocycle",
    "fixture": "two_scale_application_v1",
    "extension": "three_level_composition_v1",
    "retained_interaction_order": 2,
    "arithmetic": "exact_rational",
}
```

The extension is a Session-6 object. It is not part of the shared two-scale
application claim or its application ID.

Artifacts: `three_level_extension`, `composed_channels`, `coarse_actions`,
`posterior_bridges`, `comparison_isomorphisms`, `derivative_cocycle`, and
`retained_projection_residual`.

Metrics: `direct_staged_pushforward_residual`,
`cocycle_composition_residual`, `retained_beta_residual`,
`full_interaction_reconstruction_residual`, and
`wrong_order_negative_control`.

### `gaussian_fixed_ray` — Session 6

Launcher: `run_gaussian_fixed_ray_lab.py`.

```python
THEORY = {
    "experiment": "gaussian_fixed_ray",
    "fixture": "gaussian_fixed_ray_v1",
    "preregistration": "2026-08-09-gaussian-fixed-ray-v1",
    "blocking_schemes": ["adjacent_pairs", "balanced_alternating"],
    "matrix_dimension": 2,
}
```

Artifacts: `preregistered_job_table`, `initial_conditions`,
`per_seed_endpoints`, `backend_provenance`, `parity_matrix`, and
`performance_records`.

Metrics: `projective_ray_angle`, `normalized_coupling_distance`,
`off_family_nonlinear_remainder`, `retained_beta_residual`,
`basin_exit_rate`, `blocking_scheme_dispersion`, and
`cpu_cuda_parity_residual`.

The registry in `multiagent_elbo.experiment_support.EXPERIMENT_REGISTRY` is a
read-only mapping of frozen dataclass records. Parallel lanes consume it but do
not edit it.

## Claim and metric typing

Every new claim and metric carries three independent fields with exactly these
uppercase vocabularies:

- `theorem_status`: `ESTABLISHED`, `HYPOTHESIS`, `CONJECTURE`, `NUMERICAL`, or
  `OPEN`.
- `verification_state`: `CANDIDATE`, `LLM_SUPPORTED`, `EVIDENCE_VERIFIED`,
  `REFUTED`, or `INCONCLUSIVE`.
- `claim_origin`: `STANDARD`, `PROJECT_NOVEL`, or `APPLICATION_SPECIFIC`.

Metric `status` remains `pass`, `fail`, or `inconclusive`. It reports an
implementation threshold only. It cannot alter or infer any of the three claim
fields. In particular, a passing metric can remain `OPEN/INCONCLUSIVE`, and a
failing implementation check does not change an `ESTABLISHED` conditional
identity into a refuted theorem.

Legacy metric callers are preserved by an explicit adapter policy. The legacy
lowercase values `established_conditional_identity`,
`finite_metamorphic_identity`, and `negative_control` remain accepted verbatim.
When those callers omit the two new fields, the adapter records
`verification_state=CANDIDATE` and `claim_origin=PROJECT_NOVEL`; it does not
retroactively reclassify old evidence. A caller using an uppercase canonical
theorem status through the metric factories must supply verification state and
claim origin explicitly.

## Versioned two-scale application fixture

The immutable fixture is `tests/fixtures/two_scale_application_v1.json`.
Its application ID is:

```text
30a4bd77e738fbb73b3326ec009995ec7b2bc94f20c96e9e286644bdeec620cd
```

The application ID is the SHA-256 of UTF-8 canonical JSON with sorted keys,
compact `(',', ':')` separators, ASCII escaping enabled, and only the top-level
`application_id` field omitted. The physical fixture-file SHA-256 is a separate
provenance value because whitespace changes do not change the application ID.

All rational literals are reduced strings. The fixture declares four binary
agents, the `B01={0,1}` and `B23={2,3}` organization, a four-cycle interaction
complex, one three-agent higher-order hyperedge, exact fine labels `0000` through
`1111`, and exact coarse labels `00`, `01`, `10`, `11`. Its single arrow is a
strictly positive, normalized, recognition-independent fine-to-coarse Markov
kernel. No additional scale arrow is part of this application identity.

The fine reference is a product reference and the coarse reference is a
block-product reference. The correlated baseline gives each even-parity state
three times the mass of an odd-parity state. A binary observation kernel,
observed evidence submeasure, evidence mass, and posterior are literal. The
recognition family, extraction, product lift, and right-inverse type are
declared, but the application check is explicitly `NOT_CHECKED`. The fixture
also declares configuration coordinates, the two-block coarse matrix,
within-level comparison isomorphisms, local updated/outside axes, assumption
records, witness records, and not-yet-checked conclusion records.

The fixture validator checks the digest, exact labels, rational-string typing,
normalization, one-arrow boundary, reference typing, correlated-baseline
witness, evidence consistency, recognition-law normalization, configuration
matrix shapes, right-inverse check state, higher-order hyperedge, and canonical
claim metadata. Passing that structural validator does not certify every later
application premise.

## Standalone worker protocol

The internal protocol version is `cuda-worker-protocol-v1`. The Python 3.14
controller passes validated JSON plus exactly one hashed NPZ payload to a
standalone Python 3.12 worker. The worker does not import the project as an
installed Python-3.14 package.

Every request and response manifest has exactly these keys:

```text
schema_version
message_type
job_id
requested_backend
requested_dtype
effective_backend
effective_dtype
environment_sha256
npz_sha256
arrays
output_identity
```

`message_type` is `request` or `response`. Job IDs contain only letters,
digits, period, underscore, and hyphen, begin with an alphanumeric character,
and have at most 128 characters. Backend is `cpu` or `cuda`; requested and
effective scientific dtypes are `float64`, `float32`, or `bfloat16`. A request
uses null effective fields and null output identity. A response must report an
effective backend and dtype identical to the request; any future authorized
conversion requires a new protocol version rather than silent rewriting.

Every array descriptor has exactly `name`, `shape`, `dtype`, and `sha256`.
Names follow the job-ID character rule and are unique. Shape entries are
nonnegative integers so explicit zero-support cases remain representable.
Descriptor dtypes are `float64`, `float32`, `bfloat16`, `int64`, or `bool`.
All digests are lowercase 64-hex SHA-256 strings. The NPZ digest hashes the
exact NPZ file bytes. A descriptor digest hashes this byte sequence, with `||`
denoting concatenation:

```text
UTF-8("cuda-worker-array-v1\0")
|| UTF-8(name) || 0x00
|| ASCII(dtype) || 0x00
|| UTF-8(canonical shape JSON) || 0x00
|| canonical C-order data bytes
```

Canonical shape JSON uses no whitespace. Floating values use their IEEE-754
little-endian bit patterns (`bfloat16` uses its little-endian 16-bit pattern),
`int64` uses little-endian two's-complement bytes, and `bool` uses one byte per
element, `0x00` or `0x01`. Empty arrays have an empty data-byte suffix.

A response is validated only together with the original validated request.
Its job ID, requested backend/dtype, and environment digest must match that
request directly. The response `output_identity` is the SHA-256 of canonical
UTF-8 JSON for the object `{"request": request, "response": response}` after
replacing `output_identity` with null in both embedded manifests. Canonical JSON
uses `sort_keys=true`, `separators=(',', ':')`, `ensure_ascii=true`, no byte-order
mark, and no trailing newline. Consequently the identity also binds the exact
input NPZ digest and all input descriptors from the original request, as well
as the complete response. A response without its original request is rejected.
Both sides validate the schema, message role, job ID, environment digest, NPZ
digest, descriptors, request binding, requested/effective identity, and bound
response identity before accepting output. This freeze supplies validation
only; it implements no worker or scientific CUDA kernel.

## CUDA environment record

The durable record is `environments/cuda-rtx5090-cu128.lock.txt`. Its run-time
identity is the SHA-256 of the exact UTF-8 file bytes. The record pins the
worker executable and hash, Python version, Torch build, Torch CUDA runtime,
driver, device, compute capability, cuDNN, queryable cuBLAS library data,
current precision/determinism state, required future worker controls, and the
canonical worker dependency inventory and digest.

The Wave-0 snapshot found Python 3.12.7, Torch
`2.10.0.dev20251210+cu128`, CUDA available, CUDA runtime 12.8, driver 576.88,
an NVIDIA GeForce RTX 5090 with compute capability 12.0, cuDNN 91002, NumPy
2.0.0, and cuBLAS as the selected BLAS backend. This time-dependent record must
be rechecked before a worker run. Torch and CUDA remain absent from project
runtime dependencies.

## Artifact and publication contract

Every future run bundle retains canonical configuration and hash, source
revision and dirty-tree binding, theory snapshot digest, interpreter and
dependency versions, named RNG streams, input hashes, all three claim fields,
effective backend/dtype, exact-or-floating provenance, arrays sufficient to
recompute each reported metric, and CPU/CUDA provenance when applicable.
Failure manifests and figure manifests remain distinct. Numerical publication
finalizes before saved-artifact-only rendering, and renderer failure cannot
mutate the numerical bundle.

## Coverage and test evidence

`pytest-cov>=7.0` is an approved test-only dependency. No lockfile is changed by
this freeze. Coverage uses branch measurement with source
`src/multiagent_elbo`, emits XML by explicit command, and enforces at least 80%
line coverage for new production code. The Wave-0 focused command is:

```powershell
C:\Python314\python.exe -m pytest tests/test_config.py tests/test_experiment_support.py `
  --basetemp=.pytest-tmp/wave0-coverage `
  --cov=multiagent_elbo.config --cov=multiagent_elbo.experiment_support `
  --cov-report=term-missing --cov-report=xml:.verification/wave0/coverage.xml `
  --junitxml=.verification/wave0/pytest-focused.xml
```

The full CPU suite uses `C:\Python314\python.exe` and emits JUnit XML. Any claim
about Torch or CUDA uses `C:\anaconda\python.exe`; the CPU interpreter is never
evidence of CUDA availability.

## Ownership and re-freeze rule

After the Wave-0 commit, all shared contract paths are frozen during parallel
implementation: `config.py`, `experiment_support.py`, shared artifact/runtime/
rendering modules, package exports, existing launchers, shared tests,
`pyproject.toml`, `uv.lock`, `.gitignore`, README, hypotheses, and `Theory/**`.
Each session owns only the paths assigned in the governing implementation plan.

If a lane needs a shared-interface change, it stops and writes a change request.
A nonblocking request waits for serial integration. A blocking request halts all
affected lanes; the integration owner publishes a reviewed replacement contract
commit, and every affected lane is recreated or explicitly rebased onto that
exact SHA. All affected evidence is rerun. No lane continues against a
superseded contract or edits the registry independently.
