# Attention and categorical DQM laboratory results - 2026-08-09

## Outcome and scope

The marked-event attention and categorical DQM laboratories each produced a
complete finalized numerical bundle with 18 of 18 declared metrics passing.
Pure saved-artifact replay produced a deterministic 300-DPI PNG and vector PDF
for each laboratory without changing either numerical bundle. The launcher
integration tests also exercised both click-to-run files as direct no-argument
subprocesses from sanitized temporary working directories.

These are exact finite-fixture and numerical implementation diagnostics. The
attention results do not establish a theorem for arbitrary marked kernels or
learned attention systems. The categorical DQM results numerically corroborate
the separately recorded finite-support Taylor derivation; the finite remainder
ladder is not itself an analytic proof. No sampling, error bars, sample sizes,
or significance tests apply to these deterministic fixtures.

## Revision, environment, and provenance

| Item | Recorded value |
|---|---|
| Run-time Git commit | `b5ffae72e14fe23bea1b8837c9a979528feec436` |
| Run-time tracked/untracked state | Dirty and content-bound in each manifest |
| Dirty-tree SHA-256 | `c2186c0e1a6707b1230a90b3479d5bbbd49c234b6f14813ddac6a38e78ee04f8` |
| Git-status SHA-256 | `2a230edd26de058baaadbe66bc37bf4d886479cf58c6444e759bb86afc4d7b5b` |
| Theory-tree SHA-256 | `a7fddfcb8c67dbec71c7a35d0e415313a38154719e05d6ccd73672a810939343` |
| Root seed | `20260809` |
| Python | `3.14.4`, MSC v.1944, 64 bit |
| Platform | `Windows-10-10.0.19045-SP0` |
| NumPy | `2.4.4` |
| SciPy | `1.17.1` |
| Matplotlib | `3.10.8` |

The two launchers were imported and only the in-memory `OUTPUT.root` value was
changed. Their committed defaults were not edited for reproduction. Both runs
kept `collect_diagnostics=true` and `render_figures=false`; therefore each run
contains `diagnostics.npz` but no coupled figure directory. Figures were
subsequently rendered through the pure saved-artifact replay interface.

## Exact resolved configurations

Attention config hash:
`c2d092e1da479cc613407934dae255f7503b2c61dd6c273c2fe111daedfd179e`

```json
{"numerics":{"atol":1e-12,"dtype":"float64","max_frame_condition":1000000.0,"min_spd_rcond":1e-12,"rtol":1e-10},"output":{"collect_diagnostics":true,"render_figures":false,"root":"C:\\tmp\\multiagent-elbo-attention-dqm-task8-reproduced-20260809\\runs"},"run":{"name":"attention_marked_event","seed":20260809},"theory":{"experiment":"attention_marked_event","fixture":"nested_nonuniform_v1"}}
```

Categorical DQM config hash:
`5dd2ec6b382aa656523ffa268747f5812fd567cfc09cfcb95f7ffdc064798ed8`

```json
{"numerics":{"atol":1e-12,"dtype":"float64","max_frame_condition":1000000.0,"min_spd_rcond":1e-12,"rtol":1e-10},"output":{"collect_diagnostics":true,"render_figures":false,"root":"C:\\tmp\\multiagent-elbo-attention-dqm-task8-reproduced-20260809\\runs"},"run":{"name":"categorical_dqm","seed":20260809},"theory":{"dqm_step_sizes":[0.1,0.05,0.025,0.0125],"experiment":"categorical_dqm","finite_difference_step":1e-05,"fixture":"three_category_softmax_v1","theta":[0.6931471805599453,1.0986122886681098]}}
```

## Marked-event attention laboratory

Finalized run:

`C:\tmp\multiagent-elbo-attention-dqm-task8-reproduced-20260809\runs\attention_marked_event\c2d092e1da479cc613407934dae255f7503b2c61dd6c273c2fe111daedfd179e-20260809`

The manifest is complete. Its inventory contains `arrays.npz`, `config.json`,
`diagnostics.npz`, `manifest.json`, and `metrics.json`.

