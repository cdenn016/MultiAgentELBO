# Scientific Integrity Remediation Wave 0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Freeze a complete, machine-readable migration and evidence contract for all 22 audit findings before any remediation production code changes.

**Architecture:** Five versioned records own audit disposition, public-interface migration, status/failure ordering, historical fixed-ray bytes, and the exact installed verification control-plane snapshot. A small standalone evidence-index validator establishes the exact candidate/closure schema used by every later wave; contract tests reject omissions, duplicate ownership, ambiguous producer states, stale head relationships, unreviewed closure bytes, and bundle drift.

**Tech Stack:** Python 3.14 standard library, JSON, pathlib, hashlib, XML parsing, pytest, JUnit XML, Git, the installed verification control plane.

## Global Constraints

- Require committed design revision `c43a7c50675cf63b60f7b6cbea9664b638cd4c4e` as an ancestor of Wave 0 in an isolated `codex/` worktree; fetch and verify `origin/main` before branching.
- Preserve the user's Desktop checkout, modified launchers, untracked review directory, and `uv.lock` byte-for-byte.
- Use American English in code, tests, comments, commits, and documents.
- Use `C:\Python314\python.exe`; keep CUDA opt-in variables absent/false and do not query or run the GPU.
- Wave 0 changes contracts, validators, tests, and documentation only. It does not claim any audit defect remediated.
- Every persisted producer `verification_state` is exactly `CANDIDATE`; pass/fail/inconclusive calculations use a separate assessment field.
- Historical bundles are hash-inventoried, never rewritten, relabeled, or upgraded to manifest v2.
- Negative controls must fail before modifying output, source, cache, gate, or evidence directories.
- Use cache-disabled pytest with a worktree-local `--basetemp` and parse totals only from fresh JUnit XML.
- Candidate and closure evidence follow the two-commit exact-head protocol in the approved design; no evidence from a different Git head closes a current claim.

---

## File Responsibility Map

- Create `docs/verification/remediation/audit-disposition-v1.json`: exactly one owner, reproducer, guard, and evidence class for `AUD-01` through `AUD-22`.
- Create `docs/verification/remediation/compatibility-inventory-v1.json`: every public constructor, schema, reader, launcher field, helper carrier, and package export touched by Waves A-D.
- Create `docs/verification/remediation/status-failure-contract-v1.json`: status namespaces and last-permitted-effect ordering for public entry points.
- Create `docs/verification/remediation/historical-fixed-ray-bundles-v1.json`: exact SHA-256/size inventory of the tracked 10-file confirmatory and 9-file diagnostic extracts.
- Create `docs/verification/remediation/verification-contract-v1.json`: exact nine-file snapshot of the canonical installed verification skill under `.codex/skills/verification`.
- Create `docs/verification/remediation/remediation-evidence-v1.schema.json`: closed candidate/closure evidence-index schema.
- Create `docs/verification/remediation/README.md`: human-readable migration and evidence rules.
- Create `tools/remediation_evidence.py`: strict index construction/validation and deterministic JUnit/tested-input/environment inventory helpers.
- Create `tools/build_wave0_evidence.py`: executable Wave 0 prepare/publish and external-ledger population wrapper over the generic builder.
- Create `tests/test_remediation_contracts.py`: closed-schema, ownership, interface, status, failure-order, and historical-byte tests.
- Create `tests/test_remediation_evidence.py`: candidate/closure head, environment, tested-input, JUnit, and unknown-field controls.
- Modify `tests/test_artifacts.py` and `tests/test_experiment_support.py`: replace OS exception text in skip reasons with the fixed strings `capability unavailable: hard_link` and `capability unavailable: symbolic_link`.

### Task 1: Freeze the 22-item audit disposition

**Files:**
- Create: `docs/verification/remediation/audit-disposition-v1.json`
- Create: `tests/test_remediation_contracts.py`

**Interfaces:**
- Produces a closed JSON object with top-level fields `schema_version`, `program_design_revision`, `audit_baseline_revision`, and `items`.
- Each item has exactly `audit_id`, `severity`, `owning_wave`, `source_locations`, `public_interfaces`, `red_reproducer`, `green_guard`, `evidence_class`, `initial_disposition`, and `final_status`.
- `initial_disposition` is always `EVIDENCE_VERIFIED_AT_AUDIT_BASELINE`; it records historical defect existence and is not a current remediation state.
- `final_status` is always `INCONCLUSIVE_PENDING_OWNER_WAVE`; Wave 0 freezes ownership but does not refute or remediate any defect.

- [ ] **Step 1: Write the missing-file and exact-owner RED tests**

```python
EXPECTED_OWNERS = {
    "AUD-01": "B", "AUD-02": "B", "AUD-03": "A", "AUD-04": "B",
    "AUD-05": "B", "AUD-06": "C", "AUD-07": "C", "AUD-08": "C",
    "AUD-09": "C", "AUD-10": "B", "AUD-11": "B", "AUD-12": "B",
    "AUD-13": "A", "AUD-14": "A", "AUD-15": "A", "AUD-16": "A",
    "AUD-17": "A", "AUD-18": "A", "AUD-19": "C", "AUD-20": "E",
    "AUD-21": "D", "AUD-22": "D",
}


def test_audit_disposition_is_complete_closed_and_uniquely_owned():
    payload = _load_json(AUDIT_DISPOSITION_PATH)
    assert set(payload) == {
        "schema_version", "program_design_revision", "audit_baseline_revision", "items"
    }
    assert payload["schema_version"] == "scientific-remediation-audit-disposition-v1"
    records = {item["audit_id"]: item for item in payload["items"]}
    assert set(records) == set(EXPECTED_OWNERS)
    assert len(records) == len(payload["items"]) == 22
    for audit_id, wave in EXPECTED_OWNERS.items():
        assert records[audit_id]["owning_wave"] == wave
        assert records[audit_id]["initial_disposition"] == "EVIDENCE_VERIFIED_AT_AUDIT_BASELINE"
        assert records[audit_id]["final_status"] == "INCONCLUSIVE_PENDING_OWNER_WAVE"
        assert set(records[audit_id]) == {
            "audit_id", "severity", "owning_wave", "source_locations",
            "public_interfaces", "red_reproducer", "green_guard",
            "evidence_class", "initial_disposition", "final_status",
        }
        assert records[audit_id]["source_locations"]
        assert records[audit_id]["public_interfaces"]
        assert records[audit_id]["red_reproducer"]
        assert records[audit_id]["green_guard"]
```

- [ ] **Step 2: Run the focused RED**

Run:

```powershell
C:\Python314\python.exe -B -m pytest tests\test_remediation_contracts.py -k audit_disposition -q -p no:cacheprovider --basetemp=.pytest-wave0-task1-red
```

Expected: FAIL because `audit-disposition-v1.json` does not exist.

- [ ] **Step 3: Write the literal 22-record disposition**

Create the top level with `schema_version="scientific-remediation-audit-disposition-v1"`, `program_design_revision="c43a7c50675cf63b60f7b6cbea9664b638cd4c4e"`, and `audit_baseline_revision="aedc6621a4e4f1c725a54f8b287aac425ef833d8"`. The `items` array is exactly the following, in audit-ID order; do not synthesize or abbreviate any record:

```json
[
  {"audit_id":"AUD-01","severity":"medium","owning_wave":"B","source_locations":["src/multiagent_elbo/artifacts.py:93-132","src/multiagent_elbo/figures.py:184-189"],"public_interfaces":["RunStore.finalize","load_run_bundle","render_run"],"red_reproducer":"Finalize a v1 run, render it, mutate metrics.json, and prove the completed figure cache is still reused.","green_guard":"run-manifest-v2 hashes every owned byte and figure-cache-identity-v2 binds the verified run inventory plus renderer revision.","evidence_class":"mechanical_counterexample_plus_regression","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-02","severity":"medium","owning_wave":"B","source_locations":["src/multiagent_elbo/figures.py:212-219","src/multiagent_elbo/figures.py:253-257"],"public_interfaces":["render_run","publish_figure_generation"],"red_reproducer":"Replace one existing PNG, fail a later figure replacement, and observe rollback delete the preexisting PNG.","green_guard":"Publish an immutable complete figure generation behind a recoverable journal and atomically replace only active-generation.json.","evidence_class":"mechanical_counterexample_plus_regression","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-03","severity":"high","owning_wave":"A","source_locations":["src/multiagent_elbo/config.py:240-241","src/multiagent_elbo/finite/measures.py:64-71","src/multiagent_elbo/finite/measures.py:88-103","src/multiagent_elbo/finite/vfe.py:35-63"],"public_interfaces":["ProbabilityMeasure","MarkovKernel","FiniteMeasure","kl_divergence","variational_free_energy"],"red_reproducer":"Construct mass (0.4,0.4) and a zero Markov row under loose configured tolerances; observe total 0.8 and negative KL/free energy.","green_guard":"One machine-scale structural canonicalizer enforces finite nonnegative normalized probability and Markov membership while FiniteMeasure remains intentionally unnormalized.","evidence_class":"mathematical_derivation_plus_mechanical_counterexample","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-04","severity":"medium","owning_wave":"B","source_locations":["src/multiagent_elbo/experiment_support.py:61-134"],"public_interfaces":["MetricRecord","target_metric","lower_bounded_metric","upper_bounded_metric","inapplicable_metric"],"red_reproducer":"Directly construct invalid state/scope strings and pass NaN values or negative/nonfinite tolerances through metric helpers.","green_guard":"metric-record-v2 uses closed enums, finite operands and nonnegative tolerances, derives assessment_decision internally, and persists verification_state exactly CANDIDATE.","evidence_class":"mechanical_counterexample_plus_regression","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-05","severity":"low","owning_wave":"B","source_locations":["src/multiagent_elbo/finite/agent_network.py:672-684"],"public_interfaces":["PremiseAssessment","assess_fixed_channel_premise"],"red_reproducer":"Pass caller-supplied True to the public premise helper and observe producer state EVIDENCE_VERIFIED.","green_guard":"Producer helpers return CANDIDATE evidence plus a separate applicability decision; only an external ledger may promote a claim.","evidence_class":"mechanical_counterexample_plus_regression","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-06","severity":"high","owning_wave":"C","source_locations":["src/multiagent_elbo/config.py:498","src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py:1583","src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py:2448"],"public_interfaces":["FixedRayExecutionIdentity","validate_fixed_ray_execution_identity","run_fixed_ray_experiment","run_cuda_sentinel","publish_confirmatory_experiment"],"red_reproducer":"Select matrix_dimension=3 in each pilot, sentinel, gate, and confirmatory mode and observe a recorded 3x3 configuration reach the hard-coded 2x2 system path.","green_guard":"Every fixed-ray entry point consumes one validated 2x2 execution identity before gate, directory, subprocess, RNG, or GPU effects.","evidence_class":"source_reachability_plus_cpu_fault_injection","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-07","severity":"medium","owning_wave":"C","source_locations":["src/multiagent_elbo/config.py:562-567","src/multiagent_elbo/cuda_backend.py:519-604","tools/cuda_worker.py:378-385"],"public_interfaces":["ComputeConfig.device_index","ComputeConfig.deterministic","ComputeConfig.allow_tf32","WorkerProtocolManifest","WorkerJobResult","run_worker_job"],"red_reproducer":"Choose nondefault device_index or deterministic settings and prove the request omits them while the worker hard-codes cuda:0 and deterministic algorithms.","green_guard":"worker-protocol-v2 transports, validates, echoes, and binds device/determinism/TF32 fields, or rejects unsupported values before effects.","evidence_class":"mechanical_counterexample_plus_regression","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-08","severity":"medium","owning_wave":"C","source_locations":["src/multiagent_elbo/artifacts.py:48-57","run_gaussian_fixed_ray_lab.py:142-168"],"public_interfaces":["resolve_output_root","run_cuda_sentinel","discover_cuda_sentinel","publish_confirmatory_experiment"],"red_reproducer":"Launch from an external CWD with a relative output root, publish a sentinel, and prove confirmatory discovery searches a different repository-relative path.","green_guard":"One canonical resolved output root is validated once and carried in execution identity through publication and discovery.","evidence_class":"mechanical_counterexample_plus_regression","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-09","severity":"medium","owning_wave":"C","source_locations":["src/multiagent_elbo/finite/scale_cocycle_experiment.py:298-734"],"public_interfaces":["retained_interaction_order","collect_diagnostics","run_scale_cocycle_experiment"],"red_reproducer":"Change retained_interaction_order or collect_diagnostics, observe a new configuration hash, and reproduce byte-identical metrics and arrays.","green_guard":"Only retained_interaction_order=2 and collect_diagnostics=True are admitted until a behavioral implementation exists; all other values fail before output.","evidence_class":"mechanical_counterexample_plus_regression","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-10","severity":"medium","owning_wave":"B","source_locations":["src/multiagent_elbo/config.py:257-280","src/multiagent_elbo/runtime.py:66-99"],"public_interfaces":["OutputConfig.root","resolve_output_root","collect_provenance","prepare_run_bundle"],"red_reproducer":"Place output inside a hashed source or Theory root and show publication immediately changes the provenance digest it claims.","green_guard":"The canonical root resolver rejects resolved, symlink, reparse, junction, or alias overlap with every hashed input root before publication.","evidence_class":"mechanical_counterexample_plus_regression","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-11","severity":"medium","owning_wave":"B","source_locations":["src/multiagent_elbo/artifacts.py:86-90","src/multiagent_elbo/artifacts.py:307-311","src/multiagent_elbo/figures.py:419-426"],"public_interfaces":["RunStore.write_npz","prepare_run_bundle","load_run_bundle","render_run"],"red_reproducer":"Finalize an object-dtype or structured-object NPZ and prove the production allow_pickle=False reader cannot reopen the completed run.","green_guard":"Preparation rejects object-bearing and noncanonical dtypes before serialization or path creation; readers hash and parse the same immutable bytes.","evidence_class":"mechanical_counterexample_plus_regression","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-12","severity":"low","owning_wave":"B","source_locations":["src/multiagent_elbo/runtime.py:39-63"],"public_interfaces":["RngStreams.spawn_keys","RngStreams.provenance"],"red_reproducer":"Mutate the exposed spawn-key dictionary after generator creation and observe recorded provenance change independently of the streams.","green_guard":"RNG spawn keys are immutable ordered tuples and every provenance accessor returns detached immutable data.","evidence_class":"mechanical_counterexample_plus_regression","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-13","severity":"medium","owning_wave":"A","source_locations":["src/multiagent_elbo/finite/measures.py:23-30"],"public_interfaces":["ProbabilityMeasure.mass","FiniteMeasure.mass","MarkovKernel.matrix","InformationPoint.probability"],"red_reproducer":"Re-enable WRITEABLE on an owning validated NumPy array and install negative or unnormalized authoritative state.","green_guard":"Every public authoritative numerical array is backed by immutable bytes or returned as a defensive copy with no mutation path to internal state.","evidence_class":"mechanical_counterexample_plus_regression","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-14","severity":"medium","owning_wave":"A","source_locations":["src/multiagent_elbo/realizations/gaussian/interactions.py:45-52"],"public_interfaces":["MatrixDomainPolicy","SpectralConditioningAssessment","assess_spectral_psd","assemble_precision"],"red_reproducer":"Pass diag(-1e-5,1e6) through the norm-scaled PSD check and observe an accepted assembled Laplacian with a negative mode.","green_guard":"One explicit absolute/relative spectral policy returns pass, fail, or inconclusive and all PSD consumers use it.","evidence_class":"spectral_oracle_plus_mechanical_counterexample","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-15","severity":"medium","owning_wave":"A","source_locations":["src/multiagent_elbo/finite/information_history.py:80-83","src/multiagent_elbo/finite/information_history.py:137-138"],"public_interfaces":["SpectralQuotientAssessment","assess_spectral_quotient","information_history_diagnostics"],"red_reproducer":"Use the three-state and scaled-binary fixtures to obtain reported rank one while np.linalg.pinv retains rank two.","green_guard":"One assessed eigensystem and cutoff mask owns rank, nullity, pseudoinverse, projector, condition number, and natural gradient.","evidence_class":"spectral_oracle_plus_mechanical_counterexample","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-16","severity":"medium","owning_wave":"A","source_locations":["src/multiagent_elbo/finite/information_history.py:266-282"],"public_interfaces":["RecoveryDiagnostics","recovery_diagnostics"],"red_reproducer":"Scale a total-information-loss channel to 1e-12 and observe pointwise_full_fisher_equality=True under the absolute floor.","green_guard":"fisher-recovery-v2 separates exact equality from quotient-threshold recovery using a relative Loewner/whitened spectrum with null directions explicit.","evidence_class":"quotient_derivation_plus_mechanical_counterexample","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-17","severity":"medium","owning_wave":"A","source_locations":["src/multiagent_elbo/finite/scale_cocycle.py:438-454","src/multiagent_elbo/finite/scale_cocycle_experiment.py:318-322"],"public_interfaces":["ExactFisherChannelWitness","fisher_cocycle_diagnostics","run_scale_cocycle_experiment"],"red_reproducer":"Replace the claimed Fisher tensor with a nonsymmetric bilinear form and observe all three algebraic residuals pass exactly.","green_guard":"Persist an exact statistical-family/channel Fisher witness, validate symmetry/PSD/provenance, and retain the arbitrary-bilinear negative control.","evidence_class":"exact_statistical_witness_plus_mechanical_counterexample","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-18","severity":"low","owning_wave":"A","source_locations":["src/multiagent_elbo/finite/vfe.py:35-42"],"public_interfaces":["kl_divergence","variational_free_energy"],"red_reproducer":"Use normalized near-equal laws that produce direct-sum KL=-5.15e-17 through cancellation.","green_guard":"A stable reducer clamps only a derived machine-scale negative roundoff band after structural probability validity and rejects material negativity.","evidence_class":"roundoff_bound_plus_mechanical_counterexample","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-19","severity":"medium","owning_wave":"C","source_locations":["src/multiagent_elbo/realizations/gaussian/fixed_ray.py:56-60"],"public_interfaces":["MatrixDomainPolicy","FixedRaySystem","build_preregistered_system"],"red_reproducer":"Construct FixedRaySystem with diag(inf,1) or condition number 1e13 and observe nonfinite coupling/residual output.","green_guard":"The public constructor requires Wave A's matrix policy and rejects nonfinite, non-SPD, or out-of-contract conditioning with no unchecked factory.","evidence_class":"mechanical_counterexample_plus_regression","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-20","severity":"high","owning_wave":"E","source_locations":["Research@c9f237d2ca54c274ba5760012e62823a69d203a3:manuscripts/magent_elbo_whitepaper/08a_coarse_graining.tex:172-194"],"public_interfaces":["coarse-graining manuscript connectedness claim"],"red_reproducer":"Apply F(x)=3x^2-2x^3 on [0,1] to a connected one-block system and exhibit two attracting fixed points with basin-dependent limits.","green_guard":"State common-fixed-point convergence only conditionally on specified dynamics, existence, uniqueness, and convergence/basin hypotheses while retaining OPEN/INCONCLUSIVE boundaries.","evidence_class":"mathematical_counterexample_plus_manuscript_build","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-21","severity":"medium","owning_wave":"D","source_locations":["src/multiagent_elbo/realizations/gaussian/fixed_ray_experiment.py:748-819","src/multiagent_elbo/cuda_backend.py:519-604","tools/cuda_worker.py:89-143"],"public_interfaces":["TimingObservation","run_remediation_performance_profile","run_worker_job","publish_confirmatory_experiment"],"red_reproducer":"Measure the 40-job/640-exchange path and retain raw spans showing repeated process startup and library hashing without assigning causality from aggregate wall time.","green_guard":"D0 partitions controller, preflight, hashing, startup, initialization, serialization, kernel, and publication spans; D1 batching is permitted only if the preregistered budget fails.","evidence_class":"revision_bound_causal_timing","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"},
  {"audit_id":"AUD-22","severity":"low","owning_wave":"D","source_locations":[".verification/deep-audit-runtime/full2-aedc662.xml"],"public_interfaces":["TimingObservation","run_remediation_performance_profile","build_counterexample_catalog"],"red_reproducer":"Reproduce machine-readable per-test timings and partition catalog construction from assertions instead of treating 83.839/163.428 seconds as causal attribution.","green_guard":"D0 publishes repeated raw component spans and a frozen decision rule; D1 cache/splitting occurs only when the accepted budget fails.","evidence_class":"revision_bound_causal_timing","initial_disposition":"EVIDENCE_VERIFIED_AT_AUDIT_BASELINE","final_status":"INCONCLUSIVE_PENDING_OWNER_WAVE"}
]
```

