# F6-gl-no-go-adjudication

*Verbatim agent return, workflow wf_0b4620e2-7dc, 2026-08-13.*

## finding_id

FINDING-6 (full-GL invariant-form no-go worded too strongly)

## verdict

UPHELD

## severity

medium

## confidence

high

## restatement

The reviewer asserts three things. (1) The correct no-go is that gl(K,R) admits no POSITIVE-DEFINITE Ad-invariant inner product — i.e. no Ad-invariant form controlling every Lie-algebra direction. (2) The stronger claim actually written in worklog PA-2 (line 156) and overview.md:153 — that EVERY element of the 2-dimensional space of Ad-invariant symmetric bilinear forms on gl(K,R) is indefinite, with signature (3,1) at K=2 and (6,3) at K=3, hence that kappa||F_A||^2 "cannot be both gauge-invariant and nonnegative"/"bounded below" — is FALSE, because (tr X)(tr Y) is Ad-invariant and nonnegative, though degenerate. (3) A prediction, made blind: Fisher dressing can supply a nonnegative invariant STATE-DEPENDENT sector that is nevertheless stabilizer-degenerate and noncoercive along noncompact gauge orbits. The proposed fix is to state the positive-definite full-direction no-go, and to call compact type sufficient for the first coercive fixed-inner-product theory rather than necessary for every degenerate or state-dependent curvature functional.

## superseded_status

NOT superseded, and not answered. Worklog section 4b (lines 693-1112, new in 4dee0db) leaves PA-2 at line 156 textually untouched — I grepped the whole worklog for 'PA-2', 'positive-definite', 'Ad-invariant' and 'Killing'; the only hits are line 156 (the overstated PA-2 itself) and line 752 (an unrelated Fisher mass term). overview.md:153 and :195 are likewise unchanged at HEAD. Section 4b's synthesis at line ~1100 even asserts 'No returned result contradicts rm-01...rm-06', which is not quite right on this point: section 4.2 (worklog:798-836) records 'T-CURV — invariance proved for noncompact G', i.e. a gauge-invariant nonnegative curvature functional for GL(K,R), which contradicts the LITERAL reading of PA-2 ('cannot be both gauge-invariant and nonnegative') even though it does not contradict rm-04's correctly-worded finding K1 (rm-04:878-881). So section 4b partially CONFIRMS the reviewer from a second direction while failing to propagate the correction back to PA-2 and to overview.md. The panel returns docs/audits/panels-2026-08-12/panelA-T-CURV-derivation.md:23-35 and panelA-T-CURV-skeptic.md:33,41 independently CONFIRM the reviewer's part-(c) prediction in full. Nothing in the panels or in 4b refutes any part of Finding 6.

## evidence

### 1

LOCUS CONFIRMED (cited). The overstated text is live at HEAD (4dee0db). docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md:156 (PA-2 row; the review cited :146, drift of 10 lines) reads: 'kappa||F_A||^2 **cannot** be both gauge-invariant and nonnegative for G=GL(K,R). Ad-invariant symmetric bilinear forms on gl(K,R) form exactly a 2-dim space (tr(XY), trX trY); **every** element is indefinite — signature (3,1) for K=2, (6,3) for K=3. Exhaustive search.' overview.md:153 reads: 'kappa||F_A||^2 cannot be both gauge-invariant and bounded below for GL(K,R); all Ad-invariant forms on gl(K) are indefinite'. overview.md:195 reads 'Compact is kinematically necessary for the curvature sector and for coercivity.'

### 2

SOURCE vs PARAPHRASE (cited). rm-04 is internally split and the worklog copied the wrong half. docs/audits/roadmap-review-2026-08-12/rm-04-gauge-kinematics.md:45-46 (section 0(4), the headline) DOES say '...and **every** element of it is indefinite — signature (3,1) for K=2, (6,3) for K=3, no positive-definite combination (exhaustive search, sec 1.5)'. But the actual computation it points to, rm-04:285-288, reports only: 'signature of tr(XY): 3 positive, 1 negative => INDEFINITE / any positive-definite combination a*tr(XY)+b*trX trY ? -> NONE'. The script ledger at rm-04:984 records the same: 'exhaustive 61x61 search for a **positive-definite** combination ... NONE positive definite'. The ranked finding K1 at rm-04:878-881 is likewise correctly worded ('tr(XY) has signature (3,1)... with no positive-definite combination'). So rm-04 PROVES the positive-definite no-go and only its section-0 headline sentence overstates it to 'every element is indefinite'. Worklog PA-2 faithfully paraphrases the overstated headline rather than the correct body/finding. The reviewer's diagnosis of the defect is exactly right, and the reviewer located the right file and the right sections.

