# Gauge and coordinate invariance proof

The finite theorem requires no gauge-field integration. Its symmetry statement is invariance under
simultaneous fiber-coordinate changes.

For each (a), let (g_a^q:\mathsf K_a\to\mathsf K_a') and
(g_a^s:\mathsf M_a\to\mathsf M_a') be measurable bimeasurable bijections. Transform

\[
q_a'=(g_a^q)_\#q_a,quad p_a'=(g_a^q)_\#p_a,quad
s_a'=(g_a^s)_\#s_a,quad r_a'=(g_a^s)_\#r_a,
\]

and (\zeta_a'=(g_a^q\times g_a^s)_\#\zeta_a). Let the edge maps transform by endpoint
conjugation,

\[
(\Omega_{ab}^n)'=g_a^q\circ\Omega_{ab}^n\circ(g_b^q)^{-1},
\qquad
(\widetilde\Omega_{ab}^n)'=g_a^s\circ\widetilde\Omega_{ab}^n\circ(g_b^s)^{-1}.
\]

Then

\[
((\Omega_{ab}^n)')_\#q_b'
=(g_a^q)_\#(\Omega_{ab}^n)_\#q_b,
\]

and analogously in the model channel. Relative entropy is invariant under a bimeasurable bijection:

\[
D_{\rm KL}(g_\#\mu\Vert g_\#\nu)=D_{\rm KL}(\mu\Vert\nu).
\]

Therefore every private, belief-relational, model-relational, categorical, and mutual-information
KL term is unchanged. The likelihood contribution is unchanged if the transformed density
representative satisfies

\[
\ell_a'(o_a'\mid g_a^qk,g_a^sm)=\ell_a(o_a\mid k,m)
\]

for the correspondingly transformed observation record, or if the observation is a gauge scalar.
The rows (\beta,\gamma,\pi^q,\pi^s) are label probabilities and do not transform under fiber
coordinates. Hence the complete finite scalar is invariant.

For a principal group (G) acting through representations on the two statistical fibers, this is
the passive-gauge statement with (g_a^q=\rho_q(g_a)) and (g_a^s=\rho_s(g_a)). Algebraic KL
invariance does not require compactness. Compactness becomes important only when one integrates
over dynamical links or frames using a normalized Haar reference and seeks coercive curvature
actions.
