# P3 — Finite Negative Constructions (Counterexample Witnesses), Full Pointwise Meta-Agent Package

STATUS: COMPLETE

Reviewer role: adversarial investigator specializing in constructing and destroying finite
counterexamples. Mandate: verify that each exhibited witness actually witnesses the claimed
negative statement, and that the negative statement being witnessed is the interesting one rather
than a premise-deleted strawman.

Review target: git revision `8ce635807a6ca2a388255fc996c98f7c535e5843` (confirmed by
`git rev-parse HEAD`).

**Bottom line.** Every number in `counterexample-proofs.md` is correct — I recomputed all of them
independently and found no arithmetic error anywhere. Nothing here is a Critical finding: no stated
negative result is false. The defects are of the second kind the brief anticipates: the five
negative results are true but far weaker than the surrounding prose implies, all five refute
statements that the affirmative theory never asserts, and the executable "51 of 51" evidence
apparatus contains twelve checks that cannot fail and one — the sole executable check attached to
CE-4's numeric value — that passes for laws with the wrong answer.

---

## PART A — Reproduction (what actually happened)

### A.1 Script execution — the reproduction claims CHECK OUT

Commands run (Git Bash on Windows; `python` = `C:\Python314\python.exe`, Python 3.14.4):

```
cd ".../evidence"
python    finite_nongaussian_witness.py   ->  EXIT_CODE=0, stdout EMPTY
python -O finite_nongaussian_witness.py   ->  EXIT_CODE=0, stdout EMPTY
sha256sum finite-nongaussian-output.json  ->  ca79ea94822e74ad1e7fb3257d0ea852a609a9102be0e49a302687ad1612c062   (both runs)
git status --porcelain                    ->  no tracked file modified
```

The script prints **nothing** to stdout in either mode. "51 of 51 checks pass" is therefore not
observable from a run; it is observable only from the JSON the script rewrites, whose `summary`
block reads `check_count: 51, failed_check_count: 0, passed_check_count: 51`. I counted the
`record(...)` call sites in the source myself and independently get 51 (4 kernel + 12 main-law +
8 main-KL + 7 CE1 + 6 CE2 + 4 CE3 + 10 CE4). Consistent.

Byte-identity between the normal run, the `-O` run, and the committed artifact reproduces exactly.
The mechanism is by construction rather than luck: `record()` (lines 66–69) stores a `bool` instead
of using `assert`, so `-O` has nothing to strip. That is a legitimate design and the evidence
record's side condition states it honestly.

All three SHA-256 bindings in `counterexample-register.md` line 59 verify:

| artifact | claimed | recomputed |
|---|---|---|
| `evidence/counterexample-proofs.md` | `59c38ed4…6de6fc` | matches |
| `evidence/finite-nongaussian-output.json` | `ca79ea94…12c062` | matches |
| `evidence/finite_nongaussian_witness.py` | `15a9eea5…f78835` | matches |

I also ran the skill's own release validator against the package:

```
python "C:/Users/chris and christine/.claude/skills/rigorous-theory-search/scripts/validate_run.py" \
  --mode release ".../2026-08-15-full-pointwise-meta-agent"
-> EXIT 0, no output
```

It passes. Its own docstring reads *"Validate run structure; it cannot establish mathematical
truth."*

### A.2 Independent recomputation — ALL ARITHMETIC CHECKS OUT

I wrote my own script from the *mathematical statements* in `counterexample-proofs.md`, not from
the package's script: `Fraction` probabilities, 60-digit `Decimal` logarithms, and an independently
written `kl()` that returns `+Infinity` on a support violation. Every displayed value reproduces.

Main lossy witness (§1):

- `K_0 = (3/4, 1/4)`, `K_1 = (1/4, 3/4)`, both rows normalized.
- `Π_I`, `Q_I` normalized; `Π_I^{MB} = (3/8, 1/8, 1/8, 3/8)` in the stated order — eq. (1.4) confirmed.
- `Q_A = Π_A = {(0,0):3/8, (0,1):1/8, (1,0):1/8, (1,1):3/8}`, and `Q_A(m,b) = (1/2)K_m(b)` — eq. (1.8) confirmed.
- `q_A^m = q_A^b = Bernoulli(1/2)` confirmed.
- `KL(Q_I‖Π_I) = 0.693147180559945309417232121458176568075500134360255254120680 = log 2` — eq. (1.10) confirmed to 60 digits.
- `KL(Π_I‖Q_I) = +∞` confirmed (support violation at every `e≠b` atom).
- `KL(Q_A‖Π_A) = 0` — eq. (1.11) confirmed.
- All four fibers give `q(·|z) = δ_b`, `π(·|z) = Bern(1/2)`, conditional KL `= log 2`; `Δ_A = log 2` — eq. (1.12) confirmed.
- Chain rule `KL_fine = KL_coarse + Δ_A` holds exactly (`log 2 = 0 + log 2`), hence `F_I = F_A + Δ_A` with `−log p_X(1) = 0`.
- Evaluator compatibility `P(B=b | M=m) = K_m(b)` at all four `(m,b)` — eq. (1.9) confirmed.

CE-1 (N1): identical fair marginals in both coordinates, `R ≠ S`, disjoint supports,
`KL(R‖S) = KL(S‖R) = +∞`. Confirmed.

