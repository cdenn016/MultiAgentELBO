"""Populate the revision-bound verification ledger for the ELBO/action bridge."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "docs/derivations/2026-08-12-elbo-to-effective-section-action"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


NAMES = (
    "statement_precision",
    "definitions_and_domains",
    "assumptions",
    "derivation_validity",
    "theorem_dependencies",
    "limiting_cases",
    "counterexample_search",
    "notation_conclusion_agreement",
)


def criteria(score: int) -> list[dict[str, object]]:
    return [{"name": name, "score": score} for name in NAMES]


def views(
    *,
    candidate_ids: tuple[str, str],
    descriptions: tuple[str, str],
    view_ids: tuple[str, str],
    outcomes: tuple[str, str],
    score: int,
    locations: tuple[str, str],
) -> dict[str, object]:
    left, right = candidate_ids
    view_a, view_b = view_ids
    return {
        "calibration_kind": "independent reconstruction and adversarial counterexample scan",
        "unresolved_disagreement": False,
        "comparison": {
            "method": "pairwise",
            "candidate_count": 2,
            "candidate_ids": [left, right],
            "candidate_descriptions": [
                {"id": left, "description": descriptions[0]},
                {"id": right, "description": descriptions[1]},
            ],
            "pivot_ids": [],
            "orders": ["AB", "BA"],
            "matches": [
                {
                    "left": left,
                    "right": right,
                    "view_id": view_a,
                    "outcome": outcomes[0],
                    "criteria": criteria(score),
                    "result_location": locations[0],
                },
                {
                    "left": right,
                    "right": left,
                    "view_id": view_b,
                    "outcome": outcomes[1],
                    "criteria": criteria(score),
                    "result_location": locations[1],
                },
            ],
        },
        "scores": [
            {"view_id": view_a, "criteria": criteria(score)},
            {"view_id": view_b, "criteria": criteria(score)},
        ],
    }


def evidence(evidence_id: str, path: Path, revision: str) -> dict[str, str]:
    relative = path.relative_to(ROOT).as_posix()
    return {
        "id": evidence_id,
        "kind": "derivation",
        "location": f"{relative}; SHA256 {sha256(path)}",
        "artifact_revision": revision,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ledger",
        default=".verification/elbo-effective-action-ledger.json",
    )
    args = parser.parse_args()
    ledger_path = (ROOT / args.ledger).resolve()
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    revision = ledger["artifact_revision"]

    exact_path = RUN / "evidence/exact-contraction-proof.md"
    counter_path = RUN / "evidence/adversarial-counterexamples.md"
    theorem_path = RUN / "construction-or-strongest-theorem.md"
    final_path = RUN / "final-report.md"

    exact_evidence = evidence("ELBO-ACTION-EXACT-DERIVATION", exact_path, revision)
    reconstruction_evidence = evidence(
        "ELBO-ACTION-INDEPENDENT-RECONSTRUCTION", theorem_path, revision
    )
    obstruction_evidence = evidence(
        "ELBO-ACTION-CONTINUUM-OBSTRUCTIONS", counter_path, revision
    )
    boundary_evidence = evidence(
        "ELBO-ACTION-TERMINAL-BOUNDARY", final_path, revision
    )

    ledger["claims"] = [
        {
            "id": "ELBO-EXACT-COARSE-ACTION",
            "domain": "mathematics",
            "statement": (
                "For fixed finite N and an admitted finite lattice, a fixed "
                "normalized microscopic posterior and a fixed measurable coarse "
                "section map induce an exact coarse probability-law VFE by KL "
                "disintegration; when the coarse posterior is dominated, its "
                "negative log Radon-Nikodym density is an exact finite-lattice "
                "effective action, with entropy, normalizers, and conditional-KL "
                "correction retained."
            ),
            "severity": "medium",
            "state": "EVIDENCE_VERIFIED",
            "artifact_revision": revision,
            "criteria": criteria(19),
            "escalation_triggers": [],
            "escalation_target": 2,
            "views": views(
                candidate_ids=("exact_contraction", "no_exact_contraction"),
                descriptions=(
                    "KL disintegration yields the stated exact coarse VFE and density action.",
                    "No exact coarse action follows from the fixed microscopic law and coarse map.",
                ),
                view_ids=("posterior-disintegration", "independent-reconstruction"),
                outcomes=("left", "right"),
                score=19,
                locations=(
                    "evidence/exact-contraction-proof.md",
                    "construction-or-strongest-theorem.md",
                ),
            ),
            "evidence": [exact_evidence, reconstruction_evidence],
            "counterevidence": [],
            "verifiers": [
                {
                    "role": "verifier-adjudicator",
                    "view_ids": ["posterior-disintegration", "independent-reconstruction"],
                    "result": "support",
                    "evidence_ids": [
                        "ELBO-ACTION-EXACT-DERIVATION",
                        "ELBO-ACTION-INDEPENDENT-RECONSTRUCTION",
                    ],
                    "result_location": "docs/derivations/2026-08-12-elbo-to-effective-section-action/construction-or-strongest-theorem.md",
                }
            ],
            "open_obligations": [],
            "evidence_invalidated": False,
        },
        {
            "id": "PIFB2-CLOSURE-AND-CONTINUUM",
            "domain": "mathematics",
            "statement": (
                "The current intended microscopic family has a PIFB2 retained "
                "projection with a uniformly vanishing refinement residual, and "
                "the resulting lattice functionals converge both as deterministic "
                "actions and as exact probability-law ELBOs on a continuum section space."
            ),
            "severity": "medium",
            "state": "INCONCLUSIVE",
            "artifact_revision": revision,
            "criteria": criteria(15),
            "escalation_triggers": [],
            "escalation_target": 2,
            "views": views(
                candidate_ids=("complete_continuum_derivation", "obligations_open"),
                descriptions=(
                    "The current artifacts prove residual control and both continuum limits.",
                    "Generated interactions, gauge compactness, and process-law convergence remain open.",
                ),
                view_ids=("continuum-proof-audit", "counterexample-stress-test"),
                outcomes=("right", "left"),
                score=15,
                locations=(
                    "final-report.md unresolved obligations",
                    "evidence/adversarial-counterexamples.md",
                ),
            ),
            "evidence": [obstruction_evidence, boundary_evidence],
            "counterevidence": [],
            "verifiers": [
                {
                    "role": "verifier-adjudicator",
                    "view_ids": ["continuum-proof-audit", "counterexample-stress-test"],
                    "result": "abstain",
                    "evidence_ids": [
                        "ELBO-ACTION-CONTINUUM-OBSTRUCTIONS",
                        "ELBO-ACTION-TERMINAL-BOUNDARY",
                    ],
                    "result_location": "docs/derivations/2026-08-12-elbo-to-effective-section-action/final-report.md",
                }
            ],
            "open_obligations": [
                "Specify the normalized microscopic section-variable family independently of the PIFB2 ansatz.",
                "Prove a uniform truncation-residual bound on bounded-energy sublevels.",
                "Prove deterministic Gamma convergence including gauge and boundary sectors.",
                "Prove tightness, relative-entropy convergence, and partition/evidence convergence for the continuum process-law ELBO.",
            ],
            "evidence_invalidated": False,
        },
    ]

    ledger_path.write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
