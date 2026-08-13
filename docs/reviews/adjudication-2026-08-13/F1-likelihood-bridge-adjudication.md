# F1-likelihood-bridge-adjudication

*Verbatim agent return, workflow wf_0b4620e2-7dc, 2026-08-13.*

## finding_id

FINDING 1 — "The theorem proves a repaired scalar, not equality to literal PIFB2" (reviewer severity: High)

## verdict

UPHELD

## severity

high

## confidence

high

## restatement

The reviewer asserts four things. (i) The closed theorem's observation term is the JOINT-law term −E_{ζ_a} log ℓ_a(o_a | K_a, M_a), and the object it calls F_PIFB2,h^{lag,1} is defined as that same display minus the mutual-information term — so the joint typing is retained in the theorem's target. (ii) Literal PIFB2's boxed functional (eq:free_energy_functional_final) writes an expectation under q_i only, with m_i left unbound inside the likelihood. (iii) PIFB2's pointwise display (eq:pointwise_free_energy) drops m_i and "naturally reads as" the predictive likelihood ∫L(o|k,m)s(dm). (iv) Under mean field these two typings are unequal: −E_{q⊗s} log L ≠ −E_q log ∫L(o|k,m)s(dm), with a two-point model of likelihood values 1/4 and 3/4 giving an exact gap of log 2 − ½ log 3 = 0.1438410362. Conclusion: equality of the closed theorem to literal PIFB2 is not proved, and the theorem's target should be renamed a repaired lagged unit-coefficient scalar.

## superseded_status

