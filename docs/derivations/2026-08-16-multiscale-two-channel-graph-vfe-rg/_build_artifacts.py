"""Build the rigorous-theory-search run package: digest, headers, hashes, JSON."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
SCHEMA = "rigorous-theory-search/v1"

TARGET = {
    "statement": (
        "For a finite directed two-channel gauge network of agents at one shared contextual "
        "point c_* in C, with generally non-flat belief and model transports Omega^b, Omega^m, "
        "a possibly cyclic skeleton, normalized directed source rows beta and gamma, external "
        "receiver occupancies alpha^b and alpha^m, and joint directed edge-event laws "
        "eta^b_ij = alpha^b_i beta_ij and eta^m_ij = alpha^m_i gamma_ij: (1) construct a "
        "normalized finite-depth generative joint P_theta(do,dW|X) containing belief and model "
        "presentations at every scale, the edge-event and transport data, stochastic partition "
        "variables, retained holonomy marks, and parent variables, together with one normalized "
        "correlated recognition kernel Q_phi(dW|o,X); (2) derive the exact variational free "
        "energy F = -log p_theta(o|X) + KL(Q_phi || Pi_{theta,o,X}) and its conditional-KL "
        "decomposition, identifying every normalizer, base measure, absolute-continuity "
        "condition, and finite-versus-extended-real boundary; and (3) decide whether descent of "
        "that variational free energy alone selects a nondegenerate partition and produces "
        "persistent nested blocks."
    ),
    "kind": "MATHEMATICAL",
    "quantifier_class": "MIXED",
    "quantifiers": (
        "Existential in conjuncts (1) and (2): there exists a normalized finite-depth joint and "
        "recognition disintegration for which the displayed VFE identity and its conditional-KL "
        "decomposition hold. Universal in conjunct (3): for every admissible tower satisfying "
        "the declared typing, descent of the tower VFE selects a nondegenerate partition. The "
        "negative certificate is matched to conjunct (3)."
    ),
    "domains": [
        "Finite scale set L = {0,...,S} with S finite.",
        "Finite agent set V at scale 0, all at one context point c_* in C.",
        "Nonempty standard Borel agent spaces Y_{i,s} = B_{i,s} x M_{i,s} x Xi_{i,s}, with "
        "B_{i,s} a subset of P(Z^b_{i,s}) (law-valued belief coordinate).",
        "Finite label pools Lambda^b_{s+1}, Lambda^m_{s+1} for memberships.",
        "Standard Borel observation space O and structural space X.",
        "Standard Borel G-space for transports; G is the common principal structure group with "
        "two representations rho_b and rho_m.",
    ],
    "codomains": [
        "Probability measures on O x W, where W collects every retained random object.",
        "Extended reals R union {+infinity} for the variational free energy.",
        "Probability measures on G for the conditional law of dressed coarse transports.",
    ],
    "regularity": (
        "Every generative and recognition factor is a normalized measurable Markov kernel "
        "conditioning only on strictly earlier variables in a declared finite partial order. "
        "The evidence density satisfies 0 < p_theta(o|X) < infinity. The recognition law is "
        "absolutely continuous with respect to the selected posterior version. The observation "
        "term is integrable from above: E_{Q_phi}[(log L_theta(o|Z_0,X))^+] < infinity. Kernel "
        "densities, where used, are jointly measurable versions relative to one family-level "
        "dominating measure per kernel."
    ),
    "measures": [
        "sigma-finite reference nu^O on the observation space.",
        "Declared sigma-finite references on each belief-presentation space P(Z^b), each model "
        "presentation space, and each auxiliary space.",
        "Counting measure on all finite factors: memberships, edge occupations, source labels, "
        "label pools.",
        "Haar measure on G when G is locally compact; counting measure when G is finite.",
        "The tower reference is the finite product of the above and is sigma-finite; an infinite "
        "product of non-probability sigma-finite factors is not, which is the concrete continuum "
        "obstruction.",
    ],
    "boundary_conditions": [
        "The likelihood attaches only at scale 0.",
        "Structural data X and each X_A = chi_A(X) stay outside every random channel.",
        "Retained boundary data at a block are the dressed boundary generators V^x_e in one "
        "simultaneous root-gauge orbit.",
        "No boundary condition at infinity is imposed; the theory is finite-design.",
    ],
    "symmetries": [
        "Passive frame rechoice in each channel, acting by rho_b and rho_m of the same group "
        "element; the passive coordinate group is G x G while the principal structure group is G.",
        "Node relabeling, under which an admissible partition selector must satisfy "
        "S(P.X) = P S(X) Q^T.",
        "Based-loop holonomy H^x_I : pi_1(Gamma_I, r_I) -> G, conjugated by root rechoice; "
        "non-flat holonomy is admitted and is not penalized toward the identity.",
    ],
    "equivalence": (
        "Two towers are equivalent when their generative joints agree as measures after the "
        "declared passive frame rechoices and node relabelings, and when the retained marks agree "
        "as one simultaneous root-gauge orbit. Separately quotienting each holonomy is not an "
        "admissible equivalence because it loses orientation relative to root features and "
        "boundary legs."
    ),
    "premises": [
        "All scale-0 agents lie at one contextual point; no physical length, lattice, translation "
        "symmetry, momentum space, or tree is assumed.",
        "The finite directed network may contain cycles.",
        "Each ordered edge carries two generally non-flat transports, one per channel.",
        "Rows beta and gamma are normalized conditional source laws; alpha^b and alpha^m are "
        "external receiver occupancies; the joint edge-event laws are their products.",
        "No generative factor may read the recognition law, its marginals or parameters, or the "
        "posterior the joint determines.",
        "Any additive decomposition of the free energy must be derived from a declared "
        "factorization of the two laws or from a normalized Gibbs factor with its partition "
        "function; otherwise it is a composite potential.",
        "A correlated recognition law is not reconstructed from its marginals.",
        "Multivariate Gaussian families are an optional computational realization and are not "
        "used in any hypothesis.",
    ],
    "modeling_postulates": [
        "Reading A: the belief coordinate is a law-valued component of the latent sample, a point "
        "of the associated-bundle fiber, rather than a marginal of the recognition law.",
        "Capacity restriction on the parent space and downward-kernel family, declared as the "
        "condition under which the partition posterior can differ from its prior.",
        "Label exclusivity of the augmented attention likelihood.",
        "Constant-row recognition restriction for the row free energy.",
        "Conditional independence of endpoint assignments given the fine edge, where the product "
        "endpoint kernel is used.",
    ],
    "search_priors": ["SEARCH_PRIOR_AFFIRMATIVE"],
    "permitted_theorems": [
        "Kolmogorov extension for standard Borel coordinate spaces.",
        "Tonelli and Fubini under sigma-finiteness.",
        "Conditional relative-entropy chain rule on standard Borel spaces.",
        "Data-processing inequality for relative entropy with its equality condition.",
        "Disintegration of measures on standard Borel spaces.",
        "P(X) is Polish when X is Polish (Kechris, Classical Descriptive Set Theory, 17.23).",
        "LaSalle invariance principle.",
        "Klein and Randic: effective resistance is a metric on a connected graph.",
        "Chung: directed graph Laplacian via the Perron vector.",
        "Freidlin-Wentzell exit-time asymptotics; Tikhonov-Fenichel slow manifolds.",
    ],
    "negative_certificate_kind": "COUNTEREXAMPLE",
    "falsification_criterion": (
        "Conjunct (3) is refuted by exhibiting one admissible tower, satisfying the declared "
        "typing, on which the minimized tower variational free energy is constant across "
        "partitions, so that the inferred partition law equals its prior. Conjuncts (1) and (2) "
        "are refuted by exhibiting a factor whose measurable codomain depends on the realized "
        "value of an earlier variable, or by exhibiting an admissible tower satisfying the stated "
        "regularity for which the displayed sum is not well defined in R union {+infinity}."
    ),
    "literature_policy": (
        "Primary sources only for load-bearing statements about arXiv:2305.10491 (Berman, "
        "Klinger, Stapleton) and arXiv:2412.12988 (Gabrielli, Garlaschelli, Patil, Serrano). "
        "Titles, author lists, version dates, journal references, abstracts, and any cited "
        "equation must be checked against the primary. A review's open problem is never cited as "
        "a solved theorem. Any statement carried from a secondary or project note must be labeled "
        "as such at the point of use and recorded as a numerical or provenance-limited item in "
        "the claim table. A bounded search is not a worldwide search and establishes no priority."
    ),
}


def canonical(obj) -> bytes:
    return json.dumps(
        obj, ensure_ascii=False, allow_nan=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


DIGEST = hashlib.sha256(canonical(TARGET)).hexdigest()
CONTRACT_ID = f"contract-sha256-{DIGEST}"
HEADER = (
    "<!-- rigorous-theory-search-metadata "
    + json.dumps(
        {"schema_version": SCHEMA, "contract_id": CONTRACT_ID, "target_digest": DIGEST},
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    + " -->\n"
)

MD_ARTIFACTS = [
    "counterexample-register.md",
    "construction-or-strongest-theorem.md",
    "final-report.md",
]

for name in MD_ARTIFACTS:
    path = RUN / name
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    if lines and lines[0].startswith("<!-- rigorous-theory-search-metadata"):
        lines = lines[1:]
    path.write_text(HEADER + "".join(lines), encoding="utf-8", newline="\n")


def sha(rel: str) -> str:
    h = hashlib.sha256()
    with (RUN / rel).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


P1 = "REPORT-part1-vfe-and-construction.md"
P2 = "REPORT-part2-parent-partition-graphrg.md"
P3 = "REPORT-part3-holonomy-blocks-dynamics.md"
P4 = "REPORT-part4-literature-experiment-verdict.md"
CX = "counterexample-register.md"
ATK = "evidence/adversarial-attacks.md"
REC = "evidence/independent-reconstruction.md"
ERA = "evidence/oracle-erasure.md"

BASE = {"schema_version": SCHEMA, "contract_id": CONTRACT_ID, "target_digest": DIGEST}


def ev(eid, kind, path, scope, side, supports=True):
    return {
        "id": eid,
        "kind": kind,
        "supports": supports,
        "scope": scope,
        "side_conditions": side,
        "artifact_path": path,
        "artifact_sha256": sha(path),
    }


TYPING_SIDE = [
    "Nonempty standard Borel spaces with sigma-finite references.",
    "Every factor is a normalized measurable Markov kernel of finite scope.",
    "Evidence density strictly positive and finite.",
]

EVIDENCE = [
    ev(
        "ev-construction", "DERIVATION", P1,
        "Proposition 1: the depth-S tower joint is a probability measure with no normalizer "
        "other than the evidence, by reverse-order integration along the declared partial order.",
        TYPING_SIDE + ["Finite label pools fix the measurable codomain of every later factor."],
    ),
    ev(
        "ev-decomposition", "DERIVATION", P1,
        "Theorem 2: the exact VFE equals the observation term plus conditional relative "
        "entropies over the top prior, both channels' memberships, graph data, holonomy marks, "
        "and parent-child kernels, as an identity in R union {+infinity}.",
        TYPING_SIDE + [
            "Recognition disintegrated along the same ordering; Q << Pi.",
            "E[(log L)^+] < infinity; necessity of this condition is unproved.",
            "Chain rule applied at the measure level; no infinite quantity is subtracted.",
        ],
    ),
    ev(
        "ev-degeneracy", "COUNTEREXAMPLE", P2,
        "Proposition 5 and Corollary 6: with an unrestricted parent space and downward-kernel "
        "family, min_Q F is constant across partitions, so the partition posterior equals its "
        "prior. Capacity restriction and positive node-count cost are separate sufficient "
        "design mechanisms; their joint necessity is open.",
        [
            "Requires the copy construction Z_{1,I} = Y_{0,I}, K^0_I = delta, P_1 = flat child law.",
            "Block factorization of K_down is respected because the product of Diracs is a Dirac.",
            "Refutes only the unrestricted case; says nothing about a capacity-bounded tower.",
        ],
    ),
    ev(
        "ev-parent", "DERIVATION", P2,
        "Proposition 3: parts (a)-(e) establishing that an instantaneous deterministic "
        "pushforward parent and an independently declared same-time parent cause cannot be "
        "imposed together, and the exhaustive trichotomy of normalized repairs.",
        [
            "Part (d) assumes a nonatomic reference on the parent space.",
            "Part (e) assumes the generative law is a normalized directed kernel composition.",
            "A soft-constrained reciprocal factor is an instance of mechanism (iii) and still "
            "owes a finite-normalizer proof.",
        ],
    ),
    ev(
        "ev-holonomy", "DERIVATION", P3,
        "Proposition 8 (empty fixed set implies infinite distortion), Proposition 9 (coarse "
        "dressed transports convolve when consecutive marks are conditionally independent, the "
        "converse being false by the Z_3 witness), and the measure-one criterion for coarse "
        "holonomy blindness.",
        [
            "Proposition 8 requires an equivariant admitted parent family.",
            "Proposition 9's convolution direction requires conditional independence, which is "
            "itself unproved for the declared blocking.",
            "Barycenters require Bochner integrability and need not lie in the represented group.",
        ],
    ),
    ev(
        "ev-nonequilibrium", "DERIVATION", P3,
        "Proposition 10: one C^1 scalar with symmetric positive-definite mobility yields LaSalle "
        "convergence, so participatory feedback derivable from that scalar cannot sustain "
        "nonequilibrium; the four admissible mechanisms are enumerated.",
        [
            "Assumes smooth dynamics and symmetric positive-definite mobility.",
            "Not extended to projected flows on the simplex boundary or indefinite "
            "preconditioners; that extension is an open obligation.",
        ],
    ),
    ev(
        "ev-intrinsic-scale", "DERIVATION", P4,
        "Proposition 11: with Perron receiver occupancy the additive symmetrization of the "
        "edge-event law preserves occupancy and equals Chung's directed Laplacian, giving a "
        "gauge-invariant symmetric PSD operator supporting effective-resistance and commute-time "
        "metrics and a well-typed diffusion scale.",
        [
            "Requires irreducibility of the attention row matrix for the Perron vector.",
            "Effective resistance is a metric per Klein and Randic, cited as an applicable theorem.",
            "Transported Fisher-Rao is a pseudometric; path independence needs holonomy "
            "stabilization.",
        ],
    ),
    ev(
        "ev-literature-bks", "PRIMARY_SOURCE", P4,
        "arXiv:2305.10491 (Berman, Klinger, Stapleton, 'Bayesian Renormalization'), v1 2023-05-17, "
        "v3 2023-10-09, MLST 4(4) 045011: abstract, Eq. (44) pushforward inverse Fisher metric, "
        "Eq. (55) Fisher-diagonal shell, and the checked absence of any treatment of directed "
        "graphs, network partitions, or holonomy.",
        [
            "Stiff/sloppy to relevant/irrelevant is the paper's interpretive claim, not a theorem.",
            "Section 3.1 argues spectrally while section 4.2 implements diagonally.",
            "Authors describe the connections as largely conceptual.",
        ],
    ),
    ev(
        "ev-literature-netrg", "PRIMARY_SOURCE", P4,
        "arXiv:2412.12988 (Gabrielli, Garlaschelli, Patil, Serrano, 'Network Renormalization'), "
        "v1 2024-12-17, Nature Reviews Physics 7:203-219 (2025): abstract and the confirmed "
        "absence of any claim that a framework solves simultaneous renormalization of topology "
        "and dynamics.",
        [
            "The section 6 open-problem heading list was not re-verified verbatim this session "
            "because HTML and PDF fetches truncated; it is carried from a project note and is "
            "marked as provenance-limited in the claim table.",
            "A review's open problem is not cited as a solved theorem anywhere in this run.",
        ],
    ),
    ev(
        "ev-counterexamples", "COUNTEREXAMPLE", CX,
        "Register of twenty-four exact counterexamples: eight constructed in this run and sixteen "
        "reused from the project's established register, covering shortcut failures in "
        "clustering, holonomy, coarse attention, membership semantics, normalization, closure, "
        "lumpability, and recovery.",
        [
            "Each entry refutes a specific named shortcut, not the surrounding theory.",
            "Entries marked [live] are cited, not reproved, here.",
        ],
    ),
]

ASSUMPTIONS = [
    {
        "id": "as-typing",
        "kind": "MODELING_POSTULATE",
        "statement": (
            "All spaces are nonempty standard Borel with sigma-finite references; every "
            "generative and recognition factor is a normalized measurable Markov kernel "
            "conditioning only on strictly earlier variables; the likelihood attaches only at "
            "scale 0; 0 < p_theta(o|X) < infinity."
        ),
    },
    {
        "id": "as-reading-a",
        "kind": "MODELING_POSTULATE",
        "statement": (
            "Reading A: the belief coordinate q^b_i is a law-valued component of the latent "
            "sample, not a marginal of the recognition law. Under Reading B the transported "
            "divergences are functionals of the recognition law and the row free energies are "
            "composite potentials rather than ELBO sectors."
        ),
    },
    {
        "id": "as-integrability",
        "kind": "MODELING_POSTULATE",
        "statement": (
            "E_{Q_phi}[(log L_theta(o|Z_0,X))^+] < infinity, so the signed observation term "
            "cannot be minus infinity and the seven-group sum is well defined in R union "
            "{+infinity}. Necessity of this condition is unproved."
        ),
    },
    {
        "id": "as-capacity",
        "kind": "MODELING_POSTULATE",
        "statement": (
            "A declared capacity restriction on the parent space Z_{s+1}, downward-kernel family "
            "K_down, and parent prior P_{s+1} is one sufficient anti-degeneracy mechanism. A "
            "strictly positive cost per parent node is another. Their joint necessity over a "
            "declared model class is open."
        ),
    },
    {
        "id": "as-attention",
        "kind": "MODELING_POSTULATE",
        "statement": (
            "Label exclusivity of the augmented attention likelihood and the constant-row "
            "recognition restriction, under which the row free energy is an exact free-energy "
            "sector with energy E_{Q}[D_ij] and inverse temperature one."
        ),
    },
    {
        "id": "as-endpoint",
        "kind": "MODELING_POSTULATE",
        "statement": (
            "Conditional independence of the receiver and source block assignments given the fine "
            "edge, where the product endpoint kernel K = C tensor C is used; otherwise a "
            "correlated endpoint kernel is required."
        ),
    },
]


def claim(cid, statement, quantifiers, kind, state, ev_ids, as_ids, falsifier):
    return {
        "id": cid,
        "statement": statement,
        "quantifiers": quantifiers,
        "kind": kind,
        "target_digest": DIGEST,
        "state": state,
        "assumption_ids": as_ids,
        "evidence_ids": ev_ids,
        "bridge_premise_ids": [],
        "falsifier": falsifier,
    }


CLAIMS = [
    claim(
        "target", TARGET["statement"], TARGET["quantifiers"], "MATHEMATICAL", "INCONCLUSIVE",
        ["ev-construction", "ev-decomposition", "ev-degeneracy", "ev-counterexamples"],
        ["as-typing", "as-reading-a", "as-integrability", "as-capacity"],
        "Conjuncts (1) and (2) fail if a factor's measurable codomain depends on a realized "
        "earlier value, or if an admissible tower satisfying the regularity has an ill-defined "
        "sum. Conjunct (3) fails affirmatively if some declared capacity restriction is exhibited "
        "under which descent provably selects a persistent nondegenerate partition.",
    ),
    claim(
        "construction",
        "The depth-S two-channel tower joint, containing belief and model presentations, "
        "edge-event and transport data, stochastic partitions over fixed finite label pools, "
        "retained holonomy marks, and parent variables, is a probability measure carrying no "
        "normalizer other than the evidence.",
        "For every admissible (theta, X) satisfying the declared typing.",
        "MATHEMATICAL", "INCONCLUSIVE", ["ev-construction"], ["as-typing"],
        "Exhibit a displayed factor whose measurable codomain depends on the realized value of an "
        "earlier variable, breaking the reverse-order integration.",
    ),
    claim(
        "decomposition",
        "The exact tower VFE equals -log p_theta(o|X) + KL(Q_phi || Pi) in R union {+infinity} "
        "and decomposes into the observation term plus conditional relative entropies over the "
        "top prior, both channels' memberships, the graph data, the holonomy marks, and the "
        "parent-child kernels; the partition and parent coordinate minimizers are the "
        "corresponding Gibbs posteriors, the parent energy collecting every conditional "
        "divergence whose generative factor conditions on the parent coordinate.",
        "For every recognition law disintegrated along the declared ordering with Q << Pi and the "
        "stated integrability.",
        "MATHEMATICAL", "INCONCLUSIVE", ["ev-decomposition"],
        ["as-typing", "as-integrability", "as-attention"],
        "Exhibit an admissible tower meeting the regularity for which the displayed sum is not "
        "well defined, or a group of terms not obtainable from the declared factorization.",
    ),
    claim(
        "degeneracy",
        "With an unrestricted parent space and downward-kernel family, the minimized tower VFE is "
        "constant across partitions, so the inferred partition law equals its prior and no "
        "hierarchy is selected. Capacity restriction and node-count cost are sufficient design "
        "mechanisms, one per degeneracy; their joint necessity over a declared model class is open.",
        "There exists an admissible tower, for every partition, on which the minimum is the same; "
        "hence the universal selection claim fails.",
        "MATHEMATICAL", "INCONCLUSIVE", ["ev-degeneracy", "ev-counterexamples"],
        ["as-typing", "as-capacity"],
        "Show the copy construction violates a hypothesis actually imposed on the tower, for "
        "instance an a priori bound on the parent space that is already part of the typing.",
    ),
    claim(
        "parent-impossibility",
        "An instantaneous deterministic pushforward parent and an independently declared "
        "same-time parent cause cannot be imposed together: the parent becomes a statistic whose "
        "prior is not free, a freely declared prior overdetermines the model, a hard constraint "
        "annihilates a Gibbs normalizer against a nonatomic reference, and two generative arrows "
        "form a directed 2-cycle with no normalization. The normalized repairs are exactly "
        "recognition demotion, temporal delay, and one undirected factor with a proved finite "
        "normalizer.",
        "For every standard Borel pair and Borel coarse map satisfying the stated conditions.",
        "MATHEMATICAL", "INCONCLUSIVE", ["ev-parent", "ev-counterexamples"], ["as-typing"],
        "Exhibit a normalized joint realizing both a deterministic pushforward and a nondegenerate "
        "independently declared parent prior with genuine downward influence.",
    ),
    claim(
        "holonomy-obstruction",
        "Non-flat connection data are retained exactly as the simultaneous root-framed orbit "
        "together with the conditional law of dressed transports; H_#Q = Q is necessary and "
        "sufficient only on the zero-distortion sector; flatness implies stabilization, flatness "
        "does not imply agreement, and stabilization does not imply flatness; an empty intersection "
        "of the holonomy fixed set with the admitted family makes a zero-distortion parent "
        "nonexistent.",
        "For every finite connected block, channel, and equivariant admitted parent family.",
        "MATHEMATICAL", "INCONCLUSIVE", ["ev-holonomy", "ev-counterexamples"], ["as-typing"],
        "Prove that every equivariant admitted family in this program contains a holonomy-fixed "
        "point, or exhibit a mean dressed transport that always lies in the represented group.",
    ),
    claim(
        "nonequilibrium",
        "Within one C^1 scalar with symmetric positive-definite mobility the flow converges by "
        "LaSalle, so participatory cross-scale feedback derivable from that scalar cannot sustain "
        "nonequilibrium; driven controls, an antisymmetric sector, delay, or non-gradient "
        "stochastic drift is required.",
        "For every bounded trajectory of such a flow.",
        "MATHEMATICAL", "INCONCLUSIVE", ["ev-nonequilibrium"], ["as-typing"],
        "Exhibit a projected natural-gradient flow with symmetric positive-definite mobility and "
        "one C^1 scalar possessing a nonconstant omega-limit set.",
    ),
    claim(
        "intrinsic-scale",
        "The edge-event law supplies a gauge-invariant directed Laplacian with exactly zero row "
        "sums; under Perron receiver occupancy its additive symmetrization preserves occupancy and "
        "coincides with Chung's directed Laplacian, yielding effective-resistance and commute-time "
        "metrics and a well-typed diffusion scale, whereas 1/beta, the Gibbs surprisal, and raw "
        "relative entropy are not metrics.",
        "For every irreducible attention row matrix on a finite directed graph.",
        "MATHEMATICAL", "INCONCLUSIVE", ["ev-intrinsic-scale", "ev-counterexamples"], ["as-typing"],
        "Exhibit an irreducible row matrix whose Perron symmetrization fails to preserve occupancy, "
        "or a triangle-inequality violation for effective resistance on the symmetrized graph.",
    ),
    claim(
        "literature",
        "Bayesian renormalization supplies a model-space relevance criterion that treats no "
        "directed graph, network partition, or holonomy; the network-renormalization review names "
        "the simultaneous renormalization of topology and dynamics as open and does not claim any "
        "framework solves it; and neither supplies a partition selector, a renormalization of "
        "non-flat transports, or a closure theorem for a directed two-channel gauge network.",
        "For the cited versions of arXiv:2305.10491 and arXiv:2412.12988 as checked.",
        "MATHEMATICAL", "INCONCLUSIVE",
        ["ev-literature-bks", "ev-literature-netrg"], ["as-typing"],
        "A passage in either primary source treating directed two-channel gauge networks, "
        "holonomy, or a proved solution to coupled topology-and-dynamics renormalization.",
    ),
]

EDGES = [
    {"from": "target", "to": "construction"},
    {"from": "target", "to": "decomposition"},
    {"from": "target", "to": "degeneracy"},
    {"from": "target", "to": "parent-impossibility"},
    {"from": "target", "to": "holonomy-obstruction"},
    {"from": "target", "to": "nonequilibrium"},
    {"from": "target", "to": "intrinsic-scale"},
    {"from": "target", "to": "literature"},
    {"from": "decomposition", "to": "construction"},
    {"from": "degeneracy", "to": "decomposition"},
]

ALL_CLAIMS = [c["id"] for c in CLAIMS]

ATTACKS = [
    {
        "id": "A1", "claim_ids": ["construction"], "disposition": "SUSTAINED",
        "attack": "A random occupied vertex set breaks the fixed-measurable-space requirement and "
                  "with it the reverse-order integration argument. The occupied set at scale s+1 "
                  "is determined by R_s, which the generative order samples after P_S and P^s_G, "
                  "so an earlier kernel's codomain would depend on a later variable.",
        "response": "SUSTAINED on external review (PR #17, finding H1). The original response "
                    "asserted that fixed finite label pools fix every later codomain, which is the "
                    "correct repair, but the body of Part 1 nonetheless indexed Z_s and G_s by the "
                    "random occupied sets V_s. The repair was described and never implemented, so "
                    "marking this REJECTED was itself an error. Part 1 section 3.1 and the "
                    "construction summary now index every scale-s object by the fixed pool "
                    "Lambda_s, with occupancy the derived predicate alpha^{x,s}_A > 0, and record "
                    "the disjoint-union alternative. Differing belief and model partitions now "
                    "route through Proposition 7's declared correspondence rather than presuming a "
                    "common occupied index.",
        "artifact_path": ATK, "artifact_sha256": sha(ATK),
    },
    {
        "id": "A2", "claim_ids": ["decomposition"], "disposition": "PARTIALLY_SUSTAINED",
        "attack": "The sum mixes a signed observation term with terms that can be +infinity, so an "
                  "identity in R union {+infinity} is not justified as stated.",
        "response": "Six groups are nonnegative and sum unambiguously; the integrability condition "
                    "bounds the observation term from below. Necessity of that condition is "
                    "unproved and is recorded as an open obligation.",
        "artifact_path": ATK, "artifact_sha256": sha(ATK),
    },
    {
        "id": "A3", "claim_ids": ["degeneracy"], "disposition": "REJECTED",
        "attack": "The copy construction is a straw model that no modeler would use, so the "
                  "proposition does not show a sensible tower is partition-blind.",
        "response": "The proposition is a necessity result: one admissible witness suffices to show "
                    "the variational principle alone cannot select, which is exactly what makes the "
                    "capacity restriction obligatory rather than optional.",
        "artifact_path": ATK, "artifact_sha256": sha(ATK),
    },
    {
        "id": "A4", "claim_ids": ["parent-impossibility"], "disposition": "PARTIALLY_SUSTAINED",
        "attack": "Nobody imposes an exact deterministic constraint inside a Gibbs model, so the "
                  "nullity argument refutes an unasserted position and the trichotomy is not "
                  "exhaustive.",
        "response": "A soft penalty is an instance of the undirected mechanism and inherits its "
                    "unproved normalizer obligation; the nullity argument targets the exact "
                    "combination the target names. Stating the soft model and proving finiteness of "
                    "its normalizer remains open.",
        "artifact_path": ATK, "artifact_sha256": sha(ATK),
    },
    {
        "id": "A5", "claim_ids": ["holonomy-obstruction"], "disposition": "REJECTED",
        "attack": "The witness family excludes its own fixed point by hand, so the obstruction is an "
                  "artifact of an artificial family.",
        "response": "The family is equivariant, which is the hypothesis the surrounding theory "
                    "imposes; requiring a family to contain its holonomy fixed points is precisely "
                    "the extra condition the proposition identifies as necessary.",
        "artifact_path": ATK, "artifact_sha256": sha(ATK),
    },
    {
        "id": "A6", "claim_ids": ["nonequilibrium"], "disposition": "PARTIALLY_SUSTAINED",
        "attack": "Real implementations use nonsmooth simplex projections and sometimes indefinite "
                  "preconditioners, so the LaSalle conclusion does not apply.",
        "response": "Projection onto a convex set still decreases the objective; an indefinite "
                    "preconditioner leaves the natural-gradient setting. Extending or refuting the "
                    "proposition for projected flows and indefinite mobilities is recorded as open.",
        "artifact_path": ATK, "artifact_sha256": sha(ATK),
    },
    {
        "id": "A7", "claim_ids": ["literature", "intrinsic-scale"],
        "disposition": "PARTIALLY_SUSTAINED",
        "attack": "Several statements about the primary papers are carried from project notes rather "
                  "than checked against the primary, which is the failure the target's literature "
                  "policy forbids.",
        "response": "Titles, authors, versions, journal references, abstracts, the two cited BKS "
                    "equations, and the absence of graph, partition, and holonomy content were "
                    "checked against the primary this session. The review's section 6 heading list "
                    "was not, because the fetches truncated; it is labeled provenance-limited at the "
                    "point of use and marked in the claim table.",
        "artifact_path": ATK, "artifact_sha256": sha(ATK),
    },
    {
        "id": "A9", "claim_ids": ["decomposition", "holonomy-obstruction"],
        "disposition": "SUSTAINED",
        "attack": "External review PR #17, findings H2, H3, H4, M1, M3, M4. The parent Gibbs update "
                  "omitted the membership, graph, and holonomy conditional divergences that also "
                  "condition on Z_{s+1}; the dressed-transport law omitted the soft endpoint "
                  "factor K^x(I,J|i,j) and was therefore unnormalized outside hard partitions; the "
                  "convolution statement was promoted to an iff whose converse is false; Theorem 2 "
                  "omitted its integrability premise; flatness was said not to imply stabilization, "
                  "though the identity stabilizes every law; and a support inclusion was asserted "
                  "at a tier with no declared topology.",
        "response": "All six sustained and repaired. V_{s+1} now sums the four parent-dependent "
                    "conditional divergences, with a two-state witness (C26) showing the truncated "
                    "form moves the argmin, not merely the value. The mu^x_{IJ} numerator now "
                    "carries K^x(I,J|i,j), with witness C27; the restricted form is retained only "
                    "for hard assignment. Proposition 9 keeps the forward implication only, with "
                    "the Z_3 witness C25. Theorem 2 lists the integrability condition as "
                    "hypothesis (iv) and states that it is not implied by positive finite evidence "
                    "and absolute continuity. Section 9.2(B) now states the chain flatness implies "
                    "stabilization, flatness does not imply agreement, stabilization does not imply "
                    "flatness. The blindness criterion is stated as mu_loop(Stab(Q_I)) = 1, with "
                    "the support form deferred to a declared topological tier.",
        "artifact_path": ATK, "artifact_sha256": sha(ATK),
    },
    {
        "id": "A8", "claim_ids": ALL_CLAIMS, "disposition": "PARTIALLY_SUSTAINED",
        "attack": "The target is a conjunction and the run closes only part of it, so no claim to "
                  "have addressed the target should be made.",
        "response": "Precisely why the terminal status is INCONCLUSIVE. Each conjunct receives its "
                    "own disposition; conjunct (3) is refuted only in the unrestricted case and the "
                    "capacity-bounded question is left open rather than absorbed.",
        "artifact_path": ATK, "artifact_sha256": sha(ATK),
    },
]

(RUN / "problem-contract.json").write_text(
    json.dumps({**BASE, "target": TARGET}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)

(RUN / "claim-ledger.json").write_text(
    json.dumps(
        {**BASE, "assumptions": ASSUMPTIONS, "evidence": EVIDENCE, "claims": CLAIMS},
        ensure_ascii=False, indent=2,
    ) + "\n",
    encoding="utf-8",
    newline="\n",
)

(RUN / "dependency-dag.json").write_text(
    json.dumps({**BASE, "edges": EDGES}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)

(RUN / "adversarial-report.json").write_text(
    json.dumps(
        {
            **BASE,
            "attacks": ATTACKS,
            "independent_reconstruction": {
                "claim_ids": ALL_CLAIMS,
                "method": "Re-derive each load-bearing interface from the frozen contract, ledger, "
                          "and DAG without the report narrative, and check that the cited evidence "
                          "proves the exact recorded statement.",
                "result": "PASS",
                "conclusion": "Seven interfaces reconstructed and agreeing; three discrepancies "
                              "found and folded back before release (conditioning of the "
                              "holonomy-mark factor, promotion of the observation integrability "
                              "condition, restriction of the degeneracy statement to the minimized "
                              "free energy). Performed by the authoring model, so it is a "
                              "reconstruction and not independent-model corroboration.",
                "artifact_path": REC,
                "artifact_sha256": sha(REC),
            },
            "oracle_erasure": {
                "claim_ids": ALL_CLAIMS,
                "method": "Remove the affirmative prior from the logical context, scan premises, "
                          "modeling postulates, regularity hypotheses, and load-bearing steps by "
                          "hand for direct or paraphrased dependence, and recompute the target's "
                          "dependency closure.",
                "result": "PASS",
                "conclusion": "No node loses support. The capacity bound, the only assumption "
                              "capable of carrying the prior's content, is invoked exclusively in "
                              "the negative direction, and the degeneracy witness is "
                              "anti-correlated with the prior, so that result survives erasure a "
                              "fortiori. Passing shows only that the prior was unnecessary.",
                "artifact_path": ERA,
                "artifact_sha256": sha(ERA),
            },
        },
        ensure_ascii=False, indent=2,
    ) + "\n",
    encoding="utf-8",
    newline="\n",
)

(RUN / "approach-registry.json").write_text(
    json.dumps(
        {
            **BASE,
            "mechanism_families": [
                {
                    "family_id": "family-ordered-kernel-tower",
                    "core_mechanism": "Ordered composition of normalized Markov kernels along a "
                                      "finite scale-indexed partial order, with the likelihood at "
                                      "scale 0 only.",
                    "target_obligation_ids": ["target", "construction", "decomposition"],
                    "representation": "Measure-level tower on a fixed product of standard Borel "
                                      "spaces with finite label pools.",
                    "invariant_or_obstruction": "Normalization without a partition function; the "
                                                "obstruction is any factor whose codomain depends "
                                                "on a realized earlier value.",
                    "obligations": ["Prove normalization and the conditional-KL decomposition."],
                    "bridge": "Conditional relative-entropy chain rule at the measure level.",
                    "failure_test": "A factor with a value-dependent measurable codomain.",
                    "verified_results": ["construction", "decomposition"],
                    "open_gaps": ["Necessity of the observation integrability condition."],
                    "novelty_fingerprint": "ordered kernel tower + label pools + two-channel "
                                           "memberships + holonomy marks as generated variables",
                    "disposition": "mature",
                },
                {
                    "family_id": "family-capacity-degeneracy",
                    "core_mechanism": "Exhibit an admissible tower whose observation marginal is "
                                      "partition-independent, forcing the minimized free energy to "
                                      "be constant across partitions.",
                    "target_obligation_ids": ["target", "degeneracy"],
                    "representation": "Copy parent space with Dirac downward kernel.",
                    "invariant_or_obstruction": "The minimized free energy depends on the partition "
                                                "only through the observation marginal.",
                    "obligations": ["Refute the universal selection conjunct."],
                    "bridge": "Minimum of the free energy equals minus log evidence.",
                    "failure_test": "A typing hypothesis excluding the copy construction.",
                    "verified_results": ["degeneracy"],
                    "open_gaps": ["Whether some capacity bound restores selection and persistence."],
                    "novelty_fingerprint": "copy-parent witness + block-factorization compatibility "
                                           "+ posterior-equals-prior corollary",
                    "disposition": "mature",
                },
                {
                    "family_id": "family-edge-event-geometry",
                    "core_mechanism": "Treat the joint directed edge-event law as the primitive "
                                      "gauge-invariant object: push it, disintegrate it, and build "
                                      "a directed Laplacian from it.",
                    "target_obligation_ids": ["target", "intrinsic-scale"],
                    "representation": "Probability law on ordered node pairs plus normalized "
                                      "endpoint kernels.",
                    "invariant_or_obstruction": "Linear mass preservation under a fixed Markov "
                                                "pushforward; row averages are not additive.",
                    "obligations": ["Supply intrinsic scales that are genuine metrics."],
                    "bridge": "Perron occupancy identifies the symmetrization with Chung's "
                              "directed Laplacian.",
                    "failure_test": "Occupancy not preserved by symmetrization under a stationary "
                                    "receiver law.",
                    "verified_results": ["intrinsic-scale"],
                    "open_gaps": ["No rescaling kernel, hence no renormalization semigroup."],
                    "novelty_fingerprint": "edge-event law + Perron occupancy + Chung symmetrization "
                                           "+ effective-resistance metric + two-channel scale spectra",
                    "disposition": "mature",
                },
                {
                    "family_id": "family-holonomy-retention",
                    "core_mechanism": "Retain the conditional law of dressed transports rather than "
                                      "a barycenter, and read blindness at the measurable tier as "
                                      "a measure-one stabilizer condition.",
                    "target_obligation_ids": ["target", "holonomy-obstruction"],
                    "representation": "Markov kernel from the coarse state into probability "
                                      "measures on the structure group.",
                    "invariant_or_obstruction": "Empty intersection of the holonomy fixed set with "
                                                "the admitted family forces infinite distortion.",
                    "obligations": ["Treat non-flat connection data exactly."],
                    "bridge": "Pushforward of the joint edge-event-and-mark law.",
                    "failure_test": "An equivariant admitted family always containing a fixed point.",
                    "verified_results": ["holonomy-obstruction"],
                    "open_gaps": ["Conditional independence of consecutive dressed marks."],
                    "novelty_fingerprint": "dressed transport law + convolution under conditional "
                                           "independence + measure-one stabilizer criterion",
                    "disposition": "mature",
                },
                {
                    "family_id": "family-gradient-obstruction",
                    "core_mechanism": "Use LaSalle on one scalar with symmetric mobility to bound "
                                      "what cross-scale feedback can produce.",
                    "target_obligation_ids": ["target", "nonequilibrium"],
                    "representation": "Natural-gradient flow on the tower recognition parameters.",
                    "invariant_or_obstruction": "A single scalar plus symmetric mobility forbids a "
                                                "nonequilibrium steady state.",
                    "obligations": ["Say what participatory feedback requires."],
                    "bridge": "Enumeration of the four ways to break the hypotheses.",
                    "failure_test": "A nonconstant omega-limit set under the stated hypotheses.",
                    "verified_results": ["nonequilibrium"],
                    "open_gaps": ["Projected flows on simplex boundaries; indefinite mobilities."],
                    "novelty_fingerprint": "LaSalle bar + four-mechanism enumeration + "
                                           "non-integrability as the technical content of "
                                           "participatory feedback",
                    "disposition": "mature",
                },
                {
                    "family_id": "family-directed-cycle-obstruction",
                    "core_mechanism": "Show that a deterministic pushforward and an independent "
                                      "same-time cause cannot coexist, by disintegration, "
                                      "overdetermination, Fubini nullity, and absence of a "
                                      "topological ordering.",
                    "target_obligation_ids": ["target", "parent-impossibility"],
                    "representation": "Joint law on a child-parent pair with a Borel coarse map.",
                    "invariant_or_obstruction": "A directed 2-cycle has no normalized ordered "
                                                "composition.",
                    "obligations": ["Compare the three parent-influence mechanisms."],
                    "bridge": "Trichotomy of normalized repairs.",
                    "failure_test": "A normalized joint realizing both arrows nondegenerately.",
                    "verified_results": ["parent-impossibility"],
                    "open_gaps": ["Finite normalizer for the soft reciprocal model."],
                    "novelty_fingerprint": "four-part impossibility + exhaustive repair trichotomy",
                    "disposition": "mature",
                },
            ],
        },
        ensure_ascii=False, indent=2,
    ) + "\n",
    encoding="utf-8",
    newline="\n",
)

(RUN / "release.json").write_text(
    json.dumps(
        {
            **BASE,
            "checkpoint": None,
            "target_claim": "target",
            "terminal_status": "INCONCLUSIVE",
            "certificate_claim": None,
            "strongest_result": (
                "Theorem A: under standard-Borel typing, normalized ordered kernels, positive "
                "finite evidence, absolute continuity, and E[(log L)^+] < infinity, the depth-S "
                "two-channel tower is normalized with no partition function beyond the evidence; "
                "the exact VFE equals -log p + KL(Q || Pi) in R union {+infinity} and decomposes "
                "into the observation term plus conditional relative entropies over the top prior, "
                "both channels' memberships, the graph data, the holonomy marks, and the "
                "parent-child kernels; the partition and parent coordinate minimizers are Gibbs "
                "posteriors; pushing the joint directed edge-event laws and disintegrating gives "
                "normalized gauge-invariant coarse rows composing under nested memberships; and "
                "non-flat holonomy is retained exactly as a root-framed orbit with the conditional "
                "law of dressed transports. Paired negative result, Proposition 5: with an "
                "unrestricted parent space the tower free energy is exactly constant across "
                "partitions, so the partition posterior equals its prior."
            ),
            "unresolved_obligations": [
                "State and defend a capacity restriction under which the partition posterior "
                "differs from its prior.",
                "Construct a nondegenerate, relabeling-natural, gauge-compatible partition selector "
                "consistent with holonomy admissibility.",
                "Construct the rescaling and identification kernel making the coarse family a "
                "semigroup; without it there is no renormalization group, beta function, blocking "
                "ratio, or relevant/irrelevant classification.",
                "Prove or refute the six persistence hypotheses for the coupled flow on a generic "
                "cyclic graph, including a metastability statement.",
                "Prove or refute exact-image invariance of the retained sector and account for "
                "generated hyperedges.",
                "Prove or refute vanishing of the natural-gradient semiconjugacy defect, separating "
                "measurability of the discarded defect from horizontal conformality.",
                "Prove or refute conditional independence of consecutive dressed marks.",
                "Formulate and attempt the two-channel group-valued analogue of the "
                "multiscale-model uniqueness theorem.",
                "Build the Bayesian-RG bridge on a common state space with a proved monotone.",
                "Declare and account for one nonequilibrium mechanism with a distinguishing "
                "observable.",
                "Supply a continuum reference measure directly on a section space.",
                "Prove or refute necessity of the observation integrability condition.",
                "Re-fetch section 6 of arXiv:2412.12988 and confirm or correct the one "
                "provenance-limited row of the claim table.",
                "Prove or refute joint necessity of the capacity restriction and the "
                "node-count cost over a declared class of admissible towers (review M2).",
                "Determine whether the restricted dressed-transport sum and the "
                "endpoint-factor form can agree beyond hard assignment (review H3).",
                "Obtain cross-model verification of every derivation in this run.",
            ],
        },
        ensure_ascii=False, indent=2,
    ) + "\n",
    encoding="utf-8",
    newline="\n",
)

print("contract_id:", CONTRACT_ID)
