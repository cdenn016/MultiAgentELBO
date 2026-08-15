<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-efe715cba81c2000403811015e6cecb599f4023133543b5cb0ae77288bccc874","schema_version":"rigorous-theory-search/v1","target_digest":"efe715cba81c2000403811015e6cecb599f4023133543b5cb0ae77288bccc874"} -->
# Operational reduction and finite nonidentifiability

## Scope

This is a direct derivation in the frozen finite binary-symmetric-channel
(BSC) subcategory. A context is a partial hard assignment, responses are
complete retained `(R,O)` joint laws, and the only admitted boundary
relabelings are the independent binary state flips of `R` and `O`. Exact
execution corroborates the displayed arithmetic but is not a premise.

## 1. The intervention monoid and its quotient

For a presentation `P`, let `A_P` be all partial sections `i` with
`i(v) in X_v` on an arbitrary subset of nodes. Define right override by

```text
(i star j)(v) = j(v), if j assigns v;
                i(v), if j does not assign v but i does;
                undefined, otherwise.                            (1)
```

**Lemma 1 (right-override monoid).** `(A_P,star,empty)` is a monoid.

**Proof.** The empty context is plainly a left and right identity. At a fixed
node, each of `(i star j) star k` and `i star (j star k)` returns the value in
the last context among `i,j,k` that assigns that node, or remains undefined if
none does. The two partial sections therefore agree pointwise. QED.

Let `Phi_P(i)` be the complete retained response to `i`, and define

```text
i ==_P j
iff Phi_P(u star i star v) = Phi_P(u star j star v)
    for every u,v in A_P.                                       (2)
```

**Lemma 2 (behavioral equivalence and two-sided congruence).** Relation (2) is
an equivalence relation and satisfies

```text
i ==_P j  =>  a star i star b ==_P a star j star b               (3)
```

for all `a,b in A_P`.

**Proof.** Reflexivity, symmetry, and transitivity follow pointwise from
equality of the complete signature indexed by `(u,v)`. If `i ==_P j`, then for
arbitrary `u,v`, associativity gives

```text
Phi_P(u star (a star i star b) star v)
 = Phi_P((u star a) star i star (b star v))
 = Phi_P((u star a) star j star (b star v))
 = Phi_P(u star (a star j star b) star v).
```

This is (3). QED.

It follows that

```text
Abar_P := A_P / ==_P,
[i][j] := [i star j],
[empty] := the identity class                                  (4)
```

is a well-defined monoid. Moreover,

```text
barPhi_P([i]) := Phi_P(i)                                       (5)
```

is well-defined: set `u=v=empty` in (2). Thus operational reduction keeps the
entire contextual multiplication and retained response map while discarding
only distinctions invisible in every two-sided context.

## 2. Shared-boundary direct, split, and null controls

For `e in [0,1]`, the BSC kernel is

```text
C_e(y|x) = 1-e if y=x, and e otherwise.
```

Direct summation over the intermediate bit proves

```text
sum_z C_b(o|z) C_a(z|r) = C_delta(o|r),
delta = a+b-2ab.                                                 (6)
```

Take `a=1/10`, `b=1/8`; then `delta=1/5`. For every partial boundary
assignment `c` on `{R,O}`, the direct presentation `R->O`, the split chain
`R->E->O`, and the split chain extended by an independent null node `N` have
the same retained response. Equation (6) proves the empty and `R`-only cases;
a hard assignment to `O` replaces the final channel in all three models; and
summing the normalized independent `N` factor gives one. These cases exhaust
the nine boundary contexts. Their exact laws, ordered by
`(R,O)=(0,0),(0,1),(1,0),(1,1)`, are:

| Context | Common retained law |
| --- | --- |
| `empty` | `(2/5,1/10,1/10,2/5)` |
| `do(R=0)` | `(4/5,1/5,0,0)` |
| `do(R=1)` | `(0,0,1/5,4/5)` |
| `do(O=0)` | `(1/2,0,1/2,0)` |
| `do(O=1)` | `(0,1/2,0,1/2)` |
| `do(R=0,O=0)` | `(1,0,0,0)` |
| `do(R=0,O=1)` | `(0,1,0,0)` |
| `do(R=1,O=0)` | `(0,0,1,0)` |
| `do(R=1,O=1)` | `(0,0,0,1)` |

This equality is a shared-boundary control, not an assertion that the raw or
fully reduced presentations are isomorphic. In particular, the split model
admits mediator interventions that the direct presentation does not.

## 3. Independent-null collapse

Let `S` be the split chain on `{R,E,O}` and `S^N` its extension by an isolated
binary node `N` with `P(N=1)=eta`; the frozen control uses `eta=2/5`. Let

```text
pi : A_(S^N) -> A_S
```

forget the assignment to `N`. It is a surjective monoid homomorphism because
forgetting a coordinate commutes pointwise with right override.

For any context `c` on `{R,E,O}` and either `n in {0,1}`, the intervened full
law factors as

```text
p_((S^N)^(do(N=n) star c))(r,e,N,o)
  = p_(S^c)(r,e,o) delta_n(N).                                  (7)
```

Summing (7) over `N` proves

```text
Phi_(S^N)(do(N=n) star c) = Phi_S(c).                            (8)
```

The context set on `{R,E,O}` is `{unassigned,0,1}^3`, so (8) covers exactly
both null assignments and all `3^3=27` retained/mediator/record contexts,
with no omitted case. If `N` is unassigned, the same proof replaces the Dirac
factor by `((1-eta),eta)`, whose sum is also one. Consequently, for every full
null-model context `i`,

```text
Phi_(S^N)(i) = Phi_S(pi(i)).                                     (9)
```

**Lemma 3 (exact quotient equivalence under forgetting `N`).** For all
`i,j in A_(S^N)`,

```text
i ==_(S^N) j  iff  pi(i) ==_S pi(j).                             (10)
```

**Proof.** If the right side holds, then for arbitrary `u,v in A_(S^N)`, use
(9) and the homomorphism property:

```text
Phi_(S^N)(u star i star v)
 = Phi_S(pi(u) star pi(i) star pi(v))
 = Phi_S(pi(u) star pi(j) star pi(v))
 = Phi_(S^N)(u star j star v).
```

Conversely, every pair of split contexts has a lift with `N` unassigned.
Apply null-model equivalence to those lifts and then (9). QED.

Therefore

```text
barpi : Abar_(S^N) -> Abar_S,   barpi([i])=[pi(i)]               (11)
```

is well-defined, surjective, and injective by (10). It is a monoid
homomorphism, preserves the identity, and preserves every response by (9).
It is therefore an isomorphism of reduced intervention experiments. In
particular, `empty`, `do(N=0)`, and `do(N=1)` have identical complete
two-sided signatures and occupy the same reduced class. Null-node inventory
cannot carry the negative certificate below.

## 4. The same-passive-signature pair

Let `L(a,b)` be the binary chain `R->E->O` with `R~Bernoulli(1/2)`, channel
`C_a` on `R->E`, and channel `C_b` on `E->O`. Define

```text
L_1 = L(1/4,1/3),
L_2 = L(1/3,1/4).                                                 (12)
```

Both are admitted objects. They have exactly the same node roles, binary
cardinalities, edges `R->E->O`, and mediator intervention target `E`; only the
two channel parameters differ.

By (6), the passive crossover in both cases is

```text
delta(1/4,1/3) = 1/4+1/3-2(1/4)(1/3) = 5/12,
delta(1/3,1/4) = 5/12.                                          (13)
```

For a uniform input, a BSC of crossover `delta` has retained joint law

```text
((1-delta)/2, delta/2, delta/2, (1-delta)/2).
```

Thus

```text
Phi_(L_1)(empty) = Phi_(L_2)(empty)
 = (7/24,5/24,5/24,7/24).                                      (14)
```

