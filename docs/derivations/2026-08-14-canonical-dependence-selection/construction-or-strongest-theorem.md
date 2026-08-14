<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-b8102c1f5917a6cbc9a69df8b10c1470d18d5146f56093a253b1a8644465bccb","schema_version":"rigorous-theory-search/v1","target_digest":"b8102c1f5917a6cbc9a69df8b10c1470d18d5146f56093a253b1a8644465bccb"} -->
# Construction or strongest theorem

## Direct negative result

For the frozen finite marginal functor \(m_X:J(X)\to M(X)\), preparation kernels from singleton lists force every section natural under all coordinatewise finite Markov kernels with independently tensored randomness to be

\[
S_X(\mu_1,\ldots,\mu_n)=\bigotimes_i\mu_i.
\]

More strongly, a wide marginal-compatible category containing all those local kernels admits a natural section if and only if every added kernel preserves product laws; when it exists, the section is unique for that morphism class. Hence the product-preserving marginal-compatible kernels form the maximal such category.

For a fair source bit, the two marginal-compatible split kernels \(R_{1/3}\) and \(R_{1/2}\) both produce fair/fair target marginals but require selected output laws with atom multisets

\[
\{1/3,1/3,1/6,1/6\}
\quad\text{and}\quad
\{3/8,3/8,1/8,1/8\}.
\]

These multisets remain distinct under every sample relabeling. The section axiom plus naturality under these two splits, without any local-kernel naturality assumption, forces one single-valued selector to equal both outputs. This is a direct scope-matched nonexistence proof for the frozen existential conjunction, independent of every positive replacement. The same binary family proves marginalization is noninjective, so no marginal section can also be faithful to every compatible full joint law.

The full proof is `evidence/natural-selector-no-go-proof.md`.

## Independently typed recovery boundaries

The three marginal-recovery predicates fail for different reasons and have separate proof paths.

* `RECOVERY-FULL-VFE-NOGO`: the product law and a positive correlated law have the same singleton marginals, while their KL values against the same positive product posterior are respectively zero and strictly positive.
* `RECOVERY-FULL-FISHER-NOGO`: the positive six-bit parity families with fixed \(\kappa=0\) and \(\kappa=1/2\) have the same singleton-marginal family map on \((0,1)^6\), while at the symmetric point their full-joint Fisher tensors are \(4I_6\) and \((65536/16383)I_6\).
* `RECOVERY-TYPED-INTERVENTION-NOGO`: conditional on the August 13 direct, latent, and null-extended BSC presentations being nonisomorphic objects in the declared typed category over one retained law, universal fiber uniqueness and two-sided recovery fail. A mere right-inverse section may still choose one conventional representative; the full causal/agency category remains open to formalization.

The proof, exact source dependencies, and strongest conditional replacements are in `evidence/recovery-factorization-no-go-proof.md`. None of the three claims depends on either of the other two.

## Strongest positive replacement

Given a declared finite reference \(p\), statistic \(T\), and target moment \(m\), a finite I-projection exists exactly when

\[
m\in\operatorname{conv}T(\operatorname{supp}p),
\]

and is then unique as a law relative to \((p,T,m)\). Its exact support is the inverse image in \(\operatorname{supp}p\) of the minimal face containing \(m\). After statistic minimalization it has a unique exponential multiplier; before minimalization, multipliers are unique only modulo affine redundancies. Every finite-KL feasible law satisfies the oriented identity

\[
D(q\|p)=D(q\|q_{p,m})+D(q_{p,m}\|p).
\]

The selected law is analytic on each fixed relative-interior face stratum. It is equivariant only when the reference and complete constraint diagram are transported coherently. For a positive reference and a full-support relative-interior singleton target, full-table higher-order log-linear interactions are inherited from \(p\); at a boundary target the statement is restricted to the minimal-face support and contrasts through zero atoms are undefined. A product reference yields the product law, whereas a feasible correlated reference selects itself.

