<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87","review_id":"VIEW-PROBABILITY-KERNEL","schema_version":"rigorous-theory-search/v1","target_digest":"15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87"} -->
# Probability and kernel domain review

## Corrected review-input identity

This same-view bounded re-review is bound to Git `HEAD` `add1a69f2b83550d13abd330c13f4b4e8e9138b9`, contract/target digest `15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87`, and the corrected pre-review mathematical/payload snapshot below. That input snapshot deliberately retained `target` as `CANDIDATE` and `terminal_status: null` while the four corrected-byte reviews were obtained.

The provenance is intentionally two-stage and non-circular. This review binds the corrected pre-review payload bytes listed here. Final assembly metadata may then bind this review's SHA-256 and therefore has different post-review hashes. No artifact claims an impossible mutual raw-hash fixed point.

| Artifact | SHA-256 |
|---|---|
| `problem-contract.json` | `ce3494750e04a421d6700c970ccbffb7f37efcde3c6998b59970ceaf49600936` |
| `approach-registry.json` | `787132b16d0392cfbe836e6bca6296d59d5d9914fe7426fb129a4b1ccb0eb45b` |
| `claim-ledger.json` | `862dd55014513c4b4c0b3b2f68e1dbf17336fa1c9fce49911aa6badbfecf9129` |
| `dependency-dag.json` | `ac28d44546eb576fa3816282200b79ff481bd74934cacebaaab50b13dfa21246` |
| `counterexample-register.md` | `59be1c062463bc9337c6edc34f90ab5df828a2c7b2b5247792a732d50deb2159` |
| `construction-or-strongest-theorem.md` | `71c563725989d8a873e72beab1e48ac960adbb34be0ebe86d3944358d73cb428` |
| `adversarial-report.json` | `bfbe5238accc8adb8c5a7f6411b91c819c3c64f616b504447c02e6108d36c85c` |
| `release.json` | `b46ace5e52dea221b6ccb94946cd18ede81f3edd583f66479c0b4564bda0c91c` |
| `final-report.md` | `730c28d4ebd5eeaefe9e69069e3486daf5825037a1c51e762bbcb6ee7b86c80c` |
| `evidence/direct-derivation.md` | `2aa70b07751d07712a3d9395f77817317d48d77d97c3fd5fb8cd1a3f6fda226a` |
| `evidence/counterexample-proofs.md` | `59c38ed4181b2f8fbf2b573c79cb7257516c7e2d91e44dbea870c953406de6fc` |
| `evidence/independent-reconstruction.md` | `d25ad3b8b6f8bae07a6865f58d9b214b21b6db2ab3b723393bc60359a564500f` |
| `evidence/oracle-erasure.md` | `249e18fb17fac8ff21945866fdde3ea88c87d81a753c5fcaf5dee95f9e08dea3` |
| `evidence/adversarial-attacks.md` | `f2c6bf6899ad6215dfa8c925d85015dac89c6498aee8a8ccb832a81ba66c3caa` |
| `evidence/release-assembly.json` | `09434008550960adf1d4fcc7daea67a3915c3f6a473afd62b81913554bcf658b` |
| `evidence/notation-standard.md` | `cfe662fa42a3e4aed5c55d14851604cfd24f2579c8188d7bda00f579f4be3695` |
| `evidence/finite_nongaussian_witness.py` | `204effc256fcc89d9b6cbaa80d33b88eac845b7bfe2694653b0e204eb4760b48` |
| `evidence/finite-nongaussian-output.json` | `7092ec0a0dce059c2fcfc177ec288b0b708481aa9eace7a6ee657e3a1dc21e0c` |
| `docs/superpowers/specs/2026-08-15-full-pointwise-meta-agent-design.md` | `a302a046e886f0a777226d667202437a6e371eac36dbfa203e8b201131afc16f` |
| `Theory/06_general_coarsegraining.tex` | `4891a8f5fa86ac0fa5266381e2c67161125645034ca40395cb2e3ed1b67dc9b2` |
| `Theory/07b_agent_network_rg.tex` | `5eb159493ec727218e2eaca4cf47f3fddeb090f6e193352846ad2a43181437ca` |

I read the frozen contract, DAG and corrected ledger/release/report/theorem payloads, direct derivation, counterexample proof and exact witness, independent reconstruction, oracle erasure, adversarial attacks, notation standard, all of canonical `Theory/06_general_coarsegraining.tex`, and the complete probability/kernel spans of canonical `Theory/07b_agent_network_rg.tex` (`1-204`, `1130-1912`, and `2725-2828`). No desired conclusion or prior release label was used as a premise.
## Exact claim scope

