STATUS: COMPLETE
AGENT: wave-4 adversarial skeptic
TARGET FINDING: W4-P9-regression (High) — "The 8/15 package regressed against the certification
discipline the same author used on 8/14"
SOURCE: `findings/P9-selfcert-falsifiability.md:466`
REVISION UNDER TEST: `8ce635807a6ca2a388255fc996c98f7c535e5843`, branch `review/2026-08-15-deep-review`

# Verdict: UPHELD_REDUCED — corrected severity **Medium**

A real, mechanically reproducible defect exists, and the attack the orchestrator handed me is false.
But the finding is inflated on three counts: two of its eight evidence rows do not survive contact
with the artifacts ("attacks that land", §4; "literature policy", §1a), its core defect is already
carried at High by P9's own `:356` finding (separately under adjudication in this same wave), and the
word "regressed" mischaracterizes both the direction of travel and the source of the standard it is
measured against — the rule sits in the 8/15 package's *own* plan and design spec (§3d), not only in
the 8/14 neighbor.

Everything below is my own machine-read of the artifacts, not a reading of either party's prose.

---

## 1. The table reproduces. Six of eight rows are exact; two fall.

I parsed both ledgers directly (`C:/Python314/python.exe`, stdlib `json`, no torch).

```
======================================================================
P14 2026-08-14-operational-intervention-extensions
schema_version: rigorous-theory-search/v1
n evidence entries: 6
evidence kinds: {'DERIVATION': 3, 'APPLICABLE_THEOREM': 1, 'SYMBOLIC_CHECK': 2}
TARGET evidence kinds: [('EV-DIRECT-DERIVATION','DERIVATION'),
                        ('EV-COUNTEREXAMPLE-DERIVATIONS','DERIVATION'),
                        ('EV-PRIOR-HARD-APPLICABLE-THEOREM','APPLICABLE_THEOREM'),
                        ('EV-INDEPENDENT-RECONSTRUCTION','DERIVATION')]
======================================================================
P15 2026-08-15-full-pointwise-meta-agent
schema_version: rigorous-theory-search/v1
n evidence entries: 11
evidence kinds: {'DERIVATION': 3, 'SYMBOLIC_CHECK': 2, 'AGENT_ASSESSMENT': 6}
TARGET evidence kinds: [('EV-TASK3-DIRECT-DERIVATION','DERIVATION'),
                        ('EV-TASK4-COUNTEREXAMPLE-DERIVATIONS','DERIVATION'),
                        ('EV-TASK5-INDEPENDENT-RECONSTRUCTION','DERIVATION'),
                        ('EV-TASK5-VIEW-PROBABILITY-KERNEL','AGENT_ASSESSMENT'),
                        ('EV-TASK5-VIEW-INFORMATION-VFE','AGENT_ASSESSMENT'),
                        ('EV-TASK5-VIEW-GAUGE-HOLONOMY','AGENT_ASSESSMENT'),
                        ('EV-TASK5-VIEW-DYNAMICS-SCOPE','AGENT_ASSESSMENT'),
                        ('EV-TASK5-ORACLE-ERASURE','AGENT_ASSESSMENT'),
                        ('EV-TASK5-ADVERSARIAL-ATTACKS','AGENT_ASSESSMENT')]
```

Row by row against the finding's table:

| Row | Investigator's claim | My reproduction | Status |
|---|---|---|---|
| Evidence kinds present | P14 `DERIVATION`×3, `SYMBOLIC_CHECK`×2, `APPLICABLE_THEOREM`×1, no `AGENT_ASSESSMENT`; P15 `DERIVATION`×3, `SYMBOLIC_CHECK`×2, `AGENT_ASSESSMENT`×6 | identical, both | **exact** |
| `target.evidence_ids` | P14 four, all derivation-class; P15 nine, six `AGENT_ASSESSMENT` | identical, both | **exact** |
| Domain reviews in package | none / four | `evidence/reviews/*.md`: P14 = 0 files, P15 = 4 files | **exact** |
| `unresolved_obligations` | six populated / `[]` | P14 `release.json` = 6 strings, P15 = `[]` | **exact** |
| Attacks that land | "several (A3, A8, A9, A12, A14, A15)" / "zero" | P14 `adversarial-report.json`: 21 attacks, `Counter({'REJECTED': 21})`. P15: 16 attacks, `Counter({'REJECTED': 16})` | **REFUTED — see §4** |
| Falsification criterion | quoted | verbatim match, both | **exact** |
| Literature policy | quoted | verbatim match, both, but the *inference* fails | **quote exact, inference REFUTED — see §1a** |
| Falsifier check (schema does not force it) | both `rigorous-theory-search/v1`, both `MIXED`, both `COUNTEREXAMPLE` | confirmed: `quantifier_class` `MIXED` in both, `negative_certificate_kind` `COUNTEREXAMPLE` in both | **exact** |

