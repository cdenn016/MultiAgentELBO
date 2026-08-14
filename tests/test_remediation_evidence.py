from __future__ import annotations

import builtins
import copy
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import types
import xml.etree.ElementTree as ET
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import FrozenInstanceError
from hashlib import sha256
from pathlib import Path, PurePosixPath

import pytest

import tools.remediation_evidence as remediation_evidence
import tools.build_wave0_evidence as wave0_evidence

from tools.build_wave0_evidence import (
    ADJUDICATOR_PATHS,
    CANDIDATE_PUBLIC_PATHS,
    CLOSURE_PUBLIC_PATHS_BY_TARGET,
    CLAIM_CRITERIA_BY_DOMAIN,
    CLAIM_SPECS,
    DEPENDENCY_INPUT_PATHS,
    INITIAL_REVIEW_PATHS,
    REVIEW_CONTEXT_FIELDS,
    REVIEW_PATHS_BY_TARGET,
    TARGET4_ADDITIONAL_REVIEW_PATHS,
    TARGET8_ADDITIONAL_REVIEW_PATHS,
    VIEW_IDS_BY_TARGET,
    _public_review_records,
    _suite_argv,
    _validate_ledger_projection,
    build_review_context,
    compute_criterion_aggregates,
    create_parser as wave0_parser,
    populate_ledger,
    prepare_evidence_bundle,
    required_review_target,
    review_target,
    validate_reviews,
)
from tools.remediation_evidence import (
    CPU_PYTHON,
    INDEX_ROOT_FIELDS,
    JUNIT_FIELDS,
    EXPECTED_VERIFICATION_ACTIVE_PATHS,
    SNAPSHOT_PATH,
    PreparedEvidenceBundle,
    PreparedEvidenceFile,
    assert_no_literal_absolute_path,
    assert_public_semantics_equal,
    canonical_json_bytes,
    capture_environment_record,
    create_parser as remediation_parser,
    parse_junit,
    privacy_transform_bytes,
    publish_evidence_bundle,
    resolve_tested_input_policy,
    resolve_verified_verification_gate,
    validate_evidence_index,
    validate_junit_skip_allowlist,
)


TASK4_TRACKED_PATHS = (
    "docs/verification/remediation/verification-contract-v1.json",
    "docs/verification/remediation/remediation-evidence-v1.schema.json",
    "tools/remediation_evidence.py",
    "tools/build_wave0_evidence.py",
    "tests/test_remediation_evidence.py",
    "tests/test_artifacts.py",
    "tests/test_experiment_support.py",
)


EXPECTED_ROOT_FIELDS = {
    "schema_version",
    "wave",
    "evidence_stage",
    "tested_git_head",
    "implementation_parent_git_head",
    "platform",
    "environment_record",
    "dependency_versions",
    "dependency_inputs",
    "tested_input_policy",
    "tested_input_inventory_sha256",
    "commands",
    "source_config_bindings",
    "reviewed_plan_binding",
    "verification_contract_binding",
    "files",
}

EXPECTED_JUNIT_FIELDS = {
    "path",
    "size_bytes",
    "sha256",
    "tests",
    "failures",
    "errors",
    "skipped",
    "time_seconds",
    "testcase_id_sha256",
    "skipped_cases",
}


TEST_VERIFICATION_GATE_SOURCE = textwrap.dedent(
    """\
    from __future__ import annotations

    import argparse
    import hashlib
    import json
    import os
    import subprocess
    from pathlib import Path, PurePosixPath


    def capture_artifact_revision(
        cwd: Path, *, excluded_paths: frozenset[Path] | None = None
    ) -> str:
        root = Path(cwd).resolve(strict=True)
        head = subprocess.check_output(
            ["git", "rev-parse", "--verify", "HEAD"], cwd=root
        ).decode("ascii").strip()
        excluded = {
            Path(path).resolve(strict=False)
            for path in (excluded_paths or frozenset())
        }
        digest = hashlib.sha256(b"test-verification-artifact-v1")
        raw_paths = subprocess.check_output(
            [
                "git",
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "-z",
            ],
            cwd=root,
        )
        for raw_path in sorted(
            item for item in raw_paths.split(bytes([0])) if item
        ):
            relative = PurePosixPath(os.fsdecode(raw_path))
            if not relative.parts or relative.parts[0] in {
                ".git",
                ".verification",
            }:
                continue
            path = root.joinpath(*relative.parts)
            if path.resolve(strict=False) in excluded:
                continue
            digest.update(relative.as_posix().encode("utf-8"))
            digest.update(b"|")
            digest.update(path.read_bytes())
            digest.update(b"|")
        return f"git:{head}:sha256:{digest.hexdigest()}"


    CLAIM_FIELDS = {
        "id", "domain", "statement", "severity", "state", "artifact_revision",
        "criteria", "escalation_triggers", "escalation_target", "views",
        "evidence", "counterevidence", "verifiers", "open_obligations",
        "evidence_invalidated",
    }
    CRITERION_FIELDS = {"name", "score"}
    EVIDENCE_FIELDS = {"id", "kind", "location", "artifact_revision"}
    VERIFIER_FIELDS = {
        "role", "view_ids", "result", "evidence_ids", "result_location",
    }
    VIEW_FIELDS = {
        "calibration_kind", "unresolved_disagreement", "comparison", "scores",
    }
    COMPARISON_FIELDS = {
        "method", "candidate_count", "candidate_ids", "candidate_descriptions",
        "pivot_ids", "orders", "matches",
    }
    CANDIDATE_DESCRIPTION_FIELDS = {"id", "description"}
    MATCH_FIELDS = {
        "left", "right", "view_id", "outcome", "criteria", "result_location",
    }
    SCORE_FIELDS = {"view_id", "criteria"}
    WAVE0_CLAIM_IDS = {
        "CHK-WAVE0-CONTRACT-COMPLETENESS",
        "CHK-WAVE0-HISTORICAL-BYTE-PINS",
    }


    def _string_list(value: object, *, nonempty: bool = False) -> bool:
        return (
            isinstance(value, list)
            and (not nonempty or bool(value))
            and all(isinstance(item, str) and bool(item) for item in value)
        )


    def _valid_criteria(value: object) -> bool:
        if not isinstance(value, list) or not value:
            return False
        names = []
        for item in value:
            if not isinstance(item, dict) or set(item) != CRITERION_FIELDS:
                return False
            name = item["name"]
            score = item["score"]
            if not isinstance(name, str) or not name:
                return False
            if isinstance(score, bool) or not isinstance(score, (int, float)):
                return False
            if not 0 <= score <= 20:
                return False
            names.append(name)
        return len(names) == len(set(names))


    def _valid_evidence(
        value: object, *, artifact_revision: str, nonempty: bool
    ) -> bool:
        if not isinstance(value, list) or (nonempty and not value):
            return False
        for item in value:
            if not isinstance(item, dict) or set(item) != EVIDENCE_FIELDS:
                return False
            if not all(
                isinstance(item[field], str) and bool(item[field])
                for field in ("id", "kind", "location", "artifact_revision")
            ):
                return False
            if item["artifact_revision"] != artifact_revision:
                return False
        return True


    def _valid_views(value: object) -> bool:
        if not isinstance(value, dict) or set(value) != VIEW_FIELDS:
            return False
        if value["calibration_kind"] != "independent_pairwise_source_reading_v1":
            return False
        if not isinstance(value["unresolved_disagreement"], bool):
            return False
        comparison = value["comparison"]
        if not isinstance(comparison, dict) or set(comparison) != COMPARISON_FIELDS:
            return False
        if comparison["method"] != "pairwise":
            return False
        candidate_count = comparison["candidate_count"]
        if isinstance(candidate_count, bool) or candidate_count != 2:
            return False
        candidate_ids = comparison["candidate_ids"]
        descriptions = comparison["candidate_descriptions"]
        if not _string_list(candidate_ids, nonempty=True) or len(candidate_ids) != 2:
            return False
        if not isinstance(descriptions, list) or len(descriptions) != 2:
            return False
        for description in descriptions:
            if (
                not isinstance(description, dict)
                or set(description) != CANDIDATE_DESCRIPTION_FIELDS
                or not all(
                    isinstance(description[field], str) and bool(description[field])
                    for field in CANDIDATE_DESCRIPTION_FIELDS
                )
            ):
                return False
        if [description["id"] for description in descriptions] != candidate_ids:
            return False
        if comparison["pivot_ids"] != [] or comparison["orders"] != ["AB", "BA"]:
            return False
        matches = comparison["matches"]
        if not isinstance(matches, list) or len(matches) != 2:
            return False
        for match in matches:
            if not isinstance(match, dict) or set(match) != MATCH_FIELDS:
                return False
            if not all(
                isinstance(match[field], str) and bool(match[field])
                for field in (
                    "left", "right", "view_id", "outcome", "result_location",
                )
            ) or not _valid_criteria(match["criteria"]):
                return False
        scores = value["scores"]
        if not isinstance(scores, list) or len(scores) not in (2, 4, 8):
            return False
        for score in scores:
            if not isinstance(score, dict) or set(score) != SCORE_FIELDS:
                return False
            if not isinstance(score["view_id"], str) or not score["view_id"]:
                return False
            if not _valid_criteria(score["criteria"]):
                return False
        return True


    def _claim_error(claim: object, *, artifact_revision: str) -> str | None:
        if not isinstance(claim, dict) or set(claim) != CLAIM_FIELDS:
            return "claim fields mismatch"
        for field in ("id", "domain", "statement", "severity", "state"):
            if not isinstance(claim[field], str) or not claim[field]:
                return f"claim {field} must be a nonempty string"
        if claim["domain"] not in {"code", "evidence"}:
            return "claim domain mismatch"
        if claim["severity"] != "medium":
            return "claim severity mismatch"
        if claim["state"] not in {"EVIDENCE_VERIFIED", "INCONCLUSIVE"}:
            return "claim state mismatch"
        if claim["artifact_revision"] != artifact_revision:
            return "claim artifact revision mismatch"
        if not _valid_criteria(claim["criteria"]):
            return "claim criteria mismatch"
        if not _string_list(claim["escalation_triggers"]):
            return "claim escalation triggers mismatch"
        if not set(claim["escalation_triggers"]) <= {
            "criterion_disagreement", "high_dispersion", "small_margin",
        }:
            return "claim escalation trigger value mismatch"
        target = claim["escalation_target"]
        if isinstance(target, bool) or target not in (2, 4, 8):
            return "claim escalation target mismatch"
        if not _valid_views(claim["views"]):
            return "claim views mismatch"
        if len(claim["views"]["scores"]) != target:
            return "claim view count mismatch"
        criterion_names = [item["name"] for item in claim["criteria"]]
        nested_criteria = [
            item["criteria"] for item in claim["views"]["scores"]
        ] + [
            item["criteria"]
            for item in claim["views"]["comparison"]["matches"]
        ]
        if any(
            [item["name"] for item in criteria] != criterion_names
            for criteria in nested_criteria
        ):
            return "claim nested criterion names mismatch"
        if not _valid_evidence(
            claim["evidence"],
            artifact_revision=artifact_revision,
            nonempty=True,
        ):
            return "claim evidence mismatch"
        if claim["counterevidence"] != []:
            return "claim counterevidence mismatch"
        verifiers = claim["verifiers"]
        if not isinstance(verifiers, list) or len(verifiers) != 1:
            return "claim verifiers mismatch"
        verifier = verifiers[0]
        if not isinstance(verifier, dict) or set(verifier) != VERIFIER_FIELDS:
            return "claim verifier fields mismatch"
        if not all(
            isinstance(verifier[field], str) and bool(verifier[field])
            for field in ("role", "result", "result_location")
        ):
            return "claim verifier string mismatch"
        if verifier["result"] not in {"support", "abstain"}:
            return "claim verifier result mismatch"
        if not (
            _string_list(verifier["view_ids"], nonempty=True)
            and _string_list(verifier["evidence_ids"], nonempty=True)
        ):
            return "claim verifier arrays mismatch"
        if verifier["view_ids"] != [
            item["view_id"] for item in claim["views"]["scores"]
        ]:
            return "claim verifier views mismatch"
        if set(verifier["evidence_ids"]) != {
            item["id"] for item in claim["evidence"]
        }:
            return "claim verifier evidence mismatch"
        obligations = claim["open_obligations"]
        if not _string_list(obligations):
            return "claim open obligations mismatch"
        if claim["evidence_invalidated"] is not False:
            return "claim invalidation state mismatch"
        if claim["state"] == "EVIDENCE_VERIFIED" and (
            obligations
            or claim["views"]["unresolved_disagreement"]
            or verifier["result"] != "support"
        ):
            return "verified claim retains an open condition"
        if claim["state"] == "INCONCLUSIVE" and not obligations:
            return "inconclusive claim lacks an open obligation"
        return None


    def main() -> int:
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command", required=True)
        start = subparsers.add_parser("start")
        start.add_argument("--cwd", default=".")
        start.add_argument("--ledger", default=".verification/ledger.json")
        start.add_argument("--mode", choices=("closure", "triage"), default="triage")
        validate = subparsers.add_parser("validate")
        validate.add_argument("ledger")
        validate.add_argument("--cwd", default=".")
        arguments = parser.parse_args()
        root = Path(arguments.cwd).resolve(strict=True)
        ledger = Path(arguments.ledger)
        if not ledger.is_absolute():
            ledger = root / ledger
        marker = root / ".verification/active.json"
        if arguments.command == "start":
            revision = capture_artifact_revision(
                root, excluded_paths=frozenset({ledger})
            )
            ledger.parent.mkdir(parents=True, exist_ok=True)
            marker.parent.mkdir(parents=True, exist_ok=True)
            ledger.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "mode": arguments.mode,
                        "artifact_revision": revision,
                        "claims": [],
                    },
                    indent=2,
                )
                + chr(10),
                encoding="utf-8",
            )
            marker.write_text(
                json.dumps(
                    {
                        "ledger": ledger.relative_to(root).as_posix(),
                        "artifact_revision": revision,
                    },
                    indent=2,
                )
                + chr(10),
                encoding="utf-8",
            )
            print(ledger.relative_to(root).as_posix())
            return 0
        payload = json.loads(ledger.read_text("utf-8"))
        activation = json.loads(marker.read_text("utf-8"))
        revision = capture_artifact_revision(
            root, excluded_paths=frozenset({ledger})
        )
        if not isinstance(payload, dict) or set(payload) != {
            "schema_version", "mode", "artifact_revision", "claims",
        }:
            print("ledger: root fields mismatch")
            return 1
        if payload["schema_version"] != "1.0":
            print("ledger: schema version mismatch")
            return 1
        if payload["mode"] not in {"closure", "triage"}:
            print("ledger: mode mismatch")
            return 1
        artifact_revision = payload["artifact_revision"]
        if not isinstance(artifact_revision, str) or not artifact_revision:
            print("ledger: artifact revision mismatch")
            return 1
        claims = payload["claims"]
        if not isinstance(claims, list):
            print("ledger: claims must be an array")
            return 1
        if not claims:
            print("ledger: claims must contain at least one claim")
            return 1
        if not isinstance(activation, dict) or set(activation) != {
            "ledger", "artifact_revision",
        }:
            print("verification activation binding mismatch")
            return 1
        if (
            activation.get("ledger") != ledger.relative_to(root).as_posix()
            or activation.get("artifact_revision")
            != artifact_revision
            or revision != artifact_revision
        ):
            print("verification activation binding mismatch")
            return 1
        for index, claim in enumerate(claims):
            error = _claim_error(claim, artifact_revision=artifact_revision)
            if error is not None:
                print(f"ledger: claims[{index}]: {error}")
                return 1
        claim_ids = [claim["id"] for claim in claims]
        if len(claim_ids) != len(set(claim_ids)) or set(claim_ids) != WAVE0_CLAIM_IDS:
            print("ledger: Wave 0 claim set mismatch")
            return 1
        return 0


    if __name__ == "__main__":
        raise SystemExit(main())
    """
).encode("utf-8")


VERIFICATION_FIXTURE_BYTES = {
    "SKILL.md": b"verification fixture skill\n",
    "references/contract.md": b"verification fixture contract\n",
    "references/criteria-code.md": b"verification fixture code criteria\n",
    "references/criteria-evidence.md": b"verification fixture evidence criteria\n",
    "references/criteria-experiment.md": b"verification fixture experiment criteria\n",
    "references/criteria-general.md": b"verification fixture general criteria\n",
    "references/criteria-math.md": b"verification fixture math criteria\n",
    "schemas/claim-ledger.schema.json": b"{\"fixture\":\"claim-ledger\"}\n",
    "scripts/verification_gate.py": TEST_VERIFICATION_GATE_SOURCE,
}


