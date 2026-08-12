<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-ea859a3e62b93365692fe1b959217ec3c21100b535e3a6633999bc36a431af9f","schema_version":"rigorous-theory-search/v1","target_digest":"ea859a3e62b93365692fe1b959217ec3c21100b535e3a6633999bc36a431af9f"} -->
# Construction or strongest theorem

Let (A) be a nonempty finite agent-site set and assume the probability data and support conditions
in the frozen contract. Conditional on the stored history (H_n), introduce for every (a\in A)
a private state-model pair, a belief source-label/copy pair, and a model source-label/copy pair. Give
these blocks the normalized generative law in `evidence/typed-construction.md` and restrict the
recognition family so the private marginals (q_a,s_a) are reused on their respective relational
copies.

Then the generative law is normalized and independent of the current recognition law. Its exact
negative ELBO is

\[
\begin{aligned}
\mathcal F_h^{n+1}
=\sum_{a\in A}\Bigg[&
D_{\rm KL}(q_a\Vert p_a)+D_{\rm KL}(s_a\Vert r_a)
+I_{\zeta_a}(K_a;M_a)
-\mathbb E_{\zeta_a}\log\ell_a(o_a\mid K_a,M_a)\\
&+D_{\rm KL}(\beta_a\Vert\pi_a^q)
+\sum_b\beta_{ab}D_{\rm KL}\!\left(
q_a\middle\|(\Omega_{ab}^n)_\#q_b^n\right)\\
&+D_{\rm KL}(\gamma_a\Vert\pi_a^s)
+\sum_b\gamma_{ab}D_{\rm KL}\!\left(
s_a\middle\|(\widetilde\Omega_{ab}^n)_\#s_b^n\right)
\Bigg].
\end{aligned}
\]

Consequently,

\[
\mathcal F_h^{n+1}
=\mathcal F_{\rm PIFB2,h}^{\rm lag,1}
+\sum_{a\in A}I_{\zeta_a}(K_a;M_a).
\]

If (\zeta_a=q_a\otimes s_a) for every (a), the correction vanishes and the finite ELBO equals
the lagged, unit-temperature, unit-private-coefficient two-channel PIFB2 scalar exactly. Under the
declared simultaneous bimeasurable endpoint actions and likelihood covariance, the scalar is
invariant.

This theorem is complete at its finite conditional scope. It does not establish same-time
reciprocal emergence, nonunit temperature, adaptive weights, cell-volume continuum scaling,
curvature dynamics, or a probability law on continuum sections.
