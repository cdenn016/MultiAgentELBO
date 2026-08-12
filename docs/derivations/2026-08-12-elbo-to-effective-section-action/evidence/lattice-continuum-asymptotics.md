<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-4648de08bcb0913989cc11fb30c2da525d83bd93ccfbee6148f85ffff82db69c","schema_version":"rigorous-theory-search/v1","target_digest":"4648de08bcb0913989cc11fb30c2da525d83bd93ccfbee6148f85ffff82db69c"} -->
# Lattice-to-continuum consistency calculations

For a regular statistical family \(q_\theta\), an edge
\(y=x+he_\mu\), and a link that approximates parallel transport,

\[
U_{xy}^h\!\cdot\theta(y)
=\theta(x)+hD_\mu^A\theta(x)+O(h^2).
\]

The score has zero expectation and the expected negative Hessian is the
Fisher tensor, so Taylor expansion gives

\[
D_{\rm KL}(q_{\theta(x)}\Vert U_{xy\#}^hq_{\theta(y)})
=\tfrac12 h^2 I_{\theta(x)}(D_\mu^A\theta,D_\mu^A\theta)+O(h^3).
\]

There are order \(h^{-d}\) edges. Hence an edge transmissibility of order
\(h^{d-2}\) yields a finite Fisher-covariant Dirichlet integral. Pointwise
self, peer, observation, and potential sectors instead use cell weights of
order \(h^d\), with cut-cell weights on local section supports.

For a compact gauge group in a unitary representation, a small plaquette has
\(H_p=I-h^2F_{\mu\nu}+O(h^3)\), and

\[
r-\operatorname{ReTr}H_p
=\tfrac12h^4\|F_{\mu\nu}\|_{\rm HS}^2+O(h^5).
\]

Therefore the Wilson sector must carry weight \(h^{d-4}\). These are
consistency expansions on smooth sequences, not Gamma-convergence proofs.
A deterministic limit additionally requires a common interpolation topology,
equicoercivity modulo gauge, liminf, recovery, boundary/topology control, and
uniformly vanishing truncation residual on bounded-energy sublevels.
