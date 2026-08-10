# Finite Counterexample Laboratory Results

**Date:** 2026-08-09

**Branch:** `codex/finite-counterexamples-20260809`

**Contract freeze:** `b80df01f239c2f9a18842f6887cdeca67dff508f`

**Tested code revision:** `ab747008b970c0c6a162be1ee1501a9baa163cb3`

**Interpreter:** `C:\Python314\python.exe` (CPython 3.14.4, CPU)

**Environment:** NumPy 2.4.4, SciPy 1.17.1, pytest 9.0.2, pytest-cov 7.1.0, coverage.py 7.15.2

## Scope and revision binding

This lane exhaustively enumerates an explicitly bounded finite rational catalog,
records minimal witnesses, and exercises metamorphic and assumption-boundary
controls. It does not prove the frozen theory and does not make continuum,
universality, or physical-time claims. Numerical or computational agreement
below is implementation and experiment evidence, not mathematical proof.

At the tested code revision, the seven changed paths relative to the contract
freeze were:

- `docs/results/2026-08-09-finite-counterexample-results.md`
- `docs/verification/reviews/2026-08-09-finite-counterexample-review.md`
- `run_finite_counterexample_lab.py`
- `src/multiagent_elbo/finite/counterexample_experiment.py`
- `src/multiagent_elbo/finite/counterexamples.py`
- `tests/test_counterexample_experiment.py`
- `tests/test_counterexamples.py`

The lane allowlist check found zero paths outside the exact Session-3 allowlist.

## Mechanical verification

The focused command was:

```powershell
$env:COVERAGE_FILE='.verification\session3\refresh.coverage'; C:\Python314\python.exe -m pytest tests\test_counterexamples.py tests\test_counterexample_experiment.py --basetemp=.pytest-tmp\session3-task3-refresh-focused --junitxml=.verification\session3\task3-refresh-focused.xml --cov=multiagent_elbo.finite --cov-branch --cov-report=xml:.verification\session3\task3-refresh-coverage.xml --cov-report=term-missing --cov-fail-under=0
```

Mechanical XML parsing reported 21 tests, 0 failures, 0 errors, 0 skips, and
22.132 seconds. The coverage XML reported:

| New production module | Line coverage | Branch coverage | Required line threshold |
|---|---:|---:|---:|
| `counterexamples.py` | 90.24% | 75.83% | 80% |
| `counterexample_experiment.py` | 97.56% | 92.86% | 80% |

The complete CPU command was:

```powershell
C:\Python314\python.exe -m pytest --basetemp=.pytest-tmp\session3-task3-refresh-full --junitxml=.verification\session3\task3-refresh-full.xml
```

Mechanical JUnit parsing reported 461 tests, 0 failures, 0 errors, 2 skips, and
42.024 seconds. The two skips are the pre-existing Windows privilege-dependent
artifact-link cases recorded in the JUnit file.

## Launcher configuration and provenance

The click-to-run launcher has no parser and uses these default dictionaries:

```python
RUN = {"name": "finite_counterexample", "seed": 20260809}
THEORY = {
    "experiment": "finite_counterexample",
    "fixture": "counterexample_catalog_v1",
    "max_states": 4,
    "max_denominator": 8,
    "arithmetic": "exact_rational",
}
NUMERICS = {
    "dtype": "float64",
    "atol": 1.0e-12,
    "rtol": 1.0e-10,
    "min_spd_rcond": 1.0e-12,
    "max_frame_condition": 1.0e6,
}
OUTPUT = {
    "root": "artifacts",
    "collect_diagnostics": True,
    "render_figures": False,
}
```

The literal no-argument launcher execution from a fresh ignored working
directory used:

```powershell
Push-Location .verification\session3\refresh-direct-root
C:\Python314\python.exe 'C:\Users\chris and christine\Documents\ChatGPT\MultiAgentELBO\.superpowers\worktrees\MultiAgentELBO-finite-counterexamples-20260809\run_finite_counterexample_lab.py'
Pop-Location
```

It returned exit code 0, `status=pass`, five metrics, and
`figures=not_requested` in 4.299551 seconds.
A second no-argument execution through `runpy.run_path(...,
run_name="__main__")` measured 16.871434 seconds with tracing enabled and a
`tracemalloc` peak of 82,137,039 bytes (78.332 MiB). This is the peak of traced
Python allocations, not process RSS; tracing overhead explains the longer run.

The clean-state direct bundle is at:

```text
.verification/session3/refresh-direct-root/artifacts/finite_counterexample/ecb50ab6806a296629778ecbd9965859c4de5b99df406a7a1b408acf3efc9af0-20260809
```

