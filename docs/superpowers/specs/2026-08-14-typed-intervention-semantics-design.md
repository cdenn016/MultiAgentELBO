# Finite Typed-Intervention Semantics Design

**Date:** 2026-08-14
**Status:** Approved design
**Repository baseline:** `f956c7f1d7fb035d157b415c670a13a46f631233`
**Theory tier:** finite typed DAGs, normalized finite kernels, exact rational witnesses

## Purpose

The current theory proves that retained observational laws do not determine every enriched typed-intervention presentation, but the unconditional recovery claim remains inconclusive because the ambient category and its isomorphisms were not formalized. This design closes that finite obligation without treating arbitrary node inventory as ontology.

The central distinction is between three levels:

1. a raw typed causal presentation, which remembers the DAG, finite node types, state spaces, normalized local kernels, and hard-intervention targets;
2. its protocol-indexed retained response experiment, which remembers what each admitted intervention does to the retained boundary law; and
3. an operational reduction by equality of the complete two-sided response signature under the total right-override intervention monoid.

The raw category records a declared causal syntax. The reduced experiment removes inert padding. Neither level establishes autonomous agency or physical ontology.

## Existing certified boundary

This design extends, without rewriting, the published certificates:

- `docs/derivations/2026-08-13-finite-presentation-descent-joint-fisher/`, which proves descent of retained VFE and retained Fisher objects under retained-law equality and exhibits direct, latent, and null-extended BSC presentations;
- `docs/derivations/2026-08-14-canonical-dependence-selection/`, which leaves broad typed-intervention recovery inconclusive and proves only the conditional forgetful-fiber no-go.

The new result formalizes one finite category and proves an internal nonisomorphism theorem. It does not declare that category ontologically canonical.

## Raw finite typed presentations

Let `FinTIP_(R,O)^iso` be the groupoid whose objects are tuples

```text
P = (V, tau, (X_v), G, (kappa_v), r, o).
```

The data satisfy:

- `V` is a finite nonempty node set;
- `r,o in V` are distinguished retained-state and record nodes;
- `tau` assigns a declared role/type to every node;
- every `X_v` is a finite nonempty state space;
- `G` is a finite DAG on `V`;
- every `kappa_v : X_pa(v) -> Delta(X_v)` is a normalized finite Markov kernel;
- the observational law is the normalized truncated product of the local kernels;
- every finite hard intervention replaces the selected local kernel by a point mass and leaves all other mechanisms unchanged.

An isomorphism is a node bijection together with state-space bijections that fixes the retained roles, preserves node types, carries the DAG to the DAG, transports every local kernel, and intertwines every hard intervention and its induced law. The groupoid uses only invertible arrows because the recovery obstruction requires only isomorphism.

## Passive forgetful functor

Let `FinObs_(R,O)^iso` contain finite retained objects

```text
(X_R, X_O, P_RO),
```

with typed boundary relabelings as isomorphisms. The passive forgetful functor

```text
U_pass : FinTIP_(R,O)^iso -> FinObs_(R,O)^iso
```

forgets auxiliary nodes, factorization, and auxiliary intervention targets while retaining the complete passive joint law on `(R,O)`. The load-bearing passive BSC laws are strictly positive, so any conditional used for interpretation is canonically recovered by division. Intervened responses are compared as complete joint tables, including when some cells vanish; no version-dependent conditioning on null events enters the category.

## Protocol-indexed response and operational reduction

For a raw presentation `P`, let `A_P` be the finite monoid of all partial hard assignments to its nodes: a context is a partial section with domain in `V` and value `i(v) in X_v` at every assigned node. In the executable binary subcategory this is a partial map `V -> {0,1}`. The product is right override:

```text
(i star j)(v) = j(v) if j assigns v, and i(v) otherwise.
```

The empty assignment is the identity. This total operation represents sequential hard interventions with the later command taking precedence. Let

```text
Phi_P(i) = retained law P_RO^i
```

be the retained response to context `i`. Define the two-sided behavioral relation

```text
i ==_P j iff Phi_P(u star i star v) = Phi_P(u star j star v)
              for every u,v in A_P.
```

Equality of the complete two-sided response signatures makes `==_P` an equivalence relation. Associativity of right override makes it a two-sided monoid congruence. Therefore the reduced protocol monoid

```text
Abar_P = A_P / ==_P
```

and the response map on its identity-based classes are well-defined.

Let `FinRIE_(R,O)^iso` be the groupoid of these finite reduced intervention experiments.

An isomorphism is a monoid isomorphism of reduced protocol classes, together with typed boundary relabelings, that preserves the identity class and every retained response law.

Reduction defines a functor

```text
Red : FinTIP_(R,O)^iso -> FinRIE_(R,O)^iso.
```

