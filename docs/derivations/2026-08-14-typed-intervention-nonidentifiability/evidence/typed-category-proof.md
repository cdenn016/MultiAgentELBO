<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-efe715cba81c2000403811015e6cecb599f4023133543b5cb0ae77288bccc874","schema_version":"rigorous-theory-search/v1","target_digest":"efe715cba81c2000403811015e6cecb599f4023133543b5cb0ae77288bccc874"} -->
# Raw finite typed presentations and functorial reduction

## Scope and evidence discipline

This artifact gives a direct finite derivation for the raw groupoid
`FinTIP_(R,O)^iso` and the reduction functor

```text
Red : FinTIP_(R,O)^iso -> FinRIE_(R,O)^iso.
```

All sets below are finite and nonempty, all sigma-algebras are discrete, and
all probability laws are mass functions with respect to counting measure.
There are no analytic limit, disintegration, or null-conditioning steps. The
exact executable witness is corroborative; none of the proofs below infer a
mathematical statement from enumeration or numerical agreement.

## 1. Objects and normalized laws

A raw presentation is

```text
P = (V, tau, (X_v)_(v in V), G, (kappa_v)_(v in V), r, o),
```

with the data and typing frozen in the problem contract. For a configuration
`x in X_V := product_(v in V) X_v`, write

```text
p_P(x) = product_(v in V) kappa_v(x_v | x_pa(v)).                 (1)
```

The product is independent of a chosen topological ordering because its
factors are real scalars indexed by nodes. The DAG determines the parent
arguments of each factor.

**Lemma 1 (normalization by finite DAG factorization).** Equation (1) is a
normalized probability law.

**Proof.** Choose a topological ordering `v_1,...,v_n`. The last node `v_n` is
a sink. In the sum of (1) over `X_V`, its state appears in no factor other than
`kappa_(v_n)`, so

```text
sum_(x_(v_n)) kappa_(v_n)(x_(v_n) | x_pa(v_n)) = 1.
```

Eliminating that factor leaves the same product on the induced DAG with
`v_n` removed. Repeating in reverse topological order yields `1`. Every factor
is nonnegative, so (1) is a probability mass function. This also covers roots,
whose parent state space is the one-point empty product. QED.

For a partial hard assignment `i`, define `P^i` by replacing `kappa_v` with
the Dirac kernel `delta_(i(v))` exactly when `v` is assigned and leaving every
other kernel unchanged.

**Lemma 2 (hard-intervention closure and sequential composition).** `P^i` is
again a raw finite typed presentation with a normalized induced law. If
`star` denotes right override, then

```text
(P^i)^j = P^(i star j).                                           (2)
```

**Proof.** A Dirac mass is a normalized finite kernel, so Lemma 1 applies
without change. At any node `v`, the kernel after the two interventions is the
Dirac mass at `j(v)` if `j` assigns `v`, the Dirac mass at `i(v)` if only `i`
assigns `v`, and the original kernel otherwise. This is exactly the
right-override rule in (2). QED.

Marginalizing the normalized law of `P^i` to the distinguished ordered
boundary `(R,O)` defines the complete retained response `Phi_P(i)`. Because it
is a complete joint table, this definition remains valid when some entries
are zero; it invokes no conditional distribution on a null event.

## 2. Typed isomorphisms and the raw groupoid

Let `P` and `Q` be raw presentations. A typed isomorphism `g : P -> Q`
consists of a node bijection `f : V_P -> V_Q` and state bijections
`h_v : X_v -> X_(f(v))` that preserve the declared roles, fix the retained
roles, carry edges to edges, and transport every local kernel. In coordinates,
if `y_(f(w))=h_w(x_w)` for the relevant nodes, kernel transport says

```text
kappa^Q_(f(v))(y_(f(v)) | y_pa(f(v)))
  = kappa^P_v(x_v | x_pa(v)).                                    (3)
```

The induced map on contexts is

```text
(g_# i)(f(v)) = h_v(i(v))                                        (4)
```

for assigned nodes and is undefined elsewhere. Let `H : X_(V_P) -> X_(V_Q)`
be the product state bijection, and let `beta=(h_r,h_o)` be its boundary
restriction.

**Lemma 3 (isomorphism transport).** For every context `i`,

```text
H_# p_(P^i) = p_(Q^(g_# i)),
Phi_Q(g_# i) = beta_# Phi_P(i),                                  (5)
```

and `g_#` is an isomorphism of right-override context monoids.

