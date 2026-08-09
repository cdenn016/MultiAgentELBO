"""Fail-closed Git lifecycle checks for the gauge-VFE RG release.

The release history is split into source (``S``), evidence (``E``), closure
(``C``), and wiki (``W``) revisions.  This module validates those revisions
using Git object bytes rather than console-formatted paths.
"""

from __future__ import annotations

import hashlib
import ctypes
from ctypes import wintypes
import os
import re
import stat
import subprocess
from collections.abc import Callable
from contextvars import ContextVar, Token
from pathlib import Path
from typing import Any, NamedTuple


_FULL_COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")
_RENAME_COPY_RE = re.compile(r"([RC])(0|[1-9][0-9]{0,2})\Z")
_SINGLE_PATH_STATUSES = frozenset({"A", "M", "D", "T"})
_REGULAR_BLOB_MODES = frozenset({"100644", "100755"})

_DERIVATION_ROOT = "docs/derivations/2026-08-03-gauge-vfe-rg-remediation"
_PRODUCTION_MARKERS = frozenset(
    {
        "docs/superpowers/plans/2026-08-03-gauge-vfe-rg-review-remediation.md",
        "manuscripts/gauge_vfe_rg/SPEC.md",
        "manuscripts/gauge_vfe_rg/verification/claims.json",
    }
)
_CURRENT_RESULT = "manuscripts/gauge_vfe_rg/verification/current-results.json"
_TRACKED_PDF = "manuscripts/gauge_vfe_rg/main.pdf"
_TASK_CONTROL_EXACT = frozenset(
    {
        "docs/superpowers/plans/2026-08-03-gauge-vfe-rg-review-remediation.md",
        "docs/superpowers/specs/2026-08-03-gauge-vfe-rg-review-remediation-design.md",
    }
)
_TASK_CONTROL_PREFIX = ".superpowers/sdd/2026-08-03-gauge-vfe-rg-review-remediation/"
_CONTROLLED_GIT_METADATA_PATHS = (
    "info/grafts",
    "shallow",
    "objects/info/alternates",
    "objects/info/http-alternates",
)
_FIXED_GIT_EXECUTABLE = Path(r"C:\Program Files\Git\cmd\git.exe")
_PRODUCTION_PROTOCOL_PROFILE = "gauge-vfe-rg-production-v1"
_SYNTHETIC_PROTOCOL_PROFILE = "synthetic-test-fixture-v1"
_ACTIVE_GIT_IDENTITY: ContextVar[dict[str, Any] | None] = ContextVar(
    "gauge_vfe_rg_lifecycle_git_identity",
    default=None,
)
_ACTIVE_GIT_GUARD: ContextVar[Any | None] = ContextVar(
    "gauge_vfe_rg_lifecycle_git_guard",
    default=None,
)

_SOURCE_TO_EVIDENCE_EXACT = frozenset(
    {
        _CURRENT_RESULT,
        _TRACKED_PDF,
        f"{_DERIVATION_ROOT}/construction-or-strongest-theorem.md",
        f"{_DERIVATION_ROOT}/counterexample-register.md",
        f"{_DERIVATION_ROOT}/adversarial-report.json",
    }
)
_SOURCE_TO_EVIDENCE_SYNTHETIC = frozenset(
    {
        _CURRENT_RESULT,
        "docs/derivations/evidence/numerics.json",
    }
)
_EVIDENCE_TO_CLOSURE_EXACT = frozenset(
    {
        f"{_DERIVATION_ROOT}/release.json",
        f"{_DERIVATION_ROOT}/final-report.md",
        "docs/reviews/2026-08-03-gauge-vfe-rg-remediation-closure-attestation.md",
        "docs/reviews/2026-08-03-gauge-vfe-rg-remediation-verification-ledger.json",
    }
)
_EVIDENCE_TO_CLOSURE_SYNTHETIC = frozenset(
    {
        "docs/derivations/closure-attestation.json",
        "docs/derivations/release.json",
    }
)
_CLOSURE_TO_WIKI_EXACT = frozenset(
    {
        "sources/manuscripts/gauge-vfe-rg-cross-scale-operator-theory-2026-08-03.md",
        "wiki/projects/Gauge-Theoretic Multi-Agent VFE Model.md",
        "wiki/concepts/Coarse Graining.md",
        "wiki/concepts/Renormalization group flow.md",
        "wiki/concepts/Renormalization-group flow of beliefs.md",
        "index.md",
        "log.md",
    }
)
_PRODUCTION_MANDATORY_PATHS = frozenset(
    {
        "manuscripts/gauge_vfe_rg/main.tex",
        "manuscripts/gauge_vfe_rg/01_introduction.tex",
        "manuscripts/gauge_vfe_rg/02_geometry.tex",
        "manuscripts/gauge_vfe_rg/03_probability.tex",
        "manuscripts/gauge_vfe_rg/04_generative.tex",
        "manuscripts/gauge_vfe_rg/05_elbo.tex",
        "manuscripts/gauge_vfe_rg/05a_expfamily.tex",
        "manuscripts/gauge_vfe_rg/05b_local_collective_elbo.tex",
        "manuscripts/gauge_vfe_rg/05c_pullback_geometry.tex",
        "manuscripts/gauge_vfe_rg/05d_relational_inference.tex",
        "manuscripts/gauge_vfe_rg/06_general_coarsegraining.tex",
        "manuscripts/gauge_vfe_rg/06_gaussian.tex",
        "manuscripts/gauge_vfe_rg/06a_generative_gaussian.tex",
        "manuscripts/gauge_vfe_rg/07_general_renormalization.tex",
        "manuscripts/gauge_vfe_rg/07_restrictions.tex",
        "manuscripts/gauge_vfe_rg/07b_agent_network_rg.tex",
        "manuscripts/gauge_vfe_rg/08_infogeometry.tex",
        "manuscripts/gauge_vfe_rg/09_coarsegraining.tex",
        "manuscripts/gauge_vfe_rg/10_renormalization.tex",
        "manuscripts/gauge_vfe_rg/11_obstructions.tex",
        "manuscripts/gauge_vfe_rg/12_philosophy.tex",
        "manuscripts/gauge_vfe_rg/appendix_claim_ledger.tex",
        "manuscripts/gauge_vfe_rg/appendix_notation.tex",
        "manuscripts/gauge_vfe_rg/appendix_numerical_provenance.tex",
        "manuscripts/gauge_vfe_rg/SPEC.md",
        "manuscripts/gauge_vfe_rg/build.ps1",
        "manuscripts/references.bib",
        "manuscripts/scientific_report.sty",
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
        "manuscripts/gauge_vfe_rg/verification/tests/test_factorization_gap.py",
        "manuscripts/gauge_vfe_rg/verification/tests/test_runner_cli.py",
        "manuscripts/gauge_vfe_rg/verification/tests/test_manifest_binding.py",
        "manuscripts/gauge_vfe_rg/verification/tests/test_lifecycle_gate.py",
        "manuscripts/gauge_vfe_rg/verification/tests/test_build_audit.py",
        "manuscripts/gauge_vfe_rg/verification/tests/test_build_bootstrap.py",
        "docs/superpowers/plans/2026-08-03-gauge-vfe-rg-review-remediation.md",
        "docs/superpowers/specs/2026-08-03-gauge-vfe-rg-review-remediation-design.md",
    }
)


class DiffEntry(NamedTuple):
    """One immutable ``git diff --name-status -z`` record."""

    status: str
    paths: tuple[str, ...]


class _TreeEntry(NamedTuple):
    """One immutable recursive ``git ls-tree -rz`` record."""

    mode: str
    object_type: str
    oid: str
    path: str


