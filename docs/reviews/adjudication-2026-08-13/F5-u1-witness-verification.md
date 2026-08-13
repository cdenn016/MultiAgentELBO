# F5-u1-witness-verification

*Verbatim agent return, workflow wf_0b4620e2-7dc, 2026-08-13.*

## holds

true

## corrected_verdict

The adjudication's core verdict — UPHELD, severity medium, NOT superseded by section 4b — is correct and survives adversarial attack. I independently reproduced every load-bearing number it reports, and in two places I strengthened its result rather than broke it. What does not survive is a set of secondary framings inside its `reviewer_missed` and `SCOPE OVERCLAIM` items, which are unfair to the reviewer and mis-cite one worklog locus.

WHAT I VERIFIED INDEPENDENTLY (all recomputed, not read):
- Statistic identity. docs/verification/u1_two_path_holonomy_witness.py:149-154 returns arccos(cos Theta) exactly. Over ten values of Theta including 5pi/4, 3pi/2 and two irrational values, max |separating_statistic - arccos(cos Theta)| = 4.44e-16, the same figure it reports; at 5pi/4 I get 2.3561944902, its exact value. Since m1 = R(gauge_i + a_direct)MU_J, m2 = R(gauge_i + a_around)MU_J and a_direct - a_around = Theta exactly (transport_angles at :81-85), it is arccos(cos Theta) identically. The docstring at :151, the print at :217-218 and the conclusion at :314-315 are false as implemented. CONFIRMED.
- Script run. All four checks PASS and the printed table reproduces worklog:526-534 digit for digit (0.3190849227 at pi/2 AND at 3pi/2; 8.02e-17 at 2pi; ELBO |LHS-RHS| = 5.5e-13). CONFIRMED.
- Record-law gauge equivalence. orbit_distance(pi/2, 3pi/2) at n_gauge=360 = 1.0557e-16, matching its 1.056e-16 to four figures. Component mean angles {22.5, 292.5} deg and {67.5, 157.5} deg as reported. I then removed the quadrature entirely: rotating the Theta=pi/2 components by exactly g = 3pi/4 and swapping labels reproduces the Theta=3pi/2 components to |dmu| <= 1.7e-16, |dSigma| <= 1.1e-16. CONFIRMED, by a stronger route than it used.
- I EXTENDED the point it only spot-checked. It verified Theta <-> -Theta equivalence at one pair. I proved it for all Theta: p(.|Theta) and p(.|2pi-Theta) are exactly gauge-equivalent under g* = pi/2 + Theta/2 plus a label swap (analytic component mismatch <= 1.0e-15 at Theta = pi/8, 1.1, 2.0, 2.9, pi/2; bounded TV minimisation finds g* to six decimals with residual 2e-9 to 1.4e-8, pure quadrature floor). Its general claim is not an extrapolation — it is true, and I have the general proof it did not supply. Note the script's own default n_gauge=180 (2-degree grid) MISSES 135 deg and returns 9.8e-3, so the finer gauge grid was necessary, not cherry-picked.
- Root cause. My grid gives (0.5,0.5) -> 1.07e-16; (0.7,0.3) -> 0.23496 (its 2.3496e-01, exact match); (0.9,0.1) -> 0.0791 (its 7.84e-02 — 1 percent apart, explained by grid 301 vs 421; same conclusion). CONFIRMED.
- Signed statistic. arctan2(m1[0]m2[1]-m1[1]m2[0], m1@m2) returns -1.5707963268 at pi/2 and +1.5707963268 at 3pi/2, gauge drift 8.882e-16 — its 8.9e-16. CONFIRMED.
- Mathematics. Lambda^2 T*M = 0 on any 1-manifold so F = dA vanishes for EVERY connection on S^1; H^2(S^1;Z) = 0 and pi_0(U(1)) = 0 give triviality; Hom(Z,U(1)) = U(1) is a continuum. Its Ambrose-Singer statement carries the correct "restricted holonomy" qualifier. The verdicts on worklog:428 (only-if half false), :479, :480-483 are right.
- Loci. The reviewer's citations are against caa4a15; the diff to 4dee0db inserts 10 lines near :105 and 4 near :594, so 410-418 / 460-476 / 498-568 map to 420-428 / 470-486 / 508-578 — exactly where :428, :479, :480-483, :526-534, :544-545 now sit. It found the right loci; it just never explains the drift.
- Supersession. Zero hits for "holonom" in worklog 693-1112; the only curvature/topology hits are :790 (Gamma-convergence interpolation topology), :825 (T-CURV), :1094 (synthesis, T-CURV). "holonom" appears in exactly 6 of 17 panel files and never about the witness. Section 4b is genuinely silent. The corroboration via worklog:810-811 (plaquette expansion) is real and does require a 2-d base. CONFIRMED.
- Survival claim. Theory/appendix_claim_ledger.tex:243-253 requests exactly the tuple it says is exhibited, and Theta=0 vs Theta=pi/2 supplies it. CONFIRMED.