- [ ] **Step 4: Run the focused GREEN**

Run the Step 2 command.

Expected: PASS with exactly one owner and nonempty evidence fields for every audit ID.

- [ ] **Step 5: Commit the disposition contract**

```powershell
git add -- docs/verification/remediation/audit-disposition-v1.json tests/test_remediation_contracts.py
git commit -m "test: freeze remediation audit ownership"
```

### Task 2: Freeze public compatibility, status, and failure ordering

**Files:**
- Create: `docs/verification/remediation/compatibility-inventory-v1.json`
- Create: `docs/verification/remediation/status-failure-contract-v1.json`
- Modify: `tests/test_remediation_contracts.py`

**Interfaces:**
- Compatibility entries have exactly `surface_id`, `kind`, `legacy_symbol_or_field`, `module_or_schema`, `owning_wave`, `migration`, `compatibility`, and `package_exports`.
- Status entries define separate closed namespaces for `theorem_status`, producer `verification_state`, numerical `assessment_decision`, run `status`, external ledger state, and historical state.
- Migration entries have exactly `schema`, `owning_wave`, `reader_behavior`, `writer_behavior`, `rewrite_behavior`, and `promotion_behavior`.
- Failure-order entries have exactly `entry_point`, `owning_wave`, `validation_order`, `last_permitted_effect`, and `negative_controls`.

- [ ] **Step 1: Add RED tests for all required interface families and status separation**

```python
REQUIRED_SURFACE_IDS = {
    "a-probability-measure", "a-finite-measure", "a-markov-kernel",
    "a-kl-divergence", "a-information-point", "a-recovery-diagnostics",
    "a-recovery-function",
    "a-matrix-domain-policy", "a-conditioning-assessment",
    "a-quotient-assessment", "a-fisher-channel-witness", "a-assemble-precision",
    "a-assess-spectral-psd", "a-assess-spectral-spd",
    "a-assess-spectral-quotient", "a-assess-symmetric-matrix",
    "a-assess-information-recovery", "a-exact-fisher-witness-factory",
    "b-metric-record", "b-finite-metric-alias", "b-gaussian-metric-alias",
    "b-metric-comparator", "b-load-metric-record",
    "b-premise-assessment", "b-premise-helper", "b-rng-streams",
    "b-output-root", "b-prepared-run-bundle", "b-run-store",
    "b-npz-array-input", "b-run-payloads", "b-prepared-artifact",
    "b-verified-run-bundle", "b-legacy-observed-bundle",
    "b-prepare-run", "b-publish-run", "b-load-run", "b-render-run",
    "b-load-verified-run", "b-verify-legacy-run", "b-figure-cache-identity",
    "b-run-manifest-v1", "b-run-manifest-v2", "b-legacy-observation",
    "b-figure-generation", "b-figure-pointer", "b-figure-journal",
    "b-launch-finite", "b-launch-network", "b-launch-attention",
    "b-launch-categorical", "b-launch-counterexample", "b-launch-information",
    "b-launch-scale", "b-launch-theory", "b-launch-holonomy",
    "b-launch-gaussian", "b-launch-fixed-diagnostic", "b-launch-fixed-ray",
    "b-launch-figures", "c-fixed-ray-system", "c-preregistered-system",
    "c-execution-identity", "c-device-index", "c-deterministic",
    "c-allow-tf32", "c-worker-manifest", "c-worker-result",
    "c-worker-runtime-binding-v3", "c-worker-request-v3", "c-worker-response-v3",
    "c-legacy-worker-observation", "c-sentinel", "c-confirmatory", "c-fixed-run",
    "c-frozen-matrix-policy", "c-identity-validator", "c-run-manifest-v3",
    "c-prepare-fixed-run", "c-load-fixed-run", "c-legacy-fixed-observation",
    "c-fixed-schema-idle-gate", "c-fixed-schema-confirmatory-gate",
    "c-fixed-schema-sentinel", "c-fixed-schema-worker-exchange-index",
    "c-fixed-schema-confirmatory-job", "c-fixed-schema-primary-execution",
    "c-fixed-schema-holdout-execution", "c-fixed-schema-confirmatory-execution",
    "c-fixed-schema-confirmatory-endpoints", "c-fixed-schema-job-table",
    "c-fixed-schema-pilot-endpoints",
    "c-retained-order", "c-collect-diagnostics", "d-timing-observation",
    "d-clock", "d-perf-counter-clock", "d-timing-span",
    "d-cpu-profile", "d-worker-timing",
}


def test_compatibility_inventory_names_every_frozen_surface():
    payload = _load_json(COMPATIBILITY_PATH)
    assert payload["schema_version"] == "scientific-remediation-compatibility-v1"
    surfaces = {item["surface_id"] for item in payload["surfaces"]}
    assert surfaces == REQUIRED_SURFACE_IDS
    assert len(payload["surfaces"]) == len(REQUIRED_SURFACE_IDS) == 100
    assert all(set(item) == {
        "surface_id", "kind", "legacy_symbol_or_field", "module_or_schema",
        "owning_wave", "migration", "compatibility", "package_exports",
    } for item in payload["surfaces"])
    assert {item["migration"] for item in payload["surfaces"]} == EXPECTED_MIGRATIONS
    assert all(item["migration"] in EXPECTED_MIGRATIONS for item in payload["surfaces"])
    assert all(item["module_or_schema"] and "|" not in item["module_or_schema"]
               for item in payload["surfaces"])


def test_producer_and_ledger_states_are_disjoint():
    payload = _load_json(STATUS_FAILURE_PATH)
    assert payload["states"]["producer_verification_state"] == ["CANDIDATE"]
    assert payload["states"]["assessment_decision"] == ["fail", "inconclusive", "pass"]
    assert payload["states"]["external_ledger_state"] == [
        "CANDIDATE", "LLM_SUPPORTED", "EVIDENCE_VERIFIED", "REFUTED", "INCONCLUSIVE"
    ]
    assert payload["states"]["historical_state"] == [
        "EVIDENCE_VERIFIED_AT_RECORDED_REVISION", "STALE_FOR_CURRENT_REVISION"
    ]
    assert "EVIDENCE_VERIFIED" not in payload["states"]["producer_verification_state"]
```

- [ ] **Step 2: Add RED tests for last-permitted-effect coverage**

Require entries for these exact operations:

```python
REQUIRED_EFFECT_ENTRY_POINTS = {
    "ProbabilityMeasure.__init__", "FiniteMeasure.__init__", "MarkovKernel.__init__",
    "InformationPoint.__init__", "ExperimentConfig.from_dicts", "MetricRecord.__init__",
    "metric_factories", "RngStreams.create", "assemble_precision",
    "recovery_diagnostics", "FixedRaySystem.__init__",
    "validate_fixed_ray_execution_identity", "resolve_output_root",
    "prepare_run_bundle", "publish_run_bundle", "load_run_bundle", "render_run",
    "run_finite_experiment", "run_multiagent_network_experiment",
    "run_attention_experiment", "run_categorical_dqm_experiment",
    "run_counterexample_experiment", "run_information_history_experiment",
    "run_scale_cocycle_experiment", "run_theory_oracle_experiment",
    "run_gauge_holonomy_experiment", "run_gaussian_experiment",
    "run_gaussian_fixed_ray_diagnostic", "run_fixed_ray_experiment",
    "run_cuda_sentinel", "publish_confirmatory_experiment", "run_worker_job",
    "run_remediation_performance_profile",
}
```

Assert exact equality with this set, exact entry-field closure, nonempty ordered validation steps and controls, and unique `entry_point` values. The literal last-effect values are frozen in Step 6 rather than inferred by the test.

