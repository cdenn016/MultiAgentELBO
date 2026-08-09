# Retrospective Task 5 categorical-DQM TDD evidence

## Provenance and limitation

This is a retrospective tracked transcription of the ignored coordination
report `.superpowers/sdd/2026-08-09-attention-categorical-dqm-labs/task-5-report.md`.
It preserves that report's staged RED/GREEN commands, observed failure
identities and results, self-review regression, final selection, and later fix
rounds. It is process evidence copied into the tracked tree after the work; it
does not make the original intermediate working trees Git-reconstructible and
does not turn console evidence into analytic proof.

| Source property | Recorded value |
|---|---|
| SHA-256 | `47ED3EB419947D922ABE2CBE2130F65FACDAF602EDF7091D8E7E75852ECF4CD8` |
| Local creation time (UTC) | `2026-08-09T18:50:53.0591194Z` |
| Local last-write time (UTC) | `2026-08-09T19:08:40.1730059Z` |
| Initial Task 5 commit | `847c928` (`feat: add parametric categorical DQM analysis`) |
| Task 5 owned files | `categorical.py`, `categorical_dqm.py`, `test_categorical_dqm.py` |

## Staged RED/GREEN record

### Stage 1: exact family and hand-derived oracles

RED command:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5-stage1-red"
```

RED identity/result (exit 1):

```text
ERROR collecting tests/test_categorical_dqm.py
tests\test_categorical_dqm.py:9: in <module>
    from multiagent_elbo.finite.categorical import CategoricalExponentialFamily
E   ModuleNotFoundError: No module named 'multiagent_elbo.finite.categorical'
1 error in 0.12s
```

GREEN command:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5-stage1-green"
```

GREEN result:

```text
.....                                                                    [100%]
5 passed in 0.09s
```

### Stage 2: independent fine and pushed centered differences

