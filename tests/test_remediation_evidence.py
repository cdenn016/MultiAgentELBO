from __future__ import annotations

import copy
import json
import os
import re
import shutil
import subprocess
import tempfile
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import FrozenInstanceError
from hashlib import sha256
from pathlib import Path, PurePosixPath

import pytest

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
    resolve_verification_gate,
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


def _run_gate(gate: Path, repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(CPU_PYTHON), "-B", str(gate), *args],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
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


@pytest.mark.parametrize(
    ("script", "expected"),
    [
        ("tools/remediation_evidence.py", "resolve-verification-gate"),
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
    assert result.stderr.strip() == "error: candidate public path contract mismatch"


def test_direct_script_resolves_installed_verification_gate() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    verification_root = Path.home() / ".codex/skills/verification"
    expected = (verification_root / "scripts/verification_gate.py").resolve(strict=True)

    result = _run_direct_script(
        "tools/remediation_evidence.py",
        "resolve-verification-gate",
        "--snapshot",
        str(repo_root / SNAPSHOT_PATH),
        "--root",
        str(verification_root),
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == str(expected)
    assert result.stderr == ""


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


def test_wave0_candidate_review_closure_and_gate_lifecycle() -> None:
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

        snapshot = json.loads((repo / SNAPSHOT_PATH).read_bytes())
        gate = resolve_verification_gate(
            snapshot, root=Path.home() / ".codex/skills/verification"
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
        with pytest.raises(ValueError, match="reconstructed public evidence"):
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