The two quoted contract strings are verbatim. P14: "…an incomplete derivation, unresolved side
condition, missing hypothesis mapping, or missing eligible evidence does not refute the target; it
yields INCONCLUSIVE **and blocks a complete release**." P15: "Inability to derive the affirmative
construction leaves that conjunct unresolved." — with no release consequence anywhere in the field.
P14's `literature_policy` names revision `53cafa374a668ea017a7c50ddbeb75e9045f73a8` and four specific
prior artifacts; P15's names no revision.

### 1a. The literature-policy row is quoted correctly but proves nothing — strike it

This is the one row where the subject-matter defense actually works, and I concede it. Three facts:

1. P15's contract **does** pin revisions, in fields P14's contract does not contain at all —
   `execution_identity.approved_planning_commit = ceffda2d0682b85395421635cabb5e951c888ba7`,
   `execution_identity.fetched_origin_main = 8c0f4d5b4116ac3883665756a451e025f0712b97`,
   `release_assembly.assembly_source_revision = add1a69f2b83550d13abd330c13f4b4e8e9138b9`. P14's
   `problem-contract.json` has only `schema_version`, `contract_id`, `target_digest`, `target`. The
   revision binding moved fields; it did not disappear.
2. P15 imports no prior repository theorem into its target's evidence — **zero** `APPLICABLE_THEOREM`
   entries, and `grep -n "docs/derivations\|Theory/" evidence/direct-derivation.md` returns nothing.
   There is no imported authority whose revision needs pinning. P14 named one because it *did* import
   one: `EV-PRIOR-HARD-APPLICABLE-THEOREM` plus the four named prior artifacts.
3. P15's policy is disjunctive and ends "No novelty or priority claim is made" — the same wording P0
   relied on when withdrawing its own process charge (`P0-principal-reviewer-notes.md:237-240`).

So two of the finding's eight rows fall (this one and "attacks that land"), not one.

## 2. I strengthened the finding beyond what the investigator claimed

The finding is a two-package comparison, which invites the charge of a cherry-picked comparator. It
does not survive. I enumerated every `claim-ledger.json` under `docs/derivations/` at HEAD:

```
2026-08-12-elbo-pifb2-fast-slow-program        {'PRIMARY_SOURCE':2,'DERIVATION':4,'APPLICABLE_THEOREM':1}
2026-08-12-elbo-to-effective-section-action    {'DERIVATION':5,'COUNTEREXAMPLE':1,'APPLICABLE_THEOREM':1}
2026-08-12-exact-two-channel-finite-elbo       {'DERIVATION':6,'APPLICABLE_THEOREM':1,'COUNTEREXAMPLE':1,'PRIMARY_SOURCE':1}
2026-08-12-pifb2-elbo-program-decision         {}
2026-08-13-finite-presentation-descent-joint-fisher  {'DERIVATION':3,'SYMBOLIC_CHECK':1}
2026-08-14-canonical-dependence-selection      {'NONEXISTENCE_PROOF':1,'DERIVATION':4,'SYMBOLIC_CHECK':5}
2026-08-14-collective-joint-lift-fisher        {'DERIVATION':4,'SYMBOLIC_CHECK':7}
2026-08-14-operational-intervention-extensions {'DERIVATION':3,'APPLICABLE_THEOREM':1,'SYMBOLIC_CHECK':2}
2026-08-14-pointwise-meta-agent-rg             {'DERIVATION':2,'SYMBOLIC_CHECK':2}
2026-08-14-typed-intervention-nonidentifiability {'DERIVATION':6,'COUNTEREXAMPLE':1,'SYMBOLIC_CHECK':15}
2026-08-15-full-pointwise-meta-agent           {'DERIVATION':3,'SYMBOLIC_CHECK':2,'AGENT_ASSESSMENT':6}
```

