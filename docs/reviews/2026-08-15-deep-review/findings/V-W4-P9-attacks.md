# V-W4-P9-attacks — Skeptic attack on finding W4-P9-attacks

STATUS: COMPLETE

**VERDICT: UPHELD_REDUCED.** Corrected severity: **High** for sub-finding (a); **Low** for
sub-finding (b), which is also substantially duplicative of L1.

Target: finding `W4-P9-attacks` (severity High), `findings/P9-selfcert-falsifiability.md:187` and
`:229`. Two grouped charges:
(a) thirteen of sixteen adversarial attacks cannot fail;
(b) the attacks a hostile referee makes first (triviality/prior art, nonvacuity, strawman negatives,
self-certification) are absent.

Summary of what I found, before the detail:

- **(a) survives, and is understated.** My own reclassification gives **15 of 16**, not 13. The
  investigator's own table already contains 14 "No" rows against a stated tally of 13 — an
  arithmetic slip — and A4, which they call the one entry where the attack "demonstrably bit",
  is also contract-determined: the version qualification it supposedly introduced was frozen in
  `problem-contract.json` from the design commit, before Task 5 existed. I verified this with git.
- **The essentiality rescue the brief proposed does not work.** I checked how many of the thirteen
  are premise-essentiality tests: five clean (A5, A6, A7, A9, A10) plus one partial (A2). Those are
  real mathematics and the investigator's one-word label "disclaimed" undersells them. But their
  *disposition* is invariant to whether the witness exists — both branches of the counterfactual
  yield `REJECTED` — so the 16/16 count still carries no information, and their content is imported
  verbatim from `counterexample-proofs.md`, already counted separately as `EV-TASK4`.
- **The location and the quotation are wrong.** `adversarial-attacks.md:4` explicitly self-fences:
  "It does not mean the stronger shortcut is true." The finding's "Claim as stated" block elides
  exactly that sentence with an ellipsis. The artifact is honest; the overclaim lives in
  `release-assembly.json`'s `final_certification_evidence` (`"result": "PASS"`,
  `"attack_disposition": "REJECTED_ALL_16"`) and the `release_gate.reason`.
- **(b)'s load-bearing counter is refuted.** "Strongest verified result" is a *mandated heading*
  from the skill's own output contract, whose gloss is "The strongest-result section states only
  what the evidence proves"; `terminal_status` is a three-valued search-outcome enum mechanically
  bound to the target's ledger state. Neither is a priority claim. On top of that, the frozen
  contract's `permitted_theorems` pre-declares the exact three standard results the "missing
  triviality attack" would have named.

---

## Method

I read all sixteen attacks in `evidence/adversarial-attacks.md` and all sixteen machine records in
`adversarial-report.json`, reclassified them against a criterion I state and defend below, checked
the frozen contract at its first commit, surveyed `strongest_result` usage across eleven sibling
packages and against the skill's schema, and verified the Polyanskiy–Wu citation by extracting the
theorem text from the book PDF. I did not adjudicate by reading either party's prose.

---

## Part (a): the severity charge

### The classification criterion

The investigator's criterion ("could it have succeeded?") is the right one but is stated
informally. I use the sharper form, which the package itself supplies in two places:

1. `evidence/adversarial-attacks.md:4` — "`REJECTED` means the attack does not defeat **the
   recorded scoped claim** because a cited derivation or counterexample supplies the needed
   condition."
2. `problem-contract.json` `target.falsification_criterion` — "An affirmative conjunct is falsified
   **only by an in-domain datum satisfying every frozen premise but violating a stated affirmative
   conclusion**."

Compose them. An attack whose scenario violates a frozen premise, or whose target proposition lies
outside the recorded scoped claim, cannot defeat the recorded scoped claim under (2), and therefore
cannot receive any disposition but `REJECTED` under (1). This is analytic, not interpretive: it is
the package's own two definitions multiplied together. So the classification reduces to a decidable
question — *does the attack's scenario satisfy every frozen premise and contradict a stated
affirmative conclusion?*

### My own reclassification of all sixteen

