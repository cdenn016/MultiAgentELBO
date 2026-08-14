<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-c68f474d3e7991fa78a557b86bd645dc1c01a4272b2a75d53a52e17ad29176b2","schema_version":"rigorous-theory-search/v1","target_digest":"c68f474d3e7991fa78a557b86bd645dc1c01a4272b2a75d53a52e17ad29176b2"} -->
# Retained Fisher descent and explicit joint-lift noncanonicity

## Retained-law Fisher theorem

Let \(X=R\times O\) be finite and let
\(p_A,p_B:\Theta\to\Delta^\circ(X)\) be \(C^2\), strictly positive
retained-law families on the same parameter manifold. If

\[
p_A(\theta,x)=p_B(\theta,x)
\quad\text{for every }(\theta,x)\in\Theta\times X,
\tag{1}
\]

then their Fisher tensors agree:

\[
g^A_\theta(u,v)
=\sum_xp_A(\theta,x)
\bigl[u\log p_A(\theta,x)\bigr]
\bigl[v\log p_A(\theta,x)\bigr]
=g^B_\theta(u,v).
\tag{2}
\]

The conclusion remains true under a parameter-independent permutation of
\(X\), because the finite sum is merely reindexed. Therefore every common
\(C^1\) configuration map \(z:\mathcal S\to\Theta\) has the same retained-joint
pullback \(z^*g^A=z^*g^B\).

Equality at one parameter is insufficient. On a small interval around zero,

\[
p_A(1;\theta)=\tfrac12+\theta,
\qquad
p_B(1;\theta)=\tfrac12+2\theta
\]

agree at \(\theta=0\), but their Fisher values there are 4 and 16.
Parameterwise equality, including its derivative information, is load-bearing.

## Two smooth right-inverse lifts of the same paired marginals

Let \((a,b)\in(0,1)^2\), let \(0\le\kappa<1\), and define

\[
d_\kappa(a,b)=\kappa a(1-a)b(1-b).
\]

On the ordered binary pair \((00,01,10,11)\), set

\[
\iota_\kappa(a,b)=\left(
(1-a)(1-b)+d_\kappa,
(1-a)b-d_\kappa,
a(1-b)-d_\kappa,
ab+d_\kappa
\right).
\tag{3}
\]

Every component is strictly positive. For example,

\[
(1-a)b-d_\kappa=(1-a)b[1-\kappa a(1-b)]>0,
\]

and the other subtracted component is analogous. The components sum to one,
and marginalization gives

\[
\Pr_{\iota_\kappa}(K=1)=a,
\qquad
\Pr_{\iota_\kappa}(M=1)=b.
\]

Thus every \(\iota_\kappa\) is a smooth right inverse of paired
marginalization. The product lift is \(\iota_0\); \(\iota_{1/2}\) is a
distinct correlated lift. At \(a=b=1/2\),

\[
\iota_0=(8,8,8,8)/32,
\qquad
\iota_{1/2}=(9,7,7,9)/32.
\tag{4}
\]

No permutation maps the uniform law to the nonuniform law.

## VFE noncanonicity

Use a trivial observation and the uniform posterior
\(u=(1/4,1/4,1/4,1/4)\). At the same displayed marginal configuration,
the product lift has VFE zero, whereas

\[
\mathcal F(\iota_{1/2})
=D_{\rm KL}(\iota_{1/2}\|u)
=\frac9{16}\log\frac98+\frac7{16}\log\frac78>0.
\tag{5}
\]

Equivalently, choosing \(\iota_{1/2}\) as the posterior gives

\[
D_{\rm KL}(\iota_0\|\iota_{1/2})
=\frac12\log\frac{64}{63}>0,
\]

while the correlated lift has zero VFE. Paired marginals therefore do not
determine a full-joint VFE.

## Fisher noncanonicity

For a positive categorical family \(p(a,b)\), the pullback Fisher matrix is

\[
g_{uv}=\sum_x\frac{\partial_u p_x\,\partial_v p_x}{p_x}.
\]

At \(a=b=1/2\), direct differentiation of (3) gives

\[
\iota_0^*g^F=
\begin{pmatrix}4&0\\0&4\end{pmatrix},
\qquad
\iota_{1/2}^*g^F=
\frac1{63}\begin{pmatrix}256&-32\\-32&256\end{pmatrix}.
\tag{6}
\]

Their difference has eigenvalues \(-4/9\) and \(4/7\). It is nonzero and
indefinite, so neither equality nor a one-sided tensor order follows from the
marginals. Scalar mutual information is not a Fisher cross block; the latter
comes from derivatives of the selected joint family.

## Consequence and scope

The retained-joint Fisher tensor descends when the entire retained family
descends parameterwise. A full-joint recognition Fisher tensor requires a
selected joint lift, and paired belief/model sections do not select one. A
product lift is a valid smooth finite-interior choice but is a modeling
restriction, not a consequence of the marginals. These results close no
continuum section-space measure, physical metric, causal, temporal, or
dimensional-unit bridge.
