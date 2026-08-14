from __future__ import annotations

import argparse
import json
import os
import socket
import sys
from pathlib import Path, PurePosixPath
from typing import Mapping, Sequence

if __package__ in (None, ""):
    _DIRECT_SCRIPT_REPO_ROOT = str(Path(__file__).resolve(strict=True).parents[1])
    if _DIRECT_SCRIPT_REPO_ROOT not in sys.path:
        sys.path.insert(0, _DIRECT_SCRIPT_REPO_ROOT)

from tools.remediation_evidence import (
    CPU_PYTHON,
    HISTORICAL_INVENTORY_PATH,
    PLAN_PATH,
    SNAPSHOT_PATH,
    GENERIC_PUBLIC_PATHS as CORE_GENERIC_PUBLIC_PATHS,
    PreparedEvidenceBundle,
    PreparedEvidenceFile,
    _canonical_json_object,
    _prepare_evidence_bundle as _prepare_generic_evidence_bundle_internal,
    _parse_junit_bytes,
    _finalize_evidence_index,
    _file_record,
    _git,
    _git_head,
    _require_closed_fields,
    _require_regular_unlinked_file,
    _reviewed_plan_binding,
    _sha256,
    _validate_command_record,
    _validate_detached_bundle,
    _validate_head_relationship,
    _validate_snapshot_payload,
    assert_no_literal_absolute_path,
    canonical_json_bytes,
    capture_environment_record,
    capture_verified_artifact_revision,
    prepare_evidence_bundle as _prepare_generic_evidence_bundle,
    privacy_transform_bytes,
    resolve_verified_verification_gate,
    publish_evidence_bundle,
    resolve_tested_input_policy,
    validate_evidence_index,
    validate_junit_skip_allowlist,
)


CLAIM_CRITERIA_BY_DOMAIN = {
    "code": (
        ("execution", "execution"),
        ("input_output_behavior", "input/output behavior"),
        ("boundary_failure_behavior", "boundary/failure behavior"),
        ("regression_coverage", "regression coverage"),
        ("configuration_reachability", "configuration reachability"),
        ("reproducibility", "reproducibility"),
    ),
    "evidence": (
        ("source_authority", "source authority"),
        ("primary_source_status", "primary-source status"),
        ("exact_statement_support", "exact support for the statement"),
        ("quotation_data_fidelity", "quotation or data fidelity"),
        ("provenance", "provenance"),
        ("artifact_revision_currency", "currency for the stated artifact revision"),
        ("material_counterevidence_coverage", "material counterevidence coverage"),
    ),
}
CLAIM_SPECS = (
    {
        "id": "CHK-WAVE0-CONTRACT-COMPLETENESS",
        "domain": "code",
        "severity": "medium",
        "kind": "mechanical",
        "evidence_ids": (
            "wave0-targeted-junit",
            "wave0-subsystem-junit",
            "wave0-full-junit",
        ),
        "statement": "The Wave 0 contract records, validators, and exact migration inventory are complete and mechanically enforced at this artifact revision.",
    },
    {
        "id": "CHK-WAVE0-HISTORICAL-BYTE-PINS",
        "domain": "evidence",
        "severity": "medium",
        "kind": "reproduced_source",
        "evidence_ids": (
            "wave0-historical-inventory-source",
            "wave0-historical-reproduced-source",
        ),
        "statement": "The two historical fixed-ray inventories reproduce all 19 source byte sizes and SHA-256 values at this artifact revision without upgrading their scientific status.",
    },
)
EVIDENCE_LOCATIONS_BY_ID = {
    "wave0-targeted-junit": "verification-evidence/wave-0/{evidence_short}/targeted.xml",
    "wave0-subsystem-junit": "verification-evidence/wave-0/{evidence_short}/subsystem.xml",
    "wave0-full-junit": "verification-evidence/wave-0/{evidence_short}/full.xml",
    "wave0-historical-inventory-source": str(HISTORICAL_INVENTORY_PATH),
    "wave0-historical-reproduced-source": "verification-evidence/wave-0/{evidence_short}/historical-verification.json",
}
INITIAL_VIEW_IDS = ("code-contract-review", "evidence-source-review")
TARGET4_ADDITIONAL_VIEW_IDS = (
    "boundary-failure-review",
    "provenance-counterevidence-review",
)
TARGET8_ADDITIONAL_VIEW_IDS = (
    "configuration-reachability-review",
    "historical-source-adversary",
    "path-privacy-adversary",
    "reproducibility-review",
)
VIEW_IDS_BY_TARGET = {
    2: INITIAL_VIEW_IDS,
    4: INITIAL_VIEW_IDS + TARGET4_ADDITIONAL_VIEW_IDS,
    8: INITIAL_VIEW_IDS + TARGET4_ADDITIONAL_VIEW_IDS + TARGET8_ADDITIONAL_VIEW_IDS,
}
INITIAL_REVIEW_PATHS = (
    "reviews/code-contract-review.json",
    "reviews/evidence-source-review.json",
)
TARGET4_ADDITIONAL_REVIEW_PATHS = (
    "reviews/escalation/boundary-failure-review.json",
    "reviews/escalation/provenance-counterevidence-review.json",
)
TARGET8_ADDITIONAL_REVIEW_PATHS = (
    "reviews/escalation/configuration-reachability-review.json",
    "reviews/escalation/historical-source-adversary.json",
    "reviews/escalation/path-privacy-adversary.json",
    "reviews/escalation/reproducibility-review.json",
)
REVIEW_PATHS_BY_TARGET = {
    2: INITIAL_REVIEW_PATHS,
    4: INITIAL_REVIEW_PATHS + TARGET4_ADDITIONAL_REVIEW_PATHS,
    8: INITIAL_REVIEW_PATHS
    + TARGET4_ADDITIONAL_REVIEW_PATHS
    + TARGET8_ADDITIONAL_REVIEW_PATHS,
}
ADJUDICATOR_PATHS = (
    "reviews/adjudicators/CHK-WAVE0-CONTRACT-COMPLETENESS.json",
    "reviews/adjudicators/CHK-WAVE0-HISTORICAL-BYTE-PINS.json",
)
ALLOWED_ESCALATION_TRIGGERS = (
    "criterion_disagreement",
    "high_dispersion",
    "small_margin",
)
GENERIC_PUBLIC_PATHS = (
    "commands/full.json",
    "commands/subsystem.json",
    "commands/targeted.json",
    "dependencies.json",
    "environment.json",
    "full.xml",
    "index.json",
    "plan-binding.json",
    "privacy-transform.json",
    "subsystem.xml",
    "targeted.xml",
)
CANDIDATE_PUBLIC_PATHS = GENERIC_PUBLIC_PATHS + ("historical-verification.json",)
CLOSURE_PUBLIC_PATHS_BY_TARGET = {
    2: GENERIC_PUBLIC_PATHS
    + ("historical-verification.json",)
    + REVIEW_PATHS_BY_TARGET[2]
    + ADJUDICATOR_PATHS,
    4: GENERIC_PUBLIC_PATHS
    + ("historical-verification.json",)
    + REVIEW_PATHS_BY_TARGET[4]
    + ADJUDICATOR_PATHS,
    8: GENERIC_PUBLIC_PATHS
    + ("historical-verification.json",)
    + REVIEW_PATHS_BY_TARGET[8]
    + ADJUDICATOR_PATHS,
}
SKIP_ALLOWLIST_BY_SUITE = {
    "targeted": {},
    "subsystem": {},
    "full": {
        "tests.test_artifacts::test_finalize_rejects_a_declared_symlink": "capability unavailable: symbolic_link",
        "tests.test_artifacts::test_finalize_rejects_a_declared_file_with_an_external_hard_link": "capability unavailable: hard_link",
        "tests.test_artifacts::test_finalize_rejects_an_external_hard_link_to_core_config": "capability unavailable: hard_link",
        "tests.test_artifacts::test_finalize_rejects_duplicate_file_identity_within_inventory": "capability unavailable: hard_link",
        "tests.test_experiment_support::test_validated_renderer_status_rejects_a_publication_symlink_escape": "capability unavailable: symbolic_link",
        "tests.test_cuda_backend::test_pinned_cuda_worker_runs_first_job_with_determinism_environment": "requires explicit dedicated CUDA-lane opt-in",
    },
}
REVIEW_CONTEXT_FIELDS = (
    "schema_version",
    "tested_git_head",
    "implementation_parent_git_head",
    "evidence_diff_inventory",
    "candidate_evidence_inventory",
    "raw_command_inventory",
    "raw_junit_inventory",
    "tested_input_inventory",
    "source_config_inventory",
    "dependency_inventory",
    "environment_inventory",
    "reviewed_plan_bytes",
    "verification_snapshot_bytes",
    "historical_source_bytes",
    "historical_reproduced_source",
    "claim_specs",
    "public_path_contracts",
)
DEPENDENCY_INPUT_PATHS = (
    "pyproject.toml",
    "environments/cuda-rtx5090-cu128.lock.txt",
    str(SNAPSHOT_PATH),
)
STATUS_BOUNDARY = "The reproduced bytes establish compatibility and byte-pinning only, not current scientific promotion."
REVIEW_FIELDS = {
    "schema_version",
    "view_id",
    "calibration_kind",
    "tested_git_head",
    "implementation_parent_git_head",
    "reviewed_input_inventory_sha256",
    "reviewed_paths",
    "claim_scores",
    "verdict",
    "escalation_triggers",
    "unresolved_disagreement",
    "open_obligations",
    "result_location",
    "falsification_conditions",
}
CLAIM_SCORE_FIELDS = {
    "claim_id",
    "domain",
    "severity",
    "evidence_ids",
    "criteria",
    "verdict",
    "escalation_triggers",
    "unresolved_disagreement",
    "open_obligations",
}
INITIAL_CLAIM_SCORE_FIELDS = CLAIM_SCORE_FIELDS | {
    "candidate_ids",
    "candidate_descriptions",
    "comparison_order",
    "comparison_outcome",
    "comparison_criteria",
}
ADJUDICATOR_FIELDS = {
    "schema_version",
    "role",
    "claim_id",
    "tested_git_head",
    "implementation_parent_git_head",
    "reviewed_input_inventory_sha256",
    "escalation_triggers",
    "escalation_target",
    "view_ids",
    "result",
    "evidence_ids",
    "result_location",
    "reason",
    "falsification_condition",
    "open_obligations",
}


