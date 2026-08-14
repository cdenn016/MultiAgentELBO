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
- Production source state during the RED run: absent in the disposable mirror by design; the live untracked witness remained untouched outside the mirror

## RED command

Run from the disposable root `C:\tmp\maelbo-typed-intervention-contract-red-r2-20260814`, which contained the amended test and its snapshot but no witness, with the CPU-only interpreter and deterministic environment:

```powershell
$env:CUDA_VISIBLE_DEVICES='-1'
$env:PYTHONHASHSEED='0'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
C:\Python314\python.exe -m pytest tests\test_typed_intervention_semantics_witness.py -q --basetemp=C:\tmp\maelbo-typed-intervention-contract-red-r2-basetemp-20260814 --junitxml=C:\Users\chris and christine\Desktop\MultiAgentELBO\.superpowers\worktrees\MultiAgentELBO-typed-intervention-semantics-20260814\docs\derivations\2026-08-14-typed-intervention-nonidentifiability\evidence\red-junit.xml
```

Process exit status: `1`.

Machine-derived JUnit totals:

- tests: 18
- failures: 18
- errors: 0
- skipped: 0
- time: 0.344 seconds

All 18 `<failure>` nodes contain the declared absent-witness assertion.

## Contract-review correction

This RED supersedes the narrower Task 1 record in commit `bff35ede271270cdd7e784f2a16d369a3dae73cd`. The production witness remained absent throughout the correction. The tightened executable contract now additionally freezes:

- every public call signature through exact `inspect.signature` parameter names, kinds, defaults, and keyword-only boundaries;
- exact nested tuple schemas for contextual signatures, behavioral classes, context assignments, multiplication rows and class indices, and response laws;
- canonical `R,E,N,O` composition ordering;
- presentation-specific absent-node rejection through each relevant direct public context entry point; and
- literal deterministic `control` and `null_control` inner schemas, each compared to an independently recomputed native record containing the specified passive laws, nine boundary responses, mediator pair and total variation, complete null signatures, split/null reduced experiments, and forget-`N` isomorphism checks.

A follow-up selector-matrix correction after commit `65c106bba378a16e72004d35fd6ca177df743321` exercises valid `contextual_response_signature` and `response_image` returns for every declared selector. The matrix binds `direct` to node order `R,O`, `split` to `R,E,O`, and `null` to `R,E,N,O`, and applies the same exact nested tuple, partition, multiplication, and response-law schema checks to all three.

The adjudicated direct-semantics correction adds an independent oracle built only from the literal nine-context direct response table and an independent right-override implementation. It derives all direct two-sided signatures, behavioral classes, class responses, and quotient multiplication before comparing them to the public direct selector. The same correction freezes literal raw invariant records for direct, split, and null presentations, checks their pairwise distinction, and binds main JSON to those literals instead of production self-calls.

## Failing tests

- `tests.test_typed_intervention_semantics_witness::test_public_api_call_signatures_are_exact`
- `tests.test_typed_intervention_semantics_witness::test_every_selector_returns_declared_signature_and_experiment_schemas[direct]`
- `tests.test_typed_intervention_semantics_witness::test_every_selector_returns_declared_signature_and_experiment_schemas[split]`
- `tests.test_typed_intervention_semantics_witness::test_every_selector_returns_declared_signature_and_experiment_schemas[null]`
- `tests.test_typed_intervention_semantics_witness::test_direct_selector_matches_independent_literal_response_oracle`
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

Every collected test failed at `_load_witness()` because `exact_typed_intervention_witness.py` did not exist. The assertion text was `expected RED: exact_typed_intervention_witness.py has not been implemented`. There were no collection errors, import errors, malformed fixtures, environmental failures, or unrelated test failures. This proves that the review-corrected executable contract reaches the missing production boundary before Task 2 implementation.