- [ ] **Step 3: Run the combined RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_remediation_contracts.py -k "compatibility or states or effect" -q -p no:cacheprovider --basetemp=.pytest-wave0-task2-red
```

Expected: FAIL because both records are missing.

- [ ] **Step 4: Create the two closed records**

For every compatibility surface, record one of these exact migration values. This
is the complete enum derived from the normative 100-row table; tests require exact
set equality, exactly 100 unique IDs, and at least one populated row for every
enum member:

```text
preserve_signature_stricter_invariant
candidate_only_producer
canonical_root_resolution
factory_only_status_derivation
immutable_generation_publication
immutable_snapshot_semantics
new_measurement_surface
new_public_assessment
new_schema_version_legacy_read_only
new_strict_public_path
required_keyword_domain_policy
required_execution_identity
strict_version_dispatch
transport_and_validate_previously_inert_field
reject_previously_accepted_unsupported_value
```

```python
EXPECTED_MIGRATIONS = {
    "candidate_only_producer",
    "canonical_root_resolution",
    "factory_only_status_derivation",
    "immutable_generation_publication",
    "immutable_snapshot_semantics",
    "new_measurement_surface",
    "new_public_assessment",
    "new_schema_version_legacy_read_only",
    "new_strict_public_path",
    "preserve_signature_stricter_invariant",
    "reject_previously_accepted_unsupported_value",
    "required_execution_identity",
    "required_keyword_domain_policy",
    "strict_version_dispatch",
    "transport_and_validate_previously_inert_field",
}
```

Record package-root re-exports explicitly as an ordered list, including an empty list when the symbol is intentionally module-private. In the status contract, require all serialized producer records—not only metrics—to use `CANDIDATE`, and require historical states to carry their recorded Git/artifact revision.

- [ ] **Step 5: Defer the combined GREEN and commit until after the normative payloads**

Do not run the following commands here. First implement every normative table
row and cross-wave ownership assertion below; execute this block only at the
explicit post-table instruction after the final failure-order row:

```powershell
git add -- docs/verification/remediation/compatibility-inventory-v1.json docs/verification/remediation/status-failure-contract-v1.json tests/test_remediation_contracts.py
git commit -m "docs: freeze remediation compatibility contracts"
```

#### Normative Task 2 payloads (supersedes the generic Step 4 prose)

The implementation writes one compatibility JSON object per row below, sorted by `surface_id`. The columns map one-to-one to the eight closed fields. `package_exports=[]` is an affirmative module-private decision. The required-ID test and table contain the same 100 unique records; tests reject omissions and additions.

| surface_id | kind | legacy_symbol_or_field | module_or_schema | wave | migration | compatibility | package_exports |
|---|---|---|---|---|---|---|---|
| `a-assemble-precision` | `public_function` | `assemble_precision` | `multiagent_elbo.realizations.gaussian.interactions` | `A` | `preserve_signature_stricter_invariant` | `valid_SPD_fixtures_preserved_invalid_or_inconclusive_rejected` | `[]` |
| `a-assess-information-recovery` | `public_function` | `assess_information_recovery` | `multiagent_elbo.finite.information_history` | `A` | `new_public_assessment` | `shared_v2_recovery_assessment_no_legacy_promotion` | `["multiagent_elbo.finite.assess_information_recovery"]` |
| `a-assess-spectral-psd` | `public_function` | `assess_spectral_psd` | `multiagent_elbo.conditioning` | `A` | `new_public_assessment` | `sole_public_PSD_policy_entry_point` | `["multiagent_elbo.assess_spectral_psd"]` |
| `a-assess-spectral-quotient` | `public_function` | `assess_spectral_quotient` | `multiagent_elbo.conditioning` | `A` | `new_public_assessment` | `sole_public_quotient_eigensystem_entry_point` | `["multiagent_elbo.assess_spectral_quotient"]` |
| `a-assess-spectral-spd` | `public_function` | `assess_spectral_spd` | `multiagent_elbo.conditioning` | `A` | `new_public_assessment` | `sole_public_SPD_policy_entry_point` | `["multiagent_elbo.assess_spectral_spd"]` |
| `a-assess-symmetric-matrix` | `public_function` | `assess_symmetric_matrix` | `multiagent_elbo.conditioning` | `A` | `new_public_assessment` | `sole_public_symmetry_policy_entry_point` | `["multiagent_elbo.assess_symmetric_matrix"]` |
| `a-conditioning-assessment` | `public_constructor` | `SpectralConditioningAssessment` | `multiagent_elbo.conditioning` | `A` | `new_public_assessment` | `new_immutable_assessment_no_legacy_relabel` | `["multiagent_elbo.SpectralConditioningAssessment"]` |
| `a-exact-fisher-witness-factory` | `public_function` | `exact_fisher_channel_witness` | `multiagent_elbo.finite.fisher` | `A` | `new_public_assessment` | `constructs_exact_channel_bound_witness_without_self_promotion` | `["multiagent_elbo.finite.exact_fisher_channel_witness"]` |
| `a-finite-measure` | `public_constructor` | `FiniteMeasure` | `multiagent_elbo.finite.measures` | `A` | `preserve_signature_stricter_invariant` | `unnormalized_but_finite_nonnegative_detached_immutable` | `["multiagent_elbo.finite.FiniteMeasure"]` |
| `a-fisher-channel-witness` | `public_constructor` | `ExactFisherChannelWitness` | `multiagent_elbo.finite.fisher` | `A` | `new_public_assessment` | `channel_bound_exact_Fisher_witness_owned_only_by_fisher_module` | `["multiagent_elbo.finite.ExactFisherChannelWitness"]` |
| `a-information-point` | `public_constructor` | `InformationPoint` | `multiagent_elbo.finite.information_history` | `A` | `preserve_signature_stricter_invariant` | `valid_probabilities_preserved_invalid_rejected_and_detached` | `["multiagent_elbo.finite.InformationPoint"]` |
| `a-kl-divergence` | `public_function` | `kl_divergence` | `multiagent_elbo.finite.vfe` | `A` | `preserve_signature_stricter_invariant` | `signature_and_support_semantics_preserved_machine_roundoff_only_clamped` | `["multiagent_elbo.finite.kl_divergence"]` |
| `a-markov-kernel` | `public_constructor` | `MarkovKernel` | `multiagent_elbo.finite.measures` | `A` | `preserve_signature_stricter_invariant` | `valid_rows_preserved_zero_or_nonnormalized_rows_rejected` | `["multiagent_elbo.finite.MarkovKernel"]` |
| `a-matrix-domain-policy` | `public_constructor` | `MatrixDomainPolicy` | `multiagent_elbo.conditioning` | `A` | `new_public_assessment` | `new_required_policy_no_unchecked_public_matrix_path` | `["multiagent_elbo.MatrixDomainPolicy","multiagent_elbo.realizations.gaussian.MatrixDomainPolicy"]` |
| `a-probability-measure` | `public_constructor` | `ProbabilityMeasure` | `multiagent_elbo.finite.measures` | `A` | `preserve_signature_stricter_invariant` | `valid_input_preserved_comparison_tolerance_no_longer_structural` | `["multiagent_elbo.finite.ProbabilityMeasure"]` |
| `a-quotient-assessment` | `public_constructor` | `SpectralQuotientAssessment` | `multiagent_elbo.conditioning` | `A` | `new_public_assessment` | `one_immutable_eigensystem_scalar_legacy_fields_are_views` | `["multiagent_elbo.SpectralQuotientAssessment"]` |
| `a-recovery-diagnostics` | `public_constructor_and_schema` | `RecoveryDiagnostics` | `fisher-recovery-v2` | `A` | `new_schema_version_legacy_read_only` | `v1_observed_only_v2_separates_exact_and_threshold_claims` | `["multiagent_elbo.finite.RecoveryDiagnostics"]` |
| `a-recovery-function` | `public_function` | `recovery_diagnostics` | `multiagent_elbo.finite.information_history` | `A` | `preserve_signature_stricter_invariant` | `signature_retained_shared_quotient_and_relative_Loewner_policy` | `["multiagent_elbo.finite.recovery_diagnostics"]` |
| `b-figure-cache-identity` | `public_constructor_and_schema` | `FigureCacheIdentity` | `figure-cache-identity-v2` | `B` | `new_strict_public_path` | `binds_verified_run_inventory_renderer_revision_and_options` | `[]` |
| `b-figure-generation` | `serialized_schema` | `figure-generation-manifest-v2` | `multiagent_elbo.figure_store` | `B` | `new_schema_version_legacy_read_only` | `legacy_observed_new_writes_content_addressed` | `[]` |
| `b-figure-journal` | `serialized_schema` | `figure-publication-journal-v2` | `multiagent_elbo.figure_store` | `B` | `new_schema_version_legacy_read_only` | `new_recovery_journal_no_legacy_rewrite` | `[]` |
| `b-figure-pointer` | `serialized_schema` | `active-generation-v2` | `multiagent_elbo.figure_store` | `B` | `new_schema_version_legacy_read_only` | `atomic_pointer_never_standalone_scientific_evidence` | `[]` |
| `b-finite-metric-alias` | `public_constructor_alias` | `FiniteExperimentMetricRecord` | `multiagent_elbo.finite.experiment` | `B` | `factory_only_status_derivation` | `import_retained_as_shared_v2_alias_no_caller_status` | `[]` |
| `b-gaussian-metric-alias` | `public_constructor_alias` | `GaussianMetricRecord` | `multiagent_elbo.realizations.gaussian.experiment` | `B` | `factory_only_status_derivation` | `import_retained_as_shared_v2_alias_no_caller_status` | `[]` |
| `b-launch-attention` | `launcher_dictionary` | `run_attention_lab.OUTPUT[root]` | `run_attention_lab.py` | `B` | `canonical_root_resolution` | `editable_value_resolved_once_against_repository_root` | `[]` |
| `b-launch-categorical` | `launcher_dictionary` | `run_categorical_dqm_lab.OUTPUT[root]` | `run_categorical_dqm_lab.py` | `B` | `canonical_root_resolution` | `editable_value_resolved_once_against_repository_root` | `[]` |
| `b-launch-counterexample` | `launcher_dictionary` | `run_finite_counterexample_lab.OUTPUT[root]` | `run_finite_counterexample_lab.py` | `B` | `canonical_root_resolution` | `editable_value_resolved_once_against_repository_root` | `[]` |
| `b-launch-figures` | `launcher_dictionary_and_reader` | `make_figures.OUTPUT[root]` | `make_figures.py` | `B` | `canonical_root_resolution` | `same_root_resolver_and_strict_or_legacy_dispatch` | `[]` |
| `b-launch-finite` | `launcher_dictionary` | `run_finite_lab.OUTPUT[root]` | `run_finite_lab.py` | `B` | `canonical_root_resolution` | `editable_value_resolved_once_against_repository_root` | `[]` |
| `b-launch-fixed-diagnostic` | `launcher_dictionary_and_reader` | `run_gaussian_fixed_ray_diagnostic.OUTPUT[root]` | `run_gaussian_fixed_ray_diagnostic.py` | `B` | `canonical_root_resolution` | `historical_diagnostic_uses_read_only_legacy_adapter` | `[]` |
| `b-launch-fixed-ray` | `launcher_dictionary_and_reader` | `run_gaussian_fixed_ray_lab.OUTPUT[root]` | `run_gaussian_fixed_ray_lab.py` | `B` | `canonical_root_resolution` | `publication_and_discovery_share_resolved_root` | `[]` |
| `b-launch-gaussian` | `launcher_dictionary` | `run_gaussian_lab.OUTPUT[root]` | `run_gaussian_lab.py` | `B` | `canonical_root_resolution` | `editable_value_resolved_once_against_repository_root` | `[]` |
| `b-launch-holonomy` | `launcher_dictionary` | `run_gauge_holonomy_lab.OUTPUT[root]` | `run_gauge_holonomy_lab.py` | `B` | `canonical_root_resolution` | `editable_value_resolved_once_against_repository_root` | `[]` |
| `b-launch-information` | `launcher_dictionary` | `run_information_history_lab.OUTPUT[root]` | `run_information_history_lab.py` | `B` | `canonical_root_resolution` | `editable_value_resolved_once_against_repository_root` | `[]` |
| `b-launch-network` | `launcher_dictionary` | `run_multiagent_network_lab.OUTPUT[root]` | `run_multiagent_network_lab.py` | `B` | `canonical_root_resolution` | `editable_value_resolved_once_against_repository_root` | `[]` |
| `b-launch-scale` | `launcher_dictionary` | `run_scale_cocycle_lab.OUTPUT[root]` | `run_scale_cocycle_lab.py` | `B` | `canonical_root_resolution` | `editable_value_resolved_once_against_repository_root` | `[]` |
| `b-launch-theory` | `launcher_dictionary` | `run_theory_oracle_lab.OUTPUT[root]` | `run_theory_oracle_lab.py` | `B` | `canonical_root_resolution` | `editable_value_resolved_once_against_repository_root` | `[]` |
| `b-legacy-observation` | `serialized_schema_and_reader` | `LegacyObservation` | `legacy-run-observation-v1` | `B` | `new_schema_version_legacy_read_only` | `observed_hashes_and_limits_without_v2_integrity_or_promotion` | `[]` |
| `b-legacy-observed-bundle` | `public_constructor` | `LegacyObservedBundle` | `multiagent_elbo.artifact_schema` | `B` | `immutable_snapshot_semantics` | `source_claim_eligible_is_literal_false_and_bytes_are_observed_only` | `["multiagent_elbo.LegacyObservedBundle"]` |
| `b-load-metric-record` | `serialized_record_reader` | `load_metric_record` | `multiagent_elbo.experiment_support` | `B` | `strict_version_dispatch` | `validates_metric_record_v2_closed_fields_and_derived_decision` | `["multiagent_elbo.load_metric_record"]` |
| `b-load-run` | `artifact_reader` | `load_run_bundle` | `multiagent_elbo.artifacts` | `B` | `strict_version_dispatch` | `v2_hashes_and_parses_same_bytes_v1_returns_observation` | `["multiagent_elbo.load_run_bundle"]` |
| `b-load-verified-run` | `artifact_reader` | `load_verified_run_bundle` | `multiagent_elbo.artifacts` | `B` | `strict_version_dispatch` | `accepts_run_manifest_v2_only_and_verifies_before_parse` | `["multiagent_elbo.load_verified_run_bundle"]` |
| `b-metric-comparator` | `public_constructor` | `MetricComparator` | `multiagent_elbo.experiment_support` | `B` | `factory_only_status_derivation` | `closed_operand_and_direction_carrier_no_verification_state` | `["multiagent_elbo.MetricComparator"]` |
| `b-metric-record` | `public_constructor_and_schema` | `MetricRecord` | `metric-record-v2` | `B` | `factory_only_status_derivation` | `closed_fields_derived_decision_candidate_only_producer` | `["multiagent_elbo.MetricRecord"]` |
| `b-npz-array-input` | `public_constructor` | `NpzArrayInput` | `multiagent_elbo.artifact_schema` | `B` | `new_strict_public_path` | `canonical_dtype_and_finiteness_policy_are_explicit` | `["multiagent_elbo.NpzArrayInput"]` |
| `b-output-root` | `public_configuration_field` | `OutputConfig.root` | `multiagent_elbo.config` | `B` | `canonical_root_resolution` | `string_or_Path_retained_resolved_root_authoritative` | `["multiagent_elbo.OutputConfig"]` |
| `b-premise-assessment` | `public_constructor` | `PremiseAssessment` | `multiagent_elbo.finite.agent_network` | `B` | `candidate_only_producer` | `public_carrier_cannot_serialize_promoted_state` | `["multiagent_elbo.finite.PremiseAssessment"]` |
| `b-premise-helper` | `public_function` | `assess_fixed_channel_premise` | `multiagent_elbo.finite.agent_network` | `B` | `candidate_only_producer` | `boolean_maps_to_applicability_not_verification_promotion` | `["multiagent_elbo.finite.assess_fixed_channel_premise"]` |
| `b-prepared-artifact` | `public_constructor` | `PreparedArtifact` | `multiagent_elbo.artifact_schema` | `B` | `immutable_snapshot_semantics` | `owns_exact_name_kind_bytes_size_and_SHA` | `["multiagent_elbo.PreparedArtifact"]` |
| `b-prepared-run-bundle` | `public_constructor` | `PreparedRunBundle` | `multiagent_elbo.artifact_schema` | `B` | `immutable_snapshot_semantics` | `no_mutable_caller_object_callback_handle_or_lazy_serializer` | `["multiagent_elbo.PreparedRunBundle"]` |
| `b-prepare-run` | `public_function` | `prepare_run_bundle` | `multiagent_elbo.artifacts` | `B` | `new_strict_public_path` | `zero_effect_preparation_owns_detached_immutable_bytes` | `["multiagent_elbo.prepare_run_bundle"]` |
| `b-publish-run` | `public_function` | `publish_run_bundle` | `multiagent_elbo.artifacts` | `B` | `new_strict_public_path` | `prepared_bytes_only_sibling_stage_manifest_last` | `["multiagent_elbo.publish_run_bundle"]` |
| `b-render-run` | `artifact_reader_and_publisher` | `render_run` | `multiagent_elbo.figures` | `B` | `immutable_generation_publication` | `signature_retained_generation_pointer_replaces_in_place_files` | `["multiagent_elbo.render_run"]` |
| `b-rng-streams` | `public_constructor` | `RngStreams` | `multiagent_elbo.runtime` | `B` | `immutable_snapshot_semantics` | `stream_derivation_preserved_provenance_detached` | `["multiagent_elbo.RngStreams"]` |
| `b-run-manifest-v1` | `serialized_schema` | `legacy-run-manifest-v1` | `multiagent_elbo.artifacts` | `B` | `new_schema_version_legacy_read_only` | `existing_v1_observed_only_never_rewritten_or_promoted` | `[]` |
| `b-run-manifest-v2` | `serialized_schema` | `run-manifest-v2` | `multiagent_elbo.artifact_schema` | `B` | `new_strict_public_path` | `closed_per_file_size_and_SHA_over_prepared_bytes` | `[]` |
| `b-run-payloads` | `public_constructor` | `RunPayloads` | `multiagent_elbo.artifact_schema` | `B` | `immutable_snapshot_semantics` | `caller_mappings_are_detached_during_zero_effect_preparation` | `["multiagent_elbo.RunPayloads"]` |
| `b-run-store` | `public_constructor_and_reader` | `RunStore` | `multiagent_elbo.artifacts` | `B` | `strict_version_dispatch` | `legacy_incremental_methods_deprecated_test_compatibility_only` | `["multiagent_elbo.RunStore"]` |
| `b-verified-run-bundle` | `public_constructor` | `VerifiedRunBundle` | `multiagent_elbo.artifact_schema` | `B` | `immutable_snapshot_semantics` | `verified_bytes_parsed_once_and_returned_as_frozen_payloads` | `["multiagent_elbo.VerifiedRunBundle"]` |
| `b-verify-legacy-run` | `artifact_reader` | `verify_legacy_v1_observed` | `multiagent_elbo.artifacts` | `B` | `new_schema_version_legacy_read_only` | `inventories_actual_legacy_bytes_without_writing_or_promoting` | `["multiagent_elbo.verify_legacy_v1_observed"]` |
| `c-allow-tf32` | `public_configuration_field` | `ComputeConfig.allow_tf32` | `multiagent_elbo.config` | `C` | `transport_and_validate_previously_inert_field` | `request_worker_echo_and_identity_digest_must_agree` | `[]` |
| `c-collect-diagnostics` | `public_configuration_field` | `collect_diagnostics` | `multiagent_elbo.config.OutputConfig` | `C` | `reject_previously_accepted_unsupported_value` | `scale_cocycle_admits_true_only_until_implemented` | `[]` |
| `c-confirmatory` | `public_function` | `publish_confirmatory_experiment` | `multiagent_elbo.realizations.gaussian.fixed_ray_experiment` | `C` | `required_execution_identity` | `unsupported_config_rejects_before_gate_or_output` | `["multiagent_elbo.realizations.gaussian.publish_confirmatory_experiment"]` |
| `c-deterministic` | `public_configuration_field` | `ComputeConfig.deterministic` | `multiagent_elbo.config` | `C` | `transport_and_validate_previously_inert_field` | `request_worker_echo_and_identity_digest_must_agree` | `[]` |
| `c-device-index` | `public_configuration_field` | `ComputeConfig.device_index` | `multiagent_elbo.config` | `C` | `transport_and_validate_previously_inert_field` | `nondefault_transported_and_verified_not_ignored` | `[]` |
| `c-execution-identity` | `public_constructor` | `FixedRayExecutionIdentity` | `multiagent_elbo.realizations.gaussian.fixed_ray_experiment` | `C` | `new_strict_public_path` | `binds_system_config_source_root_and_protocol_digests` | `["multiagent_elbo.realizations.gaussian.FixedRayExecutionIdentity"]` |
| `c-fixed-ray-system` | `public_constructor` | `FixedRaySystem` | `multiagent_elbo.realizations.gaussian.fixed_ray` | `C` | `required_keyword_domain_policy` | `valid_systems_require_explicit_policy_no_unchecked_constructor` | `["multiagent_elbo.realizations.gaussian.FixedRaySystem"]` |
| `c-fixed-run` | `public_function` | `run_fixed_ray_experiment` | `multiagent_elbo.realizations.gaussian.fixed_ray_experiment` | `C` | `required_execution_identity` | `CPU_and_authorized_paths_use_same_identity_before_effects` | `["multiagent_elbo.realizations.gaussian.run_fixed_ray_experiment"]` |
| `c-fixed-schema-confirmatory-endpoints` | `serialized_schema_family` | `confirmatory_endpoints:v1_to_v2` | `gaussian-fixed-ray-confirmatory-endpoints-v1-to-v2` | `C` | `new_schema_version_legacy_read_only` | `v1_observed_only_v2_requires_both_identity_digests` | `[]` |
| `c-fixed-schema-confirmatory-execution` | `serialized_schema_family` | `confirmatory_execution:v1_to_v2` | `gaussian-fixed-ray-confirmatory-execution-v1-to-v2` | `C` | `new_schema_version_legacy_read_only` | `v1_observed_only_v2_requires_both_identity_digests` | `[]` |
| `c-fixed-schema-confirmatory-gate` | `serialized_schema_family` | `confirmatory_gate:v1_to_v2` | `cuda-confirmatory-operator-gate-v1-to-v2` | `C` | `new_schema_version_legacy_read_only` | `v1_observed_only_v2_requires_both_identity_digests` | `[]` |
| `c-fixed-schema-confirmatory-job` | `serialized_schema_family` | `confirmatory_job:v1_to_v2` | `gaussian-fixed-ray-confirmatory-job-v1-to-v2` | `C` | `new_schema_version_legacy_read_only` | `v1_observed_only_v2_requires_both_identity_digests` | `[]` |
| `c-fixed-schema-holdout-execution` | `serialized_schema_family` | `holdout_execution:v1_to_v2` | `gaussian-fixed-ray-confirmatory-holdout-execution-v1-to-v2` | `C` | `new_schema_version_legacy_read_only` | `v1_observed_only_v2_requires_both_identity_digests` | `[]` |
| `c-fixed-schema-idle-gate` | `serialized_schema_family` | `idle_gate:v1_to_v2` | `cuda-idle-operator-gate-v1-to-v2` | `C` | `new_schema_version_legacy_read_only` | `v1_observed_only_v2_requires_both_identity_digests` | `[]` |
| `c-fixed-schema-job-table` | `serialized_schema_family` | `job_table:v1_to_v2` | `gaussian-fixed-ray-job-table-v1-to-v2` | `C` | `new_schema_version_legacy_read_only` | `v1_observed_only_v2_requires_both_identity_digests` | `[]` |
| `c-fixed-schema-pilot-endpoints` | `serialized_schema_family` | `pilot_endpoints:v1_to_v2` | `gaussian-fixed-ray-endpoints-v1-to-v2` | `C` | `new_schema_version_legacy_read_only` | `v1_observed_only_v2_requires_both_identity_digests` | `[]` |
| `c-fixed-schema-primary-execution` | `serialized_schema_family` | `primary_execution:v1_to_v2` | `gaussian-fixed-ray-confirmatory-primary-execution-v1-to-v2` | `C` | `new_schema_version_legacy_read_only` | `v1_observed_only_v2_requires_both_identity_digests` | `[]` |
| `c-fixed-schema-sentinel` | `serialized_schema_family` | `sentinel:v1_to_v2` | `gaussian-fixed-ray-cuda-sentinel-v1-to-v2` | `C` | `new_schema_version_legacy_read_only` | `v1_observed_only_v2_requires_both_identity_digests` | `[]` |
| `c-fixed-schema-worker-exchange-index` | `serialized_schema_family` | `worker_exchange_index:v1_to_v2` | `gaussian-fixed-ray-worker-exchange-index-v1-to-v2` | `C` | `new_schema_version_legacy_read_only` | `v1_observed_only_v2_requires_both_identity_digests` | `[]` |
| `c-frozen-matrix-policy` | `public_constant` | `FROZEN_FIXED_RAY_MATRIX_POLICY` | `multiagent_elbo.realizations.gaussian.fixed_ray` | `C` | `new_public_assessment` | `single_preregistered_domain_policy_constant` | `["multiagent_elbo.realizations.gaussian.FROZEN_FIXED_RAY_MATRIX_POLICY"]` |
| `c-identity-validator` | `public_function` | `validate_fixed_ray_execution_identity` | `multiagent_elbo.realizations.gaussian.fixed_ray_experiment` | `C` | `new_strict_public_path` | `sole_identity_builder_before_every_fixed_ray_effect` | `["multiagent_elbo.realizations.gaussian.validate_fixed_ray_execution_identity"]` |
| `c-legacy-fixed-observation` | `public_constructor` | `LegacyFixedRayObservation` | `multiagent_elbo.realizations.gaussian.fixed_ray_experiment` | `C` | `new_schema_version_legacy_read_only` | `v1_records_are_observed_at_revision_and_never_current_eligible` | `[]` |
| `c-legacy-worker-observation` | `public_constructor` | `LegacyWorkerObservation` | `multiagent_elbo.cuda_backend` | `C` | `new_schema_version_legacy_read_only` | `protocol_v1_v2_payloads_never_construct_current_results` | `[]` |
| `c-load-fixed-run` | `artifact_reader` | `load_verified_fixed_ray_bundle` | `multiagent_elbo.artifacts` | `C` | `strict_version_dispatch` | `accepts_identity_bound_run_manifest_v3_only` | `["multiagent_elbo.realizations.gaussian.load_verified_fixed_ray_bundle"]` |
| `c-prepare-fixed-run` | `public_function` | `prepare_fixed_ray_run_bundle` | `multiagent_elbo.artifacts` | `C` | `new_strict_public_path` | `emits_run_manifest_v3_with_both_identity_digests` | `["multiagent_elbo.realizations.gaussian.prepare_fixed_ray_run_bundle"]` |
| `c-preregistered-system` | `public_factory` | `build_preregistered_system` | `multiagent_elbo.realizations.gaussian.fixed_ray` | `C` | `required_keyword_domain_policy` | `default_frozen_policy_explicit_return_fully_assessed` | `["multiagent_elbo.realizations.gaussian.build_preregistered_system"]` |
| `c-retained-order` | `public_configuration_field` | `retained_interaction_order` | `multiagent_elbo.config.TheoryConfig` | `C` | `reject_previously_accepted_unsupported_value` | `scale_cocycle_admits_two_only_until_implemented` | `[]` |
| `c-run-manifest-v3` | `serialized_schema` | `run-manifest-v3` | `multiagent_elbo.artifact_schema` | `C` | `new_schema_version_legacy_read_only` | `fixed_ray_only_v2_general_manifest_remains_unchanged` | `[]` |
| `c-sentinel` | `public_function_and_reader` | `run_cuda_sentinel` | `multiagent_elbo.realizations.gaussian.fixed_ray_experiment` | `C` | `required_execution_identity` | `v2_identity_bound_historical_sentinel_read_only` | `["multiagent_elbo.realizations.gaussian.run_cuda_sentinel"]` |
| `c-worker-manifest` | `public_constructor_and_schema` | `WorkerProtocolManifest` | `worker-protocol-v3` | `C` | `new_schema_version_legacy_read_only` | `v1_v2_historical_v3_binds_settings_and_digests` | `["multiagent_elbo.WorkerProtocolManifest"]` |
| `c-worker-request-v3` | `public_constructor_and_schema` | `WorkerRequestV3` | `cuda-worker-request-v3` | `C` | `new_schema_version_legacy_read_only` | `v1_v2_never_rewritten_v3_required_for_current_claims` | `[]` |
| `c-worker-response-v3` | `public_constructor_and_schema` | `WorkerResponseV3` | `cuda-worker-response-v3` | `C` | `new_schema_version_legacy_read_only` | `echoes_requested_and_observed_policy_plus_both_digests` | `[]` |
| `c-worker-result` | `public_constructor` | `WorkerJobResult` | `multiagent_elbo.cuda_backend` | `C` | `new_schema_version_legacy_read_only` | `constructed_only_from_validated_protocol_v3_response` | `["multiagent_elbo.WorkerJobResult"]` |
| `c-worker-runtime-binding-v3` | `public_constructor` | `WorkerRuntimeBindingV3` | `multiagent_elbo.cuda_backend` | `C` | `new_schema_version_legacy_read_only` | `closed_requested_or_observed_device_dtype_determinism_policy` | `[]` |
| `d-clock` | `public_protocol` | `Clock` | `multiagent_elbo.performance` | `D` | `new_measurement_surface` | `injectable_monotonic_clock_contract` | `["multiagent_elbo.Clock"]` |
| `d-cpu-profile` | `click_to_run_launcher` | `run_remediation_performance_profile.CONFIG` | `tools/run_remediation_performance_profile.py` | `D` | `new_measurement_surface` | `D0_measures_D1_branches_only_from_frozen_decision` | `[]` |
| `d-perf-counter-clock` | `public_constructor` | `PerfCounterClock` | `multiagent_elbo.performance` | `D` | `new_measurement_surface` | `production_clock_uses_perf_counter_ns` | `["multiagent_elbo.PerfCounterClock"]` |
| `d-timing-observation` | `public_constructor_and_schema` | `TimingObservation` | `timing-observation-v1` | `D` | `new_measurement_surface` | `immutable_raw_record_with_candidate_producer_state` | `["multiagent_elbo.TimingObservation"]` |
| `d-timing-span` | `public_constructor_and_schema` | `TimingSpan` | `timing-span-v1` | `D` | `new_measurement_surface` | `immutable_nonnegative_monotonic_component_span` | `["multiagent_elbo.TimingSpan"]` |
| `d-worker-timing` | `serialized_schema` | `cuda-worker-timing-v1` | `multiagent_elbo.cuda_backend` | `D` | `new_measurement_surface` | `non_authoritative_sidecar_bound_to_request_response_hashes` | `[]` |

Write `status-failure-contract-v1.json` with the following exact `states` object:

```json
{
  "theorem_status":["ESTABLISHED","HYPOTHESIS","CONJECTURE","NUMERICAL","OPEN"],
  "producer_verification_state":["CANDIDATE"],
  "assessment_decision":["fail","inconclusive","pass"],
  "run_status":["incomplete","complete","failed"],
  "external_ledger_state":["CANDIDATE","LLM_SUPPORTED","EVIDENCE_VERIFIED","REFUTED","INCONCLUSIVE"],
  "historical_state":["EVIDENCE_VERIFIED_AT_RECORDED_REVISION","STALE_FOR_CURRENT_REVISION"]
}
```

Its `status_rules` array is exactly: `producer records serialize verification_state exactly CANDIDATE`; `assessment_decision never occupies a verification_state field`; `external terminal states require current domain-eligible evidence`; `historical state records both git revision and artifact revision`; `any new repository revision stales prior current code and CUDA evidence`.

Its `migrations` array contains one record per row below. Columns map exactly to `{schema,owning_wave,reader_behavior,writer_behavior,rewrite_behavior,promotion_behavior}`.

| schema | wave | reader_behavior | writer_behavior | rewrite_behavior | promotion_behavior |
|---|---|---|---|---|---|
| `fisher-recovery-v1` | `A` | `legacy_observation_only` | `forbidden` | `never` | `never` |
| `fisher-recovery-v2` | `A` | `strict_closed_fields` | `current_only` | `new_record_only` | `external_ledger_only` |
| `metric-record-v1` | `B` | `legacy_observation_only` | `forbidden` | `never` | `never` |
| `metric-record-v2` | `B` | `strict_closed_fields` | `current_only` | `new_record_only` | `external_ledger_only` |
| `legacy-run-manifest-v1` | `B` | `legacy_run_observation_v1` | `deprecated_test_compatibility_only` | `never` | `never` |
| `legacy-run-observation-v1` | `B` | `strict_closed_fields` | `adapter_output_only` | `never` | `never` |
| `run-manifest-v2` | `B` | `verify_each_owned_byte_then_parse_same_buffer` | `prepared_bundle_only` | `new_sibling_publication_only` | `external_ledger_only` |
| `run-config-v2` | `B` | `strict_closed_fields` | `prepared_bundle_only` | `new_record_only` | `not_applicable` |
| `run-provenance-v2` | `B` | `strict_closed_fields` | `prepared_bundle_only` | `new_record_only` | `not_applicable` |
| `legacy-figure-manifest-v1` | `B` | `legacy_observation_only` | `forbidden` | `never` | `never` |
| `figure-cache-identity-v2` | `B` | `strict_closed_fields` | `verified_run_only` | `new_generation_only` | `not_applicable` |
| `figure-generation-manifest-v2` | `B` | `strict_closed_fields` | `immutable_generation_only` | `never` | `external_ledger_only` |
| `active-generation-v2` | `B` | `strict_closed_fields` | `atomic_pointer_replace_only` | `atomic_replace` | `not_applicable` |
| `figure-publication-journal-v2` | `B` | `strict_recovery_only` | `sibling_staging_only` | `recover_then_replace` | `not_applicable` |
| `worker-protocol-v1` | `C` | `historical_observation_only` | `forbidden` | `never` | `never` |
| `worker-protocol-v2` | `C` | `historical_observation_only` | `forbidden` | `never` | `never` |
| `cuda-worker-request-v3` | `C` | `strict_identity_bound` | `current_worker_only` | `new_record_only` | `external_ledger_only` |
| `cuda-worker-response-v3` | `C` | `strict_identity_bound` | `current_worker_only` | `new_record_only` | `external_ledger_only` |
| `worker-result-v1` | `C` | `historical_observation_only` | `forbidden` | `never` | `never` |
| `worker-result-v2` | `C` | `historical_observation_only` | `forbidden` | `never` | `never` |
| `run-manifest-v3` | `C` | `strict_fixed_ray_identity_bound` | `fixed_ray_prepared_bundle_only` | `new_sibling_publication_only` | `external_ledger_only` |
| `fixed-ray-record-v1-to-v2-families` | `C` | `v1_legacy_observation_v2_strict_identity_bound` | `v2_current_only` | `never_rewrite_v1` | `external_ledger_only_for_v2` |
| `timing-span-v1` | `D` | `strict_closed_fields` | `measurement_only` | `new_record_only` | `never` |
| `timing-observation-v1` | `D` | `strict_revision_bound` | `measurement_only` | `new_record_only` | `external_ledger_only` |
| `cuda-worker-timing-v1` | `D` | `strict_request_response_bound` | `measurement_only` | `new_sidecar_only` | `never` |
| `remediation-evidence-v1` | `0` | `strict_closed_fields_and_current_hashes` | `prepared_evidence_bundle_only` | `never` | `external_ledger_only` |

The contract test asserts exact schema rows, exact namespaces/order, and that every historical-state record carries both a concrete Git SHA and artifact revision. It also asserts that every legacy schema has `rewrite_behavior="never"` and cannot acquire current promotion.

The cross-wave ownership seam is literal. `ExactFisherChannelWitness` is defined
only in `multiagent_elbo.finite.fisher`; `scale_cocycle` may import it but may not
define a second carrier. `InformationPoint` preserves, in order, its existing
constructor fields `probability`, `score`, `fisher`, `vfe_gradient`,
`natural_gradient`, `fisher_projector`, `rank`, `nullity`,
`positive_spectrum_condition_number`, `range_residual`, `inverse_rule`, and
`used_pseudoinverse`; Wave A computes the quotient assessment internally and
does not add or replace a constructor field. The one `MatrixDomainPolicy` class
is owned by Wave A at `multiagent_elbo.conditioning`. Wave C imports and
re-exports that same class and may construct `FROZEN_FIXED_RAY_MATRIX_POLICY`,
but it may not define a duplicate policy type. Contract tests assert definition
ownership, constructor signature equality, and object identity across re-exports.

The same file's `failure_order` array is literal below. Split `validation_order` on ` > ` and `negative_controls` on `;` into ordered JSON arrays; no token may be empty.

| entry_point | wave | validation_order | last_permitted_effect | negative_controls |
|---|---|---|---|---|
| `ProbabilityMeasure.__init__` | `A` | `shape > numeric_dtype > finite > nonnegative > structural_total > detach_to_immutable_bytes` | `return_validated_immutable_object` | `loose_tolerance_mass_0_8;zero_total;nan;caller_mutation` |
| `FiniteMeasure.__init__` | `A` | `shape > numeric_dtype > finite > nonnegative > detach_to_immutable_bytes` | `return_validated_immutable_object` | `negative_mass;nan;caller_mutation` |
| `MarkovKernel.__init__` | `A` | `shape > numeric_dtype > finite > nonnegative > each_structural_row_total > detach_to_immutable_bytes` | `return_validated_immutable_object` | `zero_row;loose_tolerance_row_0_8;nan;caller_mutation` |
| `InformationPoint.__init__` | `A` | `coordinate_shape > probability_structural_membership > parameter_finiteness > detach_to_immutable_bytes` | `return_validated_immutable_object` | `unnormalized_probability;nan_parameter;caller_mutation` |
| `ExperimentConfig.from_dicts` | `C` | `closed_dictionary_keys > scalar_types > finite_ranges > supported_experiment_options > fixed_ray_identity_fields` | `return_validated_immutable_object` | `matrix_dimension_3;unsupported_retained_order;collect_diagnostics_false;boolean_numeric_alias` |
| `MetricRecord.__init__` | `B` | `closed_enums > finite_operands > finite_nonnegative_tolerance > derive_decision > force_candidate_state` | `return_validated_immutable_object` | `nan_value;negative_tolerance;caller_selected_status;promoted_verification_state` |
| `metric_factories` | `B` | `predicate_specific_operands > finite_values > finite_nonnegative_tolerance > derive_decision > construct_metric_record` | `return_validated_immutable_object` | `nan_comparison;infinite_bound;negative_tolerance` |
| `RngStreams.create` | `B` | `integer_master_seed > fixed_stream_names > spawn_keys > create_generators > freeze_provenance` | `return_validated_immutable_object` | `boolean_seed;duplicate_stream_name;provenance_mutation` |
| `assemble_precision` | `A` | `shape > symmetry > finite_entries > spectral_assessment > assemble` | `return_validated_immutable_object` | `material_negative_mode;inconclusive_band;nan_entry` |
| `recovery_diagnostics` | `A` | `channel_shapes > probability_membership > shared_eigensystem > null_block_checks > relative_loewner_assessment` | `return_validated_immutable_object` | `scaled_total_information_loss;rank_cutoff_disagreement;fine_null_leakage` |
| `FixedRaySystem.__init__` | `C` | `required_domain_policy > shape > finite_entries > symmetry > strict_spd > condition_bound > detach_to_immutable_bytes` | `return_validated_immutable_object` | `infinite_entry;condition_1e13;missing_policy;caller_mutation` |
| `validate_fixed_ray_execution_identity` | `C` | `validate_config > resolve_output_root > validate_source_identity > construct_assessed_system > bind_scientific_digest > bind_execution_digest` | `return_validated_immutable_object` | `dimension_3;unsupported_device_policy;output_overlap;source_digest_mismatch` |
| `resolve_output_root` | `B` | `parse_path > resolve_repository_anchor > reject_missing_alias_ambiguity > reject_hashed_root_overlap` | `return_validated_absolute_path` | `source_descendant;theory_ancestor;symlink_alias;junction_alias` |
| `prepare_run_bundle` | `B` | `validate_config_and_root > detach_payloads > validate_metric_records > validate_array_dtypes > serialize_in_memory > hash_exact_bytes > validate_manifest_in_memory` | `return_detached_immutable_buffers` | `object_dtype;nan_metric;mutable_source_after_prepare;forbidden_output_overlap` |
| `publish_run_bundle` | `B` | `validate_prepared_type > rehash_prepared_bytes > validate_destination_identity > check_nonexistence > create_sibling_staging > write_owned_bytes > fsync > write_manifest_last > atomic_install` | `create_sibling_staging_directory` | `tampered_prepared_bytes;existing_destination;mid_write_fault;manifest_replace_fault` |
| `load_run_bundle` | `B` | `resolve_root > lstat_manifest > read_manifest_once > dispatch_schema > read_each_owned_file_once > verify_size_and_hash > parse_same_bytes > freeze_payload` | `return_verified_immutable_bundle` | `unknown_schema;byte_tamper;symlink_swap;object_dtype_npz` |
| `render_run` | `B` | `resolve_roots > load_verified_bundle > validate_request > validate_inputs > compute_cache_identity > acquire_lock > recover_journal > create_sibling_generation_staging` | `create_sibling_generation_staging_directory` | `stale_cache_identity;invalid_requested_figure;input_tamper;replacement_fault` |
| `run_finite_experiment` | `B` | `validate_config > resolve_root > compute_in_memory > prepare_run_bundle > publish_run_bundle` | `create_sibling_staging_directory` | `invalid_metric;invalid_array_dtype;output_overlap` |
| `run_multiagent_network_experiment` | `B` | `validate_config > resolve_root > compute_in_memory > prepare_run_bundle > publish_run_bundle` | `create_sibling_staging_directory` | `promoted_premise;invalid_metric;output_overlap` |
| `run_attention_experiment` | `B` | `validate_config > resolve_root > compute_in_memory > prepare_run_bundle > publish_run_bundle` | `create_sibling_staging_directory` | `invalid_metric;object_array;output_overlap` |
| `run_categorical_dqm_experiment` | `B` | `validate_config > resolve_root > compute_in_memory > prepare_run_bundle > publish_run_bundle` | `create_sibling_staging_directory` | `invalid_probability;invalid_metric;output_overlap` |
| `run_counterexample_experiment` | `B` | `validate_config > resolve_root > compute_in_memory > prepare_run_bundle > publish_run_bundle` | `create_sibling_staging_directory` | `promoted_candidate;invalid_metric;output_overlap` |
| `run_information_history_experiment` | `B` | `validate_config > resolve_root > compute_in_memory > prepare_run_bundle > publish_run_bundle` | `create_sibling_staging_directory` | `invalid_probability;invalid_recovery_schema;output_overlap` |
| `run_scale_cocycle_experiment` | `C` | `validate_config > validate_supported_options > resolve_root > compute_in_memory > prepare_run_bundle > publish_run_bundle` | `create_run_after_supported_option_validation` | `retained_order_not_2;collect_diagnostics_false;output_overlap` |
| `run_theory_oracle_experiment` | `B` | `validate_config > resolve_root > compute_in_memory > prepare_run_bundle > publish_run_bundle` | `create_sibling_staging_directory` | `promoted_candidate;invalid_metric;output_overlap` |
| `run_gauge_holonomy_experiment` | `B` | `validate_config > resolve_root > compute_in_memory > prepare_run_bundle > publish_run_bundle` | `create_sibling_staging_directory` | `invalid_metric;invalid_array_dtype;output_overlap` |
| `run_gaussian_experiment` | `B` | `validate_config > resolve_root > compute_in_memory > prepare_run_bundle > publish_run_bundle` | `create_sibling_staging_directory` | `invalid_psd_input;invalid_metric;output_overlap` |
| `run_gaussian_fixed_ray_diagnostic` | `C` | `validate_execution_identity > resolve_root > compute_cpu_diagnostics > prepare_run_bundle > publish_run_bundle` | `create_sibling_staging_directory` | `dimension_3;invalid_matrix_domain;output_overlap` |
| `run_fixed_ray_experiment` | `C` | `validate_execution_identity > validate_mode > resolve_gate_inputs > capture_gate_if_required > create_run_or_spawn_worker` | `capture_gate_after_identity_validation` | `dimension_3_each_mode;unsupported_device_policy;invalid_matrix_domain;output_overlap` |
| `run_cuda_sentinel` | `C` | `validate_execution_identity > validate_operator_gate > validate_worker_protocol > capture_gate > spawn_preflight > spawn_worker > prepare_publication` | `capture_gate_after_identity_validation` | `dimension_3;expired_gate;identity_digest_mismatch;worker_echo_mismatch` |
| `publish_confirmatory_experiment` | `C` | `validate_execution_identity > validate_sentinel_binding > validate_confirmatory_gate > capture_gate > spawn_workers > prepare_publication` | `capture_gate_after_identity_validation` | `dimension_3;stale_sentinel;expired_gate;identity_digest_mismatch` |
| `run_worker_job` | `C` | `validate_request_schema > validate_execution_identity > validate_interpreter_and_lock > validate_device_policy > spawn_worker > validate_response` | `spawn_worker_after_request_validation` | `protocol_v1_current_claim;device_mismatch;determinism_mismatch;identity_digest_mismatch` |
| `run_remediation_performance_profile` | `D` | `validate_profile_dictionary > bind_source_config_environment > validate_cpu_or_operator_cuda_scope > prepare_measurement_root > execute_repeated_spans > publish_raw_observations > apply_frozen_decision_rule` | `create_profile_directory_after_policy_validation` | `stale_revision;changed_environment;unauthorized_cuda_scope;decision_rule_mutation` |

Run the combined GREEN command after both literal files are written, then commit them with `tests/test_remediation_contracts.py` as already shown in Task 2 Step 5.

### Task 3: Pin historical fixed-ray bundles without upgrading them

**Files:**
- Create: `docs/verification/remediation/historical-fixed-ray-bundles-v1.json`
- Modify: `tests/test_remediation_contracts.py`

**Interfaces:**
- Produces two bundle records named `gaussian-confirmatory-fcb2c49` and `fixed-model-attraction-diagnostic`.
- Each record has `legacy_schema`, `historical_git_revision`, `limitations`, and a sorted file inventory of `{path, size_bytes, sha256}`.
- The confirmatory inventory is exactly the 10 files under `docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/`.
- The diagnostic inventory is exactly the 9 files under `docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic/`.

- [ ] **Step 1: Write the missing and mutation-sensitive RED**

```python
def test_historical_fixed_ray_bundles_are_complete_and_byte_pinned():
    payload = _load_json(HISTORICAL_BUNDLES_PATH)
    expected_counts = {
        "gaussian-confirmatory-fcb2c49": 10,
        "fixed-model-attraction-diagnostic": 9,
    }
    bundles = {item["bundle_id"]: item for item in payload["bundles"]}
    assert {key: len(value["files"]) for key, value in bundles.items()} == expected_counts
    for bundle in bundles.values():
        assert bundle["limitations"]
        for record in bundle["files"]:
            data = (ROOT / record["path"]).read_bytes()
            assert len(data) == record["size_bytes"]
            assert hashlib.sha256(data).hexdigest() == record["sha256"]
