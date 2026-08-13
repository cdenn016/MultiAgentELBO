# F5-u1-witness-adjudication

*Verbatim agent return, workflow wf_0b4620e2-7dc, 2026-08-13.*

## finding_id

5 — "The U(1) witness detects flat monodromy, not curvature or bundle topology"

## verdict

UPHELD

## severity

medium

## confidence

high

## restatement

The reviewer asserts four things. (i) Differential geometry: on C = S^1 with A = (Theta/2pi) dphi the curvature vanishes while the loop holonomy exp(i Theta) is nontrivial, and the principal U(1) bundle is trivial; hence the witness exhibits flat monodromy, not curvature and not bundle topology. (ii) Consequently the worklog's phrases "generates nontrivial holonomy iff A has curvature" (worklog:428), "the residual is not noise -- it is curvature" (:479), "consensus obstruction is topological ... frustration becomes a bundle invariant" (:480-483) are too strong. (iii) Code allegation: the statistic actually implemented in docs/verification/u1_two_path_holonomy_witness.py is arccos(cos Theta), not the group element exp(i Theta), so it identifies Theta with -Theta. (iv) A direct countercheck found the Theta = pi/2 and Theta = 3pi/2 record-law orbits gauge-equivalent to numerical precision. The reviewer concedes the witness remains a valid existence demonstration that putting transport inside the generative source separates the trivial from the selected nontrivial case, and asks only that the claim language be narrowed.

## superseded_status