| # | Attack scenario | Admitted by the frozen premises? | Disposition contingent? |
|---|---|---|---|
| A1 | channel row mass ≠ 1 | No — contract premise 3: "`C_A` is one fixed **normalized** measurable Markov kernel" | **No** |
| A2 | `C_A` chosen after `o,Q,Π` | No — same premise: "**independent of recognition, posterior, and realized observation**" | **No** |
| A3 | generation reads recognition | No — premise 1: "`P_I` is fixed and normalized **before** recognition … and no generative kernel reads `Q` or `Π`" | **No** |
| A4 | version dependence at a null observation | Not contradicted — `equivalence`: "Equality is … **up to their stated almost-sure versions**"; `quantifiers`: "**every selected** posterior `Pi_{I,o,X}`" | **No** (see below) |
| A5 | split channels break VFE | Scenario is premise-deleted; the theorem never asserts it | **No** — but ships a witness |
| A6 | marginals determine the parent | Excluded by `boundary_conditions`: "It excludes … reconstruction of a full parent law from its marginals" | **No** — but ships a witness |
| A7 | model marginal fixes an evaluator | Compatibility is premise 4 | **No** — but ships a witness |
| A8 | quotient regularity | `regularity`: "Any smooth, Gaussian, **quotient**, or bundle regularity is an additional later hypothesis" | **No** |
| A9 | marginal invariance ⇒ joint invariance | `equivalence`: "Equality of recognition marginals is not equality of full parent laws" | **No** — but ships a witness |
| A10 | trivial holonomy ⇒ agreement | `boundary_conditions`: "excludes canonical membership or channel selection" | **No** — but ships a witness |
| A11 | erased marks | `symmetries`: retention branch keeps roots/raw holonomy/boundary records in `H_A` by declaration | **No** |
| A12 | Gaussian leakage | `boundary_conditions`: "It excludes Gaussian generality" | **No** |
| A13 | `∞−∞` in the defect | **Admitted** — the contract permits infinite KL and fences only the subtraction | **Yes** |
| A14 | family-wide recovery | `boundary_conditions`: "excludes … the downstream comparison theorem" | **No** |
| A15 | cross-`X` / patch gluing | `boundary_conditions`: "excludes a full geometric meta-agent and patchwise gluing" | **No** |
| A16 | autonomy/ontology/dynamics/… (×8) | `modeling_postulates`: "does not postulate autonomy, agency, ontology, or physical interpretation" | **No** ×8 |

**My count: 15 of 16 analytically determined; 1 contingent (A13).**

### Where the investigator's number goes wrong

Two errors, both in the direction of understating their own case.

*First, arithmetic.* The finding's tally reads "**13 of 16 cannot fail** (A1–A3, A5–A12, A14–A16);
**2 are genuine hazards** (A4, A13)". Enumerate the parenthesized list: A1,A2,A3 (3) + A5…A12 (8) +
A14,A15,A16 (3) = **14**, and 14 + 2 = 16. The list is right; the number 13 is wrong, and
13 + 2 = 15 ≠ 16 on its face. Their table body confirms 14: fourteen rows read "**No**", two read
"Partly".

*Second, A4.* The finding says at `:219` "A4 is the only entry where the attack demonstrably bit:
it was answered by *weakening* the claim to a version-qualified statement." That is refuted by the
frozen contract's own history. The version qualification is original, not a response:

```
$ git log --oneline -S"up to their stated almost-sure versions" -- ".../problem-contract.json"
c2fe297 docs: design full pointwise meta-agent program

$ git show d287164:".../problem-contract.json" | python -c "...print(d['target']['equivalence'])"
Equality is equality of the declared normalized full laws or kernels up to their stated
almost-sure versions. ...
```

`c2fe297` is the design commit and `d287164` is the first commit of the derivation package; the
attack portfolio is Task-5 work that did not exist at `add1a69` at all. A4's response — "It does not
claim canonical null-slice values or version independence" — restates `equivalence` plus the
`quantifiers` phrase "every **selected** posterior `Pi_{I,o,X}`". No narrowing occurred. A4 belongs
in the analytic group, which is why my count is 15 and not 14.

### The essentiality rescue: checked, and it fails

The brief's proposed kill: *an attack testing whether a frozen premise is essential (deleting it
breaks the theorem) IS a severe test even though the premise is frozen.* I take this seriously,
because it is correct as a principle. So I checked how many of the thirteen (fifteen) are of that
form, meaning the response exhibits a witness demonstrating that the premise cannot be dropped:

- **A5** — `counterexample-proofs.md` §3, identity-versus-constant split channel: fine KL zero,
  coarse forward KL `+∞`. Establishes `NEG-SPLIT-CHANNEL-VFE`.
- **A6** — §2, correlated/anticorrelated fair joints, equal marginals, disjoint support.
- **A7** — §4, row swap on both positive-mass model points.
- **A9** — §5.3, one-coordinate flip preserving both fair marginals.
- **A10** — §5.1, unequal Bernoulli laws on an identity-transport tree.
- **A2** — partial: cites §3 as showing "this restriction is load bearing", but §3 addresses the
  *common*-channel clause, not the *pre-freezing* clause the attack actually targets.

So five clean plus one partial. On that point the investigator's table is unfair: labeling A5–A10 as
"disclaimed" reads as though the response were a scope declaration, when in five cases the response
is an exhibited counterexample. That correction is owed.

**It does not restore severity to the count, for two independent reasons.**

*First, the disposition is invariant.* Take A5. Suppose the split-channel witness exists: the attack
shows the theorem's premise is needed, the theorem is untouched, disposition `REJECTED`. Suppose it
does not exist — i.e. the identity survives split channels: then the attack's own assertion is false,
disposition `REJECTED`. Both branches of the counterfactual land on the same value. The package
states this itself in the machine record, which is the cleanest confirmation available:

```json
{ "id": "ATTACK-SPLIT-CHANNEL-SUPPORT",
  "response": "The finite identity-versus-constant channel witness proves this premise-deleted
               overreach and thereby justifies, rather than refutes, the scoped common-channel
               theorem.",
  "disposition": "REJECTED" }
```
"justifies, rather than refutes" is an admission that no outcome of this attack could have been
adverse. The same reading applies to A6, A7, A9, A10, whose disposition lines each end "and directly
establishes `NEG-…`". An essentiality test *cannot* produce `SUSTAINED` under the artifact's own
definition of the word, because succeeding at it would mean the premise is droppable — which
strengthens the theorem rather than defeating it.

*Second, the content is double-counted.* The five witnesses are not products of the attack pass.
They are `counterexample-proofs.md` §§2–5, already the sole support for the five negative conjuncts
and already carried into the ledger as `EV-TASK4-COUNTEREXAMPLE-DERIVATIONS`. Re-presenting them as
five of sixteen "attacks the package survived" adds no evidence; it adds a second count of the same
lemmas. The investigator names this at `:239` and is right to.

Conclusion on the rescue: it corrects the *characterization* of five entries without touching the
*conclusion*. The 16/16 figure remains uninformative about the target.

### A13, the one contingent entry

A13 is the only attack whose scenario the contract admits: infinite fine KL is permitted, and the
question is whether the derivation actually kept the identity additive in `[0,+∞]` and confined
subtraction to the finite tier. Its answer depended on the text, and at the bytes the domain reviews
name (`add1a69`) the justifying sentence was defective — it called the raw `t log t` integrands
pointwise nonnegative, which is false (`t log t ≥ −1/e` at `t = 1/e`), and was repaired at `1b18842`
by invoking `φ₀(t) = t log t − t + 1`. I do not charge the attack record with mis-disposition,
because `evidence/adversarial-attacks.md` did not exist at `add1a69` and describes post-fix text
correctly. What A13 shows is the shape of a genuinely contingent attack, and that exactly one of
sixteen has it.

### Where the defect actually lives — the finding's location is wrong

`adversarial-attacks.md:4`, in full:

> "`REJECTED` means the attack does not defeat the recorded scoped claim because a cited derivation
> or counterexample supplies the needed condition. **It does not mean the stronger shortcut is
> true.** All four corrected-byte domain reviews are current and `APPROVE` … Every attack below has
> the final disposition `REJECTED`; no attack remains sustained or unresolved."

The finding's **Claim as stated** block quotes the first sentence, then an ellipsis, then the last.
The elided material is precisely the artifact's self-fence. That elision matters: the artifact does
*not* invite the inference the finding says it invites. The prose artifact is honestly typed.

The overclaim is downstream, and the finding's own Location field points at it without using it:

- `evidence/release-assembly.json` `final_certification_evidence` — the attack artifact is recorded
  with `"result": "PASS"` and `"attack_disposition": "REJECTED_ALL_16"`, alongside reconstruction and
  oracle erasure, with no typing of the dispositions.