CE-2 (N2): fine `KL = 0`; split-channel coarse forward `KL = +∞`; reverse coarse `KL = log 2`.
Confirmed. I additionally computed the *common*-channel cases the document does not compute: with
the identity channel on both sides the coarse KL is `0`; with the constant-zero channel on both
sides the coarse KL is `0`. Both consistent with data processing, as expected.

CE-3 (N3): `K_m(B=1) = (1/4, 3/4)` versus `K'_m(B=1) = (3/4, 1/4)`; mismatch at every `m`; swapped
rows still normalized; generative model marginal still `(1/2, 1/2)`. Confirmed.

CE-4 (N4): `KL(Bern(1/4)‖Bern(3/4)) = KL(Bern(3/4)‖Bern(1/4)) =
0.5493061443340548456976226184612628523237452789113747258673 = (1/2)log 3`. Confirmed to 58 digits.
Bit flip stabilizes the fair law. Confirmed.

CE-5 (N5): `T_#R = S` exactly including the zero atoms; both coordinate marginals invariant; joint
not invariant. Confirmed.

**No arithmetic error exists anywhere in `counterexample-proofs.md` or `counterexample-register.md`.**
That is a real result and I report it as such.

---

## FINDINGS

### [High] All five negative results refute premises the affirmative theory itself supplies; the report concedes this for only two of the five

**Location:** `final-report.md` §"Scope and limitations" (line 40) and §"Strongest verified result"
(line 20); `counterexample-register.md` line 61; `evidence/counterexample-proofs.md` §§2–5.

**Claim as stated:**
- `final-report.md:20` — *"The five exact finite negative constructions verify failure of full-law reconstruction from marginals, unconditional split-channel VFE, model-marginal-only evaluator compatibility, agreement from trivial holonomy, and joint invariance from marginal invariance."*
- `final-report.md:40` — *"Split-channel and incompatible-evaluator witnesses refute premise-deleted overreach rather than the conditional common-channel theorem."*

**Defect:** The concession at line 40 names two of five. Tracing each negative against the
affirmative theorem's own hypothesis list shows that **all five** are refutations of statements
obtained by deleting a hypothesis the affirmative theorem explicitly assumes, or of converses the
affirmative theorem explicitly declines. None of the five constrains the affirmative theorem, and
none of the five was ever a plausible claim.

| | negative claim | hypothesis it deletes | where the affirmative theory already declines it |
|---|---|---|---|
| N1 | marginals do not determine the joint | none — but no theorem in the package ever reconstructs a joint from marginals | `construction-or-strongest-theorem.md:55` "These identities do not reconstruct a joint law"; `direct-derivation.md` §5 "asserts only forward coordinate projections" |
| N2 | split-channel VFE fails | the common-channel premise `C_Q = C_Π` (contract `premises[3]`: "`C_A` is **one** fixed normalized measurable Markov kernel") | conceded at `final-report.md:40` |
| N3 | a normalized model marginal does not force evaluator compatibility | the almost-sure compatibility hypothesis (`construction-or-strongest-theorem.md:46`) | conceded at `final-report.md:40` |
| N4 | trivial holonomy does not imply agreement | full-law covariance (7.3), `(T_I^g)_# Q_{I,o,X} = Q'_{I,o',X'}` — the hypothesis that *already asserts* the transported laws match | **not conceded** |
| N5 | marginal invariance does not imply joint invariance | full-law covariance again; the theory never claims the converse | **not conceded**; `direct-derivation.md:383` already says "No converse or reconstruction theorem from marginal identities is claimed here" |

N4 is the sharpest case. Under `direct-derivation.md` §7 the affirmative holonomy conclusion follows
from hypotheses (7.1)–(7.4), of which (7.3) is `(T_I^g)_#\mathbb Q_{I,o,X} = \mathbb Q'_{I,o',X'}`.
Reading the CE-4 tree's two nodes as two objects `(o,X)` and `(o',X')` joined by an arrow `g` with
`T^g = id`, hypothesis (7.3) reads `id_#P = Q`, i.e. `P = Q`. The witness assigns `P = Bern(1/4)`
and `Q = Bern(3/4)`, so it simply **violates (7.3)**. It is exactly as premise-deleted as CE-2 and
CE-3, and the report does not say so.

N5 is likewise a refutation of a converse that `direct-derivation.md:383` explicitly disclaims one
sentence before it is used.

**Evidence:** the hypothesis-by-hypothesis trace above, against `direct-derivation.md` §7 (read in
full, lines 378–420) and `construction-or-strongest-theorem.md` items 3 and 5. Nowhere in the
package is any of the five refuted universals stated as an asserted claim by anyone; they are not
recorded in `claim-ledger.json` at all (I enumerated all 19 claims — none of them is a universal
overreach statement).

**Falsifier:** Exhibit a claim, in this package, in `Theory/`, or in a cited primary source, that
asserts any one of the five refuted universals. If such a claim exists, the corresponding negative
constrains it and my finding is wrong for that item.

**Fix:** Extend the line-40 concession to all five: *"The five negative witnesses refute
premise-deleted or explicitly declined converse statements. They document that the affirmative
theorem's hypotheses are load-bearing; they do not constrain the theorem, and none of the refuted
universals is asserted anywhere in the package or the manuscript."* Then either demote the five from
"verified results" in the line-20 summary to "hypothesis-necessity notes", or drop them from the
seventeen-ancestor count and say so.

