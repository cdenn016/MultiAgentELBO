# Canonical selection witness TDD record

## Bound contract

- Contract ID: `contract-sha256-b8102c1f5917a6cbc9a69df8b10c1470d18d5146f56093a253b1a8644465bccb`
- Target digest: `b8102c1f5917a6cbc9a69df8b10c1470d18d5146f56093a253b1a8644465bccb`
- Test source: `tests/test_canonical_dependence_selection_witness.py`
- Intended production source: `evidence/exact_selection_witness.py`
- Production source state during this record: absent by design

## RED command

Run from the repository root with the CPU-only interpreter and deterministic environment:

```powershell
$env:CUDA_VISIBLE_DEVICES='-1'
$env:PYTHONHASHSEED='0'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
C:\Python314\python.exe -m pytest tests\test_canonical_dependence_selection_witness.py -q -p no:cacheprovider --basetemp=C:\tmp\maelbo-selector-red-20260814 --junitxml=docs\derivations\2026-08-14-canonical-dependence-selection\evidence\red-junit.xml
```

Process exit status: `1`.

Machine-derived JUnit totals:

- tests: 11
- failures: 11
- errors: 0
- skipped: 0
- time: 0.103 seconds
- LF-normalized JUnit SHA-256: `e98e5cbbd94a20f355b5b2a3caa6f450d23c9ccd4f9e9dd4d4070b9f2fbe966d`

## Failing tests

- `tests.test_canonical_dependence_selection_witness::test_binary_correlation_family_has_exact_atoms_marginals_and_split_law`
- `tests.test_canonical_dependence_selection_witness::test_preparation_pushforward_forces_the_hand_derived_product_coupling`
- `tests.test_canonical_dependence_selection_witness::test_faithful_quasi_inverse_counterexample_survives_relabeling`
- `tests.test_canonical_dependence_selection_witness::test_dependence_fisher_is_computed_exactly_on_two_controls`
- `tests.test_canonical_dependence_selection_witness::test_deterministic_completion_pushes_forward_and_composes_strictly`
- `tests.test_canonical_dependence_selection_witness::test_completion_conditional_defect_is_exactly_selective`
- `tests.test_canonical_dependence_selection_witness::test_reference_relative_selector_inherits_feasible_reference_dependence`
- `tests.test_canonical_dependence_selection_witness::test_fraction_gaussian_elimination_reports_exact_ranks`
- `tests.test_canonical_dependence_selection_witness::test_bsc_retained_quotient_has_rank_one_and_two_exact_null_vectors`
- `tests.test_canonical_dependence_selection_witness::test_promoted_parity_retains_seven_joint_directions_but_six_marginal_directions`
- `tests.test_canonical_dependence_selection_witness::test_main_emits_one_byte_stable_json_document`

## Expected failure reason

Every test failed at the same deliberate guard: `exact_selection_witness.py` did not exist. The assertion text was `expected RED: exact_selection_witness.py has not been implemented`. There were no collection errors, import errors, malformed fixtures, environmental failures, or unrelated test failures. The RED therefore demonstrates that the executable contract reaches the missing production boundary before Task 2 implementation.

The tests freeze exact rational expectations for the binary correlation family, local preparation/product control, relabeling-robust quasi-inverse obstruction, dependence Fisher values, deterministic completion and strict composition, exact conditional defect, reference-relative dependence, fraction-preserving rank, BSC retained quotient, promoted parity rank, and deterministic JSON output. No floating logarithmic comparison is presented as exact arithmetic.

## GREEN status

Not run in Task 1. Task 2 must implement the production witness minimally, re-run this file under the same environment, preserve a separate GREEN JUnit artifact, and append its machine-derived totals here.
