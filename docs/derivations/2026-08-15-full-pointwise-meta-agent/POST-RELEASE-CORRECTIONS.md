<!-- rigorous-theory-search-metadata {"contract_id":"contract-sha256-15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87","schema_version":"rigorous-theory-search/v1","target_digest":"15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87"} -->
# Post-release corrections

This erratum records defects found in this package's **certification apparatus** by the adversarial
review at `docs/reviews/2026-08-15-deep-review/`, and the corrections applied in response. It is
authoritative over any conflicting statement in `release.json`, `evidence/release-assembly.json`,
`evidence/release-provenance.json`, `final-report.md`, or the domain reviews.

**None of these corrections concerns the mathematics.** The review reconstructed the load-bearing
derivations independently — the channel pushforward and its posterior-version property, parent
absolute continuity, the additive extended-real KL chain with its nonnegative defect, the
unconditional zero-defect criterion, and the finite-tier recovery equivalence — and found no false
theorem. What follows are defects in what the release *claimed about its own verification*.

Because the package is hash-bound, these corrections necessarily change the bytes of the files they
touch. Every recorded SHA-256 of a corrected file is therefore stale **by design** from this point
forward. That is the intended trade: a stale hash on a corrected file is preferable to a
current hash on a false claim. The mathematical evidence artifacts
(`evidence/direct-derivation.md`, `evidence/counterexample-proofs.md`,
`evidence/finite_nongaussian_witness.py`) are **not** modified, so the hashes that bind the actual
proofs remain valid.

## C1 (Critical) — two domain approvals were stale against canonical sources edited after approval

**Finding.** `evidence/reviews/view-probability-kernel.md` and `evidence/reviews/view-gauge-holonomy.md`
bind `Theory/06_general_coarsegraining.tex` and `Theory/07b_agent_network_rg.tex` by SHA-256, and both
carry an explicit falsification clause that fires if a bound canonical source is mutated after review.
Both sources were mutated after those reviews approved. All four reviews were nonetheless stamped
`BOUND_CURRENT_APPROVE`, and the promotion of `target` to `EVIDENCE_VERIFIED` rested on those stamps.

**Verified independently** (`git show <rev>:<path> | sed 's/$/\r/' | sha256sum`):

| File | Bound in the reviews (`add1a69`) | At the released revision (`8ce6358`) |
|---|---|---|
| `Theory/06_general_coarsegraining.tex` | `4891a8f5fa86ac0f…` | `fa10620d2a1d0e51…` |
| `Theory/07b_agent_network_rg.tex` | `5eb159493ec72721…` | `268f9c3b75b09966…` |

`git diff --stat 1b18842 8ce6358 -- Theory/` is +29 on `Theory/06` and +153 on `Theory/07b`, and the
`07b` insertion is the entire `\theoremheading{Full pointwise probabilistic datum for a candidate
parent}{thm:rg-pointwise-parent-datum}` block. **The certified proposition was written into the
canonical source after the reviews that bind that source approved.**

**Scope.** Two of four reviews fire. `view-information-vfe.md` binds the same stale bytes but its
stated falsification conditions are all mathematical, so none is met. `view-dynamics-scope.md` binds
no canonical source.

**Correction applied.** `VIEW-PROBABILITY-KERNEL` and `VIEW-GAUGE-HOLONOMY` are re-stamped
`BOUND_STALE_PRE_INTEGRATION` in `evidence/release-assembly.json`; both review files carry a
post-release notice at the top; `release.json` no longer asserts four *current* approvals, its
`terminal_status` is qualified, and `unresolved_obligations` names the re-review obligation.

**What would close this properly:** re-running those two domain reviews against `8ce6358` bytes and
re-stamping. That is a new review, not a documentation change, and has **not** been done. Until it is,
the release rests on two derivation-backed views and two stale ones.

## H1 (High) — provenance snapshot 1 is unauditable

**Finding.** `evidence/release-provenance.json`'s `review_input_snapshot` names
`git_head add1a69` but binds bytes that cannot be recovered from that commit, or from anywhere in the
object store.

**Verified independently** — every recorded path resolved with `git show <rev>:<path>` and hashed both
raw and CRLF-rendered:

| Snapshot | Revision | Entries | Verify | Mismatch | Path absent |
|---|---|---|---|---|---|
| `review_input_snapshot` | `add1a69` | 15 | **0** | 11 | 4 |
| `fix_round_1_review_input_snapshot` | `1b18842` | 26 | **26** | 0 | 0 |
| `final_release_snapshot` | `8ce6358` | 26 | **26** | 0 | 0 |