---

### [High] `CE4_tree_directed_KL_symbolic_half_log_3` does not test its named claim — it passes for node laws whose directed KL is not (1/2)log 3

**Location:** `evidence/finite_nongaussian_witness.py:321-325`

**Claim as stated:** the check is named `CE4_tree_directed_KL_symbolic_half_log_3`, and
`claim-ledger.json` evidence record `EV-TASK4-FINITE-WITNESS-OUTPUT` scopes the JSON as *"Captured
deterministic PASS output for 51 exact finite checks, including the parent table, forward and
reverse KL orientations, all five counterexamples, and the exact witness totals."*
`counterexample-proofs.md:198-202` asserts `KL(P‖Q) = KL(Q‖P) = (1/2)log 3 > 0`.

**Defect:** The check body is

```python
record(
    checks,
    "CE4_tree_directed_KL_symbolic_half_log_3",
    Fraction(3, 4) - Fraction(1, 4) == Fraction(1, 2),
)
```

It asserts `1/2 == 1/2`. It never reads `node_laws`, never forms a ratio, and never touches the
distributions whose divergence it is named for. It is the **only** executable check attached to
CE-4's numeric value; `CE4_trivial_holonomy_unequal_laws` checks only that the two tuples differ.

**Evidence:** mutation test (scratch script `mutation_test.py`, actual output):

```
node_laws (3/4,1/4) -> (1/4,3/4): check evaluates True; true KL=0.5493061443; (1/2)log3=0.5493061443; named claim holds? True
node_laws (1/2,1/2) -> (1/4,3/4): check evaluates True; true KL=0.1438410362; (1/2)log3=0.5493061443; named claim holds? False
node_laws (9/10,1/10)-> (1/10,9/10): check evaluates True; true KL=1.7577796619; (1/2)log3=0.5493061443; named claim holds? False
```

The check returns `True` for node laws whose directed KL is `0.1438` and `1.7578`. It cannot
discriminate the claimed value from a wrong one.

Note also that the JSON's `identity_tree_directed_KL_decimal_corroboration` is produced at
`finite_nongaussian_witness.py:352` as `Decimal(3).ln() / Decimal(2)` — a hard-typed constant. It is
printed, never compared to anything computed from `node_laws`. So neither the check nor the
"corroboration" constrains the value.

I separately confirmed by independent computation that the claimed value **is** correct
(`0.54930614433405484569762261846126285232374527891137472586734`). The mathematics is right; the
executable evidence for it is empty.

**Falsifier:** Point to any other check in the 51 whose failure would follow from `node_laws` having
a directed KL other than `(1/2)log 3`. I searched all 51 and found none.

**Fix:**

```python
record(checks, "CE4_tree_directed_KL_symbolic_half_log_3",
       node_laws["left"][0] - node_laws["left"][1] == Fraction(1, 2)
       and node_laws["left"][0] / node_laws["right"][0] == Fraction(3, 1)
       and node_laws["left"][1] / node_laws["right"][1] == Fraction(1, 3))
```

i.e. check that both likelihood ratios are `3^{±1}` and that the mass difference is `1/2`, which
together do force `KL = (1/2)log 3`. Alternatively, delete the "decimal corroboration" fields, which
corroborate nothing.

---

### [Medium] Twelve of the fifty-one checks are logically incapable of failing; "51 of 51 checks pass" overstates the executable evidence

**Location:** `evidence/finite_nongaussian_witness.py` (call sites listed below);
`evidence/finite-nongaussian-output.json` `summary.check_count = 51`.

**Claim as stated:** `counterexample-register.md:4` — *"`evidence/finite-nongaussian-output.json` is
deterministic arithmetic corroboration only."* `final-report.md` and the ledger present the JSON as
`SYMBOLIC_CHECK` evidence covering *"51 exact finite checks."*

**Defect:** Twelve of the 51 checks return `True` for every possible value of the mathematical
objects they name. They are not weak tests; they are non-tests.

| line | check | body | why it cannot fail |
|---|---|---|---|
| 84–88 | `main_K_0_B1` | `evaluated_kernel[0][1] == Fraction(1,4)+Fraction(0,2)` | verbatim restatement of the construction expression at line 78 |
| 84–88 | `main_K_1_B1` | same for `m=1` | same |
| 217 | `main_singleton_evidence_one` | literal `True` | — |
| 262 | `CE2_fine_Q_equals_Pi` | `fine_fair == fine_fair.copy()` | one law compared with a copy of itself; `Q` and `Π` are never separately declared |
| 263 | `CE2_fine_KL_zero` | identical expression | same |
| 264 | `CE2_recognition_channel_identity` | `split_recognition_coarse == fine_fair` | `split_recognition_coarse = dict(fine_fair)` two lines earlier |
| 265–269 | `CE2_posterior_channel_constant_zero` | `split_posterior_coarse == {(0,):1,(1,):0}` | compared with the literal it was assigned at line 261 |
| 314 | `CE4_tree_has_trivial_holonomy` | literal `True` | — |
| 315 | `CE4_identity_transport_preserves_node_laws` | literal `True` | — |
| 321–325 | `CE4_tree_directed_KL_symbolic_half_log_3` | `Fraction(3,4)-Fraction(1,4)==Fraction(1,2)` | see previous finding |
| 327 | `CE4_nontrivial_bit_flip` | `tuple(reversed(BITS)) != BITS` | `BITS = (0,1)` is a module constant |
| 328 | `CE4_bit_flip_stabilizes_fair_law` | `tuple(reversed(fair)) == fair` | tuple symmetry, not a pushforward (this one *is* discriminating against a biased law — the weakest item in the list) |

