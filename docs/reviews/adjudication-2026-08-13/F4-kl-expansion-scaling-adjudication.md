# F4-kl-expansion-scaling-adjudication

*Verbatim agent return, workflow wf_0b4620e2-7dc, 2026-08-13.*

## finding_id

FINDING 4 — "The local KL expansion does not prove the displayed global continuum estimate" (docs/reviews/2026-08-12-pifb2-elbo-program-interim-theory-review.md:57-65)

## verdict

UPHELD_BUT_NARROWED

## severity

low

## confidence

high

## restatement

The reviewer concedes that the local coefficients (1/2 g^F h^2 + 1/3 T_skew h^3) and (1/2 g^F h^2 + 1/6 T_skew h^3) reproduce exactly, then makes seven separable assertions. (1) docs/verification/kl_expansion_check.py cancels s(h)+s(-h) at ONE CENTER only. (2) It does not define edge orientation and multiplicity. (3) It does not treat boundaries. (4) It does not prove a Riemann-sum theorem. (5) It does not close the transported (covariant) case. (6) A one-direction (oriented) Poisson edge sum has O(h), not O(h^2), global error. (7) The exact finite ELBO block lacks the required h^(d-2) coefficient, so its unweighted sum has the desired finite scaling only in d=2, unless a new normalized construction supplies that coefficient and its normalizers. The prescribed fix: state only a flat local consistency expansion; define a bidirected/symmetrized stencil; derive the mesh coefficient probabilistically; prove the global covariant limit separately.

## superseded_status

PARTLY SUPERSEDED by section 4b, with two pieces surviving. SUPERSEDED: sub-claim (5), the covariant case, is closed by worklog section 4.1(i) (worklog:716-737) and the CLOSED note inserted at worklog:108-116; I verified the parity argument symbolically myself and it holds in both KL orientations, in a non-natural chart, independent of the second and third jets, exactly as panelA-T-GRAD-skeptic.md:49-55 (VECTOR 3, FAILS_TO_LAND) reports. ANSWERED: sub-claims (2) and (4) are answered by panelA-T-GRAD-derivation.md:23-33 -- (A)/(B) give the oriented and symmetric forms with explicit multiplicity and the (h^{d-2}/2) factor, (D) generalizes to an arbitrary edge set with second/third moments of the edge-displacement measure, and (H1)-(H7) plus Prop 2.2/Cor 2.3 supply the uniform remainder a Riemann-sum theorem needs. ANSWERED: sub-claim (3), boundaries, by panelA-T-GRAD-derivation.md:71 (torus, plus an O(h) boundary-layer estimate whose arithmetic I checked). CONFIRMED, not superseded: sub-claim (6) is the panel's own statement (A) at panelA-T-GRAD-derivation.md:23, arrived at independently and reproduced numerically by its skeptic at panelA-T-GRAD-skeptic.md:124-126 (Richardson -3.21927); my own runs reproduce O(h) oriented / O(h^2) symmetric in both the flat and covariant settings. CONFIRMED and constructively repaired: sub-claim (7) is exactly panelA-T-GRAD-derivation.md:39 (E), and the 'new normalized construction' the reviewer demanded is supplied at :41 (F) via integer replication licensed by boundary-counterexamples.md:57, audited for normalizers at panelA-T-GRAD-skeptic.md:100-102 and shown unavoidable at :108-110. NOT SUPERSEDED: (i) the script docs/verification/kl_expansion_check.py is unchanged at 4dee0db, so every structural criticism of THE SCRIPT still stands as written; (ii) worklog:97 and overview.md:162-164 still carry the un-narrowed 'h^{d-2} is forced' language and overview.md:164 is now doubly stale; (iii) the global covariant limit is proved pointwise only, with Gamma-convergence explicitly open at worklog:794-796.

## evidence

### 1

EXECUTED. `python docs/verification/kl_expansion_check.py` runs clean and reproduces every stated coefficient: Poisson/Bernoulli/Exponential all give h^2 -> 1/2*g^F and h^3 -> 1/3*T_skew (forward) / 1/6*T_skew (reverse); the Gaussian scale family gives fwd = t^2 + (2/3)t^3 + ..., rev = t^2 - (2/3)t^3 + ..., pair sum t^3 coefficient exactly 0. 'All assertions passed.' The reviewer's concession is correct.