```

- [ ] **Step 2: Run the focused RED**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_remediation_contracts.py -k historical_fixed_ray -q -p no:cacheprovider --basetemp=.pytest-wave0-task3-red
```

Expected: FAIL because the historical inventory is missing.

- [ ] **Step 3: Write the literal deterministic inventory**

Use `schema_version="historical-fixed-ray-bundles-v1"`; for both records use `legacy_schema="observed-v1"` and limitation `"Observed historical bytes support compatibility and reproduction only; they do not acquire manifest-v2 self-integrity or current scientific promotion."`. Write the following exact sorted file arrays; the implementation does not regenerate, normalize, or rewrite any source byte.

```json
[
  {
    "bundle_id":"gaussian-confirmatory-fcb2c49",
    "historical_git_revision":"fcb2c49efdca2ad3ee502dc08fbb82fc285e7a05",
    "files":[
      {"path":"docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/config.json","size_bytes":792,"sha256":"66e474db7e46ae0589ca5198712c59aa9f28317d219381ddf96b989e5d40d191"},
      {"path":"docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/confirmatory_arrays.npz","size_bytes":71942,"sha256":"7040967043619fd52a0386ff0b9623febdd4c97f0c2356f8abb98fd786dc2b6a"},
      {"path":"docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/confirmatory_endpoints.json","size_bytes":214173,"sha256":"7d6b36b5bde80969d8974d5550c0ed8c125896ee03be7ffd196d3915f8261556"},
      {"path":"docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/confirmatory_job_table.json","size_bytes":9062,"sha256":"a50dd3893ce1ad9c081a8e2f2cbc5adc676e2b217c9c3ec321e8b0d62b453adf"},
      {"path":"docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/current_result.json","size_bytes":8833,"sha256":"35b1d39fb11523613b5d5771e9862fb0d2b09de2373cfbe52c1209ec2c8090ab"},
      {"path":"docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/holdout_analysis.json","size_bytes":8152,"sha256":"ff09a656d7638a233d21149132367b95072fae6030187ee997290aa1a0596d1d"},
      {"path":"docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/manifest.json","size_bytes":2522,"sha256":"7e0a050850b48b446c70bff3a67010c84d2daa1fada6c48742d3ab152d43a1fb"},
      {"path":"docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/metrics.json","size_bytes":394,"sha256":"cd45e55dd39236b556dc200a04ad081affcb19a6c52fb584ad63f3f1992f7f59"},
      {"path":"docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/primary_analysis.json","size_bytes":17093,"sha256":"f8b58ae7f8777e18800c37d63b55d37c0052cd47b407a40497405ef5f6375155"},
      {"path":"docs/verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/source_binding.json","size_bytes":2557,"sha256":"81ae0487f2b1779076b361f3339275280a1a3a5f1e8c817d52250b5ee61fae75"}
    ]
  },
  {
    "bundle_id":"fixed-model-attraction-diagnostic",
    "historical_git_revision":"039df35daa30a49e90f178edde7bfc999a7ee629",
    "files":[
      {"path":"docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic/config.json","size_bytes":917,"sha256":"0fed6f65531407e59c52b9d3916164c0f7c0810a6c5421a91fec8a33e53bea71"},
      {"path":"docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic/fixed_model_diagnostic_arrays.npz","size_bytes":278274,"sha256":"1597a92acf50811687183f0062f104acb3c5e4649bb6270e0b153841f9e08bff"},
      {"path":"docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic/fixed_model_explanation.json","size_bytes":810,"sha256":"aed3fd6a3620eff3fefe004b7f3ad65884d3d5a73378edd8ed0fb629c65ce20a"},
      {"path":"docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic/fixed_model_spectral_diagnostics.json","size_bytes":6233,"sha256":"8f1fbf50ca691c0245c0e59eaaced25af6c02aa5b4f46ac0d7908961e8e8669b"},
      {"path":"docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic/fixed_model_support_certificate.json","size_bytes":2101,"sha256":"a65bd15e36d85cf810cdb5f7bb5a7bf0dcfcf56672d6601e3d7237be06b07c8b"},
      {"path":"docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic/fixed_model_trajectory_diagnostics.json","size_bytes":192056,"sha256":"e6169a6fad904bf92082f6d1c12203a8d843e01e473804e1dae3161037111f4f"},
      {"path":"docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic/manifest.json","size_bytes":28891,"sha256":"1829624d76fe723606b5e20fbd7ad85961610b2513c59271c641f560ac38d907"},
      {"path":"docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic/metrics.json","size_bytes":1077,"sha256":"9aed3241befa42686486b7ce7c2d04ce771bf7d17d542dc6ecdb93798ae1f784"},
      {"path":"docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic/source_to_output_binding.json","size_bytes":5636,"sha256":"df3130e56bfd1bdd91801a13b6f6ffabe16931813a264ff3e2e2805891b7a355"}
    ]
  }
]
```

