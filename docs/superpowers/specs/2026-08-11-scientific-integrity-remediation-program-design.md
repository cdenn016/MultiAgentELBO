# Scientific Integrity Remediation Program Design

Date: 2026-08-11

Status: approved for implementation planning; adversarial architecture,
evidence-control, and manuscript-wave reviews passed

Program base revision: `f078e6693bcbbcd7965fba12dfa833cbad9b3b4f`

Audit baseline revision: `aedc6621a4e4f1c725a54f8b287aac425ef833d8`

Governing audit: `docs/audits/2026-08-11-post-fixed-ray-deep-audit.md`

Research context revision: `c9f237d2ca54c274ba5760012e62823a69d203a3`

## Purpose

The post-fixed-ray audit retained 22 defects without invalidating the completed
fixed-model endpoint diagnosis. This program repairs those defects in dependency-
ordered waves while preserving the project's scientific status boundaries,
historical artifacts, public APIs where practical, and live user worktrees.

The program is not a single refactor. It is a sequence of separately reviewed and
separately merged changes:

```text
Wave 0 -> Wave A -> Wave B -> Wave C -> Wave D0 -> conditional Wave D1
                          \
                           +-- Wave E in the Research repository
```

Wave E can proceed in parallel after its own contract freeze, but it never shares
a commit, branch, ledger, or publication gate with MultiAgentELBO.

## Scientific boundary retained from the completed diagnosis

The existing Gaussian fixed-ray evidence remains a historical, revision-bound
result. Nothing in this program changes these conclusions:

- the frozen `-0.02` practical-support endpoint was structurally unreachable in
  the admitted coefficient basin;
- the completed primary analyzer classification remains `inconclusive`;
- fixed-map projective attraction remains mathematically `INCONCLUSIVE`;
- unrestricted attraction, an RG fixed point or semigroup, universality, and a
  continuum limit remain `OPEN`/`INCONCLUSIVE`; and
- producer records remain `CANDIDATE`; only an external, validated ledger may
  close a claim for an exact artifact revision.

Later source revisions do not rewrite or silently rebind the old confirmatory,
sentinel, or fixed-model diagnostic bundles. They may reproduce those bundles as
explicit compatibility tests, but any new scientific claim requires new evidence
bound to the new revision.

## Goals

1. Make mathematical type construction enforce probability, positivity,
   semidefinite, conditioning, Fisher-quotient, and KL invariants independently
   of user-configurable comparison tolerances.
2. Make finalized run and figure records verify the bytes they consume and publish.
3. Make every accepted scientific configuration field reach the execution it
   describes, or reject the unsupported value before side effects.
4. Make CPU and CUDA fixed-ray paths share one exact system identity.
5. Measure the heavy CUDA and counterexample paths before changing their execution
   architecture.
6. Correct the manuscript inference from graph connectedness to a unique limiting
   fixed point while preserving the surrounding conditional algebra.
7. Close every audit item with revision-bound mechanical or mathematical evidence,
   never by agent consensus.

## Non-goals

- No cryptographic threat model, forgery resistance, remote-attestation system, or
  Git-security project is introduced. Hashes serve reproducibility and accidental
  drift detection.
- No historical artifact is modified in place.
- No new attraction, universality, physical-time, continuum, or RG theorem is
  claimed.
- No CUDA run occurs merely because code is changed. CUDA operational closure
  requires a fresh user-approved idle-GPU gate and the exact prescribed sentinel.
- No performance optimization is accepted before causal measurement.
- No live dirty checkout is reset, stashed, cleaned, switched, or overwritten.
- No Research-vault edit is coupled to a MultiAgentELBO code commit.

## Alternatives considered

### Alternative 1: patch only the three high findings

This is fast but leaves the high fixes resting on broken neighboring contracts.
For example, a fixed-ray identity validator still needs a canonical output-root
resolver and a stable matrix-domain policy; a KL clamp applied without structural
normalization could hide malformed probability laws. This alternative is rejected.

### Alternative 2: one 22-finding refactor

This minimizes branch count but maximizes evidence invalidation, review surface,
and ambiguity when a regression occurs. It would also mix manuscript claims, CPU
mathematics, artifact publication, and CUDA protocol changes. This alternative is
rejected.

### Alternative 3: dependency-ordered, independently closed waves

Each wave establishes an interface needed by the next, receives targeted and full
verification, and is merged before the next wave starts. Performance work remains
conditional on measurement, and the manuscript stays in its own repository. This
is the selected architecture.

## Wave 0: contract and migration freeze

Wave 0 is documentation and test-contract work. It freezes the program before
production code changes.

### Required records

1. An audit-disposition table maps every `AUD-01` through `AUD-22` to exactly one
   owning wave, affected public interfaces, RED reproducer, GREEN guard, evidence
   class, and final status.
2. A compatibility inventory lists every public constructor, serialized schema,
   launcher dictionary, artifact reader, and package-root export touched by the
   program.
3. A status inventory separates:
   - mathematical theorem status;
   - producer verification state;
   - run status;
   - external ledger state; and
   - historical evidence that remains valid only at an older revision.
4. A migration table freezes schema-version behavior. New strict formats receive
   new versions; old bundles are never silently rewritten.
5. A failure-order table identifies the last permitted side effect for each public
   entry point. Validation that can be performed without I/O must occur before any
   output directory, gate file, worker process, GPU query, or cache mutation.

### Wave ownership

| Wave | Audit items | Closure boundary |
|---|---|---|
| A | `AUD-03`, `AUD-13`, `AUD-14`, `AUD-15`, `AUD-16`, `AUD-17`, `AUD-18` | Mathematical and numerical invariants |
| B | `AUD-01`, `AUD-02`, `AUD-04`, `AUD-05`, `AUD-10`, `AUD-11`, `AUD-12` | Publication and runtime integrity |
| C | `AUD-06`, `AUD-07`, `AUD-08`, `AUD-09`, `AUD-19` | Experiment and CUDA execution identity |
| D | `AUD-21`, `AUD-22` | Measurement, then conditional optimization |
| E | `AUD-20` | Research manuscript claim correction |

