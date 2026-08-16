<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87","review_id":"VIEW-GAUGE-HOLONOMY","schema_version":"rigorous-theory-search/v1","target_digest":"15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87"} -->
# Gauge and holonomy domain review

> **POST-RELEASE CORRECTION (C1).** The canonical-source hashes bound below are the
> `add1a69` bytes. At the released revision `8ce6358`,
> `Theory/06_general_coarsegraining.tex` hashes `fa10620d2a1d0e51...` and
> `Theory/07b_agent_network_rg.tex` hashes `268f9c3b75b09966...`; the `07b` edit inserted
> `thm:rg-pointwise-parent-datum` itself. This review's post-review-mutation
> falsification clause is therefore met. **Its APPROVE applies to the pre-integration
> snapshot only and does not extend to the released revision.** It has not been re-run.
> See `../../POST-RELEASE-CORRECTIONS.md`.

## Disposition

**APPROVE `VIEW-GAUGE-HOLONOMY` for the corrected frozen nonterminal Task-5 draft.** This bounded same-view re-review found no Critical, High, or Medium defect in the separate channel-groupoid boundary, the declared joint full-law action, source/target covariance, `C_A` equivariance, evaluator intertwining, stabilizer qualification, raw-record retention, or the three finite holonomy witnesses. This domain approval supersedes the initial pre-correction review; it does not promote `target`, set a terminal release status, select membership, or certify a geometric meta-agent over a base patch.

## Frozen review identity

This re-review is bound to Git `HEAD add1a69f2b83550d13abd330c13f4b4e8e9138b9`, contract/target digest `15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87`, and the corrected frozen unstaged bytes below. The draft remains deliberately nonterminal: `claim-ledger.json:117-126` records `target` as `CANDIDATE`, while `release.json:5-12` leaves `terminal_status` and `certificate_claim` null and requires same-view re-review. The superseded initial gauge review had SHA-256 `32a9fb63cf466cbfe2bdf2f7b50fdd18b91854595ed7413cbd23b822fce578d6`.

| Artifact | SHA-256 |
|---|---|
| `docs/superpowers/specs/2026-08-15-full-pointwise-meta-agent-design.md` | `a302a046e886f0a777226d667202437a6e371eac36dbfa203e8b201131afc16f` |
| `docs/superpowers/plans/2026-08-15-full-pointwise-meta-agent.md` | `6dde35db2ae999bfdc5fb63a7058bc24ea3fcaef65cbc19733bc342fd9e5bfe7` |
| `problem-contract.json` | `ce3494750e04a421d6700c970ccbffb7f37efcde3c6998b59970ceaf49600936` |
| `dependency-dag.json` | `ac28d44546eb576fa3816282200b79ff481bd74934cacebaaab50b13dfa21246` |
| `claim-ledger.json` | `862dd55014513c4b4c0b3b2f68e1dbf17336fa1c9fce49911aa6badbfecf9129` |
| `release.json` | `b46ace5e52dea221b6ccb94946cd18ede81f3edd583f66479c0b4564bda0c91c` |
| `final-report.md` | `730c28d4ebd5eeaefe9e69069e3486daf5825037a1c51e762bbcb6ee7b86c80c` |
| `construction-or-strongest-theorem.md` | `71c563725989d8a873e72beab1e48ac960adbb34be0ebe86d3944358d73cb428` |
| `evidence/release-assembly.json` (pre-rebind envelope) | `09434008550960adf1d4fcc7daea67a3915c3f6a473afd62b81913554bcf658b` |
| `evidence/direct-derivation.md` | `2aa70b07751d07712a3d9395f77817317d48d77d97c3fd5fb8cd1a3f6fda226a` |
| `evidence/counterexample-proofs.md` | `59c38ed4181b2f8fbf2b573c79cb7257516c7e2d91e44dbea870c953406de6fc` |
| `evidence/independent-reconstruction.md` | `d25ad3b8b6f8bae07a6865f58d9b214b21b6db2ab3b723393bc60359a564500f` |
| `evidence/oracle-erasure.md` | `249e18fb17fac8ff21945866fdde3ea88c87d81a753c5fcaf5dee95f9e08dea3` |
| `evidence/adversarial-attacks.md` | `f2c6bf6899ad6215dfa8c925d85015dac89c6498aee8a8ccb832a81ba66c3caa` |
| released `2026-08-14-pointwise-meta-agent-rg/evidence/direct-derivation.md` | `7860e7cfd631352fd1f4d6dc4de72bd06383b2c02d7fd8d09cce0e8c5230e790` |
| `Theory/02_geometry.tex` | `7b988ff05118500ac2c7422c116110dd0645e0448bf402d3b0a822f5a97f4c01` |
| `Theory/06_general_coarsegraining.tex` | `4891a8f5fa86ac0fa5266381e2c67161125645034ca40395cb2e3ed1b67dc9b2` |
| `Theory/07b_agent_network_rg.tex` | `5eb159493ec727218e2eaca4cf47f3fddeb090f6e193352846ad2a43181437ca` |
| `Theory/09_coarsegraining.tex` | `7caedf0e2e5301b7f56ffeee350ccd280bda9c2119ba40d1619a5727fe161e80` |

