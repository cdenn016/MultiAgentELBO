# Wave 2 — Mutation analysis of the modules wave 1 did not cover

Date: 2026-08-12
Scope: the 16 modules named in the brief. Wave 1 mutation-tested the CORE modules and caught 10/10.
Execution policy: **CPU only. No GPU or CUDA job was started. `tests/test_cuda_backend.py` was excluded from every lane** (36 of its tests fail at baseline on this host anyway, on `ctypes.WinDLL` and hardcoded Windows interpreter paths).
Work was done on a copy at `/tmp/mae`. **The user's repository was never modified** — verification at the end.

---

## Headline

| | |
|---|---|
| **Overall mutation score** | **93 / 118 = 78.8 %** |
| Line coverage of the same 16 modules | **86 %** (statement+branch) |
| Modules at 100 % mutation score | 7 of 16 |
| Modules below 55 % | 3 of 16 — `finite_gauge.py` (33 %), `confirmatory_analysis.py` (33 %), `information_history.py` (50 %) |
| Cannot-fail assertions found | 3 (plus 1 weak-by-construction) |
| Invalid mutations discarded | 2 (see "Method honesty") |

The gap between 86 % line coverage and 78.8 % mutation score is not itself dramatic. What is dramatic is the *distribution*: coverage is flat (80–100 % everywhere) while the mutation score is bimodal. `confirmatory_analysis.py` has **80 % line coverage and a 33 % mutation score**. Every line of the primary statistical endpoint is executed; almost none of it is checked. That is the interesting quantity, and it is concentrated exactly in the module that decides whether the flagship experiment "supports" its conjecture.

---

## Baseline (reported honestly, before any mutation)

Host is Linux + Python 3.10.12; the repo targets Python 3.14 on Windows.

```
$ cd /tmp/mae && python3 -m pytest tests/ -q --no-header --co
891 tests collected, 1 error in 2.52s
ERROR tests/test_config.py  -  ModuleNotFoundError: No module named 'tomllib'   (stdlib only in 3.11+)

$ python3 -m pytest tests/ -q --no-header --ignore=tests/test_config.py
125 failed, 764 passed, 2 skipped in 150.54s
```

All 125 baseline failures are environmental, not mathematical. Grouped by file and root cause:

| File | Fails | Root cause |
|---|---|---|
| `test_cuda_backend.py` | 36 | `ctypes.WinDLL`, `powershell.exe`, GPU absent — **excluded, CPU-only policy** |
| `test_gaussian_fixed_ray_diagnostic_experiment.py` | 25 | `FileNotFoundError: 'C:\anaconda\python.exe'` |
| `test_gaussian_fixed_ray_experiment.py` | 17 | missing `docs/experiments/2026-08-09-gaussian-fixed-ray-preregistration.md`; CRLF digest tests |
| `test_theory_oracle_experiment.py` | 15 | `FileNotFoundError: 'C:\anaconda\python.exe'` |
| `test_gaussian_results_document.py` | 12 | source-binding hashes vs. Windows line endings |
| `test_launchers.py` | 9 | hardcoded `C:\Python314\python.exe` |
| 8 other `*_experiment.py` files | 11 | same hardcoded-interpreter / subprocess-launcher pattern |

This independently reproduces wave 1's finding **S6** (`run_checks.py:324` hardcodes `C:\Python314\python.exe`): the apparatus cannot be executed by an independent party. 32 of the failures are literally `FileNotFoundError: [Errno 2] No such file or directory: 'C:\anaconda\python.exe'`.

**Every pure-mathematics test module collects and passes.** No target module's unit tests were unrunnable, so no module had to fall back to reading-only.

### Lanes used as mutation oracles

- **MATH LANE** (primary, 20 s/run): 21 test files — every target module's unit tests plus `test_finite_experiment`, `test_gaussian_realization`, `test_measures`, `test_fisher`, `test_vfe`, `test_shared_scientific_contracts`, `test_scale_cocycle`.
  `476 tests collected, 476 passed, 0 failed` at baseline. A clean oracle: any new failure is caused by the mutation.
- **RECHECK LANES A–D** (integration/experiment files *not* in the math lane, with their own recorded baselines). Every mutation that survived the math lane was re-run against the lane containing the experiment tests for its module. Three survivors were demoted to CAUGHT by this step (FR3, FR5, FR8); the rest were confirmed.

*Note on test-order dependence:* three `test_shared_scientific_contracts.py` tests fail when that file is run in a 19-file lane and pass when run in the 21-file lane. Order/state dependence in the suite; not pursued further, but it is a latent flakiness.

### Harness

One mutation at a time; binary backup restored after every run; `find . -name '*.py.bak' | wc -l` asserted to be `0` after every batch.

---

## Method honesty — two mutations I discarded as invalid

Mutation testing is only meaningful if the mutant is semantically different. Two of my first-pass mutations were not, and I discarded them rather than count them as survivors:

- **A7** `first.matrix @ second.matrix` → `(second.matrix.T @ first.matrix.T)ᵀ`. This is the identity (AB)ᵀ = BᵀAᵀ — a **no-op**. Replaced by **A7b** (`second.matrix.T @ first.matrix.T`, no outer transpose), which was caught.
- **H6** `cell.boundary` → `tuple(cell.boundary)`, where `boundary` is already a tuple — a **no-op**. Replaced by **H6b** (`tuple(reversed(...))`), which was caught.

I also checked the one survivor where a no-op was plausible: **FR5** drops `/ ⟨r,r⟩` from a projector, which would be a no-op if `r` were a unit vector. It is not — `perron_ray = [1,1,1,1,1,1]`, `⟨r,r⟩ = 6.0` — so FR5 is a genuine mutation. (It survives for a different and more interesting reason; see F-8.)

---

## Per-module mutation table

`C` = caught, `S` = survived. "Which test" names the first/most specific failing test.

### `conditioning.py` — 4/5 (80 %)
| # | Mutation | Result | Which test |
|---|---|---|---|
| C1 | `rcond = min/max` → `max/min` | C | `test_conditioning.py::test_spectral_policy_rejects_correlated_matrix_old_proxy_false_accepted` (+9) |
| C2 | boundary band `<=` → `<` | **S** | — |
| C3 | `rcond < threshold` → `>` (fail/pass flip) | C | 41 tests across 4 files |
| C4 | drop `rtol·|threshold|` from the tolerance band | C | `test_threshold_band_is_inconclusive_and_tolerances_are_reachable` |
| C5 | `eigenvalues[0]`/`[-1]` swapped | C | same as C1 (+9) |

