# Post-fixed-ray deep audit

Date: 2026-08-11
Code-under-audit baseline revision: `aedc6621a4e4f1c725a54f8b287aac425ef833d8`
Baseline artifact revision: `git:aedc6621a4e4f1c725a54f8b287aac425ef833d8:sha256:f06ee8c7735b7b274d06f24e04bfbbd008bc74dfe317b80a103db780f5532a6f`
Scope: MultiAgentELBO source, tests, and experiment/publication paths; Research wiki context at commit `c9f237d2ca54c274ba5760012e62823a69d203a3`; and the current coarse-graining manuscript bytes identified below
Execution policy: CPU-only; no CUDA job or GPU process was started

The exact report-inclusive closure revision is recorded in the ignored control-plane files `.verification/active.json` and `.verification/ledger.json` only after this document is committed. It is intentionally not embedded here: adding that value to this tracked file would create a new commit and invalidate the value recursively. Final handoff therefore reports the external ledger, JUnit, probe, and adjudication hashes alongside this durable baseline report.

## Executive assessment

The completed fixed-model attraction diagnosis remains valid. None of the findings below invalidates its hash-bound source extract, the exact support-boundary certificate, the 40-job primary/holdout separation, or the conclusion that the frozen `-0.02` endpoint criterion is structurally unreachable while mathematical attraction and universality remain open.

The broader audit retained 22 defects: 3 high, 15 medium, and 4 low. Four additional investigator candidates were examined and dropped rather than entered as closure claims. The highest-priority work is to restore invariant-preserving probability construction, bind all CUDA fixed-ray configuration fields to the system actually executed, and correct a manuscript sentence that currently derives convergence to a common fixed point from connectedness alone.

At the code-under-audit baseline, the full CPU suite command was `C:\Python314\python.exe -B -m pytest -p no:cacheprovider --basetemp=.verification\deep-audit-runtime\full2-tmp --junitxml=.verification\deep-audit-runtime\full2-aedc662.xml`; it exited zero with 957 tests, 0 failures, 0 errors, and 3 skips in 163.428 seconds. The baseline JUnit XML SHA-256 is `206674472AA412102A25FB425ACC0B255663DD33E2AF9F3BCBE21ED02F09797C`. The skips are the two Windows symlink restrictions and the explicitly opt-in CUDA lane. The baseline revision-bound mechanical probe is `.verification/deep-audit-runtime/audit-core-probes.json`; after adding the explicit loose-tolerance ELBO control, its SHA-256 is `E7C69F37D4B4406761AA1A9EBD89D31D37124C8053EFFC64DFF6C547066F9722`, and its source script SHA-256 is `7F5B0357B6F6F43709313695C89697815CEAB756CE909395BEE060744B7FA446`.

## Review method

The audit used separate code-quality, debugging, implementation/configuration, numerical-analysis, information-geometry, differential-geometry, gauge-theory, variational-inference, transformer, performance, and independent-adjudication views. High-severity candidates received adversarial skeptic/defender review. Claude Opus 5 also reviewed selected claims at xhigh effort. Two attempts to obtain an independent Fable 5 performance/severity review ended in connection refusal and contributed no eligible evidence. Agent agreement was never treated as closure; retained claims were closed by current source traces, reproduced outputs, mathematical counterexamples, or the machine-readable JUnit record.

All 22 retained claims were recorded as `EVIDENCE_VERIFIED` in `.verification/ledger.json` for the baseline artifact revision. The validation command is `C:\Python314\python.exe C:\Users\chris and christine\.claude\skills\verification\scripts\verification_gate.py validate --cwd . .verification\ledger.json`; it exited zero at the baseline. After this report is committed, the same command is run against a newly bound report-inclusive ledger, whose exact hash and result belong to the external handoff described above rather than to this self-referential tracked document. `EVIDENCE_VERIFIED` verifies that each stated defect exists; it does not promote any scientific theorem or experiment hypothesis.

## High findings