The contract freezes every required API signature, exact BSC and validation behavior, lexicographic joint-law order, all nine shared-boundary tables, an independently derived direct-selector response experiment, mediator responses, exhaustive nullness, literal two-sided signatures, quotient-monoid reduction, same-signature passive and intervened laws, all four boundary relabelings, all eight raw binary state relabelings, literal pairwise-distinct raw presentation records, fifteen reduced classes, multiplication and full-serialization hashes, transparent counterexample records, recursive JSON encoding, fresh-process byte stability, and source-snapshot byte identity.

## Durable byte identities

The RED XML was decoded as UTF-8, every CRLF or bare CR was changed to LF, spaces and tabs were stripped only at line ends, and the file was written as UTF-8 without a BOM. No path, hostname, timing, test ID, or failure content was sanitized.

| Artifact | Filesystem SHA-256 | Filtered Git blob | Bytes | CR bytes | UTF-8 BOM |
| --- | --- | --- | ---: | ---: | --- |
| `evidence/red-junit.xml` | `f37ad52fb126a0a7e7ce235b5275542ff286adcee959e993477d44dee0a0e9ab` | `055857141c069d3481c09203a9c8c2f7617457cd` | 26329 | 0 | no |
| `tests/test_typed_intervention_semantics_witness.py` | `0df74569948a70df5100f3d006b6d7b6d97da1f7a11a6cdd028e662a489ce73e` | `a1148f6309d6240434d576d9c47a3171675e71d9` | 39241 | 0 | no |
| `evidence/test_typed_intervention_semantics_witness.snapshot.py` | `0df74569948a70df5100f3d006b6d7b6d97da1f7a11a6cdd028e662a489ce73e` | `a1148f6309d6240434d576d9c47a3171675e71d9` | 39241 | 0 | no |

The live test and package snapshot are byte-identical. For all three artifacts, the raw LF bytes and the configured Git-clean-filter bytes describe the same content; the Git blob identifiers above are the repository object identities after the explicit `text eol=lf` rules.

## GREEN command and result

After contract commit `28077de`, the witness was evaluated from the isolated repository root with the same CPU-only deterministic environment:

```powershell
$env:CUDA_VISIBLE_DEVICES='-1'
$env:PYTHONHASHSEED='0'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
C:\Python314\python.exe -m pytest tests\test_typed_intervention_semantics_witness.py -q --basetemp=C:\tmp\maelbo-typed-intervention-green-final-20260814 --junitxml=docs\derivations\2026-08-14-typed-intervention-nonidentifiability\evidence\green-junit.xml
```

Process exit status: `0`.

Machine-derived JUnit totals:

- tests: 18
- failures: 0
- errors: 0
- skipped: 0
- time: 7.055 seconds

The final test includes two in-process `main()` calls, one fresh-process witness execution, exact stdout byte equality, and live-test/snapshot byte equality. The fresh process exited zero, emitted no stderr, and produced the same single-LF ASCII document.

### Final GREEN byte identities

| Artifact | Filesystem SHA-256 | Filtered Git blob | Bytes | CR bytes | UTF-8 BOM |
| --- | --- | --- | ---: | ---: | --- |
| `evidence/exact_typed_intervention_witness.py` | `114f3c74b62161fe6866c1918ba6d7f58eb47ef144d53bb13c58704084b0d985` | `6729f8f0ea075f1f1dc4c0872ccf23a3b609fb49` | 22929 | 0 | no |
| `evidence/green-junit.xml` | `4ab838c07ac466bc11016df695b4883eb3a2bf01b599a041f9d01713695c6ff5` | `2f5ca7aeb41348e64c6b75a384bba4a48aecdfe2` | 3078 | 0 | no |
| `tests/test_typed_intervention_semantics_witness.py` | `0df74569948a70df5100f3d006b6d7b6d97da1f7a11a6cdd028e662a489ce73e` | `a1148f6309d6240434d576d9c47a3171675e71d9` | 39241 | 0 | no |
| `evidence/test_typed_intervention_semantics_witness.snapshot.py` | `0df74569948a70df5100f3d006b6d7b6d97da1f7a11a6cdd028e662a489ce73e` | `a1148f6309d6240434d576d9c47a3171675e71d9` | 39241 | 0 | no |