### `finite/attention.py` — 7/7 (100 %)
| # | Mutation | Result | Which test |
|---|---|---|---|
| A1 | `η = α⊗β` → `α · mean_i β` (conditional → marginal) | C | `test_from_alpha_beta_forms_literal_event_law_and_defensively_owns_inputs` |
| A2 | `disintegrate` sum axis 2 → 1 | C | `test_disintegrate_recovers_active_conditionals_and_masks_null_representatives` (+2) |
| A3 | drop the conditional normalization `η/α` | C | same (+2) |
| A4 | `masses @ M` → `M @ masses` | C | `test_state_and_node_pushforward_matches_literal_bridges_and_final_laws` |
| A5 | einsum `->zIJ` → `->zJI` | C | `test_node_pushforward_matches_every_literal_middle_and_coarse_base_state_value` (+1) |
| A6 | drop state-probability weighting in the joint | C | same (+1) |
| A7b | `compose_kernels` transposed composition | C | `test_compose_kernels_matches_literal_products_and_labels` |

### `finite/permutations.py` — 5/6 (83 %)
| # | Mutation | Result | Which test |
|---|---|---|---|
| P1 | `new_to_old`: inverse → identity assignment | C | `test_inverse_convention_mutation_is_detected` (+4) |
| P2 | `matrix` property transposed | **S** | — |
| P3 | `then`: composition order flipped | C | `test_inverse_and_composition_obey_the_literal_group_law` |
| P4 | `pullback_axis` uses forward map | C | `test_channel_pullback_reindexes_source_and_target_supports` (+3) |
| P5 | `argmax` axis 1 → 0 | C | `test_geometry_matrix_adapter_builds_the_same_permutation` |
| P6 | `pullback_law` uses forward map | C | `test_three_cycle_has_one_canonical_direction_and_explicit_inverse` (+2) |

### `geometry/attention_gauge.py` — 5/6 (83 %)
| # | Mutation | Result | Which test |
|---|---|---|---|
| G1 | `_softmax` max-shift removed | **S** | — |
| G2 | β softmax axis 1 → 0 | C | `test_literal_attention_logits_and_scalar_law_are_independently_pinned` (+1) |
| G3 | transport transposed `ijkl`→`ijlk` | C | same (+2) |
| G4 | covector law `solve(Fᵀ,·)` → `Fᵀ·` (Σ for Σ⁻¹) | C | `test_matched_single_node_frames_apply_pinned_action_and_preserve_scalars` |
| G5 | link congruence `solve(Sᵀ,Lᵀ)ᵀ` → `L Sᵀ` | C | same |
| G6 | `η = α[:,None]·β` → `α[None,:]·β` | C | `test_broken_link_control_changes_the_scalar_event_law_by_pinned_gap` (+1) |

### `finite/categorical.py` — 6/6 (100 %)
| # | Mutation | Result | Which test |
|---|---|---|---|
| CAT1 | `base + T·θ` → `base − T·θ` | C | 12 tests |
| CAT2 | `log p = s − log Z` → `+ log Z` | C | 25 tests |
| CAT3 | score `T − E[T]` → `T + E[T]` | C | 15 tests |
| CAT4 | `E_p[T]` → unweighted mean (cond exp → marginal) | C | 13 tests |
| CAT5 | Fisher drops the probability weighting | C | `test_family_matches_hand_derived_probability_score_and_fisher` (+3) |
| CAT6 | log-sum-exp max-shift removed | C | `test_dqm_ladder_rejects_a_directional_perturbation_that_rounds_back` (+1) |

### `finite/interactions.py` — 6/7 (86 %)
| # | Mutation | Result | Which test |
|---|---|---|---|
| I1 | conditional average → uniform mean | C | `test_nonuniform_product_reference_uses_declared_axis_weights` |
| I2 | Möbius inversion `−=` → `+=` | C | 11 tests |
| I3 | subset inclusion direction flipped | C | 11 tests |
| I4 | retained order `<=` → `<` | C | `test_pairwise_retention_reports_three_distinct_residual_norms` (+2) |
| I5 | `quotient_sup_norm` (max−min)/2 → sup\|·\| | **S** | — |
| I6 | drop reference renormalization | C | `test_tolerantly_accepted_references_are_normalized_before_projection` |
| I7 | weighted L2 drops the product-measure weights | C | 9 tests |

### `geometry/finite_gauge.py` — 2/6 (33 %) ← worst
| # | Mutation | Result | Which test |
|---|---|---|---|
| FG1 | channel congruence `Pᵀ C Q` → `P C Q` | **S** | — |
| FG2 | `channel_right` target pullback transposed | **S** | — |
| FG3 | `relabeled_q`: `m @ P` → `P @ m` | **S** | — |
| FG4 | axis references relabeled by the inverse | **S** | — |
| FG5 | KL invariance residual `−` → `+` | C | `test_componentwise_finite_relabeling_preserves_typed_observables_and_intertwines_projection` (+6) |
| FG6 | `expected_retained` not pulled back | C | same (+6) |

### `realizations/gaussian/interactions.py` — 6/7 (86 %)
| # | Mutation | Result | Which test |
|---|---|---|---|
| GI1 | prolongator `I` → `0.5·I` (restriction normalization) | C | 15 tests in `test_gaussian_realization.py` |
| GI2 | cluster self-blocks summed → averaged | C | 14 tests |
| GI3 | intra-cluster edge skip inverted | C | 15 tests |
| GI4 | parallel coarse edges overwritten, not accumulated | **S** | — |
| GI5 | Schur `rr − re·solved` → `+` | C | 13 tests |
| GI6 | Schur uses `ee` instead of `ee⁻¹` | C | 14 tests |
| GI7 | retained/eliminated index sets swapped | C | 15 tests |