The reduced passive functor

```text
Ubar_pass : FinRIE_(R,O)^iso -> FinObs_(R,O)^iso
```

retains the identity-class response and forgets the remaining protocol monoid.

This congruence removes an isolated null node: for either assignment to the null node and every partial assignment to the retained state, mediator, and record nodes, the retained response is unchanged. It does not identify two active response experiments whose complete reduced response images differ.

## Frozen target

The universal target is:

> For every two admissible finite reduced typed-intervention experiments in the declared BSC subcategory, equality of their passive retained `(R,O)` law implies isomorphism of their reduced protocol-indexed retained response experiments.

The target is `UNIVERSAL`. Its negative certificate kind is `COUNTEREXAMPLE`.

The intended terminal disposition is `COMPLETE_NEGATIVE`. The load-bearing counterexample must use the same graph, node inventory, state cardinalities, and intervention target so that the result cannot be attributed to null padding or syntactic node count.

## Load-bearing same-signature witness

For a binary symmetric channel write

```text
C_epsilon(y | x) = (1-epsilon) 1[y=x] + epsilon 1[y!=x].
```

Take `R ~ Bernoulli(1/2)` and the chain `R -> E -> O`. Define

```text
L_1 = L(a=1/4, b=1/3),
L_2 = L(a=1/3, b=1/4).
```

Both have passive crossover

```text
delta(a,b) = a + b - 2ab = 5/12,
```

so their complete passive retained laws agree. Under `do(E=0)`, in retained-law order `(R,O)=(0,0),(0,1),(1,0),(1,1)`, the responses are

```text
Phi_L1(do(E=0)) = (1/3, 1/6, 1/3, 1/6),
Phi_L2(do(E=0)) = (3/8, 1/8, 3/8, 1/8).
```

The mediator total-variation contrasts remain useful diagnostics:

```text
TV(P_O^do(E=0), P_O^do(E=1)) = abs(1 - 2b),
```

which gives `1/3` for `L_1` and `1/2` for `L_2`. Unequal TV alone is not the load-bearing proof because an arbitrary reduced-protocol bijection could map the mediator pair to another pair.

Instead, enumerate every two-sided behavioral class and its retained response. Each model has exactly fifteen classes. Under every one of the four typed binary boundary relabelings, no response class of `L_2` equals the displayed `L_1` `do(E=0)` law. Thus their complete reduced response images differ up to every admitted boundary relabeling. No reduced protocol-monoid isomorphism can intertwine the response maps, even though the passive retained law and raw structural signature agree.

## Derived recovery theorem

Let `Lbar_i = Red(L_i)`. Because `Ubar_pass(Lbar_1) = Ubar_pass(Lbar_2)` while `Lbar_1` and `Lbar_2` are nonisomorphic, the reduced passive functor is not essentially injective on the declared BSC subcategory.

Consequently there is no reconstruction functor `R : FinObs_(R,O)^iso -> FinRIE_(R,O)^iso` with a natural isomorphism

```text
R Ubar_pass ~= identity
```

on `FinRIE_(R,O)^iso`. This is a no-two-sided-recovery theorem. It does not exclude a conventional right inverse satisfying

```text
Ubar_pass R ~= identity,
```

which selects one representative in each passive fiber.

## Direct, split, and null controls

Retain the earlier exact controls with

```text
a = 1/10,
b = 1/8,
delta(a,b) = 1/5,
eta = 2/5.
```

The direct `R -> O` BSC with crossover `1/5`, the split chain, and its independent null-node extension have one common passive retained law. The exact executable witness must additionally establish:

1. all nine hard-intervention laws on the shared retained signature `{R,O}` agree;
2. `do(E=0)` and `do(E=1)` in the split model have retained-output total-variation separation `3/4`;
3. for both `n=0,1` and all `3^3=27` partial assignments `c` over `{R,E,O}`, `Phi(do(N=n) star c)=Phi(c)`;
4. the two-sided congruence classes containing `do(N=0)`, `do(N=1)`, and no-op agree;
5. forgetting `N` induces a quotient-monoid isomorphism from the null extension to the split reduced experiment.

The raw groupoid still distinguishes direct, split, and null-extended presentations. The reduced theorem must not use the null-node difference as its negative certificate.

## Executable witness contract

Create:

```text
docs/derivations/2026-08-14-typed-intervention-nonidentifiability/evidence/exact_typed_intervention_witness.py
tests/test_typed_intervention_semantics_witness.py
```

The witness uses only Python 3.14 standard-library exact arithmetic (`fractions.Fraction`, `itertools`, `json`). Floating-point probability calculations are forbidden.

### Frozen data types and validation

