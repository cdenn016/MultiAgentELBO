STATUS: COMPLETE
AGENT: wave-4 adversarial skeptic (Claude Opus 5)
TARGET REVISION: 8ce635807a6ca2a388255fc996c98f7c535e5843
BRANCH: review/2026-08-15-deep-review
FINDING UNDER ATTACK: W4-P9-ledger-eligibility (severity as filed: High)
VERDICT: **REFUTED**
CORRECTED SEVERITY: None (a distinct Low-severity residual is recorded in §7; it is not this finding)

# Attack on W4-P9-ledger-eligibility

The finding is: *"The ledger closes `target` as EVIDENCE_VERIFIED using evidence the ledger itself
types as ineligible."* I set out to kill it and it dies on three independent grounds, the first two
of which are machine-checkable and were executed.

## 1. Verbatim enumeration of the nine `target.evidence_ids`

Read directly from
`docs/derivations/2026-08-15-full-pointwise-meta-agent/claim-ledger.json` (the `claims[]` entry with
`"id": "target"`, lines 225–235), cross-indexed against the `evidence[]` array (lines 62–205). Each
`kind` is quoted verbatim from the file.

| # | `evidence_ids` entry | `kind` (verbatim) | `supports` | ledger line of the `kind` field |
|---|---|---|---|---|
| 1 | `EV-TASK3-DIRECT-DERIVATION`        | `DERIVATION`       | `true` | 65 |
| 2 | `EV-TASK4-COUNTEREXAMPLE-DERIVATIONS` | `DERIVATION`     | `true` | 80 |
| 3 | `EV-TASK5-INDEPENDENT-RECONSTRUCTION` | `DERIVATION`     | `true` | 119 |
| 4 | `EV-TASK5-VIEW-PROBABILITY-KERNEL`  | `AGENT_ASSESSMENT` | `true` | 156 |
| 5 | `EV-TASK5-VIEW-INFORMATION-VFE`     | `AGENT_ASSESSMENT` | `true` | 169 |
| 6 | `EV-TASK5-VIEW-GAUGE-HOLONOMY`      | `AGENT_ASSESSMENT` | `true` | 182 |
| 7 | `EV-TASK5-VIEW-DYNAMICS-SCOPE`      | `AGENT_ASSESSMENT` | `true` | 195 |
| 8 | `EV-TASK5-ORACLE-ERASURE`           | `AGENT_ASSESSMENT` | `true` | 132 |
| 9 | `EV-TASK5-ADVERSARIAL-ATTACKS`      | `AGENT_ASSESSMENT` | `true` | 144 |

So the split is **three `DERIVATION` and six `AGENT_ASSESSMENT`**. The investigator's arithmetic on
this table is correct.

Two corrections to the framing of the task brief rather than to the investigator. First, **no script
and no `SYMBOLIC_CHECK` entry appears in `target.evidence_ids`.** The two `SYMBOLIC_CHECK` records
(`EV-TASK4-FINITE-WITNESS-SCRIPT` line 95, `EV-TASK4-FINITE-WITNESS-OUTPUT` line 107) are attached
only to the five `NEG-*` claims, never to `target`. The wave-1 text says so explicitly at
P9:390 ("the ledger correctly declines to attach them to `target`"); the "scripts" in the brief's
summary is a paraphrase error, not an investigator error. Second, the finding's own prose at P9:390
says "the two `DERIVATION` artifacts" while its table at P9:369–371 lists three; it discounts
`EV-TASK5-INDEPENDENT-RECONSTRUCTION` on separate grounds. Nothing below turns on that.

## 2. The package's declared schema *does* have an eligibility rule, and it is existential — and satisfied

The ledger declares `"schema_version": "rigorous-theory-search/v1"` (line 2). That schema is not
rhetorical: it is a live, machine-enforced contract shipped at
`~/.claude/skills/rigorous-theory-search/`, whose `references/output-contract.md:37` states that the
release-mode validator checks "per-kind evidence eligibility and polarity."

The rule itself, `scripts/validate_run.py:610–628`:

```python
def _claim_eligibility(claims, evidence, errors):
    for claim_id, record in claims.items():
        ...
        direct = [evidence.get(item, {}) for item in _list_field(record, "evidence_ids")]
        if not any(
            item.get("kind") in eligible and item.get("supports") is expected_support
            for item in direct
        ):
            errors.append(f"claim {claim_id} lacks eligible {state} evidence")
        kinds = {str(item.get("kind")) for item in direct if item.get("supports") is expected_support}
        if kind == "MATHEMATICAL" and state == "EVIDENCE_VERIFIED" and not kinds & MATH_EVIDENCE:
            errors.append(f"mathematical claim {claim_id} lacks direct derivation, formal proof, or applicable theorem")
```