I reread the corrected contract, design, plan, DAG/ledger, release and strongest-theorem drafts, direct derivation, counterexample proof, independent reconstruction, oracle-erasure record, adversarial attacks, release assembly, the released 2026-08-14 pointwise-RG proof, and the gauge/holonomy portions of canonical `Theory/02_geometry.tex`, `Theory/06_general_coarsegraining.tex`, `Theory/07b_agent_network_rg.tex`, and `Theory/09_coarsegraining.tex`. The argument below was reconstructed from the stated actions and kernel identities; prior claim labels and reviewer agreement were not used as proof premises.

## Corrected-byte bounded re-review

The release envelope correctly treats the initial review as pre-correction evidence: `evidence/release-assembly.json:62-68` binds its old hash with state `BOUND_INITIAL_REVIEW_REREVIEW_REQUIRED`, and `:80-85` expressly says it cannot approve the corrected draft. The envelope hash in the table is therefore the pre-rebind input reviewed here; it must change when the assembler binds this superseding review.

| Corrected seam | Independent check | Gauge/holonomy effect |
|---|---|---|
| `evidence/direct-derivation.md` Section 6 | The unstaged diff is one added and one deleted line. It replaces an imprecise nonnegativity phrase with the standard nonnegative generator `phi_0(t)=t log t-t+1` and monotone truncations. Section 7, lines 381-463, is byte-for-byte equal to `HEAD`; its LF-joined slice SHA-256 is `59b912d871704964b7a72cc5ba2b88e7b490a3fb6442633850cc85447f87f094`. | None. No groupoid action, equivariance premise, evaluator identity, stabilizer condition, retention record, branch rule, or witness changed. |
| Reviewed design | The unstaged change is confined to the dynamic-closure paragraph at lines 307-317. The holonomy phase at lines 280-302 is byte-for-byte equal to `HEAD`; its LF-joined slice SHA-256 is `53fa06797acfd73831c0e5de0d337f54d97698b33e3ad117cac0354e92d8fb72`. | None. The correction distinguishes trajectory semiconjugacy from autonomy and leaves the gauge design unchanged. |
| Ledger and strongest theorem | `claim-ledger.json:117-126` now includes `ASM-HOLONOMY-ALTERNATIVE-DECLARATION` among the target assumptions and binds initial review evidence; `:137-145` retains the same conditional holonomy claims and finite falsifiers. `construction-or-strongest-theorem.md:94` still says a concrete declaration chooses a proof branch without logical exclusivity. | No circular gauge premise is introduced. The declaration assumption selects semantics and requires the chosen branch hypotheses; it does not assume either branch conclusion or select membership. |
| Release and scope documents | `release.json:5-12`, `final-report.md:10-38`, `construction-or-strongest-theorem.md:110-116`, and `evidence/release-assembly.json:80-85` update hashes, nonterminal gates, and exclusions. The expanded nonclaims include canonical channel/partition/membership selection, the downstream comparison theorem, unique DAG or microscopic physics, autonomy, and gluing. | Scope is tightened, not enlarged. No release statement turns marginal holonomy into full-law invariance, treats trivial holonomy as agreement, or lets holonomy select membership. |
| Reconstruction, erasure, and attacks | The corrected hashes are bound above. Their gauge passages (`evidence/independent-reconstruction.md:50-54`, `evidence/oracle-erasure.md:18-20,30-36`, and attacks A9-A11 and A16 at `evidence/adversarial-attacks.md:70-92,126-132`) were independently reread against the direct formulas and finite witnesses. | They preserve the same full-law/marginal boundary, raw-record semantics, branch declaration, and membership nonclaim. |

