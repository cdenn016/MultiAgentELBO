# Typed tied-replica construction

## Finite index and probability data

Let (A) be a nonempty finite set of active agent-site indices. An element (a=(i,x)) records one
of finitely many agents at one point of a finite lattice or experimental design. Refining the base
and taking (N\to\infty) are not part of this construction.

For every (a\in A), let ((\mathsf K_a,\mathscr K_a)),
((\mathsf M_a,\mathscr M_a)), and ((\mathsf O_a,\mathscr O_a)) be standard-Borel spaces. Declare
private probability laws

\[
p_a\in\mathcal P(\mathsf K_a),\qquad
r_a\in\mathcal P(\mathsf M_a),
\]

and a normalized observation kernel

\[
L_a(do\mid k,m):\mathsf K_a\times\mathsf M_a\rightsquigarrow\mathsf O_a.
\]

Relative to an observation reference (\nu_a), choose a jointly measurable density
(\ell_a(o\mid k,m)) for (L_a). The theorem fixes one admitted observation (o_a), assumes a
positive finite evidence, and either assumes finiteness of all displayed terms or uses the standard
extended-value conventions.

The model section (s_a) is a probability law on the model-parameter fiber (\mathsf M_a). It is
the agent's slow generative-model state. The likelihood kernel tells how a parameter value (m)
generates observations; the predictive kernel induced by (s_a) is

\[
\overline L_a(do\mid k)=\int L_a(do\mid k,m)s_a(dm).
\]

## Lagged transported sources

Condition on a stored history (H_n) containing the previous recognition laws (q_b^n,s_b^n)
and measurable transports

\[
\Omega_{ab}^n:\mathsf K_b\to\mathsf K_a,
\qquad
\widetilde\Omega_{ab}^n:\mathsf M_b\to\mathsf M_a.
\]

For the finite active source sets (J_a^q,J_a^s), define the normalized pushforward laws

\[
u_{ab}^n=(\Omega_{ab}^n)_\#q_b^n,
\qquad
v_{ab}^n=(\widetilde\Omega_{ab}^n)_\#s_b^n.
\]

Let (\pi_a^q=(\pi_{ab}^q)_{b\in J_a^q}) and
(\pi_a^s=(\pi_{ab}^s)_{b\in J_a^s}) be normalized positive source rows. If an agent has no
admissible source, the corresponding relational factor is absent. An all-zero row is not treated as
a probability distribution.

## Normalized generative joint

Introduce three mutually distinct latent blocks for each (a):

1. a private state-model pair ((K_a,M_a));
2. a belief-relational label and copy ((J_a^q,X_a));
3. a model-relational label and copy ((J_a^s,Y_a)).

Conditional on (H_n), define

\[
\begin{aligned}
P_a^n(&do,dk,dm,dj,dx,d\ell,dy)={}&
p_a(dk)r_a(dm)L_a(do\mid k,m)\\
&&\times\pi_{aj}^q u_{aj}^n(dx)
\times\pi_{a\ell}^s v_{a\ell}^n(dy).
\end{aligned}
\]

Every displayed factor is normalized. Finite sums and Tonelli therefore give
(P_a^n(\mathsf O_a\times\mathsf Z_a)=1). The global conditional joint

\[
P_h^n=\bigotimes_{a\in A}P_a^n
\]

is normalized. This product is an existential witness, not a claim that all useful multi-agent
generative laws factor across (a).

## Tied-replica recognition family

Let (\zeta_a(dk,dm)) be a joint private recognition law with marginals

\[
q_a=(\operatorname{pr}_{K})_\#\zeta_a,
\qquad
s_a=(\operatorname{pr}_{M})_\#\zeta_a.
\]

Let (\beta_a\) and (\gamma_a) be normalized recognition rows. Define

\[
Q_a^{n+1}(dk,dm,dj,dx,d\ell,dy)
=\zeta_a(dk,dm)\,\beta_{aj}q_a(dx)\,\gamma_{a\ell}s_a(dy).
\]

The private and relational random variables are not identified. Their recognition marginals are
tied. This is an explicit variational-family restriction that makes the same displayed (q_a) and
(s_a) serve private and relational informational roles. The global recognition law is the finite
product of the (Q_a^{n+1}). Absolute continuity is required against the fixed-observation slice of
(P_h^n).