class GateReport(NamedTuple):
    """Immutable machine-readable result returned by a lifecycle gate."""

    ok: bool
    errors: tuple[str, ...] = ()
    revisions: tuple[tuple[str, str], ...] = ()
    changes: tuple[tuple[str, tuple[DiffEntry, ...]], ...] = ()
    protocol_profile: str = _PRODUCTION_PROTOCOL_PROFILE
    head_revision: str | None = None
    git_executable: str = str(_FIXED_GIT_EXECUTABLE)
    git_executable_sha256: str | None = None

    @property
    def findings(self) -> tuple[str, ...]:
        """Return errors under the terminology used by audit consumers."""

        return self.errors

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable representation of the report."""

        return {
            "ok": self.ok,
            "errors": list(self.errors),
            "revisions": dict(self.revisions),
            "changes": {
                boundary: [
                    {"status": entry.status, "paths": list(entry.paths)}
                    for entry in entries
                ]
                for boundary, entries in self.changes
            },
            "protocol_profile": self.protocol_profile,
            "head_revision": self.head_revision,
            "git_executable": self.git_executable,
            "git_executable_sha256": self.git_executable_sha256,
        }


LifecycleReport = GateReport
PublicationIdentityReport = GateReport


class LifecycleGateError(ValueError):
    """Raised when Git output violates the lifecycle data contract."""


def _validate_repository_path(path: str) -> None:
    """Reject paths that are not safe repository-relative POSIX paths."""

    if not path:
        raise LifecycleGateError("Git path is empty")
    if path.startswith("/"):
        raise LifecycleGateError(f"Git path is absolute: {path!r}")
    if "\\" in path:
        raise LifecycleGateError(f"Git path contains a backslash: {path!r}")
    if re.match(r"[A-Za-z]:", path):
        raise LifecycleGateError(f"Git path contains a drive prefix: {path!r}")
    segments = path.split("/")
    if any(segment in {"", ".", ".."} for segment in segments):
        raise LifecycleGateError(f"Git path contains an unsafe segment: {path!r}")


def _validate_casefold_collisions(paths: tuple[str, ...]) -> None:
    """Reject distinct path spellings that alias under Windows case folding."""

    seen: dict[str, str] = {}
    for path in paths:
        folded = path.casefold()
        previous = seen.get(folded)
        if previous is not None and previous != path:
            raise LifecycleGateError(
                f"case-fold path collision: {previous!r} and {path!r}"
            )
        seen[folded] = path


def parse_name_status_z(raw: bytes) -> tuple[DiffEntry, ...]:
    """Parse exact NUL-delimited Git name-status output.

    Args:
        raw: Bytes emitted by ``git diff --name-status -z``.

    Returns:
        An immutable tuple of immutable diff entries.

    Raises:
        LifecycleGateError: If the byte stream, status, or path is malformed.
        TypeError: If ``raw`` is not bytes.
    """

    if not isinstance(raw, bytes):
        raise TypeError("name-status input must be bytes")
    if raw == b"":
        return ()
    if not raw.endswith(b"\0"):
        raise LifecycleGateError("name-status output is not NUL terminated")

    fields = raw[:-1].split(b"\0")
    if any(field == b"" for field in fields):
        raise LifecycleGateError("name-status output contains an empty field")

    entries: list[DiffEntry] = []
    observed_paths: list[str] = []
    index = 0
    while index < len(fields):
        try:
            status = fields[index].decode("ascii", errors="strict")
        except UnicodeDecodeError as exc:
            raise LifecycleGateError("diff status is not strict ASCII") from exc
        index += 1

        if status in _SINGLE_PATH_STATUSES:
            path_count = 1
        else:
            match = _RENAME_COPY_RE.fullmatch(status)
            if match is None or int(match.group(2)) > 100:
                raise LifecycleGateError(f"unsupported diff status: {status!r}")
            path_count = 2

        if index + path_count > len(fields):
            raise LifecycleGateError(f"truncated diff record for status {status!r}")

        decoded_paths: list[str] = []
        for field in fields[index : index + path_count]:
            try:
                path = field.decode("utf-8", errors="strict")
            except UnicodeDecodeError as exc:
                raise LifecycleGateError("diff path is not strict UTF-8") from exc
            _validate_repository_path(path)
            decoded_paths.append(path)
            observed_paths.append(path)
        index += path_count
        entries.append(DiffEntry(status=status, paths=tuple(decoded_paths)))

    _validate_casefold_collisions(tuple(observed_paths))
    return tuple(entries)


def _is_link_or_reparse(path: Path) -> bool:
    """Return whether ``path`` itself is a symlink, junction, or reparse point."""

    try:
        metadata = path.lstat()
    except OSError:
        return False
    attributes = getattr(metadata, "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    return stat.S_ISLNK(metadata.st_mode) or bool(attributes & reparse_flag)


def _stat_identity(metadata: os.stat_result) -> tuple[int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _stable_regular_file_bytes(path: Path, role: str) -> bytes:
    """Read one path through a handle bound to pre/post filesystem identity."""

    try:
        path_before = path.lstat()
    except FileNotFoundError:
        raise
    except OSError as exc:
        raise LifecycleGateError(f"cannot inspect {role} safely: {exc}") from exc
    try:
        if not stat.S_ISREG(path_before.st_mode) or _is_link_or_reparse(path):
            raise LifecycleGateError(f"{role} is not a regular non-reparse file")
        with path.open("rb") as handle:
            handle_before = os.fstat(handle.fileno())
            if (
                handle_before.st_dev,
                handle_before.st_ino,
                handle_before.st_size,
                handle_before.st_mtime_ns,
            ) != (
                path_before.st_dev,
                path_before.st_ino,
                path_before.st_size,
                path_before.st_mtime_ns,
            ):
                raise LifecycleGateError(
                    f"{role} opened handle does not match its path identity"
                )
            payload = handle.read()
            handle_after = os.fstat(handle.fileno())
        path_after = path.lstat()
    except LifecycleGateError:
        raise
    except OSError as exc:
        raise LifecycleGateError(f"cannot read {role} safely: {exc}") from exc
    if (
        _stat_identity(handle_before) != _stat_identity(handle_after)
        or _stat_identity(path_before) != _stat_identity(path_after)
        or len(payload) != path_before.st_size
    ):
        raise LifecycleGateError(f"{role} changed while it was read")
    return payload


class _ByHandleFileInformation(ctypes.Structure):
    """Windows ``BY_HANDLE_FILE_INFORMATION`` layout."""

    _fields_ = [
        ("attributes", wintypes.DWORD),
        ("creation", wintypes.FILETIME),
        ("access", wintypes.FILETIME),
        ("write", wintypes.FILETIME),
        ("volume", wintypes.DWORD),
        ("size_high", wintypes.DWORD),
        ("size_low", wintypes.DWORD),
        ("links", wintypes.DWORD),
        ("index_high", wintypes.DWORD),
        ("index_low", wintypes.DWORD),
    ]


class _WindowsGitGuard:
    """Hold Git open with write/delete sharing denied across validation."""

    def __init__(self) -> None:
        if os.name != "nt":
            raise LifecycleGateError(
                "fixed Git launch binding requires Windows CreateFileW"
            )
        self._kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        create = self._kernel32.CreateFileW
        create.argtypes = (
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.HANDLE,
        )
        create.restype = wintypes.HANDLE
        self._handle = create(
            str(_FIXED_GIT_EXECUTABLE),
            0x80000000,
            0x00000001,
            None,
            3,
            0x00000080,
            None,
        )
        if self._handle in (None, ctypes.c_void_p(-1).value):
            raise LifecycleGateError(
                "cannot acquire deny-write/delete fixed Git guard: "
                f"WinError {ctypes.get_last_error()}"
            )
        self._closed = False

    def snapshot(self) -> dict[str, Any]:
        """Hash and identify Git through the retained Windows handle."""

        info = _ByHandleFileInformation()
        query = self._kernel32.GetFileInformationByHandle
        query.argtypes = (
            wintypes.HANDLE,
            ctypes.POINTER(_ByHandleFileInformation),
        )
        query.restype = wintypes.BOOL
        if not query(self._handle, ctypes.byref(info)):
            raise LifecycleGateError(
                f"cannot query fixed Git guard: WinError {ctypes.get_last_error()}"
            )
        seek = self._kernel32.SetFilePointerEx
        seek.argtypes = (
            wintypes.HANDLE,
            ctypes.c_longlong,
            ctypes.POINTER(ctypes.c_longlong),
            wintypes.DWORD,
        )
        seek.restype = wintypes.BOOL
        if not seek(self._handle, 0, None, 0):
            raise LifecycleGateError(
                f"cannot rewind fixed Git guard: WinError {ctypes.get_last_error()}"
            )
        read = self._kernel32.ReadFile
        read.argtypes = (
            wintypes.HANDLE,
            wintypes.LPVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
        )
        read.restype = wintypes.BOOL
        digest = hashlib.sha256()
        size = 0
        buffer = ctypes.create_string_buffer(1024 * 1024)
        while True:
            count = wintypes.DWORD()
            if not read(
                self._handle,
                buffer,
                len(buffer),
                ctypes.byref(count),
                None,
            ):
                raise LifecycleGateError(
                    f"cannot read fixed Git guard: WinError {ctypes.get_last_error()}"
                )
            if count.value == 0:
                break
            digest.update(buffer.raw[: count.value])
            size += count.value
        declared_size = (int(info.size_high) << 32) | int(info.size_low)
        if size != declared_size or int(info.attributes) & 0x10:
            raise LifecycleGateError(
                "fixed Git guard is not one stable regular-file byte stream"
            )
        return {
            "path": str(_FIXED_GIT_EXECUTABLE),
            "sha256": digest.hexdigest(),
            "byte_count": size,
            "filesystem_identity": [
                int(info.volume),
                (int(info.index_high) << 32) | int(info.index_low),
                declared_size,
                int(info.creation.dwHighDateTime) << 32
                | int(info.creation.dwLowDateTime),
                int(info.write.dwHighDateTime) << 32
                | int(info.write.dwLowDateTime),
                int(info.attributes),
            ],
        }

    def close(self) -> None:
        """Close the retained Git handle exactly once."""

        if self._closed:
            return
        close = self._kernel32.CloseHandle
        close.argtypes = (wintypes.HANDLE,)
        close.restype = wintypes.BOOL
        if not close(self._handle):
            raise LifecycleGateError(
                f"cannot close fixed Git guard: WinError {ctypes.get_last_error()}"
            )
        self._closed = True


def _fixed_git_snapshot() -> dict[str, Any]:
    """Return Git's guarded raw bytes and filesystem identity."""

    absolute = Path(os.path.abspath(os.fspath(_FIXED_GIT_EXECUTABLE)))
    parts = absolute.parts
    current = Path(parts[0])
    for part in parts[1:]:
        current /= part
        try:
            current.lstat()
        except OSError as exc:
            raise LifecycleGateError(
                f"fixed Git executable component cannot be inspected: {current}"
            ) from exc
        if _is_link_or_reparse(current):
            raise LifecycleGateError(
                f"fixed Git executable is reparse-mediated at {current}"
            )
    guard = _ACTIVE_GIT_GUARD.get()
    owned = guard is None
    if guard is None:
        guard = _WindowsGitGuard()
    try:
        return guard.snapshot()
    finally:
        if owned:
            guard.close()