def _claim_spec(claim_id: str) -> dict[str, object]:
    try:
        return next(item for item in CLAIM_SPECS if item["id"] == claim_id)
    except StopIteration as error:
        raise ValueError(f"unknown Wave 0 claim ID: {claim_id}") from error


def required_review_target(
    *,
    completed_view_count: int,
    retained_triggers: Sequence[str],
    unresolved_criterion_disagreement: bool,
) -> int:
    if isinstance(completed_view_count, bool) or completed_view_count not in (2, 4, 8):
        raise ValueError("completed view count must be exactly 2, 4, or 8")
    triggers = tuple(retained_triggers)
    if len(set(triggers)) != len(triggers):
        raise ValueError("duplicate escalation trigger")
    unknown = set(triggers) - set(ALLOWED_ESCALATION_TRIGGERS)
    if unknown:
        raise ValueError(f"unknown escalation trigger: {sorted(unknown)[0]}")
    if unresolved_criterion_disagreement and "criterion_disagreement" not in triggers:
        raise ValueError(
            "unresolved criterion disagreement requires its retained trigger"
        )
    if completed_view_count == 2:
        return 4 if triggers else 2
    if completed_view_count == 4:
        return 8 if unresolved_criterion_disagreement else 4
    return 8


def compute_criterion_aggregates(
    view_scores: Sequence[Mapping[str, int | float]],
    *,
    criterion_keys: Sequence[str],
) -> dict[str, float]:
    if not view_scores:
        raise ValueError("at least one view score is required")
    keys = tuple(criterion_keys)
    if len(set(keys)) != len(keys) or not keys:
        raise ValueError("criterion keys must be nonempty and unique")
    expected = set(keys)
    result: dict[str, float] = {}
    for view in view_scores:
        if set(view) != expected:
            raise ValueError("view criterion keys differ from the exact claim domain")
        for value in view.values():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError("criterion score must be numeric")
            if not 0 <= value <= 20:
                raise ValueError("criterion score must be in [0,20]")
    for key in keys:
        result[key] = sum(float(view[key]) for view in view_scores) / len(view_scores)
    return result


def _suite_argv(raw_dir: Path, suite: str) -> list[str]:
    raw_dir = PurePosixPath(raw_dir.as_posix())
    prefix = [str(CPU_PYTHON), "-B", "-m", "pytest"]
    if suite == "targeted":
        selected = [
            "tests/test_remediation_contracts.py",
            "tests/test_remediation_evidence.py",
        ]
    elif suite == "subsystem":
        selected = [
            "tests/test_remediation_contracts.py",
            "tests/test_remediation_evidence.py",
            "tests/test_shared_scientific_contracts.py",
            "tests/test_gaussian_results_document.py",
        ]
    elif suite == "full":
        selected = []
    else:
        raise ValueError(f"unknown Wave 0 suite: {suite}")
    return (
        prefix
        + selected
        + [
            "-q",
            "-p",
            "no:cacheprovider",
            f"--basetemp={raw_dir / f'tmp-{suite}'}",
            f"--junitxml={raw_dir / f'{suite}.raw.xml'}",
        ]
    )


def _source_config_bindings(policy: Mapping[str, object]) -> list[dict[str, object]]:
    inputs = policy["inputs"]
    assert isinstance(inputs, list)
    explicit = {
        "docs/audits/2026-08-11-post-fixed-ray-deep-audit.md",
        "docs/superpowers/specs/2026-08-11-scientific-integrity-remediation-program-design.md",
        str(PLAN_PATH),
        "tools/remediation_evidence.py",
        "tools/build_wave0_evidence.py",
        "tests/test_remediation_contracts.py",
        "tests/test_remediation_evidence.py",
        "tests/test_artifacts.py",
        "tests/test_experiment_support.py",
        "pyproject.toml",
        ".gitignore",
        ".gitattributes",
    }
    selected = [
        item
        for item in inputs
        if isinstance(item, dict)
        and (
            str(item["path"]) in explicit
            or str(item["path"]).startswith("docs/verification/remediation/")
        )
    ]
    paths = {str(item["path"]) for item in selected}
    missing = explicit - paths
    if missing:
        raise ValueError(
            f"required source/config binding missing: {sorted(missing)[0]}"
        )
    return selected


