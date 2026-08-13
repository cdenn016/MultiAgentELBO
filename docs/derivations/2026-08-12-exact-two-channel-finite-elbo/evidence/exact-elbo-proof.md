# Exact ELBO derivation

Fix the observations (o=(o_a)_{a\in A}) and the history (H_n). Define the negative ELBO by

\[
\mathcal F_h^{n+1}(Q;o,H_n)
=\int Q(dz)\log\frac{dQ}{dP_h^n(o,\cdot)}(z),
\]

where (P_h^n(o,dz)) is the chosen likelihood-density slice. All following identities hold with
finite terms under the contract assumptions and extend in the standard way when the KL chain rules
are well defined as extended-real identities.

Because both laws factor over (a) and over the three distinct latent blocks,

\[
\mathcal F_h^{n+1}=\sum_{a\in A}
\left(\mathcal F_a^{\rm priv}
+\mathcal F_a^q+\mathcal F_a^s\right).
\]

## Private state-model block

Direct Radon-Nikodym expansion gives

\[
\mathcal F_a^{\rm priv}
=D_{\rm KL}(\zeta_a\Vert p_a\otimes r_a)
-\mathbb E_{\zeta_a}\log\ell_a(o_a\mid K_a,M_a).
\]

Let (q_a,s_a) be the marginals of (\zeta_a). Insert (q_a\otimes s_a) into the density ratio:

\[
\log\frac{d\zeta_a}{d(p_a\otimes r_a)}
=\log\frac{d\zeta_a}{d(q_a\otimes s_a)}
+\log\frac{dq_a}{dp_a}
+\log\frac{ds_a}{dr_a}.
\]

Taking (\zeta_a)-expectations yields

\[
D_{\rm KL}(\zeta_a\Vert p_a\otimes r_a)
=D_{\rm KL}(q_a\Vert p_a)
+D_{\rm KL}(s_a\Vert r_a)
+I_{\zeta_a}(K_a;M_a),
\]

where

\[
I_{\zeta_a}(K_a;M_a)
:=D_{\rm KL}(\zeta_a\Vert q_a\otimes s_a)\ge0.
\]

The correction vanishes exactly when the private state and model coordinates are independent under
(\zeta_a).

## Belief-relational block

For (u_{ab}^n=(\Omega_{ab}^n)_\#q_b^n),

\[
\begin{aligned}
\mathcal F_a^q
&=D_{\rm KL}\!\left(
\beta_{ab}q_a(dx)\middle\|\pi_{ab}^q u_{ab}^n(dx)
\right)\\
&=D_{\rm KL}(\beta_a\Vert\pi_a^q)
+\sum_{b\in J_a^q}\beta_{ab}
D_{\rm KL}\!\left(q_a\middle\|u_{ab}^n\right).
\end{aligned}
\]

The first equality is a KL on the joint label-copy space. The second is the finite-mixture KL chain
rule; it follows directly by splitting

\[
\log\frac{\beta_{ab}\,dq_a}{\pi_{ab}^q\,du_{ab}^n}
=\log\frac{\beta_{ab}}{\pi_{ab}^q}
+\log\frac{dq_a}{du_{ab}^n}.
\]

## Model-relational block

The identical calculation with
(v_{ab}^n=(\widetilde\Omega_{ab}^n)_\#s_b^n) gives

\[
\mathcal F_a^s
=D_{\rm KL}(\gamma_a\Vert\pi_a^s)
+\sum_{b\in J_a^s}\gamma_{ab}
D_{\rm KL}\!\left(s_a\middle\|v_{ab}^n\right).
\]

## Exact assembled identity

Combining the three blocks gives

\[
\boxed{
\begin{aligned}
\mathcal F_h^{n+1}
=\sum_{a\in A}\Bigg[&
D_{\rm KL}(q_a\Vert p_a)
+D_{\rm KL}(s_a\Vert r_a)
+I_{\zeta_a}(K_a;M_a)\\
&-\mathbb E_{\zeta_a}\log\ell_a(o_a\mid K_a,M_a)\\
&+D_{\rm KL}(\beta_a\Vert\pi_a^q)
+\sum_b\beta_{ab}D_{\rm KL}
\left(q_a\middle\|(\Omega_{ab}^n)_\#q_b^n\right)\\
&+D_{\rm KL}(\gamma_a\Vert\pi_a^s)
+\sum_b\gamma_{ab}D_{\rm KL}
\left(s_a\middle\|(\widetilde\Omega_{ab}^n)_\#s_b^n\right)
\Bigg].
\end{aligned}}
\]

Define the **joint-typed lagged unit-coefficient two-channel scalar**
(\mathcal F_{\mathrm{JT},h}^{\mathrm{lag},1}) as the same display with the mutual-information
term removed. In particular, its observation contribution remains the well-typed joint-private
expectation (-\mathbb E_{\zeta_a}\log\ell_a(o_a\mid K_a,M_a)). Then

\[
\mathcal F_h^{n+1}
=\mathcal F_{\mathrm{JT},h}^{\mathrm{lag},1}
+\sum_{a\in A}I_{\zeta_a}(K_a;M_a).
\]

Under the state-model mean-field restriction (\zeta_a=q_a\otimes s_a),

\[
\mathcal F_h^{n+1}
=\mathcal F_{\mathrm{JT},h}^{\mathrm{lag},1}.
\]

This equality has unit state-self, model-self, peer-energy, and categorical-KL coefficients. It uses
counting measure on the finite index set. It includes the normalized joint-private observation
factor once. It is an exact negative ELBO on the enlarged tied-replica inventory, not on the
original single-copy inventory. No equality to the literal PIFB2 observation display is asserted;
that separate source-comparison claim remains unresolved in `pifb2-crosswalk.md`.

Finally, because (P_h^n) is normalized and has positive finite evidence,

\[
\mathcal F_h^{n+1}
=-\log p_h^n(o\mid H_n)
+D_{\rm KL}\!\left(Q^{n+1}\middle\|P_h^n(\cdot\mid o,H_n)\right).
\]
