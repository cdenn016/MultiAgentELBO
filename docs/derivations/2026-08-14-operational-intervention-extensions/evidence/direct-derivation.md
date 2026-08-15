<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-af08539e8868b09e5165943d91c488c6e06a00ac7a00b1d408ae22ddca6ee7e1","schema_version":"rigorous-theory-search/v1","target_digest":"af08539e8868b09e5165943d91c488c6e06a00ac7a00b1d408ae22ddca6ee7e1"} -->
# Direct derivation of the operational intervention extensions

## 1. Frozen data and admitted maps

Write monoid multiplication by juxtaposition and its identity as `1`.  A
response system is a triple `(A,Y,Phi)` consisting of a monoid `A`, a set
`Y`, and a total map `Phi:A->Y`.  An **algebraic response-compatible quotient
triple** is `(q,B,psi)`, where `q:A->B` is a surjective unital monoid
homomorphism, `psi:B->Y` is a map, and

```text
Phi = psi o q.                                                   (1)
```

In a topological response-compatible triple, `A` and `B` are topological
monoids, `q` and `psi` are continuous, and `q` is a quotient map.  These
conditions, including the raw map `q`, are part of the object.

For the typed probability models below, an admitted relabeling is one global
quintuple

```text
(f_R,f_E,f_O,Theta,U).                                          (2)
```

The three `f` maps are invertible typed state maps and preserve the ordered
roles `R=input/parameter`, `E=mediator`, and `O=output/observation`.  Pushing
every baseline and replacement kernel through them induces the single
protocol-monoid isomorphism `Theta`.  The single protocol-independent
boundary-response isomorphism `U` obeys

```text
Phi'(Theta(a)) = U(Phi(a)) for every a in A.                    (3)
```

For ordinary retained laws, `U` is the pushforward induced by
`f_R x f_O`.  In topological tiers all maps have the stated continuity.  In
the circle tier the state maps also intertwine every heat kernel.  No map in
this category exchanges `R` with `O`, reverses the chain orientation, erases
the mediator face, or chooses a different response relabeling for different
protocols.

## 2. Algebraic contextual quotient

Define

```text
a ==_Phi b  iff  Phi(u a v)=Phi(u b v) for every u,v in A.       (4)
```

### Theorem 1 (largest response-compatible congruence)

For every response system `(A,Y,Phi)`, relation (4) is the largest two-sided
monoid congruence contained in `ker(Phi)`.

**Proof.** Equality in `Y`, evaluated at every pair of contexts, makes (4)
reflexive, symmetric, and transitive.  If `a ==_Phi b`, then for arbitrary
`x,y,u,v in A`, associativity gives

```text
Phi(u (x a y) v) = Phi((u x) a (y v))
                  = Phi((u x) b (y v))
                  = Phi(u (x b y) v).
```

Thus it is a two-sided congruence.  Taking `u=v=1` shows that it is contained
in `ker(Phi)`.

Conversely, let `~` be any two-sided congruence contained in `ker(Phi)`.  If
`a~b`, then `uav~ubv` for every `u,v`; containment in `ker(Phi)` gives the
equalities in (4).  Hence `~` is contained in `==_Phi`.  QED.

Let

```text
Syn(Phi)=A/==_Phi,  pi(a)=[a],  barPhi([a])=Phi(a).              (5)
```

Theorem 1 makes quotient multiplication well-defined, and the `u=v=1` case
makes `barPhi` well-defined.

### Theorem 2 (terminal finer-to-coarser factorization)

For every algebraic response-compatible quotient triple `(q,B,psi)`, there
is exactly one surjective unital homomorphism

```text
h:B->Syn(Phi)                                                    (6)
```

such that

```text
pi=h o q,             barPhi o h=psi.                           (7)
```

**Proof.** The kernel relation of `q` is a congruence.  If `q(a)=q(b)`, then
(1) gives `Phi(a)=Phi(b)`, so `ker(q)` lies in `ker(Phi)`.  Theorem 1 gives
`ker(q)` contained in `==_Phi`.  Therefore

```text
h(q(a))=[a]                                                      (8)
```

is well-defined.  Formula (8) proves directly that `h` is unital and
multiplicative, and surjectivity of `pi` proves surjectivity of `h`.  It also
proves the first identity in (7).  For `b=q(a)`, surjectivity of `q` and (1)
give

```text
barPhi(h(b))=barPhi([a])=Phi(a)=psi(q(a))=psi(b),
```

