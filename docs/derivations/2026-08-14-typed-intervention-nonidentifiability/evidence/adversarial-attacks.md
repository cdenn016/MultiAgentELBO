<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-efe715cba81c2000403811015e6cecb599f4023133543b5cb0ae77288bccc874","schema_version":"rigorous-theory-search/v1","target_digest":"efe715cba81c2000403811015e6cecb599f4023133543b5cb0ae77288bccc874"} -->
# Adversarial attack portfolio

## Method

Each attack was posed against the frozen statement, premises, and proof
artifacts. Responses use direct derivations or exact contained records, not
role agreement. An attack is rejected only against the scoped finite theorem;
broader ontology, agency, minimal-realization, continuum, gauge, and physical
questions remain open rather than being dismissed.

## ATTACK-01: category dependence

**Attack.** The conclusion could be advertised as category-independent even
though reduced isomorphism is defined only for finite hard-intervention
experiments with a specific two-sided quotient.

**Response.** The target quantifiers, domains, equivalence, and conclusion all
name the declared finite BSC subcategory. The raw and reduced objects and
arrows are typed in `evidence/typed-category-proof.md`; its final scope
section explicitly excludes canonicity and other intervention categories.
The final theorem repeats this relative scope. Category dependence therefore
does not invalidate the stated theorem.

**Disposition.** `REJECTED` against the frozen target. A category-independent
extension would require a separately frozen contract and proof.

**Falsification condition.** Show that either witness is not an object of the
declared category or that the conclusion silently quantifies over a different
category.

## ATTACK-02: protocol-monoid automorphisms

**Attack.** Unequal responses to the named mediator command do not preclude a
monoid automorphism from mapping that class to a different class with a
matching response.

**Response.** The proof does not rely on the named mediator pair or its
total-variation contrast. Section 6 of
`evidence/operational-reduction-proof.md` checks the complete response image
and shows that the `L_1` response `q_*` is absent from every boundary-
relabeling of the complete `L_2` image. Any protocol-monoid isomorphism is a
bijection of classes and must map the `q_*` class somewhere, where response
intertwining would fail.

**Disposition.** `REJECTED`.

**Falsification condition.** Exhibit an `L_2` class whose response is
`q_*` after one admitted boundary relabeling.

## ATTACK-03: abstract-action simulation

**Attack.** A renamed or abstractly simulated intervention action could
intertwine the two experiments even if no syntax-preserving map does.

**Response.** Reduced isomorphisms already permit arbitrary
identity-preserving monoid isomorphisms; they are not required to preserve
the labels `R`, `E`, or `O` on protocol representatives. The only
additional obligation is response intertwining under one typed boundary
relabeling. The missing response-image element defeats every abstract
simulation satisfying that obligation.

**Disposition.** `REJECTED`.

**Falsification condition.** Supply an identity-preserving monoid isomorphism
and one admitted boundary relabeling that intertwine every class response.

## ATTACK-04: null deletion

**Attack.** The negative result might be an artifact of counting an isolated
node or auxiliary intervention target.

**Response.** The load-bearing pair has the same nodes, roles, cardinalities,
edges, and mediator target. Separately, Section 3 of
`evidence/operational-reduction-proof.md` proves that forgetting an
independent null node induces a reduced-experiment isomorphism, covering both
null assignments and all twenty-seven contexts on `R,E,O`. Null inventory
cannot distinguish the counterexample pair.

**Disposition.** `REJECTED`.

**Falsification condition.** Show a raw-signature difference between
`L_1` and `L_2` or find a retained response that depends on the isolated
node.

## ATTACK-05: boundary relabeling

**Attack.** Independent bit flips on `R` or `O` might transform an
`L_2` response into the unmatched `L_1` response.

**Response.** All four flips are included. Because the two rows of
`q_*=(1/3,1/6,1/3,1/6)` agree, its four-flip orbit contains only `q_*`
and `(1/6,1/3,1/6,1/3)`. Neither occurs in the complete `L_2` response
image: zero-containing laws remain zero-containing, while its three
full-support laws use atom values `7/24,5/24,9/24,3/24`, disjoint from
`8/24,4/24`.

**Disposition.** `REJECTED`.

**Falsification condition.** Produce one of the two orbit laws in the
`L_2` response table.

## ATTACK-06: incomplete response-set matching

**Attack.** The proof might compare only mediator responses and overlook a
different protocol class with the same law.