with, at `:29` and `:31`,

```python
EVIDENCE_KINDS = {"DERIVATION", "FORMAL_PROOF", "APPLICABLE_THEOREM", "PRIMARY_SOURCE",
                  "COUNTEREXAMPLE", "NONEXISTENCE_PROOF", "NUMERICAL", "SYMBOLIC_CHECK",
                  "FIGURE", "AGENT_ASSESSMENT"}
MATH_EVIDENCE  = {"DERIVATION", "FORMAL_PROOF", "APPLICABLE_THEOREM"}
```

Three facts follow, all of them fatal to the finding:

1. `AGENT_ASSESSMENT` is a **declared, legal evidence kind** of this schema. The ledger does not
   "type it as ineligible"; the schema types it as admissible-but-non-closing.
2. The eligibility test is **`any(...)` / set-intersection, not `all(...)`**. It requires that at
   least one supporting entry be `DERIVATION`/`FORMAL_PROOF`/`APPLICABLE_THEOREM`. It places no
   upper bound on what else may be listed. `evidence_ids` is therefore, by the schema's own
   semantics, the set of evidence *bearing on* the claim, not a set certified as individually
   closure-sufficient.
3. `target` carries three `DERIVATION` entries with `supports: true`. The rule is satisfied with
   two entries to spare.

The package states this rule itself, in its own words, at `final-report.md:24`: "every mathematical
closure has direct eligible derivation evidence with the correct support polarity" — *has*, not
*consists only of*.

## 3. Executed check: the validator, plus two controls including the finding's own falsifier

Run from the repository root at the branch state. Interpreter `C:/Python314/python.exe` (no torch
involved; this is pure-stdlib JSON/SHA-256 validation).

**Control 0 — released bytes, release mode.** Byte-identical copy of the package at
`scratchpad/ctl0`:

```
$ "C:/Python314/python.exe" .../validate_run.py --mode release docs/derivations/2026-08-15-full-pointwise-meta-agent
exit=0            # no output, no errors
```

**Control A (positive control — is the eligibility check actually live?)** — `target.evidence_ids`
reduced to the six `AGENT_ASSESSMENT` entries, everything else untouched:

```
assessment-only -> ['EV-TASK5-VIEW-PROBABILITY-KERNEL', 'EV-TASK5-VIEW-INFORMATION-VFE',
                    'EV-TASK5-VIEW-GAUGE-HOLONOMY', 'EV-TASK5-VIEW-DYNAMICS-SCOPE',
                    'EV-TASK5-ORACLE-ERASURE', 'EV-TASK5-ADVERSARIAL-ATTACKS']
claim target lacks eligible EVIDENCE_VERIFIED evidence
mathematical claim target lacks direct derivation, formal proof, or applicable theorem
exit=1
```

The check is live and it does exactly what the finding wants it to do: agent assessment alone cannot
close a mathematical claim in this schema. The package is not exploiting a dead gate.

**Control B — the investigator's own stated falsifier.** P9:392 reads: *"Falsifier: Show that the
release would still read `EVIDENCE_VERIFIED` / `COMPLETE_AFFIRMATIVE` with all six
`AGENT_ASSESSMENT` entries removed."* Executed, with all six removed from `target.evidence_ids`:

```
derivation-only -> ['EV-TASK3-DIRECT-DERIVATION', 'EV-TASK4-COUNTEREXAMPLE-DERIVATIONS',
                    'EV-TASK5-INDEPENDENT-RECONSTRUCTION']
exit=0            # release mode, COMPLETE_AFFIRMATIVE, target EVIDENCE_VERIFIED, no errors
```

The release still validates clean as `COMPLETE_AFFIRMATIVE` with `target` at `EVIDENCE_VERIFIED`.
The six `AGENT_ASSESSMENT` entries carry zero load in the closure. The finding's own falsifier
condition is met.

(Scripts and mutated copies are in the session scratchpad, `mutate_ledger.py`, `ctl0/`, `ctlA/`,
`ctlB/`; the mutation touches only `target.evidence_ids` and nothing in `evidence[]`, whose file
hashes the validator recomputes from disk. `release.json` does not bind `claim-ledger.json`'s own
hash, so the mutation is well posed.)

## 4. The imported rule: where "LLM judgment cannot close a claim" actually comes from