### 3

RECOMPUTED (executed, decisive). I built the Gram matrix of B_{a,b}(X,Y)=a tr(XY)+b trX trY in the E_ij basis of gl(K,R) for K=2,3 and independently solved the Ad-invariance linear system B([Z,X],Y)+B(X,[Z,Y])=0 over all basis Z. Results: dim{Ad-invariant symmetric forms} = 2 for both K, and its span coincides with span{tr(XY), trX trY} (joint rank 2). Signatures (+,-,0): tr(XY) -> (3,1,0) at K=2 and (6,3,0) at K=3, reproducing rm-04 exactly. (trX)(trY) -> (1,0,3) at K=2 and (1,0,8) at K=3: rank 1, NONNEGATIVE, radical of dimension K^2-1 = dim sl(K,R). Ad-invariance of (tr X)^2 verified numerically: max |(tr g^{-1}Xg)^2 - (tr X)^2| = 2.8e-14 (K=2) and 2.4e-13 (K=3) over 200 random g in GL(K,R). The reviewer's counterexample is therefore correct as stated.

### 4

RECOMPUTED (executed, measure-zero character). Scanning the projective family (a,b)=(cos t, sin t) over 4001 directions including t=pi/2 exactly: at K=2, 4000 directions are INDEFINITE and exactly 1 is PSD-degenerate (a=0, b=1; signature (1,0,3)); at K=3, 4000 INDEFINITE and exactly 1 PSD-degenerate (signature (1,0,8)). Zero positive-definite directions at either K. So 'every element is indefinite' fails on precisely one line out of a 2-dimensional space — a genuine but measure-zero exception. A 20001-point scan that MISSED a=0 (pi/2 is not on that grid) returned 'indefinite = 20001', which is exactly how rm-04's 61x61 grid search could report 'no positive-definite combination' without ever noticing the semi-definite line.

### 5

RECOMPUTED (executed, two-line proof of the correct statement). Take S=E_12+E_21 and A=E_12-E_21. Both are traceless (verified: trS=trA=0 at K=2,3), so the b-term drops out, and tr(S^2)=+2, tr(A^2)=-2 (verified). Hence B_{a,b}(S,S)=+2a and B_{a,b}(A,A)=-2a have opposite signs for every a != 0. Therefore: a != 0 => indefinite for every K>=2; a = 0 => rank 1, semi-definite. That is a complete classification and it is exactly the reviewer's claim. Corollary check: the degenerate-but-indefinite locus a+bK=0 (which contains the Killing form B(X,Y)=2K tr(XY)-2 trX trY quoted at panelA-T-CURV-derivation.md:151) computes to signature (2,1,1) at K=2 and (5,3,1) at K=3 — degenerate on the center, still indefinite. Confirmed numerically.

### 6

WHAT THE EXCEPTION BUYS (recomputed + reasoned). The nonnegative form b(trX)(trY) has radical exactly sl(K,R), so as a curvature term b(tr F_{munu})(tr F^{munu}) it is Maxwell for the determinant line bundle det(E) and nothing else: it controls 1 of K^2 Lie-algebra directions and vanishes IDENTICALLY on any sl(K)-valued connection (verified: tr of a commutator of traceless matrices = 0.0 exactly). So the reviewer's counterexample destroys the LITERAL wording of PA-2 and overview:153 while leaving their OPERATIVE conclusion intact: no fixed Ad-invariant form on gl(K,R) is simultaneously nonnegative and nondegenerate, hence no fixed-inner-product kappa||F_A||^2 is both gauge-invariant and coercive on the non-abelian sector. This is why I rate the finding medium and not high.

### 7