def _historical_observations(
    repo_root: Path,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    inventory_bytes = _require_regular_unlinked_file(
        repo_root / HISTORICAL_INVENTORY_PATH, label="historical fixed-ray inventory"
    )
    inventory = json.loads(inventory_bytes)
    if not isinstance(inventory, dict) or set(inventory) != {
        "schema_version",
        "bundles",
    }:
        raise ValueError("historical fixed-ray inventory schema is not closed")
    source_inventory: list[dict[str, object]] = []
    observations: list[dict[str, object]] = []
    for bundle in inventory["bundles"]:
        for expected in bundle["files"]:
            path = expected["path"]
            data = _require_regular_unlinked_file(
                repo_root / path, label="historical fixed-ray source"
            )
            observed_sha = _sha256(data)
            observed_size = len(data)
            match = (
                observed_size == expected["size_bytes"]
                and observed_sha == expected["sha256"]
            )
            if not match:
                raise ValueError(f"historical fixed-ray source mismatch: {path}")
            source_inventory.append(_file_record(path, data))
            observations.append(
                {
                    "path": path,
                    "expected_size_bytes": expected["size_bytes"],
                    "observed_size_bytes": observed_size,
                    "expected_sha256": expected["sha256"],
                    "observed_sha256": observed_sha,
                    "match": True,
                }
            )
    source_inventory.sort(key=lambda item: str(item["path"]))
    observations.sort(key=lambda item: str(item["path"]))
    if (
        len(source_inventory) != 19
        or len({item["path"] for item in source_inventory}) != 19
    ):
        raise ValueError(
            "historical fixed-ray inventory must contain exactly 19 unique paths"
        )
    return source_inventory, observations


def _historical_verification_bytes(
    repo_root: Path,
    *,
    tested_head: str,
    implementation_parent: str,
) -> bytes:
    source_inventory, observations = _historical_observations(repo_root)
    return canonical_json_bytes(
        {
            "schema_version": "wave-0-historical-verification-v1",
            "tested_git_head": tested_head,
            "implementation_parent_git_head": implementation_parent,
            "source_inventory": source_inventory,
            "observations": observations,
            "status_boundary": STATUS_BOUNDARY,
        }
    )


def _validate_historical_verification(
    data: bytes,
    *,
    tested_head: str,
    implementation_parent: str,
) -> dict[str, object]:
    payload = json.loads(data)
    fields = {
        "schema_version",
        "tested_git_head",
        "implementation_parent_git_head",
        "source_inventory",
        "observations",
        "status_boundary",
    }
    if not isinstance(payload, dict):
        raise ValueError("historical verification must be an object")
    _require_closed_fields(payload, fields, label="historical verification")
    if canonical_json_bytes(payload) != data:
        raise ValueError("historical verification is not canonical JSON")
    if payload["schema_version"] != "wave-0-historical-verification-v1":
        raise ValueError("historical verification schema mismatch")
    if (
        payload["tested_git_head"] != tested_head
        or payload["implementation_parent_git_head"] != implementation_parent
    ):
        raise ValueError("historical verification head binding mismatch")
    if payload["status_boundary"] != STATUS_BOUNDARY:
        raise ValueError("historical verification status boundary mismatch")
    if len(payload["observations"]) != 19 or not all(
        item.get("match") is True for item in payload["observations"]
    ):
        raise ValueError(
            "historical verification must contain 19 matching observations"
        )
    assert_no_literal_absolute_path(data)
    return payload


def _snapshot_binding(repo_root: Path) -> tuple[dict[str, object], dict[str, object]]:
    data = _require_regular_unlinked_file(
        repo_root / SNAPSHOT_PATH, label="verification snapshot"
    )
    payload = json.loads(data)
    active_files = _validate_snapshot_payload(payload)
    return _file_record(str(SNAPSHOT_PATH), data), {
        **_file_record(str(SNAPSHOT_PATH), data),
        "active_files": active_files,
    }


def _inventory_tree(
    root: Path, *, prefix: Path | None = None
) -> list[dict[str, object]]:
    if not root.is_dir():
        raise ValueError(f"inventory directory is missing: {root}")
    base = prefix or root
    records = []
    for path in sorted(
        (item for item in root.rglob("*") if item.is_file()),
        key=lambda item: item.as_posix(),
    ):
        data = _require_regular_unlinked_file(path, label="inventoried evidence byte")
        records.append(_file_record(path.relative_to(base).as_posix(), data))
    return records


def _privacy_context(
    repo_root: Path, *, junit_public: Mapping[str, bytes] | None = None
) -> dict[str, object]:
    aliases: dict[str, str] = {}
    hash_replacements: dict[str, str] = {}
    junit_records: dict[str, dict[str, object]] = {}
    if junit_public:
        for suite, public in junit_public.items():
            junit_records[suite] = {
                "path": f"{suite}.xml",
                "size_bytes": len(public),
                "sha256": _sha256(public),
            }
    return {
        "repo_root": repo_root,
        "user_home": Path.home(),
        "cpu_python": CPU_PYTHON,
        "hostname": socket.gethostname(),
        "path_separator": os.pathsep,
        "path_aliases": aliases,
        "hash_replacements": hash_replacements,
        "junit_public_records": junit_records,
    }


def _mapping_record(
    *,
    raw_relative_path: str,
    public_path: str,
    raw: bytes,
    public: bytes,
    mapping: Mapping[str, object],
) -> dict[str, object]:
    return {
        "raw_relative_path": raw_relative_path,
        "raw_sha256": _sha256(raw),
        "public_path": public_path,
        "public_sha256": _sha256(public),
        "transforms": mapping["transforms"],
    }


def _kind_for_path(path: str) -> str:
    if path.startswith("commands/"):
        return "command"
    if path.endswith(".xml"):
        return "junit"
    if path == "environment.json":
        return "environment"
    if path == "dependencies.json":
        return "dependency"
    if path == "plan-binding.json":
        return "plan_binding"
    if path == "privacy-transform.json":
        return "privacy_transform"
    if path == "historical-verification.json":
        return "reproduced_source"
    if path.startswith("reviews/adjudicators/"):
        return "adjudicator"
    if path.startswith("reviews/"):
        return "review"
    raise ValueError(f"unknown public evidence kind: {path}")


def _validate_raw_command_and_junit(
    repo_root: Path,
    raw_dir: Path,
    suite: str,
) -> tuple[bytes, dict[str, object], bytes, dict[str, object]]:
    command_path = raw_dir / f"{suite}.command.json"
    junit_path = raw_dir / f"{suite}.raw.xml"
    command_bytes = _require_regular_unlinked_file(
        command_path, label=f"{suite} raw command"
    )
    command = _validate_command_record(json.loads(command_bytes), suite=suite)
    expected_argv = _suite_argv(raw_dir.relative_to(repo_root), suite)
    actual_argv = command["argv"]
    if actual_argv != expected_argv:
        raise ValueError(f"{suite} command argv differs from the frozen Wave 0 suite")
    expected_environment = capture_environment_record(
        repo_root, dependency_input_paths=DEPENDENCY_INPUT_PATHS
    )["environment_variables"]
    if command["env_allowlist"] != expected_environment:
        raise ValueError(f"{suite} command CPU environment drift")
    junit_bytes = _require_regular_unlinked_file(junit_path, label=f"{suite} raw JUnit")
    junit = _parse_junit_bytes(junit_bytes, public_path=junit_path.as_posix())
    validate_junit_skip_allowlist(junit, allowlist=SKIP_ALLOWLIST_BY_SUITE[suite])
    command_junit = command["junit"]
    assert isinstance(command_junit, dict)
    if command_junit != junit:
        raise ValueError(f"{suite} command JUnit binding differs from parsed XML")
    return command_bytes, command, junit_bytes, junit


def _prepare_wave0_virtual_bundle(
    *,
    repo_root: Path,
    raw_dir: Path,
    tested_head: str,
    implementation_parent: str,
    stage: str,
    expected_output: str,
    review_target: int | None,
    require_output_absent: bool,
) -> PreparedEvidenceBundle:
    if tuple(GENERIC_PUBLIC_PATHS) != tuple(CORE_GENERIC_PUBLIC_PATHS):
        raise ValueError("Wave 0 generic path constants drifted")
    policy = resolve_tested_input_policy(repo_root)
    policy_template = {
        key: policy[key]
        for key in ("schema_version", "selection_rules", "exclusion_rules")
    }
    source_bindings = _source_config_bindings(policy)
    source_paths = tuple(str(item["path"]) for item in source_bindings)
    raw_commands: dict[str, bytes] = {}
    raw_junits: dict[str, bytes] = {}
    for suite in ("targeted", "subsystem", "full"):
        command_bytes, _command, junit_bytes, _junit = _validate_raw_command_and_junit(
            repo_root, raw_dir, suite
        )
        raw_commands[suite] = command_bytes
        raw_junits[suite] = junit_bytes

    generic_kwargs = {
        "repo_root": repo_root,
        "wave": "wave-0",
        "evidence_stage": stage,
        "tested_git_head": tested_head,
        "implementation_parent_git_head": implementation_parent,
        "command_records": raw_commands,
        "source_config_paths": source_paths,
        "tested_input_policy": policy_template,
        "dependency_input_paths": DEPENDENCY_INPUT_PATHS,
        "raw_junit_bytes": raw_junits,
        "output_dir": expected_output,
    }
    if require_output_absent:
        generic = _prepare_generic_evidence_bundle(**generic_kwargs)
    else:
        generic = _prepare_generic_evidence_bundle_internal(
            **generic_kwargs, require_output_absent=False
        )
    base = {str(item.path): item.data for item in generic.files}
    if set(base) != set(GENERIC_PUBLIC_PATHS):
        raise ValueError("generic preparation returned a noncanonical base")
    provisional_index_bytes = base.pop("index.json")
    provisional_index = json.loads(provisional_index_bytes)
    if canonical_json_bytes(provisional_index) != provisional_index_bytes:
        raise ValueError("generic provisional index is not canonical JSON")
    privacy_bytes = base["privacy-transform.json"]
    privacy = json.loads(privacy_bytes)
    if canonical_json_bytes(privacy) != privacy_bytes:
        raise ValueError("generic privacy transform is not canonical JSON")
    mappings = list(privacy["records"])

    public_junits = {
        suite: base[f"{suite}.xml"] for suite in ("targeted", "subsystem", "full")
    }
    context = _privacy_context(repo_root, junit_public=public_junits)
    context["path_aliases"] = {
        str((raw_dir / f"{suite}.raw.xml").resolve()): f"{suite}.xml"
        for suite in ("targeted", "subsystem", "full")
    }
    context["hash_replacements"] = {
        _sha256(raw_junits[suite]): _sha256(public_junits[suite])
        for suite in ("targeted", "subsystem", "full")
    }
    extras: dict[str, bytes] = {}
    extra_preimages: list[tuple[str, str, bytes, str]] = []
    if stage == "candidate":
        historical = _historical_verification_bytes(
            repo_root,
            tested_head=tested_head,
            implementation_parent=implementation_parent,
        )
        extra_preimages.append(
            (
                "generated/historical-verification.json",
                "historical-verification.json",
                historical,
                "historical",
            )
        )
    else:
        if review_target not in (2, 4, 8):
            raise ValueError(
                "closure preparation requires validated review target 2, 4, or 8"
            )
        historical_path = raw_dir / "detached/historical-verification.json"
        historical = _require_regular_unlinked_file(
            historical_path, label="detached historical verification"
        )
        _validate_historical_verification(
            historical,
            tested_head=tested_head,
            implementation_parent=implementation_parent,
        )
        extra_preimages.append(
            (
                "detached/historical-verification.json",
                "historical-verification.json",
                historical,
                "historical",
            )
        )
        for relative in REVIEW_PATHS_BY_TARGET[review_target] + ADJUDICATOR_PATHS:
            payload = _load_canonical_raw_json(
                raw_dir / relative, label="raw review/adjudicator"
            )
            raw = canonical_json_bytes(payload)
            kind = "adjudicator" if relative in ADJUDICATOR_PATHS else "review"
            extra_preimages.append((relative, relative, raw, kind))

    for raw_relative, public_path, raw, kind in extra_preimages:
        transformed, mapping = privacy_transform_bytes(
            raw, kind=kind, privacy_context=context
        )
        if kind == "historical" and transformed != raw:
            raise ValueError(
                "historical reproduced source must already be detached public form"
            )
        extras[public_path] = transformed
        mappings.append(
            _mapping_record(
                raw_relative_path=raw_relative,
                public_path=public_path,
                raw=raw,
                public=transformed,
                mapping=mapping,
            )
        )
    mappings.sort(key=lambda item: str(item["public_path"]))
    if len({str(item["public_path"]) for item in mappings}) != len(mappings):
        raise ValueError("Wave 0 privacy map contains a duplicate public path")
    extended_privacy = canonical_json_bytes(
        {
            "schema_version": "remediation-privacy-transform-v1",
            "records": mappings,
        }
    )
    assert_no_literal_absolute_path(extended_privacy, privacy_context=context)
    base["privacy-transform.json"] = extended_privacy
    public = {**base, **extras}
    expected_paths = (
        set(CANDIDATE_PUBLIC_PATHS) - {"index.json"}
        if stage == "candidate"
        else set(CLOSURE_PUBLIC_PATHS_BY_TARGET[review_target]) - {"index.json"}
    )
    if set(public) != expected_paths:
        raise ValueError("prepared public path set differs from exact branch contract")
    final_index = _finalize_evidence_index(provisional_index, public)
    index_bytes = canonical_json_bytes(final_index)
    assert_no_literal_absolute_path(index_bytes)
    complete = {**public, "index.json": index_bytes}
    bundle = PreparedEvidenceBundle(
        PurePosixPath(expected_output),
        tuple(
            PreparedEvidenceFile(PurePosixPath(path), data)
            for path, data in sorted(complete.items())
        ),
    )
    _validate_detached_bundle(bundle, repo_root=repo_root)
    validate_evidence_index(final_index, repo_root=repo_root, actual_head=tested_head)
    return bundle


def prepare_evidence_bundle(
    *,
    repo_root: Path | str,
    wave: str,
    evidence_stage: str,
    tested_git_head: str,
    implementation_parent_git_head: str,
    raw_dir: Path | str,
    output_dir: Path | str,
) -> PreparedEvidenceBundle:
    root = Path(repo_root).resolve(strict=True)
    if wave != "wave-0":
        raise ValueError("Wave 0 wrapper only accepts wave='wave-0'")
    actual_head = _git_head(root)
    _validate_head_relationship(
        repo_root=root,
        wave=wave,
        evidence_stage=evidence_stage,
        tested_git_head=tested_git_head,
        implementation_parent_git_head=implementation_parent_git_head,
        actual_head=actual_head,
    )
    raw = Path(raw_dir)
    if not raw.is_absolute():
        raw = root / raw
    raw = raw.resolve(strict=True)
    expected_raw = (
        root / f".verification/raw/wave-0/{tested_git_head[:12]}/{evidence_stage}"
    )
    if raw != expected_raw.resolve(strict=True):
        raise ValueError(
            "raw directory does not match exact Wave 0 stage/head contract"
        )
    output_text = Path(output_dir).as_posix()
    expected_output = (
        f"docs/verification/evidence/wave-0/{tested_git_head[:12]}"
        if evidence_stage == "candidate"
        else f"verification-evidence/wave-0/{tested_git_head[:12]}"
    )
    if output_text != expected_output:
        raise ValueError(
            "output directory does not match exact Wave 0 stage/head contract"
        )
    output = root / expected_output
    if output.exists() or output.is_symlink():
        raise FileExistsError("Wave 0 public evidence destination already exists")
    policy = resolve_tested_input_policy(root)
    _source_config_bindings(policy)
    _reviewed_plan_binding(root, tested_git_head, implementation_parent_git_head)
    _snapshot_binding(root)
    review_target = None
    if evidence_stage == "candidate":
        reviews = raw / "reviews"
        if reviews.exists() and any(reviews.rglob("*.json")):
            raise ValueError("candidate preparation forbids review input")
    else:
        review_target = validate_reviews(
            repo_root=root,
            tested_head=tested_git_head,
            implementation_parent=implementation_parent_git_head,
            raw_dir=raw,
        )
    return _prepare_wave0_virtual_bundle(
        repo_root=root,
        raw_dir=raw,
        tested_head=tested_git_head,
        implementation_parent=implementation_parent_git_head,
        stage=evidence_stage,
        expected_output=expected_output,
        review_target=review_target,
        require_output_absent=True,
    )


def _review_context_path_record(
    root: Path, path: Path, *, base: Path
) -> dict[str, object]:
    data = _require_regular_unlinked_file(path, label="review context member")
    return _file_record(path.relative_to(base).as_posix(), data)


def _candidate_index(
    repo_root: Path, implementation_parent: str
) -> tuple[dict[str, object], Path]:
    candidate_dir = (
        repo_root / f"docs/verification/evidence/wave-0/{implementation_parent[:12]}"
    )
    index_path = candidate_dir / "index.json"
    data = _require_regular_unlinked_file(index_path, label="candidate evidence index")
    payload = json.loads(data)
    if canonical_json_bytes(payload) != data:
        raise ValueError("candidate evidence index is not canonical JSON")
    validate_evidence_index(
        payload, repo_root=repo_root, actual_head=implementation_parent
    )
    return payload, candidate_dir


def _write_detached_historical(
    repo_root: Path,
    raw_dir: Path,
    *,
    tested_head: str,
    implementation_parent: str,
    create_if_absent: bool,
) -> tuple[bytes, Path]:
    detached = raw_dir / "detached/historical-verification.json"
    expected = _historical_verification_bytes(
        repo_root,
        tested_head=tested_head,
        implementation_parent=implementation_parent,
    )
    if detached.exists():
        actual = _require_regular_unlinked_file(
            detached, label="detached historical verification"
        )
        if actual != expected:
            raise ValueError("existing detached historical verification bytes drifted")
        return actual, detached
    if not create_if_absent:
        raise ValueError("detached historical verification is missing")
    detached.parent.mkdir(parents=True, exist_ok=True)
    detached.write_bytes(expected)
    if detached.read_bytes() != expected:
        raise OSError("detached historical verification re-read mismatch")
    return expected, detached


def build_review_context(
    *,
    repo_root: Path | str,
    tested_head: str,
    implementation_parent: str,
    raw_dir: Path | str,
    write: bool,
) -> tuple[dict[str, object], bytes, str]:
    root = Path(repo_root).resolve(strict=True)
    raw = Path(raw_dir)
    if not raw.is_absolute():
        raw = root / raw
    raw = raw.resolve(strict=True)
    _validate_head_relationship(
        repo_root=root,
        wave="wave-0",
        evidence_stage="closure",
        tested_git_head=tested_head,
        implementation_parent_git_head=implementation_parent,
        actual_head=_git_head(root),
    )
    candidate_index, candidate_dir = _candidate_index(root, implementation_parent)
    command_inventory: list[dict[str, object]] = []
    junit_inventory: list[dict[str, object]] = []
    for suite in ("full", "subsystem", "targeted"):
        _validate_raw_command_and_junit(root, raw, suite)
        command_inventory.append(
            _review_context_path_record(root, raw / f"{suite}.command.json", base=raw)
        )
        junit_inventory.append(
            _review_context_path_record(root, raw / f"{suite}.raw.xml", base=raw)
        )
    policy = resolve_tested_input_policy(root)
    source_bindings = _source_config_bindings(policy)
    environment = capture_environment_record(
        root, dependency_input_paths=DEPENDENCY_INPUT_PATHS
    )
    environment_bytes = canonical_json_bytes(environment)
    plan = _reviewed_plan_binding(root, tested_head, implementation_parent)
    snapshot_binding, snapshot_context = _snapshot_binding(root)
    historical_data, historical_path = _write_detached_historical(
        root,
        raw,
        tested_head=tested_head,
        implementation_parent=implementation_parent,
        create_if_absent=write,
    )
    _validate_historical_verification(
        historical_data,
        tested_head=tested_head,
        implementation_parent=implementation_parent,
    )
    historical_source_inventory, _ = _historical_observations(root)
    diff_paths = str(
        _git(root, "diff", "--name-only", f"{implementation_parent}..{tested_head}")
    ).splitlines()
    allowed_prefix = f"docs/verification/evidence/wave-0/{implementation_parent[:12]}/"
    if not diff_paths or any(
        not path.startswith(allowed_prefix) for path in diff_paths
    ):
        raise ValueError(
            "review context evidence diff is not the exact candidate directory"
        )
    diff_inventory = [
        _file_record(
            path,
            _require_regular_unlinked_file(root / path, label="candidate diff byte"),
        )
        for path in sorted(diff_paths)
    ]
    candidate_inventory = [
        _file_record(
            f"docs/verification/evidence/wave-0/{implementation_parent[:12]}/{item['path']}",
            _require_regular_unlinked_file(
                candidate_dir / str(item["path"]), label="candidate evidence byte"
            ),
        )
        for item in _inventory_tree(candidate_dir)
    ]
    if not any(
        str(item["path"]).endswith("/index.json") for item in candidate_inventory
    ):
        raise ValueError("candidate evidence inventory lacks index.json")
    claim_contract = {
        "claim_specs": [
            {**item, "evidence_ids": list(item["evidence_ids"])} for item in CLAIM_SPECS
        ],
        "criteria": {
            domain: [list(pair) for pair in pairs]
            for domain, pairs in CLAIM_CRITERIA_BY_DOMAIN.items()
        },
    }
    path_contract = {
        "candidate": list(CANDIDATE_PUBLIC_PATHS),
        "closure": {
            str(target): list(paths)
            for target, paths in CLOSURE_PUBLIC_PATHS_BY_TARGET.items()
        },
    }
    payload = {
        "schema_version": "wave-0-review-context-v1",
        "tested_git_head": tested_head,
        "implementation_parent_git_head": implementation_parent,
        "evidence_diff_inventory": diff_inventory,
        "candidate_evidence_inventory": candidate_inventory,
        "raw_command_inventory": command_inventory,
        "raw_junit_inventory": junit_inventory,
        "tested_input_inventory": policy["inputs"],
        "source_config_inventory": source_bindings,
        "dependency_inventory": environment["dependency_inputs"],
        "environment_inventory": [
            _file_record("generated/environment.json", environment_bytes)
        ],
        "reviewed_plan_bytes": plan,
        "verification_snapshot_bytes": snapshot_context,
        "historical_source_bytes": {
            **_file_record(
                str(HISTORICAL_INVENTORY_PATH),
                _require_regular_unlinked_file(
                    root / HISTORICAL_INVENTORY_PATH, label="historical inventory"
                ),
            ),
            "source_inventory": historical_source_inventory,
        },
        "historical_reproduced_source": _file_record(
            historical_path.relative_to(raw).as_posix(), historical_data
        ),
        "claim_specs": {"sha256": _sha256(canonical_json_bytes(claim_contract))},
        "public_path_contracts": {
            "sha256": _sha256(canonical_json_bytes(path_contract))
        },
    }
    if tuple(payload) != REVIEW_CONTEXT_FIELDS:
        raise ValueError("review context field order drifted")
    data = canonical_json_bytes(payload)
    digest = _sha256(data)
    destination = raw / "review-context.json"
    if write:
        if destination.exists():
            existing = _require_regular_unlinked_file(
                destination, label="review context"
            )
            if existing != data:
                raise ValueError(
                    "existing review context differs from current exact inputs"
                )
        else:
            destination.write_bytes(data)
            if destination.read_bytes() != data:
                raise OSError("review context re-read mismatch")
    return payload, data, digest


def _validate_reviewed_paths(
    reviewed_paths: object,
    *,
    repo_root: Path,
    raw_dir: Path,
    historical_record: Mapping[str, object],
) -> None:
    if not isinstance(reviewed_paths, list) or not reviewed_paths:
        raise ValueError("reviewed_paths must be a nonempty inventory")
    paths = []
    for item in reviewed_paths:
        if not isinstance(item, dict) or set(item) != {"path", "size_bytes", "sha256"}:
            raise ValueError("reviewed_paths record fields mismatch")
        path = item["path"]
        if (
            not isinstance(path, str)
            or "\\" in path
            or ".." in PurePosixPath(path).parts
        ):
            raise ValueError("reviewed path must be canonical repository-relative")
        if path == historical_record["path"]:
            source = raw_dir / path
        else:
            source = repo_root / path
        data = _require_regular_unlinked_file(source, label="reviewed path")
        if len(data) != item["size_bytes"] or _sha256(data) != item["sha256"]:
            raise ValueError(f"reviewed path binding mismatch: {path}")
        paths.append(path)
    if paths != sorted(paths) or len({path.casefold() for path in paths}) != len(paths):
        raise ValueError("reviewed_paths must be sorted and case-distinct")
    if historical_record["path"] not in paths:
        raise ValueError("review must include detached historical reproduced source")


def _validate_criteria(criteria: object, *, domain: str) -> dict[str, int]:
    if not isinstance(criteria, dict):
        raise ValueError("review criteria must be an object")
    expected = {key for key, _ in CLAIM_CRITERIA_BY_DOMAIN[domain]}
    if set(criteria) != expected:
        raise ValueError("review criterion keys differ from exact claim domain")
    result: dict[str, int] = {}
    for key, value in criteria.items():
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or not 0 <= value <= 20
        ):
            raise ValueError("review criterion scores must be integers in [0,20]")
        result[key] = value
    return result


