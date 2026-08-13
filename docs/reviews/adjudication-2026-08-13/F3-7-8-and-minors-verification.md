# F3-7-8-and-minors-verification

*Verbatim agent return, workflow wf_0b4620e2-7dc, 2026-08-13.*

## holds

true

## corrected_verdict

The adjudication SURVIVES. Its verdicts on all seven items are the ones I reach independently, its ~30 line citations are almost all exact at 4dee0db, and every numerical claim I re-derived from definitions reproduced its reported figures — in the balanced/causal/ALiBi retained fractions, the least-squares span fit, and the 30-term cumulant partial sums, digit-for-digit. Both repository scripts run and give the reported values (u1 CHECK 4 |diff| = 5.542e-13). Three corrections, none of which changes a verdict.

(1) SUBSTANTIVE ERROR, finding 3. The adjudication says worklog §4.3:863-867 states the peer-sector negative 'more strongly than the evidence supports' and 'needs the balanced-row scope restriction'. Line 863 already reads 'On a balanced stencil the label-marginalization residual is exactly minus the retained peer sector at O(h^2)'. The unrestricted headline belongs to panelA-T-RESID-derivation.md:43,:237, not to the worklog — the adjudication imported the derivation's claim into the worklog. Relatedly, its recommended edit 'mark statement (4) REFUTED-AS-STATED' in §4.3 is already done at worklog:858-859. The genuine §4.3 defect is narrower and different: it omits the biased-row half of the skeptic's result (retained fraction 0.9 for a causal two-left-neighbour row, 0.36 for pi=(0.8,0.2), 1 for single-source agents — all of which I reproduced to 4-6 digits) and calls the negative 'which both agree on' when the skeptic at :45-46 denies that balanced stencils are generic and holds that the deployed rows recover the sector at O(1). Recommended action (1) should be rewritten accordingly.

(2) LABELLING. The batch verdict should read PARTLY_UPHELD / UPHELD-WITH-NARROWINGS rather than a bare UPHELD: finding 3's evidentiary premise is refuted by material the reviewer could not see (its conclusion survives, strengthened), and finding 7's blanket 'conflicts with its governing SPEC' is judged by the adjudication itself to over-reach, given SPEC.md:20-25's two explicit carve-outs which I verified verbatim. Severity medium is honest for the batch (it matches the review's own 'Substantive medium' filing), even though rm-05 independently rates the finding-8 provenance defect HIGH — a fact the adjudication surfaces rather than suppresses.

(3) CITATION HYGIENE. Three loose cites: ':123' for the declared reference measure is a blank line (the measure is at :125 and :160); worklog ':652-653' for '(now landed in this repo)' is actually 650-651; 'the 17 panel returns' should be 16 returns plus a README. The 05c ranges drift by about one line. One evidentiary method is weaker than presented — 'grep -rln PIFB Theory/*.tex returns zero hits' is a poor SPEC-compliance test, since Theory/PIFB2.tex is itself tracked in that directory and contains zero literal 'PIFB' tokens — but I ran a wider semantic sweep ('reference implementation', 'deployed action', 'Participatory', 'it-from-bit') over all 20 chapters and the three appendices and also got zero hits, so the conclusion that SPEC:17 is currently honored stands.

Everything else I attacked held: the §4b supersession reasoning is correctly two-part (stale evidence, strengthened conclusion) and does not launder contested panel output; the git-diff scope claim is right, including the §3d.7 hunk that looks at first like a counterexample but is only git's nearest-heading context; and the finding-8 ledger forensics are exact against the parsed JSON.

## attacks

### 1

