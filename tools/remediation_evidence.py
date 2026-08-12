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
    r"(?:/(?!\.{1,2}(?:/|:|$))[A-Za-z0-9_.@%+=,~-]+)*(?::[0-9]+)?"
    r"|<(?:CPU_PYTHON|HOSTNAME|PID|ABS_PATH_\d{4})>)"
)
WINDOWS_ABSOLUTE_RE = re.compile(
    r"(?i)(?:\\\\\?\\[A-Z]:\\|\\\\[^\\/\s\"'<>;]+\\[^\\/\s\"'<>;]+\\|[A-Z]:[\\/])[^\s\"'<>;]*"
)
POSIX_ABSOLUTE_RE = re.compile(r"(?<![A-Za-z0-9_.><\-])/(?![/\s\"'<>;])[^\s\"'<>;]*")
SHA256_RE = re.compile(r"[0-9a-f]{64}")
FULL_SHA_RE = re.compile(r"[0-9a-f]{40}")


XML_SEMANTIC_POSIX_ABSOLUTE_RE = re.compile(
    r"(?<![A-Za-z0-9_./\-])/(?![/\s\x22\x27<>;])[^\s\x22\x27<>;]*"
)
EMBEDDED_XML_CLOSING_TAG_RE = re.compile(r"</[A-Za-z_:][A-Za-z0-9_.:\-]*\s*>")


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


def _is_selected_tested_input(path: str) -> bool:
    if any(_matches_rule(path, rule) for rule in TESTED_INPUT_EXCLUSION_RULES):
        return False
    return any(_matches_rule(path, rule) for rule in TESTED_INPUT_SELECTION_RULES)


def _nul_paths(data: bytes) -> tuple[str, ...]:
    values = []
    for item in data.split(b"\0"):
        if item:
            values.append(item.decode("utf-8"))
    return tuple(values)


def resolve_tested_input_policy(repo_root: Path | str) -> dict[str, object]:
    root = Path(repo_root).resolve(strict=True)
    tracked = _nul_paths(_git(root, "ls-files", "-z", binary=True))
    untracked = _nul_paths(
        _git(root, "ls-files", "--others", "--exclude-standard", "-z", binary=True)
    )
    matching_untracked = sorted(
        path for path in untracked if _is_selected_tested_input(path)
    )
    if matching_untracked:
        raise ValueError(f"untracked tested input: {matching_untracked[0]}")
    selected = sorted(path for path in tracked if _is_selected_tested_input(path))
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
        "schema_version": TESTED_INPUT_SCHEMA,
        "selection_rules": list(TESTED_INPUT_SELECTION_RULES),
        "exclusion_rules": list(TESTED_INPUT_EXCLUSION_RULES),
        "inputs": inputs,
    }


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
        if with_kind and (not isinstance(item["kind"], str) or not item["kind"]):
            raise ValueError(f"{label} kind must be nonempty")
        paths.append(path)
        records.append(item)
    if require_sorted and paths != sorted(paths):
        raise ValueError(f"{label} must be ASCII-path-sorted")
    if len({path.casefold() for path in paths}) != len(paths):
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