def _validate_trigger_list(value: object) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError("escalation_triggers must be a string array")
    triggers = tuple(value)
    if list(triggers) != sorted(triggers) or len(set(triggers)) != len(triggers):
        raise ValueError("escalation triggers must be sorted and unique")
    unknown = set(triggers) - set(ALLOWED_ESCALATION_TRIGGERS)
    if unknown:
        raise ValueError(f"unknown escalation trigger: {sorted(unknown)[0]}")
    return triggers


def _validate_review(
    payload: object,
    *,
    relative_path: str,
    repo_root: Path,
    raw_dir: Path,
    tested_head: str,
    implementation_parent: str,
    context_digest: str,
    historical_record: Mapping[str, object],
    eligible_claim_ids: set[str],
) -> dict[str, object]:
    if not isinstance(payload, dict):
        raise ValueError("review record must be an object")
    _require_closed_fields(payload, REVIEW_FIELDS, label="review")
    if payload["schema_version"] != "wave-0-review-v1":
        raise ValueError("review schema_version mismatch")
    view_id = Path(relative_path).stem
    if payload["view_id"] != view_id:
        raise ValueError("review view_id/result path mismatch")
    if payload["calibration_kind"] != "independent_pairwise_source_reading_v1":
        raise ValueError("review calibration kind mismatch")
    if (
        payload["tested_git_head"] != tested_head
        or payload["implementation_parent_git_head"] != implementation_parent
    ):
        raise ValueError("review head binding mismatch")
    if payload["reviewed_input_inventory_sha256"] != context_digest:
        raise ValueError("review context digest mismatch")
    if payload["result_location"] != relative_path:
        raise ValueError("review result_location mismatch")
    _validate_reviewed_paths(
        payload["reviewed_paths"],
        repo_root=repo_root,
        raw_dir=raw_dir,
        historical_record=historical_record,
    )
    claim_scores = payload["claim_scores"]
    if not isinstance(claim_scores, list) or not claim_scores:
        raise ValueError("review claim_scores must be nonempty")
    initial = view_id in INITIAL_VIEW_IDS
    if initial and len(claim_scores) != len(CLAIM_SPECS):
        raise ValueError("initial review must score both Wave 0 claims")
    observed_claims: set[str] = set()
    claim_verdicts: list[str] = []
    aggregate_triggers: set[str] = set()
    obligations: list[str] = []
    unresolved = False
    for score in claim_scores:
        if not isinstance(score, dict):
            raise ValueError("review claim score must be an object")
        expected_fields = INITIAL_CLAIM_SCORE_FIELDS if initial else CLAIM_SCORE_FIELDS
        _require_closed_fields(score, expected_fields, label="review claim score")
        claim_id = score["claim_id"]
        if not isinstance(claim_id, str) or claim_id not in eligible_claim_ids:
            raise ValueError("review scores an ineligible claim")
        if claim_id in observed_claims:
            raise ValueError("review contains duplicate claim score")
        observed_claims.add(claim_id)
        spec = _claim_spec(claim_id)
        if score["domain"] != spec["domain"] or score["severity"] != spec["severity"]:
            raise ValueError("review claim domain/severity mismatch")
        if score["evidence_ids"] != list(spec["evidence_ids"]):
            raise ValueError("review eligible evidence IDs mismatch")
        criteria = _validate_criteria(score["criteria"], domain=str(spec["domain"]))
        verdict = score["verdict"]
        if verdict not in ("support", "conflict", "abstain"):
            raise ValueError("review verdict must be support, conflict, or abstain")
        claim_verdicts.append(verdict)
        triggers = _validate_trigger_list(score["escalation_triggers"])
        aggregate_triggers.update(triggers)
        if not isinstance(score["unresolved_disagreement"], bool):
            raise ValueError("review unresolved_disagreement must be Boolean")
        unresolved = unresolved or score["unresolved_disagreement"]
        if (
            score["unresolved_disagreement"]
            and "criterion_disagreement" not in triggers
        ):
            raise ValueError("unresolved review disagreement lacks retained trigger")
        if not isinstance(score["open_obligations"], list) or not all(
            isinstance(item, str) and item for item in score["open_obligations"]
        ):
            raise ValueError("review open_obligations must be nonempty strings")
        obligations.extend(score["open_obligations"])
        if initial:
            if score["candidate_ids"] != ["claim-statement", "explicit-negation"]:
                raise ValueError("review candidate IDs mismatch")
            descriptions = score["candidate_descriptions"]
            if not isinstance(descriptions, list) or [
                item.get("id") for item in descriptions
            ] != ["claim-statement", "explicit-negation"]:
                raise ValueError("review candidate descriptions mismatch")
            if any(
                not isinstance(item.get("description"), str) or not item["description"]
                for item in descriptions
            ):
                raise ValueError("review candidate descriptions must be nonempty")
            expected_order = "AB" if view_id == INITIAL_VIEW_IDS[0] else "BA"
            if score["comparison_order"] != expected_order:
                raise ValueError("initial review comparison order mismatch")
            if score["comparison_outcome"] not in (
                "left",
                "right",
                "tie",
                "inconclusive",
            ):
                raise ValueError("review comparison outcome is invalid")
            if score["comparison_criteria"] != criteria:
                raise ValueError("review comparison criteria must equal view criteria")
    if initial and observed_claims != {str(item["id"]) for item in CLAIM_SPECS}:
        raise ValueError("initial review claim set mismatch")
    expected_verdict = (
        "support"
        if all(item == "support" for item in claim_verdicts)
        else (
            "conflict"
            if any(item == "conflict" for item in claim_verdicts)
            else "abstain"
        )
    )
    if payload["verdict"] != expected_verdict:
        raise ValueError("review aggregate verdict mismatch")
    if payload["escalation_triggers"] != sorted(aggregate_triggers):
        raise ValueError("review aggregate escalation triggers mismatch")
    if payload["unresolved_disagreement"] is not unresolved:
        raise ValueError("review aggregate disagreement mismatch")
    if payload["open_obligations"] != obligations:
        raise ValueError("review aggregate obligations mismatch")
    if not isinstance(payload["falsification_conditions"], list) or not all(
        isinstance(item, str) and item for item in payload["falsification_conditions"]
    ):
        raise ValueError("review falsification_conditions must be nonempty strings")
    return payload


