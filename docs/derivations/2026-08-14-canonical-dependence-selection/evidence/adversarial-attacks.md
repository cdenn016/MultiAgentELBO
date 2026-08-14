<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-8112f0083a554a4df3b5de3875174d0b0cbfeee36a7bc2ea20e78c8cf9da6b39","schema_version":"rigorous-theory-search/v1","target_digest":"8112f0083a554a4df3b5de3875174d0b0cbfeee36a7bc2ea20e78c8cf9da6b39"} -->
# Adversarial attack and defense record

Each disposition is against the claim exactly as released. Several attacks
defeat a tempting stronger statement; those attacks are rejected because the
stronger statement is expressly excluded, while the limitation remains
recorded.

## ATTACK-PREPARATION-OMITTED

**Affected claims:** **SEL-PRODUCT-UNIQUENESS** and
**SEL-MAXIMAL-PRODUCT-CATEGORY**.

**Attack.** Product selection may look canonical only because the proof
quietly imports arbitrary preparation kernels. With only typed bijections, a
nonzero-correlation binary rule can remain relabeling-equivariant.

**Response.** The frozen local class contains every coordinatewise finite
Markov kernel, including $P_i(x_i\mid *)=\mu_i(x_i)$. Naturality from the
singleton list computes $S_X(\mu)=\bigotimes_i\mu_i$. The corrected
bijection-only control is
$S^\varepsilon(a,b)=p_a\otimes p_b+\delta(a,b)H$, with
$H=[[1,-1],[-1,1]]$ and
$\delta=\varepsilon a(1-a)b(1-b)(2a-1)(2b-1)$ for
$0<\varepsilon<1$. The zero row and column sums of $H$ preserve
normalization and marginals; the atomwise bound
$|\delta|\le\varepsilon p_a(x)p_b(y)$ proves nonnegativity. Flipping either
bit changes the signs of both $\delta$ and the pushed $H$, so the family is
equivariant under every coordinatewise bit bijection and is nonproduct when
$\delta\ne0$. The maximal-category theorem is explicitly relative to the

**Disposition:** **REJECTED**. Falsification would require an admitted
preparation for which the naturality calculation fails.

## ATTACK-RELABELING-QUOTIENT

**Affected claims:** **TARGET-ABSOLUTE-CANONICAL-SELECTOR** and
**SEL-CORRELATED-REFINEMENT-NOGO**.

**Attack.** Perhaps $Q_{1/3}$ and $Q_{1/2}$ are one law after an allowed
relabeling.

**Response.** Relabeling only permutes atom probabilities. The exact multisets

$$
\{1/3,1/3,1/6,1/6\},
\qquad
\{3/8,3/8,1/8,1/8\}
$$

are unequal. Bit flips can change $\rho$ to $-\rho$ but cannot change its
absolute magnitude from $1/3$ to $1/2$.

**Disposition:** **REJECTED**. Falsification would require an admitted
relabeling that maps one multiset to the other.

## ATTACK-SET-VALUED-SELECTOR

**Affected claims:** **TARGET-ABSOLUTE-CANONICAL-SELECTOR**,
**SEL-CORRELATED-REFINEMENT-NOGO**, and
**SEL-FAITHFUL-QUASI-INVERSE-NOGO**.

**Attack.** Return the whole marginal fiber
$\mu\mapsto\{Q:mQ=\mu\}$, which contains both split outputs and every joint.

**Response.** This is set-valued and changes the frozen codomain from one law.
It supplies no selected scalar, family, or enriched object. Within the frozen
signature, noninjectivity still blocks a two-sided inverse.

**Disposition:** **REJECTED**. A set-valued problem is a different target.

## ATTACK-VFE-COLLAPSE

**Affected claim:** **RECOVERY-FULL-VFE-NOGO**.

**Attack.** Conditional KL identities may collapse auxiliaries, perhaps making
the full VFE a function of singleton marginals.

**Response.** Uniform $Q_0=P$ and correlated $Q_{1/2}$ give one identical
input $(mQ,mP,z)$ but unequal exact KL values. Conditional collapse needs a
complete retained joint posterior and conditional reference, which are richer
inputs than the frozen signature.

**Disposition:** **REJECTED**. One function cannot return two unequal values
at one input.

## ATTACK-SINGULAR-FISHER-TARGET

**Affected claims:** **RECOVERY-FULL-FISHER-NOGO** and
**FISHER-RETAINED-QUOTIENT**.

**Attack.** A singular target tensor invalidates an unqualified identity
$\operatorname{rad}(\rho^*g)=\ker d\rho$, and boundary scores may be undefined.

**Response.** The released identity is

$$
\operatorname{rad}(\rho^*g)
=(d\rho)^{-1}(\operatorname{rad}g),
$$

with an exact transversality condition for equality to the kernel. The
categorical recovery witness is strictly positive. Degenerate and boundary
controls are retained rather than generalized away.

**Disposition:** **REJECTED**. The attack refutes an excluded unqualified
identity.

## ATTACK-IPROJECTION-SUPPORT-ZERO

**Affected claim:** **SEL-REFERENCE-IPROJECTION**.

**Attack.** With $p=\delta_0$, $T(x)=x$, and target $m=1$, the only feasible
law has infinite KL, so the reference selector fails.