def _xml_strings(root: ET.Element) -> Iterable[str]:
    for element in root.iter():
        yield from element.attrib.values()
        if element.text:
            yield element.text
        if element.tail:
            yield element.tail


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
        for string in _xml_strings(payload):
            components.extend(
                _iter_string_components(
                    string, path_separator=str(values["path_separator"])
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
) -> str:
    if value == values["hostname"]:
        return "<HOSTNAME>"
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
        unknown = _collect_unknown_paths(root, values=values, xml=True)
        for element in root.iter():
            for key, value in tuple(element.attrib.items()):
                if key in {"pid", "process_id", "worker_pid"}:
                    element.attrib[key] = "<PID>"
                else:
                    element.attrib[key] = _transform_string(
                        value, key=key, values=values, unknown=unknown
                    )
            if element.text:
                element.text = _transform_string(
                    element.text, key=None, values=values, unknown=unknown
                )
            if element.tail:
                element.tail = _transform_string(
                    element.tail, key=None, values=values, unknown=unknown
                )
        public = _canonical_xml_bytes(root)
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
    assert_no_literal_absolute_path(public)
    transforms = ["structural_absolute_paths", "hostname", "process_identifiers"]
    return public, {
        "raw_sha256": _sha256(data),
        "public_sha256": _sha256(public),
        "transforms": transforms,
    }


def _assert_no_literal_absolute_path_in_string(
    value: str, *, xml_semantic: bool
) -> None:
    unknown_placeholders = [
        item
        for item in UNKNOWN_PLACEHOLDER_RE.findall(value)
        if ALLOWED_PLACEHOLDER_RE.fullmatch(item) is None
    ]
    if unknown_placeholders:
        raise ValueError(f"unknown public placeholder: {unknown_placeholders[0]}")
    if xml_semantic:
        scrubbed = ALLOWED_PLACEHOLDER_PATH_RE.sub("PLACEHOLDER", value)
        scrubbed = EMBEDDED_XML_CLOSING_TAG_RE.sub("XML_CLOSING_TAG", scrubbed)
        posix_pattern = XML_SEMANTIC_POSIX_ABSOLUTE_RE
    else:
        scrubbed = ALLOWED_PLACEHOLDER_RE.sub("PLACEHOLDER", value)
        posix_pattern = POSIX_ABSOLUTE_RE
    if WINDOWS_ABSOLUTE_RE.search(scrubbed) or posix_pattern.search(scrubbed):
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
        semantic_strings = tuple(_xml_strings(root))
        for value in semantic_strings:
            _assert_no_literal_absolute_path_in_string(value, xml_semantic=True)
    else:
        _assert_no_literal_absolute_path_in_string(text, xml_semantic=False)
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
    if payload["schema_version"] != TESTED_INPUT_SCHEMA:
        raise ValueError("tested-input schema mismatch")
    if payload["selection_rules"] != list(TESTED_INPUT_SELECTION_RULES):
        raise ValueError("tested-input selection rules mismatch")
    if payload["exclusion_rules"] != list(TESTED_INPUT_EXCLUSION_RULES):
        raise ValueError("tested-input exclusion rules mismatch")
    return _validate_file_inventory(payload["inputs"], label="tested inputs")


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
    if not isinstance(wave, str) or not re.fullmatch(r"wave-[0-9]+", wave):
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
    _validate_file_inventory(
        payload["dependency_inputs"],
        label="dependency inputs",
        require_sorted=False,
    )
    if not isinstance(payload["dependency_versions"], list):
        raise ValueError("dependency_versions must be an array")
    tested_inputs = _validate_tested_input_policy(payload["tested_input_policy"])
    expected_inventory_hash = _sha256(canonical_json_bytes(tested_inputs))
    if payload["tested_input_inventory_sha256"] != expected_inventory_hash:
        raise ValueError("tested-input inventory hash mismatch")
    _validate_file_inventory(payload["commands"], label="commands")
    _validate_file_inventory(
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
    complete_paths = paths | {"index.json"}
    from tools.build_wave0_evidence import (
        CANDIDATE_PUBLIC_PATHS,
        CLOSURE_PUBLIC_PATHS_BY_TARGET,
    )

    if stage == "candidate":
        if complete_paths != set(CANDIDATE_PUBLIC_PATHS):
            raise ValueError("candidate public path contract mismatch")
        evidence_root = root / f"docs/verification/evidence/{wave}/{tested[:12]}"
    else:
        matching_targets = [
            target
            for target, expected in CLOSURE_PUBLIC_PATHS_BY_TARGET.items()
            if complete_paths == set(expected)
        ]
        if len(matching_targets) != 1:
            raise ValueError("closure public path contract mismatch")
        evidence_root = root / f"verification-evidence/{wave}/{tested[:12]}"
    if evidence_root.exists():
        for record in files:
            path = evidence_root / str(record["path"])
            data = _require_regular_unlinked_file(path, label="indexed public evidence")
            if len(data) != record["size_bytes"] or _sha256(data) != record["sha256"]:
                raise ValueError(f"indexed public byte mismatch: {record['path']}")
            assert_no_literal_absolute_path(data)
    current_policy = resolve_tested_input_policy(root)
    if current_policy != payload["tested_input_policy"]:
        raise ValueError("current tested-input policy differs from evidence index")
    plan = payload["reviewed_plan_binding"]
    snapshot = payload["verification_contract_binding"]
    assert isinstance(plan, dict)
    assert isinstance(snapshot, dict)
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
    dependency_paths = [str(item["path"]) for item in payload["dependency_inputs"]]
    expected_dependency_paths = [
        "pyproject.toml",
        "environments/cuda-rtx5090-cu128.lock.txt",
        str(SNAPSHOT_PATH),
    ]
    if dependency_paths != expected_dependency_paths or "uv.lock" in dependency_paths:
        raise ValueError("dependency input path contract mismatch")
    for record in payload["dependency_inputs"]:
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
    resolved_policy = resolve_tested_input_policy(root)
    if dict(tested_input_policy) != resolved_policy:
        raise ValueError(
            "caller-supplied tested-input policy differs from canonical resolution"
        )
    environment_payload = json.loads(environment_record_bytes)
    dependency_inputs = [
        _file_record(
            path, _require_regular_unlinked_file(root / path, label="dependency input")
        )
        for path in dependency_input_paths
    ]
    commands = [
        _file_record(f"commands/{suite}.json", data)
        for suite, data in sorted(command_records.items())
    ]
    source_bindings = [
        _file_record(
            path,
            _require_regular_unlinked_file(root / path, label="source/config input"),
        )
        for path in sorted(source_config_paths)
    ]
    plan_binding = _reviewed_plan_binding(
        root, tested_git_head, implementation_parent_git_head
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
) -> dict[str, object]:
    path = str(PLAN_PATH)
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


def _validate_detached_bundle(bundle: PreparedEvidenceBundle) -> dict[str, object]:
    if not isinstance(bundle.output_dir, PurePosixPath):
        raise ValueError("prepared output_dir must be PurePosixPath")
    _validate_relative_path(str(bundle.output_dir), label="prepared output directory")
    paths = [str(item.path) for item in bundle.files]
    if paths != sorted(paths):
        raise ValueError("prepared files must be ASCII-path-sorted")
    if len({path.casefold() for path in paths}) != len(paths):
        raise ValueError("prepared files contain a case-fold alias")
    for item in bundle.files:
        _validate_relative_path(str(item.path), label="prepared file path")
        if not isinstance(item.data, bytes):
            raise ValueError(
                "prepared evidence buffers must be detached immutable bytes"
            )
        assert_no_literal_absolute_path(item.data)
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
    if set(indexed) != set(actual):
        raise ValueError("prepared bundle path set differs from index")
    for path, record in indexed.items():
        data = actual[path].data
        if len(data) != record["size_bytes"] or _sha256(data) != record["sha256"]:
            raise ValueError(f"prepared indexed byte mismatch: {path}")
    from tools.build_wave0_evidence import (
        CANDIDATE_PUBLIC_PATHS,
        CLOSURE_PUBLIC_PATHS_BY_TARGET,
    )

    all_paths = set(actual) | {"index.json"}
    if payload["evidence_stage"] == "candidate":
        if all_paths != set(CANDIDATE_PUBLIC_PATHS):
            raise ValueError("candidate public path contract mismatch")
    elif payload["evidence_stage"] == "closure":
        if all_paths not in [
            set(paths) for paths in CLOSURE_PUBLIC_PATHS_BY_TARGET.values()
        ]:
            raise ValueError("closure public path contract mismatch")
    else:
        raise ValueError("invalid prepared evidence stage")
    return payload


def publish_evidence_bundle(
    bundle: PreparedEvidenceBundle,
    *,
    repo_root: Path | str,
) -> Path:
    payload = _validate_detached_bundle(bundle)
    root = Path(repo_root).resolve(strict=True)
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