`AGENT_ASSESSMENT` appears in **zero of the ten predecessors** and in six entries of the eleventh.
I then swept the entire git history rather than HEAD:

```
$ git log --all --format="%h" | while read h; do
    n=$(git grep -l "AGENT_ASSESSMENT" $h -- "*claim-ledger.json" | wc -l)
    [ "$n" -gt 0 ] && echo "$h : $n"; done
```

Every hit is `1`, and the earliest is `1b18842` ("docs: certify full pointwise meta-agent",
2026-08-15 15:48:24 −0500). Across the whole repository history, exactly one claim ledger has ever
carried an `AGENT_ASSESSMENT` entry. This is not an inconsistency between two packages; it is a
first, against a pattern held across eleven consecutive releases. The cherry-picking attack fails.

**One honest complication on the placement axis, which the investigator also missed.** The
`AGENT_ASSESSMENT` *kind* is a first. Putting a process-audit artifact into `target.evidence_ids` is
not. `2026-08-12-exact-two-channel-finite-elbo` closes its `MATHEMATICAL` target on five entries that
include `ev-oracle` (`evidence/oracle-erasure.md`) and `ev-reconstruction`
(`evidence/independent-reconstruction.md`) — both typed **`DERIVATION`**. So on the typing axis the
8/15 package is *more* honest than 8/12: it labels an audit an audit instead of calling it a
derivation. The strict practice (audits excluded from target evidence entirely) is 8/13's and 8/14's.
P14 itself keeps `EV-INDEPENDENT-RECONSTRUCTION` in its target, typed `DERIVATION`, exactly as P15
does. The precise delta P14 → P15 is therefore: **oracle erasure, the attack log, and four domain
reviews added to the target's closing set.** The four domain reviews have no precedent in any package
ledger in the repository. State the finding at that resolution and it is unassailable; state it as
"derivation-class evidence only in `target.evidence_ids`" and 8/12 is a counterexample to the claimed
invariant.

## 3. The attack I was handed is REFUTED on three independent grounds

The proposed killer: *the two packages certify different kinds of target — 8/14 largely
finite/algebraic with executable recomputation available, 8/15 measure-theoretic where executable
evidence is inherently limited — so the evidence mix reflects subject matter, not discipline.*

**(a) P14 is not "largely finite/algebraic."** Its own `target.domains` and `regularity` declare
compact metrizable monoids with jointly continuous multiplication, standard-Borel palettes with joint
evaluation measurability, `P(X_ret)` with its evaluation σ-algebra, compact-Polish jointly Feller
kernels with finite topological-order Ionescu–Tulcea recursion, and normalized Haar probability on the
circle with heat-kernel transition probabilities. Its `permitted_theorems` list six families spanning
algebra, general topology, measure theory, and Fourier analysis. P15's `permitted_theorems` list
exactly three, all routine measure theory: "Normalized Markov-kernel pushforward and composition on
standard-Borel spaces", "Existence and use of declared regular conditional probabilities and
disintegrations", "KL data processing and the common-channel conditional-KL chain rule". P0 reached
the same conclusion independently from the mathematics side, calling P14's compact-metrizable quotient
"the most technically substantive result in either package" and the circle heat pair "the strongest
single item across both packages." If either target is the more analytically demanding, it is P14's.

**(b) The executable-evidence variable is held constant, so it cannot be the explanation.** Both
packages have exactly **2** `SYMBOLIC_CHECK` entries, and **both exclude them from
`target.evidence_ids`**, with near-identical side conditions — P14: "The script is corroborative only
for mathematical claims"; P15: "The script is corroboration and is not mathematical closure evidence."
The premise that executable evidence was scarcer for the 8/15 subject matter is also false at the
artifact level: P15's witness runs 51 exact-`Fraction` checks and reproduces byte-identically
(sha256 `ca79ea94…`), which P9 itself verified. Executable evidence was available, was produced, and
was correctly excluded — in both packages. It is not the differing variable.

