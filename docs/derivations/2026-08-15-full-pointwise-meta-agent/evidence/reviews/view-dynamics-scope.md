# Same-view bounded dynamics and scope re-review

## Review identity and disposition

- Review ID: `VIEW-DYNAMICS-SCOPE`
- Domain: dynamics, renormalization-group scope, and static-versus-dynamic claim boundaries
- Frozen source revision: `add1a69f2b83550d13abd330c13f4b4e8e9138b9`
- Target digest: `15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87`
- Superseded initial review SHA-256: `1cb45d746e0ccb59e77d9e443992a711c785912874d2c3e1de43e31946722234`
- Disposition: **APPROVE**
- Severity count: `Critical 0`, `High 0`, `Medium 0`

The corrected bytes close prior findings `M-DYN-01` through `M-DYN-03`. They preserve `DYNAMICS-SCOPE` as a verified, scope-only non-ancestor and introduce no new dynamics or scope promotion. This is an evidence-weighted judgment against the current derivations and canonical boundaries, not a vote.

## Corrected byte bindings

These SHA-256 values were recomputed from the exact corrected bytes before this re-review was written:

```text
ce3494750e04a421d6700c970ccbffb7f37efcde3c6998b59970ceaf49600936  problem-contract.json
862dd55014513c4b4c0b3b2f68e1dbf17336fa1c9fce49911aa6badbfecf9129  claim-ledger.json
ac28d44546eb576fa3816282200b79ff481bd74934cacebaaab50b13dfa21246  dependency-dag.json
b46ace5e52dea221b6ccb94946cd18ede81f3edd583f66479c0b4564bda0c91c  release.json
730c28d4ebd5eeaefe9e69069e3486daf5825037a1c51e762bbcb6ee7b86c80c  final-report.md
bfbe5238accc8adb8c5a7f6411b91c819c3c64f616b504447c02e6108d36c85c  adversarial-report.json
71c563725989d8a873e72beab1e48ac960adbb34be0ebe86d3944358d73cb428  construction-or-strongest-theorem.md
09434008550960adf1d4fcc7daea67a3915c3f6a473afd62b81913554bcf658b  evidence/release-assembly.json
2aa70b07751d07712a3d9395f77817317d48d77d97c3fd5fb8cd1a3f6fda226a  evidence/direct-derivation.md
d25ad3b8b6f8bae07a6865f58d9b214b21b6db2ab3b723393bc60359a564500f  evidence/independent-reconstruction.md
249e18fb17fac8ff21945866fdde3ea88c87d81a753c5fcaf5dee95f9e08dea3  evidence/oracle-erasure.md
f2c6bf6899ad6215dfa8c925d85015dac89c6498aee8a8ccb832a81ba66c3caa  evidence/adversarial-attacks.md
a302a046e886f0a777226d667202437a6e371eac36dbfa203e8b201131afc16f  docs/superpowers/specs/2026-08-15-full-pointwise-meta-agent-design.md
6dde35db2ae999bfdc5fb63a7058bc24ea3fcaef65cbc19733bc342fd9e5bfe7  docs/superpowers/plans/2026-08-15-full-pointwise-meta-agent.md
```

All paths through `evidence/adversarial-attacks.md` are relative to the derivation package. The design and plan paths are repository-relative. Canonical tracked sources were checked at the frozen source revision.

## Claim IDs reviewed

Primary claims: `target` and `DYNAMICS-SCOPE`.

Dependency and semantic cross-checks: `POINTWISE-TYPING`, `PARENT-NORMALIZATION`, `DERIVED-MARGINALS`, `HOLONOMY-BLIND-FULL-LAW`, `HOLONOMY-RETENTION`, `HOLONOMY-ALTERNATIVE`, `NEG-TRIVIAL-HOLONOMY-AGREEMENT`, and `NEG-MARGINAL-HOLONOMY-JOINT`.