The law aliases are immutable tuples of `Fraction`. A binary law is ordered as `(P(0),P(1))`. A retained law is ordered as `(R,O)=(0,0),(0,1),(1,0),(1,1)`. Joint laws use ordinary lexicographic bit order in the node order declared by the function.

A context is the immutable tuple `tuple[tuple[str,int], ...]`, sorted by the fixed node order `R,E,N,O` after validation. Raw duplicate node assignments, unknown nodes, nonbinary values, invalid model strings, probabilities outside `[0,1]`, or a context that names a node absent from the selected presentation raise `ValueError`. The only model selector strings are `"direct"`, `"split"`, and `"null"`; the parameterized `"split"` selector represents both `L_1` and `L_2`. Context composition is total right override; validation of a raw context occurs before composition.

Required API and return shapes:

```text
bsc(epsilon, output_bit, input_bit) -> Fraction
compose_bsc(a, b) -> Fraction
compose_context(left, right) -> Context
direct_retained_law(delta, context=()) -> RetainedLaw
split_joint_law(a, b, context=()) -> tuple[Fraction, ...]       # R,E,O order
split_retained_law(a, b, context=()) -> RetainedLaw
null_extended_joint_law(a, b, eta, context=()) -> tuple[Fraction, ...]  # R,E,N,O
null_extended_retained_law(a, b, eta, context=()) -> RetainedLaw
intervention_response(model, *, a, b, eta=None, context=()) -> RetainedLaw
shared_boundary_intervention_law(model, context=()) -> RetainedLaw
mediator_response(b, mediator_bit) -> BinaryLaw
binary_total_variation(left, right) -> Fraction
contextual_response_signature(model, *, a, b, eta=None, context=()) -> tuple
response_image(model, *, a, b, eta=None) -> ReducedExperiment
same_signature_counterexample() -> CounterexampleRecord
raw_presentation_invariants(model) -> dict
main() -> int
```

`contextual_response_signature` is the complete finite table indexed by all pairs `(u,v)` of partial contexts and records `Phi(u star context star v)`; it therefore implements the two-sided congruence literally. A `ReducedExperiment` is `(classes, multiplication, responses)`: `classes` is the tuple of behavioral classes, each a lexicographically sorted tuple of contexts and with classes ordered by their least context; `multiplication` is the square tuple of zero-based class indices in that class order; and `responses` is the tuple of retained laws for the least representatives. `CounterexampleRecord` has exactly the keys `passive_equal`, `passive_law`, `left_experiment`, `right_experiment`, `left_unmatched_response`, `boundary_match_exists`, `diagnostic_tv`, and `raw_invariants_equal`. The tests call `response_image("split",...)` independently for both parameter pairs and compare those structures to the record, preventing an opaque hard-coded verdict. `main()` prints exactly the top-level keys `control`, `counterexample`, `null_control`, and `raw_invariants`. Its recursive encoder preserves booleans and categorical strings, maps every `Fraction` to its reduced rational string, maps every nonboolean integer to its decimal string, maps tuples/lists to JSON arrays, and then uses sorted compact JSON. Thus the printed document is a deterministic transform of independently tested native records rather than a second opaque result.

### Frozen exact tables

For the direct/split/null control, the common passive retained law is

```text
(2/5, 1/10, 1/10, 2/5).
```

The nine shared-boundary retained laws are, in canonical context order:

```text
noop       -> (2/5, 1/10, 1/10, 2/5)
do(R=0)    -> (4/5, 1/5, 0, 0)
do(R=1)    -> (0, 0, 1/5, 4/5)
do(O=0)    -> (1/2, 0, 1/2, 0)
do(O=1)    -> (0, 1/2, 0, 1/2)
do(R=0,O=0)-> (1, 0, 0, 0)
do(R=0,O=1)-> (0, 1, 0, 0)
do(R=1,O=0)-> (0, 0, 1, 0)
do(R=1,O=1)-> (0, 0, 0, 1)
```

For the same-signature pair the common passive retained law is `(7/24,5/24,5/24,7/24)`. The `do(E=0)` and `do(E=1)` output laws are `(2/3,1/3)`, `(1/3,2/3)` for `L_1`, and `(3/4,1/4)`, `(1/4,3/4)` for `L_2`. Both raw structural invariant records are exactly: roles `(retained-state,mediator,record)`, cardinalities `(2,2,2)`, edges `((R,E),(E,O))`, auxiliary target `(E)`.
### Frozen reduced-response controls

Canonical context order is lexicographic order of the node-state vector in node order `R,E,O`, with the symbols ordered as unassigned before `0` before `1`. The fifteen least representatives and identity responses are:

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