def _run(*args: str, cwd: Path) -> str:
    return subprocess.run(
        args,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _run_direct_script(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    repo_root = Path(__file__).resolve().parents[1]
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    return subprocess.run(
        [r"C:\Python314\python.exe", "-B", script, *args],
        cwd=repo_root,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )


def _write_verification_fixture(
    root: Path,
    *,
    files: Mapping[str, bytes] | None = None,
) -> dict[str, object]:
    active_files = VERIFICATION_FIXTURE_BYTES if files is None else files
    assert tuple(sorted(active_files)) == (
        EXPECTED_VERIFICATION_ACTIVE_PATHS
    )
    records = []
    for relative, data in active_files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        records.append(
            {
                "path": relative,
                "size_bytes": len(data),
                "sha256": sha256(data).hexdigest(),
            }
        )
    return {
        "schema_version": "verification-contract-v1",
        "canonical_relative_root": ".codex/skills/verification",
        "active_path_policy": (
            "skill_plus_references_schemas_and_scripts_without_caches"
        ),
        "files": sorted(records, key=lambda item: item["path"]),
    }


@contextmanager
def _windows_junction(link: Path, target: Path) -> Iterator[Path]:
    if os.name != "nt" or not hasattr(Path, "is_junction"):
        pytest.skip("capability unavailable: windows_junction")
    link.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(target)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not link.is_junction():
        if os.path.lexists(link):
            link.rmdir()
        pytest.skip("capability unavailable: windows_junction")
    try:
        yield link
    finally:
        if os.path.lexists(link):
            link.rmdir()


@contextmanager
def _directory_symlink(link: Path, target: Path) -> Iterator[Path]:
    link.parent.mkdir(parents=True, exist_ok=True)
    try:
        link.symlink_to(target, target_is_directory=True)
    except (NotImplementedError, OSError):
        pytest.skip("capability unavailable: symbolic_link")
    try:
        yield link
    finally:
        if os.path.lexists(link):
            link.unlink()


def _init_repo(path: Path) -> tuple[str, str]:
    path.mkdir()
    _run("git", "init", "-q", cwd=path)
    _run("git", "config", "user.name", "Evidence Test", cwd=path)
    _run("git", "config", "user.email", "evidence@example.invalid", cwd=path)
    (path / "README.md").write_text("parent\n", encoding="utf-8")
    _run("git", "add", "README.md", cwd=path)
    _run("git", "commit", "-qm", "parent", cwd=path)
    parent = _run("git", "rev-parse", "HEAD", cwd=path)
    evidence = path / "docs/verification/evidence/wave-0/child/file.json"
    evidence.parent.mkdir(parents=True)
    evidence.write_text("{}\n", encoding="utf-8")
    _run("git", "add", ".", cwd=path)
    _run("git", "commit", "-qm", "evidence", cwd=path)
    child = _run("git", "rev-parse", "HEAD", cwd=path)
    return parent, child


def _minimal_index(*, stage: str, tested: str, parent: str) -> dict[str, object]:
    payload: dict[str, object] = {
        "schema_version": "remediation-evidence-index-v1",
        "wave": "wave-0",
        "evidence_stage": stage,
        "tested_git_head": tested,
        "implementation_parent_git_head": parent,
        "platform": {"os": "Windows", "release": "test", "architecture": "AMD64"},
        "environment_record": {
            "path": "environment.json",
            "size_bytes": 1,
            "sha256": "0" * 64,
        },
        "dependency_versions": [],
        "dependency_inputs": [],
        "tested_input_policy": {
            "schema_version": "wave-0-source-config-theory-tools-tests-v1",
            "selection_rules": [],
            "exclusion_rules": [],
            "inputs": [],
        },
        "tested_input_inventory_sha256": sha256(canonical_json_bytes([])).hexdigest(),
        "commands": [],
        "source_config_bindings": [],
        "reviewed_plan_binding": {
            "path": "plan",
            "size_bytes": 1,
            "sha256": "1" * 64,
            "commit": parent,
        },
        "verification_contract_binding": {
            "path": "snapshot",
            "size_bytes": 1,
            "sha256": "2" * 64,
        },
        "files": [],
    }
    return payload


@contextmanager
def _short_task_repo() -> Iterator[Path]:
    source = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="w0t4-", dir=r"C:\tmp") as directory:
        repo = Path(directory) / "r"
        _run(
            "git",
            "clone",
            "-q",
            "--shared",
            str(source),
            str(repo),
            cwd=Path(directory),
        )
        _run("git", "config", "user.name", "Evidence Test", cwd=repo)
        _run("git", "config", "user.email", "evidence@example.invalid", cwd=repo)
        for relative in TASK4_TRACKED_PATHS:
            shutil.copy2(source / relative, repo / relative)
        _run("git", "add", *TASK4_TRACKED_PATHS, cwd=repo)
        staged = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=repo,
            check=False,
        ).returncode
        if staged:
            _run("git", "commit", "-qm", "task 4 fixture revision", cwd=repo)
        yield repo


def _write_raw_suite_inputs(repo: Path, *, head: str, stage: str) -> Path:
    raw = repo / f".verification/raw/wave-0/{head[:12]}/{stage}"
    raw.mkdir(parents=True)
    environment = capture_environment_record(
        repo, dependency_input_paths=DEPENDENCY_INPUT_PATHS
    )
    for suite in ("targeted", "subsystem", "full"):
        junit_path = raw / f"{suite}.raw.xml"
        junit_path.write_text(
            (
                f'<testsuite name="{suite}" tests="1" failures="0" errors="0" '
                f'skipped="0" time="0"><testcase classname="tests.fixture" '
                f'name="test_{suite}" time="0"/></testsuite>'
            ),
            encoding="utf-8",
        )
        command = {
            "schema_version": "remediation-command-record-v1",
            "id": suite,
            "argv": _suite_argv(raw.relative_to(repo), suite),
            "cwd_rel": ".",
            "interpreter": environment["interpreter"],
            "env_allowlist": environment["environment_variables"],
            "started_utc": "2026-08-11T00:00:00Z",
            "ended_utc": "2026-08-11T00:00:01Z",
            "exit_code": 0,
            "junit": parse_junit(junit_path),
        }
        (raw / f"{suite}.command.json").write_bytes(canonical_json_bytes(command))
    return raw


def _candidate_bundle(repo: Path) -> PreparedEvidenceBundle:
    head = _run("git", "rev-parse", "HEAD", cwd=repo)
    raw = _write_raw_suite_inputs(repo, head=head, stage="candidate")
    return prepare_evidence_bundle(
        repo_root=repo,
        wave="wave-0",
        evidence_stage="candidate",
        tested_git_head=head,
        implementation_parent_git_head=head,
        raw_dir=raw,
        output_dir=f"docs/verification/evidence/wave-0/{head[:12]}",
    )


def _mutate_bundle_index(
    bundle: PreparedEvidenceBundle, mutation: str
) -> PreparedEvidenceBundle:
    index_item = next(item for item in bundle.files if item.path.name == "index.json")
    payload = json.loads(index_item.data)
    if mutation == "selected_input":
        payload["tested_input_policy"]["inputs"][0]["sha256"] = "f" * 64
        payload["tested_input_inventory_sha256"] = sha256(
            canonical_json_bytes(payload["tested_input_policy"]["inputs"])
        ).hexdigest()
    elif mutation == "dependency":
        payload["dependency_inputs"][0]["sha256"] = "f" * 64
    elif mutation == "plan":
        payload["reviewed_plan_binding"]["sha256"] = "f" * 64
    elif mutation == "snapshot":
        payload["verification_contract_binding"]["sha256"] = "f" * 64
    elif mutation == "source_binding":
        record = next(
            item
            for item in payload["source_config_bindings"]
            if item["path"]
            not in {
                str(remediation_evidence.PLAN_PATH),
                str(remediation_evidence.SNAPSHOT_PATH),
            }
        )
        record["sha256"] = "f" * 64
    else:
        raise AssertionError(f"unknown test mutation: {mutation}")
    replacement = PreparedEvidenceFile(index_item.path, canonical_json_bytes(payload))
    return PreparedEvidenceBundle(
        bundle.output_dir,
        tuple(
            replacement if item.path == index_item.path else item
            for item in bundle.files
        ),
    )


def _tree_snapshot(path: Path) -> tuple[tuple[object, ...], ...] | None:
    if not path.exists():
        return None
    records: list[tuple[object, ...]] = []
    for child in sorted(path.rglob("*"), key=lambda item: item.as_posix()):
        relative = child.relative_to(path).as_posix()
        records.append(
            ("directory", relative)
            if child.is_dir()
            else ("file", relative, sha256(child.read_bytes()).hexdigest())
        )
    return tuple(records)


def _review_score(
    spec: Mapping[str, object],
    *,
    initial: bool,
    order: str | None = None,
    verdict: str = "support",
    triggers: tuple[str, ...] = (),
    unresolved: bool = False,
) -> dict[str, object]:
    criteria = {
        key: 20 for key, _label in CLAIM_CRITERIA_BY_DOMAIN[str(spec["domain"])]
    }
    obligations = [] if verdict == "support" else ["resolve recorded conflict"]
    score: dict[str, object] = {
        "claim_id": spec["id"],
        "domain": spec["domain"],
        "severity": spec["severity"],
        "evidence_ids": list(spec["evidence_ids"]),
        "criteria": criteria,
        "verdict": verdict,
        "escalation_triggers": list(triggers),
        "unresolved_disagreement": unresolved,
        "open_obligations": obligations,
    }
    if initial:
        assert order in {"AB", "BA"}
        score.update(
            {
                "candidate_ids": ["claim-statement", "explicit-negation"],
                "candidate_descriptions": [
                    {
                        "id": "claim-statement",
                        "description": str(spec["statement"]),
                    },
                    {
                        "id": "explicit-negation",
                        "description": f"It is not the case that: {spec['statement']}",
                    },
                ],
                "comparison_order": order,
                "comparison_outcome": "left" if order == "AB" else "right",
                "comparison_criteria": criteria,
            }
        )
    return score


def _write_review(
    raw: Path,
    *,
    relative: str,
    context: Mapping[str, object],
    digest: str,
    tested: str,
    parent: str,
    specs: tuple[Mapping[str, object], ...],
    triggers: tuple[str, ...] = (),
    unresolved: bool = False,
    conflict: bool = False,
) -> None:
    initial = relative in INITIAL_REVIEW_PATHS
    view_id = Path(relative).stem
    order = "AB" if view_id == "code-contract-review" else "BA"
    scores = [
        _review_score(
            spec,
            initial=initial,
            order=order if initial else None,
            verdict="conflict" if conflict and index == 0 else "support",
            triggers=triggers if index == 0 else (),
            unresolved=unresolved if index == 0 else False,
        )
        for index, spec in enumerate(specs)
    ]
    verdict = (
        "conflict"
        if any(score["verdict"] == "conflict" for score in scores)
        else "support"
    )
    aggregate_triggers = sorted(
        {trigger for score in scores for trigger in score["escalation_triggers"]}
    )
    payload = {
        "schema_version": "wave-0-review-v1",
        "view_id": view_id,
        "calibration_kind": "independent_pairwise_source_reading_v1",
        "tested_git_head": tested,
        "implementation_parent_git_head": parent,
        "reviewed_input_inventory_sha256": digest,
        "reviewed_paths": [context["historical_reproduced_source"]],
        "claim_scores": scores,
        "verdict": verdict,
        "escalation_triggers": aggregate_triggers,
        "unresolved_disagreement": any(
            bool(score["unresolved_disagreement"]) for score in scores
        ),
        "open_obligations": [
            obligation for score in scores for obligation in score["open_obligations"]
        ],
        "result_location": relative,
        "falsification_conditions": ["A bound byte or mechanical check changes."],
    }
    destination = raw / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(canonical_json_bytes(payload))


def _write_adjudicators(
    raw: Path,
    *,
    digest: str,
    tested: str,
    parent: str,
    code_target: int,
    code_triggers: tuple[str, ...],
    code_support: bool,
) -> None:
    for relative, spec in zip(ADJUDICATOR_PATHS, CLAIM_SPECS, strict=True):
        is_code = spec["domain"] == "code"
        target = code_target if is_code else 2
        support = code_support if is_code else True
        payload = {
            "schema_version": "wave-0-adjudicator-v1",
            "role": "verifier-adjudicator",
            "claim_id": spec["id"],
            "tested_git_head": tested,
            "implementation_parent_git_head": parent,
            "reviewed_input_inventory_sha256": digest,
            "escalation_triggers": list(code_triggers if is_code else ()),
            "escalation_target": target,
            "view_ids": list(VIEW_IDS_BY_TARGET[target]),
            "result": "support" if support else "abstain",
            "evidence_ids": list(spec["evidence_ids"]),
            "result_location": relative,
            "reason": "All selected evidence supports closure."
            if support
            else "A conflict remains.",
            "falsification_condition": "A selected evidence byte or result changes.",
            "open_obligations": [] if support else ["resolve recorded conflict"],
        }
        destination = raw / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(canonical_json_bytes(payload))


@contextmanager
def _review_validation_repo(
    target: int = 2,
) -> Iterator[tuple[Path, Path, str, str]]:
    with _short_task_repo() as repo:
        parent = _run('git', 'rev-parse', 'HEAD', cwd=repo)
        candidate_dir = publish_evidence_bundle(_candidate_bundle(repo), repo_root=repo)
        _run('git', 'add', '--', candidate_dir.relative_to(repo).as_posix(), cwd=repo)
        _run('git', 'commit', '-qm', 'candidate evidence', cwd=repo)
        tested = _run('git', 'rev-parse', 'HEAD', cwd=repo)
        raw = _write_raw_suite_inputs(repo, head=tested, stage='closure')
        context, _context_bytes, digest = build_review_context(
            repo_root=repo,
            tested_head=tested,
            implementation_parent=parent,
            raw_dir=raw,
            write=True,
        )
        for relative in INITIAL_REVIEW_PATHS:
            _write_review(
                raw,
                relative=relative,
                context=context,
                digest=digest,
                tested=tested,
                parent=parent,
                specs=CLAIM_SPECS,
                triggers=("criterion_disagreement",) if target >= 4 else (),
            )
        code_spec = (CLAIM_SPECS[0],)
        if target >= 4:
            for index, relative in enumerate(TARGET4_ADDITIONAL_REVIEW_PATHS):
                _write_review(
                    raw,
                    relative=relative,
                    context=context,
                    digest=digest,
                    tested=tested,
                    parent=parent,
                    specs=code_spec,
                    triggers=("criterion_disagreement",),
                    unresolved=target == 8,
                    conflict=target == 8 and index == 0,
                )
        if target == 8:
            for relative in TARGET8_ADDITIONAL_REVIEW_PATHS:
                _write_review(
                    raw,
                    relative=relative,
                    context=context,
                    digest=digest,
                    tested=tested,
                    parent=parent,
                    specs=code_spec,
                )
        _write_adjudicators(
            raw,
            digest=digest,
            tested=tested,
            parent=parent,
            code_target=target,
            code_triggers=("criterion_disagreement",) if target >= 4 else (),
            code_support=target != 8,
        )
        assert validate_reviews(
            repo_root=repo,
            tested_head=tested,
            implementation_parent=parent,
            raw_dir=raw,
        ) == target
        yield repo, raw, tested, parent


def _run_gate(
    gate: remediation_evidence.VerifiedVerificationGate,
    repo: Path,
    *args: str,
) -> subprocess.CompletedProcess[str]:
    del repo
    return remediation_evidence.run_verified_verification_gate(
        gate,
        args,
    )