Two per-claim details make this decisive. P14's two `SYMBOLIC_CHECK` entries attach to exactly one
claim, `OIE-RECOMPUTATION-CORROBORATION`, whose `kind` is **`NUMERICAL_OBSERVATION`** — they close no
mathematical claim anywhere, and P14's contract says so in `permitted_theorems`: "Exact recomputation
may corroborate finite identities but **cannot close a mathematical claim**." So the availability of
`recompute.py` explains nothing about P14's target evidence mix; P14's target closed on
derivation-class evidence alone, which was equally available to P15. Meanwhile P15 wires its finite
witness into **five `MATHEMATICAL` claims** (`NEG-MARGINAL-DETERMINATION`, `NEG-SPLIT-CHANNEL-VFE`,
`NEG-MODEL-MARGINAL-EVALUATION`, `NEG-TRIVIAL-HOLONOMY-AGREEMENT`, `NEG-MARGINAL-HOLONOMY-JOINT`),
each alongside a derivation. The mechanical-evidence dimension runs the *opposite* way from the
defense's prediction: executable evidence is more load-bearing in the 8/15 package, not less.

**(c) The differing kind is not one that subject matter can force.** Domain reviews are a process
artifact available for any subject. Nothing about measure theory makes a review into a derivation.
The governing skill says so in as many words — `~/.claude/skills/rigorous-theory-search/references/proof-obligations.md:7`:

> "Mathematical verification requires direct `DERIVATION`, `FORMAL_PROOF`, or `APPLICABLE_THEOREM`
> evidence… Numerical tests, finite enumeration, symbolic simplification without side conditions,
> figures, and **agent agreement cannot close a mathematical claim**."

and `scripts/validate_run.py:31` defines `MATH_EVIDENCE = {"DERIVATION", "FORMAL_PROOF",
"APPLICABLE_THEOREM"}`. P15's `target` is `kind: MATHEMATICAL`, `state: EVIDENCE_VERIFIED`, with 6 of
9 `evidence_ids` typed `AGENT_ASSESSMENT`. The subject-matter explanation is refuted; the discipline
explanation is what the data supports.

**(d) The rule is written into the 8/15 package's own governing documents, not imported from 8/14.**
This is the evidence that ends the argument, and it also corrects where the finding locates the
standard:

> `docs/superpowers/plans/2026-08-15-full-pointwise-meta-agent.md:28` — "Mathematics closes only by
> direct derivation, formal proof, or hypothesis-mapped theorem. **Computation and agent agreement
> corroborate but do not prove.** Missing evidence yields `INCONCLUSIVE`."

> `docs/superpowers/specs/2026-08-15-full-pointwise-meta-agent-design.md:434` — "Mathematical claims
> close only through derivation or proof."

The 8/14 plan carries the same rule (`plans/2026-08-14-operational-intervention-extensions.md:19`:
"Mathematics closes only by direct derivation… A missing proof or unresolved hypothesis mapping yields
`INCONCLUSIVE` and blocks release"), and P14's frozen contract lifts that sentence verbatim into
`falsification_criterion`. P15's plan carries the mandate and **the frozen contract dropped the
`INCONCLUSIVE` consequence**. That is not two packages differing by design choice; it is the 8/15
contract frozen weaker than the 8/15 plan authorized, which is the one genuinely new,
subject-matter-independent defect this finding contributes.

Both plans also give the domain reviews a designated home, and it is not the package ledger. P14 plan
Task 5 Step 3: "Bind mathematics claims to current derivations and all four independent views" — in
the ignored schema-1.1 `.verification/ledger.json`, closure mode. P15 plan line 401, same
architecture: "One claim per assertion; **derivations close mathematics**; mechanical results close
only mechanical claims. Link four views, skeptic, adjudicator." P15 created that closure artifact
(`docs/verification/reviews/2026-08-15-full-pointwise-meta-agent-closure.md`) *and* duplicated the
four views into the package ledger's target evidence. Nothing in either plan authorizes the second
placement.

Consequence for the title: "the discipline the same author used on 8/14" understates it. The rule is
in the 8/15 plan, the 8/15 design spec, and the skill contract. The accurate statement is *the 8/15
ledger departs from the evidence-eligibility rule its own plan states.*

**Sharpest form of the defect, which the investigator did not extract.** All four review entries carry
this side condition, verbatim, inside the same JSON object that lists them as target evidence:

> "AGENT_ASSESSMENT is adjudication and attack evidence, **not the mathematical derivation that closes
> the target**."

The package states the exclusion rule and then breaks it in the adjacent field. It applies the same
rule correctly to `SYMBOLIC_CHECK` in the same file. That is a self-contradiction inside one released
certification artifact, not a judgment call about subject matter.

**One point that cuts the other way, and I record it.** I executed the skill's own release-mode
validator against both packages:

```
$ validate_run.py --mode release 2026-08-14-operational-intervention-extensions   exit=0
$ validate_run.py --mode release 2026-08-15-full-pointwise-meta-agent             exit=0
```

Both pass. `_claim_eligibility` (line ~613) requires only that *at least one* eligible kind be
present; mixing ineligible kinds into `evidence_ids` is schema-legal. So no automated gate was
bypassed. The violated rule is the reference's prose obligation and the package's own side condition —
real, but not a gate failure. This is also the direct confirmation of the investigator's stated
falsifier: the schema does not force the difference.

## 4. What is wrong with the finding

**The "attacks that land" row is refuted.** The finding asserts P14 had "several (A3, A8, A9, A12,
A14, A15 concede or refute a stronger reading)" against P15's "zero." Machine-read:
`P14/adversarial-report.json` has **21** attacks, `Counter({'REJECTED': 21})`;
`P15/adversarial-report.json` has **16**, `Counter({'REJECTED': 16})`. Both are clean sweeps. Both
prose files carry in-scope qualifications of the same sort — P14 line 140 "REJECTED in scope; the
correlated strengthening is refuted", line 216 "REJECTED as an in-scope attack"; P15 line 4 "It does
not mean the stronger shortcut is true", line 116 "experiment-level recovery remains open". The row
implies a categorical difference in attack outcomes that the artifacts do not show. On this axis P14
is if anything the worse record (21/21). Strike the row.