- [ ] **Step 4: Prove drift detection without changing tracked evidence**

Copy one historical directory into `tmp_path`, mutate one byte, point the test helper at that temporary root, and assert a `ValueError` containing `historical bundle hash mismatch`. Never mutate the tracked source bundle.

- [ ] **Step 5: Run GREEN and commit**

Run the Step 2 command, then:

```powershell
git add -- docs/verification/remediation/historical-fixed-ray-bundles-v1.json tests/test_remediation_contracts.py
git commit -m "test: pin historical fixed-ray evidence"
```

### Task 4: Implement the closed remediation evidence index

#### Normative Task 4-6 evidence correction

This subsection and the corrected executable snippets below are binding wherever
older Task 4-6 prose conflicts with them. The evidence lifecycle is: run exact
`P/P` candidate suites and publish the candidate child `E`; rerun exact `E/P`
closure suites into ignored raw staging; compute a detached review-context
digest; obtain and validate raw reviews and adjudicators; privacy-transform and
validate the complete detached public set in memory; publish that set once to an
absent closure directory; start the installed gate; prove its empty template
fails; and populate only from the indexed public review bytes. No closure index,
ledger claim, view, adjudicator, or public directory exists before review
validation. A wrapper never invents a view or adjudication.

Create `docs/verification/remediation/verification-contract-v1.json` with closed
root fields `schema_version`, `canonical_relative_root`, `active_path_policy`,
and `files`. Values are
`schema_version="verification-contract-v1"`,
`canonical_relative_root=".codex/skills/verification"`, and
`active_path_policy="skill_plus_references_schemas_and_scripts_without_caches"`.
The sorted `files` array is exactly:

```json
[
  {"path":"SKILL.md","size_bytes":4653,"sha256":"dc5dec74ac5c3bae712b2bdc16c71383d67923ef108e6d7f9d278a6a950b17b1"},
  {"path":"references/contract.md","size_bytes":6128,"sha256":"bef6d266c94e2da962b8d1899846ea8fed83ff8f30e7376f87e0cfbe22b8de01"},
  {"path":"references/criteria-code.md","size_bytes":963,"sha256":"4febab87f009dd8ab60a381600f8e18e62322d86151f7aa5ee6a346ae87f5152"},
  {"path":"references/criteria-evidence.md","size_bytes":908,"sha256":"7dc751859c962f3e34a9bfff9ca981684a606dae8d49a2e5e6c3362a1d3d5990"},
  {"path":"references/criteria-experiment.md","size_bytes":893,"sha256":"2a540b9a92e1c01ce6276d89dc603c7e2f48c803b8cf83dca776968bae8bafb1"},
  {"path":"references/criteria-general.md","size_bytes":1082,"sha256":"dfa5236f26259b92a8a3507a4cc928fa836951f92e829526052fa412a4932729"},
  {"path":"references/criteria-math.md","size_bytes":923,"sha256":"b604f4d9ef8ed3fbafc15589620955dba88128b38c5c5c88c3343f059d769979"},
  {"path":"schemas/claim-ledger.schema.json","size_bytes":9897,"sha256":"e96958dc6606be521ec103a439c5a3c0e21f5417c6a1d445ae0401d5fabb6478"},
  {"path":"scripts/verification_gate.py","size_bytes":57702,"sha256":"a8a799496762910c463ecc179a4d63dc40107fcbe81553add189de7ed1ce4c95"}
]
```

**Binding 2026-08-13 security correction.** Freeze generic CLI
`tools/remediation_evidence.py run-verification-gate --snapshot PATH --root DIR -- <start|validate> ARGS`.
`--root` is mandatory and must resolve to an existing non-reparse directory
whose final normalized path components are exactly
`.codex/skills/verification`. There is no home-directory discovery, PATH
discovery, registry lookup, environment override, or `.claude` fallback.
The command validates the snapshot's closed schema, the exact nine sorted active
paths, every size/hash, and absence of unexpected active files in `references/`,
`schemas/`, and `scripts/` other than `__pycache__`/`*.pyc`. It never returns an
executable path. It retains the validated gate source bytes and passes those
bytes on standard input to one fixed bootstrap in a fresh
`C:\Python314\python.exe -I -S -B -c` child. The child runs from a fresh neutral
directory with all `PYTHON*` environment variables removed, compiles the gate
under a non-`__main__` name, and exposes only gate `start`/`validate` plus the
internal `capture_artifact_revision` operation used by the checked-in Wave 0
builder. Requests and responses use strict canonical framed JSON; unframed,
malformed, extra-field, unsupported-operation, or nonzero-bootstrap output fails
closed. The parent never imports or executes gate bytes and never reopens the
validated path. `evals/` is explicitly outside the runtime-active path policy.

The repository snapshot itself is selected by the tested-input resolver, appears
in `source_config_bindings`, and is the third exact dependency input after
`pyproject.toml` and `environments/cuda-rtx5090-cu128.lock.txt`. `uv.lock` is
never a tested or dependency input. The reviewed plan path
`docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md`
is also a tested/source input. `plan-binding.json` records its current size/hash
and the concrete commit returned by
`git log -n 1 --format=%H -- <plan-path>`; that commit must be an ancestor of
both `P` and `E`, and the plan blob at that commit must equal the tested plan
bytes. The wrapper discovers this binding; callers do not supply a plan commit.

Use these exact domain criteria and reject `coverage`, `freshness`,
`artifact_bound_correctness`, or any missing, extra, renamed, or duplicated
criterion. Stable keys map one-to-one to the labels in the pinned installed
files:

```python
CLAIM_CRITERIA_BY_DOMAIN = {
    "code": (
        ("execution", "execution"),
        ("input_output_behavior", "input/output behavior"),
        ("boundary_failure_behavior", "boundary/failure behavior"),
        ("regression_coverage", "regression coverage"),
        ("configuration_reachability", "configuration reachability"),
        ("reproducibility", "reproducibility"),
    ),
    "evidence": (
        ("source_authority", "source authority"),
        ("primary_source_status", "primary-source status"),
        ("exact_statement_support", "exact support for the statement"),
        ("quotation_data_fidelity", "quotation or data fidelity"),
        ("provenance", "provenance"),
        ("artifact_revision_currency", "currency for the stated artifact revision"),
        ("material_counterevidence_coverage", "material counterevidence coverage"),
    ),
}

CLAIM_SPECS = (
    {
        "id": "CHK-WAVE0-CONTRACT-COMPLETENESS",
        "domain": "code",
        "severity": "medium",
        "kind": "mechanical",
        "evidence_ids": (
            "wave0-targeted-junit",
            "wave0-subsystem-junit",
            "wave0-full-junit",
        ),
        "statement": "The Wave 0 contract records, validators, and exact migration inventory are complete and mechanically enforced at this artifact revision.",
    },
    {
        "id": "CHK-WAVE0-HISTORICAL-BYTE-PINS",
        "domain": "evidence",
        "severity": "medium",
        "kind": "reproduced_source",
        "evidence_ids": (
            "wave0-historical-inventory-source",
            "wave0-historical-reproduced-source",
        ),
        "statement": "The two historical fixed-ray inventories reproduce all 19 source byte sizes and SHA-256 values at this artifact revision without upgrading their scientific status.",
    },
)

EVIDENCE_LOCATIONS_BY_ID = {
    "wave0-targeted-junit": "verification-evidence/wave-0/{evidence_short}/targeted.xml",
    "wave0-subsystem-junit": "verification-evidence/wave-0/{evidence_short}/subsystem.xml",
    "wave0-full-junit": "verification-evidence/wave-0/{evidence_short}/full.xml",
    "wave0-historical-inventory-source":
        "docs/verification/remediation/historical-fixed-ray-bundles-v1.json",
    "wave0-historical-reproduced-source":
        "verification-evidence/wave-0/{evidence_short}/historical-verification.json",
}

INITIAL_VIEW_IDS = ("code-contract-review", "evidence-source-review")
TARGET4_ADDITIONAL_VIEW_IDS = (
    "boundary-failure-review",
    "provenance-counterevidence-review",
)
TARGET8_ADDITIONAL_VIEW_IDS = (
    "configuration-reachability-review",
    "historical-source-adversary",
    "path-privacy-adversary",
    "reproducibility-review",
)
VIEW_IDS_BY_TARGET = {
    2: INITIAL_VIEW_IDS,
    4: INITIAL_VIEW_IDS + TARGET4_ADDITIONAL_VIEW_IDS,
    8: (
        INITIAL_VIEW_IDS
        + TARGET4_ADDITIONAL_VIEW_IDS
        + TARGET8_ADDITIONAL_VIEW_IDS
    ),
}
INITIAL_REVIEW_PATHS = (
    "reviews/code-contract-review.json",
    "reviews/evidence-source-review.json",
)
TARGET4_ADDITIONAL_REVIEW_PATHS = (
    "reviews/escalation/boundary-failure-review.json",
    "reviews/escalation/provenance-counterevidence-review.json",
)
TARGET8_ADDITIONAL_REVIEW_PATHS = (
    "reviews/escalation/configuration-reachability-review.json",
    "reviews/escalation/historical-source-adversary.json",
    "reviews/escalation/path-privacy-adversary.json",
    "reviews/escalation/reproducibility-review.json",
)
REVIEW_PATHS_BY_TARGET = {
    2: INITIAL_REVIEW_PATHS,
    4: INITIAL_REVIEW_PATHS + TARGET4_ADDITIONAL_REVIEW_PATHS,
    8: (
        INITIAL_REVIEW_PATHS
        + TARGET4_ADDITIONAL_REVIEW_PATHS
        + TARGET8_ADDITIONAL_REVIEW_PATHS
    ),
}
ADJUDICATOR_PATHS = (
    "reviews/adjudicators/CHK-WAVE0-CONTRACT-COMPLETENESS.json",
    "reviews/adjudicators/CHK-WAVE0-HISTORICAL-BYTE-PINS.json",
)
ALLOWED_ESCALATION_TRIGGERS = (
    "criterion_disagreement",
    "high_dispersion",
    "small_margin",
)
GENERIC_PUBLIC_PATHS = (
    "commands/full.json",
    "commands/subsystem.json",
    "commands/targeted.json",
    "dependencies.json",
    "environment.json",
    "full.xml",
    "index.json",
    "plan-binding.json",
    "privacy-transform.json",
    "subsystem.xml",
    "targeted.xml",
)
CANDIDATE_PUBLIC_PATHS = GENERIC_PUBLIC_PATHS + (
    "historical-verification.json",
)
CLOSURE_PUBLIC_PATHS_BY_TARGET = {
    2: (
        GENERIC_PUBLIC_PATHS
        + ("historical-verification.json",)
        + REVIEW_PATHS_BY_TARGET[2]
        + ADJUDICATOR_PATHS
    ),
    4: (
        GENERIC_PUBLIC_PATHS
        + ("historical-verification.json",)
        + REVIEW_PATHS_BY_TARGET[4]
        + ADJUDICATOR_PATHS
    ),
    8: (
        GENERIC_PUBLIC_PATHS
        + ("historical-verification.json",)
        + REVIEW_PATHS_BY_TARGET[8]
        + ADJUDICATOR_PATHS
    ),
}
```

The normal branch has exactly the two independent calibrated
`INITIAL_VIEW_IDS`, `escalation_triggers=[]`, and `escalation_target=2`. If any
initial view records `small_margin`, `high_dispersion`, or
`criterion_disagreement`, the exact applicable trigger set is retained, target
becomes 4, and both `TARGET4_ADDITIONAL_VIEW_IDS` are mandatory. If criterion
disagreement remains unresolved after four views, target becomes 8,
`criterion_disagreement` remains present, and all four
`TARGET8_ADDITIONAL_VIEW_IDS` are mandatory. No target 3, 5, 6, or 7 and no
subset of an escalation tier is valid. An unresolved disagreement after eight
views is `INCONCLUSIVE` with an obligation. The installed contract defines no
numeric trigger threshold, so review records declare applicable triggers and
the validator enforces escalation rather than inventing a cutoff.

Candidate `A` is the literal claim statement; candidate `B` is its explicit
negation. The initial views provide the complete ordered `AB`/`BA` pairwise
grid; escalation views add independent criterion scores. For every criterion,
the aggregate score is exactly the arithmetic mean of that criterion across all
2, 4, or 8 required views, with no weighting or rounding before serialization.
Every aggregate, view, and match score uses the exact criterion keys for that
claim's domain. Each claim has exactly one indexed `verifier-adjudicator` record
linked to all branch-required view IDs, its literal eligible evidence IDs, and
its public result location. `index.json` is a structural gate prerequisite, not
claim evidence and never appears in an adjudicator's `evidence_ids`. A recorded
conflict or missing eligible evidence yields `INCONCLUSIVE` with a concrete open
obligation and abstaining adjudicator; it is never resolved by vote. A missing
required review/adjudicator file fails bundle construction and cannot be
silently replaced.

The evidence index's `files` field is the canonical ASCII-path-sorted exact
`{path,kind,size_bytes,sha256}` inventory of every public path except
`index.json` itself. Its path set must equal `CANDIDATE_PUBLIC_PATHS` minus the
index for candidate stage or exactly one
`CLOSURE_PUBLIC_PATHS_BY_TARGET[target]` minus the index for closure stage.
Validation rejects any extra/eleventh generic payload, the wrong branch review
set, an omitted review, any unhashed public byte, or any indexed byte not
present in the detached map.

**Files:**
- Create: `docs/verification/remediation/verification-contract-v1.json`
- Create: `docs/verification/remediation/remediation-evidence-v1.schema.json`
- Create: `tools/remediation_evidence.py`
- Create: `tools/build_wave0_evidence.py`
- Create: `tests/test_remediation_evidence.py`
- Modify: `tests/test_artifacts.py`
- Modify: `tests/test_experiment_support.py`

**Interfaces:**
- Produces `build_evidence_index(*, repo_root, wave, evidence_stage, tested_git_head, implementation_parent_git_head, command_records, source_config_paths, tested_input_policy, environment_record_bytes, dependency_input_paths, public_junit_bytes) -> dict[str, object]`; callers never supply a tested-input list.
- Produces `validate_evidence_index(payload, *, repo_root, actual_head) -> None`.
- Produces `parse_junit(path) -> dict[str, object]` using XML testcase IDs, not console text.
- Produces frozen `PreparedEvidenceFile(path: PurePosixPath, data: bytes)` and `PreparedEvidenceBundle(output_dir: PurePosixPath, files: tuple[PreparedEvidenceFile, ...])`; `prepare_evidence_bundle(...)` validates all bytes in memory and `publish_evidence_bundle(...)` is the only writer.
- Freezes generic CLI `tools/remediation_evidence.py run-junit --record PATH --junit PATH -- ARGV`, `tools/remediation_evidence.py validate INDEX --cwd ROOT`, and `tools/remediation_evidence.py run-verification-gate --snapshot PATH --root DIR -- <start|validate> ARGS`; there is deliberately no generic build CLI and no path-return gate command.
- Freezes executable wrapper `tools/build_wave0_evidence.py build --stage STAGE --tested-head SHA --implementation-parent SHA --raw-dir PATH --output-dir PATH`, `review-context-sha --tested-head SHA --implementation-parent SHA --raw-dir PATH`, `review-target --tested-head SHA --implementation-parent SHA --raw-dir PATH`, `validate-reviews --tested-head SHA --implementation-parent SHA --raw-dir PATH`, and `populate-ledger --ledger PATH --closure-index PATH`; later waves own analogous wrappers and import the generic builder.
- Candidate rule: `tested_git_head == implementation_parent_git_head == actual_head`.
- Closure rule: `tested_git_head == actual_head`, `git rev-parse actual_head^ == implementation_parent_git_head`, and every parent-to-child diff path starts with `f"docs/verification/evidence/{payload['wave']}/"`.