`AUD-19` consumes Wave A's matrix assessment but closes in Wave C when the
fixed-ray system and all execution entry points enforce it.

## Wave A: invariant-preserving mathematical types

Wave A is CPU-only. It changes type membership and numerical semantics, not CUDA
protocols or historical scientific conclusions.

### A1. Structural probability canonicalization (`AUD-03`, part of `AUD-13`)

Introduce one internal float64 structural canonicalizer used by
`ProbabilityMeasure`, `MarkovKernel`, probability-table validators, and
information-history probability inputs. `FiniteMeasure` remains intentionally
unnormalized.

For a nonnegative finite vector `x` of length `n`, define

```text
s = math.fsum(float(x_i) for x_i in x)
tau_n = 8 * n * eps_float64
```

The canonicalizer:

1. rejects Boolean, nonfinite, or negative entries;
2. rejects `s <= 0` or `abs(s - 1) > tau_n`;
3. divides by `s`;
4. adds `1 - math.fsum(y)` to the largest component;
5. rechecks finite nonnegative entries and exact `math.fsum(y) == 1.0`; and
6. returns a C-contiguous float64 array backed by immutable `bytes`.

The same rule applies independently to every Markov row. `NumericsConfig.atol`
and `rtol` remain valid comparison tolerances but never decide probability-type
membership. The policy deliberately rejects a total of `0.8`, a zero law, and a
zero Markov row even if the configured tolerances are large.

Probability tables use the same rule on their flattened entries and then restore
the declared shape. Chart-specific requirements are applied afterward; for
example, a positive-softmax chart still rejects every zero component even though a
general probability law may contain zeros.

Caller arrays are copied before validation. `FiniteMeasure` does not use the unit-
mass canonicalizer, but its finite nonnegative masses use the same immutable-array
helper. Authoritative public arrays retain the existing NumPy interface but use
immutable byte backing, so `setflags(write=True)` fails. Any helper returning an
authoritative array uses the same boundary; scratch arrays used only within a
calculation may remain mutable.

### A2. Stable KL and VFE arithmetic (`AUD-18`, dependent on A1)

All KL paths use one helper with the existing support convention:

- `q_i > 0` and `p_i == 0` returns positive infinity;
- `q_i == 0` contributes exactly zero;
- finite terms use `log(q_i) - log(p_i)` rather than a potentially overflowing
  ratio; and
- terms are accumulated with `math.fsum`.

For finite terms `t_i`, define the nonconfigurable cancellation bound

```text
b = 64 * n * eps_float64 * max(1, math.fsum(abs(t_i)))
```

If `D < -b`, raise `ArithmeticError`. If `-b <= D < 0`, return canonical `0.0`.
Otherwise return `D`. This clamp is reachable only after A1 has established valid
probability objects; it cannot hide the material negative KL caused by a malformed
law.

The same helper supplies ordinary KL, conditional KL, coarse KL, and block-update
KL. Existing public return types and infinity semantics remain stable.

### A3. Shared symmetric-matrix assessment (`AUD-14`)

Extend the existing `SpectralConditioningAssessment`/`assess_spectral_spd`
contract into one typed assessment for finite real symmetric matrices rather than
creating a competing policy. It records the symmetry residual, eigenvalues,
spectral scale, machine-scale uncertainty band, minimum eigenvalue, maximum
eigenvalue, reciprocal condition, configured reciprocal-condition threshold, and
a decision from `pass`, `inconclusive`, or `fail`.

The uncertainty band is internal and machine-scale:

```text
u = 64 * n * eps_float64 * max(1, max(abs(eigenvalues)))
```

- a symmetry residual above its corresponding machine-scale band is a definite
  failure, while an in-band nonzero residual is explicitly symmetrized and
  recorded;
- an eigenvalue below `-u` is a definite failure;
- an eigenvalue in `[-u, 0)` is inconclusive, not positive semidefinite;
- nonnegative eigenvalues satisfy the semidefinite sign requirement;
- strict positive-definite construction additionally requires a positive minimum
  eigenvalue and the declared reciprocal-condition threshold; and
- an inconclusive assessment cannot construct an authoritative Gaussian or
  fixed-ray object.

User `atol`/`rtol` do not widen symmetry or PSD/SPD type membership. They may still
define the already documented inconclusive band around the configured reciprocal-
condition decision after matrix membership is established. Exact rational
membership checks remain exact. Wave A supplies the shared assessment; Wave C
applies it to `FixedRaySystem` and its registered conditioning domain.

### A4. One Fisher quotient eigensystem (`AUD-15`)

Introduce an immutable `SpectralQuotientAssessment`. For symmetrized Fisher matrix
`F = V diag(lambda) V.T`, define

```text
s_F = max(abs(lambda))
cutoff = rcond * s_F
retained = lambda > cutoff
```

Before truncation, the matrix must pass A3's machine-scale symmetry and PSD
assessment. A negative eigenvalue below A3's uncertainty band fails, and an
in-band negative result is inconclusive and cannot construct a quotient. Fisher
`rcond` must satisfy `0 < rcond < 1`; it never licenses negative curvature. If
`s_F == 0`, rank is zero and the pseudoinverse and projector are zero. Rank,
nullity, retained condition number, pseudoinverse, range projector, and natural
gradient are all constructed from the same retained nonnegative eigensystem. No
later `np.linalg.pinv` call may choose a second mask.

The negative control `F=diag(1,-0.05), rcond=0.1` must fail before a quotient or
pseudoinverse is returned.

The existing information-point entry point and fields remain available. New code
consumes the assessment object; compatibility properties expose the former scalar
fields.

### A5. Scale-relative Fisher recovery (`AUD-16`)

