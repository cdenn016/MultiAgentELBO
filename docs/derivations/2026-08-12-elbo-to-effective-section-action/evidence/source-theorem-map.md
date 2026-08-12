<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-4648de08bcb0913989cc11fb30c2da525d83bd93ccfbee6148f85ffff82db69c","schema_version":"rigorous-theory-search/v1","target_digest":"4648de08bcb0913989cc11fb30c2da525d83bd93ccfbee6148f85ffff82db69c"} -->
# Current source map

The live exact-ELBO theory already contains the finite-lattice bridge:

- `Theory/07b_agent_network_rg.tex:16-66` defines the fixed joint, posterior,
  recognition law, coarse kernel, and exact KL chain rule.
- `Theory/07b_agent_network_rg.tex:78-123` pushes both the reference and
  evidence measures and defines the coarse Radon-Nikodym action.
- `Theory/07b_agent_network_rg.tex:1364-1392` gives the exact complete
  finite-network interaction action.
- `Theory/07b_agent_network_rg.tex:1468-1512` defines the retained projection,
  residual, and the condition under which a PIFB-like ansatz is exact.
- `Theory/05b_local_collective_elbo.tex:490-608` derives fixed-source
  attention from an explicit label variable.
- `Theory/02_geometry.tex:404-425` types finite agents as section-bearing
  objects, while `Theory/03_probability.tex:405-449` states why finite designs
  do not reconstruct a continuum section law.

The current configuration-ELBO manuscript records the complementary Gibbs
identity and its non-circularity restrictions at
`Research/manuscripts/magent_elbo_whitepaper/07_configuration_elbo.tex:105-128`
and `:201-235`. The current PIFB2 manuscript presents its action as an ansatz;
the current MAgent implementation realizes a finite effective backend with
live-peer consensus. Neither artifact supplies a microscopic derivation or a
mesh-to-continuum theorem.
