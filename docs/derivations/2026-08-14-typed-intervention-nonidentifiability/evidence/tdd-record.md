<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-efe715cba81c2000403811015e6cecb599f4023133543b5cb0ae77288bccc874","schema_version":"rigorous-theory-search/v1","target_digest":"efe715cba81c2000403811015e6cecb599f4023133543b5cb0ae77288bccc874"} -->
# Typed-intervention witness TDD record

## Bound contract

- Contract ID: `contract-sha256-efe715cba81c2000403811015e6cecb599f4023133543b5cb0ae77288bccc874`
- Target digest: `efe715cba81c2000403811015e6cecb599f4023133543b5cb0ae77288bccc874`
- Design/plan Git revision: `66a7df4de9f33ccb7cb8a98ecba92a6a55bb96a9`
- Origin-main baseline: `f956c7f1d7fb035d157b415c670a13a46f631233`
- Test source: `tests/test_typed_intervention_semantics_witness.py`
- Test snapshot: `evidence/test_typed_intervention_semantics_witness.snapshot.py`
- Intended production source: `evidence/exact_typed_intervention_witness.py`
- Production source state during the RED run: absent by design

## RED command

Run from the repository root with the CPU-only interpreter and deterministic environment:

```powershell
$env:CUDA_VISIBLE_DEVICES='-1'
$env:PYTHONHASHSEED='0'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
C:\Python314\python.exe -m pytest tests\test_typed_intervention_semantics_witness.py -q --basetemp=C:\tmp\maelbo-typed-intervention-red-20260814 --junitxml=docs\derivations\2026-08-14-typed-intervention-nonidentifiability\evidence\red-junit.xml
```

Process exit status: `1`.

Machine-derived JUnit totals:

- tests: 13
- failures: 13
- errors: 0
- skipped: 0
- time: 0.188 seconds

All 13 `<failure>` nodes contain the declared absent-witness assertion.

## Failing tests

- `tests.test_typed_intervention_semantics_witness::test_bsc_context_composition_and_validation_are_exact`
- `tests.test_typed_intervention_semantics_witness::test_joint_and_retained_laws_use_frozen_lexicographic_order`
- `tests.test_typed_intervention_semantics_witness::test_all_nine_shared_boundary_intervention_tables_are_literal`
- `tests.test_typed_intervention_semantics_witness::test_control_mediator_responses_have_exact_total_variation`
- `tests.test_typed_intervention_semantics_witness::test_null_assignments_are_exhaustively_inert_in_all_27_contexts`
- `tests.test_typed_intervention_semantics_witness::test_null_two_sided_signatures_and_reduced_quotient_are_identical`
- `tests.test_typed_intervention_semantics_witness::test_same_signature_pair_has_frozen_passive_and_mediator_responses`
- `tests.test_typed_intervention_semantics_witness::test_reduced_experiments_match_all_frozen_classes_tables_and_hashes`
- `tests.test_typed_intervention_semantics_witness::test_full_response_images_do_not_match_under_any_boundary_relabeling`
- `tests.test_typed_intervention_semantics_witness::test_raw_signature_and_all_binary_state_relabelings_are_controlled`
- `tests.test_typed_intervention_semantics_witness::test_counterexample_record_is_transparent_and_independently_recomputed`
- `tests.test_typed_intervention_semantics_witness::test_main_json_is_recursive_exact_sorted_compact_and_stable`
- `tests.test_typed_intervention_semantics_witness::test_fresh_process_json_and_lf_test_snapshot_are_byte_identical`

## Expected failure reason

Every collected test failed at `_load_witness()` because `exact_typed_intervention_witness.py` did not exist. The assertion text was `expected RED: exact_typed_intervention_witness.py has not been implemented`. There were no collection errors, import errors, malformed fixtures, environmental failures, or unrelated test failures. This proves that the frozen executable contract reaches the missing production boundary before Task 2 implementation.

The contract freezes every required API signature, exact BSC and validation behavior, lexicographic joint-law order, all nine shared-boundary tables, mediator responses, exhaustive nullness, literal two-sided signatures, quotient-monoid reduction, same-signature passive and intervened laws, all four boundary relabelings, all eight raw binary state relabelings, fifteen reduced classes, multiplication and full-serialization hashes, transparent counterexample records, recursive JSON encoding, fresh-process byte stability, and source-snapshot byte identity.

## Durable byte identities

The RED XML was decoded as UTF-8, every CRLF or bare CR was changed to LF, spaces and tabs were stripped only at line ends, and the file was written as UTF-8 without a BOM. No path, hostname, timing, test ID, or failure content was sanitized.

| Artifact | Filesystem SHA-256 | Filtered Git blob | Bytes | CR bytes | UTF-8 BOM |
| --- | --- | --- | ---: | ---: | --- |
| `evidence/red-junit.xml` | `7293f9eae9a099dcc9ee4af8be0b96e0c315ca205e4d28e041db50a797257deb` | `403b0ace408b35f53c5e2d3246d5e40f09495ce0` | 19569 | 0 | no |
| `tests/test_typed_intervention_semantics_witness.py` | `842648791ac73db70cc0749764bd7a0ac8b923e8c831a6fe95381c1a218a0d2d` | `6924a373e0458e2292a632a9c827232cd72aaca5` | 24598 | 0 | no |
| `evidence/test_typed_intervention_semantics_witness.snapshot.py` | `842648791ac73db70cc0749764bd7a0ac8b923e8c831a6fe95381c1a218a0d2d` | `6924a373e0458e2292a632a9c827232cd72aaca5` | 24598 | 0 | no |

The live test and package snapshot are byte-identical. For all three artifacts, the raw LF bytes and the configured Git-clean-filter bytes describe the same content; the Git blob identifiers above are the repository object identities after the explicit `text eol=lf` rules.

## GREEN and mutation status

GREEN, fresh-process witness execution, and all specified mutants are intentionally not run in Task 1. Task 2 must create the production witness only after this committed RED checkpoint, retain the frozen test bytes, record a zero-failure GREEN JUnit, and preserve byte-identical source restoration around every mutant.

## Evidence boundary

This RED run verifies only that the exact executable contract fails for the intended missing implementation. It is not numerical evidence for any mathematical theorem and does not establish the target counterexample, reduced nonisomorphism, or no-recovery result.