### 2

CITED + RECOMPUTED, sub-claim (1) 'one center'. Partly WRONG in letter. kl_expansion_check.py:56-82 runs the cancellation at a FREE symbolic center `th`, so the h^3 cancellation is established for all centers, not one. kl_expansion_check.py:37-53 (the Gaussian scale family) is the only single-center check. But the substantive core of the criticism is CORRECT and stronger than the reviewer stated: line 80 computes `s + s.subs(h,-h)`, i.e. it takes the fibre parameter increment to be exactly +/-h. On a lattice the neighbours are theta(c+/-h) = theta(c) +/- h*theta' + h^2*theta''/2 +/- h^3*theta'''/6, so the acceleration and jerk of the section are never exercised. There is no section, no lattice, and no sum anywhere in the file.

### 3

CITED, sub-claims (2)(3)(4). All three CONFIRMED against the file. The script contains no edge set, no orientation convention, no multiplicity factor, no domain and no boundary, and no uniformity-of-remainder argument. Its concluding claim at kl_expansion_check.py:100-102 ('the h^{d-2}-weighted lattice sum converges to the Fisher Dirichlet energy with relative error O(h^2)') asserts a global theorem the file does not contain, and omits the counting factors that fix the constant. Multiplicity is load-bearing: panelA-T-GRAD-derivation.md:27 states the symmetric form as (h^{d-2}/2) * sum_c sum_mu [E_+ + E_-] -> (1/2)int||D^A q||^2, while panelA-T-GRAD-skeptic.md:86 states the beta-row-averaged unit-coefficient version at d=2 converges to (1/4)int||D^A q||^2. I checked these are mutually consistent (factor 1/(2d) vs factor 1/2), but they differ by a factor 2 from each other precisely because the convention differs -- which is exactly the reviewer's point.

### 4

CITED, sub-claim (5). CONFIRMED of the script, but the reviewer is restating the script's own scope note verbatim: kl_expansion_check.py:18-21 says 'SCOPE: flat / trivial-transport case only ... the odd/even cancellation must be re-established covariantly. That is not checked here.' Worklog:100-106 carried the same caveat. This was never a hidden defect.

### 5

RECOMPUTED, sub-claim (6) O(h) vs O(h^2) -- and the reviewer is right, but my first test REFUTED him before a second one confirmed him. d=1 circle, Poisson fibre, bond weight h^{d-2}=h^{-1}, theta(c)=0.4+0.6 sin 2pi c+0.25 cos 4pi c: the ORIENTED sum converged at fitted exponent 1.9998, identical to the symmetric sum to 10 digits. Reason (I derived it): that theta satisfies theta(1/2-c)=theta(c), so theta'^3 is odd about c=1/4 and the O(h) coefficient is annihilated by symmetry. Measured int A'''(theta) theta'^3 dc = 1.9e-15 for Poisson, 1.6e-16 for Bernoulli, 0 for the Gaussian scale family on that section.

### 6