Let `Delta = F_fine - F_coarse` and let `V_r, Lambda_r` be the retained fine
Fisher eigensystem. Before whitening, validate symmetry and PSD membership of
`F_fine`, `F_coarse`, and `Delta`, verify the decomposition residual, and enforce
the full Loewner relation `0 <= F_coarse <= F_fine`. Explicitly check the
fine-null/fine-range cross block and the fine-null block; information cannot appear
in a direction that the fine Fisher tensor declares null. Only then compute the
dimensionless loss operator

```text
L = Lambda_r^(-1/2) V_r.T Delta V_r Lambda_r^(-1/2)
```

and its symmetric eigenvalues `mu`. Values outside `[-rcond, 1 + rcond]` reject an
inconsistent decomposition. A retained direction satisfies the declared quotient
threshold when `mu <= rcond`; all retained directions must satisfy that condition
for `quotient_threshold_recovery=True`. This is not exact recovery. The separate
field `exact_pointwise_equality` is true only when an exact persisted witness or
exact-arithmetic oracle proves `Delta` is zero on the fine range and proves the
fine-null and cross blocks are zero. Without such a witness it is `None`, never
inferred from a tolerance. Fine-null directions are reported separately and are
never counted as recovered information.

The result adds fine information rank, fine nullity, relative-loss spectrum,
maximum relative loss, Loewner residuals, and null/cross-block residuals. It
separates exact equality from equality within the declared quotient threshold;
legacy fields are versioned compatibility views and may not call a thresholded
decision exact. The existing public entry point and explicit
`global_experiment_recovery_claimed=False` boundary remain. Pointwise Fisher
recovery does not imply a global Blackwell recovery kernel.

The negative controls `F_fine=diag(1,0), F_coarse=diag(1,1)` and a nonzero
retained/null cross block must reject before a recovery classification. A nonzero
loss below `rcond` must set `quotient_threshold_recovery=True` while leaving
`exact_pointwise_equality=False` when an exact witness disproves equality.

### A6. Fisher-cocycle provenance (`AUD-17`, late and separate inside Wave A)

The generic bilinear helper remains public for compatibility, but its status is
`bilinear_identity_only`; arbitrary matrix input can never populate a
Fisher-labeled metric.

The active finite experiment derives its current matrix from an exact persisted
statistical witness:

```text
probability = (1/8, 1/8, 1/4, 1/4, 1/8, 1/8)
scores = ((2,0), (-2,0), (0,2), (0,-2), (2,2), (-2,-2))
channel = constant output
```

The score is exactly centered, the coarse Fisher matrix is zero, and the fine
Fisher defect is exactly `((2,1),(1,3))`. The published record persists the law,
scores, channel, fine and coarse Fisher matrices, conditional covariance, and
exact residual. The active metric consumes the derived defect rather than a
parallel literal. A nonsymmetric or stale matrix remains a valid algebraic
negative control but cannot acquire Fisher provenance.

### Wave A compatibility and evidence

- Public measure/kernel constructors and `.masses`/`.matrix` access remain.
- Loose comparison tolerances remain parser-valid but lose authority over type
  membership.
- Existing exact fixtures should retain semantic values. Byte changes caused by
  canonicalization require an explicit artifact/schema update, never silent hash
  substitution.
- Mathematical identities use derivations or exact oracles; numerical agreement
  alone is not mathematics evidence.
- Producer experiment records remain `CANDIDATE`.
- No CUDA rerun is required. Current-revision CUDA claims remain `INCONCLUSIVE`;
  historical CUDA evidence remains unchanged but is stale for the new revision.

## Wave B: publication and runtime integrity

Wave B consumes Wave A's immutable-array boundary. It treats hashes as scientific
reproducibility records, not as a hostile-security mechanism.

### B1. Run manifest version 2 (`AUD-01` prerequisite)

Define `run-manifest-v2`. A complete manifest records, for every payload and
configuration file other than the manifest itself:

```text
(portable run-directory-relative artifact name, size_bytes, sha256)
```

The v2 schema is closed. Its artifact inventory is a canonically sorted list of
objects with exactly `name`, `kind`, `size_bytes`, and `sha256`. Names are safe
portable run-relative paths with no aliases, traversal, reserved names, or
case-fold collisions. The manifest also records schema version, run status,
artifact kind, config identity, a typed source-identity record, and the canonical
inventory order. Missing, unknown, extra, duplicate, or case-alias filesystem
entries reject the bundle. The completed manifest is written last and is not
recursively self-hashed.

Source identity may be typed `unavailable` for a purely operational bundle, with a
reason, but such a bundle is ineligible to close a source/config-bound scientific
claim.

`load_verified_run_bundle()` returns an immutable `VerifiedRunBundle`. It opens a
completed bundle, rejects unknown/missing or duplicate inventory entries, reads
each file once, computes size and SHA-256 from that exact byte buffer, and parses
JSON or numeric NPZ from the same buffer. It never verifies a path and reopens it
later. Consumers and caches receive immutable parsed payloads plus their verified
inventory, not mutable paths. A swap or mutation between verification and parse
therefore cannot introduce unverified bytes.

Legacy v1 bundles remain readable only through
`verify_legacy_v1_observed()`, which emits a separate observation with the closed
shape

```text
{schema_version, observed_at_revision,
 files:[{name,kind,size_bytes,sha256}], legacy_schema, limitations}
```

It may support historical compatibility/reproduction but may not claim v2
self-integrity or current scientific promotion, and it never rewrites the original
bundle. Every direct reader version-dispatches; no v2 consumer silently accepts a
legacy record.

### B2. Prepared publication and value validation (`AUD-04`, `AUD-05`, `AUD-11`)

Replace incremental `RunStore.create() -> write_*()` publication for v2 producers
with a two-phase interface:

```python
prepare_run_bundle(config, provenance, payloads) -> PreparedRunBundle
publish_run_bundle(prepared) -> RunStore
```