**"Regressed" mischaracterizes the direction.** The 8/15 package did strictly *more* verification work
than the 8/14 one: four domain reviews, an oracle-erasure pass, sixteen attacks, a 5732-line notation
audit, a 51-check exact-rational witness, and a three-stage provenance chain, against P14's
derivations plus a recompute script. A reader of the title alone infers the later package was less
rigorously checked. It was not. The defect is that the *added* work was mistyped as closing evidence
for a `MATHEMATICAL` claim, not that verification was withdrawn.

**The core defect is double-counted at High.** P9 already carries, at `:356`, "[High] The ledger closes
`target` as EVIDENCE_VERIFIED using evidence the ledger itself types as ineligible" — the same six
`AGENT_ASSESSMENT` entries, stated more directly and without needing the cross-package comparison, and
separately under wave-4 adjudication as `V-W4-P9-ledger-eligibility`. Decomposing what is left:

- the ledger typing → duplicate of P9 `:356` (High, adjudicating separately)
- the falsification criterion with no release consequence → duplicate of P9 `:423` (Medium)
- `unresolved_obligations` semantics → duplicate of P9 `:442` (Medium)
- literature policy naming no authority revision → the P0 prior-work thread, adjudicated **Low**

Every component is already reported at its own severity elsewhere in the same review.
`ADJUDICATION.md:321` sets the governing rule for exactly this situation — "Duplicates of adjudicated
findings — do not double-count" — and applies it to two other findings. It applies here.

Two things survive as this finding's *own* contribution.

First, the historical fact, which is genuine, load-bearing, and stronger than the investigator stated:
`AGENT_ASSESSMENT` is a first across the entire repository history, so the 8/15 package is not merely
inconsistent with one neighbor but breaks a pattern held across all eleven prior releases — and the
four domain reviews in a target's evidence set are a first with no precedent on any axis. That is
corroborating context that materially strengthens P9 `:356`, because it destroys the only real defense
available to that finding ("you are applying an externally imported standard"). It is not an
independent High.

Second, one item that is *not* a duplicate of anything else in P9: the frozen contract's
`falsification_criterion` dropped the `INCONCLUSIVE`-and-block consequence that the 8/15 plan itself
mandates (§3d). P9 `:423` reports the asymmetry but reads it as a design choice; the plan comparison
shows it is a deviation from the package's own authorization. That is a real contract-level defect and
it is what carries the Medium.

## 5. Relation to P0

No contradiction. P0's reconstructions concern the mathematics (the pushforward-version identity, the
KL chain, the recovery theorem, the syntactic monoid, the compact quotient, the circle heat pair) and
all CHECK OUT; this finding concerns evidence typing in a JSON ledger and touches none of them. P0's
closing note — "The certification apparatus should be read as bookkeeping, not as evidence" — points
the same way as the surviving core of this finding, at the same modest weight.

---

## Corrected finding

**[Medium] The 8/15 ledger is the only one in the repository's history to close a `MATHEMATICAL`
target with `AGENT_ASSESSMENT` evidence, contradicting the governing reference and its own side
conditions.**