RECOMPUTED, sub-claim (6) continued -- with a generic asymmetric section theta(c)=0.4+0.6 sin 2pi c+0.25 cos 4pi c+0.35 sin(6pi c+0.7): oriented fitted exponent 1.15 with err1/h -> -8.128 and stable, Richardson extrapolant -8.045468; symmetric fitted exponent 1.9996 with err2/h^2 -> -674.9 stable. I derived the flat 1-D oriented O(h) coefficient in closed form as -(1/12) int A'''(theta) theta'^3 dc = -8.045494, agreeing with the measured Richardson value to 5 significant figures. Sub-claim (6) is CONFIRMED, and sharpened: the O(h) coefficient is generically nonzero but vanishes on reflection-symmetric sections, so a single naive test can miss it.

### 7

RECOMPUTED, covariant version of (6). d=1 circle, N(mu,sigma^2) fibre, genuine GL(1)_+ connection A(c)=0.5+0.6 sin 4pi c, exact abelian holonomy exp(int A), Omega_{c,c+h} != Omega_{c,c-h}. Target (1/2)int||D^A q||^2_{g^F} = 4.088430292050. Oriented sum: fitted exponent 0.9859, err1/h -> 2.802 and NOT shrinking. Symmetric sum: fitted exponent 1.9999, err2/h^2 -> -11.639 stable. This is an independent confirmation of BOTH panelA-T-GRAD-derivation.md:23 (oriented = O(h), coefficient generically nonzero and not a total derivative) and :27 (symmetric = O(h^2)) in the covariant setting.

### 8

RECOMPUTED, task (c) -- the covariant parity argument, verified symbolically by me. In the deliberately NON-natural (mu,sigma) chart (so Gamma^(e) != 0), with the transported-back curve carried to third order, mu-hat(e)=mu0+e v1+e^2 w1/2+e^3 u1/6 and sigma-hat likewise with all six jet symbols free: f(0)=0 and f'(0)=0 in both KL orientations; the single-edge h^3 coefficient is generically nonzero (forward: (3 s v1 w1 + 6 s v2 w2 - 6 v1^2 v2 - 10 v2^3)/(6 s^3)); and the h^3 coefficient of E(+h)+E(-h) is IDENTICALLY 0 in both orientations, independent of w and u. Repeated for a generic one-parameter exponential family with an arbitrary chart curve th0 + a h + b h^2/2 + d h^3/6: single-edge h^3 = a^3 A'''/6 + a b A''/2 (nonzero), pair h^3 = 0 for all a,b,d. This reproduces panelA-T-GRAD-skeptic.md:49-55 (VECTOR 3, verdict FAILS_TO_LAND) exactly, including its shorter proof: f(eps):=D(theta_0, theta-hat(eps)) is one C^3 function of one variable with f(0)=f'(0)=0, so f(h)+f(-h) is even.

### 9

RECOMPUTED, bonus -- I independently confirm the skeptic's own correction to the derivation (panelA-T-GRAD-skeptic.md:57-62, attack 4). Setting v2=w2=u2=0 (the fixed-covariance Gaussian mean submodel), my pair h^4 coefficient minus [(1/4)g^F(w,w) + (1/3)g^F(v,u)] is exactly 0, whereas pair h^4 minus (1/4)g^F(w,w) alone leaves (1/3)g^F(v,u) != 0. The derivation's section 3.5 claim '(h^4/4)|w|^2 identically' is indeed wrong and the skeptic's repair is right.

### 10

RECOMPUTED, sub-claim (7) 'only in d=2'. Direct numerical test with a Gaussian fibre on a d-torus, RAW unit-coefficient (counting-measure) symmetric bond sum, no weight at all. d=1: sum = 0.0601 -> 0.00376 as M goes 64 -> 1024, i.e. -> 0 like h. d=2: sum = 5.9255, 5.9409, 5.9448, 5.9458 at M=32..256, converging to the target (1/2)int||grad q||^2_{g^F} = 5.94608830. d=3: sum = 104.8, 158.5, 211.9, 318.4 at M=16..48, diverging like h^{-1}. So the unweighted ELBO bond sum has a finite nonzero limit iff d=2. Sub-claim (7) is CONFIRMED as literally stated, for the bond sector.

### 11

CITED + RECOMPUTED, the crucial qualification the reviewer did not draw and 4b partly obscures. d=2 does NOT resolve the scaling conflict. The bond/site RELATIVE weight mismatch is h^{-2} in EVERY dimension: panelA-T-GRAD-derivation.md:39 states (E) d-independently ('With lambda_h = h^d the gradient sector vanishes; with lambda_h = h^{d-2} the observation sector diverges as h^{-2}'), and panelB-V-BRIDGE-derivation.md:198-220 builds its own limit with TWO different weights at every d (site weight eps^d, bond weight eps^{d-2}), including at d=2, where it says explicitly 'the identification holds on the BOND SECTOR ALONE, and the site sector is a separate additive piece'. My own d=2 run confirms the site sector still grows as h^{-d} = 6.55e4 at M=256. So m_h = ceil(d h^{-2}) replication is still required at d=2; what d=2 buys is only that h^d * m_h = d is h-independent.

