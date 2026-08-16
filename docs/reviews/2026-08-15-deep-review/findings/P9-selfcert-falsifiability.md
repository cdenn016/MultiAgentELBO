# P9 — Self-Certification, Severity of Tests, and Falsifiability

STATUS: COMPLETE

**Counts:** Critical 2 · High 9 · Medium 2 · Low 1 (14 findings).
**Bottom line:** the certification is invalid as issued. Two of the three provenance snapshots bind
bytes that no longer exist anywhere, the four domain approvals satisfy their own stated falsification
condition and were carried into the release regardless, and `target` is promoted to
`EVIDENCE_VERIFIED` on evidence the package itself types as unable to close a claim. Separately, the
sixteen-attack portfolio is not a severe test: thirteen of sixteen attacks cannot fail. None of this
shows the underlying theorem is false — the mathematics I checked held — but the release is
materially stronger than what its evidence supports, and the machinery that says otherwise is
measuring its own workflow.

**Reviewer role:** philosophy of science / epistemics of verification (falsifiability, severity,
circularity, self-certification, evidence vs. confidence).

**Target revision:** `8ce635807a6ca2a388255fc996c98f7c535e5843` (branch `review/2026-08-15-deep-review`).

**Packages in scope (the 8/15 diff):**
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/` ("P15", the flagship)
- `docs/derivations/2026-08-14-operational-intervention-extensions/` ("P14", also written/extended 8/15)

## Files examined (checklist)

- [x] P15 `evidence/adversarial-attacks.md` — read in full, all sixteen classified
- [x] P15 `adversarial-report.json` — structure + `attack_summary` + sample records
- [x] P14 `evidence/adversarial-attacks.md` — read in full, all twenty-one
- [x] P15 `evidence/oracle-erasure.md` — read in full
- [x] P14 `evidence/oracle-erasure.md` — read in full
- [x] P15 `evidence/independent-reconstruction.md` vs `evidence/direct-derivation.md` — recon in full; direct proof by section headings + the diffed regions + §6 as quoted by two reviews
- [x] P14 `evidence/independent-reconstruction.md` — first 60 lines
- [x] P15 `evidence/reviews/view-dynamics-scope.md` — full
- [x] P15 `evidence/reviews/view-gauge-holonomy.md` — head + tail sampled (~110 of 200 lines)
- [x] P15 `evidence/reviews/view-information-vfe.md` — full
- [x] P15 `evidence/reviews/view-probability-kernel.md` — full
- [x] P15 `release.json`, `claim-ledger.json` (programmatically), `problem-contract.json`, `dependency-dag.json`
- [x] P14 `release.json`, `claim-ledger.json` (programmatically), `problem-contract.json`
- [x] P15 `evidence/release-provenance.json` — full, hashes recomputed
- [x] P15 `evidence/release-assembly.json` — full
- [x] `docs/change-logs/2026-08-15.md` — full
- [x] P15 `evidence/finite_nongaussian_witness.py` + output — re-executed twice, output diffed
- [x] P15 `evidence/counterexample-proofs.md` §1 — arithmetic recomputed by hand
- [x] P15 `final-report.md`, `construction-or-strongest-theorem.md` (via diff)
- [ ] P14 `evidence/recompute.py` + `recompute-output.json` — **not reached**
- [ ] P14 `evidence/prior-hard-operational-reduction-proof.md` — **not reached**

## Findings

### [Critical] Two of the three provenance snapshots bind bytes that were never committed and are now unrecoverable, so the "one-way, non-circular" chain is unauditable in principle

**Location:** `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/release-provenance.json:10-29` and `:65-108`; mirrored in `evidence/release-assembly.json:123-144` and verbatim in all four `evidence/reviews/view-*.md` tables.

**Claim as stated:**
> `"review_input_snapshot": { "snapshot_id": "corrected-pre-review-add1a69", ... "artifact_sha256": { "problem-contract.json": "ce3494750e04a421d6700c970ccbffb7f37efcde3c6998b59970ceaf49600936", ... "evidence/direct-derivation.md": "2aa70b07751d07712a3d9395f77817317d48d77d97c3fd5fb8cd1a3f6fda226a", ... } }`

and, in `release-assembly.json:125`, `"git_head": "add1a69f2b83550d13abd330c13f4b4e8e9138b9"`.

**Defect:** The snapshot is labeled with, and explicitly bound to, git HEAD `add1a69`. It does not record the bytes at `add1a69`. Every checkable entry is wrong, and the entry for the load-bearing derivation records the *post-correction* bytes that first exist two commits later.

**Evidence:** `.gitattributes` pins `docs/derivations/2026-08-15-full-pointwise-meta-agent/** text eol=lf`, so blob bytes equal working-tree bytes for this package (verified: `git show HEAD:.../problem-contract.json | sha256sum` = `e74764ab…` = `sha256sum` of the checked-out file). Recomputing the actual `add1a69` bytes:

```
$ cd "C:/Users/chris and christine/Desktop/MultiAgentELBO"
$ for f in problem-contract.json approach-registry.json claim-ledger.json dependency-dag.json \
    counterexample-register.md construction-or-strongest-theorem.md adversarial-report.json \
    release.json final-report.md evidence/direct-derivation.md; do \
    git show add1a69:"docs/derivations/2026-08-15-full-pointwise-meta-agent/$f" | sha256sum; done

43c1ca1643c183ba45f84df652de57a9775854a4f86f8bd2b4cbe7f0e6168ac1  problem-contract.json
db5cc72b943c1fbc5ec2122a7555d4e2f3577048395b63c9146976a90590befd  approach-registry.json
84d5709d83738cae9b32922f500b03b6e619f45b0fc5a6f05d0f4a8be416559f  claim-ledger.json
5a4886576b7b48d7b205cd3a5e92b9ca62fbd103391f79d78f9038e9c46a01aa  dependency-dag.json
47c5884fd495f7e19cb6e21a2d3615554f72d24a3ee57ddcddd494aa24337477  counterexample-register.md
bcaf463046ff986abf484f331aa9bc8bf9f2677b989c95b65a2c6818101ee362  construction-or-strongest-theorem.md
3073d723003a0b3827008ec8351536d5d13fd8f1c3de9ff81aa9b8096714dcca  adversarial-report.json
c5b82f049941f88cd65497afce4c518bfbd9c55acbf005fe5cd6cd239cdc6489  release.json
eaf68555b8137eab5b1b79d337c4ca575fa81e07ae616359cfb43dd12657cfb7  final-report.md
52015760e5b9ee2f07e983039d93a526a120e51753e95c650cc70303e1f3fa12  evidence/direct-derivation.md
```

Not one of these ten matches the corresponding `review_input_snapshot` entry (`ce349475…`, `787132b1…`, `862dd550…`, `ac28d445…`, `59be1c06…`, `71c56372…`, `bfbe5238…`, `b46ace5e…`, `730c28d4…`, `2aa70b07…`).

The recorded `evidence/direct-derivation.md` hash `2aa70b07…` does exist in history, but only from commit `1b18842` onward:

```
$ git log --oneline --follow -- ".../evidence/direct-derivation.md"
1b18842 docs: certify full pointwise meta-agent
22b5b36 docs: address pointwise meta-agent review
d287164 docs: derive full pointwise meta-agent
```
`add1a69` sits strictly between `22b5b36` and `1b18842`, and its committed bytes hash to `52015760…`. The package corroborates this: `construction-or-strongest-theorem.md` **as committed at `add1a69`** states verbatim "The direct derivation has SHA-256 `52015760e5b9ee2f07e983039d93a526a120e51753e95c650cc70303e1f3fa12`". Likewise `docs/superpowers/specs/2026-08-15-full-pointwise-meta-agent-design.md` (CRLF in the working tree under `* text=auto`) is recorded as `a302a046…` in both the review-input and the final snapshots, whereas the committed `add1a69` bytes hash to `226dab6e…` and only the `1b18842`/HEAD bytes hash to `a302a046…`:
```
$ git show add1a69:"…-design.md" | sed 's/$/\r/' | sha256sum   -> 226dab6e…
$ git show 1b18842:"…-design.md" | sed 's/$/\r/' | sha256sum   -> a302a046…
$ git diff --stat add1a69 HEAD -- "…-design.md"  ->  1 file changed, 7 insertions(+), 4 deletions(-)
```

Three recorded hashes (`ce349475…`, `b46ace5e…`, `862dd550…`) were searched across the last 40 revisions of the merged branch and occur in none of them.

**The reviews themselves supply the explanation, and it makes matters worse, not better.** `view-information-vfe.md:10` states: "The review input is the shared worktree at Git `HEAD add1a69…`, **plus the exact unstaged Task-5 bytes below**. Because the draft is intentionally unstaged, the Git revision alone is not its identity." `view-gauge-holonomy.md:10` likewise says "corrected frozen **unstaged** bytes below." So the stage-1 table hashes uncommitted working-tree bytes. Those bytes are gone:

```
$ cd /c/tmp/MultiAgentELBO-full-meta-agent-implementation-20260815
$ git log --oneline -1 ;  git status --short
063a5bb docs: finalize zero-defect closure wording
(clean)
$ sha256sum docs/derivations/2026-08-15-full-pointwise-meta-agent/problem-contract.json
e74764ab…   # the released value, not ce349475…
```
The originating worktree still exists and is clean at the final state. `git stash list` is empty. No commit, stash, or worktree in this repository reproduces `ce349475…`, `b46ace5e…`, `862dd550…`, `71c56372…`, `bfbe5238…`, `730c28d4…`, `59be1c06…`, `787132b1…`, `f2c6bf68…`, `d25ad3b8…`, `249e18fb…`, or `09434008…`. The same holds for the fifteen artifact hashes under `fix_round_1_review_input_snapshot` that differ from the released values.

**Why this is Critical rather than bookkeeping.** The release's central epistemic claim is provenance non-circularity: `release.json:57-62`, `release-assembly.json:145-149`, and `release-provenance.json:6-9` all argue "reviews bind corrected pre-review payload bytes; final metadata binds review hashes … no mutual raw-hash fixed point." A hash binding is evidence only because a third party can recompute it from the bytes and detect substitution. Here two of the three snapshots name bytes no third party can ever obtain, so the binding detects nothing: the tables are unfalsifiable tokens that could have been typed in any state and would look identical. What the chain actually demonstrates is internal arithmetic consistency, not that any review ever saw any particular content. The non-circularity argument therefore rests on the reader's trust in the author, which is precisely what a hash chain is supposed to make unnecessary.

Compounding this, the release-facing prose drops the "unstaged" qualifier that the reviews carry. `construction-or-strongest-theorem.md` (final) states: "The domain reviews bind the corrected pre-review mathematical/payload snapshot at Git `HEAD add1a69f2b83550d13abd330c13f4b4e8e9138b9`"; `release-assembly.json:125` records a bare `"git_head": "add1a69…"`; `view-probability-kernel.md:6` says "bound to Git `HEAD add1a69…` and the corrected pre-review mathematical/payload snapshot below." Each invites the reader to believe the snapshot is reconstructible from git. It is not, for any of the sixteen entries.

**Falsifier:** Produce any commit, stash, reflog entry, or surviving worktree in this repository whose `problem-contract.json` hashes to `ce349475…`, or any archive of the unstaged Task-5 draft. If those bytes are recoverable, the snapshots become auditable and this finding drops to Medium (mislabeling the snapshot with a git head that does not contain it).

**Fix:** Commit the review-input payload to a real (possibly throwaway) revision *before* obtaining reviews against it, and record that revision's SHA rather than a hand-maintained table; or delete the `review_input_snapshot` and `fix_round_1` tables and state honestly that the reviews and the artifacts they review were authored in the same working session with no independently recoverable pre-review state — in which case the non-circularity claim must be withdrawn, since it is not supported.

---

### [Critical] The four domain reviews satisfy their own stated falsification condition and were carried into the release anyway

**Location:** `.../evidence/reviews/view-probability-kernel.md:63-72` (falsification conditions) and `:76` (disposition); `release.json:11-56`; `release-assembly.json:67-121` (`"binding_state": "BOUND_CURRENT_APPROVE"`).

**Claim as stated:**
> "This approval is falsified for the frozen bytes if any of the following is exhibited: … post-review mutation of any bound artifact byte, hypothesis, claim statement, or canonical source without re-review and re-hashing."

and

> `"binding_state": "BOUND_CURRENT_APPROVE"`, `"reason": "… all four corrected-byte domain reviews are current APPROVE records with no Critical, High, or Medium finding."`

**Defect:** Bound artifacts and bound canonical sources mutated after the review, and no re-review at the mutated bytes is recorded. The review's own falsifier fires; the release nevertheless labels the approvals "current".

**Evidence:** The review binds `Theory/06_general_coarsegraining.tex` = `4891a8f5…` and `Theory/07b_agent_network_rg.tex` = `5eb15949…` (`view-probability-kernel.md:31-32`). `Theory/**` is `text eol=crlf` per `.gitattributes`, so:

```
$ for rev in add1a69 1b18842 HEAD; do for f in Theory/06_general_coarsegraining.tex Theory/07b_agent_network_rg.tex; do \
    git show $rev:$f | sed 's/$/\r/' | sha256sum; done; done
add1a69  4891a8f5…  Theory/06      add1a69  5eb15949…  Theory/07b
1b18842  4891a8f5…  Theory/06      1b18842  5eb15949…  Theory/07b
HEAD     fa10620d…  Theory/06      HEAD     268f9c3b…  Theory/07b
```
Both canonical sources changed after the reviews. The change to `Theory/06` is not cosmetic — it inserts a new block titled "Pointwise parent specialization" (`Theory/06_general_coarsegraining.tex`, added at former line 301+) that asserts, as `\status{ESTABLISHED}` canonical theory, exactly the posterior-pushforward identity
`P_A(Do,Dz|X) = ∫ C_A(Y,Dz) P_I(Do,DY|X)`, `Π_{A,o,X} = Π_{I,o,X} C_A`
which is the certified claim `POSTERIOR-PUSHFORWARD`. The certification's "canonical source" was amended, after the review, to contain the proposition being certified.

Within the derivation package, eight artifacts also changed between the review-input label and the release (`git diff --stat add1a69 HEAD`): `adversarial-report.json` (+314), `approach-registry.json` (+229), `claim-ledger.json` (+511), `construction-or-strongest-theorem.md` (16 lines), `counterexample-register.md` (+8), `evidence/direct-derivation.md` (1 line), `final-report.md` (20 lines), `problem-contract.json` (+9), `release.json` (62 lines). `evidence/adversarial-attacks.md` did not exist at `add1a69` at all (`git ls-tree -r --name-only add1a69 -- ".../2026-08-15-full-pointwise-meta-agent/"` returns 17 paths, none of which is `evidence/adversarial-attacks.md`, `evidence/independent-reconstruction.md`, `evidence/oracle-erasure.md`, `evidence/release-assembly.json`, or `evidence/reviews/*`).

**Falsifier:** A recorded re-review artifact dated after `8ce6358` that binds `Theory/06` = `fa10620d…` and `Theory/07b` = `268f9c3b…`. No such artifact exists in the package; the only post-commit review on record (`fix_round_1`) binds `1b18842` and returned `WITHHOLD`.

**Fix:** Re-run the four views against the released bytes and publish the resulting artifacts, or downgrade `binding_state` from `BOUND_CURRENT_APPROVE` to `STALE` and remove the reviews from the release gate's `reason`.

---

### [High] The 0/0/0 severity counts are produced by a fix-then-count loop, so they carry no information about the proof

**Location:** `.../evidence/reviews/view-probability-kernel.md:51`, `:57-59`; `release.json:17-21` etc.; `release-assembly.json:188-194`.

**Claim as stated:**
> "## Findings at Critical, High, or Medium severity — None. … Critical: 0. High: 0. Medium: 0."

**Defect:** The same document that reports zero findings also documents a defect it found and had repaired. The counting rule is "findings against the corrected bytes", which makes a nonzero count unreachable by construction: any defect found is fixed first and then counted as absent. The number is therefore a fixed point of the process, not a measurement of the proof.

**Evidence:** `view-probability-kernel.md:59` states: "The corrected sentence at `evidence/direct-derivation.md:286` **now** explicitly invokes the nonnegative generator `phi_0(t)=t log t-t+1`, **rather than calling raw `t log t` pointwise nonnegative**." That describes a real mathematical error in the pre-fix text. The pre-fix text is recoverable:

```
$ git diff add1a69 HEAD -- ".../evidence/direct-derivation.md"
-The relative-entropy chain rule, obtained by factorizing the Radon--Nikodym derivative into its
-(z)-marginal density and conditional density and applying monotone truncation to the nonnegative
-relative-entropy integrands, gives the additive identity
+The relative-entropy chain rule, obtained by … invoking the standard extended-valued chain theorem
+through the nonnegative generator (\phi_0(t)=t\log t-t+1) and its monotone truncations, rather than
+treating the raw (t\log t) integrand as pointwise nonnegative, gives the additive identity
```
The claim "the relative-entropy integrands are nonnegative" is false: `t log t ≥ −1/e`, attained at `t = 1/e`, so monotone truncation of the *raw* integrand does not justify an extended-valued additive identity without the `φ₀` shift. That is a genuine (if repairable) gap in the single most load-bearing step, `VFE-CHAIN-EXTENDED`. It was present at `add1a69`, the commit the reviews name as their input. The review nonetheless reports Medium: 0.

Note the internal inconsistency this leaves in one document: §6 (`:51`) reads the *uncorrected* sentence charitably ("The line about monotone truncation is read through the canonical nonnegative generator … therefore it is not a closure gap"), while the findings section (`:59`) says the sentence "now" contains the generator. Both cannot describe the same bytes. The review was assembled after the fix and back-dated to the pre-fix snapshot.

**Falsifier:** Show that `evidence/direct-derivation.md` at the actual bytes the reviewers saw already contained `φ₀`. It did not: `52015760…` (the `add1a69` bytes) contains the "nonnegative relative-entropy integrands" wording, and `git log -S"phi_0(t)=t\log t-t+1"` returns exactly one commit, `1b18842`, which is later.

**Fix:** Record the defect as a finding with disposition "fixed" and a nonzero pre-fix count, and state the counting rule explicitly ("counts are against post-fix bytes"). As it stands the numbers 0/0/0 should not appear in the release gate at all: they are a property of the workflow, not of the mathematics.

---

### [High] Thirteen of the sixteen adversarial attacks cannot fail, because their disposition is fixed by a frozen premise or by an explicit non-claim

**Location:** `.../evidence/adversarial-attacks.md` (all sixteen); `adversarial-report.json` `attack_summary` = `{"total":16,"rejected":16,"partially_sustained":0,"sustained":0,"unresolved":0}`.

**Claim as stated:**
> "Each numbered attack begins from the frozen statement and attempts to break a load-bearing seam. … Every attack below has the final disposition `REJECTED`; no attack remains sustained or unresolved."

**Defect:** An attack is evidence about a hypothesis only if it could have come out the other way. Mayo's severity requirement (Deborah Mayo, *Statistical Inference as Severe Testing*, CUP 2018, §1.2: a claim passes a *severe* test only if the test "would have, with high probability, produced a result that discords with C, were C false") and Popper's requirement that a test be a genuine attempt at refutation (*The Logic of Scientific Discovery*, §6, §82) both fail here for most of the portfolio. In thirteen of sixteen entries the attack proposes a scenario the frozen premises exclude by definition, or attributes to the package a claim the package explicitly disclaims. The probability that such an attack is sustained is zero whether or not the theorem is true, so a 16/16 rejection rate conveys no information about the theorem.

**Evidence — classification of all sixteen.** I read each attack and response in full and sorted by *what determines the disposition*.

| # | Title | What decides it | Could it have succeeded? |
|---|---|---|---|
| A1 | Nonnormalized parent | `ASM-COMMON-CHANNEL` requires `C_A(Y,Z_A)=1`; response's own last sentence: "Dropping normalization is outside the frozen premises." | **No** — premise-excluded |
| A2 | Channel depends on `o,Q,Π` | `ASM-COMMON-CHANNEL` freezes the channel before recognition. | **No** — premise-excluded |
| A3 | Generation reads recognition | `ASM-FINE-GENERATIVE-POSTERIOR` fixes `P_I` first. | **No** — premise-excluded |
| A4 | Null posterior versions | Real hazard (a.s.-uniqueness of RCPs). Resolved by *narrowing* the claim: "It does not claim canonical null-slice values or version independence." | **Partly** — see below |
| A5 | Split-channel support mismatch | The package's own `NEG-SPLIT-CHANNEL-VFE` witness; "The affirmative theorem never permits split channels." | **No** — attacks a disclaimed claim |
| A6 | Marginals reconstruct the parent | The package's own `NEG-MARGINAL-DETERMINATION`. | **No** — disclaimed |
| A7 | Incompatible evaluator | The package's own `NEG-MODEL-MARGINAL-EVALUATION`; compatibility is a premise. | **No** — disclaimed/premise |
| A8 | Quotient regularity | "No quotient is used in the target closure." | **No** — disclaimed |
| A9 | Marginal/full holonomy confusion | The package's own `NEG-MARGINAL-HOLONOMY-JOINT`. | **No** — disclaimed |
| A10 | Trivial holonomy ⇒ agreement | The package's own `NEG-TRIVIAL-HOLONOMY-AGREEMENT`. | **No** — disclaimed |
| A11 | Erased marks | `ASM-HOLONOMY-RETENTION-DATA` types the marks as coordinates. | **No** — definitional |
| A12 | Gaussian leakage | The contract quantifies over arbitrary standard-Borel laws. | **No** — definitional |
| A13 | `∞−∞` and reversed KL | Real hazard; correct textbook resolution (additive identity in `[0,+∞]`). | **Partly** — see below |
| A14 | Recovery overreach | "experiment-level recovery remains open." | **No** — disclaimed |
| A15 | Cross-`X`, point-to-patch | "No geometric meta-agent is certified." | **No** — disclaimed |
| A16 | Autonomy / ontology / dynamics / selection / comparison / physics / agency / gluing (eight attacks bundled as one) | Every one answered "nonclaim". | **No** — disclaimed ×8 |

Tally: **13 of 16 cannot fail** (A1–A3, A5–A12, A14–A16); **2 are genuine hazards with textbook resolutions** (A4, A13); **A16 is eight disclaimers bundled as one attack**, inflating apparent coverage without adding a test.

Even A4 and A13 are not fully severe. A13's resolution is the standard extended-valued chain rule for relative entropy (Dobrushin 1959; Csiszár 1967; see Polyanskiy–Wu, *Information Theory: From Coding to Learning*, CUP 2024, Thm 2.14 and §4.1) — a hazard whose answer is in a textbook is a low-severity test. A4 is the only entry where the attack demonstrably bit: it was answered by *weakening* the claim to a version-qualified statement. That is the right response, but recording it as `REJECTED` alongside twelve premise-excluded entries erases the difference between "the attack failed" and "the claim retreated until the attack no longer applied."

**Contrast within the same commit series.** The 8/14 package's portfolio is materially more severe. In `2026-08-14-operational-intervention-extensions/evidence/adversarial-attacks.md`, A8 answers "Response: **correct**; target erasure changes the comparison category"; A9 answers "Response: **it does**: … the old proof strategy is refuted"; A3, A12, A14, A15 each exhibit an explicit counterexample refuting a stronger reading. That package also ships `release.json` with six populated `unresolved_obligations`. The same machinery, one day earlier, produced attacks that could and did land. The 8/15 portfolio has none, which is the anomaly.

**Falsifier:** Exhibit an attack in `adversarial-attacks.md` whose disposition would have been `SUSTAINED` under some consistent reading of the frozen premises — one whose scenario the contract admits and whose refutation required new mathematics rather than citing a premise or a non-claim.

**Fix:** Retype the dispositions. `REJECTED (premise-excluded)`, `REJECTED (out of scope / non-claim)`, `SUSTAINED-AGAINST-STRONGER-READING (claim narrowed)`, and `REJECTED (new argument required)` are four different outcomes and only the last two are evidence. For this portfolio the count in those two categories is one, possibly two.

---

### [High] The attacks a hostile referee makes first are absent from the portfolio

**Location:** `.../evidence/adversarial-attacks.md`; `adversarial-report.json`; `release-assembly.json:166-183` (`"attack_disposition": "REJECTED_ALL_16"`).

**Defect:** A portfolio designed by the proof's author cannot ask the questions that would embarrass the proof's author. Four such questions are missing, and each is more dangerous to the release than any of the sixteen present.

**Missing attack I — triviality and prior art.** No attack asks whether the affirmative conjunct is a relabeling of three standard results applied in sequence. Reconstructing it: (i) a Markov kernel `C_A` pushes a normalized law to a normalized law and preserves untouched coordinates — the definition of a kernel plus Fubini–Tonelli; (ii) existence and composition of regular conditional probabilities and disintegrations on standard-Borel spaces — Kallenberg, *Foundations of Modern Probability*, 3rd ed., Thm 8.5 and Thm 6.3; (iii) the chain rule for relative entropy, `D(Q‖P) = D(Q_Z‖P_Z) + E_{Q_Z}[D(Q_{Y|Z}‖P_{Y|Z})]` in `[0,+∞]` — Dobrushin (1959), Csiszár (1967), Polyanskiy–Wu Thm 2.14. The certified "exact VFE chain identity" is (iii) applied to the joints `Q⊗C_A` and `Π⊗C_A`, using the elementary fact that a shared second factor makes the joint Radon–Nikodym derivative equal the fine one, so `D(Q̃‖P̃)=D(Q‖Π)`. The finite zero-defect/recovery equivalence is the equality case of the data-processing inequality, i.e. sufficiency in Blackwell's sense. The contract does say `"literature_policy": "… No novelty or priority claim is made."` — but the release-facing prose does not read that way: `release.json:9` is headed "strongest_result", `final-report.md:18` heads a section "Strongest verified result", and the terminal status is `COMPLETE_AFFIRMATIVE`. **The theorem is very likely true and is weaker than the certification apparatus implies.**

**Missing attack II — nonvacuity of the universal conjunct.** The affirmative conjunct is a conditional universal over data satisfying eight simultaneous premises, including `ASM-PREDECLARED-EVALUATION-COMPATIBILITY` (a predeclared evaluator agreeing a.s. with the induced conditional) together with `ASM-RECOGNITION-AC` and `ASM-EVIDENCE-REPRESENTATIVE` (finite positive evidence density at the admitted `o`). No attack asks whether that conjunction is satisfiable. If it were not, `target` would be vacuously true and `EVIDENCE_VERIFIED` a statement about the empty set. *This is covered by accident*: `evidence/counterexample-proofs.md` §1 is a valid nonvacuity witness (verified below). But nothing identifies it as such, the portfolio never raises vacuity, and the ledger files §1 under `EV-TASK4-COUNTEREXAMPLE-DERIVATIONS` — i.e. as support for the *negative* conjuncts. Coverage by accident is not coverage by design; had the premises been unsatisfiable, this portfolio would not have noticed.

**Missing attack III — the negative conjuncts refute propositions nobody asserts.** Five of the target's nine direct dependencies are existential negatives: marginals do not determine a joint; split channels break the VFE identity; a model marginal does not fix an evaluator; trivial holonomy does not force agreement; invariant marginals do not force an invariant joint. The first is the standard fact that a Fréchet class with fixed marginals contains many joints (Fréchet 1951; Sklar 1959) — the binary correlated/anticorrelated pair used here is its smallest instance. A referee asks: name a source, or a prior claim in this repository's own theory, that asserts the universal being refuted. If none exists, the negative conjunct is a scope declaration, not a result, and certifying it `EVIDENCE_VERIFIED` inflates the release. Worse, A5–A10 present the same disclaimers as *attacks the package survived*, so one trivially true lemma is counted twice: once as a verified negative conjunct, once as a rejected attack.

**Missing attack IV — self-certification.** No attack in either portfolio says: every artifact here — derivation, counterexamples, reconstruction, oracle erasure, the sixteen attacks, and all four domain reviews — was produced by one agent in one session, so their agreement is not independent and cannot raise confidence. The package acknowledges this only in a `side_conditions` string ("`AGENT_ASSESSMENT` is adjudication and attack evidence, not the mathematical derivation") and then contradicts it in the release gate, whose stated `reason` (`release-assembly.json:193`) is: "reconstruction and oracle erasure pass; all sixteen attacks are rejected; **all four corrected-byte domain reviews are current APPROVE records with no Critical, High, or Medium finding**."

**Two further omissions worth naming.** (v) Nobody asks whether the admitted-observation set is nonempty or of positive `P_I^O` measure; if the admitted `o` is a null observation, the selected version is arbitrary and the pointwise statement at that `o` constrains nothing. A4 concedes version-dependence but does not raise nullity of the admitted set, and `problem-contract.json`'s `boundary_conditions` do not require it to be non-null. (vi) Nobody attacks the only genuinely nontrivial direction of the equality criterion — that a single normalized reverse kernel `R` recovering both fine laws forces `Δ_A = 0`. A14 attacks the *family-wide* extension; the pairwise converse itself is unattacked.

**Falsifier:** Point to an entry in either `adversarial-attacks.md` that raises triviality/prior art, premise satisfiability, strawman negatives, or evidential independence. I found none; the closest is A14's "The Research wiki's experiment-comparison boundary agrees", which appeals to the same author's own knowledge base rather than a primary source.

**Fix:** Add the four attacks and answer them honestly. The honest answer to I is "the affirmative conjunct is a typed specialization of standard kernel and relative-entropy results; the contribution is the typing and the exclusion boundary, not the mathematics." The honest answer to III is "these negatives are scope declarations restating standard facts."

---

### [High] Oracle erasure is a self-report with no mechanical residue, and the release counts it as evidence

**Location:** `.../evidence/oracle-erasure.md:4-8` (method), `:40-42` (result); `claim-ledger.json` `EV-TASK5-ORACLE-ERASURE`, `kind: AGENT_ASSESSMENT`.

**Claim as stated:**
> "The audit nevertheless removes every desired-conclusion cue from the logical context, scans the frozen assumptions and load-bearing proof steps for paraphrased target dependence, and recomputes the static dependency closure from types, normalization, measurability, absolute continuity, compatibility hypotheses, and direct finite constructions alone."

and

> "`PASS`. Every static target ancestor remains derivable after semantic erasure."

**Defect:** The procedure cannot do what it claims when one agent performs both the derivation and the erasure, and it leaves nothing an outside party can check.

**Evidence.**

1. *No mechanical residue exists.* Compare the package's other two audits. The notation audit ships `notation_scan.py` (640 lines) and a 5732-line machine-readable `notation-collision-report.json`. The finite audit ships `finite_nongaussian_witness.py` and a captured `finite-nongaussian-output.json` that I re-ran and reproduced byte-identically. Oracle erasure ships a 43-line prose file. There is no erased copy of the premise set, no diff showing what was removed, no re-derivation performed against the erased text, and no script. Every sentence is an assertion by the agent that the agent's own reasoning did not depend on the conclusion.

2. *The test has no failure mode.* For erasure to be evidence, `P(erasure reports FAIL | a conclusion was smuggled into a premise)` must be high. The detection step is "scans … for paraphrased target dependence," performed by the same process that wrote the premises. If that process could not see the smuggling while writing, there is no reason it sees it while scanning; if it could see it, it would have fixed it at writing time and the scan reports PASS either way. The record has exactly this shape: the result is `PASS`, and the one place a risk is named — "The strongest potentially circular-looking clause is predeclared evaluator compatibility" (`:38`) — is resolved by pointing at the contract, which the same agent wrote.

3. *The release counts it anyway, against its own rule.* `oracle-erasure.md:42` reads: "This pass demonstrates only that no desired conclusion was smuggled into the premises; the direct and reconstructed derivations remain the mathematical evidence." Honest. The same sentence then continues: "All four corrected-byte domain reviews are current and `APPROVE` … so oracle erasure leaves no release obligation open and `target` is `EVIDENCE_VERIFIED`." The artifact that disclaims evidential force closes with the promotion.

**Is there any mechanical artifact that would survive an outside check?** One is available and was not produced: the ledger is machine-readable, so a third party could mechanically check that no claim's `assumption_ids` include an assumption whose `statement` entails the claim's `statement` — an automated premise/conclusion overlap test on frozen JSON. Nothing like this is recorded. What *is* mechanically checkable, and does hold, is the dependency traversal (see "Things that check out") — but that verifies acyclicity and closure membership, not the absence of question-begging premises, which is what erasure claims.

**Falsifier:** Produce an erased-premise artifact (the actual text with cues removed) plus a derivation performed against it, or a script that performs the paraphrase scan reproducibly. Either would make the pass checkable and this finding would drop to Low.

**Fix:** Either produce the mechanical artifact, or retype the result from `PASS` to `SELF-REPORT, NOT INDEPENDENTLY CHECKABLE` and remove it from the release gate's `reason`. Its own `side_conditions` already says "Oracle erasure is a certification audit and is not itself mathematical proof"; the gate should honor that.

---

### [High] "Independent reconstruction" is lexically fresh but structurally isomorphic to the direct proof; the release-facing outline-independence claim is unsupported

**Location:** `final-report.md:28`; `.../evidence/independent-reconstruction.md:6`, `:8`, `:62`.

**Claim as stated (release-facing, `final-report.md:28`):**
> "`evidence/independent-reconstruction.md` rebuilds the closure **without using the direct proof as its outline**: it begins from observation-indexed versions and finite falsifiers, isolates the evaluator disintegration, factors conditional density loss, and treats holonomy as declared branch data."

**Claim as stated (artifact, `:6`):**
> "It does not use `evidence/direct-derivation.md` as an outline. The reconstruction proceeds in a different order: finite falsifiers first, then normalized kernel integration, posterior pushforward, evaluator disintegration, marginal projection, conditional-KL disintegration and recovery, and finally the two holonomy semantics."

**Defect:** With the prepended block removed, the stated "different order" is the direct proof's order exactly. The prepended block is not a reordering of the direct proof at all — it is material from a *third* file (`counterexample-proofs.md`), which contains none of the affirmative closure.

**Evidence — section-by-section correspondence** (headings extracted with `grep -n "^##" ` on both files):

| `direct-derivation.md` | `independent-reconstruction.md` |
|---|---|
| — | Finite falsifiers reconstructed first *(source: `counterexample-proofs.md`, absent from the direct proof)* |
| §1 standard-Borel types + §2 single channel + §3 parent generation / posterior / AC | Kernel integration and posterior pushforward *(three sections merged; same internal order: typing → normalization → disintegration → AC)* |
| §4 Model evaluation and the compatibility seam | Evaluator existence and compatibility |
| §5 Derived marginals and their exact scope | Marginals without reconstruction |
| §6 Extended KL disintegration and finite VFE closure | Extended KL chain and finite recovery |
| §7 Full-law holonomy alternatives | Full-law holonomy alternatives *(title verbatim identical)* |
| §8 Dynamics is a typed open boundary | Static-versus-dynamic boundary |

**Quantification.** Of the load-bearing steps present in both documents — typing, channel normalization, posterior pushforward, absolute continuity, evaluator disintegration, predeclared-evaluator seam, marginal projection, joint-lift derivative, KL disintegration, zero-defect criterion, pairwise recovery, blindness branch, retention branch, dynamics boundary — **all fourteen appear in the same relative order with zero inversions**, and the merge of §1–§3 is the only change of decomposition. Each also uses the *same proof technique*: "testing with the constant function one" for normalization; bounded test functions plus Tonelli for the disintegration; transfer of channel-null events for AC; "the joint Radon–Nikodym derivative is the fine derivative because the conditional channel factor is identical" for the chain; equivariant substitution in the defining integrals for covariance. No step is proved a second way — the chain rule is not re-derived via the Donsker–Varadhan variational representation, nor via the Gelfand–Yaglom–Peres supremum over finite partitions, either of which would be an independent route.

**What is genuinely fresh: the wording.** Word-level n-gram overlap between the two files (lowercased, punctuation stripped):
```
n=4: recon 4-grams=1354, shared with direct= 57  (4.2%)
n=5: 1361 / 34  (2.5%)
n=6: 1363 / 23  (1.7%)
n=8: 1363 / 14  (1.0%)
```
and eleven of the fourteen shared 8-grams come from the identical `rigorous-theory-search-metadata` header. So this is a genuine re-expression, not copy-paste. But independence of a reconstruction is a property of its derivational route, not its prose, and by that measure the correspondence is one-to-one.

**Falsifier:** Identify one load-bearing affirmative step the reconstruction proves by a route absent from `direct-derivation.md`, or one pair of steps whose order is inverted between the two documents. I found neither.

**Mitigating fact, to the package's credit:** the artifact is honest at `:8` — "This is a sequential role-separated derivation by the Task-5 assembler, not independent-agent agreement" — and the ledger's `side_conditions` repeats it. The defect is that `final-report.md:28`, the release-facing summary a reader actually sees, drops that qualifier and asserts outline-independence. The artifact also contradicts itself: `:8` says the pass "does not promote `target` from `CANDIDATE`", while `:62` says "after their final hash binding, `target` is `EVIDENCE_VERIFIED`."

**Fix:** Change `final-report.md:28` to match the artifact: "a role-separated second pass by the same author, in the same order as the direct proof and using the same techniques; it re-expresses rather than re-routes the argument."

---

### [High] Four "independent expert views" returning 0/0/0 on a 552-line novel derivation is a fact about the reviewers, and the package's own record shows the process misses defects

**Location:** `evidence/reviews/` (four files, 552 lines total); `release.json:11-56`; `release-assembly.json:67-121`; `docs/change-logs/2026-08-15.md:35-37`.

**Claim as stated:** `release.json` binds four reviews, each `"disposition": "APPROVE"` with `"severity_counts": {"critical":0,"high":0,"medium":0}`.

**Defect:** The package's own chronology records at least three occasions where a 0/0/0 APPROVE was immediately followed by a later review that found defects in the same content. That is direct evidence that this process's detection probability at Medium-and-above is low, which is exactly what a 0/0/0 result cannot establish on its own.

**Evidence — from the package's own records.**

1. `release-provenance.json:65-107`: after the four APPROVE 0/0/0 reviews were bound, the committed Task-5 payload (`git_head 1b18842`) went to a "Fix Round 1" post-commit reviewer, which returned `"review_result": "WITHHOLD"`, `{"critical":0,"high":0,"medium":2}`, findings `M1-NOTATION-EVIDENCE-FRESHNESS` and `M2-ARTIFACT-METADATA-CONTRACT`. Two Mediums existed in bytes four expert views had just cleared at zero.

2. `docs/change-logs/2026-08-15.md:35`: "Four domain views, a structured skeptic, and an evidence-weighted adjudicator reviewed commit `fe08359…` and approved that corrected central content with Critical/High/Medium `0/0/0`." Then `:37`: "A subsequent whole-branch review at `9ddd757…` found one stale notation-appendix sentence that still attached finite fine KL to zero-defect recovery." A mathematical scope error survived a six-reviewer 0/0/0.

3. `:37` continues: "Follow-up scope and skeptic review then found that the appendix still lacked the required \(\mathbb Q_{A,o,X}\)-almost-sure qualifier and that this log had reversed the review chronology." A third round, two more findings, after two prior 0/0/0 verdicts.

4. `view-dynamics-scope.md:10` and `view-gauge-holonomy.md:10` each name a *superseded* initial review by SHA-256 (`1cb45d74…`, `32a9fb63…`) whose findings (`M-DYN-01`–`M-DYN-03`) are described as CLOSED. Those documents are not in the repository:
```
$ grep -rn "1cb45d746e0ccb59e77d9e443992a711c785912874d2c3e1de43e31946722234" .
docs/derivations/…/evidence/reviews/view-dynamics-scope.md:10     # the reference only
```
Only the approving reviews are preserved as artifacts; the rounds that found defects survive as a hash and a closure narrative. An outside reader cannot see what was found, only that it is claimed closed.

**Why the number is uninformative rather than merely unimpressive.** The counting rule makes zero the only reachable value. `view-probability-kernel.md:59` finds a defect ("rather than calling raw `t log t` pointwise nonnegative"), reports it as already corrected, and records Medium: 0. `view-information-vfe.md:36,44` finds the same defect, calls the changed text "one **load-bearing** explanatory sentence," reclassifies the repair as removing "a proof-exposition vulnerability," and records Medium: 0. Fix-then-count, or reclassify-as-exposition — either route yields zero. A metric whose value is invariant to whether a defect was found is not a measurement.

**Additional evidence that the four views are edits of earlier reviews rather than fresh passes.** `view-probability-kernel.md` contains both a reading of the *pre*-correction sentence (`:51`: "The line about monotone truncation is read through the canonical nonnegative generator … therefore it is not a closure gap") and a statement that the sentence *now* contains the generator (`:59`). Both cannot describe the same bytes.

**Falsifier:** Produce the superseded initial reviews (`1cb45d74…`, `32a9fb63…`) and any record of the reviewers' independence — separate context, no access to the author's intent. If the four views were genuinely separate passes with real prior probability of dissent, and their prior rounds' findings are preserved, the 0/0/0 becomes weak positive evidence rather than none.

**Fix:** Preserve every review round including those that found defects, and report per-round counts (`round 1: 0/0/3; round 2: 0/0/0 after repair`) rather than only the terminal round. Stop using 0/0/0 as a release gate; gate on the derivation, which the ledger's own `side_conditions` already names as the only eligible evidence.

---

### [High] The ledger closes `target` as EVIDENCE_VERIFIED using evidence the ledger itself types as ineligible

**Location:** `claim-ledger.json` `target.evidence_ids` and `evidence[*].kind`; `release-assembly.json:121`, `:188-194`; `oracle-erasure.md:42`; `independent-reconstruction.md:8`, `:62`.

**Claim as stated:**
> `release-assembly.json:193` — "**reason**: All static ancestors have eligible direct evidence; reconstruction and oracle erasure pass; all sixteen attacks are rejected; and all four corrected-byte domain reviews are current APPROVE records with no Critical, High, or Medium finding."

and, in the same file at `:121`:
> "Review agreement is adjudication and **cannot replace direct mathematical evidence**."

**Defect:** `target.evidence_ids` lists nine entries. Sorted by the ledger's own `kind` field:

*Eligible in kind (mathematical derivations):*
- `EV-TASK3-DIRECT-DERIVATION` — `DERIVATION`
- `EV-TASK4-COUNTEREXAMPLE-DERIVATIONS` — `DERIVATION`
- `EV-TASK5-INDEPENDENT-RECONSTRUCTION` — `DERIVATION` (adds nothing independent; see above)

*Ineligible under the operative protocol (LLM judgment cannot close a claim; agreement among agents is not evidence):*
- `EV-TASK5-ORACLE-ERASURE` — `AGENT_ASSESSMENT`
- `EV-TASK5-ADVERSARIAL-ATTACKS` — `AGENT_ASSESSMENT`
- `EV-TASK5-VIEW-PROBABILITY-KERNEL` — `AGENT_ASSESSMENT`
- `EV-TASK5-VIEW-INFORMATION-VFE` — `AGENT_ASSESSMENT`
- `EV-TASK5-VIEW-GAUGE-HOLONOMY` — `AGENT_ASSESSMENT`
- `EV-TASK5-VIEW-DYNAMICS-SCOPE` — `AGENT_ASSESSMENT`

Six of nine are `AGENT_ASSESSMENT`. The package agrees they cannot close a claim — each carries the `side_conditions` string "AGENT_ASSESSMENT is adjudication and attack evidence, not the mathematical derivation," and `release-assembly.json:121` says so outright. Then the release gate's stated `reason` uses them, and both certification artifacts make the promotion explicitly conditional on them:

- `oracle-erasure.md:42` — "**All four corrected-byte domain reviews are current and `APPROVE` with Critical/High/Medium counts of zero, so** oracle erasure leaves no release obligation open and `target` is `EVIDENCE_VERIFIED`."
- `independent-reconstruction.md:62` — "All four corrected-byte domain reviews are current and `APPROVE` … ; **after their final hash binding**, `target` is `EVIDENCE_VERIFIED`." — in a document that says at `:8` that this pass "does not promote `target` from `CANDIDATE`."

So the promotion from `CANDIDATE` to `EVIDENCE_VERIFIED` is carried by reviewer agreement, which the package's own rule forbids.

**Compounding freshness failure.** Under the operative protocol, evidence is fresh only for the recorded artifact revision, configuration, and inputs. The four `AGENT_ASSESSMENT` reviews record an input snapshot whose bytes are not the released bytes and are not recoverable (finding 1), and two canonical sources they bind (`Theory/06`, `Theory/07b`) demonstrably changed after the review (finding 2). Even if `AGENT_ASSESSMENT` were eligible in kind, this instance would be stale.

**What the eligible evidence can support.** The two `DERIVATION` artifacts are eligible in kind and, if their mathematics is correct (a question for the mathematical reviewers, not this one), can carry the affirmative and negative conjuncts by themselves. The two `SYMBOLIC_CHECK` artifacts are genuine mechanical evidence — I re-ran the witness and it reproduces byte-identically — and the ledger correctly declines to attach them to `target`. A defensible ledger state is therefore: `target` closed on `EV-TASK3` + `EV-TASK4` alone; the six `AGENT_ASSESSMENT` entries retained as context but excluded from closure; and `unresolved_obligations` populated with "domain reviews are bound to an unrecoverable snapshot and to two canonical sources that have since changed; re-review at released bytes outstanding."

**Falsifier:** Show that the release would still read `EVIDENCE_VERIFIED` / `COMPLETE_AFFIRMATIVE` with all six `AGENT_ASSESSMENT` entries removed. The gate's `reason` names them; `oracle-erasure.md:42` and `independent-reconstruction.md:62` condition the promotion on them; `final-report.md:14` lists them under "Certificate." Removing them removes the stated basis for promotion in all four places.

**Fix:** Drop the six `AGENT_ASSESSMENT` entries from `target.evidence_ids`, restate the gate `reason` as "closed by `EV-TASK3-DIRECT-DERIVATION` and `EV-TASK4-COUNTEREXAMPLE-DERIVATIONS`," and populate `unresolved_obligations` with the outstanding re-review.

---

### [High] The target's fourth affirmative conjunct is a modeling declaration, and the released theorem contradicts the frozen contract's wording for it

**Location:** `problem-contract.json:22` (frozen target); `claim-ledger.json` `HOLONOMY-ALTERNATIVE`; `construction-or-strongest-theorem.md` item 5 (post-review text); `view-gauge-holonomy.md` falsification condition 8.

**Claim as stated (frozen contract, `:22`):**
> "… and establish **exactly one** declared full-law holonomy alternative."

**Claim as stated (released theorem, post-review):**
> "The frozen target declares a holonomy branch; **it does not assert logical exclusivity**, because blindness and retention can coexist for different retained coordinates or quotient levels."

**Claim as stated (ledger, `HOLONOMY-ALTERNATIVE`):**
> "A concrete parent **may declare** either the fully hypothesis-backed holonomy-blind covariance branch or the raw-retention branch." Quantifier field: "For every concrete parent that declares one branch with that branch's hypotheses."

**Defect:** Two problems, either material.

*(a) The conjunct has no mathematical content under the released reading.* "A concrete parent may declare either branch, and under that branch's own hypotheses that branch's conclusions hold" is a conditional whose antecedent the modeler chooses. Nothing is established about parents in general; the statement defines what the two branches mean. Certifying it as one of four affirmative conjuncts of a verified target overstates the content of the release.

*(b) The released theorem contradicts the frozen contract text.* "Exactly one" naturally reads as a dichotomy: of the two alternatives, exactly one holds. The released theorem explicitly denies that reading, and `view-gauge-holonomy.md` falsifier 8 makes denial mandatory — the gauge approval "must be withdrawn" if anyone treats "the branch declaration as a mathematical exclusive-or." So the contract's affirmative conjunct, under its natural reading, is one the package's own reviewer requires be rejected; under the other reading it reduces to (a). The contract text is frozen and bound by `target_digest 15336a68…`, while the diverging theorem statement was edited *after* the four reviews (`construction-or-strongest-theorem.md` review-input `71c56372…` vs released `7a4fe2cf…`).

**Falsifier:** Show that "exactly one" in `problem-contract.json:22` was always intended as "exactly one branch is declared by the modeler," e.g. via a contemporaneous gloss inside the frozen contract. `problem-contract.json:50-53` (`symmetries`) describes both branches' hypotheses without disambiguating "exactly one," so the contract does not settle it.

**Fix:** Amend the frozen target to "establish the conclusions of whichever declared full-law holonomy alternative a concrete parent adopts; the two are not asserted to be exclusive," recompute `target_digest`, and re-run the reviews against the amended contract. As frozen, the certificate certifies a sentence the theorem does not prove under its natural reading.

---

### [Medium] The released target is falsifiable, but the contract's falsification criterion makes non-derivation unscorable by construction

**Location:** `problem-contract.json:73`; `claim-ledger.json` `target.falsifier`.

**Claim as stated:**
> "Each direct finite categorical witness within the stated types establishes its existential negative conjunct by refuting the corresponding universal overreach. An affirmative conjunct is falsified only by an in-domain datum satisfying every frozen premise but violating a stated affirmative conclusion. **Inability to derive the affirmative construction leaves that conjunct unresolved.**"

**The one-sentence falsifier, as the mandate requires.** The released target is falsified by exhibiting a single standard-Borel datum `(Y_I, B_A, M_A, Ξ_A, H_A, X, o, P_I, Π_{I,o,X}, Q_{I,o,X}, C_A, ev_A)` in which `C_A` is a normalized Markov kernel on `Y_I` alone (independent of `o, Q, Π`), `Q_{I,o,X} ≪ Π_{I,o,X}`, the evidence density at `o` is finite and positive, and the predeclared evaluator agrees almost surely with the induced conditional — yet one of the following fails: `Π_{I,o,X}C_A` is a version of the parent posterior; `Q_{I,o,X}C_A ≪ Π_{I,o,X}C_A`; or `D(Q_I‖Π_I) = D(Q_A‖Π_A) + E_{Q_A}[D(Q̃(·|z)‖Π̃(·|z))]`. So the target **is** falsifiable, and I do not raise a High finding on that score.

**Defect:** The final clause makes the release's strength asymmetric in a way the certification does not disclose. Under this criterion a proof failure never counts against the target; only a counterexample does. Combined with (i) each affirmative conclusion following from its premises by a standard theorem (see the triviality attack) and (ii) the premises being author-chosen, the affirmative conjunct is arranged so the only realistic falsification route — "the proof does not go through" — is defined out of the scoring. That is the certification analogue of an unrejectable null: logically two-sided, operationally one-sided.

The negative conjuncts are in better shape: each is an existential with an explicit finite witness whose arithmetic is checkable, and each is falsified by an arithmetic error in that witness. Those falsifiers are real; I checked one (below).

**Falsifier:** Show that the release records "affirmative conjunct not derivable" as a possible terminal outcome with consequences for the certificate. No artifact states what the terminal status would have been in that case.

**Fix:** State the asymmetry in `final-report.md`: "the affirmative conjunct is a conditional whose conclusions follow from its premises by standard kernel and relative-entropy theorems; the release's content is the typing and the exclusion boundary, not an unexpected mathematical fact."

---

### [Medium] `unresolved_obligations: []` is scope-relative in the 8/15 package and outcome-relative in the 8/14 package released alongside it

**Location:** `2026-08-15-full-pointwise-meta-agent/release.json:10`; `2026-08-14-operational-intervention-extensions/release.json:10-17`; `final-report.md:34-36`.

**Claim as stated:** P15 — `"unresolved_obligations": []`. P14, same schema, same 8/15 diff — six populated entries, including "Point interventions inferred from observational conditionals require controlled pointwise versions" and "Fixed-observation ELBO, posterior, factorization, agency, gauge/RG, continuum, and ontology claims require separate contracts and evidence."

**Defect:** P15's empty list is defensible on its own terms — `final-report.md:36` glosses it as "None **within the frozen target and its transitive dependency closure**," and the package tracks a long open list elsewhere (`docs/change-logs/2026-08-15.md:43` lists comparison category, patchwise gluing, bundle transitions, coupled dynamics, semiconjugacy, nonequilibrium, agency, continuum limits, physical time, unique physics, ontology as OPEN). But P14 populates the same field with items that are *also* outside its frozen closure (its obligation 6 explicitly says "require separate contracts and evidence"). Two releases in the same commit series use the field with different semantics, and a reader comparing them will read P15 as the cleaner result when the difference is bookkeeping. Since `unresolved_obligations: []` is one of the three headline self-certifications, this matters.

**Falsifier:** Show that every P14 obligation lies inside P14's transitive closure while every P15 open item lies outside P15's. P14's obligation 6 is by construction outside its closure, so the semantics differ.

**Fix:** Fix the field's meaning in the schema — either "open within closure" or "open downstream" — and apply it to both packages. If the former, P15's `[]` should be accompanied by the downstream OPEN list in the release JSON, not only in a change log.

---

### [Low] "No unresolved obligations", "16/16 rejected", and "0/0/0 ×4" are three restatements of one fact, presented as three independent confirmations

**Location:** `release.json:9-10`; `release-assembly.json:188-194`; `final-report.md:12-16`, `:34-36`; `construction-or-strongest-theorem.md` "Final release status".

**Defect:** The three headline numbers are not independent. `unresolved_obligations: []` holds because the reviews returned 0/0/0 and the attacks returned REJECTED; the attacks returned REJECTED because their dispositions cite premises the same author froze; the reviews returned 0/0/0 because counting happened after repair. Repeating the three in the release JSON, the final report, and the theorem file creates an impression of triangulation the dependency structure does not support. Presentation rather than substance, hence Low — but it is the mechanism by which the package reads as more heavily tested than it is.

**Fix:** State the three together with their dependence: "one author produced the derivation, the attacks, the erasure, the reconstruction, and the reviews; concordance among them is not independent corroboration."

---

### [High] The 8/15 package regressed against the certification discipline the same author used on 8/14

**Location:** compare `2026-08-14-operational-intervention-extensions/claim-ledger.json` and `problem-contract.json` with `2026-08-15-full-pointwise-meta-agent/` equivalents. Both are in the 8/15 diff.

**Defect:** The eligible-evidence-only pattern this review recommends is not a standard imported from outside — it is the pattern the same author used one day earlier in the same repository, and abandoned for the flagship package.

**Evidence.** Machine-read from both ledgers:

| | P14 (`2026-08-14-operational-intervention-extensions`) | P15 (`2026-08-15-full-pointwise-meta-agent`) |
|---|---|---|
| Evidence kinds present | `DERIVATION` ×3, `SYMBOLIC_CHECK` ×2, `APPLICABLE_THEOREM` ×1. **No `AGENT_ASSESSMENT` at all.** | `DERIVATION` ×3, `SYMBOLIC_CHECK` ×2, **`AGENT_ASSESSMENT` ×6** |
| `target.evidence_ids` | `EV-DIRECT-DERIVATION`, `EV-COUNTEREXAMPLE-DERIVATIONS`, `EV-PRIOR-HARD-APPLICABLE-THEOREM`, `EV-INDEPENDENT-RECONSTRUCTION` — all derivation-class | nine entries, **six of them `AGENT_ASSESSMENT`** |
| Domain reviews in package | none | four, all bound into the release gate |
| `unresolved_obligations` | six populated | `[]` |
| Attacks that land | several (A3, A8, A9, A12, A14, A15 concede or refute a stronger reading) | zero |
| Falsification criterion on non-derivation | "an incomplete derivation, unresolved side condition, missing hypothesis mapping, or missing eligible evidence does not refute the target; **it yields INCONCLUSIVE and blocks a complete release**" | "Inability to derive the affirmative construction leaves that conjunct unresolved" — no release consequence stated |
| Literature policy | names a specific authority revision (`53cafa37…`) and four specific prior artifacts | "Use only checked primary sources or released repository derivations" — no revision named |

So on 8/14 the author's own contract made missing evidence *block a complete release*; on 8/15 it merely "leaves that conjunct unresolved" while the release ships `COMPLETE_AFFIRMATIVE` with `unresolved_obligations: []`. And on 8/14 no agent judgment appeared in the ledger's evidence at all; on 8/15 two-thirds of the target's evidence is agent judgment.

**Falsifier:** Show that P15's target requires review-class evidence that P14's did not — e.g. that the schema mandates domain reviews for `MIXED` quantifier-class targets. `claim-ledger.json` schema_version is `rigorous-theory-search/v1` in both, and P14's target is also a mixed affirmative/negative conjunction with a `COUNTEREXAMPLE` negative certificate kind, so the schema does not force the difference.

**Fix:** Restore the 8/14 discipline: derivation-class evidence only in `target.evidence_ids`; reviews recorded as process metadata outside the ledger's evidence set; and the 8/14 wording that missing eligible evidence blocks a complete release.

## Things that check out

Reported honestly, as required. Each of these I verified mechanically and each held.

1. **The final-release hash table binds the committed bytes.** Every entry of `release-provenance.json.final_release_snapshot.artifact_sha256` that I recomputed matches the file at `8ce6358` — `release.json` `36a4458d…`, `problem-contract.json` `e74764ab…`, `evidence/direct-derivation.md` `2aa70b07…`, `evidence/counterexample-proofs.md` `59c38ed4…`, `evidence/adversarial-attacks.md` `edc9f7d8…`, `evidence/oracle-erasure.md` `c957a173…`, `evidence/independent-reconstruction.md` `f74f74bb…`, `evidence/release-assembly.json` `e8ac599a…`, `evidence/notation-collision-report.json` `67a8c6a2…`, `evidence/notation-registry.json` `c4ee4c4c…`, `evidence/notation-standard.md` `cfe662fa…`, `evidence/finite-nongaussian-output.json` `ca79ea94…`, `evidence/finite_nongaussian_witness.py` `15a9eea5…`, `evidence/notation_scan.py` `0c11294e…`, and all four `evidence/reviews/*.md`. Stage 3 of the chain is real; my Critical finding is about stages 1 and 2 only.

2. **All three snapshot fingerprints are reproducible and correct.** The undocumented `fingerprint_sha256` turns out to be `sha256(json.dumps(artifact_sha256, sort_keys=True, separators=(",", ":")))`, which I recovered by search and then confirmed for every block:
```
review_input_snapshot            recorded 6735ec9be08fb8bf3dc8  recomputed 6735ec9be08fb8bf3dc8  MATCH
fix_round_1_review_input_snapshot recorded 7479e84d3999e41324d2  recomputed 7479e84d3999e41324d2  MATCH
final_release_snapshot           recorded 5d3703b39303bece791d  recomputed 5d3703b39303bece791d  MATCH
```
The tables are internally consistent with their fingerprints. (The recipe is not documented anywhere in the package; that is a Low presentation gap, not a defect.)

3. **`release.json` and `release-assembly.json` review hashes match the four review files exactly.** `14f7f00f…`, `c291869c…`, `431a63b0…`, `71401ff1…` all recompute correctly.

4. **The dependency-closure claim is exactly right.** `final-report.md:22-24` and `view-dynamics-scope.md:74` claim that traversal from `target` reaches the target plus exactly seventeen static ancestors, all `EVIDENCE_VERIFIED`, and does not reach `DYNAMICS-SCOPE`. I ran the traversal on `dependency-dag.json` against `claim-ledger.json`: 18 nodes reached, zero non-`EVIDENCE_VERIFIED` in the closure, `DYNAMICS-SCOPE` not reachable (it has an outgoing edge to `PARENT-NORMALIZATION` but no incoming edge from the closure), 19 claims total. The graph is acyclic. This claim is exactly as stated.

5. **The deterministic witness reproduces byte-identically and its check count is honest.** I re-ran `finite_nongaussian_witness.py` under both `python` and `python -O`; both runs regenerate `finite-nongaussian-output.json` with sha256 `ca79ea94822e74ad1e7fb3257d0ea852a609a9102be0e49a302687ad1612c062`, unchanged from the committed value (`git status` clean afterward). The output's `summary` reports `check_count: 51, passed: 51, failed: 0`; the `checks` object contains exactly 51 entries and every value is `true`. The script uses `fractions.Fraction` throughout, so the arithmetic is exact. This is the one piece of genuinely mechanical, independently reproducible evidence in the package, and it does what it says.

6. **The §1 witness is arithmetically correct and is a valid nonvacuity witness.** I recomputed `counterexample-proofs.md` §1 by hand: with `K_0 = (3/4, 1/4)` and `K_1 = (1/4, 3/4)` on `B`, `P_I(O=1,m,b,e|X) = ¼K_m(b)` sums to 1 with `p_X(1)=1`; `Π^{MB} = ½K_m(b) = (3/8, 1/8, 1/8, 3/8)` as displayed; `Q(m,b,e) = ½K_m(b)1{e=b}` sums to 1 with atoms `(3/8, 1/8, 1/8, 3/8)`; every atom of `Π` is positive so `Q ≪ Π`; the likelihood ratio is identically 2 on `supp Q`, giving `D(Q‖Π) = log 2`; the deterministic channel retaining `(B,M)` sends both to `½K_m(b)`, so the coarse KL is 0 and the defect is `log 2`. Every figure in the document matches. Because this datum satisfies normalization, recognition-independence of `C_A`, `Q ≪ Π`, finite positive evidence, and a.s. evaluator compatibility simultaneously, it establishes that the frozen premise set is satisfiable — the affirmative conjunct is not vacuous.

7. **`view-information-vfe.md`'s independent KL derivation is correct.** I reconstructed it: with `Q̃(dy,dz)=Q(dy)C_A(y,dz)` and `P̃(dy,dz)=P(dy)C_A(y,dz)`, testing against bounded functions gives `dQ̃/dP̃(y,z)=r(y)=dQ/dP(y)`, hence `D(Q̃‖P̃)=D(Q‖P)`; `s(z)=dQ_A/dP_A(z)=E_{P̃}[r(Y)|Z=z]`; the conditional derivative is `r(y)/s(z)` for `Q_A`-a.e. `z`; and the chain theorem via the nonnegative generator `φ₀(t)=t log t − t + 1` gives `D(Q‖P) = D(Q_A‖P_A) + ∫ D(Q̃(·|z)‖P̃(·|z)) Q_A(dz)` in `[0,+∞]`. The review's insistence that the defect is weighted by `Q_A` and not `P_A` is right, and the `φ₀` correction it describes is a genuine repair (raw `t log t ≥ −1/e`, so monotone truncation of the unshifted integrand does not justify the extended-valued identity). This review does real mathematical work; my finding against it is about its severity counting and its byte binding, not its content.

8. **The four reviews state explicit falsification conditions.** All four end with numbered falsifiers that are concrete and checkable (e.g. `view-information-vfe.md` conditions 1-8, `view-gauge-holonomy.md` conditions 1-10). Writing falsifiers into a review is good practice and rare. That two of them are *satisfied* at the released bytes (finding 2) is a separate matter from their having been written.

9. **The scope disclaimers are extensive, specific, and consistent across artifacts.** `problem-contract.json:43-49`, `final-report.md:38-40`, `construction-or-strongest-theorem.md` closing paragraph, and `docs/change-logs/2026-08-15.md:43` all list the same exclusions (cross-`X` sufficiency, quotient regularity, Gaussian closure, gluing, membership selection, comparison theorem, unique DAG/physics, autonomy, agency, nonequilibrium, physical time). I checked for a scope claim in one artifact contradicted by another and found none except the holonomy "exactly one" divergence reported above. The package does not, in its prose, claim a geometric meta-agent or an autonomous agent.

10. **`unresolved_obligations: []` is glossed honestly where it is defined.** `final-report.md:36` says "None **within the frozen target and its transitive dependency closure**," and the downstream OPEN list is genuinely maintained. My Medium finding is about cross-package inconsistency of the field, not about concealment.

## Direct answers to the seven questions

**1. The sixteen attacks.** Thirteen could not have succeeded: their disposition is fixed by a frozen premise (A1-A3, A11, A12) or by a proposition the package explicitly disclaims (A5-A10, A14-A16). Two are genuine hazards with textbook resolutions (A4, A13), and only A4 actually bit — it was answered by narrowing the claim, which is recorded indistinguishably from the twelve that could not fail. A16 bundles eight separate disclaimers into one entry. Missing attacks a hostile referee would make, at minimum: (i) triviality/prior art — the affirmative conjunct is a typed specialization of Markov-kernel pushforward, standard-Borel disintegration, and the relative-entropy chain rule; (ii) nonvacuity — is the eight-premise conjunction satisfiable at all (covered by accident, never asked); (iii) strawman negatives — who asserts the universals the five `NEG-*` conjuncts refute; (iv) self-certification — all evidence comes from one agent in one session; plus (v) is the admitted-observation set non-null, and (vi) the unattacked pairwise converse of the equality criterion.

**2. Oracle erasure.** It cannot do what it claims under single-agent authorship, and it is a pure self-report. No erased premise set, no diff, no re-derivation against erased text, no script — unlike the notation and finite-witness audits in the same package, both of which ship reproducible artifacts. Its detection probability conditional on a smuggled conclusion is unknown and plausibly near zero, since the scanner is the writer. One mechanical check *would* have survived an outside audit (an automated premise/conclusion entailment scan over the machine-readable ledger) and was not performed.

**3. Independent reconstruction.** Not a paraphrase — word n-gram overlap with the direct proof is 4.2% at n=4 and 1.0% at n=8, most of it the shared metadata header. But not independent either: all fourteen load-bearing steps appear in the same relative order with zero inversions and the same proof technique at every step; the only structural change is merging direct §1-§3 and prepending material drawn from `counterexample-proofs.md`, a file the direct proof does not contain. The artifact itself is honest ("not independent-agent agreement"); `final-report.md:28` is not.

**4. The four domain views.** The 0/0/0 result is a property of the counting rule, not of the proof: defects found are repaired before counting, or reclassified as exposition. The package's own chronology records three separate occasions where a 0/0/0 verdict was followed by a later review that found defects (Fix Round 1's `WITHHOLD 0/0/2`; the stale notation sentence after the six-reviewer 0/0/0 at `fe08359`; the missing a.s. qualifier after that). The rounds that found defects are not preserved as artifacts — only their SHA-256 and a closure narrative. One review file (`view-probability-kernel.md`) contains internally inconsistent descriptions of the same sentence, showing it is an edit of an earlier review rather than a fresh pass.

**5. Provenance non-circularity.** Verified mechanically, with a split verdict. Stage 3 is real: every final-snapshot hash I recomputed matches the committed bytes, and all three fingerprints reproduce exactly under `sha256(json.dumps(table, sort_keys=True, separators=(",",":")))`. Stages 1 and 2 bind nothing: their hashes correspond to uncommitted working-tree bytes, the reviews admit this ("the exact **unstaged** Task-5 bytes"), and the originating worktree at `C:/tmp/MultiAgentELBO-full-meta-agent-implementation-20260815` is clean at the final state with an empty stash, so those bytes are permanently unrecoverable. The hashes therefore bind the content they claim to bind only for the released snapshot; for the two review snapshots they are unfalsifiable tokens. The structure is one-way and internally consistent, but two of its three links are unauditable, which defeats the purpose of asserting non-circularity.

**6. Falsifiability.** The target is falsifiable, and I state the falsifier in one sentence in the Medium finding above: a standard-Borel datum meeting every frozen premise for which `Π_{I,o,X}C_A` fails to be a version of the parent posterior, or `Q_AC_A ≪ Π_AC_A` fails, or the additive KL chain identity fails. So this is not a High finding on falsifiability as such. What *is* a High finding is that the contract scores non-derivation as unresolved with no release consequence, while the 8/14 contract by the same author scored it as `INCONCLUSIVE` and release-blocking; and that the holonomy conjunct, as frozen ("exactly one"), is contradicted by the released theorem and by the gauge reviewer's own mandatory falsifier.

**7. Ledger legitimacy.** Not legitimate as constructed. Six of the nine evidence entries closing `target` are typed `AGENT_ASSESSMENT`, which cannot close a claim under the operative protocol — and the package says so itself at `release-assembly.json:121` and in every one of those entries' `side_conditions`, then uses them in the gate's stated `reason` and in both certification artifacts' promotion sentences. Eligible evidence: `EV-TASK3-DIRECT-DERIVATION` and `EV-TASK4-COUNTEREXAMPLE-DERIVATIONS` (derivation-class, sufficient in kind if the mathematics is sound), plus `EV-TASK5-INDEPENDENT-RECONSTRUCTION` (derivation-class but adding no independence). The two `SYMBOLIC_CHECK` entries are genuine mechanical evidence and are correctly excluded from `target`. Independently, the `AGENT_ASSESSMENT` evidence is stale under the protocol's freshness rule: its recorded input snapshot is not the released bytes, and two canonical sources it binds changed afterward. The defensible state is `target` closed on the two derivations alone, with `unresolved_obligations` naming the outstanding re-review at released bytes — not `unresolved_obligations: []`.


## Coverage

**Read in full:** P15 `adversarial-attacks.md`, `oracle-erasure.md`, `independent-reconstruction.md`,
`release-provenance.json`, `release-assembly.json`, `release.json`, `problem-contract.json`,
`dependency-dag.json`, `final-report.md`, `reviews/view-probability-kernel.md`,
`reviews/view-information-vfe.md`, `reviews/view-dynamics-scope.md`;
P14 `adversarial-attacks.md`, `oracle-erasure.md`, `release.json`;
`docs/change-logs/2026-08-15.md`. Plus `.gitattributes` and the full `add1a69..HEAD` diff of
`construction-or-strongest-theorem.md`, `direct-derivation.md`, and `problem-contract.json`.

**Read programmatically (whole file parsed, fields enumerated):** P15 and P14 `claim-ledger.json`
(all claims, all evidence entries, kinds, states, `evidence_ids`); P15 `adversarial-report.json`;
P15 `finite-nongaussian-output.json` (all 51 checks).

**Sampled:** `reviews/view-gauge-holonomy.md` (~110 of 200 lines: header/bindings, the finite-witness
recomputation section, the reconstruction/adversarial audit, findings, all ten falsifiers,
recommendation — the middle gauge-mathematics sections were skimmed, as gauge content is P-gauge's
scope); `direct-derivation.md` (section structure via headings, plus the passages quoted verbatim by
the two reviews and the diffed region at line 286 — the 552 lines of measure-theoretic content are
another reviewer's scope, not mine); `counterexample-proofs.md` (§1 in full and recomputed, §§2-5 via
the reviews' restatements); P14 `independent-reconstruction.md` (first 60 lines);
`Theory/06_general_coarsegraining.tex` (lines 60-90 and the 8/15 diff hunk).

**Not reached:** P14 `evidence/recompute.py` and `recompute-output.json` (not re-executed);
P14 `evidence/prior-hard-operational-reduction-proof.md`; P14 `dependency-dag.json` traversal;
P15 `approach-registry.json`; P15 `notation_scan.py` / `notation-collision-report.json`
(the 5732-line notation audit was inspected only for existence and size, not verified);
`Theory/07b_agent_network_rg.tex`; `docs/superpowers/specs/…-design.md` and
`docs/superpowers/plans/…` (hashed, not read).

**Commands whose output is quoted in this file** were all run against the working tree at
`8ce635807a6ca2a388255fc996c98f7c535e5843` with a clean `docs/derivations/` status, using
`C:/Python314/python.exe` (pure-rational/stdlib work only; no torch, no model).

**Out of scope for this reviewer, deliberately:** whether the measure-theoretic derivation in
`direct-derivation.md` is correct. Where I state that a step is standard or correct (the chain rule,
the §1 arithmetic, the `φ₀` repair), I recomputed it; where I have not checked, I say so. Nothing in
this file should be read as endorsing the mathematics beyond those specific checks.