The bounded corrections therefore do not alter any gauge/holonomy proof obligation or conclusion. They improve KL rigor, distinguish semiconjugacy from autonomy, and make release/scope boundaries more conservative.

## Domain claim ledger

| Review check | Frozen claim IDs | State in this view | Closure evidence |
|---|---|---|---|
| Separate belief/model path groupoids versus a declared joint full-law action | `POINTWISE-TYPING`, `HOLONOMY-BLIND-FULL-LAW` | `EVIDENCE_VERIFIED` | Released channelwise proof plus canonical two-associated-bundle and joint-channel typing |
| Source/target covariance and `C_A` equivariance | `PARENT-NORMALIZATION`, `POSTERIOR-PUSHFORWARD`, `HOLONOMY-BLIND-FULL-LAW` | `EVIDENCE_VERIFIED` | Direct event-level pushforward calculation below |
| Evaluator intertwining on the compatibility domain | `EVALUATION-COMPATIBILITY`, `HOLONOMY-BLIND-FULL-LAW` | `EVIDENCE_VERIFIED` | Equations (4.4), (7.5), and (7.6) with version qualification |
| Covariance versus same-slice stabilizer invariance | `HOLONOMY-BLIND-FULL-LAW` | `EVIDENCE_VERIFIED` | Source/target groupoid typing and isotropy restriction |
| Full-law versus marginal invariance | `DERIVED-MARGINALS`, `NEG-MARGINAL-HOLONOMY-JOINT` | `EVIDENCE_VERIFIED` | Projection functoriality in the decomposed action; correlated/anticorrelated counterexample to the converse |
| Root-framed holonomy and boundary-mark retention | `HOLONOMY-RETENTION` | `EVIDENCE_VERIFIED` | Joint `H_A`-coordinate pushforward matched to the released component-indexed retained state |
| Declared branch semantics and open membership selection | `HOLONOMY-ALTERNATIVE`, `target` | `EVIDENCE_VERIFIED` for the gauge conjunct only | The branch is a declared proof case, not a logical exclusive-or; membership remains an input/open selector |
| Holonomy boundary witnesses | `NEG-TRIVIAL-HOLONOMY-AGREEMENT`, `NEG-MARGINAL-HOLONOMY-JOINT` | `EVIDENCE_VERIFIED` | Direct finite categorical derivations, independently recomputed below |

The assumption records checked directly are `ASM-HOLONOMY-BLIND-DATA`, `ASM-HOLONOMY-RETENTION-DATA`, and `ASM-HOLONOMY-ALTERNATIVE-DECLARATION` at `claim-ledger.json:13-15`. The corresponding claim and falsifier records are `claim-ledger.json:137-145`. The dependency edges at `dependency-dag.json:27-32` correctly make the two conditional branch theorems prerequisites of the alternative schema; they do not require one concrete parent to satisfy both branch hypotheses.

