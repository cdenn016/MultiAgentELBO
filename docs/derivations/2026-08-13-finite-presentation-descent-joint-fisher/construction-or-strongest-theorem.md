<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-c68f474d3e7991fa78a557b86bd645dc1c01a4272b2a75d53a52e17ad29176b2","schema_version":"rigorous-theory-search/v1","target_digest":"c68f474d3e7991fa78a557b86bd645dc1c01a4272b2a75d53a52e17ad29176b2"} -->
# Finite presentation-descent and joint-lift boundary theorem

## Definitions

A finite presentation is a normalized law \(P_{REO}\) on nonempty finite
retained, auxiliary, and record spaces. Two presentations are observationally
equivalent when, after the declared identification of \(R\) and \(O\), their
retained laws \(P_{RO}\) agree and their retained conditioning sigma-algebras
agree up to completion. In a parameterized family this equality is required
for every parameter under one fixed parameter identification.

For an observation \(o\) of positive evidence \(z_o=P_O(o)\), define

\[
\mathcal F_{\rm coll}(Q_R;o)
=-\log z_o+D_{\rm KL}\!\left(Q_R\middle\|P_R(\cdot\mid o)\right).
\]

## Theorem

Under the frozen finite, normalization, support, and regularity hypotheses:

1. The collapsed VFE is constant on every observational-equivalence class.

2. If
   \(Q_{RE}=Q_R\eta(E\mid R)\) and
   \(P_{RE\mid o}=P_R(\cdot\mid o)\kappa_o(E\mid R)\), then

   \[
   \mathcal F_{\rm full}(Q_R\eta;o)
   =\mathcal F_{\rm coll}(Q_R;o)
   +\mathbb E_{Q_R}D_{\rm KL}(\eta(\cdot\mid R)\|\kappa_o(\cdot\mid R)).
   \tag{1}
   \]

   On the tier \(Q_R\ll P_R(\cdot\mid o)\), equality holds exactly at
   posterior completion, \(Q_R\)-almost surely. Minimization over all
   auxiliary lifts has value \(\mathcal F_{\rm coll}\) and a unique minimizing
   joint law \(Q_R\kappa_o\). Kernel values on \(Q_R\)-null retained states are
   irrelevant.

3. If two strictly positive \(C^2\) retained categorical families agree
   parameterwise, then their score functions and retained Fisher tensors
   agree. A fixed parameter-independent sample relabeling merely reindexes
   the Fisher sum. Consequently every common \(C^1\) configuration pullback of that
   retained tensor also agrees.

4. Paired marginal sections do not determine a full-joint VFE or Fisher
   tensor. For \((a,b)\in(0,1)^2\), set

   \[
   d_\kappa=\kappa a(1-a)b(1-b)
   \]

   and, in the outcome order \((00,01,10,11)\),

   \[
   \iota_\kappa(a,b)=\bigl(
   (1-a)(1-b)+d_\kappa,
   (1-a)b-d_\kappa,
   a(1-b)-d_\kappa,
   ab+d_\kappa\bigr).
   \tag{2}
   \]

   Both \(\iota_0\) and \(\iota_{1/2}\) are smooth positive right inverses of
   paired marginalization. At \(a=b=1/2\), they are respectively
   \((8,8,8,8)/32\) and \((9,7,7,9)/32\). Against the uniform posterior their
   VFE values differ, and their Fisher pullbacks are

   \[
   \begin{pmatrix}4&0\\0&4\end{pmatrix}
   \quad\text{and}\quad
   \frac1{63}\begin{pmatrix}256&-32\\-32&256\end{pmatrix}.
   \tag{3}
   \]

   Thus the lift/dependence sector is additional model structure.

## Proof dependency map

The first two conclusions follow from evidence and posterior equality plus the
finite relative-entropy chain rule. The support-qualified zero condition for
KL proves the equality and minimization clauses. The third conclusion follows
by substituting the common retained family into the finite score-covariance
definition. The fourth follows by direct positivity, normalization,
marginalization, KL, and Fisher calculations for (2). Full derivations are in
`evidence/vfe-descent-proof.md` and `evidence/fisher-lift-proof.md`.

The independent binary XOR family in
`evidence/bsc-presentation-proof.md` verifies that this boundary is
nonvacuous: a direct record channel, a latent environment chain, and the same
chain with an independent null node have identical retained laws, while their
uncompleted full VFEs, full Fisher tensors, node inventories, and typed
intervention structures can differ.

## Sharp boundaries

Equation (1) is an extended-real additive identity. If the retained
recognition law is singular with respect to the posterior, an
\(+\infty=+\infty\) equality does not imply conditional matching and posterior
kernels on posterior-null states are version dependent.

Parameterwise retained-family equality is essential for Fisher descent.
Equality at one parameter does not determine score derivatives. Likewise,
pointwise existence of a product coupling does not establish an admissible
smooth equivariant lift in a more restrictive continuum theory.

The theorem identifies invariants of the finite observational quotient. It
does not prove that environment nodes are autonomous agents, select a
canonical agentization, preserve auxiliary intervention algebras, construct a
continuum probability on section space, or turn an informational semimetric
into spacetime, causal structure, time, mass, or a dimensional constant.