{
  "attack": "RECOMPUTATION AUDIT \u2014 the adjudication reports a long list of numbers (eps identity to 1.33e-15; retained fractions 0.891583/0.897880/0.899469/0.899867 and 0.359432/.../0.359984; lstsq coefficients (-0.0684500,-0.0684500,+0.13517349); cumulant partial sums -0.433781/-0.863135/-2.00205/-53151.5; CHECK 4 |diff|=5.54e-13). Attack: these were lifted from the panel artifacts (which contain their own numerics) and dressed as independent work.",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "I rewrote every one of these from the definitions in a fresh scratch script (numpy + mpmath at 50-60 dps) and reproduced them, in several cases to every digit reported. (A) max |eps_a(x) + D_KL(pi||pi_post(.|x))| = 1.11e-15 over 20000 draws, 0 sign violations. (B) generalized-Hoelder Z<=1: 0 violations in 20000 discrete trials. (C) balanced pi=(1/2,1/2), m=(+1,-1): D_KL(q||ubar)/(h^4/4) = 0.83737, 0.950738, 0.986942, 0.996684, 0.999168 at h=0.4..0.025 \u2014 identical to the adjudication's 0.837370, 0.950738, 0.986942, 0.996684, 0.999168. (D1) causal m=(-1,-2): retained 0.891583, 0.897880, 0.899469, 0.899867 -> 0.9 \u2014 digit-for-digit identical. (D2) pi=(0.8,0.2): 0.359432, 0.359774, 0.359938, 0.359984 -> 0.36 = (2w-1)^2 \u2014 digit-for-digit identical. (E) lstsq of -kappa_2/2 onto span{E_+,E_-,1} at h=0.37 over 801 grid points: (-0.06845, -0.06845, 0.13517349) vs exact (-h^2/2, -h^2/2, h^2(h^2+log2pi)/2); max residual 3.6e-15; and eps_exact = -log cosh(hx) to 1.78e-15 (the adjudication's own figure). The analytic identity behind it checks by hand: E_+ + E_- = x^2 + h^2 + log2pi and kappa_2 = h^2 x^2, so -kappa_2/2 = -(h^2/2)(E_++E_-) + (h^2/2)(h^2+log2pi) exactly. (F) cumulant series, J=2, pi=(1/2,1/2), E=(0,D), 30 mpmath terms: eps_partial = -0.4337809, -0.863135, -2.002047, -53151.46 against exact -0.4337808, -0.8554402, -1.086603, -1.813568 \u2014 again digit-for-digit the adjudication's numbers. I also ran both repository scripts: kl_expansion_check.py passes all assertions (1/2 g^F h^2; 1/3 vs 1/6 T_skew h^3; symmetric-stencil h^3 cancellation), and u1_two_path_holonomy_witness.py CHECK 4 gives LHS=RHS=2.4495355549, |LHS-RHS|=5.542e-13 \u2014 exactly as reported. The only number I could not reproduce is the cosmetic 'residual of eps_exact against the span = 0.043' (I get 0.1224 on [-6,6] with 801 points; the skeptic reports 0.223); this is grid-dependent and load-bearing only for the sign of the statement (nonzero), which holds. The recomputation claim is genuine."
}

### 2

{
  "attack": "CONFUSION OF THE WORKLOG'S CLAIM WITH THE DERIVATION'S CLAIM \u2014 the adjudication writes 'the negative in worklog \u00a74.3:863-867 is stated more strongly than the evidence supports and needs the balanced-row scope restriction the skeptic demands at :45-46', and recommends editing \u00a74.3 to 'mark statement (4) REFUTED-AS-STATED and the \u00a76 headline SCOPE-RESTRICTED-TO-BALANCED-ROWS'.",
  "outcome": "REPAIRABLE",
  "reasoning": "This lands. Worklog line 863 begins verbatim: '**The consequential negative, which both agree on.** On a balanced stencil the label-marginalization residual is *exactly minus* the retained peer sector at O(h^2), leaving O(h^4)'. The balanced-stencil restriction is already there; it is the DERIVATION (panelA-T-RESID-derivation.md:43, :237) that states the unrestricted headline 'the Fisher-covariant Dirichlet peer sector is not generated'. The adjudication attributes the derivation's over-reach to the worklog. Worse for the recommended action: worklog:858-859 already reads '(3) Statement (4) is false as written (two independent counterexamples)', so one of the seven prescribed edits is already in the file the adjudication quoted three lines earlier. The residual defect is real but different from the one stated: \u00a74.3 omits the biased-row counterweight entirely (retained fraction 0.9 on a causal two-left-neighbour row, 0.36 on an ALiBi-like row, 1 for single-source agents \u2014 all of which I reproduced), and it calls the negative one 'which both agree on' when the skeptic at :45-46 explicitly denies that balanced stencils are 'the generic lattice case' and holds that the deployed pi_ij (PIFB2.tex:709 causal masking / ALiBi / learned position bias) recover the sector at O(1). So the criticism should be re-aimed at an omission, not an overstatement, and the recommended edit for \u00a74.3 should be halved."
}

