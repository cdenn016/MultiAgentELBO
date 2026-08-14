<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-ebf8914b08524414858dcfd879ec3b08e5abd21bb0c9f8f36feb64d97f1cd7f2","schema_version":"rigorous-theory-search/v1","target_digest":"ebf8914b08524414858dcfd879ec3b08e5abd21bb0c9f8f36feb64d97f1cd7f2"} -->
# Counterexample register

## C1: fixed scalar kappa fails odd-flip equivariance

For any nonzero \(\kappa\), complementing one bit reverses \(\chi\) while
leaving \(D\) invariant. Thus the pushforward is
\(Q_{C\theta,-\kappa}\), not \(Q_{C\theta,\kappa}\). The executable checks all
64 atoms off center. Declaring \(\kappa\) a pseudoscalar repairs covariance,
but that declaration is extra structure.

## C2: singleton sections do not select the joint lift

For fixed \(\theta\), every \(\kappa\in(-1,1)\) has the same six singleton
marginals, indeed the same 63 proper marginals. Distinct \(\kappa\) values
give distinct full laws. This refutes any selection of \(\kappa\), full-joint
VFE, or full-joint Fisher from the singleton sections alone.

## C3: two-bit Fisher correction is signed and indefinite

At the two-bit center with \(\kappa=1/2\), the correlated law is
\((9,7,7,9)/32\) and

\[
G_2=\frac1{63}\begin{pmatrix}256&-32\\-32&256\end{pmatrix}.
\]

The eigenvalues of \(G_2-4I_2\) are \(-4/9\) and \(4/7\). This refutes a
universal claim that any joint lift equals the marginal Fisher metric plus a
positive-semidefinite correction. The six-bit parity theorem needs its
pairwise-independence and score-orthogonality hypotheses.

## C4: same record marginals can cancel the product interaction

For \(|a|,|b|\le\eta<1/2\), the four strictly positive atoms

\[
(q_{11},q_{10},q_{01},q_{00})
=\tfrac14(1+a+b,1+a-b,1-a+b,1-a-b)
\]

have the same two binary marginals as the conditionally independent product
kernel, but their \(ab\) coefficient is zero. This refutes inference of the
product kernel or its possible six-bit term from the two marginal kernels.

## C5: incoherent target handling breaks VFE covariance

KL is invariant when both recognition and target are pushed forward by the
same finite bijection. If only recognition is pushed and a noninvariant target
is held fixed in its old coordinates, the two KL values can differ. This is
the sharp boundary on fixed-target paired-complement covariance.

## C6: redundant interaction amplitudes lose rank

For \(Q=P+(\kappa\eta)\chi D\), the interaction derivatives are proportional.
Only \(\kappa\eta\) is identifiable; the interaction Fisher block has rank at
most one and rank zero at the origin. This refutes a claim that adding both
symbols automatically creates two Fisher directions.

## C7: physical and canonical conclusions are not entailed

The finite construction supplies no intervention algebra, autonomous-agency
criterion, GL(K) bundle, continuum limit, operational clock, dimensionful
units, or coarse-graining map. Since these objects are absent from the
premises, the release neither verifies nor refutes a future theorem that adds
them; it blocks inference of those conclusions from this package alone.