### 12

CITED, task (d) -- is the three-way d=2 convergence real? It is REAL but it is ONE fact seen three ways, not three independent corroborations, and panelB-V-BRIDGE-derivation.md:197 says so itself: 'This is the same fact as the eps^{d-2} = eps^0 = 1 weight ... The match is not an analogy; it is an identity.' All three are the classical statement that a two-derivative (Dirichlet) energy density is scale-invariant exactly in d=2: (i) the reviewer's/T-GRAD's counting h^{-d} sites x O(h^2) per bond = h^{2-d}; (ii) V-BRIDGE (V4, :31) det(gothic-g) = |det U|^{2-d} == 1 for every Bravais lattice iff d=2; (iii) V-BRIDGE (V1, :17) and (:130) Weyl invariance sqrt|Omega^2 gamma|(Omega^2 gamma)^{munu} = Omega^{d-2}(...), Omega-independent iff d=2. V-BRIDGE (V3, :27) adds a genuinely distinct algebraic route -- degree d/2 of sqrt(det h) versus degree 1 of any bond sum -- which lands on the same exponent for a different reason (Minkowski concavity of det^{1/2} on PSD_d holds iff d<=2).

### 13

CITED -- a NEW defect in section 4b that the reviewer could not have seen and that is exactly the 'sound alike but are different claims' trap. Worklog:1087-1089 (the hand-written 4.7 synthesis) asserts the connection mismatch 'explains the d=2 coincidence in 4.6 and the Gaussian-fixed-covariance escape in 4.1 as the same phenomenon: both are exactly where the Amari-Chentsov contraction drops out.' This is contradicted by its own source: panelB-V-BRIDGE-derivation.md:17 states 'The statistical nature of the target (curvature of g^F, the Amari-Chentsov tensor) plays NO role in (V1): delta_gamma at fixed q sees h as an arbitrary fixed symmetric psd (0,2) tensor field.' The 4.6 d=2 selection is a homogeneity/Weyl fact about h as an abstract psd tensor; T_AC is not involved. The 4.1 Gaussian-fixed-covariance escape genuinely is a T_AC-vanishing fact. Merging them is unsupported.

### 14

CITED -- the d=2 escape is unavailable for the very families the script verifies. panelB-V-BRIDGE-derivation.md:59 (H3) 'dim B >= d. Strictly necessary ... At d = 2 this excludes every one-parameter fiber (normal location, Bernoulli, Poisson, exponential)'. kl_expansion_check.py:90-92 verifies exactly Poisson, Bernoulli and Exponential.

### 15

CITED -- the reviewer's demanded repair now exists. panelA-T-GRAD-derivation.md:41 (F) supplies the missing coefficient by integer replication m_h = ceil(d h^{-2}), explicitly licensed by docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/boundary-counterexamples.md:57 ('Positive integer coefficients can be represented by repeated independent copies with tied recognition'), keeping P_h^n normalized and Q-independent. panelA-T-GRAD-skeptic.md:100-102 (VECTOR 4, NORMALIZATION) audited this for a dropped log-normalizer and found none, reproducing the envelope numbers to every quoted digit; panelA-T-GRAD-skeptic.md:108-110 tried five routes to obtain the h^{-2} relative weight without replication and failed on all five, certifying (E) as a strict no-go. Note also that m_h is an INTEGER, which is consistent with the T-COEF unit-entropy principle (worklog:882-889) that an exact negative ELBO carries integer block-count coefficients.

### 16

CITED -- boundary treatment is now supplied, as an estimate rather than a proof. panelA-T-GRAD-derivation.md:71 (H1) chooses the torus to eliminate boundary terms and asserts 'on a domain with boundary the interior estimate is unchanged and the O(h) boundary layer contributes h^{d-2} * O(h^{-(d-1)}) * O(h^2) = O(h) -> 0'. I checked the arithmetic (h^{d-2} * h^{-(d-1)} * h^2 = h); it is correct as a counting estimate but is asserted in a hypothesis block, not proved.

### 17

