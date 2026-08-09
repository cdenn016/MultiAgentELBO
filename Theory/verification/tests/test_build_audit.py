"""Real-artifact RED contract for machine-readable TeX build auditing."""

from __future__ import annotations

import atexit
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest


AUDIT_PATH = Path(__file__).resolve().parents[1] / "build_audit.py"
BUILD_SCRIPT_PATH = Path(__file__).resolve().parents[2] / "build.ps1"
PRODUCTION_PROFILE = "gauge-vfe-rg-production-v1"
TRUSTED_PYTHON = Path(r"C:\Python314\python.exe")
TRUSTED_GIT = Path(r"C:\Program Files\Git\cmd\git.exe")
WINDOWS_DIRECTORY = Path(r"C:\WINDOWS")
WINDOWS_SYSTEM_DIRECTORY = WINDOWS_DIRECTORY / "System32"
TRUSTED_PYPDF_SITE = Path(
    r"C:\Users\chris and christine\AppData\Roaming\Python\Python314\site-packages"
)
TRUSTED_PYPDF_ROOT = TRUSTED_PYPDF_SITE / "pypdf"
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


@contextmanager
def held_windows_read_locks(paths: tuple[Path, ...]):
    """Hold read-only, share-read handles that deny writes and deletion."""

    import ctypes
    from ctypes import wintypes

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    create_file = kernel32.CreateFileW
    create_file.argtypes = (
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    )
    create_file.restype = wintypes.HANDLE
    close_handle = kernel32.CloseHandle
    close_handle.argtypes = (wintypes.HANDLE,)
    close_handle.restype = wintypes.BOOL
    invalid_handle = ctypes.c_void_p(-1).value
    handles: list[int] = []
    try:
        for path in paths:
            handle = create_file(
                str(path.resolve()),
                0x80000000,  # GENERIC_READ
                0x00000001,  # FILE_SHARE_READ
                None,
                3,  # OPEN_EXISTING
                0x00000080,  # FILE_ATTRIBUTE_NORMAL
                None,
            )
            if handle == invalid_handle:
                raise OSError(ctypes.get_last_error(), f"CreateFileW failed for {path}")
            handles.append(handle)
        yield kernel32, tuple(handles)
    finally:
        for handle in reversed(handles):
            close_handle(handle)
KPATHSEA_HELP_FORMATS_SAMPLE = """
[variables: GFFONTS GLYPHFONTS TEXFONTS]
[variables: PKFONTS TEXPKS GLYPHFONTS TEXFONTS]
[variables: TFMFONTS TEXFONTS]
[variables: AFMFONTS TEXFONTS]
[variables: MFBASES TEXMFINI]
[variables: BIBINPUTS TEXBIB]
[variables: BSTINPUTS]
[variables: TEXMFCNF]
[variables: TEXMFDBS]
[variables: TEXFORMATS TEXMFINI]
[variables: TEXFONTMAPS TEXFONTS]
[variables: MPMEMS TEXMFINI]
[variables: MFINPUTS]
[variables: MFPOOL TEXMFINI]
[variables: MFTINPUTS]
[variables: MPINPUTS]
[variables: MPPOOL TEXMFINI]
[variables: MPSUPPORT]
[variables: OCPINPUTS]
[variables: OFMFONTS TEXFONTS]
[variables: OPLFONTS TEXFONTS]
[variables: OTPINPUTS]
[variables: OVFFONTS TEXFONTS]
[variables: OVPFONTS TEXFONTS]
[variables: TEXPICTS TEXINPUTS]
[variables: TEXINPUTS]
[variables: TEXDOCS]
[variables: TEXPOOL TEXMFINI]
[variables: TEXSOURCES]
[variables: TEXPSHEADERS PSHEADERS]
[variables: TRFONTS]
[variables: T1FONTS T1INPUTS TEXFONTS TEXPSHEADERS PSHEADERS]
[variables: VFFONTS TEXFONTS]
[variables: TEXCONFIG]
[variables: TEXINDEXSTYLE INDEXSTYLE]
[variables: TTFONTS TEXFONTS]
[variables: T42FONTS TEXFONTS]
[variables: WEB2C]
[variables: KPSEWHICHINPUTS]
[variables: MISCFONTS TEXFONTS]
[variables: WEBINPUTS]
[variables: CWEBINPUTS]
[variables: ENCFONTS TEXFONTS]
[variables: CMAPFONTS TEXFONTS]
[variables: SFDFONTS TEXFONTS]
[variables: OPENTYPEFONTS TEXFONTS]
[variables: PDFTEXCONFIG]
[variables: LIGFONTS TEXFONTS]
[variables: TEXMFSCRIPTS]
[variables: LUAINPUTS]
[variables: FONTFEATURES]
[variables: FONTCIDMAPS]
[variables: MLBIBINPUTS BIBINPUTS TEXBIB]
[variables: MLBSTINPUTS BSTINPUTS]
[variables: CLUAINPUTS]
[variables: RISINPUTS]
[variables: BLTXMLINPUTS]
"""

PDF_METADATA = {
    "title": "Gauge VFE RG Build Audit Fixture",
    "author": "Robert C. Dennis",
    "subject": "Lifecycle build verification",
    "keywords": "gauge, VFE, RG",
    "creator": "pytest fixture",
    "producer": "hand-built PDF fixture",
    "creation_date": "D:20260803093000-05'00'",
    "modification_date": "D:20260803093000-05'00'",
}


class MissingAudit:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, **_kwargs):
        return self


def audit_module():
    if not AUDIT_PATH.is_file():
        return None
    spec = importlib.util.spec_from_file_location("build_audit_contract", AUDIT_PATH)
    assert spec and spec.loader, "DEFECT [build audit module]: build_audit.py must be importable"
    loaded = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(loaded)
    finally:
        _LOADED_AUDIT_MODULES.append(loaded)
    return loaded


def audit_api():
    loaded = audit_module()
    value = getattr(loaded, "audit_build", None) if loaded is not None else None
    return value if callable(value) else MissingAudit("audit_build")


