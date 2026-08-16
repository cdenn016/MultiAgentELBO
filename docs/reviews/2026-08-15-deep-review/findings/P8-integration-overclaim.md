# P8 — Integration / Overclaim Audit (claim-vs-proof)

STATUS: COMPLETE

Reviewer role: claim auditing — compare what the integrated manuscript ASSERTS against what the
supporting derivation packages actually PROVE; find every place scope widens between proof and prose.

Review target: `8ce635807a6ca2a388255fc996c98f7c535e5843` (branch `review/2026-08-15-deep-review`).
Diff base: `060f80e5556e41e0f31aeafcd9ef8564c1544c16^`.

## Files to examine (checklist)

Integration surfaces (the ASSERTIONS):
- [x] `overview.md` (8/15 diff) — read in full (diff), plus §7 block and "Say this" block in context
- [x] `Theory/SPEC.md` (8/15 diff) — read in full (diff)
- [x] `Theory/appendix_claim_ledger.tex` (8/15 diff, ~140 added lines) — read in full (diff)
- [x] `Theory/05d_relational_inference.tex` (8/15 diff) — read in full (diff)
- [x] `Theory/01_introduction.tex`, `03_probability.tex`, `04_generative.tex` (8/15 diff) — read in full
- [x] `Theory/06_general_coarsegraining.tex`, `06a`, `07b`, `appendix_notation.tex` (8/15 diff) — read in full
- [x] `docs/STATUS.md` (8/15 diff) — read in full

Ground truth (the PROOFS):
- [x] `docs/derivations/2026-08-15-full-pointwise-meta-agent/final-report.md`, `problem-contract.json`,
      `evidence/direct-derivation.md`, `evidence/notation-standard.md`, `evidence/notation-registry.json`,
      `evidence/notation_scan.py` (hazard detector), `evidence/notation-collision-report.json`
- [x] `docs/derivations/2026-08-14-operational-intervention-extensions/final-report.md`, `problem-contract.json`
- [ ] NOT REACHED: `2026-08-15` `evidence/counterexample-proofs.md`, `adversarial-attacks.md`, `independent-reconstruction.md`
- [x] SAMPLED: `2026-08-14` `evidence/direct-derivation.md` §5, `counterexample-proofs.md` §3.2

Specific hunts:
- [x] H1 "full" pointwise candidate-parent theorem — does "full" mislead? does anything downstream glue?
- [x] H2 finiteness fence — swept every occurrence of `\Delta_A` and the recovery equivalence repo-wide
- [x] H3 conditional theorems presented as unconditional
- [x] H4 every added ledger row: status vs actual evidence; scope vs frozen contract
- [x] H5 "Say this, and not more" boilerplate in overview.md — sentence-by-sentence support check
- [x] H6 silent retractions

---

## Things that CHECK OUT (verified, no finding)

These are reported honestly as clean results; each was reconstructed, not accepted.

1. **The finiteness fence is complete across every integration surface.** I swept the whole repo for
   `\Delta_A`, `F_I-F_A`, and "recovery". Every non-package occurrence
   (`overview.md:545-550`, `Theory/SPEC.md:815-820`, `Theory/07b_agent_network_rg.tex:170-178`,
   `Theory/appendix_claim_ledger.tex:200-209`, `Theory/appendix_notation.tex:71-77`,
   `docs/STATUS.md:317-323`, `solid_RG_theory.md:381`,
   `docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md:3757-3761`) carries the same
   four-part fence: additive in `[0,+\infty]`; extended-real VFE identity after adding the finite
   `-\log p_X(o)`; unconditional zero-defect criterion; finite fine KL required for ordinary
   subtraction AND for the two-way pairwise recovery equivalence. I found **no** integration surface
   that uses the subtraction or the recovery equivalence without the premise. The pre-existing
   `thm:rg-exact-coarse-vfe` (`Theory/07b:34-58`) already carried the same fence
   ("If the fine KL is finite, their ordinary real-valued difference equals ..."), so the 8/15
   additions did not create an inconsistency with it either. **Hunt H2 returns zero findings.**

2. **The unconditional zero-defect criterion is genuinely unconditional.** Reconstructed:
   `\Delta_A=\int \KL(\hat Q(dY|z)\Vert\hat\Pi(dY|z))\,\mathbb Q_{A,o,X}(dz)` is the integral of a
   nonnegative measurable function; it vanishes iff the integrand vanishes `\mathbb Q_{A,o,X}`-a.s.,
   and `\KL=0` iff the two conditional laws coincide. No finiteness is used. The manuscript is
   correct to state this without the premise, and correct to fence only the subtraction and the
   recovery equivalence.

3. **`prop:hist-operational-quotient-universal-property` is correct as proved.** I reconstructed it:
   `\sim_\Phi` is an equivalence; `a\sim b \Rightarrow xay\sim xby` by associativity, so it is a
   two-sided congruence; `u=v=1` puts it inside `\ker\Phi`; any congruence `\approx\subseteq\ker\Phi`
   satisfies `a\approx b \Rightarrow uav\approx ubv \Rightarrow \Phi(uav)=\Phi(ubv)`, hence
   `\approx\subseteq\sim_\Phi` — largest. For a surjective unital homomorphism `q` with `\Phi=\psi q`,
   `\ker q` is a congruence inside `\ker\Phi`, so `h([q(a)])=[a]_{\sim_\Phi}` is well defined,
   surjective, unital, multiplicative, unique (by surjectivity of `q`), and `\bar\Phi h=\psi`.
   Finiteness is needed only for "equality of cardinalities ⇒ isomorphism". Terminality is correct.

4. **`thm:hist-compact-operational-quotient` is correct as proved.** Signature continuity into
   `Y^{D\times D}` (countable product of metrizable = metrizable), density + joint continuity of
   multiplication + continuity of `\Phi` + Hausdorff `Y` promotes `D\times D` agreement to all
   contexts; continuous bijection from compact `A/\sim` onto Hausdorff `S_D(A)` is a homeomorphism;
   `\pi\times\pi` is a closed continuous surjection from a compact space to a Hausdorff space hence a
   quotient map, giving continuity of `\bar m`; `\bar\Phi\pi=\Phi` gives continuity of `\bar\Phi`.

5. **`thm:hist-soft-bsc-target-face-nonidentifiability` arithmetic is exact.** Recomputed:
   `Q_b(t)(O=0\mid R=r)=b+(1-2b)t_r`; with `R` uniform,
   `\mathrm{TV}=\tfrac{|1-2b|}{2}(|t_0-t_0'|+|t_1-t_1'|)`; diameter over `[\epsilon,1-\epsilon]^2` is
   `|1-2b|(1-2\epsilon)`. For `L_1=L(1/4,1/3)`, `b=1/3`, `|1-2b|=1/3` → `(1-2\epsilon)/3`; for
   `L_2=L(1/3,1/4)`, `b=1/4`, `|1-2b|=1/2` → `(1-2\epsilon)/2`. The interior-witness separation
   `|1-2b|(s_+-s_-)` follows from `t=(s_-,s_-)`, `t'=(s_+,s_+)`. Also confirmed the shared passive
   crossover: `a+b-2ab=5/12` for both, giving the retained law `(7/24,5/24,5/24,7/24)`.

6. **`thm:hist-circle-heat-intervention-nonidentifiability` is correct as proved.** Recomputed both
   Fourier contradictions. If `H_s=H_tL`, put `g=Le_1`; `|g|\le1` by Markov positivity, but
   `H_tg=e^{-s}e_1` forces `\hat g(1)=e^{t-s}>1`, contradicting `|\hat g(1)|\le\|g\|_\infty\le1`.
   Forward garbling: `\nu H_t=(\nu H_{t-s})H_s` (heat semigroup commutes), giving the inclusion.
   Strictness: `\nu_\rho H_s=H_{\rho+s}(x_0,\cdot)`; equating to `\nu H_t` forces
   `|\hat\nu(1)|=e^{t-s-\rho}>1` for `0<\rho<t-s`. Both are valid.

7. **Both "no reconstruction from marginals" fences survived integration.** `Theory/07b` theorem body
   ("No displayed marginal pair reconstructs any of the corresponding full laws"),
   `appendix_claim_ledger.tex:197-199`, `SPEC.md`, `overview.md`, and `STATUS.md` all repeat it. The
   derivation `evidence/direct-derivation.md` §5 restricts to forward projections only. Consistent.