For `M[i][j]=[representative_i star representative_j]`, the compact JSON multiplication table has SHA-256 `c65706798f15a0a7fe8ee6d2be77525dc9afabf4266443f182d151ede619ea2d` for both models. The canonical full-experiment serialization is a recursively key-sorted compact JSON object with keys `boundary_order`, `identity`, `multiplication`, `node_order`, and `records`; `identity` is the numeric zero class index. Each record has `members` as the canonically ordered list of every raw context in the class, `representative` as the first such context, and `response` as reduced rational strings. The class-size vector is exactly `(1,3,3,1,1,1,3,3,1,1,1,3,3,1,1)`. Contexts are lists of `[node,bit]` pairs. Serialize with `json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")`. Each byte string has length 2337. The exact SHA-256 values are `7a9b8ef13488caca86f061633c092873b8f64a949c7e134f1ae7eb27cae65283` for `L_1` and `a83aa65a81eeda2817cc584c284b999453ec3633187881737ea159df41219dd0` for `L_2`.

For the null control, the complete two-sided signatures of no-op, `do(N=0)`, and `do(N=1)` are byte-identical. Serialize the response sequence in `u`-major, `v`-major canonical-context order as compact JSON rational arrays. Its SHA-256 is `19a12f8ac81046c57b6ff3d2c6039d69fab34639e47e9af074f431638ac3ce33`.

Required exact tests:

1. exact BSC composition, normalization, and validation failures;
2. exact retained-law equality for direct, split, and null presentations;
3. literal equality to every frozen shared-boundary table above;
4. exact mediator responses and TV `3/4` for the control;
5. exhaustive nullness for both null assignments and all 27 partial `{R,E,O}` contexts;
6. direct equality of the complete two-sided signatures of no-op, `do(N=0)`, and `do(N=1)`, plus quotient-monoid well-definedness and split/null reduced isomorphism;
7. same-signature passive equality at crossover `5/12`, the frozen response laws, and diagnostic contrasts `1/3` versus `1/2`;
8. exhaustive four-boundary-relabeling proof that the full reduced response images do not match;
9. exact raw structural invariant equality and all allowed binary state relabeling controls;
10. deterministic JSON with exactly the four frozen top-level keys and recursive transformation above; keys are lexicographically ordered, separators are `(",",":")`, all numeric leaves are reduced rational or decimal strings matching `^-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?$`, booleans remain booleans, categorical strings remain strings, and the document ends in exactly one LF;
11. fresh-process byte equality for JSON and byte identity between the live LF test file and its package snapshot.

Tests must be committed and observed failing before the witness exists. RED and GREEN JUnit XML, the byte-identical LF test-source snapshot, per-mutant command/exit/JUnit evidence with pre/post source SHA-256, and a TDD record must be retained inside the derivation package. The test path and package path both receive explicit `text eol=lf` rules. An unsorted nested-JSON mutation must fail.

## Durable certificate

The rigorous-theory run lives at:

```text
docs/derivations/2026-08-14-typed-intervention-nonidentifiability/
```

It contains the nine required root artifacts plus contained proof, exact-witness, independent-reconstruction, oracle-erasure, and adversarial evidence. The release validator must return `COMPLETE_NEGATIVE` for the frozen universal target.

The claim ledger must distinguish raw typed-presentation well-definedness; passive BSC equality; two-sided congruence and protocol reduction well-definedness; null-node operational collapse; full response-image relabeling invariance; same-signature reduced nonisomorphism; nonessential injectivity of `Ubar_pass`; no universal two-sided recovery; conventional right-inverse allowance; shared-boundary intervention equality; and autonomous agency/physical interpretation as open non-target claims.

## Central integration

After release certification, propagate only the verified finite boundary into `Theory/05d_relational_inference.tex`, `Theory/SPEC.md`, `Theory/appendix_claim_ledger.tex`, `overview.md`, `docs/STATUS.md`, and `docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md`.

The August 13 and earlier August 14 packages remain immutable. Replace the current broad typed-intervention `INCONCLUSIVE` status only for the declared finite category. Preserve as open ontological canonicity, autonomous agency, arbitrary soft interventions or latent-dilation equivalence, continuum/gauge categories, and all physical identifications.

## Verification gates

Before publication, the rigorous-theory release validator, focused exact suite, full CPU suite, converged TeX build, evidence-hash audit, EOL/C0/UTF-8 checks, independent mathematics and manuscript reviews, closure ledger, and `git diff --check` must pass on the exact committed revision. Publication uses an explicit feature push, `--ff-only` main update, non-force main push, and local/remote SHA parity proof.

## Claim boundary

This project may conclude that passive retained data fail to identify active response semantics in the declared finite category. It may not conclude that latent mediators are autonomous agents, that the category is the unique ontology, that null-node inventory is physical, or that intervention semantics emerge from VFE alone.
