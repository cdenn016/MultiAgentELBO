<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-7d2c4a48da6b18e0d1dd177ba0e42e6ab6b625410e5cbefa9c9031dcfb9dd985","schema_version":"rigorous-theory-search/v1","target_digest":"7d2c4a48da6b18e0d1dd177ba0e42e6ab6b625410e5cbefa9c9031dcfb9dd985"} -->
# Construction and strongest theorem

Full development: `REPORT-part1-vfe-and-construction.md` through
`REPORT-part4-literature-experiment-verdict.md`. This file states the typed
construction and the strongest result the derivations support.

## The typed construction

Finite scale set $L=\{0,\dots,S\}$. All spaces nonempty standard Borel, all reference
measures $\sigma$-finite. All scale-0 agents at one context point $c_\*\in\mathcal C$;
the finite directed skeleton may contain cycles; no length, lattice, translation
symmetry, momentum space, or tree is assumed.

Per scale $s$ and node $i$: $\mathsf Y_{i,s}=\mathsf B_{i,s}\times\mathsf M_{i,s}\times\Xi_{i,s}$
with $\mathsf B_{i,s}\subseteq\mathcal P(\mathsf Z^b_{i,s})$ law-valued (standard Borel
because $\mathcal P$ of a Polish space is Polish) and $\mathsf M_{i,s}$ carrying an
evaluator $\mathrm{ev}$ into normalized generative kernels. Graph data
$G_s=(\alpha^{b,s},\alpha^{m,s},\beta^s,\gamma^s,a^s,\Omega^{b,s},\Omega^{m,s})$ with
non-flat transports. Memberships $R_s=(R^b_s,R^m_s)$ valued in fixed finite label pools
$\Lambda^b_{s+1},\Lambda^m_{s+1}$, with normalized incidence-supported endpoint kernels
$K^x_s(A,B\mid i,j)$. Holonomy marks $H_s$ recording component roots, based holonomy
representations $H^x_I:\pi_1(\Gamma_I,r_I)\to G$, and dressed boundary generators
$V^x_e=\tau^x_{I\leftarrow i}\Theta^x_e(\tau^x_{J\leftarrow j})^{-1}$, as one
simultaneous root-gauge orbit. Structural data $X$ and each $X_A=\chi_A(X)$ stay
outside every random channel.

The normalized generative joint is the ordered kernel composition

$$
\begin{aligned}
\mathbb P_\theta(do,dW\mid X)={}& L_\theta(do\mid Z_0,X)\,P_S(dZ_S,dG_S\mid X)\\
&\times\prod_{s=0}^{S-1}P^s_R(dR_s\mid Z_{s+1},G_{s+1},X)\\
&\times\prod_{s=0}^{S-1}P^s_G(dG_s\mid Z_{s+1},R_s,X)\,P^s_H(dH_s\mid Z_{s+1},R_s,G_s,X)\\
&\times\prod_{s=0}^{S-1}K^s_\downarrow(dZ_s\mid Z_{s+1},R_s,G_s,H_s,X),
\end{aligned}
$$

with the likelihood attached only at scale 0 and $K^s_\downarrow$ the only generative
locus of downward influence. Recognition is one correlated law
$\mathbb Q_\phi(dW\mid o,X)$ disintegrated along the same ordering.

Coarse-graining acts on measures, bottom-up, and is not a second generative arrow:
$\eta^{x,c}_{AB}=\sum_{i,j}\eta^x_{ij}K^x(A,B\mid i,j)$,
$\alpha^{x,c}_A=\sum_B\eta^{x,c}_{AB}$,
$\beta^c_{AB}=\eta^{x,c}_{AB}/\alpha^{x,c}_A$ on positive parent occupancy.

## Theorem A