8. **The randomized-intervention determinant is a real derivation, not a numerical assertion.**
   `2026-08-14/.../counterexample-proofs.md` §3.2 exhibits the 15×15 contextual minor, the Bareiss
   recurrence, all fourteen pivots `p0…p13`, three named row interchanges, the final southeast entry
   `-(2b-1)^6(2d-1)^3/32`, and the row-swap sign `-1` that reconciles it with (3.3). The
   generic-field-then-specialize step is valid: both sides of (3.3) are polynomials in `(b,d)` and
   agree on a Zariski-dense open set where the pivots are nonzero, hence agree identically. I checked
   the closed form at both released points: `(2\cdot\tfrac13-1)^6(2\cdot\tfrac5{12}-1)^3/32
   = (1/729)(-1/216)/32 = -1/5038848` and `(1/64)(-1/216)/32 = -1/442368`, matching
   `recompute-output.json` and the manuscript. The package correctly labels the executable
   recomputation as corroboration and names the displayed matrix/pivots/sign as the proof. (Not
   verified: the 15×15 entries themselves and the pivot sequence.)

9. **The two late fence repairs are correct and did land.** `f4b1a61` replaced
   "Ordinary VFE subtraction, **zero-defect recovery**, and the pairwise common-recovery equivalence
   require finite fine KL" with "Zero defect is equivalent to equality of the discarded conditional
   laws without a finite-KL premise. Ordinary VFE subtraction and the two-way pairwise
   common-recovery equivalence require finite fine KL"; `063a5bb` added the missing
   `\mathbb Q_{A,o,X}`-almost-sure qualifier. Both are mathematically correct, and the pre-repair
   wording was *under*-claiming, not over-claiming. `Theory/appendix_notation.tex:71-77` now agrees
   with (6.7)/(6.8)/(6.12).

10. **`STATUS.md` §14 and `solid_RG_theory.md` §12 Phase 2 both carry the holonomy conditionality**
    that `overview.md:604` drops, and `solid_RG_theory.md` §11 correctly lists holonomy blindness
    under `CONDITIONAL` rather than `ESTABLISHED`. The failure is localized to one `overview.md`
    bullet, not systemic.

11. **The `\Cref` targets added to the ledger all resolve.** `thm:rg-pointwise-parent-datum`,
   `prop:hist-operational-quotient-universal-property`, `thm:hist-compact-operational-quotient`,
   `thm:hist-soft-bsc-target-face-nonidentifiability`,
   `thm:hist-randomized-hard-intervention-nonidentifiability`,
   `prop:hist-standard-borel-intervention-semantics`,
   `cor:hist-compact-feller-operational-quotient`,
   `thm:hist-circle-heat-intervention-nonidentifiability` all exist in `Theory/main.aux`. No dangling
   reference was introduced.

---

## Claim-by-claim table

Verdicts: **S** = SUPPORTED (proof establishes exactly this), **O** = OVERSTATED (true but weaker than
the prose implies, or a premise dropped), **U** = UNSUPPORTED, **?** = UNVERIFIABLE in this pass.

### A. `overview.md` §7 "Full pointwise candidate-parent theorem" (lines 534-556)

| # | Claim as written | Where the proof is supposed to be | What the proof actually establishes | Verdict |
|---|---|---|---|---|
| A1 | "manuscript status **ESTABLISHED**, release ledger `EVIDENCE_VERIFIED`, terminal status `COMPLETE_AFFIRMATIVE`, target digest `15336a68…`" | `release.json`, `claim-ledger.json` | Labels correctly transcribed. But they are bound to `add1a69` package bytes, not to the integrated manuscript. | S (transcription) / O (as support for the *manuscript*) |
| A2 | "a normalized recognition-independent \(C_A\) sends the fine generative joint, selected posterior-version family, and correlated recognition law to a normalized parent triple with the observation unchanged" | `direct-derivation.md` §§2–3, (3.1)–(3.6) | Exactly this: (3.2) with φ=f=1 gives normalization, (3.3) the unchanged observation marginal, (3.5) the parent posterior version, (3.6) absolute continuity. | S |
| A3 | "The parent model evaluator is either induced by disintegration or is a predeclared jointly measurable normalized family satisfying the explicit almost-sure compatibility condition." | (4.3)–(4.5) | Exactly this, with the correct warning that disintegration does not validate a predeclared family. Overview omits the standard-Borel premise that disintegration needs. | S (Low: premise elided) |
| A4 | "All named parent marginals are derived projections and do not reconstruct the joints." | §5, (5.2)–(5.3) | Exactly this; §5 explicitly declines the converse. | S |
| A5 | "The KL chain is additive in \([0,+\infty]\) with defect \(\Delta_A(o,X)\)." | (6.4) | Exactly this, via the nonnegative generator \(\phi_0(t)=t\log t-t+1\) and monotone truncations — a legitimate route avoiding signed-integrand rearrangement. | S |
| A6 | "Adding the same finite real \(-\log p_X(o)\) … a finite VFE may be negative." | (6.5)–(6.6) | Exactly this. `-\log p_X(o)` is finite by the admitted-observation declaration `0<p_X(o)<\infty`, and negative when `p_X(o)>1`. | S |
| A7 | "Without a finiteness premise, \(\Delta_A=0\) exactly when the discarded conditional … laws agree \(\mathbb Q_{A,o,X}\)-almost surely." | (6.8) | Proved unconditionally, and independently reconstructed here. But the frozen ledger claim bearing `EVIDENCE_VERIFIED` is finite-quantified. | S (math) / O (certification scope) |
| A8 | "Finite fine KL is required for ordinary subtraction … and for the two-way pairwise common-recovery equivalence; family-wide recovery still requires simultaneous hypotheses." | (6.7), (6.12) + closing remark | Exactly this, including "+∞=+∞ supplies neither". | S |
| A9 | "Holonomy blindness additionally requires typed actions, full fine-law covariance, compatible selected posterior versions, channel equivariance, evaluator covariance, and fixed-\((o,X)\) isotropy for same-slice invariance." | §7 (7.1)–(7.6) | Exactly this; the derivation also records that full-frame triviality is sufficient but not necessary. | S |
| A10 | "Raw root-framed holonomy retention is the alternative and selects no membership." | §7 final paragraphs | Exactly this. | S |
| A11 | Open list (canonical selection, comparison category, gluing, geometric meta-agency, autonomy, agency, nonequilibrium, continuum, physical time, unique DAG/physics, ontology) | `final-report.md` §Scope; `direct-derivation.md` §9 | Matches the package exclusion list item for item. | S |

### B. `overview.md` §8 live front and §9 open decision 1

| # | Claim as written | Proof location | What is actually established | Verdict |
|---|---|---|---|---|
| B1 | "Static Phases 1--2 are closed at one \(r_*\) by the released common-channel theorem." (line 604) | `HOLONOMY-BLIND-FULL-LAW` etc. | Phase 1 closed. Phase 2's holonomy half is a conditional implication under `ASM-HOLONOMY-BLIND-DATA`; its own exit condition asks to *prove* channel equivariance, which the theorem *assumes*. `solid_RG_theory.md` §12 and `STATUS.md` §14 carry the conditionality; `overview.md:604` does not. | O |
| B2 | "The next order is strict and remains OPEN/TODO: freeze the comparison category … participatory nonequilibrium and operational agency grades from one tower action or proved reduction without double counting." | `final-report.md` §Scope; `07b` `open:rg-pointwise-parent-dynamics` | Consistent. | S |
| B3 | "Relative to fixed operational data, the contextual protocol quotient is terminal and, for finite protocol monoids, has minimum class cardinality over the raw quotient map. This is not raw-realization minimality." | `05d` prop 9.29 | Reconstructed and correct; missing "surjective unital homomorphism" on `q`. | S / O (premise) |
| B4 | "In the frozen BSC category, equal passive retained law determines neither the reduced hard experiment, the normalized marked-soft mediator face, nor the independently randomized affine experiment." | `05d` thms 9.34, 9.37, 9.39 | Three theorems in three *different* morphism categories; the singular "the frozen BSC category" conflates them. | O |
| B5 | "The compact-Feller circle pair supplies the corresponding smooth continuous no-go under preserved heat geometry and ordered boundary roles." | `05d` thm 9.42 | Reconstructed and correct. | S |
| B6 | "Measurability alone does not establish a standard-Borel quotient; that requires an exhibited smooth classifier or stronger topology." | `05d` prop 9.40 proof | Exactly this. | S |