Four entries — `evidence/adversarial-attacks.md`, `evidence/independent-reconstruction.md`,
`evidence/oracle-erasure.md`, `evidence/release-assembly.json` — name paths that did not exist at the
commit the snapshot claims as its `git_head`. An exhaustive search of all 1,418 blobs in the object
store, including unreachable ones, recovers 4 of the 15.

**Not affected.** Stages 2 and 3 verify completely, and `evidence/direct-derivation.md`
(`2aa70b07…`) is recoverable and byte-identical at `1b18842`, `8ce6358`, and `HEAD` — so the
mathematics any reader wants to check is obtainable. The one-way, self-excluding structure of the
non-circularity claim does hold.

**Correction applied.** Stage 1 carries an `audit_status` of `UNAUDITABLE` recording these counts.
Its hashes are retained as a historical record, not as a verifiable binding.

**Also recorded (Low):** no `fingerprint_sha256` in any of the three snapshots is reproducible,
because the package documents no construction rule for it.

## H2 (High) — the 16/16 attack-rejection rate was presented as certification evidence

**Finding.** An attack is evidence about a hypothesis only if it could have come out the other way.
Independent reclassification of all sixteen attacks found **15 of 16** whose disposition is fixed by a
frozen premise or by an explicit non-claim — both branches of the counterfactual yield `REJECTED`.
Six of those are genuine premise-essentiality tests and are real mathematics, but their *disposition*
is still invariant to whether the witness exists. A 16/16 rejection rate therefore carries no
information about whether the theorem is true. (Severity criterion: Mayo, *Statistical Inference as
Severe Testing*, CUP 2018, §1.2; Popper, *The Logic of Scientific Discovery*, §§6, 82.)

**The attacks artifact is not at fault.** `evidence/adversarial-attacks.md:4` already self-fences:

> `REJECTED` means the attack does not defeat the recorded scoped claim because a cited derivation or
> counterexample supplies the needed condition. **It does not mean the stronger shortcut is true.**

The overclaim was one file over: `evidence/release-assembly.json` carried a bare
`"attack_disposition": "REJECTED_ALL_16"` inside `final_certification_evidence`, and
`release_gate.reason` cited "all sixteen attacks are rejected" as a ground for the gate.

**Correction applied.** The `attack_disposition` field now carries the artifact's own fence and an
explicit statement that the rate is not evidence of the theorem's truth; `release_gate.reason` no
longer cites the attack count as a ground.

## Medium findings, corrected 2026-08-16

