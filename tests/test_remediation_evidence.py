from __future__ import annotations

import copy
import json
import re
import subprocess
import tempfile
from dataclasses import FrozenInstanceError
from hashlib import sha256
from pathlib import Path, PurePosixPath

import pytest

from tools.build_wave0_evidence import (
    ADJUDICATOR_PATHS,
    CLOSURE_PUBLIC_PATHS_BY_TARGET,
    CLAIM_CRITERIA_BY_DOMAIN,
    REVIEW_CONTEXT_FIELDS,
    REVIEW_PATHS_BY_TARGET,
    VIEW_IDS_BY_TARGET,
    compute_criterion_aggregates,
    create_parser as wave0_parser,
    required_review_target,
)
from tools.remediation_evidence import (
    INDEX_ROOT_FIELDS,
    JUNIT_FIELDS,
    EXPECTED_VERIFICATION_ACTIVE_PATHS,
    PreparedEvidenceBundle,
    PreparedEvidenceFile,
    assert_no_literal_absolute_path,
    assert_public_semantics_equal,
    canonical_json_bytes,
    create_parser as remediation_parser,
    parse_junit,
    privacy_transform_bytes,
    publish_evidence_bundle,
    resolve_tested_input_policy,
    resolve_verification_gate,
    validate_evidence_index,
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


def _run(*args: str, cwd: Path) -> str:
    return subprocess.run(
        args,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


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


def test_contract_constants_are_exact() -> None:
    assert INDEX_ROOT_FIELDS == EXPECTED_ROOT_FIELDS
    assert JUNIT_FIELDS == EXPECTED_JUNIT_FIELDS
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


def test_parsers_expose_only_the_frozen_commands() -> None:
    generic = remediation_parser()
    assert (
        generic.parse_args(
            ["resolve-verification-gate", "--snapshot", "s", "--root", "r"]
        ).command
        == "resolve-verification-gate"
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


def test_verification_snapshot_resolver_is_exact_and_rejects_extras(
    tmp_path: Path,
) -> None:
    root = tmp_path / ".codex/skills/verification"
    (root / "references").mkdir(parents=True)
    (root / "schemas").mkdir()
    (root / "scripts").mkdir()
    files = []
    for rel in EXPECTED_VERIFICATION_ACTIVE_PATHS:
        path = root / rel
        path.write_text(rel + "\n", encoding="utf-8")
        data = path.read_bytes()
        files.append(
            {"path": rel, "size_bytes": len(data), "sha256": sha256(data).hexdigest()}
        )
    snapshot = {
        "schema_version": "verification-contract-v1",
        "canonical_relative_root": ".codex/skills/verification",
        "active_path_policy": "skill_plus_references_schemas_and_scripts_without_caches",
        "files": sorted(files, key=lambda item: item["path"]),
    }
    assert (
        resolve_verification_gate(snapshot, root=root)
        == root / "scripts/verification_gate.py"
    )
    (root / "scripts/extra.py").write_text("pass\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unexpected active verification file"):
        resolve_verification_gate(snapshot, root=root)