**Proof.** For an unintervened node, (3) identifies the corresponding product
factors. For an intervened node, the state bijection sends
`delta_(i(v))` to `delta_(h_v(i(v)))`. Multiplying these equalities over all
nodes proves the joint-law statement in (5); summing over all nonboundary
states proves the retained statement. Equation (4) preserves the empty
context. Pointwise, a later assignment remains the later assignment after a
bijection, hence

```text
g_#(i star j) = (g_# i) star (g_# j).
```

The inverse is induced by `(f^(-1),(h_v^(-1)))`, so `g_#` is a monoid
isomorphism. QED.

Identity node and state bijections satisfy (3), composites satisfy it by
substitution, and every typed isomorphism has the typed inverse just used.
Consequently these objects and arrows form the groupoid
`FinTIP_(R,O)^iso`. Lemma 3 also shows that passive marginalization is a
well-defined functor

```text
U_pass : FinTIP_(R,O)^iso -> FinObs_(R,O)^iso.
```

## 3. Operational objects

For each `P`, let `A_P` be its finite right-override context monoid and define

```text
i ==_P j
iff
Phi_P(u star i star v) = Phi_P(u star j star v)
for every u,v in A_P.                                            (6)
```

The companion artifact `operational-reduction-proof.md` proves directly that
right override is a monoid operation, that (6) is an equivalence and a
two-sided congruence, and that

```text
Abar_P := A_P / ==_P,
barPhi_P([i]) := Phi_P(i)                                        (7)
```

are well-defined. Thus the reduced object is the boundary-typed tuple

```text
Red(P) = (X_R, X_O, Abar_P, [empty], barPhi_P).
```

An arrow in `FinRIE_(R,O)^iso` is a pair `(alpha,beta)` where `alpha` is an
identity-preserving monoid isomorphism, `beta` is a typed boundary state
relabeling, and

```text
barPhi_Q(alpha(c)) = beta_# barPhi_P(c)                           (8)
```

for every reduced protocol class `c`. All such arrows are invertible, so
`FinRIE_(R,O)^iso` is a groupoid.

## 4. Reduction on arrows

For a raw isomorphism `g : P -> Q`, define

```text
Red(g)([i]_P) := [g_# i]_Q.                                      (9)
```

**Lemma 4 (behavioral equivalence is transported exactly).**

```text
i ==_P j  iff  g_# i ==_Q g_# j.                                (10)
```

**Proof.** Assume `i ==_P j`. Given arbitrary `u',v' in A_Q`, surjectivity of
the context-monoid isomorphism gives `u'=g_#u` and `v'=g_#v`. Lemma 3 and the
monoid law give

```text
Phi_Q(u' star g_#i star v')
 = beta_# Phi_P(u star i star v)
 = beta_# Phi_P(u star j star v)
 = Phi_Q(u' star g_#j star v').
```

This proves the forward implication. Apply the same argument to `g^(-1)` for
the reverse implication. QED.

Equation (10) makes (9) well-defined and bijective. Lemma 3 makes it an
identity-preserving monoid homomorphism, and (5) yields response
intertwining (8). Hence `Red(g)` is a reduced-experiment isomorphism.

**Proposition 5 (functoriality of operational reduction).** Equations (7) and
(9) define a functor

```text
Red : FinTIP_(R,O)^iso -> FinRIE_(R,O)^iso.
```

**Proof.** The context map of an identity raw isomorphism is the identity, so
`Red(id_P)=id_(Red(P))`. For composable raw isomorphisms `g,h`, their context
maps obey `(h o g)_#=h_# o g_#`; passing to equivalence classes gives
`Red(h o g)=Red(h) o Red(g)`. QED.

Finally,

```text
Ubar_pass(Red(P)) := (X_R, X_O, barPhi_P([empty]))
```

and the boundary part of a reduced arrow define the functor

```text
Ubar_pass : FinRIE_(R,O)^iso -> FinObs_(R,O)^iso.
```

The identity class is preserved by every reduced arrow, so this definition is
well-typed.

## 5. Exact scope boundary

The construction proves well-definedness only for the declared finite typed
DAGs, normalized finite kernels, hard interventions, typed isomorphisms, and
complete retained joint responses. It does not prove that this category is a
canonical ontology, that a mediator or intervention target is an autonomous
agent, or that arbitrary soft, stochastic, continuous, gauge, or
renormalization-scale interventions admit the same reduction.
