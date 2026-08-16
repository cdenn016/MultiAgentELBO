# P2 — Information Theory / VFE Investigator Findings

STATUS: COMPLETE

Reviewer scope: information theory and variational free energy — KL divergence on extended reals,
chain rules, conditional KL, data processing, the ELBO/VFE decomposition, and the exact arithmetic
hazards of `[0,+infty]` versus finite tiers.

Review target: git revision `8ce635807a6ca2a388255fc996c98f7c535e5843`.

**Headline.** The mathematics of the informational core is, as far as I could reconstruct it,
**correct**. I found no false theorem and no `infinity - infinity`. The KL chain (6.4), the extended
VFE identity (6.6), the zero-defect criterion (6.8), and the recovery corollaries (6.10)–(6.12) all
survive independent rederivation. The defects are of scope and bookkeeping, and they cut in *both*
directions: the frozen certification is **narrower** than the claim the manuscript now asserts as
ESTABLISHED (High), while two of the stated theorems are **weaker than the truth** because they
carry a finiteness hypothesis that a bounded f-divergence removes (Medium). One "OPEN" item is a
two-line corollary of the document's own equations.

Counts: Critical 0, High 1, Medium 5, Low 4.

---

## Files read

**In full:**
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md` (498 lines)
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/reviews/view-information-vfe.md` (161 lines)
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/release.json`
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/construction-or-strongest-theorem.md` §4 (lines 55–95)

**Targeted (relevant sections read verbatim):**
- `claim-ledger.json` — `VFE-CHAIN-EXTENDED`, `VFE-FINITE-ZERO-DEFECT-RECOVERY`, `target`, evidence records
- `problem-contract.json` — full `/target` object extracted programmatically
- `evidence/counterexample-proofs.md` — the finite witness (lines 95–175) and CE-1, CE-2
- `evidence/adversarial-attacks.md` — A12–A16
- `evidence/independent-reconstruction.md` — the KL/VFE section
- `Theory/06_general_coarsegraining.tex` — lines 60–320 (KL contraction, equality, recovery, ELBO)
- `Theory/07b_agent_network_rg.tex` — lines 140–185
- `Theory/appendix_claim_ledger.tex` — lines 190–230
- `overview.md` — lines 470–590, 760–810; `solid_RG_theory.md` — §8, §11, Phase 2
- `docs/STATUS.md:315-330`; `docs/change-logs/2026-08-15.md`
- git history and SHA-256 of every package artifact named in the review binding

**Not reached:** `Theory/05_elbo.tex` in full (only its cross-references from 06/07b);
`evidence/notation-*` artifacts; `evidence/finite_nongaussian_witness.py` (I verified the witness
*arithmetic* by hand from `counterexample-proofs.md` instead of running the script);
`oracle-erasure.md`; `adversarial-report.json`; `approach-registry.json` beyond one grep.

---

## SECTIONS THAT CHECK OUT — reported honestly, zero findings

Every one of these I reconstructed independently. They are **correct**.

**(6.2) — RN derivative of the joint lift.** For bounded measurable `g(Y,z)`,
`int g dQhat = int int g(Y,z) C_A(Y,dz) r(Y) Pi_I(dY)`, so `dQhat/dPihat (Y,z) = r(Y)`,
`Pihat`-a.s. Correct.

**(6.3) — the channel lift preserves KL.** `KL(Qhat||Pihat) = int r log r dPihat = KL(Q_I||Pi_I)`
because `C_A(Y, Z_A) = 1`. Equality in `[0,+infty]`. Correct.

**(6.4) — the chain-rule identity. Correct in the extended reals, with no hidden subtraction.**
I rederived it from the generator the document names, `phi_0(t) = t log t - t + 1 >= 0`
(`phi_0'(t) = log t`, minimum at `t = 1`, `phi_0(1) = 0`), which represents KL as an integral of a
genuinely nonnegative integrand: `KL(Q||Pi) = int phi_0(dQ/dPi) dPi`. With `lambda = dQ_A/dPi_A`
and `rho_z = dQhat(.|z)/dPihat(.|z)`, the RN derivative factors as `lambda(z) rho_z(Y)`, and the
exact algebraic identity

    phi_0(lambda*rho) = lambda*phi_0(rho) + rho*phi_0(lambda) + (lambda-1)(rho-1)

holds identically (I verified it term by term: the difference of the two sides is
`lambda*rho - lambda - rho + 1`). Integrating against `Pihat` and disintegrating over `z`, the cross
term vanishes because `int (rho_z - 1) dPihat(.|z) = 0`, leaving

    KL(Qhat||Pihat) = KL(Q_A||Pi_A) + int lambda(z) KL_z dPi_A = KL(Q_A||Pi_A) + int KL_z dQ_A.

That is (6.4). Every piece is a nonnegative integrand, so the identity is an equality in
`[0,+infty]`. The document's assertion that (6.4) "is not formed by subtracting an infinite coarse
divergence from an infinite fine divergence" is **correct**. I also confirmed the identity
numerically over 3000 random finite instances (5-point fine space, 3-point coarse space, random
channel): max `|KL_I - (KL_A + Delta_A)|` = `8.9e-16`.

**The `Q_A` weighting is the correct one.** `Delta_A` is the standard conditional relative entropy
`D(Qhat_{Y|Z} || Pihat_{Y|Z} | Q_A)` in the sense of Polyanskiy–Wu Def. 2.12 (average over the
*numerator* marginal). Weighting by `Pi_A` instead would break the identity. Correct.

**Integration of the `Pi`-reverse kernel against `Q_A` is legitimate.** `Pihat(.|z)` is determined
only `Pi_A`-a.s., but `Delta_A` integrates it against `Q_A`. This is well-posed exactly because
(3.6) establishes `Q_A << Pi_A`, and the document proves (3.6) correctly: `Pi_A(D) = 0` forces
`C_A(Y,D) = 0` `Pi_I`-a.s., which transfers to `Q_I`-a.s. by (1.2), hence `Q_A(D) = 0`. Correct.

**(3.3) — the evidence term survives the channel.** `P_A^O = nu_X` because `C_A` acts only on `Y`.
This is the single most load-bearing structural check in Section 6: it is what makes "add the same
finite real `-log p_X(o)` to both tiers" legitimate rather than a sleight of hand. It is correct,
and the corresponding statement in `Theory/06` (`thm:cg-evidence-preserving-channel`) is proved
properly by a pi-lambda extension.