PREDICTION (c) — CONFIRMED, AND IT IS A CLEAN BLIND HIT (cited). The panel returns are NEW in 4dee0db: `git ls-tree -r caa4a15 | grep -c panels-2026-08-12` returns 0, so the reviewer could not have read them. Reviewer: 'Fisher dressing can likewise provide a nonnegative invariant state-dependent sector while remaining stabilizer-degenerate and noncoercive along noncompact gauge orbits.' Match, three for three: (i) NONNEGATIVE INVARIANT STATE-DEPENDENT — panelA-T-CURV-derivation.md:23-25 '(3) [FORMAL PROOF] ... <Ad_g Y, Ad_g Z>_{g_# q} = <Y,Z>_q ... requires no Ad-invariant inner product on g, no normalized Haar measure, and no compactness ... supplies a conjugation-invariant curvature energy for any closed subgroup of GL(K,R), including noncompact ones', and :20 'a Fisher-weighted, state-dependent Yang-Mills energy, not ||F||_F^2'. (ii) STABILIZER-DEGENERATE — panelA-T-CURV-derivation.md:31 '(4b) [FORMAL PROOF, degeneracy] rad<.,.>_q = g_q ... the isotropy algebra, iso so(K-1) if mu != 0 and so(K) if mu = 0', and :200 'which is exactly the Lie algebra of Stab_G(q)'. (iii) NONCOERCIVE ALONG NONCOMPACT GAUGE ORBITS — panelA-T-CURV-derivation.md:35 '(4d) [COUNTEREXAMPLE, coercivity] Unconditional coercivity FAILS', and the skeptic sharpens it to precisely the reviewer's phrasing at panelA-T-CURV-skeptic.md:33 'INVARIANCE AND COERCIVITY ARE STRUCTURALLY INCOMPATIBLE HERE ... the ellipticity ratio lambda_max/lambda_min is unbounded ON EVERY SINGLE GAUGE ORBIT', with the skeptic's net verdict at :41 describing the derived object as 'a matter-dressed, state-dependent, positive-semidefinite quadratic form on g, degenerate on the belief's isotropy algebra, with infimum zero over belief space in nilpotent directions, and with unbounded condition number along every gauge orbit'. The reviewer's one sentence is a compressed statement of the entire T-CURV outcome, written without access to it.

### 8

CROSS-CHECK: the derivation agent itself used the CORRECT wording, which is further evidence the worklog's is the outlier. panelA-T-CURV-derivation.md:151: 'What was NOT used: compactness; an Ad-invariant **positive-definite** form on g (none exists on gl(K,R) — the Killing form B(X,Y)=2K tr(XY)-2 trX trY is indefinite)'. That is the reviewer's preferred formulation verbatim, produced independently.

### 9

MINOR REVIEWER IMPRECISION (recomputed/reasoned). The proposed fix says 'Call compact type **sufficient** for the first coercive fixed-inner-product theory, not necessary'. For a FIXED positive-definite Ad-invariant form, compact type is necessary AND sufficient (a real Lie group admits an Ad-invariant inner product iff it is of compact type; gl(K,R) = sl(K,R) + R with sl(K,R) of noncompact type, hence none, consistent with my 0-positive-definite-directions scan). What compactness is NOT necessary for is a nonnegative DEGENERATE form or a STATE-DEPENDENT one. The fix should be worded accordingly.


## recomputation

