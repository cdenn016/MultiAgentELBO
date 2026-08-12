<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-4648de08bcb0913989cc11fb30c2da525d83bd93ccfbee6148f85ffff82db69c","schema_version":"rigorous-theory-search/v1","target_digest":"4648de08bcb0913989cc11fb30c2da525d83bd93ccfbee6148f85ffff82db69c"} -->
# Counterexamples and removal obligations

Exact coarse-graining is not automatically local. If
\(Y\sim N(0,\tau^2)\) and \(X_a\mid Y\sim N(Y,\sigma^2)\), eliminating \(Y\)
generates an all-to-all term proportional to \((\sum_aX_a)^2\). Eliminating a
hidden Ising spin coupled to four retained spins generates a nonzero four-body
operator through \(-\log[2\cosh(\sum_iJ_ix_i)]\). A local pairwise PIFB2 basis
therefore needs an explicit projection and residual.

A fixed two-variable joint ELBO cannot generically yield the live-peer term
\(D_{\rm KL}(\operatorname{Ber}(p)\Vert\operatorname{Ber}(r))\). For every
fixed positive joint \(P(i,j)\), the product-recognition functional
\(D_{\rm KL}(q_iq_j\Vert P)\) has
\(\partial_p\partial_r^2=0\), whereas the live-peer KL has
\(\partial_p\partial_r^2=r^{-2}-(1-r)^{-2}\), nonzero away from
\(r=1/2\). The sender cannot be both a current variational marginal and a
fixed generative factor without an additional typed layer.

For \(K\ge2\), \(\|H-I\|_F^2\) is not invariant under
\(H\mapsto g^{-1}Hg\) in \(GL(K)\). Taking
\(H=I+\epsilon E_{12}\) and \(g=\operatorname{diag}(t,1)\) changes the
norm by \(t^{-2}\). Moreover noncompact Haar volume is infinite, so a
gauge-invariant Gibbs law needs a quotient/gauge slice, Jacobian, stabilizer
treatment, and a finite reference measure.

Finally, deterministic energy convergence does not imply process-law ELBO
convergence. For \(M=1/h\) product Bernoulli sites, the unscaled exact KL is
\(M d_{\rm KL}(q\Vert p)\), while the quadrature-scaled density action is
\(hM d_{\rm KL}(q\Vert p)\). The first diverges and the second stays finite.