The re-review also checked `ASM-DYNAMIC-SPECIAL-CASE`, the target closure, the scope-only release classification, the corrected independent reconstruction and oracle erasure, and attacks A2, A10, A12, A15, and A16.

## Prior-finding closure

### M-DYN-01 - CLOSED

- Corrected locations: `final-report.md:10`; `claim-ledger.json:117-124`; `release.json:6`.
- Result: every release-facing surface now uses the exact target claim ID `target`. The ledger and report consistently retain its nonterminal `CANDIDATE` state. No nonexistent alias remains.

### M-DYN-02 - CLOSED

- Corrected locations: `final-report.md:38`; `evidence/adversarial-attacks.md:126-132`; `adversarial-report.json:142-146`; `evidence/oracle-erasure.md:36`.
- Frozen boundary: `problem-contract.json:44-46,61-62`.
- Result: the final scope explicitly excludes canonical membership selection, canonical coarse-channel or partition selection, the downstream comparison theorem, and recovery of a unique latent DAG or unique microscopic physics. Corrected A16 attacks each promotion and rejects it using the supplied-channel, downstream-category, and nonidentifiability boundaries. The structured adversarial report mirrors that attack. A10 continues to distinguish holonomy from membership selection.

### M-DYN-03 - CLOSED

- Corrected location: `docs/superpowers/specs/2026-08-15-full-pointwise-meta-agent-design.md:304-324`, especially lines 315-318.
- Result: the design now says that zero defect is exact **trajectory semiconjugacy on the declared state class**. It separately requires autonomous fine and parent vector fields, a fixed coarse map or correctly typed autonomous extension, well-posed flows, and stated existence domains before autonomous closure.
- Agreement: this matches `evidence/direct-derivation.md:467-492`, `Theory/07b_agent_network_rg.tex:2444-2448`, and `solid_RG_theory.md:290-309`.

No new Critical, High, or Medium finding arose in the corrected bytes.

## Dynamics and closure verification

### Static mixed target remains static

`claim-ledger.json:117-126` defines a conditional-universal affirmative conjunct and five existential finite negative conjuncts. None requires dynamics. The target's direct dependency edges remain `dependency-dag.json:6-14`. The only dynamics edge remains `DYNAMICS-SCOPE -> PARENT-NORMALIZATION` at line 33, using the file's claim-to-dependency orientation.

A read-only mechanical traversal from `target` reached exactly the target plus its seventeen static ancestors and did not reach `DYNAMICS-SCOPE`. It also confirmed that `evidence/release-assembly.json:7-27` excludes `DYNAMICS-SCOPE` from `static_target_closure` and records it in `scope_only_claims`. The same run confirmed `target` is `CANDIDATE` and `DYNAMICS-SCOPE` is `EVIDENCE_VERIFIED`. Mechanical preflight result: `PASS`.

### Deterministic semiconjugacy remains typed only

`ASM-DYNAMIC-SPECIAL-CASE` at `claim-ledger.json:16` separately supplies the differentiable spaces, fields, and moving deterministic map. `DYNAMICS-SCOPE` at line 140 and `evidence/direct-derivation.md:465-475` state the moving-map chain-rule defect

```text
delta_t = partial_t c_t + D c_t V_t - Vbar_t o c_t.
```

The `partial_t c_t` term remains present. Zero defect means exact trajectory semiconjugacy only on the declared state class. Approximate closure still requires a norm, state class, parameter interval, defect bound, and propagation/stability argument. The corrected design no longer promotes this statement to autonomy.

### Semigroup, generator, and lumpability language remains conditional

`evidence/direct-derivation.md:477-490` defines the stochastic-channel observable lift and states exact Markov closure as `T_t U = U \overline T_t`. It obtains the generator relation only on a common invariant domain. Its converse still requires an invariant domain or core, hypotheses that both operators generate the stated semigroups, and a uniqueness or closure theorem lifting generator intertwining to semigroup intertwining. `claim-ledger.json:16,140` preserves every condition.

