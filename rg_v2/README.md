# Local-First Renormalization v2

This is a repository-local CPU laboratory, not an installed
`multiagent_elbo` package. Run its focused regression gate from the repository
root with:

```powershell
$env:CUDA_VISIBLE_DEVICES = "-1"; $env:PYTHONHASHSEED = "0"
C:\Python314\python.exe -B -m pytest tests\rg_v2\test_legacy_regression.py -q -p no:cacheprovider
```

The dependency is one-way: `rg_v2` may use stable public
`multiagent_elbo` primitives, while installed-package source must not import
`rg_v2`. Release 1 admits the fixture IDs `lf3_product_v1`,
`lf3_correlated_v1`, and `lf3_dirac_boundary_v1`; the separate
`legacy-rescaling-v1` manifest freezes pre-v2 behavior.

The Release 1 run contract will publish six semantic artifacts:
`fixture_snapshot.json`, `population_joint.json`,
`population_inference.json`, `aggregate_datum.json`, `metrics.json`, and
`arrays.npz`. Its terminal constructed object is `AggregateDatum`; it is not a
coarse agent and has no evaluator, observation interface, or update rule.
