# Claude Opus remediation closure evidence

Source/theory revision: `76af87b` (`fix: reconcile finite VFE theory and verifier`).

All executable checks used `C:\Python314\python.exe`, `CUDA_VISIBLE_DEVICES=-1`, and
`PYTHONHASHSEED=0`. They make no CUDA claim.

## Artifacts

| Artifact | Machine-readable result | Bytes | SHA-256 |
|---|---:|---:|---|
| `full-cpu.junit.xml` | 1,182 tests; 1,166 passed; 16 skipped; 0 failures/errors | 186166 | `6dd6813ce01731399d800c24e9c9abe5eeed121f377092aaed1e01c2b86015c2` |
| `verifier-independent.junit.xml` | 183 tests; 170 passed; 13 skipped; 0 failures/errors | 35256 | `119ceff248ca8918bf336812ca925a45a0963963cedd661fbbdc8afb446a68d5` |
| `theory-focused.junit.xml` | 28 tests; 28 passed; 0 skipped/failures/errors | 4477 | `99bea732f3e96b41bb40455e97fc308475559091f077bff6ae7395930557377d` |

## Commands

```powershell
C:\Python314\python.exe -m pytest -q `
  --junitxml=C:\tmp\maelbo-opus-remediation-full-20260813.xml `
  --basetemp=C:\tmp\maelbo-opus-remediation-full-20260813

C:\Python314\python.exe -m pytest `
  tests/test_remediation_evidence.py `
  tests/test_attention_experiment.py::test_attention_launcher_import_is_side_effect_free_and_main_is_click_to_run `
  tests/test_categorical_dqm_experiment.py::test_categorical_dqm_launcher_is_import_safe_and_main_honors_output_override `
  -q --junitxml=C:\tmp\multiagentelbo-verifier-final-review-20260813T1.xml

C:\Python314\python.exe -m pytest `
  tests/test_markdown_hygiene.py tests/test_presentation_descent_witness.py `
  tests/test_meta_agent_coherence_witness.py tests/test_shared_latent_coupling_witness.py `
  -q --junitxml=C:\tmp\maelbo-theory-docs-preflight-20260813.xml
```

The two rigorous-theory packages were separately checked with the installed
`rigorous-theory-search/scripts/validate_run.py --mode release`; both exited zero.