**(6.6) — the extended VFE identity.** `-log p_X(o)` is a finite real by the admissibility
declaration `0 < p_X(o) < infty`. Addition in `(-infty, +infty]` is associative and no
`-infty + infty` can arise because `F_A > -infty` always. `F_I, F_A` land in `(-infty, +infty]`.
The claim that a finite VFE may be negative is correct. Correct.

**The specific hazard in my mandate — a later step reusing nonnegativity of a VFE term after a
finite real was added — DOES NOT OCCUR.** I checked every downstream step in `direct-derivation.md`
§6, in `construction-or-strongest-theorem.md` §4, in `Theory/06` `sec:cg-elbo`, and in `Theory/07b`.
(6.7) is fenced on finite fine KL; (6.8) uses nonnegativity of the **integrand of `Delta_A`**, which
really is in `[0,+infty]` and is not a VFE; (6.12) uses DPI on KL, not a sign of `F`. `Theory/06`
eq. `cg-elbo-monotone` states the coarse/fine comparison as an *inequality* valid in the extended
reals and explicitly handles `Q_o not<< P_o` by assigning `-infty`, never forming an undefined sum.
A repo-wide grep for `F >= 0`-shaped assertions returns exactly one hit, `direct-derivation.md:331`,
which is `F_I - F_A = Delta_A >= 0` inside the finite fence and is correct. **No finding.**

**(6.8), both directions.** (<=) is immediate. (=>): `int f dQ_A = 0` with `f >= 0` measurable gives
`f = 0` `Q_A`-a.s., then `KL(mu||nu) = 0 <=> mu = nu` for probability measures (strict convexity of
`t log t`; or Pinsker). The integrand is genuinely a KL of two probability kernels, and the null set
is with respect to `Q_A`, which is the measure the integral in (6.4) actually uses. The degenerate
`+infty = +infty` case cannot corrupt it because `Delta_A` is **defined** by the integral in (6.4),
never recovered by subtraction. **The criterion is correct and correct without any finiteness
premise** — the repair flagged in the change log is, at the level of `direct-derivation.md`,
mathematically complete. (Its *propagation* is not — see [MEDIUM-2] and [MEDIUM-3].)

**(6.10) and (6.11) — the forward recovery direction.** `Pi_A R_Pi = Pi_I` is the `Y`-marginal of
the disintegrated `Pihat`. Under (6.8), `Q_A R_Pi = int Q_A(dz) Pihat(dY|z) = int Q_A(dz) Qhat(dY|z)
= Q_I`. Correct, and correctly stated with no finiteness premise.

**(6.12) reverse direction, as proved.** DPI through `C_A` gives `KL_A <= KL_I`; DPI through `R`
gives `KL_I = KL(Q_A R||Pi_A R) <= KL_A`. Hence `KL_I = KL_A`, and with `KL_I < infty`, (6.4) forces
`Delta_A = 0`. **The argument as written is valid.** (The hypothesis is removable — [MEDIUM-1].)

**Every use of the subtraction form `F_I - F_A = Delta_A` in the repository is fenced by the
finiteness premise.** This was mandate question 4 and it is a clean pass. I enumerated every
occurrence at revision 8ce6358:
`evidence/direct-derivation.md:328-331`, `construction-or-strongest-theorem.md:82`,
`evidence/independent-reconstruction.md:48`, `claim-ledger.json:381`, `overview.md:549`,
`solid_RG_theory.md:381`, `docs/STATUS.md:322`, `Theory/07b_agent_network_rg.tex:175`,
`Theory/appendix_claim_ledger.tex:207`,
`docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md:3760`.
All ten are inside an explicit finite-fine-KL fence. `solid_RG_theory.md` §8 states the closure in
the **additive** form `F_o = F_o^c + Delta_C` and never subtracts. **I found no unfenced use.**

**The finite categorical witness arithmetic is correct.** With `Pi(m,b,e) = K_m(b)/4` and
`Q(m,b,e) = K_m(b)*1[e=b]/2` over `m` in a 2-point set and `b,e` binary: both normalize to 1; the
likelihood ratio on every `Q`-atom is exactly 2, so fine `KL = log 2`; the `(M,B)` pushforwards are
both `K_m(b)/2` so coarse `KL = 0`; each conditional is `KL(delta_b || Bern(1/2)) = log 2`, so
`Delta_A = log 2`; and `log 2 = 0 + log 2`. The reverse fine KL is `+infty` because `Pi` charges
`e != b`. All as claimed. **No finding.**

**`Theory/06` `cor:cg-dpi-infinite-equality-warning` is a valid counterexample.** With
`X = {a,b,c}`, `Y = {u,v}`, `K: a->u, b,c->v`, `P = (delta_a + delta_b)/2`,
`Q = (delta_b + delta_c)/2`: both KLs are `+infty`; `QK = delta_v` forces `R(v,.) = Q`; then
`(PK)R` charges `c` with mass `>= 1/4` while `P(c) = 0`. Correct. Note for the record that this
datum has `P not<< Q`, so it lies **outside** the package's standing hypothesis (1.2) — which is
precisely why it does not save the finiteness premise in (6.12); see [MEDIUM-1].

---

## Findings

### [HIGH] The unconditional zero-defect criterion is asserted as ESTABLISHED across five manuscript surfaces on the authority of a release whose frozen contract explicitly excludes the infinite tier

**Location:** `docs/derivations/2026-08-15-full-pointwise-meta-agent/problem-contract.json`
`/target/regularity`, `/target/measures[2]`, `/target/permitted_theorems[2]`, versus
`Theory/07b_agent_network_rg.tex:172-177`, `Theory/appendix_claim_ledger.tex:201-217`,
`overview.md:547-548`, `solid_RG_theory.md:381`, `docs/STATUS.md:319-320`.

**Claim as stated.** The frozen contract (digest
`15336a68593c1523eeeffe97101fbbaaf484e32145cdd1b762d7372bda94ad87`, the digest the release certifies
`COMPLETE_AFFIRMATIVE` with `"unresolved_obligations": []`) says:

> `/target/regularity`: "The primary tier uses standard-Borel measurability, normalized laws and kernels, selected regular conditionals at admitted observations, absolute continuity, **and finite terms wherever KL or VFE expressions are displayed**."
> `/target/measures[2]`: "The evidence and **every displayed KL or conditional-KL term are finite** where the affirmative VFE identity is asserted."
> `/target/permitted_theorems[2]`: "KL data processing and the common-channel conditional-KL chain rule **under the recorded finiteness hypotheses**."