def _load_context(
    repo_root: Path,
    raw_dir: Path,
    *,
    tested_head: str,
    implementation_parent: str,
) -> tuple[dict[str, object], str]:
    context_path = raw_dir / "review-context.json"
    existing = _require_regular_unlinked_file(context_path, label="review context")
    payload, expected, digest = build_review_context(
        repo_root=repo_root,
        tested_head=tested_head,
        implementation_parent=implementation_parent,
        raw_dir=raw_dir,
        write=False,
    )
    if existing != expected:
        raise ValueError("review context no longer matches exact inputs")
    return payload, digest


def _load_canonical_raw_json(path: Path, *, label: str) -> dict[str, object]:
    return _canonical_json_object(
        _require_regular_unlinked_file(path, label=label), label=label
    )


def _review_state(
    *,
    repo_root: Path,
    raw_dir: Path,
    tested_head: str,
    implementation_parent: str,
    require_adjudicators: bool,
) -> tuple[
    int, dict[str, dict[str, object]], dict[str, int], dict[str, dict[str, object]]
]:
    context, digest = _load_context(
        repo_root,
        raw_dir,
        tested_head=tested_head,
        implementation_parent=implementation_parent,
    )
    historical_record = context["historical_reproduced_source"]
    assert isinstance(historical_record, dict)
    existing_review_paths = (
        {
            path.relative_to(raw_dir).as_posix()
            for path in (raw_dir / "reviews").rglob("*.json")
            if "adjudicators" not in path.parts
        }
        if (raw_dir / "reviews").exists()
        else set()
    )
    allowed_all = set(REVIEW_PATHS_BY_TARGET[8])
    unknown = existing_review_paths - allowed_all
    if unknown:
        raise ValueError(f"unselected review path: {sorted(unknown)[0]}")
    if not set(INITIAL_REVIEW_PATHS).issubset(existing_review_paths):
        raise ValueError("both initial review records are required")
    reviews: dict[str, dict[str, object]] = {}
    initial_claim_triggers: dict[str, set[str]] = {
        str(spec["id"]): set() for spec in CLAIM_SPECS
    }
    for relative in INITIAL_REVIEW_PATHS:
        review = _validate_review(
            _load_canonical_raw_json(raw_dir / relative, label="initial review"),
            relative_path=relative,
            repo_root=repo_root,
            raw_dir=raw_dir,
            tested_head=tested_head,
            implementation_parent=implementation_parent,
            context_digest=digest,
            historical_record=historical_record,
            eligible_claim_ids={str(item["id"]) for item in CLAIM_SPECS},
        )
        reviews[Path(relative).stem] = review
        for score in review["claim_scores"]:
            initial_claim_triggers[str(score["claim_id"])].update(
                score["escalation_triggers"]
            )
    claims_requiring_four = {
        claim_id for claim_id, triggers in initial_claim_triggers.items() if triggers
    }
    global_target = 4 if claims_requiring_four else 2
    additional4_present = set(TARGET4_ADDITIONAL_REVIEW_PATHS) & existing_review_paths
    if additional4_present and additional4_present != set(
        TARGET4_ADDITIONAL_REVIEW_PATHS
    ):
        raise ValueError("partial target-4 review tier is forbidden")
    claims_requiring_eight: set[str] = set()
    if claims_requiring_four and additional4_present:
        for relative in TARGET4_ADDITIONAL_REVIEW_PATHS:
            review = _validate_review(
                _load_canonical_raw_json(
                    raw_dir / relative, label="target-4 review"
                ),
                relative_path=relative,
                repo_root=repo_root,
                raw_dir=raw_dir,
                tested_head=tested_head,
                implementation_parent=implementation_parent,
                context_digest=digest,
                historical_record=historical_record,
                eligible_claim_ids=claims_requiring_four,
            )
            reviews[Path(relative).stem] = review
            for score in review["claim_scores"]:
                claim_id = str(score["claim_id"])
                if (
                    score["unresolved_disagreement"]
                    and "criterion_disagreement" in score["escalation_triggers"]
                ):
                    claims_requiring_eight.add(claim_id)
        global_target = 8 if claims_requiring_eight else 4
    elif claims_requiring_four and require_adjudicators:
        raise ValueError("complete target-4 review tier is required")
    additional8_present = set(TARGET8_ADDITIONAL_REVIEW_PATHS) & existing_review_paths
    if additional8_present and additional8_present != set(
        TARGET8_ADDITIONAL_REVIEW_PATHS
    ):
        raise ValueError("partial target-8 review tier is forbidden")
    if claims_requiring_eight and additional8_present:
        for relative in TARGET8_ADDITIONAL_REVIEW_PATHS:
            review = _validate_review(
                _load_canonical_raw_json(
                    raw_dir / relative, label="target-8 review"
                ),
                relative_path=relative,
                repo_root=repo_root,
                raw_dir=raw_dir,
                tested_head=tested_head,
                implementation_parent=implementation_parent,
                context_digest=digest,
                historical_record=historical_record,
                eligible_claim_ids=claims_requiring_eight,
            )
            reviews[Path(relative).stem] = review
        global_target = 8
    elif claims_requiring_eight and require_adjudicators:
        raise ValueError("complete target-8 review tier is required")
    allowed_for_target = set(REVIEW_PATHS_BY_TARGET[global_target])
    if require_adjudicators and existing_review_paths != allowed_for_target:
        raise ValueError("review path set differs from selected 2/4/8 tier")
    claim_targets = {
        claim_id: (
            8
            if claim_id in claims_requiring_eight
            else 4
            if claim_id in claims_requiring_four
            else 2
        )
        for claim_id in initial_claim_triggers
    }
    adjudicators: dict[str, dict[str, object]] = {}
    if require_adjudicators:
        expected_adjudicator_paths = set(ADJUDICATOR_PATHS)
        actual_adjudicator_paths = (
            {
                path.relative_to(raw_dir).as_posix()
                for path in (raw_dir / "reviews/adjudicators").glob("*.json")
            }
            if (raw_dir / "reviews/adjudicators").exists()
            else set()
        )
        if actual_adjudicator_paths != expected_adjudicator_paths:
            raise ValueError("adjudicator path set mismatch")
        for relative in ADJUDICATOR_PATHS:
            payload = _load_canonical_raw_json(
                raw_dir / relative, label="adjudicator"
            )
            if not isinstance(payload, dict):
                raise ValueError("adjudicator must be an object")
            _require_closed_fields(payload, ADJUDICATOR_FIELDS, label="adjudicator")
            claim_id = str(payload["claim_id"])
            spec = _claim_spec(claim_id)
            target = claim_targets[claim_id]
            if (
                payload["schema_version"] != "wave-0-adjudicator-v1"
                or payload["role"] != "verifier-adjudicator"
            ):
                raise ValueError("adjudicator schema/role mismatch")
            if (
                payload["tested_git_head"] != tested_head
                or payload["implementation_parent_git_head"] != implementation_parent
            ):
                raise ValueError("adjudicator head binding mismatch")
            if payload["reviewed_input_inventory_sha256"] != digest:
                raise ValueError("adjudicator context digest mismatch")
            if payload["escalation_target"] != target or payload["view_ids"] != list(
                VIEW_IDS_BY_TARGET[target]
            ):
                raise ValueError("adjudicator target/view binding mismatch")
            expected_triggers = sorted(
                {
                    trigger
                    for view_id in VIEW_IDS_BY_TARGET[target]
                    for score in reviews[view_id]["claim_scores"]
                    if score["claim_id"] == claim_id
                    for trigger in score["escalation_triggers"]
                }
            )
            observed_triggers = list(
                _validate_trigger_list(payload["escalation_triggers"])
            )
            if observed_triggers != expected_triggers:
                raise ValueError(
                    "adjudicator escalation triggers differ from selected reviews"
                )
            if (
                payload["evidence_ids"] != list(spec["evidence_ids"])
                or "index.json" in payload["evidence_ids"]
            ):
                raise ValueError("adjudicator evidence IDs mismatch")
            expected_path = next(
                path for path in ADJUDICATOR_PATHS if Path(path).stem == claim_id
            )
            if relative != expected_path or payload["result_location"] != relative:
                raise ValueError("adjudicator result location mismatch")
            if payload["result"] not in ("support", "abstain"):
                raise ValueError("adjudicator result must be support or abstain")
            if not isinstance(payload["open_obligations"], list) or not all(
                isinstance(item, str) and item for item in payload["open_obligations"]
            ):
                raise ValueError("adjudicator obligations must be nonempty strings")
            if payload["result"] == "support" and payload["open_obligations"]:
                raise ValueError("supporting adjudicator must have no open obligations")
            if payload["result"] == "abstain" and not payload["open_obligations"]:
                raise ValueError("abstaining adjudicator requires an open obligation")
            if (
                not isinstance(payload["reason"], str)
                or not payload["reason"]
                or not isinstance(payload["falsification_condition"], str)
                or not payload["falsification_condition"]
            ):
                raise ValueError(
                    "adjudicator reason/falsification condition must be nonempty"
                )
            adjudicators[claim_id] = payload
    return global_target, reviews, claim_targets, adjudicators