def test_build_audit_cli_requires_fixed_isolated_python_runtime():
    nonisolated = subprocess.run(
        [str(TRUSTED_PYTHON), str(AUDIT_PATH), "--help"],
        text=True,
        capture_output=True,
        check=False,
    )
    isolated = subprocess.run(
        [str(TRUSTED_PYTHON), "-I", str(AUDIT_PATH), "--help"],
        text=True,
        capture_output=True,
        check=False,
    )
    exact = subprocess.run(
        [str(TRUSTED_PYTHON), "-I", "-S", str(AUDIT_PATH), "--help"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert nonisolated.returncode != 0
    assert "isolated" in (nonisolated.stdout + nonisolated.stderr).lower()
    assert isolated.returncode != 0
    assert "no-site" in (isolated.stdout + isolated.stderr).lower()
    assert exact.returncode == 0, exact.stderr


def test_build_audit_cli_cleans_controlled_pycache_after_early_parser_failure(
    tmp_path: Path,
):
    repo = tmp_path / "repo"
    build = tmp_path / "build"
    tex_temp = build / ".tex-tmp"
    repo.mkdir()
    tex_temp.mkdir(parents=True)
    command_record = build / "commands.json"
    before = set(tex_temp.glob("gauge-vfe-rg-pypdf-pycache-*"))
    completed = subprocess.run(
        [
            str(TRUSTED_PYTHON),
            "-I",
            "-S",
            str(AUDIT_PATH),
            "--repo-root",
            str(repo.resolve()),
            "--build-dir",
            str(build.resolve()),
            "--source-revision",
            "0" * 40,
            "--command-record",
            str(command_record.resolve()),
            "--output",
            str(command_record.resolve()),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode != 0
    assert set(tex_temp.glob("gauge-vfe-rg-pypdf-pycache-*")) == before


def test_executable_lock_bootstrap_closes_partial_acquisition_on_snapshot_failure(
    monkeypatch: pytest.MonkeyPatch,
):
    loaded = audit_module()
    assert loaded is not None

    class FakeStream:
        def __init__(self) -> None:
            self.closed = False

        def close(self) -> None:
            self.closed = True

    streams = [FakeStream(), FakeStream()]
    acquisitions = iter(streams)
    snapshots = 0

    def fake_open(path: Path):
        return Path(path), next(acquisitions)

    def fake_snapshot(path: Path, stream: FakeStream):
        nonlocal snapshots
        snapshots += 1
        if snapshots == 2:
            raise OSError("controlled second snapshot failure")
        return {"path": str(path), "sha256": "0" * 64, "byte_count": 0}

    monkeypatch.setattr(loaded, "_open_deny_write_file", fake_open)
    monkeypatch.setattr(loaded, "_locked_stream_snapshot", fake_snapshot)
    with pytest.raises(OSError, match="controlled second snapshot failure"):
        loaded._acquire_audit_executable_locks()
    assert all(stream.closed for stream in streams)


def test_test_loader_releases_authenticated_finder_before_the_next_test():
    """An audit unit test must not block another verifier's fixed-site imports."""

    spec = importlib.util.find_spec("scipy")
    assert spec is not None
    assert isinstance(spec.origin, str)
    assert Path(spec.origin).resolve().is_relative_to(TRUSTED_PYPDF_SITE.resolve())


def git(repo: Path, *args: str) -> str:
    completed = subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True, check=False)
    assert completed.returncode == 0, f"DEFECT [git fixture]: git {' '.join(args)} failed: {completed.stderr}"
    return completed.stdout.strip()


def commit(repo: Path, message: str) -> str:
    git(repo, "add", "-A")
    git(repo, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def two_page_pdf() -> bytes:
    first_stream = b"BT /F1 12 Tf 72 720 Td (audit page one) Tj ET"
    second_stream = b"BT /F1 12 Tf 72 720 Td (audit page two) Tj ET"
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 7 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 7 0 R >> >> /Contents 6 0 R >>",
        f"<< /Length {len(first_stream)} >>\nstream\n".encode() + first_stream + b"\nendstream",
        f"<< /Length {len(second_stream)} >>\nstream\n".encode() + second_stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        (
            b"<< /Title (Gauge VFE RG Build Audit Fixture) /Author (Robert C. Dennis) "
            b"/Subject (Lifecycle build verification) /Keywords (gauge, VFE, RG) "
            b"/Creator (pytest fixture) /Producer (hand-built PDF fixture) "
            b"/CreationDate (D:20260803093000-05'00') /ModDate (D:20260803093000-05'00') >>"
        ),
    ]
    document = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, body in enumerate(objects, 1):
        offsets.append(len(document))
        document.extend(f"{number} 0 obj\n".encode() + body + b"\nendobj\n")
    xref = len(document)
    document.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    document.extend(b"0000000000 65535 f \n")
    document.extend(b"".join(f"{offset:010d} 00000 n \n".encode() for offset in offsets[1:]))
    document.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R /Info 8 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    return bytes(document)


def validate_pdf_fixture(path: Path) -> None:
    # This intentionally does not trust the audit module: it checks the fixture's
    # PDF cross-reference, catalog, pages tree, and stream framing independently.
    raw = path.read_bytes()
    assert raw.startswith(b"%PDF-1.4\n") and b"xref\n0 9\n" in raw and raw.rstrip().endswith(b"%%EOF"), "DEFECT [PDF fixture]: missing PDF header/xref/trailer"
    assert b"/Type /Catalog /Pages 2 0 R" in raw and b"/Type /Pages /Kids [3 0 R 4 0 R] /Count 2" in raw, "DEFECT [PDF fixture]: invalid two-page catalog/pages tree"
    assert raw.count(b"/Type /Page /Parent 2 0 R") == 2 and raw.count(b"stream\nBT /F1 12 Tf") == 2, "DEFECT [PDF fixture]: page content streams are malformed"
    assert b"/Info 8 0 R" in raw and b"/Title (Gauge VFE RG Build Audit Fixture)" in raw and b"/Subject (Lifecycle build verification)" in raw, "DEFECT [PDF fixture]: real /Info metadata is missing"


def validate_tex_fixture(root: Path, build: Path) -> None:
    source = (root / "main.tex").read_text(encoding="utf-8")
    auxiliary = (build / "main.aux").read_text(encoding="utf-8")
    bibliography = (build / "main.bbl").read_text(encoding="utf-8")
    assert r"\n" not in source and source.count("\n") == 4, "DEFECT [TeX fixture]: source must use actual line breaks and contain no literal \\n command"
    assert r"\label{one}" in source and r"\newlabel{one}" in auxiliary, "DEFECT [TeX fixture]: source and auxiliary label records disagree"
    assert r"\cite{x}" in source and r"\bibitem{x}" in bibliography, "DEFECT [TeX fixture]: source and bibliography citation records disagree"


def artifacts(tmp_path: Path, log: str | None = None) -> tuple[Path, Path, dict[str, object]]:
    root, build = tmp_path / "repo", tmp_path / "build"
    root.mkdir()
    build.mkdir()
    (root / "main.tex").write_text("\\documentclass{article}\n\\begin{document}\n\\label{one}Audit~\\cite{x}.\n\\end{document}\n", encoding="utf-8")
    git(root, "init")
    git(root, "config", "core.autocrlf", "false")
    source_revision = commit(root, "source")
    pdf_bytes = two_page_pdf()
    (build / "main.pdf").write_bytes(pdf_bytes)
    validate_pdf_fixture(build / "main.pdf")
    if log is None:
        log = f"This is pdfTeX\nOutput written on main.pdf (2 pages, {len(pdf_bytes)} bytes).\n"
    else:
        log = f"This is pdfTeX\n{log}Output written on main.pdf (2 pages, {len(pdf_bytes)} bytes).\n"
    (build / "main.log").write_text(log, encoding="utf-8")
    (build / "main.aux").write_text("\\relax \n\\newlabel{one}{{1}{1}}\n", encoding="utf-8")
    (build / "main.bbl").write_text("\\begin{thebibliography}{1}\n\\bibitem{x} X.\n\\end{thebibliography}\n", encoding="utf-8")
    (build / "main.toc").write_text("\\contentsline {section}{Audit}{1}{}%\n", encoding="utf-8")
    validate_tex_fixture(root, build)
    commands = [
        {"argv": ["pdflatex", "-interaction=nonstopmode", "main.tex"], "returncode": 0, "tool_version": "fixture-pdftex-1"},
        {"argv": ["bibtex", "main"], "returncode": 0, "tool_version": "fixture-bibtex-1"},
        {"argv": ["pdflatex", "-interaction=nonstopmode", "main.tex"], "returncode": 0, "tool_version": "fixture-pdftex-1"},
        {"argv": ["pdflatex", "-interaction=nonstopmode", "main.tex"], "returncode": 0, "tool_version": "fixture-pdftex-1"},
    ]
    (build / "commands.json").write_text(json.dumps(commands), encoding="utf-8")
    inventory = {"main.tex": hashlib.sha256((root / "main.tex").read_bytes()).hexdigest()}
    expected = {
        "commands": commands,
        "tool_versions": {"pdflatex": "fixture-pdftex-1", "bibtex": "fixture-bibtex-1"},
        "input_inventory": inventory,
        "source_manifest_digest": hashlib.sha256(json.dumps(inventory, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "pdf_sha256": hashlib.sha256(pdf_bytes).hexdigest(),
        "pdf_byte_count": len(pdf_bytes),
        "page_count": 2,
        "pdf_metadata": PDF_METADATA,
        "source_revision": source_revision,
        "artifact_hashes": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(build.iterdir()) if path.is_file()},
    }
    return root, build, expected


def run_audit(root: Path, build: Path, defect: str):
    return audit_api()(
        repo_root=root,
        build_dir=build,
        source_revision=git(root, "rev-parse", "HEAD"),
        command_record=build / "commands.json",
        test_fixture=True,
    )


def file_identity(path: Path, *, repo: Path | None = None) -> dict[str, object]:
    name = path.relative_to(repo).as_posix() if repo is not None else str(path.resolve())
    payload = path.read_bytes()
    return {
        "path": name,
        "sha256": hashlib.sha256(payload).hexdigest(),
        "byte_count": len(payload),
    }


def production_artifacts(
    tmp_path: Path,
) -> tuple[Path, Path, str, dict[str, object], Path]:
    """Create a production-shape audit fixture without invoking TeX."""

    root = tmp_path / "production-repo"
    source = root / "manuscripts" / "gauge_vfe_rg"
    verification = source / "verification"
    build = tmp_path / "production-build"
    tools = tmp_path / "production-tools"
    external = tmp_path / "tex-system-input.sty"
    verification.mkdir(parents=True)
    build.mkdir()
    tools.mkdir()
    texmf_home = build / ".texmf-home"
    texmf_var = build / ".texmf-var"
    texmf_config = build / ".texmf-config"
    tex_temp = build / ".tex-tmp"
    texmf_home.mkdir()
    texmf_var.mkdir()
    texmf_config.mkdir()
    tex_temp.mkdir()

    main_tex = source / "main.tex"
    main_tex.write_text(
        "\\documentclass{article}\n\\begin{document}\n\\label{one}Audit~\\cite{x}.\n"
        "\\bibliographystyle{plainnat}\n\\bibliography{references}\n\\end{document}\n",
        encoding="utf-8",
    )
    build_script = source / "build.ps1"
    run_checks = verification / "run_checks.py"
    build_audit = verification / "build_audit.py"
    references_bib = source.parent / "references.bib"
    build_script.write_text("# production fixture build driver\n", encoding="utf-8")
    run_checks.write_text("# production fixture numerical verifier\n", encoding="utf-8")
    build_audit.write_text("# production fixture build auditor\n", encoding="utf-8")
    references_bib.write_text("@misc{x, title={X}}\n", encoding="utf-8")
    git(root, "init")
    git(root, "config", "core.autocrlf", "false")
    source_revision = commit(root, "production source")
    source_epoch = git(root, "show", "-s", "--format=%ct", source_revision)
    bootstrap_directory = tmp_path / "production-bootstrap"
    bootstrap_directory.mkdir()
    executed_build_script = bootstrap_directory / "build.ps1"
    executed_build_script.write_bytes(build_script.read_bytes())
    bootstrap_attestation = bootstrap_directory / "bootstrap-attestation.json"
    executed_bytes = executed_build_script.read_bytes()
    bootstrap_attestation.write_text(
        json.dumps(
            {
                "protocol_profile": PRODUCTION_PROFILE,
                "source_revision": source_revision,
                "repository_root": str(root.resolve()),
                "source_directory": str(source.resolve()),
                "repository_build_script": str(build_script.resolve()),
                "executed_build_script": str(executed_build_script.resolve()),
                "source_blob_oid": git(
                    root,
                    "rev-parse",
                    f"{source_revision}:manuscripts/gauge_vfe_rg/build.ps1",
                ),
                "source_blob_byte_count": len(executed_bytes),
                "source_sha256": hashlib.sha256(executed_bytes).hexdigest(),
                "bootstrap_temporary_directory": str(bootstrap_directory.resolve()),
                "bootstrap_parent_pid": os.getpid(),
                "powershell_path": str(
                    Path(r"C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe")
                ),
                "git_path": str(TRUSTED_GIT),
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    verification_result = verification / "result.json"
    manifest_bound_inputs = {
        path.relative_to(root).as_posix(): {
            "byte_count": len(payload := path.read_bytes()),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }
        for path in (build_script, main_tex, run_checks, build_audit, references_bib)
    }
    verification_result.write_text(
        json.dumps(
            {
                "protocol_profile": PRODUCTION_PROFILE,
                "source_revision": source_revision,
                "overall_status": "PASS",
                "manifest": {
                    "hash_algorithm": "SHA-256",
                    "hash_domain": "raw file bytes",
                    "path_semantics": "repository-relative POSIX paths",
                    "bound_inputs": manifest_bound_inputs,
                },
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    pdf_bytes = two_page_pdf()
    (build / "main.pdf").write_bytes(pdf_bytes)
    (build / "main.log").write_text(
        f"This is pdfTeX\nOutput written on main.pdf (2 pages, {len(pdf_bytes)} bytes).\n",
        encoding="utf-8",
    )
    (build / "main.aux").write_text(
        "\\relax \n\\newlabel{one}{{1}{1}}\n\\bibstyle{plainnat}\n\\bibdata{references}\n",
        encoding="utf-8",
    )
    (build / "main.bbl").write_text(
        "\\begin{thebibliography}{1}\n\\bibitem{x} X.\n\\end{thebibliography}\n",
        encoding="utf-8",
    )
    (build / "main.toc").write_text("\\contentsline {section}{Audit}{1}{}%\n", encoding="utf-8")
    (build / "main.blg").write_text(
        "The style file: plainnat.bst\nDatabase file #1: references.bib\n",
        encoding="utf-8",
    )
    (build / "main-bibtex.aux").write_bytes((build / "main.aux").read_bytes())
    (build / "main-bibtex.blg").write_bytes((build / "main.blg").read_bytes())
    (build / "main-bibtex.bbl").write_bytes((build / "main.bbl").read_bytes())
    external.write_text("% controlled external TeX-system fixture\n", encoding="utf-8")

    pdflatex = tools / "pdflatex.exe"
    bibtex = tools / "bibtex.exe"
    bibtex_style = tools / "plainnat.bst"
    pdflatex.write_bytes(b"controlled-pdflatex-fixture")
    bibtex.write_bytes(b"controlled-bibtex-fixture")
    bibtex_style.write_text("ENTRY{}{}{}\n", encoding="utf-8")
    executable_by_tool = {"pdflatex": pdflatex, "bibtex": bibtex}
    base_time = datetime(2026, 8, 3, 15, 0, tzinfo=timezone.utc)
    commands: list[dict[str, object]] = []
    for index, tool in enumerate(("pdflatex", "bibtex", "pdflatex", "pdflatex"), 1):
        executable = executable_by_tool[tool].resolve()
        stdout_name = f"command-{index:02d}.stdout.txt"
        stderr_name = f"command-{index:02d}.stderr.txt"
        (build / stdout_name).write_text(f"{tool} stdout {index}\n", encoding="utf-8")
        (build / stderr_name).write_text("", encoding="utf-8")
        argv = (
            [
                str(executable),
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-file-line-error",
                "-recorder",
                "-no-shell-escape",
                str(main_tex.resolve()),
            ]
            if tool == "pdflatex"
            else [str(executable), "main"]
        )
        started = base_time + timedelta(seconds=(index - 1) * 2)
        ended = started + timedelta(seconds=1)
        controlled_environment = {
            "TEXINPUTS": f"{source.resolve()};{source.parent.resolve()};",
            "BIBINPUTS": str(source.parent.resolve()),
            "BSTINPUTS": str(bibtex_style.resolve().parent),
            "TEXMFHOME": str(texmf_home.resolve()),
            "TEXMFVAR": str(texmf_var.resolve()),
            "TEXMFCONFIG": str(texmf_config.resolve()),
            "SOURCE_DATE_EPOCH": source_epoch,
        }
        commands.append(
            {
                "argv": argv,
                "returncode": 0,
                "tool_version": f"sha256:{hashlib.sha256(executable.read_bytes()).hexdigest()}",
                "executable": str(executable),
                "cwd": str(build.resolve()),
                "started_at_utc": started.isoformat().replace("+00:00", "Z"),
                "ended_at_utc": ended.isoformat().replace("+00:00", "Z"),
                "stdout_sha256": hashlib.sha256((build / stdout_name).read_bytes()).hexdigest(),
                "stderr_sha256": hashlib.sha256((build / stderr_name).read_bytes()).hexdigest(),
                "stdout_artifact": stdout_name,
                "stderr_artifact": stderr_name,
                "environment": {
                    "SystemRoot": str(WINDOWS_DIRECTORY),
                    "WINDIR": str(WINDOWS_DIRECTORY),
                    "SystemDrive": "C:",
                    "COMSPEC": str(WINDOWS_SYSTEM_DIRECTORY / "cmd.exe"),
                    "PATHEXT": ".COM;.EXE;.BAT;.CMD",
                    "PATH": f"{executable.parent};{WINDOWS_SYSTEM_DIRECTORY}",
                    "TEMP": str(tex_temp.resolve()),
                    "TMP": str(tex_temp.resolve()),
                    **controlled_environment,
                },
            }
        )
    (build / "commands.json").write_text(json.dumps(commands), encoding="utf-8")
    recorder_text = "\n".join(
        (
            f"PWD {build.resolve()}",
            f"INPUT {main_tex.resolve()}",
            f"INPUT {(build / 'main.aux').resolve()}",
            f"INPUT {(build / 'main.bbl').resolve()}",
            f"INPUT {external.resolve()}",
            "",
        )
    )
    (build / "main.fls").write_text(recorder_text, encoding="utf-8")
    recorder_paths = {
        f"pass_{number}": build / f"main-pass-{number}.fls" for number in (1, 3, 4)
    }
    for recorder_path in recorder_paths.values():
        recorder_path.write_text(recorder_text, encoding="utf-8")

    def inventory_identity(path: Path) -> dict[str, object]:
        payload = path.read_bytes()
        return {
            "sha256": hashlib.sha256(payload).hexdigest(),
            "byte_count": len(payload),
        }

    evidence_input_inventory = {
        "repository": {
            key: inventory_identity(path)
            for key, path in sorted(
                {
                    main_tex.relative_to(root).as_posix(): main_tex,
                    references_bib.relative_to(root).as_posix(): references_bib,
                }.items()
            )
        },
        "build": {
            "main-bibtex.bbl": inventory_identity(build / "main-bibtex.bbl"),
            "main.aux": inventory_identity(build / "main.aux"),
            "main.bbl": inventory_identity(build / "main.bbl"),
        },
        "external": {
            str(path.resolve()): inventory_identity(path)
            for path in sorted((external, bibtex_style), key=lambda item: str(item.resolve()))
        },
    }
    context = {
        "protocol_profile": PRODUCTION_PROFILE,
        "source_revision": source_revision,
        "head_revision": source_revision,
        "repository_root": str(root.resolve()),
        "source_directory": str(source.resolve()),
        "output_directory": str(build.resolve()),
        "initial_entries": [],
        "source_date_epoch": source_epoch,
        "controlled_environment": {
            "TEXINPUTS": f"{source.resolve()};{source.parent.resolve()};",
            "BIBINPUTS": str(source.parent.resolve()),
            "BSTINPUTS": str(bibtex_style.resolve().parent),
            "TEXMFHOME": str(texmf_home.resolve()),
            "TEXMFVAR": str(texmf_var.resolve()),
            "TEXMFCONFIG": str(texmf_config.resolve()),
            "SOURCE_DATE_EPOCH": source_epoch,
        },
        "locked_repository_inputs": manifest_bound_inputs,
        "python_executable": file_identity(TRUSTED_PYTHON),
        "git_executable": file_identity(TRUSTED_GIT),
        "pdflatex_executable": file_identity(pdflatex),
        "bibtex_executable": file_identity(bibtex),
        "build_script": file_identity(build_script, repo=root),
        "repository_build_script": file_identity(build_script),
        "executed_build_script": file_identity(executed_build_script),
        "bootstrap_attestation": file_identity(bootstrap_attestation),
        "main_tex": file_identity(main_tex, repo=root),
        "run_checks": file_identity(run_checks, repo=root),
        "build_audit": file_identity(build_audit, repo=root),
        "references_bib": file_identity(references_bib, repo=root),
        "bibtex_style": file_identity(bibtex_style),
        "verification_result": file_identity(verification_result, repo=root),
        "external_input_fixed_point": {
            "max_iterations": 8,
            "converged_iteration": 2,
            "inputs": evidence_input_inventory["external"],
        },
        "recorder_snapshots": {
            key: file_identity(path) for key, path in recorder_paths.items()
        },
        "evidence_input_inventory": evidence_input_inventory,
    }
    (build / "build-context.json").write_text(json.dumps(context), encoding="utf-8")
    return root, build, source_revision, context, external


def run_production_audit(root: Path, build: Path, revision: str):
    return audit_api()(
        repo_root=root,
        build_dir=build,
        source_revision=revision,
        command_record=build / "commands.json",
    )


def require_field(value, name: str, defect: str):
    assert hasattr(value, name), f"DEFECT [{defect}]: missing {name}"
    return getattr(value, name)


def diagnostic_text(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).lower()


def test_production_is_default_and_synthetic_relaxation_is_explicit_api_only(tmp_path: Path):
    root, build, _expected = artifacts(tmp_path)
    production = audit_api()(
        repo_root=root,
        build_dir=build,
        source_revision=git(root, "rev-parse", "HEAD"),
        command_record=build / "commands.json",
    )
    synthetic = run_audit(root, build, "explicit synthetic fixture")
    assert require_field(production, "ok", "production default") is False, (
        "DEFECT [production default]: a minimal synthetic envelope passed without test_fixture=True"
    )
    assert PRODUCTION_PROFILE in diagnostic_text(production), (
        "DEFECT [production default]: rejection did not name the exact production profile"
    )
    assert require_field(synthetic, "ok", "explicit synthetic fixture") is True
    assert require_field(synthetic, "protocol_profile", "explicit synthetic fixture") == "synthetic-test-fixture-v1"


def test_synthetic_relaxation_rejects_truthy_non_bool_and_production_envelopes(tmp_path: Path):
    type_check_root = tmp_path / "type-check"
    type_check_root.mkdir()
    root, build, _expected = artifacts(type_check_root)
    with pytest.raises(TypeError, match="bool"):
        audit_api()(
            repo_root=root,
            build_dir=build,
            source_revision=git(root, "rev-parse", "HEAD"),
            command_record=build / "commands.json",
            test_fixture="yes",
        )

    production_root, production_build, revision, _context, _external = production_artifacts(
        tmp_path / "production-shape"
    )
    outcome = audit_api()(
        repo_root=production_root,
        build_dir=production_build,
        source_revision=revision,
        command_record=production_build / "commands.json",
        test_fixture=True,
    )
    assert require_field(outcome, "ok", "fixture production-envelope guard") is False
    assert "production-shaped" in diagnostic_text(outcome)


def test_synthetic_fixture_with_lone_recorder_artifact_is_not_production_shaped(tmp_path: Path):
    root, build, _expected = artifacts(tmp_path)
    (build / "main.fls").write_text(
        f"PWD {build.resolve()}\nINPUT {(root / 'main.tex').resolve()}\n",
        encoding="utf-8",
    )
    outcome = run_audit(root, build, "lone synthetic recorder")
    assert require_field(outcome, "ok", "lone synthetic recorder") is True, diagnostic_text(outcome)


def test_complete_production_envelope_is_accepted_and_inventory_is_classified(tmp_path: Path):
    root, build, revision, context, external = production_artifacts(tmp_path)
    outcome = run_production_audit(root, build, revision)
    assert require_field(outcome, "ok", "production envelope") is True, diagnostic_text(outcome)
    assert require_field(outcome, "protocol_profile", "production envelope") == PRODUCTION_PROFILE
    assert require_field(outcome, "build_context", "production envelope") == context
    inventory = require_field(outcome, "input_inventory", "production envelope")
    assert set(inventory) == {"repository", "build", "external"}
    assert "manuscripts/gauge_vfe_rg/main.tex" in inventory["repository"]
    assert "main.aux" in inventory["build"]
    assert str(external.resolve()) in inventory["external"]
    assert require_field(outcome, "pdf_sha256", "production envelope") == require_field(
        outcome, "artifact_hashes", "production envelope"
    )["main.pdf"]
    provenance = require_field(outcome, "inspection_tool_versions", "production envelope")
    assert set(provenance) == {
        "pypdf",
        "pypdf_module_path",
        "pypdf_module_sha256",
        "pypdf_package_root",
        "pypdf_package_tree_sha256",
        "pypdf_package_file_count",
        "pypdf_distribution_root",
        "pypdf_record_path",
        "pypdf_record_sha256",
        "pypdf_pycache_prefix",
    }
    assert Path(provenance["pypdf_package_root"]).resolve() == TRUSTED_PYPDF_ROOT.resolve()
    assert Path(provenance["pypdf_module_path"]).resolve() == (
        TRUSTED_PYPDF_ROOT / "__init__.py"
    ).resolve()
    assert provenance["pypdf_module_sha256"] == hashlib.sha256(
        Path(provenance["pypdf_module_path"]).read_bytes()
    ).hexdigest()
    assert provenance["pypdf_record_sha256"] == hashlib.sha256(
        Path(provenance["pypdf_record_path"]).read_bytes()
    ).hexdigest()
    assert isinstance(provenance["pypdf"], str) and provenance["pypdf"]
    assert provenance["pypdf"] == "6.12.2"
    assert context["locked_repository_inputs"] == json.loads(
        root.joinpath(*context["verification_result"]["path"].split("/"))
        .read_text(encoding="utf-8")
    )["manifest"]["bound_inputs"]
    assert isinstance(provenance["pypdf_package_file_count"], int)
    assert provenance["pypdf_package_file_count"] > 1
    assert len(provenance["pypdf_package_tree_sha256"]) == 64


@pytest.mark.parametrize("attack", ("write", "rename", "substitute"))
def test_production_audit_holds_semantic_artifact_handles_against_real_aba_attacks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    attack: str,
):
    """A semantic read must never observe bytes other than its retained M0 bytes."""

    root, build, revision, _context, _external = production_artifacts(tmp_path)
    loaded = audit_module()
    assert loaded is not None
    victim = build / "main.log"
    original_bytes = victim.read_bytes()
    saved = victim.with_name("main.log.saved-by-attacker")
    replacement = victim.with_name("main.log.attacker-substitute")
    attack_state = {"denied": False, "active_substitute": False}
    original_source_inspection = loaded._inspect_sources
    original_log_inspection = loaded._inspect_log

    def pressure_source_inspection(*args, **kwargs):
        result = original_source_inspection(*args, **kwargs)
        try:
            if attack == "write":
                with victim.open("r+b", buffering=0) as stream:
                    stream.seek(0)
                    stream.write(b"FATAL ERROR".ljust(len(original_bytes), b"!"))
                    stream.flush()
                    os.fsync(stream.fileno())
                    stream.seek(0)
                    stream.write(original_bytes)
                    stream.flush()
                    os.fsync(stream.fileno())
            elif attack == "rename":
                victim.rename(saved)
                saved.rename(victim)
            else:
                replacement.write_bytes(
                    b"This is pdfTeX\nFatal error: attacker semantic substitute\n"
                )
                victim.rename(saved)
                os.replace(replacement, victim)
                attack_state["active_substitute"] = True
        except PermissionError:
            attack_state["denied"] = True
            if replacement.exists():
                replacement.unlink()
        return result

    def restore_before_log_inspection(log_text, *args, **kwargs):
        if attack_state["active_substitute"]:
            victim.unlink()
            saved.rename(victim)
            attack_state["active_substitute"] = False
        return original_log_inspection(log_text, *args, **kwargs)

    monkeypatch.setattr(loaded, "_inspect_sources", pressure_source_inspection)
    monkeypatch.setattr(loaded, "_inspect_log", restore_before_log_inspection)
    outcome = loaded.audit_build(
        repo_root=root,
        build_dir=build,
        source_revision=revision,
        command_record=build / "commands.json",
    )
    assert attack_state["denied"], f"real {attack} attack reached a semantic artifact"
    assert outcome.ok is True, diagnostic_text(outcome)
    assert victim.read_bytes() == original_bytes
    assert not saved.exists()
    assert not replacement.exists()


def test_audit_publication_create_new_preserves_raced_in_sentinel(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    loaded = audit_module()
    assert loaded is not None
    publish = getattr(loaded, "_publish_new_json_with_digest", None)
    assert callable(publish), "build auditor must expose its fail-closed publication primitive"
    target = tmp_path / "audit.json"
    sentinel = b"DO NOT OVERWRITE THIS RACED-IN SENTINEL"
    original_canonicalizer = loaded._canonical_json_bytes

    def race_after_preflight(value):
        payload = original_canonicalizer(value)
        target.write_bytes(sentinel)
        return payload

    monkeypatch.setattr(loaded, "_canonical_json_bytes", race_after_preflight)
    with pytest.raises(FileExistsError):
        publish(target, {"ok": True}, io.BytesIO())
    assert target.read_bytes() == sentinel


def test_audit_publication_retains_create_new_handle_through_digest_emission(tmp_path: Path):
    loaded = audit_module()
    assert loaded is not None
    publish = getattr(loaded, "_publish_new_json_with_digest", None)
    assert callable(publish), "build auditor must expose its fail-closed publication primitive"
    target = tmp_path / "audit.json"
    replacement = tmp_path / "replacement.json"
    document = {"z": 1, "ok": True, "unicode": "Fisher \u03c4"}
    expected = '{"ok":true,"unicode":"Fisher \u03c4","z":1}'.encode("utf-8")

    class AttackingStdout:
        def __init__(self):
            self.payload = bytearray()
            self.write_denied = False
            self.substitution_denied = False

        def write(self, payload: bytes) -> int:
            try:
                target.write_bytes(b"ATTACKER WRITE")
            except PermissionError:
                self.write_denied = True
            replacement.write_bytes(b"ATTACKER SUBSTITUTE")
            try:
                os.replace(replacement, target)
            except PermissionError:
                self.substitution_denied = True
            self.payload.extend(payload)
            return len(payload)

        def flush(self) -> None:
            return None

    stdout = AttackingStdout()
    digest = publish(target, document, stdout)
    assert stdout.write_denied
    assert stdout.substitution_denied
    assert target.read_bytes() == expected
    assert digest == hashlib.sha256(expected).hexdigest()
    assert bytes(stdout.payload) == f"BUILD_AUDIT_SHA256={digest}\n".encode("ascii")


def production_provenance_paths(build: Path) -> tuple[Path, ...]:
    return tuple(
        build / name
        for name in (
            "main-pass-1.fls",
            "main-pass-3.fls",
            "main-pass-4.fls",
            "main-bibtex.aux",
            "main-bibtex.blg",
            "main-bibtex.bbl",
        )
    )


def test_production_audit_reads_provenance_under_retained_read_only_locks(
    tmp_path: Path,
):
    root, build, revision, _context, _external = production_artifacts(tmp_path)
    with held_windows_read_locks(production_provenance_paths(build)):
        outcome = run_production_audit(root, build, revision)
    assert require_field(outcome, "ok", "retained provenance handles") is True, (
        diagnostic_text(outcome)
    )


def test_retained_read_only_provenance_locks_deny_write_and_substitution(
    tmp_path: Path,
):
    import ctypes
    from ctypes import wintypes

    _root, build, _revision, _context, _external = production_artifacts(tmp_path)
    paths = production_provenance_paths(build)
    before = {path: path.read_bytes() for path in paths}
    target = paths[0]
    replacement = target.with_name(f"{target.name}.replacement")
    replacement.write_bytes(b"ATTACKER SUBSTITUTE")
    moved = target.with_name(f"{target.name}.saved")
    with held_windows_read_locks(paths) as (kernel32, _handles):
        writer = kernel32.CreateFileW(
            str(target.resolve()),
            0x40000000,  # GENERIC_WRITE
            0x00000007,  # FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE
            None,
            3,  # OPEN_EXISTING
            0x00000080,
            None,
        )
        assert writer == ctypes.c_void_p(-1).value
        assert ctypes.get_last_error() == 32  # ERROR_SHARING_VIOLATION

        move_file = kernel32.MoveFileExW
        move_file.argtypes = (wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD)
        move_file.restype = wintypes.BOOL
        assert not move_file(str(target.resolve()), str(moved.resolve()), 0x1)
        assert ctypes.get_last_error() == 32
        assert not move_file(str(replacement.resolve()), str(target.resolve()), 0x1)
        assert ctypes.get_last_error() in {5, 32}  # ACCESS_DENIED or SHARING_VIOLATION
    assert all(path.read_bytes() == payload for path, payload in before.items())
    assert not moved.exists()


@pytest.mark.parametrize("snapshot_kind", ["aux", "blg", "bbl"])
def test_production_audit_rejects_forged_bibtex_provenance_snapshot(
    tmp_path: Path,
    snapshot_kind: str,
):
    root, build, revision, context, _external = production_artifacts(tmp_path)
    snapshot = build / f"main-bibtex.{snapshot_kind}"
    if snapshot_kind == "aux":
        snapshot.write_text(
            "\\bibstyle{attacker}\n\\bibdata{../attacker}\n",
            encoding="utf-8",
        )
    elif snapshot_kind == "blg":
        snapshot.write_text(
            "The style file: attacker.bst\nDatabase file #1: ../attacker.bib\n",
            encoding="utf-8",
        )
    else:
        snapshot.write_bytes(b"ATTACKER BBL WITH VALID RETAINED INVENTORY IDENTITY\n")
        payload = snapshot.read_bytes()
        context["evidence_input_inventory"]["build"]["main-bibtex.bbl"] = {
            "sha256": hashlib.sha256(payload).hexdigest(),
            "byte_count": len(payload),
        }
        (build / "build-context.json").write_text(json.dumps(context), encoding="utf-8")

    outcome = run_production_audit(root, build, revision)
    assert require_field(outcome, "ok", f"forged BibTeX {snapshot_kind} snapshot") is False
    diagnostics = diagnostic_text(outcome)
    assert f"main-bibtex.{snapshot_kind}" in diagnostics or "bibtex" in diagnostics


@pytest.mark.parametrize(
    "ambient_normalization",
    ["worktree_gitattributes", "git_info_attributes", "core_autocrlf"],
)
def test_production_audit_rejects_raw_crlf_mismatch_despite_ambient_normalization(
    tmp_path: Path,
    ambient_normalization: str,
):
    root, build, revision, context, _external = production_artifacts(tmp_path)
    main_tex = root / "manuscripts" / "gauge_vfe_rg" / "main.tex"
    main_relative = main_tex.relative_to(root).as_posix()
    crlf_bytes = main_tex.read_bytes().replace(b"\n", b"\r\n")
    main_tex.write_bytes(crlf_bytes)
    if ambient_normalization == "worktree_gitattributes":
        (root / ".gitattributes").write_text("*.tex text eol=crlf\n", encoding="utf-8")
    elif ambient_normalization == "git_info_attributes":
        info_attributes = root / ".git" / "info" / "attributes"
        info_attributes.parent.mkdir(parents=True, exist_ok=True)
        info_attributes.write_text("*.tex text eol=crlf\n", encoding="utf-8")
    else:
        git(root, "config", "core.autocrlf", "true")

    current_identity = {
        "sha256": hashlib.sha256(crlf_bytes).hexdigest(),
        "byte_count": len(crlf_bytes),
    }
    context["locked_repository_inputs"][main_relative] = current_identity
    context["main_tex"] = {"path": main_relative, **current_identity}
    context["evidence_input_inventory"]["repository"][main_relative] = current_identity
    (build / "build-context.json").write_text(json.dumps(context), encoding="utf-8")

    outcome = run_production_audit(root, build, revision)
    assert require_field(outcome, "ok", "raw CRLF source binding") is False
    diagnostics = diagnostic_text(outcome)
    assert "main.tex" in diagnostics
    assert "raw" in diagnostics or "revision" in diagnostics


def test_pypdf_actual_bytes_must_match_unchanged_record_declarations(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    loaded = audit_module()
    assert loaded is not None
    copied_site = tmp_path / "site-packages"
    copied_root = copied_site / "pypdf"
    shutil.copytree(TRUSTED_PYPDF_ROOT, copied_root)
    source_dist_infos = sorted(TRUSTED_PYPDF_SITE.glob("pypdf-*.dist-info"))
    assert len(source_dist_infos) == 1
    copied_dist_info = copied_site / source_dist_infos[0].name
    shutil.copytree(source_dist_infos[0], copied_dist_info)
    monkeypatch.setattr(loaded, "_TRUSTED_PYPDF_SITE", copied_site)
    monkeypatch.setattr(loaded, "_TRUSTED_PYPDF_ROOT", copied_root)
    monkeypatch.setattr(loaded, "_TRUSTED_PYPDF_INIT", copied_root / "__init__.py")
    monkeypatch.setattr(loaded, "_PYPDF_IMPORTED_PATH", copied_root / "__init__.py")

    baseline = loaded._pypdf_distribution_provenance()
    assert baseline["pypdf_package_file_count"] > 1
    victim = next(path for path in sorted(copied_root.rglob("*.py")) if path.name != "__init__.py")
    victim.write_bytes(victim.read_bytes() + b"\n# controlled mutation with unchanged RECORD\n")
    with pytest.raises(RuntimeError, match="RECORD.*(hash|size)|declared.*(hash|size)"):
        loaded._pypdf_distribution_provenance()


def test_pypdf_record_rejects_nonexact_hash_algorithm(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    loaded = audit_module()
    assert loaded is not None
    copied_site = tmp_path / "site-packages"
    copied_root = copied_site / "pypdf"
    shutil.copytree(TRUSTED_PYPDF_ROOT, copied_root)
    source_dist_infos = sorted(TRUSTED_PYPDF_SITE.glob("pypdf-*.dist-info"))
    assert len(source_dist_infos) == 1
    copied_dist_info = copied_site / source_dist_infos[0].name
    shutil.copytree(source_dist_infos[0], copied_dist_info)
    monkeypatch.setattr(loaded, "_TRUSTED_PYPDF_SITE", copied_site)
    monkeypatch.setattr(loaded, "_TRUSTED_PYPDF_ROOT", copied_root)
    monkeypatch.setattr(loaded, "_TRUSTED_PYPDF_INIT", copied_root / "__init__.py")
    monkeypatch.setattr(loaded, "_PYPDF_IMPORTED_PATH", copied_root / "__init__.py")
    record = copied_dist_info / "RECORD"
    record_text = record.read_text(encoding="utf-8")
    assert "sha256=" in record_text
    record.write_text(record_text.replace("sha256=", "SHA256=", 1), encoding="utf-8")
    with pytest.raises(RuntimeError, match="unsupported declared hash"):
        loaded._pypdf_distribution_provenance()


def test_pypdf_distribution_metadata_must_equal_exact_s_bound_pin(
    monkeypatch: pytest.MonkeyPatch,
):
    loaded = audit_module()
    assert loaded is not None
    monkeypatch.setattr(loaded, "_EXPECTED_PYPDF_VERSION", "6.12.2+attacker")
    with pytest.raises(RuntimeError, match="exact S-bound pin"):
        loaded._pypdf_distribution_provenance()


def test_pypdf_pycache_base_ignores_hostile_temp_and_rejects_reparse(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
):
    loaded = audit_module()
    assert loaded is not None
    poison = tmp_path / "ambient-poison"
    poison.mkdir()
    (poison / "pypdf.pyc").write_bytes(b"attacker bytecode")
    monkeypatch.setenv("TEMP", str(poison))
    monkeypatch.setenv("TMP", str(poison))
    assert loaded._bootstrap_pypdf_pycache_base() == loaded._FIXED_AUDIT_TEMP_BASE.resolve()
    monkeypatch.setattr(
        loaded,
        "_bootstrap_first_reparse_component",
        lambda path: Path(path),
    )
    with pytest.raises(RuntimeError, match="reparse-mediated"):
        loaded._bootstrap_pypdf_pycache_base()


def test_authenticated_loader_rejects_submodule_mutated_after_distribution_m0(
    tmp_path: Path,
):
    loaded = audit_module()
    assert loaded is not None
    origin = tmp_path / "authenticated_submodule.py"
    original = b"VALUE = 1\n"
    origin.write_bytes(original)
    expected_file = {
        "sha256": hashlib.sha256(original).hexdigest(),
        "byte_count": len(original),
    }
    expected_identity = loaded._bootstrap_stat_identity(origin.lstat())
    origin.write_bytes(b"VALUE = 'attacker'\n")

    class NeverExecutedLoader:
        def create_module(self, _spec):
            raise AssertionError("mutated submodule loader must not execute")

    authenticated = loaded._AuthenticatedSiteLoader(
        NeverExecutedLoader(),
        origin,
        expected_file,
        expected_identity,
    )
    with pytest.raises(ImportError, match="changed from pre-import M0"):
        authenticated.create_module(None)


def test_authenticated_finder_blocks_undeclared_fixed_site_transitive_import(
    tmp_path: Path,
):
    loaded = audit_module()
    assert loaded is not None
    site = tmp_path / "fixed-site"
    package = site / "pypdf"
    package.mkdir(parents=True)
    (site / "undeclared_dependency.py").write_text("ATTACK = True\n", encoding="utf-8")
    finder = loaded._AuthenticatedSiteFinder(
        site,
        {
            "provenance": {"pypdf_package_root": str(package)},
            "files": {},
            "file_identities": {},
        },
    )
    with pytest.raises(ModuleNotFoundError, match="outside the authenticated pypdf RECORD"):
        finder.find_spec("undeclared_dependency", [str(site)])


@pytest.mark.parametrize(
    "mutation, token",
    [
        ("missing_fls", "main.fls"),
        ("wrong_pwd", "pwd"),
        ("missing_external", "tex-system-input.sty"),
        ("wrong_cwd", "cwd"),
        ("extra_pdflatex_argument", "argv"),
        ("stream_alias", "unique"),
        ("overlapping_timestamps", "overlap"),
        ("unknown_command_key", "unknown"),
        ("missing_command_key", "missing"),
        ("wrong_child_environment", "environment"),
        ("missing_child_environment_key", "environment"),
        ("extra_child_environment_key", "environment"),
        ("wrong_profile", PRODUCTION_PROFILE),
        ("wrong_python_identity", "python_executable"),
        ("inherited_tex_sentinel", "texinputs"),
        ("inherited_bst_sentinel", "bstinputs"),
        ("changed_bibtex_style", "bibtex_style"),
        ("unrecorded_bibtex_style", "bibtex_style"),
        ("missing_blg", "main.blg"),
        ("wrong_blg_style", "plainnat.bst"),
        ("unlocked_fls_repository_input", "prelocked"),
        ("locked_manifest_mismatch", "bound_inputs"),
        ("case_colliding_locked_input", "case collision"),
    ],
)
def test_production_contract_rejects_each_incomplete_or_ambiguous_envelope(
    tmp_path: Path,
    mutation: str,
    token: str,
):
    root, build, revision, _context, external = production_artifacts(tmp_path)
    commands_path = build / "commands.json"
    context_path = build / "build-context.json"
    commands = json.loads(commands_path.read_text(encoding="utf-8"))
    context = json.loads(context_path.read_text(encoding="utf-8"))
    if mutation == "missing_fls":
        (build / "main.fls").unlink()
    elif mutation == "wrong_pwd":
        fls = (build / "main.fls").read_text(encoding="utf-8")
        (build / "main.fls").write_text(fls.replace(str(build.resolve()), str(tmp_path.resolve()), 1), encoding="utf-8")
    elif mutation == "missing_external":
        external.unlink()
    elif mutation == "wrong_cwd":
        commands[0]["cwd"] = str(tmp_path.resolve())
        commands_path.write_text(json.dumps(commands), encoding="utf-8")
    elif mutation == "extra_pdflatex_argument":
        commands[0]["argv"].insert(-1, "-shell-escape")
        commands_path.write_text(json.dumps(commands), encoding="utf-8")
    elif mutation == "stream_alias":
        commands[1]["stdout_artifact"] = commands[0]["stdout_artifact"]
        commands[1]["stdout_sha256"] = commands[0]["stdout_sha256"]
        commands_path.write_text(json.dumps(commands), encoding="utf-8")
    elif mutation == "overlapping_timestamps":
        commands[1]["started_at_utc"] = commands[0]["started_at_utc"]
        commands_path.write_text(json.dumps(commands), encoding="utf-8")
    elif mutation == "unknown_command_key":
        commands[0]["caller_controlled"] = True
        commands_path.write_text(json.dumps(commands), encoding="utf-8")
    elif mutation == "missing_command_key":
        del commands[0]["cwd"]
        commands_path.write_text(json.dumps(commands), encoding="utf-8")
    elif mutation == "wrong_child_environment":
        commands[0]["environment"]["PATH"] = "C:\\attacker"
        commands_path.write_text(json.dumps(commands), encoding="utf-8")
    elif mutation == "missing_child_environment_key":
        del commands[0]["environment"]["TEMP"]
        commands_path.write_text(json.dumps(commands), encoding="utf-8")
    elif mutation == "extra_child_environment_key":
        commands[0]["environment"]["PYTHONPATH"] = "C:\\attacker"
        commands_path.write_text(json.dumps(commands), encoding="utf-8")
    elif mutation == "wrong_profile":
        context["protocol_profile"] = "synthetic-test-fixture-v1"
        context_path.write_text(json.dumps(context), encoding="utf-8")
    elif mutation == "wrong_python_identity":
        context["python_executable"]["sha256"] = "0" * 64
        context_path.write_text(json.dumps(context), encoding="utf-8")
    elif mutation == "inherited_tex_sentinel":
        context["controlled_environment"]["TEXINPUTS"] += "CALLER_SENTINEL"
        context_path.write_text(json.dumps(context), encoding="utf-8")
    elif mutation == "inherited_bst_sentinel":
        context["controlled_environment"]["BSTINPUTS"] += "CALLER_SENTINEL"
        context_path.write_text(json.dumps(context), encoding="utf-8")
    elif mutation == "changed_bibtex_style":
        Path(context["bibtex_style"]["path"]).write_text("MUTATED STYLE\n", encoding="utf-8")
    elif mutation == "unrecorded_bibtex_style":
        del context["bibtex_style"]
        context_path.write_text(json.dumps(context), encoding="utf-8")
    elif mutation == "missing_blg":
        (build / "main.blg").unlink()
    elif mutation == "wrong_blg_style":
        (build / "main.blg").write_text(
            "The style file: attacker.bst\nDatabase file #1: ../references.bib\n",
            encoding="utf-8",
        )
    elif mutation == "unlocked_fls_repository_input":
        extra_source = root / "manuscripts" / "gauge_vfe_rg" / "attacker.tex"
        extra_source.write_text("attacker input\n", encoding="utf-8")
        with (build / "main.fls").open("a", encoding="utf-8") as stream:
            stream.write(f"INPUT {extra_source.resolve()}\n")
    elif mutation == "locked_manifest_mismatch":
        context["locked_repository_inputs"].pop(
            "manuscripts/gauge_vfe_rg/verification/build_audit.py"
        )
        context_path.write_text(json.dumps(context), encoding="utf-8")
    else:
        first_relative, first_identity = next(iter(context["locked_repository_inputs"].items()))
        context["locked_repository_inputs"][first_relative.upper()] = first_identity
        context_path.write_text(json.dumps(context), encoding="utf-8")
    outcome = run_production_audit(root, build, revision)
    assert require_field(outcome, "ok", mutation) is False, f"DEFECT [{mutation}]: production audit accepted mutation"
    assert token.casefold() in diagnostic_text(outcome), f"DEFECT [{mutation}]: diagnostic did not name {token}"


def test_audit_ignores_caller_git_redirection_and_path_spoofing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    root, build, revision, _context, _external = production_artifacts(tmp_path)
    attacker = tmp_path / "attacker"
    attacker.mkdir()
    (attacker / "payload.txt").write_text("attacker\n", encoding="utf-8")
    git(attacker, "init")
    commit(attacker, "attacker")
    fake_bin = tmp_path / "fake-bin"
    fake_bin.mkdir()
    (fake_bin / "git.cmd").write_text("@echo off\r\nexit /b 91\r\n", encoding="ascii")
    monkeypatch.setenv("PATH", f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}")
    monkeypatch.setenv("GIT_DIR", str(attacker / ".git"))
    monkeypatch.setenv("GIT_WORK_TREE", str(attacker))
    monkeypatch.setenv("GIT_OBJECT_DIRECTORY", str(attacker / ".git" / "objects"))
    outcome = run_production_audit(root, build, revision)
    assert require_field(outcome, "ok", "caller Git redirection") is True, diagnostic_text(outcome)


@pytest.mark.parametrize(
    "relative",
    [
        "info/grafts",
        "shallow",
        "objects/info/alternates",
        "objects/info/http-alternates",
    ],
)
def test_repository_metadata_overrides_are_rejected_before_git_reads(tmp_path: Path, relative: str):
    root, build, revision, _context, _external = production_artifacts(tmp_path)
    metadata = root / ".git" / Path(relative)
    metadata.parent.mkdir(parents=True, exist_ok=True)
    metadata.write_text("poison\n", encoding="utf-8")
    outcome = run_production_audit(root, build, revision)
    assert require_field(outcome, "ok", "Git metadata override") is False
    assert relative.casefold() in diagnostic_text(outcome)


def test_git_metadata_optional_read_allows_only_initial_absence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    loaded = audit_module()
    assert loaded is not None
    target = tmp_path / "grafts"
    assert loaded._optional_metadata_file_snapshot(target) is None
    target.write_bytes(b"")
    original_lstat = Path.lstat
    observations = 0

    def disappearing_lstat(path: Path):
        nonlocal observations
        if path == target:
            observations += 1
            if observations == 2:
                raise FileNotFoundError(str(path))
        return original_lstat(path)

    monkeypatch.setattr(loaded, "_first_reparse_component", lambda _path: None)
    monkeypatch.setattr(Path, "lstat", disappearing_lstat)
    with pytest.raises(OSError, match="disappeared after observation"):
        loaded._optional_metadata_file_snapshot(target)


def test_git_launch_exception_still_runs_nonrecursive_metadata_postflight(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    root, _build, _revision, _context, _external = production_artifacts(tmp_path)
    loaded = audit_module()
    assert loaded is not None
    original_guard = loaded._git_metadata_guard_snapshot
    guard_calls = 0
    observed_command: list[str] = []

    def counted_guard(repo_root: Path, errors: list[str]):
        nonlocal guard_calls
        guard_calls += 1
        return original_guard(repo_root, errors)

    def failed_launch(command: list[str], **_kwargs):
        observed_command.extend(command)
        raise OSError("controlled Git launch failure")

    monkeypatch.setattr(loaded, "_git_metadata_guard_snapshot", counted_guard)
    monkeypatch.setattr(loaded.subprocess, "run", failed_launch)
    with pytest.raises(OSError, match="controlled Git launch failure"):
        loaded._git(root, "rev-parse", "HEAD")
    assert guard_calls == 2
    assert "--literal-pathspecs" in observed_command


def test_audit_rejects_finite_side_chain_revision_and_binds_current_head(tmp_path: Path):
    root, build, revision, context, _external = production_artifacts(tmp_path)
    tree = git(root, "rev-parse", f"{revision}^{{tree}}")
    side_revision = git(
        root,
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit-tree",
        tree,
        "-m",
        "finite side chain",
    )
    result_path = root.joinpath(*context["verification_result"]["path"].split("/"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    result["source_revision"] = side_revision
    result_path.write_text(json.dumps(result), encoding="utf-8")
    context["source_revision"] = side_revision
    context["source_date_epoch"] = git(root, "show", "-s", "--format=%ct", side_revision)
    context["controlled_environment"]["SOURCE_DATE_EPOCH"] = context["source_date_epoch"]
    context["verification_result"] = file_identity(result_path, repo=root)
    (build / "build-context.json").write_text(json.dumps(context), encoding="utf-8")
    outcome = run_production_audit(root, build, side_revision)
    assert require_field(outcome, "ok", "side-chain revision") is False
    assert "ancestor of current head" in diagnostic_text(outcome)


def test_audit_re_resolves_and_rejects_current_head_motion_at_m1(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    root, build, revision, _context, _external = production_artifacts(tmp_path)
    loaded = audit_module()
    assert loaded is not None
    original = loaded._resolve_head_and_require_ancestry
    calls = 0

    def moving_head(repo_root: Path, source_revision: str, errors: list[str]):
        nonlocal calls
        calls += 1
        resolved = original(repo_root, source_revision, errors)
        return "f" * 40 if calls == 2 else resolved

    monkeypatch.setattr(loaded, "_resolve_head_and_require_ancestry", moving_head)
    outcome = loaded.audit_build(
        repo_root=root,
        build_dir=build,
        source_revision=revision,
        command_record=build / "commands.json",
    )
    assert calls == 2
    assert require_field(outcome, "ok", "moving current HEAD") is False
    assert "current git head changed" in diagnostic_text(outcome)


def test_audit_rejects_fixed_executable_identity_change_between_m0_and_m1(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    root, build, revision, _context, _external = production_artifacts(tmp_path)
    loaded = audit_module()
    assert loaded is not None
    original = loaded._trusted_executable_snapshot
    calls: dict[str, int] = {}

    def changing_snapshot(path: Path):
        record, identity = original(path)
        key = str(path)
        calls[key] = calls.get(key, 0) + 1
        if path == loaded._TRUSTED_GIT and calls[key] == 2:
            identity = (*identity[:-1], identity[-1] + 1)
        return record, identity

    monkeypatch.setattr(loaded, "_trusted_executable_snapshot", changing_snapshot)
    outcome = loaded.audit_build(
        repo_root=root,
        build_dir=build,
        source_revision=revision,
        command_record=build / "commands.json",
    )
    assert require_field(outcome, "ok", "executable identity motion") is False
    assert "git_executable bytes or filesystem identity changed" in diagnostic_text(outcome)


def test_fls_input_through_parent_junction_is_rejected_before_resolution(tmp_path: Path):
    root, build, revision, _context, external = production_artifacts(tmp_path)
    target = tmp_path / "junction-target"
    link = tmp_path / "junction-input"
    target.mkdir()
    mediated = target / "mediated.sty"
    mediated.write_text("% mediated input\n", encoding="utf-8")
    powershell = Path(r"C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe")
    junction_command = (
        "New-Item -ItemType Junction -Path '"
        + str(link).replace("'", "''")
        + "' -Target '"
        + str(target).replace("'", "''")
        + "' | Out-Null"
    )
    created = subprocess.run(
        [
            str(powershell),
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            junction_command,
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert created.returncode == 0, f"DEFECT [junction fixture]: {created.stderr}"
    fls_path = build / "main.fls"
    fls = fls_path.read_text(encoding="utf-8")
    fls_path.write_text(
        fls.replace(str(external.resolve()), str(link / mediated.name)),
        encoding="utf-8",
    )
    outcome = run_production_audit(root, build, revision)
    assert outcome.ok is False
    assert "reparse-mediated" in diagnostic_text(outcome)


def test_git_metadata_parent_junction_is_rejected_before_dag_reads(tmp_path: Path):
    root, build, revision, _context, _external = production_artifacts(tmp_path)
    info = root / ".git" / "info"
    info.rename(root / ".git" / "info-original")
    target = tmp_path / "git-info-target"
    target.mkdir()
    powershell = Path(r"C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe")
    junction_command = (
        "New-Item -ItemType Junction -Path '"
        + str(info).replace("'", "''")
        + "' -Target '"
        + str(target).replace("'", "''")
        + "' | Out-Null"
    )
    created = subprocess.run(
        [
            str(powershell),
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            junction_command,
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert created.returncode == 0, f"DEFECT [Git metadata junction fixture]: {created.stderr}"
    outcome = run_production_audit(root, build, revision)
    assert outcome.ok is False
    diagnostics = diagnostic_text(outcome)
    assert "info/grafts" in diagnostics and "reparse-mediated" in diagnostics


def test_clean_parseable_artifacts_emit_verified_metadata_not_fabricated_defaults(tmp_path: Path):
    root, build, expected = artifacts(tmp_path)
    outcome = run_audit(root, build, "clean artifact audit")
    diagnostics = (
        "errors",
        "duplicate_labels",
        "undefined_references",
        "undefined_citations",
        "rerun_requests",
        "fatal_errors",
        "overfull_boxes",
        "literal_double_question_marks",
        "invalid_status_tags",
        "doubled_status_tags",
        "stale_auxiliary_files",
    )
    required = (
        "ok",
        "source_revision",
        "tool_versions",
        "commands",
        "input_inventory",
        "source_manifest_digest",
        "pdf_sha256",
        "pdf_byte_count",
        "page_count",
        "pdf_metadata",
        "artifact_hashes",
        "changed_pages",
        *diagnostics,
    )
    for field in required:
        require_field(outcome, field, "clean artifact audit")
    assert require_field(outcome, "ok", "clean artifact audit") is True, "DEFECT [clean artifact audit]: valid artifacts must pass"
    for field in ("source_revision", "pdf_sha256", "pdf_byte_count", "page_count", "pdf_metadata", "commands", "tool_versions", "input_inventory", "source_manifest_digest", "artifact_hashes"):
        assert require_field(outcome, field, "clean artifact audit") == expected[field], f"DEFECT [clean artifact audit]: exact {field} does not match fixture bytes/records"
    for field in diagnostics:
        assert require_field(outcome, field, "clean artifact audit") == [], f"DEFECT [clean artifact audit]: clean diagnostic {field} must be empty"
    commands = require_field(outcome, "commands", "clean artifact audit")
    assert tuple(Path(command["argv"][0]).stem.lower() for command in commands) == (
        "pdflatex",
        "bibtex",
        "pdflatex",
        "pdflatex",
    ), "DEFECT [clean artifact audit]: command evidence must be exactly pdflatex, bibtex, pdflatex, pdflatex"
    assert require_field(outcome, "changed_pages", "clean artifact audit") == [1, 2], "DEFECT [clean artifact audit]: without a baseline, every PDF page must be selected for rendering"


def test_artifact_traversal_error_cannot_silently_yield_a_partial_ok_inventory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    root, build, _expected = artifacts(tmp_path)
    loaded = audit_module()
    assert loaded is not None
    original_walk = loaded.os.walk

    def controlled_walk(path, *args, **kwargs):
        if Path(path).resolve() == build.resolve():
            onerror = kwargs.get("onerror")
            if onerror is not None:
                onerror(PermissionError(13, "controlled traversal denial", str(build / "unreadable")))
        yield from original_walk(path, *args, **kwargs)

    monkeypatch.setattr(loaded.os, "walk", controlled_walk)
    outcome = loaded.audit_build(
        repo_root=root,
        build_dir=build,
        source_revision=git(root, "rev-parse", "HEAD"),
        command_record=build / "commands.json",
        test_fixture=True,
    )
    assert outcome.ok is False
    assert "controlled traversal denial" in diagnostic_text(outcome)


@pytest.mark.parametrize(
    "kind, log, diagnostic_field",
    [
        ("undefined_reference", "LaTeX Warning: Reference `missing' undefined.\n", "undefined_references"),
        ("undefined_citation", "LaTeX Warning: Citation `missing' undefined.\n", "undefined_citations"),
        ("rerun", "LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right.\n", "rerun_requests"),
        ("fatal", "! Emergency stop.\n", "fatal_errors"),
        ("overfull", "Overfull \\hbox (2.0pt too wide)\n", "overfull_boxes"),
        ("question_marks", "output ??\n", "literal_double_question_marks"),
        ("invalid_status", "STATUS: NOT_A_STATUS\n", "invalid_status_tags"),
    ],
)
def test_each_real_bad_log_fixture_populates_its_named_diagnostic(tmp_path: Path, kind: str, log: str, diagnostic_field: str):
    root, build, _ = artifacts(tmp_path, log)
    outcome = run_audit(root, build, f"{kind} log fixture")
    assert require_field(outcome, "ok", f"{kind} log fixture") is False, f"DEFECT [{kind} log fixture]: audit accepted real bad log"
    assert require_field(outcome, diagnostic_field, f"{kind} log fixture"), f"DEFECT [{kind} log fixture]: audit failed without populating {diagnostic_field}"


@pytest.mark.parametrize(
    "kind, diagnostic_field, token",
    [
        ("missing_pdf", "errors", "main.pdf"),
        ("missing_aux", "errors", "main.aux"),
        ("duplicate_label", "duplicate_labels", "one"),
        ("failed_command", "errors", "pdflatex"),
        ("wrong_command_order", "errors", "command"),
        ("fabricated_metadata", "errors", "main.pdf"),
        ("stale_aux", "stale_auxiliary_files", "stale.aux"),
    ],
)
def test_bad_artifact_state_populates_its_named_diagnostic(tmp_path: Path, kind: str, diagnostic_field: str, token: str):
    root, build, _ = artifacts(tmp_path)
    if kind == "missing_pdf":
        (build / "main.pdf").unlink()
    elif kind == "missing_aux":
        (build / "main.aux").unlink()
    elif kind == "duplicate_label":
        (build / "main.aux").write_text("\\newlabel{one}{{1}{1}}\n\\newlabel{one}{{2}{2}}\n", encoding="utf-8")
    elif kind == "failed_command":
        commands = json.loads((build / "commands.json").read_text(encoding="utf-8"))
        commands[-1]["returncode"] = 1
        (build / "commands.json").write_text(json.dumps(commands), encoding="utf-8")
    elif kind == "wrong_command_order":
        commands = json.loads((build / "commands.json").read_text(encoding="utf-8"))
        commands[0], commands[1] = commands[1], commands[0]
        (build / "commands.json").write_text(json.dumps(commands), encoding="utf-8")
    elif kind == "fabricated_metadata":
        (build / "main.pdf").write_bytes(b"not a PDF")
        (build / "main.pdf.metadata.json").write_text(json.dumps({"page_count": 1, "sha256": "fabricated"}), encoding="utf-8")
    else:
        (build / "stale.aux").write_text("stale\n", encoding="utf-8")
    outcome = run_audit(root, build, f"{kind} artifact fixture")
    assert require_field(outcome, "ok", f"{kind} artifact fixture") is False, f"DEFECT [{kind} artifact fixture]: audit accepted bad artifact state"
    diagnostic = require_field(outcome, diagnostic_field, f"{kind} artifact fixture")
    assert token in diagnostic_text(diagnostic), f"DEFECT [{kind} artifact fixture]: {diagnostic_field} did not name {token}"


def driver_fixture(tmp_path: Path) -> dict[str, object]:
    """Create a committed driver plus controlled Python and batch-tool doubles."""

    tmp_path.mkdir(parents=True, exist_ok=True)
    repo = tmp_path / "driver-repo"
    source = repo / "manuscripts" / "gauge_vfe_rg"
    verification = source / "verification"
    tools = tmp_path / "driver-tools"
    python_poison = tmp_path / "python-poison"
    python_site_marker = tmp_path / "python-sitecustomize-imported.txt"
    mutation_marker = tmp_path / "mutate-auditor.flag"
    source_mutation_marker = tmp_path / "mutate-source-swap-restore.flag"
    style_mutation_marker = tmp_path / "mutate-style-swap-restore.flag"
    trace = tmp_path / "driver-trace.txt"
    verification_mode_file = tmp_path / "verification-mode.txt"
    audit_mode_file = tmp_path / "audit-mode.txt"
    external_mode_file = tmp_path / "external-mode.txt"
    pdflatex_count_file = tmp_path / "pdflatex-count.txt"
    external_root = tmp_path / "external-inputs"
    external_a = external_root / "external-a.sty"
    external_b = external_root / "external-b.sty"
    decoy_references = tmp_path / "references.bib"
    verification_mode_file.write_text("good", encoding="utf-8")
    audit_mode_file.write_text("good", encoding="utf-8")
    external_mode_file.write_text("stable", encoding="utf-8")
    verification.mkdir(parents=True)
    tools.mkdir()
    python_poison.mkdir()
    external_root.mkdir()
    external_a.write_text("external A\n", encoding="utf-8")
    external_b.write_text("external B\n", encoding="utf-8")
    for index in range(1, 17):
        (external_root / f"nonconvergent-{index}.sty").write_text(
            f"external nonconvergent {index}\n",
            encoding="utf-8",
        )
    (python_poison / "sitecustomize.py").write_text(
        "from pathlib import Path\n"
        f"Path({str(python_site_marker)!r}).write_text('IMPORTED', encoding='utf-8')\n",
        encoding="utf-8",
    )
    script = source / "build.ps1"
    main_tex = source / "main.tex"
    runner = verification / "run_checks.py"
    auditor = verification / "build_audit.py"
    references = source.parent / "references.bib"
    result = verification / "result.json"
    script.write_bytes(BUILD_SCRIPT_PATH.read_bytes())
    main_tex.write_bytes((BUILD_SCRIPT_PATH.parent / "main.tex").read_bytes())
    references.write_text(
        "% REPOSITORY_BIBLIOGRAPHY_WITNESS\n@misc{x, title={X}}\n",
        encoding="utf-8",
        newline="\n",
    )
    decoy_references.write_text(
        "% ATTACKER_OUTPUT_PARENT_BIBLIOGRAPHY\n@misc{x, title={Attacker}}\n",
        encoding="utf-8",
        newline="\n",
    )
    runner_source = '''import hashlib
import json
import os
import pathlib
import sys

trace = pathlib.Path(r"__DRIVER_TRACE__")
with trace.open("a", encoding="utf-8") as stream:
    stream.write(
        "run_checks "
        + " ".join(sys.argv[1:])
        + f" GIT_DIR={os.environ.get('GIT_DIR', '')}"
        + f" GIT_WORK_TREE={os.environ.get('GIT_WORK_TREE', '')}"
        + f" GIT_OBJECT_DIRECTORY={os.environ.get('GIT_OBJECT_DIRECTORY', '')}\\n"
    )
result_path = pathlib.Path(sys.argv[sys.argv.index("--verify") + 1]).resolve()
report_path = pathlib.Path(sys.argv[sys.argv.index("--report") + 1])
result = json.loads(result_path.read_text(encoding="utf-8"))
digest = hashlib.sha256(result_path.read_bytes()).hexdigest()
report = {
    "ok": True,
    "protocol_profile": "gauge-vfe-rg-production-v1",
    "python_executable": r"C:\\Python314\\python.exe",
    "python_executable_sha256": hashlib.sha256(pathlib.Path(r"C:\\Python314\\python.exe").read_bytes()).hexdigest(),
    "git_executable": r"C:\\Program Files\\Git\\cmd\\git.exe",
    "git_executable_sha256": hashlib.sha256(pathlib.Path(r"C:\\Program Files\\Git\\cmd\\git.exe").read_bytes()).hexdigest(),
    "result_path": str(result_path),
    "source_revision": result["source_revision"],
    "head_revision": result["source_revision"],
    "input_sha256_before": digest,
    "input_sha256_after": digest,
    "input_unchanged": True,
    "semantic_payload_digest": "1" * 64,
    "manifest_path_count": len(result["manifest"]["bound_inputs"]),
    "check_count": 1,
    "issues": [],
}
mode = pathlib.Path(r"__VERIFICATION_MODE_FILE__").read_text(encoding="utf-8").strip()
if mode == "malformed":
    payload = "{malformed"
elif mode == "duplicate":
    payload = (
        '{"ok":true,"ok":false,"source_revision":"'
        + result["source_revision"]
        + '"}'
    )
elif mode == "minimal":
    payload = json.dumps(
        {"ok": True, "source_revision": result["source_revision"]},
        sort_keys=True,
        separators=(",", ":"),
    )
elif mode == "noncanonical":
    payload = json.dumps(report, sort_keys=False)
else:
    if mode == "ok_false":
        report["ok"] = False
        report["issues"] = [{"code": "CONTROLLED", "message": "fixture rejection"}]
    elif mode == "bad_head":
        report["head_revision"] = "f" * 40
    payload = json.dumps(report, sort_keys=True, separators=(",", ":"))
report_path.write_text(payload, encoding="utf-8", newline="")
sys.stdout.buffer.write((payload + "\\n").encode("utf-8"))
if mode == "forged_substitution":
    forged = {**report, "semantic_payload_digest": "2" * 64}
    report_path.write_text(
        json.dumps(forged, sort_keys=True, separators=(",", ":")),
        encoding="utf-8",
        newline="",
    )
if mode == "inject_git_metadata":
    metadata = pathlib.Path(__file__).resolve().parents[3] / ".git" / "info" / "grafts"
    metadata.parent.mkdir(parents=True, exist_ok=True)
    metadata.write_text("controlled late graft\\n", encoding="utf-8")
raise SystemExit(19 if mode == "ok_true_nonzero" else 0)
'''
    runner.write_text(
        runner_source.replace("__DRIVER_TRACE__", str(trace)).replace(
            "__VERIFICATION_MODE_FILE__", str(verification_mode_file)
        ),
        encoding="utf-8",
        newline="\n",
    )
    auditor_source = '''import hashlib
import importlib.metadata
import csv
import json
import os
import pathlib
import subprocess
import sys

trace = pathlib.Path(r"__DRIVER_TRACE__")
with trace.open("a", encoding="utf-8") as stream:
    stream.write("build_audit " + " ".join(sys.argv[1:]) + "\\n")
def argument(name):
    return pathlib.Path(sys.argv[sys.argv.index(name) + 1])
build = argument("--build-dir").resolve()
revision = sys.argv[sys.argv.index("--source-revision") + 1]
output = argument("--output")
context = json.loads((build / "build-context.json").read_text(encoding="utf-8"))
commands = json.loads((build / "commands.json").read_text(encoding="utf-8"))
pdf_hash = hashlib.sha256((build / "main.pdf").read_bytes()).hexdigest()
pypdf_site = pathlib.Path(r"C:\\Users\\chris and christine\\AppData\\Roaming\\Python\\Python314\\site-packages").resolve()
pypdf_root = (pypdf_site / "pypdf").resolve()
pypdf_init = (pypdf_root / "__init__.py").resolve()
pypdf_distributions = [
    distribution
    for distribution in importlib.metadata.distributions(path=[str(pypdf_site)])
    if (distribution.metadata.get("Name") or "").casefold() == "pypdf"
]
assert len(pypdf_distributions) == 1
pypdf_distribution = pypdf_distributions[0]
pypdf_records = [
    pathlib.Path(pypdf_distribution.locate_file(entry)).resolve()
    for entry in (pypdf_distribution.files or ())
    if pathlib.PurePosixPath(str(entry).replace("\\\\", "/")).name == "RECORD"
]
assert len(pypdf_records) == 1
pypdf_record = pypdf_records[0]
pypdf_files = []
with pypdf_record.open("r", encoding="utf-8", newline="") as stream:
    pypdf_record_rows = list(csv.reader(stream))
for raw_path, _declared_hash, _declared_size in pypdf_record_rows:
    candidate = pypdf_site.joinpath(*raw_path.split("/"))
    payload = candidate.read_bytes()
    pypdf_files.append(
        {
            "path": raw_path,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "byte_count": len(payload),
        }
    )
pypdf_files.sort(key=lambda entry: entry["path"])
pypdf_tree_sha256 = hashlib.sha256(
    json.dumps(pypdf_files, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
).hexdigest()
pypdf_pycache_prefix = (build / ".tex-tmp" / "fake-audit-pycache").resolve()
pypdf_pycache_prefix.mkdir()
report = {
    "ok": True,
    "protocol_profile": "gauge-vfe-rg-production-v1",
    "source_revision": revision,
    "errors": [],
    "tool_versions": {"pdflatex": "fixture", "bibtex": "fixture"},
    "inspection_tool_versions": {
        "pypdf": pypdf_distribution.version,
        "pypdf_module_path": str(pypdf_init),
        "pypdf_module_sha256": hashlib.sha256(pypdf_init.read_bytes()).hexdigest(),
        "pypdf_package_root": str(pypdf_root),
        "pypdf_package_tree_sha256": pypdf_tree_sha256,
        "pypdf_package_file_count": len(pypdf_files),
        "pypdf_distribution_root": str(pypdf_record.parent),
        "pypdf_record_path": str(pypdf_record),
        "pypdf_record_sha256": hashlib.sha256(pypdf_record.read_bytes()).hexdigest(),
        "pypdf_pycache_prefix": str(pypdf_pycache_prefix),
    },
    "commands": commands,
    "build_context": context,
    "input_inventory": {
        "repository": {"manuscripts/gauge_vfe_rg/main.tex": {"sha256": "2" * 64, "byte_count": 1}},
        "build": {"main.aux": {"sha256": "3" * 64, "byte_count": 1}},
        "external": {"C:\\\\fixture.sty": {"sha256": "4" * 64, "byte_count": 1}},
    },
    "source_manifest_digest": "5" * 64,
    "pdf_sha256": pdf_hash,
    "pdf_byte_count": (build / "main.pdf").stat().st_size,
    "page_count": 1,
    "pdf_metadata": {"title": "fixture"},
    "artifact_hashes": {"main.pdf": pdf_hash},
    "pages_to_render": [1],
    "changed_pages": [1],
    "duplicate_labels": [],
    "undefined_references": [],
    "undefined_citations": [],
    "rerun_requests": [],
    "fatal_errors": [],
    "overfull_boxes": [],
    "literal_double_question_marks": [],
    "invalid_status_tags": [],
    "doubled_status_tags": [],
    "stale_auxiliary_files": [],
}
mode = pathlib.Path(r"__AUDIT_MODE_FILE__").read_text(encoding="utf-8").strip()
if mode == "malformed":
    payload = b"{malformed\\n"
elif mode == "duplicate":
    payload = (
        '{"ok":true,"ok":false,"source_revision":"' + revision + '"}\\n'
    ).encode("utf-8")
elif mode == "minimal":
    payload = (
        json.dumps(
            {"ok": True, "source_revision": revision},
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\\n"
    ).encode("utf-8")
else:
    if mode == "ok_false":
        report["ok"] = False
        report["errors"] = ["controlled audit finding"]
    elif mode == "bad_pypdf_tree":
        report["inspection_tool_versions"]["pypdf_package_tree_sha256"] = "0" * 64
    payload = (
        json.dumps(report, sort_keys=True, separators=(",", ":")) + "\\n"
    ).encode("utf-8")
output.write_bytes(payload)
published_digest = hashlib.sha256(payload).hexdigest()
sys.stdout.buffer.write(f"BUILD_AUDIT_SHA256={published_digest}\\n".encode("ascii"))
if mode == "forged_substitution":
    forged = dict(report)
    forged["pdf_metadata"] = {**report["pdf_metadata"], "title": "FORGED VALID SUBSTITUTE"}
    output.write_bytes(
        (json.dumps(forged, sort_keys=True, separators=(",", ":")) + "\\n").encode("utf-8")
    )
if mode == "advance_head_after_report":
    repository = argument("--repo-root").resolve()
    trusted_git = pathlib.Path(r"C:\\Program Files\\Git\\cmd\\git.exe")
    def git_command(*arguments):
        completed = subprocess.run(
            [str(trusted_git), "--no-replace-objects", "-C", str(repository), *arguments],
            text=True,
            capture_output=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
        return completed.stdout.strip()
    prior_head = git_command("rev-parse", "HEAD^{commit}")
    tree = git_command("rev-parse", f"{prior_head}^{{tree}}")
    next_head = git_command(
        "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
        "commit-tree", tree, "-p", prior_head, "-m", "post-audit handoff advance",
    )
    git_command("update-ref", "HEAD", next_head, prior_head)
raise SystemExit(23 if mode == "ok_true_nonzero" else 0)
'''
    auditor.write_text(
        auditor_source.replace("__DRIVER_TRACE__", str(trace)).replace(
            "__AUDIT_MODE_FILE__", str(audit_mode_file)
        ),
        encoding="utf-8",
        newline="\n",
    )
    git(repo, "init")
    git(repo, "config", "core.autocrlf", "false")
    revision = commit(repo, "driver source")
    manifest_bound_inputs = {
        path.relative_to(repo).as_posix(): {
            "byte_count": len(payload := path.read_bytes()),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }
        for path in (script, main_tex, runner, auditor, references)
    }
    result.write_text(
        json.dumps(
            {
                "protocol_profile": PRODUCTION_PROFILE,
                "source_revision": revision,
                "overall_status": "PASS",
                "manifest": {
                    "hash_algorithm": "SHA-256",
                    "hash_domain": "raw file bytes",
                    "path_semantics": "repository-relative POSIX paths",
                    "bound_inputs": manifest_bound_inputs,
                },
            }
        ),
        encoding="utf-8",
    )

    bootstrap_temporary_directory = tmp_path / "bootstrap-child"
    bootstrap_temporary_directory.mkdir()
    executed_build_script = bootstrap_temporary_directory / "build.ps1"
    executed_build_script.write_bytes(script.read_bytes())
    source_blob_oid = git(
        repo,
        "rev-parse",
        f"{revision}:manuscripts/gauge_vfe_rg/build.ps1",
    )
    bootstrap_attestation = bootstrap_temporary_directory / "bootstrap-attestation.json"
    bootstrap_attestation.write_text(
        json.dumps(
            {
                "protocol_profile": PRODUCTION_PROFILE,
                "source_revision": revision,
                "repository_root": str(repo.resolve()),
                "source_directory": str(source.resolve()),
                "repository_build_script": str(script.resolve()),
                "executed_build_script": str(executed_build_script.resolve()),
                "source_blob_oid": source_blob_oid,
                "source_blob_byte_count": len(executed_build_script.read_bytes()),
                "source_sha256": hashlib.sha256(executed_build_script.read_bytes()).hexdigest(),
                "bootstrap_temporary_directory": str(bootstrap_temporary_directory.resolve()),
                "bootstrap_parent_pid": os.getpid(),
                "powershell_path": str(
                    Path(r"C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe")
                ),
                "git_path": str(TRUSTED_GIT),
            }
        ),
        encoding="utf-8",
    )

    pdflatex = tools / "pdflatex.cmd"
    bibtex = tools / "bibtex.cmd"
    bibtex_style = tools / "plainnat.bst"
    fake_git = tools / "git.cmd"
    bibtex_style.write_text("ENTRY{}{}{}\n", encoding="utf-8")
    pdflatex.write_text(
        "\r\n".join(
            [
                "@echo off",
                "setlocal EnableDelayedExpansion",
                "set PDFLATEX_COUNT=0",
                f'if exist "{pdflatex_count_file}" set /p PDFLATEX_COUNT=<"{pdflatex_count_file}"',
                "set /a PDFLATEX_COUNT+=1",
                f'>"{pdflatex_count_file}" echo !PDFLATEX_COUNT!',
                "set EXTERNAL_MODE=stable",
                f'if exist "{external_mode_file}" set /p EXTERNAL_MODE=<"{external_mode_file}"',
                "set /a PDFLATEX_POSITION=((PDFLATEX_COUNT-1)%%3)+1",
                "set /a DISCOVERY_ITERATION=((PDFLATEX_COUNT-1)/3)+1",
                f'>>"{trace}" echo pdflatex %*',
                f'>>"{trace}" echo TEXINPUTS=%TEXINPUTS%',
                f'>>"{trace}" echo TEXINPUTS.pdflatex=%TEXINPUTS.pdflatex%',
                f'>>"{trace}" echo TEXINPUTS_pdflatex=%TEXINPUTS_pdflatex%',
                f'>>"{trace}" echo BIBINPUTS=%BIBINPUTS%',
                f'>>"{trace}" echo BSTINPUTS=%BSTINPUTS%',
                f'>>"{trace}" echo TEXMFHOME=%TEXMFHOME%',
                f'>>"{trace}" echo TEXMFVAR=%TEXMFVAR%',
                f'>>"{trace}" echo TEXMFCONFIG=%TEXMFCONFIG%',
                f'>>"{trace}" echo KPSE_DOT=%KPSE_DOT%',
                f'>>"{trace}" echo TEXFONTMAPS=%TEXFONTMAPS%',
                f'>>"{trace}" echo OFMFONTS=%OFMFONTS%',
                f'>>"{trace}" echo TEXPICTS=%TEXPICTS%',
                f'>>"{trace}" echo PDFTEXCONFIG=%PDFTEXCONFIG%',
                f'>>"{trace}" echo GLYPHFONTS=%GLYPHFONTS%',
                f'>>"{trace}" echo MAKETEX_MODE=%MAKETEX_MODE%',
                f'>>"{trace}" echo WEB2C=%WEB2C%',
                f'>>"{trace}" echo USERPROFILE=%USERPROFILE%',
                f'>>"{trace}" echo PYTHONPATH=%PYTHONPATH%',
                f'>>"{trace}" echo TEMP=%TEMP%',
                f'>>"{trace}" echo GIT_DIR=%GIT_DIR%',
                ">main.pdf echo fake pdf",
                ">main.log echo Output written on main.pdf (1 page, 11 bytes).",
                f'findstr /L /C:"\\bibliography{{references}}" "{main_tex.resolve()}" >nul || exit /b 93',
                ">main.aux echo \\bibstyle{plainnat}",
                ">>main.aux echo \\bibdata{references}",
                ">main.toc echo contents",
                ">main.fls echo PWD %CD%",
                f'>>main.fls echo INPUT {main_tex.resolve()}',
                f'if /I "!EXTERNAL_MODE!"=="stable" >>main.fls echo INPUT {external_a.resolve()}',
                f'if /I "!EXTERNAL_MODE!"=="swap_restore" >>main.fls echo INPUT {external_a.resolve()}',
                f'if /I "!EXTERNAL_MODE!"=="first_final" if "!PDFLATEX_POSITION!"=="1" >>main.fls echo INPUT {external_a.resolve()}',
                f'if /I "!EXTERNAL_MODE!"=="first_final" if "!PDFLATEX_POSITION!"=="3" >>main.fls echo INPUT {external_b.resolve()}',
                f'if /I "!EXTERNAL_MODE!"=="evidence_new" if /I "%CD%"=="{(tmp_path / "driver-build").resolve()}" >>main.fls echo INPUT {external_b.resolve()}',
                f'if /I "!EXTERNAL_MODE!"=="evidence_new" if /I not "%CD%"=="{(tmp_path / "driver-build").resolve()}" >>main.fls echo INPUT {external_a.resolve()}',
                f'if /I "!EXTERNAL_MODE!"=="nonconvergent" >>main.fls echo INPUT {external_root.resolve()}\\nonconvergent-!DISCOVERY_ITERATION!.sty',
                'if exist "main.bbl" >>main.fls echo INPUT %CD%\\main.bbl',
                "set SWAPPED_EXTERNAL=",
                f'if /I "!EXTERNAL_MODE!"=="swap_restore" if !PDFLATEX_COUNT! GEQ 4 move /y "{external_a.resolve()}" "{external_a.resolve()}.saved" >nul 2>nul',
                f'if exist "{external_a.resolve()}.saved" set SWAPPED_EXTERNAL=1',
                f'if exist "{external_a.resolve()}.saved" >"{external_a.resolve()}" echo ATTACKER EXTERNAL',
                f'if exist "{external_a.resolve()}.saved" move /y "{external_a.resolve()}.saved" "{external_a.resolve()}" >nul 2>nul',
                "set SWAPPED_PROVENANCE=",
                'if /I "!EXTERNAL_MODE!"=="recorder_swap_restore" if "!PDFLATEX_POSITION!"=="2" move /y "main-pass-1.fls" "main-pass-1.fls.saved" >nul 2>nul',
                'if exist "main-pass-1.fls.saved" set SWAPPED_PROVENANCE=1',
                'if exist "main-pass-1.fls.saved" >"main-pass-1.fls" echo ATTACKER RECORDER',
                'if exist "main-pass-1.fls.saved" move /y "main-pass-1.fls.saved" "main-pass-1.fls" >nul 2>nul',
                'if /I "!EXTERNAL_MODE!"=="bibtex_provenance_swap_restore" if "!PDFLATEX_POSITION!"=="2" move /y "main-bibtex.aux" "main-bibtex.aux.saved" >nul 2>nul',
                'if exist "main-bibtex.aux.saved" set SWAPPED_PROVENANCE=1',
                'if exist "main-bibtex.aux.saved" >"main-bibtex.aux" echo ATTACKER AUX',
                'if exist "main-bibtex.aux.saved" move /y "main-bibtex.aux.saved" "main-bibtex.aux" >nul 2>nul',
                'if /I "!EXTERNAL_MODE!"=="bibtex_provenance_swap_restore" if "!PDFLATEX_POSITION!"=="2" move /y "main-bibtex.blg" "main-bibtex.blg.saved" >nul 2>nul',
                'if exist "main-bibtex.blg.saved" set SWAPPED_PROVENANCE=1',
                'if exist "main-bibtex.blg.saved" >"main-bibtex.blg" echo ATTACKER BLG',
                'if exist "main-bibtex.blg.saved" move /y "main-bibtex.blg.saved" "main-bibtex.blg" >nul 2>nul',
                'if /I "!EXTERNAL_MODE!"=="bbl_swap_restore" if !PDFLATEX_POSITION! GEQ 2 move /y "main.bbl" "main.bbl.saved" >nul 2>nul',
                'if exist "main.bbl.saved" set SWAPPED_PROVENANCE=1',
                'if exist "main.bbl.saved" >"main.bbl" echo ATTACKER BBL',
                'if exist "main.bbl.saved" move /y "main.bbl.saved" "main.bbl" >nul 2>nul',
                f'if exist "{source_mutation_marker}" move /y "{main_tex.resolve()}" "{main_tex.resolve()}.saved" >nul 2>nul',
                f'if exist "{main_tex.resolve()}.saved" >"{main_tex.resolve()}" echo ATTACKER SOURCE',
                f'if exist "{main_tex.resolve()}.saved" move /y "{main_tex.resolve()}.saved" "{main_tex.resolve()}" >nul 2>nul',
                f'if exist "{main_tex.resolve()}.saved" exit /b 98',
                f'if exist "{mutation_marker}" >"{auditor}" echo raise SystemExit(99)',
                "if defined SWAPPED_EXTERNAL exit /b 96",
                "if defined SWAPPED_PROVENANCE exit /b 95",
                "exit /b 0",
                "",
            ]
        ),
        encoding="ascii",
    )
    bibtex.write_text(
        "\r\n".join(
            [
                "@echo off",
                f'>>"{trace}" echo bibtex %*',
                "set EXTERNAL_MODE=stable",
                f'if exist "{external_mode_file}" set /p EXTERNAL_MODE=<"{external_mode_file}"',
                "set SWAPPED_BIBTEX_AUX=",
                'if /I "%EXTERNAL_MODE%"=="bibtex_aux_swap_restore" move /y "main.aux" "main.aux.saved" >nul 2>nul',
                'if exist "main.aux.saved" set SWAPPED_BIBTEX_AUX=1',
                'if exist "main.aux.saved" >"main.aux" echo ATTACKER AUX',
                'if exist "main.aux.saved" move /y "main.aux.saved" "main.aux" >nul 2>nul',
                f'if exist "{style_mutation_marker}" move /y "{bibtex_style}" "{bibtex_style}.saved" >nul 2>nul',
                f'if exist "{bibtex_style}.saved" >"{bibtex_style}" echo ATTACKER STYLE',
                f'if exist "{bibtex_style}.saved" move /y "{bibtex_style}.saved" "{bibtex_style}" >nul 2>nul',
                f'if exist "{bibtex_style}.saved" exit /b 97',
                "if defined SWAPPED_BIBTEX_AUX exit /b 94",
                f'if /I not "%BIBINPUTS%"=="{source.parent.resolve()}" exit /b 93',
                'findstr /L /C:"REPOSITORY_BIBLIOGRAPHY_WITNESS" "%BIBINPUTS%\\references.bib" >nul || exit /b 92',
                ">main.bbl echo REPOSITORY_BIBLIOGRAPHY_WITNESS",
                ">main.blg echo The style file: plainnat.bst",
                ">>main.blg echo Database file #1: references.bib",
                "exit /b 0",
                "",
            ]
        ),
        encoding="ascii",
    )
    fake_git.write_text(
        f'@echo off\r\n>>"{trace}" echo PATH_GIT_INVOKED %*\r\nexit /b 91\r\n',
        encoding="ascii",
    )
    return {
        "repo": repo,
        "source": source,
        "script": script,
        "runner": runner,
        "auditor": auditor,
        "result": result,
        "revision": revision,
        "tools": tools,
        "python_poison": python_poison,
        "python_site_marker": python_site_marker,
        "mutation_marker": mutation_marker,
        "source_mutation_marker": source_mutation_marker,
        "style_mutation_marker": style_mutation_marker,
        "verification_mode_file": verification_mode_file,
        "audit_mode_file": audit_mode_file,
        "external_mode_file": external_mode_file,
        "pdflatex_count_file": pdflatex_count_file,
        "external_a": external_a,
        "external_b": external_b,
        "decoy_references": decoy_references,
        "external_root": external_root,
        "bootstrap_temporary_directory": bootstrap_temporary_directory,
        "executed_build_script": executed_build_script,
        "bootstrap_attestation": bootstrap_attestation,
        "pdflatex": pdflatex,
        "bibtex": bibtex,
        "bibtex_style": bibtex_style,
        "trace": trace,
        "build": tmp_path / "driver-build",
        "verification_report": tmp_path / "driver-verification-report.json",
        "audit": tmp_path / "driver-audit.json",
    }


def test_kpathsea_scrub_declaration_covers_installed_help_formats_fixture():
    runtime_variables = {
        variable
        for group in re.findall(r"\[variables: ([^\]]+)\]", KPATHSEA_HELP_FORMATS_SAMPLE)
        for variable in group.split()
    }
    script = BUILD_SCRIPT_PATH.read_text(encoding="utf-8")
    declaration = re.search(
        r"\$directVariables\s*=\s*@\((.*?)\n\s*\)\n\s*foreach \(\$baseName",
        script,
        flags=re.DOTALL,
    )
    assert declaration is not None
    declared = set(re.findall(r"'([A-Z0-9_]+)'", declaration.group(1)))
    controlled = {"TEXINPUTS", "BIBINPUTS", "BSTINPUTS"}
    prefix_closed = {
        variable
        for variable in runtime_variables
        if variable.startswith(("TEXMF", "KPSE_", "SELFAUTO"))
    }
    missing = runtime_variables - declared - controlled - prefix_closed
    assert not missing, f"Kpathsea help-formats variables missing from scrub policy: {sorted(missing)}"
    assert {"VARTEXFONTS", "MAKETEX_MODE"} <= declared
    assert "Get-ChildItem -Path Env:" not in script
    assert "GetEnvironmentVariables" not in script
    assert "SetEnvironmentVariable" not in script
    assert "EnvironmentVariables.Clear()" in script
    assert "Invoke-ExplicitChildProcess" in script


def run_driver(
    fixture: dict[str, object],
    *,
    source_revision: str | None = None,
    verification_mode: str = "good",
    audit_mode: str = "good",
    external_mode: str = "stable",
    extra_arguments: tuple[str, ...] = (),
    extra_build_environment: dict[str, str] | None = None,
    polluted: bool = False,
    mutate_auditor: bool = False,
    mutate_source_swap_restore: bool = False,
    mutate_style_swap_restore: bool = False,
) -> subprocess.CompletedProcess[str]:
    fixture["verification_mode_file"].write_text(verification_mode, encoding="utf-8")
    fixture["audit_mode_file"].write_text(audit_mode, encoding="utf-8")
    fixture["external_mode_file"].write_text(external_mode, encoding="utf-8")
    selected_revision = source_revision or str(fixture["revision"])
    attestation = json.loads(fixture["bootstrap_attestation"].read_text(encoding="utf-8"))
    attestation["source_revision"] = selected_revision
    attestation["source_blob_oid"] = git(
        fixture["repo"],
        "rev-parse",
        f"{selected_revision}:manuscripts/gauge_vfe_rg/build.ps1",
    )
    fixture["bootstrap_attestation"].write_text(
        json.dumps(attestation),
        encoding="utf-8",
    )
    environment = dict(os.environ)
    environment.update(
        {
            "PATH": f"{fixture['tools']}{os.pathsep}{environment.get('PATH', '')}",
            "DRIVER_TRACE": str(fixture["trace"]),
            "FAKE_VERIFICATION_MODE": verification_mode,
            "FAKE_AUDIT_MODE": audit_mode,
            "PYTHONPATH": str(fixture["python_poison"]),
            "PYTHON_SITE_SENTINEL": str(fixture["python_site_marker"]),
            "TEXINPUTS": "CALLER_TEX_SENTINEL",
            "TEXINPUTS.pdflatex": "CALLER_DOT_PROGRAM_SENTINEL",
            "TEXINPUTS_pdflatex": "CALLER_UNDERSCORE_PROGRAM_SENTINEL",
            "BIBINPUTS": "CALLER_BIB_SENTINEL",
            "BSTINPUTS": "CALLER_BST_SENTINEL",
            "TEXMFHOME": "CALLER_TEXMF_SENTINEL",
            "KPSE_DOT": "CALLER_KPSE_SENTINEL",
            "texmfhome": "CALLER_LOWER_TEXMF_SENTINEL",
            "texfontmaps": "CALLER_FONTMAP_SENTINEL",
            "OFMFONTS": "CALLER_OFM_SENTINEL",
            "TEXPICTS": "CALLER_TEXPICTS_SENTINEL",
            "pDfTeXcOnFiG": "CALLER_PDFTEX_SENTINEL",
            "glyphfonts": "CALLER_GLYPH_SENTINEL",
            "MAKETEX_MODE": "CALLER_MAKETEX_SENTINEL",
            "web2c": "CALLER_WEB2C_SENTINEL",
            "USERPROFILE": str(fixture["python_poison"]),
        }
    )
    if mutate_auditor:
        fixture["mutation_marker"].write_text("mutate\n", encoding="utf-8")
    if mutate_source_swap_restore:
        fixture["source_mutation_marker"].write_text("mutate\n", encoding="utf-8")
    if mutate_style_swap_restore:
        fixture["style_mutation_marker"].write_text("mutate\n", encoding="utf-8")
    if polluted:
        environment.update(
            {
                "GIT_DIR": "CALLER_GIT_DIR_SENTINEL",
                "GIT_WORK_TREE": "CALLER_GIT_WORK_TREE_SENTINEL",
                "GIT_OBJECT_DIRECTORY": "CALLER_GIT_OBJECT_SENTINEL",
            }
        )
    powershell = Path(r"C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe")
    build_environment = {
        "GAUGE_VFE_BUILD_REPOSITORY_ROOT": str(fixture["repo"]),
        "GAUGE_VFE_BUILD_SOURCE_DIRECTORY": str(fixture["source"]),
        "GAUGE_VFE_BUILD_REPOSITORY_BUILD_SCRIPT": str(fixture["script"]),
        "GAUGE_VFE_BUILD_EXECUTED_BUILD_SCRIPT": str(fixture["executed_build_script"]),
        "GAUGE_VFE_BUILD_BOOTSTRAP_ATTESTATION_PATH": str(fixture["bootstrap_attestation"]),
        "GAUGE_VFE_BUILD_OUTPUT_DIRECTORY": str(fixture["build"]),
        "GAUGE_VFE_BUILD_AUDIT_PATH": str(fixture["audit"]),
        "GAUGE_VFE_BUILD_SOURCE_REVISION": selected_revision,
        "GAUGE_VFE_BUILD_VERIFICATION_RESULT": str(fixture["result"]),
        "GAUGE_VFE_BUILD_VERIFICATION_REPORT": str(fixture["verification_report"]),
        "GAUGE_VFE_BUILD_PDFLATEX_PATH": str(fixture["pdflatex"]),
        "GAUGE_VFE_BUILD_BIBTEX_PATH": str(fixture["bibtex"]),
        "GAUGE_VFE_BUILD_BIBTEX_STYLE_PATH": str(fixture["bibtex_style"]),
    }
    if extra_build_environment:
        build_environment.update(extra_build_environment)
    environment.update(build_environment)
    encoded_script = __import__("base64").b64encode(
        fixture["executed_build_script"].read_bytes()
    ).decode("ascii")
    environment_arguments = " ".join(
        f"$env:{name}" for name in build_environment if name in {
            "GAUGE_VFE_BUILD_REPOSITORY_ROOT",
            "GAUGE_VFE_BUILD_SOURCE_DIRECTORY",
            "GAUGE_VFE_BUILD_REPOSITORY_BUILD_SCRIPT",
            "GAUGE_VFE_BUILD_EXECUTED_BUILD_SCRIPT",
            "GAUGE_VFE_BUILD_BOOTSTRAP_ATTESTATION_PATH",
            "GAUGE_VFE_BUILD_OUTPUT_DIRECTORY",
            "GAUGE_VFE_BUILD_AUDIT_PATH",
            "GAUGE_VFE_BUILD_SOURCE_REVISION",
            "GAUGE_VFE_BUILD_VERIFICATION_RESULT",
            "GAUGE_VFE_BUILD_VERIFICATION_REPORT",
            "GAUGE_VFE_BUILD_PDFLATEX_PATH",
            "GAUGE_VFE_BUILD_BIBTEX_PATH",
            "GAUGE_VFE_BUILD_BIBTEX_STYLE_PATH",
        }
    )
    quoted_extra = " ".join("'" + value.replace("'", "''") + "'" for value in extra_arguments)
    transport = (
        "& ([ScriptBlock]::Create([Text.UTF8Encoding]::new($false,$true).GetString("
        f"[Convert]::FromBase64String('{encoded_script}')))) {environment_arguments}"
        + (f" {quoted_extra}" if quoted_extra else "")
        + "\n"
    )
    return subprocess.run(
        [
            str(powershell),
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            "-",
        ],
        cwd=fixture["repo"],
        env=environment,
        input=transport,
        text=True,
        capture_output=True,
        check=False,
    )


def test_build_driver_uses_fixed_python_git_and_controlled_tex_environment(tmp_path: Path):
    fixture = driver_fixture(tmp_path)
    before = fixture["result"].read_bytes()
    completed = run_driver(fixture, polluted=True)
    diagnostics = (completed.stdout + completed.stderr).lower()
    trace = fixture["trace"].read_text(encoding="utf-8") if fixture["trace"].is_file() else ""
    assert completed.returncode == 0, diagnostics
    assert not fixture["python_site_marker"].exists(), "caller PYTHONPATH sitecustomize was imported"
    assert fixture["result"].read_bytes() == before
    assert "PATH_GIT_INVOKED" not in trace
    assert "CALLER_GIT_" not in trace
    assert not any(
        sentinel in trace
        for sentinel in (
            "CALLER_TEX_SENTINEL",
            "CALLER_DOT_PROGRAM_SENTINEL",
            "CALLER_UNDERSCORE_PROGRAM_SENTINEL",
            "CALLER_BIB_SENTINEL",
            "CALLER_BST_SENTINEL",
            "CALLER_TEXMF_SENTINEL",
            "CALLER_KPSE_SENTINEL",
            "CALLER_LOWER_TEXMF_SENTINEL",
            "CALLER_FONTMAP_SENTINEL",
            "CALLER_OFM_SENTINEL",
            "CALLER_TEXPICTS_SENTINEL",
            "CALLER_PDFTEX_SENTINEL",
            "CALLER_GLYPH_SENTINEL",
            "CALLER_MAKETEX_SENTINEL",
            "CALLER_WEB2C_SENTINEL",
        )
    )
    assert f"USERPROFILE={fixture['python_poison']}" not in trace
    assert "PYTHONPATH=\n" in trace
    assert f"TEMP={(fixture['build'] / '.tex-tmp').resolve()}" in trace
    context = json.loads((fixture["build"] / "build-context.json").read_text(encoding="utf-8"))
    assert context["protocol_profile"] == PRODUCTION_PROFILE
    assert context["source_revision"] == fixture["revision"] == context["head_revision"]
    assert context["python_executable"]["path"] == str(TRUSTED_PYTHON)
    assert context["git_executable"]["path"] == str(TRUSTED_GIT)
    assert set(context["controlled_environment"]) == {
        "TEXINPUTS",
        "BIBINPUTS",
        "BSTINPUTS",
        "TEXMFHOME",
        "TEXMFVAR",
        "TEXMFCONFIG",
        "SOURCE_DATE_EPOCH",
    }
    assert context["controlled_environment"]["TEXINPUTS"].endswith(";")
    assert context["controlled_environment"]["BIBINPUTS"] == str(
        fixture["source"].resolve().parent
    )
    assert context["controlled_environment"]["BSTINPUTS"] == str(
        fixture["bibtex_style"].resolve().parent
    )
    assert context["controlled_environment"]["TEXMFHOME"] == str(
        (fixture["build"] / ".texmf-home").resolve()
    )
    assert context["controlled_environment"]["TEXMFVAR"] == str(
        (fixture["build"] / ".texmf-var").resolve()
    )
    assert context["controlled_environment"]["TEXMFCONFIG"] == str(
        (fixture["build"] / ".texmf-config").resolve()
    )
    assert all(
        (fixture["build"] / name).is_dir()
        for name in (".texmf-home", ".texmf-var", ".texmf-config")
    )
    labels = [line.split(" ", 1)[0] for line in trace.splitlines() if line.startswith(("run_checks ", "pdflatex ", "bibtex ", "build_audit "))]
    assert labels == ["run_checks", *(["pdflatex", "bibtex", "pdflatex", "pdflatex"] * 3), "build_audit"]
    commands = json.loads((fixture["build"] / "commands.json").read_text(encoding="utf-8"))
    assert all(command["cwd"] == str(fixture["build"].resolve()) for command in commands)
    expected_environment_keys = {
        "SystemRoot",
        "WINDIR",
        "SystemDrive",
        "COMSPEC",
        "PATHEXT",
        "PATH",
        "TEMP",
        "TMP",
        "TEXINPUTS",
        "BIBINPUTS",
        "BSTINPUTS",
        "TEXMFHOME",
        "TEXMFVAR",
        "TEXMFCONFIG",
        "SOURCE_DATE_EPOCH",
    }
    assert all(set(command["environment"]) == expected_environment_keys for command in commands)
    assert all(
        not any("CALLER_" in str(value) for value in command["environment"].values())
        for command in commands
    )
    assert commands[0]["argv"][1:] == [
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        "-recorder",
        "-no-shell-escape",
        str((fixture["source"] / "main.tex").resolve()),
    ]
    assert context["external_input_fixed_point"]["converged_iteration"] == 2
    assert str(fixture["external_a"].resolve()) in context["external_input_fixed_point"]["inputs"]
    assert set(context["recorder_snapshots"]) == {"pass_1", "pass_3", "pass_4"}
    assert set(context["evidence_input_inventory"]) == {"repository", "build", "external"}
    assert context["evidence_input_inventory"]["build"]["main-bibtex.bbl"] == {
        "sha256": hashlib.sha256(
            (fixture["build"] / "main-bibtex.bbl").read_bytes()
        ).hexdigest(),
        "byte_count": (fixture["build"] / "main-bibtex.bbl").stat().st_size,
    }
    assert context["repository_build_script"]["path"] == str(fixture["script"].resolve())
    assert context["executed_build_script"]["path"] == str(
        fixture["executed_build_script"].resolve()
    )
    assert context["bootstrap_attestation"]["path"] == str(
        fixture["bootstrap_attestation"].resolve()
    )
    stdout_lines = [line for line in completed.stdout.splitlines() if line]
    assert len(stdout_lines) == 2
    assert re.fullmatch(r"BUILD_AUDIT_SHA256=[0-9a-f]{64}", stdout_lines[0])
    assert re.fullmatch(r"BUILD_VERIFICATION_REPORT_SHA256=[0-9a-f]{64}", stdout_lines[1])


def test_build_driver_output_parent_bibliography_decoy_cannot_be_consumed_or_admitted(
    tmp_path: Path,
):
    fixture = driver_fixture(tmp_path)
    completed = run_driver(fixture)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert (fixture["build"] / "main-bibtex.bbl").read_text(encoding="utf-8").strip() == (
        "REPOSITORY_BIBLIOGRAPHY_WITNESS"
    )
    context = json.loads((fixture["build"] / "build-context.json").read_text(encoding="utf-8"))
    repository_key = "manuscripts/references.bib"
    repository_payload = (fixture["source"].parent / "references.bib").read_bytes()
    assert context["evidence_input_inventory"]["repository"][repository_key] == {
        "sha256": hashlib.sha256(repository_payload).hexdigest(),
        "byte_count": len(repository_payload),
    }
    decoy = str(fixture["decoy_references"].resolve())
    assert decoy not in context["evidence_input_inventory"]["external"]
    assert decoy not in context["external_input_fixed_point"]["inputs"]


def test_build_driver_reaches_monotone_external_input_fixed_point_before_evidence(
    tmp_path: Path,
):
    fixture = driver_fixture(tmp_path)
    completed = run_driver(fixture, external_mode="stable")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    context = json.loads((fixture["build"] / "build-context.json").read_text(encoding="utf-8"))
    fixed_point = context["external_input_fixed_point"]
    assert fixed_point["max_iterations"] == 8
    assert fixed_point["converged_iteration"] == 2
    assert str(fixture["external_a"].resolve()) in fixed_point["inputs"]
    assert not any(
        entry.name.startswith("gauge-vfe-discovery-")
        for entry in fixture["bootstrap_temporary_directory"].iterdir()
    )


def test_build_driver_denies_external_input_swap_restore_after_discovery_lock(
    tmp_path: Path,
):
    fixture = driver_fixture(tmp_path)
    before = fixture["external_a"].read_bytes()
    completed = run_driver(fixture, external_mode="swap_restore")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert fixture["external_a"].read_bytes() == before
    assert not fixture["external_a"].with_name(
        f"{fixture['external_a'].name}.saved"
    ).exists()


@pytest.mark.parametrize(
    "external_mode,snapshot_names",
    [
        ("recorder_swap_restore", ("main-pass-1.fls",)),
        ("bibtex_aux_swap_restore", ("main.aux",)),
        ("bibtex_provenance_swap_restore", ("main-bibtex.aux", "main-bibtex.blg")),
        ("bbl_swap_restore", ("main.bbl",)),
    ],
)
def test_build_driver_denies_recorder_and_bibtex_provenance_swap_restore(
    tmp_path: Path,
    external_mode: str,
    snapshot_names: tuple[str, ...],
):
    fixture = driver_fixture(tmp_path)
    completed = run_driver(fixture, external_mode=external_mode)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    for snapshot_name in snapshot_names:
        assert not (fixture["build"] / f"{snapshot_name}.saved").exists()


def test_build_driver_rejects_new_external_input_introduced_only_during_evidence(
    tmp_path: Path,
):
    fixture = driver_fixture(tmp_path)
    completed = run_driver(fixture, external_mode="evidence_new")
    diagnostics = (completed.stdout + completed.stderr).lower()
    assert completed.returncode != 0
    assert "outside the locked fixed-point envelope" in diagnostics
    trace = fixture["trace"].read_text(encoding="utf-8")
    assert not any(line.startswith("build_audit ") for line in trace.splitlines())


def test_build_driver_rejects_external_input_discovery_nonconvergence(tmp_path: Path):
    fixture = driver_fixture(tmp_path)
    completed = run_driver(fixture, external_mode="nonconvergent")
    diagnostics = (completed.stdout + completed.stderr).lower()
    assert completed.returncode != 0
    assert "did not converge within 8 iterations" in diagnostics
    assert not fixture["build"].exists() or not any(fixture["build"].iterdir())


def test_build_driver_unions_first_and_final_pdftex_pass_external_inputs(tmp_path: Path):
    fixture = driver_fixture(tmp_path)
    completed = run_driver(fixture, external_mode="first_final")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    context = json.loads((fixture["build"] / "build-context.json").read_text(encoding="utf-8"))
    external = context["evidence_input_inventory"]["external"]
    assert str(fixture["external_a"].resolve()) in external
    assert str(fixture["external_b"].resolve()) in external
    pass_one = Path(context["recorder_snapshots"]["pass_1"]["path"])
    pass_four = Path(context["recorder_snapshots"]["pass_4"]["path"])
    assert str(fixture["external_a"].resolve()) in pass_one.read_text(encoding="utf-8")
    assert str(fixture["external_b"].resolve()) in pass_four.read_text(encoding="utf-8")


def test_build_driver_disables_shell_escape_on_every_pdftex_pass(tmp_path: Path):
    fixture = driver_fixture(tmp_path)
    completed = run_driver(fixture)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    pdflatex_lines = [
        line
        for line in fixture["trace"].read_text(encoding="utf-8").splitlines()
        if line.startswith("pdflatex ")
    ]
    assert len(pdflatex_lines) == 9
    assert all(line.count("-no-shell-escape") == 1 for line in pdflatex_lines)


def test_build_driver_rejects_manifest_consistent_crlf_worktree_bytes_not_in_revision(
    tmp_path: Path,
):
    fixture = driver_fixture(tmp_path)
    main_tex = fixture["source"] / "main.tex"
    crlf_bytes = main_tex.read_bytes().replace(b"\n", b"\r\n")
    main_tex.write_bytes(crlf_bytes)
    result = json.loads(fixture["result"].read_text(encoding="utf-8"))
    manifest_entry = result["manifest"]["bound_inputs"][
        "manuscripts/gauge_vfe_rg/main.tex"
    ]
    manifest_entry["sha256"] = hashlib.sha256(crlf_bytes).hexdigest()
    manifest_entry["byte_count"] = len(crlf_bytes)
    fixture["result"].write_text(json.dumps(result), encoding="utf-8")

    completed = run_driver(fixture)
    diagnostics = (completed.stdout + completed.stderr).lower()
    assert completed.returncode != 0
    assert "raw worktree bytes are not bound to source revision" in diagnostics
    assert "manuscripts/gauge_vfe_rg/main.tex" in diagnostics


def test_build_driver_requires_in_memory_launch_and_exact_build_environment_schema(
    tmp_path: Path,
):
    body = BUILD_SCRIPT_PATH.read_text(encoding="utf-8")
    assert "Open-ExecutableLaunchLock -Path $ExecutedBuildScript" not in body
    assert not re.search(r"hash-object[^\n]+\$ExecutedBuildScript", body)
    ps_command_path_uses = list(re.finditer(r"\$PSCommandPath\b", body))
    assert len(ps_command_path_uses) == 1
    assert re.search(
        r"if \(\$PSCommandPath\)\s*\{\s*throw 'Authenticated in-memory child unexpectedly has PSCommandPath\.'\s*\}",
        body,
    )
    fixture = driver_fixture(tmp_path)
    polluted = run_driver(
        fixture,
        extra_build_environment={"GAUGE_VFE_BUILD_UNEXPECTED": "forbidden"},
    )
    assert polluted.returncode != 0
    assert "exact gauge_vfe_build_ environment schema" in (
        polluted.stdout + polluted.stderr
    ).lower()
    assert not fixture["trace"].exists()

    fixture = driver_fixture(tmp_path / "direct-file")
    powershell = Path(r"C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe")
    direct = subprocess.run(
        [
            str(powershell),
            "-NoProfile",
            "-NonInteractive",
            "-File",
            str(fixture["script"]),
            str(fixture["repo"]),
            str(fixture["source"]),
            str(fixture["script"]),
            str(fixture["executed_build_script"]),
            str(fixture["bootstrap_attestation"]),
            str(fixture["build"]),
            str(fixture["audit"]),
            str(fixture["revision"]),
            str(fixture["result"]),
            str(fixture["verification_report"]),
            str(fixture["pdflatex"]),
            str(fixture["bibtex"]),
            str(fixture["bibtex_style"]),
        ],
        cwd=fixture["repo"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert direct.returncode != 0
    assert "authenticated in-memory child unexpectedly has pscommandpath" in (
        direct.stdout + direct.stderr
    ).lower()


def test_build_driver_rejects_removed_python_path_parameter(tmp_path: Path):
    fixture = driver_fixture(tmp_path)
    completed = run_driver(
        fixture,
        extra_arguments=("-PythonPath", str(fixture["tools"] / "python.cmd")),
    )
    assert completed.returncode != 0
    assert "pythonpath" in (completed.stdout + completed.stderr).lower()
    assert not fixture["trace"].exists()


@pytest.mark.parametrize(
    "mode, token",
    [
        ("ok_false", "did not report ok=true"),
        ("ok_true_nonzero", "process failed with exit code 19"),
        ("malformed", "jsondecodeerror"),
        ("duplicate", "duplicate json object key"),
        ("minimal", "exact required property set"),
        ("noncanonical", "not canonical compact sorted strict json"),
        ("bad_head", "head_revision"),
    ],
)
def test_build_driver_distinguishes_invalid_verification_report_states(
    tmp_path: Path,
    mode: str,
    token: str,
):
    fixture = driver_fixture(tmp_path)
    completed = run_driver(fixture, verification_mode=mode)
    diagnostics = (completed.stdout + completed.stderr).lower()
    assert completed.returncode != 0
    assert token in diagnostics
    trace = fixture["trace"].read_text(encoding="utf-8") if fixture["trace"].is_file() else ""
    assert not any(line.startswith(("pdflatex ", "bibtex ", "build_audit ")) for line in trace.splitlines())
    if mode == "ok_false":
        report = json.loads(fixture["verification_report"].read_text(encoding="utf-8"))
        assert report["source_revision"] == fixture["revision"]


def test_build_driver_rejects_valid_verification_report_substituted_after_stdout(
    tmp_path: Path,
):
    fixture = driver_fixture(tmp_path)
    completed = run_driver(fixture, verification_mode="forged_substitution")
    diagnostics = (completed.stdout + completed.stderr).lower()
    assert completed.returncode != 0
    assert "verification report stdout does not equal retained verificationreport bytes" in diagnostics
    forged = json.loads(fixture["verification_report"].read_text(encoding="utf-8"))
    assert forged["ok"] is True
    assert forged["semantic_payload_digest"] == "2" * 64


@pytest.mark.parametrize(
    "mode, token",
    [
        ("ok_false", "did not report ok=true"),
        ("ok_true_nonzero", "process failed with exit code 23"),
        ("malformed", "jsondecodeerror"),
        ("duplicate", "duplicate json object key"),
        ("minimal", "exact required property set"),
        ("bad_pypdf_tree", "tree digest"),
    ],
)
def test_build_driver_distinguishes_invalid_audit_report_states(
    tmp_path: Path,
    mode: str,
    token: str,
):
    fixture = driver_fixture(tmp_path)
    completed = run_driver(fixture, audit_mode=mode)
    assert completed.returncode != 0
    assert token in (completed.stdout + completed.stderr).lower()


def test_build_driver_rejects_valid_audit_report_substituted_after_digest_publication(
    tmp_path: Path,
):
    fixture = driver_fixture(tmp_path)
    completed = run_driver(fixture, audit_mode="forged_substitution")
    diagnostics = (completed.stdout + completed.stderr).lower()
    assert completed.returncode != 0
    assert "published build audit digest does not equal retained auditpath bytes" in diagnostics
    forged = json.loads(fixture["audit"].read_text(encoding="utf-8"))
    assert forged["ok"] is True
    assert forged["pdf_metadata"]["title"] == "FORGED VALID SUBSTITUTE"


def test_build_driver_rejects_head_advance_after_audit_report(tmp_path: Path):
    fixture = driver_fixture(tmp_path)
    completed = run_driver(fixture, audit_mode="advance_head_after_report")
    assert completed.returncode != 0
    assert "head changed" in (completed.stdout + completed.stderr).lower()


def test_build_driver_rejects_source_script_mutation_before_any_execution(tmp_path: Path):
    fixture = driver_fixture(tmp_path)
    fixture["runner"].write_text("raise SystemExit(0)\n", encoding="utf-8")
    completed = run_driver(fixture)
    assert completed.returncode != 0
    assert "manifest entry disagrees with held-handle m0 bytes" in (
        completed.stdout + completed.stderr
    ).lower()
    assert not fixture["trace"].exists()


def test_build_driver_rejects_git_metadata_injected_after_numerical_verification(tmp_path: Path):
    fixture = driver_fixture(tmp_path)
    completed = run_driver(fixture, verification_mode="inject_git_metadata")
    assert completed.returncode != 0
    assert "info/grafts" in (completed.stdout + completed.stderr).lower()
    trace = fixture["trace"].read_text(encoding="utf-8")
    assert not any(line.startswith(("pdflatex ", "bibtex ", "build_audit ")) for line in trace.splitlines())


def test_build_driver_rebinds_auditor_after_tex_before_executing_it(tmp_path: Path):
    fixture = driver_fixture(tmp_path)
    before = fixture["auditor"].read_bytes()
    completed = run_driver(fixture, mutate_auditor=True)
    assert completed.returncode == 0, (completed.stdout + completed.stderr).lower()
    assert fixture["auditor"].read_bytes() == before
    trace = fixture["trace"].read_text(encoding="utf-8")
    assert any(line.startswith("pdflatex ") for line in trace.splitlines())
    assert any(line.startswith("build_audit ") for line in trace.splitlines())


def test_build_driver_denies_repository_source_swap_and_restore_during_tex(tmp_path: Path):
    fixture = driver_fixture(tmp_path)
    source = fixture["source"] / "main.tex"
    before = source.read_bytes()
    completed = run_driver(fixture, mutate_source_swap_restore=True)
    assert completed.returncode == 0, (completed.stdout + completed.stderr).lower()
    assert source.read_bytes() == before
    assert not source.with_name(f"{source.name}.saved").exists()


def test_build_driver_denies_bibtex_style_swap_and_restore_during_bibtex(tmp_path: Path):
    fixture = driver_fixture(tmp_path)
    style = fixture["bibtex_style"]
    before = style.read_bytes()
    completed = run_driver(fixture, mutate_style_swap_restore=True)
    assert completed.returncode == 0, (completed.stdout + completed.stderr).lower()
    assert style.read_bytes() == before
    assert not style.with_name(f"{style.name}.saved").exists()


def test_build_driver_rejects_crlf_change_outside_exact_raw_manifest(tmp_path: Path):
    fixture = driver_fixture(tmp_path)
    runner_bytes = fixture["runner"].read_bytes()
    assert b"\r" not in runner_bytes
    fixture["runner"].write_bytes(runner_bytes.replace(b"\n", b"\r\n"))
    completed = run_driver(fixture)
    assert completed.returncode != 0
    assert "manifest entry disagrees with held-handle m0 bytes" in (
        completed.stdout + completed.stderr
    ).lower()
    assert not fixture["trace"].exists()


def test_build_driver_rejects_finite_side_chain_source_revision(tmp_path: Path):
    fixture = driver_fixture(tmp_path)
    tree = git(fixture["repo"], "rev-parse", f"{fixture['revision']}^{{tree}}")
    side_revision = git(
        fixture["repo"],
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit-tree",
        tree,
        "-m",
        "finite side chain",
    )
    result = json.loads(fixture["result"].read_text(encoding="utf-8"))
    result["source_revision"] = side_revision
    fixture["result"].write_text(json.dumps(result), encoding="utf-8")
    completed = run_driver(fixture, source_revision=side_revision)
    assert completed.returncode != 0
    assert "ancestry" in (completed.stdout + completed.stderr).lower()
    assert not fixture["trace"].exists()