### `realizations/gaussian/fixed_ray.py` — 9/10 (90 %)
| # | Mutation | Result | Which test |
|---|---|---|---|
| FR1 | drop the `2·` in `2 arcsin` | C | `test_projective_ray_angle_is_stable_for_nearly_parallel_positive_rays` |
| FR2 | drop the half-chord | C | same |
| FR3 | `_normalized` returns the input unchanged | C¹ | **only** `test_gaussian_fixed_ray_diagnostic_experiment.py` (frozen-bundle replay) |
| FR4 | spatial map transposed | C | `test_trajectory_diagnostic_reconstructs_the_frozen_same_path_endpoint` (+1) |
| FR5 | Perron projector `outer(r,r)/⟨r,r⟩` → `outer(r,r)` | C¹ | **only** the frozen-bundle replay |
| FR6 | `(I−P)d` → `P d` | C | `test_retained_beta_is_signed_comparison_typed_finite_difference` |
| FR7 | `/ log_block_scale` → `×` | C | same |
| FR8 | `coefficient_conditioning` max/min → min/max | C¹ | **only** the frozen-bundle replay |
| FR9 | `basin_exits` `OR` → `AND` | **S** | — |
| FR10 | drop `/‖direction‖²` in the construction residual | C | `test_scalarized_ray_construction_residual_detects_matrix_mutation_without_selecting_m` (+1) |

¹ Caught only by a byte-level regression replay of a frozen artifact, not by any semantic assertion. See F-8/F-9.

### `geometry/discrete_holonomy.py` — 6/6 (100 %)
| # | Mutation | Result | Which test |
|---|---|---|---|
| H1 | path composition order flipped (homo vs anti-homo) | C | `test_link_inversion_and_open_path_transport_match_literal_order` (+4) |
| H2 | discriminant `t²−4d` → `t²+4d` | C | `test_flat_cycle_has_literal_identity_holonomy_and_conjugacy_invariants` |
| H3 | curvature `H−I` → `H+I` | C | `test_nonflat_declared_plaquette_has_literal_holonomy_and_curvature` |
| H4 | `invert_link` returns the link uninverted | C | `test_link_inversion_and_open_path_transport_match_literal_order` |
| H5 | reversed adjacency keeps the forward label | C | `test_spanning_tree_criterion_pins_flat_tree_flat_cycle_and_nonflat_cycle` |
| H6b | 2-cell boundary orientation reversed | C | `test_nonflat_declared_plaquette_has_literal_holonomy_and_curvature` |

This is the strongest module in wave 2. Notably it *does* pin the composition-order convention that wave 1's finding **G8** flagged as ambiguous in the manuscript (`H_I^x` asserted a "representation" with no homomorphism convention). The code has a convention and the tests enforce it.

### `finite/information_history.py` — 5/10 (50 %)
| # | Mutation | Result | Which test |
|---|---|---|---|
| IH1 | KL argument order flipped in `log_ratio` | C | `test_information_point_matches_independent_score_fisher_and_vfe_oracles` |
| IH2 | VFE gradient drops the probability weighting | C | same |
| IH3 | natural gradient sign flipped | C | `test_rank_deficient_fisher_uses_moore_penrose_quotient_without_hidden_inverse` (+1) |
| IH4 | natural gradient uses `F` instead of `F⁺` | C | same (+2) |
| IH5 | `range_residual` measures the in-range part | C | same (+1) |
| IH6 | rank counts `|λ| > t` (negatives as positive) | **S** | — |
| IH7 | drop the symmetrization `½(M+Mᵀ)` | **S** | — |
| IH8 | positive-spectrum condition number inverted | **S** | — |
| IH9 | `used_pseudoinverse = nullity > 0` → `>= 0` (always True) | **S** | — |
| IH10 | rank threshold inflated by 10⁶ | **S** | — |

Every mutation to the *gradient* is caught; every mutation to `_spectral_diagnostics` survives. Confirmed against `test_information_history_experiment.py` as well.

### `finite/agent_network.py` — 9/9 (100 %)
All caught: AN1 KL order flip, AN2 residual sign, AN3 `−log Z` sign, AN4 unnormalized posterior, AN5/AN6 Bernoulli bit conventions, AN7 conditional ratio inverted, AN8 `_outside_marginal` marginalizes the block axes, AN9 weight by conditional instead of joint mass. Principal catcher: `test_global_vfe_gap_and_fixed_outside_local_difference_match_literal_oracles`.

### `realizations/gaussian/confirmatory_analysis.py` — 5/15 (33 %) ← worst
| # | Mutation | Result | Which test |
|---|---|---|---|
| CF1 | sign-test direction `<` → `>` | C | `test_exact_sign_pvalue_is_conservative_at_ties` |
| CF2 | sign-test tail direction reversed | **S** | — |
| CF3 | Holm step-down `(m−i)·p` → Bonferroni `m·p` | **S** | — |
| CF4 | Holm rank index reversed `(m−i)` → `(i+1)` | C | `test_holm_adjusts_one_frozen_six_endpoint_family` |
| CF5 | binomial lower tail → upper tail | C | `test_exact_binomial_lower_tail_uses_composite_null_boundary` (+1) |
| CF6 | support `upper <= −0.02` → `>= −0.02` | C | `test_primary_analysis_uses_thirty_unique_c_jobs_and_one_six_test_holm_family` |
| CF7 | support `<= −0.02` → `< −0.02` (strict at the frozen boundary) | **S** | — |
| CF8 | bootstrap null recentering sign flipped | **S** | — |
| CF9 | two-sided factor 2 dropped from the p-value | **S** | — |
| CF10 | p-value `min(tails)` → `max(tails)` | **S** | — |
| CF11 | primary CI 95 % → 90 % (2.5/97.5 → 5/95) | **S** | — |
| CF12 | `interval_half_width` half factor dropped | **S** | — |
| CF13 | counterevidence `lower >= 0` → `<= 0` | C | `test_primary_analysis_uses_thirty_unique_c_jobs_and_one_six_test_holm_family` |
| CF14 | `distinct_rays` uses the upper instead of the lower endpoint | **S** | — |
| CF15 | bootstrap median: midpoint average → lower order statistic | **S** | — |

### `finite/categorical_dqm.py` — 5/5 (100 %)
DQ1 centered-difference `2h` dropped, DQ2 `expm1(½Δ)` half dropped, DQ3 linear-term half dropped, DQ4 probability weighting dropped, DQ5 step normalization dropped — all caught, principally by `test_two_sided_dqm_remainder_matches_pinned_ladders_and_decreases` and `test_centered_fine_log_probability_difference_matches_analytic_score`.