Its canonical configuration hash is
`ecb50ab6806a296629778ecbd9965859c4de5b99df406a7a1b408acf3efc9af0`.
The finalized manifest binds revision
`ab747008b970c0c6a162be1ee1501a9baa163cb3`, `git_dirty=false`, the empty
Git-status SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`,
theory digest
`a7fddfcb8c67dbec71c7a35d0e415313a38154719e05d6ccd73672a810939343`,
CPU/float64 effective execution, exact-rational arithmetic, Python 3.14.4,
NumPy 2.4.4, SciPy 1.17.1, and named RNG streams rooted at seed 20260809. The
finalized clean manifest SHA-256 is
`8932a9d28b0c28a67d08113dc5e94da3cc895974bebb397bcf85d9e3325dfb41`.

## Finalized artifacts and deterministic replay

The manifest is complete and declares exactly the two core files, six semantic
artifacts, and optional diagnostics. The four frozen catalog JSON artifacts are
`enumeration_bounds.json`, `candidate_records.json`,
`minimal_witnesses.json`, and `stress_matrix.json`. `metrics.json` contains the
five-metric inventory, and `arrays.npz` contains primitive numerator,
denominator, permutation, shape, axis, and retained-order arrays sufficient to
recompute every metric independently.

| Semantic artifact | SHA-256 |
|---|---|
| `metrics.json` | `054ffdaa5d144e571fc350d61b97aab91a1dc3fab5949924da5397723a28615e` |
| `enumeration_bounds.json` | `005e898f09c39b2d20612bfce0a1e4a7debb2672ae746b64b6e69b793dd52b68` |
| `candidate_records.json` | `03261b75f6b71b8df7a24c769c0c8605509e11e95bbe4ab9f39bc54d91251f79` |
| `minimal_witnesses.json` | `d9b09e5b149e4fb3b1dcf3756d4a5318aba297f00aa45d091d5858045c8ca979` |
| `stress_matrix.json` | `04ad19a198e3130118dc657acc053e4f6a3be250ed484e333c1d9de194c9c576` |
| `arrays.npz` | `7ec5bfbfd5c1acc5de06618edfa53ee6400902b4474d0cce8bdd6ef7dfc40316` |

Independent executions under `.verification/session3/replay-refresh-a` and
`.verification/session3/replay-refresh-b` produced byte-identical copies of all six
semantic artifacts. Their configuration hashes differed
(`b9ee9065...9efa` versus `68c54027...9ff0`) because the output-root strings are
part of the canonical configuration; removing only those root values left the
resolved configurations identical. Thus the scientific bytes, not the
root-sensitive bundle identity, are the determinism claim.

The requested enumeration bounds were four states and denominator eight. The
saved effective exhaustive bounds were deliberately smaller and explicit:
two-state laws and 2-by-2 channels through denominator four, plus three binary
action axes with values in `{-1, 0, 1}`. The run enumerated 7 laws, 49
channels, 6,561 actions, 19,588 candidates, and 5 globally minimal witnesses.
The requested bounds must not be mistaken for the effective exhaustive domain.

Every candidate and minimal witness carries exactly the required fields:
`claim_id`, `inside_declared_domain`, `assumptions_satisfied`,
`smallest_witness`, `exact_or_numeric`, `observed_residual`, `classification`,
`theorem_status`, `verification_state`, and `claim_origin`.

## Exact oracles, metamorphics, and negative controls

| Control | Reproduced value and classification |
|---|---|
| Support extended real | `q=(1,0)`, `p=(0,1)` returns `is_infinite=true`, no numeric value, and support violation index `(0,)`; no `inf - inf` residual is formed. |
| Parameter-dependent channel | At launcher `theta=1/4`, the fixed-channel score-gap control is exactly `1/8`; the globally smallest saved witness has `theta=1`, residual `2`, and is an `assumption_boundary`. The focused literal at `theta=1/3` is `2/9`. |
| Coherent versus one-sided relabeling | Relabeling both laws preserves KL exactly. Relabeling only `q=(3/4,1/4)` against unchanged `p` gives `ln(3)/2 = 0.5493061443340548`; this is outside the coherent-relabeling premises and is an `assumption_boundary`. |
| Source mass versus beta alone | The launcher fixture gives maximum gap `1/2`. The focused oracle maps source `(3/4,1/4)` to joint diagonal masses `(3/4,1/4)`, whereas beta-only averaging gives `(1/2,1/2)`. |
| Higher-order versus pairwise retention | A three-axis order-three action has exact order-three component `1` and pairwise omitted residual `1`. The exhaustive minimal witness has residual `1/8`; both show that pairwise retention does not reconstruct the higher-order fixture. |
| Channel orientation/order | Composing `[[1,0],[1/2,1/2]]` then `[[1/3,2/3],[1,0]]` gives `[[1/3,2/3],[2/3,1/3]]`; one further correctly oriented composition gives `[[2/3,1/3],[5/6,1/6]]`. An incompatible reversed/order-typed composition is rejected rather than coerced. |
| Deep composition | Three saved nontrivial channels produce identical direct and staged rows `[[1/2,1/2],[3/8,5/8]]` with exact residual `0`. |
| Retained-space and relabeling | The coherent retained projection reports `true` and residual `0`; holding the action fixed while requesting a nontrivial relabel reports `false`. The saved pairwise retained-space control records omitted residual `1`. |
| Tolerance scaling | Base `1/100` across two states scales exactly to `1/50`; the focused stress oracle maps `1/1000` across eight states to `1/125`. |
| Conditioning | `diag(1,4)` is accepted with dimension 2 and exact condition 4. The published near-singular stress matrix is the strictly positive-definite `diag(1,10^-100)`: its saved exact condition score is `10^100`, above the `10^12` boundary, so it is rejected with reason `near-singular SPD input exceeds the exact conditioning boundary`. A separate focused unit control rejects a singular matrix, but the published stress witness is SPD. |

The primitive array bundle was independently reloaded as `Fraction` objects
and used to recompute the support violation, `1/8` channel gap, `ln(3)/2`
one-sided KL, `1/2` source-mass gap, and order-two retained residual `1`. This
check does not call the experiment's metric-building path.

Invalid experiment, CUDA, and figure requests are tested to fail before RNG,
provenance, or `RunStore.create` seams. A sanitized subprocess test removes
`PYTHONPATH`, runs from a temporary directory without an editable install, and
asserts that Torch is not imported. The laboratory exposes no figures, so a
figure request is rejected before numerical publication rather than isolated
through a renderer.

## Claim, evidence, and falsifier ledger

| Claim | `theorem_status` | `verification_state` | `claim_origin` | Evidence type | Falsification condition |
|---|---|---|---|---|---|
| Structured support violations are represented without numeric infinity subtraction. | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `PROJECT_NOVEL` | Exact literal oracle, focused test, primitive-array replay | A supported run emits a finite residual or evaluates an undefined infinity subtraction. |
| The pinned parameter-dependent-channel fixture has nonzero gap `1/8`. | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Exact `Fraction` recomputation and artifact metric | The same literal fixture recomputes a different rational value. This would challenge the implementation/control, not refute the fixed-channel theorem because the channel depends on the parameter. |
| One-sided relabeling has KL gap `ln(3)/2`. | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `STANDARD` | Independent literal logarithmic oracle and artifact metric | The pinned two-state laws give a value other than `ln(3)/2`. This is not a coherent-relabeling theorem refutation. |
| Omitting source masses changes the pinned marked-event pushforward by `1/2`. | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `PROJECT_NOVEL` | Exact joint tables and primitive-array replay | Source-weighted and beta-only tables agree on the pinned nonuniform source fixture. |
| Pairwise retention omits residual `1` on the pinned order-three action. | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `PROJECT_NOVEL` | Exact Hoeffding components, mutation control, primitive-array replay | Order-two projection exactly reconstructs the pinned nonzero order-three component. |
| The effective finite catalog is exhaustively enumerated and deterministically serialized at this revision. | `NUMERICAL` | `EVIDENCE_VERIFIED` | `PROJECT_NOVEL` | Saved bounds/counts, 19,588 field-checked records, two-root byte hashes | An admissible object within the saved effective bounds is omitted, a smaller witness exists under the saved ordering, or semantic hashes differ across an otherwise identical replay. |
| All outside-domain witnesses are assumption-boundary examples. | `ESTABLISHED` | `EVIDENCE_VERIFIED` | `PROJECT_NOVEL` | Candidate schema validation and constructor rejection of an outside-domain theorem-refutation label | Any serialized outside-domain record is labeled as a theorem refutation or as satisfying the violated assumptions. |

`EVIDENCE_VERIFIED` in this table closes the stated implementation or finite-run
check at the tested revision. It does not elevate finite evidence into a proof
of the underlying mathematical statement.

## Open obligations

- Continuum, nondominated-law, infinite-volume, and two-index limits remain
  `OPEN` and are not assessed by this finite enumerator.
- Universality, nonlinear attraction, and any physical interpretation of scale
  or time remain `OPEN`.
- The Gaussian conditioning controls exercise small declared SPD fixtures only;
  general Gaussian-law applicability remains `OPEN` and its verification state
  is `INCONCLUSIVE` here.
- Applicability to an external multi-agent system requires that system's
  explicit laws, channels, actions, and theorem premises. No such application
  is supplied, so external applicability is `INCONCLUSIVE`.
- Cross-producer metamorphics and stress checks against Sessions 1, 2, 4, 5,
  and 6 are deferred to the serial Wave-3 integration revision and remain
  `INCONCLUSIVE` in this lane.
- The exhaustive statement is limited to the saved effective bounds. Coverage
  of the larger requested bounds is `OPEN`; no result here supports a claim
  beyond the enumerated domain.