The probability/kernel view reviewed `target` and these claim IDs: `POINTWISE-TYPING`, `MODEL-FAMILY-NORMALIZATION`, `PARENT-NORMALIZATION`, `POSTERIOR-PUSHFORWARD`, `COMMON-CHANNEL-ABSOLUTE-CONTINUITY`, `EVALUATION-COMPATIBILITY`, `DERIVED-MARGINALS`, `VFE-CHAIN-EXTENDED`, `VFE-FINITE-ZERO-DEFECT-RECOVERY`, `HOLONOMY-BLIND-FULL-LAW` (law-pushforward and selected-version mechanics only), `HOLONOMY-RETENTION` (joint-record pushforward only), `HOLONOMY-ALTERNATIVE` (probability typing only), `NEG-MARGINAL-DETERMINATION`, `NEG-SPLIT-CHANNEL-VFE`, `NEG-MODEL-MARGINAL-EVALUATION`, `NEG-TRIVIAL-HOLONOMY-AGREEMENT`, and `NEG-MARGINAL-HOLONOMY-JOINT`. Gauge semantics and the information-geometric interpretation remain for their assigned views.

## Independent derivation and premise audit

1. **Spaces, versions, and evidence.** Finite products preserve the standard-Borel property, so the displayed coordinate maps are measurable and the required regular conditionals exist (`evidence/direct-derivation.md:15-23`). The proof fixes one measurable observation-indexed posterior version before evaluating an admitted slice (`evidence/direct-derivation.md:25-45`) and separately declares a sigma-finite observation reference plus one finite positive density representative reused at both scales (`evidence/direct-derivation.md:47-53`). This correctly distinguishes an everywhere-defined selected version from its almost-sure disintegration identity. The statement is pointwise at fixed structural `X`; `X_A=chi_A(X)` is external conditioning data, not a random coordinate or an output of `C_A`, and no cross-`X` factorization is inferred (`evidence/direct-derivation.md:6-6`, `75-84`).

2. **One normalized recognition-independent channel.** Pointwise normalization `C_A(Y,Z_A)=1` and kernel measurability imply `C_A 1=1` (`evidence/direct-derivation.md:77-92`). Integrating the same `C_A` against the fixed fine generative joint, selected posterior, and recognition law gives normalized parent laws; testing with functions of the observation alone preserves the observation marginal (`evidence/direct-derivation.md:96-127`). This matches the canonical channel definition and functorial normalization proof (`Theory/06_general_coarsegraining.tex:14-52`) and the inherited common-pushforward construction (`Theory/07b_agent_network_rg.tex:16-31`). The frozen premise excludes observation-, recognition-, posterior-, parameter-, and realized-observation-dependent channel selection (`problem-contract.json:53-58`); the theorem never uses a split channel.

3. **Parent posterior and absolute continuity.** Substitution of the fine disintegration into bounded observation/parent test functions gives the parent disintegration globally, while kernel composition preserves measurability in `o` (`evidence/direct-derivation.md:130-141`). This is the selected-version-qualified identity already proved canonically (`Theory/06_general_coarsegraining.tex:258-302`). If a parent event is null under `Pi_I C_A`, its channel probability is zero `Pi_I`-almost surely; `Q_I << Pi_I` transfers that null set, proving `Q_I C_A << Pi_I C_A` (`evidence/direct-derivation.md:143-147`). No pointwise equality of arbitrary null-slice versions is claimed.

4. **Evaluator seam.** Standard-Borel disintegration of the pushed generative law supplies a normalized jointly measurable conditional of `(B_A,O,H_A)` given `(M_A,Xi_A)`, unique only on the generative `(M_A,Xi_A)` marginal (`evidence/direct-derivation.md:154-190`). Treating this selected conditional as the evaluator is the induced tier. A predeclared normalized jointly measurable evaluator does not follow from disintegration and must agree with that conditional almost surely; only after this explicit premise may it be substituted (`evidence/direct-derivation.md:192-210`). The notation `M_A -> Kern(Xi_A,W_A)` is expressly an abbreviation for joint kernel measurability, so no unproved measurable structure on an abstract kernel space or presentation quotient enters the argument (`evidence/direct-derivation.md:163-172`, `210-210`).

5. **Recognition, prior, and posterior marginals.** `P_A^Z` is explicitly the observation-integrated latent marginal and is not the posterior (`evidence/direct-derivation.md:214-221`). The recognition marginals are coordinate pushforwards of `Q_A`, the prior marginals are coordinate pushforwards of `P_A^Z`, and the posterior marginals are coordinate pushforwards of `Pi_A` (`evidence/direct-derivation.md:223-244`). These are forward identities only; no marginal-to-joint reconstruction is used.