| Metric | Value | Tolerance | Status |
|---|---:|---:|---|
| `ATT-01_factorization_residual` | `2.77555756156289e-17` | `1.01e-10` | pass |
| `ATT-01_normalization_residual` | `2.22044604925031e-16` | `1.01e-10` | pass |
| `ATT-02_direct_staged_active_beta_residual` | `1.11022302462516e-16` | `1.01e-10` | pass |
| `ATT-02_direct_staged_alpha_residual` | `5.55111512312578e-17` | `1.01e-10` | pass |
| `ATT-02_direct_staged_eta_residual` | `2.77555756156289e-17` | `1.01e-10` | pass |
| `ATT-02_literal_active_beta_residual` | `1.11022302462516e-16` | `1.01e-10` | pass |
| `ATT-02_literal_alpha_residual` | `1.11022302462516e-16` | `1.01e-10` | pass |
| `ATT-02_literal_eta_residual` | `5.55111512312578e-17` | `1.01e-10` | pass |
| `ATT-02_reverse_bridge_residual` | `1.11022302462516e-16` | `1.01e-10` | pass |
| `ATT-03_broken_link_gap_control` | `0.2109948564038245` | `1.01e-10` | pass |
| `ATT-03_gauge_alpha_residual` | `0` | `1.01e-10` | pass |
| `ATT-03_gauge_beta_residual` | `2.77555756156289e-17` | `1.01e-10` | pass |
| `ATT-03_gauge_eta_residual` | `2.77555756156289e-17` | `1.01e-10` | pass |
| `ATT-03_gauge_logits_residual` | `2.22044604925031e-16` | `1.01e-10` | pass |
| `ATT-04_incoherent_relabeling_gap_control` | `0.39062499999999994` | `1.01e-10` | pass |
| `ATT-04_relabeling_naturality_residual` | `0` | `1.01e-10` | pass |
| `ATT-NEG-01_beta_only_associativity_gap` | `0.10000000000000003` | `1.01e-10` | pass |
| `ATT-NEG-01_beta_only_correct_gap` | `0.04999999999999999` | `1.01e-10` | pass |

Numerical bundle SHA-256 values:

| File | SHA-256 |
|---|---|
| `arrays.npz` | `a5c73a04da2ced52b51ad3b23687453cec407ae2a9d1f593cda04c1bffc7b8bc` |
| `config.json` | `509f4890668cba3b1b702ea6371a200b83045353dd948db13b39b6962b530722` |
| `diagnostics.npz` | `d886af4f70709ad2e975c33e54588c6d78fa1d53357aa034660861c97de384a3` |
| `manifest.json` | `ad72855db4274efc1afce9e37e7602eebf54ada5a9d5682c155383c49918ff5d` |
| `metrics.json` | `bcce3b20050914f2953176ce951b22aa6de66f17093c7a650ec58ad425b303fe` |

## Categorical DQM and Fisher laboratory

Finalized run:

`C:\tmp\multiagent-elbo-attention-dqm-task8-reproduced-20260809\runs\categorical_dqm\5dd2ec6b382aa656523ffa268747f5812fd567cfc09cfcb95f7ffdc064798ed8-20260809`

The manifest is complete with the same five-file inventory shape as the
attention run.