- [ ] **Step 1: Write schema and unknown-field RED tests**

```python
def test_evidence_index_rejects_unknown_and_missing_fields(valid_index):
    unknown = copy.deepcopy(valid_index)
    unknown["surprise"] = True
    with pytest.raises(ValueError, match="unknown evidence-index field"):
        validate_evidence_index(unknown, repo_root=ROOT, actual_head=HEAD)
    missing = copy.deepcopy(valid_index)
    del missing["tested_input_inventory_sha256"]
    with pytest.raises(ValueError, match="missing evidence-index field"):
        validate_evidence_index(missing, repo_root=ROOT, actual_head=HEAD)
```

- [ ] **Step 2: Write parent/child semantics RED tests**

```python
def test_candidate_and_closure_heads_cannot_be_swapped(candidate_index, closure_index):
    candidate_index["tested_git_head"] = EVIDENCE_CHILD_HEAD
    with pytest.raises(ValueError, match="candidate head"):
        validate_evidence_index(candidate_index, repo_root=ROOT, actual_head=IMPLEMENTATION_HEAD)
    closure_index["implementation_parent_git_head"] = EVIDENCE_CHILD_HEAD
    with pytest.raises(ValueError, match="implementation parent"):
        validate_evidence_index(closure_index, repo_root=ROOT, actual_head=EVIDENCE_CHILD_HEAD)
```

Use a temporary two-commit Git repository in the test; do not mock ancestry or diff output.

- [ ] **Step 3: Write JUnit/environment/tested-input RED tests**

The schema has exactly the approved root fields and no others:

```python
ROOT_FIELDS = {
    "schema_version", "wave", "evidence_stage", "tested_git_head",
    "implementation_parent_git_head", "platform", "environment_record",
    "dependency_versions", "dependency_inputs", "tested_input_policy",
    "tested_input_inventory_sha256", "commands", "source_config_bindings",
    "reviewed_plan_binding", "verification_contract_binding", "files",
}
JUNIT_FIELDS = {
    "path", "size_bytes", "sha256", "tests", "failures", "errors",
    "skipped", "time_seconds", "testcase_id_sha256", "skipped_cases",
}
```

Each sanitized public command record under `commands/` has exactly `schema_version`,
`id`, `argv`, `cwd_rel`, `interpreter`, `env_allowlist`, `started_utc`,
`ended_utc`, `exit_code`, and `junit`. `argv` is an ordered JSON array of exact
tokens, never a shell string. The index's `commands` field is the sorted exact
`{path,size_bytes,sha256}` inventory of those three records. The parser
constructs testcase IDs as `classname + "::" + name`, rejects absent/duplicate
IDs, Boolean counts, nonzero failures/errors/exit, count disagreement,
negative/nonfinite time, missing files, and any actual skip not in the frozen
per-suite allowlist.

Freeze the allowlist in `tools/build_wave0_evidence.py` exactly as follows. Allowed capability skips may be absent when the host supports the capability; every actual skip must match both ID and reason byte-for-byte.

```python
SKIP_ALLOWLIST_BY_SUITE = {
    "targeted": {},
    "subsystem": {},
    "full": {
        "tests.test_artifacts::test_finalize_rejects_a_declared_symlink":
            "capability unavailable: symbolic_link",
        "tests.test_artifacts::test_finalize_rejects_a_declared_file_with_an_external_hard_link":
            "capability unavailable: hard_link",
        "tests.test_artifacts::test_finalize_rejects_an_external_hard_link_to_core_config":
            "capability unavailable: hard_link",
        "tests.test_artifacts::test_finalize_rejects_duplicate_file_identity_within_inventory":
            "capability unavailable: hard_link",
        "tests.test_experiment_support::test_validated_renderer_status_rejects_a_publication_symlink_escape":
            "capability unavailable: symbolic_link",
        "tests.test_cuda_backend::test_pinned_cuda_worker_runs_first_job_with_determinism_environment":
            "requires explicit dedicated CUDA-lane opt-in",
    },
}
```

Normalize the two dynamic skip sites before the evidence run:

```python
try:
    os.link(source_path, external_link_path)
except (NotImplementedError, OSError):
    pytest.skip("capability unavailable: hard_link")

try:
    publication_link.symlink_to(external_target, target_is_directory=True)
except (NotImplementedError, OSError):
    pytest.skip("capability unavailable: symbolic_link")
```

Freeze `tested_input_policy` as a closed object with exactly `schema_version`,
`selection_rules`, `exclusion_rules`, and `inputs`. `schema_version` is
`wave-0-source-config-theory-tools-tests-v1`; `selection_rules` is the ordered
list `prefix:src/`, `prefix:tests/`, `prefix:Theory/`, `prefix:tools/`,
`top_level_suffix:.py`, `exact:pyproject.toml`, `exact:.gitignore`,
`exact:.gitattributes`,
`exact:environments/cuda-rtx5090-cu128.lock.txt`,
`exact:docs/audits/2026-08-11-post-fixed-ray-deep-audit.md`,
`exact:docs/superpowers/specs/2026-08-11-scientific-integrity-remediation-program-design.md`,
`exact:docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md`,
`exact:docs/verification/remediation/verification-contract-v1.json`,
and `prefix:docs/verification/remediation/`. `exclusion_rules` is the ordered
list `prefix:docs/verification/evidence/`,
`prefix:verification-evidence/`, `prefix:.verification/`,
`prefix:.pytest_cache/`, `prefix:.pytest-`. `inputs` contains every selected
`{path,size_bytes,sha256}` record. The canonical resolver calls
`git ls-files -z` itself, rejects any matching untracked nonignored path,
case-fold collision, symlink/reparse input, missing file, caller-supplied
omission, or unsorted inventory, and hashes canonical compact JSON of `inputs`
for `tested_input_inventory_sha256`. This same resolver runs at candidate `P`
and closure `E`; excluding evidence output is what makes the tested
source/config inventory comparable across the evidence-only child.

`source_config_bindings` is the sorted exact subset containing the approved
design, audit report, reviewed Wave 0 plan, every file under
`docs/verification/remediation/` (including the verification snapshot),
`tools/remediation_evidence.py`, `tools/build_wave0_evidence.py`,
`tests/test_remediation_contracts.py`, `tests/test_remediation_evidence.py`,
`tests/test_artifacts.py`, `tests/test_experiment_support.py`,
`pyproject.toml`, and both Git attribute/ignore files. `dependency_inputs` is
exactly `pyproject.toml`,
`environments/cuda-rtx5090-cu128.lock.txt`, and
`docs/verification/remediation/verification-contract-v1.json`, in that order.
`uv.lock` is prohibited. Tests add an untracked matching source file, omit each
required binding in turn, edit one dependency byte, inject `uv.lock`, change
the plan commit/blob relationship, and change one selected tracked file in a
temporary Git repository; construction/validation must reject each case.

The normalized environment record has schema `remediation-environment-v1` and
exact fields `platform`, `interpreter`, `dependency_versions`,
`dependency_inputs`, and `environment_variables`. It records `os`, `release`,
`architecture`, and Python implementation/version; sorted installed `numpy`,
`scipy`, `pytest`, and every installed pytest plugin distribution; interpreter
size/SHA; dependency input size/SHA; and these exact environment keys with
either their string value or JSON null: `CUDA_VISIBLE_DEVICES`,
`MULTIAGENTELBO_RUN_CUDA_TESTS`, `VFE3_TEST_DEVICE`,
`CUBLAS_WORKSPACE_CONFIG`, `PYTHONHASHSEED`, and `PYTHONPATH`. The run requires
`CUDA_VISIBLE_DEVICES="-1"`, `PYTHONHASHSEED="0"`, and all CUDA opt-in/device
variables absent. Platform, interpreter, dependency, environment, tested-input,
source/config, plan, snapshot, review-context, or command drift invalidates the
index.

Freeze `review-context-sha` as a closed canonical payload, not a concatenation
of ad hoc digests:

```python
REVIEW_CONTEXT_FIELDS = (
    "schema_version",
    "tested_git_head",
    "implementation_parent_git_head",
    "evidence_diff_inventory",
    "candidate_evidence_inventory",
    "raw_command_inventory",
    "raw_junit_inventory",
    "tested_input_inventory",
    "source_config_inventory",
    "dependency_inventory",
    "environment_inventory",
    "reviewed_plan_bytes",
    "verification_snapshot_bytes",
    "historical_source_bytes",
    "historical_reproduced_source",
    "claim_specs",
    "public_path_contracts",
)
```

The payload has exactly those fields. `schema_version` is
`wave-0-review-context-v1`. The two head fields contain full 40-hex `E` and
`P` and the command independently proves `E^=P`. Every inventory is an
ASCII-path-sorted array of closed `{path,size_bytes,sha256}` records.
`evidence_diff_inventory` is the complete `P..E` path-and-hash inventory and
contains only the candidate evidence directory.
`candidate_evidence_inventory` revalidates and inventories every candidate
public byte, including its index. `raw_command_inventory` and
`raw_junit_inventory` cover the exact three closure suite pairs.
`tested_input_inventory`, `source_config_inventory`,
`dependency_inventory`, and `environment_inventory` are independently resolved
from current bytes and the six-key CPU environment; no caller supplies them.
`reviewed_plan_bytes` and `verification_snapshot_bytes` are the exact
path/size/hash records, with the plan commit and snapshot active-file inventory
included in their closed subobjects. `historical_source_bytes` binds the
19-record source inventory.

Before computing the digest, the command creates exactly
`$rawDir/detached/historical-verification.json` in already existing ignored raw
staging and only if absent. Its closed schema is
`wave-0-historical-verification-v1` with exact fields `schema_version`,
`tested_git_head`, `implementation_parent_git_head`, `source_inventory`,
`observations`, and `status_boundary`. `observations` is the 19-entry sorted
`{path,expected_size_bytes,observed_size_bytes,expected_sha256,observed_sha256,match}`
array produced by rereading the historical sources; every `match` must be true.
`status_boundary` is the literal statement that the reproduced bytes establish
compatibility and byte-pinning only, not current scientific promotion. The file
is privacy-transformed public form, contains no absolute path, and is the exact
`reproduced_source` reviewed by the evidence views.
`historical_reproduced_source` binds its path/size/hash.
`claim_specs` hashes canonical `CLAIM_SPECS` and criteria mappings.
`public_path_contracts` hashes `CANDIDATE_PUBLIC_PATHS` and all three
`CLOSURE_PUBLIC_PATHS_BY_TARGET` branches.

The command writes canonical `$rawDir/review-context.json` only after validating
all members and prints
`sha256(canonical_json_bytes(review_context_payload)).hexdigest()`. It never
creates a final evidence directory or index. `validate-reviews` rereads the
context and detached historical file. Closure preparation must copy the
detached `historical-verification.json` byte-for-byte; regeneration, a second
privacy pass that changes bytes, or a differing public hash fails before
publication.

Add a parameterized mutation test over every name in `REVIEW_CONTEXT_FIELDS`
and every array/subobject member: mutate one byte, path, size, hash, head,
candidate file, raw command/JUnit, input, environment value, plan/snapshot
record, historical observation, claim spec, or public-path contract and require
context validation failure or a different digest. A control recomputes the
unchanged payload twice and requires byte-identical canonical JSON and digest.

Add these concrete controls (fixtures create a temporary two-commit repository and valid raw records/XML):

```python
def test_builder_discovers_inputs_and_rejects_matching_untracked_file(repo, raw):
    extra = repo / "src" / "untracked.py"
    extra.parent.mkdir(exist_ok=True)
    extra.write_text("VALUE = 1\n", encoding="utf-8")
    destination = repo / "docs/verification/evidence/wave-0/aaaaaaaaaaaa"
    with pytest.raises(ValueError, match="untracked tested input"):
        prepare_evidence_bundle(**raw, repo_root=repo, output_dir=destination)
    assert not destination.exists()


@pytest.mark.parametrize("kind", ["command", "dependency", "environment",
                                  "plan", "review", "adjudicator", "junit"])
def test_privacy_transform_is_total_idempotent_and_semantic(
    kind, raw_public, privacy_context
):
    first, mapping = privacy_transform_bytes(
        raw_public[kind], kind=kind, privacy_context=privacy_context
    )
    second, _ = privacy_transform_bytes(
        first, kind=kind, privacy_context=privacy_context
    )
    assert first == second
    assert mapping["raw_sha256"] == sha256(raw_public[kind]).hexdigest()
    assert mapping["public_sha256"] == sha256(first).hexdigest()
    assert_private_tokens_absent(first, privacy_context=privacy_context)
    assert_public_semantics_equal(
        kind, raw_public[kind], first, privacy_context=privacy_context
    )


def test_privacy_transform_replaces_every_absolute_component(
    valid_raw_command, privacy_context
):
    raw = copy.deepcopy(valid_raw_command)
    raw["interpreter"]["path"] = r"C:\Python314\python.exe"
    raw["cwd"] = r"C:\Users\example\private-repository"
    raw["argv"] = [
        r"C:\Python314\python.exe",
        r"--root=D:\private\cache",
        r"\\server\share\fixture.json",
        r"\\?\C:\device\fixture.json",
        "/opt/tool/cache",
    ]
    raw["env_allowlist"]["PYTHONPATH"] = (
        r"C:\private\src;D:\vendor\pkg;\\server\share\lib"
    )
    raw_bytes = canonical_json_bytes(raw)

    public, mapping = privacy_transform_bytes(
        raw_bytes, kind="command", privacy_context=privacy_context
    )
    payload = json.loads(public)
    pythonpath_parts = payload["env_allowlist"]["PYTHONPATH"].split(";")

    assert payload["interpreter"]["path"] == "<CPU_PYTHON>"
    assert payload["argv"][0] == "<CPU_PYTHON>"
    assert re.fullmatch(r"--root=<ABS_PATH_\d{4}>", payload["argv"][1])
    assert all(
        re.fullmatch(r"<ABS_PATH_\d{4}>", value)
        for value in payload["argv"][2:]
    )
    assert len(pythonpath_parts) == 3
    assert len(set(pythonpath_parts)) == 3
    assert all(
        re.fullmatch(r"<ABS_PATH_\d{4}>", value)
        for value in pythonpath_parts
    )
    assert_no_literal_absolute_path(public)
    assert mapping["raw_sha256"] == sha256(raw_bytes).hexdigest()
    assert mapping["public_sha256"] == sha256(public).hexdigest()
    assert privacy_transform_bytes(
        public, kind="command", privacy_context=privacy_context
    )[0] == public


def _review_context_leaf_paths(value, prefix=()):
    if isinstance(value, dict):
        for key in sorted(value):
            yield from _review_context_leaf_paths(value[key], prefix + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _review_context_leaf_paths(item, prefix + (index,))
    else:
        yield prefix


def _mutated_review_context_scalar(value):
    if value is None:
        return "mutated"
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, float):
        return value + 1.0
    if isinstance(value, str):
        return value + "!"
    raise TypeError(f"unsupported review-context scalar: {type(value)!r}")


def _replace_review_context_member(payload, path):
    cursor = payload
    for component in path[:-1]:
        cursor = cursor[component]
    cursor[path[-1]] = _mutated_review_context_scalar(cursor[path[-1]])


def test_review_context_digest_binds_every_member(valid_review_context):
    assert set(valid_review_context) == set(REVIEW_CONTEXT_FIELDS)
    canonical = canonical_json_bytes(valid_review_context)
    digest = sha256(canonical).hexdigest()
    assert canonical_json_bytes(valid_review_context) == canonical
    assert sha256(canonical_json_bytes(valid_review_context)).hexdigest() == digest

    paths = tuple(_review_context_leaf_paths(valid_review_context))
    assert {path[0] for path in paths} == set(REVIEW_CONTEXT_FIELDS)
    for path in paths:
        mutated = copy.deepcopy(valid_review_context)
        _replace_review_context_member(mutated, path)
        mutated_bytes = canonical_json_bytes(mutated)
        assert mutated_bytes != canonical, path
        assert sha256(mutated_bytes).hexdigest() != digest, path


@pytest.mark.parametrize(
    ("completed_view_count", "triggers", "unresolved_after_four", "expected"),
    [
        (2, (), False, 2),
        (2, ("small_margin",), False, 4),
        (2, ("high_dispersion",), False, 4),
        (2, ("criterion_disagreement",), False, 4),
        (4, ("small_margin",), False, 4),
        (4, ("criterion_disagreement",), True, 8),
        (8, ("criterion_disagreement",), True, 8),
    ],
)
def test_review_target_transition_is_exact(
    completed_view_count, triggers, unresolved_after_four, expected
):
    assert required_review_target(
        completed_view_count=completed_view_count,
        retained_triggers=triggers,
        unresolved_criterion_disagreement=unresolved_after_four,
    ) == expected


def test_review_target_rejects_non_tier_counts_and_unknown_triggers():
    with pytest.raises(ValueError, match="completed view count"):
        required_review_target(
            completed_view_count=3,
            retained_triggers=(),
            unresolved_criterion_disagreement=False,
        )
    with pytest.raises(ValueError, match="escalation trigger"):
        required_review_target(
            completed_view_count=2,
            retained_triggers=("majority_vote",),
            unresolved_criterion_disagreement=False,
        )


@pytest.mark.parametrize("target", [2, 4, 8])
def test_criterion_aggregates_are_exact_arithmetic_means(target):
    criterion_keys = tuple(
        key for key, _label in CLAIM_CRITERIA_BY_DOMAIN["code"]
    )
    view_scores = tuple(
        {
            key: (view_index + criterion_index) % 21
            for criterion_index, key in enumerate(criterion_keys)
        }
        for view_index in range(target)
    )
    expected = {
        key: sum(view[key] for view in view_scores) / target
        for key in criterion_keys
    }
    assert compute_criterion_aggregates(
        view_scores, criterion_keys=criterion_keys
    ) == expected


def test_review_tiers_and_closure_path_sets_are_exact():
    assert set(VIEW_IDS_BY_TARGET) == {2, 4, 8}
    assert set(REVIEW_PATHS_BY_TARGET) == {2, 4, 8}
    assert set(CLOSURE_PUBLIC_PATHS_BY_TARGET) == {2, 4, 8}
    assert {
        target: len(paths)
        for target, paths in VIEW_IDS_BY_TARGET.items()
    } == {2: 2, 4: 4, 8: 8}
    assert {
        target: len(paths)
        for target, paths in REVIEW_PATHS_BY_TARGET.items()
    } == {2: 2, 4: 4, 8: 8}
    assert {
        target: len(paths)
        for target, paths in CLOSURE_PUBLIC_PATHS_BY_TARGET.items()
    } == {2: 16, 4: 18, 8: 22}
    for target in (2, 4, 8):
        assert len(set(VIEW_IDS_BY_TARGET[target])) == target
        assert len(set(REVIEW_PATHS_BY_TARGET[target])) == target
        assert len(set(CLOSURE_PUBLIC_PATHS_BY_TARGET[target])) == {
            2: 16, 4: 18, 8: 22
        }[target]
        assert set(REVIEW_PATHS_BY_TARGET[target]).issubset(
            CLOSURE_PUBLIC_PATHS_BY_TARGET[target]
        )
        assert set(ADJUDICATOR_PATHS).issubset(
            CLOSURE_PUBLIC_PATHS_BY_TARGET[target]
        )
        assert "historical-verification.json" in (
            CLOSURE_PUBLIC_PATHS_BY_TARGET[target]
        )


@pytest.mark.parametrize("field", sorted(ROOT_FIELDS))
def test_missing_index_field_fails_before_write(valid_kwargs, field, tmp_path):
    prepared = prepare_evidence_bundle(**valid_kwargs)
    payload = json.loads(next(f.data for f in prepared.files if f.path.name == "index.json"))
    del payload[field]
    output = tmp_path / "public"
    with pytest.raises(ValueError, match="missing evidence-index field"):
        publish_test_payload(payload, prepared, output)
    assert not output.exists()


def test_wrapper_exposes_only_frozen_commands():
    assert wave0_parser().parse_args(["build", "--stage", "candidate",
        "--tested-head", "a" * 40, "--implementation-parent", "a" * 40,
        "--raw-dir", ".verification/raw", "--output-dir", "docs/verification/evidence/wave-0/aaaaaaaaaaaa"]).command == "build"
    assert wave0_parser().parse_args(["populate-ledger", "--ledger",
        ".verification/wave-0/final-ledger.json", "--closure-index",
        "verification-evidence/wave-0/bbbbbbbbbbbb/index.json"]).command == "populate-ledger"
    assert remediation_parser().parse_args(["run-verification-gate",
        "--snapshot", "docs/verification/remediation/verification-contract-v1.json",
        "--root", r"C:\Users\example\.codex\skills\verification",
        "--", "start"]).command == (
            "run-verification-gate"
        )
    assert wave0_parser().parse_args(["review-context-sha",
        "--tested-head", "b" * 40, "--implementation-parent", "a" * 40,
        "--raw-dir", ".verification/raw"]).command == "review-context-sha"
    assert wave0_parser().parse_args(["review-target",
        "--tested-head", "b" * 40, "--implementation-parent", "a" * 40,
        "--raw-dir", ".verification/raw"]).command == "review-target"
    assert wave0_parser().parse_args(["validate-reviews",
        "--tested-head", "b" * 40, "--implementation-parent", "a" * 40,
        "--raw-dir", ".verification/raw"]).command == "validate-reviews"


EXPECTED_VERIFICATION_FILES = (
    ("SKILL.md", 4653, "dc5dec74ac5c3bae712b2bdc16c71383d67923ef108e6d7f9d278a6a950b17b1"),
    ("references/contract.md", 6128, "bef6d266c94e2da962b8d1899846ea8fed83ff8f30e7376f87e0cfbe22b8de01"),
    ("references/criteria-code.md", 963, "4febab87f009dd8ab60a381600f8e18e62322d86151f7aa5ee6a346ae87f5152"),
    ("references/criteria-evidence.md", 908, "7dc751859c962f3e34a9bfff9ca981684a606dae8d49a2e5e6c3362a1d3d5990"),
    ("references/criteria-experiment.md", 893, "2a540b9a92e1c01ce6276d89dc603c7e2f48c803b8cf83dca776968bae8bafb1"),
    ("references/criteria-general.md", 1082, "dfa5236f26259b92a8a3507a4cc928fa836951f92e829526052fa412a4932729"),
    ("references/criteria-math.md", 923, "b604f4d9ef8ed3fbafc15589620955dba88128b38c5c5c88c3343f059d769979"),
    ("schemas/claim-ledger.schema.json", 9897, "e96958dc6606be521ec103a439c5a3c0e21f5417c6a1d445ae0401d5fabb6478"),
    ("scripts/verification_gate.py", 57702, "a8a799496762910c463ecc179a4d63dc40107fcbe81553add189de7ed1ce4c95"),
)


def test_verification_snapshot_and_explicit_root_are_exact(snapshot, skill_root):
    observed = tuple(
        (item["path"], item["size_bytes"], item["sha256"])
        for item in snapshot["files"]
    )
    assert observed == EXPECTED_VERIFICATION_FILES
    assert snapshot["canonical_relative_root"] == ".codex/skills/verification"
    verified = resolve_verified_verification_gate(snapshot, root=skill_root)
    assert verified.path == (
        skill_root / "scripts/verification_gate.py"
    )
    assert verified.source_bytes == (skill_root / "scripts/verification_gate.py").read_bytes()
    with pytest.raises(ValueError, match="canonical .codex verification root"):
        resolve_verified_verification_gate(
            snapshot, root=skill_root.parents[2] / ".claude/skills/verification"
        )
```

