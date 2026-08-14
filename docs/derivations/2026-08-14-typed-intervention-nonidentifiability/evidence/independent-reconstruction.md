<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-efe715cba81c2000403811015e6cecb599f4023133543b5cb0ae77288bccc874","schema_version":"rigorous-theory-search/v1","target_digest":"efe715cba81c2000403811015e6cecb599f4023133543b5cb0ae77288bccc874"} -->
# Independent reconstruction from the frozen contract

## Method and independence boundary

This reconstruction starts from the frozen problem contract and the elementary
definitions of a finite normalized DAG, a hard intervention, a partial
assignment, and an isomorphism. It does not assume the desired negative
conclusion, the Task 3 proof narrative, the executable witness, or the
diagnostic total-variation values. After the derivation was complete, its
tables and byte-level invariants were compared with the proof and exact
execution artifacts.

The setting is finite and discrete. Every state space is nonempty, every
kernel is a normalized probability mass function with respect to counting
measure, and every response is the complete retained joint law on the ordered
boundary `(R,O)`. No conditional distribution on a zero-probability event,
limit, differentiation, or measure disintegration is used.

## Raw presentations and normalization

For a presentation `P` on a finite DAG `G=(V,E)`, define

```text
p_P(x) = product_(v in V) kappa_v(x_v | x_pa(v)).
```

Choose a topological ordering and sum out sinks in reverse order. At each
step, the only remaining factor containing the sink state is its normalized
local kernel, whose sum is one. Repetition leaves one, proving that `p_P`
is normalized. Replacing any selected local kernel by a point mass preserves
this argument. Two successive hard interventions compose nodewise by taking
the last assignment, so

```text
(P^i)^j = P^(i star j).
```

A typed node and state-space bijection transports each original kernel or
intervention point mass and therefore transports both the full law and its
retained marginal. Identities, composites, and inverses preserve those data,
which independently reconstructs the raw groupoid and its passive functor.

## Right-override reduction

At each node, `i star j` takes `j`'s value when present, otherwise
`i`'s value, otherwise remains unassigned. The empty assignment is a
two-sided identity. For any three contexts, both parenthesizations select the
last assignment among the three at each node; hence right override is
associative.

Define

```text
i == j  iff  Phi(u star i star v) = Phi(u star j star v)
             for every pair of contexts u,v.
```

Equality of these complete signatures is reflexive, symmetric, and
transitive. If `i == j`, associativity rewrites the signature of
`a star i star b` at `(u,v)` as the signature of `i` at
`(u star a,b star v)`; the same holds for `j`. Thus the relation is a
two-sided congruence. The quotient multiplication
`[i][j]=[i star j]`, identity `[empty]`, and response
`barPhi([i])=Phi(i)` are well-defined. Transport by a raw typed isomorphism
preserves the complete signature in both directions, so reduction is
functorial.

## BSC composition and the nine retained-boundary controls

For `C_e(y|x)=1-e` when `y=x` and `e` otherwise, summing over the
intermediate bit gives

```text
sum_z C_b(o|z) C_a(z|r) = C_(a+b-2ab)(o|r).
```

For the direct/split/null control `a=1/10`, `b=1/8`, so the composed
crossover is `1/5`. Direct calculation gives every retained boundary table:

| Boundary context | Retained law in order `00,01,10,11` |
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

The direct channel, split chain, and independent-null extension share these
nine boundary responses. This is a control and is not the counterexample.

## Independent null-node collapse

Let `pi` forget the isolated node `N`. It is a surjective right-override
monoid homomorphism. Whether `N` is unassigned or fixed to either bit, its
factor sums to one, so for every full context `i`,

```text
Phi_null(i) = Phi_split(pi(i)).
```

This equality covers the two fixed values of `N` and all
`3^3=27` partial contexts over `R,E,O`. Substitution into every left and
right context proves

```text
i ==_null j  iff  pi(i) ==_split pi(j).
```

Consequently forgetting `N` descends to an identity-, multiplication-, and
response-preserving quotient-monoid isomorphism. Null-node inventory is
therefore unavailable as a negative certificate.

## Same-passive-signature pair

Take the same binary chain `R -> E -> O`, the same roles, cardinalities,
edges, and mediator target, with

```text
L_1 = L(a=1/4,b=1/3),
L_2 = L(a=1/3,b=1/4).
```

Both composed crossovers equal

```text
1/4 + 1/3 - 2(1/4)(1/3) = 5/12
1/3 + 1/4 - 2(1/3)(1/4) = 5/12.
```

With uniform `R`, their complete passive retained laws are identically

```text
(7/24,5/24,5/24,7/24).
```

Thus the passive premise of the universal target holds by literal equality,
not only up to a boundary relabeling.

## Reconstruction of all fifteen behavioral classes

Write a raw context as `c(r,e,o)`, with each symbol in
`{unassigned,0,1}`. There are twenty-seven contexts. If `O` is fixed,
the central value of `E` is masked after every possible left and right
composition: the central `O` overrides a left assignment and a right
assignment can only replace it. For each fixed pair `(r,o)`, the three
`E` statuses therefore form one class. There are six such size-three
classes. When `O` is unassigned, the nine contexts are pairwise distinct
already at their identity responses, so each is a singleton. This gives
`6*3+9=27` raw contexts and exactly fifteen classes, with size vector

