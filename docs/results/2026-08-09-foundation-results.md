# Gauge-VFE-RG foundation results — 2026-08-09

## Outcome

The first MultiAgentELBO foundation is operational at Git revision
`51480cf4e47ff891f77578ac04cc88fee2e45c7f` on branch
`codex/gauge-vfe-rg-foundation-20260808`. Both dictionary-driven launchers ran
from the requested Desktop repository with a clean tracked worktree. The finite
run published 12 passing metric records; the Gaussian run published 15 passing
metric records. Both immutable numerical bundles include core arrays and the
requested diagnostic arrays. Pure saved-artifact replay then published one
PDF/PNG figure pair for each run.

These results verify the current implementation against its declared finite
fixtures and negative controls. They are numerical/software evidence, not a
proof of the analytic theory or of RG universality.

## Revision and provenance

| Item | Recorded value |
|---|---|
| Git commit | `51480cf4e47ff891f77578ac04cc88fee2e45c7f` |
| Git dirty at both run starts | `false` |
| Clean Git status SHA-256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Clean dirty-tree content digest | `0ccbb82e4a9bef951ac23137dc1206d14b2d3457c9644a8c71e003648a0fc60f` |
| Runtime Theory digest | `a7fddfcb8c67dbec71c7a35d0e415313a38154719e05d6ccd73672a810939343` |
| Theory digest framing | `sorted-relative-posix-path-nul-raw-sha256-digest-v1` |
| Theory preservation check | 44 tracked files, 0 missing, 0 differing from the live Research paths used for the snapshot |
| Root seed | `20260808` |

The run manifests also record the resolved configuration hash, Python, NumPy,
SciPy, and platform versions; the four named RNG spawn keys; the exact Theory
input hash; and a content-binding digest of tracked and nonignored untracked
dirty bytes.

## Machine test evidence

The final JUnit file is `docs/verification/pytest-foundation.xml`.

| Tests | Passed | Failed | Errors | Skipped | Time |
|---:|---:|---:|---:|---:|---:|
| 198 | 197 | 0 | 0 | 1 | 12.221 s |

The one skip is the dynamic Windows symlink regression: the test account lacks
the privilege to create a symbolic link. Hard-link ownership tests executed,
and the reparse/junction rejection path was independently inspected and probed.
This skip is therefore an explicit remaining environment coverage limitation,
not evidence that the symlink branch executed.

## Finite exact laboratory

Run directory:

`artifacts/finite-exact/ad296bae54057c87330a964e99c1ce6657bcfc2f769fd3d7211c5d6a6380e4f9-20260808`

The finalized inventory is `config.json`, `manifest.json`, `metrics.json`,
`arrays.npz`, and `diagnostics.npz`.

| Metric | Value | Tolerance | Status | Interpretation |
|---|---:|---:|---|---|
| `FIN-01_evidence_residual` | `0` | `1.10e-9` | pass | Common-channel evidence preservation |
| `FIN-02_vfe_chain_residual` | `-9.71445e-17` | `1.10e-9` | pass | Fine/coarse/conditional-KL chain rule |
| `FIN-03_block_update_residual` | `0` | `1.10e-9` | pass | Fixed-outside local/collective difference |
| `INF-01_fisher_identity_residual` | `0` | `1.10e-9` | pass | Fisher loss equals conditional score covariance |
| `INF-01_fisher_defect_min_eigenvalue` | `0` | `1.35e-9` | pass | Singular-PSD defect is retained without jitter |
| `INF-01_stochastic_weighting_control` | `1.11022e-16` | `1.10e-9` | pass | Nonuniform stochastic weighting oracle |
| `INT-01_reconstruction_residual` | `0` | `1.10e-9` | pass | Full Hoeffding interaction reconstruction |
| `INT-01_theorem_coordinate_g_norm_control` | `0.7` | `1.10e-9` | pass | Pairwise-retained coordinate-G omission |
| `INT-01_quotient_sup_norm_control` | `0.7` | `1.10e-9` | pass | Quotient-sup omission, kept distinct from G norm |
| `INT-01_weighted_l2_diagnostic_control` | `0.5` | `1.10e-9` | pass | Weighted-L2 diagnostic, kept distinct from theorem norms |
| `GAUGE_finite_relabeling_residual` | `2.77556e-17` | `1.10e-9` | pass | Coherent finite relabeling metamorphic |
| `GAUGE_mismatch_kl_delta_control` | `-0.0405465108108164` | `1.10e-9` | pass | Deliberately incoherent relabeling control |

The exact zero and near-roundoff residuals support the implementation paths for
the stated finite fixtures. The nonzero controls are important: they show that
the test suite can distinguish theorem-coordinate G norm from weighted L2,
detect incomplete relabeling, and expose pairwise interaction nonclosure.

## Gaussian realization laboratory

Run directory:

`artifacts/gaussian-realization/30e8e0dd923c24a63d9ffc91e4b1d9740d15f576bb393f3106783fdd1b78085c-20260808`

The finalized inventory is `config.json`, `manifest.json`, `metrics.json`,
`arrays.npz`, and `diagnostics.npz`.

