"""Build the bounded rigorous-theory-search package for ELBO-derived actions."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "docs/derivations/2026-08-12-elbo-to-effective-section-action"
SCHEMA = "rigorous-theory-search/v1"


TARGET = {
    "statement": (
        "For an arbitrary fixed finite number N of section-valued agents over either "
        "a finite oriented lattice or a compact contextual base with a refining lattice "
        "family, determine sufficient hypotheses under which an independently specified "
        "normalized microscopic joint law and its exact ELBO induce, by exact contraction "
        "to declared coarse section variables followed by a controlled local truncation, "
        "a PIFB2-type effective action; classify every self, peer, observation, base-gradient, "
        "connection, curvature, entropy, normalization, and correction sector as exact, "
        "conditional, truncated, or open, and determine what is required for a continuum limit."
    ),
    "kind": "MATHEMATICAL",
    "quantifier_class": "MIXED",
    "quantifiers": (
        "For every fixed finite N >= 1 and every admitted finite lattice, seek an existential "
        "construction under explicit hypotheses; for a continuum base, require a declared "
        "refining lattice family and state separately whether deterministic action convergence "
        "and process-law ELBO convergence hold."
    ),
    "domains": [
        "A fixed finite agent set I={1,...,N}.",
        "Either a finite oriented cell complex Lambda_h or a compact d-dimensional Riemannian contextual base C with a refining family Lambda_h.",
        "Standard Borel microscopic state spaces Z_h and coarse configuration spaces X_h of sampled belief, model, support, frame, and link fields.",
        "Normalized microscopic joint laws P_h(do,dz) independent of the variational law and admissible recognition laws Q_h(dz|o).",
    ],
    "codomains": [
        "Extended-real exact ELBO/VFE functionals on probability laws.",
        "Exact contracted coarse functionals on probability laws over X_h.",
        "Local PIFB2-type action ansatz spaces modulo additive constants and gauge equivalence.",
    ],
    "regularity": (
        "Finite-lattice objects are measurable and normalized with finite displayed expectations; "
        "continuum candidates use declared Sobolev or smooth section classes, uniformly regular meshes, "
        "and the differentiability and domination needed for Fisher-KL expansions."
    ),
    "measures": [
        "Declared sigma-finite microscopic and coarse reference measures at every finite lattice.",
        "A finite positive Radon base measure dmu and a base cometric for continuum contractions.",
        "Normalized Haar measure for compact gauge groups, or an explicit noncompact replacement and gauge treatment.",
    ],
    "boundary_conditions": [
        "Periodic boundaries, or explicitly declared Dirichlet or Neumann data with all boundary action terms retained."
    ],
    "symmetries": [
        "Passive gauge covariance of section and link variables with gauge-invariant scalar objectives.",
        "Relabeling covariance of the finite agent index set when the interaction graph and data are relabeled together.",
    ],
    "equivalence": (
        "Effective actions are compared modulo declared additive normalizing constants and passive gauge equivalence; "
        "projection to a finite ansatz is not equality unless the truncation residual vanishes."
    ),
    "premises": [
        "The microscopic joint law is fixed independently of Q_h and has positive finite evidence for the admitted observation.",
        "Every exact contraction uses a declared measurable coarse map or kernel and the disintegrations required by the KL contraction identity.",
        "A PIFB2-type action means a typed finite-N section action, not a population N-to-infinity limit."
    ],
    "modeling_postulates": [
        "The declared coarse variables are the operational belief, model, support, frame, and relational-link fields of the agents."
    ],
    "search_priors": ["SEARCH_PRIOR_AFFIRMATIVE"],
    "permitted_theorems": [
        "KL chain rule and data-processing/contraction identities under standard-Borel disintegration hypotheses.",
        "Gibbs variational principle with explicit reference measure and finite partition function.",
        "Second-order KL expansion by the Fisher metric for regular dominated statistical families.",
        "Riemann-sum and finite-element consistency theorems after hypothesis-by-hypothesis mapping.",
        "Gamma- or Mosco-convergence theorems only after equicoercivity and recovery/liminf hypotheses are proved."
    ],
    "negative_certificate_kind": "COUNTEREXAMPLE",
    "falsification_criterion": (
        "A counterexample to a universal subclaim, a failure of normalization or absolute continuity, "
        "dependence of the purported fixed joint on Q_h, a nonvanishing untracked truncation residual, "
        "or a mesh family for which the claimed continuum convergence fails."
    ),
    "literature_policy": (
        "Use the live Theory, current Research manuscripts and verified ledger, the Research wiki, "
        "and primary mathematical sources where an external theorem is invoked; no priority claim is attempted."
    ),
}


def canonical_digest(value: object) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def metadata(contract_id: str, digest: str) -> str:
    value = {
        "contract_id": contract_id,
        "schema_version": SCHEMA,
        "target_digest": digest,
    }
    return "<!-- rigorous-theory-search-metadata " + json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ) + " -->"


def freeze_contract() -> None:
    digest = canonical_digest(TARGET)
    contract_id = f"contract-sha256-{digest}"
    write_json(
        RUN / "problem-contract.json",
        {
            "schema_version": SCHEMA,
            "contract_id": contract_id,
            "target_digest": digest,
            "target": TARGET,
        },
    )
    for name in (
        "approach-registry.json",
        "claim-ledger.json",
        "dependency-dag.json",
        "adversarial-report.json",
        "release.json",
    ):
        path = RUN / name
        value = json.loads(path.read_text(encoding="utf-8"))
        value["schema_version"] = SCHEMA
        value["contract_id"] = contract_id
        value["target_digest"] = digest
        if name == "claim-ledger.json":
            target_claim = value["claims"][0]
            target_claim["statement"] = TARGET["statement"]
            target_claim["quantifiers"] = TARGET["quantifiers"]
            target_claim["kind"] = TARGET["kind"]
            target_claim["target_digest"] = digest
        write_json(path, value)
    header = metadata(contract_id, digest)
    for name in (
        "construction-or-strongest-theorem.md",
        "counterexample-register.md",
        "final-report.md",
    ):
        path = RUN / name
        lines = path.read_text(encoding="utf-8").splitlines()
        lines[0] = header
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    freeze_contract()