The finding labels the six entries *"Ineligible under the operative protocol (LLM judgment cannot
close a claim; agreement among agents is not evidence)"* (P9:373). That parenthetical is not from
this package and not from `rigorous-theory-search/v1`. It is near-verbatim from the user's global
`CLAUDE.md` and from the separate `verification` skill: *"LLM judgment cannot close a claim, and
agreement among agents is not evidence."*

This package never adopted that protocol. Its `schema_version` is `rigorous-theory-search/v1`; it
carries none of the `verification` skill's artifacts (no `mode`, no `artifact_revision`, no
`verifier-adjudicator` records, no `evidence_invalidated` fields). The repository does contain a
`verification`-skill ledger at `.verification/ledger.json`, but it is bound to a different revision
(`git:f9ce06a5…`) and its eleven claims are about PIFB2 observation ontology, plaquette actions, and
fiber homogeneity — nothing to do with the 8/15 pointwise meta-agent run.

And the import fails even on its own terms. The `verification` skill's gate, `verification_gate.py:856–858`:

```python
eligible = _closure_evidence(domain)
if not evidence_kinds.intersection(eligible):
```

— also an intersection test, i.e. also existential. Its contract says `llm_judgment` "may inform
triage but cannot **by itself** assign `EVIDENCE_VERIFIED`" (`references/contract.md:23`, emphasis
mine). Neither the adopted protocol nor the unadopted one forbids co-listing non-closing evidence
alongside a closing derivation. Under the brief's own framing — "violating your own declared rule is
High; failing a rule you never adopted is not a finding against this package at all" — this is the
second case, and it is not even a violation of the rule that was never adopted.

## 5. The alleged self-contradiction does not exist: necessary gate ≠ closure evidence

The finding's strongest move is that the package "agrees they cannot close a claim" and then uses
them anyway (P9:381–386). Read in full, the package's statements are consistent, and they say
something more specific than the finding reports. Each `AGENT_ASSESSMENT` record carries three
`side_conditions`, and the finding quotes the first while omitting the third:

> 1. "AGENT_ASSESSMENT is adjudication and attack evidence, not the mathematical derivation that closes the target."
> 3. "This is a domain-only approval; **final target promotion requires all four current approvals and release-mode validation**."

That is an explicit, self-declared division: the reviews are a *necessary release gate*, and the
derivation is what *closes* the mathematics. `release-assembly.json:121` says the same thing in the
same register — "Review agreement is adjudication and **cannot replace** direct mathematical
evidence." *Cannot replace* is not *cannot be additionally required*. A veto gate whose passage is
recorded in a `reason` string does not thereby become the evidential basis of the closure.

The adopted protocol *mandates* those gates. `SKILL.md:54`: "Every terminal status requires
substantive artifact-backed attacks, independent reconstruction, and oracle erasure covering the
target and every ancestor." `references/adversarial-verification.md:9`: "If any node loses support,
downgrade the release or make it `INCONCLUSIVE`." Conditioning the release on attacks, erasure, and
reconstruction is therefore protocol-compliance, not protocol-violation, and the release gate's
`reason` at `release-assembly.json:193` reads in exactly that structure — closure clause first,
gates after: *"All static ancestors have eligible direct evidence; reconstruction and oracle erasure
pass; all sixteen attacks are rejected; all four corrected-byte domain reviews are current APPROVE
records…"*

## 6. Two of the three supporting quotations are materially truncated

**`oracle-erasure.md:42`.** The finding quotes: *"All four corrected-byte domain reviews are current
and APPROVE …, so oracle erasure leaves no release obligation open and `target` is
`EVIDENCE_VERIFIED`."* The immediately preceding sentence, in the same paragraph, omitted from the
quotation, is:

> "This pass demonstrates only that no desired conclusion was smuggled into the premises; **the
> direct and reconstructed derivations remain the mathematical evidence.**"

The document names its own evidential basis one sentence before the quoted line, and the quoted line
is about a release *obligation* closing, not about evidence. Dropping the fencing sentence
manufactures the contradiction.

**`final-report.md:14`.** The finding says the reviews are listed "under 'Certificate.'" True, and
required — `output-contract.md:35` mandates that the certificate section name the evidence artifacts,
and `SKILL.md:54` mandates that attacks, reconstruction, and erasure be recorded for any terminal
release. But the sentence the finding points at draws the distinction itself: *"**Direct
mathematical support** spans Task 3 … and Task 4 …, with an independent Task-5 derivation, semantic
oracle erasure, and a sixteen-attack adversarial pass. **The corrected-byte reviews are current
APPROVE records…**" — two sentences, two categories.