Assume (i) the typing above with belief coordinates law-valued; (ii) the ordered
factorization with every factor a normalized measurable Markov kernel, likelihood at
scale 0 only, and $p_\theta(o\mid X)\in(0,\infty)$; (iii) recognition disintegrated
along the same ordering with $\mathbb Q_\phi\ll\boldsymbol\Pi_{\theta,o,X}$; (iv)
$\mathbb E_{\mathbb Q_\phi}(\log L_\theta(o\mid Z_0,X))^{+}<\infty$. Then:

1. $\mathbb P_\theta(\cdot\mid X)$ is a probability measure, and the tower carries no
   normalizer other than the evidence $p_\theta(o\mid X)$.
2. $\mathcal F^{\rm ext}_{\rm tower}=-\log p_\theta(o\mid X)+D_{\rm KL}(\mathbb Q_\phi\Vert\boldsymbol\Pi_{\theta,o,X})$
   holds in $\mathbb R\cup\{+\infty\}$ and equals the sum of the observation term, the
   top-prior divergence, and four groups of conditional divergences over the two
   channels' memberships, the graph data, the holonomy marks, and the parent-child
   kernels; the observation term is the only one that can be negative.
3. The $R_s$-coordinate minimizer is $Q^\star_R\propto P^s_R\,e^{-U_s}$ with $U_s$ the
   derived sum of graph, mark, and cross-scale conditional divergences. The
   $Z_{s+1}$-coordinate minimizer at frozen child kernel is
   $Q^\star_{s+1}\propto P_{s+1}\,e^{-\mathcal V_{s+1}}$ with
   $\mathcal V_{s+1}(z)=D_{\rm KL}(Q_s(\cdot\mid z)\Vert K^s_\downarrow(\cdot\mid z))$.
   The parent kernel is the child's prior; the child's conditional-KL profile is the
   parent's likelihood.
4. Pushing $\eta^b,\eta^m$ through normalized incidence-supported endpoint kernels and
   disintegrating gives normalized, gauge-invariant coarse occupancies and rows that
   compose exactly under nested normalized memberships, on positive parent occupancy.
5. The scale-to-scale VFE loss under one common recognition-independent channel is the
   nonnegative conditional-information defect $\Delta$, additive in $[0,+\infty]$, zero
   exactly when the discarded conditional recognition and posterior laws agree almost
   surely; ordinary subtraction requires finite fine KL.
6. Non-flat holonomy is retained exactly as the simultaneous root-framed orbit
   $(\bar z^x_I,H^x_I,\{V^x_e\})$ together with the conditional law $\mu^x_{IJ}$ of
   dressed transports $\Theta^{IJ,x}_{ij}=\Omega^x_{Ii}\Omega^x_{ij}\Omega^x_{jJ}$; no
   flatness is imposed and no barycenter is required to exist.

## Negative companion

**Proposition 5.** With an unrestricted parent space and downward-kernel family, take
$\mathsf Z_{1,I}=\mathsf Y_{0,I}$, $K^0_I=\delta$, $P_1=\mathbb P^{\rm flat,Z_0}$. Then
$\min_{\mathbb Q}\mathcal F^{(R)}_{\rm tower}=-\log p^{\rm flat}(o\mid X)$ for every
partition $R$, so the tower VFE ranks no partition and the posterior over partitions
equals the prior. Hierarchy selection is therefore carried entirely by declared
capacity restrictions on $(\mathsf Z_{s+1},K^s_\downarrow,P_{s+1})$ together with a
node-count cost; neither alone suffices.

## What Theorem A does not give

No partition selector; no block-persistence theorem; no rescaling/identification
kernel and hence no RG semigroup, beta function, blocking ratio, or
relevant/irrelevant classification; no cross-scale dynamical closure; no sustained
nonequilibrium (a single scalar with symmetric mobility converges by LaSalle, and
participatory feedback derivable from that scalar does not change this); no continuum
or thermodynamic limit; no physical time; no autonomous agency; no unique latent DAG,
unique hierarchy, or unique microscopic physics.