def _fixed_git_identity() -> tuple[str, str]:
    """Return the closed public projection of the fixed Git snapshot."""

    snapshot = _fixed_git_snapshot()
    return snapshot["path"], snapshot["sha256"]


def _run_git(
    repo_root: Path, arguments: list[str]
) -> subprocess.CompletedProcess[bytes]:
    """Run Git in a caller-independent environment and retain exact bytes."""

    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.casefold().startswith("git_")
    }

    guard = _ACTIVE_GIT_GUARD.get()
    owned_guard = guard is None
    guard_token: Token[Any | None] | None = None
    if guard is None:
        guard = _WindowsGitGuard()
        guard_token = _ACTIVE_GIT_GUARD.set(guard)
    try:
        current_identity = _fixed_git_snapshot()
        expected_identity = _ACTIVE_GIT_IDENTITY.get()
        if expected_identity is not None and current_identity != expected_identity:
            raise LifecycleGateError(
                "fixed Git executable changed after M0: "
                f"{expected_identity!r} -> {current_identity!r}"
            )
        metadata_roots = _require_controlled_git_metadata(repo_root)
        _require_controlled_git_metadata(
            repo_root,
            expected_roots=metadata_roots,
        )

        def close_subprocess_attempt() -> None:
            postflight_errors: list[BaseException] = []
            try:
                _require_controlled_git_metadata(
                    repo_root,
                    expected_roots=metadata_roots,
                )
            except BaseException as exc:
                postflight_errors.append(exc)
            try:
                closing_identity = _fixed_git_snapshot()
                if closing_identity != current_identity:
                    raise LifecycleGateError(
                        "fixed Git executable changed across one subprocess invocation: "
                        f"{current_identity!r} -> {closing_identity!r}"
                    )
                if (
                    expected_identity is not None
                    and closing_identity != expected_identity
                ):
                    raise LifecycleGateError(
                        "fixed Git executable changed after M0: "
                        f"{expected_identity!r} -> {closing_identity!r}"
                    )
            except BaseException as exc:
                postflight_errors.append(exc)
            if len(postflight_errors) == 1:
                raise postflight_errors[0]
            if postflight_errors:
                raise LifecycleGateError(
                    "multiple Git subprocess postflight checks failed: "
                    + "; ".join(
                        f"{type(error).__name__}: {error}"
                        for error in postflight_errors
                    )
                ) from postflight_errors[0]

        try:
            completed = subprocess.run(
                [
                    str(_FIXED_GIT_EXECUTABLE),
                    "--no-replace-objects",
                    "--literal-pathspecs",
                    *arguments,
                ],
                cwd=repo_root,
                env=environment,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        except BaseException as primary_error:
            try:
                close_subprocess_attempt()
            except BaseException as postflight_error:
                raise primary_error from postflight_error
            raise
        else:
            close_subprocess_attempt()
        return completed
    finally:
        if guard_token is not None:
            _ACTIVE_GIT_GUARD.reset(guard_token)
        if owned_guard:
            guard.close()


def _git_failure(command: str, completed: subprocess.CompletedProcess[bytes]) -> str:
    """Build a deterministic diagnostic for a failed Git command."""

    detail = completed.stderr.decode("utf-8", errors="backslashreplace").strip()
    return f"{command} failed with exit {completed.returncode}: {detail or 'no stderr'}"


def _decode_git_path(
    completed: subprocess.CompletedProcess[bytes], description: str
) -> str:
    """Decode one strict, single-line path emitted by Git."""

    if completed.returncode != 0:
        raise LifecycleGateError(_git_failure(description, completed))
    try:
        emitted = completed.stdout.decode("utf-8", errors="strict").rstrip("\r\n")
    except UnicodeDecodeError as exc:
        raise LifecycleGateError(f"{description} is not strict UTF-8") from exc
    if not emitted or "\n" in emitted or "\r" in emitted:
        raise LifecycleGateError(f"Git emitted a malformed path for {description}")
    return emitted


def _lexical_absolute(repo_root: Path, emitted: str) -> Path:
    """Make a Git-emitted path absolute without following reparse components."""

    candidate = Path(emitted)
    if not candidate.is_absolute():
        candidate = repo_root / candidate
    return Path(os.path.abspath(os.fspath(candidate)))


def _git_metadata_roots(repo_root: Path) -> tuple[Path, ...]:
    """Resolve Git admin/common roots locally without recursive Git execution."""

    root = repo_root.resolve(strict=True)
    dot_git = root / ".git"
    try:
        metadata = dot_git.lstat()
    except OSError as exc:
        raise LifecycleGateError(
            f"cannot inspect Git administrative entry {dot_git}: {exc}"
        ) from exc
    if _is_link_or_reparse(dot_git):
        raise LifecycleGateError(
            f"Git administrative entry is reparse-mediated: {dot_git}"
        )
    if stat.S_ISDIR(metadata.st_mode):
        admin = dot_git
    elif stat.S_ISREG(metadata.st_mode):
        raw = _stable_regular_file_bytes(dot_git, "linked-worktree Git pointer")
        try:
            rendered = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise LifecycleGateError(
                "linked-worktree Git pointer is not strict UTF-8"
            ) from exc
        match = re.fullmatch(r"gitdir: ([^\r\n]+)\n", rendered)
        if match is None:
            raise LifecycleGateError(
                "linked-worktree Git pointer is not one strict gitdir line"
            )
        admin = _lexical_absolute(root, match.group(1))
    else:
        raise LifecycleGateError(
            f"Git administrative entry is not a directory or regular file: {dot_git}"
        )
    admin = _require_nonreparse_metadata_directory(admin, "Git admin root")

    commondir = admin / "commondir"
    try:
        common_raw = _stable_regular_file_bytes(commondir, "Git commondir pointer")
    except FileNotFoundError:
        common = admin
    else:
        try:
            common_text = common_raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise LifecycleGateError("Git commondir pointer is not strict UTF-8") from exc
        if re.fullmatch(r"[^\r\n]+\n", common_text) is None:
            raise LifecycleGateError("Git commondir pointer is not one strict path line")
        common = _lexical_absolute(admin, common_text[:-1])
        common = _require_nonreparse_metadata_directory(common, "Git common root")
    return tuple(dict.fromkeys((admin, common)))


def _resolved_git_metadata_path(
    repo_root: Path,
    relative: str,
    *,
    roots: tuple[Path, ...] | None = None,
) -> Path:
    """Return one lexical Git metadata path without following reparses."""

    active_roots = _git_metadata_roots(repo_root) if roots is None else roots
    return active_roots[-1] / Path(*relative.split("/"))


def _require_nonreparse_metadata_directory(path: Path, role: str) -> Path:
    """Require every component of one Git metadata directory to be ordinary."""

    absolute = Path(os.path.abspath(os.fspath(path)))
    current = Path(absolute.parts[0])
    for part in absolute.parts[1:]:
        current /= part
        try:
            metadata = current.lstat()
        except OSError as exc:
            raise LifecycleGateError(
                f"cannot inspect {role} component {current}: {exc}"
            ) from exc
        if _is_link_or_reparse(current) or not stat.S_ISDIR(metadata.st_mode):
            raise LifecycleGateError(
                f"{role} is reparse-mediated or non-directory at {current}"
            )
    return absolute


def _metadata_anchor(path: Path, roots: tuple[Path, ...], relative: str) -> Path:
    """Select the longest Git-admin root containing one metadata path."""

    candidates: list[Path] = []
    for root in roots:
        try:
            path.relative_to(root)
        except ValueError:
            continue
        candidates.append(root)
    if not candidates:
        raise LifecycleGateError(
            f"Git metadata path {relative!r} is outside Git admin roots: {path}"
        )
    return max(candidates, key=lambda candidate: len(candidate.parts))


def _require_nonreparse_metadata_path(
    path: Path,
    roots: tuple[Path, ...],
    relative: str,
) -> None:
    """Reject a reparse at the admin root or any existing descendant component."""

    anchor = _metadata_anchor(path, roots, relative)
    current = anchor
    paths = [anchor]
    for part in path.relative_to(anchor).parts:
        current = current / part
        paths.append(current)
    for component in paths:
        if not component.exists() and not component.is_symlink():
            break
        if _is_link_or_reparse(component):
            raise LifecycleGateError(
                f"Git metadata override {relative!r} is reparse-mediated at "
                f"{component}"
            )


def _require_controlled_git_metadata(
    repo_root: Path,
    *,
    expected_roots: tuple[Path, ...] | None = None,
) -> tuple[Path, ...]:
    """Reject local ancestry or foreign-object metadata overrides."""

    roots = _git_metadata_roots(repo_root)
    if expected_roots is not None and roots != expected_roots:
        raise LifecycleGateError(
            "Git administrative roots changed across one subprocess: "
            f"{expected_roots!r} -> {roots!r}"
        )
    for relative in _CONTROLLED_GIT_METADATA_PATHS:
        path = _resolved_git_metadata_path(repo_root, relative, roots=roots)
        _require_nonreparse_metadata_path(path, roots, relative)
        try:
            raw = _stable_regular_file_bytes(
                path,
                f"Git metadata override {relative!r}",
            )
        except FileNotFoundError:
            continue
        except LifecycleGateError:
            raise
        except OSError as exc:
            raise LifecycleGateError(
                f"Git metadata override {relative!r} cannot be inspected at {path}"
            ) from exc
        _require_nonreparse_metadata_path(path, roots, relative)
        if raw:
            raise LifecycleGateError(
                f"nonempty Git metadata override {relative!r} is forbidden: {path}"
            )
    return roots


def _resolve_commit(repo_root: Path, revision: str) -> str:
    """Resolve and validate a caller-supplied full commit object identifier."""

    if not isinstance(revision, str) or _FULL_COMMIT_RE.fullmatch(revision) is None:
        raise LifecycleGateError(f"revision is not a full 40-hex commit: {revision!r}")
    type_completed = _run_git(repo_root, ["cat-file", "-t", revision])
    if type_completed.returncode != 0:
        raise LifecycleGateError(_git_failure("git cat-file -t", type_completed))
    try:
        object_type = type_completed.stdout.decode("ascii", errors="strict").rstrip(
            "\r\n"
        )
    except UnicodeDecodeError as exc:
        raise LifecycleGateError("git cat-file emitted non-ASCII output") from exc
    if object_type != "commit":
        raise LifecycleGateError(
            f"caller revision does not name a commit object: {revision} "
            f"has type {object_type!r}"
        )
    completed = _run_git(
        repo_root,
        ["rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}"],
    )
    if completed.returncode != 0:
        raise LifecycleGateError(_git_failure("git rev-parse", completed))
    try:
        resolved = completed.stdout.decode("ascii", errors="strict").strip()
    except UnicodeDecodeError as exc:
        raise LifecycleGateError("git rev-parse emitted non-ASCII output") from exc
    if re.fullmatch(r"[0-9a-f]{40}", resolved) is None:
        raise LifecycleGateError(
            f"git rev-parse emitted an invalid commit: {resolved!r}"
        )
    if resolved != revision:
        raise LifecycleGateError(
            f"caller revision changed during commit resolution: {revision} -> {resolved}"
        )
    return resolved


def _resolve_head_commit(repo_root: Path) -> str:
    """Resolve current ``HEAD`` independently and require a real commit object."""

    completed = _run_git(
        repo_root, ["rev-parse", "--verify", "--end-of-options", "HEAD"]
    )
    if completed.returncode != 0:
        raise LifecycleGateError(_git_failure("git rev-parse HEAD", completed))
    try:
        revision = completed.stdout.decode("ascii", errors="strict").rstrip("\r\n")
    except UnicodeDecodeError as exc:
        raise LifecycleGateError("git rev-parse HEAD emitted non-ASCII output") from exc
    if _FULL_COMMIT_RE.fullmatch(revision) is None:
        raise LifecycleGateError(f"HEAD is not a full 40-hex commit: {revision!r}")
    return _resolve_commit(repo_root, revision)


def _require_repository_root(repo_root: Path) -> Path:
    """Require the caller path to resolve to Git's exact worktree root."""

    try:
        resolved_root = repo_root.resolve(strict=True)
    except OSError as exc:
        raise LifecycleGateError(
            f"repository root cannot be resolved: {repo_root!s}"
        ) from exc
    if not resolved_root.is_dir():
        raise LifecycleGateError(f"repository root is not a directory: {resolved_root}")

    completed = _run_git(resolved_root, ["rev-parse", "--show-toplevel"])
    if completed.returncode != 0:
        raise LifecycleGateError(
            _git_failure("git rev-parse --show-toplevel", completed)
        )
    try:
        top_level_text = completed.stdout.decode("utf-8", errors="strict").rstrip(
            "\r\n"
        )
    except UnicodeDecodeError as exc:
        raise LifecycleGateError("Git top-level path is not strict UTF-8") from exc
    if not top_level_text or "\n" in top_level_text or "\r" in top_level_text:
        raise LifecycleGateError("Git emitted a malformed top-level path")
    try:
        top_level = Path(top_level_text).resolve(strict=True)
    except OSError as exc:
        raise LifecycleGateError(
            f"Git top-level path cannot be resolved: {top_level_text!r}"
        ) from exc
    try:
        is_same_root = resolved_root.samefile(top_level)
    except OSError as exc:
        raise LifecycleGateError("repository-root identity check failed") from exc
    if not is_same_root:
        raise LifecycleGateError(
            f"repo_root is not the Git top level: supplied={resolved_root} git={top_level}"
        )
    return resolved_root


def _require_ancestor(repo_root: Path, older: str, newer: str, boundary: str) -> None:
    """Require ``older`` to be an ancestor of or equal to ``newer``."""

    completed = _run_git(repo_root, ["merge-base", "--is-ancestor", older, newer])
    if completed.returncode == 0:
        return
    if completed.returncode == 1:
        raise LifecycleGateError(
            f"nonmonotone lifecycle boundary {boundary}: {older} is not an ancestor of {newer}"
        )
    raise LifecycleGateError(_git_failure("git merge-base --is-ancestor", completed))


def _parse_tree_z(raw: bytes) -> dict[str, _TreeEntry]:
    """Parse recursive NUL-delimited ``git ls-tree`` output."""

    if raw == b"":
        return {}
    if not raw.endswith(b"\0"):
        raise LifecycleGateError("ls-tree output is not NUL terminated")

    entries: dict[str, _TreeEntry] = {}
    for record in raw[:-1].split(b"\0"):
        if record == b"" or b"\t" not in record:
            raise LifecycleGateError("ls-tree output contains a malformed record")
        metadata, path_bytes = record.split(b"\t", 1)
        parts = metadata.split(b" ")
        if len(parts) != 3:
            raise LifecycleGateError("ls-tree metadata has the wrong field count")
        try:
            mode = parts[0].decode("ascii", errors="strict")
            object_type = parts[1].decode("ascii", errors="strict")
            oid = parts[2].decode("ascii", errors="strict")
            path = path_bytes.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise LifecycleGateError("ls-tree output has invalid encoding") from exc
        if re.fullmatch(r"[0-7]{6}", mode) is None:
            raise LifecycleGateError(f"ls-tree emitted an invalid mode: {mode!r}")
        if object_type not in {"blob", "commit"}:
            raise LifecycleGateError(
                f"ls-tree emitted an unsupported object type: {object_type!r}"
            )
        if re.fullmatch(r"[0-9a-f]{40}", oid) is None:
            raise LifecycleGateError(f"ls-tree emitted an invalid object ID: {oid!r}")
        _validate_repository_path(path)
        if path in entries:
            raise LifecycleGateError(f"ls-tree emitted duplicate path {path!r}")
        entries[path] = _TreeEntry(mode, object_type, oid, path)

    _validate_casefold_collisions(tuple(entries))
    return entries


def _tree_snapshot(repo_root: Path, revision: str) -> dict[str, _TreeEntry]:
    """Return every file-like Git tree entry at ``revision``."""

    completed = _run_git(
        repo_root,
        [
            "-c",
            "core.quotepath=false",
            "ls-tree",
            "-rz",
            "-r",
            "--full-tree",
            revision,
            "--",
        ],
    )
    if completed.returncode != 0:
        raise LifecycleGateError(_git_failure("git ls-tree", completed))
    return _parse_tree_z(completed.stdout)


def _diff_entries(
    repo_root: Path,
    older: str,
    newer: str,
    *,
    find_copies_harder: bool = True,
) -> tuple[DiffEntry, ...]:
    """Return exact name-status entries for one lifecycle boundary."""

    arguments = [
        "-c",
        "core.quotepath=false",
        "diff",
        "--no-ext-diff",
        "--no-textconv",
        "--name-status",
        "-z",
        "-M",
        "-C",
    ]
    if find_copies_harder:
        arguments.append("--find-copies-harder")
    arguments.extend((older, newer, "--"))
    completed = _run_git(repo_root, arguments)
    if completed.returncode != 0:
        raise LifecycleGateError(_git_failure("git diff --name-status -z", completed))
    return parse_name_status_z(completed.stdout)


def _require_test_fixture_flag(test_fixture: bool) -> None:
    """Require the synthetic-policy selector to be an actual Boolean."""

    if type(test_fixture) is not bool:
        raise LifecycleGateError("test_fixture must be a bool")


def _synthetic_fixture_findings(
    labeled_trees: tuple[tuple[str, dict[str, _TreeEntry]], ...],
) -> tuple[str, ...]:
    """Reject production markers or mandatory envelope paths in fixture mode."""

    canonical_by_fold = {
        path.casefold(): path
        for path in _PRODUCTION_MARKERS | _PRODUCTION_MANDATORY_PATHS
    }
    findings: list[str] = []
    for label, tree in labeled_trees:
        for path in sorted(tree):
            canonical = canonical_by_fold.get(path.casefold())
            if canonical is not None:
                findings.append(
                    "test fixture contains production marker/envelope at "
                    f"{label}: observed={path!r} canonical={canonical!r}"
                )
    return tuple(findings)


def _mandatory_envelope_findings(
    labeled_trees: tuple[tuple[str, str, dict[str, _TreeEntry]], ...],
) -> tuple[str, ...]:
    """Require the fixed production source/verifier envelope at every endpoint."""

    findings: list[str] = []
    for label, revision, tree in labeled_trees:
        for path in sorted(_PRODUCTION_MANDATORY_PATHS):
            finding = _require_regular_blob(tree, revision, path, label)
            if finding is not None:
                findings.append(f"production mandatory envelope violation: {finding}")
    return tuple(findings)


def _source_to_evidence_allowed(path: str, production: bool) -> bool:
    """Return whether ``path`` belongs to the exact ``S..E`` policy."""

    if not production:
        return path in _SOURCE_TO_EVIDENCE_SYNTHETIC
    return path in _SOURCE_TO_EVIDENCE_EXACT or path.startswith(
        f"{_DERIVATION_ROOT}/evidence/"
    )


def _evidence_to_closure_allowed(path: str, production: bool) -> bool:
    """Return whether ``path`` belongs to the exact ``E..C`` policy."""

    allowed = (
        _EVIDENCE_TO_CLOSURE_EXACT if production else _EVIDENCE_TO_CLOSURE_SYNTHETIC
    )
    return path in allowed


def _closure_to_wiki_allowed(path: str) -> bool:
    """Return whether ``path`` is one of the seven authorized wiki files."""

    return path in _CLOSURE_TO_WIKI_EXACT


def _require_regular_blob(
    tree: dict[str, _TreeEntry], revision: str, path: str, endpoint: str
) -> str | None:
    """Return a finding unless an endpoint is a regular Git blob."""

    entry = tree.get(path)
    if entry is None:
        return f"{endpoint} path {path!r} is absent at {revision}"
    if entry.object_type != "blob" or entry.mode not in _REGULAR_BLOB_MODES:
        return (
            f"{endpoint} path {path!r} is not a regular blob at {revision}: "
            f"mode={entry.mode} type={entry.object_type}"
        )
    return None


def _entry_endpoint_findings(
    entry: DiffEntry,
    older_revision: str,
    newer_revision: str,
    older_tree: dict[str, _TreeEntry],
    newer_tree: dict[str, _TreeEntry],
) -> tuple[str, ...]:
    """Check every relevant endpoint of one diff record."""

    status_kind = entry.status[0]
    requirements: tuple[tuple[dict[str, _TreeEntry], str, str, str], ...]
    if status_kind == "A":
        requirements = ((newer_tree, newer_revision, entry.paths[0], "target"),)
    elif status_kind == "D":
        requirements = ((older_tree, older_revision, entry.paths[0], "source"),)
    elif status_kind in {"M", "T"}:
        requirements = (
            (older_tree, older_revision, entry.paths[0], "source"),
            (newer_tree, newer_revision, entry.paths[0], "target"),
        )
    else:
        requirements = (
            (older_tree, older_revision, entry.paths[0], "source"),
            (newer_tree, newer_revision, entry.paths[1], "target"),
        )

    findings = [
        finding
        for tree, revision, path, endpoint in requirements
        if (finding := _require_regular_blob(tree, revision, path, endpoint))
        is not None
    ]
    return tuple(findings)


def _validate_boundary(
    repo_root: Path,
    boundary: str,
    older_revision: str,
    newer_revision: str,
    older_tree: dict[str, _TreeEntry],
    newer_tree: dict[str, _TreeEntry],
    allowed: Callable[[str], bool],
    *,
    find_copies_harder: bool,
    production: bool,
) -> tuple[tuple[DiffEntry, ...], tuple[str, ...]]:
    """Validate paths and Git object types on one exact lifecycle boundary."""

    entries = _diff_entries(
        repo_root,
        older_revision,
        newer_revision,
        find_copies_harder=find_copies_harder,
    )
    findings: list[str] = []
    for entry in entries:
        valid_production_destination = (
            entry.status in {"A", "M"} and len(entry.paths) == 1
        )
        if production and not valid_production_destination:
            findings.append(
                f"production {boundary} requires one-path A/M destination records; "
                f"got status {entry.status} paths={entry.paths!r}"
            )
        for path in entry.paths:
            if not allowed(path):
                findings.append(
                    f"{boundary} status {entry.status} changes forbidden path {path!r}"
                )
        if production:
            if valid_production_destination:
                finding = _require_regular_blob(
                    newer_tree,
                    newer_revision,
                    entry.paths[0],
                    "destination",
                )
                if finding is not None:
                    findings.append(f"{boundary} destination violation: {finding}")
        else:
            findings.extend(
                _entry_endpoint_findings(
                    entry,
                    older_revision,
                    newer_revision,
                    older_tree,
                    newer_tree,
                )
            )
    return entries, tuple(findings)


def _phase_destination_envelope_findings(
    boundary: str,
    destination_revision: str,
    destination_tree: dict[str, _TreeEntry],
    entries: tuple[DiffEntry, ...],
    required_paths: frozenset[str],
) -> tuple[str, ...]:
    """Require every fixed phase artifact as an A/M regular-blob destination."""

    destination_paths = frozenset(
        entry.paths[0]
        for entry in entries
        if entry.status in {"A", "M"} and len(entry.paths) == 1
    )
    findings = [
        f"production {boundary} destination envelope is missing A/M path {path!r}"
        for path in sorted(required_paths - destination_paths)
    ]
    for path in sorted(required_paths):
        finding = _require_regular_blob(
            destination_tree,
            destination_revision,
            path,
            f"{boundary} destination envelope",
        )
        if finding is not None:
            findings.append(f"production destination envelope violation: {finding}")
    return tuple(findings)


def _is_manifest_bound_path(path: str) -> bool:
    """Return whether ``path`` belongs to the nonnegotiable manifest envelope."""

    folded = path.casefold()
    return folded.startswith("manuscripts/gauge_vfe_rg/") or folded in {
        "manuscripts/references.bib",
        "manuscripts/scientific_report.sty",
    }


def _casefold_member(path: str, candidates: frozenset[str]) -> bool:
    """Return whether ``path`` equals one candidate under Unicode case folding."""

    folded = path.casefold()
    return any(folded == candidate.casefold() for candidate in candidates)


def _casefold_prefix(path: str, prefix: str) -> bool:
    """Return whether ``path`` begins with ``prefix`` under case folding."""

    return path.casefold().startswith(prefix.casefold())


def _is_publication_protected(path: str, production: bool) -> bool:
    """Return whether publication must preserve ``path`` byte-for-byte."""

    if _is_manifest_bound_path(path):
        return True
    if _casefold_member(path, _TASK_CONTROL_EXACT) or _casefold_prefix(
        path, _TASK_CONTROL_PREFIX
    ):
        return True
    if _casefold_prefix(path, f"{_DERIVATION_ROOT}/"):
        return True
    source_exact = (
        _SOURCE_TO_EVIDENCE_EXACT if production else _SOURCE_TO_EVIDENCE_SYNTHETIC
    )
    closure_exact = (
        _EVIDENCE_TO_CLOSURE_EXACT if production else _EVIDENCE_TO_CLOSURE_SYNTHETIC
    )
    return any(
        (
            _casefold_member(path, source_exact),
            production and _casefold_prefix(path, f"{_DERIVATION_ROOT}/evidence/"),
            _casefold_member(path, closure_exact),
            _casefold_member(path, _CLOSURE_TO_WIKI_EXACT),
        )
    )


def _canonical_publication_path(path: str, production: bool) -> str | None:
    """Return the canonical spelling for a protected noncanonical path."""

    source_exact = (
        _SOURCE_TO_EVIDENCE_EXACT if production else _SOURCE_TO_EVIDENCE_SYNTHETIC
    )
    closure_exact = (
        _EVIDENCE_TO_CLOSURE_EXACT if production else _EVIDENCE_TO_CLOSURE_SYNTHETIC
    )
    exact_paths = (
        _PRODUCTION_MANDATORY_PATHS
        | _TASK_CONTROL_EXACT
        | source_exact
        | closure_exact
        | _CLOSURE_TO_WIKI_EXACT
        | frozenset(
            {
                "manuscripts/references.bib",
                "manuscripts/scientific_report.sty",
            }
        )
    )
    canonical_by_fold = {candidate.casefold(): candidate for candidate in exact_paths}
    canonical = canonical_by_fold.get(path.casefold())
    if canonical is not None:
        return canonical if path != canonical else None

    prefixes = (
        "manuscripts/gauge_vfe_rg/verification/tests/",
        "manuscripts/gauge_vfe_rg/verification/",
        "manuscripts/gauge_vfe_rg/",
        _TASK_CONTROL_PREFIX,
        f"{_DERIVATION_ROOT}/evidence/",
        f"{_DERIVATION_ROOT}/",
    )
    for prefix in prefixes:
        if _casefold_prefix(path, prefix):
            return prefix if not path.startswith(prefix) else None
    return None


def _publication_identity_findings(
    wiki_tree: dict[str, _TreeEntry],
    publication_tree: dict[str, _TreeEntry],
    production: bool,
    *,
    candidate_label: str = "P",
) -> tuple[str, ...]:
    """Compare protected existence, mode, type, and blob object identity."""

    candidates = set(wiki_tree) | set(publication_tree)
    protected = sorted(
        path for path in candidates if _is_publication_protected(path, production)
    )
    findings: list[str] = []
    for endpoint, tree in (("W", wiki_tree), (candidate_label, publication_tree)):
        for path in sorted(tree):
            if not _is_publication_protected(path, production):
                continue
            canonical = _canonical_publication_path(path, production)
            if canonical is not None:
                findings.append(
                    f"publication protected path has noncanonical casing at {endpoint}: "
                    f"observed={path!r} canonical={canonical!r}"
                )
    for path in protected:
        wiki_entry = wiki_tree.get(path)
        publication_entry = publication_tree.get(path)
        if wiki_entry is None or publication_entry is None:
            findings.append(
                f"publication changed protected existence for {path!r}: "
                f"W={wiki_entry is not None} "
                f"{candidate_label}={publication_entry is not None}"
            )
            continue
        for endpoint, entry in (("W", wiki_entry), (candidate_label, publication_entry)):
            if entry.object_type != "blob" or entry.mode not in _REGULAR_BLOB_MODES:
                findings.append(
                    f"publication protected path {path!r} is not a regular blob at "
                    f"{endpoint}: mode={entry.mode} type={entry.object_type}"
                )
        if wiki_entry.mode != publication_entry.mode:
            findings.append(
                f"publication changed protected mode for {path!r}: "
                f"W={wiki_entry.mode} {candidate_label}={publication_entry.mode}"
            )
        if wiki_entry.object_type != publication_entry.object_type:
            findings.append(
                f"publication changed protected type for {path!r}: "
                f"W={wiki_entry.object_type} "
                f"{candidate_label}={publication_entry.object_type}"
            )
        if wiki_entry.oid != publication_entry.oid:
            findings.append(
                f"publication changed protected blob for {path!r}: "
                f"W={wiki_entry.oid} {candidate_label}={publication_entry.oid}"
            )
    return tuple(findings)


def _newly_reachable_commits(
    repo_root: Path,
    older_revision: str,
    newer_revision: str,
    boundary: str,
) -> tuple[str, ...]:
    """Enumerate the complete commit DAG newly reachable at a phase endpoint."""

    completed = _run_git(
        repo_root,
        [
            "rev-list",
            "--topo-order",
            newer_revision,
            f"^{older_revision}",
        ],
    )
    if completed.returncode != 0:
        raise LifecycleGateError(
            _git_failure(f"git rev-list newly-reachable {boundary}", completed)
        )
    try:
        rendered = completed.stdout.decode("ascii", errors="strict")
    except UnicodeDecodeError as exc:
        raise LifecycleGateError(
            f"git rev-list newly-reachable {boundary} is not ASCII"
        ) from exc
    if rendered and not rendered.endswith("\n"):
        raise LifecycleGateError(
            f"git rev-list newly-reachable {boundary} is not line terminated"
        )
    revisions = tuple(line for line in rendered.splitlines() if line)
    if (
        len(revisions) != len(set(revisions))
        or any(_FULL_COMMIT_RE.fullmatch(revision) is None for revision in revisions)
        or older_revision in revisions
        or (newer_revision != older_revision and newer_revision not in revisions)
    ):
        raise LifecycleGateError(
            f"git rev-list newly-reachable {boundary} emitted an invalid commit set"
        )
    return revisions


def _commit_parents(
    repo_root: Path,
    revision: str,
    boundary: str,
) -> tuple[str, ...]:
    """Return the exact parent identities for one commit in a phase graph."""

    completed = _run_git(
        repo_root,
        ["rev-list", "--parents", "--max-count=1", revision],
    )
    if completed.returncode != 0:
        raise LifecycleGateError(
            _git_failure(f"git rev-list --parents {boundary}", completed)
        )
    try:
        rendered = completed.stdout.decode("ascii", errors="strict")
    except UnicodeDecodeError as exc:
        raise LifecycleGateError(
            f"git rev-list --parents {boundary} is not ASCII"
        ) from exc
    if not rendered.endswith("\n") or rendered.count("\n") != 1:
        raise LifecycleGateError(
            f"git rev-list --parents {boundary} is not one terminated line"
        )
    identities = tuple(rendered.rstrip("\n").split(" "))
    if (
        not identities
        or identities[0] != revision
        or len(identities) != len(set(identities))
        or any(_FULL_COMMIT_RE.fullmatch(item) is None for item in identities)
    ):
        raise LifecycleGateError(
            f"git rev-list --parents {boundary} emitted malformed identities"
        )
    return identities[1:]


def _phase_history_findings(
    repo_root: Path,
    boundary: str,
    older_revision: str,
    newer_revision: str,
    older_tree: dict[str, _TreeEntry],
    allowed: Callable[[str], bool],
    *,
    find_copies_harder: bool,
    production: bool,
) -> tuple[str, ...]:
    """Validate every newly reachable tree and incoming edge in one phase."""

    revisions = _newly_reachable_commits(
        repo_root,
        older_revision,
        newer_revision,
        boundary,
    )
    trees: dict[str, dict[str, _TreeEntry]] = {older_revision: older_tree}

    def tree(revision: str) -> dict[str, _TreeEntry]:
        snapshot = trees.get(revision)
        if snapshot is None:
            snapshot = _tree_snapshot(repo_root, revision)
            trees[revision] = snapshot
        return snapshot

    findings: list[str] = []
    for revision in revisions:
        revision_tree = tree(revision)
        _baseline_entries, baseline_findings = _validate_boundary(
            repo_root,
            f"{boundary} baseline..{revision}",
            older_revision,
            revision,
            older_tree,
            revision_tree,
            allowed,
            find_copies_harder=find_copies_harder,
            production=production,
        )
        findings.extend(
            f"{boundary} phase-history tree violation at {revision}: {finding}"
            for finding in baseline_findings
        )
        for parent in _commit_parents(repo_root, revision, boundary):
            parent_tree = tree(parent)
            _edge_entries, edge_findings = _validate_boundary(
                repo_root,
                f"{boundary} edge {parent}..{revision}",
                parent,
                revision,
                parent_tree,
                revision_tree,
                allowed,
                find_copies_harder=find_copies_harder,
                production=production,
            )
            findings.extend(
                f"{boundary} phase-history edge violation {parent}..{revision}: "
                f"{finding}"
                for finding in edge_findings
            )
    return tuple(findings)


def _protected_history_findings(
    repo_root: Path,
    wiki_tree: dict[str, _TreeEntry],
    older_revision: str,
    newer_revision: str,
    boundary: str,
    production: bool,
) -> tuple[str, ...]:
    """Require every newly reachable post-W commit tree to preserve W exactly."""

    findings: list[str] = []
    for revision in _newly_reachable_commits(
        repo_root, older_revision, newer_revision, boundary
    ):
        commit_findings = _publication_identity_findings(
            wiki_tree,
            _tree_snapshot(repo_root, revision),
            production,
            candidate_label=f"commit {revision}",
        )
        findings.extend(
            f"{boundary} protected history violation at {revision}: {finding}"
            for finding in commit_findings
        )
    return tuple(findings)


def validate_lifecycle(
    repo_root: Path,
    source_revision: str,
    evidence_revision: str,
    closure_revision: str,
    wiki_revision: str,
    *,
    test_fixture: bool = False,
) -> GateReport:
    """Validate the trusted production lifecycle or an explicit test fixture."""

    protocol_profile = (
        _SYNTHETIC_PROTOCOL_PROFILE
        if test_fixture
        else _PRODUCTION_PROTOCOL_PROFILE
    )
    head_revision: str | None = None
    git_executable = str(_FIXED_GIT_EXECUTABLE)
    git_executable_sha256: str | None = None
    git_identity_token: Token[dict[str, Any] | None] | None = None
    git_guard: _WindowsGitGuard | None = None
    git_guard_token: Token[Any | None] | None = None
    try:
        git_guard = _WindowsGitGuard()
        git_guard_token = _ACTIVE_GIT_GUARD.set(git_guard)
        git_snapshot = _fixed_git_snapshot()
        git_executable = git_snapshot["path"]
        git_executable_sha256 = git_snapshot["sha256"]
        git_identity_token = _ACTIVE_GIT_IDENTITY.set(git_snapshot)
        _require_test_fixture_flag(test_fixture)
        root = _require_repository_root(Path(repo_root))
        _require_controlled_git_metadata(root)
        head_revision = _resolve_head_commit(root)
        resolved = (
            ("S", _resolve_commit(root, source_revision)),
            ("E", _resolve_commit(root, evidence_revision)),
            ("C", _resolve_commit(root, closure_revision)),
            ("W", _resolve_commit(root, wiki_revision)),
        )
        revision_map = dict(resolved)
        _require_ancestor(root, revision_map["S"], revision_map["E"], "S..E")
        _require_ancestor(root, revision_map["E"], revision_map["C"], "E..C")
        _require_ancestor(root, revision_map["C"], revision_map["W"], "C..W")
        _require_ancestor(root, revision_map["W"], head_revision, "W..HEAD")
        trees = {label: _tree_snapshot(root, revision) for label, revision in resolved}
        production = not test_fixture
        specifications: tuple[
            tuple[
                str,
                str,
                str,
                Callable[[str], bool],
            ],
            ...,
        ] = (
            (
                "S..E",
                "S",
                "E",
                lambda path: _source_to_evidence_allowed(path, production),
            ),
            (
                "E..C",
                "E",
                "C",
                lambda path: _evidence_to_closure_allowed(path, production),
            ),
            ("C..W", "C", "W", _closure_to_wiki_allowed),
        )
        all_changes: list[tuple[str, tuple[DiffEntry, ...]]] = []
        if production:
            findings = list(
                _mandatory_envelope_findings(
                    tuple(
                        (label, revision_map[label], trees[label])
                        for label, _ in resolved
                    )
                )
            )
        else:
            head_tree = _tree_snapshot(root, head_revision)
            findings = list(
                _synthetic_fixture_findings(
                    (("HEAD", head_tree),)
                    + tuple((label, trees[label]) for label, _ in resolved)
                )
            )
        for boundary, older_label, newer_label, allowed in specifications:
            entries, boundary_findings = _validate_boundary(
                root,
                boundary,
                revision_map[older_label],
                revision_map[newer_label],
                trees[older_label],
                trees[newer_label],
                allowed,
                find_copies_harder=production,
                production=production,
            )
            all_changes.append((boundary, entries))
            findings.extend(boundary_findings)
            findings.extend(
                _phase_history_findings(
                    root,
                    boundary,
                    revision_map[older_label],
                    revision_map[newer_label],
                    trees[older_label],
                    allowed,
                    find_copies_harder=production,
                    production=production,
                )
            )
        if production:
            changes_by_boundary = dict(all_changes)
            findings.extend(
                _phase_destination_envelope_findings(
                    "S..E",
                    revision_map["E"],
                    trees["E"],
                    changes_by_boundary["S..E"],
                    _SOURCE_TO_EVIDENCE_EXACT,
                )
            )
            findings.extend(
                _phase_destination_envelope_findings(
                    "E..C",
                    revision_map["C"],
                    trees["C"],
                    changes_by_boundary["E..C"],
                    _EVIDENCE_TO_CLOSURE_EXACT,
                )
            )
            c_w_entries = changes_by_boundary["C..W"]
            changed_wiki_paths = frozenset(
                entry.paths[0]
                for entry in c_w_entries
                if entry.status in {"A", "M"} and len(entry.paths) == 1
            )
            if changed_wiki_paths != _CLOSURE_TO_WIKI_EXACT:
                missing = sorted(_CLOSURE_TO_WIKI_EXACT - changed_wiki_paths)
                extra = sorted(changed_wiki_paths - _CLOSURE_TO_WIKI_EXACT)
                findings.append(
                    "production C..W must change exactly all seven authorized wiki "
                    f"paths: missing={missing!r} extra={extra!r}"
                )
            for path in sorted(_CLOSURE_TO_WIKI_EXACT):
                finding = _require_regular_blob(
                    trees["W"], revision_map["W"], path, "required wiki"
                )
                if finding is not None:
                    findings.append(f"C..W required artifact violation: {finding}")
        findings.extend(
            _protected_history_findings(
                root,
                trees["W"],
                revision_map["W"],
                head_revision,
                "W..HEAD",
                production,
            )
        )
        _require_controlled_git_metadata(root)
        closing_head_revision = _resolve_head_commit(root)
        if closing_head_revision != head_revision:
            raise LifecycleGateError(
                "HEAD changed during lifecycle validation: "
                f"{head_revision} -> {closing_head_revision}"
            )
        closing_git_identity = _fixed_git_snapshot()
        if closing_git_identity != git_snapshot:
            raise LifecycleGateError(
                "fixed Git executable changed after M0: "
                f"{git_snapshot!r} -> "
                f"{closing_git_identity!r}"
            )
    except (LifecycleGateError, OSError) as exc:
        report = GateReport(
            ok=False,
            errors=(str(exc),),
            protocol_profile=protocol_profile,
            head_revision=head_revision,
            git_executable=git_executable,
            git_executable_sha256=git_executable_sha256,
        )
    except BaseException:
        if git_identity_token is not None:
            _ACTIVE_GIT_IDENTITY.reset(git_identity_token)
        if git_guard_token is not None:
            _ACTIVE_GIT_GUARD.reset(git_guard_token)
        if git_guard is not None:
            git_guard.close()
        raise
    else:
        report = GateReport(
            ok=not findings,
            errors=tuple(findings),
            revisions=resolved,
            changes=tuple(all_changes),
            protocol_profile=protocol_profile,
            head_revision=head_revision,
            git_executable=git_executable,
            git_executable_sha256=git_executable_sha256,
        )
    if git_identity_token is not None:
        _ACTIVE_GIT_IDENTITY.reset(git_identity_token)
    if git_guard_token is not None:
        _ACTIVE_GIT_GUARD.reset(git_guard_token)
    if git_guard is not None:
        git_guard.close()
    return report


def verify_publication_identity(
    repo_root: Path,
    wiki_revision: str,
    publication_revision: str,
    *,
    test_fixture: bool = False,
) -> GateReport:
    """Validate descent and protected union identity from ``W`` to publication."""

    protocol_profile = (
        _SYNTHETIC_PROTOCOL_PROFILE
        if test_fixture
        else _PRODUCTION_PROTOCOL_PROFILE
    )
    head_revision: str | None = None
    git_executable = str(_FIXED_GIT_EXECUTABLE)
    git_executable_sha256: str | None = None
    git_identity_token: Token[dict[str, Any] | None] | None = None
    git_guard: _WindowsGitGuard | None = None
    git_guard_token: Token[Any | None] | None = None
    try:
        git_guard = _WindowsGitGuard()
        git_guard_token = _ACTIVE_GIT_GUARD.set(git_guard)
        git_snapshot = _fixed_git_snapshot()
        git_executable = git_snapshot["path"]
        git_executable_sha256 = git_snapshot["sha256"]
        git_identity_token = _ACTIVE_GIT_IDENTITY.set(git_snapshot)
        _require_test_fixture_flag(test_fixture)
        root = _require_repository_root(Path(repo_root))
        _require_controlled_git_metadata(root)
        head_revision = _resolve_head_commit(root)
        resolved = (
            ("W", _resolve_commit(root, wiki_revision)),
            ("P", _resolve_commit(root, publication_revision)),
        )
        revision_map = dict(resolved)
        _require_ancestor(root, revision_map["W"], revision_map["P"], "W..P")
        _require_ancestor(root, revision_map["P"], head_revision, "P..HEAD")
        wiki_tree = _tree_snapshot(root, revision_map["W"])
        publication_tree = _tree_snapshot(root, revision_map["P"])
        production = not test_fixture
        if production:
            findings = list(
                _mandatory_envelope_findings(
                    (
                        ("W", revision_map["W"], wiki_tree),
                        ("P", revision_map["P"], publication_tree),
                    )
                )
            )
        else:
            head_tree = _tree_snapshot(root, head_revision)
            findings = list(
                _synthetic_fixture_findings(
                    (
                        ("HEAD", head_tree),
                        ("W", wiki_tree),
                        ("P", publication_tree),
                    )
                )
            )
        findings.extend(
            _publication_identity_findings(wiki_tree, publication_tree, production)
        )
        findings.extend(
            _protected_history_findings(
                root,
                wiki_tree,
                revision_map["W"],
                revision_map["P"],
                "W..P",
                production,
            )
        )
        findings.extend(
            _protected_history_findings(
                root,
                wiki_tree,
                revision_map["P"],
                head_revision,
                "P..HEAD",
                production,
            )
        )
        changes = (("W..P", _diff_entries(root, revision_map["W"], revision_map["P"])),)
        _require_controlled_git_metadata(root)
        closing_head_revision = _resolve_head_commit(root)
        if closing_head_revision != head_revision:
            raise LifecycleGateError(
                "HEAD changed during publication validation: "
                f"{head_revision} -> {closing_head_revision}"
            )
        closing_git_identity = _fixed_git_snapshot()
        if closing_git_identity != git_snapshot:
            raise LifecycleGateError(
                "fixed Git executable changed after M0: "
                f"{git_snapshot!r} -> "
                f"{closing_git_identity!r}"
            )
    except (LifecycleGateError, OSError) as exc:
        report = GateReport(
            ok=False,
            errors=(str(exc),),
            protocol_profile=protocol_profile,
            head_revision=head_revision,
            git_executable=git_executable,
            git_executable_sha256=git_executable_sha256,
        )
    except BaseException:
        if git_identity_token is not None:
            _ACTIVE_GIT_IDENTITY.reset(git_identity_token)
        if git_guard_token is not None:
            _ACTIVE_GIT_GUARD.reset(git_guard_token)
        if git_guard is not None:
            git_guard.close()
        raise
    else:
        report = GateReport(
            ok=not findings,
            errors=tuple(findings),
            revisions=resolved,
            changes=changes,
            protocol_profile=protocol_profile,
            head_revision=head_revision,
            git_executable=git_executable,
            git_executable_sha256=git_executable_sha256,
        )
    if git_identity_token is not None:
        _ACTIVE_GIT_IDENTITY.reset(git_identity_token)
    if git_guard_token is not None:
        _ACTIVE_GIT_GUARD.reset(git_guard_token)
    if git_guard is not None:
        git_guard.close()
    return report


__all__ = [
    "DiffEntry",
    "GateReport",
    "LifecycleGateError",
    "LifecycleReport",
    "PublicationIdentityReport",
    "parse_name_status_z",
    "validate_lifecycle",
    "verify_publication_identity",
]
