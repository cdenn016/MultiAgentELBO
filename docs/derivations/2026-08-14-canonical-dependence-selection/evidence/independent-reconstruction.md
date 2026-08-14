<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-8112f0083a554a4df3b5de3875174d0b0cbfeee36a7bc2ea20e78c8cf9da6b39","schema_version":"rigorous-theory-search/v1","target_digest":"8112f0083a554a4df3b5de3875174d0b0cbfeee36a7bc2ea20e78c8cf9da6b39"} -->
# Independent reconstruction from the frozen control plane

## Input discipline

This pass began with only problem-contract.json, claim-ledger.json, and
dependency-dag.json. It checked their shared schema, contract ID, and target
digest; copied the frozen target statement and quantifiers; and traversed each
edge in the declared depends-on direction. Only after the target closure and
all claim statements were listed were the evidence artifacts named by the
ledger opened. The root theorem narrative was not used as an input.

The graph has five nontrivial components:

1. **TARGET-ABSOLUTE-CANONICAL-SELECTOR** depends only on
   **SEL-CORRELATED-REFINEMENT-NOGO**.
2. **RECOVERY-TYPED-INTERVENTION-NOGO** depends on
   **RECOVERY-TYPED-INTERVENTION-CONDITIONAL-NOGO** as its strongest proved
   subclaim, which does not close the unformalized unconditional predicate.
3. **SEL-MAXIMAL-PRODUCT-CATEGORY** depends on
   **SEL-PRODUCT-UNIQUENESS**.
4. **SEL-PRESENTATION-DESCENT** depends on
   **SEL-REFERENCE-IPROJECTION** and
   **SEL-DETERMINISTIC-COMPLETION**.
5. **FISHER-DECLARED-BLOCK-ATTRIBUTION** depends on
   **FISHER-RETAINED-QUOTIENT**.

Every other claim is an independent root. No reference-relative positive
theorem is an ancestor of the negative target.

## Reconstruction of the target certificate

Let $U=Y=Z=\{0,1\}$, let $u=(1/2,1/2)$, and for
$\rho\in\{1/3,1/2\}$ define

$$
R_\rho(y,z\mid x)
=\mathbf 1[y=x]
\begin{cases}
(1+\rho)/2,&z=x,\\
(1-\rho)/2,&z\ne x.
\end{cases}
\tag{1}
$$

Every row in (1) is normalized and nonnegative. Its first output marginal is
the source law; its second is the source pushed through a binary symmetric
channel with crossover $(1-\rho)/2$. Hence each $R_\rho$ is an admitted
marginal-compatible split.

The section equation on the one-coordinate source forces $S_U(u)=u$. Both
descended marginal maps send $u$ to $(u,u)$, while direct pushforward gives

