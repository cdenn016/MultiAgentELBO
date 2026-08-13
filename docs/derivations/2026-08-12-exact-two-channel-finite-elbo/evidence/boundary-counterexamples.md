# Boundary derivations and counterexamples

## Correlated private recognition

Let (K=M=\{0,1\}), let (q=s=(1/2,1/2)), and let (\zeta) put mass (1/2) on each diagonal point
((0,0),(1,1)). With (p=q,r=s), both marginal self KL terms vanish, while

\[
D_{\rm KL}(\zeta\Vert p\otimes r)
=I_\zeta(K;M)=\log2.
\]

Therefore any private decomposition containing only the two marginal self KL terms is not exact for
correlated state-model recognition. The mutual-information correction is necessary.

## Single-latent product of experts

For one shared latent with density

\[
P_\beta(k)=Z_\beta^{-1}p(k)\prod_j u_j(k)^{\beta_j},
\qquad \sum_j\beta_j=1,
\]

direct calculation gives

\[
\begin{aligned}
D_{\rm KL}(q\Vert p)+\sum_j\beta_jD_{\rm KL}(q\Vert u_j)
=D_{\rm KL}(q\Vert P_\beta)-H(q)-\log Z_\beta.
\end{aligned}
\]

The additive self-plus-peer expression therefore is not the ordinary ELBO KL of this single-latent
normalized product-of-experts model unless the entropy and partition corrections are retained. The
tied-replica construction avoids this hidden normalization by using distinct latent blocks.

## Nonunit attention temperature

The joint label-copy KL gives

\[
D_{\rm KL}(\beta\Vert\pi)+\sum_j\beta_jD_{\rm KL}(q\Vert u_j).
\]

Replacing its categorical coefficient by (\tau) produces
(\tau D_{\rm KL}(\beta\Vert\pi)) plus the same edge energies. The difference is
((\tau-1)D_{\rm KL}(\beta\Vert\pi)), nonzero whenever (\tau\ne1) and
(\beta\ne\pi). A nonunit-temperature theorem needs a separately normalized tempered model and
every source-dependent normalizer.

## Arbitrary model-self and state-self weights

A single private replica gives unit coefficients on (D_{\rm KL}(q\Vert p)) and
(D_{\rm KL}(s\Vert r)). If (s\ne r), replacing the model coefficient by
(\lambda_h\ne1) changes the scalar by
((\lambda_h-1)D_{\rm KL}(s\Vert r)). Positive integer coefficients can be represented by repeated
independent copies with tied recognition; arbitrary real coefficients require a powered or
generalized construction and its normalizers. The same applies to adaptive state precision.

## Base quadrature weights

The negative ELBO of the finite product law is a counting-measure sum. Multiplying a site term by a
cell volume (w_x) changes its probabilistic meaning unless the generative law is changed by
replication, tempering, or an explicitly normalized weighted model. Such weights are appropriate in
a deterministic action approximation, but do not remain an exact finite-law ELBO by notation alone.

## Same-time recognition sources

Replacing (q_b^n,s_b^n) in the generative kernel by the current optimization variables
(q_b^{n+1},s_b^{n+1}) makes the purported fixed joint depend on its recognition law. The one-step
ELBO proof then fails. A simultaneous theory needs a fixed configuration law, a genuine coupled
sample-level joint, or an empirical-measure large-deviation construction.

## Literal observation-display typing

The joint-typed scalar contains (-\mathbb E_{\zeta_i}\log p(o_i\mid k_i,m_i)). The current
literal PIFB2 display instead places a likelihood depending on (k_i,m_i) under an expectation over
(q_i) alone while leaving (m_i) unbound, or omits (m_i) in its pointwise version. Without a declared
model-variable convention there is no well-typed equality to prove. Under a predictive-marginal
reading, write (\zeta(dk,dm)=q(dk)t_k(dm)). The joint-minus-predictive negative-log-likelihood
difference is

\[
\mathbb E_q\!\left[D_{\rm KL}(t_k\Vert s^{(o,k)})-D_{\rm KL}(t_k\Vert s)\right],
\]

when the disintegration and absolute-continuity terms exist. It is sign-indefinite in general.
Only under (t_k=s), including (\zeta=q\otimes s), does it reduce to the nonnegative posterior-
KL gap (\mathbb E_qD_{\rm KL}(s\Vert s^{(o,k)})).

## Empty sources and hard support

For (N=1) with self-sources excluded, the peer channel is absent. An all-zero row is not a
categorical law. With hard supports, a peer KL may be (+\infty); masks are applied by restricting
the source set before the KL is formed, not by writing the undefined product (0\cdot\infty).