CORRECTIONS I WOULD APPLY (none change the verdict):
1. Drop "This is stronger than what the reviewer wrote" and the "FIX IS MISPRESCRIBED / right for a partly wrong reason" framing. review:73 says verbatim: "a direct countercheck found the pi/2 and 3pi/2 RECORD-LAW ORBITS gauge-equivalent to numerical precision." The reviewer already had the record-law-level result. The genuine addition is the root cause (PI_ROW at script:78) and the gauge angle 3pi/4 — a sharpening, not a correction.
2. Fix the SCOPE OVERCLAIM citation. worklog:466-468 does not say "Defeated"; it says the ledger entry "reopens as genuinely open" — the careful phrasing being demanded. Only overview.md:151 says "Defeated". And worklog:461-464 does argue separately against F4, which the adjudication never mentions. The residual valid charge is narrower: overview.md:151 states the three-clause negative and stamps it "Defeated" with no note that only the holonomy clause has a witness and that F vanishes identically on the witness's base.
3. Fix the sign slip: the evidence string writes arctan2(m2 x m1, m1.m2), which equals +Theta and would give +pi/2 at Theta=pi/2, contradicting its own -1.570796; the recommended_action formula cross(m1,m2) is the one that reproduces the numbers.
4. Missed supporting evidence: docs/audits/panels-2026-08-12/panelA-ground-03-theory-corpus-sweep.md:262 corroborates the reviewer from inside the corpus — 11_obstructions.tex:422 and 12_philosophy.tex:111,326 already disclaim "evidence of base curvature or bundle topology", and there is NO curvature term in any free energy in Theory/.
5. Slight mis-targeting of :479/:480-483: they sit in section 3d.5, framed as "predicted phenomenology ... to be tested rather than results" and not S^1-scoped, so "false on S^1" aims at the wrong base. The substance holds on any base and its own suggested rewrites say so, so only the justification needs repair.

Severity "medium" is honest: the existence witness, checks 3 and 4, and the ledger tuple all survive and I reproduced them; the defect is four prose sentences (worklog:428, :479, :483, :544-545), one overview line (overview.md:182), three script strings, and one design constant (script:78).

## attacks

### 1

{
  "attack": "Did it actually recompute the statistic identity, or paraphrase the reviewer? Redo it independently.",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "Recomputed over ten Theta values including two it did not use. max |separating_statistic - arccos(cos Theta)| = 4.44e-16, identical to its reported figure; at 5pi/4 I get 2.3561944902, its exact value. The code at u1_two_path_holonomy_witness.py:149-154 computes arccos of the normalised dot product of the two component means, and because m1 = R(gauge_i + a_direct)MU_J, m2 = R(gauge_i + a_around)MU_J with a_direct - a_around = Theta exactly (transport_angles :81-85), it is arccos(cos Theta) identically. Its code quotation is accurate, not a paraphrase."
}

### 2

{
  "attack": "Is orbit_distance(pi/2, 3pi/2) = 1.056e-16 real, or a quadrature artefact / cherry-picked gauge grid?",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "Real, and I strengthened it. n_gauge=360 gives 1.0557e-16 (matching 1.056e-16); n_gauge=180 \u2014 the SCRIPT's own default \u2014 gives 9.8e-3 because the 2-degree grid misses 135 deg, so the finer grid was necessary rather than cherry-picked. I then removed quadrature entirely: rotating the Theta=pi/2 components by exactly 3pi/4 and swapping labels reproduces the Theta=3pi/2 components to |dmu| <= 1.7e-16, |dSigma| <= 1.1e-16. The equivalence is exact and analytic."
}

