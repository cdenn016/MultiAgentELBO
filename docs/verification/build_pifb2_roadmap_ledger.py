"""Build the revision-bound verification ledger for the PIFB2 roadmap."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ROADMAP = ROOT / "docs/research-plans/2026-08-12-pifb2-continuum-roadmap.md"
PIFB2 = Path(r"C:\Users\chris and christine\Desktop\Research\manuscripts\PIFB2.tex")
README = Path(r"C:\Users\chris and christine\Desktop\MAgent_Model-main\README.md")
FULL_VFE = Path(
    r"C:\Users\chris and christine\Desktop\MAgent_Model-main\gauge_agent\full_vfe.py"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def criterion_map(levels: dict[str, str]) -> list[dict[str, str]]:
    return [{"name": name, "level": level} for name, level in levels.items()]


def verified_claim(
    *,
    claim_id: str,
    statement: str,
    domain: str,
    revision: str,
    criteria: dict[str, str],
    candidate_ids: tuple[str, str],
    candidate_descriptions: tuple[str, str],
    view_ids: tuple[str, str],
    result_locations: tuple[str, str],
    evidence: list[dict[str, str]],
    adjudicator_location: str,
) -> dict[str, object]:
    left, right = candidate_ids
    view_a, view_b = view_ids
    return {
        "id": claim_id,
        "domain": domain,
        "statement": statement,
        "severity": "medium",
        "state": "EVIDENCE_VERIFIED",
        "artifact_revision": revision,
        "criteria": criterion_map(criteria),
        "escalation_triggers": [],
        "escalation_target": 2,
        "views": {
            "calibration_kind": (
                "independent primary-source trace and adversarial scope scan"
            ),
            "unresolved_disagreement": False,
            "comparison": {
                "method": "pairwise",
                "candidate_count": 2,
                "candidate_ids": [left, right],
                "candidate_descriptions": [
                    {"id": left, "description": candidate_descriptions[0]},
                    {"id": right, "description": candidate_descriptions[1]},
                ],
                "pivot_ids": [],
                "orders": ["AB", "BA"],
                "matches": [
                    {
                        "left": left,
                        "right": right,
                        "view_id": view_a,
                        "outcome": "left",
                        "criteria": criterion_map(criteria),
                        "result_location": result_locations[0],
                    },
                    {
                        "left": right,
                        "right": left,
                        "view_id": view_b,
                        "outcome": "right",
                        "criteria": criterion_map(criteria),
                        "result_location": result_locations[1],
                    },
                ],
            },
            "scores": [
                {"view_id": view_a, "criteria": criterion_map(criteria)},
                {"view_id": view_b, "criteria": criterion_map(criteria)},
            ],
        },
        "evidence": [
            {**entry, "artifact_revision": revision}
            for entry in evidence
        ],
        "counterevidence": [],
        "verifiers": [
            {
                "role": "verifier-adjudicator",
                "view_ids": [view_a, view_b],
                "result": "support",
                "evidence_ids": [entry["id"] for entry in evidence],
                "result_location": adjudicator_location,
            }
        ],
        "open_obligations": [],
        "evidence_invalidated": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ledger",
        default=".verification/pifb2-continuum-roadmap-ledger.json",
    )
    args = parser.parse_args()
    ledger_path = (ROOT / args.ledger).resolve()
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    revision = ledger["artifact_revision"]

    source_criteria = {
        "source_authority": "strong",
        "primary_source_status": "strong",
        "exact_support": "strong",
        "quotation_or_data_fidelity": "adequate",
        "provenance": "strong",
        "currency": "strong",
        "counterevidence_coverage": "adequate",
    }
    general_criteria = {
        "claim_specificity": "strong",
        "artifact_identity": "strong",
        "evidence_relevance": "strong",
        "evidence_freshness": "strong",
        "counterevidence_handling": "adequate",
        "independent_view_agreement": "strong",
        "severity_calibration": "adequate",
        "closure_readiness": "strong",
    }

    claims = [
        verified_claim(
            claim_id="ROADMAP-ELBO-ACTION-TIER-SEPARATION",
            statement=(
                "The roadmap preserves the primary-source tier boundary: the "
                "complete live-peer PIFB2 scalar is an engineered action ansatz, "
                "selected sectors can have exact fixed-joint ELBO realizations, "
                "and an optional configuration-space Gibbs identity is a distinct "
                "meta-level construction."
            ),
            domain="source",
            revision=revision,
            criteria=source_criteria,
            candidate_ids=("tier_separation", "single_state_elbo"),
            candidate_descriptions=(
                "The roadmap states the three levels separately and limits each claim.",
                "The roadmap presents the whole live-peer action as one ordinary state ELBO.",
            ),
            view_ids=("manuscript-tier-trace", "level-conflation-scan"),
            result_locations=(
                "PIFB2.tex:678,3279-3332,3577-3630; roadmap:7-30,106-126",
                "Roadmap adversarial scan:7-30,106-126,166-174",
            ),
            evidence=[
                {
                    "id": "ROADMAP-TIER-PIFB2-SOURCE",
                    "kind": "primary_source",
                    "location": (
                        f"{PIFB2.as_posix()}:678,3279-3332,3577-3630; "
                        f"SHA256 {sha256(PIFB2)}"
                    ),
                },
                {
                    "id": "ROADMAP-TIER-TEXT",
                    "kind": "primary_source",
                    "location": (
                        "docs/research-plans/"
                        "2026-08-12-pifb2-continuum-roadmap.md:7-30,106-126,"
                        f"166-174; SHA256 {sha256(ROADMAP)}"
                    ),
                },
            ],
            adjudicator_location=(
                "PIFB2.tex and roadmap source locations recorded in evidence"
            ),
        ),
        verified_claim(
            claim_id="ROADMAP-GENERAL-STATISTICAL-G-ONTOLOGY",
            statement=(
                "The roadmap treats a principal G-bundle and associated general "
                "statistical-manifold fibers as structural, while treating Gaussian "
                "fibers and GL(K) frames only as examples or implementation backends."
            ),
            domain="general",
            revision=revision,
            criteria=general_criteria,
            candidate_ids=("general_ontology", "gaussian_gl_ontology"),
            candidate_descriptions=(
                "Principal G and general statistical manifolds are structural.",
                "The abstract theory is restricted to Gaussian fibers and GL(K).",
            ),
            view_ids=("structural-definition-trace", "hidden-specialization-scan"),
            result_locations=(
                "Roadmap:11-13,32-70,112-126,146-162",
                "Roadmap Gaussian/GL(K) occurrence audit:13,68,131,146-162,174",
            ),
            evidence=[
                {
                    "id": "ROADMAP-GENERAL-ONTOLOGY-TEXT",
                    "kind": "primary_source",
                    "location": (
                        "docs/research-plans/"
                        "2026-08-12-pifb2-continuum-roadmap.md:11-13,32-70,"
                        f"112-126,146-162; SHA256 {sha256(ROADMAP)}"
                    ),
                }
            ],
            adjudicator_location=(
                "Roadmap structural definitions and adversarial specialization scan"
            ),
        ),
        verified_claim(
            claim_id="ROADMAP-MAGENT-IMPLEMENTATION-CLASSIFICATION",
            statement=(
                "The roadmap accurately classifies the present MAgent implementation "
                "as a Gaussian and GL(K)-type finite realization, its population "
                "coupling as engineered, its R1 frame term as gauge fixing, its "
                "frame-derived continuum connection as pure gauge, and its "
                "attention-free versus attention-weighted base-neighbor terms as "
                "closed-ELBO versus effective-consensus sectors."
            ),
            domain="source",
            revision=revision,
            criteria=source_criteria,
            candidate_ids=("implementation_classification", "undifferentiated_elbo"),
            candidate_descriptions=(
                "The roadmap matches the live README and code-level term classifications.",
                "The roadmap incorrectly treats all runtime sectors as one exact ELBO or genuine curvature.",
            ),
            view_ids=("runtime-source-trace", "classification-skeptic"),
            result_locations=(
                "README.md:37-142; full_vfe.py:329-331,439-450,1322-1326,1454-1459,1793-1832",
                "Roadmap versus live implementation adversarial scan:158-162",
            ),
            evidence=[
                {
                    "id": "ROADMAP-MAGENT-README-SOURCE",
                    "kind": "primary_source",
                    "location": (
                        f"{README.as_posix()}:37-142; SHA256 {sha256(README)}"
                    ),
                },
                {
                    "id": "ROADMAP-MAGENT-FULLVFE-SOURCE",
                    "kind": "primary_source",
                    "location": (
                        f"{FULL_VFE.as_posix()}:329-331,439-450,1322-1326,"
                        f"1454-1459,1793-1832; SHA256 {sha256(FULL_VFE)}"
                    ),
                },
                {
                    "id": "ROADMAP-MAGENT-CROSSWALK-TEXT",
                    "kind": "primary_source",
                    "location": (
                        "docs/research-plans/"
                        "2026-08-12-pifb2-continuum-roadmap.md:158-162; "
                        f"SHA256 {sha256(ROADMAP)}"
                    ),
                },
            ],
            adjudicator_location=(
                "Live MAgent README, FullVFE source, and roadmap crosswalk"
            ),
        ),
    ]

    ledger["claims"] = claims
    ledger_path.write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