- [ ] **Step 4: Run the RED suite**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_remediation_evidence.py -q -p no:cacheprovider --basetemp=.pytest-wave0-task4-red
```

Expected: FAIL because `tools.remediation_evidence` and the JSON schema do not exist.

- [ ] **Step 5: Implement immutable canonical index construction and validation**

Use these exact immutable carriers and canonical serializer:

```python
@dataclass(frozen=True, slots=True)
class PreparedEvidenceFile:
    path: PurePosixPath
    data: bytes


@dataclass(frozen=True, slots=True)
class PreparedEvidenceBundle:
    output_dir: PurePosixPath
    files: tuple[PreparedEvidenceFile, ...]


def canonical_json_bytes(payload: object) -> bytes:
    return (
        json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
        + "\n"
    ).encode("utf-8")
```

`prepare_evidence_bundle` performs this exact order without creating a
directory: validate arguments and the `P/P` or `E/P` relationship; resolve the
canonical tested-input policy; validate the reviewed plan binding and pinned
verification snapshot; read each raw command/JUnit once; parse and allowlist
raw XML; independently construct raw environment, dependency, and plan-binding
JSON in memory; construct historical verification in memory only for candidate
stage; and, for closure, read the byte-fixed detached
`historical-verification.json`, exact branch-required reviews, and two
adjudicator records already validated against the detached review-context
digest. It uses one executable
`privacy_transform_bytes(data, *, kind, privacy_context)` implementation for
JSON and XML.

`privacy_context` first validates the raw interpreter record against
`C:\Python314\python.exe`, its version, size, and SHA, then maps that exact path
to `<CPU_PYTHON>`. It maps the resolved repository and user-profile prefixes to
`<REPO_ROOT>` and `<USER_HOME>`. A structural path walker then processes every
path-bearing JSON location and every XML text/attribute: interpreter path;
`cwd`; each argv token; the right-hand side of `--option=VALUE` tokens; every
environment value; every component of `PYTHONPATH` split with the recorded
platform path separator; dependency, plan, snapshot, review/result, and JUnit
path fields; Windows drive, UNC, and device paths; and POSIX absolute paths.
Known prefixes retain only a normalized relative suffix after their placeholder.
Every other distinct absolute component is ordered by normalized case-folded
value and replaced by `<ABS_PATH_0001>`, `<ABS_PATH_0002>`, and so on. Longest
prefix wins, separators in public suffixes are `/`, and substitution occurs on
parsed components rather than arbitrary substrings. Hostname maps to
`<HOSTNAME>`; JSON keys or XML attributes `pid`, `process_id`, and
`worker_pid` map to `<PID>`.

The public interpreter is exactly `<CPU_PYTHON>`. Public argv and environment
records retain token/key order and nonpath text, but every absolute component,
including every absolute `PYTHONPATH` entry, is a placeholder form. Public JSON
and XML may contain only `<CPU_PYTHON>`, `<REPO_ROOT>`, `<USER_HOME>`,
`<HOSTNAME>`, `<PID>`, and the numbered `<ABS_PATH_NNNN>` family in place of
private values; a Windows/POSIX absolute-path grammar scan must find zero
literal system paths in every public byte.

A second transform is byte-identical. Semantic validation parses raw and public
forms, applies the same structural normalization to the raw form, and requires
exact equality with the public form, including argv cardinality/order,
environment keys/path-list cardinality, dependency hashes, plan/snapshot
binding, review scores/verdicts/evidence IDs, and JUnit testcase IDs, counts,
outcomes, and skip reasons. Tests inject absolute drive, UNC, device, POSIX,
`--option=ABS`, interpreter, cwd, review/result, XML-property, and multi-entry
`PYTHONPATH` values; each literal must disappear, placeholders must be stable,
and a nonpath-character mutation must still fail semantic comparison.

The builder records one sorted closed mapping per external, generated, or raw
preimage in `privacy-transform.json` with exactly `raw_relative_path`,
`raw_sha256`, `public_path`, `public_sha256`, and `transforms`. This includes
all raw command records, JUnit XML, environment/dependency/plan/historical JSON,
and every branch-required review/adjudicator. Each record preserves the full
raw/public byte hashes and names the structural component transformations
without embedding a raw absolute value. `index.json` and
`privacy-transform.json` are
generated only from already transformed public records, have no private raw
preimage, and are separately scanned for every private token before hashing.
Thus every raw input has a public-hash mapping and every public byte is
privacy-validated without a self-referential hash cycle.

Only after all transforms does the builder construct the exact public virtual
map, `index.json` last, validate the closed path set and every size/hash, and
return `PreparedEvidenceBundle`. Raw staging remains only below ignored
`.verification/raw/`. No raw command, review, dependency, environment, or XML
byte is copied directly.

`publish_evidence_bundle` validates that the destination is repository-relative,
absent, non-reparse, and exactly the prepared directory. It revalidates the
complete detached virtual set before its sole publication write, creates one
sibling temporary directory, writes each already-prepared byte, rereads/hashes
every file, writes `index.json` last, and atomically renames the sibling. Any
prevalidation failure leaves the destination and parent byte-identical. Any
write failure removes only the exact new sibling and leaves no destination.

Freeze the generic CLI dispatch exactly:

```python
run = subparsers.add_parser("run-junit")
run.add_argument("--record", required=True)
run.add_argument("--junit", required=True)
run.add_argument("argv", nargs=argparse.REMAINDER)

validate = subparsers.add_parser("validate")
validate.add_argument("index")
validate.add_argument("--cwd", default=".")

gate = subparsers.add_parser("run-verification-gate")
gate.add_argument("--snapshot", required=True)
gate.add_argument("--root", required=True)
gate.add_argument("argv", nargs=argparse.REMAINDER)
```

`run-junit` requires the first remainder token to be `--`, strips only that separator, requires exact interpreter token `C:\Python314\python.exe`, requires an exact `--junitxml=<raw path>` token, rejects a preexisting record/JUnit, verifies the CPU environment policy before execution, calls `subprocess.run(argv, cwd=repo_root, shell=False, check=False)`, and atomically writes the command record only after exit. Its record has exactly `schema_version="remediation-command-record-v1"`, `id`, `argv`, `cwd_rel="."`, interpreter path/version/size/SHA, the six-key environment allowlist, UTC start/end strings, exit code, and raw JUnit path/size/SHA. It returns the pytest exit code and never derives totals from stdout.

Freeze the Wave 0 wrapper parser exactly:

```python
build = subparsers.add_parser("build")
build.add_argument("--stage", required=True, choices=("candidate", "closure"))
build.add_argument("--tested-head", required=True)
build.add_argument("--implementation-parent", required=True)
build.add_argument("--raw-dir", required=True)
build.add_argument("--output-dir", required=True)

context = subparsers.add_parser("review-context-sha")
context.add_argument("--tested-head", required=True)
context.add_argument("--implementation-parent", required=True)
context.add_argument("--raw-dir", required=True)

target = subparsers.add_parser("review-target")
target.add_argument("--tested-head", required=True)
target.add_argument("--implementation-parent", required=True)
target.add_argument("--raw-dir", required=True)

reviews = subparsers.add_parser("validate-reviews")
reviews.add_argument("--tested-head", required=True)
reviews.add_argument("--implementation-parent", required=True)
reviews.add_argument("--raw-dir", required=True)

populate = subparsers.add_parser("populate-ledger")
populate.add_argument("--ledger", required=True)
populate.add_argument("--closure-index", required=True)
```

The `build` branch contains the literal Wave 0 suite definitions and skip maps,
passes `wave="wave-0"` with parsed arguments to `prepare_evidence_bundle`, then
calls `publish_evidence_bundle` exactly once and `validate_evidence_index` from
disk. It refuses any output other than
`docs/verification/evidence/wave-0/{tested_git_head[:12]}` for candidate or
`verification-evidence/wave-0/{tested_git_head[:12]}` for closure. Candidate
preparation rejects any review input and requires exactly
`CANDIDATE_PUBLIC_PATHS`. Closure preparation rereads
`review-context.json`, requires the exact `REVIEW_PATHS_BY_TARGET[target]` and
two validated adjudicators, copies detached `historical-verification.json`
byte-identically, and requires exactly
`CLOSURE_PUBLIC_PATHS_BY_TARGET[target]`. Any missing, extra, case-aliased,
wrong-tier, regenerated-historical, or preexisting-destination path fails before
write.

`review-target` validates the context and existing review records and prints
only `2`, `4`, or `8`. With only the initial two records, it prints 2 if their
union of `escalation_triggers` is empty and 4 if any allowed trigger is present.
With four records it prints 8 exactly when
`criterion_disagreement` remains unresolved; otherwise it prints 4. Eight is
terminal. It never writes. `validate-reviews` requires the complete selected
tier, both adjudicators, exact trigger retention, and no unselected review path.
It recomputes every aggregate criterion as
`sum(view_scores[name]) / escalation_target` and requires exact numeric equality
in the ledger input; a precomputed or rounded mismatch fails.

The `populate-ledger` branch is executable only after the resolved pinned gate's
`start`. Before opening the closure index, it requires the exact ledger path
`.verification/wave-0/final-ledger.json` and a gate-created object whose fields
are exactly `schema_version`, `mode`, `artifact_revision`, and `claims`, with
`schema_version="1.0"`, `mode="closure"`, a concrete validator-accepted
artifact revision, and `claims=[]`. It then requires live `HEAD=E`, `E^=P`,
an evidence-only `P..E` diff, and revalidates the index, every indexed public
byte, review-context binding, plan binding, snapshot binding, and exact
`CLOSURE_PUBLIC_PATHS_BY_TARGET[target]`. `index.json` must validate first as a
structural prerequisite, but its ID/path is forbidden in every claim's
`evidence`, every adjudicator's `evidence_ids`, and every review's eligible
evidence list.

Population consumes the indexed `CLAIM_SPECS`, tier-selected review scores,
AB/BA matches, trigger set, target, and adjudicator records byte-for-byte; it may
not synthesize or alter a view, criterion, aggregate, verdict, evidence ID,
result location, trigger, target, or obligation. It uses the
gate template's complete artifact revision for both claims and every evidence
entry. The contract-completeness claim is `code` with current `mechanical`
evidence; the historical-byte claim is `evidence` with current
`primary_source` and `reproduced_source` evidence. If every per-claim
target-required view supports, adjudication supports, and eligible evidence is
complete, state is `EVIDENCE_VERIFIED`. Any recorded
conflict or missing eligible evidence is `INCONCLUSIVE` with a nonempty
obligation and abstaining adjudicator. Unresolved criterion disagreement after
four requires target 8; after eight it remains `INCONCLUSIVE`. No `AUD-*` claim
or `REFUTED` state is permitted. Unit tests import the resolved pinned gate validator, prove
`start` followed immediately by `validate` fails on the empty template, then
prove only the populated ledger validates.

Serialize all JSON with `canonical_json_bytes`. Reject literal absolute paths in
public records, unknown placeholders, backslashes in repository-relative public
paths, traversal, case-fold aliases, Boolean numeric fields, unordered
inventories, unhashed bindings, unknown fields, a caller-supplied tested-input
subset, a nonzero command, an unexplained skip, raw/public semantic drift,
review-tier drift, arithmetic-mean drift, or any write-before-validation attempt.

- [ ] **Step 6: Run GREEN, Ruff, and commit**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_remediation_evidence.py -q -p no:cacheprovider --basetemp=.pytest-wave0-task4-green
C:\Python314\python.exe -m ruff check --no-cache tools/remediation_evidence.py tools/build_wave0_evidence.py tests/test_remediation_evidence.py tests/test_artifacts.py tests/test_experiment_support.py
C:\Python314\python.exe -m ruff format --check --no-cache tools/remediation_evidence.py tools/build_wave0_evidence.py tests/test_remediation_evidence.py tests/test_artifacts.py tests/test_experiment_support.py
git add -- docs/verification/remediation/verification-contract-v1.json docs/verification/remediation/remediation-evidence-v1.schema.json tools/remediation_evidence.py tools/build_wave0_evidence.py tests/test_remediation_evidence.py tests/test_artifacts.py tests/test_experiment_support.py
git commit -m "feat: validate remediation evidence indexes"
```

### Task 5: Publish the Wave 0 contract guide and candidate evidence child

**Files:**
- Create: `docs/verification/remediation/README.md`
- Modify: `tests/test_remediation_contracts.py`
- Create at runtime: the `docs/verification/evidence/wave-0/` child directory
  named by the first 12 characters of the actual implementation-parent SHA.

**Interfaces:**
- The guide links all five records, including the pinned verification snapshot,
  the evidence schema, the reviewed Wave 0 plan, the approved design, and the
  audit report.
- It states that Wave 0 closes contract completeness only and remediates none of `AUD-01` through `AUD-22`.
- It documents candidate commit `P`, evidence child `E`, and uncommitted exact-child closure evidence.

- [ ] **Step 1: Write the documentation RED**

```python
def test_remediation_readme_preserves_status_and_revision_boundaries():
    text = README_PATH.read_text(encoding="utf-8")
    for phrase in (
        "Wave 0 does not remediate an audit defect",
        "producer verification_state is exactly CANDIDATE",
        "historical bundles are never upgraded",
        "candidate evidence",
        "exact-child closure evidence",
    ):
        assert phrase in text
```

- [ ] **Step 2: Run RED, write the guide, and run GREEN**

```powershell
C:\Python314\python.exe -B -m pytest tests\test_remediation_contracts.py -k readme -q -p no:cacheprovider --basetemp=.pytest-wave0-task5-red
C:\Python314\python.exe -B -m pytest tests\test_remediation_contracts.py -q -p no:cacheprovider --basetemp=.pytest-wave0-task5-green
```

The first command must fail on the missing guide; after writing it, the second must pass.

- [ ] **Step 3: Commit the final Wave 0 implementation parent `P`**

```powershell
git add -- docs/verification/remediation/README.md tests/test_remediation_contracts.py
git commit -m "docs: publish remediation contract guide"
git status --porcelain=v1
git rev-parse HEAD
```

Require an empty status and record the resulting full SHA as `P`.

- [ ] **Step 4: Run candidate targeted, subsystem, and full CPU suites at `P`**

Resolve the real implementation SHA, establish the CPU-only environment, and create only the ignored raw staging directory. The durable candidate directory must not exist until the wrapper has prepared and validated every public byte in memory.