**M1 — the flagship theorem had no proof.** `thm:rg-pointwise-parent-datum` in
`Theory/07b_agent_network_rg.tex` carried `\status{ESTABLISHED}` with neither a proof nor a pointer,
which violates `Theory/SPEC.md:70` ("Proved here, or a standard result cited to a source that has been
checked"). A full proof paragraph has been written into the manuscript: normalization and the
preserved observation marginal, the bounded-test-function argument for the parent posterior version,
null-set transfer for absolute continuity, the two evaluator tiers, the marginals as coordinate
pushforwards, the chain identity via `thm:rg-exact-coarse-vfe`, the unconditional zero-defect
criterion, and the finite-tier subtraction and recovery equivalence. The argument was already present
ten lines above in the same file; only the audit trail was missing.

**M2 — "holonomy blindness" names something that is not holonomy.** The full-law alternative widened
the acting object from the based-loop transport group $\mathfrak h_I^x(r)$ of
`thm:cg-holonomy-kl-marginal` to an arbitrary typed groupoid of bimeasurable isomorphisms, and kept
the inherited name. No connection form, horizontal distribution, lift, loop, or curvature enters its
hypotheses or its proof. A scope paragraph in `Theory/07b` and a scope note on the
`HOLONOMY-BLIND-FULL-LAW` ledger claim now state that what is proved is covariance of the full parent
laws under a declared groupoid action, with same-slice invariance on the isotropy subgroup of
$(o,X)$, and that a reader should not infer connection-theoretic content from the name. The retention
alternative is unaffected: it stores literal based-holonomy representations in $\mathsf H_A$.
The theorem is true as stated; only its label oversold it.

**M3 — `solid_RG_theory.md` is named for a theory it does not contain.** Its `OPEN/TODO` list now
names the obligation in the file's own title first. There is no rescaling map, beta function, blocking
ratio, relevant/irrelevant classification, or universality statement anywhere on that page; the only
"fixed point" is the base point $r_*$; and the certified channel has no inverse-direction map, so it
admits no iterate and no flow. What exists is a composed-scale composition law and exact pointwise
coarse-graining identities — a consistent family of coarse-grainings, which is a prerequisite for an
RG semigroup and not one.

**M4 — a witness check did not test its named claim.** In
`evidence/finite_nongaussian_witness.py`, `CE4_tree_directed_KL_symbolic_half_log_3` asserted
`Fraction(3, 4) - Fraction(1, 4) == Fraction(1, 2)`, a constant expression over two literals that
never read `node_laws` and had no connection to a directed KL of $\tfrac12\log 3$. The underlying
mathematical claim is true — for $p=(p_0,p_1)$ and its swap, $\KL(p\Vert q)=(p_0-p_1)\log(p_0/p_1)$,
which is $\tfrac12\log 3$ at $(3/4,1/4)$ — but the check certified nothing. It now computes the exact
$(\text{coefficient},\text{ratio})$ log-form from `node_laws` via a new helper, canonicalized so a
direction and its reverse agree, and two further checks assert symmetry under swap and rejection of
node laws whose directed KL is not $\tfrac12\log 3$. Mutation-tested: the predicate rejects
$(2/3,1/3)$, $(7/8,1/8)$, non-swapped pairs, and degenerate masses. The check total rises from **51 to
53**, both runs still pass and agree, and `claim-ledger.json` and `view-information-vfe.md` record the
new count. `evidence/finite-nongaussian-output.json` is regenerated and its recorded hash is
consequently stale.

**M5 — the syntactic-monoid result was restated without attribution.** Reduced on review from six
theorems to exactly one: `prop:hist-operational-quotient-universal-property`
(`Theory/05d_relational_inference.tex`) is the classical syntactic congruence and syntactic monoid,
and the borrowed notation $\operatorname{Syn}(\Phi)$ was used without saying whose it is. An
attribution paragraph now cites Myhill (1957), Nerode (1958), Schützenberger (1965), Eilenberg (1976,
Ch. B.II) and Pin (1986, Ch. 2), and five bibliography entries were added to `Theory/references.bib`.
The rest of the finding failed on review and no change was made for it: seven of the eight new
`ESTABLISHED` items carry complete proofs in place, so the SPEC obligation is met, and the
circle-heat theorem is **not** a classical restatement — it is a construction with an exhibited
witness.

**M6 — the reconstruction is not outline-independent.** `final-report.md` claimed
`evidence/independent-reconstruction.md` rebuilds the closure "without using the direct proof as its
outline". Withdrawn. Once a block sourced from `counterexample-proofs.md` is set aside, the section
order is the direct proof's order exactly, and that order is contingent — 42,636 orderings of the
load-bearing steps are admissible under the actual dependency relation, so agreement on one is
evidence of dependence, not of necessity. The artifact still supports that the closure was derived a
second time and reached the same result; it does not support structural independence.

**M7 — evidence discipline regressed against the 2026-08-14 package.** Machine-reading both ledgers
confirms a difference in evidence mix between
`docs/derivations/2026-08-14-operational-intervention-extensions/` and this package. Part of the gap
is explained by subject matter: the 8/14 target is largely finite and algebraic, so exact executable
recomputation is naturally available, whereas this target is measure-theoretic on standard-Borel
spaces, where executable evidence is inherently limited to finite witnesses. That explanation does not
cover all of it. The subject-matter-independent elements — attaching every closure to a named
derivation, and keeping agent assessments out of the closure set for mathematical claims — are
available here too and were applied less consistently. Recorded, not repaired: repairing it means
re-deriving the ledger's evidence attachments, which is a new certification pass.

## Low findings, corrected 2026-08-16

**L1 — the mathematics document cites none of the theorems it re-derives.** `direct-derivation.md`
contains no `Theory/` reference, no canonical theorem label, and no `Kullback1951`/`Csiszar1967`, so
§3 and §6 read alone as first derivations. They restate `thm:cg-evidence-preserving-channel`,
`thm:cg-kl-dpi-extended`, `thm:cg-dpi-equality`, `cor:cg-pairwise-bayes-recovery`,
`cor:cg-dpi-infinite-equality-warning` and `thm:rg-exact-coarse-vfe`, all `ESTABLISHED` at commit
`bd46058` a week earlier. The section-by-section mapping and the external attribution are now in
**`evidence/prior-results-map.md`**, and `construction-or-strongest-theorem.md` points at it. The
mapping is additive rather than inline because `direct-derivation.md`'s SHA-256
`2aa70b07…` is the one binding in this package that still verifies end to end and is byte-identical
at `1b18842`, `8ce6358` and `HEAD`; editing it would destroy the third party's ability to check
exactly the derivation the domain reviews read. No priority was ever claimed: the contract's
`literature_policy` permits released repository derivations and ends "No novelty or priority claim is
made."

**L2 — three limitation lists omitted the null-slice version dependence.** Added to
`final-report.md` and `construction-or-strongest-theorem.md`. Every displayed quantity at the admitted
`o` is a property of the *selected* posterior version; when the admitted `o` is null for the
observation reference, another admissible version changes the fine VFE (a two-point example moves it
from `log 2` to `0`) with every frozen premise intact. The package already disclosed this at
`direct-derivation.md:45` and dispositioned it as attack `A4`; only the lists advertised as complete
omitted it. `direct-derivation.md` §9's own list is left unedited for the binding reason above.

**L3 — one sentence over-read the five negative witnesses.** `final-report.md`'s "strongest verified
result" paragraph listed them without a type marker. They are now stated separately and explicitly as
**two-atom insufficiency witnesses**, not substantive theorems, with the note that two of the five
refute premise-deleted versions of the affirmative theorem rather than any claim made here.

**L4 — the snapshot fingerprints are not reproducible.** No `fingerprint_sha256` in any of the three
provenance snapshots can be recomputed, because the package documents no construction rule for the
field. Each now carries a `fingerprint_note` recording that. Not repaired: inventing a rule after the
fact would not reproduce the recorded values, and the correct fix is to define the rule and
regenerate, which is a new certification pass.

**L5 — an unhedged nonreconstruction claim.** `Theory/07b` asserted flatly that "no displayed marginal
pair reconstructs any of the corresponding full laws". `prop:prob-marginals-do-not-determine-joint`
requires at least two nondegenerate coordinates and explicitly records that the conclusion fails
without it — a one-point parent space has its unique law determined by its marginals, and the
surrounding text permits that case. The sentence now carries the hypothesis and says why it is not
decorative.

**L6 — cross-`X` notation in the evaluator equation.** In the induced tier the evaluator is defined as
$K^{X_A}_{A,m_A}:=G_A^X$, built by disintegrating $\mathbb P_A(\cdot\mid X)$, so it depends on the
fine $X$; displaying it with an $X_A$ superscript reads on its face as the factorization through
$X_A$ that the limitations disclaim. The document already defuses this in the caveat at
`direct-derivation.md:190`, and nothing downstream uses a cross-`X` factorization, so the residue is
notation hygiene in a frozen artifact. Recorded here rather than edited, for the binding reason under
L1.

**L7 — the frozen contract is self-contradictory in one clause.** `/target/regularity` says "finite
terms wherever KL or VFE expressions are displayed", which contradicts `/target/statement`,
`/target/quantifiers`, the `VFE-CHAIN-EXTENDED` ledger claim, and `final-report.md`'s own scope
sentence, all of which correctly carry the extended-real chain with no finiteness premise. **The
governing reading is the extended-real one**, and the unconditional zero-defect criterion is
mathematically correct without any finiteness hypothesis. `problem-contract.json` is *not* edited:
its bytes define the target digest `15336a68…`, and changing them would break every binding in the
package. Note also that the defect runs opposite to how it was first filed — `git show --stat fe08359`
shows the commit that introduced the unconditional wording touched no package file, so the manuscript
is the corrected surface and the package's summary labels are the stale ones.

**L8 — the 0/0/0 severity counts are produced by a fix-then-count loop.** All four review slots in
`evidence/release-assembly.json` now carry an explicit `severity_count_convention` stating that counts
are findings remaining against the *corrected* bytes, that a nonzero count is therefore unreachable by
construction, and that at least one real pre-fix mathematical error is recoverable from git for this
package. The convention is defensible; leaving it undisclosed while presenting 0/0/0 as a certification
ground was not.

**L9 — the fourth affirmative conjunct is a modeling declaration.** It fixes how a parent datum is to
be presented rather than asserting a proposition with an independent truth value, so certifying it
records that the declaration was adopted and used consistently, not that anything was verified in the
sense the other conjuncts are. `final-report.md` now says so. The stronger charge — that the released
theorem *contradicts* the contract's wording for this conjunct — was tested and refuted.

## What the release status now means

`terminal_status` is `COMPLETE_AFFIRMATIVE_WITH_CORRECTIONS`. The affirmative mathematical content is
unchanged and remains supported by the direct derivation, the finite witnesses, and the independent
reconstruction. The qualifier records that two of the four domain approvals are stale, that one
provenance stage is unauditable, and that the adversarial portfolio's rejection count is not evidence.

All seven Medium findings from the same review are addressed above. Six are repaired (M1–M6); M7 is
recorded rather than repaired, because repairing it means re-deriving the ledger's evidence
attachments, which is a new certification pass rather than a correction.