**Response.** Here $m\notin\operatorname{conv}T(\operatorname{supp}p)$. The
theorem predicts no finite minimizer and asserts existence exactly inside that
support convex hull. Its smoothness claim is also restricted to a fixed
relative-interior face stratum.

**Disposition:** **REJECTED**. The example verifies a necessary hypothesis.

## ATTACK-STOCHASTIC-COARSE-CHANNEL

**Affected claims:** **SEL-DETERMINISTIC-COMPLETION** and
**SEL-PRESENTATION-DESCENT**.

**Attack.** A stochastic channel that outputs a fair bit independently of its
input has no right inverse for nonfair targets.

**Response.** The completion theorem is explicitly deterministic, requires
target absolute continuity, and composes with pushed references. The
stochastic example blocks an unasserted extension. Retained descent uses
deterministic forgetting of auxiliary variables.

**Disposition:** **REJECTED**. A stochastic analogue needs a separate
joint-kernel theorem.

## ATTACK-PRESENTATION-RANK-DROP

**Affected claim:** **FISHER-RETAINED-QUOTIENT**.

**Attack.** A commuting presentation diagram may cross a rank drop, so it
cannot by itself yield either a pointwise quotient isomorphism or a smooth
quotient-bundle isomorphism.

**Response.** The released theorem requires a presentation diffeomorphism or
surjective submersion for its pointwise statement and constant-rank strata for
the bundle statement. In the redundant-presentation case, the correct bundle
object is $Q_A\cong F^*Q_B$. The control $F(t)=t^2$ is not a submersion at
zero and has unequal quotient dimensions there, so it confirms rather than
refutes the qualifications.

**Disposition:** **REJECTED**. The attack defeats only a commuting-diagram
overclaim that the corrected theorem does not make.

## ATTACK-NONBASIC-NODE-BLOCKS

**Affected claims:** **FISHER-DECLARED-BLOCK-ATTRIBUTION** and
**FISHER-RETAINED-QUOTIENT**.

**Attack.** Smooth pointwise direct and orthogonal blocks may rotate along one
retained-law fiber and therefore fail to descend.

**Response.** The rotating example is contained in the proof. It is why block
descent separately requires basic image subbundles/projectors. Pointwise
directness and energy orthogonality are not claimed to imply projectability.
For the pullback metric itself, basicness is automatic in the stated
submersion setting; the failure concerns separately declared blocks.

**Disposition:** **REJECTED**. The attack validates a stated boundary.

## ATTACK-INTERVENTION-OVERREACH

**Affected claims:** **RECOVERY-TYPED-INTERVENTION-NOGO**,
**RECOVERY-TYPED-INTERVENTION-CONDITIONAL-NOGO**,
**SEL-PRESENTATION-DESCENT**, and
**AGENT-LAW-ONLY-DECOMPOSITION-NOGO**.

**Attack.** Observational equality cannot formalize a causal category, prove
nonisomorphic intervention objects, or yield autonomous agency.

**Response.** The frozen unconditional **RECOVERY-TYPED-INTERVENTION-NOGO**
is **INCONCLUSIVE** because the ambient category and internal witness
nonisomorphism are unformalized. The separate
**RECOVERY-TYPED-INTERVENTION-CONDITIONAL-NOGO** theorem applies only after
those typed hypotheses are supplied and leaves a conventional right-inverse
possible. Retained descent is variational at retained-law scope. The law-only
block theorem makes no autonomous-agency identification.

**Disposition:** **REJECTED**. The overclaim is absent. Formalizing the
ambient causal category remains open outside the negative selector closure.

## ATTACK-A7-REPRESENTATION-SCOPE

**Affected claim:** **AGENT-LAW-ONLY-DECOMPOSITION-NOGO**.

**Attack.** A declared typing or partition-preserving subgroup can produce
three two-dimensional blocks.

**Response.** The theorem concerns only unlabeled law/Fisher data natural
under every $S_7$ relabeling. Added typing is valid symmetry-breaking input
and lies outside the no-go.

**Disposition:** **REJECTED**. A typed decomposition is not a counterexample
to the law-only statement.

## ATTACK-PARITY-POINTWISE-RANK

**Affected claim:** **PARITY-PROMOTED-RANK**.

**Attack.** One exact matrix rank at the symmetric parameter cannot prove rank
seven on the whole positive domain.

**Response.** The global proof does not infer from that check. Marginalizing a
hypothetical zero derivative eliminates all six marginal tangent components;
positivity of the remaining interaction derivative eliminates the seventh.
The matrix check is corroborative only.

**Disposition:** **REJECTED**. Falsification needs a nonzero full derivative
kernel tangent at an interior point.

## ATTACK-SYMBOLIC-CHECK-AS-PROOF

**Affected claim:** **SELECTION-WITNESS-REGRESSION**.

**Attack.** Passing exact tests does not prove a global mathematical theorem.

**Response.** The released claim is only a bound symbolic regression
observation. No mathematical theorem depends on it; mathematical claims point
to contained derivations.

**Disposition:** **REJECTED**. The attack would be sustained only if a theorem
used the regression as closing mathematical evidence.

## Overall disposition

The thirteen attacks cover all seventeen ledger claims, including the target and its
full dependency closure. Each is rejected against the exact released scope.
No attack is resolved by agent agreement or numerical agreement; each response
uses a contained derivation or an explicit scope boundary.
