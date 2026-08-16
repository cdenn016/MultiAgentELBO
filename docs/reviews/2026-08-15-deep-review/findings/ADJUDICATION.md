STATUS: COMPLETE

AGENT: adjudicator (Claude Opus 5) — wave 2 (§A) and wave 4 (§B)
TARGET: 8ce635807a6ca2a388255fc996c98f7c535e5843
WAVE-2 RUN AT REPO HEAD: 7433d814afbddf6b5ab1f838746ed414d346dc57
WAVE-4 RUN AT REPO HEAD: 3505a53 (branch `review/2026-08-15-deep-review`; all target artifacts read at
`8ce6358` or at their unchanged working-tree state)

# Adjudication of contested findings

Verdicts below rest on my own executed commands and reconstructions, listed under each case. Where a
skeptic and an investigator disagreed on a checkable fact I ran the check myself rather than choosing
between them. No verdict rests on agreement between agents.

---

# §B — Wave 4

## Correction to the orchestrator's input record, before anything else

The wave-4 verdict list handed to me marks eight of the eleven contested findings `INCONCLUSIVE`,
`evidence_kind: "none"`, rationale *"skeptic agent died or was skipped."* **That metadata is false for
seven of the eight.** I read every `V-W4-*.md` file on disk:

```
$ head -6 findings/V-W4-*.md | grep -c "STATUS: COMPLETE"      -> 8 of 9 files
V-W4-P1-High-2-crossX.md          STATUS: COMPLETE   UPHELD_REDUCED / Low
V-W4-P2-High-infinite-tier.md     STATUS: COMPLETE   UPHELD_REDUCED / Low
V-W4-P3-High-CE4.md               STATUS: COMPLETE   UPHELD_REDUCED / Medium
V-W4-P4-High-1-blindness.md       STATUS: COMPLETE   UPHELD_REDUCED / Medium
V-W4-P10-High-05d-uncited.md      STATUS: COMPLETE   UPHELD_REDUCED / Medium
V-W4-P9-counts.md                 STATUS: COMPLETE   UPHELD_REDUCED / Low
V-W4-P9-ledger-eligibility.md     STATUS: COMPLETE   REFUTED
V-W4-P9-fourth-conjunct.md        STATUS: COMPLETE   UPHELD_REDUCED / Low
V-W4-P9-attacks.md                STATUS: IN_PROGRESS  (12 lines, no verdict — genuinely dead)
```

Each of those seven carries executed commands, quoted output, or a reconstructed derivation. Applying
rule 1 to the *metadata* rather than to the *record on disk* would have discarded seven evidence-backed
skeptic passes and left seven High findings artificially unresolved. I adjudicate from the files. Only
`W4-P9-attacks` is genuinely unassessed, and only its sub-finding (a) survives as `INCONCLUSIVE`;
I settled its sub-finding (b) myself below.

One further metadata conflict: the orchestrator's record for `W4-P9-fourth-conjunct` reads
`REFUTED / None`, while the file on disk reads `UPHELD_REDUCED / Low`. Both agree the load-bearing
charge is refuted; they differ only on whether a residue survives. I resolve that split below on my
own execution.

## Wave-4 verdict table

