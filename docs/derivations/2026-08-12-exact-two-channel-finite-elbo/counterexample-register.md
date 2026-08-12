<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-ea859a3e62b93365692fe1b959217ec3c21100b535e3a6633999bc36a431af9f","schema_version":"rigorous-theory-search/v1","target_digest":"ea859a3e62b93365692fe1b959217ec3c21100b535e3a6633999bc36a431af9f"} -->
# Counterexample register

| ID | Overclaim defeated | Witness | Required correction |
|---|---|---|---|
| CE-1 | Marginal self KLs are exact for correlated private recognition | Perfectly correlated binary (K=M) gives (I_\zeta=\log2) while both marginal KLs vanish | Retain (I_\zeta(K;M)) or impose mean field |
| CE-2 | One normalized product-of-experts latent yields the additive self-plus-peer scalar | Direct density expansion leaves (-H(q)-\log Z_\beta) | Retain corrections or use distinct replicas |
| CE-3 | The elementary source-label KL produces arbitrary τ | Difference is ((\tau-1)D_{\rm KL}(\beta\Vert\pi)) | Use τ=1 or derive a tempered normalized model |
| CE-4 | One private replica produces arbitrary λ_h or α | Nonzero KL changes by the coefficient mismatch | Add replicas, powers, or a typed precision model |
| CE-5 | Cell-volume weights preserve exact finite-law ELBO semantics | Product-law KL adds site terms with unit counting weight | Change the microscopic law or classify as deterministic action scaling |
| CE-6 | Current live sources define a fixed joint | The generative denominator reads (Q^{n+1}) | Lag the source or construct a genuine configuration/sample law |

None of these witnesses refutes the scoped tied-replica theorem. They prevent extending its label
beyond its stated hypotheses.
