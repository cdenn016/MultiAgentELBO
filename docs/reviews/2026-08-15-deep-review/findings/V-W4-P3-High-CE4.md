STATUS: COMPLETE

AGENT: skeptic (Claude Opus 5), wave 4
FINDING UNDER ATTACK: W4-P3-High-CE4
TARGET REVISION: 8ce635807a6ca2a388255fc996c98f7c535e5843 (artifacts read at their unchanged
working-tree state on branch `review/2026-08-15-deep-review`)

# Verdict: UPHELD_REDUCED — mechanical core confirmed by execution and strengthened; severity Medium, not High

The finding's headline is exactly, mechanically true. I confirmed it by execution, and I confirmed
more than the investigator did: the check passes under four distinct mutations of `node_laws`, the
whole 51-check suite still exits 0 under every one of them, and the emitted JSON artifact publishes
a factually false pairing (`identity_tree_laws: {left: 2/3,1/3 …}` alongside
`identity_tree_directed_KL: "log(3)/2"`). I also killed the most charitable reading of the check —
that it verifies the rational coefficient of the exhibited laws — by a mutation that leaves the left
law untouched.

The severity is overstated. The underlying mathematics is true (verified exactly, both
orientations), no registered ledger claim depends on the numeric value, the registered claim that
*does* rest on CE-4 has a non-vacuous check and a correct proof, and the package fences the script
as corroboration-only in three separate places — none of which the investigator quoted in this
finding. Under the review's own rubric (`RESUME.md:64`) that is Medium, not High.

---

## 1. What the check actually is

`evidence/finite_nongaussian_witness.py:321-325`, verbatim:

```python
    record(
        checks,
        "CE4_tree_directed_KL_symbolic_half_log_3",
        Fraction(3, 4) - Fraction(1, 4) == Fraction(1, 2),
    )
```

`record` is not clever; it is `checks[name] = bool(condition)` (line 66-69). The condition is a
constant expression over two literals. Every occurrence of `node_laws` in the file:

```
$ grep -n "node_laws" docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/finite_nongaussian_witness.py
310:    node_laws = {
315:    record(checks, "CE4_identity_transport_preserves_node_laws", True)
319:        node_laws["left"] != node_laws["right"],
378:                    "left": [fraction_text(value) for value in node_laws["left"]],
379:                    "right": [fraction_text(value) for value in node_laws["right"]],
```

Line 319 is the inequality check; 378-379 are serialization. The KL check at 321-325 does not
appear. The check named for a divergence never reads the distributions.

## 2. Executed: the witness script itself

Copied to scratch (so the committed JSON is not overwritten in the review branch) and run with the
interpreter the artifact itself names:

```
$ "C:/Python314/python.exe" .../scratchpad/ce4/finite_nongaussian_witness.py
EXIT=0
$ diff scratchpad/ce4/finite-nongaussian-output.json \
       docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/finite-nongaussian-output.json
JSON IDENTICAL (reproducible)
```

The script is deterministic and the committed artifact reproduces byte-for-byte. `check_count = 51`,
51 recorded checks, all ten `CE4_*` entries `True`.

## 3. Executed: the mathematics is TRUE (exact symbolic, sympy 1.14.0)

For \(P=(3/4,1/4)\), \(Q=(1/4,3/4)\), the likelihood ratios are \(3\) and \(1/3\), so

\[
\operatorname{KL}(P\Vert Q)=\tfrac34\log 3+\tfrac14\log\tfrac13=\bigl(\tfrac34-\tfrac14\bigr)\log 3=\tfrac12\log 3,
\]

and the same by symmetry in the reverse orientation. Executed exactly rather than numerically:

```
exhibited (3/4,1/4) | (1/4,3/4)
    KL(P||Q) = log(3)/2   ~ 0.549306144334054845697622618461
    KL(Q||P) = log(3)/2   ~ 0.549306144334054845697622618461
    == (1/2)log3 ?  fwd:True  rev:True  symmetric:True
```

`counterexample-proofs.md:198-202` is correct. It is *asserted* there without the two-line
ratio computation being displayed (unlike CE-1/CE-2/CE-3, whose ratios are shown), but the assertion
is true and the computation is immediate. **There is no mathematical defect anywhere in CE-4.**

## 4. Executed: the mutation test — the check passes on wrong node laws

I mutated the `node_laws` block in the source and re-ran the *entire* script each time, then read the
recorded check value and the emitted JSON back:

```
mutant A (1/2,1/2) | (1/4,3/4)
    script exit code           : 0     checks: 51   failing: []
    CE4_tree_directed_KL_symbolic_half_log_3 = True
    JSON identity_tree_laws    : {'left': ['1/2','1/2'], 'right': ['1/4','3/4']}
    JSON identity_tree_directed_KL = 'log(3)/2'  decimal=0.549306144334054845
    TRUE KL(P||Q)              : -log(3)/2 + log(2) ~ 0.14384103622589046372
    named claim actually holds : False

mutant B (9/10,1/10) | (1/10,9/10)
    script exit code           : 0     checks: 51   failing: []
    CE4_tree_directed_KL_symbolic_half_log_3 = True
    JSON identity_tree_directed_KL = 'log(3)/2'  decimal=0.549306144334054845
    TRUE KL(P||Q)              : 8*log(3)/5 ~ 1.7577796618689755062
    named claim actually holds : False

mutant C (2/3,1/3) | (1/3,2/3)
    script exit code           : 0     checks: 51   failing: []
    CE4_tree_directed_KL_symbolic_half_log_3 = True
    JSON identity_tree_directed_KL = 'log(3)/2'  decimal=0.549306144334054845
    TRUE KL(P||Q)              : log(2)/3 ~ 0.23104906018664843647
    named claim actually holds : False

mutant D (3/4,1/4) | (1/2,1/2)          <-- left law UNCHANGED
    script exit code           : 0     checks: 51   failing: []
    CE4_tree_directed_KL_symbolic_half_log_3 = True
    JSON identity_tree_laws    : {'left': ['3/4','1/4'], 'right': ['1/2','1/2']}
    JSON identity_tree_directed_KL = 'log(3)/2'  decimal=0.549306144334054845
    TRUE KL(P||Q)              : log(3**(3/4)/2) ~ 0.13081203594113695913
    named claim actually holds : False
```

Three consequences, the last two beyond what the finding claimed:

1. **The investigator's falsifier is met by execution.** They asked: name any other check among the
   51 whose failure would follow from a wrong CE-4 directed KL. Under all four mutants, `failing:
   []` — zero of 51. No check in the artifact constrains the value.
2. **The emitted evidence artifact publishes a false statement.** `identity_tree_directed_KL` and
   its 80-digit decimal are hard-typed at lines 372-374 (`Decimal(3).ln() / Decimal(2)`) while
   `identity_tree_laws` at 378-379 is derived from `node_laws`. The JSON therefore reports
   `left: ['2/3','1/3'], right: ['1/3','2/3']` with `directed_KL: 'log(3)/2'` — a pairing whose true
   value is \(\tfrac13\log 2 \approx 0.2310\). This is worse than "printed, never compared": the
   artifact actively asserts the wrong number about the data it also serializes.
3. **The most charitable defense of the check is dead.** One could argue the check verifies the
   rational coefficient of \(\log 3\), i.e. that the left law's mass difference is \(1/2\). Mutant D
   refutes this: the left law is left at \((3/4,1/4)\), so \(3/4-1/4=1/2\) really *is* its mass
   difference, yet the true KL is \(\tfrac34\log 3-\log 2\approx 0.1308\) because the ratio is
   \(3/2\), not \(3\). The check never constrains the ratio, so even the coefficient reading fails.

I also confirmed the investigator's proposed replacement genuinely discriminates:

```
exhibited (3/4,1/4) | (1/4,3/4): fix -> True  ; claim true -> True
mutant A / B / C / D          : fix -> False ; claim true -> False
```

and it is sound as mathematics: `left[0]/right[0]==3` and `left[1]/right[1]==1/3` force
\(\operatorname{KL}=(\text{left}[0]-\text{left}[1])\log 3\), which the third conjunct pins to
\(\tfrac12\log 3\).

Executed artifacts: `…/scratchpad/ce4/attack_ce4.py`, `…/scratchpad/ce4/mut_{A,B,C,D}/`.

## 5. Why the severity is Medium, not High

`RESUME.md:64` defines **High** as *"a claim is materially stronger than its proof, or a proof has a
repairable gap"* and **Medium** as *"imprecision, missing hypothesis, notation collision, or a
citation/novelty problem."* Four facts, none of which the finding reports, place this at Medium.

**(a) The mathematical claim is true and its proof is not gapped.** Section 3 settles this exactly.
No theorem is false; nothing downstream inherits an error. The finding concedes this in its body but
files at a severity reserved for claim-versus-proof mismatches, and here there is none.

**(b) No registered claim depends on the numeric value.** The ledger claim CE-4 closes is

> `NEG-TRIVIAL-HOLONOMY-AGREEMENT`: "There exist trivial-holonomy data with unequal transported laws,
> refuting trivial holonomy as sufficient for belief or model agreement."

The \((1/2)\log 3\) value is a sharpening — `counterexample-proofs.md` introduces it with "More
sharply" — not part of the statement. I dumped all five `NEG-*` statements; none mentions a numeric
KL value. So no ledger closure is invalidated by this defect.