### 3

{
  "attack": "It generalises from ONE pair (pi/2, 3pi/2) to 'no observable whatsoever can separate Theta from -Theta on this design'. Does the verdict outrun the evidence?",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "I expected this to land and it does not \u2014 the general statement is true and I proved it. Components sit at Theta/4 and -3Theta/4; for 2pi-Theta at pi/2-Theta/4 and pi/2+3Theta/4; the common rotation g* = pi/2 + Theta/2 plus a label swap maps one set onto the other exactly. Verified analytically at Theta = pi/8, 1.1, 2.0, 2.9, pi/2 (mismatch <= 1.0e-15) and by bounded TV minimisation, which finds g* at the predicted value to six decimals with residual 2e-9 to 1.4e-8. With equal weights the mixture is an unordered pair whose complete gauge-orbit invariant is cos(a1-a2) = cos Theta, so arccos(cos Theta) really is the complete invariant and the statistic really is optimal for this design."
}

### 4

{
  "attack": "Is 'NOT superseded by 4b' correct, or did it grep the wrong range / miss a 4b claim that answers the finding?",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "Verified. 4b runs 693-1112 (header at :693, section 5 at :1113); zero hits for 'holonom'; the only curvature/topology hits are :790 (Gamma-convergence interpolation topology), :825 (T-CURV) and :1094 (synthesis, T-CURV). 4b's targets are T-GRAD/T-CURV/T-RESID/T-COEF/T-SIMUL/Panel B plus the hand synthesis at 1069-1112, none of which is section 3d. 'holonom' appears in exactly 6 of 17 panel files, and in ground-01 (:21, :361) it concerns PIFB2's Omega_ij being a flat Cech coboundary \u2014 unrelated, exactly as claimed. It did not treat a different 4b claim as answering the finding; it correctly identified worklog:810-811 as merely corroborating from the other side."
}

### 5

{
  "attack": "Did it confuse the reviewer's claim with its own, i.e. claim novelty the reviewer already had?",
  "outcome": "WEAKENS_SCOPE",
  "reasoning": "This lands. Its evidence item (b) says the record-law equivalence 'is stronger than what the reviewer wrote', and reviewer_missed (1) charges the reviewer with headlining a statistic defect and being 'right for a partly wrong reason'. But review:73 states verbatim: 'a direct countercheck found the pi/2 and 3pi/2 RECORD-LAW ORBITS gauge-equivalent to numerical precision.' The reviewer had the record-law-level result, so 'add an oriented/asymmetric observable' most plausibly includes an asymmetric design element. The genuine addition is the root cause (PI_ROW at script:78) and the exact gauge angle. Verdict unaffected; the reviewer_missed section is overstated in the adjudicator's favour."
}

### 6

{
  "attack": "Is the SCOPE OVERCLAIM charge against the worklog accurately cited?",
  "outcome": "WEAKENS_SCOPE",
  "reasoning": "Partly lands. It writes that 'worklog:466-468 and overview.md:151 record B4 as simply Defeated ... unqualified as to which clause.' worklog:466-468 says no such thing \u2014 it says the ledger entry 'reopens as genuinely open', which is the careful phrasing being demanded. Only overview.md:151 says 'Defeated'. Worse, it never mentions worklog:461-464, where the worklog DOES argue separately against F4 (P_gamma depends on A off the design, so 'trivializable over a finite set' no longer suffices), making the worklog look more careless than it is. The residual valid charge stands but is narrower: overview.md:151 states the full three-clause negative and stamps it 'Defeated' with no note that only the holonomy clause has a witness, and that F vanishes for every connection on the witness's base."
}

### 7

