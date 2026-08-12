from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import uuid
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Iterable, Mapping, Sequence

if __package__ in (None, ""):
    _DIRECT_SCRIPT_REPO_ROOT = str(Path(__file__).resolve(strict=True).parents[1])
    if _DIRECT_SCRIPT_REPO_ROOT not in sys.path:
        sys.path.insert(0, _DIRECT_SCRIPT_REPO_ROOT)


CPU_PYTHON = Path(r"C:\Python314\python.exe")
COMMAND_FIELDS = {
    "schema_version",
    "id",
    "argv",
    "cwd_rel",
    "interpreter",
    "env_allowlist",
    "started_utc",
    "ended_utc",
    "exit_code",
    "junit",
}
INDEX_ROOT_FIELDS = {
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
JUNIT_FIELDS = {
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
INTERPRETER_FIELDS = {"path", "version", "size_bytes", "sha256"}
FILE_RECORD_FIELDS = {"path", "size_bytes", "sha256"}
INDEX_FILE_FIELDS = {"path", "kind", "size_bytes", "sha256"}
INDEX_FILE_KINDS = {
    "command",
    "junit",
    "environment",
    "dependency",
    "plan_binding",
    "privacy_transform",
    "reproduced_source",
    "review",
    "adjudicator",
    "domain",
}
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
GENERIC_NON_INDEX_PUBLIC_PATHS = tuple(
    path for path in GENERIC_PUBLIC_PATHS if path != "index.json"
)
GENERIC_MAPPED_PUBLIC_PATHS = tuple(
    path for path in GENERIC_NON_INDEX_PUBLIC_PATHS if path != "privacy-transform.json"
)
ENVIRONMENT_KEYS = (
    "CUDA_VISIBLE_DEVICES",
    "MULTIAGENTELBO_RUN_CUDA_TESTS",
    "VFE3_TEST_DEVICE",
    "CUBLAS_WORKSPACE_CONFIG",
    "PYTHONHASHSEED",
    "PYTHONPATH",
)
TESTED_INPUT_SELECTION_RULES = (
    "prefix:src/",
    "prefix:tests/",
    "prefix:Theory/",
    "prefix:tools/",
    "top_level_suffix:.py",
    "exact:pyproject.toml",
    "exact:.gitignore",
    "exact:.gitattributes",
    "exact:environments/cuda-rtx5090-cu128.lock.txt",
    "exact:docs/audits/2026-08-11-post-fixed-ray-deep-audit.md",
    "exact:docs/superpowers/specs/2026-08-11-scientific-integrity-remediation-program-design.md",
    "exact:docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md",
    "exact:docs/verification/remediation/verification-contract-v1.json",
    "prefix:docs/verification/remediation/",
)
TESTED_INPUT_EXCLUSION_RULES = (
    "prefix:docs/verification/evidence/",
    "prefix:verification-evidence/",
    "prefix:.verification/",
    "prefix:.pytest_cache/",
    "prefix:.pytest-",
)
TESTED_INPUT_SCHEMA = "wave-0-source-config-theory-tools-tests-v1"
PLAN_PATH = PurePosixPath(
    "docs/superpowers/plans/2026-08-11-scientific-integrity-remediation-wave-0.md"
)
SNAPSHOT_PATH = PurePosixPath(
    "docs/verification/remediation/verification-contract-v1.json"
)
WAVE0_DEPENDENCY_INPUT_PATHS = (
    "pyproject.toml",
    "environments/cuda-rtx5090-cu128.lock.txt",
    str(SNAPSHOT_PATH),
)
HISTORICAL_INVENTORY_PATH = PurePosixPath(
    "docs/verification/remediation/historical-fixed-ray-bundles-v1.json"
)
EXPECTED_VERIFICATION_ACTIVE_PATHS = (
    "SKILL.md",
    "references/contract.md",
    "references/criteria-code.md",
    "references/criteria-evidence.md",
    "references/criteria-experiment.md",
    "references/criteria-general.md",
    "references/criteria-math.md",
    "schemas/claim-ledger.schema.json",
    "scripts/verification_gate.py",
)
ALLOWED_PLACEHOLDER_RE = re.compile(
    r"<(?:CPU_PYTHON|REPO_ROOT|USER_HOME|HOSTNAME|PID|ABS_PATH_\d{4})>"
)
UNKNOWN_PLACEHOLDER_RE = re.compile(r"<[A-Z][A-Z0-9_]*>")
ALLOWED_PLACEHOLDER_PATH_RE = re.compile(
    r"(?:<(?:REPO_ROOT|USER_HOME)>"
    r"(?:/(?!\.{1,2}(?=/|:|$|[\s\]\[(){};,\x22\x27]))"
    r"[A-Za-z0-9_.@%+=,~-]+)*(?::[0-9]+)?"
    r"|<(?:CPU_PYTHON|HOSTNAME|PID|ABS_PATH_\d{4})>)"
    r"(?=$|[\s\]\[(){};,\x22\x27]|:(?=\s|$))"
)
WINDOWS_ABSOLUTE_RE = re.compile(
    r"(?i)(?:\\\\\?\\[A-Z]:\\|\\\\[^\\/\s\"'<>;]+\\[^\\/\s\"'<>;]+\\|[A-Z]:[\\/])[^\s\"'<>;]*"
)
POSIX_ABSOLUTE_RE = re.compile(r"(?<![A-Za-z0-9_.><\-])/(?![/\s\"'<>;])[^\s\"'<>;]*")
SHA256_RE = re.compile(r"[0-9a-f]{64}")
FULL_SHA_RE = re.compile(r"[0-9a-f]{40}")
WAVE_RE = re.compile(r"wave-(?:0|[a-z](?:[0-9]+)?)")


XML_SEMANTIC_PATH_START_RE = re.compile(
    r"(?i)(?:file:/+(?=[^/\s])|(?<![A-Za-z0-9_.\-/])/+(?=[^/\s])"
    r"|\\\\\?\\[A-Z]:\\|\\\\(?=[^\\/\s]+(?:\\[^\\/\s]+"
    r"|\\?(?=$|[\]\[(){};,\x22\x27<>])))"
    r"|(?<![A-Za-z0-9_./\\\-])[A-Z]:[\\/]"
    r"|(?<![A-Za-z0-9_./\\\-])/(?![\s>]))"
)
EMBEDDED_XML_CLOSING_TAG_RE = re.compile(r"</[A-Za-z_:][A-Za-z0-9_.:\-]*\s*>")
XML_SEMANTIC_PATH_CLOSERS = frozenset("])};,")
XML_SEMANTIC_PATH_OPENERS = {"[": "]", "(": ")", "{": "}"}
XML_SEMANTIC_BARE_PATH_END_RE = re.compile(
    r"(?:[A-Za-z0-9_.@%+=~\-]+(?:[\\/][A-Za-z0-9_.@%+=~\-]+)*"
    r"|[A-Za-z0-9_.@%+=~\-]+\.[A-Za-z0-9_.@%+=~\-]+)"
)
XML_SEMANTIC_PYTEST_PATH_END_RE = re.compile(
    r"(?:[A-Za-z0-9_.@%+=~\-]+(?:[\\/]+[A-Za-z0-9_.@%+=~\-]+)*"
    r"|[A-Za-z0-9_.@%+=~\-]+\.[A-Za-z0-9_.@%+=~\-]+)"
)
XML_SEMANTIC_URI_SCHEME_RE = re.compile(r"[A-Za-z][A-Za-z0-9+.-]*:$")


PUBLIC_TCID_TOKEN = "PUBLIC_TCID_"
PUBLIC_TCID_SUFFIX_RE = re.compile(r"(?s)^(.*)\[PUBLIC_TCID_([0-9]{4})\]$")


PUBLIC_TCID_MAX_ORDINAL = 9999


@dataclass(frozen=True, slots=True)
class PreparedEvidenceFile:
    path: PurePosixPath
    data: bytes


@dataclass(frozen=True, slots=True)
class PreparedEvidenceBundle:
    output_dir: PurePosixPath
    files: tuple[PreparedEvidenceFile, ...]


def canonical_json_bytes(payload: object) -> bytes:
    return (
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _require_closed_fields(
    payload: Mapping[str, object],
    expected: set[str],
    *,
    label: str,
) -> None:
    keys = set(payload)
    missing = expected - keys
    unknown = keys - expected
    if missing:
        raise ValueError(f"missing {label} field: {sorted(missing)[0]}")
    if unknown:
        raise ValueError(f"unknown {label} field: {sorted(unknown)[0]}")


def _require_full_sha(value: object, *, label: str) -> str:
    if not isinstance(value, str) or FULL_SHA_RE.fullmatch(value) is None:
        raise ValueError(f"{label} must be a full lowercase Git SHA")
    return value


def _require_sha256(value: object, *, label: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        raise ValueError(f"{label} must be a lowercase SHA-256")
    return value


def _require_nonnegative_int(value: object, *, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{label} must be a nonnegative integer")
    return value


def _require_nonnegative_number(value: object, *, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be numeric")
    converted = float(value)
    if converted < 0 or not math.isfinite(converted):
        raise ValueError(f"{label} must be finite and nonnegative")
    return converted


def _validate_relative_path(value: object, *, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a nonempty path")
    if "\\" in value:
        raise ValueError(f"{label} must use forward slashes")
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts or "." in pure.parts:
        raise ValueError(f"{label} must be repository-relative without traversal")
    if str(pure) != value:
        raise ValueError(f"{label} is not canonical")
    return value


def _path_is_reparse(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        attributes = path.stat(follow_symlinks=False).st_file_attributes
    except (AttributeError, OSError):
        return False
    return bool(attributes & 0x400)


def _require_regular_unlinked_file(path: Path, *, label: str) -> bytes:
    if not path.exists() or not path.is_file():
        raise ValueError(f"missing {label}: {path}")
    if _path_is_reparse(path):
        raise ValueError(f"{label} must not be a symlink or reparse path: {path}")
    return path.read_bytes()


def _file_record(path: str, data: bytes) -> dict[str, object]:
    return {"path": path, "size_bytes": len(data), "sha256": _sha256(data)}


def _git(
    repo_root: Path,
    *arguments: str,
    binary: bool = False,
) -> bytes | str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=not binary,
    )
    if result.returncode != 0:
        stderr = result.stderr
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        raise ValueError(f"git {' '.join(arguments)} failed: {stderr.strip()}")
    if binary:
        assert isinstance(result.stdout, bytes)
        return result.stdout
    assert isinstance(result.stdout, str)
    return result.stdout.strip()


def _git_head(repo_root: Path) -> str:
    return _require_full_sha(_git(repo_root, "rev-parse", "HEAD"), label="HEAD")


def _matches_rule(path: str, rule: str) -> bool:
    kind, value = rule.split(":", 1)
    if kind == "prefix":
        return path.startswith(value)
    if kind == "exact":
        return path == value
    if kind == "top_level_suffix":
        return "/" not in path and path.endswith(value)
    raise ValueError(f"unknown tested-input selection rule: {rule}")


def _validate_policy_template(payload: object) -> dict[str, object]:
    if not isinstance(payload, Mapping):
        raise ValueError("tested-input policy template must be an object")
    _require_closed_fields(
        payload,
        {"schema_version", "selection_rules", "exclusion_rules"},
        label="tested-input policy template",
    )
    schema_version = payload["schema_version"]
    if not isinstance(schema_version, str) or not schema_version:
        raise ValueError("tested-input policy schema_version must be nonempty")
    normalized: dict[str, object] = {"schema_version": schema_version}
    for field in ("selection_rules", "exclusion_rules"):
        value = payload[field]
        if not isinstance(value, (list, tuple)) or not all(
            isinstance(rule, str) and rule for rule in value
        ):
            raise ValueError(f"tested-input {field} must be an ordered string array")
        rules = list(value)
        if len(rules) != len(set(rules)):
            raise ValueError(f"tested-input {field} contains a duplicate rule")
        for rule in rules:
            kind, separator, argument = rule.partition(":")
            if (
                not separator
                or not argument
                or kind
                not in {
                    "prefix",
                    "exact",
                    "top_level_suffix",
                }
            ):
                raise ValueError(f"unknown tested-input selection rule: {rule}")
        normalized[field] = rules
    return normalized


def _is_selected_tested_input(
    path: str,
    *,
    selection_rules: Sequence[str] = TESTED_INPUT_SELECTION_RULES,
    exclusion_rules: Sequence[str] = TESTED_INPUT_EXCLUSION_RULES,
) -> bool:
    if any(_matches_rule(path, rule) for rule in exclusion_rules):
        return False
    return any(_matches_rule(path, rule) for rule in selection_rules)


def _nul_paths(data: bytes) -> tuple[str, ...]:
    values = []
    for item in data.split(b"\0"):
        if item:
            values.append(item.decode("utf-8"))
    return tuple(values)


def _resolve_tested_input_policy(
    repo_root: Path | str,
    policy_template: Mapping[str, object],
) -> dict[str, object]:
    root = Path(repo_root).resolve(strict=True)
    template = _validate_policy_template(policy_template)
    selection_rules = template["selection_rules"]
    exclusion_rules = template["exclusion_rules"]
    assert isinstance(selection_rules, list)
    assert isinstance(exclusion_rules, list)
    tracked = _nul_paths(_git(root, "ls-files", "-z", binary=True))
    untracked = _nul_paths(
        _git(root, "ls-files", "--others", "--exclude-standard", "-z", binary=True)
    )
    matching_untracked = sorted(
        path
        for path in untracked
        if _is_selected_tested_input(
            path,
            selection_rules=selection_rules,
            exclusion_rules=exclusion_rules,
        )
    )
    if matching_untracked:
        raise ValueError(f"untracked tested input: {matching_untracked[0]}")
    selected = sorted(
        path
        for path in tracked
        if _is_selected_tested_input(
            path,
            selection_rules=selection_rules,
            exclusion_rules=exclusion_rules,
        )
    )
    if len(selected) != len(set(selected)):
        raise ValueError("duplicate tested input")
    folded: dict[str, str] = {}
    inputs: list[dict[str, object]] = []
    for relative in selected:
        canonical = _validate_relative_path(relative, label="tested input path")
        key = canonical.casefold()
        if key in folded and folded[key] != canonical:
            raise ValueError(
                f"case-fold tested-input collision: {folded[key]} and {canonical}"
            )
        folded[key] = canonical
        data = _require_regular_unlinked_file(root / canonical, label="tested input")
        inputs.append(_file_record(canonical, data))
    return {
        **template,
        "inputs": inputs,
    }


def resolve_tested_input_policy(repo_root: Path | str) -> dict[str, object]:
    return _resolve_tested_input_policy(
        repo_root,
        {
            "schema_version": TESTED_INPUT_SCHEMA,
            "selection_rules": TESTED_INPUT_SELECTION_RULES,
            "exclusion_rules": TESTED_INPUT_EXCLUSION_RULES,
        },
    )


def _validate_file_inventory(
    value: object,
    *,
    label: str,
    with_kind: bool = False,
    require_sorted: bool = True,
) -> list[dict[str, object]]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    expected_fields = INDEX_FILE_FIELDS if with_kind else FILE_RECORD_FIELDS
    records: list[dict[str, object]] = []
    paths: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f"{label}[{index}] must be an object")
        _require_closed_fields(item, expected_fields, label=f"{label} record")
        path = _validate_relative_path(item["path"], label=f"{label} path")
        _require_nonnegative_int(item["size_bytes"], label=f"{label} size_bytes")
        _require_sha256(item["sha256"], label=f"{label} sha256")
        if with_kind and item["kind"] not in INDEX_FILE_KINDS:
            raise ValueError(f"{label} kind is unsupported: {item['kind']}")
        paths.append(path)
        records.append(item)
    if require_sorted and paths != sorted(paths):
        raise ValueError(f"{label} must be ASCII-path-sorted")
    exact_duplicate = len(set(paths)) != len(paths)
    if require_sorted and exact_duplicate:
        raise ValueError(f"{label} contains a duplicate path")
    if not exact_duplicate and len({path.casefold() for path in paths}) != len(paths):
        raise ValueError(f"{label} contains a case-fold path alias")
    return records


def _parse_count(element: ET.Element, name: str, *, default: int | None = None) -> int:
    raw = element.attrib.get(name)
    if raw is None:
        if default is None:
            raise ValueError(f"JUnit is missing {name} count")
        return default
    try:
        value = int(raw)
    except ValueError as error:
        raise ValueError(f"JUnit {name} count is not an integer") from error
    return _require_nonnegative_int(value, label=f"JUnit {name}")


def _parse_junit_bytes(data: bytes, *, public_path: str) -> dict[str, object]:
    try:
        root = ET.fromstring(data)
    except ET.ParseError as error:
        raise ValueError(f"invalid JUnit XML: {error}") from error
    testcases = list(root.iter("testcase"))
    identifiers: list[str] = []
    skipped_cases: list[dict[str, str]] = []
    observed_failures = 0
    observed_errors = 0
    for testcase in testcases:
        classname = testcase.attrib.get("classname")
        name = testcase.attrib.get("name")
        if not classname or not name:
            raise ValueError("JUnit testcase ID requires classname and name")
        identifier = f"{classname}::{name}"
        if identifier in identifiers:
            raise ValueError(f"duplicate testcase ID: {identifier}")
        identifiers.append(identifier)
        observed_failures += len(testcase.findall("failure"))
        observed_errors += len(testcase.findall("error"))
        skipped = testcase.find("skipped")
        if skipped is not None:
            reason = skipped.attrib.get("message")
            if reason is None:
                reason = (skipped.text or "").strip()
            if not reason:
                raise ValueError(f"JUnit skipped testcase lacks a reason: {identifier}")
            skipped_cases.append({"testcase_id": identifier, "reason": reason})
    suites = list(root.findall(".//testsuite"))

    def declared_total(name: str, fallback: int) -> int:
        if name in root.attrib:
            return _parse_count(root, name)
        if suites and all(name in suite.attrib for suite in suites):
            return sum(_parse_count(suite, name) for suite in suites)
        return fallback

    declared_tests = declared_total("tests", len(testcases))
    declared_failures = declared_total("failures", observed_failures)
    declared_errors = declared_total("errors", observed_errors)
    declared_skipped = declared_total("skipped", len(skipped_cases))
    if declared_tests != len(testcases):
        raise ValueError("JUnit tests count disagrees with testcase elements")
    if declared_failures != observed_failures:
        raise ValueError("JUnit failures count disagrees with testcase outcomes")
    if declared_errors != observed_errors:
        raise ValueError("JUnit errors count disagrees with testcase outcomes")
    if declared_skipped != len(skipped_cases):
        raise ValueError("JUnit skipped count disagrees with testcase outcomes")
    if declared_failures:
        raise ValueError("JUnit contains failures")
    if declared_errors:
        raise ValueError("JUnit contains errors")
    raw_time_text = root.attrib.get("time")
    if (
        raw_time_text is None
        and suites
        and all("time" in suite.attrib for suite in suites)
    ):
        try:
            raw_time_text = str(sum(float(suite.attrib["time"]) for suite in suites))
        except ValueError as error:
            raise ValueError("JUnit time must be numeric") from error
    try:
        raw_time = float(raw_time_text or "0")
    except ValueError as error:
        raise ValueError("JUnit time must be numeric") from error
    time_seconds = _require_nonnegative_number(raw_time, label="JUnit time")
    identifiers.sort()
    skipped_cases.sort(key=lambda item: item["testcase_id"])
    return {
        "path": public_path,
        "size_bytes": len(data),
        "sha256": _sha256(data),
        "tests": declared_tests,
        "failures": declared_failures,
        "errors": declared_errors,
        "skipped": declared_skipped,
        "time_seconds": time_seconds,
        "testcase_id_sha256": _sha256(canonical_json_bytes(identifiers)),
        "skipped_cases": skipped_cases,
    }


def parse_junit(path: Path | str) -> dict[str, object]:
    source = Path(path)
    data = _require_regular_unlinked_file(source, label="JUnit XML")
    return _parse_junit_bytes(data, public_path=source.as_posix())


def validate_junit_skip_allowlist(
    junit: Mapping[str, object],
    *,
    allowlist: Mapping[str, str],
) -> None:
    skipped_cases = junit.get("skipped_cases")
    if not isinstance(skipped_cases, list):
        raise ValueError("JUnit skipped_cases must be an array")
    for item in skipped_cases:
        if not isinstance(item, dict) or set(item) != {"testcase_id", "reason"}:
            raise ValueError("invalid JUnit skipped-case record")
        testcase_id = item["testcase_id"]
        reason = item["reason"]
        if not isinstance(testcase_id, str) or allowlist.get(testcase_id) != reason:
            raise ValueError(f"unexplained skip: {testcase_id}")


def _normalize_path_text(value: str) -> str:
    normalized = value.replace("\\", "/")
    if normalized.startswith("//?/"):
        normalized = normalized[4:]
    while "//" in normalized:
        normalized = normalized.replace("//", "/")
    return normalized.rstrip("/")


def _split_component_wrapper(value: str) -> tuple[str, str, str, str]:
    stripped_left = value.lstrip()
    leading = value[: len(value) - len(stripped_left)]
    stripped = stripped_left.rstrip()
    trailing = stripped_left[len(stripped) :]
    quote = ""
    core = stripped
    if len(core) >= 2 and core[0] == core[-1] and core[0] in {"'", '"'}:
        quote = core[0]
        core = core[1:-1]
    return leading, quote, core, trailing


def _component_core(value: str) -> str:
    return _split_component_wrapper(value)[2]


def _is_absolute_component(value: str) -> bool:
    core = _component_core(value)
    return bool(
        re.match(
            r"(?i)^(?:\\\\\?\\[A-Z]:\\|\\\\[^\\/]+\\[^\\/]+\\|[A-Z]:[\\/])",
            core,
        )
        or core.startswith("/")
    )


def _privacy_values(privacy_context: Mapping[str, object]) -> dict[str, object]:
    required = {"repo_root", "user_home", "cpu_python", "hostname", "path_separator"}
    missing = required - set(privacy_context)
    if missing:
        raise ValueError(f"privacy context missing field: {sorted(missing)[0]}")
    path_separator = privacy_context["path_separator"]
    if path_separator not in (";", ":"):
        raise ValueError("privacy path separator must be ';' or ':'")
    return {
        **privacy_context,
        "repo_root": str(Path(privacy_context["repo_root"])),
        "user_home": str(Path(privacy_context["user_home"])),
        "cpu_python": str(Path(privacy_context["cpu_python"])),
        "hostname": str(privacy_context["hostname"]),
        "path_separator": path_separator,
    }


def _iter_string_components(
    value: object,
    *,
    path_separator: str,
    key: str | None = None,
) -> Iterable[str]:
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from _iter_string_components(
                child, path_separator=path_separator, key=str(child_key)
            )
    elif isinstance(value, list):
        for child in value:
            yield from _iter_string_components(
                child, path_separator=path_separator, key=key
            )
    elif isinstance(value, str):
        if key == "PYTHONPATH":
            for component in value.split(path_separator):
                if _is_absolute_component(component):
                    yield component
            return
        if value.startswith("--") and "=" in value:
            _, right = value.split("=", 1)
            if _is_absolute_component(right):
                yield right
                return
        if _is_absolute_component(value):
            yield value
            return
        for match in WINDOWS_ABSOLUTE_RE.finditer(value):
            yield match.group(0)
        for match in POSIX_ABSOLUTE_RE.finditer(value):
            yield match.group(0)


def _xml_strings_with_context(root: ET.Element) -> Iterable[tuple[str, bool]]:
    for element in root.iter():
        for key, value in element.attrib.items():
            yield value, element.tag == "testcase" and key == "name"
        if element.text:
            yield element.text, False
        if element.tail:
            yield element.tail, False


def _xml_strings(root: ET.Element) -> Iterable[str]:
    for value, _junit_testcase_name in _xml_strings_with_context(root):
        yield value


def _mask_equal_length(value: str, spans: Iterable[tuple[int, int]]) -> str:
    masked = list(value)
    for start, end in spans:
        masked[start:end] = [" "] * (end - start)
    return "".join(masked)


def _is_final_pytest_parameter_assignment_suffix(
    value: str, *, path_start: int, suffix_start: int
) -> bool:
    if not value.endswith("]"):
        return False
    opener = value.rfind("[", 0, path_start)
    if opener < 0 or value.rfind("]", 0, path_start) > opener:
        return False
    return (
        re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=[^\s\[\]]+", value[suffix_start:-1])
        is not None
    )


def _is_mirrored_pytest_input_expected_boundary(
    value: str, *, path_start: int, suffix_start: int
) -> bool:
    if not value.endswith("]]"):
        return False
    inner_opener = value.rfind("[", 0, path_start)
    if inner_opener < 0:
        return False
    outer_opener = value.rfind("[", 0, inner_opener)
    if outer_opener < 0:
        return False
    first_inner_close = value.find("]", suffix_start)
    if (
        first_inner_close < 0
        or value[first_inner_close : first_inner_close + 2] != "]-"
    ):
        return False
    first_prefix = value[outer_opener + 1 : path_start]
    first_suffix = value[suffix_start:first_inner_close]
    if not first_prefix.endswith("before=") or first_suffix != "after=safe":
        return False
    second_start = first_inner_close + 2
    second_inner_close = len(value) - 2
    if second_start >= second_inner_close or value[second_inner_close] != "]":
        return False
    expected_second = f"{first_prefix}<ABS_PATH_0001> {first_suffix}"
    return value[second_start:second_inner_close] == expected_second


def _pytest_embedded_testcase_parameter_delimiter(
    value: str, *, start: int
) -> int | None:
    if not value.endswith("]"):
        return None
    delimiter = value.find("-<testcase>", start)
    if delimiter < 0:
        return None
    closing_tag = "</testcase>"
    closing = value.find(closing_tag, delimiter + len("-<testcase>"))
    if closing < 0:
        return None
    embedded = value[delimiter + 1 : closing + len(closing_tag)]
    if "\r" in embedded or "\n" in embedded:
        return None
    tail = value[closing + len(closing_tag) :]
    if re.fullmatch(r"(?:-[A-Za-z0-9_.@%+=~\-]+)?\]{1,2}", tail) is None:
        return None
    return delimiter


def _direct_serialized_pytest_path_span(value: str) -> tuple[int, int] | None:
    opener = value.rfind("[")
    if opener < 0:
        return None
    start = opener + 1
    delimiter = _pytest_embedded_testcase_parameter_delimiter(value, start=start)
    if delimiter is None:
        return None
    candidate = value[start:delimiter]
    if not candidate or any(character in candidate for character in "<>\"'"):
        return None
    decoded_candidate = candidate.replace("\\\\", "\\")
    if not (
        _is_absolute_component(decoded_candidate)
        or re.match(r"(?i)^file:/+(?=[^/\s])", decoded_candidate)
        or re.match(r"^\\{2,}[^\\/\s]+\\+[^\\/\s]+", candidate)
    ):
        return None
    return start, delimiter


def _direct_serialized_pytest_public_path_span(
    value: str,
) -> tuple[int, int] | None:
    opener = value.rfind("[")
    if opener < 0:
        return None
    start = opener + 1
    delimiter = _pytest_embedded_testcase_parameter_delimiter(value, start=start)
    if delimiter is None:
        return None
    candidate = value[start:delimiter]
    occurrence = ALLOWED_PLACEHOLDER_PATH_RE.match(candidate + " ")
    if not (
        occurrence is not None
        and occurrence.start() == 0
        and occurrence.end() == len(candidate)
    ):
        return None
    return start, delimiter


def _is_direct_serialized_pytest_public_placeholder(
    value: str, *, start: int, end: int
) -> bool:
    public_path_span = _direct_serialized_pytest_public_path_span(value)
    return (
        public_path_span is not None
        and start == public_path_span[0]
        and start < end <= public_path_span[1]
    )


def _xml_semantic_path_end(
    value: str,
    start: int,
    prefix_end: int,
    *,
    junit_testcase_name: bool,
) -> int:
    quote = ""
    if start >= 2 and value[start - 2 : start] in {'="', "='"}:
        quote = value[start - 1]
    if quote:
        end = value.find(quote, prefix_end)
        if end < 0:
            raise ValueError("ambiguous XML absolute path boundary")
        return end

    opener = value[start - 1] if start else ""
    closer = XML_SEMANTIC_PATH_OPENERS.get(opener)
    if closer:
        end = value.find(closer, prefix_end)
        if end < 0:
            raise ValueError("ambiguous XML absolute path boundary")
        return end

    whole_string = start == 0 and all(
        character not in value
        for character in (*XML_SEMANTIC_PATH_CLOSERS, "[", "(", "{")
    )
    end = prefix_end
    while end < len(value):
        character = value[end]
        if character in XML_SEMANTIC_PATH_CLOSERS or character in {'"', "'", "<", ">"}:
            break
        if character.isspace():
            if whole_string:
                return len(value)
            next_start = end
            while next_start < len(value) and value[next_start].isspace():
                next_start += 1
            remainder = value[next_start:]
            candidate_pattern = (
                XML_SEMANTIC_PYTEST_PATH_END_RE
                if junit_testcase_name
                else XML_SEMANTIC_BARE_PATH_END_RE
            )
            candidate = candidate_pattern.match(remainder)
            if candidate is None:
                break
            candidate_text = candidate.group(0)
            if "=" in candidate_text and not any(
                separator in candidate_text for separator in ("/", "\\")
            ):
                if junit_testcase_name and _is_final_pytest_parameter_assignment_suffix(
                    value, path_start=start, suffix_start=next_start
                ):
                    return end
                if junit_testcase_name and _is_mirrored_pytest_input_expected_boundary(
                    value, path_start=start, suffix_start=next_start
                ):
                    return end
                raise ValueError("ambiguous XML absolute path boundary")
            if "." not in candidate_text and not any(
                separator in candidate_text for separator in ("/", "\\")
            ):
                if any(separator in value[start:end] for separator in ("/", "\\")):
                    colon_line_boundary = re.search(
                        r"\.[A-Za-z0-9]+:[0-9]+:$", value[start:end]
                    )
                    if colon_line_boundary is not None:
                        break
                    raise ValueError("ambiguous XML absolute path boundary")
                raise ValueError("ambiguous XML absolute path boundary")
            end = next_start + len(candidate_text)
            continue
        end += 1
    return end


def _xml_semantic_absolute_spans(
    value: str, *, junit_testcase_name: bool = False
) -> tuple[tuple[int, int], ...]:
    direct_path_span = (
        _direct_serialized_pytest_path_span(value) if junit_testcase_name else None
    )
    direct_public_path_span = (
        _direct_serialized_pytest_public_path_span(value)
        if junit_testcase_name
        else None
    )
    closing_tag_spans = tuple(
        match.span() for match in EMBEDDED_XML_CLOSING_TAG_RE.finditer(value)
    )
    masked = _mask_equal_length(value, closing_tag_spans)
    placeholder_spans = tuple(
        match.span() for match in ALLOWED_PLACEHOLDER_PATH_RE.finditer(masked)
    )
    masked = _mask_equal_length(masked, placeholder_spans)
    direct_mask_spans = tuple(
        span for span in (direct_path_span, direct_public_path_span) if span is not None
    )
    masked = _mask_equal_length(masked, direct_mask_spans)
    candidates = ({direct_path_span} if direct_path_span is not None else set()) | {
        (
            match.start(),
            _xml_semantic_path_end(
                value,
                match.start(),
                match.end(),
                junit_testcase_name=junit_testcase_name,
            ),
        )
        for match in XML_SEMANTIC_PATH_START_RE.finditer(masked)
        if not any(start <= match.start() < end for start, end in closing_tag_spans)
        and not (
            match.group(0) == "/"
            and match.end() < len(value)
            and value[match.end()] in {'"', "'", ">"}
        )
        and not (
            match.start() > 0
            and value[match.start() - 1] == ":"
            and (
                scheme_match := XML_SEMANTIC_URI_SCHEME_RE.search(
                    value[: match.start()]
                )
            )
            is not None
            and scheme_match.group(0)[:-1].casefold() != "file"
        )
    }
    selected: list[tuple[int, int]] = []
    occupied_until = 0
    for start, end in sorted(
        candidates, key=lambda span: (span[0], -(span[1] - span[0]))
    ):
        if start < occupied_until:
            continue
        selected.append((start, end))
        occupied_until = end
    return tuple(selected)


def _json_strings(value: object) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from _json_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _json_strings(child)
    elif isinstance(value, str):
        yield value


def _known_placeholder(path: str, values: Mapping[str, object]) -> str | None:
    aliases = values.get("path_aliases", {})
    if isinstance(aliases, Mapping):
        for raw, public in aliases.items():
            if (
                _normalize_path_text(path).casefold()
                == _normalize_path_text(str(raw)).casefold()
            ):
                return str(public)
    candidates = (
        (str(values["cpu_python"]), "<CPU_PYTHON>"),
        (str(values["repo_root"]), "<REPO_ROOT>"),
        (str(values["user_home"]), "<USER_HOME>"),
    )
    normalized = _normalize_path_text(path)
    for prefix, placeholder in sorted(
        candidates, key=lambda item: len(item[0]), reverse=True
    ):
        normalized_prefix = _normalize_path_text(prefix)
        if normalized.casefold() == normalized_prefix.casefold():
            return placeholder
        if normalized.casefold().startswith(normalized_prefix.casefold() + "/"):
            suffix = normalized[len(normalized_prefix) :].lstrip("/")
            return f"{placeholder}/{suffix}"
    return None


def _collect_unknown_paths(
    payload: object,
    *,
    values: Mapping[str, object],
    xml: bool,
) -> dict[str, str]:
    components: list[str] = []
    if xml:
        assert isinstance(payload, ET.Element)
        for string, junit_testcase_name in _xml_strings_with_context(payload):
            components.extend(
                string[start:end]
                for start, end in _xml_semantic_absolute_spans(
                    string, junit_testcase_name=junit_testcase_name
                )
            )
    else:
        components.extend(
            _iter_string_components(
                payload, path_separator=str(values["path_separator"])
            )
        )
    unknown = {
        _normalize_path_text(_component_core(component)).casefold(): component
        for component in components
        if _known_placeholder(_component_core(component), values) is None
        and ALLOWED_PLACEHOLDER_RE.fullmatch(_component_core(component)) is None
    }
    return {
        original: f"<ABS_PATH_{index:04d}>"
        for index, original in enumerate(sorted(unknown), start=1)
    }


def _replace_component(
    component: str,
    *,
    values: Mapping[str, object],
    unknown: Mapping[str, str],
) -> str:
    leading, quote, core, trailing = _split_component_wrapper(component)
    if ALLOWED_PLACEHOLDER_RE.fullmatch(core):
        return component
    known = _known_placeholder(core, values)
    if known is not None:
        replacement = known
    else:
        key = _normalize_path_text(core).casefold()
        replacement = unknown.get(key)
    if replacement is not None:
        return f"{leading}{quote}{replacement}{quote}{trailing}"
    return component


def _transform_string(
    value: str,
    *,
    key: str | None,
    values: Mapping[str, object],
    unknown: Mapping[str, str],
    xml_semantic: bool = False,
    junit_testcase_name: bool = False,
) -> str:
    hostname = str(values["hostname"])
    if xml_semantic:
        transformed = value
        for start, end in reversed(
            _xml_semantic_absolute_spans(value, junit_testcase_name=junit_testcase_name)
        ):
            replacement = _replace_component(
                value[start:end], values=values, unknown=unknown
            )
            transformed = transformed[:start] + replacement + transformed[end:]
        if hostname:
            transformed = re.sub(
                re.escape(hostname),
                "<HOSTNAME>",
                transformed,
                flags=re.IGNORECASE,
            )
        return transformed
    if hostname:
        value = re.sub(re.escape(hostname), "<HOSTNAME>", value, flags=re.IGNORECASE)
    if key == "PYTHONPATH":
        separator = str(values["path_separator"])
        return separator.join(
            _replace_component(component, values=values, unknown=unknown)
            if _is_absolute_component(component)
            else component
            for component in value.split(separator)
        )
    if value.startswith("--") and "=" in value:
        left, right = value.split("=", 1)
        if _is_absolute_component(right):
            return f"{left}={_replace_component(right, values=values, unknown=unknown)}"
    if _is_absolute_component(value):
        return _replace_component(value, values=values, unknown=unknown)
    transformed = WINDOWS_ABSOLUTE_RE.sub(
        lambda match: _replace_component(
            match.group(0), values=values, unknown=unknown
        ),
        value,
    )
    transformed = POSIX_ABSOLUTE_RE.sub(
        lambda match: _replace_component(
            match.group(0), values=values, unknown=unknown
        ),
        transformed,
    )
    return transformed


def _transform_json_value(
    value: object,
    *,
    values: Mapping[str, object],
    unknown: Mapping[str, str],
    key: str | None = None,
) -> object:
    if key in {"pid", "process_id", "worker_pid"}:
        return "<PID>"
    if isinstance(value, dict):
        transformed = {
            child_key: _transform_json_value(
                child,
                values=values,
                unknown=unknown,
                key=str(child_key),
            )
            for child_key, child in value.items()
        }
        if "cwd" in transformed:
            transformed.pop("cwd")
            repo = _replace_component(str(value["cwd"]), values=values, unknown=unknown)
            if repo != "<REPO_ROOT>":
                raise ValueError(
                    "raw command cwd must resolve exactly to repository root"
                )
            transformed["cwd_rel"] = "."
        return transformed
    if isinstance(value, list):
        return [
            _transform_json_value(child, values=values, unknown=unknown, key=key)
            for child in value
        ]
    if isinstance(value, str):
        replacements = values.get("hash_replacements", {})
        if isinstance(replacements, Mapping) and value in replacements:
            return str(replacements[value])
        return _transform_string(value, key=key, values=values, unknown=unknown)
    return value


def _canonical_xml_bytes(root: ET.Element) -> bytes:
    ET.indent(root, space="  ")
    body = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    return body.rstrip(b"\n") + b"\n"


def _junit_testcase_identity(testcase: ET.Element) -> tuple[str, str, str]:
    classname = testcase.attrib.get("classname")
    name = testcase.attrib.get("name")
    if not classname or not name:
        raise ValueError("JUnit testcase ID requires classname and name")
    return classname, name, f"{classname}::{name}"


def _identified_junit_testcases(root: ET.Element) -> list[ET.Element]:
    return [
        testcase
        for testcase in root.iter("testcase")
        if testcase.attrib.get("classname") and testcase.attrib.get("name")
    ]


def _require_unique_junit_testcase_ids(root: ET.Element) -> None:
    identifiers = [
        _junit_testcase_identity(testcase)[2]
        for testcase in _identified_junit_testcases(root)
    ]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("duplicate testcase ID in JUnit privacy transform")


def _junit_public_marker(name: str) -> tuple[str, int] | None:
    occurrence = PUBLIC_TCID_SUFFIX_RE.fullmatch(name)
    if occurrence is None:
        if PUBLIC_TCID_TOKEN in name:
            raise ValueError("malformed public testcase ID marker")
        return None
    base = occurrence.group(1)
    if PUBLIC_TCID_TOKEN in base:
        raise ValueError("malformed public testcase ID marker")
    return base, int(occurrence.group(2))


def _validate_public_testcase_marker_groups(testcases: Sequence[ET.Element]) -> bool:
    groups: dict[tuple[str, str], list[int | None]] = {}
    saw_marker = False
    for testcase in testcases:
        classname, name, _identifier = _junit_testcase_identity(testcase)
        marked = _junit_public_marker(name)
        if marked is None:
            base = name
            ordinal = None
        else:
            base, ordinal = marked
            saw_marker = True
        groups.setdefault((classname, base), []).append(ordinal)
    for ordinals in groups.values():
        marked = [ordinal for ordinal in ordinals if ordinal is not None]
        if not marked:
            continue
        if len(marked) != len(ordinals):
            raise ValueError("mixed public testcase ID marker group")
        if len(marked) < 2:
            raise ValueError("incomplete public testcase ID marker group")
        if sorted(marked) != list(range(1, len(marked) + 1)):
            raise ValueError("noncanonical public testcase ID marker group")
    return saw_marker


def _disambiguate_public_testcase_ids(
    testcases: Sequence[ET.Element],
    raw_identifiers: Sequence[str],
) -> None:
    if len(testcases) != len(raw_identifiers):
        raise ValueError("JUnit testcase inventory changed during privacy transform")
    if _validate_public_testcase_marker_groups(testcases):
        return
    collisions: dict[str, list[tuple[str, ET.Element]]] = {}
    for raw_identifier, testcase in zip(raw_identifiers, testcases, strict=True):
        _classname, _name, public_identifier = _junit_testcase_identity(testcase)
        collisions.setdefault(public_identifier, []).append((raw_identifier, testcase))
    if any(len(entries) > PUBLIC_TCID_MAX_ORDINAL for entries in collisions.values()):
        raise ValueError("collision group exceeds public testcase ID marker capacity")
    for entries in collisions.values():
        if len(entries) < 2:
            continue
        for ordinal, (_raw_identifier, testcase) in enumerate(
            sorted(entries, key=lambda item: item[0]),
            start=1,
        ):
            name = testcase.attrib["name"]
            testcase.attrib["name"] = f"{name}[PUBLIC_TCID_{ordinal:04d}]"


def privacy_transform_bytes(
    data: bytes,
    *,
    kind: str,
    privacy_context: Mapping[str, object],
) -> tuple[bytes, dict[str, object]]:
    values = _privacy_values(privacy_context)
    if kind == "junit":
        try:
            root = ET.fromstring(data)
        except ET.ParseError as error:
            raise ValueError(f"invalid XML privacy preimage: {error}") from error
        testcases = _identified_junit_testcases(root)
        raw_identifiers = [
            _junit_testcase_identity(testcase)[2] for testcase in testcases
        ]
        _require_unique_junit_testcase_ids(root)
        raw_has_public_markers = _validate_public_testcase_marker_groups(testcases)
        unknown = _collect_unknown_paths(root, values=values, xml=True)
        for element in root.iter():
            for key, value in tuple(element.attrib.items()):
                if key in {"pid", "process_id", "worker_pid"}:
                    element.attrib[key] = "<PID>"
                else:
                    element.attrib[key] = _transform_string(
                        value,
                        key=key,
                        values=values,
                        unknown=unknown,
                        xml_semantic=True,
                        junit_testcase_name=element.tag == "testcase" and key == "name",
                    )
            if element.text:
                element.text = _transform_string(
                    element.text,
                    key=None,
                    values=values,
                    unknown=unknown,
                    xml_semantic=True,
                )
            if element.tail:
                element.tail = _transform_string(
                    element.tail,
                    key=None,
                    values=values,
                    unknown=unknown,
                    xml_semantic=True,
                )
        transformed_identifiers = [
            _junit_testcase_identity(testcase)[2] for testcase in testcases
        ]
        if raw_has_public_markers and transformed_identifiers != raw_identifiers:
            raise ValueError(
                "marked JUnit testcase ID changed during privacy transform"
            )
        _disambiguate_public_testcase_ids(testcases, raw_identifiers)
        public = _canonical_xml_bytes(root)
        if raw_has_public_markers and public != data:
            raise ValueError("marked JUnit XML is not unchanged canonical public form")
        _require_unique_junit_testcase_ids(ET.fromstring(public))
    else:
        try:
            payload = json.loads(data)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError(f"invalid JSON privacy preimage: {error}") from error
        unknown = _collect_unknown_paths(payload, values=values, xml=False)
        transformed = _transform_json_value(payload, values=values, unknown=unknown)
        if kind == "command" and isinstance(transformed, dict):
            public_junits = values.get("junit_public_records", {})
            suite = transformed.get("id")
            if isinstance(public_junits, Mapping) and suite in public_junits:
                replacement = public_junits[suite]
                if not isinstance(replacement, Mapping) or not isinstance(
                    transformed.get("junit"), dict
                ):
                    raise ValueError("invalid command JUnit privacy replacement")
                transformed["junit"].update(replacement)
        public = canonical_json_bytes(transformed)
    assert_no_literal_absolute_path(public, privacy_context=privacy_context)
    transforms = ["structural_absolute_paths", "hostname", "process_identifiers"]
    return public, {
        "raw_sha256": _sha256(data),
        "public_sha256": _sha256(public),
        "transforms": transforms,
    }


def _assert_no_literal_absolute_path_in_string(
    value: str, *, xml_semantic: bool, junit_testcase_name: bool = False
) -> None:
    guarded = value
    if xml_semantic:
        guarded = _mask_equal_length(
            value,
            (match.span() for match in EMBEDDED_XML_CLOSING_TAG_RE.finditer(value)),
        )
    unknown_placeholders = [
        item
        for item in UNKNOWN_PLACEHOLDER_RE.findall(guarded)
        if ALLOWED_PLACEHOLDER_RE.fullmatch(item) is None
    ]
    if unknown_placeholders:
        raise ValueError(f"unknown public placeholder: {unknown_placeholders[0]}")
    for placeholder in ALLOWED_PLACEHOLDER_RE.finditer(guarded):
        occurrence = ALLOWED_PLACEHOLDER_PATH_RE.match(guarded, placeholder.start())
        if occurrence is None and not (
            junit_testcase_name
            and _is_direct_serialized_pytest_public_placeholder(
                value, start=placeholder.start(), end=placeholder.end()
            )
        ):
            raise ValueError(f"invalid public placeholder path: {placeholder.group(0)}")
    if xml_semantic:
        absolute_path_found = bool(
            _xml_semantic_absolute_spans(value, junit_testcase_name=junit_testcase_name)
        )
    else:
        scrubbed = ALLOWED_PLACEHOLDER_PATH_RE.sub("PLACEHOLDER", value)
        absolute_path_found = bool(
            WINDOWS_ABSOLUTE_RE.search(scrubbed) or POSIX_ABSOLUTE_RE.search(scrubbed)
        )
    if absolute_path_found:
        raise ValueError("literal absolute path remains in public evidence")


def assert_no_literal_absolute_path(
    data: bytes,
    *,
    privacy_context: Mapping[str, object] | None = None,
) -> None:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("public evidence is not UTF-8") from error
    semantic_strings: tuple[str, ...] | None = None
    if text.lstrip().startswith("<"):
        try:
            parser = ET.XMLParser(
                target=ET.TreeBuilder(insert_comments=True, insert_pis=True)
            )
            root = ET.fromstring(data, parser=parser)
        except ET.ParseError as error:
            raise ValueError("public evidence XML is invalid") from error
        if root.tag not in {"testsuite", "testsuites"}:
            raise ValueError("public evidence XML root is not JUnit")
        semantic_records = tuple(_xml_strings_with_context(root))
        semantic_strings = tuple(value for value, _context in semantic_records)
        for value, junit_testcase_name in semantic_records:
            _assert_no_literal_absolute_path_in_string(
                value,
                xml_semantic=True,
                junit_testcase_name=junit_testcase_name,
            )
    else:
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            _assert_no_literal_absolute_path_in_string(text, xml_semantic=False)
        else:
            semantic_strings = tuple(_json_strings(payload))
            for value in semantic_strings:
                _assert_no_literal_absolute_path_in_string(value, xml_semantic=False)
    if privacy_context is not None:
        values = _privacy_values(privacy_context)
        private_text = (
            "\n".join(semantic_strings) if semantic_strings is not None else text
        )
        for private in (
            values["repo_root"],
            values["user_home"],
            values["cpu_python"],
            values["hostname"],
        ):
            if str(private) and str(private).casefold() in private_text.casefold():
                raise ValueError("private token remains in public evidence")


def assert_public_semantics_equal(
    kind: str,
    raw: bytes,
    public: bytes,
    *,
    privacy_context: Mapping[str, object],
) -> None:
    expected, _ = privacy_transform_bytes(
        raw, kind=kind, privacy_context=privacy_context
    )
    if expected != public:
        raise ValueError("raw/public semantic comparison failed")


def _validate_snapshot_payload(snapshot: object) -> list[dict[str, object]]:
    if not isinstance(snapshot, dict):
        raise ValueError("verification snapshot must be an object")
    _require_closed_fields(
        snapshot,
        {"schema_version", "canonical_relative_root", "active_path_policy", "files"},
        label="verification snapshot",
    )
    if snapshot["schema_version"] != "verification-contract-v1":
        raise ValueError("verification snapshot schema_version mismatch")
    if snapshot["canonical_relative_root"] != ".codex/skills/verification":
        raise ValueError("verification snapshot canonical root mismatch")
    if (
        snapshot["active_path_policy"]
        != "skill_plus_references_schemas_and_scripts_without_caches"
    ):
        raise ValueError("verification snapshot active path policy mismatch")
    files = _validate_file_inventory(
        snapshot["files"], label="verification snapshot files"
    )
    if tuple(item["path"] for item in files) != EXPECTED_VERIFICATION_ACTIVE_PATHS:
        raise ValueError("verification snapshot active paths mismatch")
    return files


def resolve_verification_gate(
    snapshot: Mapping[str, object] | Path | str,
    *,
    root: Path | str,
) -> Path:
    if isinstance(snapshot, (str, Path)):
        snapshot_data = _require_regular_unlinked_file(
            Path(snapshot), label="verification snapshot"
        )
        try:
            snapshot_payload = json.loads(snapshot_data)
        except json.JSONDecodeError as error:
            raise ValueError(f"invalid verification snapshot JSON: {error}") from error
    else:
        snapshot_payload = copy.deepcopy(snapshot)
    files = _validate_snapshot_payload(snapshot_payload)
    verification_root = Path(root).resolve(strict=True)
    if not verification_root.is_dir() or _path_is_reparse(verification_root):
        raise ValueError("verification root must be an existing non-reparse directory")
    parts = tuple(part.casefold() for part in verification_root.parts[-3:])
    if parts != (".codex", "skills", "verification"):
        raise ValueError("root is not the canonical .codex verification root")
    expected_paths = {item["path"] for item in files}
    observed_active: set[str] = set()
    for subdirectory in ("references", "schemas", "scripts"):
        directory = verification_root / subdirectory
        if not directory.is_dir() or _path_is_reparse(directory):
            raise ValueError(f"missing active verification directory: {subdirectory}")
        for path in directory.rglob("*"):
            if path.is_dir():
                if _path_is_reparse(path):
                    raise ValueError(f"verification active path is reparse: {path}")
                continue
            relative = path.relative_to(verification_root).as_posix()
            if "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            observed_active.add(relative)
    observed_active.add("SKILL.md")
    unexpected = sorted(observed_active - expected_paths)
    missing = sorted(expected_paths - observed_active)
    if unexpected:
        raise ValueError(f"unexpected active verification file: {unexpected[0]}")
    if missing:
        raise ValueError(f"missing active verification file: {missing[0]}")
    for record in files:
        relative = str(record["path"])
        data = _require_regular_unlinked_file(
            verification_root / relative, label="active verification file"
        )
        if len(data) != record["size_bytes"] or _sha256(data) != record["sha256"]:
            raise ValueError(f"verification active-file mismatch: {relative}")
    gate = verification_root / "scripts/verification_gate.py"
    return gate.resolve(strict=True)


def _validate_head_relationship(
    *,
    repo_root: Path,
    wave: str,
    evidence_stage: str,
    tested_git_head: str,
    implementation_parent_git_head: str,
    actual_head: str,
) -> None:
    _require_full_sha(tested_git_head, label="tested_git_head")
    _require_full_sha(
        implementation_parent_git_head, label="implementation_parent_git_head"
    )
    _require_full_sha(actual_head, label="actual_head")
    if evidence_stage == "candidate":
        if not (tested_git_head == implementation_parent_git_head == actual_head):
            raise ValueError(
                "candidate head must equal implementation parent and actual head"
            )
        return
    if evidence_stage != "closure":
        raise ValueError("evidence_stage must be candidate or closure")
    if tested_git_head != actual_head:
        raise ValueError("closure tested head must equal actual head")
    if implementation_parent_git_head == tested_git_head:
        raise ValueError("closure implementation parent must differ from tested head")
    actual_parent = _git(repo_root, "rev-parse", f"{actual_head}^")
    if actual_parent != implementation_parent_git_head:
        raise ValueError("closure implementation parent is not actual_head^")
    diff = _git(
        repo_root,
        "diff",
        "--name-only",
        f"{implementation_parent_git_head}..{actual_head}",
    )
    allowed_prefix = f"docs/verification/evidence/{wave}/"
    paths = tuple(path for path in str(diff).splitlines() if path)
    if not paths or any(not path.startswith(allowed_prefix) for path in paths):
        raise ValueError("closure child diff is not evidence-only")


def _validate_tested_input_policy(payload: object) -> list[dict[str, object]]:
    if not isinstance(payload, dict):
        raise ValueError("tested_input_policy must be an object")
    _require_closed_fields(
        payload,
        {"schema_version", "selection_rules", "exclusion_rules", "inputs"},
        label="tested-input policy",
    )
    _validate_policy_template(
        {
            "schema_version": payload["schema_version"],
            "selection_rules": payload["selection_rules"],
            "exclusion_rules": payload["exclusion_rules"],
        }
    )
    return _validate_file_inventory(payload["inputs"], label="tested inputs")


def _policy_template_from_resolved(
    payload: Mapping[str, object],
) -> dict[str, object]:
    return _validate_policy_template(
        {
            "schema_version": payload["schema_version"],
            "selection_rules": payload["selection_rules"],
            "exclusion_rules": payload["exclusion_rules"],
        }
    )


def _plan_path_for_wave(wave: str) -> PurePosixPath:
    if WAVE_RE.fullmatch(wave) is None:
        raise ValueError("invalid evidence wave")
    labels = {
        "wave-0": "0",
        "wave-a": "a",
        "wave-b": "b",
        "wave-c": "c",
        "wave-d0": "d",
        "wave-d1": "d",
        "wave-e": "e",
    }
    try:
        label = labels[wave]
    except KeyError as error:
        raise ValueError(f"unsupported evidence wave: {wave}") from error
    return PurePosixPath(
        "docs/superpowers/plans/"
        f"2026-08-11-scientific-integrity-remediation-wave-{label}.md"
    )


def _validate_wave_input_contract(
    *,
    wave: str,
    dependency_paths: Sequence[str],
    policy_template: Mapping[str, object],
) -> tuple[tuple[str, ...], dict[str, object]]:
    _plan_path_for_wave(wave)
    normalized_paths = tuple(
        _validate_relative_path(path, label="dependency input path")
        for path in dependency_paths
    )
    if not normalized_paths:
        raise ValueError("dependency inputs must be nonempty")
    if len(normalized_paths) != len(set(normalized_paths)):
        raise ValueError("dependency inputs contain a duplicate path")
    if len({path.casefold() for path in normalized_paths}) != len(normalized_paths):
        raise ValueError("dependency inputs contain a case-fold path alias")
    if "uv.lock" in normalized_paths:
        raise ValueError("uv.lock is not an evidence dependency")
    normalized_policy = _validate_policy_template(policy_template)
    if wave == "wave-0":
        if normalized_paths != WAVE0_DEPENDENCY_INPUT_PATHS:
            raise ValueError("wave-0 dependency paths differ from frozen contract")
        expected_policy = {
            "schema_version": TESTED_INPUT_SCHEMA,
            "selection_rules": list(TESTED_INPUT_SELECTION_RULES),
            "exclusion_rules": list(TESTED_INPUT_EXCLUSION_RULES),
        }
        if normalized_policy != expected_policy:
            raise ValueError("wave-0 tested-input policy differs from frozen contract")
    return normalized_paths, normalized_policy


def _validate_binding(record: object, *, label: str, with_commit: bool = False) -> None:
    if not isinstance(record, dict):
        raise ValueError(f"{label} must be an object")
    fields = FILE_RECORD_FIELDS | ({"commit"} if with_commit else set())
    _require_closed_fields(record, fields, label=label)
    _validate_relative_path(record["path"], label=f"{label} path")
    _require_nonnegative_int(record["size_bytes"], label=f"{label} size_bytes")
    _require_sha256(record["sha256"], label=f"{label} sha256")
    if with_commit:
        _require_full_sha(record["commit"], label=f"{label} commit")


def _read_public_evidence_tree(evidence_root: Path) -> dict[str, bytes]:
    public: dict[str, bytes] = {}
    for current, directory_names, file_names in os.walk(
        evidence_root, followlinks=False
    ):
        current_path = Path(current)
        for name in tuple(directory_names):
            directory = current_path / name
            if directory.is_symlink() or _path_is_reparse(directory):
                raise ValueError(
                    "public evidence inventory contains a reparse directory"
                )
        for name in file_names:
            path = current_path / name
            relative = path.relative_to(evidence_root).as_posix()
            _validate_relative_path(relative, label="public evidence path")
            if relative in public:
                raise ValueError("public evidence inventory contains a duplicate path")
            public[relative] = _require_regular_unlinked_file(
                path, label="public evidence"
            )
    return public


def validate_evidence_index(
    payload: Mapping[str, object],
    *,
    repo_root: Path | str,
    actual_head: str,
) -> None:
    if not isinstance(payload, dict):
        raise ValueError("evidence index must be an object")
    _require_closed_fields(payload, INDEX_ROOT_FIELDS, label="evidence-index")
    if payload["schema_version"] != "remediation-evidence-index-v1":
        raise ValueError("evidence-index schema_version mismatch")
    wave = payload["wave"]
    if not isinstance(wave, str) or WAVE_RE.fullmatch(wave) is None:
        raise ValueError("invalid evidence wave")
    stage = payload["evidence_stage"]
    if not isinstance(stage, str):
        raise ValueError("invalid evidence stage")
    root = Path(repo_root).resolve(strict=True)
    tested = _require_full_sha(payload["tested_git_head"], label="tested_git_head")
    parent = _require_full_sha(
        payload["implementation_parent_git_head"],
        label="implementation_parent_git_head",
    )
    _validate_head_relationship(
        repo_root=root,
        wave=wave,
        evidence_stage=stage,
        tested_git_head=tested,
        implementation_parent_git_head=parent,
        actual_head=actual_head,
    )
    if not isinstance(payload["platform"], dict):
        raise ValueError("platform must be an object")
    _validate_binding(payload["environment_record"], label="environment record")
    dependency_inputs = _validate_file_inventory(
        payload["dependency_inputs"],
        label="dependency inputs",
        require_sorted=False,
    )
    dependency_paths = [str(item["path"]) for item in dependency_inputs]
    if len(dependency_paths) != len(set(dependency_paths)):
        raise ValueError("dependency inputs contain a duplicate path")
    if "uv.lock" in dependency_paths:
        raise ValueError("uv.lock is not an evidence dependency")
    if not isinstance(payload["dependency_versions"], list):
        raise ValueError("dependency_versions must be an array")
    tested_inputs = _validate_tested_input_policy(payload["tested_input_policy"])
    dependency_paths, policy_template = _validate_wave_input_contract(
        wave=wave,
        dependency_paths=dependency_paths,
        policy_template=_policy_template_from_resolved(payload["tested_input_policy"]),
    )
    expected_inventory_hash = _sha256(canonical_json_bytes(tested_inputs))
    if payload["tested_input_inventory_sha256"] != expected_inventory_hash:
        raise ValueError("tested-input inventory hash mismatch")
    _validate_file_inventory(payload["commands"], label="commands")
    source_bindings = _validate_file_inventory(
        payload["source_config_bindings"], label="source/config bindings"
    )
    _validate_binding(
        payload["reviewed_plan_binding"],
        label="reviewed plan binding",
        with_commit=True,
    )
    _validate_binding(
        payload["verification_contract_binding"], label="verification contract binding"
    )
    files = _validate_file_inventory(
        payload["files"], label="evidence files", with_kind=True
    )
    paths = {str(item["path"]) for item in files}
    if not set(GENERIC_NON_INDEX_PUBLIC_PATHS).issubset(paths):
        raise ValueError("evidence index lacks the complete generic base")
    if stage == "candidate":
        evidence_root = root / f"docs/verification/evidence/{wave}/{tested[:12]}"
    elif stage == "closure":
        evidence_root = root / f"verification-evidence/{wave}/{tested[:12]}"
    else:
        raise ValueError("evidence_stage must be candidate or closure")
    if evidence_root.exists():
        public_tree = _read_public_evidence_tree(evidence_root)
        index_bytes = public_tree.pop("index.json", None)
        if index_bytes is None:
            raise ValueError("public evidence inventory lacks index.json")
        if index_bytes != canonical_json_bytes(payload):
            raise ValueError("on-disk index differs from validated index payload")
        indexed = {str(record["path"]): record for record in files}
        for path, record in indexed.items():
            data = public_tree.get(path)
            if data is None:
                raise ValueError(
                    f"public evidence inventory lacks indexed byte: {path}"
                )
            if len(data) != record["size_bytes"] or _sha256(data) != record["sha256"]:
                raise ValueError(f"indexed public byte mismatch: {path}")
        _validate_complete_public_inventory(
            index_bytes=index_bytes,
            indexed=indexed,
            actual=public_tree,
        )
        privacy_context = _generic_privacy_context(root)
        for data in public_tree.values():
            assert_no_literal_absolute_path(data, privacy_context=privacy_context)
        _validate_generic_public_records(payload, public_tree, repo_root=root)
    policy = payload["tested_input_policy"]
    assert isinstance(policy, dict)
    current_policy = _resolve_tested_input_policy(root, policy_template)
    if current_policy != payload["tested_input_policy"]:
        raise ValueError("current tested-input policy differs from evidence index")
    plan = payload["reviewed_plan_binding"]
    snapshot = payload["verification_contract_binding"]
    assert isinstance(plan, dict)
    assert isinstance(snapshot, dict)
    expected_plan_path = str(_plan_path_for_wave(wave))
    if plan["path"] != expected_plan_path:
        raise ValueError("reviewed plan path differs from evidence wave")
    source_paths = {str(item["path"]) for item in source_bindings}
    tested_by_path = {str(item["path"]): item for item in tested_inputs}
    tested_paths = set(tested_by_path)
    for required in (expected_plan_path, str(SNAPSHOT_PATH)):
        if required not in source_paths or required not in tested_paths:
            raise ValueError(f"required generic source binding missing: {required}")
    if snapshot["path"] != str(SNAPSHOT_PATH):
        raise ValueError("verification contract binding path mismatch")
    for binding in source_bindings:
        path = str(binding["path"])
        if tested_by_path.get(path) != binding:
            raise ValueError(f"source/config binding differs from tested input: {path}")
        data = _require_regular_unlinked_file(
            root / path, label="source/config binding"
        )
        if len(data) != binding["size_bytes"] or _sha256(data) != binding["sha256"]:
            raise ValueError(f"source/config binding byte mismatch: {path}")
    for label, binding in (
        ("reviewed_plan_binding", plan),
        ("verification_contract_binding", snapshot),
    ):
        data = _require_regular_unlinked_file(root / str(binding["path"]), label=label)
        if len(data) != binding["size_bytes"] or _sha256(data) != binding["sha256"]:
            raise ValueError(f"{label} byte mismatch")
    plan_commit = str(plan["commit"])
    for descendant in (tested, parent):
        if (
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", plan_commit, descendant],
                cwd=root,
                check=False,
                capture_output=True,
            ).returncode
            != 0
        ):
            raise ValueError(
                "reviewed plan commit is not an ancestor of evidence heads"
            )
    committed_plan = _git(root, "show", f"{plan_commit}:{plan['path']}", binary=True)
    if committed_plan != (root / str(plan["path"])).read_bytes():
        raise ValueError("reviewed plan blob differs from current tested plan bytes")
    snapshot_payload = json.loads((root / str(snapshot["path"])).read_bytes())
    _validate_snapshot_payload(snapshot_payload)
    for record in dependency_inputs:
        dependency_path = str(record["path"])
        if tested_by_path.get(dependency_path) != record:
            raise ValueError(
                f"dependency input differs from tested input: {dependency_path}"
            )
        data = _require_regular_unlinked_file(
            root / str(record["path"]), label="dependency input"
        )
        if len(data) != record["size_bytes"] or _sha256(data) != record["sha256"]:
            raise ValueError(f"dependency input byte mismatch: {record['path']}")


def build_evidence_index(
    *,
    repo_root: Path | str,
    wave: str,
    evidence_stage: str,
    tested_git_head: str,
    implementation_parent_git_head: str,
    command_records: Mapping[str, bytes],
    source_config_paths: Sequence[str],
    tested_input_policy: Mapping[str, object],
    environment_record_bytes: bytes,
    dependency_input_paths: Sequence[str],
    public_junit_bytes: Mapping[str, bytes],
) -> dict[str, object]:
    root = Path(repo_root).resolve(strict=True)
    actual_head = _git_head(root)
    _validate_head_relationship(
        repo_root=root,
        wave=wave,
        evidence_stage=evidence_stage,
        tested_git_head=tested_git_head,
        implementation_parent_git_head=implementation_parent_git_head,
        actual_head=actual_head,
    )
    environment_payload = json.loads(environment_record_bytes)
    if canonical_json_bytes(environment_payload) != environment_record_bytes:
        raise ValueError("environment record must be canonical JSON")
    requested_dependency_paths = [
        _validate_relative_path(path, label="dependency input path")
        for path in dependency_input_paths
    ]
    dependency_paths, policy_template = _validate_wave_input_contract(
        wave=wave,
        dependency_paths=requested_dependency_paths,
        policy_template=tested_input_policy,
    )
    resolved_policy = _resolve_tested_input_policy(root, policy_template)
    if len(dependency_paths) != len(set(dependency_paths)):
        raise ValueError("dependency input paths contain a duplicate")
    if "uv.lock" in dependency_paths:
        raise ValueError("uv.lock is not an evidence dependency")
    dependency_inputs = [
        _file_record(
            path, _require_regular_unlinked_file(root / path, label="dependency input")
        )
        for path in dependency_paths
    ]
    if environment_payload.get("dependency_inputs") != dependency_inputs:
        raise ValueError("environment dependency inputs differ from requested order")
    commands = [
        _file_record(f"commands/{suite}.json", data)
        for suite, data in sorted(command_records.items())
    ]
    source_paths = [
        _validate_relative_path(path, label="source/config input path")
        for path in source_config_paths
    ]
    if source_paths != sorted(source_paths) or len(source_paths) != len(
        set(source_paths)
    ):
        raise ValueError("source/config paths must be unique and ASCII-sorted")
    resolved_paths = {
        str(item["path"])
        for item in resolved_policy["inputs"]
        if isinstance(item, dict)
    }
    missing_dependencies = set(dependency_paths) - resolved_paths
    if missing_dependencies:
        raise ValueError(
            f"dependency input is absent from tested inputs: "
            f"{sorted(missing_dependencies)[0]}"
        )
    unknown_sources = set(source_paths) - resolved_paths
    if unknown_sources:
        raise ValueError(
            f"source/config input is absent from tested inputs: "
            f"{sorted(unknown_sources)[0]}"
        )
    plan_path = str(_plan_path_for_wave(wave))
    for required in (plan_path, str(SNAPSHOT_PATH)):
        if required not in source_paths or required not in resolved_paths:
            raise ValueError(f"required generic source binding missing: {required}")
    source_bindings = [
        _file_record(
            path,
            _require_regular_unlinked_file(root / path, label="source/config input"),
        )
        for path in source_paths
    ]
    plan_binding = _reviewed_plan_binding(
        root,
        tested_git_head,
        implementation_parent_git_head,
        wave=wave,
    )
    snapshot_data = _require_regular_unlinked_file(
        root / SNAPSHOT_PATH, label="verification snapshot"
    )
    snapshot_binding = _file_record(str(SNAPSHOT_PATH), snapshot_data)
    files: list[dict[str, object]] = []
    for suite, data in sorted(command_records.items()):
        files.append(
            {**_file_record(f"commands/{suite}.json", data), "kind": "command"}
        )
    for suite, data in sorted(public_junit_bytes.items()):
        files.append({**_file_record(f"{suite}.xml", data), "kind": "junit"})
    files.append(
        {
            **_file_record("environment.json", environment_record_bytes),
            "kind": "environment",
        }
    )
    files.sort(key=lambda item: str(item["path"]))
    return {
        "schema_version": "remediation-evidence-index-v1",
        "wave": wave,
        "evidence_stage": evidence_stage,
        "tested_git_head": tested_git_head,
        "implementation_parent_git_head": implementation_parent_git_head,
        "platform": environment_payload["platform"],
        "environment_record": _file_record(
            "environment.json", environment_record_bytes
        ),
        "dependency_versions": environment_payload["dependency_versions"],
        "dependency_inputs": dependency_inputs,
        "tested_input_policy": resolved_policy,
        "tested_input_inventory_sha256": _sha256(
            canonical_json_bytes(resolved_policy["inputs"])
        ),
        "commands": commands,
        "source_config_bindings": source_bindings,
        "reviewed_plan_binding": plan_binding,
        "verification_contract_binding": snapshot_binding,
        "files": files,
    }


def _reviewed_plan_binding(
    repo_root: Path,
    tested_git_head: str,
    implementation_parent_git_head: str,
    *,
    wave: str = "wave-0",
) -> dict[str, object]:
    path = str(_plan_path_for_wave(wave))
    data = _require_regular_unlinked_file(
        repo_root / path, label="reviewed Wave 0 plan"
    )
    commit = _git(repo_root, "log", "-n", "1", "--format=%H", "--", path)
    commit = _require_full_sha(commit, label="reviewed plan commit")
    for descendant in (tested_git_head, implementation_parent_git_head):
        result = subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, descendant],
            cwd=repo_root,
            check=False,
        )
        if result.returncode != 0:
            raise ValueError(
                "reviewed plan commit is not an ancestor of evidence heads"
            )
    committed = _git(repo_root, "show", f"{commit}:{path}", binary=True)
    assert isinstance(committed, bytes)
    if committed != data:
        raise ValueError("reviewed plan bytes differ from bound plan commit")
    return {**_file_record(path, data), "commit": commit}


def dependency_versions() -> list[dict[str, str]]:
    names: set[str] = {"numpy", "scipy", "pytest"}
    for distribution in importlib.metadata.distributions():
        if any(entry.group == "pytest11" for entry in distribution.entry_points):
            name = distribution.metadata.get("Name")
            if name:
                names.add(name)
    records = []
    for name in sorted(names, key=str.casefold):
        try:
            version = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            continue
        records.append({"name": name, "version": version})
    return records


def capture_environment_record(
    repo_root: Path | str,
    *,
    dependency_input_paths: Sequence[str],
) -> dict[str, object]:
    root = Path(repo_root).resolve(strict=True)
    environment = {key: os.environ.get(key) for key in ENVIRONMENT_KEYS}
    if environment["CUDA_VISIBLE_DEVICES"] != "-1":
        raise ValueError("CUDA_VISIBLE_DEVICES must be exactly -1")
    if environment["PYTHONHASHSEED"] != "0":
        raise ValueError("PYTHONHASHSEED must be exactly 0")
    for key in (
        "MULTIAGENTELBO_RUN_CUDA_TESTS",
        "VFE3_TEST_DEVICE",
        "CUBLAS_WORKSPACE_CONFIG",
    ):
        if environment[key] is not None:
            raise ValueError(f"CUDA opt-in environment variable must be absent: {key}")
    executable = Path(sys.executable).resolve(strict=True)
    expected = CPU_PYTHON.resolve(strict=True)
    if executable != expected:
        raise ValueError(f"CPU evidence must run under {CPU_PYTHON}")
    interpreter_data = executable.read_bytes()
    dependency_inputs = [
        _file_record(
            path,
            _require_regular_unlinked_file(root / path, label="dependency input"),
        )
        for path in dependency_input_paths
    ]
    return {
        "schema_version": "remediation-environment-v1",
        "platform": {
            "os": platform.system(),
            "release": platform.release(),
            "architecture": platform.machine(),
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
        },
        "interpreter": {
            "path": str(CPU_PYTHON),
            "version": platform.python_version(),
            "size_bytes": len(interpreter_data),
            "sha256": _sha256(interpreter_data),
        },
        "dependency_versions": dependency_versions(),
        "dependency_inputs": dependency_inputs,
        "environment_variables": environment,
    }


def _validate_command_record(payload: object, *, suite: str) -> dict[str, object]:
    if not isinstance(payload, dict):
        raise ValueError("command record must be an object")
    _require_closed_fields(payload, COMMAND_FIELDS, label="command record")
    if payload["schema_version"] != "remediation-command-record-v1":
        raise ValueError("command record schema_version mismatch")
    if payload["id"] != suite:
        raise ValueError("command record suite ID mismatch")
    if payload["cwd_rel"] != ".":
        raise ValueError("command record cwd_rel must be exactly '.'")
    if not isinstance(payload["argv"], list) or not all(
        isinstance(token, str) for token in payload["argv"]
    ):
        raise ValueError("command argv must be an ordered string array")
    if not isinstance(payload["interpreter"], dict):
        raise ValueError("command interpreter must be an object")
    _require_closed_fields(
        payload["interpreter"], INTERPRETER_FIELDS, label="command interpreter"
    )
    if payload["interpreter"]["path"] not in (str(CPU_PYTHON), "<CPU_PYTHON>"):
        raise ValueError("command interpreter path mismatch")
    _require_nonnegative_int(
        payload["interpreter"]["size_bytes"], label="interpreter size"
    )
    _require_sha256(payload["interpreter"]["sha256"], label="interpreter sha256")
    if set(payload["env_allowlist"]) != set(ENVIRONMENT_KEYS):
        raise ValueError("command environment allowlist keys mismatch")
    if isinstance(payload["exit_code"], bool) or payload["exit_code"] != 0:
        raise ValueError("command exit code must be zero")
    if not isinstance(payload["junit"], dict):
        raise ValueError("command JUnit binding must be an object")
    _require_closed_fields(payload["junit"], JUNIT_FIELDS, label="JUnit binding")
    return payload


def _generic_privacy_context(
    repo_root: Path,
    *,
    public_junits: Mapping[str, bytes] | None = None,
    raw_junit_records: Mapping[str, Mapping[str, object]] | None = None,
) -> dict[str, object]:
    context: dict[str, object] = {
        "repo_root": repo_root,
        "user_home": Path.home(),
        "cpu_python": CPU_PYTHON,
        "hostname": socket.gethostname(),
        "path_separator": os.pathsep,
        "path_aliases": {},
        "hash_replacements": {},
        "junit_public_records": {},
    }
    if public_junits is None:
        return context
    aliases: dict[str, str] = {}
    hash_replacements: dict[str, str] = {}
    public_records: dict[str, dict[str, object]] = {}
    for suite, data in sorted(public_junits.items()):
        public_record = _parse_junit_bytes(data, public_path=f"{suite}.xml")
        public_records[suite] = public_record
        if raw_junit_records is not None:
            raw_record = raw_junit_records[suite]
            aliases[str(raw_record["path"])] = f"{suite}.xml"
            hash_replacements[str(raw_record["sha256"])] = str(public_record["sha256"])
    context["path_aliases"] = aliases
    context["hash_replacements"] = hash_replacements
    context["junit_public_records"] = public_records
    return context


def _generic_mapping_record(
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


def _generic_kind_for_path(path: str) -> str:
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
    return "domain"


def _finalize_evidence_index(
    index: Mapping[str, object],
    public_files: Mapping[str, bytes],
    *,
    kinds: Mapping[str, str] | None = None,
) -> dict[str, object]:
    if "index.json" in public_files:
        raise ValueError("index finalization accepts only non-index public bytes")
    if not set(GENERIC_NON_INDEX_PUBLIC_PATHS).issubset(public_files):
        raise ValueError("index finalization lacks the complete generic base")
    finalized = copy.deepcopy(dict(index))
    finalized["files"] = [
        {
            **_file_record(path, data),
            "kind": (
                str(kinds[path])
                if kinds is not None and path in kinds
                else _generic_kind_for_path(path)
            ),
        }
        for path, data in sorted(public_files.items())
    ]
    if set(finalized) != INDEX_ROOT_FIELDS:
        raise ValueError("finalized evidence index root fields drifted")
    return finalized


def _canonical_json_object(data: bytes, *, label: str) -> dict[str, object]:
    try:
        payload = json.loads(data)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid {label} JSON: {error}") from error
    if not isinstance(payload, dict) or canonical_json_bytes(payload) != data:
        raise ValueError(f"{label} must be a canonical JSON object")
    return payload


def _iter_nested_file_bindings(value: object) -> Iterable[dict[str, object]]:
    if isinstance(value, dict):
        path_key = (
            "path"
            if FILE_RECORD_FIELDS.issubset(value)
            else ("name" if {"name", "size_bytes", "sha256"}.issubset(value) else None)
        )
        if path_key is not None:
            path = _validate_relative_path(
                value[path_key], label="domain artifact path"
            )
            size = _require_nonnegative_int(
                value["size_bytes"], label="domain artifact size_bytes"
            )
            digest = _require_sha256(value["sha256"], label="domain artifact sha256")
            yield {"path": path, "size_bytes": size, "sha256": digest}
            return
        for child in value.values():
            yield from _iter_nested_file_bindings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_nested_file_bindings(child)


def _validate_complete_public_inventory(
    *,
    index_bytes: bytes,
    indexed: Mapping[str, Mapping[str, object]],
    actual: Mapping[str, bytes],
) -> None:
    indexed_paths = set(indexed)
    actual_paths = set(actual)
    if not indexed_paths.issubset(actual_paths):
        raise ValueError("public evidence inventory lacks an indexed byte")
    extras = actual_paths - indexed_paths
    if not extras:
        return

    index_binding = _file_record("index.json", index_bytes)
    candidates: list[tuple[str, dict[str, object]]] = []
    for path in sorted(extras):
        if not path.endswith(".json"):
            continue
        try:
            payload = _canonical_json_object(actual[path], label="one-way domain index")
        except ValueError:
            continue
        root_binding = payload.get("base_index", payload.get("root_index"))
        normalized_root = tuple(_iter_nested_file_bindings(root_binding))
        if normalized_root == (index_binding,):
            candidates.append((path, payload))
    if len(candidates) != 1:
        raise ValueError(
            "public evidence inventory has unbound or ambiguous domain extras"
        )

    domain_index_path, domain_index = candidates[0]
    covered: dict[str, dict[str, object]] = {}
    for key, value in domain_index.items():
        if key in {"base_index", "root_index"}:
            continue
        for record in _iter_nested_file_bindings(value):
            path = str(record["path"])
            existing = covered.get(path)
            if existing is not None and existing != record:
                raise ValueError("domain index contains conflicting file bindings")
            covered[path] = record
    expected_domain_paths = extras - {domain_index_path}
    if set(covered) != expected_domain_paths:
        raise ValueError("public evidence inventory domain coverage mismatch")
    for path, record in covered.items():
        data = actual[path]
        if len(data) != record["size_bytes"] or _sha256(data) != record["sha256"]:
            raise ValueError(f"domain-indexed public byte mismatch: {path}")


def _validate_generic_public_records(
    index: Mapping[str, object],
    public_files: Mapping[str, bytes],
    *,
    repo_root: Path | None = None,
) -> None:
    if not set(GENERIC_NON_INDEX_PUBLIC_PATHS).issubset(public_files):
        raise ValueError("generic public records are incomplete")
    for path in GENERIC_NON_INDEX_PUBLIC_PATHS:
        assert_no_literal_absolute_path(public_files[path])

    environment = _canonical_json_object(
        public_files["environment.json"], label="environment record"
    )
    _require_closed_fields(
        environment,
        {
            "schema_version",
            "platform",
            "interpreter",
            "dependency_versions",
            "dependency_inputs",
            "environment_variables",
        },
        label="environment record",
    )
    if environment["schema_version"] != "remediation-environment-v1":
        raise ValueError("environment schema mismatch")
    dependencies = _canonical_json_object(
        public_files["dependencies.json"], label="dependency record"
    )
    _require_closed_fields(
        dependencies,
        {"schema_version", "dependency_versions", "dependency_inputs"},
        label="dependency record",
    )
    if dependencies["schema_version"] != "remediation-dependencies-v1":
        raise ValueError("dependency schema mismatch")
    if (
        dependencies["dependency_versions"] != environment["dependency_versions"]
        or dependencies["dependency_inputs"] != environment["dependency_inputs"]
        or index["dependency_versions"] != environment["dependency_versions"]
        or index["dependency_inputs"] != environment["dependency_inputs"]
    ):
        raise ValueError("dependency input byte mismatch across public records")
    if index["platform"] != environment["platform"]:
        raise ValueError("environment platform differs from index")
    if index["environment_record"] != _file_record(
        "environment.json", public_files["environment.json"]
    ):
        raise ValueError("environment index binding mismatch")
    if repo_root is not None:
        dependency_paths = tuple(
            str(record["path"])
            for record in _validate_file_inventory(
                index["dependency_inputs"],
                label="dependency inputs",
                require_sorted=False,
            )
        )
        live_environment = capture_environment_record(
            repo_root, dependency_input_paths=dependency_paths
        )
        expected_environment, _mapping = privacy_transform_bytes(
            canonical_json_bytes(live_environment),
            kind="environment",
            privacy_context=_generic_privacy_context(repo_root),
        )
        if public_files["environment.json"] != expected_environment:
            raise ValueError(
                "public environment differs from live execution environment"
            )

    plan = _canonical_json_object(
        public_files["plan-binding.json"], label="plan binding"
    )
    _require_closed_fields(
        plan,
        {"schema_version", "path", "size_bytes", "sha256", "commit"},
        label="plan binding",
    )
    if plan["schema_version"] != f"{index['wave']}-plan-binding-v1":
        raise ValueError("plan-binding schema mismatch")
    if {key: value for key, value in plan.items() if key != "schema_version"} != index[
        "reviewed_plan_binding"
    ]:
        raise ValueError("reviewed_plan_binding byte mismatch across public records")

    commands = {
        str(record["path"]): record
        for record in _validate_file_inventory(index["commands"], label="commands")
    }
    for suite in ("full", "subsystem", "targeted"):
        junit_path = f"{suite}.xml"
        command_path = f"commands/{suite}.json"
        junit = _parse_junit_bytes(public_files[junit_path], public_path=junit_path)
        command = _validate_command_record(
            _canonical_json_object(
                public_files[command_path], label=f"{suite} command record"
            ),
            suite=suite,
        )
        if command["junit"] != junit:
            raise ValueError(f"{suite} public command JUnit binding mismatch")
        if (
            command["interpreter"] != environment["interpreter"]
            or command["env_allowlist"] != environment["environment_variables"]
        ):
            raise ValueError(f"{suite} command execution environment mismatch")
        if commands.get(command_path) != _file_record(
            command_path, public_files[command_path]
        ):
            raise ValueError(f"{suite} command index binding mismatch")

    privacy = _canonical_json_object(
        public_files["privacy-transform.json"], label="privacy transform"
    )
    _require_closed_fields(
        privacy, {"schema_version", "records"}, label="privacy transform"
    )
    if privacy["schema_version"] != "remediation-privacy-transform-v1":
        raise ValueError("privacy-transform schema mismatch")
    records = privacy["records"]
    if not isinstance(records, list):
        raise ValueError("privacy-transform records must be an array")
    public_paths: list[str] = []
    raw_paths: list[str] = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("privacy-transform record must be an object")
        _require_closed_fields(
            record,
            {
                "raw_relative_path",
                "raw_sha256",
                "public_path",
                "public_sha256",
                "transforms",
            },
            label="privacy-transform record",
        )
        raw_path = _validate_relative_path(
            record["raw_relative_path"], label="privacy raw path"
        )
        public_path = _validate_relative_path(
            record["public_path"], label="privacy public path"
        )
        _require_sha256(record["raw_sha256"], label="privacy raw sha256")
        _require_sha256(record["public_sha256"], label="privacy public sha256")
        if public_path not in public_files or record["public_sha256"] != _sha256(
            public_files[public_path]
        ):
            raise ValueError(f"privacy public byte mismatch: {public_path}")
        transforms = record["transforms"]
        if (
            not isinstance(transforms, list)
            or not transforms
            or not all(isinstance(item, str) and item for item in transforms)
        ):
            raise ValueError("privacy transforms must be a nonempty string array")
        public_paths.append(public_path)
        raw_paths.append(raw_path)
    if public_paths != sorted(public_paths):
        raise ValueError("privacy-transform records must be public-path sorted")
    if len(set(public_paths)) != len(public_paths) or len(set(raw_paths)) != len(
        raw_paths
    ):
        raise ValueError("privacy-transform records contain duplicate paths")
    if not set(GENERIC_MAPPED_PUBLIC_PATHS).issubset(public_paths):
        raise ValueError("privacy-transform generic path coverage mismatch")


def _prepare_evidence_bundle(
    *,
    repo_root: Path | str,
    wave: str,
    evidence_stage: str,
    tested_git_head: str,
    implementation_parent_git_head: str,
    command_records: Mapping[str, bytes],
    source_config_paths: Sequence[str],
    tested_input_policy: Mapping[str, object],
    dependency_input_paths: Sequence[str],
    raw_junit_bytes: Mapping[str, bytes],
    output_dir: Path | str,
    require_output_absent: bool,
) -> PreparedEvidenceBundle:
    root = Path(repo_root).resolve(strict=True)
    actual_head = _git_head(root)
    _validate_head_relationship(
        repo_root=root,
        wave=wave,
        evidence_stage=evidence_stage,
        tested_git_head=tested_git_head,
        implementation_parent_git_head=implementation_parent_git_head,
        actual_head=actual_head,
    )
    dependency_paths, policy_template = _validate_wave_input_contract(
        wave=wave,
        dependency_paths=dependency_input_paths,
        policy_template=tested_input_policy,
    )
    _resolve_tested_input_policy(root, policy_template)

    output_text = Path(output_dir).as_posix()
    _validate_relative_path(output_text, label="prepared output directory")
    expected_output = (
        f"docs/verification/evidence/{wave}/{tested_git_head[:12]}"
        if evidence_stage == "candidate"
        else f"verification-evidence/{wave}/{tested_git_head[:12]}"
    )
    if output_text != expected_output:
        raise ValueError("output directory differs from evidence stage/head")
    output = root.joinpath(*PurePosixPath(output_text).parts)
    if require_output_absent and (output.exists() or output.is_symlink()):
        raise FileExistsError("public evidence destination already exists")

    suites = {"full", "subsystem", "targeted"}
    if set(command_records) != suites or set(raw_junit_bytes) != suites:
        raise ValueError("generic preparation requires exact three-suite inputs")
    parsed_commands: dict[str, dict[str, object]] = {}
    raw_junit_records: dict[str, dict[str, object]] = {}
    for suite in sorted(suites):
        command_bytes = command_records[suite]
        junit_bytes = raw_junit_bytes[suite]
        if not isinstance(command_bytes, bytes) or not isinstance(junit_bytes, bytes):
            raise ValueError("generic raw command and JUnit inputs must be bytes")
        command_payload = _canonical_json_object(
            command_bytes, label=f"{suite} raw command record"
        )
        command = _validate_command_record(command_payload, suite=suite)
        raw_junit = command["junit"]
        assert isinstance(raw_junit, dict)
        parsed = _parse_junit_bytes(junit_bytes, public_path=str(raw_junit["path"]))
        if parsed != raw_junit:
            raise ValueError(f"{suite} raw command JUnit binding mismatch")
        parsed_commands[suite] = command
        raw_junit_records[suite] = parsed

    base_context = _generic_privacy_context(root)
    public: dict[str, bytes] = {}
    mappings: list[dict[str, object]] = []
    public_junits: dict[str, bytes] = {}
    for suite in sorted(suites):
        raw = raw_junit_bytes[suite]
        transformed, mapping = privacy_transform_bytes(
            raw, kind="junit", privacy_context=base_context
        )
        path = f"{suite}.xml"
        public_junits[suite] = transformed
        public[path] = transformed
        mappings.append(
            _generic_mapping_record(
                raw_relative_path=f"raw/{suite}.xml",
                public_path=path,
                raw=raw,
                public=transformed,
                mapping=mapping,
            )
        )

    context = _generic_privacy_context(
        root,
        public_junits=public_junits,
        raw_junit_records=raw_junit_records,
    )
    environment_payload = capture_environment_record(
        root, dependency_input_paths=dependency_paths
    )
    for suite in sorted(suites):
        command = parsed_commands[suite]
        if (
            command["env_allowlist"] != environment_payload["environment_variables"]
            or command["interpreter"] != environment_payload["interpreter"]
        ):
            raise ValueError(f"{suite} command execution environment drift")
        raw = command_records[suite]
        transformed, mapping = privacy_transform_bytes(
            raw, kind="command", privacy_context=context
        )
        public_command = _validate_command_record(
            _canonical_json_object(transformed, label=f"{suite} public command record"),
            suite=suite,
        )
        expected_junit = _parse_junit_bytes(
            public_junits[suite], public_path=f"{suite}.xml"
        )
        if public_command["junit"] != expected_junit:
            raise ValueError(f"{suite} public command JUnit binding mismatch")
        path = f"commands/{suite}.json"
        public[path] = transformed
        mappings.append(
            _generic_mapping_record(
                raw_relative_path=f"raw/{suite}.command.json",
                public_path=path,
                raw=raw,
                public=transformed,
                mapping=mapping,
            )
        )

    environment_raw = canonical_json_bytes(environment_payload)
    environment_public, mapping = privacy_transform_bytes(
        environment_raw, kind="environment", privacy_context=context
    )
    public["environment.json"] = environment_public
    mappings.append(
        _generic_mapping_record(
            raw_relative_path="generated/environment.json",
            public_path="environment.json",
            raw=environment_raw,
            public=environment_public,
            mapping=mapping,
        )
    )
    dependencies_raw = canonical_json_bytes(
        {
            "schema_version": "remediation-dependencies-v1",
            "dependency_versions": environment_payload["dependency_versions"],
            "dependency_inputs": environment_payload["dependency_inputs"],
        }
    )
    dependencies_public, mapping = privacy_transform_bytes(
        dependencies_raw, kind="dependency", privacy_context=context
    )
    public["dependencies.json"] = dependencies_public
    mappings.append(
        _generic_mapping_record(
            raw_relative_path="generated/dependencies.json",
            public_path="dependencies.json",
            raw=dependencies_raw,
            public=dependencies_public,
            mapping=mapping,
        )
    )
    plan_binding = _reviewed_plan_binding(
        root,
        tested_git_head,
        implementation_parent_git_head,
        wave=wave,
    )
    plan_raw = canonical_json_bytes(
        {"schema_version": f"{wave}-plan-binding-v1", **plan_binding}
    )
    plan_public, mapping = privacy_transform_bytes(
        plan_raw, kind="plan", privacy_context=context
    )
    public["plan-binding.json"] = plan_public
    mappings.append(
        _generic_mapping_record(
            raw_relative_path="generated/plan-binding.json",
            public_path="plan-binding.json",
            raw=plan_raw,
            public=plan_public,
            mapping=mapping,
        )
    )
    mappings.sort(key=lambda item: str(item["public_path"]))
    privacy_bytes = canonical_json_bytes(
        {
            "schema_version": "remediation-privacy-transform-v1",
            "records": mappings,
        }
    )
    assert_no_literal_absolute_path(privacy_bytes, privacy_context=context)
    public["privacy-transform.json"] = privacy_bytes
    if set(public) != set(GENERIC_NON_INDEX_PUBLIC_PATHS):
        raise ValueError("generic preparation path contract mismatch")

    index = build_evidence_index(
        repo_root=root,
        wave=wave,
        evidence_stage=evidence_stage,
        tested_git_head=tested_git_head,
        implementation_parent_git_head=implementation_parent_git_head,
        command_records={
            suite: public[f"commands/{suite}.json"] for suite in sorted(suites)
        },
        source_config_paths=source_config_paths,
        tested_input_policy=policy_template,
        environment_record_bytes=public["environment.json"],
        dependency_input_paths=dependency_paths,
        public_junit_bytes={suite: public[f"{suite}.xml"] for suite in sorted(suites)},
    )
    finalized = _finalize_evidence_index(index, public)
    index_bytes = canonical_json_bytes(finalized)
    assert_no_literal_absolute_path(index_bytes)
    complete = {**public, "index.json": index_bytes}
    bundle = PreparedEvidenceBundle(
        PurePosixPath(output_text),
        tuple(
            PreparedEvidenceFile(PurePosixPath(path), data)
            for path, data in sorted(complete.items())
        ),
    )
    _validate_detached_bundle(bundle, repo_root=root)
    if require_output_absent:
        validate_evidence_index(finalized, repo_root=root, actual_head=actual_head)
    return bundle


def prepare_evidence_bundle(
    *,
    repo_root: Path | str,
    wave: str,
    evidence_stage: str,
    tested_git_head: str,
    implementation_parent_git_head: str,
    command_records: Mapping[str, bytes],
    source_config_paths: Sequence[str],
    tested_input_policy: Mapping[str, object],
    dependency_input_paths: Sequence[str],
    raw_junit_bytes: Mapping[str, bytes],
    output_dir: Path | str,
) -> PreparedEvidenceBundle:
    return _prepare_evidence_bundle(
        repo_root=repo_root,
        wave=wave,
        evidence_stage=evidence_stage,
        tested_git_head=tested_git_head,
        implementation_parent_git_head=implementation_parent_git_head,
        command_records=command_records,
        source_config_paths=source_config_paths,
        tested_input_policy=tested_input_policy,
        dependency_input_paths=dependency_input_paths,
        raw_junit_bytes=raw_junit_bytes,
        output_dir=output_dir,
        require_output_absent=True,
    )


def _validate_detached_bundle(
    bundle: PreparedEvidenceBundle,
    *,
    repo_root: Path | str | None = None,
) -> dict[str, object]:
    if not isinstance(bundle.output_dir, PurePosixPath):
        raise ValueError("prepared output_dir must be PurePosixPath")
    _validate_relative_path(str(bundle.output_dir), label="prepared output directory")
    paths = [str(item.path) for item in bundle.files]
    if paths != sorted(paths):
        raise ValueError("prepared files must be ASCII-path-sorted")
    if len({path.casefold() for path in paths}) != len(paths):
        raise ValueError("prepared files contain a case-fold alias")
    resolved_root = (
        Path(repo_root).resolve(strict=True) if repo_root is not None else None
    )
    privacy_context = (
        _generic_privacy_context(resolved_root) if resolved_root is not None else None
    )
    for item in bundle.files:
        _validate_relative_path(str(item.path), label="prepared file path")
        if not isinstance(item.data, bytes):
            raise ValueError(
                "prepared evidence buffers must be detached immutable bytes"
            )
        assert_no_literal_absolute_path(item.data, privacy_context=privacy_context)
    try:
        index_file = next(
            item for item in bundle.files if str(item.path) == "index.json"
        )
    except StopIteration as error:
        raise ValueError("prepared evidence bundle lacks index.json") from error
    try:
        payload = json.loads(index_file.data)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid prepared index JSON: {error}") from error
    if canonical_json_bytes(payload) != index_file.data:
        raise ValueError("prepared index is not canonical JSON")
    if not isinstance(payload, dict):
        raise ValueError("prepared index must be an object")
    _require_closed_fields(payload, INDEX_ROOT_FIELDS, label="evidence-index")
    files = _validate_file_inventory(
        payload["files"], label="evidence files", with_kind=True
    )
    indexed = {str(record["path"]): record for record in files}
    actual = {
        str(item.path): item for item in bundle.files if str(item.path) != "index.json"
    }
    if not set(GENERIC_NON_INDEX_PUBLIC_PATHS).issubset(indexed):
        raise ValueError("prepared index lacks the complete generic base")
    for path, record in indexed.items():
        data = actual[path].data
        if len(data) != record["size_bytes"] or _sha256(data) != record["sha256"]:
            raise ValueError(f"prepared indexed byte mismatch: {path}")
    _validate_complete_public_inventory(
        index_bytes=index_file.data,
        indexed=indexed,
        actual={path: item.data for path, item in actual.items()},
    )
    if payload["evidence_stage"] not in {"candidate", "closure"}:
        raise ValueError("invalid prepared evidence stage")
    _validate_generic_public_records(
        payload,
        {path: item.data for path, item in actual.items()},
        repo_root=resolved_root,
    )
    return payload


def publish_evidence_bundle(
    bundle: PreparedEvidenceBundle,
    *,
    repo_root: Path | str,
) -> Path:
    root = Path(repo_root).resolve(strict=True)
    payload = _validate_detached_bundle(bundle, repo_root=root)
    validate_evidence_index(payload, repo_root=root, actual_head=_git_head(root))
    stage = payload["evidence_stage"]
    tested = str(payload["tested_git_head"])
    wave = str(payload["wave"])
    expected_output = (
        f"docs/verification/evidence/{wave}/{tested[:12]}"
        if stage == "candidate"
        else f"verification-evidence/{wave}/{tested[:12]}"
    )
    if str(bundle.output_dir) != expected_output:
        raise ValueError("prepared output directory differs from index stage/head")
    output = root.joinpath(*bundle.output_dir.parts)
    if output.exists() or output.is_symlink():
        raise FileExistsError(
            f"evidence destination already exists: {bundle.output_dir}"
        )
    current = output.parent
    while current != root:
        if current.exists() and _path_is_reparse(current):
            raise ValueError(f"evidence destination ancestor is reparse: {current}")
        current = current.parent
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() or output.is_symlink():
        raise FileExistsError(
            f"evidence destination appeared before publication: {bundle.output_dir}"
        )
    sibling = output.parent / f".{output.name}.tmp-{uuid.uuid4().hex}"
    if sibling.exists():
        raise FileExistsError(f"evidence publication sibling exists: {sibling}")
    try:
        sibling.mkdir()
        non_index = [item for item in bundle.files if str(item.path) != "index.json"]
        index = next(item for item in bundle.files if str(item.path) == "index.json")
        for item in [*non_index, index]:
            destination = sibling.joinpath(*item.path.parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(item.data)
            if destination.read_bytes() != item.data:
                raise OSError(f"published byte re-read mismatch: {item.path}")
        if output.exists() or output.is_symlink():
            raise FileExistsError("evidence destination appeared during publication")
        sibling.rename(output)
    except BaseException:
        if sibling.exists() and sibling.parent == output.parent:
            shutil.rmtree(sibling)
        raise
    return output


def _atomic_write_absent(path: Path, data: bytes) -> None:
    if path.exists() or path.is_symlink():
        raise FileExistsError(f"refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if path.exists() or path.is_symlink():
            raise FileExistsError(f"refusing to overwrite existing file: {path}")
        temporary.rename(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def run_junit_command(
    *,
    repo_root: Path,
    record_path: Path,
    junit_path: Path,
    argv: Sequence[str],
    junit_argument: str | None = None,
) -> int:
    if not argv or argv[0] != str(CPU_PYTHON):
        raise ValueError(f"run-junit interpreter must be exactly {CPU_PYTHON}")
    expected_junit_token = f"--junitxml={junit_path}"
    if junit_argument is not None:
        expected_junit_token = "--junitxml=" + junit_argument
    if argv.count(expected_junit_token) != 1:
        raise ValueError(
            "run-junit argv must contain the exact raw --junitxml path token"
        )
    if record_path.exists() or record_path.is_symlink():
        raise FileExistsError("run-junit record already exists")
    if junit_path.exists() or junit_path.is_symlink():
        raise FileExistsError("run-junit JUnit already exists")
    environment = capture_environment_record(
        repo_root,
        dependency_input_paths=(
            "pyproject.toml",
            "environments/cuda-rtx5090-cu128.lock.txt",
            str(SNAPSHOT_PATH),
        ),
    )
    started = _utc_now()
    result = subprocess.run(
        list(argv),
        cwd=repo_root,
        shell=False,
        check=False,
    )
    ended = _utc_now()
    if not junit_path.is_file():
        raise ValueError("run-junit command did not produce the required JUnit XML")
    junit = parse_junit(junit_path)
    interpreter = environment["interpreter"]
    assert isinstance(interpreter, dict)
    payload = {
        "schema_version": "remediation-command-record-v1",
        "id": record_path.name.removesuffix(".command.json"),
        "argv": list(argv),
        "cwd_rel": ".",
        "interpreter": interpreter,
        "env_allowlist": environment["environment_variables"],
        "started_utc": started,
        "ended_utc": ended,
        "exit_code": result.returncode,
        "junit": junit,
    }
    _atomic_write_absent(record_path, canonical_json_bytes(payload))
    return result.returncode


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build and validate remediation evidence"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser("run-junit")
    run.add_argument("--record", required=True)
    run.add_argument("--junit", required=True)
    run.add_argument("argv", nargs=argparse.REMAINDER)
    validate = subparsers.add_parser("validate")
    validate.add_argument("index")
    validate.add_argument("--cwd", default=".")
    resolve = subparsers.add_parser("resolve-verification-gate")
    resolve.add_argument("--snapshot", required=True)
    resolve.add_argument("--root", required=True)
    return parser


def _main(argv: Sequence[str] | None = None) -> int:
    arguments = create_parser().parse_args(argv)
    if arguments.command == "run-junit":
        if not arguments.argv or arguments.argv[0] != "--":
            raise ValueError("run-junit requires the literal '--' argv separator")
        repo_root = Path.cwd().resolve(strict=True)
        record = Path(arguments.record)
        junit = Path(arguments.junit)
        if not record.is_absolute():
            record = repo_root / record
        if not junit.is_absolute():
            junit = repo_root / junit
        return run_junit_command(
            repo_root=repo_root,
            record_path=record,
            junit_path=junit,
            argv=arguments.argv[1:],
            junit_argument=arguments.junit,
        )
    if arguments.command == "validate":
        repo_root = Path(arguments.cwd).resolve(strict=True)
        index = Path(arguments.index)
        if not index.is_absolute():
            index = repo_root / index
        data = _require_regular_unlinked_file(index, label="evidence index")
        payload = json.loads(data)
        if canonical_json_bytes(payload) != data:
            raise ValueError("evidence index is not canonical JSON")
        validate_evidence_index(
            payload, repo_root=repo_root, actual_head=_git_head(repo_root)
        )
        return 0
    if arguments.command == "resolve-verification-gate":
        gate = resolve_verification_gate(arguments.snapshot, root=arguments.root)
        print(gate)
        return 0
    raise AssertionError(f"unhandled command: {arguments.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(_main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2) from error