RED command:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5-stage2-red"
```

RED identity/result (exit 1):

```text
ERROR collecting tests/test_categorical_dqm.py
tests\test_categorical_dqm.py:10: in <module>
    from multiagent_elbo.finite.categorical_dqm import (
E   ModuleNotFoundError: No module named 'multiagent_elbo.finite.categorical_dqm'
1 error in 0.13s
```

GREEN command:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5-stage2-green"
```

GREEN result:

```text
.......                                                                  [100%]
7 passed in 0.09s
```

### Stage 3: Fisher decomposition and both signed DQM ladders

RED command:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5-stage3-red"
```

RED identity/result (exit 1):

```text
ERROR collecting tests/test_categorical_dqm.py
tests\test_categorical_dqm.py:10: in <module>
    from multiagent_elbo.finite.categorical_dqm import (
E   ImportError: cannot import name 'analyze_categorical_dqm' from 'multiagent_elbo.finite.categorical_dqm' (C:\tmp\MultiAgentELBO-attention-dqm-20260809\src\multiagent_elbo\finite\categorical_dqm.py)
1 error in 0.13s
```

GREEN command:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5-stage3-green"
```

GREEN result:

```text
.........                                                                [100%]
9 passed in 0.09s
```

### Stage 4: malformed/support/perturbation boundaries

RED command:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5-stage4-red"
```

RED identity/result (exit 1; Boolean theta was silently coerced before the
guard):

```text
.................F.........................                              [100%]
_ test_family_rejects_boolean_wrong_shape_and_nonfinite_theta[theta0-Boolean] _

>       with pytest.raises((TypeError, ValueError), match=message):
E       Failed: DID NOT RAISE any of (<class 'TypeError'>, <class 'ValueError'>)

tests\test_categorical_dqm.py:212: Failed
1 failed, 42 passed in 0.14s
```

GREEN command:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5-stage4-green"
```

GREEN result:

```text
...........................................                              [100%]
43 passed in 0.10s
```

## Self-review regression: partial directional round-back

The first guard rejected only a perturbation whose entire vector equaled
theta. It allowed a nonzero direction coordinate to round back if another
coordinate still changed. The focused regression was added before tightening
the guard.

RED command:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py -k partial_round_back --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5-self-review-red"
```

RED identity/result:

```text
F                                                                        [100%]
_ test_dqm_ladder_rejects_partial_round_back_in_a_nonzero_direction_coordinate _

>       with pytest.raises(ValueError, match="rounds back"):
E       Failed: DID NOT RAISE <class 'ValueError'>

tests\test_categorical_dqm.py:310: Failed
1 failed, 43 deselected in 0.10s
```

GREEN command:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py -k partial_round_back --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5-self-review-green"
```

GREEN result:

```text
.                                                                        [100%]
1 passed, 43 deselected in 0.06s
```

## Initial final selection

The report records this exact post-commit command at `847c928`:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py tests/test_fisher.py tests/test_measures.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5"
```

Result:

```text
.......................................................................  [100%]
71 passed in 0.12s
```

`git diff --cached --check` passed before that commit. An optional concurrent
`compileall` was explicitly excluded from closure evidence after it raced
pytest for the same `__pycache__` replacements and received `PermissionError`;
the isolated 71-test selection imported and executed the three modules.

## Fix round 1: doubled finite-difference denominator overflow

Commit: `09ebd3c` (`fix: avoid centered-difference step overflow`). The focused
regressions pin fine secants `((1e-308,),(-1e-308,))` and pushed swap-channel
secants `((-1e-308,),(1e-308,))` at `step=1e308`.

RED command:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py -k overflowing_doubled_step --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5-fix1-red"
```

RED identities/result:

```text
FF                                                                       [100%]
FAILED tests/test_categorical_dqm.py::test_centered_fine_difference_avoids_overflowing_doubled_step
  ACTUAL: array([[ 0.], [-0.]])
  DESIRED: array([[ 1.e-308], [-1.e-308]])
FAILED tests/test_categorical_dqm.py::test_centered_pushed_difference_avoids_overflowing_doubled_step
  ACTUAL: array([[-0.], [ 0.]])
  DESIRED: array([[-1.e-308], [ 1.e-308]])
2 failed, 44 deselected in 0.13s
```

GREEN command:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py -k overflowing_doubled_step --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5-fix1-green"
```

GREEN result:

```text
..                                                                       [100%]
2 passed, 44 deselected in 0.09s
```

Post-commit selection at `09ebd3c`:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py tests/test_fisher.py tests/test_measures.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5-fix1"
```

```text
........................................................................ [ 98%]
.                                                                        [100%]
73 passed in 0.12s
```

## Fix round 2: genuine underflow-warning coverage

Commit: `394083d` (`fix: silence expected subnormal quotient warning`). The
round-1 tests had inherited NumPy's default `under="ignore"`; the revised tests
explicitly set `np.errstate(under="warn")` while promoting `RuntimeWarning` to
an exception.

RED command:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py -k overflowing_doubled_step --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5-fix2-red"
```

RED identities/result:

```text
FF                                                                       [100%]
FAILED tests/test_categorical_dqm.py::test_centered_fine_difference_avoids_overflowing_doubled_step
src\multiagent_elbo\finite\categorical_dqm.py:133: in _centered_quotient
E   RuntimeWarning: underflow encountered in divide
FAILED tests/test_categorical_dqm.py::test_centered_pushed_difference_avoids_overflowing_doubled_step
src\multiagent_elbo\finite\categorical_dqm.py:133: in _centered_quotient
E   RuntimeWarning: underflow encountered in divide
2 failed, 44 deselected in 0.11s
```

Focused GREEN command at `394083d`:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py -k overflowing_doubled_step --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5-fix2-green-postcommit"
```

Focused GREEN result:

```text
..                                                                       [100%]
2 passed, 44 deselected in 0.10s
```

Full GREEN command at `394083d`:

```powershell
C:\Python314\python.exe -m pytest -q -p no:cacheprovider tests/test_categorical_dqm.py tests/test_fisher.py tests/test_measures.py --basetemp="C:\tmp\multiagent-elbo-attention-dqm-task5-fix2"
```

Full GREEN result:

```text
........................................................................ [ 98%]
.                                                                        [100%]
73 passed in 0.13s
```

The final fix suppresses underflow only around the large-step division that
intentionally returns representable subnormal secants. The recorded tests show
that both intended subnormal results survive `under="warn"` without leaking a
`RuntimeWarning`; the fixed-channel and finite-family scope boundaries remain.
