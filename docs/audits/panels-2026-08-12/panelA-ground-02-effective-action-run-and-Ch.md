# panelA-ground-02-effective-action-run-and-Ch

*Recovered verbatim from workflow journal.jsonl, 2026-08-13. Agent a16a80a8.*

## summary

A. C_h. The effective-action run defines the coarse map in exactly one sentence: "Let \(C_h:Z_h\to X_h\) be a measurable coarse map that is fixed independently of the recognition law" (exact-contraction-proof.md:6-8). Domain Z_h = "standard-Borel microscopic space", codomain X_h = "coarse configuration spaces ... of sampled belief, model, support, frame, and link fields" (problem-contract.json:13). It is LEFT WHOLLY ABSTRACT: no C_h is constructed, exhibited, or even constrained beyond measurability + Q-independence, and the identification of X_h with sampled sections is flagged as a MODELING_POSTULATE (claim-ledger.json:16-20), not a theorem. Release obligation #1 is precisely to supply it (release.json:11). Note a typing mismatch with the manuscript the run cites: Theory/07b_agent_network_rg.tex:18-24 makes the coarse object a Markov *kernel* C: Y⇝Z, not a map; the run silently specializes to the deterministic case.

B (crux). eps_h and c_h occur in exactly three lines of the entire corpus, all in one file. The run writes "A PIFB2 action is obtained by projecting that complete action onto the chosen self, peer, observation, base-edge, link, plaquette, and attention scopes: S_h^exact = S_h^PIFB + eps_h + c_h" (construction-or-strongest-theorem.md:16-19), then "This is an exact identity, not an assertion that eps_h=0. The truncated ELBO error is uniformly bounded by ||eps_h||_inf when that norm is finite" (:22-24). c_h is NEVER defined anywhere; eps_h is never independently characterized. As written the identity is a TAUTOLOGY (eps_h := S_exact − S_PIFB − c_h). The only substantive content is inherited from the cited manuscript locus (source-theorem-map.md:12-13 → 07b:1468-1512), where R_ℓ is "a declared bounded idempotent retained projection" and the residual is definitionally r = (I−R_{ℓ+1})T_ℓ (07b:1473-1482) — also difference-defined, but there the projection lives in a *specified* Banach space: the Hoeffding–Möbius interaction space G_ℓ with norm Σ_A ||g_A||_∞ relative to a PRODUCT reference ν_ℓ (07b:1203-1214). So eps_h becomes determinate only after (i) a product reference and (ii) a retained scope set are declared. Neither is declared in the run.