The manuscript, citing that release as its authority, says:

> "**Without a finite-fine-KL premise**, \(\Delta_A=0\) exactly when the two discarded conditional laws in \eqref{eq:rg-pointwise-parent-defect} agree \(\mathbb Q_{A,o,X}\)-almost surely." — `Theory/07b:172-174`, carrying `\status{ESTABLISHED}` at `:177`.

and, in the same breath, `Theory/appendix_claim_ledger.tex:214-217`:

> "The manuscript status is \textsc{established}; the bound release records ledger state \texttt{EVIDENCE\_VERIFIED} and terminal package status \texttt{COMPLETE\_AFFIRMATIVE}."

**Defect:** The certified target is a **finite-tier** theorem — its own `measures` clause requires
every displayed KL and conditional-KL term to be finite, and its `permitted_theorems` clause admits
the chain rule only "under the recorded finiteness hypotheses". The manuscript asserts a strictly
larger claim (the criterion holds with *no* finiteness premise, i.e. precisely on the tier the
contract excludes) and stamps it ESTABLISHED while pointing at the release for authority. The
release cannot support it: nothing in `[0,+infty]` is inside the frozen domain. Separately, the
derivation's own §6 uses the chain rule in `[0,+infty]` and states (6.4) as an equality in
`[0,+infty]`, which is a use of a theorem outside `/target/permitted_theorems`.

Note carefully what this finding is **not**: the unconditional criterion is **true** (I verified it
above, and `direct-derivation.md` (6.8) proves it correctly). The defect is that the certification
chain the manuscript invokes does not cover the claim it is invoked for, and the release
simultaneously declares zero unresolved obligations.

**Evidence:**
1. `problem-contract.json` `/target` extracted programmatically at revision 8ce6358; the three
   clauses are quoted verbatim above.
