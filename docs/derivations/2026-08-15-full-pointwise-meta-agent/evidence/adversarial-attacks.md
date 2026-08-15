<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87","schema_version":"rigorous-theory-search/v1","target_digest":"15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87"} -->
# Adversarial attacks on the static pointwise release

Each numbered attack begins from the frozen statement and attempts to break a load-bearing seam. `REJECTED` means the attack does not defeat the recorded scoped claim because a cited derivation or counterexample supplies the needed condition. It does not mean the stronger shortcut is true. All four corrected-byte domain reviews are current and `APPROVE` with Critical/High/Medium counts of zero. Every attack below has the final disposition `REJECTED`; no attack remains sustained or unresolved.

## A1. Nonnormalized parent construction

Attack: A purported channel may have row mass different from one, or the pushed joint may omit a normalizer, so `P_A`, `Pi_A`, or `Q_A` need not be probability laws.

Response: `direct-derivation.md` Sections 2-3 requires `C_A(Y,Z_A)=1` pointwise and tests the pushforward with the constant function one. Recognition and posterior start normalized and use the same channel. `counterexample-proofs.md` Section 1 checks a concrete deterministic common channel and normalized tables.

Disposition: `REJECTED` for `POINTWISE-TYPING`, `PARENT-NORMALIZATION`, and `MODEL-FAMILY-NORMALIZATION`. Dropping normalization is outside the frozen premises.

## A2. Observation-, recognition-, or posterior-dependent coarse channel

Attack: Choosing `C_A` after seeing `o`, `Q`, `Pi`, or recognition parameters can manufacture agreement or a zero defect and invalidate posterior pushforward.

Response: `ASM-COMMON-CHANNEL` and `direct-derivation.md` Section 2 freeze one channel on random `Y` before recognition and posterior inputs; structural `X` stays outside and the observation coordinate is unchanged. The split-channel witness in `counterexample-proofs.md` Section 3 shows that this restriction is load bearing.

Disposition: `REJECTED` for `PARENT-NORMALIZATION`, `POSTERIOR-PUSHFORWARD`, `COMMON-CHANNEL-ABSOLUTE-CONTINUITY`, `VFE-CHAIN-EXTENDED`, and `VFE-FINITE-ZERO-DEFECT-RECOVERY` under the frozen premise.

## A3. Generation reads recognition

Attack: If `P_I`, an evaluated kernel, or the induced parent conditional reads `Q_I` or `Pi_I`, the construction is circular rather than a fixed generative model.

Response: `ASM-FINE-GENERATIVE-POSTERIOR` fixes `P_I` before recognition, and the induced evaluator is selected from pushed generation alone. The predeclared evaluator is also fixed independently and must meet a separate generative compatibility seam. No recognition marginal is used to define generation.

Disposition: `REJECTED` for `PARENT-NORMALIZATION`, `MODEL-FAMILY-NORMALIZATION`, and `EVALUATION-COMPATIBILITY`. The recognition-dependent route is retired as a contract violation in `approach-registry.json`.

## A4. Null posterior versions

Attack: A regular conditional is unique only almost surely, so evaluating an arbitrary version at a selected null observation can make the pointwise theorem version dependent.

Response: `direct-derivation.md` Sections 1 and 3 first fixes a measurable observation-indexed version, proves the parent disintegration globally by bounded test functions, and then restricts to an admitted observation with a declared finite density representative. It does not claim canonical null-slice values or version independence.

Disposition: `REJECTED` for `POSTERIOR-PUSHFORWARD` and `VFE-CHAIN-EXTENDED` as version-qualified claims. Any canonical-null-version theorem remains outside scope.

## A5. Split-channel support mismatch

Attack: Different channels can map equal fine laws to coarse laws with incompatible support, so common-channel data processing and the VFE identity may fail catastrophically.

Response: `counterexample-proofs.md` Section 3 gives exactly this witness: fine KL zero becomes coarse forward KL `+infinity`. The affirmative theorem never permits split channels.

Disposition: `REJECTED` as an attack on the scoped common-channel claims and directly establishes `NEG-SPLIT-CHANNEL-VFE`.

## A6. Marginals reconstruct the full parent

Attack: The two belief/model marginals may be presented as sufficient to determine the correlated parent recognition law or generative joint.

Response: `counterexample-proofs.md` Section 2 gives correlated and anticorrelated fair joints with identical marginals and disjoint support. `direct-derivation.md` Section 5 asserts only forward coordinate projections.

Disposition: `REJECTED` for `DERIVED-MARGINALS` and directly establishes `NEG-MARGINAL-DETERMINATION`.

## A7. Incompatible or nonmeasurable evaluator

Attack: A normalized model marginal does not make an arbitrary evaluator jointly measurable or compatible with the pushed generative conditional.

Response: `direct-derivation.md` Section 4 separates an induced disintegration tier from a predeclared tier. The latter requires normalization, joint measurability, and almost-sure compatibility. `counterexample-proofs.md` Section 4 swaps the rows on both positive-mass model points.

Disposition: `REJECTED` for `MODEL-FAMILY-NORMALIZATION` and conditional `EVALUATION-COMPATIBILITY`; the witness directly establishes `NEG-MODEL-MARGINAL-EVALUATION`.

## A8. Kernel-presentation quotient regularity

Attack: Identifying model presentations with equal evaluated kernels may create a nonmeasurable, non-Hausdorff, singular, or non-smooth quotient, invalidating the parent model space.

