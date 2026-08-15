<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-af08539e8868b09e5165943d91c488c6e06a00ac7a00b1d408ae22ddca6ee7e1","schema_version":"rigorous-theory-search/v1","target_digest":"af08539e8868b09e5165943d91c488c6e06a00ac7a00b1d408ae22ddca6ee7e1"} -->
# Adversarial attacks and dispositions

## A1. The universal-property arrow may be reversed

Attack: a familiar minimal automaton slogan might suggest a map from the
contextual quotient into every response-compatible quotient.

Response: `ker(q)` is contained in contextual equivalence, not conversely.
Therefore the well-defined map is `h(q(a))=[a]`, from the finer quotient `B`
onto the coarser contextual quotient. The identities `pi=h q` and
`barPhi h=psi` determine it uniquely. The reversed arrow would require the
opposite kernel inclusion, which is absent. Disposition: **REJECTED**.

## A2. The factor map may fail without the declared quotient-triple data

Attack: if `q` were not surjective or unital, or if `Phi` did not factor
through it, the terminal statement could be ill-typed or nonunique.

Response: these properties are explicit frozen hypotheses. Surjectivity makes
`h` unique and onto; unitality makes it a unital homomorphism; response
factorization puts `ker(q)` inside `ker(Phi)`. The theorem is not asserted
after deleting them. Disposition: **REJECTED** within scope.

## A3. Minimum objects may have nontrivial automorphisms

Attack: minimum cardinality might have been inflated to unique rigidity of a
bare response monoid.

Response: the four-element power-set union monoid with cardinality response
has contextual equivalence equal to identity but admits the nonidentity swap
of its two atoms. The theorem instead compares triples over the raw map from
`A`; commuting with `id_A` forces the identity. Disposition: **REJECTED** for
the frozen claim; bare-object rigidity is explicitly refuted.

## A4. Infinite cardinality may invalidate minimum cardinality

Attack: a surjection between infinite sets does not give a strict cardinality
test or make equal cardinality imply bijectivity.

Response: the largest-congruence and terminal-factor claims are arbitrary-
monoid results, while minimum cardinality and equality-implies-isomorphism are
restricted to finite `A`. The finite restriction is visible in the target and
atomic claim. Disposition: **REJECTED**.

## A5. Dense contextual signatures may miss nondense contexts

Attack: equality only on a countable dense context set need not imply equality
at every context.

Response: joint continuity of multiplication and continuity of `Phi` let
sequences from the dense set converge simultaneously to arbitrary left and
right contexts. The equality passes to the limit. Without continuity the
claim is not made; the nonsmooth Borel control demonstrates that boundary.
Disposition: **REJECTED**.

## A6. Quotient multiplication may not be continuous

Attack: an algebraic quotient of a topological monoid can carry a bad quotient
topology, and continuity of multiplication does not descend automatically.

Response: here the quotient is compact metrizable via the signature image.
The product map `pi x pi` is a continuous surjection from compact to Hausdorff,
therefore quotient, and `mbar(pi x pi)=pi m` descends continuity. Compared
topological triples also require `q` to be a quotient map. Disposition:
**REJECTED**.

## A7. Compact palettes alone may not make the response continuous

Attack: an abstract compact topology on a kernel palette could make evaluation
discontinuous.

Response: finite soft palettes are compact subsets of their finite-dimensional
stochastic-kernel polytopes with the Euclidean/evaluation-subspace topology.
Retained atom probabilities are finite polynomials in exactly those continuous
evaluations. The theorem does not use arbitrary compact kernel topologies.
Disposition: **REJECTED**.

## A8. Target erasure may destroy the BSC invariant

Attack: an arbitrary protocol permutation need not carry the mediator face to
itself, so unequal face diameters may not obstruct an uncolored isomorphism.

Response: correct; target erasure changes the comparison category. The frozen
category marks the mediator face and requires its pushforward under the typed
protocol map. In that category, one boundary bijection preserves total
variation and must preserve the unequal diameters. No target-erasing theorem
is claimed. Disposition: **REJECTED** as an in-scope attack and retained as a
scope boundary.

## A9. Convexification may erase the hard response-image obstruction

Attack: the old deterministic response absent from the second BSC model may
become an allowed mixture after randomization.

Response: it does: the recorded response is the mixture with weights `5/6`
and `1/6`, and boundary assignments span the four-atom simplex. The released
randomized proof does not reuse that invariant; it uses the full two-sided
contextual rank, convolution structure, and affine extreme points.
Disposition: **REJECTED** against the actual proof; the old proof strategy is
refuted.

## A10. The randomized determinant may be only executable evidence

Attack: a script reporting a nonzero determinant cannot prove the symbolic
formula or its side conditions.

Response: the proof artifact displays the complete selected matrix, the
fraction-free Bareiss recurrence, three row swaps, all successive pivots, and
the final factorization. The generic rational-function calculation implies a
polynomial identity at every specialization. Exact executable elimination is
only corroboration. Disposition: **REJECTED**.

## A11. Full rank alone may not rule out experiment isomorphism

Attack: trivial contextual equivalence in both experiments does not itself
show that no isomorphism exists between them.

