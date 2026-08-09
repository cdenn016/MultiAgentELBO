"""Adversarial contract for the external, non-self-authenticating release bootstrap."""

from __future__ import annotations

import atexit
import base64
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import zlib
from pathlib import Path

import pytest


REFERENCE_PATH = Path(__file__).resolve().parents[1] / "build_bootstrap_reference.ps1.txt"
TRANSPORT_PATH = Path(__file__).resolve().parents[1] / "build_bootstrap_transport.txt"
AUDIT_MODULE_PATH = Path(__file__).resolve().parents[1] / "build_audit.py"
BUILD_SCRIPT_PATH = Path(__file__).resolve().parents[2] / "build.ps1"
POWERSHELL = Path(r"C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe")
TRUSTED_GIT = Path(r"C:\Program Files\Git\cmd\git.exe")
TRUSTED_PYTHON = Path(r"C:\Python314\python.exe")
TRUSTED_PYPDF_SITE = Path(
    r"C:\Users\chris and christine\AppData\Roaming\Python\Python314\site-packages"
)
PRODUCTION_PROFILE = "gauge-vfe-rg-production-v1"
_LOADED_AUDIT_MODULES: list[object] = []


def _dispose_test_audit_module(loaded: object) -> None:
    """Release process-global resources owned by one dynamic test import."""

    finder = getattr(loaded, "_PYPDF_SITE_FINDER", None)
    if finder is not None:
        sys.meta_path[:] = [candidate for candidate in sys.meta_path if candidate is not finder]
    for cleanup_name in (
        "_cleanup_audit_executable_locks",
        "_cleanup_controlled_pycache_root",
    ):
        cleanup = getattr(loaded, cleanup_name, None)
        if callable(cleanup):
            cleanup()
            atexit.unregister(cleanup)


@pytest.fixture(autouse=True)
def isolate_dynamic_audit_module_process_state():
    """Keep production-lifetime import guards inside the unit test that loaded them."""

    meta_path_before = list(sys.meta_path)
    pycache_prefix_before = sys.pycache_prefix
    dont_write_bytecode_before = sys.dont_write_bytecode
    first_new_module = len(_LOADED_AUDIT_MODULES)
    try:
        yield
    finally:
        loaded_here = _LOADED_AUDIT_MODULES[first_new_module:]
        del _LOADED_AUDIT_MODULES[first_new_module:]
        for loaded in reversed(loaded_here):
            _dispose_test_audit_module(loaded)
        sys.meta_path[:] = meta_path_before
        sys.pycache_prefix = pycache_prefix_before
        sys.dont_write_bytecode = dont_write_bytecode_before


def audit_module(name: str):
    """Load one auditor instance and register its test-owned process state."""

    spec = importlib.util.spec_from_file_location(name, AUDIT_MODULE_PATH)
    assert spec and spec.loader
    loaded = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(loaded)
    finally:
        _LOADED_AUDIT_MODULES.append(loaded)
    return loaded