### AUD-03 — Structural tolerances can destroy probability and ELBO invariants

Locations: `src/multiagent_elbo/config.py:240-241`, `src/multiagent_elbo/finite/measures.py:64-71`, `src/multiagent_elbo/finite/measures.py:88-103`, `src/multiagent_elbo/finite/vfe.py:35-63`

`atol` and `rtol` accept any positive finite value and are then used as structural membership tolerances for probability masses and Markov rows. With parser-valid loose tolerances, a zero-total measure and zero-row kernel are accepted. A second probe with mass `(0.4, 0.4)` produced total mass `0.8`, KL/free energy `-0.17851484105136778`, and ELBO `0.17851484105136778` above log evidence zero.

This is silent invalidation of the core probability, KL, VFE, and ELBO types. Checked-in launchers use tight tolerances and exact normalized fixtures, so current published results are unaffected. Skeptics therefore argued for medium or low severity; the binding high rating reflects that an admitted public configuration can silently violate central mathematical invariants.

Required correction: separate structural normalization policy from numerical comparison tolerances. Reject invalid mass/row totals or normalize under a fixed machine-scale policy, then guarantee all constructible probability objects satisfy their declared invariants. Add negative controls at loose tolerances and stable nonnegative KL handling for residual roundoff.

### AUD-06 — CUDA fixed-ray execution can mislabel a hard-coded 2x2 system

Locations: `src/multiagent_elbo/config.py:498`, `src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py:1583`, `src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py:2448`

The configuration accepts any positive `matrix_dimension`. The CPU pilot rejects values other than two, but the CUDA sentinel and confirmatory entry points omit that guard and construct the frozen 2x2 system unconditionally. The editable launcher passes the configured theory record into these authorized publication paths, so a non-2 value can be recorded in configuration/provenance while a 2x2 system is actually executed.

The shipped default and all current evidence use dimension two. One skeptic therefore rated this medium; the binding high rating reflects silent scientific configuration/output mismatch in a gated publication path.

Required correction: introduce one shared fixed-ray identity validator, execute it before gate creation, sentinel publication, confirmatory publication, and CPU pilot publication, and add fail-before-write regression tests for every unsupported dimension.

### AUD-20 — Connectedness is incorrectly promoted to convergence to one fixed point

Location: Research commit `c9f237d2ca54c274ba5760012e62823a69d203a3`, current manuscript `manuscripts/magent_elbo_whitepaper/08a_coarse_graining.tex:172-194`, especially line 180; file SHA-256 `E08DEADCE851B890B260787379956C794E3AA8764F124146043164C7F3EABA38`

The manuscript correctly states that attraction and basin coverage are unproved, but then says connected coupled agents “reach the same fixed point.” Connectedness alone establishes neither convergence nor uniqueness of an attractor. In the adversarial review, the skeptic argued for medium severity because the surrounding section repeatedly disclaims an actual RG theorem. The defender gave the one-block map `F(x)=3x^2-2x^3` on `[0,1]`, which has two attracting fixed points with basin-dependent limits, and showed that the false inference is used to rule out observable effective-law variation. The binding high rating is limited to that participatory/RG conclusion and does not implicate the exact-ELBO or aggregation algebra.

Required correction: make the common-fixed-point conclusion conditional on a specified dynamics plus existence, uniqueness, and convergence/basin hypotheses. Preserve the present `OPEN`/`INCONCLUSIVE` attraction and RG-flow boundary. This is a manuscript correction, not evidence that the finite calculations are wrong.

## Medium findings

### AUD-01 — Generic manifests do not bind bytes, and figure cache reuse can be stale

Locations: `src/multiagent_elbo/artifacts.py:93-132`, `src/multiagent_elbo/figures.py:184-189`

Finalized generic manifests list artifact names and completion status but no per-file digest. The figure cache accepts a completed figure manifest before reloading or hashing the numerical bundle. After mutating metrics, the probe still returned the cached figure bundle as complete. Add canonical hashes/sizes to the generic manifest and bind every figure manifest to the complete numerical artifact inventory and renderer revision. The fixed-model diagnostic’s separate tracked source-to-output binding remains intact.