**Response.** Section 5 derives all fifteen classes from all twenty-seven raw
contexts. Section 6 partitions the complete response table into full-support
and zero-containing laws before comparing the entire image. The executable
test `test_full_response_images_do_not_match_under_any_boundary_relabeling`
and the altered-response-image mutant corroborate that the implementation
reaches the complete image, but the direct table carries the proof.

**Disposition.** `REJECTED`.

**Falsification condition.** Identify a missing behavioral class or a
miscomputed row that contains an orbit element of `q_*`.

## ATTACK-07: right-inverse confusion

**Attack.** The recovery corollary could wrongly claim that no section
`R` with `Ubar_pass R ~= identity` exists.

**Response.** The contradiction uses the opposite composite,
`R Ubar_pass ~= identity`, on every reduced experiment. The proof and
release state only that universal two-sided reconstruction is impossible.
They explicitly leave the conventional representative-selection condition
`Ubar_pass R ~= identity` allowed.

**Disposition.** `REJECTED`.

**Falsification condition.** Find any release sentence that converts the
two-sided no-go into nonexistence of a conventional section.

## ATTACK-08: normalization and intervention closure

**Attack.** The finite product laws or intervened laws might fail to normalize,
putting the witness outside the declared domain.

**Response.** Lemma 1 of `evidence/typed-category-proof.md` sums sinks in
reverse topological order; every normalized local factor contributes one.
Lemma 2 observes that a point mass is itself a normalized kernel, so every
hard intervention remains inside the domain. All witness parameters lie in
`[0,1]`.

**Disposition.** `REJECTED`.

**Falsification condition.** Exhibit a local kernel that is not normalized or
an intervention whose replacement factor is not a valid point mass.

## ATTACK-09: conditioning on null events

**Attack.** Hard assignments create zero cells, so a hidden choice of
conditional-distribution version might control the response comparison.

**Response.** The passive and intervened objects are complete retained joint
mass tables. Marginalization is finite summation, and equality is literal
equality of four rational atoms. No conditional law or density representative
on a null slice is used anywhere in the category or counterexample.

**Disposition.** `REJECTED`.

**Falsification condition.** Identify a proof step that divides by a
zero-probability marginal or compares version-dependent conditionals.

## ATTACK-10: agency and ontology overreach

**Attack.** A mediator, intervention target, or reduced protocol class could be
silently identified with an autonomous agent or a physical entity.

**Response.** The contract declares mathematical presentations only. The
proofs and release explicitly exclude autonomous agency, ontological
canonicity, and physical identification. These broader statements are
recorded as open non-target claims, so the finite theorem does not depend on
them.

**Disposition.** `REJECTED` against the scoped theorem.

**Falsification condition.** Find a load-bearing premise or conclusion that
asserts autonomous agency or physical ontology.

## ATTACK-11: class count inferred only by execution

**Attack.** The fifteen-class claim might be a finite program output rather
than a mathematical derivation.

**Response.** The direct proof derives six size-three classes when `O` is
hard assigned and nine singleton classes when `O` is unassigned. Their
sizes sum to twenty-seven. Pairwise distinct identity responses separate the
fifteen displayed rows. Exact execution and serialization hashes are only
corroborative.

**Disposition.** `REJECTED`.

**Falsification condition.** Find two displayed classes with equal complete
two-sided signatures or a raw context absent from the partition.

## ATTACK-12: wrong negative-certificate quantifier

**Attack.** A single pair cannot disprove an existential target or establish a
global nonexistence theorem.

**Response.** The frozen target is a universal implication over all admitted
pairs, and its declared negative certificate kind is a counterexample. One
admitted pair satisfying the premise and falsifying the conclusion is
quantifier-matched. The release makes no existential nonexistence claim.

**Disposition.** `REJECTED`.

**Falsification condition.** Show that the frozen target is existential or
that the pair fails either domain admission, passive equality, or reduced
nonisomorphism.

## Evidence-weighted adjudication

All twelve attacks are rejected against the exact frozen target. The decisive
evidence is the direct finite derivation of well-defined reduction, literal
passive equality, complete class enumeration, and unmatched response image
under all four admitted boundary relabelings. The null-node control,
diagnostic total variation, focused test, mutation portfolio, and serialization
hashes corroborate specific boundaries but do not carry the theorem.

No attack resolves the separate open obligations concerning category
canonicity, autonomous agency, minimal realization, soft or continuous
interventions, continuum or gauge theory, VFE emergence, or informational-to-
physical identifications.