### `finite/counterexamples.py` — 5/5 (100 %)
CX1 KL order flip, CX2 absolute-continuity direction flip, CX3 second channel transposed, CX4 relabel by the inverse, CX5 zero-mass skip on the wrong side — all caught.

### `finite/theory_oracles.py` — 8/8 (100 %)
TO1 ELBO log-ratio inverted, TO2 KL order flipped, TO3 decomposition residual sign, TO4 Fisher defect sign, TO5 conditional covariance not centred, TO6 absolute-continuity direction, TO7 `_conditional_projection` integrates the retained axes, TO8 coarse Fisher drops the mass weighting — all caught. The exact-`Fraction` oracle lane is genuinely load-bearing. (Wave 1's **T-11** stands: it is implementation-independent but assumption-identical.)

---

## Surviving-mutation findings

Ordered by scientific severity. Each names the missing test.

### F-1 — CRITICAL — The primary statistical endpoint is essentially unprotected
`realizations/gaussian/confirmatory_analysis.py`, 10 survivors.

The primary endpoint's *entire inferential apparatus* can be replaced by a different one without a single red test:

- **CF11**: the 95 % bootstrap percentile interval can become a 90 % interval. The interval is the input to `support` (`primary_interval["upper"] <= -0.02`) and to `forced_inconclusive` (`interval_half_width > 0.02`).
- **CF12**: `interval_half_width` can drop its `/2`, doubling it, which flips `forced_inconclusive` for any run with half-width in (0.01, 0.02].
- **CF9 / CF10 / CF8**: the primary p-value can silently become one-sided, take the wrong tail, or be recentred on the wrong side of the null. All three change the reported p-value; none is checked.
- **CF15**: the bootstrap statistic can stop being the median for even sample sizes.
- **CF3**: **Holm becomes Bonferroni.** The six-endpoint family-wise correction loses its step-down structure and no test notices. Only the *rank index* is pinned (CF4 caught), not the step-down maximum.
- **CF2**: the exact sign test's tail direction can be reversed.
- **CF14**: `distinct_rays` — the counterevidence trigger — can read the upper instead of the lower confidence limit.

**Scientific claim now unprotected:** that the confirmatory analysis implements the *preregistered* inferential procedure — a 95 % percentile bootstrap on the median, a two-sided bootstrap p-value, and Holm's step-down correction over the six frozen secondary endpoints. Nothing tests that the published numbers are those statistics rather than nearby impostors. This compounds wave 1's **T-04** (the `-0.02` threshold was mathematically unreachable) and **N-02** (`premises_passed` is a literal): the gate was unreachable, the premises are literals, and now the estimator itself is unpinned.

**Tests that should exist:**
1. `test_primary_interval_is_a_95_percent_percentile_bootstrap_of_the_median` — feed a fixed vector and a fixed seed, assert `lower`/`upper` equal `np.percentile(..., [2.5, 97.5])` of an independently recomputed bootstrap distribution, and assert they are **not** equal to the 5/95 values.
2. `test_primary_pvalue_is_two_sided_and_uses_the_smaller_tail` — construct an asymmetric bootstrap distribution where `lower_count != upper_count`, and pin the value; assert it is exactly twice the one-sided value.
3. `test_holm_is_step_down_not_bonferroni` — a six-p-value family where Holm and Bonferroni differ (e.g. `p = (0.001, 0.02, 0.03, 0.04, 0.5, 0.9)`), asserting the Holm adjusted values and asserting `adjusted != 6*p` for at least one endpoint.
4. `test_interval_half_width_is_half_the_interval` — pin against a literal.
5. `test_bootstrap_statistic_is_the_median_for_even_sample_sizes`.
6. `test_distinct_rays_uses_the_lower_confidence_limit` — a case where lower ≤ 0.05 < upper.

### F-2 — HIGH — `finite_gauge.py`: every relabeling-direction claim is untestable because all fixture permutations are involutions
`geometry/finite_gauge.py`, 4 survivors (FG1–FG4). **Root cause identified and verified.**

`tests/test_finite_experiment.py::gauge_fixture` supplies four permutations. All four are self-inverse:

```
first_flip   old_to_new=(2, 3, 0, 1)  new_to_old=(2, 3, 0, 1)  involution=True  matrix_symmetric=True
target_swap  old_to_new=(1, 0)        new_to_old=(1, 0)        involution=True  matrix_symmetric=True
bit_flip     old_to_new=(1, 0)        new_to_old=(1, 0)        involution=True  matrix_symmetric=True
identity     old_to_new=(0, 1)        new_to_old=(0, 1)        involution=True  matrix_symmetric=True
```

Because `P = Pᵀ = P⁻¹` for every one of them, `Pᵀ C Q` ≡ `P C Q` (FG1), `m @ P` ≡ `P @ m` (FG3), and `ref @ P` ≡ `ref @ Pᵀ` (FG2, FG4). The transpose/direction mutations are **no-ops on the fixture** — not because the code is right, but because the test data cannot distinguish a permutation from its inverse.

**Scientific claim now unprotected:** that `apply_site_relabeling` implements a *coherent* relabeling — i.e. that the recognition law, the channel's source index, the channel's target index, and the axis references are all pulled back by the **same direction** of the same permutation. A wrong theory that pulls the law forward and the channel backward would produce identical (zero) invariance residuals on this fixture. This is the computational counterpart of wave 1's **G6**: `finite_gauge.py` is permutation relabeling — and now we know it is permutation relabeling whose direction is never tested.

**Test that should exist:** `test_site_relabeling_is_coherent_under_a_non_involutive_permutation` — rerun the existing assertions with `first_flip` replaced by the 4-cycle `(1, 2, 3, 0)` and `bit_flip` by a 3-cycle on a 3-element axis, pinning `result.recognition.masses`, `result.axis_references` and `channel_intertwining` to literals. A single non-involutive fixture kills all four mutants.

Secondary note: `test_...intertwines_projection` lines 99–101 assert `result.recognition.masses @ result.channel.matrix == (q.masses @ channel.matrix) @ target.matrix`, which is the *same expression* the module computes internally as `channel_left` vs `channel_right` and then asserts again at line 113 as `channel_intertwining < 1e-12`. The test re-derives the module's own internal comparison rather than an independent oracle.

### F-3 — HIGH — `_spectral_diagnostics` is entirely unchecked, including a rank threshold inflated by 10⁶
`finite/information_history.py`, 5 survivors (IH6–IH10).

`_spectral_diagnostics` produces `rank`, `nullity` and `positive_spectrum_condition_number`, and `nullity` decides `used_pseudoinverse`. All five mutations survive both the math lane and `test_information_history_experiment.py`:

- **IH10** multiplies the rank threshold by 10⁶ — the numerical rank decision boundary moves six orders of magnitude and nothing changes.
- **IH6** counts `|λ| > t`, so a **negative** eigenvalue is counted as part of the positive spectrum. Fisher information is PSD, so this should be detectable by a rank-deficient or indefinite fixture; there is none.
- **IH7** removes the symmetrization `½(M+Mᵀ)` before `eigvalsh`.
- **IH8** inverts the condition number (`λ_min/λ_max` instead of `λ_max/λ_min`) — the reported field is never asserted.
- **IH9** makes `used_pseudoinverse` **always `True`** (`nullity >= 0`). This is a new instance of wave 1's **N-02**/**N-07** vacuity pattern *introduced by mutation and not detected*: a load-bearing provenance boolean that no test can distinguish from a constant.

**Scientific claim now unprotected:** wave 1's finding **F6** — `prop:hist-semidefinite-gradient-obstruction` demands a justified quotient before any pseudoinverse, and `used_pseudoinverse`/`rank`/`nullity` are the fields that are supposed to *document* when the quotient was taken. Those fields are unverified, so the record of whether a pseudoinverse was legitimately used carries no information.

**Tests that should exist:**
1. `test_spectral_diagnostics_pins_rank_nullity_and_condition_number_on_a_known_spectrum` — build a matrix with eigenvalues `(4, 1, 0)` (and one with a small negative eigenvalue `-1e-9`), assert `rank == 2`, `nullity == 1`, `condition == 4.0`, and assert the negative eigenvalue is **not** counted.
2. `test_rank_threshold_is_rcond_times_scale` — two matrices straddling the threshold, asserting different ranks.
3. `test_used_pseudoinverse_is_false_for_a_full_rank_fisher` — the direct `premises_passed`-style guard: assert `False` somewhere.

### F-4 — MED-HIGH — Galerkin coarse-graining never accumulates parallel edges
`realizations/gaussian/interactions.py`, GI4.

`coarse_edges[key] = coarse_edges.get(key, 0) + weight` can become `= weight` — the last fine edge mapping to a coarse pair overwrites all the others. The module's own consistency check (`np.allclose(restricted, coarse.precision)`, which raises `GaussianNumericalError`) would fire if any test partition produced two distinct fine edges collapsing onto the same coarse pair. None does.

**Scientific claim now unprotected:** that coarse-graining *sums* the couplings across a cluster boundary — the defining step of a block-spin/Galerkin restriction. Every other Galerkin mutation is caught (GI1, GI2, GI3, GI7 by 14–15 tests each), so the module is otherwise well tested; this is a fixture gap, not a coverage gap.

**Test that should exist:** `test_galerkin_sums_parallel_edges_across_a_cluster_boundary` — a partition with ≥2 fine edges between the same pair of clusters, asserting the coarse edge block equals the sum.

### F-5 — MED — The spectral conditioning band boundary is never tested at equality
`conditioning.py`, C2.

`abs(rcond − threshold) <= boundary_tolerance` → `<` survives. The existing test is named `test_threshold_band_is_inconclusive_and_tolerances_are_reachable` and it does catch C4 (dropping the relative term), so the band's *width* is tested — but never a point at exactly the band edge, which is where `inconclusive` and `fail`/`pass` meet.

**Scientific claim now unprotected:** that a matrix landing exactly on the declared tolerance boundary is classified `inconclusive` rather than `pass`/`fail`. For a project whose epistemic discipline rests on a three-valued decision, the boundary between "inconclusive" and a verdict is the interesting case.

**Test that should exist:** `test_exact_band_edge_is_inconclusive_not_a_verdict` — construct a matrix whose `rcond` is exactly `threshold + boundary_tolerance` (constructible in float64 from a diagonal matrix), assert `decision == "inconclusive"`.

### F-6 — MED — `quotient_sup_norm` is indistinguishable from the plain sup-norm on its only fixture
`finite/interactions.py`, I5.

`0.5·max(ω) − 0.5·min(ω)` → `max|ω|` survives. Verified numerically: the fixture `0.3·x₁x₂x₃ + 0.4·x₁x₂x₄` on spins ±1 gives

```
omitted max = 0.7   min = -0.7
quotient (max-min)/2 = 0.7     sup|.| = 0.7     EQUAL = True
```

The fixture is exactly symmetric about zero, so the quotient seminorm coincides with the sup-norm. `test_pairwise_retention_reports_three_distinct_residual_norms` asserts `quotient_sup_norm == approx(0.7)` — a value both implementations produce.

**Scientific claim now unprotected:** that `quotient_sup_norm` is a norm on the quotient by constants (invariant under `ω ↦ ω + c`), which is the whole reason it is reported separately from `theorem_coordinate_g_norm` and `weighted_l2_diagnostic`. Wave 1 caught a quotient sup-norm mutation in a core module; this specific equivalence class is unprotected here.

**Test that should exist:** `test_quotient_sup_norm_is_invariant_under_adding_a_constant` — use an asymmetric omitted component (e.g. `0.3·x₁x₂x₃ + 0.5`), assert `quotient_sup_norm` is unchanged when a constant is added and that it differs from `max|ω|`.

### F-7 — MED — `FinitePermutation.matrix` can be transposed with no effect
`finite/permutations.py`, P2.

The dataclass's `matrix` property materializes the permutation matrix. Transposing it survives all 476 math-lane tests. Its **only** consumer in `src` is `geometry/finite_gauge.py` (verified by grep: all other `.matrix` hits belong to `MarkovKernel` or `ScaleMorphism`), and F-2 explains why `finite_gauge`'s fixture cannot detect it. `permutations.py` has **100 % line coverage** and a 5/6 mutation score — the single uncovered claim is the one property with no independent test.

**Test that should exist:** `test_matrix_property_matches_the_old_to_new_convention` — for the 3-cycle already used elsewhere in that file, assert `p.matrix` equals a literal matrix and that `p.matrix != p.matrix.T`, plus the round trip `FinitePermutation.from_matrix(p.matrix).old_to_new == p.old_to_new`.

### F-8 — MED — The Perron projection in the fixed-ray flagship is a no-op on the frozen system
`realizations/gaussian/fixed_ray.py`, FR5 (demoted to CAUGHT only by a frozen-artifact replay).

`projection = outer(r,r)/⟨r,r⟩` → `outer(r,r)` survives the whole math lane. The reason is structural and verified:

```
scheme adjacent_pairs        row sums [1 1 1 1 1 1]   col sums [1 1 1 1 1 1]      <- doubly stochastic
differences row-sums: [-1.1e-16, 6.7e-16, 0.0, 4.4e-16, 4.4e-16]                  <- d ⟂ Perron ray, exactly
||(I-P)d|| == ||(I-6P)d||  ->  True
```

`adjacent_pairs` is **doubly stochastic**, so every finite difference `d = (A−I)c` satisfies `1ᵀd = 0`, i.e. `d` already lies in the orthogonal complement of the Perron ray. The projector therefore removes nothing, and *any* scalar multiple of it gives the same answer. The unit test `test_retained_beta_is_signed_comparison_typed_finite_difference` uses only `adjacent_pairs`, and its pinned expectation `[1.5, 0.9, 0.3, −0.3, −0.9, −1.5]/log 2` sums to zero — consistent with a projection that does nothing.

The other frozen scheme, `balanced_alternating`, has column sums `[1, 1, 1.1, 1, 1, 0.9]` and **does** expose the mutation (`FR5-detectable=True`).

**Scientific claim now unprotected by any semantic test:** that `retained_beta_residual_vectors` is the component of the flow *transverse to the Perron ray* — the quantity the whole "retained β" diagnostic exists to measure. On the preregistered system it is numerically indistinguishable from the raw finite difference. This sharpens wave 1's **N-10** ("convergence to the Perron ray is textbook Perron–Frobenius, independent of the VFE, gauge or RG theory"): not only is the dynamics trivial, the diagnostic that is supposed to extract non-trivial structure from it is inert on that dynamics.

**Test that should exist:** `test_retained_beta_projection_removes_the_perron_component` — run the same assertions on `scheme="balanced_alternating"`, and add a direct unit test feeding a difference with a non-zero Perron component, asserting `(I−P)d ≠ d`.

### F-9 — MED — Three fixed-ray diagnostics are protected only by a byte-level artifact replay
`realizations/gaussian/fixed_ray.py`, FR3, FR5, FR8.

These three survive every semantic test in the math lane and are caught **only** by `test_gaussian_fixed_ray_diagnostic_experiment.py`, which replays a frozen diagnostic bundle (`test_call_observer_records_all_80_validated_production_invocations`, `test_trajectory_diagnostic_reconstructs_the_frozen_same_path_endpoint`, …). That is real protection, but it is regression protection, not specification protection: it says "the numbers changed", never "the numbers are wrong", and it is exactly the lane that **fails at baseline on this host** (25 failures, `C:\anaconda\python.exe`). On any machine that is not the author's, FR3 and FR8 are undetectable.

FR3 is the starkest: `_normalized` returning its input unchanged destroys the *projective* character of `projective_ray_angle` — the angle stops being scale-invariant:

```
angle(v, r) correct = 0.4539612515723805
angle(v, r) FR3     = 3.141592653589793
angle(2v, r): correct = 0.4539612515723805 (invariant)   FR3 = 3.141592653589793
```

**Scientific claim now unprotected:** that the primary endpoint is an angle between **rays** (scale-invariant), not between vectors. `test_projective_ray_angle_is_stable_for_nearly_parallel_positive_rays` catches FR1 and FR2 but passes already-normalized inputs, so `_normalized` is the identity inside it.

**Test that should exist:** `test_projective_ray_angle_is_scale_invariant` — assert `projective_ray_angle(v, r) == projective_ray_angle(c·v, c'·r)` for `c, c' ∈ {0.1, 1, 10}` on an unnormalized `v`.

### F-10 — LOW-MED — `basin_exits` OR → AND is undetected
`realizations/gaussian/fixed_ray.py`, FR9. `(c < lower) | (c > upper)` → `&`, which is **identically False** (a coordinate cannot be both below the lower and above the upper bound). Every trajectory reports "no basin exit". Survives the math lane, lane A and `test_figures.py`.

The existing test is named `test_finite_trajectory_records_all_preregistered_diagnostics_without_basin_exit` — it only ever exercises the negative case, and the mutated code also returns the negative case. `basin_exit_events`/`basin_exit_rate` feed `support` (`basin_rate <= 0.05`) and `counterevidence` (`basin_rate > 0.20`) in `confirmatory_analysis`.

**Test that should exist:** `test_basin_exit_fires_on_both_bounds_separately` — one trajectory driven below `basin_lower` and one above `basin_upper`, asserting `basin_exits` is `True` in each case.

### F-11 — LOW — `attention_gauge._softmax` max-shift removal is undetected
`geometry/attention_gauge.py`, G1. Mathematically a no-op (softmax is shift-invariant); it matters only for overflow with large logits. Wave 1 caught the equivalent mutation in a core module, so a stability test exists there but not here. Reported for completeness, and because `CAT6` — the same mutation in `finite/categorical.py` — **was** caught, showing the pattern is testable and simply absent in this module.

**Test that should exist:** `test_softmax_does_not_overflow_on_large_logits` — logits of order `1e3`, assert finite output summing to 1.

---

## Assertions that cannot fail

Wave 1 found `defect_is_psd`, the cocycle composition residual, and `premises_passed`. Extending that hunt to the wave-2 modules:

### V-1 — `positive_definite` is derived from a hardcoded literal
`src/multiagent_elbo/finite/counterexample_experiment.py:562,581`

```python
minimum_diagonal = Fraction(1, 10**100)
...
"positive_definite": minimum_diagonal > 0,
```

`minimum_diagonal` is a **constant**, independent of every input. So `positive_definite` is `Fraction(1, 10**100) > 0` — always `True`. Yet `tests/test_counterexample_experiment.py:318` asserts

```python
assert near_singular["positive_definite"] is True
```

as though it were a check on the constructed matrix. It is a check that `1/10¹⁰⁰ > 0`. Verified:

```
minimum_diagonal = 1 / 10^100
positive_definite = minimum_diagonal > 0 = True  <- constant, independent of all inputs
```

The *scientifically meaningful* neighbouring assertion — `"rejected": assessment.decision == "fail"` on the same object — **is** load-bearing (C1/C3/C5 all break it). The vacuous one sits next to a good one, which is how it survived review.

**Fix:** either delete the assertion, or make `minimum_diagonal` a parameter and add a negative control with a non-positive diagonal that asserts `positive_definite is False`.

### V-2 — `inside_declared_domain` and `assumptions_satisfied` are boolean literals (a new instance of wave 1's N-02)
`src/multiagent_elbo/finite/counterexample_experiment.py:180,181,207,208,231,232,255,256`

These two fields of `CandidateRecord` are never computed anywhere in `src` — they are passed as literals at all four call sites:

```
180:  inside=False,   181:  assumptions=False,
207:  inside=False,   208:  assumptions=False,
231:  inside=True,    232:  assumptions=True,
255:  inside=True,    256:  assumptions=True,
```

and `tests/test_counterexample_experiment.py:243-244` asserts

```python
assert record["inside_declared_domain"] is True
assert record["assumptions_satisfied"] is True
```

which re-reads the literal written at line 231. `grep -rn "inside_declared_domain=False\|assumptions_satisfied=False" tests/` returns **0**. The assertion cannot fail unless someone edits the literal; it carries no information about whether the witness is actually inside the declared domain. This is structurally identical to wave 1's **N-02** (`premises_passed=True` as a literal), now found in a second module.

Note the fields *are* consumed: `CandidateRecord.__post_init__` (`counterexamples.py:208`) enforces that an outside-domain candidate must use `classification == "assumption_boundary"`. So the type discipline is real; only the *values* are unearned.

**Fix:** derive `inside`/`assumptions` from the witness (they are decidable — the domain conditions are explicit rational predicates), or rename them to `declared_inside_domain` to make clear they are author assertions, not computed checks, and record them as such in the manifest.

### V-3 — `direct_equals_staged` tests associativity, which survives an order reversal
`src/multiagent_elbo/finite/counterexample_experiment.py:421-422,499`

```python
composed_direct = compose_channels(compose_channels(a, b), c)
composed_staged = compose_channels(a, compose_channels(b, c))
...
"direct_equals_staged": composed_direct == composed_staged,
```

asserted at `test_counterexample_experiment.py:303` as `is True`. This is associativity, which holds for **any** associative composition rule — including a wholesale order reversal (`compose(A,B) := B·A` gives `(A∘B)∘C = C·B·A = A∘(B∘C)`). It therefore provides no evidence for the *orientation* claim in the name of the surrounding test. Strictly it is not vacuous (my CX3, transposing the second channel, does break associativity and was caught), so I record it as **weak rather than cannot-fail**. This is the same observation wave 1 made about `eq:rg-kernel-semigroup` in **RG-1**: "the one proved semigroup is congruence associativity — true for every S".

The orientation claim *is* separately protected by `test_composition_orientation_and_deep_composition_are_exact`, which caught CX3. The fix is only to stop presenting the associativity boolean as if it were the orientation check.

### Assertions checked and found genuinely load-bearing
To report the negative result as well: I grepped all `assert` lines in `tests/` for tolerances wider than `1e-3` (`abs=`, `rtol=`, `atol=`, `rel=` at `1e-0/1/2` or `0.x`) and found **zero** — the tolerance discipline wave 1 praised holds across the wave-2 test modules too. The `assert ... is True` census returned 20 hits; of those, `manifest["complete"] is True` (7 occurrences) is computed from a real completion state, and `stress[...]["coherent"]`, `fails_full_reconstruction` (`pairwise.residual > 0`) and `rejected` are all computed from data. Only V-1 and V-2 are constants.

---

## Claim coverage, not line coverage

For each experiment module in `src`, the theoretical claim it exists to provide evidence for, and whether a test would catch that claim being implemented wrongly. **Modules answering "no" are the important output.**

| Module | Claim it provides evidence for | Would a test catch a wrong implementation? |
|---|---|---|
| `finite/agent_network.py` | The collective VFE decomposes as posterior-KL + (−log Z); overlapping local objectives do not sum to the collective one (`thm:obs-collective-vfe`, `05b`) | **Yes** — 9/9. Exact-`Fraction` oracles pin every sign and weighting. |
| `finite/theory_oracles.py` | Independent exact re-derivation of the evidence/ELBO/KL identity and the Fisher channel defect (`05b`, `08`) | **Yes** — 8/8. But wave 1's **T-11** stands: assumption-identical, so it can indict an encoding, never the theory. |
| `finite/counterexamples.py` | Chapter 11's negative results: KL is not relabeling-invariant one-sidedly, composition orientation matters, retained space fails full reconstruction | **Yes** — 5/5 for the mathematics. **But** two of the published *record fields* are literals (V-2) and one is a constant (V-1). |
| `finite/categorical.py` | The categorical exponential family's score/Fisher identities (`hyp:exp-regular-minimal`, `07`) | **Yes** — 6/6. (Wave 1's **F7** — non-minimal sufficient statistics accepted — is a validation gap, not a mutation gap.) |
| `finite/categorical_dqm.py` | Differentiability in quadratic mean for the finite family (`05d`) | **Yes** — 5/5. The pinned two-sided ladder is a genuinely strong test. |
| `finite/attention.py` | Row-softmax attention arises as a state-conditioned marked-event law and is stable under coarse-graining (`prop:obs-attention-elbo`, `05b:547`) | **Yes** — 7/7. |
| `geometry/attention_gauge.py` | Attention logits are gauge-invariant scalars under local frame changes (`05c`) | **Yes** for the covariance law — 5/6; G4/G5 (the covector and link congruences, the actual gauge content) are both caught. Only numerical stability (G1) is unprotected. |
| `geometry/discrete_holonomy.py` | Graph holonomy, conjugacy invariants, plaquette curvature; flat iff path-independent (`07b`, `09`, `11`) | **Yes** — 6/6, including the composition-order convention wave 1's **G8** flagged as undeclared in the manuscript. |
| `finite/interactions.py` | Hoeffding decomposition against a declared product reference; retained-order projection with three separately typed residuals (`07b`) | **Mostly** — 6/7. The *quotient* seminorm's defining property is untested (F-6). |
| `realizations/gaussian/interactions.py` | Galerkin block aggregation and Schur-complement marginalization commute with the coarse operator (`06`, `07b`) | **Mostly** — 6/7. The Schur sign, the `Σ` vs `Σ⁻¹` substitution and the index partition are all caught. Edge accumulation is not (F-4). |
| `conditioning.py` | A three-valued (pass/fail/inconclusive) spectral SPD policy with a declared tolerance band | **Mostly** — 4/5. Direction and magnitude are pinned; the band edge itself is not (F-5). |
| `finite/permutations.py` | Canonical old-to-new convention with an explicit inverse; pullbacks of laws and channels | **Mostly** — 5/6, and 100 % line coverage. The `matrix` property is the one unprotected claim (F-7). |
| `realizations/gaussian/fixed_ray.py` | `conj:grg-fixed-b-attraction` — scalarized coupling trajectories converge to a fixed projective ray, with retained-β transverse to it | **Partly — and not on the frozen system.** 9/10, but three catches come only from a frozen-artifact replay that fails at baseline off the author's machine (F-9), and the transverse projection is provably inert on the preregistered dynamics (F-8). |
| `finite/information_history.py` | `prop:hist-semidefinite-gradient-obstruction` — a pseudoinverse is legitimate only on the identifiable tangent quotient (`05d:560`) | **No, for the part that matters.** The gradient and the natural-gradient rule are well tested (5/5); the rank/nullity/`used_pseudoinverse` record that documents *whether the quotient was justified* is completely unprotected (5 survivors, F-3). This is precisely wave 1's **F6**. |
| `geometry/finite_gauge.py` | Componentwise finite Borel relabeling leaves evidence, KL, VFE and conditional KL invariant and intertwines the retained projection | **No.** 2/6. The invariance residuals are checked, but every fixture permutation is an involution, so no test can tell a relabeling from its inverse (F-2). The gauge *direction* is untested. |
| `realizations/gaussian/confirmatory_analysis.py` | That the preregistered confirmatory inference (95 % percentile bootstrap, two-sided p-value, Holm over six frozen endpoints) was executed as frozen | **No.** 5/15. The estimator, its confidence level, its p-value construction and its multiplicity correction can all be replaced without a red test (F-1). |

