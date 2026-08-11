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


def _read_json(name: str) -> dict[str, object]:
    return json.loads((EVIDENCE_DIRECTORY / name).read_text(encoding="utf-8"))


def _current_state_section(document: str) -> str:
    heading = "## Current state\n"
    start = document.index(heading) + len(heading)
    next_heading = document.find("\n## ", start)
    return document[start:] if next_heading == -1 else document[start:next_heading]


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
    assert current["producer_verification_state"] == primary["verification_state"]
    assert current["producer_verification_state"] == holdout["verification_state"]


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
