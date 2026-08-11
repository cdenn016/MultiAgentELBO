"""Contract for the current Gaussian fixed-ray result record.

The historical pilot narrative remains intentionally present in the results
document.  Assertions about the completed confirmatory run therefore inspect
only the explicitly delimited current-state section.
"""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIRECTORY = (
    REPOSITORY_ROOT
    / "docs"
    / "verification"
    / "evidence"
    / "2026-08-10-gaussian-confirmatory-fcb2c49"
)
RESULT_DOCUMENT = REPOSITORY_ROOT / "docs" / "results" / "2026-08-09-gaussian-fixed-ray-results.md"
BINDING_LINK = (
    "[source binding](../verification/evidence/"
    "2026-08-10-gaussian-confirmatory-fcb2c49/source_binding.json)"
)
SCIENTIFIC_REVISION = "fcb2c49efdca2ad3ee502dc08fbb82fc285e7a05"
COORDINATOR_EVIDENCE_SHA256 = (
    "7fb07f04d709a3d07613fa220529875c7ddd63601940f3bbb2b87d2440b055fa"
)
ORIGINAL_INVENTORY = {
    "config.json": {
        "sha256": "66e474db7e46ae0589ca5198712c59aa9f28317d219381ddf96b989e5d40d191",
        "size_bytes": 792,
    },
    "confirmatory_arrays.npz": {
        "sha256": "7040967043619fd52a0386ff0b9623febdd4c97f0c2356f8abb98fd786dc2b6a",
        "size_bytes": 71942,
    },
    "confirmatory_endpoints.json": {
        "sha256": "7d6b36b5bde80969d8974d5550c0ed8c125896ee03be7ffd196d3915f8261556",
        "size_bytes": 214173,
    },
    "confirmatory_execution.json": {
        "sha256": "04661576c3a4132fca52739a95038a221976abdd2fcd02ea5bbe0d9d3a8fe518",
        "size_bytes": 9334757,
    },
    "confirmatory_job_table.json": {
        "sha256": "a50dd3893ce1ad9c081a8e2f2cbc5adc676e2b217c9c3ec321e8b0d62b453adf",
        "size_bytes": 9062,
    },
    "holdout_analysis.json": {
        "sha256": "ff09a656d7638a233d21149132367b95072fae6030187ee997290aa1a0596d1d",
        "size_bytes": 8152,
    },
    "manifest.json": {
        "sha256": "7e0a050850b48b446c70bff3a67010c84d2daa1fada6c48742d3ab152d43a1fb",
        "size_bytes": 2522,
    },
    "metrics.json": {
        "sha256": "cd45e55dd39236b556dc200a04ad081affcb19a6c52fb584ad63f3f1992f7f59",
        "size_bytes": 394,
    },
    "primary_analysis.json": {
        "sha256": "f8b58ae7f8777e18800c37d63b55d37c0052cd47b407a40497405ef5f6375155",
        "size_bytes": 17093,
    },
    "primary_execution.json": {
        "sha256": "e1a952259227f754bafacf3e0a983cea28996325adee96d1579ae1944024f816",
        "size_bytes": 7170105,
    },
}
TRACKED_SCIENTIFIC_SUBSET = [
    "config.json",
    "confirmatory_arrays.npz",
    "confirmatory_endpoints.json",
    "confirmatory_job_table.json",
    "holdout_analysis.json",
    "manifest.json",
    "metrics.json",
    "primary_analysis.json",
]


def _read_json(name: str) -> dict[str, object]:
    return json.loads((EVIDENCE_DIRECTORY / name).read_text(encoding="utf-8"))


def _current_state_section(document: str) -> str:
    heading = "## Current state\n"
    start = document.index(heading) + len(heading)
    next_heading = document.find("\n## ", start)
    return document[start:] if next_heading == -1 else document[start:next_heading]


def test_source_binding_pins_the_complete_original_inventory() -> None:
    """A stale binding or corrupted replay input breaks the source contract."""

    binding = _read_json("source_binding.json")

    assert binding["scientific_revision"] == SCIENTIFIC_REVISION
    assert binding["coordinator_evidence_sha256"] == COORDINATOR_EVIDENCE_SHA256
    assert binding["complete_original_inventory"] == ORIGINAL_INVENTORY
    assert binding["tracked_scientific_subset"] == TRACKED_SCIENTIFIC_SUBSET

    untracked_execution_logs = {
        "confirmatory_execution.json",
        "primary_execution.json",
    }
    assert untracked_execution_logs <= set(binding["complete_original_inventory"])
    assert (
        set(binding["complete_original_inventory"])
        - set(binding["tracked_scientific_subset"])
        == untracked_execution_logs
    )

    for name in TRACKED_SCIENTIFIC_SUBSET:
        path = EVIDENCE_DIRECTORY / name
        expected = ORIGINAL_INVENTORY[name]
        assert path.stat().st_size == expected["size_bytes"]
        assert sha256(path.read_bytes()).hexdigest() == expected["sha256"]


