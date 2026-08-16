export const meta = {
  name: 'multiagentelbo-0815-deep-review-wave1',
  description: 'Wave 1: ten independent expert investigators review the 2026-08-15 codex theory work, writing findings incrementally to disk',
  phases: [
    { title: 'Investigate' },
  ],
}

const REPO = 'C:/Users/chris and christine/Desktop/MultiAgentELBO'
const OUT = REPO + '/docs/reviews/2026-08-15-deep-review/findings'
const HEAD = '8ce635807a6ca2a388255fc996c98f7c535e5843'
const BASE = '060f80e5556e41e0f31aeafcd9ef8564c1544c16^'

const COMMON = `
You are an independent expert investigator on a deep adversarial review of theory work committed to
the repository at "${REPO}" on 2026-08-15 by another AI agent (codex).

REVIEW TARGET: git revision ${HEAD} on branch review/2026-08-15-deep-review.
The 8/15 diff is: git diff ${BASE} ${HEAD}
(Quote paths with spaces. Use absolute paths. The shell is Git Bash on Windows.)

CRITICAL CONTEXT — the work self-certifies. The two derivation packages under docs/derivations/
declare their central target EVIDENCE_VERIFIED, terminal status COMPLETE_AFFIRMATIVE, "no unresolved
obligations", sixteen adversarial attacks rejected, and four internal domain reviews all APPROVE at
Critical/High/Medium 0/0/0. Those internal attestations were produced by the same agent that wrote
the proofs. YOUR JOB IS TO TEST THEM, NOT TO INHERIT THEM. Do not treat any internal review,
adversarial-report entry, oracle-erasure record, or ledger state as evidence of anything. Read the
actual mathematics.

MANDATE — INCREMENTAL PERSISTENCE. A rate limit is expected to interrupt this session. You MUST
write your findings file to disk EARLY and UPDATE IT AS YOU GO, not only at the end. Specifically:

  STEP 0 (do this before any substantive reading): write your findings file with a header
    STATUS: IN_PROGRESS
    and a "Files to examine" checklist.
  Then, after EVERY finding you establish, append it to the file immediately.
  When done, rewrite the header to STATUS: COMPLETE and add a "Coverage" section listing exactly
  which files you read in full, which you sampled, and which you did not reach.

If you are cut off mid-work, the file on disk is the deliverable. Treat it that way.

FINDING FORMAT (one block per finding, in your file):

  ### [SEVERITY] Short title
  **Location:** path:line or path §section
  **Claim as stated:** verbatim quote of what the document asserts
  **Defect:** what is actually wrong, missing, or unsupported
  **Evidence:** your reconstructed derivation, the counterexample you built, the command you ran
    with its actual output, or the primary source with a quotation. NOT "this seems wrong."
  **Falsifier:** the specific fact that would show YOUR finding is wrong
  **Fix:** the smallest repair that would make the claim correct, or the honest restatement

SEVERITY SCALE:
  Critical — a stated theorem is false, or the certification is invalid
  High     — a claim is materially stronger than its proof; or a proof has a real gap
  Medium   — missing hypothesis, imprecision, notation collision, novelty/citation problem
  Low      — wording, presentation, hedging

RULES OF EVIDENCE:
  - Reconstruct load-bearing derivations yourself. Do not accept a step because it is asserted.
  - If you claim a step is wrong, exhibit the counterexample or the corrected computation.
  - If you claim something is standard/known, cite the primary source by name and result.
  - Report honestly when a claim CHECKS OUT. A section with zero findings is a legitimate result and
    you must say so explicitly rather than manufacturing findings.
  - Distinguish "the theorem is false" from "the theorem is true but weaker than the surrounding
    prose implies". The second is the more likely failure mode here and is a High finding.
  - Report what you actually read. Do not claim coverage you do not have.

Python: bare 'python' resolves to a CPU-only torch install; that is fine for pure-Python/rational
scripts. If an import fails, retry with "C:/anaconda/python.exe". Never run anything model-scale.
`