6. **Common-channel KL/recovery mechanics.** Attaching the identical channel gives joint lifts whose Radon-Nikodym derivative is the fine density (`evidence/direct-derivation.md:251-275`). Disintegrating both lifts over `z` yields the standard additive extended relative-entropy chain: fine KL equals parent KL plus the `Q_A`-average conditional KL (`evidence/direct-derivation.md:278-304`), consistent with the canonical exact VFE theorem (`Theory/07b_agent_network_rg.tex:34-66`). The line about monotone truncation is read through the canonical nonnegative generator `phi_0(t)=t log t-t+1`, which gives the extended proof without rearranging signed or infinite integrals (`Theory/06_general_coarsegraining.tex:65-82`); therefore it is not a closure gap. The same finite density representative adds to both scales (`evidence/direct-derivation.md:306-325`). On finite fine KL, zero defect is equivalent to equality of discarded conditionals `Q_A`-almost surely and hence to recovery by the selected posterior reverse kernel; conversely, one normalized reverse kernel recovering both laws and data processing in both directions force equality (`evidence/direct-derivation.md:328-379`). This is explicitly pairwise, not family-wide, matching the canonical recovery boundary (`Theory/06_general_coarsegraining.tex:124-165`).

7. **Exact finite falsifiers.** The main categorical datum has normalized Bernoulli evaluator rows, a normalized fine posterior with all atoms positive, a normalized correlated recognition law supported on `E=B`, and the deterministic common channel retaining `(B,M)` (`evidence/counterexample-proofs.md:8-83`). Direct summation gives equal parent laws, fair belief/model recognition and prior marginals, evaluator compatibility on both positive generative model atoms, fine forward KL `log(2)`, coarse KL zero, and conditional defect `log(2)` (`evidence/counterexample-proofs.md:86-136`). The correlated/anticorrelated square has equal fair coordinate marginals and distinct disjoint-support joints (`evidence/counterexample-proofs.md:138-154`). Identity versus constant-zero split channels turn fine KL zero into coarse forward KL `+infinity` and are correctly labeled outside the affirmative common-channel premise (`evidence/counterexample-proofs.md:156-172`). Swapping the two evaluator rows disagrees on both positive generative model atoms (`evidence/counterexample-proofs.md:174-190`). The identity-transport tree and first-coordinate flip give the stated agreement and joint-invariance falsifiers (`evidence/counterexample-proofs.md:192-218`). The script's 51 exact rational checks and captured output corroborate these tables, but the ledger correctly treats the direct proof, not computation, as mathematical closure (`claim-ledger.json:35-71`).

## Findings at Critical, High, or Medium severity

None.

No bounded mathematical fix remains for this view. The corrected sentence at `evidence/direct-derivation.md:286` now explicitly invokes the nonnegative generator `phi_0(t)=t log t-t+1` and its monotone truncations, rather than calling raw `t log t` pointwise nonnegative. The exact-witness script remains corroborative; `evidence/counterexample-proofs.md` supplies the mathematical derivations. Critical: 0. High: 0. Medium: 0.

## Falsification conditions

This approval is falsified for the frozen bytes if any of the following is exhibited:

- an in-domain standard-Borel datum satisfying every frozen premise for which a displayed regular conditional or the measurable parent posterior composition does not exist;
- a normalized measurable `C_A` for which the parent pushforward is not normalized, changes the untouched observation marginal, or makes `o -> Pi_(I,o,X) C_A` fail the bounded-test-function disintegration identity;
- an event null under `Pi_A` but positive under `Q_A` despite `Q_I << Pi_I` and use of the same channel;
- a pushed parent law without an induced jointly measurable conditional evaluator, or a predeclared evaluator satisfying the explicit almost-sure compatibility premise whose generative factorization nevertheless fails on positive parent mass;
- a bounded coordinate test function violating one of the six recognition/prior/posterior marginal pushforwards;
- a common-channel pair satisfying the recorded support and evidence hypotheses for which the additive relative-entropy chain or finite pairwise recovery equivalence fails;
- an arithmetic or typing failure in the finite categorical tables, including nonnormalization, failure of `Q_I << Pi_I`, unequal claimed parent laws, a split-channel coarse forward KL other than `+infinity`, or evaluator disagreement only on generative-null model values; or
- post-review mutation of any bound artifact byte, hypothesis, claim statement, or canonical source without re-review and re-hashing.

## Disposition

**APPROVE for the corrected probability-and-kernel domain after same-view bounded re-review.** The scoped standard-Borel/RCP/version assumptions, evidence-density declaration, common-channel normalization and recognition independence, structural-`X` typing, parent law/posterior/AC construction, evaluator measurability and compatibility seam, all three marginal families, finite categorical witness, and split-channel/evaluator falsifiers are mathematically supported by the corrected review-input snapshot. This is a domain-only approval: it does not by itself promote `target`, certify the information/VFE, gauge/holonomy, or dynamics/scope domains, or authorize terminal release without final coordinator binding and release-mode validation.