NOT superseded, NOT answered. Section 4b of the worklog (lines 693-1112) is silent on section 3d and on the U(1) witness: grepping lines 693-1112 for 'holonom' returns zero hits, and the only 'curvature'/'topology' hits are the T-CURV Fisher-dressed energy and a Gamma-convergence 'interpolation topology'. Section 4b's targets are T-GRAD (4.1), T-CURV (4.2), T-RESID (4.3), T-COEF (4.4), T-SIMUL (4.5), Panel B (4.6), and the hand-written synthesis (4.7, lines 1069-1112) lists 'what moved' as items 1-4, none of which is section 3d. The 16 panel returns in docs/audits/panels-2026-08-12/ likewise never touch the witness: 'holonom' appears in only 6 of 17 files and always in unrelated contexts (T-CURV plaquette expansion; ground-01's finding that PIFB2's deployed Omega_ij is a flat Cech coboundary with vanishing holonomy, panelA-ground-01:21,361). So the reviewer's finding stands unaddressed by the new material. Section 4b does, however, CORROBORATE the reviewer from the other side: worklog:810-811 records the genuine curvature statement D_KL(q||(H_P)_# q) = (1/2) h^4 ||F_munu(c).q||^2_{g^F(q)} + O(h^5) as a PLAQUETTE expansion -- which requires a 2-dimensional base and therefore cannot be witnessed on S^1 at all. 4b thus independently confirms that curvature lives where the reviewer says it lives, and not where the witness sits.

## evidence

### 1

(a) CODE, cited and quoted. docs/verification/u1_two_path_holonomy_witness.py:149-154 defines the statistic: `def separating_statistic(Theta, gauge_i=0.0, gauge_j=0.0):` ... `(m1, _), (m2, _) = record_law_components(Theta, gauge_i, gauge_j)` / `c = np.dot(m1, m2) / (np.linalg.norm(m1) * np.linalg.norm(m2))` / `return np.arccos(np.clip(c, -1.0, 1.0))`. Since m1 = R(a_direct) MU_J and m2 = R(a_around) MU_J with |MU_J| = 1 and a_direct - a_around = Theta exactly (transport_angles, :81-85), the returned value is arccos(cos Theta) identically. The docstring on :151 nonetheless asserts 'it equals the holonomy'. The reviewer's allegation (iii) is literally correct.

### 2

(a) RECOMPUTED, not merely read. I evaluated separating_statistic against arccos(cos Theta) at Theta in {0, pi/8, pi/4, pi/2, pi, 5pi/4, 3pi/2, 2pi}: max |difference| = 4.4e-16 (machine zero) across all eight. At Theta = 5pi/4 the statistic returns 2.3561944902 = 2pi - 5pi/4, i.e. the fold is explicit. Scratch script at C:\Users\CHRISA~1\AppData\Local\Temp\claude\C--Users-chris-and-christine-Desktop-MultiAgentELBO\c87a5256-fdb7-4d07-a3d8-c6455d784e89\scratchpad\f5_check.py (outside the repo; no repository file was modified).

### 3

(b) EXECUTED. I ran `python docs/verification/u1_two_path_holonomy_witness.py` to completion: all four checks PASS and the printed table reproduces worklog:526-534 digit for digit, including orbit distance 0.3190849227 and statistic 1.570796 at BOTH Theta = pi/2 and Theta = 3pi/2. The reviewer's cited coincidence is real, not a transcription error.

### 4

(b) DECISIVE RECOMPUTATION -- the coincidence is a property of the RECORD LAWS, not only of the statistic. I computed orbit_distance(pi/2, 3pi/2) directly on the full mixture densities (TV minimized over the gauge circle, 720 samples): 1.056e-16. A refined bounded minimization over the gauge angle gives g* = 2.35619449 = 3pi/4 with TV = 1.33e-09. The component mean angles are {22.5 deg, 292.5 deg} at Theta = pi/2 and {67.5 deg, 157.5 deg} at Theta = 3pi/2; adding 135 deg to the first set and swapping labels returns the second exactly. So p(.|pi/2) and p(.|3pi/2) are the SAME point of the gauge quotient. This is stronger than what the reviewer wrote: on this design no observable whatsoever -- oriented or not -- can separate Theta from -Theta, because the two record laws are literally gauge-equivalent.

### 5

(b) LOCATED THE ROOT CAUSE. The culprit is PI_ROW = np.array([0.5, 0.5]) at script:78 combined with both paths pushing forward the SAME q_j. With equal weights the mixture is an unordered pair {R_{a1} q_j, R_{a2} q_j}, whose only gauge-orbit invariant is the unsigned angle |a1 - a2| = arccos(cos Theta). arccos(cos Theta) is therefore the COMPLETE invariant of the design -- the statistic is optimal, the design is deficient. I confirmed this by breaking the label symmetry: with PI_ROW = (0.7, 0.3), orbit_distance(pi/2, 3pi/2) = 2.3496e-01 > 0; with (0.9, 0.1) it is 7.84e-02 > 0; with (0.5, 0.5) it is 1.06e-16. A signed statistic arctan2(m2 x m1, m1.m2) returns -1.570796 at Theta = pi/2 and +1.570796 at Theta = 3pi/2 with gauge drift 8.9e-16 over 200 random gauges -- but it is only a legitimate RECORD statistic once the weights are unequal, since with equal weights the labeling is unidentifiable from p(o|Theta).

### 6

(c) MATHEMATICS, checked from first principles and symbolically. On any 1-manifold Lambda^2 T*M = 0, so F = dA (abelian) vanishes identically for EVERY connection on S^1, not merely for A = (Theta/2pi) dphi. The base was chosen so that curvature is not merely absent but untestable in principle. Meanwhile the holonomy is exp(i * int_0^{2pi} (Theta/2pi) dphi) = exp(i Theta), which sympy confirms integrates to Theta; nontrivial for Theta not in 2pi Z. So nontrivial holonomy with zero curvature -- flat monodromy -- exactly as the reviewer says.

### 7

(c) BUNDLE TOPOLOGY. Principal U(1) bundles over a base B are classified by H^2(B; Z); H^2(S^1; Z) = 0. Equivalently, principal G-bundles over S^n are classified by pi_{n-1}(G), and pi_0(U(1)) = 0 since U(1) is connected. Every principal U(1) bundle over S^1 is trivial. The moduli of flat U(1) connections mod gauge is Hom(pi_1(S^1), U(1)) = Hom(Z, U(1)) = U(1), a CONTINUUM -- so Theta varies continuously over a fixed trivial bundle. It is therefore not a discrete/topological invariant and emphatically not a bundle invariant.

### 8

(c) VERDICT ON THE THREE WORKLOG PHRASES. worklog:428 'generates nontrivial holonomy **iff** A has curvature' -- the 'if' half is true (Ambrose-Singer: F nonzero at a point implies nontrivial restricted holonomy), the 'only if' half is FALSE, and it is precisely the half the witness relies on. worklog:479 'The residual is *not noise* -- it is curvature' -- false on S^1; the residual is the monodromy of a flat connection. worklog:483 'Frustration becomes a bundle invariant' -- false here; it is a modulus of the flat connection mod gauge, a point of Hom(pi_1(C),G)/conj, on a bundle that is trivial with c_1 = 0. The language is defensible only on a base with genuine curvature (dim >= 2, e.g. T^2) or nontrivial H^2 (T^2, S^2). Note that worklog:585-586 (obligation 2) itself offered 'C = S^1 or T^2'; S^1 is the one choice that can test neither curvature nor topology.

### 9

(d) THE SPECIFIC SENTENCE. worklog:544-545 reads 'Both are Aut_G(P)-invariant, and for abelian U(1) the statistic *is* the holonomy (conjugacy class = element).' Given (a) and (b) this is FALSE AS IMPLEMENTED. The implemented statistic determines only the unordered pair {e^{iTheta}, e^{-iTheta}} -- the O(2) conjugacy class, not the U(1) element. The same false clause propagates verbatim to the script docstring (:151, :217-218, :314-315) and to overview.md:182 ('the separating statistic is Aut_G(P)-invariant to 10^-15 and equals the holonomy'), which the reviewer did not flag.

### 10

SCOPE OVERCLAIM the reviewer did not fully draw out. B4 (docs/audits/ultradeep-wave2-2026-08-12/wave2-01-constructions.md:695-713) makes a THREE-clause negative -- no record statistic detects holonomy, curvature, OR bundle topology -- and its own topology counterexample (F4, wave2-01:674-680) is C = S^2, U(1), Hopf bundles of distinct c_1. The S^1 witness defeats only the holonomy clause, and only for flat monodromy. Yet worklog:466-468 and overview.md:151 record B4 as simply 'Defeated for curve-mediated transport', unqualified as to which clause.

### 11

WHAT SURVIVES INTACT. The separating tuple that appendix_claim_ledger.tex:242-256 requested -- named bundle and connection, assigned base loop, gauge-invariant record statistic, two connection data with distinct holonomy conjugacy classes and differing record laws -- IS genuinely exhibited at Theta = 0 versus Theta = pi/2 (orbit distance 0.3190849227, reproduced by me). Check 3 (flat coboundary, TV = 0 to machine zero) and check 4 (ELBO identity, |LHS-RHS| = 5.5e-13) also reproduce and are unaffected. The defect is in the claim language and in one design choice, not in the existence result.


## recomputation

Ran the repository script end to end (all four checks PASS; table reproduces worklog:526-534 exactly). Independently recomputed, in a scratch script outside the repo: (1) separating_statistic minus arccos(cos Theta) = at most 4.4e-16 over eight values of Theta including 5pi/4 and 3pi/2 -- the statistic IS arccos(cos Theta); (2) orbit_distance(pi/2, 3pi/2) = 1.056e-16 on the full record laws, with the optimal gauge angle refined by bounded minimization to g* = 2.35619449 = 3pi/4 giving TV = 1.33e-09, and component mean-angle sets {22.5, 292.5} deg and {67.5, 157.5} deg related by a 135 deg rotation plus label swap -- so the coincidence lives in the RECORD LAWS, not only in the statistic; (3) symmetry-breaking test: orbit_distance(pi/2, 3pi/2) = 1.06e-16 at pi_J = (0.5,0.5), 2.3496e-01 at (0.7,0.3), 7.84e-02 at (0.9,0.1) -- the equal-weight prior at script:78 is the root cause; (4) a signed gauge-invariant angle arctan2(m2 x m1, m1.m2) returns -pi/2 and +pi/2 at Theta = pi/2 and 3pi/2 with gauge drift 8.9e-16; (5) sympy: int_0^{2pi} (Theta/2pi) dphi = Theta, so holonomy = exp(i Theta), while F = dA vanishes identically because Lambda^2 T*S^1 = 0 for every connection. Bundle triviality argued from H^2(S^1;Z) = 0 and pi_0(U(1)) = 0 (standard classification, not recomputed).

## reviewer_missed

Three things the reviewer got imprecise or missed, and one thing understated in the programme's favour. (1) FIX IS MISPRESCRIBED. The reviewer headlines the defect as a statistic defect and prescribes 'add an oriented/asymmetric observable'. That will not work: I verified the two record laws are themselves gauge-equivalent (orbit distance 1.06e-16), so on the equal-weight design NO observable of p(o|Theta) separates +Theta from -Theta. The repair must be a DESIGN change (unequal path priors, or otherwise distinguishable channels) before any oriented observable becomes a legitimate function of the record. The reviewer is right for a partly wrong reason on the remedy. (2) THE STATISTIC IS ACTUALLY OPTIMAL. arccos(cos Theta) is the complete gauge-orbit invariant of this equal-weight two-path design, so calling it 'weak' inverts the diagnosis: the statistic extracts everything the design contains. (3) MISSED THE VACUITY AND THE PROPAGATION. The reviewer did not note that F vanishes on S^1 for EVERY connection (not just this A), so the base makes B4's curvature clause untestable in principle and the worklog's own obligation-2 alternative 'S^1 or T^2' (worklog:585-586) picked the wrong one; nor that B4 is a three-clause negative whose topology clause is anchored at S^2 with distinct Chern numbers (wave2-01:674-680) and is untouched, while worklog:466-468 and overview.md:151 record B4 as flatly 'Defeated'; nor that the false 'equals the holonomy' clause also appears at overview.md:182 and at script:151, :217-218, :314-315. (4) UNDERSTATED IN THE PROGRAMME'S FAVOUR: the Theta = 0 versus Theta = pi/2 separation (orbit distance 0.3190849227) does genuinely furnish the separating tuple the ledger requested, with distinct holonomy conjugacy classes, so the existence claim itself survives fully. Additionally, the 3pi/2 row of the worklog table (worklog:533) is not independent evidence at all -- it is the pi/2 row's mirror image -- which the table presents as if it were a seventh data point.

## recommended_action

Make five text edits and one script edit; do not retract the existence witness. (1) worklog:544-545 -- delete 'for abelian U(1) the statistic *is* the holonomy (conjugacy class = element)'; replace with: 'the statistic implemented at u1_two_path_holonomy_witness.py:149-154 is arccos(cos Theta), which determines only the unordered pair {e^{iTheta}, e^{-iTheta}}. It is the complete gauge-orbit invariant of this equal-weight two-path design: the Theta = pi/2 and Theta = 3pi/2 record laws are gauge-equivalent (orbit distance 1.06e-16, at gauge angle 3pi/4), so the 3pi/2 row below is the pi/2 row mirrored and is not independent evidence.' Add the same footnote at the 3pi/2 row, worklog:533. (2) worklog:428 -- replace 'generates nontrivial holonomy **iff** A has curvature' with 'generates nontrivial holonomy whenever A is not gauge-trivial. Nonzero curvature implies nontrivial restricted holonomy (Ambrose-Singer); the converse is false -- a flat connection on a base with pi_1 nontrivial has nontrivial monodromy and identically zero curvature.' (3) worklog:479 -- 'The residual is *not noise* -- it is holonomy: the monodromy of A around gamma prime composed with gamma inverse. On a base of dimension at least 2 the infinitesimal version of the same residual is curvature (cf. the plaquette expansion at worklog:810-811).' (4) worklog:480-483 -- replace 'Frustration becomes a bundle invariant' with 'Frustration becomes an invariant of the flat connection modulo gauge, i.e. a point of Hom(pi_1(C),G)/conj. It is not a bundle invariant: in the witness the bundle is trivial (H^2(S^1;Z) = 0) and the holonomy varies continuously over the modulus space U(1).' (5) overview.md:182 and worklog:466-468 / overview.md:151 -- change 'equals the holonomy' to 'separates the holonomy up to Theta <-> -Theta', and qualify 'B4 defeated' as 'B4's HOLONOMY clause defeated, for flat monodromy only; B4's curvature and bundle-topology clauses are untouched, since F vanishes identically on any 1-dimensional base and every principal U(1) bundle over S^1 is trivial. Testing those requires C = T^2 (curvature and nontrivial H^2) or S^2 (Chern classes, matching B4's own F4 counterexample at wave2-01:674-680).' (6) SCRIPT, minimal change to make the element recoverable: set PI_ROW to an asymmetric prior such as np.array([0.7, 0.3]) at :78 (verified: orbit_distance(pi/2, 3pi/2) then equals 0.2350 > 0), and only then replace separating_statistic:149-154 with the signed angle np.arctan2(m1[0]*m2[1] - m1[1]*m2[0], m1 @ m2) (verified gauge-invariant to 8.9e-16). Add a comment recording that the signed statistic is NOT a function of the record law under equal weights, so the prior asymmetry is a prerequisite, not a cosmetic change. Optionally add a T^2 variant to test the curvature clause, but that is new work, not a repair.