```text
(1,3,3,1,1,1,3,3,1,1,1,3,3,1,1).
```

The independently derived least representatives and responses are:

| ID | Representative | `L_1` response | `L_2` response |
| ---: | --- | --- | --- |
| 0 | `()` | `(7/24,5/24,5/24,7/24)` | same |
| 1 | `((O,0),)` | `(1/2,0,1/2,0)` | same |
| 2 | `((O,1),)` | `(0,1/2,0,1/2)` | same |
| 3 | `((E,0),)` | `(1/3,1/6,1/3,1/6)` | `(3/8,1/8,3/8,1/8)` |
| 4 | `((E,1),)` | `(1/6,1/3,1/6,1/3)` | `(1/8,3/8,1/8,3/8)` |
| 5 | `((R,0),)` | `(7/12,5/12,0,0)` | same |
| 6 | `((R,0),(O,0))` | `(1,0,0,0)` | same |
| 7 | `((R,0),(O,1))` | `(0,1,0,0)` | same |
| 8 | `((R,0),(E,0))` | `(2/3,1/3,0,0)` | `(3/4,1/4,0,0)` |
| 9 | `((R,0),(E,1))` | `(1/3,2/3,0,0)` | `(1/4,3/4,0,0)` |
| 10 | `((R,1),)` | `(0,0,5/12,7/12)` | same |
| 11 | `((R,1),(O,0))` | `(0,0,1,0)` | same |
| 12 | `((R,1),(O,1))` | `(0,0,0,1)` | same |
| 13 | `((R,1),(E,0))` | `(0,0,2/3,1/3)` | `(0,0,3/4,1/4)` |
| 14 | `((R,1),(E,1))` | `(0,0,1/3,2/3)` | `(0,0,1/4,3/4)` |

The product of classes is determined without a choice by
`M[i][j]=[representative_i star representative_j]`. Canonical compact-JSON
serialization of this multiplication table has SHA-256
`c65706798f15a0a7fe8ee6d2be77525dc9afabf4266443f182d151ede619ea2d`
for both models. The full canonical experiments each have length 2337 bytes
and SHA-256 values
`7a9b8ef13488caca86f061633c092873b8f64a949c7e134f1ae7eb27cae65283`
for `L_1` and
`a83aa65a81eeda2817cc584c284b999453ec3633187881737ea159df41219dd0`
for `L_2`. These hashes corroborate the reconstructed object identity; the
direct class argument and rational response table carry the mathematics.

## Four-relabeling response-image obstruction

Let

```text
q_* = (1/3,1/6,1/3,1/6),
```

the `L_1` response to `do(E=0)`. Independent flips of the binary
`R` and `O` labels generate only the two laws

```text
(1/3,1/6,1/3,1/6),
(1/6,1/3,1/6,1/3).
```

Every `L_2` response with a zero remains zero-containing after a boundary
flip. The only full-support responses in its complete fifteen-class image are

```text
(7/24,5/24,5/24,7/24),
(3/8,1/8,3/8,1/8),
(1/8,3/8,1/8,3/8).
```

Their positive atom values are drawn from
`{7/24,5/24,9/24,3/24}`, whereas the orbit of `q_*` uses
`{8/24,4/24}`. Hence no `L_2` response equals `q_*` after any of the
four admitted boundary relabelings. An arbitrary identity-preserving
protocol-monoid isomorphism must still send the `q_*` class to a class with
the required relabeled response. Since no such class exists, no reduced
experiment isomorphism exists.

This complete response-image obstruction is independent of the diagnostic
mediator total variations and of null-node inventory.

## Counterexample and recovery consequences

The two admitted reduced experiments have equal passive retained objects and
are nonisomorphic. They therefore refute the frozen universal implication by
a direct counterexample. The same pair proves that `Ubar_pass` is not
essentially injective. If a functor `R` satisfied
`R Ubar_pass ~= identity` on all reduced experiments in the subcategory,
the two nonisomorphic objects in the same passive fiber would both be
isomorphic to the same reconstructed object, a contradiction.

That contradiction has the opposite composition order from the conventional
section condition `Ubar_pass R ~= identity`. It neither proves nor refutes
the existence of such a representative-selecting section.

## Cross-check against contained artifacts

After this derivation, comparison with the contained proof and exact execution
artifacts found exact agreement on the definitions, normalization, nine
boundary tables, twenty-seven-context null audit, fifteen classes, class-size
vector, passive law, unmatched response orbit, multiplication hash, and both
full-experiment hashes. The focused CPU-only suite independently reported
eighteen tests, zero failures, zero errors, and zero skips. Those mechanical
checks corroborate the finite data but do not replace the derivation.

## Scope boundary

Nothing in this reconstruction selects the declared category as an ontology,
identifies a mediator or protocol with an autonomous agent, handles arbitrary
soft, stochastic, or continuous interventions, proves a minimal realization
theorem, extends the result to continuum or gauge categories, derives VFE
dynamics, or identifies informational quantities with physical units.
