# Finite-horizon process extension

The one-step theorem conditions on (H_n). This makes the source laws
((\Omega_{ab}^n)_\#q_b^n) and
((\widetilde\Omega_{ab}^n)_\#s_b^n) fixed during the (n+1) recognition update even though the
stored beliefs and models change between steps.

Let the algorithmic history state (H_n) contain the stored law-valued fields, transports, priors,
and observation record. Suppose the update rule that forms (P_h^n(\cdot\mid H_n)), receives the
next observation, and maps the result to (H_{n+1}) is measurable. On a finite horizon, the iterated
normalized kernels define a normalized history/process law. Thus both endpoints can fluctuate over
time without contemporaneous dependence of the generative kernel on the variational law currently
being optimized.

This is a conditional adaptive-process construction. It is not an equilibrium derivation of the
same-time scalar

\[
D_{\rm KL}\!\left(q_a^{n+1}\middle\|(\Omega_{ab}^{n+1})_\#q_b^{n+1}\right),
\]

and it is not a probability law on continuum section space. To randomize the law-valued fields
themselves, promote them to typed configuration variables and supply their transition kernel or
configuration prior, entropy, and normalization.
