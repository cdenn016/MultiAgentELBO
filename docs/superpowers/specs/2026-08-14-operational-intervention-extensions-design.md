# Operational Intervention Extensions Design

**Date:** 2026-08-14
**Status:** Approved by the user's autonomous-continuation instruction
**Repository baseline:** `53cafa374a668ea017a7c50ddbeb75e9045f73a8`
**Theory tier:** algebraic response monoids, finite soft/stochastic kernels, compact-Feller standard-Borel models

## Purpose

The released finite hard-intervention theorem proves that equal passive retained laws need not determine the reduced protocol-indexed response experiment. Its open boundary currently groups together four different questions: whether the behavioral quotient is minimal, whether the construction extends to soft or randomized protocols, whether it extends to continuous state spaces, and whether it canonically reconstructs a latent DAG. This design separates and resolves the first three as far as the present hypotheses allow while keeping the fourth open.

The central discipline is that an operational quotient is canonical only relative to fixed data: a protocol monoid, its retained-response map, its target/type coloring when that coloring is retained, and the admitted morphisms. No result below selects those data ontologically.

An admitted typed relabeling from `(A,Phi:Y)` to `(A',Phi':Y')` consists of invertible typed state maps `f_R,f_E,f_O` that preserve the ordered external roles, a protocol-monoid isomorphism `Theta:A->A'` induced by pushing every baseline and replacement kernel through those state maps, and one protocol-independent boundary-response isomorphism `U:Y->Y'` such that `Phi'(Theta(a))=U(Phi(a))` for every protocol `a`. In topological tiers these maps have the declared continuity, and in the circle tier the state maps also intertwine every heat kernel. A protocol-dependent response relabeling is not admitted.

## Layer 1: universal operational quotient

Fix a monoid `A`, a response set `Y`, and `Phi : A -> Y`. Define

```text
a equiv_Phi b iff Phi(u a v) = Phi(u b v) for every u,v in A.
```

This is the largest two-sided monoid congruence contained in `ker(Phi)`. Let `pi : A -> Syn(Phi)` be the quotient and let `barPhi([a])=Phi(a)`.

An algebraic response-compatible quotient triple is `(q,B,psi)`, where `q : A -> B` is a surjective unital monoid homomorphism, `psi : B -> Y` is a map, and `Phi=psi∘q`. Every such triple admits one unique surjective unital homomorphism `h : B -> Syn(Phi)` satisfying `pi=h∘q` and `barPhi∘h=psi`. Thus `Syn(Phi)` is terminal when arrows point from finer response-compatible quotients to coarser ones.

For finite `A`, `Syn(Phi)` has minimum cardinality. Equality of cardinalities makes `h` an isomorphism. Any two minimum-cardinality quotient triples are uniquely isomorphic **over `A`**, meaning the isomorphism commutes with both quotient maps and responses.

The phrase “unique up to unique isomorphism” must not be used after forgetting the quotient map from `A`. Bare response monoids can have response-preserving automorphisms. The result minimizes protocol classes only; it does not minimize nodes, edges, latent states, kernels, parameters, or computational cost.

## Layer 2: compact topological quotient

Let `A` be a compact metrizable monoid with jointly continuous multiplication, `Y` metrizable Hausdorff, and `Phi` continuous. Choose a countable dense `D` containing the identity and define

```text
S_D(a) = (Phi(u a v))_(u,v in D).
```

Continuity and density give `ker(S_D)=equiv_Phi`. The image `S_D(A)` is compact metrizable, and the canonical map `Syn(Phi) -> S_D(A)` is a homeomorphism. Quotient multiplication and the descended response are continuous. The quotient is independent of `D`; only the displayed coding depends on `D`, and its multiplication is induced by `S_D(ab)`, not coordinatewise multiplication.

A topological response-compatible quotient triple is an algebraic response-compatible quotient triple `(q,B,psi)` in which `B` is a topological monoid, both `q` and `psi` are continuous, and `q` is a quotient map. In the compact theorem, `B` is compact Hausdorff; a continuous surjection from compact `A` to Hausdorff `B` is automatically a quotient map, but the quotient-map condition remains explicit in the triple. The same terminal universal property then holds by a unique continuous surjection `B -> Syn(Phi)`.

## Layer 3: normalized local soft replacements

For a finite DAG presentation `P` on finite node state spaces, identify a local kernel with its finitely many stochastic coordinates and give every node `v` a palette `J_v` that is a compact subset of the corresponding finite-dimensional stochastic-kernel polytope, with its Euclidean (equivalently, evaluation-subspace) topology. Thus every kernel-coordinate evaluation is continuous. Require `J_v` to be stable under its declared typed relabelings, adjoin an isolated symbol `bottom_v` meaning “leave the baseline mechanism unchanged,” and form the componentwise right-override monoid