NOT superseded, and NOT answered by worklog section 4b. Section 4b (docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md:693-1112, subsections 4.1 T-GRAD, 4.2 T-CURV, 4.3 T-RESID, 4.4 T-COEF, 4.5 T-SIMUL, 4.6 Panel B, 4.7 synthesis) never touches the observation-term typing; a grep of the whole worklog for predictive / \\overline L / unbound / Jensen returns hits only at :48-49 (the standing typing block, which defines the predictive model but does not reconcile it with PIFB2's display). The finding is instead INDEPENDENTLY CONFIRMED by the new panel returns: docs/audits/panels-2026-08-12/panelA-ground-01-pifb2-deployed-action.md extract #6 ('a real typing mismatch, not a notational one'), and docs/audits/panels-2026-08-12/panelA-T-SIMUL-derivation.md:251, :302, :333, which explicitly leave it unresolved and list deciding it as a required next step. Two independent agents plus the external referee now agree. Status: CONFIRMED and OPEN.

## evidence

### 1

CITED + LOCATED. Theorem typing confirmed. docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md:34 carries the term `-\mathbb E_{\zeta_a}\log\ell_a(o_a\mid K_a,M_a)` inside the closed theorem, and :41 sets that display equal to `F_{PIFB2,h}^{lag,1} + sum_a I_{zeta_a}(K_a;M_a)`. The source derivation docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/exact-elbo-proof.md (boxed assembled identity, then the sentence 'Define F_{PIFB2,h}^{lag,1} as the same display with the mutual-information term removed') confirms verbatim that the joint-law observation term is RETAINED in the theorem's target and only I(K;M) is stripped. Reviewer claim (i): CONFIRMED exactly.

### 2

CITED, VERBATIM. PIFB2 boxed display, Theory/PIFB2.tex:689: `- \sum_i \int_{\mathcal{C}} \chi_i(c) \mathbb{E}_{q_i(c)}[\log p(o(c) \mid k_i, m_i)] dc`. The expectation is over q_i(c) alone. Theory/PIFB2.tex:170-172 (Definition, Statistical Manifolds) types q_i as a law on B_state = Gaussians over k only, and s_i as a law on B_model over m; :748 states 'the canonical functional contains no cross-bundle morphism coupling the model and belief channels.' So m_i is genuinely a free symbol. STRONGER THAN THE REVIEWER NOTICED: the boxed functional's own argument list at :684 is F[{q_i},{p_i},{s_i},{r_i},{phi_i},{beta_ij},{gamma_ij}] — m_i is not among the declared arguments. The boxed display is therefore not a well-defined functional of its stated arguments. The same free-m_i term recurs at :750 (eq:free_energy_adaptive). Reviewer claim (ii): CONFIRMED, and understated.

### 3

CITED, VERBATIM. PIFB2 pointwise display, Theory/PIFB2.tex:669: `- \sum_i \mathbb{E}_{q_i(c)}[\log p(o(c) \mid k_i)]` — m_i absent entirely. Same m-free form recurs at :941, :2679, :2822, :3211. I found NO place in PIFB2.tex where p(o|k_i) is defined as the s_i-marginal (grep for s_i(dm), marginaliz*, predictive over the whole 3956-line file returns nothing on the observation channel; the only 'predictive' construction, :3251, is the cross-scale shadow prior, a different object). Moreover :2715 evaluates -E_{q_i}[log p(o_i|k_i)] as a Gaussian with a FIXED precision Lambda_{o_i}, i.e. an m-free likelihood, not a marginal. So reviewer claim (iii) is a CHARITABLE RECONSTRUCTION, not a literal reading — the reviewer's own hedge 'naturally reads as' is the right register. The worklog itself invites the reconstruction at :48-49, which defines the predictive model \overline L_i(do|k)=\int L_i(do|k,m)s_i(dm).

### 4

RECOMPUTED (sympy, exact). Two-point model, s uniform on {m1,m2}, L=1/4 and 3/4: joint = -(1/2)log(1/4)-(1/2)log(3/4) = 2log2 - (1/2)log3 = 0.8369882168; predictive = -log(1/2) = log2 = 0.6931471806; gap = log2 - (1/2)log3, and sympy.simplify(gap - (log(2)-log(3)/2)) == 0. Numeric 0.1438410362 — matches the reviewer's digits to 1e-10. Reviewer claim (iv) arithmetic: REPRODUCES EXACTLY.

### 5

RECOMPUTED — the reviewer UNDER-SPECIFIED the model. The stated data ('likelihood values 1/4 and 3/4') does not fix the mixing weights of s. gap(w) = log(3^{w-1}(3-2w)); at w=1/2 it is 0.1438410362, but at w=1/4 it is 0.0923315154 and at w=3/4 it is 0.1308120359. The quoted number requires the uniform two-point law s=(1/2,1/2). Uniform is the natural default reading, so this is a specification lapse, not an error.

### 6

PROVED + RECOMPUTED (direction). -log is strictly convex, so by Jensen -E_s log L >= -log E_s L pointwise in k, hence the JOINT term is the LARGER of the two: -E_{q(x)s} log L >= -E_q log \bar L, with equality iff L(o|k,.) is s-a.s. constant for q-a.e. k. Exact closed form for the gap, verified symbolically to residual 0 on a general 2x3 grid with s on the simplex: joint - predictive = E_q[ D_KL(s || s^{(o,k)}) ], where s^{(o,k)}(dm) = s(dm)L(o|k,m)/\bar L(o|k) is the Bayes posterior over m given o at fixed k. For the reviewer's model this evaluates to 0.5*log2 + 0.5*log(2/3) = log2 - 0.5log3, matching the gap identically. Numerical sweep over 200,000 random finite models: min(joint - predictive) = 0.0 exactly, never negative. So the theorem's scalar is an UPPER bound on any predictive-marginal reading — the theorem is the conservative side, which the reviewer did not state.

### 7

RECOMPUTED — the gap is UNBOUNDED, which the reviewer did not check. Continuous instance L(o|k,m)=N(o;k+m,1), s=N(0,v), q=delta_k: joint = d^2/2 + v/2 + (1/2)log 2pi, predictive = d^2/(2(v+1)) + (1/2)log(2pi(v+1)) with d=o-k, so gap = d^2 v/(2(v+1)) + (v - log(1+v))/2, verified by sympy to be identically that expression. It is >0 for every v>0, equals (1-log2)/2 = 0.1534 at d=0,v=1, and diverges as v->infinity or |d|->infinity. The discrepancy is therefore not a bounded O(small) perturbation that could be absorbed into a residual.

### 8

RECOMPUTED — which typing is FORCED. The private-block generative law is p_a(dk) r_a(dm) L_a(o|k,m) with recognition zeta_a(dk,dm); its negative ELBO is KL(zeta||p(x)r) - E_zeta log L, and KL(zeta||p(x)r) = KL(q||p)+KL(s||r)+I_zeta(K;M) (verified numerically to 1.1e-16 over random 3x4 instances). The JOINT typing is thus the only one with an exact ELBO reading; a predictive-marginal term -E_q log \bar L paired with a separate KL(s||r) is the ELBO of nothing standard. So the defect lies in PIFB2's display, not in the theorem's algebra — the reviewer's framing ('the theorem proves a REPAIRED scalar') gets the culpability backwards even though the claim-status conclusion is right.

### 9

CONFIRMED BY NEW MATERIAL (post-caa4a15). docs/audits/panels-2026-08-12/panelA-ground-01-pifb2-deployed-action.md, extract #6: 'THE OBSERVATION TERM IS TYPED INCONSISTENTLY BETWEEN THE TWO DISPLAYS AND DOES NOT MATCH THE THEOREM'S JOINT EXPECTATION. At :689 ... the expectation is taken over q_i ALONE, with no s_i (or joint zeta_i) expectation. At :669 the pointwise version drops m_i entirely ... This is a real typing mismatch, not a notational one.' Same file extract #13 notes the manuscript already concedes ansatz status at :678 but does NOT concede this. The panel agent reached this independently and BEFORE the review.

### 10

CONFIRMED, STILL OPEN, by docs/audits/panels-2026-08-12/panelA-T-SIMUL-derivation.md:251 ('It does NOT deliver ... the m_i typing of the observation term (:669 vs :689)'), :302 ('The observation term typing mismatch is untouched ... I did not resolve which'), and :333, which lists as a next step 'Decide the observation-term typing (PIFB2:669 vs :689 vs the closed theorem's joint zeta_a expectation) and re-state section 5's bound under the chosen convention. This is a one-line fix in the algebra but changes what -log p(o) actually is.'

