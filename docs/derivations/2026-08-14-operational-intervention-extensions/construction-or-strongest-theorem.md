<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-af08539e8868b09e5165943d91c488c6e06a00ac7a00b1d408ae22ddca6ee7e1","schema_version":"rigorous-theory-search/v1","target_digest":"af08539e8868b09e5165943d91c488c6e06a00ac7a00b1d408ae22ddca6ee7e1"} -->
# Construction or strongest theorem

## Strongest directly derived result

Fix a monoid `A`, response set `Y`, and response map `Phi:A->Y`, and define

```text
a equiv_Phi b iff Phi(u a v)=Phi(u b v) for every u,v in A.
```

The evidence files `evidence/direct-derivation.md` and
`evidence/counterexample-proofs.md` establish the following scoped theorem.

**Operational-intervention extension theorem.**

1. The relation `equiv_Phi` is the largest two-sided monoid congruence
   contained in `ker(Phi)`.  If `(q,B,psi)` is any response-compatible
   quotient triple, meaning that `q:A->B` is a surjective unital monoid
   homomorphism and `Phi=psi q`, there is one unique surjective unital
   homomorphism

   ```text
   h:B->Syn(Phi):=A/equiv_Phi
   ```

   satisfying `pi=h q` and `barPhi h=psi`.  Thus `Syn(Phi)` is terminal when
   arrows point from finer response-compatible quotients to coarser ones.
   When `A` is finite, it has minimum cardinality, and equality of quotient
   cardinalities makes `h` an isomorphism over `A`.  These cardinality claims
   are finite-only.  Bare-object unique rigidity is never asserted after the
   quotient map from `A` has been forgotten.

2. If `A` is compact metrizable with jointly continuous multiplication, `Y`
   is metrizable Hausdorff, and `Phi` is continuous, then `Syn(Phi)` is compact
   metrizable and its descended multiplication and response are continuous.
   A countable dense context set gives a continuous complete signature whose
   compact image realizes the quotient.  The same terminal property holds
   continuously among compact-Hausdorff topological response-compatible
   triples for which `q` and `psi` are continuous and `q` is a quotient map.

3. For a finite normalized DAG on finite state spaces, compact replacement
   palettes inside the finite-dimensional stochastic-kernel polytopes, with
   their Euclidean/evaluation-subspace topology, form a compact componentwise
   right-override protocol monoid after adjoining isolated `bottom` symbols.
   Replacement preserves normalization, and every retained-law coordinate is
   a finite polynomial in continuous kernel coordinates, so the response is
   continuous.  In the marked mediator face of the passively equal BSC pair

   ```text
   L_1=L(1/4,1/3),       L_2=L(1/3,1/4),
   ```

   the exact total-variation diameters on
   `[epsilon,1-epsilon]^2`, `0<epsilon<1/2`, are

   ```text
   (1-2epsilon)/3       and       (1-2epsilon)/2.
   ```

   Every strict-interior parent-independent pair
   `epsilon<s_-<s_+<1-epsilon` has separation
   `|1-2b|(s_+-s_-)`.  Consequently, equal passive retained laws do not
   determine the marked soft experiment under the declared typed,
   ordered-boundary-preserving morphisms.

4. For the released fifteen-class hard protocol monoid `S`, independently
   randomized selectors form the affine convolution monoid `Delta(S)`, with
   response equal to the affine mixture of deterministic responses.  A
   fifteen-coordinate contextual-signature minor for the BSC family has

   ```text
   det M(b,delta) = (2b-1)^6 (2delta-1)^3 / 32,
   ```

   and is nonzero for both models at `delta=5/12`.  Hence randomized
   behavioral equivalence is equality.  Any admitted affine unital
   convolution-monoid isomorphism maps simplex vertices to vertices and would
   restrict to the already-refuted hard response-experiment isomorphism.
   Passive equality therefore does not identify the independently randomized
   response experiment, even though convexification makes the old unmatched
   hard response a mixture in the other model.

5. For a finite DAG of standard-Borel node spaces with standard-Borel
   palettes and declared normalized pointwise kernels whose evaluations are
   jointly measurable, finite topological-order recursion gives normalized
   joint laws and a Borel response into the retained-law space equipped with
   its evaluation sigma-algebra.  The algebraic quotient exists, but it need
   not be standard Borel.  Under the stronger compact-Polish, compact-palette,
   isolated-bottom, finite-coordinate right-override, and jointly Feller
   hypotheses, the response is weakly continuous and the compact quotient in
   item 2 applies.  Finite-coordinate does not mean finite cardinality.

6. Let `T` be the circle with normalized Haar law and heat kernels `H_tau`.
   For every `0<s<t`, the chains

   ```text
   P_1=m(dR)H_s(R,dE)H_t(E,dO),
   P_2=m(dR)H_t(R,dE)H_s(E,dO)
   ```

   have the same passive retained law
   `m(dR)H_(s+t)(R,dO)`.  With mediator palette `P(T)` in the weak topology
   and constant-parent replacements `K_nu(dE|R=r)=nu(dE)`, the palette is
   compact metrizable and jointly Feller.  The mediator channels satisfy the
   strict one-way Blackwell comparison

   ```text
   H_t=H_s H_(t-s),       but no Markov L has H_s=H_t L,
   ```

   and their soft output sets satisfy

   ```text
   {nu H_t:nu in P(T)} proper-subset {nu H_s:nu in P(T)}.
   ```

   Strictness has the positive smooth witness
   `nu_rho=H_rho(x_0,dot)` for every fixed `x_0` and
   `0<rho<t-s`.  Thus passive equality also fails to identify this frozen
   compact-Feller mediator experiment.

## Canonicity and morphism qualifications

The quotient in items 1 and 2 is canonical only relative to the fixed
operational data `(A,Phi,Y)`, the quotient map from `A`, any retained
target/type coloring, and the admitted morphisms.  The four-element
power-set union monoid in `evidence/counterexample-proofs.md` has a nontrivial bare
response-preserving automorphism, so uniqueness must remain over `A`.

For the finite BSC and circle conclusions, `R` is fixed as input/parameter and
`O` as output/observation.  A presentation comparison is induced by invertible
typed state maps, their compatible protocol map `Theta`, and one
protocol-independent boundary map `U` satisfying
`Phi'(Theta(a))=U(Phi(a))` for every protocol.  The mediator target face is
retained, and circle maps additionally intertwine the heat kernels.  Neither
boundary exchange nor time reversal is admitted.

## Open boundary

The theorem does not establish a target-erasing arbitrary-soft result,
correlated/shared-noise randomization, point interventions inferred from
almost-sure observational conditionals, a standard-Borel quotient without a
smooth classifier, a noncompact quotient theorem, or a canonical raw
latent/DAG/generative realization.  It also makes no equality claim for
fixed-observation ELBOs, latent posteriors, or factorizations and no claim
about agency, gauge/RG dynamics, continuum physics, or ontology.

The exact recomputation is corroborative only.  Formal release status remains
pending the package-wide independent reconstruction, adversarial checks,
hash-bound evidence ledger, and release validator.