which is the second identity.  Finally, any map satisfying `pi=h o q` must
satisfy (8), and `q` is surjective, so it is unique.  QED.

Thus `Syn(Phi)` is terminal when arrows point from finer response-compatible
quotient triples to coarser ones.

### Corollary 2.1 (finite minimum cardinality, only over `A`)

If `A` is finite, then `Syn(Phi)` has minimum cardinality among algebraic
response-compatible quotient triples.  If such a triple `(q,B,psi)` has
`|B|=|Syn(Phi)|`, its factor `h` is an isomorphism.  Any two minimum triples
are uniquely isomorphic over `A` and compatibly with their responses.

**Proof.** Every `B` is finite because `q` is surjective, and Theorem 2 gives
a surjection `B->Syn(Phi)`, hence `|B|>=|Syn(Phi)|`.  Equality makes that
surjection bijective and therefore a unital monoid isomorphism.  If `h_i`
is the isomorphism from `(q_i,B_i,psi_i)` to `Syn(Phi)`, then

```text
F=h_2^{-1} o h_1:B_1->B_2                                      (9)
```

is the unique isomorphism satisfying `F o q_1=q_2` and
`psi_2 o F=psi_1`; uniqueness follows from surjectivity of `q_1`.  QED.

The finiteness hypothesis is used only for cardinality.  Theorems 1 and 2
hold for arbitrary monoids.  Corollary 2.1 minimizes protocol classes, not
latent nodes, DAG edges, states, kernels, parameters, or computational cost.
After forgetting `q`, a bare response monoid can have nontrivial
response-preserving automorphisms; `evidence/counterexample-proofs.md`
records an explicit four-element example.

## 3. Compact topological quotient

Assume now that `A` is a compact metrizable monoid with jointly continuous
multiplication, `Y` is metrizable Hausdorff, and `Phi` is continuous.  Choose
a countable dense subset `D` of `A` containing `1` and define

```text
S_D(a)=(Phi(u a v))_(u,v in D) in Y^(D x D).                    (10)
```

The countable product is metrizable and Hausdorff, and `S_D` is continuous
coordinate by coordinate.

### Theorem 3 (compact signature realization)

The kernel of `S_D` is `==_Phi`.  The quotient `Syn(Phi)` with the quotient
topology is compact metrizable, the canonical bijection

```text
Sbar_D:Syn(Phi)->S_D(A)                                         (11)
```

is a homeomorphism, and quotient multiplication and `barPhi` are continuous.
Only the coding (10), not the quotient, depends on `D`.

**Proof.** Contextual equivalence plainly implies equal signatures.  For the
converse, suppose `S_D(a)=S_D(b)`.  Given arbitrary `u,v in A`, choose
sequences `u_n,v_n in D` converging to them.  Joint continuity of
multiplication and continuity of `Phi` give

```text
Phi(u a v)=lim_n Phi(u_n a v_n)
          =lim_n Phi(u_n b v_n)=Phi(u b v).
```

Thus `ker(S_D)= ==_Phi`.

The quotient map `pi:A->Syn(Phi)` is continuous and `S_D=Sbar_D o pi`.
Because `pi` is a quotient map, `Sbar_D` is continuous; the kernel identity
makes it bijective.  Its domain is compact and `S_D(A)` is Hausdorff, so it
is a homeomorphism.  The image is a compact subspace of a metrizable space,
hence is compact metrizable.

Let `m` and `mbar` denote raw and quotient multiplication.  The map
`pi x pi:A x A->Syn(Phi) x Syn(Phi)` is a continuous surjection from a
compact space to a Hausdorff space, so it is a quotient map.  Since

```text
mbar o (pi x pi)=pi o m,                                        (12)
```

the quotient-map criterion proves that `mbar` is continuous.  Similarly,
`barPhi o pi=Phi` and the quotient property of `pi` prove continuity of
`barPhi`.  Multiplication on the signature image is the operation induced by
`S_D(ab)`; it is not coordinatewise multiplication in `Y^(D x D)`.  QED.

### Corollary 3.1 (continuous terminal property)

Let `(q,B,psi)` be a topological response-compatible quotient triple with
`B` compact Hausdorff.  The unique algebraic factor `h:B->Syn(Phi)` from
Theorem 2 is a continuous surjection.

**Proof.** The identity `h o q=pi` has continuous right-hand side.  Because
`q` is a quotient map, it implies continuity of `h`.  Surjectivity and
uniqueness are algebraic.  A continuous surjection from compact `A` to
Hausdorff `B` is automatically quotient, but the definition of the triple
keeps that condition explicit.  QED.

