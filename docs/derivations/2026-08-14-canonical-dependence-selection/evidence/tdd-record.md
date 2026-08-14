<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-8112f0083a554a4df3b5de3875174d0b0cbfeee36a7bc2ea20e78c8cf9da6b39","schema_version":"rigorous-theory-search/v1","target_digest":"8112f0083a554a4df3b5de3875174d0b0cbfeee36a7bc2ea20e78c8cf9da6b39"} -->
# Canonical selection witness TDD record

## Bound contract

- Contract ID: `contract-sha256-8112f0083a554a4df3b5de3875174d0b0cbfeee36a7bc2ea20e78c8cf9da6b39`
- Target digest: `8112f0083a554a4df3b5de3875174d0b0cbfeee36a7bc2ea20e78c8cf9da6b39`
- Test source: `tests/test_canonical_dependence_selection_witness.py`
- Intended production source: `evidence/exact_selection_witness.py`
- Production source state during the RED run: absent by design

## RED command

Run from the repository root with the CPU-only interpreter and deterministic environment:

```powershell
$env:CUDA_VISIBLE_DEVICES='-1'
$env:PYTHONHASHSEED='0'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
C:\Python314\python.exe -m pytest tests\test_canonical_dependence_selection_witness.py -q -p no:cacheprovider --basetemp={TEMP}\maelbo-selector-red-20260814 --junitxml=docs\derivations\2026-08-14-canonical-dependence-selection\evidence\red-junit.xml
```

Process exit status: `1`.

Machine-derived JUnit totals:

- tests: 11
- failures: 11
- errors: 0
- skipped: 0
- time: 0.103 seconds
- Sanitized LF JUnit SHA-256: `7d1b7cf9febf349c88c9a57c2aaa8d462df33b3cac4f3210c37e2d1d36dec1f8`

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

The durable GREEN record was regenerated during the Task 5 review repair from the repository root under the deterministic CPU environment:

```powershell
$env:CUDA_VISIBLE_DEVICES='-1'
$env:PYTHONHASHSEED='0'
Remove-Item Env:MULTIAGENTELBO_RUN_CUDA_TESTS -ErrorAction SilentlyContinue
Remove-Item Env:VFE3_TEST_DEVICE -ErrorAction SilentlyContinue
Remove-Item Env:CUBLAS_WORKSPACE_CONFIG -ErrorAction SilentlyContinue
C:\Python314\python.exe -m pytest tests\test_canonical_dependence_selection_witness.py -q -p no:cacheprovider --basetemp={TEMP}\maelbo-selector-task5-review-fix-20260814-8112f008 --junitxml={STAGING_ROOT}\evidence\green-junit.xml
```

Process exit status: `0`.

Machine-derived JUnit totals:

- tests: 13
- failures: 0
- errors: 0
- skipped: 0
- time: 0.060 seconds
- Sanitized LF JUnit SHA-256: `82714d624ac455d1dfdbd9e22eeff3cb484077b555c79b99f57baf65ff3b1dc2`

The production-source SHA-256 is `2518612bb7fc9055843efda16b296595dec7e88d115ae2f4438486cf38360e45`. The LF test-contract-snapshot SHA-256 is `132181dfa9f5f581eaa5d0e25d840e9589e11a1b7e311ee52bed75e0f61d2ac4`.

`{TEMP}` denotes the machine temporary root and `{STAGING_ROOT}` denotes
the atomic writable package-staging root. They are explicit provenance
redactions; every other command token and environment assignment is retained.
The durable GREEN and RED JUnit files replace the machine hostname with
`{HOST}`; the RED file also replaces the absolute worktree prefix with
`{WORKTREE}`. Test IDs, totals, timings, failure messages, and pass/fail
semantics are preserved.

## Exactness boundary

The binary laws, marginalization, products, split kernel, deterministic pushforwards, posterior completion, conditional cross-product defect, Fisher score sum, Gaussian elimination, BSC Fisher pullback, and both promoted-parity derivative ranks use `Fraction` throughout. `completion_conditional_defect` is the exact sum of squared within-cell cross products

```text
(candidate[x] reference[x'] - candidate[x'] reference[x])^2.
```

It is zero for the selected posterior completion and strictly positive for the declared distinct feasible candidate. No logarithm or floating KL value is used as uniqueness evidence. The JSON document serializes every rational as an integer string or `numerator/denominator` string and contains no path, host, clock, random, or environment field.

## Mutation evidence

Two initial reversible source mutations were applied separately, tested, and reversed. Before and after each mutation, the exact witness SHA-256 was the same `6dac3d00abf6eb7703d60b400c84d64b134df7db117387da1019e197cf9f2513`.

1. One negative categorical atom derivative in `dependence_fisher` was changed to positive. The run exited `1` with 11 tests, 2 failures, 0 errors, and 0 skips. The direct Fisher test and deterministic-JSON test failed because the categorical derivative vector no longer had zero total. This catches a sign mutation that a bare sum of squares would otherwise hide.
2. The promoted-parity `kappa` derivative column was replaced by zero. The run exited `1` with 11 tests, 1 failure, 0 errors, and 0 skips. The promoted-parity rank test reported rank 6 instead of the required rank 7.

The mutation JUnit files were scratch diagnostics under `{TEMP}`; they are not closure evidence and are not referenced as durable artifacts.

### Reviewer-fix mutation cycle

The tightened 13-test contract was first run RED against the pre-fix implementation: 13 tests, 2 failures, 0 errors, and 0 skips. The missing derivative-provider seam and numeric JSON rank leaves caused the expected failures. After the minimal production changes, all 13 tests passed.

Five additional reversible mutations each failed its focused test with 1 test, 1 failure, 0 errors, and 0 skips. Each reversal restored witness SHA-256 `2518612bb7fc9055843efda16b296595dec7e88d115ae2f4438486cf38360e45` exactly.

1. Removing the positive-charge rejection on a zero-reference coarse cell failed the zero-reference-fiber test.
2. Doubling every squared conditional cross product failed the exact `625/11664` defect assertion.
3. Doubling the promoted-parity `theta` derivative entries preserved rank seven but failed the independent `+/-1/32` atom-entry assertions.
4. Returning JSON rank integers rather than rational strings failed the recursive leaf-schema check.
5. Bypassing `_dependence_atom_derivatives` with an inlined tuple failed the monkeypatched dependency test, proving that `dependence_fisher` consumes the provider rather than returning only the closed form.

## Portability controls

The four durable witness inputs have zero carriage-return bytes and are bound by their final LF SHA-256 values:

- `exact_selection_witness.py`: 14,820 bytes, SHA-256 `2518612bb7fc9055843efda16b296595dec7e88d115ae2f4438486cf38360e45`;
- `green-junit.xml`: 2,293 bytes, SHA-256 `82714d624ac455d1dfdbd9e22eeff3cb484077b555c79b99f57baf65ff3b1dc2`;
- `test_canonical_dependence_selection_witness.snapshot.py`: 12,586 bytes, SHA-256 `132181dfa9f5f581eaa5d0e25d840e9589e11a1b7e311ee52bed75e0f61d2ac4`;
- `red-junit.xml`: 14,690 bytes, SHA-256 `7d1b7cf9febf349c88c9a57c2aaa8d462df33b3cac4f3210c37e2d1d36dec1f8`.

The test-contract snapshot represents the portable LF test source rather than platform-specific checkout newlines. The ledger separately binds this TDD record, closing the source/test/JUnit/command/environment provenance chain without treating execution as mathematical proof.
