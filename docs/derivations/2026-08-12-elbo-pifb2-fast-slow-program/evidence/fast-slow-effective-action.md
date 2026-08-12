# Fast/slow effective action

For slow structure (S), normalized likelihood evidence (p(o\mid S)), posterior
(P(dz\mid o,S)), and recognition law (Q),

[
\mathcal F_{\rm state}[Q;S,o]
=-\log p(o\mid S)+D_{\rm KL}(Q\Vert P(\cdot\mid o,S)).
]

Therefore

[
\inf_Q\mathcal F_{\rm state}[Q;S,o]=-\log p(o\mid S)
]

when the exact posterior is admitted. Restricted recognition adds the minimum posterior-KL gap.
With slow prior density (dP_0/d\nu_S), the profiled slow density action is

[
S_{\rm slow}^{\rm eff}(S;o)
=-\log p(o\mid S)-\log\frac{dP_0}{d\nu_S}(S)
]

up to an observation-dependent additive constant.

For gradient-flow dynamics (dot q=-\nabla_qF(q,S)),
(dot S=-\epsilon\nabla_SF(q,S)), substitution of (q^*(S)) is justified only after proving a
uniformly attracting normally hyperbolic fast branch. At nonzero fast temperature,

[
e^{-S_{\rm eff}(S)/T_q}=\int e^{-F(q,S)/T_q}\,\nu_q(dq),
]

and the saddle expansion contains fluctuation determinants. Profiling is the zero-temperature or
exact-optimization operation, not the generic finite-temperature action.