## 4. Finite normalized local-kernel replacement

Let a finite DAG have finite node state spaces `X_v`, normalized baseline
kernels `K_v^0`, and a topological order.  Identify a local kernel with the
finitely many numbers

```text
K_v(x_v | x_pa(v)).                                             (13)
```

The normalized kernels form a finite-dimensional stochastic-kernel
polytope.  For each node choose a compact palette `J_v` in that polytope with
its Euclidean, equivalently evaluation-subspace, topology.  Adjoin one
isolated symbol `bottom_v` and put

```text
A_J = product_v ({bottom_v} disjoint-union J_v).                 (14)
```

For `a in A_J`, use `K_v^0` when `a_v=bottom_v` and use `a_v` otherwise.
Define componentwise right override by

```text
(a star b)_v = b_v if b_v != bottom_v, else a_v.                 (15)
```

### Theorem 4 (compact normalized soft protocol monoid)

The space `A_J` is a compact metrizable topological monoid under (15).
Every protocol induces a normalized DAG law.  Every coordinate of every
retained marginal is continuous in `a`; hence the retained-law response is
continuous and Theorem 3 supplies a compact metrizable operational quotient.

**Proof.** At one node, right override chooses the first projection on the
clopen set where the second input is `bottom_v` and the second projection on
its clopen complement.  It is therefore continuous.  It is associative
because it returns the last non-bottom entry in a sequence, and `bottom_v`
is its identity.  A disjoint union of compact `J_v` with one isolated point
is compact metrizable, and the node set is finite, so (14) is compact
metrizable and (15) is jointly continuous.

For a protocol `a`, the joint mass function is

```text
p_a(x)=product_v K_v^a(x_v | x_pa(v)).                           (16)
```

Successively summing (16) in reverse topological order replaces each
normalized terminal conditional sum by `1`, proving total mass `1` and
nonnegativity.  A retained atom probability is a finite sum of finite
products of the coordinates (13).  Each evaluation coordinate is continuous
on `J_v`; at the isolated bottom point it takes the fixed baseline value and
is also continuous.  Thus every retained-law coordinate is a continuous
piecewise polynomial.  On a finite retained space, coordinate continuity is
exactly continuity of the probability-law response.  The compact quotient
theorem applies.  QED.

Sequential replacement semantics agrees with (15): the later protocol
replaces precisely its non-bottom coordinates.  Typed pushforward by the
maps in (2) preserves normalization, right override, and (3).  The BSC
mediator-face calculation and its unequal total-variation diameters are in
`evidence/counterexample-proofs.md`; target-face and ordered-boundary
preservation are essential hypotheses of that result.

## 5. Independently randomized protocols

Let `S` be a finite reduced hard-protocol monoid, with deterministic response
`phi:S->V` in the real vector space spanned by retained probability laws.
Put `Rand(S)=Delta(S)`.  For `p,q in Delta(S)`, define

```text
(p*q)(z)=sum_(xy=z) p(x)q(y),
Phi_R(p)=sum_x p(x)phi(x).                                      (17)
```

The first formula is the law of the product of independently drawn
selectors.  Finite rearrangement of sums proves associativity, and the Dirac
mass at the identity is the unit.  The second formula is affine and is the
unmarked response obtained after forgetting the selector.

For `x in S`, define its complete deterministic contextual vector

```text
c_x=(phi(u x v))_(u,v in S),                                   (18)
```

with every retained-law atom included as a scalar coordinate.

### Theorem 5 (full contextual rank and randomized rigidity)

If the vectors `{c_x:x in S}` are linearly independent, contextual
equivalence on `Delta(S)` is equality.  Moreover, every
response-compatible affine unital convolution-monoid isomorphism between two
such randomized experiments restricts on Dirac masses to a
response-compatible unital hard-monoid isomorphism.

**Proof.** If `p` and `q` have identical randomized responses in every
deterministic left and right context, affine expansion of (17) gives

```text
0=sum_x (p(x)-q(x)) c_x.                                        (19)
```

Linear independence forces every coefficient to vanish, so `p=q`.
Deterministic contexts suffice because they are admitted randomized
contexts; allowing further mixtures cannot weaken equality.

An affine bijection between finite simplices maps extreme points to extreme
points: if the image of an extreme point had a nontrivial convex
decomposition, applying the affine inverse would give such a decomposition
of the original point.  Thus an affine isomorphism `T` has