```text
M_P^J = product_v ({bottom_v} disjoint-union J_v).
```

Kernel replacement preserves DAG normalization and sequential composition. On finite state spaces every retained-law coordinate is a finite polynomial in the continuously evaluated kernel coordinates, so the response is continuous. Layer 2 therefore supplies a compact operational quotient and functorial transport under typed kernel isomorphisms.

The finite BSC pair from the hard certificate remains a counterexample when the reduced object retains the mediator-replacement face. Fix `0<epsilon<1/2`. For `L(a,b): R -> E -> O`, replace the mediator kernel by

```text
K_t(E=0 | R=r) = t_r,  t in [epsilon,1-epsilon]^2.
```

The retained conditional is `P(O=0|R=r)=b+(1-2b)t_r`. The total-variation diameter of this marked soft face is

```text
D_b(epsilon) = (1-2 epsilon) |1-2b|.
```

For `L_1=L(1/4,1/3)` and `L_2=L(1/3,1/4)`, passive crossover is `5/12`, but the diameters are `(1-2 epsilon)/3` and `(1-2 epsilon)/2`. Typed boundary relabelings preserve total variation. For every `epsilon<s_-<s_+<1-epsilon`, the parent-independent interior preparations `t=(s_-,s_-)` and `t'=(s_+,s_+)` have separation `|1-2b|(s_+-s_-)`, so no hard endpoint carries the result.

Preservation of the mediator target/type face and the ordered external boundary is load-bearing: `R` is the input/parameter boundary and `O` is the output/observation boundary. Admitted morphisms may not exchange `R` with `O` or reverse the chain orientation. A target-erasing or time-reversing reduced monoid is a different category.

## Layer 4: unmarked randomized protocols

Let `S_P` be the released finite hard reduced monoid and let `Rand(P)=Delta(S_P)`. Independently randomized sequential protocols compose by convolution, and the unobserved response is the affine mixture of deterministic responses.

For the released fifteen-class BSC models, the complete contextual-signature vectors are linearly independent. An exact fifteen-coordinate minor has

```text
det M(b,delta) = (2b-1)^6 (2delta-1)^3 / 32.
```

At `delta=5/12`, the determinants are `-1/5038848` and `-1/442368`. Therefore randomized behavioral equivalence is equality. Any response-compatible affine unital convolution-monoid isomorphism of the randomized simplices maps extreme points to extreme points and would restrict to the already-refuted hard reduced isomorphism. Equal passive laws therefore do not identify the unmarked independently randomized response experiment in this morphism category.

The old unmatched-response law is not the invariant after convexification: it is a mixture of two responses in the other model. In this four-atom retained-law witness, the four boundary point interventions are exactly the four vertices and hence span the full retained simplex. The proof uses the complete contextual signature, convolution, affine structure, and response compatibility. Correlated sequential randomization needs a joint selector/shared-noise object and is outside this theorem.

## Layer 5: standard-Borel and compact-Feller semantics

For a finite DAG of standard-Borel node spaces, declare standard-Borel replacement palettes, normalized measurable baseline kernels, and replacement kernels whose evaluation map `(theta,x_pa) -> K_v(theta,x_pa;A)` is jointly measurable for every measurable output set `A`. Equip the retained-law space `P(X_ret)` with its evaluation sigma-algebra. Finite topological-order Ionescu--Tulcea recursion produces one normalized joint law for every protocol and makes the retained response Borel. No regular conditional is inferred from observational data; the pointwise mechanisms are model data.

The set-valued operational quotient always exists algebraically. Standard Borelness alone does not certify a standard-Borel quotient because the contextual relation quantifies over an uncountable protocol set. A measurable quotient needs an explicit smooth classifier or stronger topology.

A sufficient positive tier takes compact Polish node spaces, compact metrizable replacement palettes `J_v`, one isolated `bottom_v` per node, and the finite-coordinate compact protocol monoid `A=product_v({bottom_v} disjoint-union J_v)` with coordinatewise right override. The node set is finite, but a palette and hence the monoid may have infinite cardinality. This multiplication is jointly continuous. If the baseline and replacement kernels are jointly Feller in state and palette parameter, the response into the weak law space is continuous, so Layer 2 yields a compact metrizable reduced experiment.

## Layer 6: smooth continuous nonidentifiability