Executed under the session scratchpad (no repo files touched), numpy float64, K=2 and K=3. (1) Solved the Ad-invariance system B([Z,X],Y)+B(X,[Z,Y])=0 by SVD over all basis Z: dim = 2 at both K, span = span{tr(XY), trX trY} (joint rank 2 with the two candidate Grams). (2) Signatures (#pos,#neg,#null): tr(XY) -> (3,1,0) at K=2, (6,3,0) at K=3 [reproduces rm-04:285-288 exactly]. (trX)(trY) -> (1,0,3) at K=2, (1,0,8) at K=3 -> NONNEGATIVE, rank 1, radical = sl(K,R). -(trX)(trY) -> (0,1,3)/(0,1,8), negative semidefinite. (3) Projective scan over 4001 directions (a,b)=(cos t,sin t) with t=pi/2 hit exactly: K=2 gives {INDEFINITE: 4000, PSD-DEGENERATE: 1}; K=3 gives {INDEFINITE: 4000, PSD-DEGENERATE: 1}; POSITIVE-DEFINITE: 0 at both K. A 20001-point scan that misses t=pi/2 reports 20001/20001 indefinite — reproducing how rm-04's grid search could miss the exception. (4) Ad-invariance of (tr X)^2 under 200 random g in GL(K,R): max deviation 2.8e-14 (K=2), 2.4e-13 (K=3). (5) Analytic classification confirmed numerically: S=E_12+E_21 and A=E_12-E_21 are traceless with tr(S^2)=+2, tr(A^2)=-2, so B_{a,b}(S,S)=2a and B_{a,b}(A,A)=-2a; a != 0 => indefinite, a = 0 => rank-1 semi-definite. Complete classification, no exhaustive search needed. (6) Degenerate locus a+bK=0: signature (2,1,1) at K=2, (5,3,1) at K=3 — this is the Killing form direction quoted at panelA-T-CURV-derivation.md:151; degenerate on the center and still indefinite. (7) tr of a commutator of traceless 3x3 matrices = 0.0 exactly, confirming that b(tr F)^2 vanishes identically on sl(K)-valued connections.

## recommended_action

Three edits, all wording-only; no mathematical result changes.

(1) Replace the PA-2 row at docs/research-plans/2026-08-12-elbo-to-continuum-action-worklog.md:156 with:
"**PA-2** | For G=GL(K,R), K>=2, there is **no positive-definite Ad-invariant inner product on gl(K,R)**, hence no fixed-inner-product kappa||F_A||^2 that is both gauge-invariant and coercive. The Ad-invariant symmetric bilinear forms are exactly the 2-dim space {a tr(XY) + b trX trY}. Complete classification (verified independently): with S=E_12+E_21 and A=E_12-E_21 traceless and tr(S^2)=+2, tr(A^2)=-2, every form with a != 0 is **indefinite** — signature (K(K+1)/2, K(K-1)/2) at b=0, i.e. (3,1) for K=2 and (6,3) for K=3, with the trace direction flipping sign across a+bK=0 (the Killing form 2K tr(XY)-2 trX trY sits on that degenerate locus). The **only** semi-definite elements are the line a=0, b>0: b(trX)(trY), which is Ad-invariant and nonnegative but has radical sl(K,R), i.e. it is Maxwell for the determinant line and vanishes identically on sl(K)-valued connections. So the correct no-go is *positive-definiteness*, not indefiniteness of every element. | `rm-04-gauge-kinematics.md` §1.5 and finding **K1** §8 (NOTE: rm-04's §0(4) headline says 'every element is indefinite'; its own computation at :285-288 and its finding K1 at :878-881 establish only 'no positive-definite combination', which is the correct and sufficient statement) | Compact type is a kinematic necessity **for a coercive fixed-inner-product curvature sector** — indeed necessary and sufficient for a definite Ad-invariant form — and belongs in T0 in that scope. It is **not** necessary for gauge invariance or nonnegativity as such: see §4.2, where a state-dependent Fisher-dressed form is exactly invariant for noncompact G, at the cost of being degenerate on the isotropy algebra and noncoercive along gauge orbits."

(2) Replace overview.md:153 with:
"| **Yang-Mills indefiniteness** | gl(K,R) admits no positive-definite Ad-invariant inner product; the invariant forms are span{tr(XY), trX trY} and every nondegenerate one is indefinite. The only nonnegative one, (trX)(trY), has radical sl(K,R) and sees only the determinant line. So no fixed-inner-product kappa||F_A||^2 is both gauge-invariant and coercive for GL(K,R) | `rm-04` §1.5, K1 §8; state-dependent escape at worklog §4.2 |"

(3) Replace overview.md:195 with:
"3. **Compact G vs full GL(K).** Compact type is necessary and sufficient for a **fixed** Ad-invariant positive-definite form, hence for a coercive fixed-inner-product curvature sector, and it is separately required for gauge-invariant coercive confinement (PA-3). It is **not** required for gauge invariance or nonnegativity of the curvature sector as such: §4.2's Fisher-dressed form is exactly invariant for noncompact G but is degenerate on the belief's isotropy algebra and noncoercive along gauge orbits."

Do NOT edit docs/audits/roadmap-review-2026-08-12/rm-04-gauge-kinematics.md — it is an archived verbatim referee return. Its §0(4) overstatement should be recorded as an erratum inside the worklog's PA-2 source column (as drafted above), consistent with how the repo treats other archived audits."