```text
T(delta_x)=delta_(theta(x))                                     (20)
```

for a bijection `theta`.  Preservation of convolution and the unit makes
`theta` a unital monoid isomorphism.  Applying the single response
intertwiner `U` from (3) to (20) proves hard response compatibility.  QED.

For the released fifteen-class BSC monoids, the explicit contextual minor in
`evidence/counterexample-proofs.md` has

```text
det M(b,delta)=(2b-1)^6(2delta-1)^3/32.                          (21)
```

At `delta=5/12` it is nonzero for both `b=1/3` and `b=1/4`.
Therefore Theorem 5 applies.  If the two randomized BSC experiments admitted
an affine response-compatible isomorphism, its restriction to their Dirac
vertices would be a hard response-compatible monoid isomorphism.  That
contradicts the released hard nonisomorphism.  Hence the randomized
experiments are nonisomorphic despite their equal passive law.  This argument
requires independent convolution, affinity, the unit, and the one global
response intertwiner.  A correlated or shared-noise selector needs a joint
selector object and is not covered.

## 6. Declared standard-Borel semantics

Let `v_1,...,v_n` be a topological ordering of a finite DAG.  Each node space
`X_v` and each replacement palette `J_v` is standard Borel.  Baseline and
replacement mechanisms are declared normalized kernels, and for every
Borel `C subset X_v` the evaluation

```text
(theta,x_pa(v)) -> K_v(theta,x_pa(v);C)                          (22)
```

is jointly measurable.  The bottom symbol selects the declared baseline;
it does not invoke a conditional inferred from a passive law.

### Theorem 6 (Borel protocol response)

Finite topological-order kernel recursion assigns every protocol one
normalized joint law, and the map from protocols to the retained law is
measurable when the law space carries its evaluation sigma-algebra.

**Proof.** Start with the unit mass on the empty product.  At step `k`, extend
the current parameterized measure by the kernel for `v_k`.  Joint
measurability in (22) and the standard monotone-class argument for kernel
integration show that the integral of every bounded measurable cylinder
function is measurable in the protocol.  Induction through the finite order
produces a normalized joint kernel.  Taking a retained-coordinate inverse
image is another measurable cylinder operation, so for every retained Borel
set `C`, the evaluation `a -> Phi(a)(C)` is measurable.  These evaluations
generate the declared sigma-algebra on the retained-law space.  QED.

This theorem parameterizes only the explicitly declared kernel families.
It does not endow the collection of all kernels with an implicit standard
Borel structure.  The algebraic quotient exists as a set, but standard
Borelness of the quotient does not follow: (4) quantifies over an uncountable
protocol space, and its equivalence relation need not be Borel or smooth.

## 7. Compact-Polish Feller tier

Assume in addition that all node spaces are compact Polish, each `J_v` is
compact metrizable, bottom is isolated, and the baseline and replacement
kernels are jointly Feller: integrating any continuous node function gives
a continuous function of the parent state and palette parameter.

### Theorem 7 (weakly continuous compact response)

The finite-coordinate monoid (14), which may have infinite cardinality, is
compact metrizable with jointly continuous multiplication.  Its response in
the weak topology on retained laws is continuous.  Consequently its
contextual quotient is compact metrizable with continuous multiplication and
response.

**Proof.** Compactness and multiplication were proved in Theorem 4 without
using finiteness of palette cardinality.  For response continuity, take a
continuous function `f` on the compact retained product and pull it back to
the full node product.  Integrate successively in reverse topological order.
The jointly Feller hypothesis and finite products preserve continuity at
each step, so

```text
a -> integral f dPhi(a)                                        (23)
```

is continuous for every continuous `f`.  This is exactly weak continuity of
the response on compact metrizable state spaces.  Theorem 3 applies.  QED.

No noncompact quotient theorem follows from this argument, and standard
Borelness alone supplies neither the topology nor the Feller property.

## 8. Circle heat-kernel theorem

Let `T=R/(2 pi Z)` with normalized Haar probability `m`.  Use the Markov
operator convention

```text
(H_r f)(x)=integral f(y) H_r(x,dy),
H_r e_n=exp(-n^2 r)e_n,
H_r H_q=H_(r+q).                                                (24)
```

For `r>0`, `H_r` has a strictly positive smooth density and is Feller.  Fix
`0<s<t` and define the ordered chains