### 3

{
  "attack": "'SUPERSEDED BY \u00a74b' REASONING \u2014 the adjudication may be treating a different claim in 4b as answering finding 3, and treating contested panel output as settled fact.",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "The mapping is exact and the epistemic handling is careful. The reviewer's finding 3 names three missing objects: explicit C_h, pushed-forward posterior, computed residual. panelA-T-RESID-derivation.md supplies C_h^(1) at :124, C_h^(2) at :141, C_h^(3)=id at :159 (I read all three), the pushforward as Lemma 0 at :93-95, the closed-form residual eps_a(x)=log[GM/AM] at :170, and the first corpus definition of c_h at :180 \u2014 all at the cited lines. The adjudication does NOT then treat this as vindication: it foregrounds the skeptic's survives:false / confidence:high (verified at skeptic :5-11) and the PROVED->PARTIAL downgrade at :49, and independently re-derives three of the skeptic's attacks. It then concludes the reviewer's CONCLUSION holds a fortiori while the reviewer's EVIDENCE is stale \u2014 which is the correct two-part structure, not a laundering of contested material. One small slip: the reference measure is declared at :125 (nu_a = p_a (x) r_a) and :160 (the level-3 nu_a); line :123 cited alongside is blank."
}

### 4

{
  "attack": "LOCUS AUDIT \u2014 did the adjudication read the cited loci, or paraphrase? Line numbers drift between revisions and this batch cites ~30 of them.",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "I checked essentially every citation against the file at 4dee0db and the hit rate is unusually high. Exact: Theory/SPEC.md:17 (sole 'PIFB2' occurrence, confirmed by grep) and the two exceptions at :20-25 (quoted verbatim and correctly); worklog:24 'For a finite agent-site set A'; :143 the absolute Documents/ChatGPT path; :173 'written into Theory/'; :179-184 the fragmentation table; :379-381 the 05c:1368 standing warning; :397-405 the \u00a73d.1 transport definition; :484-487 the exp(-L/xi) item (verbatim); :542-545 CHECK 2; :558-559 'Obligation 1 of \u00a73d.7 is discharged'; :571-572 'Obligation 2 ... obligations 3 and 4 remain'; :576-578 the CONJECTURE status header; :681 'Discharge \u00a73d.7 obligations 3-4'; :684 next-step #5; :688-689 next-step #6; :863 the consequential negative; :906-907 'neither is to be exported to Theory/'; :1102 'Nothing here is cleared for Theory/ yet'; :1128-1131 \u00a76 write policy (which indeed never names Theory/ or SPEC.md). overview.md:95, :105, :106, :115, :136, :222-232, :229 all exact. rm-05:69 (row A-2, HIGH provenance) and :138-140 exact. final-report.md:14 exact and verbatim. construction-or-strongest-theorem.md:4, release.json:9, claim-ledger.json:139 all exact for the inherited 'finite lattice' wording. Theory/main.tex has exactly 23 \\input lines and PIFB2.tex is not among them (confirmed). Drift found only at ':652-653' for '(now landed in this repo)' (actually 650-651), the blank ':123', and the 05c equation/proposition ranges (off by ~1; prop:pb-curve-taxonomy is at 621, eq:pb-section-curve-length label at 630). None is substantive."
}

