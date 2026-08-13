# F2-lagged-vs-contemporaneous-verification

*Verbatim agent return, workflow wf_0b4620e2-7dc, 2026-08-13.*

## holds

true

## corrected_verdict

The adjudication survives. Verdict UPHELD, severity high, and NOT superseded by section 4b all stand, and I confirm them on independent evidence rather than by deferring to the adjudication: my own base-neighbour instance (3-site cycle, 2 neighbours per site, K=3, nontrivial permutation transports) exhibits an exact negative-ELBO decomposition (residual 3.6e-15) with a strictly positive base-neighbour transported-KL sector (0.496109389) under a generative joint whose total correlation across design points is 7.4e-17 — i.e. `hyp:gen-design-product` holding exactly. That alone refutes the '<=' direction of worklog:291 and the load-bearing inference in worklog:250, and by inheritance the boxed :310-311 and overview.md:171-173. Every one of the adjudication's other numbers reproduces to the printed digit, kl_expansion_check.py passes, and all citations are exact except A4.1 beginning at wave2-01-constructions.md:317 rather than :314.

Three evidence items should be downgraded, none of which touches the verdict. (1) The A4.1/TC_D 'independent third route' is not one: TC_D is a recognition-side total correlation and is exactly zero on the design-product recognition family the worklog actually uses (typed-construction.md:110; I computed 0.000e+00), so it bears on a generic slogan the worklog never asserts. Strike it from `evidence` and from `reviewer_missed`(b), keeping only the sufficiency half of (b) — that relaxing the hypothesis yields an interaction energy -E log psi (which I verified symbolically to 5.6e-17), not a transported KL. (2) The appeal to worklog 4.5 should be narrowed to its verifiable content — 4.5(C) answers overview.md:198's open decision 4 in the negative — and stripped of the gloss that this makes the reviewer's lagged/contemporaneous distinction 'a proven inequivalence of two different objects', because 4.5's counterexample is a directed peer 3-cycle while the base-neighbour stencil is edge-symmetric, and 4.5's own checkable prediction at worklog:967 says that under edge-symmetry the two flows agree up to halved coupling. (3) The supporting citation of 4.1(ii)(c) must carry the caveat that the Dirichlet energy is the block's value AT THE DIAGONAL, i.e. under postulate (P2)'s unproven lim_{h->0} lim_{n->inf} exchange.

Two factual corrections to `superseded_status`. It is not true that panelB-V-TYPE-derivation.md:52 is 'the only panel text touching it': panelB-V-BRIDGE-derivation.md:67 ((H5)) and :314 (OB-12) restate the same claim, both self-labelled inherited — so the conclusion holds but the repair scope grows to those two loci. And the survey missed 4b material that reinforces the finding: worklog 4.3 (:872-874) states that P^n_h = (x)_a P^n_a 'by construction' and its skeptic calls blockwise-product rigidity 'a restatement of the product hypothesis' — the worklog's own new section conceding the strict product structure that 3c.3-3c.5 deny. Net: 4b makes the finding more forceful, as the adjudication says, but for a partly different reason than it gives.

Two minor wording fixes: the evidence bullet should adopt the recommendation's own careful framing that worklog:250 is 'either tautological or false' rather than claiming Test 1 refutes it 'outright'; and the remark that the reviewer's line cites 'have drifted by ~4-10 lines' should note they were exact at the reviewed revision caa4a15 (:230, :240, :281-282, :300-301) and shift by a uniform +10.

## attacks

### 1