This is equality of the complete passive object, stronger than equality only
up to a boundary relabeling.

## 5. Direct derivation of the fifteen behavioral classes

Write `c(r,e,o)` for the context that assigns precisely the entries not equal
to `-`, in node order `R,E,O`, where each symbol lies in `D={-,0,1}`. There
are `27` raw contexts.

If `o` is `0` or `1`, then the three contexts

```text
{ c(r,e,o) : e in D }                                           (15)
```

are behaviorally equivalent for fixed `r,o`. Indeed, after arbitrary left
and right composition, `O` remains hard assigned: the central assignment
overrides any left `O`, and a right `O` can only replace it by another hard
assignment. The value of the central `E` assignment can therefore affect no
retained variable, and summing over unretained `E` gives one. This yields six
classes of size three.

If `O` is unassigned, each `c(r,e,-)` is a singleton class. The following
exact identity responses show both that the nine singletons are distinct and
that no two of the fifteen displayed classes merge. Entries with different
support are unequal; within a common support, the shown positive rational
atoms are unequal. Hence equality already fails at `u=v=empty`, which is a
necessary component of (2).

| ID | Least representative | Class membership | `L_1` response | `L_2` response |
| ---: | --- | --- | --- | --- |
| 0 | `c(-,-,-)` | singleton | `(7/24,5/24,5/24,7/24)` | same |
| 1 | `c(-,-,0)` | (15), `r=-,o=0` | `(1/2,0,1/2,0)` | same |
| 2 | `c(-,-,1)` | (15), `r=-,o=1` | `(0,1/2,0,1/2)` | same |
| 3 | `c(-,0,-)` | singleton | `(1/3,1/6,1/3,1/6)` | `(3/8,1/8,3/8,1/8)` |
| 4 | `c(-,1,-)` | singleton | `(1/6,1/3,1/6,1/3)` | `(1/8,3/8,1/8,3/8)` |
| 5 | `c(0,-,-)` | singleton | `(7/12,5/12,0,0)` | same |
| 6 | `c(0,-,0)` | (15), `r=0,o=0` | `(1,0,0,0)` | same |
| 7 | `c(0,-,1)` | (15), `r=0,o=1` | `(0,1,0,0)` | same |
| 8 | `c(0,0,-)` | singleton | `(2/3,1/3,0,0)` | `(3/4,1/4,0,0)` |
| 9 | `c(0,1,-)` | singleton | `(1/3,2/3,0,0)` | `(1/4,3/4,0,0)` |
| 10 | `c(1,-,-)` | singleton | `(0,0,5/12,7/12)` | same |
| 11 | `c(1,-,0)` | (15), `r=1,o=0` | `(0,0,1,0)` | same |
| 12 | `c(1,-,1)` | (15), `r=1,o=1` | `(0,0,0,1)` | same |
| 13 | `c(1,0,-)` | singleton | `(0,0,2/3,1/3)` | `(0,0,3/4,1/4)` |
| 14 | `c(1,1,-)` | singleton | `(0,0,1/3,2/3)` | `(0,0,1/4,3/4)` |

For completeness, each row follows directly from

```text
P^c(r,o)
 = q_R^c(r) sum_e q_E^c(e|r) q_O^c(o|e),                        (16)
```

where an assigned factor is its indicated Dirac mass. With neither `E` nor
`O` assigned, (16) uses `delta=5/12`; with `E=e` assigned and `O` unassigned,
it uses `(C_b(0|e),C_b(1|e))`; with `O` assigned, it is independent of `E`.
These are exactly the entries in the table. The class-size vector is therefore

```text
(1,3,3,1,1,1,3,3,1,1,1,3,3,1,1),
```

whose sum is `27`. This proves the class enumeration and does not appeal to
the executable enumeration.

## 6. Complete response-image obstruction under all boundary relabelings

Let

```text
q_* := Phi_(L_1)(do(E=0)) = (1/3,1/6,1/3,1/6).                  (17)
```