### 11

CHECKED — the overclaim is live in the repository at HEAD. overview.md:123-124 states 'the lagged, unit-temperature, unit-coefficient two-channel PIFB2 action is exactly a negative ELBO.' The 'Reading of the terms' list immediately below (overview.md:126-133) fences the tied-replica inventory, the lag, tau=1, and the omitted I(K;M) — but says NOTHING about the observation-term typing. The derivation's own crosswalk (docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/pifb2-crosswalk.md:12) records only 'Expected observation log likelihood | Exact once under the joint private law (zeta_a)', which states the theorem's typing without flagging that PIFB2's display differs. So the unfenced claim the reviewer targets is real and unrepaired.

### 12

EXECUTED. python docs/verification/kl_expansion_check.py runs clean ('All assertions passed'), confirming the environment and that this finding is independent of the KL-expansion machinery.


## recomputation

Ran four scratch scripts under the session scratchpad (never in the repo). (1) Exact sympy reconstruction of the reviewer's two-point model: joint = 2log2 - (1/2)log3 = 0.8369882168, predictive = log2 = 0.6931471806, gap = log2 - (1/2)log3 = 0.1438410362, with sympy.simplify(gap - (log(2)-log(3)/2)) == 0. Reviewer's digits reproduce exactly. (2) Weight sensitivity: gap(w) = log(3^{w-1}(3-2w)); 0.0923315154 at w=1/4, 0.1438410362 at w=1/2, 0.1308120359 at w=3/4 — the quoted value needs the uniform law. (3) General identity, verified symbolically to residual exactly 0 on a 2x3 grid with s constrained to the simplex: (-E_{q(x)s} log L) - (-E_q log \\bar L) = E_q[D_KL(s || s^{(o,k)})] >= 0, s^{(o,k)}(dm) = s(dm)L(o|k,m)/\\bar L(o|k). Numerical sweep of 200,000 random finite models: minimum of (joint - predictive) = 0.0, never negative. (4) Gaussian instance L(o|k,m)=N(o;k+m,1), s=N(0,v), q=delta_k: gap = d^2 v/(2(v+1)) + (v - log(1+v))/2 (sympy-verified identity), = (1-log2)/2 = 0.1534264097 at d=0,v=1, unbounded in v and d. (5) ELBO decomposition KL(zeta||p(x)r) = KL(q||p)+KL(s||r)+I_zeta(K;M) verified numerically to 1.1e-16 over random 3x4 instances, establishing that the joint typing is the ELBO-forced one. (6) Ran docs/verification/kl_expansion_check.py — all assertions pass (independent of this finding).

