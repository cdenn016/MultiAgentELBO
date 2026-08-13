# panelA-T-RESID-skeptic

*Recovered verbatim from workflow journal.jsonl, 2026-08-13. Agent a565302f.*

## survives

false

## confidence

high

## corrected_statement

NOT PROVED as stated. Statement (4) is false as written (two independent counterexamples); statement (6)'s headline is false outside a symmetry-fine-tuned class; statements (1) and (2) are true but vacuous/tautological; statements (0), (3), (5) and the expansions in (6) are correct and survive with strengthened hypotheses. The strongest surviving theorem:

THEOREM (label-elimination residual for the tied-replica law). Assume (H1)-(H5) as stated, plus:
(H6') the reference is a product of PROBABILITY laws with (C_h)_#Pi_{h,o} ~ nu_h — this is NOT automatic from Pi being a product; it additionally requires lambda_a << bar u_a (level 2) resp. lambda_a << u_aj for every j (level 3);
(H9) S_h in L^inf(nu_h) whenever the Hoeffding-Mobius space G of 07b:1204 is invoked (automatic if all retained coordinate spaces are finite; FAILS for Gaussian sources under Lebesgue);
(H4') D_KL(q_a||u_aj) < infinity for every j (absolute continuity alone is not enough), or use the entropy-free proofs below;
(H7') the link expansion carried to fourth order with q_a-dominated remainders, uniform over edges.

(0) Posterior block factorization: Pi_{a,o} = pi_a^post (x) pi^q_aj u^n_aj (x) pi^s_al v^n_al. TRUE. The replica blocks are unchanged by conditioning — the belief-copy block is statistically inert, carries no evidence, and is independent of every other agent.

(1) Blockwise-product rigidity: a product law composed with a blockwise map pushes forward to a product, so S_h = sum_a S_a(x_a) nu_h-a.e. and all Hoeffding components above order 1 vanish. TRUE but VACUOUS: it is a restatement of the hypothesis, proves nothing about any law with cross-agent coupling, and does NOT discharge final-report.md:55, whose "its" binds to the section-valued family of final-report.md:53-54 that the claim concedes it does not supply. Use the conditional-integration projectors of 07b:1185-1200, not an anchored Mobius sum (which evaluates an a.e.-defined S on a nu-null slice).

(2) Label-retaining contraction: "retains the labels together with (K,M,X,Y)" means all six coordinates, so C_h is a bimeasurable relabeling of the identity and the statement is exact-elbo-proof.md:141-147 verbatim (reproduced numerically to 0.00e+00). eps_h = 0; c_h = 0 ONLY under the unnormalized convention — under the normalized convention of statement (3), c_h = sum_a[-log p_a(o_a) + log|J^q_a||J^s_a|] != 0. Since the microscopic law was engineered to have this ELBO, and release.json's first obligation demands a family specified INDEPENDENTLY of the PIFB2 ansatz, this establishes nothing about PIFB2's effective-action status.

(3) Label-marginalizing contraction — SURVIVES INTACT, and is the real result. Pointwise, unconditionally:
    eps_a(x) = log[ prod_j u_aj(x)^{pi_aj} / sum_j pi_aj u_aj(x) ] = -D_KL(pi^q_a || pi^{q,post}_a(.|x)) <= 0,
an algebraic identity (not merely an expectation identity), with eps_a == 0 iff u_aj = bar u_a lambda-a.e. for all j, iff X_a is independent of J^q_a. Under the normalized convention c_a = -log Z^q_a >= 0 with Z^q_a = int prod_j u_aj^{pi_aj} dlambda_a in (0,1] by generalized Holder. Companion exact identity, hypothesis-free and preferable to the c_h language:
    sum_j pi_aj D_KL(q_a||u_aj) = D_KL(q_a || PoE_a) + c_a,   PoE_a = prod_j u_aj^{pi_aj}/Z^q_a.
CAVEAT: eps_a is the residual against the STIPULATED projection S^PIFB_{a,rel} := sum_j pi_aj E_aj (recognition row frozen at the prior). It is not a best approximation and is not unique; freezing at beta* or at the envelope-reduced row -log sum_j pi_j e^{-D_j} yields different residuals of different sign. Determinacy here comes from a stipulation, not a derivation.

(4) REPLACE ENTIRELY. The cumulant series is asymptotic, not convergent: its radius is pi/range for a symmetric two-source row, so it diverges on {x : range_j E_aj(x) > pi}, a set of positive q-measure in every Gaussian instance. And -kappa_2/2 is NOT in general outside the PIFB2 peer span: for one-dimensional common-covariance Gaussian sources with J >= 2 distinct means it lies EXACTLY in span{E_aj, 1}. The correct statement is: the exact residual eps_a (e.g. -log cosh(hx)) is outside the span in that family, and in expectation E_{q_a}[-kappa_2/2] splits as -Var_pi(D)/2 (which PIFB2's own envelope reduction already contains, PIFB2.tex:717-733) minus (1/4)sum_{j,j'} pi_j pi_j' Var_{q_a} log(u_aj'/u_aj), the latter vanishing iff the transported sources are q_a-a.s. mutually proportional. That the latter is not in the span of PIFB2's terms remains CONJECTURE — no proof is given.

(5) Ordering theorem — SURVIVES: D_KL(q_a||bar u_a) <= -log sum_j pi_aj e^{-D_aj} <= sum_j pi_aj D_aj, right-minus-middle = D_KL(pi^q_a||beta*_a) exactly. Prove the left inequality entropy-free (set tilde-E_j = log(q_a/u_aj), apply concavity of -lse to E_q tilde-E_j = D_aj); do not add and subtract H(q_a), which may be infinite. The comparison to 07b:1816-1829 is CORRECT and is the submission's genuinely novel contribution: coarsening the label inside the row functional gives the middle term, eliminating it from the joint law gives the left term, and 07b (which anticipates the structure at 1811-1814) never computes the gap.

(6) REPLACE THE HEADLINE, KEEP THE FORMULAS. Under (H7'):
    sum_j pi_aj D_aj = (h^2/2) sum_j pi_aj Var_{q_a}(g_j) + O(h^4),
    D_KL(q_a||bar u_a) = (h^2/2) Var_{q_a}(bar g) + O(h^4),        bar g = sum_j pi_aj g_j,
    E_{q_a} eps_a = -(h^2/2) E_{q_a} Var_{pi_a}(g_J) + O(h^4),
    c_a = (h^2/2)[sum_j pi_aj Var_{q_a} g_j - Var_{q_a} bar g] + O(h^4),
with the O(h^3) coefficients vanishing identically by per-source normalization (a strengthening of the claim's own derivation, confirmed on a skewed balanced-in-mean row). CORRECT CONCLUSION: the label-marginalized contraction produces the Fisher quadratic of the ROW-AVERAGED covariant derivative, I(Dbar-theta, Dbar-theta), where PIFB2 retains the row-average of the per-edge quadratics; the deficit is (h^2/2)E_q Var_pi(g_J) >= 0. Consequently the retained fraction is Var_q(bar g) / sum_j pi_j Var_q(g_j), and:
  - BALANCED rows (bar g == 0: symmetric neighbour set with symmetric row) — retained fraction 0, the contracted relational action is O(h^4), and the Fisher-Dirichlet sector is NOT recovered at O(1) under the h^{d-2} weight. Gaussian witness exact: peer = h^2/2, D_KL(q||bar u) = h^4/4 + O(h^6). This is the relevant case for an isotropic continuum limit, but it is symmetry-fine-tuned, NOT "the generic lattice case".
  - BIASED rows (bar g != 0) — the Fisher-Dirichlet sector IS recovered at O(1). Retained fraction 0.900 for a two-left-neighbour causal row, 0.360 for pi = (0.8,0.2), and 1 exactly for any single-source agent. PIFB2.tex:709 names causal masking, ALiBi and learned position biases as the deployed pi_ij, so the negative result does not reach the deployed model.
Finally, none of this is a statement about the ELBO: the full objective is unchanged, and on a balanced stencil the peer sector migrates in its entirety into the discarded conditional KL E_{q_a} D_KL(beta_a || pi^{q,post}_a(.|X)). Level 2 deletes the attention row from the recognition law altogether, so "PIFB2's peer sector is not generated" is more honestly stated as "deleting the attention variable deletes the attention-weighted peer energy". The reading "the peer sector IS the additive constant c_h" holds only at the single recognition point around which (H7) is expanded, since c_a is constant in q_a and sum_j pi_j D_aj is not.

VERDICT ON THE TARGET: the identity S_h^exact = S_h^PIFB + eps_h + c_h is made DETERMINATE for this law — that much is achieved and is real. It is not made NON-TAUTOLOGICAL: the microscopic law is the one reverse-engineered from PIFB2, and the projection S^PIFB is stipulated rather than derived. Status should be downgraded from PROVED to PARTIAL, with (4) marked REFUTED-AS-STATED and (6) marked SCOPE-RESTRICTED-TO-BALANCED-ROWS.

## attacks

### 1

{
  "attack": "VECTOR 8 / COUNTEREXAMPLE \u2014 Statement (4) is FALSE in the claim's own flagship example. The 'leading generated operator' -\u00bd\u03ba\u2082 is asserted to be 'outside the span of PIFB2's action'. Take the claim's own witness: q=N(0,1), u_\u00b1=N(\u00b1h,1), \u03c0=(\u00bd,\u00bd), peer basis E_\u00b1(x)=-log u_\u00b1(x).",
  "verdict": "KILLS_IT",
  "reasoning": "log(u_-/u_+) = -2hx, so \u03ba\u2082(x)=h\u00b2x\u00b2. But E_+ + E_- = x\u00b2 + h\u00b2 + log2\u03c0. Hence -\u00bd\u03ba\u2082 = -(h\u00b2/2)(E_+ + E_-) + (h\u00b2/2)(h\u00b2+log2\u03c0) \u2014 EXACTLY a linear combination of the peer basis plus a constant. Verified by least squares at h=0.37: fitted coefficients (-0.0684500, -0.0684500, +0.1351735) against the exact prediction (-h\u00b2/2, -h\u00b2/2, h\u00b2(h\u00b2+log2\u03c0)/2) = (-0.0684500, -0.0684500, +0.1351735); max residual 1.6e-13 (relative 3.6e-14). This generalizes: for one-dimensional common-covariance Gaussian sources, E_j = x\u00b2/2 - \u03bc_j x + const, so span{E_j,1} is ALL quadratics once J\u22652 with distinct means, while log(u_j'/u_j) is affine so \u03ba\u2082 is a quadratic. Verified IN THE SPAN for J=2,3,5 with random means/rows (residuals 7.7e-15 to 2.6e-12). Gaussian equal-covariance beliefs are precisely PIFB2's belief class and precisely the class used in statement (6). By contrast the EXACT residual \u03b5_a(x) = -log cosh(hx) IS outside the span (residual 0.223), so the conclusion the claim wants survives for \u03b5_a but NOT for the operator it names as the leading generated one. Additionally the stated ARGUMENT is a non-sequitur: it reads \u03c0^q_a as 'the attention row' and invokes PIFB2's linearity in \u03b2, but \u03c0 is the fixed generative prior row and \u03b5_a does not depend on \u03b2 at all; and two lines later the claim's own split concedes that half of E_q[-\u00bd\u03ba\u2082], namely -\u00bdVar_\u03c0(D), 'is what PIFB2 already has'. No proof is anywhere given that the residual functional is not in the span; that assertion is CONJECTURE status."
}

### 2

{
  "attack": "VECTOR 1 / HIDDEN HYPOTHESIS \u2014 Statement (4)'s cumulant series has finite radius of convergence, which is never assumed and demonstrably fails.",
  "verdict": "KILLS_IT",
  "reasoning": "\u03b5_a = -\u039b_x(-1) with \u039b_x(t)=log E_\u03c0 e^{tE_{aJ}(x)}; the series \u03a3\u03ba_n t^n/n! is evaluated at |t|=1. For J=2, \u03c0=(\u00bd,\u00bd), E_1=0, E_2=D, the nearest singularity of log((1+e^{tD})/2) is at tD=i\u03c0, so the radius is \u03c0/D and the series DIVERGES for D>\u03c0. mpmath at 40 dps, 60 terms: D=2 \u2192 partial sum 0.433781 = exact (last term 5.7e-14); D=3 \u2192 0.85446 vs exact 0.85544; D=3.5 \u2192 partial sum -10.79 vs exact -1.0866, terms growing to 2.2e1; D=5 \u2192 partial sum -3.04e10 vs exact -1.8136, terms 4.3e10. In the claim's own Gaussian witness range_j E_aj(x)=2h|x|, so the series diverges on {|x|>\u03c0/(2h)} \u2014 a set of positive \u03bb- and positive q-measure for EVERY h>0. The claim writes 'the cumulant expansion of \u03b5_a is \u03b5_a = -\u00bd\u03ba\u2082+\u2159\u03ba\u2083-\u22ef' as an unqualified identity with no smallness hypothesis. The Hoeffding sup-norm bound -\u03b5_a \u2264 \u215b(range)\u00b2 is fine (verified 0/20000 violations); it is only the series that fails. Repairable by restating as an asymptotic expansion valid where range_j E_aj(x) is small, but as written statement (4) is false pointwise."
}

### 3

{
  "attack": "VECTOR 8 / COUNTEREXAMPLE \u2014 Statement (6)'s headline negative fails for every biased row, which is exactly the deployed regime. 'Balanced stencil' is called 'the generic lattice case'; it is a symmetry-fine-tuned case of measure zero, and PIFB2.tex:709 names causal masking, ALiBi, and learned position biases as the deployed \u03c0_ij.",
  "verdict": "KILLS_IT",
  "reasoning": "High-precision (mpmath, 50 dps) computation of D_KL(q\u2016\u016b) vs \u03a3_j\u03c0_jD_aj for q=N(0,1), u_j=N(m_j h,1). BALANCED \u03c0=(\u00bd,\u00bd), m=(+1,-1): ratio 0.0190, 0.00493, 0.00125, 0.000312 at h=0.2,0.1,0.05,0.025 \u2192 0, and D/(h\u2074/4) \u2192 0.8374, 0.9507, 0.9869, 0.9967, 0.9992 (the claim's own numbers reproduced \u2014 its numerics are honest). CAUSAL two-left-neighbour row \u03c0=(\u00bd,\u00bd), m=(-1,-2): ratio \u2192 0.8916, 0.8979, 0.8995, 0.8999 \u2192 0.9. NINETY PERCENT of the peer sector SURVIVES at O(h\u00b2), hence at O(1) under the h^{d-2} edge weight of lattice-continuum-asymptotics.md:20-22, matching the predicted (h\u00b2/2)Var_q(\u1e21)=9h\u00b2/8 to 4 digits. ALiBi-like \u03c0=(0.8,0.2): ratio \u2192 0.3600 = (2w-1)\u00b2. Single-source agents (|J|=1, explicitly admitted at typed-construction.md:57-59): \u016b=u_1, \u03b5\u22610, and the peer term is reproduced EXACTLY at all orders. So 'the Fisher-covariant Dirichlet peer sector is not generated by contracting the tied-replica law onto the replica coordinates' is FALSE whenever \u1e21\u22620. What is true is the sharper, correct statement the claim also makes: the contraction produces \u00bdh\u00b2I(D\u0304\u03b8,D\u0304\u03b8), the Fisher quadratic of the ROW-AVERAGED covariant derivative \u2014 still a Fisher-covariant Dirichlet form \u2014 rather than PIFB2's \u00bdh\u00b2\u03a3\u03c0_jI(D_\u03bcj\u03b8,D_\u03bcj\u03b8). Total cancellation requires \u1e21\u22610, i.e. a symmetric neighbour set AND a symmetric row."
}

### 4

{
  "attack": "VECTOR 6 / TAUTOLOGY \u2014 Statement (2) is the previously-closed theorem restated at C_h=id, applied to a microscopic law that was reverse-engineered from PIFB2, and release.json's obligation #1 explicitly demands a family specified INDEPENDENTLY of the PIFB2 ansatz.",
  "verdict": "WEAKENS_SCOPE",
  "reasoning": "Statement (2) hypothesizes that c_a retains (J^q_a,J^s_a) TOGETHER WITH (K_a,M_a,X_a,Y_a) \u2014 i.e. all six coordinates \u2014 so on standard Borel spaces c_a is a bimeasurable relabeling of the identity and nothing is coarse-grained. The resulting F^{X,(3)} = D_KL(Q_h\u2016\u03a0_{h,o}) - log p_h(o) is exact-elbo-proof.md:141-147 verbatim; I reproduced it to |diff| = 0.00e+00 on a 2-agent K=3,M=2,J=2 model. The microscopic law itself was constructed to have this ELBO (typed-construction.md:87-88 calls the product across a 'an existential witness'; exact-elbo-proof.md:120-134 defines F^{lag,1}_{PIFB2,h} as the assembled display minus I_\u03b6). release.json's first unresolved obligation reads 'Specify the intended normalized microscopic section-variable family INDEPENDENTLY of the PIFB2 ansatz' \u2014 the tied-replica law is not independent of it. Finding \u03b5=0 for the law engineered to give PIFB2 is circular as a test of whether PIFB2 is an effective action. The claim is honest about this ('nothing has been coarse-grained'), so it is a scope issue, not a false statement; but statement (2) contributes no new content."
}

### 5

{
  "attack": "VECTOR 7 / SCOPE INFLATION \u2014 The claim asserts it discharges final-report.md:55 ('compute or bound its exact generated interaction coordinates'). That obligation is anaphoric on the family of final-report.md:53-54, which the claim concedes it does not supply.",
  "verdict": "WEAKENS_SCOPE",
  "reasoning": "final-report.md:53-55 reads: 'Specify one normalized microscopic family whose slow variables are genuine sampled belief/model sections rather than recognition parameters. / Compute or bound ITS exact generated interaction coordinates.' The pronoun binds to the family of the first bullet. The claim's \u00a77 correctly concedes that first bullet is undischarged (P_h^n has no law-valued coordinates), and then asserts the second is discharged. Computing the interaction coordinates of a DIFFERENT family does not discharge an obligation about that family. Compounding this, statement (1)'s conclusion is vacuous by construction: it proves only that a product law composed with a blockwise map pushes forward to a product. Nothing is established about any law with genuine cross-agent coupling \u2014 which is the entire content of CE-1/CE-2 (adversarial-counterexamples.md:4-9). The claim admits the probe is trivial but still books the obligation as discharged."
}

### 6

{
  "attack": "VECTOR 1 / HIDDEN HYPOTHESIS \u2014 Statement (1) invokes the Hoeffding\u2013M\u00f6bius Banach space of 07b:1193-1214, whose ambient space is L^\u221e(\u03bd_\u2113) with \u03bd_\u2113 a product of PROBABILITY laws (07b:1143). Neither condition holds for the references the claim itself declares.",
  "verdict": "REPAIRABLE",
  "reasoning": "07b:1204 defines H_{\u2113,A}=P_{\u2113,A}L^\u221e(\u03bd_\u2113) and 07b:1143 states 'each \u03bd_{\u2113i} is a probability law'. (i) The level-3 reference \u03bd_a=(p_a\u2297r_a)\u2297(unif\u2297\u03bb_a)\u2297(unif\u2297\u03bc_a) contains \u03c3-finite \u03bb_a,\u03bc_a, so it is not a product probability and (H6) \u2014 which the claim scopes to statement (1) \u2014 is violated by the claim's own levels 2 and 3. (ii) S_h \u2208 L^\u221e(\u03bd_h) is nowhere assumed and fails generically: S_a \u2283 -log u_aj(x), unbounded for any source with unbounded support (all Gaussians), and \u222b|log u_aj|d\u03bb_a = \u221e under Lebesgue, so even C_{\u2113,B}S_h of 07b:1185-1188 is undefined and \u2016S_h\u2016_G is not a number. (iii) The claim's Corollary proof uses the ANCHORED M\u00f6bius form \u03a3_{B'\u2286B}(-1)^{|B|-|B'|}S(x_{B'},x\u00b0_{B^c}), which is NOT the definition at 07b:1193-1200 (conditional integration) and evaluates the a.e.-defined S on a \u03bd_h-null slice when the marginals are atomless. (iv) (H6) is claimed 'SATISFIED here by construction because \u03a0_{h,o} is itself a product' \u2014 false: equivalence (C_h)_#\u03a0 ~ \u03bd_h additionally requires \u03bb_a \u226a \u016b_a (level 2) resp. \u03bb_a \u226a u_aj for all j (level 3), which no stated hypothesis gives (take \u03bb_a = Lebesgue on R with all u_aj supported on [0,1]). All repairable by restricting to finite retained coordinate spaces with counting/uniform references, where S_h \u2208 L^\u221e automatically; the elementary conclusion 'S is a sum of one-body terms' never needed the machinery."
}

### 7

{
  "attack": "VECTOR 4 / NORMALIZATION \u2014 c_h is convention-split, and the two levels are not compared under one convention: statement (2) reports c_h=0 while the very convention statement (3) introduces makes it nonzero at level 3 too.",
  "verdict": "WEAKENS_SCOPE",
  "reasoning": "At level 3 e^{-S^PIFB_a} = \u2113_a(o_a|k,m)\u03c0^q_{aj}u_aj(x)\u03c0^s_{a\u2113}v_a\u2113(y), whose \u03bd_a-integral is p_a(o_a)/(|J^q_a||J^s_a|) \u2260 1. So under the NORMALIZED convention c_a = -log p_a(o_a) + log|J^q_a| + log|J^s_a| \u2260 0, not 0 as statement (2) asserts; '0' holds only under the unnormalized convention where c_h \u2261 0 by fiat \u2014 which is precisely the tautology (construction-or-strongest-theorem.md:14-24) the target was written to remove. Separately, the reading in \u00a76 that 'the peer sector IS, to leading order, precisely the additive constant c_h' cannot hold as a functional statement: c_a = -log\u222b\u220fu_aj^{\u03c0_aj}d\u03bb_a does not depend on q_a, while \u03a3_j\u03c0_jD_KL(q_a\u2016u_aj) does. The correct, exact, hypothesis-free identity is \u03a3_j\u03c0_jD_aj = D_KL(q_a\u2016PoE_a) + c_a with PoE_a = \u220fu_aj^{\u03c0_aj}/Z^q_a (verified 0/20000 violations; e.g. peer 1.0595833396 = 0.7258547294 + 0.3337286102) \u2014 this is boundary-counterexamples.md:16-37's own product-of-experts identity. The 'constant' reading is true only at the single recognition point around which (H7) is expanded. The positive normalization claims DO hold: Z^q_a \u2264 1 by generalized H\u00f6lder (0/20000 violations) and \u03b5_a \u2264 0 by AM\u2013GM (0/20000 violations)."
}

### 8

{
  "attack": "VECTOR 5 / LEVEL CONFUSION \u2014 At level 2 the attention row \u03b2 is integrated out of the RECOGNITION law as well, so the level-2 'effective theory' has no attention variable at all. The negative result is then about deleting PIFB2's central variable, not about coarse-graining.",
  "verdict": "WEAKENS_SCOPE",
  "reasoning": "R^{(2)}_h = \u2297_a \u03b6_a\u2297q_a\u2297s_a contains no \u03b2, \u03b3. The full objective is unchanged \u2014 the claim's own consistency identity (which I verified is a POINTWISE identity, hence unconditional: D_KL(q\u2016\u016b) + \u03a3_j\u03b2_j log(\u03b2_j \u016b/\u03c0_j u_j) = D_KL(\u03b2\u2016\u03c0) + \u03a3_j\u03b2_j log(q/u_j)) shows the peer sector simply migrates into the discarded conditional KL E_q D_KL(\u03b2_a\u2016\u03c0^{q,post}_a(\u00b7|X)). So (6)'s 'the residual cancels the retained peer sector' is a statement about how a deliberately lossy projection PARTITIONS the ELBO, not about the ELBO. Separately, S^PIFB_{a,rel}(x) := \u03a3_j\u03c0_ajE_aj(x) freezes a recognition variable (\u03b2) at the generative prior \u03c0 to obtain a state function. That freezing is a stipulation, not a derivation: freezing instead at PIFB2's own optimizer \u03b2*_j \u221d \u03c0_j e^{-D_j}, or comparing against the envelope-reduced row -log \u03a3\u03c0_j e^{-D_j} (PIFB2.tex:717-733, which is what PIFB2 actually is after optimizing \u03b2), gives different residuals of different sign. The theorem never shows \u03c0 is canonical, minimal, or an orthogonal projection, so 'THE residual' is determinate only relative to an undeclared normative choice. (The leading-order cancellation in (6) is robust to this choice, since \u03b2*_j = \u03c0_j(1+O(h\u00b2)).)"
}

### 9

{
  "attack": "VECTOR 2 / ORDER OF LIMITS \u2014 h\u21920 is exchanged with E_{q_a}, with the sum over h^{-d} edges, and (H7) silently tethers the variational variable q_a to the lagged field.",
  "verdict": "REPAIRABLE",
  "reasoning": "The claim admits the edge-uniformity gap ((H7)'s O(h\u00b3) remainders are never claimed uniform at lattice-continuum-asymptotics.md:4-9). Two further points it does not flag. (i) (H7) posits log u_aj = log q_a + hg_j + ..., which constrains the RECOGNITION variable q_a to lie within O(h) of the transported lagged neighbours. So (6) holds on a shrinking neighbourhood of the consensus manifold, not on 'bounded-energy sublevels' as final-report.md:56 demands; the claim's own conclusion that obligation (3) must be restated in a relative norm is correct but understates this. (ii) (H7) as stated only supports O(h\u00b3) remainders, whereas the O(h\u2074) conclusion needs the expansion one order further with a q_a-dominating function. This one is fixable and in fact the result is STRONGER than claimed: writing f_j = hg_j+h\u00b2t_j+h\u00b3s_j, per-source normalization E_q e^{f_j}=1 forces E_q t_j = -\u00bdE_q g_j\u00b2 and E_q s_j + E_q g_j t_j + \u2159E_q g_j\u00b3 = 0 order by order; since \u1e21\u22610 makes M-1 = O(h\u00b2) so log M = (M-1)+O(h\u2074), both the h\u00b2 and h\u00b3 coefficients of -E_q log M vanish IDENTICALLY by linearity of the j-average over those constraints \u2014 no lattice odd-symmetry needed. Confirmed numerically on a non-symmetric balanced-in-mean row (J=3, \u03c0=1/3, m=(+1,+1,-2), \u1e21\u22610): D/h\u2074 \u2192 0.9155, 0.9772, 0.9942, 0.9985."
}

### 10

{
  "attack": "VECTOR 1 / HIDDEN HYPOTHESIS \u2014 several derivations add and subtract the differential entropy H_\u03bb(q_a) = -E_q log q_a, which may be \u00b1\u221e, producing \u221e-\u221e.",
  "verdict": "REPAIRABLE",
  "reasoning": "The ordering theorem's proof writes E_{q_a}E_aj(X) = D_aj + H(q_a) and cancels H(q_a) across the Jensen chain; \u00a73c's assembly writes \u03a3_j\u03b2_aj E_{q_a}E_aj - H(q_a) = \u03a3_j\u03b2_aj D_KL(q_a\u2016u_aj); \u00a75 writes 'its q_a-expectation is \u03a3\u03c0_aj D_aj + H(q_a), the entropy being absorbed by -H_\u03bd(R)'. Under a \u03c3-finite \u03bb_a the differential entropy can be infinite while every KL is finite, and then each of these is \u221e-\u221e. Also (H4) assumes only q_a \u226a u^n_aj, which does NOT imply D_aj < \u221e. All three results survive with entropy-free proofs \u2014 for the ordering theorem set \u03c1_j = u_j/q, \u1ebc_j = -log \u03c1_j with E_q \u1ebc_j = D_j, then D_KL(q\u2016\u016b) = E_q \u03a8(\u1ebc) \u2264 \u03a8(E_q \u1ebc) = -log \u03a3\u03c0_j e^{-D_j} by concavity of \u03a8 = -lse alone, no entropy appears. Likewise \u03b5_a(x) = -D_KL(\u03c0^q_a\u2016\u03c0^{q,post}_a(\u00b7|x)) is a POINTWISE algebraic identity (verified to 1e-9 over 20000 random trials), so the 'exact expectation' formula holds unconditionally in [-\u221e,0] and does not need the finiteness the claim's derivation route through \u00a73b requires. The chain D_KL(q\u2016\u016b) \u2264 -log \u03a3\u03c0_j e^{-D_j} \u2264 \u03a3\u03c0_j D_j with right-minus-middle = D_KL(\u03c0^q_a\u2016\u03b2*_a) is correct: 0/20000 violations."
}

### 11

{
  "attack": "VECTOR 3 / ASYMMETRY OF KL \u2014 was the third-order term computed, and does argument order matter?",
  "verdict": "FAILS_TO_LAND",
  "reasoning": "The third-order term is not computed in the claim ((H7) stops at O(h\u00b3) remainders), so the O(h\u2074) assertion is under-derived AS WRITTEN \u2014 but the term genuinely vanishes, by the normalization argument above, and I confirmed it numerically on a row with nonzero third source-moment (m=(+1,+1,-2), \u03a3m_j\u00b3 = -6 \u2260 0, still O(h\u2074)). On argument order: every result is stated for the mode-seeking direction D_KL(q_a\u2016u_aj), matching exact-elbo-proof.md:64-83; the AM\u2013GM sign of \u03b5_a, the Jensen chain, and the H\u00f6lder bound Z^q_a \u2264 1 all depend on that order and would not transfer to D_KL(u_aj\u2016q_a). The claim never says so, but it never uses the wrong order either. No error lands here."
}

### 12

{
  "attack": "VECTOR 6 / TAUTOLOGY \u2014 is the genuinely novel piece (the 07b comparison) real?",
  "verdict": "FAILS_TO_LAND",
  "reasoning": "I checked this against the primary source and the claim is CORRECT and non-trivial. 07b:1816-1829 gives E^c_J = -\u03c4 log[(1/\u03c0^c_J)\u03a3_{j\u2208J}\u03c0_j e^{-E_j/\u03c4}] for coarsening a source label WITHIN the row functional, status ESTABLISHED; at \u03c4=1 and full merge with E_j = D_aj this is exactly -log \u03a3_j \u03c0_aj e^{-D_aj}, the middle term of the ordering chain. Eliminating the label from the underlying JOINT LAW instead yields D_KL(q_a\u2016\u016b_a), the left term. The two differ by the Jensen gap of \u03a8 = -lse along q_a, a quantity 07b does not compute; 07b:1811-1814 anticipates only the structure ('replacing it by one categorical row is a further coarse channel whose conditional KL appears in the chain rule'). This is the one genuinely new and fully correct contribution in the submission, and it is not what the theorem is titled about. Related: statement (0) (Lemma 0) and statement (3)'s equality criterion (\u03b5_a \u2261 0 iff u_aj = \u016b_a \u03bb-a.e. for all j \u2208 supp \u03c0, equivalently X_a \u22a5 J^q_a) are both correct as stated."
}

