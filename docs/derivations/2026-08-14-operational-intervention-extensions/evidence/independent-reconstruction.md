<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-af08539e8868b09e5165943d91c488c6e06a00ac7a00b1d408ae22ddca6ee7e1","schema_version":"rigorous-theory-search/v1","target_digest":"af08539e8868b09e5165943d91c488c6e06a00ac7a00b1d408ae22ddca6ee7e1"} -->
# Independent reconstruction of the operational intervention extensions

## Reconstruction contract

This pass starts from the frozen definitions, quantifiers, admitted morphisms,
atomic claim statements, and dependency directions. It does not treat the
requested affirmative outcome, the numerical recomputation, or agreement by
other reviewers as a premise. The response system is `(A,Y,Phi)`, contextual
equivalence is

```text
a ~ b  iff  Phi(u a v)=Phi(u b v) for all u,v in A,
```

and every comparison retains the ordered external roles and uses one global
protocol-independent boundary-response map. The reconstruction covers
`target` and every dependency reachable from it.

## Algebraic quotient reconstruction

For `OIE-CONTEXTUAL-CONGRUENCE`, equality of every contextual response makes
`~` an equivalence relation. If `a~b`, associativity rewrites a context around
`xay` as a context around `a`, so `xay~xby`; therefore `~` is a two-sided
congruence. The identity context shows `~` lies in `ker(Phi)`. Conversely, if
any two-sided congruence `R` lies in `ker(Phi)` and `a R b`, then
`uav R ubv` for every context, hence `Phi(uav)=Phi(ubv)`. Thus `R` is
contained in `~`; no larger response-compatible congruence exists.

For `OIE-TERMINAL-QUOTIENT`, let `pi:A->A/~` be the canonical map and let
`(q,B,psi)` be response-compatible. Surjectivity and `Phi=psi q` imply
`ker(q)` is a congruence contained in `ker(Phi)`, hence in `~`. The formula

```text
h(q(a))=[a]
```

is therefore well-defined, unital, multiplicative, and surjective. It gives
`pi=h q` and `barPhi h=psi`. Any other factor with `pi=h q` has the same value
on every `q(a)` and is identical because `q` is surjective. The arrow is from
the finer quotient `B` to the coarser contextual quotient; reversing it is not
the proved universal property.

For `OIE-FINITE-MINIMALITY`, finite `A` makes every surjective image `B`
finite. The surjection `h:B->A/~` gives `|B|>=|A/~|`. Equality makes `h`
bijective and hence a monoid isomorphism. Comparing two minimum triples by
their factors through `A/~` gives a unique isomorphism commuting with their
raw quotient maps. This is a finite cardinality theorem over `A`; it does not
imply unique rigidity after forgetting the quotient map.

## Compact topological reconstruction

For `OIE-COMPACT-QUOTIENT`, choose a countable dense `D` in compact metrizable
`A` and form the signature

```text
S_D(a)=(Phi(uav))_(u,v in D).
```

It is continuous into the countable product of the metrizable Hausdorff
space `Y`. Equal full contextual responses imply equal signatures. Conversely,
sequential approximation of arbitrary `u,v` by points of `D`, joint
continuity of multiplication, and continuity of `Phi` turn equal signatures
into equal full contextual responses. Hence `ker(S_D)=~`. The quotient is
homeomorphic to the compact image `S_D(A)`, so it is compact metrizable.
Because `pi x pi` is a compact-to-Hausdorff continuous surjection, it is a
quotient map; the identity `mbar(pi x pi)=pi m` descends continuous
multiplication. The same quotient-map argument descends `barPhi`. For a
topological response-compatible triple, `h q=pi` and the assumed quotient-map
property of `q` make the algebraic factor continuous.

## Finite soft-kernel reconstruction

For `OIE-SOFT-MONOID`, each finite-state local-kernel palette is a compact
subset of a finite stochastic-kernel polytope. Adjoining an isolated bottom
symbol and taking a finite product remains compact metrizable. Coordinatewise
right override returns the last non-bottom entry; associativity and the unit
are immediate, while continuity follows by splitting on the clopen bottom
and non-bottom pieces. Replacing a normalized local kernel preserves the DAG
normalization: reverse topological summation successively removes normalized
terminal kernels. Every retained atom is a finite sum of finite products of
kernel evaluations, so the response is continuous in the declared evaluation
topology. The compact quotient result then applies.

For `OIE-BSC-SOFT-SEPARATION`, replacing the mediator of a binary chain by
`K_t(E=0|R=r)=t_r` gives

```text
P(O=0|R=r)=b+(1-2b)t_r.
```

With uniform `R`, direct summation of the two signed atom differences in each
row gives

```text
TV(Q_b(t),Q_b(t'))
  = |1-2b| (|t_0-t'_0|+|t_1-t'_1|)/2.
```

The square `[epsilon,1-epsilon]^2` therefore has diameter
`(1-2epsilon)|1-2b|`. For outgoing crossovers `1/3` and `1/4`, the diameters
are respectively `(1-2epsilon)/3` and `(1-2epsilon)/2`. The same formula on
the strictly interior constant-parent preparations `(s_-,s_-)` and
`(s_+,s_+)` gives `|1-2b|(s_+-s_-)`. A typed boundary bijection preserves
total variation, and the admitted protocol map preserves the marked mediator
face, so unequal diameters obstruct an admitted experiment isomorphism.

## Independent randomized reconstruction

For `OIE-RANDOMIZED-MONOID`, probability laws on a finite hard monoid compose
by the convolution law of independently sampled selectors. Finite
rearrangement proves associativity, the identity Dirac law is the unit, and
the unmarked response is the affine mixture of deterministic responses.
This construction does not encode a coupling between sequential selectors.