- `release_gate.reason` — "All static ancestors have eligible direct evidence; reconstruction and
  oracle erasure pass; **all sixteen attacks are rejected**; all four corrected-byte domain reviews
  are current APPROVE records …"
- `adversarial-report.json` `attack_summary` — `{"total":16,"rejected":16,"partially_sustained":0,
  "sustained":0,"unresolved":0}`, four counters of which three are unreachable for 15 of the 16
  records.

So the correct statement of the defect is: *a count that is analytically pinned at 16/16 is named as
one of four grounds in the release gate, and neither the report schema nor the gate carries the
artifact's own caveat that a rejection does not establish the stronger claim.* Severity **High**
stands on that — it voids one of four named pillars of `EVIDENCE_VERIFIED` — but the location moves
from the derivation artifact to the release metadata, and the investigator's Fix (retype the
dispositions into four categories) is the right repair, applied to `adversarial-report.json` and the
gate rather than to the prose.

One over-reach in the finding's Fix text should be trimmed: "only the last two are evidence" is too
strong. A premise-exclusion audit is evidence about whether the release's scope declarations match
its claims, which is worth having. It is simply not evidence about the theorem, which is what the
gate uses it for.

---

## Part (b): the missing-attack charge

### Fact check first

I read all sixteen. None raises triviality/prior art, premise satisfiability, strawman negatives, or
evidential independence. The finding's factual claim is **true**. Everything below concerns what
follows from it.

### The novelty-claim counter is refuted

The brief asks me to settle whether "strongest" is a scope word or a priority claim. It is a scope
word, and not even the author's word — it is imposed by the schema.

*The heading is mandated.* `~/.claude/skills/rigorous-theory-search/references/output-contract.md:19`
lists nine required headings, "these exact final-report headings **and no additional headings**",
including `## Strongest verified result`. The same file glosses it: "**The strongest-result section
states only what the evidence proves.**" The scaffold template
(`assets/templates/final-report.md`) ships that section pre-filled with "No result has been
verified.", and `assets/templates/release.json:9` ships `strongest_result` as "No theorem,
construction, or counterexample has been established." A field whose default value is a confession
of nothing established is not a novelty slot.

