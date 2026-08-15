<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-af08539e8868b09e5165943d91c488c6e06a00ac7a00b1d408ae22ddca6ee7e1","schema_version":"rigorous-theory-search/v1","target_digest":"af08539e8868b09e5165943d91c488c6e06a00ac7a00b1d408ae22ddca6ee7e1"} -->
# Counterexample register

Detailed calculations for every entry are in
`evidence/counterexample-proofs.md`.  Entries labeled **scope control** are
outside a frozen hypothesis and do not refute the target.

## CE-OIE-001: nonrigidity after forgetting the raw quotient map

**Claim attacked.** A minimum response-compatible quotient is unique up to a
unique isomorphism as a bare response monoid.

**Witness.** Take the four-element monoid `P({1,2})` under union and response
`Phi(S)=|S|`.  Contextual equivalence is equality, but swapping `1` and `2`
is a nonidentity response-preserving monoid automorphism.

**Disposition.** `REFUTED` for bare-object unique rigidity.  The frozen claim
is narrower and survives: comparison over the raw map from `A` forces the
unique factor map.  Minimum cardinality is asserted only for finite `A`.

## CE-OIE-002: passively equal BSCs have unequal marked soft faces

**Claim attacked.** The passive retained law identifies the marked finite
soft mediator experiment.

**Witness.** The chains `L_1=L(1/4,1/3)` and `L_2=L(1/3,1/4)` both have
passive crossover `5/12`.  On the mediator replacement face

```text
K_t(E=0|R=r)=t_r,       t in [epsilon,1-epsilon]^2,
```

their exact total-variation diameters are

```text
(1-2epsilon)/3       and       (1-2epsilon)/2.
```

Every strict-interior parent-independent pair has separation
`|1-2b|(s_+-s_-)`, so the discrepancy does not depend on hard endpoints.

**Disposition.** Certified mathematical counterexample under morphisms that
preserve the mediator target face, the ordered `R`-to-`O` boundary, and one
global boundary response map.  It supports, rather than refutes, the frozen
affirmative conjunction.

## CE-OIE-003: target erasure and time reversal change the category

**Strengthening controlled.** Drop target coloring or permit exchange of `R`
and `O` and reversal of the chain.

**Witness.** If target coloring is erased, an arbitrary protocol map need not
carry the mediator face to itself, so its diameter is no longer invariant.
Separately, BSC reversibility gives

```text
(1/2)B_a(e|r)B_b(o|e)=(1/2)B_b(e|o)B_a(r|e),
```

which maps the baseline presentation `L(a,b)` to `L(b,a)` under path reversal.

**Disposition.** Scope control.  It shows that target preservation and
boundary order are load-bearing.  It does not construct an isomorphism of the
frozen forward active experiments and does not refute CE-OIE-002.

## CE-OIE-004: convexification destroys the old hard response invariant

**Proof strategy attacked.** Reuse the unmatched deterministic response from
the hard theorem after allowing unmarked randomized protocols.

**Witness.** If `q_*=(1/3,1/6,1/3,1/6)` is the `L_1` response to `do(E=0)`,
then in `L_2`

```text
q_* = (5/6) response(do(E=0)) + (1/6) response(do(E=1)).
```

Moreover, the four hard boundary assignments `do(R=r,O=o)` are the four
vertices of the retained four-atom simplex, so their mixtures span its full
law space.

**Disposition.** The old response-image obstruction is `REFUTED` as a
randomized invariant.  The frozen randomized theorem instead uses full
contextual rank, convolution, affine structure, and the fact that affine
simplex isomorphisms preserve hard vertices.  Any admitted randomized
isomorphism would therefore restrict to a response-compatible hard-monoid
isomorphism, contradicting the released hard reduced nonisomorphism.

## CE-OIE-005: selector marginals do not determine shared-noise composition

**Strengthening attacked.** Use independent convolution to represent
correlated sequential randomization.

**Witness.** In a two-coordinate right-override monoid, let the first selector
set coordinate one to unbiased `Z` and the second set coordinate two to
unbiased `W`.  Independent bits give the uniform law on four composites;
`W=Z` gives only `(0,0),(1,1)`; and `W=1-Z` gives only `(0,1),(1,0)`.  The
selector marginals are identical in all three cases.

**Disposition.** `REFUTED` for a marginal-convolution model of shared noise.
Correlated protocols require a joint selector/coupling and are outside the
frozen independent-randomization theorem.

## CE-OIE-006: null conditional versions change point interventions

**Strengthening attacked.** Infer every point intervention from the passive
observational law on a standard-Borel space.