Preparation canonicalizes and validates the complete in-memory inventory with no
filesystem effects, including strict JSON encoding with `allow_nan=False`. The
returned `PreparedRunBundle` owns detached immutable serialized byte buffers for
the config, provenance, JSON payloads, and NPZ payload plus the complete inventory
computed from those exact buffers. It retains no caller mapping, array, callback,
source path, or lazy serializer. `publish_run_bundle` may write only those owned
buffers and may not reread or reserialize an original object. Publication writes a
new sibling staging directory, verifies the written bytes, emits the completed
manifest last, and installs the finished run.
An optional incomplete crash marker is distinct from the completed manifest and
can never be consumed as a complete run.

Before preparation can complete:

- `metric-record-v2` contains a structured comparator (`kind`, target or bound,
  direction, strictness, tolerance, and applicability reason). Status is not a
  caller-supplied initialization field; a factory derives it and the loader
  recomputes it from this frozen truth table:

  | kind | required fields | `pass` predicate |
  |---|---|---|
  | `within_absolute_tolerance` | target, inclusive | `abs(value-target) <= tolerance` |
  | `at_most` | upper bound, inclusive | `value <= bound+tolerance` |
  | `at_most` | upper bound, strict | `value < bound-tolerance` |
  | `at_least` | lower bound, inclusive | `value >= bound-tolerance` |
  | `at_least` | lower bound, strict | `value > bound+tolerance` |
  | `expected_positive_infinity` | no target/bound, inclusive, zero tolerance | `value == +inf` |

  An inapplicable assessment has no comparator result, records a nonempty reason,
  and yields the separate decision `inconclusive`; it never serializes a passing
  metric. For ordinary comparators, value,
  target/bound, and tolerance are real finite non-Booleans; tolerance is
  nonnegative; and kind, direction, and strictness are closed enums. Applicability
  reasons are nonempty. Only an explicit `expected_positive_infinity` comparator
  accepts positive infinity; no comparator accepts NaN or negative infinity, and
  extended values cannot pass through an ordinary numeric comparator. Inventory
  and migrate the shared `MetricRecord`, the separate record in
  `finite/experiment.py`, and `GaussianMetricRecord` in
  `realizations/gaussian/experiment.py`. Also migrate the public
  `PremiseAssessment` carrier and `assess_fixed_channel_premise` helper in
  `finite/agent_network.py`: both Boolean branches return
  `verification_state=CANDIDATE`, while `satisfied` and the typed applicability
  decision carry the calculation result;
- every returned or persisted producer record, metric or otherwise, has
  verification state `CANDIDATE`. A run/applicability
  assessment may be `pass`, `fail`, or `inconclusive`, but it is not a verification
  state. Promotion belongs exclusively to the external ledger; and
- `validate_npz_payload()` accepts only declared canonical numeric/bool dtypes,
  finite requirements appropriate to each array, unique safe names, and
  C-contiguous shapes. It rejects object, structured, datetime, Unicode, byte
  string, and pickle-dependent arrays before any file is created.

### B3. Immutable RNG provenance (`AUD-12`)

`RngStreams` stores spawn keys as immutable tuples and exposes them through a
read-only mapping or detached mapping copy. Provenance serialization is derived
from that immutable record and cannot diverge from already-created generators by
mutating a shared dictionary.

### B4. Canonical output-root resolution (`AUD-10`, prerequisite for `AUD-08`)

One shared resolver is used by every launcher, `RunStore`, discovery routine, and
figure publisher:

```python
resolve_output_root(root, *, anchor, repo_root, theory_root) -> Path
```

- relative roots resolve against the declared `anchor`, normally repository root,
  never ambient process CWD;
- the result is absolute, normalized, and symlink/reparse aware;
- overlap with a hashed source or Theory root is rejected;
- an in-repository output is allowed only as a declared exception when
  `git check-ignore` succeeds, `git ls-files` reports zero tracked paths beneath
  it, it is explicitly excluded from every source digest, and no symlink/reparse
  component redirects it into an input tree; and
- the resolved value, not the user's spelling, is the one carried through
  publication and discovery.

This preserves the checked-in ignored `artifacts/` default while preventing a run
from mutating the source identity it records.

### B5. Verified figure cache and transactional publication (`AUD-01`, `AUD-02`)

A figure-cache key binds:

1. the verified source manifest digest and complete artifact inventory;
2. the ordered figure request and renderer options;
3. the renderer source revision/schema; and
4. the expected output inventory.

Figure schema v2 uses content-addressed immutable generation directories plus a
small active-generation pointer. Rendering occurs in a new same-volume sibling
staging directory under an exclusive publisher lock. After every output is
generated, validated, and inventoried, staging is renamed to its immutable
generation ID. A temporary pointer file is then atomically replaced to select the
new generation. Readers verify the pointer and generation manifest before use.
The renderer never overwrites a generation file and never “rolls back” by deleting
preexisting output.

A crash before pointer replacement leaves the complete old generation active; a
crash afterward leaves the complete new generation active. An orphaned or former
generation is harmless. Wave B performs no generation reclamation: readers can
retain an old pointer without acquiring a lease, so deletion would race them.
Garbage collection is deferred until a future reader-lease/shared-lock or RCU
grace-period protocol has its own crash-recovery design and tests. Lock ownership,
stale-lock recovery, and startup journal recovery for publication are part of the
schema. This is an atomic pointer protocol, not an unsupported claim that a
nonempty directory replacement is portable.

Validation precedes destination creation. Byte-tamper, stale-cache, concurrent
publisher, injected mid-render failure, process termination at every rename/pointer
boundary, and recovery are mandatory controls. A reader must observe either one
complete old generation or one complete new generation, never a mix or loss.

## Wave C: Gaussian, CUDA, and experiment identity

Wave C consumes Wave A's matrix assessment and Wave B's canonical output root and
validated publication primitives.

### C1. Fixed-ray execution identity (`AUD-06`, `AUD-19`)

Introduce an immutable `FixedRayExecutionIdentity` produced by
`validate_fixed_ray_execution_identity(config, repo_root)`. It owns the canonical
validated `FixedRaySystem` instance; consumers do not rebuild that system from
parallel literals. It binds:

- exact experiment, fixture, preregistration, ordered schemes, and dimension;
- dimension `2` for the current frozen contract;
- finite symmetric positive-definite direction assessed under a required
  `MatrixDomainPolicy`, with `min_spd_rcond` as the conditioning limit;
- exact runtime system matrices and their canonical digest;
- dtype and scientific numerical policy;
- canonical output root and run namespace; and
- source/config/theory identities.

The record exposes two hashes. `scientific_system_digest` covers the validated
system, schemes, dimension, dtype, and scientific numerical policy and is invariant
under an output-root change. `execution_binding_digest` additionally covers the
complete run/config/source identity and canonical publication namespace. One run's
gate, job table, worker envelopes, and manifest share the execution binding;
equivalent-output-root determinism checks compare the scientific system digest and
semantic payloads.

The public `FixedRaySystem` constructor remains the construction entry point and
adds a required keyword-only `domain_policy: MatrixDomainPolicy`; there is no
unchecked public constructor or alternative raw factory. The preregistered builder
passes the frozen canonical policy explicitly. Direct construction
with `diag(inf,1)`, an asymmetric matrix, or reciprocal condition below
`min_spd_rcond` fails before an object is returned.

The identity validator runs before gate capture, gate-file creation, GPU inspection,
preflight, worker launch, staging directory creation, `RunStore.create()`, sentinel,
confirmatory execution, and CPU pilot publication. Unsupported dimensions,
nonfinite directions, excessive conditioning, or system/config digest drift fail
before effects.

Every gate, sentinel, job table, worker request/response, and final manifest carries
both named fields. `scientific_system_digest` must agree across semantically
equivalent runs even when their canonical output roots differ.
`execution_binding_digest` must agree within one publication namespace across the
config, gate, sentinel, job table, worker envelopes, and final manifest, and must
change when that namespace or any bound source/config identity changes. No entry
point reconstructs either digest from a subset of fields.

### C2. CUDA worker protocol version 2 (`AUD-07`)

Request and response records explicitly carry:

- requested and observed device index;
- requested and observed deterministic-algorithm state;
- requested and observed TF32 state;
- backend, dtype, environment, library, and worker-source identities; and
- both `scientific_system_digest` and `execution_binding_digest`.

The current scientific contract rejects anything except device `0`, deterministic
algorithms enabled, and TF32 disabled before worker launch, even though the fields
are transported so a future schema can intentionally support alternatives. The
worker independently confirms the observed settings and the controller rejects a
mismatch.

CPU fault-injection tests exercise protocol semantics without CUDA. A new CUDA
claim remains `INCONCLUSIVE` until a fresh exact-revision gate and sentinel are
explicitly authorized and completed.

### C3. Publication/discovery root parity (`AUD-08`)

Sentinel publication and confirmatory discovery both receive the canonical root
from Wave B and the execution identity from C1. Tests launch from repository root
and an unrelated working directory and require the same discoverable namespace.
No finder constructs `ROOT / OUTPUT["root"]` independently.

### C4. Scale-cocycle option reachability (`AUD-09`)

Until higher retained orders or a reduced publication schema are implemented,
`retained_interaction_order != 2` and `collect_diagnostics=False` are rejected
before RNG or output creation. The only accepted contract is order `2` with
`collect_diagnostics=True`, which publishes the existing exact nine-payload
inventory (`three_level_extension`, `composed_channels`, `coarse_actions`,
`posterior_bridges`, `comparison_isomorphisms`, `derivative_cocycle`,
`retained_projection_residual`, `metrics`, and `arrays`) plus config and manifest.
This deliberately closes the inert-toggle defect without inventing an ambiguous
reduced inventory.

Configuration identity includes only implemented behavior or an explicitly
rejected unsupported value. Mutation tests prove reachability for every accepted
field.

## Wave D: measurement before performance changes

Wave D never mixes correctness and performance changes.

### D0. Causal timing records (`AUD-21`, `AUD-22`)

Add revision-, configuration-, environment-, and machine-bound timing records.
For CUDA, partition at least:

- controller validation;
- preflight process startup;
- CUDA-library hashing;
- Python/Torch import and process startup;
- CUDA initialization;
- request serialization and response parsing;
- kernel launch and synchronization; and
- output validation/publication.

For the counterexample suite, partition catalog enumeration, exact minimization,
serialization, fixture construction, and assertions. Timings use repeated trials,
warm/cold labels, medians and dispersion, and preserve raw measurements. The prior
60.7-minute aggregate and `1.009e12` logical hash-byte estimate remain context, not
causal attribution or an SLA.

D0 closes only the measurement claims. It does not claim that a particular
optimization is warranted.

### D1. Conditional optimization

After D0, choose the smallest architecture supported by the measured dominant
cost:

1. If repeated process/hash overhead dominates, prefer one immutable worker
   request per outer paired job containing both schemes and all eight steps. This
   reduces 16 exchanges per job to one while matching the already frozen whole-job
   retry unit.
2. A cross-job persistent worker is considered only if paired-job batching is
   insufficient and a reviewed protocol preserves per-job identity, gate expiry,
   crash/restart, immutable responses, idempotent resume, and environment
   attestation.
3. Counterexample catalog caching is introduced only if D0 shows repeated catalog
   construction dominates. The cache contains one immutable pure catalog;
   mutation tests bypass or isolate it so monkeypatch controls cannot be masked.

Before implementation, the D0 report freezes an accepted performance budget and
decision rule. D1 must compare before/after on the same machine and equivalent
revision-derived configuration, reproduce identical numerical artifacts and
scientific decisions, and include injected crash, retry, gate-expiry, and resume
tests.

A full confirmatory CUDA rerun is not automatic. The minimum operational gate is a
fresh sentinel on the exact final source; any heavier run requires the user's
separate contemporaneous authorization and a free GPU.

## Wave E: manuscript correction in the Research repository (`AUD-20`)