### AUD-02 — Partial figure replacement can delete preexisting output

Locations: `src/multiagent_elbo/figures.py:212-219`, `src/multiagent_elbo/figures.py:253-257`

If an early final image is overwritten and a later replacement fails, rollback deletes the overwritten path instead of restoring its previous bytes. The probe lost an existing PNG while an existing PDF survived. Publish through a temporary directory and atomically replace the complete set, or preserve and restore backups on every failure path.

### AUD-04 — Metric records permit incoherent or nonfinite scientific status

Locations: `src/multiagent_elbo/experiment_support.py:61-134`

Direct `MetricRecord` construction accepts invalid status/scope strings. Helper constructors accept nonfinite values and invalid tolerances, including a nonfinite passing comparison. No built-in producer failure was demonstrated. Enforce enumerated states/scopes, finite values and tolerances, nonnegative tolerances, and internally derived pass/fail decisions.

### AUD-07 — CUDA device and determinism configuration are ignored

Locations: `src/multiagent_elbo/config.py:562-567`, `src/multiagent_elbo/cuda_backend.py:519-604`, `tools/cuda_worker.py:378-385`

`device_index` and `deterministic` are accepted and hashed but never enter the worker request. The worker hard-codes `cuda:0` and deterministic algorithms enabled. Frozen defaults match. Either carry and verify these fields throughout the protocol, or reject every nonimplemented value before any gate or output is created.

### AUD-08 — Sentinel publication and discovery disagree outside the repository CWD

Locations: `src/multiagent_elbo/artifacts.py:48-57`, `run_gaussian_fixed_ray_lab.py:142-168`

Relative `OUTPUT.root` publication resolves against process CWD, whereas sentinel discovery searches under repository `ROOT`. A supported arbitrary-CWD launch can publish a valid sentinel that the confirmatory launcher cannot find. Resolve the output root once to an absolute canonical path and pass the same value to both publication and discovery.

### AUD-09 — Scale-cocycle options change identity but not behavior

Location: `src/multiagent_elbo/finite/scale_cocycle_experiment.py:298-734`

`retained_interaction_order` and `collect_diagnostics` enter configuration identity, but the experiment always computes the fixed order-2 projection and emits the same diagnostics. The probe found different configuration hashes with identical metrics and arrays. Implement the options or reject unsupported values; do not serialize scientifically inert toggles.

### AUD-10 — Output roots may invalidate the provenance they claim

Locations: `src/multiagent_elbo/config.py:257-280`, `src/multiagent_elbo/runtime.py:66-99`

Output may be placed inside a source or Theory tree that is hashed before run creation. Publication then changes the hashed tree, making the manifest’s source identity stale immediately. Reject output roots that overlap any hashed input root, with resolved-path and symlink-aware tests.

### AUD-11 — `RunStore` can finalize NPZ files its own readers reject

Locations: `src/multiagent_elbo/artifacts.py:86-90`, `src/multiagent_elbo/artifacts.py:307-311`, `src/multiagent_elbo/figures.py:419-426`

Object-dtype arrays can be written and finalized, but production readers use `allow_pickle=False`, making the completed bundle unreadable. Reject object, structured-object, and noncanonical dtypes before creating the NPZ or manifest.

### AUD-13 — Read-only finite-measure arrays can be made writable again

Location: `src/multiagent_elbo/finite/measures.py:23-30`

The arrays own their storage and merely have `WRITEABLE` cleared; callers can re-enable it and install negative or unnormalized mass after validation. Store public arrays over immutable bytes-backed buffers or return defensive copies without exposing authoritative mutable state.

### AUD-14 — Norm-scaled PSD tolerance admits materially negative modes

Location: `src/multiagent_elbo/realizations/gaussian/interactions.py:45-52`