C. lattice-continuum-asymptotics.md DERIVES two second-order expansions and DERIVES the three weights only by edge/cell counting. The link consistency U^h·θ(y)=θ(x)+hD^A_μθ(x)+O(h²) is a HYPOTHESIS (:7-9). KL(q_θ(x)||U#q_θ(y)) = ½h²I(D^Aθ,D^Aθ)+O(h³) is DERIVED from zero-mean score + Fisher = −E[Hessian] (:15-18). h^{d-2}: DERIVED by counting ("There are order h^{-d} edges. Hence an edge transmissibility of order h^{d-2}", :20-22). h^d: ASSERTED for self/peer/observation/potential sectors with no argument (:22-23). Wilson: H_p = I − h²F + O(h³) and r − ReTr H_p = ½h⁴||F||²_HS + O(h⁵) DERIVED for compact groups in unitary reps, h^{d-4} again by counting (:26-32). The file itself states the ceiling: "These are consistency expansions on smooth sequences, not Gamma-convergence proofs" (:33-34). Smoothness: regular dominated family on a compact regular stratum, uniformly regular mesh, compact unitary rep (claim-ledger.json:58-62, :207).

D/E. Sixteen distinct witnesses (5+5+6) and three adversarial bundles are on record; two universal subclaims are formally REFUTED (generic-local-closure, live-peer-fixed-joint). Release obligations: 4+4+0. Details in extracts/gotchas.

## extracts

### 1

{
  "label": "A. C_h definition (the only one that exists)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/exact-contraction-proof.md:4-8",
  "statement": "\"Fix a finite lattice, finite agent count, standard-Borel microscopic space \\(Z_h\\), and normalized microscopic posterior \\(\\Pi_{h,o}\\). Let \\(C_h:Z_h\\to X_h\\) be a measurable coarse map that is fixed independently of the recognition law.\" This is the complete specification: measurable, deterministic, Q-independent. No construction, no locality, no equivariance, no fiber structure is imposed.",
  "status_tag": "ABSTRACT / UNSPECIFIED"
}

### 2

{
  "label": "A. C_h codomain intent",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/problem-contract.json:13",
  "statement": "\"Standard Borel microscopic state spaces Z_h and coarse configuration spaces X_h of sampled belief, model, support, frame, and link fields.\" X_h is intended as sampled section values, but only intended.",
  "status_tag": "DECLARED_DOMAIN"
}

### 3

{
  "label": "A. Section typing is a postulate, not a theorem",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/claim-ledger.json:16-20",
  "statement": "\"id\": \"a-section-typing\", \"kind\": \"MODELING_POSTULATE\", \"statement\": \"The retained coarse variables are sampled values of the finite agents' belief, model, support, frame, and link sections.\" The identification of coarse variables with agent sections carries no proof burden discharged anywhere in the run.",
  "status_tag": "MODELING_POSTULATE"
}

### 4

{
  "label": "A. Manuscript uses a KERNEL, not a map (typing mismatch)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/07b_agent_network_rg.tex:18-24",
  "statement": "\"A coarse channel between standard-Borel latent spaces is a fixed Markov kernel C:\\mathsf Y\\rightsquigarrow\\mathsf Z that does not read $Q_o$ and does not alter the observation coordinate.\" The run's C_h is the deterministic special case; the manuscript theorem is strictly more general.",
  "status_tag": "ESTABLISHED (manuscript)"
}

### 5

{
  "label": "A. Exact contraction identity proved from C_h",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/exact-contraction-proof.md:11-24",
  "statement": "D_KL(Q_h||Pi_{h,o}) = D_KL(R_h||P^o_{X,h}) + int D_KL(Q_h(dz|x)||Pi_{h,o}(dz|x)) R_h(dx), with R_h=(C_h)_#Q_h, P^o_{X,h}=(C_h)_#Pi_{h,o}; hence inf over Q_h with (C_h)_#Q_h=R_h of F_h(Q_h;o) = -log p_h(o) + D_KL(R_h||P^o_{X,h}), attained at the posterior-conditional lift Q_h^*(dz)=int Pi_{h,o}(dz|x) R_h(dx).",
  "status_tag": "DERIVATION / EVIDENCE_VERIFIED"
}

### 6

{
  "label": "A. Explicit non-implication",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/exact-contraction-proof.md:36-37",
  "statement": "\"This theorem does not imply that \\(S_h\\) is local, pairwise, or PIFB2-shaped.\"",
  "status_tag": "SCOPE_LIMIT"
}

### 7

{
  "label": "B. THE CRUX \u2014 the residual identity, verbatim",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/construction-or-strongest-theorem.md:14-20",
  "statement": "\"The exact density action admits a complete finite interaction decomposition. A PIFB2 action is obtained by projecting that complete action onto the chosen self, peer, observation, base-edge, link, plaquette, and attention scopes: \\[ S_h^{\\rm exact}=S_h^{\\rm PIFB}+\\varepsilon_h+c_h. \\]\" No projection operator, no basis, no reference measure, no norm, and no ambient space are specified in the run.",
  "status_tag": "TAUTOLOGY AS WRITTEN"
}

### 8

{
  "label": "B. THE CRUX \u2014 self-admitted tautology + the only quantitative claim",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/construction-or-strongest-theorem.md:22-26",
  "statement": "\"This is an exact identity, not an assertion that \\(\\varepsilon_h=0\\). The truncated ELBO error is uniformly bounded by \\(\\|\\varepsilon_h\\|_\\infty\\) when that norm is finite. ... No current evidence proves a vanishing residual, a full dynamical-gauge Gamma limit, or a continuum process-law ELBO for the intended PIFB2/MAgent family.\" The bound is ASSERTED with no derivation, and c_h does not appear in it.",
  "status_tag": "ASSERTED"
}

### 9

{
  "label": "B. c_h is never defined anywhere in the corpus",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/construction-or-strongest-theorem.md:19",
  "statement": "Exhaustive grep over all three run directories returns \\varepsilon_h at exactly lines 19, 22, 23 of this one file and c_h at exactly line 19. No file states what c_h is (constant? R_h-independent? the additive normalizer of exact-contraction-proof.md:34?). eps_h is likewise never characterized independently of the difference.",
  "status_tag": "UNDEFINED SYMBOL"
}

### 10

{
  "label": "B. Where the residual IS given content (cited by the run)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/source-theorem-map.md:12-13",
  "statement": "\"`Theory/07b_agent_network_rg.tex:1468-1512` defines the retained projection, residual, and the condition under which a PIFB-like ansatz is exact.\" This is the only pointer from the run to a substantive residual definition.",
  "status_tag": "PRIMARY_SOURCE POINTER"
}

### 11

{
  "label": "B. Manuscript residual: also difference-defined, but typed",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/07b_agent_network_rg.tex:1468-1482",
  "statement": "\"Let \\(R_\\ell:\\mathcal G_\\ell\\to\\mathcal G_\\ell\\) be a declared bounded idempotent retained projection which intertwines the componentwise/permutation gauge action...\" with r^G_{l+1}(g_l) = (I-R_{l+1}) T_l^G(g_l) and rbar^Q_{l+1}(g_l) = E_{l+1} r^G_{l+1}(g_l). The residual is literally (I-R)T: difference-defined. R_ell is 'declared', i.e. still a free choice.",
  "status_tag": "ESTABLISHED (definitional)"
}

### 12

{
  "label": "B. The exactness criterion the residual encodes",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/07b_agent_network_rg.tex:1487-1496",
  "statement": "T_l^G(Ran R_l) subseteq Ran R_{l+1} <=> r^G_{l+1}(g)=0 for every g in Ran R_l. \"Thus a retained update is exact precisely under this exact-image-invariance condition; otherwise it is a projection scheme with the displayed residual.\" This is the non-tautological content available to a downstream prover: closure = invariance of Ran R under the exact interaction step.",
  "status_tag": "ESTABLISHED"
}

### 13

{
  "label": "B. The space and norm in which eps_h must live",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/07b_agent_network_rg.tex:1203-1214",
  "statement": "G_l = ell^1-direct-sum over nonempty A subseteq V_l of H_{l,A} = P_{l,A} L^infty(nu_l), with ||g||_{G_l} = sum_{A nonempty} ||g_A||_infty, where P_{l,A} are Boolean-lattice Mobius projectors built from conditional integration against a PRODUCT reference nu_l (eq:rg-hoeffding-mobius-projectors, :1193-1200). Hoeffding decomposition therefore requires a product reference measure.",
  "status_tag": "ESTABLISHED"
}

### 14

{
  "label": "B. Exponential extraction bound \u2014 the hidden cost of the projection",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/07b_agent_network_rg.tex:1228-1239",
  "statement": "||E_l|| <= 1, ||H_l|| <= 3^{|V_l|}-1, and \"Its exponential dependence is sharp in the worst case: for biased Rademacher product coordinates and f(x)=prod_i x_i, the sum of component norms approaches the bound at the corresponding product scale as the bias tends to one.\"",
  "status_tag": "ESTABLISHED (sharp)"
}

### 15

{
  "label": "B. Two-sided residual norm control",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/07b_agent_network_rg.tex:1499-1508",
  "statement": "||r^G_{l+1}||_{G_{l+1}} / (3^{|V_{l+1}|}-1) <= ||rbar^Q_{l+1}||_{Bbar_{l+1}} <= ||r^G_{l+1}||_{G_{l+1}}. A coordinate-norm bound gives a sup-norm (action-quotient) bound for free; the converse costs 3^{|V|}.",
  "status_tag": "ESTABLISHED"
}

### 16

{
  "label": "B. Product-equivalence is not automatic (blocks Hoeffding coordinates)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/Theory/07b_agent_network_rg.tex:1160-1173",
  "statement": "\"Product equivalence is an admitted, not an automatic, scale premise.\" For the deterministic diagonal-cloning channel K(x,{(x,x)})=1 on {0,1}, pi_1 = pi_0 K is supported on the diagonal and \"There is no product probability nu_1 = nu_{11} tensor nu_{12} on {0,1}^2 equivalent to pi_1 ... No target Hoeffding decomposition relative to a product reference is admitted at this target.\"",
  "status_tag": "COUNTEREXAMPLE"
}

### 17

{
  "label": "B. The open claim that eps_h -> 0",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/claim-ledger.json:254-270",
  "statement": "id \"pifb-controlled-projection\", state \"INCONCLUSIVE\": \"For the current intended PIFB2/MAgent microscopic family, the exact coarse action has a PIFB2 retained projection whose residual vanishes uniformly on bounded-energy sublevels as the base lattice is refined.\" Falsifier: \"A nonvanishing generated operator or residual sequence refutes controlled closure; a uniform residual theorem would verify it.\" Note the norm and the sublevel set are both unspecified.",
  "status_tag": "INCONCLUSIVE"
}

### 18

{
  "label": "C. Link-consistency hypothesis (assumed, not derived)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/lattice-continuum-asymptotics.md:4-9",
  "statement": "\"For a regular statistical family \\(q_\\theta\\), an edge \\(y=x+he_\\mu\\), and a link that approximates parallel transport, \\[ U_{xy}^h\\cdot\\theta(y)=\\theta(x)+hD_\\mu^A\\theta(x)+O(h^2). \\]\" This is a stipulated property of the link, not a derived one.",
  "status_tag": "ASSERTED HYPOTHESIS"
}

### 19

{
  "label": "C. Fisher expansion \u2014 DERIVED",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/lattice-continuum-asymptotics.md:11-18",
  "statement": "\"The score has zero expectation and the expected negative Hessian is the Fisher tensor, so Taylor expansion gives \\[ D_{\\rm KL}(q_{\\theta(x)}\\Vert U_{xy\\#}^hq_{\\theta(y)})=\\tfrac12 h^2 I_{\\theta(x)}(D_\\mu^A\\theta,D_\\mu^A\\theta)+O(h^3). \\]\"",
  "status_tag": "DERIVATION"
}

### 20

{
  "label": "C. h^{d-2} \u2014 DERIVED by counting only",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/lattice-continuum-asymptotics.md:20-22",
  "statement": "\"There are order \\(h^{-d}\\) edges. Hence an edge transmissibility of order \\(h^{d-2}\\) yields a finite Fisher-covariant Dirichlet integral.\" Dimensional/Riemann-sum consistency; no convergence proof, no uniformity statement on the O(h^3) remainder.",
  "status_tag": "DERIVED (counting) / CONVERGENCE OPEN"
}

### 21

{
  "label": "C. h^d \u2014 ASSERTED, no argument at all",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/lattice-continuum-asymptotics.md:22-23",
  "statement": "\"Pointwise self, peer, observation, and potential sectors instead use cell weights of order \\(h^d\\), with cut-cell weights on local section supports.\" One sentence; no derivation, no cut-cell construction, no error term.",
  "status_tag": "ASSERTED"
}

### 22

{
  "label": "C. Wilson h^{d-4} \u2014 DERIVED for compact unitary reps",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/lattice-continuum-asymptotics.md:25-32",
  "statement": "\"For a compact gauge group in a unitary representation, a small plaquette has \\(H_p=I-h^2F_{\\mu\\nu}+O(h^3)\\), and \\[ r-\\operatorname{ReTr}H_p=\\tfrac12h^4\\|F_{\\mu\\nu}\\|_{\\rm HS}^2+O(h^5). \\] Therefore the Wilson sector must carry weight \\(h^{d-4}\\).\"",
  "status_tag": "DERIVATION (compact only)"
}

### 23

{
  "label": "C. The file's own ceiling statement",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/lattice-continuum-asymptotics.md:33-37",
  "statement": "\"These are consistency expansions on smooth sequences, not Gamma-convergence proofs. A deterministic limit additionally requires a common interpolation topology, equicoercivity modulo gauge, liminf, recovery, boundary/topology control, and uniformly vanishing truncation residual on bounded-energy sublevels.\"",
  "status_tag": "SCOPE_LIMIT"
}

### 24

{
  "label": "C. Declared regularity for the asymptotics",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/claim-ledger.json:57-62 and :207",
  "statement": "Side conditions: \"Regular dominated statistical family\", \"Uniform mesh and smooth link consistency\", \"Compact unitary gauge representation for Wilson sector\". Claim quantifier: \"Every fixed finite N, regular dominated statistical family on a compact regular stratum, and sufficiently fine uniformly regular mesh.\"",
  "status_tag": "DECLARED_HYPOTHESES"
}

### 25

{
  "label": "D. Effective-action run counterexample register (CE-1..CE-5)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/counterexample-register.md:6-13",
  "statement": "CE-1 kills 'exact contraction is automatically local' (shared Gaussian latent -> all-to-all rank-one term). CE-2 kills 'exact elimination remains pairwise' (hidden Ising spin -> four-agent interaction). CE-3 kills 'live-peer KL is an ordinary fixed-joint state ELBO' (mixed-derivative mismatch). CE-4 kills 'raw positive GL curvature is gauge invariant' (diagonal conjugation rescales Frobenius energy). CE-5 kills 'action convergence implies process ELBO convergence' (product Bernoulli). Closing caveat: \"These counterexamples do not refute the existential possibility of a restricted, well-typed microscopic family. They refute generic automatic PIFB2 closure.\"",
  "status_tag": "COUNTEREXAMPLE"
}

### 26

{
  "label": "D. CE-1/CE-2 witnesses in full",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/adversarial-counterexamples.md:4-9",
  "statement": "\"If \\(Y\\sim N(0,\\tau^2)\\) and \\(X_a\\mid Y\\sim N(Y,\\sigma^2)\\), eliminating \\(Y\\) generates an all-to-all term proportional to \\((\\sum_aX_a)^2\\). Eliminating a hidden Ising spin coupled to four retained spins generates a nonzero four-body operator through \\(-\\log[2\\cosh(\\sum_iJ_ix_i)]\\). A local pairwise PIFB2 basis therefore needs an explicit projection and residual.\"",
  "status_tag": "COUNTEREXAMPLE"
}

### 27

{
  "label": "D. CE-3 live-peer mixed-derivative obstruction (exact numbers)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/adversarial-counterexamples.md:11-18",
  "statement": "\"For every fixed positive joint \\(P(i,j)\\), the product-recognition functional \\(D_{\\rm KL}(q_iq_j\\Vert P)\\) has \\(\\partial_p\\partial_r^2=0\\), whereas the live-peer KL has \\(\\partial_p\\partial_r^2=r^{-2}-(1-r)^{-2}\\), nonzero away from \\(r=1/2\\). The sender cannot be both a current variational marginal and a fixed generative factor without an additional typed layer.\" Ledger state for claim live-peer-fixed-joint: REFUTED (claim-ledger.json:189-203).",
  "status_tag": "REFUTED"
}

### 28

{
  "label": "D. CE-4 GL non-invariance (exact factor)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/adversarial-counterexamples.md:20-25",
  "statement": "\"For \\(K\\ge2\\), \\(\\|H-I\\|_F^2\\) is not invariant under \\(H\\mapsto g^{-1}Hg\\) in \\(GL(K)\\). Taking \\(H=I+\\epsilon E_{12}\\) and \\(g=\\operatorname{diag}(t,1)\\) changes the norm by \\(t^{-2}\\). Moreover noncompact Haar volume is infinite, so a gauge-invariant Gibbs law needs a quotient/gauge slice, Jacobian, stabilizer treatment, and a finite reference measure.\"",
  "status_tag": "COUNTEREXAMPLE"
}

### 29

{
  "label": "D. CE-5 action-vs-process divergence (exact numbers)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/adversarial-counterexamples.md:27-30",
  "statement": "\"For \\(M=1/h\\) product Bernoulli sites, the unscaled exact KL is \\(M d_{\\rm KL}(q\\Vert p)\\), while the quadrature-scaled density action is \\(hM d_{\\rm KL}(q\\Vert p)\\). The first diverges and the second stays finite.\"",
  "status_tag": "COUNTEREXAMPLE"
}

### 30

{
  "label": "D. Effective-action run: single adversarial attack, SUSTAINED",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/adversarial-report.json:7-26",
  "statement": "id \"attack-locality-circularity-continuum\", disposition SUSTAINED, against all 11 claims: \"Exact contraction may be nonlocal and many-body; current belief sections may be recognition parameters rather than Q-independent coarse samples; live-peer KL is not generically a fixed-joint state ELBO; GL gauge volume may be nonnormalizable; and deterministic action convergence does not imply process-law ELBO convergence.\"",
  "status_tag": "SUSTAINED"
}

### 31

{
  "label": "D. Fast-slow run counterexample register (CE-1..CE-5)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-pifb2-fast-slow-program/counterexample-register.md:4-12",
  "statement": "CE-1 kills 'same-time live-peer term is automatically a fixed-joint ELBO' (the proposed generative peer law reads current q_j) -> 'Lag or promote fields'. CE-2 kills 'a Gibbs lift derives the action' (defining P propto e^{-S_PIFB} inserts S_PIFB) -> 'Use an independent microscopic law and contraction'. CE-3 kills 'fast/slow labels prove adiabatic reduction' (multiple or unstable fast minima) -> 'Prove attraction and normal hyperbolicity'. CE-4 kills 'positive Frobenius curvature is full-GL invariant'. CE-5 kills 'deterministic action convergence gives process-law convergence'. \"These attacks do not refute the exact lagged construction. They delimit what remains open.\"",
  "status_tag": "COUNTEREXAMPLE"
}

### 32

{
  "label": "D. Fast-slow run: single adversarial attack, SUSTAINED",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-pifb2-fast-slow-program/adversarial-report.json:7-24",
  "statement": "id \"attack-circularity-equilibrium-gl\", disposition SUSTAINED: \"Same-time live-peer laws can make the generative law depend on Q; a Gibbs lift can insert rather than derive the action; fast/slow labels do not prove adiabatic elimination; and noncompact GL has positivity and gauge-volume failures.\" Response: \"Use the exact lagged conditional model first, retain the equilibrium/emergence and adiabatic claims as open, prove the compact-group theory first, and require SPD dressing plus quotient/coercivity for GL.\"",
  "status_tag": "SUSTAINED"
}

### 33

{
  "label": "D. Fast-slow: why the lag is load-bearing",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-pifb2-fast-slow-program/evidence/transported-peer-derivations.md:33-36",
  "statement": "\"This is exact because \\(q^n\\) belongs to the conditioned history, not the variational law being optimized at \\(n+1\\). The simultaneous replacement \\(q_j^n\\mapsto q_j^{n+1}\\) destroys that fixed-conditional argument. Configuration-law promotion or an empirical-measure theorem is then needed.\"",
  "status_tag": "DERIVATION + OBSTRUCTION"
}

### 34

{
  "label": "D. Fast-slow: profiling is zero-temperature only",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-pifb2-fast-slow-program/evidence/fast-slow-effective-action.md:26-36",
  "statement": "\"For gradient-flow dynamics (dot q=-nabla_q F(q,S)), (dot S=-epsilon nabla_S F(q,S)), substitution of (q^*(S)) is justified only after proving a uniformly attracting normally hyperbolic fast branch. At nonzero fast temperature, e^{-S_eff(S)/T_q}=int e^{-F(q,S)/T_q} nu_q(dq), and the saddle expansion contains fluctuation determinants. Profiling is the zero-temperature or exact-optimization operation, not the generic finite-temperature action.\" (Note: this file carries NO rigorous-theory-search metadata header, unlike the run's other artifacts.)",
  "status_tag": "DERIVATION + OBSTRUCTION"
}

### 35

{
  "label": "D. Fast-slow: GL SPD dressing candidate and its unmet obligations",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-pifb2-fast-slow-program/evidence/compact-and-gl-group-program.md:14-30",
  "statement": "\"||g^{-1}(H-I)g||_F^2 = epsilon^2/t^2\" for H=I+epsilon E_12, g=diag(t,1). Dressing W_M(H)=Tr[M^{-1}(H-I)^T M (H-I)] with M^g=g^T M g \"but existence and normalization further require nondegeneracy of (M), control of (D_A M), a gauge quotient or slice, and a finite reference law. Full (GL(K)) has no normalized Haar measure. Any 'complexity growth' must be formulated as a gauge-invariant observable before it is physical.\"",
  "status_tag": "ALGEBRAIC REPAIR / ANALYTICALLY OPEN"
}

### 36

{
  "label": "D. Exact two-channel run: counterexample register (CE-1..CE-6)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-exact-two-channel-finite-elbo/counterexample-register.md:4-14",
  "statement": "CE-1: marginal self KLs are not exact for correlated private recognition (perfectly correlated binary gives I_zeta = log 2 while both marginal KLs vanish) -> retain I_zeta or impose mean field. CE-2: one normalized product-of-experts latent leaves -H(q)-log Z_beta -> use distinct replicas. CE-3: elementary source-label KL cannot produce arbitrary tau; difference is (tau-1)D_KL(beta||pi). CE-4: one private replica cannot produce arbitrary lambda_h or alpha. CE-5: cell-volume weights do not preserve exact finite-law ELBO semantics. CE-6: current live sources do not define a fixed joint (the generative denominator reads Q^{n+1}). \"None of these witnesses refutes the scoped tied-replica theorem. They prevent extending its label beyond its stated hypotheses.\"",
  "status_tag": "COUNTEREXAMPLE"
}

### 37

{
  "label": "D. Exact run: base quadrature weights are NOT an ELBO",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/boundary-counterexamples.md:60-66",
  "statement": "\"The negative ELBO of the finite product law is a counting-measure sum. Multiplying a site term by a cell volume (w_x) changes its probabilistic meaning unless the generative law is changed by replication, tempering, or an explicitly normalized weighted model. Such weights are appropriate in a deterministic action approximation, but do not remain an exact finite-law ELBO by notation alone.\"",
  "status_tag": "COUNTEREXAMPLE"
}

### 38

{
  "label": "D. Exact run: empty sources / hard support edge cases",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/boundary-counterexamples.md:74-79",
  "statement": "\"For (N=1) with self-sources excluded, the peer channel is absent. An all-zero row is not a categorical law. With hard supports, a peer KL may be (+\\infty); masks are applied by restricting the source set before the KL is formed, not by writing the undefined product (0\\cdot\\infty).\"",
  "status_tag": "BOUNDARY CONDITION"
}

### 39

{
  "label": "D. Exact run: five adversarial attacks A-E and dispositions",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-exact-two-channel-finite-elbo/evidence/adversarial-attacks.md:1-45",
  "statement": "A 'the replicas merely insert the answer' -> \"Sustained as an interpretive limitation, rejected as an algebraic objection ... The theorem proves existence of an exact representational lift, not uniqueness or physical emergence.\" B 'reciprocal graphs reintroduce source-label normalization failure' -> Rejected for this scoped theorem; \"The attack returns if relational copies are identified with shared contemporaneous agent states.\" C 'state-model correlation silently lost' -> Rejected (I_{zeta_a} retained). D 'arbitrary temperatures/weights called exact' -> Rejected; theorem is explicitly unit temperature and unit private coefficients. E 'finite exactness promoted to a continuum theorem' -> Rejected; \"Cell-volume, edge-gradient, and curvature scalings are not included and no process law on section space is claimed.\" Aggregate disposition in adversarial-report.json:19 is REJECTED.",
  "status_tag": "REJECTED (aggregate)"
}

### 40

{
  "label": "E. Effective-action run release.json obligations (verbatim, 4 items)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/release.json:10-15",
  "statement": "terminal_status INCONCLUSIVE, certificate_claim null. Obligations: (1) \"Specify the intended normalized microscopic section-variable family independently of the PIFB2 ansatz.\" (2) \"Prove a controlled local PIFB2 truncation residual for the refining lattice family.\" (3) \"Prove deterministic Gamma convergence including dynamical gauge sectors.\" (4) \"Construct and prove convergence of the continuum process-law ELBO including entropy and normalizers.\"",
  "status_tag": "UNRESOLVED"
}

### 41

{
  "label": "E. Effective-action final-report obligations (5 items \u2014 DIFFERS from release.json)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/final-report.md:51-61",
  "statement": "(1) \"Specify one normalized microscopic family whose slow variables are genuine sampled belief/model sections rather than recognition parameters.\" (2) \"Compute or bound its exact generated interaction coordinates.\" (3) \"Prove the retained PIFB residual vanishes in a declared norm uniformly on bounded-energy sublevels.\" (4) \"Establish equicoercivity, liminf, recovery, boundary, topology, and gauge compactness for a deterministic continuum action.\" (5) \"Separately establish tightness, continuum reference/process laws, relative-entropy convergence, and partition/evidence convergence.\" Item (2) \u2014 computing the generated interaction coordinates \u2014 has no counterpart in release.json.",
  "status_tag": "UNRESOLVED"
}

### 42

{
  "label": "E. Fast-slow run release.json obligations (verbatim, 4 items)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-pifb2-fast-slow-program/release.json:9-15",
  "statement": "strongest_result: \"Exact finite-N lagged transported-peer KL identity, exact fast-state profiling identity, and compact-subgroup reduction.\" Obligations: (1) \"Same-time reciprocal peer emergence from an independently specified microscopic law.\" (2) \"Adiabatic fast/slow theorem and finite-temperature corrections.\" (3) \"Controlled PIFB residual and deterministic/process-law continuum limits.\" (4) \"Normalized coercive full-GL extension with invariant complexity observables.\"",
  "status_tag": "UNRESOLVED"
}

### 43

{
  "label": "E. Fast-slow final-report obligations (5 items \u2014 DIFFERS from release.json)",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-pifb2-fast-slow-program/final-report.md:44-50",
  "statement": "(1) \"Derive or refute the simultaneous reciprocal interaction from an independent microscopic model.\" (2) \"Prove the fast/slow singular-perturbation hypotheses or retain the coupled dynamics.\" (3) \"Prove a controlled PIFB interaction residual and fixed-(N) lattice continuum limit.\" (4) \"Construct the continuum probability law and relative-entropy limit separately.\" (5) \"Define and control the SPD/nonmetricity sector, gauge quotient, and invariant complexity for full GL.\" Here the continuum obligation is split into deterministic (3) and process-law (4).",
  "status_tag": "UNRESOLVED"
}

### 44

{
  "label": "E. Exact two-channel run release.json \u2014 zero obligations",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-exact-two-channel-finite-elbo/release.json:7-10",
  "statement": "terminal_status \"COMPLETE_AFFIRMATIVE\", certificate_claim \"target\", \"unresolved_obligations\": []. But claim same-time-emergence is separately carried at state INCONCLUSIVE inside that run's ledger (claim-ledger.json:254-259), i.e. the empty obligation list is scoped to the certified target only.",
  "status_tag": "CLOSED (scoped)"
}

### 45

{
  "label": "Cross-run: the open sector table",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/pifb2-sector-map.md:4-22",
  "statement": "Sector-by-sector strongest justified status. Notable rows: \"Base-gradient Fisher term | Conditional local expansion | Same-agent neighboring-base KL, links approaching a connection, Fisher regularity, and h^{d-2} scaling\"; \"Compact curvature | Conditional continuum expansion | Wilson plaquettes and h^{d-4} scaling\"; \"Raw GL(K) positive curvature | Obstructed | Frobenius norm is not conjugation invariant; invariant trace forms are indefinite\"; \"Fisher/SPD-dressed GL(K) curvature | Algebraically viable; analytically open\"; \"Higher-body, nonlocal, boundary, memory terms | Exact correction sectors | Retain them or prove a residual bound\"; \"Continuum process-law ELBO | Open and strictly stronger\".",
  "status_tag": "SECTOR MAP"
}

### 46

{
  "label": "Cross-run: both inconclusive runs pass oracle erasure with the same verdict",
  "location": "C:/tmp/MultiAgentELBO-elbo-action-019ff75d/docs/derivations/2026-08-12-elbo-to-effective-section-action/evidence/oracle-erasure.md:7-11",
  "statement": "\"What disappears is the choice of which local operators to retain and how to interpret them as self, peer, attention, connection, and curvature sectors. Therefore PIFB2 and MAgent are useful hypotheses for the retained basis, but not evidence that the basis is exactly generated.\" Matched by the fast-slow run's oracle-erasure.md:8-10.",
  "status_tag": "PASS"
}


## gotchas

### 1

(B) DECISIVE: as written in the run, the residual identity IS a tautology. eps_h and c_h appear on exactly three lines of one file (construction-or-strongest-theorem.md:19,22,23); c_h is never defined at all, and eps_h has no independent characterization. Anyone who cites 'S_exact = S_PIFB + eps + c' as a theorem is citing a definition. The non-vacuous content lives only in Theory/07b_agent_network_rg.tex:1468-1512, and even there the residual is (I-R)T with R merely 'declared'.

### 2

(B) The only non-tautological handle on the residual is the exact-image-invariance criterion at 07b:1487-1496: closure holds iff T_l(Ran R_l) subseteq Ran R_{l+1}. A prover should target THAT, not 'eps_h -> 0' in the abstract, because 'eps_h -> 0' has no declared norm, no declared sublevel set, and no declared ambient space in the run.

### 3

(B) eps_h is only determinate after a PRODUCT reference measure is fixed (the Hoeffding-Mobius projectors at 07b:1193-1200 are built from conditional integration against nu_l, and G_l = P_{l,A} L^infty(nu_l)). The derivation run never states this hypothesis. If nu_h is not a product, there is no interaction-coordinate decomposition and eps_h is undefined.

### 4

(B) Product-equivalence can FAIL for exactly the kind of coarse map the run admits. 07b:1160-1180 shows a deterministic diagonal-cloning channel produces a coarse law with no equivalent product reference, so 'No target Hoeffding decomposition relative to a product reference is admitted'. Since the run's C_h is a deterministic measurable map, any attempt to DERIVE (rather than posit) the tied-replica lift by coarse-graining a microscopic space where two coarse coordinates read the same microscopic variable will trip this. Note this does NOT retroactively damage the closed two-channel theorem, whose generative joint is already a product of independent history-conditioned blocks; the tying lives only in the recognition law Q.

### 5

(B) The assertion 'the truncated ELBO error is uniformly bounded by ||eps_h||_inf' (construction:23-24) is stated without derivation and drops c_h. If the truncated functional is renormalized (its own partition function Z_PIFB), then F_exact - F_PIFB = E_R[eps_h + c_h] + log Z_exact - log Z_PIFB; c_h cancels between the two terms but log-sum-exp Lipschitzness gives 2||eps_h||_inf, not ||eps_h||_inf. If instead the exact log Z_h is retained, the difference is E_R[eps_h] + c_h and the c_h term is NOT bounded by ||eps_h||_inf. Either way the stated constant is wrong or the convention is unstated. Re-derive before using.

### 6

(B) Norm mismatch across the two loci: the run bounds with ||eps_h||_inf (sup norm on the action quotient), the manuscript's projection lives in G_l with the much stronger norm sum over ALL 2^{|V|}-1 nonempty subsets A of ||g_A||_inf. The manuscript direction ||rbar^Q|| <= ||r^G|| is the helpful one (a coordinate bound implies the sup bound); the reverse costs 3^{|V|}-1, and that bound is SHARP (07b:1235-1239). Under lattice refinement |V_h| ~ h^{-d}, so any residual argument that has to go coordinate-wards is exponentially hard in h^{-d}. This is a real, unstated obstruction to obligation (2) of the effective-action final report.

### 7

(A) C_h is not specified. Do not treat any concrete coarse map (cell averaging, block spin, section sampling) as 'the' C_h of the run - the run's first release obligation is precisely to supply the microscopic family and hence C_h. Also note the run uses a deterministic MAP while the manuscript theorem it leans on (07b:18-24) is for a Markov KERNEL; the run's statement is a strict special case, and its disintegration is over the fibers C_h^{-1}(x).

### 8

(A) exact-contraction-proof.md never writes the definition of F_h(Q_h;o) it uses at line 22, and never states Q_h << Pi_{h,o} or 0 < p_h(o) < infinity in the text (those live only in claim-ledger.json:33-37 as side conditions). State them explicitly if you build on it.

### 9

(A) The contraction infimum at exact-contraction-proof.md:21-24 is over ALL fine laws with the given pushforward. If the operative recognition family is restricted (mean field, parametric), the identity becomes an inequality plus a posterior-KL gap - a point the fast-slow run makes explicitly (fast-slow-effective-action.md:17) but the effective-action run does not.

### 10

(C) The h^d cell weight for self/peer/observation/potential sectors is ASSERTED in one sentence with no derivation and no error term (lattice-continuum-asymptotics.md:22-23). Only h^{d-2} and h^{d-4} carry counting arguments, and even those are Riemann-sum consistency, not convergence.

### 11

(C) The remainders O(h^3) (Fisher) and O(h^5) (Wilson) are never claimed UNIFORM over edges/plaquettes. The sums only converge if they are: h^{-d} edges * h^{d-2} weight * O(h^3) = O(h) requires a uniform-in-x remainder. Supply uniform third-derivative / uniform domination hypotheses yourself; the file does not.

### 12

(C) The Fisher expansion presupposes absolute continuity of the transported law U_{xy#}q_{theta(y)} w.r.t. q_{theta(x)} and nonsingular Fisher metric. The approach registry lists exactly this as the failure test ('Singular Fisher strata or O(1) link mismatch', approach-registry.json:117); claim quantifiers restrict to 'a compact regular stratum' (claim-ledger.json:207).

### 13

(C) The Wilson result is COMPACT-GROUP-ONLY (unitary representation). It does not transfer to GL(K,R): CE-4 in two separate runs shows raw Frobenius curvature is not conjugation invariant (factor t^{-2}), and full GL has no normalized Haar measure.

### 14

(C/D) The base-gradient (Fisher) and curvature sectors are ABSENT from the closed finite-probability theorem, and lattice-continuum-asymptotics.md never derives them from ANY ELBO - it checks the scaling of a postulated lattice action. Do not present these as ELBO-derived.

### 15

(D) Attack E / CE-5 of the exact run and CE-5 of the effective-action run jointly forbid the obvious bridge: you cannot take the closed finite theorem's counting-measure sum and multiply site terms by cell volumes w_x and still call it an exact ELBO (boundary-counterexamples.md:60-66). Doing so silently changes the generative law.

### 16

(D) The same-time obstruction is identical in all three runs and has a single mechanism: the generative denominator reads Q^{n+1} (exact run CE-6; fast-slow CE-1; effective-action CE-3). The only escape routes named anywhere are (i) lag, (ii) promote law-valued fields to genuine configuration coordinates and derive their law by contraction, (iii) an empirical-measure / weighted transported Sanov-type LDP. Route (iii) is registered as disposition 'open' with zero verified results (fast-slow approach-registry.json:49-61).

### 17

(D) CE-2 of the fast-slow run bars the shortcut a prover is most likely to reach for: defining P propto e^{-S_PIFB} and calling the resulting ELBO a derivation. That is insertion, not emergence.

### 18

(D) tau != 1 has an EXACT computed mismatch, (tau-1) D_KL(beta||pi) (boundary-counterexamples.md:46-51). Extending to nonunit temperature requires a separately normalized tempered generative model plus every source-dependent normalizer - not a coefficient edit.

### 19

(E) release.json and final-report.md disagree on the obligation lists in BOTH inconclusive runs (4 vs 5 items each). The effective-action final report carries an obligation absent from release.json: 'Compute or bound its exact generated interaction coordinates' (final-report.md:55). Treat the union as the true obligation set.

### 20

(E) The exact two-channel run's empty unresolved_obligations list is scoped to the certified target only; its own ledger still carries same-time-emergence at INCONCLUSIVE (claim-ledger.json:254-259). Do not read 'COMPLETE_AFFIRMATIVE' as 'nothing open in that run'.

### 21

Notation is NOT shared across runs: three distinct contract hashes (4648de08.../2d0dcc77.../ea859a3e...), and S means the effective action in the effective-action run but the SLOW STRUCTURE variable in the fast-slow run (fast-slow-effective-action.md:1-25). Cross-quoting formulas between runs without retyping is a live source of error.

### 22

Two artifacts in the fast-slow run (evidence/fast-slow-effective-action.md, transported-peer-derivations.md, compact-and-gl-group-program.md, independent-reconstruction.md, oracle-erasure.md, source-map.md) lack the rigorous-theory-search metadata header comment that the effective-action run's artifacts all carry, and their LaTeX is partly mangled (backslashes stripped: 'Omega', 'pi_{ij}', 'dot S'). Read them as prose, not as machine-checkable formulas.

### 23

Both inconclusive runs are revision-bound to repository commit 24c02aa29cd76589a52e54c56e4247f0560f7e87 and manuscripts read 2026-08-12 (final-report.md:65-66; :54-56). The working tree has since moved; verify any Theory/*.tex line citation before reusing it - I verified 07b_agent_network_rg.tex:16-66, :1160-1239, :1364-1392, :1468-1512 against the current worktree copy and they match the source map.