```text
P_1=m(dR) H_s(R,dE) H_t(E,dO),
P_2=m(dR) H_t(R,dE) H_s(E,dO).                                 (25)
```

The comparison keeps `R` as input/parameter, `O` as output/observation, and
`E` as the marked mediator.

### Lemma 8.1 (the full soft palette is compact Feller)

Take `J_E=P(T)` with its weak topology and

```text
K_nu(dE | R=r)=nu(dE).                                         (26)
```

Then `J_E` is compact metrizable and the family (26) is jointly Feller.

**Proof.** Probability measures on a compact metrizable space form a compact
metrizable space in the weak topology.  For every continuous `f`,

```text
(nu,r) -> integral f dnu                                       (27)
```

is weakly continuous and independent of `r`.  This is joint Feller
continuity.  QED.

An arbitrary `nu` in this palette may be singular.  The statement is that
every `K_nu` is Feller; positive smooth density is asserted only for heat
kernels and for the heat preparation used below.

### Theorem 8 (same passive law, strict one-way Blackwell order)

The two chains in (25) have the same passive retained law,

```text
m(dR) H_(s+t)(R,dO).                                           (28)
```

As marked mediator-to-output experiments, `H_s` strictly
Blackwell-dominates `H_t`: `H_t=H_s H_(t-s)`, but there is no Markov kernel
`L`, equivariant or otherwise, satisfying `H_s=H_t L`.

**Proof.** Integrating out `E` and applying the semigroup identity in either
order gives (28).  The factorization `H_t=H_s H_(t-s)` is a Markov garbling,
so `H_s` dominates `H_t`.

For strictness, suppose an arbitrary Markov kernel `L` satisfied
`H_s=H_t L`.  Let `e_1(x)=exp(i x)` and set `g=L e_1`.  Positivity and
normalization of `L` imply `|g(x)|<=1`.  Taking the first Haar-Fourier
coefficient of

```text
H_t g=H_s e_1=exp(-s)e_1                                      (29)
```

and using self-adjoint Fourier diagonalization of `H_t` gives

```text
exp(-t) ghat(1)=exp(-s),  hence |ghat(1)|=exp(t-s)>1.            (30)
```

But `|ghat(1)|<=integral |g| dm<=1`, a contradiction.  No
translation-equivariance or other symmetry of `L` was assumed.  QED.

### Theorem 9 (strict soft response-set inclusion)

Let

```text
R_r={nu H_r:nu in P(T)}.                                       (31)
```

Then `R_t` is a proper subset of `R_s`.  For every fixed `x_0 in T` and
every `0<rho<t-s`, a positive smooth witness outside `R_t` is

```text
nu_rho H_s=H_(rho+s)(x_0,dot),
nu_rho=H_rho(x_0,dot).                                         (32)
```

**Proof.** Since `H_t=H_(t-s) H_s`, every

```text
nu H_t=(nu H_(t-s)) H_s
```

lies in `R_s`.  To prove strictness, suppose (32) equaled `nu H_t` for some
probability measure `nu`.  Comparing magnitudes of first Fourier
coefficients gives

```text
exp(-(rho+s))=|nuhat(1)| exp(-t),
|nuhat(1)|=exp(t-s-rho)>1,                                     (33)
```

contrary to `|nuhat(1)|<=1`.  Because `rho>0`, `nu_rho` and the response in
(32) have positive smooth heat densities.  QED.

Any admitted isomorphism in the frozen circle category uses the compatible
`Theta` and the same global `U` for all protocols, intertwines every heat
kernel, and preserves the ordered external roles.  Such an isomorphism would
preserve Blackwell equivalence and the soft response sets.  Theorems 8 and 9
therefore obstruct it.  A boundary exchange can explain the passive
factorization symmetry but is not an admitted active-experiment map.

## 9. Exact theorem boundary

The derivations establish a canonical operational quotient only relative to
the fixed `(A,Phi,Y)`, target/type strata, and morphism category.  They do not
select a protocol monoid, identify protocols with agents, or minimize a raw
latent/DAG realization.  They do not cover target-erasing soft morphisms,
correlated selectors, adaptive or shared-noise interventions, arbitrary
null-slice versions of observational conditionals, a noncompact quotient,
fixed-observation ELBO equality, autonomous agency, gauge or RG dynamics, or
physical ontology.  Exact computation in `evidence/recompute.py` corroborates
finite arithmetic and selected Fourier inequalities but is not a premise of
any theorem above.