| Metric | Value | Tolerance | Status |
|---|---:|---:|---|
| `DQM-01_finite_difference_score_residual` | `1.78369541359302e-11` | `1.01e-10` | pass |
| `DQM-01_literal_probability_residual` | `1.11022302462516e-16` | `1.01e-10` | pass |
| `DQM-01_literal_score_residual` | `1.11022302462516e-16` | `1.01e-10` | pass |
| `DQM-01_negative_remainder_ladder_monotonicity` | `-0.0007022389056087949` | `0` | pass |
| `DQM-01_normalization_residual` | `2.22044604925031e-16` | `1.01e-10` | pass |
| `DQM-01_positive_remainder_ladder_monotonicity` | `-0.0007008471695697045` | `0` | pass |
| `DQM-01_score_centering_residual` | `7.40148683083438e-17` | `1.01e-10` | pass |
| `DQM-01_two_sided_remainder_final` | `0.0007017902174741355` | `0.0125` | pass |
| `INF-02_conditional_score_fd_residual` | `1.80370163249677e-11` | `1.01e-10` | pass |
| `INF-02_fisher_defect_min_eigenvalue` | `0.06666666666666668` | `1.01e-10` | pass |
| `INF-02_fisher_identity_residual` | `4.16333634234434e-17` | `1.01e-10` | pass |
| `INF-02_literal_coarse_fisher_residual` | `2.77555756156289e-17` | `1.01e-10` | pass |
| `INF-02_literal_coarse_probability_residual` | `1.11022302462516e-16` | `1.01e-10` | pass |
| `INF-02_literal_conditional_score_residual` | `1.11022302462516e-16` | `1.01e-10` | pass |
| `INF-02_literal_fine_fisher_residual` | `2.77555756156289e-17` | `1.01e-10` | pass |
| `INF-02_literal_fisher_defect_residual` | `1.38777878078145e-17` | `1.01e-10` | pass |
| `INF-02_positive_loss_trace_control` | `0.1380952380952381` | `1.01e-10` | pass |
| `INF-NEG-01_wrong_weight_gap` | `0.1904761904761905` | `1.01e-10` | pass |

Numerical bundle SHA-256 values:

| File | SHA-256 |
|---|---|
| `arrays.npz` | `5987ac6add5beb921e83c9e097015be7334c730b86fc359f88939a7df594d462` |
| `config.json` | `bcf6c549341b437ff51141f59de5f5343209d7a154856f132a98c7a4c1664af5` |
| `diagnostics.npz` | `5a2812a37e101cb4a9ad96485176f0d1b59dd3636294d87917efe54656b0a973` |
| `manifest.json` | `7736fa195ae6e75b4465112dde135949e3a33be14c1b430bf6847c0ebafa9419` |
| `metrics.json` | `033e126b0a424ac8a05b7e5cb20eb16436d7815b71aa532e25cc549786102450` |

The finite-support analytic DQM argument and the numerical checks have different
roles. Positivity and smoothness of this categorical exponential family admit
the Taylor expansion used for the analytic DQM statement. The centered finite
difference comparisons, two-sided normalized-remainder ladder, Fisher identity,
and wrong-weight controls test the implementation at the declared fixture and
finite steps. They do not replace the derivation or generalize it beyond the
declared family and fixed parameter-independent coarse channel.

## Pure saved-artifact figures

Final attention replay:

`C:\tmp\multiagent-elbo-attention-dqm-final-fix1-panel-c-replays-20260809\attention`

| File | SHA-256 |
|---|---|
| `attention-composition.png` | `632f4421bca828c8c65852b7aeae2951c9072fd565d5aa8a978ffef96303ebb6` |
| `attention-composition.pdf` | `7ed36223d64763e2f2d1b40ba5807fba0b4c4e6a5109b14f1f7651e3f758495b` |

Final categorical DQM replay:

`C:\tmp\multiagent-elbo-attention-dqm-final-fix1-panel-c-replays-20260809\categorical_dqm`

| File | SHA-256 |
|---|---|
| `categorical-dqm-diagnostic.png` | `d6a1be6daec5c5abde56e01e84b43160a5c6847717e418841f36555911ee748b` |
| `categorical-dqm-diagnostic.pdf` | `316e560325f62fc209d97538100a2ce6f358a285e06e872064d2bbe411dc0045` |

Both manifests are complete and record 300 DPI. Each PNG is exactly 1050
pixels wide and each PDF MediaBox is exactly 252 points wide, yielding the
required 3.5-inch physical width. Repeat replay into independent directories
produced the same four SHA-256 values, and before/after hashes confirmed no
change to either numerical bundle.