### C. `Theory/SPEC.md` additions

| # | Claim as written | Proof location | What is actually established | Verdict |
|---|---|---|---|---|
| C1 | "contextual equivalence is the largest two-sided congruence contained in `ker(Phi)`" | `05d` prop 9.29 | Correct; `05d` says "kernel **relation**" — SPEC drops "relation" for a non-homomorphism `Φ`. | S (Low: imprecision) |
| C2 | "Every response-compatible quotient `q:A->B` with `Phi=psi q` has one unique surjective unital factor `B->Syn(Phi)` over `A`." | `05d` prop 9.29 | Requires `q` a surjective unital **homomorphism**. | O |
| C3 | "If `A` is finite, it has minimum protocol-class cardinality, and equality of cardinalities gives the unique isomorphism over `A`." | `05d` prop 9.29 | Correct. Conservative: minimum cardinality also holds for infinite `A` in ZFC; only equality⇒iso needs finiteness. Under-claiming, not over-claiming. | S |
| C4 | "The same terminal factor is continuous for compact-Hausdorff response-compatible triples whose `q` and `psi` are continuous and whose `q` is a quotient map. Compactness and the quotient-map hypotheses are load-bearing." | `05d` thm 9.30 | Continuity of `h` follows from `hq=\pi` plus the quotient property of `q` alone; compactness of `B` is not used at that step. Extra hypothesis, so still true. | S (Low: over-hypothesized) |
| C5 | "exact total-variation diameters `(1-2epsilon)/3` and `(1-2epsilon)/2`, with strict-interior witnesses" | `05d` thm 9.37 | Recomputed exactly; correct. | S |
| C6 | "`det M(b,delta)=(2b-1)^6(2delta-1)^3/32`, nonzero for both models at `delta=5/12`" | `2026-08-14/.../counterexample-proofs.md` §3.2 | Derived symbolically by fraction-free Bareiss with 14 displayed pivots and an explicit three-row-swap sign; the generic→specialization step is a valid polynomial-identity argument. I verified the closed form reproduces `-1/5038848` (b=1/3) and `-1/442368` (b=1/4) at δ=5/12, matching `recompute-output.json`. I did **not** verify the 15×15 matrix entries or the pivot sequence. | S (partially verified) / ? (matrix entries) |
| C7 | "`H_s` strictly Blackwell-dominates `H_t`, and `{nu H_t}` is a proper subset of `{nu H_s}`" | `05d` thm 9.42 | Reconstructed and correct. | S |
| C8 | "Its manuscript theorem is **ESTABLISHED**; its package ledger records `target` as `EVIDENCE_VERIFIED`, and `release.json` records `COMPLETE_AFFIRMATIVE`." | `release.json`, `claim-ledger.json` | Transcription correct, and the separation of manuscript status from package labels is the right discipline. | S |
| C9 | "The selected parent posterior identity holds at the observation-kernel level, not by applying an almost-sure equality at an arbitrary exceptional observation." | `direct-derivation.md` §3 after (3.5) | Exactly this; the derivation is careful that (1.1) determines the kernel only `ν_X`-a.e. while the selected version is declared everywhere. | S |

### D. `Theory/appendix_claim_ledger.tex` added rows

| # | Row / claim | Status asserted | Package evidence | Verdict |
|---|---|---|---|---|
| D1 | "Operational intervention quotient and nonidentifiability (established)" — merged item covering universal property, compact quotient, hard/soft/randomized no-goes, Borel & compact-Feller tiers, circle pair | `ESTABLISHED` | All components exist in `05d` and are `EVIDENCE_VERIFIED` in the 8/14 package. The row names none of the three distinct morphism classes and drops the "TV is a diagnostic, not the proof invariant" sentence. | O |
| D2 | Universal-property display inside D1 | `ESTABLISHED` | Premise on `q` dropped. | O |
| D3 | "Category-independent intervention semantics (open)" | `OPEN` | Matches the 8/14 contract's excluded-extensions list. | S |
| D4 | "Full pointwise probabilistic datum (established)" | `ESTABLISHED` | Body matches `direct-derivation.md` clause for clause. Closing sentence imports `EVIDENCE_VERIFIED`/`COMPLETE_AFFIRMATIVE` onto an unconditional zero-defect statement whose frozen claim is finite-quantified. | S (body) / O (label scope) |
| D5 | "Partition selection and experiment-level recovery (open)": "what remains open is one common recovery kernel for an entire statistical experiment **without separately imposing simultaneous family hypotheses**" | `OPEN` | Matches (6.12) and its closing remark. Honest. | S |
| D6 | "Downstream comparison, gluing, and agency (open)": "none of its members lies in the static release ancestry" | `OPEN` | Matches `final-report.md` §Dependency closure (target + 17 ancestors; `DYNAMICS-SCOPE` a deliberate non-ancestor) and §Scope. | S |
| D7 | Deletion of "same **raw signature** and passive retained law" → "same passive retained law" | — | `05d:1245-1247` still asserts the stronger shared structure. The ledger now records a weaker antecedent, making the recorded no-go weaker than the one proved. Unrecorded weakening. | O (Low) |

### E. `Theory/05d_relational_inference.tex` added theorems

| # | Result | Verdict | Note |
|---|---|---|---|
| E1 | `prop:hist-operational-quotient-universal-property` | S | Reconstructed in full. |
| E2 | `thm:hist-compact-operational-quotient` | S | Reconstructed in full. |
| E3 | `def:hist-normalized-soft-intervention-monoid` | S | Compact metrizable right-override product with isolated `⊥_v`; response coordinates are finite sums of finite products of continuous kernel evaluations, hence continuous. |
| E4 | `thm:hist-soft-bsc-target-face-nonidentifiability` | S | TV formula and both diameters recomputed exactly. |
| E5 | `def:hist-affine-randomized-intervention-monoid` | S | Convolution monoid, affine response, unit = point mass at hard identity; flags that correlated selectors need a joint object. |
| E6 | `thm:hist-randomized-hard-intervention-nonidentifiability` | S (partial) | Vertex-preservation + convolution/unit ⇒ hard isomorphism is correct; determinant partially verified (C6). |
| E7 | `prop:hist-standard-borel-intervention-semantics` | S | Finite topological-order recursion + monotone class; correctly declines a standard-Borel quotient. |
| E8 | `cor:hist-compact-feller-operational-quotient` | S | Reverse-topological Feller integration ⇒ weak continuity; applies E2. |
| E9 | `thm:hist-circle-heat-intervention-nonidentifiability` | S | Both Fourier contradictions reconstructed. |
| E10 | `open:hist-typed-intervention-recovery` rewrite | S | Exclusion list matches the frozen contract. |

---

## Findings

### [MEDIUM] The 8/15 notation standard was not propagated into the body, and the scanner that certifies it is structurally blind to the two symbols it renamed

**Location:** `Theory/07b_agent_network_rg.tex:1886-1889` (body) vs `Theory/SPEC.md:240-243` and
`Theory/appendix_notation.tex:353-358` (standard);
`docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation_scan.py` `_hazards()`

**Claim as stated:** `Theory/SPEC.md` §3 is headed "**Notation — fixed, do not deviate**", and the
8/15 diff replaced, in both `SPEC.md` and `appendix_notation.tex`, the row
`\alpha_i,\beta_{ij},\eta_{ij}=\alpha_i\beta_{ij}` with

> `\alpha_i^x` the external normalized receiver occupancy in channel `x`. The marked event laws are
> `\eta_{ij}^q=\alpha_i^q\beta_{ij}` and `\eta_{ij}^m=\alpha_i^m\gamma_{ij}`.

`evidence/notation-standard.md` §"Collision and migration contract" states: "Active-source legacy
spellings are accepted only when the registry supplies the same alias, type, and scope … Every other
collision is `unclassified_collision` and makes the scanner fail." Commit `f4b1a61` is titled
"docs: correct zero-defect notation boundary" and the report records
`"unclassified_collision": 0`, `"status": "PASS"`.