**Witness.** With uniform `R` on `[0,1]`, two Borel Bernoulli kernels for `E`
can agree with parameter `1/2` except at `r_*=1/2`, where their parameters are
respectively `0` and `1`.  They induce the same joint observational law but
opposite responses to `do(R=r_*)`.

**Disposition.** `REFUTED` for uncontrolled null-version identification.  The
frozen theorem uses explicitly declared pointwise normalized mechanisms.

## CE-OIE-007: a measurable contextual quotient can be nonsmooth

**Strengthening attacked.** Every contextual quotient of a standard-Borel
protocol monoid by a Borel response is automatically standard Borel.

**Witness.** Let `A={0,1}^N` under XOR and let `Phi(x)` indicate finite
support.  Then

```text
x equiv_Phi y iff x xor y has finite support,
```

the nonsmooth eventual-equality relation `E_0`.

**Disposition.** `REFUTED` for automatic standard-Borel quotient structure.
The algebraic quotient still exists.  A measurable quotient theorem needs an
explicit smooth classifier or stronger topological hypotheses.

## CE-OIE-008: noncompact input need not have compact quotient

**Strengthening attacked.** Delete compactness from the compact quotient
theorem while retaining its compact conclusion.

**Witness.** For `A=(R,+)` and `Phi=id_R`, contextual equivalence is equality,
so the quotient is `R`, not compact.

**Disposition.** `REFUTED` for the unqualified strengthening.  No claim is
made about alternative noncompact sufficient hypotheses.

## CE-OIE-009: circle heat pair has equal passive law and unequal experiment

**Claim attacked.** The passive retained law identifies the frozen
compact-Feller mediator experiment.

**Witness.** For `0<s<t`, compare

```text
P_1=m(dR)H_s(R,dE)H_t(E,dO),
P_2=m(dR)H_t(R,dE)H_s(E,dO).
```

Both retain `m(dR)H_(s+t)(R,dO)`.  Yet `H_s` strictly Blackwell-dominates
`H_t`: `H_t=H_sH_(t-s)`, while a reverse garbling would violate first-Fourier
mode Markov contraction.  Constant-parent mediator preparations satisfy

```text
{nu H_t} proper-subset {nu H_s},
```

with positive smooth strictness witness
`nu_rho=H_rho(x_0,dot)`, `0<rho<t-s`.

**Disposition.** Certified mathematical counterexample under the fixed
ordered boundary, mediator parameter experiment, heat geometry, compatible
protocol map, and one global response map.  It supports the frozen
affirmative conjunction.

## CE-OIE-010: circle time reversal and latent-coordinate freedom

**Strengthening controlled.** Permit time reversal, boundary exchange, or
arbitrary latent maps that need not intertwine the heat semigroup.

**Witness.** Reversibility gives

```text
m(dr)H_s(r,de)H_t(e,do)=m(do)H_t(o,de)H_s(e,dr),
```

so the baseline circle path presentations reverse into one another.  In a
linear-Gaussian alternative, latent rescaling can simultaneously change
incoming coefficients, latent noise scale, and outgoing coefficients, making
an unfrozen latent-scale contrast a coordinate gauge.

**Disposition.** Scope control.  These are different morphism categories;
they do not refute CE-OIE-009.  They explain why heat-intertwining typed maps,
ordered boundary roles, and a global protocol-independent response map are
explicit hypotheses.

## CE-OIE-011: operational minimality is not raw-realization minimality

**Strengthening attacked.** The minimum contextual protocol quotient uniquely
selects a latent DAG/generative realization.

**Witness.** Adjoin to any presentation an independent, unretained, isolated
node `N`.  Its assignments and replacement kernels never change a retained
response, so its protocol coordinate disappears under contextual quotient,
while the raw DAG, state spaces, and kernels have changed.

**Disposition.** `REFUTED` for deriving raw uniqueness from operational
minimality alone.  Minimal realization itself remains `OPEN`: it first needs a
realization category, morphisms, complexity functional, and
reachability/observability conditions controlling null padding, state
splitting, and gauge labels.

## Frozen-target falsification boundary

A counterexample satisfying a conjunct's frozen hypotheses and admitted
morphisms would refute that conjunct.  None is registered here.  Missing proof
or unresolved hypothesis mapping would instead make the release
`INCONCLUSIVE`.  Failure of a target-erasing, correlated, null-version,
noncompact, raw-realization, ELBO/VFE, agency, gauge/RG, or ontology extension
is outside the frozen conjunction and cannot be counted as a target
falsifier.