### 5

{
  "attack": "THE SPEC-COMPLIANCE EVIDENCE IS A TOKEN GREP \u2014 'grep -rln PIFB Theory/*.tex returns zero hits' cannot establish that SPEC:17 is honored, because a crosswalk can be written without the acronym, and Theory/PIFB2.tex is itself one of the scanned files.",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "The method is weak but the conclusion survives an independent, wider test. Theory/PIFB2.tex exists, is git-tracked, is 3956 lines, and \u2014 surprisingly \u2014 contains zero literal 'PIFB' strings, so the adjudication's grep is even less discriminating than it looks. But I ran a semantic sweep over the 20 chapters plus the three appendices for 'reference implementation', 'deployed action', 'Participatory', 'it-from-bit', 'it from bit' and got ZERO hits. The adjudication was also honest that PIFB2.tex is 'physically present in the directory' and rested the load on non-inclusion in main.tex, which I confirmed. Its finding-7 substantive conclusion \u2014 SPEC:17 currently honored; the real hole is that worklog \u00a76's write policy never names Theory/ and worklog:173's gate is a reconciliation gate rather than a SPEC gate \u2014 stands."
}

### 6

{
  "attack": "SCOPE OF THE 'byte-identical' CLAIM \u2014 the adjudication asserts \u00a73b, \u00a73b.3, \u00a73c, \u00a73d.5, \u00a73d.7 and \u00a76 are byte-identical between caa4a15 and 4dee0db, and that overview.md was untouched. The second diff hunk carries the context line 'connections exists. Obligations, in order:', which sits inside \u00a73d.7.",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "I chased this because the hunk header @@ -584,6 +594,10 @@ quotes \u00a73d.7's obligation list as its context. Reading the hunk body, the four added lines are the '**RESOLVED 2026-08-13**' banner inserted immediately after the '## 4. RESULTS \u2014 PENDING / RESUME HERE' heading; the \u00a73d.7 lines are only git's nearest-heading context. \u00a73d.7 is genuinely unchanged. The full diff is exactly three hunks (\u00a72 CLOSED banner, \u00a74 RESOLVED banner, next-steps + \u00a74b replacing the old '_pending_' placeholders), plus 17 new files in docs/audits/panels-2026-08-12/, and `git diff caa4a15 4dee0db -- overview.md` is empty. I separately confirmed \u00a75 and \u00a76 survive byte-identical in the tail. The scope claim holds. (Trivial miscount: the adjudication once says 'the 17 panel returns'; the directory holds 16 returns plus a README.)"
}

### 7

{
  "attack": "MINOR (ii) OVER-READS \u2014 the adjudication upgrades the reviewer's point from 'the weight is not derived' to 'the weight is identically 1 for every curve', which requires identifying the un-defined L(gamma) of worklog:484-487 with the vertical Fisher length of the omega-horizontal lift.",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "The chain is verifiable and the adjudication itself flags the alternative reading. worklog:485 cites '05c:589, vertical Fisher length' explicitly; Theory/05c_pullback_geometry.tex prop:pb-curve-taxonomy (heading at :621, \\status{ESTABLISHED}) states verbatim 'If Gamma is omega-horizontal, then L^omega(Gamma)=0'; and worklog:397-405 defines the \u00a73d.1 coupling as D_KL(q_i(c_i) || (P_gamma)_# q_j(c_j)), where P_gamma is parallel transport, i.e. the horizontal lift. So L^omega = 0 for the transported curve is a definitional consequence, no numerics needed. The adjudication does not hide the escape route \u2014 it names the section-curve length L^omega(s o gamma) at eq:pb-section-curve-length as the repair and notes xi stays exogenous. Its two corroborations also check out verbatim: worklog:379-381 already carries the 05c:1368 warning against this exact use, and worklog:486-487 cites rm-03 \u00a70's 'absorbable by free parameters' judgement while claiming to escape it."
}