Wave E uses a dedicated Research worktree and commit. It does not wait for code
waves and does not update the live dirty Research checkout.

The correction preserves Equations `coarse-tying-blocks` and
`rescaled-aggregation-flow`, the exact ELBO/gap/sufficiency algebra, and every
`OPEN`/`INCONCLUSIVE` status. It changes only the status-bearing prose at current
lines 178, 180, 182, and 194. The precise implication is:

- if every `S_l` respects the graph-component decomposition and the normalization
  is prescribed without coupling components, block-diagonal structure is
  preserved and the induced maps act componentwise;
- within a connected component, observations occur only along declared edges;
- connectedness alone implies neither existence of a limit, uniqueness of a fixed
  object modulo the residual global frame action, global attraction, nor
  membership in one basin; and
- a common limiting law follows only for a specified rescaled map on a common
  comparison space under separately stated existence, quotient-uniqueness,
  convergence, and basin hypotheses.

Consequently the manuscript cannot currently conclude that distinct effective
laws require disconnected components or that effective-law variation is
unobservable. Those sentences become conditional consequences of a future
one-attractor-per-component theorem. The existing statement that no rescaling,
attraction theorem, RG flow, or universality result has been established remains.

Line 178 changes “a fixed point ... which the population has arrived at” to a
candidate effective law that requires the declared normalized dynamics to reach
it. Line 182 makes running couplings testable only after a normalization and
trajectory are declared, and makes approach testable only after a fixed object and
convergence criterion are specified. Line 194 explicitly retains the missing
existence, uniqueness modulo gauge, convergence, and non-observability obligations.

Wave E checks neighboring paragraphs for the same implication, builds
`manuscripts/MAgent_exact_elbo_whitepaper.tex` with the repository's forced
LuaLaTeX/BibTeX procedure in a temporary output directory, requires zero undefined
references/citations and no new warnings, runs forbidden-old-string and required-
status scans, and receives an independent mathematical review. The counterexample
`F(x)=3x^2-2x^3` on one connected block remains a review control: its fixed points
are `0`, `1/2`, and `1`, with derivatives `0`, `3/2`, and `0`, so the two attracting
fixed points have basin-dependent limits. A second scalar control stays inside the
declared family: different gauge-invariant ratios `a/m` give inequivalent invariant
rays on the same connected support. Both controls are added as exact SymPy/pure-
algebra tests, not left as prose-only review examples.

From the Research root, the cache-free oracle command is:

```powershell
C:\Python314\python.exe -B -m pytest manuscripts\magent_elbo_whitepaper\verification\test_elbo_oracles.py -q -p no:cacheprovider --junitxml=docs\verification\evidence\wave-e\<implementation-short-head>\elbo-oracles.xml
```

The current XML is parsed for counts and must have zero failures/errors. Its exact
size, SHA-256, testcase-ID digest, and skip inventory enter the Wave E evidence
index.

The wiki is not silently changed. The preexisting stale uniqueness wording in
`wiki/concepts/Coarse Graining.md` is recorded as a later wiki-consistency item and
is not smuggled into Wave E. Any later ingest of the corrected manuscript or audit
disposition requires its own explicit vault publication step.

The Research base has an explicit publication-order gate. Fetch first. If the
fixed-ray ingest commit `c9f237d2` is not yet reachable from fetched `origin/main`,
Wave E uses a new worktree and branch whose declared unpublished parent is `c9f237d2`;
the ingest must publish before the manuscript child. The existing ingest worktree
is not reused, and the heavily dirty live Research review checkout is never
advanced or edited.

## Error and side-effect ordering

The following order is mandatory for every changed entry point:

1. Parse types and schema.
2. Validate mathematical membership and supported configuration.
3. Resolve and validate all source, output, and identity paths.
4. Verify every input artifact inventory and digest.
5. Construct immutable execution/configuration identity.
6. Only then create directories, write gate files, query the GPU, start workers,
   mutate caches, or publish outputs.
7. Write the complete manifest last.

Tests snapshot the destination and relevant source roots before every negative
control and require zero byte changes afterward. The old incremental RunStore API
is either deprecated for v2 scientific producers or explicitly labeled legacy;
it cannot satisfy, and may not advertise, this program-wide zero-effect promise.

## Schema and compatibility policy

- New scientific record shapes receive explicit new schema versions.
- Readers dispatch by schema version and reject unknown fields by default.
- Legacy records are not rewritten in place.
- Compatibility adapters are narrow, named, and cannot upgrade a legacy evidence
  state.
- Public Python signatures remain where doing so does not preserve the defect.
- If a formerly accepted value was mathematically invalid or scientifically inert,
  fail-closed rejection is the intended compatibility break.
- Package-root re-exports are updated only when a new public type is part of the
  documented contract.

## Verification and claim-state contract

Every implementation task follows this sequence:

1. Record a RED reproducer against the exact pre-fix revision.
2. Implement the smallest GREEN change.
3. Run targeted tests with cache disabled and machine-readable JUnit.
4. Run the affected subsystem suite.
5. Commit the implementation source/config bytes with no evidence placeholder.
6. At that clean implementation commit, run the candidate suite and commit its
   JUnit/probes/derivations/index in one durable evidence-only child. These records
   are history for the implementation parent, not exact-child closure.
7. At the evidence child, rerun targeted, affected-subsystem, and full CPU suites
   into a fresh nonignored, uncommitted closure directory named by the child SHA.
   Write a closure index and make no later source/config/evidence mutation.
8. Obtain independent code and domain review appropriate to the exact evidence
   child plus its closure bytes.
9. Start the verification control plane only after the closure set is complete.
   Its artifact digest binds `HEAD` plus those nonignored closure bytes. Populate a
   new external ledger at that exact artifact revision and validate it before merge.

Historical audit ledgers remain true for their recorded revisions and are preserved
as history. They are never rewritten as though the defect had not existed. For
each audit item, the final ledger contains at least two current-revision claims:

- the proposition "the audited defect still reproduces at the current revision":
  `REFUTED`, with current counterevidence; and
- the new regression guard and implementation contract pass at the exact final
  revision: `EVIDENCE_VERIFIED`.

Mathematical changes also require a derivation, exact oracle, or proof. Artifact
changes require byte-tamper and failure-injection evidence. Experiment claims
require reproduced outputs. JUnit totals and failure counts are parsed from XML,
never copied from a progress line.

Durable candidate evidence is committed under
`docs/verification/evidence/<wave>/<implementation-short-head>/`. Exact-child
closure evidence is written afterward under the nonignored, uncommitted path
`verification-evidence/<wave>/<evidence-child-short-head>/`. The latter is included
in the verification gate's worktree digest and is preserved without mutation; it
is not committed, avoiding an infinite evidence-commit recursion. A closed-schema
`remediation-evidence-v1` index contains:

```text
{schema_version, wave, evidence_stage, tested_git_head,
 implementation_parent_git_head,
 platform:{os,release,architecture,python_implementation},
 environment_record:{path,size_bytes,sha256},
 dependency_versions:[{name,version}],
 dependency_inputs:[{path,size_bytes,sha256}],
 tested_input_policy, tested_input_inventory_sha256,
 commands:[{id, argv, cwd_rel,
   interpreter:{path,version,sha256}, env_allowlist,
   started_utc, ended_utc, exit_code,
   junit:{path,size_bytes,sha256,tests,failures,errors,skipped,time_seconds,
          testcase_id_sha256,skipped_cases:[{id,reason}]}}],
 source_config_bindings:[{path,size_bytes,sha256}]}
```

Fields and list order are canonical and unknown fields reject. `evidence_stage` is
`candidate` or `closure`. In a candidate index, `tested_git_head` and
`implementation_parent_git_head` both equal the implementation commit `P`. In a
closure index, `tested_git_head` equals the evidence child `E`,
`implementation_parent_git_head` equals `P`, and the validator proves that `E` is
the direct evidence-only child of `P`. Swapped heads, nonancestry, or a non-evidence
path in `P..E` reject. The tested-input policy is versioned and defines an
exhaustive canonical source/config/Theory/tool inventory; its digest proves
completeness. The normalized environment record
captures installed NumPy/SciPy/pytest/plugin versions, platform, dependency and
lockfile hashes, plus relevant environment-variable values or explicit absence.
The durable candidate index names `P`; the closure index names `E` while retaining
the explicit parent `P`. Neither embeds the gate artifact revision. Raw closure
XML remains local. Any tracked/public evidence is deterministically scrubbed of
absolute user paths, hostnames, process identifiers, and private gate telemetry
without altering test IDs, counts, outcomes, or reasons; the privacy transform and
raw local hash are recorded. The external
ledger under `.verification/<wave>/final-ledger.json` binds the uncommitted closure
index and bytes to the captured artifact revision. No ignored `.verification/**`
file is the sole evidence for a closed mechanical claim. Each JUnit command uses
explicit `C:\Python314\python.exe`, records CUDA opt-in variables as absent/false,
exits zero, and has an exact skip allowlist; no new unexplained skip is accepted.
At closure, the Git index and tracked worktree are clean. The only permitted
nonignored untracked paths are the exact closure-evidence files inventoried by the
closure index and included in the verification gate's artifact digest.

Every persisted producer `verification_state` is exactly `CANDIDATE`.
`pass`/`fail`/`inconclusive` belongs to a separate typed numerical or applicability
assessment. `LLM_SUPPORTED`, `EVIDENCE_VERIFIED`, `REFUTED`, and `INCONCLUSIVE` as
verification states exist only in the external ledger. Missing current evidence,
a stale revision, or unresolved reviewer disagreement yields ledger
`INCONCLUSIVE`.

The resolution claims for `AUD-03`, `AUD-06`, and `AUD-20` retain severity `high`.
Each records the `high_severity` escalation trigger, uses escalation target 4 or 8,
includes the verification skill's required independent views, and has one
structured skeptic plus one adjudicator linked to current eligible evidence. Agent
agreement itself is never evidence.

After every merged wave, prior code-evidence ledgers become stale for the new
revision. The next wave starts a fresh ledger. A final aggregate ledger re-runs or
re-adjudicates every current claim with evidence whose `artifact_revision` equals
the new ledger revision; old ledgers remain historical records and are not carried
forward as current closure.

A CUDA sentinel may close only its exact sentinel protocol/parity claim. It cannot
close confirmatory execution, a full sweep, scientific attraction, or unrestricted
CPU/CUDA equivalence.

Every wave revision invalidates current CUDA binding even when CUDA code is
untouched. CUDA evidence additionally becomes stale after any change to source, configuration, Theory
bytes, worker/request-response schema, job table, execution identity,
gate/sentinel policy, dependencies, interpreter, CUDA runtime/driver/hardware,
device selection, determinism/TF32 settings, or the measured execution path.
No CUDA rerun is required for Waves A or B; their current CUDA claims remain
`INCONCLUSIVE`, while historical CUDA evidence remains unchanged but stale for the
new revision. Wave C necessarily changes execution identity/protocol; D0 invalidates prior performance
attribution if instrumentation changes the path; D1 invalidates operational and
performance evidence. Historical sentinel and confirmatory artifacts remain valid
only for their recorded revision. Operator acceptance proves authorization, not
execution.

## Per-wave evidence matrix

### Wave 0

- Static/schema tests prove all 22 unique audit IDs, exact owner mapping, complete
  constructor/reader/launcher/re-export/schema inventories, and the last-permitted-
  effect table.
- A SHA/size inventory pins every historical fixed-ray bundle without rewriting it.
- The schema/contract suite is Wave 0's affected subsystem; targeted, contract-
  subsystem, and full CPU JUnit close contract completeness only. No defect is yet
  claimed remediated.

### Wave A