**`independent-reconstruction.md:8` vs `:62`.** `:8` says the pass "does not promote `target` from
`CANDIDATE`" *and gives the reason in the same sentence*: "same-view bounded re-review remains a
separate release gate." `:62` reports the state after that gate closed. A statement about the state
while a gate is open is not contradicted by a statement about the state after it shuts. (In any
case, that alleged contradiction is the subject of a different P9 finding at :317, not this one.)

## 7. What actually survives — and it is not this finding

One sentence in the package genuinely blurs the distinction. `release.json:9`, the
`strongest_result` summary field:

> "The mixed pointwise target and all seventeen static ancestors are EVIDENCE_VERIFIED **by** direct
> Task-3 and Task-4 derivations, independent reconstruction, semantic oracle erasure, final
> adversarial dispositions, **and four current corrected-byte domain approvals."

The "by" governs a list that ends with the approvals, so a reader could take the approvals as part of
what verifies. That is a **presentational looseness in one summary field**, severity **Low**, located
at `release.json:9` — a file the finding never cites — and it is contradicted by the per-entry
`side_conditions`, by `release-assembly.json:121`, by `final-report.md:14`, by `final-report.md:24`,
and by `oracle-erasure.md:42`'s own fencing sentence. It is a different observation from the filed
finding, not a reduced version of it: it does not concern `target.evidence_ids`, it is not a schema
violation, and the finding's prescribed fix (delete the six `AGENT_ASSESSMENT` entries, P9:394) would
not touch it while stripping records the protocol requires be recorded.

## 8. Relation to the principal reviewer's reconstructions

No conflict. `P0-principal-reviewer-notes.md` reconstructs the posterior-pushforward identity, parent
absolute continuity, and the additive KL chain, and contains no statement about the ledger, evidence
eligibility, or `AGENT_ASSESSMENT`. This verdict neither relies on nor contradicts P0.

## Verdict

**REFUTED.** The package declares an eligibility rule (`rigorous-theory-search/v1`, machine-enforced),
that rule is existential rather than exclusive, and `target` satisfies it with three `DERIVATION`
entries. `AGENT_ASSESSMENT` is a legal declared kind, typed by the package as a necessary release
gate and not as closing evidence, and used exactly that way. The rule the finding actually applies
("LLM judgment cannot close a claim; agreement among agents is not evidence") is imported verbatim
from the user's separate `verification` skill, which this package never adopted — and whose own gate
is likewise an intersection test that this ledger would pass. The finding's own falsifier was
executed and met: with all six `AGENT_ASSESSMENT` entries deleted from `target.evidence_ids`, the run
still validates clean in release mode as `COMPLETE_AFFIRMATIVE` with `target` at `EVIDENCE_VERIFIED`.
An attribution looseness in one summary sentence of `release.json` remains, at Low, as a separate
item.

## Falsifier of my own attack

Any one of the following would overturn this verdict:

1. **A text in the package or in `rigorous-theory-search/v1` that makes `evidence_ids` a
   closure-only set** — i.e. that every listed entry must be of closure-eligible kind, or that a
   non-closing kind must be recorded in some other field. I searched
   `claim-ledger.json`, `release.json`, `release-assembly.json`, `final-report.md`, `SKILL.md`,
   `output-contract.md`, `adversarial-verification.md`, and `validate_run.py` and found the opposite
   at `validate_run.py:619` (`any`) and `final-report.md:24` ("has direct eligible derivation
   evidence"). Produce such a text and the finding revives at High.
2. **A demonstration that Control B is not faithful** — that removing the six entries breaks some
   release requirement my run did not exercise (e.g. an append-only history check, or a hash binding
   of `claim-ledger.json` I missed). `release.json` binds review hashes, not the ledger's hash, and
   the release-mode run exited 0; show otherwise and the "carries zero load" conclusion fails.
3. **Evidence that this run adopted the `verification`-skill protocol** — a `verification` ledger
   entry bound to revision 8ce6358 (or to the run's own artifacts) covering the `target` claim. The
   only such ledger in the repo, `.verification/ledger.json`, is bound to `git:f9ce06a5…` and covers
   unrelated PIFB2/plaquette claims.
4. **A mathematical defect in `EV-TASK3-DIRECT-DERIVATION` or `EV-TASK4-COUNTEREXAMPLE-DERIVATIONS`.**
   My verdict is that the closure rests on those two artifacts and not on reviewer agreement. It says
   nothing about whether their mathematics is correct. If they are wrong, `target` is not verified —
   but that would be a finding against the derivations, not against the ledger's evidence typing, and
   it would still leave this finding refuted as stated.