A current replay of the protected foundation bundles also reproduced every
legacy byte exactly: finite PNG
`a5d8cff7a8960c116204533dbcb7b85feb212f8dc46ee3e1f144f0275e45d8a8`,
finite PDF
`c0b623960154466c5f681727c16d7e62cc7dc2cc87aba12a9af6d316633d8172`,
Gaussian PNG
`430c015843854db663b588e9b4927254f6524d9a77d3f1a32b6d595a78acad45`,
and Gaussian PDF
`4903791c7a2f99d979723901abf5a9810e8c162d56e334ffb474d332d5cf0ddd`.

The attention caption states: "Exact finite marked-event composition diagnostic
from finalized saved artifacts at final-state probabilities (0.666667,
0.333333); no sampling, error bars, or significance tests."

The DQM caption states: "Categorical DQM numerical diagnostic from finalized
saved artifacts at theta=(0.693147, 1.09861), direction=(0.6, -0.8), and step
range [0.0125, 0.1]; analytic/finite-difference agreement and the finite
remainder ladder are implementation checks, not an analytic proof."

Original-resolution visual inspection of these fresh replays confirmed that the
attention panels name final states `w0` and `w1`, and that the DQM step axis shows
only `0.0125`, `0.025`, `0.05`, and `0.1` without conflicting minor labels. No
text is clipped or overlapping. Panel C is inside the upper-left of its axes
and is visually clear of every major/minor y-tick label, the title, the data, and
the legend. Final-size labels remain readable; the axes are restrained without
chart junk; and accessible Okabe-Ito colors are reinforced by distinct marker
and line-style encodings. Renderer-construction regressions independently check
the state labels, fixed step labels, absence of minor-label text, panel-C
separation, exact width, and canvas containment at 1050-pixel export geometry.

## Launcher and machine-test evidence

The launcher tests import each file with invalid `sys.argv` without writes or
argument-parser attributes, override only `OUTPUT.root` for `main()`, and run
each file directly with no arguments from a sanitized temporary working
directory with `PYTHONPATH` set to the empty string. Each direct run reports
`status=pass` and creates exactly one complete manifest.

The final post-review JUnit evidence generated on source revision `cc863e4` is
`docs/verification/pytest-foundation.xml` with SHA-256
`e4b595e859444539840dac867c3ea35c860fd599c90433800484e91678a8150c`.
Counts were parsed from the XML rather than inferred from console progress.

| Tests | Passed | Failures | Errors | Skipped | Time |
|---:|---:|---:|---:|---:|---:|
| 385 | 383 | 0 | 0 | 2 | 18.543 s |

The consolidated fix added three figure regressions. The state/tick focused
result is `2 passed, 22 deselected`; the panel-C focused result is
`1 passed, 24 deselected`; and the plan's integrated figure/launcher/attention/
DQM slice is `65 passed`. After the final scoped source re-review approved the
fix with no remaining findings, the full suite above was rerun. Final-revision
ledger binding remains a separate control-plane step.

Both skips are Windows symbolic-link cases for which the test account returned
WinError 1314: `test_finalize_rejects_a_declared_symlink` and
`test_validated_renderer_status_rejects_a_publication_symlink_escape`. They are
environment coverage limitations and are not evidence that those symlink paths
executed.

## Independent review and remaining boundaries

The durable review record is `docs/verification/independent-reviews.md`.
Earlier task-scoped reviews pinned the attention gauge action, hardened DQM
finite-difference step controls and warnings, and added positive-loss and
monotonicity controls before this integration. The broad whole-branch review
found no Critical or Important source, mathematics, or test defect. Its two
Minor figure/process findings were corrected, and the final scoped re-review at
`cc863e4` reported no remaining findings. Verification-ledger binding remains
deliberately separate from that source-review verdict.

The results leave open arbitrary categorical families, parameter-dependent or
learned coarse channels, continuum limits, nontrivial connections or holonomy,
learned marked-event kernels, and empirical attention performance. They neither
establish RG attraction/universality nor change any frozen Theory statement.