- Targeted JUnit covers measures, VFE, information history, interactions,
  Gaussian matrix policies, and scale cocycle, followed by affected-subsystem and
  full CPU JUnit.
- Required negatives include totals `0` and `0.8`, a zero Markov row, exact
  canonical sums, immutable backing, KL support/infinity and tiny-versus-material
  negative boundaries, PSD pass/inconclusive/fail, a single Fisher mask,
  full-Loewner relative loss, the persisted Fisher witness, and a nonsymmetric
  non-Fisher control.
- Exact derivations/oracles accompany mathematics claims. High `AUD-03` receives
  the verification skill's high-severity escalation, skeptic, and adjudicator.

### Wave B

- Targeted JUnit covers artifacts, figures, metrics, runtime, launchers, every
  experiment reader/writer, and historical fixed-ray compatibility, followed by
  subsystem and full CPU JUnit.
- Faults cover unknown/missing/extra/duplicate/case-alias artifacts, size/hash
  tamper, verify-before-parse, prohibited NPZ/JSON forms before parent creation,
  producer-state boundaries, RNG mutation, root overlap/reparse/tracked/arbitrary-
  CWD behavior, exact legacy byte pins, cache invalidation, concurrency, and every
  render/generation/pointer failure boundary. A prepare-then-mutate control changes
  every original caller JSON mapping and NPZ array before publication and proves
  that the published bytes and inventory remain the detached prepared snapshot. A
  malformed-input control proves that even the staging parent remains absent.

### Wave C

- CPU-only targeted fault injection covers config, CUDA backend envelopes,
  fixed-ray construction, gate, sentinel, confirmatory, results, scale cocycle,
  and launchers, followed by subsystem and full CPU JUnit.
- Unsupported dimension and invalid/nonfinite/asymmetric/indefinite/overconditioned
  systems reject before gate, GPU query, RNG, subprocess, or directory creation.
- One execution-binding digest must match config, validated system record, CPU
  pilot, gate, sentinel, job table, request, response, and manifest. The scientific
  system digest remains identical across equivalent output roots. Unsupported worker settings and protocol
  mismatches reject. Arbitrary-CWD discovery is reproduced. Unsupported scale
  options reject with zero effects.
- CUDA operational state stays `INCONCLUSIVE` without a separately authorized
  exact-revision sentinel.

### Wave D0 and conditional D1

- D0 has fake-clock schema tests plus raw repeated timing records that separate all
  named CUDA and CPU components. It freezes a decision rule and budget and closes
  measurement only.
- CUDA timing remains `INCONCLUSIVE` without authorization.
- D1, if triggered, requires same-machine/config before-and-after records, exact
  semantic-output hashes, crash/retry/expiry/resume controls, and targeted,
  subsystem, and full CPU JUnit. A fresh sentinel is required only for a current
  sentinel operational claim; a 40-job equivalence/performance claim remains
  `INCONCLUSIVE` unless separately authorized and rerun.

### Wave E

- Research uses its own revision and ledger. Evidence includes the mathematical
  counterexamples, exact source diff, equation-byte comparison, neighboring-
  language scan, and root TeX build.
- Wave E is never included in the MultiAgentELBO aggregate ledger.

## Integration and WIP safety

- Every wave starts from freshly fetched `origin/main` in its own branch/worktree.
- A wave owns an explicit path list; parallel agents do not edit shared files.
- Integration is serial in dependency order and uses fast-forward-only or reviewed
  non-force merges.
- Before advancing a dirty live checkout, record its modified/untracked paths and
  prove the incoming commit has no overlap. Never stash, reset, clean, or discard.
- Research and MultiAgentELBO use different branches, worktrees, remotes, ledgers,
  and commits.
- Only the exact verified evidence-child SHA may fast-forward `main`. A merge,
  rebase, cherry-pick, or post-verification source/evidence change requires a new
  artifact revision, re-adjudication, and ledger.
- CUDA work begins only after a current GPU-availability check and user approval of
  the exact prescribed run.

## Acceptance criteria

The program is complete only when:

1. all 22 audit IDs have one owning wave, one disposition, current tests, and a
   final ledger state;
2. invalid probability, matrix, Fisher, metric, NPZ, output-root, and execution-
   identity inputs fail before effects;
3. every finalized v2 bundle authenticates its own complete payload inventory and
   every figure cache binds the verified source bytes;
4. fixed-ray CPU, gate, sentinel, confirmatory, and worker paths consume one exact
   system identity;
5. accepted configuration fields either change their declared behavior or are
   rejected as unsupported;
6. performance changes, if any, follow a preserved causal profile and reproduce
   identical scientific outputs;
7. the manuscript no longer derives a unique limiting fixed point from
   connectedness;
8. every MultiAgentELBO code wave (0, A, B, C, D0, and conditional D1) has
   zero-failure targeted, subsystem, and full CPU JUnit at its exact final
   revision; Wave E instead has zero-failure exact Research oracle JUnit, a clean
   root TeX build, required/forbidden language scans, equation-byte comparison,
   and a validated Research-revision mathematics ledger;
9. every final ledger validates and every producer state remains within the
   declared boundary;
10. any CUDA status is honestly `INCONCLUSIVE` unless current eligible evidence
    closes that exact scoped claim; a fresh authorized sentinel can close only its
    sentinel protocol/parity claim, never confirmatory, full-sweep, or general
    equivalence; and
11. remote publication and live-checkout fast-forward preserve all preexisting WIP
    bytes.

## Implementation-plan split

This design produces separate detailed plans rather than one mega-plan:

1. Wave 0 and Wave A mathematical invariants;
2. Wave B publication/runtime integrity;
3. Wave C experiment/CUDA identity;
4. Wave D0 measurement and a later conditional D1 plan; and
5. Wave E manuscript correction in Research.

Wave A and Wave E may be implemented in parallel after their plans pass review.
Waves B and C remain serial. D1 is not written as an implementation commitment
until D0 supplies causal evidence and freezes the decision rule.