CITED -- what genuinely remains open, and the corpus says so. Worklog:794-796: 'this is pointwise convergence at a fixed C^2 section, NOT Gamma-convergence. Equicoercivity, liminf, recovery sequences, interpolation topology and gauge compactness all remain missing, and six independent failures block the H^1 case.' docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/lattice-continuum-asymptotics.md:34: 'consistency expansions on smooth sequences, not Gamma-convergence proofs.' The reviewer's fourth prescribed fix ('prove the global covariant limit separately') is therefore done pointwise and still open variationally.

### 18

CITED -- residual live documentation defect. Worklog:97 still reads '(C3) Therefore the weight h^{d-2} is forced, not chosen' with no pointer to (E)/(F), and the CLOSED note at worklog:108-116 discharges only the covariant cancellation, not the ELBO-origin of the coefficient. overview.md:162-164 still reads 'so the weight h^{d-2} is forced. Flat transport only; covariant case open' -- both halves now stale: the covariant case is closed (4.1(i)) and 'forced' is true only of the deterministic Riemann sum, not of the ELBO, whose own coefficients are unit (boundary-counterexamples.md:63: 'The negative ELBO of the finite product law is a counting-measure sum ... weights ... do not remain an exact finite-law ELBO by notation alone').


## recomputation

All under the system scratchpad, never in the repo. (1) Executed docs/verification/kl_expansion_check.py unmodified: all assertions pass, coefficients 1/2, 1/3, 1/6 and the symmetric-stencil h^3 cancellation reproduce exactly. (2) rate_check.py / rate_check2.py -- d=1 torus, bond weight h^{d-2}=h^{-1}, M = 64..8192. Flat Poisson on a symmetric section: oriented exponent 1.9998, symmetric 1.9998 (the O(h) coefficient is annihilated by parity of that section). Flat Poisson on an asymmetric section, target 29.635452465984: oriented exponent 1.1542 with err1/h -> -8.1279 and Richardson extrapolant -8.045468, versus my closed-form prediction -(1/12) int A'''(theta) theta'^3 dc = -8.045494 (5 significant figures); symmetric exponent 1.9996 with err2/h^2 -> -674.9. Covariant Gaussian fibre with a genuine GL(1)_+ connection, target 4.088430292050: oriented exponent 0.9859 with err1/h -> 2.802 non-vanishing, symmetric exponent 1.9999 with err2/h^2 -> -11.639. (3) parity.py (SymPy) -- (mu,sigma) non-natural chart, transported-back curve with free jets v,w,u: f(0)=0, f'(0)=0, h^2 coefficient = (v1^2+2 v2^2)/sigma0^2 = g^F(v,v), single-edge h^3 coefficient generically nonzero, and the h^3 coefficient of E(+h)+E(-h) identically 0 in BOTH KL orientations for all w,u. Same for a generic exponential family in a non-natural chart: pair h^3 = 0 for all (a,b,d). Also confirmed the skeptic's h^4 correction: on the fixed-covariance mean submodel the pair h^4 coefficient equals (1/4)g^F(w,w)+(1/3)g^F(v,u) exactly, so the derivation's '(h^4/4)|w|^2 identically' is incomplete. (4) dscaling.py -- raw unit-coefficient nearest-neighbour KL sum, Gaussian fibre on a d-torus, no weight: d=1 -> 0 like h; d=2 -> 5.9255, 5.9409, 5.9448, 5.9458 at M=32,64,128,256 against target 5.94608830; d=3 -> 104.8, 158.5, 211.9, 318.4 at M=16,24,32,48, diverging. Site sector h^{-d} = 6.55e4 at d=2, M=256, i.e. still divergent at d=2. (5) Symbolic side-check: int A'''(theta) theta'^3 dc = 1.9e-15 (Poisson), 1.6e-16 (Bernoulli), 0 (Gaussian scale) on the accidentally symmetric section, explaining why the first oriented test showed no O(h).

## reviewer_missed