The PSD check scales tolerance by the largest matrix norm. A matrix with eigenvalues approximately `[-1e-5, 1e6]` was accepted and produced an assembled Laplacian with negative minimum eigenvalue near `-2e-5`. Frozen fixtures were not affected. Use a declared absolute/relative semidefinite policy with an explicit inconclusive band or project only when the projection is part of the contract.

### AUD-15 — Fisher rank metadata and pseudoinverse use different cutoffs

Locations: `src/multiagent_elbo/finite/information_history.py:80-83`, `src/multiagent_elbo/finite/information_history.py:137-138`

Rank diagnostics use `rcond * max(1, lambda_max)` while `np.linalg.pinv` uses `rcond * lambda_max`. The recorded three-state probe reported rank one while the projector retained rank two. A separate scaled binary construction likewise demonstrates that the retained solve and reported quotient can disagree. Compute one eigendecomposition and use one cutoff mask for rank, projector, pseudoinverse, condition number, and natural gradient.

### AUD-16 — Fisher recovery uses a scale-dependent absolute floor

Location: `src/multiagent_elbo/finite/information_history.py:266-282`

A channel that loses all Fisher information at scale `1e-12` was assigned `pointwise_full_fisher_equality=True` because the defect was compared with `atol + rtol * max(1, norm)`, although the separate global experiment flag remained false. Use a Fisher-whitened generalized spectrum or another declared relative, coordinate-aware criterion, with fine-null directions treated separately.

### AUD-17 — The “Fisher cocycle” check proves only a bilinear identity

Locations: `src/multiagent_elbo/finite/scale_cocycle.py:438-454`, `src/multiagent_elbo/finite/scale_cocycle_experiment.py:318-322`

The active hard-coded literal is symmetric positive definite, but the three residual forms agree algebraically for any matrix. A nonsymmetric replacement passed exactly because the API does not validate the claimed tensor class, and no persisted derivation binds the active literal to a statistical model/channel as a Fisher defect. Derive and persist the defect from an admissible family and channel, validate symmetry/PSD/provenance, and retain an arbitrary-bilinear negative control. Otherwise rename the metric as an algebraic bilinear-cocycle check.

### AUD-19 — `FixedRaySystem` accepts nonfinite and out-of-contract conditioning

Location: `src/multiagent_elbo/realizations/gaussian/fixed_ray.py:56-60`

The public constructor accepts `diag(inf, 1)` and a condition number of `1e13`, despite the registered scientific conditioning domain. The infinite direction produces nonfinite coupling/residual outputs. Require finite entries, finite eigenvalues, strict SPD membership, and the declared condition bound at construction. The preregistered frozen system is safe.

### AUD-21 — CUDA confirmatory execution repeats expensive process and hash work

Locations: `src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py:748-819`, `src/multiagent_elbo/cuda_backend.py:519-604`, `tools/cuda_worker.py:89-143`

The 40-job confirmatory path makes 640 serial one-row exchanges. Each launches preflight and worker processes and repeatedly hashes the CUDA libraries. The preserved execution took 3,644.331 seconds; the architecture presents approximately `1.009e12` logical bytes to hashing. This is not a physical-I/O estimate, and the aggregate timer does not isolate hashing from Python/Torch startup, CUDA initialization, serialization, or kernels. The path is opt-in and resumable, so the binding rating is medium rather than high.

Before optimization, profile those components separately. A persistent worker/session is acceptable only if it preserves exact gate identity, immutable request/response evidence, per-job retry semantics, environment attestation, and crash-resume behavior.

## Low findings

### AUD-05 — A public helper can promote caller-supplied premises

Location: `src/multiagent_elbo/finite/agent_network.py:672-684`

A caller-supplied boolean can yield `EVIDENCE_VERIFIED`. The active experiment overrides the producer state to `CANDIDATE`, so current results are safe. Make producer helpers emit candidate evidence records only; reserve promotion for the external ledger.