Location: `2026-08-15-full-pointwise-meta-agent/claim-ledger.json` (`target.evidence_ids`, and the six
`AGENT_ASSESSMENT` entries' `side_conditions`); contrast `problem-contract.json:target.falsification_criterion`
and `:literature_policy` with the 2026-08-14 equivalents.

Scope: reported as corroborating evidence for P9 `:356` rather than as an independent High; the
"attacks that land" and "literature policy" rows struck; "regressed against 8/14" replaced by
"departs from the evidence-eligibility rule stated in its own plan, `plans/2026-08-15-…:28`, which
every prior package honored." The added verification work was mistyped as closing evidence; it was not
withdrawn. Carried as this finding's own new item: the frozen `falsification_criterion` dropped the
`INCONCLUSIVE`-and-block consequence the plan mandates.

Fix, essentially as the investigator wrote it, with the placement stated precisely: keep the four
domain reviews, the oracle-erasure pass, and the attack log out of `target.evidence_ids` and in the
schema-1.1 closure ledger where both plans put them; close `target` on
`EV-TASK3-DIRECT-DERIVATION` + `EV-TASK4-COUNTEREXAMPLE-DERIVATIONS` (+ the reconstruction, as P14
does); and restore the plan's own wording that missing eligible evidence yields `INCONCLUSIVE` and
blocks a complete release.

## Falsifier of my own attack

Four things would show this verdict wrong.

1. **If P9 `:356` (`V-W4-P9-ledger-eligibility`) is refuted or dropped in wave-4 adjudication**, then
   W4-P9-regression becomes the only carrier of the `AGENT_ASSESSMENT`-closure defect, my
   double-counting ground evaporates, and it should stand at **High**. My reduction is contingent on
   that finding surviving; it is not a judgment that the underlying defect is minor.
2. **If any ledger anywhere — a branch, a worktree, a dangling object — uses `AGENT_ASSESSMENT` in
   `target.evidence_ids` before `1b18842`**, my "first in repository history" strengthening collapses
   and the finding weakens to an inconsistency between neighbors. I swept `git log --all` and all
   `.superpowers/worktrees/`; a sweep of unreachable objects via `cat-file --batch-all-objects` would
   close it completely and I did not run one.
3. **If a reference file I did not read requires `target.evidence_ids` to enumerate every artifact the
   release gate cites.** I read `SKILL.md`, `references/proof-obligations.md`, and
   `scripts/validate_run.py`, but not every file under `~/.claude/skills/rigorous-theory-search/references/`.
   If such a requirement exists, P15's six entries are mandated bookkeeping and the finding is
   REFUTED outright rather than reduced.
4. **If P14's `adversarial-attacks.md` prose contains a disposition other than `REJECTED`** that
   `adversarial-report.json` does not record — i.e. the JSON I counted is not faithful to the prose —
   then the "attacks that land" row I struck may be defensible on the prose and my refutation of that
   row is wrong. I checked every `Disposition` line in the P14 prose and all read `REJECTED`, so I
   consider this closed, but the JSON was my primary count.

## Commands and interpreter

All work used `C:/Python314/python.exe` (stdlib `json` only; no torch, no model, no CUDA claim) and
`git` against the working tree at `8ce635807a6ca2a388255fc996c98f7c535e5843`. The validator run used
`~/.claude/skills/rigorous-theory-search/scripts/validate_run.py --mode release`. Nothing in the
repository was modified except this file.

Parsed field-by-field: all eleven `docs/derivations/*/claim-ledger.json` (every claim, every evidence
entry, `kind`/`state`/`evidence_ids` resolved); P14 and P15 `problem-contract.json`, `release.json`,
`adversarial-report.json`. Read: `docs/superpowers/plans/2026-08-14-operational-intervention-extensions.md`
(Task 5) and `…/2026-08-15-full-pointwise-meta-agent.md` (lines 26-30, 297-303, 379-401);
`docs/superpowers/specs/2026-08-15-full-pointwise-meta-agent-design.md:405-452`;
`~/.claude/skills/rigorous-theory-search/{SKILL.md, references/proof-obligations.md,
scripts/validate_run.py:29-31,70-90,600-630}`; `findings/P9-selfcert-falsifiability.md` and
`findings/P0-principal-reviewer-notes.md` in full.