def review_target(
    *,
    repo_root: Path | str,
    tested_head: str,
    implementation_parent: str,
    raw_dir: Path | str,
) -> int:
    root = Path(repo_root).resolve(strict=True)
    raw = Path(raw_dir)
    if not raw.is_absolute():
        raw = root / raw
    target, _reviews, _claim_targets, _adjudicators = _review_state(
        repo_root=root,
        raw_dir=raw.resolve(strict=True),
        tested_head=tested_head,
        implementation_parent=implementation_parent,
        require_adjudicators=False,
    )
    return target


def validate_reviews(
    *,
    repo_root: Path | str,
    tested_head: str,
    implementation_parent: str,
    raw_dir: Path | str,
) -> int:
    root = Path(repo_root).resolve(strict=True)
    raw = Path(raw_dir)
    if not raw.is_absolute():
        raw = root / raw
    target, reviews, claim_targets, adjudicators = _review_state(
        repo_root=root,
        raw_dir=raw.resolve(strict=True),
        tested_head=tested_head,
        implementation_parent=implementation_parent,
        require_adjudicators=True,
    )
    for claim_id, claim_target in claim_targets.items():
        view_ids = VIEW_IDS_BY_TARGET[claim_target]
        scores = []
        verdicts = []
        for view_id in view_ids:
            review = reviews[view_id]
            matching = [
                item for item in review["claim_scores"] if item["claim_id"] == claim_id
            ]
            if len(matching) != 1:
                raise ValueError(
                    "each claim target requires exactly one score from each selected view"
                )
            score = matching[0]
            scores.append(score["criteria"])
            verdicts.append(score["verdict"])
        spec = _claim_spec(claim_id)
        keys = tuple(key for key, _ in CLAIM_CRITERIA_BY_DOMAIN[str(spec["domain"])])
        compute_criterion_aggregates(scores, criterion_keys=keys)
        adjudicator = adjudicators[claim_id]
        if (
            all(verdict == "support" for verdict in verdicts)
            and adjudicator["result"] != "support"
        ):
            raise ValueError(
                "supporting views require supporting adjudication when evidence is complete"
            )
        if (
            any(verdict != "support" for verdict in verdicts)
            and adjudicator["result"] != "abstain"
        ):
            raise ValueError(
                "recorded review conflict requires abstaining adjudication"
            )
    return target