```powershell
$ErrorActionPreference = 'Stop'
$implementationSha = (git rev-parse HEAD).Trim()
$implementationShort = $implementationSha.Substring(0, 12)
$rawDir = ".verification/raw/wave-0/$implementationShort/candidate"
$candidateDir = "docs/verification/evidence/wave-0/$implementationShort"
if (Test-Path -LiteralPath $rawDir) { throw "candidate raw directory already exists" }
if (Test-Path -LiteralPath $candidateDir) { throw "candidate evidence directory already exists" }
New-Item -ItemType Directory -Path $rawDir | Out-Null
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/targeted.command.json" --junit "$rawDir/targeted.raw.xml" -- C:\Python314\python.exe -B -m pytest tests/test_remediation_contracts.py tests/test_remediation_evidence.py -q -p no:cacheprovider --basetemp="$rawDir/tmp-targeted" --junitxml="$rawDir/targeted.raw.xml"
if ($LASTEXITCODE -ne 0) { throw "Wave 0 candidate targeted suite failed" }

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/subsystem.command.json" --junit "$rawDir/subsystem.raw.xml" -- C:\Python314\python.exe -B -m pytest tests/test_remediation_contracts.py tests/test_remediation_evidence.py tests/test_shared_scientific_contracts.py tests/test_gaussian_results_document.py -q -p no:cacheprovider --basetemp="$rawDir/tmp-subsystem" --junitxml="$rawDir/subsystem.raw.xml"
if ($LASTEXITCODE -ne 0) { throw "Wave 0 candidate subsystem suite failed" }

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/full.command.json" --junit "$rawDir/full.raw.xml" -- C:\Python314\python.exe -B -m pytest -q -p no:cacheprovider --basetemp="$rawDir/tmp-full" --junitxml="$rawDir/full.raw.xml"
if ($LASTEXITCODE -ne 0) { throw "Wave 0 candidate full suite failed" }
```

The three `run-junit` calls above are the exact candidate suite/argv contract. They write only ignored raw XML and command records. Now prepare, scrub, publish, and validate the candidate bundle with `P/P` head polarity:

```powershell
C:\Python314\python.exe -B tools\build_wave0_evidence.py build --stage candidate --tested-head $implementationSha --implementation-parent $implementationSha --raw-dir $rawDir --output-dir $candidateDir
if ($LASTEXITCODE -ne 0) { throw "Wave 0 candidate evidence build failed" }
C:\Python314\python.exe -B tools\remediation_evidence.py validate "$candidateDir/index.json" --cwd .
if ($LASTEXITCODE -ne 0) { throw "Wave 0 candidate evidence validation failed" }
Get-ChildItem -LiteralPath $candidateDir -File | Select-Object -ExpandProperty Name
git status --porcelain=v1
git add -- $candidateDir
git commit -m "test: record wave 0 candidate evidence"
$evidenceSha = (git rev-parse HEAD).Trim()
$actualParent = (git rev-parse HEAD^).Trim()
if ($actualParent -ne $implementationSha) { throw "candidate evidence is not the exact child of P" }
$unexpected = @(git diff --name-only "$implementationSha..$evidenceSha" | Where-Object { $_ -notlike "$candidateDir/*" })
if ($unexpected.Count -ne 0) { throw "candidate child contains non-evidence paths: $unexpected" }
```

The public directory contains exactly `CANDIDATE_PUBLIC_PATHS`. Its three
sanitized command records, dependency/environment/plan bindings, historical
verification record, XML files, and privacy map are inventoried by `index.json`.
Every public byte passes the total privacy scan and every raw input has a
raw-to-public hash mapping. The resulting commit is evidence child `E`; it
contains no raw XML, raw command record, review, cache, or gate telemetry.

### Task 6: Close Wave 0 at exact evidence child `E`

**Files:**
- Create but do not commit: the `verification-evidence/wave-0/` child directory
  whose name is computed as `(git rev-parse HEAD).Substring(0, 12)`.
- Create within that directory exactly one
  `CLOSURE_PUBLIC_PATHS_BY_TARGET[review_target]` branch: 16 files for target
  2, 18 for target 4, or 22 for target 8, always including two claim-specific
  adjudicators and the exact detached historical reproduced-source bytes.
- Create ignored control plane: gate-owned `.verification/active.json` and `.verification/wave-0/final-ledger.json`

**Interfaces:**
- Produces exact-child targeted, subsystem, and full CPU JUnit plus a `closure` evidence index bound to `E` and parent `P`.
- Closes only `CHK-WAVE0-CONTRACT-COMPLETENESS` and `CHK-WAVE0-HISTORICAL-BYTE-PINS` as `EVIDENCE_VERIFIED`.
- Leaves all 22 remediation claims unclosed; no current defect proposition is marked `REFUTED` in Wave 0.

- [ ] **Step 1: Rerun all three suites at exact `E`, then obtain raw reviews**

Resolve the actual child and parent, establish the same CPU-only environment, and create only ignored raw staging. This is the exact `E/P` closure invocation; do not reuse candidate XML or basetemps.

```powershell
$ErrorActionPreference = 'Stop'
$evidenceSha = (git rev-parse HEAD).Trim()
$implementationSha = (git rev-parse HEAD^).Trim()
$evidenceShort = $evidenceSha.Substring(0, 12)
$implementationShort = $implementationSha.Substring(0, 12)
$rawDir = ".verification/raw/wave-0/$evidenceShort/closure"
$closureDir = "verification-evidence/wave-0/$evidenceShort"
$candidateDir = "docs/verification/evidence/wave-0/$implementationShort"
if ((git rev-parse HEAD^).Trim() -ne $implementationSha) { throw "invalid E/P relationship" }
if (-not (Test-Path -LiteralPath "$candidateDir/index.json")) { throw "candidate index for P is missing" }
if (Test-Path -LiteralPath $rawDir) { throw "closure raw directory already exists" }
if (Test-Path -LiteralPath $closureDir) { throw "closure evidence directory already exists" }
New-Item -ItemType Directory -Path $rawDir | Out-Null
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
$env:CUDA_VISIBLE_DEVICES = '-1'
$env:PYTHONHASHSEED = '0'

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/targeted.command.json" --junit "$rawDir/targeted.raw.xml" -- C:\Python314\python.exe -B -m pytest tests/test_remediation_contracts.py tests/test_remediation_evidence.py -q -p no:cacheprovider --basetemp="$rawDir/tmp-targeted" --junitxml="$rawDir/targeted.raw.xml"
if ($LASTEXITCODE -ne 0) { throw "Wave 0 closure targeted suite failed" }

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/subsystem.command.json" --junit "$rawDir/subsystem.raw.xml" -- C:\Python314\python.exe -B -m pytest tests/test_remediation_contracts.py tests/test_remediation_evidence.py tests/test_shared_scientific_contracts.py tests/test_gaussian_results_document.py -q -p no:cacheprovider --basetemp="$rawDir/tmp-subsystem" --junitxml="$rawDir/subsystem.raw.xml"
if ($LASTEXITCODE -ne 0) { throw "Wave 0 closure subsystem suite failed" }

C:\Python314\python.exe -B tools\remediation_evidence.py run-junit --record "$rawDir/full.command.json" --junit "$rawDir/full.raw.xml" -- C:\Python314\python.exe -B -m pytest -q -p no:cacheprovider --basetemp="$rawDir/tmp-full" --junitxml="$rawDir/full.raw.xml"
if ($LASTEXITCODE -ne 0) { throw "Wave 0 closure full suite failed" }

if (Test-Path -LiteralPath $closureDir) { throw "closure directory exists before review" }
$reviewContextSha = (& 'C:\Python314\python.exe' -B tools\build_wave0_evidence.py review-context-sha --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir).Trim()
if ($LASTEXITCODE -ne 0 -or $reviewContextSha -notmatch '^[0-9a-f]{64}$') { throw "review context digest failed" }
if (-not (Test-Path -LiteralPath "$rawDir/review-context.json")) { throw "review context bytes missing" }
if (-not (Test-Path -LiteralPath "$rawDir/detached/historical-verification.json")) { throw "detached historical reproduced source missing" }
if (Test-Path -LiteralPath $closureDir) { throw "review context wrote final closure bytes" }
```

Before any build/index command, dispatch two independent source-reading reviews
at exact `E` and save canonical raw JSON under
`$rawDir/reviews/code-contract-review.json` and
`$rawDir/reviews/evidence-source-review.json`. Each review has exactly
`schema_version`, `view_id`, `calibration_kind`, `tested_git_head`,
`implementation_parent_git_head`, `reviewed_input_inventory_sha256`,
`reviewed_paths`, `claim_scores`, `verdict`, `escalation_triggers`,
`unresolved_disagreement`, `open_obligations`, `result_location`, and
`falsification_conditions`. Values bind full `E`, full `P`,
`$reviewContextSha`, sorted repository-relative reviewed paths, both literal
claim IDs, the exact per-domain criterion keys, integer scores in `[0,20]`,
and the intended public review path. `calibration_kind` is exactly
`independent_pairwise_source_reading_v1`. Each `claim_scores` item has exactly
`claim_id`, `domain`, `severity`, `evidence_ids`, `criteria`, `verdict`,
`escalation_triggers`, `unresolved_disagreement`, and `open_obligations`.
Initial-view claim records additionally and exactly contain `candidate_ids`,
`candidate_descriptions`, `comparison_order`, `comparison_outcome`, and
`comparison_criteria`. Candidate IDs are
`claim-statement` and `explicit-negation` with nonempty descriptions. The
`code-contract-review` record carries the `AB` order and the
`evidence-source-review` record carries `BA`. `comparison_criteria` exactly
matches `criteria`. Escalation-view claim records use the smaller closed field
set and never add a duplicate comparison match. Each initial review scores both
claims. Each escalation review scores exactly the nonempty subset of claims
whose current target includes that view; it may not pad an untriggered claim.
Aggregate review fields equal the deterministic conjunction of their included
claim records. Both reviews explicitly include the detached public-form
`historical-verification.json` path/hash in `reviewed_paths` and context.

Run `review-target` after the initial two records:

```powershell
$reviewTarget = [int]((& 'C:\Python314\python.exe' -B tools\build_wave0_evidence.py review-target --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir).Trim())
if ($LASTEXITCODE -ne 0 -or $reviewTarget -notin @(2, 4)) { throw "invalid initial review target" }
```

If it prints 4, obtain exactly
`reviews/escalation/boundary-failure-review.json` and
`reviews/escalation/provenance-counterevidence-review.json` for each triggered
claim, then rerun `review-target`. It must print 4 unless criterion disagreement
remains unresolved, in which case it must print 8. If it prints 8, obtain
exactly the four `TARGET8_ADDITIONAL_REVIEW_PATHS` for each still-disputed
claim. Run `review-target` once more and require a stable result of 8. An
unselected escalation file, omitted selected file, target regression, trigger
removal, or escalation record that scores an untriggered claim is invalid.

Save one raw adjudicator per claim under `$rawDir/reviews/adjudicators/`. Each
closed record has exactly `schema_version`, `role`, `claim_id`,
`tested_git_head`, `implementation_parent_git_head`,
`reviewed_input_inventory_sha256`, `escalation_triggers`,
`escalation_target`, `view_ids`, `result`, `evidence_ids`,
`result_location`, `reason`, `falsification_condition`, and
`open_obligations`. `role="verifier-adjudicator"`; `view_ids` equals
`VIEW_IDS_BY_TARGET[claim_target]`; `evidence_ids` equals that claim's literal
`CLAIM_SPECS` IDs and never includes `index.json` or an index-derived evidence
ID; and
`result_location` is the intended public path in `ADJUDICATOR_PATHS`. Results
are `support` only when every target-required view agrees and eligible evidence
is complete; otherwise they are `abstain` with an obligation. A claim may
remain target 2 while the other claim drives the closure branch to 4 or 8. No
majority resolution exists.

```powershell
$validatedTarget = [int]((& 'C:\Python314\python.exe' -B tools\build_wave0_evidence.py validate-reviews --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir).Trim())
if ($LASTEXITCODE -ne 0 -or $validatedTarget -ne $reviewTarget) { throw "raw exact-E review validation failed" }
if (Test-Path -LiteralPath $closureDir) { throw "review validation wrote closure bytes" }
```

The review validator checks closed fields, exact heads/context digest, sorted
reviewed paths, literal claim/domain/severity/evidence IDs, complete criteria,
exact 2/4/8 per-claim view sets, arithmetic-mean aggregates, complete initial
AB/BA comparisons, trigger/target transitions, adjudicator binding, public
result locations, and absence of private-token placeholders in raw semantic
fields. Missing, extra, conflict-obscuring, or fabricated records fail.

- [ ] **Step 2: Prepare once, publish once, and validate exact closure bytes**

```powershell
C:\Python314\python.exe -B tools\build_wave0_evidence.py build --stage closure --tested-head $evidenceSha --implementation-parent $implementationSha --raw-dir $rawDir --output-dir $closureDir
if ($LASTEXITCODE -ne 0) { throw "Wave 0 closure evidence build failed" }
C:\Python314\python.exe -B tools\remediation_evidence.py validate "$closureDir\index.json" --cwd .
if ($LASTEXITCODE -ne 0) { throw "Wave 0 closure evidence validation failed" }
git diff --check
git diff --cached --quiet
git diff --quiet
$trackedDirty = @(git status --porcelain=v1 --untracked-files=no)
if ($trackedDirty.Count -ne 0) { throw "tracked worktree is dirty: $trackedDirty" }
$expectedClosureRelative = @(
  "commands/full.json",
  "commands/subsystem.json",
  "commands/targeted.json",
  "dependencies.json",
  "environment.json",
  "full.xml",
  "historical-verification.json",
  "index.json",
  "plan-binding.json",
  "privacy-transform.json",
  "reviews/adjudicators/CHK-WAVE0-CONTRACT-COMPLETENESS.json",
  "reviews/adjudicators/CHK-WAVE0-HISTORICAL-BYTE-PINS.json",
  "reviews/code-contract-review.json",
  "reviews/evidence-source-review.json",
  "subsystem.xml",
  "targeted.xml"
)
if ($reviewTarget -ge 4) {
  $expectedClosureRelative += @(
    "reviews/escalation/boundary-failure-review.json",
    "reviews/escalation/provenance-counterevidence-review.json"
  )
}
if ($reviewTarget -eq 8) {
  $expectedClosureRelative += @(
    "reviews/escalation/configuration-reachability-review.json",
    "reviews/escalation/historical-source-adversary.json",
    "reviews/escalation/path-privacy-adversary.json",
    "reviews/escalation/reproducibility-review.json"
  )
}
$expectedClosureCount = @{2 = 16; 4 = 18; 8 = 22}[$reviewTarget]
if (@($expectedClosureRelative | Sort-Object -Unique).Count -ne $expectedClosureCount) {
  throw "branch-specific closure inventory drift"
}
$expectedClosureFiles = @($expectedClosureRelative | ForEach-Object { "$closureDir/$_" })
$actualUntracked = @(git ls-files --others --exclude-standard | Sort-Object)
$expectedUntracked = @($expectedClosureFiles | Sort-Object)
if (Compare-Object $expectedUntracked $actualUntracked) { throw "unexpected nonignored untracked paths" }
```

The exact 16/18/22 branch files above are the only nonignored untracked paths.
Every byte other than self-inventorying `index.json` is hash-inventoried by it;
the validator separately hashes the index and checks its canonical bytes. The
published `historical-verification.json` hash must equal the detached reviewed
file hash. Ignored `.verification/raw/...` may remain local but can never be
sole claim evidence. Do not commit closure bytes.

- [ ] **Step 3: Confirm the published bundle contains the reviewed bytes**

Re-open every public path in
`REVIEW_PATHS_BY_TARGET[$reviewTarget]` and both public adjudicators from
`$closureDir`, recompute their hashes against `index.json`, and require their
semantic records to equal the validated raw records after the declared privacy
transform. Rehash published and detached `historical-verification.json` and
require byte identity. Any source, contract, candidate-evidence, raw closure
input, review, or public closure byte change invalidates `$reviewContextSha` and
requires rerunning Task 6 from Step 1. A reviewer does not close a claim;
current domain-eligible evidence plus structured adjudication does.

- [ ] **Step 4: Start the real gate, populate its template explicitly, and validate**

The safe repository wrapper exposes only installed-gate `start` and `validate`.
`start` writes an empty candidate template; therefore the plan explicitly invokes
the checked-in Wave 0 population wrapper between `start` and `validate`:

```powershell
$verificationRoot = 'C:\Users\chris and christine\.codex\skills\verification'
$snapshot = 'docs/verification/remediation/verification-contract-v1.json'
$ledger = '.verification/wave-0/final-ledger.json'
if (Test-Path -LiteralPath '.verification/active.json') { throw "verification gate is already active" }
if (Test-Path -LiteralPath $ledger) { throw "Wave 0 ledger already exists" }

& 'C:\Python314\python.exe' -B tools\remediation_evidence.py run-verification-gate --snapshot $snapshot --root $verificationRoot -- start --cwd . --mode closure --ledger $ledger
if ($LASTEXITCODE -ne 0) { throw "verification gate start failed" }

& 'C:\Python314\python.exe' -B tools\remediation_evidence.py run-verification-gate --snapshot $snapshot --root $verificationRoot -- validate --cwd . $ledger
if ($LASTEXITCODE -eq 0) { throw "empty start template unexpectedly validated" }

C:\Python314\python.exe -B tools\build_wave0_evidence.py populate-ledger --ledger $ledger --closure-index "$closureDir/index.json"
if ($LASTEXITCODE -ne 0) { throw "explicit Wave 0 ledger population failed" }

& 'C:\Python314\python.exe' -B tools\remediation_evidence.py run-verification-gate --snapshot $snapshot --root $verificationRoot -- validate --cwd . $ledger
if ($LASTEXITCODE -ne 0) { throw "populated Wave 0 ledger failed validation" }

$ledgerJson = Get-Content -LiteralPath $ledger -Raw | ConvertFrom-Json
if (@($ledgerJson.claims).Count -ne 2) { throw "Wave 0 ledger must contain exactly two claims" }
if (@($ledgerJson.claims | Where-Object { $_.id -like 'AUD-*' }).Count -ne 0) { throw "Wave 0 must not close an AUD claim" }
$nonVerified = @($ledgerJson.claims | Where-Object { $_.state -ne 'EVIDENCE_VERIFIED' })
if ($nonVerified.Count -ne 0) { throw "Wave 0 ledger is valid but closure is blocked by an INCONCLUSIVE claim" }
```

The wrapper copies the concrete gate-generated `artifact_revision` to both
claims and every evidence entry; it does not invent a Git SHA as an artifact
revision. The closure index is validated as a structural prerequisite but is
not claim evidence. The claims reference exact public JUnits,
historical source/reproduction records, every per-claim target-required public
review, and both public adjudicators. The ignored ledger is never sole evidence. After
successful validation, no file outside the excluded ledger may change; the
final handoff names `.verification/wave-0/final-ledger.json` so the gate hook
can validate and remove `.verification/active.json`.

- [ ] **Step 5: Publish only exact verified `E`**

Push the dedicated Wave 0 branch, integrate it serially only after both reviews and ledger validation pass, fast-forward the clean integration branch to exact `E`, rerun remote/local SHA checks, and preserve the user's live WIP. A merge commit or changed tree requires a fresh exact-final closure run.