Two further checks are exact duplicates of neighbors: `main_coarse_KL_zero` (line 200) is the
byte-identical expression to `main_parent_laws_equal` (line 121), and
`CE3_mismatch_on_positive_generative_model_mass` (line 304) is the byte-identical expression to
`CE3_generative_model_marginal_fair` (line 294). `main_fine_KL_symbolic_log_2` (line 188) is the
conjunction of two checks already recorded.

The consequence for CE-2 is concrete: **the "fine KL = 0" half of CE-2 has no non-vacuous executable
check at all.** Both checks that name it (`CE2_fine_Q_equals_Pi`, `CE2_fine_KL_zero`) compare one
dict with a copy of itself, so they would pass verbatim if the document had declared
`Q = Bern(1/2)` and `Π = Bern(1/3)`.

**Evidence:** mutation test, actual output:

```
== M2: CE2_fine_Q_equals_Pi / CE2_fine_KL_zero ==
   fine_fair = Bern(1/2) (the real witness): check evaluates True
   fine_fair = Bern(1/3) (a DIFFERENT law): check evaluates True
== M3: main_K_m_B1 ==   m=0: True   m=1: True   (check restates construction verbatim)
== M6: main_singleton_evidence_one / CE4_tree_has_trivial_holonomy /
       CE4_identity_transport_preserves_node_laws: source is the literal `True`
== M7: tuple(reversed(BITS)) != BITS -> True (constant)
```

**Falsifier:** Show a value assignment to `evaluated_kernel`, `fine_fair`,
`split_recognition_coarse`, `split_posterior_coarse`, `BITS`, or `node_laws` that makes any of the
twelve listed checks return `False`. I could not construct one for any of them.

**Fix:** Delete the twelve, or repair them to read the objects they name. Then report the honest
count — roughly 33–35 discriminating checks — rather than 51. Nothing mathematical changes; I
verified all the underlying values independently and they are correct.

---

### [Medium] Two checks are named for claims their bodies do not test

**Location:** `evidence/finite_nongaussian_witness.py:212-216` and `:304-308`

**Claim as stated:** check names `main_total_defect_symbolic_log_2` and
`CE3_mismatch_on_positive_generative_model_mass`.

**Defect:**
- `main_total_defect_symbolic_log_2` has body `sum(recognition_parent.values()) == 1`. That is a normalization check. It says nothing about `Δ_A`. (The preceding check, `main_each_conditional_defect_symbolic_log_2` at line 202, *is* load-bearing and correct; the two together do complete the argument, but the name of this one claims the whole conclusion for a body that supplies only "the weights sum to one".)
- `CE3_mismatch_on_positive_generative_model_mass` has body `all(generative_model_marginal[m] == Fraction(1,2) for m in BITS)`. It never references `mismatch_atoms`. It is the fairness check again under a name asserting mismatch.

**Evidence:** mutation test, actual output:

```
== M4: main_total_defect_symbolic_log_2 ==
   normalized? True  -> check passes regardless of Delta_A
== M5: CE3_mismatch_on_positive_generative_model_mass ==
   with a SWAP-FREE evaluator (no mismatch at all), the expression is still True
```

**Falsifier:** Show that either body's failure would follow from the named claim being false.

**Fix:** Rename to `main_parent_recognition_weights_sum_to_one` and
`CE3_generative_model_marginal_fair_duplicate`, or replace the bodies with
`all(mismatch_atoms)` -style content that reads the object named.

---

### [Medium] CE-2's data are not "within the frozen types": the contract admits exactly one channel

**Location:** `claim-ledger.json` claim `NEG-SPLIT-CHANNEL-VFE`, field `quantifiers`;
`problem-contract.json` `target.premises[2]` and `target.falsification_criterion`;
`evidence/counterexample-proofs.md` §3.

**Claim as stated:** ledger — *"There exists the Task-4 finite categorical split-channel witness
**within the frozen types**."* Contract falsification criterion — *"Each direct finite categorical
witness **within the stated types** establishes its existential negative conjunct."*

**Defect:** The frozen types contain exactly one channel slot: `premises[2]` reads *"`C_A` is **one**
fixed normalized measurable Markov kernel on random fine variables only."* The parent laws are
defined as `Π_A = Π_I C_A` and `Q_A = Q_I C_A` with the *same* `C_A`. CE-2 requires two distinct
channels `C_Q` and `C_Π`. There is no slot for a second channel; a datum carrying two channels is
not an instance of the frozen type system, it is an instance of an enlargement of it. CE-2 also has
no observation coordinate, no `Ξ_A`/`H_A` factors, and no structural `X`, although those are
recoverable as singletons.