{
  "attack": "Did it actually read the cited loci, or accept paraphrases? Checked every citation character-by-character against the files.",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "Every load-bearing citation is exact. worklog:240 ('A base-neighbour block is precisely residual cross-design dependence'), :250 ('such a law exists iff `hyp:gen-design-product` is relaxed'), :291-292 ('vanishes identically iff ... So eta_q is the strength of admitted cross-context dependence'), :309-311 (boxed 'C earns its manifold structure iff the generative model admits cross-context dependence') all verified verbatim (grep on docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md). Theory/04_generative.tex:89-96 reads exactly as quoted, including '\\status{HYPOTHESIS}\\label{hyp:gen-design-product}'. typed-construction.md:5-7, :39-54, :71-88 confirm A = agent-site indices a=(i,x), lagged u_ab^n=(Omega_ab^n)_# q_b^n, and P_h^n = (x)_{a in A} P_a^n. panelA-T-GRAD-derivation.md:37 is exactly 'Let A = {i}x\u039b_h, and instantiate the tied-replica theorem ... lagged sources u_{c,c'} = (\u03a9^A_{c,c'})_# q_i^n(c')'. :328 and :351 are the first body lines under the \u00a75.4 and \u00a75.6 headers at :327 and :350 and carry exactly the quoted sentences. panelA-T-GRAD-skeptic.md:134 carries the quoted mixed-time endorsement. boundary-counterexamples.md:68-73 reads as quoted. overview.md:166-173 carries both the 'costs exactly one hypothesis' and the boxed 'iff' claim. Only trivial slip: Theorem A4.1 begins at wave2-01-constructions.md:317, not :314."
}

### 2

{
  "attack": "Did it RECOMPUTE or assert? I rewrote the computations from scratch with different numbers, a different lattice topology (3-cycle, 2 neighbours per site, K=3, nontrivial permutation transports Omega), and an explicit total-correlation check on the normalized joint.",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "Every number reproduces to the printed digit, and my structurally stronger instance confirms the same conclusion. Independent script C:\\Users\\CHRISA~1\\AppData\\Local\\Temp\\claude\\C--Users-chris-and-christine-Desktop-MultiAgentELBO\\c87a5256-fdb7-4d07-a3d8-c6455d784e89\\scratchpad\\adv_f2.py: (A) 3-site base-neighbour instance, exact KL(Q||P)=2.846293185771904 vs theorem block decomposition 2.846293185771908 (residual 3.6e-15), base-neighbour sector = 0.496109389 > 0, and the normalized joint's total correlation across design points = 7.4e-17 with ||P - (x)_a P_a||_inf = 8.7e-19, i.e. hyp:gen-design-product holds EXACTLY. This independently reproduces exact-elbo-proof.md:96-118's boxed identity and refutes worklog:291's '<=' direction without relying on the adjudication's setup at all. (B) I(K_a;K_b) = 0.000000/0.082283/0.368064 at rho=0/0.4/0.8, matching the closed form (1/2)[(1+rho)log(1+rho)+(1-rho)log(1-rho)], with transported KL identically 0 \u2014 matches. (C) 0.831777 = 0.6 log 4 \u2014 matches. (D) excess 0.306321213 vs D(q_a||q_b) 0.253246060, and I additionally verified symbolically that the excess equals -E_Q log psi to 5.6e-17, confirming the interaction-energy characterization rather than merely asserting it. (E) F = 0.238399726773653 = sum_a F_a + TC_D with TC_D = 0.130812036, residual 8.3e-17. Also re-ran docs/verification/kl_expansion_check.py: 'All assertions passed' (1/2 g^F, 1/3 and 1/6 T_skew, h^3 cancellation across Gaussian/Bernoulli/Exponential)."
}

### 3

{
  "attack": "The A4.1 / TC_D bullet is sold as 'an independent third route' and 'a second, structurally different refutation'. Is it actually about the base-neighbour sector at all?",
  "outcome": "WEAKENS_SCOPE",
  "reasoning": "It is not. TC_D(Q_X) = KL(Q_X || (x)_a Q_a) (wave2-01-constructions.md:328) is a RECOGNITION-side total correlation, and typed-construction.md:110 states that in the construction at issue 'The global recognition law is the finite product of the Q_a^{n+1}'. I computed TC_D for a design-product recognition law: exactly 0.000e+00. So on the very family the worklog uses, A4.1's cross-design term vanishes identically and contributes nothing to the base-neighbour question. What A4.1 refutes is the generic slogan 'a cross-design term in F implies the hypothesis is relaxed', which worklog:250/:291 does not assert in that form \u2014 those are statements about the base-neighbour transported-KL sector specifically. The bullet is arithmetically correct (I reproduced it) but its relevance is oversold, both in `evidence` and in `reviewer_missed`(b) where it is offered as an 'independent internal refutation the reviewer missed'. It should be demoted to an analogy. The verdict does not depend on it: Test 1 / my Test A carry the refutation alone."
}