For a deterministic coarse map \(f:X\to Y\), reference \(p\), and \(r\ll f_\#p\), the unique KL-minimizing completion relative to \((f,p,r)\) is

\[
L_f^p(r)(x)=
\begin{cases}
r(f(x))p(x)/(f_\#p)(f(x)),&(f_\#p)(f(x))>0,\\
0,&(f_\#p)(f(x))=0.
\end{cases}
\]

It composes strictly along nested deterministic coarse maps when every stage uses the pushed reference. With the retained posterior as reference and a feasible retained target \(m\in\operatorname{conv}T(\operatorname{supp}\pi)\), the finite optimizer satisfies \(q^*\ll\pi\), its deterministic completion is defined, and the retained optimizer and optimized VFE value descend under the August 13 retained-joint/conditioning equivalence. The retained envelope differential descends only for a positive \(C^1\) parameterized family with a common locally fixed feasible set and support stratum and a unique \(C^1\) optimizer. Presentation-specific auxiliary completions do not descend.

The full proof and boundary counterexamples are in `evidence/reference-relative-selection-proof.md`.

## Retained Fisher quotient and declared-block boundary

For every smooth retained-law map \(\rho:\Theta\to N\) and positive-semidefinite
target tensor \(g\), the pullback radical is exactly

\[
\operatorname{rad}(\rho^*g)=d\rho^{-1}(\operatorname{rad}g).
\]

It equals \(\ker d\rho\) if and only if
\(\operatorname{im}d\rho\cap\operatorname{rad}g=\{0\}\). Constant rank then
gives a smooth positive-definite vector-bundle quotient
\(T\Theta/\ker d\rho\cong\operatorname{im}d\rho\). A global quotient manifold
still requires a simple regular null foliation and basic tensors.

A familywise commuting presentation diagram
\(\rho_BF=J\rho_A\), with \(F\) a diffeomorphism (or the proved
surjective-submersion redundant-presentation variant) and \(J\) a Fisher
isometric immersion, transports the kernels and induces a quotient isometry.
Generic Markov contraction or equality at one parameter is insufficient.

For a declared smooth splitting \(T\Theta=\bigoplus_aB_a\), the following are
equivalent on a constant-rank stratum: the quotient block images form a direct
sum, their retained images form a direct sum, the kernel splits blockwise, and
each quotient tangent has a unique linear block decomposition. Additive Fisher
energy additionally requires pairwise Fisher orthogonality. Descent along
retained-law fibers requires the block images/projectors to be basic, and
presentation invariance additionally requires natural transport by a declared
type-preserving permutation. A rotating-block example proves that pointwise
smooth directness and orthogonality do not imply basicness.

At the uniform seven-outcome law, permutation naturality would make any
law/Fisher-only decomposition into three rank-two blocks define
\(S_7\to S_3\). Its restriction to the perfect group \(A_7\) is trivial, while
the six-dimensional sum-zero representation has scalar commutant and is
irreducible. Hence no such natural block decomposition exists without typing
or other symmetry-breaking data. Finally, the promoted parity family
\((\theta,\kappa)\mapsto Q_{\theta,\kappa}\) has full-joint rank seven
everywhere, whereas singleton retention has rank six and kernel exactly
\(\operatorname{span}\{\partial_\kappa\}\). Identifiability is therefore
relative to the declared retained map.

The direct proofs are in `evidence/fisher-quotient-agentization-proof.md`.

## Current scope

This stage proves the selector and recovery nonexistence results, the reference-relative replacements, and the retained Fisher quotient and law-only agentization boundary. The run's root claim ledger, dependency DAG, adversarial record, and terminal release remain for the package-assembly stage; this document does not by itself assign terminal certification state. No result here derives autonomous agents, intervention structure, continuum dynamics, physical geometry, or dimensional units from marginal sections or Fisher geometry.