## reviewer_missed

Four things, in rising order of importance. (1) The two-point model is under-specified: the number 0.1438410362 requires s uniform, i.e. weights (1/2,1/2); gap(w) = log(3^{w-1}(3-2w)) gives 0.0923 at w=1/4 and 0.1308 at w=3/4. (2) The Jensen counterexample quantifies theorem-vs-PREDICTIVE, which is a comparison against the reviewer's own charitable reconstruction of :669, not against PIFB2 as literally written. Against the boxed :689 no Jensen comparison exists at all, because :689 has a free symbol m_i that is not among the boxed functional's declared arguments (Theory/PIFB2.tex:684) — 'equality to literal PIFB2' is not merely unproved, it is not well-posed. That is a stronger and cleaner statement of the same defect. (3) The reviewer did not check the SIGN or the SIZE. Jensen determines the direction: the theorem's joint term is always the LARGER, exceeding the predictive term by exactly E_q[D_KL(s || s^{(o,k)})], the expected information the observation carries about the model parameter. And the gap is unbounded — in a Gaussian instance it is d^2 v/(2(v+1)) + (v-log(1+v))/2, which diverges with model uncertainty v. So it cannot be absorbed as a small residual. (4) The reviewer's framing assigns the defect to the theorem ('proves a REPAIRED scalar'). The joint typing is the one FORCED by the ELBO — negative ELBO of p(dk)r(dm)L(o|k,m) under recognition zeta is exactly KL(q||p)+KL(s||r)+I(K;M) - E_zeta log L (verified to 1e-16). The theorem's algebra is right; PIFB2's display is the defective object. The correct fix therefore edits PIFB2 (bind m_i under s_i at :689, or reconcile :669), not only the theorem's label. Finally, one asymmetry the reviewer did not draw: the theorem needs zeta = q(x)s to kill I(K;M), and it is precisely under that mean field that the Jensen gap to the predictive reading is generically strictly positive — the two repairs pull in opposite directions and cannot both be satisfied by one choice of zeta.

## recommended_action

Two edits, both required; the first is the load-bearing one. (A) In overview.md, amend the claim at :123-124 and add a fifth bullet to the 'Reading of the terms' list at :126-133: the theorem's observation term is -E_{zeta_a} log L_a(o_a|K_a,M_a), an expectation over the JOINT private law; PIFB2's boxed display (Theory/PIFB2.tex:689) writes E_{q_i}[log p(o|k_i,m_i)] with m_i unbound and not among the functional's declared arguments (:684), and its pointwise display (:669) drops m_i entirely. State plainly: 'Equality to the literal PIFB2 observation term is not proved and is not currently well-posed; the theorem's target is the joint-typed lagged unit-coefficient scalar. If PIFB2's :669 form is read as the predictive marginal -E_q log \\bar L, the two differ by E_q[D_KL(s_i || s_i^{(o,k)})] >= 0, so the theorem's scalar is an UPPER bound on the predictive objective, and the gap is unbounded in the model uncertainty.' Mirror the same caveat in the worklog's closed-theorem block (:22-53, after the Typing block at :46-49) and add a row to docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/pifb2-crosswalk.md next to line 12 reading 'PIFB2 observation display (:669/:689) | typing mismatch; not matched by this theorem.' (B) Execute the step panelA-T-SIMUL-derivation.md:333 already names: decide the convention by author fiat and edit Theory/PIFB2.tex:689 (and the duplicate at :750) to bind m_i — write -chi_i E_{q_i(c) (x) s_i(c)}[log p(o(c)|k_i,m_i)] if the joint typing is adopted, which makes the closed theorem exact on that term and simultaneously repairs :689's free symbol; then reconcile :669, :941, :2679, :2822 to the same convention. Note explicitly in the commit that adopting the joint typing is what the ELBO forces, and that the predictive alternative has no exact ELBO reading. Do NOT record this finding as answered by section 4b — 4b is silent on it.