### AUD-12 — RNG provenance exposes mutable spawn-key state

Location: `src/multiagent_elbo/runtime.py:39-63`

The frozen `RngStreams` object exposes a mutable dictionary. A caller can change recorded provenance without changing the already-created generators. Store immutable tuples/mappings and return detached provenance values.

### AUD-18 — Direct floating KL can be slightly negative

Location: `src/multiagent_elbo/finite/vfe.py:35-42`

For otherwise normalized laws, cancellation produced KL `-5.15e-17`. Use a numerically stable summation and a documented machine-scale clamp only after structural validity is established. The larger negative KL case belongs to AUD-03 and must not be hidden by clamping.

### AUD-22 — Counterexample-associated tests dominate current CPU suite time

Location: machine-readable JUnit `.verification/deep-audit-runtime/full2-aedc662.xml`

The 45 counterexample-associated JUnit cases consumed 83.839 of the suite’s 163.428 seconds, or 51.3 percent. This is a timing observation, not a causal profile: the present evidence does not partition repeated catalog construction from the assertions and surrounding fixture work. Profile those cases before deciding whether to cache the exact catalog or split invariant construction from per-test assertions. No correctness or accepted performance budget is implicated.

## Investigator candidates dropped before ledger closure

These were source-reviewed triage candidates, not separate `REFUTED` claims in the final ledger:

- **Gate expiry is unchecked — dropped.** Both sentinel and confirmatory paths check expiry before and during execution in `fixed_ray_experiment.py`.
- **The experiment registry is mutable or order-unstable — dropped.** Ordered completeness checks and `MappingProxyType` protect the registered surface, with passing coverage.
- **A no-Git environment falsely claims verified source completeness — dropped.** Runtime provenance records missing Git fields honestly; manifest completion describes artifact inventory, not scientific verification.
- **No pure CPU/controller path exists — dropped.** Pure analysis/controller paths are present, CUDA is isolated in subprocess workers, and the ordinary pilot leaves CUDA claims inconclusive rather than inferring them.

## Preserved scientific boundaries

The audit does not change these conclusions:

1. The exact fixed-domain endpoint certificate is `ESTABLISHED` only under its enumerated finite-system, basin, completeness, uncensoring, raw-angle, scale-window, and paired-maximum premises.
2. The 40-job diagnostic/confirmatory classification remains `NUMERICAL / CANDIDATE / APPLICATION_SPECIFIC` at the producer boundary; the external ledger verifies integrity and frozen-rule classification, not attraction.
3. Fixed-model practical attraction remains `INCONCLUSIVE`; the frozen endpoint support criterion is refuted as reachable on the admitted basin, not the mathematical attraction conjecture itself.
4. Unrestricted attraction, continuum limits, RG flow, universality, and physical-time interpretations remain `OPEN` or `INCONCLUSIVE`.
5. CUDA parity evidence remains revision- and configuration-bound. No new CUDA evidence was produced in this audit.

## Recommended remediation order

1. Restore mathematical type invariants: probability/Markov normalization, stable KL, shared Fisher quotient cutoff, scale-relative Fisher recovery, and Fisher-defect provenance.
2. Harden publication semantics: content-hashed manifests/cache, numeric-only NPZ, immutable evidence objects, validated metrics, transactional figure output, and nonoverlapping output roots.
3. Freeze experiment identity: shared fixed-ray dimension/domain checks, implemented-or-rejected CUDA controls, one canonical output root, and implemented-or-rejected scale-cocycle toggles.
4. Correct the manuscript connectedness claim while preserving the open attraction/RG boundary.
5. Profile and redesign the CUDA exchange architecture without weakening gate, retry, provenance, or resume guarantees; then remove duplicated exact-catalog test work.

Every remediation should begin with a failing regression, preserve producer `CANDIDATE` status, and revalidate the exact final revision with machine-readable CPU results. CUDA should be rerun only when a change actually affects the CUDA protocol or worker and the operator has explicitly made the GPU available for that run.
