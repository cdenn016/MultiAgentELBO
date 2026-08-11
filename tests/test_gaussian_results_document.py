"""Contract for the current Gaussian fixed-ray result record.

The historical pilot narrative remains intentionally present in the results
document.  Assertions about the completed confirmatory run therefore inspect
only the explicitly delimited current-state section.
"""

from __future__ import annotations

import json
import math
import re
from hashlib import sha256
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIRECTORY = (
    REPOSITORY_ROOT
    / "docs"
    / "verification"
    / "evidence"
    / "2026-08-10-gaussian-confirmatory-fcb2c49"
)
DIAGNOSTIC_EVIDENCE_DIRECTORY = (
    REPOSITORY_ROOT
    / "docs"
    / "verification"
    / "evidence"
    / "2026-08-10-fixed-model-attraction-diagnostic"
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
DIAGNOSTIC_REVISION = "039df35daa30a49e90f178edde7bfc999a7ee629"
DIAGNOSTIC_SOURCE_BINDING_SHA256 = (
    "c9b6a73764f51b6269f7ba4296985128ede106fa4853d9a02d83d4bbe24d95c0"
)
DIAGNOSTIC_BINDING_SHA256 = (
    "df3130e56bfd1bdd91801a13b6f6ffabe16931813a264ff3e2e2805891b7a355"
)
DIAGNOSTIC_BOUND_ARTIFACTS = {
    "config.json": {
        "sha256": "0fed6f65531407e59c52b9d3916164c0f7c0810a6c5421a91fec8a33e53bea71",
        "size_bytes": 917,
    },
    "fixed_model_diagnostic_arrays.npz": {
        "sha256": "1597a92acf50811687183f0062f104acb3c5e4649bb6270e0b153841f9e08bff",
        "size_bytes": 278274,
    },
    "fixed_model_explanation.json": {
        "sha256": "aed3fd6a3620eff3fefe004b7f3ad65884d3d5a73378edd8ed0fb629c65ce20a",
        "size_bytes": 810,
    },
    "fixed_model_spectral_diagnostics.json": {
        "sha256": "8f1fbf50ca691c0245c0e59eaaced25af6c02aa5b4f46ac0d7908961e8e8669b",
        "size_bytes": 6233,
    },
    "fixed_model_support_certificate.json": {
        "sha256": "a65bd15e36d85cf810cdb5f7bb5a7bf0dcfcf56672d6601e3d7237be06b07c8b",
        "size_bytes": 2101,
    },
    "fixed_model_trajectory_diagnostics.json": {
        "sha256": "e6169a6fad904bf92082f6d1c12203a8d843e01e473804e1dae3161037111f4f",
        "size_bytes": 192056,
    },
    "manifest.json": {
        "sha256": "1829624d76fe723606b5e20fbd7ad85961610b2513c59271c641f560ac38d907",
        "size_bytes": 28891,
    },
    "metrics.json": {
        "sha256": "9aed3241befa42686486b7ce7c2d04ce771bf7d17d542dc6ecdb93798ae1f784",
        "size_bytes": 1077,
    },
}
DIAGNOSTIC_TRACKED_INVENTORY = {
    **DIAGNOSTIC_BOUND_ARTIFACTS,
    "source_to_output_binding.json": {
        "sha256": DIAGNOSTIC_BINDING_SHA256,
        "size_bytes": 5636,
    },
}
DIAGNOSTIC_BINDING_LINK = (
    "[source-to-output binding](../verification/evidence/"
    "2026-08-10-fixed-model-attraction-diagnostic/source_to_output_binding.json)"
)
PRIVATE_BYTE_PATTERNS = {
    "Windows user root": re.compile(rb"[A-Za-z]:[\\\\/]+Users[\\\\/]", re.IGNORECASE),
    "Windows temporary root": re.compile(rb"[A-Za-z]:[\\\\/]+tmp[\\\\/]", re.IGNORECASE),
    "POSIX user root": re.compile(rb"/(?:Users|home)/", re.IGNORECASE),
    "account name": re.compile(rb"chris and christine", re.IGNORECASE),
    "isolated worktree name": re.compile(
        rb"MultiAgentELBO-fixed-model-attraction-diagnosis-design-20260810",
        re.IGNORECASE,
    ),
}
TELEMETRY_KEY_PATTERN = re.compile(
    r"(?:^|_)(?:pid|process(?:es)?|elapsed|duration|wall_time|started_at|finished_at)(?:$|_)",
    re.IGNORECASE,
)
REQUIRED_APPLICATION_PREMISES = {
    "complete_uncensored_endpoints_for_adjacent_pairs_and_balanced_alternating": {
        "censored_worst_case_count": 0,
        "completed_eligible_job_count": 40,
        "passed": True,
        "rejected_endpoint_count": 0,
        "scheme_endpoint_count": 80,
    },
    "endpoint_scales_4_through_8_unchanged": {
        "diagnostic_record_count": 80,
        "passed": True,
        "source_scale_window": [4, 5, 6, 7, 8],
    },
    "frozen_maps_unchanged": {
        "passed": True,
        "runtime_map_conformance_max_absolute_error": {
            "adjacent_pairs": 0.0,
            "balanced_alternating": 5.551115123125783e-17,
        },
    },
    "initial_coefficients_admitted_in_basin": {
        "any_state_basin_exit_count": 0,
        "basin": [0.25, 4.0],
        "initial_vector_count": 40,
        "maximum": 3.840230242657913,
        "minimum": 0.2505016290001245,
        "outside_basin_scalar_count": 0,
        "passed": True,
    },
    "paired_least_favorable_maximum_unchanged": {
        "passed": True,
        "per_job_maximum_check_count": 40,
        "pooled_output_present": False,
        "populations": {"C": 30, "H_descriptive_only": 10},
    },
    "raw_angle_ols_unchanged": {
        "diagnostic_record_count": 80,
        "endpoint_angle": "raw_projective_angle",
        "endpoint_estimator": "ordinary_least_squares_slope",
        "passed": True,
    },
}


def _read_json(name: str) -> dict[str, object]:
    return json.loads((EVIDENCE_DIRECTORY / name).read_text(encoding="utf-8"))


def _reject_nonfinite_constant(value: str) -> None:
    raise AssertionError(f"nonfinite JSON constant: {value}")


def _read_strict_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=_reject_nonfinite_constant,
    )
    assert isinstance(value, dict)
    return value


