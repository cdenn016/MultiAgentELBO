"""Fail-closed audit for an isolated gauge-VFE/RG TeX build.

The audit treats the command record and generated files as evidence, never as
instructions.  It therefore does not execute TeX, consult metadata sidecars,
or repair a build.  Every value reported below is derived from the supplied
Git revision and the bytes present at the audit instant.
"""

import argparse
import atexit
import base64
import csv
import ctypes
import hashlib
import importlib.machinery
import json
import math
import msvcrt
import os
import re
import stat
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from io import BytesIO, StringIO
from pathlib import Path, PurePosixPath
from typing import Any
from ctypes import wintypes


_TRUSTED_PYTHON = Path(r"C:\Python314\python.exe")
_TRUSTED_GIT = Path(r"C:\Program Files\Git\cmd\git.exe")
_TRUSTED_PYPDF_SITE = Path(
    r"C:\Users\chris and christine\AppData\Roaming\Python\Python314\site-packages"
)
_TRUSTED_PYPDF_ROOT = _TRUSTED_PYPDF_SITE / "pypdf"
_TRUSTED_PYPDF_INIT = _TRUSTED_PYPDF_ROOT / "__init__.py"
_EXPECTED_PYPDF_VERSION = "6.12.2"
_FIXED_AUDIT_TEMP_BASE = Path(
    r"C:\Users\chris and christine\AppData\Local\Temp"
)
_WINDOWS_DIRECTORY = Path(r"C:\WINDOWS")
_WINDOWS_SYSTEM_DIRECTORY = _WINDOWS_DIRECTORY / "System32"

if __name__ == "__main__":
    if sys.flags.isolated != 1 or sys.flags.no_site != 1:
        raise SystemExit(
            "build_audit.py production CLI requires exact isolated no-site startup (-I -S)"
        )
    if Path(sys.executable).resolve() != _TRUSTED_PYTHON.resolve():
        raise SystemExit(
            f"build_audit.py production CLI requires exact Python executable {_TRUSTED_PYTHON}"
        )


def _bootstrap_first_reparse_component(path: Path) -> Path | None:
    """Check an import-bootstrap path without depending on later helpers."""

    absolute = Path(os.path.abspath(path))
    parts = absolute.parts
    if not parts:
        return None
    current = Path(parts[0])
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    for part in parts[1:]:
        current /= part
        try:
            information = current.lstat()
        except OSError:
            return None
        attributes = getattr(information, "st_file_attributes", 0)
        if current.is_symlink() or bool(attributes & reparse_flag):
            return current
    return None


def _bootstrap_pypdf_pycache_base() -> Path:
    """Choose a non-ambient, validated base before importing third-party code."""

    if __name__ == "__main__":
        if "--help" in sys.argv:
            base = _FIXED_AUDIT_TEMP_BASE
        else:
            positions = [index for index, value in enumerate(sys.argv) if value == "--build-dir"]
            if len(positions) != 1 or positions[0] + 1 >= len(sys.argv):
                raise RuntimeError(
                    "build_audit.py production CLI requires exactly one --build-dir before dependency admission"
                )
            raw_build_dir = Path(sys.argv[positions[0] + 1])
            if not raw_build_dir.is_absolute():
                raise RuntimeError("production --build-dir must be absolute before dependency admission")
            build_dir = raw_build_dir.resolve(strict=True)
            base = build_dir / ".tex-tmp"
    else:
        base = _FIXED_AUDIT_TEMP_BASE
    component = _bootstrap_first_reparse_component(base)
    if component is not None:
        raise RuntimeError(f"controlled pypdf pycache base is reparse-mediated at {component}")
    resolved = base.resolve(strict=True)
    if not resolved.is_dir():
        raise RuntimeError("controlled pypdf pycache base is not a directory")
    return resolved


def _bootstrap_stat_identity(information: os.stat_result) -> tuple[int, ...]:
    """Return the private filesystem identity used during import admission."""

    return (
        information.st_dev,
        information.st_ino,
        information.st_mode,
        information.st_size,
        information.st_mtime_ns,
        information.st_ctime_ns,
        getattr(information, "st_file_attributes", 0),
    )


def _bootstrap_content_identity(information: os.stat_result) -> tuple[int, ...]:
    """Return the handle-comparable subset of a filesystem identity."""

    return (
        information.st_dev,
        information.st_ino,
        information.st_size,
        information.st_mtime_ns,
        getattr(information, "st_file_attributes", 0),
    )


def _bootstrap_read_regular(path: Path) -> tuple[bytes, tuple[int, ...]]:
    """Read one non-reparse file with path/open-handle stability checks."""

    component = _bootstrap_first_reparse_component(path)
    if component is not None:
        raise RuntimeError(f"pypdf inventory path is reparse-mediated at {component}")
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise RuntimeError(f"pypdf inventory path is not a regular file: {path}")
    with path.open("rb") as stream:
        opened = os.fstat(stream.fileno())
        if _bootstrap_content_identity(before) != _bootstrap_content_identity(opened):
            raise RuntimeError(f"pypdf inventory path changed while opening: {path}")
        payload = stream.read()
        after_read = os.fstat(stream.fileno())
    after_close = path.lstat()
    if (
        _bootstrap_content_identity(opened) != _bootstrap_content_identity(after_read)
        or _bootstrap_stat_identity(before) != _bootstrap_stat_identity(after_close)
    ):
        raise RuntimeError(f"pypdf inventory path changed during stable read: {path}")
    return payload, _bootstrap_stat_identity(after_close)


