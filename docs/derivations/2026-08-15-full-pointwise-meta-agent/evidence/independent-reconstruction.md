<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87","schema_version":"rigorous-theory-search/v1","target_digest":"15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87"} -->
# Independent reconstruction of the static pointwise datum

## Method and independence boundary

This pass starts from `problem-contract.json`, the atomic statements in `claim-ledger.json`, and the dependency directions in `dependency-dag.json`. It does not use `evidence/direct-derivation.md` as an outline. The reconstruction proceeds in a different order: finite falsifiers first, then normalized kernel integration, posterior pushforward, evaluator disintegration, marginal projection, conditional-KL disintegration and recovery, and finally the two holonomy semantics. Only after those steps were complete were their conclusions compared with the recorded claims and evidence hashes.

This is a sequential role-separated derivation by the Task-5 assembler, not independent-agent agreement. Four initial domain-review artifacts are now bound, but their reviewed inputs predate the correction pass and same-view bounded re-review remains a separate release gate. Accordingly, the result below supports the mathematical ancestors but does not promote `target` from `CANDIDATE` or set a terminal release status.

## Frozen closure and dynamics rationale

The static target depends on `EVALUATION-COMPATIBILITY`, `DERIVED-MARGINALS`, `VFE-FINITE-ZERO-DEFECT-RECOVERY`, `HOLONOMY-ALTERNATIVE`, and the five `NEG-*` claims. Their transitive closure adds `POINTWISE-TYPING`, `MODEL-FAMILY-NORMALIZATION`, `PARENT-NORMALIZATION`, `POSTERIOR-PUSHFORWARD`, `COMMON-CHANNEL-ABSOLUTE-CONTINUITY`, `VFE-CHAIN-EXTENDED`, `HOLONOMY-BLIND-FULL-LAW`, and `HOLONOMY-RETENTION`.

`DYNAMICS-SCOPE` is retained as a verified boundary theorem but is not a target ancestor. The exact frozen target constructs a static pointwise datum and explicitly excludes autonomy, agency, dynamics, and gluing. Requiring a dynamic special case as a dependency would silently strengthen that target. Dynamics is nevertheless reconstructed and attacked below as a scope guard.

## Finite falsifiers reconstructed first

On the binary square, the correlated law with mass one-half on `(0,0),(1,1)` and the anticorrelated law with mass one-half on `(0,1),(1,0)` have the same two fair marginals and disjoint supports. This directly proves `NEG-MARGINAL-DETERMINATION` and also supplies the dependence-changing action used by `NEG-MARGINAL-HOLONOMY-JOINT`.

For split channels, take identical fine laws `Q=Pi=Bernoulli(1/2)`, send `Q` through the identity, and send `Pi` through the constant-zero channel. Fine forward KL is zero and coarse forward KL is `+infinity`. The construction violates the common-channel premise and therefore proves exactly `NEG-SPLIT-CHANNEL-VFE`, not a defect in the common-channel theorem.

For model evaluation, use the two normalized rows `K_0(B=1)=1/4` and `K_1(B=1)=3/4` with a fair generative model marginal. The swapped evaluator `m -> K_(1-m)` disagrees at both positive-mass model points. This proves `NEG-MODEL-MARGINAL-EVALUATION` and isolates almost-sure compatibility as a necessary seam.

An identity-transport two-node tree has no nontrivial loop, yet Bernoulli `1/4` and `3/4` laws remain unequal. This proves `NEG-TRIVIAL-HOLONOMY-AGREEMENT`. Flipping the first coordinate sends the correlated joint to the anticorrelated joint while both coordinate marginals remain fair, proving `NEG-MARGINAL-HOLONOMY-JOINT`.

## Kernel integration and posterior pushforward

Fix the nonempty standard-Borel factors and form their finite product `Z_A`. Structural `X` and `X_A=chi_A(X)` are conditioning data, not random channel outputs. Let `C_A:Y_I~>Z_A` be normalized and measurable. For bounded measurable `f`, its kernel action satisfies `C_A 1=1`. Integrating `C_A` against the fixed normalized fine joint therefore gives a normalized parent joint, and testing with functions of the observation alone shows that its observation marginal is unchanged. This reconstructs `POINTWISE-TYPING` and `PARENT-NORMALIZATION`.

Let `o -> Pi_(I,o,X)` be the selected fine regular-conditional kernel. For bounded observation test `phi` and parent test `f`, substitute the fine disintegration into the parent integral and apply Tonelli. The result is the parent disintegration with kernel `o -> Pi_(I,o,X) C_A`. This proves `POSTERIOR-PUSHFORWARD` globally before selecting the admitted slice; it does not canonically determine values on fine-posterior null observations.