This does not make CE-2 false — it is trivially true — but the phrase "within the frozen types" is
incorrect for it, and it is the phrase that licenses the witness to close the conjunct under the
contract's own falsification criterion.

**Evidence:** `problem-contract.json` `target.codomains` lists exactly `Z_A`, `P_A`, `Π_{A,o,X}`,
`Q_{A,o,X}`, `ev_A`. `target.quantifiers` quantifies over *"every normalized measurable
recognition-independent Markov kernel `C_A`"* — one kernel per instantiation. Applying two different
kernels produces two different parents, not one parent with a split channel.

**Falsifier:** A place in `problem-contract.json` or `direct-derivation.md` that types a second,
separately-declared coarse channel for the posterior branch. I did not find one.

**Fix:** Restate the quantifier: *"within the frozen types **enlarged by a second coarse channel**,
an enlargement the affirmative theorem never permits."* Equivalent content, honest typing.

---

### [Medium] CE-4 §5.1 uses a notion of holonomy that is not the one the affirmative theorem uses, and picks the degenerate end of the family

**Location:** `evidence/counterexample-proofs.md:194-204`; compare `evidence/direct-derivation.md`
§7 (lines 381–420) and `problem-contract.json` `target.symmetries[0]`.

**Claim as stated:** *"Take a two-node tree with identity transport on its sole edge. A tree has no
nontrivial based loops, so its holonomy group is trivial."*

**Defect:** Two problems.

1. *Notion mismatch.* The affirmative theorem's holonomy is a **groupoid of bimeasurable actions**
   `T_O^g, T_I^g, T_A^g` on the declared spaces (`direct-derivation.md` §7; contract
   `symmetries[0]`: *"declared joint fine and parent holonomy actions, `C_A` equivariance…"*). There
   is no graph, no edge, no based loop and no transport-along-a-path anywhere in the frozen types.
   CE-4 §5.1 imports *graph/cycle* holonomy instead. §§5.2 and 5.3 do use the pushforward-action
   notion (`g_#F`, `T_#R`) and are in-type; only §5.1 is not.

2. *Degeneracy.* The witness is doubly degenerate: the graph has **no cycles at all** *and* the
   transport is the **identity**. Neither the holonomy structure nor the transport structure is
   exercised. "Trivial holonomy" is achieved by having nothing to compute a holonomy on. The
   informative version of the statement — a connected graph *with* a cycle carrying trivial
   holonomy but *non-identity* transports — is not exhibited, and is exactly the version the
   repository's own manuscript states (see next finding).

**Evidence:** I built the sharper witness in five lines. Three-cycle `1→2→3→1` with the coboundary
link field `U = (id, flip, flip)`, giving `Ω_12 = flip`, `Ω_23 = id`, `Ω_31 = flip`. Actual output of
`sharper_ce4.py`:

```
cycle holonomy trivial (Hol(test) == test): True
non-identity transports present: True True
  edge 2->1: T_#P_2 = Bern(3/4)  vs  P_1 = Bern(1/4)  agree=False  KL=0.549306144334054845697622618461262852323
  edge 3->2: T_#P_3 = Bern(1/4)  vs  P_2 = Bern(1/4)  agree=True   KL=0.00
  edge 1->3: T_#P_1 = Bern(3/4)  vs  P_3 = Bern(1/4)  agree=False  KL=0.549306144334054845697622618461262852323
half log 3 = 0.549306144334054845697622618461262852323
```

Trivial cycle holonomy, two non-identity transports, node laws disagreeing at `(1/2)log 3` on two of
three edges. Strictly stronger than the package's witness and no harder to state.

**Falsifier:** Show that graph holonomy is a declared object in the frozen types, or that the
identity-transport tree exercises a structure the three-cycle version does not.

**Fix:** Either restate §5.1 in the groupoid language the theorem uses ("take the trivial groupoid
action `T^g = id` and two unequal laws; hypothesis (7.3) fails"), or replace the tree with the
coboundary three-cycle above and say explicitly which notion of holonomy is meant.

---

### [Medium] N1 and N4 duplicate results already ESTABLISHED in this repository's own manuscript, and N1 has a standard primary attribution, none of which is cited

**Location:** `evidence/counterexample-proofs.md` §2 and §5.1; `counterexample-register.md` CE-1,
CE-4; against `Theory/03_probability.tex:433-437` and `Theory/12_philosophy.tex:229-236`.

**Claim as stated:** register — *"Status: exact counterexample; closes `NEG-MARGINAL-DETERMINATION`"*
and *"closes `NEG-TRIVIAL-HOLONOMY-AGREEMENT`."* Contract `literature_policy`: *"Use only checked
primary sources or released repository derivations for invoked theorems; record exact statements and
hypothesis mappings."*

**Defect:** Both statements already exist in the repository, at `\status{ESTABLISHED}`, and neither
is cited by the package.

- `Theory/03_probability.tex:433` — `\propositionheading{Coordinate marginals do not determine a
  sufficiently rich joint}{prop:prob-marginals-do-not-determine-joint}`, with a Gaussian proof at
  line 437 and downstream uses at `05_elbo.tex:33`, `05_elbo.tex:289`,
  `06_general_coarsegraining.tex:692`. That is N1.
- `Theory/12_philosophy.tex:229-232` — *"They are independent. A graph coboundary constrains links
  but leaves the means free. Conversely, under nontrivial holonomy, belief agreement can survive on
  the fixed subspace `μ_{i_0} ∈ ker(H_γ^b − I)`."* `\status{ESTABLISHED}`. That is **both** halves
  of CE-4 (§5.1 and §5.2), stated more sharply — the manuscript's version has non-identity
  coboundary transports, the package's has identity transport on a tree.

N1 additionally has a standard primary attribution the package does not give: the non-uniqueness of
a joint law with prescribed marginals is Fréchet's problem (M. Fréchet, *Sur les tableaux de
corrélation dont les marges sont données*, Annales de l'Université de Lyon Sect. A 14 (1951) 53–77),
and the complete description of the freedom is Sklar's theorem (A. Sklar, *Fonctions de répartition
à n dimensions et leurs marges*, Publ. Inst. Statist. Univ. Paris 8 (1959) 229–231).