*`terminal_status` is an enum, not a boast.* `scripts/validate_run.py:30` —
`TERMINAL_STATUSES = {"COMPLETE_AFFIRMATIVE", "COMPLETE_NEGATIVE", "INCONCLUSIVE"}` — and `:657`
binds them mechanically to the target's ledger state: `{"COMPLETE_AFFIRMATIVE": "EVIDENCE_VERIFIED",
"COMPLETE_NEGATIVE": "REFUTED", "INCONCLUSIVE": "INCONCLUSIVE"}`. `COMPLETE_AFFIRMATIVE` means "the
frozen conjunction resolved affirmatively rather than negatively or not at all". It says nothing
about the literature.

*Sibling usage confirms it.* Across eleven packages in `docs/derivations/`, `strongest_result`
carries scope-limited and sometimes explicitly incomplete statements. Two packages are
`COMPLETE_NEGATIVE`; two are `INCONCLUSIVE`; `2026-08-12-pifb2-elbo-program-decision` reads "a
restricted continuum construction route is credible but **not yet a completed theorem**";
`2026-08-13-finite-presentation-descent-joint-fisher` opens "**On the supported finite tier**";
`2026-08-14-typed-intervention-nonidentifiability` opens "**In the declared finite BSC
subcategory**". No package uses the field to rank against external work.

*And the triviality attack was pre-answered by the frozen contract.* `problem-contract.json`
`target.permitted_theorems`, present at the package's first commit `d287164`, lists exactly the three
standard results the investigator reconstructs:

> "Normalized Markov-kernel pushforward and composition on standard-Borel spaces."
> "Existence and use of declared regular conditional probabilities and disintegrations on the stated
> standard-Borel tier."
> "KL data processing and the common-channel conditional-KL chain rule under the recorded finiteness
> hypotheses."

These are (i), (ii) and (iii) of Missing Attack I, declared as *imports* before Task 1. `final-report.md`
"Scope and limitations" additionally records "Split-channel and incompatible-evaluator witnesses
refute premise-deleted overreach rather than the conditional common-channel theorem" — the
investigator's own recommended honest answer to III, already in the release. And
`literature_policy` has ended "No novelty or priority claim is made" since the design commit.

So the finding's premise — that the release-facing prose "does not read that way" and that
`strongest_result` / `COMPLETE_AFFIRMATIVE` function as novelty claims — is wrong on the schema
evidence. Missing Attack I is a real coverage gap of **Low** severity, and it is L1's territory;
P0's post-wave-2 correction already adjudicated the same substance to Low. I do not re-count it.

### The other missing attacks

**II (nonvacuity)** — the witness exists, and it is cited: A1's response says
"`counterexample-proofs.md` Section 1 checks a concrete deterministic common channel and normalized
tables." I read §1: `M = B = E = {0,1}`, `O = {1}`, `Ξ_A = H_A = {∗}`, normalized rows
`K_m(B=1) = 1/4 + m/2`, `p_X(1) = 1`, `Π_{I,1,X}(m,b,e) = ¼K_m(b)`, `Q_{I,1,X} = ½K_m(b)1_{e=b}`.
It is a satisfying instance, so the conjunct is not vacuous. Note also `p_X(1) = 1`: the admitted
observation in the witness has probability one, which disposes of omission (v) for the exhibited
instance. What is missing is a *label* saying "this is the satisfiability answer". Presentational —
**Low**.

**III (strawman negatives)** — partly wrong on method. Exhibiting a counterexample to show that a
hypothesis cannot be dropped is standard sharpness practice and requires no prior claimant; the
demand at `:239` to "name a source, or a prior claim in this repository's own theory, that asserts
the universal being refuted" applies a standard that would condemn most "the hypothesis is
necessary" remarks in the literature. The genuine residue is the double-count (five negative
conjuncts also counted as five/six rejected attacks), which belongs to (a) and is counted there.

**IV (self-certification)** — true, and duplicative. P9 already reports the substance three times
over as separate findings (oracle erasure as unfalsifiable self-report; the four reviews as
non-independent; the ledger closing on `AGENT_ASSESSMENT`). Naming it a fourth time as a missing
attack adds a location, not a defect.

**(vi) the pairwise converse** — a genuine coverage gap: nothing attacks the direction "a single
normalized reverse kernel `R` recovering both fine laws forces `Δ_A = 0`". But P0 reconstructed that
converse independently (`P0-principal-reviewer-notes.md`, "The recovery theorem (6.9)–(6.12) …
CHECKS OUT, and is classical"), so the absent attack hid no error. Coverage, not correctness.

Aggregate for (b): a real but **Low** coverage/labeling defect, heavily overlapping L1 and P9's own
other findings. High is not defensible for it.

---

## Source checks

**Mayo.** The finding invokes the severity requirement as: a claim passes a severe test only if the
test "would have, with high probability, produced a result that discords with C, were C false".
Verified in substance against secondary literature on *Statistical Inference as Severe Testing*
(CUP 2018): Mayo's two-part formulation is (S-1) H agrees with the data, and (S-2) with high
probability H would not have passed the test so well were H false. The paraphrase is faithful. I did
not confirm the §1.2 locus specifically; §1.2 is "Probabilism, Performance, and Probativeness" and
the requirement is introduced across the Preface and Excursion 1, so the section pointer is loose
but the attribution is correct. Popper, *LScD* §6 (falsifiability as demarcation) and §82 (the
positive theory of corroboration) are apt for "a test must be a genuine attempt at refutation".

**Polyanskiy–Wu.** Verified directly by extracting text from the book PDF
(`people.lids.mit.edu/yp/homepage/data/itbook-2022.pdf`, pp. 49–50):

> "**Theorem 2.14 (Properties of Divergence).** Assume that X and Y are standard Borel. Then
> (a) Conditional divergence can be expressed unconditionally … (b) (Monotonicity)
> D(P_{X,Y}‖Q_{X,Y}) ≥ D(P_Y‖Q_Y). (c) (Full chain rule) … (e) (Conditioning increases divergence)
> … D(P_Y‖Q_Y) ≤ D(P_{Y|X}‖Q_{Y|X}|P_X), with equality iff D(P_{X|Y}‖Q_{X|Y}|P_Y) = 0."

The two-variable chain rule itself is equation (2.24), one theorem earlier, so the citation is off
by one; but Thm 2.14(c) *is* a full chain rule and Thm 2.14(e) is the defect inequality with its
equality criterion, both stated for standard Borel spaces. The investigator's reconstruction — that
the certified identity is the chain rule applied to `Q ⊗ C_A` and `Π ⊗ C_A`, with the shared second
factor forcing the joint derivative to equal the fine one — is correct, and matches P0's independent
reconstruction. The citation substantively holds.

**Kallenberg.** Ch. 8 of the 3rd edition is "Conditioning and disintegration" (confirmed from the
published table of contents), consistent with the citation. I could not obtain the book to confirm
that Thm 8.5 and Thm 6.3 are the specific disintegration and RCP-composition statements. Not
load-bearing: the underlying claim (RCP existence and disintegration on standard Borel is standard)
is independently corroborated by Polyanskiy–Wu's standing standard-Borel hypothesis and by the
repository's own `Theory/06`.

---

## Relation to P0's independent reconstructions

No contradiction. P0's "Open concern (mine): novelty of the central identity — NOT a correctness
finding" reaches the same conclusion as Missing Attack I on the mathematics, and P0's post-wave-2
CORRECTION independently adjudicated the attribution/process charge to **Low** on the same evidence
I use here (`literature_policy` disclaims novelty; the domain reviews do cite `Theory/06` by line
range). My reduction of (b) to Low is consistent with that adjudication, not a new judgment. P0 does
not address the attack portfolio's severity, so (a) is untouched by P0's notes.

---

## Corrected finding, as it should be recorded

**(a) [High] Fifteen of sixteen adversarial dispositions are analytically pinned at `REJECTED`, and
the release gate counts the resulting 16/16 as evidence.** Location:
`evidence/release-assembly.json` `final_certification_evidence` and `release_gate.reason`;
`adversarial-report.json` `attack_summary`. Not `adversarial-attacks.md`, which self-fences at :4.
Five entries (A5, A6, A7, A9, A10) do carry exhibited counterexamples establishing premise
essentiality — genuine mathematics, but imported from `counterexample-proofs.md` and already counted
as `EV-TASK4`, and with dispositions invariant to whether the witnesses exist. Exactly one entry
(A13) had a contingent disposition. Fix: type the dispositions (`premise-excluded` /
`non-claim` / `sharpness-witness, content credited to EV-TASK4` / `new argument required`), report
the last category's count (one), and drop "all sixteen attacks are rejected" from the gate reason.

**(b) [Low] Four hostile-referee questions are absent from the portfolio.** Factually correct.
Severity Low because (i) the frozen contract pre-declares the three standard results as permitted
imports and disclaims novelty, (ii) "Strongest verified result" and `COMPLETE_AFFIRMATIVE` are
schema-mandated scope labels, not priority claims, (iii) the nonvacuity witness exists and is cited,
(iv) the strawman-negatives charge misapplies the standard for sharpness counterexamples, and
(v) the self-certification charge duplicates three of P9's other findings. Overlaps L1; do not
double-count.

---

## FALSIFIER OF MY OWN ATTACK

Two facts would show this verdict wrong.

1. *Against my count of 15 and my endorsement of (a).* Exhibit a scenario that satisfies **every**
   frozen premise in `problem-contract.json` and also defeats a recorded scoped claim, and show that
   it is what one of A1–A3, A5–A12, A14–A16 actually proposes. That would make at least one of those
   dispositions contingent and my "analytically pinned" argument would fail for it. I found none —
   each of the fourteen names a premise, a `boundary_conditions` exclusion, an `equivalence` clause,
   or a `modeling_postulates` disclaimer that its scenario contradicts.

2. *Against my reduction of (b) to Low.* Produce any use, in this repository's packages or in the
   `rigorous-theory-search` schema, of `strongest_result`, `## Strongest verified result`, or
   `COMPLETE_AFFIRMATIVE` that ranks a result against the external literature rather than against
   what the run's own evidence establishes. One such instance would restore the investigator's
   reading that the apparatus makes a novelty claim, and (b) would rise toward the stated severity.
   I checked eleven sibling packages, the output contract, both scaffold templates, and the
   validator, and found the opposite in every case.