$$
R_{\rho\#}u=Q_\rho,\qquad
Q_\rho(y,z)=\frac{1+\rho(-1)^{y\oplus z}}4.
\tag{2}
$$

Naturality under both splits would require

$$
S_{(Y,Z)}(u,u)=Q_{1/3}=Q_{1/2}.
\tag{3}
$$

Their atom multisets are

$$
\left\{\frac13,\frac13,\frac16,\frac16\right\},
\qquad
\left\{\frac38,\frac38,\frac18,\frac18\right\}.
\tag{4}
$$

They are unequal. Outcome relabeling only permutes an atom multiset, and bit
flips can change the sign but not the absolute magnitude of $\rho$. Thus the
contradiction survives the frozen equivalence. No single-valued law-valued
section satisfies the two quantified naturality equations. Since the frozen
target asks existentially for one family satisfying this and every further
conjunct, (1)--(4) are a scope-matched nonexistence proof of the conjunction.
They use neither product uniqueness nor a positive replacement theorem.

The sole ancestor **SEL-CORRELATED-REFINEMENT-NOGO** is exactly the theorem
proved by (1)--(4). The target is therefore **REFUTED** and its sole ancestor
is **EVIDENCE_VERIFIED**.

## Selector classification and faithfulness

For **SEL-PRODUCT-UNIQUENESS**, take a singleton typed list of the same arity
as $X$. The preparation kernel from singleton coordinate $i$ to $X_i$ is the
requested marginal $\mu_i$. Independent tensoring prepares
$\bigotimes_i\mu_i$ jointly and $(\mu_i)_i$ marginally. Naturality and the
section equation force

$$
S_X((\mu_i)_i)=\bigotimes_i\mu_i.
\tag{5}
$$

Finite summation proves the converse for all local kernels. For
**SEL-MAXIMAL-PRODUCT-CATEGORY**, restriction to local kernels first gives
(5). Naturality under an added marginal-compatible kernel $K$ is then
equivalent to

$$
K_\#\!\left(\bigotimes_i\mu_i\right)
=\bigotimes_j(\bar K\mu)_j
\tag{6}
$$

for every marginal tuple. Necessity, sufficiency, identity, and composition
follow directly. This proves maximality relative to the frozen marginal
functor and local subcategory.

For **SEL-FAITHFUL-QUASI-INVERSE-NOGO**, (2) with $\rho=0$ and $\rho=1/2$
gives distinct joints in one marginal fiber. If $Sm$ were the identity on
every joint, applying it to their common marginal datum would make the
distinct laws equal. The binary fiber embeds into every list with two
nontrivial coordinates.

## Recovery dispositions

For **RECOVERY-FULL-VFE-NOGO**, use the uniform posterior $P=Q_0$ and
recognition laws $Q_0,Q_{1/2}$. Their displayed marginal inputs and evidence
$z>0$ agree, but

$$
-\log z+D(Q_0\Vert P)=-\log z,\qquad
-\log z+D(Q_{1/2}\Vert P)>-\log z.
\tag{7}
$$

The inequality is the exact finite KL zero criterion, not a decimal
comparison. One function of $(mQ,mP,z)$ cannot return both values.

For **RECOVERY-FULL-FISHER-NOGO**, the positive six-bit families

$$
Q^{(\kappa)}_\theta(x)
=P_\theta(x)+\kappa(-1)^{\sum_i x_i}
 \prod_i\theta_i(1-\theta_i)
\tag{8}
$$

have the same singleton-marginal family for every fixed $\kappa$. Direct score
summation at the center gives

$$
G^{(0)}=4I_6,\qquad
G^{(1/2)}=\frac{65536}{16383}I_6.
\tag{9}
$$

The tensors differ on the same parameter base although the complete singleton
family maps agree.

For **RECOVERY-TYPED-INTERVENTION-NOGO**, the complete ambient category,
object-admission rules, and internal nonisomorphism proof are absent.
Nothing in the contract or observational-law calculation supplies them, so
the frozen unconditional no-go reconstructs only to **INCONCLUSIVE**.

For **RECOVERY-TYPED-INTERVENTION-CONDITIONAL-NOGO**, if the direct, latent,
and null-extended BSC presentations are nonisomorphic objects over one
forgetful image in a declared typed category, universal
two-sided reconstruction $R$ would imply

$$
E_1\cong R(U(E_1))=R(U(E_2))\cong E_2,
\tag{10}
$$

contradicting nonisomorphism. This proves the conditional implication, not
the missing hypotheses. It does not prohibit a conventional right-inverse
choosing one representative per fiber. Formalizing the ambient causal
category and proving witness admission and nonisomorphism remain explicit
obligations for the unconditional claim.

## Reference-relative replacements

For **SEL-REFERENCE-IPROJECTION**, finite KL is finite exactly on laws
supported by $A=\operatorname{supp}p$. A finite feasible law exists exactly
when $m\in\operatorname{conv}T(A)$. Compactness gives attainment and strict
convexity gives uniqueness as a law. Exposing the minimal face forces feasible
finite-KL laws onto its inverse-image support; a one-sided entropy derivative
makes the optimizer positive at each point of that support. Minimal affine
coordinates make the log-partition covariance positive definite, yielding the
qualified exponential representation and the oriented identity

$$
D(q\Vert p)=D(q\Vert q_{p,m})+D(q_{p,m}\Vert p).
\tag{11}
$$

Analyticity is only on fixed relative-interior face strata, and equivariance
requires coherent transport of the reference and constraints.

For **SEL-DETERMINISTIC-COMPLETION**, deterministic $f:X\to Y$, reference
$p$, and $r\ll f_\#p$ give

$$
L_f^p(r)(x)
=r(f(x))\frac{p(x)}{(f_\#p)(f(x))}
\tag{12}
$$

on positive-reference fibers and zero otherwise. Fiber summation proves
normalization, conditional KL proves unique finite minimization as a law, and
cancellation proves strict nested composition when each stage uses the pushed
reference.

For **SEL-PRESENTATION-DESCENT**, the declared August 13 equivalence supplies
the same retained evidence and posterior. With the same feasible moment slice,
I-projection supplies the same retained optimizer and (12) minimizes each
presentation's auxiliary fiber. The retained optimizer and optimum descend;
the auxiliary law does not. The envelope differential additionally needs the
recorded positive C1 family, fixed feasible set/support stratum, and unique C1
optimizer.

## Fisher quotient and agentization boundaries

For **FISHER-RETAINED-QUOTIENT**, positivity of a semidefinite form implies
$g(u,u)=0$ exactly on its radical. For $h=\rho^*g$ this gives

$$
\operatorname{rad}h=(d\rho)^{-1}(\operatorname{rad}g),
\tag{13}
$$

with equality to $\ker d\rho$ exactly when the derivative image meets the
target radical trivially. The radical identity is pointwise. The proof's
constant-rank hypotheses are used only when quotient spaces must assemble into
a smooth vector bundle. A diffeomorphic Fisher-isometric commuting diagram
gives pointwise quotient isometries; on constant-rank strata they assemble
into a bundle isomorphism over the presentation diffeomorphism. In the
surjective-submersion variant, the bundle statement is $Q_A\cong F^*Q_B$,
not injectivity of total spaces. The rank-drop control $F(t)=t^2$ shows why a
commuting diagram alone is insufficient.

A global quotient manifold also needs a simple Hausdorff connected-leaf
space. For the pullback tensor itself, basicness along connected fibers is
automatic; projectability of separately declared blocks is not. A generic
Markov contraction also fails to supply the required isometry.

For **FISHER-DECLARED-BLOCK-ATTRIBUTION**, the isomorphism
$E/K\cong\operatorname{im}L$ proves equivalence of quotient directness, image
directness, blockwise kernel splitting, and unique quotient decomposition.
Energy additivity separately requires metric orthogonality. Block descent
separately requires projectable image distributions. Locally this is the
bracket condition
$[\Gamma(K),\Gamma(B_a+K)]\subseteq\Gamma(B_a+K)$; agreement across
disconnected components of one retained fiber is an additional global
condition. The rotating-block example violates the bracket test even though
its images are pointwise direct and orthogonal.

For **AGENT-LAW-ONLY-DECOMPOSITION-NOGO**, a natural unordered $2+2+2$ split
at the uniform seven-outcome law would give a homomorphism $S_7\to S_3$. Its
restriction to perfect $A_7$ is trivial. The sum-zero representation has
scalar commutant: every equivariant endomorphism extends by zero on the
invariant all-ones line, the resulting endomorphism of $\mathbb R^7$ has the
two-transitive commutant form, and its restriction is scalar. Hence the
sum-zero representation is irreducible, so three nonzero invariant two-planes
cannot exist. The conclusion concerns unlabeled law/Fisher data only.

For **PARITY-PROMOTED-RANK**, marginalizing a zero full derivative forces all
six $\theta$ components to vanish. The remaining derivative is
$b\chi(x)\prod_i\theta_i(1-\theta_i)$, forcing $b=0$ throughout the positive
open domain. The full rank is seven. Singleton retention has derivative
$(I_6\;0)$, rank six, and kernel
$\operatorname{span}\{\partial_\kappa\}$.

## Executable witness boundary

**SELECTION-WITNESS-REGRESSION** is a symbolic-check claim, not a theorem
dependency. The ledger separately binds the production source, frozen
test-contract snapshot, fresh GREEN JUnit, and TDD provenance record. Their
exact rational scope covers the finite laws, defects, and ranks named by the
claim; floating logarithmic output remains outside the exact classification.
The derivations, not those checks, carry the mathematical claims.

## Result

The target and all fifteen **EVIDENCE_VERIFIED** claims reconstruct at their
ledger scopes; the unconditional intervention claim reconstructs accurately
to **INCONCLUSIVE**. The target closure contains no open ancestor, the split
proof refutes the frozen existential conjunction, and the positive
replacements are logically separate. This reconstruction returns **PASS**. It is a
mathematical reconstruction record, not a claim that structural validation
proves the derivations.
