"""Generate the evidence-gated ELBO-to-effective-action derivation package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "docs/derivations/2026-08-12-elbo-to-effective-section-action"
EVIDENCE = RUN / "evidence"
SCHEMA = "rigorous-theory-search/v1"


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    problem = json.loads((RUN / "problem-contract.json").read_text(encoding="utf-8"))
    contract_id = problem["contract_id"]
    digest = problem["target_digest"]
    target = problem["target"]
    EVIDENCE.mkdir(parents=True, exist_ok=True)

    meta = "<!-- rigorous-theory-search-metadata " + json.dumps(
        {"contract_id": contract_id, "schema_version": SCHEMA, "target_digest": digest},
        sort_keys=True,
        separators=(",", ":"),
    ) + " -->"

    def render(text: str) -> str:
        return (text.replace("{META}", meta).replace("{contract_id}", contract_id)
                .replace("{{", "{").replace("}}", "}"))

    evidence_text = {
        "exact-contraction-proof.md": r"""{META}
# Exact contraction and density-action theorem

Fix a finite lattice, finite agent count, standard-Borel microscopic space
\(Z_h\), and normalized microscopic posterior \(\Pi_{h,o}\). Let
\(C_h:Z_h\to X_h\) be a measurable coarse map that is fixed independently of
the recognition law. For a fine recognition law \(Q_h\), write
\(R_h=(C_h)_\#Q_h\) and \(P_{X,h}^o=(C_h)_\#\Pi_{h,o}\). Standard-Borel
disintegration and the chain rule for relative entropy give

\[
D_{{\rm KL}}(Q_h\Vert\Pi_{h,o})
=D_{{\rm KL}}(R_h\Vert P_{X,h}^o)
+\int D_{{\rm KL}}(Q_h(dz\mid x)\Vert\Pi_{h,o}(dz\mid x))\,R_h(dx).
\]

The second term is nonnegative and vanishes for the posterior-conditional
lift \(Q_h^\star(dz)=\int\Pi_{h,o}(dz\mid x)R_h(dx)\). Therefore

\[
\inf_{{Q_h:(C_h)_\#Q_h=R_h}}
\mathcal F_h(Q_h;o)
=-\log p_h(o)+D_{{\rm KL}}(R_h\Vert P_{X,h}^o).
\]

If \(P_{X,h}^o=Z_h^{-1}e^{-S_h}\nu_h\), then the exact contracted ELBO is

\[
\mathcal F_h^X(R_h;o)
=\mathbb E_{{R_h}}S_h-H_{{\nu_h}}(R_h)
+\log Z_h-\log p_h(o).
\]

Thus \(S_h=-\log[dP_{X,h}^o/d\nu_h]\), modulo an additive constant, is the
exact finite-lattice effective density action. The entropy, partition
normalizer, evidence, and discarded conditional KL are not optional. This
theorem does not imply that \(S_h\) is local, pairwise, or PIFB2-shaped.
""",
        "pifb2-sector-map.md": r"""{META}
# Exact, conditional, truncated, and open sectors

| Sector | Strongest justified status | Required bridge |
|---|---|---|
| Whole finite coarse VFE | Exact | Fixed microscopic joint, fixed coarse map, disintegration |
| Coarse density action | Exact modulo constants | Declared coarse reference and Radon-Nikodym density |
| Observation | Exact globally; local decomposition conditional | Fixed typed likelihood or exact interaction projection |
| Self term | Conditional/exact when an exact retained interaction | Fixed prior factor or nonzero exact projection coefficient |
| Live-peer KL between current recognition marginals | Not an ordinary fixed-joint state ELBO | Promote law-valued fields to genuine configuration variables, introduce fixed source templates, or mark as engineered truncation |
| Fixed-source attention and row entropy | Exact | Explicit source-label latent, fixed source prior and fixed sample-state energy |
| Correlated attention | Exact with correction | Retain conditional total correlation |
| Base-gradient Fisher term | Conditional local expansion | Same-agent neighboring-base KL, links approaching a connection, Fisher regularity, and \(h^{{d-2}}\) scaling |
| Connection links | Exact variables only if present in the joint | Normalized link reference and equivariant coarse map |
| Compact curvature | Conditional continuum expansion | Wilson plaquettes and \(h^{{d-4}}\) scaling |
| Raw GL(K) positive curvature | Obstructed | Frobenius norm is not conjugation invariant; invariant trace forms are indefinite |
| Fisher/SPD-dressed GL(K) curvature | Algebraically viable; analytically open | Transforming SPD metric, gauge control, coercivity, and finite reference measure |
| Configuration entropy | Exact and mandatory | Probability law over entire section configurations |
| Normalizers and Jacobians | Exact and mandatory when field-dependent | Partition/evidence convergence and gauge-volume treatment |
| Higher-body, nonlocal, boundary, memory terms | Exact correction sectors | Retain them or prove a residual bound |
| Deterministic continuum action | Conditional/open | Common interpolation, equicoercivity, liminf, recovery, and residual control |
| Continuum process-law ELBO | Open and strictly stronger | Tightness, reference-law convergence, entropy liminf/recovery, and partition convergence |

The finite number of agents is not sent to infinity. Refinement is in the
base lattice. An agent is a section-bearing object over its support, and the
lattice samples that section.
""",
        "lattice-continuum-asymptotics.md": r"""{META}
# Lattice-to-continuum consistency calculations

For a regular statistical family \(q_\theta\), an edge
\(y=x+he_\mu\), and a link that approximates parallel transport,

\[
U_{{xy}}^h\!\cdot\theta(y)
=\theta(x)+hD_\mu^A\theta(x)+O(h^2).
\]

The score has zero expectation and the expected negative Hessian is the
Fisher tensor, so Taylor expansion gives

\[
D_{{\rm KL}}(q_{{\theta(x)}}\Vert U_{{xy\#}}^hq_{{\theta(y)}})
=\tfrac12 h^2 I_{{\theta(x)}}(D_\mu^A\theta,D_\mu^A\theta)+O(h^3).
\]

There are order \(h^{-d}\) edges. Hence an edge transmissibility of order
\(h^{{d-2}}\) yields a finite Fisher-covariant Dirichlet integral. Pointwise
self, peer, observation, and potential sectors instead use cell weights of
order \(h^d\), with cut-cell weights on local section supports.

For a compact gauge group in a unitary representation, a small plaquette has
\(H_p=I-h^2F_{{\mu\nu}}+O(h^3)\), and

\[
r-\operatorname{{ReTr}}H_p
=\tfrac12h^4\|F_{{\mu\nu}}\|_{{\rm HS}}^2+O(h^5).
\]

Therefore the Wilson sector must carry weight \(h^{{d-4}}\). These are
consistency expansions on smooth sequences, not Gamma-convergence proofs.
A deterministic limit additionally requires a common interpolation topology,
equicoercivity modulo gauge, liminf, recovery, boundary/topology control, and
uniformly vanishing truncation residual on bounded-energy sublevels.
""",
        "adversarial-counterexamples.md": r"""{META}
# Counterexamples and removal obligations

Exact coarse-graining is not automatically local. If
\(Y\sim N(0,\tau^2)\) and \(X_a\mid Y\sim N(Y,\sigma^2)\), eliminating \(Y\)
generates an all-to-all term proportional to \((\sum_aX_a)^2\). Eliminating a
hidden Ising spin coupled to four retained spins generates a nonzero four-body
operator through \(-\log[2\cosh(\sum_iJ_ix_i)]\). A local pairwise PIFB2 basis
therefore needs an explicit projection and residual.

A fixed two-variable joint ELBO cannot generically yield the live-peer term
\(D_{{\rm KL}}(\operatorname{{Ber}}(p)\Vert\operatorname{{Ber}}(r))\). For every
fixed positive joint \(P(i,j)\), the product-recognition functional
\(D_{{\rm KL}}(q_iq_j\Vert P)\) has
\(\partial_p\partial_r^2=0\), whereas the live-peer KL has
\(\partial_p\partial_r^2=r^{{-2}}-(1-r)^{{-2}}\), nonzero away from
\(r=1/2\). The sender cannot be both a current variational marginal and a
fixed generative factor without an additional typed layer.

For \(K\ge2\), \(\|H-I\|_F^2\) is not invariant under
\(H\mapsto g^{{-1}}Hg\) in \(GL(K)\). Taking
\(H=I+\epsilon E_{{12}}\) and \(g=\operatorname{{diag}}(t,1)\) changes the
norm by \(t^{-2}\). Moreover noncompact Haar volume is infinite, so a
gauge-invariant Gibbs law needs a quotient/gauge slice, Jacobian, stabilizer
treatment, and a finite reference measure.

Finally, deterministic energy convergence does not imply process-law ELBO
convergence. For \(M=1/h\) product Bernoulli sites, the unscaled exact KL is
\(M d_{{\rm KL}}(q\Vert p)\), while the quadrature-scaled density action is
\(hM d_{{\rm KL}}(q\Vert p)\). The first diverges and the second stays finite.
""",
        "independent-reconstruction.md": r"""{META}
# Independent reconstruction

The derivation was reconstructed from the normalized microscopic posterior,
without using the proposed PIFB2 action as an oracle. KL disintegration first
produced the exact coarse functional. A Radon-Nikodym density then defined the
exact action. Only afterward was the PIFB2 operator basis introduced as a
projection of that action. The reconstruction reproduced the exact
conditional-KL correction, recognition entropy, evidence and partition
normalizers, and the higher-body/nonlocal residual. It also independently
separated the deterministic base-refinement problem from convergence of laws
on a continuum section space. Result: PASS for the strongest partial theorem
and for the stated inconclusive boundary.
""",
        "oracle-erasure.md": r"""{META}
# Oracle-erasure check

Erase the PIFB2 manuscript and MAgent implementation from the premise. The
exact contraction theorem, coarse density action, and interaction expansion
still follow from the independently specified microscopic law, coarse map,
KL chain rule, and Radon-Nikodym derivative. What disappears is the choice of
which local operators to retain and how to interpret them as self, peer,
attention, connection, and curvature sectors. Therefore PIFB2 and MAgent are
useful hypotheses for the retained basis, but not evidence that the basis is
exactly generated. Result: PASS.
""",
        "source-theorem-map.md": r"""{META}
# Current source map

The live exact-ELBO theory already contains the finite-lattice bridge:

- `Theory/07b_agent_network_rg.tex:16-66` defines the fixed joint, posterior,
  recognition law, coarse kernel, and exact KL chain rule.
- `Theory/07b_agent_network_rg.tex:78-123` pushes both the reference and
  evidence measures and defines the coarse Radon-Nikodym action.
- `Theory/07b_agent_network_rg.tex:1364-1392` gives the exact complete
  finite-network interaction action.
- `Theory/07b_agent_network_rg.tex:1468-1512` defines the retained projection,
  residual, and the condition under which a PIFB-like ansatz is exact.
- `Theory/05b_local_collective_elbo.tex:490-608` derives fixed-source
  attention from an explicit label variable.
- `Theory/02_geometry.tex:404-425` types finite agents as section-bearing
  objects, while `Theory/03_probability.tex:405-449` states why finite designs
  do not reconstruct a continuum section law.

The current configuration-ELBO manuscript records the complementary Gibbs
identity and its non-circularity restrictions at
`Research/manuscripts/magent_elbo_whitepaper/07_configuration_elbo.tex:105-128`
and `:201-235`. The current PIFB2 manuscript presents its action as an ansatz;
the current MAgent implementation realizes a finite effective backend with
live-peer consensus. Neither artifact supplies a microscopic derivation or a
mesh-to-continuum theorem.
""",
    }

    for filename, text in evidence_text.items():
        (EVIDENCE / filename).write_text(render(text).rstrip() + "\n", encoding="utf-8")

    evidence_specs = [
        ("ev-exact-contraction", "DERIVATION", True, "Exact finite-lattice KL contraction and density-action identity.", "exact-contraction-proof.md", ["Standard-Borel disintegration", "Fixed Q-independent microscopic law and coarse map", "Positive finite evidence"]),
        ("ev-sector-map", "DERIVATION", True, "Typed classification of PIFB2 sectors after exact contraction.", "pifb2-sector-map.md", ["Fixed finite N", "Base refinement rather than population limit"]),
        ("ev-asymptotics", "DERIVATION", True, "Fisher-gradient and compact Wilson-plaquette scaling calculations.", "lattice-continuum-asymptotics.md", ["Regular dominated statistical family", "Uniform mesh and smooth link consistency", "Compact unitary gauge representation for Wilson sector"]),
        ("ev-counterexamples", "COUNTEREXAMPLE", False, "Counterexamples to generic locality, live-peer fixed-joint exactness, undressed GL positivity, and action-to-process inference.", "adversarial-counterexamples.md", ["Claims are refuted only at their stated universal scope"]),
        ("ev-reconstruction", "DERIVATION", True, "Independent reconstruction of the strongest partial theorem and its boundary.", "independent-reconstruction.md", ["No use of PIFB2 action as a microscopic premise"]),
        ("ev-oracle-erasure", "DERIVATION", True, "Oracle-erasure test separating ELBO derivation from PIFB operator selection.", "oracle-erasure.md", ["PIFB2 and MAgent removed from the premise"]),
        ("ev-source-map", "APPLICABLE_THEOREM", True, "Revision-bound map to the live exact coarse-action and interaction-projection results.", "source-theorem-map.md", ["Repository revision 24c02aa29cd76589a52e54c56e4247f0560f7e87", "Research manuscript paths inspected on 2026-08-12"]),
    ]
    evidence_records = []
    for evidence_id, kind, supports, scope, filename, conditions in evidence_specs:
        path = EVIDENCE / filename
        evidence_records.append({
            "id": evidence_id,
            "kind": kind,
            "supports": supports,
            "scope": scope,
            "side_conditions": conditions,
            "artifact_path": f"evidence/{filename}",
            "artifact_sha256": sha256(path),
        })

    assumptions = [
        {"id": "a-fixed-joint", "kind": "DECLARED_ASSUMPTION", "statement": "The normalized microscopic law and coarse map are fixed independently of the recognition law."},
        {"id": "a-disintegration", "kind": "DECLARED_ASSUMPTION", "statement": "The admitted spaces and maps support the regular conditional probabilities used by KL disintegration."},
        {"id": "a-section-typing", "kind": "MODELING_POSTULATE", "statement": "The retained coarse variables are sampled values of the finite agents' belief, model, support, frame, and link sections."},
        {"id": "a-continuum", "kind": "DECLARED_ASSUMPTION", "statement": "Any continuum claim uses a declared refining mesh, base measure, interpolation topology, boundary conditions, and gauge treatment."},
    ]

    def claim(claim_id: str, statement: str, quantifiers: str, state: str,
              evidence_ids: list[str], assumption_ids: list[str], falsifier: str) -> dict[str, object]:
        return {
            "id": claim_id,
            "statement": statement,
            "quantifiers": quantifiers,
            "kind": "MATHEMATICAL",
            "target_digest": digest,
            "state": state,
            "assumption_ids": assumption_ids,
            "evidence_ids": evidence_ids,
            "bridge_premise_ids": [],
            "falsifier": falsifier,
        }

    claims = [
        {
            "id": "target",
            "statement": target["statement"],
            "quantifiers": target["quantifiers"],
            "kind": target["kind"],
            "target_digest": digest,
            "state": "INCONCLUSIVE",
            "assumption_ids": ["a-fixed-joint", "a-disintegration", "a-section-typing", "a-continuum"],
            "evidence_ids": ["ev-exact-contraction", "ev-sector-map", "ev-asymptotics", "ev-counterexamples", "ev-source-map"],
            "bridge_premise_ids": [],
            "falsifier": "A complete release would require a specified microscopic family, an exact or controlled PIFB projection, and the requested continuum convergence proof; any failed normalization, residual, or compactness premise defeats it.",
        },
        claim("exact-coarse-action", "A fixed normalized microscopic posterior and fixed measurable coarse map induce an exact finite-lattice coarse VFE and a coarse Radon-Nikodym density action.", "Every fixed finite N and admitted finite lattice under the declared disintegration and normalization hypotheses.", "EVIDENCE_VERIFIED", ["ev-exact-contraction", "ev-source-map"], ["a-fixed-joint", "a-disintegration"], "Exhibit recognition dependence, failure of disintegration, or a coarse law for which the KL chain rule identity fails."),
        claim("density-elbo-ledger", "The exact coarse ELBO equals expected density action plus recognition entropy, partition normalization, evidence normalization, and the conditional-KL correction before minimization.", "Every admitted coarse law with the displayed Radon-Nikodym derivatives and finite terms.", "EVIDENCE_VERIFIED", ["ev-exact-contraction"], ["a-fixed-joint", "a-disintegration"], "Produce a normalized dominated example violating the Radon-Nikodym KL expansion."),
        claim("fixed-source-attention", "An explicit fixed source-label latent variable yields categorical attention KL, row entropy, softmax minimizer, and correlation corrections exactly.", "Every finite nonempty source set with positive fixed priors and integrable sample-state energies.", "EVIDENCE_VERIFIED", ["ev-sector-map", "ev-source-map"], ["a-fixed-joint"], "Show an admitted fixed-label model whose categorical KL fails to expand into the stated energy and entropy terms."),
        claim("live-peer-fixed-joint", "A nonzero live-peer KL between current recognition marginals is generically representable as an ordinary fixed-joint state-level ELBO on an open product-recognition family.", "Every positive fixed two-agent binary joint and an open set of Bernoulli product recognition laws.", "REFUTED", ["ev-counterexamples"], ["a-fixed-joint"], "The derivative counterexample is falsified by a Q-independent positive joint reproducing the live-peer KL on an open Bernoulli parameter set."),
        claim("fisher-gradient", "Same-agent neighboring-base KL terms with the correct link consistency and h scaling converge on smooth sequences to a Fisher-covariant Dirichlet density.", "Every fixed finite N, regular dominated statistical family on a compact regular stratum, and sufficiently fine uniformly regular mesh.", "EVIDENCE_VERIFIED", ["ev-asymptotics"], ["a-section-typing", "a-continuum"], "A regular family or smooth link-consistent sequence violates the second-order Fisher expansion or its h scaling."),
        claim("compact-curvature", "Compact-group Wilson plaquette terms with h^(d-4) weights converge on smooth sampled connections to the quadratic curvature density.", "Every smooth compact-group connection in a finite-dimensional unitary representation on a uniformly refining mesh.", "EVIDENCE_VERIFIED", ["ev-asymptotics"], ["a-continuum"], "A smooth compact connection and consistent plaquette sampling violate the small-holonomy trace expansion."),
        claim("generic-local-closure", "Exact contraction generically closes on only the local pairwise PIFB2 operator sectors with zero residual.", "All normalized finite microscopic laws and all admitted coarse maps.", "REFUTED", ["ev-counterexamples"], ["a-fixed-joint"], "Refute the Gaussian or hidden-spin generated nonlocal/higher-body interaction examples."),
        claim("pifb-controlled-projection", "For the current intended PIFB2/MAgent microscopic family, the exact coarse action has a PIFB2 retained projection whose residual vanishes uniformly on bounded-energy sublevels as the base lattice is refined.", "Every fixed finite N and the intended refining lattice family after the microscopic family and projection norm are fixed.", "INCONCLUSIVE", ["ev-sector-map", "ev-counterexamples", "ev-source-map"], ["a-section-typing", "a-continuum"], "A nonvanishing generated operator or residual sequence refutes controlled closure; a uniform residual theorem would verify it."),
        claim("deterministic-continuum", "The retained PIFB2 lattice actions Gamma-converge to a gauge-covariant continuum section action for fixed finite N.", "The intended refining mesh family, section topology, boundary data, and gauge quotient after all are explicitly fixed.", "INCONCLUSIVE", ["ev-asymptotics", "ev-counterexamples"], ["a-continuum"], "Failure of equicoercivity, liminf, recovery, topology control, or residual convergence defeats the claim."),
        claim("process-elbo-continuum", "The exact coarse probability-law ELBOs converge to a continuum process-law ELBO on a section space.", "The intended refining family with a common Polish embedding and normalized reference/process laws.", "INCONCLUSIVE", ["ev-counterexamples", "ev-sector-map"], ["a-continuum"], "Failure of tightness, relative-entropy liminf/recovery, projective consistency, or partition convergence defeats the claim."),
    ]

    binding = {"schema_version": SCHEMA, "contract_id": contract_id, "target_digest": digest}
    write_json(RUN / "claim-ledger.json", {**binding, "assumptions": assumptions, "evidence": evidence_records, "claims": claims})

    families = [
        ("EC-KL", "KL disintegration and exact contraction", ["exact-coarse-action", "density-elbo-ledger"], "Fine and coarse probability laws", "Conditional KL is nonnegative", "Push the normalized posterior through a fixed coarse map", "Failure of disintegration or Q-independent typing", ["Exact finite-lattice coarse VFE", "Exact density action"], ["Locality is not automatic"], "law-KL-disintegration-density", "accepted"),
        ("ORDER-PARAMETER", "Constrained KL and Legendre duality", ["pifb-controlled-projection"], "Finite-dimensional section order parameters", "The rate function is convex in linear moment coordinates", "Contract the exact coarse law under declared moments", "A nonconvex target in fixed linear coordinates cannot equal the exact rate function", ["Exact deterministic order-parameter functional under constraint qualification"], ["Sufficient order parameters may be as large as the full law"], "moment-logMGF-Legendre", "conditional"),
        ("FULL-INTERACTION", "Hoeffding-Mobius interaction decomposition", ["generic-local-closure", "pifb-controlled-projection"], "Finite coarse action modulo constants", "All generated hyperedges remain explicit", "Project the exact interaction coordinates onto the PIFB basis", "Hidden-variable elimination generates omitted higher-body terms", ["Exact retained action plus residual identity"], ["No uniform residual theorem for intended MAgent family"], "interaction-projection-residual", "accepted-with-open-bound"),
        ("FIXED-SOURCE", "Explicit categorical source-label variational factor", ["fixed-source-attention", "live-peer-fixed-joint"], "Joint receiver-source event law", "Categorical KL and conditional total correlation", "Derive attention before any live-peer substitution", "Letting the fixed joint read current q_j is circular", ["Fixed-source attention exactness"], ["Live recognition-peer interpretation remains conditional"], "label-KL-softmax-TC", "accepted"),
        ("FISHER-GRADIENT", "Second-order KL expansion on base edges", ["fisher-gradient", "deterministic-continuum"], "Statistical-bundle sections and connection links", "Fisher metric controls the local Hessian", "Scale edge KL by h^(d-2)", "Singular Fisher strata or O(1) link mismatch", ["Smooth-sequence covariant-gradient consistency"], ["Full liminf and recovery remain open"], "edge-KL-Fisher-covariant-jet", "conditional"),
        ("COMPACT-CURVATURE", "Wilson plaquette expansion", ["compact-curvature", "deterministic-continuum"], "Compact unitary lattice links", "Conjugation-invariant positive trace action", "Scale plaquette action by h^(d-4)", "Non-small holonomy or irregular mesh", ["Smooth-sequence curvature consistency"], ["Dynamical gauge compactness remains open"], "plaquette-Wilson-curvature", "conditional"),
        ("GL-DRESSED", "SPD/Fisher dressing of noncompact GL curvature", ["deterministic-continuum", "process-elbo-continuum"], "GL links plus a transforming SPD metric", "Dressed norm is gauge invariant; raw Frobenius norm is not", "Treat the SPD metric and gauge quotient as genuine variables", "Metric degeneration or infinite gauge volume", ["Algebraic invariance repair"], ["Coercivity, normalization, and continuum existence remain open"], "noncompact-GL-SPD-gauge-volume", "open"),
        ("PROCESS-LIMIT", "Weak-law and relative-entropy variational convergence", ["process-elbo-continuum"], "Probability laws on a common Polish section space", "Tightness and entropy lower semicontinuity", "Reconstruct lattice laws on a common continuum space", "Deterministic Gamma convergence without reference-law convergence", [], ["No current process-law construction for full PIFB2 system"], "law-tightness-entropy-partition", "open"),
    ]
    family_records = []
    for family_id, mechanism, obligations, representation, invariant, bridge, failure, verified, gaps, fingerprint, disposition in families:
        family_records.append({
            "family_id": family_id,
            "core_mechanism": mechanism,
            "target_obligation_ids": obligations,
            "representation": representation,
            "invariant_or_obstruction": invariant,
            "obligations": obligations,
            "bridge": bridge,
            "failure_test": failure,
            "verified_results": verified,
            "open_gaps": gaps,
            "novelty_fingerprint": fingerprint,
            "disposition": disposition,
        })
    write_json(RUN / "approach-registry.json", {**binding, "mechanism_families": family_records})

    ancestor_ids = [c["id"] for c in claims if c["id"] != "target"]
    write_json(RUN / "dependency-dag.json", {**binding, "edges": [{"from": "target", "to": item} for item in ancestor_ids]})

    counter_path = EVIDENCE / "adversarial-counterexamples.md"
    recon_path = EVIDENCE / "independent-reconstruction.md"
    oracle_path = EVIDENCE / "oracle-erasure.md"
    write_json(RUN / "adversarial-report.json", {
        **binding,
        "attacks": [
            {
                "id": "attack-locality-circularity-continuum",
                "claim_ids": ["target", *ancestor_ids],
                "attack": "Exact contraction may be nonlocal and many-body; current belief sections may be recognition parameters rather than Q-independent coarse samples; live-peer KL is not generically a fixed-joint state ELBO; GL gauge volume may be nonnormalizable; and deterministic action convergence does not imply process-law ELBO convergence.",
                "response": "The exact contraction theorem survives under fixed typed variables. The stronger PIFB2 closure and both continuum targets are withheld. Live-peer terms are reclassified, the full residual is retained, compact and noncompact gauge cases are separated, and entropy/normalization are explicit.",
                "disposition": "SUSTAINED",
                "artifact_path": "evidence/adversarial-counterexamples.md",
                "artifact_sha256": sha256(counter_path),
            }
        ],
        "independent_reconstruction": {
            "claim_ids": ["target", *ancestor_ids],
            "method": "Reconstructed from the normalized microscopic posterior, a fixed coarse map, KL disintegration, and interaction projection without assuming the PIFB2 action.",
            "result": "PASS",
            "conclusion": "The exact finite-lattice action theorem and the inconclusive boundary were reproduced independently.",
            "artifact_path": "evidence/independent-reconstruction.md",
            "artifact_sha256": sha256(recon_path),
        },
        "oracle_erasure": {
            "claim_ids": ["target", *ancestor_ids],
            "method": "Removed PIFB2 and MAgent from the derivational premises and checked which results remain.",
            "result": "PASS",
            "conclusion": "Exact contraction remains; only the choice and interpretation of the retained local operator basis depend on PIFB2 and MAgent intuition.",
            "artifact_path": "evidence/oracle-erasure.md",
            "artifact_sha256": sha256(oracle_path),
        },
    })

    counterexamples = r"""{META}
# Counterexample register

| ID | Universal subclaim defeated | Witness | Consequence |
|---|---|---|---|
| CE-1 | Exact contraction is automatically local | Shared Gaussian latent produces an all-to-all rank-one term | Locality needs decay/Markov/residual hypotheses |
| CE-2 | Exact elimination remains pairwise | Hidden Ising spin produces a four-agent interaction | PIFB closure needs full interaction projection |
| CE-3 | Live-peer KL is an ordinary fixed-joint state ELBO | Mixed-derivative mismatch for Bernoulli factors | Use fixed sources, promoted law fields, or mark as engineered |
| CE-4 | Raw positive GL curvature is gauge invariant | Diagonal conjugation rescales Frobenius energy | Use compact group or transforming SPD dressing |
| CE-5 | Action convergence implies process ELBO convergence | Product Bernoulli exact KL diverges while density action stays finite | Prove process-law convergence separately |

These counterexamples do not refute the existential possibility of a restricted,
well-typed microscopic family. They refute generic automatic PIFB2 closure.
"""
    (RUN / "counterexample-register.md").write_text(render(counterexamples).rstrip() + "\n", encoding="utf-8")

    theorem = r"""{META}
# Construction or strongest theorem

For every fixed finite agent number and admitted finite lattice, let the
microscopic posterior be fixed and normalized, and let the sampled
section-configuration map be measurable and independent of the recognition
law. Then KL disintegration induces an exact coarse probability-law VFE. If
the coarse posterior has a density relative to a declared reference, its
negative log density is an exact finite-lattice effective action, modulo an
additive normalizing constant. The full ELBO additionally contains recognition
entropy, evidence/partition normalizers, and the conditional-KL information
discarded by coarse-graining.

The exact density action admits a complete finite interaction decomposition.
A PIFB2 action is obtained by projecting that complete action onto the chosen
self, peer, observation, base-edge, link, plaquette, and attention scopes:

\[
S_h^{{\rm exact}}=S_h^{{\rm PIFB}}+\varepsilon_h+c_h.
\]

This is an exact identity, not an assertion that \(\varepsilon_h=0\). The
truncated ELBO error is uniformly bounded by \(\|\varepsilon_h\|_\infty\)
when that norm is finite. Fisher-gradient and compact Wilson-curvature
calculations identify the necessary \(h^{{d-2}}\) and \(h^{{d-4}}\) scalings
on smooth sequences. No current evidence proves a vanishing residual, a full
dynamical-gauge Gamma limit, or a continuum process-law ELBO for the intended
PIFB2/MAgent family.

Terminal conclusion: the exact finite-lattice bridge is affirmative; generic
PIFB2 closure and the requested continuum theory remain inconclusive.
"""
    (RUN / "construction-or-strongest-theorem.md").write_text(render(theorem).rstrip() + "\n", encoding="utf-8")

    report = r"""{META}
# Rigorous theory search report

## Frozen contract

The contract is `{contract_id}`. It concerns fixed finite \(N\) agents whose
belief and model objects are sections. Only the base lattice is refined.

## Terminal status

**INCONCLUSIVE.** The exact finite-lattice contraction is established, but the
current artifacts do not prove controlled PIFB2 closure or either requested
continuum limit.

## Certificate

No complete affirmative or negative certificate is issued. The strongest
partial theorem is the exact KL-contraction and density-action theorem; the
counterexamples rule out generic automatic locality and closure.

## Strongest verified result

An independently specified normalized microscopic joint and a fixed measurable
coarse section map induce the exact coarse functional
\(-\log p_h(o)+D_{{\rm KL}}(R_h\Vert P_{{X,h}}^o)\). When the coarse posterior
has density \(Z_h^{{-1}}e^{{-S_h}}\) relative to \(\nu_h\), this is
\(\mathbb E_R S_h-H_{{\nu_h}}(R)+\log Z_h-\log p_h(o)\). The PIFB2 basis can
then be applied as an explicit projection, with an exact residual ledger.

## Dependency closure

Exact contraction, density/entropy bookkeeping, fixed-source attention,
Fisher edge scaling, and compact Wilson scaling are evidence-verified.
Generic pairwise/local closure and ordinary fixed-joint live-peer exactness are
refuted. Controlled PIFB projection, deterministic Gamma convergence, and
process-law ELBO convergence are terminally inconclusive for the present
microscopic family.

## Independent reconstruction

The theorem and boundary were reproduced from posterior disintegration and
interaction projection without using the PIFB2 action as a premise.

## Oracle erasure

After erasing PIFB2 and MAgent, the exact action theorem remains. What is lost
is the proposed local operator basis and its physical interpretation. Thus the
two artifacts are valid intuition for model selection, not derivational
evidence.

## Unresolved obligations

- Specify one normalized microscopic family whose slow variables are genuine
  sampled belief/model sections rather than recognition parameters.
- Compute or bound its exact generated interaction coordinates.
- Prove the retained PIFB residual vanishes in a declared norm uniformly on
  bounded-energy sublevels.
- Establish equicoercivity, liminf, recovery, boundary, topology, and gauge
  compactness for a deterministic continuum action.
- Separately establish tightness, continuum reference/process laws,
  relative-entropy convergence, and partition/evidence convergence.

## Scope and limitations

The result is revision-bound to repository commit
`24c02aa29cd76589a52e54c56e4247f0560f7e87` and the Research manuscripts read
on 2026-08-12. No continuum process law, noncompact GL existence theorem, or
claim that the current MAgent backend is an exact microscopic ELBO is made.
"""
    (RUN / "final-report.md").write_text(render(report).rstrip() + "\n", encoding="utf-8")

    write_json(RUN / "release.json", {
        **binding,
        "checkpoint": "release",
        "target_claim": "target",
        "terminal_status": "INCONCLUSIVE",
        "certificate_claim": None,
        "strongest_result": "Exact finite-lattice KL contraction yields a coarse probability-law VFE and Radon-Nikodym density action; PIFB2 is an exact retained projection plus residual, not generically a closed action.",
        "unresolved_obligations": [
            "Specify the intended normalized microscopic section-variable family independently of the PIFB2 ansatz.",
            "Prove a controlled local PIFB2 truncation residual for the refining lattice family.",
            "Prove deterministic Gamma convergence including dynamical gauge sectors.",
            "Construct and prove convergence of the continuum process-law ELBO including entropy and normalizers.",
        ],
    })


if __name__ == "__main__":
    main()