2. `git log --oneline -- docs/derivations/2026-08-15-full-pointwise-meta-agent/` shows the package
   was last touched at `a623b6e`. The Task-7 scope correction `fe08359` ("docs: correct pointwise
   VFE scope") touched **no** package file — it edited only `overview.md`, `solid_RG_theory.md`,
   `Theory/*.tex`, `docs/STATUS.md` and the worklog. So the correction that introduced the
   unconditional wording never entered the certified artifact set, and the contract was never
   reopened to admit the extended tier.
3. `release.json` at HEAD still reads `"terminal_status": "COMPLETE_AFFIRMATIVE"`,
   `"unresolved_obligations": []`, `"certificate_claim": "target"`.

**Falsifier:** Point to a clause in `problem-contract.json` (or an amendment bound to the same
target digest) that admits `[0,+infty]`-valued KL terms into the affirmative conjunct. I searched
the whole `/target` object; `/target/measures[2]` and `/target/regularity` say the opposite. A
second falsifier: show that `\status{ESTABLISHED}` in `Theory/` is defined to mean "proved in the
manuscript" independent of the release, in which case the appendix's explicit appeal to
`EVIDENCE_VERIFIED`/`COMPLETE_AFFIRMATIVE` is decorative rather than load-bearing.

**Fix (smallest repair):** Either (a) amend `problem-contract.json` `/target/measures` and
`/target/regularity` to admit `[0,+infty]`-valued KL and conditional-KL terms for the chain identity
and the zero-defect criterion, re-freeze the digest, and re-run the release — the mathematics
already supports it, so this is bookkeeping; or (b) in `Theory/07b:172-177` and
`Theory/appendix_claim_ledger.tex:201-217`, split the status: `\status{ESTABLISHED}` for the
finite-tier statement that the release covers, and a separate sentence marking the unconditional
extension as manuscript-proved but outside the frozen certificate. Do not leave the release's
`unresolved_obligations: []` standing alongside a manuscript claim it does not reach.

---

### [MEDIUM-1] The finiteness premise on the pairwise-recovery equivalence (6.12) is unnecessary, and the manuscript's necessity claim ("required") is false

**Location:** `evidence/direct-derivation.md` §6, eqs. (6.9)–(6.12);
`overview.md:548-550`; `solid_RG_theory.md:381`; `Theory/07b:174-176`;
`Theory/appendix_claim_ledger.tex:206-209`; `docs/STATUS.md:321-322`.

**Claim as stated:**
> "Conversely, **assume the fine KL is finite** and there exists one normalized kernel \(R:\mathsf Z_A\rightsquigarrow\mathsf Y_I\) satisfying both recovery identities. ... Thus, **on the finite tier**, \(\Delta_A=0 \Longleftrightarrow\) one common normalized recovery kernel recovers both declared laws." (`direct-derivation.md` §6)

> "Finite fine KL is **required** for ordinary subtraction \(\mathcal F_I-\mathcal F_A=\Delta_A\) and for the stated two-way pairwise common-recovery equivalence" (`overview.md:548-550`; identical at `solid_RG_theory.md:381`, `Theory/07b:174-176`, `STATUS.md:321-322`).

**Defect:** Finiteness is genuinely required for the *subtraction* clause. It is **not** required
for the recovery equivalence. The equivalence

    Delta_A = 0  <=>  a common normalized recovery kernel exists

holds verbatim on all of `[0,+infty]` under the package's standing hypotheses. The document's proof
needs finiteness only because it routes through KL, whose cancellation is illegitimate at `+infty`.
Routing through a **bounded** f-divergence removes the hypothesis outright. The word "required"
therefore asserts a necessity that is mathematically false, on five surfaces.

**Evidence — my reconstruction.** Let `rho(P,Q) = int sqrt((dP/dmu)(dQ/dmu)) dmu` be the
Bhattacharyya affinity (`= 1 - H^2(P,Q)/2`). It lies in `[0,1]` for every pair, is always finite,
is independent of the dominating `mu`, and `rho(P,Q) = 1 <=> P = Q`.

*Step 1 — the affinity of the joint lift equals the affinity of the fine pair.* With `mu`
dominating `Q_I, Pi_I` and `muhat(dY,dz) = mu(dY) C_A(Y,dz)`, we have
`dQhat/dmuhat(Y,z) = (dQ_I/dmu)(Y)`, hence `rho(Qhat,Pihat) = int sqrt(q_I p_I) dmu = rho(Q_I,Pi_I)`.
(Same mechanism as the document's own (6.2)–(6.3), with `sqrt` in place of `t log t`.)

*Step 2 — disintegration of the affinity over `z`.* With `sigma` dominating `Q_A, Pi_A`, densities
`q_A, p_A`, and `rho_z := rho(Qhat(.|z), Pihat(.|z)) in [0,1]`,

    rho(Qhat, Pihat) = int sqrt(q_A(z) p_A(z)) * rho_z * sigma(dz).

*Step 3 — DPI for the affinity.* Since `rho_z <= 1`,
`rho(Q_I,Pi_I) = rho(Qhat,Pihat) <= int sqrt(q_A p_A) dsigma = rho(Q_A,Pi_A)`.
Applying the same inequality to the kernel `R` gives `rho(Q_A,Pi_A) <= rho(Q_A R, Pi_A R)`.

*Step 4 — a common recovery kernel forces equality.* If `Q_A R = Q_I` and `Pi_A R = Pi_I`, then
`rho(Q_A,Pi_A) <= rho(Q_I,Pi_I) <= rho(Q_A,Pi_A)`, so `rho(Q_A,Pi_A) = rho(Q_I,Pi_I)`.

*Step 5 — the equality condition.* Equality in Step 3 means `int sqrt(q_A p_A)(1 - rho_z) dsigma = 0`,
so `rho_z = 1` for `sigma`-a.e. `z` in `{q_A > 0} ∩ {p_A > 0}`. Because `Q_A << Pi_A` — the
document's own (3.6) — we have `Q_A({p_A = 0}) = 0` and `Q_A({q_A = 0}) = 0`, so the exceptional set
is `Q_A`-null. Hence `Qhat(.|z) = Pihat(.|z)` `Q_A`-a.s., which is exactly the right-hand side of
the document's own (6.8), and therefore `Delta_A = 0`.

No step used `KL(Q_I||Pi_I) < infty`. Every quantity in the argument is bounded by 1. The forward
direction ((6.8) => common recovery via `R_Pi`) is already proved in the document with no finiteness
premise. So **both** directions hold on `[0,+infty]`.

Mechanical corroboration of Steps 2 and 3: over 3000 random finite instances (5-point fine space,
3-point coarse space, random Markov channel, random `Q`, `Pi`), max residual on the Step-2
disintegration identity was `2.2e-16` and the minimum Step-3 DPI slack `rho(Q_A,Pi_A) - rho(Q_I,Pi_I)`
was `+4.4e-4` (never negative). Script: scratchpad `check_affinity.py`.

This is the classical equality-in-DPI / sufficiency characterization, of which the document uses
only the KL instance — precisely the instance where finiteness is unavoidable. Primary sources:
I. Csiszár, "Eine informationstheoretische Ungleichung und ihre Anwendung auf den Beweis der
Ergodizität von Markoffschen Ketten", *Publ. Math. Inst. Hungar. Acad. Sci.* 8 (1963) 85–108;
F. Liese & I. Vajda, "On divergences and informations in statistics and information theory",
*IEEE Trans. Inform. Theory* 52(10) (2006) 4394–4412 (sufficiency <=> equality in the f-divergence
DPI for strictly convex f). Modern textbook statement: Polyanskiy & Wu, *Information Theory: From
Coding to Learning*, CUP 2024, §7.

**Why the package's own infinite-tier warning does not rescue the hypothesis.** `Theory/06`
`cor:cg-dpi-infinite-equality-warning` exhibits `P not<< Q` with `KL(PK||QK) = KL(P||Q) = +infty`
and no common recovery kernel. That corollary is correct, but it refutes a *different* implication
(infinite KL equality => recovery), and its datum violates the package's standing hypothesis (1.2),
`Q_{I,o,X} << Pi_{I,o,X}`. In that same example the affinity test still bites: `rho(P,Q) = 1/2`
while `rho(PK,QK) = 1/sqrt(2)`, strict DPI, so no common recovery — exactly as my Step 5 predicts.
The affinity route is informative precisely where KL is not.

**The infinite tier is not a vacuous regime, so the restriction discards real content.** Concrete
witness: `Y_I = N x {0,1}`, `Pi_I(n,e) = pi_n/2`, `Q_I(n,e) = q_n t_n(e)` with `q_n << pi_n` chosen so
`sum q_n log(q_n/pi_n) = +infty`, and `C_A` forgetting `e`. Then `KL_I = +infty`, `KL_A = +infty`,
(6.4) is uninformative, but `Delta_A = sum_n q_n KL(t_n || Unif) > 0` whenever some `t_n != Unif`,
and `rho(Q_I,Pi_I) = sum_n sqrt(q_n pi_n) * sum_e sqrt(t_n(e)/2) < sum_n sqrt(q_n pi_n)
= rho(Q_A,Pi_A)` strictly — so the criterion correctly reports "no common recovery" on a tier the
document declares out of scope.

**Falsifier:** Exhibit `Q_I, Pi_I, C_A` with `Q_I << Pi_I`, a normalized kernel `R` with
`Q_A R = Q_I` and `Pi_A R = Pi_I`, and `Delta_A > 0`. Steps 1–5 show no such object exists.
Alternatively, break Step 2 (the affinity disintegration) or Step 5 (the null-set transfer) on a
standard-Borel space.

**Fix:** In `direct-derivation.md` §6, replace "assume the fine KL is finite and there exists one
normalized kernel R" with "assume there exists one normalized kernel R", and replace the KL/DPI
sentence with the four-line affinity argument. Then (6.12) is stated unconditionally, matching
(6.8), and the two halves of the section finally agree. On the five manuscript surfaces, change
"Finite fine KL is required for ordinary subtraction \(\mathcal F_I-\mathcal F_A=\Delta_A\) and for
the stated two-way pairwise common-recovery equivalence" to "Finite fine KL is required for the
ordinary subtraction \(\mathcal F_I-\mathcal F_A=\Delta_A\); the zero-defect criterion and the
two-way pairwise common-recovery equivalence need no finiteness premise." If the authors decline to
import the affinity route, the minimal honest restatement is "the proof given here uses finite fine
KL" — never "finite fine KL is required".

---

### [MEDIUM-2] Inside the certified package, the strongest-theorem statement, the ledger claim, and the independent reconstruction all bind the zero-defect criterion to the finite tier — contradicting `direct-derivation.md` (6.8) in the same package — while the bound information/VFE review attests that they are "correctly separated"

**Location:** `construction-or-strongest-theorem.md:82-92`; `claim-ledger.json` claim
`VFE-FINITE-ZERO-DEFECT-RECOVERY`; `evidence/independent-reconstruction.md:48`;
`evidence/reviews/view-information-vfe.md:123`.

**Claims as stated:**

`construction-or-strongest-theorem.md:82-90` — the package's headline theorem statement:
> "**If the fine KL is finite**, the ordinary real difference is (\mathcal F_I-\mathcal F_A=\Delta_A), **and**
> \[ \Delta_A=0 \Longleftrightarrow \widehat{\mathbb Q}_{I,o,X}(dY\mid z) = \widehat{\boldsymbol\Pi}_{I,o,X}(dY\mid z) \quad \mathbb Q_{A,o,X}\text{-almost surely}. \]"

`claim-ledger.json`, `VFE-FINITE-ZERO-DEFECT-RECOVERY`, `"state": "EVIDENCE_VERIFIED"`:
> `"statement": "When fine KL is finite, the ordinary VFE difference equals Delta_A; Delta_A=0 exactly when discarded conditional recognition and posterior laws agree Q_A-a.s., equivalently when one normalized pairwise recovery kernel recovers both fine laws."`
> `"quantifiers": "For every in-scope common-channel pair with finite KL(Q_{I,o,X}||Pi_{I,o,X})."`

`evidence/independent-reconstruction.md:48`:
> "This reconstructs `VFE-FINITE-ZERO-DEFECT-RECOVERY` **only pairwise and only on the finite tier**."

`evidence/reviews/view-information-vfe.md:123`:
> "| `VFE-FINITE-ZERO-DEFECT-RECOVERY` | Supported | The zero criterion, finite ordinary VFE difference, and pairwise two-law recovery equivalence are **correctly separated** from experiment-wide recovery; `direct-derivation.md:327-381`. |"

**Defect:** In `construction-or-strongest-theorem.md:82` the "and" is inside the scope of "If the
fine KL is finite", so the zero-defect criterion is presented as a consequence of finiteness. The
ledger's `quantifiers` field puts the whole conjunction — criterion included — under "finite KL".
Both contradict `direct-derivation.md` (6.8), which states the criterion with no finiteness premise
and adds the finiteness sentence *afterwards* ("When the fine KL is finite, (6.8) is **also**
equivalent to ordinary real-valued VFE equality"). Three artifacts of one package disagree about
the scope of one theorem, and the two carrying the `EVIDENCE_VERIFIED` / headline-statement roles
carry the over-restricted version. The bound domain review's specific attestation that they are
"correctly separated" is false against the bytes it bound.

**Evidence:**
- `sha256sum evidence/direct-derivation.md` at HEAD = `2aa70b07751d07712a3d9395f77817317d48d77d97c3fd5fb8cd1a3f6fda226a`,
  which **matches exactly** the hash bound in `view-information-vfe.md:20`. So the reviewer read the
  version of §6 that already states (6.8) unconditionally.
- `git show a623b6e -- construction-or-strongest-theorem.md` shows the only post-review change to
  that file was SHA/provenance bookkeeping; lines 82–92 are unchanged from the reviewed bytes. So
  the reviewer also read the over-fenced statement, and signed off on both.
- `git log --oneline -- docs/derivations/2026-08-15-full-pointwise-meta-agent/` confirms the Task-7
  correction `fe08359` never entered the package, so this inconsistency is still live at 8ce6358.

**Falsifier:** Show that `quantifiers` in this ledger schema records the *domain over which evidence
was checked* rather than the theorem's scope. The sibling entry `VFE-CHAIN-EXTENDED` uses
`quantifiers` as the theorem's scope ("For every pair satisfying ASM-RECOGNITION-AC, ..."), which
argues against that reading. A second falsifier: a reading of `construction-or-strongest-theorem.md:82`
on which the displayed equivalence escapes the "If the fine KL is finite" antecedent.

**Fix:** Split the ledger entry into `VFE-ZERO-DEFECT-CRITERION` (quantifier: every in-scope
common-channel pair, no finiteness) and `VFE-FINITE-SUBTRACTION` (quantifier: finite fine KL). Per
[MEDIUM-1] the recovery equivalence belongs with the first. In
`construction-or-strongest-theorem.md`, move the displayed equivalence out of the finiteness
antecedent — one sentence break.

---

### [MEDIUM-3] `solid_RG_theory.md` §8 and §11 still state the zero-defect criterion under a finite-KL premise, contradicting the Phase-2 paragraph of the same file

**Location:** `solid_RG_theory.md:277` (§8) and `:330` (§11 ESTABLISHED list) versus `:381` (Phase 2).

**Claim as stated:**
> `:277` — "**For finite fine KL**, \(\Delta_C=0\) exactly when the discarded conditional recognition and posterior laws agree \(Q_o^c\)-almost surely."
> `:330` — "the extended common-channel KL/VFE chain and its **finite** zero-defect and pairwise recovery corollaries"
> `:381` — "**Without a finiteness premise**, \(\Delta_A=0\) exactly when the discarded conditional recognition and posterior laws agree \(\mathbb Q_{A,o,X}\)-almost surely."

**Defect:** The same document asserts the same criterion with and then without a finiteness premise
about a hundred lines apart, and its certified-boundary list at `:330` labels the zero-defect
corollary "finite". `solid_RG_theory.md` is described in its own §11 table as "Start page and **sole
human-facing pointwise guide**", so this is the first surface a reader hits. The Task-7 repair
reached `:381` but not §8 or the §11 status list. None of the three is *false* — §8's is a true
statement under a superfluous hypothesis — but they cannot all be one theorem's scope.

**Evidence:** Direct quotation of the three lines at revision 8ce6358, above. `git show fe08359
--stat` confirms the correction commit edited this file; it simply did not reach §8 or §11.

**Falsifier:** Show that §8 deliberately reports a different, older theorem (the historical
two-channel marginal-pair result) whose scope genuinely is the finite tier. §8's own text argues
against this: it derives the general standard-Borel disintegration for an arbitrary normalized
recognition-independent Markov channel `C`, i.e. exactly the Section-6 object, and §11 lists the
corollaries of the *current* package.

**Fix:** In §8, delete "For finite fine KL," from the sentence at `:277` and add "Finite fine KL is
what licenses the ordinary real-valued difference \(\mathcal F_o-\mathcal F_o^c\)." In §11 `:330`,
change "its finite zero-defect and pairwise recovery corollaries" to "its zero-defect and pairwise
recovery corollaries and the finite-tier subtraction".

---

### [MEDIUM-4] The family-wide recovery caveat is asserted, never demonstrated, and is a two-line corollary of the document's own (6.10)–(6.11) in the case the theorem actually addresses

**Location:** `evidence/direct-derivation.md` §6, sentence after (6.12);
`Theory/06_general_coarsegraining.tex` §`sec:cg-kl-recovery`, final paragraph, `\status{ESTABLISHED}`;
`Theory/appendix_claim_ledger.tex:219-225` (`\status{OPEN}`);
`solid_RG_theory.md:336` (OPEN/TODO list); `evidence/adversarial-attacks.md` A14.

**Claim as stated:**
> "This is pair-specific recovery. **A single recovery kernel for an entire model family requires simultaneous recovery hypotheses for every family member.**" (`direct-derivation.md` §6)
> "Pairwise equality does not prove that stronger statement. \status{ESTABLISHED}" (`Theory/06`)
> "what remains open is one common recovery kernel for an entire statistical experiment without separately imposing simultaneous family hypotheses" (`appendix_claim_ledger.tex:222-224`, `\status{OPEN}`)
> A14 disposition: "`REJECTED` for `VFE-FINITE-ZERO-DEFECT-RECOVERY`; experiment-level recovery remains open."

**Defect:** This is mandate question 5 and the answer is: **merely asserted**. No counterexample and
no proof is supplied anywhere in the package for the failure of family-wide recovery in the
zero-defect setting, and in the setting the theorem actually treats the statement is a corollary of
the document's own equations, not an open problem.

**Evidence:**

*(a) The shared-posterior case is immediate.* `R_Pi(z,.) = Pihat(.|z)` is built from `Pi_I` and
`C_A` alone — it does not read `Q` at all. So let `{Q^(k)}_{k in K}` be **any** family of recognition
laws with `Q^(k) << Pi_I` and `Delta_A^(k) = 0`. By the document's (6.10), `Pi_A R_Pi = Pi_I`; by
(6.11), `Q_A^(k) R_Pi = Q^(k)` for every `k`. One kernel, whole family. That is exactly
experiment-level common recovery for `{Pi_I} u {Q^(k)}`, and it needs no hypothesis beyond the
pointwise one applied to each member. For a variational problem — one posterior, a family of
recognition laws — this is the case that matters, and the caveat is vacuous there.

*(b) `Theory/06` already says this and then contradicts itself.* Its own paragraph reads: "For a
dominated experiment, one common dominating probability \(P_0\) and simultaneous finite equalities
\(\KL(P_\theta K\Vert P_0K)=\KL(P_\theta\Vert P_0)\) \((\theta\in\Theta)\) make the single Bayes
kernel \(R_{P_0}\) recover every \(P_\theta\)." Those "simultaneous finite equalities" are just
zero-defect for each `theta` against the common `P_0`. So the very sentence that names the
hypothesis shows it is not an extra structural assumption. The next sentence, "Pairwise equality
does not prove that stronger statement", is then either trivial (if "pairwise" means one single
pair) or self-contradictory (if it means every pair against the common `P_0`).

*(c) The remaining reading is closed by a 1949 theorem.* If "pairwise" means sufficiency for every
pair `{P_theta, P_theta'}` with no distinguished reference, then for a **dominated** family pairwise
sufficiency implies sufficiency — Halmos & Savage, "Application of the Radon-Nikodym Theorem to the
Theory of Sufficient Statistics", *Ann. Math. Statist.* 20(2) (1949) 225–241, whose factorization
theorem gives, for dominated families, that sufficiency of `T` is equivalent to every pairwise
likelihood ratio being `T`-measurable. Here the family is dominated by construction: `Q^(k) << Pi_I`
for all `k`. The package cites no source at all on this point (see [LOW-3]); A14's response cites
"The Research wiki's experiment-comparison boundary", which is an internal document, not a source.

*(d) The only family-wide counterexample in the repository is about something else.* `Theory/06`
exhibits `X = (A,B)` independent Bernoulli with `Pr_theta(A=1) = 1/2 + theta/4`,
`Pr_theta(B=1) = 1/2 + theta^2/4` and `K` discarding `B`, concluding "no parameter-independent
reverse kernel can recover the whole experiment". Correct — but its hypothesis is **Fisher equality
at one parameter**, not zero defect for every family member. Indeed for `theta != 0` the pair
`(P_theta, P_0)` has strictly positive defect, so it is not a counterexample to the statement at
issue.

**Falsifier:** Exhibit a family `{Q^(k)}` with `Q^(k) << Pi_I`, `Delta_A^(k) = 0` for every `k`, and
no single normalized kernel recovering `Pi_I` and every `Q^(k)`. My (a) shows `R_Pi` is such a
kernel, so this would refute the finding. Alternatively, exhibit a dominated family that is pairwise
sufficient but not sufficient, refuting the Halmos–Savage reading in (c).

**Fix:** In `direct-derivation.md` §6, replace the caveat with the corollary it actually is:
"Because `R_Pi` does not read the recognition law, one and the same `R_Pi` recovers `Pi_I` together
with every recognition law in a family whose members individually satisfy (6.8). A family whose
*posteriors* also vary requires a kernel recovering each declared posterior, which is a separate
hypothesis." Then remove "family-wide common recovery absent simultaneous hypotheses" from the
OPEN/TODO list at `solid_RG_theory.md:336` and downgrade `\status{OPEN}` at
`appendix_claim_ledger.tex:225` to the residual varying-posterior case, and revise A14's disposition
accordingly.

---

### [MEDIUM-5] The certified derivation invokes the extended-valued chain rule, DPI, and the KL equality condition with no citation to any primary source

**Location:** `evidence/direct-derivation.md:286` and §6 throughout; package-wide.

**Claim as stated:**
> "The relative-entropy chain rule, obtained by factorizing the Radon--Nikodym derivative into its \(z\)-marginal density and conditional density and **invoking the standard extended-valued chain theorem** through the nonnegative generator \(\phi_0(t)=t\log t-t+1\) and its monotone truncations, rather than treating the raw \(t\log t\) integrand as pointwise nonnegative, gives the additive identity ..."

**Defect:** The single load-bearing theorem of the whole informational core is invoked as "the
standard extended-valued chain theorem" with no reference, and "its monotone truncations" stands in
for the proof. A grep of the entire package (`grep -rn "cite\|Csisz\|Kullback\|Dupuis\|Polyanskiy\|
Halmos\|Savage\|Blackwell\|Le Cam"`) returns **zero** citations to any primary information-theory
source; the only hits are the words "cited" and "Blackwell" used descriptively. The same holds for
the DPI step in (6.12) and for `KL(mu||nu) = 0 <=> mu = nu`. `Theory/06` by contrast does cite
Kullback (1951) and Csiszár (1967) for the kernel-form information-loss theorem, so the manuscript
knows the standard is higher than the package meets.

The identity is true — I reconstructed it above, and the `phi_0` route does work — so this is a
sourcing defect, not a mathematical one. But a package that declares its target EVIDENCE_VERIFIED on
the strength of a written derivation cannot leave its central theorem unsourced.

**Evidence:** The grep result above, run at revision 8ce6358 over the whole package directory.

**Falsifier:** A citation elsewhere in the package (I searched the eight `.md` and six `.json`
artifacts) or a rule in the `rigorous-theory-search` schema that exempts evidence artifacts from
citation.

**Fix:** Add one line to `direct-derivation.md` §6: the chain rule for relative entropy in
`[0,+infty]` on standard-Borel spaces is Dupuis & Ellis, *A Weak Convergence Approach to the Theory
of Large Deviations* (Wiley 1997), Theorem C.3.1; the modern textbook statement is Polyanskiy & Wu,
*Information Theory: From Coding to Learning* (CUP 2024), Thm 2.13. For the equality condition in
DPI, cite Csiszár (1963) / Liese & Vajda (2006) as in [MEDIUM-1].

---

### [LOW-1] `solid_RG_theory.md` §8 writes conditionals of a law that has no `z` coordinate

**Location:** `solid_RG_theory.md:263-265`.

**Claim as stated:**
> \(\operatorname{KL}(Q_o\Vert\Pi_o) = \operatorname{KL}(Q_o^c\Vert\Pi_o^c) + \int\operatorname{KL}(Q_o(\cdot\mid z)\Vert\Pi_o(\cdot\mid z))Q_o^c(dz)\)

**Defect:** `Q_o` and `Pi_o` are laws on the fine space only. §8 never introduces the joint lifts
`Qhat(dy,dz) = Q_o(dy)C(y,dz)` and `Pihat(dy,dz) = Pi_o(dy)C(y,dz)`, so `Q_o(.|z)` and `Pi_o(.|z)`
are undefined objects there. `direct-derivation.md` §6 does this correctly, introducing (6.1) first.
The seam matters: the whole content of the defect is that these are the **reverse channels of `C`
under two different input laws**. Without the lift a reader can mistake them for conditionals of a
given joint — which is what makes the defect look like a mutual information (it is not; see [LOW-2]).

**Falsifier:** A definition of `Q_o(.|z)` elsewhere in `solid_RG_theory.md`. I grepped the file;
there is none.

**Fix:** Insert before the display: "Write `Qhat(dy,dz) = Q_o(dy)C(y,dz)` and
`Pihat(dy,dz) = Pi_o(dy)C(y,dz)`, and let `Q_o(.|z)`, `Pi_o(.|z)` denote their `z`-disintegrations."

---

### [LOW-2] "Conditional-information VFE defect" overreads what `Delta_A` is

**Location:** `solid_RG_theory.md:12`; `overview.md:773`; `Theory/appendix_claim_ledger.tex:201`;
`docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md:3756`.

**Claim as stated:**
> "one normalized recognition-independent channel produces ... and the exact **conditional-information VFE defect**" (`solid_RG_theory.md:12`)

**Defect (mandate question 6).** `Delta_A` **is** exactly a conditional relative entropy —
`D(Qhat_{Y|Z} || Pihat_{Y|Z} | Q_A)` in the standard sense, averaged over the numerator marginal
`Q_A`. That identification is correct and I verified it. It is **not** a conditional mutual
information, and it is not a measure of information discarded by `C_A`. The naming invites the
second reading, which is false: `Delta_A = 0` is compatible with `C_A` discarding everything (take
`C_A` constant and `Q_I = Pi_I`; then `Delta_A = 0` while `Y` is entirely erased), and `Delta_A > 0`
is compatible with `C_A` being nearly lossless. `Delta_A` measures the *disagreement of two reverse
channels*, i.e. the failure of `C_A` to be sufficient for the pair `{Q_I, Pi_I}` — a relative, not an
absolute, quantity. The derivation itself is careful ("the discarded conditional recognition and
posterior laws agree"); only the summary label is loose.

**Falsifier:** A place in the corpus where "conditional-information" is defined to mean "conditional
relative entropy". I found no definition of the phrase anywhere.

**Fix:** Use "conditional-KL VFE defect", or "the pair-relative conditional-divergence defect". If
"conditional-information" is kept, define it once: "conditional information here means the
conditional relative entropy `D(Qhat_{Y|Z} || Pihat_{Y|Z} | Q_A)`, not a mutual information."

---

### [LOW-3] "A finite VFE may be negative" is presented as a mathematical caveat; it is a units convention, and no VFE *level* in this framework is intrinsic

**Location:** `direct-derivation.md` §1 (the `lambda_X` declaration) and §6 (6.5)–(6.6);
`overview.md:546`; `solid_RG_theory.md:381`; `Theory/07b:172`; `appendix_claim_ledger.tex:203`;
`STATUS.md:319`.

**Claim as stated:**
> "Adding the same finite real \(-\log p_X(o)\) to both KL terms gives an extended-real VFE identity; **a finite VFE may be negative**."

**Defect:** True, but the reason is not stated and it is stronger than "may". `p_X = dnu_X/dlambda_X`
depends on the declared sigma-finite reference `lambda_X`; rescaling `lambda_X -> c*lambda_X` sends
`F -> F + log c` for any `c > 0`. So a finite `F` can be made *any* real number by a change of
reference measure, and no VFE **level** in this framework carries information — only differences
(`F_I - F_A = Delta_A`) and comparisons at a fixed declared `lambda_X` do. The document is otherwise
meticulous about version- and representative-dependence (it belabors selected posterior versions and
null-slice values), so the omission is conspicuous. It also explains why the sign caveat is needed
at all: in the discrete/counting-measure case `p_X(o) <= 1` and `F >= 0` always, which is presumably
where the reflex being guarded against comes from.

**Falsifier:** A place in the corpus stating that `F` is invariant under the choice of `lambda_X`, or
a normalization constraint on `lambda_X` I missed. §1 fixes `lambda_X` as free sigma-finite data.

**Fix:** One clause after (6.5): "The value of `F` depends on the declared `lambda_X` and shifts by
`log c` under `lambda_X -> c lambda_X`; only the defect `Delta_A` and comparisons at fixed
`lambda_X` are reference-independent, which is why no sign can be assumed for a finite VFE."

---

### [LOW-4] The measurability of the defect integrand is asserted rather than established

**Location:** `direct-derivation.md` §6, sentence before (6.8).

**Claim as stated:**
> "The equality condition is exact. **A nonnegative measurable function has zero integral exactly when it is zero almost surely**, and KL vanishes exactly at equality of probability measures."

**Defect:** Both cited facts are correct, but the premise that `z -> KL(Qhat(.|z) || Pihat(.|z))` is
*measurable* is used and never established. It is true — KL is jointly measurable in the pair of
measures under the standard Borel structure on `P(Y_I)`, and `z -> (Qhat(.|z), Pihat(.|z))` is
measurable as a disintegration — but in a document that spends paragraphs on selected-version
measurability elsewhere (e.g. the explicit remark that `o -> Pi_{A,o,X}(D)` is "measurable by
composition of kernels" after (3.5)), leaving this one implicit is inconsistent. Note the integral
in (6.4) needs the same fact, so it is load-bearing twice.

**Falsifier:** A sentence in §6 establishing the measurability. I read §6 in full; there is none.

**Fix:** One clause: "the integrand is measurable in `z` because `(mu,nu) -> KL(mu||nu)` is Borel on
`P(Y_I) x P(Y_I)` and the disintegrations are measurable kernels."

---

## Answers to the six mandate questions

1. **The KL chain.** Reconstructed from `phi_0(t) = t log t - t + 1` and verified numerically. The
   additive identity (6.4) is correct in `[0,+infty]` and is genuinely additive, not a disguised
   subtraction. **Every** rearrangement into a subtraction in the repository (ten sites, enumerated
   above) is fenced by the finiteness premise. No unfenced use found.
2. **The VFE identity.** Correct. `-log p_X(o)` is finite by declaration and identical at both scales
   because of (3.3). The resulting objects live in `(-infty,+infty]`, and **no later step uses
   nonnegativity of a VFE term**. The specific hazard I was asked to hunt does not occur. See
   [LOW-3] for the one presentational gap.
3. **The zero-defect criterion.** Both directions verified; correct with **no** finiteness premise,
   as `direct-derivation.md` (6.8) states. The integrand is genuinely a KL of probability kernels and
   the null set is with respect to `Q_A`, the correct measure. The `+infty = +infty` degenerate case
   cannot corrupt it because `Delta_A` is defined by the integral, never by subtraction. The
   *mathematical* repair is complete in `direct-derivation.md`; its *propagation* is not — the
   package's own strongest-theorem statement, ledger, and reconstruction still bind the criterion to
   the finite tier ([MEDIUM-2]), as do `solid_RG_theory.md` §8 and §11 ([MEDIUM-3]).
4. **The finite tier.** Clean pass for the subtraction form: all ten uses fenced. But the finiteness
   premise is attached to *more* than the subtraction — it is wrongly attached to the recovery
   equivalence ([MEDIUM-1]) and, in three package artifacts, to the zero-defect criterion
   ([MEDIUM-2]).
5. **Pairwise common recovery.** The two-way equivalence is correct as stated and, in fact, correct
   without the finiteness hypothesis ([MEDIUM-1]). The family-wide caveat is **asserted, never
   demonstrated**; the only family-wide counterexample in the corpus concerns Fisher equality at one
   parameter, not zero defect; and in the shared-posterior case family-wide recovery is a two-line
   corollary of the document's own (6.10)–(6.11) ([MEDIUM-4]).
6. **Is `Delta_A` the object the prose calls it?** It is exactly a conditional relative entropy,
   `D(Qhat_{Y|Z} || Pihat_{Y|Z} | Q_A)`, with the standard `Q_A` weighting. It is **not** a
   conditional mutual information and not a measure of information discarded by the channel; the
   label "conditional-information VFE defect" is looser than the object ([LOW-2]).

---

## Coverage

**Read in full:** `evidence/direct-derivation.md`; `evidence/reviews/view-information-vfe.md`;
`release.json`; `construction-or-strongest-theorem.md` §4.

**Read in relevant part (sections quoted above):** `claim-ledger.json` (VFE/target claims, evidence
records); `problem-contract.json` (`/target` extracted in full programmatically);
`evidence/counterexample-proofs.md` lines 95–175; `evidence/adversarial-attacks.md` A12–A16;
`evidence/independent-reconstruction.md` KL/VFE section;
`Theory/06_general_coarsegraining.tex` lines 60–320; `Theory/07b_agent_network_rg.tex` lines 140–185;
`Theory/appendix_claim_ledger.tex` lines 190–230; `overview.md` lines 470–590 and 760–810;
`solid_RG_theory.md` §8, §11, Phase 2; `docs/STATUS.md` lines 315–330;
`docs/change-logs/2026-08-15.md`.

**Mechanical checks actually run:** SHA-256 of five package artifacts against the review binding
table; `git log` per package file; `git show a623b6e` on the strongest-theorem document; a
3000-instance random finite check of the KL chain identity, the Bhattacharyya-affinity
disintegration, and affinity-DPI nonnegativity (scratchpad `check_affinity.py`, CPU Python, no
torch); repo-wide greps for the subtraction form, for VFE-nonnegativity assertions, and for
citations.

**Not reached:** `Theory/05_elbo.tex` in full; `evidence/notation-registry.json`,
`notation-collision-report.json`, `notation_scan.py`; `evidence/finite_nongaussian_witness.py` (not
executed — the witness arithmetic was verified by hand from `counterexample-proofs.md` instead);
`evidence/oracle-erasure.md`; `adversarial-report.json`; `approach-registry.json` beyond one grep;
`evidence/release-provenance.json` and `release-assembly.json` beyond `release.json`;
`evidence/reviews/view-probability-kernel.md`, `view-gauge-holonomy.md`, `view-dynamics-scope.md`
(other reviewers' lanes). The certification-integrity questions raised in [HIGH] and [MEDIUM-2]
touch the P0/P8 lanes and should be cross-checked there.