Response: The default construction retains presentations in the declared standard-Borel `M_A`. `direct-derivation.md` Section 4 explicitly declines injectivity and every automatic quotient-regularity claim. No quotient is used in the target closure.

Disposition: `REJECTED` for `MODEL-FAMILY-NORMALIZATION` and `EVALUATION-COMPATIBILITY`. A regular quotient requires a separate theorem.

## A9. Marginal/full holonomy confusion

Attack: Separate invariance of belief and model marginals may be used as if it implied covariance or invariance of the correlated full parent law.

Response: `direct-derivation.md` Section 7 begins from full fine-law covariance, selected-version compatibility, channel equivariance, and evaluator covariance. `counterexample-proofs.md` Section 5.3 flips one coordinate, preserving both fair marginals while changing the joint.

Disposition: `REJECTED` for `HOLONOMY-BLIND-FULL-LAW` and directly establishes `NEG-MARGINAL-HOLONOMY-JOINT`.

## A10. Trivial holonomy selects agreement or membership

Attack: A tree or flat frame connection may be treated as proof that node laws agree or that a cluster is canonically selected.

Response: `counterexample-proofs.md` Section 5.1 places unequal Bernoulli laws on an identity-transport tree. Both holonomy branches explicitly leave membership selection open.

Disposition: `REJECTED` for `HOLONOMY-ALTERNATIVE` and directly establishes `NEG-TRIVIAL-HOLONOMY-AGREEMENT`.

## A11. Erased marks and lost correlations

Attack: A parent declared to retain holonomy may actually average or discard roots, raw based-holonomy records, boundary marks, or their correlations with `(B_A,M_A,Xi_A)`.

Response: `ASM-HOLONOMY-RETENTION-DATA` includes those objects as explicit `H_A` coordinates, and `C_A` outputs them jointly. Full-law pushforward retains the joint record distribution. If a construction erases them, it must instead satisfy every blindness/covariance hypothesis or decline both claims.

Disposition: `REJECTED` for `HOLONOMY-RETENTION` and `HOLONOMY-ALTERNATIVE`. No averaged-link or hidden erasure theorem is asserted.

## A12. Gaussian leakage

Attack: Gaussian parameter vectors or moment matching may silently define the ambient belief/model fibers and make the claimed theorem nongeneral.

Response: The frozen contract and `direct-derivation.md` use arbitrary normalized laws and kernels on standard-Borel spaces. The executable witness is finite categorical and explicitly non-Gaussian. Smooth, DQM, Fisher, and Gaussian tiers are excluded unless separately hypothesized.

Disposition: `REJECTED` for `POINTWISE-TYPING` and every static ancestor.

## A13. Infinity-minus-infinity and reversed KL

Attack: Writing the defect as fine KL minus coarse KL may hide `+infinity-(+infinity)`, and reversing KL may substitute a different finite value.

Response: `direct-derivation.md` Section 6 proves an additive identity in `[0,+infinity]`. Ordinary differences and pairwise recovery appear only when fine forward `KL(Q||Pi)` is finite. `counterexample-proofs.md` records reverse fine KL as infinite and never substitutes it.

Disposition: `REJECTED` for `VFE-CHAIN-EXTENDED` and `VFE-FINITE-ZERO-DEFECT-RECOVERY`.

## A14. Recovery overreach

Attack: Equality for one pair may be promoted to one parameter-independent recovery kernel for an entire experiment or family.

Response: `direct-derivation.md` Section 6 proves only pairwise common recovery on the finite tier and explicitly requires simultaneous hypotheses for a family-wide result. The Research wiki's experiment-comparison boundary agrees that one law or one divergence equality does not prove Blackwell equivalence.

Disposition: `REJECTED` for `VFE-FINITE-ZERO-DEFECT-RECOVERY`; experiment-level recovery remains open.

## A15. Cross-X and point-to-patch overreach

Attack: Because `X_A=chi_A(X)` is displayed and one point `r_*` lies in an overlap, the parent may be claimed to factor through `X_A` across structural values or glue into sections over the patch.

Response: `ASM-POINTWISE-STANDARD-BOREL` and `direct-derivation.md` Sections 1 and 9 restrict the theorem to one fixed `X` and one `r_*`. Cross-X factorization, measurable or smooth channel families, cocycles, active-set changes, rank jumps, and gluing are separate obligations.

Disposition: `REJECTED` for `POINTWISE-TYPING` and `target`. No geometric meta-agent is certified.

## A16. Autonomy, ontology, dynamics, selection, comparison, physics, agency, and gluing overreach

Attack: A normalized static pointwise datum may be called an autonomous agent, complete ontology, persistent nonequilibrium system, physical clock, or patchwise geometric meta-agent; it may also be claimed to canonically select its coarse channel or partition, supply the downstream comparison theorem, or recover a unique latent DAG or unique microscopic physics.

Response: `DYNAMICS-SCOPE` supplies only conditional chain-rule and semigroup criteria and is not a static target dependency. The theorem assumes one supplied `C_A`; it proves no canonical rule selecting a channel, partition, membership, or presentation. The comparison theorem is explicitly downstream and requires fixed parent data plus a separately declared comparison category. Category-relative observational or interventional statements do not identify a unique latent DAG or microscopic physics. `problem-contract.json`, `construction-or-strongest-theorem.md`, and `final-report.md` preserve every one of these exclusions.

Disposition: `REJECTED` for `target` and `DYNAMICS-SCOPE`. Autonomy, ontology, agency, dynamics, canonical coarse selection, the comparison theorem, unique DAG or physics recovery, and gluing are nonclaims, not consequences of the static theorem.
