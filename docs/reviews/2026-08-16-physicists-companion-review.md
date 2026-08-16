# Physicist's Companion Review and Revision

Date: 2026-08-16

The review compared `physicists_companion.tex` with the governing chapter order in `Theory/main.tex`, the exact attention construction in `Theory/05b_local_collective_elbo.tex`, the static pointwise parent construction and status boundaries summarized in `Theory/appendix_claim_ledger.tex`, and the proposed extension in `Theory/grand_canonical_meta_agent_formation.tex`. The revision keeps the companion at a physicist's mathematical level while preserving the distinctions that are load bearing in the detailed manuscript.

The main correction concerns normalization. The standard attention contribution to the dimensionless VFE is `KL(beta_i || pi_i) + tau_i^{-1} sum_j beta_ij E[D_ij]`. The corresponding row free energy in mismatch-energy units is `F_i^row = sum_j beta_ij E[D_ij] + tau_i KL(beta_i || pi_i)`. Both expressions have the same softmax minimizer, but the latter is the transparent Helmholtz form. The revision also gives the total derivative when both the row probabilities and transported mismatches evolve, so row descent is not mistaken for descent of the coupled system.

The thermodynamic interpretation is now separated into three levels. The VFE has an exact Gibbs variational or Helmholtz structure in information units. A normalized attention row is a canonical ensemble over admitted sources. A grand-canonical network requires a separate occupation variable and a fluctuating edge or membership count; the product `beta_ij D_ij` alone does not supply a chemical potential or a particle number. The proposed Bernoulli edge ensemble is therefore labeled as an extension rather than folded into the established main theorem.

The meta-agent discussion is likewise split by type. Adaptive fine agents can reorganize their effective bonds without producing a parent. The established pointwise parent begins only when one normalized recognition-independent channel pushes the full generative, recognition, and posterior laws. Recursive networks of parents, fluctuating memberships, cross-scale feedback, sustained nonequilibrium, and Wheelerian participation remain proposed or open. A new TikZ hierarchy figure makes those stages visually distinct.

The closing status table and summary were corrected so that the finite static mathematical results are not called empirically inconclusive. What remains empirically inconclusive is the physical and cross-scale interpretation. Multivariate Gaussian models remain optional computational realizations rather than the definition of the theory.

The revised standalone document compiled successfully with pdfLaTeX after the reference and outline passes settled. The focused build produced 26 pages, no unresolved references or citations, no TeX errors, and no overfull or underfull boxes. Its temporary artifacts were removed, and the repository's pre-existing untracked PDF was not overwritten.