For `OIE-RANDOMIZED-RANK`, write `c_x` for the full deterministic two-sided
contextual vector of hard class `x`. Equal randomized contextual signatures
give

```text
sum_x (p(x)-q(x)) c_x = 0.
```

The displayed fifteen-by-fifteen minor in
`evidence/counterexample-proofs.md` uses all fifteen hard classes and fifteen
specified contextual atom coordinates. Substitution into fraction-free
Bareiss elimination, including the three recorded row swaps, yields

```text
det M(b,delta)=(2b-1)^6(2delta-1)^3/32.
```

The generic elimination is a polynomial identity, so possible zero pivots at
special parameter values do not restrict the identity. At `delta=5/12` the
values for `b=1/3` and `b=1/4` are `-1/5038848` and `-1/442368`, both nonzero.
Thus the contextual vectors are linearly independent and randomized
behavioral equivalence is literal equality.

For `OIE-HARD-NONISOMORPHISM`, use the fixed class order and the first four
response columns of the displayed minor. In `L_1`, `do(E=0)` has

```text
q_*=(1/3,1/6,1/3,1/6).
```

Under every typed binary flip of `R` and `O`, its orbit contains only `q_*`
and `(1/6,1/3,1/6,1/3)`. The complete `L_2` class table has only three
full-support responses:

```text
(7/24,5/24,5/24,7/24),
(3/8,1/8,3/8,1/8),
(1/8,3/8,1/8,3/8).
```

Every other response has a zero, a property preserved by boundary
permutation. The union of full-support atom values is
`{7/24,5/24,9/24,3/24}`, disjoint from the q-star orbit values
`{8/24,4/24}`. Thus no hard class
can receive the Dirac vertex while satisfying the same one global typed
boundary response map. This directly re-establishes
`OIE-HARD-NONISOMORPHISM` under the ordered `R`-to-`O` boundary.

For `OIE-RANDOMIZED-NONISOMORPHISM`, an affine bijection of finite simplices
maps extreme points to extreme points; its action is
`delta_x -> delta_theta(x)`. Convolution and unit preservation make `theta` a
unital hard-monoid isomorphism. The one global response intertwiner makes its
Dirac restriction response-compatible with exactly the ordered-boundary hard
experiment just reconstructed, which is impossible. This ancestor bridge,
not rank alone, supplies the final randomized contradiction.

## Measurable and Feller reconstruction

For `OIE-BOREL-RESPONSE`, finite topological-order recursion starts from the
unit law and extends it with each declared normalized kernel. Joint evaluation
measurability plus the monotone-class kernel-integration lemma makes every
bounded cylinder integral measurable in the protocol. Induction gives a
normalized joint kernel. Retained-set evaluations are measurable cylinder
operations and generate the declared evaluation sigma-algebra on retained
laws. This proves a Borel response for declared pointwise kernels, not for an
uncontrolled almost-sure conditional version. A separate broader
standard-Borel-monoid witness shows only that measurability by itself cannot
force quotient smoothness; it is not presented as a finite-DAG witness.

For `OIE-FELLER-QUOTIENT`, the finite-coordinate right-override monoid is
compact metrizable even when its palettes have infinite cardinality. To fill
the iterated-integration interface explicitly, a weakly continuous kernel on
compact spaces integrates every jointly continuous bounded integrand
continuously: finite sums `g(parameter)h(state)` are dense in the continuous
functions by Stone-Weierstrass, and uniform approximation passes through the
normalized kernels. Applying this lemma in reverse topological order shows
that every retained continuous test-function expectation depends continuously
on the protocol. Thus the response is weakly continuous, and the compact
contextual quotient theorem applies.

## Circle heat reconstruction

For `OIE-CIRCLE-PALETTE`, compact metrizability of the circle makes `P(T)`
compact metrizable in the weak topology. The constant-parent kernel
`K_nu(dE|r)=nu(dE)` is normalized, and for every continuous `f` its integral
is `int f dnu`, weakly continuous in `nu` and independent of `r`. Hence the
palette is jointly Feller. Arbitrary palette laws may be singular; smooth
positivity is used only for heat kernels and the strictness witness.

For `OIE-CIRCLE-BLACKWELL`, the semigroup law makes both ordered chains retain
`m(dR)H_(s+t)(R,dO)`. The identity `H_t=H_s H_(t-s)` gives a response-side
garbling from `H_s` to `H_t`. If a reverse Markov kernel `L` existed, set
`g=L e_1`. Markov contraction gives `|g|<=1`. The first Fourier coefficient
of `H_t g=H_s e_1` would be `g_hat(1)=exp(t-s)>1`, contradicting
`|g_hat(1)|<=int |g| dm<=1`. Thus the comparison is strict without assuming
equivariance of `L`.

For `OIE-CIRCLE-SOFT-INCLUSION`, semigroup factorization gives
`{nu H_t}` contained in `{nu H_s}`. Choose
`nu_rho=H_rho(x_0,dot)` with `0<rho<t-s`. If
`H_(rho+s)(x_0,dot)=nu H_t`, first-mode magnitudes would force
`|nu_hat(1)|=exp(t-s-rho)>1`, impossible for a probability law. The witness
is positive and smooth because `rho>0`; therefore the inclusion is proper.

## Closure result

Every dependency of `target` reconstructs from the frozen typed hypotheses.
The algebraic, topological, finite-kernel, randomized, measurable, Feller,
and circle interfaces agree at their dependency seams. The reconstruction
does not establish any excluded raw-realization, correlated-randomization,
null-version, noncompact, ELBO/VFE, agency, gauge/RG, or ontology extension.
The exact executable recomputation is useful transcription corroboration but
is not used to close any mathematical claim.