def test_current_result_matches_copied_primary_and_holdout_records() -> None:
    """A changed current outcome or copied analysis record breaks the contract."""

    current = _read_json("current_result.json")
    primary = _read_json("primary_analysis.json")
    holdout = _read_json("holdout_analysis.json")

    assert current["completed_jobs"] == 40
    assert current["missing_jobs"] == 0
    assert current["rejected_jobs"] == 0
    assert current["retried_jobs"] == 0
    assert current["primary"]["classification"] == "inconclusive"
    assert current["primary"]["estimate"] == -0.00026786510016806844
    assert current["primary"]["interval"][1] == -0.00021070275415133334
    assert current["holdout"]["scope"] == "descriptive_replication_only"
    assert current["producer_verification_state"] == "CANDIDATE"

    assert current["primary"]["classification"] == primary["classification"]
    assert current["primary"]["estimate"] == primary["primary_endpoint"]["estimate"]
    assert current["primary"]["interval"] == [
        primary["primary_endpoint"]["lower"],
        primary["primary_endpoint"]["upper"],
    ]
    assert current["holdout"]["scope"] == holdout["analysis_scope"]
    assert current["holdout"]["estimate"] == holdout["primary_endpoint"]["estimate"]
    assert current["holdout"]["interval"] == [
        holdout["primary_endpoint"]["lower"],
        holdout["primary_endpoint"]["upper"],
    ]
    assert current["producer_verification_state"] == primary["verification_state"]
    assert current["producer_verification_state"] == holdout["verification_state"]


def test_primary_and_holdout_job_populations_are_exact_and_disjoint() -> None:
    """A pooled, overlapping, or incomplete C/H population breaks the contract."""

    current = _read_json("current_result.json")
    primary = _read_json("primary_analysis.json")
    holdout = _read_json("holdout_analysis.json")
    published_table = _read_json("confirmatory_job_table.json")
    primary_job_ids = primary["primary_job_ids"]
    holdout_job_ids = holdout["holdout_job_ids"]
    expected_primary_job_ids = [f"C{index:03d}" for index in range(1, 31)]
    expected_holdout_job_ids = [f"H{index:03d}" for index in range(1, 11)]

    assert primary_job_ids == expected_primary_job_ids
    assert holdout_job_ids == expected_holdout_job_ids
    assert published_table["executed_primary_job_ids"] == primary_job_ids
    assert published_table["executed_holdout_job_ids"] == holdout_job_ids
    assert current["primary"]["job_count"] == len(primary_job_ids) == 30
    assert current["holdout"]["job_count"] == len(holdout_job_ids) == 10
    assert set(primary_job_ids).isdisjoint(holdout_job_ids)
    assert len(set(primary_job_ids) | set(holdout_job_ids)) == current["completed_jobs"] == 40


def test_source_binding_distinguishes_job_table_file_and_canonical_payload_hashes() -> None:
    """A published execution wrapper cannot replace the frozen planned table hash."""

    binding = _read_json("source_binding.json")
    primary = _read_json("primary_analysis.json")
    holdout = _read_json("holdout_analysis.json")
    manifest = _read_json("manifest.json")
    published_table = _read_json("confirmatory_job_table.json")

    raw_file_hash = sha256(
        (EVIDENCE_DIRECTORY / "confirmatory_job_table.json").read_bytes()
    ).hexdigest()
    planned_table = dict(published_table)
    planned_table.pop("executed_primary_job_ids")
    planned_table.pop("executed_holdout_job_ids")
    planned_table["confirmatory_executed"] = False
    canonical_payload_hash = sha256(
        json.dumps(
            planned_table,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()

    assert binding["complete_original_inventory"]["confirmatory_job_table.json"]["sha256"] == raw_file_hash
    assert raw_file_hash == "a50dd3893ce1ad9c081a8e2f2cbc5adc676e2b217c9c3ec321e8b0d62b453adf"
    assert binding["scientific_payload_hashes"]["job_table_canonical_json_sha256"] == canonical_payload_hash
    assert canonical_payload_hash == "c3d019beb7c7cc1e6c1d383c3069745c528859aba4b1ded0de1c3a97449075cd"
    assert primary["job_table_sha256"] == canonical_payload_hash
    assert holdout["job_table_sha256"] == canonical_payload_hash
    assert manifest["provenance"]["input_hashes"]["job_table_sha256"] == canonical_payload_hash


def test_current_state_section_links_the_binding_and_states_the_current_outcome() -> None:
    """Stale pilot language cannot satisfy or invalidate the current outcome."""

    document = RESULT_DOCUMENT.read_text(encoding="utf-8")
    current_state = _current_state_section(document)

    assert BINDING_LINK in current_state
    assert "[current result](../verification/evidence/2026-08-10-gaussian-confirmatory-fcb2c49/current_result.json)" in current_state
    assert "40-job" in current_state
    assert "inconclusive" in current_state
    assert "CANDIDATE" in current_state
    assert "p <= 2/10001" in current_state
    assert "C and H jobs were not run" not in current_state