### Line coverage alongside

```
$ python3 -m coverage run --branch --source=src/multiagent_elbo -m pytest <math lane>
476 passed in 53.91s
```

| Module | Line+branch cover | Mutation score | Gap |
|---|---|---|---|
| `finite/permutations.py` | **100 %** | 83 % | 17 |
| `finite/interactions.py` | 95 % | 86 % | 9 |
| `finite/attention.py` | 93 % | 100 % | — |
| `finite/categorical.py` | 93 % | 100 % | — |
| `geometry/attention_gauge.py` | 93 % | 83 % | 10 |
| `geometry/finite_gauge.py` | **90 %** | **33 %** | **57** |
| `finite/counterexamples.py` | 89 % | 100 % | — |
| `finite/categorical_dqm.py` | 87 % | 100 % | — |
| `conditioning.py` | 86 % | 80 % | 6 |
| `realizations/gaussian/interactions.py` | 86 % | 86 % | 0 |
| `finite/information_history.py` | **85 %** | **50 %** | **35** |
| `finite/theory_oracles.py` | 84 % | 100 % | — |
| `geometry/discrete_holonomy.py` | 84 % | 100 % | — |
| `finite/agent_network.py` | 82 % | 100 % | — |
| `realizations/gaussian/fixed_ray.py` | 80 % | 90 % | — |
| `realizations/gaussian/confirmatory_analysis.py` | **80 %** | **33 %** | **47** |
| **TOTAL** | **86 %** | **78.8 %** | |

