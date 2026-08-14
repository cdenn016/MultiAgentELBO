<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-efe715cba81c2000403811015e6cecb599f4023133543b5cb0ae77288bccc874","schema_version":"rigorous-theory-search/v1","target_digest":"efe715cba81c2000403811015e6cecb599f4023133543b5cb0ae77288bccc874"} -->
# Counterexample register

## CE-TIP-001: same passive law, different reduced active response image

**Universal target attacked.** Equality of the passive retained `(R,O)` law
implies isomorphism of the reduced protocol-indexed retained response
experiments for every pair in the frozen BSC subcategory.

**Witness.** Use the same binary chain, node roles, cardinalities, edges, and
mediator target in both objects:

```text
L_1 = L(a=1/4,b=1/3),
L_2 = L(a=1/3,b=1/4).
```

Both parameter pairs are normalized and admissible. Their composed crossover
is exactly

```text
a+b-2ab = 5/12,
```

so both passive retained laws are

```text
(7/24,5/24,5/24,7/24).
```

**Operational reduction.** Direct derivation partitions each set of twenty-seven
raw contexts into fifteen two-sided behavioral classes: nine singleton classes
with `O` unassigned and six size-three classes in which a hard-assigned `O`
masks the three possible central `E` statuses. The class-size vector is

```text
(1,3,3,1,1,1,3,3,1,1,1,3,3,1,1).
```

**Load-bearing obstruction.** In `L_1`, the class of `do(E=0)` has response

```text
q_* = (1/3,1/6,1/3,1/6).
```

Across all four independent binary flips of `R` and `O`, the orbit of `q_*`
contains only

```text
(1/3,1/6,1/3,1/6),
(1/6,1/3,1/6,1/3).
```

The only full-support responses anywhere in the complete `L_2` reduced image
have first atoms `7/24`, `3/8=9/24`, or `1/8=3/24`; the orbit atoms are
`1/3=8/24` or `1/6=4/24`. Responses with zeros remain responses with zeros
under relabeling. Hence no `L_2` response class can be carried to `q_*` by any
admitted boundary relabeling. An arbitrary identity-preserving protocol-monoid
isomorphism would still have to map the `q_*` class to such a response class,
so no reduced-experiment isomorphism exists.

**Direct evidence.** The full derivation is in
`evidence/operational-reduction-proof.md`; raw normalization, isomorphism
transport, and functoriality of `Red` are in
`evidence/typed-category-proof.md`. The exact rational witness and focused
tests corroborate the class table and response image but do not substitute for
these derivations.

**Disposition at this checkpoint.** Direct counterexample derivation complete;
terminal rigorous-theory release remains pending the Task 4 dependency ledger,
independent reconstruction, oracle erasure, and adversarial certificate.

## Non-load-bearing controls

The mediator-output total-variation values `1/3` and `1/2` diagnose the active
difference but do not close the theorem, because a protocol isomorphism need
not preserve the named mediator pair. Direct/split/null node-count differences
also do not close it. Indeed, the independent null extension is operationally
isomorphic to the split model after two-sided reduction: forgetting `N`
induces a quotient-monoid isomorphism and covers both assignments to `N` and
all twenty-seven contexts on `{R,E,O}`.

## Falsification and boundaries

CE-TIP-001 would fail if either parameterized chain were outside the frozen
subcategory or if one constructed an identity-preserving protocol-monoid
isomorphism whose response map intertwines under a single admitted typed
boundary relabeling. The exhaustive response-image obstruction rules out the
second possibility in the declared category.

The entry does not address category canonicity, autonomous agency, arbitrary
soft or continuous interventions, arbitrary latent-dilation equivalence,
continuum or gauge categories, renormalization, VFE emergence, or physical
identifications.
