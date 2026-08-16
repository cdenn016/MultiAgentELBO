STATUS: COMPLETE
AGENT: wave-4 adversarial skeptic (independent re-run)
FINDING UNDER ATTACK: W4-P9-fourth-conjunct (severity as filed: High)
TARGET REVISION: 8ce635807a6ca2a388255fc996c98f7c535e5843 (review branch HEAD 3505a53; the
  reviewed package bytes are identical at both — verified below)
BRANCH: review/2026-08-15-deep-review

# Verdict: UPHELD_REDUCED

**Corrected severity: Low.** Charge (ii) — that the released theorem *contradicts* the frozen
contract — is REFUTED outright by frozen contract text the investigator did not read, and by a
structural argument that makes the exclusive-or reading untenable. Charge (i) — that the conjunct is
a modeling declaration with no mathematical content, so certifying it is vacuous — is REFUTED as
stated: the conjunct's affirmative content is a hypothesis-gated conditional theorem whose hypothesis
I showed by exact computation is load-bearing, and whose fence (invariance only on the isotropy
subgroup) is likewise real. What survives is a Low residue at exactly one of the four cited
locations: `claim-ledger.json` `HOLONOMY-ALTERNATIVE` is phrased modally ("a concrete parent **may
declare** either …"), which is a permission rather than a proposition, and the frozen `statement`
sentence read in isolation is ambiguous enough that a competent reader landed on the wrong reading.
Both are repaired by a one-clause gloss. Neither justifies amending a frozen contract, recomputing
`target_digest`, or re-running the reviews, which is what the finding's Fix demands.

A prior wave-4 skeptic file for this finding existed on disk (committed at `3505a53`) recording
REFUTED / None. I did not defer to it. I recomputed everything below independently and land one notch
short of it: the contradiction charge dies, but the ledger-wording residue is real and the prior
attack wrote it off.

---

## 0. Provenance of the wording I am quoting: the digest, recomputed, under a documented rule

The mandate asks whether the package documents a construction rule for `target_digest`. **It does**,
not inside the package but inside the skill the package was produced under —
`C:/Users/chris and christine/.claude/skills/rigorous-theory-search/references/problem-contract.md:11`:

> "Serialize the complete `target` object as UTF-8 canonical JSON with sorted keys, no insignificant
> whitespace, and no non-finite numbers. Its full SHA-256 is `target_digest`, and `contract_id` is
> `contract-sha256-<target_digest>`. … The target claim repeats the exact target statement, kind, and
> quantifiers and carries the same digest, **which binds every remaining structured target field**."

Recomputed (`C:/Python314/python.exe`, stdlib only):

```
$ python - <<'EOF'
import json, hashlib
d = json.load(open('docs/derivations/2026-08-15-full-pointwise-meta-agent/problem-contract.json'))
t = d['target']
print(hashlib.sha256(json.dumps(t, separators=(',',':'), sort_keys=True).encode()).hexdigest())
EOF

file_bytes              e74764ab2db321fe269b48f3e45dca2e16a713df58a83c14d17233f26ab00e08
target_compact_sorted   15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87   MATCH
target_compact_unsorted db26b1e4f7fe13e23f66101d1b167e5e7d3eec060e3a629e16016b26594b66cf
target_indent2_sorted   075e32b8c0feaf8afa0621453c4e97ef4bad7559d82c5041a2b5f4743effddb5
statement_string_only   182b72b94f0405c22f94ffdadcdc97e7855c40dbdd6097d0f3797f593bbf1cda
```

The recorded `target_digest` / `contract_id` is reproduced exactly by hashing the **whole `target`
object**, and is *not* the hash of the `statement` string, the file, or an indented serialization.
The frozen object therefore has eighteen keys:

```
boundary_conditions, codomains, domains, equivalence, falsification_criterion, kind,
literature_policy, measures, modeling_postulates, negative_certificate_kind, permitted_theorems,
premises, quantifier_class, quantifiers, regularity, search_priors, statement, symmetries
```

`quantifiers` and `symmetries` are inside the digest. The finding treats `problem-contract.json:22`
(the `statement` string) as "the frozen contract's wording for it" and argues from that sentence
alone. That premise is false, and its falsehood is what decides charge (ii).

---

## 1. The two sides, quoted verbatim

**Frozen contract, `problem-contract.json:22` (`target.statement`), final affirmative conjunct:**

> "… prove the exact VFE chain identity with its nonnegative conditional-KL defect and equality
> criterion, and **establish exactly one declared full-law holonomy alternative**."

**Frozen contract, `problem-contract.json:25` (`target.quantifiers`), affirmative clause, closing
words — same digest, same freeze:**

> "… and every almost-sure evaluation-compatible parent conditional, the stated parent-law,
> posterior, projection, VFE, **and declared holonomy-alternative conclusions hold**."

**Frozen contract, `problem-contract.json:51-52` (`target.symmetries`), both bullets in full:**

> "For the holonomy-blind alternative, declared joint fine and parent holonomy actions, `C_A`
> equivariance, full-law covariance or invariance, and evaluation compatibility **are required**."
> "For the retention alternative, roots, raw root-framed holonomy, and boundary records remain in
> `H_A`; **no holonomy-blind invariance claim is made**."

**Released theorem, `construction-or-strongest-theorem.md:94`, opening of item 5:**

> "The frozen target declares a holonomy branch; **it does not assert logical exclusivity**, because
> blindness and retention can coexist for different retained coordinates or quotient levels."

**Released ledger, `claim-ledger.json` `HOLONOMY-ALTERNATIVE`:**

> statement: "A concrete parent **may declare** either the fully hypothesis-backed holonomy-blind
> covariance branch or the raw-retention branch. No converse or reconstruction theorem from marginal
> data is claimed here; membership selection remains OPEN."
> quantifiers: "For every concrete parent that declares one branch with that branch's hypotheses."

---

## 2. Charge (ii) — "the released theorem contradicts the frozen contract" — REFUTED

The investigator's own falsifier reads:

> "Show that 'exactly one' in `problem-contract.json:22` was always intended as 'exactly one branch
> is declared by the modeler,' e.g. **via a contemporaneous gloss inside the frozen contract**.
> `problem-contract.json:50-53` (`symmetries`) describes both branches' hypotheses without
> disambiguating 'exactly one,' so the contract does not settle it."

They checked `symmetries` and stopped. The gloss they asked for is in `quantifiers`, three lines
above `symmetries` and inside the same digest: the affirmative conclusion the contract commits to is
that **"the … declared holonomy-alternative conclusions hold"** — the conclusions *of the declared
alternative*. That is verbatim what the released theorem says and verbatim what `HOLONOMY-ALTERNATIVE`
records. There is no contradiction between them; there is a terse sentence and its own gloss, in one
frozen object, hashed together.

Four further facts, each checkable, close the exclusive-or reading off:

**(a) The universal quantifier list contains no holonomy datum at all.** `quantifiers` runs over
`I` at fixed `r_*`, `Y_I`, `B_A, M_A, Xi_A, H_A`, `X` with `X_A = chi_A(X)`, admitted `o`, `P_I`,
`Pi_{I,o,X}`, `Q_{I,o,X}`, `C_A`, `ev_A`, and the a.s. evaluation-compatible parent conditional. No
groupoid, no arrow, no source/target action. Under the XOR reading the affirmative conjunct would
assert "for every such datum, exactly one of {blindness, retention} holds" — but for a generic datum
in that list neither branch is even *statable*, because blindness needs a declared arrow
(`T_O^g, T_I^g, T_A^g`) that the list does not quantify over, and retention needs `H_A` to carry
specific record types that the list leaves free. A reading that makes the sentence not a proposition
about the quantified data is not the reading.

**(b) The XOR reading makes the frozen target flatly false, at a datum I can exhibit.** Blindness and
retention are not complementary; a datum can satisfy neither. Take `Y_I = {0,1,2}`,
`B_A = M_A = Xi_A = H_A = {*}` (singletons, standard Borel), `O = {o_0}`; `P_I(do,dY|X)` normalized
and fixed before any recognition or posterior datum, with finite positive unchanged evidence;
`Pi_{I,o_0,X}` the selected posterior derived from it; `Q_{I,o_0,X} << Pi_{I,o_0,X}`; `C_A` a fixed
normalized measurable Markov kernel on `Y_I` alone, reading neither `Q` nor `Pi` nor the realized `o`;
`ev_A` normalized and measurable and agreeing a.s. with the induced conditional; bridge
disintegrations trivially declared. Every frozen premise `problem-contract.json:56-60` is satisfied.
No groupoid arrow is declared, so `ASM-HOLONOMY-BLIND-DATA` fails; `H_A` is a point, so it carries no
component root, no raw root-framed holonomy, no dressed boundary mark, and
`ASM-HOLONOMY-RETENTION-DATA` fails. **Neither branch holds.** Under the XOR reading this is an
in-domain datum satisfying every frozen premise and violating a stated affirmative conclusion — which
is precisely the contract's own falsification criterion (`:73`) for an affirmative conjunct. So the
XOR reading does not yield "the theorem contradicts the contract"; it yields "the target is refuted,
Critical." The investigator did not claim that and did not exhibit such a datum. A reading on which
the author's own frozen sentence is trivially false, refuted by a three-point space, is the wrong
reading.

**(c) "Declared" means datum-supplied everywhere else in the frozen target, without exception.**
Machine-extracted from the frozen object: "every **declared** standard-Borel fine random space `Y_I`
and parent factors"; "**declared** finite categorical data within the frozen types"; "their
**declared** standard-Borel measurable spaces"; "**declared** joint fine and parent holonomy actions";
"the **declared** normalized full laws or kernels"; "The bridge disintegrations … are **declared**
before the identity is used"; "**declared** regular conditional probabilities and disintegrations".
Every occurrence is datum-supplied. None means "declared once by the contract for all data". So
"exactly one **declared** full-law holonomy alternative" reads with the frozen document, not against
it.

**(d) Grammar: the deliverable-count reading is the parallel one.** The sentence is four verb+object
deliverables: "**construct** the full normalized pointwise parent probabilistic datum **by one**
normalized recognition-independent channel, **derive** its parent posterior and recognition laws and
their projections, **prove** the exact VFE chain identity …, and **establish exactly one** declared
full-law holonomy alternative." The XOR reading requires silently inserting an elided complement
clause — "establish *that* exactly one … *holds*" — which breaks the parallelism the other three
conjuncts keep. And the same numeral idiom occurs earlier in the same sentence, "**by one** normalized
recognition-independent channel", where it is unambiguously a count of what the construction uses,
not a uniqueness claim about the world. (That "one channel" is load-bearing: the split-channel
negative conjunct is the counterexample to using two.)

**On the finding's use of `view-gauge-holonomy.md` falsifier 8.** The quotation is accurate
(`:194`: "Treating the branch declaration as a mathematical exclusive-or, requiring blindness and
retention to be mutually incompatible …"), the gloss is not. Falsifier 8 is a self-guard: the review
lists conditions under which *its own approval* must be withdrawn if the package is found doing the
thing. It forbids the package from overclaiming an exclusive-or; it does not "require rejection" of a
contract conjunct. Section 7 of the same review (`:147`) is a direct, released, in-package resolution
of the same phrase: "The target phrase 'establish exactly one declared full-law holonomy alternative'
is resolved by `ASM-HOLONOMY-ALTERNATIVE-DECLARATION` … It is not a theorem that blindness and
retention are mutually exclusive properties."

**On the finding's provenance parenthetical, which is wrong.** The finding says the diverging theorem
statement "was edited *after* the four reviews (`construction-or-strongest-theorem.md` review-input
`71c56372…` vs released `7a4fe2cf…`)". Content SHA-256 of that file at every revision that touches it:

```
c2fe297 c573e2e5   e058bab 6569e5e7   d287164 bb9bd845
22b5b36 bcaf4630   add1a69 bcaf4630   1b18842 4498334a   a623b6e / HEAD 7a4fe2cf
```

`71c56372` (the hash `release-provenance.json` records for the review-input snapshot) matches **no**
committed revision — that is the separate Critical provenance finding, not this one. What is decidable
here: the four review files did not exist at `add1a69` (`view-gauge-holonomy.md` is absent, empty-hash
`e3b0c442`); they first appear at `1b18842`, **the same commit that introduces item 5's "does not
assert logical exclusivity" sentence** (`4498334a`), and `view-gauge-holonomy.md:147` quotes that very
sentence at that very line number. And `git diff 1b18842 a623b6e` on the theorem file touches only the
witness SHA and the provenance paragraph — **item 5 is byte-identical between the certified and
released versions**. So the released reviews reviewed the disputed sentence; it was not slipped in
behind them.

Charge (ii) fails on every count.

---

## 3. Charge (i) — "a modeling declaration, so certifying it is vacuous" — REFUTED as stated

The declaration is the *hypothesis* of the conjunct, not its content. A conditional theorem whose
antecedent a modeler supplies is ordinary mathematics — "let `G` act on `X` such that …" is the same
shape — and the test of whether it is vacuous is whether the hypothesis is load-bearing and the
conclusion refutable. I reconstructed both and then executed the reconstruction.

**Hand reconstruction of the blindness conclusion (7.5).** For bounded measurable `f` on `Z_A'`,
write `(C_A' f)(Y') = ∫ f dC_A'(Y', ·)`. Hypothesis (7.4),
`C_A'(T_I^g Y, D) = C_A(Y, (T_A^g)^{-1} D)`, says exactly that
`C_A'(T_I^g Y, ·) = (T_A^g)_# C_A(Y, ·)`, so `∫ f(z') C_A'(T_I^g Y, dz') = ∫ f(T_A^g z) C_A(Y, dz)`.
Then

```
∫ f d[(T_A^g)_#(Pi_I C_A)] = ∫∫ f(T_A^g z) C_A(Y,dz) Pi_I(dY)
                           = ∫ (C_A' f)(T_I^g Y) Pi_I(dY)
                           = ∫ (C_A' f)(Y') [(T_I^g)_# Pi_I](dY')      [nothing but change of variables]
                           = ∫ (C_A' f)(Y') Pi'_{I,o',X'}(dY')          [hypothesis (7.2)]
                           = ∫ f d(Pi'_{I,o',X'} C_A').
```

This is the chain displayed at `evidence/direct-derivation.md:442-446`, and it is correct. Note where
the hypotheses enter: (7.4) at line 2 and (7.2) at line 4. Neither is decoration.

**Executed check** (`fractions.Fraction`, exact; script in scratchpad, reproduced here in full effect).
`Y = {0,1,2}`, `Z = {a,b}`, `T_I = (0→1→2→0)`, `T_A = (a↔b)`, `Pi_I = (1/2, 1/3, 1/6)`,
`C_A` rows `(1/4,3/4), (1/2,1/2), (1,0)`; `Pi'_I := (T_I)_# Pi_I` per (7.2) and `C_A'` built per (7.4):

```
Pi_A            = {'a': 11/24, 'b': 13/24}
A. (T_A)#Pi_A   = {'a': 13/24, 'b': 11/24}
A. Pi'_I C_A'   = {'a': 13/24, 'b': 11/24}
A. (7.5) holds under (7.2)+(7.4): True
B. Pi'_I C_A (no 7.4) = {'a': 5/8, 'b': 3/8} | equals (T_A)#Pi_A: False
C. (T_A)#Pi_A == Pi_A (same-slice invariance): False
C'. (T_A)# fair == fair, with T_A != id: True
```

Read off: **A** the conclusion holds under the stated hypotheses; **B** dropping the equivariance
hypothesis (7.4) breaks the conclusion (5/8 vs 13/24), so the hypothesis is load-bearing and the
theorem is not vacuously true; **C** covariance does *not* deliver same-slice invariance for a
non-isotropy arrow, so the fence at `direct-derivation.md:459` ("Same-slice invariance follows only
for isotropy arrows that fix the declared `X` and admitted `o`") is a real restriction, not a
disclaimer; **C'** a nontrivial action can nevertheless stabilize a full law, so the same line's
"Full-frame triviality is one sufficient way … but it is not necessary" is also correct.

A statement with a load-bearing hypothesis, a conclusion that fails when the hypothesis is dropped, a
nontrivial fence, and a well-posed falsifier (`HOLONOMY-BLIND-FULL-LAW`: "An arrow satisfying every
stated covariance/equivariance identity whose pushed full parent law violates the corresponding
covariance identity") is not something that "can be neither verified nor refuted." The vacuity charge
fails.

**Where the investigator did land on something.** Two narrower points survive, and they are the Low
residue:

1. The **retention** half genuinely is definitional. `direct-derivation.md:461`: "Then (3.1) and (3.4)
   retain their joint distributions and every correlation with the other parent coordinates **by
   definition of full-law pushforward**." The document says so itself, so it is disclosed, not hidden;
   but half the fourth conjunct is a restatement of what a pushforward is.
2. `HOLONOMY-ALTERNATIVE`'s statement is **modal, not propositional** — "a concrete parent *may
   declare* either …" is a permission. The ledger schema wants claims to be propositions with truth
   values; the actual propositions live in `HOLONOMY-BLIND-FULL-LAW` and `HOLONOMY-RETENTION`, which
   have their own entries and their own evidence. `HOLONOMY-ALTERNATIVE` is a wrapper whose falsifier
   ("A declared branch satisfying its full hypotheses but not its stated full-law conclusion") is just
   the disjunction of the other two falsifiers. Marking a permission `MATHEMATICAL` /
   `EVIDENCE_VERIFIED` is loose bookkeeping. It does *not* mean the conjunct is uncertified — the
   conjunct's content is carried by the two branch claims, both of which are real — so this is a
   wording defect, not a certification hole.

---

## 4. Relation to the principal reviewer's reconstructions

No conflict. `P0-principal-reviewer-notes.md` reconstructs statement 1 (pushforward of a version),
parent absolute continuity, the KL chain and defect, and the recovery theorem, and marks each CHECKS
OUT; it does not touch statement 5 or the holonomy conjunct. My reconstruction of (7.5) is in the same
family as the principal reviewer's statement-1 calculation — both are bounded-test-function pushforward
arguments through `C_A` — and reaches the same kind of conclusion: correct, elementary, correctly
fenced. The principal reviewer's standing observation that "the novelty is thin and the certification
language oversells it" is consistent with my Low residue and is, in my judgment, the accurate frame for
this conjunct. It is not the frame the finding used.

---

## 5. Corrected finding, as it should be carried forward

**Severity: Low. Category: wording / ledger bookkeeping, not correctness, not contradiction.**

The frozen `statement`'s clause "establish exactly one declared full-law holonomy alternative" is
terse enough to invite an exclusive-or misreading — demonstrably, since a wave-1 investigator with the
whole package open made it. The frozen `quantifiers` field already glosses it correctly, and the
released theorem, the gauge review §7, and `ASM-HOLONOMY-ALTERNATIVE-DECLARATION` all state the
intended reading explicitly. Separately, `HOLONOMY-ALTERNATIVE`'s statement is modal where the schema
wants a proposition.

**Correct fix (not the finding's).** Do *not* amend the frozen target, do *not* recompute
`target_digest`, do *not* re-run the reviews — the contract is not wrong, and re-freezing a correct
contract to fix a gloss would invalidate a certification for no mathematical reason. Instead: (1)
carry one sentence in `final-report.md` and `construction-or-strongest-theorem.md` noting that
"exactly one" counts the branch a datum declares, as `target.quantifiers` already states; (2) restate
`HOLONOMY-ALTERNATIVE` propositionally, e.g. "For every concrete parent declaring one branch together
with that branch's hypotheses, that branch's stated full-law conclusion holds", which is a proposition,
is what the two branch claims prove, and keeps the same falsifier.

---

## FALSIFIER OF MY OWN ATTACK

The single fact that would overturn this verdict: **a released or frozen passage in which the package
asserts, as a conclusion rather than as a hypothesis, that blindness and retention are mutually
exclusive — or asserts the conclusions of *both* branches for one and the same datum.** Either would
restore a genuine contradiction and put the finding back at High. I searched for both and found the
opposite: `grep -rn "exclusive\|exactly one"` over the entire package returns exactly five hits —
`problem-contract.json:22`, its verbatim copy in `claim-ledger.json:210`, and `view-gauge-holonomy.md`
`:60`, `:147`, `:194`, all three of which *deny* exclusivity — and `direct-derivation.md:463` states
the branches disjunctively for a concrete parent ("either it invokes the holonomy-blind covariance theorem under (7.1)-(7.6), or it
retains the raw records and declines a blindness claim").

Secondarily, my charge-(ii) refutation leans on `target.quantifiers` being inside the frozen digest.
If the digest rule were something other than "hash the whole `target` object" — e.g. if it hashed only
`statement` — my central argument would collapse. It does not: `sha256` of the `statement` string alone
is `182b72b9…`, not `15336a68…`, and the skill's `references/problem-contract.md:11` documents the
whole-object rule in words. Both were checked, not assumed.
