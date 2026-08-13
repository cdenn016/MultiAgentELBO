# F1-likelihood-bridge-verification

*Verbatim agent return, workflow wf_0b4620e2-7dc, 2026-08-13.*

## holds

true

## corrected_verdict

UPHELD — same verdict, same severity band, with three corrections to the record. (1) STATUS should read CONFIRMED, ALREADY INTERNALLY REGISTERED, UNFENCED IN THE PUBLIC OVERVIEW — not 'confirmed and unnoticed'. The programme's own docs/research-plans/2026-08-12-pifb2-continuum-roadmap.md:104, present at the reviewed revision caa4a15, already states the defect in the adjudication's own 'stronger' form ('An expectation under a belief law on k cannot contain an unintegrated random model variable m') and prescribes the choice; docs/audits/roadmap-review-2026-08-12/rm-03-action-class.md:363-365 confirms it as 'a live bug in the parent manuscript ... should be carried into WP0 as a correction'; docs/audits/panels-2026-08-12/panelA-ground-01-pifb2-deployed-action.md:369 (gotcha #6, NOT extract #6) and panelA-T-SIMUL-derivation.md:251/:302/:333 restate it post-caa4a15. Four internal registers plus the external referee, not two — so the adjudication's 'STRONGER THAN THE REVIEWER NOTICED' well-posedness argument is not its own discovery. (2) NOT SUPERSEDED BY SECTION 4b is CORRECT and survives a broader sweep than the adjudication ran: worklog:1048's 'typing question (V-TYPE)' is Panel B's recognition-vs-generative typing of the induced-volume action, a different object; 4b's only contact with the observation channel is worklog:953, which silently adopts the joint typing; worklog 4.5 omits T-SIMUL's own obstruction #8. Add one under-reported corroboration: worklog:925-926 newly records the skeptic's insistence that the theorem's scalar is 'not PIFB2's actual functional', supporting the reviewer's headline by a different route (tau, unit coefficients, chi-free). (3) SEVERITY high is defensible but should be stated as claim-hygiene on a registered defect: the live, unrepaired locus is exactly overview.md:124-125 with its fence list at :128-133 omitting the observation typing, mirrored in the worklog theorem block at :22-53. Every numerical claim reproduces independently (gap = log2 - (1/2)log3 = 0.1438410362; gap(w) = log(3^{w-1}(3-2w)) giving 0.0923315154 / 0.1308120359; joint - predictive = E_q[D_KL(s||s^{(o,k)})] with symbolic residual 0; Gaussian gap d^2 v/(2(v+1)) + (v-log(1+v))/2 = 0.1534264097 at d=0,v=1 and unbounded; KL chain rule to 1.8e-15; kl_expansion_check.py clean). Two internal defects to strike from the adjudication's evidence without changing the verdict: the invalid inference that PIFB2.tex:2715's fixed Lambda_{o_i} rules out a marginal reading, and the misattribution of 'no cross-bundle morphism' to PIFB2.tex:748 when it is at :459. Recommended actions (A) and (B) remain right and should additionally cite roadmap:104 as the existing register and rm-03:365 as the standing WP0 correction rather than presenting the repair as new.

## attacks

### 1

{
  "attack": "Did it actually check the cited loci, or accept paraphrases? Re-derive every file:line it gives.",
  "outcome": "REPAIRABLE",
  "reasoning": "The load-bearing quotations are verbatim and correctly located. worklog:34 does carry `-\\mathbb E_{\\zeta_a}\\log\\ell_a(o_a\\mid K_a,M_a)` and :41 the `= F_PIFB2,h^lag,1 + sum_a I_{zeta_a}` display; exact-elbo-proof.md carries the boxed identity followed verbatim by 'Define (F_{PIFB2,h}^{lag,1}) as the same display with the mutual-information term removed'; PIFB2.tex:689 and :669 are exactly as quoted; :684's argument list is exactly {q_i},{p_i},{s_i},{r_i},{phi_i},{beta_ij},{gamma_ij} with no m_i; the m_i-unbound form recurs at :750. Three locating errors, none substantive: (a) 'the canonical functional contains no cross-bundle morphism coupling the model and belief channels' is at PIFB2.tex:459, NOT :748 as cited (:748 is inside eq:free_energy_adaptive); (b) the q_i/s_i typing sentence is at :176, not :170-172 (which is the Fisher-metric coordinate formula); (c) the ground-01 finding is gotcha #6 at :369, not 'extract #6' \u2014 extract #6 at :74 is the transport-operator definition. Every quoted string exists verbatim, so the finding is mis-shelved, not fabricated. Also missed a fourth recurrence of the free-m_i form at PIFB2.tex:918."
}

### 2

{
  "attack": "Did it recompute the numerics, or assert them? Redo all six computations independently.",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "I reran everything from scratch (sympy 1.14 / numpy 2.4.4) and every number reproduces. (1) Two-point uniform model: joint = 2log2 - (1/2)log3 = 0.8369882168, predictive = log2 = 0.6931471806, simplify(gap - (log(2)-log(3)/2)) == 0, numeric 0.1438410362 \u2014 matches reviewer and adjudication. (2) Weight sensitivity: I derived gap(w) = (w-1)log3 + log(3-2w) by hand; sympy confirms simplify(G - log(3**(w-1)*(3-2w))) == 0; values 0.0923315154 / 0.1438410362 / 0.1308120359 at w = 1/4, 1/2, 3/4, digit-for-digit identical. (3) joint - predictive = E_q[KL(s || s^{(o,k)})] on a general symbolic 2x3 grid with s on the simplex: residual exactly 0. (4) Gaussian instance: sympy gives joint = d^2/2 + v/2 + (1/2)log2pi and simplify(gap - (d^2 v/(2(v+1)) + (v-log(1+v))/2)) == 0; 0.1534264097 = (1-log2)/2 at d->0, v=1; diverges in v and d. (5) KL(zeta||p(x)r) = KL(q||p)+KL(s||r)+I(K;M) over 20k random 3x4 instances: max residual 1.78e-15. (6) docs/verification/kl_expansion_check.py runs clean. One immaterial nit: my 200k sweep bottoms at -1.78e-15, so 'min = 0.0 exactly' is a floating-point flourish; the sign claim follows from Jensen anyway. Nothing lands."
}

### 3

{
  "attack": "Is the 'not superseded by section 4b' reasoning sound, or did an incomplete grep let 4b material through? 4b contains a subsection literally headed 'the typing question (V-TYPE)'.",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "The adjudication's grep terms (predictive / \\overline L / unbound / Jensen) were incomplete \u2014 grepping 'typing' hits worklog:1048 INSIDE section 4b, and 'm_i' hits :933. I checked both. worklog:1048-1054 is Panel B's question of which data in the induced-volume action is recognition-side vs generative (support, density, reference row, anisotropy, scale) \u2014 a wholly different typing question; :933 is the reaction term b_i(m_i - mbar_i) in natural coordinates. Section 4b's only contact with the observation channel is :953, which writes p^n(o) = prod_a int p_a(dk) r_a(dm) L_a(o_a|k,m) \u2014 i.e. silently ADOPTS the joint typing without flagging the mismatch. worklog 4.5 conspicuously omits T-SIMUL's own obstruction #8 while recording its neighbours. So the right answer was reached by a narrow route, but it survives a broader independent sweep: 4b is genuinely silent on this finding. One under-report: 4b's 4.5(A) at :925-926 IS new material partially corroborating the reviewer's headline \u2014 the skeptic 'insists the word deployed be dropped: S is the tau=1, unit-coefficient, chi-free skeleton, not PIFB2's actual functional' \u2014 supporting 'not literal PIFB2' by a different route. The flat 'never touches' misses that."
}

### 4

{
  "attack": "The verdict rests on panel returns, which the task warns are contested (several skeptics returned survives:false). Are the two panel citations safe?",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "Both citations are of a kind skeptic contest cannot touch. panelA-ground-01 is a ground-truth extraction agent with no skeptic counterpart, and its gotcha #6 (:369) is a verbatim reading of the two PIFB2 displays, verifiable directly against the .tex \u2014 I verified it. panelA-T-SIMUL-derivation.md:251, :302, :333 are exact line hits and are the agent's OWN scope-limitation, obstruction, and next-obligation entries \u2014 self-reported limits, which a skeptic upholding the result strengthens rather than weakens. T-SIMUL is precisely the one Panel A target whose skeptic returned survives:true (worklog:918). The 'panels are contested' attack does not reach these two."
}

### 5

{
  "attack": "Completeness of the evidence sweep: is the defect really unregistered in the repository, and is the 'STRONGER THAN THE REVIEWER NOTICED' well-posedness point actually the adjudication's own?",
  "outcome": "WEAKENS_SCOPE",
  "reasoning": "This lands. docs/research-plans/2026-08-12-pifb2-continuum-roadmap.md:104 \u2014 present in the repo AT THE REVIEWED REVISION caa4a15, hence visible to the reviewer \u2014 already states the finding in exactly the adjudication's 'stronger' form: 'the observation sector must choose between E_{q_i}[-log p(o|k)] and a joint recognition law zeta_i(k,m) for E_{zeta_i}[-log p(o|k,m)]. An expectation under a belief law on k cannot contain an unintegrated random model variable m.' And docs/audits/roadmap-review-2026-08-12/rm-03-action-class.md:363-365 independently confirms it: 'PIFB2.tex eq:free_energy_functional_final writes E_{q_i(c)}[log p(o(c)|k_i,m_i)] with m_i unintegrated. The roadmap is right and the flag should be carried into WP0 as a correction.' The adjudication found neither. So (i) its claimed advance over the reviewer is not its own \u2014 the repo made that argument first; (ii) 'Two independent agents plus the external referee now agree' undercounts by two registers, one pre-dating the review; (iii) the correct status is 'internally registered in three places and left unfenced in the public overview', not 'unnoticed defect'. Verdict unaffected \u2014 arguably reinforced \u2014 but novelty and 'unrepaired' framing overstate."
}

### 6

{
  "attack": "Is severity 'high' honest, or inflated to make a cleaner story? Weigh the deflating evidence the adjudication never considered.",
  "outcome": "WEAKENS_SCOPE",
  "reasoning": "High is defensible but at the top of the band, and no deflating evidence was weighed. Deflators not reported: (a) the derivation never asserts identity \u2014 exact-elbo-proof.md DEFINES F_PIFB2,h^lag,1 as 'the same display with the mutual-information term removed', so the theorem is internally honest and the reviewer's title ('proves a repaired scalar') partly restates what the derivation already says; (b) pifb2-crosswalk.md's opening paragraph explicitly declares the differing recognition object ('The exact-ELBO crosswalk uses a joint private recognition marginal zeta_i(dk,dm), with (q_i,s_i) as its marginals') and its row 12 is conditional \u2014 'Exact ONCE UNDER the joint private law (zeta_a)'. The adjudication's evidence item 11 says the crosswalk states the typing 'without flagging that PIFB2's display differs'; that is uncharitable \u2014 it does flag it, just too weakly to license the overview headline; (c) roadmap:104 already prescribes the repair. What remains genuinely live is one unfenced sentence at overview.md:124-125 whose five-bullet fence list at :128-133 omits the observation typing, mirrored in the worklog theorem block at :22-53 \u2014 I verified both. Given the unbounded Gaussian gap and that overview.md is the public claim, high survives; but it should be labelled claim-hygiene on a registered defect."
}

### 7

{
  "attack": "Is any supporting inference in the evidence chain simply invalid?",
  "outcome": "REPAIRABLE",
  "reasoning": "One is. Evidence item 3 argues PIFB2.tex:2715 'evaluates -E_{q_i}[log p(o_i|k_i)] as a Gaussian with a FIXED precision Lambda_{o_i}, i.e. an m-free likelihood, not a marginal.' Void: a Gaussian predictive marginal is also fixed-precision \u2014 int N(o; k+m, Lambda^{-1}) N(m; 0, V) dm = N(o; k, Lambda^{-1}+V). Lambda_{o_i} is defined only as Sigma_{o_i}^{-1}, 'observation precision' (PIFB2.tex:1337), saying nothing either way. The CONCLUSION (PIFB2 never defines p(o|k_i) as the s_i-marginal, so reviewer claim (iii) is a charitable reconstruction) still holds by absence-of-definition, not by this argument. Related imprecision: 'the only predictive construction, :3251' undercounts \u2014 'predictive' occurs at :522, :1604, :1675, :1882, :3162, :3235, :3258, :3265 \u2014 though all are the cross-scale shadow prior or predictive-processing philosophy, none on the observation channel, so the substance survives."
}

### 8

{
  "attack": "Did it confuse the reviewer's claim with the worklog's claim, particularly in 'reviewer_missed' item (4)?",
  "outcome": "WEAKENS_SCOPE",
  "reasoning": "Partially. reviewer_missed (4) says the reviewer's framing 'assigns the defect to the theorem' and 'gets the culpability backwards'. But 'repaired' means repaired RELATIVE TO PIFB2 \u2014 the reviewer's own word already locates the broken object in PIFB2 and says the theorem silently fixed it. What is actually deficient in the reviewer's finding is the FIX, which is one-sided (rename the theorem's target) and does not require editing PIFB2.tex:689. The adjudication's substantive point \u2014 that the joint typing is ELBO-forced and the edit belongs in PIFB2 \u2014 is correct and I verified the supporting decomposition to 1.8e-15; it is simply aimed at the wrong sentence of the review. A mis-attribution inside a supplementary list, not in the verdict."
}

### 9

{
  "attack": "Does the recommended action generalize further than the evidence supports?",
  "outcome": "REPAIRABLE",
  "reasoning": "Mild scope creep. Recommendation (A) would put into the public overview a quantified claim that the theorem's scalar exceeds 'the predictive objective' by E_q[D_KL(s||s^{(o,k)})] with unbounded gap. But the adjudication itself established (correctly, and I confirmed) that the predictive objective is the reviewer's charitable reconstruction of :669, not literal PIFB2, and that '-E_q log \\bar L paired with a separate KL(s||r) is the ELBO of nothing standard' \u2014 I checked: the exact marginalized ELBO is KL(q||p) - E_q log \\bar L_r using r, and carries NO KL(s||r) term. Fencing the overview against a non-PIFB2, non-ELBO comparison object is more than the load-bearing repair needs; the well-posedness fence is what must go in. It is hedged in its own text ('If PIFB2's :669 form is read as...'), so repairable by demotion to a footnote."
}

### 10

{
  "attack": "Rescue attempt for the programme: read PIFB2's E_{q_i}[log p(o|k_i,m_i)] as mere shorthand for the joint expectation, which would make the theorem exactly right and the finding cosmetic.",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "I tried this; it does not rescue the equality claim. :669 and :689 disagree with each other \u2014 m_i absent vs present \u2014 so at most one can be the intended shorthand, and neither is declared anywhere in the 3956-line file. PIFB2 :459 states the canonical functional has no cross-bundle morphism coupling the channels, and :3501 says the separate q_i and s_i factors DISCARD the within-node cross-channel block, so a joint recognition zeta_i is affirmatively excluded by the manuscript's own structure. Under the shorthand repair the theorem's term WOULD match exactly at mean field \u2014 which is why panelA-T-SIMUL-derivation.md:333 calls it 'a one-line fix in the algebra but changes what -log p(o) actually is' \u2014 but a repair the reader must supply is precisely the reviewer's point. The finding stands."
}

