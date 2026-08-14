<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-ebf8914b08524414858dcfd879ec3b08e5abd21bb0c9f8f36feb64d97f1cd7f2","schema_version":"rigorous-theory-search/v1","target_digest":"ebf8914b08524414858dcfd879ec3b08e5abd21bb0c9f8f36feb64d97f1cd7f2"} -->
# Weighted marginal Fisher gate

Let \(a_i=\theta_i(1-\theta_i)\) and consider a proposed weighted marginal
metric

\[
G_w=\operatorname{diag}\left(\frac{w_i}{a_i}\right).
\]

For any strictly positive joint family with the declared singleton marginals,
the exact comparison is

\[
\begin{aligned}
G_{\rm joint}-G_w
={}&\left[
\mathbb E[ss^{\mathsf T}]-G_{\rm prod}
+\mathbb E[sR^{\mathsf T}]
+\mathbb E[Rs^{\mathsf T}]
+\mathbb E[RR^{\mathsf T}]
\right]\\
&+\operatorname{diag}\left(\frac{1-w_i}{a_i}\right),\tag{1}
\end{aligned}
\]

where \(G_{\rm prod}=\operatorname{diag}(1/a_i)\). The bracket is the full
signed defect relative to the unit-weight product marginal metric. Neither it
nor the diagonal weight correction may be omitted.

On a tangent subspace \(V\), equality \(G_{\rm joint}|_V=G_w|_V\) holds if
and only if the bilinear defect in (1) vanishes on \(V\times V\). Equality of
traces, diagonals, or one selected tangent is insufficient.

For the six-bit parity family at the center,

\[
G_{\rm joint}=\frac4{1-c^2}I_6,\qquad
G_w=4\operatorname{diag}(w_i),\qquad c=\frac{\kappa}{64}.
\]

On the full six-dimensional tangent space these metrics agree if and only if

\[
w_i=\frac1{1-c^2}\qquad\text{for every }i.\tag{2}
\]

In particular, unit weights \(w_i=1\) agree with the joint Fisher metric if
and only if \(c=0\), equivalently \(\kappa=0\). Choosing the weights in (2)
matches this one center tensor by construction; it does not recover the full
joint law, select \(\kappa\), or establish equality away from the center.