If a parent event has zero `Pi_I C_A` mass, its channel probability is zero `Pi_I`-almost surely. Fine `Q_I << Pi_I` transfers that zero to `Q_I`, so the parent recognition pushforward is absolutely continuous with respect to the parent posterior. This proves `COMMON-CHANNEL-ABSOLUTE-CONTINUITY`.

## Evaluator existence and compatibility

Disintegrate the pushed parent generative law into `(B_A,O,H_A)` conditional on `(M_A,Xi_A)`. Standard-Borel regularity supplies a normalized jointly measurable conditional kernel. Reading this conditional as the induced evaluator proves `MODEL-FAMILY-NORMALIZATION`, but only up to the parent `(M_A,Xi_A)` marginal's null sets. No measurable structure on an abstract kernel space, injectivity, or regular presentation quotient follows.

For a predeclared evaluator, normalization and joint measurability merely type it. Equality with the selected parent conditional must be supplied almost surely. Substitution then gives the parent generative factorization, proving the conditional predeclared tier of `EVALUATION-COMPATIBILITY`. The construction never lets generation read recognition or posterior data.

## Marginals without reconstruction

Coordinate pushforward is functorial. Applying the belief and model projections to the parent recognition law, latent generative marginal, and parent posterior yields the six recorded marginals and reconstructs `DERIVED-MARGINALS`. The correlated/anticorrelated witness above prevents inversion of those projection identities.

## Extended KL chain and finite recovery

Attach the same `C_A` to the fine recognition and posterior laws to obtain two joint laws on `Y_I x Z_A`. Their joint Radon-Nikodym derivative is the fine derivative because the conditional channel factor is identical. Disintegrating both joint laws over `z` and factoring the derivative yields the additive identity in `[0,+infinity]`: fine KL equals parent KL plus the parent-recognition average of conditional KL. All terms are nonnegative, so no subtraction of infinities occurs. Adding the same finite `-log p_X(o)` gives `VFE-CHAIN-EXTENDED`.

When fine KL is finite, every term is finite and the ordinary VFE difference equals the defect. The defect vanishes exactly when the two discarded conditional laws agree parent-recognition almost surely. That common conditional is then one normalized reverse kernel recovering both fine laws. Conversely, a single reverse kernel recovering both laws and data processing in both directions force equality of the finite fine and coarse KL values, so the defect is zero. This reconstructs `VFE-FINITE-ZERO-DEFECT-RECOVERY` only pairwise and only on the finite tier.

## Full-law holonomy alternatives

For the blindness branch, start with typed source and target groupoid actions. Covariance of fine generation, the selected posterior versions, and recognition, together with `C_A` equivariance, lets the action be moved through each defining integral. The three pushed parent laws are therefore covariant. Evaluator covariance is a separate kernel identity. Same-slice invariance follows only for isotropy arrows fixing the declared slice and versions. This reconstructs `HOLONOMY-BLIND-FULL-LAW` without inferring a regular quotient space.

For the retention branch, include roots, raw root-framed holonomy, and boundary marks as coordinates of `H_A`, and require `C_A` to emit them jointly. Full-law pushforward then retains their distributions and correlations. No averaging, conjugacy quotient, or erasure is claimed. This reconstructs `HOLONOMY-RETENTION`. A concrete parent must declare one fully typed branch, which yields `HOLONOMY-ALTERNATIVE`; neither branch selects membership.

## Static-versus-dynamic boundary

If a separate differentiable flow and moving deterministic map are declared, the ordinary chain rule gives `partial_t c_t + D c_t V_t - Vbar_t o c_t`. If Markov semigroups are declared, exact closure is semigroup intertwining. A generator identity requires a common invariant domain or core, generation hypotheses, and a uniqueness or closure theorem before it implies semigroup intertwining. These statements reconstruct `DYNAMICS-SCOPE` as a boundary only. They do not make the static datum autonomous or geometric and do not establish nonequilibrium persistence, agency, ontology, physical time, or patchwise gluing.

## Result

Every static target ancestor listed above reconstructs from the frozen premises, and all five existential negative conjuncts have direct finite derivations. The result of this sequential derivation pass is `PASS`. All four corrected-byte domain reviews are current and `APPROVE` with Critical/High/Medium counts of zero; after their final hash binding, `target` is `EVIDENCE_VERIFIED`.