def _bootstrap_pypdf_distribution_snapshot() -> dict[str, Any]:
    """Capture exact RECORD-listed pypdf bytes without importing package code."""

    for path, label in (
        (_TRUSTED_PYPDF_SITE, "trusted pypdf site-packages root"),
        (_TRUSTED_PYPDF_ROOT, "trusted pypdf package root"),
        (_TRUSTED_PYPDF_INIT, "trusted pypdf initializer"),
    ):
        component = _bootstrap_first_reparse_component(path)
        if component is not None:
            raise RuntimeError(f"{label} is reparse-mediated at {component}")
    site = _TRUSTED_PYPDF_SITE.resolve(strict=True)
    package_root = _TRUSTED_PYPDF_ROOT.resolve(strict=True)
    module_path = _TRUSTED_PYPDF_INIT.resolve(strict=True)
    if package_root.parent != site or module_path != package_root / "__init__.py":
        raise RuntimeError("trusted pypdf package or initializer is outside the exact trusted site")

    dist_infos = []
    for candidate in site.iterdir():
        folded = candidate.name.casefold()
        if not (folded.startswith("pypdf-") and folded.endswith(".dist-info")):
            continue
        component = _bootstrap_first_reparse_component(candidate)
        if component is not None:
            raise RuntimeError(f"pypdf dist-info path is reparse-mediated at {component}")
        if not candidate.is_dir():
            raise RuntimeError(f"pypdf dist-info candidate is not a directory: {candidate}")
        dist_infos.append(candidate.resolve(strict=True))
    if len(dist_infos) != 1:
        raise RuntimeError(
            f"trusted pypdf site must contain exactly one pypdf distribution, found {len(dist_infos)}"
        )
    distribution_root = dist_infos[0]
    record_path = distribution_root / "RECORD"
    record_bytes, record_identity = _bootstrap_read_regular(record_path)
    try:
        rows = list(csv.reader(StringIO(record_bytes.decode("utf-8"), newline="")))
    except (UnicodeError, csv.Error) as exc:
        raise RuntimeError(f"pypdf RECORD is not strict UTF-8 CSV: {exc}") from exc
    if not rows:
        raise RuntimeError("pypdf RECORD is empty")

    entries: list[dict[str, str | int]] = []
    identities: dict[str, tuple[int, ...]] = {}
    payloads: dict[str, bytes] = {}
    exact_paths: set[str] = set()
    folded_paths: set[str] = set()
    resolved_paths: set[str] = set()
    for row_number, row in enumerate(rows, 1):
        if len(row) != 3:
            raise RuntimeError(f"pypdf RECORD row {row_number} must contain exactly three fields")
        raw_path, declared_hash, declared_size = row
        if (
            not raw_path
            or "\\" in raw_path
            or PurePosixPath(raw_path).is_absolute()
            or any(part in {"", ".", ".."} or ":" in part for part in raw_path.split("/"))
        ):
            raise RuntimeError(f"pypdf RECORD row {row_number} has unsafe path {raw_path!r}")
        folded = raw_path.casefold()
        if raw_path in exact_paths:
            raise RuntimeError(f"pypdf RECORD has duplicate path {raw_path!r}")
        if folded in folded_paths:
            raise RuntimeError(f"pypdf RECORD has case-colliding path {raw_path!r}")
        exact_paths.add(raw_path)
        folded_paths.add(folded)

        candidate = site.joinpath(*raw_path.split("/"))
        component = _bootstrap_first_reparse_component(candidate)
        if component is not None:
            raise RuntimeError(f"pypdf RECORD path is reparse-mediated at {component}")
        try:
            resolved_candidate = candidate.resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise RuntimeError(f"pypdf RECORD path is missing at row {row_number}: {raw_path}") from exc
        try:
            resolved_candidate.relative_to(site)
        except ValueError as exc:
            raise RuntimeError(f"pypdf RECORD path escapes the trusted site: {raw_path}") from exc
        normalized_resolved = os.path.normcase(str(resolved_candidate))
        if normalized_resolved in resolved_paths:
            raise RuntimeError(f"pypdf RECORD paths alias the same installed file: {raw_path}")
        resolved_paths.add(normalized_resolved)

        payload, identity = _bootstrap_read_regular(resolved_candidate)
        actual_hash = hashlib.sha256(payload).hexdigest()
        actual_size = len(payload)
        if bool(declared_hash) != bool(declared_size):
            raise RuntimeError(
                f"pypdf RECORD row {row_number} must declare both hash and size or neither"
            )
        if declared_hash:
            algorithm, separator, encoded_digest = declared_hash.partition("=")
            if algorithm != "sha256" or separator != "=" or not encoded_digest:
                raise RuntimeError(
                    f"pypdf RECORD row {row_number} uses unsupported declared hash {declared_hash!r}"
                )
            try:
                declared_digest_bytes = base64.b64decode(
                    encoded_digest + "=" * (-len(encoded_digest) % 4),
                    altchars=b"-_",
                    validate=True,
                )
            except (ValueError, TypeError) as exc:
                raise RuntimeError(
                    f"pypdf RECORD row {row_number} has invalid declared hash encoding"
                ) from exc
            if len(declared_digest_bytes) != hashlib.sha256().digest_size:
                raise RuntimeError(
                    f"pypdf RECORD row {row_number} has invalid declared SHA-256 length"
                )
            if declared_digest_bytes.hex() != actual_hash:
                raise RuntimeError(f"pypdf RECORD declared hash disagrees for {raw_path}")
            if re.fullmatch(r"0|[1-9][0-9]*", declared_size) is None:
                raise RuntimeError(
                    f"pypdf RECORD row {row_number} has invalid declared size {declared_size!r}"
                )
            if int(declared_size) != actual_size:
                raise RuntimeError(f"pypdf RECORD declared size disagrees for {raw_path}")
        entries.append({"path": raw_path, "sha256": actual_hash, "byte_count": actual_size})
        identities[raw_path] = identity
        payloads[raw_path] = payload

    entries.sort(key=lambda entry: str(entry["path"]))
    record_relative = record_path.relative_to(site).as_posix()
    module_relative = module_path.relative_to(site).as_posix()
    metadata_candidates = [
        path
        for path in exact_paths
        if PurePosixPath(path).name == "METADATA"
        and PurePosixPath(path).parent.name == distribution_root.name
    ]
    if record_relative not in exact_paths:
        raise RuntimeError("pypdf RECORD does not inventory its own actual bytes")
    if module_relative not in exact_paths:
        raise RuntimeError("pypdf RECORD does not inventory the imported module origin")
    if len(metadata_candidates) != 1:
        raise RuntimeError("pypdf RECORD must inventory exactly one distribution METADATA file")
    metadata_text = payloads[metadata_candidates[0]].decode("utf-8")
    names = [line[6:].strip() for line in metadata_text.splitlines() if line.startswith("Name: ")]
    versions = [line[9:].strip() for line in metadata_text.splitlines() if line.startswith("Version: ")]
    if names != ["pypdf"] or len(versions) != 1 or not versions[0]:
        raise RuntimeError("pypdf distribution METADATA has no exact Name/Version identity")
    version = versions[0]
    if version != _EXPECTED_PYPDF_VERSION:
        raise RuntimeError(
            f"pypdf distribution version {version!r} does not equal the exact S-bound pin "
            f"{_EXPECTED_PYPDF_VERSION!r}"
        )
    expected_dist_info_name = f"pypdf-{version}.dist-info"
    if distribution_root.name != expected_dist_info_name:
        raise RuntimeError(
            f"pypdf dist-info root must be exactly {expected_dist_info_name}, found {distribution_root.name}"
        )

    root_identities: dict[str, tuple[int, ...]] = {}
    for label, root in (
        ("site", site),
        ("package", package_root),
        ("distribution", distribution_root),
    ):
        information = root.lstat()
        if not stat.S_ISDIR(information.st_mode):
            raise RuntimeError(f"trusted pypdf {label} root is not a directory")
        root_identities[label] = _bootstrap_stat_identity(information)
    canonical_entries = json.dumps(
        entries,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    provenance = {
        "pypdf": version,
        "pypdf_module_path": str(module_path),
        "pypdf_module_sha256": hashlib.sha256(payloads[module_relative]).hexdigest(),
        "pypdf_package_root": str(package_root),
        "pypdf_package_tree_sha256": hashlib.sha256(canonical_entries).hexdigest(),
        "pypdf_package_file_count": len(entries),
        "pypdf_distribution_root": str(distribution_root),
        "pypdf_record_path": str(record_path),
        "pypdf_record_sha256": hashlib.sha256(record_bytes).hexdigest(),
    }
    return {
        "provenance": provenance,
        "files": {
            str(entry["path"]): {
                "sha256": str(entry["sha256"]),
                "byte_count": int(entry["byte_count"]),
            }
            for entry in entries
        },
        "file_identities": identities,
        "root_identities": root_identities,
    }


_KERNEL32 = ctypes.WinDLL("kernel32", use_last_error=True)
_CREATE_FILE = _KERNEL32.CreateFileW
_CREATE_FILE.argtypes = (
    wintypes.LPCWSTR,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.LPVOID,
    wintypes.DWORD,
    wintypes.DWORD,
    wintypes.HANDLE,
)
_CREATE_FILE.restype = wintypes.HANDLE
_CLOSE_HANDLE = _KERNEL32.CloseHandle
_CLOSE_HANDLE.argtypes = (wintypes.HANDLE,)
_CLOSE_HANDLE.restype = wintypes.BOOL
_GENERIC_READ = 0x80000000
_GENERIC_WRITE = 0x40000000
_FILE_SHARE_READ = 0x00000001
_CREATE_NEW = 1
_OPEN_EXISTING = 3
_FILE_ATTRIBUTE_NORMAL = 0x00000080
_INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value


def _open_deny_write_file(path: Path) -> tuple[Path, Any]:
    """Open a regular file while denying concurrent write/delete sharing."""

    component = _bootstrap_first_reparse_component(path)
    if component is not None:
        raise OSError(f"launch-bound path is reparse-mediated at {component}")
    resolved = path.resolve(strict=True)
    handle = _CREATE_FILE(
        str(resolved),
        _GENERIC_READ,
        _FILE_SHARE_READ,
        None,
        _OPEN_EXISTING,
        _FILE_ATTRIBUTE_NORMAL,
        None,
    )
    if handle == _INVALID_HANDLE_VALUE:
        raise OSError(ctypes.get_last_error(), f"cannot acquire deny-write handle for {resolved}")
    try:
        descriptor = msvcrt.open_osfhandle(int(handle), os.O_RDONLY | os.O_BINARY)
    except BaseException:
        _CLOSE_HANDLE(handle)
        raise
    try:
        stream = os.fdopen(descriptor, "rb", buffering=0)
    except BaseException:
        os.close(descriptor)
        raise
    return resolved, stream


def _locked_stream_snapshot(path: Path, stream: Any) -> dict[str, Any]:
    """Hash and identify a deny-write file through its retained handle."""

    before = os.fstat(stream.fileno())
    path_before = path.lstat()
    if (
        not stat.S_ISREG(before.st_mode)
        or _bootstrap_content_identity(path_before) != _bootstrap_content_identity(before)
    ):
        raise OSError(f"held handle does not identify the regular path {path}")
    stream.seek(0)
    digest = hashlib.sha256()
    byte_count = 0
    for block in iter(lambda: stream.read(1024 * 1024), b""):
        digest.update(block)
        byte_count += len(block)
    after = os.fstat(stream.fileno())
    path_after = path.lstat()
    stream.seek(0)
    if (
        _bootstrap_stat_identity(before) != _bootstrap_stat_identity(after)
        or _bootstrap_stat_identity(path_before) != _bootstrap_stat_identity(path_after)
        or _bootstrap_content_identity(after) != _bootstrap_content_identity(path_after)
        or byte_count != after.st_size
    ):
        raise OSError(f"held-handle bytes or filesystem identity changed while hashing {path}")
    return {
        "path": str(path),
        "sha256": digest.hexdigest(),
        "byte_count": byte_count,
        "stat_identity": _bootstrap_stat_identity(path_after),
    }


def _assert_locked_stream_m0(
    path: Path,
    stream: Any,
    expected: dict[str, Any],
    label: str,
) -> None:
    """Require one retained handle to remain at its run-scoped M0 identity."""

    if _locked_stream_snapshot(path, stream) != expected:
        raise RuntimeError(f"{label} changed from its retained-handle M0")


@dataclass(slots=True)
class _HeldBuildArtifact:
    """One immutable build artifact read and retained through one audit handoff."""

    path: Path
    stream: Any
    payload: bytes
    snapshot: dict[str, Any]


@dataclass(slots=True)
class _RetainedBuildArtifactInventory:
    """Complete deny-write/delete inventory for one isolated build directory."""

    root: Path
    entries: dict[str, _HeldBuildArtifact]
    acquisition_errors: list[str]

    def _normalized(self, path: Path) -> str:
        return os.path.normcase(os.path.abspath(os.fspath(path)))

    def contains_path(self, path: Path) -> bool:
        try:
            return os.path.commonpath((self._normalized(path), self._normalized(self.root))) == self._normalized(
                self.root
            )
        except ValueError:
            return False

    def get(self, path: Path) -> _HeldBuildArtifact | None:
        return self.entries.get(self._normalized(path))

    def read(self, path: Path) -> tuple[bytes, tuple[int, ...]]:
        entry = self.get(path)
        if entry is None:
            raise OSError(f"build artifact was absent from the retained M0 inventory: {path}")
        current = _locked_stream_snapshot(entry.path, entry.stream)
        if current != entry.snapshot:
            raise OSError(f"retained build artifact changed from M0: {entry.path}")
        return entry.payload, tuple(entry.snapshot["stat_identity"])

    def snapshot(
        self,
        errors: list[str],
        phase: str,
    ) -> tuple[dict[str, str], dict[str, tuple[int, ...]]]:
        hashes: dict[str, str] = {}
        states: dict[str, tuple[int, ...]] = {}
        try:
            current_paths = _enumerate_build_artifact_paths(self.root)
        except OSError as exc:
            errors.append(f"cannot enumerate complete build artifact inventory at {phase}: {exc}")
            current_paths = []
        expected_relative = {
            entry.path.relative_to(self.root).as_posix() for entry in self.entries.values()
        }
        current_relative = {path.relative_to(self.root).as_posix() for path in current_paths}
        if current_relative != expected_relative:
            added = sorted(current_relative - expected_relative)
            removed = sorted(expected_relative - current_relative)
            errors.append(
                f"build artifact inventory changed from retained M0 at {phase}: "
                f"added={added!r}, removed={removed!r}"
            )
        for entry in sorted(self.entries.values(), key=lambda item: item.path.as_posix()):
            relative = entry.path.relative_to(self.root).as_posix()
            try:
                current = _locked_stream_snapshot(entry.path, entry.stream)
            except OSError as exc:
                errors.append(f"cannot validate retained build artifact {relative} at {phase}: {exc}")
                continue
            if current != entry.snapshot:
                errors.append(f"retained build artifact changed from M0 at {phase}: {relative}")
            hashes[relative] = str(entry.snapshot["sha256"])
            states[relative] = tuple(entry.snapshot["stat_identity"])
        return dict(sorted(hashes.items())), dict(sorted(states.items()))

    def close(self) -> None:
        failures: list[str] = []
        for entry in reversed(tuple(self.entries.values())):
            try:
                entry.stream.close()
            except OSError as exc:
                failures.append(f"{entry.path}: {exc}")
        if failures:
            raise OSError("cannot close retained build artifact handles: " + "; ".join(failures))


_ACTIVE_BUILD_ARTIFACTS: ContextVar[_RetainedBuildArtifactInventory | None] = ContextVar(
    "gauge_vfe_rg_active_build_artifacts",
    default=None,
)


def _enumerate_build_artifact_paths(build_dir: Path) -> list[Path]:
    """Enumerate one exact non-reparse regular-file domain without following links."""

    component = _first_reparse_component(build_dir)
    if component is not None:
        raise OSError(f"build directory is reparse-mediated at {component}")
    root = build_dir.resolve(strict=True)
    if not root.is_dir():
        raise OSError(f"build directory is not a directory: {root}")
    discovered: list[Path] = []
    folded: dict[str, str] = {}
    for current, directories, filenames in os.walk(root, topdown=True, followlinks=False):
        directories.sort(key=str.casefold)
        filenames.sort(key=str.casefold)
        current_path = Path(current)
        for directory in tuple(directories):
            candidate = current_path / directory
            if _is_reparse_point(candidate):
                raise OSError(f"build artifact inventory contains a reparse directory: {candidate}")
        for filename in filenames:
            candidate = current_path / filename
            information = candidate.lstat()
            if not stat.S_ISREG(information.st_mode) or _is_reparse_point(candidate):
                raise OSError(f"build artifact inventory contains a non-regular file: {candidate}")
            relative = candidate.relative_to(root).as_posix()
            prior = folded.get(relative.casefold())
            if prior is not None and prior != relative:
                raise OSError(f"build artifact inventory has a case collision: {prior!r}, {relative!r}")
            folded[relative.casefold()] = relative
            discovered.append(candidate)
    return sorted(discovered, key=lambda path: path.relative_to(root).as_posix())


@contextmanager
def _retain_build_artifact_inventory(build_dir: Path):
    """Acquire the complete artifact inventory before M0 and release it after handoff."""

    entries: dict[str, _HeldBuildArtifact] = {}
    errors: list[str] = []
    try:
        root = Path(build_dir).resolve(strict=True)
    except (OSError, RuntimeError, ValueError) as exc:
        root = Path(build_dir).resolve()
        errors.append(f"cannot resolve build artifact inventory root: {exc}")
    else:
        try:
            initial_paths = _enumerate_build_artifact_paths(root)
            for path in initial_paths:
                locked_path, stream = _open_deny_write_file(path)
                try:
                    snapshot = _locked_stream_snapshot(locked_path, stream)
                    stream.seek(0)
                    payload = stream.read()
                    stream.seek(0)
                    if (
                        hashlib.sha256(payload).hexdigest() != snapshot["sha256"]
                        or len(payload) != snapshot["byte_count"]
                    ):
                        raise OSError(f"retained bytes disagree with held-handle M0: {locked_path}")
                except BaseException:
                    stream.close()
                    raise
                entries[os.path.normcase(os.path.abspath(os.fspath(locked_path)))] = _HeldBuildArtifact(
                    path=locked_path,
                    stream=stream,
                    payload=payload,
                    snapshot=snapshot,
                )
            repeated_paths = _enumerate_build_artifact_paths(root)
            if [path.relative_to(root).as_posix() for path in repeated_paths] != [
                path.relative_to(root).as_posix() for path in initial_paths
            ]:
                raise OSError("build artifact path inventory changed while M0 handles were acquired")
        except (OSError, RuntimeError, ValueError) as exc:
            errors.append(f"cannot acquire complete retained build artifact inventory: {exc}")
    inventory = _RetainedBuildArtifactInventory(root, entries, errors)
    try:
        yield inventory
    finally:
        inventory.close()


def _acquire_audit_executable_locks() -> dict[str, tuple[Path, Any, dict[str, Any]]]:
    """Acquire all executable locks transactionally, closing partial state on failure."""

    acquired: dict[str, tuple[Path, Any, dict[str, Any] | None]] = {}
    try:
        for field, path in (
            ("python_executable", _TRUSTED_PYTHON),
            ("git_executable", _TRUSTED_GIT),
        ):
            locked_path, locked_stream = _open_deny_write_file(path)
            acquired[field] = (locked_path, locked_stream, None)
            locked_snapshot = _locked_stream_snapshot(locked_path, locked_stream)
            acquired[field] = (locked_path, locked_stream, locked_snapshot)
    except BaseException:
        for _path, stream, _snapshot in reversed(tuple(acquired.values())):
            try:
                stream.close()
            except OSError:
                pass
        raise
    return {
        field: (path, stream, snapshot)
        for field, (path, stream, snapshot) in acquired.items()
        if snapshot is not None
    }


_AUDIT_EXECUTABLE_LOCKS = _acquire_audit_executable_locks()


def _cleanup_audit_executable_locks() -> None:
    """Release retained executable handles in reverse acquisition order."""

    for _path, stream, _snapshot in reversed(tuple(_AUDIT_EXECUTABLE_LOCKS.values())):
        try:
            stream.close()
        except OSError:
            pass


atexit.register(_cleanup_audit_executable_locks)


_PYPDF_ADMISSION_M0 = _bootstrap_pypdf_distribution_snapshot()
_PYPDF_PYCACHE_BASE = _bootstrap_pypdf_pycache_base()
_PYPDF_PYCACHE_ROOT = Path(
    tempfile.mkdtemp(prefix="gauge-vfe-rg-pypdf-pycache-", dir=_PYPDF_PYCACHE_BASE)
)
if _bootstrap_first_reparse_component(_PYPDF_PYCACHE_ROOT) is not None:
    raise RuntimeError("controlled pypdf pycache root is reparse-mediated")
if any(_PYPDF_PYCACHE_ROOT.iterdir()):
    raise RuntimeError("controlled pypdf pycache root was not created empty")
sys.pycache_prefix = str(_PYPDF_PYCACHE_ROOT)
sys.dont_write_bytecode = True


def _cleanup_controlled_pycache_root() -> None:
    """Remove the task-owned empty cache root when no parent handoff consumes it."""

    try:
        if _bootstrap_first_reparse_component(_PYPDF_PYCACHE_ROOT) is None:
            _PYPDF_PYCACHE_ROOT.rmdir()
    except OSError:
        pass


atexit.register(_cleanup_controlled_pycache_root)


def _assert_controlled_pycache_empty() -> None:
    """Require the retained pypdf bytecode-cache root to remain empty."""

    if _bootstrap_first_reparse_component(_PYPDF_PYCACHE_ROOT) is not None:
        raise RuntimeError("controlled pypdf pycache root became reparse-mediated")
    if any(_PYPDF_PYCACHE_ROOT.iterdir()):
        raise RuntimeError("controlled pypdf pycache root is not empty")


class _AuthenticatedSiteLoader:
    """Bind each admitted fixed-site module execution to its M0 source bytes."""

    def __init__(
        self,
        loader: Any,
        origin: Path,
        expected_file: dict[str, str | int],
        expected_identity: tuple[int, ...],
    ) -> None:
        self._loader = loader
        self._origin = origin
        self._expected_file = expected_file
        self._expected_identity = expected_identity
        self._locked_path: Path | None = None
        self._locked_stream: Any = None

    def _acquire_origin(self) -> None:
        if self._locked_stream is not None:
            return
        locked_path, locked_stream = _open_deny_write_file(self._origin)
        self._locked_path = locked_path
        self._locked_stream = locked_stream
        self._assert_origin_m0()

    def _close_origin(self) -> None:
        if self._locked_stream is not None:
            self._locked_stream.close()
            self._locked_stream = None
            self._locked_path = None

    def create_module(self, spec: Any) -> Any:
        """Delegate module allocation to the authenticated original loader."""

        self._acquire_origin()
        creator = getattr(self._loader, "create_module", None)
        try:
            return creator(spec) if creator is not None else None
        except BaseException:
            self._close_origin()
            raise

    def _assert_origin_m0(self) -> None:
        if self._locked_path is None or self._locked_stream is None:
            raise ImportError(f"authenticated fixed-site origin has no retained handle: {self._origin}")
        snapshot = _locked_stream_snapshot(self._locked_path, self._locked_stream)
        if (
            snapshot["sha256"] != self._expected_file["sha256"]
            or snapshot["byte_count"] != self._expected_file["byte_count"]
            or snapshot["stat_identity"] != self._expected_identity
        ):
            raise ImportError(
                f"authenticated fixed-site module changed from pre-import M0: {self._origin}"
            )

    def exec_module(self, module: Any) -> None:
        """Check the exact origin immediately before and after delegated execution."""

        self._acquire_origin()
        try:
            self._loader.exec_module(module)
        finally:
            try:
                self._assert_origin_m0()
                _assert_controlled_pycache_empty()
            finally:
                self._close_origin()


class _AuthenticatedSiteFinder:
    """Admit only RECORD-authenticated modules from the fixed pypdf site."""

    def __init__(self, site: Path, snapshot: dict[str, Any]) -> None:
        self._site = site.resolve(strict=True)
        self._package_root = Path(snapshot["provenance"]["pypdf_package_root"]).resolve(
            strict=True
        )
        self._preexisting_modules = frozenset(sys.modules)
        self._authenticated: dict[
            str, tuple[Path, dict[str, str | int], tuple[int, ...]]
        ] = {}
        for relative, record in snapshot["files"].items():
            origin = self._site.joinpath(*relative.split("/")).resolve(strict=True)
            normalized = os.path.normcase(str(origin))
            self._authenticated[normalized] = (
                origin,
                record,
                snapshot["file_identities"][relative],
            )

    def _under_site(self, path: Path) -> bool:
        try:
            path.relative_to(self._site)
        except ValueError:
            return False
        return True

    def find_spec(
        self,
        fullname: str,
        path: Any = None,
        target: Any = None,
    ) -> Any:
        """Block any import whose resolved fixed-site origin is unauthenticated."""

        del target
        spec = importlib.machinery.PathFinder.find_spec(fullname, path)
        if spec is None:
            return None
        origin = getattr(spec, "origin", None)
        if isinstance(origin, str) and origin not in {"built-in", "frozen"}:
            candidate = Path(origin)
            try:
                resolved = candidate.resolve(strict=True)
            except (OSError, RuntimeError):
                resolved = candidate.resolve()
            if self._under_site(resolved):
                admitted = self._authenticated.get(os.path.normcase(str(resolved)))
                if admitted is None:
                    raise ModuleNotFoundError(
                        f"fixed-site module {fullname!r} is outside the authenticated pypdf RECORD",
                        name=fullname,
                    )
                origin_path, expected_file, expected_identity = admitted
                if spec.loader is None:
                    raise ModuleNotFoundError(
                        f"fixed-site module {fullname!r} has no authenticated executable loader",
                        name=fullname,
                    )
                spec.loader = _AuthenticatedSiteLoader(
                    spec.loader,
                    origin_path,
                    expected_file,
                    expected_identity,
                )
                return spec
        locations = getattr(spec, "submodule_search_locations", None)
        if locations is not None:
            for raw_location in locations:
                location = Path(raw_location).resolve()
                if self._under_site(location) and not (
                    location == self._package_root
                    or location.is_relative_to(self._package_root)
                ):
                    raise ModuleNotFoundError(
                        f"fixed-site namespace {fullname!r} is outside the authenticated pypdf RECORD",
                        name=fullname,
                    )
        return None


def _assert_no_undeclared_fixed_site_modules(finder: _AuthenticatedSiteFinder) -> None:
    """Reject any executed fixed-site module outside the admitted RECORD set."""

    for name, module in tuple(sys.modules.items()):
        if name in finder._preexisting_modules:
            continue
        origin = getattr(module, "__file__", None)
        if not isinstance(origin, str) or not origin:
            continue
        candidate = Path(origin)
        try:
            resolved = candidate.resolve(strict=True)
        except (OSError, RuntimeError):
            continue
        if finder._under_site(resolved) and os.path.normcase(str(resolved)) not in finder._authenticated:
            raise RuntimeError(
                f"undeclared fixed-site module executed outside authenticated pypdf RECORD: {name} ({resolved})"
            )


_PYPDF_SITE_FINDER = _AuthenticatedSiteFinder(
    _TRUSTED_PYPDF_SITE,
    _PYPDF_ADMISSION_M0,
)
sys.meta_path.insert(0, _PYPDF_SITE_FINDER)
_assert_no_undeclared_fixed_site_modules(_PYPDF_SITE_FINDER)
_assert_controlled_pycache_empty()
try:
    import pypdf
except ModuleNotFoundError:
    if sys.flags.isolated != 1 or Path(sys.executable).resolve() != _TRUSTED_PYTHON.resolve():
        raise
    bootstrap_reparse = _bootstrap_first_reparse_component(_TRUSTED_PYPDF_INIT)
    if bootstrap_reparse is not None:
        raise RuntimeError(
            f"trusted isolated Python package path is reparse-mediated at {bootstrap_reparse}"
        )
    _TRUSTED_PYPDF_INIT.resolve(strict=True)
    sys.path.append(str(_TRUSTED_PYPDF_SITE))
    import pypdf

from pypdf import PdfReader

_PYPDF_IMPORTED_PATH = Path(pypdf.__file__ or "")
_pypdf_import_reparse = _bootstrap_first_reparse_component(_PYPDF_IMPORTED_PATH)
if _pypdf_import_reparse is not None:
    raise RuntimeError(f"imported pypdf path is reparse-mediated at {_pypdf_import_reparse}")
if _PYPDF_IMPORTED_PATH.resolve(strict=True) != _TRUSTED_PYPDF_INIT.resolve(strict=True):
    raise RuntimeError(
        f"pypdf must be imported from exact trusted module {_TRUSTED_PYPDF_INIT}, "
        f"not {_PYPDF_IMPORTED_PATH}"
    )
if sys.flags.isolated == 1 and "sitecustomize" in sys.modules:
    raise RuntimeError("isolated pypdf admission unexpectedly imported sitecustomize")
if getattr(pypdf, "__version__", None) != _PYPDF_ADMISSION_M0["provenance"]["pypdf"]:
    raise RuntimeError("pypdf module version disagrees with its pre-import distribution M0")
_PYPDF_POST_IMPORT = _bootstrap_pypdf_distribution_snapshot()
if _PYPDF_POST_IMPORT != _PYPDF_ADMISSION_M0:
    raise RuntimeError("trusted pypdf distribution changed during package import admission")
_assert_no_undeclared_fixed_site_modules(_PYPDF_SITE_FINDER)


_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_REVISION_RE = re.compile(r"^[0-9a-f]{40}$")
PRODUCTION_PROTOCOL_PROFILE = "gauge-vfe-rg-production-v1"
SYNTHETIC_PROTOCOL_PROFILE = "synthetic-test-fixture-v1"
_COMMAND_KEYS = frozenset(
    {
        "argv",
        "returncode",
        "tool_version",
        "executable",
        "cwd",
        "started_at_utc",
        "ended_at_utc",
        "stdout_sha256",
        "stderr_sha256",
        "stdout_artifact",
        "stderr_artifact",
        "environment",
    }
)
_BUILD_CONTEXT_KEYS = frozenset(
    {
        "protocol_profile",
        "source_revision",
        "head_revision",
        "repository_root",
        "source_directory",
        "output_directory",
        "initial_entries",
        "source_date_epoch",
        "controlled_environment",
        "locked_repository_inputs",
        "python_executable",
        "git_executable",
        "pdflatex_executable",
        "bibtex_executable",
        "build_script",
        "main_tex",
        "run_checks",
        "build_audit",
        "references_bib",
        "bibtex_style",
        "verification_result",
        "repository_build_script",
        "executed_build_script",
        "bootstrap_attestation",
        "external_input_fixed_point",
        "recorder_snapshots",
        "evidence_input_inventory",
    }
)
_CONTROLLED_TEX_ENV_KEYS = frozenset(
    {
        "TEXINPUTS",
        "BIBINPUTS",
        "BSTINPUTS",
        "TEXMFHOME",
        "TEXMFVAR",
        "TEXMFCONFIG",
        "SOURCE_DATE_EPOCH",
    }
)
_CHILD_ENV_KEYS = frozenset(
    {
        "SystemRoot",
        "WINDIR",
        "SystemDrive",
        "COMSPEC",
        "PATHEXT",
        "PATH",
        "TEMP",
        "TMP",
        *_CONTROLLED_TEX_ENV_KEYS,
    }
)
_OUTPUT_RE = re.compile(
    r"Output written on\s+(.+?)\s+\((\d+)\s+pages?,\s+(\d+)\s+bytes\)\.",
    re.IGNORECASE,
)
_SOURCE_SUFFIXES = frozenset({".tex", ".sty", ".cls", ".bst", ".bib"})
_AUXILIARY_NAMES = frozenset(
    {
        "main.aux",
        "main.bbl",
        "main.blg",
        "main.log",
        "main.toc",
        "main.out",
        "main.lof",
        "main.lot",
        "main.fls",
        "main-pass-1.fls",
        "main-pass-3.fls",
        "main-pass-4.fls",
        "main-bibtex.aux",
        "main-bibtex.blg",
        "main-bibtex.bbl",
        "main.synctex.gz",
    }
)
_AUXILIARY_SUFFIXES = (
    ".aux",
    ".bbl",
    ".blg",
    ".log",
    ".toc",
    ".out",
    ".lof",
    ".lot",
    ".fls",
    ".fdb_latexmk",
    ".synctex.gz",
)
_ALLOWED_STATUSES = frozenset(
    {
        "ESTABLISHED",
        "DEFINITION",
        "HYPOTHESIS",
        "CONJECTURE",
        "NUMERICAL",
        "OPEN",
        "NOT-CLAIMED",
    }
)
_REQUIRED_ARTIFACTS = (
    "main.log",
    "main.aux",
    "main.bbl",
    "main.toc",
    "main.pdf",
    "main.fls",
    "main.blg",
)
_PDF_METADATA_FIELDS = (
    ("title", "/Title"),
    ("author", "/Author"),
    ("subject", "/Subject"),
    ("keywords", "/Keywords"),
    ("creator", "/Creator"),
    ("producer", "/Producer"),
    ("creation_date", "/CreationDate"),
    ("modification_date", "/ModDate"),
)


@dataclass(frozen=True, slots=True)
class AuditResult:
    """Immutable audit envelope with deterministic JSON-compatible fields."""

    ok: bool
    protocol_profile: str
    source_revision: str
    errors: list[str]
    tool_versions: dict[str, str]
    inspection_tool_versions: dict[str, str]
    commands: list[dict[str, Any]]
    build_context: dict[str, Any]
    input_inventory: dict[str, Any]
    source_manifest_digest: str
    pdf_sha256: str
    pdf_byte_count: int
    page_count: int
    pdf_metadata: dict[str, str | None]
    artifact_hashes: dict[str, str]
    pages_to_render: list[int]
    changed_pages: list[int]
    duplicate_labels: list[str]
    undefined_references: list[str]
    undefined_citations: list[str]
    rerun_requests: list[str]
    fatal_errors: list[str]
    overfull_boxes: list[str]
    literal_double_question_marks: list[str]
    invalid_status_tags: list[str]
    doubled_status_tags: list[str]
    stale_auxiliary_files: list[str]

    def to_dict(self) -> dict[str, Any]:
        """Return a detached, strict-JSON-compatible representation."""

        return asdict(self)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _stat_identity(information: os.stat_result) -> tuple[int, ...]:
    return (
        information.st_dev,
        information.st_ino,
        information.st_mode,
        information.st_size,
        information.st_mtime_ns,
        information.st_ctime_ns,
        getattr(information, "st_file_attributes", 0),
    )


def _content_identity(information: os.stat_result) -> tuple[int, ...]:
    return (
        information.st_dev,
        information.st_ino,
        information.st_size,
        information.st_mtime_ns,
        getattr(information, "st_file_attributes", 0),
    )


def _open_regular_file(path: Path) -> tuple[Any, tuple[int, ...], tuple[int, ...]]:
    reparse_component = _first_reparse_component(path)
    if reparse_component is not None:
        raise OSError(f"path is reparse-mediated at {reparse_component}: {path}")
    before = path.lstat()
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    if not stat.S_ISREG(before.st_mode) or bool(
        getattr(before, "st_file_attributes", 0) & reparse_flag
    ):
        raise OSError(f"not a regular non-reparse file: {path}")
    stream = path.open("rb")
    opened = os.fstat(stream.fileno())
    if _content_identity(before) != _content_identity(opened):
        stream.close()
        raise OSError(f"file identity changed while opening: {path}")
    return stream, _stat_identity(before), _content_identity(opened)


def _read_bytes_stable(path: Path) -> tuple[bytes, tuple[int, ...]]:
    active = _ACTIVE_BUILD_ARTIFACTS.get()
    if active is not None and active.contains_path(path):
        return active.read(path)
    stream, path_identity, opened_identity = _open_regular_file(path)
    try:
        data = stream.read()
        after_read = _content_identity(os.fstat(stream.fileno()))
    finally:
        stream.close()
    after_close = _stat_identity(path.lstat())
    if opened_identity != after_read or path_identity != after_close:
        raise OSError(f"file changed during stable read: {path}")
    return data, path_identity


def _sha256_file_with_identity(path: Path) -> tuple[str, int, tuple[int, ...]]:
    active = _ACTIVE_BUILD_ARTIFACTS.get()
    if active is not None and active.contains_path(path):
        payload, identity = active.read(path)
        return hashlib.sha256(payload).hexdigest(), len(payload), identity
    stream, path_identity, opened_identity = _open_regular_file(path)
    digest = hashlib.sha256()
    byte_count = 0
    try:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
            byte_count += len(block)
        after_read = _content_identity(os.fstat(stream.fileno()))
    finally:
        stream.close()
    after_close = _stat_identity(path.lstat())
    if (
        opened_identity != after_read
        or path_identity != after_close
        or byte_count != path_identity[3]
    ):
        raise OSError(f"file changed during stable hashing: {path}")
    return digest.hexdigest(), byte_count, path_identity


def _sha256_file(path: Path) -> str:
    return _sha256_file_with_identity(path)[0]


def _trusted_executable_snapshot(
    path: Path,
) -> tuple[dict[str, str | int], tuple[int, ...]]:
    """Capture a fixed executable's raw bytes and filesystem identity."""

    component = _first_reparse_component(path)
    if component is not None:
        raise OSError(f"trusted executable path is reparse-mediated at {component}")
    resolved = path.resolve(strict=True)
    digest, byte_count, identity = _sha256_file_with_identity(resolved)
    return (
        {"path": str(resolved), "sha256": digest, "byte_count": byte_count},
        identity,
    )


def _require_production_cli_runtime() -> str:
    """Require the exact isolated Python runtime and return its stable digest M0."""

    if sys.flags.isolated != 1:
        raise SystemExit("build_audit.py production CLI requires isolated Python mode (-I)")
    if sys.flags.no_site != 1:
        raise SystemExit("build_audit.py production CLI requires disabled site startup (-S)")
    try:
        executable = Path(sys.executable).resolve(strict=True)
        expected = _TRUSTED_PYTHON.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise SystemExit(f"cannot resolve trusted Python runtime: {exc}") from exc
    if executable != expected:
        raise SystemExit(
            f"build_audit.py production CLI requires exact Python executable {_TRUSTED_PYTHON}"
        )
    component = _first_reparse_component(Path(sys.executable))
    if component is not None:
        raise SystemExit(f"trusted Python runtime path is reparse-mediated at {component}")
    try:
        digest = _sha256_file(executable)
    except OSError as exc:
        raise SystemExit(f"cannot hash trusted Python runtime stably: {exc}") from exc
    locked_path, locked_stream, locked_m0 = _AUDIT_EXECUTABLE_LOCKS["python_executable"]
    _assert_locked_stream_m0(locked_path, locked_stream, locked_m0, "trusted Python")
    if digest != locked_m0["sha256"]:
        raise SystemExit("trusted Python path bytes do not equal retained launch-handle M0")
    return digest


def _strict_json_load(path: Path) -> Any:
    def reject_constant(value: str) -> Any:
        raise ValueError(f"nonfinite JSON constant {value!r} is forbidden")

    def finite_float(value: str) -> float:
        parsed = float(value)
        if not math.isfinite(parsed):
            raise ValueError(f"JSON number {value!r} overflows to a nonfinite value")
        return parsed

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON object key {key!r} is forbidden")
            result[key] = value
        return result

    raw, _identity = _read_bytes_stable(path)
    text = raw.decode("utf-8")
    return json.loads(
        text,
        parse_constant=reject_constant,
        parse_float=finite_float,
        object_pairs_hook=unique_object,
    )


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def validate_bootstrap_receipt(
    receipt_path: Path,
    expected_receipt_sha256: str,
    *,
    expected_transport_sha256: str,
    expected_transport_byte_count: int,
    expected_mode: str,
    expected_repository_root: Path | str,
    expected_source_revision: str,
    expected_receipt_path: Path | str,
    expected_source_directory: Path | str,
    expected_output_directory: Path | str,
    expected_audit_path: Path | str,
    expected_verification_result: Path | str,
    expected_verification_report: Path | str,
    expected_pdflatex_path: Path | str,
    expected_bibtex_path: Path | str,
    expected_bibtex_style_path: Path | str,
) -> dict[str, Any]:
    """Validate one accepted bootstrap receipt against independent launch inputs.

    The receipt cannot authenticate its own transport assertion.  Callers must
    therefore supply the prelaunch transport digest and byte count separately.
    The emitted receipt digest similarly arrives over the parent process
    channel and is checked before any receipt field is trusted.
    """

    digest_pattern = re.compile(r"[0-9a-f]{64}\Z")
    oid_pattern = re.compile(r"[0-9a-f]{40}\Z")
    uuid4_pattern = re.compile(r"[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}\Z")

    if digest_pattern.fullmatch(expected_receipt_sha256) is None:
        raise ValueError("expected receipt digest must be lowercase SHA-256")
    if digest_pattern.fullmatch(expected_transport_sha256) is None:
        raise ValueError("expected transport digest must be lowercase SHA-256")
    if type(expected_transport_byte_count) is not int or expected_transport_byte_count <= 0:
        raise ValueError("expected transport byte count must be a positive integer")
    if expected_mode not in {"Build", "NumericalUpdate", "NumericalVerify"}:
        raise ValueError("expected bootstrap mode is invalid")
    if _REVISION_RE.fullmatch(expected_source_revision) is None:
        raise ValueError("expected source revision must be lowercase SHA-1")

    def expected_absolute(value: Path | str, label: str, *, allow_empty: bool = False) -> str:
        raw_value = os.fspath(value)
        if allow_empty and raw_value == "":
            return ""
        path = Path(raw_value)
        if not path.is_absolute():
            raise ValueError(f"{label} must be an independently supplied absolute path")
        return str(path.resolve())

    expected_repository = expected_absolute(expected_repository_root, "expected repository root")
    expected_receipt = expected_absolute(expected_receipt_path, "expected receipt path")
    expected_source = expected_absolute(expected_source_directory, "expected source directory")
    expected_output = expected_absolute(
        expected_output_directory,
        "expected output directory",
        allow_empty=expected_mode != "Build",
    )
    expected_audit = expected_absolute(
        expected_audit_path,
        "expected audit path",
        allow_empty=expected_mode != "Build",
    )
    expected_result = expected_absolute(expected_verification_result, "expected verification result")
    expected_report = expected_absolute(expected_verification_report, "expected verification report")
    expected_pdflatex = expected_absolute(
        expected_pdflatex_path,
        "expected pdflatex path",
        allow_empty=expected_mode != "Build",
    )
    expected_bibtex = expected_absolute(
        expected_bibtex_path,
        "expected bibtex path",
        allow_empty=expected_mode != "Build",
    )
    expected_style = expected_absolute(
        expected_bibtex_style_path,
        "expected BibTeX style path",
        allow_empty=expected_mode != "Build",
    )
    if expected_mode == "Build" and any(
        value == ""
        for value in (expected_output, expected_audit, expected_pdflatex, expected_bibtex, expected_style)
    ):
        raise ValueError("Build receipt validation requires every independent build-only path")
    if expected_mode != "Build" and any(
        os.fspath(value) != ""
        for value in (
            expected_output_directory,
            expected_audit_path,
            expected_pdflatex_path,
            expected_bibtex_path,
            expected_bibtex_style_path,
        )
    ):
        raise ValueError("numerical receipt validation requires empty build-only expected paths")

    receipt_path = Path(receipt_path).resolve()
    if str(receipt_path) != expected_receipt:
        raise ValueError("receipt path differs from the independent launch value")
    raw, _receipt_identity = _read_bytes_stable(receipt_path)
    actual_receipt_sha256 = hashlib.sha256(raw).hexdigest()
    if actual_receipt_sha256 != expected_receipt_sha256:
        raise ValueError("bootstrap receipt digest does not equal the parent-channel digest")

    def reject_constant(value: str) -> Any:
        raise ValueError(f"nonfinite JSON constant {value!r} is forbidden")

    def finite_float(value: str) -> float:
        parsed = float(value)
        if not math.isfinite(parsed):
            raise ValueError(f"JSON number {value!r} overflows to a nonfinite value")
        return parsed

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON object key {key!r} is forbidden")
            result[key] = value
        return result

    try:
        document = json.loads(
            raw.decode("utf-8", errors="strict"),
            parse_constant=reject_constant,
            parse_float=finite_float,
            object_pairs_hook=unique_object,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"bootstrap receipt is not strict JSON: {exc}") from exc
    if not isinstance(document, dict):
        raise ValueError("bootstrap receipt must contain one JSON object")

    def require_exact(value: Any, keys: set[str], label: str) -> dict[str, Any]:
        if not isinstance(value, dict) or set(value) != keys:
            raise ValueError(f"{label} does not have the exact required property set")
        return value

    require_exact(
        document,
        {
            "schema_version",
            "protocol_profile",
            "approved_transport_sha256",
            "approved_transport_byte_count",
            "outer_argv",
            "mode",
            "accepted",
            "source_revision",
            "repository_root",
            "source_directory",
            "temporary_directory",
            "repository_source",
            "executed_source",
            "bootstrap_attestation",
            "tool_identities",
            "git_metadata_root_binding",
            "git_metadata_m0",
            "child",
            "m1",
            "cleanup",
            "fresh_targets",
            "outputs",
            "error",
        },
        "bootstrap receipt",
    )
    if document["schema_version"] != "gauge-vfe-bootstrap-receipt-v1":
        raise ValueError("bootstrap receipt schema version is unsupported")
    if document["protocol_profile"] != "gauge-vfe-rg-production-v1":
        raise ValueError("bootstrap receipt protocol profile is invalid")
    if document["approved_transport_sha256"] != expected_transport_sha256:
        raise ValueError("receipt transport digest differs from the independent prelaunch digest")
    if document["approved_transport_byte_count"] != expected_transport_byte_count:
        raise ValueError("receipt transport byte count differs from the independent prelaunch count")
    if document["accepted"] is not True or document["error"] is not None:
        raise ValueError("bootstrap receipt is not an accepted success receipt")
    mode = document["mode"]
    if mode not in {"Build", "NumericalUpdate", "NumericalVerify"}:
        raise ValueError("bootstrap receipt mode is invalid")
    if mode != expected_mode:
        raise ValueError("bootstrap receipt mode differs from the independent launch value")
    if oid_pattern.fullmatch(str(document["source_revision"])) is None:
        raise ValueError("bootstrap receipt source revision is invalid")
    if document["source_revision"] != expected_source_revision:
        raise ValueError("bootstrap receipt source revision differs from the independent launch value")
    if document["repository_root"] != expected_repository:
        raise ValueError("bootstrap receipt repository root differs from the independent launch value")
    if document["source_directory"] != expected_source:
        raise ValueError("bootstrap receipt source directory differs from the independent launch value")
    for path_value, label, require_directory in (
        (expected_repository, "repository root", True),
        (expected_source, "source directory", True),
    ):
        path = Path(path_value)
        if (
            _first_reparse_component(path) is not None
            or (require_directory and not path.is_dir())
        ):
            raise ValueError(f"bootstrap receipt {label} is not a current non-reparse directory")
    expected_source_from_repository = Path(expected_repository) / "manuscripts" / "gauge_vfe_rg"
    if Path(expected_source) != expected_source_from_repository:
        raise ValueError("independent source directory is not the exact repository manuscript directory")
    expected_outer_argv = [
        r"C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe",
        "-NoProfile",
        "-NonInteractive",
        "-Command",
        "-",
    ]
    if document["outer_argv"] != expected_outer_argv:
        raise ValueError("bootstrap receipt outer argv is not the approved exact invocation")
    metadata_binding = require_exact(
        document["git_metadata_root_binding"],
        {"repository_root", "git_directory", "common_directory"},
        "Git metadata-root binding",
    )
    if metadata_binding["repository_root"] != document["repository_root"] or any(
        not isinstance(metadata_binding[field], str)
        or not Path(metadata_binding[field]).is_absolute()
        for field in ("repository_root", "git_directory", "common_directory")
    ):
        raise ValueError("Git metadata-root binding is invalid")
    metadata_errors: list[str] = []
    current_metadata_directories = _git_metadata_directories(
        Path(expected_repository), metadata_errors
    )
    if metadata_errors or not current_metadata_directories:
        raise ValueError(
            "cannot independently resolve current Git metadata roots: "
            + "; ".join(metadata_errors)
        )
    current_git_directory = current_metadata_directories[0]
    current_common_directory = current_metadata_directories[-1]
    if (
        metadata_binding["git_directory"] != str(current_git_directory)
        or metadata_binding["common_directory"] != str(current_common_directory)
    ):
        raise ValueError("Git metadata-root binding differs from the current repository roots")
    current_head_process = _git(
        Path(expected_repository), "rev-parse", "--verify", "HEAD^{commit}"
    )
    current_head = current_head_process.stdout.decode("ascii", errors="replace").strip()
    if current_head_process.returncode != 0 or oid_pattern.fullmatch(current_head) is None:
        raise ValueError("cannot independently resolve the current repository HEAD commit")
    ancestry = _git(
        Path(expected_repository),
        "merge-base",
        "--is-ancestor",
        expected_source_revision,
        current_head,
    )
    if ancestry.returncode != 0:
        raise ValueError("expected source revision is not an ancestor of current repository HEAD")

    cleanup = require_exact(document["cleanup"], {"completed", "error"}, "cleanup record")
    if cleanup != {"completed": True, "error": None}:
        raise ValueError("bootstrap cleanup did not complete without error")
    m1 = require_exact(
        document["m1"],
        {
            "completed",
            "error",
            "git_metadata",
            "temporary_directory_m0",
            "temporary_directory_m1",
            "output_directory_m0",
            "output_directory_m1",
        },
        "M1 record",
    )
    if m1["completed"] is not True or m1["error"] is not None:
        raise ValueError("bootstrap M1 did not complete without error")
    temporary_directory = Path(str(document["temporary_directory"]))
    if not temporary_directory.is_absolute() or temporary_directory.exists():
        raise ValueError("bootstrap temporary directory was not removed after M1")

    identity_keys = {"path", "final_path", "sha256", "byte_count", "handle_identity"}

    def require_identity(value: Any, label: str, *, bind_current: bool) -> dict[str, Any]:
        record = require_exact(value, identity_keys, label)
        path_value = record["path"]
        if not isinstance(path_value, str) or not Path(path_value).is_absolute():
            raise ValueError(f"{label}.path must be absolute")
        if digest_pattern.fullmatch(str(record["sha256"])) is None:
            raise ValueError(f"{label}.sha256 is invalid")
        if type(record["byte_count"]) is not int or record["byte_count"] < 0:
            raise ValueError(f"{label}.byte_count is invalid")
        if (
            not isinstance(record["final_path"], str)
            or not isinstance(record["handle_identity"], list)
            or len(record["handle_identity"]) != 7
            or not all(isinstance(item, str) for item in record["handle_identity"])
        ):
            raise ValueError(f"{label} has an invalid held-handle identity")
        if os.path.normcase(os.path.normpath(record["final_path"])) != os.path.normcase(
            os.path.normpath(path_value)
        ):
            raise ValueError(f"{label}.final_path does not equal its exact lexical path")
        if bind_current:
            path = Path(path_value)
            component = _first_reparse_component(path)
            if component is not None:
                raise ValueError(f"{label}.path is reparse-mediated at {component}")
            payload, _identity = _read_bytes_stable(path)
            if len(payload) != record["byte_count"] or hashlib.sha256(payload).hexdigest() != record["sha256"]:
                raise ValueError(f"{label} no longer equals its receipt raw-byte identity")
        return record

    tool_identities = document["tool_identities"]
    expected_tool_paths = {
        "powershell": r"C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe",
        "git": str(_TRUSTED_GIT),
        "python": str(_TRUSTED_PYTHON),
        **(
            {
                "pdflatex": expected_pdflatex,
                "bibtex": expected_bibtex,
                "plainnat": expected_style,
            }
            if mode == "Build"
            else {}
        ),
    }
    require_exact(tool_identities, set(expected_tool_paths), "bootstrap tool identities")
    validated_tools: dict[str, dict[str, Any]] = {}
    for name, expected_path in expected_tool_paths.items():
        identity = require_identity(
            tool_identities[name],
            f"bootstrap tool {name}",
            bind_current=True,
        )
        if identity["path"] != expected_path:
            raise ValueError(f"bootstrap tool {name} differs from the independent launch path")
        validated_tools[name] = identity

    if m1["git_metadata"] != document["git_metadata_m0"]:
        raise ValueError("bootstrap Git metadata differs between M0 and M1")
    metadata_m0 = document["git_metadata_m0"]
    if not isinstance(metadata_m0, list) or not metadata_m0:
        raise ValueError("bootstrap Git metadata M0 must be one nonempty record list")
    metadata_roots = []
    for field in ("git_directory", "common_directory"):
        root = Path(metadata_binding[field])
        if root not in metadata_roots:
            metadata_roots.append(root)
    guarded_relatives = (
        Path("info") / "grafts",
        Path("shallow"),
        Path("objects") / "info" / "alternates",
        Path("objects") / "info" / "http-alternates",
        Path("refs") / "replace",
    )
    expected_metadata_paths = {
        str(Path(expected_repository) / ".git"),
        *(
            str(root / relative)
            for root in metadata_roots
            for relative in guarded_relatives
        ),
    }
    observed_metadata_paths: set[str] = set()
    for index, value in enumerate(metadata_m0):
        if not isinstance(value, dict):
            raise ValueError(f"Git metadata M0 record {index} is not an object")
        path_value = value.get("path")
        kind = value.get("kind")
        if not isinstance(path_value, str) or path_value in observed_metadata_paths:
            raise ValueError("Git metadata M0 contains an invalid or duplicate path")
        observed_metadata_paths.add(path_value)
        if kind == "absent":
            require_exact(value, {"path", "kind"}, "absent Git metadata record")
            if Path(path_value).exists():
                raise ValueError(f"Git metadata path recorded absent now exists: {path_value}")
        elif kind == "directory":
            require_exact(
                value,
                {"path", "kind", "final_path", "stable_handle_identity"},
                "worktree Git directory record",
            )
            if path_value != str(Path(expected_repository) / ".git") or not Path(path_value).is_dir():
                raise ValueError("Git directory record does not bind the repository .git directory")
            if os.path.normcase(value["final_path"]) != os.path.normcase(path_value):
                raise ValueError("Git directory record final path differs from its lexical path")
        elif kind == "link-file":
            require_exact(
                value,
                {
                    "path",
                    "kind",
                    "final_path",
                    "sha256",
                    "byte_count",
                    "stable_handle_identity",
                },
                "worktree Git link-file record",
            )
            if path_value != str(Path(expected_repository) / ".git"):
                raise ValueError("Git link-file record does not bind the repository .git marker")
            if os.path.normcase(value["final_path"]) != os.path.normcase(path_value):
                raise ValueError("Git link-file record final path differs from its lexical path")
            payload, _identity = _read_bytes_stable(Path(path_value))
            if (
                value["sha256"] != hashlib.sha256(payload).hexdigest()
                or value["byte_count"] != len(payload)
            ):
                raise ValueError("Git link-file record does not equal current raw bytes")
        elif kind in {"empty-directory", "empty-file"}:
            required = {
                "path",
                "kind",
                "attributes",
                "creation_time_utc_ticks",
                "last_write_time_utc_ticks",
            }
            if kind == "empty-file":
                required.add("byte_count")
            require_exact(value, required, f"{kind} Git metadata record")
            path = Path(path_value)
            if kind == "empty-directory":
                if not path.is_dir() or any(path.iterdir()):
                    raise ValueError(f"Git metadata directory is not empty: {path_value}")
            elif not path.is_file() or path.stat().st_size != 0 or value["byte_count"] != 0:
                raise ValueError(f"Git metadata file is not empty: {path_value}")
            if any(
                isinstance(value[field], bool) or not isinstance(value[field], int)
                for field in ("attributes", "creation_time_utc_ticks", "last_write_time_utc_ticks")
            ):
                raise ValueError(f"{kind} Git metadata record has invalid typed metadata")
            information = path.stat()
            expected_creation_ticks = information.st_ctime_ns // 100 + 116_444_736_000_000_000
            expected_write_ticks = information.st_mtime_ns // 100 + 116_444_736_000_000_000
            if (
                value["attributes"] != getattr(information, "st_file_attributes", 0)
                or value["creation_time_utc_ticks"] != expected_creation_ticks
                or value["last_write_time_utc_ticks"] != expected_write_ticks
            ):
                raise ValueError(f"{kind} Git metadata record differs from current filesystem metadata")
        else:
            raise ValueError(f"Git metadata M0 record has unsupported kind: {kind!r}")
        if "stable_handle_identity" in value and (
            not isinstance(value["stable_handle_identity"], list)
            or len(value["stable_handle_identity"]) != 2
            or not all(isinstance(item, str) for item in value["stable_handle_identity"])
        ):
            raise ValueError("Git metadata M0 record has an invalid stable handle identity")
    if observed_metadata_paths != expected_metadata_paths:
        raise ValueError("Git metadata M0 does not cover the exact repository override-path domain")

    temporary_m0 = require_exact(
        m1["temporary_directory_m0"],
        {"final_path", "handle_identity"},
        "temporary-directory M0",
    )
    temporary_m1 = require_exact(
        m1["temporary_directory_m1"],
        {"final_path", "handle_identity"},
        "temporary-directory M1",
    )
    if (
        temporary_m0["final_path"] != document["temporary_directory"]
        or temporary_m1["final_path"] != temporary_m0["final_path"]
        or not isinstance(temporary_m0["handle_identity"], list)
        or not isinstance(temporary_m1["handle_identity"], list)
        or len(temporary_m0["handle_identity"]) != 7
        or len(temporary_m1["handle_identity"]) != 7
        or not all(isinstance(item, str) for item in temporary_m0["handle_identity"])
        or not all(isinstance(item, str) for item in temporary_m1["handle_identity"])
        or temporary_m0["handle_identity"][:2] != temporary_m1["handle_identity"][:2]
    ):
        raise ValueError("bootstrap temporary-directory identity is inconsistent across M0/M1")

    child = require_exact(
        document["child"],
        {
            "argv",
            "exit_code",
            "stdout",
            "stderr",
            "stdout_base64",
            "stderr_base64",
            "stdout_sha256",
            "stderr_sha256",
            "stdout_byte_count",
            "stderr_byte_count",
            "stdin_sha256",
            "stdin_byte_count",
            "started_at_utc",
            "ended_at_utc",
        },
        "child record",
    )
    if child["exit_code"] != 0:
        raise ValueError("bootstrap child did not exit successfully")
    try:
        stdout_bytes = base64.b64decode(child["stdout_base64"], validate=True)
        stderr_bytes = base64.b64decode(child["stderr_base64"], validate=True)
    except (TypeError, ValueError) as exc:
        raise ValueError("bootstrap child stream evidence is not strict base64") from exc
    for name, payload in (("stdout", stdout_bytes), ("stderr", stderr_bytes)):
        if child[f"{name}_byte_count"] != len(payload):
            raise ValueError(f"bootstrap child {name} byte count is inconsistent")
        if child[f"{name}_sha256"] != hashlib.sha256(payload).hexdigest():
            raise ValueError(f"bootstrap child {name} digest is inconsistent")
        try:
            decoded = payload.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ValueError(f"bootstrap child {name} is not strict UTF-8") from exc
        if child[name] != decoded:
            raise ValueError(f"bootstrap child {name} text does not equal retained raw bytes")
    if stderr_bytes:
        raise ValueError("accepted bootstrap child has nonempty stderr")
    try:
        started_at = datetime.fromisoformat(str(child["started_at_utc"]).replace("Z", "+00:00"))
        ended_at = datetime.fromisoformat(str(child["ended_at_utc"]).replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("bootstrap child timestamps are not ISO-8601") from exc
    if started_at.tzinfo is None or ended_at.tzinfo is None or ended_at < started_at:
        raise ValueError("bootstrap child timestamps are not ordered timezone-aware instants")

    outputs = require_exact(
        document["outputs"],
        (
            {
                "verification_result",
                "verification_report",
                "audit_path",
                "output_directory",
                "build_evidence",
                "artifact_hashes",
                "transaction_receipt_id",
            }
            if mode == "Build"
            else {"verification_result", "verification_report", "transaction_receipt_id"}
        ),
        "bootstrap outputs",
    )
    result_identity = require_identity(outputs["verification_result"], "verification result", bind_current=True)
    report_identity = require_identity(outputs["verification_report"], "verification report", bind_current=True)
    if result_identity["path"] != expected_result:
        raise ValueError("verification result path differs from the independent launch value")
    if report_identity["path"] != expected_report:
        raise ValueError("verification report path differs from the independent launch value")
    report_path = Path(report_identity["path"])
    report_bytes, _report_fs_identity = _read_bytes_stable(report_path)
    report = _strict_json_load(report_path)
    report_keys = {
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
    require_exact(report, report_keys, "verification report")
    if report_bytes != _canonical_json_bytes(report):
        raise ValueError("verification report bytes are not canonical JSON")
    receipt_id = outputs["transaction_receipt_id"]
    if not isinstance(receipt_id, str) or uuid4_pattern.fullmatch(receipt_id) is None:
        raise ValueError("bootstrap transaction receipt is not lowercase UUID4 hex")
    if (
        report["ok"] is not True
        or report["input_unchanged"] is not True
        or report["issues"] != []
        or report["protocol_profile"] != document["protocol_profile"]
        or report["source_revision"] != document["source_revision"]
        or report["head_revision"] != current_head
        or report["result_path"] != result_identity["path"]
        or report["transaction_receipt_id"] != receipt_id
        or any(
            report[field] != result_identity["sha256"]
            for field in (
                "input_sha256_before",
                "input_sha256_after",
                "published_result_sha256",
            )
        )
    ):
        raise ValueError("verification report does not bind the accepted receipt outputs")
    if (
        isinstance(report["manifest_path_count"], bool)
        or not isinstance(report["manifest_path_count"], int)
        or report["manifest_path_count"] < 1
        or isinstance(report["check_count"], bool)
        or not isinstance(report["check_count"], int)
        or report["check_count"] < 1
        or digest_pattern.fullmatch(str(report["semantic_payload_digest"])) is None
        or report["python_executable"] != validated_tools["python"]["path"]
        or report["python_executable_sha256"] != validated_tools["python"]["sha256"]
        or report["git_executable"] != validated_tools["git"]["path"]
        or report["git_executable_sha256"] != validated_tools["git"]["sha256"]
    ):
        raise ValueError("verification report tool, count, or semantic identity fields are invalid")

    fresh_targets = document["fresh_targets"]
    expected_fresh_keys = (
        {"verification_report", "audit_path", "output_directory"}
        if mode == "Build"
        else {"verification_report"}
    )
    require_exact(fresh_targets, expected_fresh_keys, "fresh-target record")
    report_target = require_exact(
        fresh_targets["verification_report"],
        {"path", "initial_state", "created"},
        "verification-report fresh target",
    )
    if report_target != {
        "path": report_identity["path"],
        "initial_state": "absent",
        "created": True,
    }:
        raise ValueError("verification report was not bound as one fresh created target")

    repository_source = document["repository_source"]
    executed_source = document["executed_source"]
    if mode == "Build":
        require_exact(
            repository_source,
            {"path", "relative_path", "git_blob_oid", "git_blob_byte_count"},
            "repository source",
        )
        expected_repository_script = str(Path(expected_source) / "build.ps1")
        if (
            repository_source["path"] != expected_repository_script
            or repository_source["relative_path"] != "manuscripts/gauge_vfe_rg/build.ps1"
            or oid_pattern.fullmatch(str(repository_source["git_blob_oid"])) is None
            or type(repository_source["git_blob_byte_count"]) is not int
            or repository_source["git_blob_byte_count"] <= 0
        ):
            raise ValueError("repository build source is not the exact independently expected Git blob")
        source_process = _git(
            Path(expected_repository),
            "show",
            f"{expected_source_revision}:manuscripts/gauge_vfe_rg/build.ps1",
        )
        if source_process.returncode != 0:
            raise ValueError("cannot independently materialize the repository build source")
        source_bytes = source_process.stdout
        source_blob_oid = hashlib.sha1(
            b"blob " + str(len(source_bytes)).encode("ascii") + b"\0" + source_bytes
        ).hexdigest()
        if (
            source_blob_oid != repository_source["git_blob_oid"]
            or len(source_bytes) != repository_source["git_blob_byte_count"]
        ):
            raise ValueError("repository build source receipt identity differs from Git raw bytes")
        executed = require_identity(
            {key: executed_source[key] for key in identity_keys},
            "executed source",
            bind_current=False,
        )
        if set(executed_source) != identity_keys | {"git_blob_oid"}:
            raise ValueError("executed source does not have the exact build property set")
        if (
            repository_source["relative_path"] != "manuscripts/gauge_vfe_rg/build.ps1"
            or repository_source["path"] == executed["path"]
            or repository_source["git_blob_oid"] != executed_source["git_blob_oid"]
            or repository_source["git_blob_byte_count"] != executed["byte_count"]
            or repository_source["git_blob_oid"] is None
            or executed["sha256"] != hashlib.sha256(source_bytes).hexdigest()
        ):
            raise ValueError("repository and executed build sources are not distinctly Git-bound")
        attestation_identity = require_identity(
            document["bootstrap_attestation"],
            "bootstrap attestation",
            bind_current=False,
        )
        if child["argv"] != [
            expected_outer_argv[0],
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            "-",
        ]:
            raise ValueError("build child argv is not the exact in-memory invocation")
        encoded_source = base64.b64encode(source_bytes).decode("ascii")
        child_transport = (
            "& ([ScriptBlock]::Create([Text.UTF8Encoding]::new($false,$true).GetString("
            f"[Convert]::FromBase64String('{encoded_source}')))) "
            "$env:GAUGE_VFE_BUILD_REPOSITORY_ROOT $env:GAUGE_VFE_BUILD_SOURCE_DIRECTORY "
            "$env:GAUGE_VFE_BUILD_REPOSITORY_BUILD_SCRIPT $env:GAUGE_VFE_BUILD_EXECUTED_BUILD_SCRIPT "
            "$env:GAUGE_VFE_BUILD_BOOTSTRAP_ATTESTATION_PATH $env:GAUGE_VFE_BUILD_OUTPUT_DIRECTORY "
            "$env:GAUGE_VFE_BUILD_AUDIT_PATH $env:GAUGE_VFE_BUILD_SOURCE_REVISION "
            "$env:GAUGE_VFE_BUILD_VERIFICATION_RESULT $env:GAUGE_VFE_BUILD_VERIFICATION_REPORT "
            "$env:GAUGE_VFE_BUILD_PDFLATEX_PATH $env:GAUGE_VFE_BUILD_BIBTEX_PATH "
            "$env:GAUGE_VFE_BUILD_BIBTEX_STYLE_PATH\n"
        ).encode("ascii")
        if (
            child["stdin_sha256"] != hashlib.sha256(child_transport).hexdigest()
            or child["stdin_byte_count"] != len(child_transport)
        ):
            raise ValueError("build child stdin payload does not equal the exact Git-source transport")
        audit_identity = require_identity(outputs["audit_path"], "build audit", bind_current=True)
        if audit_identity["path"] != expected_audit:
            raise ValueError("build audit path differs from the independent launch value")
        if stdout_bytes.splitlines() != [
            f"BUILD_AUDIT_SHA256={audit_identity['sha256']}".encode("ascii"),
            f"BUILD_VERIFICATION_REPORT_SHA256={report_identity['sha256']}".encode("ascii"),
        ]:
            raise ValueError("build child stdout digest handoff is inconsistent")
        audit_document = _strict_json_load(Path(audit_identity["path"]))
        if not isinstance(audit_document, dict) or not isinstance(audit_document.get("build_context"), dict):
            raise ValueError("build audit does not contain one typed build context")
        build_evidence = require_exact(
            outputs["build_evidence"],
            {
                "external_input_fixed_point",
                "recorder_snapshots",
                "evidence_input_inventory",
            },
            "receipt build evidence",
        )
        if any(
            build_evidence[field] != audit_document["build_context"].get(field)
            for field in build_evidence
        ):
            raise ValueError("receipt build evidence does not equal the retained build audit context")
        for field, receipt_value in (
            ("repository_build_script", {
                "path": repository_source["path"],
                "sha256": executed["sha256"],
                "byte_count": executed["byte_count"],
            }),
            ("executed_build_script", {
                "path": executed["path"],
                "sha256": executed["sha256"],
                "byte_count": executed["byte_count"],
            }),
            ("bootstrap_attestation", {
                "path": attestation_identity["path"],
                "sha256": attestation_identity["sha256"],
                "byte_count": attestation_identity["byte_count"],
            }),
        ):
            if audit_document["build_context"].get(field) != receipt_value:
                raise ValueError(f"build audit context does not bind receipt {field}")
        audit_target = require_exact(
            fresh_targets["audit_path"],
            {"path", "initial_state", "created"},
            "audit fresh target",
        )
        if audit_target != {"path": audit_identity["path"], "initial_state": "absent", "created": True}:
            raise ValueError("build audit was not bound as one fresh created target")
        output_directory = require_exact(
            outputs["output_directory"],
            {"path", "final_path", "handle_identity"},
            "output-directory identity",
        )
        output_path = Path(str(output_directory["path"]))
        if not output_path.is_absolute() or not output_path.is_dir() or _first_reparse_component(output_path) is not None:
            raise ValueError("output directory is not a regular absolute non-reparse directory")
        if str(output_path) != expected_output:
            raise ValueError("build output directory differs from the independent launch value")
        output_m0 = require_exact(
            m1["output_directory_m0"],
            {"path", "final_path", "handle_identity"},
            "output-directory M0",
        )
        output_m1 = require_exact(
            m1["output_directory_m1"],
            {"path", "final_path", "handle_identity"},
            "output-directory M1",
        )
        if (
            output_m0 != output_directory
            or output_m1["path"] != output_m0["path"]
            or output_m1["final_path"] != output_m0["final_path"]
            or not isinstance(output_m0["handle_identity"], list)
            or not isinstance(output_m1["handle_identity"], list)
            or len(output_m0["handle_identity"]) != 7
            or len(output_m1["handle_identity"]) != 7
            or not all(isinstance(item, str) for item in output_m0["handle_identity"])
            or not all(isinstance(item, str) for item in output_m1["handle_identity"])
            or output_m0["handle_identity"][:2] != output_m1["handle_identity"][:2]
        ):
            raise ValueError("build output-directory identity is inconsistent across M0/M1")
        output_target = require_exact(
            fresh_targets["output_directory"],
            {"path", "initial_state", "created"},
            "output-directory fresh target",
        )
        if (
            output_target["path"] != output_directory["path"]
            or output_target["initial_state"] not in {"absent", "empty-directory"}
            or output_target["created"] is not (output_target["initial_state"] == "absent")
        ):
            raise ValueError("output-directory creation outcome is inconsistent")
        audit_artifacts = audit_document.get("artifact_hashes")
        receipt_artifacts = outputs["artifact_hashes"]
        if not isinstance(audit_artifacts, dict) or not isinstance(receipt_artifacts, dict):
            raise ValueError("build artifact hashes must be exact JSON objects")
        if list(audit_artifacts) != sorted(audit_artifacts) or set(receipt_artifacts) != set(audit_artifacts):
            raise ValueError("receipt build artifact set does not equal sorted audit artifact_hashes")
        discovered: list[str] = []
        for candidate in sorted(output_path.rglob("*")):
            component = _first_reparse_component(candidate)
            if component is not None:
                raise ValueError(f"build output inventory is reparse-mediated at {component}")
            if candidate.is_file():
                discovered.append(candidate.relative_to(output_path).as_posix())
        discovered.sort()
        if discovered != list(audit_artifacts):
            raise ValueError("current build output regular-file set differs from audit artifact_hashes")
        for relative, declared_digest in audit_artifacts.items():
            pure = PurePosixPath(relative)
            if (
                not relative
                or pure.is_absolute()
                or "\\" in relative
                or any(part in {"", ".", ".."} or ":" in part for part in pure.parts)
                or digest_pattern.fullmatch(str(declared_digest)) is None
            ):
                raise ValueError(f"invalid build artifact path or digest: {relative!r}")
            record = require_identity(
                receipt_artifacts[relative],
                f"build artifact {relative}",
                bind_current=True,
            )
            expected_path = output_path.joinpath(*pure.parts).resolve(strict=True)
            if record["path"] != str(expected_path) or record["sha256"] != declared_digest:
                raise ValueError(f"build artifact receipt identity is inconsistent: {relative}")
    else:
        if document["bootstrap_attestation"] is not None:
            raise ValueError("numerical receipt unexpectedly contains a build attestation")
        repository_record = require_exact(
            repository_source,
            {
                "path",
                "relative_path",
                "git_blob_oid",
                "git_blob_byte_count",
                "worktree_sha256",
                "worktree_byte_count",
                "worktree_binding",
            },
            "numerical repository source",
        )
        executed_record = require_identity(
            {key: executed_source[key] for key in identity_keys},
            "numerical executed source",
            bind_current=True,
        )
        if set(executed_source) != identity_keys | {"git_blob_oid"}:
            raise ValueError("numerical executed source has an invalid property set")
        expected_numerical_source = str(Path(expected_source) / "verification" / "run_checks.py")
        if (
            repository_record["path"] != expected_numerical_source
            or repository_record["relative_path"]
            != "manuscripts/gauge_vfe_rg/verification/run_checks.py"
            or repository_record["git_blob_oid"] != executed_source["git_blob_oid"]
            or oid_pattern.fullmatch(str(repository_record["git_blob_oid"])) is None
            or type(repository_record["git_blob_byte_count"]) is not int
            or repository_record["git_blob_byte_count"] <= 0
            or repository_record["worktree_sha256"] != executed_record["sha256"]
            or repository_record["worktree_byte_count"] != executed_record["byte_count"]
            or repository_record["worktree_binding"] != "raw"
            or repository_record["path"] != executed_record["path"]
        ):
            raise ValueError("numerical receipt did not execute the locked repository source path")
        numerical_source_process = _git(
            Path(expected_repository),
            "show",
            f"{expected_source_revision}:manuscripts/gauge_vfe_rg/verification/run_checks.py",
        )
        if numerical_source_process.returncode != 0:
            raise ValueError("cannot independently materialize the numerical source Git blob")
        numerical_blob = numerical_source_process.stdout
        numerical_oid = hashlib.sha1(
            b"blob " + str(len(numerical_blob)).encode("ascii") + b"\0" + numerical_blob
        ).hexdigest()
        current_numerical_bytes, _numerical_identity = _read_bytes_stable(
            Path(expected_numerical_source)
        )
        if (
            numerical_oid != repository_record["git_blob_oid"]
            or len(numerical_blob) != repository_record["git_blob_byte_count"]
            or current_numerical_bytes != numerical_blob
        ):
            raise ValueError("numerical source does not equal its declared Git blob binding")
        expected_child_argv = [
            validated_tools["python"]["path"],
            "-I",
            "-S",
            expected_numerical_source,
            "--update" if mode == "NumericalUpdate" else "--verify",
            expected_result,
        ]
        if mode == "NumericalUpdate":
            expected_child_argv.extend(("--source-revision", expected_source_revision))
        expected_child_argv.extend(("--report", expected_report))
        if child["argv"] != expected_child_argv:
            raise ValueError("numerical child argv differs from the exact independent invocation")
        if child["stdin_sha256"] is not None or child["stdin_byte_count"] is not None:
            raise ValueError("numerical child unexpectedly used bootstrap stdin payload")
        if stdout_bytes != report_bytes + b"\n":
            raise ValueError("numerical child stdout does not equal canonical report bytes plus LF")
        if m1["output_directory_m0"] is not None or m1["output_directory_m1"] is not None:
            raise ValueError("numerical receipt unexpectedly contains output-directory identities")

    return document


def _publish_new_json_with_digest(path: Path, value: Any, stdout: Any) -> str:
    """Create one canonical report without replacement and attest it while retained."""

    payload = _canonical_json_bytes(value)
    path = Path(os.path.abspath(os.fspath(path)))
    component = _first_reparse_component(path)
    if component is not None:
        raise OSError(f"audit publication path is reparse-mediated at {component}")
    parent = path.parent.resolve(strict=True)
    if not parent.is_dir():
        raise NotADirectoryError(f"audit publication parent is not a directory: {parent}")
    if path.parent != parent:
        raise OSError("audit publication parent lexical path does not equal its canonical path")

    handle = _CREATE_FILE(
        str(path),
        _GENERIC_READ | _GENERIC_WRITE,
        _FILE_SHARE_READ,
        None,
        _CREATE_NEW,
        _FILE_ATTRIBUTE_NORMAL,
        None,
    )
    if handle == _INVALID_HANDLE_VALUE:
        error = ctypes.get_last_error()
        if error in {80, 183}:
            raise FileExistsError(error, "audit publication target already exists", str(path))
        raise OSError(error, f"cannot create new audit publication target {path}")
    try:
        descriptor = msvcrt.open_osfhandle(int(handle), os.O_RDWR | os.O_BINARY)
    except BaseException:
        _CLOSE_HANDLE(handle)
        raise
    stream = os.fdopen(descriptor, "w+b", buffering=0)
    try:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
        stream.seek(0)
        published = stream.read()
        stream.seek(0)
        if published != payload:
            raise OSError("retained AuditPath bytes do not equal canonical report bytes")
        snapshot_m0 = _locked_stream_snapshot(path, stream)
        digest = hashlib.sha256(payload).hexdigest()
        if snapshot_m0["sha256"] != digest or snapshot_m0["byte_count"] != len(payload):
            raise OSError("retained AuditPath identity does not equal canonical report bytes")
        marker = f"BUILD_AUDIT_SHA256={digest}\n".encode("ascii")
        written = stdout.write(marker)
        if written is not None and written != len(marker):
            raise OSError("audit digest marker was only partially emitted")
        stdout.flush()
        snapshot_m1 = _locked_stream_snapshot(path, stream)
        if snapshot_m1 != snapshot_m0:
            raise OSError("retained AuditPath changed during digest emission")
        return digest
    finally:
        stream.close()


def _git(repo_root: Path, *arguments: str) -> subprocess.CompletedProcess[bytes]:
    command = [
        str(_TRUSTED_GIT),
        "--no-replace-objects",
        "--literal-pathspecs",
        "-C",
        str(repo_root),
        *arguments,
    ]
    preflight_errors: list[str] = []
    metadata_m0 = _git_metadata_guard_snapshot(repo_root, preflight_errors)
    if metadata_m0 is None:
        return subprocess.CompletedProcess(
            command,
            126,
            b"",
            ("Git metadata preflight rejected: " + "; ".join(preflight_errors)).encode("utf-8"),
        )
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.upper().startswith("GIT_")
    }
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    git_path, git_stream, git_m0 = _AUDIT_EXECUTABLE_LOCKS["git_executable"]
    _assert_locked_stream_m0(git_path, git_stream, git_m0, "trusted Git")
    postflight_errors: list[str] = []
    try:
        try:
            completed = subprocess.run(
                command,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        finally:
            _assert_locked_stream_m0(git_path, git_stream, git_m0, "trusted Git")
    finally:
        active_exception = sys.exception()
        try:
            metadata_m1 = _git_metadata_guard_snapshot(repo_root, postflight_errors)
            if metadata_m1 is None or metadata_m1 != metadata_m0:
                if metadata_m1 is not None and metadata_m1 != metadata_m0:
                    postflight_errors.append(
                        "Git metadata roots or override-path identities changed during the subprocess"
                    )
                if active_exception is not None and postflight_errors:
                    active_exception.add_note(
                        "Git metadata postflight rejected: " + "; ".join(postflight_errors)
                    )
        except BaseException as postflight_exception:
            if active_exception is None:
                raise
            active_exception.add_note(
                f"Git metadata postflight itself failed: {postflight_exception}"
            )
    if postflight_errors:
        detail = "Git metadata postflight rejected: " + "; ".join(postflight_errors)
        stderr = completed.stderr + (("\n" if completed.stderr else "") + detail).encode("utf-8")
        return subprocess.CompletedProcess(command, 126, completed.stdout, stderr)
    return completed


def _git_metadata_directories(repo_root: Path, errors: list[str]) -> list[Path]:
    """Resolve worktree/common Git metadata roots without invoking Git."""

    marker = repo_root / ".git"
    marker_reparse = _first_reparse_component(marker)
    if marker_reparse is not None:
        errors.append(f"repository .git metadata path is reparse-mediated at {marker_reparse}")
        return []
    if marker.is_dir():
        git_dir = marker.resolve()
    elif marker.is_file():
        try:
            marker_bytes, _identity = _read_bytes_stable(marker)
            line = marker_bytes.decode("utf-8").strip()
        except (OSError, UnicodeError) as exc:
            errors.append(f"cannot read repository .git marker: {exc}")
            return []
        if not line.startswith("gitdir: ") or "\n" in line or "\r" in line:
            errors.append("repository .git file has an invalid gitdir record")
            return []
        candidate = Path(line[8:])
        if not candidate.is_absolute():
            candidate = repo_root / candidate
        reparse_component = _first_reparse_component(candidate)
        if reparse_component is not None:
            errors.append(f"repository gitdir path is reparse-mediated at {reparse_component}")
            return []
        try:
            git_dir = candidate.resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            errors.append(f"repository gitdir is invalid: {exc}")
            return []
        if not git_dir.is_dir() or _is_reparse_point(git_dir):
            errors.append("repository gitdir must be a regular non-reparse directory")
            return []
    else:
        errors.append("repository has no regular .git metadata marker")
        return []

    directories = [git_dir]
    common_marker = git_dir / "commondir"
    common_reparse = _first_reparse_component(common_marker)
    if common_marker.is_file() and common_reparse is None:
        try:
            common_bytes, _identity = _read_bytes_stable(common_marker)
            common_value = common_bytes.decode("utf-8").strip()
            common_candidate = Path(common_value)
            if not common_candidate.is_absolute():
                common_candidate = git_dir / common_candidate
            common_component = _first_reparse_component(common_candidate)
            if common_component is not None:
                raise OSError(f"commondir path is reparse-mediated at {common_component}")
            common_dir = common_candidate.resolve(strict=True)
        except (OSError, UnicodeError, RuntimeError) as exc:
            errors.append(f"repository commondir is invalid: {exc}")
        else:
            if not common_dir.is_dir() or _is_reparse_point(common_dir):
                errors.append("repository commondir must be a regular non-reparse directory")
            elif common_dir not in directories:
                directories.append(common_dir)
    elif common_marker.exists() or common_reparse is not None:
        errors.append("repository commondir marker must be a regular non-reparse file")
    return directories


def _optional_metadata_file_snapshot(path: Path) -> tuple[bytes, tuple[int, ...]] | None:
    """Read an optional metadata file; only initial absence is nonfatal."""

    component = _first_reparse_component(path)
    if component is not None:
        raise OSError(f"metadata path is reparse-mediated at {component}")
    try:
        before = path.lstat()
    except FileNotFoundError:
        return None
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    if not stat.S_ISREG(before.st_mode) or bool(
        getattr(before, "st_file_attributes", 0) & reparse_flag
    ):
        raise OSError(f"metadata path is not a regular non-reparse file: {path}")
    stream = path.open("rb")
    try:
        opened = os.fstat(stream.fileno())
        if _content_identity(before) != _content_identity(opened):
            raise OSError(f"metadata file changed while opening: {path}")
        payload = stream.read()
        after_read = os.fstat(stream.fileno())
    finally:
        stream.close()
    try:
        after_close = path.lstat()
    except FileNotFoundError as exc:
        raise OSError(f"metadata file disappeared after observation: {path}") from exc
    if (
        _content_identity(opened) != _content_identity(after_read)
        or _stat_identity(before) != _stat_identity(after_close)
    ):
        raise OSError(f"metadata file changed during stable read: {path}")
    return payload, _stat_identity(after_close)


def _optional_metadata_component_snapshot(path: Path) -> tuple[Any, ...]:
    """Capture an optional directory component with stable absent semantics."""

    component = _first_reparse_component(path)
    if component is not None:
        raise OSError(f"metadata component is reparse-mediated at {component}")
    try:
        before = path.lstat()
    except FileNotFoundError:
        return (str(path), "absent")
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    if not stat.S_ISDIR(before.st_mode) or bool(
        getattr(before, "st_file_attributes", 0) & reparse_flag
    ):
        raise OSError(f"metadata component is not a regular non-reparse directory: {path}")
    try:
        after = path.lstat()
    except FileNotFoundError as exc:
        raise OSError(f"metadata component disappeared after observation: {path}") from exc
    if _stat_identity(before) != _stat_identity(after):
        raise OSError(f"metadata component changed during stable observation: {path}")
    return (str(path.resolve()), "directory", *_stat_identity(after))


def _git_metadata_guard_snapshot(
    repo_root: Path,
    errors: list[str],
) -> tuple[tuple[Any, ...], ...] | None:
    """Capture a nonrecursive boundary snapshot around one Git subprocess."""

    roots = _git_metadata_directories(repo_root, errors)
    if not roots or errors:
        return None
    records: list[tuple[Any, ...]] = []
    for metadata_root in roots:
        for relative in ("", "info", "objects", "objects/info"):
            candidate = (
                metadata_root.joinpath(*relative.split("/"))
                if relative
                else metadata_root
            )
            try:
                records.append(_optional_metadata_component_snapshot(candidate))
            except OSError as exc:
                errors.append(f"cannot stably inspect Git metadata component {relative or '.'}: {exc}")
        for relative in (
            "commondir",
            "info/grafts",
            "shallow",
            "objects/info/alternates",
            "objects/info/http-alternates",
        ):
            candidate = metadata_root.joinpath(*relative.split("/"))
            try:
                snapshot = _optional_metadata_file_snapshot(candidate)
            except OSError as exc:
                errors.append(f"cannot stably inspect Git metadata override {relative}: {exc}")
                continue
            if snapshot is None:
                records.append((str(candidate), "absent"))
                continue
            payload, identity = snapshot
            records.append(
                (str(candidate.resolve()), "file", hashlib.sha256(payload).hexdigest(), *identity)
            )
            if relative != "commondir" and payload:
                errors.append(f"forbidden nonempty Git metadata override: {relative}")
    if errors:
        return None
    return tuple(records)


def _reject_git_metadata_overrides(repo_root: Path, errors: list[str]) -> bool:
    """Reject alternate-history/object controls before the first Git read."""

    clean = True
    names = (
        "info/grafts",
        "shallow",
        "objects/info/alternates",
        "objects/info/http-alternates",
    )
    for metadata_root in _git_metadata_directories(repo_root, errors):
        for relative in names:
            candidate = metadata_root.joinpath(*relative.split("/"))
            reparse_component = _first_reparse_component(candidate)
            if reparse_component is not None:
                errors.append(
                    f"forbidden reparse-mediated Git metadata override {relative}: {reparse_component}"
                )
                clean = False
                continue
            try:
                snapshot = _optional_metadata_file_snapshot(candidate)
            except OSError as exc:
                errors.append(f"cannot inspect Git metadata override {relative}: {exc}")
                clean = False
                continue
            if snapshot is None:
                continue
            payload, _identity = snapshot
            if payload:
                errors.append(f"forbidden nonempty Git metadata override: {relative}")
                clean = False
    return clean and not errors


def _unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _is_reparse_point(path: Path) -> bool:
    try:
        information = path.lstat()
    except OSError:
        return False
    attributes = getattr(information, "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    return path.is_symlink() or bool(attributes & reparse_flag)


def _first_reparse_component(path: Path) -> Path | None:
    """Return the first existing symlink/junction component without resolving it."""

    absolute = Path(os.path.abspath(path))
    parts = absolute.parts
    if not parts:
        return None
    current = Path(parts[0])
    for part in parts[1:]:
        current /= part
        try:
            current.lstat()
        except OSError:
            return None
        if _is_reparse_point(current):
            return current
    return None


def _tool_name(executable: str) -> str:
    name = re.split(r"[\\/]", executable)[-1].casefold()
    for suffix in (".exe", ".cmd", ".bat", ".com"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return name


def _parse_utc(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    if re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})",
        value,
    ) is None:
        return None
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        return None
    return parsed


def _load_commands(
    command_record: Path,
    *,
    production: bool,
    build_dir: Path,
    main_tex: Path | None,
    errors: list[str],
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    if not command_record.is_file():
        errors.append(f"missing command record: {command_record.name}")
        return [], {}
    if _is_reparse_point(command_record):
        errors.append(f"command record must be a regular non-reparse file: {command_record.name}")
        return [], {}
    try:
        document = _strict_json_load(command_record)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"invalid command record {command_record.name}: {exc}")
        return [], {}
    if not isinstance(document, list):
        errors.append("command record must be a JSON array")
        return [], {}

    commands: list[dict[str, Any]] = []
    versions: dict[str, str] = {}
    intervals: list[tuple[datetime, datetime, int]] = []
    stream_artifacts: dict[str, int] = {}
    expected_order = ("pdflatex", "bibtex", "pdflatex", "pdflatex")
    if len(document) != len(expected_order):
        errors.append(
            f"command sequence must contain exactly four records in pdflatex, bibtex, pdflatex, pdflatex order; found {len(document)}"
        )

    for index, raw_command in enumerate(document):
        if not isinstance(raw_command, dict):
            errors.append(f"command record {index + 1} must be an object")
            continue
        command = dict(raw_command)
        commands.append(command)
        if production:
            observed_keys = set(command)
            missing_keys = sorted(_COMMAND_KEYS - observed_keys)
            unknown_keys = sorted(observed_keys - _COMMAND_KEYS)
            if missing_keys:
                errors.append(
                    f"command record {index + 1} is missing required keys: {', '.join(missing_keys)}"
                )
            if unknown_keys:
                errors.append(
                    f"command record {index + 1} has unknown keys: {', '.join(unknown_keys)}"
                )
        argv = command.get("argv")
        if (
            not isinstance(argv, list)
            or not argv
            or any(not isinstance(argument, str) or not argument for argument in argv)
        ):
            errors.append(f"command record {index + 1} has an invalid argv string array")
            continue
        observed_tool = _tool_name(argv[0])
        expected_tool = expected_order[index] if index < len(expected_order) else None
        if expected_tool is None or observed_tool != expected_tool:
            errors.append(
                f"command order mismatch at record {index + 1}: expected {expected_tool or 'no extra command'}, found {observed_tool or argv[0]}"
            )

        returncode = command.get("returncode")
        if isinstance(returncode, bool) or not isinstance(returncode, int):
            errors.append(f"{observed_tool or 'command'} record {index + 1} has a non-integer returncode")
        elif returncode != 0:
            errors.append(
                f"{observed_tool or 'command'} record {index + 1} failed with return code {returncode}"
            )

        version = command.get("tool_version")
        if not isinstance(version, str) or not version.strip():
            errors.append(f"{observed_tool or 'command'} record {index + 1} has no tool_version")
        elif observed_tool in {"pdflatex", "bibtex"}:
            prior = versions.get(observed_tool)
            if prior is not None and prior != version:
                errors.append(f"inconsistent {observed_tool} tool versions in command record")
            versions.setdefault(observed_tool, version)

        if not production and observed_tool == "pdflatex":
            if "-interaction=nonstopmode" not in argv or not argv[-1].casefold().endswith(".tex"):
                errors.append(
                    f"pdflatex record {index + 1} must use -interaction=nonstopmode and a TeX source argument"
                )
        elif not production and observed_tool == "bibtex" and argv[1:] != ["main"]:
            errors.append("bibtex command must target exactly the main jobname")

        if production:
            executable = command.get("executable")
            if not isinstance(executable, str) or not executable or not Path(executable).is_absolute():
                errors.append(f"command record {index + 1} executable must be an absolute path")
            elif _tool_name(executable) != observed_tool:
                errors.append(f"command record {index + 1} executable disagrees with argv[0]")
            elif _first_reparse_component(Path(executable)) is not None:
                errors.append(f"command record {index + 1} executable path is reparse-mediated")
            elif not Path(executable).is_file() or _is_reparse_point(Path(executable)):
                errors.append(f"command record {index + 1} executable is not a regular file")
            else:
                try:
                    resolved_executable = Path(executable).resolve(strict=True)
                    resolved_argv0 = Path(argv[0]).resolve(strict=True)
                except (OSError, RuntimeError) as exc:
                    errors.append(f"command record {index + 1} executable identity is invalid: {exc}")
                else:
                    if resolved_executable != resolved_argv0:
                        errors.append(f"command record {index + 1} executable disagrees with argv[0]")

            cwd = command.get("cwd")
            try:
                cwd_matches = isinstance(cwd, str) and Path(cwd).resolve(strict=True) == build_dir
            except (OSError, RuntimeError):
                cwd_matches = False
            if not cwd_matches:
                errors.append(f"command record {index + 1} cwd must equal the canonical build directory")

            environment = command.get("environment")
            if not isinstance(environment, dict):
                errors.append(f"command record {index + 1} environment must be an object")
            else:
                environment_keys = set(environment)
                missing_environment = sorted(_CHILD_ENV_KEYS - environment_keys)
                unknown_environment = sorted(environment_keys - _CHILD_ENV_KEYS)
                if missing_environment:
                    errors.append(
                        f"command record {index + 1} environment is missing required keys: "
                        + ", ".join(missing_environment)
                    )
                if unknown_environment:
                    errors.append(
                        f"command record {index + 1} environment has unknown keys: "
                        + ", ".join(unknown_environment)
                    )
                if any(not isinstance(value, str) for value in environment.values()):
                    errors.append(
                        f"command record {index + 1} environment values must all be strings"
                    )
                if isinstance(executable, str):
                    expected_environment = {
                        "SystemRoot": str(_WINDOWS_DIRECTORY),
                        "WINDIR": str(_WINDOWS_DIRECTORY),
                        "SystemDrive": "C:",
                        "COMSPEC": str(_WINDOWS_SYSTEM_DIRECTORY / "cmd.exe"),
                        "PATHEXT": ".COM;.EXE;.BAT;.CMD",
                        "PATH": f"{Path(executable).parent};{_WINDOWS_SYSTEM_DIRECTORY}",
                        "TEMP": str(build_dir / ".tex-tmp"),
                        "TMP": str(build_dir / ".tex-tmp"),
                    }
                    for name, value in expected_environment.items():
                        if environment.get(name) != value:
                            errors.append(
                                f"command record {index + 1} environment {name} is not the exact controlled value"
                            )

            if isinstance(executable, str):
                expected_argv = (
                    [
                        executable,
                        "-interaction=nonstopmode",
                        "-halt-on-error",
                        "-file-line-error",
                        "-recorder",
                        "-no-shell-escape",
                        str(main_tex),
                    ]
                    if observed_tool == "pdflatex" and main_tex is not None
                    else [executable, "main"]
                    if observed_tool == "bibtex"
                    else None
                )
                if expected_argv is None or argv != expected_argv:
                    errors.append(
                        f"command record {index + 1} argv does not equal the exact production argv"
                    )

            started = _parse_utc(command.get("started_at_utc"))
            ended = _parse_utc(command.get("ended_at_utc"))
            if started is None or ended is None:
                errors.append(f"command record {index + 1} has invalid UTC timestamps")
            elif started > ended:
                errors.append(f"command record {index + 1} ends before it starts")
            else:
                intervals.append((started, ended, index + 1))
            if isinstance(executable, str) and Path(executable).is_file():
                match = re.search(
                    r"(?:^|;)sha256:([0-9a-f]{64})$",
                    version if isinstance(version, str) else "",
                )
                if match is None:
                    errors.append(
                        f"command record {index + 1} tool_version has no lowercase SHA-256 suffix"
                    )
                else:
                    try:
                        executable_digest = _sha256_file(Path(executable))
                    except OSError as exc:
                        errors.append(
                            f"command record {index + 1} executable could not be hashed stably: {exc}"
                        )
                    else:
                        if executable_digest != match.group(1):
                            errors.append(
                                f"command record {index + 1} tool_version SHA-256 disagrees with executable bytes"
                            )
            for hash_field in ("stdout_sha256", "stderr_sha256"):
                digest = command.get(hash_field)
                if not isinstance(digest, str) or _SHA256_RE.fullmatch(digest) is None:
                    errors.append(f"command record {index + 1} has invalid {hash_field}")
            for stream_name in ("stdout", "stderr"):
                artifact_field = f"{stream_name}_artifact"
                digest_field = f"{stream_name}_sha256"
                artifact_name = command.get(artifact_field)
                if (
                    not isinstance(artifact_name, str)
                    or not artifact_name
                    or Path(artifact_name).is_absolute()
                    or Path(artifact_name).name != artifact_name
                    or artifact_name in {".", ".."}
                ):
                    errors.append(
                        f"command record {index + 1} has an invalid {artifact_field} basename"
                    )
                    continue
                artifact_path = (command_record.parent / artifact_name).resolve()
                original_artifact_path = command_record.parent / artifact_name
                if (
                    _first_reparse_component(original_artifact_path) is not None
                    or
                    not _is_relative_to(artifact_path, command_record.parent)
                    or not artifact_path.is_file()
                    or _is_reparse_point(artifact_path)
                ):
                    errors.append(
                        f"command record {index + 1} {artifact_field} is not a regular build artifact"
                    )
                    continue
                prior_record = stream_artifacts.get(artifact_name.casefold())
                if prior_record is not None:
                    errors.append(
                        f"all eight command stream artifacts must be globally unique; {artifact_name} is reused by records {prior_record} and {index + 1}"
                    )
                else:
                    stream_artifacts[artifact_name.casefold()] = index + 1
                recorded_digest = command.get(digest_field)
                if isinstance(recorded_digest, str) and _SHA256_RE.fullmatch(recorded_digest):
                    actual_digest = _sha256_file(artifact_path)
                    if actual_digest != recorded_digest:
                        errors.append(
                            f"command record {index + 1} {digest_field} disagrees with {artifact_name} bytes"
                        )
            if command.get("stdout_artifact") == command.get("stderr_artifact"):
                errors.append(
                    f"command record {index + 1} must use distinct stdout and stderr artifacts"
                )
    if production and len(stream_artifacts) != 8:
        errors.append(
            f"production command evidence must bind eight globally unique stream artifacts; found {len(stream_artifacts)}"
        )
    if production and len(intervals) == 4:
        for previous, current in zip(intervals, intervals[1:]):
            _prior_start, prior_end, prior_index = previous
            current_start, _current_end, current_index = current
            if current_start < prior_end:
                errors.append(
                    f"command UTC intervals overlap or are not globally ordered between records {prior_index} and {current_index}"
                )

    return commands, dict(sorted(versions.items()))


def _resolve_source_revision(repo_root: Path, source_revision: str, errors: list[str]) -> str | None:
    if not isinstance(source_revision, str) or _REVISION_RE.fullmatch(source_revision) is None:
        errors.append("source revision must be a full lowercase 40-hex Git commit")
        return None
    completed = _git(
        repo_root,
        "-c",
        "core.quotepath=false",
        "rev-parse",
        "--verify",
        f"{source_revision}^{{commit}}",
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        errors.append(f"source revision is not a real Git commit: {detail or source_revision}")
        return None
    try:
        resolved = completed.stdout.decode("ascii").strip().lower()
    except UnicodeError:
        errors.append("Git returned a non-ASCII source revision")
        return None
    if _REVISION_RE.fullmatch(resolved) is None or resolved != source_revision:
        errors.append(f"source revision resolved to unexpected commit {resolved!r}")
        return None
    return resolved


def _resolve_head_and_require_ancestry(
    repo_root: Path,
    source_revision: str,
    errors: list[str],
) -> str | None:
    head = _git(repo_root, "rev-parse", "--verify", "HEAD^{commit}")
    if head.returncode != 0:
        errors.append("cannot resolve the current Git HEAD commit")
        return None
    resolved_head = head.stdout.decode("ascii", errors="replace").strip().lower()
    if _REVISION_RE.fullmatch(resolved_head) is None:
        errors.append(f"Git returned an invalid current HEAD commit: {resolved_head!r}")
        return None
    ancestry = _git(repo_root, "merge-base", "--is-ancestor", source_revision, resolved_head)
    if ancestry.returncode != 0:
        errors.append(
            f"source revision {source_revision} must be an ancestor of current HEAD {resolved_head}"
        )
        return None
    return resolved_head


def _verify_git_top_level(repo_root: Path, errors: list[str]) -> bool:
    completed = _git(repo_root, "rev-parse", "--show-toplevel")
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        errors.append(f"repository root is not a Git worktree: {detail or repo_root}")
        return False
    try:
        top_level = Path(completed.stdout.decode("utf-8").strip()).resolve(strict=True)
    except (UnicodeError, OSError, RuntimeError) as exc:
        errors.append(f"Git returned an invalid worktree top level: {exc}")
        return False
    if os.path.normcase(str(top_level)) != os.path.normcase(str(repo_root)):
        errors.append(
            f"repo_root must be exactly the Git worktree top level: expected {top_level}, found {repo_root}"
        )
        return False
    return True


def _walk_regular_files(root: Path, errors: list[str], label: str) -> list[Path]:
    files: list[Path] = []

    def record_walk_error(exc: OSError) -> None:
        location = exc.filename if exc.filename is not None else str(root)
        errors.append(f"cannot traverse {label} at {location}: {exc}")

    for directory, names, filenames in os.walk(
        root,
        topdown=True,
        followlinks=False,
        onerror=record_walk_error,
    ):
        directory_path = Path(directory)
        kept_names: list[str] = []
        for name in sorted(names):
            candidate = directory_path / name
            if name == ".git":
                continue
            if _is_reparse_point(candidate):
                errors.append(f"{label} contains a reparse directory: {candidate.relative_to(root).as_posix()}")
                continue
            kept_names.append(name)
        names[:] = kept_names
        for name in sorted(filenames):
            candidate = directory_path / name
            relative = candidate.relative_to(root).as_posix()
            if _is_reparse_point(candidate):
                errors.append(f"{label} contains a reparse file: {relative}")
                continue
            try:
                mode = candidate.stat().st_mode
            except OSError as exc:
                errors.append(f"cannot inspect {label} file {relative}: {exc}")
                continue
            if stat.S_ISREG(mode):
                files.append(candidate)
            else:
                errors.append(f"{label} contains a non-regular artifact: {relative}")
    return files


def _pypdf_distribution_provenance() -> dict[str, Any]:
    """Return stable byte provenance for the exact admitted pypdf distribution."""

    snapshot = _bootstrap_pypdf_distribution_snapshot()
    provenance = snapshot["provenance"]
    imported_path = _PYPDF_IMPORTED_PATH.resolve(strict=True)
    if imported_path != Path(provenance["pypdf_module_path"]):
        raise RuntimeError("imported pypdf module origin disagrees with its exact RECORD inventory")
    if getattr(pypdf, "__version__", None) != provenance["pypdf"]:
        raise RuntimeError("pypdf module version disagrees with its exact RECORD inventory")
    return {**provenance, "pypdf_pycache_prefix": str(_PYPDF_PYCACHE_ROOT)}


def _inventory_from_fls(repo_root: Path, build_dir: Path, errors: list[str]) -> list[Path]:
    fls_path = build_dir / "main.fls"
    if not fls_path.is_file():
        return []
    try:
        raw, _identity = _read_bytes_stable(fls_path)
        lines = raw.decode("utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        errors.append(f"cannot parse main.fls as UTF-8: {exc}")
        return []
    discovered: dict[str, Path] = {}
    for line_number, line in enumerate(lines, 1):
        if not line.startswith("INPUT "):
            continue
        value = line[6:]
        if not value:
            errors.append(f"main.fls:{line_number}: empty INPUT record")
            continue
        candidate = Path(value)
        if not candidate.is_absolute():
            candidate = build_dir / candidate
        reparse_component = _first_reparse_component(candidate)
        if reparse_component is not None:
            errors.append(
                f"main.fls:{line_number}: INPUT path is reparse-mediated at {reparse_component}: {value}"
            )
            continue
        try:
            resolved = candidate.resolve(strict=True)
        except OSError:
            continue
        if not _is_relative_to(resolved, repo_root):
            continue
        if _is_reparse_point(resolved) or not resolved.is_file():
            errors.append(f"main.fls:{line_number}: repository input is not a regular file: {value}")
            continue
        relative = resolved.relative_to(repo_root).as_posix()
        discovered[relative] = resolved
    if not discovered:
        errors.append("main.fls contains no regular repository-owned source inputs")
    return [discovered[key] for key in sorted(discovered)]


def _production_inventory_from_fls(
    repo_root: Path,
    build_dir: Path,
    errors: list[str],
) -> tuple[dict[str, dict[str, dict[str, Any]]], dict[tuple[str, str], Path]]:
    """Parse every recorder input into a complete classified byte inventory."""

    inventory: dict[str, dict[str, dict[str, Any]]] = {
        "repository": {},
        "build": {},
        "external": {},
    }
    paths: dict[tuple[str, str], Path] = {}
    fls_path = build_dir / "main.fls"
    if not fls_path.is_file() or _is_reparse_point(fls_path):
        errors.append("production profile requires regular non-reparse main.fls recorder evidence")
        return inventory, paths
    try:
        raw, _identity = _read_bytes_stable(fls_path)
        lines = raw.decode("utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        errors.append(f"cannot parse main.fls as UTF-8: {exc}")
        return inventory, paths

    pwd_records = [(number, line[4:]) for number, line in enumerate(lines, 1) if line.startswith("PWD ")]
    if len(pwd_records) != 1:
        errors.append(f"main.fls must contain exactly one PWD record; found {len(pwd_records)}")
    else:
        line_number, value = pwd_records[0]
        try:
            recorded_pwd = Path(value).resolve(strict=True)
        except (OSError, RuntimeError, ValueError) as exc:
            errors.append(f"main.fls:{line_number}: invalid PWD record: {exc}")
        else:
            if recorded_pwd != build_dir:
                errors.append(
                    f"main.fls PWD must equal the canonical build directory: {recorded_pwd}"
                )

    input_count = 0
    casefolded: dict[tuple[str, str], str] = {}
    for line_number, line in enumerate(lines, 1):
        if not line.startswith("INPUT "):
            continue
        input_count += 1
        value = line[6:]
        if not value:
            errors.append(f"main.fls:{line_number}: empty INPUT record")
            continue
        candidate = Path(value)
        if not candidate.is_absolute():
            candidate = build_dir / candidate
        reparse_component = _first_reparse_component(candidate)
        if reparse_component is not None:
            errors.append(
                f"main.fls:{line_number}: INPUT path is reparse-mediated at {reparse_component}: {value}"
            )
            continue
        try:
            resolved = candidate.resolve(strict=True)
        except (OSError, RuntimeError, ValueError) as exc:
            errors.append(f"main.fls:{line_number}: INPUT is missing: {value}: {exc}")
            continue
        if _is_reparse_point(resolved) or not resolved.is_file():
            errors.append(
                f"main.fls:{line_number}: INPUT is not a regular non-reparse file: {value}"
            )
            continue
        if _is_relative_to(resolved, repo_root):
            category = "repository"
            key = resolved.relative_to(repo_root).as_posix()
        elif _is_relative_to(resolved, build_dir):
            category = "build"
            key = resolved.relative_to(build_dir).as_posix()
        else:
            category = "external"
            key = str(resolved)
        collision_key = (category, key.casefold())
        prior = casefolded.get(collision_key)
        if prior is not None and prior != key:
            errors.append(f"main.fls input inventory has a case-fold collision: {prior!r}, {key!r}")
            continue
        casefolded[collision_key] = key
        try:
            digest, byte_count, _file_identity = _sha256_file_with_identity(resolved)
        except OSError as exc:
            errors.append(f"main.fls:{line_number}: cannot hash INPUT {value}: {exc}")
            continue
        record = {"sha256": digest, "byte_count": byte_count}
        prior_record = inventory[category].get(key)
        if prior_record is not None and prior_record != record:
            errors.append(f"main.fls repeated INPUT changed identity: {key}")
        inventory[category][key] = record
        paths[(category, key)] = resolved
    if input_count == 0:
        errors.append("main.fls contains no INPUT records")
    if not inventory["repository"]:
        errors.append("main.fls contains no regular repository-owned source inputs")
    return (
        {category: dict(sorted(entries.items())) for category, entries in inventory.items()},
        dict(sorted(paths.items())),
    )


def _validate_final_recorder_binding(
    *,
    build_dir: Path,
    build_context: dict[str, Any],
    recorder_inventory: dict[str, dict[str, dict[str, Any]]],
    evidence_inventory: dict[str, dict[str, dict[str, Any]]],
    errors: list[str],
) -> None:
    """Bind canonical ``main.fls`` bytes and inputs to retained build evidence."""

    recorder_snapshots = build_context.get("recorder_snapshots")
    pass_four = (
        recorder_snapshots.get("pass_4")
        if isinstance(recorder_snapshots, dict)
        else None
    )
    pass_four_path_value = pass_four.get("path") if isinstance(pass_four, dict) else None
    if not isinstance(pass_four_path_value, str) or not pass_four_path_value:
        errors.append(
            "build-context.json pass_4 recorder path is unavailable for final main.fls binding"
        )
    else:
        try:
            final_bytes, _final_identity = _read_bytes_stable(build_dir / "main.fls")
            pass_four_bytes, _pass_four_identity = _read_bytes_stable(
                Path(pass_four_path_value)
            )
        except (OSError, RuntimeError, ValueError) as exc:
            errors.append(f"cannot bind final main.fls to retained pass_4 recorder bytes: {exc}")
        else:
            if final_bytes != pass_four_bytes:
                errors.append(
                    "final main.fls PWD/input recorder bytes do not equal the retained pass_4 snapshot"
                )

    locked_repository_inputs = build_context.get("locked_repository_inputs")
    for category in ("repository", "build", "external"):
        declared = evidence_inventory.get(category, {})
        for key, record in sorted(recorder_inventory.get(category, {}).items()):
            if (
                category == "repository"
                and (
                    not isinstance(locked_repository_inputs, dict)
                    or key not in locked_repository_inputs
                )
            ):
                errors.append(
                    f"main.fls repository input was not present in the prelocked source envelope: {key}"
                )
            admitted = declared.get(key)
            if admitted is None:
                errors.append(
                    f"main.fls {category} input is absent from the complete evidence inventory: {key}"
                )
            elif admitted != record:
                errors.append(
                    f"main.fls {category} input identity disagrees with the complete evidence inventory: {key}"
                )


def _capture_classified_inventory_state(
    inventory: dict[str, dict[str, dict[str, Any]]],
    paths: dict[tuple[str, str], Path],
    errors: list[str],
    phase: str,
) -> dict[tuple[str, str], tuple[int, ...]]:
    states: dict[tuple[str, str], tuple[int, ...]] = {}
    for category in ("repository", "build", "external"):
        for key, record in sorted(inventory.get(category, {}).items()):
            path = paths.get((category, key))
            if path is None:
                errors.append(f"{phase} input inventory has no retained path for {category}:{key}")
                continue
            try:
                digest, byte_count, identity = _sha256_file_with_identity(path)
            except OSError as exc:
                errors.append(f"cannot capture {phase} input state for {category}:{key}: {exc}")
                continue
            if record != {"sha256": digest, "byte_count": byte_count}:
                errors.append(f"{phase} input bytes disagree with inventory for {category}:{key}")
            states[(category, key)] = identity
    return dict(sorted(states.items()))


def _context_input(
    *,
    repo_root: Path,
    context: dict[str, Any],
    field: str,
    errors: list[str],
) -> tuple[str, str, int] | None:
    record = context.get(field)
    if not isinstance(record, dict):
        errors.append(f"build-context.json has no {field} identity object")
        return None
    relative = record.get("path")
    declared_digest = record.get("sha256")
    if (
        not isinstance(relative, str)
        or not relative
        or "\\" in relative
        or relative.startswith("/")
        or ":" in relative.split("/", 1)[0]
        or any(part in {"", ".", ".."} for part in relative.split("/"))
    ):
        errors.append(f"build-context.json {field}.path is not a safe repository-relative POSIX path")
        return None
    if not isinstance(declared_digest, str) or _SHA256_RE.fullmatch(declared_digest) is None:
        errors.append(f"build-context.json {field}.sha256 is not a lowercase SHA-256 digest")
        return None
    candidate = repo_root.joinpath(*relative.split("/"))
    try:
        resolved = candidate.resolve(strict=True)
    except (OSError, RuntimeError, ValueError) as exc:
        errors.append(f"build-context.json {field} path is missing: {relative}: {exc}")
        return None
    if (
        not _is_relative_to(resolved, repo_root)
        or not resolved.is_file()
        or _is_reparse_point(resolved)
        or resolved.relative_to(repo_root).as_posix() != relative
    ):
        errors.append(f"build-context.json {field} path is not one regular repository file: {relative}")
        return None
    try:
        actual_digest, byte_count, _identity = _sha256_file_with_identity(resolved)
    except OSError as exc:
        errors.append(f"build-context.json {field} path could not be hashed stably: {relative}: {exc}")
        return None
    if actual_digest != declared_digest:
        errors.append(
            f"build-context.json {field}.sha256 disagrees with raw bytes for {relative}"
        )
        return None
    return relative, actual_digest, byte_count


def _load_legacy_build_context_inputs(
    *,
    repo_root: Path,
    build_dir: Path,
    source_revision: str,
    require_context: bool,
    errors: list[str],
) -> tuple[dict[str, str], set[str]]:
    context_path = build_dir / "build-context.json"
    if not context_path.is_file():
        if require_context:
            errors.append("rich command evidence requires build-context.json")
        return {}, set()
    if _is_reparse_point(context_path):
        errors.append("build-context.json must be a regular non-reparse file")
        return {}, set()
    try:
        context = _strict_json_load(context_path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"invalid build-context.json: {exc}")
        return {}, set()
    if not isinstance(context, dict):
        errors.append("build-context.json must contain one JSON object")
        return {}, set()
    if context.get("source_revision") != source_revision:
        errors.append("build-context.json source_revision does not equal the requested source revision")
    if context.get("initial_entries") != []:
        errors.append("build-context.json does not attest an empty initial output directory")
    recorded_repo = context.get("repository_root")
    recorded_output = context.get("output_directory")
    try:
        repo_matches = isinstance(recorded_repo, str) and os.path.normcase(
            str(Path(recorded_repo).resolve())
        ) == os.path.normcase(str(repo_root))
    except (OSError, RuntimeError, ValueError):
        repo_matches = False
    if not repo_matches:
        errors.append("build-context.json repository_root does not equal repo_root")
    try:
        output_matches = isinstance(recorded_output, str) and os.path.normcase(
            str(Path(recorded_output).resolve())
        ) == os.path.normcase(str(build_dir))
    except (OSError, RuntimeError, ValueError):
        output_matches = False
    if not output_matches:
        errors.append("build-context.json output_directory does not equal build_dir")
    source_date_epoch = context.get("source_date_epoch")
    if not isinstance(source_date_epoch, str) or re.fullmatch(r"[0-9]+", source_date_epoch) is None:
        errors.append("build-context.json source_date_epoch must be a decimal Git commit timestamp")
    else:
        timestamp = _git(
            repo_root,
            "show",
            "-s",
            "--format=%ct",
            source_revision,
        )
        expected_epoch = timestamp.stdout.decode("ascii", errors="replace").strip()
        if timestamp.returncode != 0 or expected_epoch != source_date_epoch:
            errors.append("build-context.json source_date_epoch does not equal the source commit timestamp")

    additions: dict[str, str] = {}
    evidence_only: set[str] = set()
    build_script = _context_input(
        repo_root=repo_root,
        context=context,
        field="build_script",
        errors=errors,
    )
    if build_script is not None:
        relative, digest, _byte_count = build_script
        recorded_source = context.get("source_directory")
        expected_script = None
        if isinstance(recorded_source, str):
            try:
                source_directory = Path(recorded_source).resolve(strict=True)
                if _is_relative_to(source_directory, repo_root):
                    expected_script = (source_directory / "build.ps1").resolve(strict=True)
            except (OSError, RuntimeError):
                expected_script = None
        actual_script = repo_root.joinpath(*relative.split("/")).resolve()
        if expected_script is None or actual_script != expected_script:
            errors.append("build-context.json build_script identity does not name source_directory/build.ps1")
        additions[relative] = digest

    verification_result = _context_input(
        repo_root=repo_root,
        context=context,
        field="verification_result",
        errors=errors,
    )
    if verification_result is not None:
        relative, digest, _byte_count = verification_result
        additions[relative] = digest
        evidence_only.add(relative)
        result_path = repo_root.joinpath(*relative.split("/"))
        try:
            result_document = _strict_json_load(result_path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"verification result is not strict JSON: {exc}")
        else:
            if not isinstance(result_document, dict):
                errors.append("verification result must contain one JSON object")
            else:
                if result_document.get("source_revision") != source_revision:
                    errors.append("verification result source_revision does not equal the requested source revision")
                if result_document.get("overall_status") != "PASS":
                    errors.append("verification result overall_status is not PASS")
                manifest = result_document.get("manifest")
                if not isinstance(manifest, dict):
                    errors.append("verification result has no manifest object")
                elif (
                    set(manifest)
                    != {"hash_algorithm", "hash_domain", "path_semantics", "bound_inputs"}
                    or manifest.get("hash_algorithm") != "SHA-256"
                    or manifest.get("hash_domain") != "raw file bytes"
                    or manifest.get("path_semantics") != "repository-relative POSIX paths"
                    or not isinstance(manifest.get("bound_inputs"), dict)
                    or not manifest.get("bound_inputs")
                ):
                    errors.append("verification result manifest envelope is invalid")
                else:
                    for manifest_path, entry in sorted(manifest["bound_inputs"].items()):
                        if not isinstance(entry, dict) or set(entry) != {"byte_count", "sha256"}:
                            errors.append(f"verification manifest entry has an invalid shape: {manifest_path!r}")
                            continue
                        synthetic_context = {
                            "manifest_entry": {
                                "path": manifest_path,
                                "sha256": entry.get("sha256"),
                            }
                        }
                        verified = _context_input(
                            repo_root=repo_root,
                            context=synthetic_context,
                            field="manifest_entry",
                            errors=errors,
                        )
                        if verified is None:
                            continue
                        manifest_relative, manifest_digest, actual_count = verified
                        byte_count = entry.get("byte_count")
                        if (
                            isinstance(byte_count, bool)
                            or not isinstance(byte_count, int)
                            or byte_count < 0
                            or byte_count != actual_count
                        ):
                            errors.append(
                                f"verification manifest byte_count disagrees with raw bytes: {manifest_relative}"
                            )
                            continue
                        prior = additions.get(manifest_relative)
                        if prior is not None and prior != manifest_digest:
                            errors.append(
                                f"verification manifest disagrees with build-context identity: {manifest_relative}"
                            )
                        additions[manifest_relative] = manifest_digest
    return additions, evidence_only


def _validate_identity_record(
    *,
    record: Any,
    field: str,
    expected_path: Path | None,
    repo_root: Path | None,
    errors: list[str],
) -> tuple[Path, str, int] | None:
    """Validate one exact path/hash/byte-count identity envelope."""

    if not isinstance(record, dict) or set(record) != {"path", "sha256", "byte_count"}:
        errors.append(
            f"build-context.json {field} must contain exactly path, sha256, and byte_count"
        )
        return None
    declared_path = record.get("path")
    digest = record.get("sha256")
    byte_count = record.get("byte_count")
    if not isinstance(declared_path, str) or not declared_path:
        errors.append(f"build-context.json {field}.path must be a nonempty string")
        return None
    if not isinstance(digest, str) or _SHA256_RE.fullmatch(digest) is None:
        errors.append(f"build-context.json {field}.sha256 is not a lowercase SHA-256 digest")
        return None
    if isinstance(byte_count, bool) or not isinstance(byte_count, int) or byte_count < 0:
        errors.append(f"build-context.json {field}.byte_count must be a nonnegative integer")
        return None

    if repo_root is None:
        candidate = Path(declared_path)
        if not candidate.is_absolute():
            errors.append(f"build-context.json {field}.path must be absolute")
            return None
    else:
        if (
            "\\" in declared_path
            or declared_path.startswith("/")
            or ":" in declared_path.split("/", 1)[0]
            or any(part in {"", ".", ".."} for part in declared_path.split("/"))
        ):
            errors.append(
                f"build-context.json {field}.path is not a safe repository-relative POSIX path"
            )
            return None
        candidate = repo_root.joinpath(*declared_path.split("/"))
    reparse_component = _first_reparse_component(candidate)
    if reparse_component is not None:
        errors.append(
            f"build-context.json {field}.path is reparse-mediated at {reparse_component}"
        )
        return None
    try:
        resolved = candidate.resolve(strict=True)
    except (OSError, RuntimeError, ValueError) as exc:
        errors.append(f"build-context.json {field}.path is missing: {declared_path}: {exc}")
        return None
    if not resolved.is_file() or _is_reparse_point(resolved):
        errors.append(f"build-context.json {field}.path is not a regular non-reparse file")
        return None
    if repo_root is not None:
        if not _is_relative_to(resolved, repo_root) or resolved.relative_to(repo_root).as_posix() != declared_path:
            errors.append(f"build-context.json {field}.path does not resolve to its exact repository path")
            return None
    if expected_path is not None:
        try:
            expected = expected_path.resolve(strict=True)
        except (OSError, RuntimeError):
            expected = expected_path.resolve()
        if resolved != expected:
            errors.append(f"build-context.json {field}.path does not equal {expected}")
    try:
        actual_digest, actual_count, _identity = _sha256_file_with_identity(resolved)
    except OSError as exc:
        errors.append(f"build-context.json {field} could not be hashed stably: {exc}")
        return None
    if actual_digest != digest:
        errors.append(f"build-context.json {field}.sha256 disagrees with raw bytes")
    if actual_count != byte_count:
        errors.append(f"build-context.json {field}.byte_count disagrees with raw bytes")
    if actual_digest != digest or actual_count != byte_count:
        return None
    return resolved, actual_digest, actual_count


def _validate_typed_input_inventory(
    *,
    record: Any,
    repo_root: Path,
    build_dir: Path,
    field: str,
    errors: list[str],
) -> tuple[
    dict[str, dict[str, dict[str, Any]]],
    dict[tuple[str, str], Path],
]:
    """Validate one sorted repository/build/external raw-byte inventory."""

    empty = {"repository": {}, "build": {}, "external": {}}
    if not isinstance(record, dict) or list(record) != ["repository", "build", "external"]:
        errors.append(
            f"build-context.json {field} must contain exactly ordered repository, build, and external maps"
        )
        return empty, {}

    inventory: dict[str, dict[str, dict[str, Any]]] = {
        "repository": {},
        "build": {},
        "external": {},
    }
    paths: dict[tuple[str, str], Path] = {}
    for category in ("repository", "build", "external"):
        entries = record.get(category)
        if not isinstance(entries, dict):
            errors.append(f"build-context.json {field}.{category} must be one JSON object")
            continue
        keys = list(entries)
        if keys != sorted(keys):
            errors.append(f"build-context.json {field}.{category} keys are not ordinal-sorted")
        folded: set[str] = set()
        for key, identity in entries.items():
            if not isinstance(key, str) or not key:
                errors.append(f"build-context.json {field}.{category} contains an empty or non-string path")
                continue
            if key.casefold() in folded:
                errors.append(f"build-context.json {field}.{category} contains a case-colliding path: {key!r}")
                continue
            folded.add(key.casefold())
            if not isinstance(identity, dict) or set(identity) != {"sha256", "byte_count"}:
                errors.append(
                    f"build-context.json {field}.{category}[{key!r}] has an invalid identity shape"
                )
                continue
            digest = identity.get("sha256")
            byte_count = identity.get("byte_count")
            if not isinstance(digest, str) or _SHA256_RE.fullmatch(digest) is None:
                errors.append(
                    f"build-context.json {field}.{category}[{key!r}].sha256 is invalid"
                )
                continue
            if isinstance(byte_count, bool) or not isinstance(byte_count, int) or byte_count < 0:
                errors.append(
                    f"build-context.json {field}.{category}[{key!r}].byte_count is invalid"
                )
                continue

            if category in {"repository", "build"}:
                if (
                    "\\" in key
                    or key.startswith("/")
                    or ":" in key.split("/", 1)[0]
                    or any(part in {"", ".", ".."} for part in key.split("/"))
                ):
                    errors.append(
                        f"build-context.json {field}.{category} path is not safe POSIX-relative: {key!r}"
                    )
                    continue
                root = repo_root if category == "repository" else build_dir
                candidate = root.joinpath(*key.split("/"))
            else:
                candidate = Path(key)
                if not candidate.is_absolute():
                    errors.append(
                        f"build-context.json {field}.external path must be absolute: {key!r}"
                    )
                    continue
            component = _first_reparse_component(candidate)
            if component is not None:
                errors.append(
                    f"build-context.json {field}.{category} path is reparse-mediated at {component}: {key}"
                )
                continue
            try:
                resolved = candidate.resolve(strict=True)
            except (OSError, RuntimeError, ValueError) as exc:
                errors.append(
                    f"build-context.json {field}.{category} path is missing: {key}: {exc}"
                )
                continue
            if not resolved.is_file() or _is_reparse_point(resolved):
                errors.append(
                    f"build-context.json {field}.{category} path is not a regular non-reparse file: {key}"
                )
                continue
            if category == "repository":
                if not _is_relative_to(resolved, repo_root) or resolved.relative_to(repo_root).as_posix() != key:
                    errors.append(
                        f"build-context.json {field}.repository path does not resolve exactly: {key}"
                    )
                    continue
            elif category == "build":
                if not _is_relative_to(resolved, build_dir) or resolved.relative_to(build_dir).as_posix() != key:
                    errors.append(
                        f"build-context.json {field}.build path does not resolve exactly: {key}"
                    )
                    continue
            elif _is_relative_to(resolved, repo_root) or _is_relative_to(resolved, build_dir):
                errors.append(
                    f"build-context.json {field}.external path is misclassified: {key}"
                )
                continue
            try:
                actual_digest, actual_count, _identity = _sha256_file_with_identity(resolved)
            except OSError as exc:
                errors.append(
                    f"build-context.json {field}.{category} path could not be hashed stably: {key}: {exc}"
                )
                continue
            if actual_digest != digest or actual_count != byte_count:
                errors.append(
                    f"build-context.json {field}.{category} identity disagrees with raw bytes: {key}"
                )
                continue
            inventory[category][key] = {"sha256": digest, "byte_count": byte_count}
            paths[(category, key)] = resolved
    return inventory, paths


def _inventory_from_recorder_snapshots(
    *,
    repo_root: Path,
    build_dir: Path,
    recorder_paths: dict[str, Path],
    bibtex_inputs: tuple[Path, ...],
    errors: list[str],
) -> dict[str, dict[str, dict[str, Any]]]:
    """Reconstruct the complete per-pass plus BibTeX evidence inventory."""

    candidates: dict[str, Path] = {}
    recorder_inputs: dict[str, set[str]] = {
        "pass_1": set(),
        "pass_3": set(),
        "pass_4": set(),
    }
    for pass_name in ("pass_1", "pass_3", "pass_4"):
        recorder_path = recorder_paths.get(pass_name)
        if recorder_path is None:
            continue
        try:
            payload, _identity = _read_bytes_stable(recorder_path)
            lines = payload.decode("utf-8", errors="strict").splitlines()
        except (OSError, UnicodeError) as exc:
            errors.append(f"build-context.json {pass_name} recorder is not stable strict UTF-8: {exc}")
            continue
        pwd_values = [line[4:] for line in lines if line.startswith("PWD ")]
        if len(pwd_values) != 1:
            errors.append(
                f"build-context.json {pass_name} recorder must contain exactly one PWD record"
            )
            continue
        try:
            recorded_pwd = Path(pwd_values[0]).resolve(strict=True)
        except (OSError, RuntimeError, ValueError) as exc:
            errors.append(f"build-context.json {pass_name} recorder PWD is invalid: {exc}")
            continue
        if recorded_pwd != build_dir:
            errors.append(
                f"build-context.json {pass_name} recorder PWD does not equal the build directory"
            )
        raw_inputs = [line[6:] for line in lines if line.startswith("INPUT ")]
        if not raw_inputs:
            errors.append(f"build-context.json {pass_name} recorder contains no INPUT records")
        for raw_input in raw_inputs:
            if not raw_input:
                errors.append(f"build-context.json {pass_name} recorder contains an empty INPUT record")
                continue
            candidate = Path(raw_input)
            if not candidate.is_absolute():
                candidate = recorded_pwd / candidate
            component = _first_reparse_component(candidate)
            if component is not None:
                errors.append(
                    f"build-context.json {pass_name} recorder input is reparse-mediated at {component}: {raw_input}"
                )
                continue
            try:
                resolved = candidate.resolve(strict=True)
            except (OSError, RuntimeError, ValueError) as exc:
                errors.append(
                    f"build-context.json {pass_name} recorder input is missing: {raw_input}: {exc}"
                )
                continue
            normalized = os.path.normcase(str(resolved))
            candidates[normalized] = resolved
            recorder_inputs[pass_name].add(normalized)

    generated_bbl = build_dir / "main.bbl"
    normalized_generated_bbl = os.path.normcase(str(generated_bbl))
    for pass_name in ("pass_3", "pass_4"):
        if normalized_generated_bbl not in recorder_inputs[pass_name]:
            errors.append(
                f"build-context.json {pass_name} recorder does not declare the canonical generated main.bbl input"
            )

    for bibtex_input in bibtex_inputs:
        component = _first_reparse_component(bibtex_input)
        if component is not None:
            errors.append(
                f"build-context.json BibTeX evidence input is reparse-mediated at {component}: {bibtex_input}"
            )
            continue
        try:
            resolved = bibtex_input.resolve(strict=True)
        except (OSError, RuntimeError, ValueError) as exc:
            errors.append(f"build-context.json BibTeX evidence input is invalid: {bibtex_input}: {exc}")
            continue
        candidates[os.path.normcase(str(resolved))] = resolved

    inventory: dict[str, dict[str, dict[str, Any]]] = {
        "repository": {},
        "build": {},
        "external": {},
    }
    for resolved in sorted(candidates.values(), key=lambda value: os.path.normcase(str(value))):
        if _is_relative_to(resolved, repo_root):
            category = "repository"
            key = resolved.relative_to(repo_root).as_posix()
        elif _is_relative_to(resolved, build_dir):
            category = "build"
            key = resolved.relative_to(build_dir).as_posix()
        else:
            category = "external"
            key = str(resolved)
        try:
            digest, byte_count, _identity = _sha256_file_with_identity(resolved)
        except OSError as exc:
            errors.append(f"cannot hash reconstructed evidence input {resolved}: {exc}")
            continue
        identity = {"sha256": digest, "byte_count": byte_count}
        prior = inventory[category].get(key)
        if prior is not None and prior != identity:
            errors.append(f"reconstructed evidence input changed identity: {key}")
        inventory[category][key] = identity
    return {
        category: dict(sorted(entries.items()))
        for category, entries in inventory.items()
    }


def _require_raw_file_identity_equal(
    *,
    expected_path: Path,
    actual_path: Path,
    label: str,
    errors: list[str],
) -> None:
    """Require two regular files to have the same stable raw-byte identity."""

    identities: list[tuple[str, int]] = []
    for role, path in (("expected", expected_path), ("actual", actual_path)):
        component = _first_reparse_component(path)
        if component is not None:
            errors.append(f"{label} {role} path is reparse-mediated at {component}")
            return
        try:
            resolved = path.resolve(strict=True)
        except (OSError, RuntimeError, ValueError) as exc:
            errors.append(f"{label} {role} path is missing or invalid: {exc}")
            return
        if not resolved.is_file() or _is_reparse_point(resolved):
            errors.append(f"{label} {role} path is not a regular non-reparse file")
            return
        try:
            digest, byte_count, _identity = _sha256_file_with_identity(resolved)
        except OSError as exc:
            errors.append(f"{label} {role} path could not be hashed stably: {exc}")
            return
        identities.append((digest, byte_count))
    if identities[0] != identities[1]:
        errors.append(
            f"{label} raw SHA-256 and byte_count disagree: "
            f"expected sha256={identities[0][0]} byte_count={identities[0][1]}, "
            f"actual sha256={identities[1][0]} byte_count={identities[1][1]}"
        )


def _load_production_build_context(
    *,
    repo_root: Path,
    build_dir: Path,
    source_revision: str,
    head_revision: str | None,
    errors: list[str],
) -> tuple[
    dict[str, str],
    set[str],
    dict[str, Any],
    dict[str, tuple[Path, str, int]],
    dict[str, dict[str, dict[str, Any]]],
    dict[tuple[str, str], Path],
]:
    """Load and validate the mandatory exact production build context."""

    context_path = build_dir / "build-context.json"
    if not context_path.is_file() or _is_reparse_point(context_path):
        errors.append("production profile requires a regular non-reparse build-context.json")
        return {}, set(), {}, {}, {"repository": {}, "build": {}, "external": {}}, {}
    try:
        document = _strict_json_load(context_path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"invalid build-context.json: {exc}")
        return {}, set(), {}, {}, {"repository": {}, "build": {}, "external": {}}, {}
    if not isinstance(document, dict):
        errors.append("build-context.json must contain one JSON object")
        return {}, set(), {}, {}, {"repository": {}, "build": {}, "external": {}}, {}
    observed_keys = set(document)
    missing = sorted(_BUILD_CONTEXT_KEYS - observed_keys)
    unknown = sorted(observed_keys - _BUILD_CONTEXT_KEYS)
    if missing:
        errors.append(f"build-context.json is missing required keys: {', '.join(missing)}")
    if unknown:
        errors.append(f"build-context.json has unknown keys: {', '.join(unknown)}")
    if document.get("protocol_profile") != PRODUCTION_PROTOCOL_PROFILE:
        errors.append(
            f"build-context.json protocol_profile must be exactly {PRODUCTION_PROTOCOL_PROFILE}"
        )
    if document.get("source_revision") != source_revision:
        errors.append("build-context.json source_revision does not equal the requested source revision")
    if head_revision is None or document.get("head_revision") != head_revision:
        errors.append("build-context.json head_revision does not equal the verified current HEAD")
    if document.get("initial_entries") != []:
        errors.append("build-context.json does not attest an empty initial output directory")

    source_dir = repo_root / "manuscripts" / "gauge_vfe_rg"
    for field, expected in (
        ("repository_root", repo_root),
        ("source_directory", source_dir),
        ("output_directory", build_dir),
    ):
        raw_path = document.get(field)
        try:
            matches = isinstance(raw_path, str) and Path(raw_path).resolve(strict=True) == expected.resolve(strict=True)
        except (OSError, RuntimeError, ValueError):
            matches = False
        if not matches:
            errors.append(f"build-context.json {field} does not equal {expected}")

    epoch = document.get("source_date_epoch")
    if not isinstance(epoch, str) or re.fullmatch(r"[0-9]+", epoch) is None:
        errors.append("build-context.json source_date_epoch must be a decimal Git commit timestamp")
    else:
        timestamp = _git(repo_root, "show", "-s", "--format=%ct", source_revision)
        expected_epoch = timestamp.stdout.decode("ascii", errors="replace").strip()
        if timestamp.returncode != 0 or epoch != expected_epoch:
            errors.append("build-context.json source_date_epoch does not equal the source commit timestamp")

    declared_style = document.get("bibtex_style")
    declared_style_path = declared_style.get("path") if isinstance(declared_style, dict) else None
    try:
        style_directory = (
            str(Path(declared_style_path).resolve(strict=True).parent)
            if isinstance(declared_style_path, str)
            else None
        )
    except (OSError, RuntimeError, ValueError):
        style_directory = None
    controlled_texmf_roots = {
        "TEXMFHOME": build_dir / ".texmf-home",
        "TEXMFVAR": build_dir / ".texmf-var",
        "TEXMFCONFIG": build_dir / ".texmf-config",
    }
    for name, path in controlled_texmf_roots.items():
        component = _first_reparse_component(path)
        if component is not None:
            errors.append(f"build-context.json {name} root is reparse-mediated at {component}")
        if not path.is_dir():
            errors.append(f"build-context.json {name} root is not a directory under the build domain")
    controlled_temp_root = build_dir / ".tex-tmp"
    temp_component = _first_reparse_component(controlled_temp_root)
    if temp_component is not None:
        errors.append(f"build-context.json controlled TEMP root is reparse-mediated at {temp_component}")
    if not controlled_temp_root.is_dir():
        errors.append("build-context.json controlled TEMP root is not a directory under the build domain")
    expected_environment = {
        "TEXINPUTS": f"{source_dir.resolve()};{source_dir.parent.resolve()};",
        "BIBINPUTS": str(source_dir.parent.resolve()),
        "BSTINPUTS": style_directory,
        **{name: str(path.resolve()) for name, path in controlled_texmf_roots.items()},
        "SOURCE_DATE_EPOCH": epoch,
    }
    controlled_environment = document.get("controlled_environment")
    if controlled_environment != expected_environment:
        errors.append(
            "build-context.json controlled_environment must contain exact controlled TeX, BibTeX, user-tree, and SOURCE_DATE_EPOCH values"
        )

    _validate_identity_record(
        record=document.get("python_executable"),
        field="python_executable",
        expected_path=_TRUSTED_PYTHON,
        repo_root=None,
        errors=errors,
    )
    _validate_identity_record(
        record=document.get("git_executable"),
        field="git_executable",
        expected_path=_TRUSTED_GIT,
        repo_root=None,
        errors=errors,
    )

    additions: dict[str, str] = {}
    evidence_only: set[str] = set()
    locked_repository_inputs = document.get("locked_repository_inputs")
    validated_locked_inputs: dict[str, dict[str, str | int]] = {}
    if not isinstance(locked_repository_inputs, dict) or not locked_repository_inputs:
        errors.append(
            "build-context.json locked_repository_inputs must be a nonempty exact map"
        )
    else:
        folded_locked_paths: set[str] = set()
        for relative, entry in sorted(locked_repository_inputs.items()):
            folded = relative.casefold()
            if folded in folded_locked_paths:
                errors.append(
                    f"build-context.json locked_repository_inputs has a case collision: {relative!r}"
                )
                continue
            folded_locked_paths.add(folded)
            if not isinstance(entry, dict) or set(entry) != {"byte_count", "sha256"}:
                errors.append(
                    f"build-context.json locked_repository_inputs entry has an invalid shape: {relative!r}"
                )
                continue
            checked = _validate_identity_record(
                record={"path": relative, **entry},
                field=f"locked_repository_inputs entry {relative}",
                expected_path=None,
                repo_root=repo_root,
                errors=errors,
            )
            if checked is None:
                continue
            path, digest, byte_count = checked
            exact_relative = path.relative_to(repo_root).as_posix()
            validated_locked_inputs[exact_relative] = {
                "sha256": digest,
                "byte_count": byte_count,
            }
            additions[exact_relative] = digest
    expected_repository_paths = {
        "build_script": source_dir / "build.ps1",
        "main_tex": source_dir / "main.tex",
        "run_checks": source_dir / "verification" / "run_checks.py",
        "build_audit": source_dir / "verification" / "build_audit.py",
        "references_bib": source_dir.parent / "references.bib",
        "verification_result": None,
    }
    verified_paths: dict[str, Path] = {}
    for field, expected_path in expected_repository_paths.items():
        verified = _validate_identity_record(
            record=document.get(field),
            field=field,
            expected_path=expected_path,
            repo_root=repo_root,
            errors=errors,
        )
        if verified is None:
            continue
        path, digest, count = verified
        relative = path.relative_to(repo_root).as_posix()
        additions[relative] = digest
        verified_paths[field] = path
        if field == "verification_result":
            evidence_only.add(relative)
        else:
            locked_identity = validated_locked_inputs.get(relative)
            if locked_identity != {"sha256": digest, "byte_count": count}:
                errors.append(
                    f"build-context.json {field} does not equal its prelocked repository identity"
                )

    external_inputs: dict[str, tuple[Path, str, int]] = {}
    for field, expected_tool in (
        ("pdflatex_executable", "pdflatex"),
        ("bibtex_executable", "bibtex"),
    ):
        verified_tool = _validate_identity_record(
            record=document.get(field),
            field=field,
            expected_path=None,
            repo_root=None,
            errors=errors,
        )
        if verified_tool is None:
            continue
        tool_path, tool_digest, tool_count = verified_tool
        if _tool_name(str(tool_path)) != expected_tool:
            errors.append(f"build-context.json {field} does not name {expected_tool}")
            continue
        external_inputs[str(tool_path)] = (tool_path, tool_digest, tool_count)
    bibtex_style = _validate_identity_record(
        record=document.get("bibtex_style"),
        field="bibtex_style",
        expected_path=None,
        repo_root=None,
        errors=errors,
    )
    if bibtex_style is not None:
        style_path, style_digest, style_count = bibtex_style
        if style_path.name.casefold() != "plainnat.bst":
            errors.append("build-context.json bibtex_style must name exactly plainnat.bst")
        else:
            external_inputs[str(style_path)] = (style_path, style_digest, style_count)

    repository_build_script = _validate_identity_record(
        record=document.get("repository_build_script"),
        field="repository_build_script",
        expected_path=source_dir / "build.ps1",
        repo_root=None,
        errors=errors,
    )
    executed_build_script: tuple[Path, str, int] | None = None
    attested_executed_record = document.get("executed_build_script")
    if not isinstance(attested_executed_record, dict) or set(attested_executed_record) != {
        "path",
        "sha256",
        "byte_count",
    }:
        errors.append(
            "build-context.json executed_build_script must be one exact bootstrap-attested path/hash/count identity"
        )
    else:
        executed_path_value = attested_executed_record.get("path")
        executed_digest = attested_executed_record.get("sha256")
        executed_count = attested_executed_record.get("byte_count")
        executed_candidate = Path(executed_path_value) if isinstance(executed_path_value, str) else Path()
        if (
            not isinstance(executed_path_value, str)
            or not executed_candidate.is_absolute()
            or not isinstance(executed_digest, str)
            or _SHA256_RE.fullmatch(executed_digest) is None
            or isinstance(executed_count, bool)
            or not isinstance(executed_count, int)
            or executed_count <= 0
        ):
            errors.append("build-context.json executed_build_script has an invalid bootstrap-attested identity")
        elif _first_reparse_component(executed_candidate) is not None:
            errors.append("build-context.json bootstrap-attested executed_build_script is reparse-mediated")
        else:
            try:
                executed_path = executed_candidate.resolve(strict=True)
            except (OSError, RuntimeError, ValueError) as exc:
                errors.append(
                    f"build-context.json bootstrap-attested executed_build_script path is missing: {exc}"
                )
            else:
                if not executed_path.is_file() or _is_reparse_point(executed_path):
                    errors.append(
                        "build-context.json bootstrap-attested executed_build_script is not a regular file"
                    )
                else:
                    executed_build_script = (executed_path, executed_digest, executed_count)
    bootstrap_attestation = _validate_identity_record(
        record=document.get("bootstrap_attestation"),
        field="bootstrap_attestation",
        expected_path=None,
        repo_root=None,
        errors=errors,
    )
    repository_script = verified_paths.get("build_script")
    if repository_build_script is not None and repository_script is not None:
        if repository_build_script != (
            repository_script,
            str(document["build_script"]["sha256"]),
            int(document["build_script"]["byte_count"]),
        ):
            errors.append(
                "build-context.json repository_build_script does not equal build_script raw-byte identity"
            )
    if repository_build_script is not None and executed_build_script is not None:
        if repository_build_script[1:] != executed_build_script[1:]:
            errors.append(
                "build-context.json bootstrap-attested executed_build_script identity does not equal repository_build_script bytes"
            )

    if bootstrap_attestation is not None:
        attestation_path = bootstrap_attestation[0]
        try:
            attestation = _strict_json_load(attestation_path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"bootstrap attestation is not strict JSON: {exc}")
        else:
            attestation_keys = {
                "protocol_profile",
                "source_revision",
                "repository_root",
                "source_directory",
                "repository_build_script",
                "executed_build_script",
                "source_blob_oid",
                "source_blob_byte_count",
                "source_sha256",
                "bootstrap_temporary_directory",
                "bootstrap_parent_pid",
                "powershell_path",
                "git_path",
            }
            if not isinstance(attestation, dict) or set(attestation) != attestation_keys:
                errors.append("bootstrap attestation does not have the exact required property set")
            elif repository_build_script is not None and executed_build_script is not None:
                expected_attestation_values = {
                    "protocol_profile": PRODUCTION_PROTOCOL_PROFILE,
                    "source_revision": source_revision,
                    "repository_root": str(repo_root),
                    "source_directory": str(source_dir.resolve()),
                    "repository_build_script": str(repository_build_script[0]),
                    "executed_build_script": str(executed_build_script[0]),
                    "source_blob_byte_count": executed_build_script[2],
                    "source_sha256": executed_build_script[1],
                    "powershell_path": r"C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe",
                    "git_path": str(_TRUSTED_GIT),
                }
                if any(attestation.get(key) != value for key, value in expected_attestation_values.items()):
                    errors.append("bootstrap attestation does not bind the exact production build invocation")
                if (
                    not isinstance(attestation.get("source_blob_oid"), str)
                    or _REVISION_RE.fullmatch(attestation["source_blob_oid"]) is None
                    or isinstance(attestation.get("bootstrap_parent_pid"), bool)
                    or not isinstance(attestation.get("bootstrap_parent_pid"), int)
                    or attestation["bootstrap_parent_pid"] < 1
                ):
                    errors.append("bootstrap attestation has an invalid typed source identity")
                temporary_value = attestation.get("bootstrap_temporary_directory")
                try:
                    attested_temporary = Path(temporary_value).resolve(strict=True)
                except (TypeError, OSError, RuntimeError, ValueError) as exc:
                    errors.append(f"bootstrap attestation temporary directory is invalid: {exc}")
                else:
                    if (
                        not attested_temporary.is_dir()
                        or _first_reparse_component(attested_temporary) is not None
                        or executed_build_script[0] != attested_temporary / "build.ps1"
                        or attestation_path != attested_temporary / "bootstrap-attestation.json"
                    ):
                        errors.append(
                            "bootstrap attestation and executed source are not exact children of its temporary directory"
                        )
                source_oid = _git(
                    repo_root,
                    "rev-parse",
                    f"{source_revision}:manuscripts/gauge_vfe_rg/build.ps1",
                )
                if (
                    source_oid.returncode != 0
                    or source_oid.stdout.decode("ascii", errors="replace").strip()
                    != attestation.get("source_blob_oid")
                ):
                    errors.append("bootstrap attestation source_blob_oid does not equal the Git build-script blob")

    recorder_paths: dict[str, Path] = {}
    recorder_snapshots = document.get("recorder_snapshots")
    if not isinstance(recorder_snapshots, dict) or list(recorder_snapshots) != [
        "pass_1",
        "pass_3",
        "pass_4",
    ]:
        errors.append(
            "build-context.json recorder_snapshots must contain exactly ordered pass_1, pass_3, and pass_4 identities"
        )
    else:
        for pass_name, pass_number in (("pass_1", 1), ("pass_3", 3), ("pass_4", 4)):
            checked = _validate_identity_record(
                record=recorder_snapshots.get(pass_name),
                field=f"recorder_snapshots.{pass_name}",
                expected_path=build_dir / f"main-pass-{pass_number}.fls",
                repo_root=None,
                errors=errors,
            )
            if checked is not None:
                recorder_paths[pass_name] = checked[0]

    evidence_inventory, evidence_paths = _validate_typed_input_inventory(
        record=document.get("evidence_input_inventory"),
        repo_root=repo_root,
        build_dir=build_dir,
        field="evidence_input_inventory",
        errors=errors,
    )
    references_path = verified_paths.get("references_bib")
    if bibtex_style is not None and references_path is not None and len(recorder_paths) == 3:
        reconstructed_inventory = _inventory_from_recorder_snapshots(
            repo_root=repo_root,
            build_dir=build_dir,
            recorder_paths=recorder_paths,
            bibtex_inputs=(
                bibtex_style[0],
                references_path,
                build_dir / "main-bibtex.bbl",
            ),
            errors=errors,
        )
        snapshot_bbl_identity = reconstructed_inventory["build"].get("main-bibtex.bbl")
        recorder_bbl_identity = reconstructed_inventory["build"].get("main.bbl")
        if snapshot_bbl_identity is None or recorder_bbl_identity is None:
            errors.append(
                "build-context.json reconstructed inventory must contain both main-bibtex.bbl and recorder-derived main.bbl"
            )
        elif snapshot_bbl_identity != recorder_bbl_identity:
            errors.append(
                "build-context.json main-bibtex.bbl raw SHA-256 and byte_count do not equal recorder-derived main.bbl"
            )
        _require_raw_file_identity_equal(
            expected_path=build_dir / "main-bibtex.bbl",
            actual_path=build_dir / "main.bbl",
            label="BibTeX generated BBL snapshot versus recorder-derived final main.bbl",
            errors=errors,
        )
        if reconstructed_inventory != evidence_inventory:
            errors.append(
                "build-context.json evidence_input_inventory does not equal the complete pass_1/pass_3/pass_4 plus BibTeX inventory"
            )

    fixed_point = document.get("external_input_fixed_point")
    fixed_inputs: dict[str, dict[str, Any]] = {}
    if not isinstance(fixed_point, dict) or set(fixed_point) != {
        "max_iterations",
        "converged_iteration",
        "inputs",
    }:
        errors.append("build-context.json external_input_fixed_point has an invalid shape")
    else:
        maximum = fixed_point.get("max_iterations")
        converged = fixed_point.get("converged_iteration")
        if maximum != 8:
            errors.append("build-context.json external_input_fixed_point.max_iterations must equal 8")
        if isinstance(converged, bool) or not isinstance(converged, int) or not 2 <= converged <= 8:
            errors.append(
                "build-context.json external_input_fixed_point.converged_iteration must be an integer from 2 through 8"
            )
        fixed_inventory, _fixed_paths = _validate_typed_input_inventory(
            record={"repository": {}, "build": {}, "external": fixed_point.get("inputs")},
            repo_root=repo_root,
            build_dir=build_dir,
            field="external_input_fixed_point.inputs",
            errors=errors,
        )
        fixed_inputs = fixed_inventory["external"]
        if fixed_inputs != evidence_inventory["external"]:
            errors.append(
                "build-context.json fixed-point inputs do not exactly equal the external evidence inventory"
            )

    result_path = verified_paths.get("verification_result")
    if result_path is not None:
        try:
            result_document = _strict_json_load(result_path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"verification result is not strict JSON: {exc}")
        else:
            if not isinstance(result_document, dict):
                errors.append("verification result must contain one JSON object")
            else:
                if result_document.get("protocol_profile") != PRODUCTION_PROTOCOL_PROFILE:
                    errors.append(
                        f"verification result protocol_profile must be exactly {PRODUCTION_PROTOCOL_PROFILE}"
                    )
                if result_document.get("source_revision") != source_revision:
                    errors.append("verification result source_revision does not equal the requested source revision")
                if result_document.get("overall_status") != "PASS":
                    errors.append("verification result overall_status is not PASS")
                manifest = result_document.get("manifest")
                if not isinstance(manifest, dict) or set(manifest) != {
                    "hash_algorithm",
                    "hash_domain",
                    "path_semantics",
                    "bound_inputs",
                }:
                    errors.append("verification result manifest envelope is invalid")
                elif (
                    manifest.get("hash_algorithm") != "SHA-256"
                    or manifest.get("hash_domain") != "raw file bytes"
                    or manifest.get("path_semantics") != "repository-relative POSIX paths"
                    or not isinstance(manifest.get("bound_inputs"), dict)
                    or not manifest["bound_inputs"]
                ):
                    errors.append("verification result manifest envelope is invalid")
                else:
                    if manifest["bound_inputs"] != locked_repository_inputs:
                        errors.append(
                            "verification result manifest bound_inputs does not exactly equal "
                            "build-context.json locked_repository_inputs"
                        )
                    for relative, entry in sorted(manifest["bound_inputs"].items()):
                        if not isinstance(entry, dict) or set(entry) != {"byte_count", "sha256"}:
                            errors.append(f"verification manifest entry has an invalid shape: {relative!r}")
                            continue
                        checked = _validate_identity_record(
                            record={"path": relative, **entry},
                            field=f"verification manifest entry {relative}",
                            expected_path=None,
                            repo_root=repo_root,
                            errors=errors,
                        )
                        if checked is None:
                            continue
                        path, digest, _count = checked
                        manifest_relative = path.relative_to(repo_root).as_posix()
                        prior = additions.get(manifest_relative)
                        if prior is not None and prior != digest:
                            errors.append(
                                f"verification manifest disagrees with build-context identity: {manifest_relative}"
                            )
                        additions[manifest_relative] = digest
    return (
        dict(sorted(additions.items())),
        evidence_only,
        document,
        dict(sorted(external_inputs.items())),
        evidence_inventory,
        evidence_paths,
    )


def _source_inventory(
    repo_root: Path,
    build_dir: Path,
    source_revision: str,
    require_context: bool,
    errors: list[str],
) -> tuple[dict[str, str], set[str]]:
    candidates = _inventory_from_fls(repo_root, build_dir, errors)
    if not candidates and not (build_dir / "main.fls").is_file():
        candidates = [
            path
            for path in _walk_regular_files(repo_root, errors, "repository")
            if path.suffix.casefold() in _SOURCE_SUFFIXES
        ]
    bibliography = repo_root / "manuscripts" / "references.bib"
    if bibliography.is_file() and not _is_reparse_point(bibliography):
        candidates.append(bibliography.resolve())
    inventory: dict[str, str] = {}
    for path in sorted(candidates, key=lambda item: item.relative_to(repo_root).as_posix()):
        relative = path.relative_to(repo_root).as_posix()
        try:
            inventory[relative] = _sha256_file(path)
        except OSError as exc:
            errors.append(f"cannot hash source input {relative}: {exc}")
    context_inputs, evidence_only = _load_legacy_build_context_inputs(
        repo_root=repo_root,
        build_dir=build_dir,
        source_revision=source_revision,
        require_context=require_context,
        errors=errors,
    )
    for relative, digest in context_inputs.items():
        prior = inventory.get(relative)
        if prior is not None and prior != digest:
            errors.append(f"build-context.json identity disagrees with source inventory: {relative}")
        inventory[relative] = digest
    casefolded: dict[str, str] = {}
    for relative in sorted(inventory):
        prior = casefolded.get(relative.casefold())
        if prior is not None and prior != relative:
            errors.append(f"source inventory has a case-fold path collision: {prior!r}, {relative!r}")
        casefolded[relative.casefold()] = relative
    if not inventory:
        errors.append("source inventory is empty")
    return dict(sorted(inventory.items())), evidence_only


def _capture_inventory_state(
    repo_root: Path,
    inventory: dict[str, str],
    errors: list[str],
    phase: str,
) -> dict[str, tuple[int, ...]]:
    states: dict[str, tuple[int, ...]] = {}
    for relative, expected_digest in sorted(inventory.items()):
        path = repo_root.joinpath(*relative.split("/"))
        try:
            digest, _byte_count, identity = _sha256_file_with_identity(path)
        except OSError as exc:
            errors.append(f"cannot capture {phase} source state for {relative}: {exc}")
            continue
        if digest != expected_digest:
            errors.append(f"{phase} source digest disagrees with inventory: {relative}")
        states[relative] = identity
    return states


def _verify_inventory_at_revision(
    repo_root: Path,
    revision: str | None,
    inventory: dict[str, str],
    evidence_only: set[str],
    errors: list[str],
) -> None:
    if revision is None:
        return
    for relative, worktree_digest in inventory.items():
        if relative in evidence_only:
            continue
        listing = _git(
            repo_root,
            "--literal-pathspecs",
            "-c",
            "core.quotepath=false",
            "ls-tree",
            "-z",
            revision,
            "--",
            relative,
        )
        if listing.returncode != 0 or not listing.stdout:
            errors.append(f"source input is absent from Git revision {revision}: {relative}")
            continue
        records = listing.stdout[:-1].split(b"\0") if listing.stdout.endswith(b"\0") else []
        if len(records) != 1 or b"\t" not in records[0]:
            errors.append(f"source input has an invalid Git tree record: {relative}")
            continue
        header, encoded_path = records[0].split(b"\t", 1)
        pieces = header.split(b" ")
        try:
            listed_path = encoded_path.decode("utf-8")
        except UnicodeError:
            errors.append(f"source input has a non-UTF-8 Git path: {relative}")
            continue
        if (
            len(pieces) != 3
            or pieces[0] not in {b"100644", b"100755"}
            or pieces[1] != b"blob"
            or listed_path != relative
        ):
            errors.append(f"source input is not one regular Git blob: {relative}")
            continue
        oid = pieces[2].decode("ascii", errors="replace")
        blob = _git(repo_root, "cat-file", "blob", oid)
        if blob.returncode != 0:
            errors.append(f"cannot read Git blob for source input {relative}")
            continue
        blob_digest = _sha256_bytes(blob.stdout)
        if blob_digest != worktree_digest:
            errors.append(
                f"raw source input bytes differ from the exact Git blob at revision {revision}: {relative}"
            )


def _decode_text(path: Path, errors: list[str]) -> str:
    try:
        raw, _identity = _read_bytes_stable(path)
        return raw.decode("utf-8")
    except UnicodeError as exc:
        errors.append(f"{path.name} is not valid UTF-8: {exc}")
        return raw.decode("utf-8", errors="replace")
    except OSError as exc:
        errors.append(f"cannot read {path.name}: {exc}")
        return ""


def _inspect_bibtex_dependency_declarations(
    build_dir: Path,
    errors: list[str],
) -> None:
    """Bind BibTeX-only style/database declarations omitted by pdfTeX recorder."""

    aux_path = build_dir / "main-bibtex.aux"
    blg_path = build_dir / "main-bibtex.blg"
    for label, path in (("AUX", aux_path), ("BLG", blg_path)):
        component = _first_reparse_component(path)
        if component is not None:
            errors.append(f"BibTeX {label} dependency snapshot is reparse-mediated at {component}")
            return
        if not path.is_file() or _is_reparse_point(path):
            errors.append(
                f"missing required regular non-reparse BibTeX {label} dependency snapshot: {path.name}"
            )
            return
    aux_text = _decode_text(aux_path, errors)
    blg_text = _decode_text(blg_path, errors)
    aux_styles = re.findall(r"^\\bibstyle\{([^{}]+)\}\s*$", aux_text, re.MULTILINE)
    aux_databases = re.findall(r"^\\bibdata\{([^{}]+)\}\s*$", aux_text, re.MULTILINE)
    if aux_styles != ["plainnat"]:
        errors.append(
            f"main-bibtex.aux must declare exactly one BibTeX style plainnat; found {aux_styles!r}"
        )
    if aux_databases != ["references"]:
        errors.append(
            f"main-bibtex.aux must declare exactly one BibTeX database references; found {aux_databases!r}"
        )

    blg_styles = [
        value.strip()
        for value in re.findall(r"^The style file:\s*(.+?)\s*$", blg_text, re.MULTILINE)
    ]
    blg_databases = [
        value.strip()
        for value in re.findall(r"^Database file #\d+:\s*(.+?)\s*$", blg_text, re.MULTILINE)
    ]
    if blg_styles != ["plainnat.bst"]:
        errors.append(
            f"main-bibtex.blg must declare exactly one logical plainnat.bst style; found {blg_styles!r}"
        )
    if blg_databases != ["references.bib"]:
        errors.append(
            f"main-bibtex.blg must declare exactly one logical references.bib database; found {blg_databases!r}"
        )
    _require_raw_file_identity_equal(
        expected_path=blg_path,
        actual_path=build_dir / "main.blg",
        label="BibTeX BLG dependency snapshot versus final main.blg",
        errors=errors,
    )


def _strip_tex_comments(text: str) -> str:
    stripped: list[str] = []
    for line in text.splitlines():
        cut = len(line)
        for index, character in enumerate(line):
            if character != "%":
                continue
            slash_count = 0
            cursor = index - 1
            while cursor >= 0 and line[cursor] == "\\":
                slash_count += 1
                cursor -= 1
            if slash_count % 2 == 0:
                cut = index
                break
        stripped.append(line[:cut])
    return "\n".join(stripped)


def _line_findings(text: str, predicate: Any, prefix: str) -> list[str]:
    findings: list[str] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if predicate(line):
            findings.append(f"{prefix}:{line_number}: {line.strip()}")
    return findings


def _inspect_sources(
    repo_root: Path,
    inventory: dict[str, str],
    errors: list[str],
    duplicate_labels: list[str],
    invalid_status_tags: list[str],
    doubled_status_tags: list[str],
) -> dict[str, str]:
    source_texts: dict[str, str] = {}
    labels: dict[str, list[str]] = {}
    for relative in sorted(inventory):
        if not relative.casefold().endswith(".tex"):
            continue
        path = repo_root / Path(relative)
        text = _decode_text(path, errors)
        try:
            inspected_digest = _sha256_file(path)
        except OSError as exc:
            errors.append(f"cannot rehash inspected TeX source {relative}: {exc}")
        else:
            if inspected_digest != inventory[relative]:
                errors.append(f"TeX source changed after M0 inventory: {relative}")
        source_texts[relative] = text
        uncommented = _strip_tex_comments(text)
        for match in re.finditer(r"\\label\s*\{([^{}]+)\}", uncommented):
            labels.setdefault(match.group(1), []).append(relative)
        for match in re.finditer(r"\\status\s*\{([^{}]+)\}", uncommented):
            token = match.group(1).strip()
            if token not in _ALLOWED_STATUSES:
                line_number = uncommented.count("\n", 0, match.start()) + 1
                invalid_status_tags.append(
                    f"{relative}:{line_number}: invalid status {token!r}"
                )
        offset = 0
        for paragraph in re.split(r"\n\s*\n", uncommented):
            statuses = re.findall(r"\\status\s*\{([^{}]+)\}", paragraph)
            if len(statuses) > 1 and "status taxonomy" not in paragraph.casefold():
                line_number = uncommented.count("\n", 0, offset) + 1
                doubled_status_tags.append(
                    f"{relative}:{line_number}: multiple status tags in one paragraph: {', '.join(statuses)}"
                )
            offset += len(paragraph) + 2
    for label, locations in sorted(labels.items()):
        if len(locations) > 1:
            duplicate_labels.append(
                f"source duplicate label {label!r}: {', '.join(locations)}"
            )
    return source_texts


def _inspect_log(
    log_text: str,
    undefined_references: list[str],
    undefined_citations: list[str],
    rerun_requests: list[str],
    fatal_errors: list[str],
    overfull_boxes: list[str],
    literal_double_question_marks: list[str],
    invalid_status_tags: list[str],
    duplicate_labels: list[str],
) -> None:
    for line_number, line in enumerate(log_text.splitlines(), 1):
        lower = line.casefold()
        location = f"main.log:{line_number}: {line.strip()}"
        if "undefined" in lower and "reference" in lower:
            undefined_references.append(location)
        if "undefined" in lower and "citation" in lower:
            undefined_citations.append(location)
        if (
            "rerun" in lower
            or "re-run" in lower
            or "label(s) may have changed" in lower
            or "please run bibtex" in lower
            or "please (re)run bibtex" in lower
        ):
            rerun_requests.append(location)
        if (
            line.lstrip().startswith("!")
            or "emergency stop" in lower
            or "fatal error" in lower
            or "no output pdf file produced" in lower
            or "undefined control sequence" in lower
            or "file ended while scanning use of" in lower
        ):
            fatal_errors.append(location)
        if "overfull \\hbox" in lower or "overfull \\vbox" in lower:
            overfull_boxes.append(location)
        if "??" in line:
            literal_double_question_marks.append(location)
        if "multiply defined" in lower or "multiply-defined labels" in lower:
            duplicate_labels.append(location)
        for match in re.finditer(r"STATUS:\s*([A-Za-z0-9_-]+)", line, re.IGNORECASE):
            token = match.group(1)
            if token not in _ALLOWED_STATUSES:
                invalid_status_tags.append(
                    f"main.log:{line_number}: invalid status {token!r}"
                )


def _inspect_aux(aux_text: str, duplicate_labels: list[str]) -> None:
    labels: dict[str, list[int]] = {}
    for line_number, line in enumerate(aux_text.splitlines(), 1):
        for match in re.finditer(r"\\newlabel\s*\{([^{}]+)\}", line):
            labels.setdefault(match.group(1), []).append(line_number)
    for label, lines in sorted(labels.items()):
        if len(lines) > 1:
            duplicate_labels.append(
                f"main.aux: duplicate \\newlabel{{{label}}} on lines {', '.join(map(str, lines))}"
            )


def _inspect_stale_auxiliaries(build_dir: Path, errors: list[str]) -> list[str]:
    findings: list[str] = []
    for path in _walk_regular_files(build_dir, errors, "build directory"):
        relative = path.relative_to(build_dir).as_posix()
        name = path.name.casefold()
        if name.endswith(_AUXILIARY_SUFFIXES) and name not in _AUXILIARY_NAMES:
            findings.append(f"unexpected auxiliary artifact: {relative}")
    context_path = build_dir / "build-context.json"
    if context_path.is_file():
        try:
            context = _strict_json_load(context_path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"invalid build-context.json: {exc}")
        else:
            initial_entries = context.get("initial_entries") if isinstance(context, dict) else None
            if initial_entries != []:
                findings.append(
                    f"build-context.json records nonempty start inventory: {initial_entries!r}"
                )
    return findings


def _inspect_source_tree_auxiliaries(repo_root: Path, errors: list[str]) -> list[str]:
    canonical = repo_root / "manuscripts" / "gauge_vfe_rg"
    if (canonical / "main.tex").is_file():
        source_root = canonical
    elif (repo_root / "main.tex").is_file():
        source_root = repo_root
    else:
        errors.append("cannot locate the manuscript source root for stale-auxiliary inspection")
        return []
    findings: list[str] = []
    for path in _walk_regular_files(source_root, errors, "manuscript source tree"):
        name = path.name.casefold()
        if name.endswith(_AUXILIARY_SUFFIXES):
            relative = path.relative_to(repo_root).as_posix()
            findings.append(f"source-tree auxiliary artifact: {relative}")
    return findings


def _artifact_snapshot(
    build_dir: Path,
    errors: list[str],
    phase: str,
) -> tuple[dict[str, str], dict[str, tuple[int, ...]]]:
    active = _ACTIVE_BUILD_ARTIFACTS.get()
    if active is not None and active.root == build_dir:
        return active.snapshot(errors, phase)
    hashes: dict[str, str] = {}
    states: dict[str, tuple[int, ...]] = {}
    for path in _walk_regular_files(build_dir, errors, "build directory"):
        relative = path.relative_to(build_dir).as_posix()
        try:
            digest, _byte_count, identity = _sha256_file_with_identity(path)
            hashes[relative] = digest
            states[relative] = identity
        except OSError as exc:
            errors.append(f"cannot hash build artifact {relative}: {exc}")
    return dict(sorted(hashes.items())), dict(sorted(states.items()))


def audit_build(
    *,
    repo_root: Path,
    build_dir: Path,
    source_revision: str,
    command_record: Path,
    test_fixture: bool = False,
) -> AuditResult:
    """Acquire one complete retained artifact domain and audit it through M1."""

    with _retain_build_artifact_inventory(Path(build_dir)) as retained:
        token = _ACTIVE_BUILD_ARTIFACTS.set(retained)
        try:
            return _audit_build_core(
                repo_root=repo_root,
                build_dir=build_dir,
                source_revision=source_revision,
                command_record=command_record,
                test_fixture=test_fixture,
                retained_artifacts=retained,
            )
        finally:
            _ACTIVE_BUILD_ARTIFACTS.reset(token)


def _audit_build_core(
    *,
    repo_root: Path,
    build_dir: Path,
    source_revision: str,
    command_record: Path,
    test_fixture: bool,
    retained_artifacts: _RetainedBuildArtifactInventory,
) -> AuditResult:
    """Audit one already-completed isolated build without mutating its bytes.

    Args:
        repo_root: Exact Git worktree root containing the manuscript source.
        build_dir: Isolated directory containing build artifacts and evidence.
        source_revision: Full lowercase Git commit bound to source inputs.
        command_record: Strict JSON command evidence inside ``build_dir``.
        test_fixture: Allow the intentionally reduced synthetic-test protocol.
            This relaxation is API-only and is never exposed by the CLI.
    """

    if type(test_fixture) is not bool:
        raise TypeError("test_fixture must be exactly bool")

    errors: list[str] = list(retained_artifacts.acquisition_errors)
    trusted_executables_m0: dict[
        str,
        tuple[dict[str, str | int], tuple[int, ...]],
    ] = {}
    if not test_fixture:
        for field, path in (
            ("python_executable", _TRUSTED_PYTHON),
            ("git_executable", _TRUSTED_GIT),
        ):
            try:
                trusted_executables_m0[field] = _trusted_executable_snapshot(path)
            except OSError as exc:
                errors.append(f"cannot capture trusted {field} identity at M0: {exc}")
                continue
            locked_path, locked_stream, locked_m0 = _AUDIT_EXECUTABLE_LOCKS[field]
            try:
                _assert_locked_stream_m0(locked_path, locked_stream, locked_m0, field)
            except (OSError, RuntimeError) as exc:
                errors.append(f"trusted {field} retained launch handle is invalid at M0: {exc}")
                continue
            record_m0, identity_m0 = trusted_executables_m0[field]
            if (
                record_m0 != {
                    "path": locked_m0["path"],
                    "sha256": locked_m0["sha256"],
                    "byte_count": locked_m0["byte_count"],
                }
                or identity_m0 != locked_m0["stat_identity"]
            ):
                errors.append(f"trusted {field} path M0 does not equal retained launch-handle M0")
    duplicate_labels: list[str] = []
    undefined_references: list[str] = []
    undefined_citations: list[str] = []
    rerun_requests: list[str] = []
    fatal_errors: list[str] = []
    overfull_boxes: list[str] = []
    literal_double_question_marks: list[str] = []
    invalid_status_tags: list[str] = []
    doubled_status_tags: list[str] = []

    original_repo_root = Path(repo_root)
    original_build_dir = Path(build_dir)
    for original, label in (
        (original_repo_root, "repository root"),
        (original_build_dir, "build directory"),
    ):
        component = _first_reparse_component(original)
        if component is not None:
            errors.append(f"{label} path is reparse-mediated at {component}")
    try:
        repo_root = original_repo_root.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        repo_root = original_repo_root.resolve()
        errors.append(f"invalid repository root: {exc}")
    try:
        build_dir = original_build_dir.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        build_dir = original_build_dir.resolve()
        errors.append(f"invalid build directory: {exc}")
    command_record = Path(command_record)
    if not command_record.is_absolute():
        command_record = build_dir / command_record
    command_component = _first_reparse_component(command_record)
    if command_component is not None:
        errors.append(f"command record path is reparse-mediated at {command_component}")
    command_record = command_record.resolve()

    if not repo_root.is_dir():
        errors.append(f"repository root is not a directory: {repo_root}")
    if not build_dir.is_dir():
        errors.append(f"build directory is not a directory: {build_dir}")
    if _is_relative_to(build_dir, repo_root):
        errors.append("build directory must be outside the repository source tree")
    if not _is_relative_to(command_record, build_dir):
        errors.append("command record must be inside the build directory")
    if test_fixture:
        production_context_path = build_dir / "build-context.json"
        full_production_files_present = (
            (repo_root / "manuscripts" / "gauge_vfe_rg" / "main.tex").is_file()
            and production_context_path.is_file()
            and all((build_dir / name).is_file() for name in _REQUIRED_ARTIFACTS)
        )
        production_profile_context = False
        if full_production_files_present:
            try:
                candidate_context = _strict_json_load(production_context_path)
            except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
                candidate_context = None
            production_profile_context = (
                isinstance(candidate_context, dict)
                and candidate_context.get("protocol_profile") == PRODUCTION_PROTOCOL_PROFILE
            )
        if production_profile_context:
            errors.append(
                "synthetic test-fixture protocol rejects a production-shaped source/build envelope"
            )

    protocol_profile = (
        SYNTHETIC_PROTOCOL_PROFILE if test_fixture else PRODUCTION_PROTOCOL_PROFILE
    )
    build_context: dict[str, Any] = {}
    artifact_hashes, artifact_states_m0 = (
        _artifact_snapshot(build_dir, errors, "M0") if build_dir.is_dir() else ({}, {})
    )

    git_metadata_ok = (
        True
        if test_fixture
        else _reject_git_metadata_overrides(repo_root, errors)
        if repo_root.is_dir()
        else False
    )
    git_top_level_ok = (
        _verify_git_top_level(repo_root, errors)
        if repo_root.is_dir() and git_metadata_ok
        else False
    )
    resolved_revision = (
        _resolve_source_revision(repo_root, source_revision, errors)
        if repo_root.is_dir() and git_top_level_ok and git_metadata_ok
        else None
    )
    head_revision = (
        _resolve_head_and_require_ancestry(repo_root, source_revision, errors)
        if not test_fixture and resolved_revision is not None
        else None
    )
    main_tex = (
        repo_root / "manuscripts" / "gauge_vfe_rg" / "main.tex"
        if not test_fixture
        else None
    )
    if main_tex is not None:
        try:
            main_tex = main_tex.resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            errors.append(f"production main.tex is missing or invalid: {exc}")
            main_tex = None
    commands, tool_versions = _load_commands(
        command_record,
        production=not test_fixture,
        build_dir=build_dir,
        main_tex=main_tex,
        errors=errors,
    )

    evidence_only: set[str]
    repository_inventory: dict[str, str]
    classified_paths: dict[tuple[str, str], Path] = {}
    if test_fixture:
        input_inventory, evidence_only = (
            _source_inventory(
                repo_root,
                build_dir,
                source_revision,
                False,
                errors,
            )
            if repo_root.is_dir() and build_dir.is_dir()
            else ({}, set())
        )
        repository_inventory = dict(input_inventory)
        input_states_m0: dict[Any, tuple[int, ...]] = (
            _capture_inventory_state(repo_root, repository_inventory, errors, "M0")
            if repo_root.is_dir()
            else {}
        )
    else:
        input_inventory = {"repository": {}, "build": {}, "external": {}}
        if git_metadata_ok and repo_root.is_dir() and build_dir.is_dir():
            (
                context_inputs,
                evidence_only,
                build_context,
                context_external_inputs,
                context_evidence_inventory,
                context_evidence_paths,
            ) = _load_production_build_context(
                repo_root=repo_root,
                build_dir=build_dir,
                source_revision=source_revision,
                head_revision=head_revision,
                errors=errors,
            )
            input_inventory = context_evidence_inventory
            classified_paths = context_evidence_paths
            final_recorder_inventory, _final_recorder_paths = (
                _production_inventory_from_fls(repo_root, build_dir, errors)
            )
            _validate_final_recorder_binding(
                build_dir=build_dir,
                build_context=build_context,
                recorder_inventory=final_recorder_inventory,
                evidence_inventory=input_inventory,
                errors=errors,
            )
            for field, (record_m0, _identity_m0) in trusted_executables_m0.items():
                if build_context.get(field) != record_m0:
                    errors.append(
                        f"build-context.json {field} does not equal its audit M0 raw-byte identity"
                    )
            controlled_environment = build_context.get("controlled_environment")
            locked_repository_inputs = build_context.get("locked_repository_inputs")
            if isinstance(locked_repository_inputs, dict):
                for relative in sorted(input_inventory["repository"]):
                    if relative not in locked_repository_inputs:
                        errors.append(
                            "repository input from the complete evidence inventory was not present in the prelocked "
                            f"source envelope: {relative}"
                        )
            if isinstance(controlled_environment, dict):
                for index, command in enumerate(commands, 1):
                    environment = command.get("environment")
                    if isinstance(environment, dict):
                        observed_controlled = {
                            name: environment.get(name) for name in _CONTROLLED_TEX_ENV_KEYS
                        }
                        if observed_controlled != controlled_environment:
                            errors.append(
                                f"command record {index} controlled TeX environment does not equal build-context.json"
                            )
                    tool = _tool_name(str(command.get("executable", "")))
                    field = (
                        "pdflatex_executable"
                        if tool == "pdflatex"
                        else "bibtex_executable"
                        if tool == "bibtex"
                        else None
                    )
                    if field is not None:
                        declared_tool = build_context.get(field)
                        if (
                            not isinstance(declared_tool, dict)
                            or command.get("executable") != declared_tool.get("path")
                        ):
                            errors.append(
                                f"command record {index} executable does not equal build-context.json {field}"
                            )
        else:
            context_inputs, evidence_only, context_external_inputs = {}, set(), {}
            errors.append(
                f"{PRODUCTION_PROTOCOL_PROFILE} build context could not be verified because Git metadata is unsafe"
            )
        for relative, digest in context_inputs.items():
            path = repo_root.joinpath(*relative.split("/"))
            try:
                actual_digest, byte_count, _identity = _sha256_file_with_identity(path)
            except OSError as exc:
                errors.append(f"cannot retain production context input {relative}: {exc}")
                continue
            if actual_digest != digest:
                errors.append(f"production context input digest changed: {relative}")
            input_inventory["repository"][relative] = {
                "sha256": actual_digest,
                "byte_count": byte_count,
            }
            classified_paths[("repository", relative)] = path.resolve()
        for key, (path, digest, byte_count) in context_external_inputs.items():
            prior = input_inventory["external"].get(key)
            record = {"sha256": digest, "byte_count": byte_count}
            if prior is not None and prior != record:
                errors.append(f"external input identity disagrees with main.fls inventory: {key}")
            input_inventory["external"][key] = record
            classified_paths[("external", key)] = path
        input_inventory = {
            category: dict(sorted(entries.items()))
            for category, entries in input_inventory.items()
        }
        repository_inventory = {
            relative: record["sha256"]
            for relative, record in input_inventory["repository"].items()
        }
        input_states_m0 = _capture_classified_inventory_state(
            input_inventory,
            classified_paths,
            errors,
            "M0",
        )
    _verify_inventory_at_revision(
        repo_root,
        resolved_revision,
        repository_inventory,
        evidence_only,
        errors,
    )
    source_manifest_digest = _sha256_bytes(
        json.dumps(
            input_inventory,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    )

    _inspect_sources(
        repo_root,
        repository_inventory,
        errors,
        duplicate_labels,
        invalid_status_tags,
        doubled_status_tags,
    )

    required_artifacts = (
        tuple(name for name in _REQUIRED_ARTIFACTS if name not in {"main.fls", "main.blg"})
        if test_fixture
        else _REQUIRED_ARTIFACTS
    )
    for name in required_artifacts:
        path = build_dir / name
        if not path.is_file() or _is_reparse_point(path):
            errors.append(f"missing required regular artifact: {name}")

    log_text = ""
    log_path = build_dir / "main.log"
    if log_path.is_file() and not _is_reparse_point(log_path):
        log_text = _decode_text(log_path, errors)
        _inspect_log(
            log_text,
            undefined_references,
            undefined_citations,
            rerun_requests,
            fatal_errors,
            overfull_boxes,
            literal_double_question_marks,
            invalid_status_tags,
            duplicate_labels,
        )

    aux_path = build_dir / "main.aux"
    if aux_path.is_file() and not _is_reparse_point(aux_path):
        _inspect_aux(_decode_text(aux_path, errors), duplicate_labels)
    if not test_fixture:
        _inspect_bibtex_dependency_declarations(build_dir, errors)

    pdf_sha256 = ""
    pdf_byte_count = 0
    page_count = 0
    pdf_metadata: dict[str, str | None] = {
        field: None for field, _pdf_key in _PDF_METADATA_FIELDS
    }
    pdf_path = build_dir / "main.pdf"
    if pdf_path.is_file() and not _is_reparse_point(pdf_path):
        try:
            pdf_bytes, _pdf_identity = _read_bytes_stable(pdf_path)
            pdf_sha256 = _sha256_bytes(pdf_bytes)
            pdf_byte_count = len(pdf_bytes)
            if not pdf_bytes.startswith(b"%PDF-") or not pdf_bytes.rstrip().endswith(b"%%EOF"):
                raise ValueError("missing a valid PDF header or EOF marker")
            reader = PdfReader(BytesIO(pdf_bytes), strict=True)
            page_count = len(reader.pages)
            if page_count < 1:
                raise ValueError("PDF page tree is empty")
            metadata = reader.metadata
            if metadata is None:
                raise ValueError("PDF has no real /Info metadata dictionary")
            for field, pdf_key in _PDF_METADATA_FIELDS:
                raw_value = metadata.get(pdf_key)
                value = str(raw_value) if raw_value is not None else None
                pdf_metadata[field] = value
                if value is None or not value.strip():
                    errors.append(f"main.pdf metadata is missing {field}")
            for number, page in enumerate(reader.pages, 1):
                try:
                    text = page.extract_text() or ""
                except Exception as exc:
                    errors.append(f"cannot extract text from main.pdf page {number}: {exc}")
                    continue
                if "??" in text:
                    literal_double_question_marks.append(
                        f"main.pdf:page {number}: extracted text contains literal ??"
                    )
        except Exception as exc:
            errors.append(f"main.pdf failed strict PDF parsing: {exc}")
            page_count = 0
            pdf_metadata = {field: None for field, _pdf_key in _PDF_METADATA_FIELDS}
    if pdf_sha256 and artifact_hashes.get("main.pdf") != pdf_sha256:
        errors.append("pdf_sha256 does not equal artifact_hashes['main.pdf']")

    if log_text:
        output_records = list(_OUTPUT_RE.finditer(log_text))
        if not output_records:
            errors.append("main.log has no final Output written on main.pdf record")
        elif pdf_byte_count and page_count:
            record = output_records[-1]
            target = record.group(1).strip().strip('"')
            log_pages = int(record.group(2))
            log_bytes = int(record.group(3))
            if Path(target).name.casefold() != "main.pdf":
                errors.append(f"main.log output target is not main.pdf: {target}")
            if log_pages != page_count:
                errors.append(
                    f"main.log page count {log_pages} disagrees with parsed main.pdf page count {page_count}"
                )
            if log_bytes != pdf_byte_count:
                errors.append(
                    f"main.log byte count {log_bytes} disagrees with actual main.pdf byte count {pdf_byte_count}"
                )

    stale_auxiliary_files = (
        _inspect_stale_auxiliaries(build_dir, errors) if build_dir.is_dir() else []
    )
    if repo_root.is_dir():
        stale_auxiliary_files.extend(_inspect_source_tree_auxiliaries(repo_root, errors))

    if repo_root.is_dir() and build_dir.is_dir():
        if test_fixture:
            input_inventory_m1, evidence_only_m1 = _source_inventory(
                repo_root,
                build_dir,
                source_revision,
                False,
                errors,
            )
            input_states_m1 = _capture_inventory_state(
                repo_root,
                input_inventory_m1,
                errors,
                "M1",
            )
            if input_inventory_m1 != input_inventory or evidence_only_m1 != evidence_only:
                errors.append("source input inventory changed between M0 and M1")
        else:
            if git_metadata_ok:
                (
                    context_inputs_m1,
                    evidence_only_m1,
                    build_context_m1,
                    context_external_inputs_m1,
                    input_inventory_m1,
                    classified_paths_m1,
                ) = _load_production_build_context(
                    repo_root=repo_root,
                    build_dir=build_dir,
                    source_revision=source_revision,
                    head_revision=head_revision,
                    errors=errors,
                )
            else:
                (
                    context_inputs_m1,
                    evidence_only_m1,
                    build_context_m1,
                    context_external_inputs_m1,
                ) = {}, set(), {}, {}
                input_inventory_m1 = {"repository": {}, "build": {}, "external": {}}
                classified_paths_m1 = {}
            locked_repository_inputs_m1 = build_context_m1.get("locked_repository_inputs")
            if isinstance(locked_repository_inputs_m1, dict):
                for relative in sorted(input_inventory_m1["repository"]):
                    if relative not in locked_repository_inputs_m1:
                        errors.append(
                            "M1 repository input from the complete evidence inventory was not present in the prelocked "
                            f"source envelope: {relative}"
                        )
            for relative, digest in context_inputs_m1.items():
                path = repo_root.joinpath(*relative.split("/"))
                try:
                    actual_digest, byte_count, _identity = _sha256_file_with_identity(path)
                except OSError as exc:
                    errors.append(f"cannot retain M1 production context input {relative}: {exc}")
                    continue
                input_inventory_m1["repository"][relative] = {
                    "sha256": actual_digest,
                    "byte_count": byte_count,
                }
                classified_paths_m1[("repository", relative)] = path.resolve()
                if digest != actual_digest:
                    errors.append(f"M1 production context input digest changed: {relative}")
            for key, (path, digest, byte_count) in context_external_inputs_m1.items():
                prior = input_inventory_m1["external"].get(key)
                record = {"sha256": digest, "byte_count": byte_count}
                if prior is not None and prior != record:
                    errors.append(f"M1 BibTeX style identity disagrees with main.fls inventory: {key}")
                input_inventory_m1["external"][key] = record
                classified_paths_m1[("external", key)] = path
            input_inventory_m1 = {
                category: dict(sorted(entries.items()))
                for category, entries in input_inventory_m1.items()
            }
            input_states_m1 = _capture_classified_inventory_state(
                input_inventory_m1,
                classified_paths_m1,
                errors,
                "M1",
            )
            if (
                input_inventory_m1 != input_inventory
                or evidence_only_m1 != evidence_only
                or build_context_m1 != build_context
            ):
                errors.append("source input inventory changed between M0 and M1")
        if input_states_m1 != input_states_m0:
            errors.append("source input identity or metadata changed between M0 and M1")

    artifact_hashes_m1, artifact_states_m1 = (
        _artifact_snapshot(build_dir, errors, "M1") if build_dir.is_dir() else ({}, {})
    )
    if artifact_hashes_m1 != artifact_hashes:
        errors.append("build artifact inventory changed between M0 and M1")
    if artifact_states_m1 != artifact_states_m0:
        errors.append("build artifact identity or metadata changed between M0 and M1")
    if not test_fixture and repo_root.is_dir():
        closing_metadata_ok = _reject_git_metadata_overrides(repo_root, errors)
        if closing_metadata_ok:
            final_head_revision = _resolve_head_and_require_ancestry(
                repo_root,
                source_revision,
                errors,
            )
            if final_head_revision != head_revision:
                errors.append(
                    "current Git HEAD changed between audit M0 and M1: "
                    f"{head_revision!r} -> {final_head_revision!r}"
                )
    if not test_fixture:
        for field, path in (
            ("python_executable", _TRUSTED_PYTHON),
            ("git_executable", _TRUSTED_GIT),
        ):
            snapshot_m0 = trusted_executables_m0.get(field)
            try:
                snapshot_m1 = _trusted_executable_snapshot(path)
            except OSError as exc:
                errors.append(f"cannot capture trusted {field} identity at M1: {exc}")
                continue
            if snapshot_m0 is None or snapshot_m1 != snapshot_m0:
                errors.append(f"trusted {field} bytes or filesystem identity changed between M0 and M1")
            locked_path, locked_stream, locked_m0 = _AUDIT_EXECUTABLE_LOCKS[field]
            try:
                _assert_locked_stream_m0(locked_path, locked_stream, locked_m0, field)
            except (OSError, RuntimeError) as exc:
                errors.append(f"trusted {field} retained launch handle is invalid at M1: {exc}")
    pages_to_render = list(range(1, page_count + 1))

    errors = _unique(errors)
    duplicate_labels = _unique(duplicate_labels)
    undefined_references = _unique(undefined_references)
    undefined_citations = _unique(undefined_citations)
    rerun_requests = _unique(rerun_requests)
    fatal_errors = _unique(fatal_errors)
    overfull_boxes = _unique(overfull_boxes)
    literal_double_question_marks = _unique(literal_double_question_marks)
    invalid_status_tags = _unique(invalid_status_tags)
    doubled_status_tags = _unique(doubled_status_tags)
    stale_auxiliary_files = _unique(stale_auxiliary_files)
    finding_lists = (
        errors,
        duplicate_labels,
        undefined_references,
        undefined_citations,
        rerun_requests,
        fatal_errors,
        overfull_boxes,
        literal_double_question_marks,
        invalid_status_tags,
        doubled_status_tags,
        stale_auxiliary_files,
    )

    return AuditResult(
        ok=not any(finding_lists),
        protocol_profile=protocol_profile,
        source_revision=source_revision,
        errors=errors,
        tool_versions=tool_versions,
        inspection_tool_versions=_pypdf_distribution_provenance(),
        commands=commands,
        build_context=build_context,
        input_inventory=input_inventory,
        source_manifest_digest=source_manifest_digest,
        pdf_sha256=pdf_sha256,
        pdf_byte_count=pdf_byte_count,
        page_count=page_count,
        pdf_metadata=pdf_metadata,
        artifact_hashes=artifact_hashes,
        pages_to_render=pages_to_render,
        changed_pages=list(pages_to_render),
        duplicate_labels=duplicate_labels,
        undefined_references=undefined_references,
        undefined_citations=undefined_citations,
        rerun_requests=rerun_requests,
        fatal_errors=fatal_errors,
        overfull_boxes=overfull_boxes,
        literal_double_question_marks=literal_double_question_marks,
        invalid_status_tags=invalid_status_tags,
        doubled_status_tags=doubled_status_tags,
        stale_auxiliary_files=stale_auxiliary_files,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--build-dir", required=True, type=Path)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--command-record", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser


def _run_cli_audit_with_retained_artifacts(
    *,
    arguments: argparse.Namespace,
    retained: _RetainedBuildArtifactInventory,
    output: Path,
    python_digest_m0: str,
    pypdf_snapshot_m0: dict[str, Any],
    pypdf_provenance_m0: dict[str, Any],
) -> int:
    """Run, publish, and attest while every M0 artifact handle remains retained."""

    token = _ACTIVE_BUILD_ARTIFACTS.set(retained)
    try:
        outcome = _audit_build_core(
            repo_root=arguments.repo_root,
            build_dir=arguments.build_dir,
            source_revision=arguments.source_revision,
            command_record=arguments.command_record,
            test_fixture=False,
            retained_artifacts=retained,
        )
        try:
            python_digest_m1 = _sha256_file(_TRUSTED_PYTHON)
        except OSError as exc:
            raise SystemExit(f"cannot re-hash trusted Python runtime after audit: {exc}") from exc
        if python_digest_m1 != python_digest_m0:
            raise SystemExit("trusted Python runtime bytes changed during build audit")
        _assert_no_undeclared_fixed_site_modules(_PYPDF_SITE_FINDER)
        _assert_controlled_pycache_empty()
        try:
            pypdf_snapshot_m1 = _bootstrap_pypdf_distribution_snapshot()
        except (OSError, RuntimeError, ValueError) as exc:
            raise SystemExit(f"cannot re-bind trusted pypdf distribution at M1: {exc}") from exc
        pypdf_provenance_m1 = {
            **pypdf_snapshot_m1["provenance"],
            "pypdf_pycache_prefix": str(_PYPDF_PYCACHE_ROOT),
        }
        if pypdf_snapshot_m1 != pypdf_snapshot_m0:
            raise SystemExit(
                "trusted pypdf distribution bytes or filesystem identities changed during build audit"
            )
        if pypdf_provenance_m1 != pypdf_provenance_m0:
            raise SystemExit("trusted pypdf distribution bytes changed during build audit")
        if outcome.inspection_tool_versions != pypdf_provenance_m1:
            raise SystemExit("build audit report pypdf provenance does not equal the M1 byte identity")
        _publish_new_json_with_digest(output, outcome.to_dict(), sys.stdout.buffer)
        return 0 if outcome.ok else 1
    finally:
        _ACTIVE_BUILD_ARTIFACTS.reset(token)


def main(argv: list[str] | None = None) -> int:
    python_digest_m0 = _require_production_cli_runtime()
    pypdf_snapshot_m0 = _PYPDF_ADMISSION_M0
    pypdf_provenance_m0 = {
        **pypdf_snapshot_m0["provenance"],
        "pypdf_pycache_prefix": str(_PYPDF_PYCACHE_ROOT),
    }
    parser = _parser()
    arguments = parser.parse_args(argv)
    repo_root = arguments.repo_root.resolve()
    build_dir = arguments.build_dir.resolve()
    command_record = arguments.command_record
    if not command_record.is_absolute():
        command_record = build_dir / command_record
    command_record = command_record.resolve()
    output = arguments.output.resolve()
    if output == command_record:
        parser.error("--output must not equal --command-record")
    if _is_relative_to(output, build_dir):
        parser.error("--output must be outside --build-dir and its artifact hash domain")
    if _is_relative_to(output, repo_root):
        parser.error("--output must be outside --repo-root and its governed source tree")
    with _retain_build_artifact_inventory(build_dir) as retained:
        return _run_cli_audit_with_retained_artifacts(
            arguments=arguments,
            retained=retained,
            output=output,
            python_digest_m0=python_digest_m0,
            pypdf_snapshot_m0=pypdf_snapshot_m0,
            pypdf_provenance_m0=pypdf_provenance_m0,
        )


if __name__ == "__main__":
    raise SystemExit(main())