def _review_context_leaf_paths(
    value: object, prefix: tuple[object, ...] = ()
) -> Iterator[tuple[object, ...]]:
    if isinstance(value, dict):
        for key in sorted(value):
            yield from _review_context_leaf_paths(value[key], prefix + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _review_context_leaf_paths(item, prefix + (index,))
    else:
        yield prefix


def _mutate_review_context_leaf(payload: object, path: tuple[object, ...]) -> None:
    cursor = payload
    for component in path[:-1]:
        cursor = cursor[component]  # type: ignore[index]
    leaf = cursor[path[-1]]  # type: ignore[index]
    if leaf is None:
        replacement: object = "mutated"
    elif isinstance(leaf, bool):
        replacement = not leaf
    elif isinstance(leaf, int):
        replacement = leaf + 1
    elif isinstance(leaf, float):
        replacement = leaf + 1.0
    elif isinstance(leaf, str):
        replacement = leaf + "!"
    else:
        raise TypeError(f"unsupported review-context scalar: {type(leaf)!r}")
    cursor[path[-1]] = replacement  # type: ignore[index]


def test_contract_constants_are_exact() -> None:
    assert INDEX_ROOT_FIELDS == EXPECTED_ROOT_FIELDS
    assert JUNIT_FIELDS == EXPECTED_JUNIT_FIELDS
    assert remediation_evidence.WAVE0_DEPENDENCY_INPUT_PATHS == DEPENDENCY_INPUT_PATHS
    assert set(VIEW_IDS_BY_TARGET) == {2, 4, 8}
    assert {target: len(paths) for target, paths in VIEW_IDS_BY_TARGET.items()} == {
        2: 2,
        4: 4,
        8: 8,
    }
    assert {target: len(paths) for target, paths in REVIEW_PATHS_BY_TARGET.items()} == {
        2: 2,
        4: 4,
        8: 8,
    }
    assert {
        target: len(paths) for target, paths in CLOSURE_PUBLIC_PATHS_BY_TARGET.items()
    } == {
        2: 16,
        4: 18,
        8: 22,
    }
    for target in (2, 4, 8):
        assert set(REVIEW_PATHS_BY_TARGET[target]).issubset(
            CLOSURE_PUBLIC_PATHS_BY_TARGET[target]
        )
        assert set(ADJUDICATOR_PATHS).issubset(CLOSURE_PUBLIC_PATHS_BY_TARGET[target])


def test_canonical_json_and_prepared_carriers_are_immutable() -> None:
    assert canonical_json_bytes({"b": 2, "a": 1}) == b'{"a":1,"b":2}\n'
    item = PreparedEvidenceFile(PurePosixPath("a.json"), b"{}\n")
    bundle = PreparedEvidenceBundle(PurePosixPath("out"), (item,))
    with pytest.raises(FrozenInstanceError):
        item.data = b"changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        bundle.files = ()  # type: ignore[misc]


def test_generic_prepare_api_is_public_acyclic_and_exact() -> None:
    prepare = remediation_evidence.prepare_evidence_bundle
    assert tuple(inspect.signature(prepare).parameters) == (
        "repo_root",
        "wave",
        "evidence_stage",
        "tested_git_head",
        "implementation_parent_git_head",
        "command_records",
        "source_config_paths",
        "tested_input_policy",
        "dependency_input_paths",
        "raw_junit_bytes",
        "output_dir",
    )
    assert all(
        parameter.kind is inspect.Parameter.KEYWORD_ONLY
        for parameter in inspect.signature(prepare).parameters.values()
    )
    assert "tools.build_wave0_evidence" not in inspect.getsource(remediation_evidence)


def test_generic_wave_mapping_rejects_unapproved_unsuffixed_wave_d() -> None:
    with pytest.raises(ValueError, match="unsupported evidence wave"):
        remediation_evidence._plan_path_for_wave("wave-d")


@pytest.mark.parametrize(
    ("wave", "plan_label", "dependency_paths"),
    [
        (
            "wave-a",
            "a",
            (
                "pyproject.toml",
                "environments/cuda-rtx5090-cu128.lock.txt",
                "docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md",
                "docs/verification/remediation/verification-contract-v1.json",
            ),
        ),
        (
            "wave-d0",
            "d",
            (
                "pyproject.toml",
                "environments/cuda-rtx5090-cu128.lock.txt",
            ),
        ),
    ],
)
def test_generic_prepare_builds_exact_cross_wave_base_without_writes(
    wave: str,
    plan_label: str,
    dependency_paths: tuple[str, ...],
) -> None:
    with _short_task_repo() as repo:
        head = _run("git", "rev-parse", "HEAD", cwd=repo)
        raw = _write_raw_suite_inputs(repo, head=head, stage="candidate")
        plan_path = (
            "docs/superpowers/plans/"
            f"2026-08-11-scientific-integrity-remediation-wave-{plan_label}.md"
        )
        snapshot_path = "docs/verification/remediation/verification-contract-v1.json"
        selected = {
            plan_path,
            snapshot_path,
            "tools/remediation_evidence.py",
            *dependency_paths,
        }
        policy = {
            "schema_version": f"{wave}-source-config-tests-v1",
            "selection_rules": tuple(f"exact:{path}" for path in sorted(selected)),
            "exclusion_rules": (
                "prefix:docs/verification/evidence/",
                "prefix:verification-evidence/",
                "prefix:.verification/",
            ),
        }
        output = f"docs/verification/evidence/{wave}/{head[:12]}"
        command_records = {
            suite: (raw / f"{suite}.command.json").read_bytes()
            for suite in ("targeted", "subsystem", "full")
        }
        junit_bytes = {
            suite: (raw / f"{suite}.raw.xml").read_bytes()
            for suite in ("targeted", "subsystem", "full")
        }

        bundle = remediation_evidence.prepare_evidence_bundle(
            repo_root=repo,
            wave=wave,
            evidence_stage="candidate",
            tested_git_head=head,
            implementation_parent_git_head=head,
            command_records=command_records,
            source_config_paths=tuple(sorted((plan_path, snapshot_path))),
            tested_input_policy=policy,
            dependency_input_paths=dependency_paths,
            raw_junit_bytes=junit_bytes,
            output_dir=output,
        )

        assert tuple(str(item.path) for item in bundle.files) == (
            remediation_evidence.GENERIC_PUBLIC_PATHS
        )
        assert not (repo / output).exists()
        index = json.loads(
            next(item.data for item in bundle.files if item.path.name == "index.json")
        )
        assert index["wave"] == wave
        assert index["reviewed_plan_binding"]["path"] == plan_path
        assert tuple(item["path"] for item in index["dependency_inputs"]) == (
            dependency_paths
        )
        assert tuple(item["path"] for item in index["files"]) == (
            remediation_evidence.GENERIC_NON_INDEX_PUBLIC_PATHS
        )


def test_generic_prepare_rejects_empty_wave0_dependencies_before_transform(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with _short_task_repo() as repo:
        head = _run("git", "rev-parse", "HEAD", cwd=repo)
        raw = _write_raw_suite_inputs(repo, head=head, stage="candidate")
        policy = {
            "schema_version": remediation_evidence.TESTED_INPUT_SCHEMA,
            "selection_rules": remediation_evidence.TESTED_INPUT_SELECTION_RULES,
            "exclusion_rules": remediation_evidence.TESTED_INPUT_EXCLUSION_RULES,
        }
        command_records = {
            suite: (raw / f"{suite}.command.json").read_bytes()
            for suite in ("targeted", "subsystem", "full")
        }
        junit_bytes = {
            suite: (raw / f"{suite}.raw.xml").read_bytes()
            for suite in ("targeted", "subsystem", "full")
        }

        def unexpected_transform(*args: object, **kwargs: object) -> object:
            del args, kwargs
            raise AssertionError("privacy transform ran before input contract")

        monkeypatch.setattr(
            remediation_evidence, "privacy_transform_bytes", unexpected_transform
        )
        with pytest.raises(ValueError, match="dependency inputs must be nonempty"):
            remediation_evidence.prepare_evidence_bundle(
                repo_root=repo,
                wave="wave-0",
                evidence_stage="candidate",
                tested_git_head=head,
                implementation_parent_git_head=head,
                command_records=command_records,
                source_config_paths=(
                    str(remediation_evidence.PLAN_PATH),
                    str(remediation_evidence.SNAPSHOT_PATH),
                ),
                tested_input_policy=policy,
                dependency_input_paths=(),
                raw_junit_bytes=junit_bytes,
                output_dir=f"docs/verification/evidence/wave-0/{head[:12]}",
            )


def test_wave0_wrapper_reads_each_raw_junit_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with _short_task_repo() as repo:
        head = _run("git", "rev-parse", "HEAD", cwd=repo)
        raw = _write_raw_suite_inputs(repo, head=head, stage="candidate")
        observed: dict[str, int] = {}
        original = wave0_evidence._require_regular_unlinked_file

        def count_read(path: Path, *, label: str) -> bytes:
            source = Path(path)
            if source.parent == raw and source.name.endswith(".raw.xml"):
                observed[source.name] = observed.get(source.name, 0) + 1
            return original(source, label=label)

        monkeypatch.setattr(
            wave0_evidence, "_require_regular_unlinked_file", count_read
        )
        prepare_evidence_bundle(
            repo_root=repo,
            wave="wave-0",
            evidence_stage="candidate",
            tested_git_head=head,
            implementation_parent_git_head=head,
            raw_dir=raw,
            output_dir=f"docs/verification/evidence/wave-0/{head[:12]}",
        )
        assert observed == {
            "full.raw.xml": 1,
            "subsystem.raw.xml": 1,
            "targeted.raw.xml": 1,
        }


def test_parse_junit_uses_testcase_ids_and_skip_reasons(tmp_path: Path) -> None:
    xml = tmp_path / "report.xml"
    xml.write_text(
        '<?xml version="1.0"?><testsuites tests="2" failures="0" errors="0" skipped="1" time="0.5">'
        '<testsuite tests="2" failures="0" errors="0" skipped="1" time="0.5">'
        '<testcase classname="tests.test_a" name="test_ok" time="0.2"/>'
        '<testcase classname="tests.test_a" name="test_skip" time="0.3">'
        '<skipped message="capability unavailable: hard_link"/></testcase>'
        "</testsuite></testsuites>",
        encoding="utf-8",
    )
    parsed = parse_junit(xml)
    assert set(parsed) == EXPECTED_JUNIT_FIELDS
    assert parsed["tests"] == 2
    assert parsed["skipped_cases"] == [
        {
            "testcase_id": "tests.test_a::test_skip",
            "reason": "capability unavailable: hard_link",
        }
    ]
    ids = ["tests.test_a::test_ok", "tests.test_a::test_skip"]
    assert parsed["testcase_id_sha256"] == sha256(canonical_json_bytes(ids)).hexdigest()


def test_real_declared_symlink_node_matches_frozen_skip_allowlist(
    tmp_path: Path,
) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    junit_path = tmp_path / "declared-symlink.xml"
    environment = os.environ.copy()
    for name in (
        "MULTIAGENTELBO_RUN_CUDA_TESTS",
        "VFE3_TEST_DEVICE",
        "CUBLAS_WORKSPACE_CONFIG",
    ):
        environment.pop(name, None)
    environment["CUDA_VISIBLE_DEVICES"] = "-1"
    environment["PYTHONHASHSEED"] = "0"

    result = subprocess.run(
        [
            str(CPU_PYTHON),
            "-B",
            "-m",
            "pytest",
            "tests/test_artifacts.py::test_finalize_rejects_a_declared_symlink",
            "-q",
            "-p",
            "no:cacheprovider",
            f"--junitxml={junit_path}",
        ],
        cwd=repo_root,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    validate_junit_skip_allowlist(
        parse_junit(junit_path),
        allowlist={
            "tests.test_artifacts::test_finalize_rejects_a_declared_symlink": (
                "capability unavailable: symbolic_link"
            )
        },
    )


@pytest.mark.parametrize(
    ("body", "message"),
    [
        (
            '<testcase classname="a" name="x"/><testcase classname="a" name="x"/>',
            "duplicate testcase ID",
        ),
        ('<testcase classname="a"/>', "testcase ID"),
        ('<testcase classname="a" name="x"><failure/></testcase>', "failures"),
    ],
)
def test_parse_junit_rejects_semantic_failures(
    tmp_path: Path, body: str, message: str
) -> None:
    count = body.count("<testcase")
    failures = 1 if "<failure" in body else 0
    xml = tmp_path / "bad.xml"
    xml.write_text(
        f'<testsuite tests="{count}" failures="{failures}" errors="0" skipped="0" time="0">{body}</testsuite>',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match=message):
        parse_junit(xml)


def test_junit_privacy_transform_disambiguates_colliding_public_testcase_ids(
    tmp_path: Path,
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    raw_names = (
        "case[//server]",
        "case[//etc]",
        "case[///etc]",
        "case[///opt/private]",
        "case[////opt/private]",
        "case[file:////opt/private]",
    )

    def transform(
        names: tuple[str, ...],
    ) -> tuple[bytes, dict[str, str], dict[str, object]]:
        root = ET.Element(
            "testsuite",
            tests="6",
            failures="0",
            errors="0",
            skipped="0",
            time="1.25",
        )
        for name in names:
            ET.SubElement(root, "testcase", classname="tests.test_paths", name=name)
        public, _mapping = privacy_transform_bytes(
            ET.tostring(root, encoding="utf-8"),
            kind="junit",
            privacy_context=context,
        )
        public_root = ET.fromstring(public)
        public_names = tuple(
            testcase.attrib["name"] for testcase in public_root.iter("testcase")
        )
        pattern = "public-*.xml"
        output = tmp_path / f"public-{len(list(tmp_path.glob(pattern)))}.xml"
        output.write_bytes(public)
        return public, dict(zip(names, public_names, strict=True)), parse_junit(output)

    public, identifiers, parsed = transform(raw_names)
    reversed_public, reversed_identifiers, reversed_parsed = transform(
        tuple(reversed(raw_names))
    )
    assert identifiers == reversed_identifiers
    assert identifiers["case[///etc]"] == ("case[<ABS_PATH_0001>][PUBLIC_TCID_0001]")
    assert identifiers["case[//etc]"] == ("case[<ABS_PATH_0001>][PUBLIC_TCID_0002]")
    assert identifiers["case[////opt/private]"] == (
        "case[<ABS_PATH_0002>][PUBLIC_TCID_0001]"
    )
    assert identifiers["case[///opt/private]"] == (
        "case[<ABS_PATH_0002>][PUBLIC_TCID_0002]"
    )
    assert identifiers["case[//server]"] == "case[<ABS_PATH_0003>]"
    assert identifiers["case[file:////opt/private]"] == "case[<ABS_PATH_0004>]"
    assert len(set(identifiers.values())) == 6
    assert public.count(b"PUBLIC_TCID_") == 4
    for literal in raw_names:
        assert literal.encode() not in public
    assert_no_literal_absolute_path(public, privacy_context=context)
    for field, expected in (
        ("tests", 6),
        ("failures", 0),
        ("errors", 0),
        ("skipped", 0),
        ("time_seconds", 1.25),
    ):
        assert parsed[field] == reversed_parsed[field] == expected
    assert parsed["testcase_id_sha256"] == reversed_parsed["testcase_id_sha256"]
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )
    assert (
        privacy_transform_bytes(reversed_public, kind="junit", privacy_context=context)[
            0
        ]
        == reversed_public
    )


@pytest.mark.parametrize("suite", ["targeted", "subsystem", "full"])
def test_junit_privacy_transform_accepts_exact_p15_reports(
    tmp_path: Path, suite: str
) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    raw_path = (
        repo_root
        / ".verification"
        / "raw"
        / "wave-0"
        / "0ff7ec6436d8"
        / "candidate"
        / f"{suite}.raw.xml"
    )
    if not raw_path.is_file():
        pytest.skip("exact P15 raw JUnit is local verification evidence")
    context = {
        "repo_root": repo_root,
        "user_home": Path.home(),
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "DESKTOP-RT15E78",
        "path_separator": ";",
    }
    expected = {
        "targeted": (152, 0, 0, 0, 57.117),
        "subsystem": (175, 0, 0, 0, 75.892),
        "full": (1109, 0, 0, 3, 226.629),
    }[suite]
    raw_record = parse_junit(raw_path)
    raw = raw_path.read_bytes()
    public, _mapping = privacy_transform_bytes(
        raw, kind="junit", privacy_context=context
    )
    public_path = tmp_path / f"{suite}.xml"
    public_path.write_bytes(public)
    public_record = parse_junit(public_path)
    fields = ("tests", "failures", "errors", "skipped", "time_seconds")
    assert tuple(raw_record[field] for field in fields) == expected
    assert tuple(public_record[field] for field in fields) == expected
    assert public.count(b"PUBLIC_TCID_") == 4
    assert b"//etc" not in public
    assert b"///opt/private" not in public
    assert_no_literal_absolute_path(public, privacy_context=context)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )
    assert_public_semantics_equal("junit", raw, public, privacy_context=context)


@pytest.mark.parametrize(
    ("names", "message"),
    [
        (
            ("case[PUBLIC_TCID_0001]",),
            "incomplete public testcase ID marker group",
        ),
        (
            ("case", "case[PUBLIC_TCID_0001]"),
            "mixed public testcase ID marker group",
        ),
        (
            ("case[PUBLIC_TCID_0001]", "case[PUBLIC_TCID_0003]"),
            "noncanonical public testcase ID marker group",
        ),
        (("case[PUBLIC_TCID_001]",), "malformed public testcase ID marker"),
        (("case[PUBLIC_TCID_0001]tail",), "malformed public testcase ID marker"),
    ],
)
def test_junit_privacy_transform_rejects_malformed_reserved_marker_groups(
    tmp_path: Path, names: tuple[str, ...], message: str
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    root = ET.Element("testsuite")
    for name in names:
        ET.SubElement(root, "testcase", classname="tests.test_paths", name=name)
    with pytest.raises(ValueError, match=message):
        privacy_transform_bytes(
            ET.tostring(root, encoding="utf-8"),
            kind="junit",
            privacy_context=context,
        )


def test_junit_privacy_transform_rejects_synthesized_id_pre_collision(
    tmp_path: Path,
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    root = ET.Element("testsuite")
    for name in (
        "case[//etc]",
        "case[///etc]",
        "case[<ABS_PATH_0001>][PUBLIC_TCID_0001]",
    ):
        ET.SubElement(root, "testcase", classname="tests.test_paths", name=name)
    with pytest.raises(ValueError, match="public testcase ID marker group"):
        privacy_transform_bytes(
            ET.tostring(root, encoding="utf-8"),
            kind="junit",
            privacy_context=context,
        )


def test_junit_privacy_transform_rejects_reversed_raw_marker_assignment(
    tmp_path: Path,
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    root = ET.Element("testsuite")
    for name in (
        "case[//etc][PUBLIC_TCID_0001]",
        "case[///etc][PUBLIC_TCID_0002]",
    ):
        ET.SubElement(root, "testcase", classname="tests.test_paths", name=name)
    with pytest.raises(ValueError, match="public testcase ID marker"):
        privacy_transform_bytes(
            ET.tostring(root, encoding="utf-8"),
            kind="junit",
            privacy_context=context,
        )


def test_junit_privacy_transform_rejects_nested_reserved_marker_token(
    tmp_path: Path,
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    root = ET.Element("testsuite")
    for ordinal in (1, 2):
        ET.SubElement(
            root,
            "testcase",
            classname="tests.test_paths",
            name=f"case[PUBLIC_TCID_9999][PUBLIC_TCID_{ordinal:04d}]",
        )
    with pytest.raises(ValueError, match="malformed public testcase ID marker"):
        privacy_transform_bytes(
            ET.tostring(root, encoding="utf-8"),
            kind="junit",
            privacy_context=context,
        )


def test_junit_privacy_transform_rejects_marked_identity_that_needs_scrubbing(
    tmp_path: Path,
) -> None:
    private_home = tmp_path / "private-home"
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": private_home,
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    root = ET.Element("testsuite")
    for ordinal in (1, 2):
        ET.SubElement(
            root,
            "testcase",
            classname="tests.test_paths",
            name=f"case[{private_home}][PUBLIC_TCID_{ordinal:04d}]",
        )
    with pytest.raises(ValueError, match="marked JUnit testcase ID changed"):
        privacy_transform_bytes(
            ET.tostring(root, encoding="utf-8"),
            kind="junit",
            privacy_context=context,
        )


def test_junit_privacy_transform_rejects_collision_group_over_marker_capacity() -> None:
    testcases = [
        ET.Element("testcase", classname="tests.test_paths", name="case")
        for _ in range(10_000)
    ]
    raw_identifiers = [f"tests.test_paths::raw-{index:04d}" for index in range(10_000)]
    with pytest.raises(ValueError, match="exceeds public testcase ID marker capacity"):
        remediation_evidence._disambiguate_public_testcase_ids(
            testcases, raw_identifiers
        )
    assert all(testcase.attrib["name"] == "case" for testcase in testcases)


def test_junit_privacy_transform_rejects_raw_duplicate_testcase_ids(
    tmp_path: Path,
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    root = ET.Element("testsuite")
    for _ in range(2):
        ET.SubElement(root, "testcase", classname="tests.test_paths", name="case")
    with pytest.raises(ValueError, match="duplicate testcase ID"):
        privacy_transform_bytes(
            ET.tostring(root, encoding="utf-8"),
            kind="junit",
            privacy_context=context,
        )


@pytest.mark.parametrize(
    ("completed", "triggers", "unresolved", "expected"),
    [
        (2, (), False, 2),
        (2, ("small_margin",), False, 4),
        (2, ("high_dispersion",), False, 4),
        (2, ("criterion_disagreement",), False, 4),
        (4, ("small_margin",), False, 4),
        (4, ("criterion_disagreement",), True, 8),
        (8, ("criterion_disagreement",), True, 8),
    ],
)
def test_review_target_transition_is_exact(
    completed: int, triggers: tuple[str, ...], unresolved: bool, expected: int
) -> None:
    assert (
        required_review_target(
            completed_view_count=completed,
            retained_triggers=triggers,
            unresolved_criterion_disagreement=unresolved,
        )
        == expected
    )


def test_review_target_rejects_invalid_counts_and_triggers() -> None:
    with pytest.raises(ValueError, match="completed view count"):
        required_review_target(
            completed_view_count=3,
            retained_triggers=(),
            unresolved_criterion_disagreement=False,
        )
    with pytest.raises(ValueError, match="escalation trigger"):
        required_review_target(
            completed_view_count=2,
            retained_triggers=("majority_vote",),
            unresolved_criterion_disagreement=False,
        )


@pytest.mark.parametrize("target", [2, 4, 8])
def test_criterion_aggregates_are_exact_means(target: int) -> None:
    keys = tuple(key for key, _ in CLAIM_CRITERIA_BY_DOMAIN["code"])
    views = tuple(
        {key: (view + criterion) % 21 for criterion, key in enumerate(keys)}
        for view in range(target)
    )
    assert compute_criterion_aggregates(views, criterion_keys=keys) == {
        key: sum(view[key] for view in views) / target for key in keys
    }
    with pytest.raises(ValueError, match="criterion"):
        compute_criterion_aggregates(({"coverage": 1},), criterion_keys=keys)


def test_privacy_transform_is_total_idempotent_and_semantic(tmp_path: Path) -> None:
    repo = tmp_path / "private-repository"
    home = tmp_path / "private-home"
    context = {
        "repo_root": repo,
        "user_home": home,
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    raw = {
        "schema_version": "remediation-command-record-v1",
        "id": "targeted",
        "argv": [
            r"C:\Python314\python.exe",
            rf"--root={repo}\cache",
            r"\\server\share\fixture.json",
            r"\\?\C:\device\fixture.json",
            "/opt/tool/cache",
        ],
        "cwd": str(repo),
        "interpreter": {
            "path": r"C:\Python314\python.exe",
            "version": "3.14",
            "size_bytes": 1,
            "sha256": "0" * 64,
        },
        "env_allowlist": {
            "PYTHONPATH": r"C:\private\src;D:\vendor\pkg;\\server\share\lib"
        },
        "started_utc": "2026-08-11T00:00:00Z",
        "ended_utc": "2026-08-11T00:00:01Z",
        "exit_code": 0,
        "junit": {
            "path": str(repo / "targeted.xml"),
            "size_bytes": 1,
            "sha256": "1" * 64,
        },
    }
    raw_bytes = canonical_json_bytes(raw)
    public, mapping = privacy_transform_bytes(
        raw_bytes, kind="command", privacy_context=context
    )
    payload = json.loads(public)
    assert payload["interpreter"]["path"] == "<CPU_PYTHON>"
    assert payload["cwd_rel"] == "."
    assert "cwd" not in payload
    assert re.fullmatch(r"--root=<REPO_ROOT>/cache", payload["argv"][1])
    assert all(
        re.fullmatch(r"<ABS_PATH_\d{4}>", value) for value in payload["argv"][2:]
    )
    assert len(set(payload["env_allowlist"]["PYTHONPATH"].split(";"))) == 3
    assert (
        privacy_transform_bytes(public, kind="command", privacy_context=context)[0]
        == public
    )
    assert mapping["raw_sha256"] == sha256(raw_bytes).hexdigest()
    assert mapping["public_sha256"] == sha256(public).hexdigest()
    assert_no_literal_absolute_path(public)
    assert_public_semantics_equal("command", raw_bytes, public, privacy_context=context)
    mutated = json.loads(public)
    mutated["id"] = "changed"
    with pytest.raises(ValueError, match="semantic"):
        assert_public_semantics_equal(
            "command", raw_bytes, canonical_json_bytes(mutated), privacy_context=context
        )


def test_privacy_transform_preserves_spaced_and_quoted_path_components(
    tmp_path: Path,
) -> None:
    context = {
        "repo_root": tmp_path / "Repository Root",
        "user_home": tmp_path / "User Home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    raw = {
        "argv": [
            r"D:\Program Files\tool.exe",
            r'"E:\Quoted Folder\tool.exe"',
            r"--cache=D:\Program Files\cache",
            r'--quoted="E:\Quoted Folder\cache"',
            r"\\server\share name\folder\fixture.json",
            r"\\?\F:\Device Folder\fixture.json",
            "/opt/Program Files/tool",
        ],
        "environment": {
            "PYTHONPATH": (
                r'D:\Program Files\pkg;"E:\Quoted Folder\pkg";'
                r"\\server\share name\lib"
            ),
            "CACHE_DIR": r"D:\Cache Root",
        },
    }
    raw_bytes = canonical_json_bytes(raw)

    public, _mapping = privacy_transform_bytes(
        raw_bytes, kind="environment", privacy_context=context
    )
    payload = json.loads(public)

    for private in (
        "Program Files",
        "Quoted Folder",
        "share name",
        "Device Folder",
        "Cache Root",
    ):
        assert private.encode() not in public
    assert payload["argv"][0].startswith("<ABS_PATH_")
    assert payload["argv"][1].startswith('"<ABS_PATH_')
    assert payload["argv"][1].endswith('>"')
    assert payload["argv"][2].startswith("--cache=<ABS_PATH_")
    assert payload["argv"][3].startswith('--quoted="<ABS_PATH_')
    pythonpath = payload["environment"]["PYTHONPATH"].split(";")
    assert len(pythonpath) == 3
    assert pythonpath[0].startswith("<ABS_PATH_")
    assert pythonpath[1].startswith('"<ABS_PATH_') and pythonpath[1].endswith('>"')
    assert pythonpath[2].startswith("<ABS_PATH_")
    assert payload["environment"]["CACHE_DIR"].startswith("<ABS_PATH_")
    assert_no_literal_absolute_path(public)
    assert (
        privacy_transform_bytes(public, kind="environment", privacy_context=context)[0]
        == public
    )
    assert_public_semantics_equal(
        "environment", raw_bytes, public, privacy_context=context
    )


def test_privacy_transform_scrubs_spaced_and_quoted_xml_paths(tmp_path: Path) -> None:
    context = {
        "repo_root": tmp_path / "Repository Root",
        "user_home": tmp_path / "User Home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    raw = (
        b'<?xml version="1.0"?>'
        b'<testsuite tests="1" failures="0" errors="0" skipped="0" time="0">'
        b"<properties>"
        b'<property name="cache" value="D:\\Program Files\\cache"/>'
        b'<property name="quoted" value="&quot;E:\\Quoted Folder\\cache&quot;"/>'
        b'<property name="option" value="--root=F:\\Option Folder\\cache"/>'
        b"</properties>"
        b'<testcase classname="tests.test_paths" name="test_paths">'
        b"<system-out>/opt/Program Files/log</system-out>"
        b"</testcase></testsuite>"
    )

    public, _mapping = privacy_transform_bytes(
        raw, kind="junit", privacy_context=context
    )

    for private in ("Program Files", "Quoted Folder", "Option Folder"):
        assert private.encode() not in public
    assert_no_literal_absolute_path(public)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )
    assert_public_semantics_equal("junit", raw, public, privacy_context=context)


def test_privacy_transform_accepts_escaped_junit_fragments_and_placeholder_suffixes(
    tmp_path: Path,
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    raw = (
        b'<?xml version="1.0"?>'
        b'<testsuite tests="2" failures="0" errors="0" skipped="0" time="0">'
        b'<testcase classname="tests.test_xml" '
        b'name="case[&lt;testcase classname=&quot;a&quot; name=&quot;x&quot;/&gt;]" '
        b'file="&lt;REPO_ROOT&gt;/tests/test_xml.py"/>'
        b'<testcase classname="tests.test_xml" '
        b'name="case[&lt;testcase classname=&quot;a&quot; name=&quot;x&quot;&gt;'
        b'&lt;failure/&gt;&lt;/testcase&gt;]"/>'
        b"</testsuite>"
    )

    public, _mapping = privacy_transform_bytes(
        raw, kind="junit", privacy_context=context
    )

    assert b"/&gt;" in public
    assert b"/testcase&gt;" in public
    assert b"&lt;REPO_ROOT&gt;/tests/test_xml.py" in public
    assert_no_literal_absolute_path(public)


def test_privacy_transform_accepts_path_before_embedded_closing_tag(
    tmp_path: Path,
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    quote = chr(34)
    raw = (
        f"<testsuite tests={quote}1{quote} failures={quote}0{quote} "
        f"errors={quote}0{quote} skipped={quote}0{quote} time={quote}0{quote}>"
        f"<testcase classname={quote}tests.test_xml{quote} "
        f"name={quote}case[&lt;testcase&gt;C:\\private\\report.xml"
        f"&lt;/testcase&gt;]{quote}/></testsuite>"
    ).encode("utf-8")
    public, _mapping = privacy_transform_bytes(
        raw, kind="junit", privacy_context=context
    )

    assert b"private" not in public
    assert b"&lt;ABS_PATH_" in public
    assert b"&lt;/testcase&gt;" in public
    assert_no_literal_absolute_path(public)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )


def test_privacy_transform_accepts_nested_hostname_suffix_guard_case(
    tmp_path: Path,
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    quote = chr(34)
    raw = (
        f"<testsuite tests={quote}1{quote} failures={quote}0{quote} "
        f"errors={quote}0{quote} skipped={quote}0{quote} time={quote}0{quote}>"
        f"<testcase classname={quote}tests.test_xml{quote} "
        f"name={quote}guard[&lt;testsuite&gt;&lt;testcase&gt;"
        f"&amp;lt;HOSTNAME&amp;gt;/x&lt;/testcase&gt;&lt;/testsuite&gt;]"
        f"{quote}/></testsuite>"
    ).encode("utf-8")
    public, _mapping = privacy_transform_bytes(
        raw, kind="junit", privacy_context=context
    )

    assert b"&amp;lt;HOSTNAME&amp;gt;&lt;ABS_PATH_" in public
    assert b"&lt;/testcase&gt;" in public
    assert_no_literal_absolute_path(public)


def test_xml_placeholder_guard_rejects_closing_tag_path_smuggling() -> None:
    xml = (
        b"<testsuite><testcase>&lt;ABS_PATH_0001&gt;&lt;/testcase&gt;"
        b"/opt/private</testcase></testsuite>"
    )

    with pytest.raises(ValueError, match="literal absolute path"):
        assert_no_literal_absolute_path(xml)


def test_privacy_transform_scrubs_paths_inside_escaped_xml_fragments(
    tmp_path: Path,
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    quote = chr(34)
    raw = (
        f"<testsuite><testcase name={quote}case[&lt;testsuite&gt;"
        f"&lt;testcase&gt;/opt/private/report.xml&lt;/testcase&gt;"
        f"&lt;/testsuite&gt;]{quote}/></testsuite>"
    ).encode("utf-8")
    public, _mapping = privacy_transform_bytes(
        raw, kind="junit", privacy_context=context
    )

    assert b"/opt/private" not in public
    assert b"&lt;ABS_PATH_" in public
    assert_no_literal_absolute_path(public)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )


def test_privacy_transform_does_not_parse_python_suffix_as_windows_drive(
    tmp_path: Path,
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    quote = chr(34)
    raw = (
        f"<testsuite><testcase name={quote}case[&lt;testsuite source="
        f"&quot;&amp;lt;REPO_ROOT&amp;gt;/tests/test_xml.py:"
        f"/opt/private/report.xml&quot;/&gt;]{quote}/></testsuite>"
    ).encode("utf-8")
    public, _mapping = privacy_transform_bytes(
        raw, kind="junit", privacy_context=context
    )

    assert b"test_xml.p&lt;ABS_PATH_" not in public
    assert b"/opt/private" not in public
    assert_no_literal_absolute_path(public)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )


@pytest.mark.parametrize("suite", ["targeted", "subsystem", "full"])
def test_privacy_transform_accepts_preserved_p6_raw_junit(suite: str) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    raw_path = (
        repo_root
        / ".verification"
        / "raw"
        / "wave-0"
        / "4e2e1d4a87bf"
        / "candidate"
        / f"{suite}.raw.xml"
    )
    if not raw_path.is_file():
        pytest.skip("preserved P6 raw JUnit is local verification evidence")
    context = {
        "repo_root": repo_root,
        "user_home": Path.home(),
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "DESKTOP-RT15E78",
        "path_separator": ";",
    }

    public, _mapping = privacy_transform_bytes(
        raw_path.read_bytes(), kind="junit", privacy_context=context
    )

    assert_no_literal_absolute_path(public, privacy_context=context)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        (
            "test_xml_semantic_path_tokenizer_fails_closed_on_ambiguous_"
            "spaced_path[before=/opt/Private Folder/token.txt after=safe]",
            "test_xml_semantic_path_tokenizer_fails_closed_on_ambiguous_"
            "spaced_path[before=<ABS_PATH_0001> after=safe]",
        ),
        (
            "test_xml_semantic_path_tokenizer_fails_closed_on_ambiguous_"
            r"spaced_path[before=D:\\Program Files\\secret\\token.txt after=safe]",
            "test_xml_semantic_path_tokenizer_fails_closed_on_ambiguous_"
            "spaced_path[before=<ABS_PATH_0001> after=safe]",
        ),
    ],
)
def test_junit_testcase_name_context_redacts_exact_p12_parameter_path(
    tmp_path: Path, name: str, expected: str
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    raw = f'<testsuite><testcase name="{name}"/></testsuite>'.encode()

    with pytest.raises(ValueError, match="literal absolute path"):
        assert_no_literal_absolute_path(raw)
    public, _mapping = privacy_transform_bytes(
        raw, kind="junit", privacy_context=context
    )

    testcase = ET.fromstring(public).find("testcase")
    assert testcase is not None
    assert testcase.attrib["name"] == expected
    assert " after=safe]" in testcase.attrib["name"]
    assert_no_literal_absolute_path(public)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )


@pytest.mark.parametrize("placement", ["text", "property-name"])
def test_p12_parameter_path_context_does_not_relax_other_xml_fields(
    tmp_path: Path, placement: str
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    name = (
        "test_xml_semantic_path_tokenizer_fails_closed_on_ambiguous_"
        "spaced_path[before=/opt/Private Folder/token.txt after=safe]"
    )
    if placement == "text":
        raw = f"<testsuite><testcase>{name}</testcase></testsuite>".encode()
    else:
        raw = (
            f'<testsuite><properties><property name="{name}"/></properties>'
            f"<testcase/></testsuite>"
        ).encode()

    with pytest.raises(ValueError, match="ambiguous XML absolute path"):
        assert_no_literal_absolute_path(raw)
    with pytest.raises(ValueError, match="ambiguous XML absolute path"):
        privacy_transform_bytes(raw, kind="junit", privacy_context=context)


def test_junit_testcase_name_context_redacts_nested_input_expected_pair(
    tmp_path: Path,
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    cases = (
        (
            "test_junit_testcase_name_context_redacts_exact_p12_parameter_path["
            "test_xml_semantic_path_tokenizer_fails_closed_on_ambiguous_spaced_path["
            "before=/opt/Private Folder/token.txt after=safe]-"
            "test_xml_semantic_path_tokenizer_fails_closed_on_ambiguous_spaced_path["
            "before=<ABS_PATH_0001> after=safe]]",
            "test_junit_testcase_name_context_redacts_exact_p12_parameter_path["
            "test_xml_semantic_path_tokenizer_fails_closed_on_ambiguous_spaced_path["
            "before=<ABS_PATH_0001> after=safe]-"
            "test_xml_semantic_path_tokenizer_fails_closed_on_ambiguous_spaced_path["
            "before=<ABS_PATH_0001> after=safe]]",
        ),
        (
            "test_junit_testcase_name_context_redacts_exact_p12_parameter_path["
            r"test_xml_semantic_path_tokenizer_fails_closed_on_ambiguous_spaced_path["
            r"before=D:\\\\Program Files\\\\secret\\\\token.txt after=safe]-"
            "test_xml_semantic_path_tokenizer_fails_closed_on_ambiguous_spaced_path["
            "before=<ABS_PATH_0001> after=safe]]",
            "test_junit_testcase_name_context_redacts_exact_p12_parameter_path["
            "test_xml_semantic_path_tokenizer_fails_closed_on_ambiguous_spaced_path["
            "before=<ABS_PATH_0001> after=safe]-"
            "test_xml_semantic_path_tokenizer_fails_closed_on_ambiguous_spaced_path["
            "before=<ABS_PATH_0001> after=safe]]",
        ),
    )
    for name, expected in cases:
        root = ET.Element("testsuite")
        ET.SubElement(root, "testcase", name=name)
        raw = ET.tostring(root, encoding="utf-8")

        public, _mapping = privacy_transform_bytes(
            raw, kind="junit", privacy_context=context
        )

        testcase = ET.fromstring(public).find("testcase")
        assert testcase is not None
        assert testcase.attrib["name"] == expected
        assert_no_literal_absolute_path(public)
        assert (
            privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
            == public
        )


def test_nested_input_expected_context_does_not_relax_other_xml_fields(
    tmp_path: Path,
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    value = (
        "outer[inner[before=/opt/Private Folder/token.txt after=safe]-"
        "inner[before=<ABS_PATH_0001> after=safe]]"
    )
    roots = []
    text_root = ET.Element("testsuite")
    ET.SubElement(text_root, "testcase").text = value
    roots.append(text_root)
    property_root = ET.Element("testsuite")
    properties = ET.SubElement(property_root, "properties")
    ET.SubElement(properties, "property", name=value)
    ET.SubElement(property_root, "testcase")
    roots.append(property_root)
    for root in roots:
        raw = ET.tostring(root, encoding="utf-8")
        with pytest.raises(ValueError, match="ambiguous XML absolute path"):
            privacy_transform_bytes(raw, kind="junit", privacy_context=context)


def test_nested_input_expected_context_rejects_mismatched_structure(
    tmp_path: Path,
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    invalid_names = (
        (
            "outer[inner[before=/opt/Private Folder/token.txt after=safe]-"
            "different[before=<ABS_PATH_0001> after=safe]]"
        ),
        (
            "outer[inner[before=/opt/Private Folder/token.txt after=safe]-"
            "inner[before=<ABS_PATH_0001>/secret after=safe]]"
        ),
        (
            "outer[inner[before=/opt/Private Folder/token.txt after=safe]-"
            "inner[before=<ABS_PATH_0001> after=unsafe]]"
        ),
        "outer[inner[before=/opt/Private Folder/token.txt after=safe]-other]",
        (
            "outer[inner[before=/opt/Private Folder/token.txt after=safe]-"
            "inner[before=<ABS_PATH_0001> after=safe]-third]"
        ),
    )
    for name in invalid_names:
        root = ET.Element("testsuite")
        ET.SubElement(root, "testcase", name=name)
        with pytest.raises(
            ValueError,
            match="ambiguous XML absolute path|invalid public placeholder path",
        ):
            privacy_transform_bytes(
                ET.tostring(root, encoding="utf-8"),
                kind="junit",
                privacy_context=context,
            )


@pytest.mark.parametrize(
    ("serialized_path", "suffix"),
    [
        (
            "file:///opt/private/report.xml",
            "-<testcase><ABS_PATH_0001></testcase>]",
        ),
        (
            "//server/share/private/report.xml",
            "-<testcase><ABS_PATH_0001></testcase>]",
        ),
        (
            r"D:\\Program Files\\secret\\token.txt",
            "-<testcase><ABS_PATH_0001></testcase>-private_fragments1]",
        ),
        (
            r"\\\\server\\share\\Private Folder\\token.txt",
            "-<testcase><ABS_PATH_0001></testcase>-private_fragments1]",
        ),
    ],
)
def test_junit_testcase_name_redacts_direct_serialized_pytest_path_only(
    tmp_path: Path, serialized_path: str, suffix: str
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    prefix = "test_xml_semantic_path_tokenizer_scrubs_entire_bounded_spaced_path["
    name = f"{prefix}{serialized_path}{suffix}"
    root = ET.Element("testsuite")
    ET.SubElement(root, "testcase", name=name)
    raw = ET.tostring(root, encoding="utf-8")

    public, _mapping = privacy_transform_bytes(
        raw, kind="junit", privacy_context=context
    )

    testcase = ET.fromstring(public).find("testcase")
    assert testcase is not None
    public_name = testcase.attrib["name"]
    assert serialized_path not in public_name
    assert public_name.startswith(f"{prefix}<ABS_PATH_")
    assert public_name.endswith(suffix)
    assert_no_literal_absolute_path(public)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )


def test_junit_testcase_name_preserves_known_placeholder_suffix() -> None:
    repo_root = Path(r"C:\private repository")
    context = {
        "repo_root": repo_root,
        "user_home": Path(r"C:\private home"),
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    suffix = "-<testcase><ABS_PATH_0001></testcase>]"
    name = f"node[{repo_root / 'safe'}{suffix}"
    root = ET.Element("testsuite")
    ET.SubElement(root, "testcase", name=name)

    public, _mapping = privacy_transform_bytes(
        ET.tostring(root, encoding="utf-8"),
        kind="junit",
        privacy_context=context,
    )

    testcase = ET.fromstring(public).find("testcase")
    assert testcase is not None
    assert testcase.attrib["name"] == f"node[<REPO_ROOT>/safe{suffix}"
    assert_no_literal_absolute_path(public)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )


def test_junit_testcase_name_does_not_allow_placeholder_before_opening_tag() -> None:
    root = ET.Element("testsuite")
    ET.SubElement(
        root,
        "testcase",
        name="node[<ABS_PATH_0001><testcase>private</testcase>]",
    )

    with pytest.raises(ValueError, match="invalid public placeholder path"):
        assert_no_literal_absolute_path(ET.tostring(root, encoding="utf-8"))


@pytest.mark.parametrize("suite", ["targeted", "subsystem", "full"])
def test_privacy_transform_accepts_fresh_p12_raw_junit(suite: str) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    raw_path = (
        repo_root
        / ".verification"
        / "raw"
        / "wave-0"
        / "1d2bcc101066"
        / "candidate"
        / f"{suite}.raw.xml"
    )
    if not raw_path.is_file():
        pytest.skip("fresh P12 raw JUnit is local verification evidence")
    context = {
        "repo_root": repo_root,
        "user_home": Path.home(),
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "DESKTOP-RT15E78",
        "path_separator": ";",
    }

    public, _mapping = privacy_transform_bytes(
        raw_path.read_bytes(), kind="junit", privacy_context=context
    )

    assert_no_literal_absolute_path(public, privacy_context=context)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )


@pytest.mark.parametrize("suite", ["targeted", "subsystem", "full"])
def test_privacy_transform_accepts_fresh_p13_raw_junit(suite: str) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    raw_path = (
        repo_root
        / ".verification"
        / "raw"
        / "wave-0"
        / "7a5d4681579f"
        / "candidate"
        / f"{suite}.raw.xml"
    )
    if not raw_path.is_file():
        pytest.skip("fresh P13 raw JUnit is local verification evidence")
    context = {
        "repo_root": repo_root,
        "user_home": Path.home(),
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "DESKTOP-RT15E78",
        "path_separator": ";",
    }

    public, _mapping = privacy_transform_bytes(
        raw_path.read_bytes(), kind="junit", privacy_context=context
    )

    assert_no_literal_absolute_path(public, privacy_context=context)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )


@pytest.mark.parametrize(
    ("semantic", "expected"),
    [
        (
            "file:///opt/private/report.xml",
            b"<testcase>&lt;ABS_PATH_0001&gt;</testcase>",
        ),
        (
            "//server/share/private/report.xml",
            b"<testcase>&lt;ABS_PATH_0001&gt;</testcase>",
        ),
        (
            "case[/opt/private]",
            b"<testcase>case[&lt;ABS_PATH_0001&gt;]</testcase>",
        ),
        (
            "case(/opt/private)",
            b"<testcase>case(&lt;ABS_PATH_0001&gt;)</testcase>",
        ),
        (
            "before=/opt/private,after",
            b"<testcase>before=&lt;ABS_PATH_0001&gt;,after</testcase>",
        ),
        (
            r"case[C:\private\report.xml]",
            b"<testcase>case[&lt;ABS_PATH_0001&gt;]</testcase>",
        ),
    ],
)
def test_xml_semantic_path_tokenizer_preserves_nonpath_boundaries(
    tmp_path: Path, semantic: str, expected: bytes
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    raw = f"<testsuite><testcase>{semantic}</testcase></testsuite>".encode()

    with pytest.raises(ValueError, match="literal absolute path"):
        assert_no_literal_absolute_path(raw)
    public, _mapping = privacy_transform_bytes(
        raw, kind="junit", privacy_context=context
    )

    assert semantic.encode() not in public
    assert b"private" not in public.lower()
    assert expected in public
    assert_no_literal_absolute_path(public)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )


@pytest.mark.parametrize(
    ("semantic", "expected", "private_fragments"),
    [
        (
            r"D:\Program Files\secret\token.txt",
            b"<testcase>&lt;ABS_PATH_0001&gt;</testcase>",
            (b"Program Files", b"secret", b"token.txt"),
        ),
        (
            r"\\server\share\Private Folder\token.txt",
            b"<testcase>&lt;ABS_PATH_0001&gt;</testcase>",
            (b"server", b"Private Folder", b"token.txt"),
        ),
        (
            "/opt/Private Folder/token.txt",
            b"<testcase>&lt;ABS_PATH_0001&gt;</testcase>",
            (b"/opt", b"Private Folder", b"token.txt"),
        ),
        (
            'before="/opt/Private Folder/token.txt",after',
            b'<testcase>before="&lt;ABS_PATH_0001&gt;",after</testcase>',
            (b"/opt", b"Private Folder", b"token.txt"),
        ),
    ],
)
def test_xml_semantic_path_tokenizer_scrubs_entire_bounded_spaced_path(
    tmp_path: Path,
    semantic: str,
    expected: bytes,
    private_fragments: tuple[bytes, ...],
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    raw = f"<testsuite><testcase>{semantic}</testcase></testsuite>".encode()

    with pytest.raises(ValueError, match="literal absolute path"):
        assert_no_literal_absolute_path(raw)
    public, _mapping = privacy_transform_bytes(
        raw, kind="junit", privacy_context=context
    )

    assert semantic.encode() not in public
    assert all(fragment not in public for fragment in private_fragments)
    assert expected in public
    assert_no_literal_absolute_path(public)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )


@pytest.mark.parametrize(
    "semantic",
    [
        "before=/opt/Private Folder/token.txt after=safe",
        r"before=D:\Program Files\secret\token.txt after=safe",
    ],
)
def test_xml_semantic_path_tokenizer_fails_closed_on_ambiguous_spaced_path(
    tmp_path: Path, semantic: str
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    raw = f"<testsuite><testcase>{semantic}</testcase></testsuite>".encode()

    with pytest.raises(ValueError, match="ambiguous XML absolute path"):
        assert_no_literal_absolute_path(raw)
    with pytest.raises(ValueError, match="ambiguous XML absolute path"):
        privacy_transform_bytes(raw, kind="junit", privacy_context=context)


@pytest.mark.parametrize(
    "semantic",
    [
        "/opt/Private Folder token.txt",
        r"D:\Secret Project token.txt",
        r"\\server\share\Secret Project token.txt",
        "/home/chris and christine/file.txt",
    ],
)
def test_xml_semantic_path_tokenizer_never_partially_redacts_spaced_path(
    tmp_path: Path, semantic: str
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    raw = f"<testsuite><testcase>{semantic}</testcase></testsuite>".encode()

    with pytest.raises(ValueError, match="(?:literal|ambiguous).*absolute path"):
        assert_no_literal_absolute_path(raw)
    result: bytes | None = None
    try:
        result = privacy_transform_bytes(raw, kind="junit", privacy_context=context)[0]
    except ValueError as error:
        assert "ambiguous XML absolute path" in str(error)
    if result is not None:
        assert semantic.encode() not in result
        assert b"ABS_PATH_" in result
        assert_no_literal_absolute_path(result)
        assert (
            privacy_transform_bytes(result, kind="junit", privacy_context=context)[0]
            == result
        )


@pytest.mark.parametrize(
    "semantic",
    [
        "</opt/private/report.xml",
        "</home/private/token.txt",
        r"prefix<C:\private\token.txt",
    ],
)
def test_xml_semantic_path_tokenizer_rejects_escaped_angle_smuggling(
    tmp_path: Path, semantic: str
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    encoded = semantic.replace("<", "&lt;")
    raw = f"<testsuite><testcase>{encoded}</testcase></testsuite>".encode()

    with pytest.raises(ValueError, match="literal absolute path"):
        assert_no_literal_absolute_path(raw)
    public, _mapping = privacy_transform_bytes(
        raw, kind="junit", privacy_context=context
    )

    assert b"private" not in public.lower()
    assert b"ABS_PATH_" in public
    assert_no_literal_absolute_path(public)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )


@pytest.mark.parametrize(
    "semantic",
    [
        "//server",
        "//etc",
        "///etc",
        "///opt/private",
        "////opt/private",
        "file:////opt/private",
    ],
)
def test_xml_semantic_path_tokenizer_covers_complete_leading_slash_run(
    tmp_path: Path, semantic: str
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    raw = f"<testsuite><testcase>{semantic}</testcase></testsuite>".encode()

    with pytest.raises(ValueError, match="literal absolute path"):
        assert_no_literal_absolute_path(raw)
    public, _mapping = privacy_transform_bytes(
        raw, kind="junit", privacy_context=context
    )

    assert semantic.encode() not in public
    assert b"<testcase>&lt;ABS_PATH_0001&gt;</testcase>" in public
    assert_no_literal_absolute_path(public)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )


@pytest.mark.parametrize(
    "semantic",
    [
        "https://example.com/path?q=1",
        "http://localhost:8080/test",
        "ftp://files.example.com/archive.tar",
        "urn:test://artifact/id",
        "pytest://case/id",
    ],
)
def test_xml_semantic_path_tokenizer_preserves_non_file_uri_text(
    tmp_path: Path, semantic: str
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    raw = f"<testsuite><testcase>{semantic}</testcase></testsuite>".encode()

    public, _mapping = privacy_transform_bytes(
        raw, kind="junit", privacy_context=context
    )

    testcase = ET.fromstring(public).find("testcase")
    assert testcase is not None
    assert testcase.text == semantic
    assert b"ABS_PATH_" not in public
    assert_no_literal_absolute_path(public)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )
    assert_public_semantics_equal("junit", raw, public, privacy_context=context)


@pytest.mark.parametrize("semantic", [r"\\server", "\\\\server\\"])
@pytest.mark.parametrize("placement", ["text", "attribute"])
def test_xml_semantic_path_tokenizer_scrubs_bounded_unc_server_root(
    tmp_path: Path, semantic: str, placement: str
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    if placement == "text":
        raw = f"<testsuite><testcase>{semantic}</testcase></testsuite>".encode()
    else:
        raw = f'<testsuite private="{semantic}"><testcase/></testsuite>'.encode()

    with pytest.raises(ValueError, match="literal absolute path"):
        assert_no_literal_absolute_path(raw)
    public, _mapping = privacy_transform_bytes(
        raw, kind="junit", privacy_context=context
    )

    root = ET.fromstring(public)
    transformed = (
        root.find("testcase").text if placement == "text" else root.attrib["private"]
    )
    assert transformed == "<ABS_PATH_0001>"
    assert b"server" not in public.lower()
    assert semantic.encode() not in public
    assert_no_literal_absolute_path(public)
    assert (
        privacy_transform_bytes(public, kind="junit", privacy_context=context)[0]
        == public
    )


def test_json_privacy_rejects_placeholder_traversal_and_scrubs_embedded_hostname(
    tmp_path: Path,
) -> None:
    context = {
        "repo_root": tmp_path / "private-repository",
        "user_home": tmp_path / "private-home",
        "cpu_python": Path(r"C:\Python314\python.exe"),
        "hostname": "private-host",
        "path_separator": ";",
    }
    with pytest.raises(ValueError, match="placeholder"):
        assert_no_literal_absolute_path(
            canonical_json_bytes({"path": "<REPO_ROOT>/safe/../outside"})
        )

    public, _mapping = privacy_transform_bytes(
        canonical_json_bytes({"message": "worker=private-host completed"}),
        kind="environment",
        privacy_context=context,
    )
    assert b"private-host" not in public
    assert b"<HOSTNAME>" in public
    assert_no_literal_absolute_path(public, privacy_context=context)


def test_xml_placeholder_guard_accepts_canonical_root_and_home_suffixes() -> None:
    xml = (
        b'<testsuite source="&lt;REPO_ROOT&gt;/tests/test_xml.py:42">'
        b"<testcase>&lt;USER_HOME&gt;/cache/item-1.json</testcase>"
        b"<testcase/> &lt;REPO_ROOT&gt;/safe/nested_file.py"
        b"</testsuite>"
    )

    assert_no_literal_absolute_path(xml)


@pytest.mark.parametrize(
    "xml",
    [
        b'<testsuite source="&lt;CPU_PYTHON&gt;/secret"/>',
        b"<testsuite><testcase>&lt;HOSTNAME&gt;/x</testcase></testsuite>",
        b"<testsuite><testcase/> &lt;PID&gt;/x</testsuite>",
        b'<testsuite source="&#x3C;ABS_PATH_0001&#x3E;/x"/>',
        (
            b"<testsuite><testcase>&#60;REPO_ROOT&#62;/safe/../outside"
            b"</testcase></testsuite>"
        ),
        (
            b"<testsuite><testcase/> &#x3c;REPO_ROOT&#x3e;"
            b"&#92;..&#92;outside</testsuite>"
        ),
        (
            b'<testsuite source="&lt;REPO_ROOT&gt;/tests/test_xml.py:'
            b'/opt/private/report.xml"/>'
        ),
    ],
)
def test_xml_placeholder_guard_rejects_partial_suffixes_and_traversal(
    xml: bytes,
) -> None:
    with pytest.raises(ValueError, match="placeholder"):
        assert_no_literal_absolute_path(xml)


@pytest.mark.parametrize(
    "xml",
    [
        rb'<testsuite private="C:\private\report.xml"/>',
        rb"<testsuite><testcase>\\server\share\report.xml</testcase></testsuite>",
        rb"<testsuite><testcase/>\\?\C:\device\report.xml</testsuite>",
        b"<testsuite><testcase>/opt/private/report.xml</testcase></testsuite>",
    ],
)
def test_xml_absolute_path_guard_rejects_decoded_attribute_text_and_tail(
    xml: bytes,
) -> None:
    with pytest.raises(ValueError, match="literal absolute path"):
        assert_no_literal_absolute_path(xml)


def test_index_rejects_unknown_and_missing_fields(tmp_path: Path) -> None:
    del tmp_path
    with tempfile.TemporaryDirectory(prefix="w0-index-") as directory:
        repo = Path(directory) / "repo"
        parent, _child = _init_repo(repo)
        payload = _minimal_index(stage="candidate", tested=parent, parent=parent)
        unknown = copy.deepcopy(payload)
        unknown["surprise"] = True
        with pytest.raises(ValueError, match="unknown evidence-index field"):
            validate_evidence_index(unknown, repo_root=repo, actual_head=parent)
        missing = copy.deepcopy(payload)
        del missing["tested_input_inventory_sha256"]
        with pytest.raises(ValueError, match="missing evidence-index field"):
            validate_evidence_index(missing, repo_root=repo, actual_head=parent)


def test_index_rejects_duplicate_dependency_paths_with_distinct_records(
    tmp_path: Path,
) -> None:
    del tmp_path
    with tempfile.TemporaryDirectory(prefix="w0-dependency-path-") as directory:
        repo = Path(directory) / "repo"
        parent, _child = _init_repo(repo)
        payload = _minimal_index(stage="candidate", tested=parent, parent=parent)
        payload["dependency_inputs"] = [
            {
                "path": "pyproject.toml",
                "size_bytes": 1,
                "sha256": "0" * 64,
            },
            {
                "path": "pyproject.toml",
                "size_bytes": 2,
                "sha256": "1" * 64,
            },
        ]

        with pytest.raises(
            ValueError, match="dependency inputs contain a duplicate path"
        ):
            validate_evidence_index(payload, repo_root=repo, actual_head=parent)


def test_index_rejects_dependency_case_fold_path_aliases(tmp_path: Path) -> None:
    del tmp_path
    with tempfile.TemporaryDirectory(prefix="w0-dependency-alias-") as directory:
        repo = Path(directory) / "repo"
        parent, _child = _init_repo(repo)
        payload = _minimal_index(stage="candidate", tested=parent, parent=parent)
        payload["dependency_inputs"] = [
            {
                "path": "PyProject.toml",
                "size_bytes": 1,
                "sha256": "0" * 64,
            },
            {
                "path": "pyproject.toml",
                "size_bytes": 2,
                "sha256": "1" * 64,
            },
        ]

        with pytest.raises(ValueError, match="contains a case-fold path alias"):
            validate_evidence_index(payload, repo_root=repo, actual_head=parent)


def test_index_rejects_duplicate_tested_input_paths_with_distinct_records(
    tmp_path: Path,
) -> None:
    del tmp_path
    with tempfile.TemporaryDirectory(prefix="w0-tested-input-path-") as directory:
        repo = Path(directory) / "repo"
        parent, _child = _init_repo(repo)
        payload = _minimal_index(stage="candidate", tested=parent, parent=parent)
        payload["tested_input_policy"]["inputs"] = [
            {
                "path": "src/example.py",
                "size_bytes": 1,
                "sha256": "0" * 64,
            },
            {
                "path": "src/example.py",
                "size_bytes": 2,
                "sha256": "1" * 64,
            },
        ]

        with pytest.raises(ValueError, match="tested inputs contains a duplicate path"):
            validate_evidence_index(payload, repo_root=repo, actual_head=parent)


def test_index_rejects_unknown_evidence_file_kind(tmp_path: Path) -> None:
    del tmp_path
    with tempfile.TemporaryDirectory(prefix="w0-file-kind-") as directory:
        repo = Path(directory) / "repo"
        parent, _child = _init_repo(repo)
        payload = _minimal_index(stage="candidate", tested=parent, parent=parent)
        payload["dependency_inputs"] = [
            {
                "path": path,
                "size_bytes": index + 1,
                "sha256": str(index) * 64,
            }
            for index, path in enumerate(DEPENDENCY_INPUT_PATHS)
        ]
        policy = payload["tested_input_policy"]
        policy["selection_rules"] = list(
            remediation_evidence.TESTED_INPUT_SELECTION_RULES
        )
        policy["exclusion_rules"] = list(
            remediation_evidence.TESTED_INPUT_EXCLUSION_RULES
        )
        payload["files"] = [
            {
                "path": "commands/full.json",
                "kind": "unknown",
                "size_bytes": 1,
                "sha256": "0" * 64,
            }
        ]

        with pytest.raises(ValueError, match="evidence files kind is unsupported"):
            validate_evidence_index(payload, repo_root=repo, actual_head=parent)


@pytest.mark.parametrize(
    "wave",
    ["wave-0", "wave-a", "wave-b", "wave-c", "wave-d0", "wave-d1", "wave-e"],
)
def test_index_rejects_empty_dependencies_for_every_wave(
    tmp_path: Path, wave: str
) -> None:
    del tmp_path
    with tempfile.TemporaryDirectory(prefix="w0-empty-dependencies-") as directory:
        repo = Path(directory) / "repo"
        parent, _child = _init_repo(repo)
        payload = _minimal_index(stage="candidate", tested=parent, parent=parent)
        payload["wave"] = wave

        with pytest.raises(ValueError, match="dependency inputs must be nonempty"):
            validate_evidence_index(payload, repo_root=repo, actual_head=parent)


@pytest.mark.parametrize(
    ("dependency_paths", "policy_field", "policy_value", "message"),
    [
        (
            tuple(reversed(DEPENDENCY_INPUT_PATHS)),
            None,
            None,
            "wave-0 dependency paths differ from frozen contract",
        ),
        (
            DEPENDENCY_INPUT_PATHS[:-1],
            None,
            None,
            "wave-0 dependency paths differ from frozen contract",
        ),
        (
            ("README.md", *DEPENDENCY_INPUT_PATHS[1:]),
            None,
            None,
            "wave-0 dependency paths differ from frozen contract",
        ),
        (
            DEPENDENCY_INPUT_PATHS,
            "schema_version",
            "wave-a-inputs-v1",
            "wave-0 tested-input policy differs from frozen contract",
        ),
        (
            DEPENDENCY_INPUT_PATHS,
            "selection_rules",
            ["prefix:src/"],
            "wave-0 tested-input policy differs from frozen contract",
        ),
        (
            DEPENDENCY_INPUT_PATHS,
            "exclusion_rules",
            [],
            "wave-0 tested-input policy differs from frozen contract",
        ),
    ],
)
def test_index_rejects_wave0_dependency_and_policy_contract_drift(
    tmp_path: Path,
    dependency_paths: tuple[str, ...],
    policy_field: str | None,
    policy_value: object,
    message: str,
) -> None:
    del tmp_path
    with tempfile.TemporaryDirectory(prefix="w0-input-contract-") as directory:
        repo = Path(directory) / "repo"
        parent, _child = _init_repo(repo)
        payload = _minimal_index(stage="candidate", tested=parent, parent=parent)
        payload["dependency_inputs"] = [
            {
                "path": path,
                "size_bytes": index + 1,
                "sha256": str(index) * 64,
            }
            for index, path in enumerate(dependency_paths)
        ]
        policy = payload["tested_input_policy"]
        policy["schema_version"] = remediation_evidence.TESTED_INPUT_SCHEMA
        policy["selection_rules"] = list(
            remediation_evidence.TESTED_INPUT_SELECTION_RULES
        )
        policy["exclusion_rules"] = list(
            remediation_evidence.TESTED_INPUT_EXCLUSION_RULES
        )
        if policy_field is not None:
            policy[policy_field] = policy_value

        with pytest.raises(ValueError, match=message):
            validate_evidence_index(payload, repo_root=repo, actual_head=parent)


def test_candidate_and_closure_heads_cannot_be_swapped(tmp_path: Path) -> None:
    del tmp_path
    with tempfile.TemporaryDirectory(prefix="w0-heads-") as directory:
        repo = Path(directory) / "repo"
        parent, child = _init_repo(repo)
        candidate = _minimal_index(stage="candidate", tested=child, parent=parent)
        with pytest.raises(ValueError, match="candidate head"):
            validate_evidence_index(candidate, repo_root=repo, actual_head=parent)
        closure = _minimal_index(stage="closure", tested=child, parent=child)
        with pytest.raises(ValueError, match="implementation parent"):
            validate_evidence_index(closure, repo_root=repo, actual_head=child)


def test_publish_is_absent_only_and_prevalidates_without_write(tmp_path: Path) -> None:
    output = tmp_path / "public"
    item = PreparedEvidenceFile(
        PurePosixPath("index.json"), canonical_json_bytes({"invalid": True})
    )
    bundle = PreparedEvidenceBundle(PurePosixPath("public"), (item,))
    with pytest.raises(ValueError):
        publish_evidence_bundle(bundle, repo_root=tmp_path)
    assert not output.exists()


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("selected_input", "current tested-input policy"),
        ("dependency", "dependency input byte mismatch"),
        ("plan", "reviewed_plan_binding byte mismatch"),
        ("snapshot", "verification_contract_binding byte mismatch"),
        ("source_binding", "source/config binding"),
    ],
)
def test_publish_rejects_stale_current_bindings_before_any_write(
    mutation: str, message: str
) -> None:
    with _short_task_repo() as repo:
        bundle = _mutate_bundle_index(_candidate_bundle(repo), mutation)
        output = repo.joinpath(*bundle.output_dir.parts)
        parent = output.parent
        before = _tree_snapshot(parent)

        with pytest.raises(ValueError, match=message):
            publish_evidence_bundle(bundle, repo_root=repo)

        assert not output.exists()
        assert _tree_snapshot(parent) == before


def test_disk_validation_rejects_extra_and_rehashed_semantic_drift() -> None:
    with _short_task_repo() as repo:
        bundle = _candidate_bundle(repo)
        output = publish_evidence_bundle(bundle, repo_root=repo)
        index_path = output / "index.json"
        original_index = json.loads(index_path.read_bytes())

        extra = output / "unindexed-extra.json"
        extra.write_bytes(canonical_json_bytes({"unexpected": True}))
        with pytest.raises(ValueError, match="inventory"):
            validate_evidence_index(
                original_index,
                repo_root=repo,
                actual_head=str(original_index["tested_git_head"]),
            )
        extra.unlink()

        command_path = output / "commands/full.json"
        command = json.loads(command_path.read_bytes())
        command["exit_code"] = 1
        command_bytes = canonical_json_bytes(command)
        command_path.write_bytes(command_bytes)
        mutated_index = copy.deepcopy(original_index)
        command_file = next(
            record
            for record in mutated_index["files"]
            if record["path"] == "commands/full.json"
        )
        command_file["size_bytes"] = len(command_bytes)
        command_file["sha256"] = sha256(command_bytes).hexdigest()
        command_binding = next(
            record
            for record in mutated_index["commands"]
            if record["path"] == "commands/full.json"
        )
        command_binding["size_bytes"] = len(command_bytes)
        command_binding["sha256"] = sha256(command_bytes).hexdigest()
        index_path.write_bytes(canonical_json_bytes(mutated_index))
        with pytest.raises(ValueError, match="exit code"):
            validate_evidence_index(
                mutated_index,
                repo_root=repo,
                actual_head=str(mutated_index["tested_git_head"]),
            )


def test_disk_validation_rejects_coherently_rehashed_live_environment_drift() -> None:
    with _short_task_repo() as repo:
        output = publish_evidence_bundle(_candidate_bundle(repo), repo_root=repo)
        index_path = output / "index.json"
        index = json.loads(index_path.read_bytes())

        environment_path = output / "environment.json"
        environment = json.loads(environment_path.read_bytes())
        environment["environment_variables"]["PYTHONHASHSEED"] = "not-live"
        environment_bytes = canonical_json_bytes(environment)
        environment_path.write_bytes(environment_bytes)
        environment_record = {
            "path": "environment.json",
            "size_bytes": len(environment_bytes),
            "sha256": sha256(environment_bytes).hexdigest(),
        }
        index["environment_record"] = environment_record
        indexed_environment = next(
            record for record in index["files"] if record["path"] == "environment.json"
        )
        indexed_environment.update(
            {
                "size_bytes": len(environment_bytes),
                "sha256": sha256(environment_bytes).hexdigest(),
            }
        )

        for suite in ("full", "subsystem", "targeted"):
            relative = f"commands/{suite}.json"
            path = output / relative
            command = json.loads(path.read_bytes())
            command["env_allowlist"]["PYTHONHASHSEED"] = "not-live"
            command_bytes = canonical_json_bytes(command)
            path.write_bytes(command_bytes)
            for collection in (index["commands"], index["files"]):
                record = next(item for item in collection if item["path"] == relative)
                record["size_bytes"] = len(command_bytes)
                record["sha256"] = sha256(command_bytes).hexdigest()

        index_path.write_bytes(canonical_json_bytes(index))
        with pytest.raises(ValueError, match="live execution environment"):
            validate_evidence_index(
                index,
                repo_root=repo,
                actual_head=str(index["tested_git_head"]),
            )


@pytest.mark.parametrize(
    ("domain_index_path", "record_key"),
    [
        ("domain-evidence.json", "path"),
        ("performance-evidence-inventory.json", "name"),
    ],
)
def test_detached_domain_extras_require_complete_one_way_inventory(
    domain_index_path: str,
    record_key: str,
) -> None:
    with _short_task_repo() as repo:
        head = _run("git", "rev-parse", "HEAD", cwd=repo)
        raw = _write_raw_suite_inputs(repo, head=head, stage="candidate")
        resolved_policy = resolve_tested_input_policy(repo)
        policy = {
            key: resolved_policy[key]
            for key in ("schema_version", "selection_rules", "exclusion_rules")
        }
        base = remediation_evidence.prepare_evidence_bundle(
            repo_root=repo,
            wave="wave-0",
            evidence_stage="candidate",
            tested_git_head=head,
            implementation_parent_git_head=head,
            command_records={
                suite: (raw / f"{suite}.command.json").read_bytes()
                for suite in ("full", "subsystem", "targeted")
            },
            source_config_paths=(
                str(remediation_evidence.PLAN_PATH),
                str(remediation_evidence.SNAPSHOT_PATH),
            ),
            tested_input_policy=policy,
            dependency_input_paths=DEPENDENCY_INPUT_PATHS,
            raw_junit_bytes={
                suite: (raw / f"{suite}.raw.xml").read_bytes()
                for suite in ("full", "subsystem", "targeted")
            },
            output_dir=f"docs/verification/evidence/wave-0/{head[:12]}",
        )
        index_item = next(item for item in base.files if str(item.path) == "index.json")
        domain_bytes = canonical_json_bytes({"domain": "eligible"})
        domain_record = {
            record_key: "domain-record.json",
            "size_bytes": len(domain_bytes),
            "sha256": sha256(domain_bytes).hexdigest(),
        }
        if record_key == "name":
            domain_record["kind"] = "profile"
        domain_index_bytes = canonical_json_bytes(
            {
                "schema_version": "test-domain-evidence-v1",
                "base_index": {
                    record_key: "index.json",
                    "size_bytes": len(index_item.data),
                    "sha256": sha256(index_item.data).hexdigest(),
                },
                "artifacts": [domain_record],
            }
        )
        valid = PreparedEvidenceBundle(
            base.output_dir,
            tuple(
                sorted(
                    (
                        *base.files,
                        PreparedEvidenceFile(
                            PurePosixPath(domain_index_path), domain_index_bytes
                        ),
                        PreparedEvidenceFile(
                            PurePosixPath("domain-record.json"), domain_bytes
                        ),
                    ),
                    key=lambda item: str(item.path),
                )
            ),
        )
        remediation_evidence._validate_detached_bundle(valid)

        smuggled = PreparedEvidenceBundle(
            base.output_dir,
            tuple(
                sorted(
                    (
                        *valid.files,
                        PreparedEvidenceFile(
                            PurePosixPath("unbound.json"),
                            canonical_json_bytes({"smuggled": True}),
                        ),
                    ),
                    key=lambda item: str(item.path),
                )
            ),
        )
        with pytest.raises(ValueError, match="domain coverage"):
            remediation_evidence._validate_detached_bundle(smuggled)


@pytest.mark.parametrize(
    ("script", "expected"),
    [
        ("tools/remediation_evidence.py", "run-verification-gate"),
        ("tools/build_wave0_evidence.py", "review-context-sha"),
    ],
)
def test_direct_script_help_starts_without_pythonpath(
    script: str, expected: str
) -> None:
    result = _run_direct_script(script, "--help")

    assert result.returncode == 0, result.stderr
    assert expected in result.stdout
    assert result.stderr == ""


def test_direct_script_build_parser_starts_without_pythonpath() -> None:
    result = _run_direct_script("tools/build_wave0_evidence.py", "build", "--help")

    assert result.returncode == 0, result.stderr
    assert "--stage" in result.stdout
    assert "--tested-head" in result.stdout
    assert result.stderr == ""


def test_direct_script_validate_reaches_lazy_wrapper_import(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _, tested = _init_repo(repo)
    payload = _minimal_index(stage="candidate", tested=tested, parent=tested)
    tested_input_policy = resolve_tested_input_policy(repo)
    payload["tested_input_policy"] = tested_input_policy
    payload["tested_input_inventory_sha256"] = sha256(
        canonical_json_bytes(tested_input_policy["inputs"])
    ).hexdigest()
    index_path = tmp_path / "candidate-index.json"
    index_path.write_bytes(canonical_json_bytes(payload))

    result = _run_direct_script(
        "tools/remediation_evidence.py",
        "validate",
        str(index_path),
        "--cwd",
        str(repo),
    )

    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.strip() == "error: dependency inputs must be nonempty"


def test_direct_script_runs_deterministic_verification_gate_from_retained_bytes(
    tmp_path: Path,
) -> None:
    verification_root = tmp_path / "profile/.codex/skills/verification"
    snapshot = _write_verification_fixture(verification_root)
    snapshot_path = tmp_path / "verification-contract-v1.json"
    snapshot_path.write_bytes(canonical_json_bytes(snapshot))
    repo = tmp_path / "repo"
    _init_repo(repo)
    ledger_relative = ".verification/wave-0/final-ledger.json"

    result = _run_direct_script(
        "tools/remediation_evidence.py",
        "run-verification-gate",
        "--snapshot",
        str(snapshot_path),
        "--root",
        str(verification_root),
        "--",
        "start",
        "--cwd",
        str(repo),
        "--ledger",
        ledger_relative,
        "--mode",
        "closure",
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == ledger_relative
    assert result.stderr == ""
    assert (repo / ledger_relative).is_file()


def test_deterministic_verification_gate_rejects_malformed_nonempty_claim(
    tmp_path: Path,
) -> None:
    verification_root = tmp_path / "profile/.codex/skills/verification"
    snapshot = _write_verification_fixture(verification_root)
    gate = resolve_verified_verification_gate(snapshot, root=verification_root)
    repo = tmp_path / "repo"
    _init_repo(repo)
    ledger_relative = ".verification/wave-0/final-ledger.json"

    started = _run_gate(
        gate,
        repo,
        "start",
        "--cwd",
        str(repo),
        "--ledger",
        ledger_relative,
        "--mode",
        "closure",
    )
    assert started.returncode == 0, started.stderr
    ledger = repo / ledger_relative
    malformed = json.loads(ledger.read_bytes())
    malformed["claims"] = [{}]
    ledger.write_bytes(canonical_json_bytes(malformed))

    validated = _run_gate(gate, repo, "validate", ledger_relative, "--cwd", str(repo))

    assert validated.returncode != 0
    assert "claim fields mismatch" in validated.stdout


def test_parsers_expose_only_the_frozen_commands() -> None:
    generic = remediation_parser()
    assert (
        generic.parse_args(
            [
                "run-verification-gate",
                "--snapshot",
                "s",
                "--root",
                "r",
                "--",
                "start",
            ]
        ).command
        == "run-verification-gate"
    )
    with pytest.raises(SystemExit):
        generic.parse_args(["build"])
    wrapper = wave0_parser()
    assert (
        wrapper.parse_args(
            [
                "build",
                "--stage",
                "candidate",
                "--tested-head",
                "a" * 40,
                "--implementation-parent",
                "a" * 40,
                "--raw-dir",
                ".verification/raw",
                "--output-dir",
                "docs/verification/evidence/wave-0/aaaaaaaaaaaa",
            ]
        ).command
        == "build"
    )
    assert (
        wrapper.parse_args(
            [
                "review-context-sha",
                "--tested-head",
                "b" * 40,
                "--implementation-parent",
                "a" * 40,
                "--raw-dir",
                ".verification/raw",
            ]
        ).command
        == "review-context-sha"
    )
    assert (
        wrapper.parse_args(
            [
                "review-target",
                "--tested-head",
                "b" * 40,
                "--implementation-parent",
                "a" * 40,
                "--raw-dir",
                ".verification/raw",
            ]
        ).command
        == "review-target"
    )
    assert (
        wrapper.parse_args(
            [
                "validate-reviews",
                "--tested-head",
                "b" * 40,
                "--implementation-parent",
                "a" * 40,
                "--raw-dir",
                ".verification/raw",
            ]
        ).command
        == "validate-reviews"
    )
    assert (
        wrapper.parse_args(
            [
                "populate-ledger",
                "--ledger",
                ".verification/wave-0/final-ledger.json",
                "--closure-index",
                "verification-evidence/wave-0/bbbbbbbbbbbb/index.json",
            ]
        ).command
        == "populate-ledger"
    )


def test_review_context_contract_is_closed() -> None:
    assert REVIEW_CONTEXT_FIELDS == (
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


@pytest.mark.parametrize(
    ("target", "relative", "label"),
    [
        (2, INITIAL_REVIEW_PATHS[0], "initial review"),
        (4, TARGET4_ADDITIONAL_REVIEW_PATHS[0], "target-4 review"),
        (8, TARGET8_ADDITIONAL_REVIEW_PATHS[0], "target-8 review"),
        (2, ADJUDICATOR_PATHS[0], "adjudicator"),
    ],
)
def test_validate_reviews_rejects_noncanonical_raw_json_before_closure(
    target: int, relative: str, label: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    with _review_validation_repo(target) as (repo, raw, tested, parent):
        path = raw / relative
        canonical = path.read_bytes()
        payload = json.loads(canonical)
        noncanonical = (
            json.dumps(
                dict(reversed(tuple(payload.items()))),
                separators=(",", ":"),
            )
            + "\n"
        ).encode("utf-8")
        assert json.loads(noncanonical) == payload
        assert canonical_json_bytes(payload) == canonical
        assert noncanonical != canonical
        path.write_bytes(noncanonical)

        closure_dir = repo / f"verification-evidence/wave-0/{tested[:12]}"
        assert not closure_dir.exists()
        with pytest.raises(
            ValueError, match=rf"{re.escape(label)} must be a canonical JSON object"
        ):
            validate_reviews(
                repo_root=repo,
                tested_head=tested,
                implementation_parent=parent,
                raw_dir=raw,
            )
        assert path.read_bytes() == noncanonical
        assert not closure_dir.exists()

        if label == "adjudicator":
            path.write_bytes(canonical)
            original_validate_reviews = wave0_evidence.validate_reviews

            def validate_then_mutate(**kwargs: object) -> int:
                validated_target = original_validate_reviews(**kwargs)
                path.write_bytes(noncanonical)
                return validated_target

            monkeypatch.setattr(
                wave0_evidence, "validate_reviews", validate_then_mutate
            )
            with pytest.raises(
                ValueError,
                match="raw review/adjudicator must be a canonical JSON object",
            ):
                prepare_evidence_bundle(
                    repo_root=repo,
                    wave="wave-0",
                    evidence_stage="closure",
                    tested_git_head=tested,
                    implementation_parent_git_head=parent,
                    raw_dir=raw,
                    output_dir=closure_dir.relative_to(repo),
                )
            assert path.read_bytes() == noncanonical
            assert not closure_dir.exists()


def test_wave0_candidate_review_closure_and_gate_lifecycle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = tmp_path / "profile"
    verification_root = profile / ".codex/skills/verification"
    fixture_snapshot = _write_verification_fixture(verification_root)
    with _short_task_repo() as repo:
        parent = _run("git", "rev-parse", "HEAD", cwd=repo)
        candidate = _candidate_bundle(repo)
        assert len(candidate.files) == 12
        assert {str(item.path) for item in candidate.files} == set(
            CANDIDATE_PUBLIC_PATHS
        )
        candidate_dir = publish_evidence_bundle(candidate, repo_root=repo)
        candidate_index = json.loads((candidate_dir / "index.json").read_bytes())
        validate_evidence_index(candidate_index, repo_root=repo, actual_head=parent)

        _run(
            "git",
            "add",
            "--",
            candidate_dir.relative_to(repo).as_posix(),
            cwd=repo,
        )
        _run("git", "commit", "-qm", "candidate evidence", cwd=repo)
        tested = _run("git", "rev-parse", "HEAD", cwd=repo)
        assert _run("git", "rev-parse", "HEAD^", cwd=repo) == parent
        expected_diff = {
            f"{candidate_dir.relative_to(repo).as_posix()}/{relative}"
            for relative in CANDIDATE_PUBLIC_PATHS
        }
        assert (
            set(
                _run(
                    "git", "diff", "--name-only", f"{parent}..{tested}", cwd=repo
                ).splitlines()
            )
            == expected_diff
        )

        raw = _write_raw_suite_inputs(repo, head=tested, stage="closure")
        context, context_bytes, digest = build_review_context(
            repo_root=repo,
            tested_head=tested,
            implementation_parent=parent,
            raw_dir=raw,
            write=True,
        )
        assert tuple(context) == REVIEW_CONTEXT_FIELDS
        assert (raw / "review-context.json").read_bytes() == context_bytes
        assert sha256(context_bytes).hexdigest() == digest
        leaf_paths = tuple(_review_context_leaf_paths(context))
        assert {path[0] for path in leaf_paths} == set(REVIEW_CONTEXT_FIELDS)
        for path in leaf_paths:
            mutated = copy.deepcopy(context)
            _mutate_review_context_leaf(mutated, path)
            assert sha256(canonical_json_bytes(mutated)).hexdigest() != digest

        detached = raw / str(context["historical_reproduced_source"]["path"])
        detached_bytes = detached.read_bytes()
        detached.unlink()
        with pytest.raises(ValueError, match="detached historical"):
            build_review_context(
                repo_root=repo,
                tested_head=tested,
                implementation_parent=parent,
                raw_dir=raw,
                write=False,
            )
        assert not detached.exists()
        detached.parent.mkdir(parents=True, exist_ok=True)
        detached.write_bytes(detached_bytes)

        closure_output = f"verification-evidence/wave-0/{tested[:12]}"
        with pytest.raises(ValueError, match="initial review"):
            prepare_evidence_bundle(
                repo_root=repo,
                wave="wave-0",
                evidence_stage="closure",
                tested_git_head=tested,
                implementation_parent_git_head=parent,
                raw_dir=raw,
                output_dir=closure_output,
            )
        assert not (repo / closure_output).exists()

        for relative in INITIAL_REVIEW_PATHS:
            _write_review(
                raw,
                relative=relative,
                context=context,
                digest=digest,
                tested=tested,
                parent=parent,
                specs=CLAIM_SPECS,
                triggers=("criterion_disagreement",),
            )
        assert (
            review_target(
                repo_root=repo,
                tested_head=tested,
                implementation_parent=parent,
                raw_dir=raw,
            )
            == 4
        )
        code_spec = (CLAIM_SPECS[0],)
        for relative in TARGET4_ADDITIONAL_REVIEW_PATHS:
            _write_review(
                raw,
                relative=relative,
                context=context,
                digest=digest,
                tested=tested,
                parent=parent,
                specs=code_spec,
                triggers=("criterion_disagreement",),
            )
        assert (
            review_target(
                repo_root=repo,
                tested_head=tested,
                implementation_parent=parent,
                raw_dir=raw,
            )
            == 4
        )
        _write_adjudicators(
            raw,
            digest=digest,
            tested=tested,
            parent=parent,
            code_target=4,
            code_triggers=("criterion_disagreement",),
            code_support=True,
        )
        assert (
            validate_reviews(
                repo_root=repo,
                tested_head=tested,
                implementation_parent=parent,
                raw_dir=raw,
            )
            == 4
        )
        closure4 = prepare_evidence_bundle(
            repo_root=repo,
            wave="wave-0",
            evidence_stage="closure",
            tested_git_head=tested,
            implementation_parent_git_head=parent,
            raw_dir=raw,
            output_dir=closure_output,
        )
        assert {str(item.path) for item in closure4.files} == set(
            CLOSURE_PUBLIC_PATHS_BY_TARGET[4]
        )
        privacy4 = json.loads(
            next(
                item.data
                for item in closure4.files
                if str(item.path) == "privacy-transform.json"
            )
        )
        assert {record["public_path"] for record in privacy4["records"]} == (
            set(CLOSURE_PUBLIC_PATHS_BY_TARGET[4])
            - {"index.json", "privacy-transform.json"}
        )
        assert not (repo / closure_output).exists()

        shutil.rmtree(raw / "reviews/adjudicators")
        for index, relative in enumerate(TARGET4_ADDITIONAL_REVIEW_PATHS):
            _write_review(
                raw,
                relative=relative,
                context=context,
                digest=digest,
                tested=tested,
                parent=parent,
                specs=code_spec,
                triggers=("criterion_disagreement",),
                unresolved=True,
                conflict=index == 0,
            )
        assert (
            review_target(
                repo_root=repo,
                tested_head=tested,
                implementation_parent=parent,
                raw_dir=raw,
            )
            == 8
        )
        for relative in TARGET8_ADDITIONAL_REVIEW_PATHS:
            _write_review(
                raw,
                relative=relative,
                context=context,
                digest=digest,
                tested=tested,
                parent=parent,
                specs=code_spec,
            )
        _write_adjudicators(
            raw,
            digest=digest,
            tested=tested,
            parent=parent,
            code_target=8,
            code_triggers=("criterion_disagreement",),
            code_support=False,
        )
        code_adjudicator_path = raw / ADJUDICATOR_PATHS[0]
        code_adjudicator_bytes = code_adjudicator_path.read_bytes()
        mismatched_adjudicator = json.loads(code_adjudicator_bytes)
        mismatched_adjudicator["escalation_triggers"] = []
        code_adjudicator_path.write_bytes(canonical_json_bytes(mismatched_adjudicator))
        with pytest.raises(ValueError, match="adjudicator escalation triggers"):
            validate_reviews(
                repo_root=repo,
                tested_head=tested,
                implementation_parent=parent,
                raw_dir=raw,
            )
        code_adjudicator_path.write_bytes(code_adjudicator_bytes)
        assert (
            validate_reviews(
                repo_root=repo,
                tested_head=tested,
                implementation_parent=parent,
                raw_dir=raw,
            )
            == 8
        )
        code_adjudicator = json.loads((raw / ADJUDICATOR_PATHS[0]).read_bytes())
        evidence_adjudicator = json.loads((raw / ADJUDICATOR_PATHS[1]).read_bytes())
        assert code_adjudicator["view_ids"] == list(VIEW_IDS_BY_TARGET[8])
        assert evidence_adjudicator["view_ids"] == list(VIEW_IDS_BY_TARGET[2])
        closure8 = prepare_evidence_bundle(
            repo_root=repo,
            wave="wave-0",
            evidence_stage="closure",
            tested_git_head=tested,
            implementation_parent_git_head=parent,
            raw_dir=raw,
            output_dir=closure_output,
        )
        assert {str(item.path) for item in closure8.files} == set(
            CLOSURE_PUBLIC_PATHS_BY_TARGET[8]
        )
        privacy8 = json.loads(
            next(
                item.data
                for item in closure8.files
                if str(item.path) == "privacy-transform.json"
            )
        )
        assert {record["public_path"] for record in privacy8["records"]} == (
            set(CLOSURE_PUBLIC_PATHS_BY_TARGET[8])
            - {"index.json", "privacy-transform.json"}
        )
        assert not (repo / closure_output).exists()

        shutil.rmtree(raw / "reviews")
        for relative in INITIAL_REVIEW_PATHS:
            _write_review(
                raw,
                relative=relative,
                context=context,
                digest=digest,
                tested=tested,
                parent=parent,
                specs=CLAIM_SPECS,
            )
        assert (
            review_target(
                repo_root=repo,
                tested_head=tested,
                implementation_parent=parent,
                raw_dir=raw,
            )
            == 2
        )
        with pytest.raises(ValueError, match="adjudicator"):
            prepare_evidence_bundle(
                repo_root=repo,
                wave="wave-0",
                evidence_stage="closure",
                tested_git_head=tested,
                implementation_parent_git_head=parent,
                raw_dir=raw,
                output_dir=closure_output,
            )
        assert not (repo / closure_output).exists()
        _write_adjudicators(
            raw,
            digest=digest,
            tested=tested,
            parent=parent,
            code_target=2,
            code_triggers=(),
            code_support=True,
        )
        assert (
            validate_reviews(
                repo_root=repo,
                tested_head=tested,
                implementation_parent=parent,
                raw_dir=raw,
            )
            == 2
        )

        closure = prepare_evidence_bundle(
            repo_root=repo,
            wave="wave-0",
            evidence_stage="closure",
            tested_git_head=tested,
            implementation_parent_git_head=parent,
            raw_dir=raw,
            output_dir=closure_output,
        )
        assert len(closure.files) == 16
        assert {str(item.path) for item in closure.files} == set(
            CLOSURE_PUBLIC_PATHS_BY_TARGET[2]
        )
        closure_dir = publish_evidence_bundle(closure, repo_root=repo)
        closure_index = json.loads((closure_dir / "index.json").read_bytes())
        validate_evidence_index(closure_index, repo_root=repo, actual_head=tested)

        verified_gate = remediation_evidence.resolve_verified_verification_gate(
            fixture_snapshot,
            root=verification_root,
        )
        gate = verified_gate
        monkeypatch.setattr(
            Path, "home", classmethod(lambda cls: profile)
        )

        def resolve_lifecycle_gate(
            snapshot: Mapping[str, object] | Path | str, *, root: Path | str
        ) -> remediation_evidence.VerifiedVerificationGate:
            assert Path(snapshot).resolve(strict=True) == repo / SNAPSHOT_PATH
            assert Path(root) == verification_root
            return verified_gate

        monkeypatch.setattr(
            wave0_evidence,
            "resolve_verified_verification_gate",
            resolve_lifecycle_gate,
        )
        ledger_relative = ".verification/wave-0/final-ledger.json"
        public_review_path = closure_dir / INITIAL_REVIEW_PATHS[0]
        original_public_review = public_review_path.read_bytes()
        index_path = closure_dir / "index.json"
        original_index = index_path.read_bytes()
        mutated_public_review = json.loads(original_public_review)
        first_criterion = next(
            iter(mutated_public_review["claim_scores"][0]["criteria"])
        )
        mutated_public_review["claim_scores"][0]["criteria"][first_criterion] = 19
        mutated_public_bytes = canonical_json_bytes(mutated_public_review)
        public_review_path.write_bytes(mutated_public_bytes)
        mutated_index = json.loads(original_index)
        review_record = next(
            item
            for item in mutated_index["files"]
            if item["path"] == INITIAL_REVIEW_PATHS[0]
        )
        review_record["size_bytes"] = len(mutated_public_bytes)
        review_record["sha256"] = sha256(mutated_public_bytes).hexdigest()
        index_path.write_bytes(canonical_json_bytes(mutated_index))
        with pytest.raises(ValueError, match="privacy public byte mismatch"):
            validate_evidence_index(mutated_index, repo_root=repo, actual_head=tested)

        started = _run_gate(
            gate,
            repo,
            "start",
            "--cwd",
            str(repo),
            "--ledger",
            ledger_relative,
            "--mode",
            "closure",
        )
        assert started.returncode == 0, started.stderr
        empty = _run_gate(gate, repo, "validate", ledger_relative, "--cwd", str(repo))
        assert empty.returncode != 0
        assert "claims must contain at least one claim" in empty.stdout
        with pytest.raises(ValueError, match="privacy public byte mismatch"):
            populate_ledger(
                repo_root=repo,
                ledger_path=ledger_relative,
                closure_index_path=index_path,
            )
        marker = repo / ".verification/active.json"
        ledger = repo / ledger_relative
        marker.unlink()
        ledger.unlink()
        public_review_path.write_bytes(original_public_review)
        index_path.write_bytes(original_index)
        started = _run_gate(
            gate,
            repo,
            "start",
            "--cwd",
            str(repo),
            "--ledger",
            ledger_relative,
            "--mode",
            "closure",
        )
        assert started.returncode == 0, started.stderr

        original_ledger = ledger.read_bytes()
        original_marker = marker.read_bytes()
        marker_payload = json.loads(original_marker)
        marker_mutations = []
        with_extra = copy.deepcopy(marker_payload)
        with_extra["unexpected"] = True
        marker_mutations.append(with_extra)
        wrong_path = copy.deepcopy(marker_payload)
        wrong_path["ledger"] = ".verification/wave-0/other.json"
        marker_mutations.append(wrong_path)
        wrong_revision = copy.deepcopy(marker_payload)
        wrong_revision["artifact_revision"] = "git:" + "0" * 40 + ":sha256:" + "0" * 64
        marker_mutations.append(wrong_revision)
        for mutation in marker_mutations:
            marker.write_bytes(canonical_json_bytes(mutation))
            with pytest.raises(ValueError, match="activation marker"):
                populate_ledger(
                    repo_root=repo,
                    ledger_path=ledger_relative,
                    closure_index_path=closure_dir / "index.json",
                )
            assert ledger.read_bytes() == original_ledger
        marker.write_bytes(original_marker)
        drift = repo / "gate-drift.txt"
        drift.write_text("changed after activation\n", encoding="utf-8")
        with pytest.raises(ValueError, match="live artifact changed"):
            populate_ledger(
                repo_root=repo,
                ledger_path=ledger_relative,
                closure_index_path=closure_dir / "index.json",
            )
        assert ledger.read_bytes() == original_ledger
        drift.unlink()

        populate_ledger(
            repo_root=repo,
            ledger_path=ledger_relative,
            closure_index_path=closure_dir / "index.json",
        )
        populated = _run_gate(
            gate, repo, "validate", ledger_relative, "--cwd", str(repo)
        )
        assert populated.returncode == 0, populated.stdout + populated.stderr
        ledger_payload = json.loads(ledger.read_bytes())
        public_reviews, _public_adjudicators = _public_review_records(closure_dir, 2)
        _validate_ledger_projection(ledger_payload, public_reviews)
        rounded_projection = copy.deepcopy(ledger_payload)
        rounded_projection["claims"][0]["criteria"][0]["score"] += 0.1
        with pytest.raises(ValueError, match="criterion aggregate"):
            _validate_ledger_projection(rounded_projection, public_reviews)
        synthesized_view = copy.deepcopy(ledger_payload)
        synthesized_view["claims"][0]["views"]["scores"].append(
            copy.deepcopy(synthesized_view["claims"][0]["views"]["scores"][0])
        )
        with pytest.raises(ValueError, match="view-score projection"):
            _validate_ledger_projection(synthesized_view, public_reviews)
        assert {claim["id"] for claim in ledger_payload["claims"]} == {
            spec["id"] for spec in CLAIM_SPECS
        }
        assert all(
            claim["state"] == "EVIDENCE_VERIFIED"
            and not str(claim["id"]).startswith("AUD-")
            for claim in ledger_payload["claims"]
        )
        assert all(
            claim["artifact_revision"] == ledger_payload["artifact_revision"]
            and all(
                evidence["artifact_revision"] == ledger_payload["artifact_revision"]
                for evidence in claim["evidence"]
            )
            for claim in ledger_payload["claims"]
        )


def test_tested_input_resolver_rejects_matching_untracked_file(tmp_path: Path) -> None:
    del tmp_path
    with tempfile.TemporaryDirectory(prefix="w0-inputs-") as directory:
        repo = Path(directory) / "repo"
        repo.mkdir()
        _run("git", "init", "-q", cwd=repo)
        _run("git", "config", "user.name", "Evidence Test", cwd=repo)
        _run("git", "config", "user.email", "evidence@example.invalid", cwd=repo)
        source = repo / "src/tracked.py"
        source.parent.mkdir()
        source.write_text("VALUE = 1\n", encoding="utf-8")
        _run("git", "add", ".", cwd=repo)
        _run("git", "commit", "-qm", "base", cwd=repo)
        extra = repo / "src/untracked.py"
        extra.write_text("VALUE = 2\n", encoding="utf-8")
        with pytest.raises(ValueError, match="untracked tested input"):
            resolve_tested_input_policy(repo)

def test_wave0_executes_only_the_gate_bytes_retained_during_validation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    verified_source = textwrap.dedent(
        """\
        def capture_artifact_revision(cwd, *, excluded_paths=None):
            return "verified-revision"
        """
    ).encode("utf-8")
    tampered_source = textwrap.dedent(
        """\
        def capture_artifact_revision(cwd, *, excluded_paths=None):
            return "tampered-revision"
        """
    ).encode("utf-8")
    profile = tmp_path / "profile"
    verification_root = profile / ".codex/skills/verification"
    fixture_files = dict(VERIFICATION_FIXTURE_BYTES)
    fixture_files["scripts/verification_gate.py"] = verified_source
    snapshot = _write_verification_fixture(
        verification_root,
        files=fixture_files,
    )
    gate_path = verification_root / "scripts/verification_gate.py"
    repo = tmp_path / "repo"
    repo.mkdir()
    ledger = repo / ".verification/wave-0/final-ledger.json"
    ledger.parent.mkdir(parents=True)
    marker = repo / ".verification/active.json"
    marker.write_bytes(
        canonical_json_bytes(
            {
                "ledger": ".verification/wave-0/final-ledger.json",
                "artifact_revision": "verified-revision",
            }
        )
    )
    snapshot_path = repo / SNAPSHOT_PATH
    snapshot_path.parent.mkdir(parents=True)
    snapshot_path.write_bytes(canonical_json_bytes(snapshot))
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: profile))

    if hasattr(wave0_evidence, "resolve_verified_verification_gate"):
        original_snapshot_resolver = (
            wave0_evidence.resolve_verified_verification_gate
        )

        def replace_after_snapshot_validation(*args: object, **kwargs: object) -> object:
            resolved = original_snapshot_resolver(*args, **kwargs)
            resolved.path.write_bytes(tampered_source)
            return resolved

        monkeypatch.setattr(
            wave0_evidence,
            "resolve_verified_verification_gate",
            replace_after_snapshot_validation,
        )

    assert wave0_evidence._validate_active_gate_binding(
        root=repo,
        ledger=ledger,
        ledger_payload={"artifact_revision": "verified-revision"},
    ) == "verified-revision"
    assert gate_path.read_bytes() == tampered_source



def test_verification_snapshot_resolver_is_exact_and_rejects_extras(
    tmp_path: Path,
) -> None:
    root = tmp_path / "profile/.codex/skills/verification"
    snapshot = _write_verification_fixture(root)
    assert (
        resolve_verified_verification_gate(snapshot, root=root).path
        == root / "scripts/verification_gate.py"
    )
    (root / "scripts/extra.py").write_text("pass\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unexpected active verification file"):
        resolve_verified_verification_gate(snapshot, root=root)


def test_verification_snapshot_resolver_accepts_only_the_profile_sibling_junction(
    tmp_path: Path,
) -> None:
    profile = tmp_path / "profile"
    physical_root = profile / ".claude/skills/verification"
    snapshot = _write_verification_fixture(physical_root)
    lexical_root = profile / ".codex/skills/verification"

    with _windows_junction(lexical_root, physical_root):
        assert (
            resolve_verified_verification_gate(snapshot, root=lexical_root).path
            == physical_root / "scripts/verification_gate.py"
        )
        (physical_root / "scripts/verification_gate.py").write_bytes(
            b"tampered fixture\n"
        )
        with pytest.raises(ValueError, match="active-file mismatch"):
            resolve_verified_verification_gate(snapshot, root=lexical_root)


def test_verification_snapshot_resolver_rejects_noncanonical_lexical_alias(
    tmp_path: Path,
) -> None:
    physical_root = tmp_path / "profile/.codex/skills/verification"
    snapshot = _write_verification_fixture(physical_root)
    alias = tmp_path / "verification-alias"

    with _windows_junction(alias, physical_root):
        with pytest.raises(ValueError, match="lexical"):
            resolve_verified_verification_gate(snapshot, root=alias)


def test_verification_snapshot_resolver_rejects_same_byte_arbitrary_junction(
    tmp_path: Path,
) -> None:
    physical_root = tmp_path / "attacker/.codex/skills/verification"
    snapshot = _write_verification_fixture(physical_root)
    lexical_root = tmp_path / "profile/.codex/skills/verification"

    with _windows_junction(lexical_root, physical_root):
        with pytest.raises(ValueError, match="sibling"):
            resolve_verified_verification_gate(snapshot, root=lexical_root)


def test_verification_snapshot_resolver_rejects_reparse_ancestor(
    tmp_path: Path,
) -> None:
    redirected_codex = tmp_path / "redirected/profile/.codex"
    physical_root = redirected_codex / "skills/verification"
    snapshot = _write_verification_fixture(physical_root)
    lexical_codex = tmp_path / "profile/.codex"
    lexical_root = lexical_codex / "skills/verification"

    with _windows_junction(lexical_codex, redirected_codex):
        with pytest.raises(ValueError, match="reparse ancestor"):
            resolve_verified_verification_gate(snapshot, root=lexical_root)


def test_verification_snapshot_resolver_rejects_terminal_directory_symlink(
    tmp_path: Path,
) -> None:
    physical_root = tmp_path / "attacker/.codex/skills/verification"
    snapshot = _write_verification_fixture(physical_root)
    lexical_root = tmp_path / "profile/.codex/skills/verification"

    with _directory_symlink(lexical_root, physical_root):
        with pytest.raises(ValueError, match="symlink"):
            resolve_verified_verification_gate(snapshot, root=lexical_root)


def test_verification_snapshot_resolver_rejects_nested_junction(
    tmp_path: Path,
) -> None:
    root = tmp_path / "profile/.codex/skills/verification"
    snapshot = _write_verification_fixture(root)
    nested_target = tmp_path / "outside"
    nested_target.mkdir()
    nested = root / "references/nested"

    with _windows_junction(nested, nested_target):
        with pytest.raises(ValueError, match="reparse"):
            resolve_verified_verification_gate(snapshot, root=root)


def test_verified_gate_runner_uses_retained_bytes_after_path_replacement(
    tmp_path: Path,
) -> None:
    verification_root = tmp_path / "profile/.codex/skills/verification"
    snapshot = _write_verification_fixture(verification_root)
    verified = remediation_evidence.resolve_verified_verification_gate(
        snapshot, root=verification_root
    )
    tampered_marker = tmp_path / "tampered-gate-executed.txt"
    verified.path.write_text(
        "from pathlib import Path\n"
        f"Path({str(tampered_marker)!r}).write_text('tampered', encoding='utf-8')\n"
        "def main(): return 91\n",
        encoding="utf-8",
    )
    repo = tmp_path / "repo"
    _init_repo(repo)

    result = remediation_evidence.run_verified_verification_gate(
        verified,
        [
            "start",
            "--cwd",
            str(repo),
            "--ledger",
            ".verification/wave-0/final-ledger.json",
            "--mode",
            "closure",
        ],
    )

    assert result.returncode == 0, result.stderr
    assert not tampered_marker.exists()
    assert (repo / ".verification/wave-0/final-ledger.json").is_file()


def test_isolated_gate_capture_ignores_cwd_and_pythonpath_poisoning(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    verification_root = tmp_path / "profile/.codex/skills/verification"
    snapshot = _write_verification_fixture(verification_root)
    verified = remediation_evidence.resolve_verified_verification_gate(
        snapshot, root=verification_root
    )
    repo = tmp_path / "repo"
    _, head = _init_repo(repo)
    poison = tmp_path / "poison"
    poison.mkdir()
    marker = tmp_path / "shlex-poisoned.txt"
    (poison / "shlex.py").write_text(
        "from pathlib import Path\n"
        f"Path({str(marker)!r}).write_text('poisoned', encoding='utf-8')\n"
        "raise RuntimeError('shadow shlex imported')\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(poison)
    monkeypatch.setenv("PYTHONPATH", str(poison))

    revision = remediation_evidence.capture_verified_artifact_revision(
        verified, cwd=repo
    )

    assert revision.startswith(f"git:{head}:sha256:")
    assert not marker.exists()


def test_isolated_gate_capture_ignores_parent_sys_modules_poisoning(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    verification_root = tmp_path / "profile/.codex/skills/verification"
    snapshot = _write_verification_fixture(verification_root)
    verified = remediation_evidence.resolve_verified_verification_gate(
        snapshot, root=verification_root
    )
    repo = tmp_path / "repo"
    _, head = _init_repo(repo)
    poison = types.ModuleType("argparse")

    def reject_parent_module(_name: str) -> object:
        raise AssertionError("parent argparse poison reached isolated child")

    poison.__getattr__ = reject_parent_module  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "argparse", poison)

    revision = remediation_evidence.capture_verified_artifact_revision(
        verified, cwd=repo
    )

    assert revision.startswith(f"git:{head}:sha256:")


def test_isolated_gate_capture_combines_retained_bytes_and_import_isolation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    verification_root = tmp_path / "profile/.codex/skills/verification"
    snapshot = _write_verification_fixture(verification_root)
    verified = remediation_evidence.resolve_verified_verification_gate(
        snapshot, root=verification_root
    )
    path_marker = tmp_path / "path-tamper.txt"
    verified.path.write_text(
        "from pathlib import Path\n"
        f"Path({str(path_marker)!r}).write_text('tampered', encoding='utf-8')\n"
        "def capture_artifact_revision(cwd, *, excluded_paths=None):\n"
        "    return 'tampered-revision'\n",
        encoding="utf-8",
    )
    repo = tmp_path / "repo"
    _, head = _init_repo(repo)
    poison = tmp_path / "poison"
    poison.mkdir()
    import_marker = tmp_path / "import-poison.txt"
    (poison / "shlex.py").write_text(
        "from pathlib import Path\n"
        f"Path({str(import_marker)!r}).write_text('poisoned', encoding='utf-8')\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(poison)
    monkeypatch.setenv("PYTHONPATH", str(poison))

    revision = remediation_evidence.capture_verified_artifact_revision(
        verified, cwd=repo
    )

    assert revision.startswith(f"git:{head}:sha256:")
    assert not path_marker.exists()
    assert not import_marker.exists()


def test_wave0_never_executes_gate_bytes_in_the_builder_process(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = tmp_path / "profile"
    verification_root = profile / ".codex/skills/verification"
    snapshot = _write_verification_fixture(verification_root)
    repo = tmp_path / "repo"
    _init_repo(repo)
    snapshot_path = repo / SNAPSHOT_PATH
    snapshot_path.parent.mkdir(parents=True)
    snapshot_path.write_bytes(canonical_json_bytes(snapshot))
    ledger = repo / ".verification/wave-0/final-ledger.json"
    ledger.parent.mkdir(parents=True)
    verified = remediation_evidence.resolve_verified_verification_gate(
        snapshot, root=verification_root
    )
    revision = remediation_evidence.capture_verified_artifact_revision(
        verified, cwd=repo, excluded_paths=frozenset({ledger})
    )
    marker = repo / ".verification/active.json"
    marker.write_bytes(
        canonical_json_bytes(
            {
                "ledger": ".verification/wave-0/final-ledger.json",
                "artifact_revision": revision,
            }
        )
    )
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: profile))

    def reject_parent_exec(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("verification gate executed in builder process")

    monkeypatch.setattr(builtins, "exec", reject_parent_exec)

    assert wave0_evidence._validate_active_gate_binding(
        root=repo,
        ledger=ledger,
        ledger_payload={"artifact_revision": revision},
    ) == revision


def test_verified_gate_runner_rejects_unsupported_gate_operation(
    tmp_path: Path,
) -> None:
    verification_root = tmp_path / "profile/.codex/skills/verification"
    snapshot = _write_verification_fixture(verification_root)
    verified = remediation_evidence.resolve_verified_verification_gate(
        snapshot, root=verification_root
    )

    with pytest.raises(ValueError, match="only start or validate"):
        remediation_evidence.run_verified_verification_gate(
            verified, ["abandon", "--cwd", str(tmp_path)]
        )


def test_verified_gate_child_output_is_strictly_framed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    verified = remediation_evidence.VerifiedVerificationGate(
        path=tmp_path / "verification_gate.py",
        source_bytes=b"def main(): return 0\n",
    )

    def malformed_child(*args: object, **kwargs: object) -> subprocess.CompletedProcess[bytes]:
        argv = args[0]
        assert argv[:5] == [
            str(CPU_PYTHON),
            "-I",
            "-S",
            "-B",
            "-c",
        ]
        assert kwargs["input"].endswith(verified.source_bytes)
        return subprocess.CompletedProcess(argv, 0, stdout=b"unframed", stderr=b"")

    monkeypatch.setattr(remediation_evidence.subprocess, "run", malformed_child)

    with pytest.raises(ValueError, match="framed output"):
        remediation_evidence.run_verified_verification_gate(
            verified, ["validate", "ledger.json", "--cwd", str(tmp_path)]
        )


def test_governing_wave0_lifecycle_has_no_resolved_path_execution() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    plan = (
        repo_root
        / "docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md"
    ).read_text("utf-8")
    readme = (
        repo_root / "docs/verification/remediation/README.md"
    ).read_text("utf-8")

    assert "resolve-verification-gate" not in plan
    assert "$gate" not in plan
    assert "run-verification-gate" in plan
    assert "resolve-verification-gate" not in readme
    assert "run-verification-gate" in readme


@pytest.mark.parametrize("wave", tuple("abcde"))
def test_governing_wave_lifecycle_uses_only_retained_byte_runner(wave: str) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    plan = (
        repo_root
        / f"docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-{wave}.md"
    ).read_text("utf-8")

    assert "**Binding 2026-08-13 gate-execution supersession.**" in plan
    assert "resolve-verification-gate" not in plan
    assert "run-verification-gate --snapshot" in plan
    assert re.search(
        r"run-verification-gate\s+--snapshot\s+\S+\s+--root\s+\S+\s+--\s+(?:start|validate)",
        plan,
    )
    inline_runner_examples = re.findall(
        r"`([^`]*run-verification-gate[^`]*)`", plan
    )
    assert inline_runner_examples
    assert all(
        "--snapshot" not in example
        or re.search(r"--\s+(?:(?:start|validate)\b|<start\|validate>)", example)
        for example in inline_runner_examples
    )
    runner_invocations = re.findall(
        r"(?m)^\s*&[^\r\n]*run-verification-gate[^\r\n]*$", plan
    )
    assert runner_invocations
    assert all(
        re.search(r"--\s+(?:start|validate)\b", invocation)
        for invocation in runner_invocations
    )
    assert re.search(
        r"(?mi)^\s*\$(?:resolverOutput|resolvedGate)\s*=", plan
    ) is None
    assert re.search(
        r"(?i)Resolve-Path\s+-LiteralPath\s+\$(?:gate|resolvedGate)\b", plan
    ) is None
    assert re.search(r"(?m)^\s*\$gate\s*=", plan) is None
    assert re.search(
        r"(?m)^\s*&[^\r\n]*\$gate\s+(?:start|validate)\b", plan
    ) is None
    assert re.search(
        r"(?m)^\s*&[^\r\n]*resolve-verification-gate\b", plan
    ) is None