Let `T` be the circle with normalized Haar measure and heat kernels `H_t`, where

```text
H_t e_n = exp(-n^2 t) e_n,  H_s H_t = H_(s+t).
```

For `0<s<t`, compare the chains

```text
P_1 = m(dR) H_s(R,dE) H_t(E,dO),
P_2 = m(dR) H_t(R,dE) H_s(E,dO).
```

To place the soft circle experiment inside the compact-Feller tier, take the mediator palette `J_E=P(T)` with the weak topology and use the constant-parent replacement kernel `K_nu(dE|R=r)=nu(dE)`. Since `T` is compact metrizable, `P(T)` is compact metrizable; for every continuous test function `f`, `(nu,r) -> integral f dnu` is continuous and independent of `r`, so this family is jointly Feller.

Their passive retained law is the same: `m(dR) H_(s+t)(R,dO)`. Their marked mediator experiments are `H_t` and `H_s`. Since `H_t=H_s H_(t-s)`, `H_s` Blackwell-dominates `H_t`. Reverse simulation is impossible: if `H_s=H_t L`, applying the first Fourier mode would require a Markov contraction to produce a Fourier coefficient of magnitude `exp(t-s)>1`. The comparison category fixes `R` as the input/parameter boundary, `O` as the output/observation boundary, and the mediator parameter experiment. Its typed relabelings use the single global intertwiner `U` and compatible protocol map `Theta` defined above, preserve the circle heat geometry, and may not exchange `R` with `O` or implement time reversal.

The result remains soft: arbitrary mediator preparation laws have response sets `{nu H_t}` and `{nu H_s}`, with the first strictly contained in the second. Strictness already has a positive smooth witness: fix `x_0` on the circle, choose `0<rho<t-s`, and use the preparation law `nu_rho=H_rho(x_0,dot)`, where `dot` denotes the measure argument. Then `nu_rho H_s=H_(rho+s)(x_0,dot)`, while representing that law as `nu H_t` would require a first Fourier coefficient of magnitude `exp(t-s-rho)>1`. Every kernel has a positive smooth density and is Feller. Retention of the ordered `R`-to-`O` boundary, mediator parameter experiment, and heat geometry is load-bearing.

## Analytic boundaries

- Observational regular conditionals are defined only almost surely. Point interventions at null conditioning values require declared pointwise mechanisms, dominated intervention laws, or continuous full-support versions.
- An uncountable family of Dirac interventions has no common sigma-finite dominating measure. Measure-level responses remain valid; a single ordinary density chart and finite VFE do not follow.
- Adaptive policies and shared-noise interventions require a controlled-process or joint-selector semantics; nodewise independent replacement is insufficient.
- Standard Borelness supplies no canonical topology. Feller continuity and compactness are additional structure.
- The target-colored theorem does not imply a target-erasing theorem.

## Canonicity and minimal realization boundary

Operational quotient minimality is established for one fixed `(A,Phi)` and, in colored variants, fixed target strata. Minimal latent/DAG/generative realization remains open. A future theorem must first declare a realization category, semantics functor, morphisms, complexity functional, reachability/observability conditions, treatment of null padding/state splitting/gauge labels, and a universal property in each semantics fiber. Minimum cardinality alone does not select a functorial raw realization.

## Deliverables

1. A new release-validated derivation package under `docs/derivations/2026-08-14-operational-intervention-extensions/`.
2. Direct proofs of the universal quotient, compact quotient, finite soft/randomized results, and circle heat-kernel theorem.
3. A standard-library exact recomputation artifact for the rational BSC identities, determinants, and convexification boundary; continuous Fourier checks remain corroborative, not proof.
4. Scoped integration into `Theory/05d_relational_inference.tex`, `Theory/SPEC.md`, `Theory/appendix_claim_ledger.tex`, `overview.md`, `docs/STATUS.md`, and the August 12 worklog.
5. Four independent algebra/category, probability/topology, adversarial-counterexample, and manuscript-scope views; a structured high-severity skeptic and adjudicator; rigorous-theory release validation; three-pass TeX build; schema-1.1 closure verification; and safe Git publication.

## Claim boundary

This phase may establish canonical minimization of protocol classes relative to fixed operational data, finite soft/randomized passive nonidentifiability under the declared morphisms, and compact-Feller continuous passive nonidentifiability with retained target structure. It may not identify protocols with agents, choose intervention targets or latent ontology canonically, recover every raw presentation, infer VFE/ELBO equality from response equality, or promote the result to continuum gauge/RG dynamics or physical ontology.
