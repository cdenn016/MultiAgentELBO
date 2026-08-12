"""Frozen contracts for the scientific-integrity remediation program."""

from __future__ import annotations

import json
from pathlib import Path


AUDIT_DISPOSITION_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "verification"
    / "remediation"
    / "audit-disposition-v1.json"
)

EXPECTED_OWNERS = {
    "AUD-01": "B", "AUD-02": "B", "AUD-03": "A", "AUD-04": "B",
    "AUD-05": "B", "AUD-06": "C", "AUD-07": "C", "AUD-08": "C",
    "AUD-09": "C", "AUD-10": "B", "AUD-11": "B", "AUD-12": "B",
    "AUD-13": "A", "AUD-14": "A", "AUD-15": "A", "AUD-16": "A",
    "AUD-17": "A", "AUD-18": "A", "AUD-19": "C", "AUD-20": "E",
    "AUD-21": "D", "AUD-22": "D",
}


def _load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def test_audit_disposition_is_complete_closed_and_uniquely_owned():
    payload = _load_json(AUDIT_DISPOSITION_PATH)
    assert set(payload) == {
        "schema_version", "program_design_revision", "audit_baseline_revision", "items"
    }
    assert payload["schema_version"] == "scientific-remediation-audit-disposition-v1"
    records = {item["audit_id"]: item for item in payload["items"]}
    assert set(records) == set(EXPECTED_OWNERS)
    assert len(records) == len(payload["items"]) == 22
    for audit_id, wave in EXPECTED_OWNERS.items():
        assert records[audit_id]["owning_wave"] == wave
        assert records[audit_id]["initial_disposition"] == "EVIDENCE_VERIFIED_AT_AUDIT_BASELINE"
        assert records[audit_id]["final_status"] == "INCONCLUSIVE_PENDING_OWNER_WAVE"
        assert set(records[audit_id]) == {
            "audit_id", "severity", "owning_wave", "source_locations",
            "public_interfaces", "red_reproducer", "green_guard",
            "evidence_class", "initial_disposition", "final_status",
        }
        assert records[audit_id]["source_locations"]
        assert records[audit_id]["public_interfaces"]
        assert records[audit_id]["red_reproducer"]
        assert records[audit_id]["green_guard"]