The package's genuine increment over `prop:prob-marginals-do-not-determine-joint` is that the
witness is finite and categorical rather than Gaussian. That is a real, small increment and should
be stated as such rather than as closure of a fresh claim.

**Evidence:** `grep -rn "prob-marginals-do-not-determine-joint" Theory/*.tex` returns five hits;
`Theory/12_philosophy.tex:220-240` read in full. `grep -rn "Fréchet\|Sklar\|copula"` over the
derivation package: zero hits.

**Falsifier:** Show a citation to `prop:prob-marginals-do-not-determine-joint`,
`Theory/12_philosophy.tex`, Fréchet, or Sklar anywhere in
`docs/derivations/2026-08-15-full-pointwise-meta-agent/`.

**Fix:** One sentence each in `counterexample-register.md`: *"CE-1 is the finite categorical form of
`prop:prob-marginals-do-not-determine-joint` (Theory/03_probability.tex:433), whose released proof
is Gaussian; the classical statement is Fréchet (1951) / Sklar (1959). CE-4 is the finite categorical
form of the independence recorded at Theory/12_philosophy.tex:229-232."*

---

### [Medium] `counterexample-proofs.md:154` states N1 universally; the universal reading is false inside the frozen types

**Location:** `evidence/counterexample-proofs.md:154`

**Claim as stated:** *"This finite witness proves `NEG-MARGINAL-DETERMINATION`: even both complete
coordinate marginals do not reconstruct the full dependence law."*