const AGENTS = [
  {
    label: 'P1-measure-probability',
    file: 'P1-measure-probability.md',
    prompt: `${COMMON}

YOUR EXPERTISE: measure-theoretic probability — standard Borel spaces, Markov kernels, disintegration
of measures, regular conditional probability, absolute continuity, Radon-Nikodym derivatives, and the
almost-sure qualifiers that make or break such statements.

YOUR SCOPE — the measure-theoretic core of the full pointwise meta-agent package:
  docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md  (READ IN FULL)
  docs/derivations/2026-08-15-full-pointwise-meta-agent/construction-or-strongest-theorem.md
  docs/derivations/2026-08-15-full-pointwise-meta-agent/problem-contract.json
  docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/independent-reconstruction.md

QUESTIONS YOU MUST ANSWER, each with reconstructed proof or counterexample:
 1. The construction pushes a fine generative joint P_I, a selected posterior family Pi_{I,o,X}, and a
    correlated recognition law Q_{I,o,X} through ONE normalized recognition-independent Markov channel
    C_A : Y_I ~> Z_A, leaving the observation in O unchanged. Is the resulting parent triple actually
    well defined? Check normalization, measurability of the pushforward kernels, and whether the
    observation marginal is genuinely preserved rather than assumed preserved.
 2. Parent posterior DISINTEGRATION and ABSOLUTE CONTINUITY are claimed. Verify: does the standard
    disintegration theorem apply as invoked (standard Borel, sigma-finiteness, which measure is
    disintegrated over which)? Is the a.s.-uniqueness of the version handled, or does the argument
    silently pick a version and then use pointwise properties of it?
 3. The parent posterior is said to be a PUSHFORWARD of the fine selected posterior version. Does
    pushforward of a version of a conditional law generally give a version of the conditional law of
    the pushforward? This is the step most likely to be wrong. Either prove it under the stated
    hypotheses or build a counterexample. Absolute continuity of the fine law does NOT automatically
    survive pushforward under a non-injective channel.
 4. The evaluator: "induced by disintegration" vs "predeclared jointly measurable normalized family
    satisfying an explicit almost-sure compatibility condition". Are these genuinely separated, or
    does the induced case smuggle in the predeclared case's hypotheses? Is the compatibility
    condition stated with the right measure and the right null set?
 5. Every almost-sure qualifier: which measure, on which space, and is it the right one? The change
    log records a late repair adding a "Q_{A,o,X}-almost-surely" qualifier — check whether every
    OTHER a.s. statement in the derivation carries the correct measure.
 6. "All named parent marginals are derived projections and do not reconstruct the joints." Verify
    the derivation actually establishes the marginals as projections rather than defining them
    independently and then asserting consistency.

WRITE TO: ${OUT}/P1-measure-probability.md`,
  },
  {
    label: 'P2-information-vfe',
    file: 'P2-information-vfe.md',
    prompt: `${COMMON}

YOUR EXPERTISE: information theory and variational free energy — KL divergence on extended reals,
chain rules, conditional KL, data-processing, the ELBO/VFE decomposition, and the exact arithmetic
hazards of [0,+infty] versus finite tiers.

YOUR SCOPE — the informational core of the full pointwise meta-agent package:
  docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md  (READ IN FULL,
    concentrating on the KL chain, defect, VFE identity, zero-defect criterion, recovery)
  docs/derivations/2026-08-15-full-pointwise-meta-agent/claim-ledger.json
  docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/reviews/view-information-vfe.md
    (read this ONLY to see what the internal reviewer claimed to check, then check it yourself)

QUESTIONS YOU MUST ANSWER, each with reconstructed derivation or counterexample:
 1. THE KL CHAIN. The claim is an additive chain in [0,+infty]:
    KL(fine) = KL(parent) + Delta_A(o,X), with Delta_A a conditional-information defect.
    Reconstruct this from the chain rule for relative entropy. Verify it holds in the EXTENDED reals,
    including every case where a term is +infty. Additivity in [0,+infty] is safe; the danger is any
    place the text rearranges the identity into a subtraction. Find every such rearrangement.
 2. THE VFE IDENTITY. "Adding the same finite real -log p_X(o) to both KL terms gives an extended-real
    VFE identity; a finite VFE may be negative." Check this carefully: adding a finite constant to an
    extended-real quantity is fine, but the resulting object is no longer in [0,+infty], so any later
    step that uses nonnegativity of a VFE term is broken. Hunt for exactly that.
 3. THE ZERO-DEFECT CRITERION. "Without a finiteness premise, Delta_A = 0 exactly when the discarded
    conditional recognition and posterior laws agree Q_{A,o,X}-almost surely." Verify BOTH directions.
    The (<=) direction is easy. The (=>) direction requires that Delta_A be an integral of a
    conditional KL that vanishes iff the integrand vanishes a.e. — verify the integrand is genuinely
    a KL and that the null set is with respect to the correct measure. Watch for the case Delta_A=0
    because both sides are +infty, which the change log flags as a repaired defect; confirm the
    repair is complete and consistent everywhere.
 4. THE FINITE TIER. "Finite fine KL is required for ordinary subtraction F_I - F_A = Delta_A and for
    the stated two-way pairwise common-recovery equivalence." Check that EVERY use of the subtraction
    form in the derivation AND in the integrated manuscript prose is fenced by the finiteness premise.
    An unfenced use anywhere is a High finding.
 5. PAIRWISE COMMON RECOVERY. State the recovery theorem precisely as the document does, then verify
    the two-way equivalence. Then check the separate claim that "family-wide recovery still requires
    simultaneous hypotheses" — is the failure of the naive family-wide statement actually
    demonstrated, or merely asserted as a caveat?
 6. Is Delta_A actually the object the surrounding text calls it? The prose calls it a
    "conditional-information VFE defect". Verify the identification with a conditional mutual
    information or conditional KL, or find that the identification is looser than claimed.

WRITE TO: ${OUT}/P2-information-vfe.md`,
  },
  {
    label: 'P3-counterexamples-pointwise',
    file: 'P3-counterexamples-pointwise.md',
    prompt: `${COMMON}

YOUR EXPERTISE: constructing and destroying finite counterexamples. You verify that an exhibited
witness actually witnesses the claimed negative statement, and you check that the negative statement
being witnessed is the interesting one rather than a premise-deleted strawman.

YOUR SCOPE — the five finite negative constructions:
  docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/counterexample-proofs.md (READ IN FULL, 594 lines)
  docs/derivations/2026-08-15-full-pointwise-meta-agent/counterexample-register.md
  docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/finite_nongaussian_witness.py (466 lines)
  docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/finite-nongaussian-output.json

THE FIVE CLAIMED NEGATIVE RESULTS:
  N1 full-law reconstruction from marginals FAILS
  N2 split-channel VFE FAILS
  N3 model-marginal-only evaluator compatibility FAILS
  N4 agreement does NOT follow from trivial holonomy
  N5 joint invariance does NOT follow from marginal invariance

DO ALL OF THE FOLLOWING:
 1. EXECUTE the witness script and record the ACTUAL output:
      cd "${REPO}/docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence"
      python finite_nongaussian_witness.py
    Report the real exit code and real stdout. The package claims 51 of 51 checks pass and that
    normal and optimized (-O) runs are byte-identical; verify BOTH by actually running both.
 2. For EACH of N1..N5, independently recompute the numbers by hand or with your own short script
    (write scratch scripts under the system temp dir, not in the repo). Do the exhibited finite
    objects actually have the claimed properties? Recompute at least the KL values, the marginals,
    and the invariance/holonomy checks yourself.
 3. STRAWMAN CHECK — this is the most important part. For each of N1..N5, ask: does the witness
    refute the interesting claim, or does it refute a version of the claim with a premise deleted?
    The final report itself concedes "Split-channel and incompatible-evaluator witnesses refute
    premise-deleted overreach rather than the conditional common-channel theorem." Determine for each
    of the five whether the negative result constrains the positive theory at all, or whether it is
    a no-op that was never plausible. A negative result that only refutes something nobody claimed is
    a Medium finding about the value of the certification, and you should say so plainly.
 4. Check that the witness script's checks correspond to the mathematical statements in
    counterexample-proofs.md. A script can pass 51/51 checks that do not test the theorem. Map each
    of the 51 checks to the claim it is supposed to support, and flag any claim with no corresponding
    executable check and any check that tests something trivial.
 5. The final report says the five existential negative claims are verified by DERIVATION evidence
    with supports:true and that no COUNTEREXAMPLE evidence kind is attached. Check whether this
    bookkeeping choice hides anything.

WRITE TO: ${OUT}/P3-counterexamples-pointwise.md`,
  },
  {
    label: 'P4-gauge-holonomy',
    file: 'P4-gauge-holonomy.md',
    prompt: `${COMMON}

YOUR EXPERTISE: gauge theory and fiber bundles — principal bundles, associated bundles, connections,
parallel transport, holonomy, equivariance, cocycle conditions, and gauge-fixing.

YOUR SCOPE:
 (a) The holonomy branch of the pointwise meta-agent package:
     docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md
       (the holonomy-blindness / raw-retention sections)
     docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/reviews/view-gauge-holonomy.md
       (read only to see what was claimed checked, then check it yourself)
 (b) The notation program's bundle split, which touched the whole manuscript:
     docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation-standard.md
     docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/notation-registry.json
     git diff ${BASE} ${HEAD} -- Theory/02_geometry.tex Theory/05c_pullback_geometry.tex Theory/appendix_notation.tex overview.md

QUESTIONS YOU MUST ANSWER:
 1. HOLONOMY BLINDNESS. The claim: under typed actions, full fine-law covariance, compatible selected
    posterior versions, channel equivariance, evaluator covariance, and fixed-(o,X) isotropy, the
    parent datum is blind to holonomy on the same slice; the alternative branch is raw root-framed
    holonomy retention. Reconstruct this. Specifically:
      - Is "holonomy blindness" a theorem or a definitional consequence of the hypotheses? Count how
        many of the six hypotheses are doing real work versus assuming the conclusion. If the
        hypotheses are jointly strong enough to make the statement vacuous, that is a High finding.
      - Is the isotropy hypothesis at fixed (o,X) an assumption about the group action or about the
        data? Which?
      - Does the channel-equivariance hypothesis have any nontrivial model, or is the only channel
        satisfying it the trivial one? Exhibit a nontrivial example or report that you could not.
 2. Is there an actual CONNECTION and an actual PARALLEL TRANSPORT in this pointwise construction, or
    is "holonomy" being used for a discrete composition of transition maps with no curvature content?
    The construction is explicitly pointwise at one r_* and explicitly does not glue over U_A. A
    holonomy statement at a single point is suspicious — determine what loop the holonomy is around.
 3. THE BUNDLE SPLIT. The 8/15 work renamed the root gauge bundle P -> \\mathscr P_G and separated it
    from a scale-local bundle, with commit 3f5f49b "docs: correct scale-bundle notation" repairing a
    "generic scale theorem typing". Verify: are the two bundles genuinely different objects with
    different structure groups/base spaces, or is this a rename dressed as a mathematical
    correction? Check that the separation is applied consistently in Theory/02, Theory/05c,
    Theory/07b, appendix_notation.tex and overview.md — find any surviving conflation.
 4. Check whether any cocycle or equivariance condition asserted in the 8/15 additions is actually
    verified, versus declared. Gauge-theoretic writing frequently asserts equivariance of a
    constructed object without checking it; look for exactly that.

WRITE TO: ${OUT}/P4-gauge-holonomy.md`,
  },
  {
    label: 'P5-category-operational',
    file: 'P5-category-operational.md',
    prompt: `${COMMON}

YOUR EXPERTISE: algebra and category theory — monoids, congruences, syntactic monoids and the
Myhill-Nerode/Schutzenberger theory, universal properties and terminality, quotient categories, and
topological algebra (compact right-topological monoids, Ellis's theorem, Feller kernels, compact
metrizable quotients).

YOUR SCOPE — the operational intervention extensions package:
  docs/derivations/2026-08-14-operational-intervention-extensions/evidence/direct-derivation.md (READ IN FULL)
  docs/derivations/2026-08-14-operational-intervention-extensions/construction-or-strongest-theorem.md
  docs/derivations/2026-08-14-operational-intervention-extensions/evidence/prior-hard-operational-reduction-proof.md
  docs/derivations/2026-08-14-operational-intervention-extensions/claim-ledger.json
  and the integrated prose in overview.md (the operational-intervention-boundary section)

QUESTIONS YOU MUST ANSWER:
 1. TERMINALITY. The claim: for a fixed monoid A and response Phi with pi : A ->> Syn(Phi), every
    response-compatible surjection q : A ->> B with Phi = psi q admits a UNIQUE surjective unital
    homomorphism h : B ->> Syn(Phi) with pi = h q and \\bar Phi h = psi. Reconstruct this proof
    completely. Check: is h well defined (the kernel containment argument), is it a homomorphism, is
    it surjective, is it unique, and is unitality actually established rather than assumed?
 2. NOVELTY. This is, on its face, the syntactic-monoid universal property — the coarsest
    response-compatible congruence, i.e. the Myhill-Nerode / syntactic congruence theorem, in a
    two-sided contextual form. Determine precisely what is new here versus what is textbook. Cite
    primary sources by name (Rabin-Scott, Myhill, Nerode, Schutzenberger, Pin's "Varieties of Formal
    Languages", Eilenberg). If the result is a restatement of a classical theorem, say so plainly and
    make it a Medium (novelty/attribution) finding. If there IS a genuine extension, say exactly what
    it is. Use WebSearch/WebFetch to check the literature; do not rely on memory alone.
 3. THE MINIMALITY CLAIM. "When A is finite this minimizes protocol-class cardinality only." Verify
    the minimality argument, and verify the fence — the text repeatedly insists this is NOT raw
    minimal realization. Check whether the fence is honored everywhere the result is used
    downstream, especially in overview.md and Theory/SPEC.md.
 4. THE TOPOLOGICAL CLAIM. "Under compact-metrizable monoid and continuous-response hypotheses, a
    countable dense contextual signature realizes a compact metrizable quotient with continuous
    multiplication and response." This is the hardest claim in the package. Verify:
      - Is the quotient Hausdorff? A quotient of a compact metrizable space by an equivalence
        relation is compact metrizable iff the relation is CLOSED. Is closedness established?
      - Is joint continuity of multiplication on the quotient proved, or only separate continuity?
        This distinction is exactly where compact right-topological semigroup theory lives, and
        conflating them would be a Critical finding.
      - What role does the countable dense contextual signature actually play? Is it used to
        metrize, or to separate points, or merely rhetorically?
 5. The overview prose adds: "On a finite DAG, declared normalized standard-Borel kernel families with
    jointly measurable evaluations give a Borel retained response. The construction supplies an
    algebraic quotient but does not by itself establish a standard-Borel quotient." Verify this
    honest-looking caveat is actually the correct caveat, and that nothing downstream uses the
    standard-Borel quotient it disclaims.

WRITE TO: ${OUT}/P5-category-operational.md`,
  },
  {
    label: 'P6-blackwell-comparison',
    file: 'P6-blackwell-comparison.md',
    prompt: `${COMMON}

YOUR EXPERTISE: comparison of statistical experiments (Blackwell/Le Cam), garbling and sufficiency,
convex geometry of experiment representations, binary symmetric channels, Markov semigroups, and heat
kernels on the circle.

YOUR SCOPE — the quantitative claims of the operational intervention extensions package:
  docs/derivations/2026-08-14-operational-intervention-extensions/evidence/counterexample-proofs.md (READ IN FULL)
  docs/derivations/2026-08-14-operational-intervention-extensions/evidence/recompute.py (495 lines)
  docs/derivations/2026-08-14-operational-intervention-extensions/evidence/recompute-output.json
  docs/derivations/2026-08-14-operational-intervention-extensions/counterexample-register.md

CLAIMS TO VERIFY QUANTITATIVELY:
 1. THE BSC PAIR. The chains L(1/4,1/3) and L(1/3,1/4) are said to have the SAME passive retained law
    but to be nonidentifiable in three distinct ways. Independently recompute the passive retained
    law of both and confirm they are actually equal. Then:
 2. MARKED-SOFT FACE DIAMETERS. Claimed exact values (1-2*epsilon)/3 and (1-2*epsilon)/2, "with
    strict-interior witnesses". Derive these two numbers from scratch. What norm/metric is "diameter"
    taken in? An unstated metric would make the numbers meaningless. Confirm the two are unequal for
    all admissible epsilon and that unequal diameters genuinely obstruct isomorphism in the declared
    category.
 3. RANDOMIZED AFFINE NONIDENTIFIABILITY. "a nonzero fifteen-coordinate contextual determinant forces
    randomized equivalence to be equality and every admitted affine convolution isomorphism restricts
    to the forbidden hard isomorphism." Recompute that determinant yourself and report its exact
    value. Verify the logic: nonzero determinant => the affine map is determined => it restricts to a
    hard isomorphism that was already refuted. Check for a gap between "affine convolution
    isomorphism" and "affine isomorphism".
 4. THE CIRCLE HEAT PAIR. "the ordered heat chains H_s H_t and H_t H_s have the same passive retained
    law, yet H_s strictly Blackwell-dominates H_t and their soft response sets are strictly nested."
    Note H_s and H_t COMMUTE (heat semigroup on the circle), so H_s H_t = H_t H_s as operators — the
    claim must therefore be about ORDERED experiments/protocols, not about the composite kernel.
    Determine exactly what distinguishes the two ordered chains if their composite is identical, and
    whether the claimed distinction is a real experimental difference or an artifact of the encoding.
    This is the single highest-value check in your scope. For s < t, H_s strictly Blackwell-dominates
    H_t is standard (H_t = H_{t-s} H_s, a garbling) — verify the strictness and verify the soft
    response set nesting is strict rather than merely non-strict.
 5. EXECUTE the recompute script and record ACTUAL output:
      cd "${REPO}/docs/derivations/2026-08-14-operational-intervention-extensions/evidence"
      python recompute.py
    Compare its output to recompute-output.json. Report any mismatch. Check whether the script uses
    exact rational arithmetic or floating point, and whether any claimed "exact" value is actually a
    float comparison with a tolerance.
 6. Write your own independent verification script (in the system temp dir, NOT in the repo) for at
    least the BSC passive-law equality and the face diameters, and report its output.

WRITE TO: ${OUT}/P6-blackwell-comparison.md`,
  },
  {
    label: 'P7-rg-coarsegraining',
    file: 'P7-rg-coarsegraining.md',
    prompt: `${COMMON}

YOUR EXPERTISE: renormalization group theory, coarse-graining, effective actions, lumpability and
exact decimation, and the conditions under which a coarse-graining map is consistent (semigroup
property, commuting diagram, fixed points).

YOUR SCOPE — the RG-facing surfaces changed on 8/15:
  solid_RG_theory.md (READ IN FULL, 27933 bytes; then read the 8/15 diff: git diff ${BASE} ${HEAD} -- solid_RG_theory.md)
  git diff ${BASE} ${HEAD} -- Theory/06_general_coarsegraining.tex Theory/07b_agent_network_rg.tex Theory/06a_generative_gaussian.tex
  docs/derivations/2026-08-14-pointwise-meta-agent-rg/ (the 8/14 predecessor, for continuity)

QUESTIONS YOU MUST ANSWER:
 1. Read solid_RG_theory.md in full and judge whether it is a solid RG theory. Specifically: is there
    a genuine RG semigroup (composition of coarse-grainings equals a single coarse-graining at the
    composed scale), or only a single-step coarse-graining map called RG? Is there a flow, a fixed
    point, or a relevant/irrelevant operator classification, or is the RG language decorative?
 2. The 8/15 pointwise meta-agent theorem is explicitly POINTWISE at one r_*, explicitly does NOT glue
    over U_A, and explicitly does not establish a canonical coarse channel or partition. An RG
    coarse-graining requires exactly the things the theorem disclaims: a canonical channel, a scale
    parameter, and composability. Determine whether solid_RG_theory.md and Theory/07b now depend on
    something the pointwise theorem does not supply. If the RG story is written as if the meta-agent
    construction supports it and the construction explicitly does not, that is a High finding.
 3. Check the 8/15 additions to Theory/07b_agent_network_rg.tex (+153 lines) and
    Theory/06_general_coarsegraining.tex (+29 lines) line by line. What exactly was added, and is it
    proved, cited, or asserted?
 4. Does the coarse-graining respect the KL/VFE structure — i.e. is there a monotonicity or
    contraction statement under coarse-graining, and is it proved with the right direction of
    inequality? Data-processing gives KL contraction under a channel; verify any such use has the
    channel on the correct side.
 5. Is the "scale" in the scale-local bundle the same scale as the RG scale? If two different scale
    notions are being identified without argument, report it.

WRITE TO: ${OUT}/P7-rg-coarsegraining.md`,
  },
  {
    label: 'P8-integration-overclaim',
    file: 'P8-integration-overclaim.md',
    prompt: `${COMMON}

YOUR EXPERTISE: claim auditing. You compare what a manuscript ASSERTS against what its supporting
derivations actually PROVE, and you find every place where scope quietly widens between the proof and
the prose.

YOUR SCOPE — the integration surfaces. Read the 8/15 diff for each:
  git diff ${BASE} ${HEAD} -- overview.md
  git diff ${BASE} ${HEAD} -- Theory/SPEC.md
  git diff ${BASE} ${HEAD} -- Theory/appendix_claim_ledger.tex
  git diff ${BASE} ${HEAD} -- Theory/05d_relational_inference.tex
  git diff ${BASE} ${HEAD} -- Theory/01_introduction.tex Theory/03_probability.tex Theory/04_generative.tex
  git diff ${BASE} ${HEAD} -- docs/STATUS.md
Ground truth is what the two packages actually prove:
  docs/derivations/2026-08-15-full-pointwise-meta-agent/final-report.md and its evidence/ directory
  docs/derivations/2026-08-14-operational-intervention-extensions/final-report.md and its evidence/

METHOD — build a claim-by-claim table. For EVERY substantive assertion added on 8/15 to overview.md,
SPEC.md, appendix_claim_ledger.tex, and Theory/05d, record:
  (claim as written) | (where the proof is supposed to be) | (what the proof actually establishes) |
  (verdict: SUPPORTED / OVERSTATED / UNSUPPORTED / UNVERIFIABLE)
Put this table in your findings file. It is your primary deliverable — build it incrementally and
save after every few rows.

SPECIFIC THINGS TO HUNT:
 1. The manuscript status ESTABLISHED is asserted for the "full pointwise candidate-parent theorem".
    The theorem is pointwise at one r_*, one X, one admitted observation, one declared channel, and
    does not glue. Does the word "full" in the manuscript mislead about which of those it is full in?
    Does anything downstream treat it as more than one point?
 2. The finiteness fence. The KL chain is additive in [0,+infty]; the subtraction F_I - F_A = Delta_A
    and the recovery equivalence require FINITE fine KL. Find EVERY place in the integrated prose
    that uses the subtraction or the recovery equivalence WITHOUT the finiteness premise. The change
    log records two late repairs in this exact area (fe08359, f4b1a61) plus one more for a missing
    a.s. qualifier — check whether the repairs are complete across all integration surfaces or only
    the ones that were scanned.
 3. Conditional theorems presented as unconditional. The pointwise theorem's affirmative part is
    conditional on standard-Borel, normalized-common-channel, evaluator, finite-KL, and
    holonomy-branch premises. Find integration text that drops a premise.
 4. appendix_claim_ledger.tex gained 140 lines. Check every added ledger row: does its stated status
    match the package's actual evidence, and does its stated scope match the frozen contract?
 5. The "Say this, and not more" boilerplate in overview.md was heavily rewritten. Read the new
    version against the packages and report any sentence in it that is not supported.
 6. Check for claims that were WEAKENED or REMOVED on 8/15 without the change being recorded — a
    silent retraction is as much a finding as an overclaim.

WRITE TO: ${OUT}/P8-integration-overclaim.md`,
  },
  {
    label: 'P9-selfcert-falsifiability',
    file: 'P9-selfcert-falsifiability.md',
    prompt: `${COMMON}

YOUR EXPERTISE: philosophy of science and epistemics of verification — falsifiability, severity of
tests, circularity, self-certification, and the difference between a process that produces confidence
and a process that produces evidence.

YOUR SCOPE — the certification machinery itself, in BOTH packages:
  */adversarial-report.json  and  */evidence/adversarial-attacks.md
  */evidence/oracle-erasure.md
  */evidence/independent-reconstruction.md
  docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/reviews/  (all four view-*.md)
  */release.json, */claim-ledger.json, */problem-contract.json, */dependency-dag.json
  docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/release-provenance.json
  docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/release-assembly.json
  docs/change-logs/2026-08-15.md

QUESTIONS YOU MUST ANSWER:
 1. THE SIXTEEN ATTACKS. Read every attack in adversarial-attacks.md. For each: was it a severe test
    (could it plausibly have succeeded and killed the claim) or a soft ball? Classify all sixteen.
    Then ask the question the portfolio cannot ask itself: what is the OBVIOUS attack that is NOT in
    the portfolio? Name at least three attacks a hostile referee would make that the portfolio omits.
 2. ORACLE ERASURE. The record claims desired-conclusion cues were removed and closure recomputed
    from typed assumptions alone. Assess whether this procedure can do what it claims when the same
    agent performs both the derivation and the erasure. Is there any mechanical artifact that would
    survive an outside check, or is the record purely a self-report?
 3. INDEPENDENT RECONSTRUCTION. It claims to rebuild the closure "without using the direct proof as
    its outline". Compare the two documents structurally (section order, lemma order, notation,
    phrasing). Is it genuinely independent, or a paraphrase? Quantify: how many of the load-bearing
    steps appear in the same order with the same decomposition?
 4. THE FOUR DOMAIN VIEWS. All four APPROVE at Critical/High/Medium 0/0/0. In a 550-line novel
    measure-theoretic derivation, a 0/0/0 result across four independent expert views is itself
    evidence about the reviewers, not the proof. Assess.
 5. PROVENANCE NON-CIRCULARITY. release-provenance.json claims three one-way snapshots and no mutual
    raw-hash fixed point. Verify the hash chain actually has the claimed structure — recompute at
    least one SHA-256 with a shell command and confirm it matches. Report whether the hashes bind the
    content they claim to bind.
 6. FALSIFIABILITY OF THE TARGET. Read problem-contract.json. The contract distinguishes "existential
    negative conjuncts" from "refuted universal claims" and defines "in-domain falsifiers". State, in
    one sentence, what observation or construction would falsify the released target. If you cannot
    state one, the target is unfalsifiable as frozen, and that is a High finding.
 7. THE LEDGER STATE. The user's own verification protocol holds that LLM judgment cannot close a
    claim and that agreement among agents is not evidence. The package closes 'target' as
    EVIDENCE_VERIFIED on the strength of derivations, internal reviews, and a deterministic script.
    Judge whether that closure is legitimate under that protocol. Be specific about which evidence,
    if any, would be eligible.

WRITE TO: ${OUT}/P9-selfcert-falsifiability.md`,
  },
  {
    label: 'P10-rigor-sweep',
    file: 'P10-rigor-sweep.md',
    prompt: `${COMMON}

YOUR TASK: a rigor sweep of the prose added on 2026-08-15. First invoke the 'rigor-sweep' skill via
the Skill tool and follow its procedure. That skill treats every hedge as a debt to pay down rather
than a fence to accept.

YOUR SCOPE — only text ADDED or CHANGED on 8/15. Get it with:
  git diff ${BASE} ${HEAD} -- overview.md solid_RG_theory.md
  git diff ${BASE} ${HEAD} -- Theory/05d_relational_inference.tex Theory/07b_agent_network_rg.tex Theory/02_geometry.tex Theory/03_probability.tex Theory/06_general_coarsegraining.tex
  git diff ${BASE} ${HEAD} -- Theory/SPEC.md
  docs/derivations/2026-08-15-full-pointwise-meta-agent/evidence/direct-derivation.md
  docs/derivations/2026-08-14-operational-intervention-extensions/evidence/direct-derivation.md

HUNT FOR, and for each occurrence RESOLVE rather than merely flag:
  - "declared", "admitted", "where retained", "under the stated hypotheses" used to avoid stating
    the hypothesis. This corpus uses "declared" very heavily; determine in each case whether it names
    a specific hypothesis or hides an unproved assumption.
  - "essentially", "morally", "one can show", "it follows that", "clearly", "standard", "routine"
  - vague quantifiers: "several", "various", "suitable", "appropriate", "generic", "typical"
  - approximations with no error term: "approximately", "to leading order", "up to"
  - "it is well known" / "standard" with no citation — for each, either supply the primary source or
    mark it as an unpaid debt
  - assertions of existence with no construction
  - any place a limit, sum, or exchange of order is performed without justification

For each hedge, do ONE of:
  (a) PAY IT DOWN: supply the missing step, exact constant, bound, or primary-source citation.
  (b) SHARPEN IT: restate as the precise conditions under which the claim holds.
  (c) MARK IT OPEN: state exactly what holds, under what assumptions, and precisely what remains open.
Never simply record that a hedge exists.

Report counts by category and by file, then the resolved items. Prioritize hedges in load-bearing
mathematical steps over hedges in framing prose, and say which is which.

WRITE TO: ${OUT}/P10-rigor-sweep.md`,
  },
]

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['agent', 'status', 'file_written', 'counts', 'headline_findings', 'coverage_note'],
  properties: {
    agent: { type: 'string' },
    status: { type: 'string', enum: ['COMPLETE', 'PARTIAL'] },
    file_written: { type: 'string', description: 'absolute path of the findings file written' },
    counts: {
      type: 'object',
      additionalProperties: false,
      required: ['critical', 'high', 'medium', 'low'],
      properties: {
        critical: { type: 'integer' },
        high: { type: 'integer' },
        medium: { type: 'integer' },
        low: { type: 'integer' },
      },
    },
    headline_findings: {
      type: 'array',
      maxItems: 8,
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['severity', 'title', 'location', 'one_line_evidence'],
        properties: {
          severity: { type: 'string', enum: ['Critical', 'High', 'Medium', 'Low'] },
          title: { type: 'string' },
          location: { type: 'string' },
          one_line_evidence: { type: 'string' },
        },
      },
    },
    things_that_checked_out: {
      type: 'array',
      maxItems: 8,
      items: { type: 'string' },
      description: 'claims you verified as correct — report these honestly',
    },
    coverage_note: { type: 'string', description: 'what you read in full, sampled, and did not reach' },
  },
}

phase('Investigate')
log(`Dispatching ${AGENTS.length} expert investigators over the 2026-08-15 work at ${HEAD}`)

const results = await parallel(
  AGENTS.map((a) => () =>
    agent(a.prompt, { label: a.label, phase: 'Investigate', schema: SCHEMA })
      .then((r) => (r ? { ...r, agent: a.label } : { agent: a.label, status: 'PARTIAL', file_written: `${OUT}/${a.file}`, counts: { critical: 0, high: 0, medium: 0, low: 0 }, headline_findings: [], coverage_note: 'AGENT DIED OR WAS SKIPPED — re-dispatch on resume' }))
  )
)

const clean = results.filter(Boolean)
const totals = clean.reduce(
  (acc, r) => ({
    critical: acc.critical + (r.counts?.critical || 0),
    high: acc.high + (r.counts?.high || 0),
    medium: acc.medium + (r.counts?.medium || 0),
    low: acc.low + (r.counts?.low || 0),
  }),
  { critical: 0, high: 0, medium: 0, low: 0 }
)

log(`Wave 1 done. Totals C/H/M/L = ${totals.critical}/${totals.high}/${totals.medium}/${totals.low}`)

return { head: HEAD, totals, results: clean }
