# P3 — Finite Negative Constructions (Counterexample Witnesses), Full Pointwise Meta-Agent Package

STATUS: IN_PROGRESS

Reviewer role: adversarial investigator specializing in constructing and destroying finite
counterexamples. Mandate: verify that each exhibited witness actually witnesses the claimed
negative statement, and that the negative statement is the interesting one rather than a
premise-deleted strawman.

Review target: git revision 8ce635807a6ca2a388255fc996c98f7c535e5843 (verified with
`git rev-parse HEAD`).

## Files to examine

- [x] evidence/counterexample-proofs.md (READ IN FULL, 223 lines as committed — the task brief said
      594 lines; the file on disk at this revision is 223 lines. Noted, not a finding.)
- [x] counterexample-register.md (READ IN FULL, 64 lines)
- [x] evidence/finite_nongaussian_witness.py (READ IN FULL, 467 lines)
- [x] evidence/finite-nongaussian-output.json (READ IN FULL)
- [x] EXECUTE witness script, normal and `-O`
- [x] Independent recomputation of N1..N5 and the main lossy witness
- [ ] Strawman check for N1..N5 (in progress)
- [ ] Map 51 checks to mathematical claims
- [ ] DERIVATION-vs-COUNTEREXAMPLE evidence-kind bookkeeping check

---

## PART A — Reproduction results (what actually happened)

### A.1 Script execution — CHECKS OUT

Commands run (Git Bash, `python` = `C:\Python314\python.exe`, Python 3.14.4):

```
cd ".../evidence"
python finite_nongaussian_witness.py     -> EXIT_CODE=0, stdout EMPTY
python -O finite_nongaussian_witness.py  -> EXIT_CODE=0, stdout EMPTY
```

The script prints nothing to stdout in either mode; its only output is the JSON file it rewrites.
The "51 of 51 checks pass" claim is therefore not observable from stdout — it is observable only
from the regenerated `finite-nongaussian-output.json`, whose `summary` block reads
`check_count: 51, failed_check_count: 0, passed_check_count: 51`. I counted the `record(...)` call
sites in the source independently and get 51 (4 kernel + 12 main-law + 8 main-KL + 7 CE1 + 6 CE2 +
4 CE3 + 10 CE4 = 51). Consistent.

Byte-identity: after both the normal and the `-O` run,

```
sha256sum finite-nongaussian-output.json
ca79ea94822e74ad1e7fb3257d0ea852a609a9102be0e49a302687ad1612c062
```

which is exactly the committed file's digest and exactly the digest bound in
`counterexample-register.md` line 59. `git status --porcelain` after both runs showed no
modification to any tracked file. **Both the normal/`-O` byte-identity claim and the digest binding
reproduce.** Note the mechanism is by construction, not by luck: `record()` deliberately stores a
`bool` instead of using `assert`, so `-O` has nothing to strip.

Digest bindings in `counterexample-register.md` §"Task-5 release binding" all verify:

| artifact | claimed | actual |
|---|---|---|
| evidence/counterexample-proofs.md | `59c38ed4…6de6fc` | matches |
| evidence/finite-nongaussian-output.json | `ca79ea94…12c062` | matches |
| evidence/finite_nongaussian_witness.py | `15a9eea5…f78835` | matches |

### A.2 Independent recomputation — ALL ARITHMETIC CHECKS OUT

I wrote my own script from the *mathematical statements* in `counterexample-proofs.md` (not from
the package's script), using `Fraction` for probabilities and 60-digit `Decimal` logs, with an
independently written `kl()` that returns `+Infinity` on a support violation. Scratch file:
`%TEMP%\claude\…\scratchpad\indep_recheck.py`. Every displayed value in the document reproduces:

Main lossy witness (§1):
- `K_0 = (3/4, 1/4)`, `K_1 = (1/4, 3/4)`, both rows normalized.
- `Pi_I` and `Q_I` both normalized; `Pi_I^{MB} = (3/8, 1/8, 1/8, 3/8)` in the stated order — eq. (1.4) confirmed.
- `Q_A = Pi_A = {(0,0):3/8, (0,1):1/8, (1,0):1/8, (1,1):3/8}` and `Q_A(m,b) = (1/2)K_m(b)` — eq. (1.8) confirmed.
- `q_A^m = q_A^b = Bernoulli(1/2)` confirmed.
- `KL(Q_I‖Pi_I) = 0.69314718055994530941723212145817656807550013436025525412068` = `log 2` to 60 digits — eq. (1.10) confirmed.
- `KL(Pi_I‖Q_I) = +∞` confirmed (support violation on every `e≠b` atom).
- `KL(Q_A‖Pi_A) = 0` — eq. (1.11) confirmed.
- Per-fiber conditional KLs: all four fibers give `q(·|z)=δ_b`, `π(·|z)=Bern(1/2)`, conditional KL `= log 2`; `Δ_A = log 2` — eq. (1.12) confirmed.
- Chain rule `KL_fine = KL_coarse + Δ_A` holds exactly (`log2 = 0 + log2`).
- Evaluator compatibility: `P(B=b|M=m) = K_m(b)` for all four `(m,b)` — eq. (1.9) confirmed.

CE-1 (N1): `R`, `S` have identical fair marginals in both coordinates, `R ≠ S`, `KL(R‖S) = KL(S‖R) = +∞`. Confirmed.

CE-2 (N2): fine `KL = 0`; split-channel coarse forward `KL = +∞`; reverse coarse `KL = log 2`. Confirmed. I additionally computed the *common*-channel versions the document does not compute: with the identity channel on both sides the coarse KL is `0`, and with the constant-zero channel on both sides the coarse KL is `0`. Both consistent with data processing.

CE-3 (N3): `K_m(B=1) = (1/4, 3/4)` vs `K'_m(B=1) = (3/4, 1/4)`; mismatch at every `m`; swapped rows still normalized; generative model marginal still `(1/2, 1/2)`. Confirmed.

CE-4 (N4): `KL(Bern(1/4)‖Bern(3/4)) = KL(Bern(3/4)‖Bern(1/4)) = 0.5493061443340548456976226184612628523237452789113747258673` = `(1/2)log 3` to 58 digits. Confirmed. Bit flip stabilizes the fair law. Confirmed.

CE-5 (N5): `T_#R = S` exactly (including zero atoms), both coordinate marginals invariant, joint not invariant. Confirmed.

**No arithmetic error found anywhere in `counterexample-proofs.md` or
`counterexample-register.md`.** Every rational value, every marginal, every KL (finite, infinite,
and symbolic) is correct as stated. That is a real result and I report it as such.

---

## Findings

(strawman analysis, check-mapping, and bookkeeping in progress)
