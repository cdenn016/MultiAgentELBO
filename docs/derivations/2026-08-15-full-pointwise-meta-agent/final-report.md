<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87","schema_version":"rigorous-theory-search/v1","target_digest":"15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87"} -->
# Rigorous theory search report

## Frozen contract

The frozen mixed target is bound to SHA-256 `15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87`; neither its text nor quantifiers changed during Task 5. It is pointwise at fixed `r_*`, fixed structural `X`, and one admitted observation with a finite positive evidence representative. Its affirmative part is conditional on the declared standard-Borel, normalized common-channel, evaluator, finite-KL, and holonomy-branch premises; its five negative parts are existential finite categorical constructions.

## Terminal status

`COMPLETE_AFFIRMATIVE_WITH_CORRECTIONS`. The exact ledger/release target identifier is `target` (descriptive title: full pointwise meta-agent target), and its ledger state is `EVIDENCE_VERIFIED`. The affirmative mathematical content is unchanged; the qualifier records the certification defects in `POST-RELEASE-CORRECTIONS.md`.

## Certificate

The certificate claim is `target`. Direct mathematical support spans Task 3 (`evidence/direct-derivation.md`, SHA-256 `2aa70b07751d07712a3d9395f77817317d48d77d97c3fd5fb8cd1a3f6fda226a`) and Task 4 (`evidence/counterexample-proofs.md`, SHA-256 `59c38ed4181b2f8fbf2b573c79cb7257516c7e2d91e44dbea870c953406de6fc`), with an independent Task-5 derivation and semantic oracle erasure. A sixteen-attack adversarial pass is recorded but is **not** part of the certificate: fifteen of the sixteen dispositions are fixed by a frozen premise or an explicit non-claim, so the rejection count carries no information about the theorem (`POST-RELEASE-CORRECTIONS.md`, H2).

Of the domain reviews, two are current `APPROVE` records with Critical/High/Medium counts of zero — information/VFE `c291869ccb7d518f2df85c43f60319e59654c2769e0fdc8b07373a53430525d4` and dynamics/scope `71401ff15af3c1ce033ddbd9b01cace311f04c1eeef17a09d13b7f8125b8461b`. The other two — probability/kernel `14f7f00fdbc0a3e2f67357c249aa631eae336940f7ea99d9aad3b164f423b27e` and gauge/holonomy `431a63b06b90277ce2697d6d57a86054346564d2bb449cf11fe3673bd6fb42ba` — are `BOUND_STALE_PRE_INTEGRATION`; their approvals cover the pre-integration snapshot only (`POST-RELEASE-CORRECTIONS.md`, C1).

The provenance is non-circular in structure — three one-way snapshots, no mutual raw-hash fixed-point claim — but the first stage is **unauditable**: `review_input_snapshot` verifies 0 of its 15 entries at the `HEAD add1a69` it names, 11 being unrecoverable from the object store and 4 naming paths absent at that commit. The Fix Round 1 snapshot at `HEAD 1b18842` and the final snapshot at `HEAD 8ce6358` each verify 26 of 26 (`POST-RELEASE-CORRECTIONS.md`, H1).

## Strongest verified result

The construction supplies normalized parent generative, posterior, and recognition laws through one fixed recognition-independent Markov channel; preserves the observation marginal; proves parent posterior disintegration and absolute continuity; separates induced from explicitly compatible predeclared evaluators; derives belief, model, and posterior marginals only as forward projections; proves the additive extended-valued KL chain and the frozen finite-VFE corollary; characterizes finite zero defect and pairwise common recovery; and establishes the declared full-law covariance ("holonomy blindness") or raw-record retention branch.

Separately from the affirmative content above, and **not** to be read as part of it, five exact finite
constructions are recorded as **two-atom insufficiency witnesses** (2026-08-16 remediation, finding
L3). Each refutes a specific sufficiency claim — full-law reconstruction from marginals, unconditional
split-channel VFE, model-marginal-only evaluator compatibility, agreement from trivial holonomy, and
joint invariance from marginal invariance — and none is a substantive theorem in its own right. Two of
the five (split-channel VFE, incompatible evaluator) refute premise-deleted versions of the
affirmative theorem rather than any claim made here. `DYNAMICS-SCOPE` is separately verified as a
boundary/nonclaim.

## Dependency closure

The release closure contains `target` plus exactly seventeen transitive ancestors, all `EVIDENCE_VERIFIED`. `DYNAMICS-SCOPE` is deliberately not an ancestor because the frozen target excludes dynamics from static closure. The dependency graph is acyclic, every endpoint resolves, and every mathematical closure has direct eligible derivation evidence with the correct support polarity. The five existential negative claims remain verified by `DERIVATION` evidence with `supports: true`; no `COUNTEREXAMPLE` evidence kind is attached to those affirmative existential claim records.