| Finding | Investigator severity | Skeptic verdict | ADJUDICATED | Adjudicated severity | Evidence relied on |
|---|---|---|---|---|---|
| W4-P1-High-2-crossX | High | UPHELD_REDUCED / Low | **CONFIRMED** as notation hygiene; the correctness clause and the "caveat confined to one paragraph" clause **REFUTED** | **Low** | My own `grep` of `Theory/SPEC.md:220` and `Theory/appendix_notation.tex:60` (the skeptic's one open obligation, discharged by me); my own read of `direct-derivation.md:6,154,190,452` |
| W4-P2-High-infinite-tier | High | UPHELD_REDUCED / Low | **CONFIRMED** as an internal contract inconsistency; the load-bearing clause **REFUTED** | **Low** | My own JSON dump of `claim-ledger.json` (`VFE-CHAIN-EXTENDED` = `EVIDENCE_VERIFIED`, statement literally `[0,+infinity]`-valued, no finiteness in `quantifiers`) against `problem-contract.json` `target.regularity` |
| W4-P3-High-CE4 | High | UPHELD_REDUCED / Medium | **CONFIRMED** (mechanical core; location corrected) | **Medium** | My own read of `finite_nongaussian_witness.py:321-325` and `:372-374`; `claim-ledger.json:109-112`; skeptic's four executed mutants |
| W4-P4-High-1-blindness | High | UPHELD_REDUCED / Medium | **CONFIRMED**, and **merged with P4-High-2** — one finding, counted once | **Medium** (one Medium total, not two) | My own dump of `HOLONOMY-BLIND-FULL-LAW` / `HOLONOMY-RETENTION` / `HOLONOMY-ALTERNATIVE` statements and quantifiers; skeptic's executed `V-W4-P4-High-1-check.py`; wave-2 §A verdict on P4-High-2 |
| W4-P10-High-05d-uncited | High | UPHELD_REDUCED / Medium | **CONFIRMED** as an **attribution** defect, scope reduced from six theorems to **one** | **Medium** | My own `grep -rniE "syntactic\|myhill\|nerode\|schutzenberger\|eilenberg" Theory/*.tex Theory/references.bib` → 0 on point; my read of `05d:1082`; P0's independent identification; skeptic's arXiv:1504.02694 |
| W4-P9-counts | High (×2) | UPHELD_REDUCED / Low | **CONFIRMED** narrowly; the non-disclosure charge and the alleged review self-contradiction **REFUTED** | **Low** | Skeptic's reconstruction of the pre-fix `φ₀` defect, corroborated by my own read of `direct-derivation.md:286` |
| W4-P9-attacks (a) "13/16 cannot fail" | High | none (skeptic dead) | **INCONCLUSIVE** — check named below | — | none |
| W4-P9-attacks (b) "prior-art/triviality attacks absent" | High | none (skeptic dead) | **CONFIRMED as fact by my own execution; weak as a defect** | **Low** | My own enumeration of all sixteen records in `evidence/adversarial-report.json` |
| W4-P9-independence | High (×2) | UPHELD_REDUCED / Low | **CONFIRMED** as a release-summary overclaim; both inferences drawn from the structural match **REFUTED** | **Low** | Skeptic's executed `V-W4-P9-independence-structcmp.py` / `-linext.py`; my own diff of `independent-reconstruction.md:46` against `direct-derivation.md:286` |
| W4-P9-ledger-eligibility | High | REFUTED | **REFUTED** (I override one leg of the skeptic's reasoning; verdict unchanged) | **None** (separate Low residue at `release.json:9`) | My own execution: `validate_run.py:619` is `any(...)`; `target` = 3 `DERIVATION` + 6 `AGENT_ASSESSMENT`; `proof-obligations.md:7` read in full |
| W4-P9-fourth-conjunct | High | REFUTED (record) / UPHELD_REDUCED-Low (file) | Charge (b) "contradicts the frozen contract" **REFUTED by my own execution**; charge (a) **CONFIRMED** in one location only | **Low** | My own recomputation of `target_digest` = `15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87` over the whole `target` object, matching the recorded value; `target.quantifiers` read in full; three separate holonomy ledger rows dumped |
| W4-P9-regression | High | UPHELD_REDUCED / Medium | **CONFIRMED** as an evidence-typing defect; the "regressed" framing and the "attacks that land" row **REFUTED** | **Medium** | My own sweep of all eleven `docs/derivations/*/claim-ledger.json` |

Two wave-4 findings are adjudicated **REFUTED in their load-bearing form** (`ledger-eligibility` in
full, `fourth-conjunct`'s charge (b)); one is **INCONCLUSIVE** in part; the rest survive, all of them
at a lower severity than filed, and none of them as a correctness defect. **No wave-4 finding shows a
false theorem.**

## Wave-4 case-by-case

### W4-P1-High-2-crossX — CONFIRMED at Low. I discharge the skeptic's one open obligation, in its favor.

The skeptic left exactly one obligation open: it did not check whether `Theory/SPEC.md` or
`Theory/appendix_notation.tex` — both listed as `canonical_sources` for the evaluator symbol — type the
parent evaluator with `X_A` in its domain, and said its verdict fails if they do not. I checked:

```
$ grep -n "operatorname{ev}" Theory/SPEC.md Theory/appendix_notation.tex
Theory/SPEC.md:204          \(\operatorname{ev}_i:m_i\mapsto K^X_{i,m_i}\).
Theory/SPEC.md:220          \(\operatorname{ev}_A:m_A\mapsto K^{X_A}_{A,m_A}\).
Theory/appendix_notation.tex:32   \operatorname{ev}_i(m_i)=K^X_{i,m_i}\)
Theory/appendix_notation.tex:60   \(\operatorname{ev}_A:m_A\mapsto K^{X_A}_{A,m_A}\)
```

Both canonical sources carry `K^{X_A}` for the *parent* evaluator and `K^{X}` for the fine one. The
superscript is the program's standing notation, not an artifact of this derivation, so there is no
second semantic type and no registry collision.

I also refute the finding's third clause directly. The cross-`X` disclaimer is not confined to one
paragraph; it is in the theorem's standing setup and repeated at the point of use:

- `direct-derivation.md:6` — "This theorem is pointwise in this one \(X\). It makes no claim that two
  values \(X,X'\) with \(\chi_A(X)=\chi_A(X')\) induce the same parent law. Such a cross-\(X\) claim
  would require a separately measurable factorization through \(X_A\)."
- `:154` — "At fixed \(X_A\), a parent evaluation family means…" (the tier is declared slice-local).
- `:190` — "The notation \(X_A\) does not prove cross-\(X\) factorization: … equality of their induced
  kernels whenever \(\chi_A(X)=\chi_A(X')\), together with measurability in \(X_A\), is an additional
  premise."

So (4.5) is not "false under a literal reading"; it is a fixed-slice statement whose slice is declared
twice in the same document. The only two-`X` site is `:452-453`, and it is an equivariance *hypothesis*.
What survives is that a reader scanning the display alone can misread the superscript as a
factorization claim, and that the derivation's symbol is out of step with the package's own claim
ledger. **Low — wording/presentation under `RESUME.md:64`.**

### W4-P2-High-infinite-tier — CONFIRMED at Low; the load-bearing sentence is refuted by execution.

The finding's load-bearing sentence is "the release cannot support it: nothing in `[0,+∞]` is inside
the frozen domain." I dumped the ledger rather than adjudicating prose:

```
VFE-CHAIN-EXTENDED   state=EVIDENCE_VERIFIED   kind=MATHEMATICAL
  statement:   "The two joint lifts through the same C_A obey the additive [0,+infinity]-valued KL
                disintegration: fine KL equals parent KL plus the nonnegative conditional-KL defect…"
  quantifiers: "For every pair satisfying ASM-RECOGNITION-AC, ASM-COMMON-CHANNEL,
                ASM-EVIDENCE-REPRESENTATIVE."          <- no finiteness
```

The extended tier is inside the release, certified, with no finiteness quantifier. The sentence is
false and the finding's fix (b) — demote the manuscript's `\status{ESTABLISHED}` to match the package —
would make the documentation less accurate, not more.

What survives is a genuine contradiction *inside the frozen contract object*. `target.regularity`
reads "…and **finite terms wherever KL or VFE expressions are displayed**", which is contradicted by
`target.statement`, by `target.quantifiers` (neither carries KL-finiteness), by the certified
`VFE-CHAIN-EXTENDED`, by `final-report.md:40`, and by the package's own `direct-derivation.md`
(6.3)/(6.4)/(6.6), all of which display extended-valued KL. One clause, one repair. The substantive
half of the charge is already filed by the same investigator as its own `MEDIUM-2` and must not be
counted twice. **Low.**

The mathematics is not in dispute and I did not re-derive it: P0, the investigator, and the skeptic all
reach the same unconditional zero-defect criterion, and P0's reconstruction (§"Verified: the additive
KL chain") already carries it.

### W4-P3-High-CE4 — CONFIRMED at Medium.

I read the check myself rather than accepting the mutation table:

```python
# evidence/finite_nongaussian_witness.py:321-325
    record(
        checks,
        "CE4_tree_directed_KL_symbolic_half_log_3",
        Fraction(3, 4) - Fraction(1, 4) == Fraction(1, 2),
    )
```

That is a constant expression over two literals. It never reads `node_laws`, so a check named for a
directed KL constrains nothing about the distributions it is named for. The emitted artifact compounds
it: `:372-374` hard-types `"identity_tree_directed_KL": "log(3)/2"` next to `identity_tree_laws`, which
*is* derived from `node_laws` — so the JSON will publish a false pairing under any change to the laws.
The skeptic's four executed mutants (including mutant D, which leaves the exhibited left law verbatim
and still passes) establish this beyond the investigator's own falsifier.

Severity. The rubric reserves **High** for "a claim materially stronger than its proof, or a proof with
a repairable gap." Neither applies: the mathematics of CE-4 is true (`KL = (3/4 − 1/4)log 3 = ½log 3`,
verified exactly in both orientations), and I confirmed that no ledger *claim* depends on the value —
the only ledger mention of `log(3)/2` is a side condition of the evidence record itself:

```
$ grep -n "log(3)" claim-ledger.json
112:  "Decimal log values are readability-only corroboration; symbolic log(2), log(3)/2, zero, and
       +infinity labels are primary."
```

What is over-reported is the `EV-TASK4-FINITE-WITNESS-OUTPUT` scope sentence, "51 exact finite checks,
including … forward and reverse KL orientations", one of which is a tautology. That is imprecision in a
certified evidence artifact, i.e. **Medium**. I adopt the skeptic's location correction:
`counterexample-proofs.md:198-202` should be struck from the finding — the mathematics there is right.

### W4-P4-High-1-blindness — CONFIRMED at Medium, MERGED with P4-High-2, counted ONCE.

The skeptic's reconstruction is sound and I checked its premise against the ledger:

```
HOLONOMY-BLIND-FULL-LAW  statement: "Under typed source/target groupoid actions, full fine-law
  covariance, compatible selected posterior versions, recognition covariance, C_A equivariance, and
  evaluation covariance, full parent … laws are covariant; same-slice invariance follows only on the
  fixed-(o,X) stabilizer."
```

Every conclusion is downstream of an *assumed* fine-level covariance. At an admitted isotropy arrow,
(7.2)/(7.3) assume the fine laws are invariant and (7.5) carries that assumption through an
assumed-equivariant kernel. So the configuration the word "blind" names — the parent failing to
register a motion the fine level registers — is not a consequence of (7.1)–(7.6) and cannot be
witnessed by any datum `ASM-HOLONOMY-BLIND-DATA` admits. The label misdescribes; the theorem is true
and correctly fenced (the "only on the stabilizer" clause is in the ledger statement itself).

**Counting rule, stated explicitly under rule 4 and the wave-2 non-double-counting rule.** This is the
second word of the same three-place string that wave-2's P4-High-2 attacks. P4-High-2 shows "holonomy"
has no connection-theoretic content in §7; this shows "blind" names an erasure the theorem does not
deliver. They are logically independent as claims but they are one defective label repaired by one
rename, and P4's own Medium "the dichotomy is not a dichotomy" is a third facet of it. **Report as one
Medium finding, "§7's branch label `holonomy-blind` misdescribes on both words." Do not tally two.**

One provenance point cuts against the package and I record it: "holonomy" is inherited vocabulary,
but "blind" is coined by this work (`git log -S"holonomy-blind"` first hits `ceffda2`; it enters the
manuscript at `b9ba51f`), and it is introduced with no definition anywhere — its only operative gloss
is by contrast at `:461`.

### W4-P10-High-05d-uncited — CONFIRMED at Medium as an ATTRIBUTION defect, scope one item not six.

Rule 4 governs here. This is not a correctness finding and it is not an overclaim finding about the
theorem; it is attribution, and the rubric puts attribution at Medium.

I verified the surviving item myself:

```
$ grep -rniE "syntactic|myhill|nerode|schutzenberger|eilenberg" --include=*.tex --include=*.bib Theory/
   (two hits, both in PIFB2.tex about syntax in attention heads; nothing on point)
$ sed -n '1082,1090p' Theory/05d_relational_inference.tex
   \propositionheading{Universal property of the contextual operational quotient}…
   a\sim_\Phi b  \iff  \Phi(uav)=\Phi(ubv)  for every u,v \in A
```

That is the syntactic congruence, and the universal property that follows is the syntactic-monoid
universal property. P0 identified it independently and named the primary sources (Myhill; Nerode;
Schützenberger; Pin, *Varieties of Formal Languages* Ch. 2; Eilenberg Vol. B); the skeptic fetched
arXiv:1504.02694 (Adámek–Milius–Urbat) and matched Definition 36 / Definition 32. Neither the
manuscript nor its 466-entry `references.bib` names any of them, and the borrowed notation `Syn(Φ)` is
used without saying whose it is.

The rest of the finding fails and I accept the skeptic's refutations, which are checkable and were
checked: `SPEC.md:71`'s `ESTABLISHED` obligation is **disjunctive** ("Give the proof **or** the
citation"), and seven of the eight new `ESTABLISHED` items carry a complete `\paragraph{Proof.}` ending
in `\(\square\)` — so the SPEC-conformance leg is refuted outright, and the count "six" is wrong in
both directions. The circle-heat theorem is not a classical restatement (P0 reconstructed it in full in
Fourier and called it "the strongest single item across both packages"); the compact-quotient theorem
is not a one-step corollary (P0 showed the countable dense signature is what buys metrizability and
that joint continuity is obtained correctly). **Medium, one item.**

### W4-P9-counts — CONFIRMED at Low.

I corroborated the skeptic's concession because it is the part that matters: the *pre-fix* mathematics
at `add1a69` was genuinely wrong, not merely loose. It justified the chain rule by "monotone truncation
to the nonnegative relative-entropy integrands", and the raw `t log t` integrand is not nonnegative
(minimum `−1/e` at `t = 1/e`). The released text repairs exactly this, and I read the repair:

```
direct-derivation.md:286  "…invoking the standard extended-valued chain theorem through the
  nonnegative generator (φ₀(t)=t log t − t + 1) and its monotone truncations, rather than treating the
  raw (t log t) integrand as pointwise nonnegative…"
```

So a real Medium-or-worse defect existed in the load-bearing step at the commit the reviews name, and
the released reviews report 0/0/0. That is the finding's factual predicate and it holds.

The charges that fail are the ones doing the rhetorical work: the fix-then-count convention *is*
disclosed in every release-facing artifact (`release.json`, `release-assembly.json`, `final-report.md`,
and all four reviews carry the "corrected-byte" / "same-view re-review" / "cannot replace direct
mathematical evidence" qualifier), and the alleged self-contradiction inside
`view-probability-kernel.md` does not exist once the bound derivation hash is checked. What survives is
one narrow drafting sentence, not "the counts carry no information about the proof." **Low.**

### W4-P9-attacks — (b) settled by me and CONFIRMED as fact; (a) INCONCLUSIVE.

The skeptic file is twelve lines and `STATUS: IN_PROGRESS`. This is the one finding where the
orchestrator's "died" metadata is accurate. I settled the half that is mechanical.

**(b) — CONFIRMED as fact.** I enumerated the register myself:

```
$ python - <<'…'  adversarial-report.json
n=16  Counter({'REJECTED': 16})
ATTACK-NONNORMALIZATION, -DEPENDENT-COARSE-CHANNEL, -GENERATION-READS-RECOGNITION,
-NULL-POSTERIOR-VERSION, -SPLIT-CHANNEL-SUPPORT, -MARGINAL-RECONSTRUCTION, -INCOMPATIBLE-EVALUATOR,
-KERNEL-QUOTIENT-REGULARITY, -MARGINAL-FULL-HOLONOMY, -TRIVIAL-HOLONOMY-SELECTION, -ERASED-MARKS,
-GAUSSIAN-LEAKAGE, -INFINITY-MINUS-INFINITY, -FAMILY-WIDE-RECOVERY, -CROSS-X-GLUING,
-AUTONOMY-ONTOLOGY-DYNAMICS
```

Every one of the sixteen is an over-reading attack ("this could be inflated into X"). **Not one attacks
triviality, novelty, or prior art** — the two objections P0 reached independently and that wave 1 and
wave 2 both confirmed have real content. The fact is established.

**But its force as a defect is weak, and I say so rather than shading it.** `problem-contract.json`'s
`literature_policy` ends "No novelty or priority claim is made", and its `literature_policy` admits
"released repository derivations" as sources. A portfolio is not obliged to attack a claim the contract
declines to make. And wave 2 established that three of the four domain reviews *do* cite the ancestor
chapter by exact line range. So this is a completeness observation about the attack portfolio, in the
same thread as P1-High-1 (adjudicated **Low** in §A) — **Low, and do not count it twice with that
finding.**

**(a) — INCONCLUSIVE.** "Thirteen of the sixteen cannot fail, because their disposition is fixed by a
frozen premise or an explicit non-claim" is a severity-of-test judgment (Mayo/Popper), and no party has
put eligible evidence behind it. **The one specific check that would settle it:** for each of the
sixteen, exhibit a datum that satisfies every frozen premise in `target.premises` and
`target.quantifiers` and on which the attacked failure mode actually occurs; an attack for which such a
datum exists is severe, an attack for which the frozen premises make it impossible is not. The skeptic
for `W4-P4-High-1-blindness` performed exactly this construction for one attack
(`V-W4-P4-High-1-check.py`), and the same method applied to the remaining fifteen decides the finding
mechanically. Until that is run, `INCONCLUSIVE`.

### W4-P9-independence — CONFIRMED at Low; both inferences refuted.

The structural comparison reproduces (skeptic's `V-W4-P9-independence-structcmp.py`: the n-gram table
byte-for-byte, section-block order A–F identical in both derivations, zero inversions across fourteen
load-bearing steps). Both inferences drawn from it fail.

The reconstruction's *inputs* are mandated by the protocol —
`references/adversarial-verification.md:7`, "from the problem contract, claim ledger, and dependency
DAG without the intended narrative" — and `claim-ledger.json` lists its claims in block order
A,B,C,D,E,F,G. An agent obeying the protocol literally reproduces the direct proof's order without
opening it. The match is what compliance predicts, so it is not evidence of outline reuse. (The
skeptic's linear-extension count — 3,876 extensions over 12 affirmative nodes, 60 admissible section
orders — refutes the *weaker* defense that the mathematics forces the order; the protocol defense is
the one that holds.) And sub-finding (a) demands a mechanical residue the governing protocol says three
times cannot exist (`SKILL.md:54`; `output-contract.md:39`; `adversarial-verification.md:9`, all
stating that paraphrase detection is a semantic judgment the validator cannot make), while the required
record form is fully supplied.

What survives is `final-report.md:28` overselling independence while
`independent-reconstruction.md:8` fences it honestly. **Low — summary looseness.**

**New item, found by the skeptic, favoring the investigator, and confirmed by me.** I diffed the two
documents at the disputed step:

```
independent-reconstruction.md:46  "All terms are nonnegative, so no subtraction of infinities occurs."
direct-derivation.md:286          "…through the nonnegative generator φ₀(t)=t log t − t + 1 and its
                                   monotone truncations, RATHER THAN treating the raw t log t
                                   integrand as pointwise nonnegative…"
```

The reconstruction's one-clause justification is, verbatim in substance, the loose route the direct
proof was corrected to avoid (see W4-P9-counts). And (6.3) is elided from the reconstruction entirely.
So the artifact typed `DERIVATION` and counted toward closure did not independently re-derive the one
step that had a known defect. That is a real coverage gap. It is **new in wave 4, has no wave-1
counterpart, and is therefore recorded but not adjudicated: Low**, carried to the final report as a
separate item.

### W4-P9-ledger-eligibility — REFUTED. I override one leg of the skeptic's reasoning; the verdict stands.

**Where I override the skeptic.** Its §4 claims the rule the finding applies — "LLM judgment cannot
close a claim; agreement among agents is not evidence" — "is not from this package and not from
`rigorous-theory-search/v1`", and is imported from a `verification` skill this package never adopted.
**That is wrong, and I checked it.** The adopted protocol's own reference says it verbatim:

```
~/.claude/skills/rigorous-theory-search/references/proof-obligations.md:7
  "Mathematical verification requires direct DERIVATION, FORMAL_PROOF, or APPLICABLE_THEOREM evidence…
   Numerical tests, finite enumeration, symbolic simplification without side conditions, figures, and
   AGENT AGREEMENT CANNOT CLOSE A MATHEMATICAL CLAIM."
```

So the rule is adopted, not imported, and the skeptic's cleanest line of defense is unavailable.

**The verdict is nevertheless REFUTED, on the mechanics I executed myself.** The adopted rule forbids
closing *by* agent agreement. It does not forbid listing non-closing evidence alongside closing
evidence. The gate is existential:

```python
# ~/.claude/skills/rigorous-theory-search/scripts/validate_run.py:618-626
direct = [evidence.get(item, {}) for item in _list_field(record, "evidence_ids")]
if not any(item.get("kind") in eligible and item.get("supports") is expected_support for item in direct):
    errors.append(...)
kinds = {str(item.get("kind")) for item in direct if item.get("supports") is expected_support}
if kind == "MATHEMATICAL" and state == "EVIDENCE_VERIFIED" and not kinds & MATH_EVIDENCE:
    errors.append(...)
# MATH_EVIDENCE = {"DERIVATION", "FORMAL_PROOF", "APPLICABLE_THEOREM"}
```

`any(...)` and a set intersection — not `all(...)`. And I dumped the claim rather than trusting either
table:

```
target  state=EVIDENCE_VERIFIED  kind=MATHEMATICAL
  EV-TASK3-DIRECT-DERIVATION            DERIVATION        supports=True
  EV-TASK4-COUNTEREXAMPLE-DERIVATIONS   DERIVATION        supports=True
  EV-TASK5-INDEPENDENT-RECONSTRUCTION   DERIVATION        supports=True
  EV-TASK5-VIEW-{PROBABILITY-KERNEL,INFORMATION-VFE,GAUGE-HOLONOMY,DYNAMICS-SCOPE}  AGENT_ASSESSMENT
  EV-TASK5-{ORACLE-ERASURE,ADVERSARIAL-ATTACKS}                                     AGENT_ASSESSMENT
```

Three `DERIVATION` entries carry the closure; the six `AGENT_ASSESSMENT` entries are surplus. The
skeptic executed the finding's own falsifier (delete all six; release mode still exits 0 with `target`
at `EVIDENCE_VERIFIED`) and it was met. The closure does not rest on agent agreement, so the adopted
rule at `proof-obligations.md:7` is not violated. **REFUTED.**

A distinct **Low** residue, which is *not* this finding and which the finding never cites:
`release.json:9`'s `strongest_result` reads "…are EVIDENCE_VERIFIED **by** direct Task-3 and Task-4
derivations, … **and four current corrected-byte domain approvals**", where the "by" governs a list
ending in the approvals. That single summary field does read the approvals as part of what verifies,
and it is contradicted by the per-entry `side_conditions`, `release-assembly.json:121`,
`final-report.md:14,24`, and `oracle-erasure.md:42`'s own fencing sentence.

### W4-P9-fourth-conjunct — charge (b) REFUTED by my own execution; charge (a) CONFIRMED at Low.

The two skeptic records disagree on whether a residue survives. I resolve it by running the check both
of them turn on.

**Charge (b), "the released theorem contradicts the frozen contract's wording", is REFUTED.** The
contract phrase is "declared holonomy-alternative", and the finding reads it as an exclusive-or over
branches. Whether that reading is even available depends on whether `target.quantifiers` is inside the
freeze. I recomputed the digest:

```
sha256( json.dumps(target, separators=(',',':'), sort_keys=True) )
  = 15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87
recorded target_digest
  = 15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87        MATCH
```

The freeze covers all eighteen `target` keys, `quantifiers` included. And `target.quantifiers`, read in
full, ends: "…the stated parent-law, posterior, projection, VFE, **and declared holonomy-alternative
conclusions hold**" — a conjunctive obligation over branches each gated on its own hypotheses, quantified
over `Y_I, B_A, M_A, Xi_A, H_A, X, o, P_I, Pi, Q, C_A, ev_A` and **no holonomy or groupoid data at all**,
so a "for every datum exactly one branch holds" proposition is not even statable inside the frozen
quantifier. The exclusive-or reading is unavailable, and it would additionally make the frozen target
trivially false, since blindness and retention are not complementary. Charge (b) fails on frozen text
the investigator did not read.

**Charge (a), "the conjunct is a modeling declaration with no mathematical content", is CONFIRMED in one
location and refuted elsewhere.** The ledger carries three rows, not one, and I dumped all three. Two
have real mathematical content with hypotheses and fences:

```
HOLONOMY-BLIND-FULL-LAW  "…full parent generative, posterior, and recognition laws are covariant;
                          same-slice invariance follows only on the fixed-(o,X) stabilizer."
HOLONOMY-RETENTION       "When H_A and C_A explicitly retain roots, raw root-framed holonomy, and
                          boundary marks, full parent pushforwards retain their joint laws…"
```

The third does not:

```
HOLONOMY-ALTERNATIVE  kind=MATHEMATICAL  state=EVIDENCE_VERIFIED
  statement:   "A concrete parent MAY DECLARE either the fully hypothesis-backed holonomy-blind
                covariance branch or the raw-retention branch…"
  quantifiers: "For every concrete parent that declares one branch with that branch's hypotheses."
```

A row typed `MATHEMATICAL` and closed at `EVIDENCE_VERIFIED` whose `statement` is a permission ("may
declare") rather than a proposition. Its `quantifiers` field rescues it as a conditional, and the actual
theorem lives in the two rows above, so nothing false is certified and nothing is vacuously closed —
but the statement field of a certified mathematical claim should state a proposition. **Low — one
clause repairs it.** I decline the finding's prescription (amend the frozen target, recompute the
digest, re-run four reviews); the frozen object already disambiguates itself in `quantifiers` and
`symmetries`, and `view-gauge-holonomy.md:147` carries a titled section resolving the same question the
same way.

### W4-P9-regression — CONFIRMED at Medium; the framing refuted.

I ran the comparison across every package rather than the two the finding names:

```
$ python - (all 11 docs/derivations/*/claim-ledger.json)
2026-08-12-elbo-pifb2-fast-slow-program        all {PRIMARY_SOURCE:2, DERIVATION:4, APPLICABLE_THEOREM:1}
2026-08-12-elbo-to-effective-section-action    all {DERIVATION:5, COUNTEREXAMPLE:1, APPLICABLE_THEOREM:1}
2026-08-12-exact-two-channel-finite-elbo       all {DERIVATION:6, APPLICABLE_THEOREM:1, COUNTEREXAMPLE:1, PRIMARY_SOURCE:1}
2026-08-13-finite-presentation-descent…        all {DERIVATION:3, SYMBOLIC_CHECK:1}
2026-08-14-canonical-dependence-selection      all {NONEXISTENCE_PROOF:1, DERIVATION:4, SYMBOLIC_CHECK:5}
2026-08-14-collective-joint-lift-fisher        all {DERIVATION:4, SYMBOLIC_CHECK:7}
2026-08-14-operational-intervention-extensions all {DERIVATION:3, APPLICABLE_THEOREM:1, SYMBOLIC_CHECK:2}
                                            target {DERIVATION:3, APPLICABLE_THEOREM:1}
2026-08-14-pointwise-meta-agent-rg             all {DERIVATION:2, SYMBOLIC_CHECK:2}
2026-08-14-typed-intervention-nonidentifiability all {DERIVATION:6, COUNTEREXAMPLE:1, SYMBOLIC_CHECK:15}
2026-08-15-full-pointwise-meta-agent           all {DERIVATION:3, SYMBOLIC_CHECK:2, AGENT_ASSESSMENT:6}
                                            target {DERIVATION:3, AGENT_ASSESSMENT:6}
```

`AGENT_ASSESSMENT` appears in **zero of the ten predecessors** and only in the 8/15 package. That is
stronger than the two-package comparison the finding filed, and it kills the cherry-picked-comparator
defense. The subject-matter defense also fails: both packages carry exactly two `SYMBOLIC_CHECK`
entries, both correctly exclude them from `target`, so availability of executable evidence is held
constant and cannot explain the difference.

The sharpest form of the defect is internal, and I confirm it: the four review entries carry the side
condition "`AGENT_ASSESSMENT` is adjudication and attack evidence, **not the mathematical derivation
that closes the target**" while sitting inside `target.evidence_ids` — the field whose semantics that
sentence denies, in the same JSON file that applies the distinction correctly to `SYMBOLIC_CHECK`.
Under `RESUME.md:64` that is imprecision in a certification artifact: **Medium**.

Two parts of the finding are refuted. **(1)** The "attacks that land" row is false — I counted both
registers: 8/14 is 21 attacks, all `REJECTED`; 8/15 is 16 attacks, all `REJECTED`. Both are clean
sweeps. Strike the row. **(2)** "Regressed" inverts the direction: the 8/15 package did strictly *more*
verification work (an independent reconstruction, an oracle-erasure pass, four domain reviews, none of
which the 8/14 package ran). The defect is that added work was **mistyped as closing evidence**, not
that work was withdrawn. The finding should be restated accordingly.

**Counting.** With `W4-P9-ledger-eligibility` adjudicated REFUTED, this finding is the sole surviving
carrier of the evidence-typing defect, so there is no double count — but it and the `release.json:9`
residue recorded under that finding are **one** item, not two.

---

# §A — Wave 2

## Verdict table

| Finding | Investigator severity | Skeptic verdict | ADJUDICATED | Adjudicated severity | Evidence relied on |
|---|---|---|---|---|---|
| P9-Critical-2-reviews-falsified | Critical | UPHELD_REDUCED / Critical | **CONFIRMED** (scope reduced: 2 of 4 reviews, not 4) | **Critical** | My own `git show \| sed \| sha256sum` over `add1a69`/`1b18842`/`8ce6358`; my own read of all four review falsifier lists; my own `git diff --stat 1b18842 8ce6358 -- Theory/` |
| P9-Critical-1-provenance | Critical | UPHELD_REDUCED / High | **CONFIRMED** (headline refuted: 1 of 3 snapshots, not 2) | **High** | My own recomputation of all three provenance snapshots against git (0/15, 26/26, 26/26); my own exhaustive `cat-file --batch-all-objects` blob search (1418 blobs) |
| P10-High-2-established-no-proof | High | UPHELD_REDUCED / Medium | **CONFIRMED** (title clause "no proof anywhere in Theory/" refuted) | **Medium** | My own read of `Theory/07b:34-190`; `Theory/SPEC.md:65-71,105-110`; grep for proof markers/`\Cref` in the theorem block |
| P4-High-2-not-holonomy | High | UPHELD_REDUCED / Medium | **CONFIRMED** (headline overstated) | **Medium** | My own grep of `direct-derivation.md:381-465` for connection-theoretic vocabulary; my own read of `Theory/06:560-605` (`thm:cg-holonomy-kl-marginal`) |
| P7-High-1-no-RG | High | UPHELD_REDUCED / Medium | **CONFIRMED** (four supporting sub-claims refuted) | **Medium** | My own grep of `solid_RG_theory.md` (0 hits for "semigroup"; no rescaling/beta/universality); `solid_RG_theory.md:247-252`; `docs/STATUS.md:41,77,193,215`; `overview.md:251,560-565` |
| P1-High-1-prior-work | High (P0 concurred at High) | UPHELD_REDUCED / Low | **CONFIRMED as attribution defect; contract-violation and "no citation" clauses REFUTED** | **Low** | My own `grep -rn "06_general"` over the package (19 hits, with mapping sentences); `grep -c "Theory/"` in `direct-derivation.md` = 0; `grep -rn "cg-"` = 0; `problem-contract.json` `literature_policy` read in full; `git show bd46058:Theory/06` |
| P1-High-3-null-slice | High | UPHELD_REDUCED / Low | **CONFIRMED as internal-consistency defect; "KL term untreated" REFUTED** | **Low** | My own read of `evidence/adversarial-attacks.md:30-36`, `adversarial-report.json:48-54`, `direct-derivation.md:45`; hand check of the KL endpoint |
| P3-High-1-strawman-negatives | High | UPHELD_REDUCED / Low | **CONFIRMED as summary-prose defect; two evidentiary clauses REFUTED** | **Low** | My own dump of the five `NEG-*` records from `claim-ledger.json`; `Theory/05_elbo.tex:30-42`; `Theory/03_probability.tex:425-440`; the finding's own table |

No contested finding was adjudicated INCONCLUSIVE. No contested finding was adjudicated REFUTED in
full; every one has a surviving, evidence-backed core, and in five of eight the core is materially
narrower than the filed headline.

---

## Case-by-case reconstruction

### P9-Critical-2 — CONFIRMED, Critical, scope reduced to two of four reviews

I ran the canonical-source binding check myself rather than accepting either party's table:

```
$ for rev in add1a69 1b18842 8ce6358; do for f in Theory/06_general_coarsegraining.tex \
    Theory/07b_agent_network_rg.tex; do git show $rev:$f | sed 's/$/\r/' | sha256sum; done; done
add1a69  4891a8f5fa86ac0f  Theory/06      add1a69  5eb159493ec72721  Theory/07b
1b18842  4891a8f5fa86ac0f  Theory/06      1b18842  5eb159493ec72721  Theory/07b
8ce6358  fa10620d2a1d0e51  Theory/06      8ce6358  268f9c3b75b09966  Theory/07b
```

`view-probability-kernel.md:31-32`, `view-gauge-holonomy.md:30-31`, and `view-information-vfe.md:29-30`
each record `4891a8f5…` and `5eb15949…`. Those bytes are stale at the released revision.
`grep -rn "fa10620d\|268f9c3b"` over every `.md`/`.json` in the repository outside `docs/reviews/`
returns nothing: no re-review, no re-hash.

The mutation is not cosmetic, and I checked this rather than inferring it. `git diff --stat 1b18842
8ce6358 -- Theory/` is +29 on `Theory/06` and +153 on `Theory/07b`, and the `Theory/07b` insertion is
the entire block `\theoremheading{Full pointwise probabilistic datum for a candidate
parent}{thm:rg-pointwise-parent-datum}` — i.e. the certified proposition was written into the
canonical source after the reviews that bind that source approved.

**Which reviews actually fire.** I read all four falsifier lists. `view-probability-kernel.md:72` and
`view-gauge-holonomy.md:196` both carry an explicit post-review-mutation-of-a-canonical-source clause,
and both bind the mutated files. `view-information-vfe.md:148-157` binds the files but its eight
falsification conditions are all mathematical; none is a byte-mutation clause. `view-dynamics-scope.md`
binds no canonical source at all. So two of four reviews satisfy their own stated falsification
condition, not four. The skeptic is right on the count and I confirm it independently.

**Severity, stated precisely under rule 4.** This is not a correctness finding. No theorem is false;
nothing mathematical depends on it. The review rubric (`RESUME.md:64`) defines Critical disjunctively:
"a stated theorem is false **or the certification is invalid**." `release-assembly.json:73,86,99,112`
stamp all four reviews `BOUND_CURRENT_APPROVE`, `release.json:7` records
`terminal_status: COMPLETE_AFFIRMATIVE`, and the promotion to `EVIDENCE_VERIFIED` rests on those
approvals. Two of the approvals are stale by their own rule, and one of the post-review edits inserted
the certified theorem into the source cited as canonical for it. The certification is invalid. Critical
stands — as a certification-validity finding and nothing more.

I decline the investigator's "the canonical source was amended to contain the proposition being
certified" *circularity* framing. `git show bd46058:Theory/06` confirms
`thm:cg-evidence-preserving-channel`, `thm:cg-dpi-equality`, `cor:cg-pairwise-bayes-recovery`, and
`thm:cg-kl-dpi-extended` all pre-existed this work, so the mathematics being pointed at was already
there. Use the stale binding, not the circularity story.

### P9-Critical-1 — CONFIRMED, reduced to High; the headline is refuted by my own execution

I recomputed all three provenance snapshots against git rather than adjudicating between the two
tables. Script logic: for each recorded path, `git show <rev>:<path>`, hash raw and CRLF-rendered,
compare to the recorded value.

```
=== review_input_snapshot            rev add1a69   entries 15  -> ok=0  mismatch=11  path-absent=4
=== fix_round_1_review_input_snapshot rev 1b18842   entries 26  -> ok=26 mismatch=0   path-absent=0
=== final_release_snapshot           rev 8ce6358   entries 26  -> ok=26 mismatch=0   path-absent=0
```

The finding's headline ("**two** of the three provenance snapshots bind bytes that were never
committed") and its supporting sentence ("the same holds for the fifteen artifact hashes under
`fix_round_1` that differ from the released values") are both **refuted by execution**: stage 2
verifies 26/26 at `1b18842`. Stages 2 and 3 are fully auditable.

Stage 1 is not. I then ran the recovery search the finding's own falsifier demands, over every object
in the store including unreachable ones:

```
$ git cat-file --batch-all-objects --batch-check   -> 1418 blobs
  found:     ac28d445 (dependency-dag.json), 59be1c06 (counterexample-register.md),
             2aa70b07 (evidence/direct-derivation.md), a302a046 (design spec)
  NOT found: 71c56372, 730c28d4, 787132b1, 862dd550, b46ace5e, bfbe5238, ce349475
```

and separately confirmed the four `path-absent` entries — `evidence/adversarial-attacks.md`,
`evidence/independent-reconstruction.md`, `evidence/oracle-erasure.md`,
`evidence/release-assembly.json` — do not match their recorded stage-1 hashes at `1b18842` or
`8ce6358` either. So 4 of 15 stage-1 entries are recoverable, 11 are not, and four bound evidence
documents did not exist at the commit the snapshot names as its `git_head`.

Two further overstatements in the finding fail. `2aa70b07…` (the derivation itself) *is* recoverable
and is byte-identical at `1b18842`, `8ce6358`, and HEAD, so a third party can obtain and check the
mathematics the reviews claim to have read — "the binding detects nothing" is too strong. And the
distinct-snapshot, self-excluding structure of the non-circularity claim is itself checkable and holds.

**High, not Critical:** one snapshot of three, the mathematics recoverable, no mathematical claim
dependent on it. **High, not Medium:** the finding's own falsifier was tested exhaustively against the
object store and was not met.

Side observation I confirm as newly raised in wave 2 and not adjudicated here for lack of a wave-1
counterpart: no `fingerprint_sha256` in any of the three snapshots is reproducible, because no
construction rule for it is documented anywhere in the package. Low; carry to the final report as a
new item, not as part of this finding.

### P10-High-2 — CONFIRMED, reduced to Medium; the title clause is refuted

I read `Theory/07b_agent_network_rg.tex` myself. `thm:rg-pointwise-parent-datum` occupies lines 76-190,
carries `\status{ESTABLISHED}`, and a grep of that span for `proof`/`Proof`/`\Cref`/`\ref{` returns one
hit, an internal `\eqref` to its own defect equation. No proof, no pointer.

`Theory/SPEC.md:70` defines `ESTABLISHED` as "Proved here, or a standard result cited to a source that
has been checked", obligation "Give the proof or the citation"; `:108` "Established theorems remain at
their proofs"; `:29-30` "Nothing in this document is a report on a prior manuscript. It stands alone",
which forecloses the repair of pointing at `docs/derivations/`. So the manuscript's own rule is
violated for its flagship theorem.

But the finding's characterization "no proof anywhere in `Theory/`" is false, and I verified this by
reading rather than by grep. Ten lines above, `thm:rg-exact-coarse-vfe` (`Theory/07b:34-66`) states
the identical content and carries a `\paragraph{Proof.}` that gives exactly the argument:
`C(y,\mathsf Z)=1` preserves the observation marginal; attaching the same channel to both measures
preserves relative entropy, `KL(Q_o‖Π_o) = KL(Q̂_o‖Π̂_o)`; disintegration on `z` plus the
relative-entropy chain rule splits the latter into `KL(Q_o^c‖Π_o^c)` plus the conditional integral. I
reconstructed the missing step and it is that argument, term for term. The defect is a broken audit
trail on a theorem proved ten lines above it in the same file, repairable by a five-line proof
paragraph and two cross-references. **Medium** — a citation/audit-trail defect under the rubric, not a
proof gap.

### P4-High-2 — CONFIRMED, reduced to Medium; the headline is overstated

I grepped §7 of `evidence/direct-derivation.md` (lines 381-465) for `connection|transport|loop|
curvature|cycle|parallel|holonom|path`. Four hits, all of them accounted for: the section heading;
line 383 ("holonomy groupoid"); line 461, the *retention* branch, which declares `H_A` to contain "the
raw root-framed based-holonomy representation"; and line 463. No connection form, no horizontal
distribution, no lift, no loop, no curvature appears anywhere in the section, and the theorem
(7.1)–(7.5) uses none. The mathematical core of the finding survives: §7's theorem is invariance under
an abstract groupoid of measurable isomorphisms and has no connection-theoretic content.

Two corrections I confirm. First, "Nothing in §7 is holonomy" is false as written — line 461 is
genuine holonomy data. The accurate statement is that no *theorem* in §7 has connection-theoretic
content. Second, the finding misses the strongest defense, which I checked directly: `Theory/06:564-601`
defines a genuine based-loop transport group `𝔥_I^x(r) = {T_λ : λ: r→r}` and proves
`thm:cg-holonomy-kl-marginal` about holonomy-stabilized parallel marginal-law sections, and §7 line 383
positions itself explicitly as the full-law generalization of that marginal statement. The name is
inherited from a predecessor where it was earned; the defect is that the generalization silently
widened the acting group from loop transports to an unrestricted groupoid and kept the name.

That is a scope-description defect in a certified conjunct, not a false statement and not a proof gap.
The document's own summary states the correct content. **Medium.**

### P7-High-1 — CONFIRMED, reduced to Medium; four supporting sub-claims refuted

I confirmed the core by grep: `solid_RG_theory.md` contains zero occurrences of "semigroup", and no
rescaling/identification kernel, beta function, blocking ratio, relevant/irrelevant operator, or
universality anywhere. Its only "fixed point" hit (`:365`) is the base point `r_*`. The certified
channel `C_A: Y_I ⇝ Z_A` has no declared inverse-direction map, so it admits no iterate and no flow.
A file titled "solid RG theory" contains no renormalization dynamics.

But four supporting claims fail, and one of them is the finding's own falsifier. `solid_RG_theory.md:247-252`
displays `C_20(B|i) = Σ_A C_21(B|A) C_10(A|i)` — a composed-scale composition law at three levels,
which the finding asserts appears nowhere. And the package-level charge that the absence goes unfenced
is refuted by text I read directly: `docs/STATUS.md:41` ("equations only; no interacting fixed point
exists"), `:77` ("No interacting fixed point in `07b`. Every exhibited fixed sector is trivial"),
`:193` and `:215` (renormalization listed OPEN), and `overview.md:560-565`, which states that "exact"
governs the equations and not the existence of a fixed point, that every exhibited fixed sector is
trivial, and that the only computed exponent lives in an `O(d)`-reduced sector a general `GL(d)` action
destroys. That fencing is sharper than the fix the finding proposes.

What survives is one documentation defect local to one file: `solid_RG_theory.md` is named for a theory
it does not contain, and its "Certified boundary" section — whose declared function is to enumerate what
is not closed — omits the obligation named in the file's own title. **Medium.**

### P1-High-1 — CONFIRMED as an attribution defect at Low; two clauses REFUTED. I override P0 here.

P0 reached this finding independently and rated it **High** as an "attribution and process" defect, on
the reasoning that a process running sixteen attacks, an oracle-erasure pass, an independent
reconstruction, and four expert reviews "does not notice that the theorem was already proved in the
same repository." I ran the check and the process charge does not survive it.

```
$ grep -rn "06_general" docs/derivations/2026-08-15-full-pointwise-meta-agent/   -> 19 hits
```

Three of the four domain reviews cite the ancestor chapter by exact line range with explicit mapping
sentences: `view-probability-kernel.md:45` — "This is the selected-version-qualified identity **already
proved canonically** (`Theory/06:258-302`)"; `:51` — "consistent with the canonical exact VFE theorem
(`Theory/07b:34-66`)" and "matching the canonical recovery boundary (`Theory/06:124-165`)";
`view-information-vfe.md:112` — "matches `Theory/06_general_coarsegraining.tex:85-165`". The process did
notice, and said so, at the granularity the contract requires. P0's process charge is refuted on this
evidence; P0's *mathematical* claim — that the four results were already `ESTABLISHED` in
`Theory/06` — I verified independently at `git show bd46058:Theory/06` and it stands.

Two further clauses of the finding as filed fail. The contract-violation charge is wrong: I read
`problem-contract.json` `literature_policy` in full and it is disjunctive — "Use only checked primary
sources **or released repository derivations** for invoked theorems; record exact statements and
hypothesis mappings" — and it ends "**No novelty or priority claim is made**." No novelty claim appears
anywhere in the package; `grep -ni "novel\|new theorem\|priority\|original"` over `final-report.md` and
`construction-or-strongest-theorem.md` returns nothing on point. And the "no citation" clause is false
of the reviews.

What survives, and it is real:

```
$ grep -c "Theory/" .../evidence/direct-derivation.md     -> 0
$ grep -rn "cg-" .../2026-08-15-full-pointwise-meta-agent/ -> 0
$ grep -rni "kullback\|csisz" .../2026-08-15-full-pointwise-meta-agent/ -> 0
```

The mathematics document carries no pointer to the theorems it re-derives, so read alone it presents §3
and §6 as first derivations; no prior theorem *label* appears anywhere in the package, so the citations
that do exist are drift-prone line ranges; and the `Kullback1951`/`Csiszar1967` attribution the prior
chapter carries is not carried forward. One cross-reference line per section repairs it. **Low.**

(Incidental correction to P0: the Kullback/Csiszár citation sits at `Theory/06:122`, inside the proof
of `thm:cg-dpi-equality`, not `thm:cg-kl-dpi-extended`.)

### P1-High-3 — CONFIRMED as an internal-consistency defect at Low; the central charge REFUTED

The finding's mathematics is sound — a single-point change to a posterior version on a Lebesgue-null
set changes `F_I` from `log 2` to `0` — and I do not dispute it. The charge that fails is that the
package treats only the evidence term and leaves the KL term untreated. I read the package:

- `direct-derivation.md:45` — "An admitted observation `o` is a point at which this selected version,
  its evidence representative, **and every later slice-wise expression** are declared to be used. No
  arbitrary conditional version is silently evaluated on an unspecified null slice." "Every later
  slice-wise expression" is the KL term.
- `evidence/adversarial-attacks.md:30-36` — attack **A4, "Null posterior versions"**, states the exact
  pathology and is dispositioned "`REJECTED` for `POSTERIOR-PUSHFORWARD` and `VFE-CHAIN-EXTENDED` as
  version-qualified claims. Any canonical-null-version theorem remains outside scope."
  `VFE-CHAIN-EXTENDED` is the KL claim the finding says is untreated.
- `adversarial-report.json:48-54` — `ATTACK-NULL-POSTERIOR-VERSION`, bound to both claim ids, recording
  "Canonical null-slice values are not claimed."

I also checked the finding's endpoint arithmetic by hand and it is wrong: under the frozen premise
`Q_I ≪ Π_I` on a finite space, `KL` is finite, so the reachable range is `[0,∞)`, not `[0,∞]`.
`+∞` requires `Π({0}) = 0`, which the premises forbid.

What survives: three limitation lists — `direct-derivation.md:498` (§9, advertised as the "exact
limitations"), `construction-or-strongest-theorem.md:118`, and `final-report.md:40` — omit a limitation
the same package records as an open gap in its attack register. That is an internal-consistency defect
in the sections that advertise completeness of the limitation list, worth one clause each. **Low.**

### P3-High-1 — CONFIRMED as a summary-prose defect at Low; two evidentiary clauses REFUTED

The finding's title asserts all five negatives refute premises the affirmative theory supplies. Its own
table contradicts that: N1's deleted hypothesis is recorded as "none" and N5's as "the theory never
claims the converse." Exactly two (N2, N3) are premise deletions, which is exactly the set
`final-report.md:40` concedes. The report's usage is type-correct and the proposed fix would make it
less accurate.

Two evidentiary statements in the finding are refuted by execution. First, "they are not recorded in
`claim-ledger.json` at all (I enumerated all 19 claims)". I dumped the ledger:

```
NEG-MARGINAL-DETERMINATION       | ... refuting universal reconstruction of the full parent from those marginals.
NEG-SPLIT-CHANNEL-VFE            | ... violate the unconditional common-channel contraction and VFE identity.
NEG-MODEL-MARGINAL-EVALUATION    | ... refuting model-marginal sufficiency for evaluation compatibility.
NEG-TRIVIAL-HOLONOMY-AGREEMENT   | ... refuting trivial holonomy as sufficient for belief or model agreement.
NEG-MARGINAL-HOLONOMY-JOINT      | ... refuting marginal holonomy invariance as sufficient for full-law invariance.
```

All five are present and each names its refuted universal, four in explicit "X is not sufficient for Y"
form. Second, the load-bearing premise "none of the five was ever a plausible claim" is refuted by this
repository's own manuscript: `Theory/03_probability.tex:430` calls the coordinate marginals "a lossy
summary" and proves `prop:prob-marginals-do-not-determine-joint` at `\status{ESTABLISHED}`, and
`Theory/05_elbo.tex:37` writes "Marginal recognition laws cannot be substituted for the population law
in an exact entropy or evidence calculation, and the following makes **the error** exact rather than
merely warning against it." The program treats N1 as a live error worth exhibiting, not a straw man.

What survives: `final-report.md:20` lists the five inside the "strongest verified result" sentence, and
the seventeen-ancestor count includes them with no type marker, so that one sentence over-reads five
two-atom insufficiency witnesses as substantive theorems. The correct scope is stated in four documents
including the next paragraph of the same file. **Low.**

---

## Unchallenged findings (updated after wave 4)

Rule 5: these were not put to a skeptic, for budget reasons. They are **unchallenged, not confirmed**,
and carry no adjudicated verdict. They must be re-verified before any of them enters the final report
as established. Counts are by the investigator's own severity labels. **Every wave-1 High and Critical
finding has now been challenged and adjudicated** (waves 2 and 4); what remains unchallenged is Medium
and Low only.

- **P1** (measure/probability): 5 Medium, 2 Low.
- **P2** (information/VFE): 5 Medium, 4 Low.
- **P3** (counterexamples): 6 Medium, 4 Low.
- **P4** (gauge/holonomy): 8 Medium, 1 Low.
- **P5** (category/operational): 3 Medium, 4 Low.
- **P6** (Blackwell comparison): 3 Medium, 4 Low.
- **P7** (RG/coarse-graining): 5 Medium, 2 Low.
- **P8** (integration/overclaim): 7 Medium, 3 Low.
- **P9** (self-certification): 2 Medium (`:423`, `:442`), 1 Low (`:456`).
- **P10** (rigor sweep): 7 Medium, 5 Low (two of which are positive "CHECKS OUT" records).

One part of one challenged finding is **INCONCLUSIVE** rather than unchallenged:
`W4-P9-attacks` sub-finding (a). Its skeptic file is `STATUS: IN_PROGRESS` with no verdict, and the
one check that decides it is named in §B.

**Duplicates of adjudicated findings — do not double-count.** Two unchallenged High findings describe
the same underlying defect as findings adjudicated above and are covered by those verdicts:
`P7-rg-coarsegraining.md:110` ("the flagship 8/15 theorem is the only stated result in `Theory/07b`
carrying no proof") is P10-High-2, adjudicated **Medium**; and `P8-integration-overclaim.md:353` ("the
four APPROVE reviews bind manuscript bytes that no longer match the reviewed revision") is
P9-Critical-2, adjudicated **Critical** with the count corrected to two of four reviews.

Two spun-off items surfaced during wave 2 that have no wave-1 counterpart and are therefore not
adjudicated: the non-reproducibility of the three `fingerprint_sha256` values (Low), and
`Theory/07b:151`'s unhedged "No displayed marginal pair reconstructs any of the corresponding full
laws", which lacks the nondegeneracy hypothesis `prop:prob-marginals-do-not-determine-joint` requires
and is falsified by the one-point parent case the surrounding text permits (Low).

Two further spun-off items surfaced during wave 4, likewise recorded but not adjudicated:
`independent-reconstruction.md:46` justifies the extended chain rule by the very clause
(`direct-derivation.md`'s pre-fix "all terms are nonnegative") that the direct proof was corrected to
avoid, and elides (6.3) entirely, so the `DERIVATION`-typed reconstruction did not independently
re-derive the one step with a known defect (Low, favors the investigator on `W4-P9-independence`); and
`release.json:9`'s `strongest_result` field lists the four domain approvals inside the scope of "are
EVIDENCE_VERIFIED **by**" (Low, and it is one item with `W4-P9-regression`, not two).

**Wave-4 counting rules, binding on the final report.** `W4-P4-High-1-blindness` and the wave-2
`P4-High-2` are **one Medium**, not two. `W4-P9-attacks` (b) and the wave-2 `P1-High-1` attribution
finding are **one Low**, not two. `W4-P9-regression` and the `release.json:9` residue are **one
Medium**, not two.

---

## What actually checks out

This section is not a courtesy. It is the larger part of what the evidence shows, and it should carry
the same weight in the final report as the defects above.

**The mathematics is correct wherever it was reconstructed, by three independent parties.** P0 verified
by hand, from the statements alone: that `o ↦ Π_{A,o,X} = Π_{I,o,X} C_A` is genuinely a selected parent
posterior version (the bounded-test-function calculation goes through because `C_A` acts only on the
conditioned variable and leaves `o` fixed — the general "pushforward of a conditional law is a
conditional law of the pushforward" is false and is *not* what is used); that
`Q_{A,o,X} ≪ Π_{A,o,X}`; that the additive extended-real KL chain `KL(Q_I‖Π_I) = KL(Q_A‖Π_A) + Δ_A`
holds with every term in `[0,+∞]` and nothing infinite subtracted; that the zero-defect criterion holds
unconditionally in the direction claimed, needing no finiteness, and that the finiteness premise is
correctly placed on the *subtraction* only; and that the recovery theorem (6.9)–(6.12) is the classical
equality-in-DPI/sufficiency characterization, correctly proved with the finiteness fence in the right
place. The wave-2 skeptics reconstructed the same identities independently and reached the same result.
I re-derived nothing that contradicted them, and the two structural facts I did check directly — that
`thm:rg-exact-coarse-vfe` proves the chain identity correctly at `Theory/07b:34-66`, and that §7's
theorem uses exactly bimeasurability, the intertwining, three pushforward hypotheses and groupoid
composition — hold.

**The fencing is unusually careful and it is not decorative.** `docs/STATUS.md:41,77,193,215` and
`overview.md:560-565` state flatly that "exact" governs the equations and not the existence of a fixed
point, that every exhibited fixed sector is trivial, and that renormalization remains open — fencing
sharper than one wave-1 finding proposed as its own fix. `direct-derivation.md:45` and adversarial
attack A4 disclose the null-slice version dependence and decline any canonical-null-version claim.
`problem-contract.json` states outright that "No novelty or priority claim is made." Three of the four
domain reviews map the derivation onto its canonical ancestors by exact line range. Several wave-1
findings alleged overclaims that the package had already fenced, and those clauses are refuted.

**Two of the three provenance stages are fully auditable.** I recomputed them: 26/26 artifact hashes
verify at `1b18842` for `fix_round_1`, and 26/26 at `8ce6358` for the final release snapshot. The
derivation document itself is recoverable and byte-identical across `1b18842`, `8ce6358`, and HEAD, so
the mathematics any reader wants to check is obtainable.

**The strongest results in the release are the ones nobody attacked.** P0's own reconstructions confirm
in full: the circle heat-pair no-go, verified in Fourier through passive equality, garbling,
strictness, and strict soft-set inclusion — "a clean, genuinely good construction and the strongest
single item across both packages"; the compact metrizable operational quotient, where the countable
dense contextual signature is load-bearing (it is what buys metrizability) and where the joint —
not merely separate — continuity of multiplication is obtained correctly; and the syntactic-congruence
terminality result with its finite-cardinality fence stated correctly. P10 independently logged the
same three as CHECKS OUT.

**Wave 4 adds to this list, not to the defect list.** Four separate claims that wave-1 investigators
filed as High turn out, on execution, to be things the package got *right*:

- The extended `[0,+∞]` tier **is** inside the release, certified as `VFE-CHAIN-EXTENDED` at
  `EVIDENCE_VERIFIED` with no finiteness quantifier. The charge that the release "cannot support it"
  is false, and the finding's proposed fix would have made the documentation less accurate.
- The cross-`X` disclaimer is **not** confined to one paragraph: it is in the theorem's standing setup
  at `direct-derivation.md:6`, restated at `:154` and `:190`, and the `K^{X_A}` superscript is the
  program's canonical parent-evaluator notation at `Theory/SPEC.md:220` and
  `Theory/appendix_notation.tex:60`, not an ad-hoc symbol.
- The frozen contract's fourth conjunct **does not** contradict the released theorem. I recomputed the
  target digest and it covers all eighteen keys; read with its own `quantifiers`, the conjunct is a
  conjunctive obligation over hypothesis-gated branches, and the exclusive-or reading the finding
  attributes to it is not statable inside the frozen quantifier.
- The `EVIDENCE_VERIFIED` closure of `target` **does not** rest on agent agreement. The gate is
  existential, three `DERIVATION` entries carry it, and deleting all six `AGENT_ASSESSMENT` entries
  leaves the release validating clean.

Two mathematical facts were also newly confirmed in wave 4 rather than merely asserted: CE-4's directed
KL really is `½ log 3` in both orientations (exact symbolic), and the extended chain rule and
zero-defect criterion hold with no finiteness anywhere, re-derived a third time via the `φ₀` generator.
And the package's own correction history works: the pre-fix derivation at `add1a69` justified the chain
rule by monotone-truncating a signed integrand, which is invalid, and the released text at
`direct-derivation.md:286` repairs it explicitly and names the error it is avoiding.

**The honest headline.** The mathematics is correct and carefully fenced. What outruns it is the
certification apparatus, and the specific failure is narrower and more mechanical than the panel
alleged: two of four domain approvals are stale against canonical sources that were edited after
approval — one edit inserting the certified theorem itself into the source cited as canonical for it —
and the first of three provenance snapshots binds bytes that are unrecoverable for 11 of 15 entries,
four of which name paths that did not exist at the commit the snapshot claims. The novelty problem is
real but smaller than filed: the contract disclaims novelty, the reviews cite the ancestors by line
range, and the residual is that the mathematics document and the release-facing prose do not. The
flagship theorem's `ESTABLISHED` tag violates the manuscript's own rule by carrying neither a proof nor
a pointer — while sitting ten lines below a proved statement of the same identity. Nothing found in
either wave shows a false theorem.

Wave 4 does not change that headline; it sharpens the second half of it. Every one of the wave-4 High
findings that survives does so as a **label, bookkeeping, or attribution** defect: a branch named
`holonomy-blind` that is neither, an evidence record typed `AGENT_ASSESSMENT` sitting in the field its
own side condition disclaims, a check named for a divergence that is a constant expression, a
syntactic-monoid universal property restated with no attribution in a 466-entry bibliography, a
`regularity` clause contradicting the `statement` in the same frozen object, and a certified
`MATHEMATICAL` row whose statement is a permission rather than a proposition. Two of the eleven are
refuted outright in their load-bearing form and one is inconclusive in part. Across all four waves,
**not one finding has produced a false theorem, a gapped proof, or a claim its own derivation fails to
support.** The defects are in what the package says *about* its mathematics, not in the mathematics —
with one exception worth naming precisely: the attack portfolio contains sixteen over-reading attacks
and zero attacks on triviality or prior art, which is why a package whose core results were already
proved in this repository a week earlier passed sixteen adversarial attacks, an oracle-erasure pass, an
independent reconstruction, and four expert reviews without that ever becoming a finding.
