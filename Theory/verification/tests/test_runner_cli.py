"""Black-box RED contract for the positional update/verify runner interface."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import threading
import uuid
from pathlib import Path
from types import SimpleNamespace

import pytest


RUNNER = Path(__file__).resolve().parents[1] / "run_checks.py"
RUNNER_RELATIVE = Path("manuscripts/gauge_vfe_rg/verification/run_checks.py")
PRODUCTION_PROTOCOL_PROFILE = "gauge-vfe-rg-production-v1"
SYNTHETIC_PROTOCOL_PROFILE = "synthetic-test-fixture-v1"
FIXED_PYTHON_EXECUTABLE = Path(r"C:\Python314\python.exe")
FIXED_GIT_EXECUTABLE = Path(r"C:\Program Files\Git\cmd\git.exe")
FIXED_SITE_PACKAGES = Path(
    r"C:\Users\chris and christine\AppData\Roaming\Python\Python314\site-packages"
)
DEPENDENCY_NAMES = {
    "numpy",
    "scipy",
    "sympy",
    "mpmath",
    "pypdf",
    "pytest",
}
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
)
PRODUCTION_MANUSCRIPT_ENVELOPE = (
    "01_introduction.tex",
    "02_geometry.tex",
    "03_probability.tex",
    "04_generative.tex",
    "05_elbo.tex",
    "05a_expfamily.tex",
    "05b_local_collective_elbo.tex",
    "05c_pullback_geometry.tex",
    "05d_relational_inference.tex",
    "06_general_coarsegraining.tex",
    "06_gaussian.tex",
    "06a_generative_gaussian.tex",
    "07_general_renormalization.tex",
    "07_restrictions.tex",
    "07b_agent_network_rg.tex",
    "08_infogeometry.tex",
    "09_coarsegraining.tex",
    "10_renormalization.tex",
    "11_obstructions.tex",
    "12_philosophy.tex",
    "appendix_claim_ledger.tex",
    "appendix_notation.tex",
    "appendix_numerical_provenance.tex",
)
TEST_RESULT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["schema_version", "protocol_profile", "generated_at_utc", "source_revision", "source_dirty", "overall_status", "environment", "manifest", "checks", "semantic_payload_digest"],
    "additionalProperties": False,
    "properties": {
        "schema_version": {"const": "3.0"},
        "protocol_profile": {"const": SYNTHETIC_PROTOCOL_PROFILE},
        "generated_at_utc": {"type": "string"},
        "source_revision": {"type": "string", "pattern": "[0-9a-f]{40}"},
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
                "python_executable_sha256": {"type": "string", "pattern": "[0-9a-f]{64}"},
                "git_executable": {"type": "string"},
                "git_executable_sha256": {"type": "string", "pattern": "[0-9a-f]{64}"},
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
                "bound_inputs": {"type": "object"},
            },
        },
        "checks": {
            "type": "array", "minItems": 1,
            "items": {
                "type": "object",
                "required": ["check_id", "status", "evidence_kind", "observed"],
                "additionalProperties": False,
                "properties": {
                    "check_id": {"type": "string"},
                    "status": {"enum": ["PASS", "FAIL", "INCONCLUSIVE"]},
                    "evidence_kind": {"type": "string"},
                    "observed": {"type": "object"},
                },
            },
        },
        "semantic_payload_digest": {"type": "string", "pattern": "[0-9a-f]{64}"},
    },
}


class MissingAtomicWrite:
    def __call__(self, *_args, **_kwargs):
        return None


def runner_module():
    spec = importlib.util.spec_from_file_location("runner_cli_contract", RUNNER)
    assert spec and spec.loader
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def fixture_runner_module(root: Path):
    runner = root / RUNNER_RELATIVE
    spec = importlib.util.spec_from_file_location(
        f"runner_cli_fixture_{hash(root)}", runner
    )
    assert spec and spec.loader
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def install_fake_dependency_environment(
    loaded,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[dict[str, object], Path]:
    """Install a complete, byte-backed six-package provenance fixture."""

    user_base = tmp_path / "Python"
    site = user_base / "Python314/site-packages"
    site.mkdir(parents=True)

    class FixturePackagePath:
        def __init__(self, value: str):
            self.value = value

        def __str__(self) -> str:
            return self.value

    class FixtureDistribution:
        def __init__(self, name: str):
            self.version = DEPENDENCY_PINS[name]
            self.metadata = {"Name": name}
            package = site / name / "__init__.py"
            package.parent.mkdir(parents=True)
            package.write_bytes(b"alpha\n")
            record = site / f"{name}-1.0.dist-info/RECORD"
            record.parent.mkdir(parents=True)
            self._path = record.parent
            record.write_text(
                f"{name}/__init__.py,,6\n{name}-1.0.dist-info/RECORD,,\n",
                encoding="utf-8",
            )
            self.files = (
                FixturePackagePath(f"{name}/__init__.py"),
                FixturePackagePath(f"{name}-1.0.dist-info/RECORD"),
            )

        def locate_file(self, item: object) -> Path:
            return site / str(item)

    distributions = {name: FixtureDistribution(name) for name in DEPENDENCY_NAMES}
    monkeypatch.setattr(loaded, "_FIXED_SITE_PACKAGES", site)
    monkeypatch.setattr(loaded, "_FIXED_USER_BASE", user_base)
    monkeypatch.setattr(
        loaded,
        "_find_dependency_spec",
        lambda name: SimpleNamespace(origin=str(site / name / "__init__.py")),
    )
    monkeypatch.setattr(
        loaded.importlib.metadata,
        "distribution",
        lambda name: distributions[name],
    )
    monkeypatch.setattr(
        loaded.importlib.metadata,
        "distributions",
        lambda **kwargs: (
            [distributions[kwargs["name"]]]
            if "name" in kwargs
            else list(distributions.values())
        ),
    )
    monkeypatch.setattr(
        loaded,
        "_dependency_versions",
        lambda: dict(DEPENDENCY_PINS),
    )
    return distributions, site / "numpy/__init__.py"


def runner_api(name: str, defect: str):
    value = getattr(runner_module(), name, None)
    return value if callable(value) else MissingAtomicWrite()


def files(root: Path) -> dict[str, str]:
    return {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(root.rglob("*")) if path.is_file()}


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
        "-c", "user.name=Runner Contract",
        "-c", "user.email=runner-contract@example.invalid",
        "commit", "--quiet", "-m", message,
    )
    return git(root, "rev-parse", "HEAD")


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def refresh_semantic_digest(document: dict) -> None:
    payload = {key: value for key, value in document.items() if key not in {"generated_at_utc", "semantic_payload_digest"}}
    document["semantic_payload_digest"] = hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def report_codes(path: Path) -> set[str]:
    document = json.loads(path.read_text(encoding="utf-8"))
    return {
        issue["code"]
        for issue in document.get("issues", [])
        if isinstance(issue, dict) and isinstance(issue.get("code"), str)
    }


def assert_only_report_added(before: dict[str, str], after: dict[str, str], report: Path, defect: str) -> None:
    expected = dict(before)
    expected[report.name] = after.get(report.name, "")
    assert report.name in after, f"DEFECT [{defect}]: explicit report was not written"
    assert after == expected, f"DEFECT [{defect}]: verify changed existing bytes or wrote outside its explicit report"


def invoke(
    root: Path,
    *args: str,
    env_overrides: dict[str, str] | None = None,
    test_fixture: bool = True,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    if env_overrides:
        environment.update(env_overrides)
    command = [
        str(FIXED_PYTHON_EXECUTABLE),
        "-I",
        "-S",
        "-B",
        str(root / RUNNER_RELATIVE),
        *args,
    ]
    if test_fixture:
        harness = (
            "import importlib.util,sys;"
            "p=sys.argv[1];"
            "s=importlib.util.spec_from_file_location('fixture_runner_entry',p);"
            "m=importlib.util.module_from_spec(s);"
            "s.loader.exec_module(m);"
            "raise SystemExit(m.main(sys.argv[2:],test_fixture=True))"
        )
        command = [
            str(FIXED_PYTHON_EXECUTABLE),
            "-B",
            "-c",
            harness,
            str(root / RUNNER_RELATIVE),
            *args,
        ]
    return subprocess.run(
        command,
        cwd=root,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )


def governed_tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    for relative, content in {
        "manuscripts/gauge_vfe_rg/main.tex": "\\documentclass{article}\n",
        "manuscripts/gauge_vfe_rg/nested/child.tex": "child\n",
        "manuscripts/gauge_vfe_rg/SPEC.md": "spec\n",
        "manuscripts/gauge_vfe_rg/scientific_report.sty": "style\n",
        "manuscripts/scientific_report.sty": "parent style\n",
        "manuscripts/gauge_vfe_rg/build.ps1": "build\n",
        "manuscripts/references.bib": "@book{x,title={x}}\n",
        "manuscripts/gauge_vfe_rg/verification/claims.json": json.dumps({"schema_version": "1.0", "protocol_profile": SYNTHETIC_PROTOCOL_PROFILE, "checks": [{"check_id": "CHK-FIXTURE-PASS"}]}, sort_keys=True) + "\n",
        "manuscripts/gauge_vfe_rg/verification/requirements.txt": PINNED_REQUIREMENTS,
        "manuscripts/gauge_vfe_rg/verification/VERIFICATION.md": "protocol\n",
        "manuscripts/gauge_vfe_rg/verification/result.schema.json": json.dumps(TEST_RESULT_SCHEMA, sort_keys=True) + "\n",
        "manuscripts/gauge_vfe_rg/verification/lifecycle_gate.py": "# gate\n",
        "manuscripts/gauge_vfe_rg/verification/build_audit.py": "# audit\n",
        "manuscripts/gauge_vfe_rg/verification/build_bootstrap_reference.ps1.txt": "# bootstrap reference\n",
        "manuscripts/gauge_vfe_rg/verification/build_bootstrap_transport.txt": "IyBib290c3RyYXAgcmVmZXJlbmNlCg==\n",
    }.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    (root / "manuscripts/gauge_vfe_rg/verification/requirements.txt").write_bytes(
        PINNED_REQUIREMENTS.encode("ascii")
    )
    shutil.copy2(RUNNER, root / RUNNER_RELATIVE)
    fixture_tests = root / "manuscripts/gauge_vfe_rg/verification/tests"
    fixture_tests.mkdir(parents=True, exist_ok=True)
    for source in sorted((RUNNER.parent / "tests").glob("test_*.py")):
        shutil.copy2(source, fixture_tests / source.name)
    bound_paths = [
        path.relative_to(root).as_posix()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    ]
    policy_path = root / "manuscripts/gauge_vfe_rg/verification/manifest-policy.json"
    policy_path.write_text(
        json.dumps(
            {
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
                "bound_paths": sorted([*bound_paths, policy_path.relative_to(root).as_posix()]),
                "reject_unexpected_governed_paths": True,
                "explicit_exclusions": [
                    "manuscripts/gauge_vfe_rg/main.pdf",
                    "manuscripts/gauge_vfe_rg/verification/current-results.json",
                    "**/__pycache__/**",
                    "**/*.pyc",
                ],
            },
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )
    git(root, "init", "--quiet")
    git(root, "config", "core.autocrlf", "false")
    commit_all(root, "valid governed source fixture")
    return root


def rewrite_json(path: Path, transform) -> None:
    document = json.loads(path.read_text(encoding="utf-8"))
    transform(document)
    path.write_text(json.dumps(document, sort_keys=True) + "\n", encoding="utf-8")


def declare_synthetic_protocol(root: Path) -> str:
    rewrite_json(
        root / "manuscripts/gauge_vfe_rg/verification/manifest-policy.json",
        lambda document: document.__setitem__(
            "protocol_profile", SYNTHETIC_PROTOCOL_PROFILE
        ),
    )
    rewrite_json(
        root / "manuscripts/gauge_vfe_rg/verification/claims.json",
        lambda document: document.__setitem__(
            "protocol_profile", SYNTHETIC_PROTOCOL_PROFILE
        ),
    )
    if git(root, "status", "--porcelain"):
        return commit_all(root, "declare explicit synthetic verification fixture")
    return git(root, "rev-parse", "HEAD")


def add_full_production_manuscript_envelope(root: Path) -> str:
    tex_root = root / "manuscripts/gauge_vfe_rg"
    additions: list[str] = []
    for name in PRODUCTION_MANUSCRIPT_ENVELOPE:
        path = tex_root / name
        if not path.exists():
            path.write_text(f"production envelope: {name}\n", encoding="utf-8")
            additions.append(path.relative_to(root).as_posix())
    policy_path = root / "manuscripts/gauge_vfe_rg/verification/manifest-policy.json"
    rewrite_json(
        policy_path,
        lambda document: document["bound_paths"].extend(
            sorted(set(additions) - set(document["bound_paths"]))
        ),
    )
    rewrite_json(
        policy_path,
        lambda document: document.__setitem__(
            "bound_paths", sorted(document["bound_paths"])
        ),
    )
    return commit_all(root, "complete production manuscript envelope")


def remove_protocol_declarations(root: Path) -> None:
    for relative in (
        "manuscripts/gauge_vfe_rg/verification/manifest-policy.json",
        "manuscripts/gauge_vfe_rg/verification/claims.json",
    ):
        rewrite_json(root / relative, lambda document: document.pop("protocol_profile", None))
    if git(root, "status", "--porcelain"):
        commit_all(root, "remove protocol declarations")


def test_undeclared_synthetic_checks_cannot_downgrade_production_protocol(
    tmp_path: Path,
):
    root = governed_tree(tmp_path)
    remove_protocol_declarations(root)
    result, report = tmp_path / "downgraded.json", tmp_path / "downgraded.report.json"

    completed = invoke(
        root,
        "--update",
        str(result),
        "--report",
        str(report),
        test_fixture=False,
    )

    assert completed.returncode != 0, (
        "DEFECT [production-to-fixture downgrade]: undeclared top-level fixture checks "
        "must not produce PASS/0"
    )
    assert not result.exists(), (
        "DEFECT [production-to-fixture downgrade]: rejected synthetic mode wrote a result"
    )
    assert "PROTOCOL_PROFILE_MISMATCH" in report_codes(report), (
        "DEFECT [production-to-fixture downgrade specificity]: expected "
        f"PROTOCOL_PROFILE_MISMATCH, got {sorted(report_codes(report))}"
    )


def test_production_profile_rejects_top_level_synthetic_checks(tmp_path: Path):
    root = governed_tree(tmp_path)
    rewrite_json(
        root / "manuscripts/gauge_vfe_rg/verification/manifest-policy.json",
        lambda document: document.__setitem__(
            "protocol_profile", PRODUCTION_PROTOCOL_PROFILE
        ),
    )
    rewrite_json(
        root / "manuscripts/gauge_vfe_rg/verification/claims.json",
        lambda document: document.update(
            {
                "schema_version": "2.1",
                "protocol_profile": PRODUCTION_PROTOCOL_PROFILE,
            }
        ),
    )
    source_revision = commit_all(root, "production envelope with forbidden fixture checks")
    result = tmp_path / "production-downgrade.json"
    report = tmp_path / "production-downgrade.report.json"

    completed = invoke(
        root,
        "--update",
        str(result),
        "--source-revision",
        source_revision,
        "--report",
        str(report),
        test_fixture=False,
    )

    assert completed.returncode != 0
    assert not result.exists()
    assert "PROTOCOL_PROFILE_MISMATCH" in report_codes(report), (
        "DEFECT [production envelope downgrade specificity]: expected exact production "
        f"profile rejection, got {sorted(report_codes(report))}"
    )


def test_explicit_in_process_synthetic_protocol_fixture_remains_available(
    tmp_path: Path,
):
    root = governed_tree(tmp_path)
    declare_synthetic_protocol(root)
    result = tmp_path / "synthetic-result.json"

    completed = invoke(root, "--update", str(result))

    assert completed.returncode == 0, (
        "DEFECT [explicit synthetic fixture]: declared synthetic fixture failed: "
        f"{completed.stderr}{completed.stdout}"
    )
    document = json.loads(result.read_text(encoding="utf-8"))
    assert document["protocol_profile"] == SYNTHETIC_PROTOCOL_PROFILE
    assert [item["check_id"] for item in document["checks"]] == ["CHK-FIXTURE-PASS"]


def test_tracked_dual_synthetic_declarations_cannot_downgrade_ordinary_cli(
    tmp_path: Path,
):
    root = governed_tree(tmp_path)
    source_revision = add_full_production_manuscript_envelope(root)
    result = tmp_path / "ordinary-cli-result.json"
    report = tmp_path / "ordinary-cli-report.json"

    completed = invoke(
        root,
        "--update",
        str(result),
        "--source-revision",
        source_revision,
        "--report",
        str(report),
        test_fixture=False,
    )

    assert completed.returncode != 0
    assert not result.exists()
    assert "PROTOCOL_PROFILE_MISMATCH" in report_codes(report)
    report_document = json.loads(report.read_text(encoding="utf-8"))
    assert report_document["protocol_profile"] == PRODUCTION_PROTOCOL_PROFILE


def test_explicit_fixture_api_rejects_full_production_manuscript_envelope(
    tmp_path: Path,
):
    root = governed_tree(tmp_path)
    source_revision = add_full_production_manuscript_envelope(root)
    loaded = fixture_runner_module(root)

    with pytest.raises(loaded.VerificationFailure) as caught:
        loaded.build_result(root, source_revision, test_fixture=True)

    assert caught.value.code == "PROTOCOL_PROFILE_MISMATCH"


def test_result_and_report_record_exact_executable_identities(tmp_path: Path):
    root = governed_tree(tmp_path)
    source_revision = git(root, "rev-parse", "HEAD")
    loaded = fixture_runner_module(root)
    document = loaded.build_result(root, source_revision, test_fixture=True)
    result = tmp_path / "provenance-result.json"
    result.write_bytes(loaded.canonical_json_bytes(document))
    report = loaded.verify_result(result, root, test_fixture=True)
    report_document = loaded.verification_report_document(report)

    expected_python_hash = hashlib.sha256(FIXED_PYTHON_EXECUTABLE.read_bytes()).hexdigest()
    expected_git_hash = hashlib.sha256(FIXED_GIT_EXECUTABLE.read_bytes()).hexdigest()
    assert document["environment"]["python_executable"] == str(FIXED_PYTHON_EXECUTABLE)
    assert document["environment"]["python_executable_sha256"] == expected_python_hash
    assert document["environment"]["git_executable"] == str(FIXED_GIT_EXECUTABLE)
    assert document["environment"]["git_executable_sha256"] == expected_git_hash
    dependency_provenance = document["environment"]["dependency_provenance"]
    assert set(dependency_provenance) == DEPENDENCY_NAMES
    for name, provenance in dependency_provenance.items():
        assert set(provenance) == {
            "installed",
            "version",
            "module_origin",
            "module_origin_sha256",
            "record_path",
            "record_sha256",
            "record_byte_count",
            "record_entry_count",
            "actual_tree_sha256",
            "actual_file_count",
            "actual_byte_count",
        }
        assert provenance["installed"] is True
        assert provenance["version"] == DEPENDENCY_PINS[name]
        assert Path(provenance["module_origin"]).is_relative_to(FIXED_SITE_PACKAGES)
        assert Path(provenance["record_path"]).is_relative_to(FIXED_SITE_PACKAGES)
        assert len(provenance["record_sha256"]) == 64
        assert len(provenance["module_origin_sha256"]) == 64
        assert len(provenance["actual_tree_sha256"]) == 64
        assert provenance["record_entry_count"] > 0
        assert provenance["actual_file_count"] == provenance["record_entry_count"]
        assert provenance["actual_byte_count"] > 0
    assert report.ok is True
    assert report_document["protocol_profile"] == SYNTHETIC_PROTOCOL_PROFILE
    assert report_document["head_revision"] == source_revision
    assert report_document["python_executable"] == str(FIXED_PYTHON_EXECUTABLE)
    assert report_document["python_executable_sha256"] == expected_python_hash
    assert report_document["git_executable"] == str(FIXED_GIT_EXECUTABLE)
    assert report_document["git_executable_sha256"] == expected_git_hash


@pytest.mark.parametrize("operation", ["update", "verify"])
def test_update_and_verify_reject_fixed_git_identity_change_after_m0(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    operation: str,
):
    root = governed_tree(tmp_path)
    source_revision = git(root, "rev-parse", "HEAD")
    loaded = fixture_runner_module(root)
    result = tmp_path / f"tool-m1-{operation}.json"
    report_path = tmp_path / f"tool-m1-{operation}.report.json"
    if operation == "verify":
        baseline = loaded.build_result(root, source_revision, test_fixture=True)
        result.write_bytes(loaded.canonical_json_bytes(baseline))

    real_identity = loaded._stable_executable_identity
    git_calls = 0

    def drifting_identity(path: Path, role: str):
        nonlocal git_calls
        identity = real_identity(path, role)
        if role == "Git":
            git_calls += 1
            if git_calls > 1:
                identity = {**identity, "sha256": "f" * 64}
        return identity

    monkeypatch.setattr(loaded, "_stable_executable_identity", drifting_identity)

    if operation == "update":
        returncode = loaded.main(
            [
                "--update",
                str(result),
                "--source-revision",
                source_revision,
                "--report",
                str(report_path),
            ],
            test_fixture=True,
        )
        codes = report_codes(report_path)
        assert returncode != 0
        assert not result.exists()
    else:
        report = loaded.verify_result(result, root, test_fixture=True)
        codes = {issue.code for issue in report.issues}
        assert report.ok is False

    assert git_calls >= 2
    assert "EXECUTABLE_IDENTITY" in codes


@pytest.mark.parametrize("role", ["Python", "Git"])
def test_verify_rejects_byte_identical_tool_filesystem_identity_change(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    role: str,
):
    root = governed_tree(tmp_path)
    source_revision = git(root, "rev-parse", "HEAD")
    loaded = fixture_runner_module(root)
    result = tmp_path / f"byte-identical-{role.casefold()}.json"
    baseline = loaded.build_result(root, source_revision, test_fixture=True)
    result.write_bytes(loaded.canonical_json_bytes(baseline))
    real_identity = loaded._stable_executable_identity
    role_calls = 0
    first_hash: str | None = None

    def byte_identical_replacement(path: Path, observed_role: str):
        nonlocal role_calls, first_hash
        identity = real_identity(path, observed_role)
        if observed_role == role:
            role_calls += 1
            if role_calls == 1:
                first_hash = identity["sha256"]
            else:
                changed = list(identity["filesystem_identity"])
                changed[1] += 1
                identity = {**identity, "filesystem_identity": changed}
        return identity

    monkeypatch.setattr(
        loaded,
        "_stable_executable_identity",
        byte_identical_replacement,
    )
    report = loaded.verify_result(result, root, test_fixture=True)

    assert report.ok is False
    assert role_calls >= 2
    assert first_hash is not None
    assert any(
        issue.code == "EXECUTABLE_IDENTITY"
        and issue.expected is not None
        and issue.observed is not None
        for issue in report.issues
    )


def test_dependency_provenance_hashes_actual_files_when_record_is_unchanged(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    loaded = runner_module()
    _distributions, numpy_init = install_fake_dependency_environment(
        loaded,
        tmp_path,
        monkeypatch,
    )

    before = loaded._dependency_provenance()
    numpy_init.write_bytes(b"omega\n")
    after = loaded._dependency_provenance()

    assert before["numpy"]["record_sha256"] == after["numpy"]["record_sha256"]
    assert before["numpy"]["actual_tree_sha256"] != after["numpy"][
        "actual_tree_sha256"
    ], (
        "DEFECT [actual dependency bytes]: changing executed package bytes while "
        "leaving RECORD unchanged must change the recorded provenance identity"
    )


def test_dependency_provenance_rejects_dist_info_outside_exact_site_packages(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    loaded = runner_module()
    record_root = tmp_path / "Python"
    site = record_root / "Python314/site-packages"
    package = site / "fixturedep/__init__.py"
    package.parent.mkdir(parents=True)
    package.write_bytes(b"fixture\n")
    record = site / "fixturedep-1.0.dist-info/RECORD"
    record.parent.mkdir(parents=True)
    record.write_text(
        "fixturedep/__init__.py,,8\nfixturedep-1.0.dist-info/RECORD,,\n",
        encoding="utf-8",
    )

    class FixtureDistribution:
        version = "1.0"
        files = (
            "fixturedep/__init__.py",
            "fixturedep-1.0.dist-info/RECORD",
        )
        _path = record_root / "shadow/fixturedep-1.0.dist-info"

        @staticmethod
        def locate_file(item: object) -> Path:
            return site / str(item)

    monkeypatch.setattr(loaded, "_FIXED_SITE_PACKAGES", site)
    monkeypatch.setattr(loaded, "_FIXED_USER_BASE", record_root)
    with pytest.raises(loaded.VerificationFailure) as caught:
        loaded._installed_distribution_provenance(
            "fixturedep",
            package,
            FixtureDistribution(),
        )

    assert caught.value.code == "EXECUTABLE_IDENTITY"
    assert "dist-info" in str(caught.value).lower()


def test_dependency_provenance_rejects_duplicate_matching_dist_info(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    loaded = runner_module()
    distributions, _numpy_init = install_fake_dependency_environment(
        loaded,
        tmp_path,
        monkeypatch,
    )
    duplicate = distributions["numpy"]
    all_distributions = list(distributions.values()) + [duplicate]
    monkeypatch.setattr(
        loaded.importlib.metadata,
        "distributions",
        lambda **_kwargs: all_distributions,
    )

    with pytest.raises(loaded.VerificationFailure) as caught:
        loaded._dependency_provenance()

    assert caught.value.code == "EXECUTABLE_IDENTITY"
    assert "exactly one" in str(caught.value).lower()


@pytest.mark.parametrize("declared_hash", ["evil=AAAA", "sha512=" + "A" * 86])
def test_dependency_provenance_rejects_unsupported_or_wrong_declared_hash(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    declared_hash: str,
):
    loaded = runner_module()
    distributions, _numpy_init = install_fake_dependency_environment(
        loaded,
        tmp_path,
        monkeypatch,
    )
    numpy_distribution = distributions["numpy"]
    record = Path(numpy_distribution._path) / "RECORD"
    record.write_text(
        f"numpy/__init__.py,{declared_hash},6\n"
        "numpy-1.0.dist-info/RECORD,,\n",
        encoding="utf-8",
    )

    with pytest.raises(loaded.VerificationFailure) as caught:
        loaded._dependency_provenance()

    assert caught.value.code == "EXECUTABLE_IDENTITY"
    assert "hash" in str(caught.value).lower() or "bytes" in str(caught.value).lower()


def test_dependency_pins_accept_only_the_exact_six_line_contract(tmp_path: Path):
    loaded = runner_module()
    requirements = tmp_path / "requirements.txt"
    requirements.write_text(PINNED_REQUIREMENTS, encoding="ascii", newline="\n")

    assert loaded._dependency_pins(requirements) == DEPENDENCY_PINS


def test_dependency_pins_accept_uniform_crlf_fresh_checkout_bytes(tmp_path: Path):
    loaded = runner_module()
    requirements = tmp_path / "requirements.txt"
    requirements.write_bytes(PINNED_REQUIREMENTS.replace("\n", "\r\n").encode("ascii"))

    assert loaded._dependency_pins(requirements) == DEPENDENCY_PINS


@pytest.mark.parametrize(
    "replacement",
    [
        PINNED_REQUIREMENTS.replace("pytest==9.0.2", "numpy==2.4.4"),
        PINNED_REQUIREMENTS.replace("numpy==2.4.4", "NumPy==2.4.4"),
        PINNED_REQUIREMENTS.replace("numpy==2.4.4", "numpy>=2.4.4"),
        PINNED_REQUIREMENTS.replace("numpy==2.4.4", "numpy ==2.4.4"),
        PINNED_REQUIREMENTS.replace("numpy==2.4.4", "numpy==02.4.4"),
        PINNED_REQUIREMENTS.replace("numpy==2.4.4\n", "numpy==2.4.4\r\n"),
    ],
)
def test_dependency_pins_reject_duplicate_or_malformed_lines(
    tmp_path: Path,
    replacement: str,
):
    loaded = runner_module()
    requirements = tmp_path / "requirements.txt"
    requirements.write_text(replacement, encoding="ascii", newline="\n")

    with pytest.raises(loaded.VerificationFailure) as caught:
        loaded._dependency_pins(requirements)

    assert caught.value.code == "EXECUTABLE_IDENTITY"


def test_dependency_provenance_rejects_exact_pin_version_mismatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    loaded = runner_module()
    distributions, _numpy_init = install_fake_dependency_environment(
        loaded,
        tmp_path / "dependencies",
        monkeypatch,
    )
    distributions["numpy"].version = "2.4.3"

    with pytest.raises(loaded.VerificationFailure) as caught:
        loaded._dependency_provenance(verify_imported_versions=False)

    assert caught.value.code == "EXECUTABLE_IDENTITY"
    assert caught.value.expected == "2.4.4"
    assert caught.value.observed == "2.4.3"


def test_dependency_provenance_rejects_syntactically_valid_out_of_range_pin(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    loaded = runner_module()
    install_fake_dependency_environment(
        loaded,
        tmp_path / "dependencies",
        monkeypatch,
    )
    requirements = tmp_path / "requirements.txt"
    requirements.write_text(
        PINNED_REQUIREMENTS.replace("numpy==2.4.4", "numpy==99.0.0"),
        encoding="ascii",
        newline="\n",
    )
    monkeypatch.setattr(loaded, "REQUIREMENTS_PATH", requirements)

    with pytest.raises(loaded.VerificationFailure) as caught:
        loaded._dependency_provenance(verify_imported_versions=False)

    assert caught.value.code == "EXECUTABLE_IDENTITY"
    assert caught.value.expected == "99.0.0"
    assert caught.value.observed == "2.4.4"


def test_verify_rejects_dependency_map_provenance_cross_field_mismatch(
    tmp_path: Path,
):
    root = governed_tree(tmp_path)
    source_revision = git(root, "rev-parse", "HEAD")
    loaded = fixture_runner_module(root)
    document = loaded.build_result(root, source_revision, test_fixture=True)
    document["environment"]["dependencies"]["numpy"] = "99.0.0"
    refresh_semantic_digest(document)
    result = tmp_path / "cross-field-result.json"
    result.write_bytes(loaded.canonical_json_bytes(document))

    report = loaded.verify_result(result, root, test_fixture=True)

    assert report.ok is False
    assert "EXECUTABLE_IDENTITY" in {issue.code for issue in report.issues}
    assert any(
        issue.location == "$.environment.dependencies"
        for issue in report.issues
    )


@pytest.mark.parametrize("tamper", ["installed_integer", "source_dirty_integer"])
def test_verify_rejects_boolean_const_integer_type_confusion(
    tmp_path: Path,
    tamper: str,
):
    root = governed_tree(tmp_path)
    source_revision = git(root, "rev-parse", "HEAD")
    loaded = fixture_runner_module(root)
    document = loaded.build_result(root, source_revision, test_fixture=True)
    if tamper == "installed_integer":
        document["environment"]["dependency_provenance"]["numpy"]["installed"] = 1
    else:
        document["source_dirty"] = 0
    refresh_semantic_digest(document)
    result = tmp_path / f"{tamper}.json"
    result.write_bytes(loaded.canonical_json_bytes(document))

    report = loaded.verify_result(result, root, test_fixture=True)

    assert report.ok is False
    expected_code = (
        "EXECUTABLE_IDENTITY"
        if tamper == "installed_integer"
        else "SCHEMA_VIOLATION"
    )
    assert expected_code in {issue.code for issue in report.issues}


@pytest.mark.parametrize("operation", ["update", "verify"])
def test_update_and_verify_reject_dependency_bytes_changed_after_m0(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    operation: str,
):
    root = governed_tree(tmp_path)
    source_revision = git(root, "rev-parse", "HEAD")
    loaded = fixture_runner_module(root)
    _distributions, numpy_init = install_fake_dependency_environment(
        loaded,
        tmp_path / "dependencies",
        monkeypatch,
    )
    result = tmp_path / f"dependency-m1-{operation}.json"
    report_path = tmp_path / f"dependency-m1-{operation}.report.json"
    if operation == "verify":
        baseline = loaded.build_result(root, source_revision, test_fixture=True)
        result.write_bytes(loaded.canonical_json_bytes(baseline))

    real_provenance = loaded._dependency_provenance
    calls = 0

    def provenance_then_mutate_package_bytes():
        nonlocal calls
        provenance = real_provenance()
        calls += 1
        if calls == 1:
            numpy_init.write_bytes(b"omega\n")
        return provenance

    monkeypatch.setattr(
        loaded,
        "_dependency_provenance",
        provenance_then_mutate_package_bytes,
    )

    if operation == "update":
        returncode = loaded.main(
            [
                "--update",
                str(result),
                "--source-revision",
                source_revision,
                "--report",
                str(report_path),
            ],
            test_fixture=True,
        )
        stdout_report = json.loads(capsys.readouterr().out)
        codes = {
            issue["code"]
            for issue in stdout_report["issues"]
        }
        assert returncode != 0
        assert stdout_report["ok"] is False
        assert not result.exists()
        assert not report_path.exists()
    else:
        report = loaded.verify_result(result, root, test_fixture=True)
        codes = {issue.code for issue in report.issues}
        assert report.ok is False

    assert calls >= 2
    assert "EXECUTABLE_IDENTITY" in codes


def test_verify_final_m1_failure_preserves_result_and_existing_report_bytes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
):
    root = governed_tree(tmp_path)
    source_revision = git(root, "rev-parse", "HEAD")
    loaded = fixture_runner_module(root)
    _distributions, numpy_init = install_fake_dependency_environment(
        loaded,
        tmp_path / "dependencies",
        monkeypatch,
    )
    result = tmp_path / "verify-m1-result.json"
    report_path = tmp_path / "verify-m1-report.json"
    baseline = loaded.build_result(root, source_revision, test_fixture=True)
    result.write_bytes(loaded.canonical_json_bytes(baseline))
    before_result = result.read_bytes()
    before_report = b"preexisting verify report sentinel\n"
    report_path.write_bytes(before_report)
    real_stage = loaded._stage_json_document
    mutated = False

    def stage_then_mutate_dependency(path: Path, value: object):
        nonlocal mutated
        staged = real_stage(path, value)
        if not mutated:
            numpy_init.write_bytes(b"omega\n")
            mutated = True
        return staged

    monkeypatch.setattr(
        loaded,
        "_stage_json_document",
        stage_then_mutate_dependency,
    )
    returncode = loaded.main(
        ["--verify", str(result), "--report", str(report_path)],
        test_fixture=True,
    )

    stdout_report = json.loads(capsys.readouterr().out)
    assert returncode != 0
    assert mutated is True
    assert stdout_report["ok"] is False
    assert "EXECUTABLE_IDENTITY" in {
        issue["code"] for issue in stdout_report["issues"]
    }
    assert result.read_bytes() == before_result
    assert report_path.read_bytes() == before_report


def test_update_final_m1_failure_preserves_existing_result_and_report_bytes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
):
    root = governed_tree(tmp_path)
    source_revision = git(root, "rev-parse", "HEAD")
    loaded = fixture_runner_module(root)
    _distributions, numpy_init = install_fake_dependency_environment(
        loaded,
        tmp_path / "dependencies",
        monkeypatch,
    )
    result = tmp_path / "preserved-result.json"
    report_path = tmp_path / "preserved-report.json"
    original_result = b"preexisting result sentinel\n"
    original_report = b"preexisting report sentinel\n"
    result.write_bytes(original_result)
    report_path.write_bytes(original_report)
    real_stage = loaded._stage_json_document
    stage_count = 0

    def stage_then_mutate_after_report(path: Path, value: object):
        nonlocal stage_count
        staged = real_stage(path, value)
        stage_count += 1
        if stage_count == 2:
            numpy_init.write_bytes(b"omega\n")
        return staged

    monkeypatch.setattr(loaded, "_stage_json_document", stage_then_mutate_after_report)

    returncode = loaded.main(
        [
            "--update",
            str(result),
            "--source-revision",
            source_revision,
            "--report",
            str(report_path),
        ],
        test_fixture=True,
    )

    stdout_report = json.loads(capsys.readouterr().out)
    assert returncode != 0
    assert stage_count == 2
    assert stdout_report["ok"] is False
    assert "EXECUTABLE_IDENTITY" in {
        issue["code"] for issue in stdout_report["issues"]
    }
    assert result.read_bytes() == original_result
    assert report_path.read_bytes() == original_report
    assert not list(tmp_path.glob("*.stage.tmp"))


def test_update_precommit_source_failure_preserves_existing_output_bytes(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
):
    root = governed_tree(tmp_path)
    source_revision = git(root, "rev-parse", "HEAD")
    loaded = fixture_runner_module(root)
    governed = root / "manuscripts/gauge_vfe_rg/main.tex"
    governed.write_bytes(governed.read_bytes() + b"dirty source mismatch\n")
    result = tmp_path / "early-failure-result.json"
    report_path = tmp_path / "early-failure-report.json"
    original_result = b"preexisting early result sentinel\n"
    original_report = b"preexisting early report sentinel\n"
    result.write_bytes(original_result)
    report_path.write_bytes(original_report)

    returncode = loaded.main(
        [
            "--update",
            str(result),
            "--source-revision",
            source_revision,
            "--report",
            str(report_path),
        ],
        test_fixture=True,
    )

    stdout_report = json.loads(capsys.readouterr().out)
    assert returncode != 0
    assert stdout_report["ok"] is False
    assert "SOURCE_BLOB_MISMATCH" in {
        issue["code"] for issue in stdout_report["issues"]
    }
    assert result.read_bytes() == original_result
    assert report_path.read_bytes() == original_report


def test_update_preflight_conflict_preserves_existing_output_bytes(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
):
    root = governed_tree(tmp_path)
    loaded = fixture_runner_module(root)
    result = root / "forbidden-result.json"
    report_path = tmp_path / "preflight-report.json"
    original_result = b"preexisting preflight result sentinel\n"
    original_report = b"preexisting preflight report sentinel\n"
    result.write_bytes(original_result)
    report_path.write_bytes(original_report)

    returncode = loaded.main(
        ["--update", str(result), "--report", str(report_path)],
        test_fixture=True,
    )

    stdout_report = json.loads(capsys.readouterr().out)
    assert returncode != 0
    assert stdout_report["ok"] is False
    assert "REPORT_TARGET_CONFLICT" in {
        issue["code"] for issue in stdout_report["issues"]
    }
    assert result.read_bytes() == original_result
    assert report_path.read_bytes() == original_report


def test_update_report_commit_failure_keeps_valid_result_and_stale_report_rejectable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
):
    root = governed_tree(tmp_path)
    source_revision = git(root, "rev-parse", "HEAD")
    loaded = fixture_runner_module(root)
    result = tmp_path / "committed-result.json"
    report_path = tmp_path / "stale-success-report.json"
    stale_hash = "0" * 64
    stale_receipt = "a" * 32
    stale_report = {
        "ok": True,
        "protocol_profile": SYNTHETIC_PROTOCOL_PROFILE,
        "source_revision": source_revision,
        "result_path": str(result.absolute()),
        "input_sha256_before": stale_hash,
        "input_sha256_after": stale_hash,
        "input_unchanged": True,
        "transaction_receipt_id": stale_receipt,
        "published_result_sha256": stale_hash,
        "issues": [],
    }
    stale_bytes = canonical_json_bytes(stale_report)
    report_path.write_bytes(stale_bytes)
    real_publish = loaded._publish_staged_json

    def fail_only_report_commit(staged, *, retain_handle: bool = False) -> None:
        if loaded._same_path(staged.target_path, report_path):
            raise PermissionError("synthetic report commit denial")
        real_publish(staged, retain_handle=retain_handle)

    monkeypatch.setattr(loaded, "_publish_staged_json", fail_only_report_commit)

    returncode = loaded.main(
        [
            "--update",
            str(result),
            "--source-revision",
            source_revision,
            "--report",
            str(report_path),
        ],
        test_fixture=True,
    )

    stdout_report = json.loads(capsys.readouterr().out)
    assert result.exists(), stdout_report
    result_document = json.loads(result.read_text(encoding="utf-8"))
    published_hash = hashlib.sha256(result.read_bytes()).hexdigest()
    retained_stale = json.loads(report_path.read_text(encoding="utf-8"))
    assert returncode != 0
    assert result_document["overall_status"] == "PASS"
    assert report_path.read_bytes() == stale_bytes
    assert stdout_report["ok"] is False
    assert stdout_report["published_result_sha256"] is None
    assert stdout_report["transaction_receipt_id"] != stale_receipt
    assert "ATOMIC_REPLACE" in {
        issue["code"] for issue in stdout_report["issues"]
    }
    assert retained_stale["published_result_sha256"] != published_hash
    assert retained_stale["input_sha256_after"] != published_hash
    assert retained_stale["transaction_receipt_id"] != stdout_report[
        "transaction_receipt_id"
    ]


@pytest.mark.parametrize("operation", ["update", "verify"])
def test_result_handle_denies_write_and_replace_through_report_commit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    operation: str,
):
    root = governed_tree(tmp_path)
    source_revision = git(root, "rev-parse", "HEAD")
    loaded = fixture_runner_module(root)
    result = tmp_path / f"held-through-report-{operation}.json"
    report_path = tmp_path / f"held-through-report-{operation}.report.json"
    if operation == "verify":
        baseline = loaded.build_result(root, source_revision, test_fixture=True)
        result.write_bytes(loaded.canonical_json_bytes(baseline))
    replacement = tmp_path / f"attacker-{operation}.json"
    replacement.write_bytes(b'{"attacker":true}')
    real_publish = loaded._publish_staged_json
    attack_attempted = False

    def publish_while_attacking_result(staged, *, retain_handle: bool = False):
        nonlocal attack_attempted
        if loaded._same_path(staged.target_path, report_path):
            attack_attempted = True
            with pytest.raises(PermissionError):
                result.write_bytes(b'{"attacker":true}')
            with pytest.raises(PermissionError):
                os.replace(replacement, result)
        real_publish(staged, retain_handle=retain_handle)

    monkeypatch.setattr(
        loaded,
        "_publish_staged_json",
        publish_while_attacking_result,
    )
    arguments = [
        f"--{operation}",
        str(result),
        "--report",
        str(report_path),
    ]
    if operation == "update":
        arguments.extend(["--source-revision", source_revision])

    returncode = loaded.main(arguments, test_fixture=True)

    captured = capsys.readouterr().out
    stdout_report = json.loads(captured)
    assert report_path.exists(), json.dumps(stdout_report, indent=2)
    report_bytes = report_path.read_bytes()
    assert captured.encode("utf-8") == report_bytes + b"\n"
    report_document = json.loads(report_bytes)
    current_hash = hashlib.sha256(result.read_bytes()).hexdigest()
    expected_report_keys = {
        "ok",
        "result_path",
        "source_revision",
        "input_sha256_before",
        "input_sha256_after",
        "input_unchanged",
        "transaction_receipt_id",
        "published_result_sha256",
        "semantic_payload_digest",
        "manifest_path_count",
        "check_count",
        "protocol_profile",
        "head_revision",
        "python_executable",
        "python_executable_sha256",
        "git_executable",
        "git_executable_sha256",
        "issues",
    }
    receipt = uuid.UUID(stdout_report["transaction_receipt_id"])
    assert returncode == 0
    assert attack_attempted is True
    assert set(stdout_report) == expected_report_keys
    assert set(report_document) == expected_report_keys
    assert receipt.version == 4
    assert receipt.hex == stdout_report["transaction_receipt_id"]
    assert stdout_report["ok"] is True
    assert report_document["ok"] is True
    assert report_document["published_result_sha256"] == current_hash
    assert report_document["input_sha256_after"] == current_hash


def test_result_guard_blocks_path_replacement_until_held_handle_closes(
    tmp_path: Path,
):
    loaded = runner_module()
    result = tmp_path / "held-result.json"
    replacement = tmp_path / "replacement.json"
    original = b'{"state":"held"}'
    result.write_bytes(original)
    replacement.write_bytes(b'{"state":"replacement"}')
    guard = loaded._WindowsExecutableGuard(result, "verification result witness")

    try:
        with pytest.raises(PermissionError):
            os.replace(replacement, result)
        payload, snapshot = guard.read()
        assert payload == original
        assert snapshot["sha256"] == hashlib.sha256(original).hexdigest()
    finally:
        guard.close()

    os.replace(replacement, result)
    assert result.read_bytes() == b'{"state":"replacement"}'


@pytest.mark.parametrize("target_exists", [False, True])
def test_retained_json_stage_denies_substitution_and_publishes_exact_handle(
    tmp_path: Path,
    target_exists: bool,
):
    loaded = runner_module()
    target = tmp_path / "transaction-result.json"
    replacement = tmp_path / "attacker-stage.json"
    if target_exists:
        target.write_bytes(b'{"state":"old"}')
    replacement.write_bytes(b'{"state":"attacker"}')
    expected = {"state": "authenticated"}
    staged = loaded._stage_json_document(target, expected)

    try:
        with pytest.raises(PermissionError):
            staged.temporary_path.write_bytes(b'{"state":"mutated"}')
        with pytest.raises(PermissionError):
            os.replace(replacement, staged.temporary_path)

        loaded._publish_staged_json(staged)

        assert target.read_bytes() == loaded.canonical_json_bytes(expected)
        assert hashlib.sha256(target.read_bytes()).hexdigest() == staged.payload_sha256
    finally:
        loaded._cleanup_staged_json(staged)


def test_retained_governed_registry_denies_policy_schema_and_claims_aba(
    tmp_path: Path,
):
    root = governed_tree(tmp_path)
    loaded = fixture_runner_module(root)
    relatives = (
        "manuscripts/gauge_vfe_rg/verification/manifest-policy.json",
        "manuscripts/gauge_vfe_rg/verification/result.schema.json",
        "manuscripts/gauge_vfe_rg/verification/claims.json",
    )
    evidence, tokens = loaded._acquire_run_evidence(root, test_fixture=True)

    try:
        for index, relative in enumerate(relatives):
            target = root / relative
            original = target.read_bytes()
            variant = tmp_path / f"variant-{index}.json"
            restored = tmp_path / f"restored-{index}.json"
            variant.write_bytes(b'{"attacker":"B"}')
            restored.write_bytes(original)

            with pytest.raises(PermissionError):
                target.write_bytes(b'{"attacker":"B"}')
            with pytest.raises(PermissionError):
                os.replace(variant, target)
            with pytest.raises(PermissionError):
                os.replace(restored, target)

            assert target.read_bytes() == original
            assert loaded._strict_json_file(target) == json.loads(original)

        loaded._require_run_evidence_unchanged(root, evidence)
    finally:
        loaded._release_run_evidence(tokens)


def test_stable_file_read_rejects_disappearance_after_initial_lstat(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    loaded = runner_module()
    target = tmp_path / "observed-metadata"
    target.write_bytes(b"")
    real_open = Path.open
    removed = False

    def remove_after_initial_observation(path: Path, *args, **kwargs):
        nonlocal removed
        if path == target and not removed:
            target.unlink()
            removed = True
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", remove_after_initial_observation)

    with pytest.raises(loaded._StableFileReadError, match="disappeared"):
        loaded._open_stable_regular_file(target)

    assert removed is True


def test_authenticated_loader_locks_origin_before_delegated_create_module(
    tmp_path: Path,
):
    loaded = runner_module()
    origin = tmp_path / "authenticated_module.py"
    original = b"VALUE = 1\n"
    origin.write_bytes(original)
    replacement_blocked = False

    class Delegate:
        def create_module(self, _spec):
            nonlocal replacement_blocked
            try:
                origin.write_bytes(b"VALUE = 2\n")
            except PermissionError:
                replacement_blocked = True
            return SimpleNamespace()

        def exec_module(self, _module):
            return None

    loader = loaded._AuthenticatedSiteLoader(
        Delegate(),
        origin,
        {
            "byte_count": len(original),
            "sha256": hashlib.sha256(original).hexdigest(),
        },
        "authenticated_module",
    )

    module = loader.create_module(SimpleNamespace())
    assert replacement_blocked is True
    assert loader._guard is not None
    loader.exec_module(module)
    assert loader._guard is None
    assert origin.read_bytes() == original

def test_runner_ignores_caller_path_when_selecting_fixed_git(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    root = governed_tree(tmp_path)
    source_revision = git(root, "rev-parse", "HEAD")
    shadow = tmp_path / "shadow-bin"
    shadow.mkdir()
    shutil.copy2(Path(os.environ["SystemRoot"]) / "System32/where.exe", shadow / "git.exe")
    monkeypatch.setenv("PATH", f"{shadow}{os.pathsep}{os.environ.get('PATH', '')}")
    loaded = fixture_runner_module(root)

    document = loaded.build_result(root, source_revision, test_fixture=True)

    assert document["overall_status"] == "PASS"
    assert document["environment"]["git_executable"] == str(FIXED_GIT_EXECUTABLE)


def test_ordinary_cli_rejects_nonisolated_pythonpath_startup(tmp_path: Path):
    root = governed_tree(tmp_path)
    result = tmp_path / "nonisolated.json"
    report = tmp_path / "nonisolated.report.json"
    caller_path = tmp_path / "caller-pythonpath"
    caller_path.mkdir()
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(caller_path)

    completed = subprocess.run(
        [
            str(FIXED_PYTHON_EXECUTABLE),
            "-B",
            str(root / RUNNER_RELATIVE),
            "--update",
            str(result),
            "--source-revision",
            git(root, "rev-parse", "HEAD"),
            "--report",
            str(report),
        ],
        cwd=root,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode != 0
    assert not result.exists()
    assert not report.exists()
    assert "-i -s" in completed.stderr.lower(), (
        "DEFECT [isolated CLI]: ordinary production startup must reject before "
        f"third-party imports; stdout={completed.stdout!r} stderr={completed.stderr!r}"
    )


def test_isolated_import_authenticates_only_runtime_dependencies_and_empty_pycache():
    harness = (
        "import importlib.util,json,pathlib,sys;"
        "p=pathlib.Path(sys.argv[1]);"
        "s=importlib.util.spec_from_file_location('isolated_runner_probe',p);"
        "m=importlib.util.module_from_spec(s);"
        "s.loader.exec_module(m);"
        "blocked=False;"
        "\ntry:\n import charset_normalizer\nexcept ImportError:\n blocked=True\n"
        "cache=pathlib.Path(m._AUTHENTICATED_PYCACHE_DIRECTORY.name);"
        "print(json.dumps({'pypdf': 'pypdf' in sys.modules,"
        "'pytest': 'pytest' in sys.modules,"
        "'charset': 'charset_normalizer' in sys.modules,"
        "'undeclared_blocked': blocked,"
        "'dont_write_bytecode': sys.dont_write_bytecode,"
        "'pycache_entries': sorted(x.name for x in cache.iterdir())},sort_keys=True))"
    )

    completed = subprocess.run(
        [
            str(FIXED_PYTHON_EXECUTABLE),
            "-I",
            "-S",
            "-B",
            "-c",
            harness,
            str(RUNNER),
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    observed = json.loads(completed.stdout)
    assert observed == {
        "charset": False,
        "dont_write_bytecode": True,
        "pycache_entries": [],
        "pypdf": False,
        "pytest": False,
        "undeclared_blocked": True,
    }


def test_runner_rejects_empty_alternates_through_reparse_parent(tmp_path: Path):
    root = governed_tree(tmp_path)
    loaded = fixture_runner_module(root)
    info_path = root / ".git/objects/info"
    external_info = tmp_path / "external-object-info"
    external_info.mkdir()
    (external_info / "alternates").touch()
    if info_path.exists():
        shutil.rmtree(info_path)
    completed = subprocess.run(
        [
            os.environ.get("COMSPEC", r"C:\Windows\System32\cmd.exe"),
            "/d",
            "/c",
            "mklink",
            "/J",
            str(info_path),
            str(external_info),
        ],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr or completed.stdout

    try:
        with pytest.raises(loaded.VerificationFailure) as caught:
            loaded._reject_git_metadata_overrides(root)
    finally:
        os.rmdir(info_path)

    assert caught.value.code == "GIT_METADATA_OVERRIDE"
    assert "reparse" in str(caught.value).lower()


def test_source_binding_rechecks_git_metadata_after_object_reads(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    root = governed_tree(tmp_path)
    source_revision = git(root, "rev-parse", "HEAD")
    loaded = fixture_runner_module(root)
    manifest = loaded.build_manifest(root, test_fixture=True)
    metadata = root / ".git/objects/info/http-alternates"
    real_git = loaded._git
    inserted = False

    def mutating_git(repo_root, *arguments, **kwargs):
        nonlocal inserted
        completed = real_git(repo_root, *arguments, **kwargs)
        if not inserted and arguments[:2] == ("cat-file", "blob"):
            metadata.parent.mkdir(parents=True, exist_ok=True)
            metadata.write_text(
                "https://objects.example.invalid/repository/objects\n",
                encoding="utf-8",
            )
            inserted = True
        return completed

    monkeypatch.setattr(loaded, "_git", mutating_git)
    try:
        with pytest.raises(loaded.VerificationFailure) as caught:
            loaded._source_binding_issues(
                root,
                source_revision,
                manifest,
                test_fixture=True,
            )
    finally:
        metadata.unlink(missing_ok=True)

    assert inserted is True
    assert caught.value.code == "GIT_METADATA_OVERRIDE"
    assert "http-alternates" in str(caught.value.location)


def test_git_subprocess_postflight_rejects_boundary_visible_metadata_mutation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    root = governed_tree(tmp_path)
    loaded = fixture_runner_module(root)
    real_run = loaded.subprocess.run
    metadata = root / ".git/info/grafts"
    mutated = False

    def mutate_before_subprocess_returns(command, *args, **kwargs):
        nonlocal mutated
        completed = real_run(command, *args, **kwargs)
        if not mutated:
            metadata.parent.mkdir(parents=True, exist_ok=True)
            metadata.write_bytes(b"forbidden\n")
            mutated = True
        return completed

    monkeypatch.setattr(loaded.subprocess, "run", mutate_before_subprocess_returns)
    try:
        with pytest.raises(loaded.VerificationFailure) as caught:
            loaded._git(root, "rev-parse", "HEAD")
    finally:
        metadata.unlink(missing_ok=True)

    assert mutated is True
    assert caught.value.code == "GIT_METADATA_OVERRIDE"


def test_git_subprocess_launch_exception_still_executes_metadata_postflight(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    root = governed_tree(tmp_path)
    loaded = fixture_runner_module(root)
    real_metadata_check = loaded._reject_git_metadata_overrides
    metadata_checks = 0

    def counting_metadata_check(repo_root: Path, **kwargs):
        nonlocal metadata_checks
        metadata_checks += 1
        return real_metadata_check(repo_root, **kwargs)

    def launch_failure(*_args, **_kwargs):
        raise OSError("synthetic Git launch failure")

    monkeypatch.setattr(
        loaded,
        "_reject_git_metadata_overrides",
        counting_metadata_check,
    )
    monkeypatch.setattr(loaded.subprocess, "run", launch_failure)

    with pytest.raises(OSError, match="synthetic Git launch failure"):
        loaded._git(root, "rev-parse", "HEAD")

    assert metadata_checks == 3


def test_git_launch_exception_still_detects_executable_identity_change(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    root = governed_tree(tmp_path)
    loaded = fixture_runner_module(root)
    real_identity = loaded._stable_executable_identity
    identity_calls = 0

    def drifting_identity(path: Path, role: str):
        nonlocal identity_calls
        identity = real_identity(path, role)
        if role == "Git":
            identity_calls += 1
            if identity_calls > 1:
                identity = {**identity, "sha256": "f" * 64}
        return identity

    def launch_failure(*_args, **_kwargs):
        raise OSError("synthetic Git launch failure")

    monkeypatch.setattr(loaded, "_stable_executable_identity", drifting_identity)
    monkeypatch.setattr(loaded.subprocess, "run", launch_failure)

    with pytest.raises(OSError, match="synthetic Git launch failure") as caught:
        loaded._git(root, "rev-parse", "HEAD")

    assert identity_calls >= 2
    assert isinstance(caught.value.__cause__, loaded.VerificationFailure)
    assert caught.value.__cause__.code == "EXECUTABLE_IDENTITY"


@pytest.mark.parametrize("operation", ["update", "verify"])
def test_update_and_verify_reject_head_move_during_final_source_binding(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    operation: str,
):
    root = governed_tree(tmp_path)
    source_revision = git(root, "rev-parse", "HEAD")
    source_tree = git(root, "rev-parse", f"{source_revision}^{{tree}}")
    non_descendant = git(
        root,
        "-c",
        "user.name=Runner Contract",
        "-c",
        "user.email=runner-contract@example.invalid",
        "commit-tree",
        source_tree,
        "-m",
        "unrelated HEAD with identical governed tree",
    )
    loaded = fixture_runner_module(root)
    result = tmp_path / f"head-toctou-{operation}.json"
    report_path = tmp_path / f"head-toctou-{operation}.report.json"
    if operation == "verify":
        baseline = loaded.build_result(root, source_revision, test_fixture=True)
        result.write_bytes(loaded.canonical_json_bytes(baseline))

    real_metadata_check = loaded._reject_git_metadata_overrides
    metadata_checks = 0

    def metadata_check_then_move_head(repo_root: Path, **kwargs) -> None:
        nonlocal metadata_checks
        real_metadata_check(repo_root, **kwargs)
        metadata_checks += 1
        if metadata_checks == 4:
            git(root, "update-ref", "HEAD", non_descendant)

    monkeypatch.setattr(
        loaded,
        "_reject_git_metadata_overrides",
        metadata_check_then_move_head,
    )

    if operation == "update":
        returncode = loaded.main(
            [
                "--update",
                str(result),
                "--source-revision",
                source_revision,
                "--report",
                str(report_path),
            ],
            test_fixture=True,
        )
        codes = report_codes(report_path)
        assert returncode != 0
        assert not result.exists()
    else:
        report = loaded.verify_result(result, root, test_fixture=True)
        codes = {issue.code for issue in report.issues}
        assert report.ok is False

    assert metadata_checks >= 4
    assert "SOURCE_REVISION_NOT_ANCESTOR" in codes, (
        "DEFECT [source HEAD TOCTOU]: the final source-binding close accepted a "
        f"stale HEAD during {operation}; got {sorted(codes)}"
    )


@pytest.mark.parametrize("kind", ["tex", "test"])
def test_cli_update_rejects_recursive_source_tree_shrink(
    tmp_path: Path,
    kind: str,
):
    root = governed_tree(tmp_path)
    policy = root / "manuscripts/gauge_vfe_rg/verification/manifest-policy.json"
    rewrite_json(policy, lambda document: document.pop("bound_paths"))
    source_revision = commit_all(root, "source S without redundant bound-path inventory")
    relative = (
        "manuscripts/gauge_vfe_rg/nested/child.tex"
        if kind == "tex"
        else "manuscripts/gauge_vfe_rg/verification/tests/test_manifest_binding.py"
    )
    (root / relative).unlink()
    result, report = tmp_path / f"shrunken-{kind}.json", tmp_path / f"shrunken-{kind}.report.json"

    completed = invoke(
        root,
        "--update",
        str(result),
        "--source-revision",
        source_revision,
        "--report",
        str(report),
    )

    assert completed.returncode != 0, (
        f"DEFECT [recursive {kind} shrink]: update accepted a governed path deleted after S"
    )
    assert not result.exists()
    assert "MANIFEST_PATH_SET_MISMATCH" in report_codes(report), (
        f"DEFECT [recursive {kind} shrink specificity]: got {sorted(report_codes(report))}"
    )


def test_cli_ignores_caller_git_identity_redirection(tmp_path: Path):
    root = governed_tree(tmp_path)
    foreign = tmp_path / "foreign-repo"
    shutil.copytree(root, foreign)
    evidence = foreign / "docs/foreign-only.txt"
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text("foreign object database\n", encoding="utf-8")
    foreign_revision = commit_all(foreign, "foreign-only revision")
    clean_environment = {
        key: value
        for key, value in os.environ.items()
        if not key.upper().startswith("GIT_")
    }
    local_probe = subprocess.run(
        ["git", "cat-file", "-e", f"{foreign_revision}^{{commit}}"],
        cwd=root,
        env=clean_environment,
        text=True,
        capture_output=True,
        check=False,
    )
    assert local_probe.returncode != 0, (
        "DEFECT [ambient Git identity fixture]: foreign revision unexpectedly exists "
        "in the target object database"
    )
    result, report = tmp_path / "foreign-result.json", tmp_path / "foreign.report.json"

    completed = invoke(
        root,
        "--update",
        str(result),
        "--source-revision",
        foreign_revision,
        "--report",
        str(report),
        env_overrides={
            "GIT_DIR": str(foreign / ".git"),
            "GIT_WORK_TREE": str(root),
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "core.repositoryformatversion",
            "GIT_CONFIG_VALUE_0": "0",
        },
    )

    assert completed.returncode != 0, (
        "DEFECT [ambient Git identity]: update accepted a revision reachable only "
        "through caller GIT_DIR/GIT_WORK_TREE"
    )
    assert not result.exists()
    assert "SOURCE_REVISION_NOT_FOUND" in report_codes(report), (
        f"DEFECT [ambient Git identity specificity]: got {sorted(report_codes(report))}"
    )


@pytest.mark.parametrize("metadata", ["info/grafts", "shallow"])
def test_cli_rejects_git_ancestry_metadata_overrides(
    tmp_path: Path,
    metadata: str,
):
    root = governed_tree(tmp_path)
    revision = git(root, "rev-parse", "HEAD")
    override = root / ".git" / metadata
    override.parent.mkdir(parents=True, exist_ok=True)
    override.write_text(revision + "\n", encoding="ascii")
    result, report = tmp_path / "metadata-result.json", tmp_path / "metadata.report.json"

    completed = invoke(
        root,
        "--update",
        str(result),
        "--source-revision",
        revision,
        "--report",
        str(report),
    )

    assert completed.returncode != 0, (
        f"DEFECT [Git {metadata} override]: ancestry-affecting metadata was accepted"
    )
    assert not result.exists()
    assert "GIT_METADATA_OVERRIDE" in report_codes(report), (
        f"DEFECT [Git {metadata} override specificity]: got {sorted(report_codes(report))}"
    )


@pytest.mark.parametrize("kind", ["update", "report", "external-dot-git"])
def test_cli_rejects_destructive_targets_inside_repository_or_dot_git(
    tmp_path: Path,
    kind: str,
):
    root = governed_tree(tmp_path)
    external_result = tmp_path / f"{kind}-result.json"
    external_report = tmp_path / f"{kind}-report.json"
    if kind == "update":
        result = root / "docs/forbidden-result.json"
        report = external_report
    elif kind == "report":
        result = external_result
        report = root / "docs/forbidden-report.json"
    else:
        result = tmp_path / "external" / ".git" / "forbidden-result.json"
        report = external_report

    completed = invoke(root, "--update", str(result), "--report", str(report))

    assert completed.returncode != 0, f"DEFECT [target containment {kind}]: target was accepted"
    assert not result.exists(), f"DEFECT [target containment {kind}]: result target was written"
    if kind == "report":
        assert not report.exists(), "DEFECT [target containment report]: unsafe report was written"
    assert json.loads(completed.stdout)["issues"][0]["code"] == "REPORT_TARGET_CONFLICT", (
        f"DEFECT [target containment {kind} specificity]: {completed.stdout}"
    )


def test_linked_worktree_git_pointer_is_never_a_writable_result_target(tmp_path: Path):
    root = governed_tree(tmp_path)
    linked = tmp_path / "linked-worktree"
    git(root, "worktree", "add", "--quiet", "--detach", str(linked), "HEAD")
    pointer = linked / ".git"
    before = pointer.read_bytes()
    report = tmp_path / "linked-worktree.report.json"

    completed = invoke(linked, "--update", str(pointer), "--report", str(report))

    assert completed.returncode != 0, (
        "DEFECT [linked-worktree .git pointer]: destructive target was accepted"
    )
    assert pointer.read_bytes() == before, (
        "DEFECT [linked-worktree .git pointer]: .git pointer bytes were replaced"
    )
    assert "REPORT_TARGET_CONFLICT" in report_codes(report), (
        f"DEFECT [linked-worktree .git pointer specificity]: got {sorted(report_codes(report))}"
    )


def test_cli_requires_exactly_one_positional_mode_and_result(tmp_path: Path):
    root = governed_tree(tmp_path)
    neither = invoke(root)
    both = invoke(root, "--update", "result.json", "--verify", "result.json")
    assert neither.returncode != 0, "DEFECT [implicit mode]: runner must reject no mode"
    assert both.returncode != 0, "DEFECT [conflicting modes]: runner must reject both modes"
    assert "--update RESULT" in neither.stderr + neither.stdout, "DEFECT [usage]: positional --update RESULT contract missing"


def test_update_then_verify_preserves_result_and_writes_only_explicit_report(tmp_path: Path):
    root, result, report = governed_tree(tmp_path), tmp_path / "result.json", tmp_path / "report.json"
    update = invoke(root, "--update", str(result))
    assert update.returncode == 0, f"DEFECT [update]: positional --update RESULT failed: {update.stderr}"
    before, before_inventory = result.read_bytes(), files(tmp_path)
    verify = invoke(root, "--verify", str(result), "--report", str(report))
    assert verify.returncode == 0, f"DEFECT [verify]: positional --verify RESULT failed: {verify.stderr}"
    assert result.read_bytes() == before, "DEFECT [verify immutability]: verify rewrote its input result"
    assert_only_report_added(before_inventory, files(tmp_path), report, "verify writes")


@pytest.mark.parametrize("corruption", ["trailing_whitespace", "semantic", "profile", "revision", "nan", "infinity"])
def test_each_real_result_corruption_fails_without_mutating_input_or_other_files(tmp_path: Path, corruption: str):
    root, result, report = governed_tree(tmp_path), tmp_path / "result.json", tmp_path / f"{corruption}.report.json"
    bootstrap = invoke(root, "--update", str(result))
    assert bootstrap.returncode == 0, f"DEFECT [{corruption} fixture]: update must create a valid result"
    document = json.loads(result.read_text(encoding="utf-8"))
    if corruption == "trailing_whitespace":
        old = result.read_bytes()
        corrupted = old + b"\n"
        assert corrupted != old and json.loads(corrupted.decode("utf-8")) == document
        result.write_bytes(corrupted)
    elif corruption == "semantic":
        document["semantic_payload_digest"] = "0" * 64
        result.write_bytes(canonical_json_bytes(document))
    elif corruption == "profile":
        document["protocol_profile"] = PRODUCTION_PROTOCOL_PROFILE
        refresh_semantic_digest(document)
        result.write_bytes(canonical_json_bytes(document))
    elif corruption == "revision":
        document["source_revision"] = "0" * 40
        refresh_semantic_digest(document)
        result.write_bytes(canonical_json_bytes(document))
    else:
        document["checks"][0]["observed"]["number"] = float("nan" if corruption == "nan" else "inf")
        result.write_text(json.dumps(document, sort_keys=True, separators=(",", ":"), allow_nan=True), encoding="utf-8")
    before, inventory = result.read_bytes(), files(tmp_path)
    verify = invoke(root, "--verify", str(result), "--report", str(report))
    assert verify.returncode != 0, f"DEFECT [{corruption}]: verifier accepted a real corrupted result"
    assert result.read_bytes() == before, f"DEFECT [{corruption}]: verifier rewrote corrupted input"
    assert_only_report_added(inventory, files(tmp_path), report, f"{corruption} immutability")
    expected_code = {
        "trailing_whitespace": "NONCANONICAL_RESULT_BYTES",
        "semantic": "SEMANTIC_DIGEST_MISMATCH",
        "profile": "SEMANTIC_RECOMPUTATION_MISMATCH",
        "revision": "SOURCE_REVISION_NOT_FOUND",
        "nan": "NONFINITE_JSON",
        "infinity": "NONFINITE_JSON",
    }[corruption]
    assert expected_code in report_codes(report), f"DEFECT [{corruption} specificity]: expected {expected_code}, got {sorted(report_codes(report))}"


@pytest.mark.parametrize(
    "timestamp",
    [
        "2026-02-29T12:00:00Z",
        "2026-13-01T12:00:00Z",
        "2026-12-01T24:00:00Z",
        "2026-12-01T23:60:00Z",
    ],
)
def test_verify_rejects_impossible_whole_second_utc_timestamp(
    tmp_path: Path,
    timestamp: str,
):
    root = governed_tree(tmp_path)
    source_revision = git(root, "rev-parse", "HEAD")
    loaded = fixture_runner_module(root)
    document = loaded.build_result(root, source_revision, test_fixture=True)
    document["generated_at_utc"] = timestamp
    refresh_semantic_digest(document)
    result = tmp_path / "invalid-calendar-result.json"
    result.write_bytes(loaded.canonical_json_bytes(document))

    report = loaded.verify_result(result, root, test_fixture=True)

    assert report.ok is False
    schema_issues = [issue for issue in report.issues if issue.code == "SCHEMA_VIOLATION"]
    assert schema_issues
    assert "calendar" in str(schema_issues[0].observed).lower()


def test_atomic_update_replaces_sentinel_without_temp_leak(tmp_path: Path):
    root = governed_tree(tmp_path)
    success_result = tmp_path / "success.json"
    success_result.write_bytes(b"SUCCESS-SENTINEL")
    update = invoke(root, "--update", str(success_result))
    assert update.returncode == 0 and success_result.read_bytes() != b"SUCCESS-SENTINEL", "DEFECT [atomic replace]: update must replace existing sentinel"
    assert set(path.name for path in tmp_path.iterdir()) == {"repo", "success.json"}, "DEFECT [atomic replace]: successful update leaked a temporary artifact"


def test_canonical_current_results_update_succeeds_without_temp_leak(tmp_path: Path):
    root = governed_tree(tmp_path)
    target = root / "manuscripts/gauge_vfe_rg/verification/current-results.json"
    update = invoke(root, "--update", str(target))
    assert update.returncode == 0, (
        "DEFECT [canonical update]: governed current-results update failed: "
        f"{update.stderr}{update.stdout}"
    )
    assert target.is_file(), "DEFECT [canonical update]: current-results.json was not written"
    assert not list(target.parent.glob(".current-results.json.*.tmp")), (
        "DEFECT [canonical update]: same-directory staging temporary leaked"
    )
    verify = invoke(root, "--verify", str(target))
    assert verify.returncode == 0, (
        "DEFECT [canonical update]: freshly written current-results did not verify: "
        f"{verify.stderr}{verify.stdout}"
    )


def test_failed_atomic_update_preserves_sentinel_and_leaks_only_explicit_report(tmp_path: Path):
    root = governed_tree(tmp_path)
    failed_result, report = tmp_path / "failed.json", tmp_path / "failed.report.json"
    failed_result.write_bytes(b"FAILURE-SENTINEL")
    claims = root / "manuscripts/gauge_vfe_rg/verification/claims.json"
    claims.write_bytes(claims.read_bytes() + b"\n")
    before_failure = files(tmp_path)
    failed = invoke(
        root,
        "--update", str(failed_result),
        "--source-revision", git(root, "rev-parse", "HEAD"),
        "--report", str(report),
    )
    assert failed.returncode != 0, "DEFECT [failed atomic update]: governed source drift must fail update"
    assert failed_result.read_bytes() == b"FAILURE-SENTINEL", "DEFECT [failed atomic update]: failure changed the sentinel target"
    assert_only_report_added(before_failure, files(tmp_path), report, "failed atomic update")
    assert "SOURCE_BLOB_MISMATCH" in report_codes(report), f"DEFECT [failed atomic update specificity]: got {sorted(report_codes(report))}"


def test_public_atomic_write_is_all_or_nothing_under_success_serialization_failure_and_reader_race(tmp_path: Path):
    target = tmp_path / "result.json"
    target.write_text(json.dumps({"state": "old"}), encoding="utf-8")
    atomic_write = runner_api("atomic_write_json", "public atomic write")
    assert not isinstance(atomic_write, MissingAtomicWrite), "DEFECT [public atomic write]: run_checks.py must export atomic_write_json"
    old_bytes = target.read_bytes()
    old_hash = hashlib.sha256(old_bytes).hexdigest()
    observed_errors: list[str] = []
    observed_hashes: list[str] = []
    overlap_reads = [0]
    old_read, writer_alive, stop = threading.Event(), threading.Event(), threading.Event()

    def reader() -> None:
        while not stop.is_set():
            try:
                raw = target.read_bytes()
                json.loads(raw.decode("utf-8"))
                observed_hashes.append(hashlib.sha256(raw).hexdigest())
                old_read.set()
                if writer_alive.is_set():
                    overlap_reads[0] += 1
            except (OSError, json.JSONDecodeError) as exc:
                observed_errors.append(type(exc).__name__)

    thread = threading.Thread(target=reader, daemon=True)
    thread.start()
    assert old_read.wait(timeout=2), "DEFECT [public atomic write]: reader never completed an old-file read before writer start"
    new_document = {"state": "new", "payload": "x" * 20_000_000}
    new_bytes = json.dumps(new_document, sort_keys=True, separators=(",", ":")).encode("utf-8")
    new_hash = hashlib.sha256(new_bytes).hexdigest()

    def writer() -> None:
        writer_alive.set()
        try:
            atomic_write(target, new_document)
        finally:
            writer_alive.clear()

    writer_thread = threading.Thread(target=writer, daemon=True)
    writer_thread.start()
    writer_thread.join(timeout=10)
    assert not writer_thread.is_alive(), "DEFECT [public atomic write]: writer did not complete"
    stop.set()
    thread.join(timeout=2)
    assert not thread.is_alive(), "DEFECT [public atomic write]: reader thread did not terminate"
    assert old_hash in observed_hashes, "DEFECT [public atomic write]: reader did not observe the old complete document"
    assert overlap_reads[0] > 0, "DEFECT [public atomic write]: reader completed no read while writer was alive"
    assert set(observed_hashes) <= {old_hash, new_hash}, "DEFECT [public atomic write]: reader observed bytes other than complete old/new JSON"
    assert hashlib.sha256(target.read_bytes()).hexdigest() == new_hash, "DEFECT [public atomic write]: successful write did not replace the exact new document"
    assert not observed_errors, f"DEFECT [public atomic write]: reader observed partial JSON: {observed_errors}"
    before_failure = target.read_bytes()
    with pytest.raises((TypeError, ValueError)):
        atomic_write(target, {"unserializable": object()})
    assert target.read_bytes() == before_failure, "DEFECT [serialization failure]: failed public write changed existing bytes"
    assert list(tmp_path.iterdir()) == [target], "DEFECT [serialization failure]: failed public write leaked temporary files"