def _public_review_records(
    closure_dir: Path, target: int
) -> tuple[dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    reviews = {
        Path(relative).stem: json.loads(
            _require_regular_unlinked_file(
                closure_dir / relative, label="public review"
            )
        )
        for relative in REVIEW_PATHS_BY_TARGET[target]
    }
    adjudicators = {
        Path(relative).stem: json.loads(
            _require_regular_unlinked_file(
                closure_dir / relative, label="public adjudicator"
            )
        )
        for relative in ADJUDICATOR_PATHS
    }
    return reviews, adjudicators


def _validate_active_gate_binding(
    *,
    root: Path,
    ledger: Path,
    ledger_payload: Mapping[str, object],
) -> str:
    marker_path = root / ".verification/active.json"
    marker_bytes = _require_regular_unlinked_file(
        marker_path, label="verification activation marker"
    )
    marker = json.loads(marker_bytes)
    if not isinstance(marker, dict) or set(marker) != {"ledger", "artifact_revision"}:
        raise ValueError("activation marker fields mismatch")
    expected_reference = ".verification/wave-0/final-ledger.json"
    if marker["ledger"] != expected_reference:
        raise ValueError("activation marker ledger path mismatch")
    artifact_revision = ledger_payload["artifact_revision"]
    if marker["artifact_revision"] != artifact_revision:
        raise ValueError("activation marker artifact revision mismatch")
    verified_gate = resolve_verified_verification_gate(
        root / SNAPSHOT_PATH,
        root=Path.home() / ".codex/skills/verification",
    )
    try:
        live_revision = capture_verified_artifact_revision(
            verified_gate,
            cwd=root,
            excluded_paths=frozenset({ledger}),
        )
    except (OSError, ValueError) as error:
        raise ValueError(f"cannot capture live artifact revision: {error}") from error
    if live_revision != artifact_revision:
        raise ValueError("live artifact changed after verification activation")
    return str(artifact_revision)


def _validate_ledger_projection(
    ledger_payload: Mapping[str, object],
    reviews: Mapping[str, Mapping[str, object]],
) -> None:
    claims = ledger_payload.get("claims")
    if not isinstance(claims, list):
        raise ValueError("projected ledger claims must be an array")
    by_id = {str(claim.get("id")): claim for claim in claims if isinstance(claim, dict)}
    if set(by_id) != {str(spec["id"]) for spec in CLAIM_SPECS}:
        raise ValueError("projected ledger claim set mismatch")
    for spec in CLAIM_SPECS:
        claim_id = str(spec["id"])
        claim = by_id[claim_id]
        available = [
            reviews[view_id]
            for view_id in VIEW_IDS_BY_TARGET[8]
            if view_id in reviews
            and any(
                score["claim_id"] == claim_id
                for score in reviews[view_id]["claim_scores"]
            )
        ]
        target = len(available)
        if target not in (2, 4, 8):
            raise ValueError("projected ledger claim lacks a complete review tier")
        score_records = [
            next(
                score
                for score in review["claim_scores"]
                if score["claim_id"] == claim_id
            )
            for review in available
        ]
        criterion_keys = tuple(
            key for key, _label in CLAIM_CRITERIA_BY_DOMAIN[str(spec["domain"])]
        )
        aggregate = compute_criterion_aggregates(
            [score["criteria"] for score in score_records],
            criterion_keys=criterion_keys,
        )
        expected_criteria = [
            {"name": key, "score": aggregate[key]} for key in criterion_keys
        ]
        if claim.get("criteria") != expected_criteria:
            raise ValueError("projected ledger criterion aggregate mismatch")
        if claim.get("escalation_target") != target:
            raise ValueError("projected ledger escalation target mismatch")
        views = claim.get("views")
        if not isinstance(views, dict):
            raise ValueError("projected ledger views must be an object")
        expected_scores = [
            {
                "view_id": review["view_id"],
                "criteria": [
                    {"name": key, "score": score["criteria"][key]}
                    for key in criterion_keys
                ],
            }
            for review, score in zip(available, score_records, strict=True)
        ]
        if views.get("scores") != expected_scores:
            raise ValueError("projected ledger view-score projection mismatch")


def populate_ledger(
    *,
    repo_root: Path | str,
    ledger_path: Path | str,
    closure_index_path: Path | str,
) -> None:
    root = Path(repo_root).resolve(strict=True)
    ledger = Path(ledger_path)
    if not ledger.is_absolute():
        ledger = root / ledger
    expected_ledger = root / ".verification/wave-0/final-ledger.json"
    if ledger.resolve(strict=True) != expected_ledger.resolve(strict=True):
        raise ValueError(
            "ledger path must be exactly .verification/wave-0/final-ledger.json"
        )
    ledger_bytes = _require_regular_unlinked_file(ledger, label="gate-created ledger")
    ledger_payload = json.loads(ledger_bytes)
    if not isinstance(ledger_payload, dict) or set(ledger_payload) != {
        "schema_version",
        "mode",
        "artifact_revision",
        "claims",
    }:
        raise ValueError("gate ledger template fields mismatch")
    if (
        ledger_payload["schema_version"] != "1.0"
        or ledger_payload["mode"] != "closure"
        or ledger_payload["claims"] != []
    ):
        raise ValueError(
            "populate-ledger requires the empty closure template from gate start"
        )
    artifact_revision = ledger_payload["artifact_revision"]
    if (
        not isinstance(artifact_revision, str)
        or not artifact_revision.strip()
        or "placeholder" in artifact_revision.casefold()
    ):
        raise ValueError("gate artifact revision is not concrete")
    artifact_revision = _validate_active_gate_binding(
        root=root,
        ledger=ledger,
        ledger_payload=ledger_payload,
    )
    index_path = Path(closure_index_path)
    if not index_path.is_absolute():
        index_path = root / index_path
    index_bytes = _require_regular_unlinked_file(
        index_path, label="closure evidence index"
    )
    index = json.loads(index_bytes)
    if canonical_json_bytes(index) != index_bytes:
        raise ValueError("closure evidence index is not canonical JSON")
    head = _git_head(root)
    expected_index_path = (
        root / f"verification-evidence/wave-0/{head[:12]}/index.json"
    ).resolve(strict=True)
    if index_path.resolve(strict=True) != expected_index_path:
        raise ValueError("closure index path is not the exact evidence root index")
    validate_evidence_index(index, repo_root=root, actual_head=head)
    if index["evidence_stage"] != "closure" or index["tested_git_head"] != head:
        raise ValueError("populate-ledger requires exact-head closure evidence")
    closure_dir = index_path.parent
    indexed_paths = {str(item["path"]) for item in index["files"]}
    matching_targets = [
        target
        for target, paths in CLOSURE_PUBLIC_PATHS_BY_TARGET.items()
        if indexed_paths | {"index.json"} == set(paths)
    ]
    if len(matching_targets) != 1:
        raise ValueError("closure index does not select exactly one review tier")
    target = matching_targets[0]
    raw_dir = (root / f".verification/raw/wave-0/{head[:12]}/closure").resolve(
        strict=True
    )
    validated_target = validate_reviews(
        repo_root=root,
        tested_head=head,
        implementation_parent=str(index["implementation_parent_git_head"]),
        raw_dir=raw_dir,
    )
    if validated_target != target:
        raise ValueError("validated review target differs from closure path tier")
    reconstructed_bundle = _prepare_wave0_virtual_bundle(
        repo_root=root,
        raw_dir=raw_dir,
        tested_head=head,
        implementation_parent=str(index["implementation_parent_git_head"]),
        stage="closure",
        expected_output=f"verification-evidence/wave-0/{head[:12]}",
        review_target=validated_target,
        require_output_absent=False,
    )
    reconstructed = {str(item.path): item.data for item in reconstructed_bundle.files}
    if set(reconstructed) != indexed_paths | {"index.json"}:
        raise ValueError("reconstructed public evidence path set differs from index")
    for relative, expected_bytes in reconstructed.items():
        observed_bytes = _require_regular_unlinked_file(
            closure_dir / relative, label="reconstructed public evidence"
        )
        if observed_bytes != expected_bytes:
            raise ValueError(f"reconstructed public evidence byte mismatch: {relative}")
    reviews, adjudicators = _public_review_records(closure_dir, target)
    claims = []
    evidence_short = head[:12]
    for spec in CLAIM_SPECS:
        claim_id = str(spec["id"])
        available = [
            reviews[view_id]
            for view_id in VIEW_IDS_BY_TARGET[target]
            if any(
                item["claim_id"] == claim_id
                for item in reviews[view_id]["claim_scores"]
            )
        ]
        claim_target = len(available)
        if claim_target not in (2, 4, 8):
            raise ValueError("public reviews do not form a complete per-claim tier")
        if [review["view_id"] for review in available] != list(
            VIEW_IDS_BY_TARGET[claim_target]
        ):
            raise ValueError("public per-claim view order/target mismatch")
        score_records = [
            next(
                item for item in review["claim_scores"] if item["claim_id"] == claim_id
            )
            for review in available
        ]
        criterion_keys = tuple(
            key for key, _ in CLAIM_CRITERIA_BY_DOMAIN[str(spec["domain"])]
        )
        aggregate = compute_criterion_aggregates(
            [item["criteria"] for item in score_records], criterion_keys=criterion_keys
        )
        triggers = sorted(
            {
                trigger
                for item in score_records
                for trigger in item["escalation_triggers"]
            }
        )
        unresolved = any(item["unresolved_disagreement"] for item in score_records)
        adjudicator = adjudicators[claim_id]
        obligations = list(adjudicator["open_obligations"])
        supported = (
            all(item["verdict"] == "support" for item in score_records)
            and adjudicator["result"] == "support"
            and not obligations
            and not unresolved
        )
        state = "EVIDENCE_VERIFIED" if supported else "INCONCLUSIVE"
        if not supported and not obligations:
            raise ValueError(
                "inconclusive public claim requires a concrete open obligation"
            )
        initial = score_records[:2]
        matches = []
        for review, item in zip(available[:2], initial, strict=True):
            order = item["comparison_order"]
            left, right = (
                ("claim-statement", "explicit-negation")
                if order == "AB"
                else ("explicit-negation", "claim-statement")
            )
            matches.append(
                {
                    "left": left,
                    "right": right,
                    "view_id": review["view_id"],
                    "outcome": item["comparison_outcome"],
                    "criteria": [
                        {"name": key, "score": item["comparison_criteria"][key]}
                        for key in criterion_keys
                    ],
                    "result_location": review["result_location"],
                }
            )
        evidence = []
        for evidence_id in spec["evidence_ids"]:
            kind = str(spec["kind"])
            if evidence_id == "wave0-historical-inventory-source":
                kind = "primary_source"
            location = EVIDENCE_LOCATIONS_BY_ID[str(evidence_id)].format(
                evidence_short=evidence_short
            )
            evidence.append(
                {
                    "id": evidence_id,
                    "kind": kind,
                    "location": location,
                    "artifact_revision": artifact_revision,
                }
            )
        claims.append(
            {
                "id": claim_id,
                "domain": spec["domain"],
                "statement": spec["statement"],
                "severity": spec["severity"],
                "state": state,
                "artifact_revision": artifact_revision,
                "criteria": [
                    {"name": key, "score": aggregate[key]} for key in criterion_keys
                ],
                "escalation_triggers": triggers,
                "escalation_target": claim_target,
                "views": {
                    "calibration_kind": "independent_pairwise_source_reading_v1",
                    "unresolved_disagreement": unresolved,
                    "comparison": {
                        "method": "pairwise",
                        "candidate_count": 2,
                        "candidate_ids": initial[0]["candidate_ids"],
                        "candidate_descriptions": initial[0]["candidate_descriptions"],
                        "pivot_ids": [],
                        "orders": ["AB", "BA"],
                        "matches": matches,
                    },
                    "scores": [
                        {
                            "view_id": review["view_id"],
                            "criteria": [
                                {"name": key, "score": item["criteria"][key]}
                                for key in criterion_keys
                            ],
                        }
                        for review, item in zip(available, score_records, strict=True)
                    ],
                },
                "evidence": evidence,
                "counterevidence": [],
                "verifiers": [
                    {
                        "role": adjudicator["role"],
                        "view_ids": adjudicator["view_ids"],
                        "result": adjudicator["result"],
                        "evidence_ids": adjudicator["evidence_ids"],
                        "result_location": adjudicator["result_location"],
                    }
                ],
                "open_obligations": obligations,
                "evidence_invalidated": False,
            }
        )
    if any(
        str(claim["id"]).startswith("AUD-") or claim["state"] == "REFUTED"
        for claim in claims
    ):
        raise ValueError("Wave 0 ledger must not close AUD claims or use REFUTED")
    populated = {**ledger_payload, "claims": claims}
    _validate_ledger_projection(populated, reviews)
    data = canonical_json_bytes(populated)
    temporary = ledger.with_name(f".{ledger.name}.populate.tmp")
    if temporary.exists():
        raise FileExistsError("ledger population temporary path already exists")
    temporary.write_bytes(data)
    if temporary.read_bytes() != data:
        temporary.unlink(missing_ok=True)
        raise OSError("populated ledger re-read mismatch")
    temporary.replace(ledger)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Wave 0 remediation evidence")
    subparsers = parser.add_subparsers(dest="command", required=True)
    build = subparsers.add_parser("build")
    build.add_argument("--stage", required=True, choices=("candidate", "closure"))
    build.add_argument("--tested-head", required=True)
    build.add_argument("--implementation-parent", required=True)
    build.add_argument("--raw-dir", required=True)
    build.add_argument("--output-dir", required=True)
    context = subparsers.add_parser("review-context-sha")
    context.add_argument("--tested-head", required=True)
    context.add_argument("--implementation-parent", required=True)
    context.add_argument("--raw-dir", required=True)
    target = subparsers.add_parser("review-target")
    target.add_argument("--tested-head", required=True)
    target.add_argument("--implementation-parent", required=True)
    target.add_argument("--raw-dir", required=True)
    reviews = subparsers.add_parser("validate-reviews")
    reviews.add_argument("--tested-head", required=True)
    reviews.add_argument("--implementation-parent", required=True)
    reviews.add_argument("--raw-dir", required=True)
    populate = subparsers.add_parser("populate-ledger")
    populate.add_argument("--ledger", required=True)
    populate.add_argument("--closure-index", required=True)
    return parser


def _main(argv: Sequence[str] | None = None) -> int:
    arguments = create_parser().parse_args(argv)
    root = Path.cwd().resolve(strict=True)
    if arguments.command == "build":
        prepared = prepare_evidence_bundle(
            repo_root=root,
            wave="wave-0",
            evidence_stage=arguments.stage,
            tested_git_head=arguments.tested_head,
            implementation_parent_git_head=arguments.implementation_parent,
            raw_dir=arguments.raw_dir,
            output_dir=arguments.output_dir,
        )
        destination = publish_evidence_bundle(prepared, repo_root=root)
        index = json.loads((destination / "index.json").read_bytes())
        validate_evidence_index(index, repo_root=root, actual_head=_git_head(root))
        return 0
    if arguments.command == "review-context-sha":
        _payload, _bytes, digest = build_review_context(
            repo_root=root,
            tested_head=arguments.tested_head,
            implementation_parent=arguments.implementation_parent,
            raw_dir=arguments.raw_dir,
            write=True,
        )
        print(digest)
        return 0
    if arguments.command == "review-target":
        print(
            review_target(
                repo_root=root,
                tested_head=arguments.tested_head,
                implementation_parent=arguments.implementation_parent,
                raw_dir=arguments.raw_dir,
            )
        )
        return 0
    if arguments.command == "validate-reviews":
        print(
            validate_reviews(
                repo_root=root,
                tested_head=arguments.tested_head,
                implementation_parent=arguments.implementation_parent,
                raw_dir=arguments.raw_dir,
            )
        )
        return 0
    if arguments.command == "populate-ledger":
        populate_ledger(
            repo_root=root,
            ledger_path=arguments.ledger,
            closure_index_path=arguments.closure_index,
        )
        return 0
    raise AssertionError(f"unhandled command: {arguments.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(_main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2) from error