def _walk_json(value: Any, path: str = "$") -> list[tuple[str, Any]]:
    values = [(path, value)]
    if isinstance(value, dict):
        for key, child in value.items():
            values.extend(_walk_json(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            values.extend(_walk_json(child, f"{path}[{index}]"))
    return values


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


def test_fixed_model_diagnostic_extract_has_exact_bound_inventory() -> None:
    """A missing, extra, truncated, or changed public artifact breaks publication."""

    actual_names = {
        path.name for path in DIAGNOSTIC_EVIDENCE_DIRECTORY.iterdir() if path.is_file()
    }
    assert actual_names == set(DIAGNOSTIC_TRACKED_INVENTORY)

    binding_path = DIAGNOSTIC_EVIDENCE_DIRECTORY / "source_to_output_binding.json"
    binding = _read_strict_json(binding_path)
    assert binding["diagnostic_artifacts"] == DIAGNOSTIC_BOUND_ARTIFACTS

    for name, expected in DIAGNOSTIC_TRACKED_INVENTORY.items():
        path = DIAGNOSTIC_EVIDENCE_DIRECTORY / name
        payload = path.read_bytes()
        assert len(payload) == expected["size_bytes"]
        assert sha256(payload).hexdigest() == expected["sha256"]


def test_public_manifest_has_one_enumerated_redaction_and_raw_run_a_is_hash_only() -> None:
    """A private raw manifest or unenumerated semantic change breaks the extract."""

    binding = _read_strict_json(
        DIAGNOSTIC_EVIDENCE_DIRECTORY / "source_to_output_binding.json"
    )
    manifest_path = DIAGNOSTIC_EVIDENCE_DIRECTORY / "manifest.json"
    manifest = _read_strict_json(manifest_path)

    assert binding["public_manifest"] == DIAGNOSTIC_BOUND_ARTIFACTS["manifest.json"]
    assert binding["redactions"] == [
        {
            "json_pointer": "/provenance/theory_root",
            "raw_value_sha256": "13d059ed1d13d16b93c9852a4473b19a2069ad2df9551c28055ed39100d757af",
            "reason": "remove machine-local absolute worktree path",
            "replacement": "Theory",
        }
    ]
    assert binding["manifest_semantics_unchanged_except_enumerated_redactions"] is True
    assert manifest["provenance"]["theory_root"] == "Theory"
    assert binding["raw_manifest"] == {
        "logical_source": "task-6-lane-a/run-a/manifest.json",
        "sha256": "ca542a09725823c2fdb51845dac44ec9de984add0d8ebf3429e5785ae6e502c0",
        "size_bytes": 29038,
    }
    assert set(binding["raw_manifest"]) == {"logical_source", "sha256", "size_bytes"}
    assert binding["raw_manifest"]["sha256"] != sha256(manifest_path.read_bytes()).hexdigest()


def test_fixed_model_diagnostic_extract_contains_no_private_or_telemetry_bytes() -> None:
    """Machine paths, process telemetry, or nonfinite JSON cannot enter Git."""

    for path in DIAGNOSTIC_EVIDENCE_DIRECTORY.iterdir():
        if not path.is_file():
            continue
        payload = path.read_bytes()
        for label, pattern in PRIVATE_BYTE_PATTERNS.items():
            assert pattern.search(payload) is None, f"{label} in {path.name}"
        if path.suffix != ".json":
            continue
        document = _read_strict_json(path)
        for json_path, value in _walk_json(document):
            if isinstance(value, float):
                assert math.isfinite(value), f"nonfinite value at {path.name}:{json_path}"
            if isinstance(value, dict):
                for key in value:
                    assert TELEMETRY_KEY_PATTERN.search(key) is None, (
                        f"telemetry key at {path.name}:{json_path}.{key}"
                    )


def test_fixed_model_binding_records_all_six_passed_premises_and_both_oracles() -> None:
    """A weakened application premise or missing independent oracle blocks use."""

    binding = _read_strict_json(
        DIAGNOSTIC_EVIDENCE_DIRECTORY / "source_to_output_binding.json"
    )
    evidence = binding["application_premise_evidence"]

    assert evidence["all_passed"] is True
    assert evidence["required_premises"] == REQUIRED_APPLICATION_PREMISES
    assert evidence["oracle_bindings"] == {
        "lane_b1_math_oracle": {
            "sha256": "0fd58a395ca04c8300548e1137465b4622a843487be07eeafb4cbc5fadd93fb2",
            "size_bytes": 57466,
        },
        "lane_b2_trajectory_oracle": {
            "sha256": "6280fb7e7d69404c02499f4598df749cc20368b0fb635edd4554a91f97df7a1c",
            "size_bytes": 350002,
        },
    }


def test_fixed_model_artifacts_preserve_semantics_array_inventory_and_candidate_state() -> None:
    """A pooled population, wrong theorem boundary, or promoted producer is invalid."""

    support = _read_strict_json(
        DIAGNOSTIC_EVIDENCE_DIRECTORY / "fixed_model_support_certificate.json"
    )
    spectral = _read_strict_json(
        DIAGNOSTIC_EVIDENCE_DIRECTORY / "fixed_model_spectral_diagnostics.json"
    )
    trajectory = _read_strict_json(
        DIAGNOSTIC_EVIDENCE_DIRECTORY / "fixed_model_trajectory_diagnostics.json"
    )
    explanation = _read_strict_json(
        DIAGNOSTIC_EVIDENCE_DIRECTORY / "fixed_model_explanation.json"
    )
    manifest = _read_strict_json(DIAGNOSTIC_EVIDENCE_DIRECTORY / "manifest.json")

    assert support["rational_slope_lower_bound"] == {
        "fraction": {"denominator": 625, "numerator": -9}
    }
    assert support["rational_margin_above_threshold"] == {
        "fraction": {"denominator": 1250, "numerator": 7}
    }
    assert support["paired_support_boundary_reachable"] is False
    assert support["theorem_status"] == "ESTABLISHED"
    assert support["attraction_claim"] == "not_established"
    assert support["universality_claim"] == "not_established"

    adjacent = spectral["maps"]["adjacent_pairs"]
    alternating = spectral["maps"]["balanced_alternating"]
    assert adjacent["eigenvalue_multiplicities"] == [
        {"imag": 0.0, "multiplicity": 5, "real": 0.4}
    ]
    assert adjacent["slow_cluster_dimension"] == 5
    assert alternating["slow_cluster_dimension"] == 3
    assert alternating["transient_amplification"] is False

    assert trajectory["replay_call_count"] == 80
    assert len(trajectory["records"]) == 80
    assert trajectory["primary_C"]["job_count"] == 30
    assert trajectory["primary_C"]["estimate"] == -0.0002678651001680694
    assert trajectory["descriptive_H"]["job_count"] == 10
    assert trajectory["descriptive_H"]["scope"] == "descriptive_replication_only"
    assert trajectory["descriptive_H"]["estimate"] == -0.0003031040729630512
    assert set(trajectory["primary_C"]["job_ids"]).isdisjoint(
        trajectory["descriptive_H"]["job_ids"]
    )
    assert "pooled" not in trajectory
    assert len(trajectory["array_sha256"]) == 180
    assert trajectory["array_sha256"] == manifest["provenance"]["array_sha256"]

    assert explanation["completed_finite_classification"] == "inconclusive"
    assert explanation["mathematical_attraction"]["conclusion"] == "INCONCLUSIVE"
    assert explanation["universality"]["theorem_status"] == "OPEN"
    assert explanation["universality"]["conclusion"] == "INCONCLUSIVE"

    producer_states = {
        value
        for document in (support, spectral, trajectory, explanation)
        for json_path, value in _walk_json(document)
        if json_path.endswith(".verification_state")
    }
    assert producer_states == {"CANDIDATE"}


def test_current_result_records_the_bounded_fixed_model_diagnostic() -> None:
    """The authoritative record must not overstate the conditional diagnosis."""

    current = _read_json("current_result.json")
    diagnostic = current["fixed_model_diagnostic"]

    assert diagnostic["diagnostic_revision"] == DIAGNOSTIC_REVISION
    assert diagnostic["source_binding_sha256"] == DIAGNOSTIC_SOURCE_BINDING_SHA256
    assert diagnostic["evidence_directory"] == (
        "docs/verification/evidence/2026-08-10-fixed-model-attraction-diagnostic"
    )
    assert diagnostic["artifact_sha256"] == {
        name: record["sha256"] for name, record in DIAGNOSTIC_TRACKED_INVENTORY.items()
    }
    assert diagnostic["oracle_bindings"] == {
        "lane_b1_math_oracle": {
            "sha256": "0fd58a395ca04c8300548e1137465b4622a843487be07eeafb4cbc5fadd93fb2",
            "size_bytes": 57466,
        },
        "lane_b2_trajectory_oracle": {
            "sha256": "6280fb7e7d69404c02499f4598df749cc20368b0fb635edd4554a91f97df7a1c",
            "size_bytes": 350002,
        },
    }
    assert diagnostic["exact_map_spectra"] == {
        "adjacent_pairs": {
            "characteristic_polynomial": "(lambda - 1)(lambda - 2/5)^5",
            "spectrum": [
                {"eigenvalue": "1", "multiplicity": 1},
                {"eigenvalue": "2/5", "multiplicity": 5},
            ],
        },
        "balanced_alternating": {
            "characteristic_polynomial": (
                "(lambda - 1)(5 lambda - 1)(50 lambda^2 - 15 lambda + 2)"
                "(100 lambda^2 - 30 lambda + 3)/25000"
            ),
            "spectrum": [
                {"eigenvalue": "1", "multiplicity": 1},
                {"eigenvalue": "1/5", "multiplicity": 1},
                {"eigenvalue": "(3 + i sqrt(7))/20", "multiplicity": 1},
                {"eigenvalue": "(3 - i sqrt(7))/20", "multiplicity": 1},
                {"eigenvalue": "(3 + i sqrt(3))/20", "multiplicity": 1},
                {"eigenvalue": "(3 - i sqrt(3))/20", "multiplicity": 1},
            ],
        },
    }
    assert diagnostic["application_premises"] == REQUIRED_APPLICATION_PREMISES
    assert diagnostic["confirmatory_classification"] == {
        "unchanged": True,
        "value": "inconclusive",
    }

    endpoint = diagnostic["endpoint_feasibility"]
    assert endpoint["conditional_scope"] == {
        "complete_uncensored_endpoints": True,
        "endpoint_angle": "raw_projective_angle",
        "endpoint_estimator": "ordinary_least_squares_slope",
        "initial_coefficients": "[1/4,4]^6",
        "maps": ["adjacent_pairs", "balanced_alternating"],
        "paired_reduction": "least_favorable_maximum_across_two_frozen_schemes",
        "scales": [4, 5, 6, 7, 8],
    }
    assert endpoint["coefficient_of_variation_bound"] == "15/8"
    assert endpoint["tan_theta4_bound"] == "6/125"
    assert endpoint["rational_slope_lower_bound"] == "-9/625"
    assert endpoint["rational_margin_above_threshold"] == "7/1250"
    assert endpoint["threshold"] == "-1/50"
    assert endpoint["paired_support_boundary_reachable"] is False
    assert endpoint["theorem_status"] == "ESTABLISHED"
    assert endpoint["producer_verification_state"] == "CANDIDATE"
    assert endpoint["claim_origin"] == "APPLICATION_SPECIFIC"

    assert diagnostic["continuous_trajectory_summaries"] == {
        "primary_C": {
            "claim_origin": "APPLICATION_SPECIFIC",
            "estimate": -0.0002678651001680694,
            "job_count": 30,
            "population": "C",
            "producer_verification_state": "CANDIDATE",
            "scope": "confirmatory_primary",
            "theorem_status": "NUMERICAL",
        },
        "descriptive_H": {
            "claim_origin": "APPLICATION_SPECIFIC",
            "estimate": -0.0003031040729630512,
            "job_count": 10,
            "population": "H",
            "producer_verification_state": "CANDIDATE",
            "scope": "descriptive_replication_only",
            "theorem_status": "NUMERICAL",
        },
    }
    assert diagnostic["fixed_model_mathematical_attraction"] == {
        "claim_origin": "APPLICATION_SPECIFIC",
        "conclusion": "INCONCLUSIVE",
        "producer_verification_state": "CANDIDATE",
        "theorem_status": "OPEN",
    }
    assert diagnostic["unrestricted_universality"] == {
        "claim_origin": "APPLICATION_SPECIFIC",
        "mathematical_verification_state": "INCONCLUSIVE",
        "producer_verification_state": "CANDIDATE",
        "theorem_status": "OPEN",
    }


def test_current_state_section_links_and_scopes_the_fixed_model_diagnostic() -> None:
    """The public prose must state the finite conditional boundary without overclaiming."""

    current_state = _current_state_section(RESULT_DOCUMENT.read_text(encoding="utf-8"))
    current_state_flat = " ".join(current_state.split())

    assert "### Fixed-model endpoint-feasibility diagnostic" in current_state
    assert DIAGNOSTIC_BINDING_LINK in current_state
    assert "`[1/4,4]^6`" in current_state_flat
    assert "scales 4 through 8" in current_state_flat
    assert "raw-angle OLS" in current_state_flat
    assert "per-job least-favorable maximum" in current_state_flat
    assert (
        "`-0.02` practical-support boundary is structurally unreachable"
        in current_state_flat
    )
    assert "mathematical attraction remains `INCONCLUSIVE`" in current_state_flat
    assert "unrestricted universality remains `OPEN / INCONCLUSIVE`" in current_state_flat
    assert "attraction is false" not in current_state.lower()
    assert "mechanism is proved" not in current_state.lower()
