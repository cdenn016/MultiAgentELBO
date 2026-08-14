<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-c68f474d3e7991fa78a557b86bd645dc1c01a4272b2a75d53a52e17ad29176b2","schema_version":"rigorous-theory-search/v1","target_digest":"c68f474d3e7991fa78a557b86bd645dc1c01a4272b2a75d53a52e17ad29176b2"} -->
# Independent reconstruction

## Method

An isolated reconstructor read `problem-contract.json` first and did not read
the construction, final report, ledger evidence, or evidence derivations until
after deriving a candidate result. It independently reconstructed all target
dependencies, constructed a second direct-versus-latent binary witness, and
then compared its result with the run artifacts.

## Reconstruction

For a finite presentation \(P_{REO}\) and a positive-evidence observation
\(o\), retained-law equality fixes

\[
z_o=P_O(o),\qquad \pi_o=P_R(\cdot\mid o).
\]

Therefore

\[
\mathcal F_{\rm coll}(Q_R;o)
=-\log z_o+D_{\rm KL}(Q_R\|\pi_o)
\]

is presentation invariant. Disintegrating
\(Q_{RE}=Q_R\eta(E\mid R)\) and
\(P_{RE\mid o}=\pi_o\kappa_o(E\mid R)\) gives, atom by atom,

\[
\mathcal F_{\rm full}(Q_R\eta;o)
=\mathcal F_{\rm coll}(Q_R;o)
+\mathbb E_{Q_R}D_{\rm KL}(\eta(\cdot\mid R)\|\kappa_o(\cdot\mid R)).
\]

On \(Q_R\ll\pi_o\), KL nonnegativity and its zero condition give exact
posterior completion and the unique minimizing joint law
\(Q_R\kappa_o\). With singular \(Q_R\), infinite equality is vacuous, exactly
matching the stated boundary. A posterior-uniform null binary auxiliary with
recognition \(\delta_0\) gives the independent strict defect \(\log2\).

For a strictly positive finite categorical family, parameterwise retained-law
equality gives termwise equality of scores and Fisher tensors. A fixed outcome
relabeling reindexes the sum. Every common \(C^1\) configuration pullback is
therefore equal. The reconstructor independently recovered the one-point
countercontrol with Fisher values 4 and 16.

The reconstructor then derived the lift family

\[
\iota_\kappa(a,b)=\bigl(
(1-a)(1-b)+d_\kappa,
(1-a)b-d_\kappa,
a(1-b)-d_\kappa,
ab+d_\kappa\bigr),
\]

where \(d_\kappa=\kappa a(1-a)b(1-b)\). Factoring the two subtracted cells
proves global positivity for \(0\le\kappa<1\), and direct summation proves the
right-inverse identities. For \(\kappa=0,1/2\) at the center, independent
calculation gives

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

with difference eigenvalues \(-4/9\) and \(4/7\).

## Independent presentation witness

As a construction independent of the run's XOR chain, the reconstructor used
parameters \((\phi,\tau)\), a uniform binary auxiliary, and direct versus
auxiliary-conditioned record accuracies
\(\phi\) and \(\phi+(-1)^e\tau\). Marginalization over the auxiliary produces
the same retained record law in both presentations. The retained Fisher is

\[
\operatorname{diag}([\phi(1-\phi)]^{-1},0),
\]

while the latent full Fisher is

\[
\frac12
\begin{pmatrix}A+B&A-B\\A-B&A+B\end{pmatrix},
\]

where
\(A=[(\phi+\tau)(1-\phi-\tau)]^{-1}\) and
\(B=[(\phi-\tau)(1-\phi+\tau)]^{-1}\). The auxiliary interventions also
change record accuracy by \(\pm\tau\). This independently establishes the same
descent/non-descent boundary without using the run's witness.

## Comparison and result

The contract-only reconstruction agrees exactly with the substantive run on
all dependency claims:

- `collapsed-vfe-descent` — PASS;
- `conditional-kl-completion` — PASS;
- `full-latent-nondescend` — PASS;
- `retained-fisher-descent` — PASS;
- `binary-dilation-boundary` — PASS;
- `smooth-right-inverse-lifts` — PASS;
- `vfe-lift-dependence` — PASS;
- `fisher-lift-dependence` — PASS;
- `paired-marginal-noncanonicity` — PASS;
- `target` — PASS.

No autonomous-agency, ontology, physical-geometry, continuum, time,
dimensionful-constant, or novelty claim was used. The reconstruction's only
pre-release objection was the then-unpopulated hash/adversarial/release
scaffold, not the mathematics.
