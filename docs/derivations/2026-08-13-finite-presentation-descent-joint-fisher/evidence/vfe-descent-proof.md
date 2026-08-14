<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-c68f474d3e7991fa78a557b86bd645dc1c01a4272b2a75d53a52e17ad29176b2","schema_version":"rigorous-theory-search/v1","target_digest":"c68f474d3e7991fa78a557b86bd645dc1c01a4272b2a75d53a52e17ad29176b2"} -->
# Collapsed VFE descent and the auxiliary conditional-KL defect

## Typed setting

Let \(R\), \(O\), and each auxiliary space \(E_a\) be nonempty finite sets
with their full sigma-algebras. A presentation is a normalized law

\[
P^a_{R E_a O}\in\mathcal P(R\times E_a\times O).
\]

Two presentations are observationally equivalent when their retained
marginals \(P^a_{RO}\) agree under the declared identification of \((R,O)\),
and their retained conditioning sigma-algebras agree up to \(P_O\)-completion.
Auxiliary split, merge, dilation, and independent-null-node insertion are
admitted only when they preserve these retained data.

Fix \(o\in O\) with evidence \(z_o=P_O(o)>0\). Counting measure supplies
canonical pointwise representatives on positive-mass slices. Define

\[
\pi_o(r)=P(R=r\mid O=o),\qquad
\mathcal F_{\rm coll}(Q_R;o)
=-\log z_o+D_{\rm KL}(Q_R\|\pi_o).
\]

For a full recognition law with retained marginal \(Q_R\), write

\[
Q^a_{R E_a}(r,e)=Q_R(r)\eta^a(e\mid r),
\qquad
P^a_{R E_a\mid o}(r,e)=\pi_o(r)\kappa^a_o(e\mid r).
\]

The posterior kernel \(\kappa^a_o\) is unique on every \(r\) with
\(\pi_o(r)>0\); its values elsewhere are version choices.

## Theorem

For every observationally equivalent pair, every common \(Q_R\), and every
selected positive-evidence observation,

\[
\mathcal F^{1}_{\rm coll}(Q_R;o)=\mathcal F^{2}_{\rm coll}(Q_R;o).
\]

For every presentation \(a\), the full-latent VFE satisfies the extended-real
additive identity

\[
\mathcal F^a_{\rm full}(Q_R\eta^a;o)
=\mathcal F_{\rm coll}(Q_R;o)
+\sum_r Q_R(r)D_{\rm KL}\!\left(
\eta^a(\cdot\mid r)\middle\|\kappa^a_o(\cdot\mid r)
\right).
\tag{1}
\]

If \(Q_R\ll\pi_o\) and the displayed conditional KL terms are finite, equality
of the full and collapsed VFEs holds exactly when

\[
\eta^a(\cdot\mid r)=\kappa^a_o(\cdot\mid r)
\quad Q_R\text{-almost everywhere}.
\tag{2}
\]

Consequently,

\[
\min_{Q_{R E_a}:(Q_{R E_a})_R=Q_R}
\mathcal F^a_{\rm full}(Q_{R E_a};o)
=\mathcal F_{\rm coll}(Q_R;o),
\tag{3}
\]

and the unique minimizing joint law is

\[
Q^{a,*}_{R E_a}(r,e)=Q_R(r)\kappa^a_o(e\mid r).
\tag{4}
\]

Kernel values on \(Q_R\)-null retained states are immaterial and do not spoil
uniqueness of the joint law.

## Proof

The retained evidence \(z_o\) and posterior \(\pi_o\) are determined by
\(P_{RO}\). Therefore \(\mathcal F_{\rm coll}\) is constant on each
observational-equivalence class.

On the support of \(Q_R\eta^a\), split the log density ratio:

\[
\log\frac{Q_R(r)\eta^a(e\mid r)}
{\pi_o(r)\kappa^a_o(e\mid r)}
=\log\frac{Q_R(r)}{\pi_o(r)}
+\log\frac{\eta^a(e\mid r)}{\kappa^a_o(e\mid r)}.
\]

Summing first over \(e\), then over \(r\), proves the relative-entropy chain
rule and (1). This identity is additive in \([0,+\infty]\); subtraction is
legitimate only when the collapsed term is finite. Nonnegativity of every
conditional KL proves (2), and choosing \(\eta^a=\kappa^a_o\) proves
attainability in (3). The finite-space KL zero condition proves (4) and
joint-law uniqueness.

## Sharp failure controls

Let \(R=O=\{*\}\). The collapsed VFE is zero. Insert an observationally null
binary auxiliary whose posterior is uniform, while choosing recognition
\(\delta_0\). The retained law and conditioning algebra are unchanged, but
the full VFE is

\[
D_{\rm KL}(\delta_0\|(1/2,1/2))=\log2.
\]

Posterior completion or merging the null split restores zero. Thus an
arbitrary unminimized full-latent VFE does not descend.

The support hypothesis is load-bearing. If \(\pi_o=\delta_0\) and
\(Q_R=\delta_1\), both collapsed and full VFEs are \(+\infty\). Changing the
posterior-kernel version on the posterior-null state can change the displayed
conditional defect without changing the generative law. Therefore the raw
statement \(+\infty=+\infty\) implies neither conditional matching nor
intrinsic kernel uniqueness.

## Scope

The result is finite and observational. It does not identify intervention
algebras across presentations, prove that an auxiliary node is autonomous, or
turn representational equivalence into ontological identity.
