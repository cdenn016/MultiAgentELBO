<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-a0d61fb082b9632a9aac685fced7bf4a82f1a9f115a72b9583a6ed96f636c952","schema_version":"rigorous-theory-search/v1","target_digest":"a0d61fb082b9632a9aac685fced7bf4a82f1a9f115a72b9583a6ed96f636c952"} -->
# Counterexample proofs

These eight witnesses refute shortcut claims that the pointwise theorem explicitly excludes. They do not refute the frozen affirmative conjunction.

## CE-1: KL thresholds are not transitive

Let (P=\operatorname{Bernoulli}(1/10)), (Q=\operatorname{Bernoulli}(1/2)), and (R=\operatorname{Bernoulli}(9/10)). Direct calculation gives

\[
\begin{aligned}
\operatorname{KL}(P\Vert Q)
&=\tfrac1{10}\log\tfrac15+\tfrac9{10}\log\tfrac95
\approx0.368064,\\
\operatorname{KL}(Q\Vert R)
&=\tfrac12\log\tfrac59+\tfrac12\log5
=\tfrac12\log\tfrac{25}{9}
\approx0.510826,\\
\operatorname{KL}(P\Vert R)
&=\tfrac1{10}\log\tfrac19+\tfrac9{10}\log9
=\tfrac45\log9
\approx1.757780.
\end{aligned}
\]

At threshold (0.6), (P) is close to (Q) and (Q) is close to (R), while (P) is not close to (R). Threshold adjacency therefore is not an equivalence relation and cannot define parents without an additional clustering rule.

## CE-2: zero marginal KL can hide an infinite full-joint VFE defect

On ({0,1}^2), let

\[
Q(0,0)=Q(1,1)=\tfrac12,
\qquad
P(0,1)=P(1,0)=\tfrac12,
\]

with all other atoms zero. Every singleton marginal of (P) and (Q) is fair, so all singleton-marginal KL divergences vanish. The joint supports are disjoint, hence

\[
\operatorname{KL}(Q\Vert P)=+\infty.
\]

For the common deterministic coarse channel (C(x,y)=x), (QC=PC=\operatorname{Bernoulli}(1/2)), while the conditionals (Q(dy\mid x)=\delta_x) and (P(dy\mid x)=\delta_{1-x}) are mutually singular. The exact conditional-KL defect is (+infty). Thus zero marginal KL neither supplies a joint recognition law nor controls full VFE.

## CE-3: trivial holonomy permits arbitrarily large disagreement

Take a two-vertex tree, identity transport, and positive-definite unit edge weight. The graph has trivial holonomy. For (a>0), put

\[
p_1=\mathcal N(-ae_1,I_K),
\qquad
p_2=\mathcal N(ae_1,I_K).
\]

The equal-covariance Gaussian formula gives

\[
\operatorname{KL}(p_1\Vert p_2)=2a^2,
\]

which is unbounded as (a\to\infty). Full-frame flatness is therefore not sufficient for belief agreement.

## CE-4: nontrivial holonomy can stabilize a law

Take a triangle in (K=3) with identity transports on two edges and closing holonomy

\[
H=\operatorname{diag}(1,-1,-1)\neq I.
\]

The represented fixed vector sector is only (operatorname{span}(e_1)), so the full fixed (K)-sector is absent. Nevertheless, for every (sigma>0),

\[
H_\#\mathcal N(0,\sigma^2I_3)=\mathcal N(0,\sigma^2I_3).
\]

Assigning this law at all vertices makes every transported marginal KL zero. Trivial holonomy is therefore not necessary for state-specific belief agreement.

## CE-5: a connection spectral gap is state blind and arbitrarily scalable

For two vertices with identity link and scalar edge weight (c>0),

\[
L_c=c
\begin{pmatrix}
1&-1\\
-1&1
\end{pmatrix}
\otimes I_K.
\]

Its positive spectral gap is (2c). The matrix contains no belief law. The same (L_c) can accompany identical laws or the arbitrarily separated Gaussians of CE-3. Rescaling the edge weight from (c) to (Mc) multiplies the gap by (M) without changing the laws. A raw gap is therefore a state-blind, scale-dependent diagnostic, not an intrinsic agreement threshold.

## CE-6: one-way KL can be finite while reverse KL is infinite

On ({0,1}), let (P=(1,0)) and (Q=(1/2,1/2)). Then

\[
\operatorname{KL}(P\Vert Q)=\log2<\infty,
\qquad
\operatorname{KL}(Q\Vert P)=+\infty.
\]

Any directed-threshold rule must declare its direction and support convention. A small or finite forward value gives no reverse-support guarantee.

## CE-7: a Gaussian barycenter leaves an exact nonlinear boundary-action residual

Let the two equally weighted child laws be

\[
P_- = \mathcal N(-a,1),
\qquad
P_+ = \mathcal N(a,1),
\qquad a\neq0.
\]

Their full-Gaussian forward-KL barycenter is the moment-matching Gaussian

\[
G=\mathcal N(0,1+a^2).
\]

For the quartic boundary functional (H(x)=\lambda x^4), with (\lambda\neq0), each child has fourth moment

\[
\mathbb E_{P_\pm}[X^4]=a^4+6a^2+3,
\]

whereas the Gaussian parent has

\[
\mathbb E_G[X^4]=3(1+a^2)^2.
\]

The parent-minus-child-average residual is therefore exactly

\[
\mathcal R_H
=\mathbb E_G[H]
-\tfrac12\left(\mathbb E_{P_-}[H]+\mathbb E_{P_+}[H]\right)
=2\lambda a^4\neq0.
\]

Thus Gaussian moment matching does not preserve this nonlinear boundary action. The unrestricted law barycenter (\tfrac12(P_-+P_+)) does preserve expectations by linearity; the residual is introduced by projecting that mixture back to the Gaussian family.

As an independent family-closure control, the bimeasurable bijection (h(x)=x^3) sends (X\sim\mathcal N(0,1)) to a non-Gaussian variable: (\mathbb E[X^6]=15) and (\mathbb E[X^{12}]=10395), whereas a centered Gaussian of variance (15) has fourth moment (675).

## CE-8: literal overlapping parents double-count a shared child

Give one child (i) unit mass and declare literal full incidence in two parents (A) and (B):

\[
R(A\mid i)=R(B\mid i)=1.
\]

Pushing the child mass by (R) gives total parent mass (2), not (1). A unary factor owned by (i) is likewise copied once into each parent and counted twice if the parent objectives are added. For a self-edge event, independent replication at both endpoints produces four parent-pair copies and total edge-event mass (4). This is a replicated cover with retained multiplicity, not a normalized soft membership. Normalizing to (C(A\mid i)=C(B\mid i)=1/2) defines a different stochastic construction and makes the two parent assignments dependent through the shared child.

## Exactness boundary

CE-2, CE-5, CE-6, and CE-8 are finite exact support or rational calculations. CE-3 and CE-4 use exact Gaussian formulas and integer matrices. CE-7 uses exact Gaussian moments. CE-1 uses exact logarithmic expressions evaluated numerically only for readability. The contained recomputation is corroboration; these displayed arguments are the mathematical evidence.