Response: the proof separately uses the affine-simplex theorem: any admitted
affine bijection maps Dirac vertices to Dirac vertices. Convolution and unit
preservation turn the vertex permutation into a hard-monoid isomorphism; the
single global response intertwiner makes it a hard response-experiment
isomorphism. The hard obstruction is rechecked from the displayed response
columns: the boundary-flip orbit of
`(1/3,1/6,1/3,1/6)` is absent from every complete `L_2` hard response,
including all three full-support rows, while zero-containing rows remain
zero-containing under typed boundary flips. Therefore no such vertex
restriction exists under the ordered boundary and one global response map.
Disposition: **REJECTED**.

## A12. Marginal convolution may silently encode shared randomness

Attack: sequential selectors with equal marginals can have correlated noise,
so independent convolution may not describe them.

Response: a two-coordinate override witness gives three different composite
laws from identical selector marginals: independent bits, equal shared bits,
and complementary shared bits. The theorem explicitly concerns independent
selector sampling. Correlated selectors need a joint selector or coupling.
Disposition: **REJECTED** in scope; the correlated strengthening is refuted.

## A13. Observational conditionals may not define null-point interventions

Attack: standard-Borel disintegration gives conditional kernels only almost
surely, so a point intervention at a null parent value is version-dependent.

Response: the theorem begins with declared pointwise normalized kernels. The
two Bernoulli kernels differing only at `r=1/2` induce the same passive joint
law but opposite point-intervention responses, proving why observational
versions cannot substitute for declared mechanisms. Disposition: **REJECTED**.

## A14. The measurable contextual quotient may not be standard Borel

Attack: a Borel response on a standard-Borel protocol monoid does not ensure a
smooth contextual equivalence relation.

Response: on `{0,1}^N` under XOR, the finite-support indicator has contextual
equivalence equal to eventual equality `E_0`, which has no standard-Borel
classifier. This is a broader standard-Borel-monoid control, not a finite-DAG
right-override witness; it only blocks inferring smoothness from measurability
alone. The positive finite-DAG theorem asserts a Borel response and only an
algebraic quotient; standard-Borel quotient structure is not claimed without
a smooth classifier. Disposition: **REJECTED**.

## A15. Compactness may be dispensable

Attack: perhaps the compact quotient conclusion extends to noncompact
protocol monoids under the same remaining hypotheses.

Response: for `(R,+)` with identity response, contextual equivalence is
equality and the quotient is noncompact `R`. No unqualified noncompact compact-
quotient theorem is possible. Disposition: **REJECTED**.

## A16. Iterated Feller integration may omit a joint-integrand lemma

Attack: the local Feller property is usually stated for a test function of the
child alone, whereas reverse DAG integration produces jointly continuous
integrands involving parents and protocol parameters.

Response: on compact products, Stone-Weierstrass uniformly approximates a
jointly continuous integrand by finite sums of products of continuous
parameter/parent functions and continuous child functions. Weak continuity of
the kernel handles each product, and normalization passes uniform error
through integration. Induction therefore yields weak response continuity.
Disposition: **REJECTED**.

## A17. Reverse Blackwell garbling may exist without equivariance

Attack: excluding only translation-equivariant reverse garblings would not
prove strict Blackwell order against arbitrary Markov kernels.

Response: the proof assumes an arbitrary Markov kernel `L`. Markov contraction
gives `|L e_1|<=1`, while `H_s=H_t L` would force its first Fourier coefficient
to have magnitude `exp(t-s)>1`. No symmetry of `L` is used. Disposition:
**REJECTED**.

## A18. Strict soft inclusion may rely on a singular preparation

Attack: the proper-inclusion witness might lie on an inadmissible or singular
boundary of the palette.

Response: choose `nu_rho=H_rho(x_0,dot)` with `0<rho<t-s`. It has a positive
smooth density. Equality of its `H_s` response to any `nu H_t` would require
`|nu_hat(1)|>1`, impossible. The full palette permits singular measures, but
the strictness witness does not require one. Disposition: **REJECTED**.

## A19. Time reversal may identify the two chain presentations

Attack: BSC and heat kernels are reversible, and exchanging `R` with `O`
reverses one passive presentation into the other.

Response: this is an exact equality of reversed baseline path laws, not an
isomorphism of the frozen forward active experiments. The comparison category
fixes `R` as input/parameter, `O` as output/observation, mediator target,
protocol direction, and one global response map. Time reversal is expressly
outside it. Disposition: **REJECTED** as an in-scope attack.

## A20. Operational minimality may imply raw latent canonicity or ontology

Attack: the contextual quotient might uniquely recover the raw latent DAG,
or equality of response laws might identify the full generative ontology.

Response: adjoining an independent unretained node changes the raw DAG and
kernel presentation without changing any retained response, so the contextual
quotient forgets it. Raw realization requires a separate category, complexity
functional, reachability/observability conditions, and gauge controls. No
fixed-observation ELBO, latent-posterior, agency, gauge/RG, or ontology claim is
made. Disposition: **REJECTED**.

## A21. Numerical agreement may be carrying the theorem

Attack: the determinant values and Fourier margins may be trusted only because
the recomputation script returns the expected output.

Response: every target ancestor cites direct derivation evidence, supplemented
by the independent reconstruction. The executable artifacts close only a
separate finite corroboration claim. Removing them leaves the full mathematical
dependency closure intact. Disposition: **REJECTED**.

## Coverage conclusion

The attacks collectively cover `target` and every transitive dependency. Each
attack is rejected against the frozen claim or retained as an explicit control
against a stronger out-of-scope claim. No sustained attack remains against the
released conjunction.
