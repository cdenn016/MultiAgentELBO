"""Real temporary-tree mutation contract for fail-closed manifest binding."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess

import pytest


RUNNER_PATH = Path(__file__).resolve().parents[1] / "run_checks.py"
SYNTHETIC_PROTOCOL_PROFILE = "synthetic-test-fixture-v1"
DEPENDENCY_PINS = {
    "numpy": "2.4.4",
    "scipy": "1.17.1",
    "sympy": "1.14.0",
    "mpmath": "1.3.0",
    "pypdf": "6.12.2",
    "pytest": "9.0.2",
}
PINNED_REQUIREMENTS = "".join(
    f"{name}=={version}\n" for name, version in DEPENDENCY_PINS.items()
).encode("ascii")
BOUND_FILES = (
    "manuscripts/gauge_vfe_rg/main.tex", "manuscripts/gauge_vfe_rg/chapters/child.tex", "manuscripts/gauge_vfe_rg/SPEC.md", "manuscripts/references.bib", "manuscripts/gauge_vfe_rg/scientific_report.sty", "manuscripts/scientific_report.sty", "manuscripts/gauge_vfe_rg/build.ps1", "manuscripts/gauge_vfe_rg/verification/claims.json", "manuscripts/gauge_vfe_rg/verification/run_checks.py", "manuscripts/gauge_vfe_rg/verification/requirements.txt", "manuscripts/gauge_vfe_rg/verification/VERIFICATION.md", "manuscripts/gauge_vfe_rg/verification/result.schema.json", "manuscripts/gauge_vfe_rg/verification/manifest-policy.json", "manuscripts/gauge_vfe_rg/verification/lifecycle_gate.py", "manuscripts/gauge_vfe_rg/verification/build_audit.py", "manuscripts/gauge_vfe_rg/verification/build_bootstrap_reference.ps1.txt", "manuscripts/gauge_vfe_rg/verification/build_bootstrap_transport.txt", "manuscripts/gauge_vfe_rg/verification/tests/test_factorization_gap.py", "manuscripts/gauge_vfe_rg/verification/tests/test_runner_cli.py", "manuscripts/gauge_vfe_rg/verification/tests/test_manifest_binding.py", "manuscripts/gauge_vfe_rg/verification/tests/test_lifecycle_gate.py", "manuscripts/gauge_vfe_rg/verification/tests/test_build_audit.py", "manuscripts/gauge_vfe_rg/verification/tests/test_build_bootstrap.py",
)
TEST_RESULT_SCHEMA = {
    "type": "object",
    "required": ["schema_version", "protocol_profile", "generated_at_utc", "source_revision", "source_dirty", "overall_status", "environment", "manifest", "checks", "semantic_payload_digest"],
    "additionalProperties": False,
    "properties": {
        "schema_version": {"const": "3.0"},
        "protocol_profile": {"const": SYNTHETIC_PROTOCOL_PROFILE},
        "generated_at_utc": {"type": "string", "pattern": r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"},
        "source_revision": {"type": "string", "pattern": r"[0-9a-f]{40}"},
        "source_dirty": {"const": False},
        "overall_status": {"enum": ["PASS", "FAIL"]},
        "environment": {
            "type": "object",
            "required": [
                "python",
                "python_executable",
                "python_executable_sha256",
                "git_executable",
                "git_executable_sha256",
                "platform",
                "machine",
                "dependencies",
                "dependency_provenance",
            ],
            "additionalProperties": False,
            "properties": {
                "python": {"type": "string"}, "python_executable": {"type": "string"},
                "python_executable_sha256": {"type": "string", "pattern": r"[0-9a-f]{64}"},
                "git_executable": {"type": "string"},
                "git_executable_sha256": {"type": "string", "pattern": r"[0-9a-f]{64}"},
                "platform": {"type": "string"}, "machine": {"type": "string"},
                "dependencies": {"type": "object", "additionalProperties": {"type": "string"}},
                "dependency_provenance": {
                    "type": "object",
                    "additionalProperties": {"type": "object"},
                },
            },
        },
        "manifest": {
            "type": "object",
            "required": ["hash_algorithm", "hash_domain", "path_semantics", "bound_inputs"],
            "additionalProperties": False,
            "properties": {
                "hash_algorithm": {"const": "SHA-256"},
                "hash_domain": {"const": "raw file bytes"},
                "path_semantics": {"const": "repository-relative POSIX paths"},
                "bound_inputs": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object", "required": ["byte_count", "sha256"], "additionalProperties": False,
                        "properties": {"byte_count": {"type": "integer"}, "sha256": {"type": "string", "pattern": r"[0-9a-f]{64}"}},
                    },
                },
            },
        },
        "checks": {
            "type": "array", "minItems": 1,
            "items": {
                "type": "object", "required": ["check_id", "status", "evidence_kind", "observed"], "additionalProperties": False,
                "properties": {"check_id": {"type": "string"}, "status": {"enum": ["PASS", "FAIL", "INCONCLUSIVE"]}, "evidence_kind": {"type": "string"}, "observed": {"type": "object"}},
            },
        },
        "semantic_payload_digest": {"type": "string", "pattern": r"[0-9a-f]{64}"},
    },
}


class MissingAPI:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, *_args, **_kwargs):
        return MissingResult(self.name)


class MissingResult:
    def __init__(self, name: str):
        self.name = name


def module():
    spec = importlib.util.spec_from_file_location("manifest_contract_runner", RUNNER_PATH)
    assert spec and spec.loader
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def api(name: str, defect: str):
    value = getattr(module(), name, None)
    return value if callable(value) else MissingAPI(name)


def schema_errors(value, schema: dict, path: str = "$") -> list[str]:
    errors: list[str] = []
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: not in declared enum")
    expected_type = schema.get("type")
    matches_type = {
        "object": isinstance(value, dict), "array": isinstance(value, list),
        "string": isinstance(value, str), "boolean": isinstance(value, bool),
        "integer": isinstance(value, int) and not isinstance(value, bool),
    }.get(expected_type, True)
    if not matches_type:
        return errors + [f"{path}: expected {expected_type}"]
    if isinstance(value, str) and "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
        errors.append(f"{path}: pattern mismatch")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: too few items")
        for index, item in enumerate(value):
            errors.extend(schema_errors(item, schema.get("items", {}), f"{path}[{index}]"))
    if isinstance(value, dict):
        required = set(schema.get("required", []))
        errors.extend(f"{path}: missing {name}" for name in sorted(required - set(value)))
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        if additional is False:
            errors.extend(f"{path}: unexpected {name}" for name in sorted(set(value) - set(properties)))
        for name, item in value.items():
            child_schema = properties.get(name, additional if isinstance(additional, dict) else {})
            errors.extend(schema_errors(item, child_schema, f"{path}.{name}"))
    return errors


def canonical_fixture_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, f"git {' '.join(args)} failed: {completed.stderr}"
    return completed.stdout.strip()


def commit_all(root: Path, message: str) -> str:
    git(root, "add", "--all")
    git(
        root,
        "-c", "user.name=Manifest Contract",
        "-c", "user.email=manifest-contract@example.invalid",
        "commit", "--quiet", "-m", message,
    )
    return git(root, "rev-parse", "HEAD")


def seeded_json(relative: str) -> object:
    if relative.endswith("result.schema.json"):
        return TEST_RESULT_SCHEMA
    if relative.endswith("manifest-policy.json"):
        return {
            "schema_version": "1.0",
            "protocol_profile": SYNTHETIC_PROTOCOL_PROFILE,
            "hash_algorithm": "SHA-256",
            "hash_domain": "raw file bytes",
            "path_semantics": "repository-relative POSIX paths",
            "recursive_inclusions": [
                {
                    "root": "manuscripts/gauge_vfe_rg",
                    "glob": "**/*.tex",
                },
                {
                    "root": "manuscripts/gauge_vfe_rg/verification/tests",
                    "glob": "**/test_*.py",
                },
            ],
            "required_paths": [
                "manuscripts/gauge_vfe_rg/SPEC.md",
                "manuscripts/gauge_vfe_rg/build.ps1",
                "manuscripts/references.bib",
                "manuscripts/gauge_vfe_rg/verification/claims.json",
                "manuscripts/gauge_vfe_rg/verification/run_checks.py",
                "manuscripts/gauge_vfe_rg/verification/requirements.txt",
                "manuscripts/gauge_vfe_rg/verification/VERIFICATION.md",
                "manuscripts/gauge_vfe_rg/verification/result.schema.json",
                "manuscripts/gauge_vfe_rg/verification/manifest-policy.json",
                "manuscripts/gauge_vfe_rg/verification/lifecycle_gate.py",
                "manuscripts/gauge_vfe_rg/verification/build_audit.py",
                "manuscripts/gauge_vfe_rg/verification/build_bootstrap_reference.ps1.txt",
                "manuscripts/gauge_vfe_rg/verification/build_bootstrap_transport.txt",
            ],
            "style_candidates": [
                "manuscripts/gauge_vfe_rg/scientific_report.sty",
                "manuscripts/scientific_report.sty",
            ],
            "governed_namespaces": [
                "manuscripts/gauge_vfe_rg",
                "manuscripts/gauge_vfe_rg/verification/tests",
            ],
            "explicit_exclusions": [
                "manuscripts/gauge_vfe_rg/main.pdf",
                "manuscripts/gauge_vfe_rg/verification/current-results.json",
                "**/__pycache__/**",
                "**/*.pyc",
            ],
            "bound_paths": list(BOUND_FILES),
            "reject_unexpected_governed_paths": True,
        }
    if relative.endswith("claims.json"):
        return {
            "schema_version": "1.0",
            "protocol_profile": SYNTHETIC_PROTOCOL_PROFILE,
            "checks": [{"check_id": "CHK-FIXTURE-PASS"}],
        }
    return {}


def tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    for relative in BOUND_FILES:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if relative.endswith("verification/requirements.txt"):
            payload = PINNED_REQUIREMENTS
        elif path.suffix == ".json":
            payload = canonical_fixture_bytes(seeded_json(relative)) + b"\n"
        else:
            payload = f"bound:{relative}\n".encode()
        path.write_bytes(payload)
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "--quiet")
    commit_all(root, "fixture parent with distinct governed blob")
    main = root / BOUND_FILES[0]
    main.write_bytes(main.read_bytes() + b"source-boundary\n")
    commit_all(root, "source revision S")
    return root


def independent_golden(root: Path, source_revision: str) -> dict:
    bound_inputs = {}
    for relative in BOUND_FILES:
        raw = (root / relative).read_bytes()
        bound_inputs[relative] = {"byte_count": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    document = {
        "schema_version": "3.0",
        "protocol_profile": SYNTHETIC_PROTOCOL_PROFILE,
        "generated_at_utc": "2026-08-03T00:00:00Z",
        "source_revision": source_revision,
        "source_dirty": False,
        "overall_status": "PASS",
        "environment": {"python": "fixture-python-3.14", "python_executable": "C:/fixture/python.exe", "python_executable_sha256": "0" * 64, "git_executable": "C:/fixture/git.exe", "git_executable_sha256": "1" * 64, "platform": "fixture-windows", "machine": "AMD64", "dependencies": dict(DEPENDENCY_PINS), "dependency_provenance": {}},
        "manifest": {"hash_algorithm": "SHA-256", "hash_domain": "raw file bytes", "path_semantics": "repository-relative POSIX paths", "bound_inputs": bound_inputs},
        "checks": [{"check_id": "CHK-FIXTURE-PASS", "status": "PASS", "evidence_kind": "reproduced_output", "observed": {"fixture_complete": True}}],
        "semantic_payload_digest": "",
    }
    refresh_semantic_digest(document)
    return document


def refresh_semantic_digest(document: dict) -> None:
    payload = {key: value for key, value in document.items() if key not in {"generated_at_utc", "semantic_payload_digest"}}
    document["semantic_payload_digest"] = hashlib.sha256(canonical_fixture_bytes(payload)).hexdigest()


def write_result(result: Path, document: dict) -> None:
    result.write_bytes(canonical_fixture_bytes(document))


def golden(root: Path, result: Path, source_revision: str | None = None):
    revision = source_revision or git(root, "rev-parse", "HEAD")
    document = api("build_result", "golden bound result")(
        root, revision, test_fixture=True
    )
    if not isinstance(document, dict):
        document = independent_golden(root, revision)
    errors = schema_errors(document, TEST_RESULT_SCHEMA)
    assert not errors, f"DEFECT [golden fixture shape]: complete baseline violates independent result schema: {errors}"
    assert set(document["manifest"]["bound_inputs"]) == set(BOUND_FILES), "DEFECT [golden fixture shape]: complete baseline must bind every governed path"
    encoded = api("canonical_json_bytes", "golden canonical bytes")(document)
    if not isinstance(encoded, bytes):
        encoded = canonical_fixture_bytes(document)
    result.write_bytes(encoded)
    return document


def issue_codes(report: object) -> set[str]:
    codes: set[str] = set()
    for issue in getattr(report, "issues", ()):
        code = issue.get("code") if isinstance(issue, dict) else getattr(issue, "code", None)
        if isinstance(code, str):
            codes.add(code)
    return codes


def assert_accepted(result: Path, root: Path, defect: str):
    report = api("verify_result", defect)(result, root, test_fixture=True)
    assert getattr(report, "ok", None) is True, f"DEFECT [{defect}]: verifier rejected the unmodified golden result"
    assert not issue_codes(report), f"DEFECT [{defect}]: accepted golden result retained issues: {sorted(issue_codes(report))}"


def assert_rejected(result: Path, root: Path, defect: str, expected_code: str | None = None):
    report = api("verify_result", defect)(result, root, test_fixture=True)
    assert getattr(report, "ok", None) is False, f"DEFECT [{defect}]: verifier accepted mutation"
    if expected_code is not None:
        assert expected_code in issue_codes(report), f"DEFECT [{defect}]: expected {expected_code}, got {sorted(issue_codes(report))}"


def test_unmodified_golden_result_is_accepted(tmp_path: Path):
    root, result = tree(tmp_path), tmp_path / "result.json"
    golden(root, result)
    assert_accepted(result, root, "positive golden acceptance")


def advance_to_evidence_revision(root: Path) -> str:
    evidence = root / "docs/evidence/task-4.json"
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text('{"evidence_only":true}\n', encoding="utf-8")
    return commit_all(root, "evidence revision E")


def test_source_revision_s_is_accepted_at_e(tmp_path: Path):
    root, result = tree(tmp_path), tmp_path / "result.json"
    source_revision = git(root, "rev-parse", "HEAD")
    golden(root, result, source_revision)
    advance_to_evidence_revision(root)
    assert git(root, "rev-parse", "HEAD") != source_revision
    assert_accepted(result, root, "source S accepted at evidence E")


@pytest.mark.parametrize(
    "mutable_git_state",
    ["worktree_attributes", "info_attributes", "autocrlf"],
)
def test_source_binding_raw_mismatch_cannot_be_relaxed_by_mutable_git_eol_state(
    tmp_path: Path,
    mutable_git_state: str,
):
    root = tree(tmp_path)
    source_revision = git(root, "rev-parse", "HEAD")
    relative = BOUND_FILES[0]
    governed_path = root / relative
    source_blob = governed_path.read_bytes()
    assert b"\n" in source_blob and b"\r" not in source_blob
    current_bytes = source_blob.replace(b"\n", b"\r\n")
    governed_path.write_bytes(current_bytes)

    if mutable_git_state == "worktree_attributes":
        (root / ".gitattributes").write_text(
            f"{relative} text eol=crlf\n",
            encoding="ascii",
            newline="\n",
        )
    elif mutable_git_state == "info_attributes":
        info_attributes = root / ".git/info/attributes"
        info_attributes.write_text(
            f"{relative} text eol=crlf\n",
            encoding="ascii",
            newline="\n",
        )
    else:
        git(root, "config", "core.autocrlf", "true")

    loaded = module()
    current_manifest = loaded.build_manifest(root, test_fixture=True)
    issues = loaded._source_binding_issues(
        root,
        source_revision,
        current_manifest,
        test_fixture=True,
    )
    mismatches = [
        issue
        for issue in issues
        if issue.code == "SOURCE_BLOB_MISMATCH" and issue.location == relative
    ]

    assert len(mismatches) == 1, (
        "DEFECT [mutable EOL relaxation]: raw LF source bytes and CRLF retained "
        f"bytes must mismatch regardless of {mutable_git_state}, got {issues!r}"
    )
    assert mismatches[0].expected == {
        "byte_count": len(source_blob),
        "sha256": hashlib.sha256(source_blob).hexdigest(),
    }
    assert mismatches[0].observed == {
        "byte_count": len(current_bytes),
        "sha256": hashlib.sha256(current_bytes).hexdigest(),
    }


@pytest.mark.parametrize(
    "relative",
    [
        "manuscripts/gauge_vfe_rg/chapters/child.tex",
        "manuscripts/gauge_vfe_rg/verification/tests/test_factorization_gap.py",
    ],
)
def test_source_revision_governed_path_set_cannot_shrink_recursively(
    tmp_path: Path,
    relative: str,
):
    root = tree(tmp_path)
    policy_path = root / "manuscripts/gauge_vfe_rg/verification/manifest-policy.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    policy.pop("bound_paths")
    policy_path.write_bytes(canonical_fixture_bytes(policy) + b"\n")
    source_revision = commit_all(root, "source S without redundant bound-path inventory")

    (root / relative).unlink()
    construct = api("build_result", "source-tree governed path-set equality")
    with pytest.raises(Exception) as caught:
        construct(root, source_revision, test_fixture=True)
    assert getattr(caught.value, "code", None) == "MANIFEST_PATH_SET_MISMATCH", (
        "DEFECT [recursive source shrink]: deleting a governed path committed at S "
        f"must fail with MANIFEST_PATH_SET_MISMATCH, got {caught.value!r}"
    )


def test_governed_walk_fails_closed_when_directory_enumeration_errors(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    root = tree(tmp_path)
    loaded = module()

    def unreadable_walk(
        _root: Path,
        *,
        followlinks: bool,
        onerror=None,
    ):
        assert followlinks is False
        if onerror is not None:
            onerror(PermissionError("fixture governed directory is unreadable"))
        return iter(())

    monkeypatch.setattr(loaded.os, "walk", unreadable_walk)
    with pytest.raises(loaded.ManifestPolicyError) as caught:
        loaded._walk_governed_files(root, "manuscripts/gauge_vfe_rg")
    assert "unreadable" in str(caught.value).lower() or "travers" in str(
        caught.value
    ).lower(), (
        "DEFECT [walk omission]: an os.walk enumeration error must fail closed "
        f"instead of returning a partial governed set, got {caught.value!r}"
    )


def test_source_revision_rejects_commit_only_noncanonical_governed_namespace(
    tmp_path: Path,
):
    root = tree(tmp_path)
    canonical_blob = git(
        root,
        "rev-parse",
        "HEAD:manuscripts/gauge_vfe_rg/main.tex",
    )
    alias = "Manuscripts/gauge_vfe_rg/rogue.tex"
    git(
        root,
        "update-index",
        "--add",
        "--cacheinfo",
        f"100644,{canonical_blob},{alias}",
    )
    git(
        root,
        "-c",
        "user.name=Manifest Contract",
        "-c",
        "user.email=manifest-contract@example.invalid",
        "commit",
        "--quiet",
        "-m",
        "source revision with noncanonical governed namespace",
    )
    source_revision = git(root, "rev-parse", "HEAD")

    git(root, "update-index", "--force-remove", alias)
    git(
        root,
        "-c",
        "user.name=Manifest Contract",
        "-c",
        "user.email=manifest-contract@example.invalid",
        "commit",
        "--quiet",
        "-m",
        "remove commit-only alias from current tree",
    )

    loaded = module()
    current_manifest = loaded.build_manifest(root, test_fixture=True)
    issues = loaded._source_revision_governed_path_issues(
        root,
        source_revision,
        current_manifest["bound_inputs"],
        test_fixture=True,
    )
    assert "UNEXPECTED_GOVERNED_PATH" in {
        issue.code for issue in issues
    }, (
        "DEFECT [case alias]: a source tree entry under a case-fold alias of the "
        "governed manuscript namespace must be rejected even when it never exists "
        f"in the working tree, got {issues!r}"
    )


@pytest.mark.parametrize("drift", ["source_revision", "bound_blob"])
def test_source_at_e_rejects_coherent_git_binding_drift(tmp_path: Path, drift: str):
    root, result = tree(tmp_path), tmp_path / "result.json"
    source_revision = git(root, "rev-parse", "HEAD")
    original = golden(root, result, source_revision)
    advance_to_evidence_revision(root)

    changed = json.loads(json.dumps(original))
    if drift == "source_revision":
        changed["source_revision"] = git(root, "rev-parse", f"{source_revision}^")
        defect = "coherent source revision drift"
    else:
        bound_path = root / BOUND_FILES[0]
        bound_path.write_bytes(bound_path.read_bytes() + b"evidence-source-drift\n")
        commit_all(root, "forbidden governed blob drift after E")
        raw = bound_path.read_bytes()
        changed["source_dirty"] = True
        changed["manifest"]["bound_inputs"][BOUND_FILES[0]] = {
            "byte_count": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        }
        defect = "coherent governed blob drift after E"
    refresh_semantic_digest(changed)
    write_result(result, changed)
    assert_rejected(result, root, defect, "SOURCE_BLOB_MISMATCH")


def test_discovery_recursively_finds_every_governed_class_and_no_constant_allowlist(tmp_path: Path):
    root = tree(tmp_path)
    found = api("discover_bound_inputs", "recursive governed discovery")(
        root,
        test_fixture=True,
    )
    assert isinstance(found, dict), "DEFECT [recursive governed discovery]: missing public discovery interface"
    paths = set(found)
    assert set(BOUND_FILES) <= paths, "DEFECT [recursive governed discovery]: missing governed inputs"
    assert "manuscripts/gauge_vfe_rg/chapters/child.tex" in paths, "DEFECT [recursive governed discovery]: recursive TeX omitted"


def test_build_manifest_matches_independent_raw_byte_inventory(tmp_path: Path):
    root = tree(tmp_path)
    manifest = api("build_manifest", "raw-byte manifest construction")(
        root,
        test_fixture=True,
    )
    assert isinstance(manifest, dict), "DEFECT [raw-byte manifest construction]: missing public build_manifest interface"
    assert set(manifest) == {"hash_algorithm", "hash_domain", "path_semantics", "bound_inputs"}
    assert manifest["hash_algorithm"] == "SHA-256"
    assert manifest["hash_domain"] == "raw file bytes"
    assert manifest["path_semantics"] == "repository-relative POSIX paths"
    assert set(manifest["bound_inputs"]) == set(BOUND_FILES)
    for relative in BOUND_FILES:
        raw = (root / relative).read_bytes()
        assert manifest["bound_inputs"][relative] == {
            "byte_count": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        }


def test_semantic_payload_removes_only_two_top_level_fields_without_mutation():
    document = {
        "generated_at_utc": "excluded",
        "semantic_payload_digest": "excluded",
        "nested": {
            "generated_at_utc": "retained",
            "semantic_payload_digest": "retained",
        },
        "value": 7,
    }
    before = json.loads(json.dumps(document))
    payload = api("semantic_payload", "semantic exclusion boundary")(document)
    assert document == before, "DEFECT [semantic exclusion boundary]: semantic_payload mutated its input"
    assert payload == {"nested": before["nested"], "value": 7}, "DEFECT [semantic exclusion boundary]: exclusions were not exactly the two top-level fields"


def test_canonical_json_bytes_are_compact_sorted_utf8_and_reject_nonfinite():
    canonical = api("canonical_json_bytes", "canonical JSON bytes")
    assert canonical({"z": 1, "alpha": "β"}) == '{"alpha":"β","z":1}'.encode("utf-8"), "DEFECT [canonical JSON bytes]: encoding is not compact sorted UTF-8"
    with pytest.raises((TypeError, ValueError)):
        canonical({"bad": float("nan")})


def test_validate_result_shape_accepts_golden_and_rejects_one_extra_field(tmp_path: Path):
    root, result = tree(tmp_path), tmp_path / "result.json"
    document = golden(root, result)
    validate = api("validate_result_shape", "public shape validator")
    assert validate(document, test_fixture=True) == [], "DEFECT [public shape validator]: schema-valid golden result was rejected"
    malformed = json.loads(json.dumps(document))
    malformed["extra"] = True
    errors = validate(malformed, test_fixture=True)
    assert isinstance(errors, list) and errors, "DEFECT [public shape validator]: undeclared top-level field was accepted"

    renamed_dependency = json.loads(json.dumps(document))
    provenance = renamed_dependency["environment"]["dependency_provenance"]
    provenance["evil"] = provenance.pop("numpy")
    errors = validate(renamed_dependency, test_fixture=True)
    assert errors, (
        "DEFECT [closed dependency provenance]: renaming required numpy to an "
        "undeclared seventh dependency must violate the exact schema"
    )


@pytest.mark.parametrize("relative", BOUND_FILES)
def test_each_real_bound_file_byte_mutation_is_rejected(tmp_path: Path, relative: str):
    root, result = tree(tmp_path), tmp_path / "result.json"
    golden(root, result)
    path = root / relative
    path.write_bytes(path.read_bytes() + b"changed\n")
    assert_rejected(result, root, f"byte mutation {relative}")


@pytest.mark.parametrize("kind", ["malformed", "missing_bound_file", "extra_bound_file", "missing_result_field", "extra_result_field", "newline", "semantic", "source_dirty", "unknown_check", "duplicate_check", "revision", "nan", "infinity"])
def test_real_tree_and_result_mutations_fail_closed(tmp_path: Path, kind: str):
    root, result = tree(tmp_path), tmp_path / "result.json"
    document = golden(root, result)
    if kind == "malformed":
        (root / "manuscripts/gauge_vfe_rg/verification/claims.json").write_text("{", encoding="utf-8")
    elif kind == "missing_bound_file":
        (root / BOUND_FILES[0]).unlink()
    elif kind == "extra_bound_file":
        extra = root / "manuscripts/gauge_vfe_rg/chapters/unexpected.tex"
        extra.parent.mkdir(parents=True, exist_ok=True)
        extra.write_text("unexpected\n", encoding="utf-8")
    elif kind == "missing_result_field":
        required = next((field for field in ("source_revision", "semantic_payload_digest", "checks") if field in document), None)
        assert required is not None, "DEFECT [missing result field fixture]: build_result must emit a required result field"
        document.pop(required)
        result.write_text(json.dumps(document) + "\n", encoding="utf-8")
    elif kind == "extra_result_field":
        document["unrecognized_result_field"] = {"must": "fail closed"}
        refresh_semantic_digest(document)
        write_result(result, document)
    elif kind == "newline":
        path = root / BOUND_FILES[0]
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
    elif kind == "semantic":
        document["semantic_payload_digest"] = "0" * 64
        write_result(result, document)
    elif kind == "source_dirty":
        document["source_dirty"] = True
        refresh_semantic_digest(document)
        write_result(result, document)
    elif kind in {"unknown_check", "duplicate_check"}:
        valid = json.loads(json.dumps(document["checks"][0]))
        if kind == "unknown_check":
            valid["check_id"] = "CHK-UNKNOWN"
            document["checks"] = [valid]
        else:
            document["checks"] = [valid, json.loads(json.dumps(valid))]
        refresh_semantic_digest(document)
        write_result(result, document)
    elif kind == "revision":
        document["source_revision"] = "0" * 40
        refresh_semantic_digest(document)
        write_result(result, document)
    else:
        result.write_text('{"value": ' + ("NaN" if kind == "nan" else "Infinity") + "}\n", encoding="utf-8")
    expected_codes = {
        "semantic": "SEMANTIC_DIGEST_MISMATCH",
        "source_dirty": "SCHEMA_VIOLATION",
        "unknown_check": "CHECK_ID_UNKNOWN",
        "duplicate_check": "CHECK_ID_DUPLICATE",
        "revision": "SOURCE_REVISION_NOT_FOUND",
    }
    assert_rejected(result, root, f"real {kind} mutation", expected_codes.get(kind))