**Defect:** The ledger claim is correctly existential (*"There exist finite parent laws with
identical belief and model marginals but distinct dependence"*). The prose sentence is universal:
"both complete coordinate marginals do not reconstruct the full dependence law", with no
quantification over which spaces. That universal reading is **false** inside the frozen types.
The contract's `domains` require the declared spaces to be nonempty standard-Borel, and singletons
are admitted — the package's own §1 witness sets `O = {1}`, `Ξ_A = {∗}`, `H_A = {∗}`. If either
retained coordinate space is a singleton, the joint *is* determined by its marginals. The
repository's manuscript states exactly this exception at `Theory/03_probability.tex:434`: *"Without
it the conclusion can fail: for one agent and one design point with `K_{i,a} = M_{i,a} = {0}`, the
space `Y_D` is a singleton and its unique law is determined by its marginals."*

**Evidence:** Take `B_A = {0}`, `M_A = {0,1}`. `P(B_A × M_A)` has two atoms, the `M_A`-marginal has
two free parameters minus normalization = one, the joint has the same, and the map is a bijection.
So marginals determine the joint. Verified by inspection; no computation needed.

**Falsifier:** Show that the frozen types exclude singleton or otherwise degenerate factor spaces.
`problem-contract.json` `domains` says only "nonempty standard-Borel", and §1 of the proof document
uses singletons.

**Fix:** *"…: there exist parent laws whose belief and model marginals agree while their dependence
differs. (The universal form requires a richness hypothesis — with a singleton factor the marginals
do determine the joint; cf. `prop:prob-marginals-do-not-determine-joint`.)"*

---

### [Medium] The DERIVATION/`supports: true` bookkeeping is schema-legal but converts five refutations into five verifications, leaving nothing REFUTED and moving the refuted universals out of the checkable ledger

**Location:** `final-report.md:24`; `claim-ledger.json` claims `NEG-*` and evidence
`EV-TASK4-COUNTEREXAMPLE-DERIVATIONS`; `problem-contract.json`
`target.negative_certificate_kind`.

**Claim as stated:** `final-report.md:24` — *"The five existential negative claims remain verified by
`DERIVATION` evidence with `supports: true`; no `COUNTEREXAMPLE` evidence kind is attached to those
affirmative existential claim records."*

**Defect:** Legal, disclosed, and consequential. Three things follow.

1. **The frozen contract's declared negative certificate is never produced.**
   `problem-contract.json` sets `negative_certificate_kind: "COUNTEREXAMPLE"`, and the skill's
   `references/problem-contract.md` says *"A mixed target must choose explicitly from the frozen
   quantifier structure; the validator does not infer one."* The package chose COUNTEREXAMPLE and
   then attached zero COUNTEREXAMPLE evidence anywhere. The validator does not catch this — it only
   enforces `UNIVERSAL ⟹ COUNTEREXAMPLE` (`validate_run.py:261`) — and I confirmed
   `validate_run.py --mode release` exits 0 on this package. So the contract's frozen negative
   certificate kind is decorative.

2. **No claim in the ledger is ever `REFUTED`.** Because the refuted universals are not entered as
   claims, the ledger reads as 19/19 `EVIDENCE_VERIFIED` with `unresolved_obligations: []`. Had the
   five universals been entered and refuted, the ledger would carry five `REFUTED` rows. The chosen
   encoding produces a uniformly affirmative artifact.

3. **The substance is outside the machine-checkable part.** Which universal is being refuted, and
   whether anyone ever asserted it, appears only in prose (`counterexample-register.md:61`,
   `final-report.md:40`). The ledger — the artifact the validator checks — records five true
   existentials about `{0,1}`-valued distributions and nothing about what they refute. A reader who
   audits the ledger mechanically learns nothing about the first High finding above.

To be fair to the package: this is disclosed at `counterexample-register.md:61` and
`final-report.md:24`, and the register's closing paragraph (line 63) is an honest scope fence. My
objection is that the encoding makes the certification's headline count ("eighteen ancestors, all
EVIDENCE_VERIFIED") read as eighteen positive results when five of them are trivial existentials
about a two-atom sample space.

**Evidence:** enumerated all 19 ledger claims and all 11 evidence records; kinds are
`DERIVATION ×3`, `SYMBOLIC_CHECK ×2`, `AGENT_ASSESSMENT ×6`. No `COUNTEREXAMPLE`, no
`NONEXISTENCE_PROOF`, no `supports: false` anywhere. Validator exit 0.

**Falsifier:** A `COUNTEREXAMPLE`-kind evidence record, or a `REFUTED` claim, anywhere in
`claim-ledger.json`.

**Fix:** Either (a) add the five refuted universals as `REFUTED` claims with `COUNTEREXAMPLE`
evidence, honoring the frozen `negative_certificate_kind`, or (b) change
`negative_certificate_kind` and say plainly in `final-report.md` that the negative conjuncts are
encoded as existential verifications and that the five refuted universals are not asserted anywhere
in the program.

---

### [Low] The chain-rule identity `F_I = F_A + Δ_A` asserted in §1 has no executable check

**Location:** `evidence/counterexample-proofs.md:136`; `evidence/finite_nongaussian_witness.py`
(absent).

**Claim as stated:** *"Because the unchanged evidence term is `−log p_X(1) = 0`, equations
(1.10)–(1.12) also give the exact VFE identity `F_I = F_A + Δ_A`."*

**Defect:** `grep -n "Delta_A\|chain\|addit" finite_nongaussian_witness.py` returns only the two JSON
payload lines 424–425. No check compares `fine_KL` with `coarse_KL + Δ_A`. This is the one identity
in §1 that is the actual point of the witness, and it is the one with no corresponding check.

**Evidence:** the grep above; and my own recomputation, which confirms the identity holds exactly
(`log 2 = 0 + log 2`, `CHAIN RULE KL_fine == KL_coarse + Delta_A ? True`).

**Falsifier:** a check in the 51 that reads all three quantities.

**Fix:** the surrogate is one line, since all three values are symbolic multiples of `log 2`:
`record(checks, "main_chain_rule_log2_equals_zero_plus_log2", fine_ratio == 2 and recognition_parent == posterior_parent and all(conditional ratios == 2))`.

---

### [Low] The register's CE-5 has no corresponding check prefix

**Location:** `counterexample-register.md:30-34` versus
`evidence/finite_nongaussian_witness.py:326-345`.

**Defect:** The register enumerates CE-1 … CE-5. The script's check names use prefixes `main_`,
`CE1_`, `CE2_`, `CE3_`, `CE4_` only; CE-5's four checks are filed under `CE4_` names
(`CE4_joint_action_maps_correlated_to_anticorrelated`, `CE4_first_marginal_invariant`,
`CE4_second_marginal_invariant`, `CE4_full_joint_not_invariant`). A reader mapping register entries
to executable evidence finds no CE-5 evidence.

**Evidence:** the 51 check names in `finite-nongaussian-output.json` lines 3–53; no key begins
`CE5`.

**Fix:** rename the four to `CE5_*`.

---

### [Low] `main_model_prior_marginal_fair` / `main_belief_prior_marginal_fair` compute posterior marginals, conflating exactly the distinction §1 warns about

**Location:** `evidence/finite_nongaussian_witness.py:143-152`;
`evidence/counterexample-proofs.md:93`.

**Claim as stated:** `counterexample-proofs.md:93` — *"this numerical equality does not identify
prior and recognition types in general."*

**Defect:** Both checks named "prior" evaluate `marginal(posterior_parent, ·)`, i.e. the marginal of
`Π_A`, not of the latent prior `P_A^Z(·|X)`. In this singleton-observation instance the two objects
coincide (I verified: `P_I`'s `Y`-marginal equals `Π_I` because `P(O=1) = 1`), so nothing is
numerically wrong. But the script performs precisely the prior/posterior identification the prose
warns against, and since `posterior_parent == recognition_parent` is separately checked, these two
checks are also arithmetically identical to `main_model_recognition_marginal_fair` and
`main_belief_recognition_marginal_fair`.

**Evidence:** lines 143–152 read `posterior_parent`; lines 133–142 read `recognition_parent`; line
121 checks the two are equal.

**Fix:** rename to `main_model_posterior_marginal_fair` / `main_belief_posterior_marginal_fair`, or
construct `P_A^Z` explicitly and check that.

---

### [Low] The witness script produces no stdout and silently overwrites a tracked repository file

**Location:** `evidence/finite_nongaussian_witness.py:461`

**Defect:** `OUTPUT_PATH.write_text(...)` rewrites the committed
`evidence/finite-nongaussian-output.json` as a side effect of running the script. A reviewer
following the package's own reproduction instruction modifies a tracked artifact. It happens to be
byte-identical here — which is why `git status` stayed clean in my runs — so the only real cost is
that the reproduction claim "51 of 51 checks pass" is invisible at the console. A reader who runs the
script sees an empty terminal and must diff the JSON to learn anything.

**Evidence:** both runs produced empty stdout and exit code 0; `git status --porcelain` unchanged.

**Fix:** print the summary line to stdout, and accept an `--output` path or a `--check` mode that
compares against the committed file instead of overwriting it.

---

## THINGS THAT CHECK OUT (reported honestly, with zero findings)

1. **Every rational value, marginal, support statement, likelihood ratio, and KL value in
   `counterexample-proofs.md` is correct.** I recomputed all of them independently. No arithmetic
   error exists in the document.
2. **The main lossy witness (§1) is internally exact and satisfies the affirmative theorem's
   hypotheses.** One recognition-independent deterministic channel; `Q_I ≪ Π_I`; normalized rows;
   finite evidence; and the evaluator is genuinely compatible (`P(B|M=m) = K_m`). `Δ_A = log 2`,
   `F_A = 0`, `F_I = log 2`, chain rule exact. It is a legitimate non-Gaussian instance of the
   Task-3 construction, and calling it "lossy" is accurate rather than flattering.
3. **The `-O` byte-identity claim reproduces**, and the mechanism (`record()` instead of `assert`)
   is honest engineering rather than a trick.
4. **All three SHA-256 bindings in the counterexample register verify.**
5. **The package passes its own release validator** (`validate_run.py --mode release`, exit 0).
6. **The `+∞` orientations are handled correctly and are not swapped.** §1 correctly records
   `KL(Π_I‖Q_I) = +∞` as *not* interchangeable with the VFE orientation, §3 correctly records the
   reverse coarse KL as `log 2` and does not substitute it, and CE-1 correctly notes both directions
   are `+∞` from disjoint supports. This is the place a sloppy witness would break and it does not.
7. **The register's closing scope paragraph (line 63) is an accurate, non-inflated fence.** *"The
   witnesses do not establish an impossibility theorem for every coarsening, a converse to data
   processing, evaluator uniqueness on null fibers, quotient regularity, dynamics, autonomy,
   ontology, or gluing."* That is exactly right and I found no violation of it.
8. **No Gaussian family or approximation is used anywhere**, as claimed. All arithmetic is
   `Fraction`.
9. **CE-3's mismatch really does land on positive generative mass** at both model points, and the
   document is careful to measure it against `P_A^M` rather than `q_A^m` — a distinction it flags
   explicitly and gets right.

## Coverage

Read **in full**:
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/counterexample-proofs.md` (222 lines — the brief said 594; the file at this revision is 222)
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/counterexample-register.md` (63 lines)
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/finite_nongaussian_witness.py` (466 lines)
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/finite-nongaussian-output.json` (265 lines)
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/construction-or-strongest-theorem.md` (118 lines)
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/final-report.md` (40 lines)
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/problem-contract.json`
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/release.json`
- all 19 claims and all 11 evidence records of `claim-ledger.json`
- `~/.claude/skills/rigorous-theory-search/references/problem-contract.md`, `references/proof-obligations.md`

**Sampled** (targeted reads/greps, not full):
- `evidence/direct-derivation.md` — §7 holonomy typing (lines 378–420) read in full; §§1–6 and 8 sampled by grep only
- `evidence/adversarial-attacks.md` — grepped for counterexample-related attacks; individual attack texts not read line by line
- `Theory/03_probability.tex` (lines 430–465), `Theory/12_philosophy.tex` (lines 220–245), `Theory/09_coarsegraining.tex` (holonomy grep), `Theory/SPEC.md` (grep)
- `~/.claude/skills/rigorous-theory-search/scripts/validate_run.py` — grepped for the evidence-kind and certificate-kind logic; executed, not read in full

**Not reached** (outside my scope, or deliberately not inherited per the brief):
- `evidence/independent-reconstruction.md`, `evidence/oracle-erasure.md`, `evidence/reviews/*` (the four internal domain reviews), `evidence/notation-*`, `evidence/release-*`, `adversarial-report.json`, `approach-registry.json`, `dependency-dag.json`
- the full text of `evidence/direct-derivation.md` outside §7

Scratch scripts (not in the repository):
`%TEMP%\claude\C--Users-chris-and-christine-Desktop-MultiAgentELBO\dee27a29-…\scratchpad\`
— `indep_recheck.py` (independent recomputation), `mutation_test.py` (check-vacuity mutations),
`sharper_ce4.py` (the three-cycle holonomy witness).