The three modules with the largest gaps are the three that answer "no" in the claim-coverage table. Line coverage ranks `permutations.py` (100 %) above `agent_network.py` (82 %); mutation testing ranks them the other way round, and the mutation ranking is the correct one — `agent_network.py` pins every sign in the VFE decomposition against exact rational oracles, while `permutations.py` executes a property that nothing asserts.

**The one-sentence version:** line coverage in this repository measures how much of the code the tests *run*; it is uniformly high and uninformative. Mutation score measures how much of the code the tests *constrain*, and it collapses in exactly the two places where the project's scientific conclusions are produced — the gauge-relabeling module and the confirmatory statistics.

---

## Priority of fixes

1. **F-1** — pin the confirmatory estimator (6 tests). This is the module that publishes the project's headline decision, and it is at 33 %.
2. **F-2** — one non-involutive permutation in `gauge_fixture` kills four mutants at once. Cheapest high-value fix in this report.
3. **F-3** — pin `_spectral_diagnostics` on a known spectrum (3 tests); closes wave 1's **F6** on the code side.
4. **F-8/F-9** — add `balanced_alternating` to the retained-β test and a scale-invariance test for `projective_ray_angle`; both are two-line additions to existing tests.
5. **V-1/V-2** — delete or derive the three constant/literal booleans; they are wave 1's **N-02** pattern reappearing.
6. **F-4, F-5, F-6, F-7, F-10, F-11** — one fixture or one test each.

Items 2, 4 and 6 are together well under a day and would take the overall mutation score from 78.8 % to roughly 92 %.

---

## Verification that the user's repository is unmodified

All work was done on the copy at `/tmp/mae`. Every mutation was applied with a binary backup and reverted immediately; `find . -name '*.py.bak' | wc -l` was asserted to be `0` after every batch, and the final tree comparison is byte-identical:

```
$ diff -rq /tmp/mae/src <original>/src        # (excluding __pycache__)
(no output — identical)

$ cd <original> && git diff --stat HEAD -- src tests
(empty — source and tests untouched)

$ git status --porcelain
 M run_attention_lab.py
 M run_categorical_dqm_lab.py
?? docs/audits/2026-08-11-ultradeep-expert-audit.md
?? docs/audits/ultradeep-2026-08-11/
?? docs/reviews/
?? uv.lock
```

The working tree is clean apart from today's audit documents, as expected. The two modified launchers are **not** mine: both are `render_figures: False → True` one-line changes, and both are byte-identical to my copy taken before any mutation ran (`cmp` reports IDENTICAL), so they predate this work.

**No GPU or CUDA job was run at any point.** `tests/test_cuda_backend.py` was excluded from every lane; its 36 baseline failures are reported above but were never used as an oracle.
