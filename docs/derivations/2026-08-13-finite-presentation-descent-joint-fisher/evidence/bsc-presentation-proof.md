<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-c68f474d3e7991fa78a557b86bd645dc1c01a4272b2a75d53a52e17ad29176b2","schema_version":"rigorous-theory-search/v1","target_digest":"c68f474d3e7991fa78a557b86bd645dc1c01a4272b2a75d53a52e17ad29176b2"} -->
# Binary environment dilation, null-node control, and quotient obstruction

## Construction

Let \(R=O=E=N=\{0,1\}\), let \(E_D=\{*\}\), and write

\[
B_t(x)=t^x(1-t)^{1-x},\qquad
\delta(a,b)=a+b-2ab.
\]

On the common parameter manifold \(\Theta=(0,1)^3\), with
\(\theta=(a,b,\eta)\), define three strictly positive normalized finite
presentations:

\[
P^D_\theta(r,*,o)=\frac12 B_{\delta(a,b)}(o\mathbin\oplus r),
\]

\[
P^{L0}_\theta(r,e,o)=\frac12 B_a(e\mathbin\oplus r)
B_b(o\mathbin\oplus e),
\]

and

\[
P^{L+}_\theta(r,e,n,o)=\frac12 B_a(e\mathbin\oplus r)
B_b(o\mathbin\oplus e)B_\eta(n).
\]

Summing over \(n\) contributes one. Summing over \(e\) gives the mismatch
probability

\[
a(1-b)+(1-a)b=\delta(a,b).
\]

Therefore

\[
P^D_{RO,\theta}=P^{L0}_{RO,\theta}=P^{L+}_{RO,\theta}
=\frac12 B_{\delta(a,b)}(o\mathbin\oplus r).
\tag{1}
\]

With the common retained conditioning algebra \(\sigma(O)\), the three
presentations are observationally equivalent for every \(\theta\).

## VFE chain rule and the null-node control

For an observed \(o\), a retained recognition law \(q_R\), and an auxiliary
recognition kernel \(k(e,n\mid r)\), factor the latent posterior as

\[
P^{L+}_\theta(r,e,n\mid o)
=P_\theta(r\mid o)P^{L+}_\theta(e,n\mid r,o).
\]

The finite relative-entropy chain rule gives

\[
\mathcal F_{L+}(q_Rk;o)
=\mathcal F_{\rm coll}(q_R;o)
+\sum_rq_R(r)D_{\rm KL}\!\left(
k(\cdot\mid r)\middle\|P^{L+}_\theta(E,N\mid r,o)
\right),
\tag{2}
\]

where

\[
\mathcal F_{\rm coll}(q_R;o)
=\sum_rq_R(r)\log\frac{q_R(r)}{P^D_\theta(r,o)}
=\log2+D_{\rm KL}\!\left(q_R\middle\|P_\theta(R\mid o)\right).
\]

Thus equality in (2) holds exactly when the auxiliary kernel is the
conditional posterior for every \(q_R\)-positive retained state, and

\[
\inf_k\mathcal F_{L+}(q_Rk;o)=\mathcal F_{\rm coll}(q_R;o).
\tag{3}
\]

The independent-null-node control makes non-descent of an arbitrary full VFE
explicit. Set

\[
k_\lambda(e,n\mid r)=P^{L+}_\theta(e\mid r,o)B_\lambda(n),
\qquad \lambda\ne\eta.
\]

Then

\[
\mathcal F_{L+}(q_Rk_\lambda;o)-\mathcal F_{\rm coll}(q_R;o)
=D_{\rm KL}(\operatorname{Ber}\lambda\|\operatorname{Ber}\eta)>0.
\tag{4}
\]

## Retained and full Fisher tensors

Let \(v=(1-2b,1-2a,0)^\mathsf T\). The retained mismatch
\(X=O\mathbin\oplus R\) is Bernoulli with parameter \(\delta\), so the common
retained Fisher tensor is

\[
I_{\rm ret}(\theta)=\frac{vv^\mathsf T}{\delta(1-\delta)}.
\tag{5}
\]

In the full latent presentation, the mismatch variables
\(U=E\mathbin\oplus R\), \(V=O\mathbin\oplus E\), and \(N\) are independent
Bernoulli variables with parameters \(a,b,\eta\). Hence

\[
I_D^{\rm full}=I_{\rm ret},\qquad
I_{L0}^{\rm full}=\operatorname{diag}\!\left(
\frac1{a(1-a)},\frac1{b(1-b)},0\right),
\]

\[
I_{L+}^{\rm full}=\operatorname{diag}\!\left(
\frac1{a(1-a)},\frac1{b(1-b)},\frac1{\eta(1-\eta)}\right).
\tag{6}
\]

The retained Fisher tensor therefore descends through observational
equivalence, while the full Fisher tensor does not. In particular, inserting
the independent null node adds a strictly positive Fisher direction that the
retained law cannot see.

## Quotient criterion and intervention obstruction

Let

\[
\pi(P)=\bigl(P_{RO},\overline{\sigma(O)}\bigr).
\]

A typed readout \(T\) descends to observational-equivalence classes if and
only if it is constant on every fiber of \(\pi\). Evidence, retained posterior
kernels up to null slices, collapsed-VFE landscapes and minima, retained
entropies and divergences, parameterwise retained score/Fisher tensors,
posterior-completed full VFE, and conditionally minimized full VFE all satisfy
this criterion. Arbitrary full-latent VFE, auxiliary posteriors, full-joint
Fisher tensors, node counts, factorizations, labels, and intervention
structures do not generally satisfy it.

For example, under the usual intervention that replaces the selected node
kernel while retaining downstream kernels,

\[
P^{L+}_\theta(O=o\mid\operatorname{do}(E=e))=B_b(o\mathbin\oplus e).
\tag{7}
\]

For \(b\ne1/2\), the two interventions on \(E\) induce distinct record laws,
whereas the direct presentation has only a singleton auxiliary intervention.
The presentations have the same \(\pi\)-image but nonisomorphic typed
intervention structures. Consequently no map defined only on the
observational quotient can recover every presentation's original auxiliary
intervention structure.

This is a quotient-level obstruction, not a proof that every possible
canonicalization is impossible. A conventional representative, an enriched
equivalence carrying intervention kernels, or an independent agency axiom may
still select more structure.

## Exact failure certificate

At

\[
(a,b,\eta,\lambda)=\left(\frac14,\frac13,\frac25,\frac12\right),
\qquad \delta=\frac5{12},
\]

the null-node defect is

\[
\frac12\log\frac{25}{24}>0,
\]

and

\[
I_{\rm ret}=
\begin{pmatrix}
16/35&24/35&0\\
24/35&36/35&0\\
0&0&0
\end{pmatrix},
\]

\[
I_{L0}^{\rm full}=\operatorname{diag}(16/3,9/2,0),\qquad
I_{L+}^{\rm full}=\operatorname{diag}(16/3,9/2,25/6).
\]

Also \(P(O=e\mid\operatorname{do}(E=e))=2/3\). Failure of normalization,
(1), any displayed exact value, or positivity of (4) falsifies the
construction.

## Scope

The construction proves finite observational descent and its sharp boundary.
It does not infer autonomous agency from node presence, preserve interventions
under observational equivalence, define a continuum section-space law, or
identify a descended information tensor with physical geometry.