def git(repo: Path, *arguments: str) -> str:
    """Run the fixed Git executable for one disposable fixture repository."""

    completed = subprocess.run(
        [str(TRUSTED_GIT), "--no-replace-objects", "-C", str(repo), *arguments],
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    return completed.stdout.strip()


def commit(repo: Path, message: str) -> str:
    """Commit all current fixture files and return the full revision."""

    git(repo, "add", "--all")
    git(
        repo,
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit",
        "-m",
        message,
    )
    return git(repo, "rev-parse", "HEAD^{commit}")


def _safe_build_driver() -> str:
    return r'''[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$RepositoryRoot,
    [Parameter(Mandatory = $true)][string]$SourceDirectory,
    [Parameter(Mandatory = $true)][string]$RepositoryBuildScript,
    [Parameter(Mandatory = $true)][string]$ExecutedBuildScript,
    [Parameter(Mandatory = $true)][string]$BootstrapAttestationPath,
    [Parameter(Mandatory = $true)][string]$OutputDirectory,
    [Parameter(Mandatory = $true)][string]$AuditPath,
    [Parameter(Mandatory = $true)][string]$SourceRevision,
    [Parameter(Mandatory = $true)][string]$VerificationResult,
    [Parameter(Mandatory = $true)][string]$VerificationReport,
    [Parameter(Mandatory = $true)][string]$PdflatexPath,
    [Parameter(Mandatory = $true)][string]$BibtexPath,
    [Parameter(Mandatory = $true)][string]$BibtexStylePath
)
$ErrorActionPreference = 'Stop'
if ($PSCommandPath) { throw 'Authenticated in-memory child unexpectedly has PSCommandPath.' }
[void][System.IO.Directory]::CreateDirectory($OutputDirectory)
$utf8 = New-Object System.Text.UTF8Encoding($false)
function Get-Sha256([string]$Path) {
    $stream = [System.IO.File]::Open(
        $Path, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read,
        [System.IO.FileShare]::Read
    )
    $digest = [System.Security.Cryptography.SHA256]::Create()
    try {
        return ([BitConverter]::ToString($digest.ComputeHash($stream))).Replace('-', '').ToLowerInvariant()
    }
    finally { $digest.Dispose(); $stream.Dispose() }
}
function Get-Identity([string]$Path) {
    $full = [System.IO.Path]::GetFullPath($Path)
    return [ordered]@{
        path = $full
        sha256 = Get-Sha256 $full
        byte_count = [int64](Get-Item -LiteralPath $full).Length
    }
}
$attestation = Get-Content -LiteralPath $BootstrapAttestationPath -Raw | ConvertFrom-Json
$recorderPaths = [ordered]@{}
foreach ($pass in @('pass_1', 'pass_3', 'pass_4')) {
    $recorderPath = Join-Path $OutputDirectory "$pass.fls"
    [System.IO.File]::WriteAllText($recorderPath, "PWD $OutputDirectory`n", $utf8)
    $recorderPaths[$pass] = Get-Identity $recorderPath
}
$externalIdentity = Get-Identity $BibtexStylePath
$fixedInputs = [ordered]@{}
$fixedInputs[[System.IO.Path]::GetFullPath($BibtexStylePath)] = [ordered]@{
    sha256 = $externalIdentity.sha256
    byte_count = $externalIdentity.byte_count
}
$buildInputs = [ordered]@{}
foreach ($pass in @('pass_1', 'pass_3', 'pass_4')) {
    $record = $recorderPaths[$pass]
    $buildInputs["$pass.fls"] = [ordered]@{
        sha256 = $record.sha256
        byte_count = $record.byte_count
    }
}
$context = [ordered]@{
    protocol_profile = 'gauge-vfe-rg-production-v1'
    source_revision = $SourceRevision
    repository_root = [System.IO.Path]::GetFullPath($RepositoryRoot)
    source_directory = [System.IO.Path]::GetFullPath($SourceDirectory)
    repository_build_script = [ordered]@{
        path = [System.IO.Path]::GetFullPath($RepositoryBuildScript)
        sha256 = [string]$attestation.source_sha256
        byte_count = [int64]$attestation.source_blob_byte_count
    }
    executed_build_script = [ordered]@{
        path = [System.IO.Path]::GetFullPath($ExecutedBuildScript)
        sha256 = [string]$attestation.source_sha256
        byte_count = [int64]$attestation.source_blob_byte_count
    }
    bootstrap_attestation = Get-Identity $BootstrapAttestationPath
    external_input_fixed_point = [ordered]@{
        max_iterations = 8
        converged_iteration = 2
        inputs = $fixedInputs
    }
    recorder_snapshots = $recorderPaths
    evidence_input_inventory = [ordered]@{
        repository = [ordered]@{}
        build = $buildInputs
        external = $fixedInputs
    }
    pdflatex_path = [System.IO.Path]::GetFullPath($PdflatexPath)
    bibtex_path = [System.IO.Path]::GetFullPath($BibtexPath)
    bibtex_style_path = [System.IO.Path]::GetFullPath($BibtexStylePath)
    attested_blob_oid = [string]$attestation.source_blob_oid
}
$contextBytes = $utf8.GetBytes(($context | ConvertTo-Json -Compress -Depth 8))
[System.IO.File]::WriteAllBytes((Join-Path $OutputDirectory 'build-context.json'), $contextBytes)
[System.IO.File]::WriteAllBytes((Join-Path $OutputDirectory 'main.pdf'), [System.Text.Encoding]::ASCII.GetBytes('FAKE_PDF'))
$artifactHashes = [ordered]@{}
foreach ($artifact in @(Get-ChildItem -LiteralPath $OutputDirectory -File -Recurse | Sort-Object FullName)) {
    $relative = $artifact.FullName.Substring($OutputDirectory.Length).TrimStart('\').Replace('\', '/')
    $artifactHashes[$relative] = Get-Sha256 $artifact.FullName
}
$audit = [ordered]@{
    ok = $true
    protocol_profile = 'gauge-vfe-rg-production-v1'
    source_revision = $SourceRevision
    build_context = $context
    artifact_hashes = $artifactHashes
}
[System.IO.File]::WriteAllText($AuditPath, ($audit | ConvertTo-Json -Compress -Depth 8), $utf8)
$resultSha256 = Get-Sha256 $VerificationResult
$headRevision = (& 'C:\Program Files\Git\cmd\git.exe' --no-replace-objects --literal-pathspecs -C $RepositoryRoot rev-parse --verify 'HEAD^{commit}').Trim()
if ($LASTEXITCODE -ne 0 -or $headRevision -notmatch '^[0-9a-f]{40}$') { throw 'Cannot resolve current HEAD.' }
$report = [ordered]@{
    check_count = 1
    git_executable = 'C:\Program Files\Git\cmd\git.exe'
    git_executable_sha256 = Get-Sha256 'C:\Program Files\Git\cmd\git.exe'
    head_revision = $headRevision
    input_sha256_after = $resultSha256
    input_sha256_before = $resultSha256
    input_unchanged = $true
    issues = @()
    manifest_path_count = 1
    ok = $true
    protocol_profile = 'gauge-vfe-rg-production-v1'
    published_result_sha256 = $resultSha256
    python_executable = 'C:\Python314\python.exe'
    python_executable_sha256 = Get-Sha256 'C:\Python314\python.exe'
    result_path = [System.IO.Path]::GetFullPath($VerificationResult)
    semantic_payload_digest = ('3' * 64)
    source_revision = $SourceRevision
    transaction_receipt_id = '123e4567e89b42d3a456426614174000'
}
[System.IO.File]::WriteAllText($VerificationReport, ($report | ConvertTo-Json -Compress -Depth 8), $utf8)
[System.IO.File]::WriteAllText("$VerificationReport.trace", 'SAFE_BUILD', [System.Text.Encoding]::UTF8)
$auditSha256 = Get-Sha256 $AuditPath
$reportSha256 = Get-Sha256 $VerificationReport
[Console]::Out.WriteLine("BUILD_AUDIT_SHA256=$auditSha256")
[Console]::Out.WriteLine("BUILD_VERIFICATION_REPORT_SHA256=$reportSha256")
'''


def _safe_numerical_runner() -> str:
    return '''from __future__ import annotations
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import uuid

here = pathlib.Path(__file__).resolve()
target_flag = "--update" if "--update" in sys.argv else "--verify"
target = pathlib.Path(sys.argv[sys.argv.index(target_flag) + 1]).resolve()
report = pathlib.Path(sys.argv[sys.argv.index("--report") + 1]).resolve()
if target_flag == "--update":
    revision = sys.argv[sys.argv.index("--source-revision") + 1]
    target.write_bytes(json.dumps({"source_revision": revision, "overall_status": "PASS"}, sort_keys=True, separators=(",", ":")).encode("utf-8"))
else:
    revision = json.loads(target.read_text(encoding="utf-8"))["source_revision"]
result_sha256 = hashlib.sha256(target.read_bytes()).hexdigest()
git_path = pathlib.Path(r"C:\\Program Files\\Git\\cmd\\git.exe")
head_revision = subprocess.run(
    [str(git_path), "--no-replace-objects", "--literal-pathspecs", "-C", str(here.parents[3]), "rev-parse", "--verify", "HEAD^{commit}"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
document = {
    "ok": True,
    "result_path": str(target),
    "source_revision": revision,
    "input_sha256_before": result_sha256,
    "input_sha256_after": result_sha256,
    "input_unchanged": True,
    "transaction_receipt_id": uuid.uuid4().hex,
    "published_result_sha256": result_sha256,
    "semantic_payload_digest": "3" * 64,
    "manifest_path_count": 1,
    "check_count": 1,
    "protocol_profile": "gauge-vfe-rg-production-v1",
    "head_revision": head_revision,
    "python_executable": sys.executable,
    "python_executable_sha256": hashlib.sha256(pathlib.Path(sys.executable).read_bytes()).hexdigest(),
    "git_executable": str(git_path),
    "git_executable_sha256": hashlib.sha256(
        git_path.read_bytes()
    ).hexdigest(),
    "issues": [],
}
report_bytes = json.dumps(document, sort_keys=True, separators=(",", ":")).encode("utf-8")
report.write_bytes(report_bytes)
pathlib.Path(str(report) + ".trace").write_text("SAFE_NUMERICAL", encoding="utf-8")
sys.stdout.buffer.write(report_bytes + b"\\n")
'''


def bootstrap_fixture(tmp_path: Path) -> dict[str, Path | str]:
    """Create one committed source tree plus fake TeX tools and fresh targets."""

    repo = tmp_path / "repo"
    source = repo / "manuscripts" / "gauge_vfe_rg"
    verification = source / "verification"
    tools = tmp_path / "fake-tex-tools"
    verification.mkdir(parents=True)
    tools.mkdir()
    build_script = source / "build.ps1"
    run_checks = verification / "run_checks.py"
    build_script.write_text(_safe_build_driver(), encoding="utf-8", newline="\n")
    run_checks.write_text(_safe_numerical_runner(), encoding="utf-8", newline="\n")
    verification_result = verification / "current-results.json"
    verification_result.write_text(
        json.dumps({"overall_status": "PASS", "source_revision": "fixture"}, sort_keys=True),
        encoding="utf-8",
    )
    (source / "main.tex").write_text("\\documentclass{article}\n", encoding="utf-8")
    (source.parent / "references.bib").write_text("@misc{x,title={X}}\n", encoding="utf-8")
    pdflatex = tools / "pdflatex.cmd"
    bibtex = tools / "bibtex.cmd"
    plainnat = tools / "plainnat.bst"
    pdflatex.write_text("@echo off\r\nexit /b 0\r\n", encoding="ascii")
    bibtex.write_text("@echo off\r\nexit /b 0\r\n", encoding="ascii")
    plainnat.write_text("ENTRY{}{}{}\n", encoding="ascii")
    git(repo, "init")
    revision = commit(repo, "bootstrap fixture")
    return {
        "repo": repo,
        "source": source,
        "build_script": build_script,
        "run_checks": run_checks,
        "revision": revision,
        "pdflatex": pdflatex,
        "bibtex": bibtex,
        "plainnat": plainnat,
        "build": tmp_path / "build-output",
        "audit": tmp_path / "build-audit.json",
        "verification_result": verification_result,
        "verification_report": tmp_path / "verification-report.json",
        "receipt": tmp_path / "bootstrap-receipt.json",
        "trace": tmp_path / "verification-report.json.trace",
        "spoof": tmp_path / "path-spoof",
    }


def authenticated_outer_environment(
    fixture: dict[str, Path | str],
    spoof: Path,
) -> dict[str, str]:
    """Return the exact closed environment authenticated by the bootstrap body."""

    return {
        "SystemRoot": r"C:\WINDOWS",
        "WINDIR": r"C:\WINDOWS",
        "SystemDrive": "C:",
        "COMSPEC": r"C:\WINDOWS\System32\cmd.exe",
        "PATHEXT": ".COM;.EXE;.BAT;.CMD;.CPL",
        "PATH": f"{spoof};C:\\WINDOWS\\System32;C:\\WINDOWS",
        "TEMP": str(Path(fixture["repo"]).parent),
        "TMP": str(Path(fixture["repo"]).parent),
        "PSModulePath": (
            r"C:\Program Files\WindowsPowerShell\Modules;"
            r"C:\WINDOWS\System32\WindowsPowerShell\v1.0\Modules"
        ),
    }


def invoke_bootstrap(
    fixture: dict[str, Path | str],
    mode: str,
    *,
    source_revision: str | None = None,
    unused_build_fields_empty: bool = False,
    environment_overrides: dict[str, str | None] | None = None,
    extra_argv: tuple[str, ...] = (),
) -> subprocess.CompletedProcess[str]:
    """Invoke the exact tracked reference as external ``-Command`` literal test input."""

    literal_bytes = TRANSPORT_PATH.read_bytes()
    literal_bytes.decode("ascii")
    spoof = Path(fixture["spoof"])
    spoof.mkdir(exist_ok=True)
    (spoof / "git.cmd").write_text("@echo off\r\nexit /b 93\r\n", encoding="ascii")
    (spoof / "powershell.exe").write_text("spoof", encoding="ascii")
    environment = authenticated_outer_environment(fixture, spoof)
    if unused_build_fields_empty:
        output_directory = audit_path = ""
        pdflatex = bibtex = plainnat = ""
    else:
        output_directory = str(fixture["build"])
        audit_path = str(fixture["audit"])
        pdflatex = str(fixture["pdflatex"])
        bibtex = str(fixture["bibtex"])
        plainnat = str(fixture["plainnat"])
    environment.update(
        {
            "GAUGE_VFE_BOOTSTRAP_MODE": mode,
            "GAUGE_VFE_BOOTSTRAP_REPOSITORY_ROOT": str(fixture["repo"]),
            "GAUGE_VFE_BOOTSTRAP_SOURCE_REVISION": source_revision
            or str(fixture["revision"]),
            "GAUGE_VFE_BOOTSTRAP_RECEIPT_PATH": str(fixture["receipt"]),
            "GAUGE_VFE_BOOTSTRAP_SOURCE_DIRECTORY": str(fixture["source"]),
            "GAUGE_VFE_BOOTSTRAP_OUTPUT_DIRECTORY": output_directory,
            "GAUGE_VFE_BOOTSTRAP_AUDIT_PATH": audit_path,
            "GAUGE_VFE_BOOTSTRAP_VERIFICATION_RESULT": str(
                fixture["verification_result"]
            ),
            "GAUGE_VFE_BOOTSTRAP_VERIFICATION_REPORT": str(
                fixture["verification_report"]
            ),
            "GAUGE_VFE_BOOTSTRAP_PDFLATEX_PATH": pdflatex,
            "GAUGE_VFE_BOOTSTRAP_BIBTEX_PATH": bibtex,
            "GAUGE_VFE_BOOTSTRAP_BIBTEX_STYLE_PATH": plainnat,
            "GAUGE_VFE_BOOTSTRAP_TRANSPORT_SHA256": hashlib.sha256(
                literal_bytes
            ).hexdigest(),
            "GAUGE_VFE_BOOTSTRAP_TRANSPORT_BYTE_COUNT": str(len(literal_bytes)),
        }
    )
    for name, value in (environment_overrides or {}).items():
        if value is None:
            environment.pop(name, None)
        else:
            environment[name] = value
    completed = subprocess.run(
        [
            str(POWERSHELL),
            "-NoProfile",
            "-NonInteractive",
            *extra_argv,
            "-Command",
            "-",
        ],
        cwd=fixture["repo"],
        env=environment,
        input=literal_bytes,
        capture_output=True,
        check=False,
    )
    return subprocess.CompletedProcess(
        completed.args,
        completed.returncode,
        completed.stdout.decode("utf-8", errors="strict"),
        completed.stderr.decode("utf-8", errors="strict"),
    )


def receipt_digest(completed: subprocess.CompletedProcess[str]) -> str:
    """Extract the receipt digest emitted over the bootstrap process channel."""

    prefix = "BOOTSTRAP_RECEIPT_SHA256="
    values = [line[len(prefix) :] for line in completed.stdout.splitlines() if line.startswith(prefix)]
    assert len(values) == 1, completed.stdout + completed.stderr
    assert len(values[0]) == 64 and values[0] == values[0].lower()
    return values[0]


def receipt_expectations(
    fixture: dict[str, Path | str],
    mode: str,
) -> dict[str, object]:
    """Return the independent prelaunch values required by receipt validation."""

    is_build = mode == "Build"
    return {
        "expected_transport_sha256": hashlib.sha256(TRANSPORT_PATH.read_bytes()).hexdigest(),
        "expected_transport_byte_count": len(TRANSPORT_PATH.read_bytes()),
        "expected_mode": mode,
        "expected_repository_root": Path(fixture["repo"]).resolve(),
        "expected_source_revision": str(fixture["revision"]),
        "expected_receipt_path": Path(fixture["receipt"]).resolve(),
        "expected_source_directory": Path(fixture["source"]).resolve(),
        "expected_output_directory": Path(fixture["build"]).resolve() if is_build else "",
        "expected_audit_path": Path(fixture["audit"]).resolve() if is_build else "",
        "expected_verification_result": Path(fixture["verification_result"]).resolve(),
        "expected_verification_report": Path(fixture["verification_report"]).resolve(),
        "expected_pdflatex_path": Path(fixture["pdflatex"]).resolve() if is_build else "",
        "expected_bibtex_path": Path(fixture["bibtex"]).resolve() if is_build else "",
        "expected_bibtex_style_path": Path(fixture["plainnat"]).resolve() if is_build else "",
    }


def test_authenticated_outer_environment_factory_supplies_exact_launch_values(
    tmp_path: Path,
) -> None:
    """Catch incomplete launch values even when PowerShell repairs them at startup."""

    fixture = bootstrap_fixture(tmp_path)
    spoof = Path(fixture["spoof"])
    factory = globals().get("authenticated_outer_environment")
    assert callable(factory), "bootstrap tests need one shared authenticated environment factory"
    environment = factory(fixture, spoof)
    assert environment == {
        "SystemRoot": r"C:\WINDOWS",
        "WINDIR": r"C:\WINDOWS",
        "SystemDrive": "C:",
        "COMSPEC": r"C:\WINDOWS\System32\cmd.exe",
        "PATHEXT": ".COM;.EXE;.BAT;.CMD;.CPL",
        "PATH": f"{spoof};C:\\WINDOWS\\System32;C:\\WINDOWS",
        "TEMP": str(Path(fixture["repo"]).parent),
        "TMP": str(Path(fixture["repo"]).parent),
        "PSModulePath": (
            r"C:\Program Files\WindowsPowerShell\Modules;"
            r"C:\WINDOWS\System32\WindowsPowerShell\v1.0\Modules"
        ),
    }


def test_reference_is_non_executable_exact_literal_with_all_public_modes() -> None:
    assert REFERENCE_PATH.is_file(), "missing auditable bootstrap literal reference"
    assert TRANSPORT_PATH.is_file(), "missing exact one-line bootstrap transport"
    assert REFERENCE_PATH.name.endswith(".ps1.txt")
    body_bytes = REFERENCE_PATH.read_bytes()
    body = body_bytes.decode("ascii")
    transport_bytes = TRANSPORT_PATH.read_bytes()
    transport = transport_bytes.decode("ascii")
    assert transport_bytes.count(b"\n") == 1 and transport_bytes.endswith(b"\n")
    assert b"\r" not in transport_bytes
    assert transport.startswith(
        "& ([ScriptBlock]::Create([Text.Encoding]::ASCII.GetString("
    )
    encoded_candidates = re.findall(
        r"FromBase64String\('([A-Za-z0-9+/=]+)'\)",
        transport,
    )
    assert len(encoded_candidates) == 1
    assert base64.b64decode(encoded_candidates[0], validate=True) == body_bytes
    assert body.startswith("[CmdletBinding()]\nparam(")
    assert body.rstrip().endswith("}")
    assert "Build" in body
    assert "NumericalUpdate" in body
    assert "NumericalVerify" in body
    assert str(POWERSHELL) in body
    assert str(TRUSTED_GIT) in body
    assert str(TRUSTED_PYTHON) in body
    assert "Invoke-Expression" not in body
    assert "Get-Command" not in body
    assert "NormalizeCrLf" not in body
    assert "crlf_to_lf" not in body
    assert re.search(r"(?m)^\s*HOME\s*=", body) is None


def test_direct_command_line_transport_is_mechanically_impossible() -> None:
    """The approved stdin transport is required, not a convenience."""

    literal = TRANSPORT_PATH.read_text(encoding="ascii")
    argv = [
        str(POWERSHELL),
        "-NoProfile",
        "-NonInteractive",
        "-Command",
        literal,
    ]
    assert len(subprocess.list2cmdline(argv)) > 32_767
    with pytest.raises(OSError, match=r"(206|too long)"):
        subprocess.run(argv, text=True, capture_output=True, check=False)


def test_subprocess_feeder_preserves_raw_stdin_bytes_at_child_boundary() -> None:
    """Binary ``input=`` must not perform Python text-mode LF-to-CRLF rewriting."""

    payload = TRANSPORT_PATH.read_bytes() + b"\x00\n\r\nRAW-END"
    capture = (
        "$stream=[Console]::OpenStandardInput();"
        "$memory=New-Object IO.MemoryStream;"
        "$stream.CopyTo($memory);"
        "$bytes=$memory.ToArray();"
        "$sha=[Security.Cryptography.SHA256]::Create();"
        "try{$hash=([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-','').ToLowerInvariant()}"
        "finally{$sha.Dispose();$memory.Dispose()};"
        "[Console]::Out.WriteLine(\"$($bytes.Length):$hash\")"
    )
    completed = subprocess.run(
        [str(POWERSHELL), "-NoProfile", "-NonInteractive", "-Command", capture],
        input=payload,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr.decode("utf-8", errors="replace")
    assert completed.stdout.decode("ascii").strip() == (
        f"{len(payload)}:{hashlib.sha256(payload).hexdigest()}"
    )


def test_inner_build_driver_uses_only_explicit_bootstrap_identity_inputs() -> None:
    """The in-memory child must not infer its source identity from host globals."""

    body = BUILD_SCRIPT_PATH.read_text(encoding="utf-8")
    for name in (
        "RepositoryRoot",
        "SourceDirectory",
        "RepositoryBuildScript",
        "ExecutedBuildScript",
        "BootstrapAttestationPath",
        "OutputDirectory",
        "AuditPath",
        "SourceRevision",
        "VerificationResult",
        "VerificationReport",
        "PdflatexPath",
        "BibtexPath",
        "BibtexStylePath",
    ):
        assert re.search(
            rf"\[Parameter\(Mandatory = \$true\)\]\s*\[string\]\${name}\b",
            body,
        ), f"missing mandatory explicit inner-build input {name}"
    assert "$PSScriptRoot" not in body
    assert len(re.findall(r"\$PSCommandPath\b", body)) == 1
    assert re.search(
        r"if\s*\(\$PSCommandPath\)\s*\{\s*throw\s+'Authenticated in-memory child unexpectedly has PSCommandPath\.'",
        body,
    )
    assert "Resolve-Executable -Value $PdflatexPath" not in body
    assert "Resolve-Executable -Value $BibtexPath" not in body


def test_build_mode_materializes_exact_s_blob_and_separates_source_from_execution(
    tmp_path: Path,
) -> None:
    fixture = bootstrap_fixture(tmp_path)
    Path(fixture["build_script"]).write_text(
        f"Set-Content -LiteralPath '{fixture['trace']}' -Value ATTACKER_CHECKOUT\n",
        encoding="utf-8",
    )
    completed = invoke_bootstrap(fixture, "Build")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert Path(fixture["receipt"]).is_file(), completed.stdout + completed.stderr
    assert Path(fixture["trace"]).read_text(encoding="utf-8-sig") == "SAFE_BUILD"
    receipt = json.loads(Path(fixture["receipt"]).read_text(encoding="utf-8-sig"))
    assert receipt["accepted"] is True
    assert receipt["mode"] == "Build"
    assert receipt["approved_transport_sha256"] == hashlib.sha256(
        TRANSPORT_PATH.read_bytes()
    ).hexdigest()
    assert receipt["approved_transport_byte_count"] == len(TRANSPORT_PATH.read_bytes())
    assert receipt["repository_source"]["path"] == str(Path(fixture["build_script"]).resolve())
    assert receipt["executed_source"]["path"] != receipt["repository_source"]["path"]
    assert receipt["executed_source"]["git_blob_oid"] == receipt["repository_source"]["git_blob_oid"]
    assert receipt["executed_source"]["byte_count"] == receipt["repository_source"]["git_blob_byte_count"]
    result_identity = receipt["outputs"]["verification_result"]
    report_identity = receipt["outputs"]["verification_report"]
    audit_identity = receipt["outputs"]["audit_path"]
    report = json.loads(Path(fixture["verification_report"]).read_bytes())
    assert result_identity["sha256"] == report["published_result_sha256"]
    assert report_identity["sha256"] == hashlib.sha256(
        Path(fixture["verification_report"]).read_bytes()
    ).hexdigest()
    assert audit_identity["sha256"] == hashlib.sha256(
        Path(fixture["audit"]).read_bytes()
    ).hexdigest()
    assert receipt["outputs"]["transaction_receipt_id"] == report["transaction_receipt_id"]
    assert receipt["fresh_targets"]["audit_path"]["initial_state"] == "absent"
    assert receipt["fresh_targets"]["verification_report"]["initial_state"] == "absent"
    assert receipt["fresh_targets"]["output_directory"]["initial_state"] == "absent"
    assert Path(receipt["temporary_directory"]).is_absolute()
    assert not Path(receipt["temporary_directory"]).exists()
    assert receipt["cleanup"]["completed"] is True
    assert hashlib.sha256(Path(fixture["receipt"]).read_bytes()).hexdigest() == receipt_digest(completed)


def test_build_rejects_forged_bootstrap_attested_executed_context(tmp_path: Path) -> None:
    fixture = bootstrap_fixture(tmp_path)
    build_script = Path(fixture["build_script"])
    source = build_script.read_text(encoding="utf-8")
    exact = """executed_build_script = [ordered]@{
        path = [System.IO.Path]::GetFullPath($ExecutedBuildScript)
        sha256 = [string]$attestation.source_sha256
        byte_count = [int64]$attestation.source_blob_byte_count
    }"""
    forged = exact.replace(
        "sha256 = [string]$attestation.source_sha256",
        "sha256 = ('0' * 64)",
    )
    assert exact in source
    build_script.write_text(source.replace(exact, forged), encoding="utf-8", newline="\n")
    fixture["revision"] = commit(Path(fixture["repo"]), "forged executed-context witness")
    completed = invoke_bootstrap(fixture, "Build")
    assert completed.returncode != 0
    assert (
        "Typed build report does not bind repository source, executed materialization, "
        "and bootstrap attestation identities."
    ) in (completed.stdout + completed.stderr)
    receipt = json.loads(Path(fixture["receipt"]).read_bytes())
    assert receipt["accepted"] is False


def test_numerical_mode_locks_same_repository_path_and_rejects_tampered_checkout(
    tmp_path: Path,
) -> None:
    fixture = bootstrap_fixture(tmp_path)
    Path(fixture["run_checks"]).write_text(
        "raise SystemExit('ATTACKER_NUMERICAL_EXECUTED')\n",
        encoding="utf-8",
    )
    completed = invoke_bootstrap(
        fixture,
        "NumericalUpdate",
        unused_build_fields_empty=True,
    )
    assert completed.returncode != 0
    assert "not bound to source revision" in (completed.stdout + completed.stderr).lower()
    assert not Path(fixture["trace"]).exists()
    receipt = json.loads(Path(fixture["receipt"]).read_text(encoding="utf-8-sig"))
    assert receipt["accepted"] is False
    assert receipt["cleanup"]["completed"] is True
    assert not Path(receipt["temporary_directory"]).exists()


def test_numerical_mode_rejects_crlf_worktree_bytes_independent_of_git_normalization(
    tmp_path: Path,
) -> None:
    fixture = bootstrap_fixture(tmp_path)
    runner = Path(fixture["run_checks"])
    source_bytes = runner.read_bytes()
    assert b"\n" in source_bytes and b"\r" not in source_bytes
    runner.write_bytes(source_bytes.replace(b"\n", b"\r\n"))
    completed = invoke_bootstrap(
        fixture,
        "NumericalUpdate",
        unused_build_fields_empty=True,
    )
    assert completed.returncode != 0
    diagnostics = (completed.stdout + completed.stderr).lower()
    assert "raw bytes" in diagnostics and "not bound to source revision" in diagnostics
    assert not Path(fixture["trace"]).exists()


def test_numerical_update_uses_fixed_isolated_python_and_emits_accepted_receipt(
    tmp_path: Path,
) -> None:
    fixture = bootstrap_fixture(tmp_path)
    completed = invoke_bootstrap(
        fixture,
        "NumericalUpdate",
        unused_build_fields_empty=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert Path(fixture["trace"]).read_text(encoding="utf-8") == "SAFE_NUMERICAL"
    receipt = json.loads(Path(fixture["receipt"]).read_text(encoding="utf-8-sig"))
    assert receipt["accepted"] is True
    assert receipt["mode"] == "NumericalUpdate"
    assert receipt["repository_source"]["path"] == receipt["executed_source"]["path"]
    assert receipt["child"]["argv"][:3] == [str(TRUSTED_PYTHON), "-I", "-S"]
    assert receipt["m1"]["completed"] is True
    assert base64.b64decode(receipt["child"]["stdout_base64"], validate=True) == (
        Path(fixture["verification_report"]).read_bytes() + b"\n"
    )
    assert hashlib.sha256(Path(fixture["receipt"]).read_bytes()).hexdigest() == receipt_digest(completed)


@pytest.mark.parametrize("mode", ("Build", "NumericalUpdate", "NumericalVerify"))
def test_public_mode_receipts_reach_success_and_validate_end_to_end(
    tmp_path: Path,
    mode: str,
) -> None:
    """Every public mode must cross preflight and produce an independently accepted receipt."""

    fixture = bootstrap_fixture(tmp_path)
    if mode == "NumericalVerify":
        Path(fixture["verification_result"]).write_text(
            json.dumps(
                {
                    "overall_status": "PASS",
                    "source_revision": str(fixture["revision"]),
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
            encoding="utf-8",
            newline="\n",
        )
        commit(Path(fixture["repo"]), "bind verify witness to authenticated source revision")
    completed = invoke_bootstrap(
        fixture,
        mode,
        unused_build_fields_empty=mode != "Build",
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    receipt_path = Path(fixture["receipt"])
    document = json.loads(receipt_path.read_bytes())
    assert document["accepted"] is True
    assert document["mode"] == mode
    assert document["error"] is None
    assert document["m1"]["completed"] is True
    assert document["cleanup"]["completed"] is True

    module = audit_module(f"bootstrap_receipt_positive_{mode.lower()}")
    assert module.validate_bootstrap_receipt(
        receipt_path,
        receipt_digest(completed),
        **receipt_expectations(fixture, mode),
    )["accepted"] is True

    if mode == "NumericalUpdate":
        assert "--source-revision" in document["child"]["argv"]
    elif mode == "NumericalVerify":
        assert document["child"]["argv"] == [
            str(TRUSTED_PYTHON),
            "-I",
            "-S",
            str(Path(fixture["run_checks"]).resolve()),
            "--verify",
            str(Path(fixture["verification_result"]).resolve()),
            "--report",
            str(Path(fixture["verification_report"]).resolve()),
        ]
        assert "--source-revision" not in document["child"]["argv"]


def test_numerical_verify_receipt_validator_rejects_exact_argv_tampering(
    tmp_path: Path,
) -> None:
    """A fresh digest must not legitimize altered NumericalVerify child arguments."""

    fixture = bootstrap_fixture(tmp_path)
    Path(fixture["verification_result"]).write_text(
        json.dumps(
            {
                "overall_status": "PASS",
                "source_revision": str(fixture["revision"]),
            },
            sort_keys=True,
            separators=(",", ":"),
        ),
        encoding="utf-8",
        newline="\n",
    )
    commit(Path(fixture["repo"]), "bind tamper witness to authenticated source revision")
    completed = invoke_bootstrap(
        fixture,
        "NumericalVerify",
        unused_build_fields_empty=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    receipt_path = Path(fixture["receipt"])
    original = receipt_path.read_bytes()

    module = audit_module("bootstrap_receipt_verify_argv_tamper")
    assert module.validate_bootstrap_receipt(
        receipt_path,
        receipt_digest(completed),
        **receipt_expectations(fixture, "NumericalVerify"),
    )["accepted"] is True

    for mutation in ("add_source_revision", "switch_mode", "drop_report"):
        document = json.loads(original)
        argv = document["child"]["argv"]
        if mutation == "add_source_revision":
            report_index = argv.index("--report")
            argv[report_index:report_index] = [
                "--source-revision",
                str(fixture["revision"]),
            ]
        elif mutation == "switch_mode":
            argv[argv.index("--verify")] = "--update"
        else:
            report_index = argv.index("--report")
            del argv[report_index : report_index + 2]
        mutated = json.dumps(document, separators=(",", ":")).encode("utf-8")
        receipt_path.write_bytes(mutated)
        with pytest.raises(ValueError, match="argv|invocation"):
            module.validate_bootstrap_receipt(
                receipt_path,
                hashlib.sha256(mutated).hexdigest(),
                **receipt_expectations(fixture, "NumericalVerify"),
            )


@pytest.mark.parametrize("target", ["audit", "verification_report", "build"])
def test_build_preflight_rejects_stale_or_nonempty_targets(
    tmp_path: Path,
    target: str,
) -> None:
    fixture = bootstrap_fixture(tmp_path)
    path = Path(fixture[target])
    if target == "build":
        path.mkdir()
        (path / "stale.txt").write_text("stale", encoding="utf-8")
    else:
        path.write_text("stale", encoding="utf-8")
    completed = invoke_bootstrap(fixture, "Build")
    assert completed.returncode != 0
    assert not Path(fixture["trace"]).exists()
    diagnostics = (completed.stdout + completed.stderr).lower()
    assert "fresh" in diagnostics or "empty" in diagnostics


def test_bootstrap_rejects_missing_unexpected_environment_and_extra_outer_switch(
    tmp_path: Path,
) -> None:
    missing = bootstrap_fixture(tmp_path / "missing")
    missing_completed = invoke_bootstrap(
        missing,
        "Build",
        environment_overrides={"PATH": None},
    )
    assert missing_completed.returncode != 0
    assert "missing required bootstrap environment" in (
        missing_completed.stdout + missing_completed.stderr
    ).lower()

    unexpected = bootstrap_fixture(tmp_path / "unexpected")
    unexpected_completed = invoke_bootstrap(
        unexpected,
        "Build",
        environment_overrides={"gauge_vfe_bootstrap_attacker": "1"},
    )
    assert unexpected_completed.returncode != 0
    assert "unexpected outer bootstrap" in (
        unexpected_completed.stdout + unexpected_completed.stderr
    ).lower()

    extra = bootstrap_fixture(tmp_path / "extra")
    extra_completed = invoke_bootstrap(extra, "Build", extra_argv=("-NoLogo",))
    assert extra_completed.returncode != 0
    assert "outer bootstrap argv" in (extra_completed.stdout + extra_completed.stderr).lower()


def test_outer_temp_reparse_is_rejected_before_child_launch(tmp_path: Path) -> None:
    fixture = bootstrap_fixture(tmp_path)
    target = tmp_path / "temp-target"
    junction = tmp_path / "temp-junction"
    target.mkdir()
    created = subprocess.run(
        [
            str(POWERSHELL),
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            f"New-Item -ItemType Junction -Path '{junction}' -Target '{target}' | Out-Null",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert created.returncode == 0, created.stderr
    completed = invoke_bootstrap(
        fixture,
        "Build",
        environment_overrides={"TEMP": str(junction), "TMP": str(junction)},
    )
    assert completed.returncode != 0
    assert "reparse-mediated" in (completed.stdout + completed.stderr).lower()
    assert not Path(fixture["trace"]).exists()


def test_build_output_directory_must_be_disjoint_from_evidence_targets(tmp_path: Path) -> None:
    fixture = bootstrap_fixture(tmp_path)
    Path(fixture["build"]).mkdir()
    fixture["audit"] = Path(fixture["build"]) / "nested-audit.json"
    completed = invoke_bootstrap(fixture, "Build")
    assert completed.returncode != 0
    assert "disjoint" in (completed.stdout + completed.stderr).lower()
    assert not Path(fixture["trace"]).exists()


@pytest.mark.parametrize("kind", ["relative", "missing"])
def test_build_rejects_nonabsolute_or_missing_explicit_tex_tool(
    tmp_path: Path,
    kind: str,
) -> None:
    fixture = bootstrap_fixture(tmp_path)
    fixture["pdflatex"] = "pdflatex.cmd" if kind == "relative" else tmp_path / "missing-pdflatex.exe"
    completed = invoke_bootstrap(fixture, "Build")
    assert completed.returncode != 0
    diagnostics = (completed.stdout + completed.stderr).lower()
    expected = "explicit absolute path" if kind == "relative" else "missing path component"
    assert expected in diagnostics, diagnostics


def test_build_child_report_substitution_after_handoff_is_rejected(tmp_path: Path) -> None:
    fixture = bootstrap_fixture(tmp_path)
    source = _safe_build_driver().replace(
        '[Console]::Out.WriteLine("BUILD_VERIFICATION_REPORT_SHA256=$reportSha256")',
        '[Console]::Out.WriteLine("BUILD_VERIFICATION_REPORT_SHA256=$reportSha256")\n'
        "$substitute = Get-Content -LiteralPath $VerificationReport -Raw | ConvertFrom-Json\n"
        "$substitute.semantic_payload_digest = ('4' * 64)\n"
        "[System.IO.File]::WriteAllText($VerificationReport, ($substitute | ConvertTo-Json -Compress -Depth 8), $utf8)",
    )
    Path(fixture["build_script"]).write_text(source, encoding="utf-8", newline="\n")
    fixture["revision"] = commit(Path(fixture["repo"]), "report substitution witness")
    completed = invoke_bootstrap(fixture, "Build")
    assert completed.returncode != 0
    assert "handoff" in (completed.stdout + completed.stderr).lower()


@pytest.mark.parametrize("mutation", ["replace_main_pdf", "add_unlisted_file"])
def test_build_artifact_inventory_rejects_post_audit_output_mutation(
    tmp_path: Path,
    mutation: str,
) -> None:
    fixture = bootstrap_fixture(tmp_path)
    attack = (
        "[System.IO.File]::WriteAllText((Join-Path $OutputDirectory 'main.pdf'), 'ATTACK', $utf8)"
        if mutation == "replace_main_pdf"
        else "[System.IO.File]::WriteAllText((Join-Path $OutputDirectory 'unlisted.txt'), 'ATTACK', $utf8)"
    )
    source = _safe_build_driver().replace(
        '[Console]::Out.WriteLine("BUILD_VERIFICATION_REPORT_SHA256=$reportSha256")',
        '[Console]::Out.WriteLine("BUILD_VERIFICATION_REPORT_SHA256=$reportSha256")\n' + attack,
    )
    Path(fixture["build_script"]).write_text(source, encoding="utf-8", newline="\n")
    fixture["revision"] = commit(Path(fixture["repo"]), f"artifact mutation witness {mutation}")
    completed = invoke_bootstrap(fixture, "Build")
    assert completed.returncode != 0
    diagnostics = (completed.stdout + completed.stderr).lower()
    assert "artifact" in diagnostics or "regular-file set" in diagnostics


def test_numerical_stdout_must_equal_retained_canonical_report_bytes(tmp_path: Path) -> None:
    fixture = bootstrap_fixture(tmp_path)
    source = _safe_numerical_runner().replace(
        'sys.stdout.buffer.write(report_bytes + b"\\n")',
        'sys.stdout.buffer.write(report_bytes + b"\\nEXTRA\\n")',
    )
    Path(fixture["run_checks"]).write_text(source, encoding="utf-8", newline="\n")
    fixture["revision"] = commit(Path(fixture["repo"]), "stdout substitution witness")
    completed = invoke_bootstrap(
        fixture,
        "NumericalUpdate",
        unused_build_fields_empty=True,
    )
    assert completed.returncode != 0
    assert "canonical stdout" in (completed.stdout + completed.stderr).lower()


def test_early_build_child_failure_still_runs_m1_and_cleanup(tmp_path: Path) -> None:
    fixture = bootstrap_fixture(tmp_path)
    Path(fixture["build_script"]).write_text(
        "throw 'EARLY_CHILD_FAILURE'\n",
        encoding="utf-8",
        newline="\n",
    )
    fixture["revision"] = commit(Path(fixture["repo"]), "early child failure witness")
    completed = invoke_bootstrap(fixture, "Build")
    assert completed.returncode != 0
    receipt = json.loads(Path(fixture["receipt"]).read_bytes())
    assert receipt["accepted"] is False
    assert receipt["m1"]["completed"] is True
    assert receipt["cleanup"]["completed"] is True
    assert not Path(receipt["temporary_directory"]).exists()


def test_retained_materialization_denies_write_delete_rename_and_replace(tmp_path: Path) -> None:
    fixture = bootstrap_fixture(tmp_path)
    denial_probe = r'''
foreach ($probe in @(
    [scriptblock]{ [System.IO.File]::WriteAllText($ExecutedBuildScript, 'ATTACK') },
    [scriptblock]{ [System.IO.File]::Delete($ExecutedBuildScript) },
    [scriptblock]{ [System.IO.File]::Move($ExecutedBuildScript, "$ExecutedBuildScript.moved") },
    [scriptblock]{
        $replacement = Join-Path ([System.IO.Path]::GetDirectoryName($ExecutedBuildScript)) 'replacement.ps1'
        [System.IO.File]::WriteAllText($replacement, 'ATTACK')
        [System.IO.File]::Replace($replacement, $ExecutedBuildScript, $null)
    }
)) {
    $denied = $false
    try { & $probe }
    catch { $denied = $true }
    if (-not $denied) { throw 'RETAINED_MATERIALIZATION_MUTATION_SUCCEEDED' }
}
'''
    source = _safe_build_driver().replace(
        "if ($PSCommandPath) { throw 'Authenticated in-memory child unexpectedly has PSCommandPath.' }",
        "if ($PSCommandPath) { throw 'Authenticated in-memory child unexpectedly has PSCommandPath.' }\n"
        + denial_probe,
    )
    Path(fixture["build_script"]).write_text(source, encoding="utf-8", newline="\n")
    fixture["revision"] = commit(Path(fixture["repo"]), "retained materialization denial witness")
    completed = invoke_bootstrap(fixture, "Build")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert Path(fixture["trace"]).read_text(encoding="utf-8-sig") == "SAFE_BUILD"


def test_corrupt_git_blob_is_rejected_by_same_handle_oid_check(tmp_path: Path) -> None:
    fixture = bootstrap_fixture(tmp_path)
    object_id = git(
        Path(fixture["repo"]),
        "rev-parse",
        f"{fixture['revision']}:manuscripts/gauge_vfe_rg/build.ps1",
    )
    loose_object = Path(fixture["repo"]) / ".git" / "objects" / object_id[:2] / object_id[2:]
    assert loose_object.is_file(), "fixture blob must remain loose for corruption witness"
    loose_object.chmod(0o600)
    malicious = b"Write-Output 'wrong object bytes'\n"
    loose_object.write_bytes(zlib.compress(b"blob " + str(len(malicious)).encode() + b"\0" + malicious))
    completed = invoke_bootstrap(fixture, "Build")
    assert completed.returncode != 0
    assert "blob oid" in (completed.stdout + completed.stderr).lower()
    assert not Path(fixture["trace"]).exists()


def test_receipt_tamper_fails_digest_bound_validator(tmp_path: Path) -> None:
    fixture = bootstrap_fixture(tmp_path)
    completed = invoke_bootstrap(fixture, "Build")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    digest = receipt_digest(completed)
    module = audit_module("bootstrap_receipt_audit")
    validator = getattr(module, "validate_bootstrap_receipt", None)
    assert callable(validator), "build auditor must expose the digest-bound receipt validator"
    assert validator(
        Path(fixture["receipt"]),
        digest,
        **receipt_expectations(fixture, "Build"),
    )["accepted"] is True
    document = json.loads(Path(fixture["receipt"]).read_text(encoding="utf-8-sig"))
    document["accepted"] = False
    Path(fixture["receipt"]).write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(ValueError, match="digest"):
        validator(
            Path(fixture["receipt"]),
            digest,
            **receipt_expectations(fixture, "Build"),
        )


def test_receipt_validator_rejects_valid_receipt_digest_with_wrong_asserted_transport(
    tmp_path: Path,
) -> None:
    fixture = bootstrap_fixture(tmp_path)
    completed = invoke_bootstrap(fixture, "Build")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    module = audit_module("bootstrap_receipt_transport_audit")
    validator = module.validate_bootstrap_receipt
    document = json.loads(Path(fixture["receipt"]).read_bytes())
    document["approved_transport_sha256"] = "0" * 64
    mutated_bytes = json.dumps(document, separators=(",", ":")).encode("utf-8")
    Path(fixture["receipt"]).write_bytes(mutated_bytes)
    mutated_digest = hashlib.sha256(mutated_bytes).hexdigest()
    with pytest.raises(ValueError, match="transport"):
        validator(
            Path(fixture["receipt"]),
            mutated_digest,
            **receipt_expectations(fixture, "Build"),
        )


@pytest.mark.parametrize(
    ("field", "replacement", "diagnostic"),
    (
        ("expected_source_revision", "0" * 40, "source revision"),
        ("expected_mode", "NumericalVerify", "mode"),
        ("expected_verification_report", "independent-other-report.json", "report path"),
    ),
)
def test_receipt_validator_rejects_independent_launch_value_mismatch(
    tmp_path: Path,
    field: str,
    replacement: str,
    diagnostic: str,
) -> None:
    fixture = bootstrap_fixture(tmp_path)
    completed = invoke_bootstrap(fixture, "Build")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    module = audit_module("bootstrap_receipt_launch_audit")
    expectations = receipt_expectations(fixture, "Build")
    if field == "expected_verification_report":
        expectations[field] = tmp_path / replacement
    elif field == "expected_mode":
        expectations[field] = replacement
        for build_only in (
            "expected_output_directory",
            "expected_audit_path",
            "expected_pdflatex_path",
            "expected_bibtex_path",
            "expected_bibtex_style_path",
        ):
            expectations[build_only] = ""
    else:
        expectations[field] = replacement
    with pytest.raises(ValueError, match=diagnostic):
        module.validate_bootstrap_receipt(
            Path(fixture["receipt"]),
            receipt_digest(completed),
            **expectations,
        )


@pytest.mark.parametrize("stale_head", (False, True))
def test_receipt_validator_binds_current_descendant_head(
    tmp_path: Path,
    stale_head: bool,
) -> None:
    fixture = bootstrap_fixture(tmp_path)
    repo = Path(fixture["repo"])
    if stale_head:
        build_script = Path(fixture["build_script"])
        source = build_script.read_text(encoding="utf-8")
        source = source.replace("head_revision = $headRevision", "head_revision = $SourceRevision")
        build_script.write_text(source, encoding="utf-8", newline="\n")
        fixture["revision"] = commit(repo, "stale report-head witness source")
    source_revision = str(fixture["revision"])
    (repo / "evidence-only-descendant.txt").write_text("E\n", encoding="utf-8", newline="\n")
    evidence_revision = commit(repo, "evidence-only descendant")
    assert evidence_revision != source_revision

    completed = invoke_bootstrap(fixture, "Build")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    module = audit_module("bootstrap_receipt_head_audit")
    invocation = lambda: module.validate_bootstrap_receipt(
        Path(fixture["receipt"]),
        receipt_digest(completed),
        **receipt_expectations(fixture, "Build"),
    )
    if stale_head:
        with pytest.raises(ValueError, match="head|outputs"):
            invocation()
    else:
        assert invocation()["accepted"] is True


def test_build_audit_atomic_publisher_returns_exact_canonical_bytes(tmp_path: Path) -> None:
    module = audit_module("bootstrap_audit_publisher")
    target = tmp_path / "audit.json"
    value = {"z": 1, "ok": False, "errors": []}
    stdout = io.BytesIO()
    digest = module._publish_new_json_with_digest(target, value, stdout)
    published = target.read_bytes()
    assert published == b'{"errors":[],"ok":false,"z":1}'
    assert digest == hashlib.sha256(published).hexdigest()
    assert stdout.getvalue() == f"BUILD_AUDIT_SHA256={digest}\n".encode("ascii")
    rejected_stdout = io.BytesIO()
    with pytest.raises(FileExistsError):
        module._publish_new_json_with_digest(target, value, rejected_stdout)
    assert target.read_bytes() == published
    assert rejected_stdout.getvalue() == b""


def test_bootstrap_audit_loader_releases_authenticated_finder_before_the_next_test() -> None:
    """A bootstrap unit test must not block another verifier's fixed-site imports."""

    spec = importlib.util.find_spec("scipy")
    assert spec is not None
    assert isinstance(spec.origin, str)
    assert Path(spec.origin).resolve().is_relative_to(TRUSTED_PYPDF_SITE.resolve())
