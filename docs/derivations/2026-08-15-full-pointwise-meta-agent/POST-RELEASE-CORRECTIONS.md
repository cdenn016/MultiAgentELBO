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

## What the release status now means

`terminal_status` is `COMPLETE_AFFIRMATIVE_WITH_CORRECTIONS`. The affirmative mathematical content is
unchanged and remains supported by the direct derivation, the finite witnesses, and the independent
reconstruction. The qualifier records that two of the four domain approvals are stale, that one
provenance stage is unauditable, and that the adversarial portfolio's rejection count is not evidence.

All seven Medium findings from the same review are addressed above. Six are repaired (M1–M6); M7 is
recorded rather than repaired, because repairing it means re-deriving the ledger's evidence
attachments, which is a new certification pass rather than a correction.