| Metric | Value | Tolerance | Status | Interpretation |
|---|---:|---:|---|---|
| `GAU-01_energy_residual` | `7.10543e-15` | `1.01e-10` | pass | Precision energy pinned to `149/5` in both frames |
| `GAU-01_laplacian_energy_residual` | `8.88178e-16` | `1.01e-10` | pass | Laplacian energy pinned to `34/5` in both frames |
| `GAU-01_generalized_spectrum_residual` | `3.33067e-16` | `1.01e-10` | pass | Matched pencil roots agree with the radical oracle |
| `GAU-01_eigenpair_residual` | `1.86170e-16` | `1.01e-10` | pass | Normalized generalized-eigenpair residual |
| `GAU-01_metric_orthogonality_residual` | `6.66134e-16` | `1.01e-10` | pass | Precision-metric eigenvector orthogonality |
| `GAU-01_logdet_difference_residual` | `-8.88178e-16` | `1.01e-10` | pass | Inverse-congruence log-determinant scaling |
| `GAU-01_determinant_oracle_residual` | `1.13687e-13` | `1.01e-10` | pass | Both literal precision determinants |
| `GAU-01_commuting_square_residual` | `5.55112e-17` | `1.01e-10` | pass | Literal `S'`, `T_c`, and both coarse operators |
| `GAU-01_ordinary_spectrum_oracle_residual` | `8.88178e-16` | `1.01e-10` | pass | Both frame-specific ordinary spectra |
| `GAU-01_ordinary_spectrum_change_control` | `1.8006815631` | `1.01e-10` | pass | Ordinary spectrum is not a nonorthogonal-frame invariant |
| `GAU-02_galerkin_residual` | `0` | `1.01e-10` | pass | Hard-identification/Galerkin operator restriction |
| `GAU-02_schur_distinction_control` | `4.4545454545` | `1.01e-10` | pass | Schur marginal differs from Galerkin restriction |
| `GAU-02_scalar_schur_oracle_residual` | `8.88178e-16` | `1.01e-10` | pass | Literal scalar Schur complement |
| `GAU-02_kron_schur_oracle_residual` | `4.44089e-16` | `1.01e-10` | pass | Literal matrix-valued Schur complement |
| `GAU-02_kron_nonclosure_control` | `0.05263157895` | `1.01e-10` | pass | Manufactured off-diagonal weight is asymmetric |

The run preserves the distinction between operator-level Galerkin restriction
and Gaussian marginalization. It also treats raw minimum eigenvalues and
condition numbers as chart-dependent diagnostics rather than gauge invariants.
No pseudoinverse, eigenvalue clamp, or jitter repair is used.

## Saved-artifact figures

The finite figure replay is in:

`artifacts/finite-exact/figures/ad296bae54057c87330a964e99c1ce6657bcfc2f769fd3d7211c5d6a6380e4f9-20260808`

The Gaussian figure replay is in:

`artifacts/gaussian-realization/figures/30e8e0dd923c24a63d9ffc91e4b1d9740d15f576bb393f3106783fdd1b78085c-20260808`

Both figure manifests are complete. Each output contains a vector PDF and a
300-DPI PNG generated only from finalized `metrics.json` and `arrays.npz`.
Visual inspection confirmed readable labels, visible finite residual tolerance
bands, and coincident exact/original/transformed generalized spectra. The PNG
width is exactly 1050 pixels at 300 DPI and the PDF MediaBox width is exactly
252 points, so both exports are 3.5 inches wide. Captions identify `n=1 exact
fixture`; no sampling uncertainty or significance marks are fabricated.

## Independent review and remediation

Fixed-commit adversarial review initially found two important figure defects
(partial PNG publication on a failed PDF replace, and the ability to target a
finalized run directory) plus a physical-width mismatch. Transactional rollback,
resolved containment checks, and exact-width exports were added. Re-review
found no Critical or Important issues.

Independent numerical review initially found three important Gaussian defects
(determinant/condition-boundary frame rejection, unbacked renderer statuses,
and a missing first-class commuting-square metric) plus a retain-all ordering
defect. The fixes use `slogdet`, tolerance-safe condition gates, verified
on-disk figure inventories with SHA-256 identities, pinned/persisted coarse
oracles, and requested-order Schur output. Re-review found no Critical,
Important, or Minor issues. The durable review record is
`docs/verification/independent-reviews.md`.

## What remains open

This release intentionally does not claim:

- DQM or Fisher geometry for arbitrary law families;
- application-level membership in the thin Gaussian interaction family;
- nontrivial connections, parallel transport, or holonomy;
- marked-event attention composition and its negative controls;
- continuum/projective limits, learned partition selection, or empirical
  recovery;
- attraction, universality, or a fixed ray for the full Gaussian cone.

The next implementation milestone should add the marked-event attention
composition experiment and a parametric categorical DQM family before any
multi-scale Gaussian attraction study. Any later RG study must preregister its
basin, comparison maps, blocking schemes, seeds, scale window, and failure
criteria; a single finite trajectory cannot close a universality claim.