### 8

{
  "attack": "BATCH VERDICT 'UPHELD' AND SEVERITY 'medium' ARE FLATTENED / DEFLATED. Internally the adjudication records finding 7 as PARTLY_UPHELD with 'the reviewer's blanket conflicts-with-SPEC over-reaches', finding 3 with its evidentiary premise refuted, and minor (iii) as narrowed \u2014 yet the top-line label is a bare UPHELD. And it cites rm-05's HIGH severity for finding 8 while assigning the batch medium.",
  "outcome": "WEAKENS_SCOPE",
  "reasoning": "Partly lands, on labelling rather than substance. A single 'UPHELD' is generous for a batch in which one finding's blanket claim is judged to over-reach and another's stated evidence is judged stale; PARTLY_UPHELD or UPHELD_WITH_NARROWINGS is the honest one-word summary. Mitigation: the per-finding verdicts are all stated explicitly in the first sentence of each evidence bullet, so nothing is concealed. On severity: 'medium' matches the reviewer's own filing (findings 3, 7, 8 sit under 'Substantive medium findings') and the batch contains four minors, so medium is defensible even though rm-05 independently rates the finding-8 defect HIGH (provenance) \u2014 which the adjudication itself surfaces rather than suppresses."
}

### 9

{
  "attack": "MINOR (iii) MANUFACTURES A RESIDUAL CONTRADICTION \u2014 the adjudication says CHECK 2 'discharges [obligation 3] for abelian U(1)' while '\u00a73d.8 two lines later still lists obligation 3 as remaining'.",
  "outcome": "WEAKENS_SCOPE",
  "reasoning": "Mild over-reading, and the distance is 26 lines, not two. \u00a73d.8:568-570 explicitly scopes the gap \u2014 'nor anything about non-abelian G where the statistic must be a conjugacy-class invariant rather than an element' \u2014 immediately before saying obligations 3 and 4 remain, and the revised next-step at :681 says 'gauge-invariance of the statistic under non-abelian G'. So obligation 3 remaining is a scope statement, not a contradiction. The adjudication nonetheless lands in the right place, concluding 'the live to-do list is consistent; only the \u00a73d.7 status header and the section ordering are unrepaired' \u2014 which I confirmed (\u00a73d.8 begins at :508, \u00a73d.7 at :574, and :576-578 still reads 'Status: CONJECTURE ... not that a separating pair of connections exists' directly above a witness whose four checks I ran and which all pass)."
}

### 10

{
  "attack": "FINDING 8 \u2014 the adjudication's 'UPHELD (fully) but MOOT AS NOVELTY' rests on ledger contents it may have paraphrased rather than parsed.",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "I parsed all four claim-ledger.json files myself. docs/derivations/2026-08-12-pifb2-elbo-program-decision/claim-ledger.json has assumptions: 0 entries, evidence: 0 entries, and exactly one claim, id 'target', state INCONCLUSIVE, evidence_ids [] \u2014 precisely as described. docs/derivations/2026-08-12-elbo-to-effective-section-action/claim-ledger.json carries id 'live-peer-fixed-joint', state REFUTED, evidence_ids ['ev-counterexamples'] \u2014 the redirection is correct. final-report.md:14 is verbatim as quoted, with no path, ID, revision or hash. rm-05-provenance-gates.md:69 is row A-2 at severity **HIGH (provenance)**, and :138-140 contains the completed grep, the identification of Research/manuscripts/verified-ledger.md as the GL(K) manuscript ledger, the 'roadmap line 174 verified -> final-report.md:14 -> nothing resolvable' chain, and the exact prescribed repair. The 'this is a rediscovery, and rm-05's version is stronger' observation is correct and is the one place the adjudication improves on the reviewer rather than merely grading them."
}