### 4

{
  "attack": "'The only panel text touching it is panelB-V-TYPE-derivation.md:52.' Is that survey accurate?",
  "outcome": "WEAKENS_SCOPE",
  "reasoning": "False as stated. grep for 'gen-design-product' across docs/audits/panels-2026-08-12/ returns THREE loci, not one: panelB-V-TYPE-derivation.md:52, plus panelB-V-BRIDGE-derivation.md:67 ('(H5) hyp:gen-design-product ... must be RELAXED. Without this the base-neighbour block does not exist and there is nothing to take a limit of. This is E3 and it is unchanged.') and panelB-V-BRIDGE-derivation.md:314 ('OB-12 (unchanged, inherited). The whole base-neighbour block requires relaxing hyp:gen-design-product'). The adjudication's substantive point survives \u2014 both V-BRIDGE loci self-label as inherited ('This is E3', '(unchanged, inherited)'), exactly as V-TYPE:52 cites '(worklog E5)' \u2014 so none is independent verification. But the survey is inaccurate and it understates how far the contested claim has now propagated into the panel corpus, which sharpens rather than blunts the recommended_action's scope: the repair must also flag V-BRIDGE (H5) and OB-12 as inheriting a defective premise."
}

### 5

{
  "attack": "Is the appeal to worklog 4.5 (T-SIMUL) as making the finding 'MORE forceful' sound, or is it a different claim being used to answer this one?",
  "outcome": "WEAKENS_SCOPE",
  "reasoning": "Partly a different claim. Three problems. (i) 4.5's target is the PEER-coupling flow of the deployed PIFB2 simulator; transferring it to base-neighbour (same agent, two contexts) coupling relies on panelA-T-GRAD-derivation.md:351's structural identification '(i,c') is a distinct element of A ... structurally identical to a peer' \u2014 an argument, not a theorem, and 4.5's decisive counterexample is a DIRECTED attention 3-cycle with complex linearization eigenvalues. (ii) The base-neighbour stencil is symmetric by construction (uniform beta over the 2d neighbours; the whole O(h^3) parity cancellation of 4.1(i) depends on it), and 4.5's own 'Checkable prediction' at worklog:967 says 'Under edge-symmetry the lagged flow equals the same-time flow at *halved* peer coupling.' In precisely the edge-symmetric regime relevant here the two schemes agree up to a factor 2 in the coupling \u2014 far weaker than 'not the dt->0 limit of one another'. (iii) The reviewer's Finding-2 dichotomy is about fixed-joint ELBO EXACTNESS, not about dynamical limits; 4.5 answers overview.md:198's open decision 4, a neighbouring but distinct question. The adjudication's narrower statement \u2014 that 4.5 answers open decision 4 in the negative \u2014 is correct and I verified it at worklog:943-947. Its stronger gloss, that this converts the reviewer's distinction into 'a proven inequivalence of two different objects', overreaches."
}

### 6

{
  "attack": "Does the strongest new supporting evidence (worklog 4.1(ii)(c), 'the block's value at the diagonal is exactly (1/2) INT ||D^A q||^2 + O(h^2)') carry an unstated caveat that would blunt it?",
  "outcome": "WEAKENS_SCOPE",
  "reasoning": "Yes, one the adjudication omits. That value is delivered AT THE DIAGONAL q^{n+1}=q^n, which is exactly the derivation's own postulate (P2) at panelA-T-GRAD-derivation.md:358: 'evaluation at a self-consistent stationary configuration ... i.e. the iterated limit lim_{h->0} lim_{n->inf}, whose exchange is unproven', and worklog:790-792 still records 'this is pointwise convergence at a fixed C^2 section, not Gamma-convergence'. The skeptic's forward-Euler reframing rebuts 'mass term, minimizer phi=0' but does not discharge the order-of-limits declaration for the diagonal energy value. So 'the Dirichlet energy is obtainable from the LAGGED, product-law construction' is true modulo a declared evaluation point. This does not touch the verdict: my Test A refutes worklog:250 and :291 at fixed finite h with a strictly product law and no diagonal evaluation whatsoever."
}