## Mutation evidence

Nine reversible mutants were applied separately to the final source. Every run used the focused 18-test file, exited `1`, reported at least one test failure, and reported zero errors and zero skips. Every reversal restored witness SHA-256 `114f3c74b62161fe6866c1918ba6d7f58eb47ef144d53bb13c58704084b0d985` exactly before the next mutation.

| Mutant | Mutant SHA-256 | Failures | JUnit SHA-256 |
| --- | --- | ---: | --- |
| wrong channel composition | `db24dfb9b853805ac9bc6762bc5e5559291d41eace5ecf041481a5ee095dd84b` | 5 | `9b8a67cc0f0c4da324e58dbf0ba5cacc92d4c1bd74808297884125871d222551` |
| ignored `b` | `9e329bbf74b211ed678ee7bbd06cd74b5562c628920754f7b897a943f35ead37` | 9 | `4516cafe6bec2836759eff889bf109c89921e5a5487709ae69580166303361a3` |
| omitted left/right context composition | `6e266140812bb8e052a30826befcbc4cfac5790720d788539f03db8a3f870983` | 2 | `3f7c2fecbde225c1934af5575efd69f2b9d71ed30330f70167bac391913f0eda` |
| altered response-image entry | `8f5666cdb4e02e98d03485be3fb7e6bd728e7cdaec92a15e037e7e2346e69729` | 2 | `9140f3fa54bb24ff81408e4e0cd76c3b3f34e2cfc32d1a79ba7785a40bfec241` |
| collapsed class multiplication | `7e3125519bc9d64088f5bb1e51bfa8b8e4581ceb9e3cec2ab393d451309e1690` | 6 | `4a62f404cb6bcd8530951c50ab416d2a09a0660f7381cff346c36d9608349d65` |
| equalized diagnostic contrasts | `c82958c6623855861febf42eafdff4cd49da87fe9705760a3f98c03cb9e7946c` | 1 | `ae0899b8266290dfdb87c648a74c662d71b885315447ae0e9397689cd17b858b` |
| unsorted nested JSON | `c97edcc1eff22642afb171584768165fee2b2b1e9dcefbcbdd778cda6da6d19f` | 1 | `0daeb88fb744ae6b658825862af6c841b2977d8b24765dec12659d0725b13111` |
| direct response semantics | `3388a07264bd55afaba06c2aeb7cf47b26490f5191624757ea885498d0e38ad4` | 2 | `046c19d7c287dc894df313af2932a86783ba75b093b607bcd58993ff3bd28a5f` |
| direct/null raw invariants | `4bc41723bb9a101ed37bbd328982e75aaf9717145ce4432fb4521a3136822e7a` | 2 | `957f5b8a58706191c769ee57e32b2a47f641eaf6d610e22753ec07712f0cb19f` |

`evidence/mutations/mutation-record.json` records each exact command, semantic edit, process exit, machine-derived totals, failing test identifiers, JUnit location and SHA-256, and pre/mutant/post source hashes. Its SHA-256 is `e03fccd021e623deb40e0013590a0f8a376f73f44126db4541495fd2689dd1fc`, its filtered Git blob is `1fdfa2562ae6a339426c64c76f5117e02ef52501`, and all nine recorded bindings passed an independent standard-library parser check.

The JSON mutant disables both recursive dictionary ordering and `json.dumps` key sorting. Disabling only the serializer sort remains behaviorally sorted because the witness independently sorts nested dictionaries before serialization; the combined mutant removes both safeguards and is killed by the canonical-byte test.

## Evidence boundary

The RED establishes that the frozen executable contract reaches the missing implementation boundary. GREEN and mutation evidence establish the current exact program behavior for the bound source and test bytes. They corroborate finite tables and counterexample data, but they are not a mathematical derivation and do not by themselves prove reduced nonisomorphism or the no-recovery theorem.