**Defect:** The rename was never applied to the one place in the manuscript body where those symbols
carry a theorem. `Theory/07b_agent_network_rg.tex` §`sec:rg-meta-attention` still reads, verbatim:

```
Let $\alpha_i(y)$ be a normalized receiver occupancy and define the joint marked edge-event law
\eta_{ij}(y)=\alpha_i(y)\beta_{ij}(y),
```

`\alpha_i` and `\eta_{ij}` (unsuperscripted) are now undefined symbols: the notation appendix row that
defined them was deleted on 8/15, the registry lists `\alpha_i^x` and `\eta_{ij}^x` with
`"legacy_aliases": []`, and no legacy declaration covers them. This is exactly the situation the
migration contract says must fail the scanner. It does not, because `_hazards()` in `notation_scan.py`
searches for a hard-coded token list — `Q_q, Q_m, C_t, \varpi_i, P_A, Q_A, \mathscr P_G` (scale
redefinition), `P` (principal bundle), local dummy `P,Q`, `m_i`, `C_A` — and never looks for
`\alpha_i` or `\eta_{ij}` in any spelling.

**Evidence:** Re-ran the released scanner against the review revision:

```
$ python docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation_scan.py \
    --registry docs/derivations/.../evidence/notation-registry.json --root . --output <scratch>
notation collision scan: PASS (13 documented legacy; 103 immutable)
exit=0
```

and, from the released report, the complete token vocabulary it is capable of emitting contains
`\alpha_i^x` and `\eta_{ij}^x` but no bare `\alpha_i`/`\eta_{ij}` class at all:

```
tokens seen: ['C_A','C_t','P (principal bundle)','P,Q (local dummy measures)','P_A','Q_A','Q_m','Q_q',
 'R\to E\to O','\alpha_i^x','\beta_{ij}', ... ,'\eta_{ij}^x', ...]
counts {'canonical': 837, 'documented_legacy': 15, 'immutable_evidence': 91, 'unclassified_collision': 0}
```

`Theory/07b_agent_network_rg.tex` is in the scanned active set (`source_coverage.active_files`
includes it, and `\beta_{ij}` occurrences in it are recorded), so this is a detector gap, not a
coverage gap.

**Falsifier:** If a legacy declaration or registry alias covering bare `\alpha_i`/`\eta_{ij}` in
`Theory/07b` exists that I missed, or if `\alpha_i(y)`/`\eta_{ij}(y)` is elsewhere re-declared in
`Theory/` under the new standard, this finding is wrong. I grepped `Theory/*.tex` for
`\alpha_i^` and found occurrences only in `Theory/PIFB2.tex` (an *excluded*, non-`main.tex` document,
where `\alpha_i` means something else entirely) — never in `07b`.

**Fix:** Either rename the two lines in `Theory/07b_agent_network_rg.tex` §`sec:rg-meta-attention`
to `\alpha_i^q(y)` / `\eta_{ij}^q(y)`, or add an explicit `legacy_declarations` entry with that path
and line range. Independently, add `\alpha_i` and `\eta_{ij}` to `_hazards()`; without that the
scanner's PASS carries no information about the symbols the 8/15 standard actually changed, so
"zero-defect notation boundary" is not supported by the artifact cited for it.

### [MEDIUM] `docs/STATUS.md` §13 and §14 were added in the same commit range and contradict each other on whether Phases 1–2 are open

**Location:** `docs/STATUS.md` §13 ("2026-08-15 full meta-agent construction roadmap -- OPEN/TODO")
vs §14 ("2026-08-15 full pointwise probabilistic datum -- current authority")