### 7

{
  "attack": "Did it inflate scope by extending the finding to 3c.5 (:309-311) and overview.md, which the reviewer's location line (:213-242,280-301) arguably does not cover? And is the 'the reviewer's line cite has drifted by ~4-10 lines' characterization honest?",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "I checked the reviewed revision directly. At caa4a15 the four claims sit at :230, :240, :281-282, and :300-301 (git show caa4a15:docs/research-plans/...). The reviewer's cited ranges :213-242 and :280-301 therefore covered ALL FOUR exactly, including the boxed 3c.5 conclusion at old :300-301 = current :310-311. The extension to 3c.5 is legitimate, not manufactured. The extension to overview.md:166-173 is also legitimate \u2014 I verified the text is propagated there nearly verbatim. Minor demerit only: the shift is a uniform +10 (4b was appended at :693 and above it nothing moved except a 10-line insertion), and the reviewer's cites were EXACT at the revision reviewed, so 'has drifted by ~4-10 lines' slightly misdescribes the situation in a way mildly unflattering to the reviewer. Not material."
}

### 8

{
  "attack": "Internal tension: the evidence bullet says Test 1 'refutes the => direction of worklog:250 ... outright', but recommended_action(1) concedes :250 is 'either tautological ... or false'.",
  "outcome": "WEAKENS_SCOPE",
  "reasoning": "Real but self-corrected. If 'a normalized generative law that couples neighbouring design points' just means 'a law that is not a design product', the '=>' direction of :250 is a tautology and no computation can refute it; what Test 1 actually refutes is the load-bearing inference that the base-neighbour sector REQUIRES such a law. The recommended_action states this correctly; the evidence bullet overstates it. The right formulation is the one in the recommendation, and adopting it costs the verdict nothing."
}

### 9

{
  "attack": "Is severity 'high' honest, or inflated to make a cleaner story?",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "Honest. The defect does not touch the exact finite tied-replica ELBO theorem, and the adjudication says so \u2014 it explicitly preserves the idle-wheel half of 3c.5 and the finite-h exactness in recommended_action(5) and reviewer_missed(c), which is the opposite of inflation. But the falsified clause is boxed, load-bearing, and has propagated to overview.md:166-173 as a headline 'Idle-wheel result', to worklog:589 and :683, and into two Panel B returns as a declared hypothesis; and it converts a modeling declaration into a purported probabilistic quantity (eta_q). Independently confirming the 'declared, not measured' point: with sum_b beta_b = 1 and m_h = ceil(d h^{-2}) and weight h^d, worklog:768 fixes the coefficient of (1/2)INT||D^Aq||^2 at exactly 1 \u2014 eta_q is forced to a constant by normalization, not free to record a 'strength of dependence'. High is right."
}

### 10

{
  "attack": "Is 'NOT superseded and NOT answered by 4b' correct \u2014 or did 4b quietly settle the gen-design-product claim somewhere the adjudication did not look?",
  "outcome": "FAILS_TO_LAND",
  "reasoning": "Correct, and if anything under-argued. I grepped 'gen-design-product' across the whole worklog: inside 4b (:693-1104) there is not one occurrence; 4.1's reconciliation at :793-796 endorses only the A4.4 escape; the hand-written synthesis 4.7 (:1069-1104) is silent; worklog:683 itself records the neighbouring question as 'Untouched by either panel'. Beyond that, I found 4b material the adjudication MISSED that further confirms the reviewer: worklog 4.3 (:872-874) states 'because P^n_h = (x)_a P^n_a by construction, this law is structurally incapable of generating multi-body operators', and the T-RESID skeptic strikes blockwise-product rigidity as 'true but vacuous \u2014 a restatement of the product hypothesis'. That is the worklog's own 4b conceding, in a different section, exactly the strict product structure that falsifies 3c.3-3c.5. The omission strengthens the adjudication's conclusion rather than weakening it."
}


## hold_placeholder

x
