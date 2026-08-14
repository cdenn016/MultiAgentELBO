<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-c68f474d3e7991fa78a557b86bd645dc1c01a4272b2a75d53a52e17ad29176b2","schema_version":"rigorous-theory-search/v1","target_digest":"c68f474d3e7991fa78a557b86bd645dc1c01a4272b2a75d53a52e17ad29176b2"} -->
# Oracle-erasure check

## Method and erased material

An isolated checker removed `target.search_priors`, ignored every ledger state,
PASS assertion, adversarial disposition, final-report conclusion, agent-only
ontology, physicalization claim, canonical-agentization claim, and
preferred-lift principle. It also erased contract premise 5, because saying
that each proposed lift is already a smooth right inverse semantically repeats
one dependency claim. The premise is redundant rather than load-bearing: the
checker rederived its content directly from the displayed formula.

Covered claims are `target` and every transitive dependency ancestor:
`collapsed-vfe-descent`, `conditional-kl-completion`,
`full-latent-nondescend`, `retained-fisher-descent`,
`binary-dilation-boundary`, `paired-marginal-noncanonicity`,
`smooth-right-inverse-lifts`, `vfe-lift-dependence`, and
`fisher-lift-dependence`.

## Derivation after erasure

Retained-law equality fixes evidence and the retained posterior. Therefore

\[
\mathcal F_{\rm coll}(Q_R;o)
=-\log P_O(o)+D_{\rm KL}(Q_R\|P_R(\cdot\mid o))
\]

is constant on the observational quotient. Finite disintegration and the KL
chain rule independently yield the auxiliary conditional-KL defect. Its zero
condition on \(Q_R\ll P_R(\cdot\mid o)\) proves posterior completion and
conditional minimization; a null binary auxiliary gives the strict \(\log2\)
non-descent control.

Parameterwise equality of strictly positive finite categorical families gives
termwise equality of derivatives, scores, and Fisher tensors. Fixed outcome
relabeling reindexes the sum, and a common \(C^1\) pullback preserves equality.

For the XOR family, direct marginalization gives
\(\delta=a+b-2ab\). Independent Bernoulli mismatch coordinates give the
retained and full Fisher tensors without assuming descent. Their ranks are at
most one, two, and three across the open parameter cube.

After erasing the right-inverse premise, direct factorization of the proposed
lift cells gives

\[
(1-a)b[1-\kappa a(1-b)]>0,
\qquad
a(1-b)[1-\kappa(1-a)b]>0.
\]

Summation gives normalization and marginals \((a,b)\), and polynomial
dependence gives smoothness. At the center, direct KL and Fisher calculations
give

\[
D_{\rm KL}(\iota_0\|\iota_{1/2})
=\tfrac12\log(64/63)>0,
\]

\[
g_0=4I_2,
\qquad
g_{1/2}=\frac1{63}
\begin{pmatrix}256&-32\\-32&256\end{pmatrix},
\]

with difference eigenvalues \(-4/9\) and \(4/7\). Thus the noncanonicity
claim is derived rather than assumed.

## Result

**PASS.** Every dependency-closure claim follows after removal of the
affirmative prior and the semantically circular right-inverse premise. No
agent-only ontology, physical geometry, preferred lift, or desired descent
claim is used as an axiom. The deterministic executable is only corroboration;
the derivations close the mathematics.

The checker separately observed that the inspected pre-release scaffold still
had placeholder hashes and empty terminal records. Those provenance
obligations are resolved only by the final artifact binding and release-mode
validator, not by oracle erasure.