**(c) The claim that *is* registered has a non-vacuous check.** The finding dismisses
`CE4_trivial_holonomy_unequal_laws` as "checks only that the two tuples differ." That is precisely
`NEG-TRIVIAL-HOLONOMY-AGREEMENT`'s content, and it is data-dependent: setting the two laws equal
would fail it. The registered claim's executable support is thin but real, and its proof is correct.

**(d) The package explicitly fences the script as corroboration, in three places the finding does not
quote.**

- `counterexample-register.md:4` — "`evidence/finite-nongaussian-output.json` is deterministic
  arithmetic corroboration only."
- `counterexample-proofs.md:4` — "The displayed arguments are the direct mathematical evidence;
  `finite_nongaussian_witness.py` only corroborates their finite arithmetic."
- `finite_nongaussian_witness.py:1-6` (module docstring) — "The direct proofs are in
  counterexample-proofs.md. … Symbolic logarithmic labels are primary."

In the package's own evidence architecture the proofs are primary and the script is secondary. The
empty check therefore degrades corroboration, not proof.

**(e) The ledger over-scoping leg is narrower than filed.** The finding leans on
`EV-TASK4-FINITE-WITNESS-OUTPUT`'s scope sentence — *"51 exact finite checks, including … forward and
reverse KL orientations …"* — as if it were wholesale false. It is not. I read the other KL checks:
`main_reverse_fine_KL_infinite` (line 194) tests a real support condition,
`main_fine_KL_symbolic_log_2` (line 188) tests normalization and all ratios \(=2\),
`CE1_KL_correlated_to_anticorrelated_infinite` / `CE1_KL_anticorrelated_to_correlated_infinite`
(lines 250, 255) test genuine support disjointness, `CE2_coarse_forward_KL_infinite` (line 272) and
`CE2_coarse_reverse_KL_symbolic_log_2` (line 277) are data-dependent. The scope sentence is
supported for the main witness, CE-1 and CE-2; only the CE-4 item is unsupported. That is a narrow
evidence-scope inaccuracy, i.e. Medium under the rubric.

## 6. What survives, stated precisely

`CE4_tree_directed_KL_symbolic_half_log_3` is a constant expression and is not a check. It cannot
fail for any node laws, and I demonstrated four node-law pairs on which it passes while the named
claim is false. The emitted JSON compounds this by hard-typing `identity_tree_directed_KL` and its
decimal alongside data-derived `identity_tree_laws`, so the artifact will publish a false pairing
under any change to the laws. Neither this check nor any other of the 51 constrains CE-4's numeric
value. The correct disposition is the investigator's fix — replace the constant with the two ratio
conditions, which I verified discriminates on all five cases — or, equivalently, drop the numeric
value from the check register and the JSON, since it is decorative relative to the registered claim.

**Corrected location.** `counterexample-proofs.md:198-202` should be struck from the location line.
The mathematics there is correct. The defect lives entirely in
`finite_nongaussian_witness.py:321-325` and `:372-374`, in the derived
`evidence/finite-nongaussian-output.json`, and in one clause of the
`EV-TASK4-FINITE-WITNESS-OUTPUT` scope sentence.

**Corrected severity.** Medium — an evidence-artifact integrity and scope defect. Not High: nothing
mathematical is wrong, no proof has a gap, and no ledger claim loses its closure.

## 7. Relation to P0

`P0-principal-reviewer-notes.md` contains no reconstruction touching CE-4, holonomy witnesses, or the
finite non-Gaussian script (grep for `CE4`, `CE-4`, `half_log_3`, `log(3)/2`, `corroboration`,
`symbolic` returns nothing). There is no conflict with the principal reviewer's independent work.

## 8. Falsifier of my own attack

My reduction to Medium rests on the claim that **no registered claim, and not the certification,
depends on the value \(\tfrac12\log 3\)**. Exhibit any package claim, ledger record, certification
condition, or manuscript theorem whose truth or closure requires the CE-4 directed KL to equal
\(\tfrac12\log 3\) — rather than merely requiring the two node laws to be unequal — and the finding
returns to High, because then an unsupported numeric value would be load-bearing. Secondarily, if the
adjudicator rules that a `SYMBOLIC_CHECK` evidence record's `scope` sentence counts as "a claim"
under `RESUME.md:64`, then "materially stronger than its proof" applies on its face and High stands.

My confirmation of the mechanical core would be falsified only by showing my mutants violate a stated
premise of CE-4. They do not: each keeps two Bernoulli laws on a two-node identity-transport tree with
`left != right`, which is the entire construction, and mutant D keeps the exhibited left law verbatim.