The package does not misapply the deterministic strong-lumpability theorem to arbitrary stochastic `C_A`. `Theory/07b_agent_network_rg.tex:1946-2025` types that theorem for a surjective Borel deterministic map and distinguishes every-initial-law strong lumpability from weak lumpability at one initial law. The reviewed draft instead uses the observable lift of `C_A` and directly requires semigroup intertwining. Canonical warnings that a general evolution family is not automatically an autonomous semigroup or spectrum remain at `Theory/07b_agent_network_rg.tex:2431-2461,2564-2580`.

## No new scope promotion

- Autonomous agency and dynamical RG remain nonclaims at `evidence/direct-derivation.md:465-498` and `construction-or-strongest-theorem.md:96-116`. The downstream program remains open in `solid_RG_theory.md:328-349,386-398` and `docs/STATUS.md:259-296`.
- Physical time remains excluded at `final-report.md:38` and `evidence/direct-derivation.md:492`. `Theory/SPEC.md:804-812,820-834` continues to separate auxiliary flow parameters, RG depth, and physical time.
- Sustained nonequilibrium and Wheelerian feedback remain open at `evidence/direct-derivation.md:492` and design lines 362-383. The worklog preserves the required mechanisms and no-double-counting obligation at `docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md:3707-3730`.
- Canonical membership and channel or partition selection remain excluded. `HOLONOMY-ALTERNATIVE` at `claim-ledger.json:139`, `evidence/direct-derivation.md:463`, and A10 keep holonomy and membership distinct; the contract, corrected A16, oracle erasure, and final report state that supplied `C_A` is not canonically selected.
- The downstream comparison theorem and recovery of a unique DAG or microscopic physics remain excluded at `problem-contract.json:46,62`, design lines 326-341, corrected A16, and `final-report.md:38`.
- Patch gluing and geometric promotion remain downstream at `problem-contract.json:44`, `evidence/independent-reconstruction.md:14,58`, A15/A16, and design lines 343-360.
- Gaussian families remain optional examples rather than ambient theory at `problem-contract.json:35,46`, `evidence/direct-derivation.md:498`, A12, and plan line 18. The executable witness remains finite categorical and non-Gaussian.

The corrected reconstruction (`evidence/independent-reconstruction.md:12-14,58-62`) and oracle-erasure pass (`evidence/oracle-erasure.md:18-20,36-42`) preserve the same boundary. The corrected attack portfolio covers supplied-channel normalization and independence, holonomy versus membership and full-law distinctions, Gaussian leakage, point-to-patch gluing, autonomy, canonical selection, comparison, and unique-physics promotion. No scope attack remains unanswered.

## Falsification conditions

This approval would be falsified by any of the following:

1. a path from `target` to `DYNAMICS-SCOPE` or inclusion of `DYNAMICS-SCOPE` in the static closure;
2. omission of `partial_t c_t` for a changing map, or promotion of zero defect beyond exact semiconjugacy on its declared state class;
3. a Markov-closure claim without semigroup intertwining, or a generator-to-semigroup converse without the recorded domain/core, generation, and uniqueness/closure hypotheses;
4. any static conclusion of autonomy, dynamical RG, physical time, sustained nonequilibrium, canonical membership/channel/partition selection, unique DAG/physics, the comparison theorem, or patchwise gluing;
5. use of holonomy triviality as a membership rule, or replacement of the general standard-Borel theorem by a Gaussian model class;
6. drift of any corrected input hash above before coordinator rebinding.

The corrected bytes close `M-DYN-01` through `M-DYN-03` and satisfy this domain view. Disposition: **APPROVE**, with `Critical 0`, `High 0`, and `Medium 0`. Coordinator rebinding of this changed review file and final release-mode validation remain procedural release steps, not open dynamics/scope findings.