## Independent gauge and holonomy argument

### 1. Separate channel groupoids are preserved

The released pointwise-RG theorem begins with a belief channel `x=q` and a model channel `x=m`, each with its own sample fibers, weighted support graph, reciprocal transports, path groupoid, and based holonomy (`2026-08-14-pointwise-meta-agent-rg/evidence/direct-derivation.md:6-40`). Its zero-distortion theorem is applied separately to `(beta,Omega)` and `(gamma,tilde Omega)` and yields only the typed marginal pair `(Q_q,Q_m)`, not a full joint law (`:61-104`).

This channel separation agrees with the canonical geometry. The ambient theory uses one principal bundle but two associated statistical bundles, potentially inequivalent representations, separate local frames, and two connections (`Theory/02_geometry.tex:4-11`, `:40-95`, `:282-333`). Graph links and based holonomy are channel-specific and neither channel is determined by the other (`Theory/02_geometry.tex:561-620`, `:684-720`). Thus “separate groupoids” does not mean an unannounced active product-gauge symmetry; it means separate represented belief/model path actions within the declared geometry.

The new full-law theorem does not identify those channel groupoids. It assumes an additional typed joint groupoid arrow

\[
g:(o,X)\longrightarrow(o',X')
\]

with bimeasurable actions `T_O^g`, `T_I^g`, and `T_A^g` on the complete fine and parent spaces (`evidence/direct-derivation.md:381-393`). In an application to the two marginal channels, this joint action must be declared so that its coordinate restrictions intertwine the separate represented belief and model actions. That is exactly the canonical requirement that a joint coarse channel intertwine the two represented coordinate actions (`Theory/06_general_coarsegraining.tex:491-499`). Existence or uniqueness of such a joint lift is not derived from marginal holonomy, and the theorem does not claim it. If it is unavailable, the raw-retention branch remains the safe construction. The abstraction is therefore conditional but correctly typed, not a conflation of belief and model holonomy.

### 2. Source/target action and channel equivariance imply parent covariance

Let `mu` be any source fine law, `mu'=(T_I^g)_#mu`, and suppose the source and target channels satisfy

\[
C_A'(T_I^gY,D)=C_A(Y,(T_A^g)^{-1}D).
\]

For every measurable target event `D`, direct substitution gives

\[
\begin{aligned}
[(T_A^g)_\#(\mu C_A)](D)
&=(\mu C_A)((T_A^g)^{-1}D)\\
&=\int C_A(Y,(T_A^g)^{-1}D)\,\mu(dY)\\
&=\int C_A'(T_I^gY,D)\,\mu(dY)\\
&=\int C_A'(Y',D)\,\mu'(dY')\\
&=(\mu'C_A')(D).
\end{aligned}
\]

Applying this identity to recognition and selected posterior laws proves the second and third parts of (7.5). Applying the same calculation to the joint fine generative law with the additional observation action `T_O^g` proves the first part. This verifies the source/target orientation in (7.1)-(7.5) at `evidence/direct-derivation.md:385-446`; the inverse image in (7.4) is on the correct side. Bimeasurability and groupoid-compatible composition/inversion are sufficient at this measurable tier. No smoothness, Gaussian family, global quotient, or fixed-frame identification is used.

The selected-posterior hypothesis is load bearing. Fine disintegration determines posterior kernels only almost surely, so generative covariance alone does not select covariant exceptional-slice values. Equation (7.2) explicitly requires compatible selected versions (`evidence/direct-derivation.md:401-424`), matching the canonical warning that an equivariant conditional version is an additional hypothesis (`Theory/06_general_coarsegraining.tex:497-499`).

### 3. Evaluation covariance is a separate intertwining obligation

When `T_A^g` decomposes into coordinate actions on `(B,M,Xi,H)`, the evaluator must obey