A typed binary boundary relabeling is a pair of flips
`(s_R,s_O) in {0,1}^2`, acting by permutation of atoms:

```text
(T_(s_R,s_O)q)(r,o) = q(r xor s_R, o xor s_O).                  (18)
```

The two rows of `q_*` are equal. Therefore its orbit under all four flips is
exactly

```text
q_0 = (1/3,1/6,1/3,1/6),
q_1 = (1/6,1/3,1/6,1/3).                                       (19)
```

The first and third atoms agree and are positive in both orbit elements. Any
`L_2` response containing a zero cannot equal either one, and a boundary flip
only permutes zeros. From the complete fifteen-row table, the only full-support
`L_2` responses are

```text
(7/24,5/24,5/24,7/24),
(3/8,1/8,3/8,1/8),
(1/8,3/8,1/8,3/8).                                              (20)
```

Their first atoms are respectively `7/24`, `3/8=9/24`, and `1/8=3/24`.
The first atoms in (19) are `1/3=8/24` and `1/6=4/24`. The sets are disjoint,
so neither law in (19) appears anywhere in the complete `L_2` response image.
Because each flip is its own inverse, this proves

```text
q_* notin T_(s_R,s_O)(Image(barPhi_(L_2)))
for all four (s_R,s_O).                                        (21)
```

**Theorem 4 (same-passive-signature reduced nonisomorphism).**
`Red(L_1)` and `Red(L_2)` have equal passive retained objects but are not
isomorphic in `FinRIE_(R,O)^iso`.

**Proof.** Passive equality is (14). Suppose a reduced isomorphism existed.
It would consist of a bijective monoid map on the fifteen protocol classes and
one boundary relabeling, and it would intertwine every response. In particular,
the class of `do(E=0)` in `Red(L_1)` would map to an `L_2` class whose relabeled
response is `q_*`. Equation (21) proves that no such class exists. QED.

The diagnostic mediator-output contrast is

```text
TV(C_b(.|0),C_b(.|1)) = |1-2b|,
```

which is `1/3` for `L_1` and `1/2` for `L_2`. This scalar is not used in the
proof: an arbitrary protocol-class bijection need not preserve the named
mediator pair. The complete response-image obstruction (21) is load-bearing.

## 7. Passive nonidentifiability and recovery obstruction

Let `X=Red(L_1)` and `Y=Red(L_2)`. Equation (14) says

```text
Ubar_pass(X) = Ubar_pass(Y),                                    (22)
```

while Theorem 4 says `X` and `Y` are nonisomorphic. Hence
`Ubar_pass` is not essentially injective on the declared BSC subcategory.

**Corollary 5 (no universal two-sided recovery).** There is no functor

```text
R : FinObs_(R,O)^iso -> FinRIE_(R,O)^iso
```

with a natural isomorphism

```text
R Ubar_pass ~= identity_(FinRIE_(R,O)^iso)                      (23)
```

on the declared subcategory.

**Proof.** If (23) existed, its components at `X` and `Y`, together with (22),
would give

```text
X ~= R(Ubar_pass(X)) = R(Ubar_pass(Y)) ~= Y,
```

contradicting Theorem 4. QED.

This argument does not refute a conventional right inverse satisfying

```text
Ubar_pass R ~= identity_(FinObs_(R,O)^iso).                     (24)
```

Equation (24) may select one active representative of a passive object; it
does not recover every active object in that passive fiber.

## 8. Exact theorem boundary

The theorem is category-relative. It establishes finite passive-to-active
nonidentifiability for normalized binary BSC chains, all partial hard
assignments, the complete two-sided contextual quotient, and typed boundary
bit flips. It does not establish that the declared category is ontologically
canonical, that `E`, `N`, or an intervention target is an autonomous agent,
that arbitrary latent dilations or soft/stochastic/continuous interventions
obey the same theorem, or that continuum, gauge, renormalization, VFE, or
physical quantities emerge from this construction.
