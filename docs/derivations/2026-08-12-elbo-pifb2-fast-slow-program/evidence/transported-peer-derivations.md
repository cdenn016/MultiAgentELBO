# Transported peer derivations

For a transport (Omega_{ij}) from (j)'s fiber to (i)'s fiber, the typed divergence is

[
D_{\rm KL}\!\left(q_i\middle\|(\Omega_{ij})_\#q_j\right).
]

It is a transported recognition-field interaction. Zero divergence is transported agreement, but
the interaction plus other terms need not produce global consensus.

Let \(\pi_i=(\pi_{ij})_j\) and \(\beta_i=(\beta_{ij})_j\) be strictly positive probability rows
satisfying \(\sum_j\pi_{ij}=\sum_j\beta_{ij}=1\). Assume that \(q_i^{n+1}\) and every
transported state law \((\Omega_{ij}^n)_\#q_j^n\) are normalized and satisfy the stated
common-domination convention. Define at update \(n+1\)

\[
P_i^n(j,dx)=\pi_{ij}(\Omega_{ij}^n)_\#q_j^n(dx),\qquad
Q_i^{n+1}(j,dx)=\beta_{ij}q_i^{n+1}(dx).
\]

Both are normalized laws. Direct expansion gives

[
\begin{aligned}
D_{\rm KL}(Q_i^{n+1}\Vert P_i^n)
&=\sum_j\int\beta_{ij}q_i^{n+1}(x)
 \log\frac{\beta_{ij}q_i^{n+1}(x)}
 {\pi_{ij}[(\Omega_{ij}^n)_\#q_j^n](x)}dx\\
&=D_{\rm KL}(\beta_i\Vert\pi_i)
 +\sum_j\beta_{ij}D_{\rm KL}
 \left(q_i^{n+1}\middle\|(\Omega_{ij}^n)_\#q_j^n\right).
\end{aligned}
]

This is exact because (q^n) belongs to the conditioned history, not the variational law being
optimized at (n+1). The simultaneous replacement (q_j^n\mapsto q_j^{n+1}) destroys that fixed-
conditional argument. Configuration-law promotion or an empirical-measure theorem is then needed.