**Claim as stated:** §13: "This section records the next dependency order only. It proves no theorem,
modifies no release, and **does not promote** the certified fixed-$r_*$ pair of parent marginals to a
full pointwise probabilistic meta-agent datum. … the full datum still requires generative,
recognition, and posterior objects plus the VFE and model interfaces." Its table then lists, under the
heading "**OPEN deliverable**", rows 1 ("Full pointwise probabilistic meta-agent datum at fixed
$r_*$") and 2 ("Pointwise VFE and holonomy closure").

§14, immediately below: "**Static Phases 1--2 are closed only at this pointwise level.**"

**Defect:** Both sections landed in the 8/15 diff. As committed, the same file simultaneously lists
Phase 1 and Phase 2 as OPEN deliverables and declares them closed, with no supersession pointer in
either direction. §12 explicitly says "This chronological correction supersedes … Section 11", so the
document does use explicit supersession notes elsewhere; §14 carries none, and §13 carries no
"superseded by §14" note. A reader consulting §13 (the section a roadmap-oriented reader would open)
gets the wrong status.

**Evidence:** `git diff 060f80e^ 8ce6358 -- docs/STATUS.md` adds §12, §13 and §14 in one hunk; §13's
table header is literally `| Order | OPEN deliverable | Exit condition before the next phase |` with
rows 1 and 2 as above, and §14's fourth paragraph begins "Static Phases 1--2 are closed only at this
pointwise level."

**Falsifier:** If §14 or §13 contains a cross-reference marking the supersession that I missed. I read
the full added text of both sections; neither names the other.

**Fix:** One sentence in §13: "Orders 1 and 2 are closed by Section 14; Orders 3–5 remain open."

### [MEDIUM] The universal-property row drops the "surjective unital monoid homomorphism" hypothesis on `q`

**Location:** `Theory/appendix_claim_ledger.tex:93-110`; `overview.md:82-88`; `docs/STATUS.md` §12
row "Contextual operational quotient"

**Claim as stated:** Ledger: "Fix a monoid \(A\) and a response \(\Phi\). … **For a compatible
quotient \(q\)**, write \(\pi:A\twoheadrightarrow\operatorname{Syn}(\Phi)\), \(q:A\twoheadrightarrow
B\), \(\Phi=\psi q\). There is one unique surjective unital homomorphism satisfying \(h:B
\twoheadrightarrow\operatorname{Syn}(\Phi)\), \(\pi=hq\), \(\bar\Phi h=\psi\)."
Overview: "Every response-compatible \(q:A\twoheadrightarrow B\) with \(\Phi=\psi q\) admits one
unique surjective unital homomorphism \(h\) …"
STATUS §12: "Every response-compatible `q:A->B` with `Phi=psi q` admits one unique surjective unital
`h:B->Syn(Phi)` …"

**Defect:** The theorem as proved in `Theory/05d_relational_inference.tex:1082-1112` requires
"**If \(q:A\to B\) is a surjective unital monoid homomorphism** and \(\Phi=\psi q\)". That hypothesis
is load-bearing and is not implied by "response-compatible" or by the double-headed arrow: for a bare
surjective *set* map `q` with `\Phi=\psi q`, `\ker q` need not be a congruence, `B` need not be a
monoid, and `h` need not exist. All three integration surfaces state the conclusion with only the
factorization condition `\Phi=\psi q` displayed.

**Evidence:** Counterexample to the statement as written in the three integration surfaces. Take
`A=(\{1,x\},\cdot)` the two-element monoid with `x^2=x`, `Y=\{0,1\}`, `\Phi(1)=1`, `\Phi(x)=0`.
Then `\sim_\Phi` is trivial and `\operatorname{Syn}(\Phi)=A`. Let `B=\{1,x\}` carry the *other*
monoid structure (the group `\mathbb Z/2`, `x^2=1`), let `q=\operatorname{id}` as a set map (a
surjection with `\Phi=\psi q` for `\psi=\Phi`). No unital *homomorphism* `h:B\to A` with `hq=\pi=\mathrm{id}`
exists, because `h=\mathrm{id}` is not multiplicative (`h(x\cdot_B x)=h(1)=1\ne x=h(x)\cdot_A h(x)`).
The 05d statement excludes this by requiring `q` to be a homomorphism; the ledger/overview/STATUS
wordings do not.

**Falsifier:** If "compatible quotient" / "response-compatible" is defined earlier in the ledger or
overview as "surjective unital monoid homomorphism with `\Phi=\psi q`". I searched
`appendix_claim_ledger.tex` and `overview.md`: neither defines the term. The definition exists only in
`05d` and in the frozen contract (`problem-contract.json`, `equivalence` field).

**Fix:** Insert "surjective unital monoid homomorphism" before `q` in all three places. This is a
one-phrase repair; the underlying theorem is correct.

### [HIGH] The four "APPROVE 0/0/0" domain reviews bind manuscript bytes that no longer match the reviewed revision, predate the substantive VFE correction, and one of them still states the pre-correction (finite-KL) zero-defect criterion

**Location:** `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/reviews/*.md`;
cited by `.../final-report.md` §Certificate and `.../release.json` `review_bindings`

**Claim as stated:** `final-report.md`: "The corrected-byte reviews are **current** `APPROVE` records
with Critical/High/Medium counts of zero: probability/kernel `14f7f00f…`, information/VFE `c291869c…`,
gauge/holonomy `431a63b0…`, and dynamics/scope `71401ff1…`." `release.json`:
`"unresolved_obligations": []`, `"terminal_status": "COMPLETE_AFFIRMATIVE"`.
`Theory/appendix_claim_ledger.tex:212-216` then imports those labels into the manuscript:
"The manuscript status is \textsc{established}; the bound release records ledger state
`EVIDENCE_VERIFIED` and terminal package status `COMPLETE_AFFIRMATIVE`."

**Defect:** Three of the four reviews carry a "frozen review identity" table binding the *manuscript*
sources they consulted. They bind

```
Theory/06_general_coarsegraining.tex  4891a8f5fa86ac0fa5266381e2c67161125645034ca40395cb2e3ed1b67dc9b2
Theory/07b_agent_network_rg.tex       5eb159493ec727218e2eaca4cf47f3fddeb090f6e193352846ad2a43181437ca
```

At the reviewed revision `8ce6358` those files hash to `fa10620d2a1d…` and `268f9c3b75b0…`. The
reviews were written at `HEAD add1a69`; the manuscript integration (`b9ba51f`), the substantive VFE
scope correction (`fe08359`), and two further notation corrections (`f4b1a61`, `063a5bb`) all landed
afterward. So the reviews (a) never examined the integrated manuscript prose that
`overview.md`, `SPEC.md`, `appendix_claim_ledger.tex` and `STATUS.md` now assert, and (b) their own
recorded bindings are stale by the package's own freshness discipline.

Confirmation that the staleness is substantive, not clerical: `view-probability-kernel.md:51` states
"**On finite fine KL**, zero defect is equivalent to equality of discarded conditionals `Q_A`-almost
surely" — precisely the formulation that `fe08359` was committed to repair, and which the manuscript
now states *without* the finiteness premise. A review whose text asserts the superseded form cannot
be a current approval of the superseding text.

**Evidence:**

```
$ python -c "...sha256..."
fa10620d2a1d0e51b5a50b88d0a7434afcde6a0112af062e74fed586e97d7166 Theory/06_general_coarsegraining.tex
268f9c3b75b09966ed05a6c08e0cbd3f17188d88143f599037ff371d9c3e598c Theory/07b_agent_network_rg.tex
2aa70b07751d07712a3d9395f77817317d48d77d97c3fd5fb8cd1a3f6fda226a docs/.../evidence/direct-derivation.md   (matches the certificate)
```

```
$ git log --oneline 060f80e^..8ce6358
8ce6358 Merge pull request #4 ...
063a5bb docs: finalize zero-defect closure wording      <- Theory/appendix_notation.tex
f4b1a61 docs: correct zero-defect notation boundary     <- Theory/appendix_notation.tex
9ddd757 docs: close full pointwise meta-agent program
fe08359 docs: correct pointwise VFE scope               <- 8 canonical files incl. 06, 07b, SPEC, ledger
b9ba51f docs: integrate pointwise probabilistic datum   <- the whole manuscript integration
a623b6e / 1b18842 / add1a69 ...                          <- reviews bound here
```

`docs/change-logs/2026-08-15.md:39` concedes the gap and points the binding for the final commits at
`.verification/ledger.json`. That file is git-ignored (`.gitignore:25`), its content stops at
`2026-08-13`, and it contains **zero** occurrences of `2026-08-15` or of any of the four late commit
SHAs:

```
$ git check-ignore -v .verification/ledger.json
.gitignore:25:.verification/  .verification/ledger.json
$ grep -c "2026-08-15" .verification/ledger.json
0
$ python -c "... re.findall(r'2026-08-\d\d', json)"   ->  ['2026-08-12', '2026-08-13']
```

So no artifact — tracked or untracked — records any gate result for the last four commits of the
reviewed revision, including the one that repaired a substantive scope defect.

**Falsifier:** If the two Theory hashes in the review tables refer to a *pre-integration* working
copy that the reviews deliberately treated as background context rather than as reviewed artifact,
and some *other* artifact records a post-`fe08359` review of the integrated prose. The change log
(line 35) does claim "Four domain views, a structured skeptic, and an evidence-weighted adjudicator
reviewed commit `fe08359…` and approved that corrected central content with 0/0/0" — but no such
review artifact exists in the repository; the only review files present are the four bound to
`add1a69`. If those artifacts exist somewhere I did not look, this finding weakens to Medium.

**Fix:** Do not import the package labels into the manuscript ledger as if they certified the
manuscript prose. Either (i) restate `appendix_claim_ledger.tex:212-216` as "the bound *package*
records … for the frozen package bytes at `add1a69`; the manuscript integration is not covered by
those reviews", or (ii) produce a review artifact bound to the integrated bytes and commit it.

### [MEDIUM] The manuscript asserts an unconditional zero-defect criterion; the frozen package claim that carries the `EVIDENCE_VERIFIED` label is quantified over finite fine KL only

**Location:** `Theory/appendix_claim_ledger.tex:200-216`, `Theory/07b_agent_network_rg.tex:172-176`,
`Theory/SPEC.md:816-820`, `overview.md:547-550`, `docs/STATUS.md:319-323`
vs `docs/derivations/2026-08-15-full-pointwise-meta-agent/claim-ledger.json`
claim `VFE-FINITE-ZERO-DEFECT-RECOVERY`

**Claim as stated:** Manuscript (all five surfaces, identical wording): "**Without a finiteness
premise**, \(\Delta_A=0\) exactly when the discarded conditional recognition and posterior laws agree
\(\mathbb Q_{A,o,X}\)-almost surely." The ledger row then closes with "The manuscript status is
\textsc{established}; the bound release records ledger state `EVIDENCE_VERIFIED` and terminal package
status `COMPLETE_AFFIRMATIVE`."

Frozen package claim `VFE-FINITE-ZERO-DEFECT-RECOVERY` (state `EVIDENCE_VERIFIED`):
> statement: "**When fine KL is finite**, the ordinary VFE difference equals Delta_A; Delta_A=0
> exactly when discarded conditional recognition and posterior laws agree Q_A-a.s., equivalently when
> one normalized pairwise recovery kernel recovers both fine laws."
> quantifiers: "**For every in-scope common-channel pair with finite KL(Q_{I,o,X}||Pi_{I,o,X})**."

**Defect:** The certified claim's quantifier is restricted to finite fine KL. The manuscript states a
strictly larger claim and, in the same paragraph, attaches the `EVIDENCE_VERIFIED` /
`COMPLETE_AFFIRMATIVE` labels to it. The labels do not reach the extra generality.

To be explicit about which way this cuts: **the manuscript's stronger statement is mathematically
correct**, and I verified it independently (see "Things that check out", item 2); it is also stated
unconditionally in the package's own derivation at `evidence/direct-derivation.md` eq. (6.8) and the
sentence immediately after it. So this is a certification-scope defect, not a false theorem. But the
claim ledger — whose whole function is to record exactly what is certified and how far — records a
label that its bound artifact does not carry at that scope.

**Evidence:** `claim-ledger.json` claim `VFE-FINITE-ZERO-DEFECT-RECOVERY` verbatim above (extracted
by JSON read). No other claim in the 19-claim ledger asserts an infinite-tier zero-defect criterion:
`VFE-CHAIN-EXTENDED` covers only the additive identity in `[0,+\infty]`, not the equality criterion.

**Falsifier:** If some other claim record (e.g. `VFE-CHAIN-EXTENDED`) is intended to carry the
unconditional criterion. Its statement — "the additive `[0,+infinity]`-valued KL disintegration …
and the corresponding extended VFE identity without infinity-minus-infinity" — contains no equality
criterion, so it does not.

**Fix:** In `appendix_claim_ledger.tex`, attribute the unconditional criterion to
`evidence/direct-derivation.md` (6.8) rather than to the release label, e.g. "…agree
\(\mathbb Q_{A,o,X}\)-almost surely (proved unconditionally in the bound derivation; the frozen
release claim `VFE-FINITE-ZERO-DEFECT-RECOVERY` is quantified on the finite tier)."

### [MEDIUM] The merged ledger row conflates three intervention no-goes proved in three different morphism categories, and silently deletes the previously recorded statement of which invariant carries the hard proof

**Location:** `Theory/appendix_claim_ledger.tex:93-160` (item "Operational intervention quotient and
nonidentifiability (established)"); `overview.md:88-104`; `overview.md` "Say this" block line ~779

**Claim as stated (new):** One item, one `\status{ESTABLISHED}`, covering: the hard fifteen-class
nonisomorphism; "The same pair has unequal exact marked-soft mediator-face diameters,
\((1-2\epsilon)/3\) and \((1-2\epsilon)/2\)"; the randomized affine no-go; the Borel/compact-Feller
tiers; and the circle heat pair. "Say this" block: "In the declared BSC category, one passive
retained law determines neither the reduced hard experiment, the normalized marked-soft mediator
face, nor the independently randomized affine experiment."

**Claim as stated (deleted on 8/15, from the same ledger item):**
> "The first model's \(\operatorname{do}(E=0)\) response is absent from the complete second-model
> response image under all four admitted typed boundary flips. **That image obstruction, not mediator
> total variation, proves** \Cref{thm:hist-finite-typed-intervention-nonidentifiability}."
and, from "Say this": "Null-node collapse is a control and **mediator total variation is diagnostic,
not the proof invariant**."

**Defect:** Two problems, both about scope.

(1) There is not one "declared BSC category". The hard theorem's admitted morphisms include *four
independent typed binary boundary relabelings of `R` and `O`* and need not preserve the named
mediator pair — which is exactly why `05d`'s proof says the total-variation contrast is a diagnostic
there. The marked-soft theorem *requires* mediator-target retention
(`05d`: "Retain the mediator-replacement face … The theorem retains the mediator target"), and the
randomized theorem requires affine unital convolution-monoid isomorphisms. These are three different
categories with three different admitted-morphism classes. The ledger row states none of the three
restrictions, and the "Say this" block names a single category.

(2) The deleted sentences were the ones preventing the exact confusion the new text now invites: the
new soft diameters are `(1-2\epsilon)/3` and `(1-2\epsilon)/2`, which at `\epsilon\to0` are literally
the `1/3` and `1/2` numbers the old ledger said were "diagnostics, not the proof invariant". After
8/15 the caveat survives only in `05d`'s proof paragraph and in `docs/STATUS.md` §11; it is gone from
the ledger, from `overview.md` §2, and from "Say this".

**Evidence:** `git diff 060f80e^ 8ce6358 -- Theory/appendix_claim_ledger.tex` shows both sentences on
`-` lines. `Theory/05d_relational_inference.tex:1285-1289` still contains, inside the hard theorem's
proof: "The mediator-output total-variation contrasts, \(1/3\) for \(L_1\) and \(1/2\) for \(L_2\),
are diagnostics only: an arbitrary protocol-class bijection need not preserve the named mediator
pair. The complete response-image mismatch is the proof invariant." `05d:1263-1265` states the hard
category's morphisms as "all four independent typed binary boundary relabelings of \(R\) and \(O\)";
`05d:1338-1341` states the soft theorem's as "Retain the mediator-replacement face, the ordered roles
… and one global typed response intertwiner."

**Falsifier:** If the ledger or "Say this" defines "the declared BSC category" to include mediator
retention. It does not; `overview.md` line ~790 explicitly says "**Where declared**, the marked-soft
and circle comparisons retain the mediator target", conceding the categories differ.

**Fix:** Split the ledger item into "hard (established)" / "marked-soft, mediator-retaining
(established)" / "independently randomized affine (established)", each with its morphism class named,
and restore one clause: "in the hard category the total-variation contrast is a diagnostic, not the
proof invariant; the soft result upgrades it to an invariant only because mediator retention is
imposed."

### [MEDIUM] The 8/15 operational-intervention integration — roughly half the diff under review — has no change-log entry, and the change log that exists disclaims the merge that produced the reviewed revision

**Location:** `docs/change-logs/2026-08-15.md` (the only change log in `docs/change-logs/`)

**Claim as stated:** "## Scope — This session executed the approved full pointwise meta-agent program
in the isolated branch `codex/full-meta-agent-implementation-20260815`." and "Publication was not
authorized: no push, merge, or `main` advancement occurred." The document then narrates Tasks 1–7,
all of them belonging to the pointwise meta-agent program.

**Defect:** Two *separate* programs landed on 2026-08-15. Commits `060f80e..8c0f4d5` are the
operational-intervention-extensions program; `ceffda2..063a5bb` are the pointwise meta-agent program.
Commit `8c0f4d5` ("docs: integrate operational intervention extensions") alone touched
`Theory/05d_relational_inference.tex` (+324), `Theory/SPEC.md` (+64), `Theory/appendix_claim_ledger.tex`
(+87), `docs/STATUS.md` (+21), `overview.md` (+136) — i.e. it is the source of `STATUS.md` §12, most
of the 140 added ledger lines, the entire `overview.md` §2 rewrite, and the deletion of the
"mediator total variation is diagnostic, not the proof invariant" fence documented in the previous
finding. None of that appears in any change log. Per the repository's own convention (global
`CLAUDE.md`: "After a session's edits, write a `.md` describing all changes made to the codebase.
One document per day"), the day's log is required to cover the day's edits and does not.

The `no merge occurred` sentence is true of the agent session but is false of the artifact it now
ships inside: the reviewed revision `8ce6358` *is* the merge of that branch into `main`.

**Evidence:**
```
$ git log --oneline 060f80e^..8ce6358          # 23 commits, two distinct programs
$ git show --stat 8c0f4d5
 Theory/05d_relational_inference.tex | 324 ++, Theory/SPEC.md | 64 ++, Theory/appendix_claim_ledger.tex | 87 ++,
 docs/STATUS.md | 21 ++, docs/research-plans/2026-08-12-...worklog.md | 182 ++, overview.md | 136 ++
$ git log --oneline -S"mediator total variation is diagnostic" -- overview.md Theory/appendix_claim_ledger.tex
8c0f4d5 docs: integrate operational intervention extensions
$ ls docs/change-logs/
2026-08-15.md
```

**Falsifier:** If a change log for the operational-intervention program exists elsewhere. I listed
`docs/change-logs/` in full: `2026-08-15.md` is the only file.

**Fix:** Add a Section covering `060f80e..8c0f4d5` to `docs/change-logs/2026-08-15.md`, explicitly
listing the fence deletions, and correct the merge sentence to name the session rather than the
repository state.

### [MEDIUM] "Static Phases 1--2 are closed" over-reads Phase 2's own exit condition, which asks for a *proof* of channel equivariance that the released theorem instead *assumes*

**Location:** `overview.md:604-611`; `docs/STATUS.md:329`; exit condition at `docs/STATUS.md` §13
table row 2

**Claim as stated:** `overview.md:604`: "**Full pointwise probabilistic datum -- ESTABLISHED.**
Static Phases 1--2 are closed at one \(r_*\) by the released common-channel theorem."
`STATUS.md:329`: "Static Phases 1--2 are closed only at this pointwise level."

Phase 2's exit condition, as written in the same commit (`STATUS.md` §13 row 2): "Prove the
common-channel conditional-KL defect and normalization; declare the joint holonomy actions;
**prove coarse-channel equivariance** and the appropriate covariance or invariance of
\(\mathbb P_A\), \(\mathbb Q_A\), and \(\boldsymbol\Pi_A\)."

**Defect:** The released theorem does not prove coarse-channel equivariance for any channel; it
*requires* it. `Theory/07b_agent_network_rg.tex` eq. `eq:rg-pointwise-parent-holonomy-channel` is
introduced by "**require** \(C_A(g\cdot Y,g\cdot D)=C_A(Y,D)\)", and the derivation's (7.4) is listed
among the hypotheses of §7 with the explicit remark "(7.2) is an explicit version hypothesis;
almost-sure uniqueness of regular conditionals does not choose covariant null-slice values
automatically." What is established is the implication "declared equivariance + declared covariance
⇒ parent covariance", i.e. `HOLONOMY-BLIND-FULL-LAW` in the package ledger, whose quantifier is
"For every groupoid arrow and datum satisfying `ASM-HOLONOMY-BLIND-DATA`."

`overview.md:604`'s bullet carries no premise at all. `STATUS.md:329` is better — the immediately
preceding paragraph lists the holonomy premises — but its qualifier is "only at this pointwise
level", i.e. it fences the *base point*, not the *conditionality*.

**Evidence:** `Theory/07b_agent_network_rg.tex` §"Full-law holonomy alternatives", the sentence
beginning "For a holonomy-blind parent, **supply** bimeasurable typed groupoid actions … **require**
the fine generative and recognition laws to be covariant; **select** a posterior-version family
compatible with those actions; **require** [equivariance] … and **require** evaluator covariance."
Every verb is a hypothesis verb. `evidence/direct-derivation.md` §7 (7.1)–(7.4) likewise.
`claim-ledger.json`: `HOLONOMY-BLIND-FULL-LAW.quantifiers = "For every groupoid arrow and datum
satisfying ASM-HOLONOMY-BLIND-DATA."`

**Falsifier:** If Phase 2's exit condition is read as "prove the *consequences of* coarse-channel
equivariance". The row's own next sentences ("A holonomy-blind path-independent parent needs full-law
compatibility, while a richer parent may retain holonomy as internal state") support the conditional
reading, so this is a wording defect rather than a false claim — hence Medium, not High.

**Fix:** `overview.md:604`: "Static Phase 1 is closed at one \(r_*\); Phase 2 is closed conditionally,
on the declared typed actions, fine-law covariance, compatible selected posterior versions, channel
equivariance, and evaluator covariance — the released theorem assumes these rather than exhibiting a
channel that satisfies them."

### [LOW] `overview.md` §7 omits the standard-Borel premise and the finite-evidence admission condition that the theorem statement carries

**Location:** `overview.md:537-543`

**Claim as stated:** "For a finite child block \(I\), parent label \(A\), one fixed
\(r_*\in\mathcal U_A\), fixed structural \(X\), and **one admitted observation**, a normalized
recognition-independent \(C_A\) sends … The parent model evaluator is either **induced by
disintegration** or is a predeclared jointly measurable normalized family …"

**Defect:** `Theory/07b_agent_network_rg.tex` states "Let \(\mathsf O,\mathsf Y_I,\mathsf B_A,
\mathsf M_A,\boldsymbol\Xi_A\), and \(\mathsf H_A\) be nonempty **standard-Borel** spaces" and "At an
admitted \(o\) **with a finite positive evidence representative**". The overview block drops both.
Standard-Borelness is what makes "induced by disintegration" available at all; the finite positive
evidence representative is what makes the pointwise `-\log p_X(o)` term meaningful on a continuous
`O`. Every other integration surface (`SPEC.md`, `STATUS.md` §14, `solid_RG_theory.md`, and the ledger
via "Under the hypotheses of \Cref{thm:rg-pointwise-parent-datum}") states at least the standard-Borel
premise.

**Evidence:** `overview.md` §7 block versus `Theory/07b_agent_network_rg.tex:76-100` and
`evidence/direct-derivation.md` §1 lines 15-53.

**Falsifier:** If `overview.md` states standard-Borelness earlier in a way that governs §7. Its symbol
table row for `\mathcal B_b,\mathcal B_m` mentions "declared subsets of \(\mathcal P(\mathsf K)\)" but
the four parent factor spaces added on 8/15 carry no regularity in that table.

**Fix:** Add "declared standard-Borel spaces" and "with a finite positive evidence representative" to
the first sentence of the block.

### [LOW] `06_general_coarsegraining.tex`'s new specialization paragraph reads as if the test identity pins the parent posterior at every observation

**Location:** `Theory/06_general_coarsegraining.tex:304-331` ("Pointwise parent specialization")

**Claim as stated:** "\(\boldsymbol\Pi_{A,o,X}=\boldsymbol\Pi_{I,o,X}C_A\) … **for every \(o\) in the
selected version family**. Indeed, for bounded measurable \(f\) on \(\mathsf O\) and \(g\) on
\(\mathsf Z_A\), [test identity], **which is the defining test-function identity for the displayed
selected parent posterior version**."

**Defect:** The composition `\boldsymbol\Pi_{I,o,X}C_A` is indeed defined at every `o`, but the
displayed test-function identity determines a regular conditional only
`\mathbb P_I^O(\cdot\mid X)`-almost everywhere. Placing "for every \(o\)" immediately before an
identity that holds a.e. invites the reading that the identity itself is pointwise. The bound
derivation is explicit about this (`direct-derivation.md` §1: "The selected kernel is declared on
every observation, while (1.1) determines it only \(\nu_X\)-almost everywhere"; §3: "(3.4) selects a
globally measurable parent version, including declared exceptional-point values inherited from the
fine selected version"). `SPEC.md` states the distinction correctly ("holds at the observation-kernel
level, not by applying an almost-sure equality at an arbitrary exceptional observation"). Only the
`06` paragraph is compressed.

**Evidence:** `Theory/06_general_coarsegraining.tex:307-325` vs `evidence/direct-derivation.md`
lines 45 and 141.

**Falsifier:** If `\Cref{thm:cg-evidence-preserving-channel}`, which the paragraph specializes,
already carries the everywhere/a.e. distinction in a way the reader has in hand. It states the
pushforward construction; the version-selection caveat sits at `06:497-499`, a different section.

**Fix:** Change "for every \(o\) in the selected version family" to "at every \(o\), by composition of
the selected fine version with \(C_A\); the displayed test identity characterizes it
\(\mathbb P_I^O(\cdot\mid X)\)-almost everywhere."

### [LOW] `07b`'s holonomy-equivariance equation writes one `C_A` on both sides of a groupoid arrow whose source and target spaces the derivation keeps distinct

**Location:** `Theory/07b_agent_network_rg.tex` eq. `eq:rg-pointwise-parent-holonomy-channel`

**Claim as stated:** "require \(C_A(g\cdot Y,g\cdot D)=C_A(Y,D)\), for every admitted arrow and
measurable parent event".

**Defect:** The bound derivation writes the same hypothesis as
\(C_A'(T_I^gY,D)=C_A(Y,(T_A^g)^{-1}D)\) (eq. 7.4), with a *primed* channel on the target slice,
because an arrow \(g:(o,X)\to(o',X')\) has bimeasurable actions between *different* declared spaces
\(\mathsf Y_I\to\mathsf Y_I'\), \(\mathsf Z_A\to\mathsf Z_A'\). Writing `C_A` on both sides silently
identifies source and target channels, which is exact only for isotropy arrows — the very case the
next sentence is careful to separate ("Same-slice invariance at a fixed \((o,X)\) follows only for
isotropy arrows"). The two forms coincide under that identification, so this is notation compression,
not a false claim.

**Evidence:** `evidence/direct-derivation.md` (7.4) plus "with source and target spaces understood
from the arrow"; `07b`'s equation carries no prime.

**Falsifier:** If `07b`'s "typed groupoid actions" sentence declares one ambient space so that
`C_A' = C_A` by construction. It says "bimeasurable typed groupoid actions on the complete fine random
space, the parent space \(\mathsf Z_A\), the unchanged observation space, and structural data" —
singular spaces, which supports the identification reading but then makes the groupoid an action
groupoid on one object, weaker than the derivation's setting.

**Fix:** Prime the target-slice channel to match (7.4), or say explicitly that the equation is written
for arrows within one declared slice.

---

## Hunt verdicts

**H1 — does "full" mislead?** No, in the manuscript. Every occurrence of "full" attaches to *full law*
as opposed to *marginals*, and is paired with "pointwise" plus an exclusion list.
`Theory/07b` follows the theorem with a `\status{NOT-CLAIMED}` block naming exactly what "full" does
*not* mean ("no parent local sections over \(\mathcal U_A\), patch gluing, geometric meta-agent,
autonomous dynamics, agency, nonequilibrium persistence, continuum limit, physical time, unique latent
DAG, unique microscopic physics, or ontology"). `STATUS.md` §13 goes further: "Even that completed
fixed-point datum is not a geometric meta-agent; geometric language requires patchwise local sections
and gluing in Phase 4." The residual risk is in *program* names ("full meta-agent implementation",
"full meta-agent construction roadmap"), where "full" reads as modifying "meta-agent"; those are
branch and section titles, not claims. No finding.

**Does anything downstream treat the theorem as more than one point?** No. I traced all six
cross-references to `thm:rg-pointwise-parent-datum` (`06:331`, `07b:1788`, `07b:2165`,
`appendix_claim_ledger:191`, `:222`, plus its own statement). None quantifies over `r`, none glues
over `\mathcal U_A`; `07b:1788` and `:2165` are the two-alternative holonomy paragraph and the open
dynamics problem. The `06` specialization quantifies over the *observation*, not over `r_*`, and that
quantification is supported by the derivation (see the LOW finding for the wording). No finding.

**H2 — finiteness fence.** Complete across all integration surfaces; zero findings (see "Things that
check out", item 1). The recorded repairs (`fe08359`, `f4b1a61`) and the a.s.-qualifier repair
(`063a5bb`) did land on every surface. I verified this by an independent repo-wide sweep rather than
by trusting the change log.

**H3 — conditional theorems presented as unconditional.** One instance (`overview.md:604`, MEDIUM),
plus premise elision in the universal-property statements (MEDIUM) and in `overview.md` §7 (LOW). The
pointwise theorem's affirmative premises are otherwise correctly carried on every surface read.

**H4 — added ledger rows.** See table §D: four rows fully supported, three overstated in scope
(D1, D2, D4), one silently weakened (D7).

**H5 — "Say this, and not more".** Fourteen substantive sentences; twelve supported verbatim against
the packages. The two exceptions: the singular "the declared BSC category" (folded into the
morphism-category MEDIUM finding), and the omission of the evaluator seam from the pointwise sentence
— the block says the theorem "constructs normalized parent generative, selected posterior, and
correlated recognition laws … derives their marginals, and reports the exact conditional-information
VFE defect" without noting that the model coordinate acquires generative meaning only through an
induced or explicitly compatible evaluator. One clause would repair it; I did not raise it separately
because `SPEC.md`, the ledger, `STATUS.md` and `07b` all carry the seam.

**H6 — silent retractions.** Three found, all in `8c0f4d5`: the "mediator total variation is
diagnostic, not the proof invariant" fence (removed from the ledger, `overview.md` §2, and "Say this";
surviving only in `05d`'s proof paragraph and `STATUS.md` §11); the "same raw signature" antecedent
(D7); and the explanatory clause "because one complete response-image element remains unmatched under
every admitted boundary flip" (removed from `overview.md` §2). None is recorded in any change log —
see the change-log MEDIUM finding.

---

## Summary counts

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 1 |
| Medium | 5 |
| Low | 4 |

No stated theorem in the 8/15 additions was found to be false. Every load-bearing mathematical claim
I could reconstruct — the KL chain and its equality criterion, the syntactic-quotient universal
property and its compact version, the soft-BSC total-variation diameters, the circle heat-kernel
Blackwell and response-set separations, and the closed-form determinant at the two released points —
checked out. The defects are in the *certification chain* and in *scope wording*: an approval record
that does not cover the reviewed bytes, three premise elisions, one conflation of three morphism
categories, one document-internal status contradiction, one incomplete notation migration whose
verifier is blind to the symbols it renamed, and an undocumented half of the day's diff.

## Coverage

**Read in full:**
- `git diff 060f80e^ 8ce6358` for: `overview.md`, `Theory/SPEC.md`, `Theory/appendix_claim_ledger.tex`,
  `Theory/05d_relational_inference.tex`, `Theory/01_introduction.tex`, `Theory/03_probability.tex`,
  `Theory/04_generative.tex`, `Theory/06_general_coarsegraining.tex`, `Theory/06a_generative_gaussian.tex`,
  `Theory/07b_agent_network_rg.tex`, `Theory/appendix_notation.tex`, `docs/STATUS.md`,
  `solid_RG_theory.md` (first 160 diff lines, covering §§1, 9, 11, 12).
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/`: `final-report.md`, `problem-contract.json`,
  `release.json`, `claim-ledger.json` (all 19 claims listed; five read in full),
  `evidence/direct-derivation.md` (all 499 lines), `evidence/notation-standard.md`,
  `evidence/notation-registry.json`.
- `docs/derivations/2026-08-14-operational-intervention-extensions/`: `final-report.md`,
  `problem-contract.json`.
- `docs/change-logs/2026-08-15.md` (all 46 lines).
- `Theory/05d_relational_inference.tex:1225-1305` (hard BSC theorem + proof, in the committed file).
- `Theory/07b_agent_network_rg.tex:1-72` (`thm:rg-exact-coarse-vfe` + proof) and `:1878-1950`
  (`sec:rg-meta-attention`), in the committed file.

**Sampled:**
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation_scan.py` — read
  `_hazards()` and the token-classification block; the rest of the 640 lines was not read.
- `docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation-collision-report.json` —
  queried programmatically (status, counts, token vocabulary, per-token records, source coverage);
  the 5732 lines were not read line by line.
- `evidence/reviews/view-information-vfe.md`, `view-dynamics-scope.md` — headers and identity tables;
  `view-gauge-holonomy.md`, `view-probability-kernel.md` — grepped for Theory bindings and for the
  zero-defect statements. Full argument bodies not read.
- `2026-08-14/.../evidence/direct-derivation.md` — §5 (Theorem 5) only.
- `2026-08-14/.../evidence/counterexample-proofs.md` — §3.2 (determinant) only.
- `2026-08-14/.../evidence/recompute.py` and `recompute-output.json` — grepped/queried, not run.
- `.verification/ledger.json` — queried for dates and commit SHAs, not read.

**Not reached:**
- `2026-08-15` package: `evidence/counterexample-proofs.md` (222 lines, the five negative
  constructions), `evidence/adversarial-attacks.md` (the sixteen attacks),
  `evidence/independent-reconstruction.md`, `evidence/oracle-erasure.md`,
  `evidence/finite_nongaussian_witness.py` and its output, `release-assembly.json`,
  `release-provenance.json`, `approach-registry.json`, `adversarial-report.json`,
  `counterexample-register.md`, `construction-or-strongest-theorem.md`, `dependency-dag.json`.
- `2026-08-14` package: `evidence/adversarial-attacks.md`, `independent-reconstruction.md`,
  `oracle-erasure.md`, `prior-hard-operational-reduction-proof.md`, `counterexample-register.md`,
  `claim-ledger.json` (547 lines), `adversarial-report.json`, `approach-registry.json`.
- `docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md` (+394 lines on 8/15),
  `docs/superpowers/plans/2026-08-15-full-pointwise-meta-agent.md` (+423),
  `docs/superpowers/specs/2026-08-15-full-pointwise-meta-agent-design.md` (+451),
  `docs/superpowers/specs/2026-08-14-operational-intervention-extensions-design.md` (+135),
  `docs/verification/reviews/2026-08-15-full-pointwise-meta-agent-closure.md` (+58) — sampled only via
  grep for the `\Delta_A` fence.
- `solid_RG_theory.md` sections 2-8 and 10 (unchanged on 8/15 except for notation renames).
- The 15×15 contextual minor entries and the Bareiss pivot sequence in the 8/14 package.
- No LaTeX build was run, so I did not confirm that `main.tex` still compiles with the added
  `\Cref` targets; I confirmed only that every added label exists in `Theory/main.aux`.

## Method notes

- I treated no internal review, adversarial-report entry, oracle-erasure record, or ledger state as
  evidence. Where I cite them it is as *claims under audit*, and in the HIGH finding they are the
  object of the finding rather than its support.
- Every mathematical verdict marked S in the tables was reconstructed independently before being
  compared with the package text, except where the row says otherwise (C6).
- Mechanical checks actually executed: the released notation scanner at `HEAD` (PASS, exit 0);
  SHA-256 of eleven manuscript and package files; JSON extraction from the collision report, claim
  ledger, release, and recompute output; `git log -S` for the deleted fence; `git check-ignore` and a
  date scan of `.verification/ledger.json`.