\[
(T_B^g\times T_O^g\times T_H^g)_\#
K^{X_A}_{A,m}(\xi;\cdot)
=K^{X_A'}_{A,T_M^gm}(T_\Xi^g\xi;\cdot).
\]

This is correctly typed: the left side acts on the evaluator output `(B,O,H)`, while the right side transforms both evaluator inputs `(m,xi)` and the structural label from `X_A` to `X_A'` (`evidence/direct-derivation.md:448-457`). Parent full-law covariance makes the transported old conditional a version of the target conditional. Equation (7.6), together with induced compatibility or the explicit predeclared seam (4.4), identifies that version with the target evaluator on the transported compatibility domain. Disintegration alone would not force a chosen evaluator to intertwine or choose covariant null extensions, and the draft does not claim otherwise.

This also preserves the model-law/evaluated-kernel distinction. The model coordinate action `T_M^g` acts on presentations in `M_A`; evaluation covariance says their kernels intertwine. It is not inferred from invariance of `q_A^m` or `p_A^m`, and the evaluator-mismatch witness remains applicable.

### 4. Covariance is not same-slice invariance

Equation (7.5) compares a source slice `(o,X)` with a target slice `(o',X')`. It is a covariance statement, not an assertion that one fixed law is unchanged. Same-slice invariance follows only for isotropy arrows that identify source and target spaces, fix the admitted `o` and structural `X`, and preserve the selected versions (`evidence/direct-derivation.md:459`). This is the correct stabilizer qualification.

Full-frame triviality is sufficient because the represented actions are then identities, but it is not necessary. A nonidentity action can lie in the stabilizer of a particular law. The finite bit flip `g(u)=1-u` stabilizes `Bernoulli(1/2)` (`evidence/counterexample-proofs.md:206-208`); on a full product space, the same nonidentity first-coordinate flip also stabilizes the uniform product law. Canonical Gaussian examples give the same distinction: nontrivial represented holonomy can preserve an isotropic Gaussian even when the structural fixed sector is proper (`Theory/09_coarsegraining.tex:808-832`). The draft therefore correctly separates frame triviality, state-specific stabilization, and full-law invariance.

### 5. Full-law invariance implies marginal invariance only in the forward direction

For a decomposed parent action, coordinate projections intertwine the full action with its belief/model coordinate actions. Hence

\[
\operatorname{pr}_{b\#}(T_A^g)_\#Q_A
=(T_B^g)_\#\operatorname{pr}_{b\#}Q_A,
\]

and similarly for the model coordinate. Full-law covariance or invariance therefore projects to marginal covariance or invariance. Without a coordinate decomposition, no separate marginal action is defined; the complete blindness branch already supplies the decomposition needed by evaluator identity (7.6). The draft makes no converse claim (`evidence/direct-derivation.md:448-459`).

The converse is false because marginals discard dependence. Let `R` put mass one-half on `(0,0),(1,1)` and `S` put mass one-half on `(0,1),(1,0)`. The action `T(b,m)=(1-b,m)` preserves both fair coordinate marginals but sends `R` to `S != R` (`evidence/counterexample-proofs.md:210-218`). This is an exact witness for `NEG-MARGINAL-HOLONOMY-JOINT`, not merely an analogy. It also confirms that inherited marginal stabilization `h_#q_A^x=q_A^x` cannot certify a correlated full parent law.

### 6. Raw retention preserves the simultaneous gauge datum

The released pointwise-RG proof defines, separately for each channel and each membership incidence component, a root, rooted tree transports, internal based holonomy, and dressed boundary marks. It retains the component-indexed mark law and every correlation, and it explicitly forbids collapsing disconnected components or replacing the marks by one averaged group element without another theorem (`2026-08-14-pointwise-meta-agent-rg/evidence/direct-derivation.md:251-316`). Canonical 07b gives the stronger geometric presentation: the exact datum is the simultaneous root-framed state `(root feature, H_I^x, {V_e^x})`; separately quotienting holonomies loses their orientation relative to roots and boundary legs, and a naive noncompact conjugacy quotient need not be standard Borel (`Theory/07b_agent_network_rg.tex:1618-1673`).

The current retention branch imports that content by requiring `H_A` to contain measurable component roots, the raw root-framed based-holonomy representation, and dressed boundary marks, with `C_A` outputting the complete channel-typed/component-indexed records jointly with `(B_A,M_A,Xi_A)` (`evidence/direct-derivation.md:461`). Because the full parent laws are pushforwards through this joint output, they retain the records' distributions and all correlations with the other parent coordinates. This is a joint-record statement. It does not assert invertible recovery of the entire fine state, quotient regularity, path erasure, an averaged group element, or blindness. The standard-Borel and measurability premises remain necessary for whatever concrete record encoding is chosen.

### 7. “Exactly one branch” is a declaration rule, not logical exclusivity

The target phrase “establish exactly one declared full-law holonomy alternative” is resolved by `ASM-HOLONOMY-ALTERNATIVE-DECLARATION`: a concrete proof invocation declares one semantic branch and supplies that branch's hypotheses (`claim-ledger.json:15`, `:135`). It is not a theorem that blindness and retention are mutually exclusive properties. The strongest theorem states this explicitly: the frozen target declares a branch but “does not assert logical exclusivity,” because covariance and retention can coexist at different retained coordinates or quotient levels (`construction-or-strongest-theorem.md:94`).

Accordingly, the direct proof's “either” at `evidence/direct-derivation.md:463` is a proof-case declaration. The DAG's dependence of `HOLONOMY-ALTERNATIVE` on both conditional branch theorems establishes the case schema; it does not conjoin their hypotheses for one parent. This is logically consistent.

Neither branch selects `A`. The current proof says so expressly (`evidence/direct-derivation.md:463`), the released pointwise theorem leaves a canonical partition selector open (`2026-08-14-pointwise-meta-agent-rg/evidence/direct-derivation.md:386-390`), and the canonical marginal-law theorem takes the cluster and weights as inputs (`Theory/06_general_coarsegraining.tex:643-647`). Canonical Gaussian holonomy likewise supplies a structural fixed-sector rank but no partition cost or intrinsic scale (`Theory/09_coarsegraining.tex:427-435`, `:1051-1065`). Holonomy constrains admissible parallel modes after membership is declared; it does not dynamically form the membership.

### 8. Independent recomputation of the finite holonomy witnesses

1. **Trivial holonomy without agreement.** A reciprocal identity link on a two-node tree has no nontrivial reduced loop; every closed walk cancels by backtracking, so its represented holonomy is trivial. For `P=Bernoulli(1/4)` and `Q=Bernoulli(3/4)`, identity transport changes neither law and

   \[
   \operatorname{KL}(P\Vert Q)
   =\tfrac14\log\tfrac13+\tfrac34\log3
   =\tfrac12\log3>0.
   \]

   Reversing `P,Q` gives the same value. Thus trivial holonomy is not sufficient for belief or model agreement (`counterexample-proofs.md:194-204`).

2. **Nontrivial stabilizer.** The bit flip is not the identity, but it permutes the two atoms of the fair law, so `g_#Bernoulli(1/2)=Bernoulli(1/2)` (`counterexample-proofs.md:206-208`). Thus frame triviality is not necessary for law stabilization.

3. **Invariant marginals with noninvariant dependence.** Under `T(b,m)=(1-b,m)`, the correlated atoms `(0,0),(1,1)` map to the anticorrelated atoms `(1,0),(0,1)`. Both coordinate marginals remain fair, but the joint support changes, so `T_#R=S != R` (`counterexample-proofs.md:210-218`). Thus marginal stabilization is not sufficient for full-law invariance.

All three witnesses are finite categorical laws inside the general standard-Borel theory. They do not use multivariate Gaussians; the Gaussian chapter supplies optional corroborating realizations, not the ambient definition.

## Reconstruction and adversarial-record audit

The independent reconstruction correctly treats the blindness branch as equivariant kernel integration with a separate evaluator identity and the retention branch as joint output of roots, raw holonomy, and boundary marks (`evidence/independent-reconstruction.md:50-54`). The oracle-erasure record does not smuggle parent covariance, quotient regularity, or membership selection into the premises (`evidence/oracle-erasure.md:18-20`, `:30-36`). Adversarial attacks A9-A11 target precisely the marginal/full-law, trivial-holonomy/membership, and erased-mark seams; A16 additionally rejects canonical membership/channel/partition selection, a downstream comparison theorem, and unique DAG or microscopic-physics recovery (`evidence/adversarial-attacks.md:70-92`, `:126-132`). Their responses match the direct derivations, witnesses, and frozen exclusions.

Two interpretive guards are worth preserving, but neither is a C/H/M finding. First, the abstract joint groupoid is extra application data; it is not automatically reconstructed from the separate marginal path groupoids. Second, “retains raw holonomy” means the complete simultaneous channel-typed/component-indexed root-framed record required by the retention assumption, not a list of conjugacy classes or separately averaged marks.

## Critical, High, and Medium findings

None.

No bounded mathematical repair is required by this domain view.

## Falsification conditions

This approval must be withdrawn if any of the following is exhibited for the frozen bytes:

1. A purported joint action silently identifies the separate belief and model path groupoids, uses one channel's transport as the other without a declared specialization, or invokes an active `G x G` gauge symmetry where the canonical one-principal-bundle theory supplies only separate represented coordinate actions.
2. A groupoid arrow satisfying every hypothesis in (7.1)-(7.4) for which the event-level calculation above fails and a parent generative, posterior, or recognition law is not covariant as asserted.
3. A selected posterior family used on exceptional observation slices without the explicit covariance/version hypothesis (7.2).
4. A predeclared evaluator satisfying (4.4) and (7.6) whose transported generative conditional nevertheless fails to agree on positive transformed `(M_A,Xi_A)` mass, or a claimed evaluator-covariance conclusion inferred only from a model marginal.
5. A claim of same-slice invariance for an arrow that changes `o`, `X`, source/target spaces, or selected versions, or a proof that nontrivial stabilizers are impossible despite the fair-law witness.
6. Failure of projection functoriality under the declared decomposed action, or any use of separate marginal invariance as a converse theorem for the correlated full law.
7. A retention implementation satisfying `ASM-HOLONOMY-RETENTION-DATA` that omits a declared component root, channel-typed raw based-holonomy generator, dressed boundary mark, or its joint correlation; equivalently, a record claimed retained only after quotienting, averaging, or erasing information forbidden by the branch.
8. Treating the branch declaration as a mathematical exclusive-or, requiring blindness and retention to be mutually incompatible, or using holonomy as a canonical/dynamic membership selector.
9. Any arithmetic or typing failure in the tree, bit-flip, or correlated/anticorrelated witness.
10. Mutation of any bound artifact, canonical source, assumption, or claim statement without re-review and recomputation of its SHA-256.

## Final recommendation

Bind the new hash of this superseding file as `VIEW-GAUGE-HOLONOMY`, replace the initial pre-correction review binding, and keep the draft nonterminal until the remaining required same-view reviews are present and all review hashes are adjudicated. For this domain, the corrected frozen theorem preserves separate belief/model holonomy structures, conditions full-law blindness on a separately declared joint source/target action and every required equivariance/version/evaluator seam, restricts invariance to the proper stabilizer, retains raw simultaneous holonomy data when blindness is unavailable, rejects marginal-to-joint and trivial-holonomy-to-agreement shortcuts, and leaves membership selection open. **C/H/M: none. Final disposition: APPROVE.**