Five things. (1) The reviewer's 'ONE CENTER' wording is inaccurate: kl_expansion_check.py:56-82 does the cancellation at a free symbolic center. The real defect is stronger and different -- the increment is taken as exactly +/-h, so the section's acceleration and jerk are never exercised, which is precisely the step the covariant parity argument had to supply. (2) The reviewer's O(h) claim for a 'one-direction Poisson edge sum' is not unconditionally true: I measured exponent 2.00 for the oriented Poisson sum on a reflection-symmetric section, because the O(h) coefficient is -(1/12) int A'''(theta) theta'^3 dc, which parity annihilates. It is generically nonzero (measured -8.045468 versus my analytic -8.045494 on an asymmetric section), so the claim is right generically but a referee reproducing it carelessly would refute it. (3) The reviewer treats the covariant case as an open gap; a single elementary observation closes it -- f(eps) = D(theta_0, theta-hat(eps)) is one C^3 function with f(0)=f'(0)=0 -- which I verified symbolically and which needs only that the +/-h transported-back points lie on one smooth curve (true for straight-segment parallel transport) and that the edge WEIGHTS be symmetric, not merely the displacements (panelA-T-GRAD-skeptic.md:92-94, attack 8(iii)). (4) The reviewer's 'only in d=2' clause invites the over-reading that d=2 rescues the construction. It does not: the bond/site relative weight mismatch is h^{-2} in EVERY dimension, V-BRIDGE's own limit uses two weights (eps^d and eps^{d-2}) at d=2 as well, and V-BRIDGE (H3) at panelB-V-BRIDGE-derivation.md:59 requires dim B >= d, which at d=2 excludes every one-parameter fibre -- i.e. excludes Poisson, Bernoulli and Exponential, the three families kl_expansion_check.py:90-92 actually verifies. (5) The reviewer could not see it, but the worklog's own hand-written synthesis at worklog:1087-1089 now over-unifies the d=2 results, claiming the 4.6 d=2 coincidence and the 4.1 Gaussian-fixed-covariance escape are 'the same phenomenon ... exactly where the Amari-Chentsov contraction drops out'. panelB-V-BRIDGE-derivation.md:17 explicitly denies that T_AC plays any role in the d=2 selection. That merger should be struck.

## recommended_action

Three small documentation edits; no mathematics needs redoing. (1) worklog:97 -- amend (C3) from 'Therefore the weight h^{d-2} is forced, not chosen' to distinguish two senses: h^{d-2} is forced as the unique deterministic Riemann-sum weight, but the exact ELBO is a counting-measure sum with unit coefficients (boundary-counterexamples.md:63) and supplies h^{d-2} only via the integer replication m_h = ceil(d h^{-2}) of panelA-T-GRAD-derivation.md:41 (F), which remains a declared -- though canonically forced, parabolic -- postulate. Add a forward pointer from section 2 to section 4.1(ii)(b) and to (E)/(F), the way the covariant caveat now points to 4.1(i). (2) overview.md:162-164 -- both halves are stale: replace 'Flat transport only; covariant case open' with a pointer to worklog section 4.1(i), and narrow 'the weight h^{d-2} is forced' as in (1). (3) worklog:1087-1089 -- strike or qualify the claim that the 4.6 d=2 coincidence and the 4.1 Gaussian-fixed-covariance escape are 'the same phenomenon ... where the Amari-Chentsov contraction drops out'; panelB-V-BRIDGE-derivation.md:17 states that T_AC plays no role in the d=2 selection, which is a homogeneity/Weyl fact about h as an abstract psd tensor. Replace with the accurate unification: all the d=2 statements are the classical scale-invariance of a two-derivative energy density in two dimensions, which V-BRIDGE:197 already states ('not an analogy; it is an identity'), plus V-BRIDGE (V3):27's distinct Minkowski-concavity route. OPTIONAL, low cost, high value: add to docs/verification/kl_expansion_check.py a second section that (i) puts a section theta(c) on a refining d=1 torus, (ii) prints the fitted exponents for the oriented and symmetric sums with an explicitly stated edge convention and the (h^{d-2}/2) factor, and (iii) does the free-jet symbolic parity check. That converts the file from a local coefficient check into a reproduction of statements (A) and (B) and removes the standing gap between what the script proves and what its lines 100-102 claim. Do NOT adopt the reviewer's first prescribed fix ('state only a flat local consistency expansion') -- it is now too weak; the covariant symmetric-stencil statement is established.