{
  "attack": "Are the differential-geometry claims (F = 0, trivial bundle, flat moduli a continuum) right, or asserted as background?",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "All correct, and it labelled the bundle classification honestly as standard-not-recomputed. Lambda^2 T*M = 0 on a 1-manifold so F = dA vanishes for every connection on S^1 \u2014 the sharper point the reviewer did not make, correctly added. H^2(S^1;Z) = 0 and pi_0(U(1)) = 0 both give triviality; Hom(pi_1(S^1),U(1)) = U(1) is a continuum, so Theta is a modulus not a discrete invariant. Its Ambrose-Singer statement carries the correct 'restricted holonomy' qualifier rather than the sloppy version. The three verdicts on worklog:428, :479, :483 are correct."
}

### 8

{
  "attack": "Does the recommended script fix actually work, and is the signed statistic stated consistently?",
  "outcome": "REPAIRABLE",
  "reasoning": "The fix works \u2014 PI_ROW=(0.7,0.3) gives orbit distance 0.235 > 0 on my grid, and the caveat that the signed statistic is not a function of the record law under equal weights is correct and important. But the formula is stated inconsistently: the evidence string writes arctan2(m2 x m1, m1.m2), which equals +Theta and so gives +pi/2 at Theta=pi/2, contradicting its own reported -1.570796; the recommended_action formula cross(m1,m2) is the one that reproduces the reported numbers (I get -1.5707963268 and +1.5707963268, drift 8.882e-16). A sign-convention slip in the prose, not in the result."
}

### 9

{
  "attack": "Are :479 and :480-483 correctly targeted, given they sit in a section that is not S^1-scoped?",
  "outcome": "REPAIRABLE",
  "reasoning": "Section 3d.5 (worklog:470-491) is explicitly 'Predicted phenomenology, stated as consequences to be tested rather than results' and precedes the S^1 witness at 3d.8, so calling :479 'false on S^1' aims at a base the sentence does not commit to. The substance holds on any base \u2014 the two-path residual is the loop's monodromy and curvature is only its infinitesimal/plaquette version (as worklog:810-811 itself shows), and 'frustration becomes a bundle invariant' is wrong generally since the fixed-point criterion is a property of the connection's holonomy, not of the bundle class. Its own suggested rewrites say precisely this, so only the justification needs repair."
}

### 10

{
  "attack": "Is severity 'medium' inflated to make a cleaner story?",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "Honest. It explicitly preserves the existence result, and I confirmed what it preserves: check 3 (coboundary control, TV = 0 to machine zero at every Theta tested), check 4 (|LHS-RHS| = 5.5e-13), and the Theta=0 vs Theta=pi/2 separation at orbit distance 0.3190849227, which does satisfy the tuple requested at Theory/appendix_claim_ledger.tex:243-253. The defect is four prose sentences, one overview line, three script strings and one design constant. The worklog's own scope paragraph at :568-572 already hedges hard, which would argue for lower rather than higher severity; medium is defensible because worklog:544-545 and overview.md:182 are flatly false statements inside a results record."
}

### 11

{
  "attack": "Did it miss corroborating material in the new panel returns that changes the picture?",
  "outcome": "WEAKENS_SCOPE",
  "reasoning": "It missed one item, which strengthens its verdict but weakens its claim to have swept the new material. docs/audits/panels-2026-08-12/panelA-ground-03-theory-corpus-sweep.md:262 reports that every occurrence of 'curvature' in Theory/ is a disclaimer \u2014 including 11_obstructions.tex:422 and 12_philosophy.tex:111,326 saying results are 'not claimed to be evidence of base curvature or bundle topology' \u2014 and that there is NO curvature term in any free energy in Theory/. That is the reviewer's exact distinction already enforced in the ambient corpus and belongs in the evidence."
}

### 12

{
  "attack": "Did it check the cited loci, given the reviewer's line numbers were written against caa4a15 and the file has since shifted?",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "It found the right loci. The caa4a15 -> 4dee0db diff inserts 10 lines near :105 and 4 near :594, so the reviewer's 410-418 / 460-476 / 498-568 map to 420-428 / 470-486 / 508-578 in the current file \u2014 exactly where :428, :479, :480-483, :526-534 and :544-545 now sit. Every line it quoted I read and confirmed verbatim, including script strings at :151, :217-218, :314-315 and overview.md:151, :182. Its only omission is that it never explains the drift, so a reader cannot tell it checked rather than guessed."
}

