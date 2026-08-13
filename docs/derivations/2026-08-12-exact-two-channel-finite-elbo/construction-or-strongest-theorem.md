<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-f091d276dce8d75cad91f94bafb714df817d148010529b51cdde612e77ff4bc2","schema_version":"rigorous-theory-search/v1","target_digest":"f091d276dce8d75cad91f94bafb714df817d148010529b51cdde612e77ff4bc2"} -->
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

Define the **joint-typed lagged unit-coefficient two-channel scalar**
(\mathcal F_{\mathrm{JT},h}^{\mathrm{lag},1}) by the same display with the mutual-information term
removed. Thus

\[
\mathcal F_h^{n+1}
=\mathcal F_{\mathrm{JT},h}^{\mathrm{lag},1}
+\sum_{a\in A}I_{\zeta_a}(K_a;M_a).
\]

If (\zeta_a=q_a\otimes s_a) for every (a), the correction vanishes and the finite ELBO equals
(\mathcal F_{\mathrm{JT},h}^{\mathrm{lag},1}) exactly. Under the declared simultaneous
bimeasurable endpoint actions and likelihood covariance, the scalar is invariant.

This theorem is complete at its finite conditional scope. It does not identify its joint-private
observation term with the literal PIFB2 observation display, which remains a separate inconclusive
nondependency claim pending an author-approved typing convention. It also does not establish
same-time reciprocal emergence, nonunit temperature, adaptive weights, cell-volume continuum
scaling, curvature dynamics, or a probability law on continuum sections.