## Independent reconstruction

`evidence/independent-reconstruction.md` rebuilds the closure: it begins from observation-indexed versions and finite falsifiers, isolates the evaluator disintegration, factors conditional density loss, and treats holonomy as declared branch data. It covers `target`, all seventeen ancestors, and the separate dynamics boundary. Result: `PASS` **as a second derivation**.

**The outline-independence claim is withdrawn** (2026-08-16 remediation, finding M6). This document previously asserted that the reconstruction proceeds "without using the direct proof as its outline". That claim is unsupported: once a prepended block sourced from `evidence/counterexample-proofs.md` is set aside, the section order is the direct proof's order exactly, and the order is *contingent* rather than forced — 42,636 orderings of the load-bearing steps are admissible under the actual dependency relation, so agreement on one of them is evidence of dependence, not of mathematical necessity. What the artifact supports is that the closure was derived a second time and reached the same result; it does not support that the second derivation was structurally independent of the first. A reconstruction meeting the stronger claim would have to be produced without sight of the direct proof, and that has not been done.

## Oracle erasure

`evidence/oracle-erasure.md` removes desired-conclusion cues, inspects every premise and load-bearing step for paraphrased leakage, and recomputes closure from the typed assumptions and direct evidence alone. No target conclusion is assumed through normalization, evaluator compatibility, zero defect, recovery, holonomy, canonical selection, dynamics, ontology, or gluing. Result: `PASS`.

## Unresolved obligations

None **mathematical** within the frozen target and its transitive dependency closure.

Two **certification** obligations are open, recorded in `POST-RELEASE-CORRECTIONS.md`:

1. **(C1)** Re-run `VIEW-PROBABILITY-KERNEL` and `VIEW-GAUGE-HOLONOMY` against `8ce6358` bytes and
   re-stamp. Both bind canonical `Theory/06` and `Theory/07b` bytes that were edited after they
   approved — the `Theory/07b` edit inserted `thm:rg-pointwise-parent-datum` itself — so each review's
   own post-review-mutation falsification clause is met.
2. **(H1)** Repair or replace `review_input_snapshot` in `evidence/release-provenance.json`. It
   verifies 0 of 15 entries at the `add1a69` it names; 11 are unrecoverable from the object store and
   4 name paths that did not exist at that commit.

## Scope and limitations

The certificate is a static pointwise standard-Borel theorem, not a complete geometric or physical theory. It does not establish cross-`X` sufficiency, a canonical or measurable quotient of evaluator presentations, Gaussian closure, smoothness, patchwise gluing, a canonical membership selector, a canonical coarse channel or partition, the downstream comparison theorem, a unique latent DAG, unique microscopic physics, autonomous dynamics, agency, ontology, Wheelerian feedback, nonequilibrium persistence, or physical time. Split-channel and incompatible-evaluator witnesses refute premise-deleted overreach rather than the conditional common-channel theorem. Holonomy blindness is a full-law statement under explicit action/version/evaluator hypotheses; marginal invariance is not full-law invariance, and raw retention preserves the complete joint marked record. Extended KL is additive in the nonnegative extended reals; ordinary VFE differences and recovery equivalences are asserted only on the finite tier.

Three further limitations, added by the 2026-08-16 remediation:

**Null-slice version dependence (L2).** Every displayed quantity at the admitted `o` is a property of
the *selected* posterior version, not of the conditional law as an equivalence class. When the
admitted `o` lies in a null set of the observation reference, a different admissible version changes
the fine VFE — a two-point example moves it from `log 2` to `0` while every frozen premise still
holds. The package discloses this at `evidence/direct-derivation.md:45` and dispositions it as attack
`A4`, but the limitation lists previously omitted it. Nothing is claimed about canonical null-slice
values.

**The fourth affirmative conjunct is a modeling declaration (L9).** It fixes how a parent datum is to
be *presented*, not a proposition with an independent truth value, so certifying it records that the
declaration was adopted and used consistently — it is not a verification in the sense the other
conjuncts are. The stronger charge, that the released theorem *contradicts* the contract's wording for
it, was tested and refuted.

**Prior results (L1).** The measure-theoretic and information-theoretic core of §3 and §6 restates
results already `ESTABLISHED` in this repository a week earlier; the mapping and the
Kullback–Leibler / Csiszár attribution are in `evidence/prior-results-map.md`.
